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

#### 4.0.0.0.2. The Dirty Dozen of Fallacies of MLOps
####.0.0.0.3. MLOpsの誤謬のダーティダース

There are a number of fallacies (bad assumptions) that MLOps practitioners often make that cause AI systems to never make it to production. 
MLOpsの実践者がしばしば犯す誤謬（悪い仮定）がいくつかあり、それがAIシステムが本番環境に到達しない原因となります。

We have covered these fallacies in earlier chapters, but I present them here as a refresher to show you what happens if you fall for a fallacy: 
これらの誤謬については以前の章で取り上げましたが、ここでは誤謬に陥った場合に何が起こるかを示すために再確認として提示します。

_1. Do it all in one monolithic ML pipeline_ 
_1. すべてを一つのモノリシックなMLパイプラインで行う_

We saw that you can write a batch ML system as a single monolithic pipeline (parameterized to run in either training or inference mode). 
バッチMLシステムを単一のモノリシックパイプラインとして記述できることを見ました（トレーニングモードまたは推論モードで実行するようにパラメータ化されています）。

However, you cannot run a real-time ML system as a single ML pipeline, nor can you build an agentic RAG system with a single program. 
しかし、リアルタイムMLシステムを単一のMLパイプラインとして実行することはできず、単一のプログラムでエージェント的なRAGシステムを構築することもできません。

_The effects of this fallacy and how to overcome it: Without a unified architecture for building AI systems, building every new batch or real-time AI system will be like starting from scratch. 
_この誤謬の影響とそれを克服する方法：AIシステムを構築するための統一されたアーキテクチャがないと、すべての新しいバッチまたはリアルタイムAIシステムを構築することは、ゼロから始めるようなものになります。

This makes it difficult for developers to transition from building one type of AI system to another. 
これにより、開発者があるタイプのAIシステムから別のタイプのAIシステムに移行することが難しくなります。

You overcome this challenge by decomposing your AI system into feature/training/inference pipelines (FTI pipelines) that are connected to make up your batch/real-time/LLM AI system. 
この課題を克服するためには、AIシステムを特徴/トレーニング/推論パイプライン（FTIパイプライン）に分解し、それらを接続してバッチ/リアルタイム/LLM AIシステムを構成します。

_2. Data for AI is static_ 
_2. AIのためのデータは静的である_

Data scientists who learned to train models with static datasets are accustomed to models that only make predictions, and create value, once. 
静的データセットでモデルをトレーニングすることを学んだデータサイエンティストは、一度だけ予測を行い、価値を生み出すモデルに慣れています。

In the real world, AI systems work with dynamic data sources and repeatedly create value from new data as it arrives. 
実世界では、AIシステムは動的データソースで機能し、新しいデータが到着するたびに繰り返し価値を生み出します。

_The effects of this fallacy and how to overcome it: Developers have difficulty working with dynamic data sources if they don’t have the skills needed to extract and manage data from them. 
_この誤謬の影響とそれを克服する方法：開発者は、動的データソースからデータを抽出し管理するために必要なスキルを持っていない場合、動的データソースで作業するのが難しいです。

Developers have difficulty distinguishing between batch ML systems that make predictions on a schedule and real-time ML systems that make predictions in response to prediction requests. 
開発者は、スケジュールに基づいて予測を行うバッチMLシステムと、予測リクエストに応じて予測を行うリアルタイムMLシステムを区別するのが難しいです。

You overcome this by following the FTI architecture when building your AI system.  
AIシステムを構築する際にFTIアーキテクチャに従うことで、この問題を克服します。

_3. All data transformations for AI are created equal_ 
_3. AIのためのすべてのデータ変換は平等に作成される_

Data transformations are not all the same. 
データ変換はすべて同じではありません。

Model-independent transformations create reusable feature data in feature pipelines. 
モデルに依存しない変換は、特徴パイプラインで再利用可能な特徴データを作成します。

Model-dependent transformations are performed after reading data from the feature store and need to be implemented consistently in both training and inference pipelines. 
モデルに依存する変換は、フィーチャーストアからデータを読み取った後に実行され、トレーニングパイプラインと推論パイプラインの両方で一貫して実装する必要があります。

On-demand transformations create features using request-time data. 
オンデマンド変換は、リクエスト時のデータを使用して特徴を作成します。

They are performed in both feature pipelines when backfilling with historical data and online inference pipelines on request-time data. 
それらは、履歴データでバックフィルする際のフィーチャーパイプラインと、リクエスト時データに基づくオンライン推論パイプラインの両方で実行されます。

