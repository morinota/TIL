## link リンク

https://www.hopsworks.ai/post/feature-store-the-missing-data-layer-in-ml-pipelines
https://www.hopsworks.ai/post/feature-store-the-missing-data-layer-in-ml-pipelines

## title タイトル

Feature Store: The missing data layer for Machine Learning pipelines?
フィーチャーストア： 機械学習パイプラインに足りないデータ層？

## abstract 抄録

A feature store is a central vault for storing documented, curated, and access-controlled features.
フィーチャーストアは、文書化され、キュレーションされ、アクセス制御されたフィーチャーを保存するための中央保管庫である。
In this blog post, we discuss the state-of-the-art in data management for deep learning and present the first open-source feature store, available in Hopsworks.
このブログポストでは、深層学習のためのデータ管理の最先端について議論し、Hopsworksで利用可能な最初のオープンソースのフィーチャーストアを紹介する。

# What is a feature store? フィーチャーストアとは何か？

The concept of a feature store was introduced by Uber in 2017.
フィーチャーストアのコンセプトは2017年にウーバーによって導入された。
The feature store is a central place to store curated features within an organization.
フィーチャーストアは、組織内でキュレーションされたフィーチャーを保存する中心的な場所である。
A feature is a measurable property of some data-sample.
特徴とは、あるデータサンプルの測定可能な特性である。

It could be for example an image-pixel, a word from a piece of text, the age of a person, a coordinate emitted from a sensor, or an aggregate value like the average number of purchases within the last hour.
例えば、画像ピクセル、テキストの単語、人の年齢、センサーから発せられる座標、あるいは過去1時間以内の平均購買数のような集計値などである。
Features can be extracted directly from files and database tables, or can be derived values, computed from one or more data sources.
特徴量は、ファイルやデータベーステーブルから直接抽出することも、1つまたは複数のデータソースから計算された派生値とすることもできます。

Features are the fuel for AI systems, as we use them to train machine learning models so that we can make predictions for feature values that we have never seen before.
特徴量はAIシステムの燃料であり、それを使って機械学習モデルを訓練することで、見たこともないような特徴量の予測も可能になる。

## The feature store has two interfaces: フィーチャーストアは2つのインターフェースを持っています：

Writing to the feature store: The interface for Data Engineers.
フィーチャーストアに書き込む： データエンジニアのためのインターフェース
At the end of the feature engineering pipeline, instead of writing features to a file or a project-specific database or file, features are written to the feature store.
フィーチャーエンジニアリングパイプラインの最後では、フィーチャーをファイルやプロジェクト固有のデータベースやファイルに書き込むのではなく、フィーチャーストアに書き込む。

Reading from the feature store:
フィーチャーストアから読む

‍The interface for Data Scientists.
データサイエンティストのためのインターフェース。
To train a model on a set of features, the features can be read from the feature store directly.
特徴のセットでモデルを学習するには、特徴を特徴ストアから直接読み込むことができる。

A feature store is not a simple data storage service, it is also a data transformation service as it makes feature engineering a first-class construct.
フィーチャーストアは単なるデータ保存サービスではなく、フィーチャーエンジニアリングを第一級の構成要素とするデータ変換サービスでもある。
Feature engineering is the process of transforming raw data into a format that is understandable for predictive models.
フィーチャーエンジニアリングは、生データを予測モデルにとって理解しやすい形式に変換するプロセスである。

# Why you need a feature store? なぜフィーチャーストアが必要なのか？

At Hopsworks we are committed to developing technologies to operate machine learning workflows at large scale and to help organizations distill intelligence from data.
ホップワークスでは、機械学習ワークフローを大規模に運用し、組織がデータからインテリジェンスを抽出できるよう支援する技術の開発に取り組んでいます。
Machine learning is an extremely powerful method that has the potential to help us move from a historical understanding of the world to a predictive modeling of the world around us.
機械学習は、世界の歴史的な理解から、私たちを取り巻く世界の予測的なモデリングへと移行するのに役立つ可能性を秘めた、非常に強力な手法である。
However, building machine learning systems is hard and requires specialized platforms and tools.
しかし、機械学習システムの構築は難しく、専門的なプラットフォームやツールを必要とする。

Although ad-hoc feature engineering and training pipelines is a quick way for Data Scientists to experiment with machine learning models, such pipelines have a tendency to become complex over time.
データサイエンティストにとって、アドホックなフィーチャーエンジニアリングとトレーニングパイプラインは、機械学習モデルを実験する手っ取り早い方法だが、そのようなパイプラインは時間とともに複雑になる傾向がある。

