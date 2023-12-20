# Bayesian Personalized Ranking from Implicit Feedback

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/pdf/2305.05585.pdf
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
  - 左辺の $E_{P(R_f)}[P(R_g|R_t)]$ の意味:
    - $P(R_f)$ に対する期待値。(=見方を変えると尤度関数??)
    - -> 観測された補助行動データ $R_g$ を用いて $P(R_f)$ を学習させるってこと。
  - 左辺の $KL[P(R_f)||P(R_t)]$ の意味:
    - $P(R_f)$ から $P(R_t)$ に情報を伝達しようとしてる? (KLダイバージェンスが小さくなるように学習させるから?)

また、式(8)の導出課程と同様に、KLダイバージェンス $KL[P(R_g) || P(R_t)]$ の式に、式(7)の1段目の式を代入して以下の等式が得られる。

$$
E_{P(R_g)}[P(R_f|R_t)] - KL[P(R_g) || P(R_t)] = \log P(R_g) - KL(P(R_g)||P(R_t|R_f))
$$

- 上述の2つの式(式8と上式)では、真のユーザ嗜好分布 $P(R_t)$ と推薦モデル $t_{\theta}$ の学習には活用できない。
- そこで、式4の仮定「学習が収束した時、ターゲット行動および補助行動から学習された嗜好分布 $P(R_f)$ と $P(R_g)$ は、それぞれ真の嗜好分布 $P(R_t)$ に近くなっているはず」を活用する。
  - -> 2つの式内の$P(R_f)$ に対する期待値、$P(R_g)$ に対する期待値をそれぞれ $P(R_t)$ に対する期待値に置き換えることで、$P(R_t)$ と $t_{\theta}$ の学習に活用できそうになる...!
  - 置き換えたver.の式が以下。 (左辺の期待値を置き換えたので、$=$ が $\approx$ に変わってる...!)

$$
E_{P(R_t)}[log P(R_g|R_t)] - KL[P(R_f)||P(R_t)]
\approx
log P(R_g) - KL[P(R_f)||P(R_t|R_g)]
\tag{9}
$$

$$
E_{P(R_t)}[log P(R_f|R_t)] - KL[P(R_g)||P(R_t)]
\approx
log P(R_f) - KL[P(R_g)||P(R_t|R_f)]
\tag{10}
$$

- 式9の左辺と式10の左辺を組み合わせると、以下の損失関数ができあがる。

$$
L = - E_{P(R_t)}[log P(R_g|R_t)] + KL[P(R_f)||P(R_t)]
\\
- E_{P(R_t)}[log P(R_f|R_t)] + KL[P(R_g)||P(R_t)]
$$

- 損失関数の意味:
  - データ観測値の尤度 ($P(R_g|R_t)$ と $P(R_f|R_t)$, $R_t$ がパラメータ側:thinking:) を最大化しようとする。
  - かつ、異なる行動データから学習された嗜好分布間 ($P(R_f)$ と $P(R_t)$)のKLダイバージェンスを最小化しようとする。(直接2つの分布の距離を最小化しょうとするんじゃなくて、間に $P(R_t)$ を挟んでる)

### 学習プロセス

- 2種類の行動データ $R_f$ と $R_g$ から、それぞれユーザの嗜好分布 $P(R_f)$ と $P(R_g)$ を学習する。
- 事前学習:
  - 学習の安定性を高めるため、$P(R_f)$ を $R_f$ で、$P(R_g)$ を $R_g$ で、それぞれ事前学習する。
  - 事前学習モデルとして、ターゲット・レコメンダー $t_{\theta}$ と同じモデル構造を使用する。
- メインの学習:
  - 情報伝達におけるKL-ダイバージェンスの役割を強化するために、KL-ダイバージェンスの有効性を高めるハイパーパラメータ $\alpha$ を損失関数に追加する。

$$
L_{MBA} = - E_{P(R_t)}[log P(R_g|R_t)] + \alpha KL[P(R_f)||P(R_t)]
\\
- E_{P(R_t)}[log P(R_f|R_t)] + \alpha KL[P(R_g)||P(R_t)]
\tag{12}
$$

- 損失関数内の期待値の導出方法(損失関数に学習させたいモデル $h$ を含めるステップ?):
  - 前述したように $R_f$ と $R_g$ には、異なる種類のノイズとバイアスが含まれた上で破損している。そのようなデータから真のユーザ嗜好を推論するために、以下のことを試みる。
    - $h^{f}_{\phi}(u,i)$ と $h^{f}_{\varphi}(u,i)$ を用いて、真のユーザ嗜好と観測されたターゲット行動データ間の相関を捉える。
    - $h^{g}_{\phi'}(u,i)$ と $h^{g}_{\varphi'}(u,i)$ を用いて、真のユーザ嗜好と観測された補助行動データ間の相関を捉える。
  - 具体的には、**損失関数内の2つの期待値をそれぞれ以下のように展開**する。

