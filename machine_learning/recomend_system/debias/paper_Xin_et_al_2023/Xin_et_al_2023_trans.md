## 0.1. link リンク

https://arxiv.org/pdf/2305.05585.pdf
https://arxiv.org/pdf/2305.05585.pdf

## 0.2. title タイトル

Improving Implicit Feedback-Based Recommendation through Multi-Behavior Alignment
マルチ行動アライメントによる暗黙のフィードバックに基づくレコメンデーションの改善

## 0.3. abstruct abstruct

Recommender systems that learn from implicit feedback often use large volumes of a single type of implicit user feedback, such as clicks, to enhance the prediction of sparse target behavior such as purchases.
暗黙のフィードバックから学習するレコメンダーシステムは、購入のような疎なターゲット行動(=最適化させたい行動?)の予測を強化するために、クリックのような単一のタイプの暗黙のユーザフィードバックを大量に使用することが多い。
Using multiple types of implicit user feedback for such target behavior prediction purposes is still an open question.
このようなターゲット行動予測の目的で、**複数のタイプの暗黙的ユーザフィードバックを使用することは、まだ未解決の問題**である。
Existing studies that attempted to learn from multiple types of user behavior often fail to: (i) learn universal and accurate user preferences from different behavioral data distributions, and (ii) overcome the noise and bias in observed implicit user feedback.
複数のタイプのユーザ行動から学習しようとする既存の研究は、しばしば以下の事に失敗する：(i)異なる行動データ分布から普遍的で正確なユーザ嗜好を学習する、(ii)観測された暗黙的なユーザフィードバックにおけるノイズとバイアスを克服する。
To address the above problems, we propose multi-behavior alignment (MBA), a novel recommendation framework that learns from implicit feedback by using multiple types of behavioral data.
上記の問題点を解決するために、我々は、複数種類の行動データを用いて暗黙のフィードバックから学習する新しい推薦フレームワークである**multi-behavior alignment(MBA)**(alignmentは調整??:thinking:)を提案する。
We conjecture that multiple types of behavior from the same user (e.g., clicks and purchases) should reflect similar preferences of that user.
同じユーザからの複数のタイプの行動（例えば、クリックや購入）は、そのユーザの類似した嗜好を反映しているはずだと推測される。
To this end, we regard the underlying universal user preferences as a latent variable.
この目的のために、私たちは**根底にある普遍的なユーザの嗜好を潜在変数とみなす**。
The variable is inferred by maximizing the likelihood of multiple observed behavioral data distributions and, at the same time, minimizing the Kullback–Leibler divergence (KL-divergence) between user models learned from auxiliary behavior (such as clicks or views) and the target behavior separately.
この(潜在)変数は、観測された複数の行動データ分布の尤度を最大化すると同時に、補助行動(clickやviewなど)から学習したユーザモデルと対象行動との間のKLダイバージェンス(Kullback-Leibler divergence)を個別に最小化することで推論される。
MBA infers universal user preferences from multi-behavior data and performs data denoising to enable effective knowledge transfer.
**MBAは、複数の行動データから普遍的なユーザ嗜好を推測し、効果的な知識伝達を可能にするためにデータのノイズ除去を行う**。
We conduct experiments on three datasets, including a dataset collected from an operational e-commerce platform.
電子商取引のプラットフォームから収集したデータセットを含む、3つのデータセットで実験を行った。
Empirical results demonstrate the effectiveness of our proposed method in utilizing multiple types of behavioral data to enhance the prediction of the target behavior.
実証結果は、複数種類の行動データを利用して対象行動の予測精度を向上させる提案手法の有効性を示している。

# 1. Introduction はじめに

Recommender systems aim to infer user preferences from observed user-item interactions and recommend items that match those preferences.
レコメンダーシステムは、観察されたユーザとアイテムの相互作用からユーザの嗜好を推測し、その嗜好に合ったアイテムを推薦することを目的としている。
Many operational recommender systems are trained from implicit user feedback [14, 16].
多くの運用されている推薦システムは、暗黙のユーザフィードバックから学習される[14, 16]。
Recommender systems that learn from implicit user feedback are typically trained on a single type of implicit user behavior, such as clicks.
暗黙的なユーザフィードバックから学習するレコメンダーシステムは、通常、クリックなどの単一タイプの暗黙的なユーザ行動で学習される。(そうなの...??)
However, in real-world scenarios, multiple types of user behavior are logged when a user interacts with a recommender system.
しかし、実世界のシナリオでは、ユーザがレコメンダー・システムと相互作用する際に、**複数のタイプのユーザ行動が記録される**。(うんうん...!)
For example, users may click, add to a cart, and purchase items on an e-commerce platform [31].
例えば、ユーザはeコマースプラットフォーム上で商品をクリックし、カートに入れ、購入することができる[31]。
Simply learning recommenders from a single type of behavioral data such as clicks can lead to a misunderstanding of a user’s real user preferences since the click data is noisy and can easily be corrupted due to bias [5], and thus lead to suboptimal target behavior (e.g., purchases) predictions.
クリックのような単一の行動データから単純にレコメンダーを学習することは、**クリックデータはノイズが多く、バイアスによって容易に破損する可能性がある**ため[5]、ユーザの実際のユーザ嗜好を誤解することにつながり、その結果、最適でないターゲット行動(購入など)の予測につながる可能性がある。
Meanwhile, only considering purchase data tends to lead to severe cold-start problems [26, 41, 48] and data sparsity problems [23, 27].
一方、購入データのみを考慮すると、深刻なコールドスタート問題[26, 41, 48]やデータスパースティ問題[23, 27]を引き起こす傾向がある。

### 1.0.1. Using multiple types of behavioral data.複数のタイプの行動データを使用する。

How can we use multiple types of auxiliary behavioral data (such as clicks) to enhance the prediction of sparse target user behavior (such as purchases) and thereby improve recommendation performance? Some prior work [2, 12] has used multi-task learning to train recommender systems on both target behavior and multiple types of auxiliary behavior.
複数種類の補助行動データ(クリックなど)を使って、スパースなターゲットユーザー行動(購入など)の予測を強化し、推薦パフォーマンスを向上させるにはどうすればいいのだろうか？いくつかの先行研究[2, 12]では、multi-task学習(=click予測問題とconversion予測問題を学習させる、みたいな??:thinking:)を用いて、target behavior(ターゲット行動)と複数種類の auxiliary behavior(補助行動)の両方について推薦システムを学習している。
Building on recent advances in graph neural networks, Jin et al.[18] encode target behavior and multiple types of auxiliary behavior into a heterogeneous graph and perform convolution operations on the constructed graph for recommendation.
Jinら[18]は、グラフ・ニューラル・ネットワークの最近の進歩に基づき、ターゲット行動と複数種類の補助行動を異種グラフに符号化し、推薦のために構築されたグラフに対して畳み込み演算を行う。
In addition, recent research tries to integrate the micro-behavior of useritem interactions into representation learning in the sequential and session-based recommendation [25, 44, 46].
さらに、最近の研究では、逐次推薦やセッションベースの推薦において、ユーザとアイテムの相互作用のミクロな行動を表現学習(??)に統合することが試みられている[25, 44, 46]。
These publications focus on mining user preferences from user-item interactions, which is different from our task of predicting target behavior from multiple types of user behavior.
これらの出版物は、ユーザとアイテムの相互作用からユーザの嗜好をマイニングすることに焦点を当てており、複数のタイプのユーザ行動からターゲット行動を予測する我々のタスクとは異なる。

### 1.0.2. Limitations of current approaches. 現在のアプローチの限界。

Prior work on using multiple types of behavioral data to improve the prediction of the target behavior in a recommendation setting has two main limitations.
レコメンデーション設定において、ターゲット行動の予測を改善するために複数のタイプの行動データを使用する先行研究には、主に2つの限界がある。

The first limitation concerns the gap between data distributions of different types of behavior.
最初の限界は、異なるタイプの行動のデータ分布間のギャップに関するものである。
This gap impacts the learning of universal and effective user preferences.
このギャップは、普遍的で効果的なユーザ嗜好の学習に影響を与える。
For example, users may have clicked on but not purchased items, resulting in different positive and negative instance distributions across auxiliary and target behaviors.
例えば、ユーザはアイテムをクリックしたが購入しなかった可能性があり、その結果、補助行動とターゲット行動で正と負のインスタンス分布が異なる。
Existing work typically learns separate user preferences for different types of behavior and then combines those preferences to obtain an aggregate user representation.
既存の研究では、通常、異なるタイプの行動に対するユーザの嗜好を個別に学習し、次にそれらの嗜好を組み合わせて集約的なユーザ表現を得る。
We argue that:
我々は次のように主張する：
(i) user preferences learned separately based on different types of behavior may not consistently lead to the true user preferences,
(i)異なるタイプの行動に基づいて別々に学習されたユーザ嗜好は、一貫して真のユーザ嗜好につながらない可能性がある、
and (ii) multiple types of user behavior should reflect similar user preferences; in other words, there should be an underlying universal set of user preferences under different types of behavior of the same user.
(ii)複数のタイプのユーザ行動は、類似したユーザ嗜好を反映するはずである、言い換えれば、同じユーザの異なるタイプの行動の下で、根底に普遍的なユーザ嗜好のセットが存在するはずである。