As the number of models increases, it quickly becomes a pipeline jungle that is hard to manage.
モデル数が増えれば、たちまちパイプラインのジャングルと化し、管理が難しくなる。
This motivates the usage of standardized methods and tools for the feature engineering process, helping reduce the cost of developing new predictive models.
このことは、新しい予測モデルの開発コストを削減するのに役立つ、特徴工学プロセスのための標準化された方法とツールの使用を動機づける。
The feature store is a service designed for this purpose.
フィーチャーストアはこの目的のために設計されたサービスである。

## Technical Debt in Machine Learning Systems 機械学習システムにおける技術的負債

“Machine Learning: The High-Interest Credit Card of Technical Debt”
「機械学習： 技術的負債という高金利のクレジットカード"

Machine learning systems have a tendency to assemble technical debt [1].
機械学習システムには、技術的負債を抱える傾向がある[1]。
Examples of technical debt in machine learning systems are:
機械学習システムにおける技術的負債の例としては、以下のようなものがある：

There is no principled way to access features during model serving.
モデル提供中にフィーチャーにアクセスする原則的な方法はない。

Features cannot easily be re-used between multiple machine learning MLOps pipelines.
特徴は、複数の機械学習MLOpsパイプライン間で簡単に再利用できない。

Data science projects work in isolation without sharability, collaboration and re-use.
データサイエンス・プロジェクトは、共有可能性、コラボレーション、再利用がなければ、孤立して機能する。

Features used for training and serving are inconsistent.
トレーニングやサーブに使用される機能には一貫性がない。

When new data arrives, there is no way to pin down exactly which features need to be recomputed, rather the entire pipeline needs to be run to update features.
新しいデータが届くと、どのフィーチャーを再計算する必要があるのかを正確に特定する方法はなく、むしろフィーチャーを更新するためにパイプライン全体を実行する必要がある。

Several organizations that we have spoken to struggle to scale their machine learning workflows due to the technical complexity, and some teams are even reluctant to adopt machine learning considering the high technical cost of it.
私たちが話を聞いたいくつかの組織は、技術的な複雑さのために機械学習ワークフローの拡張に苦労しており、機械学習にかかる高い技術的コストを考慮して、機械学習の採用に消極的なチームさえある。

Using a feature store is a best practice for an MLOps pipeline, it can reduce the technical debt of machine learning workflows.
フィーチャーストアの使用はMLOpsパイプラインのベストプラクティスであり、機械学習ワークフローの技術的負債を減らすことができる。

“Pipeline jungles can only be avoided by thinking holistically about data collection and feature extraction”
「パイプラインのジャングルは、データ収集と特徴抽出を総合的に考えることでしか回避できない"

# Data Engineering is the hardest problem in Machine Learning データエンジニアリングは機械学習で最も難しい問題である

“Data is the hardest part of ML and the most important piece to get right.
「データはMLで最も難しい部分であり、正しく理解するために最も重要な部分である。
Modelers spend most of their time selecting and transforming features at training time and then building the pipelines to deliver those features to production models.
モデラーは、トレーニング時にフィーチャーを選択して変換し、それらのフィーチャーを本番モデルに提供するためのパイプラインを構築することに、ほとんどの時間を費やしている。
Broken data is the most common cause of problems in production ML systems”
壊れたデータは、本番MLシステムにおける問題の最も一般的な原因である。

Delivering machine learning solutions in production and at large-scale is very different from fitting a model to a pre-processed dataset.
機械学習ソリューションを本番環境で大規模に提供することは、事前に処理されたデータセットにモデルを当てはめることとは大きく異なる。
In practice, a large part of the effort that goes into developing a model is spent on feature engineering and data wrangling.
実際には、モデルの開発にかかる労力の大部分は、フィーチャーエンジニアリングとデータ整理に費やされる。

There are many different ways to extract features from raw data, but common feature engineering steps include:
生データから特徴を抽出する方法はさまざまだが、一般的な特徴工学のステップには次のようなものがある：

Converting categorical data into numeric data;
カテゴリーデータを数値データに変換する；

Normalizing data (to alleviate ill-conditioned optimization when features originate from different distributions);
データの正規化（異なる分布に由来する特徴がある場合に、条件の悪い最適化を緩和する）；

One-hot-encoding/binarization;
ワンホットエンコーディング/2値化；

Feature binning (e.g., convert continuous features into discrete);
フィーチャービニング（連続フィーチャを離散フィーチャに変換するなど）；

Feature hashing (e.g., to reduce the memory footprint of one-hot-encoded features);
特徴のハッシュ化（例えば、ワンホットエンコードされた特徴のメモリフットプリントを削減するため）；

Computing polynomial features;
多項式の特徴を計算する；

Representation learning (e.g., extract features using clustering, embeddings, or generative models);
表現学習（例：クラスタリング、埋め込み、または生成モデルを使用して特徴を抽出する）；

