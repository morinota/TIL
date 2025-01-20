
# DEEP LEARNING WITH LOGGED BANDIT FEEDBACK  
**Maarten de Rijke**  
アムステルダム大学  
derijke@uva.nl  
**Thorsten Joachims**  
コーネル大学  
tj@cs.cornell.edu  
**Adith Swaminathan**  
マイクロソフトリサーチ  
adswamin@microsoft.com  

### ABSTRACT 要約

We propose a new output layer for deep neural networks that permits the use of logged contextual bandit feedback for training. 
私たちは、トレーニングのためにログされたコンテキストバンディットフィードバックを使用できる新しい出力層を深層ニューラルネットワークのために提案します。

Such contextual bandit feedback can be available in huge quantities (e.g., logs of search engines, recommender systems) at little cost, opening up a path for training deep networks on orders of magnitude more data. 
**このようなコンテキストバンディットフィードバックは、大量に（例：検索エンジンやレコメンダーシステムのログ）低コストで利用可能であり、深層ネットワークを桁違いのデータでトレーニングする道を開く**。

To this effect, we propose a counterfactual risk minimization approach for training deep networks using an equivariant empirical risk estimator with variance regularization, BanditNet, and show how the resulting objective can be decomposed in a way that allows stochastic gradient descent training. 
この目的のために、私たちは、分散正則化を伴う等変的経験リスク推定器を使用した深層ネットワークのトレーニングのための反事実リスク最小化アプローチ、BanditNetを提案し、得られた目的が確率的勾配降下法によるトレーニングを可能にする方法で分解できることを示します。

We empirically demonstrate the effectiveness of the method by showing how deep networks – ResNets in particular – can be trained for object recognition without conventionally labeled images. 
私たちは、深層ネットワーク、特にResNetが従来のラベル付けされた画像なしで物体認識のためにトレーニングできる方法を示すことによって、この手法の有効性を実証的に示します。

<!-- ここまで読んだ! -->

### 1 INTRODUCTION はじめに

Log data can be recorded from online systems such as search engines, recommender systems, or online stores at little cost and in huge quantities.  
**ログデータは、検索エンジン、レコメンダーシステム、またはオンラインストアなどのオンラインシステムから、低コストで大量に記録することができます**。(なるほど、あまり意識したことなかったけど、低コストなのか...!:thinking:)
For concreteness, consider the interaction logs of an ad-placement system for banner ads.  
具体的には、バナー広告の広告配置システムのインタラクションログを考えてみましょう。  
Such logs typically contain a record of the input to the system (e.g., features describing the user, banner ad, and page), the action that was taken by the system (e.g., a specific banner ad that was placed) and the feedback furnished by the user (e.g., clicks on the ad, or monetary payoff).  
このようなログには、通常、システムへの入力（例：ユーザ、バナー広告、ページを説明する特徴）、システムによって取られたアクション（例：配置された特定のバナー広告）、およびユーザから提供されたフィードバック（例：広告のクリックや金銭的な報酬）が記録されています。  
This feedback, however, provides only partial information – “contextual-bandit feedback” – limited to the actions taken by the system.  
しかし、**このフィードバックは、システムによって取られたアクションに限定された部分的な情報、すなわち「コンテキストバンディットフィードバック」**しか提供しません。  
We do not get to see how the user would have responded, if the system had chosen a different action (e.g., other ads or banner types).  
システムが異なるアクション（例：他の広告やバナータイプ）を選択していた場合、ユーザがどのように反応したかを見ることはできません。 (反実仮想!)
Thus, the feedback for all other actions the system could have taken is typically not known.  
したがって、システムが取ることができた他のすべてのアクションに対するフィードバックは通常知られていません。  
This makes learning from log data fundamentally different from traditional supervised learning, where “correct” predictions and a loss function provide feedback for all actions.  
**これにより、ログデータからの学習は、すべてのアクションに対して「正しい」予測と損失関数がフィードバックを提供する従来の教師あり学習とは根本的に異なります**。(＝これが、推薦システムは予測問題じゃなくて意思決定の最適化だよ、と言われる所以だ...!:thinking:)

In this paper, we propose a new output layer for deep neural networks that allows training on logged contextual bandit feedback.  
本論文では、ログされたコンテキストバンディットフィードバックでのトレーニングを可能にする**深層ニューラルネットワークの新しい出力層**を提案します。(出力層を提案??)
By circumventing the need for full-information feedback, our approach opens a new and intriguing pathway for acquiring knowledge at unprecedented scale, giving deep neural networks access to this abundant and ubiquitous type of data.  
完全な情報フィードバックの必要性を回避することで、私たちのアプローチは、前例のない規模で知識を獲得するための新しく魅力的な道を開き、深層ニューラルネットワークにこの豊富で普遍的なデータタイプへのアクセスを提供します。  
Similarly, it enables the application of deep learning even in domains where manually labeling full-information feedback is not viable.  
**同様に、手動で完全な情報フィードバックにラベル付けすることが実行可能でない領域でも、深層学習の適用を可能にします**。(なるほど、そもそもラベル付けされてないデータには、教師あり学習できないよね、という前提か...!:thinking:)  

In contrast to online learning with contextual bandit feedback (e.g., (Williams, 1992; Agarwal et al., 2014)), we perform **batch learning from bandit feedback (BLBF)** (Beygelzimer & Langford, 2009; Swaminathan & Joachims, 2015a;b;c) and the algorithm does not require the ability to make interactive interventions.  
コンテキストバンディットフィードバックを用いた**オンライン学習（例：（Williams, 1992; Agarwal et al., 2014））とは対照的に、私たちはバンディットフィードバックからのバッチ学習（BLBF）（Beygelzimer & Langford, 2009; Swaminathan & Joachims, 2015a;b;c）を行い**、アルゴリズムはインタラクティブな介入を行う能力を必要としません。 
At the core of the new output layer for BLBF training of deep neural networks lies a counterfactual training objective that replaces the conventional cross-entropy objective.  
深層ニューラルネットワークのBLBFトレーニングのための新しい出力層の中心には、**従来のクロスエントロピー目的を置き換える反事実的トレーニング目的**があります。(あ、目的関数をちゃんと設計したよ、の原点的な論文なのかも...!:thinking:)  
Our approach – called BanditNet – follows the view of a deep neural network as a stochastic policy.  
私たちのアプローチは、BanditNetと呼ばれ、**深層ニューラルネットワークを確率的方策として捉えます**。  
We propose a counterfactual risk minimization (CRM) objective that is based on an equivariant estimator of the true error that only requires propensity-logged contextual bandit feedback.  
私たちは、傾向ログされたコンテキストバンディットフィードバックのみを必要とする真の誤差の等変推定量に基づく反事実的リスク最小化（CRM）目的を提案します。
This makes our training objective fundamentally different from the conventional cross-entropy objective for supervised classification, which requires full-information feedback.  
これにより、**私たちのトレーニング目的は、完全な情報フィードバックを必要とする従来の教師あり分類のクロスエントロピー目的とは根本的に異なります**。  
Equivariance in our context means that the learning result is invariant to additive translations of the loss, and it is more formally defined in Section 3.2.  
私たちの文脈における等変性は、学習結果が損失の加法的変換に対して不変であることを意味し、これはセクション3.2でより正式に定義されています。  
To enable large-scale training, we show how this training objective can be decomposed to allow stochastic gradient descent (SGD) optimization.  
大規模トレーニングを可能にするために、このトレーニング目的がどのように分解され、確率的勾配降下（SGD）最適化を可能にするかを示します。  

In addition to the theoretical derivation of BanditNet, we present an empirical evaluation that verifies the applicability of the theoretical argument.  
BanditNetの理論的導出に加えて、理論的議論の適用可能性を検証する実証評価を示します。  
It demonstrates how a deep neural network architecture can be trained in the BLBF setting.  
これは、深層ニューラルネットワークアーキテクチャがBLBF設定でどのようにトレーニングできるかを示しています。  
In particular, we derive a BanditNet version of ResNet (He et al., 2016) for visual object classification.  
特に、視覚オブジェクト分類のためのResNet（He et al., 2016）のBanditNetバージョンを導出します。  
Despite using potentially much cheaper data, we find that Bandit-ResNet can achieve the same classification performance given sufficient amounts of contextual bandit feedback as ResNet trained with cross-entropy on conventionally (full-information) annotated images.  
**潜在的にはるかに安価なデータ(=教師ラベルのアノテーション作業が不要、という意味で...!)を使用**しているにもかかわらず、Bandit-ResNetは、従来の（完全情報）注釈付き画像でクロスエントロピーでトレーニングされたResNetと同じ分類性能を達成できることがわかりました。  
To easily enable experimentation on other applications, we share an implementation of BanditNet.[1]  
他のアプリケーションでの実験を容易にするために、BanditNetの実装を共有します。[1]

<!-- ここまで読んだ! -->

### 2 RELATED WORK 関連研究

(BLBF = Batch Learning from Bandit Feedback。つまり、バンディットフィードバックからのバッチ学習)

Several recent works have studied weak supervision approaches for deep learning. 
最近のいくつかの研究では、深層学習のための弱い監視アプローチが研究されています。
Weak supervision has been used to pre-train good image features (Joulin et al., 2016) and for information retrieval (Dehghani et al., 2017). 
弱い監視は、良好な画像特徴の事前学習（Joulin et al., 2016）や情報検索（Dehghani et al., 2017）に使用されています。
Closely related works have studied label corruption on CIFAR10 recently (Zhang et al., 2016). 
関連する研究では、最近CIFAR10におけるラベルの破損が研究されています（Zhang et al., 2016）。
However, all these approaches use weak supervision/corruption to construct noisy proxies for labels, and proceed with traditional supervised training (using cross-entropy or mean-squared-error loss) with these proxies. 
しかし、これらのアプローチはすべて、ラベルのためのノイズの多い代理を構築するために弱い監視/破損を使用し、これらの代理を用いて従来の教師あり学習（クロスエントロピーまたは平均二乗誤差損失を使用）を進めます。
In contrast, we work in the BLBF setting, which is an orthogonal data-source, and modify the loss functions optimized by deep nets to directly implement risk minimization.  
対照的に、私たちはBLBF設定で作業し、これは直交データソースであり、リスク最小化を直接実装するために深層ネットワークによって最適化された損失関数を修正します。

