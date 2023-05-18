# Predicting Online Performance of News Recommender Systems Through Richer Evaluation Metrics

published date: 16 September 2015,
authors: Andrii Maksai , Florent Garcin , Boi Faltings
url(paper): https://dl.acm.org/doi/10.1145/2792838.2800184
(勉強会発表者: morinota)

---

## どんなもの?

- オフラインで測定可能なmetricsを利用して、推薦システムのオンライン性能を予測する事で、コストの掛かるABテストを最小限にする方法を調査する論文.
- acurracy metricsに加えて、diversity, coverage, serendipity等のmetricsを組み合わせて、新しい性能予測モデルを作成する.
- このモデルを用いて、**オンラインテストを必要としない推薦アルゴリズムのハイパーパラメータ調整**に使用する事を提案.
- ニュースサイトのデータと実験により評価する.

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/1-Figure1-1.png)

## 導入: 推薦モデルのオフライン精度とオンライン性能の乖離問題

- 推薦システムの歴史の中で、**最も精度(文脈的にはオフライン精度...!)の高い推薦モデルが必ずしもベストではない**ということが早くから認識されていた.
- オフライン精度を基準にアルゴリズムを並べると、サイト運営者が最も気にする指標であるオンラインでのCTRを基準に並べるのと**全く逆の結果になる**事もある、と主張されている[6, 27].
- 推薦アルゴリズムが稼働していない過去の行動から収集したオフラインデータを用いて、推薦のオフライン精度を元にモデルを最適化することは、最適なアルゴリズムを選択する方法として有効でも効率的でもない可能性がある[13, 19]

- アルゴリズムを比較する最も公平な方法は、オンラインでアルゴリズムを公開し、推薦に対するユーザの実際の反応を比較することである.
- そのためには、オンライン環境の存在と熱心なユーザの存在が必要であり、長い時間がかかる.
- **オンライン環境のシミュレーション(オフライン環境での...!)**は、その代替となりうるもの[11, 27].

## 先行研究と比べて何がすごい？

## 技術や手法の肝は？

### オンライン性能に影響を与えそうなオフラインmetricsを探索

様々なmetricsをレビューし、オンラインパフォーマンスに最も影響を与えそうなものを見つけ出し、それらの間のトレードオフの存在を示す.
本論文では、5つの異なるグループに分類される17のmetricsを考慮している.

- Accuracy/Error metrics group: オフライン精度的なmetrics.
  - Precision
  - NDPM
  - Kendall's tau
  - Spearman's ρ
  - Success [6],
  - Markedness,
  - Informedness,
  - Matthew’s Correlation [15]
- Diversity metrics group: 推薦リストのアイテム間の非類似性を表すmetrics.
  - “intra-list” diversity:推薦リスト内の多様性
  - temporal diversity: ユーザの異なる訪問時に表示された、推薦アイテムの数に依存する(by Lathia et al[10])
  - "personalization": ユーザペア間の推薦結果の多様性(by Zhou et al[30])
- Novelty metrics group: 推薦アイテムがユーザにとって新しいものであるかを示すmetrics(ex. ユーザーがすでに好きなカテゴリのアイテムを推薦することは、Noveltyが低い推薦と言える)
  - “surprisal”: (by reference[30])
- Coverage metrics group:
  - coverage: これまでに推薦されたことのあるアイテムの割合を示すmetrics.
  - prediction coverage: 推薦結果を作成可能なユーザ数(?)
  - Gini Index: ジニ係数
  - Shannon’s Entropy [17]
- Serendipity metrics group: 推薦アイテムがユーザにとって予想外であると同時にlikeである性質を示す.
  - Serendipity by Ge [7]
  - Serendipity by Murakami [14]

#### metric間の相関関係

Swissinfoデータセット()に対して3種類のアルゴリズムを適用し、metrics間の相関を確認した.

- group内での相関:
  - Accuracy/Error metrics group(NDPM、Kendallのτ、Success、Spearmanのρ、Markedness、Informedness、Matthews相関)は、アルゴリズムが出力した推薦リストについて、**全metricのペア間で0.9以上の相関**が見られた.
  - 他の Diversity group, Coverage group, Serendipity group内でも、それぞれ同様の結果が得られた.
