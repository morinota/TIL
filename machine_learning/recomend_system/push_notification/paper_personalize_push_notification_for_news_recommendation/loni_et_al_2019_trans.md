### 0.1. link 0.1. リンク

- https://proceedings.mlr.press/v109/loni19a.html httpsを使用しています。

- [pdf](http://proceedings.mlr.press/v109/loni19a/loni19a.pdf) pdf](http:

### 0.2. title 0.2. タイトル

Personalized Push Notifications for News Recommendation
ニュース推薦のためのパーソナライズドプッシュ通知

### 0.3. abstract 0.3. アブストラクト

Push notifications on mobile devices are an important way for users to stay up to date with news.
モバイル端末のプッシュ通知は、ユーザーにとって常に最新のニュースを入手するための重要な手段である.
Push notifications can also be a major source of annoyance for users: being interrupted at the wrong time for something you do not care about is frustrating.
プッシュ通知は、ユーザーにとって大きな悩みの種にもなる. どうでもいいことにタイミング悪く割り込まれるのは、イライラするものである.
It is crucial to ensure the right push is sent to the right user at the right moment.
適切なタイミングで適切なユーザーに適切なプッシュ通知を送信することは、非常に重要.
In this paper we address this problem of personalized push notifications.
この論文では、パーソナライズされたプッシュ通知に関するこの問題に取り組む.
We introduce our streaming push personalization pipeline, describe how we personalize pushes, discuss challenges, and end with open questions.
私たちのストリーミングプッシュパーソナライゼーションパイプラインを紹介し、どのようにプッシュをパーソナライズするかを説明し、課題について議論し、最後にオープンな質問で締めくくる.

## 1. Introduction 1. はじめに

The abundance of online news services makes recommender systems convenient techniques to generate personalized recommendations and help users to discover relevant articles.
オンラインニュースサービスの普及により、推薦システムは個人化された推薦を生成し、ユーザーが関連記事を発見するのを助ける便利な技術となっている.
In such systems, recommendations are typically created by learning to generate a personalized ranked-list for each user.
このようなシステムでは、通常、各ユーザーのためにパーソナライズされたランク付けリストを生成するための学習によって、推薦文が作成される.
The recommendations are then displayed as a list of items on the web or mobile apps.
そして、推薦文はウェブやモバイルアプリにリストとして表示される.

Despite the presence of many studies where recommendations are generated as a ranked list of items (Hopfgartner et al., 2016), to our knowledge, there are no studies that propose to serve personalized news recommendation with push notifications.
推薦がアイテムのランク付けされたリストとして生成される多くの研究が存在するにもかかわらず（Hopfgartner et al., 2016）、**我々の知る限り、プッシュ通知でパーソナライズされたニュース推薦を提供することを提案する研究は存在しない**.
A push notification is a fast and effective way to inform users about the latest and most important news via an in-app message on a mobile device or via a browser message.
プッシュ通知は、モバイルデバイス上のアプリ内メッセージまたはブラウザメッセージを介して、最新かつ最も重要なニュースをユーザーに通知するための迅速かつ効果的な方法である.

In this work we propose a distributed system to create personalized push notifications in the context of a major European news publisher.
この研究では，ヨーロッパの大手ニュース出版社を対象に，パーソナライズされたプッシュ通知を作成するための分散システムを提案する．
In Section 2 We first motivate why it is important to personalize push notifications.
セクション2では、まず、なぜプッシュ通知をパーソナライズすることが重要なのかを説明する.
We then describe our Personalized Push Notification system and its architecture in Section 3.
次に、セクション3では、パーソナライズド・プッシュ通知システムとそのアーキテクチャを説明する.
In Section 4 we discuss open questions and challenges of making personalized pushes.
セクション4では、パーソナライズド・プッシュ通知の作成に関する未解決の質問と課題について説明する.
We briefly describe some related work in Section 5 and finally we draw some conclusion in Section 6.
セクション5では、いくつかの関連する仕事を簡単に説明し、最後にセクション6でいくつかの結論を出す.

## 2. News Consumpition via Push Notification 2. プッシュ通知によるニュース消費

In this section we describe the current model of sending push notifications, as used at DPG Media, 1 discuss the challenges and limitations of the current system and motivate the importance of using a personalized push notification system.
このセクションでは、**DPG Media**で使用されているプッシュ通知送信の現行モデルについて説明し、現行システムの課題と限界について述べ、パーソナライズされたプッシュ通知システムを使用することの重要性を動機付ける.

Currently, push notifications at DPG Media are not personalized.
現在、DPG Media のプッシュ通知は、パーソナライズされていない.
Instead, users of most mobile apps of DPG Media can subscribe to one or more predefined news categoriesin which they are interested in.
その代わり、DPG Mediaのほとんどのモバイルアプリのユーザーは、**興味のある1つまたは複数の定義済みのニュースカテゴリを登録**することができる.
A news editor then decides whether a newly published article should be pushed to all users who have subscribed to its category.
そして、**ニュース編集者が、新しく公開された記事を、そのカテゴリーを購読しているすべてのユーザーにプッシュすべきかどうかを決定**する.
The push-worthiness of the article is thus determined by humans, based on factors such as urgency and importance of the events described in the article.
このように、**記事のプッシュ価値は、記事に書かれている出来事の緊急性や重要性などの要素に基づいて、人間が判断**する.
Figure 1 illustrates the category subscription and a sample push notification from Algemeen Dagblad (AD), the app of one of the most popular newspapers in Europe, published by DPG Media.
図1は、DPG Mediaが発行するヨーロッパで最も人気のある新聞の1つであるAlgemeen Dagblad（AD）のアプリから、カテゴリーの購読とプッシュ通知の例を示したもの.

The existing, non-personalized, setup suffers from several issues.
既存の、パーソナライズされていない設定には、いくつかの問題がある.
First and foremost, not every article that is pushed within a specific category is relevant to all the users who subscribed to that category.
まず第一に、**特定のカテゴリーで配信されるすべての記事が、そのカテゴリーを購読しているすべてのユーザーに関連しているわけではない**.
For instance, within the sports category, news editors can decide to push articles about soccer, cycling, darts, formula 1 etc., however a user subscribed to the sports category will typically not have an interest in all of these subcategories.
たとえば、**スポーツ・カテゴリーでは、ニュース編集者はサッカー、サイクリング、ダーツ、フォーミュラ1などの記事をプッシュすることを決定できますが、スポーツ・カテゴリーを購読しているユーザーは、通常これらのサブカテゴリーすべてに関心を持っているわけではない**.

Second, the push-worthiness of a news article is subjective and is not necessarily equal for all users.
第二に、**ニュース記事のプッシュ価値は主観的なものであり、すべてのユーザーにとって必ずしも平等ではない**.
For example, whether or not a piece of news about formula 1 championship is important and should be pushed is subject to the opinion of the news editor and might not necessarily be relevant to the user.
例えば、フォーミュラ1の優勝に関するニュースが重要でプッシュすべきかどうかは、ニュース編集者の意見に左右され、ユーザーにとって必ずしも適切でない可能性がある.

Finally, since users can only subscribe to a limited number of broad categories, news editors have no means of reaching smaller audiences than those subscribed to the broad categories.
第三に、**ユーザーは限られた数の大分類にしか登録できないため、ニュース編集者は大分類に登録したユーザーよりも小さなオーディエンスにリーチする手段を持たない**.
As a result, our editors only push very few articles, based on their expected relevance to a large audience.
その結果、編集者は、多くの読者との関連性に基づいて、ごく少数の記事のみをプッシュする.
Niche articles, however, will never be pushed to anyone since there is no way for editors to reach a niche audience.
しかし、ニッチな記事は、編集者がニッチな読者にリーチする方法がないため、誰にもプッシュされることはないでしょう。

With personalized push notifications, we aim to address the above shortcomings.
パーソナライズド・プッシュ通知では、上記のような欠点を解決することを目指す.
We want to bring niche articles to only those people who want to read them, while simultaneously filtering out articles that are irrelevant for a given user.
私たちは、**ニッチな記事を読みたい人だけに届けると同時に、特定のユーザーにとって無関係な記事をフィルタリングしたい**と考えている.
Our first instantiation of niches is hyper locality: articles that are specific to a very small region are typically only interesting to a small number of users.
ニッチの最初の例は、hyper localityである. 非常に狭い地域に特化した記事は、通常、少数のユーザーにとってのみ興味深いものである.

## 3. Personalized Push Notification 3. パーソナライズされたプッシュ通知

We address the challenge of news personalization with personalized push notifications.
我々は、パーソナライズされたプッシュ通知によって、ニュースのパーソナライズという課題に取り組んでいる.
Our goal is to find the most relevant news for each user while still bringing diverse news, hence keeping the filter bubble (Pariser, 2011) to a minimum.
我々の目標は、各ユーザーにとって最も関連性の高いニュースを見つけると同時に、多様なニュースを届け、フィルターバブル（Pariser, 2011）を最小限に抑えることである.
More specifically, personalized push notifications should meet the following criteria:
具体的には、パーソナライズド・プッシュ通知は、以下の基準を満たす必要がある.

- **Personalized**: Push notifications should be personalized, that is, the interests and the preferences of the users should be taken into account. パーソナライズされていること. プッシュ通知はパーソナライズされるべき. つまり、ユーザーの興味や嗜好を考慮する必要がある.

- **Explainable**: The reason why a push notification was sent should be explainable to justify the recommendations and establish a ”sense of forgiveness” when users do not find the recommendations relevant to them (Van Barneveld and Van Setten, 2004). 説明可能であること. プッシュ通知が送られた理由は説明可能であるべきで、推薦を正当化し、ユーザーが推薦を自分に関連したものと感じない場合に「許しの感覚」を確立する（Van Barneveld and Van Setten, 2004）.

- **Include important news**: Regardless of the degree of personalization, push notifications should still inform users about breaking news and important updates. 重要なニュースを含める。 パーソナライズの程度にかかわらず、プッシュ通知はニュース速報や重要な更新情報をユーザーに伝える必要がある.

- **Diversity and opposing opinions**: To make sure the personalized recommendations do not create filter bubbles for users, the system should make sure that recommendations are diverse and are not necessarily supporting the opinion that users often read. In particular for a news product, as opposed to a product that is merely entertainment, it is important to maintain objectivity. 多様性と反対意見.パーソナライズド・レコメンデーションがユーザーにとってフィルターバブルを作らないようにするために、システムはレコメンデーションが多様で、必ずしもユーザーがよく読む意見を支持していないことを確認する必要がある. 特にニュース系は、エンターテインメントとは異なり、客観性を保つことが重要である.

- **(Hyper-)local news**: In particular, (hyper-)local news can only ever be pushed when push is personalized. (Hyper-)local news is only relevant to very few users, but to these users, it is typically highly relevant: users care about what happens around the corner. This type of news is not pushed in non-personalized systems: categories that users can subscribe to will never be fine-grained enough. More importantly, in a non-personalized system, human editors will never be able to identify all the small regions an article is relevant to. 超）ローカルニュース：特に、（超）ローカルニュースは、プッシュがパーソナライズされている場合にのみ、プッシュすることが可能. (超）**ローカル・ニュースは、ごく少数のユーザーにしか関係しないが、そのようなユーザーにとっては、通常、非常に関連性の高いものであり、ユーザーは近くで何が起こっているかを気にしている**. この種のニュースは、パーソナライズされていないシステムではプッシュされない. ユーザーが購読できるカテゴリーは、十分にきめ細かいものにはならないからである. さらに重要なことは、パーソナライズされていないシステムでは、人間の編集者は、記事が関連するすべての小さな地域を特定することはできないという事である.

- **Anonymous users**: The majority of the readers are users without an account. The system should be able to learn the preferences of such users. 匿名ユーザー. 読者の大半は、アカウントを持たないユーザーである. そのようなユーザーの嗜好をシステムが学習できるようにする必要がある.

  - NPの場合はここは問題なさそう.

- **Address the cold-start problem**: An inherent challenge in news recommendation is the cold-start problem: news is most relevant shortly after it is published. At that moment, there is no or a very limited number of interactions on the newly published articles and it is therefore not possible to effectively exploit algorithms such as collaborative filtering as they heavily rely on user-item interactions. The system should be capable to effectively exploit the content of news articles to tackle the cold-start problem. コールドスタート問題への対応：ニュース推薦の本質的な課題として、コールドスタート問題がある. その時点では、新しく公開された記事に対するインタラクションがないか、非常に限られているため、協調フィルタリングなどのアルゴリズムは、ユーザーとアイテムのインタラクションに大きく依存しているため、効果的に利用することができない. コールドスタート問題に対処するためには、**ニュース記事の内容を効果的に利用する**ことができるシステムが必要である.
  - (Push通知は基本的に新しいアイテムを推薦する. -> collaborative filteringベースの手法のみでは対応困難 -> content-base的な要素を含める必要がありそう...!)

### 3.1. Architecture 3.1. アーキテクチャ

We propose a distributed, extensible and scalable architecture consisting of several decoupled components that communicate using an asynchronous messaging system.
我々は、非同期メッセージングシステムを使用して通信する、いくつかの非結合コンポーネントから成る、分散、拡張可能でスケーラブルなアーキテクチャを提案する.
We also use Redis, a distributed cache system, in several components to make sure the pipelines can effectively handle the large traffic of incoming articles and user interactions.
また、パイプラインが大量の記事とユーザーインタラクションを効果的に処理できるように、いくつかのコンポーネントで分散キャッシュシステムであるRedisを使用している.
Figure 2 illustrates the high-level architecture of our system.
図2は、本システムのハイレベルなアーキテクチャを示している.
Our system consists of three pipelines, each with a set of independent components:
本システムは**3つのパイプライン**から構成されており、それぞれが独立したコンポーネントを有している.

- **Push pipeline**: this pipeline processes newly published articles and pushes them to the relevant users. Pushパイプライン：新しく公開された記事を処理し、関連するユーザーにプッシュするパイプライン.
- **Profiler pipeline**: this pipeline processes users’ interactions and maintains their profiles. プロファイラーパイプライン：ユーザーのインタラクションを処理し、プロフィールを管理するパイプライン.
- **Evaluation pipeline**: this pipeline decides about the models that should be used, maintains experiments and A/B testing and collect users’ feedback to tune models. 評価パイプライン：使用するモデルを決定し、実験やASPの維持管理を行うパイプライン.

In the next section, each pipeline is described in more detail.
次章では、各パイプラインの詳細を説明する.

#### 3.1.1. Push Pipeline 3.1.1. プッシュパイプライン

As soon as an article is published by a journalist, the article is picked up by the push pipeline.
ジャーナリストによって記事が公開されると、すぐにプッシュ・パイプラインによって記事がピックアップされる.
The article is then enriched and stitched to candidate users.
その後、記事はenrich(?)され、ユーザー候補にstitch(=候補に入る的な意味?)される.
The stitched useritem candidates are then classified and the accepted candidates are pushed to the users.
縫合されたユーザーアイテム候補は分類され、採用された候補はユーザーにプッシュされる.

Figure 3 illustrates the architecture of the push pipeline.
図3は、プッシュパイプラインのアーキテクチャを示したもの.
The pipeline consists of eight independent components that communicate asynchronously in a streaming fashion using Kafka:3
このパイプラインは8つの独立したコンポーネントからなり、Kafkaを使ってストリーミング方式で非同期的に通信を行う.

- **Enricher**: Given an article in JSON format with fields including title, raw text, and author, the Enricher adds metadata including named entities, sentiment (Pang et al., 2002), and IPTC topics.4 エンリッチャ。 タイトル、原文、著者などのフィールドを持つ JSON 形式の記事があると、Enricher は、名前付きエンティティ、センチメント (Pang et al., 2002)、IPTC トピックなどのメタデータを追加する.
- **Stitcher**: Given an enriched article, the Stitcher queries the user profile for all users that might be interested in the article. It produces a tuple consisting of an article and a user profile, i.e., a user-item, to the next Kafka topic. Stitcher。 エンリッチされた記事が与えられると、Stitcherはその記事に興味を持ちそうなすべてのユーザーに対して、ユーザープロファイルを問い合わせる. 記事とユーザープロファイルからなるタプル、つまりユーザーアイテムを次のKafkaトピックに生成する.
- **Featurizer**: Given a user-item, the Featurizer extracts features and adds them to the next Kafka topic. Some examples of features are: 1) the degree to which a user is interested in the location of the article, 2) cosine similarity between a content embedding of the article and the user, 3) the amount of interest the user showed in the author of the article. Currently we use a Word2Vec model (Mikolov et al., 2013) to produce embeddings of users and articles from their Bag-of-Words (BoW) representations. A user’s BoW is the aggregation of the BoW of the articles that they read in the past. フィーチャライザー。 ユーザーアイテムが与えられると、**特徴を抽出**し、次のKafkaトピックに追加する. **特徴量の例としては 例えば、1) ユーザが記事のlocationに興味を持つ度合い、2) 記事のコンテンツ埋め込みとユーザとのコサイン類似度、3) ユーザが記事の著者に示した興味の度合い、など**である. 現在、我々は**Word2Vecモデル(Mikolov et al., 2013)**を用いて、**Bag-of-Words(BoW)表現からユーザと記事の埋め込み**を生成しています. ユーザーのBoWは、過去に読んだ記事のBoWを集約したものである.
- **Classifier**: Given the user-item features, the Classifier decides whether the item is relevant for the user. If relevant, the Classifier adds the item to the next Kafka topic. Classifier（クラシファイア）。 ユーザーとアイテムの特徴が与えられたら、クラシファイアは**そのアイテムがユーザーに関連しているかどうかを判断**する. 関連性がある場合、クラシファイアはそのアイテムを次のKafkaトピックに追加する.
- **Modeler**: Given a historical dataset of user profiles and items, the Modeler allows for creating classification models for the Classifier. Modeler（モデラー）。 ユーザープロファイルとアイテムの履歴データセットが与えられると、ModelerはClassifierのための分類モデルを作成する.
- **Bouncer**: Given an incoming message from a Kafka topic, the Bouncer decides to add it to the next Kafka topic or not, based on business rules such as a limit on the total number of pushes we send on a day. Bouncer（バウンサー）。 Kafkaトピックから受信したメッセージを、1日に送信するプッシュ総数の制限などのビジネスルールに基づいて、次のKafkaトピックに追加するかどうかを決定するバウンサー.
- **Switcher**: Given the accepted push candidates, the switcher dispatches the push candidates to different A/B buckets using our A/B testing service. Depending on the configuration of the bucket that a push candidate is assigned to, the switcher decides whether a push candidate should be pushed or not. Bouncer also makes sure that the items that are already pushed to a users are not pushed again. スイッチャーは、受け取ったプッシュ候補を、A/Bテストサービスを使って、異なるA/Bバケットに振り分ける. プッシュ候補が割り当てられたバケットの構成に応じて、スイッチャーはプッシュ候補をプッシュすべきかどうかを判断する. また、Bouncerは既にプッシュされているアイテムが再度プッシュされないようにする.
- **Pusher**: Given user-items, the Pusher formats the actual push notification. Furthermore, it adds a message to the topic for updating the profile and notifying the AB-platform that a push notification is sent out. Pusherです。 ユーザーアイテムが与えられると、Pusherは実際のプッシュ通知をフォーマットする. さらに、プロフィールを更新し、プッシュ通知が送信されたことをABプラットフォームに通知するために、トピックにメッセージを追加する.

