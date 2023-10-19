## 0.1. link リンク

- https://arxiv.org/abs/2308.05972

## 0.2. title タイトル

Augmented Negative Sampling for Collaborative Filtering
協調フィルタリングのための拡張ネガティブサンプリング

## 0.3. abstract 抄録

Negative sampling is essential for implicit-feedback-based collaborative filtering, which is used to constitute negative signals from massive unlabeled data to guide supervised learning.
**ネガティブサンプリングは、教師あり学習を導くために、大量のラベルなしデータからネガティブシグナルを構成するために使用される**、implicitフィードバックベースの協調フィルタリングに不可欠である。
The stateof-the-art idea is to utilize hard negative samples that carry more useful information to form a better decision boundary.
最先端のアイデアは、より良い決定境界を形成するために、**より有用な情報を持つハードネガティブサンプル**を利用することである。
To balance efficiency and effectiveness, the vast majority of existing methods follow the two-pass approach, in which the first pass samples a fixed number of unobserved items by a simple static distribution and then the second pass selects the final negative items using a more sophisticated negative sampling strategy.
効率と有効性のバランスをとるため、既存の手法の大部分は2パス・アプローチに従っており、1パス目は単純な静的分布によって固定数の未観測項目をサンプリングし、2パス目はより洗練されたネガティブ・サンプリング戦略を用いて最終的なネガティブ項目を選択する。
However, selecting negative samples from the original items in a dataset is inherently restricted due to the limited available choices, and thus may not be able to contrast positive samples well.
しかし、データセットのオリジナル項目からネガティブサンプルを選択することは、利用可能な選択肢が限られているため、本質的に制約があり、ポジティブサンプルをうまく対比できない可能性がある。
In this paper, we confirm this observation via carefully designed experiments and introduce two major limitations of existing solutions: ambiguous trap and information discrimination.
本稿では、入念に設計された実験によってこの観察を確認し、既存の解決策の2つの大きな限界を紹介する：曖昧な罠」と「情報の識別」である。

Our response to such limitations is to introduce “augmented” negative samples that may not exist in the original dataset.
このような制限に対する我々の対応は、元のデータセットには存在しないかもしれない「増強された」ネガティブサンプルを導入することである。
This direction renders a substantial technical challenge because constructing unconstrained negative samples may introduce excessive noise that eventually distorts the decision boundary.
なぜなら、制約のない負サンプルを構築することは、過剰なノイズを導入し、最終的に決定境界を歪めてしまう可能性があるからである。
To this end, we introduce a novel generic augmented negative sampling (ANS) paradigm and provide a concrete instantiation.
この目的のために、我々は新しい一般的な拡張ネガティブサンプリング（ANS）パラダイムを導入し、具体的なインスタンス化を提供する。
First, we disentangle hard and easy factors of negative items.
まず、ネガティブ項目のハード要因とイージー要因を分離する。
Next, we generate new candidate negative samples by augmenting only the easy factors in a regulated manner: the direction and magnitude of the augmentation are carefully calibrated.
次に、調整された方法で簡単な因子のみを増強することにより、新しい負サンプル候補を生成する：増強の方向と大きさは注意深く調整される。
Finally, we design an advanced negative sampling strategy to identify the final augmented negative samples, which considers not only the score function used in existing methods but also a new metric called augmentation gain.
最後に、既存の手法で使用されているスコア関数だけでなく、オーグメンテーションゲインと呼ばれる新しい指標も考慮した、最終的なオーグメンテーションされたネガティブサンプルを特定するための高度なネガティブサンプリング戦略を設計する。
Extensive experiments on real-world datasets demonstrate that our method significantly outperforms state-of-the-art baselines.
実世界のデータセットを用いた広範な実験により、我々の手法が最先端のベースラインを大幅に上回ることが実証された。
Our code is publicly available at https://github.com/Asa9aoTK/ANS-Recbole.
我々のコードは https://github.com/Asa9aoTK/ANS-Recbole で公開されている。

# 1. Introduction はじめに

Collaborative filtering (CF), as an important paradigm of recommender systems, leverages observed user-item interactions to model users’ potential preferences [13, 15, 35].
協調フィルタリング（CF）は、推薦システムの重要なパラダイムとして、ユーザの潜在的な嗜好をモデル化するために、**観察されたユーザとアイテムのinteractionを活用する**[13, 15, 35]。
In real-world scenarios, such interactions are normally in the form of implicit feedback (e.g., clicks or purchases), instead of explicit ratings [34].
実世界のシナリオでは、このようなinteractionは通常、明示的な評価ではなく、暗黙的なフィードバック（クリックや購入など）の形で行われる[34]。
Each observed interaction is normally considered a positive sample.
観察された各interactionは通常、**positive sample**とみなされる。
As for negative samples, existing methods usually randomly select some uninteracted items.
ネガティブサンプルに関しては、既存の方法は通常、いくつかのinteractionしていないitemをランダムに選択する。
Then a CF model is optimized to give positive samples higher scores than negative ones via, for example, the Bayesian personalized ranking (BPR) loss function [26], where a score function (e.g., inner product) is used to measure the similarity between a user and an item.
そして、CFモデルは、例えば、スコア関数(例えば、内積)がユーザとアイテムの間の類似性を測定するために使用されるベイズパーソナライズドランキング（BPR）損失関数[26]を介して、**肯定的なサンプルに否定的なサンプルよりも高いスコアを与えるように最適化される**。

Recent studies have shown that negative samples have a great impact on model performance [22, 41, 45].
最近の研究では、負のサンプルがモデルの性能に大きな影響を与えることが示されている[22, 41, 45]。
As the state of the art, hard negative sampling strategies whose general idea is to oversample high-score negative items have exhibited promising performance [4, 8, 9, 41, 44].
一般的な考え方として、高得点のネガティブitemをオーバーサンプリングする**ハードネガティブサンプリング戦略**が、有望な性能を示している[4, 8, 9, 41, 44]。
While selecting a negative item with a high score makes it harder for a model to classify a user, it has the potential to bring more useful information and greater gradients, which are beneficial to model training [4, 25].
高いスコアでnegative itemを選択することは、モデルがユーザを分類することを難しくする一方で、より有用な情報やより大きな勾配をもたらす可能性があり、モデルの学習に有益である[4, 25]。
Ideally, one would calculate the scores of all uninteracted items to identify the best negative samples.
理想的なのは、最高のネガティブサンプルを特定するために、interactしていないすべてのitemのスコアを計算することである。
However, its time complexity is prohibitive.
しかし、時間計算量は法外である。
To balance efficiency and effectiveness, the two-pass approach has been widely adopted [1, 9, 16, 41, 44].
効率と有効性のバランスをとるために、**2パスアプローチ**が広く採用されている[1, 9, 16, 41, 44]。(ふむふむ:thinking:)
The first pass samples a fixed number of unobserved items by a static distribution, and the second pass then selects the final negative items with a more sophisticated negative sampling method.
最初のパスでは、固定数の未観測itemを静的分布でサンプリングし、2番目のパスでは、より洗練されたネガティブサンプリング法で最終的なnegative itemsを選択する。

Despite the significant progress made by hard negative sampling, selecting negative samples from the original items in a dataset is inherently restricted due to the limited available choices.
ハードネガティブサンプリングによって大きな進歩があったにもかかわらず、データセット内の元のitemからネガティブサンプルを選択することは、利用可能な選択肢が限られているため、本質的に制限されている。
Such original items may not be able to contrast positive samples well.
このようなオリジナルアイテムは、陽性サンプルをうまく対比できない可能性がある。
Indeed, we design a set of intuitive experiments to show that existing works suffer from two major drawbacks.(1) Ambiguous trap.
実際、我々は一連の直感的な実験をデザインし、**既存の手法が2つの大きな欠点に苦しんでいる**ことを示す。
Since the vast majority of unobserved items have very low scores (i.e., they are easy negative samples), randomly sampling a small number of candidate negative items in the first pass is difficult to include useful hard negative samples, which, in turn, substantially limits the efficacy of the second pass.(2) Information discrimination.
未観測項目の大部分は非常に低いスコア(すなわち、easyな陰性サンプル)であるため、第1パスで少数のnegative item候補を無作為にサンプリングしても、有用なハードnegativeサンプルを含めることは困難であり、ひいては第2パスの有効性を大幅に制限することになる(2)。
In the second pass, most existing studies overly focus on high-score negative items and largely neglect low-score negative items.
2つ目のパスでは、既存の研究のほとんどが、高得点のネガティブitemに過度に焦点を当て、低得点のネガティブitemをほとんど無視している。
We empirically show that such low-score negative items also contain critical, unique information that leads to better model performance.
我々は、このような低得点のネガティブitemにも、より良いモデル性能をもたらす重要でユニークな情報が含まれていることを実証的に示す。

Our response to such drawbacks is to introduce “augmented” negative samples (i.e., synthetic items) that are more similar to positive items while still being negative.
**このような欠点に対する我々の対応策は、negativeでありながらpositiveなitemにより似ている「増強された」否定的なサンプル(すなわち合成item)を導入すること**である。
While data augmentation techniques have been proposed in other domains [17, 37, 38, 40], it is technically challenging to apply similar ideas to negative sampling for collaborative filtering.
データ増強技術は他の領域でも提案されているが[17, 37, 38, 40]、**協調フィルタリングのネガティブサンプリングに同様のアイデアを適用するのは技術的に困難**である。
This is because all of them fail to carefully regulate and quantify the augmentation needed to approximate positive items while not introducing excessive noise or still being negative.
なぜなら、そのどれもが、過剰なノイズを発生させたり、ネガティブなままであることを避けながら、ポジティブなitemを近似させるために必要な補強を注意深く調整し、定量化できていないからである。

