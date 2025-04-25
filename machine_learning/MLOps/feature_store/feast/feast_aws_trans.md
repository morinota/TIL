# Getting started with Feast, an open source feature store running on AWS Managed Services
# Feastの始め方：AWSマネージドサービス上で動作するオープンソースのフィーチャーストア


This post was written by Willem Pienaar, Principal Engineer at Tecton and creator of Feast.
この記事は、Tectonのプリンシパルエンジニアであり、**Feastの創作者であるWillem Pienaarによって書かれました**。

Feast is an open source feature store and a fast, convenient way to serve machine learning (ML) features for training and online inference.
Feastはオープンソースのフィーチャーストアであり、機械学習（ML）機能をトレーニングおよびオンライン推論のために提供するための迅速で便利な方法です。
Feast lets you build point-in-time correct training datasets from feature data, allows you to deploy a production-grade feature serving stack to Amazon Web Services (AWS) in seconds, and simplifies tracking features models are using.
Feastを使用すると、フィーチャーデータから時点正確なトレーニングデータセットを構築でき、数秒でAmazon Web Services（AWS）に本番環境向けのフィーチャーサービングスタックをデプロイでき、モデルが使用しているフィーチャーの追跡が簡素化されます。

## Why Feast? なぜFeastなのか？

Most ML teams today are well versed in shipping machine learning models into production, but deploying models into production is only a small part of the MLOps lifecycle. 
今日のほとんどのMLチームは、機械学習モデルを本番環境にデプロイすることに精通していますが、モデルを本番環境にデプロイすることはMLOpsライフサイクルのほんの一部に過ぎません。 
Most teams don’t have a declarative way to ship data into production for consumption by machine learning models. 
ほとんどのチームは、機械学習モデルが消費するためにデータを本番環境に送信するための宣言的な方法を持っていません。 
That’s where Feast helps. 
そこでFeastが役立ちます。

- **Tracking and sharing features**: Feast allows teams to define and track feature metadata (such as data sources, entities, and features) through declarative definitions that are version controlled in Git. 
- 特徴の追跡と共有：Feastは、チームがGitでバージョン管理された宣言的定義を通じて、特徴メタデータ（データソース、エンティティ、特徴など）を定義し、追跡することを可能にします。 
This allows teams to maintain a versioned history of operationalized features, helping teams understand how features are performing in production, and enabling reuse and sharing of features across teams. 
これにより、チームは運用化された特徴のバージョン履歴を維持でき、特徴が本番環境でどのように機能しているかを理解し、チーム間での特徴の再利用と共有を可能にします。

- **Managed serving infrastructure**: Feast takes all the work out of setting up data infrastructure. 
- 管理された提供インフラストラクチャ：Feastはデータインフラストラクチャの設定に関するすべての作業を取り除きます。 
Feast makes configuring your data infrastructure for serving features possible, makes populating these stores with feature values easy, and provides an SDK for reading feature values from these stores at low latency. 
Feastは、特徴を提供するためのデータインフラストラクチャの設定を可能にし、これらのストアに特徴値を簡単に格納できるようにし、低遅延でこれらのストアから特徴値を読み取るためのSDKを提供します。

- **A consistent view of data**: Machine learning models need to see a consistent view of features in training as they will see in production. 
- 一貫したデータのビュー：機械学習モデルは、トレーニング中に本番環境で見るのと同じ一貫した特徴のビューを見る必要があります。 
Feast ensures this consistency through time-travel-based training dataset generation, and through a unified serving interface that helps your online models see a consistent view of features during inference and training. 
Feastは、タイムトラベルに基づくトレーニングデータセット生成と、推論とトレーニング中にオンラインモデルが特徴の一貫したビューを見るのを助ける**統一されたサービングインターフェース**を通じて、この一貫性を確保します。

## Feast on AWS

With the latest release of Feast, you can take advantage of AWS storage services to run an open source feature store:
最新のFeastのリリースにより、AWSストレージサービスを利用してオープンソースのフィーチャーストアを運用することができます：

