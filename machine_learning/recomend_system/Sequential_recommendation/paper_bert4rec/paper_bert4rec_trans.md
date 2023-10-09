## 0.1. link リンク

https://arxiv.org/abs/1904.06690
https://arxiv.org/abs/1904.06690

## 0.2. title タイトル

BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer
BERT4Rec：
トランスフォーマからの双方向エンコーダ表現による逐次推薦

## 0.3. abstract 抄録

Modeling users’ dynamic preferences from their historical behaviors is challenging and crucial for recommendation systems.
ユーザの過去の行動から動的な嗜好をモデル化することは、推薦システムにとって挑戦的かつ重要である。
Previous methods employ sequential neural networks to encode users’ historical interactions from left to right into hidden representations for making recommendations.
これまでの手法では、逐次的なニューラルネットワークを採用し、ユーザーの過去のやりとりを左から右へとレコメンデーションするための隠れ表現にエンコードする。
Despite their effectiveness, we argue that such left-to-right unidirectional models are sub-optimal due to the limitations including: a) unidirectional architectures restrict the power of hidden representation in users’ behavior sequences; b) they often assume a rigidly ordered sequence which is not always practical.
その有効性にもかかわらず、我々はこのような左から右への一方向モデルは、以下のような制限のために最適ではないと主張する：
a)一方向アーキテクチャは、ユーザーの行動シーケンスにおける隠れた表現力を制限する。
b)uni-directionalアーキテクチャは、hogehoge
To address these limitations, we proposed a sequential recommendation model called BERT4Rec, which employs the deep bidirectional self-attention to model user behavior sequences.
これらの限界に対処するために、我々は、BERT4Recと呼ばれる逐次レコメンデーションモデルを提案した。
To avoid the information leakage and efficiently train the bidirectional model, we adopt the Cloze objective to sequential recommendation, predicting the random masked items in the sequence by jointly conditioning on their left and right context.
情報漏洩を回避し、双方向モデルを効率的に学習するために、我々は**Cloze Objective**を逐次推薦に採用する。
In this way, we learn a bidirectional representation model to make recommendations by allowing each item in user historical behaviors to fuse information from both left and right sides.
このように、ユーザの履歴行動の**各itemに左右の情報を融合させる**ことで、双方向表現モデルを学習し、レコメンデーションを行う。
Extensive experiments on four benchmark datasets show that our model outperforms various state-of-the-art sequential models consistently
4つのベンチマークデータセットを用いた広範な実験により、我々のモデルが様々な最新の逐次モデルを一貫して凌駕することが示された。

# 1. Introduction はじめに

Accurately characterizing users’ interests lives at the heart of an effective recommendation system.
ユーザーの興味を正確に把握することは、効果的な推薦システムの中核をなす。
In many real-world applications, users’ current interests are intrinsically dynamic and evolving, influenced by their historical behaviors.
多くの実世界のアプリケーションでは、**ユーザの現在の興味は、過去の行動に影響され、本質的にダイナミックで進化している**。
For example, one may purchase accessories (e.g., Joy-Con controllers) soon after buying a Nintendo Switch, though she/he will not buy console accessories under normal circumstances.
例えば、ニンテンドースイッチを買ってすぐにアクセサリー（Joy-Conコントローラーなど）を買うかもしれないが、通常であればゲーム機のアクセサリーを買うことはない。

To model such sequential dynamics in user behaviors, various methods have been proposed to make sequential recommendations based on users’ historical interactions [15, 22, 40].
ユーザー行動におけるこのような逐次的なダイナミクスをモデル化するために、ユーザーの過去のインタラクションに基づいて逐次的な推薦を行う様々な方法が提案されている[15, 22, 40]。
They aim to predict the successive item(s) that a user is likely to interact with given her/his past interactions.
これは、ユーザーが過去のインタラクションから、次にインタラクションしそうなアイテムを予測することを目的としている。
Recently, a surge of works employ sequential neural networks, e.g., Recurrent Neural Network (RNN), for sequential recommendation and obtain promising results [7, 14, 15, 56, 58].
最近、逐次推薦にリカレント・ニューラル・ネットワーク（RNN）などの逐次ニューラルネットワークを採用する研究が急増し、有望な結果が得られている[7, 14, 15, 56, 58]。
The basic paradigm of previous work is to encode a user’s historical interactions into a vector (i.e., representation of user’s preference) using a left-to-right sequential model and make recommendations based on this hidden representation.
これまでの研究の基本的なパラダイムは、**左から右への逐次モデルを使用して、ユーザーの過去のインタラクションをベクトル（すなわち、ユーザの嗜好の表現）に符号化**し、このhidden representationに基づいて推薦を行うことである。

Despite their prevalence and effectiveness, we argue that such left-to-right unidirectional models are not sufficient to learn optimal representations for user behavior sequences.
このような左から右への一方向的なモデルは、その普及率と有効性にもかかわらず、**ユーザの行動シーケンスに最適な表現を学習するには十分ではないと主張する**。
The major limitation, as illustrated in Figure 1c and 1d, is that such unidirectional models restrict the power of hidden representation for items in the historical sequences, where each item can only encode the information from previous items.
図1cと1dに示されているように、このような一方向のモデルでは、**各itemが前のitemからの情報しか符号化できないため、履歴シーケンスのitemに対する隠れ表現の力が制限されるという大きな限界**がある。
Another limitation is that previous unidirectional models are originally introduced for sequential data with natural order, e.g., text and time series data.
もう1つの限界は、これまでの一方向モデルはもともと、テキストや時系列データなど、自然な順序を持つ逐次データに対して導入されたものだということだ。
They often assume a rigidly ordered sequence over data which is not always true for user behaviors in real-world applications.
それらはしばしば、データ上の厳密な順序を想定しているが、実際のアプリケーションにおけるユーザー行動には必ずしも当てはまらない。(推薦に有用な隠れ表現を作る事が目的なのだから、厳密にuni-directionalを守る事は重要ではない、みたいな??:thinking:)
In fact, the choices of items in a user’s historical interactions may not follow a rigid order assumption [18, 54] due to various unobservable external factors [5].
実際、ユーザーの過去のインタラクションにおけるアイテムの選択は、様々な観測不可能な外的要因 [5]のために、**rigid order assumption(厳密な順序の仮定) [18, 54]**に従わないかもしれない。
In such a situation, it is crucial to incorporate context from both directions in user behavior sequence modeling.
このような状況では、ユーザ行動シーケンスのモデリングにおいて、双方向からのコンテキストを組み込むことが極めて重要である。

To address the limitations mentioned above, we seek to use a bidirectional model to learn the representations for users’ historical behavior sequences.
上記の限界に対処するため、私たちは双方向モデルを使用して、ユーザーの過去の行動シーケンスに対する表現を学習することを目指している。
Specifically, inspired by the success of BERT [6] in text understanding, we propose to apply the deep bidirectional self-attention model to sequential recommendation, as illustrated in Figure 1b.
具体的には、テキスト理解におけるBERT[6]の成功に触発されて、図1bに示すように、深層双方向自己アテンションモデルを逐次推薦に適用することを提案する。
For representation power, the superior results for deep bidirectional models on text sequence modeling tasks show that it is beneficial to incorporate context from both sides for sequence representations learning [6].
表現力については、テキストシーケンスのモデリングタスクにおける深層双方向モデルの優れた結果が、シーケンス表現学習において双方からのコンテキストを取り入れることが有益であることを示している[6]。
For rigid order assumption, our model is more suitable than unidirectional models in modeling user behavior sequences since all items in the bidirectional model can leverage the contexts from both left and right side.
厳密な順序を仮定した場合、双方向モデルのすべての項目が左右両方のコンテキストを利用できるため、ユーザーの行動シーケンスをモデル化する上で、一方向モデルよりも我々のモデルの方が適している。

However, it is not straightforward and intuitive to train the bidirectional model for sequential recommendation.
しかし、逐次推薦のための双方向モデルを学習するのは、直感的で簡単なことではない。
Conventional sequential recommendation models are usually trained left-to-right by predicting the next item for each position in the input sequence.
従来の逐次推薦モデルは、通常、入力シーケンスの各位置に対して次のアイテムを予測することにより、左から右へと学習される。
As shown in Figure 1, jointly conditioning on both left and right context in a deep bidirectional model would cause information leakage, i.e., allowing each item to indirectly “see the target item”.
図1に示すように、深い双方向モデルにおいて左右両方の文脈を共同で条件付けすると、情報の漏れが生じる、つまり、各itemが間接的に「対象itemを見る」ことができるようになる。
This could make predicting the future become trivial and the network would not learn anything useful.
これでは、未来を予測することは些細なことになりかねず、ネットワークは何も有益なことを学べなくなる。

To tackle this problem, we introduce the Cloze task [6, 50] to take the place of the objective in unidirectional models (i.e., sequentially predicting the next item).
この問題に取り組むため、**一方向モデルにおける目的（つまり、次の項目を逐次予測する=next item prediction:thinking:）の代わりに、Clozeタスク[6, 50]**を導入する。(Clozeタスク??:thinking:)
Specifically, we randomly mask some items (i.e., replace them with a special token [mask]) in the input sequences, and then predict the ids of those masked items based on their surrounding context.
具体的には、入力シーケンス中のいくつかのアイテムをランダムにマスクし（つまり、特別なトークン[mask]で置き換える）、次にそれらの周囲のコンテキストに基づいて、マスクされたアイテムのIDを予測する。(要するにBERTのmasked-item-predictionか...!:thinking:)
In this way, we avoid the information leakage and learn a bidirectional representation model by allowing the representation of each item in the input sequence to fuse both the left and right context.
このようにして、入力シーケンスの各アイテムの表現が左と右のコンテキストの両方を融合するようにすることで、情報の漏れを回避し、双方向表現モデルを学習する。
In addition to training a bidirectional model, another advantage of the Cloze objective is that it can produce more samples to train a more powerful model in multiple epochs.
双方向モデルのトレーニングに加えて、**Cloze目的関数のもう一つの利点は、より強力なモデルを複数のエポックでトレーニングするために、より多くのサンプルを生成できること**である。(??)
However, a downside of the Cloze task is that it is not consistent with the final task (i.e., sequential recommendation).
しかし、**クロース・タスクの欠点は、最終タスク（つまり逐次推薦）と整合性がないこと**である。
To fix this, during the test, we append the special token “[mask]” at the end of the input sequence to indicate the item that we need to predict, and then make recommendations base on its final hidden vector.
これを解決するために、テスト中に、予測する必要がある項目を示すために、入力シーケンスの最後に特別なトークン"[mask]"を追加し、その最終的な隠れベクトルに基づいて推薦を行う。
Extensive experiments on four datasets show that our model outperforms various state-of-the-art baselines consistently.
4つのデータセットを用いた広範な実験により、我々のモデルが様々な最先端のベースラインを一貫して凌駕することが示された。

