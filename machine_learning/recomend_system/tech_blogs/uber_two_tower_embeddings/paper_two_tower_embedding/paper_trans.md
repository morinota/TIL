## 0.1. link リンク

https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf?uclick_id=516d5009-f5a0-49d5-b5cb-7fcf02e27ab8
https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf?uclick_id=516d5009-f5a0-49d5-b5cb-7fcf02e27ab8

## 0.2. title タイトル

Deep Neural Networks for YouTube Recommendations
YouTubeレコメンデーションのためのディープ・ニューラル・ネットワーク

## 0.3. abstruct abstruct

YouTube represents one of the largest scale and most sophisticated industrial recommendation systems in existence.
YouTubeは、現存する中で最大規模かつ最も洗練された産業用レコメンデーションシステムのひとつである。
In this paper, we describe the system at a high level and focus on the dramatic performance improvements brought by deep learning.
本稿では、このシステムを高いレベルで説明し、ディープラーニングがもたらす劇的な性能向上に焦点を当てる。
The paper is split according to the classic two-stage information retrieval dichotomy: first, we detail a deep candidate generation model and then describe a separate deep ranking model.
本稿は、古典的な2段階の情報検索の二分法に従っている：
まず、ディープ候補生成モデルについて詳述し、次にディープ・ランキング・モデルについて述べる。
We also provide practical lessons and insights derived from designing, iterating and maintaining a massive recommendation system with enormous userfacing impact.
また、ユーザーに多大な影響を与える大規模なレコメンデーションシステムの設計、反復、保守から得られた実践的な教訓や洞察も提供する。

# 1. Introduction はじめに

![fig]()

YouTube is the world’s largest platform for creating, sharing and discovering video content.
YouTubeは、ビデオコンテンツを作成、共有、発見するための世界最大のプラットフォームです。
YouTube recommendations are responsible for helping more than a billion users discover personalized content from an ever-growing corpus of videos.
YouTubeのレコメンデーションは、10億人以上のユーザーが、増え続ける動画のコーパスからパーソナライズされたコンテンツを発見する手助けをしている。
In this paper we will focus on the immense impact deep learning has recently had on the YouTube video recommendations system.
本稿では、ディープラーニングが最近YouTubeの動画レコメンデーションシステムに与えた絶大な影響に焦点を当てる。
Figure 1 illustrates the recommendations on the YouTube mobile app home.
図1は、YouTubeモバイルアプリのホームに表示されるレコメンデーションを示している。
Recommending YouTube videos is extremely challenging from three major perspectives:
YouTubeの動画をレコメンドすることは、3つの観点から非常に難しい：

- Scale: Many existing recommendation algorithms proven to work well on small problems fail to operate on our scale.
- 規模：小さな問題でうまく機能することが証明されている既存の推薦アルゴリズムの多くは、私たちのスケールで動作しません。
  Highly specialized distributed learning algorithms and efficient serving systems are essential for handling YouTube’s massive user base and corpus.
  YouTubeの膨大なユーザーベースとコーパスを扱うには、高度に専門化された分散学習アルゴリズムと効率的なサービングシステムが不可欠である。
- Freshness: YouTube has a very dynamic corpus with many hours of video are uploaded per second.
- 新鮮さ：
  YouTubeのコーパスは非常にダイナミックで、1秒間に何時間もの動画がアップロードされている。
  The recommendation system should be responsive enough to model newly uploaded content as well as the latest actions taken by the user.
  レコメンデーション・システムは、新しくアップロードされたコンテンツやユーザーによる最新のアクションをモデル化するのに十分な応答性を持つべきである。
  Balancing new content with well-established videos can be understood from an exploration/exploitation perspective.
  新しいコンテンツと定評のある映像のバランスは、exploration/exploitationの観点から理解することができる。
- Noise: Historical user behavior on YouTube is inherently difficult to predict due to sparsity and a variety of unobservable external factors.
- ノイズ
  YouTubeの過去のユーザー行動は、スパース性と様々な観測不可能な外部要因のため、本質的に予測が困難である。
  We rarely obtain the ground truth of user satisfaction and instead model noisy implicit feedback signals.
  私たちは、ユーザー満足度の真実を得ることはほとんどなく、代わりにノイズの多い暗黙のフィードバック信号をモデル化する。
  Furthermore, metadata associated with content is poorly structured without a well defined ontology.
  さらに、コンテンツに関連するメタデータは、明確に定義されたオントロジーがなければ、構造化が不十分である。
  Our algorithms need to be robust to these particular characteristics of our training data.
  我々のアルゴリズムは、訓練データのこのような特殊な特性に対してロバストである必要がある。

In conjugation with other product areas across Google, YouTube has undergone a fundamental paradigm shift towards using deep learning as a general-purpose solution for nearly all learning problems.
グーグル全体の他の製品分野と連携して、**YouTubeはほぼすべての学習問題に対する汎用ソリューションとしてディープラーニングを使用する方向へと根本的なパラダイムシフトを遂げた**。
Our system is built on Google Brain [4] which was recently open sourced as TensorFlow [1].
我々のシステムは、最近TensorFlow [1]としてオープンソース化されたGoogle Brain [4]をベースに構築されている。
TensorFlow provides a flexible framework for experimenting with various deep neural network architectures using largescale distributed training.
TensorFlowは、大規模な分散トレーニングを使用して、さまざまなディープニューラルネットワークアーキテクチャを実験するための柔軟なフレームワークを提供する。
Our models learn approximately one billion parameters and are trained on hundreds of billions of examples.
私たちのモデルは約10億のパラメータを学習し、数千億の例で訓練されています。

In contrast to vast amount of research in matrix factoriza-tion methods [19], there is relatively little work using deep neural networks for recommendation systems.
行列分解法の膨大な研究 [19]とは対照的に、**推薦システムにディープニューラルネットワークを使用した研究は比較的少ない**。(RecSys2016年頃はそうだったんだ...!:thinking:)
Neural networks are used for recommending news in [17], citations in [8] and review ratings in [20].
ニューラルネットワークは、[17]ではニュースの推薦に、[8]では引用に、[20]ではレビューの評価に使われている。
Collaborative filtering is formulated as a deep neural network in [22] and autoencoders in [18].
協調フィルタリングは、[22]ではディープニューラルネットワークとして、[18]ではオートエンコーダとして定式化されている。(ふむふむ:thinking:)
Elkahky et al.used deep learning for cross domain user modeling [5].
Elkahkyらは、ディープラーニングをクロスドメインユーザーモデリングに使用した[5]。
In a content-based setting, Burges et al.used deep neural networks for music recommendation [21].
コンテンツ・ベースの設定では、Burgesらがディープ・ニューラル・ネットワークを使って音楽を推薦している[21]。

