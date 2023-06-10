## 0.1. link リンク

- https://arxiv.org/abs/1706.03762 https://arxiv.org/abs/1706.03762

## 0.2. title タイトル

Attention Is All You Need
アテンション・イズ・オール・ユー・ニード

## 0.3. abstract アブストラクト

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration.
支配的な配列の伝達モデルは、エンコーダー・デコーダー構成の複雑なリカレントまたは畳み込みニューラルネットワークをベースにしています。
The best performing models also connect the encoder and decoder through an attention mechanism.
また、性能の良いモデルでは、エンコーダーとデコーダーをアテンション機構で接続しています。
We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.
私たちは、**attention のメカニズムにのみ基づき**、再帰や畳み込みを完全に排除した新しい**シンプルな**ネットワークアーキテクチャ "**Transformer**"を提案します。(attentionってrecurrenceの一種だと思ってた...)
Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.
2つの機械翻訳タスクで実験した結果、これらのモデルは、並列化可能で訓練に要する時間が大幅に短縮される一方で、品質が優れていることがわかりました。
Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU.
本モデルは、WMT 2014の英語からドイツ語への翻訳タスクで28.4 BLEUを達成し、アンサンブルを含む既存の最良結果を2 BLEU以上上回った。
On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature.
WMT 2014の英仏翻訳タスクにおいて、我々のモデルは、8台のGPUで3.5日間学習した後、新しい単一モデルの最新BLEUスコア41.8を確立しました（文献にある最高のモデルの学習コストのごく一部です）。
We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.
我々は、Transformerが他のタスクにうまく汎化することを、大規模な訓練データと限られた訓練データの両方で英語の構成語構文解析にうまく適用することによって示す。

# 1. Introduction 序章

Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation [35, 2, 5].
リカレントニューラルネットワーク、特にlong short-term memory(LSTM)型 [13] とゲート型リカレント [7] ニューラルネットワークは、言語モデリングや機械翻訳などのシーケンスモデリングやトランスダクション問題における最先端のアプローチとして確固たる地位を築いている [35, 2, 5].
Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures [38, 24, 15].
その後、リカレント言語モデルやエンコーダ・デコーダ・アーキテクチャの限界に挑戦する数多くの努力が続けられている[38, 24, 15]。

Recurrent models typically factor computation along the symbol positions of the input and output sequences.
リカレントモデルは、通常、入力と出力シーケンスのシンボル位置に沿って計算を行う。
Aligning the positions to steps in computation time, they generate a sequence of hidden states ht, as a function of the previous hidden state ht−1 and the input for position t.
位置を計算時間のステップに合わせ、前の隠れ状態$h_{t-1}$と位置$t$の入力の関数として、一連の隠れ状態$h_{t}$を生成する。
This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples.
この本質的に**逐次的な性質は、トレーニングデータ内での並列化を妨げます**。これは、メモリ制約により例間でのバッチ処理が制限されるため、シーケンス長が長くなるにつれて重要になります。
Recent work has achieved significant improvements in computational efficiency through factorization tricks [21] and conditional computation [32], while also improving model performance in case of the latter.
最近の研究では、因数分解のトリック[21]や条件付き計算[32]によって計算効率の大幅な向上を達成し、後者の場合はモデルの性能も向上しています。
The fundamental constraint of sequential computation, however, remains.
しかし、逐次計算の基本的な制約が残っています。

Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences [2, 19].
Attentionメカニズムは、様々なタスクにおける説得力のあるシーケンスモデリングや伝達(transduction)モデルに不可欠な要素となっており、入力シーケンスや出力シーケンスにおける距離に関係なく依存関係をモデリングすることができます[2, 19]。
In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network.
しかし、一部の事例[27]を除いて、**このような attention メカニズムはリカレントネットワークと組み合わせて使用**されている.

In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.
本研究では、**recurrence を排除**し、代わりに入力と出力の間のグローバルな依存関係を描く attention メカニズムに完全に依存するモデルアーキテクチャであるTransformerを提案します。
The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.
Transformerは、**大幅に並列化**することができ、8つのP100 GPUでわずか12時間の学習で、翻訳品質の新たな境地に達することができます。

# 2. Background

