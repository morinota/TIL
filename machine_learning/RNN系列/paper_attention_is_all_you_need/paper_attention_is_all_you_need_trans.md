## link リンク

- https://arxiv.org/abs/1706.03762 https://arxiv.org/abs/1706.03762

## title タイトル

Attention Is All You Need
アテンション・イズ・オール・ユー・ニード

## abstract アブストラクト

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration.
支配的な配列の伝達モデルは、エンコーダー・デコーダー構成の複雑なリカレントまたは畳み込みニューラルネットワークをベースにしています。
The best performing models also connect the encoder and decoder through an attention mechanism.
また、性能の良いモデルでは、エンコーダーとデコーダーをアテンション機構で接続しています。
We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.
私たちは、注意のメカニズムにのみ基づき、再帰や畳み込みを完全に排除した新しいシンプルなネットワークアーキテクチャ「トランスフォーマー」を提案します。
Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.
2つの機械翻訳タスクで実験した結果、これらのモデルは、並列化可能で訓練に要する時間が大幅に短縮される一方で、品質が優れていることがわかりました。
Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU.
本モデルは、WMT 2014の英語からドイツ語への翻訳タスクで28.4 BLEUを達成し、アンサンブルを含む既存の最良結果を2 BLEU以上上回った。
On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature.
WMT 2014の英仏翻訳タスクにおいて、我々のモデルは、8台のGPUで3.5日間学習した後、新しい単一モデルの最新BLEUスコア41.8を確立しました（文献にある最高のモデルの学習コストのごく一部です）。
We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.
我々は、Transformerが他のタスクにうまく汎化することを、大規模な訓練データと限られた訓練データの両方で英語の構成語構文解析にうまく適用することによって示す。

# Introduction 序章

Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation [35, 2, 5].
リカレントニューラルネットワーク、特に長短期記憶型 [13] とゲート型リカレント [7] ニューラルネットワークは、言語モデリングや機械翻訳などのシーケンスモデリングやトランスダクション問題における最先端のアプローチとして確固たる地位を築いている [35, 2, 5].
Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures [38, 24, 15].
その後、リカレント言語モデルやエンコーダ・デコーダ・アーキテクチャの限界に挑戦する数多くの努力が続けられている[38, 24, 15]。

Recurrent models typically factor computation along the symbol positions of the input and output sequences.
リカレントモデルは、通常、入力と出力シーケンスのシンボル位置に沿って計算を行う。
Aligning the positions to steps in computation time, they generate a sequence of hidden states ht, as a function of the previous hidden state ht−1 and the input for position t.
位置を計算時間のステップに合わせ、前の隠れ状態ht-1と位置tの入力の関数として、一連の隠れ状態htを生成する。
This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples.
この本質的に逐次的な性質は、トレーニング例内での並列化を妨げます。これは、メモリ制約により例間でのバッチ処理が制限されるため、シーケンス長が長くなるにつれて重要になります。
Recent work has achieved significant improvements in computational efficiency through factorization tricks [21] and conditional computation [32], while also improving model performance in case of the latter.
最近の研究では、因数分解のトリック[21]や条件付き計算[32]によって計算効率の大幅な向上を達成し、後者の場合はモデルの性能も向上しています。
The fundamental constraint of sequential computation, however, remains.
しかし、逐次計算の基本的な制約が残っています。

Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences [2, 19].
注意メカニズムは、様々なタスクにおける説得力のあるシーケンスモデリングや伝達モデルに不可欠な要素となっており、入力シーケンスや出力シーケンスにおける距離に関係なく依存関係をモデリングすることができます[2, 19]。
In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network.
しかし、一部の事例[27]を除いて、このような注意メカニズムはリカレントネットワークと組み合わせて使用されている。

In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.
本研究では、再帰性を排除し、代わりに入力と出力の間のグローバルな依存関係を描く注意メカニズムに完全に依存するモデルアーキテクチャであるTransformerを提案します。
The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.
Transformerは、大幅に並列化することができ、8つのP100 GPUでわずか12時間の学習で、翻訳品質の新たな境地に達することができます。

# Background その背景

