---
format:
  revealjs:
    # incremental: false
    theme: [default, quarto_custom_style.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: hogehogeな論文を読んだ
subtitle: n週連続推薦システム系論文読んだシリーズ 20週目
date: 2023/07/05
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 論文の基本情報

- title: Denoising Self-Attentive Sequential Recommendation
- published date: September 2022,
- authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
- url(paper): [https://arxiv.org/pdf/2212.04120.pdf](https://arxiv.org/pdf/2212.04120.pdf)

## ざっくり論文概要

# Introduction

## sequential 推薦の発展

- しかし、**sequential推薦器のrobustness**についてはあまり研究されていない.
- 実世界の多くのitem sequences(特にimplicit feedback!)は自然にノイズが多く、**真陽性(true-positive)と偽陽性(false-positive) の両方のinteractionを含む** [6, 45, 46].
  - 偽陽性の例: 好きじゃないけどクリックしてしまった. 購入してみたが嫌いだった.
  - 実際、クリックの大部分はユーザの嗜好に合わず、多くの購入された製品は否定的なレビューで終わったり、返品されたりする.
  - (next-token-predictionと比較しても、こういったノイズが多かったりするのかな:thinking:)
- そのため、**ノイズに強いアルゴリズムを開発することは、sequential推薦において大きな意義がある**.

## self-atteniton networkがノイズの多いsequenceに弱い問題

- 残念ながら、vanillaなself-attention networkは、**Lipschitz連続ではなく(?)**、**入力sequenceの質に弱いという問題**がある[28]
- 図1は、左から右へのsequential recommendationの一例.
- ex.) ある父親が息子に(携帯電話、ヘッドフォン、ノートパソコン)、娘に(カバン、ズボン)を購入する場合、(携帯電話、カバン、ヘッドフォン、ズボン、ノートPC)という順序になったとする.
- sequential recommendation の設定では、**ユーザの以前の行動(ex. 電話、カバン、ヘッドホン、ズボン)から、次のアイテム(ex. ノートPC)を推論すること**を意図している.
- しかし、アイテム間のcorrelationsが不明確であり、**直感的にパンツとノートPCの関連を納得できない**ため、この予測はuntrustworthyである.
- trustworthyなモデルは、sequence内の無関係なアイテムを無視し、相関のあるアイテムのみを捉えることができるはず.

## ノイズの多いsequenceにどう対応すべきか?

- 既存のself-attentive sequential model(ex. SASRec [26], BERT4Rec [41])は、full attention distributionが密である事から、全てのitemに一定以上のcredit(=attention weight?)を割り当ててしまう為、sequence内のノイズに対処するには不十分.
- 一つの簡単な戦略は、**attention layersの接続をsparseにした**Transformerアーキテクチャを設計すること[10, 58].(LMタスクで活発に研究されてるらしい)
  - しかし、これらのモデルは事前に定義されたattention schemas(??)に大きく依存しており、柔軟性や適応性に欠けている.
  - また、エンドツーエンドの学習アプローチとは異なり、言語モデルタスクのsparseパターンがsequential推薦にうまく一般化できるかどうかは不明.

## 本論文の目的 & 提案手法の概要

- 本論文の目的は、**ノイズの多いimplicit feedbackからのnext-item-predictionタスク**において、self-attention型sequential推薦モデルをより良く学習させるための**ノイズ除去戦略(Rec-Denoiser)**を提案する事.
- 提案手法のアイデアは、**全てのattentionは必要ではなく、冗長なattentionを刈り取ることでさらに性能が向上する**、という最近の知見に由来[10, 12, 40, 55, 58].
- Rec-Denoiserは、タスクと無関係なattentionをself-attention layersで削除する様な、学習可能なmaskを導入する.
  - 利点1: sequenceからより情報量の多いアイテムのsubsetを抜き出し、明示的にnext-token-predictionを実行できる.
  - 利点2: Transformerのアーキテクチャを変更せず、**attention分布のみを変更する**為、実装が容易 & あらゆるTransformerに適用可能で、その解釈可能性を向上できる.
- 実世界のベンチマークデータセットを使った実験で、手法の有効性を検証.

## 提案手法 Rec-Denoiser の２つの大きな課題 とその対応

Rec-Denoiserでは、2つの大きな課題がある.

- 課題1: binary mask(i.e. 0は削除され、1は保持される)は、その離散性に依ってback-propropagation実行不可能.
  - ->本論文では、probabilistic reparameterization(確率的再パラメータ化?)[25]により、離散変数を連続的な近似値で緩和する.(ここが結構頑張りどころっぽい:thinking:)
  - この工夫によって、提案手法の微分可能なmaskは、Transformerとend-to-endで一緒に学習可能.
- 課題2: scaled dot-product attention は Lipschitz連続(?)ではない為、input perturbations(入力摂動?ノイズ??)に対して脆弱[28].
  - ->本論文では、Transformerブロック全体にヤコビアン正則化[21, 24]を適用.

# Sequential Recommender と Sparse Transformer に関する既存研究

## Sequential Recommender

## Sparse Transformer

# Sequential Recommendationの定式化

## Sequential Recommendationタスクの定式化

# self-attentive recommender モデルの再検討

## Embedding Layer

## Transformer Block 1: Self-attention 層

## Transformer Block 2: Point-wise Feed-forward 層

## Transformer Block 3: 学習の目的関数

## noisy attention問題

# 提案手法: Rec-Denoiserについて

## differentiableな(微分可能な) mask

## 学習可能なsparse Attention

## 効率的な勾配計算

## Jacobian Regularization(ヤコビアン正則化)

## 損失関数の最適化1

## 損失関数の最適化2: end-to-endの学習

## モデルのcomplexity(計算量?)

# 実験
