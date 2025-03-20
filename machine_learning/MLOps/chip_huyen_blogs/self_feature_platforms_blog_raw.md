# Self-serve feature platforms: architectures and APIs 自己サービス機能プラットフォーム：アーキテクチャとAPI
Jan 8, 2023•Chip Huyen 2023年1月8日•チップ・フユエン

The last few years saw the maturation of a core component of the MLOps stack that has significantly improved the ML production workflows: feature platforms. 
ここ数年で、MLOpsスタックのコアコンポーネントが成熟し、MLプロダクションワークフローが大幅に改善されました：機能プラットフォームです。

A feature platform handles feature engineering, feature computation, and serving computed features for models to use to generate predictions. 
機能プラットフォームは、特徴量エンジニアリング、特徴量計算、およびモデルが予測を生成するために使用する計算された特徴量の提供を処理します。

LinkedIn, for example, mentioned that they’ve deployed Feathr, their feature platform, for dozens of applications at LinkedIn including Search, Feed, and Ads. 
例えば、LinkedInは、検索、フィード、広告を含む数十のアプリケーションに対して、彼らの機能プラットフォームであるFeathrを展開したと述べています。

Their feature platform reduced engineering time required for adding and experimenting with new features from weeks to days, while performed faster than the custom feature processing pipelines that they replaced by as much as 50%. 
彼らの機能プラットフォームは、新しい機能の追加や実験に必要なエンジニアリング時間を数週間から数日へと短縮し、置き換えたカスタム機能処理パイプラインよりも最大50％速く動作しました。

This post consists of two parts. 
この記事は二部構成になっています。

The first part discusses the evolution of feature platforms, how they differ from model platforms and feature stores. 
第一部では、機能プラットフォームの進化、モデルプラットフォームや機能ストアとの違いについて説明します。

The second part discusses the core challenges of making feature platforms self-serve for data scientists and increase the iteration speed for feature engineering. 
第二部では、データサイエンティストが自己サービスで機能プラットフォームを利用できるようにするための主要な課題と、特徴量エンジニアリングの反復速度を向上させる方法について説明します。

If you’re already familiar with feature platforms, you might want to skip Part I. 
すでに機能プラットフォームに精通している場合は、第一部をスキップしたいかもしれません。

To see the a list of public feature platforms referenced for this post, see Comparison of feature platforms. 
この記事で参照されている公開機能プラットフォームのリストについては、「機能プラットフォームの比較」をご覧ください。



## Part I. Evolution of feature platforms 特徴プラットフォームの進化

The need for feature platforms arose when companies moved from batch prediction to online prediction. 
特徴プラットフォームの必要性は、企業がバッチ予測からオンライン予測に移行したときに生じました。

Without a feature platform, online prediction at scale for many use cases would be hard, if not impossible. 
特徴プラットフォームがなければ、多くのユースケースにおける大規模なオンライン予測は困難であり、場合によっては不可能です。

This doesn’t mean that a feature platform can’t support batch prediction. 
これは、特徴プラットフォームがバッチ予測をサポートできないという意味ではありません。

For many companies, a feature platform can be used to support both batch and online prediction. 
多くの企業にとって、特徴プラットフォームはバッチ予測とオンライン予測の両方をサポートするために使用できます。

A challenge for most online prediction use cases is latency, which results from 3 types of latency (excluding network latency): 
ほとんどのオンライン予測ユースケースにとっての課題はレイテンシであり、これは3種類のレイテンシ（ネットワークレイテンシを除く）から生じます：

1. Feature computation latency: time it takes to compute features from raw data. 
   特徴計算レイテンシ：生データから特徴を計算するのにかかる時間です。

   If a model only uses features that have been precomputed, this value will be none during inference. 
   モデルが事前に計算された特徴のみを使用する場合、この値は推論中はゼロになります。

2. Feature retrieval latency: time it takes for the prediction service to retrieve computed features needed to compute prediction. 
   特徴取得レイテンシ：予測サービスが予測を計算するために必要な計算済みの特徴を取得するのにかかる時間です。

3. Prediction computation latency: time it takes for a model to generate a prediction from computed features. 
   予測計算レイテンシ：モデルが計算済みの特徴から予測を生成するのにかかる時間です。

Prediction computation is relatively well-researched, and many tools have been developed to optimize it. 
予測計算は比較的よく研究されており、それを最適化するための多くのツールが開発されています。

Feature platforms are designed to optimize feature computation and feature retrieval, not prediction computation latency. 
特徴プラットフォームは、予測計算レイテンシではなく、特徴計算と特徴取得を最適化するように設計されています。



### Feature platform vs. feature store 特徴プラットフォームと特徴ストア

Since the industry is still new, people might have different opinions, but generally, a feature store is part of a feature platform. 
業界はまだ新しいため、人々は異なる意見を持つかもしれませんが、一般的に特徴ストアは特徴プラットフォームの一部です。

The main goals of a feature store are:
特徴ストアの主な目標は以下の通りです：
1. Reduce feature retrieval latency
1. 特徴取得のレイテンシを削減すること
2. Store computed features for reuse to reduce computation cost: multiple models that need the same feature should be able to reuse that feature without redundant computation.
2. 計算された特徴を再利用のために保存し、計算コストを削減すること：同じ特徴量を必要とする複数のモデルは、冗長な計算なしにその特徴を再利用できるべきです。

In its simplest form, a feature store is a key-value store that stores computed features in-memory. 
最も単純な形では、特徴ストアは計算された特徴をメモリ内に保存するキー-バリュー型ストアです。

Common key-value stores include DynamoDB, Redis, Bigtable. 
一般的なキー-バリュー型ストアには、DynamoDB、Redis、Bigtableが含まれます。

In its moderately more complex form, a feature store also handles persisting feature values on disk so that they can be used for training, ensuring the train-predict consistency.
やや複雑な形では、特徴ストアは特徴値をディスクに永続化することも扱い、トレーニングに使用できるようにし、トレーニングと予測の一貫性を確保します。

Feature platforms handle both feature retrieval and feature computation. 
特徴プラットフォームは、特徴取得と特徴計算の両方を扱います。

The most notable examples of feature platforms are Airbnb’s Chronon (previously Zipline) and LinkedIn’s Feathr (open source).
特徴プラットフォームの最も注目すべき例は、AirbnbのChronon（以前はZipline）とLinkedInのFeathr（オープンソース）です。

Feature stores like Feast, Amazon SageMaker Feature Store, and Vertex AI Feature Store do not handle feature computation, and therefore, are not feature platforms.
Feast、Amazon SageMaker Feature Store、Vertex AI Feature Storeのような特徴ストアは特徴計算を扱わないため、特徴プラットフォームではありません。



### Feature platform vs. model platform 特徴プラットフォームとモデルプラットフォーム

As online prediction use cases mature, we see more and more companies separating their feature platform from their model platform, as they have distinct responsibilities and requirements.
オンライン予測のユースケースが成熟するにつれて、企業は特徴プラットフォームとモデルプラットフォームを分離する傾向が強まっています。これらは異なる責任と要件を持っています。

A model platform concerns how models are packaged and served. It usually consists of three major components:
モデルプラットフォームは、モデルがどのようにパッケージ化され、提供されるかに関するものです。通常、以下の3つの主要なコンポーネントで構成されています。

