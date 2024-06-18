## refs 審判

- https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/ https://aws.amazon.com/jp/blogs/machine-learning/process-amazon-redshift-data-and-schedule-a-training-pipeline-with-amazon-sagemaker-processing-and-amazon-sagemaker-pipelines/

# Process Amazon Redshift data and schedule a training pipeline with Amazon SageMaker Processing and Amazon SageMaker Pipelines Amazon SageMaker Processing と Amazon SageMaker Pipelines を使って Amazon Redshift のデータを処理し、トレーニングパイプラインをスケジュールする。

Customers in many different domains tend to work with multiple sources for their data: object-based storage like Amazon Simple Storage Service (Amazon S3), relational databases like Amazon Relational Database Service (Amazon RDS), or data warehouses like Amazon Redshift.
**様々なドメインの顧客は、データを複数のソースで扱う傾向がある**： Amazon Simple Storage Service (Amazon S3)のようなオブジェクトベースのストレージ、Amazon Relational Database Service (Amazon RDS)のようなリレーショナル・データベース、Amazon Redshiftのようなデータウェアハウス。
(まさにそう!笑)
Machine learning (ML) practitioners are often driven to work with objects and files instead of databases and tables from the different frameworks they work with.
機械学習（ML）の実務者は、よく使うさまざまなフレームワークから、**データベースやテーブルではなくオブジェクトやファイルで作業することが多い**。(確かに...)
They also prefer local copies of such files in order to reduce the latency of accessing them.
また、**アクセスの待ち時間を減らすために**、そのようなファイルのローカルコピーを好むことが多い。(ローカルコピーってdump的な意味かな。なるほど、こういう利点があるのか...!:thinking_face:)

Nevertheless, ML engineers and data scientists might be required to directly extract data from data warehouses with SQL-like queries to obtain the datasets that they can use for training their models.
とはいえ、MLエンジニアやデータサイエンティストは、**SQLのようなクエリを使ってデータウェアハウスから直接データを抽出し、モデルの学習に使えるデータセットを取得する必要があるかもしれない**。

In this post, we use the Amazon SageMaker Processing API to run a query against an Amazon Redshift cluster, create CSV files, and perform distributed processing.
この記事では、Amazon SageMaker Processing APIを使用して、Amazon Redshiftクラスタに対してクエリを実行し、CSVファイルを作成し、分散処理を実行します。
As an extra step, we also train a simple model to predict the total sales for new events, and build a pipeline with Amazon SageMaker Pipelines to schedule it.
追加ステップとして、新規イベントの総売上高を予測する簡単なモデルをトレーニングし、Amazon SageMaker Pipelinesでパイプラインを構築してスケジューリングします。

<!-- ここまで読んだ! -->

## Prerequisites 前提条件

This post uses the sample data that is available when creating a Free Tier cluster in Amazon Redshift.
この記事では、Amazon RedshiftでFree Tierクラスタを作成する際に利用可能なサンプルデータを使用します。
As a prerequisite, you should create your cluster and attach to it an AWS Identity and Access Management (IAM) role with the correct permissions.
前提条件として、クラスタを作成し、適切な権限を持つAWS Identity and Access Management (IAM) ロールをクラスタにアタッチする必要があります。
For instructions on creating the cluster with the sample dataset, see Using a sample dataset.
サンプルデータセットでクラスタを作成する手順については、サンプルデータセットの使用を参照してください。
For instructions on associating the role with the cluster, see Authorizing access to the Amazon Redshift Data API.
ロールをクラスタに関連付ける手順については、Amazon Redshift Data APIへのアクセスを許可するを参照してください。

(↑はRedshift側のリソースの準備なのであんまり気にしなくて良い気がしてる)

You can then use your IDE of choice to open the notebooks.
その後、お好みのIDEを使ってノートブックを開くことができる。
This content has been developed and tested using SageMaker Studio on a ml.t3.medium instance.
このコンテンツは、ml.t3.medium インスタンス上で SageMaker Studio を使用して開発およびテストされています。
For more information about using Studio, refer to the following resources:
Studioの使い方の詳細については、以下のリソースを参照してください：

- Onboard to Amazon SageMaker Domain Amazon SageMakerドメインへのオンボード
- Clone a Git Repository in SageMaker Studio SageMaker Studio で Git リポジトリをクローンする
- Change an Instance Type インスタンスタイプの変更

## Define the query クエリーの定義

