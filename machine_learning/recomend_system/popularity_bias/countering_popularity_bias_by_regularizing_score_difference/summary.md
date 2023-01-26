はじめに, 本記事は論文読み会で発表した内容になります.

# Countering Popularity Bias by Regularizing Score Differences

published date: 13 September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url: https://dl.acm.org/doi/fullHtml/10.1145/3523227.3546757
(勉強会発表者: morinota)

---

## どんなもの?

- 多くの推薦システムでは、人気のアイテム(="short-head"なアイテム)は頻繁に推薦され、人気のないニッチなアイテム("long-tail"なアイテム)はほとんどor全く推薦されないという、Popularity Bias(人気度バイアス)に悩まされている.
- popularity biasは二種類に分けられる.
  - data bias: 多くの場合、学習データはアイテムの人気度においてロングテール分布を示している
  - model bias: 推薦システムは、ユーザが同じように好きなアイテムであっても、人気のあるアイテムに不当に高い推薦スコアを与えることがあり、その結果、人気のあるアイテムを過剰に推薦してしまう.
  - さらに，このような偏った推薦が feedback loop(?) を形成し，filter bubble やecho chamber(?)を引き起こす可能性がある.
    - feedback loop: 推薦結果をユーザに提供した際のfeedbackを受け取り、その結果を次の推薦に反映する事.
    - filter bubble: 推薦システムにより**ユーザが得られる情報が集約**されていく事. (それがユーザの嗜好と合致するバブルかは問わない)
    - echo chamber: 閉鎖的空間内でのコミュニケーションが繰り返されることにより、**特定の信念が増幅または強化されてしまう**状況の比喩.
- そこで本研究では，**ユーザが好むアイテム間で推薦スコアが等しくなるように直接正則化**することで，精度を維持したまま推薦結果の偏りを低減する新しい手法を提案する．

![Figure 1: The long-tail of item popularity. ](https://d3i71xaburhd42.cloudfront.net/6d77d7467f993780d02f3d8ea563959643d48f89/1-Figure1-1.png)

## 先行研究と比べて何がすごい？

既存手法は、精度向上と人気バイアス低減のトレードオフに悩まされる事が多い.

## どうやって有効だと検証した?

- ベースライン学習によりモデルの偏りを誘発する合成データセットを用いた実験.
- 4つのベンチマークデータセットと4つの推薦モデルを用いた実証実験.

## 技術や手法の肝は？

## 議論はある？

## 次に読むべき論文は？

- 情報検索における検索結果多様化の先行研究[Exploiting Query Reformulations for Web Search Result Diversification](https://dl.acm.org/doi/pdf/10.1145/1772690.1772780?casa_token=_NkfT8SH_V4AAAAA:mkjn91maD3dGMMF6GbfFSbmOqqa9tfqBDohAO26vAytPbVt0BQidOPWX0tL4EsUkRD00tJ-4CrMWAQ)
- regularized long-tail diversification algorithmに関する論文 [Controlling Popularity Bias in Learning to Rank Recommendation](https://dl.acm.org/doi/10.1145/3109859.310991

## 実装するとしたら、なんとなくこんな感じ...?
