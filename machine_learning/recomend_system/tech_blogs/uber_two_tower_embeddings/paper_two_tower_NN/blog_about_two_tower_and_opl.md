# タイトル: 「反実仮想機械学習」を参考に、推薦タスクの実務でよく使われてるtwo-towerモデルを勾配ベースのオフ方策学習で最適化したいんだー！

## ブログ構成案

- 3行まとめ
- はじめに: 本ブログを書く意味付け
- two-towerモデルはこんな感じの雰囲気
- 勾配ベースのオフ方策学習はこんな感じの雰囲気
- two-towerモデルを勾配ベースのオフ方策学習するための作戦をまとめる
- pytorchでいざ実装!
- open bandit pipelineパッケージの合成データを使って、性能を評価してみる。
- おわりに

# 以下、本文

## はじめに: 本ブログを書く意味付け

## two-towerモデルはこんな感じの雰囲気

- two-towerモデルとは?
  - 推薦システムや検索タスクなどでよく使われる、**深層学習ベースのモデルの一つ**。
  - 特に**大規模なコーパス (数百万~数億規模のアイテム)から関連アイテムを高速に取得するretreivalフェーズ**に強みを持つ。
    - 2-stages推薦でいうところの1ステージ目「retrieval」の部分を担当するモデルとして使われることが多い印象。2ステージ目の「reranking」の部分は別のリッチなモデルが使われたりするイメージ...!:thinking:
- 構造上の特徴
  - **2つの encoder (i.e. tower)** から構成されるモデル。
    - (ちなみにNLP分野では「**デュアルエンコーダ(dual encoder)**」と呼ばれているらしい...!:thinking:)
  - 1つ目の encoder (ユーザタワー, クエリタワーとか呼ばれる) : クエリ(ユーザ情報やコンテキスト)を入力として受け取り、埋め込みに変換。
  - 2つ目の encoder (アイテムタワーとか呼ばれる) : 推薦や検索の候補となるアイテム(商品、ニュース記事、etc.)を入力として受け取り、埋め込みに変換。
  - two-towerモデルは**クエリとアイテムを共通の埋め込み空間**にマッピングする。推論時はその埋め込み空間上で内積で類似度を計算 -> 上位K個のアイテムを取得することで推薦や検索を行う。
- two-towerモデルの利点
  - スケーラブルで高速:
    - 大規模なデータセットでも高速に推論できる (事前にアイテム埋め込みをインデックス化し、近傍探索でretreiveできる)
    - **推論時(検索時)の計算コストが低い (クエリの埋め込みを計算 -> 事前計算されたアイテム埋め込みと内積計算するだけ)**
  - 特徴量の柔軟な活用
    - 任意のユーザやアイテムの特徴量を多層NNで非線形変換して埋め込みを作るので、**特徴量エンジニアリングの自由度が高い**
      - 画像特徴量、NLP的な特徴量なども組み込みやすい。
      - 扱いたい特徴量に応じて各towerの構造も柔軟にアレンジできる。ニュース推薦の分野ではアイテムタワー内部にAttention機構を採用したりしてた...!:thinking:
    - また純粋な行動履歴ベースの行列分解(Matrix Factorization)モデルよりも、アイテムやユーザの特徴量を柔軟に組み込めるので、コールドスタートアイテム、コールドスタートユーザに対応しやすい。
