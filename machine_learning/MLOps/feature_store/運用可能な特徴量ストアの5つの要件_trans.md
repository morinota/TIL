# 5 Minimum Requirements of an Operational Feature Store
# 操作可能なフィーチャーストアの最小要件5つ

Ben Epstein·Follow  
ベン・エプスタイン·フォロー

Published in Feature Stores for ML·6 min read·Jul 15, 2020  
「Feature Stores for ML」に掲載·6分で読める·2020年7月15日

By Ben Epstein, Sergio Ferragut, and Monte Zweben  
著者：ベン・エプスタイン、セルジオ・フェラガット、モンテ・ツヴェーベン

I’ve spent the last few months thinking heavily about feature stores.  
私はここ数ヶ月、フィーチャーストアについて深く考えてきました。  
It’s the hottest new buzz word in the ML space, and everyone has a distinct implementation laser-focused on their personal use cases.  
これはML（機械学習）分野で最も注目されている新しいバズワードであり、誰もが自分のユースケースに特化した独自の実装を持っています。

A recent article¹ that I read talked about this exact topic and did a great job summarizing the fundamental problem:  
私が最近読んだ記事¹はこの正確なトピックについて語っており、根本的な問題をうまく要約していました：  
these implementations don’t create a general purpose, conceptual framework for what a feature store is, rather focusing on the outcomes of their particular use cases.  
これらの実装はフィーチャーストアが何であるかの一般的な概念フレームワークを作成せず、特定のユースケースの結果に焦点を当てています。  
If we forget what we’ve read about these implementations and rethink this from the ground up,  
もし私たちがこれらの実装について読んだことを忘れ、ゼロから再考することができれば、  
we may be able to design a general purpose feature store that works for any use-case.  
**あらゆるユースケースに対応する一般的なフィーチャーストア**を設計できるかもしれません。

What is a feature store?  
フィーチャーストアとは何ですか？  
A feature store is a shareable repository of predictive features, both complex and simple, for use in near real-time machine learning and business intelligence.  
フィーチャーストアは、近いリアルタイムの機械学習とビジネスインテリジェンスで使用するための、複雑なものと単純なものの予測フィーチャーの共有可能なリポジトリです。  
As you can see, this is a broad and general definition.  
ご覧の通り、これは広範で一般的な定義です。  
That’s because a feature store has a plethora of use cases, all of which should be possible if architected correctly.  
**フィーチャーストアには多くのユースケースがあり、正しく設計されていればすべてが可能であるた**めです。  
So let’s start from the ground up and list out some of the minimal requirements.  
それでは、ゼロから始めて、いくつかの最小要件をリストアップしましょう。



# Shareable 共有可能性

