---
marp: true
theme: default
paginate: true
header: 'RecSysの実運用で人気なTwo-Towerモデル! と言ってもいろんなバリエーションがありそうだなぁと思った話'
footer: 'Y-tech AI勉強会 2025/10/05 https://x.com/moritama7431'
---

# RecSysの実運用で人気なTwo-Towerモデル!

と言ってもいろんなバリエーションがありそうだなぁと思った話

---

## なんで今回このトピックを話したいんだっけ??

- TODO

---

## 今日のアウトライン

1. はじめに: そもそもTwo-towerモデルって??なんで人気なんだっけ??
2. 主張1: ネットワーク構造のバリエーション
3. 主張2: 学習方法のバリエーション
4. まとめ

---

<!-- _class: lead -->

# はじめに

---

## RecSysの実運用でTwo-Towerモデルが結構人気

Googleさん、Uberさん、リクルートさん、ZOZOさん、日経さん、etc...

---

## Two-Towerモデルってざっくり何だっけ??

- 2つの独立したニューラルネットワーク（タワー）を用いた推薦モデル。
  - User Tower: ユーザ特徴を埋め込みベクトルに変換。
  - Item Tower: アイテム特徴を埋め込みベクトルに変換。
  - predictionモジュール: 両タワーの出力を元に(ユーザ, アイテム)ペアに関するスコアを算出。
- NLP分野のdual encoderモデルを推薦・検索タスクに応用したもの。

---

## なんでRecSysの実運用で人気なんだっけ??

NNの恩恵を受けつつ、推論時のスケーラビリティと処理速度を両立させやすい

- Item埋め込みを事前計算してオフラインで保存
- 推論時はUser埋め込みのみをリアルタイム計算
- ANN検索で高速に候補アイテムを検索

計算量: O(q × M) → O(M) + O(q)

---

## 先に参考文献を紹介

1. Google Play事例 (2020): [Mixed Negative Sampling...](https://storage.googleapis.com/gweb-research2023-media/pubtools/6090.pdf)
2. Uber事例 (2023): [Innovative Recommendation Applications...](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
3. TODO: その他

---

<!-- _class: lead -->

# 主張1

ネットワーク構造のバリエーション

---

## Two-tower型アーキテクチャの基本構成

3つの主要コンポーネント:

1. User Tower (Query Tower)
2. Item Tower
3. Predictionモジュール

---

## タワーのバリエーション (1/3): 基本はMLP

だんだんと出力層にかけて次元が小さくなっていく構造

```
Input Features (高次元)
     ↓
Dense Layer 1
     ↓
Dense Layer 2 (次元削減)
     ↓
Embedding Layer (低次元)
```

これが「タワー」と呼ばれる所以

---

## タワーのバリエーション (2/3): Attention・RNN

next-item prediction重視の場合:

- AttentionやRNNを組み込むバリエーションもある
- ユーザーの行動履歴をシーケンスとして扱う

---

## タワーのバリエーション (3/3): パラメータ共有

両タワーの中間部分のパラメータを共通化してる事例もある

- Uberさんの事例など
- パラメータ数の削減、学習の安定化

---

## predictionモジュールのバリエーション (1/2)

最も一般的: **内積(dot-product)**

- シンプルで高速
- 埋め込み空間での類似度として解釈しやすい

---

## predictionモジュールのバリエーション (2/2)

でも内積だけじゃない!

- 軽量モデルを採用することもあり
  - Youtubeのrerankingフェーズでの事例
- その他: コサイン類似度、ユークリッド距離、Hadamard積 + MLP

---

<!-- _class: lead -->

# 主張2

学習方法のバリエーション

---

## そもそもRecSysタスクを定式化してみよう

目的: ユーザーuに対して、最も関連性の高いアイテムiを推薦する

課題:
- 明示的なラベルが少ない（暗黙的フィードバックが中心）
- データ収集バイアス
- スケーラビリティ

---

## 代理学習問題(surrogate learning problem)

真の目的を直接最適化するのは困難 → 代わりに関連する別のタスクを学習

代理タスクの例:
- クリック率予測
- 購入確率予測
- next-item予測

---

## 学習アプローチ 1: 回帰ベース

予測タスクとして学習する

- ユーザー-アイテムペアのスコアを予測
- 損失関数: MSE, Binary Cross Entropyなど

---

## 学習アプローチ 2: contrastive learning

ポジティブ・ネガティブペアを対比的に学習

- ネガティブサンプリングが重要
- 損失関数: Softmax Cross Entropy, BPRなど

---

## 学習アプローチ 3: 勾配ベース

推薦システムを強化学習問題として定式化

- 累積報酬最大化
- 長期的なユーザー満足度を最大化

---

<!-- _class: lead -->

# まとめ

---

## なぜTwo-TowerモデルがRecSysで人気なのか

NNの恩恵 + スケーラビリティ + 推論速度の両立

- Item埋め込みの事前計算
- ANN検索による高速化
- O(q × M) → O(M) + O(q)

---

## 構造のバリエーション

- タワー: 基本はMLP、Attention・RNN、パラメータ共有も可
- predictionモジュール: 内積が一般的、軽量モデルも可

**→ とりあえずMLP + 内積から始めて良さそう!**

---

## 学習方法のバリエーション

3つのアプローチ:
1. 回帰ベース
2. contrastive learning
3. 勾配ベース

**→ 自社のユースケースに応じて選ぶ**

---

## 思ったこと

Two-towerの自由度の高さは...

- デメリット: 色々選択しないといけない
- メリット: 自由に設計できる

**モデルアーキテクチャや目的関数の設計は腕の見せ所!**

---

## (再掲) 参考文献

1. Google Play事例 (2020)
2. Uber事例 (2023)

---

<!-- _class: lead -->

# ご清聴ありがとうございました
