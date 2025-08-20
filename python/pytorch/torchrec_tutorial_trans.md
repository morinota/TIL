
Opens in a new window
新しいウィンドウで開く

Opens an external website
外部ウェブサイトを開く

Opens an external website in a new window
新しいウィンドウで外部ウェブサイトを開く

This website utilizes technologies such as cookies to enable essential site functionality, as well as for analytics, personalization, and targeted advertising.
このウェブサイトは、基本的なサイト機能を有効にするため、また分析、パーソナライズ、ターゲット広告のためにクッキーなどの技術を利用しています。

To learn more, view the following link:
詳細を学ぶには、以下のリンクを参照してください：

- Learn
- 学ぶ

Get Started
- 始める

Tutorials
- チュートリアル

Learn the Basics
- 基本を学ぶ

PyTorch Recipes
- PyTorchレシピ

Intro to PyTorch - YouTube Series
- PyTorch入門 - YouTubeシリーズ

Webinars
- ウェビナー

Community
- コミュニティ

Landscape
- ランドスケープ

Join the Ecosystem
- エコシステムに参加する

Community Hub
- コミュニティハブ

Forums
- フォーラム

Developer Resources
- 開発者リソース

Contributor Awards
- 貢献者賞

Community Events
- コミュニティイベント

PyTorch Ambassadors
- PyTorch大使

Projects
- プロジェクト

PyTorch
- PyTorch

vLLM
- vLLM

DeepSpeed
- DeepSpeed

Host Your Project
- プロジェクトをホストする

Docs
- ドキュメント

PyTorch
- PyTorch

Domains
- ドメイン

Blogs & News
- ブログとニュース

Blog
- ブログ

Announcements
- お知らせ

Case Studies
- ケーススタディ

Events
- イベント

Newsletter
- ニュースレター

About
- について

PyTorch Foundation
- PyTorch財団

Members
- メンバー

Governing Board
- 理事会

Technical Advisory Council
- 技術諮問委員会

Cloud Credit Program
- クラウドクレジットプログラム

Staff
- スタッフ

Contact
- お問い合わせ

Begin Mobile Menu
モバイルメニューを開始

- Learn
- 学ぶ

- Get Started
- 始める

- Tutorials
- チュートリアル

- Learn the Basics
- 基本を学ぶ

- PyTorch Recipes
- PyTorchレシピ

- Introduction to PyTorch - YouTube Series
- PyTorch入門 - YouTubeシリーズ

- Webinars
- ウェビナー

- Community
- コミュニティ

- Landscape
- ランドスケープ

- Join the Ecosystem
- エコシステムに参加する

- Community Hub
- コミュニティハブ

- Forums
- フォーラム

- Developer Resources
- 開発者リソース

- Contributor Awards
- 貢献者賞

- Community Events
- コミュニティイベント

- PyTorch Ambassadors
- PyTorch大使

- Projects
- プロジェクト

- PyTorch
- PyTorch

- vLLM
- vLLM

- DeepSpeed
- DeepSpeed

- Host Your Project
- プロジェクトをホストする

- PyTorch
- PyTorch

- Domains
- ドメイン

- Blog & News
- ブログとニュース

- Blog
- ブログ

- Announcements
- お知らせ

- Case Studies
- ケーススタディ

- Events
- イベント

- Newsletter
- ニュースレター

- About
- について

- PyTorch Foundation
- PyTorch財団

- Members
- メンバー

- Governing Board
- 理事会

- Technical Advisory Council
- 技術諮問委員会

- Cloud Credit Program
- クラウドクレジットプログラム

- Staff
- スタッフ

- Contact
- お問い合わせ

End Mobile Menu
モバイルメニューを終了

⌘+K
- Intro
- イントロ

- Compilers
- コンパイラ

- Domains
- ドメイン

- Distributed
- 分散

- Deep Dive
- 深堀り

- Extension
- 拡張

- Ecosystem
- エコシステム

- Recipes
- レシピ

- Unstable
- 不安定

⌘+K
- X
- GitHub
- GitHub

- Discourse
- Discourse

- PyPi
- PyPi

X
- GitHub
- GitHub

- Discourse
- Discourse

- PyPi
- PyPi

Section Navigation
セクションナビゲーション

Image and Video
画像と動画

- TorchVision Object Detection Finetuning Tutorial
- TorchVisionオブジェクト検出ファインチューニングチュートリアル

- Transfer Learning for Computer Vision Tutorial
- コンピュータビジョンのための転移学習チュートリアル

- Adversarial Example Generation
- 敵対的例生成

- DCGAN Tutorial
- DCGANチュートリアル

- Spatial Transformer Networks Tutorial
- 空間変換ネットワークチュートリアル

Reinforcement Learning
強化学習

- Reinforcement Learning (DQN) Tutorial
- 強化学習（DQN）チュートリアル

- Reinforcement Learning (PPO) with TorchRL Tutorial
- TorchRLを用いた強化学習（PPO）チュートリアル

- Train a Mario-playing RL Agent
- マリオをプレイするRLエージェントを訓練する

- Pendulum: Writing your environment and transforms with TorchRL
- ペンデュラム：TorchRLを用いた環境と変換の作成

Recommendation Systems
推薦システム

- Introduction to TorchRec
- TorchRecの紹介

- Exploring TorchRec sharding
- TorchRecのシャーディングの探求

Other Domains
他のドメイン

- See Audio tutorials on the audio website
- オーディオウェブサイトでオーディオチュートリアルを参照

- See ExecuTorch tutorials on the ExecuTorch website
- ExecuTorchウェブサイトでExecuTorchチュートリアルを参照

-
- ドメイン

- Introduction...
- イントロダクション...

★
★
★
★
★

Note
注意

Go to the end to download the full example code.
最後に行って、完全な例のコードをダウンロードしてください。

Go to the end
最後に行く



# Introduction to TorchRec はじめに：TorchRec

Created On: Oct 02, 2024 | Last Updated: Jul 10, 2025 | Last Verified: Oct 02, 2024  
作成日：2024年10月2日 | 最終更新日：2025年7月10日 | 最終確認日：2024年10月2日  

TorchRec is a PyTorch library tailored for building scalable and efficient recommendation systems using embeddings.  
TorchRecは、埋め込みを使用してスケーラブルで効率的な推薦システムを構築するために特化したPyTorchライブラリです。  

This tutorial guides you through the installation process, introduces the concept of embeddings, and highlights their importance in recommendation systems.  
このチュートリアルでは、インストールプロセスを案内し、埋め込みの概念を紹介し、推薦システムにおけるその重要性を強調します。  

It offers practical demonstrations on implementing embeddings with PyTorch and TorchRec, focusing on handling large embedding tables through distributed training and advanced optimizations.  
PyTorchとTorchRecを使用した埋め込みの実装に関する実践的なデモを提供し、分散トレーニングと高度な最適化を通じて大規模な埋め込みテーブルを処理することに焦点を当てています。  

- Fundamentals of embeddings and their role in recommendation systems  
- 埋め込みの基本と推薦システムにおけるその役割  

- How to set up TorchRec to manage and implement embeddings in PyTorch environments  
- PyTorch環境で埋め込みを管理および実装するためのTorchRecの設定方法  

- Explore advanced techniques for distributing large embedding tables across multiple GPUs  
- 複数のGPUにわたって大規模な埋め込みテーブルを分散するための高度な技術を探る  

- PyTorch v2.5 or later with CUDA 11.8 or later  
- CUDA 11.8以降を搭載したPyTorch v2.5以上  

- Python 3.9 or later  
- Python 3.9以上  

- FBGEMM  
- FBGEMM  



## Install Dependencies 依存関係のインストール

Before running this tutorial in Google Colab, make sure to install the following dependencies:
Google Colabでこのチュートリアルを実行する前に、以下の依存関係をインストールしてください。

```
!pip3 install --pre torch --index-url https://download.pytorch.org/whl/cu121 -U
!pip3 install fbgemm_gpu --index-url https://download.pytorch.org/whl/cu121
!pip3 install torchmetrics==1.0.3
!pip3 install torchrec --index-url https://download.pytorch.org/whl/cu121
```

torchmetrics
==
1
Note
If you are running this in Google Colab, make sure to switch to a GPU runtime type.
注意
Google Colabで実行している場合は、GPUランタイムタイプに切り替えてください。
For more information, see Enabling CUDA
詳細については、CUDAの有効化を参照してください。



### Embeddings 埋め込み

When building recommendation systems, categorical features typically have massive cardinality, posts, users, ads, and so on. 
推薦システムを構築する際、カテゴリカル特徴は通常、大規模なカーディナリティ（多様性）を持ち、投稿、ユーザー、広告などがあります。

In order to represent these entities and model these relationships, embeddings are used. 
これらのエンティティを表現し、これらの関係をモデル化するために、embeddings（埋め込み）が使用されます。

In machine learning, embeddings are a vectors of real numbers in a high-dimensional space used to represent meaning in complex data like words, images, or users. 
機械学習において、embeddingsは高次元空間における実数のベクトルであり、単語、画像、ユーザーなどの複雑なデータにおける意味を表現するために使用されます。



### Embeddings in RecSys 埋め込みの推薦システムにおける役割

Now you might wonder, how are these embeddings generated in the first place? 
さて、これらの埋め込みは最初にどのように生成されるのか不思議に思うかもしれません。

Well, embeddings are represented as individual rows in an Embedding Table, also referred to as embedding weights. 
埋め込みは、Embedding Table（埋め込みテーブル）内の個々の行として表現され、埋め込み重みとも呼ばれます。

The reason for this is that embeddings or embedding table weights are trained just like all of the other weights of the model via gradient descent! 
その理由は、埋め込みや埋め込みテーブルの重みが、モデルの他の重みと同様に勾配降下法を通じて訓練されるからです！

Embedding tables are simply a large matrix for storing embeddings, with two dimensions (B, N), where: 
埋め込みテーブルは、埋め込みを保存するための大きな行列であり、2つの次元（B, N）を持ちます。ここで：

- B is the number of embeddings stored by the table 
- Bはテーブルに保存される埋め込みの数です。

- N is the number of dimensions per embedding (N-dimensional embedding). 
- Nは各埋め込みの次元数（N次元の埋め込み）です。

The inputs to embedding tables represent embedding lookups to retrieve the embedding for a specific index or row. 
埋め込みテーブルへの入力は、特定のインデックスまたは行の埋め込みを取得するための埋め込みルックアップを表します。

In recommendation systems, such as those used in many large systems, unique IDs are not only used for specific users, but also across entities like posts and ads to serve as lookup indices to respective embedding tables! 
多くの大規模システムで使用される推薦システムでは、ユニークIDは特定のユーザーだけでなく、投稿や広告などのエンティティ全体で使用され、それぞれの埋め込みテーブルへのルックアップインデックスとして機能します！

Embeddings are trained in RecSys through the following process: 
埋め込みは、次のプロセスを通じてRecSysで訓練されます：

- Input/lookup indices are fed into the model, as unique IDs. 
- 入力/ルックアップインデックスは、ユニークIDとしてモデルに供給されます。

- IDs are hashed to the total size of the embedding table to prevent issues when the ID > number of rows 
- IDは、IDが行数を超えた場合の問題を防ぐために、埋め込みテーブルの総サイズにハッシュ化されます。

- Embeddings are then retrieved and pooled, such as taking the sum or mean of the embeddings. 
- 次に、埋め込みが取得され、プールされます。例えば、埋め込みの合計または平均を取ります。

- This is required as there can be a variable number of embeddings per example while the model expects consistent shapes. 
- これは、モデルが一貫した形状を期待する一方で、例ごとに可変の埋め込み数が存在する可能性があるためです。

- The embeddings are used in conjunction with the rest of the model to produce a prediction, such as Click-Through Rate (CTR) for an ad. 
- 埋め込みは、モデルの残りの部分と組み合わせて使用され、広告のクリック率（CTR）などの予測を生成します。

- The loss is calculated with the prediction and the label for an example, and all weights of the model are updated through gradient descent and backpropagation, including the embedding weights that were associated with the example. 
- 損失は、予測と例のラベルを用いて計算され、モデルのすべての重みが勾配降下法と逆伝播を通じて更新されます。これには、例に関連付けられた埋め込み重みも含まれます。

These embeddings are crucial for representing categorical features, such as users, posts, and ads, in order to capture relationships and make good recommendations. 
これらの埋め込みは、ユーザー、投稿、広告などのカテゴリ特徴を表現するために重要であり、関係を捉え、良い推薦を行うために必要です。

