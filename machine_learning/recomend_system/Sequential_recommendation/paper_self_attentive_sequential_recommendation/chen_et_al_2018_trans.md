## Link リンク

- https://arxiv.org/pdf/1808.09781.pdf https://arxiv.org/pdf/1808.09781.pdf

## title タイトル

Self-Attentive Sequential Recommendation
セルフ・アテンション・シーケンシャル・レコメンデーション

## abstract 抄録

Sequential dynamics are a key feature of many modern recommender systems, which seek to capture the ‘context’ of users’ activities on the basis of actions they have performed recently.
シーケンシャルダイナミクスは、多くの最新のレコメンダーシステムの重要な特徴であり、ユーザーが最近行った行動に基づいて、ユーザーの活動の「コンテキスト」を捉えようとするものである。
To capture such patterns, two approaches have proliferated: Markov Chains (MCs) and Recurrent Neural Networks (RNNs).
このようなパターンを捉えるために、2つのアプローチが広まってきた： マルコフ連鎖（MC）とリカレント・ニューラル・ネットワーク（RNN）である。
Markov Chains assume that a user’s next action can be predicted on the basis of just their last (or last few) actions, while RNNs in principle allow for longer-term semantics to be uncovered.
マルコフ・チェーンは、ユーザーの次の行動を、直近（または直近の数回）の行動だけに基づいて予測できると仮定しているが、RNNは原理的に、より長期的なセマンティクスを明らかにすることができる。
Generally speaking, MC-based methods perform best in extremely sparse datasets, where model parsimony is critical, while RNNs perform better in denser datasets where higher model complexity is affordable.
一般的に言って、MCベースの手法は、モデルの簡潔性が重要である極端に疎なデータセットで最高のパフォーマンスを発揮し、RNNは、より高いモデルの複雑さが手頃である密なデータセットでより良いパフォーマンスを発揮する。
The goal of our work is to balance these two goals, by proposing a self-attention based sequential model (SASRec) that allows us to capture long-term semantics (like an RNN), but, using an attention mechanism, makes its predictions based on relatively few actions (like an MC).
私たちの研究の目標は、この**2つの目標のバランスを取ること**である。self-attentionに基づくsequentialモデル（SASRec）を提案することで、（RNNのように）長期的なセマンティクスを捉えることができるが、attentionメカニズムを使用することで、（MCのように）比較的少ない行動に基づいて予測を行うことができる。
At each time step, SASRec seeks to identify which items are ‘relevant’ from a user’s action history, and use them to predict the next item.
各時間ステップにおいて、SASRecはユーザの行動履歴からどのitemが‘relevant’であるかを特定し、次のitemを予測するために使用する。
Extensive empirical studies show that our method outperforms various state-of-the-art sequential models (including MC/CNN/RNN-based approaches) on both sparse and dense datasets.
広範な実証研究により、我々の手法は、**スパースデータセットと高密度データセットの両方において、様々な最先端の逐次モデル（MC/CNN/RNNベースのアプローチを含む）を凌駕する**ことが示されている。
Moreover, the model is an order of magnitude more efficient than comparable CNN/RNN-based models.
さらに、このモデルは、同程度のCNN/RNNベースのモデルよりも桁違いに効率的である。
Visualizations on attention weights also show how our model adaptively handles datasets with various density, and uncovers meaningful patterns in activity sequences.
また、注意の重みを視覚化することで、我々のモデルがいかに様々な密度のデータセットを適応的に処理し、活動シーケンスにおける意味のあるパターンを発見するかを示している。

# Introduction はじめに

The goal of sequential recommender systems is to combine personalized models of user behavior (based on historical activities) with some notion of ‘context’ on the basis of users’ recent actions.
逐次レコメンダーシステムの目標は、（過去の行動に基づく）ユーザー行動のパーソナライズされたモデルと、ユーザーの最近の行動に基づく「コンテキスト」の概念を組み合わせることである。
Capturing useful patterns from sequential dynamics is challenging, primarily because the dimension of the input space grows exponentially with the number of past actions used as context.
シーケンシャルダイナミクスから有用なパターンを捕捉することは困難であるが、その主な理由は、入力空間の次元が、コンテキストとして使用される過去のアクションの数に応じて指数関数的に増大するからである。
Research in sequential recommendation is therefore largely concerned with how to capture these highorder dynamics succinctly.
そのため、逐次推薦の研究は、このような高次のダイナミクスをいかに簡潔にとらえるかに主眼を置いている。
Markov Chains (MCs) are a classic example, which assume that the next action is conditioned on only the previous action (or previous few), and have been successfully adopted to characterize short-range item transitions for recommendation [1].
マルコフ連鎖(MC)は古典的な例であり、次の行動が前の行動(または前の数行動)だけを条件とすると仮定し、推薦のための短距離項目遷移を特徴付けるためにうまく採用されている[1]。
Another line of work uses Recurrent Neural Networks (RNNs) to summarize all previous actions via a hidden state, which is used to predict the next action [2].
別の研究では、リカレント・ニューラル・ネットワーク（RNN）を使用して、隠し状態を介して過去のすべての行動を要約し、次の行動を予測するために使用される[2]。
Both approaches, while strong in specific cases, are somewhat limited to certain types of data.
どちらのアプローチも、特定のケースには強いが、特定のタイプのデータにやや限定される。
MC-based methods, by making strong simplifying assumptions, perform well in highsparsity settings, but may fail to capture the intricate dynamics of more complex scenarios.
MCベースの手法は、単純化する仮定が強いため、スパース性が高い設定ではうまく機能するが、より複雑なシナリオの複雑なダイナミクスを捉えることができない可能性がある。
Conversely RNNs, while expressive, require large amounts of data (an in particular dense data) before they can outperform simpler baselines.
逆にRNNは、表現力は高いものの、単純なベースラインを上回る性能を発揮するには、大量のデータ（特に高密度なデータ）を必要とする。

Recently, a new sequential model Transfomer achieved stateof-the-art performance and efficiency for machine translation tasks [3].
最近、**新しい sequential モデル Transfomer** が機械翻訳タスクで最先端の性能と効率を達成した[3]。(Transformerが2017年、本論文が2018年か...!)
Unlike existing sequential models that use convolutional or recurrent modules, Transformer is purely based on a proposed attention mechanism called ‘self-attention,’ which is highly efficient and capable of uncovering syntactic and semantic patterns between words in a sentence.
Transformerは、畳み込みやリカレントモジュールを使用する既存の逐次モデルとは異なり、純粋に「自己注意」と呼ばれる提案された注意メカニズムに基づいており、非常に効率的で、文中の単語間の統語的・意味的パターンを発見することができる。
Inspired by this method, we seek to apply self-attention mechanisms to sequential recommendation problems.
この方法に触発され、**我々は self-attention メカニズムを sequential 推薦問題に適用することを目指す**。
Our hope is that this idea can address both of the problems outlined above, being on the one hand able to draw context from all actions in the past (like RNNs) but on the other hand being able to frame predictions in terms of just a small number of actions (like MCs).
一方では（RNNのように）過去のすべての行動からコンテキストを引き出すことができ、他方では（MCのように）少数の行動だけから予測を組み立てることができる。
Specifically, we build a Self-Attention based Sequential Recommendation model (SASRec), which adaptively assigns weights to previous items at each time step (Figure 1).
具体的には、**self-attentionに基づく逐次推薦モデル（SASRec）を構築**する. 本モデルは、各時間ステップ(=各time stepでのnext-item prediction)で適応的に過去のアイテムに重みを割り当てる（図1）。
The proposed model significantly outperforms state-of-theart MC/CNN/RNN-based sequential recommendation methods on several benchmark datasets.
提案モデルは、いくつかのベンチマークデータセットにおいて、最新のMC/CNN/RNNベースの sequential 推薦手法を大幅に上回る.
In particular, we examine performance as a function of dataset sparsity, where model performance aligns closely with the patterns described above.
特に、データセットの疎密の関数として性能を検証し、モデルの性能は上述のパターンと密接に一致する.
Due to the self-attention mechanism, SASRec tends to consider long-range dependencies on dense datasets, while focusing on more recent activities on sparse datasets.
self-attention メカニズムにより、SASRecは密なデータセットでは長距離の依存関係を考慮し、疎なデータセットではより最近の活動に焦点を当てる傾向がある。
This proves crucial for adaptively handling datasets with varying density.
これは、密度が変化するデータセットを適応的に処理するために極めて重要である。
Furthermore, the core component (i.e., the self-attention block) of SASRec is suitable for parallel acceleration, resulting in a model that is an order of magnitude faster than CNN/RNNbased alternatives.
さらに、**SASRecのコア・コンポーネント（すなわち自己注意ブロック）は並列加速に適しており、その結果、CNN/RNNベースの代替品よりも1桁高速なモデルが得られる**。
In addition, we analyze the complexity and scalability of SASRec, conduct a comprehensive ablation study to show the effect of key components, and visualize the attention weights to qualitatively reveal the model’s behavior.
さらに、SASRecの複雑性とスケーラビリティを分析し、主要コンポーネントの効果を示すために包括的なアブレーション研究を実施し、**モデルの挙動を定性的に明らかにするために attention weight を可視化する**.

# Related Work 関連作品

Several lines of work are closely related to ours.
私たちの仕事と密接に関係しているものがいくつかある。
We first discuss general, followed by temporal, recommendation, before discussing sequential recommendation (in particular MCs and RNNs).
最初に一般的な推薦、次に時間的な推薦について説明し、その後に逐次的な推薦（特にMCとRNN）について説明する。
Last we introduce the attention mechanism, especially the self-attention module which is at the core of our model.
最後に、注意のメカニズム、特にこのモデルの核となる自己注意モジュールを紹介する。

## General Recommendation

