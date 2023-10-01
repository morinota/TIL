## Link リンク

- https://aws.amazon.com/jp/blogs/machine-learning/build-and-deploy-ml-inference-applications-from-scratch-using-amazon-sagemaker/ https://aws.amazon.com/jp/blogs/machine-learning/build-and-deploy-ml-inference-applications-from-scratch-using-amazon-sagemaker/

# Build and deploy ML inference applications from scratch using Amazon SageMaker Amazon SageMakerを使ってML推論アプリケーションをゼロから構築しデプロイする

As machine learning (ML) goes mainstream and gains wider adoption, ML-powered inference applications are becoming increasingly common to solve a range of complex business problems.
機械学習（ML）が主流となり、より広く採用されるようになるにつれ、MLを利用した推論アプリケーションは、さまざまな複雑なビジネス上の問題を解決するためにますます一般的になってきている。
The solution to these complex business problems often requires using multiple ML models and steps.
このような複雑なビジネス問題の解決には、多くの場合、複数のMLモデルとステップを使用する必要がある。
This post shows you how to build and host an ML application with custom containers on Amazon SageMaker.
この投稿では、Amazon SageMaker上でカスタムコンテナを使ってMLアプリケーションを構築し、ホストする方法を紹介します。

Amazon SageMaker offers built-in algorithms and pre-built SageMaker docker images for model deployment.
Amazon SageMaker は、組み込みのアルゴリズムと、モデルのデプロイ用にあらかじめ構築された SageMaker docker イメージを提供します。
But, if these don’t fit your needs, you can bring your own containers (BYOC) for hosting on Amazon SageMaker.
しかし、これらがあなたのニーズに合わない場合は、**Amazon SageMakerでホスティングするためのコンテナを自分で持ち込む(Bring Your Own Containers, BYOC)**ことができる。

There are several use cases where users might need to BYOC for hosting on Amazon SageMaker.
Amazon SageMakerでのホスティングにBYOCが必要なケースはいくつかあります。

1. Custom ML frameworks or libraries: If you plan on using a ML framework or libraries that aren’t supported by Amazon SageMaker built-in algorithms or pre-built containers, then you’ll need to create a custom container. カスタム ML フレームワークまたはライブラリ:Amazon SageMaker の組み込みアルゴリズムやビルド済みコンテナでサポートされていない ML フレームワークやライブラリを使用する場合は、カスタムコンテナを作成する必要があります。

2. Specialized models: For certain domains or industries, you may require specific model architectures or tailored preprocessing steps that aren’t available in built-in Amazon SageMaker offerings. 特殊なモデル: 特定のドメインや業種では、Amazon SageMaker のビルトイン製品では利用できない特定のモデルアーキテクチャやカスタマイズされた前処理ステップが必要になる場合があります。

3. Proprietary algorithms: If you’ve developed your own proprietary algorithms inhouse, then you’ll need a custom container to deploy them on Amazon SageMaker. 独自のアルゴリズム: 独自のアルゴリズムを社内で開発した場合、Amazon SageMaker にデプロイするためのカスタムコンテナが必要になります。

4. Complex inference pipelines: If your ML inference workflow involves custom business logic — a series of complex steps that need to be executed in a particular order — then BYOC can help you manage and orchestrate these steps more efficiently. 複雑な推論パイプライン: ML推論ワークフローにカスタムのビジネスロジック（特定の順序で実行する必要がある一連の複雑なステップ）が含まれる場合、BYOCはこれらのステップをより効率的に管理し、オーケストレーションするのに役立ちます。

## Solution overview 解決策の概要

In this solution, we show how to host a ML serial inference application on Amazon SageMaker with real-time endpoints using two custom inference containers with latest scikit-learn and xgboost packages.
このソリューションでは、最新のscikit-learnとxgboostパッケージを使用した2つのカスタム推論コンテナを使用して、リアルタイムエンドポイントを持つAmazon SageMaker上でMLシリアル推論アプリケーションをホストする方法を示します。

The first container uses a scikit-learn model to transform raw data into featurized columns.
1番目のコンテナは、scikit-learnモデルを使って生データをフィーチャー化されたカラムに変換する。
It applies StandardScaler for numerical columns and OneHotEncoder to categorical ones.
数値列にはStandardScalerを適用し、カテゴリー列にはOneHotEncoderを適用する。

![](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2023/09/19/ml-13802-image001-new.png)

The second container hosts a pretrained XGboost model (i.e., predictor).
2番目のコンテナは、事前に学習されたXGboostモデル（すなわち予測器）をホストする。
The predictor model accepts the featurized input and outputs predictions.
予測モデルは特徴化された入力を受け入れ、予測を出力する。

