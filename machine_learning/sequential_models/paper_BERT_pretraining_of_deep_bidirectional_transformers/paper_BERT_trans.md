## 0.1. link リンク

https://arxiv.org/abs/1810.04805
https://arxiv.org/abs/1810.04805

## 0.2. title タイトル

https://arxiv.org/abs/1810.04805
https://arxiv.org/abs/1810.04805

## 0.3. abstract 抄録

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.
私たちは、**BERT（Bi-directional Encoder Representations from Transformers）**と呼ばれる新しい言語表現モデルを紹介する。
Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pretrain deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers.
最近の言語表現モデル（Peters et al, 2018a; Radford et al, 2018）とは異なり、BERTは、すべての層で左右両方の文脈を共同で条件付けることによって、ラベル付けされていないテキストから深い双方向表現を事前学習するように設計されている。
As a result, the pre-trained BERT model can be finetuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial taskspecific architecture modifications.
その結果、事前に訓練されたBERTモデルは、タスク固有のアーキテクチャを大幅に変更することなく、質問応答や言語推論などの広範なタスクのための最先端のモデルを作成するために、出力層を1つ追加するだけでfine-tuningすることができる。
BERT is conceptually simple and empirically powerful.
BERTは概念的にシンプルで、経験的に強力である。
It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).
GLUEスコアは80.5%（絶対値で7.7%の向上）、MultiNLI精度は86.7%（絶対値で4.6%の向上）、SQuAD v1.1質問応答テストF1は93.2（絶対値で1.5%の向上）、SQuAD v2.0テストF1は83.1（絶対値で5.1%の向上）と、11の自然言語処理タスクで新たな最先端の結果を得ています。

# 1. Introduction はじめに

Language model pre-training has been shown to be effective for improving many natural language processing tasks (Dai and Le, 2015; Peters et al., 2018a; Radford et al., 2018; Howard and Ruder, 2018).
言語モデルの事前トレーニングは、多くの自然言語処理タスクの改善に有効であることが示されている（Dai and Le, 2015; Peters et al., 2018a; Radford et al.）
These include sentence-level tasks such as natural language inference (Bowman et al., 2015; Williams et al., 2018) and paraphrasing (Dolan and Brockett, 2005), which aim to predict the relationships between sentences by analyzing them holistically, as well as token-level tasks such as named entity recognition and question answering, where models are required to produce fine-grained output at the token level (Tjong Kim Sang and De Meulder, 2003; Rajpurkar et al., 2016).
これには、自然言語推論（Bowman et al, 2015; Williams et al, 2018）や言い換え（Dolan and Brockett, 2005）のような文レベルのタスクがあり、これらは文を全体的に分析することによって文間の関係を予測することを目的としている。

There are two existing strategies for applying pre-trained language representations to downstream tasks: feature-based and fine-tuning.
事前に訓練された言語表現を下流のタスクに適用するための既存の戦略には、特徴ベースとfine-tuningの2つがある。
The feature-based approach, such as ELMo (Peters et al., 2018a), uses task-specific architectures that include the pre-trained representations as additional features.
ELMo（Petersら、2018a）のような特徴ベースのアプローチは、事前に訓練された表現を追加特徴として含むタスク固有のアーキテクチャを使用する。
The fine-tuning approach, such as the Generative Pre-trained Transformer (OpenAI GPT) (Radford et al., 2018), introduces minimal task-specific parameters, and is trained on the downstream tasks by simply fine-tuning all pretrained parameters.
**Generative Pre-trained Transformer (OpenAI GPT)** (Radford et al., 2018)のようなfine-tuningアプローチは、最小限のタスク固有のパラメータを導入し、すべての事前学習済みパラメータをfine-tuningするだけで下流のタスクで学習される。
The two approaches share the same objective function during pre-training, where they use unidirectional language models to learn general language representations.
この2つのアプローチは、事前学習において同じ目的関数を共有し、一般的な言語表現を学習するために一方向性言語モデルを使用する。
We argue that current techniques restrict the power of the pre-trained representations, especially for the fine-tuning approaches.
我々は、現在の技術では、特にファインチューニングアプローチにおいて、事前に訓練された表現の力が制限されることを主張する。
The major limitation is that standard language models are unidirectional, and this limits the choice of architectures that can be used during pre-training.
主な制限は、標準的な言語モデルは一方向性(=next-token-predictionって意味?)であるため、事前学習時に使用できるアーキテクチャの選択肢が制限されることである。
For example, in OpenAI GPT, the authors use a left-toright architecture, where every token can only attend to previous tokens in the self-attention layers of the Transformer (Vaswani et al., 2017).
例えば、OpenAI GPTでは、著者らは**left-torightアーキテクチャ**を使用しており、各トークンはTransformerのself-attention層で前のトークンにしかattentionできない（Vaswani et al, 2017）.(確かattention weightの計算時に対象tokenよりも time step の古いtokenのみを使う様にmaskを導入してた...!. でもこれはnext-token-predictionタスクとしては自然なarchitectureに思える...!)
Such restrictions are sub-optimal for sentence-level tasks, and could be very harmful when applying finetuning based approaches to token-level tasks such as question answering, where it is crucial to incorporate context from both directions.
**このような制限は文レベルのタスクには最適ではなく**、質問応答のようなトークンレベルのタスクにファインチューニングに基づくアプローチを適用する場合、**双方向(both directions)からのコンテキストを取り込むことが重要**であるため、非常に有害である可能性がある.
In this paper, we improve the fine-tuning based approaches by proposing BERT: Bidirectional Encoder Representations from Transformers.
本稿では、**BERT（Bidirectional Encoder Representations from Transformers）**を提案することで、fine-tuningベースのアプローチを改善する。
BERT alleviates the previously mentioned unidirectionality constraint by using a “masked language model” (MLM) pre-training objective, inspired by the Cloze task (Taylor, 1953).
BERT は、Cloze 課題（Taylor, 1953）に着想を得た “masked language model”（MLM）事前学習目的(=事前学習時の目的関数の意味??)を使用することで、前述の単方向性制約を緩和している.
The masked language model randomly masks some of the tokens from the input, and the objective is to predict the original vocabulary id of the masked word based only on its context.
マスク言語モデルは、**入力からいくつかのトークンをランダムにマスク**し、その文脈のみに基づいてマスクされた単語の元の語彙IDを予測することを目的とする.(next-token-predictionではなく、masked-token-predictionみたいな...??)
Unlike left-toright language model pre-training, the MLM objective enables the representation to fuse the left and the right context, which allows us to pretrain a deep bidirectional Transformer.
left-torightの言語モデルの事前学習とは異なり、**MLMの目的関数は左右の文脈を融合する表現を可能にし、deep bi-directional Transformerの事前学習を可能にする**.
In addition to the masked language model, we also use a “next sentence prediction” task that jointly pretrains text-pair representations.
マスクされた言語モデルに加え、テキストペア表現を共同で事前学習する **“next sentence prediction”タスク** も使用する. (i.e. 2つの目的関数を使って、事前学習するって事...??)
The contributions of our paper are as follows:
本稿の貢献は以下の通りである：