There should be no skew between the feature pipeline and online inference pipeline implementations of on-demand transformations. 
オンデマンド変換のフィーチャーパイプラインとオンライン推論パイプラインの実装の間に偏りがあってはなりません。

_The effects of this fallacy and how to overcome it: If you don’t support model-dependent transformations, you won’t reuse features in your feature store. 
_この誤謬の影響とそれを克服する方法：モデルに依存する変換をサポートしない場合、フィーチャーストアで特徴を再利用することはできません。

If you don’t support on-demand transformations, you won’t have the same code to compute real-time features from prediction request parameters and backfill feature data in feature pipelines. 
オンデマンド変換をサポートしない場合、予測リクエストパラメータからリアルタイム特徴を計算し、フィーチャーパイプラインで特徴データをバックフィルするための同じコードを持つことはできません。

If you don’t support both model-dependent and on-demand transformations, you’ll have difficulty building an observable AI system that logs/monitors interpretable features. 
モデルに依存する変換とオンデマンド変換の両方をサポートしない場合、解釈可能な特徴をログ/監視する可観測なAIシステムを構築するのが難しくなります。

The solution is to untangle your data transformations into model-independent, model-dependent, and on-demand transformations. 
解決策は、データ変換をモデルに依存しない、モデルに依存する、オンデマンドの変換に分解することです。

_4. There is no need for a feature store_ 
_4. フィーチャーストアは必要ない_

The feature store is the data layer that connects the feature pipelines and the training/inference pipelines. 
フィーチャーストアは、フィーチャーパイプラインとトレーニング/推論パイプラインを接続するデータ層です。

Building a batch ML system without a feature store is possible if you do not care about reusing features and are willing to implement your own solutions for governance, lineage, feature/prediction logging, and monitoring. 
フィーチャーストアなしでバッチMLシステムを構築することは、特徴を再利用することを気にせず、ガバナンス、系譜、特徴/予測ログ、監視のための独自のソリューションを実装することを厭わない場合は可能です。

However, if you are working with time-series data, you will also have to roll your own solution for creating point-in-time correct training data from your tables. 
ただし、時系列データを扱っている場合は、テーブルから時点に正しいトレーニングデータを作成するための独自のソリューションを構築する必要があります。

If you are building a real-time ML system, you will need to have a feature store (or build one yourself) to provide precomputed features (as context/history) for online models. 
リアルタイムMLシステムを構築している場合は、オンラインモデルのために事前計算された特徴（コンテキスト/履歴として）を提供するためにフィーチャーストアを持つ必要があります（または自分で構築する必要があります）。

The feature store also ensures there is no skew between your offline and online transformations. 
フィーチャーストアは、オフラインとオンラインの変換の間に偏りがないことを保証します。

In short, without a feature store, you may be able to roll out your first batch ML system, but your velocity for each additional batch model will not improve. 
要するに、フィーチャーストアなしで最初のバッチMLシステムを展開することはできるかもしれませんが、追加のバッチモデルごとの速度は向上しません。

For real-time ML systems, you will need a feature store to provide history/context to online models and infrastructure to ensure correct, governed, and observable features. 
リアルタイムMLシステムの場合、オンラインモデルに履歴/コンテキストを提供し、正確でガバナンスされた可観測な特徴を確保するためのインフラストラクチャを持つためにフィーチャーストアが必要です。

_The effects of this fallacy and how to overcome it: You will end up building the feature store capabilities yourself, spending much of your time figuring out how to work correctly with mutable data, how to create point-in-time correct training data, and how to synchronize data in columnar datastores with low-latency row-oriented stores for online inference. 
_この誤謬の影響とそれを克服する方法：フィーチャーストアの機能を自分で構築することになり、可変データで正しく作業する方法、時点に正しいトレーニングデータを作成する方法、オンライン推論のために列指向ストアと低遅延の行指向ストアでデータを同期する方法を見つけるのに多くの時間を費やすことになります。

You will use fewer features in your online models because of the effort required to make them available as precomputed features. 
事前計算された特徴として利用可能にするために必要な労力のため、オンラインモデルで使用する特徴は少なくなります。

You will not normalize your data models (in a snowflake schema), as it will be too hard. 
データモデルを正規化することは（スノーフレークスキーマで）、あまりにも難しいため、行いません。

The cost to build and deploy every new model will always be high and not go down over time. 
新しいモデルを構築して展開するコストは常に高く、時間が経つにつれて下がることはありません。

