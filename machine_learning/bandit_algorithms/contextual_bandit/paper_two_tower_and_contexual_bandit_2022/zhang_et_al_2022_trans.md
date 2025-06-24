## Two-Stage Neural Contextual Bandits for Personalised News Recommendation

**Mengyan Zhang** _[∗]_  
オーストラリア国立大学  
Data61, CSIRO  

**Zhenyu He**  
電子科学技術大学  

**Xing Xie** **Cheng Soon Ong**  
マイクロソフトリサーチアジア  
Data61, CSIRO  
オーストラリア国立大学  

### Abstract

**Thanh Nguyen-Tang** **Fangzhao Wu**  
ディーキン大学  
マイクロソフトリサーチアジア  

We consider the problem of personalised news recommendation where each user consumes news sequentially.
私たちは、各ユーザーがニュースを逐次的に消費するパーソナライズされたニュース推薦の問題を考えます。  
Existing personalised news recommendation methods focus on exploiting user interests and ignores exploration in recommendation, which leads to biased feedback loops and hurt recommendation quality in the long term.  
既存のパーソナライズされたニュース推薦手法は、ユーザーの興味を利用することに焦点を当てており、推薦における探索を無視しているため、偏ったフィードバックループを生み出し、長期的には推薦の質を損ないます。  
We build on contextual bandits recommendation strategies which naturally address the exploitation-exploration trade-off.  
私たちは、自然に利用と探索のトレードオフに対処するコンテキストバンディット推薦戦略に基づいて構築します。  
The main challenges are the computational efficiency for exploring the large-scale item space and utilising the deep representations with uncertainty.  
主な課題は、大規模なアイテム空間を探索するための計算効率と、不確実性を伴う深い表現を利用することです。  
We propose a two-stage hierarchical topic-news deep contextual bandits framework to efficiently learn user preferences when there are many news items.  
私たちは、多くのニュースアイテムがある場合にユーザーの好みを効率的に学習するための二段階の階層的トピック-ニュース深層コンテキストバンディットフレームワークを提案します。  
We use deep learning representations for users and news, and generalise the neural upper confidence bound (UCB) policies to generalised additive UCB and bilinear UCB.  
私たちは、ユーザーとニュースのために深層学習表現(=**要するにユーザと記事のベクトルを作って、内積でスコアリングするtwo-tower model的なアプローチ**...!:thinking:)を使用し、ニューラル上限信頼区間（UCB）ポリシーを一般化加法UCBおよびバイリニアUCBに一般化します。
Empirical results on a large-scale news recommendation dataset show that our proposed policies are efficient and outperform the baseline bandit policies.  
大規模なニュース推薦データセットにおける実証結果は、私たちの提案したポリシーが効率的であり、ベースラインのバンディットポリシーを上回ることを示しています。  

### 1 Introduction

オンラインプラットフォームは、効果的かつ効率的なパーソナライズされたニュース推薦に依存しています [25]。
The recommender system faces the exploitation-exploration dilemma, where one can exploit by recommending items that the users like the most so far, or one can also explore by recommending items that users have not browsed before but may potentially like [16].  
推薦システムは、**活用と探索のジレンマ**に直面しており、ユーザーがこれまで最も好んでいるアイテムを推薦することで活用することも、ユーザーがまだ閲覧していないが好む可能性のあるアイテムを推薦することで探索することもできます [16]。  
Focusing on exploitation tends to create a pernicious feedback loop, which amplifies biases and raises the so-called filter bubbles or _echo chamber [15]_, where the exposure of items is narrowed by such a self-reinforcing pattern.  
活用に焦点を当てることは、偏見を増幅し、いわゆるフィルターバブルやエコーチェンバー [15] を引き起こす有害なフィードバックループを生み出す傾向があります。このような**自己強化パターン**によってアイテムの露出が狭まります。  

Contextual bandits are designed to address the exploitation-exploration dilemma and have been proposed used to mitigate the feedback loop effect [2, 16] by user interest and item popularity exploration.  
コンテキストバンディットは、活用と探索のジレンマに対処するために設計されており、ユーザーの興味やアイテムの人気の探索によってフィードバックループ効果を軽減するために提案されています [2, 16]。  
One can formalise the online recommendation problem as a sequential decision-making under uncertainty, where given some contextual information, an agent (the recommender system) selects one or more arms (the news items) from all possible choices according to a policy (recommendation strategy), with the goal of designing a policy which maximises the cumulative rewards (user clicks).  
**オンライン推薦問題を不確実性の下での逐次的な意思決定として形式化することができ**、いくつかの**コンテキスト情報が与えられた場合、エージェント（推薦システム）は、ポリシー（推薦戦略）に従ってすべての可能な選択肢から1つ以上のアーム（ニュースアイテム）を選択し、累積報酬（ユーザークリック）を最大化するポリシーを設計することを目指します**。  

There are two main challenges on applying contextual bandits algorithms in news recommendations.  
**ニュース推薦におけるコンテキストバンディットアルゴリズムの適用には、2つの主な課題**があります。  
First, the recommendations need to be scalable for the large news spaces with millions of news items, which requires the bandit algorithms to learn efficiently when there are many arms (news items).  
第一に、推薦は数百万のニュースアイテムを持つ大規模なニュース空間に対してスケーラブルである必要があり、これはバンディットアルゴリズムが**多くのアーム（ニュースアイテム）がある**ときに効率的に学習することを要求します。  
Second, contextual bandits algorithms need to utilise good representations of both news and users.  
第二に、コンテキストバンディットアルゴリズムは、ニュースとユーザーの両方の良い表現を利用する必要があります。  

_∗Email: mengyan.zhang@anu.edu.au_

Preprint. Under review.

-----

Figure 1: Two-stage neural contextual bandits framework for news recommendation. We address the large item space using a two-stage hierarchy of topic and news items.  
図1: ニュース推薦のための二段階ニューラルコンテキストバンディットフレームワーク。トピックとニュースアイテムの二段階の階層を使用して大規模なアイテム空間に対処します。  

The state-of-the-art news recommender systems utilise deep neural networks (DNN) with two-tower structures (user and news encoders) [24].  
最先端のニュース推薦システムは、**二塔構造（ユーザーとニュースエンコーダ）を持つ深層ニューラルネットワーク（DNN）を利用**しています [24]。  
How to combine contextual bandits models with such DNN models with valid uncertainty estimations remains an open problem.  
**コンテキストバンディットモデルをこのようなDNNモデルと有効なuncertainty estimations(不確実性推定)を持って組み合わせる方法**は、未解決の問題のままです。  
We review related work which addresses each challenge respectively in Section 3.3.  
私たちは、各課題にそれぞれ対処する関連研究をセクション3.3でレビューします。  

