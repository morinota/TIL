## 0.1. link

- https://dl.acm.org/doi/pdf/10.1145/3460231.3474236 httpsを使用しています。

## 0.2. title タイトル

Values of User Exploration in Recommender Systems
リコメンダーシステムにおけるユーザー探索の価値

## 0.3. abstract アブストラクト

Reinforcement Learning (RL) has been sought after to bring next-generation recommender systems to further improve user experience on recommendation platforms.
強化学習（Renforcement Learning: RL）は、推薦プラットフォームにおけるユーザ体験をさらに向上させる次世代推薦システムを実現するために求められている.
While the exploration-exploitation tradeoff is the foundation of RL research, the value of exploration in (RL-based) recommender systems is less well understood.
探索と利用のトレードオフはRL研究の基礎であるが、（RLに基づく）推薦システムにおける探索の価値についてはあまり理解されていない.
Exploration, commonly seen as a tool to reduce model uncertainty in regions of sparse user interaction
探索は、一般に、**ユーザとのインタラクションが疎な領域でモデルの不確実性を低減するためのツール**とみなされている.

We examine the role of user exploration in changing different facets of recommendation quality that more directly impact user experience.
我々は、ユーザーエクスペリエンスに直接影響を与える推薦品質の様々な側面を変化させるユーザー探索の役割を検証する.
To do so, we introduce a series of methods inspired by exploration research in RL to increase user exploration in an RL-based recommender system, and study their effect on the end recommendation quality, more specifically, on accuracy, diversity, novelty and serendipity.
そのために、RLにおける探索研究にヒントを得て、RLベースの推薦システムにおいてユーザの探索を増加させる一連の方法を導入し、最終的な推薦品質、より具体的には精度、多様性、新規性、セレンディピティに対するそれらの効果を研究する.
We propose a set of metrics to measure (RL based) recommender systems in these four aspects and evaluate the impact of exploration-induced methods against these metrics.
我々は、これらの4つの側面において（RLベースの）推薦システムを測定するための一連のメトリクスを提案し、これらのメトリクスに対して、探索を誘発する手法の影響を評価する.
In addition to the offline measurements, we conduct live experiments on an industrial recommendation platform serving billions of users to showcase the benefit of user exploration.
オフラインでの測定に加え、我々はユーザ探索の利点を紹介するために、数十億のユーザにサービスを提供する産業用推薦プラットフォームでライブ実験を行う.
Moreover, we use conversion of casual users to core users as an indicator of the holistic long-term user experience and study the values of user exploration in helping platforms convert users.
さらに、カジュアルユーザからコアユーザへの転換を、長期的なユーザ体験の全体像の指標として用い、プラットフォームがユーザーの転換を支援する際のユーザー探索の価値を研究している.
Through offline analyses and live experiments, we study the correlation between these four facets of recommendation quality and long term user experience, and connect serendipity to improved long term user experience.
オフライン分析とライブ実験を通じて、これら推薦品質の4つの側面と長期的なユーザ体験の相関関係を研究し、セレンディピティと長期的なユーザー体験の向上を結びつけています.

# 1. Introduction はじめに

In the era of increasing choices, recommender systems are becoming indispensable in helping users navigate the million or billion pieces of contents available on recommendation platforms.
選択肢の増えた現代において、推薦システム（Recommendender System）は、ユーザーが推薦プラットフォーム上で100万、10億のコンテンツをナビゲートするために必要不可欠なものとなってきている.
These systems are built to satisfy users’ information needs by anticipating what they would be interested in consuming next.
これらのシステムは，**ユーザが次に何を消費することに興味があるかを予測**し，**ユーザの情報ニーズを満たす**ために構築されている.
Collaborative filtering [28, 47] and supervised learning based approaches predicting users’ immediate response toward recommendations [12, 65] such as clicks, dwell time, likes, have had enormous successes.
協調フィルタリング[28, 47]と教師あり学習ベースのアプローチは、クリック、滞在時間、「いいね！」など、推薦に対するユーザーの即時反応を予測し、大きな成功を収めている[12, 65].
Researchers however are becoming increasingly aware of the limitations of such approaches.
しかし、研究者たちはこのようなアプローチの限界に気付きつつある.
First, focus on driving short-term engagements such as user clicks fails to account for the long term impact of a recommendation.
まず、ユーザのクリックなど短期的なエンゲージメントに焦点を当てると、レコメンデーションがもたらす長期的な影響(=feedback roopの事??)を考慮することができない.
Second, lack of exploration causes these systems to increasingly concentrate on the known user interests and create satiation effect, i.e., reduced enjoyment of the content.
第二に、探索の不足により、これらのシステムは**既知のユーザーの興味にますます集中**し、飽和効果、すなわちコンテンツの楽しみを減少させることになる.

Reinforcement learning (and bandits) techniques have emerged as appealing alternatives [11, 23, 67, 68] over the years.
強化学習（およびバンディット）技術は、長年にわたって魅力的な代替手段として浮上してきた[11, 23, 67, 68].
Compared with supervised learning based approaches, RL offers two advantages:
教師あり学習ベースのアプローチと比較すると、RLには2つの利点がある.