The paper is organized as follows: A brief system overview is presented in Section 2.
本稿の構成は以下の通りである：
セクション2にシステムの概要を示す。
Section 3 describes the candidate generation model in more detail, including how it is trained and used to serve recommendations.
セクション3では、**候補生成モデル(=2stagesの1stage目, uberでいうcandidate retrieveのモデル...??)**がどのように学習され、どのようにレコメンデーションを提供するために使用されるかを含め、より詳細に説明する。
Experimental results will show how the model benefits from deep layers of hidden units and additional heterogeneous signals.
実験結果は、隠れユニットの深い層と追加的な異種信号が、このモデルにどのような利益をもたらすかを示すだろう。
Section 4 details the ranking model, including how classic logistic regression is modified to train a model predicting expected watch time (rather than click probability).
セクション4は、**どのように古典的なロジスティック回帰が(クリック確率ではなく)期待されるウォッチタイムを予測するモデルを訓練するために修正されるかを含む、ランキングモデルの詳細**である。(candidate rankingって古典的なロジスティック回帰でも十分なのか...!)
Experimental results will show that hidden layer depth is helpful as well in this situation.
実験結果は、この状況では隠れ層の深さも役に立つことを示している。
Finally, Section 5 presents our conclusions and lessons learned.
最後に、セクション5で結論と教訓を述べる。

# 2. System Overview システム概要

![fig2]()

The overall structure of our recommendation system is illustrated in Figure 2.
推薦システムの全体構造を図2に示す。
The system is comprised of two neural networks: one for candidate generation and one for ranking.
このシステムは**2つのニューラルネットワーク**で構成されている：
1つは候補生成用、もう1つはランキング用である。(candidate rankingもNNなの?)
The candidate generation network takes events from the user’s YouTube activity history as input and retrieves a small subset (hundreds) of videos from a large corpus.
候補生成ネットワークは、ユーザーのYouTube行動履歴からイベントを入力とし、大規模なコーパスから動画の小さなサブセット（数百）を検索(retrieve)する。(ここでも"retrieve"という表現を使うんだ...!)
These candidates are intended to be generally relevant to the user with high precision.
これらの候補は、高い精度でユーザに一般的に関連することを意図している。
The candidate generation network only provides broad personalization via collaborative filtering.
候補者生成ネットワークは、協調フィルタリングによる**広範な(broadな!)パーソナライゼーションしか提供しない**。
The similarity between users is expressed in terms of coarse features such as IDs of video watches, search query tokens and demographics.
ユーザー間の類似性は、ビデオ視聴のID、検索クエリのトークン、デモグラフィックのような粗い特徴で表現される。

Presenting a few “best” recommendations in a list requires a fine-level representation to distinguish relative importance among candidates with high recall.
**リストの中で少数の「ベスト」な推薦を提示するには、高いrecallを持つ候補の中で相対的な重要性を区別するための細かいレベルの表現(=特徴量?)が必要**である。
The ranking network accomplishes this task by assigning a score to each video according to a desired objective function using a rich set of features describing the video and user.
ランキング・ネットワークは、ビデオとユーザを説明する豊富な特徴量セットを使用して、望ましい目的関数に従って各ビデオにスコアを割り当てることによって、このタスクを達成する。
The highest scoring videos are presented to the user, ranked by their score.
スコアの高い動画は、そのスコアによってランク付けされ、ユーザーに提示される。

The two-stage approach to recommendation allows us to make recommendations from a very large corpus (millions) of videos while still being certain that the small number of videos appearing on the device are personalized and engaging for the user.
**レコメンデーションのtwo-stage approachにより、非常に大規模なコーパス（数百万本）からレコメンデーションを行うことができ**、同時に、デバイスに表示される少数のビデオが、ユーザーにとってパーソナライズされた魅力的なものであることを確信することができる。
Furthermore, this design enables blending candidates generated by other sources, such as those described in an earlier work [3].
さらに、この設計は、以前の研究[3]で説明されたような、**他のソースから生成された候補をブレンドすることを可能にする**。(CF由来のcandidateと、CB由来のcandidate)

During development, we make extensive use of offline metrics (precision, recall, ranking loss, etc.) to guide iterative improvements to our system.
開発中、**私たちはオフライン・メトリクス(精度、リコール、ランキング・ロスなど)を広範囲に活用し、システムの反復的な改善を導いている**。(特にOPE的な事は工夫してないのかな...!:thinking:)
However for the final determination of the effectiveness of an algorithm or model, we rely on A/B testing via live experiments.
しかし、**アルゴリズムやモデルの有効性を最終的に判断するためには、ライブ実験によるA/Bテストに頼る**ことになる。
In a live experiment, we can measure subtle changes in click-through rate, watch time, and many other metrics that measure user engagement.
ライブ実験では、クリックスルー率、視聴時間、その他ユーザーエンゲージメントを測る多くの指標の微妙な変化を測定することができる。
This is important because live A/B results are not always correlated with offline experiments.
**ライブのA/B結果は、オフラインの実験と必ずしも相関関係がないため、これは重要である**。(Google もOPEの問題苦労しているのか...!)

# 3. Candidate Generation 候補者の生成

During candidate generation, the enormous YouTube corpus is winnowed down to hundreds of videos that may be relevant to the user.
候補生成の際、膨大なYouTubeコーパスは、ユーザに関連しそうな数百の動画に絞り込まれる。
The predecessor to the recommender described here was a matrix factorization approach trained under rank loss [23].
ここで説明する**レコメンダーの前身は、ランクロスのもとで訓練された行列分解アプローチ**である[23]。(=元々はMFだった)
Early iterations of our neural network model mimicked this factorization behavior with shallow networks that only embedded the user’s previous watches.
私たちのニューラルネットワークモデルの初期のiterations(=試行?)は、ユーザの過去の**視聴履歴を埋め込むだけの浅いネットワークで、このMFの動作を模倣**した。
From this perspective, our approach can be viewed as a nonlinear generalization of factorization techniques.
この観点から、我々のアプローチは**MF技術の非線形一般化**とみなすことができる。(=通常のMFって線形モデルなんだっけ?)

## 3.1. Recommendation as Classification

We pose recommendation as extreme multiclass classification where the prediction problem becomes accurately classifying a specific video watch wt at time t among millions of videos i (classes) from a corpus V based on a user U and context C,
我々は、推薦を極端な多クラス分類とみなしている:
ここで、予測問題は、ユーザ $U$ とコンテキスト $C$ に基づいて、コーパス $V$ から何百万ものビデオ $i$ (=classes)の中で、時間tで特定のビデオ視聴 $w_t$ を正確に分類することになる:

$$
P(w_{i} = i|U,C) = \frac{e^{v_i u}}{\sum_{j \in V} e^{v_j u}}
$$

(ユーザベクトルとアイテムベクトルの内積を、temperature無しのsoftmax関数に通して、確率にしてる感じ。)