The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU [16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building block, computing hidden representations in parallel for all input and output positions.
逐次計算を減らすという目標は、Extended Neural GPU [16], ByteNet [18], ConvS2S [9]の基礎にもなっています。これらはすべて、畳み込みニューラルネットワークを基本構成要素として、すべての入力と出力位置に対して並行して隠れ表現を計算しています。
In these models, the number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet.
これらのモデルでは、任意の2つの入出力位置からの信号を関連付けるために必要な演算数は、位置間の距離に応じて、ConvS2Sでは線形に、ByteNetでは対数的に増加する。
This makes it more difficult to learn dependencies between distant positions [12].
そのため、離れた位置同士の依存関係を学習することが難しくなっています[12]。
In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as described in section 3.2.
Transformerでは、注意の重み付けされた位置が平均化されるため、有効解像度が低下する代償として、この操作は一定の回数に抑えられますが、この効果は3.2節で述べたように、マルチヘッドアテンションで打ち消されています。

Self-attention, sometimes called intra-attention is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence.
自己注意（イントラ注意と呼ばれることもある）は、1つの配列の異なる位置を関連付け、配列の表現を計算するための注意機構である。
Self-attention has been used successfully in a variety of tasks including reading comprehension, abstractive summarization, textual entailment and learning task-independent sentence representations [4, 27, 28, 22].
自己注意は、読解、抽象的要約、テキストの含意、タスクに依存しない文表現の学習など、さまざまなタスクでうまく利用されている[4, 27, 28, 22]．

End-to-end memory networks are based on a recurrent attention mechanism instead of sequencealigned recurrence and have been shown to perform well on simple-language question answering and language modeling tasks [34].
エンドツーエンドメモリーネットワークは、配列に沿った再帰性ではなく、再帰性注意メカニズムに基づいており、単純な言語の質問応答や言語モデリングタスクで優れた性能を示すことが示されている[34]。

To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequencealigned RNNs or convolution.
しかし、私たちの知る限り、Transformerは、配列整列したRNNや畳み込みを使用せずに、入力と出力の表現を計算するために、完全に自己注意に依存する最初のトランスダクションモデルです。
In the following sections, we will describe the Transformer, motivate self-attention and discuss its advantages over models such as [17, 18] and [9].
以下のセクションでは、Transformerについて説明し、自己注意を動機付け、[17, 18]や[9]のようなモデルに対する優位性を議論することにする。

# Model Architecture モデル・アーキテクチャ

Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35].
競合する神経配列伝達モデルの多くは、エンコーダ-デコーダ構造を持っている [5, 2, 35]．
Here, the encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence of continuous representations z = (z1, ..., zn).
ここで、エンコーダは、入力された記号表現列（x1、・・・、xn）を連続表現列z＝（z1、・・・、zn）にマッピングする。
Given z, the decoder then generates an output sequence (y1, ..., ym) of symbols one element at a time.
zが与えられると、次にデコーダはシンボルの出力シーケンス（y1、...、ym）を一度に1要素ずつ生成する。
At each step the model is auto-regressive [10], consuming the previously generated symbols as additional input when generating the next.
各ステップにおいて、モデルは自動回帰的であり[10]、次のシンボルを生成する際に、以前に生成されたシンボルを追加入力として消費します。

The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1, respectively.
Transformerは、図1の左半分と右半分にそれぞれ示すように、エンコーダーとデコーダーの両方に、積層自己アテンションとポイントワイズ完全接続層を使用するこの全体的なアーキテクチャに従います。

## Encoder and Decoder Stacks 

### Encoder: エンコーダー

The encoder is composed of a stack of N = 6 identical layers.
エンコーダは、N＝6個の同一の層を積み重ねたものである。
Each layer has two sub-layers.
各レイヤーには2つのサブレイヤーがあります。
The first is a multi-head self-attention mechanism, and the second is a simple, positionwise fully connected feed-forward network.
1つ目は、多頭の自己アテンション機構、2つ目は、位置的に完全接続されたシンプルなフィードフォワードネットワークです。
We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1].
2つのサブレイヤーそれぞれの周囲に残留接続[11]を採用し、その後、レイヤー正規化[1]を行います。
That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself.
つまり、各サブレイヤーの出力はLayerNorm(x + Sublayer(x))となり、Sublayer(x)はサブレイヤー自身が実装する関数である。
To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512.
このような残差接続を容易にするため、埋め込み層だけでなく、モデルのすべてのサブ層は、dmodel = 512の次元の出力を生成します。

### Decoder: デコーダー

