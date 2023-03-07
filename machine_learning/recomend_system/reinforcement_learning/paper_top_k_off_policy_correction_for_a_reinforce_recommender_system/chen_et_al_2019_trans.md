## 0.1. link

- https://arxiv.org/abs/1812.02353 httpsを使用しています。

## 0.2. title タイトル

Top-K Off-Policy Correction for a REINFORCE Recommender System
REINFORCE推薦システムのためのTop-Kオフポリシー補正法

## 0.3. abstract アブストラクト

Industrial recommender systems deal with extremely large action spaces -- many millions of items to recommend.
産業用推薦システムは、何百万もの商品を推薦するという非常に大きな行動空間を扱っている.
Moreover, they need to serve billions of users, who are unique at any point in time, making a complex user state space.
さらに、何十億人ものユーザーを対象とするため、ユーザーの状態空間も複雑である.
Luckily, huge quantities of logged implicit feedback (e.g., user clicks, dwell time) are available for learning.
幸いなことに、膨大な量の暗黙的フィードバック（ユーザーのクリック数、滞在時間など）が学習用に利用できる.
Learning from the logged feedback is however subject to biases caused by only observing feedback on recommendations selected by the previous versions of the recommender.
しかし、**ログに記録されたフィードバックからの学習は、以前のバージョンのレコメンダーによって選択された推薦アイテムリストに対するフィードバックのみを観測することによって引き起こされるバイアスに左右される**.
In this work, we present a general recipe of addressing such biases in a production top-K recommender system at Youtube, built with a policy-gradient-based algorithm, i.e. REINFORCE.
本論文では、YoutubeのトップK推薦システムにおいて、**policy-gradient-based algorithm**(i.e. REINFORCE)を用いて、このようなバイアスに対処するための一般的なレシピを紹介する.
The contributions of the paper are:
本論文の貢献は以下の通りである.
(1) scaling REINFORCE to a production recommender system with an action space on the orders of millions; (2) applying off-policy correction to address data biases in learning from logged feedback collected from multiple behavior policies; (3) proposing a novel top-K off-policy correction to account for our policy recommending multiple items at a time; (4) showcasing the value of exploration.
(1)REINFORCEを数百万の行動空間を持つ推薦システムに拡張すること、(2)複数のbehavior policy から収集したログfeedbackから学習する際の data bias に対処するために off-policy 修正を適用すること、(3)一度に複数のitemを推薦するポリシーを説明するために新しいトップKオフポリシー修正を提案すること、(4)探査の価値を紹介すること、である.
We demonstrate the efficacy of our approaches through a series of simulations and multiple live experiments on Youtube.
私たちは、一連のシミュレーションとYoutubeでの複数のライブ実験を通して、私たちのアプローチの有効性を実証している.

# 1. Introduction はじめに

Recommender systems are relied on, throughout industry, to help users sort through huge corpuses of content and discover the small fraction of content they would be interested in.
推薦システムは、ユーザが膨大なコンテンツの中から興味のありそうなごく一部のコンテンツを探し出すことを支援するために、産業界全体で利用されている.
This problem is challenging because of the huge number of items that could be recommended.
この問題は、推薦される可能性のあるアイテムが膨大であるため、困難なものとなっている.
Furthermore, surfacing the right item to the right user at the right time requires the recommender system to constantly adapt to users’ shifting interest (state) based on their historical interaction with the system [6].
さらに、**適切なユーザに適切なアイテムを適切なタイミングで**提示するためには、推薦システムは、ユーザの過去のシステムとの相互作用に基づいて**変化するユーザの興味(状態 = state)に常に適応する**必要がある[6].
Unfortunately, we observe relatively little data for such a large state and action space, with most users only having been exposed to a small fraction of items and providing explicit feedback to an even smaller fraction.
しかし、このような大きな状態・行動空間に対して、我々は比較的少ないデータしか観測しておらず、ほとんどのユーザはごく一部のアイテムにしか触れておらず、さらにごく一部のユーザにしかexplicit feedback を与えていない.
That is, recommender systems receive extremely sparse data for training in general, e.g., the Netflix Prize dataset was only 0.1% dense [5].
例えば、Netflix Prizeのデータセットは0.1%の密度に過ぎない[5].
As a result, a good amount of research in recommender systems explores different mechanisms for treating this extreme sparsity.
その結果、レコメンダーシステムの研究のかなりの部分は、**この極端なスパース性を処理するためのさまざまなメカニズムを探求**している.
Learning from implicit user feedback, such as clicks and dwell-time, as well as filling in unobserved interactions, has been an important step in improving recommenders [19] but the problem remains an open one.
クリックや滞在時間などのユーザのimplicit feedbackからの学習や、観測されな い Interaction の充填は、レコメンダーを改善する上で重要なステップとなっていますが [19]、この問題はまだ未解決のものである.

In a mostly separate line of research, reinforcement learning (RL) has recently achieved impressive advances in games [38, 46] as well as robotics [22, 25].
強化学習(RL)は、ゲーム[38, 46]やロボット工学[22, 25]において、最近目覚しい発展を遂げている.
RL in general focuses on building agents that take actions in an environment so as to maximize some notion of long term reward.
RLは一般に、**長期的な報酬(reward)の概念を最大化するように環境中で行動するagentを構築すること**に焦点を合わせている.
Here we explore framing recommendation as building RL agents to maximize each user’s long term satisfaction with the system.
ここでは、推薦を、**各ユーザのシステムに対する長期的な満足度を最大化するRL agent** の構築としてとらえることを検討する.
This offers us new perspectives on recommendation problems as well as opportunities to build on top of the recent RL advancement.
これは、推薦問題に対する新しい視点と、最近のRLの進歩の上に構築される機会を提供するものである.
However, there are significant challenges to put this perspective into practice.
しかし、この視点を実践するためには、大きな課題がある.

As introduced above, recommender systems deal with large state and action spaces, and this is particularly exacerbated in industrial settings.
前述したように、**推薦システムは大きな状態空間(ユーザのstateが変わり得るって話?)と行動空間(=ユーザの選択肢=アイテムが多いって話?)**を扱うが、これは産業環境において特に悪化している.
The set of items available to recommend is non-stationary and new items are brought into the system constantly, resulting in an ever-growing action space with new items having even sparser feedback.
推薦可能なアイテムのセットは非定常(non-stationary)であり、新しいアイテムが常にシステムに持ち込まれるため、**新しいアイテムのfeedbackがさらに疎になり、action space が常に大きくなる**(=新アイテムが追加された事で??)(これはaction spaceの拡大の話!).
Further, user preferences over these items are shifting all the time, resulting in continuously-evolving user states.
さらに、これらのアイテムに対するユーザーの嗜好は常に変化しており、結果としてユーザーの状態は常に変化している. (これは state spaceがlargeって話!)
Being able to reason through these large number of actions in such a complex environment poses unique challenges in applying existing RL algorithms.
このような複雑な環境において、多数のアクションを推論することは、既存のRLアルゴリズムを適用する上でユニークな課題をもたらす.
Here we share our experience adapting the REINFORCE algorithm [48] to a neural candidate generator (a top-𝐾 recommender system) with extremely large action and state spaces.
ここでは、REINFORCEアルゴリズム[48]を、**非常に大きなaction space と state space を持つneural candidate generator(top-K推薦システム)に適応させた経験**を紹介する.

In addition to the massive action and state spaces, RL for recommendation is distinct in its limited availability of data.
また、推薦のための RL は、膨大な行動空間(action space)と状態空間(state space)に加えて、**利用可能なデータが限られていることが特徴**である.
Classic RL applications have overcome data inefficiencies by collecting large quantities of training data with self-play and simulation [38].
古典的な RL アプリケーションは、自己再生とシミュレーションによって大量の学習データを収集することで、データの非効率性を克服してきた [38].
In contrast, the complex dynamics of the recommender system has made simulation for generating realistic recommendation data nonviable.
これに対し、レコメンダーシステムの複雑なダイナミクスは、現実的な推薦データを生成するためのシミュレーションを非実現的なものにしている.
As a result, we cannot easily probe for reward in previously unexplored areas of the state and action space, since observing reward requires giving a real recommendation to a real user.
その結果、**報酬(reward)を観測するには実際のユーザに推薦する必要がある**ため、状態空間と行動空間の未踏の領域における報酬を容易に探索することができない.
Instead, the model relies mostly on data made available from the previous recommendation models (policies), most of which we cannot control or can no longer control.
そのため，このモデルでは，これまでの推薦モデル(=推薦アイテムの選択戦略=policy)から得られるデータに依存することになるが，そのほとんどは我々がコントロールできない，あるいはコントロールできなくなったデータである.
To most effectively utilize logged-feedback from other policies, we take an off-policy learning approach, in which we simultaneously learn a model of the previous policies and incorporate it in correcting the data biases when training our new policy.
そこで、他の推薦モデルからのフィードバックを効果的に利用するために、過去の推薦モデルを同時に学習し、新しい推薦モデルの学習時にデータのbiasを補正する**off-policy学習**というアプローチをとる.
We also experimentally demonstrate the value in exploratory data.
また、探索的(exploratory)なデータにおける価値を実験的に示している.

Finally, most of the research in RL focuses on producing a policy that chooses a single item.
最後に，**RL の研究のほとんどは，単一のitemを選択するpolicyの作成に焦点をあてている**．
Real-world recommenders, on the other hand, typically offer the user multiple recommendations at a time [44].
一方、実世界のレコメンダーは通常、一度に複数の推薦アイテムをユーザーに提供する [44].
Therefore, we define a novel top-𝐾 off-policy correction for our top-𝐾 recommender system.
そこで、我々はtop-K 推薦システムのために、新しい**top-K off-policy correction(補正)**を定義する.
We find that while the standard off-policy correction results in a policy that is optimal for top-1 recommendation, this top-𝐾 off-policy correction leads to significant better top-𝐾 recommendations in both simulations and live experiments.
その結果、標準的なoff-policy補正はtop-1推薦に最適なpolicyとなるが、このtop-K off-policy補正はシミュレーションとライブ実験の両方で有意に優れたtop-K推薦につながることを見出した.
Together, we offer the following contributions:
以上により、我々は以下の貢献を行う.

- REINFORCE Recommender: We scale a REINFORCE policy-gradient-based approach to learn a neural recommendation policy in a extremely large action space. REINFORCEレコメンダー。 非常に大きな行動空間におけるneural recommendation policy を学習する為に、REINFORCEのpolicy-gradient-basedなアプローチをscaleさせる.
- Off-Policy Candidate Generation: We apply off-policy correction to learn from logged feedback, collected from an ensemble of prior model policies. We incorporate a learned neural model of the behavior policies to correct data biases. オフポリシー候補の生成。 事前モデルpolicy の アンサンブルから収集されたログfeedbackから学習する off-policy 補正を適用する. 学習したbehavior policy の neural model を組み込み、データのbiasを補正する.
- Top-𝐾 Off-Policy Correction: We offer a novel top-𝐾 offpolicy correction to account for the fact that our recommender outputs multiple items at a time. Top-K Off-Policy Correction: レコメンダーが一度に複数のアイテムを出力することを考慮し、新しいtop-K off-policy補正を提供する.
- Benefits in Live Experiments: We demonstrate in live experiments, which was rarely done in existing RL literature, the value of these approaches to improve user long term satisfaction ライブ実験でのメリット. 既存のRLの文献ではほとんど行われていなかった、**ユーザの長期的な満足度を向上させるこれらのアプローチの価値**をライブ実験で実証する.