where u ∈ R N represents a high-dimensional “embedding” of the user, context pair and the vj ∈ R N represent embeddings of each candidate video.
ここで、**$u \in \mathbb{R}^{N}$ はユーザーとコンテキストのペアの高次元の「埋め込み」**を表し、$v_{j} \in \mathbb{R}^{N}$ は各候補ビデオの埋め込みを表す。(ユーザのembeddingではなく、user \* contextのembedding??)
In this setting, an embedding is simply a mapping of sparse entities (individual videos, users etc.) into a dense vector in R N .
**この設定では、埋め込みとは、単に疎なエンティティ（個々のビデオ、ユーザーなど）を $\mathbb{R}^{N}$の密なベクトルにマッピングすること**である。(ふむふむ。sparce -> dense)
The task of the deep neural network is to learn user embeddings u as a function of the user’s history and context that are useful for discriminating among videos with a softmax classifier.
**ディープ・ニューラル・ネットワークのタスクは、ソフトマックス分類器で動画を識別するのに有用な、ユーザの履歴とコンテキストの関数としてのユーザー埋め込み $u$ を学習すること**である。(=たぶん分類問題を学習させたNNの、encoder的に、中間層の出力をembeddingとして抜き出してる感じっぽい...!)
Although explicit feedback mechanisms exist on YouTube (thumbs up/down, in-product surveys, etc.) we use the implicit feedback [16] of watches to train the model, where a user completing a video is a positive example.
YouTubeには、明示的なフィードバック・メカニズム（サムズアップ／ダウン、商品内アンケートなど）が存在するが、**私たちはモデルをトレーニングするために、ユーザーがビデオを完走したことをpositiveな例とする、視聴の暗黙的フィードバック[16]を使用する**。(一部explicit feedbackもあるが、基本的にはimplicit feedbackを使う...!)
This choice is based on the orders of magnitude more implicit user history available, allowing us to produce recommendations deep in the tail where explicit feedback is extremely sparse.
この選択は、**利用可能な暗黙のユーザ履歴が桁違いに多い**ことに基づいており、**明示的なフィードバックが極端に少ない様なlong-tailアイテムの奥深くまで**レコメンデーションを作成することを可能にしている。(確かに、explicit feedbackのみのモデルではlong-tailアイテムは考慮できなそう...! implicit feedbackを使ってもpopularity biasを対策しないとlong-tailアイテムの推薦はつくりにくいけど...!)

### 3.1.1. Efficient Extreme Multiclass 効率的なエクストリーム・マルチクラス

To efficiently train such a model with millions of classes, we rely on a technique to sample negative classes from the background distribution (“candidate sampling”) and then correct for this sampling via importance weighting [10].
何百万ものクラスでこのようなモデルを効率的に訓練するために、我々はbackgroud distribution(?, 事後分布の意味??)から負のクラスをサンプリングし(“candidate sampling”)、**重要度重み付けによってこのサンプリングを補正する技術**に頼る[10]。(=MNARなデータの補正をしている、という事だろうか??:thinking:)
For each example the cross-entropy loss is minimized for the true label and the sampled negative classes.
各例について、真のラベルとサンプリングされた負のクラスについて、交差エントロピーの損失が最小化される。
In practice several thousand negatives are sampled, corresponding to more than 100 times speedup over traditional softmax.
実際には数千のネガがサンプリングされ、従来のソフトマックスの100倍以上のスピードアップに相当する。(softmax関数の為のサンプリング??)
A popular alternative approach is **hierarchical softmax** [15], but we weren’t able to achieve comparable accuracy.
一般的な代替アプローチは**階層的ソフトマックス[15]**だが、同等の精度を達成することはできなかった。
In hierarchical softmax, traversing each node in the tree involves discriminating between sets of classes that are often unrelated, making the classification problem much more difficult and degrading performance.
階層型ソフトマックスでは、ツリーの各ノードを走査することは、しばしば無関係なクラスの集合を識別することになり、分類問題をより難しくし、パフォーマンスを低下させる。
At serving time we need to compute the most likely N classes (videos) in order to choose the top N to present to the user.
サービング時に、ユーザに提示するトップ $N$ を選択するために、最も可能性の高い $N$ 個のクラス(=ビデオ)を計算する必要がある。
Scoring millions of items under a strict serving latency of tens of milliseconds requires an approximate scoring scheme sublinear in the number of classes.
**数十ミリ秒の厳しい待ち時間の下で数百万のアイテムをスコアリングするには、計算量がクラス数(=ユニークアイテム数)に比例しない様な、近似的なスコアリング方式が必要**である。
Previous systems at YouTube relied on hashing [24] and the classifier described here uses a similar approach.
YouTubeの以前のシステムはハッシュ[24]に依存しており、ここで説明する分類器も同様のアプローチを使っている。
Since calibrated likelihoods from the softmax output layer are not needed at serving time, the scoring problem reduces to a nearest neighbor search in the dot product space for which general purpose libraries can be used [12].
ソフトマックス出力層からの較正された尤度(=確率)は、**serving time(=推論時?)には必要ない**(=中間層の出力だけembeddingとして使えば良いので)ので、スコアリング問題は、汎用のライブラリを使用することができる**ドット積空間の最近傍探索に軽減される**[12]。
We found that A/B results were not particularly sensitive to the choice of nearest neighbor search algorithm.
A/Bテストの結果は、最近傍探索アルゴリズムの選択に対して特に敏感ではないことがわかった。

## 3.2. Model Architecture モデル・アーキテクチャ

Inspired by continuous bag of words language models [14], we learn high dimensional embeddings for each video in a fixed vocabulary and feed these embeddings into a feedforward neural network.
continuous bag of words言語モデル[14]にヒントを得て、**各動画の高次元の埋め込みを固定語彙(=fixed vocabulary)で学習し、これらの埋め込みをフィードフォワード・ニューラル・ネットワークに入力**する。(->これが一番下の入力??)
A user’s watch history is represented by a variable-length sequence of sparse video IDs which is mapped to a dense vector representation via the embeddings.
ユーザの視聴履歴は、**スパースなビデオIDの可変長sequence**で表現され、embeddingを介して**密なベクトル表現にマッピングされる**。
The network requires fixed-sized dense inputs and simply averaging the embeddings performed best among several strategies (sum, component-wise max, etc.).
このネットワークは、**固定サイズの密な入力を必要**とし、いくつかの戦略(合計、成分ごとの最大値など)の中で、単純に埋め込みを平均化することが最も良い結果を出した。
Importantly, the embeddings are learned jointly with all other model parameters through normal gradient descent backpropagation updates.
重要なことは、**embeddingは、通常の勾配降下バックプロパゲーション更新を通じて、他のすべてのモデルパラメータと共同で学習される**ことである。(じゃあ実際には、sparseなsequenceをdenseなembeddingに変換する処理もarchitectureに含まれる??)
Features are concatenated into a wide first layer, followed by several layers of fully connected Rectified Linear Units (ReLU) [6].
**特徴量は広い第1層に連結**され、その後に完全連結された整流線形ユニット(ReLU)[6]の数層が続く.
Figure 3 shows the general network architecture with additional non-video watch features described below.
図3は、一般的なネットワーク・アーキテクチャを示し、ビデオウォッチ以外の特徴量については後述する。

