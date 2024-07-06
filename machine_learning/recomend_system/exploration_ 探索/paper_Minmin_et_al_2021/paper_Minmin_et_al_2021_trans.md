## 0.1. refs: refs：

https://dl.acm.org/doi/pdf/10.1145/3460231.3474236
[empty]

## 0.2. title タイトル

Values of User Exploration in Recommender Systems
推薦システムにおけるユーザ探索の価値

## 0.3. abstract 抄録

Reinforcement Learning (RL) has been sought after to bring nextgeneration recommender systems to further improve user experience on recommendation platforms.
強化学習(RL)は、レコメンデーションプラットフォームにおけるユーザーエクスペリエンスをさらに向上させる次世代のレコメンデーションシステムを実現するために注目されている。
While the exploration-exploitation tradeoff is the foundation of RL research, the value of exploration in (RL-based) recommender systems is less well understood.
探索と利用のトレードオフはRL研究の基礎であるが、（RLベースの）レコメンダーシステムにおける探索の価値はあまり理解されていない。
Exploration, commonly seen as a tool to reduce model uncertainty in regions of sparse user interaction/feedback, is believed to cost user experience in the short term, while the indirect benefit of better model quality arrives at a later time.
探索は、一般的に、ユーザーとのインタラクションやフィードバックが疎な領域でモデルの不確実性を低減するためのツールと考えられているが、短期的にはユーザーエクスペリエンスを犠牲にすると考えられている。
We focus on another aspect of exploration, which we refer to as user exploration to help discover new user interests, and argue it can improve user experience even in the more imminent term.
我々は、**新しいユーザの興味を発見するための user exploration (ユーザ探索) と呼ばれる探索のもう一つの側面に焦点を当て、それがユーザーエクスペリエンスをより即座に改善できると主張する**。

We examine the role of user exploration in changing different facets of recommendation quality that more directly impact user experience.
我々は、ユーザ体験に直接影響を与える推薦品質の異なる側面を変化させるユーザ探索の役割を検証する。
To do so, we introduce a series of methods inspired by exploration research in RL to increase user exploration in an RL-based recommender system, and study their effect on the end recommendation quality, more specifically, on accuracy, diversity, novelty and serendipity.
そのために、RLベースの推薦システムにおいてユーザの探索性を高めるために、RLにおける探索研究にインスパイアされた一連の手法を導入し、最終的な推薦品質、より具体的には精度、多様性、新規性、セレンディピティに対する効果を研究する。
We propose a set of metrics to measure (RL based) recommender systems in these four aspects and evaluate the impact of exploration-induced methods against these metrics.
これらの4つの側面から（RLベースの）レコメンダーシステムを評価するためのメトリクスセットを提案し、これらのメトリクスに対する探索誘発手法の影響を評価する。
In addition to the offline measurements, we conduct live experiments on an industrial recommendation platform serving billions of users to showcase the benefit of user exploration.
オフラインでの測定に加え、数十億のユーザーにサービスを提供する産業用レコメンデーション・プラットフォームでライブ実験を行い、ユーザ探索の利点を紹介する。(オンライン実験もやってるんんだ...!:thinking_face:)
Moreover, we use conversion of casual users to core users as an indicator of the holistic long-term user experience and study the values of user exploration in helping platforms convert users.
**さらに、カジュアルユーザからコアユーザへの転換を総合的な長期的ユーザ体験の指標とし、プラットフォームがユーザを転換させるためのユーザ探索の価値を研究する。**
Through offline analyses and live experiments, we study the correlation between these four facets of recommendation quality and long term user experience, and connect serendipity to improved long term user experience.
オフライン分析およびライブ実験を通じて、推薦品質のこれら4つの側面と長期的なユーザー・エクスペリエンスとの相関関係を研究し、セレンディピティを長期的なユーザー・エクスペリエンスの向上につなげている。

# 1. Information インフォメーション

In the era of increasing choices, recommender systems are becoming indispensable in helping users navigate the million or billion pieces of contents available on recommendation platforms.
選択肢が増える時代において、レコメンデーション・システムは、レコメンデーション・プラットフォーム上で利用可能な百万、億単位のコンテンツをユーザーがナビゲートするのに不可欠なものとなっている。
These systems are built to satisfy users’ information needs by anticipating what they would be interested in consuming next.
これらのシステムは、ユーザが次に何を消費したいと思うかを予測することで、ユーザの情報ニーズを満たすように構築されている。
Collaborative filtering [28, 47] and supervised learning based approaches predicting users’ immediate response toward recommendations [12, 65] such as clicks, dwell time, likes, have had enormous successes.
協調フィルタリング[28, 47]や、推奨に対するユーザーのimmediate response(即時反応)[12, 65]（クリック、滞在時間、「いいね！」など）を予測する教師あり学習ベースのアプローチは、大きな成功を収めている。
Researchers however are becoming increasingly aware of the limitations of such approaches.
**しかし研究者たちは、そうしたアプローチの限界をますます認識しつつある。**
First, focus on driving short-term engagements such as user clicks fails to account for the long term impact of a recommendation.
第一に、ユーザーのクリックなどの短期的なエンゲージメントを促進することに焦点を当てると、推薦の長期的な影響を考慮することができない。
Second, lack of exploration causes these systems to increasingly concentrate on the known user interests and create satiation effect, i.e., reduced enjoyment of the content.
第二に、探究心の欠如により、これらのシステムは既知のユーザの興味にますます集中し、飽和効果、すなわちコンテンツの楽しみの減少を引き起こす。

Reinforcement learning (and bandits) techniques have emerged as appealing alternatives [11, 23, 67, 68] over the years.
強化学習（およびバンディット）技術は、長年にわたって魅力的な選択肢として浮上してきた[11, 23, 67, 68]。
Compared with supervised learning based approaches, RL offers two advantages: 1) Exploration.
教師あり学習に基づくアプローチと比較して、RLには2つの利点がある： 1）探索。
(Online) RL algorithms inherently explore regions they are less certain about.
(オンライン）RLアルゴリズムは、本質的に確信の持てない領域を探索する。
This provides a natural mechanism to deviate from the current system behavior, and introduce previously unseen contents to users; 2) Long-term user experience optimization.
2）長期的なユーザー体験の最適化。
As the planning horizon of these RL agents extends, the recommender naturally shifts its focus from short-term user engagement toward optimizing the long-term user experience on the platform.
これらのRLエージェントの計画地平が広がるにつれて、**レコメンダーは短期的なユーザーエンゲージメントから、プラットフォーム上での長期的なユーザーエクスペリエンスの最適化へと自然に焦点を移していく**。
We focus our discussion on exploration, though as we show in the analyses it innately connects to the long-term user experience.
分析で示したように、探索は長期的なユーザー体験につながるものである。

The tradeoff between exploration and exploitation is central to the design of RL agents [17, 57].
探索と搾取のトレードオフは、RLエージェントの設計の中心である[17, 57]。
An agent learns to form a policy to maximize returns in a changing environment by taking actions and receiving reward/feedback from the environment.
エージェントは、環境から報酬やフィードバックを受けながら行動を起こすことで、変化する環境の中でリターンを最大化するための方針を立てることを学習する。
The agent is incentivized to exploit, repeating actions taken in the past that produced higher rewards, to maximize reward.
エージェントは、報酬を最大化するために、より高い報酬をもたらした過去の行動を繰り返し、exploit(搾取, 活用??)することを奨励される。
On the other hand, the agent needs to explore previously unseen actions in order to discover potentially better options.
一方、エージェントは、より良い選択肢を発見するために、以前に見たことのない行動を探索する必要がある。
Exploration in RL based recommender systems serves a similar goal, that is to expose users to previously unseen items to discover contents the user is potentially interested in.
RLベースのレコメンダーシステムにおける探索は、ユーザーが潜在的に興味を持っているコンテンツを発見するために、未見のアイテムにユーザーをさらすという同様の目的を果たす。
The benefit of exploration to counter the selection bias of existing systems and generate training data to reduce model uncertainty has been established [11].
既存のシステムの選択バイアスに対抗し、モデルの不確実性を低減するためのトレーニングデータを生成するための探索の利点は、確立されている[11]。(この記述は、OPEやOPLの観点で探索は利点があるよってことだよね...!:thinking_face:)
Here we focus on another aspect of exploration that we refer to as user exploration, i.e., exploration for discovering something new for the user.
ここでは、探索のもう一つの側面であるユーザ探索、つまりユーザにとって新しい何かを発見するための探索に焦点を当てる。

As exploration innately leads to recommending something less pertinent to the known user interests, it is often seen as a cost to user experience, especially in the short term.
**探索は生来、既知のユーザーの興味にあまり適切でないものを推薦することにつながるため、特に短期的には、ユーザー・エクスペリエンスに対するコストと見なされることが多い。**
Here we argue that recommender systems have an inherent need for exploration as users perceive other factors of recommendation quality besides accuracy [5, 66].
ここで我々は、**推薦システムは、ユーザが正確さ以外の推薦品質の要因を知覚するため、本質的に探索の必要性がある**と主張する[5, 66]。
We dissect the values of user exploration by examining its role in changing different aspects of recommendation quality that impact the user experience on recommendation platforms.
レコメンデーション・プラットフォームにおけるユーザー・エクスペリエンスに影響を与えるレコメンデーション・クオリティの様々な側面を変化させる役割を検証することで、ユーザー・エクスプロレーションの価値を解剖する。
Together, we make the following contributions: • Methods to Introduce User Exploration: We introduce a collection of methods, inspired by exploration research in RL, to improve user exploration in recommender systems.
併せて、我々は以下の貢献を行う： - **ユーザ探索を導入する方法 推薦システムにおけるユーザ探索を改善するために、RLにおける探索研究に触発された手法を紹介する**。(exploitionのみの決定的な推薦システムに、explorationを導入する手法...!:thinking_face:)
• Metrics: We propose a set of metrics measuring the different aspects of recommendation quality, that is accuracy, diversity, novelty and serendipity for RL based recommender systems.

- メトリクス RLベースの推薦システムにおいて、推薦品質の異なる側面、すなわち正確性、多様性、新規性、セレンディピティを測定する一連のメトリクスを提案する。
  • Offline Analyses: We conduct an extensive set of offline analyses to understand the values of user exploration in changing the four aspects of recommendation quality.
- オフライン分析 我々は、推薦品質の4つの側面を変化させるユーザ探索の価値を理解するために、広範なオフライン分析を実施する。
  • Live Experiments: We conduct live experiments of the proposed methods on a commercial recommendation platform serving billions of users and millions of items, and showcase the value of user exploration in improving long-term user experience on the platform.
- ライブ実験： 数十億のユーザーと数百万のアイテムを提供する商用推薦プラットフォーム上で提案手法のライブ実験を行い、プラットフォーム上の長期的なユーザー体験を改善するためのユーザー探索の価値を示す。
  • Serendipity for Long Term User Experience: Through offline analyses and live experiments, we study the correlation between these four aspects of recommendation quality and the long term user experience.
