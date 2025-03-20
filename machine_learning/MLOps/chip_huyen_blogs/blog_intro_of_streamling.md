# Introduction to streaming for data scientists
# データサイエンティストのためのストリーミング入門

Aug 3, 2022•Chip Huyen
2022年8月3日•チップ・フユエン

As machine learning moves towards real-time, streaming technology is becoming increasingly important for data scientists. 
機械学習がリアルタイムに向かうにつれて、ストリーミング技術はデータサイエンティストにとってますます重要になっています。
Like many people coming from a machine learning background, I used to dread streaming. 
**機械学習のバックグラウンドを持つ多くの人々と同様に、私は以前はストリーミングを恐れていました**。
In our recent survey, almost half of the data scientists we asked said they would like to move from batch prediction to online prediction but can’t because streaming is hard, both technically and operationally. 
最近の調査では、**私たちが尋ねたデータサイエンティストのほぼ半数が、バッチ予測からオンライン予測に移行したいと考えているが、技術的にも運用的にもストリーミングが難しいためにできないと答えました**。(気持ちわかる...!!:thinking:)
Phrases that the streaming community take for granted like “time-variant results”, “time travel”, “materialized view” certainly don’t help. 
time-variant results (時間変動結果?)、time travel (タイムトラベル?)、materialized view (マテリアライズドビュー?)など、ストリーミングコミュニティが当然のように使うフレーズは、確かに助けにはなりません。

Over the last year, working with a co-founder who’s super deep into streaming, I’ve learned that streaming can be quite intuitive. 
昨年、ストリーミングに非常に詳しい共同創業者と一緒に働く中で、ストリーミングはかなり直感的であることを学びました。
This post is an attempt to rephrase what I’ve learned. 
**この投稿は、私が学んだことを言い換える試み**です。(この表現いいな...!:thinking:)

With luck, as a data scientist, you shouldn’t have to build or maintain a streaming system yourself.
運が良ければ、データサイエンティストとして、ストリーミングシステムを自分で構築したり維持したりする必要はないはずです。
Your company should have infrastructure to help you with this. 
あなたの会社には、これを支援するためのインフラが整っているはずです。
However, understanding where streaming is useful and why streaming is hard could help you evaluate the right tools and allocate sufficient resources for your needs. 
しかし、**ストリーミングがどこで有用であり、なぜストリーミングが難しいのかを理解すること**で、適切なツールを評価し、ニーズに応じた十分なリソースを割り当てるのに役立つかもしれません。

### Quick recap: historical data vs. streaming data 履歴データvs.ストリーミングデータ

Once your data is stored in files, data lakes, or data warehouses, it becomes historical data. 
**データがファイル、データレイク、またはデータウェアハウスに保存されると、それはhistoricalデータになります。**

Streaming data refers to data that is still flowing through a system, e.g. moving from one microservice to another. 
**ストリーミングデータは、システムを通じてまだ流れているデータ**を指します。例えば、あるマイクロサービスから別のマイクロサービスに移動するデータです。

Batch processing vs. stream processing
バッチ処理とストリーム処理
Historical data is often processed in batch jobs — jobs that are kicked off periodically. 
履歴データは、しばしばバッチジョブで処理されます。バッチジョブとは、定期的に開始されるジョブのことです。
For example, once a day, you might want to kick off a batch job to generate recommendations for all users. 
例えば、1日に1回、すべてのユーザに対する推薦を生成するためにバッチジョブを開始したいかもしれません。
When data is processed in batch jobs, we refer to it as batch processing. 
データがバッチジョブで処理されるとき、私たちはそれをバッチプロセスと呼びます。
Batch processing has been a research subject for many decades, and companies have come up with distributed systems like MapReduce and Spark to process batch data efficiently. 
バッチ処理は何十年にもわたって研究の対象となっており、企業はバッチデータを効率的に処理するためにMapReduceやSparkのような分散システムを考案してきました。

Stream processing refers to doing computation on streaming data. 
**ストリーム処理は、ストリーミングデータに対して計算を行うこと**を指します。
Stream processing is relatively new. 
ストリーム処理は比較的新しい技術です。
We’ll discuss it in this post. 
この投稿では、それについて議論します。

<!-- ここまで読んだ! -->

## 1. Where is streaming useful in machine learning? 機械学習におけるストリーミングの有用性はどこにあるか？

There are three places in the ML production pipeline where streaming can matter a lot: online prediction, real-time observability, and continual learning.
機械学習のプロダクションパイプラインには、**ストリーミングが非常に重要になる3つの場所**があります：オンライン予測、リアルタイム監視、そして継続的学習。

### Online prediction (vs. batch prediction) オンライン予測（バッチ予測との比較）

Batch prediction means periodically generating predictions offline, before prediction requests arise. 
**バッチ予測とは、予測リクエストが発生する前に、定期的にオフラインで予測を生成すること**を意味します。
For example, every 4 hours, Netflix might generate movie recommendations for all of its users. 
例えば、Netflixは4時間ごとにすべてのユーザーに対して映画の推薦を生成するかもしれません。
The recommendations are stored and shown to users whenever they visit the website. 
これらの推薦は保存され、ユーザーがウェブサイトを訪れるたびに表示されます。

Online prediction means generating predictions on-demand, after prediction requests arise. 
**オンライン予測とは、予測リクエストが発生した後に、オンデマンドで予測を生成すること**を意味します。
For example, an ecommerce site might generate product recommendations for a user whenever this user visits the site. 
例えば、eコマースサイトは、ユーザーがサイトを訪れるたびにそのユーザーに対して商品推薦を生成するかもしれません。
Because recommendations are generated online, latency is crucial. 
推薦がオンラインで生成されるため、レイテンシ（遅延）が重要です。

(バッチ推論vsリアルタイム推論という議論が多いが、ストリーミングパイプラインでリクエストとは非同期に予測結果を作る「ニアリアルタイム推論」という分類もありそう...!!:thinking:)

---

Imagine you work for an ecommerce site and want to predict the optimal discount to give a user for a given product to encourage them to buy it. 
あなたがeコマースサイトで働いていて、特定の製品に対してユーザに与える最適な割引を予測して、購入を促したいと想像してみてください。
One of the features you might use is the average price of all the items this user has looked at in the last 30 minutes. 
あなたが使用するかもしれない特徴量の一つは、このユーザーが過去30分間に見たすべての商品の平均価格です。
This is an online feature– it needs to be computed on online data (as opposed to being pre-computed on historical data). 
これはオンライン特徴量であり、オンラインデータ（履歴データで事前に計算されるのではなく）から計算する必要があります。

One “easy” way to do this is to spin up a service like AWS Lambda and Google Cloud Function to compute this feature whenever requests arrive. 
**これを行う「簡単な」方法の一つは、リクエストが到着するたびにこの特徴量を計算する**ためにAWS LambdaやGoogle Cloud Functionのようなサービスを立ち上げることです。
This is how many companies are doing it and it works in many simple cases. 
**多くの企業がこのように行っており、多くの単純なケースでは機能**します。
However, it doesn’t scale if you want to use complex online features. 
**しかし、複雑なオンライン特徴量を使用したい場合、スケールしません**。(うんうん...!:thinking:)