- We demonstrate the importance of bidirectional pre-training for language representations. Unlike Radford et al. (2018), which uses unidirectional language models for pre-training, BERT uses masked language models to enable pretrained deep bidirectional representations. This is also in contrast to Peters et al. (2018a), which uses a shallow concatenation of independently trained left-to-right and right-to-left LMs. **言語表現(=言語から特徴量を良い感じに抽出する事??)における双方向の事前学習の重要性**を示す。 事前学習に一方向性言語モデル(i.e. next-token-predictionタスクを学習させる...!)を使用するRadford et al(2018)とは異なり、BERTはmasked言語モデル(i.e. masked-token-predictionタスクを学習させる...!)を使用し、深い双方向表現の事前学習を可能にする。 これは、独立に訓練された左から右へのLMと右から左へのLMの浅い連結を使用するPetersら(2018a)とも対照的である。

- We show that pre-trained representations reduce the need for many heavily-engineered taskspecific architectures. BERT is the first finetuning based representation model that achieves state-of-the-art performance on a large suite of sentence-level and token-level tasks, outperforming many task-specific architectures. 我々は、**事前に訓練された表現(=token表現?sentence表現?)が、多くの重く設計されたタスク固有のアーキテクチャの必要性を減らすこと**を示す。 BERTは、文レベルおよびトークンレベルの大規模なタスク群で最先端の性能を達成し、多くのタスク固有のアーキテクチャを凌駕する、fine-tuningに基づく初の表現モデルである.

- BERT advances the state of the art for eleven NLP tasks. The code and pre-trained models are available at https://github.com/ google-research/bert. BERT は、11 の NLP タスクの最先端技術を前進させる。 コードと訓練済みモデルは、https://github.com/ google-research/bertで入手できる。

# 2. Related Work 関連作品

Related Work There is a long history of pre-training general language representations, and we briefly review the most widely-used approaches in this section.
関連作品 **一般的な言語表現の事前学習には長い歴史**があり、このセクションでは最も広く使われているアプローチを簡単にレビューする。

## 2.1. Unsupervised Feature-based Approaches 教師なし特徴ベース(?)のアプローチ (feature-based = 単語の埋め込みベクトルを使うって意味...??:thinking:)

Learning widely applicable representations of words has been an active area of research for decades, including non-neural (Brown et al., 1992; Ando and Zhang, 2005; Blitzer et al., 2006) and neural (Mikolov et al., 2013; Pennington et al., 2014) methods.
非ニューラル（Brown et al, 1992; Ando and Zhang, 2005; Blitzer et al, 2006）やニューラル（Mikolov et al, 2013; Pennington et al, 2014）の方法を含め、単語の広く適用可能な表現を学習すること(=あ、基本的には単語表現の学習なんだ...!)は、数十年にわたり活発な研究分野である。
Pre-trained word embeddings are an integral part of modern NLP systems, offering significant improvements over embeddings learned from scratch (Turian et al., 2010).
**事前に学習された単語埋め込みは、最新の自然言語処理システムに不可欠な要素**であり、ゼロから学習した埋め込みよりも大幅に改善される（Turian et al.）
To pretrain word embedding vectors, left-to-right language modeling objectives have been used (Mnih and Hinton, 2009), as well as objectives to discriminate correct from incorrect words in left and right context (Mikolov et al., 2013).
単語埋め込みベクトルの事前学習には、左から右への言語モデリング目標（Mnih and Hinton, 2009）や、左右の文脈で正しい単語と正しくない単語を識別する目標（Mikolov et al. 2013）

These approaches have been generalized to coarser granularities, such as sentence embeddings (Kiros et al., 2015; Logeswaran and Lee, 2018) or paragraph embeddings (Le and Mikolov, 2014).
**これらのアプローチは、文埋め込み（Kiros et al, 2015; Logeswaran and Lee, 2018）や段落埋め込み（Le and Mikolov, 2014）など、より粗い粒度に一般化されている**. (このあたりはNLP -> RecSys の応用にも関連してそう.)
To train sentence representations, prior work has used objectives to rank candidate next sentences (Jernite et al., 2017; Logeswaran and Lee, 2018), left-to-right generation of next sentence words given a representation of the previous sentence (Kiros et al., 2015), or denoising autoencoder derived objectives (Hill et al., 2016).
文の表現を訓練するために、先行研究では、次の文の候補をランク付けする目的関数（Jernite et al, 2017; Logeswaran and Lee, 2018）、前の文の表現を与えられた次の文の単語の左から右への生成（Kiros et al, 2015）、または**ノイズ除去オートエンコーダ由来**(これはたぶんYahooさんの論文みたいな話だと思う...!)の目的関数（Hill et al, 2016）が使用されている。

ELMo and its predecessor (Peters et al., 2017, 2018a) generalize traditional word embedding research along a different dimension.
ELMoとその前身（Peters et al, 2017, 2018a）は、従来の単語埋め込み研究を異なる次元で一般化したものである。
They extract context-sensitive features from a left-to-right and a right-to-left language model.
left-to-right、right-to-left(i.e. previous-token-predictionタスク...??)の言語モデルから文脈に応じた特徴を抽出する。
The contextual representation of each token is the concatenation of the left-to-right and right-to-left representations.
各トークンの文脈表現は、左から右への表現と右から左への表現の連結(=ベクトルをシンプルにconcatenateした感じ...??)である。
When integrating contextual word embeddings with existing task-specific architectures, ELMo advances the state of the art for several major NLP benchmarks (Peters et al., 2018a) including question answering (Rajpurkar et al., 2016), sentiment analysis (Socher et al., 2013), and named entity recognition (Tjong Kim Sang and De Meulder, 2003).
文脈に基づく単語埋め込みを既存のタスク固有のアーキテクチャと統合する場合、ELMoは、質問応答（Rajpurkar et al., 2016）、感情分析（Socher et al., 2013）、および名前付きエンティティ認識（Tjong Kim Sang and De Meulder, 2003）を含む、いくつかの主要なNLPベンチマーク（Peters et al.）でSOTAを進歩させた.
Melamud et al.(2016) proposed learning contextual representations through a task to predict a single word from both left and right context using LSTMs.
Melamudら(2016)は、LSTMを用いて左右両方の文脈から一つの単語を予測する課題を通して文脈表現を学習することを提案した。
Similar to ELMo, their model is feature-based and not deeply bidirectional.
ELMoと同様、彼らのモデルは特徴ベースであり、深い双方向性はない.(双方向だがBERTとは違う、と...??)
Fedus et al.(2018) shows that the cloze task can be used to improve the robustness of text generation models.
Fedusら(2018)は、クローズ課題がテキスト生成モデルの頑健性を向上させるために利用できることを示している。

## 2.2. Unsupervised Fine-tuning Approaches 教師なしfine-tuningアプローチ

