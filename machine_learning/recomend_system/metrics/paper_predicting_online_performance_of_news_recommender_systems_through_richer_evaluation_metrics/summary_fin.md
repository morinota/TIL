# Predicting Online Performance of News Recommender Systems Through Richer Evaluation Metrics

published date: 16 September 2015,
authors: Andrii Maksai , Florent Garcin , Boi Faltings
url(paper): https://dl.acm.org/doi/10.1145/2792838.2800184
(勉強会発表者: morinota)

今回から、論文に記載されていた内容は基本的に語尾に"だよ"をつけてみています. "だよ"が付いてない文は主に自分の感想です...!

---

## どんなもの?

- **オフラインで測定可能なmetricsを利用して、推薦システムのオンライン性能を予測する**事で、コストの掛かるABテストを最小限にする方法を調査する論文だよ.
  - オフライン観測可能なmetricsとして、acurracy metricsに加えてdiversity, coverage, serendipity 等のbeyond-accuracyなmetricsも含めているよ.
- また、オンライン性能予測モデルを用いて、推薦アルゴリズムのハイパーパラメータを自動調整する手法も提案しているよ.(論文の例では、複数の推薦結果のブレンドの際の重み付け設定をself-adjustingしていたよ...!)
- 以下は結果の概要だよ.
  - オンライン性能の予測には複数のmetrics群が重要であることが示されたよ.(オフライン精度だけでなく...!)
  - coverage や serendipity といった指標は、CTRなどのオンライン性能の予測や最適化において重要な役割を果たしそうだったよ.
  - また、オンライン性能予測モデルを用いて最適なアルゴリズムとハイパーパラメータを選択することができるよ.
  - この手法により、やみくもに**A/Bテストを実施するよりも多くの労力を節約できるよ**.