Virtually all previous methods that can learn from logged bandit feedback employ some form of risk minimization principle (Vapnik, 1998) over a model class. 
ログされたバンディットフィードバックから学習できるほぼすべての以前の方法は、モデルクラスに対してリスク最小化原則の何らかの形を採用しています（Vapnik, 1998）。
Most of the methods (Beygelzimer & Langford, 2009; Bottou et al., 2013; Swaminathan & Joachims, 2015a) employ an inverse propensity scoring (IPS) estimator (Rosenbaum & Rubin, 1983) as empirical risk and use stochastic gradient descent (SGD) to optimize the estimate over large datasets. 
ほとんどの方法（Beygelzimer & Langford, 2009; Bottou et al., 2013; Swaminathan & Joachims, 2015a）は、経験的リスクとして逆傾向スコアリング（IPS）推定量（Rosenbaum & Rubin, 1983）を採用し、大規模データセットに対して推定を最適化するために確率的勾配降下法（SGD）を使用します。
Recently, the self-normalized estimator (Trotter & Tukey, 1956) has been shown to be a more suitable estimator for BLBF (Swaminathan & Joachims, 2015c). 
最近、自己正規化推定量（Trotter & Tukey, 1956）がBLBFに対してより適切な推定量であることが示されています（Swaminathan & Joachims, 2015c）。
(IPS推定量よりも、normalized IPS推定量の方が良いよね、みたいな話か!:thinking:)
The self-normalized estimator, however, is not amenable to stochastic optimization and scales poorly with dataset size. 
しかし、自己正規化推定量は確率的最適化に適しておらず、データセットのサイズに対してスケールが悪いです。
In our work, we demonstrate how we can efficiently optimize a reformulation of the self-normalized estimator using SGD.  
私たちの研究では、SGDを使用して自己正規化推定量の再定式化を効率的に最適化する方法を示します。

Previous BLBF methods focus on simple model classes: log-linear and exponential models (Swaminathan & Joachims, 2015a) or tree-based reductions (Beygelzimer & Langford, 2009). 
以前のBLBF方法は、単純なモデルクラスに焦点を当てています：対数線形モデルおよび指数モデル（Swaminathan & Joachims, 2015a）または木ベースの削減（Beygelzimer & Langford, 2009）。
In contrast, we demonstrate how current deep learning models can be trained effectively via batch learning from bandit feedback (BLBF), and compare these with existing approaches on a benchmark dataset (Krizhevsky & Hinton, 2009).  
対照的に、私たちは現在の深層学習モデルがバンディットフィードバック（BLBF）からのバッチ学習を通じて効果的に訓練できる方法を示し、これをベンチマークデータセット（Krizhevsky & Hinton, 2009）上の既存のアプローチと比較します。

Our work, together with independent concurrent work (Serban et al., 2017), demonstrates success with off-policy variants of the REINFORCE (Williams, 1992) algorithm. 
私たちの研究は、独立した同時研究（Serban et al., 2017）とともに、REINFORCE（Williams, 1992）アルゴリズムのオフポリシー変種での成功を示しています。
In particular, our algorithm employs a Lagrangian reformulation of the self-normalized estimator, and the objective and gradients of this reformulation are similar in spirit to the updates of the REINFORCE algorithm. 
特に、私たちのアルゴリズムは自己正規化推定量のラグランジュ再定式化を採用し、この再定式化の目的と勾配はREINFORCEアルゴリズムの更新に似た精神を持っています。
This connection sheds new light on the role of the baseline hyper-parameters in REINFORCE: rather than simply reduce the variance of policy gradients, our work proposes a constructive algorithm for selecting the baseline in the off-policy setting and it suggests that the baseline is instrumental in creating an equivariant counterfactual learning objective.  
この接続は、REINFORCEにおけるベースラインハイパーパラメータの役割に新たな光を当てます：単にポリシー勾配の分散を減少させるのではなく、私たちの研究はオフポリシー設定におけるベースラインを選択するための構成的アルゴリズムを提案し、ベースラインが等変的反事実的学習目的を作成する上で重要であることを示唆しています。

<!-- ここまで読んだ! -->

### 3 BANDITNET: COUNTERFACTUAL RISK MINIMIZATION FOR DEEP NETS  
### 3 BANDITNET: 深層ネットワークのための反事実リスク最小化

To formalize the problem of batch learning from bandit feedback for deep neural networks, consider  
バンディットフィードバックからのバッチ学習の問題を深層ニューラルネットワークに対して形式化するために、次のことを考えます。
the contextual bandit setting where a policy π takes as input x and outputs an action y.  
ポリシーπが入力xを受け取り、アクションyを出力する文脈バンディットの設定です。
In response, we observe the loss (or payoff) δ(x, y) of the selected action y, where δ(x, y) is an arbitrary (unknown) function that maps actions and contexts to a bounded real number. 
その応答として、選択されたアクションyの損失（またはペイオフ）δ(x, y)を観察します。ここで、δ(x, y)はアクションと文脈を有界な実数にマッピングする任意の（未知の）関数です。
アクションと文脈を有界な実数にマッピングする任意の（未知の）関数です。
For example,  in display advertising, the context x could be a representation of the user and page, y denotes the displayed ad, and δ(x, y) could be the monetary payoff from placing the ad (zero if no click, or dollar amount if clicked). 
例えば、ディスプレイ広告では、文脈xはユーザとページの表現であり、yは表示された広告を示し、δ(x, y)は広告を配置した際の金銭的な報酬（クリックがない場合はゼロ、クリックされた場合は金額）である可能性があります。
The contexts are drawn i.i.d. from a fixed but unknown distribution Pr(X).  
文脈は、**固定されているが未知の分布Pr(X)からi.i.d.に**描かれます。

In this paper, a (deep) neural network is viewed as implementing a stochastic policy π. We can think of such a network policy as a conditional distribution πw(Y | x) over actions y ∈ _Y, where w are the parameters of the network. 
本論文では、（深層）ニューラルネットワークは、確率ポリシーπを実装していると見なされます。このようなネットワークポリシーは、アクションy∈_Yにわたる条件付き分布πw(Y | x)として考えることができます。
The network makes a prediction by sampling an action y ∼ _πw(Y | x), where deterministic πw(Y | x) are a special case. As we will show as part of the empirical evaluation, many existing network architectures are compatible with this stochastic-policy view. 
ネットワークは、アクション $y \sim \pi_w(Y | x)$をサンプリングすることで予測を行います。決定論的な $ \pi_w(Y | x)$ は特別な場合です。実証評価の一環として示すように、**多くの既存のネットワークアーキテクチャは、この確率的方策の視点と互換性がある**。(あ、この論文は、特にNNのアーキテクチャの提案ではなく、目的関数とかcontextual banditログでーたを使ったNNの学習方法の提案っぽい...!:thinking:)
For example, any network fw(x, y) with a softmax output layer  
例えば、ソフトマックス出力層を持つ任意のネットワーク $ f_w(x, y)$ 
(ソフトマックス出力層を持つNNも、例えばの話なので、別にどんなNNのアーキテクチャでもいいだ...!:thinking:)

$$
\pi_w(y | x) = \frac{\exp(f_w(x, y))}{\sum_{y' \in Y} \exp(f_w(x, y'))}
$$  

can be re-purposed as a conditional distribution from which one can sample actions, instead of interpreting it as a conditional likelihood like in full-information supervised learning.  
アクションをサンプリングするための条件付き分布として再利用することができます。これは、完全情報教師あり学習のように条件付き尤度として解釈する代わりです。

The goal of learning is to find a policy πw that minimizes the risk (analogously: maximizes the payoff) defined as  
学習の目標は、次のように定義されるリスク（類似的に：ペイオフを最大化する）を最小化するポリシーπwを見つけることです。

$$
R(\pi_w) = \mathbb{E}_{x \sim P_r(X)} \mathbb{E}_{y \sim \pi_w(Y | x)}[\delta(x, y)]
$$  

Any data collected from an interactive system depends on the policy π0 that was running on the  
インタラクティブシステムから収集されたデータは、システム上で実行されていたポリシーπ0に依存し、どのアクションyと損失δ(x, y)が観察されるかを決定します。

system at the time, determining which actions y and losses δ(x, y) are observed. We call π0 the  
このポリシーをログポリシーと呼び、単純のためにそれが定常であると仮定します。

_logging policy, and for simplicity assume that it is stationary. The logged data D are n tuples of  
ログされたデータDは、観察された文脈xi ∼ Pr(X)、アクションyi ∼ _π0(Y | xi)を含むnタプルです。

observed context $x_i \sim P_r(X)$, action $y_i \sim \pi_0(Y | x_i)$ taken by the logging policy, the probability  
ログポリシーによって取られたアクション、確率$ p_i \equiv \pi_0(y_i | x_i)$（これを傾向と呼びます）、および受け取った損失$ \delta_i \equiv \delta(x_i, y_i)$です。

of this action $p_i \equiv \pi_0(y_i | x_i)$, which we call the propensity, and the received loss $ \delta_i \equiv \delta(x_i, y_i)$:  
$$
D = [(x_1, y_1, p_1, \delta_1), \ldots, (x_n, y_n, p_n, \delta_n)].
$$  
We will now discuss how we can use this logged contextual bandit feedback to train a neural network  
これから、ログされた文脈バンディットフィードバックを使用して、リスク$ R(\pi_w)$が低いニューラルネットワークポリシー$ \pi_w(Y | x)$を訓練する方法について説明します。

policy $ \pi_w(Y | x)$ that has low risk $ R(\pi_w)$.  

### 3.1 COUNTERFACTUAL RISK MINIMIZATION  
### 3.1 反事実リスク最小化

While conditional maximum likelihood is a standard approach for training deep neural networks,  
条件付き最大尤度は深層ニューラルネットワークを訓練するための標準的なアプローチですが、

it requires that the loss $ \delta(x_i, y)$ is known for all $ y \in Y$.  
すべての$ y \in Y$に対して損失$ \delta(x_i, y)$が知られている必要があります。

However, we only know $ \delta(x_i, y_i)$ for the particular $ y_i$ chosen by the logging policy $ \pi_0$.  
しかし、ログポリシー$ \pi_0$によって選択された特定の$ y_i$に対してのみ$ \delta(x_i, y_i)$を知っています。

We therefore take a different approach following (Langford et al., 2008; Swaminathan & Joachims, 2015b),  
したがって、（Langford et al., 2008; Swaminathan & Joachims, 2015b）に従って異なるアプローチを取ります。

where we directly minimize an empirical risk that can be estimated from the logged bandit data $ D$.  
ここでは、ログされたバンディットデータ$ D$から推定できる経験リスクを直接最小化します。

This approach is called counterfactual risk minimization (CRM) (Swaminathan & Joachims, 2015b),  
このアプローチは反事実リスク最小化（CRM）と呼ばれ（Swaminathan & Joachims, 2015b）、

since for any policy $ \pi_w$ it addresses the  
任意のポリシー$ \pi_w$に対して、そのポリシーがどのように機能するかという反事実的な質問に対処します。

counterfactual question of how well that policy would have performed, if it had been used instead  
もしそれが$ \pi_0$の代わりに使用されていた場合、そのポリシーがどれだけうまく機能したかという反事実的な質問に対処します。

of $ \pi_0$.  
$ \pi_0$の代わりに。