As with the feature-based approaches, the first works in this direction only pre-trained word embedding parameters from unlabeled text (Collobert and Weston, 2008).
特徴ベースのアプローチと同様に、この方向での最初の研究は、ラベル付けされていないテキストから単語埋め込みパラメータを事前に訓練したのみである（Collobert and Weston, 2008）。
More recently, sentence or document encoders which produce contextual token representations have been pre-trained from unlabeled text and fine-tuned for a supervised downstream task (Dai and Le, 2015; Howard and Ruder, 2018; Radford et al., 2018).
最近では、文脈トークン表現を生成する文や文書のエンコーダーが、ラベル付けされていないテキストから事前に訓練され、教師ありの下流タスクのためにfine-tuningされている（Dai and Le, 2015; Howard and Ruder, 2018; Radford et al.）
The advantage of these approaches is that few parameters need to be learned from scratch.
**これらのアプローチの利点は、パラメータをゼロから学習する必要がほとんどないこと**だ。
At least partly due to this advantage, OpenAI GPT (Radford et al., 2018) achieved previously state-of-the-art results on many sentencelevel tasks from the GLUE benchmark (Wang et al., 2018a).
**少なくとも部分的にはこの利点により、OpenAI GPT (Radford et al, 2018)はGLUEベンチマーク(Wang et al, 2018a)の多くの文レベルタスクで、以前最先端の結果を達成**した。
Left-to-right language model-ing and auto-encoder objectives have been used for pre-training such models (Howard and Ruder, 2018; Radford et al., 2018; Dai and Le, 2015).
左から右への言語モデル化とオートエンコーダの目的関数は、このようなモデルの事前学習に使用されてきた（Howard and Ruder, 2018; Radford et al, 2018; Dai and Le, 2015）。

## 2.3. Transfer Learning from Supervised Data

There has also been work showing effective transfer from supervised tasks with large datasets, such as natural language inference (Conneau et al., 2017) and machine translation (McCann et al., 2017).
また、自然言語推論（Conneau et al, 2017）や機械翻訳（McCann et al, 2017）のように、大規模なデータセットを持つ**教師ありタスクからの効果的な転移学習**を示す研究もある. (事前学習されたパラメータをfine-tuning = 転移学習 で認識あってる...??:thinking:)
Computer vision research has also demonstrated the importance of transfer learning from large pre-trained models, where an effective recipe is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014).
コンピュータビジョンの研究では、事前に訓練された大規模なモデルからの転移学習の重要性も実証されており、効果的なレシピは、ImageNetで事前に訓練されたモデルをfine-tuningすることである（Deng et al, 2009; Yosinski et al, 2014）.(確かに、CVの分野では教師有り学習で得られたパラメータを使って、個別のタスクに転移学習させる印象があるかも...!:thinking:)

# 3. BERT バート

We introduce BERT and its detailed implementation in this section.
このセクションでは、BERT およびその詳細な実装について紹介する。
There are two steps in our framework: pre-training and fine-tuning.
私たちのフレームワークには、**事前学習とfine-tuningという2つのステップ**がある。
During pre-training, the model is trained on unlabeled data over different pre-training tasks.
事前学習では、モデルは**異なる事前学習タスク**のラベルなしデータで学習される。(masked-token-prediction タスクと next-sentence-predictionタスク??)
For finetuning, the BERT model is first initialized with the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the downstream tasks.
fine-tuningのために、**BERT モデルは、まず事前に訓練されたパラメータで初期化され、下流タスクからのラベル付きデータを使用してすべてのパラメータがfine-tuningされる**. (やっぱりfine-tuning = 転移学習なのかな)
Each downstream task has separate fine-tuned models, even though they are initialized with the same pre-trained parameters.
それぞれの下流タスクは、同じ事前訓練されたパラメータで初期化されているにもかかわらず、別々のfine-tuningされたモデルを持っている。
The question-answering example in Figure 1 will serve as a running example for this section.
図1の質問応答例(=ある下流タスク?)が、このセクションの実行例となる。
A distinctive feature of BERT is its unified architecture across different tasks.
**BERTの特徴は、異なるタスクにわたって統一されたアーキテクチャ**である.
There is minimal difference between the pre-trained architecture and the final downstream architecture.
事前に訓練されたアーキテクチャと最終的なダウンストリーム・アーキテクチャの差はほとんどない.(違いは最終的な出力層の形くらい??)

### 3.0.1. Model Architecture モデル・アーキテクチャ

BERT’s model architecture is a multi-layer bidirectional Transformer encoder based on the original implementation described in Vaswani et al.(2017) and released in the tensor2tensor library.1
BERTのモデルアーキテクチャは、Vaswani et al.(2017)(=Transformerの元論文)で説明され、tensor2tensorライブラリでリリースされたオリジナルの実装に基づく**multi-layer bidirectional Transformer encoder(多層双方向Transformerエンコーダ)**である。
Because the use of Transformers has become common and our implementation is almost identical to the original, we will omit an exhaustive background description of the model architecture and refer readers to Vaswani et al.(2017) as well as excellent guides such as “The Annotated Transformer.”2
Transformerの使用は一般的になっており、我々の実装はオリジナルとほぼ同じであるため、モデルアーキテクチャの徹底的な背景説明は省略し、Vaswani et al.(2017) や、"The Annotated Transformer "のような優れたガイドを読者に紹介する.

In this work, we denote the number of layers (i.e., Transformer blocks) as L, the hidden size as H, and the number of self-attention heads as A.
本研究では、the number of layers (i.e., Transformer blocks)を$L$、hidden size(=なんだろう...FFNの隠れ層の次元数?? いや多分出力される各tokenのhidden stateの次元数!)を $H$、self-attentionのhead数を $A$ と定義する.
We primarily report results on two model sizes: BERTBASE (L=12, H=768, A=12, Total Parameters=110M) and BERTLARGE (L=24, H=1024, A=16, Total Parameters=340M).
本研究は、2つのモデルサイズの結果を報告する: BERTBASE (L=12, H=768, A=12, Total Parameters=110M)とBERTLARGE (L=24, H=1024, A=16, Total Parameters=340M)である.

BERTBASE was chosen to have the same model size as OpenAI GPT for comparison purposes.
BERTBASEは、比較のためにOpenAI GPTと同じモデルサイズを選択した。
Critically, however, the BERT Transformer uses bidirectional self-attention, while the GPT Transformer uses constrained self-attention where every token can only attend to context to its left.4
しかし、決定的に重要なのは、BERTトランスフォーマーは双方向のself-attentionを使用するのに対して、GPTトランスフォーマーは制約された(i.e. left-to-rightの...!)self-attentionを使用することである。(この違いを本論文では評価して、双方向の方が一方向よりも効果的である事を主張したい...!:thinking:)

### 3.0.2. Input/Output Representations 入出力表現

To make BERT handle a variety of down-stream tasks, our input representation is able to unambiguously represent both a single sentence and a pair of sentences (e.g., h Question, Answeri) in one token sequence.
BERT が様々なダウンストリームタスクを処理できるようにするために、我々の入力表現は、1つのtoken sequenceとして、"単一文" と "文のペア(例えば、Question、 Answer)" の両方を明確に表現することができる.(どっちでも良いって話...!)
Throughout this work, a “sentence” can be an arbitrary span of contiguous text, rather than an actual linguistic sentence.
本論文を通して、**"sentence"は必ずしも実際の言語文ではなく、連続したテキストの任意のスパン**を意味する.
A “sequence” refers to the input token sequence to BERT, which may be a single sentence or two sentences packed together.
**“sequence”とは、BERT への入力トークン列**を指し、**1つの文または 2 つの文が一緒になっている場合がある**。