- 長期的なユーザー体験のためのセレンディピティ： オフライン分析とライブ実験を通じて、**推薦品質のこれら4つの側面と長期的なユーザー・エクスペリエンスとの相関関係を研究する**。
  Using conversion of casual users to core users as an indicator of the holistic long term user experience, we connect serendipity to improved long term user experience.
  **カジュアルユーザからコアユーザへの転換を総合的な長期的ユーザ体験の指標とすること**で、セレンディピティを長期的ユーザー体験の向上につなげている。

# 2. Related Work 関連作品

## 2.1. Reinforcement Learning for Recommender Systems.

推薦システムのための強化学習.
Deep reinforcement learning, combining high-capacity function approximators, i.e., deep neural networks, with the mathematical formulations in classic reinforcement learning [57], has achieved enormous success in various domains such as games, robotics and hardware design [18, 33, 36, 52].
ディープ強化学習は、大容量の関数近似器、すなわちディープニューラルネットワークを古典的な強化学習の数学的定式化[57]と組み合わせたもので、ゲーム、ロボット工学、ハードウェア設計などの様々な領域で大きな成功を収めている[18, 33, 36, 52]。
It has attracted a lot of attention from the recommeder system research community as well.
レコメンダーシステムの研究コミュニティからも注目を集めている。
Shani et al.[51] were among the first to formally formulate recommendation as a Markov decision process (MDP) and experiment with model-based RL approaches for book recommendation.
Shaniら[51]は、推薦をマルコフ決定過程(MDP)として正式に定式化し、書籍推薦のためのモデルベースRLアプローチを実験した最初の人々の一人である。
Zheng et al.[70] applied DQN for news recommendation.
Zhengら[70]はニュース推薦にDQNを適用した。
Dulac-Arnold et al.[14] enabled RL in problem spaces with a large number of discrete actions and showcased its performance on various recommendation tasks with tens of thousands of actions.
Dulac-Arnoldら[14]は、離散的なアクションの数が多い問題空間でのRLを可能にし、数万アクションの様々な推薦タスクでの性能を示した。
Liu et al.[34] tested actor-critic approaches on recommendation datasets such as MovieLens, Yahoo Music and Jester.
Liuら[34]は、MovieLens、Yahoo Music、Jesterなどの推薦データセットで俳優批評アプローチをテストした。
Set recommendation using RL has been studied in [11, 23, 69].
RLを用いたセット推薦については、[11, 23, 69]で研究されている。
In recent years, we also start seeing success of RL in real-world recommendation applications.
近年、RLは実世界の推薦アプリケーションでも成功を収め始めている。
Chen et al.[11] scaled a batch RL algorithm, i.e., REINFORCE with off-policy correction to a commercial platform serving billions of users and tens of millions of contents.
**Chenら[11]は、数十億のユーザーと数千万のコンテンツにサービスを提供する商用プラットフォームに、バッチRLアルゴリズム、すなわちオフポリシー補正を伴うREINFORCEをスケーリングした。**
Hu et al.[22] tested an extension of the deep deterministic policy gradient (DDPG) method for learning to rank on Taobao, a commercial search platform.
Huら[22]は、淘宝網（Taobao）という商業的な検索プラットフォームで、ランク付けを学習するための深層決定性政策勾配（DDPG）法の拡張をテストした。

## 2.2. Exploration in Reinforcement Learning.

強化学習における探索。
The exploration/exploitation dilemma has long been studied in multi-armed bandits and classic reinforcement learning [17, 57].
探索／搾取のジレンマは、多腕バンディットや古典的な強化学習で長い間研究されてきた[17, 57]。
Exploration methods are concerned with reducing agents’ uncertainty of the environment reward and/or the dynamics.
探索手法は、エージェントの環境報酬やダイナミクスの不確実性を低減することに関係する。
For the stochastic bandits problems, Upper Confidence Bound (UCB) [30] and Thompson Sampling (TS) [4, 10, 59] are among the most well known techniques with both theoretical guarantees and empirical successes.
確率的バンディッツ問題では、UCB(Upper Confidence Bound)[30]とTS(Thompson Sampling)[4,10,59]が理論的保証と経験的成功の両方を持つ最もよく知られた手法の一つである。
In classic reinforcement learning with tabular settings, count-based exploration techniques quantifying the uncertainty based on the inverse square root of the state-action visit count, can be seen as extension of these techniques to Markov Decision Processes (MDPs).
表形式設定の古典的な強化学習では、状態-行動訪問回数の逆平方根に基づいて不確実性を定量化する回数ベースの探索技法は、これらの技法をマルコフ決定過程（MDP）に拡張したものと見なすことができる。
Tang et al.[58] further generalizes counted-based methods to deep RL with highdimensional state spaces.
Tangら[58]はさらに、計数ベースの手法を高次元の状態空間を持つ深層RLに一般化している。
Another camp of methods, commonly referred to as intrinsic motivation [21, 24, 48, 56], encourages the agents to explore regions leading up to surprises.
内発的動機づけ[21, 24, 48, 56]と一般的に呼ばれるもう1つの手法では、エージェントに驚きにつながる領域の探索を促す。
The surprise factor is often measured by the agents’ predictive errors on environment reward or dynamics, or equivalently information gain the agents can acquire by taking an action under the current state.
サプライズ要素は、多くの場合、エージェントの環境報酬やダイナミクスの予測誤差、あるいは現在の状態下で行動を起こすことによって得られる情報利得によって測定される。
Bellemare et al.[6] unifies count-based exploration and intrinsic motivation through the lens of information gain or learning progress.
Bellemareら[6]は、情報獲得や学習の進歩というレンズを通して、カウントに基づく探索と内発的動機づけを統合している。
Our work takes inspiration from these existing works, and re-designs the algorithms to fit more closely with the recommendation setup.
我々の研究は、これらの既存の作品からインスピレーションを受け、より推薦の設定に合うようにアルゴリズムを再設計している。

## 2.3. Diversity, Novelty and Serendipity of Recommender Systems. 推薦システムの多様性、新規性、セレンディピティ。

While early recommendation research has focused almost exclusively on improving recommendation accuracy, it has become increasingly recognized that there are other factors of recommendation quality contributing to the overall user experience on the platform.
初期のレコメンデーション研究では、レコメンデーションの精度を向上させることだけに焦点が当てられていたが、**レコメンデーションの品質には、プラットフォーム上でのユーザ体験全体に貢献する他の要因がある**ことが次第に認識されるようになってきた。
Herlocker et al.[19] in their seminal work of evaluating collaborative filtering based recommender systems defined various metrics to measure recommendation accuracy, coverage, novelty as well as serendipity.
Herlockerら[19]は、協調フィルタリングベースの推薦システムを評価する代表的な研究で、推薦精度、カバー率、新規性、セレンディピティを測定する様々な指標を定義した。
Diversity is another important aspect that has been extensively studied [3, 5].
多様性もまた、広く研究されてきた重要な側面である[3, 5]。
Diversification algorithms are used to increase coverage of the full range of user interests, and to counter the saturation effect of consuming similar contents [72].
多様化アルゴリズムは、ユーザーの興味の全範囲のカバレッジを高め、類似したコンテンツを消費することによる飽和効果に対抗するために使用される[72]。
Zhou et al.[71] studied the dilemma between accuracy and diversity, and proposed a hybrid approach to balance the two.
Zhouら[71]は、精度と多様性の間のジレンマを研究し、2つのバランスをとるためのハイブリッドアプローチを提案した。
Novelty [8] is closely related to long tail recommendation [62], measuring the capacity of the recommender systems to make predictions and reach the full inventory of contents available on the platforms.
新規性[8]はロングテール推薦[62]と密接に関連しており、推薦システムが予測を行い、プラットフォーム上で利用可能なコンテンツの全在庫に到達する能力を測定する。
One of the early definitions of serendipity was introduced in [19], which captures the degree to which a recommendation is both relevant and surprising to users.
セレンディピティの初期の定義の一つは[19]で紹介されたもので、推薦がユーザーにとって適切であると同時に驚くべきものである度合いを捉えている。
Zhang et al.[66] proposed a hybrid rank-interpolation approach to combine outputs of three LDA algorithms [7] focusing on either accuracy, diversity or serendipity to achieve a balance between these factors in the end recommendations.
Zhangら[66]は、精度、多様性、セレンディピティのいずれかに焦点を当てた3つのLDAアルゴリズム[7]の出力を組み合わせるためのハイブリッドランク補間アプローチを提案し、最終的な推薦においてこれらの要素のバランスを実現する。
Oku and Hattori [41] proposed a fusion based technique to mix items users expressed interest on based on item attributes in order to introduce serendipitous contents.
奥・服部[41]は、セレンディピティコンテンツを導入するために、アイテムの属性に基づいてユーザが興味を示したアイテムをミックスするフュージョンベースの手法を提案した。
Our work measures the effect of exploration on recommendation accuracy, diversity, novelty and serendipity, and connects these factors to long term user experience.
我々の研究は、**探索(ここではユーザ探索?)が推薦精度、多様性、新規性、セレンディピティに与える影響を測定**し、これらの要素を長期的なユーザー体験に結びつける。

<!-- ここまで読んだ! -->

# 3. Background 背景

We base our work on the REINFORCE recommender system introduced in [11], in which the authors framed a set recommendation problem as a Markov Decision Process (MDP) (S, A, P, R, ρ0,γ ).
私たちは[11]で紹介されたREINFORCE推薦システムをベースにしており、著者たちは**セット推薦問題**(=k個のアイテムをおすすめする問題...!)をマルコフ決定過程（MDP）$(S, A, P, R, \rho_0, \gamma)$としてフレーム化した。
Here S is the state space capturing the user interests and context, A is the discrete action space containing items available for recommendation, P : S × A × S → R is the state transition probability, and R : S × A → R is the reward function, with r(s, a) note the immediate reward of action a under state s.
ここで、$S$ はユーザの関心や文脈を表す状態空間(=特徴量空間??)、 $A$ は推薦可能なアイテムを含む**離散的なアクション空間**、 $P : S \times A \times S \rightarrow \mathbb{R}$ は状態遷移確率(=3つの変数の同時確率?)、 $R : S \times A \rightarrow \mathbb{R}$ は報酬関数(=2つの変数の同時確率?)であり、$r(s, a)$ は状態$s$の下でのアクション$a$の即時報酬を示す。
ρ0 is the initial state distribution, and γ the discount for future rewards.
$\rho_0$ は初期状態分布、$\gamma$ は将来の報酬の割引率である（=将来の報酬が現在の報酬よりもどの程度価値が低いかを表現したもの）。
Let Ht = {(A0, a0,r0), · · · , (At−1, at−1,rt−1)} denote an user’s historical activities on the platform up to time t, where At ′ stands for the set of items recommended to the user at time t ′ , at ′ denotes the item the user interacted with at t ′ (at ′ can be null), and rt ′ captures the user feedback (reward) on at ′ (rt ′ = 0 if the user did not interact with any item in At ′).
＄H*{t} = \{(A*{0}, a*{0}, r*{0}), \cdots, (A*{t-1}, a*{t-1}, r*{t-1})\}$ は、時刻$t$までのプラットフォーム上でのユーザの過去の活動を示し、$A*{t}'$ は時刻$t'$にユーザに推薦されたアイテムのセットを表し、$a_{t}'$ は$t'$でユーザが相互作用したアイテムを示し（$a_{t}'$ がnullの場合がある）、$r_{t}'$ は$a_{t}'$に対するユーザのフィードバック（報酬）を捉える（$a_{t}'$に対してユーザが何もアクションを起こさなかった場合、$r_{t}' = 0$）。
The history Ht is encoded through a recurrent neural network to capture the latent user state, that is, ust = RNNθ (Ht ).
履歴 $H_{t}$ は、潜在的なユーザーの状態、すなわち $u_{st} = RNN_{\theta}(H_{t})$ を捉えるために、再帰ニューラルネットワークを用いてエンコードされる。(u_stは、ユーザの過去の行動履歴を埋め込んだもの...??)
Given the latent user state, a softmax policy over the item corpus A is parameterized as
潜在的なユーザの状態が与えられた場合、アイテムコーパスA上のソフトマックスポリシーは以下のようにパラメータ化される:

$$
\pi_{\theta}(a|s_{t}) = \frac{\exp(u_{st}^{T}v_{a})}{\sum_{a' \in A} \exp(u_{st}^{T}v_{a'})}, \forall a \in A
\tag{1}
$$

which defines a distribution over the item corpus A conditioning on the user state st at time t.
これは、時刻tにおけるユーザ状態stを条件とするアイテムコーパスA上の分布を定義している。(=ユーザ状態s*tで条件づけた行動の確率分布関数)
Here va stands for the embedding of the item a.
ここで $v*{a}$ はアイテム$a$の埋め込みを表す。
The agent then generates a set of recommendation At to user at time t according to the learned softmax policy πθ (·|st ).
次に、エージェントは、学習されたソフトマックスポリシー $\pi_{\theta}(-|s_{t})$ に従って、時刻$t$にユーザに推薦するアイテムのセット $A_{t}$ を生成する。
The policy parameters θ are learned using REINFORCE [60] so as to maximize the expected cumulative reward over the user trajectories,
**ポリシーのパラメータθは、ユーザの軌跡に対する期待累積報酬を最大化するように**、REINFORCE [60]を用いて学習される。

$$
\max_{\theta} J(\theta_{\theta})
= \mathbb{E}_{s_0 \sim \rho_{0}, a_{t} \sim \pi_{\theta}(-|s_{t})} \left[ \sum_{t=0}^{T} r(s_{t}, a_{t}) \right]
\\
\tag{2}
$$

where Rt = Ir(st ,at )>0 · ÍT t ′=t γ t ′−t r(st ′, at ′) is the discounted cumulative reward starting from time t.
ここで、 $R_{t} = I_{t}(s_{t}, a_{t}) > 0 \cdot \sum_{t' = t}^{T} \gamma^{t' - t} r(s_{t'}, a_{t'})$ は、時刻 $t$ から始まる割引累積報酬である。
RL was designed as an online learning paradigm in the first place [57].
**RLはそもそもオンライン学習のパラダイムとして設計された**[57]。
Note that the expectation in eq.2 is taken over the trajectories generated according to the learned policy, and d πθ t (s) is the discounted state visitation probability under πθ [32].
なお、式2の期待値は、学習されたポリシーに従って生成された軌跡に対して取られ、$d_{\pi_{\theta}}(s)$ は $\pi_{\theta}$ のもとでの割引後の状態訪問確率である[32]。
One of the main contribution of [11] is bringing the REINFORCE algorithm to the offline batch learning setup commonly deployed in industrial recommender systems.
[11]の主な貢献の一つは、REINFORCEアルゴリズムを、**産業用推薦システムで一般的に導入されているオフラインバッチ学習のセットアップに導入したこと**である。
(RLは元々オンライン学習のparadimだったのに、それを実践しやすいオフラインバッチ学習として使えるようにしたってことか...!：thinking_face:)
The authors applied a first-order approximation [2] of importance sampling to address the distribution shift caused by offline training, resulting in a gradient of the following:
著者らは、オフライン学習によって引き起こされる分布シフトに対処するために、重要度サンプリングの一次近似[2]を適用し、以下の勾配を得た。

$$
\Delta_{\theta} J(\pi_{\theta}) = \mathbb{E}_{s \sim d_{\beta_{t}}, a \sim \pi_{\theta}} \left[ \frac{\pi_{\theta}(a|s)}{\beta_{t}(a|s)} \nabla_{\theta} \log \pi_{\theta}(a|s) \cdot R_{t} \right]
$$

Here β(·|s) denotes the behavior policy, i.e., the action distribution conditioning on state s in the batch collected trajectories.
ここで、 $\beta(-|s)$ は、バッチ収集された軌跡における状態 $s$ に条件づけられたアクション分布、すなわち行動ポリシーを示す。
d β t (s) is the discounted state visitation probability under β.
d β t (s) は、βのもとでの割引後の状態訪問確率である。
This importance weight is further adapted to accommodate the set recommendation setup.
この重要度のウェイトは、セット推薦の設定に対応するようにさらに調整される。
We refer interested readers to [11] for more details.
詳細は[11]を参照されたい。

To balance exploration and exploitation, a hybrid approach that returns the top K ′ most probable items, while sampling the rest K −K ′ items according to πθ (Boltzmann exploration [13]), is employed during serving.
探索と利用をバランスさせるために、サービング中に、最も確率が高い上位K'個のアイテムを返す一方で、**残りのK-K'個のアイテムを $\pi_{\theta}$ に従ってサンプリングするハイブリッドアプローチ（ボルツマン探索[13]）が採用されている**。

<!-- ここまで読んだ! -->

# 4. Method メソッド

<!-- methodは一旦飛ばそう! -->

Here we introduce three simple methods inspired by exploration research in RL to increase user exploration in the REINFORCE recommender system during training.
ここでは、REINFORCEレコメンダーシステムにおいて、学習中にユーザの探索を増やすために、**RLにおける探索研究にヒントを得た3つの簡単な方法を紹介**する。
That is, to recommend content less pertinent to the known user interests, and to discover new user interests.
つまり、**既知のユーザーの興味にあまり関係のないコンテンツを推薦し、新しいユーザーの興味を発見すること**である。

## 4.1. Entropy Regularization エントロピー正則化

The first method promotes recommending contents less pertinent to the known user interests by encouraging the policy πθ (·|s) to have an output distribution with high entropy [61].
最初の方法は、ポリシーπθ (-|s)が高いエントロピーを持つ出力分布を持つように促すことで、既知のユーザの興味にあまり適切でないコンテンツを推薦することを促進する[61]。
Mnih et al.[38] observed that adding entropy of the policy to the objective function discourages premature convergence to sub-optimal deterministic policies and leads to better performance.
Mnihら[38]は、policyのエントロピーを目的関数に追加することで、最適でない決定論的なポリシーへの早期収束を抑制し、より良いパフォーマンスをもたらすことを観察した。
Pereyra et al.[46] conducted a systemic study of entropy regularization and found it to improve a wide range of state-of-the-art models.
Pereyraら[46]は、エントロピー正則化の体系的な研究を行い、エントロピー正則化が広範囲の最先端モデルを改善することを発見した。
We add of the entropy to the RL learning objective as defined in eq.2 during training.
式2で定義されるRLの学習目的に対して、学習時にエントロピーを追加する。
That is,
それはそうだ、

$$
\max_{\theta} J(\theta) + \alpha \sum_{s_{t} - d^{\beta}_{t}(s)}H(\pi_{\theta}(-|s_{t}))
\tag{4}
$$

where the entropy of the conditional distribution πθ (·|s) is defined as H (πθ (·|s)) = − Í a ∈A πθ (a|s) log πθ (a|s).
$\pi_{\theta}(-|s)$の条件付き分布のエントロピーは、$H(\pi_{\theta}(-|s)) = - \sum_{a \in A} \pi_{\theta}(a|s) \log \pi_{\theta}(a|s)$ と定義される。
Here α controls the strength of the regularization.
ここでαは正則化の強さを制御する。
The entropy is equivalent to the negative reverse KL divergence of the conditional distribution πθ (·|s) to the uniform distribution.
エントロピーは、一様分布に対する条件付き分布πθ (-|s)の負の逆KL発散と等価である。
That is, H (πθ (·|s)) = −DK L(πθ (·|s)||U ) + const, where U stands for a uniform distribution across the action space A.
つまり、$H(\pi_{\theta}(-|s)) = - D_{KL}(\pi_{\theta}(-|s)||U) + const$ であり、$U$ はアクション空間$A$全体にわたる一様分布を表す。
As we increase this regularization, it pushes the learned policy to be closer to a uniform distribution, thus promoting exploration.
この正則化を大きくすると、学習された方針がより一様分布に近くなり、探索が促進される。

(学習後の条件付きアクション確率分布がなめらかになる、みたいな感じっぽい...!)

## 4.2. Intrinsic Motivation and Reward Shaping 内発的動機づけと報酬の形成

The second method helps discovering new user interests through reward shaping.
2つ目の方法は、リワード・シェーピングを通じて新しいユーザーの興味を発見するのに役立つ。
The reward function r(s, a) as defined in eq.2, describes the (immediate) value of a recommendation a to a user s.
式2で定義される報酬関数r(s, a)は、ユーザーsに対する推薦aの（即時の）価値を記述する。
It plays a critical role in deciding the learned policy πθ .
これは、学習された方針πθを決定する上で重要な役割を果たす。
Reward shaping, transforming or supplying additional rewards beyond those provided by the MDP, is very effective in guiding the learning of RL agents to produce policies desired by the algorithm designers [1, 27, 40].
報酬シェーピングは、MDPが提供する報酬以外の報酬を変換したり供給したりするもので、アルゴリズム設計者が望む政策を生み出すようにRLエージェントの学習を導くのに非常に効果的である[1, 27, 40]。
Exploration has been extensively studied in RL [6, 42–44, 55], and has been shown to be extremely useful in solving hard tasks, e.g., tasks with sparse reward and/or long horizons, and .
探索はRLにおいて広く研究されており[6, 42-44, 55]、困難なタスク、例えば報酬がまばらなタスクや長いホリゾンを持つタスク、.NETを解く際に非常に有用であることが示されている。
These works can be roughly grouped into two categories.
これらの作品は大きく2つのカテゴリーに分類できる。
One concerns quantifying the uncertainty of the value function of the state-action pairs so the agent can direct its exploration on regions where it is most uncertain.
一つは、状態-行動ペアの価値関数の不確実性を定量化することで、エージェントが最も不確実性の高い領域の探索を指示できるようにすることである。
The other uses a qualitative notion of curiosity or intrinsic motivation to encourage the agent to explore its environment and learn skills that might be useful later.
もうひとつは、好奇心や内発的動機づけという定性的な概念を用いて、エージェントが環境を探索し、後で役に立つかもしれないスキルを学ぶように促すものだ。
Both camps of methods later adds an intrinsic reward r i (s, a), either capturing the uncertainty or curiosity to the extrinsic reward r e (s, a) that is emitted by the environment directly, to help the agent explore the unknown or learn new skills.
どちらの手法も、エージェントが未知を探索したり新しいスキルを学んだりするのを助けるために、環境から直接発せられる外在的報酬r e (s, a)に、不確実性や好奇心を捕らえた内在的報酬r i (s, a)を後から加える。
That is, transforming the reward function to
つまり、報酬関数を次のように変換する。

