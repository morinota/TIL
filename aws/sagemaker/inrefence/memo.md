## refs:

- [既存のPyTorchモデルをAmazon SageMakerのリアルタイム推論エンドポイントにデプロイする](https://qiita.com/thruaxle/items/8339d70de0548f00460f)
- [Amazon SageMaker におけるカスタムコンテナ実装パターン詳説 〜推論編〜](https://aws.amazon.com/jp/blogs/news/sagemaker-custom-containers-pattern-inference/)
- [Amazon SageMaker 推論 Part 3 もう悩まない︕機械学習モデルのデプロイパターンと戦略](https://pages.awscloud.com/rs/112-TZM-766/images/AWS-Black-Belt_2022_Amazon-SageMaker-Inference-Part-3_1014_v1.pdf)
- [Amazon SageMaker 推論 Part2 すぐにプロダクション利用できる！ モデルをデプロイして推論する方法](https://d1.awsstatic.com/webinars/jp/pdf/services/202208_AWS_Black_Belt_AWS_AIML_Dark_04_inference_part2.pdf)

# Sagemaker 推論エンドポイント:

## なにそれ?

- Sagemaker:
  - MLモデルの学習や推論に必要な環境の構築を、専用のコンピューティング環境(Sagemaker MLインスタンス上で稼働するコンテナ)上でフルマネージドに行うことができる。
- Sagemakerでホストできる推論環境の選択肢は4種類:
  - 1. リアルタイム推論エンドポイント
  - 2. サーバレス推論エンドポイント
  - 3. 非同期推論
  - 4. バッチ推論
- リアルタイム推論エンドポイントは、低レイテンシーまたは高スループットが要求されるオンライン推論に適したオプション。
  - 参考: [推論オプション](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/deploy-model.html#deploy-model-options)

## リアルタイム推論エンドポイントについて:

- 低レイテンシーや高スループットが要求されるオンライン推論に最適。
- 選択したインスタンスタイプに基づいて、持続的なtrafficを処理できる、**永続的でフルマネージド方のendpoint(REST API)**として使用できる。
- 最大6MBのペイロードサイズと、60秒の処理時間のワークロードに対応する。
  - payload: 推論リクエストに含まれるデータのこと。
  - workload: 推論リクエストを処理するために必要な計算のこと。
- **外部アプリケーションからアクセス可能**。
- 自動スケーリングが可能。

図を見た感じでは、外部からのリクエストをまず HTTPS Endpointが受けとり、それがElastic Load Balancerを経由して、Sagemaker エンドポイントのML instances (Auto Scaling Group)に送られるぽい。

## リアルタイプ推論エンドポイントのデプロイ手順:

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

## リアルタイム推論エンドポイントがmodel artifactをどう使うのか:

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

## 推論スクリプト `inference.py` の書き方のお作法

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

# 推論エンドポイントのコスト最適化のtips:

## 複数のモデルをデプロイする場合のコスト最適化:

### Multi-Models Endpoint:

- ざっくり雰囲気的な理解:
  - **単一のML instanceの1コンテナ内に複数のモデル(i.e. 複数のmodel artifact)をhostすることができる機能**っぽい。
    - **モデルの数だけ推論エンドポイントを稼働させておくよりも、コスト最適化ができる**。
    - query parameterなどで、どのモデル (i.e. どのmodel artifact) を使うか指定するようなイメージ。(ex. `TargetModel='model-008.tar.gz'`)

### Multi-Containers Endpoint:

- ざっくり雰囲気的な理解:
  - 単一のML instanceに複数のコンテナをhostすることができる機能。最大15コンテナまで。
  - 個々の呼び出しもできるし、pipeline的な呼び出しもできる。
  - multi-models endpointと違い、コールドスタートはない。
    - (え、逆にmulti-models endpointはコールドスタートあるの??じゃあ使いづらくない??:thinking:)
    - んーでもなんか、次のページにはコールドスタートなさそうな事が書いてる。
      - (https://pages.awscloud.com/rs/112-TZM-766/images/AWS-Black-Belt_2022_Amazon-SageMaker-Inference-Part-3_1014_v1.pdf の35ページ目とか)

## デプロイパターンと戦略:

- まずリアルタイム推論が必要か否か。
  - いいえ(一日ごと、1時間ごと、１週間毎、一ヶ月ごとなど)の場合 -> Sagemaker Batch Transform。
- hogehoge

# 安全なデプロイのために:

- 参考:
  - https://pages.awscloud.com/rs/112-TZM-766/images/AWS-Black-Belt_2022_Amazon-SageMaker-Inference-Part-3_1014_v1.pdf の36ページ目とか