![fig3]()

Figure 3: Deep candidate generation model architecture showing embedded sparse features concatenated with dense features. Embeddings are averaged before concatenation to transform variable sized bags of sparse IDs into fixed-width vectors suitable for input to the hidden layers. All hidden layers are fully connected. In training, a cross-entropy loss is minimized with gradient descent on the output of the sampled softmax. At serving, an approximate nearest neighbor lookup is performed to generate hundreds of candidate video recommendations.
図3：ディープ候補生成モデルのアーキテクチャは、埋め込まれた疎な特徴を密な特徴と連結したものである。エンベッディングは連結前に平均化され、スパースIDの可変サイズのバッグを隠れ層への入力に適した固定幅のベクトルに変換する。すべての隠れ層は完全に接続されている。訓練では、サンプリングされたソフトマックスの出力に対して勾配降下法を用いてクロスエントロピー損失が最小化される。サービング時には、近似最近傍探索が実行され、何百ものビデオ推薦候補が生成される。

## 3.3. Heterogeneous Signals 異種シグナル

A key advantage of using deep neural networks as a generalization of matrix factorization is that arbitrary continuous and categorical features can be easily added to the model.
**ディープニューラルネットワークを行列分解法の一般化として使用する主な利点は、任意のcontinuous特徴量やcategorical特徴量を簡単にモデルに追加できること**である.(うんうん。CFとCBのハイブリッド手法に簡単に拡張できるってこと??)
Search history is treated similarly to watch history - each query is tokenized into unigrams and bigrams and each token is embedded.
検索履歴は視聴履歴と同様に扱われ、各クエリは uni-gram (=各検索履歴を個別に使う??) と bi-bram (=連続する2つ検索履歴を人まとまりとして扱う?)にトークン化され、各トークンが埋め込まれる。
Once averaged, the user’s tokenized, embedded queries represent a summarized dense search history.
一度平均化されると、**ユーザのトークン化された埋め込みクエリは、要約された高密度の検索履歴を表す**。
Demographic features are important for providing priors so that the recommendations behave reasonably for new users.
人口統計学的な特徴量(ex. 年齢、性別、地理的位置、言語、関心分野)は、推薦モデルが新しいユーザに対して合理的な振る舞いをするように、事前情報を提供するために重要である。
The user’s geographic region and device are embedded and concatenated.
ユーザの地理的地域とデバイスが埋め込まれ、連結される。
Simple binary and continuous features such as the user’s gender, logged-in state and age are input directly into the network as real values normalized to [0, 1].
ユーザの性別、ログイン状態、年齢のような単純なバイナリおよび連続的特徴は、[0, 1]に正規化された実数値としてネットワークに直接入力される。(embedされずに!)

### 3.3.1. “Example Age” Feature

Many hours worth of videos are uploaded each second to YouTube.
YouTubeには毎秒何時間分もの動画がアップロードされている。
Recommending this recently uploaded (“fresh”) content is extremely important for YouTube as a product.
**最近アップロードされた（「新鮮な」）コンテンツを推薦することは、YouTubeにとって非常に重要**である。
We consistently observe that users prefer fresh content, though not at the expense of relevance.
私たちは一貫して、ユーザが新鮮なコンテンツを好むことを観察しているが、relevanceを犠牲にしているわけではない。
In addition to the first-order effect of simply recommending new videos that users want to watch, there is a critical secondary phenomenon of bootstrapping and propagating viral content [11].
ユーザが見たい新しいビデオを単純に推薦するという一次的な効果に加え、バイラルコンテンツをブートストラップして伝播させるという重要な二次的現象がある[11]。(??)
Machine learning systems often exhibit an implicit bias towards the past because they are trained to predict future behavior from historical examples.
機械学習システムは、過去の例から将来の行動を予測するように訓練されているため、しばしば過去への暗黙のバイアスを示す。
The distribution of video popularity is highly non-stationary but the multinomial distribution over the corpus produced by our recommender will reflect the average watch likelihood in the training window of several weeks.
ビデオの人気度分布は非定常性が高い(=人気なアイテムが時間とともに変わりゆく=新しいアイテムが人気上位を置き換え続ける?)が、我々のレコメンダーが生成するコーパス上の多項分布は、数週間のトレーニングウィンドウにおける平均視聴可能性を反映する。(古めのアイテムのtraining exampleを優遇して学習しちゃう??)
To correct for this, we feed the age of the training example as a feature during training.
これを補正するために、**訓練時にtraining exampleの年齢を特徴量として与える**。
At serving time, this feature is set to zero (or slightly negative) to reflect that the model is making predictions at the very end of the training window.
サービング時には、モデルがトレーニング・ウィンドウの最後の方で予測を行っている(=新しくuploadされたアイテムに対して予測スコアを出す?)ことを反映するため、この特徴量はゼロ（またはわずかにマイナス）に設定される。
Figure 4 demonstrates the efficacy of this approach on an arbitrarily chosen video [26].
図4は、任意に選ばれたビデオ[26]に対するこのアプローチの有効性を示している。

![fig4]()

- 緑: Emprical Distribution(=経験的分布) -> tapされやすいアイテムは、uploadされて0 ~ 5日以内のアイテム。

## 3.4. Label and Context Selection ラベルとコンテキストの選択

It is important to emphasize that recommendation often involves solving a surrogate problem and transferring the result to a particular context.
**推薦は、しばしば代理的な問題(=今回で言えば他クラス分類問題?)を解決し、その結果を特定のcontextに移すことを含むこと**を強調することが重要である。
A classic example is the assumption that accurately predicting ratings leads to effective movie recommendations [2].
典型的な例は、**視聴率を正確に予測することが効果的な映画推薦につながるという仮定**である[2]。
We have found that the choice of this surrogate learning problem has an outsized importance on performance in A/B testing but is very difficult to measure with offline experiments.
我々は、この**代理学習問題(surrogate learning problem)の選択**が、A/Bテストのパフォーマンスにおいて非常に重要であるが、オフライン実験では測定が非常に困難であることを発見した。(OPE的な話??)

