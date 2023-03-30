# RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations

published date: 13 October 2022,
authors: Sanne Vrijenhoek, Gabriel Bénédict, Mateo Gutierrez Granada, Daan Odijk, Maarten de Rijke
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## どんなもの?

- 従来の推薦システムの文献では、**多様性は単に類似性の反対と見なされる**ことが多く、一般に識別されたトピック、カテゴリ、または単語モデル間の距離として定義される.
- しかしこれは、**報道機関の規範や価値観を考慮した社会科学的な多様性**(=規範的多様性/normative diversityと呼ぶことにする)の解釈を表現していない.
- 本論文は、normative diversityを表現する事を目的に、推薦を評価するための汎用的な metrics framework である**RADio**を紹介する.
  - RADioはランクを考慮したジェンセン・シャノン（JS）ダイバージェンスを導入している.
- 本論文では、Microsoft News Datasetと6つの推薦アルゴリズムにおいて、**"notmative diversityにおける5つの概念**をニュース推薦がどの程度反映しているか"をRADioによって評価した.
- その結果、**RADioはニュース推薦システムの設計に利用できる可能性のある、洞察に満ちた推定値を提供する**ことがわかった.

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

## どうやって有効だと検証した?

TUP RADioの潜在的な有効性を実証するために、public datasetで実験した.

### dataset と 評価対象のアルゴリズム

MINDデータセット[80]には、2019年10月12日から11月22日の間にMSNニュースのニュース項目と、ランダムにサンプリングされ匿名化された100万人のユーザーとのインタラクションが含まれている.
各インタラクションには、どの記事がユーザーに提示され、どれがクリックされたか、ユーザーの読書履歴をリスト化したインプレッションログが含まれている.

MINDデータセットは、このデータセットで学習されたニュース推薦アルゴリズムに関する性能比較を伴って公開され、その中にはニュース専用のニューラル推薦手法NPA [78]、NAML [77]、LSTUR [1] およびNRMS [79]が含まれている.
**これらのアルゴリズムは、特にニュースアイテムの寿命が短い(short lifespan)ことから、汎用的なもの[80]や一般的な協調フィルタリングモデル（交互最小二乗法（ALS）など）を凌駕することが示された**[31].
これらのアルゴリズムは、ユーザがどのアイテムをクリックする可能性が高いかを予測するために、インプレッション・ログに対して学習される.

本論文では、**これらのニューラル推薦法をRADioフレームワークで評価し**(DARTメトリクスで)、妥当な候補セット(元の印象ログ)に基づく2つのナイーブなベースライン法(ランダム選択, アイテムの人気度をデータセットに記録されたクリック数で近似した、最も人気のあるアイテムからの選択)と性能を比較する.(かなりnaiveなbaselineと比較するんだ...! ALS等の一般的な推薦モデルとの比較でも良さそうな気がするが...!)

### 分析手法:

RADioはすべての${P, Q}$のペアの平均を計算するので、以下の感度分析で示されるように、我々はペアの距離に対する信頼区間も取得する.

各記事のメタデータは5つのメソッドでエンリッチされる:

- (1) Complexity analysis:
- (2) Story clustering:
- (3) Sentiment analysis:
- (4) Named entity recognition:
- (5) Named entity augmentation:

We implement RADio with the pipeline above.
上記のようなパイプラインでRADioを実装する.
表2は、上記の番号付きリストとDARTメトリクスをリンクさせたもの.
この実装のコードはオンラインで入手可能である.

我々は、異なる推薦戦略(LSTUR、NAML、NPA、NRMS、most popular, random)に対して、KL DivergenceとJensen-Shannonの両方をダイバージェンスメトリクスとして、推薦における位置に対する割引の有無、異なるランキングカットオフでRADioフレームワークの結果を評価した.

### 実験結果:

全体的な結果についてコメントした後、異なるハイパーパラメータに対する感度分析を行い、この選択の動機付けをさらに行う.

表 3 は、RADIO の rank-aware JS divergence の結果を示している.
値が高いほど divergence スコアが高いことを意味するが、**各divergence スコア の良し悪しは、推薦システムの目的に依存する**(後述).

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

## お気持ち実装