To this end, we present a novel generic augmented negative sampling (ANS) paradigm and then provide a concrete instantiation.
この目的のために、我々は新しい一般的な **augmented negative sampling(ANS)**パラダイムを提示し、具体的なインスタンス化を提供する。
Our insight is that it is imperative to understand a negative item’s hardness from a more fine-granular perspective.
私たちの洞察は、ネガティブなアイテムのhardさをより細かい粒状の観点から理解することが不可欠であるということである。(=ぶっちゃけhard negative sampleってどんなnegative sampleなんだろう...?を理解しようって話:thinking:)
We propose to disentangle an item’s embedding into hard and easy factors (i.e., a set of dimensions of the embedding vector), where hardness is defined by whether a negative item has similar values to the corresponding user in the given factor.
我々は、**アイテムの埋め込みを、hardな因子とeasyな因子(埋め込みベクトルの次元の集合)に分離することを提案する**。hardさは、ネガティブアイテムが、与えられた因子において、対応するユーザと同様の値を持つかどうかによって定義される。
This definition is in line with the definition of hardness in hard negative sampling.
この定義は、hard negtive samplingにおける"hardness"の定義と一致している。
Here the key technical challenge originates from the lack of supervision signals.
ここで重要な技術的課題は、supervision signals(=教師ラベル?)の欠如に起因する。
Consequently, we propose two learning tasks that combine contrastive learning (CL) [43] and disentanglement methods [12] to guarantee the credibility of the disentanglement.
その結果、我々は、分離の信頼性を保証するために、contrastive learning(対照学習, CL)[43]とdisentanglement methods(分離手法)[12]を組み合わせた2つの学習タスクを提案する。
Since our goal is to create synthetic negative items similar to positive items, we keep the hard factor of a negative item unchanged and focus on augmenting the easy factor by controlling the direction and magnitude of added noise.
**われわれの目標は、ポジティブitemと類似した合成ネガティブitemを作成すること**であるため、ネガティブ項目のハードファクターは変更せず、付加されるノイズの方向と大きさを制御することによって、イージーファクターを増強することに集中する。
The augmentation mechanism needs to be carefully designed so that the augmented item will become more similar to the corresponding positive item, but will not cross the decision boundary.
補強のメカニズムは、補強されたitemが対応するpositive itemに似てくるが、判定境界を越えないように注意深く設計する必要がある。
Furthermore, we introduce a new metric called augmentation gain to measure the difference between the scores before and after the augmentation.
さらに、**オーグメンテーション・ゲイン**と呼ばれる新しい指標を導入し、オーグメンテーション前後のスコアの差を測定する。
Our sampling strategy is guided by augmentation gain, which gives low-score items with higher augmentation gain a larger probability of being sampled.
私たちのサンプリング戦略は、オーグメンテーションゲインによって導かれ、オーグメンテーションゲインの高い低スコアitemがサンプリングされる確率が高くなる。
In this way, we can effectively mitigate information discrimination, leading to better performance.
こうすることで、情報による差別を効果的に緩和し、より良いパフォーマンスにつなげることができる。
We summarize our main contributions as follows:
我々の主な貢献は以下の通りである：

- We design a set of intuitive experiments to reveal two notable limitations of existing hard negative sampling methods, namely ambiguous trap and information discrimination. 我々は、既存のハードネガティブサンプリング法の2つの顕著な限界、すなわちambiguous trap(曖昧な罠)とinformation discrimination(情報の識別)を明らかにするために、一連の直感的な実験をデザインする。

- To the best of our knowledge, we are the first to propose to generate negative samples from a fine-granular perspective to improve implicit CF. In particular, we propose a new direction of generating regulated augmentation to address the unique challenges of CF. 我々の知る限り、暗黙的CFを改善するために、微細な粒度の観点からネガティブサンプルを生成することを提案したのは我々が初めてである。特に、CF特有の課題に対処するために、**調節された補強を生成するという新しい方向性**を提案する。

- We propose a general paradigm called augmented negative sampling (ANS) that consists of three steps, including disentanglement, augmentation, and sampling. We also present a concrete implementation of ANS, which is not only performant but also efficient. 我々は、**拡張ネガティブサンプリング(ANS)**と呼ばれる一般的なパラダイムを提案する。ANSは、分離、拡張、サンプリングの3つのステップから構成される。 また、ANSの具体的な実装についても紹介する。

- We conduct extensive experiments on five real-world datasets to demonstrate that ANS can achieve significant improvements over representative state-of-the-art negative sampling methods. 我々は5つの実世界のデータセットで大規模な実験を行い、ANSが代表的な最先端のネガティブサンプリング手法よりも大幅な改善を達成できることを実証する。

# 2. Related Work 関連作品

## 2.1. Model-Agnostic Negative Sampling モデル無視ネガティブサンプリング

A common type of negative sampling strategy selects negative samples based on a pre-determined static distribution [6, 36, 39].
一般的なタイプのネガティブサンプリング戦略は、事前に決定された静的分布(=固定された分布?)に基づいてネガティブサンプルを選択する[6, 36, 39]。
Such a strategy is normally efficient since it does not need to be adjusted in the model training process.
このような戦略は、モデルのトレーニング過程で調整する必要がないため、通常は効率的である。
Random negative sampling (RNS) [5, 26, 35, 40] is a simple and representative model-agnostic sampling strategy, which selects negative samples from unobserved items according to a uniform distribution.
ランダムネガティブサンプリング（RNS）[5, 26, 35, 40]は、一様分布に従って未観測itemからネガティブサンプルを選択する、シンプルで代表的なモデル不可知サンプリング戦略である。
However, the uniform distribution is difficult to guarantee the quality of negative samples.
しかし、一様分布では陰性サンプルの品質を保証することは難しい。(たしかに:thinking:)
Inspired by the word-frequency-based distribution [11] and node-degree-based distribution [23] in other domains, an itempopularity-based distribution [2, 6] has been introduced.
他のドメインにおける単語頻度ベースの分布[11]やノード度ベースの分布[23]に触発され、**アイテムポピュラリティベースの分布**[2, 6]が導入された。(うんうん。アイテムの人気度に基づくのは想像しやすい:thinking:)
Under this distribution, popular items are more likely to be sampled as negative items, which helps to mitigate the widespread popularity bias issue in recommender systems [3].
この分布の下では、人気アイテムはネガティブアイテムとしてサンプリングされる可能性が高くなり、推薦システムで広く見られる人気バイアス問題を緩和するのに役立つ[3]。(うんうん...!:thinking:)
Although this kind of strategy is generally efficient, the pre-determined distributions are not customized for the underlying models and not adaptively adjusted during the training process.
この種の戦略は一般的に効率的であるが、事前に決定された分布は**基礎となるモデル用にカスタマイズされておらず**、**学習プロセス中に適応的に調整されることもない**。
As a result, their performance is often sub-optimal.
その結果、彼らのパフォーマンスはしばしば最適とは言えない。

## 2.2. Model-Aware Negative Sampling モデルを意識したネガティブサンプリング

These strategies take into consideration some information of the underlying model, denoted by $f$, to guide the sampling process.
これらの戦略は、$f$ で示される underlying model (??)の情報を考慮して、サンプリングプロセスを導く。
Given $f$, the probability of sampling an item 𝑖 is defined as $p(i|f) \propto g(f, \mathbf{e}_{i})$, where $g(·, ·)$ is a sampling function, and $\mathbf{e}_{i}$ denotes the embedding of $i$.
$f$ が与えられたとき、item $i$ をサンプリングする確率は $p(i|f) \propto g(f, \mathbf{e}_{i})$ と定義される、
ここで、$g(-, -)$ はサンプリング関数、$mathbf{e}_{i}$ は $i$ の埋め込みを表す。
Existing studies focus on choosing different $f$ and/or designing a proper $g(·, ·)$ to achieve better performance.
既存の研究は、より良いパフォーマンスを達成するために、異なる$f$ を選択すること、および/または適切な $g(·, ·)$ を設計することに焦点を当てている。
The most representative work is hard negative sampling, which defines 𝑔(·, ·) as a score function.
最も代表的な研究は、$g(·, ·)$ をスコア関数(=user-itemのpreference scoreを出力する関数??:thinking:)として定義するハードネガティブサンプリングである。
It assigns higher sampling probabilities to the negative items with larger prediction scores [8, 9, 16, 25, 41, 44].
これは、予測スコアの大きいnegative itemにより高いサンプリング確率を割り当てる[8, 9, 16, 25, 41, 44]。
For example, DNS [41] assumes that the high-score items should be more likely to be selected, and thus chooses $g(·, ·)$ to be the inner product and $f$ to be user representations.
例えば、DNS [41]は、高得点の項目が選択される可能性が高いと仮定し、$g(·, ·)$ を内積、$f$ をユーザ表現とする。
With the goal of mitigating false negative samples, SRNS [9] further incorporates the information about the last few epochs into $f$ and designs $g(·, ·)$ to give false negative samples lower scores.
SRNS[9]は、偽陰性サンプルを軽減する目的で、さらに直近の数エポックに関する情報を $f$ に組み込み、偽陰性サンプルにより低いスコアを与えるように $g(·, ·)$ を設計する。
IRGAN [33] integrates a generative adversarial network into $g(·, ·)$ to determine the probabilities of negative samples through the min-max game.
IRGAN [33]は、生成的な敵対的ネットワークを $g(·, ·)$ に統合し、最小-最大ゲームを通して負サンプルの確率を決定する。
ReinforcedNS [8] use reinforcement learning into $g(·, ·)$.
ReinforcedNS [8]は、強化学習を $g(·, ·)$ に用いる。