1. Amazon Redshift and Amazon Simple Storage Service (Amazon S3) can be used as an offline store, which supports feature serving for training and batch inference of large amounts of feature data.
1. Amazon Redshiftと**Amazon Simple Storage Service (Amazon S3)は、オフラインストアとして使用**でき、大量のフィーチャーデータのトレーニングおよびバッチ推論のためのフィーチャーサービングをサポートします。

2. Amazon DynamoDB, a NoSQL key-value database, can be used as an online store. 
2. NoSQLキー・バリューデータベースであるAmazon DynamoDBは、オンラインストアとして使用できます。
Amazon DynamoDB supports feature serving at low latency for real-time prediction.
Amazon DynamoDBは、リアルタイム予測のための低遅延でのフィーチャーサービングをサポートしています。

<!-- ここまで読んだ-->

## Use case: Real-time credit scoring 使用例: リアルタイムクレジットスコアリング

When individuals apply for loans from banks and other credit providers, the decision to approve a loan application is made through a statistics model. 
個人が銀行やその他のクレジット提供者からローンを申請する際、ローン申請を承認するかどうかの決定は統計モデルを通じて行われます。
Often, this model uses information about a customer to determine the likelihood that they will repay or default on a loan. 
このモデルは、顧客に関する情報を使用して、彼らがローンを返済する可能性やデフォルトする可能性を判断します。
This process is called credit scoring. 
このプロセスは**クレジットスコアリング**と呼ばれます。

For this use case, we will demonstrate how a real-time credit scoring system can be built using Feast and scikit-Learn. 
この使用例では、Feastとscikit-Learnを使用してリアルタイムクレジットスコアリングシステムを構築する方法を示します。

This real-time system is required to accept a loan request from a customer and respond within 100 ms with a decision on whether their loan has been approved or rejected. 
このリアルタイムシステムは、**顧客からのローンリクエストを受け入れ、100ミリ秒以内にそのローンが承認されたか拒否されたかの決定を返す**必要があります。

A fully working demo repository for this use case is available on GitHub. 
この使用例のための完全に動作するデモリポジトリはGitHubで入手可能です。

<!-- ここまで読んだ! -->

## Data model データモデル

We have three datasets at our disposal to build this credit scoring system.  
私たちは、このクレジットスコアリングシステムを構築するために、3つのデータセットを利用できます。

The first is a loan dataset.  
最初のデータセットは、ローンデータセットです。
This dataset has features based on historic loans for current customers.  
このデータセットは、現在の顧客に対する過去のローンに基づいた特徴を持っています。
Importantly, this dataset contains the target column, loan_status.  
重要なことに、このデータセットにはターゲット列であるloan_statusが含まれています。
This column denotes whether a customer has defaulted on a loan.  
この列は、顧客がローンのデフォルトをしたかどうかを示します。

The second dataset we will use is a zip code dataset.  
私たちが使用する2番目のデータセットは、郵便番号データセットです。
This dataset is used to enrich the loan dataset with supplementary features about a specific geographic location.  
このデータセットは、特定の地理的場所に関する補足的な特徴でローンデータセットを豊かにするために使用されます。

The third and final dataset is a credit history dataset.  
3番目で最後のデータセットは、クレジット履歴データセットです。
This is a dataset that contains the credit history on a per-person basis and is updated on a frequent basis by the credit institution.  
これは、個人ごとのクレジット履歴を含むデータセットで、クレジット機関によって頻繁に更新されます。
Every time a credit check is done on an individual, this dataset will be updated.  
個人に対してクレジットチェックが行われるたびに、このデータセットは更新されます。