The solution is to use a feature store. 
解決策は、フィーチャーストアを使用することです。

_5. Experiment tracking is required for MLOps_ 
_5. 実験追跡はMLOpsに必要である_

Many teams erroneously believe that installing an experiment-tracking service is the starting point for building AI systems. 
多くのチームは、実験追跡サービスをインストールすることがAIシステムを構築するための出発点であると誤って信じています。

Experiment tracking will slow you down in getting to your first MVPS. 
実験追跡は、最初のMVPSに到達するのを遅くします。

Experiment tracking is premature optimization in MLOps. 
実験追跡はMLOpsにおける早すぎる最適化です。

You can use a model registry for operational needs, such as model storage, governance, model performance/bias evaluation, and model cards. 
モデルストレージ、ガバナンス、モデルのパフォーマンス/バイアス評価、モデルカードなどの運用ニーズには、モデルレジストリを使用できます。

Experiment tracking is a research journal for model training. 
実験追跡はモデルトレーニングのための研究ジャーナルです。

_The effects of this fallacy and how to overcome it: Just like the monkey rope experiment, in which monkeys continue to beat up any monkey that tries to climb the rope (even though none of the monkeys know why they are not supposed to climb the rope), many ML engineers think that the start of an MLOps project is to install an experiment-tracking service. 
_この誤謬の影響とそれを克服する方法：猿のロープ実験のように、猿たちはロープを登ろうとする猿を叩き続けます（どの猿もなぜロープを登ってはいけないのかを知らないにもかかわらず）、多くのMLエンジニアはMLOpsプロジェクトの開始は実験追跡サービスをインストールすることだと考えています。

The solution is to start with the model registry to store required metadata about models and their training runs, until you actually need an experiment-tracking service (which most ML engineers will probably never need). 
解決策は、モデルとそのトレーニング実行に関する必要なメタデータを保存するためにモデルレジストリから始めることです。実際に実験追跡サービスが必要になるまで（ほとんどのMLエンジニアはおそらく必要ないでしょう）。

_6. MLOps is just DevOps for ML_ 
_6. MLOpsはMLのためのDevOpsに過ぎない_

Like DevOps, MLOps requires the automated testing of the source code for your pipelines, but unlike DevOps, in MLOps you also need to version and test the input data. 
DevOpsと同様に、MLOpsはパイプラインのソースコードの自動テストを必要としますが、DevOpsとは異なり、MLOpsでは入力データのバージョン管理とテストも必要です。

Data validation tests prevent garbage in from producing garbage out. 
データ検証テストは、ゴミが入ることを防ぎ、ゴミが出ることを防ぎます。

Similarly, model validation tests have no corollary in DevOps. 
同様に、モデル検証テストはDevOpsには相当するものがありません。

There is also the difference that AI system performance tends to degrade over time, due to data and model drift. 
AIシステムのパフォーマンスは、データとモデルのドリフトにより、時間とともに劣化する傾向があります。

_The effects of this fallacy and how to overcome it: Without data tests, your training or inference data may get contaminated. 
_この誤謬の影響とそれを克服する方法：データテストがないと、トレーニングデータや推論データが汚染される可能性があります。

Without model tests, your models may have bias or poor performance. 
モデルテストがないと、モデルにバイアスやパフォーマンスの低下が生じる可能性があります。

Your AI system’s performance may degrade over time due to a lack of feature monitoring and model performance monitoring. 
特徴の監視やモデルパフォーマンスの監視が不足しているため、AIシステムのパフォーマンスが時間とともに劣化する可能性があります。

Follow MLOps best practices for offline data validation, model validation, and feature/model monitoring. 
オフラインデータ検証、モデル検証、特徴/モデル監視のためのMLOpsのベストプラクティスに従ってください。

_7. Versioning models is enough for safe upgrade/rollback_ 
_7. モデルのバージョン管理だけでは安全なアップグレード/ロールバックには不十分である_

For a stateful, real-time ML system, the model deployment is tightly coupled to the versioned feature views that provide it with precomputed features. 
状態を持つリアルタイムMLシステムでは、モデルのデプロイメントは、事前計算された特徴を提供するバージョン管理されたフィーチャービューに密接に結びついています。

When you upgrade a model deployment, it is not enough to just update the model version. 
モデルのデプロイメントをアップグレードする際には、モデルのバージョンを更新するだけでは不十分です。

