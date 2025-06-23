refs: https://arxiv.org/pdf/2306.14834

# Scalable Neural Contextual Bandit for Recommender Systems

## ざっくり概要!

## イントロ: 研究のモチベーション

### 従来のRecSysの課題

- 教師あり学習の限界
- 探索の必要性

### 従来のneural contextual banditの課題

- 計算コストの高さ
- 既存手法の非実用性

## 関連研究と探索戦略

### TS(Thompson Sampling)系のアプローチ

### UCB(Upper Confidence Bound)系のアプローチ

### 計算上のボトルネック

## ENR(Epistemic Neural Recommender)の提案

- スケーラブルなニューラルネットワークベースのコンテキストバンディットアルゴリズム ENR(Epistemic Neural Recommender)を提案する。
  - 前述の通り、**Thompson SamplingやUCBのNN手法の大きな欠点はその計算コストの高い不確実性推定プロセス**。これが実運用システムへの適用を妨げてる。
- 本論文の提案手法 ENR の主要な目的は、モデルの性能を向上させながら、この計算コストの問題に対処すること。

### Informative Naural Representation(情報の多いニューラル表現)

- 全てのNN探索手法に共通する重要な観点は、context-actionペアのための効果的な表現の生成。
  - 特にcontexual banditのフレームワーク内では、考慮したい主要な表現要因は以下の3つ:
    - 1. 行動表現(action representation)
    - 2. コンテキスト表現(context representation)
    - 3. コンテキスト-行動間の表現(context-action representation)
- 行動表現とコンテキスト表現の生成方法:
  - hoge
- コンテキスト-行動間の表現の生成方法:
  - hoge
- 最終的な表現の生成方法:
  - 上記の3種の表現を連結(concat)して、最終的な表現を得る。
    - $x_{t, A} = concat(h_{\beta_{context}}(x_{S_t}), h_{\beta_{action}}(x_{A})), I(x_{S_t}, x_{A})$
  - この表現は不確実性推定にも利用される。

### ENRアーキテクチャ

- 上記で導出された表現 $x_{t, A}$を用いて、点推定と不確実性推定の両方を行うNNが設計される。
- EpiNetの採用と改善:
  - 

### ENR Thompson Sampling エージェント

## 実験

### 実験方法

### 主な実験結果

### アブレーションスタディ的な実験結果