$$
\max_{\theta} J(\theta) + \alpha \sum_{s_{t} - d^{\beta}_{t}(s)}H(\pi_{\theta}(-|s_{t}))
\tag{4}
$$

where c controls the relative importance of the intrinsic reward w.r.t. the extrinsic reward emitted by the environment.
ここで、cは、環境から発せられる外発的報酬に対する内発的報酬の相対的な重要性を制御する。
Schmidhuber [49] formally captures the theory of creativity, fun and curiosity as an intrinsic desire to discover surprising patterns of the environment, and argues that a curiosity-driven agent can learn even in the absence of external reward.
Schmidhuber[49]は、創造性、楽しさ、好奇心の理論を、環境の驚くべきパターンを発見したいという内発的欲求として正式にとらえ、好奇心主導型のエージェントは、外部からの報酬がなくても学習できると主張している。
Our proposal bears the same principle by rewarding the agent more when it discovers some previously unknown patterns of the environment, that is the user.
我々の提案は、エージェントが環境（ユーザー）の未知のパターンを発見したときに、より多くの報酬を与えるという同じ原理を採用している。
Let R e t (st , at ) = Ir e (st ,at )>0 · ÍT t ′=t γ t ′−t r e (st ′, at ′) be the discounted cumulation of the extrinsic reward on the stateaction pair (st , at ) observed on the trajectory.

We then define the cumulative reward Rt (st , at ) used for the gradient update in eq.3 as
次に、式3の勾配更新に用いる累積報酬 Rt (st , at ) を次のように定義する。


Here c > 1 is a constant multiplier.
ここでc > 1は定数倍である。
As explained in Section 3, the agent perceives the environment, that is the user interests and context, through encoding user’s historical activities Ht = {(A0, a0,r0), · · · , (At−1, at−1,rt−1)}.
セクション3で説明したように、エージェントは、ユーザの履歴 Ht = {(A0, a0,r0), - - , (At-1, at-1,rt-1)} を符号化することにより、環境、つまりユーザの興味とコンテキストを認識する。
One can imagine a large update (surprise) to the agent’s modeling of the environment if an item at recommended given the state st is 1) drastically different from any of the items the user interacted with in the past; 2) enjoyed by the user, i.e., r e (st , at ) or R e (st , at ) is high.
もし状態stが与えられたときに推奨されるアイテムが、1)ユーザが過去にやりとりしたアイテムのどれとも大きく異なる、2)ユーザが楽しんでいる、つまりr e (st , at )またはR e (st , at )が高い場合、エージェントの環境モデリングが大きく更新される（サプライズ）ことが想像できる。
These two conditions, surprise and relevance, align with the serendipity metrics we are going to detail in Section 5.5.To measure the surprise of at , we define It = {at ′, ∀t ′ < t and rt ′ > 0} as the set of items the user interacted with up to time t.
atの驚きを測定するために、我々はIt = {at ′, ∀t ′ < t and rt ′ > 0}を時間tまでにユーザーが相互作用したアイテムのセットと定義する。
As recommendation items are often associated with various attributes as described in Section 5.1, we use these attributes to measure the similarity (or difference) of a candidate action at towards It .
セクション5.1で述べたように、推薦項目は様々な属性と関連していることが多いので、これらの属性を用いて、It に対する候補行動の類似度（または相違度）を測定する。
For example, we consider an item at surprising (different) if its topic cluster is different from any of the items in It .
例えば、トピック・クラスタが It 内のどのアイテムとも異なる場合、そのアイテムは意外性がある（異なる）と考える。
The multiplicative design in eq.6 naturally accomplishes the second condition, that is, relevance.
式.6の乗法設計は、2番目の条件、つまり関連性を自然に達成する。
Comparing with the additive form (eq.5), the multiplicative design results in: 1) a candidate action at with zero extrinsic reward, i.e., R e t (st , at ) = 0 will NOT receive any additional reward even if being under-surfaced; 2) an action at receiving higher extrinsic reward R e t (st , at ) will be rewarded even more compared with those that are equally surprising but received lower extrinsic reward.
加法形式（式5）と比較すると、乗法設計の結果は以下のようになる： 1) 外在的報酬がゼロの候補行動at、すなわちR e t (st , at ) = 0は、たとえアンダーサーフェスであっても追加報酬を受け取らない。2) 外在的報酬R e t (st , at ) が高い候補行動atは、同じように驚くが外在的報酬が低い候補行動と比較して、さらに報酬が高くなる。
This contrasts with the additive form where the extrinsic rewards observed does not influence the intrinsic reward.
これは、観察された外発的報酬が内発的報酬に影響を与えない加算型とは対照的である。
In other words, the additive design gives a uniform boost to actions based entirely on surprise.
言い換えれば、この加算設計は、不意打ちに基づく行動を一律に後押しする。
The multiplicative design on the other end, favors surprising actions that actually lead to improved user experience, indicated by higher extrinsic reward.
もう一方の乗法的デザインは、より高い外発的報酬によって示される、ユーザー体験の向上に実際につながる意外な行動を好む。

## 4.3. Actionable Representation for Exploration 探索のための実用的な表現

The third method reinforces the newly discovered user interest through representation learning.
第3の方法は、表現学習によって新たに発見されたユーザーの興味を強化する。
Learning effective representation is critical to improve the sample efficiency of many machine learning algorithms, and RL is no exception.
多くの機械学習アルゴリズムのサンプル効率を向上させるためには、効果的な表現を学習することが重要であり、RLも例外ではない。
Most prior work on representation learning for RL has focused on generative approaches, learning representations that capture all underlying factors of variation in the observation space in a more disentangled or well-ordered manner.
RLのための表現学習に関する先行研究のほとんどは、生成的なアプローチに焦点を当てており、観測空間における変動のすべての根本的な要因を、よりばらばらに、あるいは整然とした方法で捉える表現を学習してきた。
Self-supervised learning [20, 25, 50, 54] to capture the full dynamics of the environment has also attracted a lot of attentions lately.
環境のダイナミクスを完全に把握するための自己教師付き学習[20, 25, 50, 54]も、最近注目を集めている。
Ghosh et al.[16] instead argue to learn functionally salient representations: representations that are not necessarily complete in terms of capturing all factors of variation in the observation space, but rather aim to capture those factors of variation that are important for decision making – that are "actionable." The REINFORCE agent introduced in Section 3 describes the environment, i.e., the user, through encoding his/her historical activities Ht .
Ghoshら[16]は、代わりに機能的に顕著な表現を学習することを主張する： この表現は、観測空間における全ての変動要因を捉えるという点では必ずしも完全ではなく、むしろ意思決定にとって重要な変動要因、つまり 「行動可能な 」変動要因を捉えることを目的としている。セクション3で紹介するREINFORCEエージェントは、環境、すなわちユーザーを、彼の過去の活動Htを符号化することで記述する。
That is, ust = RNNθ (Ht ).
つまり、ust = RNNθ（Ht ）である。
When an user interacted with a surprising item at (to the agent) and gave high reward, the user state ust should be updated to capture the new information so the agent can act differently next.
ユーザが（エージェントにとって）驚くようなアイテムとインタラクトし、高い報酬を与えたとき、エージェントが次に異なる行動を取れるように、ユーザの状態は新しい情報を取り込むために更新されなければならない。
That is, to make recommendations according to the newly acquired information about the new interest of the user.
つまり、ユーザーの新たな興味について新たに得た情報に従って推薦を行うことである。
To aid the agent in capturing this information in its state, we extend Ht with an additional bit, indicating whether or not an item the user interacts with is surprising and relevant.
エージェントがこの情報を状態に取り込むのを助けるために、我々はHtを追加ビットで拡張し、ユーザが相互作用したアイテムが驚きと関連性があるかどうかを示す。
That is, we expand Ht = {(A0, a0,r0,i0), · · · , (At−1, at−1,rt−1,it−1)}, where it ′ = 1 if 1) the attribute of at (such as topic cluster) is different from that of any items in It ′ (being a surprise) and; 2) rt > 0 (being relevant).
つまり、Ht＝{(A0,a0,r0,i0), - - , (At-1, at-1,rt-1,it-1)} と展開し、1)atの属性(トピック・クラスターなど)がIt′内のどのアイテムの属性とも異なる(サプライズである)、2)rt＞0(関連性がある)場合、it′＝1とする。
Here It ′ is the list of items the user has interacted with up to time t ′ .
ここで、It ′は、時刻t ′までにユーザが相互作用した項目のリストである。
This feature is then embedded and consumed by the RNN along with other features describing the item at .
この特徴は、.NETのアイテムを説明する他の特徴とともにRNNに埋め込まれ、消費される。

# 5. Measurement 測定

<!-- Methodは一旦飛ばしてここから読む! -->

<!-- 推薦システムの良し悪しを評価するための指標の設計のセクション?? -->

Personalization has been the cornerstone of modern recommender systems.
パーソナライゼーションは、現代のレコメンダーシステムの基礎となっている。
It aims to produce targeted and accurate recommendations based on user historical activities.
これは、ユーザーの過去のアクティビティに基づいて、ターゲットを絞った正確なレコメンデーションを作成することを目的としている。
Overly focusing on the accuracy aspect of recommendation, however, runs the risk of exposing users only to a concentrated set of contents.
**しかし、レコメンデーションの精度を重視しすぎると、ユーザーに限られたコンテンツしか提供できなくなる危険性がある**。
This could attract user attention in the near term, but likely hurt user experience in the long run.
これは短期的にはユーザーの注目を集めるかもしれないが、長期的にはユーザー体験を損なう可能性が高い。
There has been a growing body of work examining factors other than accuracy in shaping user’s perception of recommendation quality [9, 19, 35, 66, 72, 72].
**推薦の質に対するユーザの認識を形成する上で、accuracy以外の要因を検討する研究が増えている**[9, 19, 35, 66, 72, 72]。(beyond-accuracy metricsってやつか:thinking_face:)
In particular, aspects such as diversity, novelty and serendipity of recommendations have been studied.
特に、レコメンデーションの多様性、新規性、セレンディピティといった側面が研究されてきた。
Here we design metrics to measure these four aspects for a RL based recommender system.
ここでは、RLベースのレコメンダーシステムのために、**これら4つの側面を測定するためのメトリクスを設計**する。
Some of the metrics measure directly on the learned policy πθ , and thus apply only to systems producing a distribution over the content vocabulary.
**メトリクスのいくつかは、学習されたポリシー $\pi_{\theta}$ に対して直接適用される**ため、コンテンツボキャブラリー全体にわたる分布を生成するシステムにのみ適用される。
(これって、全てのコンテンツを推薦し得るような確率的なpolicyを前提としたmetricsだよってこと?? もしくは $\pi_{\theta}(a|x) \forall a in A$ が既知の方策だったら適用可能ってことかも...??:thinking_face:)
Others measure on the recommendation set A πθ generated by acting according to πθ (taking most probable items) 1 , which are generic for any types of recommender systems 2 .
また $\pi_{\theta}$ に従って行動することによって**生成された推薦set $A_{\pi_{\theta}}$ に対して測定されるものもあり、これはどのようなタイプのレコメンダーシステムにも一般的**である。(うんうん、こういうmetricsならpolicyが決定的でも確率的でも一様に評価可能...!:thinking_face:)
These metrics bear similarity to many prior works in quantifying the four factors of recommendation quality [5, 8, 15, 19, 26, 29, 66].
これらの指標は、推薦品質の4つの要素を定量化する多くの先行研究[5, 8, 15, 19, 26, 29, 66]と類似している。

