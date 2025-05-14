- refs: https://neptune.ai/blog/feature-stores-components-of-a-data-science-factory-guide

# Feature Stores: Components of a Data Science Factory [Guide] 特徴ストア：データサイエンスファクトリーの構成要素 [ガイド]
Sumit Saha
21st August, 2023 2023年8月21日

Ineffective and expensive feature engineering practices often plague companies that work with large amounts of data. 
効果的でない高コストの特徴エンジニアリング手法は、大量のデータを扱う企業をしばしば悩ませます。 
This keeps them from organizing a sophisticated machine learning operation. 
これにより、彼らは洗練された機械学習の運用を整えることができません。 
A lot of time is spent fetching the data for ML purposes, but it’s unclear whether there are any inconsistencies between ingestion and service of models. 
機械学習の目的でデータを取得するのに多くの時間が費やされますが、モデルの取り込みとサービスの間に不整合があるかどうかは不明です。 

As a result of this slowed-down process and inability to reproduce results, project stakeholders may lose trust in positive ML outcomes. 
このプロセスの遅延と結果を再現できないことの結果として、プロジェクトの利害関係者はポジティブな機械学習の成果に対する信頼を失う可能性があります。 
How can we avoid this situation? 
この状況をどのように回避できますか？

The Feature Store is part of the answer. 
特徴ストアはその答えの一部です。 
It’s a crucial part of the data science infrastructure, meant to establish a stable pipeline for end users. 
それは、エンドユーザーのために安定したパイプラインを確立することを目的としたデータサイエンスインフラストラクチャの重要な部分です。

## What is a Feature Store? 特徴ストアとは？

A Feature Store is a service that ingests large volumes of data, computes features, and stores them. 
特徴ストアは、大量のデータを取り込み、特徴を計算し、それを保存するサービスです。
With a Feature Store, machine learning pipelines and online applications have easy access to data. 
特徴ストアを使用することで、機械学習パイプラインやオンラインアプリケーションはデータに簡単にアクセスできます。

Implemented as a dual-database, Feature Stores are designed to serve data both in real-time and to be processed in batches: 
特徴ストアはデュアルデータベースとして実装されており、リアルタイムでデータを提供することと、バッチ処理を行うことの両方に対応するように設計されています。

- Online feature stores serve online applications with data at a low-latency. 
- オンラインフィーチャーストアは、低遅延でオンラインアプリケーションにデータを提供します。
Examples include MySQL Cluster, Redis, Cassandra DB, etc. 
例としては、MySQL Cluster、Redis、Cassandra DBなどがあります。

- Offline feature stores are scale-out SQL databases that provide data for developing AI models and make feature governance possible for explainability and transparency. 
- オフラインフィーチャーストアは、AIモデルの開発のためにデータを提供し、説明可能性と透明性のためのフィーチャーガバナンスを可能にするスケールアウトSQLデータベースです。
Examples include Hive, BigQuery, Parquet. 
例としては、Hive、BigQuery、Parquetなどがあります。



### Feature Store vs Data Lake vs Data Warehouse

At an abstract level, Feature Stores offer a subset of the functionalities of a Data Lake. 
**抽象的なレベルでは、Feature StoresはData Lakeの機能の一部を提供します**。
Feature Stores are specialized in storing features for machine learning applications, and Data Lakes are a centralized repository for data that goes beyond features, used for analytical purposes as well. 
Feature Storesは機械学習アプリケーションのための特徴を保存することに特化しており、Data Lakesは特徴を超えたデータのための中央集権的なリポジトリであり、分析目的でも使用されます。
On the other hand, data warehouses provide a relational database with a schema to be used by business analysts for generation reports, dashboards and more by writing queries in SQL. 
一方、データウェアハウスは、ビジネスアナリストがSQLでクエリを記述してレポート、ダッシュボードなどを生成するために使用するスキーマを持つリレーショナルデータベースを提供します。

### Issues associated with Feature Engineering 特徴エンジニアリングに関連する問題

- **Dynamic nature of feature definitions**:A particular feature might end up having different definitions across multiple teams within the organization. 
- 特徴の定義の動的な性質：特定の特徴は、組織内の複数のチームで異なる定義を持つことがあります。 
If not properly documented, it gets increasingly difficult to maintain the logic behind the feature and the information conveyed by it. 
適切に文書化されていない場合、特徴の背後にある論理やそれによって伝えられる情報を維持することがますます難しくなります。 
Feature Stores aid this problem by maintaining the de-facto definition associated with the feature. 
Feature Storesは、特徴に関連する事実上の定義を維持することでこの問題を助けます。 
This makes it easier for the end-users of the data, and maintains consistency in the results derived from that data. 
これにより、データのエンドユーザーが容易になり、そのデータから得られる結果の一貫性が維持されます。

