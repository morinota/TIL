---
format:
  html:
    theme: cosmo
  # revealjs:
  #   # incremental: false
  #   # theme: [default, custom_lab.scss]
  #   theme: [default, custom_lab.scss]
  #   slide-number: true
  #   scrollable: true
  #   logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
  #   footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: RecSysの実運用で人気なTwo-Towerモデル! と言ってもいろんなバリエーションがありそうだなぁと思った話
subtitle: y-tech-ai ワクワク勉強会
date: 2025/10/07
author: モーリタ
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 0.1. なんで今回このトピックを話したいんだっけ??

- ここ数年、**RecSysの実運用でTwo-Towerモデルが結構人気!**
- 実は我々もまさにTwo-Towerモデルを採用し運用に移ろうとしてるフェーズ。
  - ただ当然「単に人気だからTwo-Towerモデルを採用しよう!」ではなく、「全てのアーキテクチャはトレードオフ」であることを念頭に置いた上で、なぜ実運用で人気なのか、自社ドメインで採用するべきなのかをきちんと言語化・説明できるようにしたい。
- また、実際に運用しようとすると、Two-Towerモデルにも色々なバリエーションがあって、**DS・MLエンジニア・MLOpsエンジニアが設計・意思決定を頑張るべきことが結構ある**なぁと感じた。

## 0.2. 今日のアウトライン

1. はじめに: そもそもTwo-towerモデルって??なんで人気なんだっけ??
2. 主張1: Two-towerのネットワーク構造のバリエーションが色々ある!
3. 主張2: Two-towerの学習方法のバリエーションが色々ある!
4. まとめ

# 1. はじめに: そもそもTwo-towerモデルって??なんで人気なんだっけ??

## 1.1. RecSysの実運用でTwo-Towerモデルが結構人気

