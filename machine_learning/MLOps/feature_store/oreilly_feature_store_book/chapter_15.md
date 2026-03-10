CHAPTER 15: TikTok’s Personalized Recommender: The World’s Most Valuable AI System
第15章: TikTokのパーソナライズドレコメンダー: 世界で最も価値のあるAIシステム

This chapter brings together what we have learned so far in the form of a case study.
この章では、これまで学んだことをケーススタディの形でまとめます。
You will design, build, and deploy a real-time, personalized video recommendation system that works at scale.
あなたは、スケールで機能するリアルタイムのパーソナライズドビデオ推薦システムを設計、構築、展開します。
It is inspired by TikTok’s recommender system—the AI system that enabled TikTok to dethrone YouTube through innovation in real-time AI.
これは、TikTokがリアルタイムAIの革新を通じてYouTubeを打倒することを可能にしたAIシステムであるTikTokのレコメンダーシステムに触発されています。
We will build our recommender system using the _retrieval-and-ranking architecture_ for real-time personalized AI systems.
私たちは、リアルタイムパーソナライズAIシステムのための_retrieval-and-ranking architecture_を使用してレコメンダーシステムを構築します。
We will also extend our video recommendation system to include agentic search for videos using natural language.
また、自然言語を使用したビデオのエージェンティック検索を含むように、ビデオ推薦システムを拡張します。
Finally, we will conclude the book with a dirty dozen of fallacies that we hope you will no longer fall for after having read this book, as well as some advice on your ethical responsibilities as an AI system builder.
**最後に、この本を読んだ後にもう二度と騙されないことを願う12の誤謬と、AIシステムビルダーとしての倫理的責任に関するいくつかのアドバイス**で本書を締めくくります。
Thanks for hanging in there, and let’s get cracking with the most rewarding part of working with AI—building real-world AI systems that can change the world for the better.
ここまでお付き合いいただきありがとうございます。それでは、**AIと共に働く最もやりがいのある部分、つまり世界をより良く変えることができる実世界のAIシステムを構築**することに取り掛かりましょう。

<!-- ここまで読んだ! -->

## 1. Introduction to Recommenders レコメンダーの紹介

_Recommender systems help users discover relevant content in user-facing systems._
_レコメンダーシステムは、ユーザー向けシステムで関連するコンテンツを発見するのに役立ちます。_
The content can be anything from videos to music to ecommerce to social media posts.
コンテンツは、ビデオ、音楽、eコマース、ソーシャルメディアの投稿など、何でもかまいません。
The first approaches to recommendation systems were not personalized.
推薦システムの最初のアプローチはパーソナライズされていませんでした。
_Content-based recommendation systems for videos can use genres, directors, actors, or_ plot keywords to suggest videos that are similar to those a user has previously watched and enjoyed.
_ビデオのコンテンツベースの推薦システムは、ジャンル、監督、俳優、または_ プロットキーワードを使用して、ユーザが以前に視聴し楽しんだビデオに似たビデオを提案できます。
You only need content usage features to train content recommender models, which makes them easy to scale.
**コンテンツレコメンダーモデルをトレーニングするには、コンテンツ利用特徴量だけが必要**であり、これによりスケールしやすくなります。
Netflix and YouTube still have content-based recommendations as one of several types of recommendations they provide.
**NetflixとYouTubeは、提供するいくつかのタイプの推薦の1つとして、依然としてコンテンツベースの推薦を持っています。**

<!-- ここまで読んだ! -->

The next classes of recommender systems were built on interaction datasets, contain‐ ing user action events for content, such as views, likes, and shares.
次のクラスのレコメンダーシステムは、ビュー、いいね、シェアなどのコンテンツに対するユーザーアクションイベントを含むインタラクションデータセットに基づいて構築されました。
Item-to-item (i2i) _recommendation focuses on the relationships between items themselves, enabling fea‐_ tures like “Customers who bought this item also bought…” or “If you liked this video, you might enjoy….” 
**アイテム間（i2i）_推薦は、アイテム自体の関係に焦点を当て、「このアイテムを購入した顧客は他に何を購入したか…」や「このビデオが気に入ったなら、こちらも楽しめるかもしれません…」といった機能を可能**にします。
Interaction datasets provide patterns of co-consumption or simi‐ larity, and i2i methods enable users to easily explore related options.
インタラクションデータセットは、共同消費や類似性のパターンを提供し、**i2iメソッドはユーザーが関連オプションを簡単に探索できるように**します。

<!-- ここまで読んだ! -->

_User-to-item (u2i) recommendations take a different approach by centering recom‐_ mendations on the individual user.
ユーザーからアイテム（u2i）推薦は、個々のユーザに中心を置くことで異なるアプローチを取ります。
Here, the goal is to suggest items to a user based on their historical preferences and behaviors, or by drawing on the experiences of similar users.
ここでは、ユーザーの歴史的な好みや行動に基づいてアイテムを提案すること、または類似のユーザーの経験を引き出すことが目標です。
The first widely used method for i2i and u2i recommender systems was _collaborative filtering, but it has challenges working with large data volumes and_ sparse data (where most users interact with only a tiny fraction of items).
i2iおよびu2iレコメンダーシステムの最初の広く使用されている方法は_コラボレーティブフィルタリングでしたが、大量のデータボリュームや_ スパースデータ（ほとんどのユーザーがアイテムのごく一部としか相互作用しない場合）での作業には課題があります。
Factoriza‐ _tion machines were introduced to better handle data sparsity, but they also encounter_ scalability issues for large data volumes and real-time updates.
ファクタリゼーションマシンはデータのスパース性をより良く処理するために導入されましたが、**大量のデータボリュームやリアルタイムの更新に対してもスケーラビリティの問題に直面**します。

<!-- ここまで読んだ! -->

In the next section, we will look at the state-of-the-art retrieval-and-ranking architec‐ ture that addresses these challenges, but we will start by looking at the data we need to collect to build our recommendation system.
次のセクションでは、これらの課題に対処する最先端のretrieval-and-rankingアーキテクチャを見ていきますが、まずは推薦システムを構築するために収集する必要があるデータを見ていきます。
Table 15-1 shows popular features used to train video recommendation models.
表15-1は、ビデオ推薦モデルをトレーニングするために使用される一般的な特徴量を示しています。

![]()
_Table 15-1. Classes of features used in video recommender systems and their data properties_
**表15-1. ビデオレコメンダーシステムで使用される特徴のクラスとそのデータ特性**

- user profileグループ
  - 特徴量の例: 性別, 年齢, 言語, デバイス, 興味, 場所, 最近の視聴
  - データ変換の分類: モデル非依存, モデル依存
  - データボリューム/速度: GBs/TBs, バッチおよびストリーミング
- Videoグループ
  - 特徴量の例: タイトル, ジャンル, 長さ, 年齢, クリック, CTR, いいね, 説明, コンテンツ
  - データ変換の分類: モデル非依存, モデル依存
  - データボリューム/速度: GBs/TBs, バッチおよびストリーミング
- Interactionsグループ
  - 特徴量の例: 視聴, スキップ, いいね, シェア, 視聴時間
  - データ変換の分類: モデル非依存, モデル依存
  - データボリューム/速度: TBs/PBs, バッチおよびストリーミング
- Real-time contextグループ
  - 特徴量の例: トレンド（あなたの近く、あなたの人口統計、友人）
  - データ変換の分類: モデル非依存, オンデマンド
  - データボリューム/速度: GBs/TBs, ストリーミング
- In-session browsingグループ
  - 特徴量の例: デバイス、使用パターン（ビンジなど）、最後のクリック、セッションの長さ
  - データ変換の分類: モデル非依存, オンデマンド
  - データボリューム/速度: GBs/TBs, ストリーミング
- Graph/Socialグループ
  - 特徴量の例: ソーシャルアクション（友人がいいねしたなど）、社会的近接
  - データ変換の分類: モデル依存, オンデマンド
  - データボリューム/速度: GBs/TBs, バッチおよびストリーミング

<!-- ここまで読んだ! -->

At a high level, the features useful for building recommendation models are centered around users, items (videos, in our case), and interactions between users and items.
**高いレベルで、推薦モデルを構築するのに役立つ特徴は、ユーザー、アイテム（この場合はビデオ）、およびユーザーとアイテム間の相互作用に中心を置いています。**
Some of the features contain slowly changing data that is stored in a data warehouse and updated by batch feature pipelines; for example, information about a user’s viewing behavior, such as the average view percentage for videos and compressed viewing statistics on video genres.
いくつかの特徴は、データウェアハウスに保存され、**バッチフィーチャーパイプラインによって更新されるゆっくりと変化するデータ**を含んでいます。**たとえば、ビデオの平均視聴率やビデオジャンルに関する圧縮視聴統計など、ユーザーの視聴行動に関する情報**です。

