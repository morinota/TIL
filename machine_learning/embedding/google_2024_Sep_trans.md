## refs 審判

<https://medium.com/google-cloud/embeddings-how-to-select-the-right-one-135032315709>
<https://medium.com/google-cloud/embeddings-how-to-select-the-right-one-135032315709>

# Embeddings: How to select the right one? エンベッディング 正しいものを選ぶには？

Notes from my reading in quest to answer questions like:
以下の質問に答えるために読書したメモ:

How do I choose the right embedding model for a task?
タスクに適したエンベデッドモデルを選ぶには？

Will the same embedding model work for all my tasks?
同じエンベデッドモデルが、すべてのタスクに適用されるのでしょうか？

How can I evaluate an embedding model for a given task?
与えられたタスクに対する埋め込みモデルを評価するには？

How do I detect bias in embedding model?
埋め込みモデルのバイアスを検出するには？

Is the model with higher number of dimensions always the best choice?
次元数の多いモデルが常に最良の選択なのか？

## What are Embeddings? エンベッディングとは？

Imagine trying to explain the taste of an apple to someone who’s never had one.
リンゴを食べたことのない人にリンゴの味を説明しようとするのを想像してみてほしい。
You could use words like “sweet,” “crunchy,” and “juicy,” but it’s hard to truly capture the experience.
甘い」、「歯ごたえがある」、「ジューシー」といった言葉を使うことはできても、その経験を本当に表現するのは難しい。
Embeddings are like giving computers a taste of language, helping them understand the meaning and connections between words, even if they don’t “experience” them like we do.
エンベッディングは、コンピューターに言語を体験させるようなもので、私たちのように 「体験 」することはできなくても、言葉の意味やつながりを理解するのに役立つ。

Computers may be intelligent at crunching numbers, but they cannot understand text directly.
コンピューターは数字を計算することには長けているかもしれないが、テキストを直接理解することはできない。
Words, text and documents need to be converted into numbers for making computers understand them.
コンピュータに理解させるためには、言葉、テキスト、文書を数字に変換する必要がある。

Essentially, embeddings turn words and phrases into special codes that computers can understand.
**基本的に、エンベッディングは単語やフレーズをコンピュータが理解できる特別なコードに変える。** (基本的にはNLP分野のembeddingの話をしてるっぽい...!sparseかdenceかという話ではなさそう:thinking:)
Similar words get codes that are close to each other, while different words get codes that are far apart.
似たような単語には近いコードがつき、違う単語には遠いコードがつく。
This allows computers to “see” how words relate, like understanding that “happy” and “joyful” are similar, while “happy” and “sad” are opposites.
例えば、「嬉しい」と「楽しい」は似ているが、「楽しい」と「悲しい」は正反対である。
Embeddings could be created for words, sentences or documents as well.
エンベッディングは、単語、文、文書に対しても作成できる。

## Why are embeddings becoming important? なぜ埋め込みが重要になるのか？

Embeddings are becoming increasingly important because they help computers handle the massive amounts of text we create every day.
**エンベッディングは、私たちが毎日作成する膨大な量のテキストをコンピュータが処理するのに役立つため、ますます重要になってきている**。(うんうん)
They’re like super-efficient translators, allowing computers to quickly process and understand language, leading to better search results, more accurate translations, and even smarter chatbots.
コンピューターが言語を素早く処理し理解することで、より良い検索結果、より正確な翻訳、そしてさらに賢いチャットボットにつながる。

Think of it like teaching a computer to read between the lines.
コンピューターに行間を読むことを教えるようなものだと思ってください。
Instead of just looking for specific words, embeddings help computers grasp the overall meaning of a sentence or document, leading to more relevant and helpful information.
embeddingsは、特定の単語だけでなく、文や文書の全体的な意味を把握するのを助け、より関連性の高い情報を提供する。