Note that all our components can be scaled up horizontally with demand.
なお、当社のすべてのコンポーネントは、需要に応じて水平方向にスケールアップすることが可能です。

#### 3.1.2. Profile Pipeline 3.1.2. プロファイルパイプライン

An important aspect of a recommender system is to be able to properly represent a user.
推薦システムにおいて重要なことは、**ユーザを適切に表現できること**である.
In our system, a user is represented by a rich profile that is created based on the users’ interaction data and is further enriched with article data and potentially contextual information.
本システムでは、ユーザの Interaction データに基づき作成され、さらに記事データおよび潜在的な文脈情報によって強化されたリッチプロファイルによって、ユーザを表現する.
We continuously update user profiles while also keeping daily records, i.e., a single representation of each user is created every day.
我々はユーザプロファイルを継続的に更新すると同時に、日々の記録を保持する. つまり、**各ユーザの単一の表現が毎日作成**される.
The daily user profiles are later aggregated, with an aggregator job, to have a more complete representation of users.
**日次のユーザープロファイルは後にaggregator jobによって集約**され、より完全なユーザ表現が得られる.
We use Elasticsearch5 to store user profiles.
ユーザープロファイルの保存には、Elasticsearch5を使用している.
Daily profiles are also stored in a Redis cache to avoid frequent I/O and to improve the scalability of the pipeline.
また、日々のプロファイルはRedisキャッシュに保存され、頻繁なI/Oを回避し、パイプラインのスケーラビリティを向上させる.