## 5.1. Attributes

We first introduce two item attributes that are used to define both the surprise factor in eq (6) as well as the metrics:
まず、**式(6)のsurprise因子とメトリクスの両方を定義するために使用される2つのアイテム属性**を紹介する。

### Topic cluster. トピック・クラスター
A topic cluster for each item is produced by: 1) taking the item co-occurrence matrix, where entry (i, j) counts the number of times item i and j were interacted by the same user consecutively; 2) performing matrix factorization to generate one embedding for each item; 3) using k-means to cluster the learned embeddings into 10K clusters; 4) assigning the nearest cluster to each item.
各アイテムのトピック・クラスタは、次のようにして生成される： 1) アイテムの共起行列（項目(i, j)は、項目iとjが同じユーザーによって連続して相互作用した回数をカウントする）を取る; 2) マトリックス因子化を行い、各アイテムに1つの埋め込みを生成する; 3) k-meansを使用して学習された埋め込みを10Kのクラスタにクラスタリングする; 4) 各アイテムに最も近いクラスタを割り当てる。

### Content provider.
コンテンツプロバイダー。
Content provider is another attribute of interest as: 1) we observed consistency between contents produced by the same provider, e.g., a food blogger often writes about specific cuisines; 2) we are interested in understanding the importance of content-provider diversity/novelty [37, 64] in influencing long term user experience.
コンテンツ提供者は興味深い属性の一つです。理由としては、1) 同じ提供者によって作られたコンテンツには一貫性が見られることが多いこと（例えば、フードブロガーは特定の料理について頻繁に書く傾向があります）、2) 長期的なユーザー体験に影響を与えるコンテンツ提供者の多様性や新規性の重要性を理解したいという点があります【37, 64】。

## 5.2. Accuracy 正確さ

Arguably the most important property of a recommender is to be able to retrieve contents the user is interested in consuming.
レコメンダーの最も重要な特性は、ユーザーが消費したいと思うコンテンツを検索できることである。
We compute the mean average precision at K = 50 (mAP@50) [63] on the recommended set A πθ to measure the accuracy, that is the average precision of identifying an item the user is interested in consuming among A πθ .
正確さを測定するために、推奨セットA πθ において、ユーザーが消費したいと思うアイテムを識別する平均精度を測定するために、K = 50での平均平均精度（mAP@50）[63]を計算する。

## 5.3. Diversity 多様性

Diversity measures the number of distinct faucets the recommendation set contains.
多様性は、推薦セットが含む異なる蛇口の数(??)を測定する。
Many measurements of set diversity have been proposed [39, 45, 53].
セットの多様性については、多くの測定法が提案されている[39, 45, 53]。(うんうん...!)
Among them, the average dissimilarity of all pairs of items in the set is a popular choice.
その中でも、**推薦セット内のすべてのアイテムのペアの平均非類似度**がよく使われる。

$$
Diversity(A^{\pi_{\theta}}) = E_{s \in d^B} [1 - \frac{1}{|A^{\pi_{\theta}}|(|A^{\pi_{\theta}}| - 1)} \sum_{i,j \in A^{\pi_{\theta}}, i \neq j} Sim(i, j)]
$$

We define the similarity between two items i and j both on topic level and on content provider level.
本研究では、**2つのアイテムiとjの類似度を、トピックレベルとコンテンツプロバイダレベルの両方で定義**する。
That is, Sim(i, j) = 1 if i and j belongs to the same topic cluster, and 0 otherwise.
つまり、Sim(i, j) = 1 は、iとjが同じトピッククラスタに属している場合であり、それ以外は0である。
Similarly for content provider.
コンテンツプロバイダーも同様だ。

## 5.4. Novelty ノベルティ

The two terms of novelty and serendipity have been used interchangeably in the literature.
**新規性(novelty)とセレンディピティという2つの用語は、文献の中で同じ意味で使われている**。(あ、そうなのか...!:thinking:)
In this work, we use novelty to focus on the global popularity-based measurements and serendipity to capture the unexpectedness/surprise of the recommendation to a specific user.
**この研究では、noveltyはグローバルな人気に基づく測定に焦点を当て、serendipityは特定のユーザーに対する推薦の意外性／驚きを捉えるために使用**する。(別の指標として使用するってことね!)
That is, novelty concerns the recommender system’s capacity to suggest something a user is unlikely to know about already or discover by themselves.
つまり、**新規性とは、ユーザがすでに知っていたり、自分で発見したりしそうもないものを推薦システムが提案する能力**に関するものである。(これって、本質的に推薦システムで求められる能力だよな...!:thinking:)
Zhou et al.[71] first introduced the notion of self-information of a recommended item, which measures the unexpectedness of a recommended item relative to its global popularity
Zhouら[71]は、**推薦アイテムのself-information(自己情報?)という概念**を最初に導入し、これは**推薦アイテムのグローバルな人気に対する推薦アイテムの unexpectedness(意外性)**を測定する。