In short, embeddings are like giving computers a secret decoder ring for human language.
要するに、embeddingsは、コンピュータに人間の言語のための秘密のデコーダリングを提供するようなものだ。
They’re helping bridge the gap between how we communicate and how computers understand, making technology more intuitive and useful for everyone.
私たちのコミュニケーション方法とコンピューターが理解する方法のギャップを埋め、テクノロジーをより直感的で誰にとっても便利なものにしている。

## Design Considerations for choosing Embeddings エンベッディングを選択する際の設計上の考慮点

### Dimensionality 次元数

Dimensionality refers to the number of features of the text represented by the embeddings.
次元性とは、埋め込みによって表現されるテキストの特徴の数を指す。
This is the number of numerical values used to represent each word/phrase/document in a vector space.
これは、ベクトル空間で各単語/フレーズ/文書を表現するために使用される数値の数である。
Imagine each word as a point in a multi-dimensional space, where the number of dimensions determines the quality and complexity of this representation.
各単語を多次元空間の点と想像し、次元数によって表現の質と複雑さが決まる。

Quality of Embeddings: Higher dimensionality of embeddings provides more features to capture subtle nuances and relationships between words.
**エンベッディングの質**： エンベッディングの次元を高くすることで、単語間の微妙なニュアンスや関係性を捉えるための特徴を増やすことができる。
This can lead to improved performance in tasks like machine translation, sentiment analysis, and question answering, where context and precision are important.
これにより、機械翻訳、感情分析、質問応答など、文脈と精度が重要なタスクのパフォーマンスを向上させることができる。
Whereas lower dimensionality might not fully capture the semantic richness of words but can be sufficient for simpler tasks like word similarity or document clustering.
一方、次元数が低いと単語の意味的な豊かさを十分に捉えられないかもしれないが、単語の類似性や文書のクラスタリングのような単純なタスクには十分である。

**Latency**: Higher dimensional embeddings results in larger embedding vectors, requiring more memory and computational resources for storage and processing.
遅延： **高次元の埋め込みは埋め込みベクトルが大きくなり、保存と処理に多くのメモリと計算資源を必要とする**。(そりゃそう:thinking:)
This can lead to increased latency, especially in real-time applications or on resource-constrained devices.
これは、特にリアルタイム・アプリケーションやリソースに制約のあるデバイスでは、待ち時間の増加につながる可能性がある。
Lower dimensional embeddings can enable faster processing and reduced latency
低次元のエンベッディングは、より高速な処理と待ち時間の短縮を可能にする。

There are newer embedding models that can handle long context and variable dimensions
長い文脈や可変次元(OpenAIのやつとか??途中で切ってもOKみたいな)を扱える、より新しいエンベッディング・モデルがある。

- **Long Context Embeddings** that can encode longer sequences
より長いシーケンスをエンコードできる長いコンテキストの埋め込み
- **Variable Dimension Embeddings** that can produce a latent representation of an arbitrary number of tokens
任意の数のトークンの潜在表現を生成できる可変次元埋め込み

<!-- ここまで読んだ -->

### Sparsity スパース

Sparsity refers to the proportion of zero values within the embedding vectors.
スパース性とは、埋め込みベクトル内のゼロ値の割合を指す。

Sparse Embeddings contain a large number of zero values, with only a few non-zero elements.
スパース埋め込みには多数のゼロ値が含まれ、ゼロ以外の要素はわずかである。
(あ、埋め込みの定義としてdenceなベクトルである必要があると思ってるけど、sparceでもいいのか。流石にone-hotベクトルは埋め込みとは言わないのかな:thinking:)
They are often associated with high-dimensional representations where many dimensions are irrelevant for the given word.
これらは、多くの次元が与えられた単語にとって無関係である場合に高次元表現と関連している。
SPLADE v2 model provides highly sparse representations and competitive results.
SPLADE v2モデルは、非常にスパースな表現と競争力のある結果を提供します。
Dense Embeddings have non-zero values in most or all dimensions, capturing a richer and more continuous representation of word meanings
密な埋め込みは、ほとんどの次元またはすべての次元でゼロ以外の値を持ち、単語の意味をより豊かで連続的に表現する。