Representing users with daily profiles has two advantages.
**ユーザーを日次プロフィールで表現することには、2つの利点**がある.
First, the model can be trained with a varying window of interaction data, depending on the intended length of the time window.
まず、意図する時間窓の長さに応じて、Interaction データの窓を変えてモデルを学習することができる.
A benefit of this approach is that we can train and predict with only recent user interactions and therefore the recommendations are adapted with the change of user preferences over time.
このアプローチの利点は、**最近のuser interactions のみで学習・予測できる**ため、時間の経過に伴うユーザー嗜好の変化に合わせてレコメンデーションが適応されることである.
Recency has been shown to be effective in generating recommendations (Li et al., 2014).
Recencyはレコメンデーションの生成に有効であることが示されている（Li et al.，2014）。
Second, the granularity of daily profiles makes it easy to discard old interactions.
第二に、日々のプロファイルの粒度により、古いインタラクションを簡単に捨てることができる.
This is particularly important with the new GDPR regulations 6 since online services are not allowed to keep user interaction histories indefinitely.
これは、新しいGDPR規制6により、オンラインサービスがユーザーとのインタラクション履歴を無期限に保持することが許されないため、特に重要である.
In our system, this is achieved by deleting old daily profiles.
本システムでは、古い日別プロフィールを削除することでこれを実現している.

