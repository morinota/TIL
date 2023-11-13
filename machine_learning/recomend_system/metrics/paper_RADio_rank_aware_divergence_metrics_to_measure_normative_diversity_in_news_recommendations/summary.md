# RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations

published date: 13 October 2022,
authors: Sanne Vrijenhoek, Gabriel Bénédict, Mateo Gutierrez Granada, Daan Odijk, Maarten de Rijke
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## どんなもの?

ようするに「〇〇を目的としたニュースメディアを目指す場合、☓☓と△△のdiversity metricのスコアが高い推薦システムを選ぶと良い」みたいなdiversity metricsの使い方, モデルの選び方を提案する論文(と解釈してます...!).
RecSys2022 Best Paper Awardsを取得している論文らしい.

- 従来の推薦システムの文献では、**多様性(=記述的多様性/descriptive diversity)は単に類似性の反対と見なされる**ことが多く、一般に識別されたtopic、category、またはアイテム間の距離として定義される.
- しかしdescriptive diversityは、報道機関の規範や価値観を考慮した社会科学的な多様性(=**規範的多様性/normative diversity**と呼ぶことにする)を表現していない.
- 本論文は、normative diversityを表現する事を目的に、推薦システムを評価するための汎用的な metrics framework である**RADio**を提案する.
  - RADioは rank-awareな JS Divergence metric を採用し、DART metricsを拡張したもの.
- 本論文では、Microsoft News Datasetと6つの推薦アルゴリズムにおいて、**"notmative diversityにおける5つの概念(DART metricsの5つのmetric)**をニュース推薦システムがどの程度反映しているか"をRADioによって評価した.

## 先行研究と比べて何がすごい？

### Descriptive (General-Purpose) Diversity (記述的?(汎用的)多様性)

ニュース推薦における diversity に関する formal mathematical workの最近の研究について.
descriptive diversityは、本論文で対象にする"normative diversity"とは異なる解釈ではあるが、情報検索の文献[17, 62]では中心的な概念.

ニュース推薦システムの開発では、現在、**アルゴリズムの予測力**に大きな焦点が当てられる事が多い.
しかし、これでは、**ユーザが過去に接したことのあるコンテンツと類似したものを不当に促進し、"more of the same "のループにユーザを閉じ込めてしまう可能性がある**.
これに取り組むために，"**(descriptive?) diversity**"が導入される．これは，典型的には"**opposite of similarity**"(類似性の逆? ユーザの嗜好との類似性?)と定義される[11]．
その目的は、**ユーザが推薦リストで同じ種類のアイテムを表示されるのを防ぐこと**であり、しばしば intra-list-diversity (ILD)(推薦アイテムリスト間の平均pair-wise 非類似度)として表現される.(=diversity指標の計算に非類似度的な考えを用いているケースが多いから、"opposite of similarity"なのかな...? それとも順序が逆?).
**ILDはリスト間の距離関数を指定する必要がある(=2つのアイテム間の距離を何らかの方法で定量化する必要がある?)**ため、2つのリストが離れていることの意味については解釈次第となる.
理論的には，異なるsourcesや viewpoints の存在を考慮した指標で解釈することも可能だが、実際には2つのbag-of-wordsモデルや単語埋め込みのcosine similarityのような**descriptiveなdistance metricとして実装されることがほとんど**.

多様性に関連する他の人気のある **"beyond-accuracy(精度を超えた)"メトリクス** は、以下がある:

- **novelty(新規性)**(ユーザーが過去に見たものとこのアイテムがどれだけ違うか).
- **serendipity**(ユーザーがこのアイテムにポジティブに驚いたか).
- **coverage**(少なくとも1人のユーザに推薦された記事の割合).

このような descriptiveなdiversity の概念は，推薦システムにおいて以下の**４つの時点**で対応する事が可能:

- (i)学習前に，JS divergence [27]を用いてプロファイルの多様性に基づいてユーザをクラスタリングする，
- (ii)学習時に直接最適化する（例：learning-to-rank [10, 13, 70], collaborative filter [60], graph [30, 59] or bandits [21, 84].
- (iii) 推薦セットの再ランク付けを行い、diversity と relevance(=既に観測されたユーザのpreferenceとのrelevance??)のバランスをとる [16]、あるいは popularity と relevance のバランスをとる [15].
- (iv) 推薦後のmetricを定義し、推薦セットごとあるいはユーザ単位で多様性を測る(ex. generalist-specialist score [2, 73])

この4つの方法のいずれにおいても、ユーザに提示する推薦の relevance とdescriptive diversity のレベルはトレードオフの関係にあるが、**diversityを高めることが必ずしもrelevanceに悪影響を与える必要はない**ことを示す研究もある[48].
しかし、近年では、**diversity と accuracy のトレードオフを明示的に行う**ニューラル・ベース・レコメンダーが注目されている[61].
また、最近では、ユーザの多様性ニーズを区別する研究も行われている[83].

### Normative Diversity (規範的多様性)

本論文で対象とする方のdiversity.
このdiversityは、normative conceptとして文献で広く議論されており、生態系の多様性から機械学習システムにおける公平性の代理としての多様性[51]まで、科学の多くの異なる分野で役割を担っている[46, 65].
これらの多様性の解釈はしばしば関連しているが，**民主主義理論や社会におけるメディアの役割**に由来する，**diverseなニュース推薦システム**のニュアンスを完全にカバーするものではない.