- Quality of Embeddings: Sparse embeddings might compromise on the semantic information due to the limited number of non-zero values.
エンベッディングの品質： 疎な埋め込みでは、非ゼロ値の数が限られているため、意味情報が損なわれる可能性がある。
Dense embeddings capture more semantic information leading to improved accuracy in tasks like machine translation, sentiment analysis, and natural language inference.
密な埋め込みは、機械翻訳、感情分析、自然言語推論のようなタスクにおいて、精度の向上につながるより多くの意味情報をキャプチャする。

- Computational Efficiency: Sparse embeddings allows for optimized storage and computation leading to faster processing.
計算効率： スパース埋め込みにより、ストレージと計算が最適化され、処理が高速化される。
Dense embeddings would require more storage and computational resources that could impact the performance especially in real time applications.
高密度の埋め込みは、より多くのストレージと計算資源を必要とし、特にリアルタイムアプリケーションのパフォーマンスに影響を与える可能性がある。

Dimensionality reduction techniques like Principal Component Analysis (PCA) or Autoencoders can be used to transform high-dimensional dense embeddings into a lower dimensional space.
主成分分析（PCA）やオートエンコーダのような次元削減技術は、高次元の密な埋め込みを低次元空間に変換するために使用することができる。

### Embedding Algorithms 埋め込みアルゴリズム

- **Traditional Algorithms**: Text embedding models like Word2Vec, Glove create static embeddings where each word or phrase has fixed representation regardless of the context.
従来のアルゴリズム Word2VecやGloveのようなテキスト埋め込みモデルは、**文脈に関係なく各単語やフレーズが固定された表現を持つ静的埋め込み**を作成します。

- **Contextual Algorithms**: With Transformers, context is included via self-attention making the recent embedding models better at more nuanced understanding of language though increasing computational complexity.
文脈アルゴリズム： Transformersでは、self-attentionを介して文脈が含まれ、最近の埋め込みモデルは、計算の複雑さが増すものの、言語の微妙な理解を向上させる。
Embeddings created using contextual algorithms can handle polysemy (words with multiple meanings) and homonymy (words with same spelling but different meanings) much better
文脈アルゴリズムを使用して作成された埋め込みは、多義性（複数の意味を持つ単語）や同音異義語（同じスペルを持つが異なる意味を持つ単語）をはるかにうまく処理できる。

### Interpretability 解釈可能性

Implementing interpretability in embeddings involves employing techniques to understand and explain the relationships captured within the embedding space.
埋め込みに解釈可能性を実装するには、埋め込み空間内で捉えられた関係を理解し、説明する技術を採用する必要があります。

#### Visualization of Embeddings エンベッディングの可視化