You may also need to upgrade the version of the feature view used by the model deployment. 
モデルのデプロイメントで使用されるフィーチャービューのバージョンもアップグレードする必要があります。

_The effects of this fallacy and how to overcome it: You can introduce subtle bugs if you do not couple model deployment versions with feature versions. 
_この誤謬の影響とそれを克服する方法：モデルデプロイメントのバージョンをフィーチャーバージョンと結びつけないと、微妙なバグを引き起こす可能性があります。

For example, if your new deployment uses the old feature version but the new feature group version is schema compatible with the previous version, the system will appear to work as before. 
例えば、新しいデプロイメントが古いフィーチャーバージョンを使用しているが、新しいフィーチャーグループバージョンが前のバージョンとスキーマ互換性がある場合、システムは以前と同様に機能しているように見えます。

However, its performance will suffer, and it will be a hard bug to find. 
しかし、そのパフォーマンスは低下し、バグを見つけるのが難しくなります。

The solution is to tightly couple the version of the model deployment with the feature view that feeds it. 
解決策は、モデルデプロイメントのバージョンをそれにフィードするフィーチャービューと密接に結びつけることです。

_8. There is no need for data versioning_ 
_8. データのバージョン管理は必要ない_

Reproducibility of training data requires data versioning. 
トレーニングデータの再現性にはデータのバージョン管理が必要です。

_The effects of this fallacy and how to overcome it: Without data versioning, if you re-create a training dataset and late data arrives since the creation of the first training dataset, the late data will be included in subsequent training dataset creation. 
_この誤謬の影響とそれを克服する方法：データのバージョン管理がないと、トレーニングデータセットを再作成し、最初のトレーニングデータセットの作成以降に遅れてデータが到着した場合、遅れて到着したデータがその後のトレーニングデータセットの作成に含まれることになります。

This is because there is no ingestion timestamp for late-arriving data. 
これは、遅れて到着したデータに対する取り込みタイムスタンプがないためです。

The solution is to support data versioning, as with lakehouse tables, and it includes ingestion timestamps for data points. 
解決策は、レイクハウステーブルのようにデータのバージョン管理をサポートし、データポイントに対する取り込みタイムスタンプを含めることです。

This enables you to re-create the training data exactly as it was at the point in time when it was originally created. 
これにより、元々作成された時点でのトレーニングデータを正確に再作成することができます。

_9. The model signature is the API for model deployments_ 
_9. モデルシグネチャはモデルデプロイメントのAPIである_

A real-time ML system uses a model deployment that makes predictions in response to prediction requests. 
リアルタイムMLシステムは、予測リクエストに応じて予測を行うモデルデプロイメントを使用します。

The parameters sent by the client to the model deployment API are typically not the same as the input parameters to the model (the model signature). 
クライアントがモデルデプロイメントAPIに送信するパラメータは、通常、モデルへの入力パラメータ（モデルシグネチャ）とは異なります。

_The effects of this fallacy and how to overcome it: Developers may mistake the model deployment API for the model signature. 
_この誤謬の影響とそれを克服する方法：開発者はモデルデプロイメントAPIをモデルシグネチャと誤解する可能性があります。

Without explicit support for a deployment API, developers will be forced to read source code to infer it. 
デプロイメントAPIの明示的なサポートがない場合、開発者はそれを推測するためにソースコードを読むことを余儀なくされます。

You need to explicitly define the API (or schema) for a deployment. 
デプロイメントのAPI（またはスキーマ）を明示的に定義する必要があります。



. Without explicit support for a deployment API, developers will be forced to read source code to infer it. 
明示的なデプロイメントAPIのサポートがない場合、開発者はそれを推測するためにソースコードを読むことを余儀なくされます。

You need to explicitly define the API (or schema) for a deployment. 
デプロイメントのためのAPI（またはスキーマ）を明示的に定義する必要があります。

_10. Online prediction latency is the time taken for the model prediction_ 
_10. オンライン予測レイテンシは、モデル予測にかかる時間です。_

When you serve a model behind a network endpoint, you typically have to perform a lot of operations before you finally call `model.predict()` with the final `feature vector(s)` as input. 
ネットワークエンドポイントの背後でモデルを提供する場合、最終的な`feature vector(s)`を入力として`model.predict()`を呼び出す前に、多くの操作を実行する必要があります。

_The effects of this fallacy and how to overcome it: You cannot assume that prediction latency for network-hosted models is only the time taken for the model prediction._ 
_この誤謬の影響とそれを克服する方法：ネットワークホストモデルの予測レイテンシは、モデル予測にかかる時間だけであると仮定してはいけません。_