We propose a two-stage neural contextual bandits framework to address the above challenges, and illustrate the mapping in Figure 1.  
私たちは、上記の課題に対処するための二段階ニューラルコンテキストバンディットフレームワークを提案し、図1でマッピングを示します。  
We consider a hierarchical topic-news model, where for each of the recommendations for one user in one iteration, we recommend topics first and then select an item from the recommended topics.  
私たちは、**階層的なトピック-ニュースモデルを考慮し、1回のイテレーションで1人のユーザーに対する各推薦について、最初にトピックを推薦し、その後推薦されたトピックからアイテムを選択します**。
For each stage, we utilise the state-of-the-art two-tower deep model NRMS [24] to generate topic, news and user representations.  
各ステージでは、最先端の二塔深層モデルNRMS [24]を利用してトピック、ニュース、ユーザーの表現を生成します。  
We propose shared neural generalised additive and bilinear upper confidence bound (UCB) policies, and extend existing neural contextual bandits approaches like Monte-Carlo dropout [5] UCB, neural-linucb [20, 28] to our framework as baselines.  
私たちは、**共有ニューラル一般化加法およびバイリニア上限信頼区間（UCB）ポリシーを提案**し、モンテカルロドロップアウト [5] UCB、ニューラルLinUCB [20, 28]のような既存のニューラルコンテキストバンディットアプローチを私たちのフレームワークにベースラインとして拡張します。  
We evaluate our proposed framework empirically on a large-scale news recommendation dataset MIND [27] and compare our proposed policies with baseline approaches.  
私たちは、大規模なニュース推薦データセットMIND [27]において提案したフレームワークを実証的に評価し、提案したポリシーをベースラインアプローチと比較します。  
To our knowledge, we are the first work to apply two-stage neural contextual bandits framework to address above challenges.  
私たちの知る限り、上記の課題に対処するために二段階ニューラルコンテキストバンディットフレームワークを適用したのは初めての研究です。  

Our contributions are 1) We propose a hierarchical two-stage neural contextual bandits framework for user interest exploration in news recommendation, where in the first stage we dynamically construct topics.  
私たちの貢献は、1) ニュース推薦におけるユーザーの興味探索のための階層的二段階ニューラルコンテキストバンディットフレームワークを提案し、第一段階ではトピックを動的に構築します。  
2) We propose shared neural generalised additive and bilinear upper confidence bound policies to make use of the deep representation of contextual information.  
2) コンテキスト情報の深い表現を利用するために、共有ニューラル一般化加法およびバイリニア上限信頼区間ポリシーを提案します。  
3) We conduct experiments to simulate the user interest exploration and compare with baseline policies on a large-scale real-world news recommendation dataset.  
3) ユーザーの興味探索をシミュレートし、大規模な実世界のニュース推薦データセットにおけるベースラインポリシーと比較する実験を行います。  

<!-- ここまで読んだ! -->

### 2 Problem Setting and Challenges

**Personalised News Recommendation** We consider a news recommender system that sequentially recommends personalised news to users, with the goal of maximising cumulative clicks for all users.  
**パーソナライズされたニュース推薦** 私たちは、ユーザーにパーソナライズされたニュースを逐次的に推薦するニュース推薦システムを考え、すべてのユーザーの累積クリックを最大化することを目指します。  
The recommender system learns from the interaction history with the users, and for any given coming user, the system displays several news selected from the candidate news set.  
推薦システムはユーザーとのインタラクション履歴から学習し、特定のユーザーに対して、候補ニュースセットから選択された複数のニュースを表示します。  
Then the user will react as either click or non-click and the system uses this as the feedback to learn the preference of users.  
その後、ユーザーはクリックまたは非クリックとして反応し、システムはこれをフィードバックとして使用してユーザーの好みを学習します。  
This task is challenging since the candidate news set is in the millions and dynamically changes over time.  
このタスクは、**候補ニュースセットが数百万に及び、時間とともに動的に変化するため、困難**です。  
In addition, there are a large number of cold users (i.e. users that do not have any history) and the user interest can shift over time [25].  
さらに、**多くのコールドユーザー（すなわち、履歴を持たないユーザー）が存在**し、**ユーザーの興味は時間とともに変化する可能性**があります [25]。  
How to design such a recommendation strategy can be formulated as a sequential decision-making problem, studied in the field of contextual bandits [16, 22].  
このような推薦戦略を設計する方法は、コンテキストバンディットの分野で研究されている**sequential decision-making problem(逐次的な意思決定問題)として定式化**できます [16, 22]。  

**Cumulative Reward** We first introduce the general bandit problem formulation.
**累積報酬** まず、一般的なバンディット問題の定式化を紹介します。  
A news recommender system is regarded as an agent, news items are arms (choices), and the user and/or item embedding form the context.  
ニュース推薦システムはエージェントと見なされ、ニュースアイテムはアーム（選択肢）であり、ユーザおよび/またはアイテムの埋め込みがコンテキストを形成します。(うんうん...!:thinking:)
At each iteration $t = 1, \ldots, N$, given user $u_t$ and candidate arm set $A_t$, one can generate the item embedding $x_i \in \mathbb{R}^{d_1}$ for all $i \in A_t$, and the user embedding $z_{u_t} \in \mathbb{R}^{d_2}$ as context.  
各イテレーション $t = 1, \ldots, N$ において、ユーザー $u_t$ と候補アームセット $A_t$ が与えられた場合、すべての $i \in A_t$ に対してアイテム埋め込み $x_i \in \mathbb{R}^{d_1}$ を生成し、ユーザー埋め込み $z_{u_t} \in \mathbb{R}^{d_2}$ をコンテキストとして使用します。  
In the following, we will drop subscript $t$ for $u_t$ when there is no ambiguity.  
以下では、曖昧さがない場合は $u_t$ の下付き文字を省略します。 (自明な場合はtime step tを省略するってことね...!:thinking:)
The agent recommends $m \geq 1$ news items $S_{rec}$ according to a policy $\pi$ given the context.  
エージェントは、コンテキストが与えられた場合にポリシー $\pi$ に従って $m \geq 1$ のニュースアイテムリスト $S_{rec}$ を推薦します。  
Then the agent receives the feedback $\{y_{t,1}, \ldots, y_{t,m}\}$, where $y_{t,i} \in \{0, 1\}$ indicating whether the user clicks the item $i$ or not at iteration $t$.  
その後、エージェントはフィードバック $\{y_{t,1}, \ldots, y_{t,m}\}$ を受け取り、ここで $y_{t,i} \in \{0, 1\}$ はユーザーがイテレーション $t$ でアイテム $i$ をクリックしたかどうかを示します。
The reward is defined as $y_t = \sum_{i=1}^{m} I\{y_{t,i} = 1\}$.  
報酬は $y_t = \sum_{i=1}^{m} I\{y_{t,i} = 1\}$ と定義されます。(これは今回がクリック数を報酬としてるから! ユースケースによって報酬の定義は柔軟に調整されるはず...!:thinking:)
The goal is to design a policy to minimise the expected cumulative regret (Definition 1), which is equivalent to maximise the expected cumulative rewards [16, 22].  
**目標は、期待される累積後悔(cumulative regret)（定義1）を最小化するポリシーを設計することであり、これは期待される累積報酬を最大化することと同等**です [16, 22]。 (うんうん...!!:thinking:)
Since in recommender systems the optimal rewards are usually unknown, we focus on maximising the cumulative rewards in this work.  
推薦システムでは最適な報酬 ($y_t^{*}$) は通常未知であるため、本研究では累積報酬の最大化に焦点を当てます。(ん? これってどういうこと??:thinking:)
(あ、累積regretを最小化することが目標だけど、最適報酬が未知なので、累積regretの値を計算できない。なので、累積報酬を最大化する方法を選ぶよ、ってことか...!:thinking:)

**Definition 1. For a total iteration $N$**, the expected cumulative rewards are $E\left[\sum_{t=1}^{N} y_t\right]$.  
**定義1. 総イテレーション $N$ に対して**、期待される累積報酬は $E\left[\sum_{t=1}^{N} y_t\right]$ です。
Let the optimal reward for user $u_t$ as $y_t^{*}$, the expected cumulative regret is defined as $E\left[\sum_{t=1}^{N}(y_t^{*} - y_t)\right]$.  
ユーザー $u_t$ に対する最適な報酬を $y_t^{*}$ とし、期待される累積後悔は $E\left[\sum_{t=1}^{N}(y_t^{*} - y_t)\right]$ と定義されます。  