- 1. Exploration. 探索。
  - (Online) RL algorithms inherently explore regions they are less certain about. (オンライン）RLアルゴリズムは本質的に、確信の持てない領域を探索する。
  - This provides a natural mechanism to deviate from the current system behavior, and introduce previously unseen contents to users;
  - これは、現在のシステム動作から逸脱し、以前に見たことのないコンテンツをユーザーに紹介するための自然なメカニズムを提供する、2）長期的なユーザー体験の最適化。
- 2. Long-term user experience optimization. 長期的なユーザー体験の最適化：
  - As the planning horizon of these RL agents extends, the recommender naturally shifts its focus from short-term user engagement toward optimizing the long-term user experience on the platform.
  - RLエージェントのプランニングホライズンが長くなると、レコメンダーは短期的なユーザーエンゲージメントから、プラットフォームにおける長期的なユーザー体験の最適化へと自然にフォーカスを移していく.
  - We focus our discussion on exploration, though as we show in the analyses it innately connects to the long-term user experience.ここでは、探索に焦点を当てますが、分析で示すように、探索は長期的なユーザー体験と本質的に結びついている.

The tradeoff between exploration and exploitation is central to the design of RL agents [17, 57].
探査と開拓の間のトレードオフはRLエージェントの設計の中心である[17, 57].
An agent learns to form a policy to maximize returns in a changing environment by taking actions and receiving reward
エージェントは行動を起こし、報酬を受け取ることによって、変化する環境の中でリターンを最大化するための政策を形成するように学習する.

As exploration innately leads to recommending something less pertinent to the known user interests, it is often seen as a cost to user experience, especially in the short term.
しかし，**このような探索はユーザの興味にそぐわないものを推薦することになるため，特に短期的にはユーザ体験に対するコスト**とみなされることが多い.
Here we argue that recommender systems have an inherent need for exploration as users perceive other factors of recommendation quality besides accuracy [5, 66].
ここでは、**ユーザはaccuracy以外の推薦品質の要因を認識するため、推薦システムには本質的に探索の必要性があることを主張する**[5, 66].
We dissect the values of user exploration by examining its role in changing different aspects of recommendation quality that impact the user experience on recommendation platforms.
我々は、推薦プラットフォームにおけるユーザ体験に影響を与える推薦品質の様々な側面を変化させる役割を検証することで、ユーザー探索の価値を分解する.
Together, we make the following contributions:
併せて、以下の貢献を行う.

- Methods to Introduce User Exploration: We introduce a collection of methods, inspired by exploration research in RL, to improve user exploration in recommender systems. ユーザ探索を導入するためのメソッド RLにおける探索研究にヒントを得て、推薦システムにおけるユーザ探索を向上させるための手法群を紹介する.

- Metrics: We propose a set of metrics measuring the different aspects of recommendation quality, that is accuracy, diversity, novelty and serendipity for RL based recommender systems. メトリクス RLベースの推薦システムにおいて、推薦品質の異なる側面、すなわち、正確性、多様性、新規性、セレンディピティを測定する一連のメトリクスを提案する.

- Offline Analyses: We conduct an extensive set of offline analyses to understand the values of user exploration in changing the four aspects of recommendation quality. オフライン分析 レコメンデーション品質の4つの側面を変化させるユーザー探索の価値を理解するために、広範なオフライン分析を行っている.

- Live Experiments: We conduct live experiments of the proposed methods on a commercial recommendation platform serving billions of users and millions of items, and showcase the value of user exploration in improving long-term user experience on the platform. ライブ実験 数十億のユーザと数百万のアイテムを扱う商用推薦プラットフォームにおいて、提案手法のライブ実験を行い、プラットフォームにおける長期的なユーザ体験の向上におけるユーザ探索の価値を紹介する.

- Serendipity for Long Term User Experience: Through offline analyses and live experiments, we study the correlation between these four aspects of recommendation quality and the long term user experience. Using conversion of casual users to core users as an indicator of the holistic long term user experience, we connect serendipity to improved long term user experience. 長期的なユーザーエクスペリエンスのためのセレンディピティ: オフライン分析とライブ実験を通じて、これら4つのレコメンデーション品質と長期的なユーザ体験の相関を研究しています. カジュアルユーザからコアユーザへの転換率を指標とし、セレンディピティを長期的なユーザ体験の向上と結びつける.

# 2. Related Work 関連作品

## 2.1. Reinforcement Learning for Recommender Systems. 推薦システムのための強化学習.

Deep reinforcement learning, combining high-capacity function approximators, i.e., deep neural networks, with the mathematical formulations in classic reinforcement learning [57], has achieved enormous success in various domains such as games, robotics and hardware design [18, 33, 36, 52].
深層強化学習は、**高容量関数近似器である深層ニューラルネットワーク**と**古典的強化学習における数学的定式化**[57]を組み合わせ、ゲーム、ロボット工学、ハードウェア設計などの様々な領域で大きな成功を収めている[18, 33, 36, 52].
It has attracted a lot of attention from the recommeder system research community as well.
また、レコメンダーシステム研究コミュニティでも注目されている.
Shani et al. [51] were among the first to formally formulate recommendation as a Markov decision process (MDP) and experiment with model-based RL approaches for book recommendation.
Shani ら [51] は、**推薦を Markov 決定過程 (MDP) として公式に定式化**し、書籍推薦のためのモデルベース RL アプローチを実験した最初の研究者の一人である.
Zheng et al. [70] applied DQN for news recommendation.
Zheng ら [70] は DQN をニュース推薦に応用した.
Dulac-Arnold et al. [14] enabled RL in problem spaces with a large number of discrete actions and showcased its performance on various recommendation tasks with tens of thousands of actions.
Dulac-Arnoldら[14]は、離散的なアクションが多数存在する問題空間でのRLを可能にし、数万アクションの様々な推薦タスクでその性能を発揮した.
Liu et al. [34] tested actor-critic approaches on recommendation datasets such as MovieLens, Yahoo Music and Jester.
Liu ら[34]は，MovieLens, Yahoo Music, Jester などの推薦データセットに対して，行為者批評アプローチをテストしている.
Set recommendation using RL has been studied in [11, 23, 69].
また，RL を用いた集合推薦も [11, 23, 69] で研究されている.
In recent years, we also start seeing success of RL in real-world recommendation applications.
近年，実世界の推薦アプリケーションにおいても RL の成功が見られ始めている.
Chen et al. [11] scaled a batch RL algorithm, i.e., REINFORCE with off-policy correction to a commercial platform serving billions of users and tens of millions of contents.
Chen ら [11] はバッチ型 RL アルゴリズムである REINFORCE にオフポリシー補正を加え，数十億のユーザと数千万のコンテンツを扱う商用プラットフォームへ拡張した.
Hu et al. [22] tested an extension of the deep deterministic policy gradient (DDPG) method for learning to rank on Taobao, a commercial search platform.
Huら[22]は、商業的な検索プラットフォームであるTaobaoでのランク付けの学習のための深い決定論的政策勾配（DDPG）手法の拡張をテストした.

## 2.2. Exploration in Reinforcement Learning. 強化学習における探索

The exploration/exploitation dilemma has long been studied in multi-armed bandits and classic reinforcement learning [17, 57].
Exploration methods are concerned with reducing agents’ uncertainty of the environment reward and/or the dynamics.
For the stochastic bandits problems, Upper Confidence Bound (UCB) [30] and Thompson Sampling (TS) [4, 10, 59] are among the most well known techniques with both theoretical guarantees and empirical successes. In classic reinforcement learning with tabular settings, count-based exploration techniques quantifying the uncertainty based on the inverse square root of the state-action visit count, can be seen as extension of these techniques to Markov Decision Processes (MDPs). Tang et al. [58] further generalizes counted-based methods to deep RL with highdimensional state spaces. Another camp of methods, commonly referred to as intrinsic motivation [21, 24, 48, 56], encourages the agents to explore regions leading up to surprises. The surprise factor is often measured by the agents’ predictive errors on environment reward or dynamics, or equivalently information gain the agents can acquire by taking an action under the current state. Bellemare et al. [6] unifies count-based exploration and intrinsic motivation through the lens of information gain or learning progress. Our work takes inspiration from these existing works, and re-designs the algorithms to fit more closely with the recommendation setup.
探索/搾取のジレンマは多腕バンディットや古典的な強化学習で長い間研究されてきた[17, 57].
探索法は，エージェントの環境報酬やダイナミクスの不確実性を低減することに関係する.
確率的バンディット問題では、Upper Confidence Bound (UCB) [30] と Thompson Sampling (TS) [4, 10, 59] が理論的保証と経験的成功の両方を持つ最もよく知られた手法の一つである.
表形式設定による古典的な強化学習において、状態・行動訪問回数の逆平方根に基づいて不確実性を定量化するカウントベースの探索技術は、これらの技術のマルコフ決定過程（MDP）への拡張と見なすことができる.
Tangら[58]はさらに、カウントベースの手法を高次元の状態空間を持つ深いRLに一般化している.
また、一般に内発的動機付けと呼ばれる手法の別の陣営[21, 24, 48, 56]は、エージェントに驚きに至る領域を探索するように促す.
サプライズ要素は、しばしば、環境報酬やダイナミクスのエージェントの予測誤差、あるいは、現在の状態下で行動を起こすことによってエージェントが獲得できる情報利得によって測定される.
Bellemareら[6]は、情報利得あるいは学習進歩というレンズを通して、カウントベースの探索と内発的動機付けを統合している.
我々の研究は、これらの既存の研究からヒントを得て、より推薦の設定に近い形でアルゴリズムを再設計している.

## 2.3. Diversity, Novelty and Serendipity of Recommender Systems. レコメンダーシステムの多様性、新規性、セレンディピティ。

While early recommendation research has focused almost exclusively on improving recommendation accuracy, it has become increasingly recognized that there are other factors of recommendation quality contributing to the overall user experience on the platform.
初期のレコメンデーション研究では、レコメンデーション精度を向上させることのみに焦点が当てられていたが、**プラットフォーム上でのユーザ体験全体に貢献するレコメンデーション品質の他の要因が存在すること**が次第に認識されるようになってきました.
Herlocker et al. [19] in their seminal work of evaluating collaborative filtering based recommender systems defined various metrics to measure recommendation accuracy, coverage, novelty as well as serendipity.
**Herlocker ら [19] は協調フィルタリングベースのレコメンダーシステムを評価した代表的な研究で、レコメンデーション精度、カバレッジ、新規性、セレンディピティを測定するためのさまざまな指標を定義している**.
Diversity is another important aspect that has been extensively studied [3, 5].
多様性はもう一つの重要な側面であり、広く研究されている[3, 5].
Diversification algorithms are used to increase coverage of the full range of user interests, and to counter the saturation effect of consuming similar contents [72].
多様化アルゴリズムは，ユーザの興味・関心の全範囲のカバレッジを高め，類似コンテンツの消費による飽和効果に対抗するために使用される[72].
Zhou et al. [71] studied the dilemma between accuracy and diversity, and proposed a hybrid approach to balance the two.
Zhou ら [71]は，精度と多様性の間のジレンマを研究し，両者のバランスをとるためのハイブリッドなアプローチを提案している.
Novelty [8] is closely related to long tail recommendation [62], measuring the capacity of the recommender systems to make predictions and reach the full inventory of contents available on the platforms.
新規性(Novelty) [8] はロングテール推薦 [62]と密接に関連し，推薦システムが 予測を行い，プラットフォームで利用可能なコンテンツの完全 なインベントリに到達する能力を測定している.
One of the early definitions of serendipity was introduced in [19], which captures the degree to which a recommendation is both relevant and surprising to users.
セレンディピティの初期の定義の一つは[19]で紹介され，**推薦がユーザにとって関連性がありかつ意外である度合い**を捉えている.
Zhang et al. [66] proposed a hybrid rank-interpolation approach to combine outputs of three LDA algorithms [7] focusing on either accuracy, diversity or serendipity to achieve a balance between these factors in the end recommendations.
Zhang ら [66] は，精度，多様性，セレンディピティのいずれかに着目した 3 つの LDA アルゴリズム [7] の出力を結合し，最終的な推薦においてこれらの要素のバランスをとるハイブリッドランク補間アプローチを提案している.
Oku and Hattori [41] proposed a fusion based technique to mix items users expressed interest on based on item attributes in order to introduce serendipitous contents.
奥・服部[41]は、セレンディピティコンテンツを導入するために、ユーザが興味を示したアイテムをアイテムの属性に基づいて混合する融合技術を提案した.
Our work measures the effect of exploration on recommendation accuracy, diversity, novelty and serendipity, and connects these factors to long term user experience.
本研究では、**探索が推薦精度、多様性、新規性、セレンディピティに及ぼす影響を測定**し、これらの要因を長期的なユーザ体験に結びつける.

# 3. Background 背景

We base our work on the REINFORCE recommender system introduced in [11], in which the authors framed a set recommendation problem as a Markov Decision Process (MDP) (S, A, P, R, ρ0,γ ).
本論文では、[11] で紹介された REINFORCE 推薦システムをベースにしている. これは著者らが**集合推薦問題をマルコフ決定過程 (MDP) $(S, A, P, R, \rho_0,\gamma)$として定式化したもの**である.
Her, ここで、

- S is the state space capturing the user interests and context, S はユーザの興味とcontextを表す状態空間(state space)、
- A is the discrete action space containing items available for recommendation, A は推薦可能なアイテムを含む離散行動空間(discrete action space)、
- P : S × A × S → R is the state transition probability, P : S × A × S → R は状態遷移確率(state transition probability)、
- R : S × A → R is the reward function, R : S × A → R は報酬関数(reward function):
  - r(s, a) note the immediate reward of action a under state s. $r(s、a)$ は状態 s における行動 a の即時報酬(immediate reward)、
- ρ0 is the initial state distribution, $\rho_0$ は初期状態分布(initial state distribution)、
- γ the discount for future rewards. $\gamma$は将来の報酬(reward)に対する割引(discount)である.

Let $H_t = {(A_0, a_0,r_0), \cdots, (A_{t−1}, a_{t−1},r_{t−1})}$ denote an user’s historical activities on the platform up to time t, where ...
$H_t = {(A_0, a_0,r_0), \cdots, (A_{t−1}, a_{t−1},r_{t−1})}$は、**時間0 ~ 時間tまでのプラットフォーム上でのユーザのaction履歴**を表すとすると...

- $A_{t′}$ stands for the set of items recommended to the user at time t ′, $A_{t′}$は、時間$t′$でユーザに推薦されたアイテムの集合を表す.
- $a_{t′}$ denotes the item the user interacted with at t ′ (at ′ can be null), $a_{t′}$は、時間$t′$においてユーザがinteractしたアイテムを示し($a_{t′}$はnullでもよい)、
- and rt ′ captures the user feedback (reward) on at ′ (rt ′ = 0 if the user did not interact with any item in At ′). $r_{t′}$は、$a_{t′}$に対するユーザのフィードバック（報酬）を捕らえる(ユーザがAt ′のどのアイテムとも相互作用しなかった場合はrt ′＝0である).
- The history $H_t$ is encoded through a recurrent neural network to capture the latent user state, that is, ust = RNNθ (Ht ). 履歴$H_t$は、潜在的なユーザの状態を捕らえるために、**リカレントニューラルネットワークを通じて符号化(encode)される**、すなわち、$u_{st} = RNN_{θ} (H_t)$である.

Given the latent user state, a softmax policy over the item corpus A is parameterized as
潜在的なユーザの状態が与えられると、アイテムコーパスAに対するsoftmax policyは、以下のようにパラメータ化される. (=softmax関数を適用して得られる確率質量関数?? = **イメージとしては"ユーザ状態$s_t$で条件付けられた アイテムaをinteractする確率質量関数の値?パラメータがtheta**.")

$$
\pi_{\theta}(a|s_t) = \frac{exp(u_s^T, v_a)}{\sum_{a' \in A} \exp(u^T_s, v_{a'})}, \forall a \in A
\tag{1}
$$