The preceding loan, zip code, and credit history features will be combined into a single training dataset when building a credit-scoring model.  
前述のローン、郵便番号、クレジット履歴の特徴は、クレジットスコアリングモデルを構築する際に、**単一のトレーニングデータセットに統合**されます。
However, historic loan data is not useful for making predictions based on new customers.  
しかし、過去のローンデータは新しい顧客に基づいて予測を行うためには役に立ちません。
Therefore, we will register and serve only the zip code and credit history features with Feast, and we will assume that the incoming request contains the loan application features.  
したがって、私たちはFeastを使用して郵便番号とクレジット履歴の特徴のみを登録し提供し、受信リクエストにはローン申請の特徴が含まれていると仮定します。

An example of the loan application payload is as follows:  
ローン申請ペイロードの例は以下の通りです：

```python
loan_request = {
   "zipcode": [76104],
   "dob_ssn": [19530219_5179],
   "person_age": [133],
   "person_income": [59000],
   "person_home_ownership": ["RENT"],
   "person_emp_length": [123.0],
   "loan_intent": ["PERSONAL"],
   "loan_amnt": [35000],
   "loan_int_rate": [16.02],
}
```

## Amazon S3とRedshiftをデータソースおよびオフラインストアとして

A Redshift data source allows you to fetch historical feature values from Redshift for building training datasets and materializing features into an online store. 
Redshiftデータソースを使用すると、トレーニングデータセットを構築し、特徴をオンラインストアに具現化するために、Redshiftから過去の特徴値を取得できます。

Install Feast using pip: 
Feastをpipを使用してインストールします：

```bash
pip install feast
```

Initialize a blank feature repository: 
空の特徴リポジトリを初期化します：

```bash
feast init -m credit_scoring
```

This command will create a feature repository for your project. 
このコマンドは、プロジェクトのための特徴リポジトリを作成します。 
Let’s edit our feature store configuration using the provided feature_store.yaml: 
提供されたfeature_store.yamlを使用して、特徴ストアの設定を編集しましょう：

```yml
project: credit_scoring_aws
registry: registry.db # where we will store our feature metadata
provider: aws # the environment we are deploying to

online_store:
  type: dynamodb # the online feature store
  region: us-west-2

offline_store:
  type: redshift # the offline feature store
  cluster_id:
  region: us-west-2
  user: admin
  database: dev
  s3_staging_location:
  iam_role:
```

A data source is defined as part of the Feast Declarative API in the feature repo directory’s Python files. 
データソースは、フィーチャーリポジトリディレクトリのPythonファイル内のFeast宣言型APIの一部として定義されます。 
Now that we’ve configured our infrastructure, let’s register the zip code and credit history features we will use during training and serving. 
インフラストラクチャを構成したので、トレーニングと提供に使用する郵便番号と信用履歴のフィーチャーを登録しましょう。

Create a file called `features.py` within the credit_scoring/ directory. 
credit_scoring/ディレクトリ内にfeatures.pyというファイルを作成します。 
Then add the following feature definition to features.py: 
次に、features.pyに以下のフィーチャー定義を追加します：

```python
from datetime import timedelta
from feast import Entity, Feature, FeatureView, RedshiftSource, ValueType

zipcode = Entity(name="zipcode", value_type=ValueType.INT64)
zipcode_features = FeatureView(
    name="zipcode_features",
    entities=["zipcode"],
    ttl=timedelta(days=3650),
    features=[
        Feature(name="city", dtype=ValueType.STRING),
        Feature(name="state", dtype=ValueType.STRING),
        Feature(name="location_type", dtype=ValueType.STRING),
        Feature(name="tax_returns_filed", dtype=ValueType.INT64),
        Feature(name="population", dtype=ValueType.INT64),
        Feature(name="total_wages", dtype=ValueType.INT64),
    ],
    batch_source=RedshiftSource(
        query="SELECT * FROM spectrum.zipcode_features",
        event_timestamp_column="event_timestamp",
        created_timestamp_column="created_timestamp",
    ),
)

dob_ssn = Entity(name="dob_ssn", value_type=ValueType.STRING)
credit_history_source = RedshiftSource(
    query="SELECT * FROM spectrum.credit_history",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp",
)

credit_history = FeatureView(
    name="credit_history",
    entities=["dob_ssn"],
    ttl=timedelta(days=90),
    features=[
        Feature(name="credit_card_due", dtype=ValueType.INT64),
        Feature(name="mortgage_due", dtype=ValueType.INT64),
        Feature(name="student_loan_due", dtype=ValueType.INT64),
        Feature(name="vehicle_loan_due", dtype=ValueType.INT64),
        Feature(name="hard_pulls", dtype=ValueType.INT64),
        Feature(name="missed_payments_2y", dtype=ValueType.INT64),
        Feature(name="missed_payments_1y", dtype=ValueType.INT64),
        Feature(name="missed_payments_6m", dtype=ValueType.INT64),
        Feature(name="bankruptcies", dtype=ValueType.INT64),
    ],
    batch_source=credit_history_source,
)
```