The second limitation concerns the presence of noise and bias in auxiliary behavioral data, which impacts knowledge extraction and transfer.
2つ目の限界は、補助的な行動データにノイズやバイアスが存在し、それが知識の抽出や伝達に影響を与えることである。
A basic assumption of recommendations based on implicit feedback is that observed interactions between users and items reflect positive user preferences, while unobserved interactions are considered negative training instances.
暗黙フィードバックに基づくレコメンデーションの基本的な仮定は、ユーザとアイテムの間の観察された相互作用はポジティブなユーザの好みを反映し、観察されていない相互作用はネガティブなトレーニングインスタンスとみなされるということである。
However, this assumption seldom holds in reality.
しかし、この仮定が現実に成り立つことはめったにない。
A click may be triggered by popularity bias [5], which does not reflect a positive preference.
クリックは人気バイアス[5]によって引き起こされるかもしれない。
And an unobserved interaction may be attributed to a lack of exposure [6].
また、観察されない相互作用は、exposure(露出)の不足に起因する可能性がある[6]。
Hence, simply incorporating noisy or biased behavioral data may lead to sub-optimal recommendation performance.
したがって、単にノイズの多い、あるいは偏った行動データを取り入れるだけでは、推薦のパフォーマンスが最適化されない可能性がある。

### 1.0.3. Motivation.

![figure1]()

(論文を読んだ感じではこの散布図は、CFで得られたアイテム埋め込みを2次元空間に投影したもの。自社データでCBっぽい記事埋め込みでも試せるかも...!:thinking:)

Our assumption is that multiple types of behavior from the same user (e.g., clicks and purchases) should reflect similar preferences of that user.
私たちの仮定は、**同じユーザからの複数のタイプの行動（例えば、クリックと購入）は、そのユーザの同様の嗜好を反映するはずである**ということです。
To illustrate this assumption, consider Figure 1, which shows distributions of items that two users (𝑢1 and 𝑢2) interacted with (clicks 𝑐 and purchases 𝑝), in the Beibei and Taobao datasets (described in Section 4.2 below).
この仮定を説明するために、2人のユーザ($u_1$ と $u_2$)が相互作用したアイテム(clicks $c$ と 購入 $p$)の分布を示す図1を考えてみよう。
For both users, the items they clicked or purchased are relatively close.
どちらのユーザにとっても、**クリックしたアイテムや購入したアイテムは比較的近い**。
These observations motivate our hypothesis that multiple types of user behavior reflect similar user preferences, which is vital to improve the recommendation performance further.
これらの観察結果は、複数のタイプのユーザ行動が類似したユーザ嗜好を反映しているという我々の仮説を動機づけるものであり、推薦性能をさらに向上させるために不可欠である。

### 1.0.4. Proposed method.

To address the problem of learning from multiple types of auxiliary behavioral data and improve the prediction of the target behavior (and hence recommendation performance), we propose a training framework called multi-behavior alignment (MBA).
複数種類のautxiliary behaviorデータから学習し、target behaviorの予測(ひいては推薦性能)を向上させるという問題に対処するため、我々は**multi-behavior alignment(MBA)と呼ばれる学習フレームワーク**を提案する。
MBA aligns user preferences learned from different types of behavior.
MBAは、さまざまなタイプの行動から学んだユーザの嗜好を調整する。
The key assumption behind MBA is that multiple types of behavior from the same user reflect similar underlying user preferences.
MBAの背後にある重要な仮定は、同じユーザからの複数のタイプの行動は、同様の根本的なユーザの嗜好を反映しているということである。

To address the data distribution limitation mentioned above, we utilize KL-divergence to measure the discrepancy between user models learned from multiple types of auxiliary behavior and target behavior, and then conduct knowledge transfer by minimizing this discrepancy to improve the recommendation performance.
上記のようなデータ分布の制約(=auxiliary behaviorはノイズとバイアスが大きい, target behaviorはスパース性が高い、って話?:thinking:)に対して、KL-ダイバージェンスを利用し、複数種類の補助行動から学習したユーザモデルと対象行動(から学習したユーザモデル?)との不一致度を測定し、この不一致度を最小化することで知識移転を行い、推薦性能の向上を図る。

For the second limitation mentioned above (concerning noise and bias in behavioral data), MBA regards the underlying universal user preferences as a latent variable.
前述の2つ目の限界(行動データにおけるノイズとバイアスに関して)については、MBAは、根底にある普遍的なユーザの嗜好を潜在変数とみなしている。
The variable is then inferred by maximizing the likelihood of multiple types of observed behavioral data while minimizing the discrepancy between models trained on different types of behavioral data.
そして、観測された複数の行動データの尤度を最大化しつつ、**異なる行動データで学習したモデル間の不一致を最小化すること**(=真の嗜好が、各行動の中間にあるような想定??:thinking:)で、変数を推論する。
In this manner, MBA denoises multiple types of behavioral data and enables more effective knowledge transfer across multiple types of user behavior.
このように、MBAは複数のタイプの行動データをノイズ除去し、複数のタイプのユーザ行動にわたってより効果的な知識伝達を可能にする。

To demonstrate the effectiveness of the proposed method, we conduct extensive experiments on two open benchmark datasets and one dataset collected from an operational e-commerce platform.
提案手法の有効性を実証するため、2つのオープンベンチマークデータセットと、運用中のeコマースプラットフォームから収集した1つのデータセットで大規模な実験を行った。
Experimental results show that the proposed MBA framework outperforms related state-of-the-art baselines.
実験結果は、提案するMBAフレームワークが、関連する最新のベースラインを上回ることを示している。

### 1.0.5. Main contributions.

Our main contributions are as follows:
我々の主な貢献は以下の通りである：

- We argue that multiple types of auxiliary and target behavior should reflect similar user preferences, and we propose to infer the true user preferences from multiple types of behavioral data. 我々は、複数種類の補助行動とターゲット行動は類似したユーザ嗜好を反映するはずであると主張し、複数種類の行動データから真のユーザー嗜好を推論することを提案する。

- We propose a learning framework MBA to jointly perform data denoising and knowledge transfer across multiple types of behavioral data to enhance target behavior prediction and hence improve the recommendation performance.本研究では、複数の行動データに対してデータノイズ除去と知識伝達を共同で行うことで、対象行動の予測精度を向上させ、レコメンデーション性能を向上させる学習フレームワークMBAを提案する。

- We conduct experiments on three datasets to demonstrate the effectiveness of the MBA method. MBA法の有効性を実証するため、3つのデータセットで実験を行った。One of these datasets is collected from an operational e-commerce platform, and includes clicks and purchase behavior data.これらのデータセットの1つは、運用中のeコマース・プラットフォームから収集されたもので、クリック数と購買行動データが含まれている。Experimental results show **state-of-the-art** recommendation performance of the proposed MBA method.実験結果は、提案されたMBA手法の最先端の推薦性能を示している。

<!-- ここまで読んだ -->

# 2. Related Work 関連作品

We review prior work on multi-behavior recommendation and on denoising methods for recommendation from implicit feedback.
本稿では、multi-behavio推薦に関する先行研究と、暗黙的フィードバックからの推薦のためのノイズ除去法に関する先行研究をレビューする。(両方とも実務的に興味ある...!)

## 2.1. Multi-behavior recommendation

Unlike conventional implicit feedback recommendation models [15, 21], which train a recommender on a single type of user behavior (e.g., clicks), multi-behavior recommendation models use multiple types of auxiliary behavior data to enhance the recommendation performance on target behavior [1, 7, 12, 18, 33, 37, 39].
従来の暗黙的フィードバック推薦モデル[15, 21]が、単一のタイプのユーザ行動（例えばクリック）に基づいて推薦者を訓練するのとは異なり、複数行動推薦モデルは、複数のタイプの補助行動データを使用して、ターゲット行動に関する推薦性能を向上させる[1, 7, 12, 18, 33, 37, 39]。
Recent studies use multi-task learning to perform joint optimization on learning auxiliary behavior and target behavior.
最近の研究では、**マルチタスク学習を用いて、auxiliary behaviorとtarget behaviorの学習に関する共同最適化**を行う。
For example, Gao et al.[12] propose a multi-task learning framework to learn user preferences from multi-behavior data based on a pre-defined relationship between different behavior.
例えば、Gaoら[12]は、異なる行動間の事前に定義された関係(=behaviorの種類ごとの重み付けとか??)に基づいて、複数の行動データからユーザの嗜好を学習するマルチタスク学習フレームワークを提案している。
Since different behavioral interactions between users and items can form a heterogeneous graph, recent studies also focus on using graph neural network (GNN) to mine the correlations among different types of behavior.
ユーザとアイテムの間の異なる行動の相互作用は、異種グラフを形成することができるため、最近の研究では、グラフ・ニューラル・ネットワーク(GNN)を使用して、異なるタイプの行動間の相関関係をマイニングすることにも焦点を当てている。
For example, Wang et al.[33] uses the auxiliary behavior data to build global item-to-item relations and further improve the recommendation performance of target behavior.
例えば、Wangら[33]は、補助行動データを用いて大域的なアイテム間関係を構築し、対象行動の推薦性能をさらに向上させている。
Jin et al.[18] propose a graph convolutional network (GCN) based model on capturing the diverse influence of different types of behavior and the various semantics of different types of behavior.
Jinら[18]は、異なるタイプの行動の多様な影響と、異なるタイプの行動の多様なセマンティクスを捉える上で、グラフ畳み込みネットワーク（GCN）ベースのモデルを提案している。
Xia et al.[39] incorporate multi-behavior signals through graph-based meta-learning.
Xiaら[39]は、グラフベースのメタ学習によって、複数の行動シグナルを組み込んでいる。
Chen et al.[1] regard the multi-behavior recommendation task as a multirelationship prediction task and train the recommender with an efficient non-sampling method.
Chenら[1]は、multi-behavior推薦タスクを多関係予測タスク(?)とみなし、効率的な非サンプリング法を用いて推薦器を学習する。
Additionally, some studies apply contrastive learning or a variational autoencoder (VAE) to improve the multi-behavior recommender.
さらに、対照学習や変分オートエンコーダ（VAE）を適用して、複数行動レコメンダーを改善する研究もある。
Xuan et al.[42] propose a knowledge graph enhanced contrastive learning framework to capture multi-behavioral dependencies better and solve the data sparsity problem of the target behavior, and Ma et al.[24] propose a VAEbased model to conduct multi-behavior recommendation.
Xuanら[42]は、複数行動の依存関係をよりよく捉え、対象行動のデータ疎性の問題を解決するために、**知識グラフを強化したcontractive learningフレームワークを提案**しており、Maら[24]は、複数行動の推薦を行うためにVAEベースのモデルを提案している。