We find this combination of approaches valuable for increasing user enjoyment and believe it frames many of the practical challenges going forward for using RL in recommendations.
私たちは、このようなアプローチの組み合わせが、ユーザの楽しみを増やすために有効であると考え、RLを推薦に利用する際の今後の実用的な課題の多くを解決するものであると考えている.

# 2. Related work 関連作品

## 2.1. Reinforcement Learning: 強化学習

Value-based approaches such as Q-learning, and policy-based ones such as policy gradients constitute classical approaches to solve RL problems [40].
Q-learningのような**Value-basedのアプローチ**や、 ポリシー勾配のような**policy-basedのアプローチ**は、 RL問題を解くための古典的なアプローチである [40].
A general comparison of modern RL approaches can be found in [29] with a focus on asynchronous learning which is key to scaling up to large problems.
現代のRL手法の一般的な比較は[29]に記載されており，大規模問題へのスケールアップの鍵となる**非同期学習(asynchronous learning)**に焦点が当てられている.
Although value-based methods present many advantages such as seamless off-policy learning, they are known to be prone to instability with function approximation [41].
value-basedの方法は、seamless(?)なoff-policy学習など多くの利点を持つが、関数近似により不安定になりやすいことが知られている[41].
Often, extensive hyper-parameter tuning is required to achieve stable behavior for these approaches.
多くの場合，これらの手法で安定した動作を実現するためには，大規模なハイパーパラメータのチューニングが必要となる.
Despite the practical success of many value-based approaches such as deep Q-learning [30], policy convergence of these algorithms are not well-studied.
深層Q学習[30]のような多くのvalue-basedのアプローチの実用的な成功にもかかわらず，これらのアルゴリズムのpolicy収束(policy convergence)は十分に研究されていない.
Policy-based approaches on the other hand, remain rather stable w.r.t. function approximations given a sufficiently small learning rate.
一方、policy-basedのアプローチは、十分に小さい学習率が与えられると、関数近似に対してむしろ安定な状態を保つ.
We therefore choose to rely on a policy-gradient-based approach, in particular REINFORCE [48], and to adapt this on-policy method to provide reliable policy gradient estimates when training off-policy.
そこで我々は，policy-gradient-basedのアプローチ，特にREINFORCE [48]に依存し，off-policy(=policy外って意味?)の訓練時に信頼できるpolicy gradientの推定を提供するために，このon-policy(=policy上?)の方法を適応させることを選択する.

## 2.2. Neural Recommenders: ニューラルレコメンダー

Another line of work that is closely related to ours is the growing body of literature on applying deep neural networks to recommender systems [11, 16, 37], in particular using recurrent neural networks to incorporate temporal information and historical events for recommendation [6, 17, 20, 45, 49].
特に、recurrent neural network を使用して、推薦のための時間的情報と履歴的イベントを組み込むことができる.[6, 17, 20, 45, 49].
We employed similar network architectures to model the evolving of user states through interactions with the recommender system.
我々は、**推薦システムとのInteractionを通じてユーザの状態(state)が進化することをモデル化するために**、同様のネットワークアーキテクチャを採用した.
As neural architecture design is not the main focus of our work, we refer interested readers to these prior works for more detailed discussions.
ニューラルアーキテクチャの設計は我々の研究の主要な焦点ではないため、より詳細な議論についてはこれらの先行研究を参照するよう読者に勧める.

## 2.3. Bandit Problems in recommender systems:

On-line learning methods are also popular to quickly adapt recommendation systems as new user feedback becomes available.
また、新しいユーザからのfeedbackが利用可能になったときに、推薦システムを迅速に適応させるために、オンライン学習法が普及している.
Bandit algorithms such as Upper Confidence Bound (UCB) [3] trade off exploration and exploitation in an analytically tractable way that provides strong guarantees on the regret.
UCB (Upper Confidence Bound) [3]などのバンディット・アルゴリズムは、解析的に扱いやすい方法で探索(exploration)と活用(exploitation)をトレードオフし、regret(後悔?)を強く保証している.
Different algorithms such as Thomson sampling [9], have been successfully applied to news recommendations and display advertising.
**Thomson sampling[9]のような異なるアルゴリズムは、ニュース推薦やディスプレイ広告にうまく適用されている**.(ほうほう...!!)
Contextual bandits offer a contextaware refinement of the basic on-line learning approaches and tailor the recommendation toward user interests [27].
Contextual bandits は、基本的なオンライン学習アプローチを**context-awareに改良**し、ユーザの興味に合わせた推薦を行う [27].
Agarwal et al. [2] aimed to make contextual bandits tractable and easy to implement.
Agarwal ら [2] は Contextual bandits を扱いやすく，簡単に実装できるようにすることを目指した.
Hybrid methods that rely on matrix factorization and bandits have also been developed to solve cold-start problems in recommender systems [28].
また、推薦システムにおけるコールドスタート問題を解決するために、**行列分解とバンディットによるハイブリッド手法**も開発されている[28].

## 2.4. Propensity Scoring and Reinforcement Learning in Recommender Systems: Propensity Scoring and Reinforcement Learning in Recommender Systems:

The problem of learning off-policy [31, 33, 34] is pervasive in RL and affects policy gradient generally.
off-policy学習の問題[31, 33, 34]はRLに広く存在し，一般にpolicy gradientに影響する.
As a policy evolves so does the distribution under which gradient expectations are computed.
policy が進化するにつれて，"**gradientの期待値が計算される分布**"(なにそれ...?)も進化する.
Standard approaches in robotics [1, 36] circumvent this issue by constraining policy updates so that they do not change the policy too substantially before new data is collected under an updated policy, which in return provides monotonic improvement guarantees of the RL objective.
ロボット工学における標準的なアプローチ[1, 36]は，更新されたpolicyの下で新しいデータが収集される前に，policyをあまり大きく変更しないようにpolicy更新を制約することによってこの問題を回避し，その代わりにRL目的の単調改善保証(? monotonic improvement guarantees)を提供するものである.
Such proximal methods are unfortunately not applicable in the recommendations setting where item catalogues and user behaviors change rapidly, and therefore substantial policy changes are required.
このような近接手法は，残念ながら，**アイテムカタログやユーザの行動が急速に変化するため，大幅なpolicy変更が必要となる推薦システムの設定には適用できない**.
Meanwhile feedback is slow to collect at scale w.r.t. the large state and action space.
また、state space や action space が大きいため、feedbackはその収集に時間がかかる.
As a matter of fact, offline evaluation of a given policy is already a challenge in the recommender system setting.
実際、推薦システムでは、**オフラインでpolicyを評価することは既に課題となっている**.(これは推薦システムの精度的なオフライン評価の課題と関連するんだろうか...?)
Multiple off-policy estimators leveraging inverse-propensity scores, capped inverse-propensity scores and various variance control measures have been developed [13, 42, 43, 47].
inverse-propensity scores，capped inverse-propensity scores，様々な分散制御手段を活用した複数の**off-policy推定器(estimators)**が開発されてきた [13, 42, 43, 47].
Off-policy evaluation corrects for a similar data skew as off-policy RL and similar methods are applied on both problems.
off-policy evaluationはoff-policy RLと同様にデータの歪みを補正し、同様の手法が両問題に適用される.
Inverse propensity scoring has also been employed to improve a serving policy at scale in [39].
また，Inverse propensity scoring(逆傾向スコアリング)は[39]において，規模に応じた提供policyを改善するために採用されている.
Joachims et al. [21] learns a model of logged feedback for an unbiased ranking model; we take a similar perspective but use a DNN to model the logged behavior policy required for the off-policy learning.
Joachimsら[21]はunbiasedなランキングモデルのために、記録されたfeedbackのモデルを学習する. 我々は同様の観点から、**off-policy学習に必要な、記録されたbehavior policy をモデル化するためにDNNを使用する**.
More recently an off-policy approach has been adapted to the more complex problem of slate recommendation [44] where a pseudo-inverse estimator assuming a structural prior on the slate and reward is applied in conjunction with inverse propensity scoring.
最近、off-policyなアプローチはより複雑なslate推薦(??)の問題に適応され [44]、slate(強化学習のdomain languageっぽい.rewardと同様)と報酬(reward)の構造的事前分布(structural prior)を仮定した疑似逆推定法(pseudo-inverse estimator)が逆傾向スコアリング(inverse propensity scoring)と一緒に適用されている.

# 3. Reinforce Recommender

We begin with describing the setup of our recommender system, and our approach to RL-based recommendation.
まず、我々の推薦システムの構成と、RLに基づく推薦のアプローチについて説明する.

For each user, we consider a sequence of user historical interactions with the system, recording the actions taken by the recommender, i.e., videos recommended, as well as user feedback, such as clicks and watch time.
各ユーザについて、レコメンダーが行ったaction、すなわち、推薦するビデオ(過去に推薦したアイテムリスト)、および、クリックや視聴時間などのuser feedbackを記録した、**システム(推薦システム?)とのユーザの過去のInteraction(=推薦システムがあるアイテムをオススメして、それに対してユーザがどのようなreactionを示したか!)の sequence(順序)**を考慮する.
Given such a sequence, we predict the next action to take, i.e., videos to recommend, so that user satisfaction metrics, e.g., indicated by clicks or watch time, improve.
このような一連の動作が与えられると、次にとるべき動作、すなわち、推奨する動画を予測し、クリック数や視聴時間などのユーザー満足度の指標を向上させる.

We translate this setup into a Markov Decision Process (MDP) (S, A, P, 𝑅, 𝜌0,𝛾) where
この設定をマルコフ決定過程(Markov Decision Process) $(S, A, P, R, \rho_0,\gamma)$に変換する.

- S: a continuous state space describing the user states; S: ユーザーの状態を記述する連続的な状態空間。
- A: a discrete action space, containing items available for recommendation; A: 推薦可能なアイテムを含む、離散的な行動空間。
- $P: S \times A \times S \rightarrow \mathbb{R}$ is the state transition probability; P : S × A × S → R は状態遷移確率である。
- $R: S \times A \rightarrow \mathbb{R}$ is the reward function, where 𝑟(𝑠, 𝑎) is the immediate reward obtained by performing action 𝑎 at user state 𝑠; 𝑅 : S × A → R は報酬関数で、$r(s, a)$ はユーザの状態𝑠で行動𝑎を行うことによって得られる即時報酬である.

- 𝜌0 is the initial state distribution; ᜌは初期状態分布である。

- 𝛾 is the discount factor for future rewards. Ǿは、将来の報酬に対する割引係数である。

We seek a policy 𝜋 (𝑎|𝑠) that casts a distribution over the item to recommend 𝑎 ∈ A conditional to the user state 𝑠 ∈ S, so as to maximize the expected cumulative reward obtained by the recommender system,
推薦システムが得る期待累積報酬を最大化するように、ユーザの状態ᵄ∈Sを条件として、推薦するアイテムᵎ∈Aに対して分布を投げかける方針𝑠を模索します,

$$
\max_{\pi} J(\pi) = E_{\tau \sim \pi}[R(\tau)],
\\
\text{where } R(\tau) = \sum_{t=0}^{|\tau|} r(s_t, a_t)
$$