**[Embedding Projector](https://projector.tensorflow.org/)**: A tool that interactively visualizes embeddings in 3D, enabling exploration of nearest neighbors, clusters, and semantic relationships.
埋め込みプロジェクター： 埋め込みを3Dでインタラクティブに可視化し、最近傍探索、クラスタ探索、意味関係探索を可能にするツール。
This tool uses different dimensionality reduction techniques like PCA, T-SNE, UMAP to visualize the embeddings as a 2D or 3D visualization
このツールは、PCA、T-SNE、UMAPのような様々な次元削減技術を使用して、埋め込みを2Dまたは3Dで可視化します。
(お、T-SNEだー...!!:thinking:)

[Custom Code for visualizin](https://github.com/GoogleCloudPlatform/generative-ai/blob/68729b9c28fde5fd25147b74a05d65fff4b16800/embeddings/embedding-similarity-visualization.ipynb#L4)g the embeddings can also be leveraged
エンベッディングを視覚化するためのカスタムコードも活用できます。

#### Visualizing Attention Mechanisms attentionメカニズムの可視化

Attention in neural networks: Attention mechanisms highlight the most relevant parts of input data when making predictions, providing insights into which words or features are important for a specific task.
ニューラルネットワークにおけるattention： Attentionメカニズムは、予測を行う際に入力データの最も関連性の高い部分を強調し、特定のタスクに重要な単語や特徴を示す洞察を提供する。
Visualizing attention mechanisms using tools like BERTViz can reveal the attention patterns, showing which words or regions of the input contribute most to the output.
**BERTVizのようなツールを使用してattentionメカニズムを可視化することで、attentionパターンを明らかにし、入力のどの単語や領域が出力に最も貢献しているかを示すことができる。**

### Bias and Fairness バイアスと公平性

Embeddings are often obtained from training on large pre-existing datasets, and are susceptible to biases due to unfair representations in the original datasets.
エンベッディングは、多くの場合、既存の大規模なデータセットに対する学習から得られ、元のデータセットにおける不公正な表現によるバイアスの影響を受けやすい。
Some of the techniques available Word Embedding Fairness Evaluation (WEFE) is an open source library for measuring and mitigating bias in word embedding models.
[Word Embedding Fairness Evaluation (WEFE)](https://www.ijcai.org/proceedings/2020/0060.pdf)は、単語埋め込みモデルのバイアスを測定し緩和するためのオープンソースライブラリです。

WEFE also offers API, Github Repository and documentation to implement the framework.
また、WEFEはフレームワークを実装するためのAPI、Githubリポジトリ、ドキュメントも提供している。

The framework includes different metrics like Word Embedding Association Test (WEAT), Relative Norm Distance (RND), Mean Average Cosine Similarity (MAC), Embedding Coherence Test (ECT)
このフレームワークには、Word Embedding Association Test (WEAT)、Relative Norm Distance (RND)、Mean Average Cosine Similarity (MAC)、Embedding Coherence Test (ECT)などのさまざまなメトリクスが含まれています。

WEFE also includes a mitigation framework and Debias APIs to overcome Bias
WEFEには、バイアスを克服するための緩和フレームワークとデビアスAPIも含まれている。

### Latency レイテンシー

There are different ways of setting up Embedding models — accessing via HuggingFace, Langchain (uses HuggingFace integration) or use the embedding APIs from various providers.
HuggingFace、Langchain（HuggingFaceの統合を使用）を介してアクセスするか、または様々なプロバイダからの埋め込みAPIを使用します。

Custom embedding models hosted can also be accessed via an endpoint.
ホストされているカスタム埋め込みモデルは、エンドポイントを介してアクセスすることもできます。
Network latency can be reduced in this case, however the infrastructure scaling and updating the embedding models would have to be managed.
この場合、ネットワークの待ち時間は短縮できるが、インフラのスケーリングと埋め込みモデルの更新を管理しなければならない。

Embedding APIs from different providers simplified the task of obtaining word embeddings and allowed developers to focus on building applications.
異なるプロバイダーからのAPIを埋め込むことで、単語の埋め込みを取得する作業が簡素化され、開発者はアプリケーションの構築に集中できる。
They make it easy for the developers to access state of the art NLP technologies.
**これにより、開発者は最先端のNLP技術に簡単にアクセスできる。**(これは正直便利だよなぁ...自分でPytorchとかでNNの構造を定義して学習済み重みだけloadする、みたいなことが不要だし:thinking:)
However, if latency, privacy and security are critical, embedding models can also be hosted privately.
**しかし、レイテンシー、プライバシー、セキュリティが重要な場合は、埋め込みモデルをプライベートでホストすることもできる**。
Embedding APIs can be accessed directly from the provider like Google Cloud text embeddings API.
埋め込みAPIは、Google Cloudのテキスト埋め込みAPIのように、プロバイダーから直接アクセスできる。
Another alternative is to use LangChain provided integrations with various model providers that allow you to use embeddings with LangChain.
もう一つの選択肢は、LangChainが提供する様々なモデルプロバイダとのインテグレーションを使うことです。

It is important to understand the rate and quota limitations when using the Embedding APIs in your solution.
ソリューションで埋め込みAPIを使用する際に、レートとクォータの制限を理解することが重要です。

Embedding APIs from different providers also could vary in latency.
異なるプロバイダーのAPIを埋め込むことで、レイテンシーが異なる可能性もある。
Choice of APIs can be evaluated for latency.
APIの選択はレイテンシーで評価できる。
The blog by getzep.com provides a comparison of latency across different APIs.
getzep.comのブログでは、異なるAPI間の待ち時間の比較を提供している。

### Cost コスト

Cloud based embedding models offer flexibility and scalability, but can incur ongoing costs.
クラウドベースの組み込みモデルは、柔軟性と拡張性を提供するが、継続的なコストが発生する可能性がある。
On-premise hosted models require upfront investment in compute but can be more cost-effective in the long run for high volume proprietary models.
オンプレミスのホスト型モデルは、コンピュートへの先行投資が必要だが、大容量のプロプライエタリ・モデルの場合、長期的にはコスト効率が高くなる可能性がある。

Many high quality open source models are available, which might reduce cost.
多くの高品質なオープンソースモデルが利用可能で、コストを削減できるかもしれない。
However, due diligence need to be done to assess the fitment to the use case.
しかし、ユースケースへの適合性を評価するためには、due diligence(適切な注意)が必要です。

For custom models, strategies like quantization and distillation to reduce the model size and batching inference requests can be used to optimize cost
カスタムモデルの場合、モデルサイズを小さくするための量子化や蒸留のような戦略や、推論要求をバッチ処理することで、コストを最適化することができる。

Google Cloud offers different options and cost structures like multimodal embeddings for text, image, video.
Google Cloudは、テキスト、画像、動画のマルチモーダル埋め込みなど、さまざまなオプションとコスト構造を提供している。
Pricing for embeddings for text also varies for online and batch requests.
また、テキスト用のエンベッディングの価格も、オンラインとバッチで異なります。

### Ability to Fine Tune fine-tuningの能力

Fine tuning the model on datasets specific to the use case can enhance the performance of the pre-trained model if it is not trained on data relevant to the domain or for the specific needs.
ユースケースに特化したデータセットでモデルを微調整することで、事前に訓練されたモデルのパフォーマンスを向上させることができる。

Google Cloud provides options to fine tune the text and multilingual embedding models with user specific data.
Google Cloudは、テキストと多言語埋め込みモデルをユーザー固有のデータで微調整するオプションを提供します。
The tuning is executed using Vertex AI Pipelines
チューニングはVertex AI Pipelinesを使用して実行される。

### Selection of Embedding Models for your use case ユースケースに応じた埋め込みモデルの選択

The constant evolution of models makes it challenging to identify the right embedding model for a given task and the nature of the dataset used for the use case.
モデルの絶え間ない進化は、与えられたタスクやユースケースに使用されるデータセットの性質に適した埋め込みモデルを特定することを困難にしている。
Massive Text Embedding Benchmark (MTEB) aims to provide clarity on how different models perform on a variety of embedding tasks on different datasets.
[Massive Text Embedding Benchmark (MTEB)](https://arxiv.org/pdf/2210.07316)は、異なるデータセット上の様々な埋め込みタスクにおいて、異なるモデルがどのように動作するかを明確にすることを目的としている。

MTEB code is available open-source enabling evaluation of any embedding model on different tasks and datasets in less than 10 lines of code.
MTEBのコードはオープンソースで公開されており、10行以下のコードで、様々なタスクやデータセットに対する埋め込みモデルの評価が可能です。

Python code to use MTEB for a custom model
カスタム・モデルにMTEBを使用するPythonコード

```python
import mteb
# load a model from the hub (or for a custom implementation see https://github.com/embeddings-benchmark/mteb/blob/main/docs/reproducible_workflow.md)
model = mteb.get_model("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
tasks = mteb.get_tasks(…) # get specific tasks
# or
from mteb.benchmarks import MTEB_MAIN_EN
tasks = MTEB_MAIN_EN # or use a specific benchmark
evaluation = mteb.MTEB(tasks=tasks)
evaluation.run(model, output_folder="results")
```

MTEB Leaderboard provides insights for selection of the right embedding model based on:
MTEBリーダーボードは、適切なエンベデッド・モデルを選択するためのインサイトを提供する：

- Embedding Model performance based on task and task specific metrics relevant for the use case ユースケースに関連するタスクおよびタスク固有のメトリクスに基づく、埋め込みモデルのパフォーマンス

- Embedding Model performance on different datasets similar to the datasets and languages relevant to the use case ユースケースに関連するデータセットと言語に類似した異なるデータセットにおける埋め込みモデルのパフォーマンス

MTEB evaluates models on datasets of varying text lengths which are grouped into three categories:
MTEBは、3つのカテゴリーに分類された様々なテキスト長のデータセットでモデルを評価する：

Sentence to Sentence (S2S) — a sentence is compared to another sentence
センテンス・トゥ・センテンス（S2S） - 文を別の文と比較する。

Paragraph to Paragraph (P2P) — A paragraph is compared with another paragraph
段落対段落（P2P） - 段落を別の段落と比較する。

Sentence to Paragraph (S2P) — a single sentence is input query, but used to retrieve long documents consisting of multiple sentences.
Sentence to Paragraph (S2P) - 単文が入力クエリーであるが、複数の文からなる長い文書を検索するために使用される。

MTEB leaderboard consists of 199 datasets (as displayed on the leaderboard).
MTEBリーダーボードは199のデータセットで構成されている（リーダーボードに表示）。
These include 10 multilingual datasets for some of the tasks.
これらには、いくつかのタスクのための10個の多言語データセットが含まれる。
Some of the datasets have similarities with each other.
いくつかのデータセットは互いに類似している。

Performance of the embedding models on custom datasets or datasets similar to the existing datasets can be evaluated based on the metrics for the given task.
カスタムデータセットまたは既存のデータセットに類似したデータセットに対する埋め込みモデルの性能は、与えられたタスクのメトリクスに基づいて評価することができる。

## References 参考文献

Embeddings | Machine Learning | Google for Developers
 Machine Learning

On the Dimensionality of Embedding
エンベッディングの次元性について

SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval
SPLADE v2： 情報検索のための疎な語彙と展開モデル

Embedding projector
プロジェクターの埋め込み

BertVIZ
バートビズ

WEFE: The Word Embeddings Fairness Evaluation Framework
WEFE 単語埋め込み公正評価フレームワーク

the WEFE documentation!
WEFEの文書

Mitigation Framework — WEFE 0.4.1 documentation
軽減フレームワーク - WEFE 0.4.1 ドキュメント

Text embeddings API | Generative AI on Vertex AI | Google Cloud
 Generative AI on Vertex AI

Embedding models | 🦜️🔗 LangChain
 🦜️🔗 LangChain

longembed: extending embedding models for long context retrieval
longembed： 長い文脈検索のための埋め込みモデルの拡張

[2305.09967] Variable Length Embeddings
[2305.09967] 可変長の埋め込み

Get multimodal embeddings | Generative AI on Vertex AI | Google Cloud
 Generative AI on Vertex AI

Massive Text Embedding Benchmark
大規模テキスト埋め込みベンチマーク

A Survey of Embedding Models (and why you should look beyond OpenAI)
エンベッディング・モデルの調査（そして、OpenAI以外にも目を向けるべき理由）

Tune text embeddings | Generative AI on Vertex AI | Google Cloud
 Generative AI on Vertex AI

<!-- ここまで読んだ! -->