Recommender systems focus on modeling the compatibility between users and items, based on historical feedback (e.g.clicks, purchases, likes).
レコメンダーシステムは、過去のフィードバック（例：クリック、購入、いいね！）に基づいて、ユーザとアイテムの間の互換性をモデル化することに焦点を当てている。
User feedback can be explicit (e.g.ratings) or implicit (e.g.clicks, purchases, comments) [4], [5].
ユーザからのフィードバックは、明示的なもの（評価など）と暗黙的なもの（クリック、購入、コメントなど）がある[4]、[5]。
Modeling implicit feedback can be challenging due to the ambiguity of interpreting ‘non-observed’ (e.g.non-purchased) data.
**暗黙のフィードバックをモデル化することは、「観察されていない」（例えば、購入されていない）データを解釈することの曖昧さのために困難**である。(ウンウン...!)
To address the problem, point-wise [4] and pairwise [5] methods are proposed to solve such challenges.
この問題を解決するために、point-wise法[4]やpairwise法[5]が提案されている.
Matrix Factorization (MF) methods seek to uncover latent dimensions to represent users’ preferences and items’ properties, and estimate interactions through the inner product between the user and item embeddings [6], [7].
行列因数分解(MF)法は、ユーザーの嗜好とアイテムの特性を表す潜在的な次元を明らかにし、ユーザーとアイテムの埋め込み間の内積を通して相互作用を推定しようとする[6]、[7]。
In addition, another line of work is based on Item Similarity Models (ISM) and doesn’t explicitly model each user with latent factors (e.g.FISM [8]).
さらに、Item Similarity モデル(ISM)に基づき、各ユーザを潜在因子で明示的にモデル化しない研究もある(FISM [8]など)。(i.e. Content Base手法の意味だろうか...:thinking:)
They learn an item-to-item similarity matrix, and estimate a user’s preference toward an item via measuring its similarities with items that the user has interacted with before.
**アイテム間の類似度行列を学習**し、あるアイテムに対するユーザの嗜好を、そのユーザーが過去に接したことのあるアイテムとの類似度を測定することで推定する.
Recently, due to their success in related problems, various deep learning techniques have been introduced for recommendation [9].
最近、関連する問題(i.e. 推薦システム以外のMLタスク?)での成功により、様々な深層学習技術が推薦のために導入されている[9]。
One line of work seeks to use neural networks to extract item features (e.g.images [10], [11], text [12], [13], etc.) for content-aware recommendation.
ある研究では、コンテンツを意識した推薦のために、ニューラルネットワークを使ってアイテムの特徴（画像[10]、[11]、テキスト[12]、[13]など）を抽出しようとしている。
Another line of work seeks to replace conventional MF.
従来のMFに取って代わろうとする仕事もある.
For example, NeuMF [14] estimates user preferences via Multi-Layer Perceptions (MLP), and AutoRec [15] predicts ratings using autoencoders.
例えば、NeuMF [14]はMLP（Multi-Layer Perceptions）を用いてユーザの嗜好を推定し、AutoRec [15]はオートエンコーダを用いて評価を予測する.

## Temporal Recommendation 時間的推薦?

Dating back to the Netflix Prize, temporal recommendation has shown strong performance on various tasks by explicitly modeling the timestamp of users’ activities.
ネットフリックス賞までさかのぼると、**temporal recommendation(時間的推薦)**は、ユーザーのアクティビティのタイムスタンプを明示的にモデル化することで、様々なタスクで高いパフォーマンスを示してきた.
TimeSVD++ [16] achieved strong results by splitting time into several segments and modeling users and items separately in each.
TimeSVD++ [16]は、時間をいくつかのセグメントに分割し、それぞれでユーザとアイテムを別々にモデル化することで、強力な結果を達成した.
Such models are essential to understand datasets that exhibit significant (short- or long-term) temporal ‘drift’ (e.g.‘how have movie preferences changed in the last 10 years,’ or ‘what kind of businesses do users visit at 4pm?’, etc.) [16]–[18].
このようなモデルは、重要な（短期的または長期的な）時間的 ‘drift’ 示すデータセットを理解するために不可欠である(例えば、「過去10年間で映画の好みはどのように変化したか」、または「午後4時にユーザーはどのようなビジネスを訪れるか」など)[16]～[18]。(temporal recommendationって、sequential recommendationとは別物なのかな. 順序、というよりは時間?)
Sequential recommendation (or next-item recommendation) differs slightly from this setting, as it only considers the order of actions, and models sequential patterns which are independent of time.
**逐次推薦（または次アイテム推薦）はこの設定とは少し異なり、行動の順序のみを考慮し、時間に依存しない逐次パターンをモデル化する。**(やっぱり! temporal recommendation != sequential recommendation)
Essentially, sequential models try to model the ‘context’ of users’ actions based on their recent activities, rather than considering temporal patterns per se.
基本的に、逐次モデルは、時間的パターンそのものを考慮するのではなく、ユーザーの最近の行動に基づいて、ユーザーの行動の'context(文脈)'をモデル化しようとする。

## Sequential Recommendation

(マルコフ連鎖ベースの手法)
Many sequential recommender systems seek to model itemitem transition matrices as a means of capturing sequential patterns among successive items.
多くの逐次レコメンダーシステムは、連続するアイテム間の逐次パターンを捕捉する手段として、**item-to-item 遷移行列をモデル化**しようとしている。
For instance, FPMC fuses an MF term and an item-item transition term to capture longterm preferences and short-term transitions respectively [1].
例えば、FPMCはMF項とitem-item遷移項を融合し、それぞれ長期的な選好と短期的な遷移を捉える[1].
Essentially, the captured transition is a first-order Markov Chain (MC), whereas higher-order MCs assume the next action is related to several previous actions.
基本的に、捕捉された遷移は一次のマルコフ連鎖（MC）であるのに対し、高次のMCは次の行動がいくつかの前の行動(=一つ前の行動だけでなく...!:thinking:)に関連していると仮定する。
Since the last visited item is often the key factor affecting the user’s next action (essentially providing ‘context’), first-order MC based methods show strong performance, especially on sparse datasets [19].
**最後に訪問したitemは、ユーザの次の行動に影響を与える重要な要素であることが多いため(本質的に‘context’を提供する)**、一次MCベースの手法は、特に疎なデータセットで強力な性能を示す[19].
There are also methods adopting high-order MCs that consider more previous items [20], [21].
また、より前の item を考慮する**高次MC**を採用する方法もある[20]、[21]。
In particular, Convolutional Sequence Embedding (Caser), a CNN-based method, views the embedding matrix of L previous items as an ‘image’ and applies convolutional operations to extract transitions [22].
特に、**CNNベースの手法であるConvolutional Sequence Embedding (Caser)**は、L個前のアイテムの埋め込み行列を「画像」と見なし、畳み込み演算を適用して遷移を抽出する[22].(へぇー！Caserってこういう手法なのか...!:thinking:)

(RNNベースの手法)
Other than MC-based methods, another line of work adopts RNNs to model user sequences [2], [23]–[25].
MCベースの方法以外に、ユーザーシーケンスをモデル化するためにRNNを採用する研究がある[2]、[23]～[25]。
For example, GRU4Rec uses Gated Recurrent Units (GRU) to model click sequences for session-based recommendation [2], and an improved version further boosts its Top-N recommendation performance [26].
例えば、GRU4RecはGated Recurrent Units (GRU)を使ってセッションベースの推薦のための click sequences をモデル化し[2]、改良されたバージョンはTop-N推薦の性能をさらに高めている[26]。
In each time step, RNNs take the state from the last step and current action as its input.
各時間ステップにおいて、RNNは前回のステップのstateと現在のactionを入力とする。(なんか、強化学習みたいな用語...!:thinking:)
These dependencies make RNNs less efficient, though techniques like ‘session-parallelism’ have been proposed to improve efficiency [2].
このような依存関係はRNNの効率を低下させるが、効率を向上させるために「セッション並列性」のようなテクニックが提案されている[2]。

## Attention Mechanisms

Attention mechanisms have been shown to be effective in various tasks such as image captioning [27] and machine translation [28], among others.
注意メカニズムは、画像キャプション付け[27]や機械翻訳[28]など、様々なタスクで有効であることが示されている。
Essentially the idea behind such mechanisms is that sequential outputs (for example) each depend on ‘relevant’ parts of some input that the model should focus on successively.
基本的にこのようなメカニズムの背後にある考え方は、（例えば）連続する出力はそれぞれ、モデルが連続して注目すべき入力の「関連する」部分に依存するというものである。
An additional benefit is that attention-based methods are often more interpretable.
さらに、アテンション・ベースの方法は、より解釈しやすいという利点もある。
Recently, attention mechanisms have been incorporated into recommender systems [29]–[31].
最近、アテンション・メカニズムがレコメンダー・システムに取り入れられている[29]-[31].
For example, Attentional Factorization Machines (AFM) [30] learn the importance of each feature interaction for content-aware recommendation.
例えば、**Attentional Factorization Machines(AFM)[30]**は、コンテンツを考慮した推薦のために、各特徴のinteractionの重要性を学習する. 
However, the attention technique used in the above is essentially an additional component to the original model (e.g.attention+RNNs, attention+FMs, etc.).Recently, a purely attention-based sequence-to-sequence method, Transfomer [3], achieved state-of-the-art performance and efficiency on machine translation tasks which had previously been dominated by RNN/CNN-based approaches [32], [33].
しかし、上記で使用されている注意技術は、基本的に元のモデル（注意+RNNs、注意+FMsなど）に追加されたコンポーネントである。最近、純粋に注意に基づく配列対配列の手法であるTransfomer [3]は、これまでRNN/CNNベースのアプローチによって支配されていた機械翻訳タスクにおいて、最先端のパフォーマンスと効率を達成した[32], [33]。
The Transformer model relies heavily on the proposed ‘self-attention’ modules to capture complex structures in sentences, and to retrieve relevant words (in the source language) for generating the next word (in the target language).
Transformerモデルは、文中の複雑な構造を捉え、（ソース言語の）関連する単語を検索して（ターゲット言語の）次の単語を生成するために、提案された「自己注意」モジュールに大きく依存している。
Inspired by Transformer, we seek to build a new sequential recommendation model based upon the self-attention approach, though the problem of sequential recommendation is quite different from machine translation, and requires specially designed models.
Transformerに触発され、我々は自己注意のアプローチに基づいた新しい逐次推薦モデルを構築しようとしているが、逐次推薦の問題は機械翻訳とは全く異なるため、特別に設計されたモデルが必要である。