1. Model deployment API: how to package a trained model (e.g. serialized, versioned, tagged) with necessary dependencies. In many cases, trained models can also be automatically optimized (e.g. quantized). Ideally, model deployment should be self-serve – data scientists should be able to deploy models by themselves instead of handing them off to engineering teams.
   1. モデルデプロイメントAPI：トレーニングされたモデル（例：シリアライズ、バージョン管理、タグ付け）を必要な依存関係と共にパッケージ化する方法。多くの場合、トレーニングされたモデルは自動的に最適化（例：量子化）されることもあります。理想的には、モデルデプロイメントはセルフサービスであるべきであり、データサイエンティストはエンジニアリングチームに渡すのではなく、自分でモデルをデプロイできるべきです。

2. Model registry (model store): responsible for storing and versioning a packaged model to be retrieved for predictions.
   2. モデルレジストリ（モデルストア）：予測のために取得されるパッケージ化されたモデルを保存し、バージョン管理する責任があります。

3. Prediction service: responsible for retrieving models, allocating and scaling resources to generate predictions and to serve them to users.
   3. 予測サービス：モデルを取得し、予測を生成するためにリソースを割り当て、スケーリングし、ユーザーに提供する責任があります。

Note: Experimentation can be considered the fourth piece of the model platform. For many companies, model testing (shadow, A/B testing) is handled by a separate team. However, it’d be a lot easier if data scientists can configure experimentations to evaluate their models in production, and the prediction service can route traffic based on the experimentation configurations.
注：実験はモデルプラットフォームの4つ目の要素と見なすことができます。多くの企業では、モデルテスト（シャドウ、A/Bテスト）は別のチームが担当しています。しかし、データサイエンティストが本番環境でモデルを評価するための実験を設定でき、予測サービスが実験の設定に基づいてトラフィックをルーティングできれば、はるかに簡単になります。

A feature platform concerns the whole feature engineering workflow. A feature platform consists of the following components:
特徴プラットフォームは、全体の特徴エンジニアリングワークフローに関するものです。特徴プラットフォームは以下のコンポーネントで構成されています。

1. Feature API: how data scientists can create, deploy, discover, and experiment with features. Ideally, feature engineering should be self-serve for data scientists, so that they can do their job without having to pair with or wait for data engineers. This can also free data engineers to focus on more interesting work.
   1. フィーチャーAPI：データサイエンティストが特徴を作成、デプロイ、発見、実験する方法。理想的には、特徴エンジニアリングはデータサイエンティストにとってセルフサービスであるべきで、データエンジニアとペアを組んだり、待ったりすることなく仕事を行えるようにするべきです。これにより、データエンジニアはより興味深い作業に集中できるようになります。

2. Feature catalog: a catalog to store feature definitions and metadata, so that users can discover and share features.
   2. フィーチャーカタログ：特徴の定義とメタデータを保存するカタログで、ユーザーが特徴を発見し、共有できるようにします。

3. Computation engines: the engines used to compute features, e.g. Spark, Flink.
   3. 計算エンジン：特徴を計算するために使用されるエンジン（例：Spark、Flink）。

4. Feature store: physical storage of computed feature values.
   4. フィーチャーストア：計算された特徴値の物理ストレージです。

For a company at a reasonable scale, a feature platform is much harder to build than a model platform for the following reasons.
合理的な規模の企業にとって、特徴プラットフォームは以下の理由からモデルプラットフォームよりも構築がはるかに難しいです。

1. Cost. Companies have repeatedly told me that the majority of their infrastructure cost is in feature computation and storage. For an ecommerce or a fintech company of about 10M accounts, feature computation for their anti-fraud use case alone can be between a million and 10 million USD a year.
   1. コスト。企業は繰り返し、インフラコストの大部分が特徴の計算とストレージにあると私に伝えています。約1000万アカウントのeコマースまたはフィンテック企業の場合、彼らの不正防止ユースケースのための特徴計算だけで年間100万から1000万ドルの間になる可能性があります。

2. Cross-team collaboration between data engineers and data scientists. For use cases in computer vision and NLP, features can be computed using a small number of data sources. However, for use cases with tabular data like fraud, recommender system, ETA, dynamic pricing, etc. features are computed from many sources, which require the feature platform to work much more closely with the data platform compared to the model platform.
   2. データエンジニアとデータサイエンティスト間のクロスチームコラボレーション。コンピュータビジョンやNLPのユースケースでは、少数のデータソースを使用して特徴を計算できます。しかし、不正、レコメンダーシステム、ETA、動的価格設定などの表形式データを持つユースケースでは、特徴は多くのソースから計算されるため、特徴プラットフォームはモデルプラットフォームと比較してデータプラットフォームとより密接に連携する必要があります。

3. Iteration speed. Given that there are many features for any given model, the need for a platform that enables data scientists to iterate on features quickly is important. Given the right infrastructure, the number of features can grow rapidly. We’ve seen the total number of features for a company growing 2x to 10x over the last 3 years, up to 10,000s features.
   3. イテレーション速度。特定のモデルに対して多くの特徴があることを考えると、データサイエンティストが特徴を迅速にイテレートできるプラットフォームの必要性は重要です。適切なインフラがあれば、特徴の数は急速に増加する可能性があります。私たちは、ある企業の特徴の総数が過去3年間で2倍から10倍に増加し、数万の特徴に達するのを見てきました。



### Types of features a feature platform can compute 特徴プラットフォームが計算できる特徴の種類

For a feature platform to handle feature computation, it’s important to consider what types of computation it can, or should handle. 
特徴プラットフォームが特徴計算を処理するためには、どのような計算を処理できるか、または処理すべきかを考慮することが重要です。

In general, companies divide feature computation into three different categories:
一般的に、企業は特徴計算を3つの異なるカテゴリに分けます：
1. Batch features
2. Real-time (RT) features
3. Near real-time (NRT) features

Each of these feature types require different ways to ingest data and different computation engines. 
これらの各特徴タイプは、データを取り込むための異なる方法と異なる計算エンジンを必要とします。

Which feature types you need depend on your use cases, business logic, and latency requirements. 
必要な特徴タイプは、使用ケース、ビジネスロジック、およびレイテンシ要件に依存します。

We’ve seen an increasing number of use cases that require all three feature types. 
私たちは、**すべての3つの特徴タイプを必要とする使用ケースが増加している**のを見てきました。

For a detailed analysis of these three different feature types, see Appendix: Batch features vs. real-time features vs. near real-time features.
これらの3つの異なる特徴タイプの詳細な分析については、付録：バッチ特徴とリアルタイム特徴と近リアルタイム特徴を参照してください。

- Stale features
- Wasted computation
- Fresh features
- Scalable
- Easy to set up
- Fresh features

*The latency gap between real-time and near real-time features is closing, as near real-time feature computation is becoming faster as better streaming technology matures.
*リアルタイム特徴と近リアルタイム特徴の間のレイテンシギャップは縮小しており、近リアルタイム特徴計算は、より良いストリーミング技術が成熟するにつれて速くなっています。

Not all feature platforms can or should handle all feature types. 
すべての特徴プラットフォームがすべての特徴タイプを処理できるわけではなく、また処理すべきでもありません。
For example, Robinhood’s feature platform, as of 2021, only handles batch features and real-time features. 
例えば、Robinhoodの特徴プラットフォームは2021年現在、バッチ特徴とリアルタイム特徴のみを処理しています。
They’re not yet supporting near real-time features, but it’s on their roadmap. 
彼らはまだ近リアルタイム特徴をサポートしていませんが、それは彼らのロードマップにあります。

