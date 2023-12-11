## 0.1. link リンク

- https://arxiv.org/abs/2102.07619 https://arxiv.org/abs/2102.07619

## 0.2. title タイトル

MaskNet: Introducing Feature-Wise Multiplication to CTR Ranking Models by Instance-Guided Mask
MaskNet： インスタンス誘導型マスクによるCTRランキングモデルへの特徴的な乗算の導入

## 0.3. abstract アブストラクト

Click-Through Rate(CTR) estimation has become one of the most fundamental tasks in many real-world applications and it's important for ranking models to effectively capture complex high-order features.
**クリックスルー率(CTR)の推定は、多くの実世界のアプリケーションにおいて最も基本的なタスクの1つ**となっており、ランキングモデルにとって複雑な高次の特徴を効果的に捉えることが重要である.
Shallow feed-forward network is widely used in many state-of-the-art DNN models such as FNN, DeepFM and xDeepFM to implicitly capture high-order feature interactions.
浅いフィードフォワードネットワークは、FNN、DeepFM、xDeepFMなどの多くの最先端のDNNモデルで、高次の特徴の相互作用を暗黙のうちに捉えるために広く使われています。
However, some research has proved that addictive feature interaction, particular feed-forward neural networks, is inefficient in capturing common feature interaction.
しかし、中毒性のある特徴の相互作用、特にフィードフォワードニューラルネットワークは、共通の特徴の相互作用を捉えるには非効率であることが証明された研究もあります。
To resolve this problem, we introduce specific multiplicative operation into DNN ranking system by proposing instance-guided mask which performs element-wise product both on the feature embedding and feed-forward layers guided by input instance.
この問題を解決するために、我々は、入力インスタンスに導かれた特徴埋め込み層とフィードフォワード層の両方で要素ごとの積を行うインスタンスガイドマスクを提案し、DNNランキングシステムに特定の乗算演算を導入する。
We also turn the feed-forward layer in DNN model into a mixture of addictive and multiplicative feature interactions by proposing MaskBlock in this paper.
また、本論文でMaskBlockを提案することで、DNNモデルのフィードフォワード層を**加算型と乗算型の特徴量相互作用の混合型に**変えています。
MaskBlock combines the layer normalization, instance-guided mask, and feed-forward layer and it is a basic building block to be used to design new ranking model under various configurations.
MaskBlockは、レイヤーの正規化、インスタンスガイド付きマスク、フィードフォワード層を組み合わせたもので、様々な構成で新しいランキングモデルを設計するために使用される基本的なビルディングブロックである。
The model consisting of MaskBlock is called MaskNet in this paper and two new MaskNet models are proposed to show the effectiveness of MaskBlock as basic building block for composing high performance ranking systems.
本論文では、MaskBlockからなるモデルをMaskNetと呼び、MaskBlockが高性能なランキングシステムを構成するための基本構成要素としての有効性を示すために、2つの新しいMaskNetモデルを提案する。
The experiment results on three real-world datasets demonstrate that our proposed MaskNet models outperform state-of-the-art models such as DeepFM and xDeepFM significantly, which implies MaskBlock is an effective basic building unit for composing new high performance ranking systems.
3つの実世界データセットを用いた実験の結果、提案したMaskNetモデルはDeepFMやxDeepFMなどの最先端モデルを大幅に上回ることが実証され、MaskBlockが新しい高性能ランキングシステムを構成するための有効な基本構成単位であることを示唆している。

# 1. Introduction 序章

**Click-through rate (CTR) prediction** is to predict the probability of a user clicking on the recommended items.
クリックスルー率（CTR）予測は、ユーザが推薦アイテムをクリックする確率を予測するもの.
It plays important role in personalized advertising and recommender systems.
パーソナライズド広告やレコメンダーシステムにおいて重要な役割を担っている.
Many models have been proposed to resolve this problem such as Logistic Regression (LR) [16], Polynomial-2 (Poly2) [17], tree-based models [7], tensor-based models [12], Bayesian models [5], and Field-aware Factorization Machines (FFMs) [11].
この問題を解決するために、ロジスティック回帰（LR）[16]、多項式2（Poly2）[17]、木ベースモデル[7]、テンソルベースモデル[12]、ベイズモデル[5]、フィールドアウェア因子分解マシン（FFMs[11] など多くのモデルが提示されている。］
In recent years, employing DNNs for CTR estimation has also been a research trend in this field and some deep learning based models have been introduced such as Factorization-Machine Supported Neural Networks(FNN)[24], Attentional Factorization Machine (AFM)[3], wide & deep(W&D)[22], DeepFM[6], xDeepFM[13] etc.
近年、**CTR推定にDNNを採用することもこの分野の研究動向**であり、Factorization-Machine Supported Neural Networks（FNN）[24]、Attentional Factorization Machine（AFM）[3]、wide & deep（W&D）[22]、DeepFM（6）、xDeepFM（13）などの深層学習ベースのモデルが紹介されている.

Feature interaction is critical for CTR tasks and it’s important for ranking model to effectively capture these complex features.
**CTRタスクでは特徴量の相互作用が重要**であり、ランキングモデルはこれらの複雑な特徴を効果的に捉えることが重要である.
Most DNN ranking models such as FNN , W&D, DeepFM and xDeepFM use the shallow MLP layers to model high-order interactions in an implicit way and it’s an important component in current state-ofthe-art ranking systems.
FNN , W&D, DeepFM, xDeepFMなどのほとんどのDNNランキングモデルは、**浅いMLP層**(=Multi Layer Perceptron層=多層の全結合層)を使って高次の相互作用を暗黙のうちにモデル化しており、現在の最新鋭のランキングシステムにおいて重要な要素となっている.

However, Alex Beutel et.al [2] have proved that addictive feature interaction, particular feed-forward neural networks, is inefficient in capturing common feature crosses.
しかし、Alex Beutelら[2]は、中毒性のある特徴の相互作用、特にフィードフォワードニューラルネットワークは、共通の特徴の交差を捉えるのに効率が悪いことを証明しました。
They proposed a simple but effective approach named "latent cross" which is a kind of multiplicative interactions between the context embedding and the neural network hidden states in RNN model.
彼らは、RNNモデルにおけるコンテキスト埋め込みとニューラルネットワークの隠れ状態の間の一種の乗法的相互作用である"latent cross"というシンプルで効果的なアプローチを提案しました。
Recently, Rendle et.al’s work [18] also shows that a carefully configured dot product baseline largely outperforms the MLP layer in collaborative filtering.
最近、Rendleらの研究[18]でも、**協調フィルタリングにおいて、注意深く設定されたドット積ベースライン(MFのやつかな?)がMLP層を大きく上回ることが示されている**.
While a MLP can in theory approximate any function, they show that it is non-trivial to learn a dot product with an MLP and learning a dot product with high accuracy for a decently large embedding dimension requires a large model capacity as well as many training data.
MLPは理論的にはあらゆる関数を近似できるが、MLPでドットプロダクトを学習することは非自明であり、そこそこ大きな埋め込み次元に対して高い精度でドットプロダクトを学習するには、多くの学習データと同様に大きなモデル容量が必要であることを示している.
Their work also proves the inefficiency of MLP layer’s ability to model complex feature interactions.
また、彼らの研究は、**複雑な特徴量の相互作用をモデル化するMLP層の能力が非効率であることを証明している**.

Inspired by "latent cross"[2] and Rendle’s work [18], we care about the following question: Can we improve the DNN ranking systems by introducing specific multiplicative operation into it to make it efficiently capture complex feature interactions?
"latent cross"[2]とRendleの研究[18]に触発され、我々は以下の問いを気にしている： **DNNランキングシステムに特定の乗算演算を導入することで、複雑な特徴の相互作用を効率的に捉えられるように改善できないか**？

In order to overcome the problem of inefficiency of feed-forward layer to capture complex feature cross, we introduce a special kind of multiplicative operation into DNN ranking system in this paper.
feed-forward層(=データの流れが一方向である構造。データが行ったり来たり、あるいはループ等をしない。)が複雑な特徴量の交差を捉えるのに効率が悪いという問題を克服するために、本論文では**DNNランキングシステムに特殊な乗算演算を導入**した.
First, we propose an instance-guided mask performing elementwise production on the feature embedding and feed-forward layer.
まず、特徴量埋め込み層とフィードフォワード層に対して、**要素分解を行うinstance-guided mask**を提案する.(??)
The instance-guided mask utilizes the global information collected from input instance to dynamically highlight the informative elements in feature embedding and hidden layer in a unified manner.
instance-guitedマスクは、入力インスタンスから収集したグローバルな情報を利用し、特徴量埋込層と隠れ層の**情報量の多い要素を統一的に動的にハイライト**する.(情報量を集約している、必要な情報のみをフィルタリングしてるイメージ??)
There are two main advantages for adopting the instance-guided mask:
instance-guided maskを適用する事の利点は主に２つ:
firstly, the element-wise product between the mask and hidden layer or feature embedding layer brings multiplicative operation into DNN ranking system in unified way to more efficiently capture complex feature interaction.
第一に、マスクと隠れ層または特徴埋め込み層の間の要素ごとの積が、DNNランキングシステムに統一的な方法で乗算演算をもたらし、**複雑な特徴量の相互作用をより効率的に捕らえることができる**こと.
Secondly, it’s a kind of finegained bit-wise attention guided by input instance which can both weaken the influence of noise in feature embedding and MLP layers while highlight the informative signals in DNN ranking systems.
第二に、DNNランキングシステムにおいて**情報量の多い信号を強調**しながら、特徴量埋め込み層やMLP層における**ノイズの影響を弱めることができる**、入力インスタンスによって導かれる一種の細かいbit-wise attention(??Attention層??)であることである.

