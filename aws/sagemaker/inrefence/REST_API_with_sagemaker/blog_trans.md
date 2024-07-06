## refs: refs：

- https://aws.amazon.com/jp/blogs/machine-learning/creating-a-machine-learning-powered-rest-api-with-amazon-api-gateway-mapping-templates-and-amazon-sagemaker/
- 日本語やく: https://aws.amazon.com/jp/blogs/news/creating-a-machine-learning-powered-rest-api-with-amazon-api-gateway-mapping-templates-and-amazon-sagemaker/

# Creating a machine learning-powered REST API with Amazon API Gateway mapping templates and Amazon SageMaker Amazon API GatewayのマッピングテンプレートとAmazon SageMakerを使って、機械学習を利用したREST APIを作成する

July 2022: Post was reviewed for accuracy.
2022年7月 ポストの正確性を確認。

Amazon SageMaker enables organizations to build, train, and deploy machine learning models.
Amazon SageMakerは、企業が機械学習モデルを構築、訓練、展開することを可能にする。
Consumer-facing organizations can use it to enrich their customers’ experiences, for example, by making personalized product recommendations, or by automatically tailoring application behavior based on customers’ observed preferences.
消費者に向き合う組織は、顧客のエクスペリエンスを向上させるためにそれを使用することができる。たとえば、個人に合わせたプロダクトの推薦を行ったり、顧客の観察された好みに基づいてアプリケーションの動作を自動的に調整したりすることができる。
When building such applications, one key architectural consideration is how to make the runtime inference endpoint available to client software running on consumer devices.
このようなアプリケーションを構築する際、アーキテクチャ上の重要な検討事項のひとつは、消費者のデバイスで実行されている**クライアント・ソフトウェアにランタイム推論エンドポイントを利用可能にする方法**である。
Typically, the endpoint is fronted as part of a broader API, based on a conventional web-friendly approach, such as REST, which offers a complete set of application functions to client software.
通常、エンドポイントは、RESTのような従来のウェブフレンドリーなアプローチに基づく、より広範なAPIの一部として前面に押し出され、クライアント・ソフトウェアにアプリケーション機能一式を提供する。

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale.
**Amazon API Gatewayは、開発者があらゆる規模のAPIを簡単に作成、公開、保守、監視、セキュア化できるフルマネージドサービス**です。
API Gateway can be used to present an external-facing, single point of entry for Amazon SageMaker endpoints, with the following benefits:
**API Gateway は、Amazon SageMaker のエンドポイントに対して、外部向けの単一エントリーポイントを提示するために使用でき**、以下のような利点があります：

- 1. Insulates clients from the specifics of the underlying implementation by translating between a client-facing REST API and the underlying Amazon SageMaker runtime inference API
  クライアント向けの REST API と基礎となる Amazon SageMaker ランタイム推論 API 間を変換することで、**基礎となる実装の仕様からクライアントを保護**します。(クライアント側が、あ、これ、Sagemakerで動いてるのかと実装の詳細を漏らす必要がないもんね...!:thinking:)
- 2. Supports authentication and authorization of client requests
  クライアント・リクエストの認証と認可をサポート
- 3. Manages client requests through the use of throttling, rate-limiting, and quota management
  スロットリング、レート制限、クォータ管理を使用してクライアントのリクエストを管理する。
- 4. Uses firewall features as provided by AWS WAF
  AWS WAFが提供するファイアウォール機能を使用する。
- 5. Enables cost savings and operational optimization through caching and request validation
  キャッシュとリクエスト検証によるコスト削減と運用の最適化
- 6. Makes it easier to create canary deployments to introduce model changes safely
  モデルの変更を安全に導入するための**カナリアデプロイ**の作成を容易にする。

<!-- ここまで読んだ! -->

In this post, I show how API Gateway can be used to front an Amazon SageMaker inference endpoint as (part of) a REST API, by making use of an API Gateway feature called mapping templates.
この投稿では、マッピングテンプレートと呼ばれる API Gateway の機能を利用して、Amazon SageMaker の推論エンドポイントを REST API の（一部として）前面に表示する方法を紹介します。
This feature makes it possible for the REST API to be integrated directly with an Amazon SageMaker runtime endpoint, thereby avoiding the use of any intermediate compute resource (such as AWS Lambda or Amazon ECS containers) to invoke the endpoint.
この機能により、REST API を Amazon SageMaker ランタイムエンドポイントに直接統合することが可能になり、**エンドポイントを呼び出すために中間計算リソース（AWS Lambda や Amazon ECS コンテナなど）を使用する必要がなくなります**。
The result is a solution that is simpler, faster, and cheaper to run.
その結果、**よりシンプルで、より速く、より安価な**ソリューションが実現した。(めちゃいいじゃん!)

This direct integration approach is especially useful for consumer applications that exhibit high traffic volumes at peak demand times.
この直接的な統合アプローチは、ピーク時に大量のトラフィックが発生する消費者向けアプリケーションに特に有効である。
Amazon SageMaker supports automatic scaling for inference endpoints, and API Gateway automatically scales to match demand, ensuring that there is always sufficient capacity to process incoming requests, and that you only pay for what you use.
Amazon SageMakerは推論エンドポイントの自動スケーリングをサポートしており、API Gatewayは需要に合わせて自動的にスケーリングされるため、常に十分な容量で着信リクエストを処理し、使用した分だけ支払うことができます。

Note: This post focuses on direct integration with Amazon SageMaker, but you can also use mapping templates in combination with an intermediate compute layer (based, for example, on AWS Lambda), in which case you can use them to reduce load on the compute layer by reshaping payloads at the gateway itself.
注意: この投稿は Amazon SageMaker との直接統合に焦点を当てていますが、**中間計算レイヤー（たとえば AWS Lambda に基づく）と組み合わせてマッピングテンプレートを使用する**こともできます。この場合、ゲートウェイ自体でペイロードを再形成することで、計算レイヤーへの負荷を軽減することができます。