# Methodology 方法論

In the setting of sequential recommendation, we are given a user’s action sequence S u = (S u 1 , S u 2 , . , and seek to predict the next item.
逐次推薦の設定では、ユーザーの行動シーケンス が与えられてnext item を予測する事を試みる. 

During the training process, at time step t, the model predicts the next item depending on the previous t items.
学習過程では、時間ステップtで、モデルは前のt個の項目に応じて次の項目を予測する。
As shown in Figure 1, it will be convenient to think of the model’s input as (S u 1 , S u 2 , .
図1に示すように、モデルの入力を（S u 1 , S u 2 , .
..
..
, S u |Su|−1 ) and its expected output as a ‘shifted’ version of the same sequence: (S u 2 , S u 3 , .
Su
..
..
, S u |Su| ).
Su
In this section, we describe how we build a sequential recommendation model via an embedding layer, several self-attention blocks, and a prediction layer.
このセクションでは、埋め込み層、いくつかの自己アテンション・ブロック、予測層を介して、逐次推薦モデルを構築する方法を説明する。
We also analyze its complexity and further discuss how SASRec differs from related models.
また、その複雑さを分析し、SASRecが関連モデルとどのように異なるかについてさらに議論する。
Our notation is summarized in Table I.
我々の表記法を表Iにまとめた。

## Embedding Layer エンベッディングレイヤー

We transform the training sequence (S u 1 , S u 2 , ..., S u |Su|−1 ) into a fixed-length sequence s = (s1, s2, .
Su|−1 ) into a fixed-length sequence s = (s1, s2, .
..
..
, sn), where n represents the maximum length that our model can handle.
ここで、nは我々のモデルが扱える最大の長さを表す。
If the sequence length is greater than n, we consider the most recent n actions.
シーケンスの長さがnより大きい場合は、最新のn個のアクションを考慮する。
If the sequence length is less than n, we repeatedly add a ‘padding’ item to the left until the length is n.
もしシーケンスの長さがnより小さければ、長さがnになるまで左側に「パディング」項目を繰り返し追加する。
We create an item embedding matrix M ∈ R |I|×d where d is the latent dimensionality, and retrieve the input embedding matrix E ∈ R n×d , where Ei = Msi .
I
A constant zero vector 0 is used as the embedding for the padding item.
定数0のベクトル0がパディング項目の埋め込みとして使われる。

### Positional Embedding: 位置の埋め込み：

As we will see in the next section, since the self-attention model doesn’t include any recurrent or convolutional module, it is not aware of the positions of previous items.
次のセクションで説明するように、自己アテンション・モデルにはリカレント・モジュールや畳み込みモジュールが含まれていないため、前のアイテムの位置を認識することができない。
Hence we inject a learnable position embedding P ∈ R n×d into the input embedding:
したがって、学習可能な位置埋め込みP∈R n×d を入力埋め込みに注入する：

$$
\tag{1}
$$

We also tried the fixed position embedding as used in [3], but found that this led to worse performance in our case.
また、[3]で使用されているような固定位置埋め込みも試したが、我々のケースではこの方がパフォーマンスが悪くなることがわかった。
We analyze the effect of the position embedding quantitatively and qualitatively in our experiments.
我々は実験において、位置埋め込みの効果を定量的かつ定性的に分析した。

## Self-Attention Block セルフ・アテンション・ブロック

The scaled dot-product attention [3] is defined as:
スケールド・ドット・プロダクト・アテンション[3]は次のように定義される：

$$
\tag{2}
$$

where Q represents the queries, K the keys and V the values (each row represents an item).
ここで、Qはクエリ、Kはキー、Vは値を表す（各行は項目を表す）。
Intuitively, the attention layer calculates a weighted sum of all values, where the weight between query i and value j relates to the interaction between query i and key j.
直感的には、アテンション層はすべての値の重み付き合計を計算し、ここでクエリiと値jの間の重みはクエリiとキーjの間の相互作用に関係する。
The scale factor √ d is to avoid overly large values of the inner product, especially when the dimensionality is high.
スケールファクター√ dは、特に次元が高い場合に、内積の値が大きくなりすぎないようにするためのものである。

### Self-Attention layer: セルフ・アテンション・レイヤー

In NLP tasks such as machine translation, attention mechanisms are typically used with K = V (e.g.using an RNN encoder-decoder for translation: the encoder’s hidden states are keys and values, and the decoder’s hidden states are queries) [28].
機械翻訳のような自然言語処理タスクでは、一般的にK = Vで注目メカニズムが使用される（例えば、翻訳にRNNエンコーダー・デコーダーを使用する：エンコーダーの隠れ状態はキーと値であり、デコーダーの隠れ状態はクエリーである）[28]。
Recently, a self-attention method was proposed which uses the same objects as queries, keys, and values [3].
最近、同じオブジェクトをクエリ、キー、値として使用する自己アテンション法が提案された[3]。
In our case, the self-attention operation takes the embedding Eb as input, converts it to three matrices through linear projections, and feeds them into an attention layer:
私たちの場合、自己注意演算は埋め込みEbを入力とし、線形射影によって3つの行列に変換し、注意層に送り込む：

where the projection matrices WQ,WK,WV ∈ R d×d .
ここで射影行列WQ,WK,WV∈R d×d 。
The projections make the model more flexible.
プロジェクションはモデルをより柔軟にする。
For example, the model can learn asymmetric interactions (i.e., <query i, key j> and <query j, key i> can have different interactions).
例えば、モデルは非対称な相互作用を学習することができる（つまり、<クエリi, キーj>と<クエリj, キーi>は異なる相互作用を持つことができる）。

### Causality: 因果関係

Due to the nature of sequences, the model should consider only the first t items when predicting the (t + 1)-st item.
シーケンスの性質上、(t + 1)番目の項目を予測する場合、モデルは最初のt項目のみを考慮すべきである。
However, the t-th output of the self-attention layer (St) contains embeddings of subsequent items, which makes the model ill-posed.
しかし、自己注視層のt番目の出力（St）には、それ以降の項目の埋め込みが含まれるため、このモデルはイリーポーズをとることになる。
Hence, we modify the attention by forbidding all links between Qi and Kj (j > i).
したがって、QiとKj（j＞i）間のすべてのリンクを禁止することで、注意を修正する。

### Point-Wise Feed-Forward Network: ポイント・ワイズ・フィードフォワード・ネットワーク：

Though the selfattention is able to aggregate all previous items’ embeddings with adaptive weights, ultimately it is still a linear model.
自己アテンションは、適応的な重みで過去のすべての項目の埋め込みを集約することができるが、最終的には線形モデルであることに変わりはない。
To endow the model with nonlinearity and to consider interactions between different latent dimensions, we apply a point-wise two-layer feed-forward network to all Si identically (sharing parameters):
モデルに非線形性を持たせ、異なる潜在次元間の相互作用を考慮するために、すべてのSiに対して点順2層フィードフォワードネットワークを同一に適用する（パラメータを共有する）：

$$
\tag{4}
$$

where W(1) ,W(2) are d × d matrices and b (1) , b (2) are ddimensional vectors.
ここで、W(1),W(2)はd×d行列、b(1),b(2)はd次元ベクトルである。
Note that there is no interaction between Si and Sj (i 6= j), meaning that we still prevent information leaks (from back to front).
SiとSj（i 6=j）の間には相互作用はない。

## Stacking Self-Attention Blocks

After the first self-attention block, Fi essentially aggregates all previous items’ embeddings (i.e., Ebj , j ≤ i).
最初の自己アテンション・ブロックの後、Fiは基本的に以前のすべてのアイテムの埋め込みを集約する（すなわち、Ebj 、j ≤ i）。
However, it might be useful to learn more complex item transitions via another self-attention block based on F.
しかし、Fに基づく別の自己注意ブロックを介して、より複雑な項目遷移を学習することは有用かもしれない。
Specifically, we stack the self-attention block (i.e., a self-attention layer and a feedforward network), and the b-th (b > 1) block is defined as:
具体的には、自己注意ブロック（すなわち自己注意層とフィードフォワードネットワーク）を積み重ね、b番目（b＞1）のブロックを次のように定義する：

$$
\tag{5}
$$

and the 1-st block is defined as S (1) = S and F (1) = F.
であり、1-stブロックはS (1) = S、F (1) = Fと定義される。

However, when the network goes deeper, several problems become exacerbated: 1) the increased model capacity leads to overfitting; 2) the training process becomes unstable (due to vanishing gradients etc.); and 3) models with more parameters often require more training time.
しかし、ネットワークが深くなると、いくつかの問題が悪化する： 1）モデル容量の増加はオーバーフィッティングにつながる、2）学習プロセスが不安定になる（勾配の消失などが原因）、3）より多くのパラメータを持つモデルは、より多くの学習時間を必要とすることが多い。
Inspired by [3], We perform the following operations to alleviate these problems:
3]にヒントを得て、これらの問題を軽減するために以下の操作を行う：

$$
\tag{5.5}
$$