The contributions of our paper are as follows:
本稿の貢献は以下の通りである：

- We propose to model user behavior sequences with a bidirectional self-attention network through Cloze task. 我々は、**Cloze taskを用いる双方向のself-attentionネットワーク**を用いてユーザの行動シーケンスをモデル化することを提案する。To the best of our knowledge, this is the first study to introduce deep bidirectional sequential model and Cloze objective into the field of recommendation systems. 我々の知る限り、これは推薦システムの分野に深層双方向逐次モデルとCloze objectiveを導入した最初の研究である。

- We compare our model with state-of-the-art methods and demonstrate the effectiveness of both bidirectional architecture and the Cloze objective through quantitative analysis on four benchmark datasets. 我々のモデルを最新の手法と比較し、4つのベンチマークデータセットの定量的分析を通じて、双方向アーキテクチャとCloze objectiveの有効性を実証する。

- We conduct a comprehensive ablation study to analyze the contributions of key components in the proposed model. 我々は、提案モデルの主要な構成要素の寄与を分析するために、包括的なアブレーション研究を行った。

# 2. Related Work 関連作品

In this section, we will briefly review several lines of works closely related to ours, including general recommendation, sequential recommendation, and attention mechanism.
このセクションでは、一般的な推薦、逐次的推薦、注意メカニズムなど、我々の研究と密接に関連するいくつかの研究を簡単にレビューする。

## 2.1. General Recommendation

Early works on recommendation systems typically use Collaborative Filtering (CF) to model users’ preferences based on their interaction histories [26, 43].
推薦システムに関する初期の研究では、一般的に協調フィルタリング（CF）を用いて、ユーザーの対話履歴に基づく嗜好をモデル化している[26, 43]。
Among various CF methods, Matrix Factorization (MF) is the most popular one, which projects users and items into a shared vector space and estimate a user’s preference on an item by the inner product between their vectors [26, 27, 41].
様々なCF手法の中で、行列因数分解（Matrix Factorization：MF）は最もポピュラーな手法であり、ユーザとアイテムを共有ベクトル空間に投影し、それらのベクトル間の内積によってアイテムに対するユーザの嗜好を推定する[26, 27, 41]。
Another line of work is item-based neighborhood methods [20, 25, 31, 43].
もう一つの研究は、項目ベースの近傍法である[20, 25, 31, 43]。
They estimate a user’s preference on an item via measuring its similarities with the items in her/his interaction history using a precomputed item-to-item similarity matrix.
これは、あらかじめ計算されたアイテム間の類似度行列を使用して、ユーザの対話履歴のアイテムとの類似度を測定することにより、アイテムに対するユーザの嗜好を推定する。(=Content-based filteringと言って良い?:thinking: CFと対をなして紹介されてるし...!)

Recently, deep learning has been revolutionizing the recommendation systems dramatically.
近年、ディープラーニングは推薦システムに劇的な革命をもたらしている。
The early pioneer work is a two-layer Restricted Boltzmann Machines (RBM) for collaborative filtering, proposed by Salakhutdinov et al.[42] in Netflix Prize1 .
初期の先駆的な研究は、Salakhutdinovら[42]がNetflix Prize1で提案した協調フィルタリングのための2層制限ボルツマンマシン（RBM）である。

One line of deep learning based methods seeks to improve the recommendation performance by integrating the distributed item representations learned from auxiliary information, e.g., text [23, 53], images [21, 55], and acoustic features [51] into CF models.
ディープラーニングに基づく手法の一系統は、補助情報、例えばテキスト[23, 53]、画像[21, 55]、音響特徴[51]から学習された**distributed item representations(分散アイテム表現)をCFモデルに統合することで、推薦性能を向上**させようとしている。(CF + CBのhybrid手法)
Another line of work seeks to take the place of conventional matrix factorization.
また、従来の行列分解に取って代わろうとする研究もある。
For example, Neural Collaborative Filtering (NCF) [12] estimates user preferences via Multi-Layer Perceptions (MLP) instead of inner product, while AutoRec [44] and CDAE [57] predict users’ ratings using Auto-encoder framework.
例えば、ニューラル協調フィルタリング（NCF）[12]は、内積の代わりに多層知覚（MLP）を介してユーザの嗜好を推定し、AutoRec[44]とCDAE[57]は、オートエンコーダーフレームワークを使用してユーザの評価を予測する。

## 2.2. Sequential Recommendation

Unfortunately, none of the above methods is for sequential recommendation since they all ignore the order in users’ behaviors.
残念ながら、上記の方法はどれも**ユーザの行動の順序を無視**しているため、逐次的な推薦には向いていない。

Early works on sequential recommendation usually capture sequential patterns from user historical interactions using Markov chains (MCs).
逐次レコメンデーションに関する初期の研究では、マルコフ連鎖（Markov Chain：MC）を用いて、ユーザの過去のインタラクションから逐次パターンを捉えるのが一般的である。
For example, Shani et al.[45] formalized recommendation generation as a sequential optimization problem and employ Markov Decision Processes (MDPs) to address it.
例えば、Shaniら[45]は推薦生成を逐次最適化問題として定式化し、マルコフ決定過程(MDP)を用いて対処している。
Later, Rendle et al.[40] combine the power of MCs and MF to model both sequential behaviors and general interests by Factorizing Personalized Markov Chains (FPMC).
その後、Rendleら[40]は、MCとMFのパワーを組み合わせて、因子化パーソナライズド・マルコフ連鎖（FPMC）により、逐次的行動と一般的興味の両方をモデル化した。
Besides the first-order MCs, high-order MCs are also adopted to consider more previous items [10, 11].
一次MCの他に、より多くの前のitemを考慮するために高次MCも採用されている[10, 11]。

