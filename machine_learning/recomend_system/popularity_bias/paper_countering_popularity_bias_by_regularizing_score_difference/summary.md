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
- そこで本研究では，**推薦システムが各ユーザーのポジティブアイテム間で等しい推薦スコアを予測する(=人気アイテムのスコアを過剰に高くしない)**ように、損失関数にregularization termを追加することで，精度を維持したまま推薦結果の偏りを低減する新しい手法を提案する．

![Figure 1: The long-tail of item popularity. ](https://d3i71xaburhd42.cloudfront.net/6d77d7467f993780d02f3d8ea563959643d48f89/1-Figure1-1.png)

## 先行研究と比べて何がすごい？

- 既存手法は、精度向上と人気バイアス低減のトレードオフに悩まされる事が多い.

- 既存のdebias化を目的としたregularization term手法は、"itemの人気度とポジティブitemのスコアとの間のピアソン相関の大きさにペナルティを課す"ようなアプローチ. (なるほど...既存研究とはregularization termのpenalize対象が異なるのか...!!)
  - しかし、相関係数を正則化しても独立(=itemの人気度と独立になるって意味??)になるとは限らないこと，**計算コストがかかる**こと，という2つの制約がある.
- positive item内とnegative item内のスコア差をそれぞれ最小化するregularization termを用いて，精度を維持しつつモデルの偏りを低減する方法を導入したのは，本研究が初めて.

## どうやって有効だと検証した?

1. ベースライン学習によりモデルの偏りを誘発する合成データセットを用いた実験.
  - 本研究では、model-biasとそれに続く様々な手法のdebias性能を説明するために、data-biasを明示した合成データを設計する.
  - 200 x 200のuser-item interaction matrix $R$
  - 式(4)を使って疑似データを生成: アイテム列のindexが増加するにつれてアイテムの人気が直線的に減少するように設定.
  - 行列は binary(0 or 1) のinteraction情報で満たされている.
  - このようなデータは、疎でノイズの多い実世界のデータからは逸脱しているが、**推薦システムがどのようにmodel-biasを生み出すか**を観察するには適切.
  - 
1. 4つのベンチマークデータセットと4つの推薦モデルを用いた実証実験.


## 技術や手法の肝は？

- $Pos_{u}$: ユーザ$u$がconsumeしたアイテムの集合
- $Neg_{u}$: ユーザ$u$がconsumeしなかったアイテムの集合.
- $\hat{y_{ui}}$: ユーザuがアイテムiに対して持つ予測嗜好に基づく推薦スコア(=推定されるパラメータ?)

既存のBRPの目的関数:

$$
Loss_{BPR} = - \sum_{u \in U} \sum_{p \in Po_{s_u}, n \in Ne_{g_u}} \log \sigma(\hat{y}_{u,p} - \hat{y}_{u,n})
\tag{1}
$$

- model-biasを測定するための指標: PopularityRank correlation for items (PRI, アイテムの人気度順位相関)
  - アイテムの人気度と平均ランキング位置の**Spearman rank correlation coefficient(SRC, スピアマン順位相関係数)**
  - SRC(スピアマンの順位相関係数):
    - 順位データから求められる相関の指標.(初めて聞いた...!)
    - $\rho = 1 - \frac{6 \sum D^2}{N^3 - N}$ で定義される.
    - ここで、$N$は値のペアの数. $D$は対応する変数Xと変数Yの値の**順位の差**
    - XとYの２つの順位の傾向が等しい=正の(線形)相関が強い場合は$\rho=1$に近づく.
    - [wikipediaより](https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%94%E3%82%A2%E3%83%9E%E3%83%B3%E3%81%AE%E9%A0%86%E4%BD%8D%E7%9B%B8%E9%96%A2%E4%BF%82%E6%95%B0)

$$
PRI = SRC (popularity(I), ave_rank(I))
\tag{2}
$$

- 各アイテムiの `ave_rank`: 各アイテムiについて、$Pos_{u}$にiを持つ各ユーザーuを探し出し、$Pos_{u}$内でのiのランク位置の分位数(=0 ~ 1?)を計算する. 次に、$Pos_{u}$内でiを持つ全てのユーザuの順位位置の分位数を平均する.
- PRIは、"アイテムの人気度"と"推薦モデルのスコアに基づく平均ランキング位置"のSRCなので...
  - PRI値が1に近い程、人気のあるアイテムに高いスコアを与えるモデル->model-biasが大きいと言える.
  - 0 に近いほど，ポジティブなアイテムの人気と推薦スコアランキングに相関がない. -> model-biasが小さいことを意味する．

また、各ユーザーのpositiveアイテムのスコア一位の平均人気度分位値（PopQ@1）を計算する指標を式(3)提案する.

$$
PopQ@1 = \frac{1}{|U|}\sum_{u\in U} \text{PopQuantile}_u(\argmax_{x\in Po_{s_u}}(\hat{y}_{ui}))
\tag{3}
$$

ここで,

- $\text{PopQuantile}_u$ : $Pos_{u}$内の、あるアイテムの人気度分位.
  - $Pos_{u}$内でグローバルな人気が最も高いアイテム-> $\text{PopQuantile}_u=0$
  - グローバルな人気が最も低いアイテム->$\text{PopQuantile}_u=1$
  - 各ユーザのpositiveアイテムのスコア一位は、通常(=model-biasを解決してないケース!)グローバルな人気が高いpositive itemになるので、` PopQ@1` が 0 に近い場合(=sumの合計値が小さい!)はmodel-biasが大きいことを意味する.
  - 一方、PopQ@1 の値が 0.5 に近い場合は、人気度分位が 0 と 1 の間に分散している可能性が高いため、model-biasがないことを意味する.

この2つの指標により、model-biasを詳細に評価することができる.

推薦システムにとって重要なことは、model-biasを抑えながら精度を維持すること. 
model-biasが少なくても精度が低ければ、個人に合った推薦を行うことはできない.
例えば、ランダムな推薦を行うモデルは、model-biasを示さないが、ユーザの嗜好を全く考慮しない.

## 議論はある？

## 次に読むべき論文は？

- 情報検索における検索結果多様化の先行研究[Exploiting Query Reformulations for Web Search Result Diversification](https://dl.acm.org/doi/pdf/10.1145/1772690.1772780?casa_token=_NkfT8SH_V4AAAAA:mkjn91maD3dGMMF6GbfFSbmOqqa9tfqBDohAO26vAytPbVt0BQidOPWX0tL4EsUkRD00tJ-4CrMWAQ)
- regularized long-tail diversification algorithmに関する論文 [Controlling Popularity Bias in Learning to Rank Recommendation](https://dl.acm.org/doi/10.1145/3109859.310991

## 実装するとしたら、なんとなくこんな感じ...?
