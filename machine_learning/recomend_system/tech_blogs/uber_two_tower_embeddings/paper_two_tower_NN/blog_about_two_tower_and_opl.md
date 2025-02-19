# タイトル: 推薦システムの実務で人気なTwo-Towerモデルを「反実仮想機械学習」的なアプローチでオフライン学習させてみた!

## 3行まとめ

- **推薦システムの実務で人気なTwo-Towerモデル**は、論文や活用事例などを眺めている感じでは、**何らかの予測タスクを代理問題としてその誤差を最小化するようにパラメータ学習する「回帰ベース」のアプローチ**が多い印象。
- 本ブログでは、**ログデータを元に推薦方策の性能を最大化するように学習する「勾配ベース」のアプローチ**で、Two-Towerモデルのパラメータを更新することを検討した。
- また、PytorchでTwo-Towerモデルと3種類のオフライン学習方法 (IPS推定量に基づく勾配ベース, DR推定量に基づく勾配ベース, 報酬rの予測問題として解く回帰ベース) を実装し、Open Bandit Pipelineパッケージの合成データを使って実験を行った。

## はじめに

- 推薦システムのオフライン評価 & オフライン学習が難しい問題。
- 書籍「反実仮想機械学習」にて、データ収集方策によるログデータの偏りなどを考慮したオフライン学習方法を知る。
- 実務で人気なTwo-Towerモデル。論文を見ると、基本的には**即時報酬の予測問題として予測誤差を最小化するようにモデルを学習**させて推薦方策を作るようなアプローチ (i.e. 回帰ベースのアプローチ) が多いように見える。
- 本ブログでは、「反実仮想機械学習」的に、事前に定義しておいた推薦方策の性能 (の推定値) を直接最適化するようなアプローチ (i.e. 勾配ベースのアプローチ) で、Two-Towerモデルの学習を試みる...!

もし何か気になる点などあれば、ぜひカジュアルにコメントいただけたら嬉しいです:)

## Two-Towerモデルはこんな感じの雰囲気

Two-Towerモデルは、推薦システムや検索タスクで広く使われる**深層学習ベースのモデルの一つ**です。特に**大規模なコーパス（数百万〜数億規模のアイテム）から関連アイテムを高速に取得するretrievalフェーズ**に強みを持ちます。なので実システムでよくある2-stages推薦システムにおいて、特に1ステージ目の「retrieval」部分を担当することが多い印象です(2ステージ目の「reranking」部分は、別のリッチなモデルが使われることも多い)。

### Two-Towerモデルの構造

構造上の特徴としては、**以下の2つの encoder (i.e. tower)** から構成されます。
(ちなみにNLP分野では「**デュアルエンコーダ(dual encoder)**」と呼ばれているらしい...!:thinking:)

- ユーザタワー（User Tower）: ユーザ情報やコンテキストや検索クエリなどを埋め込みベクトルに変換する。
- アイテムタワー（Item Tower）: 推薦対象アイテムを埋め込みベクトルに変換する。

学習時には、二つのタワーを一緒に学習することで**ユーザとアイテムを共通の埋め込み空間にマッピング**します。
（具体的には、両タワーが出力するベクトルの内積がなんらか意味を持つように、タワー内部のパラメータを更新していくイメージ...! 何を基準に学習していくかは当然、他のモデルと同様にケースバイケース:thinking:）。
推論時には、**二つのタワーが独立して稼働**できます。各ユーザ(クエリ)やアイテムの特徴量をそれぞれのタワーを通して埋め込みベクトルにencodeし、**埋め込み空間上で内積計算することで関連アイテム上位k個を高速に取得**できます。

### Two-Towerモデルの強み

- 推論がスケーラブルで高速:
  - 事前にアイテム埋め込みをインデックス化しておき近傍探索でretrieveできるので、大規模なデータセットでも高速に推論できる。
  - **推論時(検索時)の計算コストが低い** (クエリの埋め込みを計算 -> 事前計算されたアイテム埋め込みと内積計算するだけ)
- 特徴量の柔軟な活用
  - 任意のユーザやアイテムの特徴量を多層NNで非線形変換して埋め込みを作るので、**特徴量エンジニアリングの自由度が高い**
    - 画像特徴量、NLP的な特徴量なども組み込みやすい。
  - 扱いたい特徴量に応じて各towerの構造も柔軟にアレンジできる。
    - ニュース推薦の分野では、ニュースの閲読履歴などのsequentialなデータを扱うために、タワー内部にAttention機構を採用したりしてた...!:thinking:
  - また純粋な行動履歴ベースのモデル(行列分解など)よりも、アイテムやユーザの特徴量を柔軟に組み込めるので、コールドスタートアイテム、コールドスタートユーザに対応しやすい。(これはそりゃそう)

### 参考文献

