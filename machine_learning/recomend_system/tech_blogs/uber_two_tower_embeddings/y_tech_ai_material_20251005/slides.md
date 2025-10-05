---
marp: true
theme: default
paginate: true
header: 'RecSysの実運用で人気なTwo-Towerモデル! と言ってもいろんなバリエーションがありそうだなぁと思った話'
footer: 'Y-tech AI勉強会 2025/10/05 モーリタ'
---

# RecSysの実運用で人気なTwo-Towerモデル! と言ってもいろんなバリエーションがありそうだなぁと思った話

---

<!-- _class: lead -->

# はじめに

---

## なんで今回このトピックを話したいんだっけ??

- [ ] TODO: 発表の動機を追加
  - 社内での活用事例
  - 最近の研究動向
  - 実装時の知見共有
  - など

---

<!-- 

章立てのアウトライン

- なぜ本トピックを話したいんだっけ??
- はじめに: そもそもTwo-towerモデルって??なんで人気なんだっけ??
  - RecSysの実運用でTwo-Towerモデルが結構人気
    - Googleさん、Uberさん、リクルートさん、ZOZOさん、日経さん、etc...
  - Two-Towerモデルってざっくり何だっけ??
    - 2つの独立したニューラルネットワーク（タワー）を用いた推薦モデル。
    - NLP(自然言語処理)の分野におけるdual encoderモデルを推薦・検索タスクに応用したもの。
  - なんでRecSysの実運用で人気なんだっけ??
    - NNの恩恵を受けつつ、推論時のスケーラビリティと処理速度を両立させやすい。
    - 
- 主張1: Two-towerのネットワーク構造のバリエーションが色々ある話
  - Two-tower型アーキテクチャの基本構成
    - User Tower (検索分野ではQuery Tower)
    - Item Tower
    - Predictionモジュール
  - タワーのバリエーション
    - 基本的には、だんだんと出力層にかけて次元が小さくなっていくMLP的な構造 -> これが「タワー」と呼ばれる所以。
    - 特にnext-item predictionタスクを重視したRecSysの場合は、タワーにAttentionやRNNを組み込むバリエーションもある。
    - また、両タワーの中間部分のパラメータを共通化してる事例もある(Uberさんの事例など)。
  - predictionモジュールのバリエーション
    - おそらく最も一般的なのは、内積(dot-product)でのスコア計算
    - でも内積だけじゃない! 軽量モデルを採用することもあり! (Youtubeにおけるrerankingフェーズでのtwo-towerモデルの活用事例を紹介)
- 主張2: Two-towerの学習方法のバリエーションが色々ある話
  - そもそもRecSysタスクを定式化してみよう
  - タスクの性質ゆえに代理学習問題(surrogate learning problem)も結構採用されがち!
  - 回帰ベースのアプローチ: 予測タスクとして学習する!
  - contrastive learningベースのアプローチ(回帰ベースの一種?)
  - 勾配ベースのアプローチ: 累積報酬最大化タスクとして学習する!
- おわりに: まとめ
  - なぜTwo-TowerモデルがRecSysの実運用で人気なのか -> NNの恩恵を受けつつ、スケーラビリティと推論速度を両立させやすいから!
  - Two-Towerモデルの構造のバリエーションが色々ある話 -> 色々あるが、とりあえずまずはMLP的なタワー、内積ベースのpredictionモジュールから始めて良さそう!
  - Two-Towerモデルの学習方法のバリエーションが色々ある話 -> 自社のユースケース(フェーズの違い、トラフィック量、過去に収集した観測データの性質, RecSysで改善したい指標)などに応じて、試行錯誤しつつ有効なアプローチを選びたい。
  - 思ったこと: Two-tower (に限らずNN系のアプローチ) の自由度の高さは、デメリットともメリットとも言える。
      - -> 「色々選択しないといけなくて大変」とも取れるが、「自社のユースケースに合わせて自由に設計できる」とも取れる。特にモデルアーキテクチャや目的関数の設計は、DS・ML・MLOpsエンジニアの腕の見せ所とも言えそう...!!
      - (そもそも多様なNNアーキテクチャの中でTwo-towerを選ぶ意思決定をすること、その理由をきちんと言語化して納得できる説明ができること、もMLOpsを司るエンジニアとして腕の見せどころのはず...!:thinking:)
-->

## 今日のアウトライン

1. はじめに: そもそもTwo-towerモデルって??なんで人気なんだっけ??
   - RecSysの実運用でTwo-Towerモデルが結構人気
   - Two-Towerモデルってざっくり何だっけ??
   - なんでRecSysの実運用で人気なんだっけ??
