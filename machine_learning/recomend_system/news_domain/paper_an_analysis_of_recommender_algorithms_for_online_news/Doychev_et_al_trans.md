## link 

- [pdf](https://ceur-ws.org/Vol-1180/CLEF2014wn-Newsreel-DoychevEt2014.pdf) pdf](https:

## title タイトル

An Analysis of Recommender Algorithms for Online News
オンラインニュースの推薦アルゴリズムの分析

## abstract アブストラクト

# Introduction はじめに

Recommender systems have become an essential part of our day-to-day lives, when it comes to dealing with the overwhelming amount of information available, especially online.
レコメンダーシステムは、特にオンラインで利用可能な圧倒的な量の情報を扱う際に、私たちの日常生活に欠かせないものとなっています。
Recommender systems improve user experience and increase revenue in the context of online retail stores (Amazon, eBay), online news providers (Google News, BBC) and many more.
リコメンダーシステムは、オンライン小売店（Amazon、eBay）、オンラインニュースプロバイダ（Google News、BBC）、その他多くの文脈で、ユーザー体験を向上させ、収益を増加させることができる。
In this work we present a wide range of online recommender algorithms and compare their performance in the scope of the CLEF-NewsREEL 2014 online challenge.
この作品では、幅広いオンライン推薦アルゴリズムを紹介し、CLEF-NewsREEL 2014オンラインチャレンジの範囲内でその性能を比較します。
In CLEF-NewsREEL 2014, participating teams connect to the Plista Open Recommendation Platform [1, 2] and have to respond to real-time user requests for recommendations.
CLEF-NewsREEL 2014では、参加チームはPrista Open Recommendation Platform [1, 2]に接続し、推奨に対するユーザーの要求にリアルタイムで応答しなければなりません。
Given that recommender systems have traditionally been evaluated offline, this poses an interesting challenge in terms of algorithm efficiency, tracking users, building quality models of user browsing behaviours and preferences, and in terms of dealing with a highly dynamic domain like news in which there is a constant cycle of new articles appearing and older articles becomming redundant.
従来、推薦システムはオフラインで評価されてきたため、アルゴリズムの効率性、ユーザーの追跡、ユーザーの閲覧行動や嗜好の品質モデルの構築、そして、新しい記事が現れ古い記事が冗長になるサイクルが常に存在するニュースのような非常に動的な領域を扱う点で、これは興味深い挑戦となっている。
We consider the challenges of online news recommendation more fully in Section 3.1.
オンラインニュース推薦の課題については3.1節でより詳細に検討する。
The rest of this article is organised as follows: in Section 2 we present some related research in news recommendation; in Section 3 we provide a more detailed description of the Plista ORP framework[3] and the CLEF-NewsREEL challenge, the challenges of online news recommendation, and our system architecture; in Section 4 we describe our recommender algorithms; in Section 5 we report and analyse the data collected and the performance of our recommender algorithms, and in Section 6 we conclude and discuss directions for future research.
本論文の残りの部分は以下のように構成される：セクション 2 ではニュース推薦に関するいくつかの関連研究を紹介し，セクション 3 では Plista ORP フレームワーク[3] と CLEF-NewsREEL 課題，オンラインニュース推薦の課題と我々のシステムアーキテクチャについてより詳細に説明し，セクション 4 では我々の推薦アルゴリズムを説明し，セクション 5 では集めたデータと我々の推薦アルゴリズムの性能を報告し分析し，セクション 6 では結論と将来の研究の方向性について議論する．

# Background 背景

Within the field of recommender systems, the problem of recommending news articles to readers has a number of unique and interesting features.
レコメンダーシステムの分野では、ニュース記事を読者に推薦する問題には、多くのユニークで興味深い特徴がある。
In many traditional application domains of recommender systems a user profile is built from a users transaction or preference history, for example movies that have been rated or products purchased.
従来のレコメンダーシステムの応用分野では、ユーザーの取引や嗜好の履歴からユーザープロファイルが構築される。例えば、評価された映画や購入した商品などである。
The profile is associated with the user as they interact with the site, and feeds into the creation of personalised recommendations.
このプロファイルは、ユーザーがサイトを利用する際に関連付けられ、パーソナライズされたレコメンデーションの作成に利用される。
In the news domain it is generally not common to have detailed user profiles, as users are not often required to sign in or create profiles.
ニュース分野では、ユーザーがサインインしたりプロフィールを作成したりする必要があまりないため、詳細なユーザープロファイルを持つことは一般的ではありません。
It is also uncommon in the news domain for users to explicitly provide feedback on each news article they read and often the only feedback available is implicit in the logs of the users click patterns.
また、ニュース領域では、ユーザーが読んだ各ニュース記事に対して明示的にフィードバックを提供することは珍しく、ユーザーのクリックパターンのログから暗黙的に得られるフィードバックしか得られないこともよくあります。
This presents a particular challenge for collaborative filtering methods which rely on the opinions of similar users to generate recommendations [4–6].
このことは、類似したユーザーの意見に依存して推薦を生成する協調フィルタリング手法にとって、特別な課題を提示します[4-6]。
Further complications for collaborative filtering arise from the dynamic nature of the users and the news articles themselves [7, 8].
さらに、協調フィルタリングは、ユーザーとニュース記事自体の動的な性質から生じる[7, 8]。
In general, users will prefer fresher news articles, and building an accurate model of user preferences based on the items they have previously read can be difficult [7, 9, 10].
一般に，ユーザはより新鮮なニュース記事を好みますが，ユーザが以前に読んだ記事に基づいてユーザの嗜好の正確なモデルを構築することは困難です[7, 9, 10]．
While users may have preferred categories of news articles, or topics they are particularly interested in, these preferences are difficult to learn [11, 12].
また，ユーザは好みのニュース記事のカテゴリや，特に関心のあるトピックをもっているかもしれませんが，これらの嗜好を学習することは困難です[11, 12]．
User preferences change over time too, and another challenge is to provide a diverse set of interesting recommendations, accounting for known users preferences and recency and popularity of the news articles themselves [13, 14].
また、ユーザーの好みは時間とともに変化するため、既知のユーザーの好みやニュース記事自体の最新性や人気度を考慮した上で、興味深い推薦文を多様に提供することも課題となっています[13, 14]。
Content based approaches can run into problems where some measures of similarity identify news articles which are in fact about different topics.
コンテンツベースのアプローチでは、ある類似性の尺度が、実際には異なるトピックに関するニュース記事を識別するという問題に直面することがある。
Extracting the constantly changing distribution of topics in the news presents a challenge [9, 15] in addition to learning how users choices are influenced by these latent factors [6, 16, 17].
このような潜在的な要因によってユーザの選択がどのように影響されるかを学習することに加え、常に変化するニュース内のトピックの分布を抽出することが課題となっている[9, 15]。

# Methodology メソドロジー

Plista provides the ORP platform for making live recommendations to a number of their client sites.
Plistaは、多くのクライアントサイトにライブレコメンドを行うためのORPプラットフォームを提供しています。
Plista communicates with the teams via an HTTP API, by sending (JSON) messages.
PlistaはHTTP APIを通じて、各チームと（JSON）メッセージを送信することで通信を行う。
These messages are triggered when a user reads an article or clicks on a recommendation (event notification), and whenever an article is created or updated by the publisher (item update).
これらのメッセージは、ユーザーが記事を読んだり、レコメンドをクリックしたりしたとき（イベント通知）、記事が作成されたり、出版社によって更新されたりしたとき（アイテム更新）、トリガーされます。
Requests for article recommendations (recommendation request) are sent as message to the teams, to which a response must be given within a certain timeframe (100ms).
記事の推薦を求めるリクエスト（推薦リクエスト）はチームにメッセージとして送られ、一定の時間枠（100ms）内に応答する必要があります。
The resulting dataset is unique in many respects, providing detailed user profile information for some users where available and cross-domain data from 11 different news providers.
このデータセットは，11の異なるニュースプロバイダーからのクロスドメインデータと，一部のユーザーの詳細なプロフィール情報を提供する，多くの点でユニークなデータセットである．
The dataset is fully described in [1].
このデータセットについては、[1]で詳しく説明されている。
With each message type (request, event, update) the Plista ORP framework provides additional metadata regarding the current user and article.
Plista ORPフレームワークは、各メッセージタイプ（リクエスト、イベント、アップデート）ごとに、現在のユーザーと記事に関する追加のメタデータを提供します。
Although the Plista ORP API documentation lists almost 60 fields of information, in practice we found many were unclear, or not useful or detailed enough to use.
Plista ORPのAPIドキュメントには、約60のフィールドがありますが、実際に使ってみると、不明確なものや、役に立たないもの、十分に詳細ではないものが多くありました。
Fields like Filter allowosr typify the ones we simply didn’t understand (they had no description either), and popular demographic signals like age, gender and income, expressed as probabilities (male vs female, age and income brackets) turned out to be too vague to be of use in reality.
Filter allowosrのようなフィールドは、単に理解できなかったものの代表で（彼らも説明がありませんでした）、年齢、性別、収入などの一般的な人口統計学的シグナルは、確率（男性対女性、年齢と収入のブラケット）として表現され、現実に使用するにはあまりにも曖昧であることが判明しました。
In the end, we settled on 8 metadata fields for use in our recommenders:
最終的に、レコメンダーで使用するメタデータフィールドは8つに絞られました。

- geo user: The geolocation of the user geo user: ユーザーのジオロケーション

- time weekday: The day of the week 時間 平日 曜日

- category: The subcategory under which an article is published within a given domain, e.g. sport, world, local etc. カテゴリ。 スポーツ、ワールド、ローカルなど、特定のドメイン内で記事が掲載されるサブカテゴリ。

- time hour: The hour of the day 時間目 その日の時間

- item source: The unique item (article) identifier アイテムのソース。 アイテム(記事)の一意な識別子

- publisher: The publisher (domain) of an article. publisher: 記事の発行元（ドメイン）。

- keyword: Keywords with their corresponding counts occurring in the article keyword: 記事中に出現するキーワードとその数

- user cookie: The user id, which is not necessarily unique ユーザークッキー。 ユーザーID（必ずしも一意ではない

Note that the category, publisher and keyword fields only provide a numerical id rather than a textual representation.
カテゴリー、出版社、キーワードの各フィールドは、テキスト表現ではなく、数値のIDを提供するだけであることに注意してください。
For category and publisher it was possible to exploit URLs in order to determine this information, but for keywords there was no way to uncover what the words actually were, or how they were chosen.
カテゴリーと出版社については、この情報を判断するためにURLを利用することが可能でしたが、キーワードについては、実際にどのような言葉が使われているのか、どのように選ばれたのかを明らかにする方法はありませんでした。
Nonetheless, we found that despite this the keywords still provided a useful signal.
しかし、それにもかかわらず、キーワードはまだ有用なシグナルを提供していることがわかった。
In Section 5 we provide a deeper analysis of the data provided and used.
セクション5では、提供され使用されたデータについて、より深い分析を行う。

## Challenges チャレンジ

In this section we present the challenges of producing online news recommendations.
このセクションでは、オンライン・ニュースの推薦文を作成する際の課題を紹介する。
In the section that follows, we detail the system architecture that we have implemented to cope with these challenges.
その後に続くセクションでは、これらの課題に対処するために実装したシステムアーキテクチャの詳細を説明する。
Traditionally, recommender systems are evaluated offline, with plenty of time to build complex models of user browsing behaviours and preferences.
伝統的に、推薦システムはオフラインで評価され、ユーザーの閲覧行動や嗜好の複雑なモデルを構築するのに十分な時間がある。
In realtime online scenarios like CLEF-NewsREEL however, such leisure is not afforded; not only do teams have to respond within a very tight timeframe (100ms), they also have to deal with factors like the lack of rich user browsing history as users are not obliged to register and therefore do not always have persistent profiles or identifiers.
しかし、CLEF-NewsREELのようなリアルタイムのオンラインシナリオでは、そのような余裕はありません。チームは非常に厳しい時間枠（100ms）内で応答しなければならないだけでなく、ユーザーは登録する義務がないため、常に持続的なプロファイルや識別子を持つとは限らず、豊富なユーザーの閲覧履歴などの要因に対処しなければならないのです。
Moreover, a user can access the news sites from different devices, and many users can do so from the same shared device, further complicating the ability to reliably track their browsing, as pointed out in [1].
さらに、ユーザーは異なるデバイスからニュースサイトにアクセスすることができ、多くのユーザーが同じ共有デバイスからアクセスできるため、[1]で指摘したように、ユーザーのブラウジングを確実に追跡する能力はさらに複雑になっています。
Tracking user preferences is also non-trivial, as users do not provide any explicit feedback about recommendation quality, and clickstream data is the only signal of relevance available.
また、ユーザーは推薦の質に関する明示的なフィードバックを提供せず、クリックストリームデータが唯一の関連性のシグナルとなるため、ユーザーの嗜好を追跡することも自明ではありません。
Finally, the nature of the news domain itself throws its own set of challenges into the mix due to the dynamic nature of the data, where many new articles appear every hour, and older articles quickly become redundant.
さらに、ニュースの性質として、1時間ごとに新しい記事が現れ、古い記事はすぐに冗長になるというデータの動的な性質があり、独自の課題を投げかけている。
In such unstructured and dynamic environments, it is necessary to apply techniques that satisfy requirements such as response time and scalability while improving the user experience using limited and sometimes noisy information.
このような非構造的で動的な環境では、限られた、時にはノイズの多い情報を使ってユーザー体験を向上させながら、応答時間やスケーラビリティなどの要件を満たす技術を適用する必要があるのです。

## System Architecture システムアーキテクチャ

Our system architecture, shown in Fig 1, is implemented in Python and is designed to accomplish our goals of scalability, speed and extensibility.
図1に示すように、我々のシステムアーキテクチャはPythonで実装されており、スケーラビリティ、スピード、拡張性という我々の目標を達成するために設計されています。
The first point of interaction with Plista is NGINX, a load balancing HTTP server, which filters and redirects the different types of Plista messages to individual python processes (using the Tornado framework, one for each different types of message).
Plistaとの最初のやり取りは、ロードバランシングHTTPサーバーであるNGINXで行われ、異なるタイプのPristaメッセージをフィルタリングして個々のPythonプロセス（Tornadoフレームワークを使用、異なるタイプのメッセージごとに1つ）にリダイレクトする。
All Tornado servers write to a permanent archive database, for which we use MongoDB.
Tornadoサーバーはすべて、MongoDBを使用した永続的なアーカイブデータベースに書き込んでいます。
In order to make content-based recommendations we use an ElasticSearch instance, which keeps only data that is relevant to recommendable news articles, (articles often expire after a few days and get flagged as unavailable for recommendation).
コンテンツに基づく推薦を行うために、ElasticSearchのインスタンスを使用しています。このインスタンスは、推薦可能なニュース記事に関連するデータのみを保持します（記事は数日後に期限切れとなり、推薦不可能なものとしてフラグが立つことがよくあります）。
Rather than trying to guarantee accurate recommendations in under 100ms, we precompute the recommendations and store them in a Redis instance.
また、100ミリ秒以内の正確なレコメンデーションを保証するのではなく、レコメンデーションを事前に計算し、Redisインスタンスに保存しています。
For each of our recommendation algorithms, we have a long running process which continually reads the latest events and articles from the database to build its recommendations.
各レコメンデーションアルゴリズムでは、データベースから最新のイベントや記事を継続的に読み込んで、レコメンデーションを構築するプロセスを長時間実行します。
With this offline approach, there is a danger that we might send back a recommendation for an article which has expired during the time it took to compute the recommendations.
このオフラインのアプローチでは、レコメンデーションを計算する間に期限切れになった記事に対するレコメンデーションを送り返してしまう危険性があります。
To deal with this possibility, we refresh our recommendations in the background as frequently as possible so that our recommendations have a minimal lag.
この可能性に対処するため、私たちはバックグラウンドで可能な限り頻繁に推薦文を更新し、推薦文の遅延を最小限に抑えています。
A typical refresh time for the most demanding recommenders (usually the content-based ones) is less than 5 minutes.
最も要求の厳しいレコメンダー（通常はコンテンツベースのレコメンダー）の典型的な更新時間は5分未満です。
We have constructed the system with a goal of compromising between accuracy or freshness and scalability.
私たちは、精度または鮮度とスケーラビリティの間で妥協することを目標にシステムを構築しています。
Our architecture is capable of sending recommendations back to Plista with a typical response time of about 3ms.
我々のアーキテクチャは、典型的な応答時間約3msでレコメンデーションをPristaに送り返すことが可能です。
We can easily scale it to handle many different algorithms for testing and evaluation purposes.
テストや評価のために、多くの異なるアルゴリズムを扱えるように簡単に拡張することができます。

# Recommendation Algorithms レコメンデーションアルゴリズム

In this section we describe our recommender algorithms.
このセクションでは、我々のレコメンダーアルゴリズムを説明する。
For each we describe the algorithm by how it selects the candidate set i.e. the larger set of items that will be considered for recommendation, and its ranking strategy, i.e. how it ranks the candidate items for recommendation, before returning the top-N to the user.
それぞれのアルゴリズムについて、候補セット、つまり推薦のために考慮されるアイテムの大きなセットをどのように選択するか、そして、ランキング戦略、つまり推薦のための候補アイテムをどのようにランク付けし、上位N位をユーザーに返すかについて説明する。
We refer to the target user as the user for whom the recommendations are required, and the current article as the news article the user is currently reading.
また、推薦を必要とするユーザーを「ターゲットユーザー」、ユーザーが現在読んでいる記事を「カレントアーティクル」と呼ぶ。
We have implemented sixteen recommenders in total: six popularity-based recommender, seven content-based recommenders, a feedback-based recommender, a recencybased recommender and an ensemble recommender.
我々は、6つの人気度ベース推薦器、7つの内容ベース推薦器、フィードバックベース推薦器、再帰性ベース推薦器、アンサンブル推薦器の計16の推薦器を実装した。
Before returning the top-N recommendations to the user, we apply three basic filters to the candidate set:
上位N個の推薦文をユーザに返す前に、3つの基本的なフィルタを候補集合に適用する。

- Exclude items from other domains: Recommendations must come from the same domain as the current article; we do not consider cross-domain recommendations although this is something we would like to investigate in the future, once we have an understanding of how single-domain recommenders work in this space. 他のドメインからのアイテムを除外する。 クロスドメイン・レコメンデーションは考慮しませんが、将来、単一ドメインのレコメンダーがこの領域でどのように機能するかを理解した上で、調査したいと思います。

- Exclude already read articles: We do not make recommendations of articles we know the target user has already read, however we do allow previously recommended articles to be re-recommended if the user did not click on the recommendation the first time. As always, it’s hard to interpret non-clicks in recommender systems; a more mature model might limit the number of times the same recommendation is ultimately shown to a user. 既読の記事を除外する。 ターゲットユーザーが既に読んだことがあるとわかっている記事は推薦しません。しかし、ユーザーが最初に推薦をクリックしなかった場合は、以前に推薦した記事を再推薦することを許可しています。 より成熟したレコメンデーションシステムでは、同じレコメンデーションを何度も表示することを制限するかもしれません。

- Exclude non-recommendable items: These are items that are flagged as nonrecommendable (usually older articles) by Plista. 非推奨のアイテムを除外する。 Plistaで非推奨とされたアイテム（通常は古い記事）です。

Each of the six popularity recommenders rank their candidate set by item popularity, i.e. the number of users who have read an article.
6つの人気レコメンダーはそれぞれ、アイテムの人気度、すなわち、ある記事を読んだことのあるユーザーの数によって候補セットをランク付けしている。
However, they differ in the way they compile their candidate sets.
しかし、候補集合の作成方法はそれぞれ異なる。
We have developed a basic as well as more advanced recommenders that use additional features.
我々は、基本的なレコメンダーと、さらに機能を追加した上級レコメンダーを開発した。
They can be described as follows:
その特徴は以下の通りである。

- Popularity - Basic: The candidate set is all items in the dataset. 人気度 - 基本: 候補セットはデータセット内のすべてのアイテムである。

- Popularity - Geolocation: The candidate set is all items that have been read by users in the same geographical location as the target user. 人気度 - 地理的位置。 候補セットは、ターゲットユーザーと同じ地理的位置にいるユーザーに読まれたことのあるすべてのアイテムである。

- Popularity - Item Categories: Every item is associated with zero or more news categories (business, sports, politics, etc.). The candidate set is all items whose categories intersect with the target article’s categories. 人気 - アイテムカテゴリ: すべてのアイテムは0以上のニュースカテゴリ（ビジネス、スポーツ、政治など）と関連付けられている。 候補セットは、カテゴリがターゲット記事のカテゴリと交差するすべてのアイテムである。

- Popularity - Weekday: The candidate set is all items that have been seen at least once in the same week day as the target article. 人気度 - 平日。 対象記事と同じ曜日に一度でも見られたことがあるものを候補とする。

- Popularity - Hour: The candidate set is all items that have been seen at least once in the same hour as the target article. 人気度 - 時間: 候補セットは、対象記事と同じ時間に一度でも見られたことがあるすべての項目である。

- Popularity - Freshness: The candidate set is all articles that have been published or updated in the last 24 hours. 人気度 - 鮮度。 候補セットは、過去24時間以内に公開または更新されたすべての記事である。

Similar to the Lucene-based recommender described in [2], the group of content-based recommenders recommend articles that are similar to the current article.
2]で説明した Lucene ベースのレコメンダーと同様に、コンテンツベースのレコメンダーのグループは、現在の記事に類似した記事を推薦する。
The intention here is not to present the user with an article essentially the same as the current one, something which would of course be undesirable, but rather to find articles that are strongly related to the current article.
ここでの意図は、現在の記事と本質的に同じ記事をユーザーに提示することではなく、もちろん望ましくないことだが、むしろ現在の記事と強く関連する記事を見つけることである。
We believe that in the case of news stories that evolve over a period of days or even weeks such as the recent disappearance of the Malaysia Airlines flight MH370, such recommendations would be especially desirable, as new facets of the story unfold and change.
最近のマレーシア航空MH370便の失踪事件のように、数日から数週間にわたって展開されるニュースの場合、ストーリーの新しい側面が展開され変化するにつれて、このような推奨が特に望ましいと考えられる。

