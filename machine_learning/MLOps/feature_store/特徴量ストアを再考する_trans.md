
# Rethinking Feature Stores 特徴ストアの再考

Chang She·Follow  
Published in Feature Stores for ML·6 min read·Jul 26, 2019  
Feature Stores for MLに掲載·6分で読める·2019年7月26日  

Feature engineering is a critical component in any machine learning system.
**特徴エンジニアリングは、あらゆる機械学習システムにおいて重要な要素**です。  
As the basic input into a predictive model, the quality of features can make or break the overall performance of the model.  
予測モデルへの基本的な入力として、特徴の質はモデル全体のパフォーマンスを左右します。  

Feature engineering also takes a tremendous amount of work.  
**特徴エンジニアリングには膨大な労力がかかります**。  
If a new machine learning application requires one new feature, it probably means that the ML engineers discarded ten other features and tried ten variations of each candidate feature.  
新しい機械学習アプリケーションが1つの新しい特徴を必要とする場合、それはおそらくMLエンジニアが他の10の特徴を捨て、各候補特徴の10のバリエーションを試したことを意味します。  
Features have to be computed, versioned, backfilled, and shared.  
特徴は計算され、バージョン管理され、バックフィルされ、共有されなければなりません。  
Finally the method for storing and accessing features will also fundamentally differ between offline vs online contexts.  
最後に、特徴を保存しアクセスする方法は、オフラインとオンラインのコンテキストで根本的に異なります。  

This means that as more and more companies scale up their machine learning applications, they are finding it extremely difficult to manage this combinatorial explosion of needs.  
これは、ますます多くの企業が機械学習アプリケーションを拡大するにつれて、これらのニーズの組み合わせの爆発を管理することが非常に困難であることを意味します。  
It’s become a big enough problem that many of the biggest tech companies have invested significant resources into creating specialized systems to manage model features.  
この問題は大きくなりすぎて、多くの大手テクノロジー企業がモデルの特徴を管理するための専門的なシステムを作成するために多大なリソースを投資しています。  

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*asFhOIfgSM7JvUCa.png)

# Existing Systems 既存のシステム
## Michelangelo ミケランジェロ

Uber was one of the first big companies to publish the concept of a feature store. 
Uberは、[フィーチャーストア](https://eng.uber.com/michelangelo)の概念を発表した最初の大企業の一つでした。
This was a set of services that helped users 1) create and manage shared features and 2) allow for unified references to both online and offline versions of a feature to help eliminate the need to reproduce code between offline training and online serving.
これは、ユーザーが1) 共有フィーチャーを作成および管理し、2) オンラインおよびオフラインの両方のバージョンのフィーチャーに統一された参照を可能にするサービスのセットであり、オフラインのトレーニングとオンラインの提供の間でコードを再現する必要を排除するのに役立ちます。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*F4gGPz8PukepaG5r.png)

## Zipline

Airbnb built their own as part of their Zipline framework. 
Airbnbは、彼らのZiplineフレームワークの一部として独自のものを構築しました。
In addition to setting up the basic stores and services, Zipline also focused on features to deal with timeseries alignment using “label offset” (pictured below), backfilling training datasets, combining batch and streaming data, etc.
基本的なストアとサービスの設定に加えて、Ziplineは「ラベルオフセット」を使用した時系列の整列、トレーニングデータセットのバックフィリング、バッチデータとストリーミングデータの統合などの機能にも焦点を当てました。