Real-time features might be sufficient for a smaller scale and simple online prediction use cases. 
リアルタイム特徴は、小規模でシンプルなオンライン予測使用ケースには十分かもしれません。
However, it’s hard to optimize for latency and cost for real-time features, especially as the prediction traffic fluctuates or grows, and the complexity of features increases.
しかし、特に予測トラフィックが変動したり増加したりし、特徴の複雑さが増す中で、リアルタイム特徴のレイテンシとコストを最適化するのは難しいです。
As a company onboards more online prediction use cases and their online feature space grows, supporting near real-time features is essential.
企業がより多くのオンライン予測使用ケースを導入し、オンライン特徴空間が拡大するにつれて、近リアルタイム特徴をサポートすることが不可欠です。

A year ago, I discussed in the post Real-time machine learning: challenges and solutions that most companies moving batch prediction to online prediction do so in two major steps:
1年前、私は「リアルタイム機械学習：課題と解決策」で、**バッチ予測をオンライン予測に移行するほとんどの企業が2つの主要なステップで行う**ことを議論しました：

1. Re-architect their prediction service to support online prediction, still using only batch features.
   バッチ特徴量のみを使うオンライン予測をサポートするように予測サービスを再設計する。
2. Re-architect their feature platform to support streaming features.
   ストリーミング機能をサポートするように特徴量プラットフォームを再設計する。

<!-- ここまで読んだ! -->