While minimizing an empirical risk as an estimate of the true risk $ R(\pi_w)$ is a common principle  
経験リスクを真のリスク$ R(\pi_w)$の推定値として最小化することは機械学習における一般的な原則ですが、

in machine learning (Vapnik, 1998), getting a reliable estimate based on the training data $ D$ produced by $ \pi_0$ is not straightforward.  
機械学習（Vapnik, 1998）において、$ \pi_0$によって生成されたトレーニングデータ$ D$に基づいて信頼できる推定値を得ることは簡単ではありません。

The logged bandit data $ D$ is not only incomplete (i.e., we lack knowledge of $ \delta(x_i, y)$ for many $ y \in Y$ that $ \pi_w$ would have chosen differently from $ \pi_0$),  
ログされたバンディットデータ$ D$は不完全であるだけでなく（すなわち、$ \pi_w$が$ \pi_0$とは異なる多くの$ y \in Y$に対して$ \delta(x_i, y)$の知識が欠けています）、

but it is also biased (i.e., the actions preferred by $ \pi_0$ are over-represented).  
また、バイアスもあります（すなわち、$ \pi_0$によって好まれるアクションが過剰に表現されています）。

This is why existing work on training deep neural networks either requires full knowledge of the loss function,  
これが、深層ニューラルネットワークの訓練に関する既存の研究が、損失関数の完全な知識を必要とするか、

or requires the ability to interactively draw new samples $ y_i \sim \pi_w(Y | x_i)$ for any new policy $ \pi_w$.  
または、任意の新しいポリシー$ \pi_w$に対してインタラクティブに新しいサンプル$ y_i \sim \pi_w(Y | x_i)$を引き出す能力を必要とする理由です。

In our setting we can do neither – we have a fixed dataset $ D$ that is limited to samples from $ \pi_0$.  
私たちの設定では、どちらもできません。$ \pi_0$からのサンプルに制限された固定データセット$ D$があります。

To nevertheless get a useful estimate of the empirical risk, we explicitly address both the bias and  
それでも経験リスクの有用な推定値を得るために、バイアスと

the variance of the risk estimate. To correct for sampling bias and handle missing data, we approach  
リスク推定値の分散の両方に明示的に対処します。サンプリングバイアスを修正し、欠損データを処理するために、

the risk estimation problem using importance sampling and thus remove the distribution mismatch  
重要度サンプリングを使用してリスク推定の問題にアプローチし、したがって分布の不一致を取り除きます。

between $ \pi_0$ and $ \pi_w$ (Langford et al., 2008; Owen, 2013; Swaminathan & Joachims, 2015b):  
$ \pi_0$と$ \pi_w$の間の（Langford et al., 2008; Owen, 2013; Swaminathan & Joachims, 2015b）：

$$
R(\pi_w) = \mathbb{E}_{x \sim P_r(X)} \mathbb{E}_{y \sim \pi_0(Y | x)}\left[\frac{\delta(x, y) \pi_w(y | x)}{\pi_0(y | x)}\right].
$$  
The latter expectation can be estimated on a sample $ D$ of $ n$ bandit-feedback examples using the  
後者の期待値は、$ n$のバンディットフィードバック例のサンプル$ D$を使用して推定できます。

following IPS estimator (Langford et al., 2008; Owen, 2013; Swaminathan & Joachims, 2015b):  
次のIPS推定量（Langford et al., 2008; Owen, 2013; Swaminathan & Joachims, 2015b）：

$$
\hat{R}_{IPS}(\pi_w) = \frac{1}{n} \sum_{i=1}^{n} \frac{\delta_i \pi_w(y_i | x_i)}{\pi_0(y_i | x_i)}.
$$  
This IPS estimator is unbiased and has bounded variance, if the logging policy has full support in  
このIPS推定量はバイアスがなく、バウンデッドバリアンスを持ちます。ログポリシーが完全なサポートを持つ場合、

the sense that $ \forall x, y : \pi_0(y | x) \geq \epsilon > 0$.  
すなわち、$ \forall x, y : \pi_0(y | x) \geq \epsilon > 0$です。

While at first glance it may seem natural to directly train the parameters $ w$ of a network to optimize this IPS estimate as an empirical risk, there are at least three obstacles to overcome. 
一見すると、このIPS推定値を経験リスクとして最適化するためにネットワークのパラメータ$w$を直接トレーニングすることが自然に思えるかもしれませんが、少なくとも3つの障害があります。
First, we will argue in the following section that the naive IPS estimator’s lack of equivariance makes it sub-optimal for use as an empirical risk for high-capacity models.
まず、次のセクションで、**単純なIPS推定量の不変性の欠如が、高容量モデル(=パラメータ数が多い??)の経験リスクとして使用するには最適でないこと**を主張します。
Second, we have to find an efficient algorithm for minimizing the empirical risk, especially making it accessible to stochastic gradient descent (SGD) optimization. 
第二に、特に確率的勾配降下法（SGD）最適化にアクセス可能にするための経験リスクを最小化する効率的なアルゴリズムを見つける必要があります。
And, finally, we are faced with an unusual type of bias-variance trade-off since “distance” from the exploration policy impacts the variance of the empirical risk estimate for different $ w$.
最後に、異常なタイプのバイアス-バリアンストレードオフに直面しています。なぜなら、探索ポリシーからの「距離」が異なる$w$に対して経験リスク推定値の分散に影響を与えるからです。

(単純なIPS推定量だと、実用的じゃないよね、という話か!:thinking:)
(じゃあこの論文は、方策勾配のIPS推定量+何かで、よりいい感じにオフライン学習する方法を提案してるのかな...!:thinking:)

<!-- ここまで雑に読んだ! -->

### 3.2 EQUIVARIANT COUNTERFACTUAL RISK MINIMIZATION  
### 3.2 等変反事実リスク最小化

While Eq. (5) provides an unbiased empirical risk estimate, it exhibits the – possibly severe – problem of “propensity overfitting” when directly optimized within a learning algorithm (Swaminathan & Joachims, 2015c). It is a problem of overfitting to the choices $ y_i$ of the logging policy,  and it occurs on top of the normal overfitting to the $ \delta_i$.  
式（5）はバイアスのない経験リスク推定値を提供しますが、学習アルゴリズム内で直接最適化されると「傾向の過剰適合」という可能性のある深刻な問題が発生します（Swaminathan & Joachims, 2015c）。これは、ログポリシーの選択$ y_i$に過適合する問題であり、通常の$ \delta_i$への過適合の上に発生します。
Propensity overfitting is linked to the lack of equivariance of the IPS estimator: 
傾向の過剰適合は、IPS推定量の等変性の欠如に関連しています。
while the minimizer of true risk $ R(\pi_w)$ does not change when translating the loss by a constant (i.e. $\forall x,y: \delta(x, y) + c$) by linearity of expectation, 
**真のリスク$ R(\pi_w)$の最小化は、期待値の線形性により、損失を定数で変換するときと変わりません**（すなわち、$\forall x,y: \delta(x, y) + c$）。

$$
c + \min_{w} \mathbb{E}_{x \sim Pr(X)} \mathbb{E}_{y \sim \pi_w(Y | x)}[\delta(x, y)] = \min_{w} \mathbb{E}_{x \sim Pr(X)} \mathbb{E}_{y \sim \pi_w(Y | x)}[\delta(x, y) + c].
\tag{6}
$$ 

the minimizer of the IPS-estimated empirical risk $ \hat{R}_{IPS}(\pi_w)$ can change dramatically for finite training samples, and  
IPS推定された経験リスク $\hat{R}_{IPS}(\pi_w)$ の最小化は、有限のトレーニングサンプルに対して劇的に変化する可能性があります。

$$
\sum_{i=1}^{n} \frac{(\delta_i + c) \pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} \neq \min_{w} \sum_{i=1}^{n} \frac{\delta_i \pi_w(y_i | x_i)}{\pi_0(y_i | x_i)}.
\tag{7}
$$

Intuitively, when $ c$ shifts losses to be positive numbers, policies $ \pi_w$ that put as little probability mass  as possible on the observed actions have low risk estimates.
直感的には、$ c$が損失を正の数にシフトさせると、観測されたアクションに可能な限り少ない確率質量を置くポリシー$ \pi_w$は低いリスク推定値を持ちます。
If $c$ shifts the losses to the negative range, the exact opposite is the case. 
$c$が損失を負の範囲にシフトさせると、正反対の状況になります。
For either choice of $ c$, the choice of the policy eventually selected by the  learning algorithm can be dominated by where $ \pi_0$ happens to sample data, not by which actions have low loss.  
$c$のどちらかの選択肢に関して、学習アルゴリズムによって選択されるポリシーの選択は、最終的には$\pi_0$がデータをサンプリングする場所によって支配される可能性があります。どのアクションが低い損失を持っているかではありません。

The following self-normalized IPS estimator (SNIPS) addresses the propensity overfitting problem (Swaminathan & Joachims, 2015c) and is equivariant:
次の自己正規化IPS推定量（SNIPS）は、傾向の過剰適合問題（Swaminathan & Joachims, 2015c）に対処し、equivariant(等変)です:

$$
\hat{R}_{SNIPS}(\pi_w) = \frac{1}{n} \sum_{i=1}^{n} \frac{\pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} \delta_i.
\tag{8}
$$  

In addition to being equivariant, this estimate can also have substantially lower variance than Eq. (5), since it exploits the knowledge that the denominator  
等変であるだけでなく、この推定値は、分母が常に期待値1を持つことを利用して、**式（5）よりもかなり低い分散を持つ**ことができます。

$$
S:= \frac{1}{n} \sum_{i=1}^{n} \frac{\pi_w(y_i | x_i)}{\pi_0(y_i | x_i)}
\tag{9}
$$

always has expectation 1:  
常に期待値が1になります：

$$
E[S] = \frac{1}{n} \sum_{i=1}^{n} \inf \frac{\pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} \pi_0(y_i | x_i) Pr(x_i) dy_i dx_i
\\
= \frac{1}{n} \sum_{i=1}^{n} \int 1 Pr(x_i) dx_i = 1.
\tag{10}
$$

The SNIPS estimator uses this knowledge as a multiplicative control variate (Swaminathan & Joachims, 2015c).  
SNIPS推定量は、この知識を乗算制御変数として使用します（Swaminathan & Joachims, 2015c）。
While the SNIPS estimator has some bias, this bias asymptotically vanishes at a rate of $ O(n^{-1})$ (Hesterberg, 1995).  
SNIPS推定量にはいくつかのバイアスがありますが、このバイアスは漸近的に$ O(n^{-1})$の速度で消失します（Hesterberg, 1995）。

Using the SNIPS estimator as our empirical risk implies that we need to solve the following optimization problem for training:  
SNIPS推定量を経験リスクとして使用することは、訓練のために次の最適化問題を解く必要があることを意味します。

