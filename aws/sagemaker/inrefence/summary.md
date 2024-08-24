## 0.1. refs:

- [既存のPyTorchモデルをAmazon SageMakerのリアルタイム推論エンドポイントにデプロイする](https://qiita.com/thruaxle/items/8339d70de0548f00460f)
- [Amazon SageMaker におけるカスタムコンテナ実装パターン詳説 〜推論編〜](https://aws.amazon.com/jp/blogs/news/sagemaker-custom-containers-pattern-inference/)
- [Amazon SageMaker 推論 Part 3 もう悩まない︕機械学習モデルのデプロイパターンと戦略](https://pages.awscloud.com/rs/112-TZM-766/images/AWS-Black-Belt_2022_Amazon-SageMaker-Inference-Part-3_1014_v1.pdf)
- [Amazon SageMaker 推論 Part2 すぐにプロダクション利用できる！ モデルをデプロイして推論する方法](https://d1.awsstatic.com/webinars/jp/pdf/services/202208_AWS_Black_Belt_AWS_AIML_Dark_04_inference_part2.pdf)
- 柏木さんのブログ! これは自前コンテナでSagemakerエンドポイントを作ってる例: [SageMakerとStep Functionsを用いた機械学習パイプラインで構築した検閲システム（後編）](https://tech.connehito.com/entry/2022/03/28/190436)
- CyberAgentの長江さんのSagemakerエンドポイントの高速化のtips: [SageMaker Endpointのレイテンシー高速化実験](https://nsakki55.hatenablog.com/entry/2023/01/07/134201)

# 1. Sagemaker 推論エンドポイント:

## 1.1. なにそれ?

- Sagemaker:
  - MLモデルの学習や推論に必要な環境の構築を、専用のコンピューティング環境(Sagemaker MLインスタンス上で稼働するコンテナ)上でフルマネージドに行うことができる。
- Sagemakerでホストできる推論環境の選択肢は4種類:
  - 1. リアルタイム推論エンドポイント
  - 2. サーバレス推論エンドポイント
  - 3. 非同期推論
  - 4. バッチ推論
- リアルタイム推論エンドポイントは、低レイテンシーまたは高スループットが要求されるオンライン推論に適したオプション。
  - 参考: [推論オプション](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/deploy-model.html#deploy-model-options)

## 1.2. リアルタイム推論エンドポイントについて:

- 低レイテンシーや高スループットが要求されるオンライン推論に最適。
- 選択したインスタンスタイプに基づいて、持続的なtrafficを処理できる、**永続的でフルマネージド方のendpoint(REST API)**として使用できる。
- 最大6MBのペイロードサイズと、60秒の処理時間のワークロードに対応する。
  - payload: 推論リクエストに含まれるデータのこと。
  - workload: 推論リクエストを処理するために必要な計算のこと。
- **外部アプリケーションからアクセス可能**。
- 自動スケーリングが可能。

図を見た感じでは、外部からのリクエストをまず HTTPS Endpointが受けとり、それがElastic Load Balancerを経由して、Sagemaker エンドポイントのML instances (Auto Scaling Group)に送られるぽい。

## 1.3. リアルタイプ推論エンドポイントのデプロイ手順:

以下は、ざっくりリアルタイム推論エンドポイントに必要なもの達。

- 1. 学習済みモデルのデータや推論コードをpackagingした概念である **Model Artifact** をS上に用意する。(model.tar.gzの形式のやつ...!:thinking:)
  - Boto3だとマニュアルでS3上にmodel artifactを用意しておく必要があるみたい。Sagemaker Python SDKの場合は、ローカルストレージ上の`source_dir`と`entry_point`を指定して、model artifactを作成できるらしい...!(ここは、batch jobサービスと同様:thinking:)
- 2. エンドポイントのデプロイ時にmodel artifactやdocker imageにアクセスする為のIAMロールを用意する。
  - このIAM roleは、model artifactと一緒に model としてpackagingされる。
- 3. 推論に必要な情報をpackagingした概念である **Model** を用意する。
  - モデルの推論環境を定義したもの。
  - 中身:
    - 推論コンテナimage(のURI)
    - model artifact (のS3 URI)
    - IAM Role (のARN)
    - 追加設定(optional)
      - ex. VPC 設定, multi-model deploy, multi-container deploy, etc.
  - (Model packageもほぼ同じ概念??:thinking:)
  - (batch transformの場合は、手順3まででOKになる。modelを用意したあとで`create_transform_job`を起動する感じ...!:thinking:)
- 4. エンドポイントの稼働に必要な情報を定義した Sagemaker Endpoint Configuration を用意する。
  - 手順3で定義したモデルを動かすための、computing resourcesの指定。
  - ex. インスタンスタイプ, インスタンス数, etc.
  - サーバレス推論の場合は、ここの設定だけが推論エンドポイントと異なるみたい! `ServerlessConfig`を追加する感じ...!:thinking:
- 5. Sagemaker エンドポイントを作成する。
  - 手順3で定義したモデルを、手順4で定義したcomputing resourcesで動かし、リクエストを受け取ったら推論結果を返すようにする。

## 1.4. リアルタイム推論エンドポイントがmodel artifactをどう使うのか:

- model artifact:
  - 具体的には、Sagemakerエンドポイントでモデルをホストするために、**Sagemakerの利用者が準備する必要のあるファイル一式を格納した圧縮ファイルのこと**。
  - 基本的には、学習済みモデルのデータと、推論コード、requirements.txtなどのファイルを含む。
- Sagemakerでは、このmodel artifactをS3に置いて、そのURLを指定して推論エンドポイントをデプロイする。

以下は、model artifact(model.tar.gz)の例:

```
model.tar.gz
├── model.pth # 学習済みモデルの重みパラメータ
├── code
│   ├── inference.py # 推論コード
│   └── requirements.txt # 追加したいライブラリのリスト
└── vocab.pth # その他のモデルに必要なファイル
```

- ざっくりmodel artifactの使われ方:
  - まず、model artifactとその実行環境(コンテナimage)をまとめた概念として、Sagemaker Modelが定義される。
  - その後、Sagemaker Endpoint Configurationが定義される。
  - これらを使ってSagemaker Endpointが起動する。起動の流れは以下;
    - まずインスタンス上でDockerコンテナが起動する。
    - モデル・推論スクリプトがダウンロードされる。
    - 依存関係のあるライブラリがインストールされる。
    - 推論スクリプトが実行される。(デプロイ直後の初回実行っぽい??)

## 1.5. 推論スクリプト `inference.py` の書き方のお作法

(お作法に従わない場合は、`inference.py`側でflaskとかFastAPIとか使って、自前でエンドポイントを定義したりする感じっぽい...!:thinking:)

- 参考:

  - https://d1.awsstatic.com/webinars/jp/pdf/services/202208_AWS_Black_Belt_AWS_AIML_Dark_04_inference_part2.pdf の9ページ目～

- モデルファイルを読み込んで推論するためのPythonファイルとして `inference.py` をmodel artifact内に用意する必要がある。
- `inference.py`には、以下の4つの関数を必ず定義する必要がある。
  - `model_fn()`: model artifactに含めた、学習済みモデルを読み込む関数。
    - 第一引数が、model artifatを展開したディレクトリ名が入る。
    - 第二引数が追加情報(optional)。
  - `input_fn()`: クライアントからのリクエストデータを取得し、推論で利用可能な形式に変換する関数。
    - 第一引数: リクエストデータのボディ。
    - 第二引数: リクエストデータのContent-Type。(i.e. MIMEタイプ)
      - (REST APIの `ContentType` headerで指定されるやつ..!:thinking:)
    - 第三引数: 追加情報(optional)。
    - (任意の前処理を実装できる...!:thinking:)
  - `predict_fn()`: 推論ロジックを実行する関数。
    - 第一引数: `input_fn()`でreturnされたオブジェクト。
    - 第二引数: `model_fn()`でreturnされたオブジェクト。
    - 第三引数: 追加情報(optional)。
  - `output_fn()`: 推論結果をクライアントに返す形式に変換する関数。
    - 第一引数: `predict_fn()`でreturnされたオブジェクト。
    - 第二引数: レスポンスデータのContent-Type。(i.e. MIMEタイプ):
      - (REST APIの `Accept` headerで指定されるやつ..!:thinking:)
    - 第三引数: 追加情報(optional)。
    - (任意の後処理を実装できる...!:thinking:)
- 4つの必須関数の実行タイミング:
  - 推論エンドポイントをデプロイ後の初回の推論リクエスト処理時のみ、`model_fn()` → `input_fn()` → `predict_fn()` → `output_fn()` の順で実行される。
    - あ、じゃあデプロイ直後に、空リクエストを投げておかないと、コールドスタートになっちゃう??
  - 2回目以降のリクエストでは、`input_fn()` → `predict_fn()` → `output_fn()` の順で実行される。

# 2. 推論エンドポイントのコスト最適化のtips:

## 2.1. 複数のモデルをデプロイする場合のコスト最適化:

### 2.1.1. Multi-Models Endpoint:

- ざっくり雰囲気的な理解:
  - **単一のML instanceの1コンテナ内に複数のモデル(i.e. 複数のmodel artifact)をhostすることができる機能**っぽい。
    - **モデルの数だけ推論エンドポイントを稼働させておくよりも、コスト最適化ができる**。
    - query parameterなどで、どのモデル (i.e. どのmodel artifact) を使うか指定するようなイメージ。(ex. `TargetModel='model-008.tar.gz'`)

### 2.1.2. Multi-Containers Endpoint:

- ざっくり雰囲気的な理解:
  - 単一のML instanceに複数のコンテナをhostすることができる機能。最大15コンテナまで。
  - 個々の呼び出しもできるし、pipeline的な呼び出しもできる。
  - multi-models endpointと違い、コールドスタートはない。
    - (え、逆にmulti-models endpointはコールドスタートあるの??じゃあ使いづらくない??:thinking:)
    - んーでもなんか、次のページにはコールドスタートなさそうな事が書いてる。
      - (https://pages.awscloud.com/rs/112-TZM-766/images/AWS-Black-Belt_2022_Amazon-SageMaker-Inference-Part-3_1014_v1.pdf の35ページ目とか)

## 2.2. デプロイパターンと戦略:

- まずリアルタイム推論が必要か否か。
  - いいえ(一日ごと、1時間ごと、１週間毎、一ヶ月ごとなど)の場合 -> Sagemaker Batch Transform。
- hogehoge

# 3. 安全なデプロイのために:

- 参考:
  - https://pages.awscloud.com/rs/112-TZM-766/images/AWS-Black-Belt_2022_Amazon-SageMaker-Inference-Part-3_1014_v1.pdf の36ページ目とか

# 4. リアルタイム推論のエンドポイントを試しに立ててみたメモ:
- 以下資料のパターン2を採用して、推論エンドポイントを立てることができた:
  - [Amazon SageMaker におけるカスタムコンテナ実装パターン詳説 〜推論編〜](https://aws.amazon.com/jp/blogs/news/sagemaker-custom-containers-pattern-inference/) 

最終的には、以下のようにリクエスト可能なエンドポイントをhostすることができた。

```python
import json

request_body = {"user_id": "114521", "k": 3}
content_type = "application/json"
responce = predictor.predict(json.dumps(request_body), initial_args={"ContentType": content_type})

print(json.loads(responce))

>>> {'user_id': '114521', 'recommendations': [{'1887': 12.380890434982271}, {'2266': 11.636938986300727}, {'1904': 11.24494711613486}]}
```

ざっくり、以下の手順で実現できた:

##  4.1. ECRリポジトリを用意(endpoint内でrunさせるdocker imageを格納するため)
  - (気づき)AWS提供のコンテナを使うよりも、結局のところ自前のimageを使う方が楽だった!
    - aws提供のコンテナは結局いろいろお作法があったので...!(pytorchの推論用イメージの場合は、`.pth`ファイルがないとエラーが出る、など)

```shell
AWS_PROFILE={特定のprofile} aws ecr create-repository --repository-name {リポジトリ名}
```

## 4.2. Dockerfileとentrypointのファイル `serve.py` を用意する

  - 学習済みモデルは、imageの中に入れない。
  - 推論の実際の中身の処理のコードも、imageの中に入れない。
  - **コンテナに入れるのは、依存関係のpackageと、`serve.py`のみ**。 
    - `serve.py`は、Sagemaker inference toolkit (`sagemaker-inference`)を使って、推論エンドポイントを立ち上げるためのファイル。(NginxとGunicornを起動するのかな??:thinking:)
    - **`sagemaker-inference`と`multi-model-server`を依存関係パッケージに含める点に注意!**(カスタムコンテナ戦略に確か書いてあった方法...!:thinking:)
      - MMS(`multi-model-server`): 
        - OSSのモデルサービングのライブラリ。
        - Sagemakerに限らず、オンプレミスやECS上などの様々なプラットフォーム上で動作する。
        - MMSはAWSが中心で開発してるライブラリだが、MMS自体にはSagemakerとの連携機能はないため、sagemaker inference toolkit (`sagemaker-inference`)が必要になる。
      - Sagemaker inference toolkit (`sagemaker-inference`):
        - **MMS専用のSagemaker連携用ライブラリ**。(そうなのか...!:thinking:)
        - Sagemaker Endpointのコンテナ内で利用可能。

ディレクトリ構造は以下:

```shell
.
├── Dockerfile
└── realtime_inference_endpoint
    └── serve.py
```

Dockefileの中身は以下(ライブラリのinstallと、entrypointの設定のみ):

```Dockerfile
FROM python:3.10-slim

# working directoryを設定(デフォルトは/usr/src/app)
WORKDIR /usr/src/app 

# パッケージのインストール
## sagemaker-inferenceを使用することで、いい感じに環境を構築してくれる
RUN apt-get update && apt-get upgrade -y && apt-get install -y openjdk-17-jdk-headless
RUN pip install --no-cache-dir numpy multi-model-server sagemaker-inference pydantic pandas

# 推論用のスクリプトをコピー
COPY realtime_inference_endpoint/serve.py /usr/src/app/serve.py

# entrypointを設定
ENTRYPOINT ["python", "/usr/src/app/serve.py"]
```

serve.pyの中身は非常にシンプル:
(エンドポイントを自由に決めたり、複数のモデルをhostするための設定をする場合は、このファイルをいじる必要がありそうなんだろうか...??:thinking:)

```python
from sagemaker_inference import model_server

model_server.start_model_server()
```

## 4.3. 4.3 Docker imageをbuildして、ECRリポジトリにpushする

```python
import os
import boto3

ecr_repository_name = "{リポジトリ名}"
account_id = "{アカウントID}"
aws_profile = "{特定のprofile}"
region = boto3.session.Session(profile_name=aws_profile).region_name
tag = "latest"
image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{ecr_repository_name}:{tag}"

# ECRにログイン
os.system(f"AWS_PROFILE={aws_profile} aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com")

# docker imageをbuild
os.system(f"docker buildx build --platform linux/amd64 -t {ecr_repository_name} -f realtime_inference_endpoint/Dockerfile .")

# tagを付けてpush
os.system(f"docker tag {ecr_repository_name} {image_uri}")
os.system(f"docker push {image_uri}")
```

## 4.4. 4.4 なんらかの方法で model artifact　(学習済みモデルのデータを`model.tar.gz`にまとめたもの) をS3にアップロードしておく。
  - (今回は、ローカル環境にベクトルデータを落としてきておいた。それらをまとめて`model.tar.gz`にしてS3にアップロードした)
  - (推論用のコードは含めない点に注意! まあ含めても問題ないのかもしれないが...!:thinking:)

事前に、以下のようなディレクトリ構造にしておいた:

```shell
.
└── realtime_inference_endpoint
    └── model_artifact
        ├── movie_vectors
        │   └── 000.gz
        └── user_vectors
            └── 000.gz
```

学習済みのベクトルデータをまとめて`model.tar.gz`にしてS3にアップロードする関数を以下のように作成し、実行した:

```python
import boto3
import tarfile

from pathlib import Path

def prepare_model_artifact(
    model_artifact_dir_path: Path,
    model_artifact_s3uri: str,
) -> str:
    """ローカル環境のmodel artifact directoryを指定し、model.tar.gzとしてS3にuploadする"""
    tar_path = model_artifact_dir_path.parent / "model.tar.gz"

    # model.tar.gzファイルを作成
    with tarfile.open(tar_path, mode="w:gz") as tar:
        # directory内のファイルを順番にtarに追加
        for file_path in model_artifact_dir_path.iterdir():
            tar.add(file_path, arcname=file_path.name)

    # S3にアップロード
    session = boto3.Session(profile_name=PROFILE_NAME)
    s3 = session.client("s3")
    bucket_name, key = model_artifact_s3uri.replace("s3://", "").split("/", 1)
    s3.upload_file(str(tar_path), bucket_name, key)

    # localのmodel.tar.gzファイルを削除
    tar_path.unlink()
    return model_artifact_s3uri

model_artifact_dir_path = Path("./realtime_inference_endpoint/model_artifact")
model_artifact_s3uri = f"s3://my-bucket/my-key-prefix/model.tar.gz"
prepare_model_artifact(model_artifact_dir_path, model_artifact_s3uri)
```

## 4.5. 4.5 推論コードの中身を作成する
  - Sagemaker推論endpointのお作法に従った4つの関数を持つ`inference.py`と、その他のモジュールたちを用意した。
    - 4つの関数を上書きするようなお作法
      - 初回実行時に呼ばれる処理: model_fn -> input_fn -> predict_fn -> output_fn
      - リクエストを受けて呼ばれる処理: input_fn -> predict_fn -> output_fn

ディレクトリ構造は以下:

```shell
.
└── realtime_inference_endpoint
    └── code
        ├── inference.py
        ├── loader.py
        ├── models.py
        ├── type_aliases.py
        └── recommender.py
```

inference.pyの中身は以下:

```python
# sagemaker推論endpointの推論コード
# 4つの必須関数を実装する必要がある
# 初回実行時に呼ばれる処理: model_fn -> input_fn -> predict_fn -> output_fn
# リクエストを受けて呼ばれる処理: input_fn -> predict_fn -> output_fn
from pathlib import Path
from recommender import Recommender
from loader import load_vectors_csv
from models import Request, Responce
from type_aliases import UserId, ContentId, PreferenceScore


def model_fn(model_dir: str):
    """Sagemaker推論エンドポイントの推論コードの必須関数1
    - 初回実行時に呼ばれる。
    - 学習済みモデルをロードして返す。
    """
    model_dir_path = Path(model_dir)
    return Recommender(
        user_vectors=load_vectors_csv(model_dir_path / "user_vectors", "user_id"),
        movie_vectors=load_vectors_csv(model_dir_path / "movie_vectors", "movie_id"),
    )


def input_fn(request_body: str, request_content_type: str):
    if request_content_type != "application/json":
        raise ValueError(
            f"Invalid content-type: {request_content_type} (expected: application/json)"
        )
    return Request.model_validate_json(request_body)


def predict_fn(
    input_data: Request, model: Recommender
) -> tuple[UserId, list[tuple[ContentId, PreferenceScore]]]:
    return input_data.user_id, model.predict_ver1(input_data.user_id, input_data.k)


def output_fn(
    prediction: tuple[UserId, list[tuple[ContentId, PreferenceScore]]],
    response_content_type: str,
) -> str:
    if response_content_type != "application/json":
        raise ValueError(
            f"Invalid content-type: {response_content_type} (expected: application/json)"
        )

    user_id, recommendations = prediction
    return Responce(user_id=user_id, recommendations=recommendations).model_dump_json()
```

ちなみに、APIのrequestとresponseのデータ構造は、DbC(Design by Contract)的にPydanticを使って定義 & Validationしてみた!

```python
from pydantic import BaseModel, field_validator
from type_aliases import ContentId, PreferenceScore, UserId


class Request(BaseModel):
    user_id: UserId
    k: int


class Responce(BaseModel):
    user_id: UserId
    recommendations: list[dict[ContentId, PreferenceScore]]

    @field_validator("recommendations", pre=True, each_item=True)
    def parse_recommendations(
        cls,
        target: any,
    ) -> dict[ContentId, PreferenceScore]:
        """pydanticのカスタムvalidate & parse メソッドを追加。
        recommendations fieldにて、tuple[ContentId, PreferenceScore]を許容してdict[ContentId, PreferenceScore]にparseする。
        """
        if isinstance(target, tuple) and len(target) == 2:
            content_id, preference_score = target
            if isinstance(content_id, str) and isinstance(
                preference_score, (float, int)
            ):
                return {content_id: preference_score}
        raise ValueError(
            "Invalid recommendation format. Expected a tuple of (ContentId, PreferenceScore)."
        )
```

## 4.6. 4.6 Sagemaker Model, Endpoint Configuration, Endpointを作成する
  - model artifactのS3 URIと、docker imageのURIを指定する必要がある。
  - sagemaker python SDKだと結構短く書ける印象。(endpoint configurationの存在を意識せずに済んでしまう...!:thinking:)
  - boto3だと、ローカル環境の推論コードを`source_dir`と`entry_point`として指定してデプロイ、みたいなことはできずに、手動でS3に`source.tar.gz`としてアップロードする必要はありそう...!:thinking:

```python
import sagemaker

session = boto3.Session(profile_name=PROFILE_NAME)
sagemaker_session = sagemaker.Session(boto_session=session)
model_artifact_s3uri = "s3://my-bucket/my-key-prefix/model.tar.gz"

model = sagemaker.Model(
    image_uri=image_uri,
    model_data=model_artifact_s3uri,
    role=ROLE_FOR_ENDPOINT,
    entry_point="inference.py",
    source_dir="./realtime_inference_endpoint/code",
    predictor_cls=sagemaker.predictor.Predictor,
    sagemaker_session=sagemaker_session,
)

predictor = model.deploy(
    instance_type="ml.m5.xlarge",
    initial_instance_count=1,
    endpoint_name="realtime-inference-endpoint",
    wait=True,
)
```

## 4.7 最後に、Sagemaker Ruitimeを使って実際にエンドポイントにリクエストを投げてみる

- ちなみにSagemaker Runtimeって??:thinking:
  - **SageMakerエンドポイントとのインターフェースを提供するサービス**。Saegmaker RuntimeのAPIを介して、SageMakerエンドポイントの機能を使える。
  - SageMakerエンドポイントは、モデルをホストするための実体（インフラストラクチャとスケーリング機能を含む）。Sagemaker Runtimeは、エンドポイントにリクエストを送信するためのAPIを提供するサービス。

```python
import json

request_body = {"user_id": "114521", "k": 3}
content_type = "application/json"

# predictorインスタンスはなんらか作っておく必要はある
responce = predictor.predict(
    json.dumps(request_body), initial_args={"ContentType": content_type}
)

print(json.loads(responce))
{'user_id': '114521', 'recommendations': [{'1887': 12.380890434982271}, {'2266': 11.636938986300727}, {'1904': 11.24494711613486}]}

# 試せたので、エンドポイントを削除
predictor.delete_endpoint()
```

## API Gatewayと連携して、Web APIとして公開する

# 5. ざっくり思ったこと

- Sagemaker推論エンドポイントを使うメリットの1つって、GunicornとかNginxとかの設定をせずに抽象化してSagemaker側に任せられることかもって思った。(自動スケーリングとかLoad BalancerとかもSagemaker側でやってくれるっぽい??)
