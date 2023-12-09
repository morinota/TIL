# Bayesian Personalized Ranking from Implicit Feedback

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## どんなもの?

## 先行研究と比べて何がすごい？

## 技術や手法の肝は？

以下は本論文のnotation

- ユーザ $u \in U$, アイテム $i \in I$
- クリック行動をauxiliary behavior, 購買行動をtarget behaviorとする。
- 観測された購買行動データ $R_f \in \mathbb{R}^{|U| \times |I|}$
  - 要素 $r^{f}_{u,i}$ が1なら購買行動が観測、0なら未観測。
  - 購買行動データ $R_f$ から学習されたユーザ嗜好分布: $P(R_f)$
- 観測されたクリック行動データ $R_g \in \mathbb{R}^{|U| \times |I|}$
  - 要素 $r^{g}_{u,i}$ が1ならクリック行動が観測、0なら未観測。
  - クリック行動データ $R_g$ から学習されたユーザ嗜好分布: $P(R_g)$
- 潜在的な真のユーザ嗜好行列を $R_t$、$R_t$ の確率分布を $P(R_t)$ とする。
  - 嗜好行列の各要素 $r^{t}_{u,i}$ が1なら好き、0なら嫌い。
  - 観測データ $R_f$ と $R_g$ は、$P(R_t)$ と、異なる種類のノイズやバイアスに依存して生成されると仮定する。
  - $P(R_t)$ はベルヌーイ分布に従い、ベルヌーイ分布のパラメータを予測モデル $t_{\theta}$ で近似できると仮定する。

$$
r^{t}_{u,i} \sim Bernoulli(t_{\theta}(u,i))
\tag{1}
$$

- 真のユーザ嗜好 $r^{t}_{u,i}$ は観測不可能。観測された $r^{f}_{u,i}$ と$r^{g}_{u,i}$ を教師ラベルとして扱い $r^{t}_{u,i}$ を推論する必要がある。
- よって、**観測された各種implicit feedback(i.e. $r^{f}$ と $r^{g}$) と潜在的な真のユーザ嗜好 $r^{t}$ との相関を表す**ために以下のモデル(仮定)を導入。
  - 各式の左辺の意味。それぞれの確率的事象が、パラメータhogeのベルヌーイ分布に従って発生するよという仮定。
    - 「ユーザ $u$ のアイテム $i$ に対する真の嗜好がnegativeな条件で、購買が発生する事象」
    - 「ユーザ $u$ のアイテム $i$ に対する真の嗜好がpositiveな条件で、購買が発生する事象」
    - 「ユーザ $u$ のアイテム $i$ に対する真の嗜好がnegativeな条件で、クリックが発生する事象」
    - 「ユーザ $u$ のアイテム $i$ に対する真の嗜好がpositiveな条件で、クリックが発生する事象」