Since then, I’ve observed this pattern at multiple companies. 
それ以来、私は複数の企業でこのパターンを観察してきました。
For example, Instacart discussed their two-step transitions from batch to online prediction in Lessons Learned: The Journey to Real-Time Machine Learning at Instacart. 
例えば、Instacartは「Lessons Learned: The Journey to Real-Time Machine Learning at Instacart」でバッチからオンライン予測への2段階の移行について議論しました。(あ、これ読んだな...!:thinking_face:)
DoorDash’s head of ML infra Hien Luu advised that, in the journey to build out an ML platform, companies should start small, and DoorDash started with their high throughput, low latency prediction service Sybil (2020). 
DoorDashのMLインフラの責任者であるHien Luuは、MLプラットフォームを構築する過程で、**企業は小さく始めるべき**だとアドバイスし、DoorDashは高スループット、低レイテンシの予測サービスSybil（2020）から始めました。
(たぶんこれの話: https://careersatdoordash.com/blog/doordashs-new-prediction-service/)
After that, they introduced their feature platform Riviera (2021), then Fabricator (2022). 
その後、彼らは特徴量プラットフォームRiviera（2021）を導入し、次にFabricator（2022）を導入しました。

<!-- ここまで読んだ! -->

## Part 2. Self-serve feature engineering  
## パート2. セルフサービス機能エンジニアリング  

### Challenge: slow iteration speed for streaming features  
### 課題: ストリーミング機能の遅い反復速度  

Workflows for batch features are well understood – data scientists are familiar with the process of using tools like pandas, Spark.  
バッチ機能のワークフローはよく理解されており、データサイエンティストはpandasやSparkのようなツールを使用するプロセスに精通しています。  
Workflows for streaming features, however, still have much to desire for.  
しかし、ストリーミング機能のワークフローにはまだ多くの改善の余地があります。  

Even the household-name companies with high MLOps maturity we’ve interviewed have challenges with the iteration speed for streaming features.  
私たちがインタビューしたMLOpsの成熟度が高い有名企業でさえ、ストリーミング機能の反復速度に関する課題を抱えています。  
The long iteration cycle for streaming features discourages data scientists from working with them, even if these features seem to show a lot of promise.  
ストリーミング機能の長い反復サイクルは、これらの機能が多くの可能性を示しているように見えても、データサイエンティストがそれらに取り組むことを思いとどまらせます。  
One of their data scientists told us that: “Instead of spending a quarter struggling with a streaming feature, I’d rather experiment with 10 batch features.”  
**彼らのデータサイエンティストの一人は、「ストリーミング特徴量に苦労するために四半期を費やすよりも、10のバッチ特徴量を試してみたい」と私たちに語りました。** 
(環境によっては、圧倒的にバッチの特徴量パイプラインの方が開発・改善のiterationを回しやすい → 結果としてバッチシステムの方がMLの成果をスケールさせやすい、という考え方もあるかも...??:thinking_face:)
(ただまあこのあたりのどちらが良いかは、結局MLを使うドメインやユースケースによるんだろうな。リアルタイムやストリーミング特徴量の有効性がバッチのiteration回しやすさを上回る場合もあるだろうし...!:thinking_face:)

We categorized the causes for the slow iteration speed into two buckets: lack of data scientist-friendly API, and lack of functionality for fast experimentation.
私たちは、遅い反復速度の原因を2つのカテゴリに分類しました: データサイエンティストに優しいAPIの欠如と、迅速な実験のための機能の欠如です。

<!-- ここまで読んだ! -->

### 1. Feature API

Streaming is a concept from the infrastructure world. 
ストリーミングはインフラの世界からの概念です。
True streaming engines like Flink are built on top of JVM, a place most data scientists aren’t acquainted with. 
Flinkのような真のストリーミングエンジンはJVMの上に構築されており、ほとんどのデータサイエンティストはこの環境に精通していません。
This fact is, unfortunately, often dismissed by the infra engineers who build feature platforms. 
この事実は、残念ながら、フィーチャープラットフォームを構築するインフラエンジニアによってしばしば無視されます。

#### Scala or Scala-inspired interface

We’ve seen early generations of feature platforms adopt a Scala or Kotlin interface. 
私たちは、初期のフィーチャープラットフォームがScalaまたはKotlinインターフェースを採用しているのを見てきました。
The image below is just some examples. 
以下の画像はその一例です。
When I ask infra engineers if they find Scala API to be a challenge for users to adopt, the answer is usually no – “data scientists are engineers, they can learn a new language.” 
インフラエンジニアにScala APIがユーザにとって採用の課題だと思うか尋ねると、通常の答えは「いいえ」です。「データサイエンティストはエンジニアですから、新しい言語を学ぶことができます。」
When I ask the same questions to data scientists, the answer is usually yes. 
同じ質問をデータサイエンティストにすると、通常の答えは「はい」です。
Many companies that have adopted a Scala interface. 
Scalaインターフェースを採用している企業は多くあります。

#### SQL interface

Our impression, from talking with our colleagues in streaming, is that there’s a consensus that SQL is inevitable. 
ストリーミングの同僚と話して得た印象は、SQLが避けられないという合意があるということです。
Almost all streaming engines have introduced their own SQL interfaces (see Flink SQL, KSQL, Dataflow SQL). 
ほとんどすべてのストリーミングエンジンは独自のSQLインターフェースを導入しています（Flink SQL、KSQL、Dataflow SQLを参照）。
Some feature platforms, therefore, adopt SQL. 
したがって、一部のフィーチャープラットフォームはSQLを採用しています。

DoorDash, Snap, Gojek are some of the companies that originally adopted SQL for their feature APIs. The SQL part is the transformation. The rest is feature config in YAML or JSON.
DoorDash、Snap、Gojekは、元々フィーチャーAPIにSQLを採用していた企業の一部です。SQL部分は変換です。残りはYAMLまたはJSONでのフィーチャー設定です。

If a company goes with SQL, the next question is which SQL dialect to support. 
もし企業がSQLを選択する場合、次の質問はどのSQL方言をサポートするかです。
Some companies use Flink SQL directly as their feature API. 
一部の企業はFlink SQLを直接フィーチャーAPIとして使用しています。
In the image above, DoorDash seems to be using Flink SQL. 
上の画像では、DoorDashがFlink SQLを使用しているようです。
Snap uses Spark SQL, but the example given is too simple to determine the time semantics they support. 
SnapはSpark SQLを使用していますが、示された例は彼らがサポートする時間セマンティクスを判断するにはあまりにも単純です。

Using SQL directly as an API, however, has certain drawbacks: 
しかし、SQLをAPIとして直接使用することにはいくつかの欠点があります：

1. Insufficient time semantics, such as different window types for aggregations (e.g. tumbling / hopping / sessionization window) and point-in-time joins. 
   集約のための異なるウィンドウタイプ（例：タムブリングウィンドウ、ホッピングウィンドウ、セッション化ウィンドウ）やポイントインタイム結合など、時間セマンティクスが不十分です。
2. Lack of composability. Feature pipelines can be complex. We need a language that allows building small pieces of logic independently and stitching them together, while making the pieces reusable.
   組み合わせの欠如。特徴パイプラインは複雑になります。小さなロジックの部分を独立して構築し、それらを繋ぎ合わせることができる言語が必要です。同時に、それらの部分を再利用可能にする必要があります。

#### Python interface

While SQL is increasingly gaining popularity with data scientists, Python is still the lingua franca of data science. 
SQLはデータサイエンティストの間でますます人気を集めていますが、Pythonは依然としてデータサイエンスの共通言語です。
In the last couple of years, both LinkedIn and Airbnb switched to a Python interface for their feature API. 
ここ数年で、**LinkedInとAirbnbの両方がフィーチャーAPIのためにPythonインターフェースに切り替えました**。(まあPython Interfaceがあると使いやすいよなぁ。まあSQLで一旦S3にunloadさせてからPythonで取得するのでも良いけど...!:thinking:)

LinkedIn and Airbnb are some of the companies that have switched to Python for their feature APIs.
LinkedInとAirbnbは、フィーチャーAPIにPythonを採用した企業の一部です。

Note that while Feathr supports streaming processing, it does NOT support streaming aggregations. 
Feathrがストリーミング処理をサポートしている一方で、ストリーミング集約はサポートしていないことに注意してください。

#### Considerations for feature APIs 

##### One-off batch computation vs. ongoing stream computation  一回限りのバッチ計算と継続的なストリーム計算

If you compute your feature on fixed batch data like a CSV file, it’s a one-off job. 
CSVファイルのような固定バッチデータでフィーチャーを計算する場合、それは一回限りのジョブです。
If you compute your feature on an incoming stream of data, the value needs to be continually computed with new values, which makes it a long-running job. 
もし、到着するデータのストリームでフィーチャーを計算する場合、その値は新しい値で継続的に計算される必要があり、これが長時間実行されるジョブになります。
After you’ve written a streaming feature logic, executing this logic requires starting a long-running job. 
ストリーミングフィーチャーロジックを書いた後、このロジックを実行するには長時間実行されるジョブを開始する必要があります。
Data scientists, who are used to working with notebooks, might find executing and maintaining long-running jobs challenging. 
ノートブックで作業することに慣れているデータサイエンティストは、長時間実行されるジョブの実行と維持が難しいと感じるかもしれません。

Because the outputs of streaming feature computation are continually generated, we need to write them somewhere. 
ストリーミングフィーチャー計算の出力が継続的に生成されるため、それらをどこかに書き込む必要があります。
Figuring out where to write to and configuring an output schema with the correctly-formatted keys to match existing data tables can also be challenging. 
どこに書き込むかを決定し、既存のデータテーブルに一致するように正しくフォーマットされたキーを持つ出力スキーマを設定することも難しい場合があります。

It’d be ideal if the feature API backend also handles starting streaming jobs and output schemas. 
フィーチャーAPIのバックエンドがストリーミングジョブの開始と出力スキーマの処理も行うことが理想的です。

<!-- ここまで読んだ! -->

##### Design decision: separation of transformation logic and feature logic  設計の決定：変換ロジックとフィーチャーロジックの分離

Transformationとは、データに適用される関数を指します：例として、製品ビューのカウント、取引価値の平均などがあります。
A feature consists of a transformation, sources (where to apply this transformation on), and sinks (where to write the computed feature values to). 
フィーチャーは、変換、ソース（この変換を適用する場所）、およびシンク（計算されたフィーチャー値を書き込む場所）で構成されます。
Transformation logic and feature logic don’t have to be written in the same language. 
変換ロジックとフィーチャーロジックは同じ言語で書く必要はありません。

For both DoorDash and Snap, transformation logic is in SQL, but feature logic is configured in YAML. 
DoorDashとSnapの両方では、変換ロジックはSQLで記述されていますが、フィーチャーロジックはYAMLで設定されています。
For Feathr and Airbnb, both transformation logic and feature logic are in Python. 
FeathrとAirbnbでは、変換ロジックとフィーチャーロジックの両方がPythonで記述されています。

The separation of transformation and feature serves two purposes: 
変換とフィーチャーの分離は二つの目的を果たします：
It allows the reuse of transformation logic. 
それは変換ロジックの再利用を可能にします。
For example, the same transformation can be applied to different sources to create different features. 
例えば、同じ変換を異なるソースに適用して異なるフィーチャーを作成することができます。
It creates a clean abstraction that allows different personas to work together. 
それは異なるペルソナが一緒に作業できるクリーンな抽象を作成します。
For example, data scientists can focus on creating transformations, and if they need help configuring the long-running jobs to compute their streaming features, they can collaborate with data engineers on feature configuration. 
例えば、データサイエンティストはtransformの作成に集中でき、ストリーミングフィーチャーを計算するための長時間実行されるジョブの設定に助けが必要な場合、フィーチャー設定に関してデータエンジニアと協力することができます。

<!-- ここまで読んだ! -->

### 2. Functionality for fast experimentation 迅速な実験のための機能

In this section, we’ll discuss the functionalities that can significantly speed up iteration for streaming features.  
このセクションでは、ストリーミング機能の反復を大幅に加速できる機能について説明します。

#### Data discoverability and governance データの発見可能性とガバナンス

- Feature discoverability: Say, you have a new idea for a streaming feature to be used for your model. Because feature computation and storage are expensive, the first thing you might want to do is to see whether that feature is already being used by another model or another team, so that you can reuse it.  
   特徴の発見可能性：たとえば、モデルに使用するための新しいストリーミング機能のアイデアがあるとします。特徴の計算とストレージが高価であるため、**最初にやりたいことは、その特徴がすでに他のモデルや他のチームで使用されているかどうかを確認して、再利用できるかどうかを確認すること**です。
- Source discoverability: You might want to see if this feature is actually feasible given your data setup. You might want to look up what sources are available.  
  ソースの発見可能性：この機能が実際にあなたのデータセットに対して実現可能かどうかを確認したいかもしれません。どのソースが利用可能かを調べたいかもしれません。
- Data governance: Talking about data discoverability, it’s important to consider that some data is sensitive and shouldn’t be accessible by everyone.  It’s important to:  
   データガバナンス：データの発見可能性について話すと、いくつかのデータは機密性があり、誰でもアクセスできるべきではないことを考慮することが重要です。重要なことは以下の通りです：
  - Assign roles to users and configure which data should be accessible by which roles. ユーザーに役割を割り当て、どのデータがどの役割にアクセス可能であるべきかを設定します。  
  - Automate masking of sensitive, PII data.  機密性のある個人識別情報（PII）データのマスキングを自動化します。  
  - Propagate data policy – if a feature is derived from a sensitive column, it should also be marked as sensitive.  データポリシーを伝播させること – 機能が機密列から派生している場合、それも機密としてマークされるべきです。

#### Automated backfills 自動バックフィル

Since you don’t know if this feature is helpful yet, you don’t want to deploy it to your feature store, say Redis, because it might incur high cost.  
この特徴量が役立つかどうかわからないため、Redisなどのフィーチャーストアにデプロイしたくありません。なぜなら、高コストがかかる可能性があるからです。  
You want to be able to experiment with it locally first.  
まずはローカルで実験できるようにしたいです。  
You want to train your model using this feature to see if it actually helps your model.  
この特徴量を使用してモデルをトレーニングし、それが実際にモデルに役立つかどうかを確認したいです。
Generating historical values for this streaming feature so that you can experiment with it is called backfilling.  
このストリーミング特徴量の実験ができるように**過去の履歴値を生成することをバックフィリング**と呼びます。(あ、これがbackfillの定義か!:thinking_face:)
Backfilling for streaming features is hard, as it requires point-in-time correctness.  
ストリーミング機能のバックフィリングは難しく、時点の正確性が必要です。  
For more information on time travel and backfilling, see Introduction to streaming for data scientists.  
タイムトラベルとバックフィリングに関する詳細は、「データサイエンティストのためのストリーミング入門」を参照してください。

In a talk in December 2021, Spotify mentioned 3 killer features for fast iteration that they wish they had.  
2021年12月の講演で、Spotifyは彼らが持っていたかった迅速な反復のための3つのキラーフィーチャーについて言及しました。  
The second point is automated backfills.  
2つ目のポイントは自動バックフィルです。  
[The two other points are point-in-time joins and streaming ingestion, which deserve their own blog post].  
[他の2つのポイントは、時点結合とストリーミング取り込みであり、それぞれ独自のブログ投稿に値します。]
  
### Reference feature platforms 特徴量プラットフォームに関する参考文献たち (必要に応じて読むと良さそう!:thinking_face:)

- [2018]Paypal:Data Pipelines for Real-Time Fraud Prevention at Scale(Mikhail Kourjanski)Airbnb:Zipline—Airbnb’s Declarative Feature Engineering Framework(Nikhil Simha and Varant Zanoyan)Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- [2018]Paypal:スケールでのリアルタイム詐欺防止のためのデータパイプライン(Mikhail Kourjanski)Airbnb:Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(Nikhil SimhaとVarant Zanoyan)Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Paypal:Data Pipelines for Real-Time Fraud Prevention at Scale(Mikhail Kourjanski)  
- Paypal:スケールでのリアルタイム詐欺防止のためのデータパイプライン(Mikhail Kourjanski)  
- Airbnb:Zipline—Airbnb’s Declarative Feature Engineering Framework(Nikhil Simha and Varant Zanoyan)Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Airbnb:Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(Nikhil SimhaとVarant Zanoyan)Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- [2019]Stripe:Reproducible Machine Learning with Functional Programming(Oscar Boykin)Uber:Michelangelo Palette: A Feature Engineering Platform at Uber(Amit Nene)Pinterest:Big Data Machine Learning Platform at Pinterest(Yongsheng Wu)  
- [2019]Stripe:関数型プログラミングによる再現可能な機械学習(Oscar Boykin)Uber:Michelangelo Palette: Uberの特徴エンジニアリングプラットフォーム(Amit Nene)Pinterest:Pinterestのビッグデータ機械学習プラットフォーム(Yongsheng Wu)  
- Stripe:Reproducible Machine Learning with Functional Programming(Oscar Boykin)  
- Stripe:関数型プログラミングによる再現可能な機械学習(Oscar Boykin)  
- Uber:Michelangelo Palette: A Feature Engineering Platform at Uber(Amit Nene)  
- Uber:Michelangelo Palette: Uberの特徴エンジニアリングプラットフォーム(Amit Nene)  
- Pinterest:Big Data Machine Learning Platform at Pinterest(Yongsheng Wu)  
- Pinterest:Pinterestのビッグデータ機械学習プラットフォーム(Yongsheng Wu)  
- [2020]Meta:F3: Next-generation Feature Framework at Facebook(David Chung & Qiao Yang)“Facebook’s Feature Store”(Jun Wan, 2021)Criteo:Building FeatureFlow, Criteo’s feature data generation platform(Piyush Narang)  
- [2020]Meta:F3: Facebookの次世代特徴フレームワーク(David Chung & Qiao Yang)“Facebookの特徴ストア”(Jun Wan, 2021)Criteo:FeatureFlowの構築、Criteoの特徴データ生成プラットフォーム(Piyush Narang)  
- Meta:F3: Next-generation Feature Framework at Facebook(David Chung & Qiao Yang)“Facebook’s Feature Store”(Jun Wan, 2021)  
- Meta:F3: Facebookの次世代特徴フレームワーク(David Chung & Qiao Yang)“Facebookの特徴ストア”(Jun Wan, 2021)  
- “Facebook’s Feature Store”(Jun Wan, 2021)  
- “Facebookの特徴ストア”(Jun Wan, 2021)  
- Criteo:Building FeatureFlow, Criteo’s feature data generation platform(Piyush Narang)  
- Criteo:FeatureFlowの構築、Criteoの特徴データ生成プラットフォーム(Piyush Narang)  
- [2021]DoorDash:Building Riviera: A Declarative Real-Time Feature Engineering Framework(Allen Wang & Kunal Shah)Spotify:Jukebox : Spotify’s Feature Infrastructure(Aman Khan & Daniel Kristjansson)Pinterest:“Streamlining the Pinterest ML Feature Ecosystem”(Se Won Jang & Sihan Wang)  
- [2021]DoorDash:リビエラの構築: 宣言型リアルタイム特徴エンジニアリングフレームワーク(Allen Wang & Kunal Shah)Spotify:Jukebox : Spotifyの特徴インフラ(Aman Khan & Daniel Kristjansson)Pinterest:“Pinterest ML特徴エコシステムの合理化”(Se Won Jang & Sihan Wang)  
- DoorDash:Building Riviera: A Declarative Real-Time Feature Engineering Framework(Allen Wang & Kunal Shah)  
- DoorDash:リビエラの構築: 宣言型リアルタイム特徴エンジニアリングフレームワーク(Allen Wang & Kunal Shah)  
- Spotify:Jukebox : Spotify’s Feature Infrastructure(Aman Khan & Daniel Kristjansson)  
- Spotify:Jukebox : Spotifyの特徴インフラ(Aman Khan & Daniel Kristjansson)  
- Pinterest:“Streamlining the Pinterest ML Feature Ecosystem”(Se Won Jang & Sihan Wang)  
- Pinterest:“Pinterest ML特徴エコシステムの合理化”(Se Won Jang & Sihan Wang)  
- [2022]LinkedIn:Open sourcing Feathr – LinkedIn’s feature store for productive machine learning(David Stein)DoorDash:Introducing Fabricator: A Declarative Feature Engineering Framework(Kunal Shah). Fabricator subsumes DoorDash’s previous declarative feature engineering framework Riviera.Snap:Speed Up Feature Engineering for Recommendation SystemsInstacart:Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)Coupang Eats:Eats data platform: Empowering businesses with data(Fred Fu, Coupang 2022)Airbnb:Chronon - Airbnb’s Feature Engineering Framework(Nikhil Simha). Zipline matured into Chronon, with improved APIs. Chronon is not yet open source.  
- [2022]LinkedIn:Feathrのオープンソース化 – LinkedInの生産的機械学習のための特徴ストア(David Stein)DoorDash:Fabricatorの紹介: 宣言型特徴エンジニアリングフレームワーク(Kunal Shah)。FabricatorはDoorDashの以前の宣言型特徴エンジニアリングフレームワークリビエラを包含します。Snap:推薦システムのための特徴エンジニアリングのスピードアップInstacart:学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)Coupang Eats:Eatsデータプラットフォーム: データでビジネスを強化(Fred Fu, Coupang 2022)Airbnb:Chronon - Airbnbの特徴エンジニアリングフレームワーク(Nikhil Simha)。ZiplineはChrononに成熟し、APIが改善されました。Chrononはまだオープンソースではありません。  
- LinkedIn:Open sourcing Feathr – LinkedIn’s feature store for productive machine learning(David Stein)  
- LinkedIn:Feathrのオープンソース化 – LinkedInの生産的機械学習のための特徴ストア(David Stein)  
- DoorDash:Introducing Fabricator: A Declarative Feature Engineering Framework(Kunal Shah). Fabricator subsumes DoorDash’s previous declarative feature engineering framework Riviera.  
- DoorDash:Fabricatorの紹介: 宣言型特徴エンジニアリングフレームワーク(Kunal Shah)。FabricatorはDoorDashの以前の宣言型特徴エンジニアリングフレームワークリビエラを包含します。  
- Snap:Speed Up Feature Engineering for Recommendation Systems  
- Snap:推薦システムのための特徴エンジニアリングのスピードアップ  
- Instacart:Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)  
- Instacart:学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)  
- Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)  
- 学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)  
- Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)  
- Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)  
- Coupang Eats:Eats data platform: Empowering businesses with data(Fred Fu, Coupang 2022)  
- Coupang Eats:Eatsデータプラットフォーム: データでビジネスを強化(Fred Fu, Coupang 2022)  
- Airbnb:Chronon - Airbnb’s Feature Engineering Framework(Nikhil Simha). Zipline matured into Chronon, with improved APIs. Chronon is not yet open source.  
- Airbnb:Chronon - Airbnbの特徴エンジニアリングフレームワーク(Nikhil Simha)。ZiplineはChrononに成熟し、APIが改善されました。Chrononはまだオープンソースではありません。  
- Binance:Using MLOps to Build a Real-time End-to-End Machine Learning PipelineA Closer Look at Our Machine Learning Feature Store  
- Binance:リアルタイムエンドツーエンド機械学習パイプラインを構築するためのMLOpsの使用私たちの機械学習特徴ストアの詳細な見方  
- Using MLOps to Build a Real-time End-to-End Machine Learning Pipeline  
- リアルタイムエンドツーエンド機械学習パイプラインを構築するためのMLOpsの使用  
- A Closer Look at Our Machine Learning Feature Store  
- 私たちの機械学習特徴ストアの詳細な見方  
- Gojek:Feature Engineering at Scale with Dagger and Feast(Ravi Suhag)  
- Gojek:ダガーとフィーストを用いたスケールでの特徴エンジニアリング(Ravi Suhag)  
- Faire:Building Faire’s new marketplace ranking infrastructure(Sam Kenny)  
- Faire:Faireの新しいマーケットプレイスランキングインフラの構築(Sam Kenny)  
- Paypal:Data Pipelines for Real-Time Fraud Prevention at Scale(Mikhail Kourjanski)  
- Paypal:スケールでのリアルタイム詐欺防止のためのデータパイプライン(Mikhail Kourjanski)  
- Airbnb:Zipline—Airbnb’s Declarative Feature Engineering Framework(Nikhil Simha and Varant Zanoyan)Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Airbnb:Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(Nikhil SimhaとVarant Zanoyan)Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Stripe:Reproducible Machine Learning with Functional Programming(Oscar Boykin)  
- Stripe:関数型プログラミングによる再現可能な機械学習(Oscar Boykin)  
- Uber:Michelangelo Palette: A Feature Engineering Platform at Uber(Amit Nene)  
- Uber:Michelangelo Palette: Uberの特徴エンジニアリングプラットフォーム(Amit Nene)  
- Pinterest:Big Data Machine Learning Platform at Pinterest(Yongsheng Wu)  
- Pinterest:Pinterestのビッグデータ機械学習プラットフォーム(Yongsheng Wu)  
- Meta:F3: Next-generation Feature Framework at Facebook(David Chung & Qiao Yang)“Facebook’s Feature Store”(Jun Wan, 2021)  
- Meta:F3: Facebookの次世代特徴フレームワーク(David Chung & Qiao Yang)“Facebookの特徴ストア”(Jun Wan, 2021)  
- “Facebook’s Feature Store”(Jun Wan, 2021)  
- “Facebookの特徴ストア”(Jun Wan, 2021)  
- Criteo:Building FeatureFlow, Criteo’s feature data generation platform(Piyush Narang)  
- Criteo:FeatureFlowの構築、Criteoの特徴データ生成プラットフォーム(Piyush Narang)  
- “Facebook’s Feature Store”(Jun Wan, 2021)  
- “Facebookの特徴ストア”(Jun Wan, 2021)  
- DoorDash:Building Riviera: A Declarative Real-Time Feature Engineering Framework(Allen Wang & Kunal Shah)  
- DoorDash:リビエラの構築: 宣言型リアルタイム特徴エンジニアリングフレームワーク(Allen Wang & Kunal Shah)  
- Spotify:Jukebox : Spotify’s Feature Infrastructure(Aman Khan & Daniel Kristjansson)  
- Spotify:Jukebox : Spotifyの特徴インフラ(Aman Khan & Daniel Kristjansson)  
- Pinterest:“Streamlining the Pinterest ML Feature Ecosystem”(Se Won Jang & Sihan Wang)  
- Pinterest:“Pinterest ML特徴エコシステムの合理化”(Se Won Jang & Sihan Wang)  
- LinkedIn:Open sourcing Feathr – LinkedIn’s feature store for productive machine learning(David Stein)  
- LinkedIn:Feathrのオープンソース化 – LinkedInの生産的機械学習のための特徴ストア(David Stein)  
- DoorDash:Introducing Fabricator: A Declarative Feature Engineering Framework(Kunal Shah). Fabricator subsumes DoorDash’s previous declarative feature engineering framework Riviera.  
- DoorDash:Fabricatorの紹介: 宣言型特徴エンジニアリングフレームワーク(Kunal Shah)。FabricatorはDoorDashの以前の宣言型特徴エンジニアリングフレームワークリビエラを包含します。  
- Snap:Speed Up Feature Engineering for Recommendation Systems  
- Snap:推薦システムのための特徴エンジニアリングのスピードアップ  
- Instacart:Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)  
- Instacart:学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)  
- Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)  
- 学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)  
- Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)  
- Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)  
- Coupang Eats:Eats data platform: Empowering businesses with data(Fred Fu, Coupang 2022)  
- Coupang Eats:Eatsデータプラットフォーム: データでビジネスを強化(Fred Fu, Coupang 2022)  
- Airbnb:Chronon - Airbnb’s Feature Engineering Framework(Nikhil Simha). Zipline matured into Chronon, with improved APIs. Chronon is not yet open source.  
- Airbnb:Chronon - Airbnbの特徴エンジニアリングフレームワーク(Nikhil Simha)。ZiplineはChrononに成熟し、APIが改善されました。Chrononはまだオープンソースではありません。  
- Binance:Using MLOps to Build a Real-time End-to-End Machine Learning PipelineA Closer Look at Our Machine Learning Feature Store  
- Binance:リアルタイムエンドツーエンド機械学習パイプラインを構築するためのMLOpsの使用私たちの機械学習特徴ストアの詳細な見方  
- Using MLOps to Build a Real-time End-to-End Machine Learning Pipeline  
- リアルタイムエンドツーエンド機械学習パイプラインを構築するためのMLOpsの使用  
- A Closer Look at Our Machine Learning Feature Store  
- 私たちの機械学習特徴ストアの詳細な見方  
- Gojek:Feature Engineering at Scale with Dagger and Feast(Ravi Suhag)  
- Gojek:ダガーとフィーストを用いたスケールでの特徴エンジニアリング(Ravi Suhag)  
- Faire:Building Faire’s new marketplace ranking infrastructure(Sam Kenny)  
- Faire:Faireの新しいマーケットプレイスランキングインフラの構築(Sam Kenny)  
- Paypal:Data Pipelines for Real-Time Fraud Prevention at Scale(Mikhail Kourjanski)  
- Paypal:スケールでのリアルタイム詐欺防止のためのデータパイプライン(Mikhail Kourjanski)  
- Airbnb:Zipline—Airbnb’s Declarative Feature Engineering Framework(Nikhil Simha and Varant Zanoyan)Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Airbnb:Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(Nikhil SimhaとVarant Zanoyan)Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Zipline—Airbnb’s Declarative Feature Engineering Framework(2019)  
- Zipline—Airbnbの宣言型特徴エンジニアリングフレームワーク(2019)  
- Stripe:Reproducible Machine Learning with Functional Programming(Oscar Boykin)  
- Stripe:関数型プログラミングによる再現可能な機械学習(Oscar Boykin)  
- Uber:Michelangelo Palette: A Feature Engineering Platform at Uber(Amit Nene)  
- Uber:Michelangelo Palette: Uberの特徴エンジニアリングプラットフォーム(Amit Nene)  
- Pinterest:Big Data Machine Learning Platform at Pinterest(Yongsheng Wu)  
- Pinterest:Pinterestのビッグデータ機械学習プラットフォーム(Yongsheng Wu)  
- Meta:F3: Next-generation Feature Framework at Facebook(David Chung & Qiao Yang)“Facebook’s Feature Store”(Jun Wan, 2021)  
- Meta:F3: Facebookの次世代特徴フレームワーク(David Chung & Qiao Yang)“Facebookの特徴ストア”(Jun Wan, 2021)  
- “Facebook’s Feature Store”(Jun Wan, 2021)  
- “Facebookの特徴ストア”(Jun Wan, 2021)  
- Criteo:Building FeatureFlow, Criteo’s feature data generation platform(Piyush Narang)  
- Criteo:FeatureFlowの構築、Criteoの特徴データ生成プラットフォーム(Piyush Narang)  
- “Facebook’s Feature Store”(Jun Wan, 2021)  
- “Facebookの特徴ストア”(Jun Wan, 2021)  
- DoorDash:Building Riviera: A Declarative Real-Time Feature Engineering Framework(Allen Wang & Kunal Shah)  
- DoorDash:リビエラの構築: 宣言型リアルタイム特徴エンジニアリングフレームワーク(Allen Wang & Kunal Shah)  
- Spotify:Jukebox : Spotify’s Feature Infrastructure(Aman Khan & Daniel Kristjansson)  
- Spotify:Jukebox : Spotifyの特徴インフラ(Aman Khan & Daniel Kristjansson)  
- Pinterest:“Streamlining the Pinterest ML Feature Ecosystem”(Se Won Jang & Sihan Wang)  
- Pinterest:“Pinterest ML特徴エコシステムの合理化”(Se Won Jang & Sihan Wang)  
- LinkedIn:Open sourcing Feathr – LinkedIn’s feature store for productive machine learning(David Stein)  
- LinkedIn:Feathrのオープンソース化 – LinkedInの生産的機械学習のための特徴ストア(David Stein)  
- DoorDash:Introducing Fabricator: A Declarative Feature Engineering Framework(Kunal Shah). Fabricator subsumes DoorDash’s previous declarative feature engineering framework Riviera.  
- DoorDash:Fabricatorの紹介: 宣言型特徴エンジニアリングフレームワーク(Kunal Shah)。FabricatorはDoorDashの以前の宣言型特徴エンジニアリングフレームワークリビエラを包含します。  
- Snap:Speed Up Feature Engineering for Recommendation Systems  
- Snap:推薦システムのための特徴エンジニアリングのスピードアップ  
- Instacart:Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)  
- Instacart:学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)  
- Lessons Learned: The Journey to Real-Time Machine Learning at Instacart(Guanghua Shu)  
- 学んだ教訓: Instacartにおけるリアルタイム機械学習への旅(Guanghua Shu)  
- Griffin: How Instacart’s ML Platform Tripled ML Applications in a year(Sahil Khanna)  
- Griffin: InstacartのMLプラットフォームが1年でMLアプリケーションを3倍にした方法(Sahil Khanna)  
- Coupang Eats:Eats data platform: Empowering businesses with data(Fred Fu, Coupang 2022)  
- Coupang Eats:Eatsデータプラットフォーム: データでビジネスを強化(Fred Fu, Coupang 2022)  
- Airbnb:Chronon - Airbnb’s Feature Engineering Framework(Nikhil Simha). Zipline matured into Chronon, with improved APIs. Chronon is not yet open source.  
- Airbnb:Chronon - Airbnbの特徴エンジニアリングフレームワーク(Nikhil Simha)。ZiplineはChrononに成熟し、APIが改善されました。Chrononはまだオープンソースではありません。  
- Binance:Using MLOps to Build a Real-time End-to-End Machine Learning PipelineA Closer Look at Our Machine Learning Feature Store  
- Binance:リアルタイムエンドツーエンド機械学習パイプラインを構築するためのMLOpsの使用私たちの機械学習特徴ストアの詳細な見方  
- Using MLOps to Build a Real-time End-to-End Machine Learning Pipeline  
- リアルタイムエンドツーエンド機械学習パイプラインを構築するためのMLOpsの使用  
- A Closer Look at Our Machine Learning Feature Store  
- 私たちの機械学習特徴ストアの詳細な見方  
- Gojek:Feature Engineering at Scale with Dagger and Feast(Ravi Suhag)  
- Gojek:ダガーとフィーストを用いたスケールでの特徴エンジニアリング(Ravi Suhag)  
- Faire:Building Faire’s new marketplace ranking infrastructure(Sam Kenny)  
- Faire:Faireの新しいマーケットプレイスランキングインフラの構築(Sam Kenny)  