By combining instance-guided mask, a following feed-forward layer and layer normalization, MaskBlock is proposed by us to turn the commonly used feed-forward layer into a mixture of addictive and multiplicative feature interactions.
instance-guidedマスク、後続のfeed-forward層、レイヤー正規化を組み合わせることで、**一般的に用いられるfeed-forward層を加法的・乗法的な特徴量相互作用の混合に変えるMaskBlock**が私たちによって提案されている.
The instance-guided mask introduces multiplicative interactions and the following feedforward hidden layer aggregates the masked information in order to better capture the important feature interactions.
**instance-guidedマスクは乗算的な相互作用を導入**し、次のフィードフォワード隠れ層は、重要な特徴量の相互作用をよりよく捕らえるために、マスクされた情報を集約する.
While the layer normalization can ease optimization of the network.
レイヤー正規化は、ネットワークの最適化を容易にすることができますが。

MaskBlock can be regarded as a basic building block to design new ranking models under some kinds of configuration.
MaskBlockは、ある種の構成のもとで新しいランキングモデルを設計するための**基本的なビルディングブロック**とみなすことができる.
The model consisting of MaskBlock is called MaskNet in this paper and two new MaskNet models are proposed to show the effectiveness of MaskBlock as basic building block for composing high performance ranking systems.
本論文では、**MaskBlockからなるモデルをMaskNetと呼び**、MaskBlockが高性能なランキングシステムを構成するための基本構成要素としての有効性を示すために、2つの新しいMaskNetモデルを提案する:

The contributions of our work are summarized as follows:
本研究の貢献は以下のように要約される：

- (1) In this work, we propose an instance-guided mask performing element-wise product both on the feature embedding and feed-forward layers in DNN models. The global context information contained in the instance-guided mask is dynamically incorporated into the feature embedding and feed-forward layer to highlight the important elements. (1) 本論文では、DNNモデルの特徴量埋め込み層(=自然言語テキストをembeddingに変換する層のようなイメージ?:thinking:)とフィードフォワード層の両方において、**要素ごとの積を行うinstance-guidedマスク**を提案する. instance-guidedマスクに含まれるグローバルなコンテキスト情報を、特徴量埋め込み層とフィードフォワード層に動的に取り込み、重要な要素を強調することができる.

- (2) We propose a basic building block named MaskBlock which consists of three key components: instance-guided mask, a following feed-forward hidden layer and layer normalization module. In this way, we turn the widely used feed-forward layer of a standard DNN model into a mixture of addictive and multiplicative feature interactions. (2) instance-guidedマスク、feed-forward隠れ層、レイヤー正規化モジュールの**3つの主要componentsからなるMaskBlockという基本構成ブロックを提案**する. このようにして、標準的なDNNモデルの広く使われているフィードフォワード層を、**加法的・乗法的な特徴量の相互作用の混合に変える**.

- (3) We also propose a new ranking framework named MaskNet to compose new ranking system by utilizing MaskBlock as basic building unit. To be more specific, the serial MaskNet model and parallel MaskNet model are designed based on the MaskBlock in this paper. The serial rank model stacks MaskBlock block by block while the parallel rank model puts many MaskBlocks in parallel on a sharing feature embedding layer. (3) また、MaskBlockを基本構成単位として、新しいランキングシステムを構成するMaskNetという新しいランキングフレームワークを提案している. 具体的には、本論文では**MaskBlockをベースにシリアルMaskNetモデル、パラレルMaskNetモデルを設計している**. シリアルランクモデルでは、MaskBlockをブロックごとに積み重ね、パラレルランクモデルでは、多数のMaskBlockを共有する特徴量埋め込み層上に並列に配置する.

- (4) Extensive experiments are conduct on three real-world datasets and the experiment results demonstrate that our proposed two MaskNet models outperform state-of-the-art models significantly. The results imply MaskBlock indeed enhance DNN model’s ability of capturing complex feature interactions through introducing multiplicative operation into DNN models by instance-guided mask. (4) 3つの実世界データセットで大規模な実験を行い、提案する2つのMaskNetモデルが、最先端モデルを大幅に上回ることを実証した. その結果、MaskBlockは、**instance-guidedマスクによってDNNモデルに乗算演算を導入する**ことで、複雑な特徴量間の相互作用を捉えるDNNモデルの能力を確かに向上させることが示唆された.

The rest of this paper is organized as follows.
本稿の残りの部分は、以下のように構成されている.
Section 2 introduces some related works which are relevant with our proposed model.
第2節では、本提案モデルと関連性のあるいくつかの関連作品を紹介する.
We introduce our proposed models in detail in Section 3.
セクション3では、提案するモデルを詳しく紹介する.
The experimental results on three real world datasets are presented and discussed in Section 4.
3つの実世界データセットでの実験結果を示し、セクション4で議論する.
Section 5 concludes our work in this paper.
第5節では、本論文における我々の研究を締めくくる.

# 2. Related Work 関連作品

## 2.1. State-Of-The-Art CTR Models 最先端のCTRモデル

Many deep learning based CTR models have been proposed in recent years and it is the key factor for most of these neural network based models to effectively model the feature interactions.
近年、多くの深層学習ベースのCTRモデルが提案されていますが、これらのニューラルネットワークベースのモデルの多くにとって、**特徴量間の相互作用を効果的にモデル化することは重要な要素となっている**.

Factorization-Machine Supported Neural Networks (FNN)[24] is a feed-forward neural network using FM to pre-train the embedding layer.
FNN(Factorization-Machine Supported Neural Networks)[24]は、FMを用いて埋め込み層の事前学習を行うフィードフォワードニューラルネットワークです。
Wide & Deep Learning[22] jointly trains wide linear models and deep neural networks to combine the benefits of memorization and generalization for recommender systems.
Wide & Deep Learning[22]は、推薦システムのための記憶と汎化の利点を組み合わせるために、広い線形モデルと深いニューラルネットワークを共同で学習します。
However, expertise feature engineering is still needed on the input to the wide part of Wide & Deep model.
しかし、Wide & DeepモデルのWide部分への入力には、まだ専門的なフィーチャーエンジニアリングが必要である。
To alleviate manual efforts in feature engineering, DeepFM[6] replaces the wide part of Wide & Deep model with FM and shares the feature embedding between the FM and deep component.
DeepFM[6]は、feature engineeringの手作業を軽減するために、Wide & DeepモデルのWide部分をFMに置き換え、FMとDeepコンポーネント間で特徴量埋込みを共有する。

While most DNN ranking models process high-order feature interactions by MLP layers in implicit way, some works explicitly introduce high-order feature interactions by sub-network.
多くのDNNランキングモデルはMLP層によって高次特徴量相互作用を暗黙のうちに処理しているが、いくつかの作品はサブネットワークによる高次特徴量相互作用を明示的に導入している。
Deep & Cross Network (DCN)[21] efficiently captures feature interactions of bounded degrees in an explicit fashion.
Deep & Cross Network (DCN)[21]は、有界度の特徴的な相互作用を明示的に効率よく捉えることができます。
Similarly, eXtreme Deep Factorization Machine (xDeepFM) [13] also models the loworder and high-order feature interactions in an explicit way by proposing a novel Compressed Interaction Network (CIN) part.
同様に、eXtreme Deep Factorization Machine (xDeepFM) [13]も、新しいCompressed Interaction Network (CIN) 部分を提案することにより、低次と高次の特徴量相互作用を明示的にモデル化しています。
AutoInt[19] uses a multi-head self-attentive neural network to explicitly model the feature interactions in the low-dimensional space.
AutoInt[19]は、低次元空間における特徴量の相互作用を明示的にモデル化するために、multi-head self-attentive ニューラルネットワークを使用しています。
FiBiNET[9] can dynamically learn feature importance via the Squeeze-Excitation network (SENET) mechanism and feature interactions via bilinear function.
FiBiNET[9]は、Squeeze-Excitation network（SENET）メカニズムによる特徴量の重要度、バイリニア関数による特徴量の相互作用を動的に学習することができます。

## 2.2. Feature-Wise(=特徴量毎の??:thinking:) Mask Or Gating Feature-Wise Mask Or Gating（フィーチャーワイズ・マスク・オア・ゲーティング

Feature-wise mask or gating has been explored widely in vision [8, 20], natural language processing [4] and recommendation system[14, 15].
特徴量に応じたマスクやゲーティングは、CV[8, 20]、自然言語処理[4]、推薦システム[14, 15]などで広く研究されている。
For examples, Highway Networks [20] utilize feature gating to ease gradient-based training of very deep networks.
例えば、Highway Networks [20]は、非常に深いネットワークの勾配ベースのトレーニングを容易にするために特徴量ゲーティングを利用しています。
Squeezeand-Excitation Networks[8] recalibrate feature responses by explicitly multiplying each channel with learned sigmoidal mask values.
Squeezeand-Excitation Networks[8]は、各チャンネルに学習したシグモイドマスク値を明示的に乗算することで特徴量応答を再較正する。
Dauphin et al.[4] proposed gated linear unit (GLU) to utilize it to control what information should be propagated for predicting the next word in the language modeling task.
Dauphinら[4]は、言語モデリングタスクにおいて、次の単語を予測するために伝播させる情報を制御するために、ゲート線形ユニット（GLU）を提案し、これを利用している。(RNN系列のやつね...!)
Gating or mask mechanisms are also adopted in recommendation systems.
**推薦システムでは、gatingやmaskの仕組みも採用されています。**(ほうほう、Sequential推薦においてノイズ除去する為にattention weightをマスクする手法は読んだ事あるな...!:thinking:)
Ma et al.[15] propose a novel multi-task learning approach, Multi-gate Mixture-of-Experts (MMoE), which explicitly learns to model task relationships from data.
Maら[15]は、データからタスクの関係をモデル化することを明示的に学習する、新しいマルチタスク学習アプローチ、Multi-gate Mixture-of-Experts (MMoE) を提案している。
Ma et al.[14] propose a hierarchical gating network (HGN) to capture both the long-term and short-term user interests.
Maら[14]は、ユーザの長期的な興味と短期的な興味の両方を捉えるために、hierarchical gating network(HGN)を提案しています。
The feature gating and instance gating modules in HGN select what item features can be passed to the downstream layers from the feature and instance levels, respectively.
HGNのfeature gatingとinstance gatingモジュールは、それぞれfeatureレベルとinstanceレベルから下流層に渡すことができるアイテムの特徴量を選択します。(instanceってある一つのTraining exampleのことかな?:thinking:)