Recently, RNN and its variants, Gated Recurrent Unit (GRU) [4] and Long Short-Term Memory (LSTM) [17], are becoming more and more popular for modeling user behavior sequences [7, 14, 15, 28, 37, 56, 58].
最近、RNNとその亜種であるGated Recurrent Unit（GRU）[4]とLong Short-Term Memory（LSTM）[17]は、ユーザの行動シーケンスをモデル化するためにますます人気が高まっている[7, 14, 15, 28, 37, 56, 58]。
The basic idea of these methods is to encode user’s previous records into a vector (i.e., representation of user’s preference which is used to make predictions) with various recurrent architectures and loss functions, including session-based GRU with ranking loss (GRU4Rec) [15], Dynamic REcurrent bAsket Model (DREAM) [58], user-based GRU [7], attention-based GRU (NARM) [28], and improved GRU4Rec with new loss function (i.e., BPR-max and TOP1-max) and an improved sampling strategy [14].
これらの手法の基本的な考え方は、様々なリカレント・アーキテクチャと損失関数を用いて、ユーザの過去の記録をベクトル(すなわち、 予測を行うために使用されるユーザのpreference representation）にエンコードすることである。
例えば、ランキング損失を持つセッションベースのGRU（GRU4Rec）[15]、Dynamic REcurrent bAsket Model（DREAM）[58]、user-based GRU[7]、attention-based GRU（NARM）[28]、および新しい損失関数(すなわち、BPR-maxとTOP1-max)と改善されたサンプリング戦略を持つ改良されたGRU4Rec[14]）が使用される。

Other than recurrent neural networks, various deep learning models are also introduced for sequential recommendation [3, 22, 33, 49].
リカレントニューラルネットワーク以外にも、逐次推薦のために様々なディープラーニングモデルが導入されている[3, 22, 33, 49]。
For example, Tang and Wang [49] propose a Convolutional Sequence Model (Caser) to learn sequential patterns using both horizontal and vertical convolutional filters.
例えば、TangとWang[49]は、水平と垂直の畳み込みフィルタを使用して連続パターンを学習する畳み込みシーケンスモデル(Caser)を提案している。(Caserは他のsequential recommenderの論文のベースラインとして出てきたかも:thinking:)
Chen et al.[3] and Huang et al.[19] employ Memory Network to improve sequential recommendation.
Chenら[3]とHuangら[19]は、逐次推薦を改善するためにMemory Network(??)を採用している。
STAMP captures both users’ general interests and current interests using an MLP network with attention [33].
STAMPは、ユーザの一般的な(generalな)興味と現在の興味の両方を、attention機構を含んだMLPネットワークを使って捉えている[33]。

## 2.3. Attention Mechanism

Attention mechanism has shown promising potential in modeling sequential data, e.g., machine translation [2, 52] and text classification [? ].
アテンション・メカニズムは、機械翻訳[2, 52]やテキスト分類[？]など、**sequentialデータのモデリングにおいて有望な可能性**を示している。
Recently, some works try to employ the attention mechanism to improve recommendation performances and interpretability [28, 33].
最近では、推薦のパフォーマンスと解釈可能性を向上させるために、アテンション・メカニズムを採用しようとする研究もある[28, 33]。
For example, Li et al.[28] incorporate an attention mechanism into GRU to capture both the user’s sequential behavior and main purpose in session-based recommendation.
例えば、Liら[28]は、セッションベースの推薦において、ユーザの逐次的行動と主目的(?)の両方を捕捉するために、GRUにアテンションメカニズムを組み込んでいる。

The works mentioned above basically treat attention mechanism as an additional component to the original models.
上述した作品は、基本的に注意メカニズムをオリジナルモデルのadditional componentとして扱っている。
In contrast, Transformer [52] and BERT [6] are built solely on multi-head self-attention and achieve state-of-the-art results on text sequence modeling.
対照的に、**Transformer[52]とBERT[6]は、multi-head self-attentionのみに基づいて構築されており**、テキストシーケンスのモデリングにおいて最先端の結果を達成している。
Recently, there is a rising enthusiasm for applying purely attention-based neural networks to model sequential data for their effectiveness and efficiency [30, 32, 38, 46? ].
最近、その有効性と効率性から、純粋にattenitonに基づくニューラルネットワークをsequentialデータのモデルに適用しようという熱意が高まっている[30, 32, 38, 46?］
For sequential recommendation, Kang and McAuley [22] introduce a two-layer Transformer decoder (i.e., Transformer language model) called SASRec to capture user’s sequential behaviors and achieve state-of-the-art results on several public datasets.
逐次推薦のために、KangとMcAuley [22]は、**SASRec**と呼ばれる2層のTransformerデコーダ(すなわち、Transformer言語モデル)を導入し、ユーザの逐次行動を捕捉し、いくつかの公開データセットで最先端の結果を達成している。(SASRecはself-attentionを使ったsequential recommenderで有名なやつ!:thinking:)
SASRec is closely related to our work.
SASRecは我々の仕事と密接な関係がある。
However, it is still a unidirectional model using a casual attention mask.
とはいえ、casual attention mask(=シンプルにnext-itemをmaskして、next-item-prediction問題を学習させるやつ??:thinking:)を使ったuni-directionalな(一方向的な)モデルであることに変わりはない。
While we use a bidirectional model to encode users’ behavior sequences with the help of Cloze task.
一方、我々は**Clozeタスク**の助けを借りて、**ユーザの行動シーケンスを符号化するために双方向モデルを使用**しています。

# 3. BERT4REC BERT4REC

Before going into the details, we first introduce the research problem, the basic concepts, and the notations in this paper.
詳細に入る前に、まず本稿における研究課題、基本概念、表記法を紹介する。

## 3.1. Problem Statement

In sequential recommendation, let $U=\{u_1,u_2, \cdots, u_{|U|}\}$ denote a set of users, $V=\{v_1,v_2, \cdots, v_{|V|}\}$ be a set of items, and list $S_u=[v^{(u)}_1, \cdots, v^{(u)}_{t}, \cdots, v^{(u)}_{n_u}]$ denote the interaction sequence in chronological order for user u ∈ U, where v (u) t ∈ V is the item that u has interacted with at time step2 t and nu is the the length of interaction sequence for user u.
逐次推薦において、$U=\{u_1,u_2, \cdots, u_{|U|}\}$ をユーザの集合、$V=\{v_1,v_2, \cdots, v_{|V|}\}$ はアイテムの集合、リスト $S_u=[v^{(u)}_1, \cdots, v^{(u)}_{t}, \cdots, v^{(u)}_{n_u}]$ はユーザu∈Uの時系列での対話シーケンスを示す。
ここで、$v^{(u)}_{t} \in V$ は、u が時間ステップ $t$ で相互作用したアイテムであり、nu は、ユーザーu の相互作用シーケンスの長さである。
(2Here, following [22, 40], we use the relative time index instead of absolute time index for numbering interaction records.)
(ここでは、[22, 40]に従い、交流記録の番号付けに絶対時間インデックスの代わりに相対時間インデックスを使用する。)
Given the interaction history Su , sequential recommendation aims to predict the item that user u will interact with at time step nu + 1.
インタラクション履歴 $S_u$ が与えられると、逐次推薦は時間ステップ $n_u + 1$ でユーザ $u$がインタラクションするアイテムを予測することを目的とする。
It can be formalized as modeling the probability over all possible items for user u at time step nu+1:
これは、**時間ステップ $n_u +1$ におけるユーザ $u$ のすべてのinteraction可能なitemにわたる確率**をモデル化するものとして定式化することができる:(要は条件付き確率。これをどうにかモデル化しますよ、という話か。)

$$
p(v^{(u)}_{n_u + 1} = v |\mathcal{S}_{u})
$$

## 3.2. Model Architecture モデル・アーキテクチャ

Here, we introduce a new sequential recommendation model called BERT4Rec, which adopts Bidirectional Encoder Representations from Transformers to a new task, sequential Recommendation.
ここでは、BERT4Recと呼ばれる新しい逐次推薦モデルを紹介する。BERT4Recは、新しいタスク(BERTにとって!)である逐次推薦に、トランスフォーマからの双方向エンコーダ表現を採用したものである。
It is built upon the popular self-attention layer, “Transformer layer”.
これは、人気の高いself-attentionレイヤー「トランスフォーマー・レイヤー」の上に構築されている。

![figure 1 b]()

As illustrated in Figure 1b, BERT4Rec is stacked by L bidirectional Transformer layers.
図1bに示すように、BERT4RecはL個の双方向トランスフォーマー層によって積層されている。
At each layer, it iteratively revises the representation of every position by exchanging information across all positions at the previous layer in parallel with the Transformer layer.
各レイヤーで、トランスフォーマーレイヤーと並行して、前のレイヤーのすべてのポジションの情報を交換することによって(??)、すべてのポジションの表現を繰り返し修正する。
Instead of learning to pass relevant information forward step by step as RNN based methods did in Figure 1d, self-attention mechanism endows BERT4Rec with the capability to directly capture the dependencies in any distances.
図1dのRNNベースの手法のように、関連する情報を段階的に前方に渡すように学習する代わりに、self-attentionメカニズムは、BERT4Recに、あらゆる距離の依存関係を直接捕捉する能力を与えている。
This mechanism results in a global receptive field, while CNN based methods like Caser usually have a limited receptive field.
このメカニズムにより、グローバルなreceptive fieldが得られるが、CaserのようなCNNベースの手法は通常、receptive fieldが限定される。(長期記憶と短期記憶的な話だろうか...??:thinking:)
In addition, in contrast to RNN based methods, self-attention is straightforward to parallelize.
また、RNNベースの手法とは対照的に、**自己アテンションは並列化が容易**である。(Transformerの論文に書いてあったかも)

Comparing Figure 1b, 1c, and 1d, the most noticeable difference is that SASRec and RNN based methods are all left-to-right unidirectional architecture, while our BERT4Rec uses bidirectional self-attention to model users’ behavior sequences.
図1b、図1c、図1dを比較すると、最も顕著な違いは、SASRecとRNNベースの手法はすべて左から右への一方向アーキテクチャであるのに対し、我々のBERT4Recはユーザの行動シーケンスをモデル化するために**双方向の自己注意を使用**していることである。
In this way, our proposed model can obtain more powerful representations of users’ behavior sequences to improve recommendation performances.
このようにして、我々の提案するモデルは、推薦パフォーマンスを向上させるために、ユーザの行動シーケンスのより強力な表現を得ることができる。

## 3.3. Transformer Layer トランスフォーマーレイヤー

As illustrated in Figure 1b, given an input sequence of length t, we iteratively compute hidden representations h l i at each layer l for each position i simultaneously by applying the Transformer layer from [52].
図1bに示すように、長さ $t$ の入力シーケンスが与えられると、[52]のTransformer層を適用することで、各位置 $i$ に対して各層 $l$ で隠れ表現 $\mathbf{h}^{l}_{i}$ を同時に反復計算する。
Here, we stack $\mathbf{h}^{l}_{i} \in \mathbb{R}^{d}$ together into matrix Hl ∈R t×d since we compute attention function on all positions simultaneously in practice.
ここで、$\mathbf{h}^{l}_{i} \in \mathbb{R}^{d}$ を行列 $\mathbf{H}^{l} \in \mathbb{R}^{t \times d}$ に積み重ねるが、これは実際にはすべての位置で同時にattention関数を計算するためである。
As shown in Figure 1a, the Transformer layer Trm contains two sub-layers, a Multi-Head Self-Attention sub-layer and a Position-wise Feed-Forward Network.
図1aに示すように、Trensformer層 Trm は2つのサブレイヤー、multi-head self-attention サブレイヤーと position-wise フィードフォワードネットワークを含む。

### 3.3.1. Multi-Head Self-Attention.マルチヘッドの自己アテンション。

Attention mechanisms have become an integral part of sequence modeling in a variety of tasks, allowing capturing the dependencies between representation pairs without regard to their distance in the sequences.
注意メカニズムは、**様々なタスクにおけるシーケンスモデリングの不可欠な要素となっており、シーケンス内の距離に関係なく、表現ペア間の依存関係を捉えることができる**。
Previous work has shown that it is beneficial to jointly attend to information from different representation subspaces at different positions [6, 29, 52].
これまでの研究で、異なる位置にある異なる表現部分空間からの情報に共同で注意を向けることが有益であることが示されている[6, 29, 52]。(これがmulti-head attetionを採用する理由なのか...!:thinking:)
Thus, we here adopt the multi-head self-attention instead of performing a single attention function.
したがって、ここでは単一の注意機能を実行する代わりに、multi-head self-attentionを採用する。
Specifically, multi-head attention first linearly projects Hl into h subspaces, with different, learnable linear projections, and then apply h attention function in parallel to produce the output representations which are concatenated and once again projected:
具体的には、マルチヘッド注意は、まず $\mathbf{H}^{l}$ を異なる学習可能な線形投影で $h$ 個の部分空間に線形投影し、次に $h$ 個のself-attetion関数を並列に適用して出力表現を生成し、それを連結してもう一度投影する(これはTransformerの論文でやったやつ:thinking:):

$$
MH(\mathbf{H}^l) = [head_1;head_2; \cdots, ;head_{h}] \mathbf{W}^O
\\
head_i = Attention(\mathbf{H}^l \mathbf{W}^Q_{i}, \mathbf{H}^l \mathbf{W}^K_{i}, \mathbf{H}^l \mathbf{W}^V_{i})
\tag{1}
$$

where the projections matrices for each head $\mathbf{W}^Q_i \in \mathbb{R}^{d×d/h}$, $\mathbf{W}^K_i \in \mathbb{R}^{d×d/h}$, $\mathbf{W}^V_i \in \mathbb{R}^{d×d/h}$, and $\mathbf{W}^O_i \in \mathbb{R}^{d×d}$ are learnable parameters.
ここで、各ヘッドの投影行列 $\mathbf{W}^Q_i \in \mathbb{R}^{d×d/h}$, $\mathbf{W}^K_i \in \mathbb{R}^{d×d/h}$, $\mathbf{W}^V_i \in \mathbb{R}^{d×d/h}$, and $\mathbf{W}^O_i \in \mathbb{R}^{d×d}$ は学習可能なパラメータである。
Here, we omit the layer subscript l for the sake of simplicity.
ここでは簡略化のため、レイヤーの添え字 $l$ は省略する。
In fact, these projection parameters are not shared across the layers.
実際、これらの投影パラメータはレイヤー間で共有されることはない。(各レイヤーが異なるパラメータを持つ。)
Here, the Attention function is Scaled Dot-Product Attention:
ここで、アテンション関数はScaled Dot-Product Attentionである：

$$
Attention(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = softmax(\frac{QK^T}{\sqrt{d/h}}) V
\tag{2}
$$

where query Q, key K, and value V are projected from the same matrix Hl with different learned projection matrices as in Equation 1.
ここで、クエリQ、キーK、値Vは、式1のように異なる学習された射影行列で、同じ行列 $H^l$ から射影される。
The temperature $\sqrt{d/h}$ is introduced to produce a softer attention distribution for avoiding extremely small gradients [16, 52].
温度 $\sqrt{d/h}$ は、極端に小さな勾配を避けるために、よりソフトなattention分布を作り出すために導入されている[16, 52]。(うんうん、Transformer論文でやったやつ。)

### 3.3.2. Position-wise Feed-Forward Network. ポジションごとのフィードフォワードネットワーク。

As described above, the self-attention sub-layer is mainly based on linear projections.
上述したように、self-attentionサブレイヤーは主に**線形投影に基づいている**。(このパートだけだと線形モデル...!)
To endow the model with nonlinearity and interactions between different dimensions, we apply a Position-wise Feed-Forward Network to the outputs of the self-attention sub-layer, separately and identically at each position.
**モデルに非線形性と異なる次元間の相互作用を持たせるために**、自己注意サブレイヤーの出力に、各位置で別々に、かつ同一に、position-wise フィード・フォワード・ネットワークを適用する。
It consists of two affine transformations with a Gaussian Error Linear Unit (GELU) activation in between:
これは、2つのアフィン変換と、その間のGELU(Gaussian Error Linear Unit)活性化からなる：

$$
PFFN(\mathbf{H}^l) = [FFN(\mathbf{h}^l_1)^T; \cdots; FFN(\mathbf{h}^l_t)^T]^T
\\
FFN(\mathbf{x}) = GELU(\mathbf{x}\mathbf{W}^1 + \mathbf{b}^1)\mathbf{W}^2 + \mathbf{b}^2
\\
GELU(x) = x \Phi(x)
\tag{3}
$$

where Φ(x) is the cumulative distribution function of the standard gaussian distribution, W (1) ∈ R d×4d , W (2) ∈ R 4d×d , b (1) ∈ R 4d and b (2) ∈ R d are learnable parameters and shared across all positions.
ここで、$\Phi(x)$ は標準ガウス分布の累積分布関数(=じゃあ0 ~ 1になるやつか!たぶんsigmoidと近い形なのかな!)であり、$W^(1) \in \mathbb{R}^{d \times 4d}$, $W^(2) \in \mathbb{R}^{4d×\times d}$, $\mathbf{b}^(1) \in \mathbb{R}^{4d}$ および $\mathbf{b}^(2) \in \mathbb{R}^{d}$ は学習可能なパラメータであり、すべてのポジション(=**sequence内のposition $1 ~ t$!!**)で共有される。
We omit the layer subscript l for convenience.
便宜上、レイヤーの添え字 $l$ は省略する。(=Transformerブロックの数だっけ?? 確か推薦タスクだと2個くらいでイイっていう...!)
In fact, these parameters are different from layer to layer.
実際、これらのパラメータはレイヤーごとに異なる。
In this work, following OpenAI GPT [38] and BERT [6], we use a smoother GELU [13] activation rather than the standard ReLu activation.
この作品では、OpenAI GPT [38] と BERT [6] に従って、標準的な ReLu 活性化ではなく、より滑らかな GELU [13] 活性化を使用しています。

### 3.3.3. Stacking Transformer Layer. スタッキング・トランスフォーマー・レイヤー。

![fig1a]()

As elaborated above, we can easily capture item-item interactions across the entire user behavior sequence using self-attention mechanism.
上述したように、自己アテンションメカニズムを使えば、ユーザの行動シーケンス全体にわたって、itemとitemの相互作用を簡単に捉えることができる。
Nevertheless, it is usually beneficial to learn more complex item transition patterns by stacking the self-attention layers.
とはいえ、通常、self-attentionのレイヤーを重ねることで、より複雑なitem transition(遷移)パターンを学習することは有益である。
However, the network becomes more difficult to train as it goes deeper.
しかし、ネットワークは深くなるにつれて訓練が難しくなる。
Therefore, we employ a residual connection [9] around each of the two sublayers as in Figure 1a, followed by layer normalization [1].
そのため、図1aのように、2つのサブレイヤーそれぞれの周囲に残差接続(residual connection)[9]を採用し、続いてレイヤー正規化[1]を行う。(resnet的なやつ??)
Moreover, we also apply dropout [47] to the output of each sub-layer, before it is normalized.
さらに、正規化する前に、各サブレイヤーの出力にドロップアウト[47]を適用する。
That is, the output of each sub-layer is LN(x + Dropout(sublayer(x))), where sublayer(·) is the function implemented by the sub-layer itself, LN is the layer normalization function defined in [1].
つまり、各サブレイヤの出力は $LN(x + Dropout(sublayer(x)))$ となる、
ここで、$sublayer(-)$ はサブレイヤ自身によって実装された関数であり、$LN$ は [1] で定義されたレイヤ正規化関数である。
We use LN to normalize the inputs over all the hidden units in the same layer for stabilizing and accelerating the network training.
$LN$ を使用して、同じレイヤーにあるすべての隠れユニットの入力を正規化し、ネットワーク学習を安定化・高速化する。(なるほど?レイヤー正規化はそういう効果なのか...!:thinking:)

In summary, BERT4Rec refines the hidden representations of each layer as follows:
要約すると、BERT4Rec は各層の隠れ表現を以下のように洗練する:
($l$ は各Transformerブロックの添字)

$$
\mathbf{H}^{l} = Trm(\mathbf{H}^{l-1}), \forall i \in [1, \cdots, L]
\tag{4}
$$

(↑前のTransformerブロックの出力が、次のTransformerブロックの入力になる)

$$
Trm(\mathbf{H}^{l-1}) = LN(A^{l-1} + Dropout(PFFN(A^{l-1})))
\tag{5}
$$

(↑Residual connectionとPFFN)

$$
A^{l-1} = LN(\mathbf{H}^{l} + Dropout(MH(\mathbf{H}^{l-1})))
\tag{6}
$$

(↑Residual connectionとMulti-head attention)

## 3.4. Embedding Layer エンベッディングレイヤー

As elaborated above, without any recurrence or convolution module, the Transformer layer Trm is not aware of the order of the input sequence.
上で詳しく説明したように、再帰や畳み込みモジュールを持たないトランスフォーマー層 Trm は、入力シーケンスの順序を意識しない。(あ、だからpositional encodingが必要、みたいなやつだっけ!!)
In order to make use of the sequential information of the input, we inject Positional Embeddings into the input item embeddings at the bottoms of the Transformer layer stacks.
入力の連続情報を利用するために、Transformerレイヤーのスタックの一番下にある入力itemの埋め込みに位置埋め込み(positional embedding)を注入する。
For a given item vi , its input representation h 0 i is constructed by summing the corresponding item and positional embedding.
与えられたitem $v_i$に対して、その入力表現 $\mathbf{h}^{0}_{i}$ は、対応するitem埋め込みと位置埋め込みを合計することによって構築される。

$$
\mathbf{h}^{0}_{i} = \mathbf{v}_{i} + \mathbf{p}_{i}
\tag{}
$$

where vi ∈E is the d−dimensional embedding for item vi , pi ∈P is the d−dimensional positional embedding for position index i.
ここで、vi∈Eは項目viのd次元埋め込み、pi∈Pは位置インデックスiのd次元位置埋め込みである。
In this work, we use the learnable positional embeddings instead of the fixed sinusoid embeddings in [52] for better performances.
本研究では、より良い性能を得るために、[52]の固定正弦波埋め込みに代えて、学習可能な位置埋め込みを用いる。
The positional embedding matrix P ∈ R N ×d allows our model to identify which portion of the input it is dealing with.
位置埋め込み行列 $\mathbf{P} \in \mathbb{R}^{N \times d}$ は、我々のモデルが入力のどの部分を扱っているかを識別することを可能にする。
However, it also imposes a restriction on the maximum sentence length N that our model can handle.
しかし、これはまた、我々のモデルが扱える最大の文の長さ $H$ に制限を課すものでもある。
Thus, we need to truncate the the input sequence [v1, . . . ,vt ] to the last N items [v u t−N +1 , . . . ,vt ] if t > N.
したがって、入力列[v1, ... ,vt ]は、t > Nの場合、最後のN個の項目[v u t-N +1 , ... ,vt ]まで切り捨てる必要がある。(古い要素を切り捨てるって話)

## 3.5. Output Layer 出力レイヤー

![fig1 b]()

After L layers that hierarchically exchange information across all positions in the previous layer, we get the final output HL for all items of the input sequence.
前の層のすべての位置の情報を階層的に交換するL個のTransformerブロックの後、入力シーケンスのすべてのitemに対する最終的な出力 $\mathbf{H}^{L}$ が得られる。
Assuming that we mask the item vt at time step t, we then predict the masked items vt base on h L t as shown in Figure 1b.
時間ステップ $t$ でアイテム $v_{t}$ をマスクすると仮定すると、図1bに示すように、$\mathbf{h}^L_t$ に基づいてマスクされたアイテム $v_t$ を予測する。
Specifically, we apply a two-layer feed-forward network with GELU activation in between to produce an output distribution over target items:
具体的には、GELU活性化を挟んだ2層のフィードフォワードネットワークを適用し、ターゲットitemsに対する出力分布を生成する:

$$
P(v) = softmax(GELU(\mathbf{h}^L_{t} W^P + \mathbf{b}^P) \mathbf{E}^T + \mathbf{b}^O)
\tag{7}
$$

where W P is the learnable projection matrix, b P , and b O are bias terms, E ∈ R |V |×d is the embedding matrix for the item set V.
ここで、$W^P$ は学習可能な射影行列、$b^P$ 、$b^O$ はバイアス項、$\mathbf{E} \in \mathbb{R}^{|V|\times d$ はitem集合Vの埋め込み行列である。
We use the shared item embedding matrix in the input and output layer for alleviating overfitting and reducing model size.
我々は、オーバーフィッティングを緩和し、モデルサイズを小さくするために、**入力層と出力層で共有item埋め込み行列を使用する**。

## 3.6. Model Learning モデル学習

### Training.トレーニング

Conventional unidirectional sequential recommendation models usually train the model by predicting the next item for each position in the input sequence as illustrated in Figure 1c and 1d.
従来の一方向順序推薦モデルは、図1cと1dに示すように、入力シーケンスの各位置に対して次のアイテムを予測することでモデルを学習するのが一般的である。
Specifically, the target of the input sequence [v1, . . . ,vt ] is a shifted version [v2, . . . ,v_t+1].
具体的には、入力シーケンス[v1, ... ,vt]のターゲットは、シフトされたバージョン[v2, ... ,v_t+1]である。
However, as shown in Figure 1b, jointly conditioning on both left and right context in a bidirectional model would cause the final output representation of each item to contain the information of the target item.
しかし、図1bに示すように、双方向モデルで左右両方の文脈に条件付けを行うと、各itemの最終的な出力表現に対象itemの情報が含まれることになる。
This makes predicting the future become trivial and the network would not learn anything useful.
これでは、未来を予測することは些細なことになり、ネットワークは何も有益なことを学べない。

A simple solution for this issue is to create t − 1 samples (subsequences with next items like ([v1], v2) and ([v1,v2], v3)) from the original length t behavior sequence
and then encode each histrical subsequence with the bidirectional model to predict the target item.
この問題に対する簡単な解決策は、元の長さtの行動シーケンスからt-1個のサンプル(= ([v1], v2)や([v1,v2], v3)のような**next-itemを持つ部分シーケンス**)を作成し、次に各histricalシーケンスを双方向モデルで符号化してターゲットitemを予測することである。(後半が良くわかってない:thinking:)
However, this approach is very time and resources consuming since we need to create a new sample for each position in the sequence and predict them separately.
しかしこの方法では、配列の各位置ごとに新しいサンプルを作成し、それらを個別に予測する必要があるため、非常に時間とリソースを消費する。

In order to efficiently train our proposed model, we apply a new objective: Cloze task [50] (also known as “Masked Language Model” in [6]) to sequential recommendation.
提案モデルを効率的に学習するために、我々は新しい目的を適用する：
Clozeタスク[50]（[6]では "**Masked Language Model**"とも呼ばれる）を逐次推薦に適用する。
It is a test consisting of a portion of language with some words removed, where the participant is asked to fill the missing words.
これは、いくつかの単語が削除された言語の一部からなるテストであり、参加者は欠けている単語を埋めるように求められる。
In our case, for each training step, we randomly mask ρ proportion of all items in the input sequence (i.e., replace with special token “[mask]”), and then predict the original ids of the masked items based solely on its left and right context.
私たちの場合、各トレーニングステップにおいて、入力シーケンスの全アイテムのうちρの割合をランダムにマスクし（つまり、特別なトークン"[mask]"で置き換える）、次に、マスクされたアイテムの元のIDを、その左右の文脈のみに基づいて予測する。
For example:
例えば、こうだ：

$$
Input : [v_1, v_2, v_3, v_4, v_5] \rightarrow^{randomly_mask} [v_1, [mask]_1, v_3, [mask]_2, v_5]
\\
Labels:[mask]_1 = v_2, [mask]_2 = v_4
$$

The final hidden vectors corresponding to “[mask]” are fed into an output softmax over the item set, as in conventional sequential recommendation.
“[mask]”に対応する最終的な hidden vectors は、従来の逐次推薦と同様に、アイテムセットに対する出力ソフトマックスに供給される。
Eventually, we define the loss for each masked input S ′ u as the negative log-likelihood of the masked targets:
最終的に、各マスク入力 $\mathcal{S}'_{u}$ に対する損失を、マスクされたターゲットの負の対数尤度として定義する:

$$
\mathcal{L}
= \frac{1}{|\mathcal{S}^m_u|}
\sum_{v_m \in \mathcal{S}^m_u} - log P(v_m = v^{*}_{m}|\mathcal{S}'_{u})
\tag{8}
$$

where S ′ u is the masked version for user behavior history Su , S m u is the random masked items in it, v ∗ m is the true item for the masked item vm, and the probability P(·) is defined in Equation 7.
ここで、$\mathcal{S}'_{u}$ はユーザ行動履歴Suのマスクバージョンであり、$\mathcal{S}^{m}_{u}$ はその中のランダムなマスクされた項目であり、$v^{*}_{m}$ はマスクされたitem vmの真のitemであり、確率P（-）は式(7)で定義される。

An additional advantage for Cloze task is that it can generate more samples to train the model.
さらに、**Clozeタスクの利点は、モデルを訓練するためのサンプルをより多く生成できること**である。(ランダムにmaskするから??)
Assuming a sequence of length n, conventional sequential predictions in Figure 1c and 1d produce n unique samples for training, while BERT4Rec can obtain nCk samples (if we randomly mask k items) in multiple epochs.
長さ n のシーケンスを想定すると、図 1c および 1d の従来の逐次予測では、訓練用に n 個のユニークなサンプルが生成されるのに対して、BERT4Rec では、複数回のエポックで nCk 個のサンプル（ランダムに k 個のアイテムをマスクする場合）を得ることができる。(ふむふむ...!)
It allows us to train a more powerful bidirectional representation model.
これにより、より強力な双方向表現モデルを訓練することができる。

### Test.テストだ。

As described above, we create a mismatch between the training and the final sequential recommendation task since the Cloze objective is to predict the current masked items while sequential recommendation aims to predict the future.
上述したように、Clozeの目的は現在のマスクitemを予測することであるのに対し、逐次推薦の目的は将来の予測であるため、**訓練と最終的な逐次推薦タスクの間にミスマッチが生じる**。(うんうんそうだよね。代理学習問題的な??)
To address this, we append the special token “[mask]” to the end of user’s behavior sequence, and then predict the next item based on the final hidden representation of this token.
これを解決するために、**ユーザの行動シーケンスの最後に特別なトークン「[mask]」を付加**し、このトークンの最終的な隠された表現に基づいて次のアイテムを予測する。(clsトークンじゃないんだ...!!:thinking:)
To better match the sequential recommendation task (i.e., predict the last item), we also produce samples that only mask the last item in the input sequences during training.
逐次的な推薦タスク（すなわち、最後のアイテムを予測する）にうまくマッチさせるため、**学習中に入力シーケンスの最後のアイテムだけをマスクするサンプルも作成する**。(このサンプルだけmasked item prediction = next item predictionになるのか...!)
It works like fine-tuning for sequential recommendation and can further improve the recommendation performances.
これは逐次推薦のファインチューニングのように機能し、推薦性能をさらに向上させることができる。

## 3.7. Discussion

Here, we discuss the relation of our model with previous related work.
ここでは、我々のモデルとこれまでの関連研究との関係について述べる。

### SASRec.

Obviously, SASRec is a left-to-right unidirectional version of our BERT4Rec with single head attention and causal attention mask.
明らかに、SASRecは、私たちのBERT4Recの左から右への一方向バージョンであり、単一頭部注意と因果的注意マスクを備えている。
Different architectures lead to different training methods.
アーキテクチャが異なれば、トレーニング方法も異なる。
SASRec predicts the next item for each position in a sequence, while BERT4Rec predicts the masked items in the sequence using Cloze objective.
SASRecは配列の各位置に対して次の項目を予測し、BERT4RecはCloze目的語を用いて配列中のマスクされた項目を予測する。

### CBOW & SG.

Another very similar work is Continuous Bag-ofWords (CBOW) and Skip-Gram (SG) [35].
もう1つの非常に類似した研究は、CBOW(Continuous Bag-of-Words)とSG(Skip-Gram)[35]である。
CBOW predicts a target word using the average of all the word vectors in its context (both left and right).
CBOWは、その文脈（左右両方）のすべての単語ベクトルの平均を使ってターゲット単語を予測する。
It can be seen as a simplified case of BERT4Rec, if we use one self-attention layer in BERT4Rec with uniform attention weights on items, unshare item embeddings, remove the positional embedding, and only mask the central item.
BERT4Recの自己注意層を1層とし、項目に対する注意の重みを一律とし、項目の埋め込みを共有せず、位置の埋め込みを除去し、中心項目のみをマスクすると、BERT4Recの単純化されたケースとして見ることができる。
Similar to CBOW, SG can also be seen as a simplified case of BERT4Rec following similar reduction operations (mask all items except only one).
CBOWと同様に、SGもまた、同様の削減操作（1つだけを除くすべての項目をマスクする）に従ったBERT4Recの簡略化されたケースと見なすことができる。
From this point of view, Cloze can be seen as a general form for the objective of CBOW and SG.
この観点から、 Cloze はCBOWとSGの目的を達成するための一般的な形式とみなすことができる。
Besides, CBOW uses a simple aggregator to model word sequences since its goal is to learn good word representations, not sentence representations.
その上、CBOWは単純なアグリゲータを使って単語列をモデル化する。なぜならば、CBOWの目標は良い単語表現を学習することであって、文の表現を学習することではないからだ。
On the contrary, we seek to learn a powerful behavior sequence representation model (deep selfattention network in this work) for making recommendations.
それとは逆に、我々は推薦を行うための強力な行動シーケンス表現モデル（この作品では深層自己注意ネットワーク）を学習することを目指している。

### BERT.

Although our BERT4Rec is inspired by the BERT in NLP, it still has several differences from BERT:
我々のBERT4Recは、自然言語処理におけるBERTにインスパイアされているが、BERTとはいくつかの違いがある：
a) The most critical difference is that BERT4Rec is an end-to-end model for sequential recommendation, while BERT is a pre-training model for sentence representation.

a) 最も決定的な違いは、BERT4Recが逐次推薦のためのエンドツーエンドモデルであるのに対し、BERTは文表現のための事前学習モデルであることである。
BERT leverages large-scale task-independent corpora to pre-train the sentence representation model for various text sequence tasks since these tasks share the same background knowledge about the language.
BERT は、**タスクに依存しない大規模なコーパスを活用**して、さまざまなテキストシーケンスタスクの文表現モデルを事前学習します。
However, this assumption does not hold in the recommendation tasks.
しかし、推薦タスクではこの仮定は成り立たない。
Thus we train BERT4Rec end-to-end for different sequential recommendation datasets.
このように、BERT4Rec を様々な逐次推薦データセットに対してエンドツーエンドで訓練する。

b) Different from BERT, we remove the next sentence loss and segment embeddings since BERT4Rec models a user’s historical behaviors as only one sequence in sequential recommendation task.
b) BERT4Recは、逐次推薦タスクにおいて、ユーザの過去の行動を1つのシーケンスとしてのみモデル化するため、BERTとは異なり、次文損失(next-sentenceの学習タスクだっけ?)とセグメント埋め込み(なんだっけ...??)を削除する。

# 4. Experiments 実験

## 4.1. Datasets データセット

We evaluate the proposed model on four real-world representative datasets which vary significantly in domains and sparsity.
提案モデルを、ドメインとスパース性が大きく異なる4つの実世界の代表的なデータセットで評価する。

- Amazon Beauty3 : This is a series of product review datasets crawled from Amazon.com by McAuley et al.[34]. Amazon Beauty3: これはMcAuleyら[34]によってAmazon.comからクロールされた一連の製品レビューデータセットである。They split the data into separate datasets according to the toplevel product categories on Amazon. アマゾンの商品カテゴリーごとにデータを分割した. In this work, we adopt the “Beauty” category. この作品では「ビューティー」カテゴリーを採用する。
- Steam4 : This is a dataset collected from Steam, a large online video game distribution platform, by Kang and McAuley [22]Steam4: これは、KangとMcAuley[22]によって、大規模なオンライン・ビデオゲーム配信プラットフォームであるSteamから収集されたデータセットである。
- MovieLens [8]: This is a popular benchmark dataset for evaluating recommendation algorithms.MovieLens [8]：これは推薦アルゴリズムを評価するための一般的なベンチマークデータセットである。In this work, we adopt two well-established versions, MovieLens 1m (ML1m) 5 and MovieLens 20m (ML-20m) 6 . この作品では、MovieLens 1m (ML1m) 5 と MovieLens 20m (ML-20m) 6 の 2 つの確立されたバージョンを採用している。

For dataset preprocessing, we follow the common practice in [22, 40, 49].
データセットの前処理については、[22, 40, 49]の一般的なやり方に従う。
For all datasets, we convert all numeric ratings or the presence of a review to implicit feedback of 1 (i.e., the user interacted with the item).
すべてのデータセットについて、すべての数値評価またはレビューの存在を、**暗黙のフィードバック1（すなわち、ユーザーがアイテムと相互作用した）に変換する**。(あ、implicit feedbackと見做しているのか...!)
After that, we group the interaction records by users and build the interaction sequence for each user by sorting these interaction records according to the timestamps.
その後、ユーザごとに対話記録をグループ化し、タイムスタンプに従ってこれらの対話記録をソートすることで、各ユーザの対話シーケンスを構築する。
To ensure the quality of the dataset, following the common practice [12, 22, 40, 49], we keep users with at least five feedbacks.
データセットの質を保証するために、一般的な慣行[12, 22, 40, 49]に従って、**少なくとも5つのフィードバックを持つユーザを保持する**。
The statistics of the processed datasets are summarized in Table 1.
処理したデータセットの統計を表1にまとめた。

![table1]()

## 4.2. Task Settings & Evaluation Metrics タスク設定と評価指標

To evaluate the sequential recommendation models, we adopted the leave-one-out evaluation (i.e., next item recommendation) task, which has been widely used in [12, 22, 49].
逐次推薦モデルを評価するために、[12, 22, 49]で広く用いられているleave-one-out 評価(i.e., next item recommendation)タスクを採用した。
For each user, we hold out the last item of the behavior sequence as the test data, treat the item just before the last as the validation set, and utilize the remaining items for training.
各ユーザーについて、行動シーケンスの最後のitemをテストデータとして取り出し、最後のitemの直前のitemをvalidセットとして扱い、残りのitemを学習に利用する。
For easy and fair evaluation, we follow the common strategy in [12, 22, 49], pairing each ground truth item in the test set with 100 randomly sampled negative items that the user has not interacted with.
簡単で公平な評価のために、我々は[12, 22, 49]の一般的な戦略に従い、テストセット内の各ground-truthアイテムと、ユーザが相互作用していないランダムにサンプリングされた100個のnegativeアイテムをペアリングする。
To make the sampling reliable and representative [19], these 100 negative items are sampled according to their popularity.
サンプリングの信頼性と代表性を高めるために[19]、これらの100のネガティブ項目は、その人気度合いに従ってサンプリングされる。
Hence, the task becomes to rank these negative items with the ground truth item for each user.
したがって、タスクは、各ユーザのためのground-truth itemとこれらの否定的なitemsをランク付けすることになります。

### Evaluation Metrics. 評価指標。

To evaluate the ranking list of all the models, we employ a variety of evaluation metrics, including Hit Ratio (HR), Normalized Discounted Cumulative Gain (NDCG), and Mean Reciprocal Rank (MRR).
すべてのモデルのランキングリストを評価するために、ヒット率（HR）、正規化割引累積利得（NDCG）、平均逆順位（MRR）など、さまざまな評価指標を採用する。
Considering we only have one ground truth item for each user, HR@k is equivalent to Recall@k and proportional to Precision@k; MRR is equivalent to Mean Average Precision (MAP).
HR@kはRecall@kと等価であり、Precision@kに比例し、MRRはMean Average Precision (MAP)と等価である。
In this work, we report HR and NDCG with k = 1, 5, 10.
本研究では、k = 1, 5, 10のHRとNDCGについて報告する。
For all these metrics, the higher the value, the better the performance.
これらの指標はすべて、数値が高いほどパフォーマンスが高いことを意味する。

## 4.3. Baselines & Implementation Details ベースラインと実施内容

To verify the effectiveness of our method, we compare it with the following representative baselines:
本手法の有効性を検証するため、以下の代表的なベースラインと比較した：

- POP: It is the simplest baseline that ranks items according to their popularity judged by the number of interactions.POP: 最も単純なベースラインで、インタラクションの数によって判断される人気度によってアイテムをランク付けする。
- BPR-MF [39]: It optimizes the matrix factorization with implicit feedback using a pairwise ranking loss.BPR-MF [39]：BPR-MF[39]：ペアワイズ・ランキング・ロスを用いた暗黙のフィードバックにより、行列分解を最適化する。
- NCF [12]: It models userâĂŞitem interactions with a MLP instead of the inner product in matrix factorization.NCF [12]: これは、行列分解における内積の代わりにMLPを用いて、ユーザとアイテムの相互作用をモデル化する。
- FPMC [40]: It captures users’ general taste as well as their sequential behaviors by combing MF with first-order MCs. FPMC [40]： MFと一次MCを組み合わせることで、ユーザーの一般的な嗜好と逐次的な行動を捉える。
- GRU4Rec [15]: It uses GRU with ranking based loss to model user sequences for session based recommendation. GRU4Rec [15]：GRU4Rec[15]は、セッション・ベースの推薦のために、GRUとランキング・ベースの損失を用いてユーザ・シーケンスをモデル化する。
- GRU4Rec+ [14]: It is an improved version of GRU4Rec with a new class of loss functions and sampling strategy. GRU4Rec+ [14]：GRU4Recの改良版で、新しいクラスの損失関数とサンプリング戦略を持つ。
- Caser [49]: It employs CNN in both horizontal and vertical way to model high-order MCs for sequential recommendation. Caser [49]： 逐次推薦のための高次MCをモデル化するために、水平方向と垂直方向の両方でCNNを用いる。
- SASRec [22]: It uses a left-to-right Transformer language model to capture users’ sequential behaviors, and achieves state-of-the-art performance on sequential recommendation. SASRec [22]: SASRecは、左から右へのTransformer言語モデルを用いて、ユーザの逐次的な行動をとらえ、逐次推薦において最先端の性能を達成している。

For NCF7 , GRU4Rec8 , GRU4Rec+8 , Caser9 , and SASRec10, we use code provided by the corresponding authors.
NCF7 , GRU4Rec8 , GRU4Rec+8 , Caser9 , SASRec10 については、対応する著者から提供されたコードを使用している。
For BPR-MF and FPMC, we implement them using TensorFlow.
BPR-MFとFPMCについては、TensorFlowを使って実装している。
For common hyperparameters in all models, we consider the hidden dimension size d from {16, 32, 64, 128, 256}, the ℓ2 regularizer from {1, 0.1, 0.01, 0.001, 0.0001}, and dropout rate from {0, 0.1, 0.2, · · · , 0.9}.
全モデル共通のハイパーパラメータとして、隠れ次元サイズdを｛16, 32, 64, 128, 256｝から、ℓ2正則化を｛1, 0.1, 0.01, 0.001, 0.0001｝から、ドロップアウト率を｛0, 0.1, 0.2, - -, 0.9｝から考える。
All other hyper-parameters (e.g., Markov order in Caser) and initialization strategies are either followed the suggestion from the methods’ authors or tuned on the validation sets.
その他のハイパーパラメータ（例えば、Caserのマルコフ次数）と初期化ストラテジーはすべて、メソッドの著者からの提案に従うか、検証セット上でチューニングされたものである。
We report the results of each baseline under its optimal hyper-parameter settings.
各ベースラインの最適なハイパーパラメータ設定の結果を報告する。

We implement BERT4Rec11 with TensorFlow.
BERT4Rec11をTensorFlowで実装する。
All parameters are initialized using truncated normal distribution in the range [−0.02, 0.02].
すべてのパラメータは、[-0.02, 0.02]の範囲で切り捨てられた正規分布を用いて初期化される。(正規分布の分散は??)
We train the model using Adam [24] with learning rate of 1e-4, β1 = 0.9, β2 = 0.999, ℓ2 weight decay of 0.01, and linear decay of the learning rate.
Adam [24]を使用し、学習率1e-4、β1 = 0.9、β2 = 0.999、ℓ2重み減衰0.01、学習率線形減衰でモデルを訓練する。
The gradient is clipped when its ℓ2 norm exceeds a threshold of 5.
ℓ2ノルムが閾値5を超えると勾配が切り取られる。
For fair comparison, we set the layer number L = 2 and head number h = 2 and use the same maximum sequence length as in [22], N = 200 for ML-1m and ML-20m, N = 50 for Beauty and Steam datasets.
公平な比較のために、レイヤー数L = 2(うんうん、sequential推薦は少なくて良いんだよね:thinking:)、ヘッド数h = 2とし、[22]と同じ最大配列長、ML-1mとML-20mではN = 200、BeautyとSteamデータセットではN = 50を使用する。
For head setting, we empirically set the dimensionality of each head as 32 (single head if d < 32).
ヘッドの設定については、経験的に各ヘッドの次元数を32とした（d＜32の場合はシングルヘッド）。
We tune the mask proportion ρ using the validation set, resulting in ρ = 0.6 for Beauty, ρ = 0.4 for Steam, and ρ = 0.2 for ML-1m and ML-20m.
検証セットを用いてマスクの割合ρを調整した結果、Beautyではρ=0.6、Steamではρ=0.4、ML-1mとML-20mではρ=0.2となった。
All the models are trained from scratch without any pre-training on a single NVIDIA GeForce GTX 1080 Ti GPU with a batch size of 256.
すべてのモデルは、バッチサイズ256のNVIDIA GeForce GTX 1080 Ti GPU1台で、**事前学習なしでゼロから**学習された。

## 4.4. Overall Performance Comparison 総合成績の比較

![table2]()

Table 2 summarized the best results of all models on four benchmark datasets.
表2は、4つのベンチマークデータセットにおける全モデルの最良の結果をまとめたものである。
The last column is the improvements of BERT4Rec relative to the best baseline.
最後の列は、最良のベースラインに対する BERT4Rec の改善点である。
We omit the NDCG@1 results since it is equal to HR@1 in our experiments.
NDCG@1の結果は、我々の実験ではHR@1と等しいので省略する。
It can be observed that:
以下のことが観察される:

The non-personalized POP method gives the worst performance12 on all datasets since it does not model user’s personalized preference using the historical records.
非パーソナライズドPOP法は、過去の記録を使用してユーザーのパーソナライズされた嗜好をモデル化しないため、すべてのデータセットで最悪のパフォーマンス12を示す。
Among all the baseline methods, sequential methods (e.g., FPMC and GRU4Rec+) outperforms non-sequential methods (e.g., BPR-MF and NCF) on all datasets consistently.
すべてのベースライン手法の中で、逐次手法（FPMCやGRU4Rec+など）は、すべてのデータセットで一貫して非逐次手法（BPR-MFやNCFなど）を上回る。
Compared with BPR-MF, the main improvement of FPMC is that it models users’ historical records in a sequential way.
BPR-MFと比較して、FPMCの主な改善点は、ユーザの履歴記録を逐次的にモデル化することである。
This observation verifies that considering sequential information is beneficial for improving performances in recommendation systems.
この観察から、**逐次的な情報を考慮することが推薦システムのパフォーマンス向上に有益である**ことが検証された。

Among sequential recommendation baselines, Caser outperforms FPMC on all datasets especially for the dense dataset ML-1m, suggesting that high-order MCs is beneficial for sequential recommendation.
逐次推薦ベースラインの中で、Caserは全てのデータセット、特に高密度データセットML-1mにおいてFPMCを凌駕しており、高次MCが逐次推薦に有効であることを示唆している。
However, high-order MCs usually use very small order L since they do not scale well with the order L.
しかし、高次MCは、次数Lに比例してうまくスケールしないため、通常は非常に小さな次数Lを使用する。
This causes Caser to perform worse than GRU4Rec+ and SASRec, especially on sparse datasets.
このため、CaserはGRU4Rec+やSASRecよりも、特にスパースなデータセットではパフォーマンスが悪くなる。
Furthermore, SASRec performs distinctly better than GRU4Rec and GRU4Rec+, suggesting that self-attention mechanism is a more powerful tool for sequential recommendation.
さらに、SASRecはGRU4RecやGRU4Rec+よりも明らかに良い結果を示し、**自己注意メカニズムが逐次推薦においてより強力なツールであることを示唆している**。

According to the results, it is obvious that BERT4Rec performs best among all methods on four datasets in terms of all evaluation metrics.
結果によると、BERT4Recは、4つのデータセットにおいて、すべての評価指標において、すべての手法の中で最も良好な結果を示していることが明らかである。
It gains 7.24% HR@10, 11.03% NDCG@10, and 11.46% MRR improvements (on average) against the strongest baselines.
最強のベースラインに対して、HR@10で7.24%、NDCG@10で11.03%、MRRで11.46%の改善（平均）を達成した。

### Question 1: Do the gains come from the bidirectional self-attention model or from the Cloze objective?

質問1：その利益は、双方向の自己注意モデルからもたらされるのか、それともCloze目的からもたらされるのか？

To answer this question, we try to isolate the effects of these two factors by constraining the Cloze task to mask only one item at a time.
この疑問に答えるため、一度に1つのitemだけをマスクするようにクローズ課題を制約することで、これら2つの要因の影響を分離しようと試みた。
In this way, the main difference between our BERT4Rec (with 1 mask) and SASRec is that BERT4Rec predicts the target item jointly conditioning on both left and right context.
このように、我々のBERT4Rec（マスク1つ）とSASRecの主な違いは、BERT4Recが左右両方の文脈を条件として、ターゲットitemを共同で予測することである。
We report the results on Beauty and ML-1m with d = 256 in Table 3 due to the space limitation.
紙面の都合上、表3ではd=256のBeautyとML-1mの結果を報告する。
The results show that BERT4Rec with 1 mask significantly outperforms SASRec on all metrics.
その結果、マスクを1つ使用したBERT4Recは、すべての測定基準においてSASRecを大幅に上回ることがわかった。
It demonstrates the importance of bidirectional representations for sequential recommendation.
これは、**逐次推薦における双方向表現の重要性**を示している。
Besides, the last two rows indicate that the Cloze objective also improves the performances.
さらに、最後の2行は、Cloze目標もパフォーマンスを向上させることを示している。
Detailed analysis of the mask proportion ρ in Cloze task can be found in § 4.6
クローズ課題におけるマスク割合ρの詳細な分析は§4.6

### Question 2: Why and how does bidirectional model outperform unidirectional models?

なぜ、どのように双方向モデルが一方向モデルを上回るのか？

![figure2]()

To answer this question, we try to reveal meaningful patterns by visualizing the average attention weights of the last 10 items during the test on Beauty in Figure 2.
この問いに答えるため、図2にBeauty上のテスト中の最後の10itemの平均attention wwightを可視化することで、意味のあるパターンを明らかにしようとする。
Due to the space limitation, we only report four representative attention heat-maps in different layers and heads.
紙面の都合上、異なるレイヤーとヘッドにおける代表的な4つのattentionヒートマップのみを報告する。

We make several observations from the results.
この結果から、いくつかの見解を得ることができた。

a) Attention varies across different heads.
a) attentionは各headによって異なる。
For example, in layer 1, head 1 tends to attend on items at the left side while head 2 prefers to attend on items on the right side.
例えば、レイヤー1では、ヘッド1は左側のアイテムに注目し、ヘッド2は右側のアイテムに注目する傾向がある。