You have to include the time for all preprocessing (building feature vectors, RAG, etc.) and postprocessing (feature/prediction logging). 
すべての前処理（特徴ベクトルの構築、RAGなど）と後処理（特徴/予測のログ記録）の時間を含める必要があります。

_11. LLMOps is different from MLOps_ 
_11. LLMOpsはMLOpsとは異なります。_

LLMs need GPUs for inference and fine-tuning. 
LLMは推論とファインチューニングのためにGPUを必要とします。

Similarly, LLMs need support for scalable compute, scalable storage, and scalable model serving. 
同様に、LLMはスケーラブルなコンピュート、スケーラブルなストレージ、およびスケーラブルなモデル提供のサポートが必要です。

However, many MLOps platforms do not support either GPUs or scale, and the result is that LLMs are often seen as outside of MLOps and part of a new LLMOps discipline. 
しかし、多くのMLOpsプラットフォームはGPUやスケールをサポートしておらず、その結果、LLMはしばしばMLOpsの外部にあるものと見なされ、新しいLLMOpsの分野の一部と見なされます。

However, LLMs still follow the same FTI architecture. 
しかし、LLMは依然として同じFTIアーキテクチャに従います。

If your MLOps platform supports GPUs and scale, LLMOps is just MLOps with LLMs. 
あなたのMLOpsプラットフォームがGPUとスケールをサポートしている場合、LLMOpsは単にLLMを持つMLOpsです。

Feature pipelines are used to chunk, clean, and score text for instruction and alignment datasets. 
特徴パイプラインは、指示および整列データセットのためにテキストをチャンク化、クリーンアップ、およびスコアリングするために使用されます。

They are also used to compute vector embeddings stored in a vector index for RAG. 
それらはまた、RAGのためにベクトルインデックスに保存されたベクトル埋め込みを計算するためにも使用されます。

Training pipelines are used to fine-tune and align foundation LLMs. 
トレーニングパイプラインは、基盤となるLLMをファインチューニングおよび整列させるために使用されます。

Tokenization is a model-dependent transformation that needs to be consistent between training and inference—without platform support, users often slip up, using the wrong version of the tokenizer for their LLM in inference. 
トークン化は、トレーニングと推論の間で一貫性が必要なモデル依存の変換です。プラットフォームのサポートがない場合、ユーザーはしばしば間違ったバージョンのトークナイザーを推論で使用してしまいます。

Agents and workflows are found in online inference pipelines, as are calls to external systems with RAG and function calling. 
エージェントとワークフローはオンライン推論パイプラインに見られ、RAGや関数呼び出しを伴う外部システムへの呼び出しもあります。

Your MLOps team should be able to bring the same architecture and tooling to bear on LLM systems as it does with batch and real-time ML systems. 
あなたのMLOpsチームは、バッチおよびリアルタイムのMLシステムと同様に、LLMシステムに同じアーキテクチャとツールを適用できるべきです。

_The effects of this fallacy and how to overcome it: You may duplicate your AI infrastructure by supporting a separate LLMOps stack from your MLOps stack._ 
_この誤謬の影響とそれを克服する方法：MLOpsスタックとは別のLLMOpsスタックをサポートすることで、AIインフラストラクチャを重複させる可能性があります。_

If you treat LLMOps as MLOps at scale, developers should be able to easily transition from batch/real-time ML systems to an LLM AI system—if you follow the FTI architecture. 
LLMOpsをスケールでのMLOpsとして扱う場合、開発者はFTIアーキテクチャに従えば、バッチ/リアルタイムのMLシステムからLLM AIシステムに簡単に移行できるはずです。

_12. You require an ML orchestrator for ML pipelines_ 
_12. MLパイプラインにはMLオーケストレーターが必要です。_

You do not require an ML-specific orchestrator, such as Kubeflow/Metaflow/ZenML/SageMaker Pipelines, to run your ML pipelines. 
MLパイプラインを実行するために、Kubeflow/Metaflow/ZenML/SageMaker PipelinesのようなML特有のオーケストレーターは必要ありません。

ML orchestrators were designed for batch ML systems and are often limited to running only a few different data processing and ML frameworks. 
MLオーケストレーターはバッチMLシステムのために設計されており、通常は異なるデータ処理およびMLフレームワークをいくつかしか実行できません。

For example, you can’t run a Spark feature pipeline in Kubeflow. 
例えば、KubeflowではSparkの特徴パイプラインを実行できません。