## 2.3. Normalization 正規化

Normalization techniques have been recognized as very effective components in deep learning.
正規化技術は、ディープラーニングにおいて非常に有効なcomponentとして認識されています。
Many normalization approaches have been proposed with the two most popular ones being BatchNorm [10] and LayerNorm [1] .
多くの正規化アプローチが提案されており、**最も一般的なものは BatchNorm [10] と LayerNorm [1] の2つ**である。(ほうほう...!:thinking:)
Batch Normalization (Batch Norm or BN)[10] normalizes the features by the mean and variance computed within a mini-batch.
バッチ正規化(Batch NormまたはBN)[10]は、**ミニバッチ内で計算された平均と分散によって特徴量を正規化**します。(=標準正規分布っぽくなるように値を揃えるってことかな:thinking:)
Another example is layer normalization (Layer Norm or LN)[1] which was proposed to ease optimization of recurrent neural networks.
また、リカレントニューラルネットワークの最適化を容易にするために提案されたレイヤー正規化(Layer NormまたはLN)[1]もその一例である。
Statistics of layer normalization are not computed across the 𝑁 samples in a mini-batch but are estimated in a layer-wise manner for each sample independently.
レイヤー正規化の統計は、ミニバッチの $N$ サンプル全体で計算されるのではなく、**各サンプルについて独立してlayer-wiseに**推定されます。
Normalization methods have shown success in accelerating the training of deep networks.
正規化手法は、**ディープネットワークの学習を加速させること**に成功しました。(学習効率の向上が主な目的なんだ...!:thinking:)

# 3. Our Proposed Model 私たちの提案するモデル

In this section, we first describe the feature embedding layer.
本節では、まず、特徴量埋め込み層について説明する。
Then the details of the instance-guided mask, MaskBlock and MaskNet structure we proposed will be introduced.
続いて、我々が提案したinstance-guidedマスク、MaskBlock、MaskNetの構造の詳細について紹介する。
Finally the log loss as a loss function is introduced.
最後に、損失関数としてのlog lossを紹介する。

## 3.1. Embedding Layer エンベデッドレイヤー

The input data of CTR tasks usually consists of sparse and dense features and the sparse features are mostly categorical type.
CTRタスクの入力データは通常、疎と密の特徴量で構成され、疎の特徴量は主にcategoricalである。
Such features are encoded as one-hot vectors which often lead to excessively high-dimensional feature spaces for large vocabularies.
このような特徴量は、**one-hotベクトルとして符号化される**ため、大規模な語彙の場合、過剰に高次元の特徴量空間となることが多い。(うんうん...!)
The common solution to this problem is to introduce the embedding layer.
この問題に対する一般的な解決策は、埋め込み層を導入することです。(うんうん、sparceなベクトルをdenceなベクトルに投影する、みたいなイメージ:thinking:)
Generally, the sparse input can be formulated as:
一般に、sparse入力は次のように定式化できる：

$$
\mathbf{x} = \[x_1, x_2, \cdots, x_f \]
$$

where $f$ denotes the number of fields, and 𝑥𝑖 ∈ R 𝑛 denotes a onehot vector for a categorical field with 𝑛 features and 𝑥𝑖 ∈ R 𝑛 is vector with only one value for a numerical field.
ここで、$f$ は特徴量の数を表し、$x_{i} \in \mathbb{R}^n$ $n$ 個の語彙を持つカテゴリカル特徴量に対するone-hotベクトル、$x_{j} \in \mathbb{R}$ はnumerical特徴量に対する唯一の値を持つベクトルを表す。
We can obtain feature embedding 𝑒𝑖 for one-hot vector 𝑥𝑖 via:
以下のように、one-hotベクトル $\mathbf{x}_i$ の特徴量埋め込み $\mathbf{e}_{i}$ を得ることができる:

$$
\mathbf{e}_{i} = W_{e} \mathbf{x}_{i}
\tag{2}
$$

where $W_e \in \mathbb{R}^{k \times n}$ is the embedding matrix of 𝑛 features and 𝑘 is the dimension of field embedding.
ここで、$W_e \in \mathbb{R}^{k \times n}$ は $n$ 次元の特徴量の埋め込み行列(i.e. projection matrix? :thinking:)、$k$ は特徴量埋め込みの次元数である。(projection matrixって各特徴量毎にユニークなのかな。もしくは共有なのかな。)
The numerical feature 𝑥𝑗 can also be converted into the same low-dimensional space by:
数値特徴量 $\mathbf{x}_{j}$ も、同じように低次元空間に変換(=linear projection:thinking:)することができる:
(わざわざスカラーを埋め込む必要があるのかな??:thinking:)

$$
\mathbf{e}_{j} = V_{j} \mathbf{x}_{j}
\tag{3}
$$

where 𝑉𝑗 ∈ R 𝑘 is the corresponding field embedding with size 𝑘.
ここで、$V_{j} \in \mathbb{R}^{k}$ はサイズ $k$ の対応する特徴量埋め込みである。

Through the aforementioned method, an embedding layer is applied upon the raw feature input to compress it to a low dimensional, dense real-value vector.
前述の方法により、入力された生の特徴量に対して埋め込み層を適用し、**低次元で密な実数値のベクトルに圧縮することができます**。
The result of embedding layer is a wide concatenated vector:
埋め込み層の結果は、幅の広い連結されたベクトルです:
(i.e. 列ベクトルを縦にconcatするってことかな?)

$$
V_{emb} = concat(\mathbf{e}_1, \mathbf{e}_2, \cdots, \mathbf{e}_i, \cdots, \mathbf{e}_{f})
\tag{4}
$$

where 𝑓 denotes the number of fields, and e𝑖 ∈ R 𝑘 denotes the embedding of one field.
ここで、$f$ は特徴量数を表し、$\mathbf{e}_i \in \mathbb{R}^{k}$ は1つの特徴量 $\mathbf{x}_i$ に対応する埋め込みを表します。
Although the feature lengths of input instances can be various, their embedding are of the same length 𝑓 × 𝑘, where 𝑘 is the dimension of field embedding.
入力インスタンスの各特徴量の長さは様々であるが、その埋め込みは同じ長さ $f \times k$ ($k$ は各特徴量埋め込みの次元数)である。($k$ は全ての特徴量で統一ってことかな。)

We use instance-guided mask to introduce the multiplicative operation into DNN ranking system and here the so-called "instance" means the feature embedding layer of current input instance in the following part of this paper.
本稿では、DNNのランキングシステムに乗算演算を導入するために、instance-guidedマスクを用いる。ここでいう「インスタンス」とは、本稿の以下の部分において、現在の入力インスタンスの特徴埋め込み層を指す。(=特徴量をdence vectorに埋め込んだ後のことを意味しますよ、って話か:thinking:)

## 3.2. Instance-Guided Mask インスタンス・ガイド・マスク

We utilize the global information collected from input instance by instance-guided mask to dynamically highlight the informative elements in feature embedding and feed-forward layer.
インスタンス誘導型マスクによって入力インスタンスから収集されたグローバルな情報を活用し、特徴量埋め込みとフィードフォワード層で情報量の多い要素を動的に強調します。
For feature embedding, the mask lays stress on the key elements with more information to effectively represent this feature.
特徴量埋め込みでは、この特徴量を効果的に表現するために、より多くの情報を持つ重要な要素に重点を置いているのが特徴です。(sparseからdenceへの変換:thinking:)
For the neurons in hidden layer, the mask helps those important feature interactions to stand out by considering the contextual information in the input instance.
隠れ層のニューロンにとって、マスクは、入力インスタンスの文脈情報(=特徴量間の共起性とか??)を考慮することで、重要な特徴の相互作用を際立たせるのに役立つ。
In addition to this advantage, the instance-guided mask also introduces the multiplicative operation into DNN ranking system to capture complex feature cross more efficiently.
この利点に加え、インスタンス誘導型マスクは、DNNランキングシステムに乗算演算を導入することで、複雑な特徴量間の交差をより効率的に捉えることができます。

![figure1]()

As depicted in Figure 1, two fully connected (FC) layers with identity function are used in instance-guided mask.
図1に示すように、インスタンスガイド型マスクでは、identity function(?)を持つ2つのfully connected(FC)層が使用される。
Notice that the input of instance-guided mask is always from the input instance, that is to say, the feature embedding layer.
**instance-guidedマスクの入力は常に入力インスタンスから、つまり特徴量埋め込み層からであることに注意**する。(ふむふむ...!)

The first FC layer is called "aggregation layer" and it is a relatively wider layer compared with the second FC layer in order to better collect the global contextual information in input instance.
第1FC層は"aggregation layer"と呼ばれ、入力インスタンスのグローバルな(=f個全ての特徴量の、って意味かな??:thinking:)コンテキスト情報をよりよく収集するために、第2FC層に比べて比較的広い層となっています。
The aggregation layer has parameters 𝑊𝑑1 and here 𝑑 denotes the 𝑑-th mask.
aggregation層はパラメータ $W_{d1}$ を持ち、ここで $d$ は $d$ 番目のマスクを表す。(aggregation層は$d =1$ってことかな??)
For feature embedding and different MLP layers, we adopt different instance-guided mask owning its parameters to learn to capture various information for each layer from input instance.
特徴埋め込みと異なるMLP層には、入力インスタンスから各層に様々な情報を取り込むための学習を行うため、そのパラメータに異なるインスタンスガイド付きマスクを採用しています。

The second FC layer named "projection layer" reduces dimensionality to the same size as feature embedding layer 𝑉𝑒𝑚𝑏 or hidden layer 𝑉ℎ𝑖𝑑𝑑𝑒𝑛 with parameters 𝑊𝑑2, Formally,
"projection layer"と名付けられた2番目のFC層はパラメータ $W_{d2}$ を持ち、特徴量 $V_{emb}$ または隠れ層 $V_{hidden}$ と同じ大きさに次元を圧縮す。
Instance-guidedマスクの動きを数式で表すと以下:

$$
V_{mask} = W_{d2}(Relu(W_{d1} V_{emb} + \beta_{d1})) + \beta_{d2}
\tag{5}
$$

(やってる事は中間層1つのfully-connected layerか...!特徴量埋め込みの線形変換というか...!:thinking:)

where 𝑉𝑒𝑚𝑏 ∈ R 𝑚=𝑓 ×𝑘 refers to the embedding layer of input instance,𝑊𝑑1 ∈ R 𝑡×𝑚 and𝑊𝑑2 ∈ R 𝑧×𝑡 are parameters for instanceguided mask, 𝑡 and 𝑧 respectively denotes the neural number of aggregation layer and projection layer, 𝑓 denotes the number of fields and 𝑘 is the dimension of field embedding.
ここで、$V_{emb} \in \mathbb{R}^{m = f \times k}$ は入力インスタンスの埋め込み層、$W_{d1} \in \mathbb{R}^{t \times m}, W_{d2} \in \mathbb{R}^{z \times t}$ はinstance-guidedマスク用のパラメータを指す。$t$ はaggregation層、$z$ はprojection層のニューラル数 (i.e 出力されるベクトルの次元数:thinking:) を示す。$f$ は特徴量数、$k$ は特徴量埋め込みの次元数をそれぞれ表す。
𝛽𝑑1 ∈ R 𝑡×𝑚 and 𝛽𝑑2 ∈ R 𝑧×𝑡 are learned bias of the two FC layers.
$\beta_{d1} \in \mathbb{R}^{t \times m}, \beta_{d2} \in \mathbb{R}^{z \times t}$、𝛽ᵅ2∈R𝑡は2つのFC層の学習バイアス。(たぶん誤植なのかな?? バイアスはそれぞれ$t$次元と$z$ 次元のベクトルだと思う:thinking:)
Notice here that the aggregation layer is usually wider than the projection layer because the size of the projection layer is required to be equal to the size of feature embedding layer or MLP layer.
ここで注目したいのは、projection層のサイズは特徴量埋め込み層やMLP層のサイズと等しいことが要求されるため、aggregation層は通常、projection層よりも広いことです。
So we define the size 𝑟 = 𝑡/𝑧 as reduction ratio which is a hyper-parameter to control the ratio of neuron numbers of two layers.
そこで、2つの層のニューロン数 (=tとz) の比率を制御するハイパーパラメータであるreduction ratioとして、サイズ $r = t/z$ を定義することにします。

Element-wise product is used in this work to incorporate the global contextual information aggregated by instance-guided mask into feature embedding or hidden layer as following:
本作品では、instance-guidedマスクによって集約されたグローバルな文脈情報を、以下のように特徴量埋め込みや隠れ層に取り込むために、element-wise積(i.e. アダマール積?)を使用している:

$$
V_{maskedEMB} = V_{mask} \odot V_{emb}
\\
V_{maskedHID} = V_{mask} \odot V_{hidden}
\tag{6}
$$

where V𝑒𝑚𝑏 denotes embedding layer and Vℎ𝑖𝑑𝑑𝑒𝑛 means the feedforward layer in DNN model, ⊙ means the element-wise production between two vectors as follows:
ここで、$V_{emb}$ は埋め込み層、$V_{hidden}$ はDNNモデルにおけるフィードフォワード層を表し、$\odot$ は以下のように2つのベクトル間の要素ごとの生成を意味します：

$$
V_i \odot V_j = [V_{i1} \cdot V_{j1}, \cdots, V_{iu} \cdot V_{ju}]
\tag{7}
$$

here 𝑢 is the size of vector 𝑉𝑖 and 𝑉𝑗
ここで、$u$はベクトルV_iとV_jの次元数。

The instance-guided mask can be regarded as a special kind of bitwise attention or gating mechanism which uses the global context information contained in input instance to guide the parameter optimization during training.
instance-guidedマスクは、入力インスタンスに含まれるグローバルなコンテキスト情報を用いて、学習中のパラメータ最適化をガイドする特殊な種類のbit-wise attention (=特徴量埋め込みの各要素を1つの値と見做した系列データみたいな??:thinking:) またはgating mechanism(ゲート機構)とみなすことができます。
The bigger value in𝑉𝑚𝑎𝑠𝑘 implies that the model dynamically identifies an important element in feature embedding or hidden layer.
$V_{mask}$ の値が大きいほど、モデルが特徴量埋め込みや隠れ層の重要な要素を動的に(?=ガッツリ、みたいな意味合い??)識別していることを意味する。
It is used to boost the element in vector 𝑉𝑒𝑚𝑏 or𝑉ℎ𝑖𝑑𝑑𝑒𝑛.
ベクトル $V_{emb}$ または $V_{hidden}$ の要素をboostする(??)ために使用されるものである。
On the contrary, small value in𝑉𝑚𝑎𝑠𝑘 will suppress the uninformative elements or even noise by decreasing the values in the corresponding vector 𝑉𝑒𝑚𝑏 or 𝑉ℎ𝑖𝑑𝑑𝑒𝑛.
逆に $V_{mask}$ の値が小さいと、対応するベクトル $V_{emb}$ や $V_{hidden}$ の値が小さくなり(まあアダマール積をとるしなぁ...:thinking:)、情報量の少ない要素やノイズが抑制されます。

The two main advantages in adopting the instance-guided mask are:
instance-guidedマスクの採用により2つの主な利点があります:
firstly, the element-wise product between the mask and hidden layer or feature embedding layer brings multiplicative operation into DNN ranking system in unified way to more efficiently capture complex feature interaction.
第一に、マスクと隠れ層または特徴量埋め込み層の間の要素ごとの積(=アダマール積)が、DNNランキングシステムに統一的な方法で乗算演算をもたらし、複雑な特徴の相互作用をより効率的に捕らえることができることです。
Secondly, this kind of fine-gained bit-wise attention guided by input instance can both weaken the influence of noise in feature embedding and MLP layers while highlight the informative signals in DNN ranking systems.
第二に、入力インスタンスによって導かれるこのような細かいbit-wise(element-wiseって言っても同義なのかな??:thinking:)のattentionは、特徴量埋め込みとMLP層における**ノイズの影響を弱め**、DNNランキングシステムにおける**有益な信号を強調する**ことができます。

## 3.3. MaskBlock MaskBlock

To overcome the problem of the inefficiency of feed-forward layer to capture complex feature interaction in DNN models, we propose a basic building block named MaskBlock for DNN ranking systems in this work, as shown in Figure 2 and Figure 3.
DNNモデルにおける複雑な特徴量の相互作用を捉えるにはfeed forward層が非効率であるという問題を克服するために、本研究では図2および図3に示すようなDNNランキングシステムのためのMaskBlockという基本構成ブロックを提案します。
The proposed MaskBlock consists of three key components: layer normalization module ,instance-guided mask, and a feed-forward hidden layer.
提案するMaskBlockは、レイヤー正規化モジュール、instance-guidedマスク、feed-forward隠れ層の**3つの主要components**で構成される。
The layer normalization can ease optimization of the network.
レイヤー正規化により、ネットワークの最適化を容易にすることができます。(i.e. 学習速度を向上できる)
The instance-guided mask introduces multiplicative interactions for feed-forward layer of a standard DNN model and feed-forward hidden layer aggregate the masked information in order to better capture the important feature interactions.
instance-guidedマスクは、**標準的なDNNモデルのfeed-forward層に乗算的な相互作用を導入**し、feed-forward隠れ層は、重要な特徴量の相互作用をよりよく捉えるために、マスクされた情報を集約するものである。
In this way, we turn the widely used feed-forward layer of a standard DNN model into a mixture of addictive and multiplicative feature interactions.
このようにして、標準的なDNNモデルの広く使われているフィードフォワード層を、**加法的・乗法的な特徴量の相互作用の混合に変える**のです。

First, we briefly review the formulation of LayerNorm.
まず、LayerNormの定式化を簡単に説明する。

### 3.3.1. Layer Normalization: レイヤーの正規化：

In general, normalization aims to ensure that signals have zero mean and unit variance as they propagate through a network to reduce "covariate shift" [10].
一般に、**正規化とは、信号がネットワークを伝搬する際に、平均値がゼロで分散が単位(=1.0)となるようにし**、"covariate(共変量) shift"を減らすことを目的としています[10]。(ふむふむ...!)
As an example, layer normalization (Layer Norm or LN)[1] was proposed to ease optimization of recurrent neural networks.
例えば、リカレントニューラルネットワークの最適化を容易にするために、レイヤー正規化(Layer Norm、LN)[1]が提案されています。
Specifically, let 𝑥 = (𝑥1, 𝑥2, ..., 𝑥𝐻 ) denotes the vector representation of an input of size 𝐻 to normalization layers.
具体的には、$\mathbf{x} = (x_1, x_2,\cdots, x_{H})$ は、正規化層へのサイズ $H$ の入力のベクトル表現を示すとする。
LayerNorm re-centers and re-scales input x as
LayerNormは、以下のように、入力された $\mathbf{x}$ を再中心化(re-centering)し、再スケーリング(re-scaling)する。

$$
\mathbf{h} = g \odot N(\mathbf{x}) + \mathbf{b}
, N(\mathbf{x}) = \frac{\mathbf{x} - \mu}{\delta}
\\
\mu = \frac{1}{H} \sum_{i=1}^{H} x_{i}
, \delta = \sqrt{\frac{1}{H} \sum_{i=1}^{H} (x_{i} - \mu)^2}
\tag{8}
$$