which defines a distribution over the item corpus A conditioning on the user state st at time t. Here va stands for the embedding of the item a.
これは時間tでのuser state $s_t$を条件とする アイテムコーパス A の分布(=やっぱり確率変数 $\forall{a} \in A$ の確率質量分布...!)を定義している. ここで, $v_a$はアイテムaのembeddingを表す.
The agent then generates a set of recommendation At to user at time t according to the learned softmax policy πθ (· st ). The policy parameters θ are learned using REINFORCE [60] so as to maximize the expected cumulative reward over the user trajectories,
次にエージェントは，学習されたソフトマックスポリシー(=確率質量関数)$\pi_{\theta}(\cdot|s_t)$ に従って，時刻tにおけるユーザへの推薦アイテム集合$A_t$を生成する.
ポリシーパラメータ$\theta$はREINFORCE [60]を用いて、ユーザの軌跡(trajectories)に対する**期待累積報酬(expected cumulative reward)を最大化するように学習される**. (= 尤度最大化みたいな感じかな...?)

$$
\max_{\theta} J(\pi_{\theta}) = E_{s_0 \sim \rho_0, A_t \sim \pi_{\theta}(\cdot|s_t), s_{t+1} \sim P(s_t, A_t)}
[\sum_{\sum_{t=0}^{T}r(s_t, a_t)}]
\\
\eqsim E_{s_0 \sim d_{t}^{\pi_{\theta}}(s), a_t \sim \pi_{\theta}(\cdot|s_t)}
[R_{t}(s_t, a_t)]
\tag{2}
$$

where $R_t = I_{r(s_t, a_t)>0} \cdot \sum_{t'=t}^{T}{\gamma^{t′-t}r(s_{t′}, a_{t′})}$ is the discounted cumulative reward starting from time t.
ここで、$R_t = I_{r(s_t, a_t)>0} \cdot \sum_{t'=t}^{T}{\gamma^{t′-t}r(s_{t′}, a_{t′})}$ は時刻 t から始まる割引累積報酬(discounted cumulative reward)である.

RL was designed as an online learning paradigm in the first place [57].
**RLはそもそもオンライン学習のparadigm**(=パラダイムって枠組み? 方法論みたいな?)として設計されたものである[57].
Note that the expectation in eq. 2 is taken over the trajectories generated according to the learned policy, and d πθ t (s) is the discounted state visitation probability under πθ [32].
ただし、式2の期待値は、学習された方策に従って生成された軌道(trajectories)に対するものであり、$d_{t}^{\pi_{\theta}}(s)$ は, $\pi_{\theta}$ という条件下での,割引後の状態来訪確率(discounted state visitation probability)である[32].
One of the main contribution of [11] is bringing the REINFORCE algorithm to the offline batch learning setup commonly deployed in industrial recommender systems.
[11]の主な貢献の一つは、**産業用推薦システムで一般的に展開されているオフラインのバッチ学習設定にREINFORCEアルゴリズムを導入したこと**である.
The authors applied a first-order approximation [2] of importance sampling to address the distribution shift caused by offline training, resulting in a gradient of the following:
著者らは、オフライン学習による分布シフトに対処するために、重要度サンプリングの一次近似[2]を適用し、以下のような勾配を得ることができた.

$$
\nabla_{\theta}J(\pi_{\theta}) = \frac{\partial}{\partial \theta} J(\pi_{\theta})
\\
= \sum_{s_t \sim d_t^{\beta}(s), a_t \sim \beta(\cdot|s_t)}
[
    \frac{\pi_{\theta}(a_t|s_t)}{\beta(a_t|s_t)}
    R_t(s_t, a_t)
    \nabla_{\theta} \log{\pi_{\theta}(a_t|s_t)}
]
\tag{3}
$$

Here $\beta(\cdot|s)$ denotes the behavior policy, i.e., the action distribution conditioning on state s in the batch collected trajectories. d β t (s) is the discounted state visitation probability under β. This importance weight is further adapted to accommodate the set recommendation setup. We refer interested readers to [11] for more details.
ここで、$\beta(\cdot|s)$は**行動方策(behavior policy)**、すなわち、収集した軌跡のうち状態sを条件とする行動分布(action distribution)(action aを離散変数とした確率質量分布)を示す.
$d^{\beta}_{t}(s)$ はβの条件下での割引状態訪問確率(discounted state visitation probability)である.
このimportance weight(??)はさらに集合推薦設定(set recommendation setup)に適合するように調整される. 詳細については、[11]を参照されたい.

To balance exploration and exploitation, a hybrid approach that returns the top K ′ most probable items, while sampling the rest K −K ′ items according to πθ (Boltzmann exploration [13]), is employed during serving.
**探索と活用のバランスをとるために**、上位$K′$個のmost probable items(=最も確率が高いアイテム)を返し、残りの $K-K′$ 個のアイテムを$\pi_{\theta}$に従ってサンプリングするハイブリッドアプローチ（Boltzmann exploration [13]）を提供中に採用する.

# 4. Method メソッド

Here we introduce three simple methods inspired by exploration research in RL to increase user exploration in the REINFORCE recommender system during training.
ここでは、REINFORCE推薦システムにおいて、**学習中にユーザの探索性を高めるために、RLにおける探索研究にヒントを得た3つの簡単な方法**を紹介する.
That is, to recommend content less pertinent to the known user interests, and to discover new user interests.
すなわち、**既知のユーザの興味にあまり関係のないコンテンツを推薦し、新しいユーザの興味を発見すること**である。

## 4.1. Entropy Regularization Entropy Regularization (エントロピー正則化)

The first method promotes recommending contents less pertinent to the known user interests by encouraging the policy πθ (·
s) to have an output distribution with high entropy [61]. Mnih et al. [38] observed that adding entropy of the policy to the objective function discourages premature convergence to sub-optimal deterministic policies and leads to better performance. Pereyra et al. [46] conducted a systemic study of entropy regularization and found it to improve a wide range of state-of-the-art models.

We add of the entropy to the RL learning objective as defined in eq. 2 during training.
式2で定義されるRL学習目的に対して、学習時にエントロピーを追加する.
That is,
すなわち

$$
\max_{\theta} J(\pi_{\theta}) + \alpha \sum_{s_t \in d_t^\beta (s)} H(\pi_{\theta}(\cdot|s_t))
\tag{4}
$$

where the entropy of the conditional distribution πθ (·|s) is defined as H (πθ (·|s)) = − Í a ∈A πθ (a|s) log πθ (a|s). Here α controls the strength of the regularization. The entropy is equivalent to the negative reverse KL divergence of the conditional distribution πθ (·|s) to the uniform distribution. That is, H (πθ (·|s)) = −DK L(πθ (·|s)||U ) + const, where U stands for a uniform distribution across the action space A. As we increase this regularization, it pushes the learned policy to be closer to a uniform distribution, thus promoting exploration.
ここで、条件付き分布πθ (-|s)のエントロピーは、H (πθ (-|s)) = - Í a∈A πθ (a|s) log πθ (a|s) として定義される。ここで、αは正則化の強さを制御する。エントロピーは、条件分布πθ (-|s)の一様分布に対する負の逆KL発散と等価である。つまり、H (πθ (-|s)) = -DK L(πθ (-|s)||U ) + const、ここでUは行動空間Aにわたる一様分布を表す。この正則化を強めると、学習した政策がより一様分布に近くなり、探索を促進することができる。

## 4.2. Intrinsic Motivation and Reward Shaping 内発的動機づけと報酬の形成

The second method helps discovering new user interests through reward shaping.
第二の方法は，報酬の整形を通して，新しいユーザの興味を発見するのに役立つ.
The reward function r(s, a) as defined in eq. 2, describes the (immediate) value of a recommendation a to a user s. It plays a critical role in deciding the learned policy πθ .
報酬関数$r(s, a)$は式2で定義されるように、ユーザ $s$ (=user state $s$)に対する推薦 $a$ の(即時)価値を記述するもので、学習された方策$\$を決定する上で重要な役割を果たす.
Reward shaping, transforming or supplying additional rewards beyond those provided by the MDP, is very effective in guiding the learning of RL agents to produce policies desired by the algorithm designers [1, 27, 40].
報酬関数 の形状は，ユーザ$s$に対する推薦$a$の(即時)価値を記述し，学習した方策πθを決定する上で重要な役割を果たす．報酬関数 は，MDPが提供する報酬以外の報酬を変換したり供給したりして，RLエージェントの学習を導き，アルゴリズム設計者が望む方策を実現する上で非常に有効である[1, 27, 40].

Exploration has been extensively studied in RL [6, 42–44, 55], and has been shown to be extremely useful in solving hard tasks, e.g., tasks with sparse reward and/or long horizons, and.
探索はRLにおいて広く研究されており[6, 42-44, 55]、困難なタスク、例えば、報酬が疎なタスクや長い地平線を持つタスク、.NETを解く際に非常に有用であることが示されている.
These works can be roughly grouped into two categories.
これらの研究は、大きく分けて2つのカテゴリーに分類できる.
One concerns quantifying the uncertainty of the value function of the state-action pairs so the agent can direct its exploration on regions where it is most uncertain.
一つは、**state-actionペアの価値関数の不確実性を定量化**し、エージェントが**最も不確実な領域に探索を向けることができるようにすること**に関するものである.
The other uses a qualitative notion of curiosity or intrinsic motivation to encourage the agent to explore its environment and learn skills that might be useful later.
もう一つは、curiosity(好奇心)や**intrinsic motivation(内発的動機付け)**という定性的な概念を用いて、エージェントが環境を探索し、後で役に立つかもしれないスキルを学習することを促すものである.
Both camps of methods later adds an intrinsic reward r i (s, a), either capturing the uncertainty or curiosity to the extrinsic reward r e (s, a) that is emitted by the environment directly, to help the agent explore the unknown or learn new skills.
どちらの陣営の手法も、エージェントが未知の領域を探索したり、新しいスキルを学ぶのを助けるために、環境から直接発せられる**extrinsic reward(外在的報酬)** $r^{e}(s, a)$ に、不確実性や好奇心を捉えた**intrinsic reward(内在的報酬)** $r^{i}(s, a)$ を後から追加する.
That is, transforming the reward function to...
つまり、報酬関数を以下のように変換する...

$$
r(s, a) = c \cdot r^{i}(s, a) + r^{e}(s, a)
\tag{5}
$$

where $c$ controls the relative importance of the intrinsic reward w.r.t. the extrinsic reward emitted by the environment.
ここで、$c$ は環境から放出されるextrinsic reward に対する intrinsic rewardの相対的重要度を制御する.

Schmidhuber [49] formally captures the theory of creativity, fun and curiosity as an intrinsic desire to discover surprising patterns of the environment, and argues that a curiosity-driven agent can learn even in the absence of external reward.
Schmidhuber [49] は、創造性、楽しさ、好奇心の理論を、環境の驚くべきパターンを発見したいというintrinsic rewardとして正式に捉え、好奇心駆動型エージェントはexternal reward(=extrinsic rewardの事?)が無くても学習できると主張している.
Our proposal bears the same principle by rewarding the agent more when it discovers some previously unknown patterns of the environment, that is the user.
我々の提案は、**エージェントがユーザ=環境のこれまで知られていなかったパターンを発見したときに、より多くの報酬を与える**という同じ原理を担っている.
Let $R_t^{e}(s_t, a_t) = I_{r^e(st ,at )>0} \cdot \sum_{t'=t}^{T}\gamma^{t' - t}r^{e}(s_{t'}, a_{t'})$ be the discounted cumulation of the extrinsic reward on the stateaction pair (st , at ) observed on the trajectory.
$R_t^{e}(s_t, a_t) = I_{r^e(st ,at )>0} \cdot \sum_{t'=t}^{T}\gamma^{t' - t}r^{e}(s_{t'}, a_{t'})$ を、軌道上で観測されたstate-actionペア $(s_{t'}, a_{t'})$ の extrinsic rewardの割引累積報酬とする.
We then define the cumulative reward $R_t(s_t, a_t)$ used for the gradient update in eq. 3 as
そして、式 3 の勾配更新に用いる累積報酬(cumulative reward) $R_t(s_t, a_t)$ を次のように定義する.

$$
R_{t}(s_t, a_t) =
\tag{6}
$$

Here c > 1 is a constant multiplier.
ここで、c > 1 は定数倍である.

As explained in Section 3, the agent perceives the environment, that is the user interests and context, through encoding user’s historical activities Ht = {(A0, a0,r0), · · · , (At−1, at−1,rt−1)}.
セクション 3 で説明したように，エージェントはユーザの履歴 $H_t = {(A_0, a_0, r_0), - - , (A_{t-1}, a_{t-1},r_{t-1})}$ によって環境，つまりユーザの興味と文脈を認識する.
One can imagine a large update (surprise) to the agent’s modeling of the environment if an item at recommended given the state st is 1) drastically different from any of the items the user interacted with in the past; 2) enjoyed by the user, i.e., r e (st , at ) or R e (st , at ) is high.
もし、状態 $s_t$ が与えられたときに推薦されるアイテムが、 1) ユーザが過去にやりとりしたアイテムのどれとも大きく異なる、 2) ユーザが楽しんでいる、すなわち、$r_e(s_t , a_t)$ または $R_e(s_t, a_t)$ が高い場合、**agentの環境モデリング(=policyモデル)に大きな更新(surprise)があると想像される**.
These two conditions, surprise and relevance, align with the serendipity metrics we are going to detail in Section 5.5.
この2つの条件、**surpriseとrelevance**は、セクション 5.5 で詳述するセレンディピティのメトリックと一致する.(??)