Helberger [33]に従い、本論文では**normatively diverseなニュース推薦**を、"ユーザに情報を提供することに成功し、民主主義社会における役割を果たすことを支援するもの"と定義する.
文献に存在する多くの理論モデルのうち、Helberger [33]は、民主主義のnormative framework から**4つの異なるモデル**を説明し、それぞれ、市民に適切に情報を提供することの意味について異なる見解を示している:

- 1. Liberal model(自由主義モデル):
  - 個人の成長と自律を可能にする事を目的とする.
- 2. Participatory model(参加型モデル):
  - 民主主義社会における積極的な市民としての役割をユーザが果たせるようにする事を目的とする.
- 3. Deliberative model(審議型モデル):
  - 異なる視点や意見を合理的かつ中立的に平等に提示し、議論や討論を促す事を目的とする.
- 4. Critical model(批判モデル):
  - 現状に挑戦し、社会の既存の不公平に対して行動を起こすように読者を鼓舞する事を目的とする.

各モデルの詳細や、**各モデルに従った推薦システムがどのようなものか**については、Helberger [33]を参照してください.
**どのモデルに従うかは、報道機関自身が決定すべきこと**であり、そのnorm(規範)やvalues(価値観)に沿ったものであるべきである.

これらのモデルに基づいて、**DART Metrics** [71] は推薦システムのためのnormative diversity への第一歩を踏み出し、上述した異なる民主主義モデルのニュアンスを反映させたものである:

- Calibration
- Fragmentation
- Activation
- Representation
- Alternative Voices.

表1は、DART Metricsの概要と、"各モデルにおいてDART Metricsはこうあるべき"という期待値の範囲を示している.

![](https://camo.qiitausercontent.com/1bbf04c0c8066b3684e4d381f227b3077ab27a16/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f38303865313663382d623131312d616438612d356461612d3661663562646332383331302e706e67)

### Normative diversity と Descriptive Diversity の gap

前述した**descriptive diversity metrics は汎用的であり、すべての推薦のドメインに適用できる**ことを意図している.
しかし、**その単純さゆえに、この多様性の解釈と、セクション2.2で詳述するメディアの多様性に関する社会科学の観点との間に大きなギャップが見られる**.
そのため、従来の情報検索に基づく評価基準[17, 62]では多様性で高得点を得られる推薦システムも、ニュースルームの編集者が保持する基準では多様性があるとは見なされない可能性がある. (i.e. **diversityの評価方法がまちまちだって話!**)
Loecherbachら[46]とBernsteinら[7]は、このギャップを埋めるために真に学際的な研究を求めており、Bernsteinら[7]は、学術界と産業界の密接な協力と共同ラボの創設を主張している.

本論文はその方向への一歩であり、、**実務家がNormative diversityをモニタリングするために使用できる、汎用的で数学的根拠のある rank-aware metric**を提供する.

## 技術や手法の肝は？

本論文が提案するRADioフレームワークは、Vrijenhoekら[71]が定義した**DART Metrics をさらに改良**したものである.

RADioフレームワークは、DART metricsの欠点をいくつか解決している:

- metric によって異なる value ranges.
  - ex) Activationは[-1, 1]の値域を持ち、スコアが高いほどactivatingなコンテンツの程度が高いことを示し、Calibrationは[0, ∞]の範囲を持っており、スコアが低いほどCalibrationが良いことを示している.
  - **異なる value ranges は、metricsの解釈可能性を低下させ、説明が難しくなり、その結果、ニュース編集者が採用する可能性が低くなる**.
- 推薦における記事の位置を考慮に入れていない点.
  - ニュース推薦は通常、推薦された記事がユーザによって読まれる可能性がランキングの下方に行くほど低くなるようにランク付けされたリスト.
  - -> 推薦システムの diversity を評価する際には、集合全体(ILDなど)を考慮するのではなく、**推薦ランキングにおける記事の位置**も考慮する必要がある.

上の２つの欠点を解決する為に、以下の事を考慮してRADioフレームワークを提案する.

- (i) metrics間および推薦システム間でスコアが比較可能であること.
- (ii) ランク付けされていない推薦セットとランク付けされた推薦セットの両方の定量評価が可能である事.

### ニュース推薦のmetricに望ましい基準を設定する.

ニュース推薦metricに望ましい、3つの基準を設定する.

**distance metric** の古典的な定義は以下.

- 確率変数の集合$X$をとり、$x, y,z \in X$とすると、以下の3つの条件を満たす時、distance measureが適切であると言える:
  - $D(x,y)=0 <=> x = y$: 同一性(identity)
  - $D(x,y) = D(y,x)$: 対称性(symmetry)
  - $D(x,y) \leq D(x,z) + D(z,y)$: 三角形の不等式(triangle inequality)

上に加えて、(i)異なる推薦アルゴリズムの比較のために、value rangeが[0; 1]である事, (ii)異なる多様性の側面を公正に考慮するために統一されたvalue rangeである事, (iii)rank付けされた推薦設定に合うように、離散的なrank-based distributionのセットへ適用可能な指標である事, を条件として設定する.

### f-Divergence

diversity を定量化する作業は、**確率分布の比較としてモデル化される**:
つまり、出力された推薦($Q$)とそのcontext($P$)の間の分布の違いである.