We use WordPiece embeddings (Wu et al., 2016) with a 30,000 token vocabulary.
我々は 30,000トークンの語彙を持つWordPiece埋め込み（Wu et al, 2016）を使用する. (i.e. sequence内の各tokenの特徴量としての単語埋め込み表現)
The first token of every sequence is always a special classification token ([CLS]).
**すべてのシーケンスの最初のトークンは常に特別な分類トークン([CLS])**である. (ほうほう...??)
The final hidden state corresponding to this token is used as the aggregate sequence representation for classification tasks.
**このトークンに対応する最終的な隠れ状態(=encoderの最終的な出力って意味かな...??)は、分類タスクのための集約sequence表現として使用される**.
Sentence pairs are packed together into a single sequence.
文のペアは1つのシーケンスにまとめられている.
We differentiate the sentences in two ways.
我々は**2つの方法で文章を区別**している.(i.e. sequence内のtokenが文Aのものか文Bのものか!)
First, we separate them with a special token ([SEP]).
まず、特別なトークン（[SEP]）で区切る.
Second, we add a learned embedding to every token indicating whether it belongs to sentence A or sentence B.
次に、すべてのトークンに、それが文Aに属するか文Bに属するかを示す学習済みの埋め込みを追加する. (tokenの埋め込みにconcatenateする感じ??)
As shown in Figure 1, we denote input embedding as E, the final hidden vector of the special [CLS] token as C ∈ R H, and the final hidden vector for the i th input token as Ti ∈ R H.
図1に示すように、入力埋め込みをE、特殊[CLS]トークンの最終隠れベクトルを$C \in \mathbb{R}^{H}$ 、i番目の入力トークンの最終隠れベクトルを$T_{i} \in \mathbb{R}^{H}$ とする。

For a given token, its input representation is constructed by summing the corresponding token, segment, and position embeddings.
与えられたトークン に対して、その**入力表現は、対応するトークン(=単語の意味表現 $E_{token}$)、segment(=文Aか文Bかの埋め込み. $E_{A}$ or $E_{B}$)、および positon embeddings($E_{idx}$) を合計(=concatenateではなくsum!!)する**ことによって構築される.
A visualization of this construction can be seen in Figure 2.
この構造を視覚化したものが図2である.(わかりやす！)

![figure2]()

## 3.1. Pre-training BERT

Unlike Peters et al.(2018a) and Radford et al.(2018), we do not use traditional left-to-right or right-to-left language models to pre-train BERT.
Petersら(2018a)やRadfordら(2018)とは異なり、BERTの事前学習に従来の左から右、あるいは右から左の言語モデルは使わない。
Instead, we pre-train BERT using two unsupervised tasks, described in this section.
その代わりに、このセクションで説明する 2 つの教師なしタスクを使用して、BERT を事前訓練する。
This step is presented in the left part of Figure 1.
このステップは図1の左側に示されている。

### 3.1.1. Task #1: Masked LM タスク#1： マスクLM

Intuitively, it is reasonable to believe that a deep bidirectional model is strictly more powerful than either a left-to-right model or the shallow concatenation of a left-toright and a right-to-left model.
直感的には、深い双方向モデルは、左から右へのモデルや、左から右へのモデルと右から左へのモデルの浅い連結よりも、厳密に強力であると考えるのが妥当である。
Unfortunately, standard conditional language models can only be trained left-to-right or right-to-left, since bidirectional conditioning would allow each word to indirectly “see itself”, and the model could trivially predict the target word in a multi-layered context.
残念ながら、標準的な条件付き言語モデルは、左から右、または右から左にしか学習できない。双方向の条件付けを行えば、各単語が間接的に「自分自身を見る」ことができ、モデルは多層的な文脈の中でターゲットとなる単語を些細なことでも予測できるようになるからだ。

In order to train a deep bidirectional representation, we simply mask some percentage of the input tokens at random, and then predict those masked tokens.
深い双方向表現を訓練するためには、入力トークンの何割かをランダムにマスクし、マスクされたトークンを予測すればよい。
We refer to this procedure as a “masked LM” (MLM), although it is often referred to as a Cloze task in the literature (Taylor, 1953).
文献ではCloze課題（Taylor, 1953）と呼ばれることが多いが、我々はこの手順を "masked LM"（MLM）と呼んでいる。
In this case, the final hidden vectors corresponding to the mask tokens are fed into an output softmax over the vocabulary, as in a standard LM.
この場合、マスクトークンに対応する最終的な隠れベクトルは、標準的なLMと同様に、語彙に対する出力ソフトマックスに供給される。
In all of our experiments, we mask 15% of all WordPiece tokens in each sequence at random.
すべての実験において、各シーケンスに含まれるWordPieceトークンの15%をランダムにマスクした。
In contrast to denoising auto-encoders (Vincent et al., 2008), we only predict the masked words rather than reconstructing the entire input.
ノイズ除去オートエンコーダ（Vincent et al, 2008）とは対照的に、入力全体を再構成するのではなく、マスクされた単語のみを予測する。
Although this allows us to obtain a bidirectional pre-trained model, a downside is that we are creating a mismatch between pre-training and fine-tuning, since the [MASK] token does not appear during fine-tuning.
これによって双方向の事前学習済みモデルを得ることができるが、欠点は、事前学習とfine-tuningの間にミスマッチが生じることである。
To mitigate this, we do not always replace “masked” words with the actual [MASK] token.
これを軽減するため、「マスク」された単語を実際の[MASK]トークンに置き換えるとは限らない。
The training data generator chooses 15% of the token positions at random for prediction.
学習データ生成器は、トークンの位置の15％をランダムに選んで予測する。
If the i-th token is chosen, we replace the i-th token with (1) the [MASK] token 80% of the time (2) a random token 10% of the time (3) the unchanged i-th token 10% of the time.
i番目のトークンが選択された場合、i番目のトークンを(1)80％の確率で[MASK]トークンに置き換える(2)10％の確率でランダムなトークンに置き換える(3)10％の確率で変更前のi番目のトークンに置き換える。
Then, Ti will be used to predict the original token with cross entropy loss.
そして、Tiはクロスエントロピー損失で元のトークンを予測するために使われる。
We compare variations of this procedure in Appendix C.2.
付録C.2でこの手順のバリエーションを比較する。

### 3.1.2. Task #2: Next Sentence Prediction (NSP) タスク #2: 次の文の予測 (NSP)

Many important downstream tasks such as Question Answering (QA) and Natural Language Inference (NLI) are based on understanding the relationship between two sentences, which is not directly captured by language modeling.
質問応答（QA）や自然言語推論（NLI）のような多くの重要な下流タスクは、言語モデリングでは直接捉えられない2つの文の関係を理解することに基づいている。
In order to train a model that understands sentence relationships, we pre-train for a binarized next sentence prediction task that can be trivially generated from any monolingual corpus.
文の関係を理解するモデルを訓練するために、任意のモノリンガルコーパスから些細なことで生成できる二値化された次文予測タスクの事前訓練を行う。
Specifically, when choosing the sentences A and B for each pretraining example, 50% of the time B is the actual next sentence that follows A (labeled as IsNext), and 50% of the time it is a random sentence from the corpus (labeled as NotNext).
具体的には、各予習例で文Aと文Bを選択する際、50％の確率で文BはAに続く実際の次の文（IsNextとラベル付け）であり、50％の確率でコーパスからのランダムな文（NotNextとラベル付け）である。
As we show in Figure 1, C is used for next sentence prediction (NSP).5 Despite its simplicity, we demonstrate in Section 5.1 that pre-training towards this task is very beneficial to both QA and NLI.6
図1に示すように、Cは次文予測（NSP）に使用される5。その単純さにもかかわらず、このタスクに向けた事前学習がQAとNLIの両方にとって非常に有益であることをセクション5.1で示す6。

