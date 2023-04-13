## 0.1. link リンク

- https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio

## 0.2. title タイトル

SimClusters: Community-Based Representations for Heterogeneous Recommendations at Twitter
SimClusters（シムクラスター）： Twitterにおける異質なレコメンデーションのためのコミュニティベース表現

## 0.3. abstract アブストラクト

Personalized recommendation products at Twitter target a multitude of heterogeneous items: Tweets, Events, Topics, Hashtags, and users.
Twitterのパーソナライズド・レコメンデーション製品は、多数の異質なアイテムを対象としている： ツイート、イベント、トピック、ハッシュタグ、そしてユーザ.
Each of these targets varies in their cardinality (which affects the scale of the problem) and their "shelf life'' (which constrains the latency of generating the recommendations).
これらのターゲットはそれぞれ、問題の規模に影響するカーディナリティと、レコメンデーション生成の待ち時間に制約を与える「賞味期限」が異なる.
Although Twitter has built a variety of recommendation systems before dating back a decade, solutions to the broader problem were mostly tackled piecemeal.
Twitterは10年前から様々なレコメンデーションシステムを構築してきましたが、広い意味での問題解決は**断片的な取り組みがほとんどだった.**
In this paper, we present SimClusters, a general-purpose representation layer based on overlapping communities into which users as well as heterogeneous content can be captured as sparse, interpretable vectors to support a multitude of recommendation tasks.
本論文では、重複するコミュニティに基づく汎用的な表現層であるSimClustersを紹介し、ユーザや異質なコンテンツを疎な解釈可能なベクトルとして捉え、様々な推薦タスクをサポートすることができる.
We propose a novel algorithm for community discovery based on Metropolis-Hastings sampling, which is both more accurate and significantly faster than off-the-shelf alternatives.
我々は、メトロポリス・ヘイスティングスサンプリングに基づくコミュニティ発見のための新しいアルゴリズムを提案し、既製の代替品よりも高精度かつ大幅に高速であることを示す.
SimClusters scales to networks with billions of users and has been effective across a variety of deployed applications at Twitter.
SimClustersは数十億人のユーザーを抱えるネットワークにスケールし、Twitterの様々なデプロイメントアプリケーションで効果を発揮している.

# 1. Introduction 序章

Personalized recommendations lie at the heart of many different technology-enabled products, and Twitter is no exception.
パーソナライズされたレコメンデーションは、**さまざまなテクノロジーを駆使したproductの中核をなすもの**であり、Twitterも例外ではない.
Our highlevel goal is to make content discovery effortless and to free the user from the need for manual curation.
私たちの高い目標は、**コンテンツの発見を容易にし、手動によるキュレーションの必要性からユーザを解放すること**である.
On the Twitter platform, a wide variety of content types are displayed in a multitude of contexts, requiring a variety of personalization approaches.
Twitterでは、様々な種類のコンテンツが様々な文脈で表示されるため、様々なパーソナライゼーションアプローチが必要.
For example, recommendations of interesting Tweets are an essential component of not only the Home tab, but also for dissemination via email or push notifications.
例えば、面白いツイートのレコメンドは、ホームタブだけでなく、メールやプッシュ通知での配信にも欠かせない要素である.
The “Who To Follow” module with user follow recommendations is crucial, especially for new users, and was one of the first recommendations products to be launched on Twitter [11].
**ユーザフォローを推薦する「Who To Follow」モジュールは、特に新規ユーザにとって重要**であり、Twitterで最初に発表されたレコメンデーション製品の1つである[11].(これはNPにも当てはまる.)
Trends and Events (previously called Moments) are essential for informing the user about currently ongoing news stories and topics of conversation on the platform, and the Explore tab shows the user a personalized list of these.
**トレンドとイベント(以前の名称はモーメント)は、現在進行中のニュースやプラットフォーム上で話題になっていることをユーザに知らせるために不可欠なもの**で、エクスプローラタブでは、これらのリストをユーザにパーソナライズして表示する.(NPで言えばNewsアイテムか...)
The recently launched Topics feature1 lets users follow Topics (such as “Machine Learning” or “K-Pop”) and see the algorithmically curated best tweets about those Topics in their Home feed.
**最近開始されたトピックス機能では、ユーザーはトピックス(「機械学習」や「K-POP」など)をフォローし、そのトピックスに関するアルゴリズムでキュレートされたベストツイートをホームフィードで見ることができる**.(これは、NPのkeyword follow機能に該当するのかな.)

A summary of the diversity of personalized recommendation problems at Twitter is presented in Table 1.
Twitterにおけるパーソナライズド・レコメンデーション問題の多様性をまとめたものを表1に示す.
In all cases, we are making recommendations to users, but what we’re recommending can be heterogeneous.
どのような場合でも、私たちはユーザに対して推薦を行っていますが、推薦するものは異質なものである可能性がある.
For example, we could be suggesting users, Tweets, Events, Topics, or hashtags.
例えば、ユーザ、ツイート、イベント、トピック、ハッシュタグを suggest することができる.
There are two main dimensions of interest across the different recommendations problems: the cardinality of the items being recommended and the shelf life of the computed recommendations.
異なるレコメンデーション問題で注目される2つの主要な次元があります：推薦されるアイテムのカーディナリティ(=unique値の数だっけ?)と計算された推薦の shelf life(賞味期限)である.
The shelf life of our computed recommendations is closely related to the churn we observe in the recommended content.
計算されたレコメンデーションの賞味期限は、推薦のコンテンツで観察される解約と密接に関係している.
For example, since the follower graph changes relatively slowly, user follow recommendations can remain relevant for weeks (and thus can be computed in batch).
例えば、フォロワーグラフは比較的ゆっくりと変化するため、ユーザフォローの推薦は数週間にわたり関連性を保つことができる(したがって、**バッチ処理で計算することができる**)
At the other end of the spectrum, Tweet recommendations become stale much quicker and must be generated in an online system in close to real time; for this case, batch computations would not yield results fast enough to meet the product requirements.
一方、**ツイート推薦は陳腐化するのが早く、オンラインシステムでリアルタイムに近い形で生成する必要があり**、この場合、バッチ計算では製品要件を満たすのに十分な速度で結果を得ることができない.
Naturally, in the case of recommendation problems where the item cardinality is large, being able to handle the scale of the problem is important.
当然、アイテムのカーディナリティが大きい推薦問題の場合、問題の規模に対応できることが重要.

Previously, Twitter built systems to tackle each of these different recommendation problems individually with little re-use or commonality.
これまでTwitterは、**これらの異なるレコメンデーション問題に個別に対応するシステムを構築しており、再利用や共通化はほとんど行われていなかった**.
The original example here is the “Who To Follow” system that launched a decade ago [11] for user recommendations.
ここでの元例は、10年前に発売されたユーザ推薦のための「Who To Follow」システム[11]である.
Subsequently, Gupta et al.[12] described a specialized system to generate Tweet recommendations in real time, insights from which were later deployed in GraphJet [31].
その後、Guptaら[12]は、リアルタイムでツイートレコメンデーションを生成する特殊なシステムについて説明し、そこから得た知見は後にGraphJet[31]に展開された.
GraphJet ingested the realtime stream of user-Tweet engagements to maintain a user-Tweet bipartite graph from which to generate recommendations, but the system was expensive to extend to new use cases.
GraphJetは、ユーザーとツイートの関係をリアルタイムに取り込み、ユーザーとツイートの二部グラフを維持し、そこからレコメンデーションを生成しますが、このシステムは新しいユースケースに拡張するには高価だった.
These aforementioned infrastructures were built mainly to generate candidates which got blended and scored subsequently.
これらのインフラは、**主にcandidatesを生み出し、それをブレンドして採点するために構築されたもの**である.
Twitter also built custom infrastructure for feature retrieval and scoring of arbitrarily generated candidates - examples include RealGraph [14] and RecService [9].
また、Twitterは、任意に生成された候補の特徴検索やスコアリングのためのカスタムインフラを構築している.
All of these systems were built with the aim of solving specific sub-problems in the recommendations landscape at Twitter and require separate development and maintenance.
これらのシステムはすべて、Twitterのレコメンデーション状況における特定のサブ問題を解決する目的で構築され、**個別の開発・保守が必要である**.
The central motivating question of this paper is: can we build a general system that helps us advance the accuracy of all or most of the Twitter products which require personalization and recommendations?
本論文の中心的な動機付けとなる問いは、**パーソナライズやレコメンデーションが必要なTwitter製品のすべて、あるいはほとんどの精度を高めるのに役立つ一般的なシステムを構築できるか**ということである.

The solution proposed in this paper is built on the insight that we can construct, from the user–user graph, a general-purpose representation based on community structure, where each community is characterized by a set of influencers that many people in that community follow.
本論文で提案するソリューションは、**ユーザ \* ユーザグラフ**から、コミュニティ構造に基づく汎用的な表現を構築できるという洞察に基づいており、各コミュニティは、そのコミュニティ内の多くの人々がフォローしているインフルエンサーのセットによって特徴づけられる.
Each of the different kinds of content (i.e., the targets in Table 1) is represented as a vector in the space of these communities, with the entry corresponding to the 𝑖-th community for item 𝑗 indicating how interested the 𝑖-th community is in item 𝑗.
**異なる種類のコンテンツ(すなわち表1のターゲット)のそれぞれは、これらのコミュニティの空間におけるベクトルとして表され**、アイテム $j$ に対する $i$ 番目のコミュニティに対応するエントリは、$i$番目のコミュニティがアイテム $j$ にどれだけ興味を持っているかを示している.
The end result is that we can represent heterogeneous recommendation targets as sparse, interpretable vectors in the same space, which enables solutions for a wide variety of recommendation and personalization tasks (see details in Section 6).
最終的には、**異質な推薦対象を、同じ空間のスパースで解釈可能なベクトルとして表現することができ**、様々な推薦やパーソナライゼーションタスクのソリューションが可能になる(詳細はセクション6を参照).
There are two notable aspects of our design:
私たちのデザインには、2つの特筆すべき点がある：

- 1. We avoid conventional matrix factorization methods that typically require solving massive numerical optimization problems, and instead rely on a combination of similarity search and community discovery, both of which are easier to scale. A key algorithmic innovation of our work is a new approach to community discovery — called Neighborhood-aware MH — which is 10×-100× faster, 3×-4× more accurate than off-theshelf baselines, and scales easily to graphs with ∼109 nodes and ∼1011 edges. It helps us discover ∼105 communities on Twitter that are either organized around a common topic (e.g., “K-Pop” or “Machine Learning”) or based on social relationships (e.g., those who work together or went to high-school together). We have open-sourced the implementation of the new algorithm in https://github.com/twitter/sbf. 1. 私たちは、**大規模な数値最適化問題を解く必要がある従来の行列分解法を避け、代わりに、スケールアップが容易な類似性検索とコミュニティ発見の組み合わせに頼っている**. このアルゴリズムは、既存のベースラインと比較して、10倍から100倍高速で、3倍から4倍高精度であり、109個のノードと1011個のエッジを持つグラフに容易に拡張することができる. 「K-POP」や「機械学習」といった共通の話題や、「職場が一緒」「高校が一緒」といった社会的関係から構成されるTwitter上のコミュニティ（約105件）を発見することができる. 新しいアルゴリズムの実装は、https://github.com/twitter/sbf、オープンソース化している.

- 2.  Our overall architecture has a modular and extensible design to enable the use of whichever computing paradigm is most suited to a specific component – batch-distributed, batch-multicore, or streaming-distributed. In particular, the ability to dynamically update representations using streaming-distributed components has proved crucial for accurately modeling Tweets which are Twitter’s most important type of content. 2. 私たちのアーキテクチャは、特定のコンポーネントに最も適したコンピューティングパラダイム(バッチ分散、バッチマルチコア、ストリーミング分散)を使用できるように、**全体的にモジュール式で拡張可能な設計となっている**. 特に、Twitterで最も重要なコンテンツであるツイートを正確にモデル化するためには、ストリーミング分散コンポーネントを用いて表現を動的に更新する能力が重要であることが証明された.

We refer to our overall system as SimClusters (Similarity-based Clusters) and have deployed it in production for more than a year.
私たちは、このシステム全体をSimClusters（Similarity-based Clusters）と呼び、1年以上にわたって実運用に展開しています。

SimClusters also has the following features, which correspond to our design requirements:
また、SimClustersは、私たちの設計要件に対応した以下のような特徴を持っている：