- 参考資料:
  - [Deep Neural Networks for YouTube Recommendations]()
    - 2016年のYoutubeの動画推薦システムについて紹介してる論文。
    - DNNを使った2-stages推薦を採用しており、candidate retrieve用のモデルも candidate ranking用のモデルもtwo-towerモデルを採用してた。
    - 「two-towerモデルを提案!」という内容ではなく、「Youtubeの推薦の困難さをこういう工夫で対処してますよ!」的なtipsを紹介してくれてる様な印象の論文:thinking:
  - [Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations]()
    - 2020年のGoogle Playの推薦システムを取り扱った論文。こちらは主に2-stages推薦の1ステージ目candidate retrieveのモデルとしてtwo-towerモデルを採用してた。論文のメイントピックは、two-towerモデル学習時のバイアス問題に対処するためのネガティブサンプリング方法について。
  - [Innovative Recommendation Applications Using Two Tower Embeddings at Uber](https://www.uber.com/en-JP/blog/innovative-recommendation-applications-using-two-tower-embeddings/)
    - こちらは論文ではないが、Uberさんのテックブログでtwo-towerモデルを使った推薦システムの応用事例が紹介されてた。
    - ちなみに自分はこのブログを読んでtwo-towerアーキテクチャを知り、一つ目の論文に辿り着きました!感謝...!:pray:
  - [Two-Towerモデルと近似最近傍探索による候補生成ロジックの導入](https://blog.recruit.co.jp/data/articles/two-tower-model/)
    - リクルートさんのテックブログ。
    - ちなみに自分はこのブログから、二つ目の論文に辿り着きました!感謝...!:pray:

## 勾配ベースのオフ方策学習はこんな感じの雰囲気

- そもそもオフ方策学習 (Off-policy learning, OPL) とは??
  - ログデータを使って、新しい方策(policy)を学習する手法。
  - ex. 既存の推薦システムが「ニュース記事A」を50%、「ニュース記事B」を30%の確率で推薦しているとする。
    - その推薦結果とユーザから得られた報酬（ex. クリックしたか否か）を記録し、そのログデータ(i.e. バンディットフィードバック)を使って、より良い (ex. 累積報酬の期待値を最大化する, etc.) 推薦方策を学習する。

- OPLの基本的な2種類のアプローチ:
  - OPLには、2つの基本的なアプローチとして、回帰ベースと勾配ベースの2つがある。
    -  (両者を混ぜたようなアプローチなども近年はあるみたい)
  - 1. 回帰ベース(Regression-based)
    - 従来の教師あり機械学習っぽいアプローチ。
    - 各アクションの報酬期待値 $E_{p(r|x,a)}[r] = q(x,a)$ を推定するモデル $\hat{q}(a,x)$ を学習し、予測関数 $\hat{q}(a,x)$ の出力値を直接使って意思決定を行う!
      - 例: hogehgoe
    - (すなわち、CTR予測モデルなど、教師あり学習を使った推薦モデルのアプローチの多くは、ほぼほぼ回帰ベースのアプローチに分類できそう...!!:thinking:)
  - 2. 勾配ベース(Gradient-based)
    - 事前に定義した方策性能 (policy value) $V(\pi_{\theta})$ が高くなるように、方策のパラメータ $\theta$ を最適化する方法。
    - 以下のようなパラメータ更新則で方策のパラメータを更新していくというのが、勾配ベースアプローチの基本的なアイデア。
      - $\theta_{t+1} \leftarrow \theta_{t} + \nu \nabla_{\theta} V(\pi_{\theta})$
      - ここで、$\nu$ は学習率。$\nabla_{\theta} V(\pi_{\theta})$ は方策性能の勾配 (方策勾配、policy gradient)。
    - ただし、真の方策性能 $V(\pi_{\theta})$ は未知であるため、その**方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ も当然未知**になる。
    - -> そこで勾配ベースのオフ方策学習では、**何らかの方法で方策勾配を推定して、その推定値を使って方策のパラメータを更新していく!**（仕方なく！本当は真の方策勾配でパラメータ更新をしたいが...!!）
      - ex. オフ方策評価(OPE, Off-policy evaluation)でも出てくるIPS推定量, DR推定量などを使う

- 方策性能(Policy value)と、その方策勾配(Policy gradient)の関係
  - 例えば、任意の方策 $\pi_{\theta}$ に対して、その性能を以下のように定義する場合を考える
    - （意味合いは「ある環境 $p(x)$ において、方策 $\pi_{\theta}$ を稼働させて行動を選択した場合に得られる報酬の期待値」みたいなイメージ...! オフ方策評価でもよく使われてる印象...! :thinking:）
    - $V(\pi_{\theta}) = E_{p(x) \pi_{\theta}(a|x) p(r|x,a)}[r] = E_{p(x)\pi_{\theta}(a|x)}[q(x, a)]$
  - この場合、方策性能に対するモデルパラメータ $\theta$ の勾配、すなわち方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ は以下のように表現できる。
    - (要するに、勾配の式に方策性能の定義を代入しただけ!)
    - $\nabla_{\theta} V(\pi_{\theta}) = \nabla_{\theta} E_{p(x)\pi_{\theta}(a|x)}[q(x, a)]$
  - 上記の方策勾配の定義の右辺を式変形していくといくと、最終的に以下のようになる!
    - $\nabla_{\theta} V(\pi_{\theta}) = E_{p(x)\pi_{\theta}(a|x)}[q(x, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]$
    - (元の定義式に対して、「期待値の勾配」=「勾配の期待値」の性質だったり、「同時分布の期待値」=「条件付き期待値の期待値」の性質だったり、ログトリック(条件付き確率の勾配の変形)を使ったり、...などなどしていい感じに式変形していく...!)
  - この真の方策勾配の式を元に、IPS推定量だったりDR推定量だったりを駆使して、いい感じの推定量を作って、方策のモデルパラメータをいい感じに更新していく！というのが勾配ベースのオフ方策学習の基本的な流れ...!:thinking:
    - よって実務上のパラメータ更新則は以下になる (方策勾配に推定値を表すhatがついてる点が違い!)
    - $\theta_{t+1} <- \theta_{t} + \nu \hat{\nabla_{\theta}} V(\pi_{\theta})$

- 方策勾配の代表的な推定方法1: IPS推定量
  - オフ方策評価でも王道アプローチ的な立ち位置にある「IPS推定量」の考え方を応用して、方策勾配を推定することを考える。
    - あるデータ収集方策 $\pi_{0}$ によって収集されたログデータ $D$ が与えられた時、真の方策勾配に対するIPS推定量は以下のようになる。

$$
\hat{\nabla_{\theta} V_{IPS}(\pi_{\theta};D)} := \frac{1}{n} \sum_{i=1}^{n} w(x_i, a_i) r_i \nabla_{\theta} \log \pi_{\theta}(a_i|x_i)
\tag{5.12}
$$

- なお式中の $w(x, a):= \pi_{\theta}(a|x) / \pi_{0}(a|x)$ は、学習中の方策とデータ収集方策による行動選択確率の比であり、重要度重みと呼ぶ。
- オフ方策評価におけるIPS推定量との対応関係:
  - オフ方策評価のIPS推定量: $\hat{V}_{IPS}(\pi_{\theta};D) := \frac{1}{n} \sum_{i=1}^{n} w(x_i, a_i) r_i$
  - オフ方策学習だと、推定目標が評価方策の性能 $V(\pi)$ から方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ に変わる。
  - -> なので、それに応じて報酬 $r_i$ だけじゃなく、**学習中の方策による行動選択確率の対数の勾配 $\nabla_{\theta} \log \pi_{\theta}(a_i|x_i)$ が推定量の定義に含まれるようになった**のが些細な違い!

- 方策勾配の代表的な推定方法2: DR推定量
  - オフ方策評価と同様、IPS推定量の問題: 重要度重みに起因して発生するバリアンス!
  - IPS推定量の不偏性を維持しつつバリアンスを減少させる方法 -> メジャーなのがDR推定量!!
  - データ収集方策 $\pi_{0}$ によって収集されたログデータ $D$ が与えられた時、真の方策勾配に対するDR推定量は以下のようになる。

$$
\hat{\nabla_{\theta} V_{DR}(\pi_{\theta};D)} := \frac{1}{n} \sum_{i=1}^{n} 
% \left\{
\Big\{
  w(x_i, a_i) (r_i - \hat{q}(x_i, a_i)) \nabla_{\theta} \log \pi_{\theta}(a_i|x_i) 
  \\
  + E_{\pi_{\theta}(a|x)}[\hat{q}(x_i, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]
\Big\}
$$

- なお式中の...
  -  $\hat{q}(x, a)$ は、期待報酬関数 $q(x, a)$ に対する推定モデル!
     - 例えば回帰ベースのアプローチと同様に、ログデータ $D$ を用いて損失関数を最小化して求めたモデルを使ったりする!
  - $w(x, a)$ はIPS推定量と同様の重要度重み!
- オフ方策評価におけるDR推定量との対応関係
  - 基本的には同様のアイデア!
    - 「ログデータを用いて事前に学習しておいた期待報酬関数に対する推定モデル $\hat{q}(x, a)$ をベースラインとして使うことで、**IPS推定量からのバリアンス減少を狙う！**」

## two-towerモデルを勾配ベースのオフ方策学習するための作戦をまとめる

- 前述の「two-towerモデルはこんな感じの雰囲気」セクションで共有した参考文献の論文内では、基本的には回帰ベースのアプローチでtwo-towerモデルに基づく推薦方策を学習していた印象。
  - Youtubeの論文もGoogle Playの論文でも、どちらも「推薦してクリックされたか否か」などの報酬ログ $r$ を正例/負例の教師ラベルとして、期待報酬 $q(x, a)$ を予測するモデルを学習してた印象。(負例の作り方や報酬 $r$ の定義は様々だった:thinking:)
- 今回、two-towerモデルに基づく推薦方策を、回帰ベースではなく勾配ベースのオフ方策学習で最適化することを考える!
  - まずtwo-towerモデルを使った推薦方策を定義するぞ...!
    - まずtwo-towerモデルの学習可能な全パラメータを $\theta$ で表す。
    - この場合、このtwo-towerモデルに基づく推薦方策を $\pi_{\theta}$ と表す。
    - その推薦方策の行動選択の確率分布は $\pi_{\theta}(a|x) = p(a|x, \theta)$ と表現できそう。 
      - i.e. コンテキスト(ユーザ特徴量, アイテム特徴量) $x$ とtwo-towerモデルのパラメータ $\theta$ で条件付けられた、アイテム $a$ を推薦する条件付き確率...!:thinking:
  - 次にこの $\pi_{\theta}(a|x)$ を、**two-towerモデルの出力値を使ってどんな確率質量関数として表現するか**...!:thinking:
    - パラメータ $\theta$ を持つtwo-towerモデルに対して、各コンテキスト(ユーザ特徴量) $x$ と推薦候補アイテム $a$ (実際に入力されるのはアイテム特徴量!) を入力した時の最終的な出力値 (=ユーザ埋め込みとアイテム埋め込みの内積値) を $TwoTowerModel_{\theta}(x, a)$ と表現してみる。
    - **確率質量関数の定義を満たす必要があるので、とりあえずソフトマックス関数を使うぞ!**
      - ちなみに満たしたい確率質量関数の定義は以下!
        - 1. 非負性: $\pi_{\theta}(a|x) \geq 0,  \forall a \in A$: つまり、推薦可能なすべてのアイテムについての確率質量が非負であること。
        - 2. 正規化条件: $\sum_{a \in A} \pi_{\theta}(a|x) = 1$: つまり、推薦可能なすべてのアイテムについての確率質量の総和が1であること。
      - ソフトマックス関数: $softmax(a) = \frac{\exp(a/\tau)}{\sum_{a' \in A} \exp(a'/\tau)}$ 
        - ここで $\tau$ は温度パラメータ。大きい値を設定するほど各値の差が小さくなり、小さい値を設定するほど各値の差が大きくなる。
    - 以上より、two-towerモデルに基づく推薦方策 $\pi_{\theta}(a|x)$ は以下のように表現できそう!
      - $\pi_{\theta}(a|x) = \text{softmax}(TwoTowerModel_{\theta}(x, a)) = \frac{\exp(TwoTowerModel_{\theta}(x, a) / \tau)}{\sum_{a' \in A} \exp(TwoTowerModel_{\theta}(x, a') / \tau)}$
  - 次に、推薦方策の性能を定義するぞ!
    - ここは特に何も考えず、一般的な方策性能(policy value)の定義である「期待報酬の期待値」をそのまま使うことにする...!つまり以下:
      - $V(\pi_{\theta}) = E_{p(x) \pi_{\theta}(a|x) p(r|x,a)}[r] = E_{p(x)\pi_{\theta}(a|x)}[q(x, a)]$
  - 次に、の方策勾配 $\nabla_{\theta} V(\pi_{\theta})$ を定義するぞ!
    - ここは先ほどの「勾配ベースのオフ方策学習はこんな感じの雰困」セクションで共有した方策勾配の定義式に、方策性能の定義を代入すれば良いので...!:thinking:
    -  $\nabla_{\theta} V(\pi_{\theta}) = E_{p(x)\pi_{\theta}(a|x)}[q(x, a) \nabla_{\theta} \log \pi_{\theta}(a|x)]$
    - ちなみに方策勾配の意味合いは以下のような感じ:
      - 「パラメータ $\theta$ に対する 関数 $V(\pi_{\theta})$ の勾配(微分)」
      - = 「推薦方策のパラメータ(i.e. two-towerモデルのパラメータ) $\theta$ を変化させた時の、方策性能 $V(\pi_{\theta})$ の変化率」
  - ただし実際には、真の方策性能も真の方策勾配も未知なので、推定量を使うぞ...!!
    - より具体的には、任意のデータ収集方策 $\pi_{0}(a|x)$ で収集したログデータ $D = \{(x_i, a_i, r_i)\}_{i=1}^{n}$ に対して、なんらかの推定量を使って方策勾配を推定する...!
    - とりあえず今回は、IPS推定量とDR推定量を使うぞ!
      - 両推定量の定義式は「勾配ベースのオフ方策学習はこんな感じの雰困」セクションで共有したやつをそのまま使う!

## open bandit pipelineパッケージの合成データを使って、性能を評価してみる(実装は最後のセクションに書いてます)



## pytorchでこう実装しました!

ここでは、two-towerモデルに基づく推薦方策クラスを実装してます。
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
    """two-towerモデルに基づく推薦方策を、回帰ベースアプローチで学習するメソッド。
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
            # 各バッチに対するtwo-towerモデルの出力を \hat{q}(x,a) とみなす
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

以上で、two-towerモデルに基づく推薦方策を勾配ベースのオフ方策学習で最適化するためのクラスを実装しました...!