Each of the content-based recommenders we deploy use the conventional TFIDF vector space model[18] to derive the candidate set.
私たちが導入したコンテンツベースレコメンダーは、それぞれ従来のTFIDFベクトル空間モデル[18]を用いて候補セットを導出するものである。
However, each algorithm uses a different selection of content within an article over which to apply the model.
しかし、各アルゴリズムは、モデルを適用するために、記事内のコンテンツの異なる選択を使用します。
For each of the following content-based recommenders, the candidate set is always ranked in decreasing order of similarity to the current article.
以下の各コンテンツベースレコメンダーでは、候補セットは常に現在の記事との類似度の降順にランク付けされる。

- Content - Title and Summary: The candidate set is all articles, represented by the terms in their titles and summaries. 内容 - タイトルと要約：候補セットは、タイトルと要約に含まれる用語で表されるすべての記事である。

- Content - Title and Summary + Freshness: As above, but candidate set articles must also be fresh i.e. published or updated in the last 24 hours. 内容 - タイトルと概要 + 新鮮さ。 上記と同様ですが、候補となるセット記事は、過去24時間以内に公開または更新された新鮮なものである必要があります。

- Content - Title and Summary + New: As above but candidate set articles must be brand new i.e. published in the last hour, rather than fresh. コンテンツ - タイトルと概要＋新規。 上記と同様ですが、候補となるセット記事は、新しいものではなく、直近1時間以内に公開されたものでなければなりません。

