## CHAPTER 15: TikTok’s Personalized Recommender: The World’s Most Valuable AI System
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
最後に、この本を読んだ後にもう二度と騙されないことを願う12の誤謬と、AIシステムビルダーとしての倫理的責任に関するいくつかのアドバイスで本書を締めくくります。

Thanks for hanging in there, and let’s get cracking with the most rewarding part of working with AI—building real-world AI systems that can change the world for the better.
ここまでお付き合いいただきありがとうございます。それでは、AIと共に働く最もやりがいのある部分、つまり世界をより良く変えることができる実世界のAIシステムを構築することに取り掛かりましょう。

###### Introduction to Recommenders
###### レコメンダーの紹介

_Recommender systems help users discover relevant content in user-facing systems._
_レコメンダーシステムは、ユーザー向けシステムで関連するコンテンツを発見するのに役立ちます。_

The content can be anything from videos to music to ecommerce to social media posts.
コンテンツは、ビデオ、音楽、eコマース、ソーシャルメディアの投稿など、何でもかまいません。

The first approaches to recommendation systems were not personalized.
推薦システムの最初のアプローチはパーソナライズされていませんでした。

_Content-based recommendation systems for videos can use genres, directors, actors, or_ plot keywords to suggest videos that are similar to those a user has previously watched and enjoyed.
_ビデオのコンテンツベースの推薦システムは、ジャンル、監督、俳優、または_ プロットキーワードを使用して、ユーザーが以前に視聴し楽しんだビデオに似たビデオを提案できます。

You only need content usage features to train content recommender models, which makes them easy to scale.
コンテンツレコメンダーモデルをトレーニングするには、コンテンツ使用機能のみが必要であり、これによりスケールが容易になります。

Netflix and YouTube still have content-based recommendations as one of several types of recommendations they provide.
NetflixとYouTubeは、提供するいくつかのタイプの推薦の1つとして、依然としてコンテンツベースの推薦を持っています。

-----
The next classes of recommender systems were built on interaction datasets, contain‐ ing user action events for content, such as views, likes, and shares.
次のクラスのレコメンダーシステムは、ビュー、いいね、シェアなどのコンテンツに対するユーザーアクションイベントを含むインタラクションデータセットに基づいて構築されました。

Item-to-item (i2i) _recommendation focuses on the relationships between items themselves, enabling fea‐_ tures like “Customers who bought this item also bought…” or “If you liked this video, you might enjoy….” 
アイテム間（i2i）_推薦は、アイテム自体の関係に焦点を当て、「このアイテムを購入した顧客は他に何を購入したか…」や「このビデオが気に入ったなら、こちらも楽しめるかもしれません…」といった機能を可能にします。

Interaction datasets provide patterns of co-consumption or simi‐ larity, and i2i methods enable users to easily explore related options.
インタラクションデータセットは、共同消費や類似性のパターンを提供し、i2iメソッドはユーザーが関連オプションを簡単に探索できるようにします。

_User-to-item (u2i) recommendations take a different approach by centering recom‐_ mendations on the individual user.
ユーザーからアイテム（u2i）推薦は、個々のユーザーに中心を置くことで異なるアプローチを取ります。

Here, the goal is to suggest items to a user based on their historical preferences and behaviors, or by drawing on the experiences of similar users.
ここでは、ユーザーの歴史的な好みや行動に基づいてアイテムを提案すること、または類似のユーザーの経験を引き出すことが目標です。

The first widely used method for i2i and u2i recommender systems was _collaborative filtering, but it has challenges working with large data volumes and_ sparse data (where most users interact with only a tiny fraction of items).
i2iおよびu2iレコメンダーシステムの最初の広く使用されている方法は_コラボレーティブフィルタリングでしたが、大量のデータボリュームや_ スパースデータ（ほとんどのユーザーがアイテムのごく一部としか相互作用しない場合）での作業には課題があります。

Factoriza‐ _tion machines were introduced to better handle data sparsity, but they also encounter_ scalability issues for large data volumes and real-time updates.
ファクタリゼーションマシンはデータのスパース性をより良く処理するために導入されましたが、大量のデータボリュームやリアルタイムの更新に対してもスケーラビリティの問題に直面します。

In the next section, we will look at the state-of-the-art retrieval-and-ranking architec‐ ture that addresses these challenges, but we will start by looking at the data we need to collect to build our recommendation system.
次のセクションでは、これらの課題に対処する最先端のretrieval-and-rankingアーキテクチャを見ていきますが、まずは推薦システムを構築するために収集する必要があるデータを見ていきます。

Table 15-1 shows popular features used to train video recommendation models.
表15-1は、ビデオ推薦モデルをトレーニングするために使用される一般的な特徴を示しています。

_Table 15-1. Classes of features used in video recommender systems and their data properties_
**表15-1. ビデオレコメンダーシステムで使用される特徴のクラスとそのデータ特性**

**Grouping** **Features** **Transformations** **Data volume/velocity**  
**グルーピング** **特徴** **変換** **データボリューム/速度**  
User profile Gender, age, language, device, interests, location, recently viewed  
ユーザープロファイル 性別、年齢、言語、デバイス、興味、場所、最近の視聴  
GBs/TBs, Batch and streaming  
GBs/TBs, バッチおよびストリーミング  
GBs/TBs, Batch and streaming  
GBs/TBs, バッチおよびストリーミング  
TBs/PBs, Batch and streaming  
TBs/PBs, バッチおよびストリーミング  
Video Title, genre, length, age, clicks, CTR, likes, description, content  
ビデオ タイトル、ジャンル、長さ、年齢、クリック、CTR、いいね、説明、コンテンツ  
Model-independent, model-dependent  
モデル非依存、モデル依存  
Model-independent, model-dependent  
モデル非依存、モデル依存  
Interactions View, skipped, like, share, watch time Model-independent, model-dependent  
インタラクション 視聴、スキップ、いいね、シェア、視聴時間 モデル非依存、モデル依存  
Real-time context
リアルタイムコンテキスト  
In-session browsing  
セッション中のブラウジング  
Trending (near you, your demographic, friends)  
トレンド（あなたの近く、あなたの人口統計、友人）  
Device, usage pattern (binge, etc.), last click, session duration  
デバイス、使用パターン（ビンジなど）、最後のクリック、セッションの長さ  
Model-independent, ondemand  
モデル非依存、オンデマンド  
GBs/TBs, Streaming  
GBs/TBs, ストリーミング  
On-demand GBs/TBs, Real-time processing  
オンデマンド GBs/TBs, リアルタイム処理  
Graph/Social Social actions (such as friends liked), social proximity  
グラフ/ソーシャル ソーシャルアクション（友人がいいねしたなど）、社会的近接  
Model-dependent, on-demand  
モデル依存、オンデマンド  
GBs/TBs, Batch and streaming  
GBs/TBs, バッチおよびストリーミング  
-----
At a high level, the features useful for building recommendation models are centered around users, items (videos, in our case), and interactions between users and items.
高いレベルで、推薦モデルを構築するのに役立つ特徴は、ユーザー、アイテム（この場合はビデオ）、およびユーザーとアイテム間の相互作用に中心を置いています。

Some of the features contain slowly changing data that is stored in a data warehouse and updated by batch feature pipelines; for example, information about a user’s viewing behavior, such as the average view percentage for videos and compressed viewing statistics on video genres.
いくつかの特徴は、データウェアハウスに保存され、バッチフィーチャーパイプラインによって更新されるゆっくりと変化するデータを含んでいます。たとえば、ビデオの平均視聴率やビデオジャンルに関する圧縮視聴統計など、ユーザーの視聴行動に関する情報です。

Other features contain real-time context information about global or localized viewing trends.
他の特徴は、グローバルまたはローカライズされた視聴トレンドに関するリアルタイムのコンテキスト情報を含んでいます。

For example, to enable our recommender to quickly spread breaking news, both the number of clicks and the click-through rate (CTR) are important realtime context features for videos and are updated by streaming feature pipelines.
たとえば、私たちのレコメンダーが速報ニュースを迅速に広めることを可能にするために、クリック数とクリック率（CTR）の両方がビデオにとって重要なリアルタイムコンテキスト機能であり、ストリーミングフィーチャーパイプラインによって更新されます。

Batch feature pipelines would be too slow for spreading breaking news.
バッチフィーチャーパイプラインは速報ニュースを広めるには遅すぎます。

In-session browsing features similarly contain valuable real-time signals of recent user activity but are computed on demand from request-time parameters.
セッション中のブラウジング機能も、最近のユーザー活動の貴重なリアルタイム信号を含んでいますが、リクエスト時のパラメータからオンデマンドで計算されます。

For example, if the user started viewing videos about cooking but then switched to sports, the recommender could include recommendations about sports that the user has historically interacted with and videos of the same length as other videos that the user has historically watched.
たとえば、ユーザーが料理に関するビデオの視聴を開始したが、その後スポーツに切り替えた場合、レコメンダーはユーザーが歴史的に相互作用してきたスポーツに関する推薦や、ユーザーが歴史的に視聴してきた他のビデオと同じ長さのビデオを含めることができます。

###### A TikTok Recommender with the Retrieval-and-Ranking Architecture
###### Retrieval-and-Rankingアーキテクチャを用いたTikTokレコメンダー

TikTok is the world’s most popular video streaming platform in 2025.
TikTokは2025年に世界で最も人気のあるビデオストリーミングプラットフォームです。

It has several different ways to recommend videos, including a friends feed and a following feed.
友人のフィードやフォローのフィードなど、ビデオを推薦するためのいくつかの異なる方法があります。

But its “For You” feed is what differentiates TikTok from other video streaming plat‐ forms.
しかし、「For You」フィードがTikTokを他のビデオストリーミングプラットフォームと差別化しています。

It really is personalized for you, and it updates its recommendations in real time, based on your activity.
これは本当にあなたのためにパーソナライズされており、あなたの活動に基づいてリアルタイムで推薦を更新します。

For a human to perceive the feed as reacting to their actions, it cannot take more than a couple of seconds to update; otherwise it will be “laggy,” not intelligent.
人間がフィードが自分の行動に反応していると認識するためには、更新に数秒以上かかってはいけません。そうでなければ、「遅延」が生じ、知的ではなくなります。

We will build our own version of the personalized “For You” feed based on the retrieval-and-ranking architecture, shown in Figure 15-1.
私たちは、図15-1に示されているretrieval-and-rankingアーキテクチャに基づいて、パーソナライズされた「For You」フィードの独自のバージョンを構築します。

We will decompose the problem of recommending videos into two phases: (1) a retrieval phase that uses a scalable vector index to return a few hundred candidate videos and (2) a ranking phase to order the hundreds of candidates based on a metric we want to optimize, like increased user engagement.
私たちは、ビデオを推薦する問題を2つのフェーズに分解します。(1) スケーラブルなベクトルインデックスを使用して数百の候補ビデオを返すリトリーバルフェーズと、(2) ユーザーエンゲージメントの向上のような最適化したいメトリックに基づいて数百の候補を順序付けるランキングフェーズです。

-----
_Figure 15-1. TikTok’s personalized recommender service is built on a retrieval-and-_ _ranking architecture that works at massive scale: billions of videos are indexed for bil‐_ _lions of users, handling millions of requests per second at very low latency._
**図15-1. TikTokのパーソナライズドレコメンダーサービスは、膨大なスケールで機能するretrieval-and-rankingアーキテクチャに基づいて構築されています: 数十億のビデオが数十億のユーザーのためにインデックスされ、非常に低いレイテンシで毎秒数百万のリクエストを処理します。**