- **Redundancy of features**:When data has to be sourced in raw form, data scientists spend a lot of time re-extracting features that might have been already extracted by others in the team or by pipelines currently using the data. 
- 特徴の冗長性：データが生の形で取得されなければならない場合、データサイエンティストは、チーム内の他の人や現在データを使用しているパイプラインによってすでに抽出されている可能性のある特徴を再抽出するのに多くの時間を費やします。 
Since Feature Stores provide a single source of truth, data scientists can spend less time on feature engineering, and more time on experimenting and building. 
Feature Storesは単一の真実のソースを提供するため、データサイエンティストは特徴エンジニアリングにかける時間を減らし、実験や構築にもっと時間をかけることができます。

- Gap between experimentation and production environments:Products often use a handful of programming languages and frameworks, which could be different from the tools used to experiment with a machine learning model. 
- 実験環境と生産環境のギャップ：製品はしばしば少数のプログラミング言語やフレームワークを使用し、これらは機械学習モデルの実験に使用されるツールとは異なる可能性があります。 
This gap can cause inconsistencies that may get overlooked, and ultimately worsen the model/product on the customer’s end. 
このギャップは見落とされる可能性のある不整合を引き起こし、最終的には顧客側のモデル/製品を悪化させる可能性があります。 
In other words, the expected behavior/performance of the model in development should more or less be reproducible when deployed in the product. 
言い換えれば、開発中のモデルの期待される動作/パフォーマンスは、製品に展開されたときにほぼ再現可能であるべきです。 
With Feature Stores, this transformation is unnecessary, as they maintain consistency between experimentation and production. 
Feature Storesを使用すると、この変換は不要であり、**実験と生産の間の一貫性を維持**します。

<!-- ここまで読んだ! -->

### Benefits of a Feature Store in ML pipelines 機械学習パイプラインにおけるフィーチャーストアの利点

The output from Feature Stores is implementation-agnostic. 
フィーチャーストアからの出力は、実装に依存しません。
No matter which algorithm or framework we use, the application/model will get data in a consistent format. 
**どのアルゴリズムやフレームワークを使用しても、アプリケーション/モデルは一貫した形式でデータを受け取ります**。
Another major benefit of using a Feature Store is saving time that would otherwise be spent computing features. 
フィーチャーストアを使用するもう一つの大きな利点は、特徴量を計算するのに費やされるはずの時間を節約できることです。
(Feature Pipelineが事前計算しておくからってことだよね? :thinking:)

### Components of a Feature Store 機能ストアの構成要素

- Feature Registry:Feature Registry provides a central interface that can be used by data consumers, for example data scientists, to maintain a list of features along with their definitions and metadata. 
- **Feature Registry**:フィーチャーレジストリは、データ消費者（例えばデータサイエンティスト）が特徴のリストとその定義およびメタデータを維持するために使用できる中央インターフェースを提供します。
This central repository can be updated to meet your needs.
この中央リポジトリは、ニーズに応じて更新できます。

- Operational Monitoring:Machine learning models may perform well during initial stages, but you must still monitor them for correctness and reliable results over time. 
- オペレーショナルモニタリング:機械学習モデルは初期段階では良好に機能するかもしれませんが、時間の経過とともに正確性と信頼性のある結果を監視する必要があります。
There’s always the possibility of a degrading relationship between the independent and dependent variables in a machine learning model. 
機械学習モデルにおいて、独立変数と従属変数の関係が劣化する可能性は常に存在します。
This is primarily due to the complex nature of incoming data, because of which the predictions become more unstable and less accurate with time. 
これは主に、受信データの複雑な性質によるもので、予測が時間とともにより不安定で正確性が低下します。
This phenomenon is called Model Drift and can be classified into two types: 
**この現象はモデルドリフトと呼ばれ、2つのタイプに分類できます**：
Concept Drift:Statistical properties of the target variable change over time. 
概念ドリフト:ターゲット変数の統計的特性が時間とともに変化します。
Data Drift:Statistical properties of the predictor variable change over time. 
データドリフト:予測変数の統計的特性が時間とともに変化します。

The Feature Store maintains data quality and correctness. 
フィーチャーストアはデータの品質と正確性を維持します。
It provides an interface to internal and external applications/tools to ensure proper model performance in production. 
内部および外部のアプリケーション/ツールに対してインターフェースを提供し、プロダクションでの適切なモデルパフォーマンスを確保します。

