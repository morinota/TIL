refs: https://medium.com/udemy-engineering/building-a-multi-armed-bandit-system-from-the-ground-up-a-recommendations-and-ranking-case-study-8f09f65d26b6


# Building a Multi-Armed Bandit System from the Ground Up: A Recommendations and Ranking Case Study, Part II
地上からマルチアームバンディットシステムを構築する：推薦とランキングのケーススタディ、第II部

Share
共有
Sam Cohan, Principal Machine Learning Engineer at Udemy
サム・コハン、Udemyの主任機械学習エンジニア

# Introduction はじめに

This is Part II of a two-part blog post about how we built a multi-armed bandit (MAB) system for recommendation and ranking use cases at Udemy. 
これは、Udemyでの推薦およびランキングのユースケースのために、マルチアームバンディット（MAB）システムをどのように構築したかについての二部構成のブログ投稿のパートIIです。
In Part I, we covered the theoretical and practical data science details for such a system. 
パートIでは、そのようなシステムの理論的および実践的なデータサイエンスの詳細について説明しました。
In this second and final part, we will provide an overview of our production architecture and development environment, 
この第二部および最終部では、**私たちのプロダクションアーキテクチャと開発環境の概要**を提供し、
and discuss the engineering challenges that teams may face when deploying a similar system. 
**類似のシステムを展開する際にチームが直面する可能性のあるエンジニアリングの課題**について議論します。

<!-- ここまで読んだ! -->

# Overview of System Architecture システムアーキテクチャの概要

The high-level architecture of the multi-armed bandit system for recommendations is represented in the diagram below. 
推薦のためのマルチアームバンディットシステムの高レベルアーキテクチャは、以下の図に示されています。
Note that as the red dotted arrows show, it is anear real-time closed loop system, meaning user feedback is continuously being used to improve the recommendations. 
赤い点線の矢印が示すように、これは**ほぼリアルタイムの閉ループシステム**であり、ユーザーフィードバックが継続的に使用されて推薦を改善しています。

![]()

Let’s look more closely at this loop and explain how it works and what components are involved. 
このループをより詳しく見て、どのように機能し、どのようなコンポーネントが関与しているのかを説明しましょう。

<!-- ここまで読んだ! -->

## 1. User interacts with Udemy ユーザがUdemyと対話する

The loop begins when a user interacts with the Udemy website or mobile app. 
ループは、ユーザがUdemyのウェブサイトまたはモバイルアプリと対話する際に始まります。
As the requested page is being loaded, the current best recommendations are loaded from Redis and served to the user. 
リクエストされたページが読み込まれる際、**現在の最良の推薦がRedisから読み込まれ、ユーザに提供されます**。(あ、バッチ推論じゃん!:thinking:)
We will later explain how these recommendations are kept up to date. 
これらの推薦がどのように最新の状態に保たれているかについては、後で説明します。

## 2. Events are generated and published to Kafka イベントの生成とKafkaへの公開

As UI elements are loaded and interacted with, events are generated (both from frontend and backend systems) and sent to the Eventing System. 
UI要素が読み込まれ、操作されると、イベントが生成され（フロントエンドとバックエンドの両方のシステムから）、**Eventing System**に送信されます。 
These events have tracking IDs, which allow them to be stitched together into funnel events, meaning you can know whether a UI element was viewed, was clicked on or led to an interesting downstream event like a course enrollment or lecture view (i.e., rewards). 
これらのイベントには**トラッキングIDがあり、それによりファネルイベントにまとめることができ**、UI要素が表示されたか、クリックされたか、またはコース登録や講義の視聴（つまり、報酬）などの興味深い下流イベントにつながったかを知ることができます。 
(なるほど、Udemyさんの場合はこの共通のTrackingIDでアームプレイログと報酬ログを紐づけているっぽい...!:thinking:)
The tracking system ensures the schema and consistency of the events is maintained across time and that they are reliably published to Kafka topics to be consumed by downstream systems. 
トラッキングシステムは、イベントのスキーマと一貫性が時間を通じて維持され、下流システムによって消費されるためにKafkaトピックに信頼性を持って公開されることを保証します。

## 3. Streaming apps create observations from the events 

(イベントログから報酬観測値を作るストリーミングパイプライン的なやつ...!:thinking:)