- (chatGPTに聞いたメモ):
  - 直接統合の場合:
    - API Gatewayへのリクエストを直接Sagemakerに送る。マッピングテンプレートを使用して、リクエストのフォーマットをSageamkerのエンドポイントが期待する形式に整える。
  - 中間計算レイヤーを使用する場合:
    - AWP Gatewayのマッピングテンプレートを使用して、リクエストのフォーマットを中間計算レイヤーが期待する形式に整える。
    - 中間計算レイヤーはAPI Gatewayからのリクエストを受け取り、さらに必要な処理を行なった後、Sagemakerのエンドポイントに送る。
    - (なんか中間計算レイヤーが必要な理由があんまりわからない...:thinking:)

I demonstrate the approach using a console-based walk through, starting with deployment of an Amazon SageMaker model endpoint, and then stepping through the creation of an Amazon API Gateway integration with this endpoint.
Amazon SageMaker モデルエンドポイントのデプロイから始まり、このエンドポイントを使用した Amazon API Gateway インテグレーションの作成まで、コンソールベースのウォークスルーを使用して、このアプローチをデモンストレーションします。

## Overview of solution ソリューションの概要

For illustration purposes, this post employs a use case in which a TV app requests ratings predictions for a list of movies.
説明のために、この記事では、テレビアプリが映画リストの視聴率予測をリクエストするユースケースを採用している。
Whenever the app displays a page of movies, it should display them so that movies with a higher ratings prediction are more prominent on the page.
アプリが映画のページを表示するときは常に、より高い評価を予測する映画がページ上でより目立つように表示されるべきである。(あ、推薦のusecaseね。)
In this example, every user and movie can be identified by a numeric ID, and predicted ratings are on a scale of 1 to 5, with a higher rating indicating a stronger likelihood that the user will like a particular movie.
この例では、すべてのユーザーと映画は数値IDで識別でき、予測された評価は1から5のスケールであり、より高い評価はユーザーが特定の映画を好む可能性が高いことを示している。

### Architecture 建築

The following diagram summarizes the architecture, key components, and interactions in the solution.
次の図は、ソリューションのアーキテクチャ、主要コンポーネント、相互作用をまとめたものである。
End-users interact with a client application (using a web browser or mobile device) that sends a REST-style request to an API Gateway endpoint.
エンドユーザーは、クライアントアプリケーション（Web ブラウザやモバイルデバイスを使用）と対話します。クライアントアプリケーションは、API Gateway エンドポイントに REST スタイルのリクエストを送信します。
API Gateway maps this to the request format required by the Amazon SageMaker endpoint, and invokes the endpoint to obtain an inference from the model.
API Gateway はこれを Amazon SageMaker エンドポイントが要求するリクエストフォーマットにマッピングし、エンドポイントを呼び出してモデルから推論を取得します。
API Gateway subsequently receives the response from the Amazon SageMaker endpoint and maps it to a response that is sent back to the client.
その後、API Gateway は Amazon SageMaker エンドポイントからのレスポンスを受信し、クライアントに送り返されるレスポンスにマッピングします。

![]()

### Request and response formats リクエストとレスポンスのフォーマット

The solution incorporates a REST API that supports a single resource (predicted-ratings) and a GET method.
このソリューションには、単一のリソース（`predicted-ratings`）とGETメソッドをサポートするREST APIが組み込まれている。
The request takes the form:
リクエストは次のような形だ：

```shell
GET /<api-path>/predicted-ratings/{user_id}?items=id1,id2,…,idn&
```

where the path parameter user_id represents the user for which ratings are required, and the query string parameter items contains a comma-separated list of item identifiers.
ここで、pathパラメータ `user_id` は評価が必要なユーザーを表し、クエリ文字列パラメータ `items` にはアイテム識別子のカンマ区切りリスト(=推薦アイテム候補!)が含まれています。

If the request is processed successfully, the returned HTTP response has response code 200, and the body is a JSON object containing a list of predicted ratings for the specified items as follows:
リクエストが正常に処理された場合、返されるHTTPレスポンスはレスポンスコード200を持ち、ボディは以下のように指定された項目の予測評価リストを含むJSONオブジェクトである：

```shell
{
  "ratings": [
    rating_1,
    rating_2,
    …,
    rating_n
  ]
}
```

For example, you could enter the following request:
例えば、次のようなリクエストを入力することができる：

```shell
% curl "https://<api-path>/predicted-ratings/321?items=101,131,162&"
```

This would return with a response similar to the below:
すると、以下のような返答が返ってくる：

```shell
{
  "ratings": [
    3.527499437332153,    
    3.951640844345093,    
    3.658416271209717    
  ]
}
```

### Amazon SageMaker model input and output formats Amazon SageMaker モデルの入出力フォーマット

The rating predictor solution is based on a sample model that comes supplied with Amazon SageMaker, specifically: object2vec_movie_recommendation.ipynb.
評価予測ソリューションは、Amazon SageMakerに付属しているサンプルモデルに基づいています： object2vec_movie_recommendation.ipynb です。
This model inference endpoint supports a POST method, and expects the request body to contain a JSON payload as follows:
**このモデル推論エンドポイントはPOSTメソッドをサポートしており**、リクエストボディには以下のようなJSONペイロードが含まれることを想定しています：
(Sagemaker推論endpointは基本的にPOSTメソッドを使うんだったか:thinking:)

```shell
{
  "instances": [
    {"in0": [863], "in1": [882]},
    {"in0": [278], "in1": [311]},
    {"in0": [705], "in1": [578]},
    …
  ]
}
```

where in0 represents a user ID, and in1 represents a movie ID.
`in0`はユーザーID、`in1`は映画IDを表す。

The model inference returns the following output:
モデル推論は次のような出力を返す：

```shell
{
  "predictions": [
    {"scores": [3.047305107116699]},
    {"scores": [3.58427882194519]},
    {"scores": [4.356469631195068]},
    …
  ]
}
```