where g(x) represents the self attention layer or the feedforward network.
ここでg(x)は自己注意層またはフィードフォワードネットワークを表す。
That is to say, for layer g in each block, we apply layer normalization on the input x before feeding into g, apply dropout on g’s output, and add the input x to the final output.
つまり、各ブロックのレイヤーgに対して、gに入力する前に入力xにレイヤー正規化を適用し、gの出力にドロップアウトを適用し、入力xを最終出力に加える。
We introduce these operations below.
以下にこれらの操作を紹介する。

### Residual Connections: 残留コネクション：

In some cases, multi-layer neural networks have demonstrated the ability to learn meaningful features hierarchically [34].
場合によっては、多層ニューラルネットワークは、意味のある特徴を階層的に学習する能力を実証している[34]。
However, simply adding more layers did not easily correspond to better performance until residual networks were proposed [35].
しかし、残差ネットワークが提案されるまでは、単純にレイヤーを増やしても性能向上にはなかなか結びつかなかった[35]。
The core idea behind residual networks is to propagate low-layer features to higher layers by residual connection.
残差ネットワークの核となる考え方は、残差接続によって低レイヤーの特徴を高レイヤーに伝播させることである。
Hence, if low-layer features are useful, the model can easily propagate them to the final layer.
したがって、低レイヤーの特徴が有用であれば、モデルはそれらを最終レイヤーに容易に伝播させることができる。
Similarly, we assume residual connections are also useful in our case.
同様に、残留コネクションも我々のケースでは有用であると仮定する。
For example, existing sequential recommendation methods have shown that the last visited item plays a key role on predicting the next item [1], [19], [21].
例えば、既存の逐次推薦手法では、最後に訪問したアイテムが次のアイテムの予測に重要な役割を果たすことが示されている[1]、[19]、[21]。
However, after several self-attention blocks, the embedding of the last visited item is entangled with all previous items; adding residual connections to propagate the last visited item’s embedding to the final layer would make it much easier for the model to leverage low-layer information.
しかし、いくつかの自己注意ブロックの後、最後に訪問したアイテムの埋め込みは、すべての前のアイテムと絡み合っている。最後に訪問したアイテムの埋め込みを最終層に伝播させる残余接続を追加することで、モデルが低層の情報を活用することがより容易になる。

### Layer Normalization: レイヤーの正規化：

Layer normalization is used to normalize the inputs across features (i.e., zero-mean and unitvariance), which is beneficial for stabilizing and accelerating neural network training [36].
レイヤーの正規化は、特徴間の入力を正規化（すなわち、ゼロ平均と単位分散）するために使用され、これはニューラルネットワークの学習を安定させ、加速させるために有益である[36]。
Unlike batch normalization [37], the statistics used in layer normalization are independent of other samples in the same batch.
バッチ正規化[37]とは異なり、レイヤー正規化で使用される統計量は、同じバッチ内の他のサンプルに依存しない。
Specifically, assuming the input is a vector x which contains all features of a sample, the operation is defined as:
具体的には、入力がサンプルの全特徴を含むベクトルxであるとすると、演算は次のように定義される：

$$
\tag{5.6}
$$

where  is an element-wise product (i.e., the Hadamard product), µ and σ are the mean and variance of x, α and β are learned scaling factors and bias terms.
ここで、μとσはxの平均と分散、αとβは学習されたスケーリング係数とバイアス項である。

### Dropout: 中退：

To alleviate overfitting problems in deep neural networks, ‘Dropout’ regularization techniques have been shown to be effective in various neural network architectures [38].
ディープ・ニューラル・ネットワークにおけるオーバーフィッティングの問題を軽減するために、「ドロップアウト」正則化技術が様々なニューラルネットワーク・アーキテクチャにおいて効果的であることが示されている[38]。
The idea of dropout is simple: randomly ‘turn off’ neurons with probability p during training, and use all neurons when testing.
ドロップアウトの考え方は単純で、トレーニング中に確率pでニューロンをランダムに「オフ」にし、テスト時にはすべてのニューロンを使う。
Further analysis points out that dropout can be viewed as a form of ensemble learning which considers an enormous number of models (exponential in the number of neurons and input features) that share parameters [39].
さらに分析を進めると、ドロップアウトは、パラメータを共有する膨大な数のモデル（ニューロン数と入力特徴量の指数関数）を考慮するアンサンブル学習の一形態と見なすことができることが指摘されている[39]。
We also apply a dropout layer on the embedding Eb.
また、埋め込みEbの上にドロップアウトレイヤーを適用する。

## Prediction Layer

After b self-attention blocks that adaptively and hierarchically extract information of previously consumed items, we predict the next item (given the first t items) based on F (b) t .
過去に消費したアイテムの情報を適応的かつ階層的に抽出するb個の自己注意ブロックの後、F (b) tに基づいて（最初のt個のアイテムが与えられた場合）次のアイテムを予測する。
Specifically, we adopt an MF layer to predict the relevance of item i:
具体的には、アイテムiの関連性を予測するためにMFレイヤーを採用する：

$$
\tag{}
$$

where ri,t is the relevance of item i being the next item given the first t items (i.e., s1, s2, .
ここで、ri,tは、最初のt個の項目（すなわち、s1、s2、...）が与えられたとき、項目iが次の項目であることの関連性である。
..
..
, st), and N ∈ R |I|×d is an item embedding matrix.
I
Hence, a high interaction score ri,t means a high relevance, and we can generate recommendations by ranking the scores.
したがって、インタラクションスコアri,tが高いということは、関連性が高いということであり、スコアをランク付けすることでレコメンデーションを生成することができる。

### Shared Item Embedding: 共有アイテムの埋め込み：

To reduce the model size and alleviate overfitting, we consider another scheme which only uses a single item embedding M:
モデルサイズを小さくし、オーバーフィッティングを緩和するために、単一のアイテム埋め込みMのみを使用する別の方式を考える：

$$
\tag{6}
$$

Note that F (b) t can be represented as a function depending on the item embedding M: F (b) t = f(Ms1 ,Ms2 , .
なお、F (b) tは、項目埋め込みMに依存する関数として表現できる： F (b) t = f(Ms1 ,Ms2 , .
..
..
,Mst ).
Mst ）。
A potential issue of using homogeneous item embeddings is that their inner products cannot represent asymmetric item transitions (e.g.item i is frequently bought after j, but not vise versa), and thus existing methods like FPMC tend to use heterogeneous item embeddings.
同種のアイテム埋め込みを使用することの潜在的な問題は、その内積が非対称なアイテム遷移（例えば、アイテムiはjの後によく買われるが、その逆はない）を表現できないことであり、したがってFPMCのような既存の手法は異種のアイテム埋め込みを使用する傾向がある。
However, our model doesn’t have this issue since it learns a nonlinear transformation.
しかし、我々のモデルは非線形変換を学習するので、この問題はない。
For example, the feed forward network can easily achieve the asymmetry with the same item embedding: FFN(Mi)MT j 6= FFN(Mj )MT i .
例えば、フィード・フォワード・ネットワークは、同じ項目の埋め込みで非対称性を容易に実現できる： FFN(Mi)MT j 6= FFN(Mj )MT i .
Empirically, using a shared item embedding significantly improves the performance of our model.
経験的に、共有項目の埋め込みを使用すると、我々のモデルの性能が大幅に向上する。

### Explicit User Modeling: 明示的なユーザーモデリング：

To provide personalized recommendations, existing methods often take one of two approaches: 1) learn an explicit user embedding representing user preferences (e.g.MF [40], FPMC [1] and Caser [22]); 2) consider the user’s previous actions, and induce an implicit user embedding from embeddings of visited items (e.g.FSIM [8], Fossil [21], GRU4Rec [2]).
パーソナライズされたレコメンデーションを提供するために、既存の手法はしばしば2つのアプローチのうちの1つを取る： 1)ユーザの嗜好を表す明示的なユーザ埋め込みを学習する(例：MF [40]、FPMC [1]、Caser [22])、2)ユーザの過去の行動を考慮し、訪問項目の埋め込みから暗黙的なユーザ埋め込みを誘導する(例：FSIM [8]、Fossil [21]、GRU4Rec [2])。
Our method falls into the latter category, as we generate an embedding F (b) n by considering all actions of a user.
私たちの方法は後者のカテゴリーに属し、ユーザーのすべての行動を考慮して埋め込みF (b) nを生成する。
However, we can also insert an explicit user embedding at the last layer, for example via addition: ru,i,t = (Uu + F (b) t )MT i where U is a user embedding matrix.
ru,i,t=(Uu+F(b)t)MTiここで、Uはユーザー埋め込み行列である。
However, we empirically find that adding an explicit user embedding doesn’t improve performance (presumably because the model already considers all of the user’s actions).
しかし、我々は経験的に、明示的なユーザー埋め込みを追加してもパフォーマンスが向上しないことを発見した（おそらく、モデルがすでにユーザーのすべての行動を考慮しているため）。

## Network Training ネットワークトレーニング

Recall that we convert each user sequence (excluding the last action) (S u 1 , S u 2 , .
各ユーザーシーケンス（最後のアクションを除く）（S u 1 , S u 2 , .
..
..
, S u |Su|−1 ) to a fixed length sequence s = {s1, s2, .
Su
..
..
, sn} via truncation or padding items.
sn}を切り詰めたり、パディングしたりする。
We define ot as the expected output at time step t:
ここでは、otを時間ステップtにおける期待出力と定義する：

$$
\tag{}
$$

where <pad> indicates a padding item.
ここで<pad>はパディング項目を示す。
Our model takes a sequence s as input, the corresponding sequence o as expected output, and we adopt the binary cross entropy loss as the objective function:
我々のモデルは、シーケンスsを入力とし、対応するシーケンスoを期待される出力とし、目的関数としてバイナリクロスエントロピー損失を採用する：

$$
\tag{}
$$

Note that we ignore the terms where ot = <pad>.
ot = <pad>の項は無視することに注意。

