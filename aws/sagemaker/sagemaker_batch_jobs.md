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