With well-designed $f$ and $g(·, ·)$, we can generally achieve better performance.
うまく設計された $f$ と $g(\cdot, \cdot)$ があれば、一般に、より良いパフォーマンスを達成できる。
However, selecting suitable negative items need to compute 𝑔(·, ·) for all unobserved items, which is extremely timeconsuming and prohibitively expensive.
しかし、適切なnegative itemを選択するためには、すべての未観測itemについて $g(-, -)$ を計算する必要があり、これは非常に時間がかかり、法外に高価である。
Take DNS as an example.
DNSを例にとってみよう。
Calculating the probability of sampling an item is equivalent to performing softmax on all unobserved samples, which is unacceptable in real-world applications [4, 24, 33].
**アイテムをサンプリングする確率を計算することは、すべての未観測サンプルに対してソフトマックスを実行することと等価であり、実際のアプリケーションでは受け入れられない**[4, 24, 33]。
As a result, most model-aware sampling strategies adopt the two-pass approach or its variants.
その結果、モデルを意識したサンプリング戦略のほとんどは、2パスアプローチまたはその変形を採用している。
In this case, $g(·, ·)$ is only applied to a small number of candidates sampled in the first pass.
この場合、$g(-, -)$ は最初のパスでサンプリングされた少数の候補にのみ適用される。
While such two-pass-based negative sampling strategies have been the mainstream methods, they exhibit two notable limitations, namely ambiguous trap and information discrimination, which motivates us to propose an augmented negative sampling paradigm.
このような2パスベースのネガティブサンプリング戦略は主流の手法であるが、曖昧トラップと情報識別という2つの顕著な限界がある。
In the next section, we will explain these limitations via a set of intuitive experiments.
次のセクションでは、一連の直感的な実験を通してこれらの限界を説明する。

# 3. Limitations of the Two-pass approach 2パス・アプローチの限界

In this section, we first formulate the problem of implicit CF and then explain ambiguous trap and information discrimination via intuitive experiments.
本節では、まず暗黙のCFの問題を定式化し、次に曖昧な罠と情報の識別について直感的な実験を通して説明する。
We consider the Last.fm and Amazon-Baby datasets in experiments.
実験では、Last.fmとAmazon-Babyのデータセットを使用した。
A comprehensive description of the data is provided in Section 5.
データの包括的な説明はセクション5に記載されている。

## 3.1. Implicit CF 暗黙のCF

We denote the set of historical **interactions** by $O^{+} = {(u,i^{+})|u \in \mathcal{U}, i^{+} \in \mathcal{I}}$, where U and I are the set of users and the set of items, respectively.
本論文ではinteraction履歴の集合を $O^{+} = {(u,i^{+})|u \in \mathcal{U}, i^{+} \in \mathcal{I}}$ と表記する。ここで、 $U$ と $I$ はそれぞれユーザ集合とアイテム集合。
The most common implicit CF paradigm is to learn user and item representations (e𝑢 and e𝑖 ) from the historical interactions and then predict the scores of unobserved items to recommend the top-K items.
最も一般的な暗黙的CFのパラダイム(方法?)は、過去のインタラクションからユーザとアイテムの表現(e𝑢とe𝑖)を学習し、トップKのアイテムを推薦するために未観測のアイテムのスコアを予測することである。(うんうん...!:thinking:)
The BPR loss function is widely used to optimize the model:
モデルの最適化にはBPR損失関数が広く使われている：

$$
\mathcal{L}_{BPR}
= \sum_{u, i^+ \in O^+} - \ln[\sigma(s(e_{u}m e_{i^+}) - s(e_{u}m e_{i^-}))]
\tag{1}
$$

where 𝜎(·) is the sigmoid function, and 𝑠(·, ·) is a score function (e.g., the inner product) that measures the similarity between the user and item representations.
ここで、$\sigma()$ はシグモイド関数であり、$s(\cdot, \cdot)$ はスコア関数（内積など）である。
Here 𝑖 − is a negative sample selected by a sampling strategy.
ここで、$i^-$ はサンプリング戦略によって選択された負のサンプルである。
Our goal is to design a negative sampling strategy that is generic to different CF models.
**我々の目標は、異なるCFモデルに汎用的なネガティブサンプリング戦略を設計すること**である。
Following previous studies [4, 26, 33], without loss of generality, we consider matrix factorization with Bayesian personalized ranking (MF-BPR) [26] as the basic CF model to illustrate ANS.
先行研究[4,26,33]に従い，一般性を損なわない範囲で，ANS を説明する基本 CF モデルとして，Bayesian personalized rankingによる行列分解(MF-BPR)[26]を考える。

## 3.2. Ambiguous Trap ♪あいまいな罠

![figure1]()

We choose DNS [41], which is the most representative hard negative sampling method, to train an MF-BPR model on the Last.fm dataset and calculate the scores of unobserved user-item pairs in different training periods.
Last.fmデータセットでMF-BPRモデルを訓練するために、最も代表的なハードネガティブサンプリング法であるDNS [41]を選択し、異なる訓練期間における未観測のユーザとアイテムのペアのスコアを計算する。
Figure 1(a), 1(b), 1(c) demonstrates the frequency distributions of the scores at different epochs.
図1(a)、(b)、(c)は、異なるエポックにおけるスコアの度数分布を示している。
The lowest 80% of the scores are emphasized by the pink shade.
得点の下位80％はピンクの影で強調されている。
We can observe that as training progresses, more and more scores are concentrated in the low-score region, meaning that the vast majority of unobserved items are easy negative samples.
**訓練が進むにつれて、より多くのスコアが低スコア領域に集中している**ことが観察できる。これは、**未観測itemの大部分がネガティブサンプルになりやすい**ことを意味する。
Recall that the first pass samples a fixed number of negative items by a uniform distribution.
**first passでは、一様分布によって一定数のネガティブ・アイテムをサンプリングすること**を思い出してほしい。
Randomly sampling a small number of negative items in the first pass is difficult to include useful hard negative samples, which, in turn, substantially limits the efficacy of the second pass.
**first passで少数のネガティブitemを一様ランダムにサンプリングすることは、有用なhard negative sampleを含めることが困難であり、その結果、second passの有効性が大幅に制限される**。
(2-stages推薦において、1 stage目で一様ランダムにcandidate retrieveしてしまい、2 stage目でいくら精度の高いモデルでrerankingしても、candidateにそもそもユーザの好みと合ったアイテムが含まれていない可能性があり、有効に機能しないよ、って話と同じか:thinking:)
We call this phenomenon ambiguous trap.
私たちはこの現象を ambiguous trap(曖昧な罠) と呼んでいる。(本論文内で定義している言葉なのか...!:thinking:)

![figure1]()

To further demonstrate the existence of ambiguous trap, in Figure 1(d), we plot the min-max normalizing maximum and minimum scores of the sampled negative items in the first pass on the Last.fm dataset.
ambiguous trapの存在をさらに示すために、図1(d)では、Last.fmデータセットの**first passでサンプリングされたnegative itemの最大スコアと最小スコア**を最小-最大正規化してプロットしている。
It can be seen that the difference between the maximum score and the minimum score is consistently small, suggesting that randomly sampling a small number of negative items makes the hardness of the negative samples obtained from DNS far from ideal.
**最大スコアと最小スコアの差が一貫して小さい(=>hard negtiveをサンプリングできてないってこと??:thinking:)**ことから、少数のnegative itemを無作為にサンプリングすることで、DNSから得られるネガティブサンプルのhardさが理想からかけ離れていることがわかる。
Note that a straightforward attempt to mitigate ambiguous trap is to substantially increase the sample size in the first pass.
ambiguous trapを軽減する簡単な試みは、最初のパスでサンプルサイズを大幅に増やすことである。(hard sample含まれてくれ～みたいな感じかな:thinking:)
However, it is inevitably at the cost of substantial time and space overhead [4].
しかし、その代償として、かなりの時間とスペースのオーバーヘッドが避けられない[4]。
Inspired by contrastive learning [17, 37, 40], we propose to augment the sampled negative items to increase their hardness.
contractive learning[17, 37, 40]にヒントを得て、私たちは、サンプリングされたnegative itemのhardさを上げるために、そのitemを補強することを提案する。

## 3.3. Information Discrimination 情報差別

In the second pass, most existing studies overly focus on high-score negative items and largely neglect low-score negative items, which also contain critical, unique information to improve model performance.
2つ目のパスでは、既存の研究のほとんどが、高スコアのnegative itemに過度に注目し、**モデルのパフォーマンスを向上させるために重要でユニークな情報を含む低スコアのnegative itemをほとんど無視している**。
Overemphasizing high-score items as negative samples may result in worse model performance.
高スコアのitemをネガティブサンプルとして強調しすぎると、モデルのパフォーマンスが低下する可能性がある。
Several studies [4, 27] have made efforts to assign lower sampling probabilities to low-score items using algorithms like softmax and its derivatives.
いくつかの研究[4, 27]では、ソフトマックスやその派生型のようなアルゴリズムを用いて、低スコアitemに低いサンプリング確率を割り当てる努力(=全くサンプリングしない状況を避ける為の努力??:thinking:)をしてきた。
However, selecting those significantly lower-score items in comparison to others, remains a challenge.
しかし、他のitemと比較して著しくスコアの低いitemを選択することは、依然として課題である。
We call this behavior information discrimination.
私たちはこの行動を **information discrimination(情報差別)** と呼んでいる。(=高スコアnegative itemと低スコアnegative itemの優遇・劣遇の格差?:thinking:)(これも本論文で定義した用語なんだ...!::)
To verify the existence of information discrimination, we introduce a new measure named Pairwise Exclusive-hit Ratio (PER) [18] to CF, which is used to compare the difference between the information learned by two different methods.
information discrimination の存在を検証するため、CFにPER(Pairwise Exclusive-hit Ratio)[18]という新しい尺度を導入し、2つの異なる方法(=negative sampling方法?)で学習した情報の差を比較する。
More specifically, PER(𝑥, 𝑦) quantifies the information captured by the method x but not by y via
より具体的には、$PER(x, y)$ は、手法 $x$ によって捕捉され、手法 $y$ によって捕捉されなかった情報を定量化する:

$$
PER(x,y) = \frac{|\mathcal{H}_{x} - \mathcal{H}_{y}|}{|\mathcal{H}_{x}|}
\tag{2}
$$