Computing aggregate features (e.g., count, min, max, stdev).
集計特徴（例：カウント、最小値、最大値、標準偏差）を計算する。

To illustrate the importance of feature engineering, let’s consider a classification task on a dataset with just one feature, x1, that looks like this:
特徴工学の重要性を説明するために、x1というたった1つの特徴を持つデータセットの分類タスクを考えてみよう：

We are doomed to fail if we try to fit a linear model directly to this dataset as it is not linearly separable.
このデータセットは線形分離可能ではないので、線形モデルを直接当てはめようとすると失敗する運命にある。
During feature engineering we can extract an additional feature, x2, where the function for deriving x2from the raw dataset is x2 = (x1)^2.
生データセットからx2を抽出する関数はx2 = (x1)^2である。
The resulting two-dimensional dataset might look like depicted in Figure 2.
その結果、二次元データセットは図2のようになる。

By adding an extra feature, the dataset becomes linearly separable and can be fitted by our model.
特徴量を追加することで、データセットは線形分離可能になり、我々のモデルでフィッティングできるようになる。
This was a simple example, in practice the process of feature engineering can involve much more complex transformations.
これは単純な例であり、実際にはフィーチャーエンジニアリングのプロセスはもっと複雑な変換を伴うことがある。

In the case of deep learning, deep models tend to perform better the more data they are trained on (more data samples during training can have a regularizing effect and combat overfitting).
ディープラーニングの場合、ディープモデルの性能は、より多くのデータでトレーニングされるほど向上する傾向がある（トレーニング中のデータサンプルが増えることで、正則化の効果が得られ、オーバーフィッティングに対抗できる）。
Consequently, a trend in machine learning is to train on increasingly larger datasets.
その結果、機械学習のトレンドは、ますます大規模なデータセットで学習することである。

This trend further complicates the feature engineering process as Data Engineers must think about scalability and efficiency in addition to the feature engineering logic.
データエンジニアはフィーチャーエンジニアリングのロジックに加え、スケーラビリティや効率性についても考えなければならないため、この傾向はフィーチャーエンジニアリングのプロセスをさらに複雑にしている。
With a standardized and scalable feature platform, the complexity of feature engineering can be managed more effectively.
標準化されたスケーラブルなフィーチャー・プラットフォームがあれば、フィーチャー・エンジニアリングの複雑さをより効果的に管理できる。

# Life Before the Feature Store フィーチャーストアの前の人生

In Figure 5, feature code is duplicated across training jobs and there are also features that have different implementations: one for training, and one for deployment (Inferencing) (Model C).
図5では、トレーニングジョブ間でフィーチャーコードが重複しており、実装が異なるフィーチャーも存在する： 1つはトレーニング用、もう1つはデプロイメント（Inferencing）用です（モデルC）。
Having different implementations for computing features for training and deployment entails non-DRY code and can lead to prediction problems.
トレーニング用とデプロイ用の特徴を計算するための異なる実装を持つことは、非乾燥コードを伴い、予測問題につながる可能性がある。

Moreover, without a feature store, features are typically not reusable as they are embedded in training/serving jobs.
さらに、フィーチャーストアがなければ、通常、フィーチャーはトレーニングやサービングジョブに組み込まれるため、再利用できません。
This also means that Data Scientists have to write low level code for accessing data stores, requiring data engineering skills.
これはまた、データサイエンティストがデータストアにアクセスするための低レベルのコードを書かなければならないことを意味し、データエンジニアリングのスキルが必要となる。
There is also no service to search for feature implementations, and there is no management or governance of features.
また、機能の実装を検索するサービスもなく、機能の管理やガバナンスもない。

# With a Feature Store フィーチャーストアを持つ

Data Scientists can now search for features, and with API support, easily use them to build models with minimal data engineering.
データサイエンティストは機能を検索し、APIのサポートにより、最小限のデータエンジニアリングでモデルを構築するためにそれらを簡単に使用できるようになった。
In addition, features can be cached and reused by other models, reducing model training time and infrastructure costs.
さらに、特徴をキャッシュして他のモデルで再利用できるため、モデルのトレーニング時間とインフラコストを削減できる。
Features are now a managed, governed asset in the Enterprise.
今やフィーチャーは、企業において管理され、統制された資産である。

# Economies of Scale for MLOps MLOのスケールメリット

A frequent pitfall for organizations that apply machine learning is to think of data science teams as individual groups that work independently with limited collaboration.
機械学習を適用する組織で陥りがちな落とし穴は、データ・サイエンス・チームを、限られた協力関係で独自に働く個々のグループと考えることだ。
Having this mindset results in machine learning workflows where there is no standardized way to share features across different teams and machine learning models.
このような考え方を持つと、異なるチームや機械学習モデル間で機能を共有するための標準化された方法がない機械学習ワークフローになる。