Also, ML orchestrators do not run streaming feature pipelines. 
また、MLオーケストレーターはストリーミング特徴パイプラインを実行しません。

If you want to support batch, real-time, and even LLM AI systems in one platform, not all ML pipelines or services can be managed by your ML orchestrator. 
バッチ、リアルタイム、さらにはLLM AIシステムを1つのプラットフォームでサポートしたい場合、すべてのMLパイプラインやサービスをMLオーケストレーターで管理できるわけではありません。

The implication of this is that ML orchestrators are not aware of all lineage information for all AI systems. 
これは、MLオーケストレーターがすべてのAIシステムのすべての系譜情報を把握していないことを意味します。

In contrast, the data layers (feature store, model registry) are aware of all lineage information for all classes of ML pipeline and should typically be the source of truth for lineage. 
対照的に、データレイヤー（特徴ストア、モデルレジストリ）は、すべてのクラスのMLパイプラインの系譜情報を把握しており、通常は系譜の真実の源であるべきです。

That leaves you free to use the orchestrator that best suits the requirements of your FTI pipelines. 
これにより、FTIパイプラインの要件に最も適したオーケストレーターを自由に使用できます。

_The effects of this fallacy and how to overcome it: Since its inception, MLOps has been associated with ML orchestrators, such as Kubeflow._ 
_この誤謬の影響とそれを克服する方法：MLOpsはその発足以来、KubeflowのようなMLオーケストレーターと関連付けられてきました。_

But the recent Cambrian explosion in batch and stream-processing data engines means that you may want to use a specialist framework for feature pipelines, like Apache Flink, Feldera, or Polars. 
しかし、バッチおよびストリーム処理データエンジンの最近のカンブリア爆発により、Apache Flink、Feldera、またはPolarsのような特徴パイプラインのための専門的なフレームワークを使用したいかもしれません。

ML orchestrators can’t keep up. 
MLオーケストレーターは追いつけません。

They were also originally designed to store lineage information. 
彼らはもともと系譜情報を保存するために設計されていました。

If you run an ML pipeline outside your ML orchestrator, lineage information will be lost to it. 
MLオーケストレーターの外でMLパイプラインを実行すると、系譜情報は失われます。

Instead, lineage information should be managed by the feature store and model registry, not by the orchestrator. 
代わりに、系譜情報はオーケストレーターではなく、特徴ストアとモデルレジストリによって管理されるべきです。

You are free to use the best orchestrator for each of your ML pipelines. 
各MLパイプラインに最適なオーケストレーターを自由に使用できます。

###### 4.0.0.0.4. The Ethical Responsibilities of AI Builders
###### 4.0.0.0.5. AIビルダーの倫理的責任

Finally, a word on your ethical responsibilities when you build an AI system. 
最後に、AIシステムを構築する際の倫理的責任について一言。

Before you dive into building an AI system, you should always consider any potential negative impacts of the system. 
AIシステムの構築に取り掛かる前に、システムの潜在的な悪影響を常に考慮すべきです。

It is not only your responsibility to comply with laws and regulations but also to ensure you do not cause direct or indirect harm. 
法律や規制に従うことはあなたの責任であるだけでなく、直接的または間接的な害を引き起こさないことを保証することもあなたの責任です。

For example, personalized recommender systems must be responsible AI systems. 
例えば、パーソナライズされたレコメンダーシステムは責任あるAIシステムでなければなりません。

An investigation by RTÉ Ireland Prime Time in May 2024 discovered that “by the end of an hour of scrolling, TikTok’s recommender system was showing a stream of videos almost exclusively related to depression, self-harm, and suicidal thoughts to the users it believed to be 13 years old.” 
2024年5月にRTÉ Ireland Prime Timeによる調査では、「1時間のスクロールの終わりまでに、TikTokのレコメンダーシステムは、13歳だと信じているユーザーに対して、ほぼ独占的に抑うつ、自傷行為、そして自殺の考えに関連する動画のストリームを表示していた」と発見されました。

If you work in a company that builds an AI system like that, fix the system or leave the company and whistleblow. 
そのようなAIシステムを構築する会社で働いている場合は、システムを修正するか、会社を辞めて内部告発してください。

It is not honorable to build software that is lawful but unethical. 
合法であるが倫理的でないソフトウェアを構築することは名誉あることではありません。

