refs: https://ar5iv.labs.arxiv.org/html/1910.10410
# BanditRank: Learning to Rank Using Contextual Bandits コンテキストバンディットを用いたランキング学習

## Abstract

We propose an extensible deep learning method that uses reinforcement learning to train neural networks for offline ranking in information retrieval (IR).
私たちは、情報検索（IR）におけるオフラインランキングのためにニューラルネットワークを訓練する強化学習を使用した拡張可能な深層学習手法を提案します。
We call our method BanditRank as it treats ranking as a contextual bandit problem.
私たちの手法は**BanditRankと呼ばれ、ランキングをコンテキストバンディット問題として扱います**。
In the domain of learning to rank for IR, current deep learning models are trained on objective functions different from the measures they are evaluated on.
**IRのためのランキング学習の分野において、現在の深層学習モデルは、評価される指標とは異なる目的関数で訓練されています**。
Since most evaluation measures are discrete quantities, they cannot be leveraged by directly using gradient descent algorithms without an approximation. 
ほとんどの評価指標は離散的な量であるため、近似なしに勾配降下アルゴリズムを直接使用することはできません。 
BanditRank bridges this gap by directly optimizing a task-specific measure, such as mean average precision (MAP), using gradient descent. 
BanditRankは、勾配降下を使用して、平均適合率（MAP）などのタスク特有の指標を直接最適化することによって、このギャップを埋めます。 
Specifically, a contextual bandit whose action is to rank input documents is trained using a policy gradient algorithm to directly maximize the reward. 
具体的には、入力文書をランキングするアクションを持つコンテキストバンディットが、報酬を直接最大化するためにポリシー勾配アルゴリズムを使用して訓練されます。 
The reward can be a single measure, such as MAP, or a combination of several measures. 
報酬は、MAPのような単一の指標や、いくつかの指標の組み合わせである可能性があります。 
The notion of ranking is also inherent in BanditRank, similar to the current listwise approaches. 
BanditRankには、現在のlistwiseアプローチと同様に、ランキングの概念も内在しています。 
To evaluate the effectiveness of BanditRank, we conducted a series of experiments on datasets related to three different tasks, i.e., web search, community, and factoid question answering. 
BanditRankの効果を評価するために、私たちはウェブ検索、コミュニティ、ファクトイド質問応答の3つの異なるタスクに関連するデータセットで一連の実験を行いました。 
We found that it performs better than state-of-the-art methods when applied on the question answering datasets. 
質問応答データセットに適用した際、最先端の手法よりも優れた性能を示すことがわかりました。 
On the web search dataset, we found that BanditRank performed better than four strong listwise baselines including LambdaMART, AdaRank, ListNet and Coordinate Ascent.
ウェブ検索データセットでは、BanditRankがLambdaMART、AdaRank、ListNet、Coordinate Ascentを含む4つの強力なlistwiseベースラインよりも優れた性能を発揮したことがわかりました。 

<!-- ここまで読んだ！ -->

## 1.Introduction 1. はじめに

Learning to rank is an important sub-field of information retrieval (IR), which involves designing models that rank documents corresponding to a query in order of their relevance. 
ランキング学習は情報検索（IR）の重要なサブフィールドであり、クエリに対応する文書を関連性の順にランク付けするモデルを設計することを含みます。
Considering the type of learning approach used, all ranking models can be classified into three categories, i.e., pointwise, pairwise, and listwise. 
**使用される学習アプローチの種類を考慮すると、すべてのランキングモデルは、ポイントワイズ、ペアワイズ、リストワイズの3つのカテゴリに分類できます**。
The ranking models are either trained on indirect objective functions, such as classification related functions, or direct objective functions related to the evaluation measures. 
ランキングモデルは、分類関連の関数のような間接的な目的関数、または評価指標に関連する直接的な目的関数のいずれかで訓練されます。(うんうん..)
Direct optimization of IR measures has been a long standing challenge in the learning-to-rank domain. 
**IR指標の直接最適化は、ランキング学習の分野における長年の課題**です。
If we only consider bounded IR measures such as MAP, a theoretical justification is provided regarding the superiority of direct optimization techniques(Qin etal.,2010). 
MAPのような制約のあるIR指標のみを考慮すると、直接最適化技術の優位性に関する理論的な正当性が提供されます（Qin et al., 2010）。
That study states that if an algorithm can directly optimize an IR measure on the training data, the ranking function learned with the algorithm will be one of the best ranking functions one can obtain in terms of expected test performance with respect to the same IR measure. 
その研究は、アルゴリズムがトレーニングデータ上でIR指標を直接最適化できる場合、アルゴリズムで学習されたランキング関数は、同じIR指標に関する期待されるテスト性能の観点から得られる最良のランキング関数の1つであると述べています。
Several algorithms have been developed that use direct optimization, and they can be grouped into three categories. 
**直接最適化を使用するいくつかのアルゴリズムが開発されており、それらは3つのカテゴリに分類できます**。
The algorithms in the first category try to optimize the surrogate objective functions, which are either upper bounds of IR measures(Xu and Li,2007; Yue etal.,2007; Chapelle etal.,2007)or smooth approximations of IR measures(Guiver and Snelson,2008; Taylor etal.,2008). 
最初のカテゴリのアルゴリズムは、IR指標の上限（Xu and Li, 2007; Yue et al., 2007; Chapelle et al., 2007）またはIR指標の滑らかな近似（Guiver and Snelson, 2008; Taylor et al., 2008）である代理目的関数を最適化しようとします。
The algorithms in the second category smoothly approximate the true gradient of the evaluation measures, similar to LambdaRank(Burges etal.,2007; Donmez etal.,2009; Burges,2010; Yuan etal.,2016). 
2番目のカテゴリのアルゴリズムは、LambdaRank（Burges et al., 2007; Donmez et al., 2009; Burges, 2010; Yuan et al., 2016）に似て、評価指標の真の勾配を滑らかに近似します。
The algorithms in the third category directly optimize evaluation measures in the form of rewards without any approximation using reinforcement learning such as MDPRank(Wei etal.,2017; Zhao etal.,2018). 
3番目のカテゴリのアルゴリズムは、MDPRank（Wei et al., 2017; Zhao et al., 2018）などの強化学習を使用して、近似なしに報酬の形で評価指標を直接最適化します。
However, except for some algorithms like LambdaRank, most of the algorithms in all the categories are only suitable for models with less parameters(Donmez etal.,2009)making it difficult to use deep neural networks, which are quite effective. 
**しかし、LambdaRankのような一部のアルゴリズムを除いて、すべてのカテゴリのほとんどのアルゴリズムは、パラメータが少ないモデルにのみ適しており（Donmez et al., 2009）、非常に効果的な深層ニューラルネットワークを使用することが難しくなります**。

<!-- ここまで読んだ! -->

Deep learning(LeCun etal.,2015)models have been proven to be effective with state-of-the-art results in many machine learning applications such as speech recognition, computer vision, and natural language processing, which leads to the introduction of neural networks in IR. 
深層学習（LeCun et al., 2015）モデルは、音声認識、コンピュータビジョン、自然言語処理などの多くの機械学習アプリケーションで最先端の結果を出すことが証明されており、これがIRにおけるニューラルネットワークの導入につながっています。
Neural networks have been used for functions such as automatic feature extraction and comparison and aggregation of local relevance(Guo etal.,2016; Hu etal.,2014; Huang etal.,2013; Wan etal.,2016; Pang etal.,2017). 
ニューラルネットワークは、自動特徴抽出やローカル関連性の比較と集約（Guo et al., 2016; Hu et al., 2014; Huang et al., 2013; Wan et al., 2016; Pang et al., 2017）などの機能に使用されています。
But, the neural networks are generally trained on objective functions such as cross entropy, which is not related to the evaluation measures. 
**しかし、ニューラルネットワークは一般的に、評価指標に関連しない交差エントロピーのような目的関数で訓練されます**。(ただ論文で提案されてる目的関数を無心で採用する例が多いよね、って話かな)
They do not have information about the measures that they are going to be evaluated on, i.e., the objective functions indirectly optimize the evaluation measures. 
彼らは、評価される指標に関する情報を持っておらず、つまり、**目的関数は評価指標を間接的に最適化**します。
Since most evaluation measures such as MAP, mean reciprocal rank (MRR), and normalized discounted cumulative gain (nDCG) are not differentiable, they cannot be used as the objective functions for training the neural networks. 
**MAP、平均逆順位（MRR）、および正規化割引累積ゲイン（nDCG）などのほとんどの評価指標は微分可能ではないため、ニューラルネットワークの訓練のための目的関数として使用することはできません**。(あ、そういう話なのか...:thinking:)
For leveraging the efficacy of neural networks and superiority of direct optimization, we propose an extensible deep learning method called BanditRank. 
ニューラルネットワークの有効性と直接最適化の優位性を活用するために、私たちはBanditRankと呼ばれる拡張可能な深層学習方法を提案します。
BanditRank formulates ranking as a contextual bandit problem and trains neural networks using the policy gradient algorithm(Sutton etal.,2000), for directly maximizing the target measures. 
BanditRankはランキングをコンテキストバンディット問題として定式化し、**ポリシー勾配アルゴリズム（Sutton et al., 2000）を使用してターゲット指標を直接最大化するためにニューラルネットワークを訓練します**。
Contextual bandit is a type of reinforcement learning algorithm used in decision-making scenarios in which an action has to be taken by an agent depending on the provided context. 
コンテキストバンディットは、提供されたコンテキストに基づいてエージェントがアクションを取る必要がある意思決定シナリオで使用される強化学習アルゴリズムの一種です。
The exact details of the formulation are provided in Section3. 
定式化の正確な詳細はセクション3に記載されています。
BanditRank follows the listwise approach by treating a query and the corresponding candidate documents as a single instance for training. 
**BanditRankは、クエリと対応する候補文書をトレーニングのための単一のインスタンスとして扱うリストワイズアプローチに従います**。
((x, a)じゃなくて(x, A)を1つのトレーニングサンプルとして使うってこと??:thinking:)
BanditRank is extensible in the sense that it provides a methodology for training neural networks using reinforcement learning for ranking. 
BanditRankは、**ランキングのために強化学習を使用してニューラルネットワークを訓練するための方法論を提供**するという意味で拡張可能です。
(任意のニューラルネットを強化学習ベースでLearning For Rankできる手法を提案してるよ、って話:thinking:)
Therefore, it can be used with any text-matching architecture for feature extraction and jointly trained or it can use the features extracted from a pre-trained model. 
したがって、特徴抽出のために任意のテキストマッチングアーキテクチャと共に使用することができ、共同訓練することも、事前訓練されたモデルから抽出された特徴を使用することもできます。
For example, the LETOR 4.0 dataset(Qin and Liu,2013)provides 46-dimensional feature vectors corresponding to each query-document pair that can be leveraged directly for training. 
例えば、LETOR 4.0データセット（Qin and Liu, 2013）は、各クエリ-文書ペアに対応する46次元の特徴ベクトルを提供し、これを直接訓練に活用できます。
Since BanditRank is a deep learning method, it is also extensible with respect to the choice of architectures that can be used. 
**BanditRankは深層学習手法であるため、使用できるアーキテクチャの選択に関しても拡張可能**です。
We focused on offline ranking tasks in which external relevance labels are provided for training. 
私たちは、**外部の関連性ラベルが訓練のために提供されるオフラインランキングタス**クに焦点を当てました。

<!-- ここまで読んだ! -->