Feature views allow users to register data sources in their organizations into Feast, and then use those data sources for both training and online inference. 
**フィーチャービューは、ユーザーが自組織のデータソースをFeastに登録し、それらのデータソースをトレーニングとオンライン推論の両方に使用できるようにします**。 
The preceding feature view definition tells Feast where to find zip code and credit history features. 
前述のフィーチャービュー定義は、Feastに郵便番号と信用履歴のフィーチャーの場所を示します。

Now that we have defined our first feature view, we can apply the changes to create our feature registry and configure our infrastructure: 
最初のフィーチャービューを定義したので、変更を適用してフィーチャーレジストリを作成し、インフラストラクチャを構成できます：

The preceding apply command will: 
前述のapplyコマンドは以下を行います：
- Store all entity and feature view definitions in a local file called registry.db. 
すべてのエンティティとフィーチャービューの定義を`registry.db`というローカルファイルに保存します。 
- Create an empty DynamoDB table for serving zip code and credit history features. 
郵便番号と信用履歴のフィーチャーを提供するための空のDynamoDBテーブルを作成します。 
- Ensure that your data sources on Redshift are available. 
Redshift上のデータソースが利用可能であることを確認します。

<!-- ここまで読んだ! -->

## Building a training dataset トレーニングデータセットの構築

Our loan dataset contains our target variable, so we will load that first:
私たちのローンデータセットにはターゲット変数が含まれているので、まずそれをロードします：

```
loans_df=pd.read_parquet("loan_table.parquet")
```

Then we identify the features we want to query from Feast:
次に、Feastからクエリしたい特徴を特定します：

```python
feast_features = [
   "zipcode_features:city",
   "zipcode_features:state",
   "zipcode_features:location_type",
   "zipcode_features:tax_returns_filed",
   "zipcode_features:population",
   "zipcode_features:total_wages",
   "credit_history:credit_card_due",
   "credit_history:mortgage_due",
   "credit_history:student_loan_due",
   "credit_history:vehicle_loan_due",
   "credit_history:hard_pulls",
   "credit_history:missed_payments_2y",
   "credit_history:missed_payments_1y",
   "credit_history:missed_payments_6m",
   "credit_history:bankruptcies",
]
```

Then we make a query from Feast to enrich our loan dataset. 
次に、Feastからクエリを行い、ローンデータセットを豊かにします。
Feast will automatically detect the zip code and dob_ssn join columns and join the feature data in a point-in-time correct way. 
Feastは自動的に郵便番号とdob_ssnの結合列を検出し、時点に正しい方法で特徴データを結合します。
It does this by only joining features that were available at the time the loan was active.
これは、ローンがアクティブだった時点で利用可能だった特徴のみを結合することによって行われます。

```
training_df=fs.get_historical_features(entity_df=loans,features=feast_features).to_df()
```

Once we have retrieved the complete training dataset, we can:
完全なトレーニングデータセットを取得したら、次のことができます：
- Droptimestamp columns and the loan_id column.
  - タイムスタンプ列とloan_id列を削除します。
- Encode categorical features.
  - カテゴリカル特徴をエンコードします。
- Split the training dataframe into a train, validation, and test set.
  - トレーニングデータフレームをトレーニング、検証、テストセットに分割します。