You can use mapping templates to map the GET request format received by the REST API to the POST input format expected by the Amazon SageMaker model endpoint, and conversely map the model output format to the response format required by the REST API.
**マッピングテンプレートを使用して、REST API が受け取る GET リクエスト形式を Amazon SageMaker モデルエンドポイントが期待する POST 入力形式にマッピング**し、逆にモデル出力形式を REST API が要求するレスポンス形式にマッピングすることができます。

<!-- ここまで読んだ! -->

### Amazon API Gateway method integration Amazon API Gatewayメソッドの統合

When you use API Gateway to create a REST API, you need to define the following configuration models for each API method:
API Gatewayを使用してREST APIを作成する場合、APIメソッドごとに以下の**configurationモデル**を定義する必要があります:

- **Method request** – Defines the data model for the REST request format, and specifies validation and authorization checks to be performed on the received REST request.
  - メソッドリクエスト - REST リクエスト形式のデータモデルを定義し、受信した REST リクエストに対して実行される検証および認可チェックを指定する。
- **Integration request** – Details how the REST request and associated parameters map to the format expected by the backend service endpoint (which in this example is an Amazon SageMaker inference endpoint).
  - 統合リクエスト - REST リクエストと関連するパラメータが、バックエンドのサービスエンドポイント (この例では Amazon SageMaker 推論エンドポイント) が期待する形式にどのようにマッピングされるかを詳細に説明します。
- **Integration response** – Details how the response received from the backend service (including errors) map to the response format expected by API Gateway.
  - 統合レスポンス - バックエンドサービスから受け取ったレスポンス（エラーを含む）が、API Gatewayが期待するレスポンスフォーマットにどのようにマッピングされるかを詳細に説明します。
- **Method Response** – Defines the data model and response format expected by the REST API.
  - メソッド・レスポンス - REST API が期待するデータ・モデルとレスポンス・フォーマットを定義します。

The following diagram depicts the processing flow, and shows how an example request and response are transformed at each stage.
次の図は処理の流れを描いており、リクエストとレスポンスの例が各ステージで どのように変換されるかを示している。

![]()

### Mapping Templates マッピング・テンプレート

As part of the integration request and response configurations, the solution defines mapping templates using the Apache Velocity Template Language (VTL).
integrationリクエストとintegrationレスポンスの設定の一部として、このソリューションは、Apache Velocity Template Language (VTL) を使用してマッピングテンプレートを定義します。(VTLっていうDSLがあって、その言語を使ってマッピングテンプレートを定義するよってこと?? 文脈的に、他の言語を使って定義する方法もありそう...??:thinking:)
VTL is a templating language that was originally designed for web development, but can also be used as a data format transformation tool to convert from one JSON format to another.
VTLは、もともとウェブ開発用に設計された**テンプレート言語**だが、あるJSONフォーマットから別のフォーマットに変換するデータフォーマット変換ツールとしても使用できる。(templating language = 動的なコンテンツを生成するための言語の一種?:thinking:)
With mapping templates, you can use VTL templates to convert from the REST request format to the model input format, and to convert the model output to the REST response format.
マッピングテンプレートを使用すると、VTLテンプレートを使用して、**RESTリクエスト形式からモデル入力形式に変換し、モデル出力をRESTレスポンス形式に変換**することができます。

<!-- ここまで読んだ! -->

## Walkthrough steps チュートリアルの手順

The walkthrough contains the following key steps:
このウォークスルーには、以下の重要なステップが含まれている：

- Build and deploy an Amazon SageMaker model
Amazon SageMakerモデルの構築とデプロイ (ここは既知!)

- Test the Amazon SageMaker model endpoint using the AWS CLI
AWS CLI を使用して Amazon SageMaker モデルエンドポイントをテストします。(ここもほぼ既知)

<!-- ここから未知 -->

- Create an IAM execution role for the REST API
REST API用のIAM実行ロールを作成する

- Build an API Gateway endpoint for the REST API
REST API用のAPI Gatewayエンドポイントの構築

- Create a mapping template for request integration
リクエスト統合用のマッピングテンプレートを作成する

- Create a mapping template for response integration
レスポンス統合用のマッピングテンプレートを作成する

- Deploy and test the API Gateway endpoint
API Gatewayエンドポイントのデプロイとテスト

<!-- ここまで読んだ -->

## Prerequisites 前提条件

To follow this walkthrough, you need to meet the following prerequisites:
このウォークスルーに従うには、以下の前提条件を満たす必要がある：

- Access to an AWS account – You need sufficient IAM permissions to work with IAM roles, Amazon SageMaker, Amazon S3, and API Gateway.
  - AWSアカウントへのアクセス - IAMロール、Amazon SageMaker、Amazon S3、API Gatewayを使用するには、十分なIAM権限が必要です。
- AWS CLI – Install the latest version.
  - AWS CLI - 最新バージョンをインストールしてください。
- Curl utility – Use version 7.52 onwards.
  - Curlユーティリティ - バージョン7.52以降を使用してください。
  - (あ、curlコマンドね!)

<!-- 前提条件は全て満たしてそう -->

## Step 1: Building and deploying the Amazon SageMaker model ステップ 1： Amazon SageMaker モデルの構築とデプロイ

<!-- このステップは既知なので、飛ばして良さそう。 -->

For this step, you need an S3 bucket to store the model data.
このステップでは、モデルデータを保存するS3バケットが必要です。
You can use an existing bucket or create a new one.
既存のバケツを使うことも、新しいバケツを作ることもできます。
Record the name of your bucket as you shall need it later.
後で必要になるので、バケツの名前を記録しておく。

Create your model using an Amazon SageMaker Notebook instance.
Amazon SageMaker Notebook インスタンスを使用してモデルを作成します。
Complete the following steps:
以下のステップを完了する：

- 1. Log in to your AWS account using the AWS Management Console.
AWSマネジメントコンソールを使用して、AWSアカウントにログインします。

- 2. On the Amazon SageMaker dashboard, under Notebook Instances, choose Create Notebook Instance.
Amazon SageMakerのダッシュボードで、Notebook Instancesの下にあるCreate Notebook Instanceを選択します。