## Conclusion 結論

Speed matters. 
速度は重要です。
A well-designed feature platform can improve both the speed at which fresh data can be used to improve ML predictions and the iteration speed for data scientists to improve ML models. 
よく設計された特徴量プラットフォームは、**新しいデータを使用して機械学習（ML）予測を改善する速度と、データサイエンティストがMLモデルを改善するためのiteration速度**の両方を向上させることができます。

However, building a feature platform requires non-trivial investment. 
しかし、フィーチャープラットフォームを構築するには、簡単ではない投資が必要です。
The companies that have discussed their feature platforms are reasonably large tech companies with plenty of expertise and resources. 
フィーチャープラットフォームについて議論した企業は、十分な専門知識とリソースを持つかなり大きなテクノロジー企業です。
Even then, it can still take 10s of engineers multiple years to build. 
それでも、数十人のエンジニアが数年かかることがあります。

When I asked the tech lead of one of these platforms why it took them so long to build their platform, he said: “A lot of time could’ve been saved if we knew what we were doing.” 
これらのプラットフォームの1つのテックリードに、なぜプラットフォームの構築にそんなに時間がかかったのか尋ねたところ、彼はこう言いました。「私たちが何をしているのかを知っていれば、多くの時間を節約できたでしょう。」
Building a feature platform is a trial and error process, and a wrong design decision could delay the project for a year. 
フィーチャープラットフォームの構築は試行錯誤のプロセスであり、誤った設計決定はプロジェクトを1年遅らせる可能性があります。