$$
I(a) = - \log p(a) = - \log \frac{\text{# users consumed item a}}{\text{# users}}
\\
= - \log (\text{# users consumed item a}) + const
\tag{8}
$$

Herep(a) measures the chance a random user would have consumed item a.
ここで $p(a)$ は、ランダムなユーザがアイテムaを消費する機会を測定する。
By definition, a globally "under-explored" item (tail content) will have higher self-information.
**自己情報の定義によれば、グローバルに "未探索" のアイテム（テールコンテンツ）は、より高い自己情報を持つ**。
With the definition of item-level self-information, we can then measure novelty of the learned policy pi as
アイテムレベルの自己情報の定義により、学習された方策 $\pi$ の新規性を次のように測定できる。

$$
Novelty(\pi_{\theta}) = E_{s \in d^B_t} [\sum_{a in \mathcal{A}} \pi_{\theta}(a|s_t)I(a)]
\tag{9}
$$

A learned policy πθ that casts more mass on items with higher selfinformation, being able to recommend "under-explored" items, is deemed more novel.
学習されたポリシー $\pi_{\theta}$ が、より高い自己情報を持つアイテムにより多くの質量を投影し"未探索"のアイテムを推薦できるようになると、より新規性が高いと見なされる。
(なるほど、このNoveltyが、開発者が $\pi_{\theta}(a|x)$ を認識できてないと測定できない指標の1つか...!:thinking:)
We can define the novelty metrics for attributes similarly by looking at the self-information of the attribute instead, e.g., popularity of the content provider.
**同様に、アイテム属性のnoveltyメトリクスを定義することができる**。例えば、アイテム属性レベルの自己情報 (i.e. コンテンツプロバイダの人気度合い) をみることで。

<!-- ここまで読んだ! -->

## 5.5. Serendipity ♪セレンディピティ

Serendipity captures the unexpectedness/surprise of a recommendation to a specific user.
セレンディピティは、特定のユーザーに対する推薦の意外性／驚きを捉える。
It measures the capability of the recommender system to recommend relevant contents outside of the user’s normal interests.
これは、**推薦システムがユーザの通常の興味以外の関連コンテンツを推薦する能力を測定するもの**である。
There are two important factors in play here: 1) unexpectedness/surprise: as a counter example, a recommendation of John Lenon to listeners of The Beatles will not constitutes a surprising recommendation; 2) relevance: the surprising contents should be of interest to the user.
ここには2つの重要な要素がある： 1）意外性／驚き： 逆の例として、ビートルズのリスナーにジョン・レノンを推薦しても、意外な推薦にはならない： 2）関連性：驚くような内容は、ユーザにとって関心のあるものでなければならない。
In other words, serendipity measure the ability of the recommender to discover previously unknown (to the recommender) interests of the user.
言い換えれば、セレンディピティとは、レコメンダーが（レコメンダーにとって）未知のユーザーの興味を発見する能力のことである。(うん、Serendipity = like + didn't expect だもんね...!:thinking:)
We define the serendipity value of a recommendation $\mathbf{a}_t$ w.r.t a user with interaction history of $I_t$ as
ユーザーの相互作用履歴 $I_t$ に関して、推薦アイテム $a_t$ のセレンディピティ値を次のように定義する。

もし $r^{e}(s_t, a_t) > 0$ かつ $a_t$ のトピッククラスタが $I_t$ のどのアイテムのトピッククラスタとも異なる場合、セレンディピティ値 $S^{topic}(a_t|s_t, I_t)$ は1となる。そうでない場合は0となる。

Again we can define the content-provider level serendipity value similarly.
ここでも同様に、コンテンツ提供者レベルのセレンディピティ値も定義することができる。
With the serendipity value of an item defined, we can then quantify the serendipity of the recommendation set Sπθ as.
アイテムのセレンディピティ値が定義されたことで、推薦セットのセレンディピティ $S_{\pi_{\theta}}$ を次のように定量化できる。

$$
Serendipity(A^{\pi_{\theta}}) = E_{s_t \in d^B_t} [ \frac{1}{|A^{\pi_{\theta}}|} \sum_{a \in A^{\pi_{\theta}}} S^{topic}(a|s_t, I_t)]
\tag{11}
$$

(推薦アイテム集合内のセレンディピティ値の平均値の、ユーザ特徴量の分布に対する期待値を取ることで、方策のセレンディピティを測定してる? たぶんこの定義は、ある1ユーザへの推薦結果への評価値だよね...!:thinking:)

<!-- ここまで読んだ! -->

## 5.6. Long Term User Experience 長期的なユーザー・エクスペリエンス

Past work has suggested connections between these recommendation qualities toward long term user experience, either through surveys or interviews [5, 66].
過去の研究では、調査やインタビューを通じて、長期的なユーザー体験に向けたこれらの推薦品質との関連性が示唆されている[5, 66]。
We use user returning to the platform, and user moving from a low-activity bucket to a highly-active one on the platform as the holistic measurement of improved long term user experience, and establish the connection between these measurements and long term user experience.
我々は、**ユーザがプラットフォームに戻ってくること、およびプラットフォーム上で低活動バケットから高活動バケットに移動することを、改善された長期的なユーザー体験の包括的な測定として使用**し、これらの測定と長期的なユーザー体験との関連性を確立する。
(user engagementの代理指標として、ユーザのプラットフォームへの戻りやユーザの活動レベルの変化を用いているってことか...!:thinking:)

<!-- ここまで読んだ! -->

# 6. Offline Analysis オフライン分析

We conducted an extensive set of offline experiments comparing the exploration strategies introduced in Section 4.
**セクション4で紹介した探索戦略**(あ、4章では探索戦略の方法を説明してるのか!笑)を比較するため、オフラインで広範な実験を行った。
Specifically, we built these exploration approaches onto the baseline REINFORCE recommender described in Section 3.
具体的には、セクション3で説明した**ベースラインREINFORCEレコメンダー**に、これらの探索アプローチを組み込んだ。
We evaluate them by computing the set of metrics defined in Section 5 and compare the metric movements between different hyper-parameter settings and different exploration methods.
セクション5で定義されたメトリクスのセットを計算することでそれらを評価し、異なるハイパーパラメータ設定と異なる探索方法の間でメトリクスの動きを比較する。

## 6.1. Dataset データセット

We conducted 3 runs of experiments for each comparison and report the mean and standard deviation of the metrics.
各比較について3回の実験を行い、メトリクスの平均と標準偏差を報告する。
For each experiment run, we extracted close to a billion user trajectories from a commercial recommendation platform.
各実験の実行のために、商用レコメンデーション・プラットフォームから10億人近いユーザーの軌跡を抽出した。
Each trajectory HT = {(st ,At , at ,rt ) : t = 0, .
各軌跡HT = { (st ,At , at ,rt ) ： t = 0, .
..
..
,T }, as described in Section 3, contains user historical events on the platform.
T }には、セクション3で説明したように、プラットフォーム上のユーザー履歴イベントが含まれる。
The lengths of trajectories between users can vary depending on their activity level.
ユーザー間の軌跡の長さは、活動レベルによって異なる。
We keep at most 500 historical pages with at least one positive user interaction (nonzero rt ) for each user.
各ユーザについて，少なくとも1回の肯定的なインタラクション（rtが0でない）がある履歴ページを最大500ページ保存する．
Among the collected trajectories, we hold out 1% for evaluation.
収集した軌跡のうち、評価のために1％を保留する。
We restrict our action space (item corpus) to the most popular 10 million items in the past 48 hours on the platform.
行動空間（アイテム・コーパス）を、プラットフォーム上で過去48時間に最も人気のあった1,000万アイテムに限定する。
Our goal is to build a recommender agent that can choose among the 10 million corpus the next set of items for users to consume so as to maximize the cumulative long-term reward.
我々の目標は、長期的な累積報酬を最大化するように、1,000万コーパスの中からユーザーが消費すべき次のアイテムセットを選択できるレコメンダーエージェントを構築することである。

## 6.2. Entroy Regularization 正則化

The most straightforward knob to tune up and down the exploration strength for entropy regularization is the regularization coefficient α as defined in eq.4.We compare the baseline method, a REINFORCE agent maximizing only the expected return as defined in eq.2, with added entropy regularization with α in [0.1, 0.5, 1.0, 10.0].
エントロピー正則化の探索強度を上下に調整する最も簡単なノブは、式4で定義される正則化係数αである。我々は、ベースライン手法、すなわち、式2で定義される期待リターンのみを最大化するREINFORCEエージェントと、αを[0.1, 0.5, 1.0, 10.0]の範囲で追加したエントロピー正則化とを比較する。
As shown in Table 1, entropy regularization is an extremely efficient method to introduce diversity and novelty to the system, at the cost of reduced accuracy.
表1に示すように、エントロピー正則化は、精度の低下を代償に、システムに多様性と新規性を導入する非常に効率的な方法である。
When the regularization strength is large, it also significantly drops the system’s capability to introduce serendipitous contents to users because of the loss of relevance.
正則化の強度が大きいと、関連性が失われるため、ユーザーにセレンディピティなコンテンツを紹介するシステムの能力も著しく低下する。
For example, a regularization strength of α = 1.0 drops the topic serendipity value by −21.6% (0.037 → 0.029).
例えば、正則化の強さをα = 1.0にすると、トピック・セレンディピティの値は-21.6%低下する（0.037 → 0.029）。

## 6.3. Intrinsic Motivation 内発的動機づけ

One of the obvious hyper-parameters to adjust the exploration strength for the intrinsic motivation approach is to tune the boosting factor c defined in eq.6.Here we study the impact of the more interesting variants.
内発的動機づけアプローチの探索強度を調整するための明らかなハイパーパラメータの1つは、式6で定義されるブースティング係数cを調整することである。
First, on which attribute to use to define surprise.
まず、驚きを定義するためにどの属性を使うかについて。
We experimented with defining surprise by topic cluster (denoted as "topic" in Table 2) and content provider (denoted as "provider" in Table 2).
私たちは、トピック・クラスター（表2では「トピック」と表記）とコンテンツ・プロバイダー（表2では「プロバイダー」と表記）によってサプライズを定義する実験を行った。
Second, on the length of the user historical events used to define surprise.
第二に、驚きを定義するために使用されるユーザーの歴史的出来事の長さについて。
As explained in [66], users’ perception of surprise of contents can drift over time.
66]で説明されているように、コンテンツの驚きに対するユーザーの認識は、時間とともに変化する可能性がある。
Contents that the user interacted in the past, but has not been served and interacted for a long time, can be deemed surprising when being resurfaced again.
ユーザーが過去にやりとりしたコンテンツが、長い間提供されず、やりとりもされていない場合、再浮上したときに意外だと判断される可能性がある。
We experimented with having It contain all the items the user interacted with in the past one day, one week and one year (denoted as d = 1, d = 7 and d = 365 respectively in Table 2).
過去1日、1週間、1年（表2ではそれぞれd = 1、d = 7、d = 365と表記）にユーザーが操作したすべてのアイテムを含むようにする実験を行った。
Table 2 summarizes the comparison between different variants of the intrinsic motivation proposal.
表2は、内発的動機づけの提案の異なるバリエーション間の比較をまとめたものである。
Similar to entropy regularization, all variants improve on diversity at the cost of lower accuracy.
エントロピーの正則化と同様に、すべてのバリエーションは、精度を下げる代償として多様性を向上させる。
This method does not change the novelty metrics significantly, neither on the item level nor content provider level.
この方法では、アイテム・レベルでもコンテンツ・プロバイダ・レベルでも、新規性の指標に大きな変化はない。
We thus conclude that tail contents are not necessarily more serendipitous (relevant and surprising) than popular ones.
したがって、テールコンテンツは必ずしも人気コンテンツよりもセレンディピティ（関連性や意外性）が高いとは限らないと結論づけられる。
We do see a significant improvement in the serendipity metrics, even though the overall accuracy of these methods turn out unfavorable comparing with the baseline.
これらの手法の全体的な精度は、ベースラインと比較して不利な結果となったが、セレンディピティの指標には大きな改善が見られた。
As an example, the variant which uses topic cluster and a historical window size of 7 days, improves the serendipity level by +18.9% (0.037 → 0.044) even though the overall accuracy measured by mAP@50 was dropped by −13.7% (0.070 → 0.063).
一例として、トピック・クラスターと7日間の履歴ウィンドウ・サイズを使用するバリアントでは、mAP@50で測定された全体的な精度が-13.7%（0.070 → 0.063）低下したにもかかわらず、セレンディピティ・レベルが+18.9%（0.037 → 0.044）向上している。
Attributes.
属性。
Offline analyses showed both definitions of surprise based on topic cluster and content provider are equally effective in optimizing different angles of serendipity.
オフライン分析では、トピック・クラスターとコンテンツ・プロバイダーに基づく驚きの定義の両方が、セレンディピティのさまざまな角度を最適化するのに等しく効果的であることが示された。
That is topic cluster definition improves offline topic serendipity metrics by +18.9% from 0.037 to 0.044, and content provider definition improves content provider serendipity for +11.5% from 0.078 to 0.087.
つまり、トピック・クラスターの定義はオフライン・トピックのセレンディピティ・メトリクスを0.037から0.044へと+18.9%改善し、コンテンツ・プロバイダの定義はコンテンツ・プロバイダのセレンディピティを0.078から0.087へと+11.5%改善する。
We however do see very different performance in user metrics in live experiments as shown in Section 7.1 below, suggesting one angle (topic serendipity) is more important than the other (content provider serendipity) in optimizing the overall user experience.
しかし、以下のセクション7.1に示すように、ライブ実験では、ユーザーメトリクスのパフォーマンスが大きく異なっており、ユーザーエクスペリエンス全体の最適化において、一方の角度（トピックセレンディピティ）が他方の角度（コンテンツプロバイダセレンディピティ）よりも重要であることを示唆している。
Window sizes.
窓のサイズ。
As we extend the historical window used to define surprise, i.e., having It contain longer user history, the definition of surprise becomes stricter.
驚きを定義するために使用される履歴ウィンドウを拡張すると、つまり、より長いユーザー履歴を含むようにすると、驚きの定義はより厳しくなります。
An item is less likely to be surprising/different when comparing with a longer history than a shorter one.
長い歴史と比較した場合、短い歴史と比較した場合よりも、驚きや違いが生じにくい。
As a result the percentage of state-action pairs receiving the extra multiplier of c > 1 is reduced.
その結果、c＞1の特別倍率を受けるステート・アクション・ペアの割合は減少する。
In the datasets, the percentage is reduced from 36% → 19% → 12% when the window size is extended from 1 → 7 → 365 days.
データセットでは、ウィンドウ・サイズを1日→7日→365日と拡大すると、その割合は36％→19％→12％と減少する。
The intrinsic motivation boost is applied to a smaller and smaller set of state-action pairs.
内発的動機づけのブーストは、より小さな状態-動作のペアの集合に適用される。
The relative change on diversity related metrics is marginal between these variants.
多様性に関連する指標に関する相対的な変化は、これらの変種間でわずかである。
The variant with window size of d = 7 scored the highest on the topic serendipity metric, which is defined using a window size of one year.
ウインドウサイズd = 7のバリアントは、1年のウインドウサイズで定義されるトピック・セレンディピティの指標で最も高いスコアを獲得した。

## 6.4. Actionable Representation

In this set of experiments, we compare four setups: 1) baseline: the baseline REINFORCE algorithm; 2) repre.
この一連の実験では、4つのセットアップを比較した： 1) ベースライン： ベースライン：ベースラインREINFORCEアルゴリズム。
alone: the baseline REINFORCE with the actionable representation, i.e., the additional bit indicating if the item at is serendipitous at state st according to user historical interactions It ; 3) intrinsic alone: the baseline REINFORCE with intrinsic motivation for reward shaping; 4) repre.
単独： ベースラインREINFORCEに、行動可能な表現、すなわち、ユーザーの過去のインタラクションに従っ て状態stでアイテムがセレンディピティであるかどうかを示す追加ビットを加えたもの： ベースラインREINFORCEと報酬形成のための内発的動機づけ。