Now that your Amazon Redshift cluster is up and running, and loaded with the sample dataset, we can define the query to extract data from our cluster.
Amazon Redshiftクラスタが稼働し、サンプルデータセットがロードされたので、クラスタからデータを抽出するクエリを定義します。
According to the documentation for the sample database, this application helps analysts track sales activity for the fictional TICKIT website, where users buy and sell tickets online for sporting events, shows, and concerts.
サンプルデータベースのドキュメントによると、このアプリケーションは、ユーザーがスポーツイベントやショー、コンサートのチケットをオンラインで売買する架空のウェブサイト「TICKIT」の販売活動をアナリストが追跡するのに役立ちます。
In particular, analysts can identify ticket movement over time, success rates for sellers, and the best-selling events, venues, and seasons.
特にアナリストは、長期的なチケットの動き、売り手の成功率、最も売れているイベント、会場、シーズンなどを特定することができる。

Analysts may be tasked to solve a very common ML problem: predict the number of tickets sold given the characteristics of an event.
**アナリストは、ごく一般的なMLの問題を解決するよう命じられるかもしれない： イベントの特性を考慮して売れるチケットの数を予測する**。(ありそう)
Because we have two fact tables and five dimensions in our sample database, we have some data that we can work with.
サンプル・データベースには 2 つのファクト・テーブルと 5 つのディメンジョンがあるため、作業可能なデータがあります。
(star schema的な概念。fact table = イベントログとか。dimension = イベントやユーザの属性情報とか？:thinking_face:)
For the sake of this example, we try to use information from the venue in which the event takes place as well as its date.
この例では、イベントが開催される会場とその日付の情報を使用するようにしています。
The SQL query looks like the following:
SQLクエリは以下のようになる: 

```sql
SELECT 
sum(s.qtysold) AS total_sold, e.venueid, e.catid, d.caldate, d.holiday
from sales s, event e, date d
WHERE s.eventid = e.eventid and e.dateid = d.dateid
GROUP BY e.venueid, e.catid, d.caldate, d.holiday
```

We can run this query in the query editor to test the outcomes and change it to include additional information if needed.
クエリーエディターでこのクエリーを実行して結果をテストし、必要であれば追加情報を含むように変更することができる。
(まずはクエリで想定通りのデータを取得できるか、マニュアルでチェックするよね。)

<!-- ここまで読んだ! -->

## Extract the data from Amazon Redshift and process it with SageMaker Processing Amazon Redshiftからデータを抽出し、SageMaker Processingで処理する。

Now that we’re happy with our query, we need to make it part of our training pipeline.
**さて、クエリーに満足したら、それをトレーニングパイプラインの一部にする必要がある**。

A typical training pipeline consists of three phases:
典型的なトレーニングパイプラインは、3つのフェーズで構成される：

- Preprocessing – This phase reads the raw dataset and transforms it into a format that matches the input required by the model for its training
前処理 - このフェーズでは、生のデータセットを読み取り、モデルのトレーニングに必要な入力と一致する形式に変換する。
- Training – This phase reads the processed dataset and uses it to train the model
トレーニング - このフェーズでは、処理されたデータセットを読み込み、モデルのトレーニングに使用します。
- Model registration – In this phase, we save the model for later usage
モデルの登録 - この段階では、後で使用するためにモデルを保存します。

Our first task is to use a SageMaker Processing job to load the dataset from Amazon Redshift, preprocess it, and store it to Amazon S3 for the training model to pick up.
最初のタスクは、**SageMaker Processingジョブを使用して、Amazon Redshiftからデータセットをロードし、前処理を行い、学習モデルが選択できるようにAmazon S3に保存すること**です。
SageMaker Processing allows us to directly read data from different resources, including Amazon S3, Amazon Athena, and Amazon Redshift.
**SageMaker Processingでは、Amazon S3、Amazon Athena、Amazon Redshiftなど、さまざまなリソースからデータを直接読み込むことができます。**(これってProcessing自体の機能? もしくは内部で動くData Wranglerの機能??:thinking_face:)
SageMaker Processing allows us to configure access to the cluster by providing the cluster and database information, and use our previously defined SQL query as part of a RedshiftDatasetDefinition.
SageMaker Processing では、クラスタとデータベース情報を提供することでクラスタへのアクセスを構成し、 `RedshiftDatasetDefinition` の一部として事前に定義した SQL クエリを使用することができます。(Data Wranglerの機能なのか??)
We use the SageMaker Python SDK to create this object, and you can check the definition and the parameters needed on the GitHub page.
このオブジェクトの作成には SageMaker Python SDK を使用しており、定義と必要なパラメータは GitHub ページで確認できます。
See the following code:
次のコードを参照：