The network is optimized by the Adam optimizer [41], which is a variant of Stochastic Gradient Descent (SGD) with adaptive moment estimation.
アダム・オプティマイザ[41]は、適応モーメント推定を用いた確率的勾配降下法(SGD)の変種である。
In each epoch, we randomly generate one negative item j for each time step in each sequence.
各エポックにおいて、各シーケンスの各時間ステップに1つの負アイテムjをランダムに生成する。
More implementation details are described later.
実装の詳細については後述する。

## Complexity Analysis 複雑さ解析

### Space Complexity: スペースの複雑さ：

The learned parameters in our model are from the embeddings and parameters in the self-attention layers, feed-forward networks and layer normalization.
このモデルで学習されるパラメータは、埋め込みと自己アテンション層のパラメータ、フィード・フォワード・ネットワーク、レイヤーの正規化である。
The total number of parameters is O(|I|d + nd + d 2 ), which is moderate compared to other methods (e.g.O(|U|d + |I|d) for FPMC) since it does not grow with the number of users, and d is typically small in recommendation problems.
I

### Time Complexity: 時間の複雑さ：

The computational complexity of our model is mainly due to the self-attention layer and the feedforward network, which is O(n 2d + nd2 ).
このモデルの計算量は、主に自己注意層とフィードフォワードネットワークによるもので、O(n 2d + nd2 )である。
The dominant term is typically O(n 2d) from the self-attention layer.
支配的な項は通常、自己アテンション層からのO(n 2d)である。
However, a convenient property in our model is that the computation in each self-attention layer is fully parallelizable, which is amenable to GPU acceleration.
しかし、我々のモデルの便利な特性は、各自己注意レイヤーの計算が完全に並列化可能であることで、GPUアクセラレーションが可能である。
In contrast, RNN-based methods (e.g.GRU4Rec [2]) have a dependency on time steps (i.e., computation on time step t must wait for results from time step t-1), which leads to an O(n) time on sequential operations.
対照的に、RNNベースの手法（例えばGRU4Rec [2]）は、時間ステップに依存する（すなわち、時間ステップtの計算は、時間ステップt-1からの結果を待たなければならない）ため、逐次処理にO(n)の時間がかかる。
We empirically find our method is over ten times faster than RNN and CNN-based methods with GPUs (the result is similar to that in [3] for machine translation tasks), and the maximum length n can easily scale to a few hundred which is generally sufficient for existing benchmark datasets.
また、最大長nは数百まで容易に拡張可能であり、既存のベンチマークデータセットには一般的に十分である。
During testing, for each user, after calculating the embedding F (b) n , the process is the same as standard MF methods.
テスト中、各ユーザーについて、埋め込みF（b）nを計算した後、標準的なMF手法と同じ処理を行う。
(O(d) for evaluating the preference toward an item).
(アイテムに対する選好を評価するためのO(d))。

### Handing Long Sequences: ロングシークエンスのハンド：

Though our experiments empirically verify the efficiency of our method, ultimately it cannot scale to very long sequences.
我々の実験は経験的に我々の手法の効率を検証しているが、結局のところ、非常に長いシーケンスには拡張できない。
A few options are promising to investigate in the future: 1) using restricted self-attention [42] which only attends on recent actions rather than all actions, and distant actions can be considered in higher layers; 2) splitting long sequences into short segments as in [22].
今後、いくつかの選択肢を検討することが期待される： 1)すべての行動ではなく、最近の行動のみに注目し、遠くの行動はより高いレイヤーで考慮することができる制限自己注目[42]を使用する、2)[22]のように長いシーケンスを短いセグメントに分割する。

## Discussion

We find that SASRec can be viewed as a generalization of some classic CF models.
我々は、SASRecがいくつかの古典的なCFモデルの一般化とみなすことができることを発見した。
We also discuss conceptually how our approach and existing methods handle sequence modeling.
また、我々のアプローチと既存の手法がどのようにシーケンスモデリングを扱うかについても概念的に議論する。

### Reduction to Existing Models: 既存のモデルに対する削減：

• Factorized Markov Chains: FMC factorizes a first-order item transition matrix, and predicts the next item j depending on the last item i:

- 因数分解マルコフ連鎖： FMCは一次項目遷移行列を因数分解し、最後の項目iによって次の項目jを予測する：

$$
\tag{}
$$

If we set the self-attention block to zero, use unshared item embeddings, and remove the position embedding, SASRec reduces to FMC.
自己注意ブロックをゼロに設定し、非共有アイテム埋め込みを使用し、位置埋め込みを削除すると、SASRecはFMCに減少する。
Furthermore, SASRec is also closely related to Factorized Personalized Markov Chains (FPMC) [1], which fuse MF with FMC to capture user preferences and short-term dynamics respectively:
さらに、SASRecはファクトライズド・パーソナライズド・マルコフ連鎖（FMMC）[1]とも密接に関連しており、MFとFMCを融合させることで、ユーザーの嗜好と短期的なダイナミクスをそれぞれ捉えることができる：

$$
\tag{}
$$

Following the reduction operations above for FMC, and adding an explicit user embedding (via concatenation), SASRec is equivalent to FPMC.
上記のFMCの削減操作に従い、（連結による）明示的なユーザー埋め込みを追加すると、SASRecはFPMCと同等になる。

• Factorized Item Similarity Models [8]: FISM estimates a preference score toward item i by considering the similarities between i and items the user consumed before:

- 因数分解項目類似度モデル [8]： FISMは、iとユーザーが以前に消費したアイテムとの類似性を考慮することで、アイテムiに対する嗜好スコアを推定する：

$$
\tag{}
$$

If we use one self-attention layer (excluding the feedforward network), set uniform attention weights (i.e., 1 |Su| ) on items, use unshared item embeddings, and remove the position embedding, SASRec is reduced to FISM.
Su| ) on items, use unshared item embeddings, and remove the position embedding, SASRec is reduced to FISM.
Thus our model can be viewed as an adaptive, hierarchical, sequential item similarity model for next item recommendation.
従って、我々のモデルは、適応的、階層的、逐次的な次の項目推薦のための項目類似度モデルと見なすことができる。

### MC-based Recommendation: MCベースの推薦：

Markov Chains (MC) can effectively capture local sequential patterns, assuming that the next item is only dependent on the previous L items.
マルコフ連鎖（MC）は、次の項目が前のL個の項目にのみ依存すると仮定して、局所的な連続パターンを効果的に捉えることができる。
Exiting MC-based sequential recommendation methods rely on either first-order MCs (e.g.FPMC [1], HRM [43], TransRec [19]) or high-order MCs (e.g.Fossil [21], Vista [20], Caser [22]).
既存のMCベースの逐次推薦手法は、一次MC（FPMC [1]、HRM [43]、TransRec [19]など）または高次MC（Fossil [21]、Vista [20]、Caser [22]など）に依存している。
The first group of methods tend to perform best on sparse datasets.
最初のグループの手法は、スパースなデータセットで最高の性能を発揮する傾向がある。
In contrast, higher-order MC based methods have two limitations: (1) The MC order L needs to be specified before training, rather than being chosen adaptively; (2) The performance and efficiency doesn’t scale well with the order L, hence L is typically small (e.g.less than 5).
(2)性能と効率は次数Lに比例しないため、次数Lは通常小さい（例えば5以下）。
Our method resolves the first issue, since it can adaptively attend on related previous items (e.g.focusing on just the last item on sparse dataset, and more items on dense datasets).
本手法は、関連する過去の項目（例えば、疎なデータセットでは最後の項目だけに注目し、密なデータセットではより多くの項目に注目する）に適応的にアテンションできるため、最初の問題を解決する。
Moreover, our model is essentially conditioned on n previous items, and can empirically scale to several hundred previous items, exhibiting performance gains with moderate increases in training time.
さらに、我々のモデルは、基本的にn個の過去項目を条件としており、経験的に数百個の過去項目まで拡張可能であり、訓練時間の適度な増加で性能向上を示す。

### RNN-based Recommendation: RNN ベースの推薦：

Another line of work seeks to use RNNs to model user action sequences [2], [17], [26].
別の研究では、RNNを使用してユーザーの行動シーケンスをモデル化しようとしている[2]、[17]、[26]。
RNNs are generally suitable for modeling sequences, though recent studies show CNNs and self-attention can be stronger in some sequential settings [3], [44].
RNNは一般的にシーケンスのモデリングに適しているが、最近の研究では、CNNと自己アテンションは、いくつかのシーケンシャルな設定でより強くなる可能性があることが示されている[3]、[44]。
Our self-attention based model can be derived from item similarity models, which are a reasonable alternative for sequence modeling for recommendation.
私たちの自己アテンションに基づくモデルは、推薦のためのシーケンスモデリングの合理的な代替物である項目類似性モデルから導き出すことができる。
For RNNs, other than their inefficiency in parallel computation (Section III-F), their maximum path length (from an input node to related output nodes) is O(n).
RNNの場合、並列計算の効率が悪い（セクションIII-F）以外に、（入力ノードから関連する出力ノードまでの）最大パス長はO(n)である。
In contrast, our model has O(1) maximum path length, which can be beneficial for learning long-range dependencies [45].
対照的に、我々のモデルは最大パス長がO(1)であり、長距離依存関係を学習するのに有効である[45]。

# Experiments 実験

In this section, we present our experimental setup and empirical results.
このセクションでは、実験セットアップと実証結果を紹介する。
Our experiments are designed to answer the following research questions:
我々の実験は、以下の研究課題に答えるためにデザインされた：

- RQ1: Does SASRec outperform state-of-the-art models including CNN/RNN based methods? RQ1: SASRecは、CNN/RNNをベースとした手法を含む最先端のモデルよりも優れているか？

- RQ2: What is the influence of various components in the SASRec architecture? RQ2：SASRecのアーキテクチャにおける様々なコンポーネントの影響は？

- RQ3: What is the training efficiency and scalability (regarding n) of SASRec? RQ3: SASRecの学習効率とスケーラビリティ（nについて）は？