![](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2023/09/14/ml-13802-image003.png)

Lastly, we deploy the featurizer and predictor in a serial-inference pipeline to an Amazon SageMaker real-time endpoint.
最後に、featurizerとpredictorをserial-inferenceパイプライン(serial??:thinking:)でAmazon SageMakerリアルタイムエンドポイントにデプロイする。

Here are few different considerations as to why you may want to have separate containers within your inference application.
**推論アプリケーションの中で、なぜコンテナを分けたほうがいいのか**、いくつか考えてみましょう。

- **Decoupling** – Various steps of the pipeline have a clearly defined purpose and need to be run on separate containers due to the underlying dependencies involved. This also helps keep the pipeline well structured. デカップリング - パイプラインの**様々なステップには明確に定義された目的があり**(各ステップでそれぞれ目的が異なる:thinking:)、その根底には依存関係があるため、別々のコンテナで実行する必要がある。 これはまた、パイプラインをうまく構成しておくのにも役立つ。

- **Frameworks** – Various steps of the pipeline use specific fit-for-purpose frameworks (such as scikit or Spark ML) and therefore need to be run on separate containers. フレームワーク - パイプラインの様々なステップでは、**特定の目的に合ったフレームワーク（scikitやSpark MLなど）を使用するため、別のコンテナで実行する必要がある**。

- **Resource isolation** – Various steps of the pipeline have varying resource consumption requirements and therefore need to be run on separate containers for more flexibility and control. リソースの分離 - パイプラインの**様々なステップには様々なリソース消費要件**があるため、柔軟性と制御性を高めるために別々のコンテナで実行する必要があります。(なるほど...!このステップはGPU不要/必要で、このステップはメモリ大きめのリソースで、みたいな感じか:thinking:)

- **Maintenance and upgrades** – From an operational standpoint, this promotes functional isolation and you can continue to upgrade or modify individual steps much more easily, without affecting other models. メンテナンスとアップグレード - 運用面では、**機能的な分離(functional isolation)**が促進され、他のモデルに影響を与えることなく、**個々のステップのアップグレードや変更をより簡単に**続けることができます。

Additionally, local build of the individual containers helps in the iterative process of development and testing with favorite tools and Integrated Development Environments (IDEs).
さらに、個々のコンテナのローカルビルドは、お気に入りのツールや統合開発環境(IDE)を使った開発とテストの反復プロセスに役立つ。
Once the containers are ready, you can use deploy them to the AWS cloud for inference using Amazon SageMaker endpoints.
コンテナの準備ができたら、Amazon SageMakerのエンドポイントを使用して、推論のためにAWSクラウドにデプロイすることができます。