Figure 4 illustrates the profiler pipeline.
図 4 は、profiler pipelineを示したもの.
User events are collected from different channels, processed and persisted to daily Elasticsearch indices.
ユーザイベントはさまざまなチャネルから収集され、処理されて日次の Elasticsearch インデックスに永続化される.
The profiles are accessible through a RESTful API, which is used by the push pipeline.
プロファイルは RESTful API でアクセス可能で、プッシュ・パイプラインで使用される.

#### 3.1.3. Evaluation Pipeline 3.1.3. 評価パイプライン

Our pipeline integrates an ongoing evaluation process that runs multiple experiments with A
私たちのパイプラインは、複数の実験を行う継続的な評価プロセスを統合している.

### 3.2. Modeling

Our setup allows the integration of any recommendation model to our pipeline.
また、あらゆる推薦モデルをパイプラインに統合することが可能.
The modular setup of the Featurizer and Classifier makes it possible to run multiple classification models.
FeaturizerとClassifierのモジュラーセットアップにより、複数の分類モデルを実行することが可能.
Our current model combines a content similarity score with a location overlap score.
現在のモデルは、**content similarityスコア**と**location overlapスコア**の組み合わせである.

The content similarity score is the cosine similarity between the content of the item and the aggregated content read by a user, as stored in his
content similarityスコアは、アイテムの内容(=アイテムのテキスト埋め込みベクトル?)と、ユーザが読んだ内容を集約したもの(=アイテム埋め込みベクトルの平均?)とのcosine類似度である.

