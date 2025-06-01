## モデルインスタンスの保存について

- refs: 
  - Pytorch公式: [Saving and Loading Models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

### 大きく3種類あるっぽい

#### 1つ目: 基本 state_dict形式 (.pth or .pt)
  - ex. `torch.save(model.state_dict(), 'model.pth')`
  - 一番よく使われる形式。
  - モデルの重み・バイアスなどのパラメータのみを全部state_dictという辞書形式で保存する方法。
  - メリット:
    - PyTorch公式でも推奨されてる保存方法.
    - モデルの再学習や推論で柔軟に使いやすい。
    - クラス定義が変わっても比較的安全。


読み込み方の例:

```python
model = TheModelClass(*args, **kwargs)
model.load_state_dict(torch.load(PATH, weights_only=True))
model.eval()  # 推論モードにするの忘れずに！
```


#### 2つ目: モデル全体を保存する方法 (.pt 形式)
  - ex. `torch.save(model, 'model.pt')`
  - モデルのクラス構造ごと全部保存する方法。
  - 注意点:
    - クラス定義やディレクトリ構成が変わると読み込めなくなるリスクあり。
    - 基本的にはstate_dict形式を使うことが推奨されてる。

読み込み方の例:

```python
model = torch.load(PATH, weights_only=False)
model.eval()
```

#### 3つ目: TorchScript形式 (.pt 形式)

- ex. `torch.jit.save(torch.jit.script(model), 'model_scripted.pt')`
- モデルをTorchScriptに変換して保存する方法。
- メリット:
  - モデルクラスの定義がなくても動く。
  - リアルタイム推論サーバーへのデプロイや、C++などの他言語環境で推論させたい場合に適してる。

### チェックポイント保存 (再学習・中断再開用)

必要に応じて、いろんなパラメータもdict形式で保存できる。

保存の例:

```python
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, PATH)
```

読み込みの例:

```python
model = TheModelClass(*args, **kwargs)
optimizer = TheOptimizerClass(*args, **kwargs)
checkpoint = torch.load(PATH, weights_only=True)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']
```

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