- 1. Universal representations: SimClusters provides representations for both users and a variety of content in the same space. This removes the need to invest in expensive custom infrastructure for each type of content. 1. ユニバーサルな表現： SimClustersは、**ユーザと様々なコンテンツの両方を同じ空間で表現することができる**. これにより、**コンテンツの種類ごとに高価なカスタムインフラに投資する必要がなくなった**.

- 2. Computational scale: We are able to apply SimClusters at Twitter scale, with $~10^9$ users, $~10^{11}$ edges between them, and $10^8$ new Tweets every day with $~10^9$ user engagements per day. 2. 計算規模： SimClustersは、$~10^9$ 人のユーザー、$~10^{11}$ 人のエッジ、毎日$10^8$件の新しいツイート、1日あたり$~10^9$人のユーザーのエンゲージメントを持つTwitterスケールで適用することが可能である.

- 3. Accuracy beyond the head: SimClusters representations are accurate beyond just the most popular content (“head”), primarily due to the ability to scale SimClusters to a very large representational space with ∼105 dimensions. 3. 頭部を超えた正確さ: SimClustersの表現は、最も人気のあるコンテンツ(“head”)(most popular推薦より良いって事?)を超えて正確.これは主に、SimClustersを約105次元という非常に大きな表現空間に拡張できることによる.

- 4. Item and graph churn: The modular design of SimClusters makes it easy to extend to dynamic items which rapidly rise and diminish in popularity. Many of our important recommendations and engagement prediction problem involve items that churn rapidly – most Tweets, Events, and Trends stay relevant for no more than a day or two, meaning that it is crucial to be able to efficiently learn representations of new items before they lose their relevance. 4. アイテムやグラフの入れ替わり： SimClustersのモジュール設計により、人気が急上昇・急降下する動的アイテムへの拡張が容易である. 私たちの重要なレコメンデーションやエンゲージメント予測の問題の多くは、急速に変化するアイテムを含んでいる. ほとんどのツイート、イベント、トレンドは、1日か2日程度しか関連性がない.

- 5. Interpretability: SimClusters representations are sparse and each dimension corresponds to a specific community, making them interpretable to a degree that is hard to obtain with alternatives such as matrix factorization or graph embeddings. 5. 解釈のしやすさ SimClustersの表現は疎であり、各次元は特定のコミュニティに対応しているため、行列分解やグラフ埋め込みなどの代替手段では得難い解釈可能性を持っている.

- 6. Efficient nearest neighbor search: Identifying nearest neighbors is core to many downstream tasks such as generating recommendations, similar item retrieval, and user targeting. The sparsity of SimClusters representations makes it easy to setup and maintain inverted indices for retrieving nearest neighbors, even for rapidly churning domains (see details in Section 4). 6. 効率的な近傍探索 **近傍探索は、レコメンデーションの生成、類似アイテムの検索、ユーザターゲティングなど、多くの下流タスクの中核となる**. SimClusters表現のスパース性は、急速に変化するドメインであっても、最近傍を検索するための転置インデックスの設定と維持を容易にする(詳細はセクション4でご覧ください).

SimClusters has been applied to many recommendations and personalization problems at Twitter — even for mature products such as out-of-network Tweet recommendations and Personalized Trends, SimClusters has enabled double digit improvements in the engagement rates of recommendations.
**SimClustersは、Twitterの多くのレコメンデーションやパーソナライゼーションの問題に適用されている**. ネットワーク外のツイート推薦やパーソナライズド・トレンドなどの成熟した製品においても、SimClustersは推薦のエンゲージメント率を2桁改善することを可能にした.
It has also accelerated the building of entirely new products, such as Similar Tweets and Topic Tweet recommendations.
また、Similar TweetやTopic Tweetのレコメンデーションなど、全く新しいプロダクトの構築も加速している.
SimClusters continues to be actively developed internally and applied to new use cases.
**SimClustersは、社内で活発に開発され、新しいユースケースに適用され続けている.**

# 2. Overview of SimClusters SimClustersの概要

The SimClusters system (see Figure 1) consists of two stages:
SimClustersシステム(図1参照)は、2つのステージで構成されている：