The Deep learning recommendation model (DLRM) paper talks more about the technical details of using embedding tables in RecSys. 
Deep learning recommendation model（DLRM）に関する論文では、RecSysにおける埋め込みテーブルの使用に関する技術的詳細について詳しく説明しています。

This tutorial introduces the concept of embeddings, showcase TorchRec specific modules and data types, and depict how distributed training works with TorchRec. 
このチュートリアルでは、埋め込みの概念を紹介し、TorchRec特有のモジュールとデータ型を示し、TorchRecを使用した分散トレーニングの仕組みを描写します。



#### Embeddings in PyTorch#

In PyTorch, we have the following types of embeddings:
PyTorchでは、以下の種類の埋め込みがあります。

- torch.nn.Embedding: An embedding table where forward pass returns the embeddings themselves as is.
- torch.nn.Embedding: 埋め込みテーブルで、フォワードパスは埋め込み自体をそのまま返します。

- torch.nn.EmbeddingBag: Embedding table where forward pass returns embeddings that are then pooled, for example, sum or mean, otherwise known as Pooled Embeddings.
- torch.nn.EmbeddingBag: 埋め込みテーブルで、フォワードパスは埋め込みを返し、それがプールされます。例えば、合計や平均など、別名Pooled Embeddingsとして知られています。

In this section, we will go over a very brief introduction to performing embedding lookups by passing in indices into the table.
このセクションでは、テーブルにインデックスを渡すことによって埋め込みルックアップを実行するための非常に簡単な紹介を行います。

```
num_embeddings, embedding_dim = 10, 4  # Initialize our embedding table
weights = torch.rand(num_embeddings, embedding_dim)
print("Weights:", weights)  # Pass in pre-generated weights just for example, typically weights are randomly initialized
embedding_collection = torch.nn.Embedding(num_embeddings, embedding_dim, _weight=weights)
embedding_bag_collection = torch.nn.EmbeddingBag(num_embeddings, embedding_dim, _weight=weights)

# Print out the tables, we should see the same weights as above
print("Embedding Collection Table: ", embedding_collection.weight)
print("Embedding Bag Collection Table: ", embedding_bag_collection.weight)

# Lookup rows (ids for embedding ids) from the embedding tables
# 2D tensor with shape (batch_size, ids for each batch)
ids = torch.tensor([[1, 3]])
print("Input row IDS: ", ids)
embeddings = embedding_collection(ids)  # Print out the embedding lookups
# You should see the specific embeddings be the same as the rows (ids) of the embedding tables above
print("Embedding Collection Results: ")
print(embeddings)
print("Shape: ", embeddings.shape)

# ``nn.EmbeddingBag`` default pooling is mean, so should be mean of batch dimension of values above
pooled_embeddings = embedding_bag_collection(ids)
print("Embedding Bag Collection Results: ")
print(pooled_embeddings)
print("Shape: ", pooled_embeddings.shape)

# ``nn.EmbeddingBag`` is the same as ``nn.Embedding`` but just with pooling (mean, sum, and so on)
# We can see that the mean of the embeddings of embedding_collection is the same as the output of the embedding_bag_collection
print("Mean: ", torch.mean(embedding_collection(ids), dim=1))
```



# Initialize our embedding table 埋め込みテーブルの初期化

weights
=
torch
.
rand
(
num_embeddings
,
embedding_dim
)
weights
=
torch
.
rand
(
num_embeddings
,
embedding_dim
)
print
(
"Weights:"
,
weights
)
print
(
"Weights:"
,
weights
)



# Pass in pre-generated weights just for example, typically weights are randomly initialized
事前に生成された重みを渡すのは一例に過ぎず、通常は重みはランダムに初期化されます。

embedding_collection
=
torch
.
nn
.
Embedding
(
num_embeddings
,
embedding_dim
,
_weight
=
weights
)
embedding_bag_collection
=
torch
.
nn
.
EmbeddingBag
(
num_embeddings
,
embedding_dim
,
_weight
=
weights
)



# Print out the tables, we should see the same weights as above
テーブルを出力します。上記と同じ重みが表示されるはずです。

print
(
"Embedding Collection Table: "
,
embedding_collection
.
weight
)
print
(
"Embedding Bag Collection Table: "
,
embedding_bag_collection
.
weight
)



# Lookup rows (ids for embedding ids) from the embedding tables 埋め込みテーブルからの行の検索（埋め込みIDのID）




# 2D tensor with shape (batch_size, ids for each batch) 形状が(batch_size, 各バッチのids)の2Dテンソル

ids
=
torch
.
tensor
([[
1
,
3
]])
ids
=
torch
.
tensor
([[1, 3]])
print
(
"Input row IDS: "
,
ids
)
print
(
"入力行IDS: ", ids
)
embeddings
=
embedding_collection
(
ids
)
embeddings
=
embedding_collection(ids)



# Print out the embedding lookups 埋め込みルックアップの出力




# You should see the specific embeddings be the same as the rows (ids) of the embedding tables above
上記の埋め込みテーブルの行（ID）と特定の埋め込みが同じであることを確認する必要があります。

print
(
"Embedding Collection Results: "
)
print
(
embeddings
)
print
(
"Shape: "
,
embeddings
.
shape
)



# ``nn.EmbeddingBag`` default pooling is mean, so should be mean of batch dimension of values above
``nn.EmbeddingBag``のデフォルトプーリングは平均であるため、上記の値のバッチ次元の平均であるべきです。

pooled_embeddings
=
embedding_bag_collection
(
ids
)
pooled_embeddings
=
embedding_bag_collection
(
ids
)

print
(
"Embedding Bag Collection Results: "
)
print
(
pooled_embeddings
)
print
(
"Shape: "
,
pooled_embeddings
.
shape
)
print
(
"Embedding Bag Collection Results: "
)
print
(
pooled_embeddings
)
print
(
"Shape: "
,
pooled_embeddings
.
shape
)



# ``nn.EmbeddingBag`` is the same as ``nn.Embedding`` but just with pooling (mean, sum, and so on)
``nn.EmbeddingBag``は``nn.Embedding``と同じですが、プーリング（平均、合計など）が追加されています。



# We can see that the mean of the embeddings of embedding_collection is the same as the output of the embedding_bag_collection
embedding_collectionの埋め込みの平均が、embedding_bag_collectionの出力と同じであることがわかります。

print
(
"Mean: "
,
torch
.
mean
(
embedding_collection
(
ids
),
dim
=
1
))
print(
"平均: ",
torch.mean(embedding_collection(ids), dim=1)
)

Congratulations! Now you have a basic understanding of how to use embedding tables — one of the foundations of modern recommendation systems! 
おめでとうございます！これで、現代の推薦システムの基盤の一つである埋め込みテーブルの使い方について基本的な理解を得ました！

These tables represent entities and their relationships. 
これらのテーブルは、エンティティとその関係を表します。

For example, the relationship between a given user and the pages and posts they have liked.
例えば、特定のユーザーと彼らが「いいね」したページや投稿との関係です。



## TorchRecの特徴の概要

In the section above we’ve learned how to use embedding tables, one of the foundations of modern recommendation systems! 
上のセクションでは、現代の推薦システムの基盤の一つである埋め込みテーブルの使い方を学びました！

These tables represent entities and relationships, such as users, pages, posts, etc. 
これらのテーブルは、ユーザ、ページ、投稿などのエンティティと関係を表します。

Given that these entities are always increasing, a hash function is typically applied to make sure the IDs are within the bounds of a certain embedding table. 
これらのエンティティは常に増加しているため、特定の埋め込みテーブルの範囲内にIDが収まるように、通常はハッシュ関数が適用されます。

However, in order to represent a vast amount of entities and reduce hash collisions, these tables can become quite massive (think about the number of ads for example). 
しかし、膨大な数のエンティティを表現し、ハッシュ衝突を減らすために、これらのテーブルは非常に大きくなる可能性があります（例えば、広告の数を考えてみてください）。

In fact, these tables can become so massive that they won’t be able to fit on 1 GPU, even with 80G of memory. 
実際、これらのテーブルは非常に大きくなり、80Gのメモリがあっても1つのGPUに収まらないことがあります。

In order to train models with massive embedding tables, sharding these tables across GPUs is required, which then introduces a whole new set of problems and opportunities in parallelism and optimization. 
大規模な埋め込みテーブルを持つモデルをトレーニングするためには、これらのテーブルをGPU間でシャーディングする必要があり、これにより並列処理と最適化における新たな問題と機会が生まれます。

Luckily, we have the TorchRec library that has encountered, consolidated, and addressed many of these concerns. 
幸いなことに、これらの懸念に対処し、統合したTorchRecライブラリがあります。

TorchRec serves as a library that provides primitives for large scale distributed embeddings. 
TorchRecは、大規模分散埋め込みのためのプリミティブを提供するライブラリとして機能します。

Next, we will explore the major features of the TorchRec library. 
次に、TorchRecライブラリの主要な機能を探ります。

We will start with torch.nn.Embedding and will extend that to custom TorchRec modules, explore distributed training environment with generating a sharding plan for embeddings, look at inherent TorchRec optimizations, and extend the model to be ready for inference in C++. 
torch.nn.Embeddingから始め、カスタムTorchRecモジュールに拡張し、埋め込みのシャーディングプランを生成する分散トレーニング環境を探り、TorchRecの固有の最適化を見て、モデルをC++で推論できるように拡張します。

Below is a quick outline of what this section consists of: 
以下は、このセクションの内容の簡単な概要です：

- torch.nn.Embedding
- TorchRec Modules and Data Types
- Distributed Training, Sharding, and Optimizations

TorchRec Modules and Data Types
TorchRecモジュールとデータ型

Let’s begin with importing TorchRec: 
TorchRecをインポートすることから始めましょう：

```
import torchrec
```
import torchrec

This section goes over TorchRec Modules and data types including such entities as EmbeddingCollection and EmbeddingBagCollection, JaggedTensor, KeyedJaggedTensor, KeyedTensor and more. 
このセクションでは、EmbeddingCollectionやEmbeddingBagCollection、JaggedTensor、KeyedJaggedTensor、KeyedTensorなどのエンティティを含むTorchRecモジュールとデータ型について説明します。

- EmbeddingCollection
- EmbeddingBagCollection
- JaggedTensor
- KeyedJaggedTensor
- KeyedTensor



### FromEmbeddingBagtoEmbeddingBagCollection#

### EmbeddingBag
### EmbeddingBagCollection

We have already explored torch.nn.Embedding and torch.nn.EmbeddingBag. 
私たちはすでに `torch.nn.Embedding` と `torch.nn.EmbeddingBag` を探求しました。

TorchRec extends these modules by creating collections of embeddings, in other words modules that can have multiple embedding tables, with EmbeddingCollection and EmbeddingBagCollection. 
TorchRecは、EmbeddingCollectionとEmbeddingBagCollectionを使用して、複数の埋め込みテーブルを持つことができる埋め込みのコレクションを作成することによって、これらのモジュールを拡張します。

We will use EmbeddingBagCollection to represent a group of embedding bags. 
私たちは、埋め込みバッグのグループを表すためにEmbeddingBagCollectionを使用します。

torch.nn.Embedding
torch.nn.EmbeddingBag
EmbeddingCollection
EmbeddingBagCollection
EmbeddingBagCollection

In the example code below, we create an EmbeddingBagCollection (EBC) with two embedding bags, 1 representing products and 1 representing users. 
以下の例コードでは、2つの埋め込みバッグを持つEmbeddingBagCollection（EBC）を作成します。1つは製品を、もう1つはユーザーを表します。

Each table, product_table and user_table, is represented by a 64 dimension embedding of size 4096. 
各テーブル、`product_table` と `user_table` は、サイズ4096の64次元の埋め込みで表されます。

EmbeddingBagCollection
product_table
user_table

```
ebc=torchrec.EmbeddingBagCollection(device="cpu",tables=[torchrec.EmbeddingBagConfig(name="product_table",embedding_dim=64,num_embeddings=4096,feature_names=["product"],pooling=torchrec.PoolingType.SUM,),torchrec.EmbeddingBagConfig(name="user_table",embedding_dim=64,num_embeddings=4096,feature_names=["user"],pooling=torchrec.PoolingType.SUM,),],)print(ebc.embedding_bags)
```
```
ebc = torchrec.EmbeddingBagCollection(
device = "cpu",
tables = [
torchrec.EmbeddingBagConfig(
name = "product_table",
embedding_dim = 64,
num_embeddings = 4096,
feature_names = [
"product"
],
pooling = torchrec.PoolingType.SUM,
),
torchrec.EmbeddingBagConfig(
name = "user_table",
embedding_dim = 64,
num_embeddings = 4096,
feature_names = [
"user"
],
pooling = torchrec.PoolingType.SUM,
),
],
)
print(ebc.embedding_bags)
```