```python
from sagemaker.dataset_definition.inputs import RedshiftDatasetDefinition

rdd = RedshiftDatasetDefinition(
    cluster_id="THE-NAME-OF-YOUR-CLUSTER",
    database="THE-NAME-OF-YOUR-DATABASE",
    db_user="YOUR-DB-USERNAME",
    query_string="THE-SQL-QUERY-FROM-THE-PREVIOUS-STEP",
    cluster_role_arn="THE-IAM-ROLE-ASSOCIATED-TO-YOUR-CLUSTER",
    output_format="CSV",
    output_s3_uri="WHERE-IN-S3-YOU-WANT-TO-STORE-YOUR-DATA"
)
```

Then, you can define the DatasetDefinition.
次に、DatasetDefinition を定義します。
This object is responsible for defining how SageMaker Processing uses the dataset loaded from Amazon Redshift:
このオブジェクトは、SageMaker Processing が Amazon Redshift から読み込んだデータセットをどのように使用するかを定義します:

```python
from sagemaker.dataset_definition.inputs import DatasetDefinition

dd = DatasetDefinition(
    data_distribution_type='ShardedByS3Key', # This tells SM Processing to shard the data across instances
    local_path='/opt/ml/processing/input/data/', # Where SM Processing will save the data in the container
    redshift_dataset_definition=rdd # Our ResdhiftDataset
)
```

Finally, you can use this object as input of your processor of choice.
**最後に、このオブジェクトをお好みのプロセッサーの入力として使うことができる**。
For this post, we wrote a very simple scikit-learn script that cleans the dataset, performs some transformations, and splits the dataset for training and testing.
この投稿のために、データセットのクリーンアップ、いくつかの変換の実行、トレーニングとテストのためのデータセットの分割を行う、非常にシンプルなscikit-learnスクリプトを書いた。
You can check the code in the file processing.py.
processing.pyでコードを確認できます。

We can now instantiate the SKLearnProcessor object, where we define the framework version that we plan on using, the amount and type of instances that we spin up as part of our processing cluster, and the execution role that contains the right permissions.
ここで、使用する予定のフレームワークのバージョン、処理クラスタの一部としてスピンアップするインスタンスの量とタイプ、適切なパーミッションを含む実行ロールを定義します。
Then, we can pass the parameter dataset_definition as the input of the run() method.
そして、パラメータ `dataset_definition` を `run()` メソッドの入力として渡すことができる。
(DataSetDefinitionは`ProcessingInput`クラスにwrapしてProcessingJobに渡すのか...!:thinking:)
This method accepts our processing.py script as the code to run, given some inputs (namely, our RedshiftDatasetDefinition), generates some outputs (a train and a test dataset), and stores both to Amazon S3.
このメソッドはprocessing.pyスクリプトを実行するコードとして受け取り、いくつかの入力(つまりRedshiftDatasetDefinition)を与え、いくつかの出力(trainとtestデータセット)を生成し、両方をAmazon S3に保存します。
We run this operation synchronously thanks to the parameter wait=True:
パラメータwait=Trueのおかげで、この操作は同期的に実行される：

```python
from sagemaker.sklearn import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker import get_execution_role

skp = SKLearnProcessor(
    framework_version='0.23-1',
    role=get_execution_role(),
    instance_type='ml.m5.large',
    instance_count=1
)
skp.run(
    code='processing/processing.py',
    inputs=[ProcessingInput(
        dataset_definition=dd, # ここでDatasetDefinitionをProcessingInputにwrapしてる(データの入れ物??)
        destination='/opt/ml/processing/input/data/',
        s3_data_distribution_type='ShardedByS3Key'
    )],
    outputs = [
        ProcessingOutput(
            output_name="train",
            source="/opt/ml/processing/train"
        ),
        ProcessingOutput(
            output_name="test",
            source="/opt/ml/processing/test"
        ),
    ],
    wait=True
)
```

With the outputs created by the processing job, we can move to the training step, by means of the sagemaker.sklearn.SKLearn() Estimator:
処理ジョブによって作成された出力により、sagemaker.sklearn.SKLearn() Estimatorを使用した学習ステップに移ることができます：

