Q# Meet Sibyl – DoorDash’s New Prediction Service – Learn about its Ideation, Implementation and Rollout
# シビルに会おう - DoorDashの新しい予測サービス - そのアイデア、実装、展開について学ぶ

June 29, 2020  
2020年6月29日  
Cody Zeng  
コディ・ゼン

link: https://careersatdoordash.com/blog/doordashs-new-prediction-service/

(ざっくり、推論サービスをいい感じに新しくしたよ、みたいな話!:thinking:

As companies utilize data to optimize and personalize customer experiences, it becomes increasingly important to implement services that can run machine learning models on massive amounts of data to quickly generate large-scale predictions.  
企業がデータを活用して顧客体験を最適化し、パーソナライズするにつれて、大量のデータに対して機械学習モデルを実行し、大規模な予測を迅速に生成できるサービスを実装することがますます重要になります。
At DoorDash, our platform is utilizing data to power models that curate search results, assign dashers, recognize fraud, and more.  
DoorDashでは、私たちのプラットフォームがデータを活用して、検索結果をキュレーションし、配達員を割り当て、詐欺を認識するモデルを動かしています。
This would only be possible with a robust prediction service that can apply our models to the data and serve our various microservices that rely on data-driven insights.  
これは、私たちのモデルをデータに適用し、データ駆動のインサイトに依存するさまざまなマイクロサービスに提供できる堅牢な予測サービスがあってこそ可能です。

We recently implemented DoorDash’s next generation prediction service, and named it Sibyl prediction service, after the Greek oracles who were known toutter predictions in an ecstatic frenzy.  
私たちは最近、**DoorDashの次世代予測サービスを実装**し、ギリシャの神託者にちなんで「シビル予測サービス」と名付けました。彼らは熱狂的な狂乱の中で予測を口にすることで知られていました。
In this blog post you will learn the ideation, implementation and rollout of Sibyl and the steps we took to build a prediction service that can handle massive numbers of calls per second without breaking a sweat.  
このブログ記事では、シビルのアイデア、実装、展開について学び、**秒間に大量の呼び出しを処理できる予測サービス**(-> たぶんリアルタイム推論だ!)を構築するために私たちが取ったステップを紹介します。
If you are interested in how models are integrated with the service you can check out this article here.  
モデルがサービスとどのように統合されているかに興味がある場合は、[こちらの記事](https://doordash.engineering/2020/10/01/integrating-a-scoring-framework-into-a-prediction-service/)をチェックしてください。
While Sibyl itself may be unique to DoorDash, the learnings and considerations we used to build it can be applied to almost any high throughput, low latency service.  
シビル自体はDoorDashに特有かもしれませんが、**私たちがそれを構築するために使用した学びや考慮事項は、ほぼすべての高スループット、低遅延サービスに適用できます**。
If you are looking to learn about the greater ML platform, check out this blog post: DoorDash’s ML Platform – The Beginning  
より大きなMLプラットフォームについて学びたい場合は、こちらのブログ記事をチェックしてください：[DoorDashのMLプラットフォーム - 始まり](https://doordash.engineering/2020/04/23/doordash-ml-platform-the-beginning/)

<!-- ここまで読んだ! -->

## Ideation and Requirements: The prediction service’s role in Machine learning (ML) infrastructure
## アイデアと要件：予測サービスの機械学習（ML）インフラストラクチャにおける役割

Before starting any actual coding, we took some time to consider exactly what role Sibyl would have in DoorDash’s ML infrastructure ecosystem, as well as all the required functionalities that this new prediction service needed.
実際のコーディングを始める前に、私たちは**Sibyl(新しい推論サービス)がDoorDashのMLインフラストラクチャエコシステムにおいてどのような役割を果たすのか**、また**この新しい予測サービスに必要なすべての要件**について考える時間を取りました。
(この設計の時間は大事だ...!:thinking:)

In terms of its role, we wanted the Sibyl prediction service to handle all real-time predictions, and to focus on predicting, leaving other components, such as feature calculation, model training pipelines, and storage of features and models, in separate services/stores.
その役割に関して、私たちは**Sibyl予測サービスがすべてのリアルタイム予測を処理し、予測に集中することを望んでいました。他のコンポーネント、例えば特徴量計算、モデルトレーニングパイプライン、特徴やモデルのストレージは、別のサービスやストアに任せることにしました**。
(あ、FTI Pipelinesアーキテクチャ的な設計だ!:thinking:)
The first thing we considered was scalability and latency, given that we were expecting hundreds of thousands of predictions per second, and that in order to convince other services to call our service for predictions, we needed to make them so fast that calling Sibyl would be better than the alternative of each individual service making predictions itself.
私たちが最初に考慮したのはスケーラビリティとレイテンシでした。なぜなら、私たちは**毎秒数十万の予測を期待**しており、他のサービスに私たちのサービスを呼び出して予測を行うように納得させるためには、Sibylを呼び出す方が各サービスが自ら予測を行うよりも速くする必要があったからです。

### How Sibyl prediction service fits into the ML infrastructure ecosystem:
Sibyl予測サービスがMLインフラストラクチャエコシステムにどのように適合するか：

![Figure 1: Sibyl prediction service high level flow]()

As you can see by Figure 1, all predictions come in from other services as gRPC requests, and Sibyl retrieves both models and features from independent stores (with the option of outputting predictions to Snowflake for offline evaluation).
図1に示すように、**すべての予測は他のサービスからgRPCリクエストとして受け取られ**、Sibylは独立したストアからモデルと特徴量の両方を取得します(モデルレジストリと特徴量ストア...!!:thinking:)
**オフライン評価のために予測をSnowflakeに出力するオプションもあります**。
(オフライン評価の時も、本番と同様の推論サービスに推論させるのか...! 計算リソースが分かれてないとちょっと心配になるな、まあスケーラビリティに自信があるのかも...!:thinking:)
Possible future expansion includes a separate model evaluator, which can be used for pure prediction computation needed for complex models.
将来的な拡張の可能性として、複雑なモデルに必要な純粋な予測計算に使用できるモデル評価者を分けることが考えられます。(予測結果の監視、みたいなコンポーネントのことなのかな...!:thinking:)
For V1, however, this will be included within Sibyl.
ただし、V1ではこれがSibyl内に含まれます。(今後、別のサービスに分けたいって話か...!)

In terms of required functionalities, here were some highlights:
必要な要件に関して、以下は重要なポイントです：


- **Batch predictions**: We should allow each prediction request to contain any variable amount of feature sets to predict on (note: a “feature set” is a set of feature values we want to predict on. A simple way of thinking about this is that a feature set is just an input we want to predict on).
  - バッチ予測：各予測リクエストが予測対象の特徴セットを任意の量含むことを許可すべきです（注：特徴セットとは、私たちが予測したい特徴値の集合です。特徴セットは、私たちが予測したい入力のことだと考えると簡単です）。
  Batch predictions are essential, as they allow client services to send and retrieve 1 to N predictions at once, greatly reducing the number of calls needed.
  **バッチ予測は重要です。なぜなら、クライアントサービスが1からNの予測を一度に送信および取得できるため、必要な呼び出しの回数を大幅に削減できるから**です。
  (「全てのリアルタイム予測を処理し...」と前述されてるから、リアルタイム推論に加えてバッチ推論も選択できる推論サービスである必要がある、って話なのかな...!:thinking:)

- **Shadow predictions**: In addition to making predictions and sending them back to client services, the option to make shadow predictions asynchronously in the background was essential.
    シャドウ予測：予測を行い、それをクライアントサービスに返すことに加えて、**バックグラウンドで非同期にシャドウ予測を行うオプションは不可欠**でした。
    Oftentimes, before finalizing and clamping down on one particular model, teams may have multiple candidate models, and want to test multiple models at once on the same data.   
    多くの場合、特定のモデルを最終決定し固定する前に、チームは複数の候補モデルを持ち、同じデータで複数のモデルを同時にテストしたいと考えます。
    Allowing teams the option to use one model for official predictions, and to asynchronously make predictions on the same data with different models, gives them the flexibility and power to analyze the efficacy of various candidate models.
    チームが公式な予測に1つのモデルを使用し、同じデータに対して異なるモデルで非同期に予測を行うオプションを持つことは、さまざまな候補モデルの有効性を分析するための柔軟性と力を与えます。
    (A/Bテストなどのためなのかな...!:thinking:)
    (あ、どうやら後述されてる test run などのためのシャドウ予測機能っぽい!!:thinking:)

- Feature and model fetching: As mentioned above, Sibyl needs to be able to fetch both features and models from their respective stores.
    特徴とモデルの取得：上記のように、Sibylはそれぞれのストアから特徴とモデルの両方を取得できる必要があります。
    For features, they would be fetched during each prediction, and for models, we could save time and computing power by first fetching all models when the service starts up, then caching them in-memory, eliminating the need to load them for each request.
    特徴については、各予測の際に取得され、**モデルについては、サービスが起動する際にすべてのモデルを最初に取得し、それをメモリにキャッシュすることで、各リクエストのたびにロードする必要を排除し、時間と計算能力を節約できます**。
    (モデルをオンライン更新した場合はどうするんだろ...! まあ他社事例などをみるとバックグラウンドで更新しにいくのかな...!)

<!-- ここまで読んだ! -->

## Implementation: General service overview and decision highlights 実装：一般的なサービスの概要と意思決定のハイライト

To get a general understanding of how the service works, as well as a brief overview of the moving parts of the service, here’s what the lifecycle of a typical request looks like: 
サービスがどのように機能するかを一般的に理解し、サービスの動作部分の簡単な概要を得るために、典型的なリクエストのライフサイクルは次のようになります：

![Figure 2: Lifecycle of a typical request]()

Referencing Figure 2: 
図2を参照：

- 1. The request arrives. 
    リクエストが到着します。

- 2. For each model identified in the request, we grab both the model, as well as the model config (which contains info on that model, such as all required features, default fallback values for features, and model type) from an in-memory cache. 
    リクエストで特定された各モデルについて、モデルとモデル設定（そのモデルに関する情報、必要なすべての特徴、特徴のデフォルトフォールバック値、モデルタイプなどを含む）をメモリ内キャッシュから取得します。

- 3. Then we iterate through the values provided in the request, and find out if there are any missing feature values that were not provided. 
    次に、リクエストで提供された値を反復処理し、提供されていない欠落している特徴値があるかどうかを確認します。
    We do this for all models and all feature sets at once, and store values in a map for easy lookup. 
    これをすべてのモデルとすべての特徴セットに対して一度に行い、簡単に検索できるように値をマップに格納します。

- 4. For all missing features, we attempt to retrieve feature values from the feature store, which is a Redis cache of feature values. 
    すべての欠落している特徴について、特徴値のRedisキャッシュである特徴ストアから特徴値を取得しようとします。
    If they still cannot be found, we set the feature values as the provided default value in the model config. 
    それでも見つからない場合は、モデル設定で提供されたデフォルト値として特徴値を設定します。

- 5. Now that we have all features and all feature values required for predictions, we asynchronously make a prediction for each feature set. 
    予測に必要なすべての特徴とすべての特徴値が揃ったので、非同期で各特徴セットの予測を行います。
    For each shadow model, we also launch an asynchronous coroutine, but don’t wait on the results to finish before continuing. 
    各シャドウモデルについても非同期コルーチンを起動しますが、続行する前に結果が完了するのを待ちません。

- 6. With all predictions made, finally, we construct a response protobuf object, and populate it with the predictions, returning the protobuf back to the client. 
    すべての予測が行われたら、最終的にレスポンスprotobufオブジェクトを構築し、予測でそれを埋めて、protobufをクライアントに返します。

Now I want to highlight some decisions/details we’ve made that were noteworthy: 
ここで、私たちが行った注目すべきいくつかの意思決定や詳細を強調したいと思います：

### Optimizing prediction speed using native API calls ネイティブAPI呼び出しを使用して予測速度を最適化する

The two ML frameworks that Sibyl uses, LightGBM and Pytorch (if you are curious as to why we chose these two, give DoorDash’s ML Platform – The Beginning a quick read), have API frameworks implemented in a variety of different programming languages. 
Sibylが使用する**2つのMLフレームワーク、LightGBMとPytorch**は、さまざまなプログラミング言語で実装されたAPIフレームワークを持っています。（なぜこの2つを選んだのかに興味がある場合は、[DoorDashのMLプラットフォーム - The Beginning](https://doordash.engineering/2020/04/23/doordash-ml-platform-the-beginning/)をざっと読んでみてください）
However, in order to optimize for speed, we decided to store models in their native format, and make prediction calls to these frameworks in C++. 
しかし、**速度を最適化するために、モデルをそのネイティブ形式で保存し、これらのフレームワークにC++で予測呼び出しを行う**ことに決めました。
Working in C++ allowed for us to minimize the latency for making the actual predictions. 
C++で作業することで、実際の予測を行う際のレイテンシを最小限に抑えることができました。
We used the Java Native Interface (JNI) so that the service, implemented in Kotlin, can make the LightGBM and Pytorch prediction calls, implemented in C++. 
私たちはJava Native Interface（JNI）を使用して、**Kotlinで実装されたサービスがC++で実装されたLightGBMおよびPytorchの予測呼び出しを行えるようにしました**。

<!-- ここまで読んだ! -->

### Coroutines, coroutines, and more coroutines  コルーチン、コルーチン、そしてさらにコルーチン

Due to the demanding scalability and latency requirements, one of our top priorities was to make sure that all predictions were being conducted in parallel, and that when waiting for features to be fetched from the feature store, threads would actually be performing computations and calculations (instead of just waiting). 
**要求されるスケーラビリティとレイテンシの要件が厳しいため、私たちの最優先事項の1つは、すべての予測が並行して行われていることを確認し、特徴ストアから特徴を取得するのを待っているときに、スレッドが実際に計算や計算を行っている（ただ待っているのではなく）こと**でした。
Thankfully, developing in Kotlin gave us much needed control over threads via its built-in coroutine implementation. 
幸いなことに、Kotlinでの開発により、組み込みのコルーチン実装を通じてスレッドに対する必要な制御を得ることができました。
Kotlin’s coroutines aren’t tied to a specific thread, and suspend themselves while waiting, meaning that they don’t actually hold the thread, allowing the thread to perform work on something else while waiting. 
Kotlinのコルーチンは特定のスレッドに結びついておらず、待機中に自らをサスペンドするため、実際にはスレッドを保持せず、待機中にスレッドが他の作業を行うことを可能にします。
While it is possible to implement similar behavior in Java using callbacks, syntactically, creating and managing Kotlin coroutines are far cleaner than Java threads, making multithreaded development easy. 
コールバックを使用してJavaで同様の動作を実装することは可能ですが、構文的にはKotlinのコルーチンを作成および管理する方がJavaのスレッドよりもはるかにクリーンであり、マルチスレッド開発を容易にします。

<!-- ここまで読んだ! -->

## Rolling Out: First loading testing, then introducing into production ローリングアウト：最初に負荷テストを行い、その後本番環境に導入

### Conducting a test run テストランの実施

We decided to test Sibyl's prediction capabilities on one of DoorDash's most in-demand services. 
私たちは、Sibylの予測能力をDoorDashの最も需要の高いサービスの1つでテストすることに決めました。
DoorDash’s search service has many responsibilities, one of which includes calculating which restaurants to show you when you visit doordash.com. 
DoorDashの検索サービスは多くの責任を持っており、その1つはdoordash.comを訪れたときにどのレストランを表示するかを計算することです。(ホーム画面でのレストラン推薦?? :thinking:)
You may not realize it, but every single restaurant you see on DoorDash needs to be scored and ranked beforehand, with the score being used to personalize your experience on the site, providing different restaurants in different positions on the site for different people (Figure 3).
あなたは気づかないかもしれませんが、**DoorDashで見るすべてのレストランは事前にスコアリングされ、ランク付けされる必要があります**。このスコアは、サイト上での体験をパーソナライズするために使用され、異なる人々に対して異なる位置に異なるレストランを提供します（図3）。

![Figure 3: The search service’s ranking illustrated]()

Currently, the search service’s ranking logic is done in-house and within the service itself. 
現在、検索サービスのランク付けロジックはin-houseで行われており、サービス自体の中で実行されています。
So what we decided to do was when at any time, the search service was about to rank a restaurant, it would spawn an asynchronous thread that would also call Sibyl. 
そこで、私たちが決定したのは、**検索サービスがレストランをランク付けしようとするたびに、Sibylを呼び出す非同期スレッドを生成すること**でした。(新しい推論サービスを適用する前に、本番システム上で非同期的に一緒に呼び出して非機能要件を満たせるかを検証した、ってことか...!:thinking:)
Doing this gave us the ability to not only verify that the prediction service works as intended, but also allowing us to accurately load test the service. 
これにより、**予測サービスが意図した通りに機能することを確認するだけでなく、サービスを正確に負荷テストすることも可能になりました**。
Furthermore, the asynchronous calls ensured that any calls to Sibyl would not slow down the search service’s endpoints. 
さらに、非同期呼び出しにより、Sibylへの呼び出しが検索サービスのエンドポイントを遅くすることはありませんでした。(本番システムへの悪影響を気にせず、安心して動作確認できる...!!:thinking:)

Sibyl ended up handling over 100,000 predictions per second, wow! 
Sibylは最終的に1秒あたり10万件以上の予測を処理しました、すごいですね！
This test run demonstrated that Sibyl was now ready to handle the throughput required for our production services, and that services at DoorDash could start migrating their models to call the service for any predictions. 
このtest runは、Sibylが私たちの本番サービスに必要なスループットを処理する準備が整ったこと、またDoorDashのサービスが予測のためにモデルをこのサービスに移行し始めることができることを示しました。

### Toggling request batch size and other tuning to optimize the service リクエストバッチサイズの切り替えとサービスを最適化するためのその他の調整

One configuration we played around with was the batch size for each prediction request. 
私たちが試した設定の1つは、各予測リクエストのバッチサイズでした。
Since there are potentially hundreds of stores that can appear on your store feed, the search service actually ranks hundreds of stores as once. 
ストアフィードに表示される可能性のある店舗が数百あるため、検索サービスは実際に数百の店舗を一度にランク付けします。
We were curious to see how much faster each request would be if instead of sending all stores at once to Sibyl, we split the request into sizable chunks, so that instead of predicting on ~1000 stores at once, Sibyl predicted on 50 stores in 20 separate requests. 
私たちは、**すべての店舗を一度にSibylに送信するのではなく、リクエストを適切なサイズのチャンクに分割した場合、各リクエストがどれだけ速くなるかを見たかった**のです。つまり、約1000店舗を一度に予測するのではなく、Sibylが20の別々のリクエストで50店舗を予測するということです。

We found that the optimal chunk size for each request was around 100-200 stores. 
私たちは、各リクエストの最適なチャンクサイズは約100〜200店舗であることを発見しました。
Interestingly, smaller chunk sizes, such as chunks of 10 and 20 stores, actually made latency worse. 
**興味深いことに、10店舗や20店舗のような小さなチャンクサイズは、実際にはレイテンシを悪化させました**。
Therefore, there was a nice middle ground, illustrating that while the number of stores per request mattered, the service performed better when the chunks were decently large in size. 
したがって、リクエストごとの店舗数が重要である一方で、**チャンクが適度に大きいサイズであるとサービスのパフォーマンスが向上する**ことを示す良い中間点がありました。
The hypothesis is that if chunk sizes are too small, then the number of requests increases substantially, resulting in request queuing and higher latencies. 
仮説は、**チャンクサイズが小さすぎるとリクエストの数が大幅に増加し、リクエストのキューイングと高いレイテンシを引き起こすということ**です。(I/Oの回数が増えたことによるレイテンシーの悪化が上回った感じ??:thinking:)
On the other hand, if predictions contain all 1000 stores, then the amount of data to send and receive balloons, and the propagation delay between client and service becomes our bottleneck. 
**一方、予測がすべての1000店舗を含む場合、送受信するデータ量が膨大になり、クライアントとサービス間の伝播遅延がボトルネックになります**。(これもI/O...!)
This finding was actually encouraging for us, as it demonstrated that we efficiently implemented Sibyl to run predictions in parallel, and that on a large-scale, the service is able to make substantial batch predictions without hiccup. 
この発見は実際に私たちにとって励みになりました。なぜなら、私たちがSibylを効率的に実装して**予測を並行して実行できることを**示し、大規模において**サービスが大幅なバッチ予測を問題なく行えること**を示したからです。
(じゃあスコアに基づくレストランのソートは、推論サービスの外で行ってるぽいのかな...! もしくは推論サービスのスコア計算パートのみを並行処理させるのか:thinking:)

Besides chunking, request compression was looked into as well. 
チャンク化に加えて、**リクエストの圧縮**も検討されました。
As mentioned above, one issue with these batch requests is that the sizable amount of data being sent results in large propagation delay times. 
上記のように、**これらのバッチリクエストの1つの問題は、送信されるデータの量が多いために大きな伝播遅延時間が発生すること**です。(うんうん...!:thinking:)
With hundreds of stores and their feature values included in each request, it made sense to try to compress requests in order to reduce the number of packets in the network layer that would need to be sent to Sibyl. 
数百の店舗とそれらの特徴値が各リクエストに含まれているため、Sibylに送信する必要のあるネットワーク層のパケット数を減らすためにリクエストを圧縮することを試みるのは理にかなっていました。
(あれ、特徴量は推論サービスが特徴量ストアから取得するんじゃなかったっけ...??:thinking:)

<!-- ここまで読んだ! --> 

### Finally using the service’s predictions in production サービスの予測を本番環境で使用する

When load testing, although Sibyl would be called every single time a store was ranked, the result returned by the service was never actually used. 
負荷テストの際、Sibylは店舗がランク付けされるたびに呼び出されましたが、サービスから返された結果は実際には使用されませんでした。(うんうん、test runで前述されてた話...!:thinking:)
The next step was to actually use these calculated values and to officially integrate the service’s predictions into the production workflow for various models. 
次のステップは、これらの計算された値を実際に使用し、さまざまなモデルの本番ワークフローにサービスの予測を正式に統合することでした。
While handling requests from our search service was good for load testing, due to very strict latency requirements, it would not be the first few models migrated over. 
私たちの検索サービスからのリクエストを処理することは負荷テストには良かったのですが、非常に厳しいレイテンシ要件のため、最初に移行されるモデルにはなりませんでした。
Furthermore, added time would need to be spent migrating all feature values from the search service to Sibyl’s feature store. 
さらに、検索サービスからSibylのフィーチャーストアにすべての特徴値を移行するために追加の時間が必要になります。
We decided to start with some fraud and dasher pay ML models, the reasons being that the estimated QPS would be far lower, and the latency requirements were not as strict. 
私たちは、**いくつかの詐欺検出およびダッシャーの支払いMLモデルから始めることに決めました。その理由は、推定QPSがはるかに低く、レイテンシ要件がそれほど厳しくなかったから**です。
(QPS = Queries Per Second, 1秒あたりのクエリ数)
(うんうん、まずはユーザ体験への悪影響のリスクが小さいユースケースから移行していく...!:thinking:)
Fraud detection and dasher pay do not need to be calculated nearly as quickly as loading the home page. 
詐欺検出とダッシャーの支払いは、ホームページを読み込むのと同じくらい迅速に計算する必要はありません。
Starting March of this year, both fraud and dasher pay models now officially use Sibyl for predictions. 
今年の3月から、詐欺検出モデルとダッシャーの支払いモデルの両方が正式にSibylを使用して予測を行っています。
Following the rollout, one big win observed was a 3x drop in latency (versus our old prediction service), a testament to Sibyl’s efficacy. 
**ローリングアウト**の後、観察された大きな成果は、レイテンシが3倍低下したこと（以前の予測サービスと比較して）であり、これはSibylの効果を証明するものです。
(やっぱりrollout戦略はいいよね...!!:thinking:)

<!-- ここまで読んだ! -->

### Concluding rolling out: the end of the beginning ローリングアウトの結論：始まりの終わり

Following the successful roll out of the fraud and dasher pay models in using Sibyl for predictions, over the past couple of months, the ML platform team has been continuously adding more and more models to the service, and the migration of models to Sibyl is nearing completion. 
詐欺検出モデルとダッシャーの支払いモデルがSibylを使用して予測を行うことに成功した後、過去数ヶ月間、MLプラットフォームチームはサービスにますます多くのモデルを追加し続けており、モデルのSibylへの移行は完了に近づいています。
All but five models have been migrated and are now calling Sibyl for predictions. 
5つのモデルを除いてすべてが移行され、現在はSibylを呼び出して予測を行っています。
To learn more about their migration check out this new blog post here. 
彼らの移行について詳しく知りたい場合は、[こちらの新しいブログ投稿](https://doordash.engineering/2020/10/01/integrating-a-scoring-framework-into-a-prediction-service/)をチェックしてください。

The team is continuing to add support for different feature and model types. 
チームはさまざまな特徴とモデルタイプのサポートを追加し続けています。
For example, support for embedded features, which are used primarily in neural networks, has been added. 
たとえば、主にニューラルネットワークで使用される埋め込み特徴量のサポートが追加されました。
Composite models, models that consist of a chain of submodels and expressions, called compute nodes, have also been added. 
サブモデルと式のチェーンで構成されるコンポジットモデル（計算ノードと呼ばれるモデル）も追加されました。
Although Sibyl’s role as the predictor for DoorDash has just begun, it has already been an exciting and active one! 
SibylのDoorDashの予測者としての役割はまだ始まったばかりですが、すでに刺激的で活発なものとなっています！
(いろんなモデルを低レイテンシー&高スループットで処理できる推論サーバーってことは、かなりお金かかってそう! GPU付きのインスタンスを複数台稼働させる必要があるはずなので...!:thinking:)

## Acknowledgements 謝辞

Thanks to Param Reddy, Jimmy Zhou, Arbaz Khan, and Eric Gu for your involvement in the development of Sibyl prediction service
Sibyl予測サービスの開発に関与してくださったParam Reddy、Jimmy Zhou、Arbaz Khan、Eric Guに感謝します。

<!-- ここまで読んだ! -->