The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU [16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building block, computing hidden representations in parallel for all input and output positions.
**逐次計算を減らすという目標**は、Extended Neural GPU [16], ByteNet [18], ConvS2S [9]の基礎にもなっています。これらはすべて、畳み込みニューラルネットワークを基本構成要素として、すべての入力と出力位置に対して並行して隠れ表現を計算しています。
In these models, the number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet.
これらのモデルでは、任意の2つの入出力位置からの信号を関連付けるために必要な演算数は、位置間の距離に応じて、ConvS2Sでは線形に、ByteNetでは対数的に増加する。
This makes it more difficult to learn dependencies between distant positions [12].
そのため、**離れた位置同士の依存関係を学習することが難しくなっています**[12]。
In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as described in section 3.2.
Transformerでは、この操作は一定の回数に抑えられます。attention の重み付けされた位置が平均化されるため、有効解像度が低下する事を代償とするが。この効果は3.2節で述べたように、マルチヘッドアテンションで打ち消されています。

Self-attention, sometimes called intra-attention is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence.
**Self-attention**(intra-attentionと呼ばれることもある)は、1つの配列の異なる位置を関連付け、配列の表現を計算するためのattention機構である。
Self-attention has been used successfully in a variety of tasks including reading comprehension, abstractive summarization, textual entailment and learning task-independent sentence representations [4, 27, 28, 22].
Self-attention は、読解、抽象的要約、テキストの含意、タスクに依存しない文表現の学習など、さまざまなタスクでうまく利用されている[4, 27, 28, 22]．

End-to-end memory networks are based on a recurrent attention mechanism instead of sequencealigned recurrence and have been shown to perform well on simple-language question answering and language modeling tasks [34].
エンドツーエンドメモリーネットワークは、配列に沿った再帰性ではなく、再帰性注意メカニズムに基づいており、単純な言語の質問応答や言語モデリングタスクで優れた性能を示すことが示されている[34]。

To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequencealigned RNNs or convolution.
しかし、私たちの知る限り、Transformerは、配列整列したRNNや畳み込みを使用せずに、入力と出力の表現を計算するために、**完全にself-attentionに依存**する最初のtransduction(伝達)モデルです。
In the following sections, we will describe the Transformer, motivate self-attention and discuss its advantages over models such as [17, 18] and [9].
以下のセクションでは、Transformerについて説明し、self-attentionをを動機付け、[17, 18]や[9]のようなモデルに対する優位性を議論することにする。

# 3. Model Architecture モデル・アーキテクチャ

Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35].
競合する neural sequence 伝達モデルの多くは、**エンコーダ-デコーダ構造**を持っている [5, 2, 35].
Here, the encoder maps an input sequence of symbol representations $(x1, ..., xn)$ to a sequence of continuous representations $z = (z1, ..., zn)$.
ここで、エンコーダは、入力された記号表現列$(x1, ..., xn)$を連続(連続値って事?)表現列$z = (z1, ..., zn)$にマッピングする.
Given z, the decoder then generates an output sequence $(y1, ..., ym)$ of symbols one element at a time.
zが与えられると、次にデコーダはシンボルの出力シーケンス$(y1, ..., ym)$を一度に1要素ずつ生成する。
At each step the model is auto-regressive [10], consuming the previously generated symbols as additional input when generating the next.
各ステップにおいて、モデルは自動回帰的であり[10]、**次のシンボルを生成する際に、以前に生成されたシンボルを追加入力として消費します**。(これはrecurciveのイメージ)

The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1, respectively.
Transformerは、図1の左半分と右半分にそれぞれ示すように、エンコーダーとデコーダーの両方に、積層self-attentionとpoint-wiseなfully connected layersを使用する、というこの全体的なアーキテクチャに従います。

## 3.1. Encoder and Decoder Stacks

### 3.1.1. Encoder: エンコーダー

The encoder is composed of a stack of N = 6 identical layers.
エンコーダは、$N =6$個の同一の層を積み重ねたものである。
Each layer has two sub-layers.
各層には**2つのサブレイヤー**があります。
The first is a multi-head self-attention mechanism, and the second is a simple, positionwise fully connected feed-forward network.
1つ目は、multi-headなself-attention機構、2つ目は、位置的に完全接続されたシンプルなフィードフォワードネットワーク(=全結合層?)です。
We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1].
2つのサブレイヤーそれぞれの周囲に残留接続[11]を採用し、その後、レイヤー正規化[1]を行います。
That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself.
つまり、各サブレイヤーの出力は $LayerNorm(x + Sublayer(x))$ となり、$Sublayer(x)$ はサブレイヤー自身が実装する関数である。
To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512.
このような残差接続(residual connections)を容易にするため、埋め込み層だけでなく、モデルのすべてのサブ層は、$d_{model} = 512$の次元の出力を生成します。

### 3.1.2. Decoder: デコーダー

The decoder is also composed of a stack of N = 6 identical layers.
デコーダもN＝6個の同一の層を積み重ねることで構成されています。
In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack.
デコーダは、各エンコーダ層の2つのサブレイヤーに加えて、エンコーダスタックの出力に対してmulti-head attentionを実行する**第3のサブレイヤー**を挿入する。
Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization.
エンコーダーと同様に、**各サブレイヤーの周辺に残差接続(residual connections)を採用し、その後レイヤー正規化を行います**。
We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions.
また、デコーダスタックのself-attention sub-layerを変更し、positionsが後続のpositonsに attention するのを防ぐ. ("positions"って系列データの位置の事だよね?)
This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.
このmaskingは、出力埋め込みが1位置分オフセットされていることと相まって、**位置iの予測はiより小さい位置の既知の出力にのみ依存できる**ことを保証します。

## 3.2. Attention アテンション

An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.
attention機能は、**"query" と "key-valueペアの集合" (=これらが入力?)をoutputにマッピングするもの**として記述することができ、**query、key、value、およびoutputはすべてベクトル**である.
The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.
出力はvalueの重み付き合計として計算され、各valueに割り当てられた重みは、対応するkeyとqueryの互換性関数(compatibility function)によって計算される。

### 3.2.1. Scaled Dot-Product Attention スケールドドットプロダクトアテンション

We call our particular attention "Scaled Dot-Product Attention" (Figure 2).
私たちは、このattentionを"**Scaled Dot-Product Attention**"と呼んでいます（図2）。
The input consists of queries and keys of dimension dk, and values of dimension dv.
入力はqueryと次元$d_k$のkey、次元$d_v$のvalueで構成される。
We compute the dot products of the query with all keys, divide each by √ dk, and apply a softmax function to obtain the weights on the values.
queryとすべてのkeyのドット積を計算し、それぞれを$\sqrt{d_k}$で割り、ソフトマックス関数を適用して各valueの重みを求める.