where H𝑥 denotes the set of test interactions correctly predicted by the method 𝑥.
ここで $\mathcal{H}_{x}$ は、手法 $x$ によって正しく予測されたテストinteractionの集合を表す。
Next, we choose two representative negative sampling methods, RNS [8] and DNS [41] to train MF-BPR models and calculate the PER between them.
次に、代表的なネガティブサンプリング手法であるRNS[8]とDNS[41]を選択し、MF-BPRモデルの学習を行い、両者のPERを計算する。
Recall that DNS is more likely to select high-score negative items while RNS uniformly randomly selects negative items irrespective of their scores.
DNSは高スコアのnegative itemを選択しやすく、RNSはスコアに関係なく一様にnegative itemをランダムに選択することを思い出してほしい。

![figure2]()

(横軸が手法 $x$ ??:thinking:)

The obtained results are depicted in Figure 2 (excluding HNS data for the current analysis).
得られた結果を図2に示す(今回の分析ではHNS(=たぶん別のnegative sampling手法??)のデータを除く)。
We can observe that:

- (1) the DNS strategy can indeed learn more information, confirming the benefits of leveraging hard negative samples to form a tighter decision boundary.
- (1)DNS戦略は確かに多くの情報を学習することができ、より厳しい決定境界を形成するためにhard negative sampleを活用することの利点を確認することができる。
- (2) The values of PER(RNS, DNS) on two datasets (0.2 and 0.33) indicate that even the simple RNS strategy can still learn rich information that is not learned by DNS. (2)2つのデータセットにおけるPER(RNS, DNS)の値(0.2と0.33) (i.e. RNSによって補足され、DNSによって補足されなかった情報量:thinking:)は、単純なRNS戦略でも、DNSでは学習されない豊富な情報を学習できることを示している。In other words, the easy negative items overlooked by DNS are still valuable for CF. つまり、**DNSが見過ごしがちなnegative item (i.e. 低スコアのnegative itme:thinking:)も、CFにとっては貴重**なのだ。

Such an information discrimination problem inspires us to understand a negative item’s hardness from a more fine-granular perspective in order to extract more useful information.
このような information discrimination の問題は、より有用な情報を抽出するために、**negative itemのhardnessをより細かな視点から理解すること**を促す。(=真に学習に有用なnegative sampleとはどんなものか...!これってつまりimplicit feedbackにおける、negativeとunknownをより高精度で判別しようとしてる事と同義なのかな:thinking:)

# 4. Methodology 方法論

![figure3]()

Driven by the aforementioned limitations, we propose a novel generic augmented negative sampling (ANS) paradigm, which consists of three major steps: disentanglement, augmentation, and sampling.
前述したような制約の中で、我々は新しい一般的な augmented negative sampling(ANS) パラダイムを提案する。このパラダイムは**3つの主要なステップ**から構成される: **disentanglement(分離), augmentation(拡張), sampling(サンプリング)**.
The disentanglement step learns an item’s hard and easy factors;
分離ステップでは、itemのhard factorとeasy factorを学習する;
the augmentation step adds regulated noise to the easy factor so as to increase the item’s hardness;
augmentationステップでは、アイテムのhardnessを増加させるために、easy factorに調整ノイズを加える。
the sampling strategy selects the final negative samples based on a new metric we propose.
サンプリング戦略は、我々が提案する新しい指標に基づいて最終的なnegative sampleを選択する。
The workflow of ANS is illustrated in Figure 3.
ANSのワークフローを図3に示す。
Note that these steps can be implemented by different methods and thus the overall paradigm is generic.
これらのステップは異なる方法で実装できるため、全体的なパラダイムは汎用的であることに注意。(各ステップは疎結合なので、部分的に置き換えたり拡張したりできるってこと??:thinking:)
We present a possible instantiation in the following sections.
可能なインスタンス化を以下のセクションで紹介する。

## 4.1. Disentanglement 分離

To understand a negative item’s hardness from a more fine-granular perspective, we propose to disentangle its embedding into hard and easy factors (i.e., a set of dimensions of the embedding vector),
where hardness is defined by whether a negative item has similar values to the corresponding user in the given factor.
ネガティブアイテムのhardnessをより細かく理解するために、**その埋め込みをhard factorとeasy factor (埋め込みベクトルの次元の集合)に分離する**ことを提案する。
ここで**hardnessとは、negative itemが、与えられたfactorにおいて、対応するユーザ(のembedding?:thinking:)と同じような値を持つかどうかによって定義される**。
Similarly, we follow the two-pass approach to first randomly sample $M (M <<|I|)$ items from the unobserved items to form a candidate negative set $E$.
同様に、2パス・アプローチに従って、まず未観測itemから $M (M <<|I|)$ itemをランダムにサンプリングし、candidate negative 集合 $E$ を形成する。
We design a gating module to identify which dimensions of a negative item e𝑛 ∈ R 𝑑 in E are hard with respect to user e𝑢 ∈ R 𝑑 via
$E$ におけるnegative item $\mathbf{e}_n \in \mathbb{R}^{d}$ のどの次元が、ユーザ $\mathbf{e}_u \in \mathbb{R}^{d}$ に関してhardかを特定するために、gating moduleを設計する:

$$
gate_{hard}
= \sigma(\mathbf{W}_{item} \mathbf{e}_{n} \odot \mathbf{W}_{user} \mathbf{e}_{u})
\tag{3}
$$

where $gate_{hard} \in \mathbb{R}^{d}$ gives the weights of different dimensions.
ここで、$gate_{hard} \in \mathbb{R}^{d}$ は異なる次元の重みを与える。(重みベクトルみたいな感じか:thinking:)
The sigmoid function 𝜎(·) maps the values to (0, 1).
シグモイド関数 $\sigma()$ は、値を(0, 1)にマッピングする。
W𝑖𝑡𝑒𝑚 ∈ R 𝑑×𝑑 and W𝑢𝑠𝑒𝑟 ∈ R 𝑑×𝑑 are linear transformations used to ensure that the user and item embeddings are in the common latent space [22].
$\mathbf{W}_{item}, \mathbf{W}_{user} \in \mathbb{R}^{d \times d}$ は**ユーザとアイテムの埋め込みが共通の潜在空間にあることを保証するための線形変換**である[22]。(線形変換する前は、共通のlatent spaceになくてもいいんだろうか? まあ内積とかでpreference scoreを算出する前提で作られたembeddingだったら、基本的には共通のlatent spaceにあるか:thinking:)
$\odot$ is the element-wise product, which measures the similarity between e𝑖 and e𝑢 in each dimension [35].
$\odot$ は要素ごとの積で、各次元におけるe𝑖とe*46の類似度を測る[35]。(アダマール積だっけ?)
After obtaining the weights 𝑔𝑎𝑡𝑒ℎ𝑎𝑟𝑑 , we adopt the element-wise product to extract the hard factor e ℎ𝑎𝑟𝑑 𝑛 .
重み $gate*{hard}$ を得た後、要素ごとの積を採用して hard factor $\mathbf{e}^{hard}_{n}$ を抽出する。
The easy factor e 𝑒𝑎𝑠𝑦 𝑛 is then calculated via element-wise subtraction [12].
次に、easy factor $\mathbf{e}^{easy}_{n}$ が、**要素ごとの減算**(アダマール減算みたいな?:thinking:)によって計算されます[12]。

$$
\mathbf{e}^{hard}_{n} = \mathbf{e}_n \odot gate_{hard}
\\
\mathbf{e}^{easy}_{n} = \mathbf{e}_n - \mathbf{e}^{hard}_{n}
\tag{4}
$$

Due to the lack of ground truth for hard and easy factors, it is inherently difficult to guarantee the credibility of the disentanglement.
hard factor と easy factor のグランドトゥルースがないため(そりゃそう)、ディセンションの信頼性を保証することは本質的に難しい。(品質の評価が難しいってことか:thinking:)
Inspired by its superiority in unsupervised scenarios [19, 43], we propose to adopt contrastive learning to guide the disentanglement.
教師なしシナリオ[19, 43]での優位性に触発され、我々は、分離を導くためにcontractive learningを採用することを提案する。
By definition, the hard factor of a negative item should be more similar to the user, while the easy factor should be the opposite.
定義によれば、negative itemのhard factorはよりユーザに近いものであるべきで、easy factor はその逆であるべきである。
Therefore, given a score function 𝑠(·, ·) to calculate the similarity between a pair, we design a contrastive loss L𝑐 as
したがって、(embedddingの)ペア間の類似度を計算するスコア関数 $𝑠(\cdot, \cdot)$ が与えられたとき、contractiveな損失関数 $\mathcal{L}_c$ を次のように設計する。

$$
\mathcal{L}_c =
\sum_{\mathbf{e}_{n} \in \epsilon} s(e_u, e_n^{easy}) - s(e_u, e_n^{hard})
\tag{5}
$$