**Contextual Bandits Policies** Upper Confidence Bound (UCB) are one type of classical bandits policies proposed to address the exploration-exploitation dilemma and proven to have sublinear regret bound [1].  
**コンテキストバンディットポリシー** 上限信頼区間（UCB）は、探索と利用のジレンマに対処するために提案された**古典的なバンディットポリシーの一種**であり、**sublinear regret boundを持つことが証明**されています [1]。
(「sublinear regret boundを持つ」= ざっくり、UCBが長期的にはほぼ最適なポリシーに近づくことを保証する重要な性質らしい...!:thinking:)
The idea is the picking the arm with the highest UCB acquisition score, which capture the upper confidence bound for predictions in high probability.  
アイデアは、**最も高いUCB取得スコアを持つアームを選択すること**であり、これは高い確率で予測の上限信頼区間を捉えます。  
At iteration $t$, the UCB acquisition function for a pair user-item $(u, i)$ follows  
イテレーション $t$ では、ユーザー-アイテムペア $(u, i)$ に対するUCB取得関数は次のようになります。  

$$
\alpha_{UCB}(u, i) := \hat{y}_{u,i} + \beta \sigma_{u,i},
$$  

where $\hat{y}_{u,i}$ is the click prediction, $\sigma_{u,i}$ is the uncertainty of predictions, and $\beta$ is a hyperparameter balancing the exploitation and exploration.  
ここで、$\hat{y}_{u,i}$ はクリック予測(=要するに即時報酬の期待値の推定値...!:thinking:)、$\sigma_{u,i}$ は予測の不確実性、$\beta$ は利用と探索のバランスを取るハイパーパラメータです。  
<!-- 以下はcontexual bandit * 推薦に関する既存研究の紹介! ありがてぇ...! -->
Li et al. [16] popularised the LinUCB contextual bandits approach on news recommendation tasks, where the expected reward of item $i$ and user $u$ is assumed to be linear in terms of the contextual feature $c_{u,i} \in \mathbb{R}^{d}$.  
Li et al. [16] は、ニュース推薦タスクにおけるLinUCBコンテキストバンディットアプローチを普及させました。ここで、アイテム $i$ とユーザー $u$ の期待報酬は、コンテキスト特徴 $c_{u,i} \in \mathbb{R}^{d}$ に関して線形であると仮定されます。(これは見た気がする! yahooさんのやつ??:thinking:)  
Xu et al. [28], Riquelme et al. [20] studied neural linear models, where the representation of contextual information is learnt by neural networks, which further improves the performance.  
Xu et al. [28]、Riquelme et al. [20] は、**コンテキスト情報の表現がニューラルネットワークによって学習されるニューラル線形モデル**を研究し、これにより性能がさらに向上します。

(以下は要するに「即時報酬の確率分布が正規分布以外の場合にも一般化させて対応したよ！」という話っぽい!...!:thinking:)
Filippi et al. [4] extended the LinUCB policy to the Generalised Linear Model s.t. $E[y_{u,i}|c_{u,i}] = \rho(c_{u,i}^T \theta_{u}^{*})$, where $\rho: \mathbb{R} \to \mathbb{R}$ is the inverse link function, $\theta_{u}^{*} \in \mathbb{R}^{d}$ is the unknown coefficient.  
Filippi et al. [4] は、LinUCBポリシーを**一般化線形モデルに拡張**し、$E[y_{u,i}|c_{u,i}] = \rho(c_{u,i}^T \theta_{u}^{*})$ とし、ここで $\rho: \mathbb{R} \to \mathbb{R}$ は逆リンク関数、$\theta_{u}^{*} \in \mathbb{R}^{d}$ は未知の係数です。
(文脈的にinverse link functionって、「とにかく嗜好度スコアを即時報酬の期待値の推定値に変換するよ！」って役割の関数っぽい???:thinking:)
When $\rho(x) = x$, the problem is reduced to linear bandits.  
逆リンク関数(?) $\rho(x) = x$ の場合、問題は線形バンディットに一致します。
Define the design matrix $D_u \in \mathbb{R}^{n_u \times d}$ at iteration $t$, where each row contains sample interacted with user $u$.
イテレーション $t$ における設計行列 $D_u \in \mathbb{R}^{n_u \times d}$ を定義し、各行にはユーザ $u$ と相互作用したサンプルが含まれます。
With $M_u = D_u^T D_u + I_d$ and estimated coefficient $\hat{\theta}_u$, the GLM-UCB acquisition function follows:
$M_u = D_u^T D_u + I_d$ と推定係数 $\hat{\theta}_u$ を用いて、GLM-UCB取得関数は次のようになります。  
(=要するに、即時報酬yが従う確率分布が正規分布じゃない場合(ex. binary metricの場合)は、UCB取得関数としてこれを使うよ、って話...!:thinking:)

$$
\alpha_{GLM-UCB}(u, i) := \rho(c_{u,i}^T \hat{\theta}_u) + \beta \|c_{u,i}\| M_u^{-1}.
$$

(ベータの項は、不確実性の大きさを表すやつ!)
(design matrix D の構造は、ユーザの過去のinteractionの履歴を表す行列? 列はcontextの次元数 d に対応するっぽい...! なので、ユーザの過去のinteractionの履歴が少ないほど、ベータの項が大きくなる?? :thinking:)

In this paper, we consider GLM-UCB policy as a base policy.  
**本論文では、GLM-UCBポリシーをベースポリシーとして考えます**。  
Since user feedback is binary, we use the sigmoid function, i.e. we set $\rho(x) = \frac{\exp(x)}{1 + \exp(x)}$, which is the inverse link function of a Bernoulli distribution [18].  
ユーザフィードバックはバイナリであるため、シグモイド関数を使用します。すなわち、$\rho(x) = \frac{\exp(x)}{1 + \exp(x)}$ と設定し、これはベルヌーイ分布の逆リンク関数です [18]。  

<!-- ここまで読んだ! -->

**Two-tower User and Item Representation Learning** We consider the state-of-the-art news recommendation model NRMS [24] as our base model for predictor, which is a two-tower neural network.  
**二塔ユーザーおよびアイテム表現学習** 私たちは、最先端のニュース推薦モデルNRMS [24]を予測器のベースモデルとして考えます。これはtwo-towerニューラルネットワークです。
At each stage and time step $t$, we maintain two modules: 1) The item encoder $f_t^n$, which takes item information in (e.g. for topic recommendation: topic id, topic name; for news recommendation: news id, title, abstract, etc;) and outputs a news embedding $x \in \mathbb{R}^{d_1}$, and 2) the user encoder $f_t[u]$, which takes the browsed news embedding of user $i$ in and outputs a user embedding $z \in \mathbb{R}^{d_2}$.  
各ステージおよび時間ステップ $t$ において、私たちは2つのモジュールを維持します。1) アイテムエンコーダ $f_t^n$ は、**アイテム情報（例：トピック推薦の場合：トピックID、トピック名；ニュース推薦の場合：ニュースID、タイトル、要約など）を受け取り**、ニュース埋め込み $x \in \mathbb{R}^{d_1}$ を出力します。2) ユーエンコーダ $f_t^u$ は、ユーザー $i$ の閲覧したニュース埋め込みを受け取り、ユーザー埋め込み $z \in \mathbb{R}^{d_2}$ を出力します。  
The user and news embedding are treated as context, and the arms (choices) are the candidate news available to be recommended to the coming user.  
**ユーザーとニュースの埋め込みはコンテキストとして扱われ**、アーム（選択肢）は、次のユーザに推薦可能な候補ニュースです。  