In practice, we compute the attention function on a set of queries simultaneously, packed together into a matrix Q.
実際には、行列$Q$にまとめられたqueryの集合に対して同時にattention関数を計算する。
The keys and values are also packed together into matrices K and V .
また、keyとvalueは、マトリックス$K$と$V$にまとめられている。
We compute the matrix of outputs as:
として、出力の行列を計算する：

$$
Attention(Q, K, V) = softmax(\frac{Q K^{T}}{\sqrt{d_k}})V
\tag{1}
$$

(↑によると、$Attention(Q,K,V) \in \mathbb{R}^{}$)

The two most commonly used attention functions are additive attention [2], and dot-product (multiplicative) attention.
最もよく使われるattention関数は、**additive(加法) attention[2]**と**dot-product (multiplicative=乗法) attention**の2つです。
Dot-product attention is identical to our algorithm, except for the scaling factor of √ 1 dk .
dot-product attentionは、スケーリングファクターが $\frac{1}{\sqrt{d_k}}$ であることを除けば、**我々のアルゴリズムと同じ**である.
Additive attention computes the compatibility function using a feed-forward network with a single hidden layer.
Additive attentionは、1つの隠れ層を持つフィードフォワードネットワーク(=全結合層?)を使用してcompatibility function(互換性関数?何それ?)を計算します。
(互換性関数=入力として与えられた**queryとkeyのペアの間の関連性や適合度を計算する**為に使用される関数... = dot-product attention関数の場合は、単にqueryベクトルとkeyベクトル間の内積を取って関連性を計算しているのか...!! それに対してadditive attention関数の場合は、わざわざ関連性を出力する全結合層を使ってるって事?)
While the two are similar in theoretical complexity, dot-product attention is much faster and more space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code.
両者は理論的な複雑さでは似ていますが、高度に最適化された行列乗算コードを用いて実装できるため、実際には dot-product attention の方がはるかに高速でスペース効率に優れています。

While for small values of dk the two mechanisms perform similarly, additive attention outperforms dot product attention without scaling for larger values of dk [3].
$d_k$ の値が小さいうちは2つの機構は同様の性能を発揮するが、$d_k$の値が大きくなると加法的注意はスケーリングなしでドット積注意に勝る[3]。
We suspect that for large values of dk, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients 4 .
$d_k$の値が大きい場合、**ドット積の大きさが大きくなり**、ソフトマックス関数の勾配が極端に小さくなる領域に押し込まれるのではないかと推測される4 。
To counteract this effect, we scale the dot products by √ 1 dk .
この効果を打ち消すために、ドットプロダクトを $\sqrt{d_k}$ だけスケーリングします.

### 3.2.2. Multi-Head Attention マルチヘッドアテンション

Instead of performing a single attention function with dmodel-dimensional keys, values and queries, we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections to dk, dk and dv dimensions, respectively.
$d_{model}$ 次元のkey、value、queryで単一のattention関数を実行する代わりに、query、key、valueをそれぞれ $d_k$ 、$d_k$ 、$d_v$ 次元に異なる、学習済みの**線形投影(=linearly project)**で $h$ 回行うことが有益であることがわかった. (ここがmulti-head! h個のdot-product attention関数の出力を使う、って意味??)
On each of these projected versions of queries, keys and values we then perform the attention function in parallel, yielding dv-dimensional output values.
これらの投影されたquery、value、valueのそれぞれに対して、attention機能を**並行**して実行し、**$d_v$次元の出力値**を得る.
These are concatenated and once again projected, resulting in the final values, as depicted in Figure 2.
これを連結(concat, $d_v \times h$ 次元になる?)して再び投影(=linearly project)すると、図2に示すような最終的な値が得られる.

(メモ)

- 線形投影(linear projection):
  - ベクトルを**低次元の部分空間**に射影する操作.
- 線形変換(linear transformation):
  - 同ベクトル空間にて、ベクトルの向きと長さを変換する操作.

Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.
Multi-head attention は、モデルが異なる位置の異なる表現部分空間からの情報に共同してattentionすることを可能にする.
With a single attention head, averaging inhibits this.
single attention headでは、平均化することでこれを抑制しています。

$$
MultiHead(Q,K,V) = Concat(head_{1}, \cdots, head_{h}) W^{O}
\\
\text{where } head_{i} = Attention(QW^{Q}_{i}, KW^{K}_{i}, VW^{V}_{i})
\tag{2}
$$

Where the projections are parameter matrices W Q i ∈ R dmodel×dk , W K i ∈ R dmodel×dk , WV i ∈ R dmodel×dv and WO ∈ R hdv×dmodel .
ここで、各投影(linear projection)に用いるパラメータ行列は以下:

- $W^{Q}_{i} \in \mathbb{R}^{d_{model} \times d_k}$、
- $W^{K}_{i} \in \mathbb{R}^{d_{model} \times d_k}$、
- $W^{V}_{i} \in \mathbb{R}^{d_{model} \times d_v}$、
- $W^{O} \in \mathbb{R}^{h d_{v}\times d_{model}}$