Here the expectation is taken over the trajectories $\tau = (s_0, 𝑎_0, s_1, \cdots)$ obtained by acting according to the policy: $s_0 \sim \rho_0, a_t \sim \pi(·|s_t), s_{t+1} \sim P(·|s_t, a_t)$. In other words,
ここで、上式の期待値は、policy(& initial state distribution & state transition function): $s_0 \sim \rho_0, a_t \sim \pi(·|s_t), s_{t+1} \sim P(·|s_t, a_t)$ に従ってactionした事で得られる **trajectories(軌道 = stateとactionの結果)**$\tau = (s_0, a_0, s_1, \cdots)$ を入力として計算される.

よって上式の$J(\pi)$を書き換えると、以下のようになる.

$$
J(\pi) = E_{s_0 \sim \rho_0, a_t \sin \pi(\cdot|s_t), s_{t+1} \sim P(\cdot|s_t, a_t)}[\sum_{t=0}^{|\tau|} r(s_t, a_t)]
\\
= E_{s_t \sim d_t^{\pi}(\cdot), a_t \sin \pi(\cdot|s_t)}[\sum_{t'= t}^{|\tau|} r(s_{t'}, a_{t'})]
\tag{1}
$$

ここで、

- 式(1)の一段目に関して.
  - 初期状態 $s_0$ は、 initial state distributionに基づき生成される.
  - 時間tにおけるaction $a_t$ は、時間tにおけるstate $s_t$で条件づけた(=入力とした)policy関数に基づき生成される.
  - 時間t+1における state $s_{t+1}$は、$a_t$と$s_t$で条件づけた(=入力とした)state transaction probability関数$P$に基づいて生成される.
- 式(1)の二段目に関して.
  - $d_t^{\pi}(\cdot)$は、policy $\pi$ の下で時間tにおける (discounted) **state visitation frequency(状態訪問頻度)**を意味する.
    - state visitation frequency(状態訪問頻度): agentが学習中にどのstateにどの程度の頻度でvisitしたかを示す指標.
    - reward functionの推定に役立つらしい.
    -

Here 𝑑 𝜋 𝑡 (·) denotes the (discounted) state visitation frequency at time 𝑡 under the policy 𝜋. Different families of methods are available to solve such an RL problems: Q-learning [38], Policy Gradient [26, 36, 48] and black box optimization [15]. Here we focus on a policy-gradient-based approach, i.e., REINFORCE [48].
このような RL 問題を解くために、様々な手法のfamily(?)が利用可能である.(なるほど...**期待累積報酬を最大化するようなpolicy関数を探索する事**がRLの基本的なタスクなのかな...!)
Q-learning [38], Policy Gradient [26, 36, 48], Black Box Optimization [15] など.
ここでは、policy-gradientに基づくアプローチ、すなわち、REINFORCE [48]に注目する.

We assume a function form of the policy 𝜋𝜃 , parametrised by 𝜃 ∈ R 𝑑 .
policy $\pi_{\theta}$ は $\theta \in \mathbb{R}^{d}$ でパラメータ化された関数形式を仮定する. (dはパラメータ数. $\theta$ はパラメータベクトル.)
The gradient of the expected cumulative reward with respect to the policy parameters can be derived analytically thanks to the “log-trick”, yielding the following REINFORCE gradient
**policy関数のパラメータに対する期待累積報酬(expected cumulative reward)の勾配**は，"log-trick(??)"によって解析的(なるほど!じゃあ普通に解いたら得られる?)に導かれ，以下のREINFORCE gradientを得ることができる.

$$
\nabla_{\theta} J(\pi_{\theta}) =
E_{s_t \sim d_t^{\pi}(\cdot), a_t \sin \pi(\cdot|s_t)}
[(\sum_{t'= t}^{|\tau|} r(s_{t'}, a_{t'})) \nabla_{\theta} \log{\pi_{\theta}(a_t|s_t)}]
\\
= \sum_{s_t \sim d_t^{\pi}(\cdot), a_t \sin \pi(\cdot|s_t)}
R_{t}(s_t, a_t) \nabla_{\theta} \log \pi_{\theta}(a_t|s_t)
\tag{2}
$$

Here $R_{t}(s_t, a_t)= \sum_{t'=t}^{|\tau|} r(s_{t'}, a_{t'})$ is the discounted future reward for action at time 𝑡. The discounting factor 𝛾 is applied to reduce variance in the gradient estimate. In on-line RL, where the policy gradient is computed on trajectories generated by the policy under consideration, the monte carlo estimate of the policy gradient is unbiased.
ここで、 $R_{t}(s_t, a_t)= \sum_{t'=t}^{|\tau|} r(s_{t'}, a_{t'})$ は時刻tにおけるactionに対する割引後の将来報酬(時刻t以降に獲得する報酬の合計の予測値??discountって何?)である.
割引係数$\gamma$は、勾配推定値の分散を減らすために適用される.(ほう...)
オンラインRLでは、policy-gradientは検討中のpolicyによって生成された軌道で計算されるため、policy-gradientのモンテカルロ推定値は不偏である.(不偏推定量になる理由はよくわからない...)

# 4. Off-Policy Correction(補正)

Unlike classical reinforcement learning, our learner does not have real-time interactive control of the recommender due to learning and infrastructure constraints.
古典的な強化学習とは異なり、我々の学習器は、学習とインフラの制約から、レコメンダーをリアルタイムにインタラクティブに制御することができない.
In other words, we cannot perform online updates to the policy and generate trajectories according to the updated policy immediately.
つまり、学習者はオンラインでpolicyを更新し、更新されたpolicyに従った軌道を即座に生成することができない.
Instead we receive logged feedback of actions chosen by a historical policy (or a mixture of policies), which could have a different distribution over the action space than the policy we are updating.
その代わりに、我々は、更新中のpolicyとは異なるaction space上の分布を持ちうる過去のpolicy(=現在運用中の推薦モデル?)(またはpolicyの混合物)により選択されたactionのログfeedbackを受け取る.

We focus on addressing the data biases that arise when applying policy gradient methods under this setting.
我々は，この設定のもとでpolicy-gradient法を適用する際に生じるデータの偏りを解決することに焦点を当てる.
In particular, the fact that we collect data with a periodicity of several hours and compute many policy parameter updates before deploying a new version of the policy in production implies that the set of trajectories we employ to estimate the policy gradient is generated by a different policy.
特に，数時間の周期でデータを収集し，**新バージョンのpolicyを本番に導入する前に多くのpolicy関数のパラメータの更新を計算する**という事実は，**我々がpolicy-gradientを推定するために用いる軌道のセット(=dataset)が、異なるpolicyによって生成されていることを意味する**．
Moreover, we learn from batched feedback collected by other recommenders as well, which follow drastically different policies.
さらに，他のレコメンダーが収集したfeedbackも一括して学習するが，それらは全く異なるpolicyに従っている.
A naive policy gradient estimator is no longer unbiased as the gradient in Equation (2) requires sampling trajectories from the updated policy 𝜋𝜃 while the trajectories we collected were drawn from a combination of historical policies 𝛽.
式(2)のgradientは更新されたpolicy $\pi_{\theta}$ から軌道をサンプリングする必要がある一方，我々が収集した軌道は過去のpolicy $\beta$ の組み合わせから引き出されているため，単純なpolicy-gradient の推定器はもはや不偏ではない.
(なるほど...!強化学習したいpolicyそのものを本番運用しているケースでは、受け取ったfeedback=軌道を用いてほぼ正しい勾配(不偏推定量=平均的に真の勾配と等しいみたいなイメージ)を計算可能で、結果として期待累積報酬を最大にするようなpolicyに更新=強化していけるはず.)
(しかし、強化学習したいpolicyとは別のpolicyを本番運用しているケースでは、受け取ったfeedback=軌道を式(2)に当てはめて計算しても見当違いな勾配になってしまう. 結果として変な方向にpolicyを更新していってしまう...!)

We address the distribution mismatch with importance weighting [31, 33, 34].
分布の不一致には、**重要度重み付け**[31, 33, 34]を用いて対処する.
Consider a trajectory $\tau = (s0, a0, s1, \cdots)$ sampled according to a behavior policy $\beta$, the off-policy-corrected gradient estimator is then:
behavior policy $\beta$ に従ってサンプリングされた軌道 $\tau = (s0, a0, s1, \cdots)$ を考慮すると、off-policy-corrected gradient estimator(off-policy補正勾配推定器)は、次のようになる:

$$
\nabla_{\theta} J(\pi_{\theta})
= \sum_{s_t \sim d_t^{\beta}(\cdot), a_t \sin \beta(\cdot|s_t)}
w(s_t, a_t) R_{t}(s_t, a_t) \nabla_{\theta} \log \pi_{\theta}(a_t|s_t)
\tag{3}
$$

where below is the importance weight.
ここで、以下は重要度重みである.

$$
w(s_t, a_t)
= \frac{d_t^{\pi}(s_t)}{d_t^{\beta}(s_t)}
\times \frac{\pi_{\theta}(a_t|s_t)}{\beta(a_t|s_t)}
\times \Pi_{t'=t+1}^{|\tau|} \frac{\pi_{\theta}(a_{t'}|s_{t'})}{\beta(a_{t'}|s_{t'})}
\tag{3.5}
$$

This correction produces an unbiased estimator whenever the trajectories are collected with actions sampled according to 𝛽.
この補正により、別のpolicy$\beta$に従ってサンプリングされたactionでtrajectories(軌道)が収集された場合は、常に不偏の推定値が得られる(ほう,
言うね...!).
However, the variance of the estimator can be huge when the difference in 𝜋𝜃 and the behavior policy 𝛽 results in very low or high values of the importance weights.
しかし、更新対象のpolicy $\pi$ と 別のpolicy $\beta$ の違いにより重要度重みが非常に小さいか大きい場合には、**推定値の分散が大きくなる**可能性がある.(それでも不偏性は失われないのか...)

To reduce the variance of each gradient term, we take the firstorder approximation and ignore the state visitation differences under the two policies as the importance weights of future trajectories, which yields a slightly biased estimator of the policy gradient with lower variance:
各勾配項の分散を小さくするために，1次近似(?)を行い，将来の軌道の重要度重みとして2つの政策下の状態訪問差分を無視することで，分散を小さくしたpolicy-gradientのやや偏った(=不偏性は失われた)推定値を得ることができた．

$$
\nabla_{\theta} J(\pi_{\theta})
\approx \sum_{s_t \sim d_t^{\beta}(\cdot), a_t \sin \beta(\cdot|s_t)}
\frac{\pi_{\theta}(a_t|s_t)}{\beta(a_t|s_t)} % 重みがraughになった?
R_{t}(s_t, a_t) \nabla_{\theta} \log \pi_{\theta}(a_t|s_t)
\tag{4}
$$

Achiam et al. [1] prove that the impact of this first-order approximation on the total reward of the learned policy is bounded in magnitude by 𝑂 𝐸𝑠∼𝑑 𝛽 [𝐷𝑇𝑉 (𝜋
𝛽) [𝑠]]) where 𝐷𝑇𝑉 is the total variation between 𝜋 (·
Achiamら. [1]は、この一次近似の影響を証明する. 学習したpolicyの総報酬に関する次数近似は、𝑂𝐸𝑠 𝑑 [𝐷𝑇 (𝑠)] によって大きさが拘束される. ここで、𝐷𝑇𝑉は𝑠 (-|𝑠)と𝛽𝑑の下での割引未来状態分布の合計変動である. この推定器は、正確なoff-policy補正の分散をトレードオフしつつ、非補正のpolicy-gradientの大きなバイアスを補正し、on-policy学習により適したものである.(いいとこ取り的なestimatorなのか...)

## 4.1. Parametrising the policy $\pi_{\theta}$

We model our belief on the user state at each time 𝑡, which capture both evolving user interests using a 𝑛-dimensional vector, that is, s𝑡 ∈ R 𝑛 .
各時間 t におけるユーザのstateに関するpolicyをモデル化し、 n次元ベクトル、すなわち $s_t \in \mathbb{R}^n$を用いて進化する両方のユーザの興味を捕捉する.
The action taken at each time 𝑡 along the trajectory is embedded using an 𝑚-dimensional vector $u_{a_t} \in \mathbb{R}^n$.
軌跡(trajectory)に沿った各時刻$t$で取られたactionは, $u_{a_t} \in \mathbb{R}^n$ を用いて埋め込まれている.
We model the state transition P : S×A×S with a recurrent neural network [6, 49]
**state transition(状態遷移) P : S×A×S を recurrent neural network でモデル化**する[6, 49]:

$$
s_{t+1} = f(s_t, u_{a_t})
$$

We experimented with a variety of popular RNN cells such as Long Short-Term Memory (LSTM) [18] and Gated Recurrent Units (GRU) [10], and ended up using a simplified cell called Chaos Free RNN (CFN) [24] due to its stability and computational efficiency.
我々は、LSTM（Long Short-Term Memory） [18] やGRU（Gated Recurrent Units） [10] などの有名なRNNセルをいろいろと実験した結果、安定性と計算効率の点から、Chaos Free RNN（CFN） [24] という簡易セルを使うことにした.
The state is updated recursively as
stateは、以下のように**再帰的(recursively)**に更新される.

$$
s_{t+1} =  f(s_t, u_{a_t}) = z_t \odot \tanh(s_t) + i_t \odot \tanh(W_{a}u_{a_t})
\\
z_t = \sigma(U_{z}s_{t} + W_{z}u_{a_t} + b_{z})
\\
i_t = \sigma(U_{i}s_{t} + W_{i}u_{a_t} + b_{i})
\\
\tag{5}
$$

where $z_t, i_t \in \mathbb{R}^n$ are the update and input gate respectively.
ここで、 $z_t, i_t \in \mathbb{R}^n$ はそれぞれ update gate と input gate である.

Conditioning on a user state s, the policy 𝜋𝜃 (𝑎|s) is then modeled with a simple softmax,
ユーザのstate $s$ を条件として、policy $\pi_{\theta}(a|s)$は、**単純な softmax** でモデル化される.

$$
\pi_{\theta}(a|s) = \frac{\exp(s^T v_{a} / T)}{\sum_{a'\in A} \exp(s^T v_{a'}/T)}
\tag{6}
$$

where v𝑎 ∈ R 𝑛 is another embedding for each action 𝑎 in the action space A and 𝑇 is a temperature that is normally set to 1.
ここで、 $v_a \in \mathbb{R}^{n}$ は action space $A$ における各action $a$ の別の埋め込みベクトル(actionの埋め込みベクトルが二種類ある?)で、 $T$ は通常 1 に設定される temperature である.
Using a higher value in 𝑇 produces a smoother policy over the action space.
$T$ の値を大きくすることで、action space 上でよりスムーズなpolicyが実現される.
The normalization term in the softmax requires going over all the possible actions, which is in the order of millions in our setting.
softmax の正規化項はすべての可能な action を調べる必要があり、我々の設定では数百万のオーダーとなる.
To speed up the computation, we perform sampled softmax [4] during training.
この計算を高速化するために、我々は学習時に sampled softmax[4]を実行する.
At serving time, we used an efficient nearest neighbor search algorithm to retrieve top actions and approximate the softmax probability using these actions only, as detailed in section 5.
このとき、効率的な最近傍探索アルゴリズムを用いて**上位のactionを取得し、これらのactionのみを用いてsoftmax確率を近似する**（セクション5で詳述）.

In summary, the parameter 𝜃 of the policy 𝜋𝜃 contains the two action embeddings U ∈ R 𝑚× |A | and V ∈ R 𝑛× |A | as well as the weight matrices U𝑧, U𝑖 ∈ R 𝑛×𝑛 , W𝑢, W𝑖 , W𝑎 ∈ R 𝑛×𝑚 and biases b𝑢, b𝑖 ∈ R 𝑛 in the RNN cell.
まとめると、policy $\pi_{\theta}$ のパラメータ $\theta$ は、二種類の action 埋め込み $U \in \mathbb{R}^{m \times |A|}$ と $V \in \mathbb{R}^{n \times |A|}$ を 含んでいる. また、重み行列 $U_z, U_i \in \mathbb{R}^{n \times n}$ と $W_u, W_i, W_a in \mathbb{R}^{n \times m}$ 及びバイアス項 $b_{u}, b_{i} \in \mathbb{R}^{n}$ を含んでいる.
Figure 1 shows a diagram describing the neural architecture of the main policy 𝜋𝜃.
図1は、main(?) policy $\pi_{\theta}$ のneural architecture を説明する図である.
Given an observed trajectory 𝜏 = (𝑠0, 𝑎0, 𝑠1, · · · ) sampled from a behavior policy 𝛽, the new policy first generates a model of the user state s𝑡+1 by starting with an initial state s0 ∼ 𝜌0 1 and iterating through the recurrent cell as in Equation (5).
policy $\beta$ からサンプリングされた観測されたtrajectory(軌道) $\tau = (s_0, a_0, s_1, \cdots)$ が与えられると、新しいpolicyはまずitinial state $s_0 \sim \rho_{0}$ で開始し、式(5) のように recurrent セルを反復して user state $s_{t+1}$ のモデルを生成する.
Given the user state s𝑡+1 the policy head casts a distribution on the action space through a softmax as in Equation (6).
With 𝜋𝜃 (𝑎𝑡+1 |s𝑡+1), we can then produce a policy gradient as in Equation (4) to update the policy.
user state $s_{𝑡+1}$が与えられると，policy head(policyの先端?)は式(6)のようにsoftmaxを用いて action state に分布(=確率質量分布)を投影する．
$\pi_{\theta}(a_{t+1}|s_{t+1})$ が与えられる事で、式(4) のように policy-gradient を生成し、policy を更新することができる(i.e. 期待累積報酬を最大化するようなpolicyに近づける事ができる...!).

## 4.2. Estimating the behavior policy 行動ポリシーの推定

One difficulty in coming up with the off-policy corrected estimator in Equation (4) is to get the behavior policy 𝛽.
式(4)のoff-policy補正推定量を考える上で難しいのは、behavior policy $\beta$ を得ることである.
Ideally, for each logged feedback of a chosen action we received, we would like to also log the probability of the behavior policy choosing that action.
理想的には、**受け取った chosen action のフィードバックを記録するごとに、そのactionを選択するbehavior policy の確率も記録したいところ**である.
Directly logging the behavior policy is however not feasible in our case as (1) there are multiple agents in our system, many of which we do not have control over, and (2) some agents have a deterministic policy, and setting 𝛽 to 0 or 1 is not the most effective way to utilize these logged feedback.
しかし、behavior policy(の出力する確率の値?) を直接ログに記録することは、(1)我々のシステムには複数のagentが存在し、その多くは我々が制御できない、(2)いくつかのagentは決定論的方針(deterministic policy)を持っており、 $\beta$ を0または1に設定することは、これらの記録されたフィードバックを活用する最も有効な方法ではないため、このケースでは実現可能であるとはいえない.

Instead we take the approach first introduced in [39], and estimate the behavior policy 𝛽, which in our case is a mixture of the policies of the multiple agents in the system, using the logged actions.
その代わりに、我々は[39]で最初に紹介されたアプローチを取り、**システム内の複数のagentの policy の混合であるbehavior policy $\beta$** を、記録されたactionを使用して推定する.
Given a set of logged feedback D = {(s𝑖 , 𝑎𝑖),𝑖 = 1, · · · , 𝑁}, Strehl et al.[39] estimates ˆ𝛽 (𝑎) independent of user state by aggregate action frequency throughout the corpus.
記録されたフィードバック $D = {(s_i, a_i), i = 1, \cdots N}$ のセットが与えられたとき、Strehlら[39]はコーパス全体のaction頻度を集約して user state に依存しない $\hat{\beta}_{\theta}$ を推定する.
In contrast, we adopt a context-dependent neural estimator.
これに対し、我々はcontextに依存(?)したニューラル推定を採用する.
For each state-action pair (𝑠, 𝑎) collected, we estimate the probability ˆ𝛽𝜃 ′ (𝑎𝑠) that the mixture of behavior policies choosing that action using another softmax, parametrised by 𝜃 ′ .
収集した各state-actionペア $(s, a)$ について、aでパラメタライズされた別のsoftmaxを用いて、混合behavior policy がその action を選択する確率 $\hat{\beta_{\theta'}}(a|s)$ を推定する.
As shown in Figure 1, we re-use the user state 𝑠 generated from the RNN model from the main policy, and model the mixed behavior policy with another softmax layer.
図1に示すように、main policy のRNNモデルから生成された user state $s$ を再利用し、別のソフトマックス層で混合behavior policy をモデル化する.
To prevent the behavior head from intefering with the user state of the main policy, we block its gradient from flowing back into the RNN.
behavior head(=actionの最後尾?)が main policy のuser state に干渉するのを防ぐため、その勾配がRNNに逆流するのをブロックしている.
We also experimented with separating the 𝜋𝜃 and 𝛽𝜃 ′ estimators, which incurs computational overhead for computing another state representation but does not results in any metric improvement in offline and live experiments.
また、$\pi_{\theta}$ と $\beta_{\theta'}$ の推定器を分離する実験も行いましたが、これは別のstate表現を計算するための計算オーバーヘッドが発生しますが、オフラインおよびライブ実験ではメトリックの向上にはつながらなかった.

Despite a substantial sharing of parameters between the two policy heads 𝜋𝜃 and 𝛽𝜃 ′, there are two noticeable difference between them:
2つのポリシーヘッド $\pi_{\theta}$ と $\beta_{\theta'}$ の間でパラメータがかなり共有されているにもかかわらず、両者の間には2つの顕著な違いがある.
(1) While the main policy 𝜋𝜃 is effectively trained using a weighted softmax to take into account of long term reward, the behavior policy head 𝛽𝜃 ′ is trained using only the state-action pairs;
(1) main policy(=更新したいpolicy??) $\pi_{\theta}$ が長期的な報酬を考慮した重み付きソフトマックスを効果的に用いて学習されるのに対し、behavior policy(=今運用されてるpolicy?) $\beta_{\theta'}$ はstate-actionペアのみを用いて学習される.
(2) While the main policy head 𝜋𝜃 is trained using only items on the trajectory with non-zero reward 3 , the behavior policy 𝛽𝜃 ′ is trained using all of the items on the trajectory to avoid introducing bias in the 𝛽 estimate.
(2) main policy head $\pi_{\theta}$ が軌道上の非ゼロ報酬のitemのみを用いて学習するのに対し、behavior policy $\beta_{\theta'}$ は軌道上の全てのitemを用いて学習し、$\beta$ の推定値に偏りが生じないようにする.

In [39], it is argued that that a behavior policy that is deterministically choosing an action 𝑎 given state 𝑠 at time 𝑡1 and action 𝑏 at time 𝑡2 can be treated as randomizing between action 𝑎 and 𝑏 over the timespan of the logging.
[39]では、時間 $t_1$ におけるstate $s_1$ におけるaction $a$ と、時間 $t_2$ における行動 $b$ を決定論的に選択する行動方針は、ログの時間幅においてaction $a$ とaction $b$ の間でランダム化すると扱うことができると論じている.(??)
Here we could argue the same point, which explains why the behavior policy could be other than 0 or 1 given a deterministic policy.
ここで、決定論的な方針が与えられた場合に、behavior policy が0または1以外になりうる理由を説明する、同じ点を論じることができる.
In addition, since we have multiple policies acting simultaneously, if one policy is determinstically choosing action 𝑎 given user state 𝑠, and another one is determinstically choosing action 𝑏, then estimating ˆ𝛽𝜃 ′ in such a way would approximate the expected frequency of action 𝑎 being chosen under the mixture of these behavior policies given user state 𝑠.
また、複数の policy が同時に作用しているので、あるpolicyがuser state $s$ を与えられたときに決定論的にaction $a$ を選択し、別のポリシーが決定論的に行動 $b$ を選択しているとすると、そのように $\hat{\beta_{\theta'}}$ を推定すると、user state $s$ を与えられたこれらのbehavior policy の混合下で行動 $a$ が選ばれる期待頻度に近似することができるだろう.

## 4.3. Top-𝐾 Off-Policy Correction Top-ᵃ Off-Policy Correction (オフポリシー補正)

Another challenge in our setting is that our system recommends a page of 𝑘 items to users at a time. As users are going to browse through (the full or partial set of) our recommendations and potentially interact with more than one item, we need to pick a set of relevant items instead of a single one. In other words, we seek a policy Π𝜃 (𝐴|𝑠), here each action 𝐴 is to select a set of 𝑘 items, to maximize the expected cumulative reward,
私たちの設定におけるもう一つの課題は、私たちのシステムが一度にk個のアイテムのページをユーザに推薦することである.
ユーザは推薦されたアイテムの全部または一部を閲覧し、複数のアイテムに触れる可能性があるため、単一のアイテムではなく、関連するアイテムのセットを選択する必要がある.
言い換えれば、我々はpolicy $\Pi_{\theta}(A|s)$ を求め、ここで各action $A$ は、"期待累積報酬を最大化するような**k個のアイテムのセット**を選択する"事を意味する.

$$
\max_{\theta} J(\Pi_{\theta}) E_{s_t \sim d_t^{\Pi}(\cdot), A_t \sim \Pi_{\theta}(\cdot|s_t)}[R_t(s_t, A_t)]
$$

Here 𝑅𝑡 (𝑠𝑡 , 𝐴𝑡) denotes the cumulative return of the set 𝐴𝑡 at state 𝑠𝑡 .
ここで、$R_t(s_t, A_t)$ は、state $s_t$ における集合 $A_t$ の累積報酬を示す.
Unfortunately, the action space grows exponentially under this set recommendation formulation [44, 50], which is prohibitively large given the number of items we choose from are in the orders of millions.
残念ながら、**この集合推薦の定式化ではaction space が指数関数的に増大**し [44, 50]、選択するアイテムの数が数百万のオーダーであることを考えると、法外に大きい.

To make the problem tractable, we assume that a user will interact with at most one item from the returned set 𝐴.
問題を扱いやすくするために、我々は、ユーザが返された集合 $A$ から最大1つのアイテムと interaction することを仮定する.
In other words, there will be at most one item with non-zero cumulative reward among 𝐴.
言い換えれば、"**$A$ の中でゼロでない累積報酬を持つアイテムは、せいぜい1つであろう**"という仮定をおく.
We further assume that the expected return of an item is independent of other items chosen in the set 𝐴 4 .
さらに，あるアイテムの期待リターンは，集合$A$の中で選ばれた他のアイテムとは独立であると仮定する．
With these two assumptions, we can reduce the set problem to
これら二つの仮定により、集合問題は次のように縮小できる.

$$
J(\Pi_{\theta}) E_{s_t \sim d_t^{\Pi}(\cdot), a_t \in A_t \sim \Pi_{\theta}(\cdot|s_t)}[R_t(s_t, a_t)]
$$

Here 𝑅𝑡 (𝑠𝑡 , 𝑎𝑡) is the cumulative return of the item 𝑎𝑡 the user interacted with, and 𝑎𝑡 ∈ 𝐴𝑡 ∼ Π𝜃 (·|𝑠𝑡) indicates that 𝑎𝑡 was chosen by the set policy. Furthermore, we constrain ourselves to generate the set action 𝐴 by independently sampling each item 𝑎 according to the softmax policy 𝜋𝜃 described in Equation (6) and then de-duplicate. As a result, the probability of an item 𝑎 appearing in the final non-repetitive set 𝐴 is simply 𝛼𝜃 (𝑎|𝑠) = 1 − (1 − 𝜋𝜃 (𝑎|𝑠))𝐾, where 𝐾 is the number of times we sample.
ここで、 $R_t(s_t, a_t)$ はユーザがinteractionしたアイテム$at$の累積リターン、$a_t \in A_t \sim \Pi_{\theta}(\cdot|s_t)$ はset policy によって $a_t$ が選択されたことを表す.
さらに、式（6）で記述したソフトマックスポリシー $\pi_{\theta}$ に従って各アイテム $a$ を独立にサンプリングしてセットアクション$A$を生成し、重複を解除するという制約を設けている.
その結果、アイテム $a$ が最終的な非反復集合$A$に現れる確率は、単純に $\alpha_{\theta}(a|s) = 1 - (1 - \pi_{\theta}(a|s))^K$ 、ただし$K$はサンプリングの回数とする.

We can then adapt the REINFORCE algorithm to the set recommendation setting by simply modifying the gradient update in Equation (2) to
そこで、REINFORCEアルゴリズムを集合推薦の設定に適応させるには、式（2）の勾配更新を次のように変更するだけでよい.

$$
\sum_{s_t \sim d_t^{\pi}(\cdot), a_t \sim \alpha_{\theta}(\cdot|s_t)} R_t(s_t, a_t) \nabla_{\theta} \log \alpha_{\theta}(a_t|s_t)
$$

Accordingly, we can update the off-policy corrected gradient in Equation (4) by replacing 𝜋𝜃 with 𝛼𝜃 , resulting in the top-𝐾 off-policy correction factor:
したがって、式(4)の $\pi_{\theta}$ を $\alpha_{\theta}$ に置き換えてoff-policy補正勾配を更新すれば、**top-K off-policy補正係数**が得られる.

$$
\sum_{s_t \sim d_{t}^{\pi}(\cdot), a_t \sim \beta(\cdot|s_t)}
[\frac{\alpha_{\theta}(a_t|s_t)}{\beta_{\theta}(a_t|s_t)} 
R_{t}(s_t, a_t) 
\nabla_{\theta} \log \alpha_{\theta}(a_t|s_t)]
\\
= \sum_{s_t \sim d_{t}^{\pi}(\cdot), a_t \sim \beta(\cdot|s_t)}
[\frac{\pi_{\theta}(a_t|s_t)}{\beta_{\theta}(a_t|s_t)} 
\frac{\partial \alpha_{\theta}(a_t|s_t)}{\partial \pi(a_t|s_t)} 
R_{t}(s_t, a_t) 
\nabla_{\theta} \log \pi_{\theta}(a_t|s_t)]
\tag{7}
$$

Comparing Equation (7) with Equation (4), the top-𝐾 policy adds an additional multiplier of
式（7）と式（4）を比較すると、top-K policy は、元の off-policy補正係数 $\frac{\pi_{\theta}(a_t|s_t)}{\beta_{\theta}(a_t|s_t)}$ に次の乗数(multiplier)を追加している.

$$
\lambda_{K}(s_t, a_t) = \frac{\partial \alpha_{\theta}(a_t|s_t)}{\partial \pi(a_t|s_t)} 
= K(1 - \pi_{\theta}(a_t|s_t))^{K-1}
\tag{8}
$$

Now let us take a closer look at this additional multiplier:
では、この追加倍率について詳しく見ていこう.

- As 𝜋𝜃 (𝑎|𝑠) → 0, 𝜆𝐾 (𝑠, 𝑎) → 𝐾. The top-𝐾 off-policy correction increases the policy update by a factor of 𝐾 comparing to the standard off-policy correction;
- $\pi_{\theta}(a_t|s_t) -> 0$ 即ち $\lambda_{K}(s_t, a_t) -> K$ の場合、top-K off-policy補正は標準のoff-policy補正と比較して、policyの更新をK倍に増加させる.

- As 𝜋𝜃 (𝑎|𝑠) → 1, 𝜆𝐾 (𝑠, 𝑎) → 0. This multiplier zeros out the policy update.
- $\pi_{\theta}(a_t|s_t) -> 1$ 即ち $\lambda_{K}(s_t, a_t) -> 0$ の場合、この乗数はpolicyの更新をゼロにする.

- As 𝐾 increases, this multiplier reduces the gradient to zero faster as 𝜋𝜃 (𝑎|𝑠) reaches a reasonable range. reaches a reasonable range.
- Kが大きい場合、この乗数は、$\pi_{\theta}(a_t|s_t)$ が合理的な範囲に達すると、より速く勾配(policy-gradient)をゼロにすることができる.(ゼロになったら更新が停止する.これって良いことなんだっけ?)

In summary, when the desirable item has a small mass in the softmax policy 𝜋𝜃 (·|𝑠), the top-𝐾 correction more aggressively pushes up its likelihood than the standard correction. 
要約すると、ソフトマックス policy (関数) $\pi_{\theta}(a_t|s_t)$ において望ましいアイテム(desirable item??)の質量(=確率質量?)が小さい場合、**top-K補正係数は標準の補正係数よりも積極的にその尤度を押し上げる**. 
Once the softmax policy 𝜋𝜃 (·|𝑠) casts a reasonable mass on the desirable item (to ensure it will be likely to appear in the top-𝐾), the correction then zeros out the gradient and no longer tries to push up its likelihood. 
ソフトマックスポリシー $\pi_{\theta}(a_t|s_t)$ が望ましいアイテム(desirable item??)に適度な質量(確率質量)を与えると（top-K に登場する可能性を確保するため）、補正係数は勾配をゼロにして尤度を押し上げようとはしなくなる. 
This in return allows other items of interest to take up some mass in the softmax policy. 
これにより、ソフトマックスポリシーにおいて、他の興味あるあいてむがある程度の質量を占めることができるようになる.
As we are going to demonstrate in the simulation as well as live experiment, while the standard off-policy correction converges to a policy that is optimal when choosing a single item, the top-𝐾 correction leads to better top-𝐾 recommendations.
シミュレーションと実機で実証するように、標準的なオフポリシー補正は1つのアイテムを選択する際に最適なpolicyに収束するが、top-K補正はtop-K推薦 を向上させることにつながる.

## 4.4. Variance Reduction Techniques

As detailed at the beginning of this section, we take a first-order approximation to reduce variance in the gradient estimate. 
本節の冒頭で詳述したように、勾配推定値の分散を減らすために一次近似を行う.
Nonetheless, the gradient can still suffer from large variance due to large importance weight of 𝜔(𝑠, 𝑎) = 𝜋 (𝑎 |𝑠) 𝛽 (𝑎 |𝑠) as shown in Equation (4), Similarly for top-𝐾 off-policy correction. 
それにもかかわらず、勾配は、top-K off-policy補正と同様に、式(4)に示すように、 $w(s,a) = \frac{\pi(a|s)}{\beta(a|s)}$ の**大きな重要度重みによって大きな分散に苦しむことがある**.
Large importance weight could result from (1) large deviation of the new policy 𝜋 (·|𝑠) from the behavior policy, in particular, the new policy explores regions that are less explored by the behavior policy. That is, 𝜋 (𝑎|𝑠) ≫ 𝛽 (𝑎|𝑠) and (2) large variance in the 𝛽 estimate.
大きな重要度重みは、以下の２つの要因から発生する可能性がある.（1）new policy $\pi(\cdot|s)$ の behavior policy(現在のpolicy) からの大きな乖離、特に、new policy が behavior policy によってあまり探索されない領域を探索することに起因すると考えられる. つまり、$\pi(a|s) >> \beta(a|s)$ 、(2) $\beta$ 推定値の分散が大きい.
 
We tested several techniques proposed in counterfactual learning and RL literature to control variance in the gradient estimate.
我々は、**勾配(policy-gradient)推定の分散を制御するため**に、反実仮想学習やRLの文献で提案されているいくつかの手法を検証した.
Most of these techniques reduce variance at the cost of introducing some bias in the gradient estimate.
これらの手法のほとんどは、勾配推定値に何らかのバイアスをもたらす代償として、分散を減少させる.(=不偏推定量ではなくなるが、分散が減少するような手法?)

### 4.4.1. Weight Capping.

The first approach we take is to simply cap the weight [8] as
最初のアプローチとして、weighet を単純に cap(=大きさに上限を設ける?)する[8].

$$
\bar{w}_{c}(s,a) = \min(\frac{\pi(a|s)}{\beta(a|s)}, c)
\tag{9}
$$

Smaller value of $c$ reduces variance in the gradient estimate, but introduces larger bias.
$c$ の値を小さくすると、勾配推定の分散は小さくなるが、バイアスが大きくなる.

### 4.4.2. Normalized Importance Sampling (NIS). 正規化重要度サンプリング(NIS)

Second technique we employed is to introduce a ratio control variate, where we use classical weight normalization [32] defined by:
第二の手法は、**ratio control variate(比率制御変数)**を導入することである. ここで、classical weight normalization(古典的な重みの**正規化**)[32]を用いて、次のように定義する.

$$
\bar{w}_{n}(s,a) = \frac{w(s,a)}{\sum_{(s', a') \sim \beta} w(s', a')}
$$

As E𝛽 [𝜔(𝑠, 𝑎)] = 1, the normalizing constant is equal to 𝑛, the batch size, in expectation.
$E_{\beta}[w(s,a)] = 1$ の場合、正規化定数 $\frac{1}{\sum_{(s', a') \sim \beta} w(s', a')}$ は期待値的にバッチサイズである$n$と等しくなる.
As 𝑛 increases, the effect of NIS is equivalent to tuning down the learning rate.
n が増加すると、NIS の効果は学習率をチューニングすることと等価になる.

### 4.4.3. Trusted Region Policy Optimization (TRPO). TRPO（Trusted Region Policy Optimization）。

TRPO [36] prevents the new policy 𝜋 from deviating from the behavior policy by adding a regularization that penalizes the KL divergence of these two policies.
TRPO [36]は，new policy $\pi$ がbehavior policy $\beta$ から逸脱しないように，これら二つの policy の KL Divergence にペナルティを与える正則化を追加することによって行う.
It achieves similar effect as the weight capping.
これは，weight capping と同様の効果を得ることができる.

# 5. Exploration 探求

As should be clear by this point, the distribution of training data is important for learning a good policy.
ここまでで明らかなように、良い方針を学習するためには学習データの分布が重要である。
Exploration policies to inquire about actions rarely taken by the existing system have been extensively studied.
既存のシステムでほとんど行われない行動を問い合わせる探索方針は広く研究されている。
In practice, brute-force exploration, such as 𝜖-greedy, is not viable in a production system like YouTube where this could, and mostly likely would, result in inappropriate recommendations and a bad user experience.
しかし，YouTube のようなシステムにおいて，𝜖貪欲に探索を行うことは，不適切な推薦やユーザ体験の低下を招く可能性があり，現実的でないと考えられる．
For example, Schnabel et al. [35] studied the cost of exploration.
例えば、Schnabel ら [35] は探索のコストについて研究しています。

Instead we employ Boltzmann exploration [12] to get the benefit of exploratory data without negatively impacting user experience.
その代わりに、ボルツマン探索 [12] を採用し、ユーザーエクスペリエンスに悪影響を与えることなく、探索的データの利点を得ることができる。
We consider using a stochastic policy where recommendations are sampled from 𝜋𝜃 rather than taking the 𝐾 items with the highest probability.
我々は、最も確率の高い ᵃ項目を選ぶのではなく、𝜋から推薦をサンプリングする確率的なポリシーを使用することを検討する。
This has the challenge of being computationally inefficient because we need to calculate the full softmax, which is prohibitively expensive considering our action space.
これは、完全なソフトマックスを計算する必要があるため、計算効率が悪いという課題があり、行動空間を考慮すると法外なコストがかかる。
Rather, we make use of efficient approximate nearest neighbor-based systems to look up the top 𝑀 items in the softmax [14].
その代わりに、効率的な近似最近傍システムを利用し、ソフトマックスの上位 ǔ項目を検索する[14]。
We then feed the logits of these 𝑀 items into a smaller softmax to normalize the probabilities and sample from this distribution.
次に、これらのǔ項目の対数をより小さなソフトマックスに送り込み、確率を正規化し、この分布からサンプリングする。
By setting 𝑀 ≫ 𝐾 we can still retrieve most of the probability mass, limit the risk of bad recommendations, and enable computationally efficient sampling.
𝑀 ≫ ᵃとすることで、確率の塊のほとんどを取り出すことができ、悪い推薦のリスクを制限し、計算効率の良いサンプリングを可能にする。
In practice, we further balance exploration and exploitation by returning the top 𝐾 ′ most probable items and sample 𝐾 − 𝐾 ′ items from the remaining 𝑀 − 𝐾 ′ items.
実際には、最も確率の高い上位 ᵃ項目を返し、残りの ᵃ項目から ᵃ項目を抽出することで、探索と抽出のバランスをさらに取る。

# 6. Experimental Results 実験結果

We showcase the effectiveness of these approaches for addressing data biases in a series of simulated experiments and live experiments in an industrial-scale recommender system.
我々は、一連のシミュレーション実験と産業規模の推薦システムでのライブ実験で、データの偏りに対処するためのこれらのアプローチの有効性を紹介する。

## 6.1. Simulation シミュレーション

We start with designing simulation experiments to shed light on the off-policy correction ideas under more controlled settings.
我々は、より制御された環境下でオフポリシー補正のアイデアを明らかにするために、シミュレーション実験を設計することから始める。
To simplify our simulation, we assume the problem is stateless, in other words, the reward 𝑅 is independent of user states, and the action does not alter the user states either.
シミュレーションを簡単にするために、我々は問題がステートレスであると仮定する。言い換えれば、報酬ǔはユーザの状態から独立しており、行動はユーザの状態も変えない。
As a result, each action on a trajectory can be independently chosen.
その結果、軌道上の各行動は独立して選択することができる。

### 6.1.1. Off-policy correction. オフポリシー修正

In the first simulation, we assume there are 10 items, that is A = {𝑎𝑖 ,𝑖 = 1, · · · , 10}.
最初のシミュレーションでは、アイテムが10個あると仮定し、すなわちA = {ᵄ𝑖 ,𝑖 = 1, - - , 10}とする。
The reward of each one is equal to its index, that is, 𝑟(𝑎𝑖) = 𝑖.
それぞれの報酬はそのインデックスに等しく、つまりᵄ𝑖(↪Ll_1D45E) = 𝑖である。
When we are choosing a single item, the optimal policy under this setting is to always choose the 10𝑡ℎ item as it gives the most reward, that is,
一つの項目を選ぶとき、この設定の下での最適な政策は、最も多くの報酬を与えるので、常に10𝑡↪Ll_210E の項目を選ぶこと、である。

$$
\tag{}
$$

We parameterize 𝜋𝜃 using a stateless softmax
Űᜃはステートレスソフトマックスを用いてパラメータ化する。

$$
\tag{}
$$

Given observations sampled from the behavior policy 𝛽, naively applying policy gradient without taking into account of data bias as in Equation (2) would converge to a policy
行動政策ǽからサンプリングされた観測値が与えられたとき，式(2)のようにデータの偏りを考慮せずに素朴に政策勾配を適用すると，政策

$$
\tag{}
$$

This has an obvious downside: the more the behavior policy chooses a sub-optimal item, the more the new policy will be biased toward choosing the same item.
これには明らかな欠点がある。行動政策が最適でない項目を選べば選ぶほど、新しい政策は同じ項目を選ぶ方向に偏ってしまう。

Figure 2 compares the policies 𝜋𝜃 , learned without and with off-policy correction using SGD [7], when the behavior policy 𝛽 is skewed to favor items with least reward.
図2は，SGD[7]を用いてオフポリシー補正を行うことなく学習したポリシーŰと，報酬が最も少ない項目を優先するように偏った行動ポリシー↪L_1D6↩を比較したものである．
As shown in Figure 2 (left), naively applying the policy gradient without accounting for the data biases leads to a sub-optimal policy.
図2（左）に示すように，データの偏りを考慮せずに素朴に政策勾配を適用すると，最適とは言えない政策になる．
In the worst case, if the behavior policy always chooses the action with the lowest reward, we will end up with a policy that is arbitrarily poor and mimicking the behavior policy (i.e., converge to selecting the least rewarded item).
最悪の場合、行動政策が常に報酬の最も少ない行動を選択する場合、任意に貧弱な行動政策を模倣した政策になってしまう（つまり、報酬の最も少ない項目を選択するように収束してしまう）。
On the other hand, applying the off-policy correction allows us to converge to the optimal policy 𝜋 ∗ regardless of how the data is collected, as shown in Figure 2 (right).
一方、オフポリシー補正を適用すると、図2（右）のように、データの収集方法に関わらず、最適な政策𝜋∗に収束させることができる。

### 6.1.2. Top-𝐾 off-policy correction. top-ᵃ off-policy correction.

To understand the difference between the standard off-policy correction and the top-𝐾 off-policy correction proposed, we designed another simulation in which we can recommend multiple items.
標準的なオフポリシー補正と提案された top-\_1D43 オフポリシー補正の違いを理解するために、複数のアイテムを推薦できる別のシミュレーションを設計した。
Again we assume there are 10 items, with 𝑟(𝑎1) = 10, 𝑟(𝑎2) = 9, and the remaining items are of much lower reward 𝑟(𝑎𝑖) = 1, ∀𝑖 = 3, · · · , 10. Here we focus on recommending two items, that is, 𝐾 = 2.
ここでも10個のアイテムがあり、Ǳ(ᵄ) = 10、ǲ = 9、残りのアイテムは報酬がかなり低いᑟ(𝑎) = 1、∀𝑖 = 3、-、10とする。ここでは2個のアイテム、つまりᵃ = 2の推薦に焦点を合わせる。
The behavior policy 𝛽 follows a uniform distribution, i.e., choosing each item with equal chance.
行動方針ǖは一様分布に従う、つまり、各項目を等しい確率で選択する。

Given an observation (𝑎𝑖 , 𝑟𝑖) sampled from 𝛽, the standard offpolicy correction has a SGD updates of the following form,
𝑎𝑖𝑖からサンプリングされた観測値（ᵅ）が与えられると、標準オフポリシー補正は以下の形式のSGD更新を持つ。

$$
\tag{}
$$

where 𝜂 is the learning rate.
ここで、𝜂は学習率である。
SGD keeps increasing the likelihood of the item 𝑎𝑖 proportional to the expected reward under 𝜋𝜃 until 𝜋𝜃 (𝑎𝑖) = 1, under which the gradient goes to 0. The top-𝐾 off-policy correction, on the other hand, has an update of the following form,
SGDはᜋ (ᜃ) = 1まで、ᜃの下で期待報酬に比例して項目ᑎの尤度を上げ続け、その下で勾配は0になる。 一方、top-ᵃ off-policy correctionは以下の形の更新がある。

$$
\tag{}
$$

where 𝜆𝐾 (𝑎𝑖) is the multiplier as defined in section 4.3.
ここで、𝜆 (ᵃ)は 4.3 節で定義された乗数である。
When 𝜋𝜃 (𝑎𝑖) is small, 𝜆𝐾 (𝑎𝑖) ≈ 𝐾, and SGD increases the likelihood of the item 𝑎𝑖 more aggressively.
ᜋが小さいときは、ᜆ (ᜎ) ≈ ↪Lu_1D43E となり、SGD はより積極的に項目 ᵄの可能性を増加させる。
As 𝜋𝜃 (𝑎𝑖) reaches to a large enough value, 𝜆𝐾 (𝑎𝑖) goes to 0. As a result, SGD will no longer force to increase the likelihood of this item even when 𝜋𝜃 (𝑎𝑖) is still less than 1. This in return allows the second-best item to take up some mass in the learned policy.
ᜋ (ᜃ) が十分に大きな値になると、ᜆ (ᵄ𝑖) は 0 になり、その結果、ᜋ (ᵄ𝑖) がまだ 1 以下でも SGD はこの項目の尤度を無理に上げなくなる。 その代わりに学習した方針において、二番手の項目がある程度の量を占めれるようにすることができた。

Figure 3 shows the policies 𝜋𝜃 learned with the standard (left) and top-𝐾 off-policy correction (right).
図3は、標準的なオフポリシー補正(左)とtop-1_703補正(右)で学習された政策Űを示す。
We can see that with the standard off-policy correction, although the learned policy is calibrated [23] in the sense that it still maintains the ordering of items w.r.t. their expected reward, it converges to a policy that cast almost its entire mass on the top-1 item, that is 𝜋 (𝑎1) ≈ 1.0.
標準的なオフポリシー補正では，学習されたポリシーは期待報酬に対するアイテムの順序を維持するという意味で較正[23]されているが，トップ1のアイテムにほぼ全量を投じるポリシー，すなわち，ᵄ (↪Ll_1D1E) ≈ 1.0 に収束していることが分かる．
As a result, the learned policy loses track of the difference between a slightly sub-optimal item (𝑎2 in this example) and the rest.
その結果，学習された政策は，わずかに最適でない項目 (この例では ᵄ) と残りの項目との間の差を見失う．
The top-𝐾 correction, on the other hand, converges to a policy that has a significant mass on the second optimal item, while maintaining the order of optimality between items.
一方、top-ᵃの補正は、項目間の最適性の順序を維持したまま、2番目に最適な項目に大きな質量を持つ政策に収束させる。
As a result, we are able to recommend to users two high-reward items and aggregate more reward overall.
その結果、2つの高報酬のアイテムをユーザに推奨し、全体としてより多くの報酬を集約することができる。

## 6.2. Live Experiments Live Experiments

While simulated experiments are valuable to understand new methods, the goal of any recommender systems is ultimately to improve real user experience.
新しい手法を理解するためのシミュレーション実験は貴重ですが、あらゆるレコメンダーシステムの目標は、最終的には実際のユーザー体験を向上させることです。
We therefore conduct a series of A
そのため、私たちは、実際に利用されるユーザー体験を向上させるための一連のA

We evaluate these methods on a production RNN candidate generation model in use at YouTube, similar to the setup described in [6, 11].
我々は、[6, 11]で説明したセットアップと同様に、YouTubeで使用されている本番のRNN候補生成モデルでこれらのメソッドを評価します。
The model is one of many candidate generators that produce recommendations, which are scored and ranked by a separate ranking model before being shown to users on the YouTube Homepage or the side panel on the video watch page.
このモデルは、YouTubeホームページや動画視聴ページのサイドパネルでユーザーに表示される前に、別のランキングモデルによってスコアリングとランク付けが行われる、推薦文を生成する多くの候補生成者のうちの1つです。
As described above, the model is trained following the REINFORCE algorithm.
上述したように、モデルは REINFORCE アルゴリズムに従って学習されます。
The immediate reward 𝑟 is designed to reflect different user activities; videos that are recommended but not clicked receive zero reward.
即時報酬 ὅ はさまざまなユーザーの活動を反映するように設計されており、推奨されてもクリックされないビデオはゼロ報酬を受け取ります。
The long term reward 𝑅 is aggregated over a time horizon of 4–10 hours.
長期報酬 х は4-10時間の時間軸で集計される。
In each experiment both the control and the test model use the same reward function.
各実験において、コントロールモデルとテストモデルは同じ報酬関数を使用する。
Experiments are run for multiple days, during which the model is trained continuously with new events being used as training data with a lag under 24 hours.
実験は複数日にわたって行われ、その間、新しいイベントが24時間以内の遅れでトレーニングデータとして使用され、モデルは継続的にトレーニングされる。
While we look at various online metrics with the recommender system during live experiments, we are going to focus our discussion on the amount of time user spent watching videos, referred to as ViewTime.
ライブ実験では、レコメンダーシステムの様々なオンラインメトリクスを見ますが、ここでは、ユーザーがビデオを見るのに費やした時間（ViewTimeと呼ばれる）に焦点をあてて議論したいと思います。

The experiments presented here describe multiple sequential improvements to the production system.
ここで紹介する実験は、プロダクションシステムを複数回に分けて改良したものである。
Unfortunately, in such a setting, the latest recommender system provides the training data for the next experiment, and as a result, once the production system incorporates a new approach, subsequent experiments cannot be compared to the earlier system.
残念ながら、このような設定では、最新のレコメンダーシステムが次の実験のためのトレーニングデータを提供するため、いったん本番システムが新しいアプローチを取り込むと、それ以降の実験は以前のシステムと比較することができない。
Therefore, each of the following experiments should be taken as the analysis for each component individually, and we state in each section what was the previous recommender system from which the new approach receives data.
したがって、以下の各実験は、各構成要素の個別の分析として捉えるべきであり、新しいアプローチがデータを受け取る前のレコメンダーシステムが何であったかを各セクションに記載する。

### 6.2.1. Exploration. エクスプロージョン

We begin with understanding the value of exploratory data in improving model quality.
まず，モデルの品質を向上させるための探索的なデータ の価値を理解することから始める．
In particular, we would like to measure if serving a stochastic policy, under which we sample from the softmax model as described in Section 5, results in better recommendations than serving a deterministic policy where the model always recommends the 𝐾 items with the highest probability according to the softmax.
特に，セクション 5 で述べたように，ソフトマッ クスモデルからサンプリングする確率的な政策が，ソフトマッ クスに従って常に最も高い確率で ᵃ の項目を推薦する決定論的な政策より良い推薦 をもたらすかどうかを測定したい．

We conducted a first set of experiments to understand the impact of serving a stochastic policy vs. a deterministic one while keeping the training process unchanged.
この実験では，確率的なポリシーと決定論的なポリシーとを比較し て，学習過程を変更しない場合の影響を調べるために，最初の実験 をおこなった．
In the experiment, the control population is served with a deterministic policy, while a small slice of test traffic is served with the stochastic policy as described in Section 5.
この実験では，制御集団には決定論的なポリシーを適用し，テスト・トラフィックの小片にはセクション 5 で述べたような確率論的なポリシーを適用した．
Both policies are based on the same softmax model trained as in Equation (??).
両ポリシーとも式 (?) のように学習された同じソフトマックスモデルにもとづくものである．
To control the amount of randomness in the stochastic policy at serving, we varied the temperature used in Equation (6).
また，ストキャスティックポリシーのランダムネス量を制御するために，式 (6) で使用する温度を変化させた．
A lower 𝑇 reduces the stochastic policy to a deterministic one, while a higher 𝑇 leads to a random policy that recommends any item with equal chance.
↪Lu_1D447 が低いと確率的政策が決定論的政策になり，↪Lu_1D447 が高いと任意のアイテムを等しい確率で推奨するランダム政策になる．
With 𝑇 set to 1, we observed no statistically significant change in ViewTime during the experiment, which suggests the amount of randomness introduced from sampling does not hurt the user experience directly.
↪Lu_1D447 を 1 に設定した場合，実験中に ViewTime に統計的に有意な変化は観察されず， サンプリングによって生じるランダム性の量が直接ユーザ経験を損なわないことを 示している．

However, this experimental setup does not account for the benefit of having exploratory data available during training.
しかし、この実験設定では、学習中に探索的なデータを利用できることの利点が考慮されていない。
One of the main biases in learning from logged data is that the model does not observe feedback of actions not chosen by the previous recommendation policy, and exploratory data alleviates this problem.
ログデータからの学習における主なバイアスの1つは、モデルが前回の推薦方針で選択されなかった行動のフィードバックを観測しないことであり、探索データはこの問題を軽減する。
We conducted a followup experiment where we introduce the exploratory data into training.
そこで、探索データを学習に導入する追試を行った。
To do that, we split users on the platform into three buckets: 90%, 5%, 5%.
そのために、プラットフォーム上のユーザーを90％、5％、5％の3つのバケットに分割しました。
The first two buckets are served with a deterministic policy based on a deterministic model and the last bucket of users is served with a stochastic policy based on a model trained with exploratory data.
最初の2つのバケットには決定論的なモデルに基づく決定論的なポリシーでサービスを提供し、最後のバケットのユーザーには探索的なデータで学習したモデルに基づく確率的なポリシーでサービスを提供します。
The deterministic model is trained using only data acquired in the first two buckets, while the stochastic model is trained on data from the first and third buckets.
決定論的モデルは、最初の2つのバケットで取得したデータのみを使用して訓練され、確率論的モデルは、最初と3番目のバケットのデータで訓練される。
As a result, these two models receive the same amount of training data, but the stochastic model is more likely to observe the outcomes of some rarer state, action pairs because of exploration.
その結果、これら2つのモデルは同じ量の学習データを受け取るが、ストキャスティックモデルは探索のため、いくつかの稀な状態と行動のペアの結果を観察する可能性が高くなる。

Following this experimental procedure, we observe a statistically significant increase in ViewTime by 0.07% in the test population.
この実験手順に従うと、テスト母集団において、ViewTime が 0.07% と統計的に有意に増加することが確認されま した。
While the improvement is not large, it comes from a relatively small amount of exploration data (only 5% of users experience the stochastic policy).
この改善は大きくはありませんが，比較的少ない探索データから得られたものです (確率的ポリシーを経験したユーザはわずか 5%)．
We expect higher gain now that the stochastic policy has been fully launched.
ストキャスティック・ポリシーが完全に開始された今、より高い利得が期待されます。

### 6.2.2. Off-Policy Correction. オフポリシー修正

Following the use of a stochastic policy, we tested incorporating off-policy correction during training.
ストキャスティックポリシーに続いて、トレーニング中にオフポリシー補正を組み込むことをテストしました。
Here, we follow a more traditional A
ここでは、より伝統的なA

During experiments, we observed the learned policy (test) starts to deviate from the behavior policy (control) that is used to acquire the traffic.
また，実験中に，学習されたポリシー(test)がトラフィックを獲得するための行動ポリシー(control)から乖離し始めることが観察された．
Figure 4 plots a CDF of videos selected by our nominator in control and experiment according to the rank of videos in control population (rank 1 is the most nominated video by the control model, and the rightmost is least nominated).
図4は、制御母集団における動画のランクに応じて、制御と実験でノミネータが選択した動画のCDFをプロットしたものです（ランク1は制御モデルによって最もノミネートが多い動画、右端は最もノミネートが少ない動画です）。
We see that instead of mimicking the model (shown in blue) used for data collection, the test model (shown in green) favors videos that are less explored by the control model.
データ収集に用いたモデル（青色で表示）を模倣するのではなく、テストモデル（緑色で表示）はコントロールモデルであまり探索されていない動画を優先していることがわかる。
We observed that the proportion of nominations coming from videos outside of the top ranks is increased by nearly a factor of three in experiment.
実験では、上位ランク以外の動画からのノミネートの割合が、ほぼ1/3に増加することが観察されました。
This aligns with what we observed in the simulation shown in Figure 2.
これは、図2に示したシミュレーションで観察されたものと一致しています。
While ignoring the bias in the data collection process creates a “rich get richer“ phenomenon, whereby a video is nominated in the learned policy simply because it was heavily nominated in the behavior policy, incorporating the off-policy correction reduces this effect.
データ収集過程での偏りを無視すると，行動ポリシーで多くノミネートされたからといって学習ポリシーでノミネートされるという「金持ちがより金持ちになる」現象が生じるが，オフポリシー補正を組み込むことでこの効果を低減することができる．

Interestingly, in live experiment, we did not observe a statistically significant change in ViewTime between control and test population.
興味深いことに、ライブ実験では、コントロール集団とテスト集団の間で、ViewTimeの統計的に有意な変化は観察されませんでした。
However, we saw an increase in the number of videos viewed by 0.53%, which was statistically significant, suggesting that users are indeed getting more enjoyment.
しかし、動画の視聴回数が0.53%増加し、統計的に有意であったことから、ユーザーがより楽しめていることが伺えます。

### 6.2.3. Top-𝐾 Off-Policy. Top-ᵃ Off-Policy.

We now focus on understanding if the top-𝐾 off-policy learning improves the user experience over the standard off-policy approach.
我々は、オフポリシー学習が標準的なオフポリシーアプローチよりもユーザーエクスペリエンスを向上させるかどうかを理解することに重点を置く。
In this case, we launched an equivalently structured model now trained with the top-𝐾 off-policy corrected gradient update given in Equation (7) and compared its performance to the previous off-policy model, described in Section 6.2.2.
この場合，式(7)で与えられるtop-ᵃ off-policy補正勾配更新で学習した等価構造モデルを起動し，セクション6.2.2で述べた以前のoff-policyモデルと性能を比較しました．
In this experiment, we use 𝐾 = 16 and capping 𝑐 = 𝑒 3 in Equation (9); we will explore these hyperparameters in more detail below.
この実験では，式 (9) で ᵃ = 16 とキャッピング 𝑒 = 𝑓 を使用しました．

As described in Section 4.3 and demonstrated in the simulation in Section 6.1.2, while the standard off-policy correction we tested before leads to a policy that is overly-focused on getting the top-1 item correct, the top-𝐾 off-policy correction converges to a smoother policy under which there is a non-zero mass on the other items of interest to users as well.
セクション 4.3 で説明し，セクション 6.1.2 のシミュレーションで示したように，以前テストした標準的なオフポリシー補正はトップ 1 の項目を正すことに過度に集中したポリシーを導くが，トップ ᵃオフポリシー補正は，ユーザが興味を持つ他の項目にもゼロではない質量がある，より滑らかなポリシーに収束させる．
This in turn leads to better top-𝐾 recommendation.
これにより、より良いトップ ᵃの推薦につながる。
Given that we can recommend multiple items, the top-𝐾 off-policy correction leads us to present a better fullpage experience to users than the standard off-policy correction.
複数の項目を推薦することができることを考えると、トップ\_1オフポリシー補正は標準的なオフポリシー補正よりもユーザーに良いフルページ体験を提供することにつながる。
In particular, we find that the amount of ViewTime increased by 0.85% in the test traffic, with the number of videos viewed slightly decreasing by 0.16%.
特に、テストトラフィックでは、ViewTime の量が 0.85% 増加し、動画の視聴数は 0.16% とわずかに減少していることがわかります。

### 6.2.4. Understanding Hyperparameters. ハイパーパラメータを理解する。

Last, we perform a direct comparison of how different hyperparameter choices affect the top-𝐾 off-policy correction, and in turn the user experience on the platform.
最後に、ハイパーパラメータの選択がtop-ᵃ off-policy補正、ひいてはプラットフォームでのユーザー体験にどのような影響を与えるかを直接比較しました。
We perform these tests after the top-𝐾 off-policy correction became the production model.
これらのテストは、top-ᵃ off-policy補正がプロダクションモデルになった後に実施しました。

#### 6.2.4.1. Number of actions. アクションの数

We first explore the choice of 𝐾 in the top-𝐾 off-policy correction.
まず、top-ᵃ off-policy補正におけるᵃの選択について検討する。
We train three structurally identical models, using 𝐾 ∈ {1, 2, 16, 32}; The control (production) model is the top-𝐾 off-policy model with 𝐾 = 16.
ᵃ∈ {1, 2, 16, 32} を用いて、3つの構造的に同一のモデルを訓練する。対照（生産）モデルは、↪Lu_1D43E = 16 の top-ᵃ off-policy モデルである。
We plot the results during a 5-day experiment in Figure 5.
5 日間の実験の結果を図 5 にプロットする。
As explained in Section 4.3, with 𝐾 = 1, the top-𝐾 off-policy correction reduces to the standard off-policy correction.
4.3 節で説明したように、↪Lu_1D43E = 1 の場合、top-𝐾 off-policy の補正は標準の off-policy の補正に減少する。
A drop of 0.66% ViewTime was observed for 𝐾 = 1 compared with the baseline with 𝐾 = 16.
ᵃ = 1 では、ᵃ = 16 のベースラインと比較して 0.66% の ViewTime の減少が観察されました。
This further confirms the gain we observed shifting from the standard off-policy correction to the top-𝐾 off-policy correction.
これは、標準のオフポリシー補正から top-ᵃオフポリシー補正に移行して観測された利得をさらに確認するものです。
Setting 𝐾 = 2 still performs worse than the production model, but the gap is reduced to 0.35%.
ᵃ = 2に設定しても、製品モデルよりも性能は劣るが、その差は0.35%に縮まった。
𝐾 = 32 achieves similar performance as the baseline.
ᵃ = 32はベースラインと同様の性能を達成した。
We conducted follow up experiment which showed mildly positive gain in ViewTime (+0.15% statistically significant) when 𝐾 = 8.
フォローアップ実験を行ったところ、ᵃ = 8 のときに、ViewTime がわずかに増加しました (+0.15% 統計的に有意)。

#### 6.2.4.2. Capping. キャッピング

Here we consider the effect of the variance reduction techniques on the final quality of the learned recommender.
ここでは、学習済みレコメンダーの最終的な品質に対する分散削減技術の効果について考察する。
Among the techniques discussed in Section 4.4, weight capping brings the biggest gain online in initial experiments.
セクション4.4で議論した技術の中で、重みキャッピングは初期の実験においてオンラインで最大の利得をもたらす。
We did not observe further metric improvements from normalized importance sampling, or TRPO [36].
また、正規化重要度サンプリングやTRPO[36]による更なるメトリックの向上は観察されなかった。
We conducted a regression test to study the impact of weight capping.
我々は、ウェイトキャッピングの影響を調査するために回帰テストを実施した。
We compare a model trained using cap 𝑐 = 𝑒 3 (as in production model) in Equation (9) with one trained using 𝑐 = 𝑒 5 .
これは，式(9)のcap 𝑐 = 𝑒（生産モデルのように）を用いて学習したモデルと， 𝑐 = 𝑒を用いて学習したモデルを比較するものである．
As we lift the restriction on the importance weight, the learned policy 𝜋𝜃 could potentially overfit to a few logged actions that accidentally receives high reward.
重要度重みの制限を解除すると，学習された政策ᜃは偶然に高い報酬を受け取る少数の記録された行動に対して過剰に適合する可能性がある．
Swaminathan and Joachims [43] described a similar effect of propensity overfitting.
SwaminathanとJoachims [43]は、傾向のオーバーフィッティングの同様の効果について述べている。
During live experiment, we observe a significant drop of 0.52% in ViewTime when the cap on importance weight was lifted.
ライブ実験では、重要度ウェイトの上限が解除されたときに、ViewTimeが0.52%という大幅な低下を観測しています。

# 7. Conclusion 結論

In this paper we have laid out a practical implementation of a policy gradient-based top-𝐾 recommender system in use at YouTube.
この論文では、YouTubeで使用されている政策勾配に基づくトップ1推薦システムの実用的な実装を示しました。
We scale up REINFORCE to an action space in the orders of millions and have it stably running in a live production system.
また、REINFORCEを数百万単位のアクションスペースにスケールアップし、本番システムで安定的に動作させることができた。
To realize the full benefits of such an approach, we have demonstrated how to address biases in logged data through incorporating a learned logging policy and a novel top-𝐾 off-policy correction.
このようなアプローチの利点を最大限に実現するために、学習されたロギングポリシーと新しい top-ᵃ off-policy correction を組み込むことによって、ログデータのバイアスに対処する方法を実証しました。
We conducted extensive analysis and live experiments to measure empirically the importance of accounting for and addressing these underlying biases.
私たちは、これらの根底にあるバイアスを考慮し、対処することの重要性を実証的に測定するために、広範な分析とライブ実験を実施しました。
We believe these are important steps in making reinforcement learning practically impactful for recommendation and will provide a solid foundation for researchers and practitioners to explore new directions of applying RL to recommender systems.
我々は、強化学習が推薦に実用的なインパクトを与えるための重要なステップであり、研究者や実務家が推薦システムに強化学習を適用する新しい方向性を探るための強固な基礎を提供すると考えている。