The location overlap score is a weighted sum of two location ratios:
location overlapスコアは、**2つの location ratio の加重和**である.

- the first measures the ratio of the extracted locations in the article to the number of locations the user has previously read about. 第1項は、記事中の抽出された場所の、ユーザーが以前に読んだことのある場所の数に対する比率を測定する.
- The second term measures the ratio of the locations in the article to the number of locations that the user has previously physically visited while reading articles in the AD app. 2つ目の項は、ユーザーがADアプリで記事を読みながら**過去に物理的に訪れた場所の数(??)**に対する記事中の場所の比率を測定する.
  Formally, we calculate the location overlap score as follows:
  正式には、以下のように location overlap スコアを算出する.

$$
l_{overlap} = w \frac{|l_{user} \cap l_{item}|}{|l_{user}|}
+ (1 - w) \frac{|gl_{user} \cap gl_{item}|}{|gl_{user}|}
\tag{1}
$$

where,
ここで、

- $l_{user}$ is the set of article locations previously read by the user,
  - $l_{user}$はユーザーが過去に読んだ記事のlocations(=これも文脈から抽出した"location"に関するtokenの集合??)の集合
- $gl_{item}$ is the set of physical locations of the user while reading articles in the AD app,
  - $gl_{item}$はADアプリで記事を読んでいる時のユーザーの物理的位置(位置情報??)の集合、