To measure the surprise of $a_t$, we define $I_t = {a_{t'}, \forall t′ < t \And r_{t'} > 0}$ as the set of items the user interacted with up to time t.
$a_t$の surprise を測るために、時刻tまでにユーザがinteractionしたアイテムの集合を$I_t = {a_{t'}, \forall t′ < t \And r_{t'} > 0}$ を定義する.
As recommendation items are often associated with various attributes as described in Section 5.1, we use these attributes to measure the similarity (or difference) of a candidate action at towards I_t.
推薦アイテムは、5.1節で述べたように、様々な属性と関連付けられていることが多いので、これらの属性を用いて、$I_t$に対して**action候補の類似性(または差異)を計測**する.
For example, we consider an item at surprising (different) if its topic cluster is different from any of the items in It .
例えば，$I_t$に含まれるアイテムのいずれともトピック・クラスタが異なる場合，**そのアイテムはsurprising (different)である**と考える.

The multiplicative design in eq. 6 naturally accomplishes the second condition, that is, relevance.
式6の乗法設計は、2番目の条件である"**relevance(関連性)**"を自然に達成する。
Comparing with the additive form (eq. 5), the multiplicative design results in:
加法型（式 5）と比較すると、乗法型(式6?)は次のような結果をもたらす.

- 1. a candidate action at with zero extrinsic reward, i.e., R e t (st , at ) = 0 will NOT receive any additional reward even if being under-surfaced; extrinsic rewardがゼロのaction候補$a_t$、すなわち$R^e_t(s_t, a_t) = 0$は、表面下であっても追加報酬を受けない.
- 2.  an action at receiving higher extrinsic reward R e t (st , at ) will be rewarded even more compared with those that are equally surprising but received lower extrinsic reward. 2) 外挿報酬$R^e_t(s_t, a_t) $が高いaction $a_t$は、同様に驚くが外挿報酬が低いものに比べてさらに多く報酬を受ける.

This contrasts with the additive form where the extrinsic rewards observed does not influence the intrinsic reward.
これは、**外発的報酬が内発的報酬に影響を与えない加法的なデザインとは対照的**である.
In other words, the additive design gives a uniform boost to actions based entirely on surprise.
つまり、**加法的デザインは、surpriseだけに基づくactionに対して一律のブーストを与える**.
The multiplicative design on the other end, favors surprising actions that actually lead to improved user experience, indicated by higher extrinsic reward.
一方、乗法的なデザインは、**ユーザ体験の改善(=より高い外発的報酬によって示される)に実際につながる surprise のある action を好む**.

## 4.3. Actionable Representation for Exploration 探究のための行動的表現

The third method reinforces the newly discovered user interest through representation learning.
3つ目の方法は、新たに発見されたユーザの興味を**表現学習(representation learning)**によって補強するものである.
Learning effective representation is critical to improve the sample efficiency of many machine learning algorithms, and RL is no exception.
多くの機械学習アルゴリズムのサンプル効率を向上させるためには、**効果的な表現を学習することが重要**であり、RLも例外ではない.
Most prior work on representation learning for RL has focused on generative approaches, learning representations that capture all underlying factors of variation in the observation space in a more disentangled or well-ordered manner.
RLのための表現学習に関する先行研究のほとんどは、生成的なアプローチに焦点を当てており、観測空間(observation space)の変動のすべての根本的な要因を、より分離された、あるいは、よく秩序だった方法で捉える表現を学習している.
Self-supervised learning [20, 25, 50, 54] to capture the full dynamics of the environment has also attracted a lot of attentions lately.
また、環境のDynamics(state $s_t$ とactin $a_t$が与えられた時に、環境がどのように $s_{t+1}$ と $r_t$ を返すか?の設定)を完全に捉えるための自己教師付き学習[20, 25, 50, 54]も最近注目されている.
Ghosh et al. [16] instead argue to learn functionally salient representations: representations that are not necessarily complete in terms of capturing all factors of variation in the observation space, but rather aim to capture those factors of variation that are important for decision making – that are "actionable."
Ghoshら[16]はその代わりに、機能的に顕著な表現を学習することを主張している：観察空間における変動の全ての要因を捕らえるという点では必ずしも完全ではなく、むしろ意思決定にとって重要な、つまり "action可能な(actionableな)"変動の要因を捕らえることを目指した表現である.

