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
- また、MLシステム設計における技術的負債の観点からも、FTI pipelinesは有効そう。(glue codeの削減, pipeline jungleの予防, dead experimental codepathesの予防, etc)
- MLシステムを設計・開発する上で、メンタルマップとしてFTI Pipelines architectureを意識することは良さそう。

## このテーマを選んだ経緯 & 概要

- 業務の中で、漠然と「より"良い"MLシステムってどう作ればいいんだろう」と思って色々調べ始めた。
  - "良い"ってなんだろ?
    - ex. 変更・拡張しやすい、ABテストやオフライン実験も含めて運用しやすい、プロダクトに価値提供しやすい、みたいな状態を想像してる。
  - -> i.e. システムの持続可能性が高い?:thinking:
- 昨年のMLOps勉強会の発表の中で「FTI pipelines architecture」っていう言葉を聞き、興味を持った。
- 「[From MLOps to ML Systems with Feature/Training/Inference Pipelines](https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines)」は、HopsworksのCEOの方が書いた記事で、より良いMLシステムを作る上でのメンタルマップとしてFTI pipelines architectureを採用することが重要だと主張してる。
  - Hopsworks = 特徴量ストアやモデルレジストリ等のMLプラットフォームを提供してる会社っぽい。

# まずMLの技術的負債の論文における、システムの設計に関する負債に関して

- 論文: [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)(2015年)
- 基本的には、セクション5 「ML-System Anti-Patterns」でのMLシステム設計での技術的負債に関してメモしています...!

## たぶんこの図で有名な論文です!

![]()

Figure 1: Only a small fraction of real-world ML systems is composed of the ML code, as shown by the small black box in the middle. The required surrounding infrastructure is vast and complex.

「MLアルゴリズムは、実世界のMLシステムにおいてあくまでも要素の1つだよ!他にも重要な要素はたくさんあるよ!」みたいな意図でよく引用されてる気がする:thinking:

## MLシステムがhigh-debtな設計になりがち問題。

- 多くのMLシステムでは、学習や推論用のコードの割合は小さく、残りの多くは**plumbing(配管)**である。
- MLの手法を取り入れたシステムが、high-debt(高負債)なデザインパターンで終わることは残念ながら一般的。
- 論文のセクション5では、MLシステム設計における技術的負債について記述されてた。
  - 1. Glue Code (接着剤コード)
  - 2. Pipeline Jungle
  - 3. Dead Experimental Codepaths (死んだ実験コードパス)
- あと、ML領域では抽象化が不足してるんだという話や、MLシステムにおける"common smells"についても言及されてた。

## 設計における負債1: Glue Code (接着剤コード)

- 要するに、特定のパッケージに特化した Glue Code (接着剤コード)の大量発生が負債になるよ、って話っぽい...!:thinking:
- ML研究者は、手法を一般化した**汎用(general-purpose)パッケージ**を開発しがち。
- 汎用パッケージを使用すると、多くの場合、汎用パッケージにデータを入出力する為の大量のサポートコード(Glue Code)が発生しがち。
- Glue codeは長期的にはコストがかかる。
  - -> 特定の汎用パッケージの特異性にシステムを固定してしまい、他のパッケージへの移行が難しくなるから。
- 提案されてる解決策: 汎用パッケージを共通のAPIでwrapすること。(glue codeを閉じ込める、みたいな??:thinking:)

## 設計における負債2: Pipeline Jungles

- glue codeの特殊なケースとして、**pipeline jungles**は、データ準備段階においてしばしば現れる。
  - (**学習pipelineにおける前処理がめっちゃ生い茂ってしまう**、みたいなイメージ...??:thinking:) (元データとMLモデルを接着させるための処理だから、gule codeの一種と言ってるのかな...!:thinking:)
- 注意を払わないと、時間の経過や特徴量の追加とともに複雑化・肥大化したデータ処理pipelineが生まれる。
  - -> これがPipeline Jungles! 管理・エラー検出・障害からの回復にコストがかかる。システムの技術的負債 up up!
- 提案されてる解決策: データ収集と特徴量抽出について全体的(総体的)に考えよう!

Glue codeとPipeline Junglesの原因として、**“research”と“engineering”の役割が過度に分離されてる状況**が主張されてた。**エンジニアと研究者が同じチームに組み込まれる(or 同じ人が担う)ような環境**では、これらを防ぎやすいっぽい。

## 設計における負債3: Dead Experimental Codepaths(死んだ実験用コードパス)

- glue codeやpipeline junglesを放置していくほど、**実験用コードパスを本番コード内の条件分岐として実装すること**が魅力的になっていく。
- 短期的には、コストは低い。(周囲のサポートコードやインフラが再設計不要なので...!)
- しかし長期的に、これらのコードパスが蓄積されていくと...
  - 1. 後方互換性の維持が困難になる。(ex. 新しい特徴量や変更を条件分岐で加える度に、古いコードとの互換性を保つ事が困難になる、みたいな??:thinking:)
  - 2. cyclomatic complexityが増加する。(i.e. 条件分岐が増えると、コードの複雑さが指数関数的に増加して、コードの理解・テスト・デバッグ等が困難になる、みたいな?:thinking:)
- このアンチパターンの危険性の有名な例: Knight Capitalのシステムが45分で4億6500万ドルを失った。**原因は、時代遅れの実験用コードパスから予期しない振る舞いが発生したこと**。(怖い..!:thinking:)

## MLシステムにおける"common smells"

- smells(匂い)って?
  - -> ソフトウェア設計における問題点を指し示す可能性のある、コードやシステムの特徴やパターン、みたいな意味合いっぽい:thinking:
- 論文では、MLシステムにおける"common smells"として、以下の3つを挙げていた:
  - Plain-Old-Data Type Smell
  - Multiple-Language Smell
  - Prototype Smell

# ブログで推奨されてたFTI Pipelines Architectureについて

## 最初に: FTI Pipelines Architecture って何?

## 導入: 何をすべきかという明確なメンタルマップが必要っぽい

> Maps help us navigate the world, and communicate ideas, helping us get faster to our destination.
> 地図は私たちが世界をナビゲートし、アイデアを伝え、目的地により早く到達するのに役立つ。

- MLOpsにおける既存のメンタルマップは、様々な利害関係者から集めた要求をとりあえずシンクに入れ込んだ様なもので、MLシステム構築の現実を反映していない。
-

## GoogleのMLOps Map

Figure 8: Google’s MLOps Map to help you build ML Systems

## DatabricksのMLOps Map

Figure 9: Databricks MLOps map to build ML Systems

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