The NSP task is closely related to representationlearning objectives used in Jernite et al.(2017) and Logeswaran and Lee (2018).
NSPタスクは、Jerniteら(2017)やLogeswaran and Lee(2018)で用いられた表現学習目標と密接に関連している。
However, in prior work, only sentence embeddings are transferred to down-stream tasks, where BERT transfers all parameters to initialize end-task model parameters.
しかし、先行研究では、文埋め込みのみがダウンストリームタスクに転送されるのに対し、BERT はエンドタスクモデルパラメータを初期化するためにすべてのパラメータを転送する。

### 3.1.3. Pre-training data 事前学習データ

The pre-training procedure largely follows the existing literature on language model pre-training.
事前学習手順は、言語モデルの事前学習に関する既存の文献にほぼ従っている。
For the pre-training corpus we use the BooksCorpus (800M words) (Zhu et al., 2015) and English Wikipedia (2,500M words).
事前学習コーパスには、BooksCorpus（800M語）（Zhu et al, 2015）と英語版ウィキペディア（2,500M語）を使用する。
For Wikipedia we extract only the text passages and ignore lists, tables, and headers.
ウィキペディアの場合、テキスト部分のみを抽出し、リスト、表、ヘッダーは無視する。
It is critical to use a document-level corpus rather than a shuffled sentence-level corpus such as the Billion Word Benchmark (Chelba et al., 2013) in order to extract long contiguous sequences.
長い連続シーケンスを抽出するためには、Billion Word Benchmark (Chelba et al., 2013)のようなシャッフルされた文レベルのコーパスではなく、文書レベルのコーパスを使用することが重要である。

## 3.2. Fine-tuning BERT BERTのfine-tuning

Fine-tuning is straightforward since the selfattention mechanism in the Transformer allows BERT to model many downstream tasks— whether they involve single text or text pairs—by swapping out the appropriate inputs and outputs.
Transformer の自己注 意メカニズムにより、BERT は、適切な入力と出力を入れ替えることによって、単一のテキストまたはテキストペアを含むかどうかに関係なく、 多くの下流タスクをモデル化することができるため、fine-tuningは簡単です。
For applications involving text pairs, a common pattern is to independently encode text pairs before applying bidirectional cross attention, such as Parikh et al.(2016); Seo et al.(2017).
テキストペアを含むアプリケーションの場合、Parikhら(2016); Seoら(2017)のように、双方向交差注意を適用する前にテキストペアを独立してエンコードするのが一般的なパターンである。
BERT instead uses the self-attention mechanism to unify these two stages, as encoding a concatenated text pair with self-attention effectively includes bidirectional cross attention between two sentences.
BERT は、自己注意を用いて連結されたテキストペアを符号化することで、2 つの文の間の双方向の相互注意を効果的に含むため、代わりに自己注意メカニズムを使用して、これらの 2 つの段階を統一する。
For each task, we simply plug in the taskspecific inputs and outputs into BERT and finetune all the parameters end-to-end.
各タスクについて、タスク固有の入出力をBERTに単純にプラグインし、すべてのパラメーターをエンドツーエンドでfine-tuningする。
At the input, sentence A and sentence B from pre-training are analogous to (1) sentence pairs in paraphrasing, (2) hypothesis-premise pairs in entailment, (3) question-passage pairs in question answering, and (4) a degenerate text-∅ pair in text classification or sequence tagging.
入力において、事前学習による文Aと文Bは、(1)言い換えにおける文のペア、(2)含意における仮説と前提のペア、(3)質問応答における質問とパッセージのペア、(4)テキスト分類や配列タグ付けにおける退化したテキストとφのペアに類似している。
At the output, the token representations are fed into an output layer for tokenlevel tasks, such as sequence tagging or question answering, and the [CLS] representation is fed into an output layer for classification, such as entailment or sentiment analysis.
出力では、トークン表現は、シーケンス・タグ付けや質問応答などのトークン・レベルのタスクのための出力層に供給され、[CLS]表現は、含意分析やセンチメント分析などの分類のための出力層に供給される。
Compared to pre-training, fine-tuning is relatively inexpensive.
事前トレーニングに比べ、fine-tuningは比較的安価である。
All of the results in the paper can be replicated in at most 1 hour on a single Cloud TPU, or a few hours on a GPU, starting from the exact same pre-trained model.7 We describe the task-specific details in the corresponding subsections of Section 4.
本稿の結果はすべて、全く同じ事前学習済みモデルから始めて、1つのCloud TPUで最大1時間、GPUで数時間で再現できる7。
More details can be found in Appendix A.5.
詳細は付録A.5を参照されたい。

# 4. Experiments 実験

In this section, we present BERT fine-tuning results on 11 NLP tasks.
このセクションでは、11 の NLP タスクに関する BERT のfine-tuning結果を示す。

## 4.1. GLUE ♪グルー

The General Language Understanding Evaluation (GLUE) benchmark (Wang et al., 2018a) is a collection of diverse natural language understanding tasks.
一般言語理解評価（GLUE）ベンチマーク（Wang et al, 2018a）は、多様な自然言語理解タスクを集めたものである。
Detailed descriptions of GLUE datasets are included in Appendix B.1.To fine-tune on GLUE, we represent the input sequence (for single sentence or sentence pairs) as described in Section 3, and use the final hidden vector C ∈ R H corresponding to the first input token ([CLS]) as the aggregate representation.
GLUEデータセットの詳細な説明は付録B.1に含まれている。GLUEでfine-tuningを行うために、セクション3で説明したように入力シーケンス（単一センテンスまたはセンテンスペア）を表現し、最初の入力トークン（[CLS]）に対応する最終的な隠れベクトルC∈R Hを集約表現として使用する。
The only new parameters introduced during fine-tuning are classification layer weights W ∈ R K×H, where K is the number of labels.
fine-tuningの際に導入される唯一の新しいパラメータは、分類層の重みW∈R K×H（K はラベルの数）である。
We compute a standard classification loss with C and W, i.e., log(softmax(CWT )).
CとWによる標準的な分類損失、すなわちlog(softmax(CWT ))を計算する。