(queryは系列データのある一つの位置の入力データ、keysは系列データの全位置の入力データ、valuesは系列データの全位置の出力データというか教師ラベル的なイメージ? そして $d_{model}$ は系列データの長さ??)

(メモ)
上の定義を見ると、入力となる各行列の次元数は以下:

- $Q \in \mathbb{R}^{d_k \times d_{model}}$
- $K \in \mathbb{R}^{d_k \times d_{model}}$
- $V \in \mathbb{R}^{d_v \times d_{model}}$

In this work we employ h = 8 parallel attention layers, or heads.
本研究では、h = 8個のparallel attention layers(i.e. head)を採用しています。
For each of these we use dk = dv = dmodel/h = 64.
それぞれ、$d_k = d_v = \frac{d_{model}}{h} = 64$ としています。
Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality.
各ヘッドの次元が小さくなるため(線形投影して行列の次元数が$d_k \times d_{model}$ -> $d_k × d_k$ に低次元になるから...!!)、総計算コストは、完全な次元を持つシングルヘッドアテンションのものと同様です。

### 3.2.3. Applications of Attention in our Model アテンションの応用モデル

The Transformer uses multi-head attention in three different ways:
トランスフォーマーは、3種類の方法で multi-head attention を使用します：

- In "encoder-decoder attention" layers, the queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder. This allows every position in the decoder to attend over all positions in the input sequence. This mimics the typical encoder-decoder attention mechanisms in sequence-to-sequence models such as [38, 2, 9]. **"encoder-decoder attention"層**では、queriesは前のデコーダー層から、メモリのkeysとvaluesはエンコーダーの出力からやってきます。 これにより、**デコーダーの各positionは、入力シーケンスのすべてのpositionに出席することができます**。 これは、[38, 2, 9]などの配列対配列モデルにおける典型的なエンコーダ・デコーダの注意メカニズムを模倣しています。

- The encoder contains self-attention layers. In a self-attention layer all of the keys, values and queries come from the same place, in this case, the output of the previous layer in the encoder. Each position in the encoder can attend to all positions in the previous layer of the encoder. **エンコーダーには、self-attention層**が含まれています。 self-attention層では、すべてのkeys、values、queriesは同じところ(=同じposition?)から来る、この場合、エンコーダの前の層の出力である。 エンコーダーの各positionは、エンコーダーの前のレイヤーのすべてのpositonにアテンションすることができます。

- Similarly, self-attention layers in the decoder allow each position in the decoder to attend to all positions in the decoder up to and including that position. We need to prevent leftward information flow in the decoder to preserve the auto-regressive property. We implement this inside of scaled dot-product attention by masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections. See Figure 2. 同様に、**デコーダのself-attention層**は、デコーダ内の各positionが、**そのpositionまでのデコーダ内のすべての位置**にattentionすることを可能にします。 自動回帰性を維持するために、デコーダで左向き(=逆向き? 時間を逆戻り的なイメージ?)の情報フローを防ぐ必要があります. ソフトマックスの入力のうち、不正な接続に対応するすべてのvaluesをマスクする(-∞に設定する)ことで、scaled-dot-product attentionの内部でこれを実装しています。 図2参照。

## 3.3. Position-wise Feed-Forward Networks ポジションワイズフィードフォワードネットワーク

In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically.
attention sub-layersに加え、エンコーダーとデコーダーの各レイヤーには完全接続のフィードフォワードネットワーク(=全結合層!)が含まれており、各ポジションに別々に同じように適用されます。
This consists of two linear transformations with a ReLU activation in between.
これは、2つの線形変換(=つまり中間層は一つ!)とその間のReLU活性化で構成されています.

$$
FFN(x) = \max(0, xW_{1} + b_{1})W_{2} + b_{2}
\tag{2}
$$

While the linear transformations are the same across different positions, they use different parameters from layer to layer.
線形変換は異なるpositionで同じですが(同じparametersを使用)、レイヤーごとに異なるparametersを使用します。(そりゃそうじゃ...!)
Another way of describing this is as two convolutions with kernel size 1.
別の表現では、カーネルサイズ1の2つの convolutions(畳み込み) として表現されます。
The dimensionality of input and output is dmodel = 512, and the inner-layer has dimensionality df f = 2048.
入出力層の次元は $d_{model} = 512$、中間層の次元は $d_{ff} = 2048$ である。

## 3.4. Embeddings and Softmax エンベッディングとソフトマックス

Similarly to other sequence transduction models, we use learned embeddings to convert the input tokens and output tokens to vectors of dimension dmodel.
他の配列変換モデルと同様に、学習済み埋め込みを用いて、入力tokensと出力トークンを次元tokensのベクトルに変換する.
We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities.
また、デコーダ出力を予測される**next-token確率**に変換するために、通常の学習済み線形変換とソフトマックス関数を使用します。(**次のtokenを予測するタスク...!!?? LLMと同じか...!!!???**)
In our model, we share the same weight matrix between the two embedding layers and the pre-softmax linear transformation, similar to [30].
本モデルでは、[30]と同様に、2つの埋め込み層(=これもFFNなのかな?)とプレソフトマックス線形変換の間で**同じ重み行列(parameter?)を共有**しています。
In the embedding layers, we multiply those weights by √ dmodel.
埋め込み層では、それらの重みに $\sqrt{d_{model}}$ を乗算する.