where $h$ is the output of a LayerNorm layer.
ここで、$\mathbf{h}$ はLayerNorm層の出力である。
⊙ is an element-wise production operation.
$\odot$ は要素ごとの乗算 操作です。(=アダマール積)
𝜇 and 𝛿 are the mean and standard deviation of input.
$\mu$ と $\delta$ は入力の平均と標準偏差である。
Bias b and gain g are parameters with the same dimension 𝐻.
バイアス $\mathbf{b}$ とゲイン $\mathbf{g}$ は同じ次元 $H$ のパラメータである。(ここでbiasとgainはスカラーだろうか?orベクトル??:thinking:)
(なるほど、LayerNorm層は、入力ベクトルを正規化 + 線形変換してるのか...!:thinking:)

As one of the key component in MaskBlock, layer normalization can be used on both feature embedding and feed- forward layer.
MaskBlockの主要な構成要素の1つであるレイヤー正規化は、特徴量埋め込み層とfeed-forward層の両方で使用することができます。
For the feature embedding layer, we regard each feature’s embedding as a layer to compute the mean, standard deviation, bias and gain of LN as follows:
特徴量埋め込み層については、**各特徴量の埋め込み $\mathbf{e}_{i}$ を1つの層とみなして**(ふむふむ)、以下のようにLNの平均、標準偏差、バイアス、ゲインを計算することにしています:

$$
LN\_EMB(V_{emb})
= concat(LN(\mathbf{e}_1), LN(\mathbf{e}_2),\cdots, LN(\mathbf{e}_{f}))
\tag{9}
$$

As for the feed-forward layer in DNN model, the statistics of 𝐿𝑁 are estimated among neurons contained in the corresponding hidden layer as follows:
DNNモデルのフィードフォワード層については、対応する隠れ層に含まれるニューロン間で、以下のように$LN$ (=レイヤー正規化)の統計量を推定する:

$$
LN\_HID(V_{hidden}) = ReLU(LN(W_{i} X))
\tag{10}
$$

where X ∈ R 𝑡 refers to the input of feed-forward layer, W𝑖 ∈ R 𝑚×𝑡 are parameters for the layer, 𝑡 and 𝑚 respectively denotes the size of input layer and neural number of feed-forward layer.
ここで、$X \in \mathbb{R}^{t}$ はフィードフォワード層の入力データ、$W_{i} \in \mathbb{R}^{m \times t}$ は層のパラメータ、$t$ は入力層のサイズ、フィードフォワード層のニューラル数をそれぞれ示す。(バイアス項はレイヤー正規化の中だけになるのか...!:thinking:)
Notice that we have two places to put normalization operation on the MLP: one place is before non-linear operation and another place is after non-linear operation.
MLPに正規化操作を入れる場所が2つあることに注目してください: 1つはnon-linear operation(=活性化関数の役割...!!:thinking:)の前、もう1つは非線形操作の後です。(=LayerNorm層を活性化関数の前にかませるか、それとも後にかませるか、の話:thinking:)
We find the performance of the normalization before non-linear consistently outperforms that of the normalization after non-linear operation.
非線形前の正規化の性能が、非線形演算後の正規化の性能を一貫して上回っていることがわかります。(=本論文の実験でわかった事なのかな。もしくは既存研究?:thinking:)
So all the normalization used in MLP part is put before non-linear operation in our paper as formula (4) shows.
そのため、MLP部分で使用される正規化は、式(4)が示すように、本論文ではすべてnon-linear operationの前に置かれます。

### 3.3.2. MaskBlock on Feature Embedding:

We propose MaskBlock by combining the three key elements: layer normalization, instance-guided mask and a following feed-forward layer.
我々は、レイヤー正規化、instance-guidedマスク、後続のfeed-forward層という3つの重要な要素を組み合わせてMaskBlockを提案する。
MaskBlock can be stacked to form deeper network.
MaskBlockは積み重ねてより深いネットワークを形成することができます。(Transformer Blockを積み重ねるのと同じ感じかな:thinking:)
According to the different input of each MaskBlock, we have two kinds of MaskBlocks: MaskBlock on feature embedding and MaskBlock on Maskblock.
各MaskBlockの入力の違いに応じて、**2種類のMaskBlocks**を用意しました: "MaskBlock on feature embedding"と"MaskBlock on Maskblock"
We will firstly introduce the MaskBlock on feature embedding as depicted in Figure 2 in this subsection.
本節では、まず図2に描かれたMaskBlock on feature embedding(=特徴量埋め込みに関するMaskBlock)を紹介する。

![figure2]()

The feature embedding V𝑒𝑚𝑏 is the only input for MaskBlock on feature embedding.
特徴量埋め込み $V_{emb}$ は、MaskBlock on feature embeddingの唯一の入力である。
After the layer normalization operation on embedding V𝑒𝑚𝑏, MaskBlock utilizes instance-guided mask to highlight the informative elements in V𝑒𝑚𝑏 by element-wise product, Formally,
埋め込み $V_{emb}$ のレイヤー正規化操作を行った後、MaskBlockは、instance-guidedマスクを利用して、$V_{emb}$ の情報量の多い要素をアダマール積で強調する。数式で表すと以下。

$$
V_{maskedEMB} = V_{mask} \odt LN\_EMB(V_{emb})
\tag{11}
$$

where ⊙ means an element-wise production between the instanceguided mask and the normalized vector 𝐿𝑁𝐸𝑀𝐵(V𝑒𝑚𝑏), V𝑚𝑎𝑠𝑘𝑒𝑑𝐸𝑀𝐵 denote the masked feature embedding.
ここで、⊙はインスタンスガイドされたマスクとレイヤー正規化後の特徴量埋め込み $LN\_EMB(V_{emb})$ との間の要素積、$V_{maskedEMB}$ はマスクされた特徴量埋め込みを表す。
Notice that the input of instance-guided mask V𝑚𝑎𝑠𝑘 is also the feature embedding 𝑉𝑒𝑚𝑏.
instance-guidedマスク $V_{mask}$ (を得る為の)の入力も、特徴量埋め込み $V_{emb}$ であることに注意してください。

We introduce a feed-forward hidden layer and a following layer normalization operation in MaskBlock to better aggregate the masked information by a normalized non-linear transformation.
MaskBlockにfeed-forward隠れ層とそれに続くレイヤー正規化操作を導入し、正規化されたものを非線形変換によってマスクされた情報をよりよく集約させる。
The output of MaskBlock can be calculated as follows:
MaskBlockの出力は、以下のように計算できます：
(あ、一層のfeed-forward層なんだ...!:thinking:)

$$
V_{output} = LN\_HID(W_{i} V_{maskedEMB})
\\
= ReLU(LN(W_i V_{maskedEMB}))
\tag{12}
$$

where W𝑖 ∈ R 𝑞×𝑛 are parameters of the feed-forward layer in the 𝑖-th MaskBlock, 𝑛 denotes the size of V𝑚𝑎𝑠𝑘𝑒𝑑𝐸𝑀𝐵 and 𝑞 means the size of neural number of the feed-forward layer.
ここで、$W_{i} \in \mathbb{R}^{q \times n}$ は $i$ 番目のMaskBlockにおけるfeed-forward層のパラメータ(=投影行列:thinking:)、$n$ は$V_{maskedEMB}$ のサイズ、$q$ はフィードフォワード層のニューラル数の大きさ(=$V_{output}$ の次元数...??)を表す。

The instance-guided mask introduces the element-wise product into feature embedding as a fine-grained attention while normalization both on feature embedding and hidden layer eases the network optimization.
instance-guidedマスクは、特徴量埋め込みに要素積を導入することできめ細かいattentionを採用するとともに、特徴量埋め込みと隠れ層の両方でレイヤー正規化することで、ネットワークの最適化を容易にします。
These key components in MaskBlock help the feedforward layer capture complex feature cross more efficiently.
MaskBlockのこれらのキーコンポーネントは、feed-forward層が複雑な特徴量間のクロス(=相互作用?)をより効率的に捉えることをサポートします。

### 3.3.3. MaskBlock on MaskBlock:

![fig3]()

In this subsection, we will introduce MaskBlock on MaskBlock as depicted in Figure 3.
この小節では、図3に描かれたMaskBlock on MaskBlockを紹介する。
There are two different inputs for this MaskBlock: feature embedding 𝑉𝑒𝑚𝑏 and the output 𝑉 𝑝 𝑜𝑢𝑡𝑝𝑢𝑡 of the previous MaskBlock.
このMaskBlockの入力は、特徴量埋め込み $V_{emb}$ と、前のMaskBlockの出力 $V_{output}^{p}$ の2種類です。
The input of instance-guided mask for this kind of MaskBlock is always the feature embedding 𝑉𝑒𝑚𝑏.
この種のMaskBlockのinstance-guidedマスクの入力は、常に特徴量埋め込み $V_{emb}$ となる。
MaskBlock utilizes instance-guided mask to highlight the important feature interactions in previous MaskBlock’s output 𝑉 𝑝 𝑜𝑢𝑡𝑝𝑢𝑡 by element-wise product, Formally,
MaskBlockはinstance-guidedマスクを利用して、以前のMaskBlockの出力 $V_{output}^{p}$ を要素別積で強調する。数式で表すと...

$$
V_{maskedHID} = V_{mask} \odot V_{output}^{p}
\tag{13}
$$

where ⊙ means an element-wise production between the instanceguided mask 𝑉𝑚𝑎𝑠𝑘 and the previous MaskBlock’s output 𝑉 𝑝 𝑜𝑢𝑡𝑝𝑢𝑡, 𝑉𝑚𝑎𝑠𝑘𝑒𝑑𝐻 𝐼𝐷 denote the masked hidden layer.
$\odot$ は要素積。$V_{maskedHID}$ はmaskされたhidden layerの出力。(前のブロックのhidden layerの出力 $V_{output}^{p}$ をmaskしてるから??:thinking:)

In order to better capture the important feature interactions, another feed-forward hidden layer and a following layer normalization are introduced in MaskBlock .
重要な特徴量間の相互作用をよりよく捉えるために、MaskBlock では、もう一つのフィードフォワード隠れ層とそれに続くレイヤー正規化を導入しています。
In this way, we turn the widely used feed-forward layer of a standard DNN model into a mixture of addictive and multiplicative feature interactions to avoid the ineffectiveness of those addictive feature cross models.
このようにして、標準的なDNNモデルの広く使われているフィードフォワード層を、addictive(加法的)な特徴量相互作用とmultiplicative(乗法的)な特徴量相互作用の混合に変え、それらの加法的特徴相互作用モデルの非効率性を回避する。
The output of MaskBlock can be calculated as follows:
MaskBlockの出力は、以下のように計算できます：