```python
from sagemaker.sklearn import SKLearn

s = SKLearn(
    entry_point='training/script.py',
    framework_version='0.23-1',
    instance_type='ml.m5.large',
    instance_count=1,
    role=get_execution_role()
)
s.fit({
    'train':skp.latest_job.outputs[0].destination,
    'test':skp.latest_job.outputs[1].destination
})
```

To learn more about the SageMaker Training API and Scikit-learn Estimator, see Using Scikit-learn with the SageMaker Python SDK.
SageMaker Training APIとScikit-learn Estimatorの詳細については、SageMaker Python SDKでScikit-learnを使用するを参照してください。

## Define a training pipeline トレーニングパイプラインを定義する

Now that we have proven that we can read data from Amazon Redshift, preprocess it, and use it to train a model, we can define a pipeline that reproduces these steps, and schedule it to run.
Amazon Redshiftからデータを読み込み、前処理を行い、モデルのトレーニングに使用できることが証明されたので、これらのステップを再現するパイプラインを定義し、実行するようにスケジューリングすることができます。
To do so, we use SageMaker Pipelines.
そのために SageMaker Pipelines を使用します。
Pipelines is the first purpose-built, easy-to-use continuous integration and continuous delivery (CI/CD) service for ML.
Pipelinesは、ML向けに初めて専用に構築された、使いやすい継続的インテグレーションと継続的デリバリー（CI/CD）サービスです。
With Pipelines, you can create, automate, and manage end-to-end ML workflows at scale.
Pipelinesを使えば、エンドツーエンドのMLワークフローを大規模に作成、自動化、管理できます。

Pipelines are composed of steps.
パイプラインはステップで構成される。
These steps define the actions that the pipeline takes, and the relationships between steps using properties.
これらのステップは、パイプラインが取るアクションと、プロパティを使ったステップ間の関係を定義する。
We already know that our pipelines are composed of three steps:
パイプラインが3つのステップで構成されていることはすでに知っている：

- A processing phase, defined in ProcessingStep
ProcessingStep で定義される処理フェーズ。
- A training phase, defined in TrainingStep
TrainingStepで定義されたトレーニングフェーズ
- A registration phase, defined in CreateModelStep
CreateModelStep で定義される登録フェーズ。

Furthermore, to make the pipeline definition dynamic, Pipelines allows us to define parameters, which are values that we can provide at runtime when the pipeline starts.
さらに、パイプラインの定義をダイナミックにするために、パイプラインではパラメータを定義することができる。パラメータは、パイプラインが開始するときに実行時に指定できる値である。

The following code is a snippet that shows the definition of a processing step.
次のコードは、処理ステップの定義を示すスニペットである。
The step requires the definition of a processor, which is very similar to the one defined previously during the preprocessing discovery phase, but this time using the parameters of Pipelines.
このステップではプロセッサーを定義する必要がある。このプロセッサーは、前回の前処理発見フェーズで定義したものと非常によく似ているが、今回はパイプラインのパラメーターを使用する。
The others parameters, code, inputs, and outputs are the same as we have defined previously:
その他のパラメータ、コード、入力、出力は、前回定義したものと同じである：

```python
#### PROCESSING STEP #####

# PARAMETERS
processing_instance_type = ParameterString(name='ProcessingInstanceType', default_value='ml.m5.large')
processing_instance_count = ParameterInteger(name='ProcessingInstanceCount', default_value=2)

# PROCESSOR
skp = SKLearnProcessor(
    framework_version='0.23-1',
    role=get_execution_role(),
    instance_type=processing_instance_type,
    instance_count=processing_instance_count
)

# DEFINE THE STEP
processing_step = ProcessingStep(
    name='ProcessingStep',
    processor=skp,
    code='processing/processing.py',
    inputs=[ProcessingInput(
        dataset_definition=dd,
        destination='/opt/ml/processing/input/data/',
        s3_data_distribution_type='ShardedByS3Key'
    )],
    outputs = [
        ProcessingOutput(output_name="train", source="/opt/ml/processing/output/train"),
        ProcessingOutput(output_name="test", source="/opt/ml/processing/output/test"),
    ]
)
```

Very similarly, we can define the training step, but we use the outputs from the processing step as inputs:
これと同様に、学習ステップを定義することができるが、処理ステップからの出力を入力として使用する：