Another related research field is based on micro-behaviors [25, 44, 46], which utilize the micro-operation sequence in the process of user-item interactions to capture user preferences and predict the next item.
**別の関連する研究分野は、micro-behaviors(?)に基づくもの[25, 44, 46]**で、ユーザとアイテムの相互作用の過程における micro-operationシーケンスを利用して、ユーザの嗜好を把握し、next-itemを予測するものである。
For example, Yuan et al.[44] focus on “sequential patterns” and “dyadic relational patterns” in micro-behaviors, and then use an extended self-attention network to mine the relationship between micro-behavior and user preferences.
例えば、Yuanら[44]は、ミクロ行動における「逐次的パターン」と「ダイアド的関係パターン」に注目し、拡張自己注意ネットワークを用いて、micro-behaviorsとユーザ嗜好の関係をマイニングしている。
This work focuses on mining user preferences from the micro-operation sequence.
この研究では、マイクロ操作シーケンスからユーザの嗜好をマイニングすることに焦点を当てている。

However, existing studies still neglect the different data distributions across multiple types of user behavior, and thus fail to learn accurate and universal user preferences.
しかし、既存の研究では、複数のタイプのユーザ行動にわたる異なるデータ分布が依然として無視されているため、正確で普遍的なユーザ嗜好を学習することができない。
Besides, prior work does not consider the noisy signals of user implicit feedback data, resulting in ineffective knowledge extraction and transfers.
さらに、**先行研究では、ユーザの暗黙的フィードバックデータのノイズ信号を考慮していないため**、効果的な知識抽出と転送ができない。

## 2.2. Recommendation denoising

Existing recommender systems are usually trained with implicit feedback since it is much easier to collect than explicit ratings [28].
既存の推薦システムは、明示的な評価よりもはるかに収集しやすいため、通常、暗黙的なフィードバックで訓練されている[28]。
Recently, some research [17, 32, 36] has pointed out that implicit feedback can easily be corrupted by different factors, such as various kinds of bias [5] or users’ mistaken clicks.
最近、いくつかの研究[17, 32, 36]は、**暗黙のフィードバックは、様々な種類のバイアス[5]やユーザの誤クリックなど、様々な要因によって容易に破損する可能性がある**ことを指摘している。
Therefore, there have been efforts aimed at alleviating the noisy problem of implicit recommendation.
そのため、**implicit recommendation**というノイジーな問題を緩和するための努力がなされてきた。
These efforts include sample selection methods [8– 11, 36, 43], re-weighting methods [3, 30, 32, 32, 35], methods using additional information [19, 22, 45], and methods designing specific denoising architectures [4, 13, 38, 40].
これらの取り組みには、サンプル選択法[8-11, 36, 43](=これはMNARデータに対するunder sampling手法も含まれる??:thinking:)、再重み付け法[3, 30, 32, 35] (=これはIPS重み付けとかが含まれる??:thinking:)、追加情報を利用する方法[19, 22, 45]、特定のノイズ除去アーキテクチャを設計する方法[4, 13, 38, 40](=これはdenoising sequential recommender的なやつ??:thinking:)などがある。

Sample selection methods aim to design more effective samplers for model training.
サンプル選択法は、モデルトレーニングのために、より効果的なサンプラーを設計することを目的としている。
For example, Gantner et al.[11] consider popular but un-interacted items as items that are highly likely to be negative ones, while Ding et al.[8] consider clicked but not purchased items as likely to be negative samples.
例えば、Gantnerら[11]は、人気があるがインタラクションのないアイテムをネガティブなアイテムである可能性が高いアイテムとしており、Dingら[8]は、クリックされたが購入されなかったアイテムをネガティブなサンプルである可能性が高いアイテムとしている。

Re-weighting methods typically identify noisy samples as instances with higher loss values and then assign lower weights to them.
再重み付け法は一般的に、ノイズの多いサンプルを損失値の高いインスタンスとして識別し、それらに低い重みを割り当てる。
For example, Wang et al.[32] discard the large-loss samples with a dynamic threshold in each iteration.
例えば、Wangら[32]は、各反復において、動的閾値で大損失サンプルを破棄している。
Wang et al.[35] utilize the differences between model predictions as the denoising signals.
Wangら[35]は、モデル予測間の差をノイズ除去信号として利用している。

Additional information such as dwell time [19], gaze pattern [45] and auxiliary item features [22] can also be used to denoise implicit feedback.
滞留時間[19]、視線パターン[45]、補助項目特徴[22]などの追加情報も、暗黙的フィードバックのノイズ除去に使用できる。

Methods designing specific denoising architectures improve the robustness of recommender systems by designing special modules.
特定のノイズ除去アーキテクチャを設計する方法は、特別なモジュールを設計することで推薦システムの頑健性を向上させる。
Wu et al.[38] use self-supervised learning on user-item interaction graphs to improve the robustness of graph-based recommendation models.
Wuら[38]は、グラフベースの推薦モデルの頑健性を向上させるために、ユーザーとアイテムの相互作用グラフの自己教師あり学習を使用している。
Gao et al.[13] utilize the self-labeled memorized data as denoising signals to improve the robustness of recommendation models.
Gaoら[13]は、推薦モデルの頑健性を向上させるために、自己ラベル化された記憶データをノイズ除去信号として利用している。

Unlike the work listed above, which does not consider multiple types of user behavior, in this work, we focus on extracting underlying user preferences from (potentially) corrupted multi-behavior data and then conducting knowledge transfer to improve the recommendation performance.
複数のタイプのユーザ行動を考慮しない上記の研究とは異なり、この研究では、**(潜在的に)破損した複数の行動データから根本的なユーザ嗜好を抽出**し、推薦性能を向上させるために知識移転を行うことに焦点を当てる。

<!-- ここまで読んだ! -->

# 3. Method メソッド

In this section, we detail our proposed MBA framework for multibehavior recommendation.
このセクションでは、私たちが提案するマルチ行動推薦のためのMBAフレームワークについて詳しく説明する。
We first introduce notations and the problem formulation in Section 3.1.After that, we describe how to perform multi-behavior alignment on noisy implicit feedback in Section 3.2.Finally, training details are given in Section 3.3.
その後、3.2節でノイズの多い暗黙的フィードバックに対して複数行動のアライメントを行う方法を説明し、最後に3.3節でトレーニングの詳細を述べる。

## 3.1. Notation and problem formulation

We write $u \in U$ and $i \in I$ for a user and an item, where U and I indicate the user set and the item set, respectively.
Uはユーザー集合、Iはアイテム集合を表す。
Without loss of generality, we regard click behavior as the auxiliary behavior and purchase behavior as the target behavior.
一般性を損なわない範囲で、**クリック行動をauxiliary behaviorとし、購買行動をtarget behaviorとする**。
We write $R_f \in \mathbb{R}^{|U| \times |I|}$ for the observed purchase behavior data.
ここで、観察された購買行動データを $R_f \in \mathbb{R}^{|U| \times |I|}$ と表記する。
Specifically, each item 𝑟 𝑓 𝑢,𝑖 ∈ R𝑓 is set to 1 if there is a purchase behavior between user 𝑢 and item 𝑖; otherwise 𝑟 𝑓 𝑢,𝑖 is set as 0.
具体的には、各アイテム $r^{f}_{u,i}$ は、ユーザ $u$ とアイテム $i$ の間に購買行動があれば1とされ、そうでなければ0とされる。
Similarly, we denote R𝑔 ∈ R |U |× |I | as the observed click behavior data, where each 𝑟 𝑔 𝑢,𝑖 ∈ R𝑔 is set as 1 if there is a click behavior between user 𝑢 and item 𝑖; otherwise 𝑟 𝑔 𝑢,𝑖 = 0.
同様に、$R_g \in \mathbb{R}^{|U| \times |I|}$ を観測されたクリック行動データとする。
We use 𝑃 (R𝑓 ) and 𝑃 (R𝑔) to denote the user preference distribution learned from R𝑓 and R𝑔, respectively.
$R_f$ と $R_g$ から学習された**ユーザ嗜好分布**を表すために、それぞれ $P(R_f)$ と $P(R_g)$ を使用する。

We assume that there is an underlying latent true user preference matrix $R_t$ with $r^{t}_{u,i}$ as the true preference of user 𝑢 over item 𝑖.
$R_t$ を潜在的な真のユーザ嗜好の行列とする。
The probabilistic distribution of R𝑡 is denoted as 𝑃 (R𝑡).
R𝑡の確率分布を𝑃 (R𝑡)と表す。
Both the data observation of R𝑓 and R𝑔 is motivated by the latent universal true user preference distribution 𝑃 (R𝑡) plus different kinds of noises or biases.
**$R_f$ と $R_g$ の両方のデータ観測は、潜在的で普遍的な真のユーザ嗜好分布 $P(R_t)$ と、異なる種類のノイズやバイアスによって動機づけられている**。(ふむふむ...!)
Formally, we assume that 𝑃 (R𝑡) follows a Bernoulli distribution and can be approximated by a target recommender model 𝑡𝜃 with 𝜃 as the parameters:
形式的には、$P(R_t)$ はベルヌーイ分布に従うと仮定し、 $\theta$ をパラメータとするターゲット推薦モデル $t_{\theta}$ で近似できる:

$$
r^{t}_{u,i} \sim Bernoulli(t_{\theta}(u,i))
\tag{1}
$$

Since the true user preferences 𝑟 𝑡 𝑢,𝑖 are intractable, we need to introduce the learning signals from the observed 𝑟 𝑓 𝑢,𝑖 and 𝑟 𝑔 𝑢,𝑖 to infer 𝑟 𝑡 𝑢,𝑖.
真のユーザ嗜好 $r^{t}$ は実行不可能であるため、観測された $r^{f}$ と$r^{g}$ から学習信号を導入して $r^{t}$ を推論する必要がある。(添字u, iを省略した)
As a result, we introduce the following models to depict the correlations between the observed user implicit feedback (i.e., 𝑟 𝑓 𝑢,𝑖 and 𝑟 𝑔 𝑢,𝑖 ) and the latent true user preferences 𝑟 𝑡 𝑢,𝑖:
その結果、**観測されたユーザ暗黙フィードバック(i.e. $r^{f}$ と $r^{g}$) と潜在的な真のユーザ嗜好 $r^{t}$ との相関を表す**ために以下のモデルを導入する:

<!-- ここまで読んだ! -->

$$
r^{f}_{u,i} | r^{t}_{u,i} = 0 \sim Bernouli(h^{f}_{\phi}(u,i)) \\
r^{f}_{u,i} | r^{t}_{u,i} = 1 \sim Bernouli(h^{f}_{\varphi}(u,i)) \\
r^{g}_{u,i} | r^{t}_{u,i} = 0 \sim Bernouli(h^{g}_{\phi'}(u,i)) \\
r^{g}_{u,i} | r^{t}_{u,i} = 1 \sim Bernouli(h^{g}_{\varphi'}(u,i)) \\
\tag{2}
$$

where $h^{f}_{\phi}(u,i)$ and $h^{f}_{\varphi}(u,i)$ are parameterized by 𝜙 and 𝜑 in the observed purchase behavior data, respectively, while $h^{g}_{\phi'}(u,i)$ and $h^{g}_{\varphi'}(u,i)$ are parameterized by 𝜙 ′ and 𝜑 ′ in the observed click behavior data respectively.
ここで、$h^{f}_{\phi}(u,i)$ と $h^{f}_{\varphi}(u,i)$ は、それぞれ、観察された購買行動データにて𝜙と𝜑でパラメータ化される。
一方、$h^{g}_{\phi'}(u,i)$ と $h^{g}_{\varphi'}(u,i)$ は観測されたクリック行動データの𝜙と𝜑でそれぞれパラメータ化される。

The target of our task is formulated as follows: given the observed multi-behavior user implicit feedback, i.e., R𝑓 and R𝑔, we aim to train the latent true user preference model 𝑡𝜃 , and then use 𝑡𝜃 to improve the prediction performance on target behavior.
我々のタスクの目標は以下のように定式化される： 観察された複数行動のユーザー暗黙フィードバック、すなわち $R_f$ と $R_g$ が与えられたとき、潜在的な真のユーザー嗜好モデル $t_{\theta}$ を訓練し(=ベルヌーイ分布のパラメータを出力するモデル)、次に $t_{\theta}$ を用いてターゲット行動に関する予測性能を向上させることを目指す。
More precisely, during model inference, we introduce both 𝑃 (Rf ) and 𝑃 (Rt) to perform the target behavior recommendation and use a hyperparameter 𝛽 to balance the 𝑃 (Rt) and 𝑃 (Rf ), which is formulated as:
より正確には、モデル推論時に、targer behavior推薦の性能を向上させる為に $P(R_f)$ と $P(R_t)$ の両方を導入し、$P(R_f)$ と $P(R_t)$のバランスをとるためにハイパーパラメータ $\beta$ を使用する。数式にすると以下:

$$
score = \beta P(R_t) + (1 - \beta)P(R_f)
\tag{3}
$$

(ここで、target behavior の分布 $P(R_f)$ だけを使わないのは、target ehaviorの分布も必ずしも真のユーザ嗜好と一致してるわけじゃないからかな...!:thinking:)
We select items with the highest score as the target behavior recommendation results.
最もスコアの高いitemをtarget behavior推薦の結果として選択する。

## 3.2. Multi-behavior alignment on noisy data ノイズデータに対する

The key motivation for MBA is that multiple types of user behavior should reflect similar user preferences.
MBAの主な動機は、**複数のタイプのユーザ行動が、類似したユーザ嗜好を反映しているはずだ**ということだ。
Hence, Eq.4 is expected to be achieved with the convergence of the training models:
したがって、学習モデルの収束とともに、式.4が達成されることが期待される:

$$
P(R_f) \approx P(R_g) \approx P(R_t)
\tag{4}
$$

(P(R_f)とかはいずれも、モデルによって推論されるやつだよね...!:thinking:)
Therefore, 𝑃 (R𝑓 ) and 𝑃 (R𝑡) should have a relatively small KLdivergence, which is formulated as follows:
したがって、 P(R_f) と $P(R_t)$ は比較的小さなKLdivergenceを持つべきであり、これは以下のように定式化される:

$$
KL[P(R_f) || P(R_t)] = E_{P(R_f)}[log P(R_f) - log P(R_t)]
\tag{5}
$$

(KL divergenceの式。そうそう、KL-divはJS-divと違って、対称性とかないんだった。)

Similarly, we also have the KL-divergence between 𝑃 (R𝑔) and 𝑃 (R𝑡):
P(R_g)とP(R_t)の間のKL-divも同様:

$$
KL[P(R_g) || P(R_t)] = E_{P(R_g)}[log P(R_g) - log P(R_t)]
\tag{6}
$$

However, naively minimizing the above KL-divergence is not feasible since it overlooks the data distribution gaps and correlations between multiple types of behavior.
しかし、**上記のKLダイバージェンスを素朴に最小化することは、データ分布のギャップや複数種類の行動間の相関を見落としてしまうため、実行不可能である**。
To address this issue, we use Bayes’ theorem to rewrite 𝑃 (R𝑡) as follows:
この問題に対処するため、ベイズの定理を用いて 真の嗜好分布 $P(R_t)$ を以下のように書き換える:
(ベイズの定理って、同時確率が2通りの書き方ができる事から導出できるやつだよね...! ex. $P(R_t, R_f) = P(R_t)\cdot P(R_f|R_t) = P(R_f)\cdot P(R_t|R_f)$ これを使うと式7のようになる)

$$
P(R_t) = \frac{P(R_f) P(R_t|R_f)}{P(R_f|R_t)}
= \frac{P(R_g) P(R_t|R_g)}{P(R_g|R_t)}
\tag{7}
$$

By substituting the right part of Eq.7 into Eq.5 and rearranging erms, we obtain the following equation:
式7の右辺を式5に代入し、両側の式を並べ替えると、以下の式が得られる:

$$
\tag{8}
$$

Since 𝐾𝐿[𝑃 (R𝑓 ) ∥𝑃 (R𝑡 | R𝑔)] ≥ 0, the left side of Eq.8 is an approximate lower bound of the logarithm log 𝑃 (R𝑔).
𝐾𝐿[𝑃 (R𝑓)] ∥ (R𝑃 | R𝑓) ≥ 0なので、式.8の左辺は対数log 𝑃 (R𝑔)の近似下界となる。
The bound is satisfied if, and only if, 𝑃 (R𝑓 ) perfectly recovers 𝑃 (R𝑡 | R𝑔), which means 𝑃 (R𝑓 ) trained on the observed target behavior can perfectly approximates the true user preference distribution captured from the auxiliary behavior data.
この境界は、$P(R_f)$ が $P(R_t|R_g)$ を完全に復元する(=両分布が完全に一致する) 場合にのみ満たされます。これは、観察されたtarget behaviorのもとで学習された $P(R_f)$ が、補助行動データから取得された真のユーザ選好分布を完全に近似できることを意味します。
The above condition is in line with the main motivation of the MBA, i.e., different behavior data should reflect similar user preferences.
上記の条件は、MBAの主な動機に沿ったものである。つまり、異なる行動データは、類似したユーザの嗜好を反映すべきである。

We see that the left side of Eq.8 is based on the expectation over 𝑃 (R𝑓 ), which means that we are trying to train 𝑃 (R𝑓 ) with the given corrupted auxiliary behavior data R𝑔 (i.e., the term 𝐸𝑃 (R𝑓 ) [log 𝑃 (R𝑔 | R𝑡)]) and then to transmit the information from 𝑃 (R𝑓 ) to 𝑃 (R𝑡) via the term 𝐾𝐿[𝑃 (R𝑓 ) ∥𝑃 (R𝑡)].
式.8の左辺が $P(R_f)$ に対する期待値に基づいていることがわかる。これは、与えられた破損した補助行動データ $R_g$ (i.e. hogehoge)を用いて $P(R_f)$ を訓練し、そして $P(R_f)$ から $P(R_t)$ に $KL[P(R_f)||P(R_t)]$ という項を経由して情報を伝達しようとしていることを意味する。
Such a learning process is ineffective for learning the true user preference distribution 𝑃 (R𝑡) and the target recommender model 𝑡𝜃 .
このような学習プロセスは、真のユーザ嗜好分布 $P(R_t)$ と対象のレコメンダー・モデル $t_{\theta}$ の学習には効果がありません。
To overcome the above issue, according to Eq.4, when the training process has converged, the preference distributions 𝑃 (R𝑓 ) and 𝑃 (R𝑡) would be close to each other.
上記の問題を克服するために、式.4によれば、学習過程が収束したとき、選好分布 $P(R_f)$ と $P(R_t)$ は互いに近くなる。
As a result, we can change the expectation over 𝑃 (R𝑓 ) to the expectation over 𝑃 (R𝑡) to learn 𝑃 (R𝑡) more effectively.
その結果、$P(R_f)$ に対する期待値を $P(R_t)$ に対する期待値に変更することで、$P(R_t)$ をより効果的に学習することができる。(２つの分布は近くにあるはずだからってこと??:thinking:)
So we modify the left side of Eq.8 as:
そこで、式8の左辺を次のように修正する:
(左辺を修正したので、$=$ が $\approx$ に変わってる...!)

$$
\tag{9}
$$

Similarly, if we substitute the middle part of Eq.7 into Eq.6 and perform similar derivations, we can obtain:
同様に、式7の中央部分を式6に代入し、同様の導出を行えば、次のようになる：
(式9と同様に、$P(R_f)$ の箇所を $P(R_t)$ に近似したので、$=$ が $\approx$ に変わってる...!)

$$
\tag{10}
$$

The left side of Eq.10 is an approximate lower bound of log 𝑃 (R𝑓 ).
式10の左辺はlog 𝑃 (R_1D453 )の近似下界である。
The bound is satisfied only if 𝑃 (R𝑔) perfectly recovers 𝑃 (R𝑡 | R𝑓 ), which means 𝑃 (R𝑔) trained on the observed auxiliary behaviors can perfectly approximate the true user preference distribution captured from the target behavior data.
この境界は $P(R_g)$ が $P(R_t|R_f)$ を完全に復元する場合にのみ満たされます。これは、観察された補助行動に対して学習された𝑃（R𝑔）が、ターゲット行動データから取得された真のユーザ嗜好分布を完全に近似できることを意味します。
Such condition further verifies the soundness of MBA, i.e., multiple types of user behavior are motivated by similar underlying user preferences.
このような条件は、MBAの健全性をさらに検証する。つまり、複数のタイプのユーザ行動は、根底にあるユーザーの嗜好が類似していることが動機となっている。(この文またでてきた...!)
Combining the left side of both Eq.9 and Eq.10 we obtain the loss function as:
式9と式10の左辺を組み合わせると、損失関数は次のようになる：

$$
L = - E_{P(R_t)}[log P(R_g|R_t)] + KL[P(R_f)||P(R_t)]
\\
- E_{P(R_t)}[log P(R_f|R_t)] + KL[P(R_g)||P(R_t)]
\tag{11}
$$

We can see that the loss function aims to maximize the likelihood of data observation (i.e., 𝑃 (R𝑔 | R𝑡) and 𝑃 (R𝑓 | R𝑡)) and minimize the KL-divergence between distributions learned from different user behavior data.
損失関数は、データ観測の尤度(すなわち、$P(R_g|R_t)$ と $P(R_f|R_t)$)を最大化し、異なるユーザ行動データから学習された分布間のKL-divを最小化することを目的としていることがわかる。
(ここで尤度の意味って、ユーザの真の嗜好が1の時にclickが観測されたり、conversionが観測されたりする条件付き確率を、分布のパラメータ側を変数として見たやつ??)

The learning process of MBA serves as a filter to simultaneously denoise multiple types of user behavior and conduct beneficial knowledge transfers to infer the true user preferences to enhance the prediction of the target behavior.
MBAの学習プロセスは、複数のタイプのユーザ行動を同時にノイズ除去するフィルターとして機能し、ターゲット行動の予測を強化するために、真のユーザ嗜好を推論するために有益な知識移転を行う。

<!-- ここまで読んだ -->

## 3.3. Training details トレーニングの詳細

As described in Section 3.1, we learn the user preference distributions $P(R_f)$ and $P(R_g)$ from $R_f$ and $R_g$, respectively.
セクション3.1で説明したように、$R_f$ と $R_g$ から、それぞれユーザの嗜好分布 $P(R_f)$ と $P(R_g)$ を学習する。
In order to enhance the learning stability, we pre-train $P(R_f)$ and $P(R_g)$ in R𝑓 and R𝑔, respectively.
学習の安定性を高めるために、$P(R_f)$ と $P(R_g)$ をそれぞれ $R_f$ と $R_g$ で事前学習する。(クリックモデルをクリックのログだけを使って事前学習する、みたいな...?)
We use the same model structures of our target recommender 𝑡𝜃 as the pre-training model.
事前学習モデルとして、ターゲット・レコメンダー $t_{\theta}$ と同じモデル構造を使用する。
As the training converges, the KL-divergence will gradually approach 0.
トレーニングが収束するにつれて、KLダイバージェンスは徐々に0に近づいていく。
In order to enhance the role of the KL-divergence in conveying information, we set a hyperparameter 𝛼 to enhance the effectiveness of the KL-divergence.
情報伝達におけるKL-ダイバージェンスの役割を強化するために、KL-ダイバージェンスの有効性を高めるハイパーパラメータ $\alpha$ を設定する。
Then we obtain the following training loss function:
すると、次のような学習損失関数が得られる:

$$
L_{MBA} = - E_{P(R_t)}[log P(R_g|R_t)] + \alpha KL[P(R_f)||P(R_t)]
\\
- E_{P(R_t)}[log P(R_f|R_t)] + \alpha KL[P(R_g)||P(R_t)]
\tag{12}
$$

### 3.3.1. Expectation derivation. 期待値の導出。

As described in Section 3.1, both R𝑓 and R𝑔 contain various kinds of noise and bias.
セクション3.1で説明したように、$R_f$ と $R_g$ には様々な種類のノイズとバイアスが含まれている。
In order to infer the latent true user preferences from the corrupted multi-behavior data, we use ℎ 𝑓 𝜙 (𝑢,𝑖) and ℎ 𝑓 𝜑 (𝑢,𝑖) to capture the correlations between the true user preferences and the observed purchase data.
破損した複数行動データから潜在的な真のユーザ嗜好を推論するために、$h^{f}_{\phi}(u,i)$ と $h^{f}_{\varphi}(u,i)$ を用いて、真のユーザ嗜好と観測された購買(target behavior)データ間の相関を捉える。
Similarly, ℎ 𝑔 𝜙′ (𝑢,𝑖) and ℎ 𝑔 𝜑′ (𝑢,𝑖) are used to capture the correlations between the true user preferences and the observed click data, as shown in Eq.2.
同様に、$h^{g}_{\phi}(u,i)$ と $h^{g}_{\varphi}(u,i)$ を用いて、式.2に示すように、真のユーザ嗜好と観測されたクリックデータ(support behavior)との相関を捉えることを試みる。
Specifically, we expand 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] as:
具体的には、$E_{P(R_t)}[log P(R_g|R_t)]$ を次のように展開する:

$$
E_{P(R_t)}[log P(R_g|R_t)]
= \sum_{u,i} E_{r^{t}_{u,i} \sim P(R_t)} [log P(r^{g}_{u,i}|r^{t}_{u,i})]
\tag{13}
= ...
$$

Similarly, the term 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)] can be expanded as:
同様に、$E_{P(R_t)}[log P(R_f|R_t)]$ の項は次のように展開できる：

$$
E_{P(R_t)}[log P(R_f|R_t)] = ...
\tag{14}
$$

By aligning and denoising the observed target behavior and auxiliary behavior data simultaneously, the target recommender 𝑡𝜃 is trained to learn the universal true user preference distribution.
観測されたtarget行動と auxiliary行動データを同時に整列・ノイズ除去することで、ターゲット・レコメンダー $t_{\theta}$ は普遍的な真のユーザ嗜好分布を学習するように訓練される。

### 3.3.2. Alternative model training. 代替モデルのトレーニング。

In the learning stage, we find that directly training 𝑡𝜃 with Eq.12–Eq.14 does not yield satisfactory results, which is caused by the simultaneous update of five models (i.e., ℎ 𝑔 𝜙′ , ℎ 𝑔 𝜑′ , ℎ 𝑓 𝜙 , ℎ 𝑓 𝜑 and 𝑡𝜃 ) in such an optimization process.
学習段階において、式.12-式.14を用いて $t_{\theta}$ を直接学習しても満足のいく結果が得られないことがわかる。(そうなの??) これは、5つのモデル達が同時に更新されるためである。(i.e. $h^{g}_{\phi'}, h^{g}_{\varphi'}, h^{f}_{\phi}, h^{f}_{\varphi}, t_{\theta}$)
These five models may interfere with each other and prevent 𝑡𝜃 from learning well.
これら5つのモデルは互いに干渉し合い、$t_{\theta}$ (=真に得たいモデル) の学習を妨げる可能性がある。
To address this problem, we set two alternative training steps to train the involved models iteratively.
この問題に対処するため、2つの代替学習ステップを設定し、関係するモデルを反復的に学習する。

In the first training step, we assume that a user tends to not click or purchase items that the user dislikes.
最初の学習ステップでは、**ユーザが嫌いな商品はクリックしない、購入しない傾向があると仮定**する。
That is to say, given $r^{t}_{u,i}= 0$ we have $r^{f}_{u,i} \approx 0$ and $r^{g}_{u,i} \approx 0$, so we have ℎ 𝑓 𝜙 ≈ 0 and ℎ 𝑔 𝜙′ ≈ 0 according to Eq.2.
これはつまり、真の嗜好 $r^{t}_{u,i}= 0$ の場合、$r^{f}_{u,i} \approx 0$ と $r^{g}_{u,i} \approx 0$ が成立する、つまり $h^{f}_{\varphi} \approx 0$ と $h^{g}_{\varphi'} \approx 0$ が成立するということである。
Thus in this step, only the models ℎ 𝑓 𝜑 , ℎ 𝑔 𝜑′ and 𝑡𝜃 are trained.
なのでこのステップでは、3つのモデル $h^{f}_{\varphi}, h^{g}_{\varphi'}, t_{\theta}$ のみを学習させる。
Then Eq.13 can be reformulated as:
そうすると、式.13は次のように定式化できる:

$$
\tag{15}
$$

where
ここで、

$$
\tag{}
$$

Meanwhile, Eq.14 can be reformulated as:
一方、式.14は次のように定式化できる:

$$
\tag{16}
$$

where
ここで、

$$
\tag{}
$$

Here, we denote 𝐶1 as a large positive hyperparameter to replace − logℎ 𝑔 𝜙′ (𝑢,𝑖) and − logℎ 𝑓 𝜙 (𝑢,𝑖).
ここでは、-logℎ ᑔ ↪Ll_1D719′ (𝑢,𝑖)と-logℎ 𝑓を置き換えるために、$C_1$ を大きな正のハイパーパラメータとする。

In the second training step, we assume that a user tends to click and purchase the items that the user likes.
2つ目の学習ステップでは、**ユーザが気に入った商品をクリックして購入する傾向があると仮定**する。
That is to say, given 𝑟 𝑡 𝑢,𝑖 = 1 we have 𝑟 𝑓 𝑢,𝑖 ≈ 1 and 𝑟 𝑔 𝑢,𝑖 ≈ 1, so we have ℎ 𝑓 𝜑 ≈ 1 and ℎ 𝑔 𝜑′ ≈ 1 according to Eq.2.
これはつまり、真の嗜好 $r^{t}_{u,i}= 1$ の場合、$r^{f}_{u,i} \approx 1$ と $r^{g}_{u,i} \approx 1$ が成立する、つまり $h^{f}_{\phi} \approx 1$ と $h^{g}_{\phi'} \approx 1$ が成立するということである。
Thus in this step, only the models ℎ 𝑓 𝜙 , ℎ 𝑔 𝜙′ and 𝑡𝜃 will be updated.
なのでこのステップでは、3つのモデル $h^{f}_{\phi}, h^{g}_{\phi'}, t_{\theta}$ のみを学習させる。

Then Eq.13 can be reformulated as:
そうすると、式.13は次のように定式化できる:

$$
\tag{17}
$$

where
ここで

$$
\tag{}
$$

Eq.14 can be reformulated as:
(同様に)式.14は次のように定式化できる:

$$
\tag{18}
$$

where
ここで、

$$
\tag{}
$$

𝐶2 is a large positive hyperparameter to replace − log(1−ℎ 𝑔 𝜑′ (𝑢,𝑖)) and − log(1 − ℎ 𝑓 𝜑 (𝑢,𝑖)).
$C_2$ は、-log(1-Ȑ (↪Ll_1D46,𝑖)) と - log(1 - 𝜑 (↪Ll_1D462,𝑖)) を置き換える大きな正のハイパーパラメータである。

<!-- ここまで読んだ(一応) -->

### 3.3.3. Training procedure. トレーニングの手順

In order to facilitate the description of sampling and training process, we divide 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] and 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)] into four parts (see Eq.15 to Eq.18), namely click positive loss (𝐿𝐶𝑃 and 𝐿 ′ 𝐶𝑃 ), click negative loss (𝐿𝐶𝑁 and 𝐿 ′ 𝐶𝑁 ), purchase positive loss (𝐿𝑃𝑃 and 𝐿 ′ 𝑃𝑃 ), and purchase negative loss (𝐿𝑃𝑁 and 𝐿 ′ 𝑃𝑁 ).
サンプリングとトレーニングのプロセスの説明を容易にするために、𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] と 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)] を 4つの部分に分割する(式 15 ~ 式18)。
hogehoge
Each sample in the training set can be categorized into one of three situations: (i) clicked and purchased, (ii) clicked but not purchased, and (iii) not clicked and not purchased.
**トレーニングセットの各サンプルは、3つの状況のいずれかに分類される**(うんうん:thinking:) : (i) クリックされ購入された、(ii) クリックされたが購入されなかった、(iii) クリックされず購入されなかった。
The three situations involve different terms in 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑔 | R𝑡)] and 𝐸𝑃 (R𝑡 ) [log 𝑃 (R𝑓 | R𝑡)].
hogehoge
In situation (i), each sample involves the 𝐿𝐶𝑃 and 𝐿𝑃𝑃 (or 𝐿 ′ 𝐶𝑃 and 𝐿 ′ 𝑃𝑃 in the alternative training step).
状況(i)では、各サンプルは𝐿𝑃と𝑃（または代替学習ステップでは𝑃と𝐿）を含む。
In situation (ii), each sample involves the 𝐿𝐶𝑃 and 𝐿𝑃𝑁 (or 𝐿 ′ 𝐶𝑃 and 𝐿 ′ 𝑃𝑁 in the alternative training step).
状況(ii)では、各サンプルは𝐿𝐶𝑃（または代替学習ステップでは 𝐿 𝑃 𝐿）を含む。
In situation (iii), each sample involves the 𝐿𝐶𝑁 and 𝐿𝑃𝑁 (or 𝐿 ′ 𝐶𝑁 and 𝐿 ′ 𝑃𝑁 in the alternative training step).
状況(iii)では、各サンプルは𝐿𝑁（または代替学習ステップでは𝑃𝐿）と𝑁（または𝑃𝑁）を含む。
We then train MBA according to the observed multiple types of user behavior data in situations (i) and (ii), and use the samples in situation (iii) as our negative samples.
そして、状況(i)と(ii)で観測された複数種類のユーザ行動データに従ってMBAを訓練し、状況(iii)のサンプルを負サンプルとして使用する。
Details of the training process for MBA are provided in Algorithm 1.
MBAのトレーニングプロセスの詳細は、アルゴリズム1に記載されている。