As we gain more understanding of the requirements for feature platforms and the underlying technology for streaming computation matures, this process will become more straightforward. 
フィーチャープラットフォームの要件についての理解が深まり、ストリーミング計算の基盤技術が成熟するにつれて、このプロセスはより簡単になるでしょう。
I’m excited to see more companies successfully adopt a feature platform without significant investment. 
私は、より多くの企業が大きな投資なしにフィーチャープラットフォームを成功裏に採用するのを見るのが楽しみです。

<!-- ここまで読んだ! -->

## Acknowledgments 謝辞

I’d like to thank Deepyaman Datta, Chloe He, Zhenzhong Xu, Astasia Myers, and Luke Metz for giving me feedback on the post. 
Deepyaman Datta、Chloe He、Zhenzhong Xu、Astasia Myers、そしてLuke Metzに、投稿に対するフィードバックをいただいたことに感謝します。
Thanks Nikhil Simha, Hangfei Lin, and many other who have generously answered many of my questions.
Nikhil Simha、Hangfei Lin、そして私の多くの質問に寛大に答えてくれた他の多くの方々にも感謝します。



## Appendix 付録  
### Batch features vs. real-time features vs. near real-time features

See Real-time machine learning: challenges and solutions for more detail.

#### Batch Features

Batch features are the easiest to set up, since companies can use their existing batch pipeline and only need to add:
バッチ特徴は設定が最も簡単で、**企業は既存のバッチパイプラインを使用でき**、次のことを追加するだけで済みます：