Not being able to share features across models and teams is limiting Data Scientist's productivity and makes it harder to build new models.
モデルやチーム間で機能を共有できないことは、データサイエンティストの生産性を制限し、新しいモデルを構築することを難しくしている。
By using a shared feature store, organizations can achieve an economies-of-scale effect.
共有フィーチャーストアを使用することで、組織は規模の経済効果を得ることができる。
When the feature store is built up with more features, it becomes easier and cheaper to build new models as the new models can re-use features that exist in the feature store.
フィーチャーストアがより多くのフィーチャーで構築されると、新しいモデルはフィーチャーストアに存在するフィーチャーを再利用できるため、新しいモデルを構築するのが容易になり、コストも安くなる。

# The Components of a Feature Store and a Comparison of Existing Feature Stores フィーチャーストアの構成要素と既存のフィーチャーストアの比較

During 2018, a number of large companies that are at the forefront of applying machine learning at scale announced the development of proprietary feature stores.
2018年、機械学習を大規模に適用する最前線にいる多くの大企業が、独自のフィーチャーストアの開発を発表した。
Uber, LinkedIn, and Airbnb built their feature stores on Hadoop data lakes, while Comcast built a feature store on an AWS data lake, and GO-JEK built a feature store on Google’s data platform.
Uber、LinkedIn、AirbnbはHadoopデータレイク上にフィーチャーストアを構築し、ComcastはAWSデータレイク上にフィーチャーストアを構築し、GO-JEKはGoogleのデータプラットフォーム上にフィーチャーストアを構築した。

These existing feature stores consist of five main components:
これらの既存のフィーチャーストアは、5つの主要コンポーネントで構成されている：

The feature engineering jobs, the computation of features, the dominant frameworks for feature computation are Samza (Uber [4]),Spark (Uber [4], Airbnb [5], Comcast [6]), Flink (Airbnb [5], Comcast [6]), and Beam (GO-JEK [7]).
特徴工学の仕事は、特徴の計算である。特徴計算のための主要なフレームワークは、Samza（Uber [4]）、Spark（Uber [4]、Airbnb [5]、Comcast [6]）、Flink（Airbnb [5]、Comcast [6]）、Beam（GO-JEK [7]）である。

The storage layer for storing feature data.
特徴データを保存するストレージ層。
Common solutions for storing features are Hive (Uber [4], Airbnb [5]), S3 (Comcast [6]), and BigQuery (GO-JEK [7]).
機能を保存するための一般的なソリューションは、Hive（Uber [4]、Airbnb [5]）、S3（Comcast [6]）、BigQuery（GO-JEK [7]）である。

The metadata layer used for storing code to compute features, feature version information, feature analysis data, and feature documentation.
フィーチャーを計算するコード、フィーチャーのバージョン情報、フィーチャーの分析データ、フィーチャーのドキュメントを格納するためのメタデータレイヤー。

The Feature Store API used for reading/writing features from/to the feature store.
フィーチャーストアAPIは、フィーチャーストアからフィーチャーを読み書きするために使用されます。

The feature registry, a user interface (UI) service where Data Scientists can share, discover, and order computation of features.
フィーチャー・レジストリは、データサイエンティストがフィーチャーを共有し、発見し、計算をオーダーできるユーザーインターフェース（UI）サービスです。

Before we dive into the feature store API and its usage, let’s have a look at the technology stack that we built our feature store on.
フィーチャーストアのAPIとその使い方に入る前に、フィーチャーストアを構築したテクノロジー・スタックを見てみよう。

# Hopsworks Feature Store Architecture ホップワークス特集 店舗建築

The architecture of the feature store is depicted in Figure 8.
特徴ストアのアーキテクチャを図8に示す。

# Feature Engineering Frameworks フィーチャーエンジニアリングのフレームワーク

At Hopsworks we specialize in Python-first ML pipelines, and for feature engineering we focus our support on Spark, PySpark, Numpy, and Pandas.
ホップワークスではPythonファーストのMLパイプラインを専門としており、フィーチャーエンジニアリングではSpark、PySpark、Numpy、Pandasのサポートに注力しています。
The motivation for using Spark/PySpark to do feature engineering is that it is the preferred choice for data wrangling among our users that are working with large-scale datasets.
Spark/PySparkをフィーチャーエンジニアリングに使用する動機は、大規模なデータセットを扱うユーザーの間で、データ操作にSpark/PySparkが選ばれているからです。