- 3. Under Notebook instance settings, specify a name for your notebook.
ノートブックのインスタンス設定で、ノートブックの名前を指定します。

For this example, you can set the instance type to ml.t2.medium, which is the most cost-effective option.
この例では、インスタンスタイプをml.t2.mediumに設定することができる。
In practice, you would select the instance type based on the size of the dataset and the nature of the data transformation.
実際には、データセットのサイズとデータ変換の性質に基づいてインスタンスタイプを選択することになる。

- 4. Under Permissions and Encryption, set the IAM role to Create a new role.
権限と暗号化]で、IAMロールを[新しいロールを作成]に設定する。

- 5. Ensure that S3 buckets you specify is selected, specify the bucket name for your bucket, and select Create role.
指定したS3バケットが選択されていることを確認し、バケットのバケット名を指定し、Create roleを選択する。

- 6. Leave the remaining settings with the default value.
残りの設定はデフォルト値のままにしておきます。

- 7. Choose Create notebook instance.
ノートブックのインスタンスを作成するを選択します。

It takes a few minutes to create your instance.
インスタンスの作成には数分かかります。
When the status changes from Pending to InService, your notebook instance is ready to use.
ステータスがPendingからInServiceに変わると、ノートブック・インスタンスは使用できるようになります。

- 8. Under Actions, choose Open JupyterLab.
Actions]で[Open JupyterLab]を選択します。

- A new browser tab opens for your Jupyter notebook.
Jupyterノートブック用の新しいブラウザ・タブが開きます。

- From the left navigation bar, choose the icon for Amazon SageMaker sample notebooks (hover over the icon to see the label).
左のナビゲーションバーから、Amazon SageMakerサンプルノートブックのアイコンを選択します（アイコンにカーソルを合わせるとラベルが表示されます）。

From the list of sample notebooks, select object2vec_movie_recommendation.ipynb.
サンプルノートブックのリストから、object2vec_movie_recommendation.ipynbを選択します。
as shown below:
以下のように：

The sample notebook you opened is read-only, so you need to create a writeable copy.
あなたが開いたサンプル・ノートブックは読み取り専用なので、書き込み可能なコピーを作成する必要があります。

Choose Create a Copy at the top right of the pane.
ペインの右上にある「コピーを作成」を選択します。

When prompted to Select Kernel use conda_python3.
Kernel use conda_python3を選択するようプロンプトが表示されます。

You are now ready to build and train the model in your notebook.
これで、ノートブックでモデルを構築し、トレーニングする準備が整いました。
This notebook creates two model inference endpoints (one for ratings prediction, and one for recommendations).
このノートブックは、2つのモデル推論エンドポイント（1つは視聴率予測用、もう1つはレコメンデーション用）を作成します。
You only need the first one, so you do not need to execute all the cells in the notebook.
必要なのは最初の1つだけなので、ノートブックのすべてのセルを実行する必要はない。

Before executing any cells, complete the following steps:
セルを実行する前に、以下のステップを完了する：

In your notebook, scroll down to the section Model training and inference (just over half-way down the notebook).
ノートブックで、「モデルのトレーニングと推論」のセクションまでスクロールダウンする（ノートブックの半分強）。
In the first cell (labeled Define S3 bucket that hosts data and model, and upload data to S3), set the bucket name to your choice of S3 bucket as identified earlier.
最初のセル（Define S3 bucket that host data and model, and upload data to S3）で、バケット名を先ほど選択したS3バケットに設定する。

Starting from the top, use your notebook to execute all cells in order until you get to just before the Recommendation task section (which is about three-quarters of the way down the notebook).
上から順番に、ノートブックを使って、推薦タスクセクションの直前（ノートブックの4分の3ほど下）まで、すべてのセルを実行する。

You can either do this by stepping through one cell at a time, or by selecting the first cell in the Recommendation task section and then, under Run, choose Run All Above Selected Cell (see below).
一度にセルを一つずつ見ていくか、推薦タスク・セクションで最初のセルを選択し、「実行」で「選択したセルより上のすべてを実行」を選択することでこれを行うことができる（下図参照）。

Model training and deployment takes approximately 10 minutes.
モデルのトレーニングと展開にかかる時間は約10分。
When it is complete, proceed with the following steps:
完了したら、次のステップに進む：

On the Amazon SageMaker console, under Inference, choose Endpoints.
Amazon SageMaker コンソールの「推論」で「エンドポイント」を選択します。

Verify that you can see the runtime endpoint.
ランタイム・エンドポイントが見えることを確認する。

Record the endpoint name and ARN as you will need these later.
**エンドポイント名とARN**は後で必要になるので記録しておく。

## Step 2: Testing the Amazon SageMaker model endpoint using the AWS CLI ステップ 2： AWS CLI を使用した Amazon SageMaker モデルエンドポイントのテスト

You can test the inference endpoint using the AWS CLI as follows:
以下のようにAWS CLIを使って推論エンドポイントをテストすることができる：

```shell
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name <endpoint-name> \
  --body '{"instances": [{"in0":[863],"in1":[882]}]}' \
  --content-type application/json \
  --accept application/json \
  results
```

Note: the above assumes you are using a bash-compatible shell.
注意 上記は、bash互換のシェルを使用していることを前提としています。
If you are using the standard Windows command line, replace the outer single quotes with double quotes for the body parameter, and escape the double quotes characters within the JSON.
Windows標準のコマンドラインを使用している場合、bodyパラメータでは外側のシングルクォートをダブルクォートに置き換え、JSON内ではダブルクォート文字をエスケープする。

If your endpoint is working correctly, you should see a file called results that contains output similar to the following:
エンドポイントが正しく機能していれば、以下のような出力を含むresultsというファイルが表示されるはずだ：

```shell
{"predictions":[{"scores":[2.433111906051636]}]}
```