- group間での相関: それぞれのグループの"representative(代表的な)" metricsのペア間の相関を調べた(図2. 推薦リストの長さはk=3)
  - CoverageとSerendipityを除いて、**metricsグループ間で強い相関は見られなかった**.
    - -> これは、**全ての異なるmetrics groupが、推薦結果の異なる特徴を表現している**ことを示しており、したがって、各グループの少なくとも1つの代表metricをパフォーマンスモデルの特徴として使用する必要があることを示している.
  - 散布図にplotされたpointsは3つのクラスターを形成している事が多かったとのこと. (ex. Accuracy group & Diversity group間の相関の図(図2左))
    - このクラスターは、異なるアルゴリズムによる推薦結果に対応.
    - 異なるアルゴリズムによる推薦結果では、metrics group間の関係が異なる可能性があることを示している.

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/2-Figure2-1.png)

- 推薦リストの長さが、metrics group間の相関関係に与える影響を調査(図3):
  - すべてのmetrics groupペアについて、推薦リストの長さが大きくなるにつれて、まず相関の絶対値が低下し、その後ほとんど変化がないことが確認された.
  - これは、推薦アイテムの数が異なるドメインでは、異なるmetricsの組み合わせが重要である可能性を示している.

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/2-Figure3-1.png)

#### metrics間のトレードオフ

アルゴリズムは、**その性能に影響を与えるハイパーパラメータ**を持つことが多く、そのような**ハイパーパラメータの値を変えることで、異なる推薦セットを得ることができる**.
ハイパーパラメータを変化させたときにどのように変化するかを観察する.

図4の例は、Yahooデータセットと後述するCT（Context Tree）アルゴリズムのいくつかのバリエーションを用いて得られたもの.

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/3-Figure4-1.png)

各CTアルゴリズムは、**metrics間(この場合はAccuracyとCoverage)のトレードオフ**を明確に示す曲線を作成した.
また、他のデータセットやアルゴリズムを用いて、これらのトレードオフを観察した.

### オフラインmetricsからオンライン性能を予測する.

選択したmetricsのサブセットを組み合わせて、オンラインパフォーマンスの予測モデルを作成する.

まず、本論文におけるオフライン精度とオンライン精度、クリックスルー率の定義について.

- Offline accuracy(オフライン精度): 評価対象の推薦システムが**未稼働の状態**で発生したユーザの閲覧ログに対して、推薦システムで予測できたクリック数の割合のこと.
- Online accuracy(オンライン精度): 評価対象の推薦システムが**オンライン環境で稼働中の状態**で発生したユーザの閲覧ログに対して、推薦システムで予測できたクリック数の割合のこと.(推薦した際のクリックか否かは問わない)
- Click-through rate (CTR): ユーザが推薦アイテムを見た際にクリックされた割合のこと.

上２つの精度指標の定義について、任意のランダムなユーザについて、ユーザが推薦システムを使わずに訪問したすべてのアイテムが、推薦システムによって**推薦された場合に訪問するアイテムの集合に含まれる**、という仮定に基づいている.(推薦されなかったらそのニュースを読むけど、推薦されたら読まない、という天邪鬼的な事象は無視している...!)
つまり、推薦システムを使用しているときに、推薦システムがないときにも訪問するようなアイテムをユーザが訪問した場合、**そのクリックは推薦システムの効果を測定する際に考慮されるべきではない**ということです.(ん? でもオンライン精度は考慮してしまっている、という事だよね...?! )
このトピックに関するより広範な議論は、Garcin et al.[6].によって紹介されている.(読んだら意図がわかるのかな...)

CTRとオンライン精度は、どちらも推薦システムにとって重要な指標. そこで、それぞれについて回帰モデルを構築する.

#### 特徴量の選択

次に、オンライン性能の回帰モデルに対する特徴選択方法について説明する.
オンラインパフォーマンス指標の予測には、DiversityやCoverageといった複数のmetricsが重要であるという知見を検証するため、**Least Angle Regression（LAR、[4]）**を用いた特徴選択を実施した.

最後にモデルそのものについて説明する.

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