Training examples are generated from all YouTube watches (even those embedded on other sites) rather than just watches on the recommendations we produce.
training examplesは、私たちが作成した**レコメンデーションの視聴だけでなく**、すべてのYouTubeの視聴（他のサイトに埋め込まれているものも含む）から生成されます。(うんうん。その方がimplicit feedbackの情報量多いし...)
Otherwise, it would be very difficult for new content to surface and the recommender would be overly biased towards exploitation.
そうでなければ、**新しいコンテンツが浮上するのは非常に難しく、レコメンダーは過度にexploitation(活用)に偏る**ことになる。
If users are discovering videos through means other than our recommendations, we want to be able to quickly propagate this discovery to others via collaborative filtering.
もしユーザが私たちの推薦以外の手段でビデオを発見した場合、協調フィルタリングによってこの発見を素早く他のユーザに伝えられるようにしたい。
Another key insight that improved live metrics was to generate a fixed number of training examples per user, effectively weighting our users equally in the loss function.
ライブメトリクスを改善するもう一つの重要な洞察は、**ユーザごとに固定数のトレーニング例を生成し、損失関数でユーザを均等に重み付けすること**でした。
This prevented a small cohort of highly active users from dominating the loss.
これにより、**少数のアクティブなユーザが損失を独占することを防いだ**。

Somewhat counter-intuitively, great care must be taken to withhold information from the classifier in order to prevent the model from exploiting the structure of the site and overfitting the surrogate problem.
やや直感に反するが、モデルがサイトの構造を利用し、surrogate problem をオーバーフィットするのを防ぐために、分類器から情報を隠すように細心の注意を払わなければならない。
Consider as an example a case in which the user has just issued a search query for “taylor swift”.
例えば、ユーザーが "taylor swift" の検索クエリを発行した場合を考えてみよう。
Since our problem is posed as predicting the next watched video, a classifier given this information will predict that the most likely videos to be watched are those which appear on the corresponding search results page for “taylor swift”.
我々の問題(=代理問題、surrogate problem)は、次に視聴される動画を予測することであるため、この情報を与えられた分類器は、視聴される可能性が最も高い動画は、「taylor swift」の対応する検索結果ページに表示される動画であると予測する。
Unsurpisingly, reproducing the user’s last search page as homepage recommendations performs very poorly.
驚くことに、ユーザが最後に検索したページをホームページのレコメンデーションとして再現するのは、非常にパフォーマンスが悪い。
By discarding sequence information and representing search queries with an unordered bag of tokens, the classifier is no longer directly aware of the origin of the label.
**シーケンス情報を破棄し、検索クエリを順序付けされていないbag of tokensで表現すること**で、分類器はラベル(正解ラベル)の由来を直接意識することがなくなる。

![fig5]()

Natural consumption patterns of videos typically lead to very asymmetric co-watch probabilities.
ビデオの自然な消費パターンは通常、非常に**非対称な共同視聴確率(asymmetric co-watch probabilities)**をもたらす。(ビデオA -> Bの順では視聴されやすいが、ビデオB -> Aの順では視聴されにくい。逆に、対象な共同視聴確率 = A -> B と B -> Aの視聴されやすさは同程度)
Episodic series are usually watched sequentially and users often discover artists in a genre beginning with the most broadly popular before focusing on smaller niches.
エピソードシリーズは通常、順次視聴され、ユーザは多くの場合、あるジャンルのアーティストを最も広く人気のあるものから発見し、その後、より小さなニッチに焦点を当てる。
We therefore found much better performance predicting the user’s next watch, rather than predicting a randomly held-out watch (Figure 5).
そのため、**ランダムにhold-outされた視聴を予測するよりも、ユーザの次の視聴を予測する方がはるかに優れたパフォーマンスを示す**ことがわかった（図5）。
Many collaborative filtering systems implicitly choose the labels and context by holding out a random item and predicting it from other items in the user’s history (5a).
多くの協調フィルタリングシステムは、ランダムにアイテムを取り出し、ユーザの履歴にある他のアイテムから予測することで、ラベルとコンテキストを暗黙的に選択している(5a)。
This leaks future information and ignores any asymmetric consumption patterns.
**これは将来の情報を漏らし、非対称な消費パターンを無視することになる**。
In contrast, we “rollback” a user’s history by choosing a random watch and only input actions the user took before the held-out label watch (5b).
対照的に、ランダムな視聴(training example)を選択する & hold-outされたラベルの視聴の前にユーザが取った行動のみを入力することで、ユーザの履歴を「ロールバック」する（5b）。

## 3.5. Experiments with Features and Depth 特徴と深さの実験

![fig6]()

Adding features and depth significantly improves precision on holdout data as shown in Figure 6.
図6に示すように、特徴量と深さを追加することで、hold-outデータの精度が大幅に向上する。
In these experiments, a vocabulary of 1M videos and 1M search tokens were embedded with 256 floats each in a maximum bag size of 50 recent watches and 50 recent searches.
これらの実験では、1Mのビデオと1Mの検索トークンのvocabularyを、それぞれ256個のフロート(=embedding の次元数)で、**最近の視聴50個と最近の検索50個の最大バッグサイズに埋め込んだ**。
The softmax layer outputs a multinomial distribution over the same 1M video classes with a dimension of 256 (which can be thought of as a separate output video embedding).
ソフトマックス層は、256次元の同じ1Mビデオクラス(これはそれぞれの出力ビデオ埋め込みと考えることができる)上のmultinomial distributionを出力する。(出力は、$\mathbb{R}^{1M \times 256}$ ??)
These models were trained until convergence over all YouTube users, corresponding to several epochs over the data.
これらのモデルは、全ユーチューバーに対して収束するまで学習され、データに対する数回のエポックに相当する。
Network structure followed a common “tower” pattern in which the bottom of the network is widest and each successive hidden layer halves the number of units (similar to Figure 3).
ネットワーク構造は一般的な **"tower"パターン**に従っており、**ネットワークの下部が最も広く、各隠れ層はユニット数が半分になる**（図3と同様）.(tower patternって呼ばれるんだ...!)
The depth zero network is effectively a linear factorization scheme which performed very similarly to the predecessor system.
**深さ0のネットワークは、事実上、線形因数分解スキームであり、前身のシステムと非常によく似た性能を発揮した。**
Width and depth were added until the incremental benefit diminished and convergence became difficult:
幅と深さは、増分的な利益が減少し、収束が困難になるまで追加された：

- Depth 0: A linear layer simply transforms the concatenation layer to match the softmax dimension of 256. 線形レイヤーは、単純に連結レイヤーを256のソフトマックス次元に合うように変換する。(Factorization machine的な?)
- Depth 1: 256 ReLU
- Depth 2: 512 ReLU → 256 ReLU
- Depth 3: 1024 ReLU → 512 ReLU → 256 ReLU
- Depth 4: 2048 ReLU → 1024 ReLU → 512 ReLU → 256 ReLU

# 4. Ranking ランキング

The primary role of ranking is to use impression data to specialize and calibrate candidate predictions for the particular user interface.
ランキングの主な役割は、**インプレッション・データを使って、特定のユーザ・インターフェースの予測候補を特化させ、calibrate(較正, 調節, 校正)すること**である。
For example, a user may watch a given video with high probability generally but is unlikely to click on the specific homepage impression due to the choice of thumbnail image.
例えば、ユーザはあるビデオを一般的に高い確率で見るかもしれないが、サムネイル画像の選択によって特定のホームページの印象をクリックする可能性は低い。
During ranking, we have access to many more features describing the video and the user’s relationship to the video because only a few hundred videos are being scored rather than the millions scored in candidate generation.
ランキングの際には、**ビデオとユーザの関係を説明する、より多くの特徴量にアクセス**することができる。
Ranking is also crucial for ensembling different candidate sources whose scores are not directly comparable.
ランキングは、**スコアが直接比較できない異なるcandidateソースをアンサンブルするためにも重要**である。