However, we have also observed that users working with small datasets prefer to do the feature engineering with frameworks such as Numpy and Pandas, which is why we decided to provide native support for those frameworks as well.
しかし、小規模なデータセットを扱うユーザーは、NumpyやPandasのようなフレームワークを使ってフィーチャー・エンジニアリングを行うことを好むということがわかりました。
Users can submit feature engineering jobs on the Hopsworks platform using notebooks, python files, or .jar files.
ユーザーは、ノートブック、pythonファイル、または.jarファイルを使用して、Hopsworksプラットフォーム上でフィーチャーエンジニアリングジョブを提出することができます。

# The Storage Layer ストレージ層

We have built the storage layer for the feature data on top of Hive/HopsFS with additional abstractions for modeling feature data.
私たちは、Hive/HopsFSの上に、特徴データをモデル化するための抽象化機能を追加して、特徴データのストレージレイヤーを構築しました。

The reason for using Hive as the underlying storage layer is two-fold: (1) it is not uncommon that our users are working with datasets in terabyte-scale or larger, demanding scalable solutions that can be deployed on HopsFS (see blog post on HopsFS [9]); and (2) data modeling of features is naturally done in a relational manner, grouping relational features into tables and using SQL to query the feature store.
Hiveを基盤となるストレージレイヤーとして使用する理由は2つあります： (1)我々のユーザーはテラバイトスケール以上のデータセットを扱うことが珍しくなく、HopsFS上で展開可能なスケーラブルなソリューションが要求される（HopsFSに関するブログ記事[9]を参照）、(2)特徴量のデータモデリングは当然リレーショナルな方法で行われ、リレーショナルな特徴量をテーブルにグループ化し、SQLを使用して特徴量ストアをクエリする。

This type of data modelling and access patterns fits well with Hive in combination with columnar storage formats such as Parquet or ORC.
このようなデータモデリングとアクセスパターンは、ParquetやORCのようなカラム型ストレージフォーマットと組み合わせたHiveに適している。

# The Metadata Layer メタデータ層

To provide automatic versioning, documentation, feature analysis, and feature sharing we store extended metadata about features in a metadata store.
自動バージョニング、文書化、機能分析、機能共有を提供するために、機能に関する拡張メタデータをメタデータストアに保存する。
For the metadata store we utilize NDB (MySQL Cluster) which allows us to keep feature metadata that is strongly consistent with other metadata in Hopsworks, such as metadata about feature engineering jobs and datasets.
メタデータ・ストアにはNDB（MySQL Cluster）を利用しており、フィーチャー・エンジニアリング・ジョブやデータセットに関するメタデータなど、Hopsworksの他のメタデータと強い一貫性を持つフィーチャー・メタデータを保持することができる。

# Feature Data Modeling フィーチャー・データ・モデリング

We introduce three new concepts to our users for modeling data in the feature store.
フィーチャーストアのデータをモデル化するために、3つの新しいコンセプトをユーザーに紹介します。

The feature is an individual versioned and documented data column in the feature store, e.g., the average rating of a customer.
フィーチャーとは、フィーチャーストアの個々のバージョン管理され、文書化されたデータ列のことで、例えば顧客の平均評価などである。

The feature group is a documented and versioned group of features stored as a Hive table.
機能グループは、Hiveテーブルとして格納された、文書化されバージョン管理された機能グループです。
The feature group is linked to a specific Spark/Numpy/Pandas job that takes in raw data and outputs the computed features.
特徴グループは、生データを取り込み、計算された特徴を出力する特定のSpark/Numpy/Pandasジョブにリンクされている。

The training dataset is a versioned and managed dataset of features and labels (potentially from multiple different feature groups).
トレーニングデータセットは、バージョン管理された特徴量とラベルのデータセットである（複数の異なる特徴グループの可能性がある）。
Training datasets are stored in HopsFS as tfrecords, parquet, csv, tsv, hdf5, or .npy files.
トレーニングデータセットは、tfrecords、parquet、csv、tsv、hdf5、または.npyファイルとしてHopsFSに保存されます。

When designing feature groups, it is a best-practice to let all features that are computed from the same raw datasets to be in the same feature group.
特徴グループを設計する場合、同じ生データセットから計算されたすべての特徴を同じ特徴グループにするのがベストプラクティスです。
It is common that there are several feature groups that share a common column, such as a timestamp or a customer-id, that allows feature groups to be joined together into a training dataset.
タイムスタンプやcustomer-idのような共通のカラムを持つ特徴グループが複数存在することが一般的であり、そのような特徴グループを結合してトレーニングデータセットとすることができる。

# The Feature Store API フィーチャーストア API

The feature store has two interfaces; one interface for writing curated features to the feature store and one interface for reading features from the feature store to use for training or serving.
特徴ストアには2つのインターフェイスがあり、1つはキュレーションされた特徴を特徴ストアに書き込むためのインターフェイス、もう1つは特徴ストアから特徴を読み込んでトレーニングやサービングに使用するためのインターフェイスである。