- Content - Keywords: The candidate set is all articles, represented by their keywords provided by Plista (recall that Plista provides a set of keywords and their frequencies within a document, although how the keywords are selected, or what they actually are is not disclosed). 内容 - キーワード 候補セットは、Pristaが提供するキーワードで表されるすべての記事である（Pristaは、キーワードのセットと文書内の頻度を提供するが、キーワードがどのように選択され、実際に何であるかは開示されていないことを思い出してください）。

- Content - German Entities: The candidate set is all articles, represented by their entities; using AlchemyAPI we extract entities, in German, from the full text of the articles. コンテンツ - ドイツ語のエンティティ。 候補セットは、エンティティで表されるすべての記事です。AlchemyAPIを使用して、記事のフルテキストからドイツ語のエンティティを抽出します。

- Content - English Entities: The candidate set is all articles, represented by their entities. This time, we use Google Translate to first translate the articles into English and then use OpenCalais to extract entities from the full text of the articles. 内容 - 英語のエンティティ。 候補セットは、エンティティで表されるすべての記事です。 今回は、まずGoogle翻訳で記事を英語に翻訳し、OpenCalaisで記事の全文からエンティティを抽出する。

- Content - English Entities in Context: Expanding on the previous recommender, we represent articles using both their entities and the context surrounding them in the article. In OpenCalais context represents the relevant text before and after an entity. コンテンツ - 英語のエンティティをコンテキストで表現。 前のレコメンダーを発展させ、記事中の実体とそれを取り巻くコンテキストの両方を用いて記事を表現する。 OpenCalaisでは、コンテキストはエンティティの前後の関連テキストを表します。