# 4. Experimental settings 実験的設定

## 4.1. Experimental questions 実験問題

Our experiments are conducted to answer the following research questions: (RQ1) How do the proposed methods perform compared with state-of-the-art recommendation baselines on different datasets? (RQ2) How do the proposed methods perform compared with other denoising frameworks? (RQ3) Can MBA help to learn universal user preferences from users’ multiple types of behavior? (RQ4) How do the components and the hyperparameter settings affect the recommendation performance of MBA?
我々の実験は以下の研究課題に答えるために行われた： (RQ1)提案手法は、異なるデータセットにおいて、最新の推薦ベースラインと比較してどのように動作するか？(RQ2) 提案手法は他のノイズ除去フレームワークと比較してどのようなパフォーマンスを示すか？(RQ3) MBAはユーザの複数種類の行動から普遍的なユーザ嗜好を学習するのに役立つか？(RQ4) 構成要素とハイパーパラメータの設定はMBAの推薦性能にどのような影響を与えるか？

## 4.2. Datasets データセット

To evaluate the effectiveness of our method, we conduct a series of experiments on three real-world benchmark datasets, including Beibei1 [12], Taobao2 [47], and MBD (multi-behavior dataset), a dataset we collected from an operational e-commerce platform.
本手法の有効性を評価するため、Beibei1 [12]、Taobao2 [47]、MBD (multi-behavior dataset)の3つの実世界ベンチマークデータセットで一連の実験を行った。
The details are as follows: (i) The Beibei dataset is an open dataset collected from Beibei, the largest infant product e-commerce platform in China, which includes three types of behavior, click, add-to-cart and purchase.
詳細は以下の通りである： (i)Beibeiデータセットは、中国最大の幼児向け商品ECプラットフォームであるBeibeiから収集されたオープンデータセットであり、クリック、カートに入れる、購入の3種類の行動が含まれる。
This work uses two kinds of behavioral data, clicks and purchases.
この作品では、クリックと購入という2種類の行動データを使用している。
(ii) The Taobao dataset is an open dataset collected from Taobao, the largest e-commerce platform in China, which includes three types of behavior, click, add to cart and purchase.
(ii)タオバオデータセットは、中国最大の電子商取引プラットフォームであるタオバオから収集されたオープンデータセットであり、クリック、カートに入れる、購入の3種類の行動を含む。
In this work, we use clicks and purchases of this dataset.
本研究では、このデータセットのクリック数と購入数を使用する。
(iii) The MBD dataset is collected from an operational e-commerce platform, and includes two types of behavior, click and purchase.
(iii) MBDデータセットは、運用中のeコマース・プラットフォームから収集され、クリックと購入の2種類の行動を含む。
For each dataset, we ensure that users have interactions on both types of behavior, and we set click data as auxiliary behavior data and purchase data as target behavior data.
各データセットについて、ユーザーが両方の行動に関するインタラクションを持っていることを確認し、クリックデータを補助行動データ、購入データをターゲット行動データとする。
Table 1 shows the statistics of our datasets
表1にデータセットの統計を示す。