This “easy” way is stateless, which means that each computation is independent from the previous one. 
**この「簡単な」方法はステートレス**であり、各計算が前の計算から独立していることを意味します。
Every time you compute this feature, you have to process all the data from the last 30 minutes, e.g: 
この特徴量を計算するたびに、過去30分間のすべてのデータを処理する必要があります。例えば：

- To compute this feature at 10:33am, you’ll have to process data from 10:03 to 10:33. 
    10:33にこの特徴量を計算するには、10:03から10:33までのデータを処理する必要があります。
- To compute this feature again at 10:35, you’ll have to process data from 10:05 to 10:35. 
    10:35に再度この特徴量を計算するには、10:05から10:35までのデータを処理する必要があります。

The data from 10:05 to 10:33 is processed twice! 
10:05から10:33までのデータは二重に処理されています！

Stream processing can be stateless too, but stateless stream processing is kinda boring, so we’ll only talk about stateful stream processing here. 
ストリーム処理もステートレスにすることができますが、ステートレスストリーム処理は少し退屈なので、ここではステートフルストリーム処理についてのみ話します。
Stateful stream processing can avoid redundancy, hence faster and cheaper. 
**ステートフルストリーム処理は冗長性を回避できるため、より速く、より安価**です。
For example, when computing this feature again at 10:35, you’ll only need to process data from 10:33 to 10:35 and join the new result with the previous result. 
例えば、**10:35に再度この機能を計算する際には、10:33から10:35までのデータのみを処理し、新しい結果を以前の結果と結合するだけで済む**。

<!-- ここまで読んだ! -->

### Real-time monitoring (vs. batch monitoring) リアルタイム監視（バッチ監視との比較）

There’s a world of difference between batch monitoring and real-time monitoring, and many monitoring solutions (especially batch solutions) conflate the two.
バッチ監視とリアルタイム監視には大きな違いがあり、多くの監視ソリューション（特にバッチソリューション）はこの二つを混同しています。

Batch monitoring means running a script to compute the metrics you care about periodically (like once a day), usually on data in warehouses like S3, BigQuery, Snowflake, etc.
**バッチ監視とは、S3、BigQuery、Snowflakeなどのデータウェアハウスにあるデータに対して、気にかけている指標を定期的に（例えば1日1回）計算するためにスクリプトを実行すること**を意味します。
Batch monitoring is slow. You first have to wait for data to arrive at warehouses, then wait for the script to run.
バッチ監視は遅いです。まずデータがウェアハウスに到着するのを待ち、その後スクリプトが実行されるのを待たなければなりません。
If your new model fails upon deployment, you won’t find out at least until the next batch of metrics is computed, assuming the metrics computed are sufficient to uncover the issue.
**新しいモデルがデプロイ時に失敗した場合、次のバッチの指標が計算されるまで少なくともそのことに気づくことはありません**(ちなみにこれは、計算されたmetricsが問題を明らかにするのに十分であると仮定した場合)。
And you can’t fix the failure before you find out about it.
そして、そのことに気づく前に失敗を修正することはできません。

Real-time monitoring means computing metrics on data as it arrives, allowing you to get insights into your systems in (near) real-time.
**リアルタイム監視とは、データが到着する際に指標を計算すること**を意味し、システムに対する洞察を（ほぼ）リアルタイムで得ることを可能にします。
Like online feature computation, real-time metric computation can often be done more efficiently with streaming.
オンライン特徴量の計算と同様に、リアルタイム指標計算はストリーミングを使用することでより効率的に行えることがよくあります。

![]()