Finally, we can train our classifier:
最後に、分類器をトレーニングできます：

```python
from sklearn import tree

clf=tree.DecisionTreeClassifier() clf.fit(train_X[sorted(train_X)], train_Y)
```

The full model training code is on GitHub.
完全なモデルのトレーニングコードはGitHubにあります。

<!-- ここまで読んだ! -->

### DynamoDB as an online store DynamoDBをオンラインストアとして

Before we can make online loan predictions with our credit scoring model, we must populate our online store with feature values. 
クレジットスコアリングモデルを使用してオンラインローン予測を行う前に、オンラインストアに特徴値を格納する必要があります。

To load features into the online store, we use materialize incremental:
オンラインストアに特徴をロードするために、`materialize incremental`を使用します：

```shell 
CURRENT_TIME=$(date-u+"%Y-%m-%dT%H:%M:%S")
feast materialize-incremental$CURRENT_TIME
```

This command will load features from our zip code and credit history data sources up to the $CURRENT_TIME. The materialize command can be repeatedly called as more data becomes available in order to keep the online store fresh.
このコマンドは、私たちの郵便番号とクレジット履歴のデータソースから$CURRENT_TIMEまでの特徴をロードします。 
materializeコマンドは、より多くのデータが利用可能になるにつれて繰り返し呼び出すことができ、オンラインストアを新鮮に保つことができます。
(オンラインストアの更新は、materialized view的な意味なのか...!:thinking:)

<!-- ここまで読んだ! -->

## Fetching a feature vector at low latency 低遅延での特徴ベクトルの取得

Now we have everything we need to make a loan prediction.  
これで、ローン予測を行うために必要なすべてのものが揃いました。

```python
# The incoming loan request is shown in the following object
loan_request = {
   "zipcode": [76104],
   "dob_ssn": ["19632106_4278"],
   "person_age": [133],
   "person_income": [59000],
   "person_home_ownership": ["RENT"],
   "person_emp_length": [123.0],
   "loan_intent": ["PERSONAL"],
   "loan_amnt": [35000],
   "loan_int_rate": [16.02],
}

# Next we fetch our online features from DynamoDB using Feast
# 次に、feastを使ってオンライン特徴量を取得する
customer_zipcode = loan_request['zipcode'][0]
dob_ssn = loan_request["dob_ssn"][0]

feature_vector = fs.get_online_features(
   entity_rows=[{"zipcode": zipcode, "dob_ssn": dob_ssn}],
   features=feast_features,
).to_dict()

# Then we join the Feast features to the loan request
# リクエストから受け取った特徴量と、Feastから取得した特徴量をjoinする
features = loan_request.copy()
features.update(feature_vector)
features_df = pd.DataFrame.from_dict(features)

# Finally we make a prediction
prediction = clf.predict(features_df)  # 1 = default, 0 = will repay
```

## Conclusion 結論

That’s it! We have a functional real-time credit scoring system.
それで終わりです！私たちは機能的なリアルタイムクレジットスコアリングシステムを持っています。

Check out the feastGitHub repository for the latest features, such as on-demand transformation, Feast server deployment to AWS Lambda, as well as support for streaming sources.
最新の機能（オンデマンド変換、AWS LambdaへのFeastサーバーのデプロイ、ストリーミングソースのサポートなど）については、feastのGitHubリポジトリをチェックしてください。

The complete end-to-end real-time credit scoring system is available on GitHub.
完全なエンドツーエンドのリアルタイムクレジットスコアリングシステムはGitHubで入手可能です。
Feel free to deploy it and try it out.
自由にデプロイして試してみてください。

If you want to participate in the Feast community, join us on Slack, or read the Feast documentation to get a better understanding of how to use Feast.
Feastコミュニティに参加したい場合は、Slackで私たちに参加するか、Feastのドキュメントを読んでFeastの使い方をよりよく理解してください。

<!-- ここまで読んだ! -->