- Googleさんの論文(Youtube, Google Playの事例)
  - [Deep Neural Networks for YouTube Recommendations](https://static.googleusercontent.com/media/research.google.com/ja//pubs/archive/45530.pdf)
  - [Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations](https://storage.googleapis.com/gweb-research2023-media/pubtools/6090.pdf)
- Uberさんの事例: [Innovative Recommendation Applications Using Two Tower Embeddings at Uber](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
- リクルートさんの事例: [Two-Towerモデルと近似最近傍探索による候補生成ロジックの導入](https://blog.recruit.co.jp/data/articles/two-tower-model/#%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E5%89%8D%E5%87%A6%E7%90%86)
- ZOZOさんの事例: [ZOZOTOWNホーム画面のパーソナライズ - Two-Towerモデルで実現するモジュールの並び順最適化](https://techblog.zozo.com/entry/zozotown-home-module-personalization-v1)
- 日経さんの事例: [日経電子版のアプリトップ「おすすめ」をTwo Towerモデルでリプレースしました](https://hack.nikkei.com/blog/replace_ai_rec_by_two_tower/)
- etc...

## 1.2. Two-Towerモデルってざっくり何だっけ??

![Two-Towerモデルの基本構造](image.png){fig-align="center"}

- 2つの独立したニューラルネットワーク（タワー）を用いた推薦モデル。
  - NLP分野のdual encoderを推薦・検索タスクに応用したもの。
- two-towerモデルの構成要素
  - User Tower: ユーザ特徴を埋め込みベクトルに変換。
  - Item Tower: アイテム特徴を埋め込みベクトルに変換。
  - predictionモジュール: 両タワーの出力を元に(ユーザ, アイテム)ペアに関する何らかのスコアを算出。スコアを元に何を推薦するかの意思決定を行う。

## 1.3. なんでRecSysの実運用で人気なんだっけ??

### 結論: **DNN系モデルの恩恵は受けつつ、推論時のスケーラビリティと処理速度をコスト効率良く実現できるから!**

- まず非DNN系モデルと比較して...
  - 様々な種類・形状の特徴量を柔軟に考慮することができる表現力の高さ!
- 他のDNN系モデルと比較して...
  - **推論コストが低く実現できる!**
    - ユーザとアイテムの情報を独立した2つのタワーで処理できる構造により、**計算コストの重い処理を事前計算しておける!**
    - **ANN検索との相性 ◎** なので、更にスケーラビリティ up も!
  - デメリット(メリットの裏返し): ユーザ×アイテム粒度の特徴に対応できない!

## 1.4. Two-Towerモデルが活躍してるシーン

RecSysの実運用で**Two-Towerモデルが活躍してるシーンは大きく3種類な印象**...! :thinking:

1. レイテンシ要件の厳しい**リアルタイム推薦**をコスト効率よく実現したいケース
   - ex. GoogleさんのYoutube, Google Playの事例,　Uberさんの事例, 日経さんの事例, etc.
2. **膨大な推薦アイテム候補に対する推薦**をコスト効率よく実現したいケース
   - ex. GoogleさんのYoutube, Google Playの事例, Uberさんの事例, リクルートさんの事例, ZOZOさんの事例, etc.
   - 2-stages推薦の1-stages目の候補絞り込み(candidate retrieve)フェーズで人気!
3. ユーザやアイテムのrichな**特徴量としての埋め込み表現**を学習する用途。
   - ex. Netflixさんの事例, Uberさんの事例, etc.

## 1.5. ニュース推薦ドメインでTwo-Towerモデルを採用するべきか??

### 先に結論: **lifetimeが短いニュース推薦**のユースケースにて事業価値を発揮したい場合、Two-towerモデルはかなり現実的で有力な選択肢だと思う!

前提: ニュースはlifetimeが短いので、基本的にリアルタイム推論が望ましい!

- ニュース推薦では、毎秒新しいニュース(=推薦アイテム候補)が追加される
  - 特にストレートニュース的なコンテンツはlifetimeが短く、**なるべく早く届ける事がユーザ体験にとって重要**だと思われる。
- 機械学習の推論パターンは大きくバッチ・ストリーミング(非同期)・リアルタイムの3つに分類できる。
  - **毎秒追加される推薦アイテム候補を効率的に最速で各ユーザに推薦できるようにするためには、リアルタイム推論が望ましい**...!

リアルタイム推論によるニュース推薦をプロダクション環境で実現するには、**大量のレコードに対してリアルタイムで高速に推論できる事**が必要! → **もうtwo-towerじゃん!**

## 1.6. ここまでのまとめ! 

**Two-towerモデルは、DNN系モデルの恩恵は受けつつ、推論時のスケーラビリティと処理速度をコスト効率良く実現できるから、RecSysの実運用で人気!**

アイテムのlifetimeが短いニュース推薦ドメインにおいても、Two-towerモデルはかなり現実的で有力な選択肢のはずだ!

# 2. 主張1: Two-towerのネットワーク構造にもバリエーションが色々ある!

自社のユースケースに応じてよしなに設計しよう!

## 2.1. Two-tower型アーキテクチャの基本構成

3つの主要コンポーネント:

1. User Tower (Query Tower)
2. Item Tower
3. Predictionモジュール

## 2.2. タワーのバリエーション1: 基本はFFN的な構造!

だんだんと出力層にかけて次元が小さくなっていく構造 = これが「タワー」と呼ばれる所以。

```
各種特徴量の入力層
     ↓
各種特徴量の前処理層 (Entity Embedding, Normalization, etc.)
     ↓
全結合層 (ex. 1024次元)
     ↓
全結合層 (ex. 512次元)
     ↓
出力層 (ex. 256次元)
```

Googleさんの論文達(Youtube, Google Playの事例)やUberさんの事例では、基本的にはFFN(Feed Forward Network)

## 2.3. タワーのバリエーション2: Attention・RNN

特に「**ユーザがアイテムを消費する順序**」を重視する(=Sequential Recommendationと呼ばれる分野)ようなRecSysの場合は、タワー(特にユーザタワー)にAttentionやRNNを組み込むバリエーションもある。

- SASRecモデル, BERT4Recモデルなど
- ニュース推薦モデルの論文でもNRMSなどいくつかある
- でも実運用でどれだけ使われてるかは不明...!:thinking:
- ex. ユーザタワーの入力の1つとして、アイテム消費履歴のsequenceを受け取って順序を考慮して処理するイメージ...!

## 2.4. タワーのバリエーション3: タワー間でのレイヤー共有

両タワーの一部分のレイヤーを共通化してる事例もあった(Uberさんの事例!)

- 具体的には、両タワーが同じUUID Embedding Layerを共有(ユーザidとお店idのentity embedding層を共有してるって話っぽい...!:thinking:)

![レイヤー共有の構造図](image-1.png){fig-align="center"}

ブログで紹介されてたレイヤー共有の採用理由:

- メリット1: モデルサイズの削減
  - eater id (ユーザid?) やstore_id(お店id?) のような**high-cardinality(高カーディナリティ)を持つカテゴリ特徴量**を扱う必要があった。
  - これらのembedding層を両タワーで別々に持つと、モデルサイズが爆発的に大きくなる
  - レイヤー共有によりモデルサイズを20倍削減できたとのこと。
- メリット2: モデルの推薦性能の向上
  - Uberさんのホームフィードの事例では、このレイヤー共有が推薦性能の向上に非常に重要だった。

## 2.5. predictionモジュールのバリエーション

### 内積(dot-product) - 最も一般的

- シンプルで高速。
- 埋め込み空間での類似度として解釈しやすい。
- 特にtwo-towerを**膨大な推薦アイテム候補を絞り込む用途(candidate retrieve)**で採用する場合、**ANN(Approximate Nearest Neighbor, 近似最近傍)検索**によって推論を更に高速化できる!

### 内積以外の選択肢

でも内積だけじゃない! 軽量モデルを採用することもあるっぽい!

- Youtubeの**two-towerモデルを少数アイテムのリランキング(candidate reranking)フェーズで採用**した事例では、ロジスティック回帰モデルをpredictionモジュールに採用してたっぽい!
- まあでもほぼほぼ内積が多い!

# 3. 主張2: Two-towerの学習方法にもバリエーションが色々ある!

自社のユースケースに応じてよしなに設計しよう！

## 3.1. そもそもRecSysタスクを定式化してみよう

目的: ユーザーuに対して、最も関連性の高いアイテムiを推薦する

課題:
- 明示的なラベルが少ない（暗黙的フィードバックが中心）
- データ収集バイアス
- スケーラビリティ

## 3.2. 代理学習問題(surrogate learning problem)

真の目的を直接最適化するのは困難 → 代わりに関連する別のタスクを学習

代理タスクの例:
- クリック率予測
- 購入確率予測
- next-item予測

## 3.3. 学習アプローチ 1: 回帰ベースアプローチ

予測タスクとして学習することで、累積報酬がより高くなるようなモデルを目指す!

- ユーザー-アイテムペアのスコアを予測
- 損失関数: MSE, Binary Cross Entropyなど

## 3.4. 学習アプローチ 2: 対照学習(contrastive learning)

ユーザ(クエリ)に対するポジティブ・ネガティブアイテムのペアを使った学習

- ネガティブサンプリングが重要
- 損失関数: Softmax Cross Entropy, BPRなど

## 3.5. 学習アプローチ 3: 勾配ベースアプローチ

推薦システムを強化学習問題として定式化

- 累積報酬最大化
- 長期的なユーザー満足度を最大化

# 4. まとめ

## 4.1. なぜTwo-TowerモデルがRecSysで人気なのか??

- NNの恩恵を受けつつ、スケーラビリティと推論速度を両立させやすいから!

## 4.2. Two-Towerモデルの構造のバリエーション

- 色々あるが、とりあえずまずはMLP的なタワー、内積ベースのpredictionモジュールから始めて良さそう!

## 4.3. Two-Towerモデルの学習方法のバリエーション

- 推薦タスクの性質上、いろんな代理学習問題(surrogate learning problem)が考えられる!
- 自社のユースケース(フェーズの違い、トラフィック量、過去に収集した観測データの性質, RecSysで改善したい指標)などに応じて、試行錯誤しつつ有効なアプローチを選びたい!

## 4.4. 思ったこと

- Two-tower (に限らずNN系のアプローチ) の自由度の高さは、「色々選択しないといけなくて大変」とも取れるが、「自社のユースケースに合わせて自由に設計できる」とも取れる。
- 特にモデルアーキテクチャや目的関数の設計は、DS・ML・MLOpsエンジニアの腕の見せ所とも言えそう...!!
  - そもそも多様なNNアーキテクチャの中でTwo-towerを選ぶ意思決定をすること、その理由をきちんと言語化して納得できる説明ができること自体が、MLOpsを司るエンジニアとして腕の見せどころのはず...!:thinking:

## 4.5. 参考文献

- [Deep Neural Networks for YouTube Recommendations](https://static.googleusercontent.com/media/research.google.com/ja//pubs/archive/45530.pdf) (2016)
- [Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations](https://storage.googleapis.com/gweb-research2023-media/pubtools/6090.pdf) (2020)
- [Innovative Recommendation Applications Using Two Tower Embeddings at Uber](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/) (2023)