1. キー-バリューストアの低遅延取得。
2. 計算されたバッチ特徴をキー-バリューストアに自動的にプッシュするメカニズム。

Two main drawbacks of batch features:
バッチ特徴の主な欠点は2つあります:

1. Feature staleness. If features are computed every hour, they are up to one hour stale.
   **特徴量の古さ**。特徴量が毎時計算される場合、最大で1時間古くなります。
2. Wasted computation. A company told me they need to compute features for 3 million users each time, which takes them 6 hours, therefore they can refresh their features once every 6 hours. However, only 5% of these users visit their site a day, which means that 95% of the computation is actually wasted.
   **無駄な計算**。ある企業は、毎回300万人のユーザの特徴を計算する必要があり、それには6時間かかるため、6時間ごとに特徴量を更新できると教えてくれました。しかし、これらのユーザのうち、1日にサイトを訪れるのはわずか5%であり、つまり95%の計算が実際には無駄になっています。


#### Real-time features

Real-time features are usually the next type to be deployed. 
リアルタイム特徴量は通常、次に展開されるタイプです。
Say, if you want to compute the number of views your product has had in the last 30 minutes in real-time, here are two of several simple ways you can do so:
例えば、リアルタイムで過去30分間にあなたの製品が受けたビューの数を計算したい場合、以下の2つの簡単な方法があります：