We can learn from history, and the story of the Vasa ship in Sweden is both a warning and a lesson to engineers everywhere. 
私たちは歴史から学ぶことができ、スウェーデンのバサ船の物語は、エンジニアにとって警告であり教訓でもあります。

King Gustavus Adolphus wanted a warship with 64 heavy cannons (the most in the world in 1627). 
グスタフス・アドルフ王は、64門の重砲を備えた戦艦を望みました（1627年に世界で最も多い）。

The experts told him it wasn’t possible. 
専門家たちはそれが不可能だと告げました。

Still, shipbuilders built it, knowing their work was both futile and dangerous. 
それでも、造船業者たちは、自分たちの仕事が無駄で危険であることを知りながら、それを建造しました。

The engineers were as spineless as the ship itself. 
エンジニアたちは船そのものと同じくらい臆病でした。

The Vasa sank on launch, with the loss of around 30 souls. 
バサは進水時に沈没し、約30人の命が失われました。

Don’t be the developer who builds the AI system that does harm. 
害を及ぼすAIシステムを構築する開発者にならないでください。

Together, we can make AI a force for good, but without help from the law, we will need an agreed-upon ethical code for that to happen. 
共に、私たちはAIを善の力にすることができますが、法律の助けがなければ、それを実現するためには合意された倫理コードが必要です。

Follow that ethical code and help enforce it, and you will thank yourself for it when you later reflect back on your life. 
その倫理コードに従い、それを施行する手助けをすれば、後に自分の人生を振り返ったときに自分を感謝することになるでしょう。

###### 4.0.0.0.6. Summary
###### 4.0.0.0.7. 要約

This chapter introduced a case study of building your own TikTok-like personalized recommendation service for videos. 
この章では、動画のための自分自身のTikTokのようなパーソナライズされたレコメンデーションサービスを構築するケーススタディを紹介しました。

It covered the retrieval-and-ranking architecture, which builds on the two-tower embedding model for retrieval and a ranking model for personalizing recommendations. 
それは、取得のための2タワー埋め込みモデルと、レコメンデーションをパーソナライズするためのランキングモデルに基づく取得とランキングのアーキテクチャをカバーしました。

We covered the streaming, batch, and vector embedding feature pipelines for our system; the training pipelines for the user- and video-embedding models and the ranking model; and the online inference pipeline to implement retrieval and ranking for user requests. 
私たちは、システムのためのストリーミング、バッチ、およびベクトル埋め込み特徴パイプライン、ユーザーおよび動画埋め込みモデルとランキングモデルのためのトレーニングパイプライン、ユーザーリクエストのための取得とランキングを実装するオンライン推論パイプラインをカバーしました。

We finished with a flourish, adding an agent to support free-text search across and within videos, powered by LLMs. 
私たちは、LLMによって駆動される動画全体および内部での自由形式検索をサポートするエージェントを追加して、華やかに締めくくりました。

Finally, we concluded the book with a dirty dozen of fallacies for MLOps and LLMOps that you should avoid if you want to be successful in building AI systems. 
最後に、AIシステムを構築する際に成功したいのであれば避けるべきMLOpsとLLMOpsの誤謬のダーティダズンで本書を締めくくりました。

And there is no more important time in history for building AI systems than today. 
そして、AIシステムを構築するための歴史の中で、今日ほど重要な時はありません。

Given the rate of improvements, today will always be the most important day for building AI systems. 
改善の速度を考えると、今日がAIシステムを構築するための最も重要な日であり続けるでしょう。

Go forth and create, and may the force be with you. 
前進して創造力があなたと共にあらんことを。

###### 4.0.0.0.8. About the Author
**Jim Dowling is CEO of Hopsworks and a former associate professor at KTH Royal** Institute of Technology
###### 4.0.0.0.9. 著者について
**ジム・ダウリングはHopsworksのCEOであり、KTH王立工科大学の元准教授です。**



. He has led the development of Hopsworks, including the first open-source feature store for machine learning. 
彼はHopsworksの開発を主導し、機械学習のための最初のオープンソースフィーチャーストアを含んでいます。

He has a unique background in the intersection of data and AI. 
彼はデータとAIの交差点において独自のバックグラウンドを持っています。

For data, he worked at MySQL and later led the development of HopsFS, a distributed filesystem that won the IEEE Scale Prize in 2017. 
データに関しては、彼はMySQLで働き、その後2017年にIEEE Scale Prizeを受賞した分散ファイルシステムHopsFSの開発を主導しました。

