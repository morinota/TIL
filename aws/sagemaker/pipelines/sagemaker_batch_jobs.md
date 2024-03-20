## refs

- [sagemaker Python SDKの公式ドキュメント](https://sagemaker.readthedocs.io/en/stable/overview.html)
- [Amazon Sagemakerにおけるのカスタムコンテナ実装パターン3つ](https://aws.amazon.com/jp/blogs/news/sagemaker-custom-containers-pattern-training/)

## batchジョブの実行環境で使える環境変数の意味メモ:

- 参考: [Sagemaker Containerの利用可能な環境変数リスト](https://github.com/aws/sagemaker-containers?tab=readme-ov-file#important-environment-variables)

以下の様な様々な環境変数を通じて、実行環境に関する有用なpropertyにアクセスできる。

- `SM_MODEL_DIR`:
  - ジョブが成果物を保存するディレクトリパス。学習語、このディレクトリ以下の成果物はS3にuploadされる。
  - `SM_MODEL_DIR=/opt/ml/model`
- `SM_CHANNELS`:
  - ジョブの入力チャンネル名のリスト。
  - ex.) `SM_CHANNELS='["testing","training"]'`
- `SM_CHANNEL_{channel_name}`:
  - 指定したチャンネルの入力データを含むディレクトリへのパスを表す文字列。
  - ex.) TrainingJobの起動時に2つの入力チャンネルを「train」と「test」という名前で指定した場合、環境変数`SM_CHANNEL_TRAIN`と`SM_CHANNEL_TEST`が設定される。
- `SM_HPS`:
  - ハイパーパラメータのjson dump (`hyperparameters`引数で指定した値がそのまま入っている?)
  - 例えば以下。

```python
SM_HPS='{"batch-size": "256", "learning-rate": "0.0001","communicator": "pure_nccl"}'
hyperparameters = json.loads(os.environ['SM_HPS'])
```

- `SM_HP_{hyperparameter_name}`:
  - ハイパーパラメータの値を表す文字列。
  - ex.) `SM_HP_BATCH_SIZE=256`
- `SM_NUM_GPUS`:
  - 利用可能なGPUの数。
- `SM_NUM_CPUS`:
  - 利用可能なCPUの数。
- `SM_LOG_LEVEL`:
  - ログレベル。
  - ex.) `SM_LOG_LEVEL=20`
  - 使い方は以下。

```python
import os
import logging

logger = logging.getLogger(__name__)

logger.setLevel(int(os.environ.get('SM_LOG_LEVEL', logging.INFO)))
```

- `SM_INPUT_DIR=/opt/ml/input/`:
  - 入力データとconfigurationファイルが含まれるディレクトリ。
- `SM_INPUT_CONFIG_DIR=/opt/ml/input/config`:
  - configurationファイルが含まれるディレクトリ。
  - 学習開始時には以下の3つのファイルが存在する:
    - `hyperparameters.json`: リクエスト時に指定されたハイパーパラメータの値を含むjsonファイル。
    - `inputdataconfig.json`: リクエスト時に指定されたinput data configurationを含むjsonファイル。`SM_INPUT_DATA_CONFIG`で取得可能
    - `resourceconfig.json`: 現在のホストと学習ジョブ内のすべてのホスト名を含むjsonファイル。`SM_RESOURCE_CONFIG`で取得可能。
- `SM_OUTPUT_DATA_DIR=/opt/ml/output/data/`:
  - non-modelの学習成果物を保存するディレクトリ。(ex.評価指標の値)
- `SM_TRAINING_ENV`:
  - トレーニング情報全体を提供するjson文字列。

# Sagemaker Processing

- データの前処理、後処理、特徴量エンジニアリング、データ検証、モデル評価を行うためのジョブをSageMaker上で実行するための機能。
  - これらの処理ジョブは、入力データとしてAmazon S3からデータを受け取り、処理したデータをS3に出力として保存する。
  - SageMaker Processingは、機械学習パイプラインのデータ処理ステップを効率的に管理するための強力なツールであり、データをトレーニングや推論に適した状態に整えるために重要な役割を果たす。
- Sagemaker Python SDKで実装する場合は、`ScriptProcessor`クラスを使用する。
- ジョブの実行時には、複数の入力データ、複数の出力データを定義できる。

```python
from sagemaker.sklearn.processing import SKLearnProcessor

sklearn_processor = SKLearnProcessor(
    framework_version="0.20.0",
    role="[Your SageMaker-compatible IAM role]",
    instance_type="ml.m5.xlarge",
    instance_count=1,
)

from sagemaker.processing import ProcessingInput, ProcessingOutput

sklearn_processor.run(
    code="preprocessing.py", # source_dirからの相対パス
    source_dir="path/to/your_module", # codeで指定したファイルが含まれるディレクトリ
    inputs=[
        ProcessingInput(source="s3://your-bucket/path/to/your/data", destination="/opt/ml/processing/input"), input_name="input_name",
    ],
    outputs=[
        ProcessingOutput(output_name="train_data", source="/opt/ml/processing/train", destination="s3://your-output-bucket/path/to/output/data/"),
        ProcessingOutput(output_name="test_data", source="/opt/ml/processing/test", destination="s3://your-output-bucket/path/to/output/data/"),
    ],
    arguments=["--train-test-split-ratio", "0.2"],
)
```

この場合以下の事が起こる:

- 入力データとして、S3の`{sourceで指定したS3URI}`以下の全てのS3オブジェクトが`{destinationで指定したディレクトリ}/{input_name}`以下にダウンロードされる。
- `preprocessing.py`が実行される。
- `preprocessing.py`の実行結果として、`{destinationで指定したディレクトリ}/{output_name}`以下の全てのファイルがS3の`{destinationで指定したS3URI}`以下にアップロードされる。

# Sagemaker Batch Transform

- 訓練済みモデルを使って大量のデータに対して推論を行うサービス。
  - 必要な計算リソースを管理し、エンドポイントへのインスタンスの展開からその後の削除までを行う。
- Training JobやProcessing Jobと同様に、使用する推論スクリプトをS3バケットにアップロードするか、またはローカル環境から直接参照することが可能。
  - 推論用のスクリプトを`entry_point`引数で指定する。
- 基本的には学習済みモデルのファイルがS3上に存在する前提で実行される。
  - そのため、`model_data`引数にはS3上のモデルファイル `hoge.tar.gz` のパスを指定する必要がある。