## 3.5. Positional Encoding 位置エンコード

Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.
このモデルには再帰も畳み込みもないので、**モデルがシーケンスの順序を利用するためには、シーケンス内のtokensの相対位置または絶対位置に関する何らかの情報を注入する必要があります。**
To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks.
そのため、エンコーダとデコーダのスタックの底にある入力埋め込みに"**positional encodings**"を追加する.
The positional encodings have the same dimension dmodel as the embeddings, so that the two can be summed.
**positional encodingsは(tokenの)エンベッディングと同じ次元 $d_{model}$ を持つ**ので、両者を合計することができる. ($d_{model}$は文章の長さ、という認識であってるかな)
There are many choices of positional encodings, learned and fixed [9].
位置エンコーディングには、学習型と固定型という多くの選択肢がある[9]。

In this work, we use sine and cosine functions of different frequencies:
本作品では、周波数の異なる正弦関数と余弦関数を使用しています：

$$
PE_{pos, 2i} = \sin(pos/10000^{2i/d_{model}})
\\
PE_{pos, 2i+1} = \cos(pos/10000^{2i/d_{model}})
\tag{2.2}
$$

where pos is the position and i is the dimension.
ここで、$pos$ は位置(sequenceデータの中の対象tokenの座標, **絶対的な位置座標**)である. $i$ は、位置エンコーディングベクトルの各次元を表すindexである.(このiは、モデルが**相対的な位置関係**を学習する為の情報源になる...!)
That is, each dimension of the positional encoding corresponds to a sinusoid.
つまり、位置エンコードの各次元は、正弦波に対応する.
The wavelengths form a geometric progression from 2π to 10000 · 2π.
波長は2πから $10000 \cdot 2π$ までの幾何学的な進行を形成しています.
We chose this function because we hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset k, P Epos+k can be represented as a linear function of P Epos.
この関数を選んだのは、任意の固定オフセット(=定数?) $k$ に対して、$PE_{pos+k}$ は $PE_{pos}$ の **線形関数 として表現できる**(i.e. $PE_{pos}$をなんらかの形で線形変換したら $PE_{pos+k}$ Fに変形できる...!)ため、相対位置による出席をモデルが容易に学習できると仮定したからです。

We also experimented with using learned positional embeddings [9] instead, and found that the two versions produced nearly identical results (see Table 3 row (E)).
また、代わりに学習済みのpositional embeddings[9]を使う実験も行い、2つのバージョンでほぼ同じ結果が得られることがわかりました（表3の行（E）参照）。
We chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than the ones encountered during training.
正弦波バージョンを選択したのは、トレーニング中に遭遇したシーケンスよりも長いシーケンス長にモデルを外挿できるようにするためです。

# 4. Why Self-Attention ♪ なぜ、セルフアテンションなのか

In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations (x1, ..., xn) to another sequence of equal length (z1, ..., zn), with xi , zi ∈ R d , such as a hidden layer in a typical sequence transduction encoder or decoder.
このセクションでは、典型的なシーケンス変換エンコーダやデコーダの隠れ層のように、ある可変長の記号表現列（x1、...、xn）を、同じ長さの別の列（z1、...、zn）にマッピングするために一般的に使用されるリカレント層や畳み込み層の様々な側面を比較する。
Motivating our use of self-attention we consider three desiderata.
私たちが「セルフアテンションズ」を使う動機として、3つの望みを考えています。

One is the total computational complexity per layer.
1つは、1層あたりの総計算量です。
Another is the amount of computation that can be parallelized, as measured by the minimum number of sequential operations required.
もう一つは、必要な逐次処理の最小数によって測定される、並列化できる計算の量である。

The third is the path length between long-range dependencies in the network.
3つ目は、ネットワーク内の長距離依存関係間の経路長である。
Learning long-range dependencies is a key challenge in many sequence transduction tasks.
長距離の依存関係を学習することは、多くの配列伝達タスクにおける重要な課題である。
One key factor affecting the ability to learn such dependencies is the length of the paths forward and backward signals have to traverse in the network.
このような依存関係を学習する能力に影響を与える重要な要因の1つは、前方および後方の信号がネットワーク内で通過しなければならない経路の長さです。
The shorter these paths between any combination of positions in the input and output sequences, the easier it is to learn long-range dependencies [12].
入力配列と出力配列の任意の位置の組み合わせの間のこれらの経路が短ければ短いほど、長距離依存関係の学習が容易になります[12]。
Hence we also compare the maximum path length between any two input and output positions in networks composed of the different layer types.
そこで、異なる層タイプで構成されるネットワークにおいて、任意の2つの入出力位置間の最大経路長を比較します。

As noted in Table 1, a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations.
表1にあるように、セルフアテンションレイヤーは一定回数の逐次実行操作で全てのポジションを接続するのに対し、リカレントレイヤーはO(n)の逐次実行操作を必要とします。
In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence length n is smaller than the representation dimensionality d, which is most often the case with sentence representations used by state-of-the-art models in machine translations, such as word-piece [38] and byte-pair [31] representations.
計算量の点では、配列長nが表現次元dより小さい場合、自己注目層はリカレント層より高速である。これは、機械翻訳の最先端モデルで用いられる文表現、例えばワードピース［38］やバイトペア［31］表現で最もよく見られるケースである。
To improve computational performance for tasks involving very long sequences, self-attention could be restricted to considering only a neighborhood of size r in the input sequence centered around the respective output position.
非常に長いシーケンスを含むタスクの計算性能を向上させるために、自己注意を、それぞれの出力位置を中心とした入力シーケンスのサイズrの近傍のみを考慮するように制限することができる。
This would increase the maximum path length to O(n/r).
これにより、最大パス長はO(n/r)に増加する。
We plan to investigate this approach further in future work.
このアプローチについては、今後さらに調査していく予定です。