For AI, his PhD introduced collaborative reinforcement learning, and he developed and taught the first course on deep learning in Sweden in 2016. 
AIに関しては、彼の博士号は協調強化学習を紹介し、2016年にスウェーデンで深層学習に関する最初のコースを開発し、教えました。

He also released a popular online course on serverless machine learning using Python at serverless-ml.org. 
彼はまた、serverless-ml.orgでPythonを使用したサーバーレス機械学習に関する人気のオンラインコースをリリースしました。

This combined background of data and AI helped him realize the vision of a feature store for machine learning based on general-purpose programming languages, rather than the earlier feature store work at Uber on DSLs. 
このデータとAIの組み合わせたバックグラウンドは、彼が一般目的プログラミング言語に基づく機械学習のためのフィーチャーストアのビジョンを実現するのに役立ちました。これは、以前のUberでのDSLに関するフィーチャーストアの作業とは異なります。

He was the first evangelist for feature stores, helping to create the feature store product category through talks at industry conferences (like Data/AI Summit, PyData, and OSDC) and educational articles on feature stores. 
彼はフィーチャーストアの最初のエバンジェリストであり、業界会議（Data/AI Summit、PyData、OSDCなど）での講演やフィーチャーストアに関する教育的な記事を通じてフィーチャーストア製品カテゴリの創出を助けました。

He is the organizer of the annual feature store summit conference and the featurestore.org community, as well as co-organizer of PyData Stockholm. 
彼は年次フィーチャーストアサミット会議とfeaturestore.orgコミュニティの主催者であり、PyData Stockholmの共同主催者でもあります。

###### 4.0.0.0.10. Colophon コロフォン

The animal on the cover of Building Machine Learning Systems with a Feature Store is a red-breasted pygmy parrot (Micropsitta bruijnii), native to the Maluku Islands and Melanesia. 
『フィーチャーストアを用いた機械学習システムの構築』の表紙に描かれている動物は、マルク諸島とメラネシアに生息する赤胸のピグミーオウム（Micropsitta bruijnii）です。

This parrot is a member of the smallest genus of parrot, with an average length of eight centimeters (a little over three inches). 
このオウムは最も小さなオウムの属に属し、平均長は8センチメートル（約3インチ強）です。

Unlike many other pygmy parrots, it lives in high-altitude environments and nests in tree hollows or stumps. 
他の多くのピグミーオウムとは異なり、高地環境に生息し、木の空洞や切り株に巣を作ります。

It feeds on lichen and moves in short, jerky movements, often climbing along the bark of trees. 
地衣類を食べ、短くて不規則な動きで移動し、しばしば木の樹皮に沿って登ります。

As with many birds, the red-breasted pygmy parrot exhibits sexual dimorphism, where the male and female differ in appearance: both are green but the male has a red chest and pink-orange throat while the female is primarily green with a blue crown and white face. 
多くの鳥と同様に、赤胸のピグミーオウムは性二形性を示し、オスとメスで外見が異なります。どちらも緑色ですが、オスは赤い胸とピンクオレンジの喉を持ち、メスは主に緑色で青い冠と白い顔をしています。

Its lifespan is similar to that of other small parrots, up to ten years. 
その寿命は他の小型オウムと同様で、最大10年です。

Unlike some other parrots, this species does not do well in captivity. 
他のいくつかのオウムとは異なり、この種は飼育下ではうまくいきません。

Its IUCN status is of Least Concern. 
そのIUCNのステータスは「低危険」です。

Many of the animals on O’Reilly covers are endangered; all of them are important to the world. 
O'Reillyの表紙に描かれている動物の多くは絶滅危惧種であり、すべてが世界にとって重要です。

The cover illustration is by José Marzan Jr., based on an antique line engraving from _Lydekker’s Royal Natural History. 
表紙のイラストはJosé Marzan Jr.によるもので、_Lydekker’s Royal Natural History_の古い線画に基づいています。

The series design is by Edie Freedman, Ellie Volckhausen, and Karen Montgomery. 
シリーズデザインはEdie Freedman、Ellie Volckhausen、Karen Montgomeryによるものです。

The cover fonts are Gilroy Semibold and Guardian Sans. 
表紙のフォントはGilroy SemiboldとGuardian Sansです。

The text font is Adobe Minion Pro; the heading font is Adobe Myriad Condensed; and the code font is Dalton Maag’s Ubuntu Mono. 
本文フォントはAdobe Minion Pro、見出しフォントはAdobe Myriad Condensed、コードフォントはDalton MaagのUbuntu Monoです。