- [Deep Neural Networks for YouTube Recommendations](https://static.googleusercontent.com/media/research.google.com/ja//pubs/archive/45530.pdf)
  - 2016年のYoutubeの動画推薦システムについて紹介してる論文。
  - DNNを使った2-stages推薦を採用しており、candidate retrieve用のモデルも candidate ranking用のモデルもTwo-Towerモデルを採用してた。
  - 「Two-Towerモデルを提案!」という内容ではなく、「Youtubeの推薦の困難さをこういう工夫で対処してますよ!」的なtipsを紹介してくれてる様な印象の論文:thinking:
- [Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations](https://research.google/pubs/mixed-negative-sampling-for-learning-two-tower-neural-networks-in-recommendations/)
  - 2020年のGoogle Playの推薦システムを取り扱った論文。こちらは主に2-stages推薦の1ステージ目candidate retrieveのモデルとしてTwo-Towerモデルを採用してた。論文のメイントピックは、Two-Towerモデル学習時のバイアス問題に対処するためのネガティブサンプリング方法について。
- [Innovative Recommendation Applications Using Two Tower Embeddings at Uber](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
  - こちらは論文ではないが、UberさんのテックブログでTwo-Towerモデルを使った推薦システムの応用事例が紹介されてた。
  - ちなみに自分はこのブログを読んでTwo-Towerアーキテクチャを知り、一つ目の論文に辿り着きました!感謝...!:pray:
- [Two-Towerモデルと近似最近傍探索による候補生成ロジックの導入](https://blog.recruit.co.jp/data/articles/two-tower-model/)
  - リクルートさんのテックブログ。
  - ちなみに自分はこのブログから、二つ目の論文に辿り着きました!感謝...!:pray:

## 勾配ベースのオフ方策学習はこんな感じの雰囲気

### オフ方策学習(Off-policy learning, OPL)とは??

オフ方策学習 (Off-policy learning, OPL) とは、観測されたログデータを使って、オフライン環境で新しい方策(policy)を学習する手法です。
(「オフライン学習」と言い換えても問題ないと思ってます...!)

- オフ方策学習の例
  - 既存の推薦方策が本番稼働しており、全ユーザに「ニュース記事A」を50%、「ニュース記事B」を30%の確率で推薦しているとする。
  - その推薦結果とユーザから得られた報酬（ex. クリック、購入、etc.）を記録し、そのログデータ(i.e. バンディットフィードバック)を使って、より良い推薦方策をオフライン環境で学習する。

### オフ方策学習の基本的な2種類のアプローチ:

オフ方策学習には、2つの基本的なアプローチとして**回帰ベースと勾配ベース**があります。
(ちなみに、両者を混ぜて段階的に学習させるようなハイブリッドアプローチなども近年はあるみたいです...!)。

ざっくり回帰ベースと勾配ベースのアプローチとの違いは、予測誤差を最小化するように学習するのか、それとも方策性能を最大化するように学習するのか、という点ですね...!

#### 1. 回帰ベース(Regression-based)

教師あり機械学習っぽいアプローチ。
書籍「反実仮想機械学習」では、以下のように定義されていました!

> オフ方策学習における回帰ベースのアプローチとは、データ収集方策によって収集されたログデータDのみを用いて期待報酬関数 $q(x,a)$ を推定し、それを方策に変換する手順のことである。
> (書籍「反実仮想機械学習」より引用)

回帰ベースアプローチでは、あるコンテキスト(ex. ユーザ, クエリ)に対する各アクションの報酬期待値 $E_{p(r|x,a)}[r] = q(x,a)$ を推定するモデル $\hat{q}(a,x)$ を学習し、予測関数 $\hat{q}(a,x)$ の出力値を直接使って、推薦アイテムを選択する方策を作ります。
例えば、「CTR予測モデルを学習させて予測値が高いアイテムを推薦する」ような事例は、もろ回帰ベースのアプローチと言えそうです。(なぜならCTRというのは結局、報酬 r をクリックしたか否かの2値変数として定義した場合の、期待報酬関数 $q(x,a) := E_{p(r|x,a)}[r]$ に相当するものだと思うので...!)
おそらく、教師あり学習を使った推薦モデルのアプローチの多くは、ほぼほぼ回帰ベースのアプローチに分類できそうな気がします...!:thinking:

Two-Towerモデルの事例で言えば、例えば参考文献1のYoutubeの事例では、Two-Towerモデルを2-stages推薦のretrievalフェーズとrankingフェーズの両方で使っていました。そして前者(retrievalフェーズ)のTwo-Towerモデルでは**視聴されたアイテムを予測する他クラス分類問題**として、後者(rankingフェーズ)のTwo-Towerモデルでは**視聴時間を予測する回帰問題**として学習(i.e. パラメータ更新)させていました。
これらはともに回帰ベースのアプローチに分類されると思います (前者については期待報酬関数を予測させてる訳ではない気がするから分類に迷いますが、少なくとも後述する勾配ベースのアプローチではないので...!:thinking:)。

また、参考文献5のニュース推薦タスクのNRMSモデル (タワー内部にAttention機構を採用してるTwo-Towerモデル!) では、ニュース記事を表示させて閲読したか否かの2値分類問題 (まさにCTR予測問題!) として学習させていました。これは明確に回帰ベースのアプローチに分類されそうですね...!:thinking:

よって実際に回帰ベースのアプローチで学習する際には、例えば以下のような感じのパラメータ更新則になりそうです...!

$$
loss = \sum_{i=1}^{n} l_{r}(r_i, \hat{q}(x_i, a_i))
\\
\theta_{t+1} \leftarrow \theta_{t} - \nu \nabla_{\theta} loss
$$

ここで、$l_{r}(r_i, \hat{q}(x_i, a_i))$ は、クロスエントロピー誤差や平均二乗誤差などの任意の誤差関数を表します。$\nu$ は学習率(ハイパーパラメータ)。また $\nabla_{\theta} loss$ は損失関数のモデルパラメータ $\theta$ に対する勾配(i.e. 微分) を意味します。

#### 2. 勾配ベース(Gradient-based)

ざっくり強化学習っぽいアプローチ。
勾配ベースのアプローチの基本的なアイデアは、**推薦方策の性能 (policy value) $V(\pi_{\theta})$ が高くなるように以下のようなパラメータ更新則でモデルパラメータを更新**していくことです。

$$
\theta_{t+1} \leftarrow \theta_{t} + \nu \nabla_{\theta} V(\pi_{\theta})
$$

ここで、$\nu$ は学習率(ハイパーパラメータ)。また $\nabla_{\theta} V(\pi_{\theta})$ は方策勾配(policy gradient) と呼ばれ、方策性能のモデルパラメータ $\theta$ に対する勾配(i.e. 微分) を意味します。
勾配降下法っぽい式ですね! あ、でも**方策性能を最大化したいから、右辺第二項の符号がプラス**なのか...!:thinking: 確か勾配降下法は、基本的にlossを最小化していくから、ここの符号がマイナスだった...!
(ちなみに実装時には、目的関数の最大化よりも最小化の方がPytorchで実装しやすいので、マイナスをかけて最小化問題としてます!)

先に述べた通り、回帰ベースのアプローチはなんらか予測誤差を最小化するように学習するのに対して、勾配ベースのアプローチは方策性能を最大化するように学習するという違いがありますね。

勾配ベースアプローチのアイデアは上記のとおりです。
**ただし残念ながら、上記のやり方の通りにパラメータ更新を行うことはできません。なぜなら、真の方策性能 $V(\pi_{\theta})$ は未知だから**です! 
(この話は、推薦システムのオフライン評価が難しい話でも良く言われていることですね!)
真の方策性能 $V(\pi_{\theta})$ が未知なので、その方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ も我々は知ることができず、そのままではパラメータ更新ができません。

そこで実際には、**何らかの方法で真の方策勾配を推定して、その推定値を使って方策のパラメータを更新していく**ことになります。なので勾配ベースアプローチにおける実際のパラメータ更新則は以下のようになります。ハットがついてますね...!!

$$
\theta_{t+1} \leftarrow \theta_{t} + \nu \hat{\nabla_{\theta}} V(\pi_{\theta})
$$

ここで $\hat{\nabla_{\theta}} V(\pi_{\theta})$ は、ログデータに基づく真の方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ の推定値を表します。

書籍「反実仮想機械学習」では、勾配ベースのアプローチが以下のように定義されています。方策勾配を推定し、って書いてますね...!

> オフ方策学習における勾配ベースのアプローチとは、データ収集方策によって収集されたログデータDのみを用いて方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ を推定し、それに基づいて高性能を導く方策のパラメータを学習するアプローチである。
> (書籍「反実仮想機械学習」より引用)

オフ方策評価(OPE, Off-policy evaluation)ではいろんな手段で方策性能を確度高く推定しようとしていた訳ですが、**オフ方策学習では方策性能の勾配を頑張って確度高く推定することが重要**になりそうですね...!

### 勾配ベースアプローチにおける、真の方策勾配の推定方法の例

#### IPS推定量(Importance Sampling Estimator)

オフ方策評価でも王道アプローチ的な立ち位置にある「IPS推定量」の考え方を、方策勾配の推定に応用すると以下のようになります。

$$
\hat{\nabla_{\theta}} V_{IPS}(\pi_{\theta};D) := \frac{1}{n} \sum_{i=1}^{n} w(x_i, a_i) r_i \nabla_{\theta} \log \pi_{\theta}(a_i|x_i)
$$

ここで $w(x, a):= \pi_{\theta}(a|x) / \pi_{0}(a|x)$ は重要度重み。学習対象の新方策とデータ収集方策による行動選択確率の比を表します。

#### DR推定量(Doubly Robust Estimator)

IPS推定量の問題点として、重要度重みの大きさが原因で発生するバリアンスが挙げられます。IPS推定量の強みである不偏性を維持しつつ、バリアンスを減少させる方法として、メジャーなのがDR(Doubly Robust)推定量です。

DR推定量の基本的なアイデアは、「ログデータを用いて事前に学習しておいた**期待報酬関数に対する推定モデル $\hat{q}(x, a)$ をベースライン**として使うことで、**IPS推定量からのバリアンス減少を狙う!**」というものです。
方策勾配のDR推定量は以下のようになります。

$$
\hat{\nabla_{\theta} V_{DR}(\pi_{\theta};D)} := \frac{1}{n} \sum_{i=1}^{n} 
\Big\{
  w(x_i, a_i) (r_i - \hat{q}(x_i, a_i)) \nabla_{\theta} \log \pi_{\theta}(a_i|x_i) 
  \\
  + E_{\pi_{\theta}(a|x)}[\hat{q}(x_i, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]
\Big\}
$$

ここで、$\hat{q}(x_i, a_i)$ は期待報酬関数 $q(x, a)$ に対する推定モデルを意味します。例えば回帰ベースのアプローチと同様に、ログデータ $D$ を用いて損失関数を最小化して求めたモデルを使ったりします! (ここの推定モデルは、線形回帰だったり、ニューラルネットだったり、LightGBMだったりですね! パラメータ学習時にしか使わないので、リッチなモデルを使っても全然問題ないと思ってます...!:thinking:)

#### ちなみに...方策性能の定義から方策勾配の式の導出までの流れ

ここは式変形の流れなので、興味ある方だけ読んでください...!

まず方策性能を定義。
「ある環境 $p(x)$ において、方策 $\pi_{\theta}$ を稼働させて行動を選択した場合に得られる報酬の期待値」を、方策性能として次のように定義します。
(この方策性能の定義は一般的ですが、場合によっては分散を考慮したりなどいろいろ工夫はありそうです...!)

$$
V(\pi_{\theta}) = E_{p(x) \pi_{\theta}(a|x) p(r|x,a)}[r] = E_{p(x)\pi_{\theta}(a|x)}[q(x, a)]
\\
\because q(x, a) = E_{p(r|x,a)}[r]
$$

次に方策勾配を定義する。
方策性能 $V(\pi_{\theta})$ のパラメータ $\theta$ に関する勾配は、以下のように表現できます。(ナブラ記号に、方策性能の定義を代入しただけ!)

$$
\nabla_{\theta} V(\pi_{\theta}) = \nabla_{\theta} E_{p(x)\pi_{\theta}(a|x)}[q(x, a)]
$$

最後に、方策勾配の式を扱いやすいように変形していく。
いろいろなテクニックを使って式変形していくと、最終的に以下のように表現できるようです。
(「期待値の勾配」=「勾配の期待値」の性質だったり、「同時分布の期待値」=「条件付き期待値の期待値」の性質だったり、ログトリック(条件付き確率の勾配の変形)を使ったり、...などなどしていい感じに式変形していく...!)

$$
\nabla_{\theta} V(\pi_{\theta}) = E_{p(x)\pi_{\theta}(a|x)}[q(x, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]
$$

この真の方策勾配の式を元に、IPS推定量だったりDR推定量だったりを駆使して、いい感じの推定量を作って、方策のモデルパラメータをいい感じに更新していく！というのが勾配ベースのオフ方策学習の基本的な流れなんでした...!:thinking:

### 参考文献

- 書籍「反実仮想機械学習〜機械学習と因果推論の融合技術の理論と実践」
  - 意思決定方策のオフライン学習とかの手法の考え方などを、かなり丁寧に優しく解説してくれている書籍。著者のusaitoさんブシが文章から感じられて楽しさもある...! ありがてぇ...!:pray:

## Two-Towerモデルを勾配ベースのアプローチでオフ方策学習するための定式化

### まずはTwo-Towerモデルに基づく推薦方策の定義

まずは、Two-Towerモデルに基づく推薦方策を定義してみます。

Two-Towerモデルの学習可能な全パラメータを $\theta$ で表し、このTwo-Towerモデルに基づく推薦方策を $\pi_{\theta}$ と表します。
推薦方策 $\pi_{\theta}$ の行動選択の確率分布は、以下の条件付き確率分布で表されます。

$$  
\pi_{\theta}(a|x) := p(a|x, \theta)
$$

ここで、$x$ はコンテキスト(ユーザ特徴量など)、$a$ は推薦アイテム、そして $\theta$ はTwo-Towerモデルのパラメータを表します。
つまりこの分布は、コンテキスト(ユーザ特徴量) $x$ とTwo-Towerモデルのパラメータ $\theta$ を条件付けた時の、アイテム $a$ を推薦する条件付き確率(確率質量関数)を意味しています ($p(a|x, \pi_{\theta})$ みたいなイメージ!)。

次に、この $\pi_{\theta}(a|x)$ を、Two-Towerモデルの出力値を使ってどんな確率質量関数として表現するか考えてみます。
Two-Towerモデルでは、ユーザ特徴量 $x$ とある推薦候補アイテム $a$ のアイテム特徴量を入力として、最終的にユーザ埋め込みとアイテム埋め込みの内積値を出力するんでした。
今回はその出力値を以下のように表記してみます!

$$
TwoTowerModel_{\theta}(x, a) := \text{ユーザ埋め込み} \cdot \text{アイテム埋め込み}
$$

さてこの出力値を元に、推薦方策の振る舞いを表す確率質量関数 $\pi_{\theta}(a|x)$ を表現したいわけです。確率質量関数は以下の2つの性質を持っている必要があります。

- 全ての推薦アイテム $a$ に対する確率(質量)が0以上であること(i.e. 非負性): $\pi_{\theta}(a|x) \geq 0,  \forall a \in A$      
- 全ての推薦アイテム $a$ に対する確率(質量)の総和が1であること(i.e. 正規化条件): $\sum_{a \in A} \pi_{\theta}(a|x) = 1$

この2つの性質を満たせるように、今回はそんなに深く考えずに**ソフトマックス関数**を使うことにします! ソフトマックス関数は以下のように定義される関数です。

$$
\text{softmax}(a) = \frac{\exp(a/\tau)}{\sum_{a' \in A} \exp(a'/\tau)}
$$

ここで、$\tau$ は温度パラメータであり、その値によって確率分布の滑らかさが調整されます。
$\tau$ を大きくすると、各$a$の確率質量が小さくなり均等な分布になりやすくなります。逆に$\tau$ を小さくすると、各$a$の確率質量の差が大きくなり、最も確率質量の大きいアイテムが選ばれやすくなります。

このソフトマックス関数を使って、Two-Towerモデルに基づく推薦方策の行動選択確率分布 $\pi_{\theta}(a|x)$ を以下のように表現できそうですね!
(ユーザ特徴量 $x$ とTwo-Towerモデルのパラメータ $\theta$ で条件付けた場合の、アイテム $a$ を推薦する確率質量関数を意味しています!)

$$
\pi_{\theta}(a|x) := p(a|x, \theta) 
\\
= \text{softmax}(TwoTowerModel_{\theta}(x, a)) 
\\
= \frac{\exp(TwoTowerModel_{\theta}(x, a) / \tau)}{\sum_{a' \in A} \exp(TwoTowerModel_{\theta}(x, a') / \tau)}
$$

### 次に、推薦方策の性能　（Policy Value）を定義する

次に、推薦方策の良し悪しを判断するための方策性能(policy value)を定義します。
今回はそこまで深く考えず書籍「反実仮想機械学習」でも採用されていた、以下の「期待報酬の期待値」をそのまま使うことにします。

$$
V(\pi_{\theta}) = E_{p(x) \pi_{\theta}(a|x) p(r|x,a)}[r] = E_{p(x)\pi_{\theta}(a|x)}[q(x, a)]
$$

ここで、$r$ は(即時)報酬、$q(x, a)$ はコンテキスト $x$ とアイテム $a$ で条件付けられた報酬の条件付き期待値(i.e. 条件付き確率分布 $p(r|x,a)$ に関する報酬 r の期待値)を表します。
この方策性能の真の値は未知なので、A/Bテストのようなオンライン評価ではAVG推定量、オフライン評価ではIPS推定量やDR推定量などのOPE推定量で推定し、より各々のビジネス目的に適した推薦方策を探していくんですよね。

### 最後に、方策勾配（Policy Gradient）とその推定方法を定義する

最後に、勾配ベースのアプローチでTwo-Towerモデルに基づく推薦方策を学習するために、パラメータ更新則で登場する方策勾配(policy gradient)を定義します。
方策勾配は定義より、以下のように表現できます。

$$
\nabla_{\theta} V(\pi_{\theta}) = E_{p(x)\pi_{\theta}(a|x)}[q(x, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]
$$

これは「Two-Towerモデルのパラメータ $\theta$ を変化させた時に、方策性能 $V(\pi_{\theta})$ がどのように変化するか」を表す微分のイメージですね...!

さて実環境では、真の方策性能と同様に、推定方策性能も未知なので、推定量を使うぞ...!!
より具体的には、あるデータ収集方策 $\pi_{0}(a|x)$ で収集したログデータ $D = \{(x_i, a_i, r_i)\}_{i=1}^{n}$ に対して、なんらかの推定量を使って方策勾配を推定するんでした。
今回は、IPS推定量とDR推定量を使って、方策勾配を推定することにします。
これらの推定量の定義式は、前述のIPS推定量とDR推定量の定義式をそのまま使います!

$$
\hat{\nabla_{\theta}} V_{IPS}(\pi_{\theta};D) := \frac{1}{n} \sum_{i=1}^{n} \frac{\pi_{\theta}(a_i|x_i)}{\pi_{0}(a_i|x_i)} r_i \nabla_{\theta} \log \pi_{\theta}(a_i|x_i)
$$

$$
\hat{\nabla_{\theta} V_{DR}(\pi_{\theta};D)} := \frac{1}{n} \sum_{i=1}^{n}
\Big\{
  \frac{\pi_{\theta}(a_i|x_i)}{\pi_{0}(a_i|x_i)} (r_i - \hat{q}(x_i, a_i)) \nabla_{\theta} \log \pi_{\theta}(a_i|x_i)
  \\
  + E_{\pi_{\theta}(a|x)}[\hat{q}(x_i, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]
\Big\}
$$

上記の方策勾配の推定量を用いて、それぞれ以下のパラメータ更新則で、Two-Towerモデルのパラメータ $\theta$ を更新していくことになります。

$$
\theta_{t+1} \leftarrow \theta_{t} + \nu \hat{\nabla_{\theta} V_{IPS}(\pi_{\theta};D)}
$$

$$
\theta_{t+1} \leftarrow \theta_{t} + \nu \hat{\nabla_{\theta} V_{DR}(\pi_{\theta};D)}
$$

ちなみに、Pytorchで実装する場合、自動微分機能を使って実装することになるので、**方策勾配の推定量の定義式からナブラを外します**。また、本来は方策性能を最大化したいわけですが、Pytorchの最適化関数は損失関数を最小化するように設計されているのでマイナスをかけます。よってPytorchでの実装上は、以下のようなloss関数を最小化するようにパラメータ更新することになります。

$$
loss_{IPS} = - \frac{1}{n} \sum_{i=1}^{n} \frac{\pi_{\theta}(a_i|x_i)}{\pi_{0}(a_i|x_i)} r_i \log \pi_{\theta}(a_i|x_i)
$$

$$
loss_{DR} = - \frac{1}{n} \sum_{i=1}^{n}
\Big\{
  \frac{\pi_{\theta}(a_i|x_i)}{\pi_{0}(a_i|x_i)} (r_i - \hat{q}(x_i, a_i)) \log \pi_{\theta}(a_i|x_i)
  \\
  + E_{\pi_{\theta}(a|x)}[\hat{q}(x_i, a) \log \pi_{\theta}(a|x)]
\Big\}
$$

### 実験の比較対象として、回帰べースのアプローチも考えておこう!

ちなみに、実験する際の比較対象として、回帰ベースのアプローチも考えておきます。
回帰ベースのアプローチでは、教師あり学習的に、Two-Towerモデルの出力値がなんらかの誤差関数を最小化するようにパラメータを更新していけば良さそうです。

今回はシンプルにクロスエントロピー誤差関数を使って、**「特徴量 $x$ とアイテム $a$ のペアを使って、観測された(即時)報酬 $r$ を予測する」という代理問題を解くことでパラメータ更新する**ようにしてみましょう。
(CTR予測モデルみたいな感じでTwo-Towerモデルを学習させる、というイメージですね...!:thinking:)

$$
loss = \sum_{i=1}^{n} l_{r}(r_i, \text{TwoTowerModel}_{\theta}(x_i, a_i))
\\
= \sum_{i=1}^{n} \text{CrossEntropyLoss}(r_i, \text{TwoTowerModel}_{\theta}(x_i, a_i))
$$

## 合成データを使って、Two-Towerモデルのオフ方策学習を実験してみる!

### 実験でざっくり確認したいこと

なんとなく、以下のようなことを確認したいです!

- 疑問1: 勾配ベースのアプローチでオフライン学習させて、ちゃんと方策性能を高めるようにパラメータ更新できる? (i.e. まずそもそもちゃんと実装できてる??)
- 疑問2: 勾配ベースのアプローチと回帰ベースのアプローチ、どっちが効果的??
- 疑問3: 勾配ベースのアプローチの中で、IPS推定量とDR推定量、どっちが効果的??
  - (書籍だとDR推定量がIPS推定量の完全上位互換、という感じだったが...!:thinking:)
- 疑問4: 推薦アイテム候補数が変わると、オフライン学習の効果にどのような影響がある?
  - 書籍を読んだ感じでは、推薦アイテム候補数が多いほど、基本的にタスクとしては難しくなるはず。
- 疑問5: (個人的に気になったこと!)オフライン学習時のバッチサイズが変わると、オフライン学習の効果にどのような影響があるか?
  - 統計的推定の観点からだと、より精度高く方策勾配を推定できる方が嬉しいはず。なので、学習時のバッチサイズは大きめの方が良さそう...?? 学習時の目的関数として、ログデータから推定した方策性能の推定値を使うのであれば、その分散はなるべく小さくしたい。

### Two-Towerモデルのオフ方策学習の実験設定

以下のような実験設定を考えました!

- 報酬 $r$ がbinary変数(0/1)として観測されるケースを想定(ex. クリック/非クリック, 購買/非購買, メール開封/非開封など)
- 確率的なデータ収集方策 $\pi_{0}(a|x)$ によって、ログデータ $D = \{(x_i, a_i, r_i)\}_{i=1}^{n}$ が収集される。
  - 今回は特徴量 $x$ やアイテム $a$ の特徴量は、一様分布から乱数生成して得る。
  - データ収集方策 $\pi_{0}(a|x)$ は以下の2パターンを実験で使用した。
    - パターン1: 一様ランダムなデータ収集方策。$\pi_{0}(a|x) = 1/|A|, \forall a \in A, x \in X$
    - パターン2: context-awareで確率的なデータ収集方策。確率(1-ε)で、ユーザ特徴量とアイテム特徴量の内積が最も高いアイテムを決定的に選択する。確率εで、全てのアイテムを等確率で選択するε-greedy方策。
- 3種類のオフライン学習方法を比較する
  - パターン1: IPS推定量を使った勾配ベースのアプローチ
  - パターン2: DR推定量を使った勾配ベースのアプローチ
  - パターン3: 回帰ベースのアプローチ (クロスエントロピー誤差関数を使った教師あり学習)
- Two-Towerモデルの構造は、学習方法によらず共通とする。
  - Two-Towerの入力となるユーザ特徴量とアイテム特徴量は、それぞれ50次元のベクトルとする。
  - Two-Towerモデルの各タワーの埋め込み層の次元数は100次元とする。
  - 各タワーの構造はどちらも、中間層が3層の全結合層で構成される。
  - 各中間層のユニット数はそれぞれ(100, 100, 100)とする。
- 推薦アイテム候補数は10で固定。 
  - また疑問4を確認するために、推薦アイテム候補数の違いが学習後の方策性能に与える影響の検証もしました!
    - [10, 50, 100, 200, 500, 1000, 2000, 5000]
- オフライン学習時のエポック数は100で固定。
- オフライン学習時のバッチサイズは10で固定。
  - (理由: 推薦アイテム候補数10かつ学習データ数15000の場合に、バッチサイズ10だと、学習後の方策性能が最も高くなった経験則より)
  - また疑問5を確認するために、バッチサイズの違いが学習後の方策性能に与える影響の検証もしました!
    - [10, 100, 200, 500, 1000, 2000, 5000]

### 実験結果

<!-- 図1: 一様ランダムなデータ収集方策の場合のTwo-Towerモデルによる推薦方策のオフライン学習効果 -->

図1は、一様ランダムなデータ収集方策で収集したログデータに対して、IPS推定量、DR推定量、回帰ベースのアプローチでTwo-Towerモデルによる推薦方策のオフライン学習効果を比較した結果です。横軸は学習データ数 $N$、縦軸は学習後の方策性能 $V(\pi_{\theta})$ です。
三種類のオフライン学習方法がそれぞれ、学習データ数が増えるにつれて、学習後の方策性能が向上していることが確認できます。とりあえずちゃんと実装できていそうで、一安心ですね...!!

<!-- 図2: 偏ったデータ収集方策の場合のTwo-Towerモデルによる推薦方策のオフライン学習効果 -->

図2は、context-awareな意思決定を行うような、偏ったデータ収集方策で収集したログデータに対して、IPS推定量、DR推定量、回帰ベースのアプローチでTwo-Towerモデルによる推薦方策のオフライン学習効果を比較した結果です。縦軸、横軸の意味は図1と同じです。
こちらも図1と同様に、3種類のオフライン学習方法の全てで、学習データ数が増えるにつれて、新方策の性能が向上してますね...!

DR推定量とIPS推定量はそれぞれ、学習データの偏りを補正して不偏推定量になる工夫(=具体的には重要度重み!)を導入しているので、オフライン学習が上手く機能してくれているのは期待通りなのですが、意外にもnaiveな誤差関数を使っている回帰ベースアプローチが大健闘する結果になっていますね...! :thinking:

<!-- 図3: 推薦アイテム候補数の違いが学習後の方策性能に与える影響 -->

図3は、推薦アイテム候補数を変化させた場合の、Two-Towerモデルによる推薦方策のオフライン学習効果を比較した結果です。横軸は推薦アイテム候補数、縦軸は学習後の方策性能 $V(\pi_{\theta})$ です。
3種類のオフライン学習方法の全てで、推薦アイテム候補数が増えるにつれて、学習後の方策性能が低下しています。その中で回帰ベースのアプローチは最も性能が低下していました。
推薦アイテム候補数Nが5000個の場合では、DR推定量による勾配ベースのアプローチが最も高いオフライン学習効果になっていました。

(このあたりの各手法の優劣関係って、バッチサイズとかのハイパーパラメータ調整次第で変わったりするのかな...とも思ったりしました:thinking:)

<!-- 図4: バッチサイズの違いが学習後の方策性能に与える影響 -->

最後に図4は、パラメータ更新を行うバッチサイズを変化させた場合の、Two-Towerモデルによる推薦方策のオフライン学習効果を比較した結果です。横軸はバッチサイズ、縦軸は学習後の方策性能 $V(\pi_{\theta})$ です。

前述の疑問5での予想に反して、3種類のオフライン学習方法の全てでバッチサイズ10の場合に最も高いオフライン学習効果となり、バッチサイズが大きくなるにつれて学習後の方策性能が横ばいorやや低下していく結果となりました。
(ひょっとするとこの結果も、推薦タスクの問題設定次第だったりするのかなぁと思いました...! 例えば推薦アイテム候補数が多い場合だとバッチサイズを大きくする方が有効だったりするのかも...???:thinking:)

## おわりに

本記事では、Two-Towerモデルを用いた推薦方策のオフライン学習に対して、一般的な回帰ベースのアプローチだけでなく、勾配ベースのアプローチ（IPS推定量、DR推定量）を適用する試みを行いました！

実際にPytorchを用いてTwo-Towerモデルに基づく推薦方策のオフライン学習を実装し、合成データを使って実験を行いました。
今回の実験結果からは、正直どのオフライン学習方法が優れているかなどは判断できませんでした! まあ結局ケースバイケースなのかもな〜と思ってます:)

いずれにせよ、サービスの特性やビジネス課題に合わせてきちんと推薦システムという技術で問題解決できるように、ひいては機械学習の成果をスケールできるように、**我々開発者が柔軟にいい感じに目的関数や報酬関数を設計することで機械学習という技術を使いこなしていきたいな〜**という気持ちになりました:)

最後まで読んでいただき、ありがとうございました:)
もし何か気になる点などあれば、ぜひカジュアルにコメントいただけたら嬉しいです!

## ちなみに、pytorchでこう実装しました!

実装には、[こちらのusaitoさんの論文のリポジトリ](https://github.com/usaito/www2024-lope)と[Open Bandit Pipelineパッケージ](https://github.com/st-tech/zr-obp)の実装をめちゃめちゃ参考にしました! :pray:

ここでは、Two-Towerモデルに基づく推薦方策クラスを実装してます。
まずコンストラクタ。

```python
@dataclass
class PolicyByTwoTowerModel:
    """Two-Towerモデルのオフ方策学習を行うクラス
    実装参考: https://github.com/usaito/www2024-lope/blob/main/notebooks/learning.py
    """

    dim_context_features: int
    dim_action_features: int
    dim_two_tower_embedding: int
    softmax_temprature: float = 1.0
    hidden_layer_size: tuple = (30, 30, 30)
    activation: str = "elu"
    batch_size: int = 32
    learning_rate_init: float = 0.005
    alpha: float = 1e-6
    log_eps: float = 1e-10
    solver: str = "adam"
    max_iter: int = 200
    off_policy_objective: str = "dr"
    random_state: int = 12345

    def __post_init__(self):
        """Initialize class."""

        if self.activation == "tanh":
            activation_layer = nn.Tanh
        elif self.activation == "relu":
            activation_layer = nn.ReLU
        elif self.activation == "elu":
            activation_layer = nn.ELU

        # Context Tower
        context_tower_layers = []
        input_size = self.dim_context_features
        for idx, layer_size in enumerate(self.hidden_layer_size):
            context_tower_layers.append(
                (f"context_l_{idx}", nn.Linear(input_size, layer_size))
            )
            context_tower_layers.append((f"context_a_{idx}", activation_layer()))
            input_size = layer_size
        context_tower_layers.append(
            ("embed", nn.Linear(input_size, self.dim_two_tower_embedding))
        )
        self.context_tower = nn.Sequential(OrderedDict(context_tower_layers))

        # Action Tower
        action_layers = []
        input_size = self.dim_action_features
        for idx, layer_size in enumerate(self.hidden_layer_size):
            action_layers.append((f"action_l_{idx}", nn.Linear(input_size, layer_size)))
            action_layers.append((f"action_a_{idx}", activation_layer()))
            input_size = layer_size
        action_layers.append(
            ("embed", nn.Linear(input_size, self.dim_two_tower_embedding))
        )
        self.action_tower = nn.Sequential(OrderedDict(action_layers))

        self.nn_model = nn.ModuleDict(
            {
                "context_tower": self.context_tower,
                "action_tower": self.action_tower,
            }
        )

        self.train_losses = []
        self.train_values = []
        self.test_values = []
```

続いて推薦方策の推論用のpublic & privateメソッド。
入力として、n件のユーザ(i.e. コンテキスト、クエリ)特徴量と、推薦候補アイテムの特徴量を受け取る。
出力

```python
def predict_proba(
      self,
      context: np.ndarray,
      action_context: np.ndarray,
  ) -> np.ndarray:
      """方策による行動選択確率を予測するメソッド
      Args:
          context (np.ndarray): コンテキスト特徴量の配列 (n_rounds, dim_context_features)
          action_context (np.ndarray): アクション特徴量の配列 (n_actions, dim_action_features)
      Returns:
          np.ndarray: 行動選択確率 \pi_{\theta}(a|x) の配列 (n_rounds, n_actions, 1)
      """
      assert context.shape[1] == self.dim_context_features
      assert action_context.shape[1] == self.dim_action_features

      self.nn_model.eval()

      action_dist = self._predict_proba_as_tensor(
          context=torch.from_numpy(context).float(),
          action_context=torch.from_numpy(action_context).float(),
      )
      action_dist_ndarray = action_dist.squeeze(-1).detach().numpy()
      # open bandit pipelineの合成データクラスの仕様に合わせて、1つ軸を追加してる
      return action_dist_ndarray[:, :, np.newaxis]
  
def _predict_proba_as_tensor(
    self,
    context: torch.Tensor,
    action_context: torch.Tensor,
) -> torch.Tensor:
    """方策による行動選択確率を予測するメソッド。
    行動選択確率は各アクションのロジット値を計算し、softmax関数を適用することで得られる。
    学習時にも推論時にも利用するために、PyTorchのテンソルを入出力とする。
    Args:
        context (torch.Tensor): コンテキスト特徴量のテンソル (n_rounds, dim_context_features)
        action_context (torch.Tensor): アクション特徴量のテンソル (n_actions, dim_action_features)
    Returns:
        torch.Tensor: 行動選択確率 \pi_{\theta}(a|x) のテンソル (n_rounds, n_actions)
    """
    context_embedding = self.nn_model["context_tower"](
        context
    )  # shape: (n_rounds, dim_two_tower_embedding)
    action_embedding = self.nn_model["action_tower"](
        action_context
    )  # shape: (n_actions, dim_two_tower_embedding)

    # context_embeddingとaction_embeddingの内積をスコアとして計算
    logits = torch.matmul(
        context_embedding, action_embedding.T
    )  # shape: (n_rounds, n_actions)

    # 行動選択確率分布を得るためにsoftmax関数を適用
    pi = torch.softmax(
        logits / self.softmax_temprature, dim=1
    )  # shape: (n_rounds, n_actions)

    return pi
```

続いてpublicな学習用メソッド。`off_policy_objective`属性に応じて、学習方法を切り替えます。
今回は、勾配ベースとしてIPS推定量とDR推定量、回帰ベースとして報酬 $r$ の予測誤差関数(クロスエントロピー誤差関数)を使った学習を実装しています...!

```python
def fit(
    self,
    bandit_feedback_train: BanditFeedbackDict,
    bandit_feedback_test: Optional[BanditFeedbackDict] = None,
) -> None:
    """推薦方策を学習するメソッド"""
    if self.off_policy_objective in ("ips", "dr"):
        self._fit_by_gradiant_based_approach(
            bandit_feedback_train=bandit_feedback_train,
            bandit_feedback_test=bandit_feedback_test,
        )
    elif self.off_policy_objective == "regression_based":
        self._fit_by_regression_based_approach(
            bandit_feedback_train=bandit_feedback_train,
            bandit_feedback_test=bandit_feedback_test,
        )
    else:
        raise NotImplementedError(
            "`off_policy_objective` must be one of 'ips', 'dr', or 'regression_based'"
        )
```

勾配ベースアプローチのprivateな学習メソッド。

```python
def _fit_by_gradiant_based_approach(
    self,
    bandit_feedback_train: BanditFeedbackDict,
    bandit_feedback_test: Optional[BanditFeedbackDict] = None,
) -> None:
    """推薦方策を、勾配ベースアプローチで学習するメソッド"""

    n_actions = bandit_feedback_train["n_actions"]
    context, action, reward, action_context, pscore, pi_b = (
        bandit_feedback_train["context"],
        bandit_feedback_train["action"],
        bandit_feedback_train["reward"],
        bandit_feedback_train["action_context"],
        bandit_feedback_train["pscore"],
        bandit_feedback_train["pi_b"],
    )

    # optimizerの設定
    if self.solver == "adagrad":
        optimizer = optim.Adagrad(
            self.nn_model.parameters(),
            lr=self.learning_rate_init,
            weight_decay=self.alpha,
        )
    elif self.solver == "adam":
        optimizer = optim.Adam(
            self.nn_model.parameters(),
            lr=self.learning_rate_init,
            weight_decay=self.alpha,
        )
    else:
        raise NotImplementedError("`solver` must be one of 'adam' or 'adagrad'")

    # 期待報酬の推定モデル \hat{q}(x,a) を構築
    if self.off_policy_objective == "ips":
        q_x_a_hat = np.zeros((reward.shape[0], n_actions))
    elif self.off_policy_objective == "dr":
        q_x_a_hat = estimate_q_x_a_via_regression(bandit_feedback_train)
    else:
        raise NotImplementedError

    training_data_loader = self._create_train_data_for_opl(
        context,
        action,
        reward,
        pscore,
        q_x_a_hat,
        pi_b,
    )
    action_context_tensor = torch.from_numpy(action_context).float()

    # start policy training
    q_x_a_train = bandit_feedback_train["expected_reward"]
    q_x_a_test = bandit_feedback_test["expected_reward"]
    for _ in range(self.max_iter):
        # 各エポックの最初に、学習データとテストデータに対する真の方策性能を計算
        pi_train = self.predict_proba(
            context=context, action_context=action_context
        ).squeeze(-1)
        self.train_values.append((q_x_a_train * pi_train).sum(1).mean())
        pi_test = self.predict_proba(
            context=bandit_feedback_test["context"],
            action_context=bandit_feedback_test["action_context"],
        ).squeeze(-1)
        self.test_values.append((q_x_a_test * pi_test).sum(1).mean())

        loss_epoch = 0.0
        self.nn_model.train()
        for x, a, r, p, q_x_a_hat_, pi_b_ in training_data_loader:
            optimizer.zero_grad()
            # 新方策の行動選択確率分布\pi(a|x)を計算
            pi = self._predict_proba_as_tensor(
                x, action_context_tensor
            )  # pi=(batch_size, n_actions)

            # 方策勾配の推定値を計算 (方策性能を最大化したいのでマイナスをかけてlossとする)
            loss = -self._estimate_policy_gradient(
                action=a,
                reward=r,
                pscore=p,
                q_x_a_hat=q_x_a_hat_,
                pi_0=pi_b_,
                pi=pi,
            ).mean()
            # lossを最小化するようにモデルパラメータを更新
            loss.backward()
            optimizer.step()
            loss_epoch += loss.item()

        self.train_losses.append(loss_epoch)

    # 学習完了後に、学習データとテストデータに対する真の方策性能を計算
    pi_train = self.predict_proba(
        context=context, action_context=action_context
    ).squeeze(-1)
    self.train_values.append((q_x_a_train * pi_train).sum(1).mean())
    pi_test = self.predict_proba(
        context=bandit_feedback_test["context"],
        action_context=bandit_feedback_test["action_context"],
    ).squeeze(-1)
    self.test_values.append((q_x_a_test * pi_test).sum(1).mean())

def _create_train_data_for_opl(
    self,
    context: np.ndarray,
    action: np.ndarray,
    reward: np.ndarray,
    pscore: np.ndarray,
    q_x_a_hat: np.ndarray,
    pi_0: np.ndarray,
    **kwargs,
) -> torch.utils.data.DataLoader:
    """学習データを作成するメソッド
    Args:
        context (np.ndarray): コンテキスト特徴量の配列 (n_rounds, dim_context_features)
        action (np.ndarray): 選択されたアクションの配列 (n_rounds,)
        reward (np.ndarray): 観測された報酬の配列 (n_rounds,)
        pscore (np.ndarray): 傾向スコアの配列 (n_rounds,)
        q_x_a_hat (np.ndarray): 期待報酬の推定値の配列 (n_rounds, n_actions)
        pi_0 (np.ndarray): データ収集方策の行動選択確率の配列 (n_rounds, n_actions)
    """
    dataset = NNPolicyDataset(
        torch.from_numpy(context).float(),
        torch.from_numpy(action).long(),
        torch.from_numpy(reward).float(),
        torch.from_numpy(pscore).float(),
        torch.from_numpy(q_x_a_hat).float(),
        torch.from_numpy(pi_0).float(),
    )

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=self.batch_size,
    )
    return data_loader

def _estimate_policy_gradient(
    self,
    action: torch.Tensor,  # shape: (batch_size,)
    reward: torch.Tensor,  # shape: (batch_size,)
    pscore: torch.Tensor,  # shape: (batch_size,)
    q_x_a_hat: torch.Tensor,  # shape: (batch_size, n_actions)
    pi: torch.Tensor,  # shape: (batch_size, n_actions, 1)
    pi_0: torch.Tensor,  # shape: (batch_size, n_actions)
) -> torch.Tensor:  # shape: (batch_size,)
    """
    方策勾配の推定値を計算するメソッド
    Args:
        action (torch.Tensor): 選択されたアクションのテンソル (batch_size,)
        reward (torch.Tensor): 観測された報酬のテンソル (batch_size,)
        pscore (torch.Tensor): 傾向スコアのテンソル (batch_size,)
        q_x_a_hat (torch.Tensor): 期待報酬の推定値のテンソル (batch_size, n_actions)
        pi (torch.Tensor): 現在の方策による行動選択確率のテンソル (batch_size, n_actions, 1)
        pi_0 (torch.Tensor): 収集した方策による行動選択確率のテンソル (batch_size, n_actions)
    Returns:
        torch.Tensor: 方策勾配の推定値のテンソル (batch_size,)
            ただし勾配計算自体はPyTorchの自動微分機能により行われるので、
            ここで返される値は 方策勾配の推定量の \nabla_{\theta} を除いた部分のみ
    """
    current_pi = pi.detach()
    log_prob = torch.log(pi + self.log_eps)
    idx_tensor = torch.arange(action.shape[0], dtype=torch.long)

    q_x_a_hat_factual = q_x_a_hat[idx_tensor, action]
    iw = current_pi[idx_tensor, action] / pscore
    estimated_policy_grad_arr = iw * (reward - q_x_a_hat_factual)
    estimated_policy_grad_arr *= log_prob[idx_tensor, action]
    estimated_policy_grad_arr += torch.sum(q_x_a_hat * current_pi * log_prob, dim=1)

    return estimated_policy_grad_arr

@dataclass
class NNPolicyDataset(torch.utils.data.Dataset):
    """Two-Towerモデルのオフ方策学習用のデータセットクラス"""

    context: np.ndarray  # 文脈x_i
    action: np.ndarray  # 行動a_i
    reward: np.ndarray  # 報酬r_i
    pscore: np.ndarray  # 傾向スコア \pi_0(a_i|x_i)
    q_x_a_hat: np.ndarray  # 期待報酬の推定値 \hat{q}(x_i, a)
    pi_0: np.ndarray  # データ収集方策の行動選択確率分布 \pi_0(a|x_i)

    def __post_init__(self):
        """initialize class"""
        assert (
            self.context.shape[0]
            == self.action.shape[0]
            == self.reward.shape[0]
            == self.pscore.shape[0]
            == self.q_x_a_hat.shape[0]
            == self.pi_0.shape[0]
        )

    def __getitem__(self, index):
        return (
            self.context[index],
            self.action[index],
            self.reward[index],
            self.pscore[index],
            self.q_x_a_hat[index],
            self.pi_0[index],
        )

    def __len__(self):
        return self.context.shape[0]

def estimate_q_x_a_via_regression(
    bandit_feedback_train: BanditFeedbackDict,
    q_x_a_model=MLPRegressor(hidden_layer_sizes=(10, 10, 10), random_state=12345),
) -> np.ndarray:
    """DR推定量に使用する、期待報酬関数の予測モデル \hat{q}(x,a) を学習する関数
    Args:
        bandit_feedback_train (BanditFeedbackDict): 学習データ
        q_x_a_model (MLPRegressor, optional): 期待報酬関数の予測モデルのアーキテクチャ.
            Defaults to MLPRegressor(hidden_layer_sizes=(10, 10, 10), random_state=12345).
    Returns:
        np.ndarray: 各学習データに対する各アクションの期待報酬の予測値 \hat{q}(x,a) (shape: (n_rounds, n_actions))
    """
    n_data, n_actions = (
        bandit_feedback_train["n_rounds"],
        bandit_feedback_train["n_actions"],
    )
    x, r = bandit_feedback_train["context"], bandit_feedback_train["reward"]
    actions, a_feat = (
        bandit_feedback_train["action"],
        bandit_feedback_train["action_context"],
    )
    x_a = np.concatenate([x, a_feat[actions]], axis=1)

    # 学習データに対して、期待報酬関数の予測モデル \hat{q}(x,a) を学習
    q_x_a_model.fit(x_a, r)

    # 学習した \hat{q}(x,a) を用いて、学習データに対する各アクションの期待報酬の予測値を計算
    q_x_a_hat = np.zeros((n_data, n_actions))
    for a_idx in range(n_actions):
        x_a = np.concatenate([x, np.tile(a_feat[a_idx], (n_data, 1))], axis=1)
        q_x_a_hat[:, a_idx] = q_x_a_model.predict(x_a)

    return q_x_a_hat      
```

一方で、回帰ベースアプローチのprivateな学習メソッド。

```python
def _fit_by_regression_based_approach(
    self,
    bandit_feedback_train: BanditFeedbackDict,
    bandit_feedback_test: Optional[BanditFeedbackDict] = None,
) -> None:
    """Two-Towerモデルに基づく推薦方策を、回帰ベースアプローチで学習するメソッド。
    ここでは、報酬rの予測問題としてクロスエントロピー誤差を最小化するように学習を行う。
    Args:
        bandit_feedback_train (BanditFeedbackDict): 学習用のバンディットフィードバックデータ
        bandit_feedback_test (Optional[BanditFeedbackDict]): テスト用のバンディットフィードバックデータ
    """
    n_actions = bandit_feedback_train["n_actions"]
    context, action, reward, action_context, pscore, pi_b = (
        bandit_feedback_train["context"],
        bandit_feedback_train["action"],
        bandit_feedback_train["reward"],
        bandit_feedback_train["action_context"],
        bandit_feedback_train["pscore"],
        bandit_feedback_train["pi_b"],
    )

    # optimizerの設定
    if self.solver == "adagrad":
        optimizer = optim.Adagrad(
            self.nn_model.parameters(),
            lr=self.learning_rate_init,
            weight_decay=self.alpha,
        )
    elif self.solver == "adam":
        optimizer = optim.Adam(
            self.nn_model.parameters(),
            lr=self.learning_rate_init,
            weight_decay=self.alpha,
        )
    else:
        raise NotImplementedError("`solver` must be one of 'adam' or 'adagrad'")

    training_data_loader = self._create_train_data_for_opl(
        context,
        action,
        reward,
        pscore,
        np.zeros((reward.shape[0], n_actions)),  # 回帰ベースでは不要
        pi_b,
    )
    action_context_tensor = torch.from_numpy(action_context).float()

    # start policy training
    q_x_a_train = bandit_feedback_train["expected_reward"]
    q_x_a_test = bandit_feedback_test["expected_reward"]
    for _ in range(self.max_iter):
        # 各エポックの最初に、学習データとテストデータに対する真の方策性能を計算
        pi_train = self.predict_proba(
            context=context, action_context=action_context
        ).squeeze(-1)
        self.train_values.append((q_x_a_train * pi_train).sum(1).mean())
        pi_test = self.predict_proba(
            context=bandit_feedback_test["context"],
            action_context=bandit_feedback_test["action_context"],
        ).squeeze(-1)
        self.test_values.append((q_x_a_test * pi_test).sum(1).mean())

        loss_epoch = 0.0
        self.nn_model.train()
        for x, a, r, p, q_x_a_hat_, pi_b_ in training_data_loader:
            optimizer.zero_grad()
            # 各バッチに対するTwo-Towerモデルの出力を \hat{q}(x,a) とみなす
            context_embedding = self.nn_model["context_tower"](x)
            action_embedding = self.nn_model["action_tower"](action_context_tensor)
            logits = torch.matmul(context_embedding, action_embedding.T)
            q_x_a_hat_by_two_tower = torch.sigmoid(logits)

            # 選択されたアクションに対応する\hat{q}(x,a)を取得
            selected_action_idx_tensor = torch.arange(a.shape[0], dtype=torch.long)
            q_x_a_hat_by_two_tower_of_selected_action = q_x_a_hat_by_two_tower[
                selected_action_idx_tensor,
                a,
            ]

            # 期待報酬の推定値 \hat{q}(x,a) と報酬rとのクロスエントロピー誤差を損失関数とする
            loss = torch.nn.functional.binary_cross_entropy(
                q_x_a_hat_by_two_tower_of_selected_action, r
            ).mean()

            # lossを最小化するようにモデルパラメータを更新
            loss.backward()
            optimizer.step()
            loss_epoch += loss.item()

        self.train_losses.append(loss_epoch)

    # 学習完了後に、学習データとテストデータに対する真の方策性能を計算
    pi_train = self.predict_proba(
        context=context, action_context=action_context
    ).squeeze(-1)
    self.train_values.append((q_x_a_train * pi_train).sum(1).mean())
    pi_test = self.predict_proba(
        context=bandit_feedback_test["context"],
        action_context=bandit_feedback_test["action_context"],
    ).squeeze(-1)
    self.test_values.append((q_x_a_test * pi_test).sum(1).mean())
```

以上で、Two-Towerモデルに基づく推薦方策を勾配ベースのオフ方策学習で最適化するためのクラスを実装しました...!
