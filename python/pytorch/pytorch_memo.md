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


## embedding layer (nn.Embedding)について

- refs:
  - https://zenn.dev/kaba777/articles/32d8f619ef4f72
  - [【Pytorch】nn.Embeddingの使い方を丁寧に](https://gotutiyan.hatenablog.com/entry/2020/09/02/200144)
  - [pytorch の Embedding の挙動について](https://info.drobe.co.jp/blog/engineering/pytorch-embedding)

- NNでカテゴリカル特徴量を扱う方法の一つとしてEntity Embeddingがある。
  - 詳細は /Users/masato.morita/src/TIL/machine_learning/特徴量エンジニアリング/entity_embedding_memo.md 
  - One-hot encodingよりも、カテゴリを密ベクトルにマッピングして意味を学習することができるのがentity embeddingの魅力。

### nn.Embeddingクラスについて:

- 特徴
  - 軽い! 
    - one-hot encodingよりも次元数が小さく効率的。
  - 学習可能!
    - ベクトルの値は誤差逆伝搬で更新できる。freezeも可能。
  - 柔軟!
    - 多次元埋め込み、複数カテゴリに対応できる。


- ざっくり使い方: 
  - 初期化時の引数は基本的に2つ!
    - 第一引数: `num_embeddings` 語彙サイズ。
    - 第二引数: `embedding_dim` 埋め込み次元数。
    - オプショナルの引数:
      - `padding_idx`オプション: 空っぽのゼロベクトルとして埋め込むようなカテゴリIDを指定する。
      - `max_norm`オプション: 埋め込みベクトルの最大ノルムを制限する。
      - `norm_type`オプション: ノルムの計算方法を指定する。デフォルトは2ノルム。
      - `scale_grad_by_freq`オプション: 勾配をカテゴリの出現頻度でスケーリングする。
      - `sparse`オプション: 勾配を疎行列で計算するかどうか。デフォルトはFalse。
  - 変数(properties?)
    - `weight (Tensor)`: nn.Embeddingの学習可能なパラメータ。形状は(`num_embeddings`, `embedding_dim`)。標準正規分布N(0, 1)で初期化される。
  - 入出力の形状:
    - 入力: `(*)`。IntTensorもしくはLongTensor。各要素は抽出したいカテゴリ値のID。
    - 出力: `(*, embedding_dim)`

```python
import torch
import torch.nn as nn

# 例：性別2種類、職業22種類を、それぞれ8次元ベクトルに
embedding_gender = nn.Embedding(num_embeddings=2, embedding_dim=8)
embedding_job = nn.Embedding(num_embeddings=22, embedding_dim=8)

# カテゴリデータ（label化済み）をTensorで渡す
gender_idx = torch.tensor([0, 1, 1, 0])   # 0:男性、1:女性
job_idx = torch.tensor([3, 12, 7, 5])     # 職業ID

# 埋め込みベクトルに変換（バッチでOK）
gender_emb = embedding_gender(gender_idx)  # shape: [4, 8]
job_emb = embedding_job(job_idx)           # shape: [4, 8]

# 特徴量と連続特徴を合算してMLPへ！
x = torch.cat([gender_emb, job_emb, ...], dim=1)
```

- 公式の説明は以下:
  - >A simple lookup table that stores embeddings of a fixed dictionary and size. (**固定長の辞書埋め込みを保存するシンプルなルックアップテーブル**)

### nn.Embeddingの学習について

- Embedding がシンプルなルックアップテーブルだという事は理解できたが、**ランダムに作られたベクトルというだけでは対して役に立たない**。
  - 入力に対して学習をしてこのベクトルに意味を持たせる事が大事
- クラスメソッド`from_pretrained()`を使うと、事前学習済みのembedding layerを読み込むことができる。
  - 引数:
    - `embeddings(Tensor)`: 事前学習済みの埋め込みテーブル。FloatTensor型。形状は(`num_embeddings`, `embedding_dim`)。
    - `freeze(bool)`: Trueにすると、埋め込みテーブルは学習時に更新されなくなる。`embedding.weight.requires_grad`の値に相当する。
    - `padding_idx(int)`: 初期化時と同じ。
    - `max_norm(float)`: 初期化時と同じ。
    - `norm_type(float)`: 初期化時と同じ。
    - `scale_grad_by_freq(bool)`: 初期化時と同じ。
    - `sparse(bool)`: 初期化時と同じ。


- `from_pretrained()`の使い方の例:

```python
# FloatTensor containing pretrained weights
weight = torch.FloatTensor([[1, 2.3, 3], [4, 5.1, 6.3]])
embedding = nn.Embedding.from_pretrained(weight)
# Get embeddings for index 1
input = torch.LongTensor([1])
embedding(input)
tensor([[ 4.0000,  5.1000,  6.3000]])
```