## 4.3. Evaluation protocols 評価プロトコル

We divide the datasets into training and test sets with a ratio of 4:1.
データセットを訓練セットとテストセットに4:1の比率で分割する。
We adopt two widely used metrics Recall@𝑘 and NDCG@𝑘.
我々は、広く使われている2つの指標Recall@\_1D458とNDCG@\_1D458を採用する。
Recall@𝑘 represents the coverage of true positive items that appear in the final top-𝑘 ranked list.
Recall@↪Ll458↩は、最終的な上位↪Ll458位リストに表示される真正項目のカバー率を表す。
NDCG@𝑘 measures the ranking quality of the final recommended items.
NDCG@\_1D458 は、最終的な推奨項目のランキング品質を測定する。
In our experiments, we use the setting of 𝑘 = 10, 20.
実験では、𝑘 = 10, 20の設定を使用した。
For our method and the baselines, the reported results are the average values over all users.
我々の方法とベースラインについて、報告された結果は全ユーザーの平均値である。
For every result, we conduct the experiments three times and report the average values.
すべての結果について、実験を3回行い、その平均値を報告する。

## 4.4. Baselines ベースライン

To demonstrate the effectiveness of our method, we compare MBA with several state-of-the-art methods.
本手法の有効性を実証するため、MBAをいくつかの最新手法と比較する。
The methods used for comparison include single-behavior models, multi-behavior models, and recommendation denoising methods.
比較に使用した手法には、単一行動モデル、複数行動モデル、推薦ノイズ除去法などがある。
The single-behavior models that we consider are: (i) MF-BPR [28], which uses bayesian personalized ranking (BPR) loss to optimize matrix factorization.
我々が考慮する単一行動モデルは以下の通りである： (i) MF-BPR [28]、これは行列分解を最適化するためにベイジアンパーソナライズドランキング(BPR)損失を使用する。
(ii) NGCF [34], which encodes collaborative signals into the embedding process through multiple graph convolutional layers and models higher-order connectivity in user-item graphs.
(ii)NGCF[34]は、複数のグラフ畳み込み層を通して埋め込みプロセスに協調信号をエンコードし、ユーザー項目グラフの高次の接続性をモデル化する。
(iii) LightGCN [15], which simplifies graph convolution by removing the matrix transformation and non-linear activation.
(iii) LightGCN [15]は、行列変換と非線形活性化を除去することで、グラフ畳み込みを単純化する。
We use the BPR loss to optimize LightGCN.
BPRロスを利用してLightGCNを最適化する。
The multi-behavior models that we consider are: (i) MB-GCN [18], which constructs a multi-behavior heterogeneous graph and uses GCN to perform behavior-aware embedding propagation.
我々が検討する複数行動モデルは以下の通りである： (i)MB-GCN[18]は、マルチ行動異種グラフを構築し、GCNを使用して行動を意識した埋め込み伝搬を実行する。
(ii) MB- GMN [39], which incorporates multi-behavior pattern modeling with the meta-learning paradigm.
(ii)MB-GMN[39]は、メタ学習パラダイムによる複数行動パターン・モデリングを組み込んだものである。
(iii) CML [37], which uses a new multi-behavior contrastive learning paradigm to capture the transferable user-item relationships from multi-behavior data.
(iii)CML[37]は、新しい複数行動対照学習パラダイムを用い、複数行動データから伝達可能なユーザーとアイテムの関係を捉える。
To verify that the proposed method improves performance by denoising implicit feedback, we also introduce the following denoising frameworks: (i) WBPR [11], which is a re-sampling-based method which considers popular, but un-interacted items are highly likely to be negative.
提案手法が暗黙的フィードバックをノイズ除去することで性能が向上することを検証するために、以下のノイズ除去フレームワークも紹介する： (i)WBPR[11]は、再サンプリングに基づく手法であり、人気のある、しかし対話されていない項目は否定的である可能性が高いと考える。
(ii) T-CE [32], which is a re-weighting based method which discards the large-loss samples with a dynamic threshold in each iteration.
(ii)T-CE[32]は、各反復において動的な閾値で損失の大きいサンプルを破棄する、再重み付けに基づく手法である。
(iii) DeCA [35], which is a newly proposed denoising method that utilizes the agreement predictions on clean examples across different models and minimizes the KL-divergence between the real user preference parameterized by two recommendation models.
(iii) DeCA [35]は、新たに提案されたノイズ除去手法であり、異なるモデル間のクリーンな例における一致予測を利用し、2つの推薦モデルによってパラメータ化された実際のユーザの嗜好間のKLダイバージェンスを最小化する。
(iv) SGDL [13], which is a new denoising paradigm that utilizes self-labeled memorized data as denoising signals to improve the robustness of recommendation models.
(iv)SGDL[13]は、推薦モデルの頑健性を向上させるために、自己ラベル化された記憶データをノイズ除去信号として利用する新しいノイズ除去パラダイムである。