- intrinsic: the baseline REINFORCE adding both the intrinsic motivation and the actionable representation.
  ＋内発的： ベースラインのREINFORCEは、内発的動機づけと行動可能な表現の両方を加える。
  As shown in Table 3, adding the indicator alone (row 2) and adding the indicator along with the intrinsic motivation (row 4) resulted in very different metrics.
  表3に示すように、指標を単独で追加した場合（2行目）と、指標を内発的動機づけとともに追加した場合（4行目）では、測定基準が大きく異なる結果となった。
  Adding the indicator alone without the reward shaping performs very similarly to the baseline method, suggesting the representation is more useful when combined with the reward shaping.
  報酬のシェーピングを行わずにインジケーターを追加するだけで、ベースラインの方法と非常によく似た結果が得られ、報酬のシェーピングと組み合わせることで、より有用な表現になることが示唆された。
  We see +24.3% improvement in the serendipity value comparing (row 4) to (row 1) (0.037 → 0.046), and +4.5% improvement comparing to (row 3) (0.044 → 0.046).
  (4行目)と(1行目)(0.037 → 0.046)を比較すると+24.3%、(3行目)(0.044 → 0.046)を比較すると+4.5%のセレンディピティ値の向上が見られる。
  This suggests that the added representation is indeed helpful for decision making when the intrinsic motivation is rewarding serendipitous actions, i.e.actions that discover previously unknown user interests.
  このことは、内発的動機がセレンディピティ的行動、すなわち、これまで知られていなかったユーザーの興味を発見する行動に報いるものである場合、追加された表現が意思決定に役立つことを示唆している。
  To gain more insight into how the agent utilizes the additional bit indicating whether or not a historical event is surprising when provided, we compare the learning of the baseline REINFORCE algorithm with intrinsic motivation alone (shown in orange in Figure 1) vs the one combined with both the intrinsic motivation and the actionable representation (shown in cyan in Figure 1).
  エージェントは、歴史的なイベントが提供されたときに、それが驚くべきものであるかどうかを示す追加のビットをどのように利用するかをより深く理解するために、ベースラインREINFORCEアルゴリズムの学習を、内発的動機づけのみ（図1のオレンジ色で示す）と、内発的動機づけと行動可能表現の両方を組み合わせたもの（図1のシアン色で示す）とを比較する。
  The RNN [31] Chen et al.[11] used to encode the user history Ht has an important gate named input gate.
  ユーザー履歴Htを符号化するために使用されるRNN[31] Chenら[11]には、入力ゲートという重要なゲートがある。
  This gate controls how much the RNN is updating its hidden state to take into account a new input (event).
  このゲートは、RNNが新しい入力（イベント）を考慮するためにどれだけ隠れ状態を更新するかを制御する。
  We take the activation values of the input gates across the user trajectory, and separate the values in two groups: the ones on historical events that are considered surprising and relevant (shown in Figure 1 left), and the ones on historical events that are not (shown in Figure 1 right).
  入力ゲートの活性化値をユーザーの軌跡全体にわたって取り出し、2つのグループに分ける： すなわち、意外性があり、関連性があると考えられる歴史的出来事に関するもの（図1左）と、そうでない歴史的出来事に関するもの（図1右）である。
  Comparing the left and right figures, we can see that by adding this additional information, the RNN is able to differentiate better between historical events that are serendipitous and those that are not.
  左と右の図を比較すると、この追加情報を加えることで、RNNはセレンディピティである歴史的出来事とそうでない歴史的出来事をよりよく区別できることがわかる。
  At the end of training, the mean activation for events that are surprising and relevant (left) is at 0.1765 (+1.4% higher) for intrinsic motivation + actionable representation compared with 0.1741 for intrinsic motivation alone.
  訓練終了時、驚きと関連性のある出来事（左）に対する平均活性化は、内発的動機づけ＋行動可能な表現では0.1765（＋1.4％）であるのに対し、内発的動機づけのみでは0.1741である。
  The mean activation for events that are NOT serendipitous (right) is at 0.1409 (−11.2% lower) for intrinsic motivation + actionable representation compared with 0.1586 for intrinsic motivation alone.
  セレンディピティではない出来事（右）に対する平均活性化は、内発的動機づけ＋行動可能な表現では0.1409（-11.2％）であり、内発的動機づけのみの場合は0.1586であった。
  This suggests that relying on the reward alone, RNN can still recognize the difference between these two groups of events and perform slightly larger update when the historical event is considered surprising.
  このことは、RNNが報酬だけに頼っていても、2つのイベントの違いを認識することができ、歴史的なイベントが意外なものであると考えられる場合に、わずかに大きな更新を行うことができることを示唆している。
  Adding the feature helps RNN differentiate the two groups better.
  特徴を追加することで、RNNは2つのグループをより区別しやすくなる。

# 7. Live Experiments and Logn Term User Experience ライブ実験と長期ユーザー・エクスペリエンス

<!-- 6章は一旦飛ばして、オンライン実験の7章へ! -->

We conduct a series of live A/B tests on a industrial recommendation platform serving billions of users to evaluate the impact of the proposed exploration approaches.
何十億ものユーザーに利用されている**産業用レコメンデーション・プラットフォーム上で一連のライブA/Bテストを実施**し、提案する探索アプローチの影響を評価する。(オンラインテストだ!)
The control serves the base REINFORCE agent as described in Section 3.
コントロールは、セクション3で説明したように、ベースとなるREINFORCEエージェントにサービスを提供する。
The agent selects hundreds of candidates from a corpus of 10 million.
エージェントは1,000万のコーパスから数百の候補を選ぶ。
The returned candidates A πθ , along with others, are ranked by a separate ranking system before showing to the users.
返された候補 $A_{\pi_{\theta}}$ は、ユーザに表示される前に別のランキングシステムによってランク付けされる。
(あ、今回の方策は、2-stages推薦における1段階目で採用される方策なのか...!:thinking:)
We ran three separate experiments: 
3つの別々の実験を実施した。(あ、じゃあcontrol合わせてvariant数4つのABテストってことかな...!:thinking:)
1) Entropy regularization: serving the REINFORCE agent with entropy regularization as explained in Section 4.1; 
1) エントロピー正則化： セクション4.1で説明されているように、エントロピー正則化を使用してREINFORCEエージェントにサービスを提供する。
2) Intrinsic motivation: serving the REINFORCE agent with intrinsic motivation to discover new user interest (using topic cluster attributes with a history window of 7 days and a serendipity boost c = 4) as explained in Section 4.2; 
2) 内発的動機づけ： セクション4.2で説明されているように、新しいユーザーの興味を発見するために内発的動機づけを使用してREINFORCEエージェントにサービスを提供する（トピック・クラスター属性を使用し、履歴ウィンドウを7日、セレンディピティブーストをc = 4とする）。
3) Intrinsic Motivation + Actionable Representation: serving the REINFORCE agent with both the intrinsic motivation and the actionable representation as introduced in Section 4.3. 
3) 内発的動機づけ+行動可能な表現： セクション4.3で紹介された内発的動機づけと行動可能な表現の両方を使用してREINFORCEエージェントにサービスを提供する。
We compare 1) and 2) to the baseline REINFORCE system as described in Section 3 as control to measure the effect of entropy regularization and intrinsic motivation respectively, and 3) to 2) as control to measure the additional value of introducing the actionable representation on top of intrinsic motivation.
我々は、エントロピー正則化と内発的動機づけの効果を測定するために、セクション3で説明されているベースラインREINFORCEシステムに対して、1)と2)を比較し、内発的動機づけの上に行動可能な表現を導入することの追加価値を測定するために、3)と2)を比較する。

We first summarize the live experiment results of these experiments in Section 7.1, and later measure several aspects of long term user experience in Section 7.2. In the end, we establish the connection between exploration and different aspects of recommendation quality toward improving long term user experience.
まずセクション7.1において、これらのライブ実験の結果を要約し、その後セクション7.2において、長期的なユーザー体験のいくつかの側面を測定する。最後に、長期的なユーザー体験を向上させるために、探索と推薦品質の様々な側面との関連を確立する。

<!-- ここまで読んだ! -->

## 7.1. Results 結果

Figure 3 summarizes the performances of these exploration approaches on the top-line metric capturing user overall enjoyment of the platform.
図3は、**プラットフォームに対するユーザーの総合的な楽しさを表すトップライン指標**における、これらの探索アプローチのパフォーマンスをまとめたものである。 (この縦軸の使い方を発表の際に真似したい...!:thinking:)
(あ、教えられないけど何かしらの代理指標があるんだ!いや、後述された内容をみると多分「プラットフォーム上で低活動バケットから高活動バケットに移動すること」の指標っぽい...!:thinking:)
As shown in Figure 3a (α = 0.1 in red, and α = 0.5 in blue), although entropy regularization increases diversity and novelty in both offline and live experiments, it does not lead to significant improvement on the user enjoyment.
図3a（赤がα＝0.1、青がα＝0.5）に示すように、エントロピー正則化は、オフライン実験とライブ実験の両方で多様性と新規性を増加させるものの、ユーザーの楽しみの大幅な改善にはつながらない。
In other words, increased diversity or novelty alone does not necessarily lead to better user experience.
**言い換えれば、多様性や新規性を高めるだけでは、必ずしもユーザー体験の向上にはつながらない**ということだ。
When we increase the regularization strength to α = 0.5, we see slightly worse live metrics.
正則化の強さをα = 0.5まで上げると、ライブ・メトリクスがわずかに悪化する。

Comparing with entropy regularization (Figure 3a), intrinsic motivation (Figure 3b) and its combination with actionable representation (Figure 3c), not only significantly improve on the top-line metric, but also exhibit a strong learning effect over the course of the experiments.
エントロピー正則化（図3a）と比較すると、内発的動機づけ（図3b）および行動可能な表現との組み合わせ（図3c）は、**トップラインの指標を大幅に改善するだけでなく、実験の過程で強力な学習効果を示す**。(強力な学習効果って、オフライン学習で方策を改善できてるってことか...いいね...!:thinking:)
We compare the offline measurement on accuracy, diversity, novelty and serendipity between entropy regularization with α = 0.5 (Table 1 row 3) and intrinsic motivation (Table 3 row 3) and its combination with actionable representation (Table 3 row 4) and make the following observations: 
我々は、α=0.5のエントロピー正則化（表1の行3）、内在的動機づけ（表3の行3）、および実行可能な表現との組み合わせ（表3の行4）の間の精度、多様性、新規性およびセレンディピティに関するオフライン測定を比較し、以下の観察を行う： 
1) the entropy regularization method with α = 0.5 achieves very similar diversity metrics comparing to intrinsic motivation or its combination with actionable representation.
19 α = 0.5のエントロピー正則化法は、intrinsic motivationまたはactoable representationとの組み合わせと比較して、非常に類似した多様性指標を達成する。(i.e. 多様性は、(a)と(b)(c)は同程度ってことか!)
All three methods reach a topic diversity around 0.86, and content provider diversity around 0.93; 
3つの方法はすべて、トピックの多様性が約0.86、コンテンツプロバイダの多様性が約0.93に達する。