A fundamental premise of the feature store is that it must be shareable across an organization; features must be accessible by any team that needs them. 
フィーチャーストアの基本的な前提は、それが組織全体で共有可能でなければならないということです。**特徴量は、それを必要とする任意のチームがアクセスできる必要があります**。
This is what allows for the reuse of complex features that may take weeks or months to develop. 
これにより、開発に数週間または数ヶ月かかる可能性のある複雑なフィーチャーの再利用が可能になります。
The idea of shared features is so prevalent that Twitter coined the metric “Sharing Adoption: The number of teams who use another team’s features in production.” 
共有フィーチャーのアイデアは非常に普及しており、Twitterは「[Sharing Adoption（共有採用）](https://twitter.com/jim_dowling/status/1257588702156591104)」という指標を作りました：他のチームのフィーチャーを本番環境で使用するチームの数です。
Having a single repository of features that data scientists can search and reuse to help solve their problems is crucial to their productivity. 
**データサイエンティストが検索して再利用できる特徴量達の単一のリポジトリを持つことは、彼らの生産性にとって重要**です。

If you have a fairly mature data science organization, you will likely have hundreds or thousands of features, with potentially millions of records. 
もしあなたがかなり成熟したデータサイエンス組織を持っているなら、数百または数千のフィーチャーがあり、潜在的には数百万のレコードがあるでしょう。
Easily searching through those features, whether that be through SQL or a dataframe-like API, is a must-have for data scientists to be successful. 
SQLやデータフレームのようなAPIを通じて、それらのフィーチャーを簡単に検索できることは、データサイエンティストが成功するために必須です。

<!-- ここまで読んだ! -->

# Transparent 透明性

In order for a feature store to be trusted, the origin and implementation of each feature must be available for investigation. 
フィーチャーストアが信頼されるためには、各フィーチャーの起源と実装が調査可能でなければなりません。
To achieve this, the feature generation process must be well documented and available for all to review its lineage.
これを達成するためには、フィーチャー生成プロセスが十分に文書化され、すべての人がその系譜を確認できるようにする必要があります。   


# Versioned バージョン管理

A central theme of the feature store is its collaborative nature. 
フィーチャーストアの中心的なテーマは、その協力的な性質です。
Along with transparency and sharing, versioning ensures trust: what you see is what you get. 
透明性と共有に加えて、バージョン管理は信頼を確保します：見えるものが得られるものです。
When you put a feature in your model, especially one you didn’t create yourself, it’s crucial you know it’s up to date. 
自分で作成していないフィーチャーをモデルに組み込むとき、それが最新であることを知ることが重要です。

This comes in two forms: 
これは2つの形で提供されます：

1. Versioning how a feature is calculated and if that calculation changes 
   フィーチャーがどのように計算されるか、またその計算が変更されるかのバージョン管理

2. Versioning when the feature was last updated 
   1. フィーチャーが最後に更新された日時のバージョン管理

Versioning the feature generation ensures that if the implementation of a specific feature changes over time, it’s tracked — who built it, how did it change, potentially why it changed. 
フィーチャー生成のバージョン管理は、特定のフィーチャーの実装が時間とともに変更された場合に、それが追跡されることを保証します — 誰が作成したのか、どのように変更されたのか、潜在的にその理由は何か。
With proper versioning and lineage information, feature auditability is enabled 
適切なバージョン管理と系譜情報により、フィーチャーの監査可能性が実現されます。

Versioning the feature itself saves you from accidentally making decisions on stale data. 
フィーチャー自体のバージョン管理は、古いデータに基づいて誤って意思決定を行うことからあなたを守ります。
Some features may be updated every minute, 24 hours, 2 weeks, or even 1 month, think RFM. 
**一部のフィーチャーは、毎分、24時間、2週間、または1か月ごとに更新される**ことがあります（RFMを考えてみてください）。
Others may change every time a user logs into an account or swipes a credit card. 
他のフィーチャーは、ユーザーがアカウントにログインするたびやクレジットカードをスワイプするたびに変更されることがあります。
It’s crucial to track not only when these features were updated, but also keep a full history of those changes. 
これらのフィーチャーがいつ更新されたかを追跡するだけでなく、その変更の完全な履歴を保持することが重要です。

(リークを防ぐ、的なことは書いてないな...!:thinking:)

# Governed/Access Controlled 管理された/アクセス制御された

This may seem obvious, but it’s just as important: strong enforcement over who can and who historically has queried the feature store is critical. 
これは明白に思えるかもしれませんが、同様に重要です：**誰が特徴量ストアをクエリできるか、また歴史的に誰がクエリしてきたかに対する強力な施行が重要**です。
A manager needs to easily restrict access to features (even at a column level) and see who in the organization has requested certain features, and when. 
マネージャーは、機能へのアクセスを簡単に制限できる必要があります（列レベルでも）し、組織内の誰が特定の機能をいつ要求したかを確認できる必要があります。

Along the same lines, insert/update privileges should be tightly controlled as well. 
同様に、挿入/更新の権限も厳密に制御されるべきです。

(これは技術的負債論文の、データ依存関係のスパゲティ化みたいな話かな)

# Online & Offline (Batch and Realtime) オンラインとオフライン（バッチとリアルタイム）

This is an important concept, and there is a lot to think about here. 
これは重要な概念であり、考慮すべきことがたくさんあります。
I’ve seen some confusion in the MLOps space surrounding online/offline feature stores and differing definitions. 
MLOpsの分野では、オンライン/オフラインのフィーチャーストアと異なる定義に関して混乱が見られます。
I’m going to attempt a definition and provide an alternative approach. 
私は定義を試み、代替アプローチを提供します。

A feature store has typically been segmented into two distinct workloads, offline and online. 
**フィーチャーストアは通常、オフラインとオンラインの2つの異なるワークロードに分けられます**。

1. Offline Workload: Sometimes, people refer to offline as a process that creates features in batch at set intervals. 
   **オフラインワークロード**：時には、オフラインを定期的にバッチでフィーチャーを作成するプロセスとして言及することがあります。(これは書き込み!)
   Other times, people refer to offline as the process of training models “offline” using larger, batch based queries. 
   他の時には、オフラインを大規模なバッチベースのクエリを使用してモデルを「オフライン」でトレーニングするプロセスとして言及します。
   (あとはバッチ推論だね！:thinking:)

2. Online Workload: Sometimes, this is thought of as a process that creates features in the moment from new data. 
   **オンラインワークロード**：時には、これは新しいデータからその瞬間にフィーチャーを作成するプロセスと考えられます。(これは書き込み!)
   Other times, people refer to online as the serving of models, making real time inferences on new data and returning the predictions. 
   他の時には、オンラインをモデルの提供、すなわち新しいデータに対してリアルタイムで推論を行い、予測を返すこととして言及します。

These two workloads are often handled by two separate feature stores, each with their own dedicated compute engines, that communicate with each other as necessary. 
**これらの2つのワークロードは、しばしばそれぞれ専用のコンピューティングエンジンを持つ2つの別々のフィーチャーストアによって処理され、必要に応じて相互に通信します**。(ex. DWHとRedisなど! :thinking:)
That is problematic. 
これは問題です。
Ideally you would have one engine that is both your “offline” and your “online” feature store. 
**理想的には、1つのエンジンが「オフライン」と「オンライン」のフィーチャーストアの両方を担うべき**です。(うんうん、せめてユーザ側にその境界が情報隠蔽されてて欲しいよなぁ)
One repository for all of your features, able to handle both batch, analytical queries, and low latency lookups. 
すべてのフィーチャーのための**1つのリポジトリで、バッチ、分析クエリ、低遅延のルックアップの両方を処理できるもの**です。
This reduces your operational complexity and data movement within your system, lowering the potential for data corruption. 
これにより、システム内の運用の複雑さとデータの移動が減少し、データの破損の可能性が低下します。

A potentially simpler paradigm is to separate the concepts of feature calculation from feature utilization, 
よりシンプルなパラダイム(見方、考え方??)は、フィーチャ計算の概念をフィーチャー利用から分離することです。(これがどう関わってくるんだ??:thinking:)
with the understanding that all features must have low latency lookups for utilization. 
**すべてのフィーチャーは利用のために低遅延のルックアップを持つ必要がある**という理解のもとです。

<!-- ここまで読んだ! -->

Feature calculation has two dimensions: frequency and complexity. 
**フィーチャ計算には2つの次元があります：頻度と複雑さ。**
Frequency determines the time of update of a given feature. 
頻度は、特定のフィーチャーの更新のタイミングを決定します。
These can either be real time (event driven) or batch (scheduled). 
**これらはリアルタイム（イベント駆動）またはバッチ（スケジュールされた）である可能性**があります。
Complexity, on the other hand, describes the computational scope required to generate the feature; 
一方、**複雑さはフィーチャーを生成するために必要な計算の範囲**を説明します；
think simple arithmetic functions on a record versus entire data pipelines. 
レコード上の単純な算術関数と全体のデータパイプラインを考えてみてください。
Features can be both real time and complex, such as updating the analytical aggregation “average monthly food spend” upon an individual payment at a restaurant. 
フィーチャーはリアルタイムかつ複雑であり得ます。例えば、レストランでの個々の支払いに基づいて分析集計「月平均食費」を更新することです。

The use of these features, whether calculated in batch or in real time, must be readily available with millisecond latency for business logic and machine learning models at inference time. 
これらのフィーチャーの使用は、**バッチで計算されたものであれリアルタイムで計算されたものであれ、ビジネスロジックや機械学習モデルの推論時にミリ秒の遅延で容易に利用できる必要があり**ます。

Using two disparate engines to manage your feature store is difficult and increases your architectural complexity. 
フィーチャーストアを管理するために2つの異なるエンジンを使用することは困難であり、アーキテクチャの複雑さを増加させます。
Think about the lifecycle of a machine learning model. 
機械学習モデルのライフサイクルについて考えてみてください。
The training of that model is done with the “offline” feature store, but its inference may occur in real time (using the “online” feature store). 
**そのモデルのトレーニングは「オフライン」フィーチャーストアを使用して行われますが、その推論は「オンライン」フィーチャーストアを使用してリアルタイムで行われる可能性があります**。
Having two different engines, with potentially inconsistent or stale data, can lead to poor models and bad business outcomes. 
異なる2つのエンジンを持ち、潜在的に不整合または古いデータがあると、劣悪なモデルや悪いビジネス結果につながる可能性があります。

<!-- ここまで読んだ! -->

Consider this real world example: 
この実世界の例を考えてみてください：
Imagine the following three features; 
次の3つのフィーチャーを想像してください；
daily spending aggregation per user, 
ユーザーごとの日次支出集計、
the last transaction amount made by a user, 
ユーザーによる最後の取引額、
and the output of a clustering algorithm, grouping customers into different propensities to spend. 
およびクラスタリングアルゴリズムの出力、顧客を異なる支出傾向にグループ化するものです。
The daily spending aggregation is scheduled to run once a day, 
日次支出集計は1日に1回実行されるようにスケジュールされています、
whereas the last transaction amount and the clustering algorithm are made in real-time as features change. 
一方、最後の取引額とクラスタリングアルゴリズムは、フィーチャーが変化する際にリアルタイムで作成されます。
The clustering feature is then used in other online applications such as email marketing campaigns and special offerings. 
クラスタリングフィーチャーは、その後、メールマーケティングキャンペーンや特別オファーなどの他のオンラインアプリケーションで使用されます。

Every time a user swipes a credit card, 
ユーザーがクレジットカードをスワイプするたびに、
the feature store is updated with the new “last transaction amount” feature. 
フィーチャーストアは新しい「最後の取引額」フィーチャーで更新されます。
This new feature, in addition to your aggregation feature which was updated at the end of the day, 
この新しいフィーチャーは、日末に更新された集計フィーチャーに加えて、
are fed into your clustering algorithm. 
クラスタリングアルゴリズムに供給されます。
Ideally, your feature store could propagate those changes down automatically, 
理想的には、フィーチャーストアはそれらの変更を自動的に伝播でき、
triggering the evaluation of the clustering algorithm, which may (if changed), trigger further changes, 
クラスタリングアルゴリズムの評価をトリガーし、変更があればさらなる変更をトリガーする可能性があります、
such as a flag on a users account for a new offer. 
たとえば、新しいオファーのためのユーザーアカウントにフラグを立てることです。

Having a single engine that can handle both workloads simultaneously creates a single source of truth, a single component to manage frequency and complexity. 
両方のワークロードを同時に処理できる単一のエンジンを持つことは、真実の単一のソースを作成し、頻度と複雑さを管理する単一のコンポーネントを作成します。



# Summary 概要

We’ve discussed a set of minimal requirements for an enterprise ready feature store, however, this is likely not a comprehensive list. 
私たちは、企業向けのフィーチャーストアに必要な最小限の要件のセットについて議論しましたが、これは包括的なリストではない可能性があります。
As we learn more about the use cases of machine learning in industry, this list will mature and grow. 
産業における機械学習のユースケースについてさらに学ぶにつれて、このリストは成熟し、成長していくでしょう。
If you think I missed any must-have requirements, let me know in the comments. 
もし私が見落とした必須要件があると思う方は、コメントで教えてください。
And if you’ve implemented a feature store of your own that you think is great, we’d love to hear about that too. 
また、あなた自身が素晴らしいと思うフィーチャーストアを実装した場合、それについてもぜひお聞かせください。

[1] Chang She.Rethinking Feature Stores: https://medium.com/@changshe/rethinking-feature-stores-74963c2596f0


<!-- ここまで読んだ! -->