## 4.5. Implementation details 実装の詳細

We implement our method with PyTorch.3 Without special mention, we set MF as our base model 𝑡𝜃 since MF is still one of the best models for capturing user preferences for recommendations [29].
特に言及することなく、MFをベースモデル𝑡として設定します。MFは、レコメンデーションのためのユーザの嗜好を捉えるための最良のモデルの1つです[29]。
The model is optimized by Adam [20] optimizer with a learning rate of 0.001, where the batch size is set as 2048.
このモデルは、Adam [20]オプティマイザによって、学習率0.001、バッチサイズ2048で最適化される。
The embedding size is set to 32.
埋め込みサイズは32に設定されている。
The hyperparameters 𝛼, 𝐶1 and 𝐶2 are search from { 1, 10, 100, 1000 }.
ハイパーパラメータǖ, 𝐶1, 𝐶2は{ 1, 10, 100, 1000 }から探索される。
𝛽 is search from { 0.7, 0.8, 1 }.
↪L_1FD↩は{ 0.7, 0.8, 1 }の中から探す。
To avoid over-fitting, 𝐿2 normalization is searched in { 10−6 , 10−5 , .
オーバーフィットを避けるため、 ↪Lu_1D43F の正規化は { 10-6 , 10-5 , .
..
..
, 1 }.
, 1 }.
Each training step is formed by one interacted example, and one randomly sampled negative example for efficient computation.
各訓練ステップは、効率的な計算のために、1つの相互作用のある例と1つのランダムにサンプリングされた負の例で形成される。
We use Recall@20 on the test set for early stopping if the value does not increase after 20 epochs.
20エポック後に値が増加しない場合は、テストセットのRecall@20を使用して早期停止を行う。
For the hyperparameters of all recommendation baselines, we use the values suggested by the original papers with carefully finetuning on the three datasets.
すべての推薦ベースラインのハイパーパラメータについては、3つのデータセットで慎重に微調整を行いながら、元の論文で示唆された値を使用している。
For all graph-based methods, the number of graph-based message propagation layers is fixed at 3.
すべてのグラフベースの手法において、グラフベースのメッセージ伝搬レイヤーの数は3に固定されている。

# 5. Experimental Results 実験結果

## 5.1. Performance comparison (RQ1) パフォーマンス比較（RQ1）

To answer RQ1, we conduct experiments on the Beibei, Taobao and MBD datasets.
RQ1に答えるため、Beibei、Taobao、MBDのデータセットで実験を行った。
The performance comparisons are reported in Table 2.
性能比較を表2に示す。
From the table, we have the following observations.
表から、我々は次のような見解を得た。
First, the proposed MBA method achieves the best performance and consistently outperforms all baselines across all datasets.
まず、提案されたMBA法は最高の性能を達成し、すべてのデータセットにおいてすべてのベースラインを一貫して上回る。
For instance, the average improvement of MBA over the strongest baseline is approximately 6.3% on the Beibei dataset, 6.6% on the Taobao dataset and 1.5% on the MBD dataset.
例えば、最強のベースラインに対するMBAの平均改善率は、Beibeiデータセットで約6.3%、Taobaoデータセットで6.6%、MBDデータセットで1.5%である。
These improvements demonstrate the effectiveness of MBA.
これらの改善は、MBAの有効性を証明している。
We contribute the significant performance improvement to the following two reasons: (i) we align the user preferences based on two types of two behavior, transferring useful information from the auxiliary behavior data to enhance the performance of the target behavior predictions; (ii) noisy interactions are reduced through preference alignment, which helps to improve the learning of the latent universal true user preferences.
性能の大幅な向上は、以下の2つの理由による： (i)2種類の2つの行動に基づくユーザ嗜好を整列させ、補助行動データから有用な情報を転送し、目標行動予測の性能を向上させる。(ii)嗜好の整列によりノイズの多い相互作用が減少し、潜在的で普遍的な真のユーザ嗜好の学習を向上させる。
Second, except CML the multi-behavior models outperform the single-behavior models by a large margin.
第二に、CMLを除いて、複数行動モデルは単一行動モデルを大きく上回っている。
This reflects the fact that adding auxiliary behavior information can improve the recommendation performance of the target behavior.
これは、補助的な行動情報を追加することで、対象行動の推薦性能が向上することを反映している。
We conjecture that CML cannot achieve satisfactory performance because it incorporates the knowledge contained in auxiliary behavior through contrastive meta-learning, which introduces more noisy signals.
私たちは、CMLが満足のいく性能を達成できないのは、対照的なメタ学習によって補助動作に含まれる知識を取り込むため、よりノイズの多い信号が導入されるからだと推測している。
Furthermore, we compare MBA with the best single-behavior model (NGCF on the Beibei and MBD datasets, LightGCN on the Taobao dataset), and see that MBA achieves an average improvement of 12.4% on the Beibei dataset, 26.8% on the Taobao dataset and 15.3% on the MBD dataset.
さらに、MBAを最良の単一行動モデル（BeibeiデータセットとMBDデータセットではNGCF、TaobaoデータセットではLightGCN）と比較すると、MBAはBeibeiデータセットで平均12.4%、Taobaoデータセットで26.8%、MBDデータセットで15.3%の改善を達成していることがわかる。
To conclude, the proposed MBA approach consistently and significantly outperforms related single-behavior and multi-behavior recommendation baselines on the purchase prediction task.
結論として、提案するMBAアプローチは、購買予測タスクにおいて、関連する単一行動および複数行動推薦ベースラインを一貫して有意に凌駕する。

## 5.2. Denoising (RQ2)