The decoder is also composed of a stack of N = 6 identical layers.
また、デコーダはN＝6個の同一の層を積み重ねることで構成されています。
In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack.
デコーダは、各エンコーダ層の2つのサブレイヤに加えて、エンコーダスタックの出力に対してマルチヘッドアテンションを実行する第3のサブレイヤを挿入する。
Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization.
エンコーダーと同様に、各サブレイヤーの周辺に残差接続を採用し、その後レイヤー正規化を行います。
We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions.
また、デコーダスタックのセルフアテンションサブレイヤーを変更し、ポジションが後続のポジションにアテンションするのを防ぐ。
This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.
このマスキングは、出力埋め込みが1位置分オフセットされていることと相まって、位置iの予測はiより小さい位置の既知の出力にのみ依存できることを保証します。

## Attention アテンション

An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.
アテンション機能は、クエリとキーと値のペアのセットを出力にマッピングするものとして記述することができ、クエリ、キー、値、および出力はすべてベクトルである。
The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.
出力は値の重み付き合計として計算され、各値に割り当てられた重みは、対応するキーとクエリの互換性関数によって計算される。

### Scaled Dot-Product Attention スケールドドットプロダクトアテンション

We call our particular attention "Scaled Dot-Product Attention" (Figure 2).
私たちは、このこだわりを「スケールドットプロダクトアテンション」と呼んでいます（図2）。
The input consists of queries and keys of dimension dk, and values of dimension dv.
入力はクエリーと次元dkのキー、次元dvの値で構成される。
We compute the dot products of the query with all keys, divide each by √ dk, and apply a softmax function to obtain the weights on the values.
クエリとすべてのキーのドット積を計算し、それぞれを√dkで割り、ソフトマックス関数を適用して値の重みを求める。

In practice, we compute the attention function on a set of queries simultaneously, packed together into a matrix Q.
実際には、行列Qにまとめられたクエリの集合に対して同時に注意関数を計算する。
The keys and values are also packed together into matrices K and V .
また、キーとバリューは、マトリックスKとVにまとめられている。
We compute the matrix of outputs as:
として、出力の行列を計算する：

$$
Attention
$$

The two most commonly used attention functions are additive attention [2], and dot-product (multiplicative) attention.
最もよく使われる注意機能は、加法注意[2]とドットプロダクトア注意（乗法注意）の2つです。
Dot-product attention is identical to our algorithm, except for the scaling factor of √ 1 dk .
ドットプロダクトアテンションは、スケーリングファクターが√ 1 dkであることを除けば、我々のアルゴリズムと同じである。
Additive attention computes the compatibility function using a feed-forward network with a single hidden layer.
付加的注意は、1つの隠れ層を持つフィードフォワードネットワークを使用して互換性関数を計算します。
While the two are similar in theoretical complexity, dot-product attention is much faster and more space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code.
両者は理論的な複雑さでは似ていますが、高度に最適化された行列乗算コードを用いて実装できるため、実際にはドットプロダクトアテンションの方がはるかに高速でスペース効率に優れています。

While for small values of dk the two mechanisms perform similarly, additive attention outperforms dot product attention without scaling for larger values of dk [3].
dkの値が小さいうちは2つの機構は同様の性能を発揮するが、dkの値が大きくなると加法的注意はスケーリングなしでドット積注意に勝る[3]。
We suspect that for large values of dk, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients 4 .
dkの値が大きい場合、ドット積の大きさが大きくなり、ソフトマックス関数の勾配が極端に小さくなる領域に押し込まれるのではないかと推測される4 。
To counteract this effect, we scale the dot products by √ 1 dk .
この効果を打ち消すために、ドットプロダクトを √ 1 dk だけスケーリングします。

### Multi-Head Attention マルチヘッドアテンション

Instead of performing a single attention function with dmodel-dimensional keys, values and queries, we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections to dk, dk and dv dimensions, respectively.
dmodel次元のキー、値、クエリで単一の注意機能を実行する代わりに、クエリ、キー、値をそれぞれdk、dk、dv次元に異なる、学習済みの線形投影でh回行うことが有益であることがわかった。
On each of these projected versions of queries, keys and values we then perform the attention function in parallel, yielding dv-dimensional output values.
これらの投影されたクエリ、キー、値のそれぞれに対して、注意機能を並行して実行し、dv次元の出力値を得ます。
These are concatenated and once again projected, resulting in the final values, as depicted in Figure 2.
これを連結して再度投影すると、図2に示すような最終的な値が得られる。

Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.
マルチヘッドアテンションは、モデルが異なる位置の異なる表現部分空間からの情報に共同してアテンションすることを可能にします。
With a single attention head, averaging inhibits this.
シングルアテンションヘッドでは、平均化することでこれを抑制しています。