**2.1 Challenges**

**Computational Efficiency: Large Item Space: Large scale commercial recommender system has millions of dynamically generated items.**  
**計算効率：大規模アイテム空間：大規模な商業推薦システムには、数百万の動的に生成されたアイテムがあります。**  
Calculating the acquisition scores for all candidate news can be computationally expensive.
**すべての候補ニュースの取得スコアを計算することは、計算コストが高くなる可能性**があります。  
We address this by proposing a two-stage framework by selecting topics first in Section 3.  
私たちは、セクション3で**最初にトピックを選択する二段階のフレームワーク**を提案することでこれに対処します。  
In terms of uncertainty inference, while Bayesian models provide distribution predictions and have shown good performance in bandits tasks, it is computationally expensive to maintain Bayesian neural models and updates for large scale systems.  
不確実性推論に関して、ベイズモデルは分布予測を提供し、バンディットタスクで良好な性能を示していますが、**大規模システムのためにベイズニューラルモデルと更新を維持することは計算コストが高くなります**。(なるほど! だからGLM*UCBなのか...!トンプソンサンプリングじゃなくて!:thinking:)  
Two-tower recommendation model is popular in practical usage due to its efficient inference.  
**two-tower推薦モデルは、その効率的な推論のために(=内積計算するだけ!)実用的な使用で人気**です。(うんうん:thinking:)
We consider the upper confidence bound (UCB) based policies and combine it with the two-tower deep learning framework with the additional generalised linear model to inference uncertainties.  
私たちは、**上限信頼区間（UCB）ベースのポリシーを考慮**し、**two-tower深層学習フレームワークと追加の一般化線形モデルを組み合わせて**不確実性を推論します。  

<!-- ここまで読んだ! -->

**Exploration-Exploitation: Uncertainty with Deep Representation:** Greedily recommending news to users according to predictors learnt by user clicks may lead to feedback loop bias and suboptimal recommendations.  
**探索-利用：深い表現による不確実性：** **ユーザのクリックによって学習された予測器に従ってニュースを貪欲にユーザに推薦することは、フィードバックループのバイアスや最適でない推薦を引き起こす可能性があります**。  
Thus, an appropriate level of online explorations can guide the system to dynamically track user interests and contributes to optimal recommendations.  
したがって、**適切なレベルのオンライン探索は、システムがユーザーの興味を動的に追跡し、最適な推薦に寄与するのを助けることができます**。  
State-of-the-art news recommender systems make use of deep neural networks to learn news and user representations.  
最先端のニュース推薦システムは、深層ニューラルネットワークを利用してニュースとユーザの表現を学習します。
How to make use of the power of deep representation and calculating uncertainties (i.e. confidence interval for predictions) is the key point of efficient exploration.  
**deepな埋め込み表現の力を利用し、不確実性（すなわち、予測の信頼区間）を計算する方法は、効率的な探索の重要なポイント**です。  
We propose two exploration policies to address this in 3.2.  
私たちは、これに対処するために3.2で**2つの探索ポリシーを提案**します。  
We further propose to dynamically form the topic set according to the bandits acquisition score, which avoids biased exploration due to unbalanced topics.  
さらに、**バンディットの取得スコアに従ってトピックセットを動的に形成することを提案し、アンバランスなトピックによる偏った探索を回避**します。  

<!-- ここまで読んだ! -->

### 3 Two-Stage Deep Recommendation Framework

Recall our goal is to sequentially recommend $m \geq 1$ news items to users in a large scale recommender system.  
私たちの目標は、大規模な推薦システムでユーザに逐次的に $m \geq 1$ のニュースアイテムを推薦することです。  
To reduce the computational complexity of whole-space news exploration, we consider a two-stage exploration framework in Algorithm 1.  
**全空間ニュース探索の計算複雑性を減らすために、アルゴリズム1で二段階の探索フレームワークを考慮**します。(この二段階の推薦は、OPEの分散問題への対応としても有効そう...!:thinking:)
We call each of the $m$ recommendation as recommendation slot.  
私たちは、$m$ 個の各推薦を**推薦スロット**と呼びます。  
In stage one (line 3-6), we recommend a set of topics for each recommendation slot.  
**第一段階（行3-6）では、各推薦スロットに対してトピックのセットを推薦**します。  
Each topic is treated as an arm, and we decide which topics can be recommended by the topic acquisition function $\alpha_1$.  
各トピックはアームとして扱われ、トピック取得関数 $\alpha_1$ によってどのトピックを推薦できるかを決定します。  
For example, one can use the UCB acquisition function defined in E.q. (1) or (2) as $\alpha_1$.  
例えば、E.q. (1) または (2) で定義されたUCB取得関数を $\alpha_1$ として使用できます。  

-----

Table 1: Summary of UCB policies. Recall $x_i, z_u$ are the item and user representation, $\hat{\theta}_u, \hat{\theta}_x, \hat{\theta}_z, \hat{\theta}$ are coefficients in generalised linear models, with respect to each user, all items, all users, and all user-item pairs respectively.  
表1: UCBポリシーの概要。$x_i, z_u$ はアイテムとユーザーの表現であり、$\hat{\theta}_u, \hat{\theta}_x, \hat{\theta}_z, \hat{\theta}$ は**一般化線形モデルにおける係数**であり、それぞれ各ユーザー、すべてのアイテム、すべてのユーザー、およびすべてのユーザー-アイテムペアに関連しています。  

Policy Coefficients Predicted Predicted  
Context  
Name Parameters Rewards Uncertainty  