- RQ4: Are the attention weights able to learn meaningful patterns related to positions or items’ attributes? RQ4：アテンションウェイトは、位置やアイテムの属性に関連する意味のあるパターンを学習することができるか？

## Datasets データセット

We evaluate our methods on four datasets from three real world applications.
我々は、3つの実際のアプリケーションから得られた4つのデータセットで我々の方法を評価する。
The datasets vary significantly in domains, platforms, and sparsity:
データセットは、ドメイン、プラットフォーム、スパース性が大きく異なる：

• Amazon: A series of datasets introduced in [46], comprising large corpora of product reviews crawled from Amazon.com.

- Amazon： [46]で紹介された一連のデータセットで、Amazon.comからクロールされた商品レビューの大規模なコーパスで構成されている。
  Top-level product categories on Amazon are treated as separate datasets.
  アマゾンのトップレベルの商品カテゴリーは、別のデータセットとして扱われる。
  We consider two categories, ‘Beauty,’ and ‘Games.’ This dataset is notable for its high sparsity and variability.
  我々は、「美」と「ゲーム」の2つのカテゴリーを考えている。このデータセットの特筆すべき点は、その高いスパース性と可変性である。

• Steam: We introduce a new dataset crawled from Steam, a large online video game distribution platform.

- Steam 大規模なオンラインゲーム配信プラットフォームであるSteamからクロールされた新しいデータセットを紹介する。
  The dataset contains 2,567,538 users, 15,474 games and 7,793,069 English reviews spanning October 2010 to January 2018.
  データセットには、2010年10月から2018年1月までの2,567,538人のユーザー、15,474本のゲーム、7,793,069件の英語レビューが含まれている。
  The dataset also includes rich information that might be useful in future work, like users’ play hours, pricing information, media score, category, developer (etc.).
  このデータセットには、ユーザーのプレイ時間、価格情報、メディアスコア、カテゴリー、開発者（など）など、今後の研究に役立つかもしれない豊富な情報も含まれている。

• MovieLens: A widely used benchmark dataset for evaluating collaborative filtering algorithms.

- MovieLens： 協調フィルタリングアルゴリズムの評価に広く使用されているベンチマークデータセット。
  We use the version (MovieLens-1M) that includes 1 million user ratings.
  我々は、100万人のユーザー評価を含むバージョン（MovieLens-1M）を使用しています。

We followed the same preprocessing procedure from [1], [19], [21].
我々は、[1]、[19]、[21]と同じ前処理手順に従った。
For all datasets, we treat the presence of a review or rating as implicit feedback (i.e., the user interacted with the item) and use timestamps to determine the sequence order of actions.
すべてのデータセットについて、レビューや評価の存在を暗黙のフィードバック（つまり、ユーザーがアイテムと相互作用した）として扱い、タイムスタンプを使ってアクションの順序を決定する。
We discard users and items with fewer than 5 related actions.
関連するアクションが5つ以下のユーザーとアイテムは破棄する。
For partitioning, we split the historical sequence S u for each user u into three parts: (1) the most recent action S u |Su| for testing, (2) the second most recent action S u |Su|−1 for validation, and (3) all remaining actions for training.
Su
Note that during testing, the input sequences contain training actions and the validation action.
テスト中、入力シーケンスにはトレーニングアクションと検証アクションが含まれることに注意。

Data statistics are shown in Table II.
データの統計を表IIに示す。
We see that the two Amazon datasets have the fewest actions per user and per item (on average), Steam has a high average number of actions per item, and MovieLens-1m is the most dense dataset.
アマゾンの2つのデータセットは、ユーザーあたりとアイテムあたりのアクション数が（平均して）最も少なく、スチームはアイテムあたりの平均アクション数が多く、MovieLens-1mは最も密度の高いデータセットであることがわかる。

## Comparison Methods 比較方法

To show the effectiveness of our method, we include three groups of recommendation baselines.
本手法の有効性を示すため、3つの推薦ベースライン・グループを用意した。
The first group includes general recommendation methods which only consider user feedback without considering the sequence order of actions:
最初のグループには、行動の順序を考慮せずにユーザーのフィードバックのみを考慮する一般的な推薦方法が含まれる：

• PopRec: This is a simple baseline that ranks items according to their popularity (i.e., number of associated actions).

- PopRec： これは人気度（つまり関連するアクションの数）に応じてアイテムをランク付けするシンプルなベースラインである。

• Bayesian Personalized Ranking (BPR) [5]: BPR is a classic method for learning personalized rankings from implicit feedback.

- ベイズ・パーソナライズド・ランキング（BPR）[5]： BPRは、暗黙のフィードバックからパーソナライズされたランキングを学習する古典的な手法である。
  Biased matrix factorization is used as the underlying recommender.
  基礎となるレコメンダーとしてバイアス行列分解を使用。

The second group contains sequential recommendation methods based on first order Markov chains, which consider the last visited item:
第二のグループは、一次マルコフ連鎖に基づく逐次推薦法で、最後に訪問したアイテムを考慮する：

• Factorized Markov Chains (FMC): A first-order Markov chain method.

- 因数分解マルコフ連鎖 (FMC)： 一次マルコフ連鎖法。
  FMC factorizes an item transition matrix using two item embeddings, and generates recommendations depending only on the last visited item.
  FMCは、2つの項目埋め込みを用いて項目遷移行列を因数分解し、最後に訪問した項目のみに依存する推薦文を生成する。

• Factorized Personalized Markov Chains (FPMC) [1]: FPMC uses a combination of matrix factorization and factorized first-order Markov chains as its recommender, which captures users’ long-term preferences as well as item-to-item transitions.

- 因数分解パーソナライズド・マルコフ連鎖（FPMC） [1]： FPMCは、行列因数分解と因数分解一次マルコフ連鎖の組み合わせをレコメンダーとして使用し、ユーザーの長期的な嗜好とアイテム間の遷移を捉える。

• Translation-based Recommendation (TransRec) [19]: A state-of-the-art first-order sequential recommendation method which models each user as a translation vector to capture the transition from the current item to the next.

- 翻訳ベースの推薦（TransRec）[19]： 各ユーザーを翻訳ベクトルとしてモデル化し、現在のアイテムから次のアイテムへの遷移を捉える、最先端の一次逐次推薦手法。

The last group contains deep-learning based sequential recommender systems, which consider several (or all) previously visited items:
最後のグループには、ディープラーニングに基づく逐次推薦システムが含まれ、これは以前に訪問したいくつかの（あるいはすべての）アイテムを考慮する：

• GRU4Rec [2]: A seminal method that uses RNNs to model user action sequences for session-based recommendation.

- GRU4Rec [2]： セッションベースの推薦のために、RNNを使ってユーザの行動シーケンスをモデル化する代表的な手法。
  We treat each user’s feedback sequence as a session.
  各ユーザーのフィードバックシーケンスをセッションとして扱う。

• GRU4Rec+ [26]: An improved version of GRU4Rec, which adopts a different loss function and sampling strategy, and shows significant performance gains on TopN recommendation.

- GRU4Rec+ [26]： GRU4Recの改良版で、異なる損失関数とサンプリング戦略を採用し、TopN推薦において大幅な性能向上を示す。

• Convolutional Sequence Embeddings (Caser) [22]: A recently proposed CNN-based method capturing highorder Markov chains by applying convolutional operations on the embedding matrix of the L most recent items, and achieves state-of-the-art sequential recommendation performance.

- 畳み込み系列埋め込み（Caser）[22]： 最近提案されたCNNベースの手法で、最新L項目の埋め込み行列に畳み込み演算を適用することで高次マルコフ連鎖を捕捉し、最先端の逐次推薦性能を実現する。

Since other sequential recommendation methods (e.g.PRME [47], HRM [43], Fossil [21]) have been outperformed on similar datasets by baselines among those above, we omit comparison against them.
他の逐次推薦手法（PRME [47]、HRM [43]、Fossil [21]など）は、類似のデータセットにおいて、上記のうちベースラインによって凌駕されているので、それらとの比較は省略する。
We also don’t include temporal recommendation methods like TimeSVD++ [16] and RRN [17], which differ in setting from what we consider here.
また、TimeSVD++[16]やRRN[17]のような時間的推薦法は含まれていない。

For fair comparison, we implement BPR, FMC, FPMC, and TransRec using TemsorFlow with the Adam [41] optimizer.
公正な比較のために、Adam[41]オプティマイザを搭載したTemsorFlowを用いてBPR、FMC、FPMC、TransRecを実装した。
For GRU4Rec, GRU4Rec+ , and Caser, we use code provided by the corresponding authors.
GRU4Rec、GRU4Rec+、Caserについては、対応する著者から提供されたコードを使用している。
For all methods except PopRec, we consider latent dimensions d from {10, 20, 30, 40, 50}.
PopRec以外のすべての手法では、{10, 20, 30, 40, 50}から潜在次元dを考える。
For BPR, FMC, FPMC, and TransRec, the `2 regularizer is chosen from {0.0001, 0.001, 0.01, 0.1, 1}. BPR、FMC、FPMC、およびTransRecでは、`2正則化子は{0.0001, 0.001, 0.01, 0.1, 1}から選択される。
All other hyperparameters and initialization strategies are those suggested by the methods’ authors.
他のすべてのハイパーパラメータと初期化戦略は、メソッドの著者が提案したものである。
We tune hyper-parameters using the validation set, and terminate training if validation performance doesn’t improve for 20 epochs.
検証セットを使ってハイパーパラメータを調整し、検証パフォーマンスが20エポック改善しない場合は学習を終了する。

## implementation Details implementation details