1) The entropy regularization method achieved slightly higher novelty metric, both in item level and content provider level; 
2) エントロピー正則化法は、アイテムレベルとコンテンツプロバイダレベルの新規性指標がわずかに高かった;
3) The metrics that entropy regularization loses is on accuracy and serendipity.
4) エントロピー正則化が負けているメトリックは、精度とセレンディピティである。
5) Intrinsic motivation method and its combination with actionable representation have favorable improvement on serendipity comparing with the baseline REINFORCE algorithm even though their accuracy numbers are worse. 
6) 内発的動機づけ法とその行動可能な表現との組み合わせは、精度の数値が悪いにもかかわらず、ベースラインのREINFORCEアルゴリズムと比較して、**セレンディピティに有利な改善**が見られる。
In conclusion, intrinsic motivation and its combination with actionable representation compare favorably to the baseline REINFORCE and entropy regularization only in the serendipity metrics offline.
**結論として、内発的動機づけと行動可能な表現との組み合わせは、オフラインでのセレンディピティ指標において、ベースラインのREINFORCEとエントロピー正則化と比較して有利**である。
In live experiments, the intrinsic motivation and its combination with actionable representation were shown to significantly improve over the baseline REINFORCE and entropy regularization, as shown in Figure 3 (middle and right).
**ライブ実験では、図3（中と右）に示すように、内在的動機づけと行動可能な表現との組み合わせは、ベースラインのREINFORCEとエントロピー正則化よりも大幅に改善することが示された**。
Combining the offline and live experiment observations, we hypothesize that serendipity is an important faucet of recommendation quality that leads to improved long term user experience.
オフラインとライブ実験の観察を組み合わせることで、セレンディピティは、改善された長期的なユーザー体験につながる推薦品質の重要な要素であるという仮説を立てる。
We also conducted another group of live experiments defining surprise for optimization using content provider rather than topic.
また、トピックではなくコンテンツプロバイダーを使った最適化のためのサプライズを定義する、別のライブ実験グループも行った。
The experiment turns out neutral on the top-line metric, which suggest topic serendipity is more connected with long term user experience than content provider.
この実験は、トップラインの指標に対して中立的であり、**トピックセレンディピティがコンテンツプロバイダーよりも長期的なユーザー体験と関連していること**を示唆している。

Another top-line metric that we keep track of is the number of days users returning to the platform.
私たちが記録している**もう1つのトップライン指標は、ユーザーがプラットフォームに戻った日数**です。(平均再訪日数、みたいな感じか...!:thinking:)
For both the intrinsic motivation and actionable representation treatment, we observed significant improvement on this metric as well, suggesting users are encouraged to return to the platform due to better recommendation quality.
内発的動機づけと行動可能な表現の両処理において、この指標においても大幅な改善が見られ、より良い推薦品質によってユーザーがプラットフォームに戻ることが奨励されていることを示唆している。
Figure 2 shows the improvement of user returning in the actionable representation experiment, comparing with the base REINFORCE with intrinsic motivation as control, suggesting that aiding the representation learning with the serendipity information further improves the learned policy, leading to better overall user experience.
図2は、ベースのREINFORCE with 内発的動機づけをcontrol variant ((b)パターンをcontrolとした結果ってことね!)として比較した行動可能な表現実験におけるユーザーの戻りの改善を示している。**セレンディピティ情報を使って表現学習を支援することで、学習されたポリシーがさらに改善され、全体的なユーザーエクスペリエンスが向上すること**を示している。
("学習された方策がさらに改善され"ってことは、探索的に方策が行動を選んでることで品質の高いデータを収集できて、結果としてOPLによって方策を更に最適化できているってことだよなぁ...:thinking:)

<!-- ここまで読んだ! -->

## 7.2. Long Term User Experience 長期的なユーザー・エクスペリエンス

### Learning Effect of Intrinsic Motivation. 内発的動機づけの学習効果。

To better understand the effect of intrinsic motivation and reward shaping in the long term, we examine the temporal trend of the live metrics in addition to the aggregated metrics reported above.
長期的な内発的動機づけと報酬シェーピングの効果をよりよく理解するために、上記で報告した集計指標に加えて、ライブ指標の時間的傾向を調べた。
For the 6-week experiment on intrinsic motivation, we look at week-over-week metrics by aggregating user activities within each week.
内発的動機づけに関する6週間の実験では、各週のユーザー活動を集計することで、前週比の指標を調べた。
Specifically, we track the number of unique topic clusters the user has interacted with over every week, as well as the entropy of those topic clusters.
**具体的には、ユーザが1週間ごとにやりとりしたユニークなトピック・クラスタの数と、それらのトピック・クラスタのエントロピーを追跡する**。
Suppose the user has interacted with Ni items from topic cluster i, then the entropy of his/her history is computed as − Í i pˆi loд(pˆi), where pˆi = Ni / Í i Ni is the proportion of items interacted with that are from topic cluster i.
ユーザがトピック・クラスタ $i$ から $N_i$ アイテムとやりとりしたとすると、彼/彼女の履歴のエントロピーは $- \sum_i \hat{p}_i \log(\hat{p}_i)$ として計算される。ここで、$\hat{p}_i = N_i / \sum_i N_i$ は、トピック・クラスタ $i$ からやりとりしたアイテムの割合である。

Figure 4 shows the comparison between control and treatment, where the treatment group has a boosting multiplier of 4 for unknown user interests as in Eq.(6).
図4は、コントロールとトリートメントの比較である。トリートメントグループは、式(6)のように、未知のユーザーの興味に対してブースティング乗数を4としている。
Compared with users in the control group which does not have the reward shaping, users in the treatment group have consistently interacted with more topic clusters (Fig 4a) and generated a higher entropy over cluster distributions (Fig 4c) over the whole experiment period.
リワード・シェーピングを行わないコントロール・グループのユーザーと比較すると、**トリートメント・グループのユーザーは、実験期間全体を通じて一貫して、より多くのトピック・クラスタとやりとりし（図4a）、クラスタ分布のエントロピーが高い（図4c）**。
More interestingly, the amount of improvements over control is increasing over time (Fig 4b and 4d).
さらに興味深いことに、コントロールよりも改善された量(=差分)は時間とともに増加している（図4bと4d）。
This suggests a learning effect over time from exploration, which enables users to continuously find and engage with new topics.
このことは、ユーザが継続的に新しいトピックを見つけ、それに取り組むことを可能にする、探索による長期的な学習効果を示唆している。

### User Activity Levels. ユーザーの活動レベル。

Users who come to the recommendation platform are heterogeneous in terms of activity levels.
レコメンデーション・プラットフォームにやってくるユーザは、活動レベルにおいて異質である。(うんうん...!)
Some users visit the platform occasionally, while others visit the platform more regularly and consistently.
たまにこのプラットフォームを訪れるユーザーもいれば、定期的にコンスタントに訪れるユーザーもいる。
The long-term goal of a recommendation platform is to not only satisfy the user’s need in the current session, but ideally to see them return to the recommendation platform more often in the future.
**レコメンデーション・プラットフォームの長期的な目標は、現在のセッションでユーザのニーズを満たすだけでなく、理想的には、将来、より頻繁にレコメンデーション・プラットフォームに戻ってきてもらうことである**。(うんうん...!:thinking:)

We would like to see if adding exploration in the recommendation has any effect on moving user activity levels.
**レコメンデーションに探索を加えることが、ユーザーのアクティビティレベルを上げる効果があるかどうか**を確認したい。
We define four user activity levels in terms of how many days they are active on the platform in a 2-week period, which is shown in Fig 5a.
図5aに示すように、**2週間のうち何日プラットフォーム上で活動したかという観点から、4つのユーザ活動レベルを定義する**。(この定義真似したい!というか一般的かも:thinking:)
For example, a user being casual means that he/she has been active for 1 to 4 days in the last 14 days.
例えば、カジュアルなユーザとは、過去14日間のうち1～4日間アクティブであったことを意味する。
Users can become more active or less active depending their experience on the platform as well as exogenous factors not control by recommendation.
ユーザは、プラットフォームでの経験や、レコメンデーションではコントロールできない外的要因によって、よりアクティブになったり、よりアクティブでなくなったりする。
Suppose the goal of a recommendation platform is moving casual users to become core users.
レコメンデーション・プラットフォームのゴールが、**カジュアルユーザをコアユーザに移行させること**であるとする。
An intuitive way to measure the conversion is by counting the number of users who start off casual, and end up core.
コンバージョンを測定する直感的な方法は、**カジュアルから始めてコアになったユーザの数を数えること**である。
This can be realized with a user activity level transition matrix, which measures the movement between different user activity levels.
これは、**ユーザー活動レベルの遷移行列**によって実現できる。これは、異なるユーザー活動レベル間の移動を測定する。

(以下は、具体的なユーザ活動レベルの遷移行列の集計方法!)
We examine user activity level before the experiment start date and at the end of the experiment for every treatment group to compute the transition matrix, and compare with control.
**実験開始前と実験終了時のユーザのアクティビティレベルを各処理グループごとに調べ、遷移行列を計算**し、コントロールと比較する。
Figure 5b shows the percentage difference of the transition matrices between the actionable representation treatment group and control.
図5bは、実行可能表現処理グループとコントロールの間の遷移行列の差の割合を示している。
We see that there is a significant increase in casual-to-core conversion rate.
**カジュアルからコアへのコンバージョン率が大幅に上昇している**ことがわかる。
This suggests that a successful exploration strategy can result in a desired user movement as less active users are becoming more engaged on the platform.
このことは、**探索戦略の成功が、あまりアクティブでないユーザがプラットフォーム上でより積極的になる**ことで、望ましいユーザの移動をもたらす可能性があることを示唆している。

<!-- ここまで読んだ! -->

# 8. Conclusion 結論

We present a systemic study to understand the values of exploration in recommender systems beyond reducing model uncertainty.
我々は、モデルの不確実性を低減する以上に、推薦システムにおける探索の価値を理解するための体系的研究を発表する。
We examine different user exploration strategies in affecting the four facets of recommendation quality, i.e., accuracy, diversity, novelty and serendipity, that contribute directly to user experience on the platform.
我々は、プラットフォーム上でのユーザ体験に直接寄与する、推薦品質の4つの側面、すなわち、正確性、多様性、新規性、セレンディピティに影響を与える様々なユーザー探索戦略を検証する。
We showcase exploration strategies that oriented toward discovering unknown user interests in positively influencing user experience on recommendation platforms.
レコメンデーション・プラットフォームにおけるユーザー体験にポジティブな影響を与える、未知のユーザの興味を発見することを指向した探索戦略を紹介する。
Using conversion of casual users to core users as an indicator of the holistic long term user experience, we connects serendipity to improved long term user experience.
カジュアルユーザからコアユーザへの転換を、総合的な長期的なユーザー体験の指標として使用し、セレンディピティを改善された長期的なユーザー体験につなげる。
We believe these are important first steps in understanding and improving exploration and serendipity in (RL based) recommender systems, and providing foundation for future effort in this direction.
我々は、これらが（RLベースの）推薦システムにおける探索とセレンディピティを理解し、改善するための重要な最初のステップであり、この方向における将来の取り組みの基盤を提供すると考えている。

<!-- ここまで読んだ! -->