$$
\tag{2}
$$

Where the projections are parameter matrices W Q i ∈ R dmodel×dk , W K i ∈ R dmodel×dk , WV i ∈ R dmodel×dv and WO ∈ R hdv×dmodel .
ここで、投影はパラメータ行列W Q i∈R dmodel×dk 、W K i∈R dmodel×dk 、WV i∈R dmodel×dv 、WO∈R hdv×dmodel とする。

In this work we employ h = 8 parallel attention layers, or heads.
この作品では、h = 8個の並列注意層（ヘッド）を採用しています。
For each of these we use dk = dv = dmodel/h = 64.
それぞれ、dk＝dv＝dmodel/h＝64としています。
Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality.
各ヘッドの次元が小さくなるため、総計算コストは、完全な次元を持つシングルヘッドアテンションのものと同様です。

### Applications of Attention in our Model アテンションの応用モデル

The Transformer uses multi-head attention in three different ways:
トランスフォーマーは、3種類の方法でマルチヘッドアテンションを使用します：

- In "encoder-decoder attention" layers, the queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder. This allows every position in the decoder to attend over all positions in the input sequence. This mimics the typical encoder-decoder attention mechanisms in sequence-to-sequence models such as [38, 2, 9]. エンコーダー・デコーダー・アテンション」層では、クエリーは前のデコーダー層から、メモリのキーと値はエンコーダーの出力からやってきます。 これにより、デコーダーの各ポジションは、入力シーケンスのすべてのポジションに出席することができます。 これは、[38, 2, 9]などの配列対配列モデルにおける典型的なエンコーダ・デコーダの注意メカニズムを模倣しています。

- The encoder contains self-attention layers. In a self-attention layer all of the keys, values and queries come from the same place, in this case, the output of the previous layer in the encoder. Each position in the encoder can attend to all positions in the previous layer of the encoder. エンコーダーには、自己アテンション層が含まれています。 自己アテンション層では、すべてのキー、値、クエリーは同じところから来る、この場合、エンコーダの前の層の出力である。 エンコーダーの各ポジションは、エンコーダーの前のレイヤーのすべてのポジションにアテンションすることができます。

- Similarly, self-attention layers in the decoder allow each position in the decoder to attend to all positions in the decoder up to and including that position. We need to prevent leftward information flow in the decoder to preserve the auto-regressive property. We implement this inside of scaled dot-product attention by masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections. See Figure 2. 同様に、デコーダの自己アテンション層は、デコーダ内の各位置が、その位置までのデコーダ内のすべての位置にアテンションすることを可能にします。 自動回帰性を維持するために、デコーダで左向きの情報フローを防ぐ必要があります。 ソフトマックスの入力のうち、不正な接続に対応するすべての値をマスクする（-∞に設定する）ことで、スケールドドットプロダクトアテンションの内部でこれを実装しています。 図2参照。

## Position-wise Feed-Forward Networks ポジションワイズフィードフォワードネットワーク

In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically.
注目のサブレイヤーに加え、エンコーダーとデコーダーの各レイヤーには完全接続のフィードフォワードネットワークが含まれており、各ポジションに別々に同じように適用されます。
This consists of two linear transformations with a ReLU activation in between.
これは、2つの線形変換とその間のReLU活性化で構成されています。

$$
\tag{2}
$$

While the linear transformations are the same across different positions, they use different parameters from layer to layer.
線形変換は異なる位置で同じですが、レイヤーごとに異なるパラメータを使用します。
Another way of describing this is as two convolutions with kernel size 1.
別の表現では、カーネルサイズ1の2つのコンボリューションとして表現されます。
The dimensionality of input and output is dmodel = 512, and the inner-layer has dimensionality df f = 2048.
入出力の次元はdmodel = 512、内層の次元はdf f = 2048である。

## Embeddings and Softmax エンベッディングとソフトマックス

