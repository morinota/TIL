
## Scalable Neural Contextual Bandit for Recommender Systems  
### Zheqing Zhu ##### Meta AI, Stanford University Menlo Park, CA, USA billzhu@meta.com  

#### Abstract 要約
High-quality recommender systems ought to deliver both innovative and relevant content through effective and exploratory interactions with users.  
高品質な推薦システムは、ユーザーとの効果的かつ探索的なインタラクションを通じて、革新的で関連性のあるコンテンツを提供するべきです。  
Yet, supervised learning-based neural networks, which form the backbone of many existing recommender systems, only leverage recognized user interests, falling short when it comes to efficiently uncovering unknown user preferences.  
しかし、既存の多くの推薦システムの基盤を形成する教師あり学習に基づくニューラルネットワークは、認識されたユーザーの興味のみを活用し、未知のユーザーの好みを効率的に明らかにすることには不十分です。  
While there has been some progress with neural contextual bandit algorithms towards enabling online exploration through neural networks, their onerous computational demands hinder widespread adoption in real-world recommender systems.  
ニューラルネットワークを通じてオンライン探索を可能にするためのニューラルコンテキストバンディットアルゴリズムに関しては一定の進展がありましたが、その厳しい計算要求は、実世界の推薦システムでの広範な採用を妨げています。  
In this work, we propose a scalable sample-efficient neural contextual bandit algorithm for recommender systems.  
本研究では、推薦システムのためのスケーラブルでサンプル効率の良いニューラルコンテキストバンディットアルゴリズムを提案します。  
To do this, we design an epistemic neural network architecture, Epistemic Neural Recommendation (ENR), that enables Thompson sampling at a large scale.  
これを実現するために、私たちは大規模なThompsonサンプリングを可能にするエピステミックニューラルネットワークアーキテクチャ、Epistemic Neural Recommendation (ENR)を設計しました。  
In two distinct large-scale experiments with real-world tasks, ENR significantly boosts clickthrough rates and user ratings by at least 9% and 6% respectively compared to state-of-the-art neural contextual bandit algorithms.  
実世界のタスクにおける2つの異なる大規模実験において、ENRは最先端のニューラルコンテキストバンディットアルゴリズムと比較して、クリック率とユーザー評価をそれぞれ少なくとも9%と6%向上させます。  
Furthermore, it achieves equivalent performance with at least 29% fewer user interactions compared to the best-performing baseline algorithm.  
さらに、ENRは、最も優れたベースラインアルゴリズムと比較して、少なくとも29%少ないユーザーインタラクションで同等のパフォーマンスを達成します。  
Remarkably, while accomplishing these improvements, ENR demands orders of magnitude fewer computational resources than neural contextual bandit baseline algorithms.  
驚くべきことに、これらの改善を達成しながら、ENRはニューラルコンテキストバンディットのベースラインアルゴリズムよりも桁違いに少ない計算リソースを要求します。  


