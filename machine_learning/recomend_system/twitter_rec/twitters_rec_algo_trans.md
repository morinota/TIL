## link リンク

- https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm

## title タイトル

Twitter's Recommendation Algorithm
Twitterのレコメンデーションアルゴリズム

## abstruct

Twitter aims to deliver you the best of what’s happening in the world right now
Twitterは、今世界で起きていることを最高の形でお届けすることを目指します.
This requires a recommendation algorithm to distill the roughly 500 million Tweets posted daily down to a handful of top Tweets that ultimately show up on your device’s For You timeline
そのため、レコメンデーションアルゴリズムにより、毎日投稿される約5億件のツイートの中から、お使いの端末のFor Youタイムラインに最終的に表示されるトップツイートを抽出する必要があります.
This blog is an introduction to how the algorithm selects Tweets for your timeline.
このブログでは、アルゴリズムがタイムラインのツイートを選択する仕組みについてご紹介します.

Our recommendation system is composed of many interconnected services and jobs, which we will detail in this post
私たちのレコメンデーションシステムは、**多くの相互接続されたサービスとジョブで構成されて**おり、この投稿で詳しく説明します.
While there are many areas of the app where Tweets are recommended—Search, Explore, Ads—this post will focus on the home timeline’s For You feed.
検索、探索、広告など、ツイートが推薦される領域はアプリ内にたくさんありますが、今回はホームタイムラインの「For You」フィードに焦点を当てる.

# How do we choose Tweets? どうやってTweetを選ぶのか？

The foundation of Twitter’s recommendations is a set of core models and features that extract latent information from Tweet, user, and engagement data
Twitterのレコメンデーションの基盤は、ツイート、ユーザー、エンゲージメントデータから潜在的な情報を抽出する一連のコアモデルと特徴量である.
These models aim to answer important questions about the Twitter network, such as, “What is the probability you will interact with another user in the future?” or, “What are the communities on Twitter and what are trending Tweets within them?” Answering these questions accurately enables Twitter to deliver more relevant recommendations.
これらのモデルは、"将来、他のユーザーと交流する確率は？"、"Twitter上のコミュニティとその中でのトレンドツイートは？"など、Twitterネットワークに関する重要な質問に答えることを目的としている. これらの質問に正確に答えることで、Twitterはより適切なレコメンデーションを提供することができるようになる.

The recommendation pipeline is made up of three main stages that consume these features:
レコメンデーションパイプラインは、これらの特徴量を消費する3つの主要なステージで構成されています：

- 1. Fetch the best Tweets from different recommendation sources in a process called candidate sourcing. 1 candidate sourcing と呼ばれるプロセスで、異なるレコメンデーションソースから最適なツイートをフェッチする.

- 2. Rank each Tweet using a machine learning model. 2 機械学習モデルを使って、各ツイートをランク付けする.

- 3. Apply heuristics and filters, such as filtering out Tweets from users you’ve blocked, NSFW content, and Tweets you’ve already seen. 3 ブロックしたユーザーのツイート、NSFWコンテンツ、すでに見たツイートなどをフィルタリングするなど、**ヒューリスティックとフィルターを適用**する.

The service that is responsible for constructing and serving the For You timeline is called Home Mixer
For Youタイムラインの構築と配信を担当するサービスは、Home Mixerと呼ばれます
Home Mixer is built on Product Mixer, our custom Scala framework that facilitates building feeds of content
Home Mixerは、Product Mixerをベースに構築されており、Scalaのカスタムフレームワークで、コンテンツのフィードを容易に構築することができます。
This service acts as the software backbone that connects different candidate sources, scoring functions, heuristics, and filters.
このサービスは、異なる候補ソース、スコアリング機能、ヒューリスティック、フィルターをつなぐソフトウェアバックボーンとして機能します。

This diagram below illustrates the major components used to construct a timeline:
この図は、タイムラインを構成するための主な構成要素を示したものです：