We use a batch size of 32 and fine-tune for 3 epochs over the data for all GLUE tasks.
バッチサイズ32を使用し、すべてのGLUEタスクのデータに対して3エポックでfine-tuningを行う。
For each task, we selected the best fine-tuning learning rate (among 5e-5, 4e-5, 3e-5, and 2e-5) on the Dev set.
各タスクについて、Devセットで最適なfine-tuning学習率（5e-5、4e-5、3e-5、2e-5の中から）を選択した。
Additionally, for BERTLARGE we found that finetuning was sometimes unstable on small datasets, so we ran several random restarts and selected the best model on the Dev set.
さらにBERTLARGEでは、小さなデータセットではファインチューニングが不安定になることがあることがわかったので、何度かランダムな再スタートを実行し、Devセットで最良のモデルを選択した。
With random restarts, we use the same pre-trained checkpoint but perform different fine-tuning data shuffling and classifier layer initialization.9 Results are presented in Table 1.
ランダム再スタートでは、同じ事前学習済みチェックポイントを使用するが、異なるfine-tuningデータシャッフリングと分類器レイヤーの初期化を実行する9。
Both BERTBASE and BERTLARGE outperform all systems on all tasks by a substantial margin, obtaining 4.5% and 7.0% respective average accuracy improvement over the prior state of the art.
BERTBASEとBERTLARGEは、すべてのタスクにおいてすべてのシステムを大幅に凌駕し、従来の技術水準に対してそれぞれ4.5%と7.0%の平均精度向上を達成した。
Note that BERTBASE and OpenAI GPT are nearly identical in terms of model architecture apart from the attention masking.
BERTBASEとOpenAI GPTは、アテンション・マスキングを除けば、モデル・アーキテクチャがほぼ同じであることに注意してください。
For the largest and most widely reported GLUE task, MNLI, BERT obtains a 4.6% absolute accuracy improvement.
最大かつ最も広く報告されている GLUE タスクである MNLI に対して、BERT は 4.6%の絶対精度向上を得た。
On the official GLUE leaderboard10, BERTLARGE obtains a score of 80.5, compared to OpenAI GPT, which obtains 72.8 as of the date of writing.
GLUEの公式リーダーボード10では、BERTLARGEは80.5点を獲得しており、OpenAI GPTは72.8点である。
We find that BERTLARGE significantly outperforms BERTBASE across all tasks, especially those with very little training data.
我々は、BERTLARGEが全てのタスク、特に学習データが非常に少ないタスクにおいてBERTBASEを大幅に上回ることを発見した。
The effect of model size is explored more thoroughly in Section 5.2.
モデル・サイズの効果については、セクション5.2で詳しく説明する。

## 4.2. SQuAD v1.1 SQuAD v1.1

The Stanford Question Answering Dataset (SQuAD v1.1) is a collection of 100k crowdsourced question/answer pairs (Rajpurkar et al., 2016).
Stanford Question Answering Dataset (SQuAD v1.1)は、100kのクラウドソースされた質問と回答のペアのコレクションである（Rajpurkar et al, 2016）。
Given a question and a passage from Wikipedia containing the answer, the task is to predict the answer text span in the passage.
質問と答えを含むウィキペディアの文章が与えられたら、その文章中の答えを予測する。
As shown in Figure 1, in the question answering task, we represent the input question and passage as a single packed sequence, with the question using the A embedding and the passage using the B embedding.
図1に示すように、質問回答タスクでは、入力された質問と文章を1つのパックされたシーケンスとして表現し、質問にはAエンベッディングを、文章にはBエンベッディングを使用する。
We only introduce a start vector S ∈ R H and an end vector E ∈ R H during fine-tuning.
fine-tuningの際には、開始ベクトルS（R H）と終了ベクトルE（R H）のみを導入する。
The probability of word i being the start of the answer span is computed as a dot product between Ti and S followed by a softmax over all of the words in the paragraph: Pi = e S·Ti P j e S·Tj .
単語 i が回答スパンの開始である確率は、Ti と S の間のドット積として計算され、段落内のすべての単語に対するソフトマックスが続きます： Pi = e S-Ti P j e S-Tj .
The analogous formula is used for the end of the answer span.
同様の式が、解答スパンの終わりにも使われる。
The score of a candidate span from position i to position j is defined as S·Ti + E·Tj , and the maximum scoring span where j ≥ i is used as a prediction.
位置iから位置jまでのスパン候補のスコアは、S-Ti＋E-Tjと定義され、j≧iとなる最大スコアのスパンが予測値として使用される。
The training objective is the sum of the log-likelihoods of the correct start and end positions.
訓練目標は、正しい開始位置と終了位置の対数尤度の和である。
We fine-tune for 3 epochs with a learning rate of 5e-5 and a batch size of 32.
学習率5e-5、バッチサイズ32で3エポックfine-tuning。
Table 2 shows top leaderboard entries as well as results from top published systems (Seo et al., 2017; Clark and Gardner, 2018; Peters et al., 2018a; Hu et al., 2018).
表2は、リーダーボードの上位エントリーと、公表された上位システムの結果（Seo et al.）
The top results from the SQuAD leaderboard do not have up-to-date public system descriptions available,11 and are allowed to use any public data when training their systems.
SQuADのリーダーボードで上位にランクインした選手は、最新の公開システムに関する記述がない11。
We therefore use modest data augmentation in our system by first fine-tuning on TriviaQA (Joshi et al., 2017) befor fine-tuning on SQuAD.
したがって、私たちのシステムでは、SQuADでfine-tuningを行う前に、まずTriviaQA（Joshi et al.
Our best performing system outperforms the top leaderboard system by +1.5 F1 in ensembling and +1.3 F1 as a single system.
我々の最高性能のシステムは、アンサンブルで+1.5 F1、単一システムとして+1.3 F1、トップリーダーボードシステムを上回った。
In fact, our single BERT model outperforms the top ensemble system in terms of F1 score.
実際、我々の単一 BERT モデルは、F1 スコアの点でトップのアンサンブルシステムを上回っている。
Without TriviaQA fine tuning data, we only lose 0.1-0.4 F1, still outperforming all existing systems by a wide margin.12
TriviaQAのファインチューニングデータがなければ、0.1～0.4 F1しか失わない。

## 4.3. SQuAD v2.0 SQuAD v2.0

The SQuAD 2.0 task extends the SQuAD 1.1 problem definition by allowing for the possibility that no short answer exists in the provided paragraph, making the problem more realistic.
SQuAD 2.0タスクはSQuAD 1.1の問題定義を拡張し、提供された段落に短い答えが存在しない可能性を許容することで、問題をより現実的なものにしています。
We use a simple approach to extend the SQuAD v1.1 BERT model for this task.
このタスクのために SQuAD v1.1 BERT モデルを拡張する簡単なアプローチを使用する。
We treat questions that do not have an answer as having an answer span with start and end at the [CLS] token.
答えを持たない質問は、[CLS]トークンを始点と終点とする解答スパンを持つものとして扱います。
The probability space for the start and end answer span positions is extended to include the position of the [CLS] token.
アンサースパンの開始位置と終了位置の確率空間は、[CLS]トークンの位置を含むように拡張される。
For prediction, we compare the score of the no-answer span: snull = S·C + E·C to the score of the best non-null span sˆi,j = maxj≥iS·Ti + E·Tj .
予測については、無回答スパンのスコアsnull = S-C + E-C と、最良の無回答スパンのスコアsˆi,j = maxj≥iS-Ti + E-Tj を比較する。
We predict a non-null answer when sˆi,j > snull + τ , where the threshold τ is selected on the dev set to maximize F1.
sˆi,j＞snull＋τのとき、非ヌル回答を予測する。閾値τは、F1を最大化するようにdevセット上で選択される。
We did not use TriviaQA data for this model.
このモデルにはTriviaQAのデータは使用していない。
We fine-tuned for 2 epochs with a learning rate of 5e-5 and a batch size of 48.
学習率5e-5、バッチサイズ48で2エポックfine-tuningした。
The results compared to prior leaderboard entries and top published work (Sun et al., 2018; Wang et al., 2018b) are shown in Table 3, excluding systems that use BERT as one of their components.
BERTをコンポーネントの1つとして使用するシステムを除き、先行するリーダーボードエントリーおよびトップ公開研究（Sun et al, 2018; Wang et al, 2018b）と比較した結果を表3に示す。
We observe a +5.1 F1 improvement over the previous best system.
その結果、以前の最良システムより+5.1 F1向上した。