$$
r^{f}_{u,i} | (r^{t}_{u,i} = 0) \sim Bernouli(h^{f}_{\phi}(u,i))
\\
r^{f}_{u,i} | (r^{t}_{u,i} = 1) \sim Bernouli(h^{f}_{\varphi}(u,i))
\\
r^{g}_{u,i} | (r^{t}_{u,i} = 0) \sim Bernouli(h^{g}_{\phi'}(u,i))
\\
r^{g}_{u,i} | (r^{t}_{u,i} = 1) \sim Bernouli(h^{g}_{\varphi'}(u,i))
\tag{2}
$$

上記のnotationを踏まえると、本論文が解きたいタスクは以下:

- 複数のimplicit feedbackの観測データ($R_f$ と $R_g$)を用いて、潜在的な真のユーザ嗜好モデル $t_{\theta}$ (=ベルヌーイ分布のパラメータを出力するモデル)を学習させたい。
- 学習した $t_{\theta}$ を用いて、ターゲット行動に関する予測性能を向上させたい。
  - (-> そしてターゲット行動をしてくれそうなアイテムを推薦したい...!:thinking:)
  - 推薦スコアの算出時は、ターゲット行動の推薦性能を向上させる為に、真の嗜好分布 $P(R_t)$ と、ターゲット行動データから学習された嗜好分布 $P(R_f)$ の両方を使用する。
  - $\beta$ は、$P(R_f)$ と $P(R_t)$のバランスをとるためのハイパーパラメータ。

$$
score = \beta P(R_t) + (1 - \beta)P(R_f)
\tag{3}
$$

### MBAの損失関数を導出する

MBA(Multi-Behavior Alignment)の重要な仮説は、「複数のタイプのユーザ行動が、同じユーザ嗜好を反映しているはず」という事。
(i.e. 異なるタイプのユーザ行動は、同一のユーザ嗜好分布から、それぞれ異なる度合いのバイアスとバリアンスを伴ってサンプリングされる、みたいな? :thinking: )
よって、めちゃめちゃ理想的でいい感じに学習できた場合には以下が達成されるはず...!

$$
P(R_f) \approx P(R_g) \approx P(R_t)
\tag{4}
$$

(i.e. 購買データから学習した嗜好分布だろうと、クリックデータから学習した嗜好分布だろうと、真の嗜好分布に似たものになるはず...! :thinking:)

よって、 $P(R_f)$ と $P(R_t)$ 、$P(R_f)$ と $P(R_t)$ のKLダイバージェンスはそれぞれ小さくなるはず。
(KLダイバージェンス=２つの分布間の距離が小さいほど0に近づく非負の指標:thinking:)

$$
KL[P(X)||P(Y)] = E_{P(X)}[log P(X) - log P(Y)]
$$

上記はKLダイバージェンスの式。(そうそう、KL-divはJS-divと違って、対称性を持たないんだった:thinking:)

ただ、２つのKLダイバージェンス $KL[P(R_f) || P(R_t)]$ と $KL[P(R_g) || P(R_t)]$ をnaiveに最小化しようとすると、データ分布のギャップや複数種類の行動間の相関を考慮できないのでいまいち。

この問題に対処するため、ベイズの定理を用いて 真の嗜好分布 $P(R_t)$ を以下のように置き換える:
(ベイズの定理って、同時確率が2通りの書き方ができる事から導出できるやつだよね...!)

$$
P(R_t, R_f) = P(R_t)\cdot P(R_f|R_t) = P(R_f)\cdot P(R_t|R_f)
\\
P(R_t, R_g) = P(R_t)\cdot P(R_g|R_t) = P(R_g)\cdot P(R_t|R_g)
\\
\therefore
P(R_t) = \frac{P(R_f) \cdot P(R_t|R_f)}{P(R_f|R_t)}
= \frac{P(R_g) \cdot P(R_t|R_g)}{P(R_g|R_t)}
\tag{7}
$$

ベイズの定理で置き換えた $P(R_t)$ を、２つのKLダイバージェンス $KL[P(R_f) || P(R_t)]$ と $KL[P(R_g) || P(R_t)]$ の式に代入すると、２つの等式が得られる。(論文中の式8ともう一つ)

まず式8。KLダイバージェンス $KL[P(R_f) || P(R_t)]$ の式に、式(7)の2段目の式を代入していく。

$$
KL[P(R_f) || P(R_t)] = E_{P(R_f)}[log P(R_f) - log P(R_t)]
\\
= E_{P(R_f)}[log P(R_f) - log (\frac{P(R_g) \cdot P(R_t|R_g)}{P(R_g|R_t)})]
$$

$$
= E_{P(R_f)}[\log P(R_f) - \log P(R_g) - \log P(R_t|R_g) + \log P(R_g|R_t)]
\\
\because \text{logの中身を展開}
\\
= E_{P(R_f)}[\log P(R_f) - \log P(R_t|R_g)] - E_{P(R_f)}[\log P(R_g)] + E_{P(R_f)}[P(R_g|R_t)]
\\
\because \text{和の期待値 -> 期待値の和}
$$

$$
= E_{P(R_f)}[\log P(R_f) - \log P(R_t|R_g)] - \log P(R_g) + E_{P(R_f)}[P(R_g|R_t)]
\\
\because \text{２つの嗜好分布は独立なので期待値の外に出せる}
$$

$$
\therefore
E_{P(R_f)}[P(R_g|R_t)] - KL[P(R_f) || P(R_t)] = \log P(R_g) - KL(P(R_f)||P(R_t|R_g))
\tag{8}
$$

- 式(8)についての解釈:
  - 左辺は、$\log P(R_g)$ のlower bound
    - KLダイバージェンスは非負なので。
    - このboundは、$P(R_f)$ と $P(R_t|R_g)$ が完全に一致する場合にのみ成立する。
    - = ターゲット行動の観測データから学習された嗜好分布 $P(R_f)$ と、補助行動の観測データで条件付けられた真の嗜好分布が完全に一致する場合。
    - -> この条件は、MBAの仮説「異なる行動データは、同一のユーザ嗜好を反映してるはず」に沿ったもの。
  - 左辺は $P(R_f)$ に対する期待値に基づいてる。
    - 観測された補助行動データ $R_g$ を用いて$P(R_f)$を訓練し (i.e. $E_{P(R_f)}[P(R_g|R_t)]$)、

また、式(8)の導出課程と同様に、KLダイバージェンス $KL[P(R_g) || P(R_t)]$ の式に、式(7)の1段目の式を代入して以下の等式が得られる。

$$
E_{P(R_g)}[P(R_f|R_t)] - KL[P(R_f) || P(R_t)] = \log P(R_g) - KL(P(R_f)||P(R_t|R_g))
$$

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