Let’s inspect the forward method for EmbeddingBagCollection and the module’s inputs and outputs: 
EmbeddingBagCollectionのforwardメソッドとモジュールの入力および出力を調べてみましょう。

```
import inspect
# Let's look at the ``EmbeddingBagCollection`` forward method
# What is a ``KeyedJaggedTensor`` and ``KeyedTensor``?
print(inspect.getsource(ebc.forward))
```
```
import inspect



# Let's look at the ``EmbeddingBagCollection`` forward method
「EmbeddingBagCollection」のフォワードメソッドを見てみましょう



# What is a ``KeyedJaggedTensor`` and ``KeyedTensor``? ``KeyedJaggedTensor``と``KeyedTensor``とは何ですか？

print
(
inspect
.
getsource
(
ebc
.
forward
))



### TorchRec 入出力データ型

TorchRecには、モジュールの入力と出力のための異なるデータ型があります：JaggedTensor、KeyedJaggedTensor、およびKeyedTensor。 
TorchRecには、モジュールの入力と出力のための異なるデータ型があります：JaggedTensor、KeyedJaggedTensor、およびKeyedTensor。
Now you might ask, why create new data types to represent sparse features? 
さて、なぜスパース特徴を表現するために新しいデータ型を作成するのかと疑問に思うかもしれません。
To answer that question, we must understand how sparse features are represented in code. 
その質問に答えるためには、スパース特徴がコード内でどのように表現されているかを理解する必要があります。

JaggedTensor  
KeyedJaggedTensor  
KeyedTensor  

Sparse features are otherwise known as id_list_feature and id_score_list_feature, and are the IDs that will be used as indices to an embedding table to retrieve the embedding for that ID. 
スパース特徴は、id_list_featureおよびid_score_list_featureとしても知られ、IDは埋め込みテーブルのインデックスとして使用され、そのIDの埋め込みを取得します。
To give a very simple example, imagine a single sparse feature being Ads that a user interacted with. 
非常に単純な例を挙げると、ユーザーが対話した広告が単一のスパース特徴であると想像してください。
The input itself would be a set of Ad IDs that a user interacted with, and the embeddings retrieved would be a semantic representation of those Ads. 
入力自体は、ユーザーが対話した広告のIDのセットであり、取得された埋め込みはそれらの広告の意味的表現になります。
The tricky part of representing these features in code is that in each input example, the number of IDs is variable. 
これらの特徴をコードで表現する際の難しい部分は、各入力例においてIDの数が可変であることです。
One day a user might have interacted with only one ad while the next day they interact with three. 
ある日はユーザーが1つの広告としか対話しなかったのに対し、次の日には3つの広告と対話するかもしれません。

id_list_feature  
id_score_list_feature  

A simple representation is shown below, where we have a lengths tensor denoting how many indices are in an example for a batch and a values tensor containing the indices themselves. 
以下に示すのは、バッチの例においていくつのインデックスがあるかを示すlengthsテンソルと、インデックス自体を含むvaluesテンソルを持つ単純な表現です。

lengths  
values  

```
# Batch Size 2# 1 ID in example 1, 2 IDs in example 2 id_list_feature_lengths=torch.tensor([1,2])# Values (IDs) tensor: ID 5 is in example 1, ID 7, 1 is in example 2 id_list_feature_values=torch.tensor([5,7,1])
```



# Batch Size 2 バッチサイズ2



# 1 ID in example 1, 2 IDs in example 2
id_list_feature_lengths
=
torch
.
tensor
([
1
,
2
])
1の例では1つのID、2の例では2つのIDがあります。
id_list_feature_lengths
=
torch
.
tensor
([
1
,
2
])



# Values (IDs) tensor: ID 5 is in example 1, ID 7, 1 is in example 2
# 値（ID）テンソル：ID 5は例1に、ID 7、1は例2にあります。
id_list_feature_values
=
torch
.
tensor
([
5
,
7
,
1
])
# 次に、オフセットと各バッチに含まれる内容を見てみましょう。
Next, let’s look at the offsets as well as what is contained in each batch
```
# Lengths can be converted to offsets for easy indexing of values
# 長さは値の簡単なインデックス付けのためにオフセットに変換できます。
id_list_feature_offsets=torch.cumsum(id_list_feature_lengths,dim=0)
print("Offsets: ",id_list_feature_offsets)
print("First Batch: ",id_list_feature_values[:id_list_feature_offsets[0]])
print("Second Batch: ",id_list_feature_values[id_list_feature_offsets[0]:id_list_feature_offsets[1]],)
# オフセットを表示します。
# FromtorchrecimportJaggedTensor
# ``JaggedTensor`` is just a wrapper around lengths/offsets and values tensors!
# ``JaggedTensor``は長さ/オフセットと値のテンソルをラップするだけのものです！
jt=JaggedTensor(values=id_list_feature_values,lengths=id_list_feature_lengths)
# Automatically compute offsets from lengths
# 長さからオフセットを自動的に計算します。
print("Offsets: ",jt.offsets())
# Convert to list of values
# 値のリストに変換します。
print("List of Values: ",jt.to_dense())
# ``__str__`` representation
# ``__str__`` 表現
print(jt)
# FromtorchrecimportKeyedJaggedTensor
# ``JaggedTensor`` represents IDs for 1 feature, but we have multiple features in an ``EmbeddingBagCollection``
# ``JaggedTensor``は1つの特徴のIDを表しますが、``EmbeddingBagCollection``には複数の特徴があります。
# That's where ``KeyedJaggedTensor`` comes in! ``KeyedJaggedTensor`` is just multiple ``JaggedTensors`` for multiple id_list_feature_offsets
# そこで``KeyedJaggedTensor``が登場します！``KeyedJaggedTensor``は複数のid_list_feature_offsetsのための複数の``JaggedTensors``です。
# From before, we have our two features "product" and "user". Let's create ``JaggedTensors`` for both!
# 前から、私たちには「product」と「user」という2つの特徴があります。両方のために``JaggedTensors``を作成しましょう！
product_jt=JaggedTensor(values=torch.tensor([1,2,1,5]),lengths=torch.tensor([3,1]))
user_jt=JaggedTensor(values=torch.tensor([2,3,4,1]),lengths=torch.tensor([2,2]))
# Q1: How many batches are there, and which values are in the first batch for ``product_jt`` and ``user_jt``?
# Q1: バッチは何個あり、``product_jt``と``user_jt``の最初のバッチにはどの値が含まれていますか？
kjt=KeyedJaggedTensor.from_jt_dict({"product":product_jt,"user":user_jt})
# Look at our feature keys for the ``KeyedJaggedTensor``
# ``KeyedJaggedTensor``の特徴キーを見てみましょう。
print("Keys: ",kjt.keys())
# Look at the overall lengths for the ``KeyedJaggedTensor``
# ``KeyedJaggedTensor``の全体の長さを見てみましょう。
print("Lengths: ",kjt.lengths())
# Look at all values for ``KeyedJaggedTensor``
# ``KeyedJaggedTensor``のすべての値を見てみましょう。
print("Values: ",kjt.values())
# Can convert ``KeyedJaggedTensor`` to dictionary representation
# ``KeyedJaggedTensor``を辞書表現に変換できます。
print("to_dict: ",kjt.to_dict())
# ``KeyedJaggedTensor`` string representation
# ``KeyedJaggedTensor``の文字列表現
print(kjt)
# Q2: What are the offsets for the ``KeyedJaggedTensor``?
# Q2: ``KeyedJaggedTensor``のオフセットは何ですか？
# Now we can run a forward pass on our ``EmbeddingBagCollection`` from before
# これで、前の``EmbeddingBagCollection``でフォワードパスを実行できます。
result=ebc(kjt)
result
# Result is a ``KeyedTensor``, which contains a list of the feature names and the embedding results
# 結果は``KeyedTensor``で、特徴名のリストと埋め込み結果が含まれています。
print(result.keys())
# The results shape is [2, 128], as batch size of 2. Reread previous section if you need a refresher on how the batch size is determined
# 結果の形状は[2, 128]で、バッチサイズは2です。バッチサイズがどのように決定されるかを再確認する必要がある場合は、前のセクションを再読してください。
# 128 for dimension of embedding. If you look at where we initialized the ``EmbeddingBagCollection``, we have two tables "product" and "user" of dimension 64 each
# 埋め込みの次元は128です。``EmbeddingBagCollection``を初期化した場所を見てみると、次元64の「product」と「user」という2つのテーブルがあります。
# meaning embeddings for both features are of size 64. 64 + 64 = 128
# つまり、両方の特徴の埋め込みはサイズ64です。64 + 64 = 128
print(result.values().shape)
# Nice to_dict method to determine the embeddings that belong to each feature
# 各特徴に属する埋め込みを決定するための良いto_dictメソッド
result_dict=result.to_dict()
for key,embedding in result_dict.items():
    print(key,embedding.shape)



# Lengths can be converted to offsets for easy indexing of values
長さはオフセットに変換でき、値の簡単なインデックス付けが可能です。

id_list_feature_offsets
=
torch
.
cumsum
(
id_list_feature_lengths
,
dim
=
0
)
id_list_feature_offsets
は、`torch.cumsum(id_list_feature_lengths, dim=0)` で計算されます。

print
(
"Offsets: "
,
id_list_feature_offsets
)
print
(
"First Batch: "
,
id_list_feature_values
[:
id_list_feature_offsets
[
0
]])
print
(
"Second Batch: "
,
id_list_feature_values
[
id_list_feature_offsets
[
0
]
:
id_list_feature_offsets
[
1
]],
)
print("Offsets: ", id_list_feature_offsets)
print("First Batch: ", id_list_feature_values[:id_list_feature_offsets[0]])
print("Second Batch: ", id_list_feature_values[id_list_feature_offsets[0]:id_list_feature_offsets[1]])

from
torchrec
import
JaggedTensor
torchrecからJaggedTensorをインポートします。



# ``JaggedTensor`` is just a wrapper around lengths/offsets and values tensors! ``JaggedTensor``は長さ/オフセットと値のテンソルをラップするだけのものです！

jt
=
JaggedTensor
(
values
=
id_list_feature_values
,
lengths
=
id_list_feature_lengths
)
jt
=
JaggedTensor
(
values
=
id_list_feature_values
,
lengths
=
id_list_feature_lengths
)



# Automatically compute offsets from lengths 長さからオフセットを自動的に計算する

print
(
"Offsets: "
,
jt
.
offsets
())



# Convert to list of values 値のリストに変換

print
(
"List of Values: "
,
jt
.
to_dense
())



# ``__str__`` representation ``__str__`` 表現

print
(
jt
)
print(jt)

from
torchrec
import
KeyedJaggedTensor
torchrecからKeyedJaggedTensorをインポートします。



# ``JaggedTensor`` represents IDs for 1 feature, but we have multiple features in an ``EmbeddingBagCollection``

``JaggedTensor``は1つの特徴のIDを表しますが、``EmbeddingBagCollection``には複数の特徴があります。



# That's where ``KeyedJaggedTensor`` comes in! ``KeyedJaggedTensor`` is just multiple ``JaggedTensors`` for multiple id_list_feature_offsets
# そこで ``KeyedJaggedTensor`` が登場します！ ``KeyedJaggedTensor`` は、複数の id_list_feature_offsets のための複数の ``JaggedTensors`` に過ぎません。



# From before, we have our two features "product" and "user". Let's create ``JaggedTensors`` for both!
以前から、私たちは「product」と「user」という2つの特徴を持っています。それでは、両方のために``JaggedTensors``を作成しましょう！

product_jt
=
JaggedTensor
(
values
=
torch
.
tensor
([
1
,
2
,
1
,
5
]),
lengths
=
torch
.
tensor
([
3
,
1
])
)
product_jt
=
JaggedTensor
(
values
=
torch
.
tensor
([
1
,
2
,
1
,
5
]),
lengths
=
torch
.
tensor
([
3
,
1
])
)