- **Transform**:In machine learning applications, data transformation pipelines absorb raw data and transform it into usable features. 
- 変換:機械学習アプリケーションでは、データ変換パイプラインが生データを取り込み、使用可能な特徴に変換します。
Feature Stores are responsible for managing and orchestrating them. 
**フィーチャーストアはそれらを管理し、調整する責任があります。(Feature Pipelineの管理をfeature storeがする、という考え方か...!これはいろいろな考え方がありそう...!**:thinking:)
There are three main types of transformations: 
**変換には主に3つのタイプが**あります：
- Stream for data with velocity (for example real-time logs), 
ストリーム:速度のあるデータ（例えばリアルタイムログ）用、
- Batch for stationary data, 
バッチ:静的データ用、
- On-demand for data that cannot be pre-computed. 
オンデマンド:事前に計算できないデータ用。

- Storage: Features that are not immediately required are offline, and usually stored in warehouses such as Snowflake, Hive, or Redshift. 
- **ストレージ**: すぐに必要でない特徴はオフラインで、通常はSnowflake、Hive、またはRedshiftなどのウェアハウスに保存されます。
On the other hand, online features are required in real-time and stored in databases such as MongoDB, CassandraDB, or Elasticsearch, with low-latency capabilities. 
一方、オンライン特徴はリアルタイムで必要とされ、MongoDB、CassandraDB、またはElasticsearchなどのデータベースに保存され、低遅延の機能を持っています。

- Serving:The logic behind feature extraction and processing is abstracted, which makes Feature Stores very attractive. 
- **サービング**: **特徴抽出と処理の背後にあるロジックは抽象化されており、フィーチャーストアは非常に魅力的**です。(うんうんメリットの1つ...!:thinking:)
While data scientists access the snapshot of data (point-in-time) for experimentation purposes, 
データサイエンティストは実験目的でデータのスナップショット（時点）にアクセスしますが、
Feature Stores ensure that these features are constantly updated in real-time, and readily available to the applications that need them. 
フィーチャーストアは、これらの特徴がリアルタイムで常に更新され、必要とするアプリケーションにすぐに利用可能であることを保証します。

<!-- ここまで読んだ! -->

## Feature Stores and MLOps 特徴ストアとMLOps  
### What is MLOps? MLOpsとは何か？

MLOps is about applying DevOps principles to building, testing and deploying machine learning pipelines. 
MLOpsは、機械学習パイプラインの構築、テスト、展開にDevOpsの原則を適用することに関するものです。
With MLOps practices, teams can deploy better models, more frequently. 
MLOpsの実践により、チームはより良いモデルをより頻繁に展開することができます。

Challenges of MLOps include: 
MLOpsの課題には以下が含まれます：
- data versioning, 
- データのバージョニング、
- managing specialised hardware (GPUs, etc.), 
- 専門的なハードウェア（GPUなど）の管理、
- managing data governance and compliance for models. 
- モデルのデータガバナンスとコンプライアンスの管理。

### RELATED ARTICLES 関連記事

MLOps: What It Is, Why it Matters, and How To Implement It
MLOps：それが何であるか、なぜ重要であるか、そしてどのように実装するか

The Best MLOps Tools You Need to Know as a Data Scientist
データサイエンティストとして知っておくべき最高のMLOpsツール

<!-- ここまで読んだ! -->

### MLOps vs DevOps

Traditionally, developers use Git to version control code over time, which is necessary for automation and continuous integration (CI). 
従来、開発者はGitを使用してコードのバージョン管理を行い、これは自動化と継続的インテグレーション（CI）に必要です。
This makes it easy to automatically reproduce an environment. 
これにより、環境を自動的に再現することが容易になります。

Every commit to Git triggers the automated creation of packages that can be deployed using information in version control. 
Gitへのすべてのコミットは、バージョン管理の情報を使用してデプロイ可能なパッケージの自動作成をトリガーします。
Jenkins is used alongside version control software to build, test and deploy code, so that it behaves in a controlled and predictable way. 
Jenkinsは、バージョン管理ソフトウェアとともに使用され、コードをビルド、テスト、デプロイするために使用され、制御された予測可能な方法で動作します。
The steps involved with Jenkins are: 
Jenkinsに関わるステップは次のとおりです：

1. Provisioning of Virtual Machines (VMs)/containers. 
   1. 仮想マシン（VM）/コンテナのプロビジョニング。