## Creating Features 機能の作成

The feature store is agnostic to the method for computing the features.
特徴ストアは、特徴の計算方法には関係ない。
The only requirement is that the features can be grouped together in a Pandas, Numpy, or Spark dataframe.
唯一の要件は、特徴がPandas、Numpy、またはSparkのデータフレームにまとめられることです。
The user provides a dataframe with features and associated feature metadata (metadata can also be edited later through the feature registry UI) and the feature store library takes care of creating a new version of the feature group, computing feature statistics, and linking the features to the job to compute them.
ユーザーは、フィーチャーと関連するフィーチャーメタデータを含むデータフレームを提供し（メタデータは、フィーチャーレジストリUIを通じて後で編集することもできる）、フィーチャーストアライブラリは、フィーチャーグループの新しいバージョンの作成、フィーチャー統計の計算、フィーチャーを計算するジョブへのリンクの世話をする。

Insert Features
インサート機能

Create Feature Group
フィーチャー・グループの作成

## Reading From the Feature Store (Query Planner) フィーチャーストアからの読み込み (クエリプランナー)

To read features from the feature store, users can use either SQL or APIs in Python and Scala.
フィーチャーストアからフィーチャーを読み込むには、SQLかPythonやScalaのAPIを使用する。
Based on our experience with users on our platform, Data Scientists can have diverse backgrounds.
私たちのプラットフォームのユーザーとの経験に基づいて、データサイエンティストは多様な背景を持つことができます。
Although some Data Scientists are very comfortable with SQL, others prefer higher level APIs.
SQLを使いこなすデータサイエンティストもいれば、より高度なAPIを好むデータサイエンティストもいる。

This motivated us to develop a query-planner to simplify user queries.
このことが、ユーザーのクエリーを簡素化するクエリープランナーを開発する動機となった。
The query-planner enables users to express the bare minimum information to fetch features from the feature store.
クエリプランナーは、ユーザーがフィーチャーストアからフィーチャーを取得するために必要最低限の情報を表現することを可能にします。

For example, a user can request 100 features that are spread across 20 different feature groups by just providing a list of feature names.
例えば、ユーザーは機能名のリストを提供するだけで、20の異なる機能グループにまたがる100の機能をリクエストすることができる。
The query-planner uses the metadata in the feature store to infer where to fetch the features from and how to join them together.
クエリプランナは、フィーチャストアのメタデータを使用して、フィーチャをどこから取得し、どのように結合するかを推測する。

To fetch the features “average_attendance” and “average_player_age” from the feature store, all the user has to write is this.
フィーチャーストアから "average_attendance "と "average_player_age "のフィーチャーをフェッチするには、ユーザーは次のように書くだけでよい。

# Creating training datasets トレーニングデータセットの作成

Organizations typically have many different types of raw datasets that can be used to extract features.
組織には通常、特徴を抽出するために使用できるさまざまな種類の未加工データセットがある。
For example, in the context of user recommendation there might be one dataset with demographic data of users and another dataset with user activities.
例えば、ユーザー推薦の文脈では、ユーザーの人口統計データを含むデータセットと、ユーザーのアクティビティを含むデータセットがあるかもしれない。
Features from the same dataset are naturally grouped into a feature group, and it is common to generate one feature group per dataset.
同じデータセットからの特徴は自然に特徴グループにまとめられ、データセットごとに1つの特徴グループを生成するのが一般的です。

When training a model, you want to include all features that have predictive power for the prediction task, these features can potentially span multiple feature groups.
モデルをトレーニングするとき、予測タスクに対して予測力を持つすべての特徴を含めたい。これらの特徴は、複数の特徴グループにまたがる可能性がある。
The training dataset abstraction in the Hopsworks Feature Store is used for this purpose.
この目的のために、Hopsworks Feature Storeのトレーニングデータセット抽象化が使用される。
The training dataset allows users to group a set of features with labels for training a model to do a particular prediction task.
トレーニングデータセットは、特定の予測タスクを実行するモデルをトレーニングするために、ユーザーがラベルを持つ特徴のセットをグループ化することを可能にする。

Once a user has fetched a set of features from different feature groups in the feature store, the features can be joined with labels (in case of supervised learning) and materialized into a training dataset.
一旦、ユーザが特徴ストア内の異なる特徴グループから特徴セットを取得すると、（教師あり学習の場合）その特徴はラベルと結合され、トレーニングデータセットに具体化される。

By creating a training dataset using the feature store API, the dataset becomes managed by the feature store.
フィーチャーストアAPIを使ってトレーニングデータセットを作成することで、そのデータセットはフィーチャーストアによって管理されるようになる。
Managed training datasets are automatically analyzed for data anomalies, versioned, documented, and shared with the organization.
管理されたトレーニングデータセットは、データの異常がないか自動的に分析され、バージョン管理、文書化され、組織と共有される。