user_jt
=
JaggedTensor
(
values
=
torch
.
tensor
([
2
,
3
,
4
,
1
]),
lengths
=
torch
.
tensor
([
2
,
2
]))
user_jt
=
JaggedTensor
(
values
=
torch
.
tensor
([
2
,
3
,
4
,
1
]),
lengths
=
torch
.
tensor
([
2
,
2
]))



# Q1: How many batches are there, and which values are in the first batch for ``product_jt`` and ``user_jt``?
Q1: バッチは何個あり、``product_jt``と``user_jt``の最初のバッチにはどのような値が含まれていますか？

kjt
=
KeyedJaggedTensor
.
from_jt_dict
({
"product"
:
product_jt
,
"user"
:
user_jt
})



# Look at our feature keys for the ``KeyedJaggedTensor`` ``KeyedJaggedTensor``の特徴キーを見てみましょう
print
(
"Keys: "
,
kjt
.
keys
()) 
print
(
"Keys: "
,
kjt
.
keys
()) 



# Look at the overall lengths for the ``KeyedJaggedTensor`` ``KeyedJaggedTensor``の全体の長さを確認する

print
(
"Lengths: "
,
kjt
.
lengths
())



# Look at all values for ``KeyedJaggedTensor`` ``KeyedJaggedTensor``のすべての値を見る

print
(
"Values: "
,
kjt
.
values
()) 
print
(
"値: "
,
kjt
.
values
()) 



# Can convert ``KeyedJaggedTensor`` to dictionary representation ``KeyedJaggedTensor``を辞書表現に変換できます

print
(
"to_dict: "
,
kjt
.
to_dict
()) 
print
(
"to_dict: "
,
kjt
.
to_dict
()) 



# ``KeyedJaggedTensor`` string representation ``KeyedJaggedTensor``の文字列表現

print
(
kjt
)
print
(
kjt
)



# Q2: What are the offsets for the ``KeyedJaggedTensor``? ``KeyedJaggedTensor``のオフセットは何ですか？



# Now we can run a forward pass on our ``EmbeddingBagCollection`` from before
以前の``EmbeddingBagCollection``に対してフォワードパスを実行できます。

result
=
ebc
(
kjt
)
result
=
ebc
(
kjt
)



# Result is a ``KeyedTensor``, which contains a list of the feature names and the embedding results
結果は ``KeyedTensor`` であり、特徴名のリストと埋め込み結果を含みます。

print
(
result
.
keys
())
print
(
result
.
keys
())



# The results shape is [2, 128], as batch size of 2. 
結果の形状は[2, 128]であり、バッチサイズは2です。

Reread previous section if you need a refresher on how the batch size is determined.
バッチサイズがどのように決定されるかについての復習が必要な場合は、前のセクションを再読してください。



# 128 for dimension of embedding. 
埋め込みの次元は128です。

If you look at where we initialized the ``EmbeddingBagCollection``, we have two tables "product" and "user" of dimension 64 each.
``EmbeddingBagCollection``を初期化した場所を見ると、次元がそれぞれ64の「product」と「user」の2つのテーブルがあります。



# meaning embeddings for both features are of size 64. 64 + 64 = 128
両方の特徴の意味埋め込みはサイズ64です。64 + 64 = 128

print
(
result
.
values
()
.
shape
)
print
(
result
.
values
()
.
shape
)



# Nice to_dict method to determine the embeddings that belong to each feature
Nice to_dictメソッドを使用して、各特徴に属する埋め込みを特定します。

result_dict = result.to_dict()
result_dict = result.to_dict()

for key, embedding in result_dict.items():
for key, embedding in result_dict.items():
    print(key, embedding.shape)
    print(key, embedding.shape)

Congrats! You now understand TorchRec modules and data types.
おめでとうございます！これでTorchRecモジュールとデータ型を理解しました。

Give yourself a pat on the back for making it this far.
ここまで来た自分を褒めてあげましょう。

Next, we will learn about distributed training and sharding.
次は、分散トレーニングとシャーディングについて学びます。



### Distributed Training and Sharding 分散トレーニングとシャーディング

Now that we have a grasp on TorchRec modules and data types, it’s time to take it to the next level.  
TorchRecのモジュールとデータ型を理解したので、次のステップに進む時が来ました。

Remember, the main purpose of TorchRec is to provide primitives for distributed embeddings.  
TorchRecの主な目的は、分散埋め込みのためのプリミティブを提供することです。

So far, we’ve only worked with embedding tables on a single device.  
これまで、私たちは単一のデバイス上で埋め込みテーブルのみを扱ってきました。

This has been possible given how small the embedding tables have been, but in a production setting this isn’t generally the case.  
これは、埋め込みテーブルが非常に小さいため可能でしたが、実際のプロダクション環境では一般的にそうではありません。

Embedding tables often get massive, where one table can’t fit on a single GPU, creating the requirement for multiple devices and a distributed environment.  
埋め込みテーブルはしばしば巨大になり、1つのテーブルが単一のGPUに収まらないため、複数のデバイスと分散環境が必要になります。

In this section, we will explore setting up a distributed environment, exactly how actual production training is done, and explore sharding embedding tables, all with TorchRec.  
このセクションでは、分散環境の設定、実際のプロダクショントレーニングがどのように行われるか、そしてTorchRecを使用して埋め込みテーブルのシャーディングを探ります。

This section will also only use 1 GPU, though it will be treated in a distributed fashion.  
このセクションでは、1つのGPUのみを使用しますが、分散方式で扱われます。

This is only a limitation for training, as training has a process per GPU.  
これはトレーニングにのみ制限があり、トレーニングはGPUごとにプロセスを持つためです。

Inference does not run into this requirement.  
推論はこの要件に直面しません。

In the example code below, we set up our PyTorch distributed environment.  
以下の例コードでは、PyTorchの分散環境を設定します。

Warning  
警告

If you are running this in Google Colab, you can only call this cell once, calling it again will cause an error as you can only initialize the process group once.  
Google Colabでこれを実行している場合、このセルを1回しか呼び出せません。再度呼び出すとエラーが発生します。プロセスグループは1回しか初期化できないためです。

```
import os
import torch.distributed as dist

# Set up environment variables for distributed training
# RANK is which GPU we are on, default 0
os.environ["RANK"]="0"
# How many devices in our "world", colab notebook can only handle 1 process
os.environ["WORLD_SIZE"]="1"
# Localhost as we are training locally
os.environ["MASTER_ADDR"]="localhost"
# Port for distributed training
os.environ["MASTER_PORT"]="29500"
# nccl backend is for GPUs, gloo is for CPUs
dist.init_process_group(backend="gloo")
print(f"Distributed environment initialized: {dist}")
```



# Set up environment variables for distributed training
分散トレーニングのための環境変数を設定する



# RANK is which GPU we are on, default 0
RANKは、私たちが使用しているGPUを示し、デフォルトは0です。

os.environ["RANK"] = "0"
os.environ["RANK"] = "0"



# How many devices in our "world", colab notebook can only handle 1 process

# 私たちの「世界」にはどれだけのデバイスがあり、Colabノートブックは1つのプロセスしか処理できません。

os.environ["WORLD_SIZE"] = "1"



# Localhost as we are training locally ローカルでトレーニングしているためのローカルホスト

os.environ["MASTER_ADDR"] = "localhost"
os.environ["MASTER_ADDR"] = "localhost"



# Port for distributed training 分散トレーニングのためのポート

os.environ["MASTER_PORT"] = "29500"
os.environ["MASTER_PORT"] = "29500"



# nccl backend is for GPUs, gloo is for CPUs

nccl backend is for GPUs, gloo is for CPUs
ncclバックエンドはGPU用で、glooはCPU用です。

dist.init_process_group(backend="gloo")
dist.init_process_group(backend="gloo")

print(f"Distributed environment initialized: {dist}")
print(f"分散環境が初期化されました: {dist}")



### Distributed Embeddings 分散埋め込み

We have already worked with the main TorchRec module:EmbeddingBagCollection. 
私たちはすでに主要なTorchRecモジュールであるEmbeddingBagCollectionを使用しました。

We have examined how it works along with how data is represented in TorchRec. 
その動作と、TorchRecにおけるデータの表現方法を調査しました。

However, we have not yet explored one of the main parts of TorchRec, which is distributed embeddings. 
しかし、私たちはまだTorchRecの主要な部分の一つである分散埋め込みについて探求していません。

EmbeddingBagCollection 
EmbeddingBagCollection

GPUs are the most popular choice for ML workloads by far today, as they are able to do magnitudes more floating point operations/s (FLOPs) than CPU. 
GPUは、CPUよりも桁違いに多くの浮動小数点演算を行うことができるため、今日の機械学習ワークロードにおいて最も人気のある選択肢です。

However, GPUs come with the limitation of scarce fast memory (HBM which is analogous to RAM for CPU), typically, ~10s of GBs. 
しかし、GPUには限られた高速メモリ（CPUのRAMに相当するHBM）の制約があり、通常は数十GB程度です。

A RecSys model can contain embedding tables that far exceed the memory limit for 1 GPU, hence the need for distribution of the embedding tables across multiple GPUs, otherwise known as model parallel. 
RecSysモデルは、1つのGPUのメモリ制限を大幅に超える埋め込みテーブルを含むことができるため、埋め込みテーブルを複数のGPUに分散させる必要があります。これはモデル並列として知られています。

On the other hand, data parallel is where the entire model is replicated on each GPU, which each GPU taking in a distinct batch of data for training, syncing gradients on the backwards pass. 
一方、データ並列は、全体のモデルが各GPUに複製され、各GPUがトレーニングのために異なるデータバッチを受け取り、逆伝播で勾配を同期する方式です。

Parts of the model that require less compute but more memory (embeddings) are distributed with model parallel while parts that require more compute and less memory (dense layers, MLP, etc.) are distributed with data parallel. 
計算量は少ないがメモリを多く必要とするモデルの部分（埋め込み）はモデル並列で分散され、計算量が多くメモリが少ない部分（密な層、MLPなど）はデータ並列で分散されます。



### Sharding シャーディング

In order to distribute an embedding table, we split up the embedding table into parts and place those parts onto different devices, also known as “sharding”. 
埋め込みテーブルを分散させるために、埋め込みテーブルを部分に分割し、それらの部分を異なるデバイスに配置します。これを「シャーディング」と呼びます。

There are many ways to shard embedding tables. 
埋め込みテーブルをシャーディングする方法はいくつかあります。

The most common ways are: 
最も一般的な方法は以下の通りです。

- Table-Wise: the table is placed entirely onto one device 
- Table-Wise: テーブル全体が1つのデバイスに配置されます。

- Column-Wise: columns of embedding tables are sharded 
- Column-Wise: 埋め込みテーブルの列がシャーディングされます。

- Row-Wise: rows of embedding tables are sharded 
- Row-Wise: 埋め込みテーブルの行がシャーディングされます。



### Sharded Modules シャーディングモジュール

While all of this seems like a lot to deal with and implement, you’re in luck. 
これらすべては対処し実装するには多くのように思えますが、あなたは幸運です。

TorchRec provides all the primitives for easy distributed training and inference! 
TorchRecは、簡単な分散トレーニングと推論のためのすべての基本要素を提供します！

In fact, TorchRec modules have two corresponding classes for working with any TorchRec module in a distributed environment: 
実際、TorchRecモジュールには、分散環境で任意のTorchRecモジュールを操作するための2つの対応するクラスがあります：

- The module sharder: This class exposes a sharding API that handles sharding a TorchRec Module, producing a sharded module. 
- モジュールシャーダー：このクラスは、TorchRecモジュールをシャーディングし、シャーディングされたモジュールを生成するシャーディングAPIを公開します。

* For EmbeddingBagCollection, the sharder is `EmbeddingBagCollectionSharder` 
* EmbeddingBagCollectionの場合、シャーダーは`EmbeddingBagCollectionSharder`です。

- Sharded module: This class is a sharded variant of a TorchRec module. 
- シャーディングモジュール：このクラスは、TorchRecモジュールのシャーディングされたバリアントです。

It has the same input/output as a the regular TorchRec module, but much more optimized and works in a distributed environment. 
通常のTorchRecモジュールと同じ入力/出力を持っていますが、はるかに最適化されており、分散環境で動作します。

* For EmbeddingBagCollection, the sharded variant is ShardedEmbeddingBagCollection 
* EmbeddingBagCollectionの場合、シャーディングされたバリアントはShardedEmbeddingBagCollectionです。