There are two Spark Structured Streaming applications dedicated to creating observations (a.k.a., rewards) from the Kafka events. 
Kafkaイベントから観測（別名、報酬）を作成するために特化した **2つのSpark Structured Streamingアプリケーション**があります。
The first app is the Funnel Join App, and as the name indicates, it performs a streaming join to create joined events (a.k.a., funnel events), which combine impressions, clicks and downstream events like enrollments to answer the question, “Did showing a recommendation lead to a reward in a fixed amount of time?” 
最初のアプリはFunnel Join Appで、名前が示すように、ストリーミングジョインを実行して、**インプレッション、クリック、エンロールメントなどの下流イベントを組み合わせた結合イベント（別名、ファネルイベント）を作成し、「推薦を表示することは、一定の時間内に報酬につながったか？」という質問に答えます**。

These joined events are published back to Kafka and consumed by a second Spark Structured Streaming application called the Observation App. 
これらの結合イベントはKafkaに再公開され、Observation Appと呼ばれる2つ目のSpark Structured Streamingアプリケーションによって消費されます。
The job of the Observation App is to apply sessionization logic to the joined events to create the final observations. 
**Observation Appの仕事は、結合済みeventsにセッション化ロジックを適用して最終的な観測を作成すること**です。
This app makes use of Spark’s stateful stream processing and writes the observations to a new topic on Kafka to be consumed by the Bandit Model Apps. 
このアプリはSparkの状態を持つストリーム処理を利用し、観測をKafkaの新しいトピックに書き込み、Bandit Model Appsによって消費されるようにします。
(2つのfiliterを持つ一個のパイプラインにまとめちゃえそうかな...!

<!-- ここまで読んだ-->

## 4. Bandit model apps use the observations to update recommendations and refresh Redis

The final set of Spark Streaming Applications are the Bandit Model Apps. 
最終的なSpark Streamingアプリケーションのセットは、Bandit Model Appsです。

We designed these apps to support several bandit algorithms, but in practice, we saw that the Thompson Sampling algorithm was the one that produced the best results. 
これらのアプリは、いくつかのバンディットアルゴリズムをサポートするように設計しましたが、実際にはThompson Samplingアルゴリズムが最も良い結果を生み出すことがわかりました。

These apps consume observations from Kafka in micro batches, update the arm reward probabilities and update the resulting recommendations in Redis. 
これらのアプリは、Kafkaからマイクロバッチで観測データを取得し、アームの報酬確率を更新し、Redisに結果の推薦を更新します。

Also note these apps log all of their intermediate states to a database so they can be used for offline analysis later. 
また、これらのアプリはすべての中間状態をデータベースにログとして記録するため、後でオフライン分析に使用できます。

And thus, the full cycle is complete. 
これにより、完全なサイクルが完了します。



## Candidate Generation Workflow 候補生成ワークフロー

You might be wondering how the bandit model apps know what candidates (a.k.a., arms) to consider for the recommendation use case. 
バンディットモデルアプリが推薦のユースケースに対してどの候補（別名、アーム）を考慮すべきかをどのように知っているのか疑問に思うかもしれません。

Well, that’s done via a Candidate Generation Workflow, which checks some configuration tables to grab a list of possible UI elements and their source pages. 
それは、候補生成ワークフローを通じて行われ、いくつかの設定テーブルをチェックして、可能なUI要素とそのソースページのリストを取得します。

These UI elements can be courses, carousels of courses, etc. 
これらのUI要素は、コースやコースのカルーセルなどです。

The workflow is scheduled to run nightly to refresh the arm set, but the system is designed to be robust enough that the refresh can happen in an ad-hoc manner any time. 
このワークフローは、アームセットを更新するために毎晩実行されるようにスケジュールされていますが、システムは十分に堅牢に設計されているため、いつでもアドホックに更新が行われることができます。



## Monitoring, Alerting and Supervision 監視、アラート、監督

To make sure the multi-armed bandit recommendation system remains in a healthy state around the clock, we built a real-time dashboard of vital metrics such as count of records written to each Kafka topic and Redis writes and Redis read latencies. 
マルチアームバンディット推薦システムが24時間健康な状態を維持するために、各Kafkaトピックに書き込まれたレコードの数やRedisの書き込みおよび読み取り遅延などの重要なメトリクスのリアルタイムダッシュボードを構築しました。

We defined monitors on top of these metrics and hooked the alerting to Slack and apaging solution. 
これらのメトリクスの上にモニターを定義し、アラートをSlackおよびpagingソリューションに接続しました。

In addition, we have a supervisor job that is scheduled to check the status of the streaming application every five minutes and restart them if they have failed or are in a bad state. 
さらに、ストリーミングアプリケーションの状態を5分ごとにチェックし、失敗した場合や不良状態の場合には再起動するようにスケジュールされた監視ジョブがあります。



# Engineering Challenges エンジニアリングの課題  
## Learning Curve of Developing Real Time Systems リアルタイムシステム開発の学習曲線
One of the most significant engineering challenges for this project was overcoming the steep learning curve of the involved technologies. 
このプロジェクトにおける最も重要なエンジニアリングの課題の一つは、関与する技術の急な学習曲線を克服することでした。 
Things become an order of magnitude more difficult to think about when you go from batch to real-time systems. 
バッチシステムからリアルタイムシステムに移行すると、考えることが一桁難しくなります。 
Specifically, if you are from a Python background and do not have extensive experience with the JRE universe, the tooling alone takes some time to get familiarized with. 
特に、Pythonのバックグラウンドを持ち、JREの世界に関する広範な経験がない場合、ツールに慣れるだけでも時間がかかります。 
On top, you have to deal with the idiosyncrasies of Scala (a strongly typed functional language) and Spark Structure Streaming (a streaming framework with often long and cryptic error messages). 
さらに、Scala（強く型付けされた関数型言語）やSpark Structure Streaming（しばしば長くて難解なエラーメッセージを持つストリーミングフレームワーク）の特異性にも対処しなければなりません。 
In addition to the challenges resulting from language and frameworks, the very nature of streaming applications poses its own unique challenges for development and testing. 
言語やフレームワークから生じる課題に加えて、ストリーミングアプリケーションの本質自体が開発とテストに独自の課題をもたらします。 
It is important to invest in tooling and environments that can help increase your speed of development. 
開発のスピードを向上させるために、ツールや環境に投資することが重要です。 
For example, you may want to consider how to have a minimal end-to-end system on your local machine to be able to quickly iterate on and test your code (hint: containerization is your friend). 
例えば、ローカルマシン上で最小限のエンドツーエンドシステムを持ち、迅速にコードを反復しテストできる方法を考慮することが望ましいでしょう（ヒント：コンテナ化はあなたの友人です）。 
The full details of these efforts are out of the scope of this article, but needless to say, this is a pretty significant effort that should not be underestimated. 
これらの取り組みの詳細はこの記事の範囲外ですが、言うまでもなく、これは過小評価すべきではないかなり重要な努力です。 



## Maintaining Uptime and Support Efforts 稼働時間の維持とサポートの取り組み

One of the main differences between batch applications and streaming ones is that streaming applications have to reliably run around the clock and are more susceptible to subtle bugs which can compound over time and cause the application to crash. 
バッチアプリケーションとストリーミングアプリケーションの主な違いの一つは、ストリーミングアプリケーションは24時間安定して稼働しなければならず、時間の経過とともに蓄積される微妙なバグに対してより脆弱であり、アプリケーションがクラッシュする原因となることです。

This is challenging because it requires dedicated on-call support who can be paged at anytime — day or night, holiday or not. 
これは、昼夜を問わず、休日であってもいつでも呼び出せる専任のオンコールサポートが必要であるため、困難です。

Of course, having good visibility into the health of the applications via extensive dashboards that monitor various metrics, and having decent alerting and on-call schedule are table-stakes for launching such a product. 
もちろん、さまざまなメトリクスを監視する広範なダッシュボードを通じてアプリケーションの健康状態を把握し、適切なアラートとオンコールスケジュールを持つことは、そのような製品を立ち上げるための基本条件です。

But the key to successfully supporting such a product without driving the support engineers insane is to design your applications with the assumption that they will inevitably go down, and so you must handle restarts gracefully— and ideally automate them. 
しかし、サポートエンジニアを疲弊させることなくそのような製品を成功裏にサポートするための鍵は、アプリケーションが必然的にダウンするという前提で設計し、再起動を優雅に処理し、理想的には自動化することです。

Of course, Spark has a built-in checkpointing system, which should in theory help with the graceful restart scenario. 
もちろん、Sparkには組み込みのチェックポイントシステムがあり、理論的には優雅な再起動シナリオに役立つはずです。

However, in our experience, it is not uncommon for checkpoints to become corrupt and prevent the application from restarting. 
しかし、私たちの経験では、チェックポイントが破損し、アプリケーションの再起動を妨げることは珍しくありません。

So, to avoid data loss, you must have application logic that can recover the state of your streaming application from an external database. 
したがって、データ損失を避けるためには、外部データベースからストリーミングアプリケーションの状態を回復できるアプリケーションロジックを持つ必要があります。

In our case, we snapshot the bandit arm states and Kafka offsets to an external database, so if the Spark checkpoint is corrupted, we can safely delete it and load the last valid arm states from our backup database. 
私たちの場合、バンディットアームの状態とKafkaオフセットを外部データベースにスナップショットとして保存しているため、Sparkのチェックポイントが破損した場合、安全にそれを削除し、バックアップデータベースから最後の有効なアームの状態をロードできます。

This recovery logic is baked into a supervisor job, so 99 out of 100 times that is good enough to get things going without having to escalate to the on-call engineer. 
この回復ロジックはスーパーバイザージョブに組み込まれているため、100回中99回はオンコールエンジニアにエスカレーションすることなく物事を進めるのに十分です。



# Future Directions 今後の方向性  
## Reward Enhancement 報酬の強化
Currently, we use a weighted sum of clicks and enrollments as the reward function for our multi-armed bandit system. 
現在、私たちはマルチアームバンディットシステムの報酬関数として、クリックと登録の加重和を使用しています。 
We have seen this reward definition has generally correlated well with our desired online A/B test metrics. 
この報酬定義は、私たちが望むオンラインA/Bテストの指標と一般的に良い相関関係があることがわかりました。 
However, there are several modifications of our reward function that we could make to further improve our bandit system’s ability to learn. 
しかし、私たちのバンディットシステムの学習能力をさらに向上させるために、報酬関数のいくつかの修正を行うことができます。

1. Add new rewards such as wishlist and add-to-cart events, which could provide more frequent high-intent signals beyond just enrollments to help MAB differentiate between arms more easily.  
   ウィッシュリストやカートに追加するイベントなどの新しい報酬を追加することで、登録だけでなく、より頻繁に高い意図を持つ信号を提供し、MABがアームをより簡単に区別できるようにします。 
2. Use predicted long-term rewards as an input into the decision-making process to better handle delayed or long-term feedback.  
   遅延または長期的なフィードバックをより適切に処理するために、予測された長期的な報酬を意思決定プロセスの入力として使用します。 
   One way to do this would be to capture short-term signals and use them to predict a long-term metric such as user lifetime value.  
   これを行う一つの方法は、短期的な信号をキャプチャし、それを使用してユーザーのライフタイムバリューのような長期的な指標を予測することです。 
   Then, the bandit could use this predicted reward in the short-term decision-making for which arm to select next.  
   その後、バンディットは次に選択するアームの短期的な意思決定にこの予測された報酬を使用することができます。



## Contextual Bandits 文脈バンディット

In addition to reward enhancements, our main next direction will be to evolve our MAB system into a contextual bandit system. 
報酬の向上に加えて、私たちの次の主要な方向性は、MABシステムを文脈バンディットシステムに進化させることです。 

In a contextual bandit system, every arm-reward pair is now coupled with a context vector. 
文脈バンディットシステムでは、すべてのアーム-報酬ペアは文脈ベクトルと結びつけられます。 

This context vector can include information such as user-specific features, page features, item content and so on. 
この文脈ベクトルには、ユーザー固有の特徴、ページの特徴、アイテムの内容などの情報が含まれる可能性があります。 

By including a context vector, we can personalize the MAB decision-making process. 
文脈ベクトルを含めることで、MABの意思決定プロセスをパーソナライズすることができます。 

MAB’s decision on what and when to explore versus exploit will now be dependent on both the reward history and the context which led to the reward. 
MABが何を探求し、いつ探求するかの決定は、報酬の履歴と報酬をもたらした文脈の両方に依存するようになります。 

In the unit ranking example, instead of having a single dynamically updating global ranking for all users, each user will have a dynamically updating ranking that is specific to them. 
ユニットランキングの例では、すべてのユーザーに対して単一の動的に更新されるグローバルランキングを持つのではなく、各ユーザーには特定の動的に更新されるランキングが与えられます。 

From a systems perspective, there are two main new components required to handle contextual bandits. 
システムの観点から、文脈バンディットを処理するために必要な2つの主要な新しいコンポーネントがあります。 

The first is a Real-time Model Service, which can handle both inference as well as incremental training. 
1つ目は、推論と増分トレーニングの両方を処理できるリアルタイムモデルサービスです。 

The second is a Real-time Feature Service, which can serve the contextual features to the model for inference. 
2つ目は、推論のためにモデルに文脈特徴を提供できるリアルタイムフィーチャーサービスです。 

Note that this is a significantly more challenging setup because whereas before, the predictions were updated in micro batches and served via Redis, now the personalized predictions need to be calculated on the fly as the page is loading (i.e., with sub 50 ms latency). 
これは、以前は予測がマイクロバッチで更新され、Redisを介して提供されていたのに対し、現在はページが読み込まれる際にパーソナライズされた予測をリアルタイムで計算する必要があるため、非常に挑戦的な設定であることに注意してください（すなわち、50 ms未満のレイテンシで）。 

Additionally, the model service is not your typical inference-only model service; it has to also handle model updates without interrupting the inference SLA. 
さらに、モデルサービスは典型的な推論専用のモデルサービスではなく、推論のSLAを中断することなくモデルの更新も処理する必要があります。



# Concluding Remarks 結論

In thistwo-part blog post, we presented a wide range of material covering what multi-armed bandits are, why they are so useful in recommendations applications, how to treat a ranking problem as a bandit problem in a real-life case study and what it takes to build a near real-time, fully productionized MAB system that serves millions of users at a time. 
この二部構成のブログ記事では、マルチアームバンディットが何であるか、なぜ推薦アプリケーションで非常に有用であるのか、実際のケーススタディにおいてランキング問題をバンディット問題として扱う方法、そして数百万のユーザーに同時にサービスを提供するほぼリアルタイムの完全に商用化されたMABシステムを構築するために必要なことについて、幅広い資料を提示しました。

We provided an overview of our architecture, discussed some data science and engineering challenges that can arise when building a MAB system from scratch and shared our thoughts for the future evolution of our system. 
私たちは、アーキテクチャの概要を提供し、MABシステムをゼロから構築する際に発生する可能性のあるデータサイエンスおよびエンジニアリングの課題について議論し、私たちのシステムの将来の進化についての考えを共有しました。

Bandits are a powerful tool with demonstrated success, but they can be particularly challenging to implement successfully in an industry environment, especially in a scalable, near real-time way. 
バンディットは成功が実証された強力なツールですが、特にスケーラブルでほぼリアルタイムの方法で、産業環境で成功裏に実装することは特に困難です。

We hope these blog posts can help others to understand the various challenges that arise in the development of such a system, and serve as a guide and launching point for teams to build their own MAB system from the ground up. 
私たちは、これらのブログ記事が他の人々がそのようなシステムの開発において発生するさまざまな課題を理解するのに役立ち、チームがゼロから自分たちのMABシステムを構築するためのガイドおよび出発点となることを願っています。



## Published in Udemy Tech Blog Udemyテックブログに掲載

Published in Udemy Tech Blog  
Udemyテックブログに掲載

1.3K followers  
1.3Kフォロワー

·  
·

May 29, 2025  
2025年5月29日

Learn about cool projects, product initiatives, and company culture from the data science and engineering teams at Udemy.  
Udemyのデータサイエンスおよびエンジニアリングチームから、クールなプロジェクト、製品イニシアティブ、会社文化について学びましょう。

Find these projects fun? We’re hiring!  
これらのプロジェクトが楽しいと思いますか？私たちは採用しています！ 

https://about.udemy.com/careers/  
https://about.udemy.com/careers/

Follow  
フォロー

Follow  
フォロー

Follow  
フォロー

Follow  
フォロー



## Written by Sam Cohan 著者情報

Written by Sam Cohan
サム・コハンによって書かれました

36 followers
フォロワー数: 36

·
·

Principal ML Engineer at Udemy
Udemyの主任機械学習エンジニア

Follow
フォロー



## No responses yet まだ応答はありません

Write a response 応答を書く
What are your thoughts? あなたの考えは何ですか？
What are your thoughts? あなたの考えは何ですか？
Help ヘルプ
Status ステータス
About この件について
Careers キャリア
Press プレス
Blog ブログ
Privacy プライバシー
Rules ルール
Terms 利用規約
Text to speech テキスト読み上げ