2. Fetching code onto these machines. 
   2. これらのマシンにコードを取得する。
3. Compiling the code. 
   3. コードをコンパイルする。
4. Running tests. 
   4. テストを実行する。
5. Packaging binaries. 
   5. バイナリをパッケージ化する。
6. Deploying binaries. 
   6. バイナリをデプロイする。

The most important part of MLOps is versioning data. 
**MLOpsの最も重要な部分はデータのバージョン管理**です。(ほうほう...!)
You can’t do it with Git, as it doesn’t scale to large volumes of data. 
Gitでは大規模なデータにスケールしないため、これを行うことはできません。
A simple machine learning pipeline consists of the following: 
シンプルな機械学習パイプラインは次のような構成になります：

- Validated incoming data. 
  - 検証済みの受信データ。
- Computation of features. 
  - 特徴の計算。
- Generation of training and testing data. 
  - トレーニングデータとテストデータの生成。
- Training of the model. 
  - モデルのトレーニング。
- Validation of the model. 
  - モデルの検証。
- Model deployment. 
  - モデルのデプロイ。
- Monitoring the model in production. 
  - 本番環境でのモデルの監視。

This can get even more complex when you add hyperparameter tuning, model explainability and distributed training into the picture. 
ハイパーパラメータの調整、モデルの説明可能性、分散トレーニングを追加すると、さらに複雑になる可能性があります。

Orchestration frameworks help in automatic workflow execution, model retraining, data passing between components, and workflow triggering based on events. 
オーケストレーションフレームワークは、自動ワークフローの実行、モデルの再トレーニング、コンポーネント間のデータの受け渡し、イベントに基づくワークフローのトリガーに役立ちます。
Some of these frameworks are: 
これらのフレームワークのいくつかは次のとおりです：

- TensorFlow Extended (TFX) – supports Airflow, Beam, Kubeflow pipelines 
  - TensorFlow Extended (TFX) – Airflow、Beam、Kubeflowパイプラインをサポート
- Hopsworks – supports Airflow 
  - Hopsworks – Airflowをサポート
- MLFlow – supports Spark 
  - MLFlow – Sparkをサポート
- Kubeflow – supports Kubeflow pipelines 
  - Kubeflow – Kubeflowパイプラインをサポート

TFX, MLFlow and Hopsworks support distributed processing with Beam and Spark to enable scale-out of execution on clusters using large amounts of data. 
TFX、MLFlow、およびHopsworksは、BeamおよびSparkを使用した分散処理をサポートし、大量のデータを使用したクラスターでの実行のスケールアウトを可能にします。

### Machine Learning pipelines 機械学習パイプライン

DevOps CI/CD is mostly triggered by source code updates. 
DevOpsのCI/CDは主にソースコードの更新によってトリガーされます。
MLOps and DataOps CI/CD pipelines may be triggered not just by source code updates, but also data updates and data processing: 
**MLOpsおよびDataOpsのCI/CDパイプラインは、ソースコードの更新だけでなく、データの更新やデータ処理によってもトリガーされる可能性があります**：
- DataOps mostly automates the testing and deployment of data pipelines, 
- DataOpsは主にデータパイプラインのテストとデプロイを自動化します。
- MLOps automates the process of training, validating and deploying models. 
- MLOpsはモデルのトレーニング、検証、デプロイのプロセスを自動化します。

For end-to-end machine learning pipelines, you need very deliberate feature engineering. 
エンドツーエンドの機械学習パイプラインには、非常に意図的な特徴エンジニアリングが必要です。
This can take up the majority of your bandwidth. 
これは、あなたの帯域幅の大部分を占める可能性があります。
Feature Stores can help in two ways: 
フィーチャーストアは2つの方法で役立ちます：
- Ingesting data, validating it, and transforming it into consumable features. 
- データを取り込み、それを検証し、消費可能な特徴に変換します。
- Machine learning algorithms that consume this data get trained, validated and pushed into production. 
- このデータを消費する機械学習アルゴリズムは、トレーニングされ、検証され、プロダクションにプッシュされます。

The issue with machine learning pipelines is their stateful nature. 
機械学習パイプラインの問題は、その状態を持つ性質です。
A good data pipeline should be stateless and idempotent. 
**良いデータパイプラインは、無状態で冪等であるべき**です。(i.e. 再実行しても結果が変わらないデータパイプライン...!:thinking:)
In other words, we need a lot of information before deploying a new model (in validation stage) about how well it’s performing, what are the assumptions we’re making, the impact of the model, and so on. 
言い換えれば、新しいモデル（検証段階）をデプロイする前に、そのパフォーマンス、私たちが行っている仮定、モデルの影響などについて多くの情報が必要です。
Usually, developers end up re-writing code over and over again to define input and output properly. 
通常、開発者は**入力と出力を適切に定義するため**に、何度もコードを書き直すことになります。