- $l_{item}$ is the set of extracted locations from the article,
  - $l_{item}$は記事から抽出した場所の集合(NLP的なアプローチで"location"に関するtokenを抽出してる?)
- $w$ is a weight parameter that controls the contribution of the above ratios on the calculated score.
  - $w$は上記の比率の計算スコアへの寄与を制御する重みパラメータである.

In our current setup, based on an experiment on a small number of users, we found $w = 0.7$ to be an appealing value for the weight parameter.
現在の設定では、少数のユーザーを対象とした実験に基づき、重みパラメータの値として$w=0.7$が魅力的であることがわかった.
Future work involves further tunning of this parameter based on experiments on larger number of users.
今後、より多くのユーザーを対象とした実験により、このパラメータをさらにチューニングする予定である.

## 4. Future Work and Open Questions 4. 今後の課題および未解決の問題

Personalizing push notifications breaks some new ground.
プッシュ通知のパーソナライズには、新しい領域がある.
Below are our biggest challenges.
以下は、私たちの最大のチャレンジである.

- **Daily limits**: Imagine the following scenario: we limit the number of push notifications per user per day to 10, and in the morning there is a series of articles that is urgent and relevant to a user. What should we do? Should we deplete the 10 pushes right away, not knowing what the rest of the day might bring us? We currently limit the number of pushes to 1 per 5 minutes, 2 per hour, and 10 per day. But we plan to experiment with these settings and are considering personalizing these as well. 1日の制限 次のようなシナリオを想像してみてください。1日のユーザーあたりのプッシュ通知数を10件に制限しているときに、朝になって、あるユーザーにとって緊急かつ関連性の高い一連の記事があったとする. どうしたらよいだろうか. その日のうちに何が起こるかわからないのに、すぐに10プッシュを使い果たすべきだろうか？ 現在、私たちはプッシュの回数を5分ごとに1回、1時間ごとに2回、1日ごとに10回に制限している. しかし、これらの設定を実験する予定ですし、パーソナライズすることも検討している.
- **Diversity**: As mentioned in Section 3, we aim to recommend diverse news to users. Diversity involves both near duplicate prevention and topic diversification. Since push recommendation is not a ranking problem, diversity becomes an issue as most of the existing literature on diversification focus on diversifying top-N recommendation lists (Hurley and Zhang, 2011). It is not straightforward to get a holistic view on all the sent push notifications in the way we can do this when composing a ranking. Classical diversity algorithms, such as maximal marginal relevance – MMR, (Carbonell and Goldstein, 1998) – are therefore not directly applicable. We can, however, take into account the similarity of an article to articles we pushed earlier. Currently, we do this to avoid sending near duplicate pushes. Future plans include exploitation of diversification algorithms that diversify the topics that are covered for each user. 多様性 セクション 3 で述べたように，我々は多様なニュースをユーザに推薦することを目的としている． 多様性には、**重複防止** と **トピックの多様化** の両方が含まれる. プッシュ通知はランキングの問題ではないので、**多様化に関する既存の文献のほとんどがトップNの推薦リストの多様化に焦点を当てている**ため、多様性が問題になる（Hurley and Zhang, 2011）. ランキングを構成するときにできる方法で、送信されたすべてのプッシュ通知を全体的に把握することは簡単ではありません。 したがって、最大限界関連性（MMR）（Carbonell and Goldstein, 1998）のような古典的な多様性アルゴリズムは、直接適用することができません。 しかし、私たちが以前にプッシュした記事との類似性を考慮することは可能です。 現在では、ほぼ重複したプッシュを送るのを避けるためにこれを行います。 将来的には、ユーザーごとにカバーするトピックを多様化させる多様化アルゴリズムを利用することも計画しています。
- **Explainability**: In Figure 1 we show a recommendation explanation right below the push notification “Because we think you are interested in World Cup 2018.” We currently do not support this feature, but we consider providing the most prevalent reason that caused our algorithm to push this specific article to this user, for example using the approach introduced by ter Hoeve et al. (2018). 説明可能性 図1では、"Because we think you are interested in World Cup 2018 "というプッシュ通知のすぐ下にレコメンデーション説明が表示されている. 現在この機能をサポートしていませんが、例えばter Hoeveら（2018）が紹介したアプローチを用いて、我々のアルゴリズムがこの特定の記事をこのユーザーにプッシュする原因となった、最も一般的な理由を提供することを検討している.
- **Explicit Feedback**: Once we provided recommendation reasons, we intend to provide users with a means to give feedback on those reasons. In Figure 1 we show feedback buttons that are intended for a user to provide feedback, not on this specific article but on the reason that caused us to push this article. This type of feedback can readily be used to update the profile we maintain for this user. フィードバックの明示 推薦の理由を説明した後は、その理由に対するフィードバックをユーザーに提供することを意図している. 図 1 に示すフィードバックボタンは、ユーザーが特定の記事ではなく、この**記事を推薦した理由に対してフィードバックを提供するためのもの**である. このタイプのフィードバックは、このユーザーのプロフィールを更新するために容易に利用することができる.
- **Timing**: Some content is less time sensitive and can be scheduled for the right time for a user. For example, the relevance of articles about parenting depends on a user’s life phase. To be able to recommend such articles to users at the right moment, we need a classifier that predicts the ‘expiration date’ of an item. Currently, we only push articles that are at most 1 hour old. タイミング。 コンテンツによっては、時間的な制約が少なく、ユーザーにとって適切なタイミングでスケジュールを組むことができるものもある. たとえば、子育てに関する記事の関連性は、ユーザーのライフ・フェーズに依存する. このような記事を適切なタイミングでユーザーに推薦できるようにするためには、アイテムの「有効期限」を予測する分類器が必要. 現在、私たちは最大で1時間前の記事のみをプッシュしている.