Similarly to other sequence transduction models, we use learned embeddings to convert the input tokens and output tokens to vectors of dimension dmodel.
他の配列変換モデルと同様に、学習済み埋め込みを用いて、入力トークンと出力トークンを次元dmodelのベクトルに変換する。
We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities.
また、デコーダ出力を予測されるネクストトークン確率に変換するために、通常の学習済み線形変換とソフトマックス関数を使用します。
In our model, we share the same weight matrix between the two embedding layers and the pre-softmax linear transformation, similar to [30].
本モデルでは、[30]と同様に、2つの埋め込み層とプレソフトマックス線形変換の間で同じ重み行列を共有しています。
In the embedding layers, we multiply those weights by √ dmodel.
埋め込み層では、それらの重みに√dmodelを乗算する。

## Positional Encoding 位置エンコード

Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.
このモデルには再帰も畳み込みもないので、モデルがシーケンスの順序を利用するためには、シーケンス内のトークンの相対位置または絶対位置に関する何らかの情報を注入する必要があります。
To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks.
そのため、エンコーダとデコーダのスタックの底にある入力埋め込みに「位置エンコーディング」を追加します。
The positional encodings have the same dimension dmodel as the embeddings, so that the two can be summed.
位置エンコーディングはエンベッディングと同じ次元dmodelを持つので、両者を合計することができる。
There are many choices of positional encodings, learned and fixed [9].
位置エンコーディングには、学習型と固定型という多くの選択肢がある[9]。

In this work, we use sine and cosine functions of different frequencies:
本作品では、周波数の異なる正弦関数と余弦関数を使用しています：

$$
\tag{2.2}
$$

where pos is the position and i is the dimension.
ここで、posは位置、iは次元である。
That is, each dimension of the positional encoding corresponds to a sinusoid.
つまり、位置エンコードの各次元は、正弦波に対応する。
The wavelengths form a geometric progression from 2π to 10000 · 2π.
波長は2πから10000 - 2πまでの幾何学的な進行を形成しています。
We chose this function because we hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset k, P Epos+k can be represented as a linear function of P Epos.
この関数を選んだのは、任意の固定オフセットkに対して、P Epos+kはP Eposの一次関数として表現できるため、相対位置による出席をモデルが容易に学習できると仮定したからです。

We also experimented with using learned positional embeddings [9] instead, and found that the two versions produced nearly identical results (see Table 3 row (E)).
また、代わりに学習済みの位置埋め込み[9]を使う実験も行い、2つのバージョンでほぼ同じ結果が得られることがわかりました（表3の行（E）参照）。
We chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than the ones encountered during training.
正弦波バージョンを選択したのは、トレーニング中に遭遇したシーケンスよりも長いシーケンス長にモデルを外挿できるようにするためです。

# Why Self-Attention ♪ なぜ、セルフアテンションなのか

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

# Training トレーニング

This section describes the training regime for our models.
このセクションでは、我々のモデルのためのトレーニング体制について説明する。

## Training Data and Batching 学習データとバッチング

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

## Hardware and Schedule ハードウェアとスケジュール

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

## Optimizer オプティマイザー

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

## Regularization 正規化

We employ three types of regularization during training:
学習時に3種類の正則化を採用しています：

### Residual Dropout 残留ドロップアウト

We apply dropout [33] to the output of each sub-layer, before it is added to the sub-layer input and normalized.
各サブレイヤーの出力は、サブレイヤー入力に加算され正規化される前に、ドロップアウト[33]を適用しています。
In addition, we apply dropout to the sums of the embeddings and the positional encodings in both the encoder and decoder stacks.
また、エンコーダスタックとデコーダスタックの両方において、埋め込みと位置エンコーディングの和にドロップアウトを適用しています。
For the base model, we use a rate of Pdrop = 0.1.
ベースモデルでは、Pdrop=0.1のレートを使用しています。

### Label Smoothing レーベルスムージング

During training, we employed label smoothing of value ls = 0.1 [36].
学習時には、ls = 0.1 [36]の値のラベルスムージングを採用した。
This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.
これは、モデルがより不確実であることを学習するため、複雑さを損ないますが、精度とBLEUスコアを向上させます。

# Results 結果

## Machine Translation 機械翻訳

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

## Model Variations モデルバリエーション

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

## English Constituency イギリスの選挙区

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

# Conclusion 結論

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