A single convolutional layer with kernel width k < n does not connect all pairs of input and output positions.
カーネル幅k＜nの単一の畳み込み層は、入力と出力の位置のすべてのペアを接続しない。
Doing so requires a stack of O(n/k) convolutional layers in the case of contiguous kernels, or O(logk(n)) in the case of dilated convolutions [18], increasing the length of the longest paths between any two positions in the network.
そのためには、連続カーネルの場合はO(n/k)、拡張コンボリューションの場合はO(logk(n))の畳み込み層を積み上げる必要があり[18]、ネットワーク内の任意の2位置間の最長経路の長さを増加させることになる。
Convolutional layers are generally more expensive than recurrent layers, by a factor of k.
畳み込み層は一般に、リカレント層よりもk倍ほど高価である。
Separable convolutions [6], however, decrease the complexity considerably, to O(k · n · d + n · d 2 ).
しかし、分離可能な畳み込み[6]は、複雑さを大幅に減らし、O(k - n - d + n - d 2 )とする。
Even with k = n, however, the complexity of a separable convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer, the approach we take in our model.
しかし、k = nであっても、分離可能な畳み込みの複雑さは、本モデルで採用している自己注意層とポイントワイズフィードフォワード層の組み合わせと同等です。

As side benefit, self-attention could yield more interpretable models.
副次的な効果として、自己アテンションによって、より解釈しやすいモデルが得られるかもしれません。
We inspect attention distributions from our models and present and discuss examples in the appendix.
私たちのモデルから注目分布を検査し、付録で例を提示して議論します。
Not only do individual attention heads clearly learn to perform different tasks, many appear to exhibit behavior related to the syntactic and semantic structure of the sentences.
個々のアテンションヘッドは明らかに異なるタスクを学習するだけでなく、多くは文の構文や意味構造に関連する行動を示すようです。

# 5. Training トレーニング

This section describes the training regime for our models.
このセクションでは、我々のモデルのためのトレーニング体制について説明する。

## 5.1. Training Data and Batching 学習データとバッチング

We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs.
約450万文対からなる標準的なWMT 2014英独データセットで学習を行いました。
Sentences were encoded using byte-pair encoding [3], which has a shared sourcetarget vocabulary of about 37000 tokens.
文はバイトペアエンコーディング[3]を用いて符号化され、約37000個のトークンからなるソースとターゲットの語彙が共有されています。
For English-French, we used the significantly larger WMT 2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece vocabulary [38].
英語-フランス語については、36Mの文からなる著しく大規模なWMT 2014 English-Frenchデータセットを使用し、トークンを32000ワード-ピースの語彙に分割しました[38]。
Sentence pairs were batched together by approximate sequence length.
文のペアは、おおよその配列の長さによってまとめられました。
Each training batch contained a set of sentence pairs containing approximately 25000 source tokens and 25000 target tokens.
各トレーニングバッチには、約25000のソーストークンと25000のターゲットトークンを含む文ペアのセットが含まれています。

## 5.2. Hardware and Schedule ハードウェアとスケジュール

We trained our models on one machine with 8 NVIDIA P100 GPUs.
8台のNVIDIA P100 GPUを搭載した1台のマシンでモデルの学習を行いました。
For our base models using the hyperparameters described throughout the paper, each training step took about 0.4 seconds.
本稿で紹介したハイパーパラメーターを用いたベースモデルでは、各トレーニングステップに約0.4秒を要しました。
We trained the base models for a total of 100,000 steps or 12 hours.
ベースモデルのトレーニングは、合計10万歩、12時間行いました。
For our big models,(described on the bottom line of table 3), step time was 1.0 seconds.
表3の下段にあるような大きなモデルの場合、ステップタイムは1.0秒である。
The big models were trained for 300,000 steps (3.5 days).
大きなモデルは30万歩（3.5日）分学習させました。

## 5.3. Optimizer オプティマイザー

We used the Adam optimizer [20] with β1 = 0.9, β2 = 0.98 and  = 10−9 .
Adam optimizer [20] を使用し、β1 = 0.9, β2 = 0.98, = 10-9 としました。
We varied the learning rate over the course of training, according to the formula:
計算式に従って、トレーニングの過程で学習率を変化させた：

$$
\tag{3}
$$

This corresponds to increasing the learning rate linearly for the first warmup_steps training steps, and decreasing it thereafter proportionally to the inverse square root of the step number.
これは、最初のwarmup_stepsの学習ステップでは学習率を直線的に増加させ、それ以降はステップ数の逆平方根に比例して減少させることに相当します。
We used warmup_steps = 4000.
warmup_steps = 4000を使用しました。

## 5.4. Regularization 正規化

We employ three types of regularization during training:
学習時に3種類の正則化を採用しています：

### 5.4.1. Residual Dropout 残留ドロップアウト