b) Attention varies across different layers.
b) attentionは各layerによって異なる。
Apparently, attentions in layer 2 tend to focus on more recent items.
どうやら、レイヤー2では、より新しいものに関心が集中する傾向があるようだ。
This is because layer 2 is directly connected to the output layer and the recent items play a more important role in predicting the future.
これは、レイヤー2が出力レイヤーに直結しており、未来を予測する上で最近の項目がより重要な役割を果たすからである。
Another interesting pattern is that heads in Figure 2a and 2b also tend to attend on [mask]13.(This phenomenon also exists in text sequence modeling using BERT)
もうひとつの興味深いパターンは、図2aと図2bのヘッドもまた、[mask]に参加する傾向があることだ。(この傾向はBERTによるtext sequence modelingでもあるらしい。)
It may be a way for self-attention to propagate sequence-level state to the item level.
これは、自己アテンションがシーケンスレベルの状態をアイテムレベルに伝播させる方法かもしれない。

c) Finally and most importantly, unlike unidirectional model can only attend on items at the left side, items in BERT4Rec tend to attend on the items at both sides.
c)最後に最も重要なことは、一方向モデルが左側のアイテムにしかアテンションできないのとは異なり、BERT4Recのアイテムは両側のアイテムにアテンションする傾向があるということである。
This indicates that bidirectional is essential and beneficial for user behavior sequence modeling.
このことは、**双方向性がユーザ行動シーケンスのモデリングに不可欠**であり、有益であることを示している。