To create a managed training dataset, the user supplies a Pandas, Numpy or Spark dataframe with features, labels, and metadata.
管理されたトレーニングデータセットを作成するには、ユーザーは特徴、ラベル、メタデータを含むPandas、Numpy、またはSparkデータフレームを提供します。

# The Feature Registry 特集レジストリ

The feature registry is the user interface for publishing and discovering features and training datasets.
フィーチャーレジストリは、フィーチャーとトレーニングデータセットを公開・発見するためのユーザーインターフェースである。
The feature registry also serves as a tool for analyzing feature evolution over time by comparing feature versions.
フィーチャーレジストリは、フィーチャーのバージョンを比較することで、時間経過に伴うフィーチャーの進化を分析するツールとしても機能する。
When a new data science project is started, Data Scientists within the project typically begin by scanning the feature registry for available features, and only add new features for their model that do not already exist in the feature store.
新しいデータサイエンス・プロジェクトが開始されると、プロジェクト内のデータサイエンティストは通常、利用可能なフィーチャーがないかフィーチャーレジストリをスキャンすることから始め、フィーチャーストアにまだ存在しない新しいフィーチャーだけをモデルに追加します。

The feature registry provides :
機能レジストリは、：

Keyword search on feature/feature group/training dataset metadata.
特徴/特徴グループ/トレーニングデータセットのメタデータをキーワード検索。

Create/Update/Delete/View operations on feature/feature group/training dataset metadata.
フィーチャ/フィーチャグループ/トレーニングデータセットのメタデータの作成/更新/削除/表示操作。

Automatic feature analysis.
自動特徴分析。

Feature dependency tracking.
機能依存性の追跡。

Feature job tracking.
ジョブ追跡機能を搭載。

Feature data preview.
特集データのプレビュー。

# Automatic Feature Analysis 自動フィーチャー分析

When a feature group or training dataset is updated in the feature store, a data analysis step is performed.
特徴ストア内の特徴グループまたはトレーニングデータセットが更新されると、データ分析ステップが実行される。
In particular, we look at cluster analysis, feature correlation, feature histograms, and descriptive statistics.
特に、クラスター分析、特徴相関、特徴ヒストグラム、記述統計について見ていきます。

We have found that these are the most common type of statistics that our users find useful in the feature modeling phase.
これらの統計は、ユーザーが特徴モデリング段階で役に立つと思う最も一般的な統計のタイプであることがわかりました。
For example, feature correlation information can be used to identify redundant features, feature histograms can be used to monitor feature distributions between different versions of a feature to discover covariate shift, and cluster analysis can be used to spot outliers.
例えば、特徴相関情報は冗長な特徴を特定するために使用でき、特徴ヒストグラムは共変量シフトを発見するために特徴の異なるバージョン間の特徴分布を監視するために使用でき、クラスター分析は外れ値を発見するために使用できる。
Having such statistics accessible in the feature registry helps users decide on which features to use.
機能レジストリでこのような統計にアクセスできることは、ユーザーがどの機能を使うかを決めるのに役立つ。

# Feature Dependencies and Automatic Backfilling 機能の依存性と自動バックフィル

When the feature store increases in size, the process of scheduling jobs to recompute features should be automated to avoid a potential management bottleneck.
フィーチャーストアのサイズが大きくなった場合、フィーチャーを再計算するジョブのスケジューリングプロセスは、潜在的な管理のボトルネックを避けるために自動化されるべきである。
Feature groups and training datasets in Hopsworks feature store are linked to Spark/Numpy/Pandas jobs which enables the reproduction and recompution of the features when necessary.
Hopsworksフィーチャーストアのフィーチャーグループとトレーニングデータセットは、Spark/Numpy/Pandasのジョブにリンクされており、必要に応じてフィーチャーの再生成と再計算が可能です。

Moreover, each feature group and training dataset can have a set of data dependencies.
さらに、各特徴グループとトレーニングデータセットは、一連のデータ依存関係を持つことができる。
By linking feature groups and training datasets to jobs and data dependencies, the features in the Hopsworks feature store can be automatically backfilled using workflow management systems such as Airflow [10].
フィーチャーグループとトレーニングデータセットをジョブやデータ依存関係にリンクさせることで、Hopsworksフィーチャーストアのフィーチャーは、Airflow [10]のようなワークフロー管理システムを使用して自動的にバックフィルされます。

# A Multi-Tenant Feature Store Service マルチテナント型フィーチャーストアサービス