Empirically, we prove that BanditRank is superior when compared to other strong baselines. 
経験的に、私たちはBanditRankが他の強力なベースラインと比較して優れていることを証明します。
We conducted a series of experiments on three datasets in the domains of question answering and web search. 
私たちは、質問応答とウェブ検索の分野で3つのデータセットに対して一連の実験を実施しました。
The major contributions of this paper are summarized as follows: 
この論文の主な貢献は以下のように要約されます：

- •For training neural networks by directly optimizing evaluation measures using gradient descent algorithms, we formulate the ranking problem as a contextual bandit and introduce a new deep learning method called BanditRank for ranking. 
- •評価指標を直接最適化するために勾配降下アルゴリズムを使用してニューラルネットワークを訓練するために、ランキング問題をコンテキストバンディットとして定式化し、ランキングのための新しい深層学習手法BanditRankを導入します。

- •To the best of our knowledge, BanditRank is the first listwise deep learning method that uses reinforcement learning to train neural networks for offline ranking purposes. 
•私たちの知る限り、**BanditRankはオフラインランキングの目的でニューラルネットワークを訓練するために強化学習を使用する最初のリストワイズ深層学習手法**です。
We enabled this by introducing a hybrid training objective in order to solve the exploration problem when the number of possible actions is large. 
私たちは、可能なアクションの数が多いときの探索問題を解決するためにハイブリッドトレーニング目的を導入することでこれを実現しました。

- •BanditRank provided state-of-the-art results when applied on both InsuranceQA(Feng etal.,2015) and WikiQA(Yang etal.,2015) datasets outperforming the previous best method at the time of writing of this paper. 
•BanditRankは、InsuranceQA（Feng et al., 2015）およびWikiQA（Yang et al., 2015）データセットの両方に適用された際に最先端の結果を提供し、この論文執筆時点での以前の最良の方法を上回りました。

- •In the web-search task, when applied on the benchmark MQ2007(Qin and Liu,2013) dataset using only the provided 46-dimensional features, BanditRank achieved better results than the state-of-the-art learning-to-rank algorithm LambdaMART(Burges,2010) and clearly outperformed other listwise baselines such as CoordinateAscent(Metzler and Croft,2007), ListNet(Cao etal.,2007), and AdaRank(Xu and Li,2007). 
•ウェブ検索タスクにおいて、提供された46次元の特徴のみを使用してベンチマークMQ2007（Qin and Liu, 2013）データセットに適用した場合、BanditRankは最先端の学習ランキングアルゴリズムLambdaMART（Burges, 2010）よりも優れた結果を達成し、CoordinateAscent（Metzler and Croft, 2007）、ListNet（Cao et al., 2007）、およびAdaRank（Xu and Li, 2007）などの他のリストワイズベースラインを明確に上回りました。

The remainder of the paper is structured as follows. 
論文の残りの部分は以下のように構成されています。
In the next section, we briefly discuss related studies. 
次のセクションでは、関連研究について簡単に説明します。
In Section3, we give the formulation of ranking as a contextual bandit. 
セクション3では、ランキングをコンテキストバンディットとして定式化します。
In Section4, we provide the details of the model architecture used for our experiments. 
セクション4では、私たちの実験に使用したモデルアーキテクチャの詳細を提供します。
We explain the experiments we conducted along with a comparative study of rewards in Section5. 
セクション5では、私たちが実施した実験と報酬の比較研究について説明します。
We conclude the paper in Section6. 
セクション6で論文を締めくくります。

<!-- ここまで読んだ! -->

## 2.Related Work 関連研究

BanditRank is similar to BanditSum(Dong etal.,2018), which was proposed earlier for extractive summarization tasks in NLP. 
**BanditRankは、NLPにおける抽出的要約タスクのために以前に提案されたBanditSum(Dong et al., 2018)に似ています**。(へぇ〜！)
BanditSum introduces a theoretically grounded method based on contextual bandit formalism for training neural-network-based summarizers with reinforcement learning. 
BanditSumは、強化学習を用いてニューラルネットワークベースの要約器を訓練するための文脈バンディット形式に基づいた理論的に根拠のある方法を導入します。
We have adapted the formulation of ranking as a contextual bandit from that of BanditSum. 
私たちは、BanditSumの文脈バンディットとしてのランキングの定式化を適応しました。
Adaptation of the contextual bandit framework to the ranking problem is not straightforward at all, for example, a naive application of BanditSum suffers from inadequate exploration when the number of actions is very large which is prevalent in ranking tasks. 
**文脈バンディットフレームワークをランキング問題に適応することは全く簡単ではなく**、例えば、BanditSumの単純な適用は、ランキングタスクで一般的なアクションの数が非常に大きい場合に不十分な探索に悩まされます。
Thus we propose the use of hybrid loss for leveraging the feedback from a supervised loss function as explained in Section3.4. 
したがって、セクション3.4で説明するように、**教師あり損失関数からのフィードバックを活用するためにハイブリッド損失の使用を提案**します。
(なるほど...!DR推定量っぽい目的関数を学習に使うのかな??:thinking:)
Reinforcement learning was used for directly optimizing measures such as BLEU(Papineni etal.,2002)and ROUGE(Lin,2004)in different tasks of natural language processing such as summarization and sequence prediction(Paulus etal.,2017; Lee and Lee,2017; Ranzato etal.,2015; Bahdanau etal.,2016). 
強化学習は、要約や系列予測(Paulus et al., 2017; Lee and Lee, 2017; Ranzato et al., 2015; Bahdanau et al., 2016)などの自然言語処理のさまざまなタスクにおいて、BLEU(Papineni et al., 2002)やROUGE(Lin, 2004)などの指標を直接最適化するために使用されました。

<!-- ここまで読んだ! -->

In the domain of learning-to-rank for IR, MDPRank(Wei etal.,2017)uses reinforcement learning for ranking by formulating ranking as a sequential decision process. 
情報検索のための学習ランキングの分野では、MDPRank(Wei et al., 2017)がランキングを逐次的な意思決定プロセスとして定式化することで、強化学習を使用してランキングを行います。
Since the sequential models are affected by the order of the decisions, they may be biased towards selecting documents with low relevance level at the beginning. 
逐次モデルは意思決定の順序に影響されるため、最初に関連性の低い文書を選択するバイアスがかかる可能性があります。
MDPRank is not suitable for training neural networks because a model with only 46 weight parameters requires more than 10000 epochs for convergence. 
MDPRankは、46の重みパラメータしか持たないモデルが収束するために10000エポック以上を必要とするため、ニューラルネットワークの訓練には適していません。
In contrast, BanditRank is suitable for deep architectures, and all the best results of BanditRank were achieved in less than 30 epochs of training. 
対照的に、BanditRankは深層アーキテクチャに適しており、BanditRankのすべての最良の結果は30エポック未満の訓練で達成されました。
Another issue with the setting of MDPRank is that the number of possible rankings for a query $q$ with $n_q$ number of candidate documents is $n_q!$, which is quite large making exploration more difficult. 
MDPRankの設定に関する別の問題は、$n_q$ 個の候補文書を持つクエリ $q$ の可能なランキングの数が $n_q!$ であり、これは非常に大きく、探索をより困難にすることです。
In contrast, BanditRank has more flexibility and freedom to explore the search space, as it samples a fixed number of documents $M$ without replacement based on the affinity scores during training, reducing the search space to $P_{M} n_q << n_q!$ for small $M$. 
**対照的に、BanditRankは、訓練中に親和性スコアに基づいて固定数の文書 $M$ を置換なしでサンプリングするため、探索空間を小さな $M$ に対して $P_{M} n_q << n_q!$ に減少させる柔軟性と自由度を持っています。**
This is because BanditRank uses listwise approach by treating all the candidate documents corresponding to a query as a single state. 
これは、BanditRankがクエリに対応するすべての候補文書を単一の状態として扱うリストワイズアプローチを使用しているためです。
The policy gradient algorithm was also used to train the generator of IRGAN(Wang etal.,2017b), but the rewards for the generator depend on the scoring function learned by the discriminator. 
ポリシー勾配アルゴリズムは、IRGAN(Wang et al., 2017b)の生成器を訓練するためにも使用されましたが、生成器への報酬は識別器によって学習されたスコアリング関数に依存します。
The training of IRGAN is similar to that of SeqGAN(Yu etal.,2017), which is based on the idea of using the policy gradient algorithm for tackling the generator differentiation problem due to the discrete outputs produced by the generator. 
IRGANの訓練は、生成器によって生成される離散出力による生成器の微分問題に対処するためにポリシー勾配アルゴリズムを使用するというアイデアに基づくSeqGAN(Yu et al., 2017)の訓練に似ています。
Both Bandits(Radlinski etal.,2008; Kveton etal.,2015; Katariya etal.,2016)and MDPs(Zeng etal.,2018)were used to model the interactive process between a search engine and user with the user providing implicit relevance feedback. 
Bandits(Radlinski et al., 2008; Kveton et al., 2015; Katariya et al., 2016)とMDPs(Zeng et al., 2018)の両方が、ユーザが暗黙の関連フィードバックを提供する検索エンジンとユーザ間のインタラクティブプロセスをモデル化するために使用されました。
An overview of approaches that use reinforcement learning for different IR tasks such as query reformulation, recommendation and session search can be found in a previous paper(Zhao etal.,2018). 
クエリの再定式化、推薦、セッション検索などのさまざまなIRタスクに対して強化学習を使用するアプローチの概要は、以前の論文(Zhao et al., 2018)に見られます。
BanditRank’s action is similar to the formulation of ListNet(Cao etal.,2007), which is based on the permutation of the input documents. 
BanditRankのアクションは、入力文書の順列に基づくListNet(Cao et al., 2007)の定式化に似ています。
However, both approaches differ with respect to the training method and structure of the probability model used. 
しかし、両方のアプローチは、使用される訓練方法と確率モデルの構造に関して異なります。

<!-- ここまで読んだ! -->

## 3.BanditRank Formulation 3. BanditRankの定式化

We formulate ranking as a contextual bandit trained using policy gradient reinforcement learning. 
私たちは、ランキングをポリシー勾配強化学習を用いて訓練されたコンテキストバンディットとして定式化します。
A bandit is a decision-making algorithm in which an agent repeatedly chooses one out of several actions and receives a reward based on this choice. 
バンディットとは、エージェントが複数のアクションの中から1つを繰り返し選択し、その選択に基づいて報酬を受け取る意思決定アルゴリズムです。
The goal of the agent is to maximize the cumulative reward it achieves by learning the actions that yield good rewards. 
エージェントの目標は、良い報酬をもたらすアクションを学習することによって得られる累積報酬を最大化することです。
The term agent is generally used to refer to an entity or model that interacts with the environment. 
**「エージェント」という用語は、一般的に環境と相互作用するエンティティまたはモデルを指します**。(お、いい定義！引用しやすそう...!:thinking:)
Contextual Bandit is a variant of the bandit problem that conditions its action on the context or state of the environment and observes the reward for the chosen action only. 
コンテキストバンディットは、アクションを環境のコンテキストまたは状態に条件付け、選択されたアクションに対する報酬のみを観察するバンディット問題のvariantです。
It forms a subclass of Markov decision processes with the length of each episode being one. 
これは、**各エピソードの長さが1であるマルコフ決定過程のサブクラス(=contexual banditと言えるってことか...!:thinking:)**を形成します。
Formally, assume there is an environment with context space $X$ and action space $A$. 
形式的には、コンテキスト空間 $X$ とアクション空間 $A$ を持つ環境があると仮定します。
The agent interacts with the environment in a series of time steps. 
エージェントは、一連の時間ステップで環境と相互作用します。
At each time step $t$, the agent observes a context $x_t \in X$, chooses an action $a_t \in A$, and observes a reward for that action $r(a_t)$. 
各時間ステップ $t$ において、エージェントはコンテキスト $x_t \in X$ を観察し、アクション $a_t \in A$ を選択し、そのアクションに対する報酬 $r(a_t)$ を観察します。
The goal of the agent is to maximize the cumulative rewards it achieves over a certain period. 
エージェントの目標は、特定の期間にわたって得られる累積報酬を最大化することです。

