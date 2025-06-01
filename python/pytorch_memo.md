## モデルインスタンスの保存について

- refs: 
  - https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html

### 大きく3種類あるっぽい

#### 1つ目: 基本 state_dict形式 (.pth or .pt)
  - ex. `torch.save(model.state_dict(), 'model.pth')`
  - 一番よく使われる形式。モデルの重み・バイアスなどのパラメータのみを保存する方法。
  - メリット:
    - PyTorch公式でも推奨されてる保存方法.
    - モデルの再学習や推論で柔軟に使いやすい。
    - クラス定義が変わっても比較的安全。

必要に応じて、いろんなパラメータもdict形式で保存できる。

```python
# 学習時のチェックポイント保存
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, "checkpoint.pth")
```


#### 2つ目: モデル全体を保存する方法 (.pt 形式)
  - ex. `torch.save(model, 'model.pt')`
  - モデルのクラス構造ごと全部保存する方法。
  - クラス定義がロード時に必要になるので、プロジェクト構造が変わると読み込めなくなるリスクあり。

#### 3つ目: TorchScript形式 (.pt 形式)
  - ex. `torch.jit.save(torch.jit.script(model), 'model_scripted.pt')`
  - モデルをTorchScriptに変換して保存する方法。
  - リアルタイム推論サーバーへのデプロイや、他言語環境で推論させたい場合に適してる。


### state_dict形式のS3との読み書きについて

大きく2通り方法があるっぽい。

#### 方法1: 一般的なやり方 (自前で実装)

- PyTorchの`torch.save()`や`torch.load()`は、基本的にローカルファイルやfile-likeオブジェクト(バッファなど)に対して動作する。
- なので、一度ローカルストレージやメモリ上のバッファ(`io.BytesIO`)に保存してから、boto3などでS3とダウンロード/アップロードする流れが一般的。

ex. バッファを使ってS3に書き込む例:
(読み込みも同様で、S3からバッファにダウンロードしてから`torch.load()`したらOK)

```python
import torch
import io
import boto3

# state_dictをバッファに保存
buffer = io.BytesIO()
torch.save(model.state_dict(), buffer)
buffer.seek(0)

# S3にアップロード
s3 = boto3.client('s3')
s3.put_object(Bucket='your-bucket', Key='model.pth', Body=buffer.getvalue())
```

#### 方法2: PyTorch公式拡張を使う

- 2023年末にAmazon S3 Connector for PyTorchって公式拡張が登場した。
  - https://github.com/awslabs/s3-connector-for-pytorch
- これを使えば、一時ファイルやバッファを意識せず、直接S3に保存・読み込みができるらしい。

ex. 

```python
from s3torchconnector import S3Checkpoint
import torch

CHECKPOINT_URI = "s3://your-bucket/path/"
REGION = "ap-northeast-1"
checkpoint = S3Checkpoint(region=REGION)

# S3に直接保存
with checkpoint.writer(CHECKPOINT_URI + "model.pth") as writer:
    torch.save(model.state_dict(), writer)

# S3から直接読み込み
with checkpoint.reader(CHECKPOINT_URI + "model.pth") as reader:
    state_dict = torch.load(reader)
model.load_state_dict(state_dict)
```