![fig7]()

We use a deep neural network with similar architecture as candidate generation to assign an independent score to each video impression using logistic regression (Figure 7).
候補生成と**同様のアーキテクチャを持つディープニューラルネットワークを使用**し、ロジスティック回帰を用いて各動画のimpressionに独立したスコアを割り当てる（図7）。
The list of videos is then sorted by this score and returned to the user.
ビデオのリストはこのスコアでソートされ、ユーザに返される。
Our final ranking objective is constantly being tuned based on live A/B testing results but is generally a simple function of expected watch time per impression.
最終的なランキングの目的関数は、ライブのA/Bテストの結果に基づいて常に調整されていますが、一般的には、インプレッションあたりの予想視聴時間の単純な関数です。
Ranking by click-through rate often promotes deceptive videos that the user does not complete (“clickbait”) whereas watch time better captures engagement [13, 25].
**クリックスルー率によるランキングは、しばしばユーザが完了しない偽の動画（「クリックベイト」）を促進するのに対し、視聴時間はengagementをよりよく捉える[13, 25]**。

## 4.1. Feature Representation

Our features are segregated with the traditional taxonomy of categorical and continuous/ordinal features.
私たちの特徴量は、伝統的な分類法である**categorical特徴量**と**continuous/ordinal特徴量**に分別される。
The categorical features we use vary widely in their cardinality - some are binary (e.g.whether the user is logged-in) while others have millions of possible values (e.g.the user’s last search query).
我々が使用するカテゴリカルな特徴量は、そのカーディナリティが大きく異なる。あるものはバイナリであり（例：ユーザーがログインしているかどうか）、あるものは何百万もの可能な値を持つ（例：ユーザーの最後の検索クエリ）。
Features are further split according to whether they contribute only a single value (“uni-valent”) or a set of values (“multivalent”).
特徴量はさらに、単一の値（“uni-valent”）だけを寄与するか、一連の値（“multivalent”）を寄与するかによって分けられる。
An example of a univalent categorical feature is the video ID of the impression being scored, while a corresponding multivalent feature might be a bag of the last N video IDs the user has watched.
**uni-valentのカテゴリカル特徴量の例としては、採点対象のimpressionのビデオID**があり、**対応するmulti-valentの特徴量としては、ユーザが視聴した直近のN個のビデオIDのbag**がある。
We also classify features according to whether they describe properties of the item (“impression”) or properties of the user/context (“query”).
また、アイテム(“impression”)の特性を表すか、ユーザ/コンテキスト("query")の特性を表すかによって、特徴量を分類する。
Query features are computed once per request while impression features are computed for each item scored.
**query特徴量はリクエストごとに1回計算される**が、impression特徴量はスコアされたアイテムごとに計算される。

### 4.1.1. Feature Engineering フィーチャーエンジニアリング

We typically use hundreds of features in our ranking models, roughly split evenly between categorical and continuous.
私たちは通常、ランキング・モデルで数百の特徴を使用し、カテゴリー的なものと連続的なものをほぼ均等に使い分けている。
Despite the promise of deep learning to alleviate the burden of engineering features by hand, the nature of our raw data does not easily lend itself to be input directly into feedforward neural networks.
ディープラーニングは、**手作業で特徴量を設計する負担を軽減することが期待されているにもかかわらず、生データの性質上、フィードフォワード・ニューラルネットワークに直接入力することは容易ではない**。
We still expend considerable engineering resources transforming user and video data into useful features.
私たちは今でも、ユーザやビデオのデータを有用な特徴量に変換するために、かなりのエンジニアリング・リソースを費やしている。
The main challenge is in representing a temporal sequence of user actions and how these actions relate to the video impression being scored.
主な課題は、ユーザアクションの時間的sequenceを表現することと、これらのアクションがどのように採点されるビデオのimpressionと関連しているかを表現することである。

We observe that the most important signals are those that describe a user’s previous interaction with the item itself and other similar items, matching others’ experience in ranking ads [7].
最も重要なシグナルは、**ユーザのアイテム自体や他の類似アイテムとの過去のinteractionを記述するもの**であり、広告のランキングにおける他の人の経験と一致することが観察される[7]。
As an example, consider the user’s past history with the channel that uploaded the video being scored
一例として、採点対象の動画をアップロードしたチャンネルでのユーザの過去の履歴を考えてみましょう。
how many videos has the user watched from this channel?
このチャンネルでユーザは何件のビデオを見ましたか？
When was the last time the user watched a video on this topic?
ユーザがこのトピックに関する動画を最後に見たのはいつですか？
These continuous features describing past user actions on related items are particularly powerful because they generalize well across disparate items.
**関連アイテムに対する過去のユーザの行動を記述するこれらの連続的な特徴量は、異種のアイテムにわたってよく一般化されるため、特に強力**です。
We have also found it crucial to propagate information from candidate generation into ranking in the form of features,
我々はまた、**candidate generationから特徴量という形でランキングに情報を伝達することが重要である**ことを発見した。
e.g.which sources nominated this video candidate?
どのソースがこの動画候補を推薦したのか?
What scores did they assign?
各candidate sourcesがこのアイテムに対してどのような点数をつけたのか?

Features describing the frequency of past video impressions are also critical for introducing “churn” in recommendations (successive requests do not return identical lists).
過去のビデオインプレッションの頻度を記述する特徴量は、レコメンデーションに"churn"（連続したリクエストは同一のリストを返さない）を導入するためにも重要である。
If a user was recently recommended a video but did not watch it then the model will naturally demote this impression on the next page load.
もしユーザが最近ビデオを薦められたが見なかった場合、モデルは次のページロードでこのimpressionを自然に下げる。
Serving up-to-the-second impression and watch history is an engineering feat onto itself outside the scope of this paper, but is vital for producing responsive recommendations.
**秒単位のimpressionと視聴履歴を提供すること**は、それ自体、本稿の範囲外の技術的な偉業であるが、応答性の高い推薦結果を作成するためには不可欠である。

### 4.1.2. Embedding Categorical Features カテゴリー特徴の埋め込み