## 4.4. SWAG SWAG

The Situations With Adversarial Generations (SWAG) dataset contains 113k sentence-pair completion examples that evaluate grounded commonsense inference (Zellers et al., 2018).
Situations With Adversarial Generations（SWAG）データセットには、接地されたコモンセンス推論を評価する113k文対補完例が含まれている（Zellers et al, 2018）。
Given a sentence, the task is to choose the most plausible continuation among four choices.
ある文章が与えられたら、4つの選択肢の中から最も妥当な続きを選ぶ。
When fine-tuning on the SWAG dataset, we construct four input sequences, each containing the concatenation of the given sentence (sentence A) and a possible continuation (sentence B).
SWAGデータセットでfine-tuningを行う場合、与えられた文（文A）と可能性のある続き（文B）を連結した4つの入力シーケンスを構築する。
The only task-specific parameters introduced is a vector whose dot product with the [CLS] token representation C denotes a score for each choice which is normalized with a softmax layer.
タスク固有のパラメータとして導入されるのは、[CLS]トークン表現Cとの内積が各選択肢のスコアを示すベクトルだけで、これはソフトマックス層で正規化される。
We fine-tune the model for 3 epochs with a learning rate of 2e-5 and a batch size of 16.
学習率2e-5、バッチサイズ16のモデルを3エポックでfine-tuning。
Results are presented in Table 4.
結果を表4に示す。
BERTLARGE outperforms the authors’ baseline ESIM+ELMo system by +27.1% and OpenAI GPT by 8.3%.
BERTLARGEは著者のベースラインESIM+ELMoシステムを+27.1%、OpenAI GPTを8.3%上回った。

# 5. Ablation Studies アブレーション研究

In this section, we perform ablation experiments over a number of facets of BERT in order to better understand their relative importance.
本セクションでは、BERTの多くの側面についてアブレーション実験を行い、それらの相対的重要性をよりよく理解する。
Additional ablation studies can be found in Appendix C.
その他のアブレーション研究は付録Cにある。

## 5.1. 5.1 Effect of Pre-training Tasks 5.1 事前トレーニング課題の効果

We demonstrate the importance of the deep bidirectionality of BERT by evaluating two pretraining objectives using exactly the same pretraining data, fine-tuning scheme, and hyperparameters as BERTBASE:
BERTBASEと全く同じ事前学習データ、fine-tuningスキーム、およびハイパーパラメータを使用して、2つの事前学習目標を評価することにより、BERTの深い双方向性の重要性を実証する：

### 5.1.1. No NSP: NSPはない：

A bidirectional model which is trained using the “masked LM” (MLM) but without the “next sentence prediction” (NSP) task.
マスクされたLM」（MLM）を用いて学習されるが、「次文予測」（NSP）タスクは含まない双方向モデル。

### 5.1.2. LTR & No NSP: LTR＆NSPなし：

A left-context-only model which is trained using a standard Left-to-Right (LTR) LM, rather than an MLM.
MLM ではなく、標準的な Left-to-Right (LTR) LM を用いて学習された左文脈のみのモデル。
The left-only constraint was also applied at fine-tuning, because removing it introduced a pre-train/fine-tune mismatch that degraded downstream performance.
この制約を取り除くと、プリ・トレーニングとファイン・チューニングのミスマッチが生じ、下流のパフォーマンスが低下するためだ。
Additionally, this model was pre-trained without the NSP task.
さらに、このモデルはNSPタスクなしで事前訓練された。
This is directly comparable to OpenAI GPT, but using our larger training dataset, our input representation, and our fine-tuning scheme.
これはOpenAIのGPTに直接匹敵しますが、我々のより大きなトレーニングデータセット、入力表現、fine-tuningスキームを使用しています。

We first examine the impact brought by the NSP task.
まず、NSPのタスクがもたらした影響を検証する。
In Table 5, we show that removing NSP hurts performance significantly on QNLI, MNLI, and SQuAD 1.1.Next, we evaluate the impact of training bidirectional representations by comparing “No NSP” to “LTR & No NSP”.
表5では、QNLI、MNLI、SQuAD 1.1において、NSPを取り除くとパフォーマンスが著しく低下することを示している。次に、「NSPなし」と「LTR＆NSPなし」を比較して、双方向表現のトレーニングの影響を評価する。
The LTR model performs worse than the MLM model on all tasks, with large drops on MRPC and SQuAD.
LTRモデルはすべてのタスクでMLMモデルより性能が悪く、MRPCとSQuADでは大きく低下した。
For SQuAD it is intuitively clear that a LTR model will perform poorly at token predictions, since the token-level hidden states have no rightside context.
SQuADの場合、トークン・レベルの隠れた状態には右側の文脈がないため、LTRモデルのトークン予測性能が低いことは直感的に明らかである。
In order to make a good faith attempt at strengthening the LTR system, we added a randomly initialized BiLSTM on top.
LTRシステムの強化を誠実に試みるため、ランダムに初期化されたBiLSTMを追加した。
This does significantly improve results on SQuAD, but the results are still far worse than those of the pretrained bidirectional models.
この結果、SQuADの結果は大幅に改善されたが、それでも訓練前の双方向モデルの結果よりはるかに悪い。
The BiLSTM hurts performance on the GLUE tasks.
BiLSTMはGLUEタスクのパフォーマンスを低下させた。
We recognize that it would also be possible to train separate LTR and RTL models and represent each token as the concatenation of the two models, as ELMo does.
ELMoのように、LTRモデルとRTLモデルを別々に訓練し、各トークンを2つのモデルの連結として表現することも可能であろう。
However: (a) this is twice as expensive as a single bidirectional model; (b) this is non-intuitive for tasks like QA, since the RTL model would not be able to condition the answer on the question; (c) this it is strictly less powerful than a deep bidirectional model, since it can use both left and right context at every layer.
(b)RTLモデルは質問に対する答えを条件付けることができないため、QAのようなタスクには直感的でない。(c)すべてのレイヤーで左右両方のコンテキストを使用できるため、ディープ双方向モデルよりも厳密には劣る。

## 5.2. Effect of Model Size モデルサイズの効果