Hopsworks offers an inobtrusive metadata model, where pipelines read/write to the HDFS and interact with the feature store using the Hopsworks API. 
Hopsworksは、パイプラインがHDFSに読み書きし、Hopsworks APIを使用してフィーチャーストアと対話する目立たないメタデータモデルを提供します。
This way we can store metadata, artifacts, model provenance and more, without re-writing code as required by TensorFlow Extended (TFX) or MLFlow. 
この方法により、TensorFlow Extended (TFX)やMLFlowが要求するようにコードを書き直すことなく、メタデータ、アーティファクト、モデルの出所などを保存できます。

Some of the industrial best practices along with relevant tools to help us achieve them are as follows – 
私たちがそれを達成するのを助けるためのいくつかの業界のベストプラクティスと関連ツールは以下の通りです –

- Unit test and continuous integration with Jenkins. 
- Jenkinsを使用した単体テストと継続的インテグレーション。
- Data validation using TFX or Deequ, so that features have expected values. 
- TFXまたはDeequを使用したデータ検証により、特徴が期待される値を持つようにします。
- Test for uniqueness, missingness and distinctiveness using Deequ. 
- Deequを使用して一意性、欠損、独自性をテストします。
- Check for data distribution validation using TFX or Deequ. 
- TFXまたはDeequを使用してデータ分布の検証をチェックします。
- Pairwise relationship between feature and with the target variable using Deequ. 
- Deequを使用して特徴とターゲット変数とのペアワイズ関係を確認します。
- Custom tests to measure cost of each feature. 
- 各特徴のコストを測定するためのカスタムテスト。
- Test for Personally Identifiable Information (PII) leaks. 
- 個人を特定できる情報（PII）の漏洩をテストします。

### READ ALSO 参照してください

The Best Feature Engineering Tools
最良の特徴エンジニアリングツール


<!-- ここまで読んだ! -->

## Feature Store architectures 特徴ストアアーキテクチャ  
### Uber’s Michelangelo Machine Learning platform UberのMichelangelo機械学習プラットフォーム

In 2017, Uber introduced Michelangelo as ML-as-a-service platform to make scaling up AI easy.  
2017年、UberはAIのスケーリングを容易にするために、MichelangeloをML-as-a-serviceプラットフォームとして導入しました。  
With an ever growing customer base and huge influx of rich data, Uber has deployed Michelangelo across its multiple data centers for running their online applications.  
増え続ける顧客基盤と豊富なデータの大量流入に伴い、Uberはオンラインアプリケーションを運営するために、複数のデータセンターにMichelangeloを展開しました。  
The platform was born out of a necessity.  
このプラットフォームは必要性から生まれました。  
Before Michelangelo, data scientists and engineers had to create separate predictive models and bespoke systems which in terms of scaling up was not sustainable.  
Michelangelo以前は、データサイエンティストやエンジニアは、スケーリングの観点から持続可能ではない別々の予測モデルや特注システムを作成しなければなりませんでした。  

Michelangelo is built on top of Uber’s infrastructure, with components that are built in-house as a bootstrap of mature open-source frameworks such as HDFS, Spark, XGBoost, or TensorFlow.  
Michelangeloは、HDFS、Spark、XGBoost、またはTensorFlowなどの成熟したオープンソースフレームワークのブートストラップとして社内で構築されたコンポーネントを持つUberのインフラストラクチャの上に構築されています。  
It provides a Data Lake for all transactional data.  
すべてのトランザクションデータのためのデータレイクを提供します。  
Kafka brokers are deployed to aggregate data from all of Uber’s services, and streamed via Samza compute engine with Cassandra clusters.  
Kafkaブローカーは、Uberのすべてのサービスからデータを集約するために展開され、Cassandraクラスターを使用してSamzaコンピュートエンジン経由でストリーミングされます。  

The platform uses Hive/HDFS to store Uber’s transactional and log data.  
このプラットフォームは、Uberのトランザクションデータとログデータを保存するためにHive/HDFSを使用しています。 
Features needed for online models are precomputed and stored in CassandraDB, where they can be read at a low-latency at prediction time.  
**オンラインモデルに必要な特徴は事前に計算され、CassandraDBに保存され**、予測時に低遅延で読み取ることができます。  