Similar to candidate generation, we use embeddings to map sparse categorical features to dense representations suitable for neural networks.
候補生成と同様に、埋め込みを使って、疎なカテゴリー特徴量をニューラルネットワークに適した**密な表現にマッピング**する。
Each unique ID space (“vocabulary”) has a separate learned embedding with dimension that increases approximately proportional to the logarithm of the number of unique values.
それぞれのユニークなID空間(“vocabulary”)は、ユニークな値の数の対数にほぼ比例して増加する次元を持つ別々の学習された埋め込みを持つ。
These vocabularies are simple look-up tables built by passing over the data once before training.
これらのボキャブラリーは、トレーニングの前に一度データを渡すことで構築される単純な**look-up tables(=連想配列とか!dictとか!:thinking:)**である。
Very large cardinality ID spaces (e.g.video IDs or search query terms) are truncated by including only the top N after sorting based on their frequency in clicked impressions.
**非常に大きなカーディナリティのIDスペース(ビデオIDや検索クエリ用語など)は、クリックされたインプレッションにおける頻度に基づいてソートした後、上位N件のみを含めることによって切り捨てられる**。
Out-of-vocabulary values are simply mapped to the zero embedding.
ボキャブラリー外の値は、単純にゼロ埋め込みにマッピングされる。
As in candidate generation, multivalent categorical feature embeddings are averaged before being fed in to the network.
候補生成と同様に、multi-valentのカテゴリー特徴埋め込みは、ネットワークに入力される前に平均化される。

Importantly, categorical features in the same ID space also share underlying emeddings.
重要なのは、同じID空間内のカテゴリカル特徴量も、その根底にあるembeddingを共有することである。
For example, there exists a single global embedding of video IDs that many distinct features use (video ID of the impression, last video ID watched by the user, video ID that “seeded” the recommendation, etc.).Despite the shared embedding, each feature is fed separately into the network so that the layers above can learn specialized representations per feature.
例えば、多くの異なる特徴量が使用するビデオID(impressionのビデオID、ユーザが視聴した最後のビデオID、推薦の「種」となったビデオIDなど)の単一のグローバルな埋め込みが存在する。共有された埋め込みにもかかわらず、各特徴量は、上の層が特徴量ごとに特化した表現を学習できるように、**ネットワークに別々に供給される**。
Sharing embeddings is important for improving generalization, speeding up training and reducing memory requirements.
**エンベッディングを共有することは、汎化性能を向上させ、トレーニングを高速化し、必要なメモリを削減するために重要である**。
The overwhelming majority of model parameters are in these high-cardinality embedding spaces - for example, one million IDs embedded in a 32 dimensional space have 7 times more parameters than fully connected layers 2048 units wide.
例えば、32次元空間に埋め込まれた100万個のIDは、2048ユニット幅の完全連結レイヤーの7倍のパラメーターを持つ。

### 4.1.3. Normalizing Continuous Features 連続特徴の正規化

Neural networks are notoriously sensitive to the scaling and distribution of their inputs [9] whereas alternative approaches such as ensembles of decision trees are invariant to scaling of individual features.
**ニューラルネットワークは、その入力のスケーリングと分布に敏感であることで有名である**[9]。
一方、決定木のアンサンブルのような代替アプローチは、個々の特徴量のスケーリングに対して不変である。
We found that proper normalization of continuous features was critical for convergence.
我々は、**連続特徴量の適切な正規化が収束に重要である**ことを発見した。
A continuous feature x with distribution $f$ is transformed to $\tilde{x}$ by scaling the values such that the feature is equally distributed in $[0, 1)$ using the cumulative distribution, $\tilde{x} = \inf_{-\infty}^{x} df$.
分布 $f$ を持つ連続特徴量 $x$ を、累積分布(=確率密度関数の累積分布関数) $\tilde{x} = \inf_{-\infty}^{x} df$ を用いて、$[0, 1]$ に等しく分布するようにスケーリングして $\tilde{x}$ に変換する。
This integral is approximated with linear interpolation on the quantiles of the feature values computed in a single pass over the data before training begins.
**この積分は、学習開始前にデータに対して1回だけ計算された特徴量の分位数に対する線形補間で近似される**。(解析的に求めようとすると計算量が増える!)

In addition to the raw normalized feature $\tilde{x}$, we also input powers $\tilde{x}^2$ and $\sqrt{\tilde{x}}$, giving the network more expressive power by allowing it to easily form super- and sub-linear functions of the feature.
生の正規化された特徴量 $\tilde{x}$ に加えて、べき乗 $\tilde{x}^2$ と $\sqrt{\tilde{x}}$ も入力し、特徴量の**super-linear function（超線形関数, 入力値が増加するにつれて、出力値がそれ以上に速く増加する関数）**や**sub-linear function（亜線形関数, 入力値が増加するにつれて、出力値がそれよりも遅く増加する関数）**を簡単に形成できるようにすることで、ネットワークに表現力を与えている。
Feeding powers of continuous features was found to improve offline accuracy.
連続的な特徴量を投入することで、オフラインの精度が向上することがわかった。

## 4.2. Modeling Expected Watch Time

Our goal is to predict **expected watch time** given training examples that are either positive (the video impression was clicked) or negative (the impression was not clicked).
私たちの目標は、肯定的（ビデオのimpressionがクリックされた）または否定的（impressionがクリックされなかった）のどちらかであるトレーニング例にて、与えられた予想視聴時間を予測することです。
Positive examples are annotated with the amount of time the user spent watching the video.
肯定的な例には、ユーザがビデオを見るのに費やした時間がannotateされている。(negative exampleは、時間0なのかな。)
To predict expected watch time we use the technique of weighted logistic regression, which was developed for this purpose.
予想時計時間を予測するために、この目的のために開発された加重ロジスティック回帰の手法を用いる。

![fig7]()

The model is trained with logistic regression under crossentropy loss (Figure 7).
このモデルは、クロスエントロピー損失の下でロジスティック回帰を用いて学習される（図7）。
However, the positive (clicked) impressions are weighted by the observed watch time on the video.
しかし、**ポジティブ（クリックされた）インプレッションは、観察された動画の視聴時間によって重み付けされる**。
Negative (unclicked) impressions all receive unit weight.
**否定的な(クリックされていない)impressionは、すべて単位ウェイトを受ける**。
In this way, the odds learned by the logistic regression are $\frac{\sum T_{i}}{N - k}$ where $N$ is the number of training examples, k is the number of positive impressions, and Ti is the watch time of the ith impression.
このようにして、ロジスティック回帰によって学習されたオッズは、$\frac{\sum T_{i}}{N - k}$ となる。ここで、Nはtraining exampleの数、$k$ はポジティブなimpressionの数、$T_i$ はi番目のimpressionの視聴時間である。
Assuming the fraction of positive impressions is small (which is true in our case), the learned odds are approximately E[T](1 + P), where P is the click probability and E[T] is the expected watch time of the impression.
ポジティブ・インプレッションの割合が少ないと仮定すると（このケースではそうである）、学習されたオッズはおよそ $E[T](1 + P)$ となる。
ここで、$P$ はクリック確率、$E[T]$ はインプレッションの視聴時間期待値である。
Since P is small, this product is close to E[T].
$P$ は小さいので、この積はE[T]に近い。
For inference we use the exponential function e x as the final activation function to produce these odds that closely estimate expected watch time.
推論には、最終的な活性化関数として指数関数 $e^{x}$ を使用し、視聴時間期待値を厳密に推定するオッズを生成する。