$$
V_{output} = LN\_HID(W_{i} V_{maskedHID})
\\
= ReLU(LN(W_{i} (V_{mask} \odot V_{output}^{p})))
\tag{14}
$$

where 𝑊𝑖 ∈ R 𝑞×𝑛 are parameters of the feed-forward layer in the 𝑖-th MaskBlock, 𝑛 denotes the size of V𝑚𝑎𝑠𝑘𝑒𝑑𝐻 𝐼𝐷 and 𝑞 means the size of neural number of the feed-forward layer.
ここで、$W_{i} \in \mathbb{R}^{q \times n}$ は $i$ 番目のMaskBlockにおけるフィードフォワード層のパラメータ、$n$ は $V_{maskedHID}$ のサイズ(=次元数)、$q$ はフィードフォワード層のニューラルノードの数を表す。(=)

## 3.4. MaskNet マスクネット

Based on the MaskBlock, various new ranking models can be designed according to different configurations.
MaskBlockをベースに、様々な構成で新しいランキングモデルを設計することができます。
The rank model consisting of MaskBlock is called MaskNet in this work.
**MaskBlockで構成されるランクモデルを、本論文ではMaskNetと呼ぶ。**
We also propose two MaskNet models by utilizing the MaskBlock as the basic building block.
また、MaskBlockを基本構成要素として、**2つのMaskNetモデ**ルを提案しています。

![fig4]()

### 3.4.1. Serial MaskNet:

We can stack one MaskBlock after another to build the ranking system , as shown by the left model in Figure 4.
図4の左のモデルのように、MaskBlockを次々に積み重ねてランキングシステムを構築することができます。
The first block is a MaskBlock on feature embedding and all other blocks are MaskBlock on Maskblock to form a deeper network.
最初のブロックは MaskBlock on feature embedding、それ以外のブロックは MaskBlock on Maskblock を積み重ねてより深いネットワークを形成します。
The prediction layer is put on the final MaskBlock’s output vector.
予測層は、最終的なMaskBlockの出力ベクトルにつけられる。
We call MaskNet under this serial configuration as SerMaskNet in our paper.
本稿では、このようなserial(=連続, 直列 等の意味)構成のMaskNetを**SerMaskNet** と呼ぶことにする。
All inputs of instance-guided mask in every MaskBlock come from the feature embedding layer V𝑒𝑚𝑏 and this makes the serial MaskNet model look like a RNN model with sharing input at each time step.
**全てのMaskBlockにおけるinstance-guidedマスクの入力は全て特徴量埋め込み層 $V_{emb}$ から来る**ため、シリアルMaskNetモデルは各タイムステップで入力を共有するRNNモデルのように見える。(??:thinking:)

### 3.4.2. Parallel MaskNet: パラレルマスクネット

We propose another MaskNet by placing several MaskBlocks on feature embedding in parallel on a sharing feature embedding layer, as depicted by the right model in Figure 4.
図4の右のモデルのように、**共有した特徴量埋め込み層上に、MaskBlocks on feature embedding を複数並列に配置する**ことで、別のMaskNetを提案します。
The input of each block is only the shared feature embedding V𝑒𝑚𝑏 under this configuration.
各ブロックの入力は、この構成では共有した特徴量埋め込み $V_{emb}$ のみである。(各MaskedBlockには同じ入力が渡される:thinking:)
We can regard this ranking model as a mixture of multiple experts just as MMoE[15] does.
このランキングモデルは、MMoE[15]と同じように、**複数の専門家の混合物とみなすことができる**。
Each MaskBlock pays attention to specific kind of important features or feature interactions.
各MaskBlockは、特定の種類の重要な特徴量や特徴量間の相互作用に注目しています。
We collect the information of each expert by concatenating the output of each MaskBlock as follows:
各MaskBlockの出力を以下のように連結することで、各エキスパートの情報を収集する:

$$
V_{merge} = concate(V^{1}_{output}, V^{2}_{output}, \cdots, V^{i}_{output}, \cdots, V^{u}_{output})
\tag{15}
$$

where V𝑖 𝑜𝑢𝑡𝑝𝑢𝑡 ∈ R 𝑞 is the output of the 𝑖-th MaskBlock and 𝑞 means size of neural number of feed-forward layer in MaskBlock, 𝑢 is the MaskBlock number.
ここで、$V_{output}^{i} \in \mathbb{R}^{q}$ は $i$ 番目のMaskBlockの出力、$q$ はMaskBlockのフィードフォワード層のニューラル数(=出力される埋め込みの次元数:thinking:)、$i$ はMaskBlockの通し番号である。
(じゃあ $V_{merge} \in \mathbb{R}^{uq}$ になるのかな:thinking:)

To further merge the feature interactions captured by each expert, multiple feed-forward layers are stacked on the concatenation information V𝑚𝑒𝑟𝑔𝑒 .
各エキスパートが捉えた特徴量間の相互作用をさらに統合するために、連結情報 $V_{merge}$ に複数のフィードフォワード層を積み重ねる。
Let H0 = V𝑚𝑒𝑟𝑔𝑒 denotes the output of the concatenation layer, then H0 is fed into the deep neural network and the feed forward process is:
$H_0 = V_{merge}$ が連結層の出力を表すとすると、$H_0$ はディープニューラルネットワークに投入される。そのfeed-forward処理は以下。(活性化関数がReLUの何層かのfully-connectedのfeed-forward層か。線形変換 ->非線形変換を層の数分繰り返すやつ:thinking:)

$$
H_{l} = ReLU(W_{l} H_{l-1} + \beta_{l})
\tag{16}
$$

where 𝑙 is the depth and ReLU is the activation function.
ここで、$l$ は深さ、ReLUは活性化関数である。
W𝑡 , 𝛽𝑡 , H𝑙 are the model weight, bias and output of the 𝑙-th layer.
$W_{l}, \beta_{l}, H_{l}$ は、$l$ 番目の層のモデル重み、バイアス、出力である。
The prediction layer is put on the last layer of multiple feed-forward networks.
予測層は、複数のフィードフォワードネットワークの最終層に置かれます。
We call this version MaskNet as "ParaMaskNet" in the following part of this paper.
本稿では、このMaskNetを "**ParaMaskNet**"と呼ぶことにする。

## 3.5. Prediction Layer プレディクションレイヤー

To summarize, we give the overall formulation of our proposed model’ s output as:
まとめると、提案モデルの出力の全体的な定式化は次のようになる:

$$
\hat{y} = \delta(w_0 + \sum_{i=1}^{n} w_{i} x_{i})
\tag{17}
$$

where 𝑦^ ∈ (0, 1) is the predicted value of CTR, 𝛿 is the sigmoid function, 𝑛 is the size of the last MaskBlock’s output(SerMaskNet) or feed-forward layer(ParaMaskNet), 𝑥𝑖 is the bit value of feedforward layer and 𝑤𝑖 is the learned weight for each bit value.
ここで、$\hat{y} \in (0, 1)$ はCTRの予測値、$\delta$ はシグモイド関数(あ、そうなのか:thinking)、$n$ は最後のMaskBlockの出力(SerMaskNet)またはフィードフォワード層(ParaMaskNet)のサイズ(=出力されるベクトルの次元数)、$x_i$ はフィードフォワード層の各要素、$w_{i}$ は各要素に対する学習重みです。(最終的な出力をスカラーにしたいからこの層なのね。結局はこれもfeed-forward層。)

For binary classifications, the loss function is the log loss:
二値分類の場合、損失関数は対数損失となる(=クロスエントロピー損失関数だっけ?:thinking:):
(point-wiseの損失関数でも十分なのかもなぁ...! pair-wiseとかlist-wiseな損失関数でなくても。)

$$
\mathcal{L} = - \frac{1}{N} \sum_{i=1}^{N}{
    y_i log(\hat{y}_{i}) + (1 - y_i)
}
\tag{18}
$$

where 𝑁 is the total number of training instances, 𝑦𝑖 is the ground truth of 𝑖-th instance and 𝑦^𝑖 is the predicted CTR.
ここで、𝑁は訓練インスタンスの総数(=mini-batch1つあたりのtraining exampleの数)、$y_i$ は $i$ 番目のインスタンスのground truth、$\hat{y}_{i}$ は予測CTRである。
The optimization process is to minimize the following objective function:
最適化処理は、以下の目的関数を最小化することである:

$$
L = \mathcal{L} + \lambda ||\Theta||
\tag{19}
$$

where 𝜆 denotes the regularization term and Θ denotes the set of parameters, including those in feature embedding matrix, instanceguided mask matrix, feed-forward layer in MaskBlock, and prediction part.
ここで、$\lambda$ は正則化項の強さを決めるハイパーパラメータ、$\Theta$はモデルのパラメータ集合 (特徴量埋め込み行列、instance-guidedマスク行列、MaskBlockのフィードフォワード層、予測moduleのパラメータ)を示す。

# 4. Experimental Results 実験結果

In this section, we evaluate the proposed approaches on three realworld datasets and conduct detailed ablation studies to answer the following research questions:
本節では、以下の研究課題に答えるため、3つの実世界データセットで提案アプローチを評価し、詳細なアブレーションスタディ(=各パーツの影響評価)を実施する:

- RQ1 Does the proposed MaskNet model based on the MaskBlock perform better than existing state-of-the-art deep learning based CTR models? RQ1 MaskBlockに基づくMaskNetの提案モデルは、既存の最先端ディープラーニングに基づくCTRモデルより性能が高いか？

- RQ2 What are the influences of various components in the MaskBlock architecture? Is each component necessary to build an effective ranking system? RQ2 MaskBlockアーキテクチャにおける様々なコンポーネントの影響力はどのようなものか？**効果的なランキングシステムを構築するために、各コンポーネントは必要なのか？**