![](https://miro.medium.com/v2/resize:fit:652/format:webp/1*_2n84jXDbmVlOhMt8np_5g.png)

## Feast

Neither Uber and AirBnB’s projects are open source, which was part of what made Feast interesting. 
UberとAirBnBのプロジェクトはどちらもオープンソースではなく、これがFeastを興味深いものにしている要因の一部でした。
Feast is an open-source feature store jointly developed by Gojek and Google Cloud. 
**Feastは、GojekとGoogle Cloudによって共同開発されたオープンソースのフィーチャーストア**です。
Besides being open-source, it also differs from Uber’s system by including the ingestion component. 
オープンソースであることに加えて、Feastはデータ取り込みコンポーネントを含むことでUberのシステムとは異なります。
This meant that features can be specified in a configuration yml file: 
これにより、フィーチャーは設定ymlファイルで指定できるようになりました：

```yaml
id: word.count
name: count
entity: word
owner: bob@feast.com
description: number of times the word appears
valueType: INT64
uri: https://github.com/bob/example
```


## Hopsworks

Most recently,Logical Clocksadded a feature store as part of their Hopsworks framework. 
最近、Logical ClocksはHopsworksフレームワークの一部としてフィーチャーストアを追加しました。
It mostly focuses on the offline training portion but probably has the most clearly / simply presented architecture.
それは主にオフライントレーニング部分に焦点を当てていますが、おそらく最も明確でシンプルに提示されたアーキテクチャを持っています。

<!-- ここまで読んだ! -->

# So what’s the problem? それで、問題は何ですか？

Let me preface the rest of this article with this disclaimer: each of these systems have been tested in production and they work their respective use cases. 
この記事の残りの部分に入る前に、この免責事項を述べさせてください：これらのシステムはすべて本番環境でテストされており、それぞれのユースケースで機能しています。
So until I’ve actually built/tested the ideas I’m about to discuss, you probably shouldn’t believe anything I say. 
したがって、私がこれから議論するアイデアを実際に構築/テストするまで、私の言うことを信じない方が良いでしょう。

Having said that, I’ve found it difficult to think about these existing systems coherently. 
とはいえ、私は**これらの既存のシステムについて一貫して考えるのが難しい**と感じています。
In general the focus has been “well we needed to satisfy requirement X so we implemented Y in this way” (e.g., Zipline’s backfilling, Michelangelo’s online store, etc). 
一般的に、焦点は「**私たちは要件Xを満たす必要があったので、Yをこのように実装しました**」というものでした（例：Ziplineのバックフィリング、Michelangeloのオンラインストアなど）。
But I haven’t really seen a conceptual framework that truly helps us think about how all of these different pieces fit together. 
しかし、これらの異なる要素がどのように組み合わさるかを考えるのに本当に役立つ概念的枠組みは見たことがありません。
Without a coherent conceptual framework, the result seems to be that depending on what use case you decide to add or remove, the architecture to serve these use cases may look drastically different. 
一貫した概念的枠組みがないと、追加または削除するユースケースによって、これらのユースケースに対応するアーキテクチャが大きく異なるように見えます。
For anyone trying to select or design a feature store, this is not very encouraging. 
フィーチャーストアを選択または設計しようとしている人にとって、これはあまり励みになりません。

I think we can do better. 
私たちはもっと良いことができると思います。

<!-- ここまで読んだ! -->

# Be like Joe

Wikipedia defines a feature as “an individual measurable property or characteristic of a phenomenon being observed”. 
ウィキペディアでは、**特徴を「観察されている現象の個別の測定可能な属性または特性」と定義**しています。
I think we’ve been focusing too much on the outcome of observation and not enough on the process of observation. 
私たちは観察の結果にあまりにも焦点を当てすぎており、観察のプロセスには十分に注目していないと思います。
Focusing on the outcome is static and narrow in scope. 
結果に焦点を当てることは静的であり、範囲が狭いです。
Focusing on the process gives us a coherent framework that provides natural ways to think about and design solutions for feature engineering issues. 
プロセスに焦点を当てることで、特徴エンジニアリングの問題について考え、解決策を設計するための自然な方法を提供する一貫したフレームワークが得られます。

Joe Armstrong talked about Erlang programs being structured as processes that generate messages to communicate with each other. 
ジョー・アームストロングは、Erlangプログラムが互いに通信するためにメッセージを生成するプロセスとして構成されていると話しました。
This was in stark contrast to the traditional OO paradigm and a primary factor that makes Erlang unique and successful. 
これは従来のオブジェクト指向（OO）パラダイムとは大きく対照的であり、Erlangをユニークで成功させる主要な要因です。
I’d like to propose an analogous statement about features: 
私は特徴について類似の声明を提案したいと思います。
Features are data generating processes. 
**特徴はデータ生成プロセス**です。
Processes have input and generates output. 
プロセスには入力があり、出力を生成します。
And in different contexts, processes may have different concrete implementations. 
そして、異なる文脈では、プロセスは異なる具体的な実装を持つ場合があります。

In particular, let’s discuss several unique benefits of this mental model: 
特に、このメンタルモデルのいくつかのユニークな利点について議論しましょう：

## Versioning and provenance バージョン管理と出所

Feature processes are represented by code artifacts that can be versioned. 
フィーチャープロセスは、バージョン管理可能なコードアーティファクトによって表現されます。
When a particular version of the artifact is executed to materialize the feature, the output data is point-in-time and can also be versioned. 
特定のバージョンのアーティファクトが実行されてフィーチャーが具現化されると、出力データは時点データとなり、バージョン管理も可能です。
Feature processes must also have input in order to generate output. 
フィーチャープロセスは出力を生成するために入力を持たなければなりません。
We can then follow the input feature references to trace the full provenance of a particular feature. 
その後、入力フィーチャーの参照を辿ることで、特定のフィーチャーの完全な出所を追跡できます。
As you can see, versioning, point-in-time, lineage are now no longer just extra appendages you attach to a static dataset. 
ご覧の通り、バージョン管理、時点データ、系譜はもはや静的データセットに付加する余分な付属物ではありません。
Instead they’re an integral part of the concept of a feature itself. 
むしろ、それらはフィーチャー自体の概念の不可欠な部分です。

## Lazy evaluation 遅延評価

Some features are expensive to compute (e.g., embeddings) and you’ll likely want to always materialize the output. 
いくつかの特徴は計算コストが高い（例：埋め込み）ため、出力を常に具現化したいと思うでしょう。(保持、永続化、的な意味か。マテリアライズドビュー的な!)
Other features (e.g., log(engage)) are fast to compute from the raw data so there might not be any need to materialize it at all. 
他の特徴（例：log(engage)）は、生データから迅速に計算できるため、全く具現化する必要がないかもしれません。 
But that is a level of detail that should be completely hidden from the data scientist / developer doing feature engineering. 
**しかし、それは特徴エンジニアリングを行うデータサイエンティストや開発者から完全に隠されるべき詳細のレベル**です。 
By focusing on features as processes, we can enable the user to specify just the feature identifier regardless when the feature is materialized / persisted. 
特徴をプロセスとして捉えることで、ユーザーが特徴が具現化または永続化されるタイミングに関係なく、特徴識別子のみを指定できるようにします。 
So the feature store user can write code like: 
したがって、特徴ストアのユーザーは次のようなコードを書くことができます：

```python
df = feature_store.get("user_view_time").materialize(start, end)
```

And not have to worry about what’s being fetched from database vs computed in memory. 
**そして、データベースから取得されるものとメモリ内で計算されるものについて心配する必要はありません**。
(なるほど、これが「featureがデータ生成プロセスである」と主張するからか!)
Moreover, we can also chain lazy features processes together into the pipeline and enable a feature compiler to optimize the underlying computations on the fly. 
さらに、遅延特徴プロセスをパイプラインに連結し、特徴コンパイラが基盤となる計算をリアルタイムで最適化できるようにすることも可能です。

<!-- ここまで読んだ! -->

## Online vs offline オンラインとオフライン

Processes don’t exist in isolation. 
プロセスは孤立して存在するわけではありません。 
Instead all process must run inside a particular context. 
むしろ、すべてのプロセスは特定のコンテキスト内で実行されなければなりません。 
When that context changes, the specific implementation on the process within the context may also change. 
そのコンテキストが変わると、コンテキスト内のプロセスの具体的な実装も変わる可能性があります。 
For example, the code for getting offline data vs online data for the same feature might look very different. 
**例えば、同じ特徴量のオフラインデータとオンラインデータを取得するためのコードは非常に異なる場合があります**。 
The offline code might run a SQL query or call Spark API. 
オフラインコードはSQLクエリを実行したり、Spark APIを呼び出したりするかもしれません。 
The online code might call a ScyllaDB API, a Redis API, or some custom real-time data source. 
オンラインコードはScyllaDB API、Redis API、またはカスタムのリアルタイムデータソースを呼び出すかもしれません。 
In both environments, we’d be able to write the same code to get the feature values: 
両方の環境で、機能値を取得するために同じコードを書くことができるべきでしょう。

```python
df = (feature_store.get("user_hist").filter(user_id).materialize(start, end))
```

And the offline version would get executed as perhaps some Spark code snippet whereas the online version would add the user_id filter into the request body for an API call to a user-profile service that updates in real-time. 
オフライン版はおそらくSparkのコードスニペットとして実行される一方で、オンライン版はリアルタイムで更新されるユーザープロファイルサービスへのAPI呼び出しのリクエストボディにuser_idフィルターを追加します。

<!-- ここまで読んだ! -->

## No data scientist is an island

All of the systems I described before has collaboration as a central goal. 
私が前に説明したすべてのシステムは、**コラボレーションを中心的な目標としています**。(特徴量の再利用とか!他チームが作った特徴量を使えるとか!)
While they solve for visibility and discovery of features, none of them solve the third critical problem in collaboration: trust. 
それらは特徴の可視性と発見を解決しますが、コラボレーションにおける第三の重要な問題である「信頼」を解決するものはありません。 
By focusing on the data generating process instead of the static dataset, we enable verifiability of how the feature is generated, which is much better than our current reputational paradigm of trust. 
静的データセットではなくデータ生成プロセスに焦点を当てることで、特徴がどのように生成されるかの検証可能性を可能にし、これは現在の信頼の評判的パラダイムよりもはるかに優れています。 
In addition, this also makes it a lot easier to debug complex feature pipelines because we can easily verify each stage separately. 
さらに、各ステージを個別に簡単に検証できるため、複雑な特徴パイプラインのデバッグがはるかに容易になります。

# But also be like Mike しかし、マイクのようにもなろう

A good mental model lets us describe a very complex system or phenomenon with as few distinct concepts as possible. 
良いメンタルモデルは、非常に複雑なシステムや現象をできるだけ少ない異なる概念で説明できるようにします。
Different features, use case, and functionality should all fit together into an integrated whole. 
異なる機能、ユースケース、機能性はすべて統合された全体として組み合わさるべきです。
This helps us design architectures that make sense and can stand-up to the test of time. 
これにより、意味のあるアーキテクチャを設計し、時の試練に耐えることができます。
Of course, I fully expect my thinking to evolve a lot in the process of actually building our feature store. 
もちろん、実際に私たちのフィーチャーストアを構築する過程で、私の考えが大きく進化することを完全に期待しています。
As Mike Tyson once said “Everybody has a plan until they get punched in the mouth”. 
マイク・タイソンがかつて言ったように、「誰もが計画を持っているが、口を殴られるまでだ」。

Most importantly, this is a beginning rather than an end. 
最も重要なのは、これは終わりではなく始まりであるということです。
We’re currently building out our next generation machine learning platform at Tubi. 
私たちは現在、Tubiで次世代の機械学習プラットフォームを構築しています。
If you’re passionate about creating tools and products to enable ml-driven companies, come join us and build this platform with me from vision to execution. 
もし、機械学習駆動の企業を支援するためのツールや製品を作ることに情熱を持っているなら、私たちに参加し、ビジョンから実行までこのプラットフォームを一緒に構築しましょう。
And let the punching begin. 
さあ、殴り合いを始めましょう。

<!-- ここまで読んだ! -->
