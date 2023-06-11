---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: MNARデータを使った推薦モデルのオフライン評価において、データを重み付けサンプリングしてMARデータに近づける事でbias軽減を試みる論文を読んだ
subtitle: n週連続推薦システム系論文読んだシリーズ 18週目
# date: 2023/06/02
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 論文の基本情報

- title: Debiased offline evaluation of recommender systems: a weighted-sampling approach
- published date: 30 March 2020,
- authors: Diego Carraro, Derek Bridge
- url(paper): [https://dl.acm.org/doi/10.1145/3341105.3375759](https://dl.acm.org/doi/10.1145/3341105.3375759)

## ざっくり論文概要

- 最後に書く!

# Introduction

## 推薦システムのオフライン評価 と 様々な交絡因子

推薦システムのオフライン評価には、ユーザ-アイテム間のinteraction(ex. クリック, 購入, 評価, etc.)の観測データを用いる.しかし様々な**交絡因子(Confounding factor)**によってbias(選択bias)が含まれる. (因果推論の用語だが、推薦の文脈で言えば、"interactionの観測" -> "ユーザのアイテムへの嗜好度合い" の因果関係の観測に影響を与えうる第三の因子.)

- 例1. UI上で目立つ位置に露出されたアイテムは、interactionが発生しやすい.
- 例2. 推薦システム自身が露出したアイテムは、ユーザとinteractionが発生しやすい.(feedback loop)
- 例3. 映画の星1~5の様な明示的評価において、ユーザは自分が好きなアイテムを評価しやすい.

これにより観測データにて欠損したinteractionは**MNAR(Missing Not At Random)**となる. (MNARデータと呼ぶ...!)

## MNARデータが与える影響

- 古典的なオフライン評価は、観測データが**MCAR(Missing Completely At Random)**データまたは**MAR(Missing At Random)**データのいずれかである、という仮定に基づいている.
- MCARやMARであるかのようにMNARデータを評価すると、推薦モデル性能の推定にてbiasが発生する. (ex. 人気アイテムを推薦するモデルや、activeなユーザに過度に特化したモデルを不正に評価する.)
- MNARデータの問題に対応する為に、**3種**のアプローチがある.
  - 1. MNARテストデータの代わりにMARデータを収集する.
  - 2. MNARテストデータのbiasを補正できるように、真のモデル性能の不偏推定量を設計する.
  - 3. MNARテストデータからデータをサンプリングし、**MARに近い性質を持つ介入テストデータ**を作る.

本論文は、**3つ目のアプローチ**に焦点を当てている.

## 本論文の目的 & アプローチの概要

- 本論文の目的: MNARテストデータから MARデータに近い介入テストデータを作る為の、**新しいサンプリング戦略**を調査する事.
- そのために...
  - MNARデータにおけるユーザとアイテムの分布と、unbiasedなMAR分布との間の乖離を考慮して重みを計算する、**重み付けサンプリング戦略**を提案する.
  - オフライン実験を行い、提案したサンプリング手法と既存のサンプリング戦略 SKEW を比較した.
-

# MNARデータに対処する為の三種のアプローチ

- 1. MNARテストデータの代わりに**MARデータを収集**する.
- 2. MNARテストデータのbiasを補正できるように、**真のモデル性能の不偏推定量を設計**する.
- 3. MNARテストデータからデータをサンプリングし、**MARに近い性質を持つ介入テストデータ**を作る.

## 方法1. MNARテストデータの代わりにMARデータを収集する.

## 方法2. biasを補正できるような推定量を設計する.

## 方法3. MNARデータから介入データをサンプリングする.

# 実験方法 & 結果

**MNARデータから介入テストセットを作成する様々なサンプリング戦略の良し悪し**を評価し、本論文で提案された WTD と WTD_H の活用可能性を探る為に、オフライン実験を行った.

## 実験設定

- **MARデータ部分($D^{mar} = \{O^{mar} ,Y^{mar}\}$)とMNARデータ部分($D^{mar} = \{O^{mnar},Y^{mnar}\}$)**の両方を持つ、公開データセット(2種)を使用した.
- ある推薦モデルのオフライン評価において、**MNARデータから作る介入テストセットによる評価結果**が、**MARな(unbiasedな)テストセットによる評価結果(今回のground-truth!)**とどれだけ**似ているか**という観点から、様々な戦略の良し悪しを評価した.
- シンプルな5種の推薦モデル(AveRating, PosPop, UB_KNN, IB_KNN, MF)に対して、5種のサンプリング戦略(FULL, REG, SKEW, WTD, WTD_H)を適用した.
- 介入テストデータのサイズが、**元のMNARテストデータの50%のサイズ**になる様にサンプリングした.

## (補足)使用するデータセット:

- 2つの公開データセットを使用: CoatShopping(衣服) と Webscope R3(音楽)
- どちらも**MARデータ部分($D^{mar} = \{O^{mar} ,Y^{mar}\}$)とMNARデータ部分($D^{mar} = \{O^{mnar},Y^{mnar}\}$)で構成される**. -> 今回の目的にぴったり...!
- $D^{mar}$ 部分は、いずれもforced ratings approachで収集されているため、ほぼbiasのないMARデータなはず.
- $D^{mnar}$ 部分は、推薦システムの運用中に収集されたもの.

## (補足)サンプリング戦略の良し悪しの評価方法:

- 実験の目的は、**介入テストセットを作成する様々な戦略の良し悪し**を評価すること.
- "良し悪し"の基準は、ある推薦システムのオフライン評価において、介入テストセットによる評価結果が、**unbiasedなテストセットによる評価結果とどれだけ似ているか**.

## (補足)シンプルな5種の推薦モデル

実験において5種の推薦モデルを学習させ、全てのモデルが推薦アイテムのランク付けリストを生成する.

- AvgRating: 非個別化推薦1. 評価値の平均値が高いアイテム順に推薦.
- PosPop: 非個別化推薦2. positive評価値の数が多いアイテム順に推薦.
- UB_KNN: 個別化推薦1. ユーザベースの最近傍アルゴリズム. (評価値傾向が似てるユーザを探す)
- IB_KNN: 個別化推薦2. アイテムベースの最近傍アルゴリズム. (評価値傾向が似てるアイテムを探す)
- MF: 個別化推薦3. 一般的なMatrix Factorizationアルゴリズム.(UB_KNNとIB_KNNのハイブリッド的なイメージ)

## (補足)比較対象の5種のサンプリング戦略

各戦略はサンプリング確率分布 $P_{S}(\mathcal{S}|u,i)$ を定義し、元のMNARテストセット $O^{he}$ (i.e. $Y^{he}$)から介在テストセット $O^{S}$ (i.e. $Y^{S}$)をサンプリングする.

- FULL: サンプリング無しの戦略. $P_S(\mathcal{S}|u,i) = 1$.
- REG: $O^{he}$からの一様ランダムなサンプリング. $P_S(\mathcal{S}|u,i) = 1/|O^{he}|$.
- SKEW: 既存のアイテム人気度に基づくサンプリング戦略. $P_S(\mathcal{S}|u,i) = 1/pop(i)$. $pop(i)$ は$O^{he}$におけるアイテムiのinteractionの観測数.
- **WTD: 提案された戦略1**. $P_S(\mathcal{S}|u,i) = w_{u}(w_{i})^2$. 実際のMARデータ $O^{w}$ からMAR事後分布を推定して $w_u, w_i$ を計算.
- **WTD_H: 提案された戦略1**. $P_S(\mathcal{S}|u,i)$はWTDと同じ. 実際のMARデータ $O^{w}$ を使用せず、仮説のMAR事後分布から $w_{u}, w_{i}$ を計算.

## 実験①: モデル精度指標のground-truth との差

table2は、各推薦モデルに関する**モデル精度指標(Recall@10)のground-truth**(=MARテストセット $Y^gt$ による評価結果)と、各サンプリング戦略による**介在テストセットを使った推定値**のpercentage difference.

![]()

- 一般に提案手法(WTD, WTD_H)は、**ground-truthのモデル性能を最も良く近似**できている.
- FULL戦略とREG戦略の結果はよく似ており、ground-truthから非常に離れている. -> debias効果に重要なのは"サンプリングする事"そのものではなく、**"いかにサンプリングするか"という戦略**である.

## 実験②: オフライン評価による推薦モデル達の順位づけ

- オフライン評価は複数の推薦モデルを順位づけ、**"良さそう"なモデルを絞り込む**. これによりオンライン実験(ex. ABテスト)のコストを節約できる.
- -> モデル性能の推定値がground-truthと近いだけでなく、**複数のモデルの順位付け結果がground-truthとどの程度合致しているか**も重要...!!
- ランキング類似度の評価指標(kendall's tau)を用いて、ground-truthによる順位付けの結果と比較した.

table3は、hogehoge...

table4は、hogehoge...

# まとめ

## 結論

- 本論文では、MNARデータからMAR的な性質を持つ介在テストセットを生成する新しいサンプリング戦略 **WTD**, **WTD_H** を提案した.
- 偏りのないMARテストセットをground-truthとして使用した実験により、サンプリング戦略が、MNARデータがモデルのオフライン性能評価に与えるbiasを軽減できる事を示した.
- 既存のサンプリング戦略 SKEW と比較して、本戦略は**様々な推薦モデルにおいて最も堅牢(robust)**という結果だった.
- WTD戦略ではMARデータが必要だが、**仮説のMAR分布を使うWTD_H**が上手く機能する事わかったので、本戦略の適用においてMARデータは必要ない.

## 提案手法の利点:

提案手法の利点:

- low overhead:
  - 重みの複雑な学習ステップが不要で、シンプルな設計->実装が簡単.
  - 介入によりデータセットのサイズが小さくなる-> 評価(や学習)にかかる**計算コストを削減**できる.
- high generality:
  - データセット中のinteraction valueに依存しない->**explicitデータにもimplicitデータにも**適用可能.
  - 推薦モデルの評価(検証)のみでなく、**学習に拡張**する事も可能.
  - 既存のモデルの学習や、既存のmetricによるオフライン評価に適用可能. (特別なモデルやmetricの設計が不要.)
- サンプリング重みの算出方法に、因果推論的な手法を使うのもありかも...!(それこそpropensity scoreとか?でもlow overheadの利点を失うか...!)