Every TorchRec module has an unsharded and sharded variant. 
すべてのTorchRecモジュールには、シャーディングされていないバリアントとシャーディングされたバリアントがあります。

- The unsharded version is meant to be prototyped and experimented with. 
- シャーディングされていないバージョンは、プロトタイプを作成し、実験するためのものです。

- The sharded version is meant to be used in a distributed environment for distributed training and inference. 
- シャーディングされたバージョンは、分散トレーニングと推論のために分散環境で使用されることを意図しています。

The sharded versions of TorchRec modules, for example EmbeddingBagCollection, will handle everything that is needed for Model Parallelism, such as communication between GPUs for distributing embeddings to the correct GPUs. 
TorchRecモジュールのシャーディングされたバージョン、例えばEmbeddingBagCollectionは、正しいGPUに埋め込みを分配するためのGPU間の通信など、モデル並列性に必要なすべてを処理します。

Refresher of our EmbeddingBagCollection module 
私たちのEmbeddingBagCollectionモジュールのリフレッシャ

```python
from torchrec.distributed.embeddingbag import EmbeddingBagCollectionSharder
from torchrec.distributed.planner import EmbeddingShardingPlanner, Topology
from torchrec.distributed.types import ShardingEnv

# Corresponding sharder for ``EmbeddingBagCollection`` module
# ``EmbeddingBagCollection``モジュールに対応するシャーダー
sharder = EmbeddingBagCollectionSharder()

# ``ProcessGroup`` from torch.distributed initialized 2 cells above
# 上の2つのセルで初期化されたtorch.distributedの``ProcessGroup``
pg = dist.GroupMember.WORLD
assert pg is not None, "Process group is not initialized"
print(f"Process Group: {pg}")
```
```python
ebc
from
torchrec.distributed.embeddingbag
import
EmbeddingBagCollectionSharder
from
torchrec.distributed.planner
import
EmbeddingShardingPlanner
,
Topology
from
torchrec.distributed.types
import
ShardingEnv
```  



# Corresponding sharder for ``EmbeddingBagCollection`` module
```
```
# ``EmbeddingBagCollection``モジュールに対応するシャーダー
```
```md
sharder
=
EmbeddingBagCollectionSharder
()
```
```
sharder
=
EmbeddingBagCollectionSharder
()



# ``ProcessGroup`` from torch.distributed initialized 2 cells above

``ProcessGroup``は、torch.distributedの2つ上のセルで初期化されました。

pg
=
dist
.
GroupMember
.
WORLD

pgはNoneではないことを確認します。
assert
pg
is
not
None
,
"Process group is not initialized"

print
(
f
"Process Group:
{
pg
}
"
)

pgは初期化されていないプロセスグループではありません。
"Process group is not initialized"（プロセスグループは初期化されていません）というメッセージを表示します。

print
(
f
"Process Group:
{
pg
}
"
)



### Planner プランナー

Before we can show how sharding works, we must know about the planner, which helps us determine the best sharding configuration.
シャーディングがどのように機能するかを示す前に、最適なシャーディング構成を決定するのに役立つプランナーについて知っておく必要があります。

Given a number of embedding tables and a number of ranks, there are many different sharding configurations that are possible.
埋め込みテーブルの数とランクの数が与えられると、可能なシャーディング構成は多岐にわたります。

For example, given 2 embedding tables and 2 GPUs, you can:
例えば、2つの埋め込みテーブルと2つのGPUがある場合、次のようにできます。

- Place 1 table on each GPU
- 各GPUに1つのテーブルを配置する
- Place both tables on a single GPU and no tables on the other
- 両方のテーブルを1つのGPUに配置し、もう1つのGPUにはテーブルを配置しない
- Place certain rows and columns on each GPU
- 各GPUに特定の行と列を配置する

Given all of these possibilities, we typically want a sharding configuration that is optimal for performance.
これらの可能性を考慮すると、通常はパフォーマンスに最適なシャーディング構成を望みます。

That is where the planner comes in.
そこでプランナーの出番です。

The planner is able to determine given the number of embedding tables and the number of GPUs, what is the optimal configuration.
プランナーは、埋め込みテーブルの数とGPUの数を考慮して、最適な構成を決定することができます。

Turns out, this is incredibly difficult to do manually, with tons of factors that engineers have to consider to ensure an optimal sharding plan.
実際、これは手動で行うのが非常に難しく、エンジニアが最適なシャーディングプランを確保するために考慮しなければならない要因が多数あります。

Luckily, TorchRec provides an auto planner when the planner is used.
幸いなことに、TorchRecはプランナーが使用されるときに自動プランナーを提供します。

The TorchRec planner:
TorchRecプランナーは以下のことを行います：

- Assesses memory constraints of hardware
- ハードウェアのメモリ制約を評価する
- Estimates compute based on memory fetches as embedding lookups
- メモリフェッチを埋め込みルックアップとして計算を推定する
- Addresses data specific factors
- データ特有の要因に対処する
- Considers other hardware specifics like bandwidth to generate an optimal sharding plan
- 最適なシャーディングプランを生成するために帯域幅などの他のハードウェアの特性を考慮する

In order to take into consideration all these variables, The TorchRec planner can take in various amounts of data for embedding tables, constraints, hardware information, and topology to aid in generating the optimal sharding plan for a model, which is routinely provided across stacks.
これらすべての変数を考慮するために、TorchRecプランナーは埋め込みテーブル、制約、ハードウェア情報、およびトポロジーに関するさまざまなデータを取り込み、スタック全体で定期的に提供されるモデルの最適なシャーディングプランを生成するのを支援します。

To learn more about sharding, see our sharding tutorial.
シャーディングについて詳しく学ぶには、私たちのシャーディングチュートリアルをご覧ください。

# In our case, 1 GPU and compute on CUDA device
# 私たちのケースでは、1つのGPUとCUDAデバイスで計算します
planner=EmbeddingShardingPlanner(topology=Topology(world_size=1,compute_device="cuda",))
# Run planner to get plan for sharding
# プランナーを実行してシャーディングのプランを取得します
plan=planner.collective_plan(ebc,[sharder],pg)
print(f"Sharding Plan generated:{plan}")



# In our case, 1 GPU and compute on CUDA device
私たちのケースでは、1つのGPUとCUDAデバイスで計算します。

planner
=
EmbeddingShardingPlanner
(
topology
=
Topology
(
world_size
=
1
,
compute_device
=
"cuda"
,
)
)
プランナー
=
EmbeddingShardingPlanner
(
トポロジー
=
Topology
(
ワールドサイズ
=
1
,
計算デバイス
=
"cuda"
,
)
)



# Run planner to get plan for sharding シャーディングのための計画を取得するためにプランナーを実行する

plan
= 
planner
.
collective_plan
(
ebc
,
[
sharder
],
pg
)
plan
=
planner
.
collective_plan
(
ebc
,
[
sharder
],
pg
)
print
(
f
"Sharding Plan generated:
{
plan
}
"
)
print
(
f
"シャーディング計画が生成されました:
{
plan
}
"
)



### Planner Result 結果

As you can see above, when running the planner there is quite a bit of output.
上記のように、プランナーを実行するとかなりの出力があります。

We can see a lot of stats being calculated along with where our tables end up being placed.
多くの統計が計算され、テーブルがどこに配置されるかがわかります。

The result of running the planner is a static plan, which can be reused for sharding!
プランナーを実行した結果は静的なプランであり、シャーディングに再利用できます！

This allows sharding to be static for production models instead of determining a new sharding plan everytime.
これにより、毎回新しいシャーディングプランを決定するのではなく、プロダクションモデルのために静的なシャーディングが可能になります。

Below, we use the sharding plan to finally generate ourShardedEmbeddingBagCollection.
以下では、シャーディングプランを使用して最終的にourShardedEmbeddingBagCollectionを生成します。

ShardedEmbeddingBagCollection
ShardedEmbeddingBagCollection

```
# The static plan that was generated
# 生成された静的プラン
planenv=ShardingEnv.from_process_group(pg)
# Shard the ``EmbeddingBagCollection`` module using the ``EmbeddingBagCollectionSharder``
# ``EmbeddingBagCollectionSharder``を使用して``EmbeddingBagCollection``モジュールをシャーディングします
sharded_ebc=sharder.shard(ebc,plan.plan[""],env,torch.device("cuda"))
print(f"Sharded EBC Module:{sharded_ebc}")
```



# The static plan that was generated 生成された静的プラン

plan
環境
=
ShardingEnv
.
from_process_group
(
pg
)



# Shard the ``EmbeddingBagCollection`` module using the ``EmbeddingBagCollectionSharder`` 
``EmbeddingBagCollection``モジュールを``EmbeddingBagCollectionSharder``を使用してシャーディングします。

sharded_ebc = sharder.shard(ebc, plan.plan[""], env, torch.device("cuda"))
sharded_ebc = sharder.shard(ebc, plan.plan[""], env, torch.device("cuda"))

print(f"Sharded EBC Module: {sharded_ebc}")
print(f"シャーディングされたEBCモジュール: {sharded_ebc}")



## GPU Training with LazyAwaitable

## GPUトレーニングとLazyAwaitable

Remember that TorchRec is a highly optimized library for distributed embeddings. 
TorchRecは、分散埋め込みのための高度に最適化されたライブラリであることを思い出してください。

A concept that TorchRec introduces to enable higher performance for training on GPU is a LazyAwaitable. 
TorchRecがGPUでのトレーニングのパフォーマンスを向上させるために導入する概念は、LazyAwaitableです。

You will see LazyAwaitable types as outputs of various sharded TorchRec modules. 
さまざまなシャーディングされたTorchRecモジュールの出力としてLazyAwaitable型を見ることができます。

All a LazyAwaitable type does is delay calculating some result as long as possible, and it does it by acting like an async type. 
LazyAwaitable型が行うことは、可能な限り結果の計算を遅延させることであり、それを非同期型のように振る舞うことで実現します。

```python
from typing import List
from torchrec.distributed.types import LazyAwaitable

# Demonstrate a ``LazyAwaitable`` type:
class ExampleAwaitable(LazyAwaitable[torch.Tensor]):
    def __init__(self, size: List[int]) -> None:
        super().__init__()
        self._size = size

    def _wait_impl(self) -> torch.Tensor:
        return torch.ones(self._size)

awaitable = ExampleAwaitable([3, 2])
awaitable.wait()
kjt = kjt.to("cuda")
output = sharded_ebc(kjt)  # The output of our sharded ``EmbeddingBagCollection`` module is an `Awaitable`?
print(output)
kt = output.wait()  # Now we have our ``KeyedTensor`` after calling ``.wait()``

# If you are confused as to why we have a ``KeyedTensor`` output,
# give yourself a refresher on the unsharded ``EmbeddingBagCollection`` module
print(type(kt))
print(kt.keys())
print(kt.values().shape)  # Same output format as unsharded ``EmbeddingBagCollection``

result_dict = kt.to_dict()
for key, embedding in result_dict.items():
    print(key, embedding.shape)
```
```python
from typing import List
from torchrec.distributed.types import LazyAwaitable
```



# Demonstrate a ``LazyAwaitable`` type: ``LazyAwaitable``型のデモ

class ExampleAwaitable (LazyAwaitable [torch.Tensor]):
クラス ExampleAwaitable (LazyAwaitable [torch.Tensor])：

def __init__(self, size: List[int]) -> None:
def __init__(self, size: List[int]) -> None:
super(). __init__()
super(). __init__()
self._size = size
self._size = size

def _wait_impl(self) -> torch.Tensor:
def _wait_impl(self) -> torch.Tensor:
return torch.ones(self._size)
return torch.ones(self._size)

awaitable = ExampleAwaitable([3, 2])
awaitable = ExampleAwaitable([3, 2])
awaitable.wait()
awaitable.wait()

kjt = kjt.to("cuda")
kjt = kjt.to("cuda")

output = sharded_ebc(kjt)
output = sharded_ebc(kjt)



# The output of our sharded ``EmbeddingBagCollection`` module is an `Awaitable`?
私たちのシャーディングされた ``EmbeddingBagCollection`` モジュールの出力は `Awaitable` ですか？

print
(
output
)
出力を表示します
kt
=
output
.
wait
()
kt = output.wait()



# Now we have our ``KeyedTensor`` after calling ``.wait()``

今、私たちは``.wait()``を呼び出した後に``KeyedTensor``を持っています。



# If you are confused as to why we have a ``KeyedTensor ``output,
# なぜ私たちが ``KeyedTensor ``出力を持っているのか混乱している場合、