![](https://camo.qiitausercontent.com/91062517c63bafedf6953cf10b1e3a74c62de8de/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32623466333165372d653361632d306639642d656431392d6361316535303763623534332e706e67)

- 1. In the first stage (detailed in Section 3), we discover bipartite communities from our user-user graph at scale, resulting in learning sparse, non-negative representations for our users. At the end of this stage, each user is associated with a list of communities they participate in, along with the scores quantifying the strength of their affiliation to each of those communities. We refer to this output as “User Interest Representations” and it is made available in both offline data warehouses as well as low-latency online stores, indexed by the user id. This first stage is run in a batch-distributed setting, typically as a series of MapReduce jobs running on Hadoop. 1. 第1段階(セクション3で詳述)では、ユーザとユーザのグラフから二部コミュニティを大規模に発見し、その結果、ユーザーの疎な非負表現を学習する. この段階が終わると、**各ユーザは自分が参加しているコミュニティのリストと、それぞれのコミュニティへの所属の強さを数値化したスコアとに関連づけられる**. この出力は"User Interest Representations"と呼ばれ、オフラインのデータウェアハウスと低遅延のオンラインストアの両方で、ユーザIDによってインデックス化されて利用できるようになっている. この最初の段階は、バッチ分散型の設定で実行され、通常はHadoop上で実行される一連のMapReduceジョブとして実行される.

- 2. The second stage (detailed in Section 4) consists of several jobs running in parallel, each of which calculates the representations for a specific recommendation target, using a user–target bipartite graph formed from interaction logs on the platform. Each job in the second stage operates in either a batch-distributed setting or a streaming-distributed setting, depending on the shelf-life of the recommendation target and the churn in the corresponding user–target bipartite graph. 2. 第2段階(セクション4で詳述)は、並行して実行される複数のジョブで構成され、各ジョブは、プラットフォーム上の対話ログから形成されるユーザとターゲットの二部グラフを用いて、特定の推薦対象に対する表現を計算する. 第2ステージの各ジョブは、推薦対象の賞味期限と対応するユーザ・ターゲット二部グラフのチャーンに応じて、バッチ分散設定またはストリーミング分散設定のどちらかで動作する.

The most important detail about our design is that it’s based on discovering communities from the user–user graph.
私たちのデザインで最も重要なのは、**ユーザとユーザのグラフ(この bipartite graphの事がよくわからない...)からコミュニティを発見することに基づいていること**である.
While the other user–target graphs on Twitter evolve rapidly, the user–user graph is relatively long-term and stable, and the specific communities discovered from the graph often outlive specific edges or nodes in the graph.
Twitterの他のユーザ・ターゲットグラフが急速に進化するのに対し、**ユーザ・ユーザグラフは比較的長期的に安定しており**、グラフから発見された特定のコミュニティは、グラフの特定のエッジやノードよりも長生きすることが多いのである.
In addition, the user-user graph usually also has more coverage, in the sense that there are a lot more users who have a minimum number of edges in this graph compared to the other user-item graphs.
また、ユーザ & ユーザグラフは、他のユーザ & アイテムグラフと比較して、このグラフのエッジ数が最小となるユーザが多いという意味で、通常、カバレッジが高いとも言える.

The other important aspect of our design is its modularity.
私たちのデザインのもう一つの重要な点は、モジュール化されていることである.
The different parts of the pipeline depend on each other only via offline data sets or online key-value stores, meaning that they are robust to delays in the preceding steps.
パイプラインの異なる部分は、オフラインのデータセットまたはオンラインのキーバリューストアを介してのみ互いに依存し、先行ステップの遅延に対して堅牢であることを意味する.
It is also easy to swap out existing implementations with new variants, or run multiple implementations in parallel, as long as the output is in the format expected by the downstream jobs.
また、下流のジョブが期待する出力形式であれば、既存の実装を新しいものに置き換えたり、複数の実装を並列に実行することも容易である.
The system degrades gracefully in the presence of bugs and errors - if any one of the item representation jobs has an issue, the other item representation jobs can still service their applications.
バグやエラーが発生しても、システムは優雅に劣化する. アイテム表現ジョブの1つに問題が発生しても、他のアイテム表現ジョブはそのアプリケーションにサービスを提供できる.
Our design also allows for gradually adding more modules to the system without needing to build it all in at the start — in fact, the first version of the system only output communities without any item representations, but this by itself had many useful applications.
実際、最初のバージョンでは、アイテムを表現せずにコミュニティだけを出力していましたが、それだけで多くの有用な用途があった.

# 3. Stage 1: Community Discovery ステージ1：コミュニティ発見

This stage is about discovering communities from the Twitter user– user graph i.e.
この段階は、Twitterのユーザーとユーザーのグラフからコミュニティを発見することである.
the directed graph of Follow relationships between users.
**ユーザ間のフォロー関係を表す有向グラフ**.
Following seminal work in the analysis of directed graphs such as HITS [17] and SALSA [20], we find it convenient to reformulate the directed graph as a bipartite graph.
HITS [17]やSALSA [20]などの有向グラフの解析における代表的な研究に倣って、有向グラフを二部グラフ(bipartite graph)として再定義することが便利であることがわかった.
We now frame our task as one of identifying bipartite communities i.e.
ここで、私たちの課題は、2つのコミュニティ、すなわち、**2分割されたコミュニティを識別すること**である.
communities consisting of members from left as well as right partitions, and where the edge density between the left and right member sets is high.
左パーティションと右パーティションのメンバーからなるコミュニティで、左右のメンバーセット間のエッジ密度が高い場合.
The bipartite reformulation lets us more flexibly assign users to communities — similar to HITS, we decouple the communities a user is influential in from the communities in which a user is interested.
HITSと同様に、ユーザが影響力を持つコミュニティとユーザが関心を持つコミュニティを切り離すことで、より柔軟にユーザをコミュニティへ割り当てることができます。

Problem Definition 1.
問題定義 1.
Given a bipartite user–user graph with left-partition 𝐿 and right-partition 𝑅, find 𝑘 (possibly overlapping) bipartite communities from the graph, and assign each left-node and right-node to the communities with weights to indicate the strength of their memberships.
左パーティション $L$(独立集合?) と右パーティション $R$ (=独立集合?)を持つbipartite user–user graph(=各頂点がユーザを意味するbi-partite graph)が与えられたとき、グラフから $k$個の (おそらく重複する=独立な集合ではないって事?)二分割コミュニティを見つけ、各左ノード(=左の独立集合の各頂点)と右ノード(=右の独立集合の各頂点)にそのメンバーシップの強さを示す重みをつけてコミュニティに割り当てる.

The other advantage of reformulating the directed graph as a bipartite graph is that we can choose to make 𝑅, the right set of nodes, different from 𝐿, the left set of nodes – in particular, since the majority of edges in a typical social network is directed towards a minority of users, it makes sense to pick a smaller 𝑅 than 𝐿.
有向グラフを二部グラフとして再定義するもう一つの利点は、ノードの右集合である$R$をノードの左集合である$L$と異なるように選択できることである. 特に、典型的なソーシャルネットワークの大部分の辺は少数のユーザに向けられている(=多くの一般ユーザがインフルエンサー的なユーザをフォローしている状況??)ので、$L$ よりも小さな $R$ を選ぶことは理にかなっているといる.
In Twitter’s case, we find that we’re able to cover the majority of edges (numbering ∼1011) in the full graph by including the top $∼10^7$ most followed users in 𝑅, while 𝐿 continues to include all users, which is ∼109 .
Twitterの場合、最もフォローされている上位$∼10^7$人のユーザーを $R$ に含めることで、フルグラフの大半のエッジ(約 $10^{11}$ 個)をカバーすることができ、一方、$L$ は全てのユーザを含み続け、約 $10^9$ 個となることがわかった.
Our problem definition also asks to assign non-negative scores to both the left and the right members indicating the strength of association to a community.
また、問題定義では、コミュニティとの関連性の強さを示す非負のスコアを左右(=2つの独立集合R と L?)の各メンバー(=ノード=ユーザ)に割り当てることを求めている.
Therefore, we represent the left and right memberships as sparse, non-negative matrices $U_{|L|\times k}$ and $V_{|R|\times k}$, where 𝑘 is the number of communities.
そこで、左右のメンバーシップ(=2つの独立集合R と L?)を疎な非負行列 $U_{|L|\times k}$ と $V_{|R|\times k}$ で表現する. ここで、$k$ はコミュニティ数である.
Hence, the problem of bipartite community discovery bears close similarities to the problem of sparse non-negative matrix factorization (NMF).
したがって、**2分割コミュニティ発見の問題は、sparse non-negative matrix factorization (NMF)の問題と密接な類似性を持っている**のである.(bi-partite graphとsparse行列分解の関係性がまだわかっていない??)
The biggest challenge with adapting existing approaches such as NMF and their variants [1, 3, 35] is the inability to scale them to graphs with $∼10^9$ nodes and $~10^{11}$ edges – all of our attempts internally to adapt these approaches (see e.g.
NMFやその亜種[1, 3, 35]などの**既存のアプローチを適応する際の最大の課題は、ノード数が約$∼10^9$、エッジ数が約$~10^{11}$のグラフに拡張できないこと**であり、これらのアプローチを適応するための我々の内部での試みはすべて（例えば、以下を参照。
[30]) have only worked at smaller scales and have been very difficult to debug and maintain.
[30]）は、小規模なものでしか機能せず、デバッグやメンテナンスが非常に困難であった.

With SimClusters, we instead adopt the following 3-step approach, illustrated with a toy example in Figure 2.
SimClustersでは、図2におもちゃの例で示すように、次の**3ステップのアプローチ**を採用している.

![](https://camo.qiitausercontent.com/194f3a26deb259e329da2e62437508f49aad755b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f65613534653939372d656632322d366463372d626538302d6239333261626561376433632e706e67)

- Step 1. Similarity Graph of Right Nodes: We calculate the “right projection” of the bipartite graph, i.e., we calculate the similarity between the nodes in the right partition of the bipartite graph based on their incoming edges, and we form a weighted, undirected graph consisting only of the nodes in the right partition. More details in Section 3.1. 1. **右ノードの類似度グラフ**: 二部グラフの“right projection”を計算する. つまり、二部グラフの右分割のノード間の類似度を入力エッジに基づいて計算し、右分割のノードのみからなる加重無向グラフを形成する。 詳細は3.1節で説明する.

- Step 2. Communities of Right Nodes: We discover communities from this similarity graph, using a novel neighborhood-based sampling algorithm that is inspired by the work of [33] but is much more accurate, faster, and scales to graphs with billions of edges. More details in Section 3.2. 2. **右ノードのコミュニティ**: step 1で作った類似グラフからコミュニティを発見する. このアルゴリズムは、[33]の研究に触発されているが、より正確で高速であり、数十億のエッジを持つグラフに拡張可能である. 詳細は3.2節で説明する.

- Step 3. Communities of Left Nodes: We now assign nodes from the left partition to the communities discovered in step 2, and this is described in Section 3.3. 3. **左ノードのコミュニティ** 次に、左のパーティションからノードをステップ2で発見されたコミュニティに割り当てるが、これについては3.3節で説明する.

We note that the broad outlines of this approach have been independently discovered and suggested in the past literature (see e.g.[23, 28]), but it has been largely neglected as an option among similar deployments in industry.
このアプローチの大枠は、過去の文献で独自に発見・提案されてきたものであることに留意されたい(例えば[23,28]). しかし産業界における同様の展開の中では、選択肢としてほとんど無視されてきた.
The primary reason we think this works is that while the original bipartite graph is massive and noisy, the similarity graph of right nodes is much smaller and has clearer community structure.
この方法が有効であると考える主な理由は、元の二部グラフが巨大でノイズが多いのに対し、**右ノードの類似性グラフははるかに小さく、コミュニティ構造が明確であるため**である.
From a scalability point of view, this approach shifts most of the computational burden to the first step of identifying pairs of similar users based on their followers, which is a problem that is largely solved at Twitter (see Section 3.1).
スケーラビリティの観点から、このアプローチは、**計算負荷のほとんどを、フォロワーに基づいて類似したユーザのペアを識別する最初のステップ(step 1)にシフト**し、これはTwitterでほぼ解決されている問題である(セクション3.1参照).
From a matrix-factorization point of view, this 3-step approach closely mirrors one way of performing SVD of a matrix A, via the eigen-decomposition of $A^{T}A$.
行列因数分解の観点から、この3ステップのアプローチは、$A^{T}A$の固有値分解を介した行列$A$のSVDを実行する1つの方法とよく似ている.

Our 3-step approach also isolates the hard-to-parallelize step of community discovery into step 2, where it operates on a smaller graph that fits into the memory of a single machine, while the other two steps operate on much bigger inputs and out of necessity run in batch-distributed settings such as Hadoop MapReduce.
この3ステップのアプローチでは、**並列化が困難なコミュニティ発見のステップをステップ2に分離し、1台のマシンのメモリに収まる小さなグラフで動作させる**一方、他の2ステップははるかに大きな入力で動作し、必然的にHadoop MapReduceなどのバッチ分散設定で動作する. (Hadoop使った事ないからイメージわかないな...)
This approach is also modular and allows for swapping out implementations of each of the above steps independent of the others.
また、このアプローチはモジュール化されており(step毎に??)、上記の各ステップの実装を他のステップから独立して入れ替えることが可能.
A possible concern with our 3-step approach is that it may lead to reduced accuracy compared to directly learning the communities on the input bipartite network – we empirically test this in Supplemental Section A.2 and find this not to be an issue.
この3ステップのアプローチで懸念されるのは、入力された bi-partiteネットワークのコミュニティを直接学習する場合に比べて精度が低下する可能性があるということである. 補足セクションA.2で経験的に検証したところ、これは問題ではないことがわかった.

## 3.1. Step 1: Similarity Graph of Right Nodes ステップ1：右ノードの類似性グラフ

The goal of this step is to construct a much smaller unipartite, undirected graph 𝐺 over the nodes of the right partition.
このステップの目的は、右のパーティション(独立集合$R$)のノードの上に、より小さなuni-partite の無向グラフ $G$ を構築することである.
We define the weight between two users (𝑢, 𝑣) based on the cosine similarity of their followers on the left side of the bipartite graph.
2つのユーザ($u$, $v$)間の重みを、二部グラフの左側(独立集合$L$)のフォロワーのコサイン類似度に基づいて定義する.
To elaborate, if $\vec{x_u}$ and $\vec{x_v}$ represent the binary incidence vectors of 𝑢’s and 𝑣’s followers, their cosine similarity is defined as 𝑥®𝑢 · ®𝑥𝑣/ p ∥ ®𝑥𝑢 ∥ ∥ ®𝑥𝑣 ∥.
詳しく説明すると、$\vec{x_u}$ と $\vec{x_v}$ が ユーザuとvのフォロワーの2値入射ベクトルを表すと、そのcosine類似度は $\vec{x_u} \cdot \vec{x_v} / \sqrt{|\vec{x_u}||\vec{x_v}|}$ と定義する.
With this definition, two users would have non-zero similarity, or an edge in 𝐺 simply by sharing one common neighbor in the bipartite graph.
この定義によれば、2つのユーザは、二部グラフにおいて1つの共通の隣人を共有するだけで、ゼロではない類似度がある. すなわち 類似性グラフ $G$ にエッジ(=ノード間の接続=辺)を持つことになる.
In order to avoid generating an extremely dense similarity graph, we discard the edges with similarity score lower than a certain threshold and additionally keep at most a certain number of neighbors with the largest similarity scores for each user.
極端に密な類似グラフを生成しないために、類似度スコアがある閾値より低いエッジを破棄し、さらに各ユーザの類似度スコアが最も大きい隣人を最大で一定数保持する.

The difficulty is that solving the similar users problem is very challenging at Twitter scale.
難しいのは、**類似ユーザ問題の解決は、Twitterの規模では非常に困難であるということ**である.
But because this is a problem with important applications – e.g. it is the foundation of applying itembased collaborative filtering for the “Who To Follow” module [11] – we have invested significant resources to develop a robust solution.
しかし、これは重要なアプリケーションにおける問題であり、例えば"Who To Follow"モジュール[11]にアイテムベースの協調フィルタリングを適用する際の基礎となる問題であるため、私たちは堅牢なソリューションを開発するために多大な資源を投入してきた.
Our solution, called WHIMP, uses a combination of wedge sampling and Locality Sensitive Hashing (LSH) to scale to the Twitter graph and lends itself to implementation on Hadoop MapReduce [32].
WHIMPと呼ばれる我々のソリューションは、ウェッジサンプリングとLocality Sensitive Hashing（LSH）の組み合わせでTwitterグラフに対応し、Hadoop MapReduce（32）上での実装に適している.
WHIMP is able to identify similar users for users with either large or small followings, and has been vetted in a variety of ways internally.
**WHIMPは、フォロワーが多いユーザも少ないユーザも、類似性の高いユーザを特定することができ**、社内でさまざまな検証が行われているらしい.

Ultimately, this similarity graph step takes as input a directed/bipartite graph with ∼109 nodes and ∼1011 edges and outputs an undirected graph with $∼10^7$ nodes and ∼109 edges.
最終的に、この類似グラフステップは、$~10^9$ 個のノードと$∼10^{11}$個のエッジを持つ有向/二部グラフを入力とし、$~10^7$ 個のノードと $~10^9$ 個のエッジを持つ無向グラフを出力する.
In other words, we go from shared-nothing cluster-computing scale to shared-memory multi-core scale.
つまり、shared-nothing のクラスタコンピューティング規模から、shared-memory のマルチコア規模になるのだ.(??)
The transformation wrought by this step is also reminiscent of prior research which suggested that keeping only the most important edges in a graph can benefit community discovery methods [29].
このステップによってもたらされる変換は、グラフの最も重要なエッジのみを保持することでコミュニティ発見手法に利益をもたらすことを示唆した先行研究[29]をも想起させる.

## 3.2. Step 2: Communities of Right Nodes ステップ2：右ノードの共同体

In this step, we wish to discover communities of densely connected nodes from the undirected, possibly-weighted similarity graph from the previous step.
このステップでは、前のステップで得られた無向の(おそらくは重み付けされた)類似性グラフから、密に接続されたノード集合(=ユーザ集合)のコミュニティを発見することを目的としている.
In order to accurately preserve the structure of the input similarity graph, we have observed that it is important for the communities to have hundreds of nodes, rather than thousands or tens or thousands.
入力された類似性グラフの構造を正確に保持するためには、**ある1コミュニティ当たりのノード数($k$)が数千、数万ではなく、数百であることが重要**であることが確認されている.
This means that we need algorithms that can process input graphs with $∼10^7$ nodes and $∼10^9$ edges to find $∼10^5$ communities.
つまり、ノード$∼10^7$個、エッジ$∼10^9$個の入力グラフを処理して、$∼10^5$ 個(数百だったら、$~10^3$ではない?)のコミュニティを見つけることができるアルゴリズムが必要.
Despite the long history of community discovery algorithms, we were unable to find any existing solution that can satisfy these scale requirements.
コミュニティ発見アルゴリズムの長い歴史にもかかわらず、これらの規模要件を満たすことができる既存のソリューションを見つけることができなかった.
We next describe the algorithm we developed, called Neighborhood-aware Metropolis Hastings (henceforth Neighborhood-aware MH), to meet our requirements.
次に、我々の要求を満たすために開発した **Neighborhood-aware Metropolis Hastings(以下、Neighborhood-aware MH)**と呼ばれるアルゴリズムについて説明する.

Our algorithm extends a Metropolis-Hastings sampling approach presented in [33] for discovering overlapping communities, which we first describe as background.
我々のアルゴリズムは、**重複するコミュニティを発見するために[33]で発表されたメトロポリス・ヘイスティングス・サンプリング・アプローチ**を拡張したものであり、まず背景として説明する.
Let $Z_{|R|\times k}$ be a sparse binary community assignments matrix and Z(𝑢) denote the set of communities to which the vertex 𝑢 has been assigned (in other words, Z(𝑢) gives the non-zero column indices from the 𝑢-th row in Z).
$Z_{|R|\times k}$ を疎なbinaryのコミュニティ割り当て行列とし、 $Z(u)$ は頂点$u$が割り当てられたコミュニティの集合を表す(言い換えれば、$Z(u)$ は、行列 $Z$ の $u$ 行目から非ゼロの列indicesを出力するfunctionみたいな感じ?)、と仮定する.
Equation 1 specifies an objective function over Z.
式1は、Zに対する目的関数を指定する.(Zが推定すべきパラメータなのか...!)

$$
F(Z) = \alpha \sum_{u, v \in E}  1(|Z(u) \cap Z(v)| > 0)
+ \sum_{u, v \notin E}  1(|Z(u) \cap Z(v)| = 0)
\tag{1}
$$

1 is the indicator function.
1 はindicator function である.
F (Z) is the sum of two terms – the first counts how many neighboring pairs of nodes in the graph share at least one community, while the second counts how many nonneighbor pairs of nodes in the graph do not share a community.2 Since most real, large-scale networks are very sparse, it is useful to upweight the contribution of the first term using the parameter 𝛼 – increasing values of 𝛼 means that the objective function is better optimized by Z with more non-zeros.
$F(Z)$は2つの項の合計である. 最初の項は、グラフ内のノードの隣接するペアが少なくとも1つのコミュニティを共有する数をカウントし、2番目の項は、グラフ内のノードの非隣接ペアがコミュニティを共有しない数をカウントする. **実際の大規模ネットワークのほとんどは非常にスパースなので、パラメータ𝛼を用いて最初の項の寄与を重み付けすることが有用である**. 𝛼の値が増加すると、目的関数はより非ゼロのZによって最適化することになる.
Note also that the objective function above is decomposable, in the sense that the overall objective function $F(Z)$ can be expressed as a sum of a function $f(u, Z)$ over individual vertices (below, $N(u)$ denotes the set of neighbors of vertex $u$).
また、上記の目的関数は、**全体の目的関数$F(Z)$が個々の頂点に対する関数 $f(u, Z)$ の和として表現できる**意味で、分解可能であることに注意すること. (ここで、$N(u)$ はある頂点 $u$ の近傍集合を表す.)

$$
f(u, Z) = \alpha \sum_{v \in N(u)} 1(|Z(u) \cap Z(v)| > 0)
+ \sum_{v \notin N(u)} 1(|Z(u) \cap Z(v)| = 0)
\tag{2}
$$

Using the above background, we first describe the approach for discovering overlapping communities in a general way in Algorithm 1.
以上の背景を踏まえ、まずアルゴリズム1において、重複するコミュニティを一般的な方法で発見するアプローチを説明する.
After initializing Z, we run at most 𝑇 epochs of optimization, where in each epoch we iterate over all the vertices in the graph in a shuffled order.
$Z$ を初期化した後、最大で $T$ epoch数回 最適化を実行し、各エポックではグラフ内のすべての頂点をシャッフルした順序(?)で反復する.
For each vertex 𝑢 we sample a new set of community assignments Z ′ (𝑢) using the proposal function, and calculate the difference in objective function between the newly proposed Z ′ (𝑢) and the current set of community assignments Z(𝑢).
各頂点 $u$ について、proposal function(=コードの関数)を用いてコミュニティ割り当ての新しい集合 $Z'(u)$ をサンプリングし、新しく提案された$Z'(u)$ と現在のコミュニティ割り当てのセット $Z(u)$ の間の目的関数の違いを計算する.
If $Z'(u)$ is better, then it is accepted; if not, it may still be accepted with a certain probability, indicated in line 6 of Algorithm 1.
もし $Z'(u)$ の方が良ければ、それは受け入れられる. もしそうでなくても、アルゴリズム1の6行目で示されるように、ある確率で受け入れられるかもしれない.
As noted in [33], one reason for preferring a randomized optimization procedure as opposed a deterministic optimization procedure is to avoid getting stuck in local minima.
[33]で述べられているように，決定論的な最適化手順ではなく，ランダムな最適化手順を好む理由の1つは，局所最小値にはまるのを避けることである.

The specific choices for the ‘Initialize’ and ‘Proposal’ functions made in [33] are described in Algorithm 2.
[33]で行われた`Initialize` function と`Proposal` function の具体的な選択方法は、アルゴリズム2に記載されている.
Because these functions are implemented using purely random sampling, we refer to this approach as ‘Random MH’.
これらの機能は、純粋にランダムなサンプリングで実装されているため、この手法を"**ランダムMH(Metropolis-Hastings)**"と呼んでいる.
The main practical drawback of Random MH is that it is extremely slow to obtain a satisfactorily accurate solution for even moderate values of $k$.
ランダムMHの主な実用上の欠点は、$k$ の値が適度であっても、満足のいく精度の解を得るのに非常に時間がかかるということである.(最適化戦略無しに、ランダムに、より良いパラメータを探索しているから...!)
This is not surprising considering that in each step, the proposal function generates a completely random community assignments vector and evaluates it w.r.t. the current vector; as 𝑘 increases, the space of community assignments increases exponentially which makes it very unlikely that the proposal will be able to generate an acceptable transition.
これは、`Proposal` function が各ステップで完全にランダムなコミュニティ割り当てベクトルを生成し、現在の割り当てベクトルと照らし合わせて評価することを考えれば、驚くべきことではない. $k$ が増加すると、コミュニティ割り当ての空間(=パラメータの選択肢のイメージ)は指数関数的に増加し、`Proposal` function が許容できるtransition (パラメータ更新)を生成できる可能性は非常に低くなる.

Instead, we propose Neighborhood-aware MH, specified in Algorithm 3.
その代わりに、アルゴリズム3で規定される **Neighborhood-aware MH(Metropolis-Hastings)** を提案する.
The proposal function in Neighborhood-aware MH is based on two insights or assumptions – the first is that it is extremely unlikely that a node should belong to a community that none of its neighbors currently belongs to; the second is that for most practical applications, it is unnecessary to assign a node to more than a small number of communities.
Neighborhood-aware MH(Metropolis-Hastings) の proposal functionは、以下の2つの洞察 & 仮定に基づいている: 1つ目は、あるノード(=頂点=ユーザ)が、その隣接するノードが現在所属していないコミュニティに所属する可能性は極めて低いということ. 2つ目は、**ほとんどの実用的なアプリケーションでは、ノードを少数のコミュニティ以上に所属させる必要はない(?)**ということである.
We design a two-step proposal function that works as follows.
次のような2段階のproposal function を設計している.
In the first step, for a given node 𝑢 we iterate over all the neighbors of 𝑢, look up their community assignments in Z, and identify the set of communities which are represented at least once, call it 𝑆.
最初のステップでは、与えられたノード $u$ について、$u$ のすべての近傍を繰り返し、$Z$で彼らのコミュニティ割り当てを検索し、**少なくとも一度は表されるコミュニティの集合**を識別し、それを$S$と呼ぶ.(まだ良く理解できてない.)
In the second step, we iterate over all subsets of size ≤ 𝑙 of 𝑆 from the first step, where 𝑙 is a user-provided upper bound on how many communities a node can be assigned to.
第2ステップでは、第1ステップで得られた $S$ のサイズ $\leq l$ のすべての部分集合について反復処理を行う. ここで、$l$ はノードが割り当てられるコミュニティの数に対するuser-provided(=要するに開発者が指定するハイパーパラメータの意味!)の上限値である.
For each subset 𝑠, we calculate the function $f(u, s)$ from Eqn 2, and finally sample the subset 𝑠 with probability proportional to $e^{f(u,s)}$ i.e. we apply the softmax.
各サブセット $s$ について、式2より関数 $f(u, s)$を計算し、最後に $e^{f(u,s)}$ に比例する確率でサブセット $s$ をサンプルする. (i.e. ソフトマックスを適用する)
The result of the sampling is then either accepted or rejected, as specified in lines 6 and 7 of Algorithm 1.
そして、アルゴリズム1の6行目と7行目に規定されているように、サンプリングの結果が受け入れられるか、拒否されるかのどちらかになる.
As for initializing Z, we seed each community with the neighborhood for a randomly selected node in the graph.
$Z$の初期化については、各コミュニティにグラフ内のランダムに選ばれたノードのneigbborhoodをシードする.(?)

We discuss a few important implementation details.
いくつかの重要な実装の詳細について説明する.

- Most of the complexity comes from evaluating the function 𝑓 (𝑢, 𝑠), which requires calculating the intersection between a node’s neighbors and the union of the communities in 𝑠. For many members of 𝑆 (the set computed in line 8 Algorithm 3), we can incrementally compute the summary statistics required for $f(u, s)$ as we go through a node’s neighborhood when executing line 8 of Algorithm 3, so that the subsequent inner loop in line 10 can execute much faster. Similarly, the acceptance probability for line 6 of Algorithm 1 can also reuse the 𝑓 (𝑢, Z) computed during the proposal process. 複雑さのほとんどは、関数 $f(u)$ の評価によるもので、ノードの近傍と $s$ のコミュニティの結合の間の交差を計算する必要がある. $S$ (アルゴリズム3の8行目で計算された集合)の多くのメンバーについては、アルゴリズム3の8行目を実行する際に、ノードの近傍を通過する際に $f(u, s)$ に必要な要約統計量を段階的に計算できるため、続く10行目の内部ループの実行速度が大幅に向上する. 同様に、アルゴリズム1の6行目の受け入れ確率も、`proposal`プロセスで計算された $f(u, Z)$を再利用できる.

- Sampling from a softmax distribution can be accomplished efficiently in a single pass using the Gumbel-Max trick. ソフトマックス分布(=これって、pを使ってZを更新するか判定する処理の事?=実際はbinaryのベルヌーイ分布では?)からのサンプリングは、Gumbel-Max trick(?)を使うことで1回のパスで効率的に行うことができる.

- In the important special case where we assign each node to at most one community only, each epoch of Neighborhood-aware MH can execute in 𝑂(|𝐸|) time, using both of the above mentioned tricks. 各ノードを最大1つのコミュニティのみに割り当てる重要な特殊ケースでは、上述の両方のトリックを使用することで、Neighborhood-aware MHの各エポックは $O(|E|)$ 時間で実行できる.($E$ってなんだっけ?)

- The algorithm lends itself well to parallelization. Specifically the for loop in line 4 of Algorithm 1 can be distributed among several threads which share access to Z, the rows of which can optionally be synchronized using read-write locks. In practice, we have found that removing synchronization has no effect on the accuracy and gives a slight boost in speed (similar to [24]). **このアルゴリズムは、並列化に適している**. 具体的には、アルゴリズム1の4行目のforループを、Zへのアクセスを共有する複数のスレッドに分散させることができ、その行はオプションで読み書きロックを使って同期させることができる. 実際には、同期を削除しても精度に影響はなく、速度がわずかに向上することが分かっている([24]と同様)

## 3.3. Step 3: Communities of Left Nodes

The output of the previous step is the matrix $V_{|R|×k}$ in which the $i$-th row specifies the communities to which the right-node $i$ has been assigned.
前のステップの出力は、$i$ 番目の行が右ノード$i$が割り当てられたコミュニティを指定する行列 $V_{|R| \times k}$ である.
The remaining problem that needs to be solved is coming up with the matrix $U_{|L| \times k}$ such that the $i$-th row specifies the communities to which the left-node $i$ has been assigned.
残りの問題は、i番目の行が左ノードiが割り当てられたコミュニティを指定するような行列 $U_{|L| \times k}$ を考え出すことである.
A simple way to do this assignment is to assign a left-node to communities by looking at the communities that its neighbors (which will all be right-nodes, and hence already have assignments) have been assigned to.
この割り当てを行う簡単な方法は、左ノードのneighbors(すべて右ノードであるため、すでに割り当てを受けている)が割り当てられているコミュニティを見ることによって、左ノードをコミュニティに割り当てることである.
More formally, if $A_{|L| \times |R|}$ is the adjacency matrix of the input bipartite graph, then we set $U = truncate(A\cdot V)$, where the $truncate()$ function keeps only up to a certain number of nonzeros per row to save on storage.
より正式には、$A_{|L| \times |R|}$ を**入力二部グラフの隣接行列(adjacency matrix)**(二部グラフの入力も行列で表せば良いのか...!)とすると、$U = truncate(A\cdot V)$ とする、 ここで、$truncate()$ 関数は、ストレージを節約するために、行(=左の独立集合の各頂点)ごとにある一定の数までのノンゼロだけを保持する.
This equation for calculating U is motivated by the fact that in the special case when V is an orthonormal matrix, i.e.
この$U$の計算式は、$V$が正方直交行列である場合の特殊なケース、すなわち、次の事実に動機づけられている.
$V^T V = I$, then $U = A \cdot V$ is the solution to $A = U \cdot V^T$.
$V^T V = I$であれば、$U = A \cdot V$ は $A = U \cdot V^T$ の解になる.
We have experimented with situations both where V is orthonormal (this can be achieved by assigning each right-node to at most one community) as well as situations where V is not, and have found that in each case the resulting U provides accurate representations for the left-nodes.
$V$が直交する場合(これは、**各右ノードを最大1つのコミュニティに割り当てることで実現できる**)(=あ、じゃあ運用する上では基本的に、$V$ は正方直交行列になるのか...!)と、そうでない場合の両方で実験を行い、いずれの場合も、結果として得られる$U$が左nodesを正確に表現することを発見した.(あ、結局$V$がorthonormal matrixではなくても問題なさそうなのか...!)
We refer to U as User Interest Representations, and it forms the main input for subsequent steps.
**$U$ を User Interest Representations** と呼び、以降のステップの主要なインプットを形成する.(=UがSimClustersの段階2の入力情報になる...? $V$はならない?)
The computation in this step can be scaled to our requirements easily by implementing in a batch-distributed computing paradigm such as Hadoop MapReduce.
このステップの計算は、Hadoop MapReduce のようなバッチ分散コンピューティングパラダイムで実装することで、我々の要求に合わせて**簡単にスケーリングすることができる**.

# 4. Stage 2: Item Representations Stage 2: アイテム表現

In this section, we describe how to compute representations for different items, such as Tweets, Hashtags, or users - which can be the targets for different recommendation problems.
本節では、**ツイート、ハッシュタグ、ユーザなど、様々な推薦問題の対象となりうるアイテムに対する表現(=embedding)を計算する方法**について説明する.
Along with the user interest representations U from Stage 1, this stage also relies on a user–item bipartite graph that is formed from historical or on-going user engagements with those items on the platform.
ステージ1の user interest representations U とともに、このステージは、プラットフォーム上のアイテムに対する歴史的または継続的なユーザの関与から形成される**ユーザ-アイテム二部グラフ**にも依拠する.

Our general framework is to compute an item’s representation by aggregating the representations of all the users who engaged with it, i.e., the representation for item 𝑗 is
私たちの**一般的な枠組みは、アイテムに関わったすべてのユーザの表現を集約してアイテムの表現を計算すること**(なるほど...!シンプル!). つまり、アイテム $j$ の表現は、

$$
W(j) = aggregate({U(u), \forall u \in N(j)})
\tag{3}
$$

where $N(j)$ denotes all the users who engaged with item 𝑗 in the corresponding user–item bipartite graph, and $W(j)$ and $U(u)$ are both vectors.
ここで、$N(j)$は、対応するユーザ-アイテム二部グラフにおいてアイテム$j$に関与したすべてのユーザを示し、$W(j)$ と $U(u)$ はいずれもベクトルとする.
The $𝑎𝑔𝑔𝑟𝑒𝑔𝑎𝑡𝑒$ function can be chosen based on different applications, and can also be learned from a specific supervised task [13].
$aggregate$関数は、さまざまなアプリケーションに基づいて選択することができ、特定の教師付きタスクから学習することも可能[13].
In our case, we opt for a relatively simple, interpretable 𝑎𝑔𝑔𝑟𝑒𝑔𝑎𝑡𝑒 function with the goal that W(𝑗, 𝑐) can be interpreted as the level of interest an average user of the community 𝑐 currently has in this item 𝑗.
この場合、$W(j,c)$ を**コミュニティ$c$の平均的なユーザがこのアイテム$j$に現在抱いている興味のレベル**と解釈できるように、比較的単純で解釈しやすい$aggregate$関数を選択することになる.
We choose to use “exponentially time-decayed average” as our 𝑎𝑔𝑔𝑟𝑒𝑔𝑎𝑡𝑒 function, which exponentially decays the contribution of a user who interacted with the item based on how long ago that user engaged with the item.
私たちは、**aggregate関数として"exponentially time-decayed average(指数関数的時間減衰平均)"を選択**した. これは、アイテムに関わったユーザの貢献度を、そのユーザがアイテムに関わった時間に基づいて指数関数的に減衰させる.
The half-life used for the exponential decay is item-dependent – where the shelf-life of those items is longer (such as Topics), we set longer half-lives, while for shorter shelf life items such as Tweets, we set shorter half-lives.
**指数関数的減衰に使用する半減期はアイテムに依存**し、賞味期限(shelf-lifeって表現されるんだ...!)が長いもの(トピックスなど)には長い半減期を設定し、賞味期限が短いもの(ツイートなど)には短い半減期を設定している.

The resulting matrix W is much denser than U and it is not useful to save all its non-zero values at scale.
結果として得られる行列WはUよりもはるかに密度が高く(=>$U$の要素はbinary?で離散的だけど、$W$の場合は連続的な数値だから?)、その非ゼロ値をすべてスケールで保存することは有益ではない.
Instead, we maintain two additional views or indexes of W, each of which keeps a top-k view.
その代わりに、$W$のビューまたはインデックスを2つ追加し、それぞれがトップ$k$ビューを保持する. (値が大きい要素のみを記録する、みたいな?)
The first view is R and R (𝑗) tracks the top communities for the item 𝑗.
ファーストビューは$R$で、$R(j)$は**アイテム$j$のトップコミュニティを追跡する**.
The second view is C and C (𝑐) tracks the top items for the community $c$.
第二のビューは$C$で、$C(c)$ は**コミュニティ$c$のトップアイテムを追跡する**.
In the case of items with a long shelf life, the calculation of W, R, and C is straightforwardly done in a batch setting using e.g. Hadoop MapReduce.
賞味期限が長いものの場合、W、R、Cの計算は、例えば、Hadoop MapReduceを使ってバッチ式で行うのが素直である.

However, handling items with short shelf life is more interesting.
しかし、賞味期限が短いものを扱うとなると、もっと面白い.
In this case, we realize a major advantage of an exponentially time-decayed average (as opposed to e.g. time-windowed average), which is that it lends itself to easy incremental updates for W.
この場合、指数関数的に時間的に減衰する平均の大きな利点(例えば時間窓付き平均とは異なる)が実現され、それは$W$のインクリメンタルな更新を容易にすることにつながる.
Specifically, we just need to keep two summary statistics for each cell in W - the current average itself and the last timestamp when it was updated.
具体的には、Wの各セルについて、現在の平均値そのものと、それが更新された最後のタイムスタンプという2つの要約統計量を保持すればよい.
As detailed in Algorithm 4 lines 4–7, when a new user–item engagement arrives, we are able to update W for the item by calculating a decay factor based on the time elapsed since the last update.
アルゴリズム4の4行目から7行目に詳述するように、**新しいユーザとアイテムのエンゲージメントが到着すると、前回の更新からの経過時間に基づいて減衰係数を計算することで、アイテムのWを更新することができる**.(online更新ができるのはいいね...!)
In order to exactly track the row-wise and columnwise top-k views on W, it is necessary that we track the entirety of W - if it turns out that W is too big to be tracked in its entirety, then one can use sketches to keep a summary of W at the cost of introducing errors [4, 15], although we have found this unnecessary.
もしWが大きすぎて全体を追跡できないことが判明した場合、エラーを導入する代償として、スケッチを使ってWの要約を保持することができる[4, 15]が、我々はこの必要がないと判断している.
Another way of reducing the size of W is to reduce 𝑘 i.e. the dimensionality of the representations computed in Stage 1, or by further sparsifying the input user representations U.
Wのサイズを小さくする別の方法は、$k$ すなわちステージ1で計算された表現の次元(=想定するcommunityの数??)を小さくすること、または入力されたユーザ表現$U$をさらにスパース化することである.
Calculating streaming item representations in this manner can be implemented using frameworks such as Apache Storm/Heron/Spark/Flink.
このようなストリーミングアイテム表現の計算は、Apache Storm/Heron/Spark/Flinkなどのフレームワークを用いて実装することが可能.

The two top-k views R and C are stored in low-latency key-value stores.
2つのtop-kビュー $R$ と $C$ は、低遅延のkey-valueストアに保存される.
Using these two indices, it easy to retrieve nearest neighbors for any user or item – we simply look up the top communities that a user or item is active in, and for each of those communities, identify the top users or items.
この2つの指標を用いると、**任意のユーザやアイテムの最近接者を簡単に検索することができる.** ユーザやアイテムと関連度の高い(=興味が近い=active inな) 上位のコミュニティを調べ、そのコミュニティごとに上位のユーザやアイテムを特定するだけでよいのである.
These candidates can then be ranked by fetching their full representations and computing the similarity with the representation of the query object (either user or item).
これらの候補は、その完全な表現(=embeddingベクトル)を取得し、queryオブジェクト(ユーザまたはアイテムのいずれか)の表現(=embeddingベクトル)との**類似性を計算することによってランク付け**することができる.
The upshot is that we neither need to brute-force scan through all users/items nor need to build specialized nearest neighbor indices.
その結果、すべてのユーザやアイテムを総当たりでスキャンする必要も、特別な最近傍インデックスを構築する必要もない.

# 5. Deployment Details 配置の詳細

SimClusters has been deployed in production at Twitter for more than an year so far.
SimClustersは、Twitter社で1年以上前から本番環境に導入されている.
All the representations output by the SimClusters system are also keyed by model-version, so that we can operate multiple models in parallel to enable the trying out of new parameters or code changes without affecting existing production.
SimClustersシステムから出力されるすべての表現は、**モデルバージョンでキーが設定されており、複数のモデルを並行して運用すること**で、既存の生産に影響を与えずに新しいパラメータやコードの変更を試すことができる.
The main model that is currently running in production has $∼10^5$ communities in the representations, discovered from the similarity graph of the top $∼10^7$ users by follower count.
現在、本番稼働中のメインモデルでは、フォロワー数上位$∼10^7$人のユーザのsimilarityグラフから発見された$∼10^5$のコミュニティが表現されている.
The bipartite communities discovered by the model contain nearly 70% of the edges in the input bipartite graph, suggesting that most of the structure of the graph is captured.
モデルによって発見されたbipartiteコミュニティは、入力されたbipartiteグラフのエッジの70%近くを含んでおり、グラフの構造のほとんどを捉えていることが示唆される.
The right member sets do not vary too much in their sizes, while the left member sets vary drastically, reflecting the variance in the original follower distribution.
右のメンバーセットの大きさはあまり変わらないが、左のメンバーセットの大きさは大きく異なり、元のフォロワー分布のばらつきを反映している.
Within Stage 1, Step 1 (similarity calculation) is the most expensive step, taking about 2 days to run end-to-end on Hadoop MapReduce, but note that this job was in production before SimClusters and therefore is not an additional cost introduced by SimClusters.
ステージ1のうち、**ステップ1(類似度計算)は最もコストがかかるステップで、Hadoop MapReduceでエンドツーエンドで実行するのに約2日かかる**が、このジョブはSimClusters以前から運用されていたため、SimClustersによる追加コストではないことに注意してください. (高い頻度でバッチ実行するような感じではないのかな...。一ヶ月に一度とか? まあこのステップで使用するユーザデータは上位ユーザのみだからすでにデータは十分揃っていて、短期間で傾向がかわる事はないだろうから問題なさそう...!)
Step 2 was run from scratch for the very first time when SimClusters launched; subsequently, we update the V matrix to take into account changes to the user–user similarity graph by running an abbreviated version of Neighborhood-aware MH initialized with the current V.
ステップ2はSimClustersの起動時に初めて実行された. その後、現在の$V$で初期化した Neighborhood-aware MHの短縮版を実行することにより、ユーザとユーザの類似性グラフの変化を考慮し、$V$行列を更新している.
Step 3 is also periodically run as batch application on Hadoop MapReduce using the latest version of the user–user graph and the latest V from Step 2.
また、**Step3は、最新版のユーザ-ユーザグラフとStep2の最新$V$を使い、Hadoop MapReduce上でバッチアプリケーションとして定期的に実行される**.
Once we have the output from Step 3 (the U matrix), we do not directly use the V matrix anymore, which is typically too sparse for accurate modeling.
ステップ3の出力($U$行列)(=一般ユーザのcommunity表現ベクトル)を得た後は、$V$行列(=上位ユーザのcommunity表現ベクトル)を直接使用することはありません。V行列は一般的に疎すぎて正確なモデリングができない.

For Stage 2, we currently have four jobs – two batch jobs, one for “user influence” representations and one for Topic representations; and two streaming jobs, one for Tweet representations and one for Trend representations.
Stage2では、"user influence"表現(=これだけどういうアイテムか分からない...)と"Topic"表現の**2つのバッチジョブ**と、"ツイート"表現と"トレンド"表現(=これも単に人気度が高いトレンドを全員に見せている訳でなく、各communityと親和性の高いトレンドを探してるのか...!)の**2つのストリーミングジョブ(=online更新的なジョブ.)**の計4つのジョブを現在用意している.
The purpose of the user influence representations is to tell us what communities a user is influential in, as opposed to the user interest representations (the output of Stage 1) which tell us what communities a user is interested in, The user influence representations are better than the original V matrix for this purpose as they cover many more users and are also denser for the original subset of users.
**user influence表現の目的**は、ユーザがどのようなコミュニティに興味を持っているかを表す為のuser interest表現(=ステージ1の出力)とは対照的に、**ユーザがどのようなコミュニティに影響を受けているか**を表すことである. user influence表現は、より多くのユーザをカバーし、またユーザの元のサブセットに対してより密であるため、この目的のために元の$V$行列(=これって上位ユーザのcommunity表現じゃなかったっけ?)よりも優れている.(計算方法は、ステージ2の他のアイテムと同じなのかな...="上位ユーザ"をアイテムとして計算する感じ?)
Topic representations tell us which communities are the most interested in a Topic, and the input to computing these is both the user interest representations as well as a user–Topic engagement graph.
トピック表現は、どのコミュニティがトピックに最も興味を持っているかを示すもので、これを計算するための入力は、ユーザの興味表現と、ユーザ-トピックの関係グラフの両方である.(アイテム=トピックとしたver.)
Tweet and Trend representations are computed and updated in a streaming job which takes as input user–Tweet engagements happening in real-time.
ツイートとトレンドの表現は、リアルタイムで発生するユーザとツイートのエンゲージメントを入力とするストリーミングジョブで計算・更新される.
Both the user interest and user influence representations are protected using authentication to only allow authorized access, and users are provided the chance to opt out of unwanted inferences in their Privacy dashboard.
user interest表現とuser influence表現は、認証により許可されたアクセスのみを許可するよう保護されており、ユーザはプライバシーダッシュボードで不要な推論をオプトアウトする機会を得ることができる.

Note that we store only the non-zeros in all our representations, and in all cases we truncate entries close to zero.
すべての表現において、ゼロでないものだけを保存し、すべての場合においてゼロに近いエントリーを切り捨てていることに注意してください.
The user interest representations cover $∼10^9$ users while the user influence representations cover $∼10^8$ users, with both representations having on average 10−100 non-zeros.
user interest表現は約$∼10^9$人のユーザをカバーし、user influence表現は約$∼10^8$人のユーザをカバーしており、どちらの表現も平均10~100個の非ゼロ要素を有している.(user influence表現の方がオーダーが小さいのは、user interest表現を元にaggregate計算する際に、ある一定数以上フォローされている必要があるから?)
There are fewer recommendable Tweets and Trends at any given point in time (refer Table 1), but their representations are denser, having on average ∼102 non-zeros.
ある時点で推薦されるツイートやトレンドの数は少ないが(表1参照)、その表現はより密で、平均して約102のノンゼロを持つ.
Note that for the following four representations - user influence, Topic, Tweet, and Trend - we also maintain the inverted indices, i.e. given a community, what are the top-k users/Topics/Tweets/Trends for that community (denoted by C in Section 4).
なお、以下の4つの表現(user influence、トピック、ツイート、トレンド)については、反転した指標も維持している: あるコミュニティが与えられたとき、そのコミュニティと関連度の高いトップkユーザー/トピック/ツイート/トレンドは何か（セクション4では$C$と表記している）.
Having C is essential to retrieving the items whose representation has the largest dot product or cosine similarity with another representation.
$C$は、他の表現とのドット積やコサイン類似度が最も大きい表現を持つアイテムを検索するために不可欠である.

# 6. Applications 適用

## 6.1. Similar Tweets on Tweet Details page ツイート詳細ページでの類似ツイート

For users who visit a Tweet via an email or a push notification, Twitter shows a module with other recommended Tweets, alongside replies.
メールやプッシュ通知でツイートにアクセスしたユーザに対して、Twitterは他のおすすめツイートと返信を並べたモジュールを表示する.
Prior to SimClusters, this module retrieved Tweets solely based on author similarity i.e.Tweets written by users who share a lot of followers with the author of the main Tweet on the page.
このモジュールは、SimClustersの前に、作者の類似性(ページ上のメインツイートの作者と多くのフォロワーを共有するユーザーが書いたツイート)にのみ基づいてツイートを検索していた.
We ran an online A/B test where we added similar Tweets from SimClusters i.e. we retrieved Tweets whose SimClusters representation has high cosine similarity with the representation of the main Tweet on the page.
オンラインA/Bテストでは、SimClustersから類似ツイートを追加した. つまり、SimClustersの表現(=どのcommunityと関連度が高いかを表すベクトル)がページ上のメインツイートの表現と高いコサイン類似度を持つツイートを取得した.

We found that the engagement rate on the resulting Tweets was 25% higher.4
その結果、ツイートに対するエンゲージメント率が25％高くなることがわかった.

Subsequently, we added a second candidate source for this product based on SimClusters – retrieve Tweets whose SimClusters representation have high cosine similarity with the user influence representation of the author of the main Tweet on the page.
その後、SimClustersに基づくこのproductの第二のソース候補を追加した.SimClusters表現が、ページ上のメインツイートの著者のuser influence表現(=user interest 表現からaggregateされたベクトル)と高いコサイン類似性を持つツイートを検索する.
Adding this source increases the coverage further, while the overall increase in engagement rate is a more modest but still impressive 7%.
このソースを追加することで、カバー率はさらに向上し、全体のエンゲージメント率の向上は、より控えめではありますが、それでも7％という素晴らしい結果となっている.

## 6.2. Tweet Recommendations in Home Page ホームページでおすすめツイート

A user’s Home feed on Twitter consists of both Tweets from users being directly followed as well as recommended Tweets from users not being followed (“Out of Network Tweets”).
**Twitterのホームフィード**は、直接フォローされているユーザのツイートと、フォローされていないユーザのおすすめツイート（以下「ネットワーク外ツイート」）の両方から構成される.
Prior to SimClusters, the main algorithm for recommended Tweets was what is called “Network Activity” - namely, use GraphJet [31] to identify which Tweets are being liked by the viewing user’s followings (i.e. network).
SimClusters以前は、推薦ツイートの主なアルゴリズムは「ネットワークアクティビティ」と呼ばれるものだった. つまり、GraphJet [31]を使用して、閲覧ユーザのフォロー（つまりネットワーク）がどのツイートに「いいね」を付けているかを特定する.

Using SimClusters Tweet representations, we built two candidate sources to supplement Network Activity Tweets.
**SimClustersのツイート表現(ツイートがどのcommunityと関連度が高いか?を表すベクトル)**を使って、ネットワークアクティビティツイートを補足する2つのcandidate sources を構築した.
The first candidate source identifies Tweets whose real-time representation has the highest dot-product with the viewing user’s interest representation.
第1のcandidate sources は、リアルタイム表現(=現時点でのツイートのcommunity表現)が閲覧ユーザのinterest表現とのドット積が最も高いツイートを特定する.
The second candidate source is based on item-based collaborative filtering, and uses the same underlying implementation as the “Similar Tweets” application described in Section 6.1 to identify Tweets similar to those Tweets which have been recently liked by the user.
2つ目の候補は、アイテムベースの協調フィルタリングに基づくもので、セクション6.1で説明した「類似ツイート」アプリケーションと同じ基本的な実装を使用して、ユーザが最近「いいね！」を押したツイートと類似するツイートを特定する. (類似度の評価に使用するのは simclustersで作ったtweet表現.=>関連するコミュニティに基づく類似度!)
We ran an online A/B test by replacing existing candidates in production (in certain positions on Home) using the candidates from these two new candidate sources.
この2つの新しい候補者ソースからの候補者を、本番の既存の候補者(Homeの特定のポジション)に置き換えて、オンラインでA/Bテストを実施した.
The experiment showed that the engagement rate of the new candidates is 33% higher than that for candidates generated by Network Activity, and shown in similar positions.
実験では、ネットワークアクティビティで生成された候補者と比較して、新しい候補者のエンゲージメント率が33%高く、同じようなポジションで表示されることがわかった.
The two candidate sources together were able to increase total weighted engagements on the platform by close to 1%, which is very large considering the maturity of this product and that recommended Tweets only account for a minority of the viewed content in Home pages.
これは、本製品の成熟度や、おすすめツイートがトップページの閲覧コンテンツの少数派であることを考えると、非常に大きな効果である.

Apart from new candidates, we also use the user interest and Tweet representations to improve the ranking of candidates coming from all sources.
新しい候補とは別に、user interest表現やツイート表現を利用して、あらゆるソースから来る候補のランキングを改善することもある.(=>候補生成後のランキングモデルの特徴量として使用するみたいな感じ?)
The user and item representations are used to enrich the set of existing user features, item features, as well as user-item interaction features in the input to an engagement prediction model.
ユーザとアイテムの表現は、エンゲージメント予測モデルの入力において、既存のユーザ特徴、アイテム特徴、およびユーザとアイテムの相互作用特徴のセットを豊かにするために使用される.
A/B testing showed that the model trained with these features was able to increase engagement rate of recommended content by 4.7% relatively, which is a significant lift for a mature model.
A/Bテストでは、これらの機能で学習させたモデルは、推薦コンテンツのエンゲージメント率を4.7%相対的に高めることができ、成熟したモデルとしては大きなリフトアップ効果がありました。

## 6.3. Ranking of Personalized Trends

Showing top trending content (e.g., Hashtags, Events, breaking news) is an important way to keep users informed about what is happening locally and globally.
トップトレンドのコンテンツ(ハッシュタグ、イベント、ニュース速報など)を表示することは、地域や世界で起こっていることをユーザに知らせる重要な方法.
The implementation for Trends follows a two-stage process of Trends detection followed by ranking.
Trendsの実装は、Trendsの検出とランキングの2段階を踏んでいる.
Prior to SimClusters, the ranking of a Trend primarily depended on its volume and a small number of personalization features.
SimClusters以前は、トレンドのランキングは主にそのボリューム(?)と少数のパーソナライズ機能によって決定されていた.
We used Trends SimClusters representations to score Trends for a given user by using the dot-product of the user’s interest representation along with the real-time representation for a Trend.
トレンドのSimClusters表現を使って、user interest表現とリアルタイムのtrend表現のドットプロダクト(内積!)を使用することで、与えられたユーザ-トレンドペアをスコア化した.
A/B testing revealed that using these scores led to a 8% increase in user engagement with the Trends themselves, as well as a bigger 12% increase in engagement on the landing page subsequent to a click.
A/Bテストでは、このスコアを使用することで、Trends自体のユーザエンゲージメントが8％増加し、さらにクリック後のランディングページのエンゲージメントが12％増加することがわかった.
These improvements are large when compared against other experiments run on this product.
これらの改善は、この製品で行われた他の実験と比較すると、大きなものである.

## 6.4. Topic Tweet Recommendations トピック ツイート おすすめ度

Given a Topic in a pre-defined topic taxonomy such as “Fashion” or “Marvel Movies”, how can we identify the best content about it? The original implementation here (before the product was launched publicly) primarily relied on custom text matching rules curated by human experts to identify topical Tweets.
「ファッション」や「マーベル映画」など、あらかじめ定義されたトピック分類法のトピックがある場合、そのトピックに関する最高のコンテンツを特定するにはどうすればよいだろうか. ここでのオリジナルの実装(productが一般に発売される前)は、主に人間の専門家がキュレーションしたカスタムテキストマッチングルールに依存して、トピックツイートを識別していた.
Once we realized that this approach surfaced a number of false positives (primarily due to a Tweet’s text incidentally matching the rules for a Topic), we tested a second implementation where we first identify those Tweets whose SimClusters representation has high cosine similarity with the representation of the query Topic, and then apply the textual matching rules.
この方法では、多くの誤検出(主にツイートのテキストがトピックのルールと偶然一致することによる)があることがわかったので、2番目の実装をテストした. まず、SimClusters表現が、query topic表現(=対象のtopic表現)と高いコサイン類似度を持つツイート表現を特定し、次にテキストマッチング規則(??既存のアプローチ? 二段階にしたって事?)を適用した.
Internal evaluation showed that the second approach returned much better results, therefore we launched this product publicly using this approach.
社内で評価したところ、2番目のアプローチの方がはるかに良い結果が得られたため、このアプローチでproductをlaunchした.
Since launch, this feature has received positive press externally as well as causing higher engagement with Tweets from the broader user base.
この機能は、発売以来、外部で好評を博し、より多くのユーザからツイートへのエンゲージメントを高めている.

## 6.5. Ranking Who To Follow Recommendations フォローすべき人ランキング おすすめ

The candidates for Who To Follow recommendations are ranked using an engagement prediction model, to which we added new features based on the SimClusters representations of the viewing user and the candidate user.
Who To Followレコメンデーションの候補は、エンゲージメント予測モデルを用いてランク付けされる. このモデルには、**閲覧ユーザと候補ユーザのSimClusters表現**に基づく新しい特徴が加えられている.(特徴量としての活用.)
In A/B tests, we observed an impressive increase of 7% in the follow rate by using these new features.
A/Bテストでは、これらの新たな特徴量を使用することで、フォロー率が7％向上することが確認された.

## 6.6. Applications in progress 現在進行中のアプリケーション

### 6.6.1. Notifications quality filter. 通知品質フィルター

A crucial task on Twitter is to protect users from getting abusive or spammy replies or mentions.
Twitterの重要なタスクは、罵倒やスパム的なリプライやメンションを受けないようにユーザを保護することである.
We developed new SimClusters representations for users based on the user–user block graph (i.e.when one user blocks another), and used these representations as features to train a model for filtering out abusive and spammy replies.
**ユーザとユーザのブロックグラフ（あるユーザーが他のユーザーをブロックした場合）に基づく新しいユーザ表現をSimClustersで開発**し、この表現を特徴として、罵倒やスパムのような返信をフィルタリングするモデルを学習した.
In offline tests, the model showed an impressive 4% lift in PR-AUC5 .
オフラインテストでは、PR-AUC5 が 4％向上するという素晴らしい結果を示した.

### 6.6.2.Supervised embeddings from feature combinations. 特徴の組み合わせから教師付き埋込を行う

While SimClusters representations mostly capture information from various engagement graphs, we are also experimenting approaches to combine it with other features about users or items (for example, follower counts or geo information).
**SimClustersの表現は、主に様々なエンゲージメントグラフから情報を取得する**が、ユーザやアイテムに関する他の特徴(例えば、フォロワー数やジオ情報)と組み合わせるアプローチも試している.
One approach where we are obtaining promising early results is to train a deep neural network on an ancillary prediction task (such as engagement prediction) where the input features are both the user and item SimClusters representations along with previously developed features for the user and item.
私たちが有望な初期結果を得ているアプローチの1つは、補助的な予測タスク(エンゲージメント予測など)でディープニューラルネットワークを訓練することで、入力特徴としてユーザとアイテムのSimClusters表現と、ユーザとアイテムのために以前に開発した特徴の両方を使用する.
By choosing the right architecture for this neural net, for example, the two-tower DNN model [36], we are able to learn dense embeddings separately for users and items.
このニューラルネットに適切なアーキテクチャ、例えば2塔式DNNモデル[36]を選択することで、ユーザーとアイテムについて別々に密な埋め込みを学習することができるようになる.(説明変数にユーザやアイテムのsimClusters表現、目的変数にCTR等のengagementスコアで学習させ、中間層を新たなembeddingとして抜き出す、みたいなアプローチ?)

### 6.6.3. 6.6.3 Real-time Event notifications. 6.6.3 リアルタイムイベント通知

A major application at Twitter is to notify users who may be interested when a major news event happens.
Twitterでの主な用途は、大きなニュースが起こったときに、興味を持ちそうなユーザに通知することである.(プッシュ通知か...!)
Using the SimClusters representation of an Event (which is in turn derived by aggregating the representations of the human-curated Tweets about it), we can identify the communities of users who will be interested in it, and subsequently target users interested in them.
イベントのSimClusters表現(これは、そのイベントに関する人間が作成したツイート表現を集約することで得られる)を使って、**そのイベントに興味を持つユーザのコミュニティを特定**し、そのコミュニティに興味を持つユーザをターゲットにすることができる. (新規アイテムの場合はどうしたらいいんだろう... そのアイテムの属性情報と類似したツイート表現や、作成者のUser表現を使ったら、aggregateして新規イベント表現を作れるだろうか...?)
We are currently evaluating such an approach.
現在、そのようなアプローチを評価している.

# 7. Related Work 関連作品

Traditionally, approaches to recommender systems are categorized as either neighborhood-based (which do not involve model-fitting), or model-based (which fit a model to the input data).
従来、推薦システムのアプローチは、モデルフィッティングを伴わないneighborhoodベース(ex. content-base等で、埋め込みベクトルを作るアプローチ)と、入力データにモデルをフィッティングするモデルベース(factorization machine)に分類されている.

In our experience of building recommendations at Twitter, we find that neighborhood-based methods are easier to scale, more accurate, more interpretable, and also more flexible in terms of accommodating new users and/or items [9, 11, 12, 31].
**Twitterでレコメンデーションを構築した経験から、neighborhoodベースの手法は、スケールが簡単で、より正確で、より解釈しやすく、また新しいユーザやアイテムに対応する点で、より柔軟であることがわかった** [9, 11, 12, 31] .
Recent research has also found that well-tuned neighborhood-based methods are not easy to beat in terms of accuracy [6].
また、最近の研究では、よく調整された近傍領域ベースの手法は、精度の面で簡単には勝てないことが分かっている[6].
However, neighborhoodbased approaches do not provide a general solution – we needed to build and maintain separate systems to solve each recommendation sub-problems at Twitter in the past (see Section 1 for more discussion of our past work).
しかし、neighborhoodベースのアプローチは一般的な解決策を提供するものではなく、私たちは過去にTwitterでそれぞれの推薦サブ問題を解決するために別々のシステムを構築・維持する必要がありました(過去の研究についての詳細はセクション1を参照してください)

Model-based approaches, such as factorized models [18], graph embedding [10, 26] or VAE [22], fit separate parameters for each user or item.
因数分解モデル[18](factorization machineの事かと思ったらMFの事だった!)、グラフ埋め込み[10, 26]、VAE[22]などのモデルベースのアプローチは、各ユーザやアイテムに対して別々のパラメータを当てはめる.(ここでの"パラメータ"って、特徴量の事? 埋め込みベクトルの事でもあるのかな.)
The number of model parameters that need to be learned in order to scale to a billion-user social network can easily approach 1012, necessitating unprecedentedly large systems for solving ML problems at that scale.
10億人規模のソーシャルネットワークに対応するためには、学習すべきモデルパラメータの数が$10^{12}$個に達することもあり、そのような規模のML問題を解決するためには、これまでにない大規模なシステムが必要となる.
Hybrid models, such as Factorization Machine [27] and Deep Neural Networks (DNNs) [5] have been introduced to reduce the parameter space by utilizing the side information as prior knowledge for users and items.
ユーザやアイテムの事前知識としてサイド情報(=属性情報的な?)を活用し、パラメータ空間を縮小するために、Factorization Machine [27] やディープニューラルネットワーク (DNN) [5] などのハイブリッドモデルが導入されている.
However, they require either well-defined feature vectors or pre-trained embeddings from auxiliary tasks as the input representation of users and items.
しかし、これらはユーザやアイテムの入力表現として、よく定義された特徴ベクトルか、補助タスクから事前に訓練された埋め込みを必要とする.
Graph Convolutional Networks (GCNs) [16, 37] can enrich pre-existing feature representations of the nodes by propagating the neighborhood information from the graph, without fitting model parameters for each node.
グラフ畳み込みネットワーク（GCN）[16, 37]は、各ノードのモデルパラメータをフィッティングすることなく、グラフから近傍情報を伝播することで、ノードの既存の特徴表現を豊かにすることができる.
GCNs perform well in domains where the items have a good set of pre-existing features, e.g., where the items are images [37].
GCNは、アイテムが画像である場合など、アイテムが既存の特徴の良いセットを持っているドメインでうまく機能します[37]。
Such approaches work less well in the absence of useful content features and cannot deal with the short half life of items either.
このようなアプローチは、有用なコンテンツの特徴がない場合にはうまく機能せず、アイテムの半減期が短い場合にも対応できない。
We see SimClusters as an approach to scalably learn user and item representations which can be fed to hybrid models like DNNs [5] or GCNs [37].
SimClustersは、DNN [5]やGCN [37]のような**ハイブリッドモデルに供給できるユーザとアイテムの表現をスケーラブルに学習するアプローチだと考えている**.

Our problem definition bears some similarity to the cross-domain or heterogeneous recommender systems problem [2, 38], where one can use a joint objective function to simultaneously learn the representations of users and items across multiple domains [8, 39].
我々の問題定義は、複数のドメインにまたがるユーザとアイテムの表現を同時に学習するために共同目的関数を使用できる、クロスドメインまたは異種推薦システム問題 [2, 38] に類似している [8, 39].
It is unclear how these methods can support our requirements for scale, handling dynamic items and graphs, and intepretability.
これらの方法は、スケール、動的なアイテムやグラフの扱い、インテプリタビリティといった我々の要求をどのようにサポートできるかは不明である.

# 8. Conclusion 結論

We proposed a framework called SimClusters based on detecting bipartite communities from the user-user graph and use them as a representation space to solve many personalization and recommendation problems at scale.
我々は、**ユーザ-ユーザのグラフから二部コミュニティを検出**し、それを**表現空間として利用する**ことに基づくSimClustersというフレームワークを提案し、多くのパーソナライゼーションや推薦問題をスケールアップして解決する.
SimClusters uses a novel algorithm called Neighborhood-aware MH for solving the crucial problem of unipartite community detection with better scalability and accuracy.
SimClustersでは、一組のコミュニティ検出という重要な問題を、より優れたスケーラビリティと精度で解決するために、Neighborhood-aware MHという新しいアルゴリズムを用いている.
We also presented several diverse deployed and in-progress applications where we use SimClusters representations to improve relevance at Twitter.
また、SimClusters表現を用いてTwitterでの関連性を向上させる、多様なデプロイ済みおよび進行中のアプリケーションをいくつか紹介した.

# 9. Supplement: Further Evaluation サプリメント さらなる評価

The code for Neighborhood-aware MH and an in-memory implementation of Stage 1 are open-sourced in https://github.com/twitter/sbf.
Neighborhood-aware MHのコードとStage 1のインメモリ実装は、https://github.com/ twitter/sbfでオープンソース化されている.

## 9.1. Neighborhood-aware MH Empirical evaluation Neighborhood-aware MH の 経験的評価

### 9.1.1. A.1.1 Comparison with RandomMH [33]. A.1.1 RandomMH [33]との比較。

We conducted a simple empirical evaluation in which we generated synthetic graphs with 100 nodes and varying number of communities, such that the probability of an edge between nodes inside the same community was large and the probability of an edge otherwise was small.
100ノードの合成グラフを作成し、コミュニティの数を変化させ、同じコミュニティ内のノード間のエッジの確率が大きく、それ以外のエッジの確率が小さくなるように、簡単な実証評価を行いました。
The approach from [33] which we label ‘RandomMH’, as well as our approach (‘Neighborhood-Aware’) are implemented in the same code and use the same settings, except that the implementations for the proposal and the initialization functions are different.
RandomMH」と名付けた[33]のアプローチと、我々のアプローチ（「Neighborhood-Aware」）は、提案と初期化関数の実装が異なるだけで、同じコードで実装され同じ設定を使用しています。
We compare both the approaches in terms of how many epochs they need to be to run to recover the synthetic communities, as well as the wall clock time (since the runtime for each epoch differs between the two approaches).
両者のアプローチを、合成コミュニティを回復するために何エポック実行する必要があるかという点と、ウォールクロック時間（各エポックの実行時間が両者で異なるため）の点で比較した。
As can be seen from the results in Table 2, the number of epochs and time required when using RandomMH grows exponentially with increasing 𝑘, as expected.
表2の結果からわかるように、RandomMHを使用した場合のエポック数と所要時間は、予想通りᑘの増加とともに指数関数的に成長する。
Neighborhood-aware MH on the other hand has no such problem with increasing 𝑘.
一方、Neighborhood-aware MHは、ᑘが増加してもそのような問題はない。

### 9.1.2. A.1.2 Comparison on real datasets. A.1.2 実際のデータセットでの比較。

We ran experiments on 8 real datasets (see Table 3) and compared Neighborhood-aware MH to the following algorithms from prior literature: (a) BigClam [34]: BigClam is interesting to compare to since there are many similarities, with the main difference being that it’s optimized using gradient descent rather than randomized combinatorial optimization as in our case.
我々は8つの実データセット（表3参照）で実験を行い、Neighborhood-aware MHを以下の先行文献のアルゴリズムと比較した： (a) BigClam [34]： BigClam[34]：多くの類似点があるため、比較するのは興味深いですが、主な違いは、我々の場合のようにランダムな組み合わせ最適化ではなく、勾配降下を使用して最適化されていることです。
We used the implementation in the SNAP package [21].
SNAPパッケージの実装を使用した[21]。
(b) Graclus [7]: Graclus optimizes weighted graph cuts without needing to compute eigenvectors, making it much faster than spectral algorithms without losing accuracy.6 Note that for all 8 of these datasets, the RandomMH algorithm proposed in [33] was not able to make any progress inside the allotted time (6 hours).
(b) Graclus [7]： Graclusは固有ベクトルを計算することなく重み付きグラフカットを最適化するため，精度を落とすことなくスペクトルアルゴリズムよりもはるかに高速に処理することができます6．なお，これらの8つのデータセットすべてにおいて，[33]で提案したRandomMHアルゴリズムは決められた時間（6時間）内に進展することができませんでした．

We use two kinds of datasets: similarity graphs calculated for a subset of Twitter users in the way described in Section 3.1, as well as the 4 biggest undirected social networks we were able to find externally on the KONECT [19] collection.
3.1節で説明した方法でTwitterユーザのサブセットに対して計算された類似グラフと、KONECT [19] コレクションで外部から見つけることができた4大無向性ソーシャルネットワークの2種類のデータセットを使用する。
While our method (Neighborhood-Aware MH) and Graclus both work with weighted graphs, BigClam does not, so we restrict ourselves to unweighted graphs.
我々の手法（Neighborhood-Aware MH）とGraclusは共に重み付きグラフを扱うが、BigClamはそうではないので、我々は非重み付きグラフに限定する。
For Neighborhood-aware MH, we run it with 𝑙 = 1, i.e.
Neighborhood-aware MHについては、ᑙ = 1で実行します、すなわち。
each node gets assigned to at most one community, to keep the comparison with Graclus fair.
Graclusとの比較を公平にするため、各ノードは最大1つのコミュニティに割り当てられる。
𝛼 which can be used to trade precision with recall7 was set to 10, and 𝑇 , number of epochs, was set to 5.
を10に設定し、エポック数ᵄは5とした。
All experiments were run on a 16-core machine with 256GB RAM.
すべての実験は、256GB RAMを搭載した16コアのマシンで実行されました。

We evaluate all methods on Precision and Recall.
すべての方法をPrecisionとRecallで評価します。
A method is said to predict the existence of an edge (𝑢, 𝑣) if 𝑢 and 𝑣 share at least one community per the output of the method.
ある方法は、𝑢と𝑣が方法の出力あたり少なくとも1つのコミュニティを共有している場合、エッジ（𝑢, 463）の存在を予測すると言う。
The Precision of a method is the proportion of actually existing predicted edges among all predicted edges for a method.
手法の精度は、その手法で予測されたすべてのエッジのうち、実際に存在する予測エッジの割合である。
The Recall of a method is the proportion of correctly predicted edges (by that method) among all actually existing edges in the graph.
ある手法のRecallは、グラフに実際に存在するすべての辺のうち、その手法によって正しく予測された辺の割合である。
Given Precision and Recall, F1 is their harmonic mean.
PrecisionとRecallがあるとき、F1はそれらの調和平均である。
Note that Precision and Recall are not properties of a community by itself, but rather are properties of the entire output i.e.
なお、PrecisionとRecallは、コミュニティ単体の特性ではなく、出力全体の特性である、すなわち
the (possibly overlapping) set of communities.
コミュニティーの（重複する可能性のある）集合である。
Note that our evaluation measures do not need any external groundtruth; they simply measure how well the community assignments are able to reconstruct the input graph.
なお、我々の評価指標は外部からの真実を必要とせず、単にコミュニティ割り当てが入力グラフをどれだけ再構成できるかを測定するものである。

For all of the datasets, we generally tried to set 𝑘 – the number of discovered communities – so that the average size of a community is 100, because we see that having larger communities leads to significantly degraded Precision as unrelated pairs of nodes start to share at least one community.
すべてのデータセットで、コミュニティの平均サイズが100になるように、発見されたコミュニティの数であるᑘを設定しました。
In the case of the Orkut and Livejournal datasets however, we used a smaller 𝑘 in order to get at least one of our baselines to run successfully.
しかし、OrkutとLivejournalのデータセットでは、ベースラインの少なくとも1つが正常に動作するように、より小さなᑘを使用しました。

For BigClam, we found that the default implementation was taking a very long time (more than 100× the time for our method on our smallest dataset), so we made a modification to initialize using a random neighborhood (same as our method) instead of trying to identify the neighborhoods with the best conductance which was proving very expensive.
BigClamについては、デフォルトの実装では非常に時間がかかることがわかりました（最小のデータセットで我々の手法の100倍以上の時間がかかる）ので、非常に高価であることが判明した最良のコンダクタンスの近隣を識別しようとするのではなく、ランダムな近隣（我々の手法と同じ）を使用して初期化するように修正しました。
Despite this optimization, BigClam was unable to finish execution within 6 hours for our 3 biggest datasets.
この最適化にもかかわらず、BigClamは3つの大きなデータセットで6時間以内に実行を終了することができませんでした。
For Actors and Petster, we found that BigClam finished execution successfully, but the results were completely unintelligible and seemed to have been affected by an unidentified bug.
ActorとPetsterについては、BigClamは正常に実行を終了したが、結果は全く意味不明で、正体不明のバグの影響を受けているようであることがわかった。

As can be seen from the results in Table 3, our method is able to produce significantly more accurate results and is also much faster, typically 10x-100x faster.
表3の結果からわかるように、私たちの方法は大幅に精度の高い結果を出すことができ、また、通常10倍から100倍と非常に高速であることがわかります。
Neighborhood-aware MH is fast because each epoch requires making a single pass over all the vertices and their adjacency lists and also because the overall approach is easy to parallelize.
近傍探索型MHが高速なのは、各エポックがすべての頂点とその隣接リストに対して1回のパスで済むためであり、また全体的なアプローチが並列化しやすいためです。
Our approach is able to run inside 1.5 hours for a graph with 100M nodes and 5B edges (Top100M), while the largest graph either of our baselines is able to run on is at least an order of magnitude smaller.
我々のアプローチは、100Mのノードと5Bのエッジを持つグラフ（Top100M）に対して1.5時間以内に実行することができましたが、我々のベースラインのいずれかが実行できる最大のグラフは、少なくとも1桁小さいものです。

## 9.2. Bipartite Communities Empirical evaluation Bipartite Communitiesの実証評価

A possible concern with our approach to discovering bipartite communities is whether breaking the problem up into 3 separate steps can result in a loss of accuracy, as compared to jointly learning the bipartite communities directly.
2つのコミュニティを発見する我々のアプローチで懸念されるのは、問題を3つの別々のステップに分けることで、2つのコミュニティを直接共同で学習する場合と比較して、精度が低下する可能性があるということである.
To understand this empirically, we compare against NMF (Non-negative Matrix Factorization) – recall that with both NMF and our approach, the end output is two low-dimensional sparse matrices.
このことを経験的に理解するために、NMF(Non-negative Matrix Factorization)と比較します。NMFも我々のアプローチも、最終出力は2つの低次元スパースマトリックスであることを思い出してください.
Specifically we use Scikit-Learn’s implementation [3, 25] of alternating minimization using a Coordinate Descent solver, and with ‘nndsvd’ initialization, and with 𝐿1 penalty, where the 𝐿1 coefficient is adjusted to return results of comparable sparsity to our approach.
具体的には、Scikit-Learnの座標降下ソルバーによる交互最小化の実装 [3, 25] を使用し、初期化は「nndsvd」、ᵃ1ペナルティは、我々のアプローチと同等のスパース性を返すようにᵃ1係数を調整します。
For our approach, we set various parameters as follows: for the similarity graph calculation in step 1, we only include edges with cosine similarity > 0.02; for Neighborhood-aware MH in step 2, we set 𝑙 = 4, (i.e.
ステップ1の類似グラフ計算では、コサイン類似度が0.02以上のエッジのみを対象とし、ステップ2のネイバーフッドアウェアMHでは、ᑙ=4、（すなわち、"Neighborhood-aware MH"）というように、様々なパラメータを設定しました。
each rightnode can be assigned to at most 4 communities), 𝛼 (see Eqn 1) to 10, and 𝑇 (max epochs) to 5; for calculating U in step 3, we assign a left-node to a community if and only if it is connected to at least 2 right-nodes that are assigned to that community.
各右ノードは最大4つのコミュニティに割り当てられる）、Ǽ（式1参照）～10、↪L_1D447↩（最大エポック数）～5。ステップ3のUの計算では、左ノードは、そのコミュニティに割り当てられた右ノードの少なくとも2つと接続している場合にのみコミュニティに割り当てます。
All experiments were run on commodity servers with 8 cores and 24GB RAM.
すべての実験は、8コアと24GB RAMを搭載したコモディティサーバーで実行されました。
Note that this evaluation is purely to benchmark the accuracy of our approach; in terms of actual applicability, neither NMF nor other variants are practically feasible at our scale.
なお、この評価は、純粋に我々のアプローチの精度をベンチマークするためのものであり、実際の適用可能性という点では、NMFも他のバリエーションも、我々のスケールでは現実的に実現不可能であることに注意してください。

For evaluation, we use a combination of directed graphs and document-word occurrence graphs, and evaluate on the task of link prediction.
評価には、有向グラフと文書-単語出現グラフの組み合わせを用い、リンク予測というタスクで評価しています。
We run both the approaches on 90% of the input dataset, and make a test set consisting of 10% of the held-out edges as well as the same number of randomly generated pairs of nodes which serve as negative examples in the test set.
両アプローチを入力データセットの90%で実行し、10%の保留されたエッジと、テストセットで否定例となる同数のランダムに生成されたノードのペアからなるテストセットを作成する。
E.g., if a graph consists of 100𝐾 edges, this results in a “training set” of 90𝐾 edges and test-set of 20𝐾 edges (10𝐾 positives and 10𝐾 negatives).
例えば、グラフが100_43個のエッジで構成されている場合、90_43個のエッジの「トレーニングセット」と20_43個のエッジの「テストセット」（10_43個のポジティブと10_43個のネガティブ）が得られます。
In order to predict whether an edge (𝑖, 𝑗) exists, we use the cosine similarity of U(𝑖) and V(𝑗) as the predicted score for the existence of the edge.
エッジ(𝑖, ↪Ll457)が存在するかどうかを予測するために、U(𝑖)とV(↪Ll457)のコサイン類似度をエッジ存在の予測スコアとして使用します。
(For both NMF and our approach, cosine similarity worked marginally better than dot product.) We evaluate the quality of these predicted scores in two ways - the first is we check the Correlation of the true label {0, 1} with the predicted score; and the second is to calculate the AUC (Area Under the ROC Curve).8
(NMFと我々のアプローチの両方において、コサイン類似度はドット積よりもわずかに優れていた）。1つ目は、真のラベル{0, 1}と予測スコアの相関をチェックする方法、2つ目はAUC（Area Under the ROC Curve）を計算する方法である8．

Details about the datasets as well as the results are in Table 4.
データセットの詳細と結果は、表4に示す。
In terms of Correlation, our approach is consistently better across all datasets, while in terms of AUC, both the approaches are comparable.
相関の面では、全てのデータセットにおいて我々のアプローチの方が一貫して優れており、AUCの面では、両アプローチは同等である。
We also include the timing information, where our approach is generally a little faster than NMF.
また、タイミング情報を含めると、一般的にNMFより少し速くなる。
However, note that the primary advantage of our approach is not that it’s faster than NMF, but that it’s more scalable, meaning that it is possible to extend to billionnode graphs and hundreds of thousands of latent dimensions while scaling NMF similarly is prohibitively costly.
つまり、10億ノードのグラフや数十万個の潜在次元に拡張することが可能である一方、NMFを同様に拡張するのは法外なコストがかかるということです。