Other features contain real-time context information about global or localized viewing trends.
他の特徴は、グローバルまたはローカライズされた視聴トレンドに関するリアルタイムのコンテキスト情報を含んでいます。
For example, to enable our recommender to quickly spread breaking news, both the number of clicks and the click-through rate (CTR) are important realtime context features for videos and are updated by streaming feature pipelines.
たとえば、私たちのレコメンダーが速報ニュースを迅速に広めることを可能にするために、クリック数とクリック率（CTR）の両方がビデオにとって重要なリアルタイムコンテキスト機能であり、ストリーミングフィーチャーパイプラインによって更新されます。
Batch feature pipelines would be too slow for spreading breaking news.
**バッチフィーチャーパイプラインは速報ニュースを広めるには遅すぎます。**

In-session browsing features similarly contain valuable real-time signals of recent user activity but are computed on demand from request-time parameters.
セッション中のブラウジング機能も、最近のユーザー活動の貴重なリアルタイム信号を含んでいますが、リクエスト時のパラメータからオンデマンドで計算されます。
For example, if the user started viewing videos about cooking but then switched to sports, the recommender could include recommendations about sports that the user has historically interacted with and videos of the same length as other videos that the user has historically watched.
たとえば、ユーザが料理に関するビデオの視聴を開始したが、その後スポーツに切り替えた場合、レコメンダーはユーザーが歴史的に相互作用してきたスポーツに関する推薦や、ユーザーが歴史的に視聴してきた他のビデオと同じ長さのビデオを含めることができます。

<!-- ここまで読んだ! -->

## 2. A TikTok Recommender with the Retrieval-and-Ranking Architecture Retrieval-and-Rankingアーキテクチャを用いたTikTokレコメンダー

TikTok is the world’s most popular video streaming platform in 2025.
TikTokは2025年に世界で最も人気のあるビデオストリーミングプラットフォームです。
It has several different ways to recommend videos, including a friends feed and a following feed.
友人のフィードやフォローのフィードなど、ビデオを推薦するためのいくつかの異なる方法があります。
But its “For You” feed is what differentiates TikTok from other video streaming plat‐ forms.
しかし、「For You」フィードがTikTokを他のビデオストリーミングプラットフォームと差別化しています。
It really is personalized for you, and it updates its recommendations in real time, based on your activity.
これは本当にあなたのためにパーソナライズされており、あなたの活動に基づいてリアルタイムで推薦を更新します。
For a human to perceive the feed as reacting to their actions, it cannot take more than a couple of seconds to update; otherwise it will be “laggy,” not intelligent.
**人間がフィードが自分の行動に反応していると認識するためには、更新に数秒以上かかってはいけません。**そうでなければ、「遅延」が生じ、知的ではなくなります。

<!-- ここまで読んだ! -->

We will build our own version of the personalized “For You” feed based on the retrieval-and-ranking architecture, shown in Figure 15-1.
私たちは、図15-1に示されているretrieval-and-rankingアーキテクチャに基づいて、パーソナライズされた「For You」フィードの独自のバージョンを構築します。
We will decompose the problem of recommending videos into two phases: (1) a retrieval phase that uses a scalable vector index to return a few hundred candidate videos and (2) a ranking phase to order the hundreds of candidates based on a metric we want to optimize, like increased user engagement.
私たちは、ビデオを推薦する問題を2つのフェーズに分解します。(1) スケーラブルなベクトルインデックスを使用して数百の候補ビデオを返すリトリーバルフェーズと、(2) ユーザーエンゲージメントの向上のような最適化したいメトリックに基づいて数百の候補を順序付けるランキングフェーズです。

![]()
_Figure 15-1. TikTok’s personalized recommender service is built on a retrieval-and-_ _ranking architecture that works at massive scale: billions of videos are indexed for bil‐_ _lions of users, handling millions of requests per second at very low latency._
**図15-1. TikTokのパーソナライズドレコメンダーサービスは、膨大なスケールで機能するretrieval-and-rankingアーキテクチャに基づいて構築されています: 数十億のビデオが数十億のユーザーのためにインデックスされ、非常に低いレイテンシで毎秒数百万のリクエストを処理します。**

<!-- ここまで読んだ! -->

The key systems challenges, some of which are covered in TikTok’s Monolith research paper, in building a personalized recommendation system at scale are:
スケールでパーソナライズされた推薦システムを構築する際の主要なシステムの課題のいくつかは、[TikTokのMonolith研究論文](https://oreil.ly/-oAdq)で取り上げられています。

- _Nonstationarity challenges_ User preferences and trending videos change continually, causing features to become stale in seconds and requiring models to be continually retrained.
_非定常性の課題_ **ユーザーの好みやトレンドのビデオは常に変化し、特徴が数秒で古くなり、モデルを継続的に再トレーニングする必要**があります。
When the environment is dynamic, your system needs to adapt constantly.
環境が動的な場合、システムは常に適応する必要があります。
At short timescales, this means having fresh precomputed features (stream processing) and real-time feature computation from request parameters.
**短い時間スケールでは、これは新鮮な事前計算された特徴（ストリーム処理）とリクエストパラメータからのリアルタイム特徴計算を持つこと**を意味します。
At longer time‐ [scales, this means retraining models frequently to prevent concept drift.
長い時間スケールでは、これは概念の漂流を防ぐためにモデルを頻繁に再トレーニングすることを意味します。
TikTok](https://oreil.ly/vuxew) [uses Flink to achieve subsecond streaming feature computation from user actions](https://oreil.ly/vuxew) (clicks, likes, etc.) and Cassandra (key-value store) and Redis (cache) for realtime feature serving.
TikTokは、ユーザーアクションからのサブ秒ストリーミング特徴計算を実現するためにFlinkを使用し](https://oreil.ly/vuxew) (クリック、いいねなど) 、リアルタイム特徴提供のためにCassandra（キー・バリューストア）とRedis（キャッシュ）を使用しています。
TikTok’s monolith also includes continual retraining of the models (once per minute), but we can simplify to scheduling batch training jobs that run every hour.
**TikTokのモノリスは、モデルの継続的な再トレーニング（1分ごと）も含まれていますが、毎時実行されるバッチトレーニングジョブをスケジュールすることで簡略化**できます。

<!-- ここまで読んだ! -->

---

_Sparse-feature challenges_ Most user and video features are high-cardinality categorical variables, which, in their raw form, are extremely sparse.
_スパースフィーチャーの課題_ **ほとんどのユーザーおよびビデオの特徴は高次元のカテゴリ変数であり、生の形では非常にスパース**です。
For example, recommender systems have typically stored viewing histories as one-hot vectors, where a _1 indicates that a_ user has watched a video and a 0 indicates that the user hasn’t watched it.
たとえば、レコメンダーシステムは通常、視聴履歴をワンホットベクトルとして保存しており、_1はユーザーがビデオを視聴したことを示し、0はユーザーが視聴していないことを示します。
This leads to extremely high-dimensional and mostly zero-valued (sparse) matrices, and techniques like collaborative filtering and factorization machines don’t scale to work with the increased memory and computational complexity required.
これにより、非常に高次元でほとんどゼロ値（スパース）の行列が生成され、コラボレーティブフィルタリングやファクタリゼーションマシンのような技術は、必要なメモリと計算の複雑さの増加に対応するためにスケールしません。
There is also a cold-start problem with sparse features, as they mean there’s little to no data for those entities, making it difficult to generate good recommendations.
スパースフィーチャーにはコールドスタートの問題もあり、それらのエンティティに対するデータがほとんどないため、良い推薦を生成することが難しくなります。
Models tend to recommend only popular items, neglecting the “long tail” of lessinteracted items, which reduces recommendation diversity and serendipity.
モデルは人気のあるアイテムのみを推薦する傾向があり、相互作用の少ないアイテムの「ロングテール」を無視するため、推薦の多様性と偶然性が減少します。
Sparse features can lead to overfitting because models might “memorize” rare user-item interactions instead of generalizing.
スパースフィーチャーは、モデルが一般化するのではなく、稀なユーザー-アイテムの相互作用を「記憶」する可能性があるため、過剰適合を引き起こす可能性があります。
Neural networks typically require dense representations, but raw interaction data is sparse.
ニューラルネットワークは通常、密な表現を必要としますが、生の相互作用データはスパースです。
We will solve the sparsefeature data problem using embeddings.
**私たちは、埋め込みを使用してスパースフィーチャーデータの問題を解決します。**
_Embeddings convert high-dimensional_ sparse features into low-dimensional dense vectors.
**_埋め込みは高次元の_ スパースフィーチャーを低次元の密なベクトルに変換**します。
However, we have the chal‐ lenge of connecting two different data sources: user behavior data and video data.
**ただし、ユーザー行動データとビデオデータという2つの異なるデータソースを接続するという課題**があります。
We will address this by training two models (a user-embedding model and a video-embedding model) in a single _two-tower architecture (see next section)_ with interaction data (user events like watching/liking/etc. videos).
私たちは、**インタラクションデータ（視聴/いいねなどのユーザーイベント）を使用して、単一の_two-tower architecture_で2つのモデル（ユーザー埋め込みモデルとビデオ埋め込みモデル）をトレーニングすることでこれに対処**します。(特徴量生成と変換としてTwo-towerモデルってことかな...??]]):thinking:

---

<!-- ここまで読んだ -->

_Retrieval challenges_ We will retrieve hundreds of candidate videos from a catalog containing billions of videos in a few milliseconds, using similarity search with a vector index.
_リトリーバルの課題_ 数十億のビデオを含むカタログから数百の候補ビデオを数ミリ秒で取得します。ベクトルインデックスを使用した類似性検索を利用します。
We will build a vector index that indexes all of the videos in our system, using the video embedding model, which is trained in our two-tower architecture.
私たちは、私たちのシステム内のすべてのビデオをインデックスするベクトルインデックスを構築します。これは、**私たちのtwo-tower architectureでトレーニングされたビデオ埋め込みモデルを使用**します。
We will take a user action, along with user history data, and create a vector embedding with the user embedding model.
ユーザーアクションとユーザー履歴データを取り込み、ユーザー埋め込みモデルを使用してベクトル埋め込みを作成します。
We will take a user action, along with user history data, and create a vector embedding with the user embedding model. 
ユーザーのアクションとユーザーの履歴データを取り込み、ユーザー埋め込みモデルを使用してベクトル埋め込みを作成します。
We will query the vector index with the user embedding to find the “nearest” videos. 
ユーザー埋め込みを使用してベクトルインデックスを照会し、「最も近い」動画を見つけます。
Nearest is based on the interaction data— given this user query and history, these are the videos that the user is most likely to click on or watch the longest (you can decide what to optimize for when building your two-tower embedding architecture). 
「最も近い」とは、インタラクションデータに基づいています。このユーザーのクエリと履歴を考慮すると、**ユーザーが最もクリックする可能性が高い、または最も長く視聴する動画**です（2タワー埋め込みアーキテクチャを構築する際に最適化する内容を決定できます）。

<!-- ここまで読んだ! -->

-----

_Personalized ranking challenges_ 
_パーソナライズされたランキングの課題_
The retrieval phase returns hundreds of candidate videos to ensure relevant items are included. 
取得フェーズでは、関連するアイテムが含まれるように、数百の候補動画を返します。
That is, it should have high recall. 
つまり、高いリコール率を持つ必要があります。
We then need to improve the precision and utility of the recommendations by rank-ordering so that the engaging/relevant videos appear at the top. 
次に、エンゲージメントの高い/関連性のある動画が上位に表示されるように、ランキングを行うことで推薦の精度と有用性を向上させる必要があります。
The objective should be to learn a ranking function that orders items for each user based on a desired metric. 
**目標は、各ユーザーに対してアイテムを所望のメトリックに基づいて順序付けるランキング関数を学習すること**です。
For example, if you want to optimize for the user engaging with the video, then the highest-probability videos should appear at the very top of each user’s recommended item list(s). 
例えば、ユーザーが動画にエンゲージすることを最適化したい場合、最も高い確率の動画が各ユーザーの推薦アイテムリストの最上部に表示されるべきです。
Note that in 2012, YouTube benefited significantly by changing from optimizing for users clicking on videos (view count) to how long users watch the recommended videos (watch time). 
2012年にYouTubeは、ユーザが動画をクリックすること（視聴回数）を最適化するのから、ユーザーが推薦された動画をどれだけ長く視聴するか（視聴時間）に変更することで大きな利益を得ました。
Ranking typically uses a low-latency model, such as XGBoost, and real-time features that capture recent trends. 
**ランキングは通常、XGBoostのような低遅延モデルと、最近のトレンドを捉えるリアルタイム特徴量を使用**します。

<!-- ここまで読んだ! -->

_Scalability challenges_ 
_スケーラビリティの課題_
The system needs to be able to handle millions of concurrent requests and store PBs of data, and it requires compute- and memory-efficient design as well as a highly available architecture to prevent downtime. 
システムは、数百万の同時リクエストを処理し、PB単位のデータを保存できる必要があり、ダウンタイムを防ぐために計算およびメモリ効率の良い設計と高可用性のアーキテクチャが必要です。
For the retrieval phase, we will use Hopsworks’ vector index (OpenSearch), which is partitioned over nodes and replicated for high availability. 
取得フェーズでは、Hopsworksのベクトルインデックス（OpenSearch）を使用します。これはノードに分割され、高可用性のために複製されていま
It scales to store massive volumes of data (up to PB scale) and thousands of concurrent requests. 
これは、膨大なデータ量（PBスケールまで）と数千の同時リクエストを処理するためにスケールします。
The latency will depend on the size of the vector index (number of entries), the size of the vector embeddings, whether they are stored in memory or on disk, and the storage configuration in the Facebook AI Similarity Search (FAISS) engine. 
レイテンシは、ベクトルインデックスのサイズ（エントリ数）、ベクトル埋め込みのサイズ、メモリまたはディスクに保存されているかどうか、およびFacebook AI Similarity Search（FAISS）エンジンのストレージ構成に依存します。
Latencies under 10 ms are possible, and you will need to apply tricks to keep them that low for massive data volumes. 
10ms未満のレイテンシは可能であり、大量のデータ量に対してそれを維持するための工夫が必要です。
The ranking phase will need to retrieve precomputed features for candidate videos. 
ランキングフェーズでは、候補動画のために事前計算された特徴を取得する必要があります。
This means hundreds of key-value lookups in a single batch. 
これは、単一のバッチ内で数百のキー-バリューのルックアップを意味します。
We will use Hopsworks’ feature store, built on RonDB, to retrieve a batch in 10–20 ms (p99), which can scale to handle tens of thousands of concurrent batch requests. 
私たちは、RonDB上に構築されたHopsworksのフィーチャーストアを使用して、10〜20ms（p99）でバッチを取得し、数万の同時バッチリクエストを処理できるようにスケールします。

<!-- ここまで読んだ! -->

---

_Data source challenges_ 
_データソースの課題_
We need user profile data, video data, and interaction data to build our personalized video player. 
パーソナライズされたビデオプレーヤーを構築するために、ユーザープロファイルデータ、ビデオデータ、およびインタラクションデータが必要です。
Given the lack of quality open source datasets, we will create synthetic data simulating user interactions with videos. 
質の高いオープンソースデータセットが不足しているため、ユーザーが動画とインタラクションする様子をシミュレートした合成データを作成します。
The most important data source for learning user viewing behavior is the interactions between users and videos. 
ユーザーの視聴行動を学習するための最も重要なデータソースは、ユーザーと動画の間のインタラクションです。

<!-- ここまで読んだ! -->

---

Figure 15-2 shows both positive interactions (such as views and likes) and negative interactions (such as ignoring a recommended video). 
図15-2は、ポジティブなインタラクション（視聴やいいねなど）とネガティブなインタラクション（推薦された動画を無視するなど）の両方を示しています。
We will train embedding models for the retrieval phase that help predict what video a user is likely to watch/like, given their long-term viewing behavior, their recent short-term viewing behavior, and the current viewing behavior of other users. 
私たちは、ユーザーの長期的な視聴行動、最近の短期的な視聴行動、および他のユーザーの現在の視聴行動を考慮して、ユーザーが視聴/いいねする可能性のある動画を予測するのに役立つretrieveフェーズのための埋め込みモデルを訓練します。

![]()
_Figure 15-2. Interaction data is collected from events such as video watch, no-watch, likes, and shares._ 
_図15-2. インタラクションデータは、動画視聴、未視聴、いいね、シェアなどのイベントから収集されます。_

We will assign an interaction_score for a user interaction with videos that are recommended to the user: 
**ユーザーに推薦された動画とのユーザーインタラクションに対してinteraction_scoreを割り当て**ます: 
(複数のリアクションの重みづけ和を使って合成報酬スコアを作るのかな...??:thinking:)

- 0: The user _did not watch the recommended video (or swiped away the video within a very short period of time). 
0: ユーザーは_推薦された動画を視聴しなかった（または非常に短い時間内に動画をスワイプした）

- 1: The user watched the recommended video. 
1: ユーザーは推薦された動画を視聴しました。