![](https://camo.qiitausercontent.com/9712d21aaa151409cd4875de2fb8aecf4142225c/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f36386232326262312d373038312d643564612d303865392d6164326232616238393664632e706e67)

## 導入: 推薦モデルのオフライン精度とオンライン性能の乖離問題

- 推薦システムの歴史の中で、**最も精度(文脈的にはオフライン精度...!)の高い推薦モデルが必ずしもベストではない**ということが早くから認識されていたよ.
- オフライン精度を基準にアルゴリズムを並べると、サイト運営者が最も気にする指標であるオンラインでのCTRを基準に並べるのと**全く逆の結果になる**事もある、と主張されているよ[6, 27].
- 推薦アルゴリズムが稼働していない過去の行動から収集したオフラインデータを用いて、推薦のオフライン精度を元にモデルを最適化することは、最適なアルゴリズムを選択する方法として有効でも効率的でもない可能性があるよ[13, 19].

- アルゴリズムを比較する最も公平な方法は、オンライン環境でアルゴリズムを公開し、推薦に対するユーザの実際の反応を比較することだよ.(例えばA/Bテストだよ.)
  - でもそのためには、オンライン環境の存在と熱心なユーザの存在が必要であり、長い時間がかかるよ.
- **オンライン環境のシミュレーション(オフライン環境での...!)**は、その代替となりうるものだよ.[11, 27].

## 先行研究と比べて何がすごい？

- オンライン性能が、オフライン観測可能なmetricsにどのように依存するかを研究するために回帰モデルを構築したのは本研究が初めてらしいよ.

## 技術や手法の肝は？

### オンライン性能に影響を与えそうなオフラインmetricsを探索

様々なmetricsをレビューし、オンライン性能に最も影響を与えそうなものを見つけ出し、それらの間のトレードオフの存在を示すよ.
本論文では、**5つの異なるグループに分類される17のmetrics**を考慮しているよ.

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

Swissinfoデータセット()に対して3種類のアルゴリズムを適用し、metrics間の相関を確認したよ.

- group内での相関:
  - Accuracy/Error metrics group(NDPM、Kendallのτ、Success、Spearmanのρ、Markedness、Informedness、Matthews相関)は、アルゴリズムが出力した推薦リストについて、**全metricのペア間で0.9以上の相関**が見られたよ.
  - 他の Diversity group, Coverage group, Serendipity group内でも、それぞれ同様の結果が得られたよ.
- group間での相関: それぞれのグループの"representative(代表的な)" metricsのペア間の相関を調べたよ(図2. 推薦リストの長さはk=3)
  - CoverageとSerendipityを除いて、**metricsグループ間で強い相関は見られなかったよ**.
    - -> これは、**全ての異なるmetrics groupが、推薦結果の異なる特徴を表現している**ことを示しているよ. したがって、各グループの少なくとも1つの代表metricをオンライン性能予測モデルの特徴として使用する必要があることが示唆されるよ.
  - 散布図にplotされたpointsは3つのクラスターを形成している事が多かったよ. (ex. Accuracy group & Diversity group間の相関の図(図2左))
    - このクラスターは、異なる推薦アルゴリズムによる結果に対応しているよ.
    - これは、**推薦アルゴリズムの違いに依ってmetrics group間の関係が異なる可能性**があることを示しているよ.

![](https://camo.qiitausercontent.com/74402e371b05fbbe79f599b34aca89f0beb5e0dd/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f62643963323837372d316536612d653337382d376231662d6338306431306638353132642e706e67)

- 推薦リストの長さが、metrics group間の相関関係に与える影響を調査したよ(図3):
  - すべてのmetrics groupペアについて、推薦リストの長さが大きくなるにつれて、まず相関の絶対値が低下し、その後ほとんど変化がないことが確認されたよ.
  - これは、**推薦アイテムの数に依って重要なmetricsの組み合わせが異なる可能性**を示しているよ.

![](https://camo.qiitausercontent.com/17fdb141bc1ec6f42d8a8d6abd9c678d65b791a7/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f61353131313664372d363663372d353336372d343963632d6362653839333866306136622e706e67)

#### metrics間のトレードオフ

多くの推薦アルゴリズムは、その推薦結果の性能に影響を与えるハイパーパラメータを持っており、そのような**ハイパーパラメータの値を変えることで、異なる推薦セットを得ることができるよ**.
ハイパーパラメータを変化させたときに、metricsの関係がどのように変化するかを観察したよ.

図4の例は、Yahooデータセットと後述するCT(Context Tree)アルゴリズム(=要は推薦アルゴリズムの一つ!)のいくつかのバリエーション(=3種類の推薦アルゴリズム...!)を用いて得られたものだよ. (=要はハイパーパラメータを変更した各結果をplotしてる...!)

![](https://camo.qiitausercontent.com/0696dbf9303690f1e5af6cd77c4d922e56667fc8/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f61326238613261312d626534662d313339662d393837652d3335393462633331373361362e706e67)

各CTアルゴリズムは、**metrics間(この場合はAccuracyとCoverage)のトレードオフ**を明確に示す曲線を作成したよ.
また、他のデータセットやアルゴリズムを用いて、これらのトレードオフを観察したよ.

### オフラインmetricsからオンライン性能を予測する.

選択したmetricsのサブセットを組み合わせて、オンラインパフォーマンスの予測モデルを作成するよ.

まず、本論文におけるオフライン精度とオンライン精度、クリックスルー率の定義についてだよ.

- Offline accuracy(オフライン精度): 評価対象の推薦システムが**未稼働の状態**で発生したユーザの閲覧ログに対して、推薦システムで予測できたクリック数の割合のこと.
- Online accuracy(オンライン精度): 評価対象の推薦システムが**オンライン環境で稼働中の状態**で発生したユーザの閲覧ログに対して、推薦システムで予測できたクリック数の割合のこと.(推薦した際のクリックか否かは問わない)
- Click-through rate (CTR): ユーザが推薦アイテムを見た際にクリックされた割合のこと.

上２つの精度指標の定義について、任意のランダムなユーザについて「**ユーザが推薦システムを使わずに訪問したすべてのアイテムが、推薦システムによって推薦された場合に訪問するアイテムの集合に含まれる**」という仮定に基づいているよ.(推薦されなかったらそのニュースを読むけど、推薦されたら読まない、という天邪鬼的な事象は無視している...!)
つまり、推薦システムを使用しているときに、推薦システムがないときにも訪問するようなアイテムをユーザが訪問した場合、**そのクリックは推薦システムの効果を測定する際に考慮されるべきではない**ということだよ.(ん? でもオンライン精度は考慮してしまっている、という事だよね...?! )
このトピックに関するより広範な議論は、Garcin et al.[6].によって紹介されているよ.(読んだら意図がわかるのかな...)

CTRとオンライン精度は、どちらも推薦システムにとって重要な指標だよ. そこで、それぞれについて回帰モデルを構築するよ.

#### 特徴量の選択

次に、オンライン性能の回帰モデルに対する特徴選択方法について説明するよ.
オンライン性能metricの予測には、DiversityやCoverageといった複数のmetricsが重要であるという知見を検証するため、**Least Angle Regression（LAR、[4]）**を用いた特徴選択を実施したよ.

LARは、独立変数yとn個の従属変数$x = (x_1,\cdots ,x_n)^T$の関係の線形モデルを仮定し、$L_{1}$正則化するよ：

$$
y = \beta^T x + \lambda \sum_{j=1}^{n} |x_{j}|
$$

L1正則化により、βのスパース性が促進されるよ.(不要なパラメータが落とされる様な仕組み...?)

長さ $\Delta t$ の時間間隔におけるmetricsの平均値を predictors(=説明変数?) とし、平均的なCTRをresponses(=目的変数)として、folds間(=たぶんk分割交差検証的な事をしたって事...!)の平均的な順序位置を算出したよ.
$\Delta t$ を**10分間隔**にしたのは、これより短い間隔では分散が大きく、長い間隔ではデータポイントが少なくなり、有意な結果が得られないからだよ.
F＝100を使用したよ.(=たぶん100分割交差検証みたいな感じ...!)

#### オンライン性能の回帰モデル

最後にモデルそのものについて説明するよ.
前プロセスにて最適なpredictorsを特定した後、重回帰 $y =  \beta |x$ を用いたよ.
このシンプルなモデルにより、βの係数を、特定のモデルに対する異なるmetrics間のトレードオフ(=同じCTRを得る場合に、あるmetricsを増やしたらあるmetricsを減らす必要がある、みたいな...??)として、あるいは**metricsに関するオンライン性能の微分**として解釈することができるよ(=あるmetricが1単位増えたら、オンライン性能はどれだけ増減するか...!ってイメージ).
一応、単純な線形回帰で得られた結果を、より複雑な手法で得られた結果と比較したよ.でも複雑な手法は解釈しづらいよ.

学習データに関して、オフラインデータ(recsysを使用しないユーザのブラウジング)のログで学習された推薦システムのオフラインmetrics(説明変数側)を算出し、それと同時に、オンライン性能のmetrics(目的変数側)を推薦システムを稼働している本番環境ウェブサイトから収集する必要があるよ.

### 推薦アルゴリズムのブレンドの重み付けのself-adjusting

ここからは特殊な問題設定として、**複数のレコメンダーによる推薦結果を重み付けブレンドするケース**(ex. 協調フィルタリング0.3、コンテンツベース0.7みたいなイメージ...!)を想定するよ.
具体的には、$F(i)=W^{T}(F_{1}(i), \cdots, F_m(i))$ のように、複数のレコメンダーの評価を加味して各アイテムを評価するケースだよ(i.e. レコメンダー1 ~ mの推薦結果を、$W$で重み付けブレンドして、一つの推薦結果を作る...!).

ここでは、各レコメンダー $F_a$ に対して、**潜在変数 $Z_a$ を導入**するよ.
$Z_a(t)$ は、メインアルゴリズム(=現在稼働中のブレンド推薦システムのこと...!)によって時刻 $t$ に推薦されたアイテムが、$F_a(t)$ によって推薦されたアイテムに**どれだけ近いか**(=現在稼働中のブレンド後推薦結果と、各レコメンダーの推薦結果のdistance metric、みたいな??)を意味するよ.
($Z_a(t)$ が低い -> レコメンダー$a$とブレンド後の推薦結果が似ている -> 現在、レコメンダー$a$の重み付けは高い事を意味する...!)

各時刻$t$におけるオンライン性能の回帰モデルを、説明変数 $Z_i(t)$ として設計する.
この場合、ある回帰係数 $\beta_{i}(t)$の重みが正であれば、$\beta_{i}(t+1)$ が増えるように重み付け設定を調整する事で、オンライン性能が向上する事を示しているよ(->この場合は、レコメンダー$i$の重みを小さくすべき、という示唆になる...!).
具体的には、以下の勾配降下の式により、ブレンド重み付け$W$を更新する.

$$
W_{t +1} = W_{t} + λ ∗ \beta_{t}
$$

ここで、$t$ と $t+1$ は連続する2つのtime frameに対応し、$\beta_{t}$ はtime frame $t$ のデータから学習させたオンライン性能回帰モデルの係数だよ.

このself-adjusting手法は、ブレンド重み付け設定のグリッドサーチの効果的な代替方法となる可能性があるよ.
また、レコメンダー $F_a$ が特定の オフラインmetrics セットを最適化するという単純なケースでは、このself-adjusting手法は、 オフラインmetrics セットを時間的に変化する 説明変数 として使用してCTRをモデル化することと同等だと考える事もできるよ.
(=>あるmetricを元に最適化させた推薦結果がオンライン性能に強い影響を与えた! =>即ち、あるmetricの大小はオンライン性能に強い影響を与える、といえる...!)

## どうやって有効だと検証した?

### 有効な特徴量(オフラインmetrics)選択の結果

LARによる特徴量選択の手順を、CTアルゴリズム(=推薦アルゴリズム) & Swissinfoデータセット(=データセット)に対して適用したよ.

今回は各説明変数そのものに興味があるのではなく、**metricsグループ（Accuracy、Coverage、Diversity、Serendipity、Novelty）の重要性を示したい**ので、各metricsグループの最初のmetricがモデルに入るまでの平均時間を計算したよ. table 1はその結果だよ.

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/5-Table1-1.png)

- **Serendipity、Accuracy、Diversityの3つのグループのメトリクスは、通常、モデルに入る最初の3つ**だったよ.
  - -> これら3つのグループが、**オンライン性能metricの異なる部分に関係**し、いずれも予測するために重要なmetricsである事を示しているよ.
- DiversityやSerendipityのpredictorsを取り除いた場合、Cverageの平均初回入力時間が短くなる傾向があったよ.
  - Diversity、Serendipity、Coverageの3つのグループのうち、2つで十分かもしれないということを示しているよ.
- Accuracy groupのmetricでは、どれを使っても問題なさそうだよ.

あるmetrics group当たり、LARにおいて最速な一つのmetricのみがモデルに入る様にしたよ.

### 回帰モデルの性能

学習データをdatetimeに基づいて、30％、50％、20％のパートに分けたよ.

- 最初の30%は**アルゴリズム自体のトレーニング**に使用され、オンライン性能予測モデルには使用されないよ.
- 次の50%については、アルゴリズムが出力した推薦結果と共に、**オンライン性能予測モデルのトレーニング**に使用されたよ.
- 最後の20%は、**オンライン性能予測モデルの評価**に使用されたよ.

#### CTR prediction.

表2は、回帰モデルにおけるオフラインmetricsの組み合わせとその予測誤差の結果をまとめたものだよ.
左の各列は、推薦アルゴリズム毎に結果を平均したものだよ.
右の各列は、データセット毎に結果を平均したものだよ.

![](https://camo.qiitausercontent.com/fbaf88b0075e1ce297b5e445d172a65ca59b7e4f/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32646561373135392d366335622d363730372d646338642d3063646335636632396235352e706e67)

- 4つのmetrics group からそれぞれ1つずつpredictor(説明変数)を用いることで、平均誤差が最も小さくなったよ. (noveltyは特徴選択の結果が悪く、割愛)
- metricsの全セットを説明変数として採用したケース(All)では誤差関数はより良い値を示したよ. でもおそらくオーバーフィッティングが原因だよ.
- 最初のデータセットにおいては、Diversity が非常に重要だったよ. metric一つの結果が最も良かったよ.
  - また、 diversity を含む異なるグループの組み合わせは、diversity を含まない組み合わせよりも良い結果だったよ.
- ペナルティ付きLR（All+L2）やRBFカーネル付きガウスプロセス（GP+RBF）など、より複雑なモデルはさらに良い結果を示したけど、これらは解釈しずらいよ.
- 結果はデータセット間で一貫しており、**最も優れたmetricsの組み合わせの予測精度は、一定のCTRを仮定したベースラインモデル(Const)を大幅に上回っていたよ**.

図5は、２つの推薦アルゴリズムにおいて、テスト期間におけるオンライン性能予測モデルの予測値と実測値を時系列でplotしたものだよ.

![](https://camo.qiitausercontent.com/269f70a0ec79a22088733bd22b77bf063b3edde2/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32303931313066382d653631362d383962302d616531352d3862393463393164303065302e706e67)

前述のオフラインmetricsが、確かにオンライン性能の予測力を持つことがわかるよ.
予測結果ではオンライン性能metricの経時的な曲線の形状が繰り返され、作成した回帰モデルが**オンライン性能metricの経時的な挙動やおおよその値を予測できる**可能性が高いことが示されたよ.

- また、回帰モデルの係数(parameters)を確認すると、データセットやアルゴリズムによって各parameterの大小関係が異なる事がわかったよ.
  - -> これは、推薦アルゴリズムに関係なく性能を予測するために作られた線形モデルは、各推薦アルゴリズムに特化して訓練されたモデルのセットよりも性能が低下し得る事を示唆しているよ.

#### Online accuracy prediction.

(オンライン性能予測モデルの目的変数をCTRからオンライン精度に置き換えたもの...!)
表3は、表2と同様、回帰モデルにおけるオフラインmetricsの組み合わせとその予測誤差の結果をまとめたものだよ.

![](https://camo.qiitausercontent.com/4c8a1da25a386bf7995170daf2ad5a06ef1081f2/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f61336330386663642d363361622d333361662d333064302d3134326131626238383735392e706e67)

- 予測誤差の傾向はデータセット間であまり一致しなかったよ.
  - Swissinfoデータセットでは、最良の結果はDiversityを含まない3つのグループから得られたよ.
  - LePointデータセットでは、最良の結果はSerendipityを含まない3つのグループから得られたよ.

### 推薦アルゴリズムのブレンドの重み付けのself-adjustingの結果

- 今回の実験では、Context TreeとMost Popularの2つの推薦アルゴリズムが与える**推薦結果の線形結合**に基づく4種(=ブレンドの重み付け設定が異なる4種)の推薦システムを使用し、ライブのニュースサイトでアルゴリズムを実行したよ.(i.e. Most Popularアルゴリズムによる推薦結果の重み付けを、20%, 40%, 60%, 80%の４種.)

self-adjustingの為に、2つのアルゴリズムによる推薦に近いかどうかを測定する$Z_{CT}$と$Z_{pop}$という潜在的なmetircsを用意したよ.
self-adjustingに基づき重み付けを変更する事で、本当にCTRが改善するのかどうかを検証したよ.

図６は、3つのtime frameにおいて、4種の推薦システムによるCTRを記録したものだよ. 矢印はself-adjustingによって提案された重み付け設定更新の向きを表しているよ.(左向きがmost popularityの重みを減らす、右向きが増やす...!)

![](https://camo.qiitausercontent.com/9d6e133271d568b8dca988aa4a83cd7eed03039c/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f31333466663762652d336434662d663733632d336565312d3835333036326237656666612e706e67)

- 第3期、第5期、第7期（日中）では、4種全てが**CTアルゴリズムの重みを高めるべきことを示唆**したよ. (i.e. 日中は、CTアルゴリズムの重み付けを高めるようなself-adjusting結果になった...?)(あ、でも夜時間帯である第４期と第6期も同様の傾向か...!)
- "CTRを向上させる為にこのように重み付けを変更すべき"と示唆された矢印の向きは、一貫して正しいものだったよ.(i.e. 実際に重み付け更新の矢印が指している方が、より高いCTRを記録していた...!)
  - 例えば第一期の結果を見ると、Most Popularの重み40%を使用するシステムの回帰係数はプラスで、重みの増加を示唆し、Most Popularの重み60%を使用するアルゴリズムにつながり、この時間枠で実際に高いCTRを得ることができているよ.

## 議論はある？

- オンライン性能予測モデルによる、推薦アルゴリズムのブレンドの重み付けのself-adjustingは、次のtime frameの重みを更新するよりも、次の日の同じ時間帯のtime frameの重みを更新する方が良いかも...! (時間帯によって、ユーザが求める推薦結果の性質が異なる可能性...!!)

## 次に読むべき論文は？

- coverageとかserendipityとかのmetricsの定式化は確認しておいたほうが良いかも...

## お気持ち実装