Now that you have a working Amazon SageMaker endpoint, you can build a REST API in front of it.
これで Amazon SageMaker のエンドポイントが使えるようになったので、その手前に REST API を構築することができます。

## Step 3: Creating an execution role for the REST API REST APIの実行ロールの作成

<!-- ここから未知! -->

Before you build the REST API, you need to create an execution role that gives your API the necessary permission to invoke your Amazon SageMaker endpoint.
REST API を構築する前に、**Amazon SageMaker のエンドポイントを呼び出すために必要な権限を API に与える実行ロール**を作成する必要があります。
(AWS API Gatewayに移譲するIAM Role??:thinking:)
Complete the following steps:
以下のステップを完了する：

On the IAM console, under Roles, choose Create Role.
IAMコンソールの「Roles」で「Create Role」を選択する。

For Select type of trusted entity, select AWS Service.
Select type of trusted entity」で「AWS Service」を選択します。

Choose the service API Gateway.
API Gatewayサービスを選択します。(あ、じゃあやっぱりAPI GatewayにassumeするRoleなのか...!)

Choose Next until you reach the Review.
レビュー（Review）に到達するまで、次へ（Next）を選択します。

You can see that a policy has been included which allows API Gateway to push logs to CloudWatch.
**API GatewayがログをCloudWatchにプッシュすることを許可するポリシーが含まれていること**が確認できます。
(`AmazonAPIGatewayPushToCloudWatchLogs`っていうAWS managed policyがあるみたい:thinking:)

Give your role a name, for example, APIGatewayAccessToSageMaker.
`APIGatewayAccessToSageMaker`のように、ロールに名前を付ける。

Choose Create Role.
ロールを作成する。

You now need to add permissions so your role can invoke the Amazon SageMaker endpoint.
**ロールが Amazon SageMaker エンドポイントを呼び出せるように、権限を追加する**必要があります。
(どんなアクション権限を付与する必要がある?:thinking:)

Use the role filter to find the role you just created.
ロールフィルタを使用して、作成したばかりのロールを見つけます。

Choose the role you created to see the role summary screen.
作成したロールを選択すると、ロールのサマリー画面が表示されます。

Choose Add Inline Policy.
Add Inline Policyを選択する。

On the Create Policy screen, select the service SageMaker and the action InvokeEndpoint.
ポリシーの作成画面で、**SageMaker サービスと InvokeEndpoint アクション**を選択します。

For Resources, select Specific and enter the ARN for your Amazon SageMaker endpoint.
[リソース]で[特定]を選択し、Amazon SageMaker エンドポイントの ARN を入力します。
(アクション権限の対象リソースを、今回用意したSagemakerエンドポイントのARNのみに指定:thinking:)

Choose Review Policy.
レビューポリシーを選択する。

Give your policy a name, for example, SageMakerEndpointInvokeAccess.
`SageMakerEndpointInvokeAccess` のように、ポリシーに名前を付けます。
(自作Policyだけど、HogehogePolicyじゃなくて良いんだ。まあ自明だからかな:thinking:)

Choose Create Policy.
ポリシーの作成を選択します。

On the role summary page, record the ARN for the role as you will need this later.
IAM roleのsummaryページで、**ロールのARN**を記録しておく。
(このARNは、API GatewayのIAM Roleに設定するARNのはず:thinking:)

<!-- ここまで読んだ! -->

## Step 4: Building an API Gateway endpoint ステップ4： API Gatewayのエンドポイントを構築する

In this section, you build your REST API.
このセクションでは、REST APIを構築します。

### Creating an API APIの作成

Complete the following steps:
以下のステップを完了する：
(AWSコンソールで定義する以外の場合は、cdkとかaws python sdkで定義する感じなのかな:thinking:)

- On the API Gateway console, choose Create API.
API Gatewayコンソールで、Create APIを選択します。

- Choose REST.
RESTを選択する。

- Choose New API.
New APIを選択する。

- Give your API a name, for example, RatingsPredictor.
APIに名前をつける。例えば、`RatingsPredictor`。

- For Endpoint Type, choose Regional.
Endpoint Type で Regional を選択する。

- Choose Create API.
Create APIを選択します。

Note: In a production system, you should consider whether you would benefit from the Edge Optimized option.
注意: 本番システムでは、`Edge Optimized` オプションが有益かどうかを検討する必要があります。(どんなオプション?)

### Creating a resource リソースの作成

(APIオブジェクトを作ってから、リソースを定義する??)

In the Resources editor, from the Actions menu, choose CreateResource.
ResourcesエディタのActionsメニューから、CreateResourceを選択する。

For Resource Name, enter predicted-ratings.
リソース名には`predicted-ratings`と入力する。

Ensure that the Resource Path field also contains predicted-ratings.
リソースパスのフィールドにも`predicted-ratings`が含まれていることを確認する。

Choose Create Resource.
Create Resourceを選択する。

You should see the predicted-ratings resource appear in the navigation tree.
ナビゲーションツリーに`predicted-ratings`リソースが表示されるはずです。

Choose the predicted-ratings resource you created.
**作成した予測評価リソースを選択**します。

From the Actions menu, choose Create Resource.
ActionsメニューからCreate Resourceを選択する。

For Resource Path, enter {user_id}.
Resource Pathには`{user_id}`と入力する。(これはパスパラメータを定義してる??:thinking:)

For Resource Name, enter user_id.
リソース名には`user_id`を入力する。

Choose Create Resource.
Create Resourceを選択する。

The resource navigation tree should now be similar to the following screenshot, and show /predicted-ratings/{user_id}.
リソース・ナビゲーション・ツリーは以下のスクリーンショットのようになり、`/predicted-ratings/{user_id}`が表示されます。
(ここでリソースを定義してるのって、エンドポイントを階層的に定義していくってことか...! そういえばWeb API: the good partsによると、エンドポイント=リソースの場所みたいな感じだったっけ??:thinking:)

### Creating a GET method GETメソッドの作成