<!-- ここまで読んだ! -->

Now, we can formulate the ranking problem as a contextual bandit with the environment being the dataset of queries and documents. 
さて、私たちは、ランキング問題をクエリと文書のデータセットを環境とするコンテキストバンディットとして定式化できます。
The set of query-document pairs corresponding to a single query is treated as a context, and each permutation of the candidate documents is treated as a different action. 
単一のクエリに対応するクエリ-文書ペアの集合はコンテキストとして扱われ、**候補文書の各順列は異なるアクションとして扱われます**。
(やっぱり期待通り、本論文の手法BanditRankは、単一文書じゃなくて文書順列をアクションとして扱うのか...!:thinking:)
Formally, given a query $q$ and its candidate documents $d=\{d_1,d_2,\ldots,d_{n_q}\}$, each context is the set $c=\{(q,d_1),(q,d_2),\ldots,(q,d_{n_q})\}$. 
形式的には、クエリ $q$ とその候補文書 $d=\{d_1,d_2,\ldots,d_{n_q}\}$ が与えられたとき、各コンテキストは集合 $c=\{(q,d_1),(q,d_2),\ldots,(q,d_{n_q})\}$ です。
Where $n_q$ is the number of candidate documents of $q$, and the cardinality of $c$ is given by $n_c=n_q$. 
ここで、$n_q$ は $q$ の候補文書の数であり、$c$ の基数は $n_c=n_q$ で与えられます。
Given $c$, the action of the agent is given by the permutation $a_c=(d_{k_1},d_{k_2},\ldots,d_{k_{n_q}})$ of the candidate documents, where $k_t \in \{1,2,\ldots,n_q\}$ and $k_t \neq k_{t'}$ for $t \neq t'$. 
$c$ が与えられたとき、エージェントのアクションは候補文書の順列 $a_c=(d_{k_1},d_{k_2},\ldots,d_{k_{n_q}})$ で与えられ、ここで $k_t \in \{1,2,\ldots,n_q\}$ であり、$t \neq t'$のとき$k_t \neq k_{t'}$ です。
The reward is given by a scalar function $R(a_c,g_c)$ that takes action $a_c$ and the ground-truth permutation $g_c$ corresponding to $c$ as the input. 
報酬は、アクション $a_c$ とコンテキスト $c$ に対応する真の順列 $g_c$ を入力として受け取るスカラー関数 $R(a_c,g_c)$ によって与えられます。
($g_c$ は未知の最適な順列って認識でOKそう??:thinking:)
The $g_c$ is nothing but the candidate documents sorted in descending order according to their relevance levels. 
$g_c$ は、関連性レベルに従って降順にソートされた候補文書に他なりません。
The notation $R$ is a scalar reward function defined using a combination of measures such as MAP and MRR. 
記号 $R$ は、MAPやMRRなどの指標の組み合わせを使用して定義されたスカラー報酬関数です。

<!-- ここまで読んだ! -->

The action taken by the agent is determined by its policy. 
エージェントが取るアクションは、そのポリシーによって決定されます。
In the current formulation, a policy is a neural network $p_{\theta}(.|c)$ parameterized by $\theta$. 
現在の定式化において、ポリシーは $\theta$ でパラメータ化されたニューラルネットワーク$p_{\theta}(.|c)$です。
For each input $c$, $p_{\theta}(.|c)$ encodes a probability distribution over permutations of the candidate documents. 
各入力 $c$ に対して、$p_{\theta}(.|c)$ は候補文書の順列に対する確率分布をエンコードします。(うんうん、この辺りの定義・認識は「反実仮想機械学習」とも同じだ...!:thinking:)
The goal is to find $\theta$ that cause the network to assign high probability to the permutations, which can yield good rewards induced by $R$. 
目標は、ネットワークが高い確率を順列に割り当てるようにする $\theta$ を見つけることであり、これにより$R$によって誘発される良い報酬を得ることができます。
This can be achieved by maximizing the following objective function with respect to $\theta$: 
これは、$\theta$に関して以下の目的関数を最大化することによって達成できます：

$$
J(\theta) = \mathbb{E}[R(a_c,g_c)]
\text{(1)}
$$

(上式だと、何に対する期待値かが明示されてないけど、今回の場合だと多分 $E_{p(c, g_c, a_c)}$ みたいな感じかな...!:thinking:)
where the expectation is taken over $c$ paired with $g_c$ and $a_c$ generated according to $p_{\theta}(.|c)$. 
ここで期待値は、$g_c$ と $p_{\theta}(.|c)$ に従って生成された $a_c$ とペアになった $c$ に対して取られます。
(やっぱり! じゃあ上の式は、$E_{p(c, g_c, a_c)}[R(a_c,g_c)]$ ってことで合ってるね...!:thinking:)
The above objective function is a standard objective function used in the reinforcement-learning domain, which maximizes the expected reward. 
上記の目的関数は、期待報酬を最大化する強化学習分野で使用される標準的な目的関数です。
(うんうん、報酬関数の環境における期待値の最適化はシンプル...!:thinking:)
The negative of the expectation can be treated as the loss function. 
期待値の負は損失関数として扱うことができます。
(うんうん、実装の都合上、最小化タスクに変換する方がやりやすいから...!:thinking:)

<!-- ここまで読んだ! -->

### 3.1. Structure of Policypθ(.|c) 

(アクション選択確率分布を出力する関数、どんな構造にするねん、という話...!:thinking:)

The exact action of the agent depends on the chosen structure of $p_{\theta}(.|c)$. 
エージェントの正確な行動は、選択された $p_{\theta}(.|c)$ の構造に依存します。
We follow the approach used for extractive summarization (Dong et al., 2018) because of its simplicity and effectiveness. 
私たちは、その単純さと効果性のために、抽出的要約（Dong et al., 2018）で使用されるアプローチに従います。
With this approach, $p_{\theta}(.|c)$ is decomposed into a deterministic function $\pi_{\theta}$, which contains all the network’s parameters, and $\mu$, a probability distribution induced by the output of $\pi_{\theta}$ defined as
このアプローチでは、$p_{\theta}(.|c)$ は、**ネットワークのすべてのパラメータを含む決定論的関数 $\pi_{\theta}$ と、$\pi_{\theta}$ の出力によって誘導される確率分布$\mu$に分解されます**。
(5章まで読んだメモ: $\pi_{\theta}$ は親和性スコアベクトルを出力する。言い換えると、各文書をアクションとみなした場合のアクション選択確率分布を出力する関数のイメージ! 一方で、$\mu$ は、文書順列をアクションとみなした場合のアクション選択確率分布を出力する関数のイメージ...!:thinking:)

$$
p_{\theta}(.|c) = \mu(.|\pi_{\theta}(c))
\text{(2)}
$$

Provided a $c$ corresponding to a $q$, the network $\pi_{\theta}$ outputs a real valued vector of document affinities within the range $[0,1]$. 
$q$ に対応する $c$ が与えられると、ネットワーク $\pi_{\theta}$ は、範囲$[0,1]$内の**文書の親和性の実数値ベクトルを出力**します。
The length of the vector is equal to the number of candidate documents $n_{c}$ corresponding to $q$, i.e., $\pi_{\theta}(c) \in \mathbb{R}^{n_{c}}$. 
ベクトルの長さは、$q$ に対応する候補文書の数 $n_{c}$に等しく、すなわち、$\pi_{\theta}(c) \in \mathbb{R}^{n_{c}}$ です。
The affinity score of a document $d_{i}$ given by $\pi_{\theta}(c)$ isubscript $\pi_{\theta}(c)_{i}$ represents the network’s propensity to keep the document at the top position in the output permutation. 
$\pi_{\theta}(c)$ によって与えられる各文書 $d_{i}$ の親和性スコアは、出力の順列で文書を上位に保持するネットワークの傾向を表します。
Specifically, the interpretation of the affinity scores is highly dependent upon the type of reward signal used. 
**具体的には、親和性スコアの解釈は、使用される報酬信号の種類に大きく依存します**。
For example, if only Precision@1 is used as the reward signal, the focus of the network would mainly be on the permutations that contain a relevant document at the first position. 
例えば、Precision@1のみが報酬信号として使用される場合、ネットワークの焦点は主に最初の位置に関連文書を含む順列に置かれます。

Provided the above document affinities $\pi_{\theta}(c)$, $\mu$ implements a process of repeated sampling without replacement by repeatedly normalizing the set of affinities of documents not yet selected. 
上記の文書親和性 $\pi_{\theta}(c)$ が与えられると、$\mu$ は、まだ選択されていない文書の親和性のセットを繰り返し正規化することによって、**置換なしの繰り返しサンプリング**のプロセスを実装します。(=これは要するに、プラケットルースモデルと同じ操作だな...!:thinking:)
In total, $M$ unique documents are sampled yielding an ordered subset of the candidate documents. 
合計で、$M$ のユニークな文書がサンプリングされ、候補文書の順序付けられた部分集合が得られます。
For exploring the action space, a small probability $\epsilon$ of sampling uniformly from all remaining documents is included at each step of the sampling. 
**アクション空間を探索するために、サンプリングの各ステップで残りのすべての文書から均等にサンプリングする小さな確率 $\epsilon$ が含まれます**。(あ、なるほど。プラケットルースモデルとepsilon-greedy手法の合わせ技なのか...!:thinking:)
This is similar to the $\epsilon$-greedy technique generally used in the reinforcement learning problems for exploration. 
これは、探索のために強化学習の問題で一般的に使用される$\epsilon$-greedy手法に似ています。
According to the prescribed definition of $\mu$, the probability $p_{\theta}(a_{c}|c)$ of producing a permutation $a_{c}$ corresponding to $c$ according to (2) is given by
$\mu$ の定義に従って、(2)に従って $c$ に対応する順列 $a_{c}$ を生成する確率 $p_{\theta}(a_{c}|c)$ は次のように与えられます。
(以下が $\mu$ の中身...!:thinking:)

$$
p_{\theta}(a_{c}|c) = \prod_{i=1}^{M} (
    \frac{\epsilon}{n_{c}-i+1} +
    \frac{(1-\epsilon)\pi_{\theta}(c)_{k_{i}}}{z(c) - \sum_{l=1}^{i-1}\pi_{\theta}(c)_{k_{l}}}
)
\text{(3)}
$$