The REINFORCE agent introduced in Section 3 describes the environment, i.e., the user, through encoding his/her historical activities Ht .
第3節で紹介したREINFORCEエージェントは、ユーザの過去の活動$H_t$を符号化することで、環境、つまりユーザを記述する.
That is, $u_{st} = RNN_{\theta}(H_t)$.
すなわち、$u_{st} = RNN_{\theta}(H_t)$である.
When an user interacted with a surprising item at (to the agent) and gave high reward, the user state ust should be updated to capture the new information so the agent can act differently next.
That is, to make recommendations according to the newly acquired information about the new interest of the user. To aid the agent in capturing this information in its state, we extend Ht with an additional bit, indicating whether or not an item the user interacts with is surprising and relevant. That is, we expand Ht = {(A0, a0,r0,i0), · · · , (At−1, at−1,rt−1,it−1)}, where it ′ = 1 if 1) the attribute of at (such as topic cluster) is different from that of any items in It ′ (being a surprise) and; 2) rt > 0 (being relevant). Here It ′ is the list of items the user has interacted with up to time t ′ . This feature is then embedded and consumed by the RNN along with other features describing the item at.
ユーザが（エージェントにとって）意外なアイテムとinteractし、高い報酬を得た場合、ユーザ状態$u_{s_t}$は、エージェントが次に異なるactionを取れるように、新しい情報を捕らえるために更新されるべきである.
つまり、**ユーザの新しい興味に関する新しく得た情報に従って、推薦を行う**ことである.
エージェントがその状態にこの情報を取り込むのを助けるために、我々は$H_t$を追加ビットで拡張し、ユーザが相互作用するアイテムが驚きと関連性があるか否かを示す.
すなわち、$H_{t} ={(A_0, a_0, r_0, i_0), \cdots, (A_{t-1}, a_{t-1}, r_{t-1}, i_{t-1})}$ と展開し、

- 1. $a_t$の属性（トピッククラスタなど）が$I_{t′}$内のどのアイテムとも異なる場合(= **being a surprice** )
- 2. $r_t > 0$ (=**being relevant**)

の場合に、$i_{t′}=1$ 、とする.

ここで、$I_{t′}$ は、時刻$t'$までにユーザがinteractionしたアイテムのリストである.
この特徴は、その後、RNNによって、アイテムを説明する他の特徴とともに埋め込まれ、消費される.

# 5. Measurement 測定

Personalization has been the cornerstone of modern recommender systems.
パーソナライゼーションは、現代のレコメンダーシステムの基礎となっている.
It aims to produce targeted and accurate recommendations based on user historical activities.
これは、ユーザの過去の行動履歴をもとに、ターゲットを絞った正確な推薦を行うことを目的としている.
Overly focusing on the accuracy aspect of recommendation, however, runs the risk of exposing users only to a concentrated set of contents.
しかし、**精度(accuracy)を重視するあまり、限られたコンテンツにしかアクセスできなくなる危険性がある**.
This could attract user attention in the near term, but likely hurt user experience in the long run.
これは、**短期的にはユーザの注目を集めることができても、長期的にはユーザーエクスペリエンスを損なう可能性がある**.
There has been a growing body of work examining factors other than accuracy in shaping user’s perception of recommendation quality [9, 19, 35, 66, 72, 72].
このように，レコメンデーションの品質に対する ユーザの認識を形成する要因として，**精度以外の要素(factors other than accuracy)** を検討する研究が増えてきている [9, 19, 35, 66, 72, 72].
In particular, aspects such as diversity, novelty and serendipity of recommendations have been studied.
特に，レコメンデーションの多様性，新規性，セレンディピティなどの側面が研究されている.
Here we design metrics to measure these four aspects for a RL based recommender system.
本論文では，RL ベースの推薦システムにおいて，これら**4つの側面**を測定するための指標を設計する.
Some of the metrics measure directly on the learned policy πθ , and thus apply only to systems producing a distribution over the content vocabulary.
これらのメトリクスの中には，学習された推薦方策$\pi_{\theta}$を直接測定するものがあり，content vocabularyの分布(=action spaceの分布の事?)を生成するシステムにのみ適用される.
Others measure on the recommendation set A πθ generated by acting according to πθ (taking most probable items) 1 , which are generic for any types of recommender systems 2 .
また，$\pi_{\theta}$ に従って行動することで生成される推薦集合 $A_{\pi_{\theta}}$ **(Most probable items)** を測定するものもあり，これらはあらゆる種類の推薦システムに対して汎用的である.
These metrics bear similarity to many prior works in quantifying the four factors of recommendation quality [5, 8, 15, 19, 26, 29, 66].
これらの指標は，推薦品質の 4 要素を定量化した多くの先行研究 [5, 8, 15, 19, 26, 29, 66] と類似している.

## 5.1. Attributes 属性

We first introduce two item attributes that are used to define both the surprise factor in eq (6) as well as the metrics:
まず、式(6)のsurprice因子と測定基準を定義するために使用される2つのアイテム属性を紹介する.

Topic cluster.
トピッククラスタ.
A topic cluster for each item is produced by:
各アイテムのTopic Clusterは次のようにして作成される.

1. taking the item co-occurrence matrix, where entry (i, j) counts the number of times item i and j were interacted by the same user consecutively; アイテム共起行列(エントリ(i, j)は、アイテム i と j が同じユーザーによって連続的に操作された回数を数える)を取る
2. performing matrix factorization to generate one embedding for each item; 各アイテムの埋め込みを生成するために行列分解を行う、
3. using k-means to cluster the learned embeddings into 10K clusters; k-means を使って学習した埋め込みを 10K クラスタにまとめる、
4. assigning the nearest cluster to each item. 最も近いクラスタを各アイテムに割り当てる

Content provider.
コンテンツの提供者.
Content provider is another attribute of interest as:
コンテンツ提供者は、次のような理由から注目される属性である.

- 1. we observed consistency between contents produced by the same provider, e.g., a food blogger often writes about specific cuisines; 例えば、料理ブロガーは特定の料理について書くことが多いなど、同じプロバイダーによって作られたコンテンツ間の一貫性が観察された.
- 2.  we are interested in understanding the importance of content-provider diversity/novelty [37, 64] in influencing long term user experience. 長期的なユーザ体験に影響を与えるcontent-providerの多様性/新規性 [37, 64] の重要性を理解することに興味がある.

## 5.2. Accuracy 精度

Arguably the most important property of a recommender is to be able to retrieve contents the user is interested in consuming. We compute the mean average precision at K = 50 (mAP@50) [63] on the recommended set A πθ to measure the accuracy, that is the average precision of identifying an item the user is interested in consuming among A πθ.
レコメンダーの最も重要な特性は、ユーザーが消費することに興味があるコンテンツを検索できることであると言える.
そこで、推薦セット$A_{\pi_{\theta}}$のK = 50におけるmean average precision at K=50(mAP@50)[63]を計算し、精度、すなわち$A_{\pi_{\theta}}$の中からユーザが消費したいと思うアイテムを特定できる平均精度を計測する.

## 5.3. Diversity ♪多様性

Diversity measures the number of distinct faucets the recommendation set contains.
多様性は、推薦セットが含む異なるfaucets(蛇口?)の数を測定する.
Many measurements of set diversity have been proposed [39, 45, 53].
セットの多様性の測定は多く提案されている[39, 45, 53]．
Among them, the average dissimilarity of all pairs of items in the set is a popular choice.
その中でも，**集合に含まれるすべてのペアの平均非類似度**はよく選ばれている.(dissimilarity = 1 - 正規化したsimillarity みたいなイメージ.)

$$
\text{Diversity}(A^{\pi_{\theta}})
= E_{s \in d^{\beta}}[1 - \frac{1}{|A^{\pi_{\theta}}|(|A^{\pi_{\theta}}| -1)}
\sum_{i, j \in A^{\pi_{\theta}}} \text{sim}(i,j)
]
\tag{7}
$$

We define the similarity between two items i and j both on topic level and on content provider level.
2つのアイテムiとjの間の類似度を topic level と content provoderレベルの両方で定義する.
That is, Sim(i, j) = 1 if i and j belongs to the same topic cluster, and 0 otherwise.
すなわち、Sim(i, j) = iとjが同じトピッククラスタに属する場合は1、そうでない場合は0とする.
Similarly for content provider.
コンテンツ・プロバイダについても同様.

## 5.4. Novelty

The two terms of novelty and serendipity have been used interchangeably in the literature.
**Novelty(新規性)とセレンディピティという2つの用語は、文献上では互換的に用いられている**.
In this work, we use novelty to focus on the global popularity-based measurements and serendipity to capture the unexpectedness
この研究では、グローバルな人気に基づく測定に焦点を当てるためにNoveltyを使用し、unexpectedness(意外性)を捉えるためにセレンディピティを使用している.