2. 主張1: Two-towerのネットワーク構造のバリエーションが色々ある話
   - Two-tower型アーキテクチャの基本構成
   - タワーのバリエーション
   - predictionモジュールのバリエーション
3. 主張2: Two-towerの学習方法のバリエーションが色々ある話
   - そもそもRecSysタスクを定式化してみよう
   - タスクの性質ゆえに代理学習問題(surrogate learning problem)も結構採用されがち!
4. まとめ
   - 

---

## Two-Towerモデルとは? なぜ推薦システムで重要なのか?

### Two-Towerモデルとは

- **2つの独立したニューラルネットワーク（タワー）** を用いた推薦モデル
  - User Tower: ユーザー特徴を低次元ベクトルに変換
  - Item Tower: アイテム特徴を低次元ベクトルに変換
- 2つのタワーで生成された埋め込みベクトルの**類似度（内積など）**でスコアリング

### なぜ重要なのか

- 大規模な候補生成（Candidate Generation）における**スケーラビリティ**と**推論速度**の両立
- アイテム埋め込みの**事前計算**とANN検索による高速化
- [ ] TODO: その他の重要性を追加

---

## 先に参考文献を紹介

1. Google Play事例 (2020): [Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations](https://storage.googleapis.com/gweb-research2023-media/pubtools/6090.pdf)
2. Uber事例 (2023): [Innovative Recommendation Applications Using Two Tower Embeddings](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
3. [ ] TODO: その他の参考文献を追加

---

<!-- _class: lead -->

# 本論: Two-Towerモデルのバリエーション

---

## 今日お話しすること

以下の2点について説明します:

1. **モデル構造のバリエーション**
   - タワーの基本構造
   - ネットワークアーキテクチャ
   - 特徴量エンジニアリング
   - 埋め込みベクトルの次元設計

2. **学習方法のバリエーション**
   - 損失関数の選択
   - ネガティブサンプリング戦略
   - 学習の工夫とテクニック
   - 評価指標

---

<!-- _class: lead -->

# 主張1: モデル構造のバリエーション

---

## タワーの基本構造

### シンプルなMLP (Multi-Layer Perceptron)

```
Input Features
     ↓
Dense Layer 1 + Activation
     ↓
Dense Layer 2 + Activation
     ↓
   ...
     ↓
Embedding Layer
```

- 最もシンプルで実装しやすい構造
- [ ] TODO: MLPの特徴を追加

---

## タワー内のネットワークアーキテクチャのバリエーション

### パターン1: シンプルなDNN

- [ ] TODO: 基本的なDNNの説明

### パターン2: Residual Connection

- [ ] TODO: ResNetライクな構造の説明

### パターン3: Attention Mechanism

- [ ] TODO: Self-Attentionを組み込んだ構造の説明

---

## 特徴量エンジニアリングのバリエーション

### User Tower側の特徴量

- **カテゴリカル特徴**: ユーザーID、年齢層、性別など
- **数値特徴**: [ ] TODO: 数値特徴の例と正規化方法
- **シーケンシャル特徴**: ユーザー行動履歴など

### Item Tower側の特徴量

- **カテゴリカル特徴**: アイテムID、カテゴリなど
- **テキスト特徴**: タイトル、説明文の埋め込み
- **画像特徴**: CNNで抽出した特徴

---

## 埋め込みベクトルの次元設計

### 次元数の選択

- トレードオフの考慮
  - **表現力** vs **計算コスト**
  - **過学習のリスク**
- [ ] TODO: 具体的な次元数の選び方

### 正規化

- L2正規化の重要性
  - 埋め込みベクトルのノルムを揃える
  - 類似度計算の安定化
- [ ] TODO: その他の正規化手法

---

## 実装例 (PyTorch)

```python
import torch
import torch.nn as nn

class TowerModel(nn.Module):
    def __init__(self, input_dim, hidden_dims, embedding_dim):
        super().__init__()
        # TODO: 実装例を追加
        pass

    def forward(self, x):
        # TODO: forward処理を追加
        pass
```

---

<!-- _class: lead -->

# 主張2: 学習方法のバリエーション

---

## 損失関数の選択

### Pointwise Loss: Binary Cross Entropy

```python
score = torch.sigmoid(torch.sum(user_emb * item_emb, dim=1))
loss = F.binary_cross_entropy(score, label)
```

- [ ] TODO: 特徴とユースケース

### Pairwise Loss: BPR (Bayesian Personalized Ranking)

```python
pos_score = torch.sum(user_emb * pos_item_emb, dim=1)
neg_score = torch.sum(user_emb * neg_item_emb, dim=1)
loss = -torch.log(torch.sigmoid(pos_score - neg_score))
```

- [ ] TODO: 特徴とユースケース

---

## 損失関数の選択 (続き)

### Listwise Loss: Softmax Cross Entropy

```python
# バッチ内のすべてのアイテムを候補とする
scores = torch.matmul(user_emb, item_emb.T)  # [batch, batch]
loss = F.cross_entropy(scores, labels)
```

- [ ] TODO: 特徴とユースケース

---

## ネガティブサンプリング戦略

### なぜネガティブサンプリングが必要か

- 全アイテムでSoftmaxを計算するコストが膨大
  - 数百万〜数億のアイテムに対して計算不可能
- [ ] TODO: 計算量の問題の詳細

### サンプリング手法

1. **ランダムサンプリング**: 一様分布からサンプリング
2. **人気度ベースサンプリング**: アイテム頻度に基づくサンプリング
3. **In-Batch Negative**: バッチ内の他のアイテムをネガティブとして利用

---

## バッチネガティブサンプリング

### 仕組み

```python
# バッチサイズ B の場合
user_emb: [B, D]  # B個のユーザー埋め込み
item_emb: [B, D]  # B個のアイテム埋め込み

# すべてのユーザー-アイテムペアのスコアを計算
scores = torch.matmul(user_emb, item_emb.T)  # [B, B]

# 対角成分がポジティブペア、それ以外がネガティブペア
```

### メリット

- 追加の計算コストが少ない
- バッチサイズを大きくすることでネガティブサンプル数を増やせる
- [ ] TODO: その他のメリット

---

## ハードネガティブマイニング

### 動機

- 簡単すぎるネガティブサンプルは学習に寄与しない
- スコアが高い（誤分類しやすい）ネガティブサンプルを優先的に学習

### 手法

- **オンラインマイニング**: 学習中に動的に選択
- **オフラインマイニング**: 事前に選択してデータセットに含める
- [ ] TODO: 具体的な実装方法

---

## 学習の工夫とテクニック

### Warm-up戦略

- 学習率のウォームアップ
- [ ] TODO: ウォームアップの効果

### 温度パラメータ (Temperature Scaling)

```python
scores = torch.matmul(user_emb, item_emb.T) / temperature
```

- 温度パラメータの役割
  - スコア分布の調整
  - [ ] TODO: 最適な温度の選び方

---

## 正則化とバイアスへの対処

### 正則化

- **L2正則化**: 埋め込みベクトルの過学習を防ぐ
- **Dropout**: タワー内でのDropout

### バイアスへの対処

- **Selection Bias**: 観測データのバイアス
  - [ ] TODO: IPS (Inverse Propensity Score) の利用
- **Position Bias**: 表示位置によるバイアス
  - [ ] TODO: 対処方法

---

## 評価指標

### オフライン評価

- **Recall@K**: 上位K件にポジティブアイテムが含まれる割合
- **Precision@K**: 上位K件のうちポジティブアイテムの割合
- **NDCG, MRR**: [ ] TODO: 説明を追加

### オンライン評価

- **CTR (Click-Through Rate)**: クリック率
- **コンバージョン率**: 購入率など
- **A/Bテスト**: [ ] TODO: 評価方法の詳細

---

<!-- _class: lead -->

# まとめ

---

## Two-Towerモデルのまとめ

### 主要なポイント

- **2つの独立したタワー**でユーザーとアイテムを埋め込みベクトルに変換
- **スケーラビリティ**と**推論速度**を両立した推薦モデル
- 大規模な候補生成（Candidate Generation）に最適

### モデル構造のバリエーション

- タワー内のアーキテクチャは柔軟に設計可能
- 特徴量エンジニアリングが重要

### 学習方法のバリエーション

- 損失関数の選択（Pointwise, Pairwise, Listwise）
- ネガティブサンプリング戦略の工夫
- バッチネガティブサンプリングによる効率化

---

## Two-Towerモデルを使うべき場面

- ✅ 大規模な候補集合（数百万〜数億アイテム）
- ✅ リアルタイム推論が必要
- ✅ ANN検索との組み合わせ

---

## (再掲) 参考文献

1. Google Play事例 (2020): [Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations](https://storage.googleapis.com/gweb-research2023-media/pubtools/6090.pdf)
2. Uber事例 (2023): [Innovative Recommendation Applications Using Two Tower Embeddings](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
3. [ ] TODO: その他の参考文献を追加

---

<!-- _class: lead -->

# ご清聴ありがとうございました