For feature selection, transformation, and to ensure that input data is checked for proper format and missingness, Uber developers built their own Domain Specific Language (DSL) as a subset of Scala.  
特徴選択、変換、および入力データが適切な形式と欠損をチェックされることを保証するために、Uberの開発者はScalaのサブセットとして独自のドメイン特化言語（DSL）を構築しました。  
With it, end-users can add their own user-defined functions.  
これにより、エンドユーザーは独自のユーザー定義関数を追加できます。  
The same DSL expressions are applied during training and prediction, for guaranteed reproducibility.  
同じDSL式がトレーニングと予測の際に適用され、再現性が保証されます。  

Michelangelo supports offline, large-scale distributed training of a variety of machine learning algorithms and deep learning networks, which makes it very scalable.  
Michelangeloは、さまざまな機械学習アルゴリズムと深層学習ネットワークのオフラインでの大規模分散トレーニングをサポートしており、非常にスケーラブルです。  
The model type, hyper-parameters, data sources, DSL expressions and compute resource requirements are mentioned as a model configuration.  
モデルの種類、ハイパーパラメータ、データソース、DSL式、および計算リソースの要件は、モデル構成として言及されます。  
It also provides hyper-parameter search.  
また、ハイパーパラメータの検索も提供します。  

The configured training job runs on a YARN or Mesos cluster, after which performance metrics are calculated and compiled into a report.  
構成されたトレーニングジョブはYARNまたはMesosクラスターで実行され、その後、パフォーマンスメトリクスが計算され、レポートにまとめられます。  
When running partitioned models, training data is automatically partitioned based on model configuration, and trained on the same.  
パーティションモデルを実行する際、トレーニングデータはモデル構成に基づいて自動的にパーティション分けされ、同じものに対してトレーニングされます。  
The parent model is used when needed.  
必要に応じて親モデルが使用されます。  
Information regarding the final model is stored in the model repository for deployment, and the report is saved for future analysis.  
最終モデルに関する情報はデプロイメントのためにモデルリポジトリに保存され、レポートは将来の分析のために保存されます。  

Training jobs can be managed via the Michelangelo UI, API, or even through a Jupyter Notebook.  
トレーニングジョブは、MichelangeloのUI、API、またはJupyter Notebookを通じて管理できます。  
When training is complete, a versioned object containing the following information is stored in CassandraDB:  
トレーニングが完了すると、以下の情報を含むバージョン管理されたオブジェクトがCassandraDBに保存されます：  

1. Author of the model,  
1. モデルの著者、  
2. Start and end time of training job,  
2. トレーニングジョブの開始時刻と終了時刻、  
3. Model configuration,  
3. モデル構成、  
4. Reference to training and testing data,  
4. トレーニングデータとテストデータへの参照、  
5. Feature level statistics,  
5. 特徴レベルの統計、  
6. Model performance metrics,  
6. モデルのパフォーマンスメトリクス、  
7. Learned parameters of the model,  
7. モデルの学習パラメータ、  
8. Summary statistics.  
8. 要約統計。  

<!-- ここまで読んだ! -->

### Google’s Feast: an open-source feature store

Feast is an open-source feature store for machine learning for making the process of creating, managing, sharing, and serving features easier. 
Feastは、機械学習のためのオープンソースのフィーチャーストアであり、フィーチャーの作成、管理、共有、提供のプロセスを容易にします。
In 2019, Gojek introduced it in collaboration with Google Cloud. 
2019年に、GojekはGoogle Cloudとのコラボレーションでこれを導入しました。

It uses BigQuery + GCS + S3 for offline features, and BigTable + Redis with Apache Beam for online features. 
オフラインフィーチャーにはBigQuery + GCS + S3を、オンラインフィーチャーにはBigTable + RedisとApache Beamを使用します。

Components: 
コンポーネント：

1. Feast Core: This is where all the features and their respective definitions coexist. 
   1. Feast Core: ここではすべてのフィーチャーとそれぞれの定義が共存します。

2. Feast Job Service: This component manages data processing jobs that load the data from sources into stores, and jobs that export data used for training. 
   2. Feast Job Service: このコンポーネントは、ソースからストアにデータをロードするデータ処理ジョブと、トレーニングに使用されるデータをエクスポートするジョブを管理します。

3. Feast Online Serving: Online features require low-latency access to them which is facilitated by this component. 
   3. Feast Online Serving: オンラインフィーチャーは低遅延でのアクセスを必要とし、このコンポーネントによってそれが実現されます。

