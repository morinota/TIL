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

title: hogehogeな論文を読んだ
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

## Hogehoge

## 本論文の目的 & アプローチの概要

- 本論文の目的は、hogehogeする事.

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

## (補足)5種のサンプリング戦略

## 実験①: ground-truth との差

## 実験②: オフライン評価による推薦モデル達の順位づけ

- オフライン評価は複数の推薦モデルを順位づけ、**"良さそう"なモデルを絞り込む**. これによりオンライン実験(ex. ABテスト)のコストを節約できる.
- -> モデル性能の推定値がground-truthと近いだけでなく、**複数のモデルの順位付け結果がground-truthとどの程度合致しているか**も重要...!!
- ランキング類似度の評価指標(kendall's tau)を用いて、ground-truthによる順位付けの結果と比較した.