For the architecture in the default version of SASRec, we use two self-attention blocks (b = 2), and use the learned positional embedding.
SASRecのデフォルトバージョンのアーキテクチャでは、2つの自己注意ブロック（b = 2）を使用し、学習された位置埋め込みを使用する。
Item embeddings in the embedding layer and prediction layer are shared.
埋め込み層と予測層のアイテム埋め込みは共有される。
We implement SASRec with TensorFlow.
SASRecをTensorFlowで実装する。
The optimizer is the Adam optimizer [41], the learning rate is set to 0.001, and the batch size is 128.
オプティマイザは Adam optimizer [41]、学習率は 0.001、バッチサイズは 128 である。
The dropout rate of turning off neurons is 0.2 for MovieLens-1m and 0.5 for the other three datasets due to their sparsity.
ニューロンをオフにするドロップアウト率は、MovieLens-1mでは0.2、他の3つのデータセットでは疎なため0.5である。
The maximum sequence length n is set to 200 for MovieLens-1m and 50 for the other three datasets, i.e., roughly proportional to the mean number of actions per user.
最大シーケンス長nは、MovieLens-1mでは200、他の3つのデータセットでは50に設定されている。
Performance of variants and different hyper-parameters is examined below.
以下では、さまざまなハイパーパラメータの性能について検証する。
All code and data shall be released at publication time.
すべてのコードとデータは出版時に公開される。

## Evaluation Metrics 評価指標

We adopt two common Top-N metrics, Hit Rate@10 and NDCG@10, to evaluate recommendation performance [14], [19].
我々は、推薦性能を評価するために、2つの一般的なTop-Nメトリクス、Hit Rate@10とNDCG@10を採用する[14], [19]。
Hit@10 counts the fraction of times that the ground-truth next item is among the top 10 items, while NDCG@10 is a position-aware metric which assigns larger weights on higher positions.
Hit@10は、グランドトゥルースの次の項目が上位10項目の中にある回数の割合をカウントし、NDCG@10は、より高い位置に大きな重みを割り当てる位置を考慮した指標である。
Note that since we only have one test item for each user, Hit@10 is equivalent to Recall@10, and is proportional to Precision@10.
各ユーザーに1つのテスト項目しかないので、Hit@10はRecall@10と等価であり、Precision@10に比例することに注意。
To avoid heavy computation on all user-item pairs, we followed the strategy in [14], [48].
すべてのユーザーとアイテムのペアで重い計算を避けるために、我々は[14]、[48]の戦略に従った。
For each user u, we randomly sample 100 negative items, and rank these items with the ground-truth item.
各ユーザーuについて、ランダムに100個のネガティブアイテムをサンプリングし、これらのアイテムをグランドトゥルースアイテムと順位付けする。
Based on the rankings of these 101 items, Hit@10 and NDCG@10 can be evaluated.
この101項目の順位に基づいて、Hit@10とNDCG@10を評価することができる。

## Recommendation Performance

Table III presents the recommendation performance of all methods on the four datasets (RQ1).
表IIIは、4つのデータセット（RQ1）に対する全手法の推薦性能を示している。
By considering the second best methods across all datasets, a general pattern emerges with non-neural methods (i.e., (a)-(e)) performing better on sparse datasets and neural approaches (i.e., (f)-(h)) performing better on denser datasets.
すべてのデータセットで2番目に優れた手法を考慮すると、非ニューラル手法（すなわち(a)～(e)）は疎なデータセットで、ニューラルアプローチ（すなわち(f)～(h)）は密なデータセットで、それぞれ優れた性能を発揮するという一般的なパターンが浮かび上がる。
Presumably this owes to neural approaches having more parameters to capture high order transitions (i.e., they are expressive but easily overfit), whereas carefully designed but simpler models are more effective in high-sparsity settings.
おそらくこれは、ニューラル・アプローチが高次の遷移を捉えるために多くのパラメーターを持つ（つまり、表現力は豊かだがオーバーフィットしやすい）ためであり、一方、注意深く設計されたシンプルなモデルの方が、スパース性が高い設定では効果的である。
Our method SASRec outperforms all baselines on both sparse and dense datasets, and gains 6.9% Hit Rate and 9.6% NDCG improvements (on average) against the strongest baseline.
我々の手法SASRecは、スパースデータセットと高密度データセットの両方において、全てのベースラインを凌駕し、最強のベースラインに対して6.9%のHit Rateと9.6%のNDCGの改善を獲得した（平均）。
One likely reason is that our model can adaptively attend items within different ranges on different datasets (e.g.only the previous item on sparse datasets and more on dense datasets).
その理由のひとつは、我々のモデルがデータセットによって異なる範囲（例えば、疎なデータセットでは前の項目のみ、密なデータセットではより多くの項目）の項目に適応的に出席することができるからであろう。
We further analyze this behavior in Section IV-H.
セクションIV-Hでこの挙動をさらに分析する。
In Figure 2 we also analyze the effect of a key hyperparameter, the latent dimensionality d, by showing NDCG@10 of all methods with d varying from 10 to 50.
図2では、重要なハイパーパラメータである潜在次元数dの効果も分析し、dを10から50まで変化させた場合のNDCG@10を示した。
We see that our model typically benefits from larger numbers of latent dimensions.
我々のモデルは通常、潜在次元の数が多い方が有利であることがわかる。
For all datasets, our model achieves satisfactory performance with d ≥ 40.
すべてのデータセットにおいて、我々のモデルはd≧40で満足のいく性能を達成した。

## Ablation Study アブレーション研究

Since there are many components in our architecture, we analyze their impacts via an ablation study (RQ2).
我々のアーキテクチャには多くのコンポーネントがあるため、アブレーション研究（RQ2）を通じてそれらの影響を分析する。
Table IV shows the performance of our default method and its 8 variants on all four dataset (with d = 50).
表IVは、4つのデータセットすべて（d = 50）に対する、我々のデフォルト手法とその8つの変種の性能を示している。
We introduce the variants and analyze their effect respectively:
それぞれの変種を紹介し、その効果を分析する：

• (1) Remove PE (Positional Embedding): Without the positional embedding P, the attention weight on each item depends only on item embeddings.

- (1) PE（位置埋め込み）を取り除く： 位置埋め込みPがなければ、各項目の注目度は項目埋め込みのみに依存する。
  That is to say, the model makes recommendations based on users’ past actions, but their order doesn’t matter.
  つまり、このモデルはユーザーの過去の行動に基づいて推薦を行うが、その順番は関係ない。
  This variant might be suitable for sparse datasets, where user sequences are typically short.
  この変種は、ユーザー配列が一般的に短い、疎なデータセットに適しているかもしれない。
  This variant performs better then the default model on the sparsest dataset (Beauty), but worse on other denser datasets.
  この変種は、最も疎なデータセット（Beauty）ではデフォルトモデルより良い性能を示すが、他の密なデータセットでは悪い。

• (2) Unshared IE (Item Embedding): We find that using two item embeddings consistently impairs the performance, presumably due to overfitting.

- (2) 非共有IE（項目埋め込み）： 項目埋め込みを2つ用いると、オーバーフィッティングのためと思われるが、一貫して性能が低下することがわかった。

• (3) Remove RC (Residual Connections): Without residual connections, we find that performance is significantly worse.

- (3) RC（残留コネクション）を取り除く： 残留コネクションがない場合、パフォーマンスが著しく低下することがわかる。
  Presumably this is because information in lower layers (e.g.the last item’s embedding and the output of the first block) can not be easily propagated to the final layer, and this information is highly useful for making recommendations, especially on sparse datasets.
  おそらくこれは、下位層の情報（例えば、最後のアイテムの埋め込みや最初のブロックの出力）が最終層に伝搬しにくいためであり、特に疎なデータセットでは、この情報は推薦を行う上で非常に有用である。

• (4) Remove Dropout: Our results show that dropout can effectively regularize the model to achieve better test performance, especially on sparse datasets.

- (4) ドロップアウトの除去： 我々の結果は、ドロップアウトがモデルを効果的に正則化し、特に疎なデータセットにおいて、より良いテスト性能を達成できることを示している。
  The results also imply the overfitting problem is less severe on dense datasets.
  この結果はまた、密なデータセットではオーバーフィッティングの問題がそれほど深刻ではないことを示唆している。

• (5)-(7) Number of blocks: Not surprisingly, results are inferior with zero blocks, since the model would only depend on the last item.

- (5)-(7) ブロック数： モデルは最後の項目にのみ依存するため、ブロック数が0の場合、結果は劣る。
  The variant with one block performs reasonably well, though using two blocks (the default model) still boosts performance especially on dense datasets, meaning that the hierarchical self-attention structure is helpful to learn more complex item transitions.
  ブロックが1つのバリエーションは、それなりに良いパフォーマンスを示したが、2つのブロック（デフォルトモデル）を使っても、特に密なデータセットではパフォーマンスが向上する。これは、階層的な自己注意構造が、より複雑な項目遷移を学習するのに役立つことを意味している。
  Using three blocks achieves similar performance to the default model.
  3つのブロックを使用することで、デフォルトモデルと同様のパフォーマンスを達成した。

• (8) Multi-head: The authors of Transformer [3] found that it is useful to use ‘multi-head’ attention, which applies attention in h subspaces (each a d/h-dimensional space).

- (8) マルチヘッド： Transformer[3]の著者は、h個の部分空間（それぞれd/h次元空間）で注意を適用する「マルチヘッド」注意を使用することが有用であることを発見した。
  However, performance with two heads is consistently and slightly worse than single-head attention in our case.
  しかし、2つのヘッドを使った場合のパフォーマンスは、一貫して、我々のケースでは1つのヘッドでの注目よりもわずかに悪い。
  This might owe to the small d in our problem (d = 512 in Transformer), which is not suitable for decomposition into smaller subspaces.
  これは、我々の問題のdが小さく（Transformerではd = 512）、より小さな部分空間への分解に適していないためかもしれない。

## Training Efficiency & Scalability トレーニングの効率とスケーラビリティ