In the following studies, we examine the impact of the hyperparameters, including the hidden dimensionality d, the mask proportion ρ, and the maximum sequence length N.
以下の研究では、隠れ次元d、マスク割合ρ、最大配列長Nなどの**ハイパーパラメータの影響を検証**する。
We analyze one hyper-parameter at a time by fixing the remaining hyper-parameters at their optimal settings.
残りのハイパーパラメータを最適な設定に固定し、一度に1つのハイパーパラメータを分析する。
Due to space limitation, we only report NDCG@10 and HR@10 for the follow-up experiments.
紙面の都合上、追跡実験についてはNDCG@10とHR@10についてのみ報告する。

## 4.5. Impact of Hidden Dimensionality d d

![figure3]()

We now study how the hidden dimensionality d affects the recommendation performance.
次に、**隠れ次元(hidden dimensionality) $d$ が推薦性能にどのような影響を与えるか**を検討する。
Figure 3 shows NDCG@10 and HR@10 for neural sequential methods with the hidden dimensionality d varying from 16 to 256 while keeping other optimal hyper-parameters unchanged.
図3は、隠れ次元dを16から256まで変化させたニューラル逐次法のNDCG@10とHR@10を示し、他の最適ハイパーパラメータは変化させない。
We make some observations from this figure.
この図からいくつかの考察をする。