We believe that the biggest benefit of a feature store comes when it is centralized across the entire organization.
フィーチャーストアの最大のメリットは、組織全体で一元化されたときに生まれると私たちは考えています。
The more high-quality features available in the feature store the better.
フィーチャーストアに用意されている機能は、高品質であればあるほど良い。
For example, in 2017 Uber reported that they had approximately 10000 features in their feature store [11].
例えば、2017年のUberは、フィーチャーストアに約10000のフィーチャーがあると報告している[11]。

Despite the benefit of centralizing features, we have identified a need to enforce access control to features.
機能を一元化することの利点にもかかわらず、機能へのアクセス制御を強制する必要性があることがわかった。
Several organizations that we have talked to are working partially with sensitive data that requires specific access rights that is not granted to everyone in the organization.
私たちが話を聞いたいくつかの組織は、組織内の全員に付与されていない特定のアクセス権を必要とする機密データを部分的に扱っている。
For example, it might not be feasible to publish features that are extracted from sensitive data to a feature store that is public within the organization.
例えば、機密性の高いデータから抽出された特徴を、組織内で公開されている特徴ストアに公開することは現実的ではないかもしれない。

To solve this problem we utilize the multi-tenancy property built-in to the architecture of the Hopsworks platform [12].
この問題を解決するために、私たちはHopsworksプラットフォーム[12]のアーキテクチャに組み込まれたマルチテナンシー特性を利用している。
Feature stores in Hopsworks are by default project-private and can be shared across projects, which means that an organization can combine public and private feature stores.
Hopsworksのフィーチャーストアは、デフォルトではプロジェクト・プライベートであり、プロジェクト間で共有することができます。
An organization can have a central public feature store that is shared with everyone in the organization as well as private feature stores containing features of sensitive nature that are only accessible by users with the appropriate permissions.
組織は、組織内の全員が共有する中央のパブリック機能ストアと、適切な権限を持つユーザーのみがアクセスできる、機密性の高い機能を含むプライベート機能ストアを持つことができます。

# Future Work 今後の課題

The feature store covered in this blog post is a so called batch feature store, meaning that it is a feature store designed for training and non-real time model serving.
このブログポストで取り上げるフィーチャーストアは、いわゆるバッチフィーチャーストアと呼ばれるもので、トレーニングや非リアルタイムのモデル提供のために設計されたフィーチャーストアという意味です。
In future work, we plan to extend the feature store to meet real-time guarantees that are required during serving of user-facing models.
将来的には、ユーザー向けモデルの提供時に要求されるリアルタイムの保証を満たすために、特徴ストアを拡張する予定である。

Moreover, we are currently in the process of evaluating the need for a Domain Specific Language (DSL) for feature engineering.
さらに現在、フィーチャーエンジニアリングのためのドメイン固有言語（DSL）の必要性を評価しているところです。
By using a DSL, users that are not proficient in Spark/Pandas/Numpy can provide an abstract declarative description of how features should be extracted from raw data and then the library translates that description into a Spark job for computing the features.
DSLを使用することで、Spark/Pandas/Numpyに習熟していないユーザは、生データからどのように特徴を抽出すべきかという抽象的な宣言的記述を提供することができ、ライブラリはその記述を特徴を計算するためのSparkジョブに変換する。

Finally, we are also looking into supporting Petastorm [13] as a data format for training datasets.
最後に、トレーニングデータセットのデータ形式としてPetastorm [13]のサポートも検討している。
By storing training datasets in Petastorm we can feed Parquet data directly into machine learning models in an efficient manner.
Petastormにトレーニングデータセットを保存することで、Parquetデータを直接機械学習モデルに効率的に送り込むことができます。
We consider Petastorm as a potential replacement for tfrecords, that can make it easier to re-use training datasets for other ML-frameworks than Tensorflow, such as PyTorch.
Petastormは、Tensorflow以外のMLフレームワーク（PyTorchなど）の学習データセットの再利用を容易にする、tfrecordsの代替となりうるものと考えています。

# Summary 要約

Building successful AI systems is hard.
成功するAIシステムを構築するのは難しい。
At Hopsworks we have observed that our users spend a lot of effort on the Data Engineering phase of machine learning.
ホップワークスでは、ユーザーが機械学習のデータエンジニアリング段階に多くの労力を費やしていることを確認しています。
From the release of version 0.8.0, Hopsworks provides the world’s first open-source feature store.
バージョン0.8.0のリリースから、ホップワークスは世界初のオープンソース機能ストアを提供します。
A feature store is a data management layer for machine learning that allows Data Scientists and Data Engineers to share and discover features, better understand features over time, and effectivize the machine learning workflow.
フィーチャーストアは、データサイエンティストとデータエンジニアがフィーチャーを共有・発見し、時系列でフィーチャーをより良く理解し、機械学習のワークフローを効率化することを可能にする、機械学習のためのデータ管理レイヤーである。

‍
‍