```python
# TRAININGSTEP
training_step = TrainingStep(
    name='TrainingStep',
    estimator=s,
    inputs={
        "train": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri),
        "test": TrainingInput(s3_data=processing_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri)
    }
)
```

Finally, let’s add the model step, which registers the model to SageMaker for later use (for real-time endpoints and batch transform):
最後に、モデルステップを追加します。このステップでは、後で使用するためにモデルを SageMaker に登録します（リアルタイムエンドポイントとバッチ変換用）：

```python
# MODELSTEP
model_step = CreateModelStep(
    name="Model",
    model=model,
    inputs=CreateModelInput(instance_type='ml.m5.xlarge')
)
```

With all the pipeline steps now defined, we can define the pipeline itself as a pipeline object comprising a series of those steps.
すべてのパイプラインステップが定義されたので、一連のステップからなるパイプラインオブジェクトとして、パイプライン自体を定義することができる。
ParallelStep and Condition steps also are possible.
パラレルステップやコンディションステップも可能。
Then we can update and insert (upsert) the definition to Pipelines with the .upsert() command:
そして、.upsert()コマンドを使って、定義を更新し、Pipelinesに挿入（upsert）することができる：

```python
#### PIPELINE ####
pipeline = Pipeline(
    name = 'Redshift2Pipeline',
    parameters = [
        processing_instance_type, processing_instance_count,
        training_instance_type, training_instance_count,
        inference_instance_type
    ],
    steps = [
        processing_step, 
        training_step,
        model_step
    ]
)
pipeline.upsert(role_arn=role)
```

After we upsert the definition, we can start the pipeline with the pipeline object’s start() method, and wait for the end of its run:
定義をアップサートしたら、パイプライン・オブジェクトのstart()メソッドでパイプラインを開始し、実行の終了を待ちます：

```python
execution = pipeline.start()
execution.wait()
```

After the pipeline starts running, we can view the run on the SageMaker console.
パイプラインの実行が開始されると、SageMaker コンソールで実行を確認できます。
In the navigation pane, under Components and registries, choose Pipelines.
ナビゲーションペインで、コンポーネントとレジストリの下にあるパイプラインを選択します。
Choose the Redshift2Pipeline pipeline, and then choose the specific run to see its progress.
Redshift2Pipelineパイプラインを選択し、進行状況を確認するために特定の実行を選択します。
You can choose each step to see additional details such as the output, logs, and additional information.
各ステップを選択すると、出力、ログ、追加情報などの詳細を見ることができます。
Typically, this pipeline should take about 10 minutes to complete.
通常、このパイプラインは約10分で完了する。

## Conclusions 結論

In this post, we created a SageMaker pipeline that reads data from Amazon Redshift natively without requiring additional configuration or services, processed it via SageMaker Processing, and trained a scikit-learn model.
この投稿では、**追加の設定やサービスを必要とせずに Amazon Redshift からネイティブにデータを読み込む SageMaker パイプラインを作成し**、SageMaker Processing で処理し、scikit-learn モデルを学習させました。
We can now do the following:
これで次のことができる：

- Schedule the pipeline to run with Amazon EventBridge rules (see Automating Amazon SageMaker with Amazon EventBridge) Amazon EventBridgeルールで実行するパイプラインをスケジュールする（Amazon EventBridgeによるAmazon SageMakerの自動化参照）
- Create a new scheduled pipeline for inference with the TransformStep TransformStepで推論用の新しいスケジュールされたパイプラインを作成する。
- Use the model to update an existing real-time endpoint manually or as part of a SageMaker project モデルを使用して、既存のリアルタイムエンドポイントを手動で、または SageMaker プロジェクトの一部として更新します。

If you want additional notebooks to play with, check out the following:
他にもノートブックで遊びたい方は、以下をご覧ください：

- Use the Amazon Redshift Data API from within a SageMaker notebook: extra-content/data-api-discovery.ipynb SageMaker ノートブック内から Amazon Redshift Data API を使用します： extra-content/data-api-discovery.ipynb
- Integrate the Amazon Redshift Data API in an AWS Lambda function to have more granular control, and add this step to a SageMaker pipeline: extra-content/pipeline.ipynb Amazon Redshift Data API を AWS Lambda 関数に統合して、より詳細な制御を行い、このステップを SageMaker パイプラインに追加します： extra-content/pipeline.ipynb