- 2: The user liked the recommended video. 
2: ユーザーは推薦された動画にいいねをしました。

- 3: The user shared the recommended video. 
3: ユーザーは推薦された動画をシェアしました。

If the user watches a video, we will also measure the watch_time (the length of time the user watched the video for) by computing the time between watching two videos (you could also add a stop watching event, but most viewers will just swipe between videos). 
**ユーザーが動画を視聴した場合、2つの動画を視聴する間の時間を計算することでwatch_time（ユーザーが動画を視聴した時間の長さ）を測定します（視聴を停止するイベントを追加することもできますが、ほとんどの視聴者は動画間をスワイプするだけです）。**
In the next section, you will design your own personalized, real-time AI-powered recommendation system based on this retrieval-and-ranking architecture, including the data model and the FTI pipelines. 
次のセクションでは、この取得とランキングのアーキテクチャに基づいて、データモデルやFTIパイプラインを含む、独自のパーソナライズされたリアルタイムAI駆動の推薦システムを設計します。

<!-- ここまで読んだ! -->

-----
(コラム)
Google popularized the retrieval-and-ranking architecture for personalized recommendations in [“Deep Neural Networks for](https://oreil.ly/nvvyj) [YouTube Recommendations”, published at RecSys 2016. 
Googleは、2016年にRecSysで発表された「YouTube Recommendationsのための深層ニューラルネットワーク」において、パーソナライズされた推薦のためのretrieveとランキングのアーキテクチャを普及させました。
In 2025, Netflix introduced a foundation transformer model for predicting the user’s next interaction. 
2025年、Netflixはユーザーの次のインタラクションを予測するための**基盤トランスフォーマーモデル**を導入しました。
(Transformer4Rec的なやつかな...!!:thinking:)
It will be interesting to see if transformers can disrupt recommendation models in the same way they have disrupted NLP. 
3. トランスフォーマーがNLPを破壊したのと同じように、推薦モデルを破壊できるかどうかを見るのは興味深いでしょう。
---

## 3. Real-Time Personalized Recommender リアルタイムパーソナライズドレコメンダー

The starting point for your personalized video recommendation system is to build an MVPS (see Chapter 2). 
パーソナライズされた動画推薦システムの出発点は、MVPSを構築することです（第2章を参照）。
The kanban board in Figure 15-3 shows different technologies for the FTI pipelines, the data sources (a Kafka topic and external lakehouse tables), and the prediction consumer—personalized recommendations for a video player. 
図15-3のカンバンボードは、FTIパイプラインのためのさまざまな技術、データソース（Kafkaトピックと外部レイクハウステーブル）、および予測消費者—動画プレーヤーのためのパーソナライズされた推薦を示しています。
For your feature pipelines, you will need stream processing (Feldera), batch processing (Polars), and vector-embedding (PySpark) pipelines. 
フィーチャーパイプラインには、ストリーム処理（Feldera）、バッチ処理（Polars）、およびベクトル埋め込み（PySpark）パイプラインが必要です。

![]()
_Figure 15-3. Kanban board for your minimal viable video recommender system._ 
_図15-3. 最小限の実行可能な動画レコメンダーシステムのためのカンバンボード。_

<!-- ここまで読んだ! -->

We chose these data transformation frameworks because Feldera and Polars have the easiest learning curve and scale to handle our expected load (millions of users), and we will use PySpark to compute vector embeddings as backfilling vector embeddings from video data is computationally intensive and PySpark can be scaled out to run on many nodes. 
私たちは、FelderaとPolarsが最も学習曲線が緩やかで、予想される負荷（数百万のユーザー）を処理するためにスケールするため、これらのデータ変換フレームワークを選びました。また、PySparkを使用してベクトル埋め込みを計算します。動画データからのベクトル埋め込みのバックフィルは計算集約的であり、PySparkは多くのノードで実行するためにスケールできます。
We will use the two-tower model, with the TensorFlow Recommenders library, for training the user-embedding model and the video-embedding model for our retrieval system. 
私たちは、取得システムのためにユーザー埋め込みモデルと動画埋め込みモデルを訓練するために、**TensorFlow Recommendersライブラリを使用して2タワーモデルを使用**します。
(これいいのかな...!!:thinking:)
TensorFlow Recommenders has built-in support for training two-tower embedding models. 
TensorFlow Recommendersは、2タワー埋め込みモデルの訓練をサポートしています。
We will use XGBoost as our ranking model due to its good performance and low-latency for predictions. 
**予測の良好なパフォーマンスと低遅延のため、XGBoostをランキングモデルとして使用**します。
We will host our online inference pipeline as a Python server (FastAPI) in KServe, and it will be called via a REST API from the video player application. 
私たちは、KServe内のPythonサーバー（FastAPI）としてオンライン推論パイプラインをホストし、動画プレーヤーアプリケーションからREST APIを介して呼び出されます。
We will run the pipelines and deploy the models on Hopsworks. 
私たちはパイプラインを実行し、Hopsworks上にモデルをデプロイします。

---
(コラム)
Large companies, such as Netflix, use this _retrieval-and-ranking_ architecture for both personalized recommendations and search— “a single contextual recommendation system that can serve all search and recommendation tasks.” 
Netflixのような大企業は、この_retrieve-and-rankingアーキテクチャをパーソナライズされた推薦と検索の両方に使用しています—「[すべての検索と推薦タスクに対応できる単一の文脈的推薦システム](https://www.infoq.com/presentations/recommender-search-ranking/)」。
Netflix has recommendation systems, PreQuery and MoreLikeThis, and a search system built on the same retrieval-and-ranking infrastructure using many of the same data sources and features. 
Netflixには、PreQueryやMoreLikeThisといった推薦システムがあり、**同じデータソースや特徴量を使用して同じretrieve-and-rankingインフラストラクチャに基づいた検索システム**があります。
A unified platform reduces maintenance costs and enables innovation in search or recommendations to also improve the other. 
統一されたプラットフォームはメンテナンスコストを削減し、検索や推薦の革新が他の改善にもつながることを可能にします。

---

<!-- ここまで読んだ! -->

In the following sections, we will go through the ML pipelines, but first we will design our system architecture, from our data sources to the type of feature pipeline (batch or streaming), the feature groups, and the feature views that we will need for our models. 
次のセクションではMLパイプラインを通じて進めますが、まずはデータソースからフィーチャーパイプラインの種類（バッチまたはストリーミング）、フィーチャーグループ、モデルに必要なフィーチャービューまで、システムアーキテクチャを設計します。
Figure 15-4 shows that our MVPS will need four feature groups and two feature views and will create three models. 
図15-4は、私たちのMVPSが4つのフィーチャーグループと2つのフィーチャービューを必要とし、3つのモデルを作成することを示しています。

![]()
_Figure 15-4. Feature groups, feature views, and models for our video recommender._ 
_図15-4. 私たちの動画レコメンダーのためのフィーチャーグループ、フィーチャービュー、およびモデル。_

The figure shows the interaction data arriving in Kafka, a streaming feature pipeline to compute aggregated viewing statistics, batch pipelines to compute user profile, video attributes, and ranking feature data. 
この図は、Kafkaに到着するインタラクションデータ、集約視聴統計を計算するためのストリーミングフィーチャーパイプライン、ユーザープロファイル、動画属性、およびランキングフィーチャーデータを計算するためのバッチパイプラインを示しています。
These feature groups include vector embeddings and some real-time features. 
これらのフィーチャーグループには、ベクトル埋め込みといくつかのリアルタイム特徴量が含まれています。
Our retrieval system is based on a vector index and requires two embedding models—one for user data and one for video data—and we create a retrieval feature view for those models. 
私たちのretrieveシステムはベクトルインデックスに基づいており、ユーザーデータ用とビデオデータ用の2つの埋め込みモデルが必要です。そして、これらのモデルのためにretrieveフィーチャービューを作成します。
For the ranking model, we also create a ranking feature view. 
ランキングモデルのためにも、ランキングフィーチャービューを作成します。

The code for our pipelines and instructions for how to run the ML pipelines are in the book’s source code repository. 
私たちのパイプラインのコードとMLパイプラインを実行する方法の指示は、[本のソースコードリポジトリにあります。](https://github.com/featurestorebook/mlfs-book)
We will now look at how to implement the FTI pipelines for our recommender system. 
これから、私たちのレコメンダーシステムのためのFTIパイプラインを実装する方法を見ていきます。

<!-- ここまで読んだ! -->

### 3.1. Feature Pipelines フィーチャーパイプライン

We start with the interaction data that arrives as events in a Kafka topic generated by all the video player applications. 
私たちは、すべての動画プレーヤーアプリケーションによって生成されたKafkaトピック内の**イベントとして到着するインタラクションデータから始めます。**
We assume there is an external event-sourcing pipeline that stores historical interaction events in a lakehouse table. 
外部のイベントソーシングパイプラインがあり、歴史的なインタラクションイベントをレイクハウステーブルに保存していると仮定します。
In the source code repository, we create synthetic interaction data and write it to a Kafka topic. 
ソースコードリポジトリ内で、合成インタラクションデータを作成し、それをKafkaトピックに書き込みます。
The same code can also backfill an `interaction_fg feature group with historical interaction` data. 
同じコードは、interaction_fgフィーチャーグループに歴史的インタラクションデータをバックフィルすることもできます。
The user profile data will be updated by users in the video player application. 
ユーザープロファイルデータは、動画プレーヤーアプリケーション内のユーザーによって更新されます。
The video attributes will be updated by batch pipelines that run periodically to process new videos uploaded by users. 
動画属性は、ユーザーによってアップロードされた新しい動画を処理するために定期的に実行されるバッチパイプラインによって更新されます。
Figure 15-4 also shows the classes of feature pipelines (batch, streaming, vector embedding) for the feature groups. 
図15-4は、フィーチャーグループのためのフィーチャーパイプラインのクラス（バッチ、ストリーミング、ベクトル埋め込み）も示しています。
Again, we have synthetic data generation programs to create this data. 
再度、私たちはこのデータを生成するための**合成データ生成プログラム**を持っています。
The prompts for creating the synthetic data generation programs are in the book’s source code repository. 
合成データ生成プログラムを作成するためのプロンプトは、本のソースコードリポジトリにあります。
The feature groups will all be both offline and online. 
**フィーチャーグループはすべてオフラインとオンラインの両方で使用**されます。
Offline data is used for training, and online data is used for the retrieval and ranking phases. 
オフラインデータは訓練に使用され、オンラインデータは取得とランキングのフェーズに使用されます。
We will need a streaming-feature pipeline to compute windowed aggregations for videos (video_stats_fg): 
動画のウィンドウ集計を計算するためにストリーミングフィーチャーパイプラインが必要です（video_stats_fg）：

``` 
cnt_views_last_{h/d/w/m} 
``` 
The number of views for a video in the previous hour, day, week, and month 
前の1時間、1日、1週間、1ヶ月の動画の視聴回数

``` 
ctr 
``` 
The click-through rate for the previous hour, day, week, and month 
前の1時間、1日、1週間、1ヶ月のクリック率

And to compute state for user viewing history (user_activity_fg): 
ユーザーの視聴履歴の状態を計算するために（user_activity_fg）：

``` 
recently_viewed 
``` 
The N most recently viewed videos for each user 
各ユーザーの最近視聴したN本の動画

``` 
last_login 
``` 
The timestamp for when the user last logged in 
ユーザーが最後にログインした時刻のタイムスタンプ

``` 
mean_session_duration 
``` 
The average duration of a user session for the last week 
過去1週間のユーザーセッションの平均時間

``` 
std_session_duration 
``` 
The standard deviation for user session durations for the last week 
過去1週間のユーザーセッションの時間の標準偏差

<!-- ここまで読んだ! -->

We will use Feldera to compute the streaming-feature pipelines, which can also be run in backfill mode to process historical interaction data.
私たちは、Felderを使用してストリーミングフィーチャーパイプラインを計算します。これらは、バックフィルモードで実行して、過去のインタラクションデータを処理することもできます。
The features for videos (excluding video usage statistics) are stored in `video_attrs_fg`. 
動画の特徴（動画使用統計を除く）は、`video_attrs_fg`に保存されています。
It contains features such as the video name, description, genre, and rating that are taken from the videos table in the lakehouse. 
それには、レイクハウスの動画テーブルから取得された動画名、説明、ジャンル、評価などの特徴が含まれています。
It also contains the vector index used for similarity search in our retrieval stage. 
**また、retrieve段階での類似性検索に使用されるベクトルインデックスも含まれています**。(ベクトルを他の特徴量と一緒のfeature groupに入れるのか、どうなんだろ...:thinking:)
You need to periodically update `video_attrs_fg` with a batch vector embedding pipeline, as shown in Figure 15-5.
`video_attrs_fg`をバッチベクトル埋め込みパイプラインで定期的に更新する必要があります。これは、図15-5に示されています。

![]()
_Figure 15-5. The vector-embedding pipeline periodically updates the vector index with new videos and new video statistics._
_図15-5. ベクトル埋め込みパイプラインは、新しい動画と新しい動画統計でベクトルインデックスを定期的に更新します。_

<!-- ここまで読んだ! -->

We compute the vector embedding using the vector-embedding model (trained on our interaction data, see the next section) with inputs from `videos (name, description, genre, length, rating)` as well as video viewing statistics from `video_stats_fg.` 
私たちは、`videos (name, description, genre, length, rating)`からの入力と、`video_stats_fg`からの動画視聴統計を使用して、インタラクションデータで訓練されたベクトル埋め込みモデルを使用してベクトル埋め込みを計算します。
This combination of features allows our retrieval stage to select videos based not only on their static properties (name, description, genre, rating) but also on dynamic properties, such as their trending score. 
この特徴の組み合わせにより、取得段階では、静的特性（名前、説明、ジャンル、評価）だけでなく、トレンドスコアなどの動的特性に基づいて動画を選択できます。
What if the popularity of a video changes suddenly? 
もし動画の人気が突然変わったらどうなるでしょうか？
The retrieval phase will only adapt to changes in video popularity when the vector index entries are updated. 
**取得フェーズは、ベクトルインデックスのエントリが更新されたときにのみ、動画の人気の変化に適応します。**
Dynamic properties also increase both the write load on the vector index and the compute requirements for the pipeline. 
動的特性は、ベクトルインデックスへの書き込み負荷とパイプラインの計算要件の両方を増加させます。
You may benefit from a GPU in your pipeline program, as it should produce a ~10x throughput improvement in computing vector embeddings over CPUs. 
パイプラインプログラムでGPUを使用すると、CPUに比べてベクトル埋め込みの計算で約10倍のスループット向上が得られる可能性があります。
However, your pipeline may then be bottlenecked on writing to your vector index. 
しかし、その場合、パイプラインはベクトルインデックスへの書き込みでボトルネックになる可能性があります。
For example, Hopsworks uses OpenSearch’s vector index, which can handle a few tens of thousands of updates/sec with the bulk API. 
例えば、HopsworksはOpenSearchのベクトルインデックスを使用しており、バルクAPIを使用して数万の更新/秒を処理できます。
If we run a Spark vector-embedding pipeline with a bunch of workers, we probably don’t need GPUs, as OpenSearch will be the bottleneck and adding GPUs would not make updates go faster. 
もし、複数のワーカーでSparkのベクトル埋め込みパイプラインを実行する場合、OpenSearchがボトルネックになるため、GPUは必要ないでしょう。GPUを追加しても更新が速くなることはありません。
For example, if you have 100M videos and you can make 10K updates/sec, it will take 150 minutes to update all entries. 
例えば、1億本の動画があり、1秒あたり1万の更新が可能な場合、すべてのエントリを更新するのに150分かかります。
This creates an upper bound on how often you can refresh the vector index. 
これにより、ベクトルインデックスをどのくらいの頻度で更新できるかの上限が設定されます。

<!-- ここまで読んだ! -->

However, you probably don’t need to update all entries for every incremental update—you may set a threshold for changes in a video’s popularity and only update the entry if a video’s popularity moves above/below the threshold. 
ただし、すべての増分更新のためにすべてのエントリを更新する必要はないでしょう。動画の人気の変化に対してしきい値を設定し、動画の人気がそのしきい値を超えた場合のみエントリを更新することができます。
This will reduce the number of videos to be updated by a couple of orders of magnitude, allowing you to update your entries at a much higher cadence. 
これにより、更新する動画の数が数桁減少し、エントリをはるかに高い頻度で更新できるようになります。

<!-- ここまで読んだ! -->

The other batch feature pipeline updates `user_profile_fg (location, age, gender, etc.)` with mostly static features computed from a users lakehouse table and limited feature engineering (for example, date of birth is transformed into age). 
もう一つのバッチフィーチャーパイプラインは、主にユーザのレイクハウステーブルから計算された静的特徴と限られた特徴エンジニアリング（例えば、生年月日を年齢に変換）を使用して、`user_profile_fg (location, age, gender, etc.)`を更新します。
The feature group is online, as we will use its precomputed features in the online inference pipeline. 
このフィーチャーグループはオンラインであり、オンライン推論パイプラインでその事前計算された特徴を使用します。
This pipeline can be scheduled daily for incremental updates, due to its slowly changing nature, but it can also be run in backfill mode. 
このパイプラインは、ゆっくりと変化する性質のため、増分更新のために毎日スケジュールできますが、バックフィルモードでも実行できます。
For this feature pipeline and the previous feature pipelines, you should add data validation rules, such as with Great Expectations from Chapter 8. 
このフィーチャーパイプラインと前のフィーチャーパイプラインには、Chapter 8のGreat Expectationsを使用してデータ検証ルールを追加する必要があります。
For example, the user profile and video attributes should not have missing values. 
例えば、ユーザープロファイルと動画属性には欠損値があってはなりません。

From these feature groups, we can create feature views containing the features that will be used by our three models: the user-/query-embedding model, the video-embedding model, and the ranking model. 
これらのフィーチャーグループから、ユーザ/クエリ埋め込みモデル、動画埋め込みモデル、ランキングモデルで使用される特徴を含むフィーチャービューを作成できます。

<!-- ここまで読んだ! -->

### 3.2. Training Pipelines トレーニングパイプライン

We will train our user-embedding and video-embedding models using a single training dataset constructed from the four different feature groups. 
私たちは、4つの異なるフィーチャーグループから構築された単一のトレーニングデータセットを使用して、ユーザ埋め込みモデルと動画埋め込みモデルを訓練します。
For this, we create a feature view, starting from our interaction dataset, mounted as an external `interactions` feature group, which stores our label, interaction_score, and foreign keys to user_id and video_id. 
そのために、インタラクションデータセットから始めて、外部の`interactions`フィーチャーグループとしてマウントされたフィーチャービューを作成します。このフィーチャーグループには、ラベル、interaction_score、user_idおよびvideo_idへの外部キーが保存されています。
We create our feature view by joining in further features from the user_profile_fg, video_attrs_fg, video_stats_fg, and user_activity_fg. 
user_profile_fg、video_attrs_fg、video_stats_fg、およびuser_activity_fgからさらに特徴を結合することで、フィーチャービューを作成します。

<!-- ここまで読んだ! -->

Similarly, we create ranking_fv starting from interactions, where we again use the interaction_score as our label. 
同様に、interactionsから始めてranking_fvを作成し、**再びinteraction_scoreをラベルとして使用**します。
We can use many of the same features, but also real-time features, including on-demand features and features computed in streaming feature pipelines. 
同じ特徴の多くを使用できますが、オンデマンド機能やストリーミングフィーチャーパイプラインで計算された特徴量など、リアルタイムの特徴も含めることができます。
The ranking model can react faster to changes in trending videos and user behavior. 
ランキングモデルは、トレンド動画やユーザーの行動の変化により迅速に反応できます。
Figure 15-6 shows how the retrieval-and-ranking feature views are used to create training data for the embedding models and ranking model, respectively.
図15-6は、取得およびランキングフィーチャービューがそれぞれ埋め込みモデルとランキングモデルのトレーニングデータを作成するためにどのように使用されるかを示しています。

![]()
_Figure 15-6. Create training datasets using feature views over existing feature groups_ _(tables). Register models with the model registry._
_Figure 15-6. 既存のフィーチャーグループ（テーブル）に対するフィーチャービューを使用してトレーニングデータセットを作成します。モデルをモデルレジストリに登録します。_

We materialize the training data as CSV files from the feature store, as the data volumes may be too large to store in memory in the training pipeline.
**トレーニングデータは、データボリュームがトレーニングパイプラインのメモリに保存するには大きすぎる可能性があるため、フィーチャーストアからCSVファイルとして具現化**します。
(つまり全件メモリには載せないってことか...!:thinking:)

<!-- ここまで読んだ! -->

#### 3.2.1. Two-tower embedding model ツータワー埋め込みモデル

So far in this book, we have only looked at pretrained embedding models, such as sentence-transformers that transform text into a dense vector representation with a dimension d—the length of the array of floats.
これまでのところ、本書では、テキストを密なベクトル表現に変換するsentence-transformers のような事前学習済みの埋め込みモデルのみを見てきました。これは、次元$d$、すなわち浮動小数点数の配列の長さです。

We want to train our own custom embedding models with the two-tower model architecture, using the interaction data, user data, and video data.
**私たちは、インタラクションデータ、ユーザーデータ、ビデオデータを使用して、ツータワーモデルアーキテクチャで独自のカスタム埋め込みモデルをトレーニングしたい**と考えています。
The interaction data tells us that a user with a certain profile and watch history watched a video with a genre, description, and popularity.
インタラクションデータは、特定のプロファイルと視聴履歴を持つユーザーが、ジャンル、説明、人気を持つビデオを視聴したことを示しています。
The interaction data should also include negative samples where the user didn’t watch this video, as well as when the user liked or shared a video.
**インタラクションデータには、ユーザーがこのビデオを視聴しなかった場合のネガティブサンプルや、ユーザーがビデオを「いいね」したり共有した場合も含めるべき**です。
We will use the interaction data, along with user and video features, to train two different embedding models that link these two different modalities together: users and videos.
私たちは、インタラクションデータとユーザーおよびビデオの特徴を使用して、これら2つの異なるモダリティ（ユーザーとビデオ）を結びつける2つの異なる埋め込みモデルをトレーニングします。

<!-- ここまで読んだ! -->

The two-tower model architecture takes as input samples (rows) from the user-video interaction dataset along with the score of each interaction as the label for the sample.
ツータワーモデルアーキテクチャは、ユーザー-ビデオインタラクションデータセットからのサンプル（行）を入力として受け取り、**各インタラクションスコアをサンプルのラベルとして使用**します。
We will prepare the training dataset so that we join in columns for:
トレーニングデータセットを準備し、以下の列を結合します：

_User features_ From the user profile and user watch history
_ユーザー特徴_ ユーザープロファイルとユーザー視聴履歴から

_Video features_ Profile, viewing statistics, and videos
_ビデオ特徴_ プロファイル、視聴統計、およびビデオ

The user and video features are fed into two separate neural networks (towers), one for the user features and one for the video features.
ユーザー特徴とビデオ特徴は、それぞれユーザー特徴用とビデオ特徴用の2つの別々のニューラルネットワーク（タワー）に供給されます。
Some examples of features and layers that can be included in each tower are:
各タワーに含めることができる特徴量やレイヤーのいくつかの例は次のとおりです：

_User embedding layer_ User IDs and user categorical features
_ユーザー埋め込みレイヤー_ ユーザーIDとユーザーのカテゴリカル特徴

_Video embedding layer_ Video IDs and video categorical features
_ビデオ埋め込みレイヤー_ ビデオIDとビデオのカテゴリカル特徴

_Feedforward layers_ Normalized numerical features like user age and video length
_フィードフォワードレイヤー_ ユーザーの年齢やビデオの長さのような正規化された数値特徴

_Transformer block_ Text features, like video descriptions, and sequential features, like user history
_トランスフォーマーブロック_ ビデオの説明のようなテキスト特徴や、ユーザー履歴のようなシーケンス特徴

_CNN_ Image features
_CNN_ 画像特徴

The user tower takes the user features, a user entry, and processes them through any initial layers to the embedding layers (embedding lookup tables for user and video IDs) and then feedforward layers to output a single vector: the user embedding of length _d.
ユーザータワーは、ユーザー特徴、ユーザーエントリを受け取り、初期レイヤーを経て埋め込みレイヤー（ユーザーおよびビデオIDのための埋め込みルックアップテーブル）に処理し、その後フィードフォワードレイヤーを通じて単一のベクトルを出力します：長さ$d$のユーザー埋め込みです。
The video tower takes the video features, a video entry, processes them through initial layers to embedding layers and then feedforward layers, to output a video embedding of length d.
ビデオタワーは、ビデオ特徴、ビデオエントリを受け取り、初期レイヤーを経て埋め込みレイヤーに処理し、その後フィードフォワードレイヤーを通じて長さ$d$のビデオ埋め込みを出力します。
Figure 15-7 shows the architecture, from the training data, to the two embedding towers, to output and loss function.
図15-7は、トレーニングデータから2つの埋め込みタワー、出力および損失関数までのアーキテクチャを示しています。

![]()
_Figure 15-7. User-video interaction data is enriched with user and video features and is_ _training data for the two-tower embedding model architecture._
_Figure 15-7. ユーザー-ビデオインタラクションデータは、ユーザーおよびビデオ特徴で強化され、ツータワー埋め込みモデルアーキテクチャのトレーニングデータです。_

<!-- ここまで読んだ! -->

The user embedding and video embeddings are compared using a similarity function, such as the dot product or cosine similarity.
ユーザー埋め込みとビデオ埋め込みは、内積やコサイン類似度などの類似度関数を使用して比較されます。
We collapse the output into one of two classes: positive = strong or weak engagement (1, 2, 3) or negative = no engagement (0).
**出力を2つのクラスのいずれかにまとめます：ポジティブ = 強いまたは弱いエンゲージメント（1, 2, 3）またはネガティブ = エンゲージメントなし（0）。**
(2値に集約するのかな?? それともこのまま学習させる??:thinking:)
The two-tower model is used in the retrieval phase, which is about finding any potentially interesting candidates to pass to the ranking stage.
ツータワーモデルは、ランキングステージに渡す可能性のある興味深い候補を見つけることに関するリトリーバルフェーズで使用されます。
Fine-grained preferences (such as “liked” versus “shared”) are better handled in the ranking model, which can take richer features and do personalized scoring.
細かい好み（「いいね」と「共有」のような）は、より豊富な特徴を取り入れ、パーソナライズされたスコアリングを行うランキングモデルでより良く処理されます。

The positive or negative outcome is compared with the binary label (positive or negative) using a contrastive loss function, such as information noise-contrastive estimation (InfoNCE) or sampled softmax.
ポジティブまたはネガティブの結果は、情報ノイズ対比推定（InfoNCE）やサンプリングソフトマックスのような対比損失関数を使用して、バイナリラベル（ポジティブまたはネガティブ）と比較されます。
The computed loss is used to update the weights in both the user tower and the video tower networks.
計算された損失は、ユーザータワーとビデオタワーネットワークの両方の重みを更新するために使用されます。
Larger losses will result in larger weight updates to drive the embedding towers to optimize the similarity scores so that positives are ranked above negatives.
大きな損失は、埋め込みタワーが類似度スコアを最適化し、ポジティブがネガティブよりも上位にランク付けされるように、より大きな重みの更新をもたらします。

---

Do we need negative sampling for recommendation models?
推薦モデルにネガティブサンプリングは必要ですか？
What if the recommendation service itself has not yet been launched and there is no interaction data?
もし推薦サービス自体がまだ開始されておらず、インタラクションデータがない場合はどうなりますか？
If you have some positive samples (viewed, liked), you can use a policy such as random sampling—combining user entries with random videos as negative data to bootstrap your training data.
もしいくつかのポジティブサンプル（視聴、いいね）がある場合、**ランダムサンプリングのようなポリシーを使用して、ユーザーエントリをランダムなビデオと組み合わせてネガティブデータとしてトレーニングデータをブートストラップすることができます。**

---

<!-- ここまで読んだ! -->

#### 3.2.2. Building the vector index of videos ビデオのベクトルインデックスの構築

Once the two-tower model is trained, you need to write a vector-embedding pipeline that can backfill the vector index from the interaction dataset and also incrementally process new entries in the interaction dataset.
ツータワーモデルがトレーニングされたら、インタラクションデータセットからベクトルインデックスをバックフィルし、インタラクションデータセットの新しいエントリを段階的に処理できる**ベクトル埋め込みパイプライン**を書く必要があります。
(まあ、アイテムタワーの推論パイプライン、とも言えるやつね。"vector-embedding pipeline"って名前で呼ぶのもありだな:...!:thinking:)
The vector-embedding pipeline will create a video vector embedding for each row it processes from the interaction dataset and write it to the vector index.
ベクトル埋め込みパイプラインは、インタラクションデータセットから処理する各行に対してビデオベクトル埋め込みを作成し、それをベクトルインデックスに書き込みます

When the recommender wants to retrieve candidate videos for a user query, it first computes the user vector embedding from the user features with the user embedding model.
レコメンダーがユーザークエリの候補ビデオを取得したい場合、最初にユーザー特徴からユーザー埋め込みモデルを使用してユーザーベクトル埋め込みを計算します。(この事例だと、ユーザembedding-はリアルタイムに計算する設計らしい...!:thinking:)
It then retrieves the top N (typically 50–1,000) candidate videos that are most similar to the provided user embedding, using ANN search on the vector index.
次に、ベクトルインデックス上でANN検索を使用して、提供されたユーザー埋め込みに最も類似した上位N（通常は50〜1,000）の候補ビデオを取得します。
The returned candidate videos should be ranked based using the ranking model.
返された候補ビデオは、ランキングモデルに基づいてランク付けされるべきです。

<!-- ここまで読んだ! -->

#### 3.2.3. Ranking model ランキングモデル

The ranking model takes as input the _N candidate videos and uses richer features,_ including explicit crossed features between user and video (which the two-tower model struggles with), to precisely rerank them.
ランキングモデルは、**N候補ビデオを入力として受け取り、ユーザとビデオの間の明示的な交差特徴を含むより豊富な特徴を使用して、正確に再ランク付けします（これはツータワーモデルが苦手とする部分**です）。
The ranker can also use more realtime features (on-demand or features computed in streaming feature pipelines), making them more reactive to recent changes in video popularity and user behavior.
ランカーは、よりリアルタイムの特徴（オンデマンドまたはストリーミングフィーチャーパイプラインで計算された特徴）を使用することもでき、ビデオの人気やユーザーの行動の最近の変化に対してより反応的になります。
For example, the ranking model sees “trending score” as one of many input features per video, and it learns how much “trending” matters for each user.
たとえば、**ランキングモデルは「トレンドスコア」を各ビデオの多くの入力特徴の1つとして見ており、「トレンド」が各ユーザーにとってどれほど重要であるかを学習**します。
The ranking model also needs both negative and positive samples (viewed and not viewed) and can predict more fine-grained interactions, such as likes and shares.
ランキングモデルは、ネガティブサンプルとポジティブサンプル（視聴されたものと視聴されていないもの）の両方が必要であり、いいねや共有などのより細かいインタラクションを予測できます。
Examples of rankers include Wide & Deep, DCN, and DeepFM.
ランカーの例には、Wide & Deep、DCN、DeepFMが含まれます。

<!-- ここまで読んだ! -->

One widely used metric for ranking is [normalized discounted cumulative gain](https://oreil.ly/r_D_W) [(NDCG). It compares rankings to an ideal order in which all relevant items are at the](https://oreil.ly/r_D_W) top of the list.
ランキングの一般的に使用される指標の1つは、[正規化割引累積利得](https://oreil.ly/r_D_W)（NDCG）です。これは、ランキングをすべての関連アイテムがリストの上部にある理想的な順序と比較します。
Another popular ranking metric is mean reciprocal rank (MRR).
もう1つの人気のあるランキング指標は、平均逆順位（MRR）です。
Mean average precision (MAP) at K is a ranking metric that helps evaluate the quality of ranking in recommender systems.
Kにおける平均平均精度（MAP）は、レコメンダーシステムにおけるランキングの質を評価するのに役立つランキング指標です。
It measures both the relevance of suggested items and how good the system is at placing more relevant items at the top.
これは、提案されたアイテムの関連性と、システムがより関連性の高いアイテムを上位に配置する能力の両方を測定します。

<!-- ここまで読んだ! -->

### 3.3. Online Inference Pipeline オンライン推論パイプライン

The online inference pipeline is a Python predictor script deployed on KServe as a_ FastAPI Python server.
オンライン推論パイプラインは、KServeにデプロイされたFastAPI PythonサーバーとしてのPython予測スクリプトです。
It accepts prediction requests and executes steps 2 to 6 before returning the rank-ordered list of recommended videos, as shown in Figure 15-8.
予測リクエストを受け入れ、図15-8に示すように、推奨ビデオのランク順リストを返す前に、ステップ2から6を実行します。

![]()
_Figure 15-8. The online inference pipeline, deployed on KServe._
_Figure 15-8. KServeにデプロイされたオンライン推論パイプライン。_

The online inference pipeline is a deployment object with a deployment API that takes in-session features and entity IDs as parameters.
オンライン推論パイプラインは、セッション内の特徴とエンティティIDをパラメータとして受け取るデプロイメントAPIを持つデプロイメントオブジェクトです。
It executes the following steps:
以下のステップを実行します：

1. Retrieval_ User features are read from the feature store with the `user_id and combined` with the on-demand and passed features.
  _1. リトリーバル_ ユーザー特徴は、フィーチャーストアから`user_id`を使用して読み取られ、オンデマンドおよび渡された特徴と結合されます。
  These user_features are passed to the user-embedding model that returns the user embedding, which is then sent to the vector index to return 200 candidate videos.
  これらのユーザー特徴は、ユーザー埋め込みモデルに渡され、ユーザー埋め込みが返され、その後ベクトルインデックスに送信されて200の候補ビデオが返されます。

2. Filtering_ We read the features for the 200 candidate videos using `ranking_fv and the` ```   video_ids.
  フィルタリング_ `ranking_fv`と``` video_ids ```を使用して200の候補ビデオの特徴を読み取ります。
  Now that we have the features for the candidate videos, we know the rating of each video, so we can filter out videos that are not suitable for the user’s age.
  候補ビデオの特徴が得られたので、各ビデオの評価がわかり、ユーザーの年齢に適さないビデオをフィルタリングできます。

3. Ranking_ We finally perform a model.predict() on the DataFrame containing the filtered candidate videos.
  ランキング_ 最後に、フィルタリングされた候補ビデオを含むDataFrameに対してmodel.predict()を実行します。
  The model executes these predictions in parallel, using all available CPU cores, minimizing the total latency.
  モデルは、利用可能なすべてのCPUコアを使用してこれらの予測を並行して実行し、総レイテンシを最小限に抑えます。

The pseudo-code for the online inference pipeline (predictor script) is shown in Figure 15-9, including the calls on the feature store and some estimates for the latencies of each of the steps.
オンライン推論パイプライン（予測スクリプト）の擬似コードは、図15-9に示されており、フィーチャーストアへの呼び出しや各ステップのレイテンシのいくつかの推定が含まれています。

![]()
_Figure 15-9. The model deployment stores both the user-embedding model and the rank‐_ _ing model, and it uses the feature store once for candidate retrieval and twice for feature_ _enrichment (you look up user features with user_id and video features with video_id)._
Figure 15-9. モデルデプロイメントは、ユーザー埋め込みモデルとランキングモデルの両方を保存します。また、候補の取得に1回、特徴の強化に2回フィーチャーストアを使用します（user_idでユーザー特徴を、video_idで動画特徴を検索します）。_

The figure shows a target P95 latency of 45 ms, with the breakdown for each step as follows:
図は、各ステップの内訳とともに、**目標P95レイテンシが45msであること**を示しています：

- Retrieving the user features is a primary key lookup and takes ~1 ms, and the user-embedding computation takes ~4 ms, giving a total of ~5 ms for this step.
  - ユーザ特徴の取得はプライマリキーのルックアップであり、約1msかかり、ユーザー埋め込み計算は約4msかかるため、このステップの合計は約5msです。

- ANN search on the vector index takes ~10 ms (if you have hundreds of millions of videos, your query and vector index will need serious tuning to keep the latency this low).
  - ベクトルインデックス上のANN検索は約10msかかります（数億のビデオがある場合、クエリとベクトルインデックスはこのレイテンシを低く保つために真剣な調整が必要です）。

- Filtering out the unsuitable videos is done in memory in Python and should take <1 ms.
  - 不適切な動画のフィルタリングは、Pythonのメモリ内で行われ、1ミリ秒未満で完了するはずです。
- A batch primary key lookup for the video features in the feature store takes ~23 ms.
  - フィーチャーストア内の動画フィーチャーに対する**バッチプライマリキーの検索には約23ミリ秒**かかります。(単一ユーザの特徴量取得よりはかかるよね! 複数アイテムだから...!:thinking;:)
- A ranking score estimatey the ranking model for each candidate video, performing the predictions in parallel on all available CPU cores, takes ~5 
  - ランキングモデルによって各候補動画に対して推定されたランキングスコアは、すべての利用可能なCPUコアで並行して予測を行うため、約5ミリ秒かかります。
- Asynchronous logging of the input features and predictions takes ~1 ms.
  - 入力フィーチャーと予測の非同期ログ記録には約1ミリ秒かかります。

<!-- ここまで読んだ! -->

We assume that computing on-demand features takes less than 1 ms, giving a total of roughly 45 ms.
オンデマンドフィーチャーの計算には1ミリ秒未満かかると仮定し、合計で約45ミリ秒となります。
If you have a high standard deviation for the vector index and feature store lookups, you should be aware of the _[tail at scale, where p99 latencies can](https://oreil.ly/l7f0i)_ increase significantly.
ベクトルインデックスとフィーチャーストアの検索に高い標準偏差がある場合、_「スケールでのテール、p99のレイテンシが大幅に増加する可能性がある」_ことに注意する必要があります。
Given that we are logging all features and prediction requests for the ranking model, we can monitor its performance by writing a model-monitoring job, similar to how we did in Chapter 14.
**ランキングモデルのためにすべてのフィーチャーと予測リクエストをログ記録**しているため、Chapter 14で行ったようにモデルモニタリングジョブを書くことでそのパフォーマンスを監視できます。
The outcomes become available in the interaction data (you should wait a few minutes for users to either view the recommendations or not), and you can easily compare predictions with outcomes.
結果はインタラクションデータに利用可能になり（ユーザーが推薦を視聴するかどうか数分待つ必要があります）、予測と結果を簡単に比較できます。
If the prediction performance degrades, you will need to retrain your ranking model or redesign it.
予測性能が低下した場合、ランキングモデルを再訓練するか、再設計する必要があります。
Or the prediction performance could be the result of upstream problems in the retrieval phase, in which case you may need to retrain or redesign the embedding models.
また、予測性能は取得フェーズの上流の問題の結果である可能性があり、その場合は埋め込みモデルを再訓練または再設計する必要があります。

<!-- ここまで読んだ! -->

## 4. Agentic Search for Videos 動画のエージェンティック検索

Your real-time recommendation system is the cash cow that should engage users for longer on your video player.
あなたのリアルタイム推薦システムは、ユーザーを動画プレーヤーでより長く引きつけるべきキャッシュカウです。
But now, you want to wow your users with new AI-powered features.
しかし今、あなたは新しいAI駆動の機能でユーザを驚かせたいと考えています。
You could extend the system by allowing users to search for videos using free text.
ユーザーが自由なテキストを使用して動画を検索できるようにすることで、システムを拡張できます。
You could also add new feature pipelines that transcribe your videos, extract frames from them, and allow users to attach tags describing key moments in videos.
また、動画を文字起こしし、フレームを抽出し、ユーザーが動画の重要な瞬間を説明するタグを付けることを可能にする新しいフィーチャーパイプラインを追加することもできます。
Figure 15-10 shows the architecture of an agent that can provide such free-text search capabilities, powered by LLMs.
図15-10は、LLMによって駆動されるそのような自由テキスト検索機能を提供できるエージェントのアーキテクチャを示しています。

![]()
_Figure 15-10. Agentic search for videos using video and user context information._
_図15-10. 動画とユーザーコンテキスト情報を使用した動画のエージェンティック検索_

<!-- ここまで読んだ! -->

Users can watch a video and ask questions about moments or scenes in the video.
ユーザーは動画を視聴し、**動画の瞬間やシーンについて質問**できます。
We can then use the active video_id to retrieve video_tags for that video, and an LLM will determine from the descriptions of the tags which one is most appropriate and change the offset in the video to pos_ms in the selected video_tags row.
その後、アクティブなvideo_idを使用してその動画のvideo_tagsを取得し、LLMがタグの説明から最も適切なものを判断し、選択されたvideo_tags行の動画内のオフセットをpos_msに変更します。
When a user is watching a video, the agent (powered by the LLM) will interpret the natural language query, retrieve all `video_tags for the current` `video_id, and select the most` relevant one.
ユーザーが動画を視聴しているとき、エージェント（LLMによって駆動される）は自然言語クエリを解釈し、現在の`video_id`に対するすべての`video_tags`を取得し、最も関連性の高いものを選択します。
The system will then seek the `pos_ms timestamp associated with that` tag.
システムはそのタグに関連付けられた`pos_ms`タイムスタンプを探します。



Similarly, a user can ask questions about all videos, and an ANN search of the transcripts vector index can be used to find the most similar video transcripts and then play the matched video. 
同様に、**ユーザーはすべてのビデオに関する質問**をすることができ、トランスクリプトベクトルインデックスのANN検索を使用して最も類似したビデオトランスクリプトを見つけ、その後一致したビデオを再生することができます。
For queries over all videos, the agent can perform an ANN search of the transcripts vector index or the videos vector index to find semantically similar segments or full videos and then play the top match. 
すべてのビデオに対するクエリの場合、エージェントはトランスクリプトベクトルインデックスまたはビデオベクトルインデックスのANN検索を実行して、意味的に類似したセグメントやフルビデオを見つけ、その後トップマッチを再生することができます。

That concludes our case study, and I will finish off the book with some advice on what _not to do. 
これで私たちのケーススタディは終了し、私は本書を何をしてはいけないかについてのアドバイスで締めくくります。
It’s a summary of many of the lessons we learned throughout the book, with a bit of wit thrown in. 
これは、本書を通じて学んだ多くの教訓の要約であり、少しのウィットが加えられています。

<!-- ここまで読んだ! -->