4. Feast Python SDK: This is used to manage feature definitions, launch jobs, retrieve training datasets and online features. 
   4. Feast Python SDK: これはフィーチャー定義の管理、ジョブの起動、トレーニングデータセットやオンラインフィーチャーの取得に使用されます。

5. Online Store: It stores the latest features for each entity. It can be populated by either batch ingestion or streaming ingestion jobs for a streaming source. 
   5. Online Store: 各エンティティの最新のフィーチャーを保存します(**そっか、オンラインストアには最新verだけあれば十分なんだ**...!:thinking:)。ストリーミングソースのためにバッチインジェストまたはストリーミングインジェストジョブによってデータを格納できます。

6. Offline Store: Stores batch data used to train AI models. 
   1. Offline Store: AIモデルのトレーニングに使用されるバッチデータを保存します。

How does it work? 
どのように機能するのか？

1. The log-streaming data is ingested from applications. 
   1. ログストリーミングデータはアプリケーションから取り込まれます。

2. Stream processing systems like Kafka and Spark are used to convert this data into stream features. 
   2. KafkaやSparkのようなストリーム処理システムを使用して、このデータをストリームフィーチャーに変換します。

3. Both the raw and stream features are then logged into the data lake. 
   3. 生データとストリームフィーチャーの両方がデータレイクに記録されます。

4. ETL/ELT transform data in the batch store. 
   4. ETL/ELTはバッチストア内のデータを変換します。

5. Features and their definitions are then established on the Feature Core. 
   5. フィーチャーとその定義は、Feature Coreに設定されます。

6. The Feast Job service polls for new and updated features. 
   6. Feast Jobサービスは新しいフィーチャーと更新されたフィーチャーをポーリングします。

7. Batch ingestion jobs are short-lived, they fetch data into offline and online stores. 
   7. **バッチインジェストジョブは短命で、オフラインおよびオンラインストアにデータを取得します**。

8. Stream ingestion jobs are long-lived, they fetch from streaming sources and provide to online applications. 
   8. **ストリームインジェストジョブは長命で、ストリーミングソースから取得し、オンラインアプリケーションに提供**します。

9. A machine learning pipeline is launched, data is used, all controlled by the SDK. 
   9. 機械学習パイプラインが起動され、データが使用され、すべてSDKによって制御されます。

10. According to model configurations, feast provides point-in-time training data and features. 
    10. モデルの設定に応じて、Feastは**point-in-timeなトレーニングデータとフィーチャーを提供**します。
    (**直近1週間を正解ラベル & それ以前の履歴を特徴量とするように、シンプルにtime-seriesでデータを分けて特徴量&ラベルを作るなら、feature storeでpoint-in-time機能を使う必要はないのかな...! wantedlyさんの事例を踏まえると。少なくともfeature store的なコンポーネントは別の理由で必要かもだが、point-in-time機能は持ってる必要はないかも。**)

11. The trained model is then served and the backend requests for prediction from the model serving system. 
    11. トレーニングされたモデルが提供され、バックエンドがモデルサービングシステムから予測を要求します。

12. Model Serving System requests online features from Feast Online Serving. 
    12. モデルサービングシステムはFeast Online Servingからオンラインフィーチャーを要求します。

13. Model Serving System makes predictions on online features and returns results. 
    13. モデルサービングシステムはオンラインフィーチャーに基づいて予測を行い、結果を返します。

<!-- ここまで読んだ!-->

### Hopswork’s Feature Store Hopsworksのフィーチャーストア

Data Engineers are primarily responsible for adding/updating features, which could be computed with SQL queries or even complex graph embeddings, using notebooks, programs written in Python, Java or Scala, and even Hopsworks’ UI. 
データエンジニアは、主にフィーチャーの追加/更新を担当しており、これはSQLクエリや複雑なグラフ埋め込みを使用して計算される可能性があり、ノートブック、Python、Java、Scalaで書かれたプログラム、さらにはHopsworksのUIを使用します。
Programs ingest data in the form of Pandas or Spark dataframes. 
プログラムは、PandasまたはSparkデータフレームの形式でデータを取り込みます。

Feature data is validated before ingestion using the Data Validation API. 
フィーチャーデータは、データ検証APIを使用して取り込み前に検証されます。
A UI platform is provided by Hopsworks for establishing data validation rules through which feature statistics can also be viewed. 
Hopsworksは、フィーチャー統計を表示できるデータ検証ルールを確立するためのUIプラットフォームを提供しています。
Hopsworks also supports the creation of more than one feature store, because one feature store should not necessarily be accessible to all parts of an enterprise. 
Hopsworksは、1つのフィーチャーストアが企業のすべての部門にアクセス可能である必要はないため、**複数のフィーチャーストアの作成もサポート**しています。
(これってfeature storeの一元管理的な役割と少し矛盾してる感...??:thinking:)