We apply dropout [33] to the output of each sub-layer, before it is added to the sub-layer input and normalized.
各サブレイヤーの出力は、サブレイヤー入力に加算され正規化される前に、ドロップアウト[33]を適用しています。
In addition, we apply dropout to the sums of the embeddings and the positional encodings in both the encoder and decoder stacks.
また、エンコーダスタックとデコーダスタックの両方において、埋め込みと位置エンコーディングの和にドロップアウトを適用しています。
For the base model, we use a rate of Pdrop = 0.1.
ベースモデルでは、Pdrop=0.1のレートを使用しています。

### 5.4.2. Label Smoothing レーベルスムージング

During training, we employed label smoothing of value ls = 0.1 [36].
学習時には、ls = 0.1 [36]の値のラベルスムージングを採用した。
This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.
これは、モデルがより不確実であることを学習するため、複雑さを損ないますが、精度とBLEUスコアを向上させます。

# 6. Results 結果

## 6.1. Machine Translation 機械翻訳

On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4.The configuration of this model is listed in the bottom line of Table 3.
WMT 2014英語-ドイツ語翻訳タスクにおいて、big transformerモデル（表2のTransformer (big)）は、過去に報告された最高のモデル（アンサンブルを含む）を2.0 BLEU以上上回り、新しい最先端のBLEUスコア28.4を確立しました。このモデルの構成を表3の下段に記載します。
Training took 3.5 days on 8 P100 GPUs.
トレーニングは8台のP100 GPUで3.5日かかりました。
Even our base model surpasses all previously published models and ensembles, at a fraction of the training cost of any of the competitive models.
私たちのベースモデルでさえ、過去に発表されたすべてのモデルやアンサンブルを凌駕し、競合モデルの何分の一かのトレーニングコストで実現しました。

On the WMT 2014 English-to-French translation task, our big model achieves a BLEU score of 41.0, outperforming all of the previously published single models, at less than 1/4 the training cost of the previous state-of-the-art model.
WMT 2014の英語からフランス語への翻訳タスクにおいて、我々のビッグモデルはBLEUスコア41.0を達成し、過去に発表されたすべての単一モデルを凌駕し、以前の最先端モデルの1/4以下の学習コストで達成しました。
The Transformer (big) model trained for English-to-French used dropout rate Pdrop = 0.1, instead of 0.3.For the base models, we used a single model obtained by averaging the last 5 checkpoints, which were written at 10-minute intervals.
ベースモデルには、10分間隔で書き込まれた直近の5つのチェックポイントを平均化することで得られる1つのモデルを使用し、英仏用に学習したTransformer（大）モデルは、ドロップアウト率Pdrop＝0.3ではなく、0.1でした。

For the big models, we averaged the last 20 checkpoints.
大型モデルについては、直近20回のチェックポイントを平均化しました。
We used beam search with a beam size of 4 and length penalty α = 0.6 [38].
ビームサイズ4、長さペナルティα=0.6 [38]のビームサーチを使用しました。
These hyperparameters were chosen after experimentation on the development set.
これらのハイパーパラメータは、開発セットで実験した後に選択されました。
We set the maximum output length during inference to input length + 50, but terminate early when possible [38].
推論中の最大出力長を入力長＋50に設定するが、可能な限り早期に終了させる[38]。

Table 2 summarizes our results and compares our translation quality and training costs to other model architectures from the literature.
表2に結果をまとめ、翻訳品質とトレーニングコストを文献にある他のモデルアーキテクチャと比較します。
We estimate the number of floating point operations used to train a model by multiplying the training time, the number of GPUs used, and an estimate of the sustained single-precision floating-point capacity of each GPU 5 .
トレーニング時間，使用した GPU の数，各 GPU の持続的な単精度浮動小数点演算能力の推定値 5 を掛け合わせることで，モデルのトレーニングに使用した浮動小数点演算の数を推定した．

## 6.2. Model Variations モデルバリエーション

To evaluate the importance of different components of the Transformer, we varied our base model in different ways, measuring the change in performance on English-to-German translation on the development set, newstest2013.
Transformerのさまざまなコンポーネントの重要性を評価するために、ベースモデルをさまざまに変化させ、開発セットであるnewstest2013の英語からドイツ語への翻訳性能の変化を測定しました。
We used beam search as described in the previous section, but no checkpoint averaging.
前項のビームサーチは使用したが、チェックポイントの平均化は行わなかった。
We present these results in Table 3.
これらの結果を表3に示します。

In Table 3 rows (A), we vary the number of attention heads and the attention key and value dimensions, keeping the amount of computation constant, as described in Section 3.2.2.
表3の行(A)では、3.2.2節で説明したように、計算量を一定にしたまま、注目ヘッドの数、注目キーと値の次元を変えています。
While single-head attention is 0.9 BLEU worse than the best setting, quality also drops off with too many heads.
シングルヘッドアテンションはベストな設定よりも0.9BLEU悪いですが、ヘッド数が多すぎると品質も落ちます。