GLM $\hat{x}_i$ $\hat{\theta}_u$ $\rho(x_i^T \hat{\theta}_u)$ $\|x_i\| M_u^{-1}$  
N-DropoutN-GLM $\hat{x}_i, \hat{z}_u$ $\hat{u}$ $f_{\hat{\theta}_u}^{T} f_{\hat{\theta}_n}^{-1}$ mean($\rho(x_i^T \hat{\theta}_u)$) $\|std(x_i\|Y M_{u,i}^{-1}$  
S-N-GALM $\hat{x}_i, z_u$ $f_{t[u]}^{-1}, f_{t[n]}^{-1}, \hat{\theta}_x, \hat{\theta}_z$ $\rho(\gamma x_i^T \hat{\theta}_x + \tilde{\gamma} \hat{\theta}_z^T z_u)$ $\gamma \|x_i\| A^{-1} + \tilde{\gamma} \|z_u\| A^{-1}$  
S-N-GBLM $\hat{x}_i, z_u$ $f_{t[u]}^{-1}, f_{t[n]}^{-1}, \hat{\theta}$ $\rho(x_i^T \hat{\theta}_z)$ $\|vec(x_i z_u^T)\| W_{t}^{-1}$  

-----

or (2) as $\alpha_1$.  
または (2) を $\alpha_1$ として使用します。  
For each recommendation slot, we initialise the set of recommended topics with the top $m$ acquisition scores respectively.  
各推薦スロットに対して、推薦トピック集合をそれぞれ上位 $m$ の取得スコアで初期化します。  
Then in line 6, we dynamically expand each of the topic set with the remaining high-score topics.  
次に、行6で、残りの高スコアトピックで各トピックセットを動的に拡張します。  
In stage two (line 8-11), we select the most promising news item (according to the bandit acquisition function $\alpha_2$) for each of the expanded set of topics chosen in stage one.  
第二段階（行8-11）では、第一段階で選択された拡張されたトピックセットの各トピックに対して、最も有望なニュースアイテム（バンディット取得関数 $\alpha_2$ に従って）を選択します。  
The acquisition functions in Algorithm 1 used to recommend topics and news can follow any contextual bandits policies.  
アルゴリズム1でトピックとニュースを推薦するために使用される取得関数は、任意のコンテキストバンディットポリシーに従うことができます。(任意のっていうのは、トンプソンサンプリングとか、決定的ポリシーとか...?? :thinking:)
We introduce the baselines and proposed policies we used in this work in Section 3.1 and 3.2, which are summarised in Table 1.  
私たちは、セクション3.1および3.2でこの作業で使用したベースラインと提案ポリシーを紹介し、表1に要約します。  

<!-- ここまで読んだ! -->

(上のサンプルコードでよくわからなかったやつの説明!:thinking:)
**Dynamic Topic Set Reconstruction** It is common that the sizes of the first stage arms are imbalanced.  
**動的トピックセット再構築** 第一段階のアームのサイズが不均衡であることは一般的です。  
For example, if one clusters items based on similarity, it is highly likely the clusters will end up to be imbalanced.  
例えば、アイテムを類似性に基づいてクラスタリングすると、クラスタが不均衡になる可能性が非常に高いです。  
In our application, news topics are highly imbalanced, ranging from size of 1 up to 15,000 (number of news per topics).  
私たちのアプリケーションでは、**ニューストピックは非常に不均衡で、サイズは1から15,000（トピックごとのニュース数）までの範囲**です。  
We propose to address the imbalanced topics issue by dynamically reconstructing the set of topics corresponding to each arm according to topic acquisition scores in each iteration.  
私たちは、各イテレーションにおけるトピック取得スコアに従って、各アームに対応するトピックセットを動的に再構築することで、不均衡なトピックの問題に対処することを提案します。  
After the dynamic topic set reconstruction, each topic set has at least $p$ candidate news items.  
動的トピックセット再構築の後、各トピックセットには少なくとも $p$ の候補ニュースアイテムがあります。  
The main idea of forming topic sets is to include the topics with high bandits acquisition scores, which means these topics are either potential good exploitation or exploration for user interest.  
**トピックセットを形成する主なアイデアは、高いバンディット取得スコアを持つトピックを含めること**であり、これは**これらのトピックがユーザの興味に対する潜在的な良い活用または探索であること**を意味します。  
Furthermore, we also want to allocate topics with high acquisition scores into different topic sets, so that topics with high scores will have more chance to be selected.  
さらに、高い取得スコアを持つトピックを異なるトピックセットに割り当てたいと考えており、高スコアのトピックが選択される機会が増えるようにします。(これはどういう意味???:thinking:)
We initialise each topic set with the top $m$ scoring topics $S_1, \ldots, S_m$.  
各トピックセットを上位 $m$ スコアのトピック $S_1, \ldots, S_m$ で初期化します。  
Then until all topic sets have at least $p$ news items, we add the topic with the highest topic acquisition score in the remaining topics to each of the $m$ topic set in sequential order.  
次に、すべてのトピックセットに少なくとも $p$ のニュースアイテムが含まれるまで、残りのトピックの中で最も高いトピック取得スコアを持つトピックを各 $m$ トピックセットに順次追加します。  
We illustrate the detailed description in Algorithm 2 in the Appendix.  
詳細な説明は、付録のアルゴリズム2で示します。(まあこの推薦トピック集合の再構築のロジックはドメインロジック依存だと思うし...!:thinking:)

Once the agent collects $m$ recommended items (one news item per each of $m$ recommended topics), those $m$ items will be shown to the user and the agent will get user feedback, which is $m$ binary scores indicating click or non-click for each recommended item.  
エージェントが $m$ の推薦アイテム（各 $m$ の推薦トピックごとに**1つのニュースアイテム**）を収集すると、それらの $m$ アイテムがユーザに表示され、エージェントはユーザのフィードバックを得ます。これは、各推薦アイテムに対するクリックまたは非クリックを示す $m$ のバイナリスコアです。  
The topic and news neural models are updated according to the feedback every $l_t$ and $l_n$ (pre-defined hyperparameters) iterations respectively.  
トピックとニュースのニューラルモデルは、それぞれフィードバックに従って毎 $l_t$ および $l_n$ （これらは事前定義されたハイパーパラメータ）イテレーションで更新されます。
(あ、**フィードバックがxx件溜まったらパラメータ更新する**、っていう設定か...!:thinking:)
The coefficients of generalised linear models are updated every iteration if applicable.  
**一般化線形モデルの係数は、適用可能な場合は毎イテレーションで更新されます**。
(あ、GLMのパラメータ更新は、two-towerモデルと比べて計算量が小さいはずだから...!:thinking:)  

<!-- ここまで読んだ! -->

#### 3.1 Baseline Neural Contextual Bandits Policies: Exploration 3.1 ベースラインニューラルコンテキストバンディットポリシー：探索

Recent work have studied neural contextual bandits algorithms theoretically [30, 28] and empirically [20], according to those we adapt two most popular algorithms into our framework [3, 28] (see below).  
最近の研究では、ニューラルコンテキストバンディットアルゴリズムが理論的に [30, 28] および実証的に [20] 研究されており、それに基づいて私たちは最も人気のある2つのアルゴリズムを私たちのフレームワークに適応させます [3, 28] （以下を参照）。  

**Neural Dropout UCB (N-Dropout-UCB)** As studied by Gal and Ghahramani [5], the uncertainty of predictions can be approximated by dropout applied to a neural network with arbitrary depth and non-linearity.  
**ニューラルドロップアウトUCB (N-Dropout-UCB)** GalとGhahramani [5] によって研究されたように、予測の不確実性は、任意の深さと非線形性を持つニューラルネットワークに適用されたドロップアウトによって近似できます。  
Dropout can be viewed as performing approximate variational inference, with a variational family that is a discrete distribution over the value of the parameters and zero.  
ドロップアウトは、パラメータの値とゼロの間の離散分布を持つ変分ファミリーを用いた近似変分推論を行うと見なすことができます。  
Dropout UCB policies follow this principle, where for user-item pair $(u, i)$, one can predict the click scores with Monte-Carlo dropout enabled, $Y_{u,i}[n] = [\hat{y}_{u,i}^{(1)}, \ldots, \hat{y}_{u,i}^{(n)}]$, where $\hat{y}_{u,i} = f_{t-1}(u)^T f_{t-1}(i)$.  
**ドロップアウトUCBポリシーはこの原則に従い、ユーザー-アイテムペア $(u, i)$ に対して、モンテカルロドロップアウトを有効にしてクリックスコアを予測**できます。$Y_{u,i}[n] = [\hat{y}_{u,i}^{(1)}, \ldots, \hat{y}_{u,i}^{(n)}]$、ここで $\hat{y}_{u,i} = f_{t-1}(u)^T f_{t-1}(i)$ です。  
Then using the mean of the predictions $\bar{y}_{u,i}$ as central tendency and the standard deviation $\sigma_{u,i}$ as the uncertainty, one can follow UCB policy defined in E.q. (1).  
次に、予測の平均 $\bar{y}_{u,i}$ を中心傾向として、標準偏差 $\sigma_{u,i}$ を不確実性として使用することで、E.q. (1) で定義されたUCBポリシーに従うことができます。  

**Neural Generalised Linear UCB (N-GLM-UCB)** To utilise the representation power of DNNs and the exploration ability from linear bandits, Neural-Linear [20, 28] learns contextual embedding from DNNs and use it as input of a linear model.  
**ニューラル一般化線形UCB (N-GLM-UCB)** DNNの表現力を利用し、線形バンディットからの探索能力を活用するために、Neural-Linear [20, 28] は**DNNからコンテキスト埋め込みを学習し、それを線形モデルの入力として使用**します。(うんうん、シンプル!:thinking:)
Since our reward is binary, we extend neural LinUCB [28] to neural generalised linear UCB, where we first get the deep contextual embedding learnt from NRMS model, and then follow the same acquisition function as in E.q. (2).  
私たちの報酬はバイナリであるため、ニューラルLinUCB [28] をニューラル一般化線形UCBに拡張し、**最初にNRMSモデルから学習したdeepなコンテキスト埋め込みを取得し、次にE.q. (2) と同じ取得関数に従います**。  
Applying existing neural contextual bandits algorithms directly on recommender systems may be computationally expensive or lead to suboptimal performance.  
**既存のニューラルコンテキストバンディットアルゴリズムを推薦システムに直接適用することは、計算コストが高くなるか、最適でない性能を引き起こす可能性があります**。  
For example, uncertainties inferred from Monte-Carlo can have high variance [20].  
例えば、モンテカルロから推測された不確実性は高い分散を持つ可能性があります [20]。  
Also, learning coefficients for each arm in neural-linear models is unrealistic, since one needs enough samples for each of the millions of news items.  
**また、ニューラル-線形モデルにおける各アームの係数を学習することは非現実的であり、数百万のニュースアイテムの各々に対して十分なサンプルが必要**です。(行動空間が大きいし、ダイナミックに変化するし!)
In our simulation, the number of users is much smaller than the news items, hence we learn coefficients per user.  
**私たちのシミュレーションでは、ユーザの数はニュースアイテムよりもはるかに少ないため、ユーザーごとに係数を学習**します。(なるほど?? 場合によってはユーザごとのパラメータも排除する選択肢もありそう...!:thinking:)
From our experiment in Table 2, we observe that performance still drop when the number of users increases.  
表2の実験から、ユーザーの数が増加すると性能が低下することを観察します。

<!-- ここまで読んだ! -->

#### 3.2 Proposed Policies: Additive and Bilinear UCB 提案ポリシー：加法的およびバイリニアUCB

We consider shared bandits models where the parameters are shared by all pairs of users and (or) news items.
私たちは、**パラメータがすべてのユーザーおよび（または）ニュースアイテムのペアによって共有されるshared bandits models(共有バンディットモデル)を考慮**します。
Coefficient sharing across entities can make the model learned more efficient and more generalisable.
**エンティティ間での係数共有は、学習されたモデルをより効率的かつ一般化可能にすることができます**。(うんうん、コールドスタートアイテムやコールドスタートユーザに適用可能だし...!:thinking:)

One also needs to design how to capture both the item and user embedding in the contextual information.  
また、**コンテキスト情報におけるアイテムとユーザの埋め込みの両方をどのようにキャプチャするか**を設計する必要があります(??)
We propose the generalised additive linear or generalised bilinear models to handle this.  
これに対処するために、一般化加法線形モデルまたは一般化バイリニアモデルを提案します。
Recall $x_i \in \mathbb{R}^{d_1}$ as item $i$ representation and $z_u \in \mathbb{R}^{d_2}$ as user $u$ representation.  
アイテム $i$ の表現を $x_i \in \mathbb{R}^{d_1}$、ユーザ $u$ の表現を $z_u \in \mathbb{R}^{d_2}$ として再確認します。  

<!-- ここまで読んだ! -->

(以下は、アイテム関連のパラメータと、ユーザ関連のパラメータを別々にモデル化する話!)

**Shared Neural Generalised Additive Linear UCB (S-N-GALM-UCB)** We consider an additive linear model, where the item-related coefficient $\theta_x^{*}$ and user-related coefficient $\theta_z^{*}$ are modelled separately, i.e. $E[y_{u,i}|x_i, z_u] = \rho(\gamma x_i^T \theta_x^{*} + \tilde{\gamma} \theta_z^{*T} z_u)$, where $\gamma$ is a hyperparameter, $\tilde{\gamma} = 1 - \gamma$.  
**共有ニューラル一般化加法線形UCB (S-N-GALM-UCB)** 私たちは加法線形モデルを考慮し、アイテム関連の係数 $\theta_x^{*}$ とユーザ関連の係数 $\theta_z^{*}$ を別々にモデル化します。すなわち、$E[y_{u,i}|x_i, z_u] = \rho(\gamma x_i^T \theta_x^{*} + \tilde{\gamma} \theta_z^{*T} z_u)$ とし、ここで $\gamma$ はハイパーパラメータ、$\tilde{\gamma} = 1 - \gamma$ です。  
The acquisition function follows  
UCB取得関数は次のようになります:

$$
\alpha_{S-N-GALM-UCB}(u, i) := \rho(\gamma x_i^T \hat{\theta}_x + \tilde{\gamma} \hat{\theta}_z^T z_u) + \beta(\gamma \|x_i\| A^{-1} + \tilde{\gamma} \|z_u\| A^{-1}),
$$

where $A_i = D_i^T D_i + I_d$, with $D_i \in \mathbb{R}^{n_i \times d_1}$ be a design matrix at iteration $t$, where each row contains item representations that user $u$ that has been observed up to iteration $t$; $A_u = D_u^T D_u + I_d$, with $D_u \in \mathbb{R}^{n_u \times d_2}$ be a design matrix at iteration $t$, where each row contains user representations that item $i$ has been recommended to up to iteration $t$.
ここで、

- $A_i = D_i^T D_i + I_d$ とする
  - $D_i \in \mathbb{R}^{n_i \times d_1}$ はイテレーション $t$ における設計行列。
    - 各行にはユーザ $u$ に対してイテレーション $t$ までに観察されたアイテム表現が含まれます。
- $A_u = D_u^T D_u + I_d$ とする。
  - $D_u \in \mathbb{R}^{n_u \times d_2}$ はイテレーション $t$ における設計行列。
    - 各行にはアイテム $i$ がイテレーション $t$ までに推薦されたユーザ表現が含まれる。  

In this way, the additive model handles the user and item uncertainties separately.  
このようにして、加法モデルはユーザとアイテムの不確実性を別々に扱います。

<!-- ここまで読んだ! -->
(以下は、すべてのユーザ、アイテムで共通のパラメータを使う話)

**Shared Neural Generalised Bilinear UCB (S-N-GBLM-UCB)** Inspired by the Bilinear UCB algorithm (rank $r$ Oracle UCB) proposed by Jang et al. [14], we consider a Generalised bilinear model, where we assume $E[y_{u,i}|x_i, z_u] = \rho(x_i^T \theta^{*} z_u)$, with the coefficient $\theta^{*}$ shared by all user-item pairs.  
**共有ニューラル一般化バイリニアUCB (S-N-GBLM-UCB)** Jang et al. [14] によって提案されたバイリニアUCBアルゴリズム（ランク $r$ オラクルUCB）に触発され、一般化バイリニアモデルを考慮します。ここで、$E[y_{u,i}|x_i, z_u] = \rho(x_i^T \theta^{*} z_u)$ とし、**パラメータ $\theta^{*}$ はすべてのユーザ-アイテムペアで共有**されます。
(うんうん、ユーザもアイテムも数が多い場合は、こっちの方が使い勝手良さそう...!:thinking:)
The acquisition function follows

$$
\alpha^{S-N-GBLM-UCB}(u, i) := \rho(x_i^T \hat{\theta}_z) + \beta \|vec(x_i z_u^T)\| W_{t}^{-1},
$$

where $W_t = W_0 + \sum_{s=1}^{t} vec(x_i z_u^T) vec(x_i z_u^T)^T \in \mathbb{R}^{d_1 d_2 \times d_1 d_2}$, and $W_0 = I_{d_1 d_2}$.  
ここで、$W_t = W_0 + \sum_{s=1}^{t} vec(x_i z_u^T) vec(x_i z_u^T)^T \in \mathbb{R}^{d_1 d_2 \times d_1 d_2}$ とし、$W_0 = I_{d_1 d_2}$ です。  
Computing the confidence interval might be computationally costly due to the inverse of a potentially large design matrix.
信頼区間を計算することは、潜在的に大きな設計行列の逆行列を計算する必要があるため、計算コストが高くなる可能性があります。  
Different from Jang et al. [14], instead recommending a pair of arms $(u, i)$, we consider the item $i$ as arm to be recommended, and user $u$ as side information instead of an arm.  
Jang et al. [14] とは異なり、アームのペア $(u, i)$ を推薦するのではなく、アイテム $i$ を推薦されるアームとし、ユーザー $u$ をアームではなくサイド情報と見なします。  
The two-tower model in recommender system is naturally expressed in terms of bilinear structure.  
推薦システムにおける二塔モデルは、バイリニア構造の観点から自然に表現されます。  

A bilinear bandit can be reinterpreted in the form of linear bandits [14], $x_i^T \theta^{*} z_u = \sum_{s=1}^{r} vec(x_i z_u^T) vec(\theta^{*})$.  
バイリニアバンディットは、線形バンディットの形で再解釈できます [14]。$x_i^T \theta^{*} z_u = \sum_{s=1}^{r} vec(x_i z_u^T) vec(\theta^{*})$。  
So linear bandits policies can be applied on bilinear bandits problem with regret upper bound $O(\tilde{O}(d_1^2 d_2^2 T))$, where $\tilde{O}$ ignores polylogarithmic factors in $T$.  
したがって、線形バンディットポリシーは、後悔の上限境界 $O(\tilde{O}(d_1^2 d_2^2 T))$ を持つバイリニアバンディット問題に適用できます。ここで、$\tilde{O}$ は $T$ におけるポリログ的要因を無視します。  
However naive linear bandit approaches cannot fully utilise the characteristics of the parameters space.  
しかし、単純な線形バンディットアプローチは、パラメータ空間の特性を完全に活用することはできません。  
The bilinear policy [14] shows the regret upper bound $O(\tilde{O}(\sqrt{d_1 d_2 r T}))$, with $d = \max(d_1, d_2)$ and $r = \text{rank}(\theta^{*})$.  
バイリニアポリシー [14] は、後悔の上限境界 $O(\tilde{O}(\sqrt{d_1 d_2 r T}))$ を示し、$d = \max(d_1, d_2)$ および $r = \text{rank}(\theta^{*})$ です。  

**3.3 Related Work**

**Hierarchical Exploration** To address large item spaces, hierarchical search is employed.  
**関連研究** **階層的探索** 大規模なアイテム空間に対処するために、階層的検索が採用されます。  
For two-stage bandits work, Hron et al. [10, 11] studied the effect of exploration in both two stages with linear bandits algorithms and Mixture-of-Experts nominators.  
二段階バンディットの研究において、Hron et al. [10, 11] は、線形バンディットアルゴリズムとMixture-of-Expertsノミネーターを用いて、両方の段階での探索の効果を研究しました。  
Ma et al. [17] proposed off-policy policy-gradient two stage approaches, however, without explicit two-stage exploration.  
Ma et al. [17] はオフポリシーのポリシー勾配二段階アプローチを提案しましたが、明示的な二段階探索はありません。  
There is also a branch of related work considering hierarchical exploration.  
階層的探索を考慮した関連研究の分野もあります。  
Wang et al. [23], Song et al. [22] explored on a pre-constructed tree of items in MAB or linear bandits setting.  
Wang et al. [23]、Song et al. [22] は、MABまたは線形バンディット設定における事前構築されたアイテムのツリーを探索しました。  
Zhang et al. [29] utilises key-terms to organise items into subsets and relies on occasional conversational feedback from users.  
Zhang et al. [29] は、キーワードを利用してアイテムをサブセットに整理し、ユーザーからの偶発的な会話フィードバックに依存します。  
As far as we know, no existing work studies two-stage exploration with deep contextual bandits.  
私たちの知る限り、既存の研究の中で深いコンテキストバンディットを用いた二段階探索を研究したものはありません。  

**Neural Contextual Bandits** Contextual bandits with deep models have been used as a popular approach since it utilise good representations.  
**ニューラルコンテキストバンディット** 深いモデルを用いたコンテキストバンディットは、良い表現を利用するため、人気のあるアプローチとして使用されています。  
Riquelme et al. [20] conducted a comprehensive experiment on deep contextual bandits algorithms based on Thompson sampling, including dropout, neural-linear and bootstrapped methods.  
Riquelme et al. [20] は、ドロップアウト、ニューラル-線形、ブートストラップ法を含む、トンプソンサンプリングに基づく深いコンテキストバンディットアルゴリズムに関する包括的な実験を行いました。  
Recently, there are work applying deep contextual bandits to recommender system.  
最近、推薦システムに深いコンテキストバンディットを適用する研究があります。  
Collier and Llorens [3] proposed a Thompson sampling algorithm based on inference time Concrete Dropout [6] with learnable dropout rate, and applied this approach on marketing optimisation problems at HubSpot.  
CollierとLlorens [3] は、学習可能なドロップアウト率を持つ推論時間コンクリートドロップアウト [6] に基づくトンプソンサンプリングアルゴリズムを提案し、このアプローチをHubSpotのマーケティング最適化問題に適用しました。  
Guo et al. [8] studied deep Bayesian bandits with a bootstrapped model with multiple heads and dropout units, which was evaluated offline and online in Twitter’s ad recommendation.  
Guo et al. [8] は、複数のヘッドとドロップアウトユニットを持つブートストラップモデルを用いた深いベイジアンバンディットを研究し、**Twitterの広告推薦においてオフラインおよびオンラインで評価**されました。(これは後で読もうかな...!:thinking:)
Hao et al. [9] added representation uncertainty for embedding to further encourage explore items whose embedding have not been sufficiently learned based on recurrent neural network models.  
Hao et al. [9] は、埋め込みの表現不確実性を追加して、再帰的ニューラルネットワークモデルに基づいて十分に学習されていないアイテムを探索することをさらに促進しました。  

Theoretically, Zhou et al. [30] proposed NeuralUCB and proved a sublinear regret bound, followed which Gu et al. [7] studied the case where the parameters of DNN only update at the end of batches.  
理論的には、Zhou et al. [30] はNeuralUCBを提案し、サブリニア後悔境界を証明しました。その後、Gu et al. [7] はDNNのパラメータがバッチの最後でのみ更新される場合を研究しました。  
Xu et al. [28] proposed Neural-LinUCB to make the use of deep representation from deep neural networks and shallow exploration with a linear UCB model, and provided a sublinear regret bound.  
Xu et al. [28] は、**深層ニューラルネットワークからの深い表現を利用し、線形UCBモデルで浅い探索を行う**ためにNeural-LinUCBを提案し、サブリニア後悔境界を提供しました。  
Zhu and Rigotti [31] proposed sample average uncertainty frequentist exploration, which only depends on value predictions on each action and is computationally efficient.  
ZhuとRigotti [31] は、各アクションの値予測のみに依存し、計算効率が高いサンプル平均不確実性頻度主義探索を提案しました。  

To the best of our knowledge, among those utilised the power of deep representation from existing network structures in online recommender system with bandits feedback, no existing work addressed the generalised bilinear model for exploration, which suits the two-tower recommender system naturally; and no work has addressed the hierarchical exploration, which can increase the computational efficiency and is important to the practical use in a large-scale recommender system.  
私たちの知る限り、バンディットフィードバックを持つオンライン推薦システムにおいて既存のネットワーク構造からの深い表現の力を利用した研究の中で、探索のための一般化バイリニアモデルに対処したものはなく、これは二塔推薦システムに自然に適合します。また、大規模推薦システムの実用的な使用において計算効率を高めることができる階層的探索に対処した研究もありません。  

<!-- ここまで読んだ! -->

### 4 Experiments

We conduct experiments on a large-scale news recommendation dataset, i.e. MIND [27], which was collected from the user behaviour logs of Microsoft News.  
私たちは、大規模なニュース推薦データセット、すなわちMIND [27] に関する実験を行います。これは、Microsoft Newsのユーザー行動ログから収集されました。  
The MIND dataset contains 1,000,000 users, 161,013 news, 285 topics and 24,155,470 samples, which is split to train, validation and test data for machine learning algorithm usage.  
MINDデータセットには、1,000,000人のユーザー、161,013件のニュース、285のトピック、24,155,470件のサンプルが含まれており、機械学習アルゴリズムの使用のためにトレーニング、検証、テストデータに分割されています。  

We simulate the sequential recommendation based on MIND dataset.  
私たちは、**MINDデータセットに基づいて逐次推薦をシミュレート**します。(オフライン評価!)
The experiments run in $T$ independent trials.  
実験は $T$ の独立した試行で実行されます。  
For each trial $\tau \in [1, T]$, we randomly select a set of users $U_{\tau}$ from the whole user set as the candidate user dataset from trial $\tau$.  
各試行 $\tau \in [1, T]$ に対して、全ユーザーセットからユーザーのセット $U_{\tau}$ をランダムに選択し、試行 $\tau$ からの候補ユーザーデータセットとします。  
We randomly select $\epsilon\%$ of samples $S_{known}$ from the MIND-train dataset as known data to the bandit models and can be used to pre-train the parameters of bandits neural model NRMS.  
MIND-trainデータセットからサンプルの $\epsilon\%$ をランダムに選択し、バンディットモデルに対する既知のデータとして使用し、バンディットニューラルモデルNRMSのパラメータを事前学習するために使用できます。  
Note we have removed the samples of the users in $U_{\tau}$ from $S_{known}$ for each trial $\tau$ to avoid leak information.  
各試行 $\tau$ に対して、情報漏洩を避けるために $S_{known}$ から $U_{\tau}$ のユーザーのサンプルを削除したことに注意してください。  
This simulates the case where in recommender system we have collected some history clicks for other users and we would like to recommend news to new users sequentially and learn their interests.  
これは、推薦システムにおいて他のユーザーのためにいくつかの履歴クリックを収集し、新しいユーザーにニュースを逐次的に推薦し、彼らの興味を学習したい場合をシミュレートします。  
In each iteration $t$ of the total $N$ simulation iterations within each trial $\tau$, we randomly sample a user $u_t \in U_{\tau}$ to simulate the way user $u_t$ randomly shows up to the recommender system.  
各試行 $\tau$ 内の総 $N$ シミュレーションイテレーションの各イテレーション $t$ において、ユーザー $u_t \in U_{\tau}$ をランダムにサンプリングして、ユーザー $u_t$ が推薦システムにランダムに現れる方法をシミュレートします。  

To illustrate how the computational complexity of algorithms influence the performance, we follow Song et al. [22] and introduce the computational budget $b = 5000$, which constraints the maximum number of acquisition score over arms one can compute before conducting the recommendation.  
アルゴリズムの計算複雑性が性能にどのように影響するかを示すために、私たちはSong et al. [22] に従い、計算予算 $b = 5000$ を導入します。これは、推薦を行う前に計算できる取得スコアの最大数を制約します。  
The computational budget is set to evaluate the computational efficiency of algorithms and is meaningful for practical applications like large-scale recommender system.  
**計算予算は、アルゴリズムの計算効率を評価するために設定されており、大規模推薦システムのような実用的なアプリケーションにとって意義があります**。  
For one-stage algorithms, we randomly sample $b$ news from the whole news set for the candidate news set of iteration $t$; for two-stage algorithms, we first query all topics then use the left budget to explore the items.  
一段階アルゴリズムの場合、イテレーション $t$ の候補ニュースセットのために全ニュースセットから $b$ ニュースをランダムにサンプリングします。二段階アルゴリズムの場合、最初にすべてのトピックをクエリし、残りの予算を使用してアイテムを探索します。  

We evaluate the performance by the cumulative rewards as defined in Definition 1.  
私たちは、**定義1で定義された累積報酬によって性能を評価**します。  
To make the score more comparable between different number of recommendations, we further define the clickthrough-rate (CTR) inside a batch of $m$ recommendations at iteration $t$ for each trial $\tau$ as $CTR[\tau]_t = \frac{1}{m} \sum_{i=1}^{m} I\{y_{t,\tau} = 1\}$.  
異なる数の推薦間でスコアをより比較可能にするために、各試行 $\tau$ におけるイテレーション $t$ の $m$ の推薦のバッチ内でのクリック率（CTR）を $CTR[\tau]_t = \frac{1}{m} \sum_{i=1}^{m} I\{y_{t,\tau} = 1\}$ と定義します。  
Then we evaluate the performance of bandits policies by the cumulative CTR over $N$ iterations $\sum_{t=1}^{N} CTR_t[\tau]$.  
次に、$N$ イテレーションにわたる累積CTR $\sum_{t=1}^{N} CTR_t[\tau]$ によってバンディットポリシーの性能を評価します。  
We report the mean and standard deviation of the cumulative reward or CTR over $T$ trials.  
私たちは、$T$ 試行にわたる累積報酬またはCTRの平均と標準偏差を報告します。  

-----

Table 2: Cumulative CTR for one stage policies with different number of users. We recommend 5 news for each user and simulate the experiment with 2,000 iterations, 5 trials. In policy names, “S” means shared parameters, and “N” means using neural contextual information from the NRMS.  
表2: 異なるユーザー数に対する一段階ポリシーの累積CTR。各ユーザーに5つのニュースを推薦し、2,000イテレーション、5試行で実験をシミュレートします。ポリシー名の「S」は共有パラメータを意味し、「N」はNRMSからのニューラルコンテキスト情報を使用することを意味します。  