Data scientists use Feature Stores to split data into training and testing sets for building machine learning models. 
データサイエンティストは、フィーチャーストアを使用してデータをトレーニングセットとテストセットに分割し、機械学習モデルを構築します。
Online applications use it to create a feature vector which is later used for inference. 
オンラインアプリケーションは、後で推論に使用されるフィーチャーベクターを作成するためにそれを使用します。
In addition to this, users can also query for point-in-time data. 
これに加えて、ユーザーはpoint-in-timeデータをクエリすることもできます。

Features are measurable properties, wherein each feature belongs to a Feature Group with an associated key for computation. 
フィーチャーは測定可能な特性であり、各フィーチャーは計算のための関連キーを持つフィーチャーグループに属します。
Data Scientists can generate training and testing data by providing/selecting a set of features, the target file format for the output of features (CSV, TFRecords, Numpy, etc.), and the target storage system (GCS, AWS S3, etc.). 
データサイエンティストは、フィーチャーのセット、フィーチャーの出力のターゲットファイル形式（CSV、TFRecords、Numpyなど）、およびターゲットストレージシステム（GCS、AWS S3など）を提供/選択することによって、トレーニングデータとテストデータを生成できます。

There are two ways to calculate feature groups: 
フィーチャーグループを計算する方法は2つあります。

- On-demand: There is built-in support for external DBs that lets you define features on external data sources. 
- オンデマンド：外部データソースでフィーチャーを定義できる外部DBのための組み込みサポートがあります。
- Cached: The Hopsworks Feature Store can scale up to peta-bytes of feature data. 
- キャッシュ：Hopsworksフィーチャーストアは、ペタバイトのフィーチャーデータまでスケールアップできます。

Hopsworks provides great documentation on how to use their API and get started with its feature store. 
Hopsworksは、APIの使用方法やフィーチャーストアの使い始め方に関する優れたドキュメントを提供しています。

<!-- ここまで読んだ -->

### Tectonのフィーチャーストア

While most organisations have taken up the initiative to build feature stores for internal use, 
ほとんどの組織が内部使用のためにフィーチャーストアを構築する取り組みを始めている中、 
Tecton has been building their platform to be provided as a service to various enterprises. 
Tectonは、さまざまな企業にサービスとして提供されるプラットフォームを構築しています。 
Their founding members originally were at Uber, where they had built Michelangelo. 
彼らの創設メンバーは元々Uberにおり、そこでMichelangeloを構築していました。 
Taking inspiration from Uber’s product, Tecton built and started offering its services as well. 
Uberの製品からインスピレーションを受けて、Tectonは自社のサービスを構築し、提供を開始しました。 
They also contribute to Google’s open-source feature store, Feast. 
彼らはまた、GoogleのオープンソースフィーチャーストアであるFeastにも貢献しています。


## Summary 概要

- Feature Stores quicken and stabilise the process of extracting, transforming data, engineering features, and storing them for easy access for both offline and online needs.
- Feature Storesは、データの抽出、変換、特徴量エンジニアリング、そしてオフラインおよびオンラインのニーズに対して簡単にアクセスできるように保存するプロセスを迅速化し、安定させます。
- Feature stores if not already ubiquitous should be the next must-have step for every organisation that aims to build the best AI products without having to lose their bandwidth on operational purposes.
- Feature Storesは、すでに普及していない場合、運用目的に帯域幅を失うことなく最高のAI製品を構築しようとするすべての組織にとって、次に必要なステップであるべきです。
- Traditional CI/CD pipelines are not suitable for handling data and machine learning models, which introduces the requirement of MLOps and DataOps.
- 従来のCI/CDパイプラインは、データや機械学習モデルを扱うのに適しておらず、これがMLOpsおよびDataOpsの必要性を生じさせます。
- Some of the examples of feature stores are Uber’s Michelangelo, Google’s Feast, Hopsworks’ Feature Store and Tecton’s Feature Store.
- Feature Storesの例としては、UberのMichelangelo、GoogleのFeast、HopsworksのFeature Store、TectonのFeature Storeがあります。

### References 参考文献

- https://docs.hopsworks.ai/
- https://www.logicalclocks.com/blog/mlops-with-a-feature-store
- www.tecton.ai
- splicemachine.com

<!-- ここまで読んだ -->