1. Create a lambda function that takes in all the recent user activities and counts the number of views.
   最近のユーザ活動をすべて受け取り、ビューの数をカウントするラムダ関数を作成します。
2. Store all the user activities in a database like postgres and write a SQL query to retrieve this count.
   postgresのようなデータベースにすべてのユーザ活動を保存し、このカウントを取得するSQLクエリを書くことです。

Because features are computed at prediction time, they are fresh, e.g. in the order of milliseconds.
**特徴量は予測時に計算されるため、新鮮です (例えばミリ秒単位のオーダー)**。

While real-time features are easy to set up, they’re harder to scale. 
リアルタイム特徴は設定が簡単ですが、スケールするのは難しいです。
Because real-time features are computed upon receiving prediction requests, their computation latency adds directly to user-facing latency. 
**リアルタイム特徴量は予測リクエストを受け取った際に計算されるため、その計算遅延はユーザ向けの遅延に直接加算されます**。
Traffic growth and fluctuation can significantly affect computation latency. 
**トラフィックの増加や変動は計算遅延に大きな影響を与える可能性**があります。
Complex features might be infeasible to support since they might take too long to compute.
複雑な特徴は計算に時間がかかりすぎるため、サポートが難しい場合があります。

#### Near RT / streaming features

Like batch features, near RT features are also precomputed and at prediction time, the latest values are retrieved and used. 
**バッチ特徴と同様に、near RT特徴も事前に計算され、予測時に最新の値が取得されて使用されます**。(うんうん、推論サーバーと非同期なストリーミングパイプラインによるもの...!:thinking_face:)
Since features are computed async, feature computation latency doesn’t add to user-facing latency. 
**特徴は非同期で計算されるため、特徴計算の遅延はユーザ向けの遅延に加算されません**。(これがリアルタイム特徴量との違い!)
You can use as many features or as complex features as you want.
必要なだけ多くの特徴量や複雑な特徴量を使用できます。

Unlike batch features, near RT feature values are recomputed much more frequently, so feature staleness can be in the order of seconds (it’s only “near” instead of “completely” real-time.) 
バッチ特徴とは異なり、near RT特徴の値ははるかに頻繁に再計算されるため、**特徴の古さは秒単位のオーダーになる可能性**があります（それは「完全に」リアルタイムではなく「近い」だけです）。
If a user doesn’t visit your site, its feature values won’t be recomputed, avoiding wasted computation.
ユーザがあなたのサイトを訪れない場合、その特徴値は再計算されず、無駄な計算を避けることができます。
Near RT features are computed using a streaming processing engine.
near RT特徴はストリーミング処理エンジンを使用して計算されます。

<!-- ここまで読んだ! -->