We evaluate two aspects of the training efficiency (RQ3) of our model: Training speed (time taken for one epoch of training) and convergence time (time taken to achieve satisfactory performance).
我々のモデルの学習効率（RQ3）を2つの側面から評価する： 学習速度（1エポックの学習に要する時間）と収束時間（満足のいく性能を達成するのに要する時間）である。
We also examine the scalability of our model in terms of the maximum length n.
また、このモデルのスケーラビリティを最大長nの観点から検証する。
All experiments are conducted with a single GTX-1080 Ti GPU.
すべての実験は、GTX-1080 Ti GPU 1台で実施した。

### Training Efficiency: トレーニングの効率：

Figure 3 demonstrates the efficiency of deep learning based methods with GPU acceleration.
図3は、GPUアクセラレーションによるディープラーニングベースの手法の効率を示している。
GRU4Rec is omitted due to its inferior performance.
GRU4Recは性能が劣るため省略。
For fair comparison, there are two training options for Caser and GRU4Rec+ : using complete training data or just the most recent 200 actions (as in SASRec).
公正な比較のために、CaserとGRU4Rec+には2つの学習オプションがあります：完全な学習データを使用するか、（SASRecのように）最新の200アクションだけを使用するかです。
For computing speed, SASRec only spends 1.7 seconds on model updates for one epoch, which is over 11 times faster than Caser (19.1s/epoch) and 18 times faster than GRU4Rec+ (30.7s/epoch).
計算速度に関しては、SASRecは1エポックのモデル更新に1.7秒しか費やしておらず、これはCaser（19.1s/エポック）の11倍以上、GRU4Rec+（30.7s/エポック）の18倍以上の速度である。
We also see that SASRec converges to optimal performance within around 350 seconds on ML-1M while other models require much longer.
また、SASRecはML-1Mでは350秒程度で最適性能に収束するのに対し、他のモデルではもっと長い時間を要することがわかる。
We also find that using full data leads to better performance for Caser and GRU4Rec+ .
また、Caser と GRU4Rec+ については、完全なデータを使用した方がパフォーマンスが向上することがわかった。

### Scalability: スケーラビリティ：

As with standard MF methods, SASRec scales linearly with the total number of users, items and actions.
標準的なMF手法と同様に、SASRecはユーザー、アイテム、アクションの総数に応じて線形にスケールする。
A potential scalability concern is the maximum length n, however the computation can be effectively parallelized with GPUs.
潜在的なスケーラビリティの懸念は、最大長nであるが、計算はGPUで効果的に並列化できる。
Here we measure the training time and performance of SASRec with different n, empirically study its scalability, and analyze whether it can handle sequential recommendation in most cases.
ここでは、SASRecの学習時間と性能を異なるnで測定し、そのスケーラビリティを経験的に研究し、ほとんどのケースで逐次推薦を扱うことができるかどうかを分析する。
Table V shows the performance and efficiency of SASRec with various sequence lengths.
表Vは、様々なシーケンス長でのSASRecの性能と効率を示している。
Performance is better with larger n, up to around n = 500 at which point performance saturates (possibly because 99.8% of actions have been covered).
nが大きいほど性能は向上し、n=500あたりで性能は飽和する（おそらく99.8%のアクションがカバーされたため）。
However, even with n = 600, the model can be trained in 2,000 seconds, which is still faster than Caser and GRU4Rec+ .
しかし、n = 600であっても、モデルは2,000秒で学習でき、これはCaserやGRU4Rec+よりも速い。
Hence, our model can easily scale to user sequences up to a few hundred actions, which is suitable for typical review and purchase datasets.
したがって、我々のモデルは、数百アクションまでのユーザーシーケンスに容易に拡張することができ、これは典型的なレビューや購入のデータセットに適している。
We plan to investigate approaches (discussed in Section III-F) for handling very long sequences in the future.
今後、非常に長いシーケンスを処理するためのアプローチ（セクションIII-Fで説明）を調査する予定である。

## Visualizing Attention Weights 注意の重みを視覚化する

Recall that at time step t, the self-attention mechanism in our model adaptively assigns weights on the first t items depending on their position embeddings and item embeddings.
時間ステップtにおいて、我々のモデルの自己注意メカニズムは、位置埋め込みと項目埋め込みに応じて、最初のt個の項目に適応的に重みを割り当てることを思い出す。
To answer RQ4, we examine all training sequences and seek to reveal meaningful patterns by showing the average attention weights on positions as well as items.
RQ4に答えるために、すべてのトレーニングシーケンスを調べ、アイテムだけでなくポジションに対する平均的な注意の重みを示すことで、意味のあるパターンを明らかにしようとする。

### Attention on Positions: ポジションに関する注意事項

Figure 4 shows four heatmaps of average attention weights on the last 15 positions at the last 15 time steps.
図4は、直近の15タイムステップにおける直近15ポジションの平均アテンションウェイトの4つのヒートマップを示している。
Note that when we calculate the average weight, the denominator is the number of valid weights, so as to avoid the influence of padding items in short sequences.
平均ウェイトを計算する際、短いシーケンスにおけるパディング項目の影響を避けるため、分母は有効なウェイトの数であることに注意。
We consider a few comparisons among the heatmaps:
ヒートマップ間の比較をいくつか考えてみる：

• (a) vs.

- a）対（b）。
  (c): This comparison indicates that the model tends to attend on more recent items on the sparse dataset Beauty, and less recent items for the dense dataset ML-1M.
  (c): この比較は、モデルが疎なデータセットBeautyではより新しいアイテムに、密なデータセットML-1Mではより新しいアイテムにアテンションする傾向があることを示している。
  This is the key factor that allows our model to adaptively handle both sparse and dense datasets, whereas existing methods tend to focus on one end of the spectrum.
  これは、既存の手法がどちらか一方に集中しがちなのに対し、我々のモデルが疎なデータセットと密なデータセットの両方を適応的に扱えるようにする重要な要素である。

• (b) vs.

- b）対（b）。
  (c): This comparison shows the effect of using positional embeddings (PE).
  (c): この比較は、位置埋め込み（PE）を使用した場合の効果を示している。
  Without them attention weights are essentially uniformly distributed over previous items, while the default model (c) is more sensitive in position as it is inclined to attend on recent items.
  デフォルトのモデル(c)は、最近のアイテムに注意を向ける傾向があるため、位置がより敏感になる。

• (c) vs.

- (c) vs.
  (d): Since our model is hierarchical, this shows how attention varies across different blocks.
  (d): 我々のモデルは階層的であるため、異なるブロック間で注意力がどのように変化するかを示している。
  Apparently, attention in high layers tends to focus on more recent positions.
  どうやら、高いレイヤーでは、より最近のポジションに注目が集まる傾向があるようだ。
  Presumably this is because the first self-attention block already considers all previous items, and the second block does not need to consider far away positions.
  おそらくこれは、最初の自己注意ブロックがすでにすべての前の項目を考慮しており、2番目のブロックが遠くの位置を考慮する必要がないからだと思われる。

Overall, the visualizations show that the behavior of our self-attention mechanism is adaptive, position-aware, and hierarchical.
全体として、視覚化は、我々の自己注意メカニズムの動作が適応的で、位置を認識し、階層的であることを示している。

### Attention Between Items: 項目間の注意：

Showing attention weights between a few cherry-picked items might not be statistically meaningful.
厳選されたいくつかの項目間の注目度を示しても、統計的には意味がないかもしれない。
To perform a broader comparison, using MovieLens-1M, where each movie has several categories, we randomly select two disjoint sets where each set contains 200 movies from 4 categories: Science Fiction (Sci-Fi), Romance, Animation, and Horror.
より広範な比較を行うために、各映画がいくつかのカテゴリを持つMovieLens-1Mを使用し、各セットが4つのカテゴリから200映画を含む2つの不連続なセットをランダムに選択します： SF、ロマンス、アニメーション、ホラー。
The first set is used for the query and the second set as the key.
最初のセットはクエリーに使われ、2番目のセットはキーとして使われる。
Figure 5 shows a heatmap of average attention weights between the two sets.
図5は、2つのセット間の平均注目度重みのヒートマップである。
We can see the heatmap is approximately a block diagonal matrix, meaning that the attention mechanism can identify similar items (e.g.items sharing a common category) and tends to assign larger weights between them (without being aware of categories in advance).
ヒートマップがほぼブロック対角行列であることがわかる。これは、注意メカニズムが類似のアイテム（例えば、共通のカテゴリーを共有するアイテム）を識別でき、（事前にカテゴリーを意識することなく）それらの間でより大きな重みを割り当てる傾向があることを意味する。

# Conclusion 結論

In this work, we proposed a novel self-attention based sequential model SASRec for next item recommendation.
本研究では、次のアイテムを推薦するための新しい自己注意に基づく逐次モデルSASRecを提案する。
SASRec models the entire user sequence (without any recurrent or convolutional operations), and adaptively considers consumed items for prediction.
SASRecは（リカレント演算や畳み込み演算を行わずに）ユーザーシーケンス全体をモデル化し、適応的に消費された項目を予測に考慮する。
Extensive empirical results on both sparse and dense datasets show that our model outperforms stateof-the-art baselines, and is an order of magnitude faster than CNN/RNN based approaches.
疎なデータセットと密なデータセットの両方における広範な実証結果は、我々のモデルが最新のベースラインを凌駕し、CNN/RNNベースのアプローチよりも桁違いに高速であることを示している。
In the future, we plan to extend the model by incorporating rich context information (e.g.dwell time, action types, locations, devices, etc.), and to investigate approaches to handle very long sequences (e.g.clicks).
将来的には、豊富なコンテキスト情報（滞留時間、行動タイプ、場所、デバイスなど）を組み込んでモデルを拡張し、非常に長いシーケンス（クリックなど）を扱うアプローチを調査する予定である。