- RQ3 How does the hyper-parameter of networks influence the performance of our proposed two MaskNet models? RQ3 ネットワークのハイパーパラメータは、我々が提案する2つのMaskNetモデルの性能にどのように影響するか?

- RQ4 Does instance-guided mask highlight the important elements in feature embedding and feed-forward layers according to the input instance? RQ4 インスタンスガイド型マスクは、入力インスタンスに応じて、特徴量埋め込み層やフィードフォワード層の重要な要素を強調するのか？

In the following, we will first describe the experimental settings, followed by answering the above research questions.
以下では、まず実験設定について説明し、その後、上記のリサーチクエスチョンに回答する。

## 4.1. Experiment Setup 実験セットアップ

### 4.1.1. Datasets. データセット

The following three data sets are used in our experiments:
実験では、以下の3つのデータセットを使用した：

- (1) Criteo1 Dataset: As a very famous public real world display ad dataset with each ad display information and corresponding user click feedback, Criteo data set is widely used in many CTR model evaluation. There are 26 anonymous categorical fields and 13 continuous feature fields in Criteo data set.
  - (1) Criteo1データセット： Criteoデータセットは、**各広告表示情報とそれに対応するユーザクリックフィードバック**を持つ非常に有名な公開実世界ディスプレイ広告データセットとして、多くのCTRモデル評価で広く使用されています。 Criteoのデータセットには、26の匿名カテゴリフィールドと13の連続特徴フィールドがあります。
- (2) Malware2 Dataset: Malware is a dataset from Kaggle competitions published in the Microsoft Malware prediction. The goal of this competition is to predict a Windows machine’s probability of getting infected. The malware prediction task can be formulated as a binary classification problem like a typical CTR estimation task does.
  - (2) Malware2 Dataset： Malwareは、MicrosoftのMalware予測で公開されたKaggleコンペティションのデータセットです。 この競技の目的は、Windowsマシンが感染する確率を予測することです。 **マルウェア予測タスクは、典型的なCTR推定タスクがそうであるように、二値分類問題として定式化**することができます。(あ、CTR予測タスクではないんだ!ランキング問題で解く意味があるのかな??)
- (3) Avazu3 Dataset: The Avazu dataset consists of several days of ad click- through data which is ordered chronologically. For each click data, there are 23 fields which indicate elements of a single ad impression.
  - (3) Avazu3データセット： Avazuのデータセットは、**数日分の広告クリックスルー・データを時系列に並べたもの**である。 各クリックデータには、1つの広告インプレッションの要素を示す23のフィールドが存在します。

We randomly split instances by 8 : 1 : 1 for training , validation and test while Table 1 lists the statistics of the evaluation datasets(これは時系列に沿ってデータを分けたほうがいいね...!:thinking:)
表1に評価用データセットの統計値を示す。

![table1]()

### 4.1.2. Evaluation Metrics. 評価指標

AUC (Area Under ROC) is used in our experiments as the evaluation metric.
実験では、評価指標としてAUC（Area Under ROC）を用いています。
AUC’s upper bound is 1 and larger value indicates a better performance.
AUCの上限は1であり、値が大きいほど性能が優れていることを示す。(そうか、CTR予測タスクだからAUCでもいいんだ)

RelaImp is also as work [23] does to measure the relative AUC improvements over the corresponding baseline model as another evaluation metric.
RelaImpはまた、別の評価指標として、**対応するベースラインモデルに対する相対的なAUCの改善を測定する**作業[23]と同様です。
Since AUC is 0.5 from a random strategy, we can remove the constant part of the AUC score and formalize the RelaImp as:
ランダム戦略からAUCは0.5なので、AUCスコアの定数部分を削除してRelaImpを次のように定式化することができる：

$$
RelaImp = \frac{AUC(Measured Model) - 0.5}{AUC(Base model) - 0.5} - 1
\tag{20}
$$

### 4.1.3. Models for Comparisons. 比較のためのモデル。

We compare the performance of the following CTR estimation models with our proposed approaches: FM, DNN, DeepFM, Deep&Cross Network(DCN), xDeepFM and AutoInt Model, all of which are discussed in Section 2.
以下のCTR推定モデルの性能を、我々の提案するアプローチと比較する: FM, DNN, DeepFM, Deep&Cross Network(DCN), xDeepFM, AutoInt Modelであり、これらはすべてセクション2で説明されている。
FM is considered as the base model in evaluation.
FMは評価のベースモデルとして位置づけられています。

### 4.1.4. Implementation Details.

We implement all the models with Tensorflow in our experiments.
実験ではすべてのモデルをTensorflowで実装しています。
For optimization method, we use the Adam with a mini-batch size of 1024 and a learning rate is set to 0.0001.
最適化手法としては、ミニバッチサイズを1024、学習率を0.0001に設定したAdamを使用する。
Focusing on neural networks structures in our paper, we make the dimension of field embedding for all models to be a fixed value of 10.
本稿ではニューラルネットワークの構造に着目し、**すべてのモデルでフィールドエンベッディングの次元を10という固定値**にしている。
For models with DNN part, the depth of hidden layers is set to 3, the number of neurons per layer is 400, all activation function is ReLU.
DNN部分を持つモデルについては、隠れ層の深さを3、1層あたりのニューロン数を400、すべての活性化関数をReLUとした。
For default settings in MaskBlock, the reduction ratio of instance-guided mask is set to 2.
MaskBlockのデフォルト設定では、インスタンスガイドマスクの**縮小率は2**に設定されています。
We conduct our experiments with 2 Tesla 𝐾40 GPUs.
2台のTesla K40 GPUで実験を行っています。

## 4.2. Performance Comparison (RQ1) パフォーマンスの比較（RQ1）

![table2]()

The overall performances of different models on three evaluation datasets are show in the Table 2.
3つの評価データセットにおける異なるモデルの総合的な性能を表2に示します。
From the experimental results, we can see that:
実験結果から、次のことがわかります：

- (1) Both the serial model and parallel model achieve better performance on all three datasets and obtains significant improvements over the state-of-the-art methods. It can boost the accuracy over the baseline FM by 3.12% to 11.40%, baseline DeepFM by 1.55% to 5.23%, as well as xDeepFM baseline by 1.27% to 4.46%. We also conduct a significance test to verify that our proposed models outperforms baselines with the significance level 𝛼 = 0.01. Though maskNet model lacks similar module such as CIN in xDeepFM to explicitly capture high-order feature interaction, it still achieves better performance because of the existence of MaskBlock. The experiment results imply that MaskBlock indeed enhance DNN Model’s ability of capturing complex feature interactions through introducing multiplicative operation into DNN models by instance-guided mask on the normalized feature embedding and feed-forward layer. (1)**シリアルモデル、パラレルモデルともに、3つのデータセットでより良い性能を達成し、最先端の手法と比較して大きな改善を得ることができました。** ベースラインFMを3.12%から11.40%、ベースラインDeepFMを1.55%から5.23%、xDeepFMベースラインを1.27%から4.46%の精度で向上させることができます。 また、有意水準𝛼= 0.01で、提案モデルがベースラインを上回ることを検証するために有意性検定を実施した。 maskNetモデルには、xDeepFMのCINのような高次特徴の相互作用を明示的に捉えるモジュールがありませんが、それでもMaskBlockの存在により、より高い性能を達成しています。 実験結果は、MaskBlockが、正規化された特徴埋め込み層とフィードフォワード層にインスタンスガイド付きマスクを適用し、DNNモデルに乗算演算を導入することで、複雑な特徴の相互作用を捉える能力を確かに向上させることを示唆しています。

- (2) As for the comparison of the serial model and parallel model, the experimental results show comparable performance on three evaluation datasets. It explicitly proves that MaskBlock is an effective basic building unit for composing various high performance ranking systems. (2) シリアルモデルとパラレルモデルの比較については、3つの評価データセットにおいて、実験結果は同等の性能を示しています。 MaskBlockが様々な高性能ランキングシステムを構成するための有効な基本構成単位であることを明示的に証明しています。

## 4.3. Ablation Study of MaskBlock (RQ2) MaskBlockのアブレーション研究 (RQ2)

In order to better understand the impact of each component in MaskBlock, we perform ablation experiments over key components of MaskBlock by only removing one of them to observe the performance change, including mask module, layer normalization(LN) and feed-forward network(FFN).
MaskBlockの各コンポーネントの影響をより理解するために、MaskBlockの主要コンポーネントであるマスクモジュール、レイヤー正規化（LN）、フィードフォワードネットワーク（FFN）のうち**1つだけを削除するアブレーション実験**を行い、性能変化を観察しました。
Table 3 shows the results of our two full version MaskNet models and its variants removing only one component.
表3は、MaskNetの2つのフルモデルと、1つのコンポーネントだけを取り除いたバリエーションモデルの結果です。

![table3]()

From the results in Table 3, we can see that removing either instance-guided mask or layer normalization will decrease model’s performance and this implies that both the instance-guided mask and layer normalization are necessary components in MaskBlock for its effectiveness.
表3の結果から、**インスタンスガイド付きマスクとレイヤー正規化のどちらかを削除するとモデルの性能が低下することがわかり**、インスタンスガイド付きマスクとレイヤー正規化の両方がMaskBlockの有効性を高めるために必要なコンポーネントであることが示唆されました。
As for the feed-forward layer in MaskBlock, its effect on serial model or parallel model shows difference.
MaskBlockのフィードフォワード層については、シリアルモデルとパラレルモデルで効果が異なる。
The Serial model’s performance dramatically degrades while it seems do no harm to parallel model if we remove the feed-forward layer in MaskBlock.
MaskBlockのフィードフォワード層を削除してもパラレルモデルには害がないように見えるが、Serialモデルの性能は劇的に低下していることがわかる。
We deem this implies that the feed-forward layer in MaskBlock is important for merging the feature interaction information after instance-guided mask.
このことは、MaskBlockのフィードフォワード層が、インスタンス誘導型マスクの後に特徴的な相互作用情報をマージするために重要であることを示唆していると考えられる。
For parallel model, the multiple feed-forward layers above parallel MaskBlocks have similar function as feed-forward layer in MaskBlock does and this may produce performance difference between two models when we remove this component.
並列モデルの場合、並列MaskBlockの上にある複数のフィードフォワード層は、MaskBlockのフィードフォワード層と同様の機能を持つため、このコンポーネントを削除すると、2つのモデル間で性能差が生じる可能性があります。

