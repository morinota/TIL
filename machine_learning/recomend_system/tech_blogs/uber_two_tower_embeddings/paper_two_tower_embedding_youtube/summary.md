# Deep Neural Networks for YouTube Recommendations

published date: RecSys ’16 September 15-19, 2016,
authors: Paul Covington, Jay Adams, Emre Sargin
url(paper): <https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf?uclick_id=516d5009-f5a0-49d5-b5cb-7fcf02e27ab8>
(勉強会発表者: morinota)

---

## どんなもの?

- 読んだきっかけは、Uberさんのtech blogを読んで"two-tower model"というarchitectureがよく分からなかったので...! 参考: [Innovative Recommendation Applications Using Two Tower Embeddings at Uber](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
- 2016年のYoutubeの動画推薦システムについて紹介してる論文であり、Deep NNを使った2-stagesの推薦システムを導入してるとの事: **candidate retrieve** と **candidate ranking**
- candidate retrieve のモデルも candidate ranking のモデルも、同じ様な"Tower pattern"のarchitecture の deep neural networkを採用してた。
- 「既存研究と比べてここがすごい！」という論文ではなく、Youtubeの推薦の困難さをこういう工夫で対処してますよ!的な、**tipsを紹介**してる様な論文の印象。
- 「**こういう特徴量を追加すると改善された!**」とか「**こういう代理学習問題(surrogate learning problem)を選ぶと効果的だった!**」等のtipsがたくさん紹介されていた...!

## 先行研究と比べて何がすごい？

- 2-stages推薦に関しては、Youtubeが本論文の以前からも導入してたか否かはよく分からず。
- 2016年時点では、深層学習系の推薦システムの研究は少なく、Youtubeも元々はdeep NN系のモデルではなかったみたい。
- しかし、グーグル全体の他の製品分野と連携して、**YouTubeはほぼすべての学習問題に対する汎用ソリューションとして深層学習を使用する方向へ**と根本的なパラダイムシフトを遂げた、との事。

## 技術や手法の肝は？

### 2-stages推薦の概要

![](https://www.hardikp.com/assets/youtube-recommendations/system-overview.png)

- 図2は推薦システムの全体構造。
- 2つのNNモデルで構成されている: candidate retrieve(generation)モデルとcandidate rankingモデル
  - 1ステージ目: candidate retrieve(generation)モデル:
    - 本モデルは、ユーザの行動履歴を入力とし、**大規模なcorpus(数百万本)から小さなsubset(数百)をretrieve**する。
    - 本モデルは、協調フィルタリングによる**広範な(broadな!)パーソナライゼーションのみ**を提供する。
    - 本モデルでユーザ間の類似性を抽出する為の特徴量は、以下の様な**粗い(coarseな)特徴量**: 動画視聴のid、検索クエリのトークン、demographics(=人口統計情報。ex. 年齢、性別、職業、etc.)
  - 2ステージ目: candidate rankingモデル:
    - candidate listの中で少数の"best"な推薦を提示する為には、高いrecallを持つ推薦アイテム候補の中で**相対的な重要性を区別する**為の、より細かいレベルの表現が必要。
    - よって本モデルでは、ビデオとユーザを説明する**richな特徴量set**を使用して、望ましい目的関数に従って各ビデオにスコアを割り当てる。
    - 動画アイテムはそのスコアによってラング付けされ、上位の動画がユーザに提示される。
- 2-stages推薦のメリット:
  - Scalabilityの問題に対処できる。
  - 他のソースから生成された**候補をブレンドする**工夫を取れる。(ex. CF由来のcandidateと、CB由来のcandidate :thinking:)

> During development, we make extensive use of offline metrics (precision, recall, ranking loss, etc.) to guide iterative improvements to our system. **However for the final determination of the effectiveness of an algorithm or model, we rely on A/B testing via live experiments**.
> In a live experiment, we can measure subtle changes in click-through rate, watch time, and many other metrics that measure user engagement. **This is important because live A/B results are not always correlated with offline experiments.**

Googleも、オンライン評価/オフライン評価の問題は結構苦労してるのかなぁ...:thinking: この時点では、特にOff-Policy Evaluation的な事をやってるわけではないのかな。

### candidate retrieve(generation)モデル

- 本論文以前は、rank lossに基づく行列分解アプローチを適用してた、とのこと。
- 本論文の最初の試行は、**ユーザの過去の視聴履歴を埋め込むだけの浅いネットワークで、このMFの動作を模倣**する事。
  - この観点から本アプローチは、**行列分解技術の非線形一般化**とみなせる。

- 本アプローチは、推薦を極端な多クラス分類問題とみなす。
  - 問題設定: ユーザ $U$ とコンテキスト $C$ に基づいて、コーパス $V$ から何百万ものビデオ $i$ (=classes)の中で、時間tで特定のビデオ視聴 $w_t$ を予測する(**next-item-prediction**的なタスク??:thinking:):

$$
P(w_{i} = i|U,C) = \frac{e^{v_i u}}{\sum_{j \in V} e^{v_j u}}
$$

- ここで、$u \in \mathbb{R}^{N}$ はユーザとコンテキストのペアの高次元のembeddingを表し、$v_{j} \in \mathbb{R}^{N}$ は各candidateアイテムのembeddingを表す。
  - (ユーザベクトルとアイテムベクトルの内積を、temperature無しのsoftmax関数に通して、確率として表してる感じ...!)
- 本設定における"embedding"とは、**単に疎なentity(個々のビデオ、ユーザなど)を $\mathbb{R}^{N}$ の密なベクトルにmappingすること**である。
  - (ふむふむ、entity空間から意味空間へのmappingみたいな...! sparce -> dense :thinking:)
- 本deep NNのタスクは、**ソフトマックス分類器で動画を分類するのに有用な、ユーザの履歴とコンテキストの関数としてのユーザ埋め込み $u$ を学習すること**である。
  - コンテンツ埋め込みテーブル(embedding table)も他のパラメータと一緒にbackpropで学習されてる。

![fig3](https://www.hardikp.com/assets/youtube-recommendations/candicate-generation-model.png)

図3は、モデルのarchitecture。

以下はTwo-towerモデルにおける特徴量の扱いの話。

- continuous bag of words言語モデル(=良くわかってないが単語の埋め込みベクトルを作る手法らしい...!)にヒントを得て各動画のembeddingを用意し、この動画embeddingを元にcandidate retrieveモデルの入力を作る:
  - **ユーザの視聴履歴はsparseな動画IDの可変長sequenceで表現され**(うんうん:thinking:)、動画embeddingを使ってaggregateしてdenseなベクトル表現にmappingされる。
  - この動画embeddingも、他の全てのモデルパラメータと共同で学習される。
- **全ての特徴量は広い第1層に連結**され、その後にfully connected layer[ReLU](6)の数層が続く。
  - **このarchitectureの下側(=入力側)が広く、上側(=出力側)が狭くなっている点から、"tower pattern"と呼ばれるらしい**...!
- **ディープニューラルネットワークを行列分解法の一般化として使用する主な利点は、任意のcontinuous特徴量やcategorical特徴量を簡単にモデルに追加できること**.(うんうん。CFとCBのハイブリッド手法に簡単に拡張できるってこと??)
  - Demographicな(人口統計学的な)特徴量(ex. 年齢、性別、地理的位置、言語、関心分野)は、推薦モデルが新しいユーザに対して合理的な振る舞いをするように、事前情報を提供するために重要。
  - **ユーザの性別、ログイン状態、年齢のような単純なバイナリ特徴量および連続値特徴量は、[0, 1]に正規化された実数値としてネットワークに直接入力される**
- multi-valentな特徴量 (カテゴリ値のlist, set的な特徴量) は、**埋め込みを平均化されてからネットワークに入力される**。
- embeddingの共有について。
  - 多くの異なる特徴量が使用するビデオID(例: impressionのビデオID、ユーザが視聴した最後のビデオID、推薦の「種」となったビデオIDなど)には、単一のグローバルな埋め込みが存在する。
  - それらの特徴量は、**ネットワークに別々に供給される**。
  - embeddingを共有することは、汎化性能を向上させ、トレーニングを高速化し、必要なメモリを削減するために重要。

特に"Example Age"特徴量の話:

- 最近アップロードされた(“fresh”な)コンテンツを推薦することは、YouTubeにとって非常に重要。
  - というのも、ビデオの人気度分布は非定常性が高いので。(=人気なアイテムが時間とともに変わりゆく=新しいアイテムが人気上位を置き換え続ける?) (参考:図4)
- 機械学習システムは、過去のtraining exampleから将来の行動を予測するように訓練されるため、しばしば過去への暗黙のバイアスを示す。(uploadから期間が経過してtraining exampleが多いアイテムを優遇してスコア付けしちゃう??)
- これを補正するために、**訓練時に"Example Age"(=training exampleの年齢)を特徴量として与える**。
- 推論時には、この特徴量はゼロ（またはわずかにマイナス）に設定される。

![fig4]()

explicit feedback / implicit feedback のどちらを使うかの話:

- YouTubeには、明示的なフィードバック・メカニズム（サムズアップ／ダウン、商品内アンケートなど）が存在するが、**モデルをトレーニングするために、ユーザーがビデオを完走したことをpositiveな例とする、視聴の暗黙的フィードバック[16]を使用する**。(一部explicit feedbackもあるが、基本的にはimplicit feedbackを使うって事か...!:thinking:)
- 理由は、利用可能な暗黙のユーザ履歴が桁違いに多く、**明示的なフィードバックが極端に少ない様なlong-tailアイテムの奥深くまで**レコメンデーションを作成したいから。
- (確かに、explicit feedbackのみのモデルではlong-tailアイテムは考慮できなそう...!:thinking: implicit feedbackを使ってもpopularity biasを対策しないとlong-tailアイテムは推薦されづらいと思うけど...!)

推論時の話:

- 数十ミリ秒の厳しい待ち時間の下で数百万のアイテムをスコアリングするには、**計算量がクラス数(=推薦可能なユニークアイテム数)に比例しない様な、近似的なスコアリング方式**が必要。
- 本モデルのソフトマックス出力層から得られる尤度(=確率)は、**推論時には必要ない**(=学習・評価時には使ってるってことか...!:thinking:)ので、スコアリング問題は、汎用のライブラリを使用することができる**ドット積空間の最近傍探索に軽減される**。
- A/Bテストの結果、candidate retrieveモデルの性能は、最近傍探索アルゴリズムの選択に対して特に敏感ではなかった。

推薦システムの代理学習問題(surrogate learning problem)の選択の話:

- 推薦問題は、しばしば代理的な問題(=本アプローチで言えば他クラス分類問題?)を解決し、その結果を特定のcontextに移すこと(=他クラス分類問題で学習させた中間成果物のベクトルを使う事?)を含む。
  - (予測問題で学習させたMLモデルを使って、意思決定最適化タスクを解く、みたいな話...!:thinking:)
- 典型的な例は、**視聴率を正確に予測することが効果的な映画推薦につながるという仮定**。

動画の消費パターンの話:

- youtubeにおける動画の自然な消費パターンは通常、非常に**非対称な共同視聴確率(asymmetric co-watch probabilities)**をもつ。
  - (ex. ビデオA -> Bの順では視聴されやすいが、ビデオB -> Aの順では視聴されにくい :thinking: 逆に、対称な共同視聴確率の場合は、A -> B と B -> Aの視聴されやすさは同程度)
- そのため、**ランダムにhold-outされた視聴を予測するよりも、ユーザの次の視聴を予測する方がはるかに優れたパフォーマンスを示す**ことがABテストの結果でわかった(図5) (next-item-prediction的な??:thinking:)
- 一般的な協調フィルタリングは、ランダムにアイテムを取り出し、ユーザの履歴にある他のアイテムから予測することで、label(=予測したい情報)とcontext(=入力情報)を暗黙的に選択している(図5a)。**これは将来の情報を漏らし、非対称な消費パターンを無視することになる**。
- 対照的に、ランダムな視聴(training example)を選択する & hold-outされたラベルの視聴の前にユーザが取った行動のみを入力することで、ユーザの履歴を"ロールバック"する(図5b)

![fig5]()

特徴量の数とNNの深さの話:

- 図6に示すように、特徴量とNN architectureの深さを追加することで、hold-outデータの精度が大幅に向上した。
  - 実験内容: 1Mの動画と1Mの検索トークンのvocabularyを、それぞれ256次元のembeddingにマッピング。ユーザの最近の動画視聴50件と最近の検索クエリ50個を最大バッグサイズとして、ユーザの履歴を埋め込んだ。
    - (たぶんここでの256は、two-towerモデルの出力の埋め込み次元数のこと! :thinking:)
  - 一般に、ネットワークを深くするほど、扱う特徴量を増やすほど、性能が向上した。
    - 比較した層の深さ
      - depth 0: 256 ReLU (中間層なし。特徴量連結層 -> 出力層の線形変換)
      - depth 1: 512 ReLU -> 256 ReLU
      - depth 2: 1024 ReLU -> 512 ReLU -> 256 ReLU
      - depth 3: 2048 ReLU -> 1024 ReLU -> 512 ReLU -> 256 ReLU
      - (**入力から出力にかけてだんだんユニット数が小さくなっていく = tower patternと言われる所以**...!:thinking:)
    - 性能が飽和するまで、特徴量を追加 & ネットワークを深くすることを続けたとのこと。

![fig6](image.png)

### candidate rankingモデル

本モデルの主な役割は、impressionデータ(=showしてtapしたか否か、とか?)を使って、特定のUIの予測候補を特化させ、calibrate(較正, 調節, 校正)すること。(特定のuserだけじゃなくて、特定のuserの特定のUIに特化させても良いのか...!:thinking:)
ランキングは、**スコアが直接比較できない異なるcandidateソースをアンサンブルするためにも重要**。

![fig7](https://www.hardikp.com/assets/youtube-recommendations/ranking-model.png)

- candidate retrieve(generation)モデルと**同様のアーキテクチャを持つdeep NN を使用**し、ロジスティック回帰を用いて各動画のimpressionに独立したスコアを割り当てる(図7)。
- ランキングの為の目的関数は、ライブのA/Bテストの結果に基づいて常に調整されてるが、一般的には、**impressionにおける視聴時間の期待値**に関するシンプルな損失関数を採用しているらしい。
- CTRを目的関数としたランキングは、しばしばユーザが完了しないdeceptiveな動画(“clickbait”)を促進するのに対し、**視聴時間はuser engagementをよりよく捉える**[13, 25]

feature engineeringの話:

- ランキング・モデルでは数百の特徴量を使用し、categoricalなものとcontinuousなものをほぼ均等に使い分けている。
- ディープラーニングは、**手作業で特徴量を設計する負担を軽減することが期待されているにもかかわらず、rawデータの性質上、FFNに直接入力することは容易ではない**。
  - ->なので今でも、**ユーザやビデオのデータを有用な特徴量に変換するために**、かなりのエンジニアリング・リソースを費やしている、とのこと。

continuous特徴量の話:

- 最も重要な特徴量は、**スコアリング対象アイテム自体や他の類似アイテムとの、ユーザの過去のinteractionを記述する特徴量**。(これは広告のランキング問題でも同様の傾向らしい)
  - ex. スコアリング対象の動画をアップロードしたチャンネルでのユーザの過去の履歴に関する特徴
  - このチャンネルでユーザは何件のビデオを見た?
  - ユーザがこのトピックに関する動画を最後に見たのはいつ?
  - 関連アイテムに対する過去のユーザの行動を記述するこれらの連続的な特徴量は、異種のアイテムにわたってよく一般化されるため、特に強力らしい。
- また、**candidate generationから特徴量という形でランキングに情報を伝達することが重要**だったとのこと。
  - どのcandidate sourcesがこの動画候補を推薦したのか?
  - 各candidate sourcesがこのアイテムに対してどのような点数をつけたのか?
- **ニューラルネットワークは、その入力のスケーリングと分布に敏感であることで有名**[9]。
  - **連続特徴量の適切な正規化が収束に重要**だったらしい。
  - 具体的には、分布 $f$ を持つ連続特徴量 $x$ を、累積分布(=確率密度関数の累積分布関数) $\tilde{x} = \inf_{-\infty}^{x} df$ を用いて、$[0, 1]$ に等しく分布するようにスケーリングして $\tilde{x}$ に変換する。

視聴時間の期待値のモデリングの話:

- rankingモデルにおける目的は、positive(ビデオのimpressionがクリックされた)またはnegative(impressionがクリックされなかった)のどちらかであるtraining examplesにて、与えられた視聴時間の期待値を予測すること。
  - positive exampleには、ユーザがビデオを見るのに費やした時間がannotateされている。(negative exampleは、0がannotateされてるのかな)
- ↑の目的の為に、**重み付けロジスティック回帰の手法**を採用する。
  - 本モデルは、クロスエントロピー損失の下でロジスティック回帰を用いて学習される(図7)
  - しかし、**positive(クリックされた) impressionは、観察された動画の視聴時間によって重み付けされる**。
  - **negative(クリックされていない) impressionは、すべて単位ウェイト**を紐付けられる。
    - (あ、視聴時間を直接予測するわけじゃないんだ...!!:thinking:)

## どうやって有効だと検証した?

- オフライン評価とABテストも継続的に実施しながら、特徴量やNNの深さ、目的関数の選択等を調整してたみたい。

## 議論はある？

- 推薦の為の代理問題の選択の話。本論文では、**非対称的な共同視聴行動**を考慮し、**将来の情報の漏洩を防止すること**によって将来の視聴の分類問題を選択した。(**next-item prediction的なsurrogate問題を採用した**、って認識...!:thinking:)

## 次に読むべき論文は？

- 2-stages推薦に興味がある(=もっと利点欠点等を把握して良さそうだったら活用したい...!)ので、関連してそうな論文でも読んでみようかな: [Two-Stage Session-based Recommendations with Candidate Rank Embeddings](https://arxiv.org/abs/1908.08284)

## お気持ち実装

今回は余力がなくスキップします!