## Related Work 関連作品

The majority of the published articles on news recommendation adapt content-based methods to address common challenges in news recommendation such as cold-start, sparsity, and recency (Karimi et al., 2018).
**ニュース推薦に関する発表論文の大半は、コールドスタート、スパース性、recencyといったニュース推薦における共通の課題に対処するために、コンテンツベースの手法を適応させている**（Karimi et al.、2018）。
Moreover, news recommender systems should be scalable and fast to be able to serve real-time recommendations to a large number of users in a few milliseconds.
さらに、ニュース推薦システムは、**数ミリ秒で多数のユーザーにリアルタイムの推薦を提供できるように、スケーラブルで高速である必要がある**.
The work of Lu et al. (2014) is an example of a scalable news recommender system where the scalability is achieved by adapting MinHash clustering to search similar users within smaller clusters.
Luら（2014）の仕事は、スケーラブルなニュース推薦システムの例であり、スケーラビリティは、より小さなクラスタ内の類似ユーザーを検索するためにMinHashクラスタリングを適応させることによって達成されている.
Doychev et al. (2014) propose a scalable architecture that could address the short-response-time requirement of the Plista news personalization challenge.
Doychevら（2014）は、Prista news personalization challengeの短応答時間要件に対応しうるスケーラブルなアーキテクチャを提案している.
Their model benefits from pre-computed recommendations that are stored in a Redis cache while the recommendations are updated in the background as frequently as possible.
彼らのモデルは、Redisキャッシュに保存される事前計算された推薦文の恩恵を受け、推薦文はバックグラウンドで可能な限り頻繁に更新される.

From the modeling perspective, (Kompan and Bielikov´a, 2010) and (IJntema et al., 2010) are examples of content-based methods where TF-IDF and ontology-based concepts are used to construct user profiles and find similar articles.
モデリングの観点から、(Kompan and Bielikov´a, 2010) と (IJntema et al., 2010) は、TF-IDF とオントロジーベースのコンセプトがユーザープロファイルの構築と類似記事の検索に使用されているコンテンツベースの手法の例.
The work of Montes-Garcia et al. (2013) is an example where the geographical proximity of users to news articles is exploited as an indication of the relevance of the articles to users.
Montes-Garcia et al. (2013) の研究は、**ニュース記事へのユーザーの地理的な近接性**が、ユーザーへの記事の関連性の指標として利用されている例である.

## Conclusion 結論

In this paper, we present an overview of our streaming personalized push notification framework for the news domain.
本論文では、ニュース領域向けのストリーミングパーソナライズドプッシュ通知フレームワークの概要を紹介する.
We propose an adaptive and scalable system that is capable of integrating different recommender models to build personalized push notifications.
我々は、パーソナライズドプッシュ通知を構築するために、異なるレコメンダーモデルを統合することができる適応的でスケーラブルなシステムを提案する.
In contrast to the mainstream recommender system models where recommendations are typically served as a list, personalized push notifications are arbitrary recommendations that can be sent to users at any time.
推薦が一般的にリストとして提供される主流の推薦システムモデルとは対照的に、パーソナライズドプッシュ通知は、いつでもユーザーに送ることができる任意の推薦である.

