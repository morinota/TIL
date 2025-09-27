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
  - [Pytorch公式doc embedding](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)

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

## transforms/Dataset/DataLoaderの役割について

- refs (読んだらチェック!):
  - [x] [PyTorch transforms/Dataset/DataLoaderの基本動作を確認する](https://qiita.com/takurooo/items/e4c91c5d78059f92e76d)
  - [x] [Pytorch+Polarsで高速で動作するDatasetを作る](https://zenn.dev/wotb_pythonista/articles/c5453b6e3d4625)
  - [x] [torch.tensor への変換における Numpy と Polars の速度比較](https://zenn.dev/uchiiii/articles/f58519345987ca)
  - [ ] [Pytorch DataLoaderで学習高速化！num_workersを増やすだけじゃダメ！](https://blog.master-of-ai.jp/posts/dataloader/)
  - [ ] [PyTorchでの学習・推論を高速化するコツ集](https://qiita.com/sugulu_Ogawa_ISID/items/62f5f7adee083d96a587)


### transforms/dataset/dataloaderのざっくり役割・関係性メモ

- ざっくり役割
  - transforms: 
    - データの前処理を担当するモジュール。
  - Dataset:
    - データと対応するラベルを1組返すモジュール。
    - データを返す時にtransformsを使って前処理したものを返す。
  - DataLoader:
    - Datasetからデータをバッチサイズに固めて返すモジュール。
- 3モジュールの関係性: 
  - **Datasetはtransformsを制御して、DataLoaderはDatasetを制御する(i.e. 依存する, 参照する?)という関係性**。
  - 使い方の流れ:
    - 1. Datasetクラスをインスタンス化する際に、transformsを引数として渡す。
    - 2. DataLoaderクラスをインスタンス化する際に、Datasetを引数として渡す。
    - 3. 学習時にDataLoaderからデータとラベルをバッチサイズで取得する。

#### transformsの実装のお約束:

- 必要な条件(1つ):
  - 予め用意されているtransformsの動作に習うために **「コール可能なクラス」として実装する必要がある**
    - (「コール可能」とは__call__を実装しているクラスのこと...!:thinking:)
- なぜコール可能にする必要がある??
  - 公式チュートリアルによると...
    - >We will write them as callable classes instead of simple functions so that parameters of the transform need not be passed everytime it’s called.
  - **つまり、クラスにしておけば、インスタンス化時に前処理に使うパラメータを全部渡して置けるので、前処理を実行するたびにパラメータを渡すという手間が省けるから**。

ex. 

```python
class Square(object):
    def __init__(self):
        pass
    
    def __call__(self, sample: int) -> int:
        # 任意の前処理を実装
        return sample ** 2

transform = Square()
print(transform(1)) # -> 1
print(transform(2)) # -> 4
print(transform(3)) # -> 9
print(transform(4)) # -> 16
```

#### Datasetの実装のお約束:

- PyTorchでは有名なデータセットがあらかじめtorchvision.datasetsに定義されている。**自前のデータを扱いたいときは自分のデータをリードして返してくれるDatasetを実装する必要**がある。
- 必要な条件(3つ):
  - 一つ目: `torch.utils.data.Dataset`を継承すること。
  - 二つ目: `__len__`メソッドを実装すること。
    - (`len(obj)`で実行されたときにコールされる関数...!:thinking:)
  - 三つ目: `__getitem__`メソッドを実装すること。
    - (`obj[idx]`のようにindex指定されたときにコールされる関数...!:thinking:)

ex. 

```python
import torch

# 必要条件1: torch.utils.data.Datasetを継承してること。
class MyDataset(torch.utils.data.Dataset):
  def __init__(self, data_num, transform=None):
        self.transform = transform
        self.data_num = data_num
        self.data = []
        self.label = []
        for x in range(self.data_num):
            self.data.append(x) # 0 から (data_num-1) までのリスト
            self.label.append(x%2 == 0) # 偶数ならTrue 奇数ならFalse
    
    # 必要条件2: __len__メソッドを実装してること。
    def __len__(self):
        return self.data_num

    # 必要条件3: __getitem__メソッドを実装してること。
    def __getitem__(self, idx):
        out_data = self.data[idx]
        out_label =  self.label[idx]
        
        # ポイント: データを返す前にtransformで前処理をしてから返してるところ。
        if self.transform:
            out_data = self.transform(out_data)
            
        return out_data, out_label
  
# 呼び出し例
data_set = MyDataset(10, transform=None)
print(data_set[0]) # -> (0, True)
print(data_set[1]) # -> (1, False)
print(data_set[2]) # -> (2, True)
print(data_set[3]) # -> (3, False)
print(data_set[4]) # -> (4, True)

# 先ほど実装したtransformsを渡してみる.
# データが二乗されていることに注目.
data_set = MyDataset(10, transform=Square())
print(data_set[0]) # -> (0, True)
print(data_set[1]) # -> (1, False)
print(data_set[2]) # -> (4, True)
print(data_set[3]) # -> (9, False)
print(data_set[4]) # -> (16, True)
```

#### DataLoaderの実装のお約束:

- DataLoaderは、上で説明したDatasetの仕組みを利用してバッチサイズ分のデータを生成する。
- また、データのシャッフル機能も持つ。
- **データを返す時は、データをtensor型に変換して返す。**
  - tensor型は計算グラフを保持することができるデータ型なので、DeepLearningの勾配計算に不可欠なデータ型。
- 基本的には自前で用意する必要はなく、`torch.utils.data.DataLoader`をインスタンス化して十分に対応できるケースがほとんど。

ex. 

```python
import torch
data_set = MyDataset(10, transform=Square())
dataloader = torch.utils.data.DataLoader(data_set, batch_size=2, shuffle=True)

for i in dataloader:
    print(i)

# [tensor([ 4, 25]), tensor([1, 0])]
# [tensor([64,  0]), tensor([1, 1])]
# [tensor([36, 16]), tensor([1, 1])]
# [tensor([1, 9]), tensor([0, 0])]
# [tensor([81, 49]), tensor([0, 0])]
```

学習の際には、dataloaderのループを更にepochのループで被せるイメージ。

```python
epochs = 4
for epoch in epochs:
    for i in dataloader:
        # 学習処理
```

### Datasetクラスはpandasベースやnumpyベースよりもpolarsベースが高速らしい!

- 機械学習モデルの学習や推論では、column単位のアクセスではなくrow単位のアクセスの頻度が多く、それが高速に動作する事は非常に重要のはず。
  - **polarsはrow単位のアクセスが苦手なはず。なぜならデータを内部でarrow formatで保持しているから。その代わりにcolumn単位のアクセスが得意**。
- なのになぜpolarsベースが早くなるのか??
  - numpyとpolarsを、純粋なrow単位のrandom accessで比較するとnumpyの方がかなり高速。
  - でも、**numpy.array -> torch.tensorの変換のoverheadが非常に大きいらしく**、row単位のアクセスの差が誤差になるくらい。
    - tuple -> torch.tensorの変換の方がやや早いらしい。
    - でもtorch.from_numpy()の場合はnumpy.arrayのコピーを作らないから、速度向上が見込めるらしい。
  - 結果として、polarsの方がnumpyよりも高速になるらしい。
    - polarsの場合は、df -> tuple -> torch.tensorの変換で、numpy.arrayを経由しないから早くなってるみたい。


例:

```python
    def __getitem__(self, idx):
        # このpolars.dataframe.row(idx)はtupleを返す.
        features = np.array(self.dataframe.row(idx)[:-1])
        target = np.array(self.dataframe.row(idx)[-1])
        features = self.dataframe.row(idx)[:-1]
        target = self.dataframe.row(idx)[-1]
        return torch.tensor(features, dtype=torch.float32), torch.tensor(
            target, dtype=torch.float32
        )
```

### Pytorch DataLoaderで学習高速化の話。

- 基本的なDataLoaderの使い方は以下:
  - `loader = DataLoader(my_dataset, batch_size=32, shuffle=True)`
- しかしこれだとDataLoaderの能力を完全には発揮できていないっぽい。
- DataLoaderの引数:
  - `dataset`引数
  - `batch_size`引数
  - `shuffle`引数: epochごとにデータをシャッフルするかどうか。
  - `num_workers`引数: 並列データ読み込みのプロセス数。
  - `pin_memory`引数: CPU -> GPU転送を非同期に (CUDA環境ならTrueにするのが良いらしい)。
  - `drop_last`引数: 最後に余る端数バッチを捨てるかどうか。
  - `persistent_workers`引数: Trueにすると、DataLoaderのプロセスがエポック間で生き続ける。
  - `prefetch_factor`引数: バッチの先読み数。
- 高速化に関連する重要な引数たち:
  - その1: `num_workers`
  - その2: `persistent_workers`
    - 通常，DataLoaderが最後のバッチまでの処理を行うとプロセスを終了する。
    - そうすると次のエポック開始時にプロセスを再生成する必要がある。
    - そこでpersistent_workersをTrueとすることで，プロセスを終了させず，次のエポックに再利用することができる。
  - その3: `prefetch_factor`
    - 各プロセスが先読みするバッチ数を指定できる。
    - 通常は1つのプロセスにつき2つのバッチしか読み込んでおらず，バッチデータを投げ込んで処理している間待機状態となる。
    - この時間で次のバッチを読み込み，空いている時間を効率よく使うことができる。
    - ただし，バッチデータを多く保持するので，メモリのオバーフローに注意。

例:

```python
DataLoader(ds, 
            batch_size=32, 
            shuffle=True, 
            num_workers=4,
            pin_memory=True, 
            prefetch_factor=4, 
            persistent_workers=True, 
            drop_last=True)
```

- 上記の場合...
  - 4つのプロセス(num_workers=4)が4バッチ分先読み(prefetch_factor=4)しているので，最大で16バッチがモデル入力のキューに溜まることになる。
  - サンプル数に換算すると、4*4*32=512サンプル分がメモリ上にスタンバイされることになる。
  - よってメモリの占有率は上昇するが、読み込みに時間がかかるデータにおいては、先に裏で読み込みを行うことで学習時間の短縮が期待できる。