$$
I(a) = - \log p(a)
= - \log \frac{\text{# user consumed item a}}{\text{# users}}
\\
= - \log (\text{# users consumeed item a}) + \text{const}
\tag{8}
$$

Here $p(a)$ measures the chance a random user would have consumed item a. By definition, a globally "under-explored" item (tail content) will have higher self-information.
ここで、 $p(a)$ は**ランダムなユーザがアイテムaを消費する確率**を表す.定義によれば、グローバルに"探索されていない"("under-explored"な)アイテム(tail content = long-tailアイテムの事か!)は、**より高いself-information**(自己情報??)$I(a)$を持つことになる.
With the definition of item-level self-information, we can then measure novelty of the learned policy πθ as
このようなアイテムレベルの自己情報$I(a)$の定義により、学習されたポリシー$\pi_{\theta}$の Novelty を次のように測定することができる.

$$
\text{Novelty}(\pi_{\theta})
= E_{s_t \in d_t^{\beta}}[\sum_{a \in A} \pi_{\theta}(a|s_t) I(a)]
\tag{9}
$$

A learned policy πθ that casts more mass on items with higher selfinformation, being able to recommend "under-explored" items, is deemed more novel.
**self-informantionの高いアイテムにより多くの質量(=そのアイテムを選ぶ確率質量?)を投じ**、"開拓されていない"アイテムを推薦できる学習済みポリシー$\pi_{\theta}$は、よりNoveltyが高いと判断される.
We can define the novelty metrics for attributes similarly by looking at the self-information of the attribute instead, e.g., popularity of the content provider.
属性についても、**content-providerの人気度など**、**属性のself-informationを代わりに見る**ことで、**同様にNoveltyの指標を定義できる**.

## 5.5. Serendipity ♪セレンディピティ

Serendipity captures the unexpectedness/surprise of a recommendation to a specific user. It measures the capability of the recommender system to recommend relevant contents outside of the user’s normal interests. There are two important factors in play here: 1) unexpectedness/surprise: as a counter example, a recommendation of John Lenon to listeners of The Beatles will not constitutes a surprising recommendation; 2) relevance: the surprising contents should be of interest to the user. In other words, serendipity measure the ability of the recommender to discover previously unknown (to the recommender) interests of the user.
セレンディピティは、**特定のユーザに対する推薦の unexpectedness/surprise** を表現するものである.
推薦システムが、ユーザの通常の関心事以外の関連コンテンツを推薦する能力を測るものである.
ここでは、2つの重要な要素がある.

- 1. unexpectedness/surprise：反例として、ビートルズのリスナーにジョン・レノンを推薦しても、意外な推薦にはならない.
- 2. relevance：意外なコンテンツは、ユーザにとって興味があるものでなければならない.

つまり、セレンディピティとは、**推薦者がユーザの（推薦者にとって）未知の興味を発見する能力を測定するもの**である.

We define the serendipity value of a recommendation at w.r.t. a user with interaction history of It as
我々は、"$I_t$のインタラクション履歴を持つユーザに対して、アイテム$a_t$を推薦する事"のセレンディピティ値を以下のように定義する.

$$
S^{topic}(a_t|s_t, I_t) = \begin{cases}
  1, & \text{hoge} \\
  0, & \text{otherwise}
\end{cases}
\tag{10}
$$

Again we can define the content-provider level serendipity value similarly.
ここでも同様に、content-providerレベルのセレンディピティ値を定義することもできる.
With the serendipity value of an item defined, we can then quantify the serendipity of the recommendation set Sπθ as
あるアイテム$a_t$のセレンディピティ値が定義されると、推薦セット $S_{\pi_{\theta}}$ のセレンディピティは以下のように定量化される.

$$
\text{Serendipity}(A^{\pi_{\theta}})
= E_{s_t \in d^{\beta}_t}
[\frac{1}{|A^{\pi_{\theta}}|} \sum_{a \in A^{\pi}} S^{topic}(a_t|s_t, H_t)]
\tag{11}
$$

## 5.6. Long Term User Experience 長期的なユーザエクスペリエンス

Past work has suggested connections between these recommendation qualities toward long term user experience, either through surveys or interviews [5, 66].
過去の研究では、調査やインタビューを通じて、長期的なユーザ体験に向けたこれらの推薦品質の間の関連性が示唆されている[5, 66].
We use user returning to the platform, and user moving from a low-activity bucket to a highly-active one on the platform as the holistic measurement of improved long term user experience, and establish the connection between these measurements and long term user experience.
我々は，長期的なユーザ経験の改善の全体的な測定として，ユーザがプラットフォームに戻ること，および，ユーザがプラットフォーム上で低活動バケットから高活動バケットに移動することを使用し，これらの測定と長期的なユーザ経験の間の関係を確立する.

# 6. Offline Analysis オフライン分析

We conducted an extensive set of offline experiments comparing the exploration strategies introduced in Section 4.
我々は、セクション 4 で紹介した探索戦略を比較するために、広範なオフライン実験を実施した.
Specifically, we built these exploration approaches onto the baseline REINFORCE recommender described in Section 3.
具体的には、セクション 3 で述べたベースライン REINFORCE レコメンダー上にこれらの探索手法を構築した.
We evaluate them by computing the set of metrics defined in Section 5 and compare the metric movements between different hyper-parameter settings and different exploration methods.
我々は、セクション5で定義されたメトリクスのセットを計算することによってそれらを評価し、**異なるハイパーパラメータの設定と異なる探索方法の間でメトリクスの動きを比較し**た.

## 6.1. Dataset データセット

We conducted 3 runs of experiments for each comparison and report the mean and standard deviation of the metrics.
各比較について3回の実験を行い、メトリクスの平均と標準偏差を報告する.
For each experiment run, we extracted close to a billion user trajectories from a commercial recommendation platform.
各実験では、**商用レコメンデーションプラットフォームから10億近くのユーザの軌跡を抽出**した.
Each trajectory HT = {(st ,At , at ,rt ) : t = 0, . . .
各軌跡 $H_T = {(s_t, A_t, a_t, r_t):t = 0, \cdots, T}$, as described in Section 3, contains user historical events on the platform.
各軌跡 $H_T = {(s_t, A_t, a_t, r_t):t = 0, \cdots, T}$は、セクション3で説明したように、プラットフォーム上のユーザの履歴イベントを含んでいる.
The lengths of trajectories between users can vary depending on their activity level.
ユーザ間の軌跡の長さは、ユーザの活動レベルに応じて変化しうる.
We keep at most 500 historical pages with at least one positive user interaction (nonzero rt ) for each user.
また，各ユーザの少なくとも1回の正のユーザ間Interaction(非ゼロ$r_t$)を持つ履歴ページを最大500件保持する.
Among the collected trajectories, we hold out 1% for evaluation.
また，収集した軌跡のうち，1%を評価のために残しておく.
We restrict our action space (item corpus) to the most popular 10 million items in the past 48 hours on the platform.
また，action space(=アイテムコーパス)を，過去 48 時間にプラットフォーム上で最も人気のあった 1000 万アイテムに限定する.
Our goal is to build a recommender agent that can choose among the 10 million corpus the next set of items for users to consume so as to maximize the cumulative long-term reward.
我々の目標は、長期的な累積報酬(cumulative long-term reward)を最大化するように、**ユーザが消費する次のアイテムセットを1000万コーパスの中から選択することができる推薦エージェントを構築すること**である.

## 6.2. Entropy Regularization Entropy Regularization (エントロピー正則化)

The most straightforward knob to tune up and down the exploration strength for entropy regularization is the regularization coefficient α as defined in eq. 4.
エントロピー正則化の探索強度を上下に調整するための最も分かりやすいknob(ノブ?)は、式4で定義される正則化係数αである.
We compare the baseline method, a REINFORCE agent maximizing only the expected return as defined in eq. 2, with added entropy regularization with α in [0.1, 0.5, 1.0, 10.0].
式2で定義される期待収益(expected return = reward?)のみを最大化するREINFORCEエージェントと、αを[0.1, 0.5, 1.0, 10.0]としたエントロピー正則化を加えたベースラインの方法を比較する.

As shown in Table 1, entropy regularization is an extremely efficient method to introduce diversity and novelty to the system, at the cost of reduced accuracy.
表1に示すように、**エントロピー正則化は、精度の低下を代償に、システムに多様性と新規性を導入する非常に効率的な方法**である.
When the regularization strength is large, it also significantly drops the system’s capability to introduce serendipitous contents to users because of the loss of relevance.
また、**正則化の強度が大きいと、relevanceが失われるため、ユーザにセレンディピティなコンテンツを紹介するシステムの能力が大きく低下する**.
For example, a regularization strength of α = 1.0 drops the topic serendipity value by −21.6% (0.037 → 0.029).
例えば、正則化の強さをα=1.0とすると、トピックセレンディピティの値は-21.6%（0.037→0.029）低下する.

## 6.3. Intrinsic Motivation 内発的動機づけ

One of the obvious hyper-parameters to adjust the exploration strength for the intrinsic motivation approach is to tune the boosting factor c defined in eq. 6.
内発的動機付けアプローチの探索強度を調整するための明白なハイパーパラメータの1つは、式6で定義されるブースティング係数cを調整することである.
Here we study the impact of the more interesting variants.
ここでは、より興味深い変数?の影響について研究する.

First, on which attribute to use to define surprise.
まず、**どの属性で"surprise"を定義するか**について.
We experimented with defining surprise by topic cluster (denoted as "topic" in Table 2) and content provider (denoted as "provider" in Table 2).
我々は、トピッククラスタ(表2では"topic"と表記)とコンテンツプロバイダー（表2では「プロバイダー」と表記）によって"surprise"を定義する実験を行った.
Second, on the length of the user historical events used to define surprise.
第二に、**"surprise"を定義するために使用するユーザの履歴イベントの長さ**について。
As explained in [66], users’ perception of surprise of contents can drift over time.
[66]で説明したように，ユーザのコンテンツの"surprise"に対する認識は，時間の経過とともに漂うことがある.
Contents that the user interacted in the past, but has not been served and interacted for a long time, can be deemed surprising when being resurfaced again.
**また，過去にinteractionを行ったが，長い間サービスやインタラクションを行っていないコンテンツは，再び登場したときに"surprise"と感じることがある**.
We experimented with having It contain all the items the user interacted with in the past one day, one week and one year (denoted as d = 1, d = 7 and d = 365 respectively in Table 2).
そこで，**過去1日，1週間，1年（表2においてそれぞれd=1，d=7，d=365と表記）にユーザが接触したすべてのアイテムを$I_t$に含ませて実験した.**

Table 2 summarizes the comparison between different variants of the intrinsic motivation proposal.
表2は、内発的動機付けの提案(intrinsic motivation proposal)の異なるバリエーション間の比較をまとめたもので.
Similar to entropy regularization, all variants improve on diversity at the cost of lower accuracy.
**エントロピー正則化と同様に、すべてのバリエーションは精度を下げる代償に多様性を向上させる**.
This method does not change the novelty metrics significantly, neither on the item level nor content provider level.
この方法は、アイテムレベルでもコンテンツプロバイダレベルでも、新規性の指標を大きく変えることはない.
We thus conclude that tail contents are not necessarily more serendipitous (relevant and surprising) than popular ones.
したがって，**tailコンテンツは必ずしも人気コンテンツよりもセレンディピティ(relevantとsurprising)が高いとは言えないと結論づけることができる**.(まあなー...)
We do see a significant improvement in the serendipity metrics, even though the overall accuracy of these methods turn out unfavorable comparing with the baseline.
しかし，これらの手法の全体的な精度はベースラインと比較して劣るものの，セレンディピティメトリクスには大きな改善が見られる.
As an example, the variant which uses topic cluster and a historical window size of 7 days, improves the serendipity level by +18.9% (0.037 → 0.044) even though the overall accuracy measured by mAP@50 was dropped by −13.7% (0.070 → 0.063).
例えば、トピッククラスタと7日間の履歴ウィンドウサイズを使用するバリエーションは、mAP@50で測定された全体的な精度が-13.7% (0.070 → 0.063) 減少しても、セレンディピティのレベルが+18.9% (0.037 → 0.044) 改善されている.

Attributes.
属性についての比較結果.
Offline analyses showed both definitions of surprise based on topic cluster and content provider are equally effective in optimizing different angles of serendipity.
オフライン分析では、トピッククラスタとコンテンツプロバイダに基づく驚きの定義の両方が、セレンディピティの異なる角度を最適化する上で**等しく有効**であることが示された.
That is topic cluster definition improves offline topic serendipity metrics by +18.9% from 0.037 to 0.044, and content provider definition improves content provider serendipity for +11.5% from 0.078 to 0.087.
つまり、トピッククラスタの定義は、オフラインでのトピックセレンディピティの指標を0.037から0.044へ+18.9%改善し、コンテンツプロバイダーの定義は、コンテンツプロバイダセレンディピティを0.078から0.087へ+11.5%改善することが示された.
We however do see very different performance in user metrics in live experiments as shown in Section 7.1 below, suggesting one angle (topic serendipity) is more important than the other (content provider serendipity) in optimizing the overall user experience.
しかし、以下のセクション7.1に示すように、ライブ実験では、ユーザメトリクスのパフォーマンスが非常に異なっており、**全体的なユーザ体験を最適化する上で、一方の角度（トピックセレンディピティ）が他方（コンテンツプロバイダセレンディピティ）よりも重要であること**が示唆されている.

Window sizes.
ウィンドウのサイズに関する実験結果.
As we extend the historical window used to define surprise, i.e., having It contain longer user history, the definition of surprise becomes stricter.
"surprise"を定義するために使用する履歴ウィンドウを拡張すると、つまり、より長いユーザー履歴を含むようにすると、**"surprise"の定義がより厳しくなる**.
An item is less likely to be surprising
アイテムがsurpriseである可能性は低くなる.

## 6.4. Actionable Representation Actionable Representation

In this set of experiments, we compare four setups:
この実験では、4つのセットアップを比較した.

- 1. baseline: the baseline REINFORCE algorithm; ベースライン: ベースライン REINFORCE アルゴリズム、
- 2. repre. alone: the baseline REINFORCE with the actionable representation, i.e., the additional bit indicating if the item at is serendipitous at state st according to user historical interactions It ; ベースライン REINFORCE に実行可能な表現、すなわち、ユーザーの過去のインタラクション It に従って状態 st でアイテムがセレンディピティであるかどうかを示す追加ビットを加えたもの、
- 3. intrinsic alone: the baseline REINFORCE with intrinsic motivation for reward shaping; ベースラインREINFORCEに対して、報酬形成用 の内在的動機を加えたもの.
- 4. repre. + intrinsic: the baseline REINFORCE adding both the intrinsic motivation and the actionable representation ベースライン REINFORCE に内在的動機と実行可能表現を加えたもの、

As shown in Table 3, adding the indicator alone (row 2) and adding the indicator along with the intrinsic motivation (row 4) resulted in very different metrics.
表3に示すように、**indicatorを単独で追加した場合（2行目）と、指標を内発的動機づけとともに追加した場合（4行目）では、非常に異なるmetricsとなった**.
Adding the indicator alone without the reward shaping performs very similarly to the baseline method, suggesting the representation is more useful when combined with the reward shaping.
報酬形成なしでindicatorを単独で追加すると、ベースライン手法と非常に似たパフォーマンスを示し、報酬形成と組み合わせた場合に表現がより有用であることが示唆された.
We see +24.3% improvement in the serendipity value comparing (row 4) to (row 1) (0.037 → 0.046), and +4.5% improvement comparing to (row 3) (0.044 → 0.046).
セレンディピティ値は、(4)と(1)を比較すると+24.3% (0.037 → 0.046) 、(3)を比較すると+4.5% (0.044 → 0.046) の向上が見られた.
This suggests that the added representation is indeed helpful for decision making when the intrinsic motivation is rewarding serendipitous actions, i.e. actions that discover previously unknown user interests.
このことから、セレンディピティ行動、すなわち、**これまで知られていなかったユーザの興味を発見する行動に対して報酬を与えることがintrinsic motivationである場合**、追加した表現が意思決定に有用であることが示唆された.

To gain more insight into how the agent utilizes the additional bit indicating whether or not a historical event is surprising when provided, we compare the learning of the baseline REINFORCE algorithm with intrinsic motivation alone (shown in orange in Figure 1) vs the one combined with both the intrinsic motivation and the actionable representation (shown in cyan in Figure 1).
historical eventが提供されたときに驚くかどうかを示す追加のビットをエージェントがどのように利用するかをより深く理解するために、ベースラインREINFORCEアルゴリズムの学習を、intrinsic motivationのみ（図1のオレンジで示す）と、intrinsic motivationとactionable representationの両方を組み合わせたもの（図1のシアン色で示す）とを比較してみる.
The RNN [31] Chen et al. [11] used to encode the user history Ht has an important gate named input gate.
ユーザ履歴 $H_t$ を符号化するために使用されるRNN [31](Chenら[11])には、入力ゲートという重要なゲートがある.
This gate controls how much the RNN is updating its hidden state to take into account a new input (event).
このゲートは、RNNが新しい入力（イベント）を考慮して、どれだけ隠れ状態を更新するかを制御する.
We take the activation values of the input gates across the user trajectory, and separate the values in two groups: the ones on historical events that are considered surprising and relevant (shown in Figure 1 left), and the ones on historical events that are not (shown in Figure 1 right).
ユーザの軌跡を横断して入力ゲートの活性化値をとり、意外性があり関連性があると考えられる履歴イベントに関するもの（図1左）と、そうでない履歴イベントに関するもの（図1右）に分ける.
Comparing the left and right figures, we can see that by adding this additional information, the RNN is able to differentiate better between historical events that are serendipitous and those that are not.
左右の図を比較すると、**このように付加的な情報を加えることで、RNNはセレンディピティとなるhistrical event とそうでないものをより区別することができる**ことがわかる.
At the end of training, the mean activation for events that are surprising and relevant (left) is at 0.1765 (+1.4% higher) for intrinsic motivation + actionable representation compared with 0.1741 for intrinsic motivation alone.
学習終了時、"surprising"と"relevant"のあるevent(i.e. セレンディピティ的なevent)（左図）に対する平均活性度は、intrinsic motivation だけの場合0.1741であるのに対し、 intrinsic motivation ＋ actionable representation では0.1765（+1.4%）になっている.
The mean activation for events that are NOT serendipitous (right) is at 0.1409 (−11.2% lower) for intrinsic motivation + actionable representation compared with 0.1586 for intrinsic motivation alone.
一方、セレンディピティではない事象（右）に対する活性化の平均値は、 intrinsic motivation ＋ actionable representation では0.1409（-11.2%）となり、 intrinsic motivation のみの場合の0.1586と比較して低くなっている.
This suggests that relying on the reward alone, RNN can still recognize the difference between these two groups of events and perform slightly larger update when the historical event is considered surprising.
このことは、RNNが報酬だけに頼っていても、**historical eventが surprising だと思われる場合には、これら2つのグループの違いを認識し、やや大きな更新を行うことができる**ことを示唆している.
Adding the feature helps RNN differentiate the two groups better.
特徴を加えることで、RNNが2つのグループをよりよく区別することができる.

# 7. Live Experiments and Long Term User Experience ライブ実験と長期的なユーザーエクスペリエンス

We conduct a series of live A/B tests on a industrial recommendation platform serving billions of users to evaluate the impact of the proposed exploration approaches. The control serves the base REINFORCE agent as described in Section 3. The agent selects hundreds of candidates from a corpus of 10 million. The returned candidates A πθ , along with others, are ranked by a separate ranking system before showing to the users. We ran three separate experiments: 1) Entropy regularization: serving the REINFORCE agent with entropy regularization as explained in Section 4.1; 2) Intrinsic motivation: serving the REINFORCE agent with intrinsic motivation to discover new user interest (using topic cluster attributes with a history window of 7 days and a serendipity boost c = 4) as explained in Section 4.2; 3) Intrinsic Motivation + Actionable Representation: serving the REINFORCE agent with both the intrinsic motivation and the actionable representation as introduced in Section 4.3. We compare 1) and 2) to the baseline REINFORCE system as described in Section 3 as control to measure the effect of entropy regularization and intrinsic motivation respectively, and 3) to 2) as control to measure the additional value of introducing the actionable representation on top of intrinsic motivation. We first summarize the live experiment results of these experiments in Section 7.1, and later measure several aspects of long term user experience in Section 7.2. In the end, we establish the connection between exploration and different aspects of recommendation quality toward improving long term user experience.
我々は、提案する探索アプローチの影響を評価するために、数十億のユーザーにサービスを提供する産業推薦プラットフォーム上で一連のライブA/Bテストを実施した/
制御は、セクション3で説明したように、基本的なREINFORCEエージェントを提供する.
エージェントは1,000万件のコーパスから数百の候補を選択する. 
返された候補 $A^{\pi_{\theta}}$ は、他の候補とともに、ユーザに見せる前に別のランキングシステムによってランク付けされる. 
我々は3つの別々の実験を行った.
- 1. エントロピー正則化：セクション4.1で説明したように、エントロピー正則化でREINFORCEエージェントを提供する. 
- 2. Intrinsic motivation ：セクション4.2で説明したように、新しいユーザーの興味を発見するための本質的動機づけ（7日の履歴ウィンドウとセレンディピティ・ブーストc = 4でトピッククラスタ属性を使用）をREINFORCEエージェントに与える.
- 3. Intrinsic motivation + Actionable Representation：セクション4.3で紹介したように、 Intrinsic motivation と Actionable Representation 両方でREINFORCEエージェントへ与える.