Due to the nature of personalized push notifications for news, recommendations should be generated real-time when articles are published.
ニュースのパーソナライズド・プッシュ通知の性質上、**記事が公開されたときにリアルタイムでレコメンデーションが生成される必要がある**.
Building such a system requires a proper architecture that can address issues such as scalability, performance, cold-start, timing and daily limits.
このようなシステムを構築するには、スケーラビリティ、パフォーマンス、コールドスタート、タイミング、日数制限などの問題に対処できる適切なアーキテクチャが必要.
Moreover, the system should be able to generate diverse, explainable and fair recommendations.
さらに、多様で、説明可能で、公平なレコメンデーションを生成できるシステムでなければならない.
Our distributed system is capable of plugging various models and constraints as different components to address the above issues.
我々の分散システムは、上記の問題に対処するために、様々なモデルや制約を異なるコンポーネントとして差し込むことが可能である.

## Reference

- Jaime G Carbonell and Jade Goldstein. The use of mmr and diversity-based reranking for reodering documents and producing summaries. 1998.
- Doychin Doychev, Aonghus Lawlor, Rachael Rafter, and Barry Smyth. An analysis of recommender algorithms for online news, 2014.
- Frank Hopfgartner, Torben Brodt, Jonas Seiler, Benjamin Kille, Andreas Lommatzsch, Martha Larson, Roberto Turrin, and Andr´as Ser´eny. Benchmarking news recommendations: The clef newsreel use case. SIGIR Forum, 49(2):129–136, January 2016. ISSN 0163- 5840. doi: 10.1145/2888422.2888443. URL http://doi.acm.org/10.1145/2888422.2888443.
- Neil Hurley and Mi Zhang. Novelty and diversity in top-n recommendation – analysis and evaluation. ACM Trans. Internet Technol., 10(4):14:1–14:30, March 2011. ISSN 1533- 5399. doi: 10.1145/1944339.1944341. URL http://doi.acm.org/10.1145/1944339. 1944341.
- Wouter IJntema, Frank Goossen, Flavius Frasincar, and Frederik Hogenboom. Ontologybased news recommendation. In Proceedings of the 2010 EDBT/ICDT Workshops, EDBT ’10, pages 16:1–16:6, New York, NY, USA, 2010. ACM. ISBN 978-1-60558-990-9. doi: 10.1145/1754239.1754257. URL http://doi.acm.org/10.1145/1754239.1754257.
- Mozhgan Karimi, Dietmar Jannach, and Michael Jugovac. News recommender systems – survey and roads ahead. Information Processing and Management, 54(6):1203 – 1227, 2018. ISSN 0306-4573. doi: https://doi.org/10.1016/j.ipm.2018.04.008. URL http://www.sciencedirect.com/science/article/pii/S030645731730153X.
- Michal Kompan and M´aria Bielikov´a. Content-based news recommendation. In Francesco Buccafurri and Giovanni Semeraro, editors, E-Commerce and Web Technologies, pages 61–72, Berlin, Heidelberg, 2010. Springer Berlin Heidelberg. Lei Li, Li Zheng, Fan Yang, and Tao Li. Modeling and broadening temporal user interest in personalized news recommendation. Expert Systems with Applications, 41(7):3168 – 3177, 2014. ISSN 0957-4174. doi: https://doi.org/10.1016/j.eswa.2013.11.020. URL http://www.sciencedirect.com/science/article/pii/S0957417413009329.
- Meilian Lu, Zhen Qin, Yiming Cao, Zhichao Liu, and Mengxing Wang. Scalable news recommendation using multi-dimensional similarity and jaccard-kmeans clustering. J. Syst. Softw., 95:242–251, September 2014. ISSN 0164-1212. doi: 10.1016/j.jss.2014.04. 046. URL http://dx.doi.org/10.1016/j.jss.2014.04.046.
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. Distributed representations of words and phrases and their compositionality. In Proceedings of the 26th International Conference on Neural Information Processing Systems - Volume 2, NIPS’13, pages 3111–3119, USA, 2013. Curran Associates Inc. URL http://dl.acm. org/citation.cfm?id=2999792.2999959.
- Alejandro Montes-Garcia, Jose Maria Alvarez-Rodriguez, Jose Emilio Labra-Gayo, and Marcos Martinez-Merino. Towards a journalist-based news recommendation system: The wesomender approach. Expert Systems with Applications, 40(17):6735 – 6741, 2013. ISSN 0957-4174. doi: https://doi.org/10.1016/j.eswa.2013.06.032. URL http: //www.sciencedirect.com/science/article/pii/S0957417413004272.
- Bo Pang, Lillian Lee, and Shivakumar Vaithyanathan. Thumbs up? sentiment classification using machine learning techniques. In Proceedings of EMNLP, pages 79–86, 2002.
- Eli Pariser. The filter bubble: What the Internet is hiding from you. Penguin UK, 2011.
- Maartje ter Hoeve, Anne Schuth, Daan Odijk, and Maarten de Rijke. Faithfully explaining rankings in a news recommender system. arXiv preprint arXiv:1805.05447, 2018.
- Jeroen Van Barneveld and Mark Van Setten. Designing Usable Interfaces for TV Recommender Systems, pages 259–285. Springer Netherlands, Dordrecht, 2004. ISBN 978-1-4020-2164-0. doi: 10.1007/1-4020-2164-X 10. URL https://doi.org/10.1007/ 1-4020-2164-X_10.