The next step is to create a GET method on the resource path /predicted-ratings/{user_id} and integrate it with your Amazon SageMaker endpoint.
次のステップは、**リソースパス `/predicted-ratings/{user_id}` に GET メソッドを作成し、Amazon SageMaker エンドポイントと統合すること**です。
Complete the following steps:
以下のステップを完了する：

- From the Actions menu, choose {user_id}.
アクションメニューから`{user_id}`を選ぶ。(=リソースを選ぶ)

- Choose Create Method.
"Create Method"を選ぶ。

- From the drop-down that appears under the {user_id} resource, select GET and confirm by clicking the tick mark.
user_id}リソースの下に表示されるドロップダウンから、GETを選択し、チェックマークをクリックして確定します。

The right-hand pane now displays a Setup screen.
右側のペインにセットアップ画面が表示されます。
See the following screenshot.
次のスクリーンショットをご覧ください。

![]()

- For Request Integration type, choose AWS Service.
Request Integrationのタイプは、**AWS Serviceを選択**します。

- For AWS Region, enter your Region.
AWS Regionには、あなたのリージョンを入力してください。

For AWS Service, choose SageMaker Runtime.
AWS Service には、**SageMaker Runtime を選択**します。(なるほど、これがSagemakerエンドポイントを指定してるのか:thinking:)

Leave AWS Subdomain blank.
AWS サブドメインは空白のままにしておきます。

For HTTP method, choose POST.
HTTPメソッドは**POSTを選択**する。(SagemakerエンドポイントにはPOSTメソッドでリクエストを送るから:thinking:)

For Action Type, choose Use Path override.
Action Type（アクションの種類）で、**Use Path override（パスのオーバーライドを使用）を選択**する。(ほうほう??:thinking:)

For Path override, enter the Amazon SageMaker endpoint path using the format endpoints/<sagemaker-endpoint-name>/invocations.
パスのオーバーライドには、`endpoints/<sagemaker-endpoint-name>/invocations` の形式で Amazon SageMaker のエンドポイントパスを入力します。(うんうん、転送先というか...!)

For Execution role, enter the ARN of the role you created earlier.
実行ロールには、先ほど作成したロールのARNを入力します。(うんうん、やはり。)

For Content Handling, choose Passthrough.
Content Handling（コンテンツ処理）」で「Passthrough（パススルー）」を選択する。

Select Use Default Timeout.
"Default Timeoutを使用"を選択します。

Choose Save.
保存を選択する。

You have created a GET endpoint in the REST API, and mapped it to a POST endpoint.
**REST APIでGETエンドポイントを作成し、それをPOSTエンドポイントにマッピングした**。
(エンドポイントはリソースの指定、METHODはそのリソースに対してどんな操作をするかの指定だよね...!:thinking:)
In the next step, you use mapping templates to map parameters passed in the GET request (from the path and query-string) into the right places in the POST request expected by the Amazon SageMaker endpoint.
次のステップでは、**マッピングテンプレートを使用して、GET リクエストで渡されたパラメータ（パスとクエリ文字列から）を、Amazon SageMaker エンドポイントが期待する POST リクエストの適切な場所にマッピング**します。
(なるほど、エンドポイント & methodのmappingの後に、パラメータのmappingをする、という二段階のmapping手順になってるのか...!:thinking:)

<!-- ここまで読んだ! -->

## Step 5: Create a mapping template for request integration ステップ5： リクエスト統合用のマッピングテンプレートを作成する

You should now see a Method Execution screen in the right-hand pane.
これで、右側のペインにメソッド実行画面が表示されるはずです。
See the following screenshot.
次のスクリーンショットをご覧ください。

![]()

This contains a diagram showing how requests flow from your REST API to the Amazon SageMaker runtime and how responses flow back.
これには、REST API から Amazon SageMaker ランタイムへのリクエストの流れと、レスポンスの流れを示す図が含まれています。

### Creating a VTL mapping template VTL マッピングテンプレートの作成

In this next step, create a VTL mapping template to convert GET requests received on the REST API to POST requests expected by the Amazon SageMaker runtime.
次のステップでは、**REST API で受け取った GET リクエストを Amazon SageMaker ランタイムが期待する POST リクエストに変換する VTL マッピングテンプレート**を作成します。
(エンドポイント * methodのmappingはstep 4で完了済みなので、ここではパラメータを変換するmappingを行う:thinking:)
Complete the following steps:
以下のステップを完了する：

- Choose Integration Request.
統合リクエストを選択します。

- Expand the Mapping Templates.
マッピングテンプレートを展開します。

- Select Request Body Passthrough: Never.
リクエスト・ボディ・パススルーを選択します： "Never"。 (どういうoptionなのか:thinking:)

You can safely ignore the warning because it disappears after you specify a mapping template.
マッピングテンプレートを指定すると、警告が消えるので、無視しても大丈夫です。

- Choose Add mapping template.
マッピングテンプレートの追加を選択します。

- For Content-Type, specify application/json and click the tick box to confirm.
Content-Typeにはapplication/jsonを指定し、チェックボックスをクリックして確定する。

If you scroll down, you see a multi-line text entry field.
下にスクロールすると、複数行のテキスト入力フィールドが表示される。
This is where you add your VTL template.
ここでVTLテンプレートを追加する。

- Enter the following template:
以下のテンプレートを入力する：

```shell
{
  "instances": [
#set( $user_id = $input.params("user_id") )
#set( $items = $input.params("items") )
#foreach( $item in $items.split(",") )
    {"in0": [$user_id], "in1": [$item]}#if( $foreach.hasNext ),#end
    $esc.newline
#end
  ]
}
```

- Choose Save.
保存を選択する。


The template defines what goes into the body of the POST request.
**テンプレートはPOSTリクエストのボディに入るものを定義する。** (うんうん、確かにそう見える...!)
The first two lines are copied into the request body exactly as specified.
最初の2行は、指定されたとおりにリクエストボディにコピーされる。
The third line uses a #set directive to extract and store the user_id path parameter in the variable $user_id.
3行目は、**#setディレクティブを使ってuser_idパス・パラメーターを取り出し、変数$user_idに格納**している。(ふむふむ、`set`ディレクティブ)
The fourth line extracts the query string parameter items and places it in the variable $items.
4行目は、**クエリ文字列のパラメーターitemsを取り出し、変数$itemsに入れる**。
This is stored as a single string containing a comma-separated list of items.
これは、カンマで区切られたアイテムのリストを含む単一の文字列として保存される。