```md
### Benjamin Van Roy
##### Stanford University Stanford, CA, USA bvr@stanford.edu
**Figure 1: MIND Experiment Computation-Performance** **Tradeoff. Better Tradeoff towards Top Right. We expect full-** **scale NeuralUCB and NeuralTS to perform similarly to our** **methods, but require orders of magnitude more compute.**  
### ベンジャミン・ヴァン・ロイ
##### スタンフォード大学 カリフォルニア州スタンフォード、アメリカ bvr@stanford.edu
**図1: MIND実験の計算性能トレードオフ。右上に向かうほど良いトレードオフ。私たちは、フルスケールのNeuralUCBとNeuralTSが私たちの手法と同様に機能することを期待していますが、計算リソースは桁違いに多く必要です。**

#### Keywords
Recommender Systems, Contextual Bandits, Reinforcement Learning, Exploration vs Exploitation, Decision Making under Uncertainty  
#### キーワード
レコメンダーシステム、コンテキストバンディット、強化学習、探索と活用、 不確実性下での意思決定

#### 1 Introduction
Recommender systems (RS), paramount in personalizing digital content, critically influence the quality of information accessed via the Internet. Traditionally, these systems have employed supervised learning algorithms, such as Collaborative Filtering [45], which have greatly benefited from advances in deep learning. These algorithms analyze vast quantities of data to discern user preferences; however, they are not designed to strategically probe in order to more quickly learn about user interests. Instead, they learn passively from collected data.  
#### 1 はじめに
レコメンダーシステム（RS）は、デジタルコンテンツのパーソナライズにおいて重要であり、インターネットを通じてアクセスされる情報の質に重大な影響を与えます。従来、これらのシステムは、協調フィルタリング[45]のような教師あり学習アルゴリズムを使用しており、深層学習の進歩から大きな恩恵を受けてきました。これらのアルゴリズムは、大量のデータを分析してユーザの好みを識別しますが、ユーザの興味をより早く学ぶために戦略的に探るようには設計されていません。代わりに、収集されたデータから受動的に学習します。

Current research [24, 32, 49] reveals that deep-learning-driven RS tend to quickly confine their focus to a limited set of suboptimal topics, limiting their scope and hampering their learning capacity.  
現在の研究[24, 32, 49]は、深層学習に基づくRSが迅速に限られたサブオプティマルなトピックに焦点を絞る傾向があり、その範囲を制限し、学習能力を妨げていることを明らかにしています。

This restrictive personalization strategy confines RS to recommend only those topics with which they have established familiarity, thus failing to discover and learn users’ other potential interests.  
この制限的なパーソナライズ戦略は、RSが既に親しみのあるトピックのみを推奨することに制約され、ユーザの他の潜在的な興味を発見し学ぶことができなくなります。

The ability of an RS to identify and learn about user’s unexplored interests is a significant determinant of its long-term performance.  
RSがユーザの未探索の興味を特定し学ぶ能力は、その長期的なパフォーマンスの重要な決定要因です。

The concept of exploration in RS draws heavily from bandit learning [51]. In the bandit learning formulation of RS, the system functions as an agent, each user represents a unique context, and each recommendation is an action.  
RSにおける探索の概念は、バンディット学習[51]から大きく影響を受けています。バンディット学習のRSの定式化では、システムはエージェントとして機能し、各ユーザはユニークなコンテキストを表し、各推奨はアクションとなります。

Bandit learning algorithms, such as upper confidence bound (UCB) [2, 6] and Thompson sampling [53], provide the groundwork for efficient exploration.  
上限信頼区間（UCB）[2, 6]やトンプソンサンプリング[53]などのバンディット学習アルゴリズムは、効率的な探索の基盤を提供します。

Theoretical advances [2, 3, 5, 6, 17, 18] have offered great insight into these methods, and the efficacy of such methods has been demonstrated through experiments with small-scale environments.  
理論的な進展[2, 3, 5, 6, 17, 18]は、これらの手法に関する大きな洞察を提供しており、その有効性は小規模な環境での実験を通じて実証されています。

While much of this literature has focused on small-scale environments that do not require that an agent generalizes across contexts and actions, the scale of practical RS calls for such generalization.  
この文献の多くは、エージェントがコンテキストやアクションを横断して一般化する必要のない小規模な環境に焦点を当ててきましたが、実際のRSのスケールはそのような一般化を必要とします。

Advances in neural bandits offer flexible and scalable approaches to generalization that support more sample-efficient exploration algorithms.  
ニューラルバンディットの進展は、よりサンプル効率の良い探索アルゴリズムをサポートする一般化に対する柔軟でスケーラブルなアプローチを提供します。

Building on ideas developed for linear UCB and linear Thompson sampling [12, 37], these approaches offer variations of UCB and Thompson sampling that interoperate with deep learning [1, 19, 37, 38, 42, 43, 59, 61, 64].  
線形UCBおよび線形トンプソンサンプリング[12, 37]のために開発されたアイデアに基づいて、これらのアプローチは深層学習と相互運用可能なUCBおよびトンプソンサンプリングのバリエーションを提供します[1, 19, 37, 38, 42, 43, 59, 61, 64]。

While these approaches may be sample-efficient, their computational requirements become onerous at scale.  
これらのアプローチはサンプル効率が良いかもしれませんが、スケールが大きくなると計算要件が厳しくなります。

This has limited their practical impact.  
これにより、実際の影響が制限されています。

An obstacle to scaling aforementioned approaches has been in the computation required to maintain and apply epistemic uncertainty estimates.  
前述のアプローチをスケールアップする際の障害は、エピステミック不確実性の推定を維持し適用するために必要な計算にあります。

Such estimates allow an agent to know what it does _not know, which is critical for guiding exploration.  
このような推定は、エージェントが自分が何を知らないかを知ることを可能にし、探索を導くために重要です。

The EpiNet [41]_ offers a scalable approach to uncertainty estimation, and therefore, a path toward supporting efficient exploration in practical RS.  
EpiNet[41]は、不確実性推定に対するスケーラブルなアプローチを提供し、したがって、実際のRSにおける効率的な探索をサポートする道を提供します。

In particular, epinet-enhanced deep learning combined with Thompson sampling, has the potential to greatly improve RS’ exploration capabilities and therefore improve personalization.  
特に、トンプソンサンプリングと組み合わせたエピネット強化深層学習は、RSの探索能力を大幅に向上させ、したがってパーソナライズを改善する可能性があります。

To this end, we introduce Epistemic Neural Recommendation (ENR), a novel architecture customized for RS.  
この目的のために、私たちはレコメンダーシステムに特化した新しいアーキテクチャであるエピステミックニューラルレコメンデーション（ENR）を紹介します。

We run a series of experiments using large-scale real-world RS datasets to empirically demonstrate that ENR outperforms state-of-the-art neural contextual bandit algorithms.  
私たちは、大規模な実世界のレコメンダーシステムデータセットを使用して一連の実験を行い、ENRが最先端のニューラルコンテキストバンディットアルゴリズムを上回ることを実証します。

ENR greatly enhances personalization, achieving an 9% and 6% improvement in click-through rate and user rating, respectively, across two real-world experiments.  
ENRはパーソナライズを大幅に向上させ、2つの実世界の実験でそれぞれクリック率とユーザ評価で9%および6%の改善を達成しました。

Furthermore, it attains the performance of the best baseline algorithm with at least 29% fewer user interactions.  
さらに、ENRは、少なくとも29%少ないユーザインタラクションで、最良のベースラインアルゴリズムのパフォーマンスを達成します。

Importantly, ENR accomplishes these while requiring orders of magnitude fewer computational resources than neural contextual bandit baseline algorithms, making it a considerably more scalable solution.  
重要なのは、ENRがニューラルコンテキストバンディットベースラインアルゴリズムよりも桁違いに少ない計算リソースを必要としながらこれを達成するため、かなりスケーラブルなソリューションとなることです。

As a spoiler, please see Figure 1 for a computation-performance tradeoff comparison between our method and baseline methods based on one of our real-world experiments.  
ネタバレとして、私たちの手法と実世界の実験の1つに基づくベースライン手法との計算性能トレードオフの比較については、図1をご覧ください。

The remainder of this paper is organized as follows. In Section 2, we formulate RS as a contextual bandit. In Section 3, we review existing online contextual bandit algorithms, current industry adoptions, and their relative merits. In Section 4, we introduce Epistemic Neural Recommendation. In Section 5, we present empirical results.  
この論文の残りの部分は次のように構成されています。セクション2では、RSをコンテキストバンディットとして定式化します。セクション3では、既存のオンラインコンテキストバンディットアルゴリズム、現在の業界での採用、およびそれらの相対的な利点をレビューします。セクション4では、エピステミックニューラルレコメンデーションを紹介します。セクション5では、実証結果を示します。

In Section 6, we summarize our contributions, benefits they afford, and potential future directions for neural contextual bandits.  
セクション6では、私たちの貢献、提供する利点、およびニューラルコンテキストバンディットの将来の方向性を要約します。

#### 2 Problem Definition
We conceptualize the design of RS as a contextual bandit problem where an agent interacts with a RS environment by taking an action (recommendation) based on a context (user) observed. More formally, the environment is specified by a triple that consists E of an observation space, an action space, and an observation O A probability function 𝑃𝑂 .  
#### 2 問題定義
私たちは、RSの設計をコンテキストバンディット問題として概念化し、エージェントが観察されたコンテキスト（ユーザ）に基づいてアクション（推奨）を取ることによってRS環境と相互作用します。より正式には、環境は観察空間、アクション空間、および観察Oの3つの要素からなる三重項Eによって指定されます。確率関数は$P_O$です。

**Observation space O: In a contextual bandit problem, the ob-** servation generated by the environment offers feedback in response to the previous action taken by the agent as well as a new context the agent needs to execute an action. Formally, O = S × R and at time step 𝑡, 𝑂𝑡 = (𝑆𝑡 _, 𝑅𝑡_ ). 𝑆𝑡 ∈S is a new context. This context could, for example, provide a user’s demographic information as well as data from their past interactions. We will sometimes refer to 𝑆𝑡 as a user, since we think of it as providing information that distinguishes users. 𝑅𝑡 ∈ R denotes scalar feedback from the user of the previous time step 𝑡 − 1 in response to the action 𝐴𝑡 −1. For example, 𝑅𝑡 could be binary-valued, indicating whether the user clicked in response to a recommendation. We will refer to 𝑅𝑡 as the reward received by the agent at time 𝑡.  
**観察空間O: コンテキストバンディット問題において、環境によって生成される観察は、エージェントが取った前のアクションに対するフィードバックと、エージェントがアクションを実行するために必要な新しいコンテキストを提供します。正式には、$O = S × R$であり、時刻$t$において、$O_t = (S_t, R_t)$です。$S_t ∈ S$は新しいコンテキストです。このコンテキストは、例えば、ユーザの人口統計情報や過去のインタラクションからのデータを提供することがあります。私たちは時々$S_t$をユーザと呼びます。なぜなら、これはユーザを区別する情報を提供するものと考えるからです。$R_t ∈ R$は、アクション$A_{t-1}$に対する前の時刻$t - 1$のユーザからのスカラーのフィードバックを示します。例えば、$R_t$はバイナリ値であり、ユーザが推奨に応じてクリックしたかどうかを示すことができます。私たちは$R_t$を時刻$t$にエージェントが受け取った報酬と呼びます。**

**Action space A: At each time 𝑡, the agent selects an action** _𝐴𝑡_ ∈A, which identifies a content unit for recommendation to the user 𝑆𝑡 . The action space A specifies the range of possibilities afforded by the universe of available content.  
**アクション空間A: 各時刻$t$において、エージェントはアクション$A_t ∈ A$を選択し、これはユーザ$S_t$に推奨するコンテンツユニットを特定します。アクション空間Aは、利用可能なコンテンツの宇宙によって提供される可能性の範囲を指定します。**

**Observation probability function 𝑃𝑂** : The observation probability function assigns a probability 𝑃𝑂 (𝑂𝑡 +1|𝑆𝑡 _,𝐴𝑡_ ) to each possible outcome 𝑂𝑡 +1 = (𝑆𝑡 +1, 𝑅𝑡 +1) from recommending 𝐴𝑡 to user 𝑆𝑡 .  
**観察確率関数$P_O$**: 観察確率関数は、ユーザ$S_t$に$A_t$を推奨することから得られる各可能な結果$O_{t+1} = (S_{t+1}, R_{t+1})$に確率$P_O(O_{t+1}|S_t, A_t)$を割り当てます。

This probability is a product of two others, specified by functions _𝑃𝑆_ and 𝑃𝑅:  
この確率は、関数$P_S$と$P_R$によって指定される他の2つの積です。

$$
P_O(O_{t+1}|S_t, A_t) = P_S(S_{t+1})P_R(R_{t+1}|S_t, A_t).
$$

At time 𝑡, the environment samples a new user 𝑆𝑡 ∼ _𝑃𝑆_ . The agent then supplies a recommendation 𝐴𝑡, and the environment samples 𝑅𝑡 +1 ∼ _𝑃𝑅_ (·|𝑆𝑡 _,𝐴𝑡_ ).  
時刻$t$において、環境は新しいユーザ$S_t ∼ P_S$をサンプリングします。エージェントは次に推奨$A_t$を提供し、環境は$R_{t+1} ∼ P_R(·|S_t, A_t)$をサンプリングします。

The overall objective of the agent is to maximize its average reward _𝑇[1]_ �𝑇𝑡 =1 _[𝑅][𝑡]_ [over][ 𝑇] [time steps. Note that, though each ac-]  
エージェントの全体的な目的は、平均報酬$\frac{1}{T} \sum_{t=1}^{T} R_t$を最大化することです。各アクション$A_t$は、$S_t$以外のユーザに直接影響を与えないが、アクションは観察$R_{t+1}$を通じて収集される情報に影響を与えます。このように、アクションはエージェントが学ぶことを通じて後続のユーザに間接的な影響を与えます。学習の遅延利益を最適化するには、探索と活用のバランスを取る戦略的な逐次決定が必要です。

We think of 𝑆𝑡 and 𝐴𝑡 as offering information about users and content units in arbitrary raw formats. Agents, however, often rely on starting with a more structured representations provided by domain experts.  
私たちは$S_t$と$A_t$を、ユーザとコンテンツユニットに関する情報を任意の生の形式で提供するものと考えています。しかし、エージェントはしばしばドメイン専門家によって提供されるより構造化された表現から始まることに依存します。

In this work, we also assume availability of feature extractors that map 𝑆𝑡 and 𝐴𝑡 to such representations 𝜙𝐴𝑡 and 𝜓𝑆𝑡 .  
本研究では、$S_t$と$A_t$をそのような表現$\phi_{A_t}$と$\psi_{S_t}$にマッピングする特徴抽出器の利用可能性も仮定します。

Note that our problem formulation encompasses only online learning. In a real RS, one would pretrain an agent offline on historical data before engaging in online learning.  
私たちの問題定義は、オンライン学習のみを含むことに注意してください。実際のRSでは、オンライン学習に従事する前に、エージェントをオフラインで歴史データに基づいて事前学習させることになります。

The methods we develop for online learning can be applied in this workflow post pretraining of an epinet-enhanced model.  
私たちがオンライン学習のために開発する手法は、エピネット強化モデルの事前学習後のこのワークフローに適用できます。

However, in order to focus our attention on the problem of exploration, in this paper, we limit our discussions, designs and experiments to the online learning part and leave offline learning for future work.  
しかし、探索の問題に焦点を当てるために、本論文では議論、設計、実験をオンライン学習部分に制限し、オフライン学習は将来の作業に残します。

#### 3 Related Work and Prerequisites
Among various bandit algorithms, there are two most commonly adopted online bandit strategies. One explores based on the reward estimates sampled from context-action pairs’ posterior distributions, represented by Thompson sampling [53], and the other follows the "optimism in the face of uncertainty" principle, represented by upper confidence bound (UCB) [2, 6].  
#### 3 関連研究と前提条件
さまざまなバンディットアルゴリズムの中で、最も一般的に採用されているオンラインバンディット戦略は2つあります。1つは、コンテキスト-アクションペアの事後分布からサンプリングされた報酬推定に基づいて探索するもので、トンプソンサンプリング[53]で表されます。もう1つは、「不確実性に直面した楽観主義」の原則に従い、上限信頼区間（UCB）[2, 6]で表されます。

In this section, we offer a high level introduction to Thompson sampling and UCB algorithms as well as their extensions to contextual settings.  
このセクションでは、トンプソンサンプリングとUCBアルゴリズム、およびそれらのコンテキスト設定への拡張についての高レベルの紹介を提供します。

Their deep neural network versions of the algorithms are considered baselines for our work.  
これらのアルゴリズムの深層ニューラルネットワークバージョンは、私たちの作業のベースラインと見なされます。

We will also review related industry and practical adoptions of these strategies.  
また、これらの戦略の関連する業界および実用的な採用についてもレビューします。

Note that in this section, we limit our discussion to exploration strategy for immediate reward and do not cover optimization approaches for cumulative returns [13, 60, 65].  
このセクションでは、即時報酬のための探索戦略に議論を制限し、累積リターンの最適化アプローチ[13, 60, 65]については扱いません。

#### 3.1 Thompson Sampling, Its Extensions and Related Adoptions
Thompson sampling is an exploration strategy that samples reward estimates from context-action pairs’ posterior distributions and then executes greedily with respect to these samples.  
#### 3.1 トンプソンサンプリング、その拡張と関連する採用
トンプソンサンプリングは、コンテキスト-アクションペアの事後分布から報酬推定をサンプリングし、これらのサンプルに対して貪欲に実行する探索戦略です。

This strategy is particularly popular due to its simplicity.  
この戦略は、そのシンプルさから特に人気があります。

Following the definition in Section 2, we first consider a vanilla Thompson sampling algorithm [53] for multi-armed bandits.  
セクション2の定義に従い、まずはマルチアームバンディットのためのバニラトンプソンサンプリングアルゴリズム[53]を考えます。

For a multi-armed bandit, the context 𝑆𝑡 is always the same and the agent needs to choose _𝐴𝑡_ from A without any representation learning.  
マルチアームバンディットの場合、コンテキスト$S_t$は常に同じで、エージェントは表現学習なしに$A$から$A_t$を選択する必要があります。

A Thompson sampling agent keeps a reward posterior distribution _𝑃[ˆ]𝑎_ for each arm _𝑎_ and updates it over time.  
トンプソンサンプリングエージェントは、各アーム$a$に対して報酬の事後分布$P_a$を保持し、時間とともに更新します。

At time step 𝑡, the agent chooses  
時刻$t$において、エージェントは次のように選択します。

$$
A_t = \arg \max_{a \in A} \hat{R}_{t+1,a}, \quad \hat{R}_{t+1,a} \sim P_a.
$$

where $\hat{R}_{t,a}$ is the estimated reward sampled from the agent’s posterior belief.  
ここで、$\hat{R}_{t,a}$はエージェントの事後信念からサンプリングされた推定報酬です。

The agent then updates its posterior belief $P_a$ with the latest reward $R_{t+1}$ and selected action $A_t$.  
エージェントは次に、最新の報酬$R_{t+1}$と選択したアクション$A_t$で事後信念$P_a$を更新します。

The vanilla Thompson sampling approach is a popular production strategy when it comes to small action space recommendations [31, 50].  
バニラトンプソンサンプリングアプローチは、小さなアクション空間の推奨に関して人気のあるプロダクション戦略です[31, 50]。

Extending Thompson sampling to large action space and contextual bandits, an agent can compute parametric estimates of rewards of context-action pairs by sampling linear model parameters from the posterior belief [1, 4, 46–48] instead of sampling a point estimate from the reward posterior distribution.  
トンプソンサンプリングを大規模なアクション空間およびコンテキストバンディットに拡張すると、エージェントは報酬の事後分布からポイント推定をサンプリングするのではなく、事後信念から線形モデルパラメータをサンプリングすることによってコンテキスト-アクションペアの報酬のパラメトリック推定を計算できます[1, 4, 46–48]。

Here, a linear Thompson sampling agent keeps track of a posterior belief $P[\hat{\theta}]$ over the parameters $\theta$.  
ここで、線形トンプソンサンプリングエージェントは、パラメータ$\theta$に対する事後信念$P[\hat{\theta}]$を追跡します。

The agent chooses action  
エージェントは次のアクションを選択します。

$$
A_t = \arg \max_{a \in A} \hat{\theta}_t^\top x_{t,a}, \quad \hat{\theta}_t \sim P[\hat{\theta}], \quad x_{t,a} = \text{concat}(\psi_{S_t}, \phi_a).
$$

The agent then updates its posterior belief of $P[\hat{\theta}]$ with the latest reward $R_{t+1}$, context $S_t$ and action $A_t$.  
エージェントは次に、最新の報酬$R_{t+1}$、コンテキスト$S_t$、およびアクション$A_t$で$P[\hat{\theta}]$の事後信念を更新します。

The posterior update could be performed via Laplace approximation [36], and is also presented in industry adoptions of linear Thompson sampling [12].  
事後更新はラプラス近似[36]を介して行うことができ、線形トンプソンサンプリングの業界での採用でも示されています[12]。

The method above could be extended to neural networks as the agent can also keep a posterior belief over neural network parameters.  
上記の方法は、エージェントがニューラルネットワークパラメータに対する事後信念を保持できるため、ニューラルネットワークにも拡張できます。

To avoid heavy computation of Laplace approximation, various Bayesian methods have been proposed to achieve posterior updates for distributions over neural network parameters, including deep ensemble [35], ensemble sampling with prior networks [38], Bayes by Backprop [10], Hypermodels [19], Monte-Carlo Dropouts [20] and EpiNet [41].  
ラプラス近似の重い計算を避けるために、ニューラルネットワークパラメータに対する分布の事後更新を達成するために、さまざまなベイズ法が提案されています。これには、ディープアンサンブル[35]、事前ネットワークを用いたアンサンブルサンプリング[38]、バックプロップによるベイズ[10]、ハイパーモデル[19]、モンテカルロドロップアウト[20]、およびEpiNet[41]が含まれます。

Among the methods above, the two ensemble methods [11, 39, 52] and Monte-Carlo Dropout [25] are the most commonly adopted methods for contextual bandits with parameter posterior sampling in a practical setting.  
上記の方法の中で、2つのアンサンブル手法[11, 39, 52]とモンテカルロドロップアウト[25]は、実用的な設定でパラメータ事後サンプリングを伴うコンテキストバンディットに最も一般的に採用されている方法です。

One additional line of work that leverages Thompson sampling for neural networks is neural Thompson sampling [61].  
ニューラルネットワークのためのトンプソンサンプリングを活用するもう1つの研究の流れは、ニューラルトンプソンサンプリング[61]です。

In this approach, instead of sampling from parameters’ posterior distribution, neural Thompson sampling directly samples from the posterior estimate of the reward of a context-action pair.  
このアプローチでは、パラメータの事後分布からサンプリングするのではなく、ニューラルトンプソンサンプリングはコンテキスト-アクションペアの報酬の事後推定から直接サンプリングします。

A Neural Thompson sampling agent keeps track of a matrix $\Gamma$ initialized with $\Gamma = \lambda I$, $I ∈ R^{N × N}$ is an identity matrix, where $\lambda > 0$ is a regularization parameter and $N$ is the parameter size of the neural network.  
ニューラルトンプソンサンプリングエージェントは、$\Gamma = \lambda I$で初期化された行列$\Gamma$を追跡します。$I ∈ R^{N × N}$は単位行列であり、$\lambda > 0$は正則化パラメータで、$N$はニューラルネットワークのパラメータサイズです。

Assuming a Gaussian distributed reward posterior, the variance of the distribution is estimated by  
ガウス分布の報酬事後を仮定すると、分布の分散は次のように推定されます。

$$
\sigma_{t,A}^2 = \lambda g_\theta^\top \left( x_{t,A} \right) \Gamma^{-1} g_\theta \left( x_{t,A} \right),
$$

where $g_\theta$ is the gradient of the output with respect to $\theta$ for the entire neural network.  
ここで、$g_\theta$は、全体のニューラルネットワークに対する$\theta$に関する出力の勾配です。

The agent then chooses action  
エージェントは次にアクションを選択します。

$$
A_t = \arg \max_{a \in A} \hat{R}_{t,a}, \quad \hat{R}_{t,a} \sim N(f_\theta(x_{t,a}), \alpha \sigma_{t,a}^2).
$$

where $\alpha$ is an exploration hyperparameter and $f_\theta$ is the neural network.  
ここで、$\alpha$は探索のハイパーパラメータで、$f_\theta$はニューラルネットワークです。

The agent updates $\Gamma \leftarrow \Gamma + g_\theta (x_{t,A}) g_\theta (x_{t,A})^\top / m$ with $m$ being the width of the neural network, assuming all layers with the same width.  
エージェントは、すべての層が同じ幅であると仮定して、$\Gamma \leftarrow \Gamma + g_\theta (x_{t,A}) g_\theta (x_{t,A})^\top / m$で更新します。

To the best of the authors’ knowledge, the neural Thompson sampling strategy is not well adopted by industry due to its heavy computational complexity.  
著者の知る限り、ニューラルトンプソンサンプリング戦略は、その重い計算複雑性のために業界であまり採用されていません。

#### 3.2 Upper Confidence Bound (UCB), Its Extensions and Related Adoptions
Upper confidence bound (UCB) is a general optimism facing uncertainty exploration strategy where the agent tends to choose actions that it has more uncertainties about.  
#### 3.2 上限信頼区間（UCB）、その拡張と関連する採用
上限信頼区間（UCB）は、エージェントがより不確実性のあるアクションを選択する傾向がある一般的な不確実性に直面した楽観主義の探索戦略です。

The purpose of doing so is to gather information that could help either identify the best action or eliminate bad actions.  
その目的は、最良のアクションを特定するか、悪いアクションを排除するのに役立つ情報を収集することです。

Similar to the subsection above, we first consider a vanilla UCB algorithm [2, 6] for multi-armed bandits.  
上記のサブセクションと同様に、まずはマルチアームバンディットのためのバニラUCBアルゴリズム[2, 6]を考えます。

A vanilla UCB agent selects an action $A_t$ by  
バニラUCBエージェントは、次のようにアクション$A_t$を選択します。

$$
A_t = \arg \max_{a \in A} \left( \frac{1}{t} \sum_{\tau=1}^{t} R_\tau \mathbb{1}(A_\tau = a) + \alpha \sqrt{\frac{\ln(t)}{n_{t,a}}} \right),
$$

where $n_{t,A} = \sum_{\tau=1}^{t} \mathbb{1}(A_\tau = A)$ and $\alpha \in \mathbb{R}^+$ is a hyperparameter.  
ここで、$n_{t,A} = \sum_{\tau=1}^{t} \mathbb{1}(A_\tau = A)$であり、$\alpha \in \mathbb{R}^+$はハイパーパラメータです。

There have been multiple lines of work analyzing vanilla UCB’s impact on production recommender systems in terms of degenerating feedback loops [26, 32], modeling attritions [9] and its extension to Collaborative Filtering [40].  
バニラUCBの生産レコメンダーシステムにおける影響を、劣化するフィードバックループ[26, 32]、モデル化の喪失[9]、および協調フィルタリングへの拡張[40]の観点から分析する研究がいくつかあります。

The immediate extension to UCB to linear bandit problems is LinUCB [16, 37].  
UCBの線形バンディット問題への即時の拡張はLinUCB[16, 37]です。

A LinUCB agent initializes two variables for any new action $A$ that it has never seen before, $\Gamma_A = I_d$ (d次元の単位行列)と$b_A = 0_{d \times 1}$ (d次元のゼロベクトル)であり、ここで$d$は線形パラメータのサイズです。  
LinUCBエージェントは、これまで見たことのない新しいアクション$A$に対して2つの変数を初期化します。$\Gamma_A = I_d$（d次元の単位行列）と$b_A = 0_{d \times 1}$（d次元のゼロベクトル）であり、ここで$d$は線形パラメータのサイズです。

At time step $t$, given a new context representation $\psi_{S_t}$ and each action $\phi_A$, the agent concatenates the two vectors to get a context-action pair representation $x_{t,A} = \text{concat}(\psi_{S_t}, \phi_A)$.  
時刻$t$において、新しいコンテキスト表現$\psi_{S_t}$と各アクション$\phi_A$が与えられると、エージェントは2つのベクトルを連結してコンテキスト-アクションペアの表現$x_{t,A} = \text{concat}(\psi_{S_t}, \phi_A)$を得ます。

The agent selects action  
エージェントは次のアクションを選択します。

$$
A_t = \arg \max_{a \in A} \left( \Gamma_a^{-1} b_a \right)^\top x_{t,a} + \alpha \sqrt{x_{t,a}^\top \Gamma_a^{-1} x_{t,a}}.
$$

After receiving $R_{t+1}$, the agent then updates $\Gamma_{A_t}$ and $b_{A_t}$ with $\Gamma_{A_t} \leftarrow \Gamma_{A_t} + x_{t,A_t} x_{t,A_t}^\top$ and $b_{A_t} \leftarrow b_{A_t} + R_{t+1} x_{t,A_t}$.  
$R_{t+1}$を受け取った後、エージェントは$\Gamma_{A_t} \leftarrow \Gamma_{A_t} + x_{t,A_t} x_{t,A_t}^\top$および$b_{A_t} \leftarrow b_{A_t} + R_{t+1} x_{t,A_t}$で$\Gamma_{A_t}$と$b_{A_t}$を更新します。

LinUCB is a popular algorithm for adoption in many industry usecases and particularly in the space of recommender systems [37, 44, 54, 63].  
LinUCBは、多くの業界のユースケース、特にレコメンダーシステムの分野で採用される人気のあるアルゴリズムです[37, 44, 54, 63]。

With the rise of neural networks and deep learning, so comes the need for optimism based exploration neural methods.  
ニューラルネットワークと深層学習の台頭に伴い、楽観主義に基づく探索ニューラル手法の必要性が生じます。

NeuralUCB [64] and NeuralLinUCB [59] are two representing examples of such algorithms.  
NeuralUCB[64]とNeuralLinUCB[59]は、そのようなアルゴリズムの代表的な例です。

We first introduce NeuralLinUCB as it’s a natural extension of LinUCB.  
まず、NeuralLinUCBを紹介します。これはLinUCBの自然な拡張です。

Given a neural network representation, NeuralLinUCB no longer initiates a matrix $\Gamma_A$ for each action $A$ and instead keeps track of a single matrix $\Gamma$ initialized with $\lambda I$ where $\lambda > 0$ is a regularization factor and $I ∈ R^{N × N}$ is an identity matrix.  
ニューラルネットワークの表現が与えられると、NeuralLinUCBは各アクション$A$に対して行列$\Gamma_A$を初期化せず、代わりに$\lambda > 0$が正則化因子であり、$I ∈ R^{N × N}$が単位行列である単一の行列$\Gamma$を追跡します。

Suppose the neural network’s last layer representation is $\sigma_\theta(x_{t,A}) ∈ R^N$ and full model output $f_\theta(x_{t,A}) ∈ R$, the agent takes action  
ニューラルネットワークの最終層の表現を$\sigma_\theta(x_{t,A}) ∈ R^N$、完全モデル出力を$f_\theta(x_{t,A}) ∈ R$と仮定すると、エージェントは次のアクションを取ります。

$$
A_t = \arg \max_{a \in A} \left( f_\theta(x_{t,a}) + \alpha \sigma_\theta(x_{t,a})^\top \Gamma^{-1} \sigma_\theta(x_{t,a}) \right).
$$

with the same update for $\Gamma$ and $b$ except that now the update happens with the representation $\sigma_\theta(x_{t,A})$ instead of $x_{t,A}$.  
$\Gamma$と$b$の更新は同じですが、今は更新が表現$\sigma_\theta(x_{t,A})$で行われ、$x_{t,A}$ではありません。

NeuralUCB follows the same principle as above, but replacing $\sigma_\theta(x_{t,A})$ with the gradients of all parameters within the neural network.  
NeuralUCBは上記と同じ原則に従いますが、$\sigma_\theta(x_{t,A})$をニューラルネットワーク内のすべてのパラメータの勾配に置き換えます。

Although empirically the above neural methods, Neural Thompson sampling, Neural UCB and Neural LinUCB, have achieved good performance on synthetic datasets, their downside is that they all require inverting a square matrix with its dimension equal to either the entire neural network’s parameter size or the size of the last layer representation.  
経験的には、上記のニューラル手法、ニューラルトンプソンサンプリング、ニューラルUCB、ニューラルLinUCBは合成データセットで良好なパフォーマンスを達成していますが、彼らの欠点は、すべてが正方行列を反転する必要があり、その次元はニューラルネットワーク全体のパラメータサイズまたは最終層の表現のサイズに等しいことです。

Both in many cases are intractable, especially for real-world environments and complex neural networks.  
多くのケースで、これは扱いきれないものであり、特に実世界の環境や複雑なニューラルネットワークにおいてはそうです。

#### 4 Epistemic Neural Recommendation
In this section, we introduce a novel architecture for scalable neural contextual bandit problems, drawing inspiration from Thompson sampling and recent developments in epistemic neural networks (ENN) and EpiNet [41].  
#### 4 エピステミックニューラルレコメンデーション
このセクションでは、トンプソンサンプリングと最近のエピステミックニューラルネットワーク（ENN）およびEpiNet[41]の進展からインスピレーションを得た、スケーラブルなニューラルコンテキストバンディット問題のための新しいアーキテクチャを紹介します。

As discussed in Section 3.1, the objective of a deep learning-based Thompson sampling strategy is to accurately estimate the uncertainty of a prediction, pertaining to a context-action pair, while keeping computational costs to a minimum.  
セクション3.1で述べたように、深層学習に基づくトンプソンサンプリング戦略の目的は、コンテキスト-アクションペアに関連する予測の不確実性を正確に推定し、計算コストを最小限に抑えることです。

A significant drawback of many neural methods for Thompson sampling and UCB is their computationally expensive uncertainty estimation process, which impedes their integration into real-world environments.  
トンプソンサンプリングやUCBのための多くのニューラル手法の重要な欠点は、計算コストの高い不確実性推定プロセスであり、これが実世界の環境への統合を妨げます。

The primary aim of our proposed architecture and design is to address this very issue, while enhancing model performance.  
私たちの提案するアーキテクチャと設計の主な目的は、この問題に対処しながらモデルのパフォーマンスを向上させることです。

#### 4.1 Informative Neural Representation
A key aspect shared across all neural exploration methods is the generation of effective representations for context-action pairs.  
#### 4.1 有益なニューラル表現
すべてのニューラル探索手法に共通する重要な側面は、コンテキスト-アクションペアのための効果的な表現を生成することです。

Within the contextual bandit framework, there are three main representation factors to consider: action representation, context representation, and the interaction between context and action.  
コンテキストバンディットの枠組み内では、考慮すべき3つの主要な表現要因があります：アクション表現、コンテキスト表現、およびコンテキストとアクションの相互作用です。

We assume a general and unnormalized feature representation from the environment for both contexts and actions.  
私たちは、コンテキストとアクションの両方に対して、環境からの一般的で非正規化された特徴表現を仮定します。

To distill both context and action feature representation vectors, we initially feed each vector into a linear layer followed by a ReLU activation function.  
コンテキストとアクションの特徴表現ベクトルを抽出するために、最初に各ベクトルを線形層に入力し、その後にReLU活性化関数を適用します。

This is subsequently followed by a Layer Normalization (LayerNorm) layer [7].  
その後、レイヤー正規化（LayerNorm）層[7]が続きます。

Given that raw features can contain disproportionately large values that are challenging to normalize - particularly in an online bandit setting where data continually stream in - it is crucial to employ layer normalization.  
生の特徴が正規化が難しい不均衡に大きな値を含む可能性があるため、特にデータが継続的にストリーミングされるオンラインバンディット設定では、レイヤー正規化を使用することが重要です。

This technique ensures smoother gradients, promoting stability and generalizability [58].  
この技術は、より滑らかな勾配を保証し、安定性と一般化能力を促進します[58]。

More formally,  
より正式には、

$$
h_\beta^{context}(\psi_{S_t}) = \text{LayerNorm}(\text{ReLU}(\beta_{context}^\top [\psi_{S_t}])),
$$

$$
h_\beta^{action}(\phi_A) = \text{LayerNorm}(\text{ReLU}(\beta_{action}^\top [\phi_A])).
$$

where $\theta_{context} ∈ R^{d_S}$ and $\theta_{action} ∈ R^{d_A}$ are the parameters for context and action summarization.  
ここで、$\theta_{context} ∈ R^{d_S}$および$\theta_{action} ∈ R^{d_A}$は、コンテキストとアクションの要約のためのパラメータです。

Note that after summarization through these two layers, the outputs are of the same shape.  
これらの2つの層を通じて要約した後、出力は同じ形状になります。

Having summarized and normalized representations for both action and context, we now model the interaction between these two entities.  
アクションとコンテキストの両方の要約および正規化された表現を持って、これら2つのエンティティ間の相互作用をモデル化します。

Collaborative Filtering [23, 29, 45] and Matrix Factorization [34] provide intuitive models for this interaction.  
協調フィルタリング[23, 29, 45]と行列分解[34]は、この相互作用のための直感的なモデルを提供します。

Inspired by these methods, we use element-wise multiplication to represent interactions,  
これらの方法に触発されて、相互作用を表現するために要素ごとの乗算を使用します。

$$
I(\psi_{S_t}, \phi_A) = h_\beta^{context}(\psi_{S_t}) \odot h_\beta^{action}(\phi_A).
$$

Utilizing the above three representations, we concatenate the three vectors to derive  
上記の3つの表現を利用して、3つのベクトルを連結して導出します。

$$
x_{t,A} = \text{concat}(h_\beta^{context}(\psi_{S_t}), h_\beta^{action}(\phi_A), I(\psi_{S_t}, \phi_A)).
$$

Notably, this representation diverges from Neural Collaborative Filtering (NCF) [28] in two primary ways.  
特に、この表現は、2つの主要な方法でニューラル協調フィルタリング（NCF）[28]から逸脱します。

Firstly, NCF can only manage id-listed features and it aggregates the concatenation of action and context through multi-layer perceptrons.  
第一に、NCFはIDリストされた特徴のみを管理でき、アクションとコンテキストの連結を多層パーセプトロンを通じて集約します。

In contrast, our approach can handle feature vectors without making any preliminary assumptions about the input feature shape or values.  
対照的に、私たちのアプローチは、入力特徴の形状や値に関する事前の仮定を行うことなく、特徴ベクトルを処理できます。

Secondly, we use the representations obtained through summarization for uncertainty estimation, as discussed in the following subsection.  
第二に、次のサブセクションで説明するように、不確実性推定のために要約を通じて得られた表現を使用します。

Moreover, we demonstrate in later sections through empirical studies that the direct application of NCF with uncertainty estimation yields inferior performance compared to our method.  
さらに、後のセクションで実証研究を通じて、不確実性推定を伴うNCFの直接的な適用が私たちの方法と比較して劣ったパフォーマンスをもたらすことを示します。

#### 4.2 Epistemic Neural Recommendation (ENR)
Using the representation derived above, we can now design a neural network for both point estimate and uncertainty estimation.  
#### 4.2 エピステミックニューラルレコメンデーション（ENR）
上記で導出した表現を使用して、ポイント推定と不確実性推定の両方のためのニューラルネットワークを設計できます。

For efficient epistemic uncertainty estimation using neural networks, we employ EpiNet [41], an auxiliary architecture for a general neural network.  
ニューラルネットワークを使用した効率的なエピステミック不確実性推定のために、一般的なニューラルネットワークの補助アーキテクチャであるEpiNet[41]を採用します。

This architecture leverages the final layer representation of a neural network, along with an epistemic index $z$, to generate a sample from the posterior.  
このアーキテクチャは、ニューラルネットワークの最終層の表現とエピステミックインデックス$z$を活用して、事後からサンプルを生成します。

EpiNet presents a cost-effective method for constructing ENNs, which has been demonstrated to excel in making joint predictions for classification and supervised learning tasks, while achieving strong performance in synthesized neural logistic bandits with minimal additional computational costs.  
EpiNetは、ENNを構築するためのコスト効率の良い方法を提供し、分類および教師あり学習タスクのための共同予測を行うのに優れていることが示されており、最小限の追加計算コストで合成ニューラルロジスティックバンディットで強力なパフォーマンスを達成しています。

However, a drawback of only utilizing the last layer representation, particularly in a contextual bandit setting, is the diminished representation power.  
しかし、特にコンテキストバンディット設定において、最終層の表現のみを利用することの欠点は、表現力が低下することです。

The interactions between context and action are summarized through multi-layers perceptrons for marginal predictions, and considerable information is lost in the process.  
コンテキストとアクションの相互作用は、限界予測のために多層パーセプトロンを通じて要約され、その過程でかなりの情報が失われます。

Motivated by this, we introduce Epistemic Neural Recommendation (ENR) that generates improved posterior samples via more informative representations.  
これに触発されて、より有益な表現を通じて改善された事後サンプルを生成するエピステミックニューラルレコメンデーション（ENR）を紹介します。

The remaining architecture of ENR is comprised of three parts: a function $f_\theta^x : R^{3d_E} \to R$ for marginal prediction, and two functions $g_\sigma$ and $g_{\sigma_p}$, both mapping from $R^{3d_E}$ to $R^{d_z}$, for uncertainty estimation.  
ENRの残りのアーキテクチャは、限界予測のための関数$f_\theta^x : R^{3d_E} \to R$と、不確実性推定のための2つの関数$g_\sigma$と$g_{\sigma_p}$から構成されており、両方とも$R^{3d_E}$から$R^{d_z}$にマッピングします。

Upon extraction of $x_{t,A}$, we employ $f_\theta^x$ to make the marginal prediction via $f_\theta^x(x_{t,A})$.  
$x_{t,A}$を抽出した後、$f_\theta^x$を使用して$f_\theta^x(x_{t,A})$を介して限界予測を行います。

In addition to $f_\theta^x$, $g_\sigma$ and $g_{\sigma_p}$ are independently initialized through Glorot Initialization [8, 22], and $g_{\sigma_p}$ remains constant throughout its lifetime, thereby providing robust regularization.  
$f_\theta^x$に加えて、$g_\sigma$と$g_{\sigma_p}$はGlorot初期化[8, 22]を通じて独立に初期化され、$g_{\sigma_p}$はその生涯を通じて一定のままであり、堅牢な正則化を提供します。

To initialize this segment of the network, ENR samples an epistemic index $z$ from its prior $P_z$, which could either be a discrete one-hot vector or a standard multivariate Gaussian sample.  
このネットワークのセグメントを初期化するために、ENRはその事前$P_z$からエピステミックインデックス$z$をサンプリングします。これは、離散的なワンホットベクトルまたは標準多変量ガウスサンプルのいずれかです。

The sampled $z$ is then concatenated with $x_{t,A}$ and processed through both $g_\sigma$ and $g_{\sigma_p}$.  
サンプリングされた$z$は次に$x_{t,A}$と連結され、$g_\sigma$と$g_{\sigma_p}$の両方を通じて処理されます。

Consequently, the uncertainty estimation is $(g_\sigma(x_{t,A}, z) + g_{\sigma_p}(x_{t,A}, z))^\top z$.  
その結果、不確実性推定は$(g_\sigma(x_{t,A}, z) + g_{\sigma_p}(x_{t,A}, z))^\top z$となります。

Hence the final output of ENR is  
したがって、ENRの最終出力は次のようになります。

$$
f_\theta(\psi_S, \phi_A, z) = f_\theta^x(x_{t,A}) + (g_\sigma(sg[x_{t,A}], z) + g_{\sigma_p}(sg[x_{t,A}], z))^\top z,
$$

where $x_{t,A}$ is defined in Equation 11, $\theta = (\theta_x, \sigma, \sigma_p, \beta_{context}, \beta_{action})$, and $sg[·]$ stops gradient flow of the parameter within the bracket.  
ここで、$x_{t,A}$は式11で定義され、$\theta = (\theta_x, \sigma, \sigma_p, \beta_{context}, \beta_{action})$であり、$sg[·]$は括弧内のパラメータの勾配フローを停止します。

Note that, if the reward function is a binary variable, then a sigmoid would be added to the final output of $f_\theta(\psi_S, \phi_A, z)$ as neural logistic regression is a common setup in RS.  
報酬関数がバイナリ変数である場合、$f_\theta(\psi_S, \phi_A, z)$の最終出力にシグモイドが追加されることに注意してください。ニューラルロジスティック回帰はRSで一般的な設定です。

With the neural network above, an ENR Thompson sampling agent executes action  
上記のニューラルネットワークを使用して、ENRトンプソンサンプリングエージェントはアクションを実行します。

$$
A_t = \arg \max_{a \in A} f_\theta(\psi_{S_t}, \phi_a, z), \quad z \sim P_z.
$$

After receiving reward $R_{t+1}$, then the agent can update the neural network with  
報酬$R_{t+1}$を受け取った後、エージェントは次のようにニューラルネットワークを更新できます。

$$
\theta \leftarrow \theta - \alpha \nabla_\theta L(R_{t+1}, f_\theta(\psi_{S_t}, \phi_{A_t}, z)),
$$

where $z \in Z$ through stochastic gradient descent, where $Z$ is a set of epistemic indices sampled from $P_z$ and $\alpha$ is the learning rate.  
ここで、$z \in Z$は確率的勾配降下法を通じて、$Z$は$P_z$からサンプリングされたエピステミックインデックスのセットであり、$\alpha$は学習率です。

In practice, we perform batch updates through sampling from a replay buffer and uses other more advanced optimization strategies such as ADAM [33] for parameter updates.  
実際には、リプレイバッファからサンプリングすることによってバッチ更新を行い、パラメータ更新のためにADAM[33]などの他のより高度な最適化戦略を使用します。

The loss function here could be cross-entropy loss for neural logistic contextual bandits and mean squared error loss for contextual bandits with non-binary reward.  
ここでの損失関数は、ニューラルロジスティックコンテキストバンディットのためのクロスエントロピー損失と、非バイナリ報酬を持つコンテキストバンディットのための平均二乗誤差損失です。

For the full illustration of the architecture, please refer to Figure 2. For a detailed algorithm illustration, please refer to Algorithm 1.  
アーキテクチャの完全な説明については、図2を参照してください。詳細なアルゴリズムの説明については、アルゴリズム1を参照してください。

We would like to also note that this algorithm is a full online bandit algorithm without any prior knowledge or pre-training.  
このアルゴリズムは、事前知識や事前学習なしの完全なオンラインバンディットアルゴリズムであることも注記しておきます。

This algorithm can also be extended to perform offline pretraining before online interactions to reduce the amount of exploration required.  
このアルゴリズムは、オンラインインタラクションの前にオフライン事前学習を行って、必要な探索量を減らすように拡張することもできます。

We leave this for future work.  
これについては今後の作業に残します。

#### 5 Experiments
In this section, we will go through a set of experiments ranging from a toy experiment to large-scale real-world data experiments.  
#### 5 実験
このセクションでは、玩具実験から大規模な実世界データ実験までの一連の実験を行います。

The dataset statistics are shown in Table 1. Each of the dataset has millions of interactions.  
データセットの統計は表1に示されています。各データセットには数百万のインタラクションがあります。

We will compare ENR and EpiNet  
私たちはENRとEpiNetを比較します。

**Table 1: Experiment Dataset Statistics**  
**表1: 実験データセットの統計**

| Dataset | # Users | # Items | # Interactions |
|---------|---------|---------|----------------|
| MIND [57] | 1,000,000 | 160,000 | 15,000,000 |
| KuaiRec [21] | 1,411 | 3,327 | 4,676,570 |

against 𝜖Greedy, Ensemble Sampling with Prior Networks (Ensemble) [38], Neural Thompson Sampling (Neural TS) [61], Neural UCB [64], and Neural LinUCB [59], each with a similar sized neural network.  
𝜖Greedy、事前ネットワークを用いたアンサンブルサンプリング（アンサンブル）[38]、ニューラルトンプソンサンプリング（ニューラルTS）[61]、ニューラルUCB[64]、およびニューラルLinUCB[59]と比較します。各々は同様のサイズのニューラルネットワークを持っています。

In addition, to assess advantages attributable to the architecture of ENR, we will also evaluate it against a few well recognized RS neural network architecture including, Neural Collaborative Filtering (NCF) [28], Neural Recommendation with Attentive MultiView Learning (NAML) [55], Neural Recommendation with MultiHead Self-Attention (NRMS) [56], Wide and Deep [14], and DeepFM [27], combined with exploration strategies above.  
さらに、ENRのアーキテクチャに起因する利点を評価するために、ニューラル協調フィルタリング（NCF）[28]、注意を持つマルチビュー学習によるニューラル推薦（NAML）[55]、マルチヘッド自己注意によるニューラル推薦（NRMS）[56]、Wide and Deep [14]、およびDeepFM [27]などのいくつかの認知されたRSニューラルネットワークアーキテクチャと、上記の探索戦略を組み合わせて評価します。

To ensure fairness of evaluation, we ensure that all neural network architectures other than vanilla MLP has a similar parameter size.  
評価の公平性を確保するために、バニラMLP以外のすべてのニューラルネットワークアーキテクチャが同様のパラメータサイズを持つことを確認します。

See Table 3. The algorithms all adopt ADAM [33] for model optimization.  
表3を参照してください。すべてのアルゴリズムはモデル最適化のためにADAM[33]を採用します。

Note that for both Neural UCB and Neural Thompson Sampling, due to their scalability, we are only able to experiment them with their last layer versions, where we only compute gradients of the last layer of the neural networks.  
ニューラルUCBとニューラルトンプソンサンプリングの両方について、スケーラビリティのために、私たちはそれらの最終層バージョンでのみ実験でき、ニューラルネットワークの最終層の勾配のみを計算します。

The full Neural UCB and Neural Thompson Sampling agents require inverting matrices of sizes $10^6 × 10^6$ (7.45 TB of memory and $O(10^{18})$ complexity) and $10^7 × 10^7$ (745 TB of memory and $O(10^{21})$ complexity) for MIND and KuaiRec experiments respectively, which are intractable in most commercial machines.  
完全なニューラルUCBおよびニューラルトンプソンサンプリングエージェントは、MINDおよびKuaiRec実験に対してそれぞれサイズ$10^6 × 10^6$（7.45 TBのメモリと$O(10^{18})$の複雑さ）および$10^7 × 10^7$（745 TBのメモリと$O(10^{21})$の複雑さ）の行列を反転する必要があり、これはほとんどの商業機械では扱いきれません。

See more details of computation costs in Table 4 and 5 respectively for two experiments and all experiments are performed on an AWS p4d24xlarge machine with 8 A100 GPUs, each GPU with 40 GB of GPU memory.  
計算コストの詳細については、表4および5を参照してください。すべての実験は、8つのA100 GPUを持つAWS p4d24xlargeマシンで実行され、各GPUは40 GBのGPUメモリを持っています。

NeuralLinUCB requires 6x and 3.5x inference time compared to our method in two real-world experiments with a similar training time.  
NeuralLinUCBは、同様のトレーニング時間で2つの実世界の実験において、私たちの方法と比較して6倍および3.5倍の推論時間を必要とします。

Simplified versions of NeuralTS and NeuralUCB using only gradients from the last layer of NNs require 10x and 100x inference time compared to our method in these experiments.  
ニューラルネットワークの最終層の勾配のみを使用したNeuralTSおよびNeuralUCBの簡略化バージョンは、これらの実験において私たちの方法と比較して10倍および100倍の推論時間を必要とします。

Lastly, Ensemble requires a similar inference time, but requires 5x training time compared to our method with parallel computing optimization.  
最後に、アンサンブルは同様の推論時間を必要としますが、私たちの方法と比較して5倍のトレーニング時間を必要とします。並列計算の最適化があります。

NeuralLinUCB, NeuralUCB, NeuralTS all require orders of magnitude higher inference cost and Ensemble requires orders of magnitude higher training cost.  
NeuralLinUCB、NeuralUCB、NeuralTSはすべて桁違いに高い推論コストを必要とし、アンサンブルは桁違いに高いトレーニングコストを必要とします。

We will use average reward as performance metric in the following experiments (average click-through rate and average user rating in MIND and KuaiRec respectively).  
次の実験では、平均報酬をパフォーマンスメトリックとして使用します（それぞれMINDおよびKuaiRecでの平均クリック率と平均ユーザ評価）。

We choose to not use classic metrics like NDCG or precision because they are supervised-learning metrics.  
NDCGや精度のような古典的なメトリックは、教師あり学習メトリックであるため使用しないことにします。

In online bandits, the agent’s optimal strategy could try to explore and retrieve information instead of optimizing these metrics.  
オンラインバンディットでは、エージェントの最適な戦略は、これらのメトリックを最適化するのではなく、探索して情報を取得しようとする可能性があります。

#### 5.1 Toy Experiment
For this experiment, we define a synthetic environment to evaluate the performance of ENR compared to various baselines mentioned above.  
#### 5.1 玩具実験
この実験では、上記のさまざまなベースラインと比較してENRのパフォーマンスを評価するために、合成環境を定義します。

According to Section 2, the synthetic environment is characterized as: Both action and context vectors are of dimension 100.  
セクション2に従って、合成環境は次のように特徴付けられます：アクションとコンテキストのベクトルはどちらも次元100です。

$$
R_{t+1} \sim \text{Bernoulli}[\sigma(\theta^\top \text{concat}(\psi_{S_t}, \phi_{A_t}))].
$$

The size of A is 100. $\sigma$ is the Sigmoid function and both $\theta$ is unknown to all the agents.  
$A$のサイズは100です。$\sigma$はシグモイド関数であり、$\theta$はすべてのエージェントにとって未知です。

**Table 2: MIND Dataset Illustration**  
**表2: MINDデータセットの説明**

| Impression ID | User ID | Time | User Interest History | News with Labels |
|---------------|---------|------|-----------------------|------------------|
| 91            | U397059 | 11/15/2019 10:22:32 AM | N106403 N71977 N97080 N102132 N129416-0 N26703-1 N120089-1 N53018-0 N89764-0 |

**Table 3: Parameter Sizes across Different Architectures**  
**表3: 異なるアーキテクチャ間のパラメータサイズ**

| Algorithm | MIND | KuaiRec |
|-----------|------|---------|
| MLP | $0.76 \times 10^6$ | $1.21 \times 10^7$ |
| Wide & Deep | / | $2.33 \times 10^7