The most obvious observation from these sub-figures is that the performance of each model tends to converge as the dimensionality increases.
これらの図から最も明らかなのは、**各モデルの性能は、次元が大きくなるにつれて収束する傾向がある**ということである。
A larger hidden dimensionality does not necessarily lead to better model performance, especially on sparse datasets like Beauty and Steam.
特にBeautyやSteamのような**疎なデータセットでは、隠れ次元が大きいほどモデルの性能が向上するとは限らない**。
This is probably caused by overfitting.
これはおそらくオーバーフィッティングによるものだろう。
In terms of details, Caser performs unstably on four datasets, which might limit its usefulness.
詳細については、Caserは4つのデータセットで不安定なパフォーマンスを示しており、その有用性が制限される可能性がある。
Self-attention based methods (i.e., SASRec and BERT4Rec) achieve superior performances on all datasets.
self-attentionに基づく手法（すなわち、SASRecとBERT4Rec）は、すべてのデータセットで優れた性能を達成している。
Finally, our model consistently outperforms all other baselines on all datasets even with a relatively small hidden dimensionality.
最後に、我々のモデルは、隠れ次元が比較的小さい場合でも、全てのデータセットにおいて他の全てのベースラインを一貫して上回る。
Considering that our model achieves satisfactory performance with d≥64, we only report the results with d=64 in the following analysis.
**我々のモデルはd≧64で満足のいく性能を達成することを考慮し、以下の分析ではd=64での結果のみを報告する**。(d=64、小さい...! ID-basedの手法はそれくらいで良いのかも...!)