[The key systems challenges, some of which are covered in TikTok’s Monolith research](https://oreil.ly/-oAdq) [paper, in building a personalized recommendation system at scale are:](https://oreil.ly/-oAdq)
[スケールでパーソナライズされた推薦システムを構築する際の主要なシステムの課題のいくつかは、TikTokのMonolith研究](https://oreil.ly/-oAdq) [論文で取り上げられています。](https://oreil.ly/-oAdq)

_Nonstationarity challenges_ User preferences and trending videos change continually, causing features to become stale in seconds and requiring models to be continually retrained.
_非定常性の課題_ ユーザーの好みやトレンドのビデオは常に変化し、特徴が数秒で古くなり、モデルを継続的に再トレーニングする必要があります。

When the environment is dynamic, your system needs to adapt constantly.
環境が動的な場合、システムは常に適応する必要があります。

At short timescales, this means having fresh precomputed features (stream processing) and real-time feature computation from request parameters.
短い時間スケールでは、これは新鮮な事前計算された特徴（ストリーム処理）とリクエストパラメータからのリアルタイム特徴計算を持つことを意味します。

At longer time‐ [scales, this means retraining models frequently to prevent concept drift.
長い時間スケールでは、これは概念の漂流を防ぐためにモデルを頻繁に再トレーニングすることを意味します。

TikTok](https://oreil.ly/vuxew) [uses Flink to achieve subsecond streaming feature computation from user actions](https://oreil.ly/vuxew) (clicks, likes, etc.) and Cassandra (key-value store) and Redis (cache) for realtime feature serving.
TikTokは、ユーザーアクションからのサブ秒ストリーミング特徴計算を実現するためにFlinkを使用し](https://oreil.ly/vuxew) (クリック、いいねなど) 、リアルタイム特徴提供のためにCassandra（キー・バリューストア）とRedis（キャッシュ）を使用しています。

TikTok’s monolith also includes continual retraining of the models (once per minute), but we can simplify to scheduling batch training jobs that run every hour.
TikTokのモノリスは、モデルの継続的な再トレーニング（1分ごと）も含まれていますが、毎時実行されるバッチトレーニングジョブをスケジュールすることで簡略化できます。

-----
_Sparse-feature challenges_ Most user and video features are high-cardinality categorical variables, which, in their raw form, are extremely sparse.
_スパースフィーチャーの課題_ ほとんどのユーザーおよびビデオの特徴は高次元のカテゴリ変数であり、生の形では非常にスパースです。

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
私たちは、埋め込みを使用してスパースフィーチャーデータの問題を解決します。

_Embeddings convert high-dimensional_ sparse features into low-dimensional dense vectors.
_埋め込みは高次元の_ スパースフィーチャーを低次元の密なベクトルに変換します。

However, we have the chal‐ lenge of connecting two different data sources: user behavior data and video data.
ただし、ユーザー行動データとビデオデータという2つの異なるデータソースを接続するという課題があります。

We will address this by training two models (a user-embedding model and a video-embedding model) in a single _two-tower architecture (see next section)_ with interaction data (user events like watching/liking/etc. videos).
私たちは、インタラクションデータ（視聴/いいねなどのユーザーイベント）を使用して、単一の_two-tower architecture_で2つのモデル（ユーザー埋め込みモデルとビデオ埋め込みモデル）をトレーニングすることでこれに対処します。

_Retrieval challenges_ We will retrieve hundreds of candidate videos from a catalog containing billions of videos in a few milliseconds, using similarity search with a vector index.
_リトリーバルの課題_ 数十億のビデオを含むカタログから数百の候補ビデオを数ミリ秒で取得します。ベクトルインデックスを使用した類似性検索を利用します。

We will build a vector index that indexes all of the videos in our system, using the video embedding model, which is trained in our two-tower architecture.
私たちは、私たちのシステム内のすべてのビデオをインデックスするベクトルインデックスを構築します。これは、私たちのtwo-tower architectureでトレーニングされたビデオ埋め込みモデルを使用します。

We will take a user action, along with user history data, and create a vector embedding with the user embedding model.
ユーザーアクションとユーザー履歴データを取り込み、ユーザー埋め込みモデルを使用してベクトル埋め込みを作成します。



We will take a user action, along with user history data, and create a vector embedding with the user embedding model. 
ユーザーのアクションとユーザーの履歴データを取り込み、ユーザー埋め込みモデルを使用してベクトル埋め込みを作成します。

We will query the vector index with the user embedding to find the “nearest” videos. 
ユーザー埋め込みを使用してベクトルインデックスを照会し、「最も近い」動画を見つけます。

Nearest is based on the interaction data— given this user query and history, these are the videos that the user is most likely to click on or watch the longest (you can decide what to optimize for when building your two-tower embedding architecture). 
「最も近い」とは、インタラクションデータに基づいています。このユーザーのクエリと履歴を考慮すると、ユーザーが最もクリックする可能性が高い、または最も長く視聴する動画です（2タワー埋め込みアーキテクチャを構築する際に最適化する内容を決定できます）。

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
目標は、各ユーザーに対してアイテムを所望のメトリックに基づいて順序付けるランキング関数を学習することです。

For example, if you want to optimize for the user engaging with the video, then the highest-probability videos should appear at the very top of each user’s recommended item list(s). 
例えば、ユーザーが動画にエンゲージすることを最適化したい場合、最も高い確率の動画が各ユーザーの推薦アイテムリストの最上部に表示されるべきです。

Note that in 2012, YouTube benefited significantly by changing from optimizing for users clicking on videos (view count) to how long users watch the recommended videos (watch time). 
2012年にYouTubeは、ユーザーが動画をクリックすること（視聴回数）を最適化するのから、ユーザーが推薦された動画をどれだけ長く視聴するか（視聴時間）に変更することで大きな利益を得ました。

Ranking typically uses a low-latency model, such as XGBoost, and real-time features that capture recent trends. 
ランキングは通常、XGBoostのような低遅延モデルと、最近のトレンドを捉えるリアルタイム機能を使用します。

_Scalability challenges_ 
_スケーラビリティの課題_

The system needs to be able to handle millions of concurrent requests and store PBs of data, and it requires compute- and memory-efficient design as well as a highly available architecture to prevent downtime. 
システムは、数百万の同時リクエストを処理し、PB単位のデータを保存できる必要があり、ダウンタイムを防ぐために計算およびメモリ効率の良い設計と高可用性のアーキテクチャが必要です。

For the retrieval phase, we will use Hopsworks’ vector index (OpenSearch), which is partitioned over nodes and replicated for high availability. 
取得フェーズでは、Hopsworksのベクトルインデックス（OpenSearch）を使用します。これはノードに分割され、高可用性のために複製されています。

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

_Data source challenges_ 
_データソースの課題_

We need user profile data, video data, and interaction data to build our personalized video player. 
パーソナライズされたビデオプレーヤーを構築するために、ユーザープロファイルデータ、ビデオデータ、およびインタラクションデータが必要です。

Given the lack of quality open source datasets, we will create synthetic data simulating user interactions with videos. 
質の高いオープンソースデータセットが不足しているため、ユーザーが動画とインタラクションする様子をシミュレートした合成データを作成します。

The most important data source for learning user viewing behavior is the interactions between users and videos. 
ユーザーの視聴行動を学習するための最も重要なデータソースは、ユーザーと動画の間のインタラクションです。

Figure 15-2 shows both positive interactions (such as views and likes) and negative interactions (such as ignoring a recommended video). 
図15-2は、ポジティブなインタラクション（視聴やいいねなど）とネガティブなインタラクション（推薦された動画を無視するなど）の両方を示しています。

We will train embedding models for the retrieval phase that help predict what video a user is likely to watch/like, given their long-term viewing behavior, their recent short-term viewing behavior, and the current viewing behavior of other users. 
私たちは、ユーザーの長期的な視聴行動、最近の短期的な視聴行動、および他のユーザーの現在の視聴行動を考慮して、ユーザーが視聴/いいねする可能性のある動画を予測するのに役立つ取得フェーズのための埋め込みモデルを訓練します。

-----

_Figure 15-2. Interaction data is collected from events such as video watch, no-watch, likes, and shares._ 
_図15-2. インタラクションデータは、動画視聴、未視聴、いいね、シェアなどのイベントから収集されます。_

We will assign an interaction_score for a user interaction with videos that are recommended to the user: 
ユーザーに推薦された動画とのユーザーインタラクションに対してinteraction_scoreを割り当てます：

- 0: The user _did not watch the recommended video (or swiped away the video within a very short period of time). 
- 0: ユーザーは_推薦された動画を視聴しなかった（または非常に短い時間内に動画をスワイプした）。_

- 1: The user watched the recommended video. 
- 1: ユーザーは推薦された動画を視聴しました。

- 2: The user liked the recommended video. 
- 2: ユーザーは推薦された動画にいいねをしました。

- 3: The user shared the recommended video. 
- 3: ユーザーは推薦された動画をシェアしました。

If the user watches a video, we will also measure the watch_time (the length of time the user watched the video for) by computing the time between watching two videos (you could also add a stop watching event, but most viewers will just swipe between videos). 
ユーザーが動画を視聴した場合、2つの動画を視聴する間の時間を計算することでwatch_time（ユーザーが動画を視聴した時間の長さ）を測定します（視聴を停止するイベントを追加することもできますが、ほとんどの視聴者は動画間をスワイプするだけです）。

In the next section, you will design your own personalized, real-time AI-powered recommendation system based on this retrieval-and-ranking architecture, including the data model and the FTI pipelines. 
次のセクションでは、この取得とランキングのアーキテクチャに基づいて、データモデルやFTIパイプラインを含む、独自のパーソナライズされたリアルタイムAI駆動の推薦システムを設計します。

-----

Google popularized the retrieval-and-ranking architecture for personalized recommendations in [“Deep Neural Networks for](https://oreil.ly/nvvyj) [YouTube Recommendations”, published at RecSys 2016. 
Googleは、2016年にRecSysで発表された「YouTube Recommendationsのための深層ニューラルネットワーク」において、パーソナライズされた推薦のための取得とランキングのアーキテクチャを普及させました。

In 2025, Netflix introduced a foundation transformer model for predicting the user’s next interaction. 
2025年、Netflixはユーザーの次のインタラクションを予測するための基盤トランスフォーマーモデルを導入しました。

It will be interesting to see if transformers can disrupt recommendation models in the same way they have disrupted NLP. 
トランスフォーマーがNLPを破壊したのと同じように、推薦モデルを破壊できるかどうかを見るのは興味深いでしょう。

###### Real-Time Personalized Recommender 
###### リアルタイムパーソナライズドレコメンダー

The starting point for your personalized video recommendation system is to build an MVPS (see Chapter 2). 
パーソナライズされた動画推薦システムの出発点は、MVPSを構築することです（第2章を参照）。

The kanban board in Figure 15-3 shows different technologies for the FTI pipelines, the data sources (a Kafka topic and external lakehouse tables), and the prediction consumer—personalized recommendations for a video player. 
図15-3のカンバンボードは、FTIパイプラインのためのさまざまな技術、データソース（Kafkaトピックと外部レイクハウステーブル）、および予測消費者—動画プレーヤーのためのパーソナライズされた推薦を示しています。

For your feature pipelines, you will need stream processing (Feldera), batch processing (Polars), and vector-embedding (PySpark) pipelines. 
フィーチャーパイプラインには、ストリーム処理（Feldera）、バッチ処理（Polars）、およびベクトル埋め込み（PySpark）パイプラインが必要です。

_Figure 15-3. Kanban board for your minimal viable video recommender system._ 
_図15-3. 最小限の実行可能な動画レコメンダーシステムのためのカンバンボード。_

We chose these data transformation frameworks because Feldera and Polars have the easiest learning curve and scale to handle our expected load (millions of users), and we will use PySpark to compute vector embeddings as backfilling vector embeddings from video data is computationally intensive and PySpark can be scaled out to run on many nodes. 
私たちは、FelderaとPolarsが最も学習曲線が緩やかで、予想される負荷（数百万のユーザー）を処理するためにスケールするため、これらのデータ変換フレームワークを選びました。また、PySparkを使用してベクトル埋め込みを計算します。動画データからのベクトル埋め込みのバックフィルは計算集約的であり、PySparkは多くのノードで実行するためにスケールできます。

We will use the two-tower model, with the TensorFlow Recommenders library, for training the user-embedding model and the video-embedding model for our retrieval system. 
私たちは、取得システムのためにユーザー埋め込みモデルと動画埋め込みモデルを訓練するために、TensorFlow Recommendersライブラリを使用して2タワーモデルを使用します。

TensorFlow Recommenders has built-in support for training two-tower embedding models. 
TensorFlow Recommendersは、2タワー埋め込みモデルの訓練をサポートしています。

We will use XGBoost as our ranking model due to its good performance and low-latency for predictions. 
予測の良好なパフォーマンスと低遅延のため、XGBoostをランキングモデルとして使用します。

We will host our online inference pipeline as a Python server (FastAPI) in KServe, and it will be called via a REST API from the video player application. 
私たちは、KServe内のPythonサーバー（FastAPI）としてオンライン推論パイプラインをホストし、動画プレーヤーアプリケーションからREST APIを介して呼び出されます。

We will run the pipelines and deploy the models on Hopsworks. 
私たちはパイプラインを実行し、Hopsworks上にモデルをデプロイします。

Large companies, such as Netflix, use this _retrieval-and-ranking_ architecture for both personalized recommendations and search— “a single contextual recommendation system that can serve all search and recommendation tasks.” 
Netflixのような大企業は、この_取得とランキング_アーキテクチャをパーソナライズされた推薦と検索の両方に使用しています—「すべての検索と推薦タスクに対応できる単一の文脈的推薦システム」。

Netflix has recommendation systems, PreQuery and MoreLikeThis, and a search system built on the same retrieval-and-ranking infrastructure using many of the same data sources and features. 
Netflixには、PreQueryやMoreLikeThisといった推薦システムがあり、同じデータソースや機能を使用して同じ取得とランキングのインフラストラクチャに基づいて構築された検索システムがあります。

A unified platform reduces maintenance costs and enables innovation in search or recommendations to also improve the other. 
統一されたプラットフォームはメンテナンスコストを削減し、検索や推薦の革新が他の改善にもつながることを可能にします。

In the following sections, we will go through the ML pipelines, but first we will design our system architecture, from our data sources to the type of feature pipeline (batch or streaming), the feature groups, and the feature views that we will need for our models. 
次のセクションではMLパイプラインを通じて進めますが、まずはデータソースからフィーチャーパイプラインの種類（バッチまたはストリーミング）、フィーチャーグループ、モデルに必要なフィーチャービューまで、システムアーキテクチャを設計します。

Figure 15-4 shows that our MVPS will need four feature groups and two feature views and will create three models. 
図15-4は、私たちのMVPSが4つのフィーチャーグループと2つのフィーチャービューを必要とし、3つのモデルを作成することを示しています。

_Figure 15-4. Feature groups, feature views, and models for our video recommender._ 
_図15-4. 私たちの動画レコメンダーのためのフィーチャーグループ、フィーチャービュー、およびモデル。_

The figure shows the interaction data arriving in Kafka, a streaming feature pipeline to compute aggregated viewing statistics, batch pipelines to compute user profile, video attributes, and ranking feature data. 
この図は、Kafkaに到着するインタラクションデータ、集約視聴統計を計算するためのストリーミングフィーチャーパイプライン、ユーザープロファイル、動画属性、およびランキングフィーチャーデータを計算するためのバッチパイプラインを示しています。

These feature groups include vector embeddings and some real-time features. 
これらのフィーチャーグループには、ベクトル埋め込みといくつかのリアルタイム機能が含まれています。

Our retrieval system is based on a vector index and requires two embedding models—one for user data and one for video data—and we create a retrieval feature view for those models. 
私たちの取得システムはベクトルインデックスに基づいており、ユーザーデータ用とビデオデータ用の2つの埋め込みモデルが必要です。そして、これらのモデルのために取得フィーチャービューを作成します。

For the ranking model, we also create a ranking feature view. 
ランキングモデルのためにも、ランキングフィーチャービューを作成します。

The code for our pipelines and instructions for how to run the ML pipelines are in the [book’s source code repository. 
私たちのパイプラインのコードとMLパイプラインを実行する方法の指示は、[本のソースコードリポジトリにあります。](https://github.com/featurestorebook/mlfs-book)

We will now look at how to implement the FTI pipelines for our recommender system. 
これから、私たちのレコメンダーシステムのためのFTIパイプラインを実装する方法を見ていきます。

###### Feature Pipelines 
###### フィーチャーパイプライン

We start with the interaction data that arrives as events in a Kafka topic generated by all the video player applications. 
私たちは、すべての動画プレーヤーアプリケーションによって生成されたKafkaトピック内のイベントとして到着するインタラクションデータから始めます。

We assume there is an external event-sourcing pipeline that stores historical interaction events in a lakehouse table. 
外部のイベントソーシングパイプラインがあり、歴史的なインタラクションイベントをレイクハウステーブルに保存していると仮定します。

In the source code repository, we create synthetic interaction data and write it to a Kafka topic. 
ソースコードリポジトリ内で、合成インタラクションデータを作成し、それをKafkaトピックに書き込みます。

The same code can also backfill an `interaction_fg feature group with historical interaction` data. 
同じコードは、`interaction_fgフィーチャーグループに歴史的インタラクション`データをバックフィルすることもできます。

The user profile data will be updated by users in the video player application. 
ユーザープロファイルデータは、動画プレーヤーアプリケーション内のユーザーによって更新されます。

The video attributes will be updated by batch pipelines that run periodically to process new videos uploaded by users. 
動画属性は、ユーザーによってアップロードされた新しい動画を処理するために定期的に実行されるバッチパイプラインによって更新されます。

Figure 15-4 also shows the classes of feature pipelines (batch, streaming, vector embedding) for the feature groups. 
図15-4は、フィーチャーグループのためのフィーチャーパイプラインのクラス（バッチ、ストリーミング、ベクトル埋め込み）も示しています。

Again, we have synthetic data generation programs to create this data. 
再度、私たちはこのデータを生成するための合成データ生成プログラムを持っています。

The prompts for creating the synthetic data generation programs are in the book’s source code repository. 
合成データ生成プログラムを作成するためのプロンプトは、本のソースコードリポジトリにあります。

The feature groups will all be both offline and online. 
フィーチャーグループはすべてオフラインとオンラインの両方で使用されます。

Offline data is used for training, and online data is used for the retrieval and ranking phases. 
オフラインデータは訓練に使用され、オンラインデータは取得とランキングのフェーズに使用されます。

We will need a streaming-feature pipeline to compute windowed aggregations for videos (video_stats_fg): 
動画のウィンドウ集計を計算するためにストリーミングフィーチャーパイプラインが必要です（video_stats_fg）：

``` 
cnt_views_last_{h/d/w/m} 
``` 
The number of views for a video in the previous hour, day, week, and month 
``` 
cnt_views_last_{h/d/w/m} 
``` 
前の1時間、1日、1週間、1ヶ月の動画の視聴回数

``` 
ctr 
``` 
The click-through rate for the previous hour, day, week, and month 
``` 
ctr 
``` 
前の1時間、1日、1週間、1ヶ月のクリック率

And to compute state for user viewing history (user_activity_fg): 
ユーザーの視聴履歴の状態を計算するために（user_activity_fg）：

``` 
recently_viewed 
``` 
The N most recently viewed videos for each user 
``` 
recently_viewed 
``` 
各ユーザーの最近視聴したN本の動画

``` 
last_login 
``` 
The timestamp for when the user last logged in 
``` 
last_login 
``` 
ユーザーが最後にログインした時刻のタイムスタンプ

``` 
mean_session_duration 
``` 
The average duration of a user session for the last week 
``` 
mean_session_duration 
``` 
過去1週間のユーザーセッションの平均時間

``` 
std_session_duration 
``` 
The standard deviation for user session durations for the last week 
``` 
std_session_duration 
``` 
過去1週間のユーザーセッションの時間の標準偏差



We will use Feldera to compute the streaming-feature pipelines, which can also be run in backfill mode to process historical interaction data.
私たちは、Felderを使用してストリーミングフィーチャーパイプラインを計算します。これらは、バックフィルモードで実行して、過去のインタラクションデータを処理することもできます。

The features for videos (excluding video usage statistics) are stored in `video_attrs_fg`. 
動画の特徴（動画使用統計を除く）は、`video_attrs_fg`に保存されています。

It contains features such as the video name, description, genre, and rating that are taken from the videos table in the lakehouse. 
それには、レイクハウスの動画テーブルから取得された動画名、説明、ジャンル、評価などの特徴が含まれています。

It also contains the vector index used for similarity search in our retrieval stage. 
また、取得段階での類似性検索に使用されるベクトルインデックスも含まれています。

You need to periodically update `video_attrs_fg` with a batch vector embedding pipeline, as shown in Figure 15-5.
`video_attrs_fg`をバッチベクトル埋め込みパイプラインで定期的に更新する必要があります。これは、図15-5に示されています。

_Figure 15-5. The vector-embedding pipeline periodically updates the vector index with new videos and new video statistics._
_図15-5. ベクトル埋め込みパイプラインは、新しい動画と新しい動画統計でベクトルインデックスを定期的に更新します。_

We compute the vector embedding using the vector-embedding model (trained on our interaction data, see the next section) with inputs from `videos (name, description, genre, length, rating)` as well as video viewing statistics from `video_stats_fg.` 
私たちは、`videos (name, description, genre, length, rating)`からの入力と、`video_stats_fg`からの動画視聴統計を使用して、インタラクションデータで訓練されたベクトル埋め込みモデルを使用してベクトル埋め込みを計算します。

This combination of features allows our retrieval stage to select videos based not only on their static properties (name, description, genre, rating) but also on dynamic properties, such as their trending score. 
この特徴の組み合わせにより、取得段階では、静的特性（名前、説明、ジャンル、評価）だけでなく、トレンドスコアなどの動的特性に基づいて動画を選択できます。

What if the popularity of a video changes suddenly? 
もし動画の人気が突然変わったらどうなるでしょうか？

The retrieval phase will only adapt to changes in video popularity when the vector index entries are updated. 
取得フェーズは、ベクトルインデックスのエントリが更新されたときにのみ、動画の人気の変化に適応します。

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

However, you probably don’t need to update all entries for every incremental update—you may set a threshold for changes in a video’s popularity and only update the entry if a video’s popularity moves above/below the threshold. 
ただし、すべての増分更新のためにすべてのエントリを更新する必要はないでしょう。動画の人気の変化に対してしきい値を設定し、動画の人気がそのしきい値を超えた場合のみエントリを更新することができます。

This will reduce the number of videos to be updated by a couple of orders of magnitude, allowing you to update your entries at a much higher cadence. 
これにより、更新する動画の数が数桁減少し、エントリをはるかに高い頻度で更新できるようになります。

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

###### Training Pipelines
###### トレーニングパイプライン

We will train our user-embedding and video-embedding models using a single training dataset constructed from the four different feature groups. 
私たちは、4つの異なるフィーチャーグループから構築された単一のトレーニングデータセットを使用して、ユーザ埋め込みモデルと動画埋め込みモデルを訓練します。

For this, we create a feature view, starting from our interaction dataset, mounted as an external `interactions` feature group, which stores our label, interaction_score, and foreign keys to user_id and video_id. 
そのために、インタラクションデータセットから始めて、外部の`interactions`フィーチャーグループとしてマウントされたフィーチャービューを作成します。このフィーチャーグループには、ラベル、interaction_score、user_idおよびvideo_idへの外部キーが保存されています。

We create our feature view by joining in further features from the user_profile_fg, video_attrs_fg, video_stats_fg, and user_activity_fg. 
user_profile_fg、video_attrs_fg、video_stats_fg、およびuser_activity_fgからさらに特徴を結合することで、フィーチャービューを作成します。

Similarly, we create ranking_fv starting from interactions, where we again use the interaction_score as our label. 
同様に、interactionsから始めてranking_fvを作成し、再びinteraction_scoreをラベルとして使用します。

We can use many of the same features, but also real-time features, including on-demand features and features computed in streaming feature pipelines. 
同じ特徴の多くを使用できますが、オンデマンド機能やストリーミングフィーチャーパイプラインで計算された特徴など、リアルタイムの特徴も含めることができます。

The ranking model can react faster to changes in trending videos and user behavior. 
ランキングモデルは、トレンド動画やユーザーの行動の変化により迅速に反応できます。

Figure 15-6 shows how the retrieval-and-ranking feature views are used to create training data for the embedding models and ranking model, respectively.
図15-6は、取得およびランキングフィーチャービューがそれぞれ埋め込みモデルとランキングモデルのトレーニングデータを作成するためにどのように使用されるかを示しています。



_Figure 15-6. Create training datasets using feature views over existing feature groups_ _(tables). Register models with the model registry._
_Figure 15-6. 既存のフィーチャーグループ（テーブル）に対するフィーチャービューを使用してトレーニングデータセットを作成します。モデルをモデルレジストリに登録します。_

We materialize the training data as CSV files from the feature store, as the data volumes may be too large to store in memory in the training pipeline.
トレーニングデータは、データボリュームがトレーニングパイプラインのメモリに保存するには大きすぎる可能性があるため、フィーチャーストアからCSVファイルとして具現化します。

###### Two-tower embedding model
###### ツータワー埋め込みモデル

So far in this book, we have only looked at pretrained embedding models, such as ``` sentence-transformers that transform text into a dense vector representation with a ``` dimension d—the length of the array of floats.
これまでのところ、本書では、テキストを密なベクトル表現に変換する``` sentence-transformers ```のような事前学習済みの埋め込みモデルのみを見てきました。これは、次元$d$、すなわち浮動小数点数の配列の長さです。

We want to train our own custom embedding models with the two-tower model architecture, using the interaction data, user data, and video data.
私たちは、インタラクションデータ、ユーザーデータ、ビデオデータを使用して、ツータワーモデルアーキテクチャで独自のカスタム埋め込みモデルをトレーニングしたいと考えています。

The interaction data tells us that a user with a certain profile and watch history watched a video with a genre, description, and popularity.
インタラクションデータは、特定のプロファイルと視聴履歴を持つユーザーが、ジャンル、説明、人気を持つビデオを視聴したことを示しています。

The interaction data should also include negative samples where the user didn’t watch this video, as well as when the user liked or shared a video.
インタラクションデータには、ユーザーがこのビデオを視聴しなかった場合のネガティブサンプルや、ユーザーがビデオを「いいね」したり共有した場合も含めるべきです。

We will use the interaction data, along with user and video features, to train two different embedding models that link these two different modalities together: users and videos.
私たちは、インタラクションデータとユーザーおよびビデオの特徴を使用して、これら2つの異なるモダリティ（ユーザーとビデオ）を結びつける2つの異なる埋め込みモデルをトレーニングします。

The two-tower model architecture takes as input samples (rows) from the user-video interaction dataset along with the score of each interaction as the label for the sample.
ツータワーモデルアーキテクチャは、ユーザー-ビデオインタラクションデータセットからのサンプル（行）を入力として受け取り、各インタラクションのスコアをサンプルのラベルとして使用します。

We will prepare the training dataset so that we join in columns for:
トレーニングデータセットを準備し、以下の列を結合します：

_User features_ From the user profile and user watch history
_ユーザー特徴_ ユーザープロファイルとユーザー視聴履歴から

_Video features_ Profile, viewing statistics, and videos
_ビデオ特徴_ プロファイル、視聴統計、およびビデオ

The user and video features are fed into two separate neural networks (towers), one for the user features and one for the video features.
ユーザー特徴とビデオ特徴は、それぞれユーザー特徴用とビデオ特徴用の2つの別々のニューラルネットワーク（タワー）に供給されます。

Some examples of features and layers that can be included in each tower are:
各タワーに含めることができる特徴やレイヤーのいくつかの例は次のとおりです：

_User embedding layer_ User IDs and user categorical features
_ユーザー埋め込みレイヤー_ ユーザーIDとユーザーのカテゴリカル特徴

_Video embedding layer_ Video IDs and video categorical features
_ビデオ埋め込みレイヤー_ ビデオIDとビデオのカテゴリカル特徴

_Feedforward layers_ Normalized numerical features like user age and video length
_フィードフォワードレイヤー_ ユーザーの年齢やビデオの長さのような正規化された数値特徴

_Transformer block_ Text features, like video descriptions, and sequential features, like user history
_トランスフォーマーブロック_ ビデオの説明のようなテキスト特徴や、ユーザー履歴のような順次特徴

_CNN_ Image features
_CNN_ 画像特徴

The user tower takes the user features, a user entry, and processes them through any initial layers to the embedding layers (embedding lookup tables for user and video IDs) and then feedforward layers to output a single vector: the user embedding of length _d.
ユーザータワーは、ユーザー特徴、ユーザーエントリを受け取り、初期レイヤーを経て埋め込みレイヤー（ユーザーおよびビデオIDのための埋め込みルックアップテーブル）に処理し、その後フィードフォワードレイヤーを通じて単一のベクトルを出力します：長さ$d$のユーザー埋め込みです。

The video tower takes the video features, a video entry, processes them through initial layers to embedding layers and then feedforward layers, to output a video embedding of length d.
ビデオタワーは、ビデオ特徴、ビデオエントリを受け取り、初期レイヤーを経て埋め込みレイヤーに処理し、その後フィードフォワードレイヤーを通じて長さ$d$のビデオ埋め込みを出力します。

Figure 15-7 shows the architecture, from the training data, to the two embedding towers, to output and loss function.
図15-7は、トレーニングデータから2つの埋め込みタワー、出力および損失関数までのアーキテクチャを示しています。

_Figure 15-7. User-video interaction data is enriched with user and video features and is_ _training data for the two-tower embedding model architecture._
_Figure 15-7. ユーザー-ビデオインタラクションデータは、ユーザーおよびビデオ特徴で強化され、ツータワー埋め込みモデルアーキテクチャのトレーニングデータです。_

The user embedding and video embeddings are compared using a similarity function, such as the dot product or cosine similarity.
ユーザー埋め込みとビデオ埋め込みは、内積やコサイン類似度などの類似度関数を使用して比較されます。

We collapse the output into one of two classes: positive = strong or weak engagement (1, 2, 3) or negative = no engagement (0).
出力を2つのクラスのいずれかにまとめます：ポジティブ = 強いまたは弱いエンゲージメント（1, 2, 3）またはネガティブ = エンゲージメントなし（0）。

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

Do we need negative sampling for recommendation models?
推薦モデルにネガティブサンプリングは必要ですか？

What if the recommendation service itself has not yet been launched and there is no interaction data?
もし推薦サービス自体がまだ開始されておらず、インタラクションデータがない場合はどうなりますか？

If you have some positive samples (viewed, liked), you can use a policy such as random sampling—combining user entries with random videos as negative data to bootstrap your training data.
もしいくつかのポジティブサンプル（視聴、いいね）がある場合、ランダムサンプリングのようなポリシーを使用して、ユーザーエントリをランダムなビデオと組み合わせてネガティブデータとしてトレーニングデータをブートストラップすることができます。

###### Building the vector index of videos
###### ビデオのベクトルインデックスの構築

Once the two-tower model is trained, you need to write a vector-embedding pipeline that can backfill the vector index from the interaction dataset and also incrementally process new entries in the interaction dataset.
ツータワーモデルがトレーニングされたら、インタラクションデータセットからベクトルインデックスをバックフィルし、インタラクションデータセットの新しいエントリを段階的に処理できるベクトル埋め込みパイプラインを書く必要があります。

The vector-embedding pipeline will create a video vector embedding for each row it processes from the interaction dataset and write it to the vector index.
ベクトル埋め込みパイプラインは、インタラクションデータセットから処理する各行に対してビデオベクトル埋め込みを作成し、それをベクトルインデックスに書き込みます。

When the recommender wants to retrieve candidate videos for a user query, it first computes the user vector embedding from the user features with the user embedding model.
レコメンダーがユーザークエリの候補ビデオを取得したい場合、最初にユーザー特徴からユーザー埋め込みモデルを使用してユーザーベクトル埋め込みを計算します。

It then retrieves the top N (typically 50–1,000) candidate videos that are most similar to the provided user embedding, using ANN search on the vector index.
次に、ベクトルインデックス上でANN検索を使用して、提供されたユーザー埋め込みに最も類似した上位N（通常は50〜1,000）の候補ビデオを取得します。

The returned candidate videos should be ranked based using the ranking model.
返された候補ビデオは、ランキングモデルに基づいてランク付けされるべきです。

###### Ranking model
###### ランキングモデル

The ranking model takes as input the _N candidate videos and uses richer features,_ including explicit crossed features between user and video (which the two-tower model struggles with), to precisely rerank them.
ランキングモデルは、_N候補ビデオを入力として受け取り、ユーザーとビデオの間の明示的な交差特徴を含むより豊富な特徴を使用して、正確に再ランク付けします（これはツータワーモデルが苦手とする部分です）。

The ranker can also use more realtime features (on-demand or features computed in streaming feature pipelines), making them more reactive to recent changes in video popularity and user behavior.
ランカーは、よりリアルタイムの特徴（オンデマンドまたはストリーミングフィーチャーパイプラインで計算された特徴）を使用することもでき、ビデオの人気やユーザーの行動の最近の変化に対してより反応的になります。

For example, the ranking model sees “trending score” as one of many input features per video, and it learns how much “trending” matters for each user.
たとえば、ランキングモデルは「トレンドスコア」を各ビデオの多くの入力特徴の1つとして見ており、「トレンド」が各ユーザーにとってどれほど重要であるかを学習します。

The ranking model also needs both negative and positive samples (viewed and not viewed) and can predict more fine-grained interactions, such as likes and shares.
ランキングモデルは、ネガティブサンプルとポジティブサンプル（視聴されたものと視聴されていないもの）の両方が必要であり、いいねや共有などのより細かいインタラクションを予測できます。

Examples of rankers include Wide & Deep, DCN, and DeepFM.
ランカーの例には、Wide & Deep、DCN、DeepFMが含まれます。

One widely used metric for ranking is [normalized discounted cumulative gain](https://oreil.ly/r_D_W) [(NDCG). It compares rankings to an ideal order in which all relevant items are at the](https://oreil.ly/r_D_W) top of the list.
ランキングの一般的に使用される指標の1つは、[正規化割引累積利得](https://oreil.ly/r_D_W)（NDCG）です。これは、ランキングをすべての関連アイテムがリストの上部にある理想的な順序と比較します。

Another popular ranking metric is mean reciprocal rank (MRR).
もう1つの人気のあるランキング指標は、平均逆順位（MRR）です。

Mean average precision (MAP) at K is a ranking metric that helps evaluate the quality of ranking in recommender systems.
Kにおける平均平均精度（MAP）は、レコメンダーシステムにおけるランキングの質を評価するのに役立つランキング指標です。

It measures both the relevance of suggested items and how good the system is at placing more relevant items at the top.
これは、提案されたアイテムの関連性と、システムがより関連性の高いアイテムを上位に配置する能力の両方を測定します。

###### Online Inference Pipeline
###### オンライン推論パイプライン

The _online inference pipeline is a Python predictor script deployed on KServe as a_ FastAPI Python server.
_オンライン推論パイプラインは、KServeにデプロイされたFastAPI PythonサーバーとしてのPython予測スクリプトです。_

It accepts prediction requests and executes steps 2 to 6 before returning the rank-ordered list of recommended videos, as shown in Figure 15-8.
予測リクエストを受け入れ、図15-8に示すように、推奨ビデオのランク順リストを返す前に、ステップ2から6を実行します。

_Figure 15-8. The online inference pipeline, deployed on KServe._
_Figure 15-8. KServeにデプロイされたオンライン推論パイプライン。_

The online inference pipeline is a deployment object with a deployment API that takes in-session features and entity IDs as parameters.
オンライン推論パイプラインは、セッション内の特徴とエンティティIDをパラメータとして受け取るデプロイメントAPIを持つデプロイメントオブジェクトです。

It executes the following steps:
以下のステップを実行します：

_1. Retrieval_ User features are read from the feature store with the `user_id and combined` with the on-demand and passed features.
_1. リトリーバル_ ユーザー特徴は、フィーチャーストアから`user_id`を使用して読み取られ、オンデマンドおよび渡された特徴と結合されます。

These user_features are passed to the user-embedding model that returns the user embedding, which is then sent to the vector index to return 200 candidate videos.
これらのユーザー特徴は、ユーザー埋め込みモデルに渡され、ユーザー埋め込みが返され、その後ベクトルインデックスに送信されて200の候補ビデオが返されます。

_2. Filtering_ We read the features for the 200 candidate videos using `ranking_fv and the` ```   video_ids.
_2. フィルタリング_ `ranking_fv`と``` video_ids ```を使用して200の候補ビデオの特徴を読み取ります。

Now that we have the features for the candidate videos, we know the rating of each video, so we can filter out videos that are not suitable for the user’s age.
候補ビデオの特徴が得られたので、各ビデオの評価がわかり、ユーザーの年齢に適さないビデオをフィルタリングできます。

_3. Ranking_ We finally perform a model.predict() on the DataFrame containing the filtered candidate videos.
_3. ランキング_ 最後に、フィルタリングされた候補ビデオを含むDataFrameに対してmodel.predict()を実行します。

The model executes these predictions in parallel, using all available CPU cores, minimizing the total latency.
モデルは、利用可能なすべてのCPUコアを使用してこれらの予測を並行して実行し、総レイテンシを最小限に抑えます。

-----
The pseudo-code for the online inference pipeline (predictor script) is shown in Figure 15-9, including the calls on the feature store and some estimates for the latencies of each of the steps.
オンライン推論パイプライン（予測スクリプト）の擬似コードは、図15-9に示されており、フィーチャーストアへの呼び出しや各ステップのレイテンシのいくつかの推定が含まれています。

_Figure 15-9. The model deployment stores both the user-embedding model and the rank‐_ _ing model, and it uses the feature store once for candidate retrieval and twice for feature_ _enrichment (you look up user features with user_id and video features with video_id)._
_Figure 15-9. モデルデプロイメントは、ユーザー埋め込みモデルとランキングモデルの両方を保存し、候補取得にフィーチャーストアを1回、特徴強化に2回使用します（ユーザー特徴はuser_idで、ビデオ特徴はvideo_idでルックアップします）。_

The figure shows a target P95 latency of 45 ms, with the breakdown for each step as follows:
図は、各ステップの内訳とともに、目標P95レイテンシが45msであることを示しています：

- Retrieving the user features is a primary key lookup and takes ~1 ms, and the user-embedding computation takes ~4 ms, giving a total of ~5 ms for this step.
- ユーザー特徴の取得はプライマリキーのルックアップであり、約1msかかり、ユーザー埋め込み計算は約4msかかるため、このステップの合計は約5msです。

- ANN search on the vector index takes ~10 ms (if you have hundreds of millions of videos, your query and vector index will need serious tuning to keep the latency this low).
- ベクトルインデックス上のANN検索は約10msかかります（数億のビデオがある場合、クエリとベクトルインデックスはこのレイテンシを低く保つために真剣な調整が必要です）。



- Filtering out the unsuitable videos is done in memory in Python and should take <1 ms.
- 不適切な動画のフィルタリングは、Pythonのメモリ内で行われ、1ミリ秒未満で完了するはずです。
- A batch primary key lookup for the video features in the feature store takes ~23 ms.
- フィーチャーストア内の動画フィーチャーに対するバッチプライマリキーの検索には約23ミリ秒かかります。
- A ranking score estimated by the ranking model for each candidate video, performing the predictions in parallel on all available CPU cores, takes ~5 ms.
- ランキングモデルによって各候補動画に対して推定されたランキングスコアは、すべての利用可能なCPUコアで並行して予測を行うため、約5ミリ秒かかります。
- Asynchronous logging of the input features and predictions takes ~1 ms.
- 入力フィーチャーと予測の非同期ログ記録には約1ミリ秒かかります。
We assume that computing on-demand features takes less than 1 ms, giving a total of roughly 45 ms.
オンデマンドフィーチャーの計算には1ミリ秒未満かかると仮定し、合計で約45ミリ秒となります。
If you have a high standard deviation for the vector index and feature store lookups, you should be aware of the _[tail at scale, where p99 latencies can](https://oreil.ly/l7f0i)_ increase significantly.
ベクトルインデックスとフィーチャーストアの検索に高い標準偏差がある場合、_「スケールでのテール、p99のレイテンシが大幅に増加する可能性がある」_ことに注意する必要があります。
Given that we are logging all features and prediction requests for the ranking model, we can monitor its performance by writing a model-monitoring job, similar to how we did in Chapter 14.
ランキングモデルのためにすべてのフィーチャーと予測リクエストをログ記録しているため、Chapter 14で行ったようにモデルモニタリングジョブを書くことでそのパフォーマンスを監視できます。
The outcomes become available in the interaction data (you should wait a few minutes for users to either view the recommendations or not), and you can easily compare predictions with outcomes.
結果はインタラクションデータに利用可能になり（ユーザーが推薦を視聴するかどうか数分待つ必要があります）、予測と結果を簡単に比較できます。
If the prediction performance degrades, you will need to retrain your ranking model or redesign it.
予測性能が低下した場合、ランキングモデルを再訓練するか、再設計する必要があります。
Or the prediction performance could be the result of upstream problems in the retrieval phase, in which case you may need to retrain or redesign the embedding models.
また、予測性能は取得フェーズの上流の問題の結果である可能性があり、その場合は埋め込みモデルを再訓練または再設計する必要があります。

###### Agentic Search for Videos
###### 動画のエージェンティック検索

Your real-time recommendation system is the cash cow that should engage users for longer on your video player.
あなたのリアルタイム推薦システムは、ユーザーを動画プレーヤーでより長く引きつけるべきキャッシュカウです。
But now, you want to wow your users with new AI-powered features.
しかし今、あなたは新しいAI駆動の機能でユーザーを驚かせたいと考えています。
You could extend the system by allowing users to search for videos using free text.
ユーザーが自由なテキストを使用して動画を検索できるようにすることで、システムを拡張できます。
You could also add new feature pipelines that transcribe your videos, extract frames from them, and allow users to attach tags describing key moments in videos.
また、動画を文字起こしし、フレームを抽出し、ユーザーが動画の重要な瞬間を説明するタグを付けることを可能にする新しいフィーチャーパイプラインを追加することもできます。
Figure 15-10 shows the architecture of an agent that can provide such free-text search capabilities, powered by LLMs.
図15-10は、LLMによって駆動されるそのような自由テキスト検索機能を提供できるエージェントのアーキテクチャを示しています。

_Figure 15-10. Agentic search for videos using video and user context information._
_図15-10. 動画とユーザーコンテキスト情報を使用した動画のエージェンティック検索_

Users can watch a video and ask questions about moments or scenes in the video.
ユーザーは動画を視聴し、動画の瞬間やシーンについて質問できます。
We can then use the active video_id to retrieve video_tags for that video, and an LLM will determine from the descriptions of the tags which one is most appropriate and change the offset in the video to pos_ms in the selected video_tags row.
その後、アクティブなvideo_idを使用してその動画のvideo_tagsを取得し、LLMがタグの説明から最も適切なものを判断し、選択されたvideo_tags行の動画内のオフセットをpos_msに変更します。
When a user is watching a video, the agent (powered by the LLM) will interpret the natural language query, retrieve all `video_tags for the current` `video_id, and select the most` relevant one.
ユーザーが動画を視聴しているとき、エージェント（LLMによって駆動される）は自然言語クエリを解釈し、現在の`video_id`に対するすべての`video_tags`を取得し、最も関連性の高いものを選択します。
The system will then seek the `pos_ms timestamp associated with that` tag.
システムはそのタグに関連付けられた`pos_ms`タイムスタンプを探します。



Similarly, a user can ask questions about all videos, and an ANN search of the transcripts vector index can be used to find the most similar video transcripts and then play the matched video. 
同様に、ユーザーはすべてのビデオに関する質問をすることができ、トランスクリプトベクトルインデックスのANN検索を使用して最も類似したビデオトランスクリプトを見つけ、その後一致したビデオを再生することができます。

For queries over all videos, the agent can perform an ANN search of the transcripts vector index or the videos vector index to find semantically similar segments or full videos and then play the top match. 
すべてのビデオに対するクエリの場合、エージェントはトランスクリプトベクトルインデックスまたはビデオベクトルインデックスのANN検索を実行して、意味的に類似したセグメントやフルビデオを見つけ、その後トップマッチを再生することができます。

That concludes our case study, and I will finish off the book with some advice on what _not to do. 
これで私たちのケーススタディは終了し、私は本書を何をしてはいけないかについてのアドバイスで締めくくります。

It’s a summary of many of the lessons we learned throughout the book, with a bit of wit thrown in. 
これは、本書を通じて学んだ多くの教訓の要約であり、少しのウィットが加えられています。

###### The Dirty Dozen of Fallacies of MLOps
###### MLOpsの誤謬のダーティダース

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

###### The Ethical Responsibilities of AI Builders
###### AIビルダーの倫理的責任

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

###### Summary
###### 要約

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
前進して創造し、力があなたと共にあらんことを。



###### A A/B tests for agents, 444 for batch inference, 397
A/Bテストエージェント用、444 バッチ推論用、397

ablation studies, 301 Adam (Adaptive Moment Estimation) optimizer, 285
アブレーションスタディ、301 Adam（適応モーメント推定）オプティマイザー、285

ADF (Azure Data Factory), 225 Agent Cards, 368-369 agent traces, 436
ADF（Azure Data Factory）、225 エージェントカード、368-369 エージェントトレース、436

agent-to-agent (A2A) protocol, 368-370 agentic pipeline, 44 agentic workflow pattern, 372
エージェント間（A2A）プロトコル、368-370 エージェントパイプライン、44 エージェントワークフローパターン、372

agentic workflows, defined, 21 agents (agentic AI systems), 5
エージェントワークフロー、定義、21 エージェント（エージェントAIシステム）、5

agent deployments in Hopsworks, 377-378 agent-to-agent (A2A) protocol, 368-370 defined, 14
Hopsworksにおけるエージェントのデプロイ、377-378 エージェント間（A2A）プロトコル、368-370 定義、14

development process for agents, 375-376 evals for, 397-402
エージェントの開発プロセス、375-376 評価、397-402

LLM-assisted synthetic eval generation, 400-401
LLM支援による合成評価生成、400-401

point-in-time correct RAG data for historical evals, 402
歴史的評価のための時点正確なRAGデータ、402

evolution from LLM workflows to agents, 370-375 domain-specific (intermediate) representations, 375
LLMワークフローからエージェントへの進化、370-375 ドメイン特化型（中間）表現、375

planning, 373-374 security challenges, 374
計画、373-374 セキュリティの課題、374

evolution from LLMs to agents, 342-355
LLMからエージェントへの進化、342-355

agents and workflows with LlamaIndex, 352-355
LlamaIndexを用いたエージェントとワークフロー、352-355

context window, 350-351
コンテキストウィンドウ、350-351  

##### Index
インデックス

prompt engineering, 348-350 prompt management, 345-348
プロンプトエンジニアリング、348-350 プロンプト管理、345-348

LLM workflows versus, 372, 374 logging and metrics, 436-445
LLMワークフロー対、372, 374 ロギングとメトリクス、436-445

error analysis, 438-442 guardrails, 443-444 jailbreaking and prompt injection, 444
エラー分析、438-442 ガードレール、443-444 ジェイルブレイキングとプロンプトインジェクション、444

LLM metrics, 445 online A/B testing, 444 traces, 437
LLMメトリクス、445 オンラインA/Bテスト、444 トレース、437

aggregations, 154
集約、154

(see also rolling aggregations; windowed aggregations) AI lakehouse, 77
（ローリング集約およびウィンドウ集約も参照）AIレイクハウス、77

AI systems (generally) defined, 19 feature/training/inference (FTI) pipelines, 18-20
AIシステム（一般的に）定義、19 特徴/トレーニング/推論（FTI）パイプライン、18-20

ML systems versus, 15
MLシステム対、15

air quality forecasting service (case study), 49-71
空気質予測サービス（ケーススタディ）、49-71

AI system overview, 50-52 air quality data, 52-54
AIシステムの概要、50-52 空気質データ、52-54

batch inference pipeline, 62-64 creating/backfilling feature groups, 57-58
バッチ推論パイプライン、62-64 特徴グループの作成/バックフィリング、57-58

exploratory dataset analysis, 54-57 air quality data, 54-55 weather data, 56-57
探索的データセット分析、54-57 空気質データ、54-55 天気データ、56-57

feature pipeline, 58-59 function calling with LLMs, 67-70
特徴パイプライン、58-59 LLMを用いた関数呼び出し、67-70

running the pipelines, 64-67 building dashboard as GitHub Page, 67
パイプラインの実行、64-67 GitHubページとしてダッシュボードを構築、67

scheduling pipelines as GitHub action, 65-66  
GitHubアクションとしてパイプラインをスケジュール、65-66

training pipeline, 59-62
トレーニングパイプライン、59-62

Airflow, 224 algorithmic evals, 441
Airflow、224 アルゴリズム評価、441

Apache Airflow, 224 Apache Flink, 41, 246
Apache Airflow、224 Apache Flink、41, 246

Apache Iceberg, 408 Apache Kafka, 7, 210
Apache Iceberg、408 Apache Kafka、7, 210

Apache Spark, 41 API-scraped data, 8, 212
Apache Spark、41 APIスクレイピングデータ、8, 212

Arize, 414 arrange, act, assert pattern, 201
Arize、414 配列、行動、主張パターン、201

Arrow, 161-165 ASOF JOINs, 260-262
Arrow、161-165 ASOF JOIN、260-262

atomicity, 40 audit logs, 408
原子性、40 監査ログ、408

automatic containerization, 220, 385-389
自動コンテナ化、220, 385-389

environments and jobs in Hopsworks, 386-389
Hopsworksにおける環境とジョブ、386-389

Modal jobs, 389
モーダルジョブ、389

autoregressive models, 268 AWS SageMaker, 415
自己回帰モデル、268 AWS SageMaker、415

AWS Step Functions, 225 Azure Data Factory (ADF), 225
AWS Step Functions、225 Azure Data Factory（ADF）、225

###### B backfilling batch data sources for, 207
バッチデータソースのバックフィリング、207

batch feature pipelines, 218 defined, 205, 216
バッチ特徴パイプライン、218 定義、205, 216

full loads versus, 216
フルロード対、216

backpressure, 242 backward filling, 182
バックプレッシャー、242 バックワードフィリング、182

batch data pipelines, 206 batch feature pipelines, 39, 205-229
バッチデータパイプライン、206 バッチ特徴パイプライン、39, 205-229

backfilling/incremental updates, 216-219
バックフィリング/インクリメンタル更新、216-219

backfill/incremental processing in one program, 218
1つのプログラムでのバックフィル/インクリメンタル処理、218

polling and CDC for incremental data, 217-218
インクリメンタルデータのためのポーリングとCDC、217-218

data contracts, 225 data validation with Great Expectations in Hopsworks, 226-229
データ契約、225 HopsworksにおけるGreat Expectationsによるデータ検証、226-229

feature pipeline data sources, 207-212
特徴パイプラインデータソース、207-212

API and SaaS sources, 212 batch data sources, 207-210
APIおよびSaaSソース、212 バッチデータソース、207-210

streaming data sources, 210 unstructured data in object stores/file systems, 211-212  
ストリーミングデータソース、210 オブジェクトストア/ファイルシステム内の非構造化データ、211-212

job orchestrators, 219-223
ジョブオーケストレーター、219-223

Hopsworks Jobs, 221-223 Modal, 220-221
Hopsworksジョブ、221-223 モーダル、220-221

synthetic credit card data with LLMs, 213-216
LLMを用いた合成クレジットカードデータ、213-216

LLM prompts for generating synthetic data, 215-216
合成データ生成のためのLLMプロンプト、215-216

logical model for data mart and LLM, 213-214
データマートとLLMのための論理モデル、213-214

workflow orchestrators, 223-225
ワークフローオーケストレーター、223-225

Airflow, 224 cloud providers, 225
Airflow、224 クラウドプロバイダー、225

batch inference, 104, 397 batch inference data, 137-138
バッチ推論、104, 397 バッチ推論データ、137-138

batch inference pipelines, 43, 309-317
バッチ推論パイプライン、43, 309-317

air quality forecasting service case study, 62-64
空気質予測サービスケーススタディ、62-64

batch inference for LLMs, 318-320
LLMのためのバッチ推論、318-320

batch inference for neural networks, 317
ニューラルネットワークのためのバッチ推論、317

batch predictions for entities, 312-313
エンティティのためのバッチ予測、312-313

batch predictions for time range, 310-312
時間範囲のためのバッチ予測、310-312

data modeling for batch inference, 315-317
バッチ推論のためのデータモデリング、315-317

saving batch inference with PySpark, 314-315
PySparkを用いたバッチ推論の保存、314-315

batch jobs, metrics for, 420-421
バッチジョブ、メトリクス、420-421

batch ML systems, 4, 10, 21
バッチMLシステム、4, 10, 21

batch models, logging for, 412-417
バッチモデル、ロギング、412-417

batch processing, 205 benchmarking, 248
バッチ処理、205 ベンチマーキング、248

BERT transformer model, 268 bias model bias tests, 301
BERTトランスフォーマーモデル、268 バイアスモデルバイアステスト、301

training pipeline tests for, 394-395
トレーニングパイプラインテスト、394-395

classification models, 300 classification problems, supervised learning for solving, 5
分類モデル、300 分類問題、解決のための教師あり学習、5

Claude, 345 CleanLab, 184
Claude、345 CleanLab、184

CNNs (convolutional neural networks), 284 Colab (Google Colaboratory) notebooks, 31, 54
CNN（畳み込みニューラルネットワーク）、284 Colab（Google Colaboratory）ノートブック、31, 54

cold-start problem, 420 collaboration, feature stores for, 82-83
コールドスタート問題、420 コラボレーション、特徴ストアのために、82-83

collaborative filtering, 448 Complex Event Processing (CEP) library, 247
コラボレーティブフィルタリング、448 複雑イベント処理（CEP）ライブラリ、247

concept drift, 426 Confidence-Based Performance Estimation (CBPE), 433-434
概念ドリフト、426 信頼に基づくパフォーマンス推定（CBPE）、433-434

content-based recommendation, 447 context length, 350
コンテンツベースの推薦、447 コンテキスト長、350

context window, 14 continuous deployment (CD), 17
コンテキストウィンドウ、14 継続的デプロイメント（CD）、17

continuous integration (CI) platforms, 17 convolutional neural networks (CNNs), 284
継続的インテグレーション（CI）プラットフォーム、17 畳み込みニューラルネットワーク（CNN）、284

cross-entropy loss, 285 CSV file format, 278
クロスエントロピー損失、285 CSVファイル形式、278

###### D DAG (see directed acyclic graph) data accuracy, 54
DAG（有向非巡回グラフを参照） データ精度、54

data cleaning, 184 data contracts, 30, 225
データクリーニング、184 データ契約、30, 225

data ingestion drift, 426, 429-430 data leakage, 80
データ取り込みドリフト、426, 429-430 データ漏洩、80

data modeling, 315-317 data models, 92-102
データモデリング、315-317 データモデル、92-102

data pipelines, defined, 206 data reconstruction using PCA, 431
データパイプライン、定義、206 PCAを用いたデータ再構成、431

data skipping, 119, 139 data sources, for ML system, 7-8
データスキップ、119, 139 MLシステムのためのデータソース、7-8

API-scraped data, 8 event data, 7
APIスクレイピングデータ、8 イベントデータ、7

graph data, 8 tabular data, 7 unstructured data, 8
グラフデータ、8 表形式データ、7 非構造化データ、8

data validation feature stores and, 92 Great Expectations in Hopsworks, 226-229  
データ検証、特徴ストアと、92 HopsworksにおけるGreat Expectations、226-229

WAP pattern, 227
WAPパターン、227

data validity, 54 data vault model, 94
データの有効性、54 データボールトモデル、94

data versioning, 119 data-centric AI, 267
データバージョニング、119 データ中心のAI、267

data-parallel training, 290 Databricks, 415
データ並列トレーニング、290 Databricks、415

dataflow graph, 159 dataflow program, 242
データフローグラフ、159 データフロープログラム、242

dataflow programming, 243 DataFrames data transformations for, 151-158
データフロープログラミング、243 DataFramesのデータ変換、151-158

join transformations, 158 row- and column-size increasing transformations, 157
結合変換、158 行および列サイズ増加変換、157

row- and column-size reducing transformations, 154-157
行および列サイズ減少変換、154-157

row-size preserving transformations, 153-154
行サイズ保持変換、153-154

feature functions and, 32-33 MITs and, 151-158
特徴関数と、32-33 MITと、151-158

datastreams, defined, 243 DBSP (DataBase inspired by Signal Processing), 257
データストリーム、定義、243 DBSP（信号処理に触発されたデータベース）、257

decision tree-based models, 178, 284 decorators, for automatic containerization, 220
決定木ベースのモデル、178, 284 デコレーター、自動コンテナ化のために、220

deployment API for models/feature views, 324-328
モデル/特徴ビューのためのデプロイメントAPI、324-328

dimension modeling feature groups and, 94-98 feature stores and SCD types, 96-98
次元モデリング、特徴グループと、94-98 特徴ストアとSCDタイプ、96-98

labels and features, 96 direct grading, 376
ラベルと特徴、96 直接評価、376

Direct Loss Estimation (DLE), 433 directed acyclic graph (DAG) feature functions, 158-168
直接損失推定（DLE）、433 有向非巡回グラフ（DAG）特徴関数、158-168

data types, 165-168 Lazy DataFrames, 160
データ型、165-168 レイジーデータフレーム、160

vectorized compute/multicore/Arrow, 160-165
ベクトル化計算/マルチコア/Arrow、160-165

job orchestrators and, 223
ジョブオーケストレーターと、223

Discovery Weekly (Spotify), 4 distributed training identifying bottlenecks in, 296-299
Discovery Weekly（Spotify）、4 分散トレーニング、ボトルネックの特定、296-299

Ray and, 290-292 DLE (Direct Loss Estimation), 433
Rayと、290-292 DLE（直接損失推定）、433

domain classifier, 432 drift detection, 422-436
ドメイン分類器、432 ドリフト検出、422-436

data ingestion drift, 429-430 multivariate feature drift, 431-432  
データ取り込みドリフト、429-430 多変量特徴ドリフト、431-432

univariate feature drift, 430 dynamic RBAC, 114
単変量特徴ドリフト、430 動的RBAC、114

###### E eager evaluation, 160 EDA (exploratory data analysis), 28, 36
イーガー評価、160 EDA（探索的データ分析）、28, 36

embedded (edge) ML systems, 22 embedded models, inference with, 335-339
埋め込み（エッジ）MLシステム、22 埋め込みモデル、推論、335-339

embedded AI-enabled applications, 336 stream-processing AI-enabled applications, 337-338
埋め込みAI対応アプリケーション、336 ストリーム処理AI対応アプリケーション、337-338

UIs for AI-enabled applications in Python, 338-339
PythonにおけるAI対応アプリケーションのUI、338-339

embedding drift, 432 error analysis, 438-442
埋め込みドリフト、432 エラー分析、438-442

curating evals, 441-442 log traces for, 376
評価のキュレーション、441-442 ログトレース、376

log viewer and feedback, 441
ログビューアとフィードバック、441

ethical responsibilities of AI builders, 472 ETL pipelines, 206
AIビルダーの倫理的責任、472 ETLパイプライン、206

evals agents, 397-402 curating, 441-442
評価エージェント、397-402 キュレーション、441-442

LLM-assisted synthetic eval generation, 400-401
LLM支援による合成評価生成、400-401

point-in-time correct RAG data for historical evals, 402
歴史的評価のための時点正確なRAGデータ、402

evaluation data, 299, 301 evaluator (program), 399
評価データ、299, 301 評価者（プログラム）、399

event data, 7 event sourcing, 96, 241
イベントデータ、7 イベントソーシング、96, 241

event-streaming platforms, 7, 233 experiment tracking services, 290
イベントストリーミングプラットフォーム、7, 233 実験トラッキングサービス、290

explicit schemas, 167 exploratory data analysis (EDA), 28, 36
明示的スキーマ、167 探索的データ分析（EDA）、28, 36

exponential transformation, formula for, 179 external feature groups, 129, 218
指数変換、公式、179 外部特徴グループ、129, 218

###### F fact table, 95 factorization machines, 448
ファクトテーブル、95 ファクタリゼーションマシン、448

FastAPI, 322-323 Feast feature store, 77
FastAPI、322-323 Feastフィーチャーストア、77

feature data, 88 feature data validation pipeline, 39
特徴データ、88 特徴データ検証パイプライン、39

feature definitions, 89 feature drift, 426
特徴定義、89 特徴ドリフト、426

feature engineering, 10 feature freshness, 41  
特徴エンジニアリング、10 特徴の新鮮さ、41

feature functions, 32-33 feature groups, 86-92
特徴関数、32-33 特徴グループ、86-92

creating/backfilling for air quality forecasting service, 57-58
空気質予測サービスのための作成/バックフィリング、57-58

data models, 92-102 data validation, 92
データモデル、92-102 データ検証、92

dimension modeling with credit card data mart, 94-98
クレジットカードデータマートを用いた次元モデリング、94-98

external, 129 feature definitions and, 89
外部、129 特徴定義と、89

feature freshness, 91 Hopsworks, 116-131
特徴の新鮮さ、91 Hopsworks、116-131

real-time credit card fraud detection ML system, 98-102
リアルタイムクレジットカード詐欺検出MLシステム、98-102

root/label feature groups, 272-273 storage of untransformed feature data, 88
ルート/ラベル特徴グループ、272-273 変換されていない特徴データの保存、88

storing transformed feature data in, 180 unstructured data/labels in, 267-271
変換された特徴データの保存、180 非構造化データ/ラベル、267-271

vector indexes in, 127 versioning, 122-125
ベクトルインデックス、127 バージョニング、122-125

writing to, 89-92
書き込み、89-92

feature hashing, 175 feature pipelines, 39-41
特徴ハッシング、175 特徴パイプライン、39-41

air quality forecasting service case study, 58-59
空気質予測サービスケーススタディ、58-59

Feldera and, 262-263 functions of, 20
Felderaと、262-263 機能、20

MITs and, 148-151 testing, 391-394
MITと、148-151 テスト、391-394

TikTok personalized recommender system, 456-458
TikTokパーソナライズドレコメンダーシステム、456-458

writing streaming feature pipelines, 242-248
ストリーミング特徴パイプラインの作成、242-248

Apache Flink, 246 benchmarking, 248
Apache Flink、246 ベンチマーキング、248

dataflow programming, 243 Feldera, 247
データフロープログラミング、243 Feldera、247

stateless/stateful data transformations, 244-246
ステートレス/ステートフルデータ変換、244-246

feature platform, 77 feature registry, 83
特徴プラットフォーム、77 特徴レジストリ、83

feature reuse, 83 feature selection, 273-276
特徴再利用、83 特徴選択、273-276

feature skew, 84 feature stores (generally), 75-109
特徴スキュー、84 特徴ストア（一般的に）、75-109

anatomy, 78-80 brief history, 77
解剖学、78-80 簡潔な歴史、77

classes of AI systems with, 21-23 data model for inference, 102-104
AIシステムのクラス、21-23 推論のためのデータモデル、102-104

batch inference, 104 online inference, 103  
バッチ推論、104 オンライン推論、103

defined, 75 feature groups, 86-92
定義、75 特徴グループ、86-92

fraud protection system with, 76-77 Hopsworks (see Hopsworks feature store)
詐欺防止システム、76-77 Hopsworks（Hopsworksフィーチャーストアを参照）

labels in Spine DataFrames, 101 reading feature data with feature view, 104-108
Spine DataFrames内のラベル、101 特徴ビューでの特徴データの読み取り、104-108

online inference with feature view, 108 point-in-time correct training data with feature views, 106-108
特徴ビューを用いたオンライン推論、108 特徴ビューを用いた時点正確なトレーニングデータ、106-108

uses, 80-85
使用例、80-85

centralizing data for AI in a single platform, 84-85
AIのためのデータを単一プラットフォームに集中化、84-85

context/history in real-time ML systems, 80
リアルタイムMLシステムにおけるコンテキスト/履歴、80

discovery/reuse of AI assets, 83 elimination of offline–online feature skew, 84
AI資産の発見/再利用、83 オフライン–オンライン特徴スキューの排除、84

governance of ML systems, 83 improved collaboration with FTI pipeline architecture, 82-83
MLシステムのガバナンス、83 FTIパイプラインアーキテクチャによるコラボレーションの改善、82-83

time-series data, 80-81
時系列データ、80-81

feature transformations, 173-180
特徴変換、173-180

distributions of numerical variables, 175-177
数値変数の分布、175-177



governance of ML systems, 83 improved collaboration with FTI pipe‐ line architecture, 82-83
MLシステムのガバナンス、83 FTIパイプラインアーキテクチャとの協力の改善、82-83

time-series data, 80-81
時系列データ、80-81

feature transformations, 173-180
特徴変換、173-180

distributions of numerical variables, 175-177
数値変数の分布、175-177

encoding categorical variables, 174-175
カテゴリ変数のエンコーディング、174-175

storing transformed feature data in a feature group, 180
特徴グループに変換された特徴データを保存する、180

transforming numerical variables, 178-180
数値変数の変換、178-180

feature types, 34-35
特徴タイプ、34-35

feature views, 46
特徴ビュー、46

Hopsworks feature store, 131-139
Hopsworksフィーチャーストア、131-139

batch inference data, 137-138
バッチ推論データ、137-138

creating feature views, 134-135
特徴ビューの作成、134-135

feature selection, 131-133
特徴選択、131-133

model-dependent transformations, 133
モデル依存の変換、133

online inference data, 138
オンライン推論データ、138

training data as either DataFrames of files, 135-137
トレーニングデータはDataFrameまたはファイルのいずれかとして、135-137

online inference with, 108
オンライン推論、108

point-in-time correct training data with, 106-108
時点正確なトレーニングデータ、106-108

reading feature data with, 104-108
特徴データの読み取り、104-108

transformations in, 189-193
変換、189-193

feature/training/inference (FTI) pipelines, 18-20, 82-83
特徴/トレーニング/推論（FTI）パイプライン、18-20、82-83

feed-forward neural NNs, 284
フィードフォワードニューラルネットワーク、284

Feldera, 41, 247
Feldera、41、247

incremental view maintenance, 257
インクリメンタルビューのメンテナンス、257

lagged features/feature pipelines, 262-263
遅延特徴/フィーチャーパイプライン、262-263

Flink, 246
Flink、246

foreign key, 118
外部キー、118

freshness, of feature data, 41
特徴データの新鮮さ、41

FTI (feature/training/inference) pipelines, 18-20, 82-83
FTI（特徴/トレーニング/推論）パイプライン、18-20、82-83

full load, 216
フルロード、216

full table scan, 210
フルテーブルスキャン、210

function-calling LLMs, 361, 363
関数呼び出しLLM、361、363

###### G

GDPR (General Data Protection Regulation), 9
GDPR（一般データ保護規則）、9

generative adversarial network (GAN), 269
生成的敵対ネットワーク（GAN）、269

GitHub Actions running pytest as part of, 201
GitHub Actionsがpytestを実行する、201

scheduling pipelines for air quality forecast‐ ing service, 65-66
空気質予測サービスのためのパイプラインのスケジューリング、65-66

GitHub Page, 67
GitHubページ、67

global window, 251
グローバルウィンドウ、251

Google Cloud Composer, 225
Google Cloud Composer、225

Google Colaboratory (Colab) notebooks, 31, 54
Google Colaboratory（Colab）ノートブック、31、54

governance, 402-409
ガバナンス、402-409

audit logs, 408
監査ログ、408

feature stores for, 83
のためのフィーチャーストア、83

lineage, 405-406
系譜、405-406

schematized tags, 402-405
スキーマ化されたタグ、402-405

versioning, 406-408
バージョン管理、406-408

GPUs, 287
GPU、287

graph data, 8
グラフデータ、8

GraphRAG, 360
GraphRAG、360

Great Expectations, 226-229
Great Expectations、226-229

guardrails, 443-444
ガードレール、443-444

###### H

hardware accelerators, 287
ハードウェアアクセラレーター、287

Hierarchical Data Format 5 (HDF5), 278
階層データ形式5（HDF5）、278

Hive-style partitioning, 119
Hiveスタイルのパーティショニング、119

hopping (sliding) windows, 253-256
ホッピング（スライディング）ウィンドウ、253-256

Hopsworks agent deployments in, 377-378
Hopsworksエージェントのデプロイメント、377-378

audit logs, 408
監査ログ、408

CI/CD architecture for, 383-385
のためのCI/CDアーキテクチャ、383-385

data validation with Great Expectations, 226-229
Great Expectationsによるデータ検証、226-229

environments and jobs, 386-389
環境とジョブ、386-389

first open source feature store, 77
最初のオープンソースフィーチャーストア、77

transformations in feature views, 189-193
特徴ビューにおける変換、189-193

Hopsworks feature store, 111-141
Hopsworksフィーチャーストア、111-141

faster queries for feature data, 139-141
特徴データのためのより速いクエリ、139-141

feature groups, 116-131
フィーチャーグループ、116-131

change data capture, 130
変更データキャプチャ、130

offline store (lakehouse tables), 129-130
オフラインストア（レイクハウステーブル）、129-130

online store, 125-128
オンラインストア、125-128

versioning, 119-125
バージョン管理、119-125

feature views, 131-139
特徴ビュー、131-139

batch inference data, 137-138
バッチ推論データ、137-138

creating feature views, 134-135
特徴ビューの作成、134-135

feature selection, 131-133
特徴選択、131-133

model-dependent transformations, 133
モデル依存の変換、133

online inference data, 138
オンライン推論データ、138

training data as either DataFrames of files, 135-137
トレーニングデータはDataFrameまたはファイルのいずれかとして、135-137

projects, 111-115
プロジェクト、111-115

access control at cluster level using projects, 113-115
プロジェクトを使用したクラスターレベルでのアクセス制御、113-115

access controls within projects, 113
プロジェクト内のアクセス制御、113

storing files in a project, 112
プロジェクト内にファイルを保存する、112

Hopsworks Jobs, 221-223
Hopsworksジョブ、221-223

hybrid streaming-batch architecture, 238-239
ハイブリッドストリーミングバッチアーキテクチャ、238-239

hyperparameter tuning, 135, 279, 288-290
ハイパーパラメータチューニング、135、279、288-290

###### I

i2i (item-to-item) recommendation, 448
i2i（アイテム間）推薦、448

idempotence, 40
冪等性、40

immutable datasets, 8
不変データセット、8

implicit schemas, 167
暗黙のスキーマ、167

in-context learning, 6, 349
文脈内学習、6、349

incremental load, 216
インクリメンタルロード、216

incremental queries, 120
インクリメンタルクエリ、120

incremental updates, 216-219
インクリメンタルアップデート、216-219

backfill/incremental processing in one pro‐ gram, 218
1つのプログラムでのバックフィル/インクリメンタル処理、218

polling and CDC for incremental data, 217-218
インクリメンタルデータのためのポーリングとCDC、217-218

incremental views, rolling aggregations with, 256-258
インクリメンタルビュー、ローリング集計を使用して、256-258

inference helper columns, 193
推論ヘルパーカラム、193

inference pipelines, 42-44, 309-340
推論パイプライン、42-44、309-340

batch inference for LLMs, 318-320
LLMのためのバッチ推論、318-320

batch inference pipelines, 309-317
バッチ推論パイプライン、309-317

batch inference for neural networks, 317
ニューラルネットワークのためのバッチ推論、317

batch predictions for entities, 312-313
エンティティのためのバッチ予測、312-313

batch predictions for time range, 310-312
時間範囲のためのバッチ予測、310-312

data modeling for batch inference, 315-317
バッチ推論のためのデータモデリング、315-317

saving batch inference with PySpark, 314-315
PySparkを使用したバッチ推論の保存、314-315

defined, 309
定義、309

functions of, 20
の機能、20

inference with embedded models, 335-339
埋め込まれたモデルを使用した推論、335-339

embedded AI-enabled applications, 336
埋め込まれたAI対応アプリケーション、336

stream-processing AI-enabled applica‐ tions, 337-338
ストリーム処理AI対応アプリケーション、337-338

UIs for AI-enabled applications in Python, 338-339
PythonでのAI対応アプリケーションのためのUI、338-339

model serving frameworks with KServe, 328-330
KServeを使用したモデルサービングフレームワーク、328-330

online inference pipelines, 320-328
オンライン推論パイプライン、320-328

deployment API for models/feature views, 324-328
モデル/フィーチャービューのためのデプロイメントAPI、324-328

ensuring offline–online consistency for libraries, 320-321
ライブラリのオフライン–オンラインの整合性を確保する、320-321

LLM deployments, 323
LLMのデプロイメント、323

model deployments with FastAPI, 322-323
FastAPIを使用したモデルのデプロイメント、322-323

performance and failure handling, 331-335
パフォーマンスと障害処理、331-335

handling failures on online inference pipelines, 333-334
オンライン推論パイプラインでの障害処理、333-334

mixed-mode UDFs, 331-332
混合モードUDF、331-332

model deployment SLOs, 334-335
モデルデプロイメントSLO、334-335

native UDFs/log-and-wait, 332
ネイティブUDF/ログと待機、332

inference store, defined, 309
推論ストア、定義、309

information hiding principle, 327
情報隠蔽の原則、327

ingestion time, 120-122
取り込み時間、120-122

inner joins, 158
内部結合、158

instruction datasets, 271
指示データセット、271

interactive ML systems (see real-time ML sys‐ tems) interpretability, 300
インタラクティブMLシステム（リアルタイムMLシステムを参照）解釈可能性、300

invariant, 199
不変、199

item-to-item (i2i) recommendation, 448
アイテム間（i2i）推薦、448

###### J

jailbreaking, 444
脱獄、444

job orchestrators, 219-223
ジョブオーケストレーター、219-223

Hopsworks Jobs, 221-223
Hopsworksジョブ、221-223

Modal, 220-221
Modal、220-221

Jupyter Notebooks, 54
Jupyterノートブック、54

###### K

k-fold cross-validation, 280
k分割交差検証、280

k-nearest neighbor (kNN) algorithm, 157, 269
k近傍法（kNN）アルゴリズム、157、269

kanban board, defined, 28
カンバンボード、定義、28

Kappa architecture, 239
カッパアーキテクチャ、239

KPI degradation, 427
KPIの劣化、427

KServe, 328-330
KServe、328-330

Kubernetes KServe, 417, 420
Kubernetes KServe、417、420

###### L

label encoding, 175
ラベルエンコーディング、175

label feature groups, 100, 272-273
ラベルフィーチャーグループ、100、272-273

label shift, 426
ラベルシフト、426

label-dependent transformations, 185
ラベル依存の変換、185

labels dimension modeling and, 96
ラベル次元モデリングと、96

Spine DataFrames, 101
スパインデータフレーム、101

unstructured data/labels in feature groups, 267-271
フィーチャーグループ内の非構造化データ/ラベル、267-271

labels for unstructured data, 270
非構造化データのためのラベル、270

self-supervised/unsupervised learning, 268
自己教師あり/教師なし学習、268

supervised learning and labels, 269-271
教師あり学習とラベル、269-271

lakehouse tables data for batch inference programs, 315
バッチ推論プログラムのためのレイクハウステーブルデータ、315

Hopsworks, 129-130
Hopsworks、129-130

lakehouses, 85, 208
レイクハウス、85、208

Lambda architecture, 239
ラムダアーキテクチャ、239

large language models (see LLM entries)
大規模言語モデル（LLMエントリを参照）

large reasoning models (LRMs), 350, 373, 437
大規模推論モデル（LRM）、350、373、437

Lazy DataFrames, 160
レイジーデータフレーム、160

lazy evaluation, 160
遅延評価、160

left (outer) joins, 158
左（外部）結合、158

Lightly, 184
Lightly、184

Likert scale, 399
リッカートスケール、399

lineage, 83, 405-406
系譜、83、405-406

LlamaIndex, 352-355
LlamaIndex、352-355

LLM workflows, 341-378
LLMワークフロー、341-378

agents versus, 372, 374
エージェント対、372、374

evolution from LLM workflows to agents, 370-375
LLMワークフローからエージェントへの進化、370-375

domain-specific (intermediate) repre‐ sentations, 375
ドメイン特有の（中間）表現、375

planning, 373-374
計画、373-374

security challenges, 374
セキュリティの課題、374

evolution from LLMs to agents, 342-355
LLMからエージェントへの進化、342-355

agents and workflows with LlamaIndex, 352-355
LlamaIndexを使用したエージェントとワークフロー、352-355

context window, 350-351
コンテキストウィンドウ、350-351

prompt engineering, 348-350
プロンプトエンジニアリング、348-350

prompt management, 345-348
プロンプト管理、345-348

model context protocol, 364-367
モデルコンテキストプロトコル、364-367

retrieval-augmented generation, 356-361
取得強化生成、356-361

retrieval with a document store, 358-359
ドキュメントストアを使用した取得、358-359

retrieval with a feature store, 359
フィーチャーストアを使用した取得、359

retrieval with a graph database, 360
グラフデータベースを使用した取得、360

tools/function-calling LLMs, 361
ツール/関数呼び出しLLM、361

when to use, 374
使用するタイミング、374

LLMOps, 15-18
LLMOps、15-18

LLMs batch inference for, 318-320
LLMのためのバッチ推論、318-320

deployments for online inference pipelines, 323
オンライン推論パイプラインのためのデプロイメント、323

parameter-efficient fine-tuning of, 292-295
のパラメータ効率の良いファインチューニング、292-295

text data for, 212
のためのテキストデータ、212

log transformations, 178, 179
対数変換、178、179

logical models, 213-214
論理モデル、213-214

logs/logging agents, 436-445
ログ/ロギングエージェント、436-445

error analysis, 438-442
エラー分析、438-442

guardrails, 443-444
ガードレール、443-444

jailbreaking and prompt injection, 444
脱獄とプロンプトインジェクション、444

LLM metrics, 445
LLMメトリクス、445

online A/B testing, 444
オンラインA/Bテスト、444

traces, 437
トレース、437

defined, 411
定義、411

ML models, 412-421
MLモデル、412-421

logging for batch/online models, 412-417
バッチ/オンラインモデルのためのロギング、412-417

metrics for batch models, 420-421
バッチモデルのためのメトリクス、420-421

metrics for online models, 417-420
オンラインモデルのためのメトリクス、417-420

long short-term memory (LSTM) networks, 284
長短期記憶（LSTM）ネットワーク、284

LoRA, 294
LoRA、294

lost context problem, 357
失われたコンテキストの問題、357

Lovable, 5
Lovable、5

LRMs (large reasoning models), 350, 373, 437
LRM（大規模推論モデル）、350、373、437

###### M

machine learning pipelines, 25-48
機械学習パイプライン、25-48

building ML systems with, 26-33
MLシステムの構築、26-33

minimal viable prediction service, 26-30
最小限の実行可能な予測サービス、26-30

writing modular code, 30-33
モジュラーコードの記述、30-33

case study: Titanic survival prediction, 44-47
ケーススタディ：タイタニック生存予測、44-47

data transformations in, 33-38
データ変換、33-38

feature types/model dependent transfor‐ mations, 34-36
特徴タイプ/モデル依存の変換、34-36

ML transformation taxonomy, 37-38
ML変換の分類法、37-38

real-time features with on-demand transformations, 36
オンデマンド変換を使用したリアルタイム機能、36

reusable features with modelindependent transformations, 36
モデル非依存の変換を使用した再利用可能な特徴、36

feature pipelines, 39-41
フィーチャーパイプライン、39-41

FTI (feature/training/inference) pipelines, 18-20
FTI（特徴/トレーニング/推論）パイプライン、18-20

inference pipelines, 42-44
推論パイプライン、42-44

training pipelines, 41-42
トレーニングパイプライン、41-42

machine learning systems (generally)  
機械学習システム（一般的に）

anatomy of ML system, 4-10
MLシステムの解剖、4-10

data sources, 7-8
データソース、7-8

mutable data, 8-10
可変データ、8-10

types of ML, 5-6
MLの種類、5-6

basics for building, 3-23
構築の基本、3-23

brief history, 10-15
簡単な歴史、10-15

classes of AI systems with a feature store, 21-23
フィーチャーストアを持つAIシステムのクラス、21-23

feature/training/inference (FTI) pipelines, 18-20
特徴/トレーニング/推論（FTI）パイプライン、18-20

MLOps and LLMOps, 15-18
MLOpsとLLMOps、15-18

masked language modeling, 268
マスク付き言語モデリング、268

masking, 6
マスキング、6

MCP (Model Context Protocol), 14, 364-367, 370
MCP（モデルコンテキストプロトコル）、14、364-367、370

MDTs (see model-dependent transformations)
MDT（モデル依存の変換を参照）

mean average precision (MAP) at K, 462
Kにおける平均適合率（MAP）、462

mean reciprocal rank (MRR), 462
平均逆順位（MRR）、462

metrics registry, 418
メトリクスレジストリ、418

metrics, defined, 411
メトリクス、定義、411

Michelangelo, 12, 77
Michelangelo、12、77

minimal viable prediction service (MVPS), 26-30
最小限の実行可能な予測サービス（MVPS）、26-30

case study: air quality forecasting service, 49-71
ケーススタディ：空気質予測サービス、49-71

AI system overview, 50-52
AIシステムの概要、50-52

air quality data, 52-54
空気質データ、52-54

exploratory dataset analysis, 54-57
探索的データセット分析、54-57

real-time personalized recommender, 454
リアルタイムパーソナライズドレコメンダー、454

minimum viable product (MVP), 15
最小限の実行可能製品（MVP）、15

MITs (see model-independent transformations)
MIT（モデル非依存の変換を参照）

ML pipelines, defined, 25
MLパイプライン、定義、25

ML systems, AI systems versus, 15
MLシステム、AIシステムとの対比、15

MLOps dirty dozen fallacies of, 467-471
MLOpsのダーティダズンの誤謬、467-471

evolution of ML system architectures and, 15-18
MLシステムアーキテクチャの進化、15-18

Modal for job orchestration, 220-221
ジョブオーケストレーションのためのModal、220-221

for pipeline scheduling, 65
パイプラインスケジューリングのための、65

model cards, 303-304
モデルカード、303-304

Model Context Protocol (MCP), 14, 364-367, 370
モデルコンテキストプロトコル（MCP）、14、364-367、370

model deployment pipeline, 42
モデルデプロイメントパイプライン、42

model deployments, 79, 395-396
モデルデプロイメント、79、395-396

model evaluation/validation, 299-304
モデル評価/検証、299-304

model bias tests, 301
モデルバイアステスト、301

model cards, 303-304
モデルカード、303-304

model evaluation pipeline, 42
モデル評価パイプライン、42

model file formats and model registry, 302
モデルファイル形式とモデルレジストリ、302

model interpretability, 300
モデルの解釈可能性、300

model performance for classification/ regression, 300
分類/回帰のためのモデルパフォーマンス、300

model interpretability, 300
モデルの解釈可能性、300

model registry, 302
モデルレジストリ、302

model serving networks, KServe for, 328-330
モデルサービングネットワーク、KServeのための、328-330

model training, 281-299
モデルトレーニング、281-299

checkpoints to recover from failures, 287
障害から回復するためのチェックポイント、287

credit card fraud model with XGBoost, 295-296
XGBoostを使用したクレジットカード詐欺モデル、295-296

distributed training with Ray, 290-292
Rayを使用した分散トレーニング、290-292

hyperparameter tuning with Ray Tune, 288-290
Ray Tuneを使用したハイパーパラメータチューニング、288-290

identifying bottlenecks in distributed train‐ ing, 296-299
分散トレーニングにおけるボトルネックの特定、296-299

model architecture, 283-287
モデルアーキテクチャ、283-287

parameter-efficient fine-tuning of LLMs, 292-295
LLMのパラメータ効率の良いファインチューニング、292-295

model validation pipeline, 299
モデル検証パイプライン、299

model-based cleaning, 184
モデルベースのクリーニング、184

model-based drift detection, 427
モデルベースのドリフト検出、427

model-centric AI, 267
モデル中心のAI、267

model-dependent transformations (MDTs), 35, 173-193
モデル依存の変換（MDT）、35、173-193

ensuring offline–online consistency for libraries, 320-321
ライブラリのオフライン–オンラインの整合性を確保する、320-321

feature skew and, 84
特徴の偏りと、84

feature transformations, 173-180
特徴変換、173-180

Hopsworks, 133
Hopsworks、133

MITs versus, 38
MITとの対比、38

model-specific transformations, 180-186
モデル特有の変換、180-186

transformations in feature views, 189-193
特徴ビューにおける変換、189-193

transformations in Scikit-Learn pipelines, 186-189
Scikit-Learnパイプラインにおける変換、186-189

write amplification and, 89
書き込み増幅と、89

model-independent transformations (MITs), 79, 145-172
モデル非依存の変換（MIT）、79、145-172

composition of transformations, 170-172
変換の合成、170-172

credit card fraud detection features, 168-170
クレジットカード詐欺検出機能、168-170

DAG of feature functions, 158-168
フィーチャー関数のDAG、158-168

data transformations for DataFrames, 151-158
DataFrameのためのデータ変換、151-158

join transformations, 158
結合変換、158

row- and column-size increasing trans‐ formations, 157
行および列サイズを増加させる変換、157

row- and column-size reducing transfor‐ mations, 154-157
行および列サイズを減少させる変換、154-157

row-size preserving transformations, 153-154
行サイズを保持する変換、153-154

feature pipelines, 148-151
フィーチャーパイプライン、148-151



row- and column-size reducing transformations, 154-157
行および列サイズを削減する変換、154-157

row-size preserving transformations,
153-154
行サイズを保持する変換、153-154

feature pipelines, 148-151  
特徴パイプライン、148-151  

Lazy DataFrames, 160 MDTs versus, 38 reusable features with, 36 source code organization, 146-148
Lazy DataFrames、160 MDTとの比較、38 再利用可能な特徴、36 ソースコードの整理、146-148

model-parallel training, 290 model-specific transformations, 180-186
モデル並列トレーニング、290 モデル特有の変換、180-186

data cleaning as model-based transformations, 184
モデルベースの変換としてのデータクリーニング、184

expensive features computed as needed, 185 inputting missing values, 181-184 outlier handling methods, 181 target- and label-dependent transformations, 185
必要に応じて計算される高コストの特徴、185 欠損値の入力、181-184 外れ値処理方法、181 ターゲットおよびラベル依存の変換、185

tokenizers/chat templates for LLMs, 185
LLM用のトークナイザー/チャットテンプレート、185

modular code, for ML pipelines, 30-33 modularity, 18 monitoring (see observability and monitoring) monorepo, 147 multivariate feature drift, 431-432 mutable data, 8-10 MVP (minimum viable product), 15 MVPS (see minimal viable prediction service)
MLパイプライン用のモジュラーコード、30-33 モジュラリティ、18 監視（可観測性と監視を参照）モノレポ、147 多変量特徴ドリフト、431-432 可変データ、8-10 MVP（最小実行可能製品）、15 MVPS（最小実行可能予測サービスを参照）

N NannyML, 431, 432-434 natural language processing (NLP) self-supervised learning and, 6 text data for, 212
N NannyML、431、432-434 自然言語処理（NLP）自己教師あり学習と、6 テキストデータ、212

Netflix, retrieval-and-ranking architecture, 455 neural networks, batch inference for, 317 normalization, formula for, 179 normalized discounted cumulative gain (NDCG), 462
Netflix、検索およびランキングアーキテクチャ、455 ニューラルネットワーク、バッチ推論、317 正規化、式、179 正規化された割引累積利益（NDCG）、462

notebooks, as ML pipelines, 31 NPY file format, 278 numerical variables, 34
ノートブック、MLパイプラインとして、31 NPYファイル形式、278 数値変数、34

observability and monitoring, 411-446
可観測性と監視、411-446

logging/metrics for agents, 436-445
エージェントのためのログ/メトリクス、436-445

error analysis, 438-442 guardrails, 443-444 jailbreaking and prompt injection, 444 LLM metrics, 445 online A/B testing, 444 traces, 437
エラー分析、438-442 ガードレール、443-444 脱獄とプロンプトインジェクション、444 LLMメトリクス、445 オンラインA/Bテスト、444 トレース、437

logging/metrics for ML models, 412-421
MLモデルのためのログ/メトリクス、412-421

logging for batch/online models,
412-417  
バッチ/オンラインモデルのためのログ、412-417  

metrics for batch models, 420-421 metrics for online models, 417-420
バッチモデルのためのメトリクス、420-421 オンラインモデルのためのメトリクス、417-420

monitoring features/models, 422-436
特徴/モデルの監視、422-436

data ingestion drift, 429-430 model monitoring with NannyML,
432-434
データ取り込みドリフト、429-430 NannyMLによるモデル監視、432-434

monitoring vector embeddings, 432 multivariate feature drift, 431-432 univariate feature drift, 430 when to retrain or redesign a model, 435
ベクトル埋め込みの監視、432 多変量特徴ドリフト、431-432 単変量特徴ドリフト、430 モデルを再トレーニングまたは再設計するタイミング、435

ODTs (see on-demand transformations) offline stores, 85, 129-130 offline testing, 381 offline–online skew, 84, 239 on-demand features, 38 on-demand SQL transformations, 237 on-demand transformations (ODTs), 79, 193
ODTs（オンデマンド変換を参照） オフラインストア、85、129-130 オフラインテスト、381 オフライン–オンラインの偏り、84、239 オンデマンド特徴、38 オンデマンドSQL変換、237 オンデマンド変換（ODTs）、79、193

ensuring offline–online consistency for libraries, 320-321
ライブラリのオフライン–オンラインの一貫性を確保する、320-321

feature skew and, 84 MDTs versus, 38 real-time features with, 36 transformation functions and, 139
特徴の偏りと、84 MDTとの比較、38 リアルタイム特徴との関係、36 変換関数と、139

one big table (OBT) data model, 94 online inference, 103, 108 online inference data, 138 online inference pipelines, 44, 320-328
1つの大きなテーブル（OBT）データモデル、94 オンライン推論、103、108 オンライン推論データ、138 オンライン推論パイプライン、44、320-328

deployment API for models/feature views,
324-328
モデル/特徴ビューのためのデプロイメントAPI、324-328

ensuring offline–online consistency for libraries, 320-321
ライブラリのオフライン–オンラインの一貫性を確保する、320-321

LLM deployments, 323 model deployments with FastAPI, 322-323 TikTok personalized recommender system,
462-465
LLMデプロイメント、323 FastAPIによるモデルデプロイメント、322-323 TikTokパーソナライズドレコメンダーシステム、462-465

online ML models, metrics for, 417-420 online models, logging for, 412-417 online store, 84 open table formats (OTFs), 85 OpenTelemetry, 420 orchestration (see job orchestrators) outer joins, 158
オンラインMLモデルのためのメトリクス、417-420 オンラインモデルのためのログ、412-417 オンラインストア、84 オープンテーブル形式（OTFs）、85 OpenTelemetry、420 オーケストレーション（ジョブオーケストレーターを参照） 外部結合、158

P Pandas, 41, 182 parallelized orchestration, 371 parameter-efficient fine-tuning (PEFT), 293 Parquet file format, 278 pipeline, defined, 25 Polars, 41  
P Pandas、41、182 並列化されたオーケストレーション、371 パラメータ効率の良いファインチューニング（PEFT）、293 Parquetファイル形式、278 パイプライン、定義、25 Polars、41  

polling, 217 postconditions/preconditions, in pytest unit tests, 199
ポーリング、217 postconditions/preconditions、pytestユニットテストにおける、199

precondition, 199 prediction drift, 426 predictor script, 326, 327 preference datasets, 271 primary key, 118 projection pushdown, 139 projects, Hopsworks, 111-115
前提条件、199 予測ドリフト、426 予測子スクリプト、326、327 優先データセット、271 主キー、118 プロジェクションプッシュダウン、139 プロジェクト、Hopsworks、111-115

access control at cluster level using projects,
113-115
プロジェクトを使用したクラスターレベルでのアクセス制御、113-115

access controls within projects, 113 storing files in a project, 112
プロジェクト内のアクセス制御、113 プロジェクト内のファイルの保存、112

Prometheus, 418 prompt chaining, 371 prompt decomposition, 349 prompt engineering, 348-350 prompt injection, 445 prompt template, 346 PySpark imputing missing time-series data with, 182 saving batch inference with, 314-315
Prometheus、418 プロンプトチェイニング、371 プロンプト分解、349 プロンプトエンジニアリング、348-350 プロンプトインジェクション、445 プロンプトテンプレート、346 PySparkを使用した欠損時系列データの補完、182 バッチ推論の保存、314-315

pytest, 197-202
pytest、197-202

testing methodology, 201 unit tests, 197-201
テスト方法論、201 ユニットテスト、197-201

Python, UIs for AI-enabled applications in,
338-339
Python、AI対応アプリケーションのUI、338-339

PyTorch transformations, 194-197
PyTorch変換、194-197

queries, Hopsworks feature store, 139-141
クエリ、Hopsworksフィーチャーストア、139-141

R RAG (see retrieval-augmented generation) random splits, 135 Ray, 290-292 Ray Data, 290 Ray Tune, 288-290 RBAC (role-based access control), 113, 114 real-time data transformations, 34 real-time features, 36
R RAG（検索拡張生成を参照） ランダムスプリット、135 Ray、290-292 Ray Data、290 Ray Tune、288-290 RBAC（ロールベースのアクセス制御）、113、114 リアルタイムデータ変換、34 リアルタイム特徴、36

(see also streaming features) interactive AI-enabled systems and, 232-233 shift left versus shift right, 234-242
（ストリーミング機能も参照） インタラクティブなAI対応システムと、232-233 シフト左対シフト右、234-242

definitions, 234 shift-left architectures, 238-242 shift-right architectures, 236-238
定義、234 シフト左アーキテクチャ、238-242 シフト右アーキテクチャ、236-238

real-time ML systems, 11  
リアルタイムMLシステム、11  

defined, 21 feature stores with, 80 real-time data transformations in, 34 snowflake schema versus star schema, 102 TikTok recommendation engine, 4
定義、21 特徴ストアとの関係、80 リアルタイムデータ変換、34 スノーフレークスキーマ対スタースキーマ、102 TikTokレコメンデーションエンジン、4

reciprocal transformation, formula for, 179 recommender systems (see TikTok personalized recommender system) regression models, 300 reinforcement learning, 6 reinforcement learning with human feedback (RLHF), 271, 293
相互変換、式、179 レコメンダーシステム（TikTokパーソナライズドレコメンダーシステムを参照） 回帰モデル、300 強化学習、6 人間のフィードバックを伴う強化学習（RLHF）、271、293

reranking, 358 REST APIs, 408 retrieval-and-ranking architecture, 449-454 retrieval-augmented generation (RAG), 13-15,
再ランキング、358 REST API、408 検索およびランキングアーキテクチャ、449-454 検索拡張生成（RAG）、13-15、

342, 356-361 point-in-time correct data for historical evals, 402
342、356-361 歴史的評価のための時点正確データ、402

retrieval with a document store, 358-359 retrieval with a feature store, 359 retrieval with a graph database, 360
ドキュメントストアを使用した検索、358-359 フィーチャーストアを使用した検索、359 グラフデータベースを使用した検索、360

ring all-reduce architecture, 297 RLHF (reinforcement learning with human feedback), 271, 293
リングオールリデュースアーキテクチャ、297 RLHF（人間のフィードバックを伴う強化学習）、271、293

role-based access control (RBAC), 113, 114 role-playing (prompt engineering strategy), 349 rolling aggregations, 251-252
ロールベースのアクセス制御（RBAC）、113、114 ロールプレイ（プロンプトエンジニアリング戦略）、349 ローリング集計、251-252

incremental views and, 256-258 tiled time window aggregations and, 260
インクリメンタルビューと、256-258 タイル時間ウィンドウ集計と、260

RonDB online feature store, 126 root feature groups, 272-273 routing LLM workflow, 372 routing pattern, 372
RonDBオンラインフィーチャーストア、126 ルートフィーチャーグループ、272-273 ルーティングLLMワークフロー、372 ルーティングパターン、372

scalability, 41 SCDs (slowly changing dimensions), 94, 96-98 schemas, for feature groups, 167 schematized tags, 402-405 Scikit-Learn imputation of non-time-series data, 183 outlier handling, 181 transformations in Scikit-Learn pipelines,
スケーラビリティ、41 SCD（徐々に変化する次元）、94、96-98 特徴グループのためのスキーマ、167 スキーマ化されたタグ、402-405 Scikit-Learnによる非時系列データの補完、183 外れ値処理、181 Scikit-Learnパイプラインにおける変換、

186-189
186-189

search engine, 358 security challenges, with agents, 374 self-supervised learning, 6 serving keys, 134 session window, 250  
検索エンジン、358 エージェントによるセキュリティの課題、374 自己教師あり学習、6 サービングキー、134 セッションウィンドウ、250  

SFT (supervised fine-tuning), 271, 292 shift-left architectures, 238-242
SFT（教師ありファインチューニング）、271、292 シフト左アーキテクチャ、238-242

definitions, 234 hybrid streaming-batch architecture,
238-239
定義、234 ハイブリッドストリーミングバッチアーキテクチャ、238-239

streaming-native architecture, 240-242
ストリーミングネイティブアーキテクチャ、240-242

shift-right architectures, 236-238 sink, defined, 234 slowly changing dimensions (SCDs), 94, 96-98 snowflake schema data model, 101 software-as-a-service (SaaS) systems, 8 Spark Structured Streaming, 41 Spine DataFrame, 101, 313 Spine Group, 138
シフト右アーキテクチャ、236-238 シンク、定義、234 徐々に変化する次元（SCD）、94、96-98 スノーフレークスキーマデータモデル、101 サービスとしてのソフトウェア（SaaS）システム、8 Spark Structured Streaming、41 Spine DataFrame、101、313 Spine Group、138

splitting training data, 135, 279-280 Spotify Discovery Weekly, 4 SQL for feature engineering, 150 on-demand SQL transformations, 237
トレーニングデータの分割、135、279-280 Spotify Discovery Weekly、4 特徴エンジニアリングのためのSQL、150 オンデマンドSQL変換、237

stable diffusion networks, 269 standardization, formula for, 179 star schema data model, 100-101 stateful data transformations, 241, 245 stateless data transformations, 241, 244-246 stateless online ML systems, 11 statistical hypothesis testing methods, 427 stochastic gradient descent, 285 stratified splits, 136, 280 stream processing feature pipelines, 41 stream processing ML systems, defined, 21
安定拡散ネットワーク、269 標準化、式、179 スタースキーマデータモデル、100-101 状態を持つデータ変換、241、245 状態を持たないデータ変換、241、244-246 状態を持たないオンラインMLシステム、11 統計的仮説検定方法、427 確率的勾配降下法、285 層別分割、136、280 ストリーム処理特徴パイプライン、41 ストリーム処理MLシステム、定義、21

stream-processing AI-enabled applications,
337-338
ストリーム処理AI対応アプリケーション、337-338

streaming data pipelines, defined, 206 streaming features, 231-264
ストリーミングデータパイプライン、定義、206 ストリーミング機能、231-264

backpressure, 242 credit card fraud streaming features,
258-263 ASOF joins and composition of transfor‐ mations, 260-262
バックプレッシャー、242 クレジットカード詐欺のストリーミング機能、258-263 ASOF結合と変換の構成、260-262

lagged features/feature pipelines in Fel‐ dera, 262-263
Felderaにおける遅延特徴/特徴パイプライン、262-263

event-streaming platforms, 233 need for real-time features in interactive AIenabled systems, 232-233
イベントストリーミングプラットフォーム、233 インタラクティブなAI対応システムにおけるリアルタイム機能の必要性、232-233

shift left versus shift right, 234-242
シフト左対シフト右、234-242

definitions, 234 shift-left architectures, 238-242 shift-right architectures, 236-238
定義、234 シフト左アーキテクチャ、238-242 シフト右アーキテクチャ、236-238

windowed aggregations, 248-258  
ウィンドウ集計、248-258  

choosing the best window type for aggregations, 256
集計のための最適なウィンドウタイプの選択、256

rolling aggregations, 251-252 rolling aggregations with incremental views, 256-258
ローリング集計、251-252 インクリメンタルビューを持つローリング集計、256-258

time window aggregations, 253-256
時間ウィンドウ集計、253-256

writing streaming feature pipelines, 242-248
ストリーミング特徴パイプラインの作成、242-248

Apache Flink, 246 benchmarking, 248 dataflow programming, 243 Feldera, 247 stateless/stateful data transformations,
Apache Flink、246 ベンチマーキング、248 データフロープログラミング、243 Feldera、247 状態を持たない/状態を持つデータ変換、

244-246
244-246

streaming-native architecture, 240-242 strings, transformation into numerical repre‐ sentation, 34
ストリーミングネイティブアーキテクチャ、240-242 文字列、数値表現への変換、34

structured data, 8 structured output, 349 supervised fine-tuning (SFT), 271, 292 supervised learning, 5 synthetic data LLM prompts for generating synthetic data,
構造化データ、8 構造化出力、349 教師ありファインチューニング（SFT）、271、292 教師あり学習、5 合成データ LLMプロンプトによる合成データの生成、

215-216
215-216

LLMs and, 213-216 logical model for data mart and LLM,
LLMと、213-216 データマートとLLMのための論理モデル、

213-214
213-214

synthetic evals, LLM-assisted generation of,
400-401
合成評価、LLM支援による生成、400-401

tabular data, 7 tags, schematized, 402-405 target-dependent transformations, 185 task parallelism, 243 temporal joins, 81, 106 tensor parallelism, 290 tensors, 166-167 term-based retrieval method, 358 testing AI systems, 381-409
表形式データ、7 タグ、スキーマ化された、402-405 ターゲット依存の変換、185 タスク並列性、243 時間的結合、81、106 テンソル並列性、290 テンソル、166-167 用語ベースの検索方法、358 AIシステムのテスト、381-409

automatic containerization and jobs,
385-389
自動コンテナ化とジョブ、385-389

environments and jobs in Hopsworks,
386-389
Hopsworksにおける環境とジョブ、386-389

Modal jobs, 389
モーダルジョブ、389

CI/CD tests, 390-402
CI/CDテスト、390-402

A/B tests for batch inference, 397 evals for agents, 397-402 feature pipeline tests, 391-394 testing model deployments, 395-396  
バッチ推論のためのA/Bテスト、397 エージェントのための評価、397-402 特徴パイプラインテスト、391-394 モデルデプロイメントのテスト、395-396  

training pipeline tests for model perfor‐ mance/bias, 394-395
モデルのパフォーマンス/バイアスのためのトレーニングパイプラインテスト、394-395

code progression from development to pro‐ duction, 383-385
開発から生産へのコードの進行、383-385

governance, 402-409
ガバナンス、402-409

audit logs, 408 lineage, 405-406 schematized tags, 402-405 versioning, 406-408
監査ログ、408 系譜、405-406 スキーマ化されたタグ、402-405 バージョン管理、406-408

offline testing, 381 online A/B testing, 444
オフラインテスト、381 オンラインA/Bテスト、444

testing ML systems, 16 text chunking, 186 text data, 212 text tokenization, 186 TFRecord file format, 167, 278 TikTok personalized recommender system,
MLシステムのテスト、16 テキストチャンク化、186 テキストデータ、212 テキストトークン化、186 TFRecordファイル形式、167、278 TikTokパーソナライズドレコメンダーシステム、

447-472
447-472

agentic search for videos, 465-467 ethical responsibilities of AI builders, 472 real-time ML system, 4 real-time personalized recommender,
動画のエージェント検索、465-467 AIビルダーの倫理的責任、472 リアルタイムMLシステム、4 リアルタイムパーソナライズドレコメンダー、

454-465 feature pipelines, 456-458 online inference pipeline, 462-465 training pipelines, 458-462
454-465 特徴パイプライン、456-458 オンライン推論パイプライン、462-465 トレーニングパイプライン、458-462

recommender basics, 447-449 recommender with retrieval/ranking archi‐ tecture, 449-454
レコメンダーの基本、447-449 検索/ランキングアーキテクチャを持つレコメンダー、449-454

tiled time window aggregations, 260 time to live (TTL), 126, 237 time window aggregations, 253-256 time-series data, feature stores for, 80-81 time-series splits, 136 time-travel, 120 Titanic passenger dataset, 9 Titanic survival prediction case study, 44-47
タイル時間ウィンドウ集計、260 生存時間（TTL）、126、237 時間ウィンドウ集計、253-256 時系列データ、特徴ストア、80-81 時系列分割、136 タイムトラベル、120 タイタニック乗客データセット、9 タイタニック生存予測ケーススタディ、44-47

tokenizers, 185 topic (Apache Kafka queue), 210 traces, 398, 437 training data, 277-281
トークナイザー、185 トピック（Apache Kafkaキュー）、210 トレース、398、437 トレーニングデータ、277-281

DataFrames or files, 135-137 random/time-series/stratified splits, 135 reproducible, 280 reproducible training data, 137 splitting, 279-280
DataFramesまたはファイル、135-137 ランダム/時系列/層別分割、135 再現可能、280 再現可能なトレーニングデータ、137 分割、279-280

training dataset pipeline, 42 training helper columns, 301 training pipelines, 41-42, 267-305  
トレーニングデータセットパイプライン、42 トレーニングヘルパーカラム、301 トレーニングパイプライン、41-42、267-305  

air quality forecasting service case study,
59-62
空気質予測サービスケーススタディ、59-62

feature selection, 273-276 functions of, 20 model evaluation/validation, 299-304
特徴選択、273-276 の機能、20 モデル評価/検証、299-304

model bias tests, 301 model cards, 303-304 model file formats and model registry,
モデルバイアステスト、301 モデルカード、303-304 モデルファイル形式とモデルレジストリ、

302
302

model interpretability, 300 model performance for classification/ regression, 300
モデルの解釈可能性、300 分類/回帰のためのモデルパフォーマンス、300

model training, 281-299
モデルのトレーニング、281-299

checkpoints to recover from failures, 287 credit card fraud model with XGBoost,
失敗から回復するためのチェックポイント、287 XGBoostによるクレジットカード詐欺モデル、



302
model interpretability, 300 model performance for classification/ regression, 300
モデルの解釈可能性、分類/回帰のためのモデル性能、300

model training, 281-299
モデルのトレーニング、281-299

checkpoints to recover from failures, 287 credit card fraud model with XGBoost,
295-296
失敗から回復するためのチェックポイント、287 XGBoostを用いたクレジットカード詐欺モデル、295-296

distributed training with Ray, 290-292 hyperparameter tuning with Ray Tune,
288-290
Rayを用いた分散トレーニング、290-292 Ray Tuneを用いたハイパーパラメータチューニング、288-290

identifying bottlenecks in distributed training, 296-299
分散トレーニングにおけるボトルネックの特定、296-299

model architecture, 283-287 parameter-efficient fine-tuning of LLMs,
292-295
モデルアーキテクチャ、283-287 LLMのパラメータ効率の良いファインチューニング、292-295

root/label feature groups, 272-273 testing for model performance/bias,
394-395
ルート/ラベル特徴群、272-273 モデルの性能/バイアスのテスト、394-395

TikTok personalized recommender system,
458-462 building the vector index of videos, 462 ranking model, 462 two-tower embedding model, 459-461
TikTokのパーソナライズドレコメンダーシステム、458-462 動画のベクトルインデックスの構築、462 ランキングモデル、462 二塔埋め込みモデル、459-461

training data, 277-281
トレーニングデータ、277-281

reproducible training data, 280 splitting training data, 279-280
再現可能なトレーニングデータ、280 トレーニングデータの分割、279-280

unstructured data/labels in feature groups,
267-271 labels for unstructured data, 270 self-supervised/unsupervised learning,
268
特徴群における非構造化データ/ラベル、267-271 非構造化データのラベル、270 自己教師あり学習/教師なし学習、268

supervised learning and labels, 269-271
教師あり学習とラベル、269-271

transformations, 36
変換、36

(see also specific types, e.g.: on-demand transformations) feature types/model dependent transforma‐ tions, 34-36
（特定のタイプも参照、例：オンデマンド変換）特徴タイプ/モデル依存の変換、34-36

ML pipelines, 33-38 real-time features with on-demand transfor‐ mations, 36  
MLパイプライン、33-38 オンデマンド変換を用いたリアルタイム機能、36

reusable features with model-independent transformations, 36
モデル非依存の変換を用いた再利用可能な特徴、36

standardization versus normalization, 178 taxonomy, 37-38
標準化と正規化、178 タクソノミー、37-38

transformed feature data, 88 transformers, 284 tree-based models, 178, 284 TTL (time to live), 126, 237 tumbling windows, 253-256 two-tower embedding model, 459-461
変換された特徴データ、88 トランスフォーマー、284 木構造モデル、178, 284 TTL（生存時間）、126, 237 タンブリングウィンドウ、253-256 二塔埋め込みモデル、459-461

###### U u2i (user-to-item) recommendation, 448 Uber (Michelangelo platform), 12, 77 
###### U u2i（ユーザーからアイテムへの）推薦、448 Uber（Michelangeloプラットフォーム）、12, 77

UDFs (see user-defined functions) UDTFs (user-defined table functions), 157 
UDF（ユーザー定義関数を参照） UDTF（ユーザー定義テーブル関数）、157

univariate feature drift, 430 unstructured data, 8
単変量特徴ドリフト、430 非構造化データ、8

labels for, 270 object stores/filesystems, 211-212
ラベル、270 オブジェクトストア/ファイルシステム、211-212

unsupervised learning, 6 user-defined functions (UDFs), 133
教師なし学習、6 ユーザー定義関数（UDF）、133

mixed-mode, 331-332 native UDFs/log-and-wait, 332
混合モード、331-332 ネイティブUDF/ログと待機、332

user-defined table functions (UDTFs), 157  
ユーザー定義テーブル関数（UDTF）、157

user-to-item (u2i) recommendation, 448
ユーザーからアイテムへの（u2i）推薦、448

###### V vector embedding pipeline, 39, 462 vector embeddings, 156, 432 
###### V ベクトル埋め込みパイプライン、39, 462 ベクトル埋め込み、156, 432

vector indexes, 127-128 vectorized compute engines, 160-165 verifiable evals, 442 versioning, 17, 122-125, 406-408
ベクトルインデックス、127-128 ベクトル化された計算エンジン、160-165 検証可能な評価、442 バージョン管理、17, 122-125, 406-408

###### W weak supervision, 270 windowed aggregations, 98
###### W 弱い監視、270 ウィンドウ集約、98

choosing the best window type for aggrega‐ tions, 256
集約のための最適なウィンドウタイプの選択、256

rolling aggregations, 251-252 rolling aggregations with incremental views,
256-258
ロール集約、251-252 増分ビューを用いたロール集約、256-258

time window aggregations, 253-256
時間ウィンドウ集約、253-256

write amplification, 89, 316 write-audit-publish (WAP) pattern, 227
書き込み増幅、89, 316 書き込み-監査-公開（WAP）パターン、227

###### X XGBoost, model training with, 295-296  
###### X XGBoostを用いたモデルのトレーニング、295-296  

###### About the Author
**Jim Dowling is CEO of Hopsworks and a former associate professor at KTH Royal** Institute of Technology
###### 著者について
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

###### Colophon コロフォン

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