<!-- ここまで読んだ -->

## 4.4. Hyper-Parameter Study(RQ3) ハイパーパラメーター研究(RQ3)

In the following part of the paper, we study the impacts of hyperparameters on two MaskNet models, including 1) the number of feature embedding size; 2) the number of MaskBlock; and 3) the reduction ratio in instance-guided mask module.
本論文の以下の部分では、2つのMaskNetモデルに対するハイパーパラメータの影響について、1）特徴量埋め込みサイズの数、2）MaskBlockの数、3）インスタンス誘導型マスクモジュールの**削減率**について研究している。
The experiments are conducted on Criteo dataset via changing one hyper-parameter while holding the other settings.
Criteoデータセットにおいて、1つのハイパーパラメータを変更し、他の設定を維持したまま実験を行った。
The hyper-parameter experiments show similar trend in other two datasets.
ハイパーパラメータの実験では、他の2つのデータセットでも同様の傾向が見られた。(ふむ)

### 4.4.1. Number of Feature Embedding Size. 特徴量埋め込みサイズの数。

![table4]()

The results in Table 4 show the impact of the number of feature embedding size on model performance.
表4の結果は、特徴量埋め込みサイズの数がモデルの性能に与える影響を示している。
It can be observed that the performances of both models increase when embedding size increases at the beginning.
両モデルとも、埋め込みサイズが初期に大きくなると、性能が向上することが確認できます。
However, model performance degrades when the embedding size is set greater than 50 for SerMaskNet model and 30 for ParaMaskNet model.
しかし、埋め込みサイズをSerMaskNetモデルで50以上、ParaMaskNetモデルで30以上に設定すると、モデル性能が低下する。
The experimental results tell us the models benefit from larger feature embedding size.
実験結果は、モデルがより大きな特徴量埋め込みサイズの恩恵を受けることを物語っています。

### 4.4.2. Number of MaskBlock. MaskBlockの数

![table5]()

For understanding the influence of the number of MaskBlock on model’s performance, we conduct experiments to stack MaskBlock from 1 to 9 blocks for both MaskNet models.
MaskBlockの数がモデルの性能に与える影響を理解するため、MaskNetの両モデルについて、MaskBlockを1ブロックから9ブロックまで積み上げる実験を行いました。
The experimental results are listed in the Table 5.
実験結果を表5に示します。
For SerMaskNet model, the performance increases with more blocks at the beginning until the number is set greater than 5.
SerMaskNetモデルの場合、初期にブロック数を増やすと、5個以上になるまで性能が向上することがわかります。
While the performance slowly increases when we continually add more MaskBlock into ParaMaskNet model.
一方、ParaMaskNetのモデルにMaskBlockを追加し続けると、徐々に性能が向上します。
This may indicates that more experts boost the ParaMaskNet model’s performance though it’s more time consuming.
これは、より多くの専門家がParaMaskNetモデルの性能を向上させるが、より多くの時間がかかることを示していると考えられる。

### 4.4.3. Reduction Ratio in Instance-Guided Mask. インスタンス誘導マスクにおける削減率。

![table6]()

In order to explore the influence of the reduction ratio in instance-guided mask, We conduct some experiments to adjust the reduction ratio from 1 to 5 by changing the size of aggregation layer.
インスタンス誘導型マスクにおける削減率の影響を探るため、**集約層の大きさを変えて削減率**を1～5まで調整する実験を行った。
Experimental results are shown in Table 6 and we can observe that various reduction ratio has little influence on model’s performance.
実験結果を表6に示すが、様々な縮小率がモデルの性能にほとんど影響を与えないことがわかる。
This indicates that we can adopt small reduction ratio in aggregation layer in real life applications for saving the computation resources.
このことは、実際のアプリケーションにおいて、**計算資源を節約するために、集約層の縮小率を小さくすることを採用できる**ことを示しています。

<!-- ここまで読んだ -->

## 4.5. Instance-Guided Mask Study(RQ4) インスタンス誘導型マスク研究(RQ4)

As discussed in Section in 3.2, instance-guided mask can be regarded as a special kind of bit-wise attention mechanism to highlight important information based on the current input instance.
3.2節で述べたように、インスタンス誘導型マスクは、現在の入力インスタンスに基づいて重要な情報を強調する特殊な種類の**bit単位(=特徴量埋め込みのelement単位?)のattentionメカニズムとしてみなすことができる**。
We can utilize instance-guided mask to boost the informative elements and suppress the uninformative elements or even noise in feature embedding and feed-forward layer.
**特徴量埋め込みとフィードフォワード層で、(予測の観点で)情報量の多い要素(=特徴量埋め込みの中の要素)を高め、情報量の少ない要素やノイズを抑制するために、インスタンスガイド付きマスクを利用することができます**。

To verify this, we design the following experiment: After training the SerMaskNet with 3 blocks, we input different instances into the model and observe the outputs of corresponding instance-guided masks.
これを検証するために、次のような実験を計画した：
3ブロックのSerMaskNetを学習させた後、異なるインスタンス(=学習に使ってないデータ??)をモデルに入力し、対応するインスタンス誘導型マスクの出力を観察する。

Firstly, we randomly sample 100000 different instances from Criteo dataset and observe the distributions of the produced values by instance-guided mask from different blocks.
まず、Criteoデータセットから100000個の異なるインスタンスをランダムにサンプリング(=これがテスト用データになる??)し、異なるブロック(=3つのブロックの各出力値?)からインスタンス誘導型マスクによる生成値(=出力値)の分布を観察します。
Figure 5 shows the result.
図5にその結果を示します。

![figure5]()

We can see that the distribution of mask values follow normal distribution.
**マスク値(=各maskブロックの出力値)の分布(i.e. 応答分布)は正規分布に従う**ことがわかる。
Over 50% of the mask values are small number near zero and only little fraction of the mask value is a relatively larger number.
マスク値の50％以上はゼロに近い小さな数で、相対的に大きな数のマスク値はごくわずかです。(i.e. 正規分布の平均は0あたり:thinking:)
This implies that large fraction of signals in feature embedding and feed-forward layer is uninformative or even noise which is suppressed by the small mask values.
このことは、特徴量埋め込み層とフィードフォワード層の信号(=maskブロックの入力?)の大部分は、小さなマスク値(=maskブロックの出力が0に近い)によって抑制された情報量の少ない、あるいはノイズであることを意味する。
However, there is some informative information boosted by larger mask values through instance-guided mask.
しかし、インスタンスガイド型マスクにより、マスクの値を大きくすることで、情報量が増えることもある。

Secondly, we randomly sample two instances and compare the difference of the produced values by instance-guided mask.
次に、2つのインスタンス(=入力データ, prediction example)をランダムにサンプリングし、インスタンス誘導型マスクによる生成値(=出力値)の差を比較します。
The results are shown in Figure 6.
その結果を図6に示します。

![fig6]()

We can see that: As for the mask values for feature embedding, different input instances lead the mask to pay attention to various areas.
以下のことがわかる：
特徴量埋め込みのためのマスク値(figure6 左)については、**入力インスタンス(prediction example)の違いにより、マスクが様々な領域に注目するようになります**。(maskブロックの出力値によって)
The mask outputs of instance A pay more attention to the first few features and the mask values of instance B focus on some bits of other features.
インスタンスAのマスク出力は最初の数個の特徴量に注目し、インスタンスBのマスク値は他の特徴量の一部のビットに注目する。

We can observe the similar trend in the mask values in feed-forward layer.
フィードフォワード層でのマスク値(figure 6右)も同様の傾向が見られる。
This indicates the input instance indeed guide the mask to pay attention to the different part of the feature embedding and feed-forward layer.
これは、入力インスタンス(の各prediction example??)が、特徴量埋め込み層とフィードフォワード層の異なる部分に注意を払うよう、マスクを確かに誘導していることを示しています。
(全てのexampleで決まった特徴量に大きなattention weightを付与するのではなく、特徴量間の相互作用を考慮して、各exampleごとに異なる特徴量に対して大きなattention weightを付与している、みたいな??:thinking:)

<!-- ここまで読んだ -->

# 5. Conclusion 結論

In this paper, we introduce multiplicative operation into DNN ranking system by proposing instance-guided mask which performs element-wise product both on the feature embedding and feedforward layers.
本論文では、特徴埋め込み層とフィードフォワード層の両方で要素ごとの積を行うinstance-guidedマスクを提案し、DNNランキングシステムに乗算演算を導入する。
We also turn the feed-forward layer in DNN model into a mixture of addictive and multiplicative feature interactions by proposing MaskBlock by bombing the layer normalization, instanceguided mask, and feed-forward layer.
また、レイヤー正規化、instance-guidedマスク、フィードフォワード層を組み合わせたMaskBlockを提案することで、DNNモデルのフィードフォワード層を加法的・乗法的な特徴相互作用の混合に変えています。
MaskBlock is a basic building block to be used to design new ranking model.
**MaskBlockは、新しいランキングモデルを設計するために使用する基本的な構成要素**です。
We also propose two specific MaskNet models based on the MaskBlock.
また、MaskBlockをベースにした2つの具体的なMaskNetモデルを提案しています。
The experiment results on three real-world datasets demonstrate that our proposed models outperform state-of-the-art models such as DeepFM and xDeepFM significantly.
3つの実世界データセットを用いた実験結果から、提案モデルがDeepFMやxDeepFMなどの最先端モデルを大幅に上回ることが実証された。

<!-- ここまで読んだ -->