In Table 3 rows (B), we observe that reducing the attention key size dk hurts model quality.
表3の(B)の行では、注目キーサイズdkを小さくすると、モデルの品質が低下することが確認されている。
This suggests that determining compatibility is not easy and that a more sophisticated compatibility function than dot product may be beneficial.
このことから、互換性の判断は容易ではなく、ドットプロダクトよりも洗練された互換性関数が有効である可能性が示唆されます。
We further observe in rows (C) and (D) that, as expected, bigger models are better, and dropout is very helpful in avoiding over-fitting.
さらに、(C)と(D)の行では、予想通り、大きなモデルの方が優れており、ドロップアウトはオーバーフィッティングを避けるのに非常に有効であることがわかります。
In row (E) we replace our sinusoidal positional encoding with learned positional embeddings [9], and observe nearly identical results to the base model.
(E)の行では、正弦波位置エンコーディングを学習済み位置埋め込み[9]に置き換えていますが、ベースモデルとほぼ同じ結果が得られています。

## 6.3. English Constituency イギリスの選挙区

Parsing To evaluate if the Transformer can generalize to other tasks we performed experiments on English constituency parsing.
構文解析 Transformerが他のタスクに汎化できるかどうかを評価するために、英語の構文解析の実験を行った。
This task presents specific challenges: the output is subject to strong structural constraints and is significantly longer than the input.
この課題では、出力が構造的に強い制約を受け、入力よりも大幅に長いという特殊な問題があります。
Furthermore, RNN sequence-to-sequence models have not been able to attain state-of-the-art results in small-data regimes [37].
さらに、RNNのsequence-to-sequenceモデルは、小さなデータ領域では最先端の結果を達成することができませんでした[37]。

We trained a 4-layer transformer with dmodel = 1024 on the Wall Street Journal (WSJ) portion of the Penn Treebank [25], about 40K training sentences.
Penn Treebank [25]のWall Street Journal (WSJ) 部分、約40Kの訓練文に対して、dmodel = 1024の4層変換器を訓練しました。
We also trained it in a semi-supervised setting, using the larger high-confidence and BerkleyParser corpora from with approximately 17M sentences [37].
また、約1700万文からなる大規模な高信頼度コーパスとBerkleyParserコーパス[37]を用いて、半教師付き設定での学習も行いました。
We used a vocabulary of 16K tokens for the WSJ only setting and a vocabulary of 32K tokens for the semi-supervised setting.
WSJのみの設定では16Kの語彙を、半教師付き設定では32Kの語彙を使用しました。

We performed only a small number of experiments to select the dropout, both attention and residual (section 5.4), learning rates and beam size on the Section 22 development set, all other parameters remained unchanged from the English-to-German base translation model.
セクション22の開発セットで、ドロップアウト、注意と残差の両方（セクション5.4）、学習率、ビームサイズを選択する実験を少数だけ行い、他のすべてのパラメータは英独ベース翻訳モデルから変更しませんでした。
During inference, we increased the maximum output length to input length + 300.
推論中は、最大出力長を入力長＋300に増やしました。
We used a beam size of 21 and α = 0.3 for both WSJ only and the semi-supervised setting.
WSJのみと半教師付き設定の両方で、ビームサイズ21、α=0.3を使用しました。

Our results in Table 4 show that despite the lack of task-specific tuning our model performs surprisingly well, yielding better results than all previously reported models with the exception of the Recurrent Neural Network Grammar [8].
表4の結果から、タスクに特化したチューニングがないにもかかわらず、本モデルの性能は驚くほど高く、Recurrent Neural Network Grammar [8]を除くすべての既報モデルよりも良好な結果が得られていることがわかります。

In contrast to RNN sequence-to-sequence models [37], the Transformer outperforms the BerkeleyParser [29] even when training only on the WSJ training set of 40K sentences.
RNNのsequence-to-sequenceモデル[37]とは対照的に、Transformerは、40K文のWSJトレーニングセットのみでトレーニングした場合でも、BerkeleyParser[29]よりも優れた性能を発揮しています。

# 7. Conclusion 結論

In this work, we presented the Transformer, the first sequence transduction model based entirely on attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.
本研究では、エンコーダー・デコーダーアーキテクチャで最もよく使われるリカレント層を多頭の自己注意に置き換えた、完全に注意に基づく最初の配列変換モデルであるトランスフォーマーを発表しました。

For translation tasks, the Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers.
翻訳タスクの場合、Transformerはリカレント層や畳み込み層に基づくアーキテクチャよりも大幅に速く学習させることができます。
On both WMT 2014 English-to-German and WMT 2014 English-to-French translation tasks, we achieve a new state of the art.
WMT 2014 英語からドイツ語、WMT 2014 英語からフランス語の両翻訳タスクにおいて、新しい状態を達成しました。
In the former task our best model outperforms even all previously reported ensembles.
前者のタスクでは、我々の最良のモデルは、これまでに報告されたすべてのアンサンブルを凌駕しています。

We are excited about the future of attention-based models and plan to apply them to other tasks.
私たちは、アテンションベースモデルの将来性に期待しており、他のタスクにも応用していく予定です。
We plan to extend the Transformer to problems involving input and output modalities other than text and to investigate local, restricted attention mechanisms to efficiently handle large inputs and outputs such as images, audio and video.
今後は、テキスト以外の入出力モダリティを含む問題にTransformerを拡張し、画像、音声、動画などの大規模な入出力を効率的に処理するための局所的で制限された注意メカニズムを研究する予定である。
Making generation less sequential is another research goals of ours.
また、世代交代をしにくくすることも、私たちの研究目標です。

The code we used to train and evaluate our models is available at https://github.com/ tensorflow/tensor2tensor.
モデルの訓練と評価に使用したコードは、https://github.com/ tensorflow/tensor2tensorで入手できます。