1)と2)は、エントロピー正則化と内在的動機付けの効果を測定するために、セクション3で説明したベースラインREINFORCEシステムと比較し、3)は、内在的動機付けの上に実用的表現を導入することによる付加価値を測定するために、コントロールとして2)と比較した. 
まず、7.1節でこれらの実験のライブ実験結果をまとめ、その後、7.2節で長期的なユーザ体験のいくつかの側面を測定する.
最後に、**長期的なユーザ体験を向上させるために、探索と推薦品質のさまざまな側面との関連性**を確立する.

## 7.1. Results 結果

Figure 3 summarizes the performances of these exploration approaches on the top-line metric capturing user overall enjoyment of the platform.
図3は、**ユーザのプラットフォームに対する総合的な楽しさを表す top-line metric** における、これらの探索アプローチのパフォーマンスをまとめたものである.
As shown in Figure 3a (α = 0.1 in red, and α = 0.5 in blue), although entropy regularization increases diversity and novelty in both offline and live experiments, it does not lead to significant improvement on the user enjoyment.
図3a（赤がα=0.1、青がα=0.5）に示すように、**エントロピー正則化はオフラインとライブの両方の実験で多様性と新規性を高めるが、ユーザの楽しみを大きく改善することにはつながらない.**
In other words, increased diversity or novelty alone does not necessarily lead to better user experience.
つまり、**多様性や新規性の向上だけでは、必ずしもユーザ体験の向上につながらないのである**.
When we increase the regularization strength to α = 0.5, we see slightly worse live metrics.
正則化の強さをα=0.5まで上げると、ライブのメトリクスが若干悪くなることがわかる.

