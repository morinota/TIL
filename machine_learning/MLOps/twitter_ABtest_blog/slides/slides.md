---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    scrollable: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: より良い意思決定のために under-powered なテストを避けるためのABテスト設計方法を調べてる
subtitle: y-tech-ai ワクワク勉強会
date: 2024/02/xx
author: モーリタ
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## はじめに: 経緯と概要

- 本資料は、以下のテックブログや論文を参考にunder-powered なテストを避ける為のABテストの設計方法について調べ、自分の理解をまとめたものです:)
  - [NetflixさんのABテストに関するブログ連載](https://netflixtechblog.com/building-confidence-in-a-decision-8705834e6fd8)
  - [X(旧Twitter)さんのABテストのサンプルサイズに関するブログ](https://blog.twitter.com/engineering/en_us/a/2016/power-minimal-detectable-effect-and-bucket-size-estimation-in-ab-tests)
  - [web上でのコントロール実験に関するpracticeをまとめたsurvey論文](https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf)
- 上記の文献ではABテストを経てより良い意思決定のための工夫として様々紹介されています。
- 本資料は、そのうちの**under-powered なテストを避ける為の設計方法**に焦点を当て、推薦システムを題材とした架空のABテストを例に設計を試みます。
- もし理解の誤りや気になる点などあれば、ぜひぜひお気軽に絵文字をつけてコメントしていただけると嬉しいです :smile:

# under-poweredなテストとは??

## ABテストにおける二種類の不確実性

- ABテストで得られる観測結果は、確率変数(=確率的に変動する値)なので、結果には不確実性がある。
  - (ex. 公平なコインを100回投げた時の表の出る回数は、必ずしも100回中50回とは限らないよね...!)
- ABテストによる意思決定には、大きく2種類の不確実性がある:
  - Type I error: false positive
    - 本当は施策に効果がないのに、効果があると判定しちゃう。
  - Type II error: false negative
    - 本当は施策に効果があるのに、効果がないと判定しちゃう。
- under-poweredなテストは、Type II errorのリスクが高いテストのこと。

## under-poweredなテストとは??

- under-poweredなテスト = 検出したい真の効果の大きさに対して、検出力(power, 指定した大きさの効果を正しく検出できる確率)が小さくなってしまっているテスト。
  - under-poweredなテストだと... 本当は施策に効果があるのに効果がないと判定されてしまうリスク(i.e. false negativeの確率)が高くなってしまう。
- -> under-poweredなテストを避ける為に、いい感じにABテストを設計する必要があるよね...!

## (自分の理解)under-poweredなテストを避けるためになにを設計できる?

- under-poweredなテストを避けるために、我々がABテスト開始前に設計できるのは、ざっくり以下の要素っぽい:
  - significance level(有意水準):
    - Netflixさんのブログではacceptable false positive rateとも表現されてて、個人的にはこっちの方が意味がわかりやすくて好き:thinking:
  - postulated effect size(仮定された効果量):
    - 検出力の値は検出したい効果量に依存するので、事前に設定しておく必要がある。
  - sample size(サンプルサイズ):
    - ABテストで収集すべき実験単位のサンプル数(実験単位がユーザの場合はユーザ数)。
    - 多いほどより小さい効果を検出しやすい。
  - metricの変動性:
    - metricの変動性(分散)によって、他の全ての条件が同じでも検出力が異なる。metricの変動性が大きく不安定であるほど、実験の不確実性が高くなる。
    - 評価に使用するmetricの選び方だったり、metricの変動性を抑える工夫が可能。

# 推薦システムの架空のABテストを例に、under-poweredなテストを避けつつ設計してみるぞ!

## 架空のABテストシナリオ

- 架空のABテストシナリオ:
  - ECサイトのメイン画面の「おすすめセクション」内では、人気商品を表示している(controll)。現在のconversion rateは5%(0.05)である(架空とは言え高すぎ?:pray:)。
  - 各ユーザの既存の嗜好と合致した商品を表示できれば、ユーザが好きな商品に出会える機会が増えユーザ体験が向上するのではという仮説を立て、機械学習モデルによるパーソナライズ施策を実装した(treatment)。

## サンプルサイズ以外の設定

基本的には、有意水準、評価するmetric、仮定された効果量を決めた上で、under-poweredなテストにならないような理想的なサンプルサイズの導出を試みます。

- サンプルサイズ以外の設定:
  - 有意水準(i.e. acceptable false positive rate)=5%。(今回は特に慣例から外れる理由はなさそうなので:thinking:)
  - 評価するmetric = 各ユーザのconversion rate (閲覧した商品を購入したか否かの割合)
    - 一旦 binary metricsを採用してみた。non-binary metricsを採用するケースも後半で試してみる。
  - 仮定された効果量: conversion rate +2%(0.02) (現在のconversion rate=5%に対して、施策でconversion rate=7%になると仮定(期待)する。)
  - 2つのvariant(controllとtreatment)には、それぞれ同じサンプルサイズ $n$ を割り当てる。

## (ちなみに) 評価するmetric: binary metricかnon-binary metricか

今回はABテストの統計的仮説検定で評価するmetricとして、binary metricsであるconversion rateを採用してみた。

- binary metrics:
  - 例えば、「閲覧した商品を購入したユーザ数の割合」であるconversion rateは、ユーザが閲覧した商品を購入するか、しないかのbinary metricと言える。
  - 他の例: CTR、プッシュ通知の開封率、解約率、etc...。
  - binary metricsの場合、ABテストの設計時にmetricの変動性(分散)を指定する必要はない。(期待値から直接計算されるので...!)
- non-binary metrics:
  - 例えば、「ユーザ毎の商品の平均購入金額」は、non-binary metricと言える。
  - 他の例: ユーザの滞在時間、サーバーのlatency、開封数、解約数、etc...。
  - non-binary metricsの場合、ABテストの設計時にmetricの変動性(分散)を指定する必要がある。(期待値から直接計算できないので...!)

## サンプルサイズの導出作戦

さて、under-poweredなテストにならないような理想的なサンプルサイズの導出を試みます。作戦の手順は以下です:

サンプルサイズを $n$ とおいておく。()

- 1. null distribution(帰無分布)を描画する。
  - 帰無仮説(=施策に効果がないという仮説)が正しい場合に得られる観測値の確率分布(=null distribution)を描画する。i.e. 確率分布関数を描画する。
- 2. rejection region(棄却域)を描画する。
  - 設定した有意水準(i.e. acceptable false positive rate)に基づき、rejectin region(棄却域)を描画する。
- 3. alternative distribution(対立分布)を描画する。
  - 仮定した効果量に基づき、対立仮説が正しい場合に得られる観測値の確率分布(=alternative distribution)を描画する。
- 4. 検出力を計算する。

## 手順1: null distribution(帰無分布)を描画する。

- 帰無仮説: control群とtreatment群で、真のconversion rateには差がない。
  (i.e. control群の真のconversion rate = treatment群の真のconversion rate = 5%)
- -> controll群のconversionも、treatment群のconversionも、期待値5%(p=0.05)のベルヌーイ分布に従うbinaryの確率変数である。
- -> サンプル数 $n$ の場合、controll群とtreatment群で観測されるconversion rate(=conversionの標本平均) $\hat{p}_{controll}, \hat{p}_{treatment}$ はそれぞれ、平均 $p$ 、分散 $p(1-p)/n$ の正規分布に従う。(中心極限定理より)
- -> 統計的仮説検定で扱える確率変数は1つなので、確率変数 ${\hat{p}_{treatment} - \hat{p}_{controll}}$ が従う確率分布を算出する必要がある。
  - -> 期待値 $p_{treatment} - p_{controll} = 0$ 、分散 $p(1-p)/n + p(1-p)/n = 2p(1-p)/n$ の正規分布に従う。(正規分布に従う確率変数同士の減算より)
- -> 以上より、null distributionは、期待値0、分散 $2p(1-p)/n$ の正規分布である。

以下の図は、n=100の場合のnull distributionを描画したもの。

![]()

## 手順2: rejection region(棄却域)を描画する。

有意水準(accetable false positive rate) = 5% の条件をもとに、null distribution (期待値0、分散 $2p(1-p)/n$ の正規分布)において、rejection region(棄却域)を算出する。

- rejection region(棄却域) = null distributionにおいて確率質量の累積値が5%を超えないような、最も発生しづらい観測結果の集合(i.e. 値域)
  - -> 今回の場合は片側検定を想定するので、null distributionの右側にrejection regionが描画されるイメージ。
  - -> null distributionの累積質量関数を $cmf(\odot)$ とすると、$cmf(x) < 1.0 - 0.05$ を満たす $x$ の集合がrejection regionになるはず...!

## 手順3: alternative distribution(対立分布)を描画する。

## 手順4: 検出力を計算する。

```

```

```

```

```

```

```

```