## 4.3. Experiments with Hidden Layers 隠しレイヤーの実験

![table1]()

Table 1 shows the results we obtained on next-day holdout data with different hidden layer configurations.
表1は、隠れ層の構成を変えた翌日hold-outデータで得られた結果である。
The value shown for each configuration (“weighted, per-user loss”) was obtained by considering both positive (clicked) and negative (unclicked) impressions shown to a user on a single page.
各構成で表示される値(「加重、ユーザごとの損失」)は、1つのページでユーザーに表示されたポジティブ（クリックされた）インプレッションとネガティブ（クリックされていない）インプレッションの両方を考慮して得られた。
We first score these two impressions with our model.
まず、この2つのimpressionsを我々のモデルでscore付けする。
If the negative impression receives a higher score than the positive impression, then we consider the positive impression’s watch time to be mispredicted watch time.
**ネガティブな印象がポジティブな印象よりも高いスコアを獲得した場合、ポジティブな印象の視聴時間はミス予測された視聴時間とみなす。**
Weighted, peruser loss is then the total amount mispredicted watch time as a fraction of total watch time over heldout impression pairs.
加重されたユーザごとの損失は、**誤って予測された視聴時間の合計が、保持されたimpressionペアの視聴時間の合計に占める割合**となる。

These results show that increasing the width of hidden layers improves results, as does increasing their depth.
これらの結果は、**隠れ層の幅を広げると結果が改善されること**を示している。
The trade-off, however, is server CPU time needed for inference.
しかし、**そのトレードオフは、推論に必要なサーバーのCPU時間**である。
The configuration of a 1024-wide ReLU followed by a 512- wide ReLU followed by a 256-wide ReLU gave us the best results while enabling us to stay within our serving CPU budget.
1024ワイドのReLU、512ワイドのReLU、256ワイドのReLUという構成が、CPUの予算内で最良の結果をもたらした。

For the 1024 → 512 → 256 model we tried only feeding the normalized continuous features without their powers, which increased loss by 0.2%.
1024→512→256モデルでは、正規化された連続特徴量のみをべき乗なしで与えてみたが、損失は0.2%増加した。
With the same hidden layer configuration, we also trained a model where positive and negative examples are weighted equally.
同じ隠れ層構成で、正例と負例を等しく重み付けしたモデルも訓練した。
Unsurprisingly, this increased the watch time-weighted loss by a dramatic 4.1%.
当然のことながら、これによって視聴時間の加重損失は4.1%も激増した。
(要は、論文内で説明された各工夫がそれぞれ効果を発揮して、betterな結果を作ったよ、という意味かな...!)

# 5. Conclusions 結論

We have described our deep neural network architecture for recommending YouTube videos, split into two distinct problems: candidate generation and ranking.
YouTube動画を推薦するためのディープ・ニューラル・ネットワーク・アーキテクチャを、2つの異なる問題に分けて説明した： 候補の生成とランキングである。

Our **deep collaborative filtering model**(これがtwo tower modelなのかな??) is able to effectively assimilate many signals and model their interaction with layers of depth, outperforming previous matrix factorization approaches used at YouTube [23].
私たちのディープ協調フィルタリングモデルは、多くの信号を効果的に同化し、深さのレイヤーでそれらの相互作用をモデル化することができ、YouTubeで使用されている以前の行列因数分解アプローチ[23]を凌駕している。
There is more art than science in selecting the surrogate problem for recommendations and we found classifying a future watch to perform well on live metrics by capturing asymmetric co-watch behavior and preventing leakage of future information.
**レコメンデーションのためのsurrogate問題の選択**には、科学よりも芸術が必要であり、我々は、**非対称的な共同視聴行動を捕捉**し、**将来の情報の漏洩を防止すること**によって、ライブメトリクスのパフォーマンスを向上させるために、将来の視聴を分類することを発見した。(**next-item prediction的なsurrogate問題を採用した**、って認識...!:thinking:)
Withholding discrimative signals from the classifier was also essential to achieving good results - otherwise the model would overfit the surrogate problem and not transfer well to the homepage.
識別シグナルを分類器から除外すること(=ユーザの最後の検索クエリとかを、モデルに知られない様にする事!)も、良い結果を得るためには不可欠であった。そうでなければ、モデルはサロゲート問題にオーバーフィットしてしまい、ホームページにはうまく反映されない。
We demonstrated that using the age of the training example as an input feature removes an inherent bias towards the past and allows the model to represent the time-dependent behavior of popular of videos.
我々は、入力特徴量として**training exampleの年齢**を使用することで、過去への固有のバイアスを取り除き、**人気のあるビデオの時間依存的な挙動**をモデルで表現できることを実証した。
This improved offline holdout precision results and increased the watch time dramatically on recently uploaded videos in A/B testing.
これにより、オフラインでのhold-out精度が向上し、**A/Bテストでは最近アップロードされた動画の視聴時間が劇的に伸びました**。

Ranking is a more classical machine learning problem yet our deep learning approach outperformed previous linear and tree-based methods for watch time prediction.
ランキングはより古典的な機械学習問題だが、我々のディープラーニング・アプローチは、視聴時刻の予測タスクとして、これまでの線形手法や樹木ベースの手法を凌駕した。
Recommendation systems in particular benefit from specialized features describing past user behavior with items.
特にレコメンデーションシステムは、アイテムに対する過去のユーザ行動を記述する特殊な特徴量から恩恵を受ける。
Deep neural networks require special representations of categorical and continuous features which we transform with embeddings and quantile normalization, respectively.
ディープ・ニューラル・ネットワークは、カテゴリ特徴量と連続特徴の特別な表現を必要とし、**それぞれ埋め込み(=疎->密なベクトル)と分位正規化で変換する**。
Layers of depth were shown to effectively model non-linear interactions between hundreds of features.
深いレイヤーは、何百もの特徴量間の非線形相互作用を効果的にモデル化することが示された。

Logistic regression was modified by weighting training examples with watch time for positive examples and unity for negative examples, allowing us to learn odds that closely model expected watch time.
ロジスティック回帰は、**肯定的な例では視聴時間で training example を重み付け**し、否定的な例では単一にすることで修正され、視聴時間期待値を忠実にモデル化する確率を学習できるようにした。
This approach performed much better on watch-time weighted ranking evaluation metrics compared to predicting click-through rate directly.
このアプローチは、クリックスルー率を直接予測するのに比べ、視聴時間で重み付けされたランキング評価指標においてはるかに優れた結果を示した。(これは、そもそも視聴時間予測で最適化しているモデルなのだから、tap予測で最適化しているモデルと比べて良い結果になるのは当然??:thinking:)