各 diversity metric は独自の $Q$ と $P$ を設定している.
分布Qの要素は推薦アイテムである場合もあるが、topicsやviewpoints(?)の分布など、より高いレベルの概念である場合もある.
context $P$ は、利用可能なアイテムの全体的な供給量、reading history や明示的な好みなどのuser profile、他のユーザに発行された推薦結果のいずれかを参照することができる(図1参照).

![](https://camo.qiitausercontent.com/fab3384dc55e20fc53bc5e14b3fe2c5f5c5c2e6b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f30626365306131662d666335632d353239632d643137662d6365393938303665613462632e706e67)

直感的には、P が Q と同じユーザにリンクされている場合、ユーザ内のdiversityを測定する(例えば、“filter bubbles”に閉じ込められるのを防ぐ事を目的に!).
$P$ が $Q$ 以外のユーザにリンクされている場合、ユーザ間のdiversityを測定する(例えば、パーソナライズされたwebページで表現されるviewpointsのdiversityを監視する.)

以下では、シンプルで一般的な **KL divergence metric** から始まり、その改良版(JensenShannonダイバージェンス)を本論文が推奨する metrics として提示する前に、2つの異なる metrics 設定における$P$と$Q$の役割を定式化する.

### 最もシンプルで一般的な KL divergence metric

2つの確率質量関数 Pと Q（ここではrecommendation と そのcontext）の間の**KL(Kullback-Leibler) divergence metric**［42］(relative entropyとも呼ばれる)の概念は次のように定義されている:

$$
D_{KL}(P, Q) = - \sum_{x\in X}{P(x)\log_{2}{Q(x)}}
+ \sum_{x\in X}{P(x)\log_{2}{P(x)}}
\tag{1}
$$

しばしば、$D_{KL}(𝑄) = H(P,Q) - H(P)$とも表され、$H(P,Q)$はPとQとのcross entropy、$H(P)$はPの entropy であるとする.
クロスエントロピーとKLダイバージェンスはともに、**probability distribution Q が reference probability distribution P からどれだけ離れているか**を測定するものと考えることができる.
$P = Q$のとき、$D_{KL}(P, Q) = D_{KL}(P, P) = 0$となり、distance metricの同一性を満たす.
一方で、cross entropy だけでは同一性は保証されない.(そうなの??)
これが cross entropy よりも KL divergence metricを好む主な理由である.

KL Divergence は 同一性(identity)の要件を満たすが、対称性(symmetry)と三角形の不等式(triangle inequality)は満たさない.
これらは、KL Divergenceをさらに改良させることで解決することができる.

### KL divergence の改良版: Jensen–Shannon Divergence.

KL divergence から段階を経て、**Jensen-Shannon (JS) divergence** に至る.
KLダイバージェンスはまず対称化され[37]、次に上界化(=upper boundを設定)され[45]、次のようにJS divergenceとして導出された:

$$
D_{JS}(P, Q) = - \sum_{x\in X}\frac{P(x)+Q(x)}{2} \log_{2}{\frac{P(x)+Q(x)}{2}}
\\
+ \frac{1}{2} \sum_{x\in X}{P(x)\log_{2}{P(x)}}
+ \frac{1}{2} \sum_{x\in X}{Q(x)\log_{2}{Q(x)}}
\tag{2}
$$

**基底対数2**を用いた場合、JS divergenceの境界は $0 \leq D_{JS}(P, Q) \leq 1$となる.
またEndres and Schindelin [26]は、$\sqrt{D_{JS}}$が、identity、symmetry、triangle inequality の性質を満たす適切な distance metric であることを示している.
以下、$D_{JS}$または JS Divergence と表記する場合、**log base 2**のJS定式化の平方根を暗黙に指すことになる.
(以下、$D_{JS}$または JS Divergence と表記する場合、**log base 2**のJS formulation の square root(平方根)を暗黙に指すとする.)

また、Liese and Vajda [44]は**f-Divergence**[$D_f$]を定義した：いくつかの divergence metrics の一般的な formulation である.(hogehoge-divergenceみたいなイメージ!)
その中には、JS divergence とKL divergence が含まれる. さらに本文では、**KL divergence とJS divergence の略記法として$D_f$を用いる**
離散形式の$D_f$は以下.

$$
D_f(P,Q) = \sum_{x}{Q(x)f(\frac{P(x)}{Q(x)})}
\tag{3}
$$

ここで、

- $f_{KL}(t) = t \log{t}$
- $f_{JS}(t) = \frac{1}{2}[(t+1)\log{\frac{2}{t+1}} +t \log{t}]$

とする. ($t$は関数fの入力値.)

また、metricsの指定ミス(??後述されてた)を避けるため[64]、$bar{P}$, $bar{Q}$と表記する.

$$
\bar{Q}(x) = (1 - a)Q(x) + a P(x), \\
\bar{P}(x) = (1 - a)P(x) + a Q(x),
\tag{4}
$$

ここで、aはゼロに近い小さな数である.
Qで表現され、Pで表現されないカテゴリ(例えば、ニューストピック)がある場合、$D_f$を人為的にゼロにすることを防ぐために$bar{P}$が使用される.
逆の場合(あるカテゴリが𝑃で表され、𝑄で表されない場合)、$bar{Q}$はゼロ除算を避けることができる.
確率分布全体 $bar{P}$ と $tar{Q}$ が適切な統計分布であり続けるために、$\sum_{x}\bar{P}(x) = \sum_{x}\bar{Q}(x) = 1$となるように正規化する.
notation(表記)の混雑を避けるため、以下の節では、$P$と$Q$は暗黙に$\bar{P}$と$\bar{Q}$を指すことにする.

### 工夫1: Rank-Aware な f-Divergence Metrics に改良する

本論文の工夫として、ランク付け推薦の設定に対応する為に、f-Divergence metrics の更なる reformulation を提案する.

Learning To Rank (LTR) の文献 [67, 85]、ひいては従来のdescriptive diversiyt metrics [13] では、ユーザが推薦ランクリストのさらに下のアイテムを見る可能性はかなり低くなる(i.e. inspection probabilitiesが低下する)ことがよく知られている.
また，ランキングはしばしばユーザとのrelevanceを反映するが，ニュースの場合は必ずしもそうではない(ex. ニュースのホームページのレイアウト次第?)ことに注意されたい.
本論文では、ランク付けされた推薦リストで下位の結果の重要性を重み付けするために、**PとQにオプションの discount 係数を付けてmetricを拡張する**.

ランキング関連性指標であるMean Reciprocal Rank (MRR) と Normalized Discounted Cumulative Gain (NDCG) は，LTR [14, 36]，**特にニュース推薦 [80] でよく用いられるrank-aware metrics である**.

rank-awareな$Q^∗$と任意でrank-awareな $P^∗$で、rank-awareなf-DivergenceメトリックであるRADioを定式化する.
LTRの文献に沿って、まず、推薦リストRの各アイテム $i$ を与えて、ランク付けされた推薦セット$Q^*$の 離散確率分布(=確率質量関数?)を定義する.

$$
Q^*(x) = \frac{\sum_{i} w_{R_i} 1_{i \in x}}{\sum_{i} w_{R_i}}
\tag{5}
$$

ここで、アイテム$i$のランクの重み$w_{R_i}$はdiscount形式(=rank-awareの方法)によって異なる.

- MMRの場合、$w_{R_i} = \frac{1}{R_i}$
- NDCGの場合、$w_{R_i} = \frac{1}{\log_{2}{R_i+1}}$
- $w_{R_i} = 1$の場合、$Q^∗$ はdiscountされない.(i.e. $Q^*=Q$)

**ニュース推薦では，スパース性バイアスが支配的な役割を果たす**. スクロール可能なニュース推薦ウェブサイト[40]のように，ユーザは大きなアイテムコレクションのごく一部とinteractionする.(これに関しては推薦問題全般に言える気がする)
そのため，**NDCGよりもMRRに基づく重み付けを選択**する.
これは，**NDCGよりもランキングに沿ってより重いdiscountを適用するため**である.
**後者は、ユーザがクエリに関連した特定の情報ニーズを持っており、したがってページをスクロールする傾向がより高い、クエリ関連のランキングに適している**、と言われていることに注意してほしい[14].(あーなるほど...! nDCGを使いがちだった...!!)

コンテキスト分布 $P$ がランク付けされた推薦リストである場合、同じようにdiscountされる.
$P$がユーザのreading history の場合（図1参照）、$P$ の割引率は時間と共に増加する：最近読んだ記事は、より昔に読んだ記事より高く評価される.
一方で、例えば$P$が利用可能な記事のプール全体である場合など、rank-awareを適用できない状況もある.
rank-awareな$Q^∗$と、任意でrank-awareな $P^∗$を用いて、**rank-awareなf-DivergenceメトリックであるRADioを定式化する**.

$$
D^*_{f}(P, Q) = \sum_{x} Q^*(x) f(\frac{P^*(x)}{Q^*(x)})
\tag{6}
$$

ここで、$Q^*(x)$ と $P^*(x)$ は複数の状況に対応する:例えば、$Q^*(c|R)$ は推薦セット$R$上のニュースカテゴリ $c$ のrank-aware分布である.
以下では、我々の普遍的なmetric の為に、各normative concept(=DARTの事?) of interest に従って、$P^*(x|\cdot)$ と$Q^*(x|\cdot)$ を設定する.

### 工夫2: RADioを用いて、DART metricsを拡張する

本論文では、RADioを用いて5つの DART metricsの formulation を拡張する.

まず以下の global parameters(=notation?)を定義する:

- $S$: 推薦システムが選択しうる(=推薦候補のアイテム?)ニュース記事のリストで、"supply"とも呼ばれる.
- $R: 推薦セットに含まれる記事のランク付けされたリスト.
- $H$: ユーザの reading history にある記事のリストで、新着順に表示される.

$R_{i}^u \in {1, 2, 3, \cdots}$ は、ユーザ$u$に対する推薦リストにおけるアイテム $i$のランクを意味する.
DART metrics は**ある時点の特定のユーザに対して定義される**ため、特に断らない限り、$R$ は暗黙的に$R^u$を意味する.

以下で、DART metricsの各metricをRADioを用いて拡張していく.
(DART metricsの詳細は、元論文を参照.)

#### １つ目:Calibration

Calibration (式7)は、推薦がユーザの好みにどの程度合っているかを測定する.
ユーザの好みは、reading history($H$)から推測される.
Calibration には、推薦記事のカテゴリーの divergence と complexity の2つの側面が考えられる.
前者はニュースのメタデータから抽出され、したがって本質的に categorical であると予想され、後者はlanguage modelを介して抽出されたビンの(categoricalな)確率的な尺度である.

$$
Calibration = Cal(P^*(c|H), Q^*(c|R)) = \sum_{c} Q^*(c|R) f(\frac{P^*(c|H)}{Q^*(c|R)})
\tag{7}
$$

#### ２つ目:Fragmentation

Fragmentation(式8)は、「共通の public sphere と言えるのか、それともユーザが自分たちのbubbleの中に存在しているのか」を反映している.
Fragmentationは、**各ユーザのレコメンデーションペア間のdivergence**として測定される. (=ユーザ$u$とユーザ$v$を比較する.)
ここでは、$P^*(e|R^u)$ をユーザ $u$ の推薦リスト $R$ に対するニュースイベント $e$ のrank-aware分布と考え、$Q^*(e|R^v)$ を別のユーザ $v$ の推薦リスト$R$ に対するニュースイベント $e$ のrank-aware分布と考える.
KLダイバージェンスは非対称である. すなわち、どのユーザの推薦をtarget distribution として，どのユーザの推薦をreference distributionとして選択するかによって，結果が異なることを意味する.(= $u$と$v$を入れ替えると結果が異なり得る. = distance metricの条件を満たせない!)
これを避けるために、パラメータ(=uとv)を入れ替えた**KLダイバージェンスの平均値**としてFragmentationスコアを計算する.(=これでdistance metricの条件を満たせる...!)
JSダイバージェンスはすでに対称性を持つため、他のmetricsと同様に実装されている.
理論的には、**Fragmentationでは、あるユーザの推薦結果を他のすべてのユーザの推薦結果と比較する必要がある**.
しかし、データ量が多く、計算時間が必要であるため、これは実現不可能である.
その代わりに、我々は**ユーザのペアをランダムにサンプリング**することを選択した.

$$
Fragmentation = Frag(P^*(e|R^u), Q^*(e|R^v))
= \sum_{e} Q^*(e|R^v) f(\frac{P^*(e|R^u)}{Q^*(e|R^v)})
\tag{8}
$$

#### 3つ目:Activation

off-the-shelf(市販?)のsentiment analysis(感情分析?)ツールの多くは、テキストを分析し、テキストがpositiveな感情を表現している(=ある出来事に対して、肯定的な記事?)場合は $(0、1]$、表現された感情がnegativeな場合(=否定的な記事?)は $[-1、0)$ 、完全に中立の場合は0の値を返す.
(Activationは 肯定的な記事ばっかり推薦してしまってないか、逆に否定的な記事ばっかり推薦してしまってないか、みたいな意味合いのmetric...??)
値が極端であればあるほど、表現されたpositive/negativeの感情が強いことを意味する.
[71]で提案されたように、本論文では1つの記事で表現された感情の高さ(?)、したがって activation のレベルを決定するための近似値として記事のabsolute sentiment score を使用する.
$P(k|S)$ は、その時点で利用可能だったアイテムプール内の(ビン詰め)記事$S$(=推薦可能アイテムリスト?)のActivation Score $k$ の分布を示す.
$Q^*(k|R)$ は、同様に、rank-aware推薦リスト分布(=一方で、推薦されたアイテムリスト?)におけるbinned のActivation scores について表現するもの.

$$
Activation = Act(P(k|S), Q^*(k|R))
= \sum_{k} Q^*(k|R) f(\frac{P(k|S)}{Q^*(k|R)})
\tag{9}
$$

(要するに、推薦可能なアイテムプール$S$と, 実際に推薦したアイテムリスト$R$において、記事アイテムのsentiment値の分布が異なっている場合-> 過度に、肯定的/否定的な記事ばっかり推薦してしまっていると言えそう.)

#### 4つ目:Representation

Representation(式10)は、**viewpointのdiversity(ex. 政治的トピックや政党の言及など)**の概念を近似することを目的としており、viewpointはカテゴリ的に表現される.
ここで、$p$ は特定の veiwpoint を意味し、$P(p|S)$ は記事プール全体におけるこれらの viewpoint の分布であり、$Q^*(p|R)$ は推薦セット内のveiwpoint の rank-aware分布を表現する.
(viewpointって各記事アイテムに紐づくcategoricalなメタデータなのかな?)

$$
Representation = Rep(P(p|S), Q^*(p|R))
= \sum_{p} Q^*(p|R) f(\frac{P(p|S)}{Q^*(p|R)})
\tag{10}
$$

#### 5つ目:Alternative Voices

Alternative Voices(式11)は、viewpoint diversity の一面を反映させるという意味で、**Representation metricと関連**している.
これは、**viewpoint の内容ではなく、viewpointの持ち主、特に"protected group(保護された集団?)"に属しているか否かに着目したもの**である.
このようなprotected/unprotected グループの例としては、非男性／男性、非白人／白人などがある.(なるほど...! あんまり日本だとイメージつかないなぁ...)
このアプローチは、推薦システムにおける balanced neighbourhoods(?)の実装に基づくもの[12].
$m$では、保護グループとnot保護グループの分布を指し、$m$ ∈ {Minority, Majority}とする.($m$はbinaryのcategorical変数?)
$P(m|S)$ と $Q^*(m|R)$ はそれぞれ、推薦可能アイテムプールと、rank-awareな推薦リスト分布における 保護/not保護 グループの分布(割合と表現しても問題なさそう...!)を表す.

$$
AlternativeVoices = AltV(P(m|S), Q^*(m|R))
= \sum_{m} Q^*(m|R) f(\frac{P(m|S)}{Q^*(m|R)})
\tag{11}
$$

## どうやって有効だと検証した?

TUP RADioの潜在的な有効性を実証するために、public datasetで実験した.

### dataset と 評価対象のアルゴリズム

MINDデータセット[80]には、2019年10月12日から11月22日の間にMSNニュースのニュース項目と、ランダムにサンプリングされ匿名化された100万人のユーザとのインタラクションが含まれている.
各interactionには、**どの記事がユーザに提示され、どれがクリックされたか**、ユーザのreading history をリスト化したインプレッションログが含まれている.

MINDデータセットは、このデータセットで学習されたニュース推薦アルゴリズムに関する性能比較を伴って公開され、その中にはニュース専用のニューラル推薦手法NPA [78]、NAML [77]、LSTUR [1] およびNRMS [79]が含まれている.
**これらのアルゴリズムは、特にニュースアイテムの寿命が短い(short lifespan)ことから、汎用的なもの[80]や一般的な協調フィルタリングモデル（交互最小二乗法（ALS）など）を凌駕することが示された**[31].
これらのアルゴリズムは、ユーザがどのアイテムをクリックする可能性が高いかを予測するために、インプレッション・ログに対して学習される.

本論文では、**これらのニューラル推薦法をRADioフレームワークで評価し**(DARTメトリクスで)、妥当な候補セット(元のimpressionログ)に基づく2つのナイーブなベースライン法(ランダム選択, アイテムの人気度をデータセットに記録されたクリック数で近似した、最も人気のあるアイテムからの選択)と性能を比較する.(かなりnaiveなbaselineと比較するんだ...!)

### 分析手法:

RADioはすべての${P, Q}$のペアの平均を計算するので、以下の感度分析で示されるように、我々は pair distance に対する信頼区間(=全てのPQペア毎でdart metricsが計算されるので、その平均とばらつきが取得できる)も取得する.

各記事のメタデータ(=DART metricsの計算に必要な情報)は 以下の5つのメソッドで取得される:

- (1) Complexity analysis:
- (2) Story clustering:
- (3) Sentiment analysis:
- (4) Named entity recognition:
- (5) Named entity augmentation:

We implement RADio with the pipeline above.
上記のようなパイプラインでRADioを実装する.
表2は、上記のメタデータ算出方法の番号付きリストとDART metrics をリンクさせたもの.
この実装のコードはオンラインで入手可能である.

我々は、異なる推薦戦略(LSTUR、NAML、NPA、NRMS、most popular, random)に対して、KL DivergenceとJensen-Shannon の両方を divergence metrics として、推薦における位置に対する discount の有無、異なるランキングカットオフでRADioフレームワークの結果を評価した.

### 実験結果:

全体的な結果についてコメントした後、異なるハイパーパラメータに対する感度分析を行い、この選択の動機付けをさらに行う.

表 3 は、RADIO の rank-aware JS divergence の結果を示している.
値が高いほど divergence スコアが高いことを意味するが、**各divergence スコア(=RADioで拡張された DART metricsスコア) の良し悪しは、推薦システムの目的に依存する**(後述).

![](https://camo.qiitausercontent.com/b29f57943b524983305cc8a30bb004b3252d2cdc/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f39366162323636362d393439362d636132362d393034342d3736646230306339346336652e706e67)

- randomレコメンダーはすべての指標で divergence のスコアが最も高く、また定義上 最も relevance(=ユーザの嗜好との?)の低いレコメンダーである(NDCG スコア参照).
- most popular レコメンダーと random の NDCG スコアは同程度.
  - 記事の人気度スコアはMINDのインタラクションログに記録されたクリック数から導かれ、多くの記事はゼロか1クリックしか記録されていない.
  - **候補リストに同程度のクリック数の記事しか含まれていない場合、most popular レコメンダーはランダムな選択を余儀なくされる.** -> NDCGスコアの観点から見ると、most popular と random の間に人工的な類似性がある原因.
- ニューラルレコメンダーのうち、LSTUR、NPA、NRMS、NAMLの divergence スコアはほとんどが低い範囲にある.
  - これらは似た推薦結果を生成する.(NDCG値およびWuら[80]を参照)
- ニューラルメソッドをベースラインと比較すると、いくつかの顕著な違いが観察される.
  - most popular ベースラインは complexity のCalibrationという点ではわずかに優れているが、**ニューラルレコメンダーは 人々のreading historyに存在するアイテムに対してよりCalibrationされている**ことが分かる.

以下では、さらに個々の推薦リストのdivergenceの分布全体を分析し、異なる設定に対するRADioの感度をテストする.

#### Sensitivity to the Divergence Metric

JS divergenceは、本論文が主張する universalなdiversity metricsである.
これは適切な distance metric であり、0と1の間で境界が設定されている.
図2はその主張を実証的に示しており、2つの f-Divergence metrics (KL-divergence, JS-divergence)に対するRADioの感度を可視化したものである.

![](https://camo.qiitausercontent.com/46c1a5ede8c7e74833f2fd0c5179446b97dd4ad0/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f34653436643638322d653037632d363863382d636636342d3430643063383337393430312e706e67)

KLダイバージェンスは低スコアに偏り、JSダイバージェンスはより中心的な値の分布となり、明確な違いが観察される.
さらに、JSダイバージェンスは、ニューラル推薦システムとナイーブ推薦手法、特にrandomベースラインとの間に、より多くの contrast を apply している.(=各推薦アルゴリズムの違いをより顕著に表現してる?)
MINDではサンプルが多いため、randomベースラインは diverse recommendation set の近似となる.(=理想的なdiversityを持ちうる?まあrandomだからそりゃそうか.)
KLは推薦モデル間の個々の $P, Q$ 比較ペアの分布に結果的に歪みをもたらすが、JSではそのようなことはない.
KL-Divergenceは多くのアプリケーションで見られる有名な metric であり、数学的に表現するのも簡単であるが、本論文は **JS-Divergence が理論的にも経験的にもより適合している**ことを発見した.

#### Sensitivity to Rank-awareness

DART metricsのオリジナルの定式化[71]では、定義された metrics のほとんどについて、rank-awareではなかった.
一方で、本論文が提案した定式化は、rank-awareである.
図3では、rank-aware無し Fragmentation(青)と、rank-aware有りFragmentation(オレンジ)の効果の比較結果を可視化している.

![](https://camo.qiitausercontent.com/33b2cbdef135215f69c25b39dbfee05127004b18/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f35636537653037392d353961642d363238392d383962362d3963656165303466626431322e706e67)

Rank-awarenessなmetricを使用する事で、手法間の区別がより明確になる.
rank-awareness無しmetric の場合、LSTURと most-popular 手法は、同じように分布しているように見える.
rank-awareness有りmetric の場合、LSTURはより大きな ivergenceにシフトするが、most-popular手法 はほとんど変わらない事が分かる.

#### Normative Evaluation

異なる推薦アルゴリズムの divergence スコアを比較することで、開発者は"推薦がユーザのニュース露出へ与える影響"について結論を得る事ができる.

divergence スコアを、DARTの民主主義に関するさまざまな理論モデル(表1)と組み合わせることで、どの推薦システムが他よりも"開発者が求める規範的スタンス"に適しているか、定量的情報に基づいた判断ができるようになる.

- ex)1: **Participatoryの規範と価値観を推薦に反映させることを目指す**公共サービスメディア機関:
  - Participatoryモデルは 低Fragmentationと低Activationを規定し、それはニューラルレコメンダーのスコアに示される.
  - ->ニューラルレコメンダーが、この組織の目的により適したモデルであると判断できる.
- ex)2: ある大きなメディア組織が、ウェブサイトの小さなセクションを**Criticalな規範と価値観を満たすようにしたい**と考え、そのセクションが"A different perspective "と呼ばれる推薦を含む1つの要素で構成されているとする.
  - Critical モデルでは、Representation と Alternative Voices の両方で高いdivergence スコアを要求している.
  - ↑の観点からは、random推薦が最も良いスコアを出す. この場合は、ニューラルレコメンダーを適用すべきでないと判断できる.(とはいえ、random推薦がCriticalな規範と価値観を満たしている、結論は無理がある...)

これらのスコアをさらに向上させるためには、追加のステップを踏む必要がある: 推薦アルゴリズムの開発者は、推薦における異なる目標値間のトレードオフを微調整したり、あるいはこれらの指標を明示的に最適化したりすることができる.

## 議論はある？

## 次に読むべき論文は？

- 本論文に出てきた ニュース推薦の短いlifespanに特化した 推薦手法 の論文
  - [NPA: Neural News Recommendation with Personalized Attention(2019)](https://arxiv.org/abs/1907.05559)
  - [NAML: Neural News Recommendation with Attentive Multi-View Learning(2019)](https://arxiv.org/abs/1907.05576)
  - [Neural News Recommendation with Multi-Head Self-Attention(2019)](https://aclanthology.org/D19-1671/)
  - [Neural News Recommendation with Long- and Short-term User Representations(2019)](https://aclanthology.org/P19-1033/)

## お気持ち実装

KL divergence, JS divergence, 推薦アイテムリストをrank-aware pmfに変換する処理, rank-awareな JS divergence metricの実装.

まずはテストコードから.(TDD! テストファースト開発!)

```python:test_metric.py
import math

from metric import (
    calc_f_JS_t,
    calc_JS_divergence,
    calc_KL_divergence,
    calc_rank_aware_JS_divergence,
    calc_rank_aware_pmf,
    calc_rank_weight_MMR,
    calc_rank_weight_nDCG,
)


def test_calc_KL_divergence() -> None:
    P = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q = {"a": 0.3, "b": 0.3, "c": 0.4}
    kl_div_PQ_expected = -(
        0.2 * math.log2(0.3) + 0.3 * math.log2(0.3) + 0.5 * math.log2(0.4)
    ) + (0.2 * math.log2(0.2) + 0.3 * math.log2(0.3) + 0.5 * math.log2(0.5))

    kl_div_PQ_actual = calc_KL_divergence(P, Q)
    assert math.isclose(kl_div_PQ_actual, kl_div_PQ_expected)


def test_calc_JS_divergence() -> None:
    P = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q = {"a": 0.3, "b": 0.3, "c": 0.4}

    js_div_first_term = (
        -(0.2 + 0.3) / 2 * math.log2((0.2 + 0.3) / 2)
        - (0.3 + 0.3) / 2 * math.log2((0.3 + 0.3) / 2)
        - (0.5 + 0.4) / 2 * math.log2((0.5 + 0.4) / 2)
    )
    js_div_second_term = (
        1 / 2 * (0.2 * math.log2(0.2) + 0.3 * math.log2(0.3) + 0.5 * math.log2(0.5))
    )
    js_div_third_term = (
        1 / 2 * (0.3 * math.log2(0.3) + 0.3 * math.log2(0.3) + 0.4 * math.log2(0.4))
    )
    js_div_PQ_expected = js_div_first_term + js_div_second_term + js_div_third_term

    js_div_PQ_actual = calc_JS_divergence(P, Q)
    print(js_div_PQ_actual)
    assert math.isclose(js_div_PQ_actual, js_div_PQ_expected)


def test_calc_rank_weight_nDCG() -> None:
    rank = 2
    rank_weight_expected = 1 / (math.log2(rank + 1))

    rank_weight_actual = calc_rank_weight_nDCG(rank)
    assert math.isclose(rank_weight_actual, rank_weight_expected)


def test_calc_rank_weight_MMR() -> None:
    rank = 2
    rank_weight_expected = 1 / (rank + 1)

    rank_weight_actual = calc_rank_weight_MMR(rank)
    assert math.isclose(rank_weight_actual, rank_weight_expected)


def test_calc_rank_aware_pmf() -> None:
    R = ["a", "b", "c"]
    Q_asterisk_expected = {
        "a": calc_rank_weight_MMR(1)
        / (calc_rank_weight_MMR(1) + calc_rank_weight_MMR(2) + calc_rank_weight_MMR(3)),
        "b": calc_rank_weight_MMR(2)
        / (calc_rank_weight_MMR(1) + calc_rank_weight_MMR(2) + calc_rank_weight_MMR(3)),
        "c": calc_rank_weight_MMR(3)
        / (calc_rank_weight_MMR(1) + calc_rank_weight_MMR(2) + calc_rank_weight_MMR(3)),
    }
    Q_asterisk_actual = calc_rank_aware_pmf(R)
    assert Q_asterisk_actual == Q_asterisk_expected


def test_calc_f_JS_t() -> None:
    t = 1
    f_JS_t_expected = 1 / 2 * ((t + 1) * math.log2(2 / (t + 1)) + t * math.log2(t))

    f_JS_t_actual = calc_f_JS_t(t)
    assert math.isclose(f_JS_t_actual, f_JS_t_expected)


def test_calc_rank_aware_JS_divergence() -> None:
    P_asterisk = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q_asterisk = {"a": 0.3, "b": 0.3, "c": 0.4}

    rank_aware_JS_div_expected = (
        0.3 * calc_f_JS_t(0.2 / 0.3)
        + 0.3 * calc_f_JS_t(0.3 / 0.3)
        + 0.4 * calc_f_JS_t(0.5 / 0.4)
    )
    rank_aware_JS_div_actual = calc_rank_aware_JS_divergence(P_asterisk, Q_asterisk)

    assert math.isclose(rank_aware_JS_div_actual, rank_aware_JS_div_expected)
```

中身の実装は以下.

```python: metric.py
import math
from collections import defaultdict
from typing import Any, Dict, List


def calc_KL_divergence(P: Dict[Any, float], Q: Dict[Any, float]) -> float:
    """ともに確率質量分布を想定.
    P: dictionary of probability distribution 1
    Q: dictionary of probability distribution 2
    """
    kl_div_P_Q = 0
    for x in P.keys():
        if P[x] > 0 and Q.get(x, 0) > 0:
            print(P[x], Q[x])
            kl_div_P_Q += -P[x] * math.log2(Q[x]) + P[x] * math.log2(P[x])
    return kl_div_P_Q


def calc_JS_divergence(P: Dict[Any, float], Q: Dict[Any, float]) -> float:
    js_first_term = 0
    js_second_term = 0
    js_third_term = 0
    for x in P.keys():
        P_x = P.get(x, 0)
        Q_x = Q.get(x, 0)
        if P_x <= 0 or Q_x <= 0:
            continue
        js_first_term += -(P_x + Q_x) / 2 * math.log2((P_x + Q_x) / 2)
        js_second_term += 1 / 2 * P_x * math.log2(P_x)
        js_third_term += 1 / 2 * Q_x * math.log2(Q_x)
    return js_first_term + js_second_term + js_third_term


def calc_rank_weight_nDCG(rank: int) -> float:
    return 1 / (math.log2(rank + 1))


def calc_rank_weight_MMR(rank: int) -> float:
    return 1 / (rank + 1)


def calc_rank_aware_pmf(R: List[Any]) -> Dict[Any, float]:
    rank_aware_pmf = defaultdict(float)
    rank_weights_sum = sum(
        [calc_rank_weight_MMR(rank) for rank in range(1, len(R) + 1)]
    )
    for rank_idx in range(len(R)):
        rank = rank_idx + 1
        rank_aware_pmf[R[rank_idx]] = calc_rank_weight_MMR(rank) / rank_weights_sum
    return rank_aware_pmf


def calc_f_JS_t(t: float) -> float:
    return 1 / 2 * ((t + 1) * math.log2(2 / (t + 1)) + t * math.log2(t))


def calc_rank_aware_JS_divergence(
    P_asterisk: Dict[Any, float],
    Q_asterisk: Dict[Any, float],
) -> float:
    rank_aware_JS_div = 0
    for x in P_asterisk.keys():
        P_x = P_asterisk.get(x, 0)
        Q_x = Q_asterisk.get(x, 0)
        if P_x <= 0 or Q_x <= 0:
            continue
        rank_aware_JS_div += Q_x * calc_f_JS_t(P_x / Q_x)

    return rank_aware_JS_div
```