- Positive Implicit Feedback: The candidate set is all articles that have been successfully recommended in the past (by any team’s algorithm) to some user, i.e. clicked by the user. The more popular an article is as a recommendation, i.e. the more clicks it has, the higher the algorithm ranks it. 肯定的な暗黙のフィードバック 候補セットは、過去に（どのチームのアルゴリズムによっても）あるユーザーにうまく推薦された、つまり、ユーザーによってクリックされたすべての記事である。 ある記事が推薦として人気があればあるほど、つまりクリック数が多ければ多いほど、アルゴリズムはその記事を上位にランク付けする。

- Most Recent: The candidate set is all articles in the dataset. Candidate articles are then ranked in reverse chronological order of when they were published or updated. 最も新しいもの。 候補セットは、データセット内のすべての記事である。 そして、候補となった記事は、公開または更新された時期の逆年代順でランク付けされる。

- Ensemble: Recommendations are produced based on a combination of all the popularity- and content-based recommenders above. The candidate set is the union of candidate sets from each recommender. Candidate articles are then ranked using the sum of the rankings for the top n articles from each recommender. If, for any recommender, an article does not occur in the top n recommendations, it receives the maximum ranking of n, plus a penalty of 1, as in equation 1. We set n = 100 in these experiments. アンサンブル。 レコメンデーションは、上記の人気ベースおよびコンテンツベースのレコメンダーすべての組み合わせに基づいて生成される。 候補セットは、各レコメンダーからの候補セットの和となる。 そして、各レコメンダーからの上位 n 個の記事の順位の合計を使って、候補の記事がランク付けされる。 もし、ある記事がレコメンダーの上位 n 件のレコメンデーションに含まれない場合は、式 1 のように、n の最大ランキングに 1 のペナルティを加えたものを受け取る。 この実験では n = 100 とした．

