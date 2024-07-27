## refs:

- https://sagemaker.readthedocs.io/en/stable/overview.html#configuring-and-using-defaults-with-the-sagemaker-python-sdk

## コンフィグファイルの場所

- SageMaker Python SDKは、デフォルトで2つの場所からconfigファイルを探そうとする。
  - Platform (macやwindowsなど)によってデフォルトの位置は若干異なるっぽい??
    - あと、Sagemaker notebookもまた別の場所にあるみたい。 
  - 以下のコードで確認できるみたい。

```python
import os
from platformdirs import site_config_dir, user_config_dir

#Prints the location of the admin config file
print(os.path.join(site_config_dir("sagemaker"), "config.yaml"))

#Prints the location of the user config file
print(os.path.join(user_config_dir("sagemaker"), "config.yaml"))
```

- 自分の場合は以下だった。
  - admin config fileの場所:
    - `/Library/Application Support/sagemaker/config.yaml`
  - user config fileの場所:
    - `/Users/{user_name}/Library/Application Support/sagemaker/config.yaml`

## コンフィグファイルの場所の上書き方法

- 特定の環境変数のいずれかもしくは両方を指定することで、参照するconfigファイルの場所を上書きできる。
  - `SAGEMAKER_ADMIN_CONFIG_OVERRIDE`: SDKがデフォルトでadmin configファイルを探す場所を上書きできる。
  - `SAGEMAKER_USER_CONFIG_OVERRIDE`: SDKがデフォルトでuser configファイルを探す場所を上書きできる。
- 指定できる内容:
  - ローカルのconfigファイルパス
  - S3URI
- パス (or S3URI)の指定方法:
  - configファイルのパス (ex. `file://path/to/dev_config.yaml`)
  - configファイルが存在するディレクトリのパス (ex. `file://path/to/`)
    - この場合、Sagemaker SDKは**ディレクトリ直下で`config.yaml` という名前のファイル**を探そうとする。(再帰的検索は行わない)

## (あんまり使う必要あるかわからないけど) 追加で複数のconfigファイルを読み込む方法

- [link](https://sagemaker.readthedocs.io/en/stable/overview.html#configuration-file-structure:~:text=entry%20is%20added.-,Specify%20additional%20configuration%20files,-In%20addition%20to)

## DebuggerHookConfigってどんな設定??

- TrainingJobでデバッグ情報を収集するための設定。
  - job実行中に詳細なデバッグ情報を取得し、トレーニングプロセスの進行状況をリアルタイムで監視し、パフォーマンスを評価するためのデータを提供する。
    - ex. 勾配消失、勾配爆発、over fitting, etc.