$$
E_{P(R_t)}[log P(R_g|R_t)]
= \sum_{u,i} E_{r^{t}_{u,i} \sim P(R_t)} [log P(r^{g}_{u,i}|r^{t}_{u,i})]
\\
\because \text{各事象 $r$ は独立に発生すると仮定すると、同時確率は積で表せる。logなので和になるので $\sum$ で展開できる}
\\
= \sum_{(u,i)|r^{g}_{u,i}=1} [log P(r^{g}_{u,i}|r^{t}_{u,i})]
+ \sum_{(u,i)|r^{g}_{u,i}=0} [log P(r^{g}_{u,i}|r^{t}_{u,i})]
\\
\because \text{binary確率変数 $r^{t}_{u,i}$ の期待値なので、$r^{t}_{u,i} = 1$ の時と $r^{t}_{u,i} = 0$ の時の条件付き確率の和に展開できる。}
\\
= \sum_{(u,i)|r^{g}_{u,i}=1} [log (1-h^{g}_{\varphi'}(u,i)) t_{\theta}(u,i) + log h^{g}_{\varphi'}(u,i) (1-t_{\theta}(u,i))]
\\
+ \sum_{(u,i)|r^{g}_{u,i}=0} [log (1-h^{g}_{\phi'}(u,i)) t_{\theta}(u,i) + log h^{g}_{\phi'}(u,i) (1-t_{\theta}(u,i))]
\\
\because \text{条件付き確率 $P(r^{g}_{u,i}|r^{t}_{u,i})$ をそれぞれ展開してる?}
\\
\tag{13}
$$

同様に、

$$
E_{P(R_t)}[log P(R_f|R_t)]
\\
= \sum_{(u,i)|r^{f}_{u,i}=1} [log (1-h^{f}_{\varphi}(u,i)) t_{\theta}(u,i) + log h^{f}_{\varphi}(u,i) (1-t_{\theta}(u,i))]
\\
+ \sum_{(u,i)|r^{f}_{u,i}=0} [log (1-h^{f}_{\phi}(u,i)) t_{\theta}(u,i) + log h^{f}_{\phi}(u,i) (1-t_{\theta}(u,i))]
\\
\tag{14}
$$

### alternative(交互?)なモデルトレーニング:

- 学習時に式12~14を用いて$t_{\theta}$を直接学習するといまいちだったらしい。
  - ->5つのモデルが同時に更新されるかららしい(i.e. $h^{g}_{\phi'}, h^{g}_{\varphi'}, h^{f}_{\phi}, h^{f}_{\varphi}, t_{\theta}$)
  - 5つのモデルは互いに干渉し合い、$t_{\theta}$ (=真に得たいモデル) の学習を妨げる可能性がある。
- この問題に対処するため、**2つの代替学習ステップを設定し、関係するモデルを反復的に学習する**。(ALS的に、片方のモデルを固定して、交互に学習する感じ?)

#### ステップ1:

- 仮定「ユーザが嫌いな商品はクリックしない or 購入しない傾向がある」に基づく。
  - i.e. 真の嗜好 $r^{t}_{u,i}= 0$ の場合、$r^{f}_{u,i} \approx 0$ と $r^{g}_{u,i} \approx 0$ が成立する、つまり $h^{f}_{\varphi} \approx 0$ と $h^{g}_{\varphi'} \approx 0$ が成立する。
  - よってステップ1では、3つのモデル $h^{f}_{\varphi}, h^{g}_{\varphi'}, t_{\theta}$ のみを学習させる。
- この場合、導出した2つの期待値の式(式13と式14)は以下のように変形できる。

式13の変形:

$$
E_{P(R_t)}[log P(R_g|R_t)] = L_{CN} + L_{CP}
\\
where
\\
L_{CN} = \sum_{(u,i)|r^{g}_{u,i}=0} log (1-h^{g}_{\varphi'}(u,i)) t_{\theta}(u,i)
\\
L_{CP} = \sum_{(u,i)|r^{g}_{u,i}=1} log h^{g}_{\varphi'}(u,i) t_{\theta}(u,i) - C_1 \cdot (1 - t_{\theta}(u,i))
\tag{15}
$$

CNとCPは、click positiveとclick negativeの略かな。

同様に式14の変形:

$$
E_{P(R_t)}[log P(R_f|R_t)] = L_{PN} + L_{PP}
\\
where
\\
L_{PN} = \sum_{(u,i)|r^{f}_{u,i}=0} log (1-h^{f}_{\varphi}(u,i)) t_{\theta}(u,i)
\\
L_{PP} = \sum_{(u,i)|r^{f}_{u,i}=1} log h^{f}_{\varphi}(u,i) t_{\theta}(u,i) - C_1 \cdot (1 - t_{\theta}(u,i))
\tag{16}
$$

ここで、$C_1$ は、$- \log h^{g}_{\phi'}(u,i)$ と $- \log h^{f}_{\phi}(u,i)$ を置き換えるための大きな正のハイパーパラメータである。(ステップ1では、２つの予測モデル $h^{g}_{\phi'}, h^{f}_{\phi}$ は学習しないから...!)

#### ステップ2:

- 仮定「ユーザが気に入った商品をクリック and 購入する傾向がある」に基づく。
  - i.e. 「真の嗜好 $r^{t}_{u,i}= 1$ の場合、$r^{f}_{u,i} \approx 1$ と $r^{g}_{u,i} \approx 1$ が成立する」
  - -> $h^{f}_{\phi} \approx 1$ と $h^{g}_{\phi'} \approx 1$ が成立する
  - よってステップ2では、3つのモデル $h^{f}_{\phi}, h^{g}_{\phi'}, t_{\theta}$ のみを学習させる。
- この場合、導出した2つの期待値の式(式13と式14)は以下のように変形できる。

まず式13の変形:

$$
E_{P(R_t)}[log P(R_g|R_t)] = L_{CP}' + L_{CN}'
\\
where
\\
L_{CP}' = \sum_{(u,i)|r^{g}_{u,i}=1} log h^{g}_{\phi'}(u,i) (1 - t_{\theta}(u,i))
\\
L_{CN}' = \sum_{(u,i)|r^{g}_{u,i}=0} C_2 \cdot t_{\theta}(u,i) + log (1 - h^{g}_{\phi'}(u,i)) (1 - t_{\theta}(u,i))
\tag{17}
$$

同様に式14の変形:

$$
E_{P(R_t)}[log P(R_f|R_t)] = L_{PP}' + L_{PN}'
\\
where
\\
L_{PP}' = \sum_{(u,i)|r^{f}_{u,i}=1} log h^{f}_{\phi}(u,i) (1 - t_{\theta}(u,i))
\\
L_{PN}' = \sum_{(u,i)|r^{f}_{u,i}=0} C_2 \cdot t_{\theta}(u,i) + log (1 - h^{f}_{\phi}(u,i)) (1 - t_{\theta}(u,i))
\tag{18}
$$

ここで、$C_2$ は、$- \log (1 - h^{g}_{\varphi'}(u,i))$ と $- \log (1 - h^{f}_{\varphi}(u,i))$ を置き換えるための大きな正のハイパーパラメータ。(ステップ2では、２つの予測モデル $h^{g}_{\varphi'}, h^{f}_{\varphi}$ は学習しないから...!)

### 学習手順

サンプリングとトレーニングの手順をまとめる上で、２つの期待値 $E_{P(R_t)}[log P(R_g|R_t)]$ と $E_{P(R_t)}[log P(R_f|R_t)]$ を4つの部分に分ける(式.15-式.18を参照):

- click positive loss $L_{CP}$ と $L'_{CP}$
- click negative loss $L_{CN}$ と $L'_{CN}$
- purchase positive loss $L_{PP}$ と $L'_{PP}$
- purchage negative loss $L_{PN}$ と $L'_{PN}$

- 学習データセットの各サンプルは3つの状況のいずれかに分類でき、各状況に応じて、2つの期待値 $E_{P(R𝑡)}[log P(R_g|R_t)]$ と $E_{P(R_t)}[log P(R_f|R_t)]$ の項が異なる:
  - (i) クリックされかつ購入された
    - click positive loss と purchase positive loss を含む。
    - (i.e. ステップ1では、$L_{CP}$ と $L_{PP}$、ステップ2では、$L'_{CP}$ と $L'_{PP}$)
  - (ii) クリックされたが購入されなかった
    - click positive loss と purchase negative loss を含む。
    - (i.e. ステップ1では、$L_{CP}$ と $L_{PN}$、ステップ2では、$L'_{CP}$ と $L'_{PN}$)
  - (iii) クリックされず購入されなかった。
    - click negative loss と purchase negative loss を含む。
    - (i.e. ステップ1では、$L_{CN}$ と $L_{PN}$、ステップ2では、$L'_{CN}$ と $L'_{PN}$)
- 状況(i)と(ii)で観測された複数種類のユーザ行動データに従ってMBAを訓練し、状況(iii)のサンプルをnegativeサンプルとして使用する。

![algo1]()

学習手順の詳細は以下のアルゴリズム1:

- 観察可能な振る舞い:
  - 入力値:観測されたmulti-bahaviorデータセット $R_f$ と $R_g$, ハイパーパラメータ $\alpha, \beta, C_1, C_2$
  - 出力値: 全てのモデルパラメータ $\theta, \phi, \phi', \varphi, \varphi'$
- 実装の詳細:
  - while coverage (=特定の学習目標が達成されるまで繰り返す)
    - training exampleのサンプリング
    - 損失関数の項の一つ $L_{KL}$ を計算する。
    - alternative trianingのステップ1:
      - サンプルの3つの状況に応じて、$L_{KL}, L_{CP}, L_{CN}, L_{PP}, L_{PN}$ を使って損失関数の値を計算する。
      - モデルパラメータ $\theta, \varphi, \varphi'$ を更新する。
    - alternative trianingのステップ2:
      - サンプルの3つの状況に応じて、$L_{KL}, L'_{CP}, L'_{CN}, L'_{PP}, L'_{PN}$ を使って損失関数の値を計算する。
      - モデルパラメータ $\theta, \phi, \phi'$ を更新する。

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