$$
\tag{1}
$$

# Analysis and Evaluation 分析・評価

In this section we give a brief overview of the data we receive from Plista, in order to better understand the performance of our recommender algorithms.
このセクションでは、我々のレコメンダーアルゴリズムのパフォーマンスをよりよく理解するために、Pristaから受け取ったデータの簡単な概要を説明する。
We will finish with a discussion on possible evaluation methods.
最後に、可能な評価方法について議論する。

## Dataset Overview データセットの概要

To illustrate the nature and dynamic quality of the data and how it informs our choice of recommender algorithms, we look closely at a one week sample, between Wed, 25 May ’14 and Tue, 30 Jun ’14.
データの性質と動的な品質、そしてそれがどのようにレコメンダーアルゴリズムの選択に影響を与えるかを説明するために、14年5月25日（水）から14年6月30日（火）までの1週間のサンプルを詳細に見てみましょう。
During this time period we observe 11 websites.
この期間に、11のウェブサイトを観察しました。
They range from domain-specific news e.g. sport, (sport1.de) to more general news (tagesspiegel.de) to online home and gardening stores (wohnen-undgarten.de).
これらのウェブサイトは、スポーツなどの特定分野のニュース（sport1.de）から、より一般的なニュース（tagesspiegel.de）、オンライン家庭園芸店（wohnen-undgarten.de）まで多岐にわたっています。
There were approximately 8 million visits from 1.75 million unique users to 400 thousand unique articles published.
175万人のユニークユーザーによる約800万回の訪問があり、40万件のユニークな記事が公開されました。
The mean number of observed articles per user is approximately 4, and the data sparsity is 99.99%.
1ユーザーあたりの平均観測記事数は約4、データのスパース性は99.99%である。
Over 90% of the traffic generated cumulatively from the websites is event notifications (impressions and clicks).
ウェブサイトから累積で発生したトラフィックの90%以上はイベント通知（インプレッションとクリック）である。
This traffic is unevenly distributed across the domains, with sport1.de contributing almost 40% and together with ksta.de and channelpartner.de over 80% of all traffic.
このトラフィックはドメインに偏在しており、sport1.deが40%近く、ksta.deとchannelpartner.deと合わせて80%以上のトラフィックに貢献しています。
We find that most of the users that visit tagesspiegel.de also visit most of the rest of the websites, indicating the broad appeal of this domain.
tagesspiegel.deを訪問したユーザーのほとんどが、他のウェブサイトも訪問していることがわかり、このドメインが広くアピールしていることがうかがえます。
Surprisingly enough, there is a noticeable overlap between users of sport1.de (sports website) and wohnen-und-garten.de (online home and gardening store).
意外なことに、sport1.de（スポーツサイト）とwohnen-und-garten.de（家庭・園芸用オンラインショップ）のユーザーには、顕著な重複が見られます。
On the other hand, users who frequent motor-talk.de rarely visit any of other websites.
一方、motor-talk.deをよく利用するユーザーは、他のウェブサイトをほとんど利用しない。
The uneven patterns of cross-domain traffic are certainly interesting, but for simplicity we have restricted our algorithms to only make recommendations in the same top-level domain for this work.
このようなクロスドメイン・トラフィックの不均一なパターンは確かに興味深いものですが、今回は簡略化のため、同一トップレベルドメイン内でのみ推薦を行うようアルゴリズムを限定しています。