## 4.6. Impact of Mask Proportion ρ マスク比率の影響 ρ

![figure4]()

As described in § 3.6, mask proportion ρ is a key factor in model training, which directly affects the loss function (Equation 8).
3.6節で説明したように、マスク割合ρはモデル学習における重要な要素であり、損失関数（式8）に直接影響する。
Obviously, mask proportion ρ should not be too small or it is not enough to learn a strong model.
明らかに、マスクの割合ρは小さすぎてはならない。
Meanwhile, it should not be too large, otherwise, it would be hard to train since there are too many items to guess based on a few contexts in such case.
そうでなければ、数個のコンテキストから推測するitemが多すぎるため、学習が困難になる。
To examine this, we study how mask proportion ρ affects the recommendation performances on different datasets.
これを検証するために、マスクの割合ρが推薦性能にどのような影響を与えるかを、異なるデータセットについて研究する。

Figure 4 shows the results with varying mask proportion ρ from 0.1 to 0.9.Considering the results with ρ > 0.6 on all datasets, a general pattern emerges, the performances decreasing as ρ increases.
図4は、マスク比率ρを0.1から0.9まで変化させた結果を示している。すべてのデータセットで**ρ＞0.6の結果を考慮すると、ρが大きくなるにつれて性能が低下するという一般的なパターン**が浮かび上がってくる。
From the results of the first two columns, it is easy to see that ρ = 0.2 performs better than ρ = 0.1 on all datasets.
最初の2列の結果から、すべてのデータセットでρ=0.2がρ=0.1よりも性能が良いことが容易にわかる。
These results verify what we claimed above.
これらの結果は、我々が上記で主張したことを検証するものである。