![](https://cdn.cms-twdigitalassets.com/content/dam/blog-twitter/engineering/en_us/open-source/2023/twitter-recommendation-algorithm/open-algorithm.png.img.fullhd.medium.png)

Let’s explore the key parts of this system, roughly in the order they’d be called during a single timeline request, starting with retrieving candidates from Candidate Sources.
このシステムの主要な部分を、1回のタイムラインリクエストで呼ばれる順番に、Candidate Sources から Candidate を取得するところから見ていこう.

# Candidate Sources 

Twitter has several Candidate Sources that we use to retrieve recent and relevant Tweets for a user
Twitterは、ユーザーの最近の関連ツイートを取得するために、いくつかのCandidate Sourcesを使用している.
For each request, we attempt to extract the best 1500 Tweets from a pool of hundreds of millions through these sources
各リクエストに対して、以下のソースを通じて、数億のプールからベスト1500ツイートを抽出することを試みる.
We find candidates from people you follow (In-Network) and from people you don’t follow (Out-of-Network)
あなたがフォローしている人（In-Network）、フォローしていない人（Out-of-Network）から candidate を探す.
Today, the For You timeline consists of 50% In-Network Tweets and 50% Out-of-Network Tweets on average, though this may vary from user to user.
現在、For Youのタイムラインは、ユーザーによって異なるかもしれませんが、平均して50％のIn-Networkツイートと50％のOut-of-Networkツイートで構成されています。

## In-Network Source In-Network Source

The In-Network source is the largest candidate source and aims to deliver the most relevant, recent Tweets from users you follow
In-Network source は最大の candidate source で、あなたがフォローしているユーザからの最も関連性の高い最新のツイートを配信することを目的としている.
It efficiently ranks Tweets of those you follow based on their relevance using a logistic regression model
**ロジスティック回帰モデルを使って、フォローした人のツイートを関連性に基づいて効率的にランク付けする.**
The top Tweets are then sent to the next stage.
そして、上位のツイートは次のステージに送られる.

The most important component in ranking In-Network Tweets is Real Graph
ネットワーク内ツイートのランキングで最も重要な要素は、Real Graph である.
Real Graph is a model which predicts the likelihood of engagement between two users
**Real Graph は、2人のユーザ間のエンゲージメントの可能性を予測するモデル**である.
The higher the Real Graph score between you and the author of the Tweet, the more of their tweets we'll include.
あなたとツイート作成者の間の Real Graph のスコアが高いほど、そのツイートがより多く含まれる.

The In-Network source has been the subject of recent work at Twitter.
インネットワーク・ソースは、最近Twitterで話題になっている.
We recently stopped using Fanout Service, a 12-year old service that was previously used to provide In-Network Tweets from a cache of Tweets for each user
12年前から利用していたFanout Serviceの利用を最近停止し、各ユーザーのツイートのキャッシュからネットワーク内ツイートを提供するようになった.
We’re also in the process of redesigning the logistic regression ranking model which was last updated and trained several years ago!
また、数年前に更新・トレーニングしたロジスティック回帰のランキングモデルの再設計も進めている.

## Out-of-Network Sources ネットワーク外の情報源

Finding relevant Tweets outside of a user’s network is a trickier problem: How can we tell if a certain Tweet will be relevant to you if you don’t follow the author? Twitter takes two approaches to addressing this.
ユーザのネットワークの外にある関連ツイートを見つけるのは、より厄介な問題である. 作者をフォローしていない場合、あるツイートが自分に関連するかどうかをどうやって判断すればいいのだろうか. Twitterは、この問題に対処するために2つのアプローチをとっている.

### Social Graph ソーシャルグラフ

Our first approach is to estimate what you would find relevant by analyzing the engagements of people you follow or those with similar interests.
最初のアプローチは、**自分がフォローしている人や同じような興味を持つ人の engagements を分析すること**で、あなたが関連すると思うものを推定するというものである.

We traverse the graph of engagements and follows to answer the following questions:
エンゲージメントとフォローのグラフをなぞりながら、以下の問いに答えていく：

- What Tweets did the people I follow recently engage with? 自分がフォローしている人が最近どんなツイートと絡んだのか？
- Who likes similar Tweets to me, and what else have they recently liked? 私と似たようなツイートを好きな人、最近他に好きなものは？

We generate candidate Tweets based on the answers to these questions and rank the resulting Tweets using a logistic regression model
これらの質問に対する回答に基づいて候補ツイートを生成し、得られたツイートをロジスティック回帰モデルでランク付けする.
Graph traversals of this type are essential to our Out-of-Network recommendations; we developed GraphJet, a graph processing engine that maintains a real-time interaction graph between users and Tweets, to execute these traversals
このようなグラフの traversals は、Out-of-Networkの推薦 に不可欠であり、この traversals を実行するために、ユーザとツイートの間のリアルタイムな interaction graph を保持するグラフ処理エンジンGraphJetを開発した. 
While such heuristics for searching the Twitter engagement and follow network have proven useful (these currently serve about 15% of Home Timeline Tweets), embedding space approaches have become the larger source of Out-of-Network Tweets.
Twitterのエンゲージメントやフォローネットワークを検索するヒューリスティックな手法は有用であることが証明されているが（これらは現在、ホームタイムラインツイートの約15％に対応しています）、後述する埋め込み空間アプローチ(=embedding vectorを使って距離を測ったりする方法??)はネットワーク外ツイートのより大きなソースとなっている. 

### Embedding Spaces

Embedding space approaches aim to answer a more general question about content similarity: What Tweets and Users are similar to my interests?
エンベッディングスペースアプローチは、コンテンツの類似性に関するより一般的な問いに答えることを目的としている： **どのようなツイートやユーザが私の興味と似ているのか**？

Embeddings work by generating numerical representations of users’ interests and Tweets’ content
エンベッディングは、ユーザの興味とツイートの内容を数値で表現することで機能する
We can then calculate the similarity between any two users, Tweets or user-Tweet pairs in this embedding space
そして、**この埋め込み空間において、任意の2人のユーザ、ツイート、またはユーザとツイートのペアの間の類似度を計算**することができる.
Provided we generate accurate embeddings, we can use this similarity as a stand-in for relevance.
**正確な埋め込みができれば、この類似性を関連性の代用品として使うことができる.**

One of Twitter’s most useful embedding spaces is SimClusters
Twitterの便利な埋め込みスペースの1つが **SimClusters** である.
SimClusters discover communities anchored by a cluster of influential users using a custom matrix factorization algorithm
SimClustersは、カスタム行列因数分解アルゴリズムを用いて、影響力のあるユーザのクラスターを中心としたコミュニティを発見する.
There are 145k communities, which are updated every three weeks
コミュニティは145kあり、3週間ごとに更新される.
Users and Tweets are represented in the space of communities, and can belong to multiple communities
ユーザやツイートはコミュニティという空間で表現され、複数のコミュニティに所属することができる.
Communities range in size from a few thousand users for individual friend groups, to hundreds of millions of users for news or pop culture
コミュニティの規模は、個人の友人グループの数千人から、ニュースやポップカルチャーの数億人のユーザーまで様々である.
These are some of the biggest communities:
これらは、大きなコミュニティの一部：

![](https://cdn.cms-twdigitalassets.com/content/dam/blog-twitter/engineering/en_us/open-source/2023/twitter-recommendation-algorithm/simclusters.png.img.fullhd.medium.png)

We can embed Tweets into these communities by looking at the current popularity of a Tweet in each community
各コミュニティにおけるツイートの現在の人気度を見ることで、これらのコミュニティにツイートを埋め込むことができる.
The more that users from a community like a Tweet, the more that Tweet will be associated with that community.
あるコミュニティのユーザーがそのツイートを気に入れば気に入るほど、そのツイートはそのコミュニティと関連づけられる.

[SimClusters: Community-Based Representations for Heterogeneous Recommendations at Twitter](https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio)

# Ranking ランキング

The goal of the For You timeline is to serve you relevant Tweets
For Youのタイムラインの目的は、あなたに関連するTweetを提供することである.
At this point in the pipeline, we have ~1500 candidates that may be relevant
パイプラインのこの時点で、関連する可能性のある候補が1500件ほどある.
Scoring directly predicts the relevance of each candidate Tweet and is the primary signal for ranking Tweets on your timeline
スコアリングは、各候補ツイートの関連性を直接予測し、あなたのタイムライン上のツイートをランク付けする主要なシグナルとなる.
At this stage, all candidates are treated equally, without regard for what candidate source it originated from.
この段階では、どの candidate source から出たものであるかは関係なく、**すべての candidates が平等に扱われる**.

Ranking is achieved with a ~48M parameter neural network that is continuously trained on Tweet interactions to optimize for positive engagement (e.g
ランキングは、ツイートとのやり取りを継続的にトレーニングし、ポジティブなエンゲージメントを得るために最適化された、約48Mパラメータのニューラルネットワークで実現されています（例）。
Likes, Retweets, and Replies)
いいね！」「リツイート」「リプライ」)
This ranking mechanism takes into account thousands of features and outputs ten labels to give each Tweet a score, where each label represents the probability of an engagement
このランキングメカニズムは、**何千もの特徴を考慮し、10個のラベルを出力して各ツイートにスコアを与えるもの**で、各ラベルはエンゲージメントの確率を表している.
We rank the Tweets from these scores.
このスコアからツイートをランキングしている.

- [Heavy Ranker](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md)
- [Heavy Rankerで採用されているMLモデル: MaskNet(ランク学習のNNっぽい?)](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md)

# Heuristics, Filters, and Product Features ヒューリスティック、フィルター、そして製品の特徴

After the Ranking stage, we apply heuristics and filters to implement various product features
ランキングの段階を経て、ヒューリスティックとフィルターを適用して、さまざまな製品機能を実装する.
These features work together to create a balanced and diverse feed
これらの機能が連動して、バランスのとれた多様な feed を作ることができる.
Some examples include:
などの例があります：

- Visibility Filtering: Filter out Tweets based on their content and your preferences. For instance, remove Tweets from accounts you block or mute. ビジビリティフィルタリング： ツイートの内容や好みに応じてフィルタリングが可能. 例えば、ブロックやミュートしたアカウントからのツイートを削除する.

- Author Diversity: Avoid too many consecutive Tweets from a single author. 著者の多様性： 一人の著者のツイートが連続しすぎないようにする.

- Content Balance: Ensure we are delivering a fair balance of In-Network and Out-of-Network Tweets. コンテンツのバランス： **ネットワーク内のツイートとネットワーク外のツイートを公平なバランスで配信していることを確認する.**

- Feedback-based Fatigue: Lower the score of certain Tweets if the viewer has provided negative feedback around it. フィードバックに基づく疲労感： **視聴者がそのツイートに対してネガティブなフィードバックをした場合、特定のツイートのスコアを下げる.**

- Social Proof: Exclude Out-of-Network Tweets without a second degree connection to the Tweet as a quality safeguard. In other words, ensure someone you follow engaged with the Tweet or follows the Tweet’s author. ソーシャルプルーフ： 品質保護として、そのツイートと**二次的なつながりがないネットワーク外のツイートを除外する**.  つまり、あなたがフォローしている誰かがそのツイートに関与しているか、そのツイートの作者をフォローしているかを確認する. 

- Conversations: Provide more context to a Reply by threading it together with the original Tweet. 会話： 元のツイートと一緒にスレッド化することで、リプライに**さらなる文脈を提供**する.

- Edited Tweets: Determine if the Tweets currently on a device are stale, and send instructions to replace them with the edited versions. 編集されたツイート **端末に現在表示されているツイートが古くなっているかどうかを判断**し、編集されたバージョンに置き換える指示を送信する.

# Mixing and Serving

At this point, Home Mixer has a set of Tweets ready to send to your device
この時点で、Home Mixerはデバイスに送信するためのツイートセットを準備している.
As the last step in the process, the system blends together Tweets with other non-Tweet content like Ads, Follow Recommendations, and Onboarding prompts, which are returned to your device to display.
このプロセスの最後のステップとして、システムはツイートと、広告、フォローの推薦、オンボーディングプロンプトなどの**ツイート以外のコンテンツを混ぜ合わせ**、お客様の端末に戻して表示させるのである.

The pipeline above runs approximately 5 billion times per day and completes in under 1.5 seconds on average
上記のパイプラインは1日に約50億回実行され、平均1.5秒未満で完了する.
A single pipeline execution requires 220 seconds of CPU time, nearly 150x the latency you perceive on the app.
1回のパイプライン実行に220秒のCPU時間を要し、アプリで感じるレイテンシーの150倍近い時間がかかる.

![](https://cdn.cms-twdigitalassets.com/content/dam/blog-twitter/engineering/en_us/open-source/2023/twitter-recommendation-algorithm/phone-frame-padded.png.img.fullhd.medium.png)

The goal of our open source endeavor is to provide full transparency to you, our users, about how our systems work
オープンソースの目的は、私たちのシステムがどのように機能するかについて、ユーザであるあなたに完全な透明性を提供することである.
We’ve released the code powering our recommendations that you can view here (and here) to understand our algorithm in greater detail, and we are also working on several features to provide you greater transparency within our app
私たちは、私たちのアルゴリズムをより詳しく理解するために、[ここ](https://github.com/twitter/the-algorithm)（と[ここ](https://github.com/twitter/the-algorithm-ml)）で見ることができる私たちの推薦を駆動するコードを公開しました。また、私たちのアプリでより透明性を提供するためにいくつかの機能に取り組んでいる.
Some of the new developments we have planned include:
予定している新展開の一部をご紹介する：

- A better Twitter analytics platform for creators with more information on reach and engagement クリエイターのための、リーチやエンゲージメントに関するより良いTwitter分析プラットフォーム.

- Greater transparency into any safety labels applied to your Tweets or accounts ツイートやアカウントに貼られた安全ラベルの透明性を高める.

- Greater visibility into why Tweets appear on your timeline ツイートがタイムラインに表示される理由をより深く知ることができる.

# What’s Next? 次は何だ？

Twitter is the center of conversations around the world
世界中の会話の中心はTwitter
Every day, we serve over 150 billion Tweets to people’s devices
毎日、1,500億以上のツイートを人々の端末に配信している.
Ensuring that we’re delivering the best content possible to our users is both a challenging and an exciting problem
ユーザに最高のコンテンツを提供することは、チャレンジングであると同時にエキサイティングな問題でもある.
We’re working on new opportunities to expand our recommendation systems—new real-time features, embeddings, and user representations—and we have one of the most interesting datasets and user bases in the world to do it with
私たちは、新しいリアルタイム機能、エンベッディング、ユーザー表現など、レコメンデーションシステムを拡張する新しい機会に取り組んでいる.
We are building the town square of the future
未来の街の広場をつくる
If this interests you, please consider joining us.
もしご興味があれば、ぜひご参加をご検討ください.

Written by the Twitter Team.
文責：Twitterチーム