## Evaluation 評価

We show the average and maximum CTR results as reported by Plista in Fig. 2, and we compare the CTR with our algorithms in Table 1.
Plistaが報告した平均CTRと最大CTRの結果を図2に示し、我々のアルゴリズムとCTRを比較した結果を表1に示す。
We also show the precision results from an offline evaluation we additionally performed, as we discuss later in this section.
また、このセクションで後述するように、我々が追加で行ったオフライン評価による精度結果も示しています。
With the objective of testing many algorithms the final averaged CTR < 1% is not particularly competitive.
多くのアルゴリズムをテストする目的で、最終的に平均化されたCTR < 1%は、特に競争力があるわけではありません。
We can also see that there is a noticable difference between the average and maximum CTR.
また、平均と最大のCTRの間に顕著な差があることがわかります。
This could be due to a number of reasons including network congestion, server overload and change in algorithm performance based on features such as the domain, time of the day, user geolocation, etc.
これは、ネットワークの混雑、サーバーの過負荷、およびドメイン、時間帯、ユーザーの地理的位置などの特徴に基づくアルゴリズム性能の変化など、多くの理由による可能性があります。
In future work we plan to get a better understanding of the specifics of the problem and bring the average CTR closer to the maximum.
将来的には、問題の詳細をより深く理解し、平均CTRを最大値に近づけることを計画しています。
In contrast, the scalability of our architecture is apparent in the high number of requests that we were able to respond to.
一方、我々のアーキテクチャのスケーラビリティは、対応可能なリクエスト数の多さに現れています。
We show the distribution of article popularity in Fig. 3(a).
図 3(a)に記事の人気度分布を示す。
Although, most articles have very low popularity among users, there are plenty with higher popularities suggesting that popularity-based recommenders should perform comparatively well and that is what we find - three of the top five of our recommenders are popularity-based.
ほとんどの記事はユーザーからの人気が低いが、高い人気も多く、人気度ベースのレコメンダーは比較的良いパフォーマンスを示すはずであることを示唆しており、我々のレコメンダーの上位5つのうち3つが人気度ベースであることが分かった。