In this section, we explore the effect of model size on fine-tuning task accuracy.
このセクションでは、モデルのサイズがfine-tuningタスクの精度に与える影響を探る。
We trained a number of BERT models with a differing number of layers, hidden units, and attention heads, while otherwise using the same hyperparameters and training procedure as described previously.
我々は、層数、隠れユニット数、および注意ヘッド数が異なる多数の BERT モデルを訓練したが、それ以外は、前述と同じハイパーパラメータと訓練手順を使用した。
Results on selected GLUE tasks are shown in Table 6.
GLUEタスクの結果を表6に示す。
In this table, we report the average Dev Set accuracy from 5 random restarts of fine-tuning.
この表では、5回のランダムなfine-tuningの再スタートから得られた平均Dev Set精度を報告する。
We can see that larger models lead to a strict accuracy improvement across all four datasets, even for MRPC which only has 3,600 labeled training examples, and is substantially different from the pre-training tasks.
より大きなモデルは、4つのデータセットすべてにおいて厳密な精度向上につながることがわかります。MRPCの場合は、3,600のラベル付き訓練例しかなく、訓練前のタスクとは大きく異なります。
It is also perhaps surprising that we are able to achieve such significant improvements on top of models which are already quite large relative to the existing literature.
また、既存の文献と比較してすでにかなり大規模なモデルの上に、このような大幅な改善を達成できたことも驚くべきことかもしれない。
For example, the largest Transformer explored in Vaswani et al.(2017) is (L=6, H=1024, A=16) with 100M parameters for the encoder, and the largest Transformer we have found in the literature is (L=64, H=512, A=2) with 235M parameters (Al-Rfou et al., 2018).
例えば、Vaswani et al.(2017)で探索された最大のTransformerは、エンコーダーの100Mパラメータを持つ(L=6, H=1024, A=16)であり、我々が文献で見つけた最大のTransformerは、235Mパラメータを持つ(L=64, H=512, A=2)である(Al-Rfou et al., 2018)。
By contrast, BERTBASE contains 110M parameters and BERTLARGE contains 340M parameters.
対照的に、BERTBASEは110Mのパラメータを含み、BERTLARGEは340Mのパラメータを含む。
It has long been known that increasing the model size will lead to continual improvements on large-scale tasks such as machine translation and language modeling, which is demonstrated by the LM perplexity of held-out training data shown in Table 6.
機械翻訳や言語モデリングのような大規模なタスクでは、モデルサイズを大きくすることが継続的な改善につながることは以前から知られている。
However, we believe that this is the first work to demonstrate convincingly that scaling to extreme model sizes also leads to large improvements on very small scale tasks, provided that the model has been sufficiently pre-trained.
しかし、モデルが十分に事前訓練されていれば、極端なモデルサイズへのスケーリングが非常に小規模なタスクでも大きな改善につながることを、説得力を持って実証した最初の研究だと考えている。
Peters et al.(2018b) presented mixed results on the downstream task impact of increasing the pre-trained bi-LM size from two to four layers and Melamud et al.(2016) mentioned in passing that increasing hidden dimension size from 200 to 600 helped, but increasing further to 1,000 did not bring further improvements.
Petersら(2018b)は、事前に訓練されたbi-LMのサイズを2層から4層に増やした場合の下流タスクへの影響について、さまざまな結果を示しており、Melamudら(2016)は、隠れ次元サイズを200から600に増やすことは助けになったが、さらに1,000に増やしてもそれ以上の改善はもたらさなかったと一応言及している。
Both of these prior works used a featurebased approach — we hypothesize that when the model is fine-tuned directly on the downstream tasks and uses only a very small number of randomly initialized additional parameters, the taskspecific models can benefit from the larger, more expressive pre-trained representations even when downstream task data is very small.
これらの先行研究はいずれも特徴ベースのアプローチを用いている。我々は、モデルが下流のタスク上で直接fine-tuningされ、非常に少数のランダムに初期化された追加パラメータのみを使用する場合、下流のタスクデータが非常に少ない場合でも、タスク固有のモデルは、より大きく、より表現力の高い事前訓練された表現から恩恵を受けることができるという仮説を立てている。

## 5.3. Feature-based Approach with BERT BERTによる特徴ベースのアプローチ

All of the BERT results presented so far have used the fine-tuning approach, where a simple classification layer is added to the pre-trained model, and all parameters are jointly fine-tuned on a downstream task.
これまでに発表された BERT の結果はすべて、事前に訓練されたモデルに単純な分類層を追加し、すべてのパ ラメータを下流のタスク上で共同でfine-tuningする、fine-tuningアプローチを使用している。
However, the feature-based approach, where fixed features are extracted from the pretrained model, has certain advantages.
しかし、事前に訓練されたモデルから固定的な特徴を抽出する特徴ベースのアプローチには、一定の利点がある。
First, not all tasks can be easily represented by a Transformer encoder architecture, and therefore require a task-specific model architecture to be added.
まず、すべてのタスクがTransformerエンコーダーアーキテクチャで簡単に表現できるわけではないため、タスク固有のモデルアーキテクチャを追加する必要がある。
Second, there are major computational benefits to pre-compute an expensive representation of the training data once and then run many experiments with cheaper models on top of this representation.
第二に、学習データの高価な表現を一度事前に計算し、その上でより安価なモデルで多くの実験を行うことは、計算上大きなメリットがある。
In this section, we compare the two approaches by applying BERT to the CoNLL-2003 Named Entity Recognition (NER) task (Tjong Kim Sang and De Meulder, 2003).
このセクションでは、CoNLL-2003 Named Entity Recognition（NER）タスク（Tjong Kim Sang and De Meulder, 2003）に BERT を適用して、2 つのアプローチを比較する。
In the input to BERT, we use a case-preserving WordPiece model, and we include the maximal document context provided by the data.
BERT への入力では、大文字と小文字を区別する WordPiece モデルを使用し、データによって提供される最大 の文書コンテキストを含める。
Following standard practice, we formulate this as a tagging task but do not use a CRF layer in the output.
標準的な手法に従い、タグ付けタスクとして定式化するが、出力にCRFレイヤーは使用しない。
We use the representation of the first sub-token as the input to the token-level classifier over the NER label set.
最初のサブ・トークンの表現を、NERラベル・セットに対するトークン・レベル分類器の入力として使用する。
To ablate the fine-tuning approach, we apply the feature-based approach by extracting the activations from one or more layers without fine-tuning any parameters of BERT.
fine-tuningアプローチを排除するために、BERT のパラメータをfine-tuningすることなく、1 つまたは複数の層からアクティ ブを抽出することによって、特徴ベースのアプローチを適用する。
These contextual embeddings are used as input to a randomly initialized two-layer 768-dimensional BiLSTM before the classification layer.
これらの文脈埋め込みは、分類層の前にランダムに初期化された768次元の2層BiLSTMの入力として使われる。
Results are presented in Table 7.
結果を表7に示す。
BERTLARGE performs competitively with state-of-the-art methods.
BERTLARGEは、最先端の手法と遜色ない性能を発揮する。
The best performing method concatenates the token representations from the top four hidden layers of the pre-trained Transformer, which is only 0.3 F1 behind fine-tuning the entire model.
最もパフォーマンスの高い方法は、事前に訓練されたTransformerの上位4つの隠れ層からトークン表現を連結するもので、モデル全体をfine-tuningするのと0.3F1しか変わらない。
This demonstrates that BERT is effective for both finetuning and feature-based approaches.
このことは、BERTがfine-tuningと特徴ベースのアプローチの両方に有効であることを示している。

# 6. Conclusion 結論

Recent empirical improvements due to transfer learning with language models have demonstrated that rich, unsupervised pre-training is an integral part of many language understanding systems.
近年の言語モデルによる転移学習による経験的な改善により、多くの言語理解システムにおいて、教師なしでの豊富な事前学習が不可欠であることが実証されている。
In particular, these results enable even low-resource tasks to benefit from deep unidirectional architectures.
特に、これらの結果は、低リソースのタスクでさえ、深い一方向アーキテクチャの恩恵を受けることを可能にする。
Our major contribution is further generalizing these findings to deep bidirectional architectures, allowing the same pre-trained model to successfully tackle a broad set of NLP tasks.
我々の大きな貢献は、これらの発見を深層双方向アーキテクチャに一般化することで、同じ事前学習済みモデルで幅広い自然言語処理タスクに取り組むことを可能にしたことである。