# give yourself a refresher on the unsharded ``EmbeddingBagCollection`` module
unsharded ``EmbeddingBagCollection`` モジュールの復習をしましょう。

print
(
type
(
kt
))
print
(
kt
.
keys
())
print
(
kt
.
values
()
.
shape
)
print(
type(kt)
)
print(kt.keys())
print(kt.values().shape)



# Same output format as unsharded ``EmbeddingBagCollection`` 同じ出力形式の非シャーディングの ``EmbeddingBagCollection``

result_dict
=
kt
.
to_dict
()
result_dictを辞書形式に変換します。

for
key
,
embedding
in
result_dict
.
items
():
forループでresult_dictの各アイテムを取得します。

print
(
key
,
embedding
.
shape
)
キーと埋め込みの形状を出力します。



### Anatomy of Sharded TorchRec modules#
### Sharded TorchRecモジュールの解剖

We have now successfully sharded an EmbeddingBagCollection given a sharding plan that we generated! 
私たちは、生成したシャーディングプランに基づいて、EmbeddingBagCollectionを正常にシャーディングしました！

The sharded module has common APIs from TorchRec which abstract away distributed communication/compute amongst multiple GPUs. 
シャーディングされたモジュールは、複数のGPU間の分散通信/計算を抽象化するTorchRecの共通APIを持っています。

In fact, these APIs are highly optimized for performance in training and inference. 
実際、これらのAPIはトレーニングと推論においてパフォーマンスの最適化が図られています。

Below are the three common APIs for distributed training/inference that are provided by TorchRec: 
以下は、TorchRecが提供する分散トレーニング/推論のための3つの一般的なAPIです：

EmbeddingBagCollection
- input_dist: Handles distributing inputs from GPU to GPU. 
- input_dist: GPUからGPUへの入力の分配を処理します。

- lookups: Does the actual embedding lookup in an optimized, batched manner using FBGEMM TBE (more on this later). 
- lookups: FBGEMM TBEを使用して、最適化されたバッチ方式で実際の埋め込みルックアップを行います（詳細は後述）。

- output_dist: Handles distributing outputs from GPU to GPU. 
- output_dist: GPUからGPUへの出力の分配を処理します。

The distribution of inputs and outputs is done through NCCL Collectives, namely All-to-Alls, which is where all GPUs send and receive data to and from one another. 
入力と出力の分配は、NCCL Collectives、すなわちAll-to-Allsを通じて行われ、すべてのGPUが互いにデータを送受信します。

TorchRec interfaces with PyTorch distributed for collectives and provides clean abstractions to the end users, removing the concern for the lower level details. 
TorchRecは、コレクティブのためにPyTorchの分散機能とインターフェースを持ち、エンドユーザーに対してクリーンな抽象化を提供し、低レベルの詳細に対する懸念を取り除きます。

The backwards pass does all of these collectives but in the reverse order for distribution of gradients. 
バックワードパスは、勾配の分配のためにこれらのコレクティブをすべて実行しますが、逆の順序で行います。

input_dist, lookup, and output_dist all depend on the sharding scheme. 
input_dist、lookup、およびoutput_distはすべてシャーディングスキームに依存します。

Since we sharded in a table-wise fashion, these APIs are modules that are constructed by TwPooledEmbeddingSharding. 
私たちはテーブル単位でシャーディングを行ったため、これらのAPIはTwPooledEmbeddingShardingによって構築されたモジュールです。