Lines 5-8 loop through all the items and generate the required JSON for each one.
5-8行目は、すべてのアイテムをループし、それぞれに必要なJSONを生成する。
The template converts the string held in $items to an array using the string split() method, and iterates through this using a #foreach directive.
テンプレートは、文字列の`split()`メソッドを使用して`$items`に保持されている文字列を配列に変換し、`#foreach`ディレクティブを使用してこれを繰り返し処理します。
A comma separator is inserted between JSON objects, with no comma after the last entry.
JSONオブジェクトの間にはカンマ区切りが挿入され、最後のエントリーの後にはカンマは挿入されない。


(VTLの文法を覚えないといけないと思ったけど、おそらくAPI間のパラメータのmappingってパターンがかなり限られてると思うので、まあ楽勝なのかも。)

### Testing the mapping
マッピングのテスト

You can now test this mapping using the API Gateway built-in test harness.
これで**API Gatewayのbuild-inのテストハーネスを使って**、このマッピングをテストできる。
Complete the following steps:
以下のステップを完了する：

- Choose Method Execution.
メソッド実行を選択する。

- Choose Test.
テストを選択する。

- For Path parameter {user_id}, enter 321.
パス・パラメータ `{user_id}` には 321 と入力する。

- For Query Strings parameter, enter items=101,131,162&.
Query Stringsパラメータには、`items=101,131,162&`と入力します。

- Choose Test.
テストを選択する。

If everything is working correctly, you should see response code 200, with a response body that contains a JSON object similar to the below:
すべてが正しく機能していれば、レスポンス・コード200が表示され、以下のようなJSONオブジェクトを含むレスポンス・ボディが表示されるはずです：

```shell
{
  "predictions": [
    {"scores": [3.527499437332153]},
    {"scores": [3.951640844345093]},
    {"scores": [3.658416271209717]}
  ]
}
```

You can also scroll through the logs to verify the sequence of events.
また、ログをスクロールして一連の出来事を確認することもできる。
You should see something similar to the following:
以下のようなものが表示されるはずだ: 

```shell
<timestamp>: Endpoint request body after transformations: {
  "instances": [
    {"in0": [321], "in1": [101]},
    {"in0": [321], "in1": [131]},
    {"in0": [321], "in1": [162]}
  ]
}
<timestamp> : Sending request to https://runtime.sagemaker.eu-west-1.amazonaws.com/endpoints/recs/invocations
<timestamp> : Received response. Status: 200, Integration latency: 232 ms
```

This proves that the REST request converted successfully to the input format required by the model, and that the model runtime executed successfully.
これは、RESTリクエストがモデル(=たぶんSagemakerエンドポイントのこと!)によって要求される入力フォーマットに正常に変換され、モデルのランタイムが正常に実行されたことを証明します。
However, the returned response body is still not in the format stipulated for the REST API.
**しかし、返されるレスポンス・ボディは、まだREST APIで規定されている形式ではない**。(あ、確かにレスポンスの中身のmappingはまだだった...!)
By default, API Gateway sets up the response integration to pass the response through unaltered.
**デフォルトでは、API Gatewayはレスポンス統合を設定し、レスポンスをそのまま通過させる**。(なるほど!)
In the next step, you add a second mapping template to convert the model response to the required REST API format.
次のステップでは、**2つ目のマッピングテンプレートを追加**して、モデルのレスポンスを必要な REST API フォーマットに変換します。(別のmappingテンプレートを追加する必要があるのか。)

<!-- ここまで読んだ! -->

## Step 6: Creating a mapping template for response integration ステップ6： レスポンス統合用のマッピングテンプレートの作成

To add a mapping template for the response, complete the following steps:
応答用のマッピングテンプレートを追加するには、以下の手順を実行する：

- On the Method Execution screen, choose Integration Response.
メソッド実行画面で、Integration Responseを選択します。

You should see a single entry with HTTP status regex set to the single character, with method response 200.
HTTPステータスの正規表現が1文字に設定され、メソッドのレスポンスが200である1つのエントリーが表示されるはずだ。
This is the default response rule, which returns a 200 response code and passes the response through unaltered.
これは**デフォルトのレスポンス・ルール**で、200レスポンス・コードを返し、レスポンスをそのまま通過させる。

- Expand this rule.
このルールを拡大する。(=編集する?)

- Under Mapping Templates, choose application/json.
Mapping Templatesで`application/json`を選択する。

- Enter the following mapping template
以下のマッピング・テンプレートを入力する。

```shell
{
  "ratings": [
#set( $predictions = $input.path("$.predictions") )
#foreach( $item in $predictions )
    $item.scores[0]#if( $foreach.hasNext ),#end
    $esc.newline
#end
  ]
}
```

This template iterates through the list of predictions returned by the model, and produces output that is compliant with the format required by the REST API.
このテンプレートはモデルによって返された予測値のリストを繰り返し処理し、REST APIによって要求される形式に準拠した出力を生成します。

- Choose Save.
保存を選択する。

You can test this again by following the same procedure you used earlier, and this time you should see the output in the required response format.
先ほどと同じ手順でもう一度テストすると、今度は必要なレスポンス・フォーマットで出力されるはずだ。

<!-- ここまで読んだ! -->

## Step 7: Deploying and testing the API Gateway endpoint ステップ7： API Gateway エンドポイントのデプロイとテスト

You are now ready to deploy your REST API.
これでREST APIをデプロイする準備が整いました。
Complete the following steps:
以下のステップを完了する：

- On the Method Execution screen, under Actions, choose Deploy API.
メソッド実行]画面の[アクション]で[APIのデプロイ]を選択します。