Full implementation, including code snippets, is available in this Github repository here.
コード・スニペットを含む完全な実装は、[こちら](https://github.com/aws/amazon-sagemaker-examples/tree/main/inference/structured/realtime/byoc/byoc-nginx-python)のGithubリポジトリで入手できる。

![](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2023/09/14/ml-13802-image005.png)

## Prerequisites 前提条件

As we test these custom containers locally first, we’ll need docker desktop installed on your local computer.
これらのカスタム・コンテナをまずローカルでテストするので、ローカル・コンピューターにdocker desktopがインストールされている必要がある。
You should be familiar with building docker containers.
Dockerコンテナの構築には慣れているはずだ。

You’ll also need an AWS account with access to Amazon SageMaker, Amazon ECR and Amazon S3 to test this application end-to-end.
また、このアプリケーションをエンドツーエンドでテストするには、Amazon SageMaker、Amazon ECR、Amazon S3にアクセスできるAWSアカウントが必要です。

Ensure you have the latest version of Boto3 and the Amazon SageMaker Python packages installed:
最新バージョンのBoto3とAmazon SageMaker Pythonパッケージがインストールされていることを確認してください：

```
pip install --upgrade boto3 sagemaker scikit-learn
```

## Solution Walkthrough 解決策チュートリアル

### Build custom featurizer container カスタム・フィーチャライザー・コンテナの構築

To build the first container, the featurizer container, we train a scikit-learn model to process raw features in the abalone dataset.
最初のコンテナであるfeaturizerコンテナを構築するために、abaloneデータセットの生特徴を処理するscikit-learnモデルを学習する。
The preprocessing script uses SimpleImputer for handling missing values, StandardScaler for normalizing numerical columns, and OneHotEncoder for transforming categorical columns.
前処理スクリプトは、欠損値の処理にSimpleImputer、数値列の正規化にStandardScaler、カテゴリー列の変換にOneHotEncoderを使用しています。
After fitting the transformer, we save the model in joblib format.
トランスフォーマーをフィッティングした後、**モデルをjoblib形式で保存**します。(featurizerモデルをローカルで作っておくって事なのかな??:thinking:)
We then compress and upload this saved model artifact to an Amazon Simple Storage Service (Amazon S3) bucket.
そして、この保存されたモデル・アーティファクトを圧縮してAmazon Simple Storage Service（Amazon S3）バケットにアップロードする。

Here’s a sample code snippet that demonstrates this.
これを示すサンプル・コードです。
Refer to featurizer.ipynb for full implementation:
完全な実装は[featurizer.ipynb](https://github.com/aws/amazon-sagemaker-examples/blob/main/inference/structured/realtime/byoc/byoc-nginx-python/featurizer/featurizer.ipynb)を参照:

```python
numeric_features = list(feature_columns_names)
numeric_features.remove("sex")
numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_features = ["sex"]
categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# Call fit on ColumnTransformer to fit all transformers to X, y
preprocessor = preprocess.fit(df_train_val)

# Save the processor model to disk
joblib.dump(preprocess, os.path.join(model_dir, "preprocess.joblib"))
```

Next, to create a custom inference container for the featurizer model, we build a Docker image with nginx, gunicorn, flask packages, along with other required dependencies for the featurizer model.
次に、フィーチャライザー・モデル用のカスタム推論コンテナを作成するために、nginx、gunicorn、flaskのパッケージと、フィーチャライザー・モデルに必要なその他の依存関係を含むDockerイメージを構築します。

Nginx, gunicorn and the Flask app will serve as the model serving stack on Amazon SageMaker real-time endpoints.
Nginx、gunicorn、Flaskアプリが、Amazon SageMakerリアルタイムエンドポイントのモデルサービングスタックとして機能する。

When bringing custom containers for hosting on Amazon SageMaker, we need to ensure that the inference script performs the following tasks after being launched inside the container:
Amazon SageMakerでホスティングするためにカスタムコンテナを持ち込む場合、推論スクリプトがコンテナ内で起動した後に以下のタスクを実行するようにする必要がある:

1. Model loading: Inference script (preprocessing.py) should refer to /opt/ml/model directory to load the model in the container. Model artifacts in Amazon S3 will be downloaded and mounted onto the container at the path /opt/ml/model. モデルのロード: 推論スクリプト(preprocessing.py)はコンテナにモデルをロードするために/opt/ml/modelディレクトリを参照する必要があります。 Amazon S3にあるモデル成果物はダウンロードされ、/opt/ml/modelのパスにあるコンテナにマウントされる。

2. Environment variables: To pass custom environment variables to the container, you must specify them during the Model creation step or during Endpoint creation from a training job. 環境変数: カスタム環境変数をコンテナに渡すには、モデル作成ステップ中またはトレーニングジョブからのエンドポイント作成中に指定する必要があります。

3. API requirements: The Inference script must implement both /ping and /invocations routes as a Flask application. The /ping API is used for health checks, while the /invocations API handles inference requests. API要件:推論スクリプトは、`/ping`と`/invocations`の両方のルートをFlaskアプリケーションとして実装する必要があります。 ping APIはヘルスチェックに使用され、/invocations APIは推論リクエストを処理する。

4. Logging: Output logs in the inference script must be written to standard output (stdout) and standard error (stderr) streams. These logs are then streamed to Amazon CloudWatch by Amazon SageMaker. ロギング:推論スクリプトの出力ログは、標準出力（stdout）と標準エラー（stderr）ストリームに書き出されなければならない。 これらのログは、Amazon SageMakerによってAmazon CloudWatchにストリーミングされる。

Here’s a snippet from preprocessing.py that show the implementation of /ping and /invocations.
`/ping`と`/invocations`の実装を示すpreprocessing.pyのスニペットです。

Refer to preprocessing.py under the featurizer folder for full implementation.
完全な実装はfeaturizerフォルダの[preprocessing.py](https://github.com/aws/amazon-sagemaker-examples/blob/main/inference/structured/realtime/byoc/byoc-nginx-python/featurizer/code/preprocessing.py)を参照してください。

```python
def load_model():
    # Construct the path to the featurizer model file
    ft_model_path = os.path.join(MODEL_PATH, "preprocess.joblib")
    featurizer = None

    try:
        # Open the model file and load the featurizer using joblib
        with open(ft_model_path, "rb") as f:
            featurizer = joblib.load(f)
            print("Featurizer model loaded", flush=True)
    except FileNotFoundError:
        print(f"Error: Featurizer model file not found at {ft_model_path}", flush=True)
    except Exception as e:
        print(f"Error loading featurizer model: {e}", flush=True)

    # Return the loaded featurizer model, or None if there was an error
    return featurizer

def transform_fn(request_body, request_content_type):
    """
    Transform the request body into a usable numpy array for the model.

    This function takes the request body and content type as input, and
    returns a transformed numpy array that can be used as input for the
    prediction model.

    Parameters:
        request_body (str): The request body containing the input data.
        request_content_type (str): The content type of the request body.

    Returns:
        data (np.ndarray): Transformed input data as a numpy array.
    """
    # Define the column names for the input data
    feature_columns_names = [
        "sex",
        "length",
        "diameter",
        "height",
        "whole_weight",
        "shucked_weight",
        "viscera_weight",
        "shell_weight",
    ]
    label_column = "rings"

    # Check if the request content type is supported (text/csv)
    if request_content_type == "text/csv":
        # Load the featurizer model
        featurizer = load_model()

        # Check if the featurizer is a ColumnTransformer
        if isinstance(
            featurizer, sklearn.compose._column_transformer.ColumnTransformer
        ):
            print(f"Featurizer model loaded", flush=True)

        # Read the input data from the request body as a CSV file
        df = pd.read_csv(StringIO(request_body), header=None)

        # Assign column names based on the number of columns in the input data
        if len(df.columns) == len(feature_columns_names) + 1:
            # This is a labelled example, includes the ring label
            df.columns = feature_columns_names + [label_column]
        elif len(df.columns) == len(feature_columns_names):
            # This is an unlabelled example.
            df.columns = feature_columns_names

        # Transform the input data using the featurizer
        data = featurizer.transform(df)

        # Return the transformed data as a numpy array
        return data
    else:
        # Raise an error if the content type is unsupported
        raise ValueError("Unsupported content type: {}".format(request_content_type))


@app.route("/ping", methods=["GET"])
def ping():
    # Check if the model can be loaded, set the status accordingly
    featurizer = load_model()
    status = 200 if featurizer is not None else 500

    # Return the response with the determined status code
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def invocations():
    # Convert from JSON to dict
    print(f"Featurizer: received content type: {flask.request.content_type}")
    if flask.request.content_type == "text/csv":
        # Decode input data and transform
        input = flask.request.data.decode("utf-8")
        transformed_data = transform_fn(input, flask.request.content_type)

        # Format transformed_data into a csv string
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)

        for row in transformed_data:
            csv_writer.writerow(row)

        csv_buffer.seek(0)

        # Return the transformed data as a CSV string in the response
        return flask.Response(response=csv_buffer, status=200, mimetype="text/csv")
    else:
        print(f"Received: {flask.request.content_type}", flush=True)
        return flask.Response(
            response="Transformer: This predictor only supports CSV data",
            status=415,
            mimetype="text/plain",
        )
```

### Build Docker image with featurizer and model serving stack フィーチャライザーとモデル・サービング・スタックを備えたDockerイメージをビルドする。

Let’s now build a Dockerfile using a custom base image and install required dependencies.
カスタム・ベース・イメージを使ってDockerfileをビルドし、必要な依存関係をインストールしよう。

For this, we use python:3.9-slim-buster as the base image.
そのために、`python:3.9-slim-buster`を base image として使用する。
You can change this any other base image relevant to your use case.
このベースimageは、あなたのユースケースに関連する他のベースimageに変更することができます。

We then copy the nginx configuration, gunicorn’s web server gateway file, and the inference script to the container.
次に、nginxの設定、gunicornのウェブサーバー・ゲートウェイ・ファイル、推論スクリプトをコンテナにコピーする。
We also create a python script called serve that launches nginx and gunicorn processes in the background and sets the inference script (i.e., preprocessing.py Flask application) as the entry point for the container.
また、バックグラウンドでnginxとgunicornプロセスを起動し、推論スクリプト（つまりpreprocessing.py Flaskアプリケーション）をコンテナのエントリーポイントとして設定するserveというpythonスクリプトを作成する。

Here’s a snippet of the Dockerfile for hosting the featurizer model.
以下は、フィーチャライザー・モデルをホストするためのDockerfileのスニペットである。
For full implementation refer to Dockerfile under featurizer folder.
完全な実装については、featurizerフォルダの下の[Dockerfile](https://github.com/aws/amazon-sagemaker-examples/blob/main/inference/structured/realtime/byoc/byoc-nginx-python/featurizer/Dockerfile)を参照してください。

```docker
FROM python:3.9-slim-buster
…

# Copy requirements.txt to /opt/program folder
COPY requirements.txt /opt/program/requirements.txt

# Install packages listed in requirements.txt
RUN pip3 install --no-cache-dir -r /opt/program/requirements.txt

# Copy contents of code/ dir to /opt/program
COPY code/ /opt/program/

# Set working dir to /opt/program which has the serve and inference.py scripts
WORKDIR /opt/program

# Expose port 8080 for serving
EXPOSE 8080

ENTRYPOINT ["python"]

# serve is a python script under code/ directory that launches nginx and gunicorn processes
CMD [ "serve" ]
```

### Test custom inference image with featurizer locally カスタム推論画像をローカルでフィーチャライザーとテストする。

Now, build and test the custom inference container with featurizer locally, using Amazon SageMaker local mode.
ここで、[Amazon SageMaker のローカルモード](https://sagemaker.readthedocs.io/en/stable/overview.html#local-mode)(なにそれ??:thinking:)を使用して、featurizer を含むカスタム推論コンテナをローカルにビルドし、テストします。
Local mode is perfect for testing your processing, training, and inference scripts without launching any jobs on Amazon SageMaker.
ローカルモードは、Amazon SageMaker上でジョブを起動することなく、処理、トレーニング、推論スクリプトをテストするのに最適です。
After confirming the results of your local tests, you can easily adapt the training and inference scripts for deployment on Amazon SageMaker with minimal changes.
ローカルでのテスト結果を確認した後、最小限の変更で、Amazon SageMakerでのデプロイメント用にトレーニングスクリプトと推論スクリプトを簡単に適合させることができます。

To test the featurizer custom image locally, first build the image using the previously defined Dockerfile.
featurizerカスタム・イメージをローカルでテストするには、まず先に定義したDockerfileを使ってイメージをビルドする。
Then, launch a container by mounting the directory containing the featurizer model (preprocess.joblib) to the /opt/ml/model directory inside the container.
次に、featurizer モデル（preprocess.joblib）を含むディレクトリをコンテナ内の /opt/ml/model ディレクトリにマウントしてコンテナを起動します。
Additionally, map port 8080 from container to the host.
さらに、ポート8080をコンテナからホストにマッピングする。

Once launched, you can send inference requests to http://localhost:8080/invocations.
起動したら、http://localhost:8080/invocations に推論リクエストを送ることができる。

To build and launch the container, open a terminal and run the following commands.
コンテナをビルドして起動するには、ターミナルを開いて以下のコマンドを実行する。

Note that you should replace the <IMAGE_NAME>, as shown in the following code, with the image name of your container.
次のコードに示すように、<IMAGE_NAME>をコンテナの画像名に置き換えてください。

The following command also assumes that the trained scikit-learn model (preprocess.joblib) is present under a directory called models.
また、以下のコマンドは、学習済みの scikit-learn モデル（preprocess.joblib）が models というディレクトリの下に存在することを前提としています。

```shell
docker build -t <IMAGE_NAME> .
```

```shell
docker run –rm -v $(pwd)/models:/opt/ml/model -p 8080:8080 <IMAGE_NAME>
```

After the container is up and running, we can test both the /ping and /invocations routes using curl commands.
コンテナが稼働したら、curlコマンドを使って`/ping`ルートと`/invocations`ルートの両方をテストできる。

Run the below commands from a terminal
ターミナルから以下のコマンドを実行する。

```shell
# test /ping route on local endpoint
curl http://localhost:8080/ping

# send raw csv string to /invocations. Endpoint should return transformed data
curl --data-raw 'I,0.365,0.295,0.095,0.25,0.1075,0.0545,0.08,9.0' -H 'Content-Type: text/csv' -v http://localhost:8080/invocations
```

When raw (untransformed) data is sent to http://localhost:8080/invocations, the endpoint responds with transformed data.
生データ(変換されていないデータ)がhttp://localhost:8080/invocations に送信されると、エンドポイントは変換されたデータで応答する。

You should see response something similar to the following:
以下のような反応があるはずだ：

```shell
* Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080 (#0)
> POST /invocations HTTP/1.1
> Host: localhost: 8080
> User-Agent: curl/7.87.0
> Accept: */*
> Content -Type: text/csv
> Content -Length: 47
>
* Mark bundle as not supporting multiuse
> HTTP/1.1 200 OK
> Server: nginx/1.14.2
> Date: Sun, 09 Apr 2023 20:47:48 GMT
> Content -Type: text/csv; charset=utf-8
> Content -Length: 150
> Connection: keep -alive
-1.3317586042173168, -1.1425409076053987, -1.0579488602777858, -1.177706547272754, -1.130662184748842,
* Connection #0 to host localhost left intact
```

We now terminate the running container, and then tag and push the local custom image to a private Amazon Elastic Container Registry (Amazon ECR) repository.
次に、実行中のコンテナを終了し、ローカルのカスタムイメージにタグを付けてAmazon Elastic Container Registry（Amazon ECR）のプライベートリポジトリにプッシュします。

See the following commands to login to Amazon ECR, which tags the local image with full Amazon ECR image path and then push the image to Amazon ECR.
Amazon ECRにログインし、ローカルのイメージにAmazon ECRのフルイメージパスをタグ付けし、Amazon ECRにイメージをプッシュするには、以下のコマンドを参照してください。
Ensure you replace region and account variables to match your environment.
地域変数とアカウント変数をあなたの環境に合わせて置き換えてください。

```shell
# login to ecr with your credentials
aws ecr get-login-password - -region "${region}" |\
docker login - -username AWS - -password-stdin ${account}".dkr.ecr."${region}".amazonaws.com

# tag and push the image to private Amazon ECR
docker tag ${image} ${fullname}
docker push $ {fullname}
```

Refer to create a repository and push an image to Amazon ECR AWS Command Line Interface (AWS CLI) commands for more information.
詳細については、リポジトリの作成とAmazon ECRへのイメージのプッシュ AWS Command Line Interface (AWS CLI)コマンドを参照してください。

### Optional step 任意ステップ

Optionally, you could perform a live test by deploying the featurizer model to a real-time endpoint with the custom docker image in Amazon ECR.
オプションとして、featurizerモデルをAmazon ECRのカスタムDockerイメージでリアルタイムのエンドポイントにデプロイして、ライブテストを実行することもできます。
Refer to featurizer.ipynb notebook for full implementation of buiding, testing, and pushing the custom image to Amazon ECR.
カスタムイメージの作成、テスト、Amazon ECRへのプッシュの完全な実装については、[featurizer.ipynb](https://github.com/aws/amazon-sagemaker-examples/blob/main/inference/structured/realtime/byoc/byoc-nginx-python/featurizer/featurizer.ipynb) notebookを参照してください。

Amazon SageMaker initializes the inference endpoint and copies the model artifacts to the /opt/ml/model directory inside the container.
Amazon SageMaker は推論エンドポイントを初期化し、モデルの成果物をコンテナ内の /opt/ml/model ディレクトリにコピーします。
See How SageMaker Loads your Model artifacts.
[SageMaker がモデル成果物を読み込む方法](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-inference-code.html#your-algorithms-inference-code-load-artifacts) を参照してください。

### Build custom XGBoost predictor container カスタム XGBoost 予測コンテナの構築

For building the XGBoost inference container we follow similar steps as we did while building the image for featurizer container:
XGBoost推論コンテナの構築は、フィーチャライザー・コンテナのイメージ構築と同様の手順で行う：

1. Download pre-trained XGBoost model from Amazon S3. 学習済みのXGBoostモデルをAmazon S3からダウンロードする。

2. Create the inference.py script that loads the pretrained XGBoost model, converts the transformed input data received from featurizer, and converts to XGBoost.DMatrix format, runs predict on the booster, and returns predictions in json format. 事前に学習されたXGBoostモデルをロードし、featurizerから受け取った変換された入力データをXGBoost.DMatrix形式に変換し、booster上でpredictを実行し、予測値をjson形式で返すinference.pyスクリプトを作成します。

3. Scripts and configuration files that form the model serving stack (i.e., nginx.conf, wsgi.py, and serve remain the same and needs no modification. モデルサービングスタックを形成するスクリプトや設定ファイル（nginx.conf、wsgi.py、serveなど）はそのままで、変更の必要はありません。

4. We use Ubuntu:18.04 as the base image for the Dockerfile. This isn’t a prerequisite. We use the ubuntu base image to demonstrate that containers can be built with any base image. DockerfileのベースイメージとしてUbuntu:18.04を使用する。 これは前提条件ではない。 コンテナはどのベースイメージでも構築できることを示す為に、ubuntuのベースイメージを使用する。

5. The steps for building the customer docker image, testing the image locally, and pushing the tested image to Amazon ECR remain the same as before. 顧客のDockerイメージを構築し、ローカルでイメージをテストし、テストしたイメージをAmazon ECRにプッシュする手順は以前と同じです。

For brevity, as the steps are similar shown previously; however, we only show the changed coding in the following.
簡潔にするため、前回と同様のステップを示したが、以下では変更されたコーディングのみを示す。

First, theinference.py script.
まず、inference.pyスクリプトです。
Here’s a snippet that show the implementation of /ping and /invocations.
以下は、/pingと/invocationsの実装を示すスニペットである。
Refer to inference.py under the predictor folder for full implementation of this file.
このファイルの完全な実装はpredictorフォルダのinference.pyを参照してください。

```python
@app.route("/ping", methods=["GET"])
def ping():
    """
    Check the health of the model server by verifying if the model is loaded.

    Returns a 200 status code if the model is loaded successfully, or a 500
    status code if there is an error.

    Returns:
        flask.Response: A response object containing the status code and mimetype.
    """
    status = 200 if model is not None else 500
    return flask.Response(response="\n", status=status, mimetype="application/json")

@app.route("/invocations", methods=["POST"])
def invocations():
    """
    Handle prediction requests by preprocessing the input data, making predictions,
    and returning the predictions as a JSON object.

    This function checks if the request content type is supported (text/csv; charset=utf-8),
    and if so, decodes the input data, preprocesses it, makes predictions, and returns
    the predictions as a JSON object. If the content type is not supported, a 415 status
    code is returned.

    Returns:
        flask.Response: A response object containing the predictions, status code, and mimetype.
    """
    print(f"Predictor: received content type: {flask.request.content_type}")
    if flask.request.content_type == "text/csv; charset=utf-8":
        input = flask.request.data.decode("utf-8")
        transformed_data = preprocess(input, flask.request.content_type)
        predictions = predict(transformed_data)

        # Return the predictions as a JSON object
        return json.dumps({"result": predictions})
    else:
        print(f"Received: {flask.request.content_type}", flush=True)
        return flask.Response(
            response=f"XGBPredictor: This predictor only supports CSV data; Received: {flask.request.content_type}",
            status=415,
            mimetype="text/plain",
        )

```

Here’s a snippet of the Dockerfile for hosting the predictor model.
予測モデルをホストするためのDockerfileのスニペットを以下に示す。
For full implementation refer to Dockerfile under predictor folder.
完全な実装については、predictorフォルダの下のDockerfileを参照してください。

```docker
FROM ubuntu:18.04

…

# install required dependencies including flask, gunicorn, xgboost etc.,
RUN pip3 --no-cache-dir install  flask  gunicorn  gevent  numpy  pandas  xgboost

# Copy contents of code/ dir to /opt/program
COPY code /opt/program

# Set working dir to /opt/program which has the serve and inference.py scripts
WORKDIR /opt/program

# Expose port 8080 for serving
EXPOSE 8080

ENTRYPOINT ["python"]

# serve is a python script under code/ directory that launches nginx and gunicorn processes
CMD ["serve"]
```

We then continue to build, test, and push this custom predictor image to a private repository in Amazon ECR.
そして、このカスタム予測イメージを構築し、テストし、Amazon ECRのプライベートリポジトリにプッシュし続ける。
Refer to predictor.ipynb notebook for full implementation of building, testing and pushing the custom image to Amazon ECR.
カスタムイメージのビルド、テスト、Amazon ECRへのプッシュの完全な実装については、[predictor.ipynb](https://github.com/aws/amazon-sagemaker-examples/blob/main/inference/structured/realtime/byoc/byoc-nginx-python/predictor/predictor.ipynb) notebookを参照してください。

## Deploy serial inference pipeline シリアル推論パイプラインの導入

After we have tested both the featurizer and predictor images and have pushed them to Amazon ECR, we now upload our model artifacts to an Amazon S3 bucket.
featurizerとpredictorの両方のdocker imageをテストし、それらをAmazon ECRにプッシュした後、今度はモデルの成果物をAmazon S3バケットにアップロードします。

Then, we create two model objects: one for the featurizer (i.e., preprocess.joblib) and other for the predictor (i.e., xgboost-model) by specifying the custom image uri we built earlier.
次に、2つのモデル・オブジェクトを作成する: ひとつはフィーチャライザー用（つまりpreprocess.joblib）、もうひとつは予測モデル用（つまりxgboost-model）です。

Here’s a snippet that shows that.
それを示すスニペットがここにある。
Refer to serial-inference-pipeline.ipynb for full implementation.
完全な実装はserial-inference-pipeline.ipynbを参照のこと。

```python
suffix = f"{str(uuid4())[:5]}-{datetime.now().strftime('%d%b%Y')}"

# Featurizer Model (SKLearn Model)
image_name = "<FEATURIZER_IMAGE_NAME>"
sklearn_image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:latest"

featurizer_model_name = f""<FEATURIZER_MODEL_NAME>-{suffix}"
print(f"Creating Featurizer model: {featurizer_model_name}")
sklearn_model = Model(
    image_uri=featurizer_ecr_repo_uri,
    name=featurizer_model_name,
    model_data=featurizer_model_data,
    role=role,
)

# Full name of the ECR repository
predictor_image_name = "<PREDICTOR_IMAGE_NAME>"
predictor_ecr_repo_uri
= f"{account_id}.dkr.ecr.{region}.amazonaws.com/{predictor_image_name}:latest"

# Predictor Model (XGBoost Model)
predictor_model_name = f"""<PREDICTOR_MODEL_NAME>-{suffix}"
print(f"Creating Predictor model: {predictor_model_name}")
xgboost_model = Model(
    image_uri=predictor_ecr_repo_uri,
    name=predictor_model_name,
    model_data=predictor_model_data,
    role=role,
)
```

Now, to deploy these containers in a serial fashion, we first create a PipelineModel object and pass the featurizer model and the predictor model to a python list object in the same order.
さて、これらのコンテナをシリアルにデプロイするために、まずPipelineModelオブジェクトを作成し、featurizerモデルとpredictorモデルを同じ順番でpythonのリストオブジェクトに渡します。

Then, we call the .deploy() method on the PipelineModel specifying the instance type and instance count.
次に、インスタンスタイプとインスタンス数を指定して、PipelineModel の .deploy() メソッドを呼び出します。

```python
from sagemaker.pipeline import PipelineModel

pipeline_model_name = f"Abalone-pipeline-{suffix}"

pipeline_model = PipelineModel(
    name=pipeline_model_name,
    role=role,
    models=[sklearn_model, xgboost_model],
    sagemaker_session=sm_session,
)

print(f"Deploying pipeline model {pipeline_model_name}...")
predictor = pipeline_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.xlarge",
)
```

At this stage, Amazon SageMaker deploys the serial inference pipeline to a real-time endpoint.
この段階で、Amazon SageMakerはシリアル推論パイプラインをリアルタイムエンドポイントにデプロイする。
We wait for the endpoint to be InService.
エンドポイントがInServiceになるのを待つ。

We can now test the endpoint by sending some inference requests to this live endpoint.
このライブエンドポイントに推論リクエストを送ることで、エンドポイントをテストすることができる。

Refer to serial-inference-pipeline.ipynb for full implementation.
完全な実装はserial-inference-pipeline.ipynbを参照のこと。

## Clean up クリーンアップ

After you are done testing, please follow the instructions in the cleanup section of the notebook to delete the resources provisioned in this post to avoid unnecessary charges.
テストが終わったら、この投稿でプロビジョニングされたリソースを削除するために、ノートブックのクリーンアップセクションの指示に従ってください。
Refer to Amazon SageMaker Pricing for details on the cost of the inference instances.
推論インスタンスのコストの詳細については、Amazon SageMakerの価格を参照してください。

```python
# Delete endpoint, model
try:
    print(f"Deleting model: {pipeline_model_name}")
    predictor.delete_model()
except Exception as e:
    print(f"Error deleting model: {pipeline_model_name}\n{e}")
    pass

try:
    print(f"Deleting endpoint: {endpoint_name}")
    predictor.delete_endpoint()
except Exception as e:
    print(f"Error deleting EP: {endpoint_name}\n{e}")
    pass

```

## Conclusion 結論

In this post, I showed how we can build and deploy a serial ML inference application using custom inference containers to real-time endpoints on Amazon SageMaker.
この投稿では、カスタム推論コンテナを使用して、Amazon SageMaker上のリアルタイムエンドポイントにシリアルML推論アプリケーションを構築してデプロイする方法を紹介した。

This solution demonstrates how customers can bring their own custom containers for hosting on Amazon SageMaker in a cost-efficient manner.
このソリューションは、顧客がAmazon SageMaker上でホスティングするための独自のカスタムコンテナを、コスト効率の高い方法でどのように持ち込むことができるかを示している。
With BYOC option, customers can quickly build and adapt their ML applications to be deployed on to Amazon SageMaker.
BYOCオプションにより、顧客はAmazon SageMakerにデプロイするMLアプリケーションを素早く構築し、適応させることができる。

We encourage you to try this solution with a dataset relevant to your business Key Performance Indicators (KPIs).
お客様のビジネスの重要業績評価指標（KPI）に関連するデータセットで、このソリューションをお試しください。
You can refer to the entire solution in this GitHub repository.
このGitHubリポジトリでソリューション全体を参照できる。

Referencess

参考文献

Model hosting patterns in Amazon SageMaker
[Amazon SageMakerのモデルホスティングパターン](https://aws.amazon.com/blogs/machine-learning/part-4-model-hosting-patterns-in-amazon-sagemaker-design-patterns-for-serial-inference-on-amazon-sagemaker/)

[Amazon SageMaker Bring your own containers](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-byoc-containers.html)
Amazon SageMaker 自分のコンテナを持ち込む

[Hosting models as serial inference pipeline on Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-pipelines.html)
Amazon SageMakerでモデルをシリアル推論パイプラインとしてホストする
