# refs:

- [Create a Model Package Resource](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-mkt-create-model-package.html)
- [Sagemaker Python SDK の Modelクラスのref](https://sagemaker.readthedocs.io/en/stable/api/inference/model.html)

# Model Artifact, Model Resource, Model Packageとは??

(単にModel Packageとも呼ぶ事が多そう...!)

## model package resourceってどんな概念? model artifactやmodel resourceとの違いは?

- model artifactとは?
  - 学習プロセスの結果として生成されるMLモデルのファイルやデータ(ex. `model.tar.gz`)
  - TrainingJobの成果物。
  - ざっくり「モデルそのもの」
- model resourceとは?
  - モデルをSagemaker上で**推論用(ex. batch推論ジョブや推論エンドポイント)にデプロイするために必要**な、model artifact + メタデータ + 設定を含む概念。
  - ざっくり「モデルそのもの」+「それを動かす為の情報」
  - 例えば、以下の情報を含む:
    - モデルを動かす為の権限を持つIAM role。
    - モデルを動かす為のコンテナイメージ。(推論時に実行されるコードを含む...!)
    - モデルの入出力データ形式。
- model packageとは?
  - model artifactに加えてメタデータやその他の情報をカプセル化したもの。
  - これにより、モデルのバージョン管理や承認、デプロイメントが容易になる。
  - **ざっくり「モデルそのもの」+「それを動かす為の情報」+「それを管理するための情報」**
  - 例えば、以下の情報を含む:
    - model artifact(の場所??)
    - モデルのバージョン
    - 作成日時
    - 学習に使用したデータセットに関する情報
    - モデルの評価指標
    - 使用されたアルゴリズム名
    - ハイパーパラメータ設定
    - model packageがサポートするinstance type
  - model packageはなんのために必要?
    - MLモデルのバージョン管理
    - モデルのデプロイメント
    - AWS Marketplaceでの公開

# Model Resourceの定義の話

- model resourceは、モデルをSagemaker上で**推論用(ex. batch推論ジョブや推論エンドポイント)にデプロイするために必要**な、model artifact + メタデータ + 設定を含む概念。

- Sagemaker Python SDKの場合は、`sagemaer.model.Model`クラスを使ってmodel resourceを定義する。
  - `create()`メソッドを使って、model resource(i.e. Sagemaker Model entity)を作成する。
  - `register`メソッドを使って、model packageを作成する。(モデルレジストリやAWS Marketplaceへの登録に必要)

## Model resourceの定義の為の情報:

- `image_uri`: モデルを動かす為のコンテナイメージ。(推論時に実行されるコードを含む...!)
- `model_data`: model artifactの場所。(S3の場所)
- `role`: モデルを動かす為の権限を持つIAM role。
  - S3上の学習or推論データとmodel artifactにアクセスするために、このroleを使用する。
  - 推論コード内でAWSリソースにアクセスする必要がある場合、このroleにアクション権限を追加しておく必要がある。
- `name`: model resourceの名前。
- `sagemaker_session`: Sagemakerのセッション情報。
- `source_dir`: モデルコードのディレクトリ。(Dockerfileやモデルコードを含む)
  - 絶対パスor相対パス、またはS3URIを指定する。
  - 実行されるimageの中に、source_dir内のファイルがコピーされる。指定したディレクトリ内の構造は、イメージ内で保持される。
  - ちなみに、もし`git_config`が指定されている場合、本引数はgitリポジトリ内のrootからの相対パスを指定する必要がある。
- `code_location`:
  - custom code(=`source_dir`内のコード)をuploadするS3URI。
  - 指定されない場合、S3URIは自動的に生成される。
- `entry_point`:
  - model hosting時に実行されるエントリーポイントとして実行されるPythonソースファイルのパス。
  - `source_dir`が指定されてる場合は、`source_dir`内の相対パスを指定する必要がある。
- `git_config`:
  - model resourceに含めたい推論コードのソースがgitリポジトリ上にある場合、本引数を指定する。(github上のコードも指定できるのか...!:thinking:)
  - `repo`: gitリポジトリのURL
  - `branch`: gitリポジトリのブランチ名
  - `commit`: gitリポジトリのコミットID
- `container_log_level`:
  - コンテナのログレベル。(デフォルトは`logging.INFO`)
  - 有効な値はloggingモジュールで定義されてるもの。
- `dependencies`:
  - コンテナにexportすべき追加ライブラリを定義したパス
  - 例: `['requirements.txt', 'my_module.py']`