```
sharded_ebc# Distribute input KJTs to all other GPUs and receive KJTs
```
```
sharded_ebc# 入力KJTを他のすべてのGPUに分配し、KJTを受信します。

```
sharded_ebc._input_dists# Distribute output embeddings to all other GPUs and receive embeddings
```
```
sharded_ebc._output_dists# 出力埋め込みを他のすべてのGPUに分配し、埋め込みを受信します。
``` 



# Distribute input KJTs to all other GPUs and receive KJTs
入力KJTをすべての他のGPUに分配し、KJTを受信します。

sharded_ebc
.
_input_dists



# Distribute output embeddings to all other GPUs and receive embeddings
出力埋め込みをすべての他のGPUに配布し、埋め込みを受信します。

sharded_ebc
.
_output_dists



### Optimizing Embedding Lookups 最適化された埋め込みルックアップ

In performing lookups for a collection of embedding tables, a trivial solution would be to iterate through all thenn.EmbeddingBagsand do a lookup per table. 
埋め込みテーブルのコレクションに対してルックアップを行う際、単純な解決策はすべての `nn.EmbeddingBags` を反復処理し、テーブルごとにルックアップを行うことです。 
This is exactly what the standard, unshardedEmbeddingBagCollectiondoes. 
これは、標準の非シャーディング `EmbeddingBagCollection` が行うことです。 
However, while this solution is simple, it is extremely slow. 
しかし、この解決策は単純である一方で、非常に遅いです。

`nn.EmbeddingBags` 
`EmbeddingBagCollection` 
FBGEMM is a library that provides GPU operators (otherwise known as kernels) that are very optimized. 
FBGEMMは、非常に最適化されたGPUオペレーター（別名カーネル）を提供するライブラリです。 
One of these operators is known as Table Batched Embedding (TBE), provides two major optimizations: 
これらのオペレーターの1つは、テーブルバッチ埋め込み（TBE）として知られ、2つの主要な最適化を提供します。

- Table batching, which allows you to look up multiple embeddings with one kernel call. 
- テーブルバッチ処理は、1回のカーネル呼び出しで複数の埋め込みをルックアップできるようにします。
- Optimizer Fusion, which allows the module to update itself given the canonical pytorch optimizers and arguments. 
- オプティマイザーフュージョンは、モジュールが標準のPyTorchオプティマイザーと引数を考慮して自らを更新できるようにします。

Table batching, which allows you to look up multiple embeddings with one kernel call. 
テーブルバッチ処理は、1回のカーネル呼び出しで複数の埋め込みをルックアップできるようにします。
Optimizer Fusion, which allows the module to update itself given the canonical pytorch optimizers and arguments. 
オプティマイザーフュージョンは、モジュールが標準のPyTorchオプティマイザーと引数を考慮して自らを更新できるようにします。

The ShardedEmbeddingBagCollection uses the FBGEMM TBE as the lookup instead of traditional nn.EmbeddingBags for optimized embedding lookups. 
`ShardedEmbeddingBagCollection` は、最適化された埋め込みルックアップのために従来の `nn.EmbeddingBags` の代わりにFBGEMM TBEをルックアップとして使用します。

`ShardedEmbeddingBagCollection` 
`nn.EmbeddingBags` 
``sharded_ebc._lookups`` 
``sharded_ebc._lookups`` 



### DistributedModelParallel#

DistributedModelParallel
私たちは、単一のEmbeddingBagCollectionをシャーディングすることを探求しました！ 
We have now explored sharding a singleEmbeddingBagCollection! 
EmbeddingBagCollectionSharderを使用して、シャーディングされていないEmbeddingBagCollectionからShardedEmbeddingBagCollectionモジュールを生成することができました。 
We were able to take theEmbeddingBagCollectionSharderand use the unshardedEmbeddingBagCollectionto generate aShardedEmbeddingBagCollectionmodule. 
このワークフローは良好ですが、通常、モデル並列を実装する際には、DistributedModelParallel（DMP）が標準インターフェースとして使用されます。 
This workflow is fine, but typically when implementing model parallel, DistributedModelParallel (DMP) is used as the standard interface. 
モデル（この場合はebc）をDMPでラップすると、次のことが発生します： 
When wrapping your model (in our case ebc), the following will occur:

EmbeddingBagCollection  
EmbeddingBagCollection  
EmbeddingBagCollectionSharder  
EmbeddingBagCollectionSharder  
ShardedEmbeddingBagCollection  
ShardedEmbeddingBagCollection  
ebc  
ebc  

1. モデルをどのようにシャーディングするかを決定します。 
1. Decide how to shard the model. 
DMPは利用可能なシャーダーを収集し、埋め込みテーブル（例えば、EmbeddingBagCollection）をシャーディングする最適な方法の計画を立てます。 
DMP will collect the available sharders and come up with a plan of the optimal way to shard the embedding table(s) (for example, EmbeddingBagCollection). 

2. 実際にモデルをシャーディングします。 
2. Actually shard the model. 
これには、適切なデバイス上の各埋め込みテーブルのメモリを割り当てることが含まれます。 
This includes allocating memory for each embedding table on the appropriate device(s). 

DMPは、静的シャーディングプラン、シャーダーのリストなど、私たちが実験したすべてを取り込みます。 
DMP takes in everything that we’ve just experimented with, like a static sharding plan, a list of sharders, etc. 
ただし、TorchRecモデルをシームレスにシャーディングするためのいくつかの優れたデフォルトも備えています。 
However, it also has some nice defaults to seamlessly shard a TorchRec model. 
このおもちゃの例では、2つの埋め込みテーブルと1つのGPUがあるため、TorchRecは両方を単一のGPUに配置します。 
In this toy example, since we have two embedding tables and one GPU, TorchRec will place both on the single GPU.

```
ebcmodel=torchrec.distributed.DistributedModelParallel(ebc,device=torch.device("cuda"))out=model(kjt)out.wait()modelfromfbgemm_gpu.split_embedding_configsimportEmbOptimType
```
```
ebcmodel=torchrec.distributed.DistributedModelParallel(ebc,device=torch.device("cuda"))out=model(kjt)out.wait()modelfromfbgemm_gpu.split_embedding_configsimportEmbOptimType
```  



### Sharding Best Practices シャーディングのベストプラクティス

Currently, our configuration is only sharding on 1 GPU (or rank), which is trivial: just place all the tables on 1 GPUs memory. 
現在、私たちの構成は1つのGPU（またはランク）でのみシャーディングを行っており、これは簡単です：すべてのテーブルを1つのGPUのメモリに配置するだけです。

However, in real production use cases, embedding tables are typically sharded on hundreds of GPUs, with different sharding methods such as table-wise, row-wise, and column-wise. 
しかし、実際のプロダクションの使用例では、埋め込みテーブルは通常、数百のGPUにシャーディングされ、テーブル単位、行単位、列単位などの異なるシャーディング方法が使用されます。

It is incredibly important to determine a proper sharding configuration (to prevent out of memory issues) while keeping it balanced not only in terms of memory but also compute for optimal performance. 
メモリの観点だけでなく、最適なパフォーマンスのために計算の観点でもバランスを保ちながら、適切なシャーディング構成を決定することが非常に重要です。



### Adding in the Optimizer 最適化器の追加

Remember that TorchRec modules are hyperoptimized for large scale distributed training. 
TorchRecモジュールは、大規模分散トレーニングのためにハイパー最適化されています。

An important optimization is in regards to the optimizer. 
重要な最適化は、最適化器に関するものです。

TorchRec modules provide a seamless API to fuse the backwards pass and optimize step in training, providing a significant optimization in performance and decreasing the memory used, alongside granularity in assigning distinct optimizers to distinct model parameters. 
TorchRecモジュールは、トレーニングにおける逆伝播と最適化ステップを統合するシームレスなAPIを提供し、パフォーマンスの大幅な最適化を実現し、使用するメモリを減少させるとともに、異なるモデルパラメータに異なる最適化器を割り当てる際の粒度を提供します。



## Optimizer Classes 最適化器クラス

TorchRec uses CombinedOptimizer, which contains a collection of KeyedOptimizers. 
TorchRecは、KeyedOptimizersのコレクションを含むCombinedOptimizerを使用します。

A CombinedOptimizer effectively makes it easy to handle multiple optimizers for various sub groups in the model. 
CombinedOptimizerは、モデル内のさまざまなサブグループに対して複数の最適化器を簡単に扱うことができます。

A KeyedOptimizer extends the torch.optim.Optimizer and is initialized through a dictionary of parameters exposes the parameters. 
KeyedOptimizerはtorch.optim.Optimizerを拡張し、パラメータの辞書を通じて初期化され、パラメータを公開します。

Each TBE module in a EmbeddingBagCollection will have its own KeyedOptimizer which combines into one CombinedOptimizer. 
EmbeddingBagCollection内の各TBEモジュールは、それぞれ独自のKeyedOptimizerを持ち、1つのCombinedOptimizerに統合されます。

CombinedOptimizer
CombinedOptimizer

KeyedOptimizers
KeyedOptimizers

CombinedOptimizer
CombinedOptimizer

KeyedOptimizer
KeyedOptimizer

torch.optim.Optimizer
torch.optim.Optimizer

TBE
TBE

EmbeddingBagCollection
EmbeddingBagCollection

KeyedOptimizer
KeyedOptimizer

CombinedOptimizer
CombinedOptimizer



## Fused optimizer in TorchRec#

UsingDistributedModelParallel, theoptimizer is fused, which
UsingDistributedModelParallelを使用すると、オプティマイザが融合され、バックワードでオプティマイザの更新が行われます。
means that the optimizer update is done in the backward. This is an
これはTorchRecとFBGEMMにおける最適化であり、オプティマイザの埋め込み勾配は具現化されず、パラメータに直接適用されます。
optimization in TorchRec and FBGEMM, where the optimizer embedding
This brings significant memory savings as embedding gradients are
勾配は具現化されず、パラメータに直接適用されます。これにより、埋め込み勾配は通常、パラメータ自体のサイズと同じであるため、重要なメモリの節約がもたらされます。
gradients are not materialized and applied directly to the parameters.
DistributedModelParallel
You can, however, choose to make the optimizerdensewhich does not
ただし、オプティマイザをdenseにすることを選択でき、この最適化を適用せず、埋め込み勾配を検査したり、必要に応じて計算を適用したりできます。
apply this optimization and let’s you inspect the embedding gradients or
A dense optimizer in this case would be yourcanonical PyTorch model training loop with
この場合、denseオプティマイザは、標準的なPyTorchモデルのトレーニングループにおけるオプティマイザになります。
optimizer.
dense
Once the optimizer is created throughDistributedModelParallel, you
一度DistributedModelParallelを通じてオプティマイザが作成されると、TorchRec埋め込みモジュールに関連付けられていない他のパラメータのためにオプティマイザを管理する必要があります。
still need to manage an optimizer for the other parameters not
associated with TorchRec embedding modules. To find the other
他のパラメータを見つけるには、
parameters,
usein_backward_optimizer_filter(model.named_parameters()).
in_backward_optimizer_filter(model.named_parameters())を使用します。
Apply an optimizer to those parameters as you would a normal Torch
それらのパラメータに通常のTorchオプティマイザのようにオプティマイザを適用し、このオプティマイザとmodel.fused_optimizerを組み合わせて、トレーニングループで使用できるCombinedOptimizerを作成します。
optimizer and combine this and themodel.fused_optimizerinto one
CombinedOptimizer that you can use in your training loop tozero_gradandstepthrough.
CombinedOptimizerを作成し、トレーニングループでzero_gradおよびstepを通じて使用します。
DistributedModelParallel
in_backward_optimizer_filter(model.named_parameters())
model.fused_optimizer
CombinedOptimizer
zero_grad
step



## Adding an Optimizer to EmbeddingBagCollection

EmbeddingBagCollection
EmbeddingBagCollectionにオプティマイザを追加します。
We will do this in two ways, which are equivalent, but give you options depending on your preferences:
これを2つの方法で行います。どちらも同等ですが、あなたの好みに応じて選択肢を提供します。
1. Passing optimizer kwargs through fused_params in sharder.
1. sharderのfused_paramsを通じてオプティマイザのキーワード引数を渡すこと。
2. Through apply_optimizer_in_backward, which converts the optimizer parameters to fused_params to pass to the TBE in the EmbeddingBagCollection or EmbeddingCollection.
2. apply_optimizer_in_backwardを通じて、オプティマイザのパラメータをfused_paramsに変換し、EmbeddingBagCollectionまたはEmbeddingCollectionのTBEに渡します。

Passing optimizer kwargs through fused_params in sharder.
sharderのfused_paramsを通じてオプティマイザのキーワード引数を渡すこと。
fused_params
fused_params
Through apply_optimizer_in_backward, which converts the optimizer parameters to fused_params to pass to the TBE in the EmbeddingBagCollection or EmbeddingCollection.
apply_optimizer_in_backwardを通じて、オプティマイザのパラメータをfused_paramsに変換し、EmbeddingBagCollectionまたはEmbeddingCollectionのTBEに渡します。
apply_optimizer_in_backward
apply_optimizer_in_backward
fused_params
fused_params
TBE
TBE
EmbeddingBagCollection
EmbeddingBagCollection
EmbeddingCollection
EmbeddingCollection

# Option 1: Passing optimizer kwargs through fused parameters
# オプション1: fused parametersを通じてオプティマイザのキーワード引数を渡す

from torchrec.optim.optimizers import in_backward_optimizer_filter
# We initialize the sharder with fused_params={"optimizer":EmbOptimType.EXACT_ROWWISE_ADAGRAD,"learning_rate":0.02,"eps":0.002,}
# fused_params={"optimizer":EmbOptimType.EXACT_ROWWISE_ADAGRAD,"learning_rate":0.02,"eps":0.002,}でsharderを初期化します。
# Initialize sharder with ``fused_params``
# ``fused_params``でsharderを初期化します。
sharder_with_fused_params = EmbeddingBagCollectionSharder(fused_params=fused_params)
# We'll use same plan and unsharded EBC as before but this time with our new sharder
# 前回と同じプランと非分割EBCを使用しますが、今回は新しいsharderを使用します。
sharded_ebc_fused_params = sharder_with_fused_params.shard(ebc, plan.plan[""], env, torch.device("cuda"))
# Looking at the optimizer of each, we can see that the learning rate changed, which indicates our optimizer has been applied correctly.
# 各オプティマイザを見てみると、学習率が変わったことがわかります。これは、オプティマイザが正しく適用されたことを示しています。
# If seen, we can also look at the TBE logs of the cell to see that our new optimizer is indeed being applied
# もし見られたら、セルのTBEログを見て、新しいオプティマイザが実際に適用されていることを確認できます。
print(f"Original Sharded EBC fused optimizer:{sharded_ebc.fused_optimizer}")
print(f"Sharded EBC with fused parameters fused optimizer:{sharded_ebc_fused_params.fused_optimizer}")
print(f"Type of optimizer:{type(sharded_ebc_fused_params.fused_optimizer)}")

import copy
from torch.distributed.optim import (_apply_optimizer_in_backward as apply_optimizer_in_backward,)
# Option 2: Applying optimizer through apply_optimizer_in_backward
# オプション2: apply_optimizer_in_backwardを通じてオプティマイザを適用する
# Note: we need to call apply_optimizer_in_backward on unsharded model first and then shard it
# 注意: 最初に非分割モデルでapply_optimizer_in_backwardを呼び出し、その後に分割する必要があります。
# We can achieve the same result as we did in the previous
# 前回と同じ結果を得ることができます。
ebc_apply_opt = copy.deepcopy(ebc)
optimizer_kwargs = {"lr": 0.5}
for name, param in ebc_apply_opt.named_parameters():
    print(f"{name=}")
    apply_optimizer_in_backward(torch.optim.SGD, [param], optimizer_kwargs)

sharded_ebc_apply_opt = sharder.shard(ebc_apply_opt, plan.plan[""], env, torch.device("cuda"))
# Now when we print the optimizer, we will see our new learning rate, you can verify momentum through the TBE logs as well if outputted
# これでオプティマイザを印刷すると、新しい学習率が表示されます。出力されていれば、TBEログを通じてモーメンタムを確認できます。
print(sharded_ebc_apply_opt.fused_optimizer)
print(type(sharded_ebc_apply_opt.fused_optimizer))

# We can also check through the filter other parameters that aren't associated with the "fused" optimizer(s)
# また、"fused"オプティマイザに関連付けられていない他のパラメータをフィルタを通じて確認できます。
# Practically, just non TorchRec module parameters. Since our module is just a TorchRec EBC
# 実際には、TorchRecモジュールパラメータ以外のものです。私たちのモジュールは単にTorchRec EBCです。
print("Non Fused Model Parameters:")
print(dict(in_backward_optimizer_filter(sharded_ebc_fused_params.named_parameters())).keys())

# Here we do a dummy backwards call and see that parameter updates for fused
# ここでダミーのバックワード呼び出しを行い、fusedオプティマイザのパラメータ更新が行われることを確認します。
ebc_output = sharded_ebc_fused_params(kjt).wait().values()
loss = torch.sum(torch.ones_like(ebc_output) - ebc_output)
print(f"First Iteration Loss:{loss}")
loss.backward()
ebc_output = sharded_ebc_fused_params(kjt).wait().values()
loss = torch.sum(torch.ones_like(ebc_output) - ebc_output)
# We don't call an optimizer.step(), so for the loss to have changed here,
# オプティマイザのstep()を呼び出さないので、ここで損失が変わったということは、
# that means that the gradients were somehow updated, which is what the
# fused optimizer automatically handles for us
# 勾配が何らかの形で更新されたことを意味します。これはfusedオプティマイザが自動的に処理します。
print(f"Second Iteration Loss:{loss}")



# Option 1: Passing optimizer kwargs through fused parameters
オプション1: 融合されたパラメータを通じてオプティマイザのキーワード引数を渡す

from
torchrec.optim.optimizers
import
in_backward_optimizer_filter
から
torchrec.optim.optimizersをインポートし、
in_backward_optimizer_filterをインポートします。



# We initialize the sharder with
sharderを次のように初期化します。

fused_params
=
{
"optimizer"
:
EmbOptimType
.
EXACT_ROWWISE_ADAGRAD
,
"learning_rate"
:
0.02
,
"eps"
:
0.002
,
}



# Initialize sharder with ``fused_params`` ``fused_params``でシャーダーを初期化

sharder_with_fused_params
=
EmbeddingBagCollectionSharder
(
fused_params
=
fused_params
)



# We'll use same plan and unsharded EBC as before but this time with our new sharder
同じプランと非分割EBCを以前と同様に使用しますが、今回は新しいシャーダーを使用します。

sharded_ebc_fused_params
=
sharder_with_fused_params
.
shard
(
ebc
,
plan
.
plan
[
""
],
env
,
torch
.
device
(
"cuda"
)
)



# Looking at the optimizer of each, we can see that the learning rate changed, which indicates our optimizer has been applied correctly.
各オプティマイザを見てみると、学習率が変化していることがわかります。これは、私たちのオプティマイザが正しく適用されていることを示しています。



# If seen, we can also look at the TBE logs of the cell to see that our new optimizer is indeed being applied
もし確認できれば、セルのTBEログを見て、私たちの新しいオプティマイザが実際に適用されていることを確認できます。

print
(
f
"Original Sharded EBC fused optimizer:
{
sharded_ebc
.
fused_optimizer
}
"
)
print
(
f
"Sharded EBC with fused parameters fused optimizer:
{
sharded_ebc_fused_params
.
fused_optimizer
}
"
)
print
(
f
"Type of optimizer:
{
type
(
sharded_ebc_fused_params
.
fused_optimizer
)
}
"
)
print
(
f
"元のSharded EBC融合オプティマイザ:
{
sharded_ebc
.
fused_optimizer
}
"
)
print
(
f
"融合パラメータを持つSharded EBC融合オプティマイザ:
{
sharded_ebc_fused_params
.
fused_optimizer
}
"
)
print
(
f
"オプティマイザのタイプ:
{
type
(
sharded_ebc_fused_params
.
fused_optimizer
)
}
"
)

import
copy
from
torch.distributed.optim
import
(
_apply_optimizer_in_backward
as
apply_optimizer_in_backward
,
)
import
copy
from
torch.distributed.optim
import
(
_apply_optimizer_in_backward
as
apply_optimizer_in_backward
,
)



# Option 2: Applying optimizer through apply_optimizer_in_backward オプション2: apply_optimizer_in_backwardを通じたオプティマイザの適用



# Note: we need to call apply_optimizer_in_backward on unsharded model first and then shard it
# 注: 最初にunshardedモデルでapply_optimizer_in_backwardを呼び出し、その後shardします



# We can achieve the same result as we did in the previous
# 前回と同じ結果を達成することができます。

ebc_apply_opt
=
copy
.
deepcopy
(
ebc
)
# ebc_apply_opt = copy.deepcopy(ebc)

optimizer_kwargs
=
{
"lr"
:
0.5
}
# optimizer_kwargs = {"lr": 0.5}

for
name
,
param
in
ebc_apply_opt
.
named_parameters
():
# for name, param in ebc_apply_opt.named_parameters():

print
(
f
"
{
name
=}
"
)
# print(f"{name=}")

apply_optimizer_in_backward
(
torch
.
optim
.
SGD
,
[
param
],
optimizer_kwargs
)
# apply_optimizer_in_backward(torch.optim.SGD, [param], optimizer_kwargs)

sharded_ebc_apply_opt
=
sharder
.
shard
(
ebc_apply_opt
,
plan
.
plan
[
""
],
env
,
torch
.
device
(
"cuda"
)
)
# sharded_ebc_apply_opt = sharder.shard(ebc_apply_opt, plan.plan[""], env, torch.device("cuda"))



# Now when we print the optimizer, we will see our new learning rate, you can verify momentum through the TBE logs as well if outputted
最初にオプティマイザを印刷すると、新しい学習率が表示されます。また、出力されている場合はTBEログを通じてモーメンタムを確認することもできます。

print
(
sharded_ebc_apply_opt
.
fused_optimizer
)
print
(
type
(
sharded_ebc_apply_opt
.
fused_optimizer
))



# We can also check through the filter other parameters that aren't associated with the "fused" optimizer(s)
私たちはまた、"fused" オプティマイザに関連付けられていない他のパラメータをフィルタを通じて確認することができます。



# Practically, just non TorchRec module parameters. 
実際には、TorchRecモジュールのパラメータではありません。

Since our module is just a TorchRec EBC
私たちのモジュールは単なるTorchRec EBCであるためです。



# there are no other parameters that aren't associated with TorchRec
# TorchRecに関連付けられていない他のパラメータはありません

print
(
"Non Fused Model Parameters:"
)
print
(
dict
(
in_backward_optimizer_filter
(
sharded_ebc_fused_params
.
named_parameters
())
)
.
keys
()
)



# Here we do a dummy backwards call and see that parameter updates for fused
ここでは、ダミーの逆伝播呼び出しを行い、融合されたパラメータの更新を確認します。



# optimizers happen as a result of the backward pass
# 最適化手法は逆伝播の結果として発生します

ebc_output
=
sharded_ebc_fused_params
(
kjt
)
.
wait
()
.
values
()
# ebc_outputはsharded_ebc_fused_params(kjt)の待機結果の値です

loss
=
torch
.
sum
(
torch
.
ones_like
(
ebc_output
)
-
ebc_output
)
# lossはebc_outputと同じ形状の1のテンソルからebc_outputを引いたものの合計です

print
(
f
"First Iteration Loss:
{
loss
}
"
)
# 最初のイテレーションの損失を出力します

loss
.
backward
()
# 損失の逆伝播を行います

ebc_output
=
sharded_ebc_fused_params
(
kjt
)
.
wait
()
.
values
()
# 再度ebc_outputを更新します

loss
=
torch
.
sum
(
torch
.
ones_like
(
ebc_output
)
-
ebc_output
)
# 再度損失を計算します



# We don't call an optimizer.step(), so for the loss to have changed here,
私たちはoptimizer.step()を呼び出さないので、ここで損失が変化するためには、



# that means that the gradients were somehow updated, which is what the
それは、勾配が何らかの形で更新されたことを意味します。これは、何を示していますか。



# fused optimizer automatically handles for us
fused optimizerは自動的に私たちのために処理します。

print
(
f
"Second Iteration Loss:
{
loss
}
"
)
print
(
f
"第2イテレーションの損失:
{
loss
}
"
)



## Conclusion 結論

In this tutorial, you have done training a distributed RecSys model
このチュートリアルでは、分散RecSysモデルのトレーニングを行いました。

If you are interested in the inference theTorchRec repohas a
full example of how to run the TorchRec in Inference mode.
推論に興味がある場合、TorchRecリポジトリには、TorchRecを推論モードで実行する方法の完全な例があります。

For more information, please see ourdlrmexample, which includes multinode training on the Criteo 1TB
dataset using the methods described inDeep Learning Recommendation Model
for Personalization and Recommendation Systems.
詳細については、Deep Learning Recommendation Model for Personalization and Recommendation Systemsで説明されている方法を使用して、Criteo 1TBデータセットでのマルチノードトレーニングを含むour dlrm exampleをご覧ください。

DownloadJupyternotebook:torchrec_intro_tutorial.ipynb
Jupyterノートブックをダウンロード: torchrec_intro_tutorial.ipynb

Download
Jupyter
notebook:
torchrec_intro_tutorial.ipynb
Jupyterノートブックをダウンロード: torchrec_intro_tutorial.ipynb

DownloadPythonsourcecode:torchrec_intro_tutorial.py
Pythonソースコードをダウンロード: torchrec_intro_tutorial.py

Download
Python
source
code:
torchrec_intro_tutorial.py
Pythonソースコードをダウンロード: torchrec_intro_tutorial.py

Downloadzipped:torchrec_intro_tutorial.zip
圧縮ファイルをダウンロード: torchrec_intro_tutorial.zip

Download
zipped:
torchrec_intro_tutorial.zip
圧縮ファイルをダウンロード: torchrec_intro_tutorial.zip

★
★
★
★
★
previous
Pendulum: Writing your environment and transforms with TorchRL
前の項目: Pendulum: TorchRLを使用した環境と変換の作成

next
Exploring TorchRec sharding
次の項目: TorchRecのシャーディングの探求

© Copyright 2024, PyTorch.
© 2024年、PyTorchの著作権。

Built with thePyData Sphinx Theme0.15.4.
PyData Sphinxテーマ0.15.4で構築。

previous
Pendulum: Writing your environment and transforms with TorchRL
前の項目: Pendulum: TorchRLを使用した環境と変換の作成

next
Exploring TorchRec sharding
次の項目: TorchRecのシャーディングの探求

- Install DependenciesEmbeddingsEmbeddings in RecSysEmbeddings in PyTorch
- 依存関係のインストール
- Embeddings
- RecSysにおける埋め込み
- PyTorchにおける埋め込み
- Embeddings
- RecSysにおける埋め込み
- PyTorchにおける埋め込み
- PyTorchにおける埋め込み
- FromEmbeddingBagtoEmbeddingBagCollectionTorchRec Input/Output Data TypesDistributed Training and ShardingDistributed EmbeddingsShardingSharded ModulesPlannerPlanner Result
- EmbeddingBagからEmbeddingBagCollectionへ
- TorchRecの入出力データ型
- 分散トレーニングとシャーディング
- 分散埋め込み
- シャーディング
- シャーディングされたモジュール
- プランナー
- プランナーの結果
- FromEmbeddingBagtoEmbeddingBagCollection
- EmbeddingBagからEmbeddingBagCollectionへ
- TorchRecの入出力データ型
- 分散トレーニングとシャーディング
- 分散埋め込み
- シャーディング
- シャーディングされたモジュール
- プランナー
- プランナーの結果
- GPU Training withLazyAwaitableAnatomy of Sharded TorchRec modulesOptimizing Embedding LookupsDistributedModelParallelSharding Best PracticesAdding in the Optimizer
- レイジーアウェイタブルを使用したGPUトレーニング
- シャーディングされたTorchRecモジュールの構造
- 埋め込みルックアップの最適化
- 分散モデル並列
- シャーディングのベストプラクティス
- オプティマイザーの追加
- Anatomy of Sharded TorchRec modules
- シャーディングされたTorchRecモジュールの構造
- Optimizing Embedding Lookups
- 埋め込みルックアップの最適化
- DistributedModelParallel
- 分散モデル並列
- Sharding Best Practices
- シャーディングのベストプラクティス
- Adding in the Optimizer
- オプティマイザーの追加
- Optimizer Classes
- オプティマイザークラス
- Fused optimizer in TorchRec
- TorchRecにおける融合オプティマイザー
- Adding an Optimizer toEmbeddingBagCollection
- EmbeddingBagCollectionへのオプティマイザーの追加
- Conclusion
- 結論
- Embeddings
- 埋め込み
- Embeddings in RecSysEmbeddings in PyTorch
- RecSysにおける埋め込み
- Embeddings in PyTorch
- PyTorchにおける埋め込み
- Embeddings in PyTorch
- PyTorchにおける埋め込み
- FromEmbeddingBagtoEmbeddingBagCollection
- EmbeddingBagからEmbeddingBagCollectionへ
- TorchRec Input/Output Data Types
- TorchRecの入出力データ型
- Distributed Training and Sharding
- 分散トレーニングとシャーディング
- Distributed Embeddings
- 分散埋め込み
- Sharding
- シャーディング
- Sharded Modules
- シャーディングされたモジュール
- Planner
- プランナー
- Planner Result
- プランナーの結果
- EmbeddingBag
- EmbeddingBag
- EmbeddingBagCollection
- EmbeddingBagCollection
- LazyAwaitable
- レイジーアウェイタブル
- Anatomy of Sharded TorchRec modules
- シャーディングされたTorchRecモジュールの構造
- Optimizing Embedding Lookups
- 埋め込みルックアップの最適化
- DistributedModelParallel
- 分散モデル並列
- Sharding Best Practices
- シャーディングのベストプラクティス
- Adding in the Optimizer
- オプティマイザーの追加
- DistributedModelParallel
- 分散モデル並列
- EmbeddingBagCollection
- EmbeddingBagCollection
- torchao
- torchao
- torchrec
- torchrec
- torchft
- torchft
- TorchCodec
- TorchCodec
- torchvision
- torchvision
- ExecuTorch
- ExecuTorch
- PyTorch on XLA Devices
- XLAデバイス上のPyTorch
- Scripts loaded after <body> so the DOM is not blocked
- <body>の後に読み込まれたスクリプトにより、DOMがブロックされることはありません



## Docs ドキュメント

Access comprehensive developer documentation for PyTorch
PyTorchの包括的な開発者ドキュメントにアクセスします。



## Tutorials チュートリアル

Get in-depth tutorials for beginners and advanced developers
初心者と上級開発者のための詳細なチュートリアルを入手してください。



## Resources リソース

Find development resources and get your questions answered
開発リソースを見つけ、質問に答えてもらいましょう。

Stay in touch for updates, event info, and the latest news
最新情報、イベント情報、ニュースを受け取るために連絡を取り合いましょう。

By submitting this form, I consent to receive marketing emails from the LF and its projects regarding their events, training, research, developments, and related announcements. 
このフォームを送信することにより、LFおよびそのプロジェクトからイベント、トレーニング、研究、開発、および関連する発表に関するマーケティングメールを受け取ることに同意します。

I understand that I can unsubscribe at any time using the links in the footers of the emails I receive. 
受け取ったメールのフッターにあるリンクを使用して、いつでも購読を解除できることを理解しています。

Privacy Policy
プライバシーポリシー

By submitting this form, I consent to receive marketing emails from the LF and its projects regarding their events, training, research, developments, and related announcements. 
このフォームを送信することにより、LFおよびそのプロジェクトからイベント、トレーニング、研究、開発、および関連する発表に関するマーケティングメールを受け取ることに同意します。

I understand that I can unsubscribe at any time using the links in the footers of the emails I receive. 
受け取ったメールのフッターにあるリンクを使用して、いつでも購読を解除できることを理解しています。

Privacy Policy.
プライバシーポリシー。

-
-
-
-
-
-

© PyTorch. Copyright © The Linux Foundation®. All rights reserved. 
© PyTorch。著作権 © The Linux Foundation®。全著作権所有。

The Linux Foundation has registered trademarks and uses trademarks. 
The Linux Foundationは登録商標を持ち、商標を使用しています。

For more information, including terms of use, privacy policy, and trademark usage, please see our Policies page. 
利用規約、プライバシーポリシー、商標の使用に関する詳細については、ポリシーページをご覧ください。

Trademark Usage.
商標の使用。

Privacy Policy.
プライバシーポリシー。

To analyze traffic and optimize your experience, we serve cookies on this site. 
トラフィックを分析し、体験を最適化するために、このサイトでクッキーを提供します。

By clicking or navigating, you agree to allow our usage of cookies. 
クリックまたはナビゲートすることにより、私たちのクッキーの使用を許可することに同意します。

As the current maintainers of this site, Facebook’s Cookies Policy applies. 
このサイトの現在の管理者として、Facebookのクッキーポリシーが適用されます。

Learn more, including about available controls: Cookies Policy.
詳細を学ぶには、利用可能なコントロールについても含めて、クッキーポリシーをご覧ください。

© Copyright 2024, PyTorch.
© 著作権 2024, PyTorch。

Created using Sphinx 7.2.6.
Sphinx 7.2.6を使用して作成されました。

Built with the PyData Sphinx Theme 0.15.4.
PyData Sphinxテーマ 0.15.4で構築されました。