Table 3 reports on a performance comparison with existing denoising frameworks on the Beibei, Taobao and MBD datasets.
表3は、Beibei、Taobao、MBDデータセットにおける既存のノイズ除去フレームワークとの性能比較である。
The results demonstrate that MBA can provide more robust recommendations and improve overall performance than competing approaches.
その結果、MBAは競合するアプローチよりも強固な推奨を提供し、全体的なパフォーマンスを向上させることができることが実証された。
Most of the denoising baselines do not obtain satisfactory results, even after carefully tuning their hyperparameters.
ほとんどのノイズ除去ベースラインは、ハイパーパラメータを注意深く調整しても、満足のいく結果が得られない。
Only WBPR can outperform normal training in some cases.
WBPRだけが、場合によっては通常のトレーニングを上回ることができる。
However, MBA consistently outperforms normal training and other denoising frameworks.
しかし、MBAは通常のトレーニングや他のノイズ除去フレームワークよりも常に優れている。
We think the reasons for this are as follows: (i) In MBA, we use the alignment between multi-behavior data as the denoising signal and then transmit information from the multi-behavior distribution to the latent universal true user preference distribution.
その理由は以下のように考えられる： (i)MBAでは、マルチ行動データ間のアライメントをノイズ除去信号として使用し、マルチ行動分布から潜在的な普遍的な真のユーザー嗜好分布に情報を伝達する。
This learning process facilitates knowledge transfer across multiple types of user behavior and filters out noisy signals.
この学習プロセスは、複数のタイプのユーザー行動にわたる知識の伝達を容易にし、ノイズの多い信号をフィルタリングする。
(ii) In the original papers of the compared denoising baselines, testing is conducted based on explicit user-item ratings.
(ii)比較されたノイズ除去ベースラインのオリジナル論文では、テストは明示的なユーザー項目の評価に基づいて実施されている。
However, our method does not use any explicit information like ratings, only implicit interaction data is considered.
しかし、我々の方法では、視聴率のような明示的な情報は一切使用せず、暗黙的な相互作用データのみを考慮する。
To further explore the generalization capability of MBA, we also adopt LightGCN as our base model (i.e., using LightGCN as𝑡𝜃 ).
MBAの汎化能力をさらに探求するために、LightGCNもベースモデルとして採用します（つまり、LightGCNを𝑡𝜃として使用します）。
The results are also shown in Table 3.
結果は表3にも示されている。
We see that MBA is still more effective than the baseline methods.
MBAは依然としてベースライン方式よりも効果的であることがわかる。
We find that LightGCN-based MBA does not perform as well as MF-based MBA on the Beibei and Taobao datasets.
LightGCNベースのMBAは、BeibeiとTaobaoのデータセットでは、MFベースのMBAほどのパフォーマンスを示さないことがわかった。
We think the possible reasons are as follows: (i) LightGCN is more complex than MF, making MBA more difficult to train; (ii) LightGCN may be more sensitive to noisy signals due to the aggregation of neighbourhoods, resulting in a decline in the MBA performance compared to using MF as the base model.
考えられる理由は以下の通りである： (i)LightGCNはMFよりも複雑であるため、MBAの訓練がより困難である。(ii)LightGCNは近隣の集合体であるため、ノイズの多い信号に対してより敏感である可能性があり、その結果、MFをベースモデルとして使用する場合よりもMBAの性能が低下する。
To conclude, the proposed MBA can generate more accurate recommendation compared with existing denoising frameworks.
結論として、提案されたMBAは、既存のノイズ除去フレームワークと比較して、より正確な推薦を生成することができる。

## 5.3. User preferences visualization (RQ3) ユーザー嗜好の可視化（RQ3）

To answer RQ3, we visualize the distribution of users’ interacted items.
RQ3に答えるために、ユーザーの対話アイテムの分布を可視化する。
We select two users in the Beibei, Taobao and MBD datasets and draw their behavior distributions using the parameters obtained from an MF model trained on the purchase behavior data and the parameters obtained from MBA, respectively.
Beibei、Taobao、MBDのデータセットからそれぞれ2人のユーザーを選び、購買行動データで学習したMFモデルから得られたパラメータとMBAから得られたパラメータを用いて行動分布を描く。
Figure 2 visualizes the results.
図2はその結果を視覚化したものである。
From the figure, we observe that for one user, the clicked items and purchased items distributions of MBA stay much closer than that of MF.
図から、あるユーザーについて、MBAのクリックされたアイテムと購入されたアイテムの分布は、MFの分布よりもずっと近いことがわかる。
The observation indicates that MBA can successfully align multiple types of user behavior and infer universal and accurate user preferences.
この観察結果は、MBAが複数のタイプのユーザー行動をうまく調整し、普遍的で正確なユーザー嗜好を推論できることを示している。
Besides, we see that different users in MBA have more obvious separations than users in MF, which implies that MBA provides more personalized user-specific recommendation than MF.
さらに、MBAの異なるユーザーはMFのユーザーよりも明らかに分離しており、これはMBAがMFよりもパーソナライズされたユーザー別推薦を提供していることを示唆している。

## 5.4. Model investigation (RQ4) モデル調査（RQ4）

5.4.1 Ablation study.
5.4.1 アブレーション研究。
Regarding RQ4, we conduct an ablation study (see Table 4) on the following two settings: (i) MBA-KL: we remove KL-divergence when training MBA; and (ii) MBA-PT: we co-train the 𝑃 (R𝑓 ) and 𝑃 (R𝑔) in MBA instead of pre-training.
RQ4に関しては、以下の2つの設定でアブレーションスタディを行った（表4参照）： (i) MBA-KL： (i)MBA-KL：MBAを訓練する際にKL-発散を除去する： MBA-PT: 𝑃 (R_1D454) と 𝑃 (R_1D454)を事前学習の代わりにMBAで協調学習させる。
The results show that both parts (KL-divergence and pre-trained models) are essential to MBA because removing either will lead to a performance decrease.
その結果、KLダイバージェンスと事前訓練モデルの両方がMBAにとって不可欠であることがわかった。
Without KL-divergence, we see the performance drops substantially in terms of all metrics.
KL-ダイバージェンスがないと、すべての測定基準においてパフォーマンスが大幅に低下することがわかる。
Hence, the KL-divergence helps align the user preferences learned from different behaviors, thus improving the recommendation performance.
したがって、KL-ダイバージェンスは、異なる行動から学習されたユーザーの嗜好を調整するのに役立ち、推薦性能を向上させる。
Without pre-trained models, the results drop dramatically, especially in the Taobao dataset, which indicates that it is hard to cotrain 𝑃 (R𝑓 ) and 𝑃 (R𝑔) with MBA.
これは、MBAで𝑃 (R_1D443) と𝑃 (R_1D444) を共 訓練するのが難しいことを示している。
Using a pre-trained model can reduce MBA’s complexity and provide prior knowledge so that it can more effectively extract the user’s real preferences from the different types of behavior distributions.5.4.2 Hyperparameter study.
事前に訓練されたモデルを使用することで、MBAの複雑さを軽減し、事前知識を提供することができるため、さまざまなタイプの行動分布からユーザーの真の嗜好をより効果的に抽出することができる。
Next, we conduct experiments to examine the effect of different parameter settings on MBA.
次に、さまざまなパラメータ設定がMBAに与える影響を調べる実験を行う。
Figure 3 shows the effect of 𝛼, which is used to control the weight of the KL-divergence in conveying information.
図3は、情報伝達におけるKLダイバージェンスの重みを制御するために使用される↪Ll_1FC の効果を示している。
On the Beibei dataset, the performance of MBA is affected when the 𝛼 is greater than or equal to 100.
Beibeiデータセットでは、 ↪Ll_1D6FC が100以上の場合、MBAの性能に影響が出る。
Thus, when dominated by KL-divergence, MBA’s performance will be close to that of the pre-trained models.
したがって、KL-ダイバージェンスに支配される場合、MBAの性能は事前学習済みモデルの性能に近くなる。
On the Taobao and MBD datasets, when 𝛼 is greater than or equal to 100, MBA will gradually converge, with a relatively balanced state between the KL-divergence and the expectation term.
タオバオとMBDのデータセットでは、Ǽが100以上の場合、MBAは徐々に収束し、KL-発散と期待項の間の比較的バランスのとれた状態になる。
Under this setting, MBA achieves the best performance.
この設定では、MBAが最高のパフォーマンスを発揮する。

# 6. Conclusion 結論

In this work, we have focused on the task of multi-behavior recommendation.
本研究では、複数の行動を推薦するタスクに焦点を当てた。
We conjectured that multiple types of behavior from the same user reflect similar underlying user preferences.
私たちは、同じユーザーの複数のタイプの行動は、根底にあるユーザーの好みを反映していると推測した。
To tackle the challenges of the gap between data distributions of different types of behavior and the challenge of behavioral data being noisy and biased, we proposed a learning framework, namely multi-behavior alignment (MBA), which can infer universal user preferences from multiple types of observed behavioral data, while performing data denoising to achieve beneficial knowledge transfer.
異なる行動タイプのデータ分布のギャップや、行動データにノイズや偏りがあるという課題に対して、我々は、データノイズ除去を行いながら、観測された複数種類の行動データから普遍的なユーザの嗜好を推論し、有益な知識伝達を実現する学習フレームワーク、マルチ行動アライメント(MBA)を提案した。
Extensive experiments conducted on three real-world datasets showed the effectiveness of the proposed method.
3つの実世界データセットで行った広範な実験により、提案手法の有効性が示された。
Our method proves the value of mining the universal user preferences from multi-behavior data for the implicit feedback-based recommendation.
本手法は、暗黙のフィードバックに基づく推薦のために、複数の行動データから普遍的なユーザの嗜好をマイニングすることの価値を証明する。
However, a limitation of MBA is that it can only align between two types of behavioral data.
しかし、MBAの限界は、2種類の行動データ間でしか整合が取れないことである。
As to our future work, we aim to perform alignment on more types of user behavior.
今後の課題としては、より多くの種類のユーザー行動に対してアライメントを行うことを目指している。
In addition, we plan to develop ways of conducting more effective and efficient model training.
さらに、より効果的で効率的なモデル・トレーニングの方法を開発する予定だ。
