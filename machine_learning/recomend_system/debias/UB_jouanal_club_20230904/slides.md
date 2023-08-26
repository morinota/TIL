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

title: 「ABテストする前に機械学習モデルの性能を評価できたら色々嬉しいよね。じゃあどのような方法で?」について色々調べている話
subtitle: 論文読み会
date: 2023/09/04
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 参考文献:

- 分かりやすいusaitoさんの資料: [Off-Policy Evaluationの基礎とOpen Bandit Dataset & Pipelineの紹介
  ](https://speakerdeck.com/usaito/off-policy-evaluationfalseji-chu-toopen-bandit-dataset-and-pipelinefalseshao-jie)
- netflixのtechブログ: [hoge]()
- 論文: [hoge]()
- MIPS推定量の論文: [hoge]()
- contextual bandit の論文: [hoge]()

## 今回のテーマを選んだ経緯

- hogehoge

## ABテストする前に機械学習モデルの良し悪しを評価できたらどんな点が嬉しい?

- hoge

## 仮にABテストする前に機械学習モデルの性能を全く評価できなかったら??

- hoge

# 調べた方法1. Off-Policy Evaluation 推定量を使う!

- hoge

# 調べた方法2. 凄く力技: オフライン評価指標達からオンライン性能を予測する回帰モデルを作る!

- hoge

# 調べた方法3. Netflixのtech blogで紹介されていた方法: ABテストの前にInterleaving

- hoge

# 調べた方法4. naiveだけど導入しやすさと効果は高そう: 一定期間のみ、一様ランダムなモデルを本番適用してログデータ収集

- hoge