$$
\hat{w} = \arg \min_{w \in \mathbb{R}^N} \hat{R}_{SNIPS}(\pi_w).
\tag{11}
$$

Thus, we now turn to designing efficient optimization methods for this training objective.  
したがって、私たちはこの訓練目的のための効率的な最適化手法の設計に移ります。
(この論文では、SNIPS推定量を使って損失関数を推定してるのか...!)

<!-- ここまで読んだ! -->

### 3.3 TRAINING ALGORITHM  
### 3.3 訓練アルゴリズム

Unfortunately, the training objective in Eq. (11) does not permit stochastic gradient descent (SGD) optimization in the given form (see Appendix C), which presents an obstacle to efficient and effective training of the network.
残念ながら、式（11）の訓練目的は、与えられた形式では確率的勾配降下法（SGD）最適化を許可しません（付録Cを参照）、これはネットワークの効率的かつ効果的な訓練に障害をもたらします。
To remedy this problem, we will now develop a reformulation that retains  both the desirable properties of the SNIPS estimator, as well as the ability to reuse established SGD training algorithms.
この問題を解決するために、SNIPS推定量の望ましい特性と確立されたSGDトレーニングアルゴリズムを再利用する能力の両方を保持する再定式化を開発します。
Instead of optimizing a ratio as in Eq. (11), we will reformulate the problem into a series of constrained optimization problems. 
式（11）のように比率を最適化する代わりに、**一連の制約付き最適化問題に再定式化**します。
Let $ \hat{w}$ be a solution of Eq. (11), and at that solution let $ S^*$ be the value of the control variate for $ \pi_{\hat{w}}$ [as defined in Eq. (9). 
$\hat{w}$を式（11）の解とし、その解で$ \pi_{\hat{w}}$の制御変数の値$ S^*$を定義します。
For simplicity, assume that the minimizer $ \hat{w}$ is unique. 
単純のために、最小化器$ \hat{w}$が一意であると仮定します。
If we knew $ S^*$, we could equivalently solve the following constrained  optimization problem:  
$ S^*$を知っていれば、次の制約付き最適化問題を同等に解くことができます：

<!-- 一応ここまで読んだ！よくわからん！ -->

$$
\hat{w} = \arg \min_{w \in \mathbb{R}^N} \sum_{i=1}^{n} \frac{\pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} [= S^*].
$$  
Of course, we do not actually know $ S^*$. However, we can do a grid search in $ \{S_1, \ldots, S_k\}$ for $ S^*$  
もちろん、実際には$ S^*$を知りません。しかし、$ S^*$のために$ \{S_1, \ldots, S_k\}$でグリッドサーチを行うことができます。

and solve the above optimization problem for each value, giving us a set of solutions $ \{\hat{w}^1, \ldots, \hat{w}^k\}$.  
そして、各値に対して上記の最適化問題を解くことで、$ \{\hat{w}^1, \ldots, \hat{w}^k\}$の解のセットを得ます。

Note that $ S$ is just a one-dimensional quantity, and that the sensible range we need to search for  
$ S$は単なる1次元の量であり、探索する必要がある妥当な範囲は

$ S^*$ concentrates around 1 as $ n$ increases (see Appendix B).  
$ S^*$は$n$が増加するにつれて1の周りに集中します（付録Bを参照）。

To find the overall (approximate) $ \hat{w}$ that optimizes the SNIPS estimate, we then simply take the minimum:  
SNIPS推定量を最適化する全体的（近似的）$ \hat{w}$を見つけるために、単に最小値を取ります：

$$
\hat{w} = \arg \min_{j} \left( \hat{w}_j, S_j \right) \sum_{i=1}^{n} \frac{\pi_{\hat{w}_j}(y_i | x_i)}{\pi_0(y_i | x_i)} \delta_i.
$$  
This still leaves the question of how to solve each equality constrained risk minimization problem  
これでも、各等式制約付きリスク最小化問題を解決する方法の問題が残ります。

using SGD. Fortunately, we can perform an equivalent search for $ S^*$ without constrained optimization.  
SGDを使用して。幸いなことに、制約付き最適化なしで$ S^*$の同等の検索を行うことができます。

To this effect, consider the Lagrangian of the constrained optimization problem in Eq. (12)  
この目的のために、式（12）の制約付き最適化問題のラグランジアンを考えます。

with $ S_j$ in the constraint instead of $ S^*$:  
制約の中で$ S^*$の代わりに$ S_j$を使用します：

$$
\sum_{i=1}^{n} \left( \frac{\pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} - S_j \right) = 1.
$$  
The variable $ \lambda$ is an unconstrained Lagrange multiplier. To find the minimum of Eq. (12) for a  
変数$ \lambda$は制約のないラグランジュ乗数です。式（12）の最小値を見つけるために、

particular $ S_j$, we need to minimize $ L(w, \lambda)$ w.r.t. $ w$ and maximize w.r.t. $ \lambda$.  
特定の$ S_j$に対して、$ w$に関して$ L(w, \lambda)$を最小化し、$ \lambda$に関して最大化する必要があります。

$$
\hat{w}_j = \arg \min_{w \in \mathbb{R}^N} L(w, \lambda).
$$  
However, we are not actually interested in the constrained solution of Eq. (12) for any specific $ S_j$.  
しかし、特定の$ S_j$に対する式（12）の制約付き解には実際には興味がありません。

We are merely interested in exploring a certain range $ S \in [S_1, S_k]$ in our search for $ S^*$.  
私たちは単に$ S^*$の探索において、特定の範囲$ S \in [S_1, S_k]$を探索することに興味があります。

So, we can reverse the roles of $ \lambda$ and $ S$, where we keep $ \lambda$ fixed and determine the  
したがって、$ \lambda$と$ S$の役割を逆転させ、$ \lambda$を固定して

corresponding $ S$ in hindsight. In particular, for each $ \{\lambda_1, \ldots, \lambda_k\}$ we solve  
後で対応する$ S$を決定します。特に、各$ \{\lambda_1, \ldots, \lambda_k\}$に対して解決します。

$$
\hat{w}_j = \arg \min_{w \in \mathbb{R}^N} L(w, \lambda_j).
$$  
Note that the solution $ \hat{w}_j$ does not depend on $ S_j$, so we can compute $ S_j$ after we have found the  
解$ \hat{w}_j$は$ S_j$に依存しないため、最小値$ \hat{w}_j$を見つけた後に$ S_j$を計算できます。

minimum $ \hat{w}_j$. In particular, we can determine the $ S_j$ that corresponds to the given $ \lambda_j$ using  
最小値$ \hat{w}_j$を見つけた後に、与えられた$ \lambda_j$に対応する$ S_j$を決定できます。

the necessary optimality conditions,  
必要な最適性条件を使用します。

$$
\frac{\partial L}{\partial w} = 0 \quad \text{and} \quad \frac{\partial L}{\partial \lambda_j} = 0.
$$  
In this way, the sequence of $ \lambda_j$ produces solutions $ \hat{w}_j$ corresponding to a sequence of  
このようにして、$ \lambda_j$の列は、$ S_j$の列に対応する解$ \hat{w}_j$を生成します。

$ \{S_1, \ldots, S_k\}$.  
$ \{S_1, \ldots, S_k\}$。

To identify the sensible range of $ S$ to explore, we can make use of the fact that Eq. (9) concentrates  
探索する妥当な範囲の$ S$を特定するために、式（9）が集中する事実を利用できます。

around its expectation of 1 for each $ \pi_w$ as $ n$ increases. Theorem 2 in Appendix B provides a  
各$ \pi_w$に対して$n$が増加するにつれて1の期待値の周りに集中します。付録Bの定理2は、

characterization of how large the range needs to be. Furthermore, we can steer the exploration  
範囲がどれだけ大きくなる必要があるかを特定します。さらに、探索を

of $ S$ via $ \lambda$, since the resulting $ S$ changes monotonically with $ \lambda$:  
$ \lambda$を介して$ S$を制御できます。なぜなら、結果として得られる$ S$は$ \lambda$に対して単調に変化するからです：

$$
(\lambda_a < \lambda_b) \quad \text{and} \quad (\hat{w}_a \neq \hat{w}_b \text{ are not equivalent optima in Eq. (15)}) \Rightarrow (S_a < S_b).
$$  
A more formal statement and proof are given as Theorem 1 in Appendix A. In the simplest form one  
より正式な声明と証明は付録Aに記載されています。最も単純な形では、

could therefore perform a grid search on $ \lambda$, but more sophisticated search methods are possible too.  
したがって、$ \lambda$でグリッドサーチを実行できますが、より洗練された検索方法も可能です。

After this reformulation, the key computational problem is finding the solution of Eq. (15) for each  
この再定式化の後、重要な計算問題は、各$ \lambda_j$に対して式（15）の解を見つけることです。

$ \lambda_j$. Note that in this unconstrained optimization problem, the Lagrange multiplier effectively trans-  
$ \lambda_j$。この制約のない最適化問題では、ラグランジュ乗数が効果的に損失値を変換します。

lates the loss values in the conventional IPS estimate:  
従来のIPS推定量における損失値を変換します：

$$
\hat{w}_j = \arg \min_{w} \sum_{i=1}^{n} \frac{\delta_i - \lambda_j}{\pi_0(y_i | x_i)} \pi_w(y_i | x_i) = \arg \min_{w} \hat{R}_{IPS}(\lambda_j, \pi_w).
$$  
We denote this $ \lambda$-translated IPS estimate with $ \hat{R}_{IPS}(\lambda, \pi_w)$. Note that each such optimization problem  
この$ \lambda$変換されたIPS推定量を$ \hat{R}_{IPS}(\lambda, \pi_w)$と呼びます。このような最適化問題はすべて、

is now in the form required for SGD, where we merely weight the derivative of the stochastic policy  
SGDに必要な形になり、確率的ポリシーの導関数に重みを付けるだけです。

network $ \pi_w(y | x)$ by a factor $ \frac{\delta_i - \lambda_j}{\pi_0(y_i | x_i)}$. This opens the door for re-purposing existing  
ネットワーク$ \pi_w(y | x)$に因子$ \frac{\delta_i - \lambda_j}{\pi_0(y_i | x_i)}$を掛けます。これにより、既存の

fast methods for training deep neural networks, and we demonstrate experimentally that SGD with  
深層ニューラルネットワークの訓練のための迅速な手法を再利用することができます。実験的に、SGDが

momentum is able to optimize our objective scalably.  
モーメンタムを使用して、私たちの目的をスケーラブルに最適化できることを示します。

Similar loss translations have previously been used in on-policy reinforcement learning (Williams,  
類似の損失変換は、以前にオンポリシー強化学習（Williams、

1992), where they are motivated as minimizing the variance of the gradient estimate (Weaver &  
1992）で使用されており、勾配推定の分散を最小化することを目的としています（Weaver &

Tao, 2001; Greensmith et al., 2004). However, the situation is different in the off-policy setting we  
Tao, 2001; Greensmith et al., 2004）。しかし、私たちが考慮するオフポリシー設定では状況が異なります。

consider. First, we cannot sample new roll-outs from the current policy under consideration, which  
まず、考慮中の現在のポリシーから新しいロールアウトをサンプリングすることはできません。これは、

means we cannot use the standard variance-optimal estimator used in REINFORCE. Second, we  
標準的な分散最適推定量をREINFORCEで使用できないことを意味します。第二に、

tried using the (estimated) expected loss of the learned policy as the baseline as is commonly done  
学習したポリシーの（推定された）期待損失をベースラインとして使用しようとしましたが、一般的に行われているように

in REINFORCE, but will see in the experiment section that this value for $ \lambda$ is far from optimal.  
REINFORCEで行われますが、実験セクションでこの$ \lambda$の値が最適から遠いことがわかります。

Finally, it is unclear whether gradient variance, as opposed to variance of the ERM objective, is  
最後に、勾配の分散がERM目的の分散とは異なるかどうかは不明です。

really the key issue in batch learning from bandit feedback. In this sense, our approach provides  
本当にバンディットフィードバックからのバッチ学習における重要な問題です。この意味で、私たちのアプローチは

a rigorous justification and a constructive way of picking the value of $ \lambda$ in the off-policy setting –  
厳密な正当化とオフポリシー設定における$ \lambda$の値を選択するための建設的な方法を提供します。

namely the value for which the corresponding $ S_j$ minimizes Eq. (13). In addition, one can further  
すなわち、対応する$ S_j$が式（13）を最小化する値です。さらに、

add variance regularization (Swaminathan & Joachims, 2015b) to improve the robustness of the risk  
分散正則化（Swaminathan & Joachims, 2015b）を追加してリスクの堅牢性を向上させることができます。

estimate in Eq. (18) (see Appendix D for details).  
式（18）の推定値（詳細は付録Dを参照）。



### 4 EMPIRICAL EVALUATION 実証評価

The empirical evaluation is designed to address three key questions.  
実証評価は、3つの重要な質問に対処するように設計されています。

First, it verifies that deep models can indeed be trained effectively using our approach.  
まず、私たちのアプローチを使用して深層モデルが実際に効果的に訓練できることを確認します。

Second, we will compare how the same deep neural network architecture performs under different types of data and training objectives – in particular, conventional cross-entropy training using full-information data.  
次に、同じ深層ニューラルネットワークアーキテクチャが異なる種類のデータと訓練目的の下でどのように機能するかを比較します。特に、完全情報データを使用した従来のクロスエントロピー訓練についてです。

In order to be able to do this comparison, we focus on synthetic contextual bandit feedback data for training BanditNet that is sampled from the full-information labels.  
この比較を行うために、完全情報ラベルからサンプリングされたBanditNetの訓練用の合成コンテキストバンディットフィードバックデータに焦点を当てます。

Third, we explore the effectiveness and fidelity of the approximate SNIPS objective.  
第三に、近似SNIPS目的の効果と忠実度を探ります。

For the following BanditNet experiments, we adapted the ResNet20 architecture (He et al., 2016) by replacing the conventional cross-entropy objective with our counterfactual risk minimization objective.  
以下のBanditNet実験では、従来のクロスエントロピー目的を私たちの反事実リスク最小化目的に置き換えることで、ResNet20アーキテクチャ（He et al., 2016）を適応させました。

We evaluate the performance of this Bandit-ResNet on the CIFAR-10 (Krizhevsky & Hinton, 2009) dataset, where we can compare training on full-information data with training on bandit feedback, and where there is a full-information test set for estimating prediction error.  
CIFAR-10（Krizhevsky & Hinton, 2009）データセットでこのBandit-ResNetの性能を評価します。ここでは、完全情報データでの訓練とバンディットフィードバックでの訓練を比較でき、予測誤差を推定するための完全情報テストセットがあります。

To simulate logged bandit feedback, we perform the standard supervised to bandit conversion (Beygelzimer & Langford, 2009).  
ログされたバンディットフィードバックをシミュレートするために、標準的な監視からバンディットへの変換を行います（Beygelzimer & Langford, 2009）。

We use a hand-coded logging policy that achieves about 49% error rate on the training data, which is substantially worse than what we hope to achieve after learning.  
トレーニングデータで約49%の誤差率を達成する手動コーディングされたロギングポリシーを使用します。これは、学習後に達成したいと考えているものよりも大幅に悪いものです。

This emulates a real world scenario where one would bootstrap an operational system with a mediocre policy (e.g., derived from a small hand-labeled dataset) and then deploys it to log bandit feedback.  
これは、実際のシナリオを模倣しており、平凡なポリシー（例えば、小さな手動ラベルデータセットから派生したもの）で運用システムをブートストラップし、その後バンディットフィードバックをログするために展開します。

This logged bandit feedback data is then used to train the Bandit-ResNet.  
このログされたバンディットフィードバックデータは、その後Bandit-ResNetの訓練に使用されます。

We evaluate the trained model using error rate on the held out (full-information) test set.  
訓練されたモデルの評価は、保持された（完全情報）テストセットの誤差率を使用して行います。

We compare this model against the skyline of training a conventional ResNet using the full-information feedback.  
このモデルを、完全情報フィードバックを使用して従来のResNetを訓練した際のスカイラインと比較します。

Error Rate (test)  
誤差率（テスト）

Lagrange Multiplier (lambda)  
ラグランジュ乗数（λ）

Figure 2: The x-axis shows the value of the Lagrange multiplier λ used for training.  
図2：x軸は訓練に使用されるラグランジュ乗数λの値を示しています。

Left plot shows the test error.  
左のプロットはテスト誤差を示しています。

Right plot shows the value of the SNIPS objective and the normalizer S.  
右のプロットはSNIPS目的の値と正規化因子Sを示しています。

The size of the training set is 50k bandit-feedback examples.  
訓練セットのサイズは50,000のバンディットフィードバック例です。

from the 50,000 training examples.  
50,000の訓練例から。

Both the conventional full-information ResNet as well as the Bandit-ResNet use the same network architecture, the same hyperparameters, the same data augmentation scheme, and the same optimization method that were set in the CNTK implementation of ResNet20.  
従来の完全情報ResNetとBandit-ResNetの両方は、同じネットワークアーキテクチャ、同じハイパーパラメータ、同じデータ拡張スキーム、およびResNet20のCNTK実装で設定された同じ最適化手法を使用します。

Since CIFAR10 does not come with a validation set for tuning the variance-regularization constant γ, we do not use variance regularization for Bandit-ResNet.  
CIFAR10には分散正則化定数γを調整するための検証セットがないため、Bandit-ResNetには分散正則化を使用しません。

The Lagrange multiplier _λ_ 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05 is selected on the training set via Eq. (13).  
ラグランジュ乗数_λ_ 0.65、0.7、0.75、0.8、0.85、0.9、0.95、1.0、1.05は、式（13）を介して訓練セットで選択されます。

The _∈{_ _}_ only parameter we adjusted for Bandit-ResNet is lowering the learning rate to 0.1 and slowing down the learning rate schedule.  
Bandit-ResNetのために調整した唯一のパラメータは、学習率を0.1に下げ、学習率スケジュールを遅くすることです。

The latter was done to avoid confounding the Bandit-ResNet results with potential effects from early stopping, and we report test performance after 1000 training epochs, which is well beyond the point of convergence in all runs.  
後者は、早期停止からの潜在的な影響でBandit-ResNetの結果が混乱しないように行われ、すべての実行で収束点を大きく超えた1000エポックの訓練後のテスト性能を報告します。

**Learning curve.** Figure 1 shows the prediction error of the Bandit-ResNet as more and more bandit feedback is provided for training.  
**学習曲線。** 図1は、より多くのバンディットフィードバックが訓練のために提供されるにつれて、Bandit-ResNetの予測誤差を示しています。

First, even though the logging policy that generated the bandit feedback has an error rate of 49%, the prediction error of the policy learned by the Bandit-ResNet is substantially better.  
まず、バンディットフィードバックを生成したロギングポリシーの誤差率が49%であるにもかかわらず、Bandit-ResNetによって学習されたポリシーの予測誤差は大幅に改善されています。

It is between 13% and 8.2%, depending on the amount of training data.  
これは、訓練データの量に応じて13%から8.2%の間です。

Second, the horizontal line is the performance of a conventional ResNet trained on the full-information training set.  
次に、水平線は完全情報訓練セットで訓練された従来のResNetの性能です。

It serves as a skyline of how good Bandit-ResNet could possibly get given that it is sampling bandit feedback from the same full-information training set.  
これは、Bandit-ResNetが同じ完全情報訓練セットからバンディットフィードバックをサンプリングしていることを考慮した場合、どれだけ良くなる可能性があるかのスカイラインとして機能します。

The learning curve in Figure 1 shows that Bandit-ResNet converges to the skyline performance given enough bandit feedback training data, providing strong evidence that our training objective and method can effectively extract the available information provided in the bandit feedback.  
図1の学習曲線は、Bandit-ResNetが十分なバンディットフィードバック訓練データを与えられた場合にスカイライン性能に収束することを示しており、私たちの訓練目的と方法がバンディットフィードバックで提供される利用可能な情報を効果的に抽出できることの強い証拠を提供します。

**Effect of the choice of Lagrange multiplier.** The left-hand plot in Figure 2 shows the test error of solutions ˆwj depending on the value of the Lagrange multiplier λj used during training.  
**ラグランジュ乗数の選択の影響。** 図2の左側のプロットは、訓練中に使用されるラグランジュ乗数λjの値に応じた解のテスト誤差を示しています。

It shows that λ in the range 0.8 to 1.0 results in good prediction performance, but that performance degrades outside this area.  
λが0.8から1.0の範囲にあるとき、良好な予測性能をもたらしますが、この範囲外では性能が低下します。

The SNIPS estimates in the right-hand plot of Figure 2 roughly reflects this optimal range, given empirical support for both the SNIPS estimator and the use of Eq. (13).  
図2の右側のプロットにおけるSNIPS推定値は、SNIPS推定器と式（13）の使用の両方に対する実証的な支持を考慮すると、この最適範囲を大まかに反映しています。

We also explored two other methods for selecting λ.  
また、λを選択するための他の2つの方法も探りました。

First, we used the straightforward IPS estimator as the objective (i.e., λ = 0), which leads to prediction performance worse than that of the logging policy (not shown).  
まず、単純なIPS推定器を目的として使用しました（すなわち、λ = 0）。これは、ロギングポリシーよりも悪い予測性能をもたらします（表示されていません）。

Second, we tried using the (estimated) expected loss of the learned policy as the baseline as is commonly done in REINFORCE.  
次に、REINFORCEで一般的に行われるように、学習したポリシーの（推定された）期待損失をベースラインとして使用することを試みました。

As Figure 1 shows, it is between 0.130 and 0.083 for the best policies we found.  
図1が示すように、私たちが見つけた最良のポリシーに対しては0.130から0.083の間です。

Figure 2 (left) shows that these baseline values are well outside of the optimum range.  
図2（左）は、これらのベースライン値が最適範囲の外にあることを示しています。

Also shown in the right-hand plot of Figure 2 is the value of the control variate in the denominator of the SNIPS estimate.  
図2の右側のプロットには、SNIPS推定の分母における制御変数の値も示されています。

As expected, it increases from below 1 to above 1 as λ is increased.  
予想通り、λが増加するにつれて1未満から1を超えるまで増加します。

Note that large deviations of the control variate from 1 are a sign of propensity overfitting (Swaminathan & Joachims, 2015c).  
制御変数が1から大きく逸脱することは、傾向の過剰適合の兆候であることに注意してください（Swaminathan & Joachims, 2015c）。

In particular, for all solutions ˆwj the estimated standard error of the control variate Sj was less than 0.013, meaning that the normal 95% confidence interval for each Sj is contained in [0.974, 1.026].  
特に、すべての解ˆwjに対して、制御変数Sjの推定標準誤差は0.013未満であり、各Sjの通常の95%信頼区間は[0.974, 1.026]に含まれます。

If we see a ˆwj with control variate Sj outside this range, we should be suspicious of propensity overfitting to the choices of the logging policy and discard this solution.  
この範囲外に制御変数Sjを持つˆwjを見た場合、ロギングポリシーの選択に対する傾向の過剰適合を疑い、この解を破棄すべきです。



### 5 CONCLUSIONS AND FUTURE WORK 結論と今後の研究

We proposed a new output layer for deep neural networks that enables the use of logged contextual bandit feedback for training.  
私たちは、トレーニングのためにログされたコンテキストバンディットフィードバックを使用できる新しい出力層を深層ニューラルネットワークのために提案しました。  
This type of feedback is abundant and ubiquitous in the form of interaction logs from autonomous systems, opening up the possibility of training deep neural networks on unprecedented amounts of data.  
この種のフィードバックは、自律システムからのインタラクションログの形で豊富かつ普遍的であり、前例のない量のデータで深層ニューラルネットワークをトレーニングする可能性を開きます。  
In principle, this new output layer can replace the conventional cross-entropy layer for any network architecture.  
原則として、この新しい出力層は、任意のネットワークアーキテクチャに対して従来のクロスエントロピー層を置き換えることができます。  
We provide a rigorous derivation of the training objective, linking it to an equivariant counterfactual risk estimator that enables counterfactual risk minimization.  
私たちは、トレーニング目的の厳密な導出を提供し、それを反事実リスク最小化を可能にする同変反事実リスク推定器に結びつけます。  
Most importantly, we show how the resulting training objective can be decomposed and reformulated to make it feasible for SGD training.  
最も重要なことは、得られたトレーニング目的がどのように分解され、再定式化されてSGDトレーニングに適用可能になるかを示すことです。  
We find that the BanditNet approach applied to the ResNet architecture achieves predictive accuracy comparable to conventional full-information training for visual object recognition.  
私たちは、ResNetアーキテクチャに適用されたBanditNetアプローチが、視覚的オブジェクト認識のための従来のフルインフォメーショントレーニングと同等の予測精度を達成することを発見しました。  

The paper opens up several directions for future work.  
この論文は、今後の研究のいくつかの方向性を開きます。  
First, it enables many new applications where contextual bandit feedback is readily available.  
第一に、コンテキストバンディットフィードバックが容易に利用できる多くの新しいアプリケーションを可能にします。  
Second, in settings where it is infeasible to log propensity-scored data, it would be interesting to combine BanditNet with propensity estimation techniques.  
第二に、傾向スコアデータをログすることが不可能な設定では、BanditNetと傾向推定技術を組み合わせることが興味深いでしょう。  
Third, there may be improvements to BanditNet, like smarter search techniques for S, more efficient counterfactual estimators beyond SNIPS, and the ability to handle continuous outputs.  
第三に、Sのためのよりスマートな探索技術、SNIPSを超えたより効率的な反事実推定器、連続出力を処理する能力など、BanditNetの改善があるかもしれません。  

ACKNOWLEDGMENTS  
謝辞  

This research was supported in part by NSF Award IIS-1615706, a gift from Bloomberg, the Criteo Faculty Research Award program, and the Netherlands Organisation for Scientific Research (NWO) under project nr. 612.001.116.  
この研究は、NSF賞IIS-1615706、Bloombergからの寄付、Criteo教員研究賞プログラム、およびオランダ科学研究機関（NWO）のプロジェクト番号612.001.116の下で部分的に支援されました。  
All content represents the opinion of the authors, which is not necessarily shared or endorsed by their respective employers and/or sponsors.  
すべての内容は著者の意見を表しており、必ずしもそれぞれの雇用主やスポンサーによって共有または支持されるものではありません。  



### REFERENCES 参考文献

A. Agarwal, D. Hsu, S. Kale, J. Langford, Lihong Li, and R. Schapire. Taming the monster: A fast and simple algorithm for contextual bandits. In ICML, 2014.  
A. Agarwal, D. Hsu, S. Kale, J. Langford, Lihong Li、およびR. Schapire. モンスターを手なずける：コンテキストバンディットのための高速かつシンプルなアルゴリズム。ICMLにおいて、2014年。

A. Beygelzimer and J. Langford. The offset tree for learning with partial labels. In KDD, pp. 129–138, 2009.  
A. BeygelzimerとJ. Langford. 部分ラベルを用いた学習のためのオフセットツリー。KDDにおいて、pp. 129–138、2009年。

L. Bottou, J. Peters, J. Quinonero-Candela, D. Charles, M. Chickering, E. Portugaly, D. Ray, P. Simard, and E. Snelson. Counterfactual reasoning and learning systems: The example of computational advertising. JMLR, 14:3207–3260, 2013.  
L. Bottou, J. Peters, J. Quinonero-Candela, D. Charles, M. Chickering, E. Portugaly, D. Ray, P. Simard、およびE. Snelson. 反事実的推論と学習システム：計算広告の例。JMLR, 14:3207–3260, 2013年。

M. Dehghani, H. Zamani, A. Severyn, J. Kamps, and W. B. Croft. Neural ranking models with weak supervision. In SIGIR, pp. 65–74, 2017.  
M. Dehghani, H. Zamani, A. Severyn, J. Kamps、およびW. B. Croft. 弱い監視によるニューラルランキングモデル。SIGIRにおいて、pp. 65–74、2017年。

E. Greensmith, P.L. Bartlett, and J. Baxter. Variance reduction techniques for gradient estimates in reinforcement learning. JMLR, 5:1471–1530, 2004.  
E. Greensmith, P.L. Bartlett、およびJ. Baxter. 強化学習における勾配推定のための分散削減技術。JMLR, 5:1471–1530、2004年。

K. He, X. Zhang, S. Ren, and J. Sun. Deep residual learning for image recognition. In CVPR, 2016.  
K. He, X. Zhang, S. Ren、およびJ. Sun. 画像認識のための深層残差学習。CVPRにおいて、2016年。

T. Hesterberg. Weighted average importance sampling and defensive mixture distributions. Techno_metrics, 37:185–194, 1995.  
T. Hesterberg. 重み付き平均重要度サンプリングと防御的混合分布。Techno_metrics, 37:185–194、1995年。

A. Joulin, L. van der Maaten, A. Jabri, and N. Vasilache. Learning visual features from large weakly supervised data. In ECCV, pp. 67–84, 2016.  
A. Joulin, L. van der Maaten, A. Jabri、およびN. Vasilache. 大規模な弱い監視データからの視覚特徴の学習。ECCVにおいて、pp. 67–84、2016年。

A. Krizhevsky and G. Hinton. Learning multiple layers of features from tiny images. Technical report, Computer Science Department, University of Toronto, 2009.  
A. KrizhevskyとG. Hinton. 小さな画像からの複数の特徴層の学習。技術報告、トロント大学コンピュータサイエンス学科、2009年。

J. Langford, A. Strehl, and J. Wortman. Exploration scavenging. In ICML, pp. 528–535, 2008.  
J. Langford, A. Strehl、およびJ. Wortman. 探索スカベンジング。ICMLにおいて、pp. 528–535、2008年。

A.B. Owen. Monte Carlo theory, methods and examples. 2013.  
A.B. Owen. モンテカルロ理論、方法、および例。2013年。

P. Rosenbaum and D. Rubin. The central role of propensity score in observational studies for causal effects. Biometrica, 70:41–55, 1983.  
P. RosenbaumとD. Rubin. 因果効果のための観察研究における傾向スコアの中心的役割。Biometrica, 70:41–55、1983年。

I. Serban, C. Sankar, M. Germain, S. Zhang, Z. Lin, S. Subramanian, T. Kim, M. Pieper, S. Chandar, N. R. Ke, S. Mudumba, A. de Brebisson, J. M. R. Sotelo, D. Suhubdy, V. Michalski, A. Nguyen, J. Pineau, and Y. Bengio. A deep reinforcement learning chatbot. ArXiv e-prints, September 2017.  
I. Serban, C. Sankar, M. Germain, S. Zhang, Z. Lin, S. Subramanian, T. Kim, M. Pieper, S. Chandar, N. R. Ke, S. Mudumba, A. de Brebisson, J. M. R. Sotelo, D. Suhubdy, V. Michalski, A. Nguyen, J. Pineau、およびY. Bengio. 深層強化学習チャットボット。ArXiv e-prints、2017年9月。

A. Swaminathan and T. Joachims. Counterfactual risk minimization: Learning from logged bandit feedback. In ICML, pp. 814–823, 2015a.  
A. SwaminathanとT. Joachims. 反事実リスク最小化：ログされたバンディットフィードバックからの学習。ICMLにおいて、pp. 814–823、2015年。

A. Swaminathan and T. Joachims. Batch learning from logged bandit feedback through counterfactual risk minimization. JMLR, 16:1731–1755, 2015b.  
A. SwaminathanとT. Joachims. 反事実リスク最小化を通じたログされたバンディットフィードバックからのバッチ学習。JMLR, 16:1731–1755、2015年。

A. Swaminathan and T. Joachims. The self-normalized estimator for counterfactual learning. In NIPS, 2015c.  
A. SwaminathanとT. Joachims. 反事実学習のための自己正規化推定量。NIPSにおいて、2015年。

H. F. Trotter and J. W. Tukey. Conditional monte carlo for normal samples. In Symposium on Monte Carlo Methods, pp. 64–79, 1956.  
H. F. TrotterとJ. W. Tukey. 正規サンプルのための条件付きモンテカルロ。モンテカルロ法に関するシンポジウムにおいて、pp. 64–79、1956年。

V. Vapnik. Statistical Learning Theory. Wiley, Chichester, GB, 1998.  
V. Vapnik. 統計的学習理論。Wiley, チチェスター, GB, 1998年。

L. Weaver and N. Tao. The optimal reward baseline for gradient-based reinforcement learning. In UAI, pp. 538–545, 2001.  
L. WeaverとN. Tao. 勾配ベースの強化学習のための最適報酬ベースライン。UAIにおいて、pp. 538–545、2001年。

R. Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine Learning, 8(3-4), May 1992.  
R. Williams. コネクショニスト強化学習のためのシンプルな統計的勾配追従アルゴリズム。Machine Learning, 8(3-4)、1992年5月。

C. Zhang, S. Bengio, M. Hardt, B. Recht, and O. Vinyals. Understanding deep learning requires rethinking generalization. CoRR, abs/1611.03530, 2016.  
C. Zhang, S. Bengio, M. Hardt, B. Recht、およびO. Vinyals. 深層学習を理解するには一般化の再考が必要である。CoRR, abs/1611.03530、2016年。



### A APPENDIX: STEERING THE EXPLORATION OF S THROUGH λ.  
### A付録: λを通じたSの探索の誘導

**Theorem 1. Let λa < λb and let**  
**定理1. λa < λbとし、次を定義する。**  
_wˆa_ = arg min _RˆIPS[λ][a]_ [(][π][w][)] (19)  
_wˆa_ = arg min _RˆIPS[λ][a]_ [(][π][w][)] (19)  

_w_  
_wˆb_ = arg min _RˆIPS[λ][b]_ [(][π][w][)][.] (20)  
_wˆb_ = arg min _RˆIPS[λ][b]_ [(][π][w][)][.] (20)  

_If the optima ˆwa and ˆwb are not equivalent in the sense that_  
_もし最適解ˆwaとˆwbが次の意味で同等でないなら、_  
_R[ˆ]IPS[λ][a]_ [(][π][ ˆ]wa [)][ ̸][=] _RˆIPS[λ][a]_ [(][π][ ˆ]wb [)][ and]  
_R[ˆ]IPS[λ][a]_ [(][π][ ˆ]wa [)][ ̸][=] _RˆIPS[λ][a]_ [(][π][ ˆ]wb [)][および]  
_RˆIPS[λ][b]_ [(][π][ ˆ]wa [)][ ̸][= ˆ][R]IPS[λ][b] [(][π][ ˆ]wb [)][, then]  
_RˆIPS[λ][b]_ [(][π][ ˆ]wa [)][ ̸][= ˆ][R]IPS[λ][b] [(][π][ ˆ]wb [)][なら、  
_Sa < Sb._ (21)  
_Sa < Sb._ (21)  

_Proof. Abbreviate f_ (w) = _n[1]_ �ni=1 _[δ][i]_ _ππw0((yyii||xxii))_ [and][ g][(][w][) =][ 1]n �ni=1 _ππw0((yyii||xxii))_ [. Then]  
_証明。f(w)を_n[1]_ �ni=1 _[δ][i]_ _ππw0((yyii||xxii))_とし、g(w)を1/n �ni=1 _ππw0((yyii||xxii))_とする。次に、  
_RˆIPS[λ]_ [(][π][w][) =][ f] [(][w][)][ −] _[λg][(][w][)][,]_ (22)  
_RˆIPS[λ]_ [(][π][w][) =][ f] [(][w][)][ −] _[λg][(][w][)][, (22)  

where g(w) corresponds to the value of the control variate S.  
ここで、g(w)は制御変数Sの値に対応する。  
Since ˆwa and ˆwb are not equivalent optima, we know that  
ˆwaとˆwbが同等の最適解でないため、次が成り立つ。  
_f_ ( ˆwa) − _λa g( ˆwa)_ _<_ _f_ ( ˆwb) − _λa g( ˆwb)_ (23)  
_f_ ( ˆwa) − _λa g( ˆwa)_ _<_ _f_ ( ˆwb) − _λa g( ˆwb)_ (23)  

_f_ ( ˆwb) − _λb g( ˆwb)_ _<_ _f_ ( ˆwa) − _λb g( ˆwa)_ (24)  
_f_ ( ˆwb) − _λb g( ˆwb)_ _<_ _f_ ( ˆwa) − _λb g( ˆwa)_ (24)  

Adding the two inequalities and solving implies that  
2つの不等式を加え、解くと次が成り立つ。  
_⇒_ _f_ ( ˆwa) − _λa g( ˆwa) + f_ ( ˆwb) − _λb g( ˆwb) < f_ ( ˆwb) − _λa g( ˆwb) + f_ ( ˆwa) − _λb g( ˆwa) (25)_  
_⇒_ _f_ ( ˆwa) − _λa g( ˆwa) + f_ ( ˆwb) − _λb g( ˆwb) < f_ ( ˆwb) − _λa g( ˆwb) + f_ ( ˆwa) − _λb g( ˆwa) (25)_  

_⇔_ _λa g( ˆwa) + λb g( ˆwb) > λa g( ˆwb) + λb g( ˆwa)_ (26)  
_⇔_ _λa g( ˆwa) + λb g( ˆwb) > λa g( ˆwb) + λb g( ˆwa)_ (26)  

_⇔_ (λb − _λa) g( ˆwb) > (λb −_ _λa) g( ˆwa)_ (27)  
_⇔_ (λb − _λa) g( ˆwb) > (λb −_ _λa) g( ˆwa)_ (27)  

_⇔_ _g( ˆwb) > g( ˆwa)_ (28)  
_⇔_ _g( ˆwb) > g( ˆwa)_ (28)  

_⇔_ _Sb > Sa_ (29)  
_⇔_ _Sb > Sa_ (29)  



### B APPENDIX: CHARACTERIZING THE RANGE OF S TO EXPLORE.  
### B 付録: 探索するSの範囲の特性

**Theorem 2. Let p ≤** _π0(y | x) be a lower bound on the propensity for the logging policy, then_  
**定理2. p ≤** _π0(y | x)をロギングポリシーの傾向の下限とすると、_

_constraining the solution of Eq. (11) to the w with control variate S_ [1 _ϵ, 1 + ϵ] for a training_  
_式(11)の解を制約し、制御変数Sを[1 _ϵ, 1 + ϵ]に設定すると、_

_∈_ _−_  
_set of size n will not exclude the minimizer of the true risk w[∗]_ = arg minw∈W R(πw) in the policy  
_サイズnの集合は、ポリシー空間Wにおける真のリスクの最小化者w[∗]_ = arg minw∈W R(πw)を除外しない。_

_space W with probability at least_  
_確率少なくとも_

1 2 exp � 2nϵ[2]p[2][�] _._ (30)  
1/2 exp(−2nϵ^2/p^2) _._ (30)

_Proof. For the optimal w[∗], let_  
_証明. 最適なw[∗]について、_

_πw∗_ (yi | xi) (31)  
_πw∗_ (yi | xi) (31)

_π0(yi | xi)_  
_π0(yi | xi)_

_S_ =  
_S_ =

_n_  
_n_

_�  
_i=1_  
_Σ_{i=1}^{n}_

_be the control variate in the denominator of the SNIPS estimator. S is a random variable that is a  
_これはSNIPS推定量の分母における制御変数です。Sは、_

sum of bounded random variables between 0 and  
0と

_πw∗_ (y | x)  
_πw∗_ (y | x)

max (32)  
最大値 (32)

_x,y_ _π0(y | x)_ _[≤]_ _p[1]_ _[.]_  
_x,y_ _π0(y | x)_ _[≤]_ _p[1]_ _[.]_

We can bound the probability that the control variate S of the optimum w[∗] lies outside of [1 _ϵ, 1+ϵ]_  
最適なw[∗]の制御変数Sが[1 _ϵ, 1 + ϵ]の外にある確率を制約できます。

_−_  
_−_

via Hoeffding’s inequality:  
Hoeffdingの不等式を用いて:

� 2n2ϵ2  
$$
P(S ≤ 1 - ϵ) ≤ 2 exp \left(-\frac{n(1/p)^2}{2ϵ^2}\right)
$$

_−_  
_−_

_P_ ( _S_ 1 _ϵ)_ 2 exp  
$$
P(S \leq 1 - ϵ) \leq 2 \exp \left(-\frac{n(1/p)^2}{2ϵ^2}\right)
$$

_|_ _−_ _| ≥_ _≤_  
_−_ _−_

_n(1/p)[2]_  
_n(1/p)[2]_

_�  
(33)  
(33)

= 2 exp � 2nϵ[2]p[2][�] _._ (34)  
= 2 exp(−2nϵ^2/p^2) _._ (34)

_−_  
_−_

The same argument applies to any individual policy πw, not just w[∗]. Note, however, that it can still  
同様の議論は、w[∗]だけでなく、任意の個別ポリシーπwにも適用されます。ただし、注意が必要です。

be highly likely that at least one policy πw with w ∈ _W shows a large deviation in the control variate_  
w ∈ _W_ の少なくとも1つのポリシーπwが制御変数で大きな偏差を示す可能性が高いことがあります。

for high-capacity W, which can lead to propensity overfitting when using the naive IPS estimator.  
高容量のWの場合、ナイーブIPS推定量を使用すると、傾向の過剰適合につながる可能性があります。



### C APPENDIX: WHY DIRECT STOCHASTIC OPTIMIZATION OF RATIO ESTIMATORS IS NOT POSSIBLE.  
### C付録: 比率推定量の直接確率的最適化が不可能な理由

Suppose we have a dataset of n BLBF samples D = {(x1, y1, δ1, p1) . . . (xn, yn, δn, pn)} where
各インスタンスはデータ生成分布からのi.i.d.サンプルです。次に、n + 1サンプルの2つのデータセットD[′] = D (x[′], y[′], δ[′], p[′])とD[′′] = D (x[′′], y[′′], δ[′′], p[′′])を考えます。

_∪{_ _}_ _∪{_ _}_
ここで、(x[′], y[′], δ[′], p[′]) = (x[′′], y[′′], δ[′′], p[′′])であり、(x[′], y[′], δ[′], p[′])、(x[′′], y[′′], δ[′′], p[′′]) / _D._  
_̸_ _∈_  

For notational convenience, let fi := δi _ππw0((yyii||xxii))_ [, and][ ˙][f][i][ :=][ ∇][w][f][i][;][ g][i][ :=][ π]π[w]0([(]y[y]i[i]|[|]x[x]i[i])[)] [, and][ ˙][g][i][ :=][ ∇][w][g][i][.]  
記法の便宜上、fi := δi _ππw0((yyii||xxii))_ とし、[f][i][ :=][ ∇][w][f][i][;][ g][i][ :=][ π]π[w]0([(]y[y]i[i]|[|]x[x]i[i])[)] とし、[g][i][ :=][ ∇][w][g][i][.]  

First consider the vanilla IPS risk estimate of Eq. (5).  
まず、式(5)のバニラIPSリスク推定を考えます。

$$
\hat{R}_{IPS}(\pi_w) = \frac{1}{n} \sum_{i=1}^{n} \frac{\delta_i \pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} 
$$  
$$
\hat{R}_{IPS}(\pi_w) = \frac{1}{n} \sum_{i=1}^{n} \frac{\delta_i \pi_w(y_i | x_i)}{\pi_0(y_i | x_i)} 
$$  

To maximize this estimate using stochastic optimization, we must construct an unbiased gradient
estimate. That is, we randomly select one sample from D and compute a gradient $\alpha((x_i, y_i, \delta_i, p_i))$ 
and we require that  
この推定を確率的最適化を用いて最大化するためには、無偏勾配推定を構築する必要があります。つまり、Dから1つのサンプルをランダムに選択し、勾配 $\alpha((x_i, y_i, \delta_i, p_i))$ を計算し、次の条件を満たす必要があります。

$$
\nabla_w \hat{R}_{IPS}(\pi_w) = \frac{1}{n} \sum_{i=1}^{n} \nabla_w f_i = E_{i \sim D} [\alpha((x_i, y_i, \delta_i, p_i))] .
$$  
$$
\nabla_w \hat{R}_{IPS}(\pi_w) = \frac{1}{n} \sum_{i=1}^{n} \nabla_w f_i = E_{i \sim D} [\alpha((x_i, y_i, \delta_i, p_i))] .
$$  

Here the expectation is over our random choice of 1 out of n samples. Observe that
ここで、期待値はnサンプルの中から1つをランダムに選んだものです。注意すべきは、

$$
\alpha((x_i, y_i, \delta_i, p_i)) = \dot{f}_i \text{ suffices (and indeed, this corresponds to vanilla SGD):}
$$  
$$
\alpha((x_i, y_i, \delta_i, p_i)) = \dot{f}_i \text{ で十分です（実際、これはバニラSGDに対応します）:}
$$  

$$
\frac{1}{n} \sum_{i=1}^{n} \dot{f}_i = \nabla_w \hat{R}_{IPS}(\pi_w).
$$  
$$
\frac{1}{n} \sum_{i=1}^{n} \dot{f}_i = \nabla_w \hat{R}_{IPS}(\pi_w).
$$  

$E_{i \sim D} [\alpha((x_i, y_i, \delta_i, p_i))] = \frac{1}{n} \sum_{i=1}^{n} \alpha((x_i, y_i, \delta_i, p_i)) = 1$  
他の選択肢の $\alpha( )$ も無偏勾配推定を生成することができ、これは確率的分散削減勾配最適化の研究につながります。  

Now let us attempt to construct an unbiased gradient estimate for Eq. (8):  
さて、式(8)の無偏勾配推定を構築してみましょう。

$$
\hat{R}_{SNIPS}(\pi_w) = \sum_{i=1}^{n} f_i g_i 
$$  
$$
\hat{R}_{SNIPS}(\pi_w) = \sum_{i=1}^{n} f_i g_i 
$$  

Suppose such a gradient estimate exists, $\beta((x_i, y_i, \delta_i, p_i))$. Then,  
そのような勾配推定が存在すると仮定します、$\beta((x_i, y_i, \delta_i, p_i))$。次に、

$$
\nabla_w \hat{R}_{SNIPS}(\pi_w) = \nabla_w \sum_{i=1}^{n} f_i \sum_{i=1}^{n} g_i = E_{i \sim D} [\beta((x_i, y_i, \delta_i, p_i))] = n[1] 
$$  
$$
\nabla_w \hat{R}_{SNIPS}(\pi_w) = \nabla_w \sum_{i=1}^{n} f_i \sum_{i=1}^{n} g_i = E_{i \sim D} [\beta((x_i, y_i, \delta_i, p_i))] = n[1] 
$$  

This identity is true for any sample of BLBF instances – in particular, for D[′] and D[′′]:  
この同一性は、任意のBLBFインスタンスのサンプルに対して真であり、特にD[′]とD[′′]に対しても真です。

$$
\sum_{i=1}^{n} f_i + f' = \sum_{i=1}^{n} g_i + g' = \sum_{i=1}^{n} f_i + f'' = \sum_{i=1}^{n} g_i + g'' 
$$  
$$
\sum_{i=1}^{n} f_i + f' = \sum_{i=1}^{n} g_i + g' = \sum_{i=1}^{n} f_i + f'' = \sum_{i=1}^{n} g_i + g'' 
$$  

$$
\nabla_w \nabla_w \frac{1}{n + 1} \left[ \beta((x_i, y_i, \delta_i, p_i)) + \beta((x_{n+1}, y_{n+1}, \delta_{n+1}, p_{n+1})) \right] 
$$  
$$
\nabla_w \nabla_w \frac{1}{n + 1} \left[ \beta((x_i, y_i, \delta_i, p_i)) + \beta((x_{n+1}, y_{n+1}, \delta_{n+1}, p_{n+1})) \right] 
$$  

Subtracting these two equations,  
これら2つの方程式を引き算すると、

$$
\nabla_w \sum_{i=1}^{n} f_i + f' - \sum_{i=1}^{n} f_i + f'' = \sum_{i=1}^{n} g_i + g' - \sum_{i=1}^{n} g_i + g'' 
$$  
$$
\nabla_w \sum_{i=1}^{n} f_i + f' - \sum_{i=1}^{n} f_i + f'' = \sum_{i=1}^{n} g_i + g' - \sum_{i=1}^{n} g_i + g'' 
$$  

$$
= \beta((x', y', \delta', p')) - \beta((x'', y'', \delta'', p''))
$$  
$$
= \beta((x', y', \delta', p')) - \beta((x'', y'', \delta'', p''))
$$  

The LHS clearly depends on {(xi, yi, δi, pi)}_{i=1}^{n} [in general, while the RHS does not! This contra-]
左辺は明らかに {(xi, yi, δi, pi)}_{i=1}^{n} に依存していますが、右辺はそうではありません！この矛盾は、

diction indicates that no construction of $\beta$ that only looks at a sub-sample of the data can yield an
無偏勾配推定量 $\hat{R}_{SNIPS}(\pi_w)$ を得ることができないことを示しています。  



### D APPENDIX: VARIANCE REGULARIZATION D付録: 分散正則化

Unlike in conventional supervised learning, a counterfactual empirical risk estimator like _R[ˆ]IPS_ (πw) 
従来の教師あり学習とは異なり、_R[ˆ]IPS_ (πw) のような反事実的経験リスク推定器は

can have vastly different variances Var( R[ˆ]IPS (πw)) for different πw in the hypothesis space 
仮説空間内の異なる πw に対して、Var( R[ˆ]IPS (πw)) が大きく異なる可能性があります

(and _RˆSNIPS_ (πw) as well) (Swaminathan & Joachims, 2015b). 
（および _RˆSNIPS_ (πw) も同様です）（Swaminathan & Joachims, 2015b）。 

Intuitively, the “closer” the particular _πw is to the exploration policy π0, 
直感的には、特定の _πw が探索ポリシー π0 に「近い」ほど、

the larger the effective sample size (Owen, 2013) will be and the smaller the variance of the empirical risk estimate. 
有効サンプルサイズ（Owen, 2013）が大きくなり、経験リスク推定の分散が小さくなります。 

For the optimization problems we solve in Eq. (18), 
私たちが Eq. (18) で解く最適化問題においては、

this means that we should trust the λ-translated risk estimate _R[ˆ]IPS[λ][j]_ [(][π][w][)] more for some _w than for others, 
これは、特定の _w に対して他よりも λ 変換されたリスク推定 _R[ˆ]IPS[λ][j]_ [(][π][w][)] をより信頼すべきであることを意味します。

as we use _R[ˆ]IPS[λ][j]_ [(][π][w][)] only as a proxy for finding the policy that minimizes its expected value (i.e., the true loss). 
なぜなら、私たちは _R[ˆ]IPS[λ][j]_ [(][π][w][)] をその期待値（すなわち、真の損失）を最小化するポリシーを見つけるための代理としてのみ使用するからです。 

To this effect, generalization error bounds that account for this variance difference 
この目的のために、この分散の違いを考慮した一般化誤差境界

(Swaminathan & Joachims, 2015b) motivate a new type of overfitting control. 
（Swaminathan & Joachims, 2015b）は、新しいタイプの過学習制御を促進します。 

This leads to the following training objective (Swaminathan & Joachims, 2015b), 
これにより、次のトレーニング目的が導かれます（Swaminathan & Joachims, 2015b）、

which can be thought of as a more reliable version of Eq. (18): 
これは、Eq. (18) のより信頼性の高いバージョンと考えることができます：

$$
Var( R[ˆ]IPS[λ][j] [(][π][w][)]) 
$$

_n_  
$ \hat{w}^j = \arg \min_{w} RˆIPS[λ][j] [(][π][w][)] + γ $  
Here, Var( R[ˆ]IPS[λ][j] [(][π][w][)]) is the estimated variance of ˆRIPS[λ][j] [(][π][w][)] on the training data, 
ここで、Var( R[ˆ]IPS[λ][j] [(][π][w][)]) はトレーニングデータ上の ˆRIPS[λ][j] [(][π][w][)] の推定分散であり、

and γ is a regularization constant to be selected via cross validation. 
γ はクロスバリデーションを通じて選択される正則化定数です。 

The intuition behind this objective is that we optimize the upper confidence interval, 
この目的の背後にある直感は、私たちが上限信頼区間を最適化することです、

which depends on the variance of the risk estimate for each πw. 
これは、各 πw に対するリスク推定の分散に依存します。 

While this objective again does not permit SGD optimization in its given form, 
この目的は再びその形では SGD 最適化を許可しませんが、

it has been shown that a Taylor-majorization can be used to successively upper bound the objective in Eq. (35), 
テイラーの大域化を使用して Eq. (35) の目的を逐次的に上限することができることが示されています、

and that typically a small number of iterations suffices to converge to a local optimum (Swaminathan & Joachims, 2015b). 
通常、少数の反復で局所最適に収束するのに十分であることが示されています（Swaminathan & Joachims, 2015b）。 

Each such Taylor-majorization is again of a form  
各テイラーの大域化は再び次の形を持ちます：

$$
A \cdot \frac{π_w(y_i | x_i)}{π_0(y_i | x_i)} 
$$

$$
\approx B \cdot \frac{π_w(y_i | x_i)}{π_0(y_i | x_i)}^2 \cdot \frac{1}{n} \sum_{i=1}^{n} 
$$

for easily computable constants A and B (Swaminathan & Joachims, 2015b), 
計算が容易な定数 A と B のために（Swaminathan & Joachims, 2015b）、

which allows for SGD optimization. 
これにより、SGD 最適化が可能になります。 