(プラケットルースモデルによるアクション選択確率分布って、こんなにわかりやすい式で定式化できるのか...! $z(c)$ を導入してるからかな...!:thinking:)
where $k_{t}$ is the index to the $t$-th document in $a_{c}$, $d_{k_{t}}$ and $z(c)=\sum_{m=1}^{n_{c}}\pi_{\theta}(c)_{m}$.
ここで、$k_{t}$ は、$a_{c}$ の$t$番目の文書のインデックスであり、$d_{k_{t}}$ はその文書を表します。また、$z(c)=\sum_{m=1}^{n_{c}}\pi_{\theta}(c)_{m}$ (i.e. z(c)は、コンテキスト$c$における候補文書の親和性スコアの合計)です。
We define $M=\min(n_{c},M')$, where $M'$ is an integer hyper parameter that depends on the environment or dataset. 
私たちは、$M=\min(n_{c},M')$ と定義します。ここで、$M'$ は環境またはデータセットに依存する整数ハイパーパラメータです。
This sampling method with exploration is followed only during training time. 
**この探索を伴うサンプリング手法は、トレーニング時のみ適用されます**。(ん？？本番システムでの推論時でも適用されるはずだよね!:thinking:)
At test time, we output all the candidate documents sorted in descending order according to their affinity scores. 
テスト時には、親和性スコアに基づいて降順にソートされたすべての候補文書を出力します。(あ、これはオフライン評価時には、って話なのかな。別にオフライン評価時にも、探索も含めて良い気がする...!:thinking:)

<!-- ここまで読んだ! -->

### 3.2.Policy Gradient Reinforcement Learning

(どうパラメータ更新するかという話:thinking:)
The gradient of the objective function (1) cannot be calculated directly as $a_{c}$ is discretely sampled while calculating $R(a_{c},g_{c})$.  
目的関数(1)の勾配は、$R(a_{c},g_{c})$ を計算する際に $a_{c}$ が**離散的にサンプリングされるため、直接計算することはできません**。(あ、だから方策性能ではなく方策勾配を推定するする必要があったのか...! 勾配効果法を使えるようにするために...!:thinking:)
This is a common situation in most reinforcement-learning tasks.  
これはほとんどの強化学習タスクにおいて一般的な状況です。
However, the gradient of the objective function can be calculated after a reformulation of the expectation term according to the REINFORCE algorithm (Williams, 1992; Sutton et al., 2000).  
しかし、目的関数の勾配は、REINFORCEアルゴリズム（Williams, 1992; Sutton et al., 2000）に従って期待値項を再定式化した後に計算できます。
It tells us that the gradient of that function can be calculated using the following equation:  
それは、その関数の勾配が次の式を使用して計算できることを示しています：

$$
方策勾配の定義式
\text{(4)}
$$

where the expectation is over the same variables as (1).  
ここで、期待値は(1)と同じ変数に対して計算されます。
Given a context-true permutation pair $(c,g_{c})$ sampled from the dataset or environment $D(c,g_{c})$, the gradient can be derived using the following reformulation of the expectation in (1):
データセットまたは環境$D(c,g_{c})$からサンプリングされたコンテキスト真の順列ペア$(c,g_{c})$が与えられた場合、勾配は(1)の期待値の次の再定式化を使用して導出できます：

$$
方策勾配の定義式を展開して変形...
\text{(5)}
$$

$$
方策勾配の定義式を展開して変形...2
\text{(6)}
$$

Step (5) follows from the definition of expectation for discrete quantities and the linearity of the gradient operator.  
ステップ(5)は、離散量に対する期待値の定義と勾配演算子の線形性に従います。
Step (6) is the reformulation of the gradient term, which is an important step in the derivation initially given by the REINFORCE (Williams, 1992) algorithm.  
ステップ(6)は勾配項の再定式化であり、これはREINFORCE（Williams, 1992）アルゴリズムによって最初に与えられた導出において重要なステップです。
The expectation in (4) is empirically calculated by first sampling a context-true permutation pair $(c,g_{c})$, sampling $B$ permutations $a_{c}^{1},a_{c}^{2},\ldots,a_{c}^{B}$ from $p_{\theta}(.|c)$ using the sampling method mentioned in Section 3.1, and finally taking the average.  
(4)の期待値は、まずコンテキスト真の順列ペア $(c,g_{c})$ をサンプリングし、次にセクション3.1で言及されたサンプリング方法を使用して$p_{\theta}(.|c)$から$B$個の順列$a_{c}^{1},a_{c}^{2},\ldots,a_{c}^{B}$をサンプリングし、最後に平均を取ることによって経験的に計算されます。
Empirically, the inner expectation of (4) is given by  
経験的に、(4)の内部期待値は次のように与えられます：

$$
方策勾配の推定量の定義式っぽいやつ!
\text{(7)}
$$

The number $B$ is also an integer hyperparameter that mainly depends on the dataset.  
数 $B$ は、主にデータセットに依存する整数ハイパーパラメータでもあります。(=ランキングの長さ??:thinking:)
Given the expression for $p_{\theta}(a_{c}|c)$ (3), the gradient (7) can be calculated by any automatic differentiation package.  
**$p_{\theta}(a_{c}|c)$の式(3)が与えられた場合、勾配(7)は任意の自動微分パッケージによって計算できます**。
As mentioned in Section 3.1, we sample $M=\min(n_{c},M')$ number of documents from the candidate documents during training time.  
セクション3.1で述べたように、トレーニング時に候補文書から$M=\min(n_{c},M')$個の文書をサンプリングします。
Therefore, we take reward feedback from an $M$-length ordered subset.  
したがって、$M$長の順序付きサブセットから報酬フィードバックを取得します。
Since we cannot efficiently explore the whole action space for large $M$, as the number of possible actions or permutations would then become $P_{M}^{n_{c}}$, we choose $M$ based on the average number of relevant documents per query in the dataset.  
大きな$M$に対して全アクション空間を効率的に探索できないため、可能なアクションや順列の数が$P_{M}^{n_{c}}$になるため、データセット内の各クエリに対する関連文書の平均数に基づいて$M$を選択します。
The $B$ determines the exact number of actions we explore for each context during each epoch, which can be seen from the approximation in (7).  
$B$は、各エポック中に各コンテキストに対して探索するアクションの正確な数を決定し、これは(7)の近似から見ることができます。
In our experiments, we obtained very good results even though $B$ was set to be small, i.e., $B=20$ or $B=30$.  
**私たちの実験では、$B$が小さく設定されていても、非常に良い結果を得ることができました。すなわち、$B=20$または$B=30$です**。

The gradient estimate in (7) is prone to have high variance (Sutton et al., 2000).  
**(7)の勾配推定は高い分散を持つ傾向があります**（Sutton et al., 2000）。(アクション空間が広すぎるから...!:thinking:)
Moreover, all target measures, such as MAP, MRR, and nDCG, are always non-negative, which increases the probability of every sampled permutation according to the objective function.  
さらに、MAP、MRR、nDCGなどのすべてのターゲット指標は常に非負であり、これは目的関数に従ってサンプリングされた順列の確率を増加させます。
We would prefer the probability of a bad permutation in terms of reward should be decreased.
報酬の観点から悪い順列の確率が減少することを望みます。
We use a baseline function, which is subtracted from all rewards.  
私たちは、**すべての報酬から引かれるベースライン関数を使用**します。
This decreases the variance of the estimate by acting as an advantage function, and it ensures that the permutations with low rewards receive negative rewards.  
これにより、**推定の分散がアドバンテージ関数として機能することによって減少し、低い報酬を持つ順列が負の報酬を受け取ることが保証されます**。
If chosen appropriately, the advantage function can significantly reduce the variance of the estimate (Sutton et al., 2000) without biasing the estimate.  
適切に選択されれば、アドバンテージ関数は推定のバイアスをかけることなく、推定の分散を大幅に減少させることができます（Sutton et al., 2000）。(DR推定量みたいな考え方っぽい...!!:thinking:)
Using a baseline $r_{base}$, the sample-based estimate (7) becomes  
ベースライン $r_{base}$ を使用すると、サンプルベースの推定(7)は次のようになります：

$$
方策勾配のDR推定量っぽい式!
\text{(8)}
$$

For choosing the baseline function, we follow the terminology of self-critical reinforcement learning, in which the test time performance of the current model is used as the baseline (Dong et al., 2018; Ranzato et al., 2015; Paulus et al., 2017; Rennie et al., 2017).  
ベースライン関数を選択するために、自己批判的強化学習の用語に従い、**現在のモデルのテスト時のパフォーマンスをベースラインとして使用します**（Dong et al., 2018; Ranzato et al., 2015; Paulus et al., 2017; Rennie et al., 2017）。
(DR推定量における期待報酬関数に、現在学習しようとしてるモデルを採用する、ってこと...??:thinking:)
Therefore, while calculating the gradient estimate (8) after sampling the context-true permutation pair $(c,g_{c})$, we greedily generate a permutation using the current model similar to the test time action.  
したがって、コンテキスト真の順列ペア $(c,g_{c})$ をサンプリングした後に勾配推定(8)を計算する際、テスト時のアクションに似た現在のモデルを使用して貪欲に順列を生成します。
The baseline for $a_{c}$ is then calculated by setting $r_{base}=R(a_{c}^{greedy},g_{c})$.  
したがって、$a_{c}$ のベースラインは $r_{base}=R(a_{c}^{greedy},g_{c})$ を設定することによって計算されます。
Therefore, all the permutations with reward greater than the greedy permutation receive positive rewards and other permutations receive negative rewards.  
したがって、貪欲な順列よりも報酬が大きいすべての順列は正の報酬を受け取り、他の順列は負の報酬を受け取ります。
The baseline is also intuitive in the way that it is different for different contexts.  
**ベースラインは、異なるコンテキストに対して異なるという点でも直感的**です。(まさにDR推定量だな:thinking:)

<!-- ここまで読んだ! -->

### 3.3. Reward Function R𝑅R 報酬関数 R

As mentioned earlier, the reward function can be a single target measure or a combination of several measures. 
前述のように、報酬関数は単一のターゲット測定値であるか、いくつかの測定値の組み合わせである可能性があります。
For the question answering datasets, the following reward function was used: 
質問応答データセットでは、次の報酬関数が使用されました：

$$
\text{(10)}
$$

For the web search dataset, the following reward function was used: 
ウェブ検索データセットでは、次の報酬関数が使用されました：

$$
\text{(11)}
$$

where the measures average precision (AP), reciprocal rank (RR), and nDCG@10 are traditional IR measures. 
ここで、平均適合率（AP）、逆順位（RR）、およびnDCG@10は、従来の情報検索（IR）指標です。
In the experiments section, we also provide a simple comparison of different reward functions on the web search dataset. 
実験セクションでは、ウェブ検索データセットにおける異なる報酬関数の簡単な比較も提供します。
(g_cって未知じゃんって思ってたけど、普通にMAPとかnDCGを計算したら良いのか:thinking:)

<!-- ここまで読んだ! -->

### 3.4. ハイブリッドトレーニング目的

As mentioned in the Section3.2, the problem of exploring the action space when $M$ is large can be tackled using a hybrid loss, which is a combination of the reinforcement learning loss and a standard supervised learning loss such as binary cross entropy. 
セクション3.2で述べたように、$M$ が大きいときのアクション空間を探索する問題は、強化学習損失とバイナリ交差エントロピーのような標準的な教師あり学習損失の組み合わせであるハイブリッド損失を使用して対処できます。
The supervised loss can guide the training initially when the exploration by the model is in the starting stages for large $M$. 
**教師あり損失は、モデルによる探索が大きな$M$の初期段階にあるときに、最初にトレーニングをガイドすることができます**。(あ、これが3.2で言ってたベースライン関数なのか??じゃあこのハイブリッドhogehogeっていう手法は、DR推定量のことだと思って良さそう...?? でも下を見るとまた別で損失関数に項を追加してるっぽい...!:thinking:)
Even though the number of actions explored with the model at each epoch given by $B$ is small for large $M$, i.e., $B \ll P_{M}$, a supervised signal can help the model by compensating the loss incurred due to the inefficient exploration. 
大きな$M$に対して、各エポックでモデルによって探索されるアクションの数は$B$によって与えられ、小さいですが、すなわち、$B \ll P_{M}$、教師あり信号は非効率的な探索によって発生した損失を補うことでモデルを助けることができます。
The hybrid loss function is given as follows: 
ハイブリッド損失関数は次のように与えられます：

$$
L_{hybrid} = L_{rl} + \gamma L_{sl}
$$

where $L_{rl}$ is the loss given by the reinforcement-learning algorithm, which is the negative of (1), and $L_{sl}$ is a supervised loss such as binary cross entropy. 
ここで、$L_{rl}$は強化学習アルゴリズムによって与えられる損失であり、(1)の負の値であり、$L_{sl}$はバイナリ交差エントロピーのような教師あり損失です。(あれ、ベースライン関数を使ったDR推定量とはまた違う話っぽい??:thinking:)
The notation $\gamma$ is a scaling factor accounting for the difference in magnitude between $L_{rl}$ and $L_{sl}$. 
記号$\gamma$は、$L_{rl}$と$L_{sl}$の間の大きさの違いを考慮したスケーリングファクターです。
It is a hyperparameter lying between 0 and 1. 
これは0と1の間にあるハイパーパラメータです。
We found the hybrid loss to be effective in the case of the web search dataset where the average number of relevant documents per query was equal to 10.3. 
私たちは、平均的な関連文書数が10.3であるウェブ検索データセットの場合にハイブリッド損失が効果的であることを発見しました。
Since we use binary cross entropy as the supervised loss, the hybrid training objective is a blend of the pointwise objective function $L_{sl}$ and a listwise objective function $L_{rl}$. 
私たちはバイナリ交差エントロピーを教師あり損失として使用しているため、ハイブリッドトレーニング目的は、ポイントワイズ目的関数$L_{sl}$とリストワイズ目的関数$L_{rl}$のブレンドです。
The hybrid training objective still has direct control over the target measures weighted by $\gamma$. 
ハイブリッドトレーニング目的は、$\gamma$で重み付けされたターゲット測定に対して直接的な制御を持っています。
Similar hybrid loss was used in the domain of NLP in some papers, e.g., (Paulus et al., 2017; Wu et al., 2016). 
類似のハイブリッド損失は、いくつかの論文（例：Paulus et al., 2017; Wu et al., 2016）においてNLPの分野で使用されました。

<!-- ここまで読んだ! -->

## 4.Model Architecture モデルアーキテクチャ

(context-候補ドキュメント一覧を入力として受け取り、各ドキュメントをアクションとみなした場合のアクション選択確率分布を出力する関数 $\pi_{\theta}$ の構造について...!:thinking:)
(もしかすると必ずしも確率質量関数の定義を満たすような形にはなってないかも。最終的に $p_{\theta}(.|c)$ が確率質量関数になってれば良いはずなので...!:thinking:)

In this section, we discuss the neural architecture $\pi_{\theta}$ we used in our experiments. 
このセクションでは、私たちの実験で使用したニューラルアーキテクチャ $\pi_{\theta}$ について説明します。
For demonstrating the extensibility of BanditRank, we considered two scenarios for the experiments and show that BanditRank performs well in both the scenarios.
BanditRankの拡張性を示すために、私たちは実験のために2つのシナリオを考慮し、BanditRankが両方のシナリオでうまく機能することを示します。

<!-- ここまで読んだ! -->

### Scenario 1 シナリオ1

In this scenario, we decomposed $\pi_{\theta}$ into two neural network architectures $f_{\theta 1}$ and $b_{\theta 2}$; $f_{\theta 1}$ for extracting the feature vectors from raw texts of query or documents and $b_{\theta 2}$ for a bandit network that yields the document affinities. 
このシナリオでは、$\pi_{\theta}$ を2つのニューラルネットワークアーキテクチャ$f_{\theta 1}$と$b_{\theta 2}$ に分解しました。$f_{\theta 1}$ はクエリや文書の生テキストから特徴ベクトルを抽出するためのものであり、$b_{\theta 2}$ は文書の親和性を生成するバンディットネットワークです。
For $f_{\theta 1}$, since any text-matching neural network (Tay et al., 2018; Wang and Jiang, 2016; Bian et al., 2017) that can provide a single feature vector corresponding to each query-document pair was suitable, we have used the architecture similar to the recently proposed Multi Cast Attention Networks (MCAN) (Tay et al., 2018). 
**$f_{\theta 1}$ については、各クエリ-文書ペアに対応する単一の特徴ベクトルを提供できる任意のテキストマッチングニューラルネットワーク**（Tay et al., 2018; Wang and Jiang, 2016; Bian et al., 2017）が適していたため、最近提案されたMulti Cast Attention Networks (MCAN) (Tay et al., 2018)に類似したアーキテクチャを使用しました。(あ、Two-Towerかと思ったけど、クエリ-文書ペアに対して単一の特徴ベクトルを出力するようなアーキテクチャか...!:thinking:)
The $b_{\theta 2}$ architecture was chosen to be a simple feed forward neural network with an output sigmoid unit for yielding the document affinities corresponding to a query. 
$b_{\theta 2}$ のアーキテクチャは、クエリに対応する文書の親和性を生成するための出力シグモイドユニットを持つシンプルなフィードフォワードニューラルネットワークとして選択されました。
While training, the two architectures were treated as a single architecture by positioning the bandit network on top of the text-matching network. 
**トレーニング中、2つのアーキテクチャは、バンディットネットワークをテキストマッチングネットワークの上に配置することによって、単一のアーキテクチャとして扱われました**。
(うんうん。ここはTwo-Towerモデルも同じ。こういう説明をすればわかりやすいのかも...!:thinking:)
Formally, provided with a context $c=\{(q,d_{1}),(q,d_{2}),\ldots,(q,d_{n_{q}})\}$, we passed it through both networks to obtain the document affinities $\pi_{\theta}(d)$ as given below: 
形式的には、コンテキスト $c=\{(q,d_{1}),(q,d_{2}),\ldots,(q,d_{n_{q}})\}$ が与えられた場合、私たちはそれを両方のネットワークに通して文書の親和性 $\pi_{\theta}(d)$ を取得しました。

$$
f_{\theta 1}(c) = c_{1},c_{2},\ldots,c_{n_{q}} 
\\
b_{\theta 2}(c_{1},c_{2},\ldots,c_{n_{q}}) = \pi_{\theta}(d)
$$

where $c_{i}$ is a feature vector corresponding to the query-document pair $(q,d_{i})$. 
ここで、$c_{i}$はクエリ-文書ペア $(q,d_{i})$ に対応する特徴量ベクトルです。

<!-- ここまで読んだ! -->

### Scenario 2 シナリオ2

In this scenario, we have only used $b_{\theta}$ for training. 
このシナリオでは、トレーニングに $b_{\theta}$ のみを使用しました。
The feature vectors corresponding to the query and document texts were extracted using a pre-trained neural language model such as BERT (Devlin et al., 2018), which is a state-of-the-art unsupervised language model in NLP. 
**クエリとドキュメントテキストに対応する特徴ベクトルは、BERT（Devlin et al., 2018）などの事前学習済みニューラル言語モデルを使用して抽出されました**。これは、NLPにおける最先端の教師なし言語モデルです。
In web search datasets, such as MQ2007 (Qin and Liu, 2013), 46-dimensional feature vectors composed of basic features including BM25, term frequency (TF), and LMIR, are provided for each query-document pair. 
MQ2007（Qin and Liu, 2013）などのウェブ検索データセットでは、BM25、用語頻度（TF）、およびLMIRを含む基本的な特徴から構成された**46次元の特徴ベクトルが各クエリ-ドキュメントペアに対して提供**されます。
We directly use those vectors while conducting experiment on MQ2007 dataset. 
私たちは、MQ2007データセットでの実験を行う際に、これらのベクトルを直接使用します。
Formally, provided with the query-document feature vectors $c_{1},\ldots,c_{n_{q}}$ corresponding to a context $c=\{(q,d_{1}),\ldots,(q,d_{n_{q}})\}$, we have obtained the document affinities $\pi_{\theta}(d)$ as given below: 
形式的には、コンテキスト $c=\{(q,d_{1}),\ldots,(q,d_{n_{q}})\}$ に対応するクエリ-ドキュメント特徴ベクトル $c_{1},\ldots,c_{n_{q}}$ が与えられた場合、以下のようにドキュメントの親和性 $\pi_{\theta}(d)$ を得ました：

$$
b_{\theta}(c_{1},c_{2},\ldots,c_{n_{q}}) = \pi_{\theta}(d)
$$

These scenarios are intended for separating the functionality of the text-matching and bandit networks. 
**これらのシナリオは、テキストマッチングネットワークとバンディットネットワークの機能を分離することを目的としています**。
Therefore, the inputs and outputs are not necessarily in the above prescribed format. 
**したがって、入力と出力は必ずしも上記の指定された形式である必要はありません**。(うんうん...!:thinking:)

The results obtained in both the scenarios indicate that the bandit network is not entirely dependent on a text-matching network for providing good results.
両方のシナリオで得られた結果は、**バンディットネットワークが良好な結果を提供するためにテキストマッチングネットワークに完全に依存していないこと**を示しています。
The exact details of the scenarios and the neural network architectures used for each dataset are provided in the experiments section. 
シナリオの正確な詳細と各データセットに使用されるニューラルネットワークアーキテクチャは、実験セクションに記載されています。

<!-- ここまで読んだ! -->

## 5. Experiments 実験

We conducted our experiments on three different datasets in the domains of question answering and web search. 
私たちは、質問応答とウェブ検索の分野で、3つの異なるデータセットを用いて実験を行いました。
For the question answering task, we tested BanditRank on InsuranceQA (Feng et al., 2015), which is a community question answering dataset (closed domain), and on WikiQA (Yang et al., 2015), which is a well-studied factoid question answering dataset (open domain). 
質問応答タスクでは、コミュニティ質問応答データセット（クローズドドメイン）であるInsuranceQA（Feng et al., 2015）と、よく研究された事実質問応答データセット（オープンドメイン）であるWikiQA（Yang et al., 2015）でBanditRankをテストしました。
For the web search task, we conducted our experiments on the benchmark MQ2007 (Qin and Liu, 2013) dataset. 
ウェブ検索タスクでは、ベンチマークデータセットであるMQ2007（Qin and Liu, 2013）を用いて実験を行いました。
Since the baselines and evaluation measures are different for the above three datasets, we divide this section into three subsections each dealing with a specific dataset. 
上記の3つのデータセットではベースラインと評価指標が異なるため、このセクションをそれぞれ特定のデータセットに関する3つのサブセクションに分けます。
For each dataset, we provide the details of the architecture used, implementation details, details of the baselines, and obtained results. 
各データセットについて、使用したアーキテクチャの詳細、実装の詳細、ベースラインの詳細、および得られた結果を提供します。
We adopted Scenario 1 for the InsuranceQA dataset and Scenario 2 for the MQ2007 dataset and compared both scenarios on the WikiQA dataset. 
InsuranceQAデータセットにはシナリオ1を、MQ2007データセットにはシナリオ2を採用し、WikiQAデータセットで両方のシナリオを比較しました。
Finally, we conducted a comparative study on different reward choices for training on the MQ2007 dataset. 
最後に、MQ2007データセットでのトレーニングにおける異なる報酬選択に関する比較研究を行いました。
We choose the exploration probability mentioned in Section 3.1 as $\epsilon = 0.1$ for all the experiments. 
すべての実験に対して、セクション3.1で言及された探索確率を $\epsilon = 0.1$ として選択しました。

<!-- ここまで読んだ! -->

### 5.1. Experiment 1: InsuranceQA

#### 5.1.1. Dataset and Evaluation Measures

InsuranceQA(Feng et al., 2015) is a well studied community question answering dataset with questions submitted by real users and answers composed by professionals with good domain knowledge. 
InsuranceQA（Feng et al., 2015）は、実際のユーザーから提出された質問と、専門知識を持つプロフェッショナルによって作成された回答を含む、よく研究されたコミュニティ質問応答データセットです。
In this task, BanditRank was expected to select the correct answer among a pool of candidate answers with negative answers randomly sampled from the whole dataset. 
**このタスクでは、BanditRankは、全データセットからランダムにサンプリングされた否定的な回答を含む候補回答のプールから正しい回答を選択すること**が期待されました。(これはground-truthが与えられているから、意思決定問題というより分類問題として解くべきものっぽい??:thinking:)
The dataset consists of two test datasets for evaluation. 
データセットは評価のために2つのテストデータセットで構成されています。
The evaluation measure for this task was Precision@1. 
このタスクの評価指標はPrecision@1でした。
The statistics of the dataset along with the average number of relevant answers per question are given in Table 1. 
データセットの統計と、質問ごとの関連回答の平均数は表1に示されています。

#### 5.1.2. Model and Implementation Details　モデルと実装の詳細

We used two architectures for Scenario 1. 
シナリオ1には2つのアーキテクチャを使用しました。
For the text matching part, we used the architecture of the recently proposed Multi Cast Attention Network (MCAN)(Tay et al., 2018). 
テキストマッチング部分には、最近提案されたMulti Cast Attention Network (MCAN)（Tay et al., 2018）のアーキテクチャを使用しました。
Specifically, we used the same architecture until the mean max pooling operation layer of the MCAN, which provides a fixed dimensional feature vector of each question or answer sentence. 
具体的には、MCANの平均最大プーリング操作層まで同じアーキテクチャを使用し、各質問または回答文の固定次元の特徴ベクトルを提供しました。
We used the sum function (SM) as the compression function for casting the attention. 
注意を向けるための圧縮関数として、和関数（SM）を使用しました。
For the bandit network, we modified the prediction layer of MCAN with a sigmoid unit in the output layer and kept the two highway layers intact. 
バンディットネットワークでは、MCANの予測層を出力層にシグモイドユニットを追加して修正し、2つのハイウェイ層はそのままにしました。
We conducted the experiments by replacing the highway networks with simple neural networks with the same dimensions, but the best results were obtained when highway layers were used. 
ハイウェイネットワークを同じ次元の単純なニューラルネットワークに置き換えて実験を行いましたが、ハイウェイ層を使用したときに最良の結果が得られました。
Highway networks (Srivastava et al., 2015) are gated nonlinear transform layers that control the information flow similar to the LSTM layers (Hochreiter and Schmidhuber, 1997) for sequential tasks. 
ハイウェイネットワーク（Srivastava et al., 2015）は、情報の流れを制御するゲート付き非線形変換層であり、シーケンシャルタスクに対するLSTM層（Hochreiter and Schmidhuber, 1997）に似ています。

We randomly initialized the embedding matrix with 100 dimensional vectors sampled from standard normal distribution and fixed them during training. 
埋め込み行列を標準正規分布からサンプリングした100次元ベクトルでランダムに初期化し、トレーニング中は固定しました。
The hidden size of the LSTM layers was set to 300. 
LSTM層の隠れサイズは300に設定しました。
The dimensions of the two highway prediction layers were set to 200 with ReLU being the activation function. 
2つのハイウェイ予測層の次元は200に設定し、活性化関数にはReLUを使用しました。
Once we obtained the feature vectors corresponding to the question and answer sentences from the text-matching network $h_q, h_a \in \mathbb{R}^{600}$, we passed the following vector $h_{qa} = [h_q; h_a; h_q \odot h_a; h_q - h_a] \in \mathbb{R}^{2400}$ to the bandit network, where $\odot$ is the pointwise multiplication operation and $[.;.]$ is a vector concatenation operator. 
テキストマッチングネットワークから質問と回答文に対応する特徴ベクトル $h_q, h_a \in \mathbb{R}^{600}$ を取得した後、次のベクトル $h_{qa} = [h_q; h_a; h_q \odot h_a; h_q - h_a] \in \mathbb{R}^{2400}$ をバンディットネットワークに渡しました。ここで、$\odot$ は要素ごとの乗算操作であり、$[.;.]$ はベクトルの連結演算子です。
The vectors $h_{qa}$ correspond to the query-document feature vectors $c_i$ mentioned in Section 4. 
**ベクトル $h_{qa}$ は、セクション4で言及されたクエリ-ドキュメント特徴ベクトル $c_i$ に対応**します。
Before passing $h_{qa}$ to the highway layers of the bandit network, we used a single feed forward layer with a ReLU activation function for projecting $h_{qa}$ into a 200-dimensional space. 
**$h_{qa}$ をバンディットネットワークのハイウェイ層に渡す前に、$h_{qa}$ を200次元空間に投影するためにReLU活性化関数を持つ単一のフィードフォワード層を使用**しました。
A dropout of 0.2 was applied to all layers except the embedding layer. 
埋め込み層を除くすべての層に0.2のドロップアウトが適用されました。
The sequences were padded to their batch-wise maximums. 
シーケンスはバッチごとの最大値にパディングされました。
We optimized the model using the Adam optimizer (Kingma and Ba, 2014) with the beta parameters set to $(0.9, 0.999)$ and a weight decay of $1e^{-6}$ was used for regularization. 
モデルは、ベータパラメータを $(0.9, 0.999)$ に設定したAdamオプティマイザ（Kingma and Ba, 2014）を使用して最適化し、正則化には $1e^{-6}$ の重み減衰が使用されました。
We used the hybrid training objective defined in Eq. (12) with $\gamma$ tuned over the set of values $[0.5, 0.75, 1]$. 
ハイブリッドトレーニング目的は、式（12）で定義され、$\gamma$ は値のセット $[0.5, 0.75, 1]$ にわたって調整されました。
An initial learning rate of $5e^{-5}$ was used for BanditRank with $\gamma=1$ and $1e^{-4}$ for BanditRank with other $\gamma$ values. 
初期学習率は、$\gamma=1$ のBanditRankには $5e^{-5}$ が使用され、他の $\gamma$ 値のBanditRankには $1e^{-4}$ が使用されました。
We set $M', B$ to $M' = 5$ and $B = 20$ for calculating the gradient in Eq. (8). 
勾配を計算するために、$M', B$ を $M' = 5$ および $B = 20$ に設定しました。
For BanditRank with $\gamma=0.75$, $M'$ was set to 20. 
$\gamma=0.75$ のBanditRankでは、$M'$ を20に設定しました。

We used the reward function defined as Eq. (10) during training. 
トレーニング中は、式（10）で定義された報酬関数を使用しました。

#### 5.1.3. Baselines and Results

#### 5.1.3. ベースラインと結果

We compared the performance of BanditRank against all current methods that achieved significant results on this dataset. 
BanditRankの性能を、このデータセットで重要な結果を達成したすべての現在の手法と比較しました。
The competitive baselines are the IR model (Bendersky et al., 2010), CNN with GESD (from the authors who created the InsuranceQA dataset) (Feng et al., 2015), Attentive LSTM (Tan et al., 2016), IARNN-Occam (Wang et al., 2016a), IARNN-Gate (Wang et al., 2016a), QA-CNN (Santos et al., 2016), LambdaCNN (Santos et al., 2016; Zhang et al., 2013), IRGAN (Wang et al., 2017b), and the method with the previous best P@1 measure, Comp-Agg (Wang and Jiang, 2016). 
競争ベースラインは、IRモデル（Bendersky et al., 2010）、GESDを使用したCNN（InsuranceQAデータセットを作成した著者から）（Feng et al., 2015）、Attentive LSTM（Tan et al., 2016）、IARNN-Occam（Wang et al., 2016a）、IARNN-Gate（Wang et al., 2016a）、QA-CNN（Santos et al., 2016）、LambdaCNN（Santos et al., 2016; Zhang et al., 2013）、IRGAN（Wang et al., 2017b）、および以前の最良のP@1測定値を持つ手法、Comp-Agg（Wang and Jiang, 2016）です。
A description of all the baselines can be found in previous studies (Wang and Jiang, 2016; Wang et al., 2017b). 
すべてのベースラインの説明は、以前の研究（Wang and Jiang, 2016; Wang et al., 2017b）に見つけることができます。
As the testing splits were the same for all methods, we report the P@1 measures directly from those studies. 
テストスプリットはすべての手法で同じであったため、これらの研究から直接P@1測定値を報告します。

The results in Table 2 indicate the superiority of BanditRank over all other methods. 
表2の結果は、BanditRankが他のすべての手法に対して優れていることを示しています。
BanditRank with $\gamma=1$ achieved the second best P@1 measure, this is equivalent to training the model only with the reinforcement loss. 
$\gamma=1$ のBanditRankは、2番目に良いP@1測定値を達成しました。これは、モデルを強化損失のみでトレーニングすることに相当します。
The results further improved using a hybrid loss with $\gamma=0.75$ weight to the reinforcement loss $L_{rl}$. 
結果は、強化損失 $L_{rl}$ に対して重み $\gamma=0.75$ のハイブリッド損失を使用することでさらに改善されました。
Therefore, providing some weight to the supervised loss improved the performance of BanditRank. 
したがって、教師あり損失にいくらかの重みを与えることで、BanditRankの性能が向上しました。
BanditRank exhibited significant improvement in P@1 measure by 13.3% on the test-1 dataset and 16.1% on the test-2 dataset when compared to the previous best method. 
BanditRankは、以前の最良の手法と比較して、テスト-1データセットでP@1測定値が13.3%、テスト-2データセットで16.1%の大幅な改善を示しました。

<!-- ここまで読んだ! -->

### 5.2. Experiment 2: WikiQA
#### 5.2.1. Dataset and Evaluation Measures データセットと評価指標

WikiQA(Yang et al., 2015) is a well-known open domain question answering dataset in contrast to InsuranceQA, which is a closed domain question answering dataset. 
WikiQA（Yang et al., 2015）は、保険QAとは対照的に、よく知られたオープンドメインの質問応答データセットです。
The dataset was constructed from real queries on Bing and Wikipedia. 
このデータセットは、BingとWikipediaの実際のクエリから構築されました。
In this task, the models were expected to rank the candidate answers according to the question. 
このタスクでは、モデルは質問に基づいて候補となる回答をランク付けすることが期待されました。
The evaluation measures for this task were MAP and MRR. 
このタスクの評価指標はMAPとMRRでした。
The statistics of the dataset are given in Table 3. 
データセットの統計は表3に示されています。

#### 5.2.2. Model and Implementation details モデルと実装の詳細

We considered both the scenarios given in Section 4 for WikiQA dataset. 
私たちは、WikiQAデータセットに対してセクション4で示された両方のシナリオを考慮しました。
For Scenario 1, we used the same setting of MCAN as InsuranceQA. 
シナリオ1では、保険QAと同じMCANの設定を使用しました。
The only difference was the type of embedding used. 
唯一の違いは、使用される埋め込みのタイプでした。
We initialized the embedding matrix with 300-dimensional GloVe embeddings (Pennington et al., 2014) and fixed them during training. 
埋め込み行列は、300次元のGloVe埋め込み（Pennington et al., 2014）で初期化し、トレーニング中は固定しました。
We used the reward function defined as Eq. (10) during training. 
トレーニング中は、式（10）で定義された報酬関数を使用しました。
A dropout of 0.2 was applied to all layers except the embedding layer. 
埋め込み層を除くすべての層に0.2のドロップアウトが適用されました。
The sequences were padded to their batch-wise maximums. 
シーケンスは、バッチごとの最大値にパディングされました。

We optimized the model using the Adam optimizer (Kingma and Ba, 2014) with the beta parameters set to (0.9, 0.999), and a weight decay of $1e^{-6}$ was used for regularization. 
モデルは、ベータパラメータを(0.9, 0.999)に設定したAdamオプティマイザ（Kingma and Ba, 2014）を使用して最適化し、正則化のために$1e^{-6}$の重み減衰が使用されました。
We used the hybrid training objective defined in Eq. (12) with $\gamma$ tuned over the set of values [0.25, 0.5, 0.75, 1]. 
私たちは、式（12）で定義されたハイブリッドトレーニング目的を使用し、$\gamma$を[0.25, 0.5, 0.75, 1]の値のセットで調整しました。
We provide the results of the two best performing models with respect to $\gamma$. 
私たちは、$\gamma$に関して最も良いパフォーマンスを示した2つのモデルの結果を提供します。
An initial learning rate of $5e^{-5}$ was used for BanditRank with $\gamma=1$ and $1e^{-4}$ for BanditRank with other $\gamma$ values. 
初期学習率は、$\gamma=1$のBanditRankに対して$5e^{-5}$、他の$\gamma$値のBanditRankに対して$1e^{-4}$が使用されました。
We set $M', B$ to $M' = 3$ and $B = 20$ for calculating the gradient in Eq. (8). 
式（8）で勾配を計算するために、$M', B$を$M' = 3$および$B = 20$に設定しました。
The $M'$ was chosen according to the average number of relevant queries, which is much less for the WikiQA dataset. 
$M'$は、WikiQAデータセットの関連クエリの平均数に基づいて選択されました。

<!-- ここまで読んだ! -->

For Scenario 2, we extracted word-level features from a pre-trained BERT (Devlin et al., 2018) language model, which takes a question-answer sentence pair $(q, a)$ as the input. 
シナリオ2では、事前学習済みのBERT（Devlin et al., 2018）言語モデルから単語レベルの特徴を抽出しました。このモデルは、質問-回答文のペア$(q, a)$を入力として受け取ります。
There are two versions of the BERT model available, BERT-base and BERT-large. 
利用可能なBERTモデルには、BERT-baseとBERT-largeの2つのバージョンがあります。
We conducted our experiments on features extracted with both versions. 
私たちは、両方のバージョンから抽出された特徴を使用して実験を行いました。
We used the concatenation of word-level features obtained from the last four layers of the BERT language model for training. 
**トレーニングには、BERT言語モデルの最後の4層から得られた単語レベルの特徴の連結を使用**しました。
BERT-base produced 3072-dimensional feature vectors for each word in the input sentence while BERT-large produced 4096-dimensional feature vectors after the concatenation. 
BERT-baseは、入力文の各単語に対して3072次元の特徴ベクトルを生成し、BERT-largeは連結後に4096次元の特徴ベクトルを生成しました。
These contextual word embeddings were passed through a two-layer bidirectional LSTM layer followed by mean pooling for obtaining a fixed dimensional representation of $(q, a)$. 
これらの文脈的な単語埋め込みは、2層の双方向LSTM層を通過し、その後平均プーリングを行って$(q, a)$ の固定次元表現を得ました。
These vectors correspond to the $c_i$ vectors mentioned in Section 4. 
**これらのベクトルは、セクション4で言及された$c_i$ベクトルに対応**しています。
Regarding the architecture of the bandit network, we chose a feed forward network with a single hidden layer followed by a sigmoid unit at the output layer. 
バンディットネットワークのアーキテクチャに関しては、**出力層にシグモイドユニットを持つ単一の隠れ層を持つフィードフォワードネットワークを選択**しました。
Tanh was used as the activation function. 
活性化関数としてTanhが使用されました。
For the BanditRank method trained on features extracted from BERT-base, we set the dimensions of the LSTM layer to 768. 
BERT-baseから抽出された特徴でトレーニングされたBanditRankメソッドでは、LSTM層の次元を768に設定しました。
For BERT-large, we set the dimensions of the LSTM layer to 1024. 
BERT-largeの場合、LSTM層の次元を1024に設定しました。
For the feed forward layer, we set the dimensions of the hidden layer to 256 for both types of features. 
フィードフォワード層では、両方のタイプの特徴に対して隠れ層の次元を256に設定しました。
A dropout of 0.4 was applied to all layers. 
すべての層に0.4のドロップアウトが適用されました。
We optimized BanditRank using the Adam optimizer (Kingma and Ba, 2014) with the beta parameters set to (0, 0.999) and used a weight decay of $1e^{-6}$ for regularization. 
BanditRankは、ベータパラメータを(0, 0.999)に設定したAdamオプティマイザ（Kingma and Ba, 2014）を使用して最適化し、正則化のために$1e^{-6}$の重み減衰を使用しました。
We used the hybrid training objective defined in Eq. (12) with $\gamma$ tuned over the set of values [0.5, 0.75, 1]. 
私たちは、式（12）で定義されたハイブリッドトレーニング目的を使用し、$\gamma$を[0.5, 0.75, 1]の値のセットで調整しました。
We provide the results of the best performing model with respect to $\gamma$. 
私たちは、$\gamma$に関して最も良いパフォーマンスを示したモデルの結果を提供します。
An initial learning rate of $8e^{-5}$ was used for BanditRank with $\gamma=1$ and $1e^{-4}$ for the BanditRank method with other $\gamma$ values. 
初期学習率は、$\gamma=1$のBanditRankに対して$8e^{-5}$、他の$\gamma$値のBanditRankメソッドに対して$1e^{-4}$が使用されました。
We set $M', B$ to $M' = 5$ and $B = 20$ for calculating the gradient in Eq. (8). 
式（8）で勾配を計算するために、$M', B$を$M' = 5$および$B = 20$に設定しました。
We used the reward function defined with Eq. (10) during training. 
トレーニング中は、式（10）で定義された報酬関数を使用しました。

<!-- ここまで読んだ! -->

#### 5.2.3. Baselines and Results ベースラインと結果

We compared the performance of BanditRank against all other previous methods on this dataset. 
私たちは、このデータセットにおけるBanditRankのパフォーマンスを他のすべての以前の方法と比較しました。
The baselines were CNN-Cnt (Yang et al., 2015), QA-CNN (Santos et al., 2016), NASM (Miao et al., 2016), Wang et al (Wang et al., 2016b), He and Lin (He and Lin, 2016), NCE-CNN (Rao et al., 2016), BIMPM (Wang et al., 2017a), Comp-Agg (Wang and Jiang, 2016), and the state-of-the-art method Comp-Clip (Bian et al., 2017). 
ベースラインは、CNN-Cnt（Yang et al., 2015）、QA-CNN（Santos et al., 2016）、NASM（Miao et al., 2016）、Wang et al（Wang et al., 2016b）、He and Lin（He and Lin, 2016）、NCE-CNN（Rao et al., 2016）、BIMPM（Wang et al., 2017a）、Comp-Agg（Wang and Jiang, 2016）、および最先端の方法であるComp-Clip（Bian et al., 2017）でした。
Since the testing split is same for all methods, we report the highest measures directly from the respective papers. 
テストスプリットはすべての方法で同じであるため、私たちはそれぞれの論文から直接最高の測定値を報告します。
The results given in Table 4 indicate the superiority of BanditRank over all other methods. 
表4に示された結果は、BanditRankが他のすべての方法に対して優れていることを示しています。
BanditRank trained using the features extracted from BERT-large produced the best results. 
BERT-largeから抽出された特徴を使用してトレーニングされたBanditRankは、最良の結果を出しました。
Interestingly in Scenario 1, we observed performance degradation when hybrid loss was used. 
興味深いことに、シナリオ1では、ハイブリッド損失を使用した際にパフォーマンスの低下が観察されました。
Although, this degradation may depend on many factors, one possible explanation can be that the model can explore with the help of $L_{rl}$ efficiently since the average number of relevant documents is much less. 
この低下は多くの要因に依存する可能性がありますが、1つの可能な説明は、関連文書の平均数がはるかに少ないため、モデルが$L_{rl}$の助けを借りて効率的に探索できることです。
The results in Scenario 2 indicate that, provided with good features, training a text-matching network along with the bandit network is not necessary for achieving good results. 
**シナリオ2の結果は、良い特徴が提供されれば、バンディットネットワークと共にテキストマッチングネットワークをトレーニングする必要はないことを示しています**。(ふむふむ...!:thinking:)

<!-- ここまで読んだ! -->

### 5.3. Experiment 3: MQ2007

#### 5.3.1. Dataset and Evaluation Measures データセットと評価指標

For the web search task, we used the benchmark Million Query Track 2007 (MQ2007)(Qin and Liu,2013)dataset777https://www.microsoft.com/en-us/research/project/letor-learning-rank-information-retrieval/. 
ウェブ検索タスクでは、ベンチマークのMillion Query Track 2007 (MQ2007)(Qin and Liu,2013)データセットを使用しました777https://www.microsoft.com/en-us/research/project/letor-learning-rank-information-retrieval/。
In this task, BanditRank was expected to rank the documents corresponding to a query according to their relevance. 
このタスクでは、**BanditRankはクエリに対応する文書をその関連性に基づいてランク付けすること**が期待されました。(これもground-truthが与えられてるのかな。検索だと割とそういうケースが多いのかも??:thinking:)
Unlike the previous tasks in which the relevance was binary, this task consisted of multiple-levels of relevance with {0,1,2}. 
**以前のタスクが二値の関連性であったのに対し、このタスクは{0,1,2}の複数のレベルの関連性で構成されていました**。
This dataset provides 46-dimensional feature vectors corresponding to each query-document pair. 
このデータセットは、各クエリ-文書ペアに対応する46次元の特徴ベクトルを提供します。
Moreover, the average number of relevant documents per query was very large compared to the previous tasks. 
さらに、クエリあたりの関連文書の平均数は、以前のタスクと比較して非常に大きかったです。
The statistics are given in Table 5. 
統計は表5に示されています。
Out of the total 1692 queries, the number of queries with at least one relevant document was only 1455. 
1692のクエリのうち、少なくとも1つの関連文書を持つクエリの数は1455に過ぎませんでした。

The loss for the above mentioned 237 query instances would be zero as the reward generated would be zero. 
上記の237のクエリインスタンスに対する損失は、生成される報酬がゼロであるためゼロになります。
Therefore, we conduct experiments on the dataset after removing the queries with no relevant documents as they would not help BanditRank during training. 
したがって、BanditRankのトレーニングに役立たないため、関連文書のないクエリを削除した後にデータセットで実験を行います。
We carried out 60-20-20 splitting for the train-val-test datasets after the dataset was cleaned. 
データセットがクリーンになった後、トレイン-バリデーション-テストデータセットの60-20-20分割を行いました。
The baselines were also trained and evaluated on the same splits. 
ベースラインも同じ分割でトレーニングおよび評価されました。
As per evaluation measures, we report the measures of MAP, MRR, precision, and nDCG at positions 1, 3, 10. 
評価指標に従い、位置1、3、10でのMAP、MRR、精度、およびnDCGの指標を報告します。
We also conducted significance tests using both paired t-test and Wilcoxon signed rank test. 
また、対応のあるt検定とウィルコクソン符号付き順位検定の両方を使用して有意性テストを実施しました。

<!-- ここまで読んだ! -->

#### 5.3.2. Model and Implementation details モデルと実装の詳細

We used Scenario 2 for this task. 
このタスクにはシナリオ2を使用しました。
For the bandit network, we used a feed forward layer with three highway network layers followed by an output layer with a sigmoid unit. 
**バンディットネットワークには、3つのハイウェイネットワーク層の後にシグモイドユニットを持つ出力層を持つフィードフォワード層を使用しました**。

- 森田メモ: highwayネットワークについて
  - NNの訓練を容易にするために開発された特別な層。
  - highwayネットワークは、NNの層が深くなるにつれて勾配が消失したり爆発したりする問題(勾配消失・爆発問題)を解決するために開発された。
  - 核心はLSTMにインスパイアされたゲートメカニズム。
    - 従来のFeed Forward NNでは、ある層の出力 y はその入力xに非線形変換 H を適用することで得られる: $y = H(x, W_{H})$。
    - 一方、ハイウェイネットワークでは、この変換に加えて、**入力 x をそのまま次の層に「運び去る」情報ハイウェイのような経路が追加**される。この「変換」と「運び去る」という2つの経路の情報を、ゲートを使ってどれくらいの割合で結合するかを学習する。
      - $y = H(x, W_{H}) \odot T(x, W_{T}) + x \odot C(x, W_{C})$
      - ここで...
        - $H(x, W_{H})$ はFFNNと同じ非線形変換。通常は、アフィン変換（線形変換＋バイアス）の後に非線形活性化関数が続く。
        - $T(x, W_{T})$ は「変換ゲート(transform gate)」と呼ばれるゲート。
          - 入力xから計算されて最終的に0~1の間の値を出力する。これは、$H(x, W_{H})$ からの出力のうち、どれだけの割合を通過させるかを制御する。
        - $C(x, W_{C})$ は「キャリーゲート(carry gate)」と呼ばれるゲート。
          - 入力xから計算されて最終的に0~1の間の値を出力する。これは、入力x自体をどれだけの割合で次の層に「運び去る(carry)」かを制御する。
          - 元の論文では、キャリーゲート C は変換ゲート T の補数として設定されることが多い。この場合 $C = 1 - T$ となる。
  - highwayネットワーク層は、pytorchでは直接提供はされてないっぽい。なので自前で`nn.Module`を継承して実装する必要がありそう...??:thinking:

The dimensions of the highway layer were set to 92. 
ハイウェイ層の次元は92に設定されました。
An input projection layer with an ReLU activation function was used to project the input vectors into 92 dimensions. 
ReLU活性化関数を持つ入力投影層を使用して、入力ベクトルを92次元に投影しました。
The provided 46-dimensional feature vectors correspond to vectors $c_i$ mentioned in Section 4. 
提供された46次元の特徴ベクトルは、セクション4で言及されたベクトル$c_i$に対応します。

We used the reward function defined in Eq.(11). 
私たちは、式(11)で定義された報酬関数を使用しました。
We chose nDCG@10 instead of reciprocal rank (RR) for this task as the number of relevant documents was large. 
関連文書の数が多いため、このタスクでは逆数ランク(RR)の代わりにnDCG@10を選択しました。
We optimized the model using the Adam optimizer (Kingma and Ba, 2014) with the beta parameters set to (0, 0.999), and a weight decay of $1e^{-6}$ was used for regularization. 
私たちは、ベータパラメータを(0, 0.999)に設定したAdamオプティマイザ(Kingma and Ba, 2014)を使用してモデルを最適化し、正則化のために$1e^{-6}$の重み減衰を使用しました。
We used the hybrid training objective defined in Eq.(12) with $\gamma$ tuned over the set of values [0.25, 0.5, 0.75, 1]. 
私たちは、式(12)で定義されたハイブリッドトレーニング目的を使用し、$\gamma$を[0.25, 0.5, 0.75, 1]の値のセットで調整しました。
The best results were obtained for BanditRank with $\gamma=0.5$. 
最良の結果は、$\gamma=0.5$のBanditRankで得られました。
A dropout of 0.4 was applied to all layers. 
すべての層に0.4のドロップアウトが適用されました。
An initial learning rate of $7e^{-5}$ was used for all models. 
すべてのモデルに対して$7e^{-5}$の初期学習率が使用されました。
We set $M', B$ to $M' = 40$ and $B = 30$ for calculating the gradient in Eq.(8). 
式(8)で勾配を計算するために、$M', B$を$M' = 40$および$B = 30$に設定しました。
A high value was chosen for $M'$ because the number of queries with at least 30 relevant documents was 99, which is a significant number. 
$M'$には高い値が選ばれました。なぜなら、少なくとも30の関連文書を持つクエリの数が99であり、これは重要な数だからです。
Moreover, the average number of relevant documents per query was large, i.e., 10.3. 
さらに、クエリあたりの関連文書の平均数は大きく、すなわち10.3でした。

<!-- ここまで読んだ! -->

#### 5.3.3. Baselines and Results

#### 5.3.3. ベースラインと結果

We compared BanditRank with four strong listwise baselines. 
私たちは、BanditRankを4つの強力なリストワイズベースラインと比較しました。
The baselines were AdaRank (Xu and Li, 2007), ListNet (Cao et al., 2007), Coordinate Ascent (Metzler and Croft, 2007) and the state-of-the-art listwise ranking method LambdaMART (Burges, 2010). 
ベースラインは、AdaRank (Xu and Li, 2007)、ListNet (Cao et al., 2007)、Coordinate Ascent (Metzler and Croft, 2007)、および最先端のリストワイズランキング手法であるLambdaMART (Burges, 2010)でした。
All baselines were implemented using the RankLib888https://sourceforge.net/projects/lemur/software. 
すべてのベースラインは、RankLib888https://sourceforge.net/projects/lemur/softwareを使用して実装されました。
As mentioned in Section 3.4, hybrid training objective with $\gamma=0.5$ resulted in the best performance as BanditRank with $\gamma=1$ cannot efficiently explore the relatively large action space in this task. 
セクション3.4で述べたように、$\gamma=0.5$のハイブリッドトレーニング目的は最良のパフォーマンスをもたらしました。なぜなら、$\gamma=1$のBanditRankはこのタスクで比較的大きなアクション空間を効率的に探索できないからです。

The results given in Table 6 show that BanditRank clearly outperformed AdaRank, ListNet, and Coordinate Ascent. 
表6に示された結果は、BanditRankが明らかにAdaRank、ListNet、およびCoordinate Ascentを上回ったことを示しています。
When compared with the stronger baseline LambdaMART, except for the measures P@10, nDCG@3, and nDCG@10, BanditRank achieved a minimum of 1% improvement in all other measures. 
より強力なベースラインであるLambdaMARTと比較した場合、P@10、nDCG@3、およびnDCG@10を除いて、BanditRankは他のすべての指標で最低1%の改善を達成しました。
Except for the measure nDCG@10, the improvement shown by BanditRank on all other measures is statistically significant according to the paired t-test and Wilcoxon signed rank test. 
nDCG@10の指標を除いて、BanditRankが他のすべての指標で示した改善は、対応のあるt検定およびウィルコクソン符号付き順位検定により統計的に有意です。
In the next section, we discuss the behavior of different reward functions when trained on the MQ2007 dataset. 
次のセクションでは、MQ2007データセットでトレーニングされたときの異なる報酬関数の挙動について議論します。

<!-- ここまで読んだ! -->

### 5.4. 報酬関数の比較

The reward function plays a significant role in the training of an agent in reinforcement learning. 
**報酬関数は、強化学習におけるエージェントの訓練において重要な役割を果たします。**
Gradual feedback through rewards is often required for training a good agent. 
良いエージェントを訓練するためには、報酬を通じた段階的なフィードバックがしばしば必要です。 
For comparing the behavior of reward functions during training, we conducted experiments using different reward functions on the MQ2007 dataset with the same architecture as the previous section. 
報酬関数の訓練中の挙動を比較するために、前のセクションと同じアーキテクチャを用いてMQ2007データセット上で異なる報酬関数を使用した実験を行いました。 
Since we wanted to compare the behavior of the reward function, we chose $\gamma=1$ for all the experiments. 
報酬関数の挙動を比較したかったため、すべての実験で$\gamma=1$を選択しました。 
The following reward functions were used: 
以下の報酬関数が使用されました：

$$
各報酬関数の定義
$$

The first three reward functions are the direct evaluation measures and the last three are a combination of several evaluation measures. 
最初の3つの報酬関数は直接的な評価指標であり、最後の3つは複数の評価指標の組み合わせです。 
Figure 1 plots the test set performance of the models during training epochs. 
図1は、訓練エポック中のモデルのテストセット性能をプロットしています。 
We can observe that $R_{1}$ achieved good measures right from the start when compared with $R_{2}$ and $R_{3}$. 
$R_{1}$は、$R_{2}$および$R_{3}$と比較して、開始時から良好な指標を達成したことが観察できます。 
The performance of $R_{6}$ when compared with $R_{5}$ and $R_{4}$ shows that using many evaluation measures will not necessarily improve the measures of MAP and nDCG@10. 
$R_{6}$の性能は、$R_{5}$および$R_{4}$と比較した場合、多くの評価指標を使用することが必ずしもMAPおよびnDCG@10の指標を改善するわけではないことを示しています。 
During the initial epochs, $R_{4}$ was clearly a better performer than $R_{5}$ and $R_{6}$. 
初期のエポックでは、$R_{4}$は明らかに$R_{5}$および$R_{6}$よりも優れた性能を示しました。 
After a similar performance by all three models in the next few epochs, $R_{4}$ achieved better measures of MAP and nDCG@10 in the final stages. 
次の数エポックで3つのモデルが同様の性能を示した後、$R_{4}$は最終段階でMAPおよびnDCG@10の指標をより良く達成しました。 

## 6.Conclusion 結論

We proposed an extensible listwise deep learning method BanditRank for ranking. 
私たちは、ランキングのための拡張可能なリストワイズ深層学習手法BanditRankを提案しました。
It can directly optimize the evaluation measures using the policy gradient algorithm. 
これは、ポリシー勾配アルゴリズムを使用して評価指標を直接最適化できます。(要するに回帰ベースじゃなくて勾配ベースのアプローチ...!:thinking:)
Experimental results indicate the superiority of BanditRank over other methods on the tested datasets. 
実験結果は、テストされたデータセットにおいてBanditRankが他の手法に対して優れていることを示しています。
Future work can involve modifying the structure of the policy network discussed in Section 3.1 for efficiently addressing the issue of exploration when the number of actions is large. 
今後の研究では、**アクションの数が多い場合の探索の問題に効率的に対処するために、セクション3.1で議論されたポリシーネットワークの構造を修正すること**が考えられます。
For example, we could use adaptive exploration strategies instead of simple $\epsilon$-greedy strategy, for exploring the action space. 
例えば、アクション空間を探索するために、**単純な$\epsilon$-greedy戦略の代わりに適応的探索戦略(??)を使用すること**ができます。
We can define new reward functions for handling queries with no relevant documents. 
関連する文書がないクエリを処理するための**新しい報酬関数を定義**することができます。
For example, we can penalize the model if any of the document affinity scores for such queries is greater than 0.5. 
例えば、そのようなクエリの文書親和性スコアのいずれかが0.5を超える場合、モデルにペナルティを課すことができます。
There is also a possibility of defining reward functions as the weighted average of different measures with trainable weights for better feedback. 
より良いフィードバックのために、**異なる指標の重み付き平均として報酬関数を定義する可能性**もあります。
Regarding the theoretical aspects, we can compare the directness of BanditRank to other algorithms such as LambdaRank. 
理論的な側面に関しては、BanditRankの直接性をLambdaRankなどの他のアルゴリズムと比較することができます。

<!-- ここまで読んだ! -->

