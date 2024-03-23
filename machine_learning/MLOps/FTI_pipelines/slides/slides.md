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

title: より持続可能性の高いMLシステムってどう作ればいいんだろうと悩み、有名なMLの技術的負債の論文読んだり、FTI Pipelines architectureについて調べたりした話
subtitle: y-tech-ai ワクワク勉強会
date: 2024/03/26
author: モーリタ
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## TL;DR

- より持続可能性の高いMLシステムってどう作るといいのか悩んで、有名な**MLの技術的負債の論文**や、**FTI Pipelines architecture**について調べた。
- FTI Pipelines architectureは、特徴量作成、学習、推論をそれぞれ独立したpipelineとして開発・運用する方法論。
- 確かに、ソフトウェアの複雑さ管理の観点からも、FTI pipelinesは有効そう。(モジュラー性, 関心の分離, 疎結合, 抽象化, etc)
- また、MLシステム設計における技術的負債の観点からも、FTI pipelinesは有効そう。(glue codeの削減, pipeline jungleの予防, etc)
- MLシステムを設計・開発する上で、メンタルマップとしてFTI Pipelines architectureを意識することは良さそう。

## このテーマを選んだ経緯 & 概要

- 業務の中で、漠然と「より"良い"MLシステムってどう作ればいいんだろう」と思って色々調べ始めた。
  - "良い"ってなんだろ?
    - ex. 変更・拡張しやすい、ABテストやオフライン実験も含めて運用しやすい、プロダクトに価値提供しやすい、みたいな状態を想像してる。
  - -> i.e. システムの持続可能性が高い?:thinking:
- 昨年のMLOps勉強会の発表の中で「FTI pipelines architecture」っていう言葉を聞き、興味を持った。
- 「[From MLOps to ML Systems with Feature/Training/Inference Pipelines](https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines)」は、HopsworksのCEOの方が書いた記事で、より良いMLシステムを作る上でのメンタルマップとしてFTI pipelines architectureを採用することが重要だと主張してる。
  - 要は「特徴量作成、学習、推論はそれぞれ独立したpipelineとして開発・運用しよう!」みたいな方針!
  - Hopsworks = 特徴量ストアやモデルレジストリ等のMLプラットフォームを提供してる会社っぽい。

## 導入: 何をすべきかという明確なメンタルマップが必要っぽい

## メンタルマップとしてのFTI Pipelines Architecture:

## Pre-MLOps時代の話:

- MLシステムの黎明期には、**MLシステムの開発は単にモデルを学習する以上のものである**ことがすぐに常識になった。
  - 下図は、MLシステムにおける隠れた技術的負債に関する論文(2015年)の抜粋(あ、よく引用されてる図だ! 良いMLモデルを作る以外にも色々必要だよって文脈:thinking:)
-

## アンチパターン例1:

<!-- - MLシステムには2つのタイプがある: バッチMLシステムとリアルタイムMLシステム(要はbatch推論かonline推論かの違いかな) -->

- バッチMLシステムのアンチパターンの例として下図が紹介されてた:
  - 特徴: 特徴量作成、学習、推論が一つのモノリシックなpipelineにまとまっている。学習モードか推論モードをbooleanフラグで切り替える。

![](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502ad7d387cfe977467717b_figure%204_lightbox.png)

- 良さげなところ:
  - 学習時と推論時で、特徴量の作り方の一貫性を保証しやすい!
- イマイチなところ:
  - 作成された特徴量を、他のモデルでサッと再利用できない。
  - モノリシックなためモジュラー性が低く、部分的なリソース最適化がしにくい。(ex. データサイズが増えたので特徴量作成を並列化したいが...! 学習時はGPU付きの計算機を使用したいが...!)

## アンチパターン例2:

- リアルタイムMLシステムのアンチパターンの例として下図が紹介されてた:
  - 特徴: クライアントからのリクエストを受けとり、リアルタイムで推論結果を返す。オフラインでの学習pipelineとオンラインの推論pipelineが別々になっている。

![figure5](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502adc6d9992658b4fa84b7_figure%205_lightbox.png)

- 良さげなところ:
  - 学習と推論のためのリソースをそれぞれ最適化できる(ex. 推論サーバのインスタンスを複数用意したり...!)
- イマイチなところ:
  - 作成された特徴量を、他のモデルでサッと再利用できない。
  - 学習時と推論時で、特徴量の作り方の一貫性を保証しづらい。
  - 特徴量作成のためのリソース最適化がしづらい。
  - (前述のアンチパターン例と合わせて)バッチとリアルタイムMLシステムで全く異なるアーキテクチャである点 -> 開発者にとってバッチ <-> リアルタイム間の移行コストが高い。

## FTI pipelinesアーキテクチャによるリアルタイムMLシステム例:

- 特徴: 特徴量作成の成果物をfeature storeに保存される。学習時と推論時にfeature storeからデータを取得する。(クライアントから受け取った情報を使う場合は推論時に追加の特徴量作成を行う必要はある。)

[figure6]()

## (脱線)そもそもPipeline Architectureってなんだっけ?

- 複数の**filter(component)**と、filter同士を繋ぐ**pipe**から構成されるので、pipe and filter architectureとも呼ばれる。
- たぶん「一方向的」というのが特徴 :thinking:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*C1aXSo3klBPgPZSi8ZFhHw.png)