If batch monitoring works for you, that’s great.
**バッチ監視があなたにとって機能するのであれば、それは素晴らしいこと**です。
In most use cases, however, batch monitoring often ends up being not enough.
**しかし、ほとんどのユースケースでは、バッチ監視はしばしば不十分であることが多い**です。
In software engineering, we know that the iteration speed is everything – cue Boyd’s Law of Iteration: speed of iteration beats quality of iteration.
**ソフトウェア工学では、イテレーションの速度がすべてである**ことを知っています。[ボイドのイテレーションの法則](https://blog.codinghorror.com/boyds-law-of-iteration/)を思い出してください：**イテレーションの速度はイテレーションの質に勝ります**。
The DevOps community has been obsessed with speeding up iterations for higher quality software for over two decades.
**DevOpsコミュニティは、より高品質なソフトウェアのためにイテレーションを加速することに20年以上も執着**してきました。
Two important metrics in DevOps are:
DevOpsにおける2つの重要な指標は次のとおりです：

- MTTD: mean time to detection
    **不具合や障害が発生してから、それに気づく (検知する) まで**にかかった平均時間のこと。
- MTTR: mean time to response
    **不具合や障害に気づいてから、復旧作業を完了する (あるいは原因特定や対策を実施する) まで**に要する平均時間のこと。

If something is going to fail, you want it to fail fast, and you want to know about it fast, especially before your customers do.
**何かが失敗する場合、迅速に失敗し、そのことを迅速に知りたいと思います。特に顧客よりも前に知りたい**のです。
If your user has to call you in the middle of the night complaining about a failure or worse, tweet about it, you’re likely to lose more than one customer.
もしユーザーが真夜中に失敗について不満を言うためにあなたに電話をかける必要がある場合、あるいはさらに悪いことにそれについてツイートする場合、あなたは1人以上の顧客を失う可能性が高いです。
Yet, most people doing MLOps are still okay with day-long, even week-long feedback loops.
それでも、**MLOpsを行っているほとんどの人々は、1日、さらには1週間のフィードバックループで満足している**。(満足しちゃってるかも...!:thinking:)

Many teams, without any monitoring system in place for ML, want to start with batch monitoring.
MLのための監視システムがない多くのチームは、バッチ監視から始めたいと考えています。
Batch monitoring is still better than no monitoring, and arguably easier to set up than real-time monitoring.
**バッチ監視は監視がないよりはまだ良く、リアルタイム監視よりも設定が簡単である**と言えるでしょう。

However, batch monitoring isn’t a prerequisite for real-time monitoring – setting up batch monitoring today is unlikely to make it easier to set up real-time monitoring later.
**しかし、バッチ監視はリアルタイム監視の前提条件ではありません。今日バッチ監視を設定しても、後でリアルタイム監視を設定するのが容易になることは考えにくい**です。(うっ...!:thinking:)
Working on batch monitoring first means another legacy system to tear down later when you need to get real-time.
**最初にバッチ監視に取り組むことは、リアルタイムを取得する必要があるときに後で取り壊す必要がある別のレガシーシステム**を意味します。
(いきなりリアルタイム監視やるべき、という主張なのか...!:thinking:)

<!-- ここまで読んだ! -->

### Continual learning (vs. manual retraining) 継続的学習（対手動再訓練）

Continual learning refers to the ability to update your models whenever needed and to deploy this update quickly. 
継続的学習とは、必要に応じてモデルを更新し、その更新を迅速にデプロイする能力を指します。
Fast model updates enable our models to adapt to changing environments and business requirements, especially to data distribution shifts. 
迅速なモデル更新は、私たちのモデルが変化する環境やビジネス要件、特にデータ分布の変化に適応することを可能にします。

I’ve talked to ML engineers / data scientists at over 100 companies. 
私は100社以上のMLエンジニアやデータサイエンティストと話をしました。
Almost everyone told me that continual learning is too “far out”. 
**ほとんどの人が、継続的学習は「まだ先の話だ」と言いました**。
Most companies are still struggling with dependency management and monitoring to think about continual learning. 
**ほとんどの企業は、継続的学習を考える余裕がないほど、依存関係管理やモニタリングに苦労**しています。

At the same time, nobody has ever told me that they don’t want continual learning. 
同時に、誰も継続的学習を望んでいないとは言いませんでした。
Continual learning is too “far out” because we don’t yet have the right tool for it. 
継続的学習が「まだ先の話だ」とされるのは、私たちがそれに適したツールをまだ持っていないからです。
When the right tool emerges that makes continual learning “just work”, I believe the transition will be swift. 
継続的学習を「ただ機能させる」適切なツールが登場すれば、移行は迅速に行われると私は信じています。

We don’t need streaming to continually update our models. 
**私たちはモデルを継続的に更新するためにストリーミングを必要としません**。
Assuming that you already have a way of accessing fresh data, the hard part of continual learning isn’t in updating the models, but in ensuring that the updated models work. 
新しいデータにアクセスする方法がすでにあると仮定すると、**継続的学習の難しい部分はモデルの更新ではなく、更新されたモデルが機能することを保証するこ**とです。
We need to find a way to evaluate each model iteration fast, which brings us back to real-time monitoring and streaming. 
私たちは各モデルの反復を迅速に評価する方法を見つける必要があり、これがリアルタイムモニタリングとストリーミングに戻ることになります。
(継続的訓練そのものは、実務上はx日間やx時間に1回のバッチ更新で十分だよね! でも新しいモデルをデプロイした時にそれが適切に機能しているかモニタリングするべきで、そのため結局ストリーミングデータによるリアルタイム監視が重要だよね、って解釈...!:thinking:)

<!-- ここまで読んだ! -->

## 2. From table to log

I hope that I’ve convinced you why and where we need streaming in ML. 
私は、なぜMLにおいてストリーミングが必要であるか、どこで必要であるかを納得させられたことを願っています。

If you’re not convinced, I’d love to hear from you. 
もし納得できない場合は、ぜひお知らせください。

Now, let’s walk through some of the core concepts behind streaming that I find really cool. 
さて、私が本当に面白いと思うストリーミングの背後にあるいくつかのコアコンセプトを見ていきましょう。

The first article that helped me make sense of streaming is the classic post "The log" by Jay Kreps, a creator of Kafka. 
ストリーミングを理解するのに役立った最初の記事は、Kafkaの創設者であるJay Krepsによる古典的な投稿「The log」です。

Side note: Kreps mentioned in a tweet that he wrote the post to see if there was enough interest in streaming for his team to start a company around it. 
余談ですが、Krepsはツイートで、彼のチームがストリーミングに関する会社を始めるのに十分な関心があるかどうかを確認するためにこの投稿を書いたと述べています。

The post must have been popular because his team spun out of LinkedIn to become Confluent. 
この投稿は人気があったに違いなく、彼のチームはLinkedInから分社してConfluentになりました。

The core idea of the post (for me) is the duality of table and log. 
私にとって、この投稿の核心的なアイデアは、テーブルとログの二重性です。

You’re probably already familiar with data tables, like a MySQL table or a pandas DataFrame. 
おそらく、MySQLテーブルやpandas DataFrameのようなデータテーブルにはすでに慣れているでしょう。

For simplicity, consider the following inventory table. 
簡単のために、以下の在庫テーブルを考えてみましょう。

Let’s say, on June 19, you want to make a change to this table – e.g. changing the price of item #3 (Blouse) from $30 to $35. 
例えば、6月19日にこのテーブルに変更を加えたいとしましょう。つまり、アイテム#3（ブラウス）の価格を$30から$35に変更することです。

There are many ways to do this, but the 2 common approaches are: 
これを行う方法はいくつかありますが、一般的な2つのアプローチは次のとおりです。

1. Go to where the table is stored and make the change directly (e.g. overwriting a file). 
1. テーブルが保存されている場所に行き、直接変更を加える（例：ファイルを上書きする）。

This means that we’ll have no way of reverting the change, but many companies do it anyway. 
これにより、変更を元に戻す方法がなくなりますが、多くの企業はそれでも行います。

2. Send an update with the new price {"timestamp": "2022-06-19 09:23:23", "id": 3, "Price ($)": 35}, and this update will be applied to the table. 
2. 新しい価格{"timestamp": "2022-06-19 09:23:23", "id": 3, "Price ($)": 35}を含む更新を送信し、この更新がテーブルに適用されます。

Over time, we’ll have a series of ordered updates, which is called a log. 
時間が経つにつれて、順序付けられた一連の更新があり、これをログと呼びます。

Each update is an example of an event. 
各更新はイベントの一例です。

Logs are append-only. 
ログは追加専用です。

You can only append the new events to your existing log. 
既存のログに新しいイベントを追加することしかできません。

You can’t overwrite previous events. 
以前のイベントを上書きすることはできません。

```
…
{"timestamp": "2022-06-08 11:05:04", "id": 3, "Item": "Blouse", "Price ($)": 30}
{"timestamp": "2022-06-17 03:12:16", "id": 4, "Item": "Jeans", "Price ($)": 40}
{"timestamp": "2022-06-19 09:23:23", "id": 3, "Item": "Blouse", "Price ($)": 35}
```

I’m using wall clock timestamps for readability. 
私は可読性のために壁時計のタイムスタンプを使用しています。

In practice, wall clocks are unreliable. 
実際には、壁時計は信頼性がありません。

Distributed systems often leverage logical clock instead. 
分散システムでは、代わりに論理クロックを利用することがよくあります。

A table captures the state of data at a point in time. 
テーブルは、ある時点でのデータの状態をキャプチャします。

Given a table alone, we don’t know what the state of data was a day ago or a week ago. 
テーブルだけでは、1日前や1週間前のデータの状態がわかりません。

Given a log of all the changes to this table, we can recreate this table at any point in time. 
このテーブルへのすべての変更のログがあれば、任意の時点でこのテーブルを再作成できます。

You’re already familiar with logs if you work with git. 
gitを使っているなら、ログにはすでに慣れているでしょう。

A git log keeps track of all the changes to your code. 
gitログは、コードのすべての変更を追跡します。

Given this log, you can recreate your code at any point in time. 
このログがあれば、任意の時点でコードを再作成できます。



### Stateless vs. stateful log ステートレスとステートフルのログ

It’s possible to send an event with the price difference only{"id": 3, "Action": "increase", "Price ($)": 5}. 
価格差のみを持つイベントを送信することが可能です{"id": 3, "Action": "increase", "Price ($)": 5}。

For this type of event we’ll need to look at the previous price to determine the updated price. 
このタイプのイベントでは、更新された価格を決定するために前の価格を確認する必要があります。

This is called a stateful event (we need to know the previous state to construct the current state). 
これはステートフルイベントと呼ばれます（現在の状態を構築するために前の状態を知る必要があります）。

The type of event mentioned in #2 is a stateless log. 
#2で言及されたイベントのタイプはステートレスログです。

Stateful events are required to be processed in order – adding $5 to the blouse price then doubling it is very different from doubling it then adding $5. 
ステートフルイベントは順番に処理する必要があります - ブラウスの価格に$5を加えてから倍にすることは、倍にしてから$5を加えることとは非常に異なります。

There’s a whole industry focusing on solving stateful events called Change Data Capture (CDC). 
ステートフルイベントを解決することに焦点を当てた業界全体があり、これをChange Data Capture（CDC）と呼びます。

See Debezium, Fivetran, Striim. 
Debezium、Fivetran、Striimを参照してください。



### Real-time transport and computation engine リアルタイム輸送および計算エンジン

There are two components of a streaming system: the real-time transport and the computation engine.  
ストリーミングシステムには2つのコンポーネントがあります：リアルタイム輸送と計算エンジン。

- Thereal-time transport, which are basically distributed logs.  
- リアルタイム輸送は基本的に分散ログです。  
Data in real-time transports are called streaming data, or “data in motion” as coined by Confluent.  
リアルタイム輸送のデータはストリーミングデータ、またはConfluentによって名付けられた「動いているデータ」と呼ばれます。  
Examples: Kafka, AWS Kinesis, GCP Dataflow.  
例：Kafka、AWS Kinesis、GCP Dataflow。

- Thecomputation engine performs computation (e.g. joining, aggregation, filtering, etc.) on the data being transported.  
- 計算エンジンは、輸送されているデータに対して計算（例：結合、集約、フィルタリングなど）を実行します。  
Examples: Flink, KSQL, Beam, Materialize, Decodable, Spark Streaming.  
例：Flink、KSQL、Beam、Materialize、Decodable、Spark Streaming。

Transports usually have capacity for simple computation.  
輸送は通常、単純な計算の能力を持っています。  
For example, Kafka is a transport that also has an API called Kafka Streams that provides basic stream processing capacity.  
例えば、Kafkaは、基本的なストリーム処理能力を提供するKafka StreamsというAPIを持つ輸送です。  
However, if you want to perform complex computation, you might want an optimized stream computation engine (similar to how bars usually have some food options but if you want real food you’ll want to go to a restaurant).  
しかし、複雑な計算を実行したい場合は、最適化されたストリーム計算エンジンが必要になるかもしれません（バーには通常いくつかの食事オプションがありますが、本物の食事が欲しい場合はレストランに行くのが良いのと似ています）。

We’ve discussed logs at length.  
私たちはログについて詳しく議論してきました。  
From the next section onward, we’ll focus on stream computation.  
次のセクション以降では、ストリーム計算に焦点を当てます。



## 3. ストリーム処理の簡単な例

Imagine that we want to use the average price of all items a user has looked at as a feature. 
ユーザが見たすべてのアイテムの平均価格を特徴量として使用したいと考えたとします。 
If we put all these items into a table, the feature definition might look something like this. 
これらのアイテムをテーブルに入れると、特徴量の定義は次のようになります。 
This is batch processing. 
これはバッチ処理です。

```
# Pseudocode
def average_price(table):
return sum(table.price) / len(table)
```

If, instead, we have a log of all item updates, how should we compute the average price? 
代わりに、すべてのアイテムの更新ログがある場合、平均価格はどのように計算すべきでしょうか？



### Internal state and checkpoints 内部状態とチェックポイント

One way to do it is to process events in the log (replay the log) from the beginning of time to recreate the inventory table of all items. 
その方法の一つは、ログ内のイベントを処理（ログを再生）し、すべてのアイテムの在庫テーブルを再作成することです。しかし、実際には平均価格を取得するために全体のテーブルを追跡する必要はありません。 
私たちが必要とするのは、すべてのアイテムの合計価格とアイテム数だけです。 The average price can be computed from these two values. 
平均価格はこれら二つの値から計算できます。The total price and the count constitute the internal state of the stream processing job. 
合計価格とカウントは、ストリーム処理ジョブの内部状態を構成します。We say this computation is stateful because we keep track of the internal state between computation. 
この計算は、計算の間に内部状態を追跡するため、状態を持つ（stateful）といいます。

```
# Pseudocode 擬似コード
def average_price(log):
initialize total_price, item_count
for each event in the log:
update total_price, item_count
avg_price = total_price / item_count
return avg_price
```

If the log is large (in 2021, Netflix was processing 20 trillion events a day!), replaying the log from the beginning can be prohibitively slow. 
ログが大きい場合（2021年にはNetflixが1日あたり20兆のイベントを処理していました！）、最初からログを再生するのは非常に遅くなる可能性があります。To mitigate this, we can occasionally save the internal state of the job, e.g. once every hour. 
これを軽減するために、私たちは時折ジョブの内部状態を保存することができます。例えば、1時間ごとに保存します。The saved internal state is called a checkpoint (or savepoint), and this job can resume from any checkpoint. 
保存された内部状態はチェックポイント（checkpoint）またはセーブポイント（savepoint）と呼ばれ、このジョブは任意のチェックポイントから再開できます。The function above will be updated as follows: 
上記の関数は次のように更新されます。

```
# Pseudocode 擬似コード
def average_price(log):
find the latest checkpoint X
load total_price, item_count from X
for each event in the log after X:
update total_price, item_count
avg_price = total_price / item_count
return avg_price
```



### Materialized view マテリアライズドビュー

The computed average price value, if saved, will become a materialized view of the feature average price. 
計算された平均価格の値が保存されると、それは特徴の平均価格のマテリアライズドビューになります。

Each time we query from the materialized view, we don’t recompute the value, but read the saved value. 
マテリアライズドビューからクエリを実行するたびに、値を再計算するのではなく、保存された値を読み取ります。

You might wonder: “Why must we come up with a new term like materialized view instead of saying saved copy or cache?” 
「なぜsaved copyやcacheではなく、materialized viewという新しい用語を考え出さなければならないのか？」と疑問に思うかもしれません。

Because “saved copy” or “cache” implies that the computed value will never change. 
なぜなら、「保存されたコピー」や「キャッシュ」は、計算された値が決して変わらないことを意味するからです。

Materialized views can change due to late arrivals. 
マテリアライズドビューは、遅延到着によって変わる可能性があります。

If an event that happened at 10.15am got delayed and arrived at 11.10am, all the materialized views that might be affected by this update should be recomputed to account for this delayed event. 
午前10時15分に発生したイベントが遅延し、午前11時10分に到着した場合、この更新によって影響を受ける可能性のあるすべてのマテリアライズドビューは、この遅延イベントを考慮するために再計算されるべきです。

I say “should” because not all implementations do this. 
「すべき」と言うのは、すべての実装がこれを行うわけではないからです。

Reading from a materialized view is great for latency, since we don’t need to recompute the feature. 
マテリアライズドビューから読み取ることは、レイテンシにとって素晴らしいです。なぜなら、特徴を再計算する必要がないからです。

However, the materialized view will eventually become outdated. 
しかし、マテリアライズドビューは最終的に古くなります。

Materialized views will need to be refreshed (recomputed) either periodically (every few minutes) or based on a change stream. 
マテリアライズドビューは、定期的（数分ごと）に、または変更ストリームに基づいてリフレッシュ（再計算）する必要があります。

When refreshing a materialized view, you can recompute it from scratch (e.g. using all the items to compute their average price). 
マテリアライズドビューをリフレッシュする際には、最初から再計算することができます（例：すべてのアイテムを使用して平均価格を計算する）。

Or you can update it using only the new information (e.g. using the latest materialized average price + the prices of updated items). 
または、新しい情報のみを使用して更新することもできます（例：最新のマテリアライズド平均価格 + 更新されたアイテムの価格）。

The latter is called incremental materialized. 
後者はインクリメンタルマテリアライズドと呼ばれます。

For those interested, Materialize has a great article with examples on materialized and incremental materialized. 
興味のある方のために、Materializeにはマテリアライズドとインクリメンタルマテリアライズドに関する素晴らしい記事と例があります。



## 4. タイムトラベルとバックフィリング

We’ve talked about how to compute a feature on the latest data. 
最新のデータで特徴量を計算する方法について話しました。 
Next, we’ll discuss how to compute a feature in the past. 
次に、過去のデータで特徴量を計算する方法について説明します。 

Imagine that the latest price for the item blouse in our inventory is $35. 
私たちの在庫にあるブラウスの最新の価格が$35であると想像してください。 
We want to compute the avg_price feature as it would’ve happened on June 10. 
私たちは、6月10日に発生したであろう avg_price 特徴量を計算したいと考えています。 
There are two ways this feature might have differed in the past: 
この特徴量が過去に異なっていた可能性がある方法は2つあります。 

- The data was different. For example, the blouse’s price was $30 instead of $35. 
- データが異なっていました。例えば、ブラウスの価格は$35ではなく$30でした。 
- The feature logic was different. For example: 
- 特徴量のロジックが異なっていました。例えば： 
- Today, the avg_price feature computes the average raw price of all items. 
- 今日、avg_price 特徴量はすべてのアイテムの平均生の価格を計算します。 
- On June 10, the avg_price feature computes the average listed price, and the listed price is the raw price plus discount. 
- 6月10日には、avg_price 特徴量が平均リスト価格を計算し、リスト価格は生の価格に割引を加えたものです。 
- Today, the avg_price feature computes the average raw price of all items. 
- 今日、avg_price 特徴量はすべてのアイテムの平均生の価格を計算します。 
- On June 10, the avg_price feature computes the average listed price, and the listed price is the raw price plus discount. 
- 6月10日には、avg_price 特徴量が平均リスト価格を計算し、リスト価格は生の価格に割引を加えたものです。 
- Today, the avg_price feature computes the average raw price of all items. 
- 今日、avg_price 特徴量はすべてのアイテムの平均生の価格を計算します。 
- On June 10, the avg_price feature computes the average listed price, and the listed price is the raw price plus discount. 
- 6月10日には、avg_price 特徴量が平均リスト価格を計算し、リスト価格は生の価格に割引を加えたものです。 

If we accidentally use the data or the feature logic from today instead of the data & logic from June 10, it means there is a leakage from the future. 
もし私たちが誤って6月10日のデータとロジックの代わりに今日のデータやロジックを使用した場合、それは未来からの漏洩があることを意味します。 
Point-in-time correctness refers to a system’s ability to accurately perform a computation as it would’ve happened at any time in the past. 
ポイントインタイムの正確性は、システムが過去の任意の時点で発生したであろう計算を正確に実行する能力を指します。 
Point-in-time correctness means no data leakage. 
ポイントインタイムの正確性は、データの漏洩がないことを意味します。 

Retroactively processing historical data using a different logic is also called backfilling. 
異なるロジックを使用して過去のデータを遡って処理することは、バックフィリングとも呼ばれます。 
Backfilling is a very common operation in data workflows, e.g. see backfilling in Airflow and Amplitude. 
バックフィリングはデータワークフローにおいて非常に一般的な操作であり、例えばAirflowやAmplitudeでのバックフィリングを参照してください。 
Backfilling can be done both in batch and streaming. 
バックフィリングはバッチ処理とストリーミングの両方で行うことができます。 

- With batch backfilling, you can apply the new logic (e.g. new feature definition) to a table in the past. 
- バッチバックフィリングでは、新しいロジック（例えば、新しい特徴量定義）を過去のテーブルに適用できます。 
- With stream backfilling, you can apply the new logic to the log in a given period of time in the past, e.g. apply it to the log on June 10, 2022. 
- ストリームバックフィリングでは、過去の特定の期間のログに新しいロジックを適用できます。例えば、2022年6月10日のログに適用します。 

Time travel is hard, because we need to keep track of the states of your data over time. 
タイムトラベルは難しいです。なぜなら、私たちはデータの状態を時間の経過とともに追跡する必要があるからです。 
It can get very complicated if your data is joined from multiple places. 
データが複数の場所から結合されている場合、非常に複雑になる可能性があります。 
For example, the average listed price depends on raw prices and discounts, both of them can independently change over time. 
例えば、平均リスト価格は生の価格と割引に依存しており、両方とも独立して時間とともに変化する可能性があります。



### Time travel in ML workflows MLワークフローにおけるタイムトラベル

There are many scenarios in an ML workflow where time travel is necessary, but here are the two major ones: 
MLワークフローにはタイムトラベルが必要なシナリオが多くありますが、ここでは2つの主要なシナリオを紹介します。

- to ensure the train-predict consistency for online features (also known as online-offline skew or training-serving skew) 
- オンライン機能（オンライン-オフラインの偏りまたはトレーニング-サービングの偏りとも呼ばれる）のためにトレーニングと予測の一貫性を確保すること

- to compare two models on historical data 
- 歴史的データに基づいて2つのモデルを比較すること

Online prediction can cause train-predict inconsistency. 
オンライン予測はトレーニングと予測の不一致を引き起こす可能性があります。

Imagine our model does online prediction using online features, one of them is the average price of all the items this user has looked at in the last 30 minutes. 
私たちのモデルがオンライン機能を使用してオンライン予測を行うと仮定しましょう。その一つは、このユーザーが過去30分間に見たすべてのアイテムの平均価格です。

Whenever a prediction request arrives, we compute this feature using the prices for these items at that moment, possibly using stream processing. 
予測リクエストが到着するたびに、私たちはその時点でのこれらのアイテムの価格を使用してこの機能を計算します。おそらくストリーム処理を使用して。

During training, we want to use this same feature, but computed on historical data, such as data from the last week. 
トレーニング中には、この同じ機能を使用したいのですが、過去1週間のデータなどの歴史的データに基づいて計算します。

Over the last week, however, the prices for many items have changed, some have changed multiple times. 
しかし、過去1週間で多くのアイテムの価格が変わり、一部は何度も変わっています。

We need time travel to ensure that the historical average prices can be computed correctly at each given point in time. 
私たちは、歴史的な平均価格が各時点で正しく計算できるようにするためにタイムトラベルが必要です。

Traditionally, ML workflows are development-first. 
従来、MLワークフローは開発優先です。

Data scientists experiment with new features for the training pipeline. 
データサイエンティストはトレーニングパイプラインのための新しい機能を試します。

Feature definitions, aka feature logic, are often written for batch processing, blissfully unaware of the time-dependent nature of data. 
機能定義、つまり機能ロジックは、しばしばバッチ処理のために書かれ、データの時間依存性を無視しています。

Training data often doesn’t even have timestamps. 
トレーニングデータには、しばしばタイムスタンプすらありません。

This approach might help data scientists understand how a model or feature does during training, but not how this model / feature will perform in production, both performance-wise (e.g. accuracy, F1) and operation-wise (e.g. latency). 
このアプローチは、データサイエンティストがトレーニング中にモデルや機能がどのように機能するかを理解するのに役立つかもしれませんが、このモデル/機能が本番環境でどのように機能するか（パフォーマンス面（例：精度、F1）および運用面（例：レイテンシ））を理解するのには役立ちません。

At deployment, ML or ops engineers need to translate these batch features into streaming features for the prediction pipeline and optimize them for latency. 
デプロイ時に、MLまたは運用エンジニアは、これらのバッチ機能を予測パイプラインのためのストリーミング機能に変換し、レイテンシの最適化を行う必要があります。

Errors during this translation process – e.g. changes or assumptions in one pipeline not updated or insufficiently tested in another – create train-predict inconsistency. 
この翻訳プロセス中のエラー（例：あるパイプラインでの変更や仮定が別のパイプラインで更新されていない、または十分にテストされていない）は、トレーニングと予測の不一致を引き起こします。

This inconsistency gets worse when the training and prediction pipelines use different languages, e.g. the training pipeline uses Python and the prediction pipeline uses SQL or Java. 
この不一致は、トレーニングパイプラインがPythonを使用し、予測パイプラインがSQLまたはJavaを使用する場合に悪化します。

To avoid this inconsistency, we should get rid of the translation process altogether. 
この不一致を避けるために、私たちは翻訳プロセスを完全に排除すべきです。

What if we let data scientists experiment with features for the prediction pipeline directly? 
データサイエンティストが予測パイプラインのための機能を直接試すことができるとしたらどうでしょうか？

You can write new features as they will be used in production. 
本番環境で使用されるように新しい機能を書くことができます。

To test out these new features, you apply them to historical data to generate training data to train models. 
これらの新しい機能をテストするために、歴史的データに適用してトレーニングデータを生成し、モデルをトレーニングします。

Applying new feature logic to historical data is exactly what backfilling is. 
新しい機能ロジックを歴史的データに適用することは、まさにバックフィリングです。

With this setup, ML workflows become production-first! 
この設定により、MLワークフローは本番優先になります！

Thanks to its ability to support both streaming and batch processing, SQL has emerged to be a popular language for production-first ML workflows. 
ストリーミングとバッチ処理の両方をサポートする能力のおかげで、SQLは本番優先のMLワークフローにおいて人気のある言語となっています。

In the relational database era, SQL computation engines were entirely in the batch paradigm. 
リレーショナルデータベースの時代には、SQL計算エンジンは完全にバッチパラダイムにありました。

In recent years, there has been a lot of investment in streaming SQL engines, such as KSQL and Apache Flink. 
近年、KSQLやApache FlinkなどのストリーミングSQLエンジンへの多くの投資が行われています。

(See Streaming SQL to Unify Batch & Stream Processing w/ Apache Flink @Uber) 
（ストリーミングSQLを使用してバッチとストリーム処理を統合する @Uberを参照）

Development-first ML workflows: features are written for training and adapted for online prediction. 
開発優先のMLワークフロー：機能はトレーニングのために書かれ、オンライン予測のために適応されます。

Production-first ML workflows: features are written for online prediction and backfilled for training. 
本番優先のMLワークフロー：機能はオンライン予測のために書かれ、トレーニングのためにバックフィルされます。

Backfilling to generate features for training is how feature stores like FeatureForm and Tecton ensure train-predict consistency. 
トレーニングのための機能を生成するためのバックフィリングは、FeatureFormやTectonのような機能ストアがトレーニングと予測の一貫性を確保する方法です。

However, most feature stores only support limited streaming computation engines, which can pose performance (latency + cost) challenges when you want to work with complex online features. 
しかし、ほとんどの機能ストアは限られたストリーミング計算エンジンしかサポートしておらず、複雑なオンライン機能を扱う際にパフォーマンス（レイテンシ + コスト）の課題を引き起こす可能性があります。

Imagine your team is using model A to serve live prediction requests, and you just came up with a new model B. 
あなたのチームがモデルAを使用してライブ予測リクエストに応答していると仮定し、あなたは新しいモデルBを考案しました。

Before A/B testing model B on live traffic, you want to evaluate model B on the most recent data, e.g. on the prediction requests from the last day. 
モデルBをライブトラフィックでA/Bテストする前に、最新のデータ（例：過去1日の予測リクエスト）でモデルBを評価したいと考えています。

To do so, you replay the requests from the last day, and use model B to generate predictions for those requests to see what the performance would have been if we had used B instead of A. 
そのために、過去1日のリクエストを再生し、モデルBを使用してそれらのリクエストに対する予測を生成し、Aの代わりにBを使用していた場合のパフォーマンスを確認します。

If model B uses exactly the same feature logic as model A, model B can reuse the features previously computed for model A. 
モデルBがモデルAとまったく同じ機能ロジックを使用している場合、モデルBは以前にモデルAのために計算された機能を再利用できます。

However, if model B uses a different feature set, you’ll have to backfill, apply model B’s feature logic to data from the last day, to generate features for model B. 
しかし、モデルBが異なる機能セットを使用している場合、バックフィルを行い、モデルBの機能ロジックを過去1日のデータに適用してモデルBのための機能を生成する必要があります。

This is also called a backtest. 
これはバックテストとも呼ばれます。



### Time travel challenges for data scientists データサイエンティストのためのタイムトラベルの課題

Some data science teams have told me that they need to do time travel for their data but their data doesn’t have timestamps. 
いくつかのデータサイエンスチームは、データのタイムトラベルが必要だが、データにタイムスタンプがないと私に言いました。 
What should they do? 
彼らはどうすればよいのでしょうか？

It’s impossible to time travel without timestamps. 
タイムスタンプなしでタイムトラベルすることは不可能です。 
This is not a problem that data scientists can solve without having control over how data is ingested and stored. 
これは、データがどのように取り込まれ、保存されるかを制御できないデータサイエンティストが解決できる問題ではありません。

So why don’t data scientists have access to data with timestamps? 
では、なぜデータサイエンティストはタイムスタンプ付きのデータにアクセスできないのでしょうか？

One reason is that data platforms might have been designed using practices from an era where ML production wasn’t well understood. 
一つの理由は、データプラットフォームがMLプロダクションが十分に理解されていなかった時代の慣行を用いて設計された可能性があることです。 
Therefore, they were not designed with ML production in mind, and timestamps weren’t considered an important artifact to keep track of. 
したがって、MLプロダクションを考慮して設計されておらず、タイムスタンプは追跡すべき重要なアーティファクトとは見なされていませんでした。

Another reason is the lack of communication between those who ingest the data (e.g. the data platform team) and those who consume the data (e.g. the data science team). 
もう一つの理由は、データを取り込む人々（例：データプラットフォームチーム）とデータを消費する人々（例：データサイエンスチーム）との間のコミュニケーションの欠如です。 
Many companies already have application logs, however, the timestamps are not retained during data ingestion or processing, or they are retained somewhere that data scientists don’t access to. 
多くの企業はすでにアプリケーションログを持っていますが、タイムスタンプはデータの取り込みや処理中に保持されず、またはデータサイエンティストがアクセスできない場所に保持されています。

This is an operational issue that companies who want modern ML workflows will need to invest into. 
これは、現代のMLワークフローを望む企業が投資する必要がある運用上の問題です。 
Without a well-designed data pipeline, data scientists won’t be able to build production-ready data applications. 
適切に設計されたデータパイプラインがなければ、データサイエンティストはプロダクション対応のデータアプリケーションを構築することができません。



## 5. Why is streaming hard? なぜストリーミングは難しいのか？

I hope that by now, I’ve convinced you why streaming is important for ML workloads. 
これまでに、ストリーミングが機械学習（ML）ワークロードにとって重要である理由を納得させられたことを願っています。

Another question is: if streaming is so important, why is it not more common in ML workflows? 
もう一つの疑問は、ストリーミングがそれほど重要であれば、なぜMLワークフローでより一般的ではないのかということです。

Because it’s hard. 
それは難しいからです。

If you’ve worked with streaming before, you probably don’t need any convincing. 
もし以前にストリーミングを扱ったことがあるなら、あなたはおそらく納得する必要はないでしょう。

Tyler Aikidau gave a fantastic talk on the open challenges in stream processing. 
Tyler Aikidauは、ストリーム処理におけるオープンな課題について素晴らしい講演を行いました。

Here, I’ll go over the key challenges from my perspective as a data scientist. 
ここでは、データサイエンティストとしての私の視点から、主要な課題について説明します。

This is far from an exhaustive list. 
これは決して包括的なリストではありません。

A streaming system needs to be able to handle all of these challenges and more. 
ストリーミングシステムは、これらすべての課題やそれ以上のものに対処できる必要があります。



### Distributed computation 分散計算

Streaming is simple when you have a small amount of updates and they are generated and consumed by one single machine, like the inventory example in From table to log. 
ストリーミングは、少量の更新があり、それが1台のマシンによって生成され消費される場合、例えば「From table to log」の在庫の例のように、簡単です。

However, a real-world application can have hundreds, if not thousands, of microservices, spread out over different machines. 
しかし、実世界のアプリケーションには、数百、あるいは数千のマイクロサービスが異なるマシンに分散して存在する可能性があります。

Many of these machines might try to read and write from the same log. 
これらのマシンの多くは、同じログから読み書きしようとするかもしれません。

Streaming systems are highly distributed. 
ストリーミングシステムは非常に分散化されています。

Engineers working directly with streaming need to have a deep understanding of distributed systems, which not many data scientists would’ve exposure to in their day-to-day jobs. 
ストリーミングに直接関わるエンジニアは、分散システムについて深く理解している必要がありますが、これは多くのデータサイエンティストが日常業務で触れることのない分野です。

We need good abstraction to enable data scientists to leverage streaming without having to deal with the underlying distributed systems. 
私たちは、データサイエンティストが基盤となる分散システムに対処することなくストリーミングを活用できるようにするための良い抽象化が必要です。



### Time-variant results 時間変動結果

Time adds another dimension of complexity. 
時間は複雑さの別の次元を加えます。
If you apply the same query to the same table twice, you’ll get the same result. 
同じクエリを同じテーブルに2回適用すると、同じ結果が得られます。
However, if you apply the same query to the same stream twice, you’ll likely get very different results. 
しかし、同じクエリを同じストリームに2回適用すると、非常に異なる結果が得られる可能性が高いです。

In batch, if a query fails, you can just rerun it. 
バッチ処理では、クエリが失敗した場合、単に再実行すればよいです。
But in streaming, due to time-variant results, if a query fails, what should we do? 
しかし、ストリーミングでは、時間変動結果のために、クエリが失敗した場合、私たちは何をすべきでしょうか？
Different stream processing engines have different ways to address this problem. 
異なるストリーム処理エンジンは、この問題に対処するための異なる方法を持っています。
For example, Flink uses the Chandy–Lamport algorithm, developed by K. Mani Chandy and the Turing Award winner Leslie Lamport. 
例えば、Flinkは、K. Mani Chandyとチューリング賞受賞者のLeslie Lamportによって開発されたChandy–Lamportアルゴリズムを使用しています。



### Cascading failure カスケーディング障害

In a batch setting, jobs are typically scheduled at large intervals, hence fluctuation in workloads isn’t a big deal. 
バッチ設定では、ジョブは通常大きな間隔でスケジュールされるため、ワークロードの変動はそれほど問題ではありません。

If you schedule a job to run every 24 hours and one run takes 6 hours instead of 4 hours, these extra 2 hours won’t affect the next run. 
もしジョブを24時間ごとに実行するようにスケジュールし、1回の実行が4時間ではなく6時間かかる場合、これらの追加の2時間は次の実行に影響を与えません。

However, fluctuation in a streaming setting can make it very hard to maintain consistently low latency. 
しかし、ストリーミング設定における変動は、一貫して低いレイテンシを維持することを非常に難しくする可能性があります。

Assuming that your streaming system is capable of handling 100 events / second. 
あなたのストリーミングシステムが1秒あたり100イベントを処理できると仮定します。

If the traffic is less than 100 events / second, your system is fine. 
トラフィックが1秒あたり100イベント未満であれば、システムは問題ありません。

If the traffic suddenly surges to 200 events one second, ~100 events will be delayed. 
もしトラフィックが突然1秒間に200イベントに急増した場合、約100イベントが遅延します。

If not addressed quickly, these delayed 100 seconds will overload your system the next second, and so on, causing your system to significantly slow down. 
迅速に対処しないと、これらの遅延した100イベントが次の秒にシステムを過負荷にし、その結果、システムが著しく遅くなります。



### Availability vs. consistency 可用性と一貫性

Imagine that there are two machines trying to send updates about the same item:
同じアイテムについて更新を送信しようとしている2台のマシンを想像してみてください。
- Machine A, at “03:12:10”, updates that user views product 123
- Machine Aは「03:12:10」に、ユーザーが製品123を閲覧したと更新します。
- Machine B, at “03:12:16”, updates that user views product 234
- Machine Bは「03:12:16」に、ユーザーが製品234を閲覧したと更新します。

Due to some network delays, machine A’s update is delayed in transit, and arrives later than machine B’s update.
ネットワークの遅延により、マシンAの更新は遅れて到着し、マシンBの更新よりも遅くなります。

How long should we wait for machine A before computing the average prices of all items the user has looked at in the last 30 minutes?
過去30分間にユーザーが見たすべてのアイテムの平均価格を計算する前に、マシンAをどれくらい待つべきでしょうか？

If we don’t wait long enough, we’ll miss machine A’s update, and the feature will be incorrect.
十分に待たなければ、マシンAの更新を見逃し、その機能は不正確になります。

However, if we wait too long, the latency will be low.
しかし、あまりにも長く待つと、レイテンシが低くなります。

An optimal time window is probably somewhere in the middle.
最適な時間ウィンドウは、おそらくその中間にあるでしょう。

Therefore, the results of stream computation tend to be approximate.
したがって、ストリーム計算の結果は概算になる傾向があります。

This leads us to an interesting trade-off: availability vs. consistency.
これは、興味深いトレードオフ、すなわち可用性と一貫性をもたらします。

For our system to be highly available, we’ll want to duplicate the same workload over multiple machines.
私たちのシステムが高い可用性を持つためには、同じ作業負荷を複数のマシンに複製したいと考えます。

However, the more machines there are, the more stragglers there will be, and the more inconsistent the results of your stream computation will become.
しかし、マシンが増えれば増えるほど、遅延するマシンが増え、ストリーム計算の結果はより不一致になります。

All large-scale distributed systems, not just streaming systems, have to make this tradeoff.
ストリーミングシステムだけでなく、すべての大規模分散システムはこのトレードオフを考慮しなければなりません。



### Operational challenges 運用上の課題

While streaming technology can be technically hard, the real challenge for companies to adapt streaming is in operations. 
ストリーミング技術は技術的に難しい場合がありますが、企業がストリーミングに適応する際の本当の課題は運用にあります。

Operating on (near) real-time data streams means that we can make things happen in (near) real-time. 
(ほぼ)リアルタイムのデータストリームで運用することは、(ほぼ)リアルタイムで物事を実現できることを意味します。

Unfortunately, this means that catastrophes can also happen in (near) real-time. 
残念ながら、これは災害も(ほぼ)リアルタイムで発生する可能性があることを意味します。

Maintaining a streaming system means that your engineers will have to be on-call 24x7 to respond to incidents quickly. 
ストリーミングシステムを維持することは、エンジニアが24時間365日待機してインシデントに迅速に対応しなければならないことを意味します。

If you can’t figure out the problems and resolve them fast enough, data streams will be interrupted and you might lose data. 
問題を特定し、十分に迅速に解決できない場合、データストリームが中断され、データを失う可能性があります。

Because the stake is higher in streaming systems, maintenance of streaming systems requires a high level of automation and mature DevOps practices. 
ストリーミングシステムではリスクが高いため、ストリーミングシステムの維持には高いレベルの自動化と成熟したDevOpsプラクティスが必要です。

We’ve talked to many small teams who want to maintain their own Kafka or Flink clusters and it’s not pretty. 
私たちは、自分たちのKafkaやFlinkクラスターを維持したいと考えている多くの小さなチームと話をしましたが、状況はあまり良くありません。

Streaming is an area where I can see a lot of values in managed services (e.g. Confluent instead of Kafka). 
ストリーミングは、マネージドサービス（例：Kafkaの代わりにConfluent）に多くの価値が見出せる分野です。



## Conclusion 結論

Wow, this was a hard post for me to write. 
わあ、これは私にとって書くのが難しい投稿でした。

I hope you’re still with me. 
あなたがまだ私と一緒にいてくれることを願っています。

I’m very excited about the application of streaming for ML applications. 
私は、MLアプリケーションにおけるストリーミングの応用に非常に興奮しています。

My dream is that data scientists should have access to an ML platform that enables them to leverage streaming without having to worry about its underlying complexities. 
私の夢は、データサイエンティストがその基盤となる複雑さを気にせずにストリーミングを活用できるMLプラットフォームにアクセスできることです。

This platform needs to provide a high-enough level of abstraction for things to just work, while being flexible enough for data scientists to customize their workflows. 
このプラットフォームは、物事がうまく機能するために十分なレベルの抽象化を提供し、データサイエンティストが自分のワークフローをカスタマイズできるように十分な柔軟性を持つ必要があります。

I know that leveraging streaming for ML is hard right now and I believe in the value of making it easier, so I’m working on it. 
ストリーミングをMLに活用することが今は難しいことを知っており、それを容易にする価値を信じているので、私はそれに取り組んでいます。

Hit me up if you want to chat! 
もし話したいことがあれば、気軽に連絡してください！

This is a relatively new field, and I’m still learning too. 
これは比較的新しい分野であり、私もまだ学んでいます。

I’d appreciate any feedback and discussion points you have! 
あなたのフィードバックや議論のポイントをいただけると嬉しいです！



## Acknowledgment 謝辞

Thanks Zhenzhong Xu for having patiently answered all my dumb questions on streaming, Luke Metz, Chloe He, Han-chung Lee, Dan Turkel, and Robert Metzger.
Zhenzhong Xuには、ストリーミングに関する私の愚かな質問に忍耐強く答えてくれたことに感謝します。また、Luke Metz、Chloe He、Han-chung Lee、Dan Turkel、Robert Metzgerにも感謝します。

- hi@[thiswebsite]
- chiphuyen
- chipro
- chipiscrazy
- huyenchip19
- chiphuyen

I help companies deploy machine learning into production. 
私は企業が機械学習を本番環境に展開するのを支援します。

I write about AI applications, tooling, and best practices.
私はAIアプリケーション、ツール、ベストプラクティスについて執筆しています。