Table 1: Average, max and precision of algorithms
表1: アルゴリズムの平均値、最大値、精度

Fig. 2: Average CTR (orange
図2：平均CTR（オレンジ

The complex dynamics of the news cycle are apparent in the relative performances of our popularity recommendations based on different timeframes.
ニュースサイクルの複雑なダイナミクスは、異なるタイムフレームに基づく人気記事推薦の相対的なパフォーマンスにも表れている。
We find better performance recommending articles that are popular over the course of a day compared to the course of an hour, indicating particular daily cycles in users’ news consumption.
これは、ユーザーのニュース消費における特定の日周期の存在を示している。
It will be interesting to examine further the optimal timeframe over which recommendations should be made, and how this varies across each domain.
今後、どのような時間枠で推薦を行うのが最適なのか、また、ドメインによってどのような違いがあるのか、さらに検証していく予定である。
Our popularity recommendations based on geographic location of the user (see Fig. 3(b)), also performed well, and this highlights the importance of accounting for local and spatial contexts in news recommendations.
また、ユーザーの地理的な位置情報に基づいた人気記事推薦（図3（b）参照）も良好な結果を示し、ニュース推薦においてローカルおよび空間的なコンテキストを考慮することの重要性が浮き彫りになっている。
Similar performance is found with category-based recommendations.
また、カテゴリに基づく推薦でも同様の結果が得られている。
Our intuitive understanding is that users tend to read news from the same category, and to further test this idea we looked at a transition matrix for user clicks from category to category in a single domain Fig. 4 (we chose the news domain ksta.de).
私たちの直感的な理解では、ユーザーは同じカテゴリのニュースを読む傾向があります。この考えをさらに検証するために、図4は、単一のドメインにおけるカテゴリからカテゴリへのユーザーのクリックの遷移行列を見ています（ニュースドメインksta.deを選択しました）。
We clearly see just a few dominant categories and clicks between these categories account for the vast majority of items that are read.
図4（ksta.de）を見ると、明らかにいくつかのカテゴリーが支配的で、これらのカテゴリー間のクリックが読まれるアイテムの大部分を占めていることがわかります。
However, it is clear that there are important patterns of activity between certain less popular categories and future recommender algorithms will attempt to exploit these.
しかし、人気のないカテゴリー間にも重要な活動パターンがあることは明らかであり、将来のレコメンダーアルゴリズムはこれらを利用することを試みるだろう。
The strong correlations in the click-transitions of a domain’s categories suggests that content based recommenders are likely to have some success.
ドメインのカテゴリのクリック遷移に強い相関があることから、コンテンツベースのレコメンダーがある程度成功する可能性があることが示唆されます。
We find high CTR for our content-based algorithms Content - Title and Summary, although the best performing variant is one which returns fresh recommendations.
コンテンツベースのアルゴリズムでは、Content - Title と Summary が高い CTR を示していますが、最もパフォーマンスが高いのは、新鮮なレコメンデーションを返すものです。
While users seem to express some degree of preference for articles that are similar, the behaviour is very different across domains and also changes over time.
ユーザーはある程度似たような記事を好むようですが、その行動はドメインによって大きく異なり、また時間によっても変化します。
Content-based recommenders have shown to be quite successful in the past.
コンテンツベースのレコメンダーは過去にかなりの成功を収めていることが示されている。
Our Content - Title and Summary recommenders perform among the best of our algorithms.
私たちのコンテンツ - タイトルと要約レコメンダーは、私たちのアルゴリズムの中で最高のパフォーマンスを見せています。
This shows that users enjoy articles that are related to the target article.
これは、ユーザーがターゲット記事に関連する記事を楽しんでいることを示しています。
The best performing variant is one which returns fresh recommendations.
最もパフォーマンスの良いバリエーションは、新鮮なレコメンデーションを返すものです。
Alchemy and OpenCalais are entity extraction services which tag text and use linked data sources to identify entities in text such as people, companies, etc., and relationships between entities.
Alchemy と OpenCalais は、テキストにタグ付けし、リンクされたデータソースを使用して、人、会社などのテキスト内のエンティティや、エンティティ間の関係を識別するエンティティ抽出サービスです。
While each service returns largely similar results, there are differences which can be significant (noticeable gaps in knowledge about non-English entities).
各サービスはほぼ同様の結果を返しますが、大きな違いもあります（英語以外のエンティティに関する知識のギャップが顕著に見られます）。
The resulting recommendations achieve comparatively good scores, although it should be noted that for technical reasons we did not run all of our entity recommenders for the entire duration of the competition.
技術的な理由により、すべてのレコメンダーがコンペティションの全期間にわたって稼働したわけではありませんが、結果として得られたレコメンデーションは比較的良いスコアを獲得しています。
Based on the maximum CTR they achieved (2.44%) we expect to look more closely at tuning these algorithms for further use.
最大CTR（2.44%）を達成したことから、これらのアルゴリズムのチューニングをより詳細に検討し、さらに活用することが期待されます。
The fact that the Content - German Entities outperforms Content - English Entities suggests that something is lost during the translation of articles into another language, even with entities which one might expect would be more reliably translated than full text.
Content - German Entities が Content - English Entities を上回ったという事実は、フルテキストよりも確実に翻訳されると期待されるエンティティでさえ、他の言語への記事の翻訳時に何かが失われていることを示唆しています。
We also find that including contextual text that OpenCalais provides reduces recommendation accuracy.
また、OpenCalais が提供する文脈的なテキストを含めると、推薦の精度が低下することもわかりました。
This is likely because this text firstly is not cleaned and contains stopwords, and secondly is likely to be more useful for identifying sentiment associated with entities, rather than more accurately classifying what the article is about.
これは、このテキストが第一にクリーニングされておらず、ストップワードが含まれていること、第二に、記事の内容をより正確に分類するのではなく、実体に関連する感情を特定するために有用である可能性が高いことが理由と思われます。
The Plista competition provides a single evaluation metric - CTR.
Plista のコンペティションは単一の評価指標である CTR を提供します。
There are many possible approaches to evaluation [19], and in order to evaluate our own algorithms we constructed an ‘offline’ testing setup which allows us to ‘rewind’ the dataset to any point in time.
評価には多くのアプローチがありますが [19]、当社独自のアルゴリズムを評価するために、データセットを任意の時点に「巻き戻す」ことができる「オフライン」テストのセットアップを構築しました。
We can then perform our recommendations against the data as if they were live and evaluate the results against the actual clicks that users are observed to perform.
これは、データセットを任意の時点まで「巻き戻す」こと ができる。そして、データに対して、あたかも生きているかのようにレコメン デーションを行い、ユーザーが行った実際のクリックに対して結果を評 価することができるのである。
We use a simple average precision metric for evaluation, assuming that the order of the recommendations is not relevant.
評価には、レコメンデーションの順番は関係ないと仮定し、単純な平均精度の指標を使用しています。
Our offline precision calculation allows us to shed more light on the crudely averaged
オフラインで精度を計算することで、平均化されたレコメンデーションをより明確にすることができます。



(b) Histogram of number of users seen for the top 20 most common geolocations.
(b)最も一般的な上位20の地理的位置のユーザー数のヒストグラム。
We can see that there is a considerable amount of users concentrated at the big German cities, for example almost 2.5 million user could be located at Berlin and over 1.25 million at Munich.
ベルリンに250万人、ミュンヘンに125万人など、ドイツの大都市に多くのユーザーが集中していることがわかります。

Fig. 3 CTR provided by Plista, and provides us with many interesting suggestions for further work to improve our algorithmic techniques and evaluations.
図3 Plistaから提供されたCTRは、我々のアルゴリズム技術と評価を向上させるために、さらなる作業に対する多くの興味深い示唆を与えてくれました。

Fig. 4: Click transition matrix for categories on the ksta.de domain.
Fig.4: ksta.de ドメインのカテゴリに対するクリック遷移行列．
We have excluded the category ids for which there are no click transitions to any other category.
他のカテゴリへのクリック遷移がないカテゴリ ID は除外している。
The colour scale represents the number of click transitions.
カラースケールはクリック遷移の回数を表す。

# Conclusions and Future Work 結論と今後の課題

We have presented our results for the CLEF-NewsREEL 2014 Challenge.
CLEF-NewsREEL 2014チャレンジの結果を発表しました。
We have described our scalable architecture for delivering recommendations and detailed various algorithmic approaches that we have taken.
推薦文を配信するためのスケーラブルなアーキテクチャを説明し、私たちが取った様々なアルゴリズムアプローチを詳述しました。
We have highlighted some of the issues with the dataset which impact on the type of algorithms we can implement.
我々は、我々が実装できるアルゴリズムの種類に影響を与えるデータセットの問題のいくつかを強調しました。
For future work we intend to examine more closely the user features which are most relevant for collaborative filtering approaches.
今後の課題として、協調フィルタリングアプローチに最も関連するユーザーの特徴をより詳細に調査する予定である。
The dynamic click behaviour associated with browsing patterns is a rich area to exploit, and we also intend to improve on our content-based algorithms with better entity detection and similarity measures.
また、コンテンツベースのアルゴリズムを改良し、より優れたエンティティ検出と類似性測定を行う予定です。