- For Deployment stage, choose [New Stage].
Deployment stageでは、`[New Stage]`を選択します。(stageって、API Gatewayの概念??:thinking:)

- Give your stage a name, such as test.
ステージにテストなどの名前をつける。

- Enter the required descriptions for this stage and deployment.
このステージとデプロイに必要な説明を入力します。

- Choose Deploy.
デプロイを選択します。

You should now see a Stage Editor in the right-hand pane, with an Invoke URL endpoint for your deployed API.
これで右側のペインにStage Editorが表示され、デプロイしたAPIのInvoke URLエンドポイントが表示されるはずです。
You can use curl to test your deployed endpoint.
デプロイしたエンドポイントをテストするには、curl を使用します。

At the command line, enter the following:
コマンドラインで次のように入力する：

```shell
curl "<invoke-url>/predicted-ratings/321?items=101,131,162&"
```

Replace <invoke-url> with the URL for your endpoint.
<invoke-url>をエンドポイントのURLに置き換えてください。

You should see output similar to the below:
以下のような出力が表示されるはずだ：

```shell
{
  "ratings": [
    3.527499437332153,
    3.951640844345093,
    3.658416271209717
  ]
}
```

(publicアクセス??:thinking:)

You now have a deployed, working REST API that is integrated with your Amazon SageMaker runtime.
これで、Amazon SageMaker ランタイムと統合された REST API がデプロイされ、動作するようになりました。

<!-- ここまで読んだ! -->

## Additional considerations その他の考慮事項

This post focused on how to use API Gateway mapping templates to transform requests and responses between formats required by the REST API and model runtime.
この投稿では、API Gatewayのマッピングテンプレートを使用して、REST APIとモデルランタイムが要求するフォーマット間でリクエストとレスポンスを変換する方法に焦点を当てました。
API Gateway provides numerous additional features that you can use to implement authorization, request validation, caching, response error code mapping, and throttling.
**API Gatewayは、認証、リクエストの検証、キャッシュ、レスポンスエラーコードのマッピング、スロットリングを実装するために使用できる多くの追加機能を提供しています**。(これでセキュリティ的な観点を考慮できるってことか:thinking:)
When you are designing your overall architecture, consider how best to use these features.
全体的なアーキテクチャを設計する際には、これらの機能をどのように使うのが最適かを検討してください。

This post used an example in which you could map requests and responses directly without the need for any intermediate compute resource.
この投稿では、中間的なコンピュート・リソースを必要とせずに、リクエストとレスポンスを直接マッピングできる例を使用した。
This may not be possible in all situations, such as when you need to enrich the request body with additional data from another source.
これは、リクエストボディを別のソースからの追加データで補完する必要がある場合など、すべての状況で可能とは限りません。(ex. リクエストボディのuser_idに1を追加する、みたいな前処理??:thinking:)
In such cases, you can still use VTL-based mapping templates to pre-process requests and post-process responses, which reduces the load on any intermediate compute layer.
このような場合でも、VTLベースのマッピングテンプレートを使って、リクエストの前処理とレスポンスの後処理を行うことができる。

## Cleaning up 後始末

When you are finished experimenting with your setup, clean up the various resources that you used on API Gateway, S3, and Amazon SageMaker.
セットアップの実験が終わったら、API Gateway、S3、Amazon SageMakerで使用した様々なリソースをクリーンアップします。
Make sure that you delete the Amazon SageMaker endpoint so you don’t continue to accrue charges.
Amazon SageMakerのエンドポイントを削除して、料金が発生し続けないようにしてください。

If you wish to retain the model and API Gateway setup for further experimentation at a later time, you can re-create the endpoint when required.
後日、さらなる実験のためにモデルとAPI Gatewayのセットアップを保持したい場合、必要に応じてエンドポイントを再作成することができます。
Remember to update the API Gateway request integration if you use a different endpoint name.
異なるエンドポイント名を使用する場合は、API Gatewayリクエスト統合を更新することを忘れないでください。

## Conclusion 結論

This post demonstrated how to use API Gateway to create a public RESTful endpoint for an Amazon SageMaker inference.
この投稿では、**API Gateway を使用して Amazon SageMaker 推論のパブリック RESTful エンドポイントを作成する方法**を紹介しました。
Specifically, it showed how to use mapping templates and VTL to transform requests and responses to match the formats expected by the public-facing REST endpoint and the internal inference endpoint.
具体的には、**マッピング・テンプレートとVTLを使用して、リクエストとレスポンスを、一般向けのRESTエンドポイントと内部のSagemaker推論エンドポイントが期待するフォーマットに合わせて変換**する方法を示した。

Mapping templates can help you avoid using intermediate compute resources between API Gateway and Amazon SageMaker.
**マッピングテンプレートは、API GatewayとAmazon SageMakerの間で中間コンピュートリソースを使用しないようにするのに役立ちます**。
As a result, you reduce the latency and operational complexity of your application.
**その結果、アプリケーションのレイテンシーと運用の複雑さが軽減されます**。(これは嬉しいね!:smile:)
API Gateway Mapping templates are also useful in situations in which you cannot avoid intermediate compute; you can still use them to perform pre- and post-processing to reduce load on the compute layer.
API Gatewayのマッピングテンプレートは、中間コンピュートを避けることができない状況でも役立ちます。引き続き、コンピュート・レイヤーへの負荷を軽減するために前処理と後処理を実行するために使用できます。
(あんまり思いつかないけど、mappingテンプレートでは記述できないような、複雑なテクニカルな前処理がある場合とかに、Lambdaなどの中間コンピュートリソースを使うのかな:thinking:)

This approach is especially useful for use cases characterized by high-volume peak demand with low-latency inference, as typically seen in consumer applications.
このアプローチは、**消費者向けアプリケーション(つまりtoCか!)で一般的に見られるような、高いボリュームのピーク需要と低レイテンシーの推論を特徴とするユースケースに特に有用**です。
(いいね...!:smile:)