Another top-line metric that we keep track of is the number of days users returning to the platform.
もうひとつの重要な指標は、**ユーザがプラットフォームを再び利用する日数**である.
For both the intrinsic motivation and actionable representation treatment, we observed significant improvement on this metric as well, suggesting users are encouraged to return to the platform due to better recommendation quality.
これは、レコメンデーションの質が向上することで、ユーザがプラットフォームに戻ってくるようになることを示唆している.
Figure 2 shows the improvement of user returning in the actionable representation experiment, comparing with the base REINFORCE with intrinsic motivation as control, suggesting that aiding the representation learning with the serendipity information further improves the learned policy, leading to better overall user experience.
図2は、内発的動機付けを用いたREINFORCE(control群)と比較して、アクショナブル表現の実験(treatment群)におけるユーザの再訪率の向上を示しており、**セレンディピティ情報を用いて表現学習を支援することで、学習したポリシーがさらに向上し、全体としてより良いユーザ体験につながっている**ことが示唆される.

## 7.2. Long Term User Experience 長期的なユーザーエクスペリエンス

Learning Effect of Intrinsic Motivation.
内発的動機付けの学習効果.
To better understand the effect of intrinsic motivation and reward shaping in the long term, we examine the temporal trend of the live metrics in addition to the aggregated metrics reported above.
長期間における intrinsic motivation と reward shaping の効果をよりよく理解するために、我々は、上記で報告された集約された aggregated metrics に加えて、live metrics(オンラインで観測するようなmetrics?)の時間的傾向を調べる.
For the 6-week experiment on intrinsic motivation, we look at week-over-week metrics by aggregating user activities within each week.
intrinsic motivation に関する 6 週間の実験では、各週のユーザ活動を集計して、前週比のmetricsを調べる.
Specifically, we track the number of unique topic clusters the user has interacted with over every week, as well as the entropy of those topic clusters.
具体的には、**ユーザが1週間にわたって交流したユニークなトピッククラスタの数**と、**それらのトピッククラスタのエントロピー(=乱雑さの度合い?)の追跡**を行う.
Suppose the user has interacted with Ni items from topic cluster i, then the entropy of his/her history is computed as − Í i pˆi loд(pˆi), where pˆi = Ni / Í i Ni is the proportion of items interacted with that are from topic cluster i.
ユーザーがトピッククラスタ $i$ から $N_i$ 個のアイテムと相互作用したとすると、その履歴のエントロピーは $- \sum_{i} \hat{p}_{i} \log (\hat{p}_i)$ と計算される. ここで $\hat{p}_i = \frac{N_i}{\sum_{i} N_i}$ はトピッククラスタ $i$ から相互作用したアイテムの割合である.

Figure 4 shows the comparison between control and treatment, where the treatment group has a boosting multiplier of 4 for unknown user interests as in Eq. (6).
図4は、式(6)のように、未知のユーザの興味に対してブースティング乗数を4とした場合の、対照群と処理群の比較を示している.
Compared with users in the control group which does not have the reward shaping, users in the treatment group have consistently interacted with more topic clusters (Fig 4a) and generated a higher entropy over cluster distributions (Fig 4c) over the whole experiment period.
reward shaping を行わない control群のユーザに比べ、**treatment群のユーザは実験期間全体を通して一貫して、より多くのトピッククラスタと交流し（図4a）、クラスタ分布に対するより高いエントロピーを生成している（図4c）**.
More interestingly, the amount of improvements over control is increasing over time (Fig 4b and 4d).
さらに興味深いことに、control群に対する(=比較した)改善量は時間とともに増加している .（図4b、図4d）.
This suggests a learning effect over time from exploration, which enables users to continuously find and engage with new topics.
これは、**探索による経時的な学習効果により、ユーザが継続的に新しいトピックを見つけ、それに関わることができるようになったこと**を示唆している.

User Activity Levels.
ユーザーの活動レベル.
Users who come to the recommendation platform are heterogeneous in terms of activity levels.
レコメンデーション・プラットフォームにやってくるユーザーは、活動レベルにおいて異質である(??).
Some users visit the platform occasionally, while others visit the platform more regularly and consistently.
たまに訪れるユーザもいれば、定期的かつコンスタントに訪れるユーザーもいる.
The long-term goal of a recommendation platform is to not only satisfy the user’s need in the current session, but ideally to see them return to the recommendation platform more often in the future.
推薦プラットフォームの長期的な目標は、**現在のセッションでユーザのニーズを満たすだけでなく、将来的にユーザがより頻繁に推薦プラットフォームを訪れるようになること**が理想的である.

We would like to see if adding exploration in the recommendation has any effect on moving user activity levels.
**レコメンデーションに探索を加えることで、ユーザのアクティビティレベルを動かす効果があるかどうか**を確認したいと思う.
We define four user activity levels in terms of how many days they are active on the platform in a 2-week period, which is shown in Fig 5a.
図5aに示すように、**2週間のうち何日プラットフォーム上で活動しているかという観点から、4つのユーザ活動レベルを定義**している.
For example, a user being casual means that he/she has been active for 1 to 4 days in the last 14 days. Users can become more active or less active depending their experience on the platform as well as exogenous factors not control by recommendation. Suppose the goal of a recommendation platform is moving casual users to become core users. An intuitive way to measure the conversion is by counting the number of users who start off casual, and end up core. This can be realized with a user activity level transition matrix, which measures the movement between different user activity levels.
例えば、カジュアルなユーザとは、過去14日間のうち1～4日間アクティブであったことを意味する.
ユーザは、プラットフォームでの経験や、レコメンデーションではコントロールできない外的要因によって、よりアクティブになったり、よりアクティブでなくなったりすることがある.
あるレコメンデーション・プラットフォームのゴールが、カジュアルユーザをコアユーザ に移行させることだとする. 
この conversion を測定する直感的な方法は、**カジュアルユーザからコアユーザ になったユーザの数を数えること**である.
これは、異なるユーザーの活動レベル間の移動を測定する、**ユーザの活動レベル遷移行列(user activity level transition matrix)**で実現できる.

We examine user activity level before the experiment start date and at the end of the experiment for every treatment group to compute the transition matrix, and compare with control.
実験開始日前と実験終了時のユーザの活動量をtreatment群ごとに調べて遷移行列を計算し、control群と比較する.
Figure 5b shows the percentage difference of the transition matrices between the actionable representation treatment group and control.
図5bは、アクショナブル表現処理グループ(treatment群の一つ )とcontrolの遷移行列 の**差の割合**である.
We see that there is a significant increase in casual-to-core conversion rate.
カジュアルからコアへの変換率が大きく上昇していることがわかる.
This suggests that a successful exploration strategy can result in a desired user movement as less active users are becoming more engaged on the platform.
これは、**探索戦略が成功すると、あまりアクティブでないユーザがプラットフォーム上でより熱心になるため、望ましいユーザの動きになることを示唆している**.

# 8. Conclusion 結論

We present a systemic study to understand the values of exploration in recommender systems beyond reducing model uncertainty.
我々は、推薦システムにおける探索の価値を、モデルの不確実性の低減を超えて理解するための体系的な研究を発表する.
We examine different user exploration strategies in affecting the four facets of recommendation quality, i.e., accuracy, diversity, novelty and serendipity, that contribute directly to user experience on the platform.
我々は、推薦品質（正確性、多様性、新規性、セレンディピティ）の4つの側面、すなわち、推薦プラットフォームにおけるユーザ体験に直接貢献するユーザ探索戦略について、様々な角度から検証する.
We showcase exploration strategies that oriented toward discovering unknown user interests in positively influencing user experience on recommendation platforms.
我々は、**未知のユーザの興味を発見することに重点を置いた探索戦略が、推薦プラットフォームにおけるユーザ体験にポジティブな影響を与える**ことを紹介する.
Using conversion of casual users to core users as an indicator of the holistic long term user experience, we connects serendipity to improved long term user experience.
また、カジュアルユーザからコアユーザへの転換率を指標として、セレンディピティを長期的なユーザー体験の向上につなげている.
We believe these are important first steps in understanding and improving exploration and serendipity in (RL based) recommender systems, and providing foundation for future effort in this direction.
これらは、(RLベースの)推薦システムにおける探索とセレンディピティを理解し、改善するための重要な第一歩であり、この方向での将来の努力に基礎を提供するものであると信じている.