In addition, we observe that the optimal ρ is highly dependent on the sequence length of the dataset.
さらに、**最適なρはデータセットの配列長に大きく依存する**ことがわかる。(うんうん、そりゃそうな感じ...!:thinking:)
For the datasets with short sequence length (e.g., Beauty and Steam), the best performances are achieved at ρ=0.6 (Beauty) and ρ=0.4 (Steam), while the datasets with long sequence length (e.g., ML-1m and ML-20m) prefer a small ρ=0.2.
配列長が短いデータセット（例えば、BeautyとSteam）では、ρ=0.6（Beauty）とρ=0.4（Steam）で最高の性能が達成されるが、配列長が長いデータセット（例えば、ML-1mとML-20m）では、小さなρ=0.2が好まれる。(あれ、長いほうが$\rho$ 大きくすべきかと思ってた...!:thinking:)
This is reasonable since, compared with short sequence datasets, a large ρ in long sequence datasets means much more items that need to be predicted.
短い配列のデータセットと比較して、長い配列のデータセットで大きなρは、予測する必要がある項目がはるかに多いことを意味するので、これは合理的である。(??)
Take ML-1m and Beauty as example, ρ=0.6 means we need to predict 98=⌊163.5×0.6⌋ items on average per sequence for ML-1m, while it is only 5=⌊8.8×0.6⌋ items for Beauty.
ML-1mとBeautyを例にとると、ρ=0.6は、ML-1mでは1シーケンスあたり平均98=⌊163.5×0.6⌋アイテムを予測する必要があることを意味し、Beautyではわずか5=⌊8.8×0.6⌋アイテムを予測する必要があることを意味する。
The former is too hard for model training.
前者はモデルトレーニングにはハードルが高すぎる。

## 4.7. Impact of Maximum Sequence Length N

We also investigate the effect of the maximum sequence length N on model’s recommendation performances and efficiency.
また、**最大配列長Nがモデルの推薦性能と効率に及ぼす影響**についても調査した。

![table4]()

Table 4 shows recommendation performances and training speed with different maximum length N on Beauty and ML-1m.
表4は、BeautyとML-1mで最大長Nを変えた場合の推薦性能と学習速度を示している。
We observe that the proper maximum length N is also highly dependent on the average sequence length of the dataset.
適切な最大長Nは、データセットの平均配列長にも大きく依存することがわかる。
Beauty prefers a smaller N = 20, while ML-1m achieves the best performances on N = 200.
ML-1mはN = 200で最高のパフォーマンスを達成する一方で、Beautyはより小さなN = 20を好む。
This indicates that a user’s behavior is affected by more recent items on short sequence datasets and less recent items for long sequence datasets.
これは、ユーザの行動が、**短い配列データセットではより新しいアイテムに影響され、長い配列データセットではより新しいアイテムに影響されないこと**を示している。(??)
The model does not consistently benefit from a larger N since a larger N tends to introduce both extra information and more noise.
Nを大きくすると、余分な情報とノイズが増える傾向があるため、Nを大きくしてもモデルは一貫して恩恵を受けない。
However, our model performs very stably as the length N becomes larger.
しかし、我々のモデルは長さNが大きくなるにつれて非常に安定した性能を発揮する。
This indicates that our model can attend to the informative items from the noisy historical records.
これは、我々のモデルがノイズの多い過去の記録から有益なitemを抽出できることを示している。

A scalability concern about BERT4Rec is that its computational complexity per layer is O(n 2d), quadratic with the length n.
BERT4Recのスケーラビリティに関する懸念は、1層あたりの計算量がO(n 2d)であり、長さnの2次関数であることである。(full attention distributionだからか!:thinking:)
Fortunately, the results in Table 4 shows that the self-attention layer can be effectively parallelized using GPUs.
幸い、表4の結果は、自己アテンション層がGPUを使用して効果的に並列化できることを示している。

## 4.8. Ablation Study アブレーション(切除)研究

Finally, we perform ablation experiments over a number of key components of BERT4Rec in order to better understand their impacts, including positional embedding (PE), position-wise feed-forward network (PFFN), layer normalization (LN), residual connection (RC), dropout, the layer number L of self-attention, and the number of heads h in multi-head attention.
最後に、BERT4Recの主要な構成要素である、位置埋め込み（PE）、位置ワイズフィードフォワードネットワーク（PFFN）、レイヤー正規化（LN）、残余接続（RC）、ドロップアウト、自己注意のレイヤー数L、マルチヘッドアテンションにおけるヘッド数hなどの影響をより理解するために、これらの要素のアブレーション実験を行った。
Table 5 shows the results of our default version (L = 2,h = 2) and its eleven variants on all four datasets with dimensionality d = 64 while keeping other hyperparameters (e.g., ρ) at their optimal settings.
表5は、他のハイパーパラメータ（例えば、ρ）を最適な設定に保ちながら、次元d = 64の4つのデータセットすべてについて、我々のデフォルトバージョン（L = 2,h = 2）とその11のバリエーションについての結果を示している。

![table5]()

それぞれの変種を紹介し、その効果を分析する:
We introduce the variants and analyze their effects respectively:

### (1) PE.

The results show that removing positional embeddings causes BERT4Rec’s performances decreasing dramatically on long sequence datasets (i.e., ML-1m and ML-20m).
その結果、位置埋め込みを削除すると、長配列データセット（ML-1mとML-20m）においてBERT4Recの性能が劇的に低下することがわかった。
Without the positional embeddings, the hidden representation HL for each item vi depends only on item embeddings.
位置の埋め込みがなければ、各アイテムviの隠れ表現HLはアイテムの埋め込みのみに依存する。
In this situation, we predict different target items using the same hidden representation of “[mask]”.
この状況では、同じ“[mask]”のhidden representationを使って、異なるターゲット項目を予測する。
This makes the model illposed.
これではモデルのポーズが悪い。(??)
This issue is more serious on long sequence datasets since they have more masked items to predict.
この問題は、長い配列データセットでは予測すべきマスク項目が多くなるため、より深刻になる

### (2) PFFN。

The results show that long sequence datasets (e.g., ML-20m) benefit more from PFFN.
その結果、長い配列データセット（例えばML-20m）はPFFNの恩恵をより多く受けることがわかった。
This is reasonable since a purpose of PFFN is to integrate information from many heads which are preferred by long sequence datasets as discussed in the analysis about head number h in ablation study (5).
PFFNの目的は、アブレーション研究におけるヘッド数hに関する解析(5)で述べたように、長いシーケンスデータセットが好む多くのヘッドからの情報を統合することであるため、これは合理的である。

### (3) LN, RC, and Dropout.

These components are introduced mainly to alleviate overfitting.
**これらのコンポーネントは、主にオーバーフィッティングを緩和するために導入**された。
Obviously, they are more effective on small datasets like Beauty.
明らかに、ビューティのような**小さなデータセットには効果的**だ。(overfitを緩和するcomponent群が!)
To verify their effectiveness on large datasets, we conduct an experiment on ML-20m with layer L=4.
大規模データセットでの有効性を検証するため、レイヤーL=4のML-20mで実験を行った。
The results show that NDCG@10 decreases about 10% w/o RC.
その結果、NDCG@10はRCを使用しない場合、約10%減少することがわかった。

### (4) Number of layers L.

The results show that stacking Transformer layer can boost performances especially on large datasets (e.g, ML-20m).
その結果、Transformerレイヤーを積み重ねることで、特に大規模なデータセット（例えばML-20m）において性能を向上できることが示された。
This verifies that it is helpful to learn more complex item transition patterns via deep self-attention architecture.
これは、深い自己注意アーキテクチャによって、より複雑な項目遷移パターンを学習することが有用であることを検証している。
The decline in Beauty with L = 4 is largely due to overfitting.
L = 4でのビューティーの低下は、オーバーフィッティングによるところが大きい。

### (5) Head number h.

We observe that long sequence datasets (e.g., ML-20m) benefit from a larger h while short sequence datasets (e.g., Beauty) prefer a smaller h.
我々は、長い配列データセット（例えばML-20m）はより大きなhが有益である一方、短い配列データセット（例えばBeauty）はより小さなhを好むことを観察している。
This phenomenon is consistent with the empirical result in [48] that large h is essential for capturing long distance dependencies with multi-head self-attention.
この現象は、[48]の経験的な結果である、**multi-head self-attentionで長距離の依存関係を捉えるには、大きなhが不可欠である**という結果と一致する。

# 5. Conclusion and Future Work 結論と今後の課題

Deep bidirectional self-attention architecture has achieved tremendous success in language understanding.
深い双方向の自己注意アーキテクチャは、言語理解において大きな成功を収めている。
In this paper, we introduce a deep bidirectional sequential model called BERT4Rec for sequential recommendation.
本稿では、逐次推薦のためのBERT4Recと呼ばれる深い双方向逐次モデルを紹介する。
For model training, we introduce the Cloze task which predicts the masked items using both left and right context.
モデルの学習には、左右両方の文脈を用いてマスク項目を予測するCloze課題を導入する。
Extensive experimental results on four real-world datasets show that our model outperforms state-of-the-art baselines.
4つの実世界データセットを用いた広範な実験結果は、我々のモデルが最先端のベースラインを上回ることを示している。

Several directions remain to be explored.
いくつかの方向性が残されている。
A valuable direction is to incorporate rich item features (e.g., category and price for products, cast for movies) into BERT4Rec instead of just modeling item ids.
貴重な方向性は、アイテム ID をモデル化するだけでなく、**豊富なアイテム特徴を BERT4Rec に組み込むこと**である。(例えば、商品であればカテゴリと価格、映画であればキャスト)
Another interesting direction for the future work would be introducing user component into the model for explicit user modeling when the users have multiple sessions.
将来的な研究のもう一つの興味深い方向性は、**ユーザが複数のセッションを持っている場合**、明示的なユーザモデリングのために、ユーザコンポーネントをモデルに導入することであろう。(同一ユーザの複数のsessionの関連性を考慮するって事か...!:thinking:)