However, optimizing only L𝑐 may lead to a trivial solution: including all dimensions as the hard factor.
しかし、$L_c$ のみを最適化すると、embeddingのすべての次元をhard factorにに含める様な、つまらない解になる可能性がある。
Therefore, we introduce another loss with the auxiliary information from positive items.
そこで、positive itemから得られる補助情報を使って、別の損失を導入する。
We adopt a similar operation with the same weights 𝑔𝑎𝑡𝑒ℎ𝑎𝑟𝑑 to obtain the corresponding positive item factor e ′ 𝑝 and e ′′ 𝑝 :
同じ重みベクトル $gate_{hard}$ で同様の操作を採用し、対応するpositive item factor $\mathbf{e}^{'}_{p}$ と $\mathbf{e}^{''}_{p}$ を求める：

$$
\mathbf{e}^{'}_{p} = \mathbf{e}_{p} \odot gate_{hard}
\\
\mathbf{e}^{''}_{p} = \mathbf{e}_{p} - \mathbf{e}^{'}_{p}
\tag{6}
$$

This is particularly important as $\mathbf{e}_{n}^{easy}$ may emphasize the first 48 dimensions while $\mathbf{e}_{n}^{hard}$ may emphasize the last 14.
これは、$\mathbf{e}_{n}^{easy}$ が最初の48次元を強調する一方、$\mathbf{e}_{n}^{hard}$ が最後の14次元を強調することがあるので、特に重要である。(??)
In order to ensure coherence in subsequent operations, it is imperative to maintain the correspondence of dimensions.
その後の作戦の一貫性を確保するためには、寸法の対応関係を維持することが不可欠である。
For ease of understanding, reader can directly regard them as positive samples.
理解しやすいように、読者はこれらを直接positive sampleとみなすことができる。
Intuitively, e ℎ𝑎𝑟𝑑 𝑛 should be more similar to positive since it is difficult for users to discern it as a negative sample (both have a high similarity to the user).
直感的には、$\mathbf{e}_{n}^{hard}$ は、ユーザがnegative sampleと判別しにくいため(=定義的にそのはず!)、positiveの埋め込み $\mathbf{e}^{'}_{p}$ に近いはずです(どちらもユーザとの類似度が高い)。
However, this signal is not entirely reliable, as it may not accurately reflect a user’s level of interest.
しかし、この信号 (=embedding $\mathbf{e}$ のこと?)はユーザの関心度を正確に反映しているとは限らないため、完全に信頼できるものではない。
Therefore, instead of relying on a stringent constraint like Equation 5, we introduce another disentanglement loss L𝑑 as
したがって、式5のような厳しい制約に頼る代わりに、別の分離損失 $L_d$ を次のように導入する。

$$
\mathcal{L}_d = \sum_{e_n \in E} \|\mathbf{e}^{'}_{p} - \mathbf{e}_{n}^{hard}\|^2 + s(\mathbf{e}^{''}_{p}, \mathbf{e}_{n}^{easy})
\tag{7}
$$

where the Euclidean distance is used to measure the similarity between e ′ 𝑝 and e ℎ𝑎𝑟𝑑 𝑛 while the score function is used to measure the similarity between e 𝑒𝑎𝑠𝑦 𝑝 and e ′′ 𝑛 .
ここで、ユークリッド距離は $\mathbf{e}^{'}_{p}$ と $\mathbf{e}_{n}^{hard}$ の類似性を測定するために用いられ、スコア関数は $\mathbf{e}^{''}_{p}$ と $\mathbf{e}_{n}^{easy}$ の類似性を測定するために用いられる。(二種類のcontractive learningって感じ:thinking:)
This is because we want to leverage only reliable hardness while we can be more lenient with the easy part.
これは、信頼できるhardnessだけを活用し、簡単な部分にはもっと甘くしてもいいからだ。

## 4.2. Augmentation

Next, we propose an augmentation module to create synthetic negative items which are more similar to the corresponding positive items.
次に、対応するpositive itemにより類似した合成negative itemを作成するオーグメンテーションモジュールを提案する。
After the disentanglement step, we have obtained the hard and easy factors of a negative item, where the hard factor contains more useful information for model training.
分離ステップの後、negative itemのhard factor と easy factor が得られ、hard factor にはモデル学習により有用な情報が含まれている。
Therefore, our goal is to augment the easy factor to improve model performance.
したがって、**我々の目標は、モデルのパフォーマンスを向上させるために、easy factor を増強すること**である。
However, existing augmentation techniques fail to carefully regulate and quantify the augmentation needed to approximate positive items while still being negative.
しかし、既存のaugmentation技術は、negativeでありながらpositive itemに近似するために必要なaugmentationを、注意深く調整し定量化することに失敗している。(まあともかく既存手法じゃだめってことかな:thinking:)
To this end, we propose to regulate the augmentation from two different aspects:
この目的のために、我々は2つの異なる側面からaugmentationを規制することを提案する：

**側面1: Direction**:
方向：
Intuitively, the direction of the augmentation on a negative item should be towards the corresponding positive item.
**直感的には、negative item に対する補強の方向は、対応するpositive itemに向かうべき**である。(よりhardなnegative sampleにする為に?)
Therefore, we first calculate the difference e𝑑𝑖 𝑓 between the factor of the positive item e ′′ 𝑝 and the easy factor of the negative item e 𝑒𝑎𝑠𝑦 𝑛 :
そこで、まずpositive item のfactor $e_p^{''}$ とnegative itemのeasy factor $e_n^{easy}$ の差 $\mathbf{e}_{dif}$ を計算する:

$$
\mathbf{e}_{dif} = \mathbf{e}_p^{''} - \mathbf{e}_n^{easy}
\tag{8}
$$

A first attempt is to directly make e𝑑𝑖 𝑓 as the direction of the augmentation.
最初の試みは、$\mathbf{e}_{dif}$ を増強の方向として直接作ることである。
This design is less desirable because
このデザインは理想的ではない。理由は以下:
(1) it introduces too much positive information, which may turn the augmented negative item into positive.
(1)ポジティブな情報が多すぎるため、拡張されたnegative itemがpositiveになってしまう可能性がある。(= 同一のembedding になってしまう??:thinking:)
(2) It contains too much prior information (i.e., the easy factor is identical to that of the positive item), which can lead to the model collapse problem [28, 29].
(2)事前情報が多すぎる(i.e. easy factor がpositive itemのそれと同じである)ため、モデル崩壊の問題につながる可能性がある[28, 29]。
Inspired by [40], we carefully smooth the direction of augmentation by extracting the quadrant information e𝑑𝑖𝑟 of e𝑑𝑖 𝑓 with the sign function 𝑠𝑔𝑛(·):
[40]に触発されて、$\mathbf{e}_{dif}$ の象限情報 $\mathbf{e}_{dir}$ を符号関数 $sgn(\cdot)$ で抽出することにより、augmentation方向を注意深く平滑化する:

$$
\mathbf{e}_{dir} = sgn(\mathbf{e}_{dif})
\tag{9}
$$

The direction e𝑑𝑖𝑟 ∈ R 𝑑 effectively compresses the embedding augmentation space into a quadrant space, which provides essential direction information without having the aforementioned issues.
方向 $\mathbf{e}_{dir} \in \mathbb{R}^d$ は、embedding augmentation space(埋め込み補強空間) を四分円空間に効果的に圧縮し、前述の問題を抱えることなく本質的な方向情報を提供する。

**側面2: Magnitude**:
マグニチュード：
Magnitude determines the strength of augmentation.
マグニチュードはオーグメンテーションの強さを決定する。
Several studies [14] have shown that when the perturbation to the embedding is overly large, it will dramatically change its original semantics.
いくつかの研究[14]は、埋め込みに対するperturbation(摂動?)が過度に大きくなると、元の semantics (概念?) が劇的に変化することを示している。
Therefore, we need to carefully calibrate the magnitude of the augmentation.
**したがって、補強の大きさを慎重に調整する必要がある**。(augmentatinの方向と規模、なるほど...!:thinking:)
We design a two-step approach to generate a regulated magnitude Δ ∈ R 𝑑 .
規制された大きさ $\Delta \in \mathbb{R}^d$ を生成するために、2段階のアプローチを設計する。
We first consider the distribution of Δ.
まず $\Delta$ の分布を考える。
As Δ is a noise embedding, we adopt a uniform distribution on the interval [0, 0.1].
Δは**ノイズの埋め込み**(?)であるため、**区間[0, 0.1]上の一様分布を採用**する。
The uniform distribution introduces a certain amount of randomness, which is beneficial to improve the robustness of the model.
**一様分布はある程度のランダム性を導入し、モデルのロバスト性を向上させるのに有効**である。
Second, we restrict Δ to be smaller than a margin.
次に、Δがマージンより小さくなるように制限する。(margin = 上限??:thinking:)
Instead of using a static scalar [22], we dynamically set the margin by calculating the similarity between the hard factors of the negative and corresponding positive items.
静的なスカラー[22]を使用する代わりに、negative itemと対応するpositive item の hard factor 間の類似度を計算することにより、マージンを動的に設定する。
The intuition is that a higher similarity between the hard factors suggests that the negative item already contains much useful information, and thus we should augment it with a smaller magnitude.
直感的には、**hard factor 間の類似度が高ければ高いほど、negative itemにはすでに多くの有用な情報が含まれていることを示唆し**、したがって、より小さな大きさでそれを補強すべきである。
Finally, the regulated magnitude Δ is calculated via
最後に、規制された大きさΔは次のようにして計算される。

$$
\|\Delta \| \leq \sigma()
\tag{10}
$$

where the element-wise product ⊙ is used to calculate the similarity between e ℎ𝑎𝑟𝑑 𝑛 and e ′ 𝑝 .
ここで、e ℎ↪Ll44E↩ 𝑛 と e ′ 𝑝 の類似度を計算するために要素ごとの積 ⊙ が使われる。
The transformation matrix W ∈ R 1×𝑑 is used to map the similarity vector to a scalar.
変換行列W∈R 1×_1D45は、類似性ベクトルをスカラーにマッピングするために使用される。
The sigmoid function 𝜎(·) helps remove the sign information to avoid interfering with the learned direction e𝑑𝑖𝑟.
シグモイド関数𝜎(-)は、学習された方向e𝑑𝑖𝑟に干渉しないように符号情報を除去するのに役立つ。
After carefully determining the direction and magnitude, we can generate the augmented version e 𝑎𝑢𝑔 𝑛 of the negative item e𝑛 as follows
方向と大きさを注意深く決定した後、負の項目e𝑛の増大版e 𝑎𝑢を以下のように生成することができる。

$$
\tag{11}
$$

With our design, the augmented negative item becomes more similar to the corresponding positive item without causing huge changes of the semantics, and can remain negative.
私たちのデザインでは、拡張されたネガティブ項目は、意味論に大きな変化をもたらすことなく、対応するポジティブ項目により近くなり、ネガティブのままであり続けることができる。
We apply the above operation to every item in the candidate negative set E and obtain the augmented negative set E 𝑎𝑢𝑔 .
候補否定集合Eのすべての項目に上記の操作を適用し、拡張否定集合E 𝑎𝑄を得る。

## 4.3. Sampling サンプリング

After obtaining the augmented candidate negative set E 𝑎𝑢𝑔, we need to devise a sampling strategy to select the best negative item from E 𝑎𝑢𝑔 to facilitate model training.
拡張された否定候補集合E𝑎が得られたら、モデル学習を容易にするために、E𝑎𝑔から最適な否定項目を選択するサンプリング戦略を考案する必要がある。
Existing hard negative sampling methods select the negative item with the highest score, where the score is calculated by the score function 𝑠(·, ·) with the user and negative item embeddings as input.
既存のハードネガティブサンプリング法は、最も高いスコアを持つネガティブ項目を選択する。スコアは、ユーザとネガティブ項目の埋め込みを入力として、スコア関数𝑠(-, -)によって計算される。
However, as explained before, negative items with relatively low scores will be seldom selected, which leads to the information discrimination issue.
しかし、先に説明したように、相対的に得点の低い否定的な項目はほとんど選択されない。
Although the augmentation can already alleviate information discrimination to a certain extent, we further design a more flexible and effective sampling strategy by introducing a new metric named augmentation gain.
オーグメンテーションはすでに情報識別をある程度緩和することができるが、我々はさらにオーグメンテーションゲインという新しい指標を導入することで、より柔軟で効果的なサンプリング戦略を設計する。
Augmentation gain measures the score difference before and after the augmentation.
オーグメンテーション・ゲインは、オーグメンテーション前後のスコア差を測定する。
Formally, the score 𝑠𝑐𝑜𝑟𝑒 and the augmentation gain 𝑠𝑐𝑜𝑟𝑒𝑎𝑢𝑔 are calculated as:
正式には、スコア𝑠𝑐𝑜𝑅𝑒と増強ゲイン𝑠𝑐𝑎𝑢𝑔は以下のように計算される：

$$
\tag{12}
$$

The sampling module we propose considers both 𝑠𝑐𝑜𝑟𝑒 and 𝑠𝑐𝑜𝑟𝑒𝑎𝑢𝑔 to select the suitable negative item e 𝑓 𝑖𝑛𝑎𝑙 𝑛 from the augmented candidate negative set E 𝑎𝑢𝑔.
我々が提案するサンプリング・モジュールは、𝑠𝑐𝑅と𝑒𝑐𝑅の両方を考慮し、拡張された否定候補集合EᵄEᵄから適切な否定項目eᵄE𝑔を選択する。
To explicitly balance the contributions between 𝑠𝑐𝑜𝑟𝑒 and 𝑠𝑐𝑜𝑟𝑒𝑎𝑢𝑔, we introduce a trade-off parameter 𝜖.
...
The final augmented negative item e 𝑓 𝑖𝑛𝑎𝑙 𝑛 is chosen via
最終的な否定項目e 𝑓𝑖𝑛𝑎𝑙𝑛は次のようにして選ばれる。

$$
\tag{13}
$$

## 4.4. Discussion

It is worth noting that most existing negative sampling methods can be considered as a special case of ANS.
既存のほとんどのネガティブサンプリング法は、ANSの特殊なケースと考えることができることは注目に値する。
For example, DNS [41] can be obtained by removing the disentanglement and augmentation steps.
例えば、DNS [41]は、分離とオーグメンテーションのステップを削除することで得られる。
MixGCF [16] can be obtained by removing the disentanglement step and replacing the regulated augmentation with unconstrained augmentation based on graph structure information and positive item information.
MixGCF[16]は、離散化ステップを削除し、グラフ構造情報と正項目情報に基づく無制約オーグメンテーションで規制オーグメンテーションを置き換えることで得られる。
SRNS [9] can be obtained by removing the augmentation step and considering variance in the sampling strategy step.
SRNS[9]は、オーグメンテーションのステップを削除し、サンプリング戦略のステップで分散を考慮することによって得ることができる。

## 4.5. Model Optimization モデル最適化

Finally, we adopt the proposed ANS method as the negative sampling strategy and take into consideration also the recommendation loss L to optimize the parameters Θ of an implicit CF model (e.g., MF-BPR).
最後に、暗黙的CFモデル（例えばMF-BPR）のパラメータΘを最適化するために、負のサンプリング戦略として提案されたANS法を採用し、推薦損失Lも考慮する。

$$
\tag{14}
$$

where 𝜆 is a hyper-parameter controlling the strength of 𝐿2 regularization, and 𝛾 is another hyper-parameter used to adjust the impact of the contrastive loss and the disentanglement loss.
ここで𝜆は↪Lu_1D43F 正則化の強さを制御するハイパーパラメータで、Ǿはコントラスト損失と不連続性損失の影響を調整するためのもう1つのハイパーパラメータである。
Observably, our negative sampling strategy paradigm can be seamlessly incorporated into mainstream models without the need for substantial modifications.
観察によれば、我々のネガティブサンプリング戦略のパラダイムは、大幅な修正を必要とすることなく、主流のモデルにシームレスに組み込むことができる。

# 5. Experiment 実験

In this section, we conduct comprehensive experiments to answer the following key research questions: • RQ1: How does ANS perform compared to the baselines and integrating ANS into different mainstream CF models perform compared with the original ones? • RQ2: How accurate is the disentanglement step in the absence of ground truth? • RQ3: Can ANS alleviate ambiguous trap and information discrimination? • RQ4: How do different steps affect ANS’s performance? • RQ5: How do different hyper-parameter settings (i.e., 𝛾, 𝜖, and 𝑀) affect ANS’s performance? • RQ6: How does ANS perform in efficiency?
このセクションでは、以下の主要な研究課題に答えるために包括的な実験を行う：

- RQ1：
  ANSはベースラインと比較して、またANSを異なる主流CFモデルに統合した場合、元のモデルと比較してどのように機能するのか？- RQ2：
  グランドトゥルースがない場合、ディスエンタングルメントステップはどの程度正確か？- RQ3：
  ANSは曖昧トラップと情報識別を緩和できるか？- RQ4：
  異なるステップはANSの性能にどのような影響を与えるか？- RQ5：
  ハイパーパラメーターの設定（すなわち、↪Ll_1FE, ↪Ll_1FE, ↪Ll_1FE, 𝑀）の違いはANSの性能にどのような影響を与えるか？- RQ6：
  ANSの効率性はどの程度か？

## 5.1. Experimental Setup 実験セットアップ

### 5.1.1. Datasets. データセット

We consider five public benchmark datasets in the experiments: Amazon-Baby, Amazon-Beauty, Yelp2018, Gowalla, and Last.fm.
実験では、5つのパブリック・ベンチマーク・データセットを検討する：
Amazon-Baby、Amazon-Beauty、Yelp2018、Gowalla、Last.fmである。
In order to comprehensively showcase the efficacy of the proposed methodology, we have partitioned the dataset into two distinct categories for processing.
提案手法の有効性を包括的に示すため、データセットを2つの異なるカテゴリーに分割して処理した。
For the datasets Amazonbaby, Amazon-Beauty, and Last.fm, the training set is constructed by including only the interactions that occurred on or before a specified timestamp, similar to the approach used in the state-of-theart method DENS [21].
データセットAmazonbaby、Amazon-Beauty、Last.fmについては、最新の手法DENS[21]で使用されているアプローチと同様に、指定されたタイムスタンプ以前に発生したインタラクションのみを含むことによってトレーニングセットが構築される。
After reserving the remaining interactions for the test set, a validation set is created by randomly sampling 10% of the interactions from the training set.
テストセット用に残りのインタラクションを確保した後、トレーニングセットから10%のインタラクションをランダムにサンプリングして検証セットを作成する。
The adoption of this strategy, as suggested by previous works [4, 22, 32], provides the benefit of preventing data leakage.
先行研究[4, 22, 32]で示唆されているように、この戦略を採用することで、データ漏洩を防ぐことができるという利点がある。
For Yelp and Gowalla, we have followed the conventional practice of utilizing an 80% training set, 10% test set, and 10% validation set.
YelpとGowallaについては、80％のトレーニングセット、10％のテストセット、10％の検証セットを利用するという従来のやり方に従っている。
These datasets have different statistical properties, which can reliably validate the performance of a model [7].
これらのデータセットには異なる統計的特性があり、モデルの性能を確実に検証することができる[7]。
Table 1 summarizes the statistics of the datasets.
表1にデータセットの統計をまとめた。

### 5.1.2. 2 Baseline Algorithms. 2 ベースライン・アルゴリズム

To demonstrate the effectiveness of the proposed ANS method, we compare it with several representative state-of-the-art negative sampling methods.
提案するANS法の有効性を実証するために、代表的な最新のネガティブサンプリング法と比較する。
• RNS [26]: Random negative sampling (RNS) adopts a uniform distribution to sample unobserved items.

- RNS [26]：
  ランダム・ネガティブ・サンプリング(RNS)は、未観測項目をサンプリングするために一様分布を採用する。
  • DNS [41]: Dynamic negative sampling (DNS) adaptively selects items with the highest score as the negative samples.
- DNS [41]：
  Dynamic negative sampling (DNS)は適応的に最も高いスコアを持つアイテムをネガティブサンプルとして選択する。
  • SRNS [9]: SRNS introduces variance to avoid the false negative item problem based on DNS.
- SRNS [9]：
  SRNSは、DNSに基づく偽陰性項目の問題を回避するために分散を導入する。
  • MixGCF [16]: MixGCF injects information from positive and graph to synthesizes harder negative samples.
- MixGCF [16]：
  MixGCFはポジティブとグラフから情報を注入し、より難しいネガティブサンプルを合成する。
  • DENS [21]: DENS disentangles relevant and irrelevant factors of items and designs a factor-aware sampling strategy.
- DENS [21]：
  DENSは項目の関連因子と非関連因子を分離し、因子を意識したサンプリング戦略を設計する。
  To further validate the effectiveness of our proposed methodology, we have integrated it with a diverse set of representative models.
  提案した手法の有効性をさらに検証するため、多様な代表的モデル群との統合を行った。
  • NGCF [35]: NGCF employs a message-passing scheme to effectively leverage the high-order information.
- NGCF [35]：
  NGCFは、高次情報を効果的に活用するためにメッセージパッシング方式を採用している。
  • LightGCN [13]: LightGCN adopts a simplified approach by eliminating the non-linear transformation and instead utilizing a sum-based pooling module to enhance its performance.
- LightGCN [13]：
  LightGCNは、非線形変換を排除し、その代わりに和ベースのプーリング・モジュールを利用して性能を向上させるという、簡素化されたアプローチを採用している。
  • SGL [37]: SGL incorporates contrastive learning.
- SGL［37］：
  SGLは対照学習を取り入れたものである。
  The objective is to enhance the agreement between various views of the same node, while minimizing the agreement between views of different nodes.
  目的は、同じノードの様々なビュー間の一致を高め、異なるノードのビュー間の一致を最小化することである。

### 5.1.3. Implementation Details. 実施内容

Similar to previous studies [4, 26, 33], we consider MF-BPR [26] as the basic CF model.
先行研究[4, 26, 33]と同様に、MF-BPR[26]を基本的なCFモデルとして考える。
For a fair comparison, the size of embeddings is fixed to 64, and the embeddings are initialized with Xavier [10] for all methods.
公平な比較のために、埋め込みサイズは64に固定され、埋め込みはすべての手法でXavier [10]で初期化される。
We use Adam [20] to optimize the parameters with a default learning rate of 0.001 and a default mini-batch size of 2048.
Adam[20]を使用して、デフォルト学習率0.001、デフォルトミニバッチサイズ2048でパラメータを最適化する。
The 𝐿2 regularization coefficient 𝜆 is set to 10−4 .
正則化係数 ↪Lu_1D43F は 10-4 に設定される。
The size of the candidate negative item set 𝑀 is tested in the range of {2, 4, 8, 16, 32}.
否定項目候補集合のサイズ𝑀は{2, 4, 8, 16, 32}の範囲でテストされる。
The weight 𝛾 of the contrastive and disentanglement losses and 𝜖 of the augmentation gain are both searched in the range of [0, 1].
コントラスト損失とディセンタングルメント損失の重みǾとオーグメンテーションゲインの重み𝜖はともに[0, 1]の範囲で探索される。
In order to guarantee the replicability, our approach is implemented by the RecBole v1.1.1 framework [42].
再現性を保証するために、我々のアプローチはRecBole v1.1.1フレームワーク[42]によって実装されている。
We conducted statistical tests to evaluate the significance of our experimental results.
実験結果の有意性を評価するために統計的検定を行った。

## 5.2. RQ1: Overall Performance Comparison RQ1：

総合的なパフォーマンス比較

Table 2 shows the results of training MF-BPR with different negative sampling methods.
表2は、異なるネガティブサンプリング方法でMF-BPRを訓練した結果を示している。
Additionally, the performance of ANS under different models is presented in Table 3.
さらに、異なるモデルにおけるANSのパフォーマンスを表3に示す。
Due to space limitations, we are unable to present the results of other models using various negative sampling strategies.
紙面の都合上、様々なネガティブサンプリング戦略を用いた他のモデルの結果を紹介することはできない。
Nonetheless, it is worth noting that the experimental results obtained were similar with Table 2.
それにもかかわらず、得られた実験結果が表2と同様であったことは注目に値する。
We can make the following key observations:
私たちは次のような重要な見解を示すことができる：

• ANS yields the best performance on almost all datasets.

- ANSは、ほとんどすべてのデータセットで最高の性能を発揮する。
  In particular, its highest improvements over the strongest baselines are 29.74%, 23.76%, and 31.06% in terms of 𝐻𝑖𝑡 𝑅𝑎𝑡𝑖𝑜@15, 𝑅𝑒𝑐𝑎𝑙𝑙@15, and 𝑁𝐷𝐶𝐺@15 in Beauty, respectively.
  特に、最強のベースラインに対する最高の改善は、𝐻𝑖𝑡 ᵍᵅ ᵍ@15, ᵍᵅ@15, ᵍᵍ@15, ᵍᵍ@15 で、それぞれ29.74%、23.76%、31.06%である。
  This demonstrates that ANS is capable of generating more informative negative samples.
  これは、ANSがより有益な陰性サンプルを生成できることを示している。
  • The ANS’s remarkable adaptability is a noteworthy feature that allows for its seamless integration into various models.
- ANSの卓越した適応性は、さまざまなモデルへのシームレスな統合を可能にする特筆すべき特徴である。
  The results presented in Table 3 demonstrate that the incorporation of PAN into the base models leads to improvements across all datasets.
  表3に示す結果は、ベースモデルにPANを組み込むことで、すべてのデータセットで改善が見られることを示している。
  • The model-aware methods always outperform the model-agnostic methods (RNS).
- モデルを考慮した方法は、モデルを無視した方法（RNS）よりも常に優れている。
  In general, model-agnostic methods are difficult to guarantee the quality of negative samples.
  一般的に、モデル診断的手法は陰性サンプルの質を保証することが難しい。
  Leveraging various information from the underlying model is indeed a promising research direction.
  基礎となるモデルから様々な情報を活用することは、実に有望な研究の方向性である。
  • Despite its simplicity, DNS is a strong baseline.
- そのシンプルさにもかかわらず、DNSは強力なベースラインである。
  This fact justifies our motivation of studying the hardness from a more fine granularity.
  この事実は、より細かい粒度から硬さを研究するという我々の動機を正当化する。

## 5.3. RQ2: Disentanglement Performance RQ2：

切断パフォーマンス

To verify the disentanglement performance, we spot-check a user and use the T-SNE algorithm [30] to map the disentangled factors into a two-dimensional space.
逆接の性能を検証するために、ユーザーをスポットチェックし、T-SNEアルゴ リズム[30]を使用して、逆接された因子を2次元空間にマッピングする。
The results are shown in Figure 4(a).
結果を図4(a)に示す。
We can observe that e ℎ𝑎𝑟𝑑 𝑛 and e ′ 𝑝 are clustered together, confirming that they are indeed similar.
e ℎ𝑎𝑑とe ′𝑝が一緒にクラスタ化されていることが観察され、両者が確かに類似していることが確認できる。
In contrast, e 𝑒𝑎𝑠𝑦 𝑛 and e ′′ 𝑝 are more scattered, indicating that they do not carry similar information, which is consistent with our previous analysis.
対照的に、e 𝑒 𝑛とe ′ 𝑎 𝑠はより散らばっており、同様の情報を持っていないことを示している。
The hard factors should contain most of the useful information of negative items, and thus if we use only hard factors, instead of the entire original item, to train a model, we should achieve similar performance.
ハード・ファクターにはネガティブ項目の有用な情報がほとんど含まれているはずなので、元の項目全体ではなく、ハード・ファクターだけを使用してモデルを訓練しても、同じようなパフォーマンスが得られるはずである。
We validate it by two experiments.
我々は2つの実験によってそれを検証する。
First, we plot the curves of 𝑅𝑒𝑐𝑎𝑙𝑙@20 in Figure 4(b).
まず、図4(b)に𝑅ᵅ@20 の曲線をプロットする。
HNS is a variant of RNS, which uses our disentanglement step to extract the hard factors of items and then uses only hard factors to train the model.
HNSはRNSの変形であり、我々が開発した離散化ステップを使用してアイテムのハードファクターを抽出し、次にハードファクターのみを使用してモデルを訓練する。
It can be observed that the performance of HNS is comparable to that of RNS.
HNSの性能はRNSと同等であることがわかる。
The two curves are similar, confirming that the hard factors indeed capture the most useful information of negative items.
この2つの曲線は類似しており、ハードファクターが確かにネガティブ項目の最も有用な情報を捉えていることを裏付けている。
Second, we revisit Figure 2 in Section 3.3.It can be seen that PER(RNS, HNS) is small, which means that HNS captures most of information learned in RNS.
PER(RNS、HNS)は小さく、これはHNSがRNSで学習した情報のほとんどを捉えていることを意味する。
In summary, our disentanglement step can effectively disentangle a negative sample into hard and easy factors, which lays a solid foundation for the subsequent steps in ANS.
まとめると、我々の逆接ステップは、ネガティブサンプルをハードファクターとイージーファクターに効果的に逆接できる。

## 5.4. RQ3: Ambiguous Trap and Information Discrimination RQ3：

曖昧な罠と情報弁別

### 5.4.1. Ambiguous Trap. 曖昧な罠。

Demonstrating how ANS can mitigate the ambiguous trap is a challenging task.
ANSが曖昧な罠をどのように緩和できるかを実証することは、挑戦的な課題である。
A first attempt is to show the augmentation gain of the augmented negative samples.
最初の試みは、オーグメンテーションされたネガティブサンプルのオーグメンテーションゲインを示すことである。
However, this idea is flawed because larger augmentation gain cannot always guarantee better performance (e.g., larger augmentation gain can be achieved by introducing a large number of false positive items).
しかし、この考え方には欠陥がある。というのも、オーグメンテーションの利得が大きければ大きいほど、常に性能が向上するとは限らないからだ（たとえば、オーグメンテーションの利得を大きくすると、多数の偽陽性項目を導入することになる）。
Therefore, we choose to analyze the curves of 𝑅𝑒𝑐𝑎𝑙𝑙@20 to show how ANS can mitigate the ambiguous trap, which is shown in Figure 5.
そこで、図5に示すように、ANSがどのように曖昧なトラップを軽減できるかを示すために、𝑅ᑒᑙ@20の曲線を解析することにした。
Generally, the steeper the curve is, the more information the model can learn in this epoch from negative samples.
一般的に、曲線が急であればあるほど、モデルはこのエポックで負のサンプルからより多くの情報を学習することができる。
We can observe that DNS outperforms RNS because its 𝑅𝑒𝑐𝑎𝑙𝑙@20 is always higher than that of RNS and the curve is steeper than that of RNS.
DNS の 𝑅ᑒ@20 は常に RNS よりも高く、RNS の ᑙᑙ@20 よりも曲線が急であるため、DNS が RNS よりも優れていることがわかる。
It again confirms that hard negative sampling is an effective sampling strategy.
ハード・ネガティブ・サンプリングが効果的なサンプリング戦略であることが改めて確認された。
In contrast, the curve of ANS exhibits distinct patterns.
対照的に、ANSの曲線は明確なパターンを示す。
At the beginning (from epoch 0 to epoch 30), 𝑅𝑒𝑐𝑎𝑙𝑙@20 is low because ANS needs extra efforts to learn how to disentangle and augment negative samples.
初期（エポック0からエポック30まで）には、 𝑅ᵅ@20 が低い。これは、ANSが負のサンプルの分離と補強の方法を学習するために余分な努力が必要だからである。
As the training process progresses (from epoch 30 to epoch 95), ANS demonstrates a greater average gradient.
トレーニングが進むにつれて（エポック30からエポック95まで）、ANSはより大きな平均勾配を示す。
This proves that ANS can generate harder synthetic negative samples, which can largely mitigate the ambiguous trap issue.
これは、ANSがより困難な合成ネガティブサンプルを生成できることを証明しており、曖昧なトラップの問題を大きく軽減することができる。

### 5.4.2. Information Discrimination. 情報差別。

As for the information discrimination problem, we have shown that the disentanglement step can effectively extract the useful information from low-score items.
情報識別問題に関しては、分離ステップが低得点項目から有用な情報を効果的に抽出できることを示した。
However, we have not shown that ANS can select more low-score negative items in the training process.
しかし、ANSが訓練過程において、より低得点のネガティブ項目を選択できることは示していない。
To this end, we analyze the percentages of overlapping negative samples between ANS and DNS.
そのため、ANSとDNSの陰性サンプルの重複率を分析した。
The results are presented in Table 4.
結果を表4に示す。
Recall that DNS always chooses the negative items with the highest scores as the hard negative samples.
DNSは常に最もスコアの高いネガティブ項目をハードネガティブサンプルとして選択することを思い出してください。
A less than 50% overlapping indicates that ANS does sample more low-score negative items before the augmentation and effectively alleviates the information discrimination problem.
オーバーラップが50％以下であることは、ANSがオーグメンテーションの前に低スコアのネガティブ項目をより多くサンプリングし、情報識別の問題を効果的に軽減していることを示している。

## 5.5. RQ4: Ablation Study RQ4：

アブレーション研究

We analyze the effectiveness of different components in our model, and evaluate the performance of the following variants of our model: (1) ANS without disentanglement (ANS w/o dis).(2) ANS without augmentation gain (ANS w/o gain).(3) ANS without regulated direction (ANS w/o dir).(4) ANS without regulated magnitude (ANS w/o mag).
我々は、我々のモデルにおける様々な構成要素の有効性を分析し、我々のモデルの以下の変種の性能を評価する：
(1) ANS without disentanglement (ANS w/o dis) (2) ANS without augmentation gain (ANS w/o gain) (3) ANS without regulated direction (ANS w/o dir) (4) ANS without regulated magnitude (ANS w/o mag).
It is noteworthy to state that the complete elimination of the augmentation step is not taken into consideration due to its equivalence to DNS.
DNSと同等であるため、補強ステップの完全な排除は考慮されていないことは注目に値する。
The results are presented in Table 5.
結果を表5に示す。
We can observe that all components we propose can positively contribute to model performance.
我々は、我々が提案するすべてのコンポーネントが、モデルのパフォーマンスにプラスに寄与することを観察することができる。
In particular, the results show that unconstrained augmentation (e.g., ANS w/o mag) cannot achieve meaningful performance.
特に、制約のないオーグメンテーション（例えば、マグを使わないANS）では、意味のあるパフォーマンスを達成できないことが示された。
This fact confirms that the existing unconstrained augmentation techniques cannot be directly applied to CF.
この事実は、既存の制約なしオーグメンテーション技術がCFに直接適用できないことを裏付けている。

## 5.6. RQ5: Hyper-Parameter Sensitivity RQ5：

ハイパーパラメーターの感度

### 5.6.1. Impact of 𝛾. の影響。

We present the effect of the weight of the contrastive loss and disentanglement loss, 𝛾, in Figure 6.
図6に、コントラスト損失とディセンタングルメント損失の重み↪L_1FE↩の効果を示す。
As the value of 𝛾 increases, we can first observe notable performance improvements, which proves that both loss functions are beneficial for the CF model.
このことは、どちらの損失関数もCFモデルにとって有益であることを証明している。
It is interesting to observe that once 𝛾 becomes larger than a threshold, the performance drops sharply.
Ǿが閾値より大きくなると、性能が急激に低下することは興味深い。
This observation is expected because in this case the CF model considers the disentanglement as the primary task and ignores the recommendation task.
この場合、CFモデルはディセンタングルメントを主要なタスクとみなし、推薦タスクを無視するため、このような結果が出ることが予想される。
Nevertheless, ANS can achieve reasonable performance under a relatively wide range of 𝛾 values.
とはいえ、ANSは比較的広い範囲の↪Ll_1FE 値の下で妥当な性能を達成することができる。

### 5.6.2. Impact of 𝜖. 𝜖 の影響。

Recall that 𝜖 is the parameter to balance the importance between the score and the augmentation gain in the sampling step.
↪Ll_1D716 は、サンプリングステップにおけるスコアと増大ゲインの重要度のバランスをとるためのパラメータである。
Figure 7(a) presents the results of different 𝜖 values.
図7(a)は、↪Ll_1D716 の値を変えた場合の結果である。
A small 𝜖 value overlooks the importance of the augmentation gain and only achieves sub-optimal performance; a large 𝜖 value may favor an item with a lower score (but a larger score difference), which will reduce the gradient and hurt model performance.
𝜖値を小さくすると、補強利得の重要性が見落とされ、最適以下のパフォーマンスしか得られません。𝜖値を大きくすると、スコアが低い（しかしスコア差が大きい）項目が有利になり、勾配が減少してモデルのパフォーマンスが低下します。
But still, ANS can obtain good performance under a relatively wide range of 𝜖 values.
しかしそれでも、ANSは比較的広い範囲の𝜖値の下で良好な性能を得ることができる。

### 5.6.3. Impact of 𝑀. 𝑀 の影響。

𝑀 denotes the size of candidate negative set E.
𝑀 は否定候補集合Eのサイズを表す。
The present study illustrates the impact of 𝑀 on performance, as depicted in Figure 8.
本研究では、図8に示すように、↪Lu_1D440 がパフォーマンスに与える影響を示している。
It is evident that an increase in 𝑀 leads to more negative samples, we can get harder negative samples by augmentation, thereby resulting in a performance improvement.
↪Lu_1D440 を増加させると、より多くの負サンプルが得られることは明らかであり、オーグメンテーションによってより難しい負サンプルを得ることができる。
Nevertheless, it is noteworthy that excessively large values of 𝑀 can considerably impede the efficiency of the models, and degrade performance due to noise (e.g., false negative samples).
とはいえ、 ↪Lu_1D440 の値が大きすぎると、モデルの効率性が著しく損なわれ、ノイズ（偽陰性サンプルなど）により性能が低下する可能性があることは注目に値する。

## 5.7. RQ6: Efficiency Analysis RQ6：

効率性分析

Following the previous work [22, 31], we also examine the efficiency of different negative sampling methods in Table 6.
先行研究[22, 31]に従い、表6では異なるネガティブサンプリング法の効率も検証している。
We report the average running time (in seconds) per epoch and the total number of epochs needed before reaching convergence.
エポックあたりの平均実行時間（秒）と、収束に達するまでに必要なエポック数の合計を報告する。
All three methods are relatively efficient.
この3つの方法はいずれも比較的効率的だ。
There is no wonder that RNS is the most efficient method as it is a model-agnostic strategy.
モデルにとらわれない戦略であるRNSが最も効率的な方法であることは不思議ではない。
Compared to DNS, our proposed ANS method requires more running time.
DNSと比較すると、我々の提案するANS法はより多くの実行時間を必要とする。
However, considering the huge performance improvement ANS brings, the additional running time is well justified.
しかし、ANSがもたらすパフォーマンスの大幅な向上を考えれば、追加される実行時間は十分に正当化できる。

# 6. Conclusion 結論

Motivated by ambiguous trap and information discrimination, from which the state-of-the-art negative sampling methods suffer, for the first time, we proposed to introduce synthetic negative samples from a fine-granular perspective to improve implicit CF.
最新のネガティブサンプリング法が苦しんでいる曖昧なトラップと情報識別に動機づけられ、我々は初めて、暗黙的CFを改善するために、細かい粒度の観点から合成ネガティブサンプルを導入することを提案した。
We put forward a novel generic augmented negative sampling (ANS) paradigm, along with a concrete implementation.
我々は、新しい一般的な拡張ネガティブサンプリング（ANS）パラダイムと、その具体的な実装を提案する。
The paradigm consists of three major steps.
パラダイムは大きく3つのステップからなる。
The disentanglement step disentangles negative items into hard and easy factors in the absence of supervision signals.
分離ステップでは、監督信号がない場合、ネガティブ項目をハード要因とイージー要因に分離する。
The augmentation step generates synthetic negative items using carefully calibrated noise.
増強ステップでは、慎重に調整されたノイズを使用して合成ネガティブ項目を生成する。
The sampling step makes use of a new metric called augmentation gain to effectively alleviate information discrimination.
サンプリング・ステップでは、情報の識別を効果的に緩和するために、オーグメンテーション・ゲインと呼ばれる新しいメトリックを使用する。
Comprehensive experiments demonstrate that ANS can significantly improve model performance and represents an exciting new research direction.
包括的な実験により、ANSがモデルの性能を大幅に改善できることが実証され、エキサイティングな新しい研究の方向性が示された。
In our future work, we intend to explore the efficacy of augmented negative samples in tackling various issues such as fairness and popularity bias.
今後の研究では、公平性や人気バイアスといった様々な問題に取り組む上で、増強されたネガティブサンプルの有効性を探るつもりである。
Additionally, we will actively investigate the effectiveness of employing augmented negative sampling in online experiments.
さらに、オンライン実験における増強ネガティブサンプリングの有効性を積極的に調査する。
