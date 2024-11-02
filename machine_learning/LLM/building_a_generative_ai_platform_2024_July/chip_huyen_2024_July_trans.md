<https://huyenchip.com/2024/07/25/genai-platform.html>

# Building A Generative AI Platform ジェネレーティブAIプラットフォームの構築

After studying how companies deploy generative AI applications, I noticed many similarities in their platforms.
各社がどのようにジェネレーティブAIアプリケーションを導入しているかを調査した結果、そのプラットフォームには**多くの共通点**があることに気づいた。
This post outlines the common components of a generative AI platform, what they do, and how they are implemented.
この記事では、ジェネレーティブAIプラットフォームの一般的な構成要素、それらの機能、および実装方法について概説します。
I try my best to keep the architecture general, but certain applications might deviate.
私は一般的なアーキテクチャを維持するために最善を尽くしているが、特定のアプリケーションは逸脱するかもしれない。
This is what the overall architecture looks like.
全体的なアーキテクチャはこんな感じだ。

![]()

This is a pretty complex system.
これはかなり複雑なシステムだ。
This post will start from the simplest architecture and progressively add more components.
**この記事では、最も単純なアーキテクチャから始め、徐々にさらに多くのコンポーネントを追加していく**。(わかりやすく解説してくれていそうでありがたい...!:pray:)
In its simplest form, your application receives a query and sends it to the model.
**最も単純な形では、アプリケーションはクエリを受け取り、モデルに送信する**。
The model generates a response, which is returned to the user.
**モデルはレスポンスを生成し、それがユーザに返される。**
There are no guardrails, no augmented context, and no optimization.
ガードレールも、拡張された文脈も、最適化もない。
The Model API box refers to both third-party APIs (e.g., OpenAI, Google, Anthropic) and self-hosted APIs.
**モデルAPIの欄は、サードパーティAPI（例：OpenAI、Google、Anthropic）と自己ホストAPIの両方を指す**。(外部LLMでも内製LLMでも、どちらでも置き換え可能なアーキテクチャってことか:thinking:)

From this, you can add more components as needs arise.
ここから、必要に応じてコンポーネントを追加していくことができる。
The order discussed in this post is common, though you don’t need to follow the exact same order.
この記事で取り上げた順番が一般的だが、まったく同じ順番に従う必要はない。
A component can be skipped if your system works well without it.
**コンポーネントがなくてもシステムがうまく機能する場合は、コンポーネントを省略することができる。**
Evaluation is necessary at every step of the development process.
評価は、開発プロセスの各段階で必要だ。

- Enhance context input into a model by giving the model access to external data sources and tools for information gathering.
モデルが外部のデータソースや情報収集ツールにアクセスできるようにすることで、モデルへのコンテキスト入力を強化する。

- Put in guardrails to protect your system and your users.
システムとユーザーを守るためにガードレールを設置しましょう。

- Add model router and gateway to support complex pipelines and add more security.
モデルルーターとゲートウェイを追加して、複雑なパイプラインをサポートし、セキュリティを強化。

- Optimize for latency and costs with cache.
キャッシュでレイテンシとコストを最適化。

- Add complex logic and write actions to maximize your system’s capabilities.
複雑なロジックを追加し、アクションを記述することで、システムの能力を最大限に引き出します。

Observability, which allows you to gain visibility into your system for monitoring and debugging, and orchestration, which involves chaining all the components together, are two essential components of the platform.
観測可能性(監視とデバッグのためにシステムを可視化する)とオーケストレーション(すべてのコンポーネントを連結する)は、プラットフォームの2つの重要なコンポーネントです。
We will discuss them at the end of this post.
それらについては、この記事の最後で説明する。

» What this post is not «
」 この記事ではないもの 」

This post focuses on the overall architecture for deploying AI applications.
**この記事では、AIアプリケーションを展開するための全体的なアーキテクチャに焦点を当てる**。
It discusses what components are needed and considerations when building these components.
どのようなコンポーネントが必要なのか、またこれらのコンポーネントを構築する際の注意点についても触れている。
It’s not about how to build AI applications and, therefore, does NOT discuss model evaluation, application evaluation, prompt engineering, finetuning, data annotation guidelines, or chunking strategies for RAGs.
したがって、AIアプリケーションの構築方法については説明しておらず、モデル評価、アプリケーション評価、プロンプトエンジニアリング、ファインチューニング、データ注釈のガイドライン、RAGのチャンキング戦略については説明していません。
All these topics are covered in my upcoming book AI Engineering.
これらのトピックはすべて、私の近刊『AIエンジニアリング』で取り上げている。

<!-- ここまで読んだ -->

## Step 1. Enhance Context ステップ1. コンテキストの強化

("最も簡単な形"に最初に追加するコンポーネント??:thinking:)
("最も単純な形" = アプリケーションがクエリを受け取り、モデルに送信し、モデルがレスポンスを生成してユーザに返すだけの状態)

The initial expansion of a platform usually involves adding mechanisms to allow the system to augment each query with the necessary information.
プラットフォームの最初の拡張では、**システムが各クエリに必要な情報を補完するためのメカニズムを追加すること**が一般的です。
Gathering the relevant information is called context construction.
関連情報を集めることを **context construction (コンテキスト構築)** と呼びます。

Many queries require context to answer.
多くのクエリは、答えるために文脈(context)が必要です。
The more relevant information there is in the context, the less the model has to rely on its internal knowledge, which can be unreliable due to its training data and training methodology.
**コンテキストに関連する情報が多ければ多いほど、モデルが内部の知識に頼る必要が少なくなります**。これは、トレーニングデータとトレーニング方法によって信頼性が低い可能性があるためです。
(なるほど、信頼性の観点から、基本的にはcontextを追加したいモチベーションがあるのか...!:thinking:)
Studies have shown that having access to relevant information in the context can help the model generate more detailed responses while reducing hallucinations (Lewis et al., 2020).
研究によると、**contextで関連情報にアクセスできると、モデルがより詳細な回答を生成するのに役立ち、ハルシネーションを減らすことができる**とされています（Lewis et al., 2020）。

For example, given the query “Will Acme’s fancy-printer-A300 print 100pps?”, the model will be able to respond better if it’s given the specifications of fancy-printer-A300.
たとえば、「Acmeのfancy-printer-A300は100ppsを印刷しますか？」というクエリが与えられた場合、fancy-printer-A300の仕様が与えられると、モデルはより良く応答できるでしょう。
(Thanks Chetan Tekur for the example.)
(例を示してくれたチェタン・テクールに感謝する）。

Context construction for foundation models is equivalent to feature engineering for classical ML models.
**基礎モデルの context construction は、古典的なMLモデルの特徴量エンジニアリングに相当します**。(なるほど...!:thinking:)
They serve the same purpose: giving the model the necessary information to process an input.
これらは同じ目的を果たします：**モデルに入力を処理するために必要な情報を提供すること**。(← context construction の目的)

In-context learning, learning from the context, is a form of continual learning.
コンテクスト学習、つまりコンテクストから学習することは、継続的学習の形態です。
It enables a model to incorporate new information continually to make decisions, preventing it from becoming outdated.
これにより、モデルは新しい情報を継続的に取り込んで意思決定を行い、時代遅れになるのを防ぐことができます。
For example, a model trained on last-week data won’t be able to answer questions about this week unless the new information is included in its context.
例えば、先週のデータで訓練されたモデルは、**新しい情報がコンテキストに含まれていない限り、今週に関する質問に答えることができない**。
By updating a model’s context with the latest information, e.g.fancy-printer-A300’s latest specifications, the model remains up-to-date and can respond to queries beyond its cut-off date.
最新の情報（たとえば、fancy-printer-A300の最新の仕様）でモデルのコンテキストを更新することで、モデルは最新の状態を維持し、カットオフ日を超えるクエリに応答できる。

<!-- ここまで読んだ -->

### RAGs RAG

The most well-known pattern for context construction is RAG, Retrieval-Augmented Generation.
**context construction で最もよく知られているパターンは、RAG**（Retrieval-Augmented Generation）です。
RAG consists of two components: a generator (e.g.a language model) and a retriever, which retrieves relevant information from external sources.
**RAGは2つのコンポーネントから構成**される：**generator（たとえば言語モデル）**と**retriever**。retrieverは外部ソースから関連情報を取得する。
Retrieval isn’t unique to RAGs.
retrievalはRAGに特有のものではありません。
It’s the backbone of search engines, recommender systems, log analytics, etc.
検索エンジン、推薦システム、ログ分析などのバックボーンです。
Many retrieval algorithms developed for traditional retrieval systems can be used for RAGs.
**従来の検索システム向けに開発された多くの検索アルゴリズムは、RAGにも使用できます。**
(dual-encodingなど?:thinking:)

External memory sources typically contain unstructured data, such as memos, contracts, news updates, etc.
外部記憶ソースには通常、メモ、契約、ニュース更新などの非構造化データが含まれています。
They can be collectively called documents.
それらを総称して **document** と呼ぶことができます。
A document can be 10 tokens or 1 million tokens.
文書は10トークンにも100万トークンにもなる。
Naively retrieving whole documents can cause your context to be arbitrarily long.
**直感的にdocument全体を取得すると、コンテキストが任意に長くなる可能性**があります。
RAG typically requires documents to be split into manageable chunks, which can be determined from the model’s maximum context length and your application’s latency requirements.
RAGでは通常、**documentsを管理可能なチャンクに分割する必要**があります。これは、**モデルの最大コンテキスト長とアプリケーションのレイテンシ要件から決定できる**。
(これは、クエリに関連する情報をdocumentsから上位何件取得して、contextとしてgeneratorに渡すか、って話...?? もしくは上位1件のみgeneratorに渡すとしても、その1件が自然言語として長すぎる可能性があるって話かも...!:thinking:)
To learn more about chunking and the optimal chunk size, see Pinecone, Langchain, Llamaindex, and Greg Kamradt’s tutorials.
chunkingと最適なchunkサイズについて詳しく知りたい場合は、Pinecone、Langchain、Llamaindex、Greg Kamradtのチュートリアルを参照してください。

Once data from external memory sources has been loaded and chunked, retrieval is performed using two main approaches.
外部メモリソースからのデータがロードされ、chunk化(??)されたら、2つの主要なアプローチを使用してretrievalが行われます。

- Term-based retrieval
用語ベースの検索

This can be as simple as keyword search.
これはキーワード検索と同じくらい簡単なことだ。
For example, given the query “transformer”, fetch all documents containing this keyword.
例えば、「transformer」というクエリが与えられた場合、このキーワードを含むすべての文書を(関連情報として...!)フェッチする。
More sophisticated algorithms include BM25 (which leverages TF-IDF) and Elasticsearch (which leverages inverted index).
**より洗練されたアルゴリズムには、BM25（TF-IDFを活用）とElasticsearch（逆インデックスを活用）がある**。

Term-based retrieval is usually used for text data, but it also works for images and videos that have text metadata such as titles, tags, captions, comments, etc.
用語ベースの検索は通常テキストデータに用いられるが、タイトル、タグ、キャプション、コメントなどのテキストメタデータを持つ画像や動画にも有効である。

- Embedding-based retrieval (also known as vector search)
埋め込みベースの検索（ベクトル検索とも呼ばれる）

You convert chunks of data into embedding vectors using an embedding model such as BERT, sentence-transformers, and proprietary embedding models provided by OpenAI or Google.
データのチャンクをBERT、sentence-transformers、OpenAIやGoogleが提供する独自の埋め込みモデルなどの埋め込みモデルを使用して埋め込みベクトルに変換する。
Given a query, the data whose vectors are closest to the query embedding, as determined by the vector search algorithm, is retrieved.
クエリが与えられると、ベクトル検索アルゴリズム(=たぶん近傍探索?)によって決定されたクエリ埋め込みに最も近いデータが取得される。

Vector search is usually framed as nearest-neighbor search, using approximate nearest neighbor (ANN) algorithms such as FAISS (Facebook AI Similarity Search), Google’s ScaNN, Spotify’s ANNOY, and hnswlib (Hierarchical Navigable Small World).
ベクトル検索は通常、近傍探索としてフレーム化され、FAISS（Facebook AI Similarity Search）、GoogleのScaNN、SpotifyのANNOY、hnswlib（Hierarchical Navigable Small World）などの近似最近傍（ANN）アルゴリズムを使用する。
(特にリアルタイム推論のLLMアプリケーションで、context constructionのための手段としてRAGでembedding-based retrievalを使う場合、ANNアルゴリズムを使う必要がある...!:thinking:)

The ANN-benchmarks website compares different ANN algorithms on multiple datasets using four main metrics, taking into account the tradeoffs between indexing and querying.
ANN-benchmarksのウェブサイトでは、インデックス作成とクエリのトレードオフを考慮し、4つの主要な指標を用いて複数のデータセットで異なるANNアルゴリズムを比較している。

- Recall: the fraction of the nearest neighbors found by the algorithm.
リコール： アルゴリズムによって発見された最近傍の割合。
- Query per second (QPS): the number of queries the algorithm can handle per second.
    1秒あたりのクエリー数（QPS）： アルゴリズムが1秒間に処理できるクエリー数。
    This is crucial for high-traffic applications.
    これはトラフィックの多い用途では極めて重要である。
- Build time: the time required to build the index.
    構築時間： インデックスを構築するのに必要な時間。
    This metric is important especially if you need to frequently update your index (e.g.because your data changes).
    この指標は、特にインデックスを頻繁に更新する必要がある場合（データが変更された場合など）に重要である。
- Index size: the size of the index created by the algorithm, which is crucial for assessing its scalability and storage requirements.
    インデックスサイズ： アルゴリズムによって作成されるインデックスのサイズであり、スケーラビリティとストレージ要件を評価する上で極めて重要である。

This works with not just text documents, but also images, videos, audio, and code.
これ(embedding-based retrieval)は、テキスト文書だけでなく、画像、ビデオ、オーディオ、コードでも機能する。
Many teams even try to summarize SQL tables and dataframes and then use these summaries to generate embeddings for retrieval.
多くのチームは、**SQLテーブルやデータフレームを要約してから、これらの要約を使用して検索用の埋め込みを生成しようとします。**
(データを直接embeddingに変換するのではなく、要約してからembeddingに変換するアプローチ。text-to-SQLアプリケーションでも採用してるアプローチじゃん...!:thinking:)

Term-based retrieval is much faster and cheaper than embedding-based retrieval.
**用語ベースの検索は、埋め込みベースの検索よりもはるかに高速で安価**である。(そうなのか...!そりゃANNアルゴリズム使わなきゃってモチベーションもあるわけだ:thinking:)
It can work well out of the box, making it an attractive option to start.
使い始めるには魅力的なオプションであり、すぐにうまく機能することができる。
Both BM25 and Elasticsearch are widely used in the industry and serve as formidable baselines for more complex retrieval systems.
BM25とElasticsearchは、業界で広く使用されており、より複雑な検索システムの**強力なベースラインとして機能**する。
Embedding-based retrieval, while computationally expensive, can be significantly improved over time to outperform term-based retrieval.
embedding-based retrievalは計算コストが高いが、時間の経過とともに大幅に改善され、用語ベースの検索を上回ることができる。(どうなんだろ...!検索速度も重要だし:thinking:)

A production retrieval system typically combines several approaches.
プロダクション検索システムは通常、いくつかのアプローチを組み合わせる。
Combining term-based retrieval and embedding-based retrieval is called hybrid search.
**term-based retrievalとembedding-based retrievalを組み合わせることをハイブリッド検索**と呼ぶ。

One common pattern is sequential.
**よくあるパターンとしては、sequential**がある。(two-stage recommendみたいな感じ!:thinking:)
First, a cheap, less precise retriever, such as a term-based system, fetches candidates.
まず、term-basedシステムなどの安価で精度の低いretrieverが候補を取得する。
Then, a more precise but more expensive mechanism, such as k-nearest neighbors, finds the best of these candidates.
次に、k-nearest neighborsなどのより正確でコストの高いメカニズムが、これらの候補の中から最適なものを見つける。(二段階目がembedding-based retrievalってことか...!:thinking:)
The second step is also called reranking.
第2段階はrerankingとも呼ばれる。

For example, given the term “transformer”, you can fetch all documents that contain the word transformer, regardless of whether they are about the electric device, the neural architecture, or the movie.
たとえば、「transformer」という用語があれば、電気機器、神経アーキテクチャ、映画のどれに関するものであっても、transformerという単語を含むすべての文書を取り出すことができる。
Then you use vector search to find among these documents those that are actually related to your transformer query.
次に、ベクトル検索を使って、これらの文書の中から、トランスフォーマーに関するクエリに実際に関連する文書を探し出す。
(うんうん:thinking:)

Context reranking differs from traditional search reranking in that the exact position of items is less critical.
**context rerankingは、従来の検索再ランキングと異なり、アイテムの正確な位置(ランク)がそれほど重要ではない**。(検索rerankingと比較すると、って話!:thinking:)
In search, the rank (e.g., first or fifth) is crucial.
検索では、ランク（たとえば、最初か5番目か）が重要です。
In context reranking, the order of documents still matters because it affects how well a model can process them.
**context rerankingでは、documentの順序は依然として重要です。なぜなら、それがモデルがそれらをどれだけうまく処理できるかに影響を与えるからです**。
Models might better understand documents at the beginning and end of the context, as suggested by the paper Lost in the middle (Liu et al., 2023).
モデルは、Lost in the middle（Liu et al., 2023）の論文で示されているように、コンテキストの最初と最後の文書をよりよく理解するかもしれません。
However, as long as a document is included, the impact of its order is less significant compared to in search ranking.
**しかし、対象documentが含まれている限り、その順序の影響は、検索ランキングと比較してそれほど重要ではありません**。

Another pattern is ensemble.
もう一つのパターンは **ensemble** です。
(よくKaggleで目にするような、スコアを平均するようなアンサンブル学習ではなく、interleaving的なアプローチの意味だった...!:thinking:)
Remember that a retriever works by ranking documents by their relevance scores to the query.
retrieverは、クエリに対する関連スコアによって文書をランク付けすることで動作することを覚えておいてください。
You use multiple retrievers to fetch candidates at the same time, then combine these different rankings together to generate a final ranking.
複数のリトリーバーを使って候補を同時に取得し、それらの異なるランキングを組み合わせて最終的なランキングを生成する。

<!-- ここまで読んだ -->

### RAGs with tabular data 表形式データによるRAG

(構造化データから関連情報をretrieveして、contextとしてgeneratorに渡すケース! 事例としては少なさそう??:thinking:)

External data sources can also be structured, such as dataframes or SQL tables.
外部データソースは、データフレームやSQLテーブルのように構造化することもできる。
Retrieving data from an SQL table is significantly different from retrieving data from unstructured documents.
SQLテーブルからのデータ検索は、非構造化documentからのデータ検索とは大きく異なります。
Given a query, the system works as follows.
クエリが与えられると、システムは次のように動作する。

1. Text-to-SQL: Based on the user query and the table schemas, determine what SQL query is needed.
テキストからSQLへ： ユーザークエリとテーブルスキーマに基づいて、必要なSQLクエリを決定する。
(まずここが一筋縄ではいかないはず。他社ブログを見てると、Text-to-SQLアプリケーションを開発する上でアーキテクチャが大事そう...!:thinking:)

2. SQL execution: Execute the SQL query.
SQLの実行： SQLクエリを実行します。

3. Generation: Generate a response based on the SQL result and the original user query.
生成： SQLの結果と元のユーザクエリに基づいてレスポンスを生成する。

For the text-to-SQL step, if there are many available tables whose schemas can’t all fit into the model context, you might need an intermediate step to predict what tables to use for each query.
テキストをSQLに変換するステップでは、利用可能なテーブルが多数あり、そのスキーマがすべてモデルのコンテキストに適合しない場合、各クエリに使用するテーブルを予測する中間ステップが必要になることがあります。
Text-to-SQL can be done by the same model used to generate the final response or one of many specialized text-to-SQL models.
テキストからSQLへの変換は、最終的な応答を生成するために使用される同じモデル、または多くの専門のテキストからSQLへの変換モデルの1つで行うことができます。

<!-- ここまで読んだ -->

### Agentic RAGs エージェントのRAG

An important source of data is the Internet.
**重要なデータ源はインターネット**です。(=context constructionのための手段として、外部データソースから関連情報をretrieveするケース...!:thinking:)
A web search tool like Google or Bing API can give the model access to a rich, up-to-date resource to gather relevant information for each query.
GoogleやBingのAPIのようなウェブ検索ツールは、モデルに対して、各クエリに関連する情報を収集するための豊富で最新のリソースにアクセスさせることができます。
For example, given the query “Who won Oscar this year?”, the system searches for information about the latest Oscar and uses this information to generate the final response to the user.
例えば、「今年のオスカーは誰が受賞しましたか？」というクエリが与えられた場合、システムは最新のオスカーに関する情報を検索し、この情報を使用してユーザに最終的な応答を生成します。

Term-based retrieval, embedding-based retrieval, SQL execution, and web search are actions that a model can take to augment its context.
**term-based retrieval、embedding-based retrieval、SQL実行、ウェブ検索は、いずれもモデルがcontextを補完するために取ることができるアクション**です。
You can think of each action as a function the model can call.
それぞれのアクションは、**モデルが呼び出すことができる関数**と考えることができます。
A workflow that can incorporate external actions is also called agentic.
**外部アクションを組み込むことができるワークフロー**は、エージェントとも呼ばれます。
The architecture then looks like this.
すると、アーキテクチャは次のようになる。

![]()

<!-- 余談 -->
» Action vs tool アクションとツールの定義の話

A tool allows one or more actions.
**ツールは1つ以上のアクションを可能にする**。
For example, a people search tool might allow two actions: search by name and search by email.
例えば、人名検索ツールは2つのアクションを可能にするかもしれない： 名前による検索とEメールによる検索です。
However, the difference is minimal, so many people use action and tool interchangeably.
しかし、その違いはわずかであるため、多くの人がアクションとツールを同義に使っています。

<!-- これも余談 -->
» Read-only actions vs write actions 読み取り専用アクション対書き込みアクション

Actions that retrieve information from external sources but don’t change their states are read-only actions.
外部ソースから情報を取得するが状態を変更しないアクションは、読み取り専用アクションである。
(基本的にcontext constructionのための手段としてRAGを使う場合は、read-only actionsのイメージ:thinking:)
Giving a model write actions, e.g.updating the values in a table, enables the model to perform more tasks but also poses more risks, which will be discussed later.
モデルに書き込みアクション、例えばテーブル内の値を更新する権限を与えると、モデルはより多くのタスクを実行できるが、より多くのリスクも伴う。これについては後で詳しく説明します。

<!-- ここまで読んだ -->

### Query rewriting クエリの書き換え

Often, a user query needs to be rewritten to increase the likelihood of fetching the right information.
多くの場合、**正しい情報を取得する可能性を高めるために、ユーザのクエリを書き換える必要があります**。
(関連情報をretrieveする前に、クエリをrewriteするコンポーネントが必要な場合がある...!:thinking:)
Consider the following conversation.
次のような会話を考えてみよう。

```shell
User: When was the last time John Doe bought something from us?
ユーザ: ジョン・ドウが最後に何かを買ったのはいつですか？
AI: John last bought a Fruity Fedora hat from us two weeks ago, on January 3, 2030.
AI： ジョンが最後にFruity Fedoraの帽子を買ったのは2週間前の2030年1月3日です。
User: How about Emily Doe?
ユーザ: エミリー・ドウはどうですか？
```

The last question, “How about Emily Doe?”, is ambiguous.
最後の質問「エミリー・ドウはどうですか？」は曖昧です。
If you use this query verbatim to retrieve documents, you’ll likely get irrelevant results.
**このクエリをそのまま使って文書を検索すると、無関係な結果が得られる可能性が高い**。(確かに、対話式のアプリケーションだと特に問題になりそう:thinking:)
You need to rewrite this query to reflect what the user is actually asking.
ユーザが実際に尋ねていることを反映させるために、このクエリを書き換える必要があります。
The new query should make sense on its own.
新しいクエリは、単独で意味をなすはずです。
The last question should be rewritten to “When was the last time Emily Doe bought something from us?”
最後の質問は、「エミリー・ドウが最後に私たちから何かを買ったのはいつですか？」に書き換えるべきだ。

Query rewriting is typically done using other AI models, using a prompt similar to “Given the following conversation, rewrite the last user input to reflect what the user is actually asking."
query rewritingは通常、他のAIモデルを使って行われる。「**次の会話が与えられたら、ユーザーが実際に尋ねていることを反映させるために、最後のユーザー入力を書き換えてください**」のようなプロンプトを使用する。

Query rewriting can get complicated, especially if you need to do identity resolution or incorporate other knowledge.
query rewritingは、特にidentityの解決や他の知識を組み込む必要がある場合、複雑になることがあります。
If the user asks “How about his wife?”, you will first need to query your database to find out who his wife is.
**もしユーザが「彼の妻はどうですか？」と尋ねた場合、まずデータベースにクエリを送信して彼の妻が誰かを調べる必要があります。**
If you don’t have this information, the rewriting model should acknowledge that this query isn’t solvable instead of hallucinating a name, leading to a wrong answer.
この情報がない場合、**書き換えモデルは、名前をハルシネートする代わりに、このクエリが解決できないことを認めて、誤った回答につながるのを防ぐべきです**。

(query rewritingなかなか難しそう:thinking:)

<!-- ここまで読んだ -->

## Step 2. Put in Guardrails ステップ2. ガードレールの設置

Guardrails help reduce AI risks and protect not just your users but also you, the developers.
ガードレールは、AIのリスクを軽減し、ユーザーだけでなく、開発者であるあなた自身をも保護するのに役立つ。
They should be placed whenever there is potential for failures.
**故障の可能性がある場合は必ず設置する**。
This post discusses two types of guardrails: input guardrails and output guardrails.
この記事では、**2種類のガードレール**について説明する： input guardrails と output guardrails。

### Input guardrails 入力ガードレール

Input guardrails are typically protection against two types of risks: leaking private information to external APIs, and executing bad prompts that compromise your system (model jailbreaking).
入力ガードレールは、通常、2つのリスクに対する保護です：外部APIに個人情報を漏らすリスク、およびシステムを危険にさらす悪いプロンプトを実行するリスク（モデル脱獄）。

#### Leaking private information to external APIs 外部APIへの個人情報の漏洩

This risk is specific to using external model APIs when you need to send your data outside your organization.
このリスクは、データを組織外に送信する必要がある場合に外部モデルAPIを使用する際に特有のものです。
For example, an employee might copy the company’s secret or a user’s private information into a prompt and send it to wherever the model is hosted.
たとえば、社員が会社の秘密やユーザーの個人情報をプロンプトにコピーして、モデルがホストされている場所に送信するかもしれません。

One of the most notable early incidents was when Samsung employees put Samsung’s proprietary information into ChatGPT, accidentally leaking the company’s secrets.
**初期の最も有名な事件のひとつは、サムスンの従業員がChatGPTにサムスンの独自情報を入れ、会社の秘密を誤って漏洩させたとき**です。
It’s unclear how Samsung discovered this leak and how the leaked information was used against Samsung.
サムスンがこのリークをどのように発見したのか、また、リークされた情報がサムスンに対してどのように利用されたのかは不明である。
However, the incident was serious enough for Samsung to ban ChatGPT in May 2023.
しかし、この事件は、サムスンが2023年5月にChatGPTを禁止するほど深刻でした。

There’s no airtight way to eliminate potential leaks when using third-party APIs.
サードパーティのAPIを使用する際に潜在的なリークを排除する完璧な方法はありません。
However, you can mitigate them with guardrails.
しかし、ガードレールでそれを軽減することはできる。
You can use one of the many available tools that automatically detect sensitive data.
自動的に機密データを検出する多くの利用可能なツールの1つを使用できる。
What sensitive data to detect is specified by you.
**どのような機密データを検出するかは、あなたが指定する**。
Common sensitive data classes are:
一般的な機密データクラスは以下の通りである：

- Personal information (ID numbers, phone numbers, bank accounts).
個人情報（ID番号、電話番号、銀行口座）。

- Human faces.
人の顔。

- Specific keywords and phrases associated with the company’s intellectual properties or privileged information.
会社の知的財産や特権情報に関連する特定のキーワードやフレーズ。

Many sensitive data detection tools use AI to identify potentially sensitive information, such as determining if a string resembles a valid home address.
多くの機密データ検出ツールは、文字列が有効な自宅の住所に似ているかどうかを判断するなど、潜在的に機密情報を特定するためにAIを使用しています。
If a query is found to contain sensitive information, you have two options: block the entire query or remove the sensitive information from it.
クエリに機密情報が含まれていることが判明した場合、2つの選択肢があります： クエリ全体をブロックするか、機密情報を削除するかです。
For instance, you can mask a user’s phone number with the placeholder [PHONE NUMBER].
例えば、プレースホルダ[PHONE NUMBER]でユーザの電話番号をマスクすることができます。
If the generated response contains this placeholder, use a PII reversible dictionary that maps this placeholder to the original information so that you can unmask it, as shown below.
生成された応答にこのプレースホルダが含まれている場合、このプレースホルダを元の情報にマッピングするPII可逆辞書を使用して、それを復号化できるようにします。

#### Model jailbreaking モデル脱獄

It’s become an online sport to try to jailbreak AI models, getting them to say or do bad things.
AIモデルを脱獄させ、悪いことを言わせたり、させたりするのがオンラインスポーツになっている。
While some might find it amusing to get ChatGPT to make controversial statements, it’s much less fun if your customer support chatbot, branded with your name and logo, does the same thing.
**ChatGPTに物議を醸すような発言をさせるのは面白いと思う人もいるかもしれませんが、あなたの名前とロゴでブランド化されたカスタマーサポートのチャットボットが同じことをしたら、もっと面白くありません**。
This can be especially dangerous for AI systems that have access to tools.
これは、ツールにアクセスできるAIシステムにとっては特に危険なことだ。
Imagine if a user finds a way to get your system to execute an SQL query that corrupts your data.
ユーザがシステムにデータを破壊するSQLクエリを実行させる方法を見つけたとしたらどうなるでしょうか。(SQL injection攻撃みたいな話か...!:thinking:)

To combat this, you should first put guardrails on your system so that no harmful actions can be automatically executed.
これに対抗するには、**まずシステムにガードレールを設置し、有害なアクションが自動的に実行されないようにする必要がある**。
For example, no SQL queries that can insert, delete, or update data can be executed without human approval.
例えば、データの挿入、削除、更新を行うSQLクエリは、人間の承認なしに実行することはできない。
The downside of this added security is that it can slow down your system.
**このセキュリティ強化の欠点は、システムが遅くなることだ。**

To prevent your application from making outrageous statements it shouldn’t be making, you can define out-of-scope topics for your application.
アプリケーションが、作成すべきでないとんでもない発言をするのを防ぐために、アプリケーションにスコープ外のトピックを定義することができます。
For example, if your application is a customer support chatbot, it shouldn’t answer political or social questions.
例えば、あなたのアプリケーションがカスタマーサポートのチャットボットであれば、政治的、社会的な質問には答えるべきではない。
A simple way to do so is to filter out inputs that contain predefined phrases typically associated with controversial topics, such as “immigration” or “antivax”.
そうするための簡単な方法は、「移民」や「反ワクチン」など、論争の的になるトピックに典型的に関連する定義済みのフレーズを含む**入力をフィルタリングすること**である。
More sophisticated algorithms use AI to classify whether an input is about one of the pre-defined restricted topics.
より洗練されたアルゴリズムは、AIを使って、入力があらかじめ定義された制限されたトピックのいずれかに関するものかどうかを分類する。

If harmful prompts are rare in your system, you can use an anomaly detection algorithm to identify unusual prompts.
有害なプロンプトがシステムでまれにしか表示されない場合は、異常検知アルゴリズムを使用して異常なプロンプトを特定することができる。

<!-- ここまで読んだ -->s

### Output guardrails 出力ガードレール

AI models are probabilistic, making their outputs unreliable.
AIモデルは確率論的であり、その出力は信頼性に欠ける。
You can put in guardrails to significantly improve your application’s reliability.
**ガードレールを設置することで、アプリケーションの信頼性を大幅に向上させることができる。**
Output guardrails have two main functionalities:
出力ガードレールには主に2つの機能がある：

- Evaluate the quality of each generation.
各生成の品質を評価する。

- Specify the policy to deal with different failure modes.
異なる故障モードに対処するためのポリシーを指定する。

#### Output quality measurement 出力品質測定

To catch outputs that fail to meet your standards, you need to understand what failures look like.
**基準を満たさないアウトプットをキャッチする**には、失敗がどのようなものかを理解する必要がある。
Here are examples of failure modes and how to catch them.
ここでは、故障モードの例とその対処法を紹介する。

- 1. Empty responses.
空返事だ。

- 2. Malformatted responses that don’t follow the expected output format.
**期待される出力フォーマットに従わない、不正なフォーマットによる応答**。
For example, if the application expects JSON and the generated response has a missing closing bracket.
例えば、アプリケーションがJSONを期待していて、生成されたレスポンスに閉じ括弧がない場合。
There are validators for certain formats, such as regex, JSON, and Python code validators.
正規表現、JSON、Pythonコードバリデータなど、特定のフォーマット用のバリデータがあります。
There are also tools for constrained sampling such as guidance, outlines, and instructor.
ガイダンス、アウトライン、インストラクターなど、制約のあるサンプリングのためのツールもある。

- 3. Toxic responses, such as those that are racist or sexist.
人種差別や性差別などの有害な反応。
These responses can be caught using one of many toxicity detection tools.
このような反応は、多くの毒性検出ツールのいずれかを使って捕らえることができる。

- 4. Factual inconsistent responses hallucinated by the model.
モデルによってハルシネートされた、事実に矛盾する反応。
Hallucination detection is an active area of research with solutions such as SelfCheckGPT (Manakul et al., 2023) and SAFE, Search Engine Factuality Evaluator (Wei et al., 2024).
ハルシネーションの検出は、SelfCheckGPT（Manakul et al., 2023）やSAFE、Search Engine Factuality Evaluator（Wei et al., 2024）などの解決策がある研究の活発な分野である。
You can mitigate hallucinations by providing models with sufficient context and prompting techniques such as chain-of-thought.
モデルに十分な文脈を与えたり、思考の連鎖のようなテクニックを促したりすることで、ハルシネーションを軽減することができる。
Hallucination detection and mitigation are discussed further in my upcoming book AI Engineering.
ハルシネーションの検出と軽減については、私の近日発売の書籍AIエンジニアリングでさらに詳しく説明します。

- 5. Responses that contain sensitive information.
機密情報を含む回答。
This can happen in two scenarios.
これには2つのシナリオ（i.e. 原因...!:thinking:）があり得ます。
  - Your model was trained on sensitive data and regurgitates it back. あなたのモデルは機密データで訓練され、それを再送信する。
  - Your system retrieves sensitive information from your internal database to enrich its context, and then it passes this sensitive information on to the response. あなたのシステムは、内部データベースから機密情報を取得してコンテキストを豊かにし、その後、この機密情報を応答に渡す。

This failure mode can be prevented by not training your model on sensitive data and not allowing it to retrieve sensitive data in the first place.
この失敗モードは、機密データでモデルをトレーニングしないこと、および最初から機密データをretrieveすることを許可しないことで防ぐことができる。
Sensitive data in outputs can be detected using the same tools used for input guardrails.
**出力の中の機密データは、入力ガードレールに使用されるのと同じツールを使用して検出することができる**。

- 6. Brand-risk responses, such as responses that mischaracterize your company or your competitors.
自社や競合他社を誤解させるような対応など、ブランドリスクを伴う対応。
An example is when Grok, a model trained by X, generated a response suggesting that Grok was trained by OpenAI, causing the Internet to suspect X of stealing OpenAI’s data.
例えば、Xによって訓練されたモデルであるGrokが、GrokがOpenAIによって訓練されたと示唆する応答を生成し、インターネットがXがOpenAIのデータを盗んだと疑うようになった場合。
This failure mode can be mitigated with keyword monitoring.
**この故障モードは、キーワード監視で軽減できる**。
Once you’ve identified outputs concerning your brands and competitors, you can either block these outputs, pass them onto human reviewers, or use other models to detect the sentiment of these outputs to ensure that only the right sentiments are returned.
**自社ブランドや競合他社に関する出力を特定したら**、これらの出力をブロックしたり、人間のレビュアーに渡したり、他のモデルを使用してこれらの出力の感情を検出して、正しい感情のみが返されるようにすることができる。
(なるほど...!:thinking:)

- 7. Generally bad responses.
一般的に悪い応答。
For example, if you ask the model to write an essay and that essay is just bad, or if you ask the model for a low-calorie cake recipe and the generated recipe contains an excessive amount of sugar.
**例えば、モデルにエッセイを書くように頼んだら、そのエッセイがひどかったとか、モデルに低カロリーのケーキのレシピを頼んだら、出来上がったレシピに砂糖が過剰に含まれていたとか**。
It’s become a popular practice to use AI judges to evaluate the quality of models’ responses.
**モデルの回答の質を評価するためにAIジャッジを使用することは一般的になっている**。(なるほど...!:thinking:)
These AI judges can be general-purpose models (think ChatGPT, Claude) or specialized scorers trained to output a concrete score for a response given a query.
これらのAIジャッジは、汎用モデル（ChatGPT、Claudeなど）であったり、またはクエリが与えられたときに具体的なスコアを出力するために訓練された専門のスコアラーである。

#### Failure management 故障管理

AI models are probabilistic, which means that if you try a query again, you might get a different response.
AIモデルは確率的なものである。つまり、もう一度クエリを試せば、違う回答が返ってくるかもしれない。
Many failures can be mitigated using a basic retry logic.
**多くの失敗は、基本的なリトライロジックを使用して軽減できる**。
For example, if the response is empty, try again X times or until you get a non-empty response.
例えば、レスポンスが空であれば、空でないレスポンスが返ってくるまでX回再試行する。
Similarly, if the response is malformatted, try again until the model generates a correctly formatted response.
同様に、レスポンスが不正なフォーマットであれば、モデルが正しくフォーマットされたレスポンスを生成するまで再試行する。

This retry policy, however, can incur extra latency and cost.
**しかし、この再試行ポリシーは、余分なレイテンシーとコストを発生させる可能性がある。**
One retry means 2x the number of API calls.
1回のリトライは、API呼び出し回数の2倍を意味する。
If the retry is carried out after failure, the latency experienced by the user will double.
**失敗した後に再試行すると、ユーザーが経験する待ち時間は2倍になる**。
To reduce latency, you can make calls in parallel.
**待ち時間を減らすために、並列に呼び出すことができる**。(なるほど...!:thinking:)
For example, for each query, instead of waiting for the first query to fail before retrying, you send this query to the model twice at the same time, get back two responses, and pick the better one.
例えば、それぞれのクエリに対して、最初のクエリが失敗するのを待ってから再試行するのではなく、このクエリをモデルに同時に2回送信し、2つのレスポンスを返してもらい、より良い方を選ぶ。
This increases the number of redundant API calls but keeps latency manageable.
これにより、冗長なAPIコールの数は増えるが、レイテンシーは管理可能な範囲に抑えられる。

It’s also common to fall back on humans to handle tricky queries.
また、トリッキーなクエリを処理するために人間に頼ることもよくあることだ。
For example, you can transfer a query to human operators if it contains specific key phrases.
例えば、クエリに特定のキーワードが含まれている場合、クエリを人間のオペレーターに転送することができる。
Some teams use a specialized model, potentially trained in-house, to decide when to transfer a conversation to humans.
チームによっては、専門的なモデル（社内で訓練された可能性もある）を使って、会話を人間に転送するタイミングを決定することがある。
One team, for instance, transfers a conversation to human operators when their sentiment analysis model detects that the user is getting angry.
たとえば、あるチームは、**感情分析モデルがユーザが怒っていると検出したときに、会話を人間のオペレーターに転送する**。
Another team transfers a conversation after a certain number of turns to prevent users from getting stuck in an infinite loop.
別のチームは、ユーザーが無限ループに陥るのを防ぐために、一定回数のターン後に会話を転送する。

<!-- ここまで読んだ -->

### Guardrail tradeoffs ガードレールのトレードオフ

#### Reliability vs latency tradeoff: 信頼性とレイテンシーのトレードオフ

While acknowledging the importance of guardrails, some teams told me that latency is more important
ガードレールの重要性を認識しながらも、一部のチームは、レイテンシーの方が重要だと私に話した。
They decided not to implement guardrails because they can significantly increase their application’s latency.
ガードレールはアプリケーションのレイテンシーを大幅に増加させる可能性があるため、彼らはガードレールを実装しないことに決めた。
However, these teams are in the minority.
しかし、こうしたチームは少数派である。
Most teams find that the increased risks are more costly than the added latency.
**ほとんどのチームは、増加したリスクが、追加されたレイテンシーよりもコストがかかると考えている**。(なるほど...!:thinking:)

Output guardrails might not work well in the stream completion mode.
出力ガードレールは、stream completionモードではうまく機能しないかもしれない。
By default, the whole response is generated before shown to the user, which can take a long time.
デフォルトでは、ユーザーに表示される前に全体のレスポンスが生成されるため、時間がかかる。
In the stream completion mode, new tokens are streamed to the user as they are generated, reducing the time the user has to wait to see the response.
**stream completionモードでは、新しいトークンが生成されると、それらがユーザーにストリーミングされ、ユーザーが応答を見るまでの待ち時間が短縮される**。
The downside is that it’s hard to evaluate partial responses, so unsafe responses might be streamed to users before the system guardrails can determine that they should be blocked.
**欠点は、部分的な応答を評価するのが難しいため、システムのガードレールがそれらをブロックすべきかどうかを判断する前に、危険な応答がユーザーにストリーミングされる可能性がある**ことだ。

#### Self-hosted vs third-party API tradeoff: セルフホストとサードパーティAPIのトレードオフ

Self-hosting your models means that you don’t have to send your data to a third party, reducing the need for input guardrails.
**モデルをセルフホストすることは、データをサードパーティに送る必要がないことを意味し、入力ガードレールの必要性を減らす**。
However, it also means that you must implement all the necessary guardrails yourself, rather than relying on the guardrails provided by third-party services.
**しかし、サードパーティサービスが提供するガードレールに頼るのではなく、自分で必要なすべてのガードレールを実装する必要がある**。

Our platform now looks like this.
現在、我々のプラットフォームはこのようになっている。
Guardrails can be independent tools or parts of model gateways, as discussed later.
後述するように、**ガードレールは独立したツールであるか、モデルゲートウェイの一部であるかのいずれか**である。
Scorers, if used, are grouped under model APIs since scorers are typically AI models, too.
スコアラーも通常AIモデルであるため、使用される場合はモデルAPIに分類される。
Models used for scoring are typically smaller and faster than models used for generation.
採点に使われるモデルは、一般的に生成に使われるモデルよりも小型で高速である。

![]()

<!-- ここまで読んだ -->

## Step 3. Add Model Router and Gateway ステップ3. ルーターとゲートウェイのモデル追加

As applications grow in complexity and involve more models, two types of tools emerged to help you work with multiple models: routers and gateways.
アプリケーションが複雑化し、より多くのモデルを扱うようになると、**複数のモデルを扱うのに役立つ2種類のツール**が登場した: ルーターとゲートウェイ。

### Router ルーター

An application can use different models to respond to different types of queries.
アプリケーションは、異なるタイプのクエリに対応するために、異なるモデルを使用することができる。
Having different solutions for different queries has several benefits.
**異なるクエリに対して異なるソリューションを持つことには、いくつかの利点**がある。
First, this allows you to have specialized solutions, such as one model specialized in technical troubleshooting and another specialized in subscriptions.
まず、技術的なトラブルシューティングに特化したモデルや、サブスクリプションに特化した別のモデルなど、特化したソリューションを持つことができる。
Specialized models can potentially perform better than a general-purpose model.
特化したモデルは、汎用モデルよりも性能が向上する可能性がある。
Second, this can help you save costs.
第二に、これはコスト削減に役立つ。
Instead of routing all queries to an expensive model, you can route simpler queries to cheaper models.
**すべてのクエリを高価なモデルにルーティングする代わりに、より安価なモデルに簡単なクエリをルーティングすることができる**。

A router typically consists of an intent classifier that predicts what the user is trying to do.
**ルーターは通常、ユーザが何をしようとしているかを予測するintent classifier(意図分類器)で構成**されている。
Based on the predicted intent, the query is routed to the appropriate solution.
予測された意図に基づいて、クエリは適切なソリューションにルーティングされる。
For example, for a customer support chatbot, if the intent is:
例えば、カスタマーサポートのチャットボットの場合、次のような意図があるとします：

- To reset a password –> route this user to the page about password resetting.
パスワードをリセットするには→このユーザーをパスワードリセットのページに誘導する。

- To correct a billing mistake –> route this user to a human operator.
請求ミスを訂正する→このユーザーを人間のオペレーターにルーティングする。

- To troubleshoot a technical issue –> route this query to a model finetuned for troubleshooting.
技術的な問題のトラブルシューティングを行うには→このクエリーをトラブルシューティング用に細かく調整されたモデルにルーティングする。

An intent classifier can also help your system avoid out-of-scope conversations.
**intent classifierは、システムがスコープ外の会話を避けるのにも役立ちます**。
For example, you can have an intent classifier that predicts whether a query is out of the scope.
例えば、クエリがスコープ外かどうかを予測するintent classifierを持つことができます。
If the query is deemed inappropriate (e.g.if the user asks who you would vote for in the upcoming election), the chatbot can politely decline to engage using one of the stock responses (“As a chatbot, I don’t have the ability to vote. If you have questions about our products, I’d be happy to help.”) without wasting an API call.
クエリが不適切と判断された場合（例えば、ユーザが次回の選挙で誰に投票するか尋ねる場合）、チャットボットはAPIコールを無駄にすることなく、ストックの応答の1つを使って丁寧に拒否することができます（「チャットボットとして、投票する権限はありません。製品に関する質問があれば、喜んでお手伝いします。」）。

If your system has access to multiple actions, a router can involve a next-action predictor to help the system decide what action to take next.
システムが複数のアクションにアクセスできる場合、ルーターは、next action predictorを含めることができ、システムが次にどのアクションを取るかを決定するのに役立ちます。
One valid action is to ask for clarification if the query is ambiguous.
クエリがあいまいな場合は、説明を求めることも有効なアクションの1つです。
For example, in response to the query “Freezing,” the system might ask, “Do you want to freeze your account or are you talking about the weather?” or simply say, “I’m sorry. Can you elaborate?”
例えば、クエリ「freeeze」に対して、システムは「アカウントを凍結したいのか、天気について話しているのか？」と尋ねるか、「申し訳ありません。詳しく説明していただけますか？」と言うかもしれません。

Intent classifiers and next-action predictors can be general-purpose models or specialized classification models.
intent classifierとnext-action predictorは、汎用モデルまたは特殊化された分類モデルであることができます。
Specialized classification models are typically much smaller and faster than general-purpose models, allowing your system to use multiple of them without incurring significant extra latency and cost.
**特化した分類モデルは、通常、汎用モデルよりもはるかに小さく高速であり**、システムが多数のモデルを使用しても、大幅な追加のレイテンシーやコストをかけることなく使用できます。
(これが特化モデルの利点か:thinking:)

When routing queries to models with varying context limits, the query’s context might need to be adjusted accordingly.
**様々なコンテキスト制限を持つモデルにクエリをルーティングする場合**、クエリのコンテキストを適切に調整する必要があるかもしれません。(含めたいcontextの長さに応じて、モデルを切り替えるアプローチか:thinking:)
Consider a query of 1,000 tokens that is slated for a model with a 4K context limit.
1,000トークンのクエリが、4Kコンテキスト制限のあるモデルで処理されることを考えます。
The system then takes an action, e.g.web search, that brings back 8,000-token context.
その後、システムはウェブ検索などのアクションを起こし、8,000トークンのコンテキストを返す。
You can either truncate the query’s context to fit the originally intended model or route the query to a model with a larger context limit.
クエリのコンテキストを切り捨てて本来の目的のモデルに合わせるか、コンテキスト制限が大きいモデルにクエリをルーティングするかのどちらかです。

<!-- ここまで読んだ -->

### Gateway ゲートウェイ

A model gateway is an intermediate layer that allows your organization to interface with different models in a unified and secure manner.
**モデル・ゲートウェイは、組織が異なるモデルと統一された安全な方法でインターフェースを持つことを可能にする中間層**です。
The most basic functionality of a model gateway is to enable developers to access different models – be it self-hosted models or models behind commercial APIs such as OpenAI or Google – the same way.
**モデルゲートウェイの最も基本的な機能は、開発者が異なるモデルに同じ方法でアクセスできるようにすること**です。それがセルフホストされたモデルであるか、OpenAIやGoogleなどの商用APIの背後にあるモデルであるかの違いはありません。
A model gateway makes it easier to maintain your code.
**モデルゲートウェイは、コードの保守を容易にする。**
If a model API changes, you only need to update the model gateway instead of having to update all applications that use this model API.
モデルAPIが変更された場合、そのモデルAPIを使用するすべてのアプリケーションを更新する必要がある代わりに、モデルゲートウェイだけを更新すればよい。

![]()

In its simplest form, a model gateway is a unified wrapper that looks like the following code example.
最も単純な形では、モデルゲートウェイは以下のコード例のような統一されたラッパーです。
This example is to give you an idea of how a model gateway might be implemented.
この例は、モデルゲートウェイがどのように実装されるかのアイデアを与えるためのものである。
It’s not meant to be functional as it doesn’t contain any error checking or optimization.
エラーチェックや最適化が含まれていないため、機能的ではありません。

```python

import google.generativeai as genai
import openai

def openai_model(input_data, model_name, max_tokens):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Completion.create(
        engine=model_name,
        prompt=input_data,
        max_tokens=max_tokens
    )
    return {"response": response.choices[0].text.strip()}

def gemini_model(input_data, model_name, max_tokens):
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(model_name=model_name)
    response = model.generate_content(input_data, max_tokens=max_tokens)
    return {"response": response["choices"][0]["message"]["content"]}

@app.route('/model', methods=['POST'])
def model_gateway():
    data = request.get_json()
    model_type = data.get("model_type")
    model_name = data.get("model_name")
    input_data = data.get("input_data")
    max_tokens = data.get("max_tokens")

    if model_type == "openai":
        result = openai_model(input_data, model_name, max_tokens)
    elif model_type == "gemini":
        result = gemini_model(input_data, model_name, max_tokens)
    return jsonify(result)
```

A model gateway is access control and cost management.
**モデルゲートウェイは、アクセス制御とコスト管理**です。
Instead of giving everyone who wants access to the OpenAI API your organizational tokens, which can be easily leaked, you only give people access to the model gateway, creating a centralized and controlled point of access.
OpenAI APIにアクセスしたい人全員にあなたの組織のトークンを渡すのではなく、**モデルゲートウェイにアクセス権を与えることで、中央集権化された制御されたアクセスポイントを作成**します。
The gateway can also implement fine-grained access controls, specifying which user or application should have access to which model.
**ゲートウェイはまた、どのユーザーやアプリケーションがどのモデルにアクセスできるかを指定する細かいアクセス制御を実装することができる**。
Moreover, the gateway can monitor and limit the usage of API calls, preventing abuse and managing costs effectively.
さらに、ゲートウェイはAPIコールの使用状況を監視し、制限することで、乱用を防ぎ、コストを効果的に管理することができる。

A model gateway can also be used to implement fallback policies to overcome rate limits or API failures (the latter is unfortunately common).
モデル・ゲートウェイはまた、**レート制限やAPIの失敗（残念ながら一般的）を克服するためのフォールバックポリシー**を実装するために使用することができる。(推論モデルに不具合があった場合になんとか対応するためのフォールバック戦略か...!:thinking:)
When the primary API is unavailable, the gateway can route requests to alternative models, retry after a short wait, or handle failures in other graceful manners.
プライマリAPIが利用できない場合、ゲートウェイはリクエストを代替モデルにルーティングしたり、短い待ち時間後に再試行したり、他の優雅な方法で失敗を処理したりすることができる。
This ensures that your application can operate smoothly without interruptions.
これにより、**アプリケーションが中断することなくスムーズに動作することが保証**されます。(大事...!:thinking:)

Since requests and responses are already flowing through the gateway, it’s a good place to implement other functionalities such as load balancing, logging, and analytics.
リクエストとレスポンスがすでにゲートウェイを通過するようになっているため、**ロードバランシング、ロギング、アナリティクスなどの他の機能を実装するのに適した場所**です。(推薦統一インタフェースでも...!:thinking:)
Some gateway services even provide caching and guardrails.
**ゲートウェイ・サービスの中には、キャッシュやガードレールを提供するものもあります**。

Given that gateways are relatively straightforward to implement, there are many off-the-shelf gateways.
ゲートウェイの実装が比較的簡単であることを考えると、既製品のゲートウェイも多い。
Examples include Portkey’s gateway, MLflow AI Gateway, WealthSimple’s llm-gateway, TrueFoundry, Kong, and Cloudflare.
例えば、Portkeyのゲートウェイ、MLflow AI Gateway、WealthSimpleのllm-gateway、TrueFoundry、Kong、Cloudflareなどがあります。

With the added gateway and routers, our platform is getting more exciting.
ゲートウェイとルーターが追加され、我々のプラットフォームはよりエキサイティングになっている。
Like scoring, routing is also in the model gateway.
スコアリング(=多分Output Guardrailの話...!:thinking:)と同様に、ルーティングもモデルゲートウェイに含まれている。
Like models used for scoring, models used for routing are typically smaller than models used for generation.
scoring に使われるモデルと同様に、ルーティングに使われるモデル(intent classifierやnext-action predictor)は、通常、生成に使われるモデルよりも小さくなっています。

<!-- ここまで読んだ -->

## Step 4. Reduce Latency with Cache ステップ4. キャッシュによるレイテンシーの削減

When I shared this post with my friend Eugene Yan, he said that cache is perhaps the most underrated component of an AI platform.
この投稿を友人のユージン・ヤンと共有したところ、彼は「**キャッシュはおそらくAIプラットフォームで最も過小評価されているcomponentだ**」と言いました。
Caching can significantly reduce your application’s latency and cost.
**キャッシュは、アプリケーションのレイテンシーとコストを大幅に削減することができます**。

Cache techniques can also be used during training, but since this post is about deployment, I’ll focus on cache for inference.
キャッシュのテクニックはトレーニング中にも使えるが、この投稿はデプロイメントについてなので、**推論用のキャッシュに焦点を当てる**。
(学習中のcacheって、例えばどんな風に使えるんだろう:thinking:)
Some common inference caching techniques include prompt cache, exact cache, and semantic cache.
**一般的な推論キャッシュ技術には、prompt cache、exact cache(正確なキャッシュ)、semantic cache(意味キャッシュ)があります**。
Prompt cache are typically implemented by the inference APIs that you use.
プロンプト・キャッシュは通常、使用する推論APIによって実装される。
When evaluating an inference library, it’s helpful to understand what cache mechanism it supports.
**推論ライブラリを評価する際には、そのライブラリがどのようなキャッシュ・メカニズムをサポートしているかを理解することが役立ちます**。

KV cache for the attention mechanism is out of scope for this discussion.
アテンション・メカニズム用のKVキャッシュは、今回の議論の対象外である。

<!-- ここまで読んだ -->

### Prompt cache プロンプト・キャッシュ

Many prompts in an application have overlapping text segments.
アプリケーションの多くのプロンプトには、重複するテキストセグメントがあります。
For example, all queries can share the same system prompt.
例えば、すべてのクエリは同じシステム・プロンプトを共有できます。
A prompt cache stores these overlapping segments for reuse, so you only need to process them once.
プロンプト・キャッシュは、これらの重複するセグメントを再利用するために保存するため、一度だけ処理するだけで済みます。
A common overlapping text segment in different prompts is the system prompt.
**さまざまなプロンプトで重複する共通のテキストセグメントは、システムプロンプト**である。
Without prompt cache, your model needs to process the system prompt with every query.
プロンプト・キャッシュがない場合、モデルはクエリごとにシステム・プロンプトを処理する必要があります。
With prompt cache, it only needs to process the system prompt once for the first query.
プロンプト・キャッシュを使えば、システム・プロンプトを処理するのは最初のクエリに対して一度だけでよい。

For applications with long system prompts, prompt cache can significantly reduce both latency and cost.
**長いシステム・プロンプトを伴うアプリケーションの場合、プロンプト・キャッシュは、レイテンシーとコストの両方を大幅に削減できる。**
If your system prompt is 1000 tokens and your application generates 1 million model API calls today, a prompt cache will save you from processing approximately 1 billion repetitive input tokens a day! However, this isn’t entirely free.
システム・プロンプトが1000トークンで、アプリケーションが今日100万回のモデルAPIコールを生成する場合、プロンプト・キャッシュを使えば、1日に約10億回の繰り返し入力トークンの処理を省くことができる！**しかし、これ(=プロンプト・キャッシュ)は完全に無料ではありません**。
Like KV cache, prompt cache size can be quite large and require significant engineering effort.
KVキャッシュと同様、プロンプト・キャッシュのサイズはかなり大きく、かなりのエンジニアリング努力が必要です。

Prompt cache is also useful for queries that involve long documents.
プロンプト・キャッシュは、長い文書を含むクエリにも便利です。
For example, if many of your user queries are related to the same long document (such as a book or a codebase), this long document can be cached for reuse across queries.
例えば、ユーザーのクエリの多くが同じ長いドキュメント（本やコードベースなど）に関連している場合、この長いドキュメントはクエリ間で再利用できるようにキャッシュすることができます。

Since its introduction in November 2023 by Gim et al., prompt cache has already been incorporated into model APIs.
**ギムらによって2023年11月に導入されて以来、プロンプト・キャッシュはすでにモデルAPIに組み込まれています**。
Google announced that Gemini APIs will offer this functionality in June 2024 under the name context cache.
グーグルは、ジェミニAPIが2024年6月に**コンテキストキャッシュという名称**でこの機能を提供すると発表した。
Cached input tokens are given a 75% discount compared to regular input tokens, but you’ll have to pay extra for cache storage (as of writing, $1.00 / 1 million tokens per hour).
キャッシュされたインプット・トークンは、通常のインプット・トークンに比べて75％割引されるが、キャッシュ・ストレージのために追加料金を支払う必要がある（執筆時点では、1時間あたり100万トークンあたり1ドル）。
Given the obvious benefits of prompt cache, I wouldn’t be surprised if it becomes as popular as KV cache.
**プロンプト・キャッシュの明らかな利点を考えれば、KVキャッシュと同じくらい人気が出ることも不思議ではありません**。

While llama.cpp also has prompt cache, it seems to only cache whole prompts and work for queries in the same chat session.
llama.cppもプロンプトキャッシュを持っているが、プロンプト全体をキャッシュし、同じチャットセッション内のクエリに対してのみ動作するようだ。
Its documentation is limited, but my guess from reading the code is that in a long conversation, it caches the previous messages and only processes the newest message.
ドキュメントは限られているが、コードを読んだ結果から推測すると、長い会話の中で、前のメッセージをキャッシュし、最新のメッセージのみを処理するようだ。

<!-- ここまで読んだ -->

### Exact cache 厳密なキャッシュ

If prompt cache and KV cache are unique to foundation models, exact cache is more general and straightforward.
**プロンプト・キャッシュとKVキャッシュが基盤モデル特有のものだとすれば、Exact cacheはより一般的で直接的**です。
Your system stores processed items for reuse later when the exact items are requested.
**システムは処理されたアイテムを保存し、同一のアイテムが要求されたときに後で再利用する**。
For example, if a user asks a model to summarize a product, the system checks the cache to see if a summary of this product is cached.
例えば、ユーザーが商品の要約をモデルに求めた場合、システムはキャッシュをチェックし、この商品の要約がキャッシュされているかどうかを確認する。
If yes, fetch this summary.
もしそうなら、この要約を取り寄せる。
If not, summarize the product and cache the summary.
そうでない場合は、製品を要約し、要約をキャッシュする。

Exact cache is also used for embedding-based retrieval to avoid redundant vector search.
**Exact cacheは、冗長なベクトル検索を避けるために埋め込みベースの検索にも使用される。**

If an incoming query is already in the vector search cache, fetch the cached search result.
入力されたクエリがすでにベクトル検索キャッシュにある場合、キャッシュされた検索結果をフェッチする。
If not, perform a vector search for this query and cache the result.
そうでない場合は、このクエリに対してベクトル検索を行い、結果をキャッシュする。

Cache is especially appealing for queries that require multiple steps (e.g.chain-of-thought) and/or time-consuming actions (e.g.retrieval, SQL execution, or web search).
キ**ャッシュは、複数のステップ（思考の連鎖など）や時間のかかるアクション（検索、SQL実行、ウェブ検索など）を必要とするクエリには特に魅力的**である。

An exact cache can be implemented using in-memory storage for fast retrieval.
**exact cacheは、高速な検索のためにインメモリ・ストレージを使用して実装することができる**。
However, since in-memory storage is limited, a cache can also be implemented using databases like PostgreSQL, Redis, or tiered storage to balance speed and storage capacity.
**しかし、インメモリ・ストレージには限りがあるため、PostgreSQLやRedisなどのデータベース、あるいは速度とストレージ容量のバランスを取るための階層型ストレージを使用してキャッシュを実装することもできる**。
Having an eviction policy is crucial to manage the cache size and maintain performance.
**キャッシュサイズを管理し、パフォーマンスを維持するためには、eviction policy(=立ち退きポリシー)が重要**です。
Common eviction policies include Least Recently Used (LRU), Least Frequently Used (LFU), and First In, First Out (FIFO).
**一般的なeviction policyには、Least Recently Used (LRU)、Least Frequently Used (LFU)、First In, First Out (FIFO)があります**。

How long to cache a query depends on how likely this query is to be called again.
**クエリをどのくらいキャッシュするかは、そのクエリが再度呼び出される可能性がどの程度あるかによって決まる**。
User-specific queries such as “What’s the status of my recent order” are less likely to be reused by other users, and therefore, shouldn’t be cached.
「What’s the status of my recent order(私の最近の注文の状況はどうですか)」のようなユーザ固有のクエリは、他のユーザに再利用される可能性が低く、したがってキャッシュするべきではありません。
Similarly, it makes less sense to cache time-sensitive queries such as “How’s the weather?” Some teams train a small classifier to predict whether a query should be cached.
同様に、「How is the weather?（天気はどうですか？）」のような時間的に敏感なクエリをキャッシュするのは意味がありません。**一部のチームは、クエリをキャッシュすべきかどうかを予測する小さな分類器をトレーニングしています**。

<!-- ここまで読んだ -->

### Semantic cache セマンティック・キャッシュ

Unlike exact cache, semantic cache doesn’t require the incoming query to be identical to any of the cached queries.
**厳密なキャッシュとは異なり、セマンティックキャッシュでは、入力されるクエリがキャッシュされたクエリと同一である必要はない**。
Semantic cache allows the reuse of similar queries.
セマンティックキャッシュは**類似したクエリの再利用**を可能にする。
Imagine one user asks “What’s the capital of Vietnam?” and the model generates the answer “Hanoi”.
あるユーザが「ベトナムの首都は？」と尋ね、モデルが「ハノイ」という答えを生成するとします。
Later, another user asks “What’s the capital city of Vietnam?”, which is the same question but with the extra word “city”.
その後、別のユーザが「ベトナムの首都はどこですか？」と尋ねると、同じ質問ですが「どこ」という余分な単語が付いています。
The idea of semantic cache is that the system can reuse the answer “Hanoi” instead of computing the new query from scratch.
**セマンティック・キャッシュのアイデアは、システムが新しいクエリをゼロから計算する代わりに、「ハノイ」という答えを再利用できること**です。

Semantic cache only works if you have a reliable way to determine if two queries are semantically similar.
**セマンティックキャッシュは、2つのクエリが意味的に類似しているかどうかを判断する信頼できる方法を持っている場合にのみ機能する**。
One common approach is embedding-based similarity, which works as follows:
一般的なアプローチのひとつは埋め込みベースの類似性で、次のように動作する：

- 1. For each query, generate its embedding using an embedding model.
各クエリに対して、埋め込みモデルを用いて埋め込みを生成する。
- 2. Use vector search to find the cached embedding closest to the current query embedding.
ベクトル検索を使用して、現在のクエリ埋め込みに最も近いキャッシュ埋め込みを見つける。
Let’s say this similarity score is X.
この類似スコアをXとしよう。

- 3. If X is more than the similarity threshold you set, the cached query is considered the same as the current query, and the cached results are returned.
**Xが設定した類似度のしきい値以上であれば、キャッシュされたクエリは現在のクエリと同じとみなされ、キャッシュされた結果が返されます**。(なるほど...!:thinking:)
If not, process this current query and cache it together with its embedding and results.
そうでない場合は、現在のクエリを処理し、その埋め込みと結果とともにキャッシュする。

This approach requires a vector database to store the embeddings of cached queries.
このアプローチは、**キャッシュされたクエリの埋め込みを保存するためのベクトルデータベースを必要とする**。

Compared to other caching techniques, semantic cache’s value is more dubious because many of its components are prone to failure.
**他のキャッシュ技術に比べ、セマンティックキャッシュの価値は、その多くのコンポーネントが故障しやすいため、より疑わしい**。(なるほど、不確実性が高いというか...!:thinking:)
Its success relies on high-quality embeddings, functional vector search, and a trustworthy similarity metric.
**その成功は、高品質の埋め込み、機能的なベクトル探索、信頼できる類似性メトリックに依存している**。
Setting the right similarity threshold can also be tricky and require a lot of trial and error.
適切な類似度の**しきい値を設定するのも厄介**で、多くの試行錯誤を必要とする。(閾値設定は、それはそうだよな:thinking:)
If the system mistakes the incoming query as being similar to another query, the returned response, fetched from the cache, will be incorrect.
入力されたクエリが他のクエリと類似しているとシステムが誤認した場合、キャッシュから取得された返されたレスポンスは正しくないものとなる。

In addition, semantic cache can be time-consuming and compute-intensive, as it involves a vector search.
さらに、セマンティックキャッシュは**ベクトル検索を伴うため、時間がかかり、計算量が多くなることがあります**。
The speed and cost of this vector search depend on the size of your database of cached embeddings.
このベクトル検索の速度とコストは、キャッシュされた埋め込みデータベースのサイズに依存します。

Semantic cache might still be worth it if the cache hit rate is high, meaning that a good portion of queries can be effectively answered by leveraging the cached results.
**セマンティックキャッシュは、キャッシュヒット率が高い場合にはまだ価値があるかも**しれません。つまり、キャッシュされた結果を活用することで、クエリのかなりの部分に効果的に回答できる可能性があるということです。
However, before incorporating the complexities of semantic cache, make sure to evaluate the efficiency, cost, and performance risks associated with it.
**しかし、セマンティックキャッシュの複雑さを取り入れる前に、それに関連する効率、コスト、パフォーマンスリスクを評価することを忘れないでください。**

With the added cache systems, the platform looks as follows.
キャッシュシステムを追加したプラットフォームは以下のようになる。
KV cache and prompt cache are typically implemented by model API providers, so they aren’t shown in this image.
**KVキャッシュとプロンプトキャッシュは通常、モデルAPIプロバイダーによって実装されるため、この画像には表示されていない**。
If I must visualize them, I’d put them in the Model API box.
どうしても視覚化したいのであれば、モデルAPIのボックスに入れるだろう。
There’s a new arrow to add generated responses to the cache.
生成されたレスポンスをキャッシュに追加する新しい矢印がある。
(この図に書いてあるのはexact cacheとsemantic cacheか。手前側がexact cacheで、DBと接続してる奥側がsemantic cacheっぽい??:thinking:)

![]()

<!-- ここまで読んだ -->

## Step 5. Add complex logic and write actions ステップ5. 複雑なロジックの追加と書き込みアクション

The applications we’ve discussed so far have fairly simple flows.
これまで説明してきたアプリケーションは、かなりシンプルなフローを持っている。
The outputs generated by foundation models are mostly returned to users (unless they don’t pass the guardrails).
基礎モデルによって生成されたアウトプットは、（ガードレールを通過しない限り）ほとんどがユーザに返却される。
However, an application flow can be more complex with loops and conditional branching.
**しかし、アプリケーション・フローは、ループや条件分岐によってより複雑になる可能性がある**。
A model’s outputs can also be used to invoke write actions, such as composing an email or placing an order.
モデルの出力は Eメールの作成や注文の配置などのアクションを実行するために使用することもできる。

### Complex logic 複雑な論理

Outputs from a model can be conditionally passed onto another model or fed back to the same model as part of the input to the next step.
モデルからの出力は、条件付きで別のモデルに渡したり、次のステップへの入力の一部として同じモデルにフィードバックしたりすることができる。
This goes on until a model in the system decides that the task has been completed and that a final response should be returned to the user.
これは、システム内のモデルがタスクが完了したと判断し、**最終的なレスポンスをユーザに返すべきであると判断するまで**続く。

This can happen when you give your system the ability to plan and decide what to do next.
これは、システムに次の行動を計画し決定する能力を与えたときに起こりうる。(いわゆる Agent的な?:thinking:)
As an example, consider the query “Plan a weekend itinerary for Paris.” The model might first generate a list of potential activities: visiting the Eiffel Tower, having lunch at a café, touring the Louvre, etc.
例として、「Plan a weekend itinerary for Paris(パリの週末の旅程を計画して)」というクエリを考えてみましょう。モデルはまず、潜在的な活動のリストを生成するかもしれません：エッフェル塔を訪れる、カフェで昼食をとる、ルーブル美術館を見学するなど。
Each of these activities can then be fed back into the model to generate more detailed plans.
これらの活動のそれぞれをモデルにフィードバックして、より詳細な計画を生成することができる。
For instance, “visiting the Eiffel Tower” could prompt the model to generate sub-tasks like checking the opening hours, buying tickets, and finding nearby restaurants.
例えば、「エッフェル塔を訪れる」とすると、営業時間の確認、チケットの購入、近くのレストランの検索などのサブタスクを生成するようモデルを促すことができる。
This iterative process continues until a comprehensive and detailed itinerary is created.
この反復プロセスは、包括的で詳細な旅程が作成されるまで続けられる。

Our infrastructure now has an arrow pointing the generated response back to context construction, which in turn feeds back to models in the model gateway.
私たちのインフラストラクチャーは、**生成されたレスポンスをcontext constructionに戻す矢印を持ち**、それがモデルゲートウェイ内のモデルにフィードバックされる。

<!-- ここまで読んだ -->

### Write actions アクションを書く

Actions used for context construction are read-only actions.
context constructionに使用されるアクションは、**読み取り専用のアクション**です。(?)
They allow a model to read from its data sources to gather context.
これにより、モデルはデータソースから読み取ってコンテキストを収集することができる。
But a system can also write actions, making changes to the data sources and the world.
しかし、システムは書き込みアクションも行うことができ、データソースや世界を変更することができる。
For example, if the model outputs: “send an email to X with the message Y”, the system will invoke the action send_email(recipient=X, message=Y).
例えば、モデルが 「send an email to X with the message Y(メッセージYを含むXにEメールを送信する)」と出力した場合、**システムはsend_email(recipient=X, message=Y)アクションを呼び出す**。(Agent likeな感じがする:thinking:)

Write actions make a system vastly more capable.
**書き込みアクションは、システムをはるかに能力的にする**。
They can enable you to automate the whole customer outreach workflow: researching potential customers, finding their contacts, drafting emails, sending first emails, reading responses, following up, extracting orders, updating your databases with new orders, etc.
これにより、潜在的な顧客の調査、連絡先の検索、メールの起案、最初のメールの送信、返信の読み取り、フォローアップ、注文の抽出、新しい注文でデータベースを更新するなど、**顧客アウトリーチのワークフロー全体を自動化することができる**。

However, the prospect of giving AI the ability to automatically alter our lives is frightening.
しかし、AIに我々の生活を自動的に変更する能力を与えるという見通しは恐ろしい。
Just as you shouldn’t give an intern the authority to delete your production database, you shouldn’t allow an unreliable AI to initiate bank transfers.
**インターンに本番データベースを削除する権限を与えてはいけないように、信頼性のないAIに銀行振込を開始させてはいけない**。
Trust in the system’s capabilities and its security measures is crucial.
システムの能力とセキュリティ対策への信頼は極めて重要です。
You need to ensure that the system is protected from bad actors who might try to manipulate it into performing harmful actions.
システムを操作して有害なアクションを実行させようとする悪質な行為者からシステムを保護する必要があります。

AI systems are vulnerable to cyber attacks like other software systems, but they also have another weakness: prompt injection.
AIシステムは他のソフトウェア・システムと同様にサイバー攻撃に脆弱だが、もう一つの弱点もある: **prompt injection(プロンプト・インジェクション)**。
Prompt injection happens when an attacker manipulates input prompts into a model to get it to express undesirable behaviors.
prompt injectionは、攻撃者がモデルに不適切な振る舞いをさせるために入力プロンプトを操作するときに発生する。
You can think of prompt injection as social engineering done on AI instead of humans.
prompt injectionは、人間ではなくAIに対して行われるソーシャルエンジニアリングと考えることができる。

A scenario that many companies fear is that they give an AI system access to their internal databases, and attackers trick this system into revealing private information from these databases.
**多くの企業が恐れているシナリオは、AIシステムに社内データベースへのアクセス権を与え、攻撃者がこのシステムを騙してデータベースから個人情報を漏えいさせること**だ。
If the system has write access to these databases, attackers can trick the system into corrupting the data.
システムにこれらのデータベースへの書き込みアクセス権がある場合、攻撃者はシステムを騙してデータを破壊させることができる。

Any organization that wants to leverage AI needs to take safety and security seriously.
AIを活用しようとする組織は、安全性とセキュリティに真剣に取り組む必要がある。
However, these risks don’t mean that AI systems should never be given the ability to act in the real world.
**しかし、こうしたリスクがあるからといって、AIシステムに現実世界で行動する能力を与えてはいけないというわけではありません**。
AI systems can fail, but humans can fail too.
**AIシステムは失敗する可能性があるが、人間も失敗する可能性がある。**
If we can get people to trust a machine to take us up into space, I hope that one day, securities will be sufficient for us to trust autonomous AI systems.
人々が機械に宇宙に連れて行ってもらうことを信頼できるようになれば、いつかはセキュリティが十分であることを願って、自律型AIシステムを信頼できるようになるでしょう。

![]()

<!-- ここまで読んだ -->

## Observability 観測可能性

While I have placed observability in its own section, it should be integrated into the platform from the beginning rather than added later as an afterthought.
私はobservabilityを独自のセクションに配置しましたが、それは**後から後付けで追加するのではなく、最初からプラットフォームに統合されるべき**です。
Observability is crucial for projects of all sizes, and its importance grows with the complexity of the system.
**observabilityは、あらゆる規模のプロジェクトにとって重要であり、その重要性はシステムの複雑さとともに増していきます**。

This section provides the least information compared to the others.
このセクションは、他のセクションに比べ最も情報が少ない。
It’s impossible to cover all the nuances of observability in a blog post.
ブログの記事でobservabilityのすべてのニュアンスをカバーすることは不可能です。
Therefore, I will only give a brief overview of the three pillars of monitoring: logs, traces, and metrics.
そのため、ここでは**モニタリングの3本柱について簡単に説明するにとどめる: Logs, Traces, Metrics**。
I won’t go into specifics or cover user feedback, drift detection, and debugging.
具体的な内容や、user feedback, drift detection, debuggingについては触れません。

### Metrics メトリクス

When discussing monitoring, most people think of metrics.
モニタリングについて議論するとき、多くの人はメトリクスを思い浮かべる。
What metrics to track depends on what you want to track about your system, which is application-specific.
**どのようなメトリクスを追跡するかは、システムに関して何を追跡したいかに依存し、それはアプリケーション固有である**。
However, in general, there are two types of metrics you want to track: model metrics and system metrics.
しかし一般的に、**追跡したいメトリクスには2種類あります: モデルメトリクスとシステムメトリクス**。

System metrics tell you the state of your overall system.
**システム・メトリクスは、システム全体の状態を示します**。
Common metrics are throughput, memory usage, hardware utilization, and service availability/uptime.
一般的なメトリクスは、スループット、メモリ使用量、ハードウェア使用率、およびサービスの可用性/アップタイムである。
System metrics are common to all software engineering applications.
**システム・メトリクスは、すべてのソフトウェア・エンジニアリング・アプリケーションに共通**です。
In this post, I’ll focus on model metrics.
この記事では、モデルのメトリクスに焦点を当てます。

Model metrics assess your model’s performance, such as accuracy, toxicity, and hallucination rate.
**モデルメトリクスは、accuracy(精度)、toxicity(有毒性)、hallucination rate(幻覚率)など、モデルのパフォーマンスを評価**します。
Different steps in an application pipeline also have their own metrics.
**アプリケーション・パイプラインの異なるステップには、それぞれ独自のメトリクス**があります。
For example, in a RAG application, the retrieval quality is often evaluated using context relevance and context precision.
例えば、RAGアプリケーションでは、検索品質は、コンテキストの関連性とコンテキストの精度を使用して評価されることがよくあります。
A vector database can be evaluated by how much storage it needs to index the data and how long it takes to query the data
ベクトル・データベースは、データをインデックス化するために必要なストレージ量とデータをクエリするのにかかる時間で評価できる。

There are various ways a model’s output can fail.
**モデルの出力にはさまざまな失敗の仕方**がある。
It’s crucial to identify these issues and develop metrics to monitor them.
このような**問題を特定し、それを監視するための指標を開発することが極めて重要**である。
For example, you might want to track how often your model times out, returns empty responses or produces malformatted responses.
例えば、モデルがタイムアウトする頻度や、空のレスポンスを返す頻度、あるいは不正な形式のレスポンスを生成する頻度を追跡したい場合がある。
If you’re worried about your model revealing sensitive information, find a way to track that too.
機密情報を漏洩する可能性がある場合は、それを追跡する方法を見つける必要がある。

Length-related metrics such as query, context, and response length are helpful for understanding your model’s behaviors.
クエリ、コンテキスト、レスポンスの長さなど、**長さに関連するメトリクスは、モデルの動作を理解するのに役立つ**。
Is one model more verbose than another? Are certain types of queries more likely to result in lengthy answers? They are especially useful for detecting changes in your application.
あるモデルは他のモデルよりも冗長ですか？ 特定のタイプのクエリが長い回答をもたらす可能性が高いですか？ これらは、アプリケーションの変更を検出するのに特に役立ちます。
If the average query length suddenly decreases, it could indicate an underlying issue that needs investigation.
平均クエリの長さが突然減少した場合、調査が必要な潜在的な問題を示している可能性があります。

Length-related metrics are also important for tracking latency and costs, as longer contexts and responses typically increase latency and incur higher costs.
長さに関連するメトリクスは、待ち時間とコストを追跡するためにも重要です。長いコンテキストと回答は通常、待ち時間が増加し、コストが高くなります。

Tracking latency is essential for understanding the user experience.
**latencyを追跡することは、ユーザ体験を理解するために不可欠**です。
Common latency metrics include:
一般的な待ち時間の指標には、以下のようなものがある:

- **Time to First Token (TTFT)**: The time it takes for the first token to be generated.
Time to First Token (TTFT)（最初のトークンまでの時間）： 最初のトークンが生成されるまでの時間。

- **Time Between Tokens (TBT)**: The interval between each token generation.
トークン間時間（TBT）： 各トークンが生成される間隔。

- **Tokens Per Second (TPS)**: The rate at which tokens are generated.
トークン・パー・セカンド（TPS）： トークンが生成される速度。

- **Time Per Output Token (TPOT)**: The time it takes to generate each output token.
出力トークンあたりの時間（TPOT）： 各出力トークンの生成にかかる時間。

- **Total Latency**: The total time required to complete a response.
トータル・レイテンシー： 応答を完了するのに必要な時間の合計。

You’ll also want to track costs.
**また、コストも把握しておきたい**。
Cost-related metrics are the number of queries and the volume of input and output tokens.
コストに関連するメトリクスは、クエリ数と入力および出力トークンの量である。
If you use an API with rate limits, tracking the number of requests per second is important to ensure you stay within your allocated limits and avoid potential service interruptions.
**レート制限のあるAPIを使用している場合、秒間リクエスト数を追跡することは重要**です。割り当てられた制限内にとどまり、潜在的なサービスの中断を回避するためです。

When calculating metrics, you can choose between spot checks and exhaustive checks.
**メトリクスを計算する際、spot checks(スポット・チェック)とexhaustive checks(徹底的なチェック)のどちらかを選択**できる。
Spot checks involve sampling a subset of data to quickly identify issues, while exhaustive checks evaluate every request for a comprehensive performance view.
スポット・チェックでは、データのサブセットをサンプリングして問題を素早く特定しますが、徹底的なチェックは、包括的なパフォーマンスビューを得るためにすべてのリクエストを評価します。
The choice depends on your system’s requirements and available resources, with a combination of both providing a balanced monitoring strategy.
**どちらを選択するかは、システムの要件と利用可能なリソースに依存し、両方を組み合わせることで、バランスの取れた監視戦略を実現できる**。

When computing metrics, ensure they can be broken down by relevant axes, such as users, releases, prompt/chain versions, prompt/chain types, and time.
メトリクスを計算するときは、ユーザ、リリース、プロンプト/チェーンのバージョン、プロンプト/チェーンのタイプ、時間など、**関連する軸で分解できること**を確認してください。
This granularity helps in understanding performance variations and identifying specific issues.
この細かさは、パフォーマンスの変動を理解し、特定の問題を特定するのに役立ちます。

### Logs ログ

Since this blog post is getting long and I’ve written at length about logs in [Designing Machine Learning Systems](https://www.amazon.com/Designing-Machine-Learning-Systems-Production-Ready/dp/1098107969?&_encoding=UTF8&tag=chiphuyen-20&linkCode=ur2&linkId=0a1dbab0e76f5996e29e1a97d45f14a5&camp=1789&creative=9325), I will be quick here.
このブログの記事は長くなってきたし、ログについては「機械学習システムの設計」で詳しく書いたので、ここでは手短にする。
(あ、このブログの著者の人、「機械学習システムデザイン」の著者の人なのか! ログのことそんなに書いてあったっけ...??:thinking:)
The philosophy for logging is simple: log everything.
**ロギングの哲学はシンプルだ： log everything(すべてを記録する)**。
Log the system configurations.
システム構成を記録する。
Log the query, the output, and the intermediate outputs.
クエリ、出力、中間出力を記録する。
Log when a component starts, ends, when something crashes, etc.
コンポーネントの開始、終了、クラッシュなどのログを記録する。
When recording a piece of log, make sure to give it tags and IDs that can help you know where in the system this log comes from.
ログを記録する際には、そのログがシステムのどこから来たものかを知るのに役立つタグやIDをつけるようにする。

Logging everything means that the amount of logs you have can grow very quickly.
**すべてのログを取るということは、ログの量があっという間に増えるということだ。**
Many tools for automated log analysis and log anomaly detection are powered by AI.
自動ログ解析やログ異常検出のための多くのツールはAIによって動作している。

While it’s impossible to manually process logs, it’s useful to manually inspect your production data daily to get a sense of how users are using your application.
ログを手動で処理することは不可能ですが、**毎日プロダクションデータを手動で検査して、ユーザがアプリケーションをどのように使用しているかを把握することは有用**です。(少量のログを...!ってことね。)
Shankar et al.(2024) found that the developers’ perceptions of what constitutes good and bad outputs change as they interact with more data, allowing them to both rewrite their prompts to increase the chance of good responses and update their evaluation pipeline to catch bad responses.
Shankarら(2024)は、開発者がアプリケーションのデータをより多く扱うことで、「良い出力」と「悪い出力」に対する認識が変化する、という点が強調されています。**開発者は、ユーザが実際にどうアプリケーションを使っているかを直接見ることで、自分が最初に持っていた仮定や期待とは異なることに気づくことがあります**。 これにより、開発者は、良いレスポンスの確率を高めるためにプロンプトを書き直したり、悪いレスポンスをキャッチするために評価パイプラインを更新したりすることができます。

### Traces 痕跡

Trace refers to the detailed recording of a request’s execution path through various system components and services.
**トレースとは、様々なシステムコンポーネントやサービスを介したリクエストの実行パスの詳細な記録**を指す。
In an AI application, tracing reveals the entire process from when a user sends a query to when the final response is returned, including the actions the system takes, the documents retrieved, and the final prompt sent to the model.
**AIアプリケーションでは、ユーザがクエリを送信してから最終的なレスポンスが返されるまでのプロセス全体をトレースする**ことで、システムが実行するアクション、取得されるドキュメント、モデルに送信される最終的なプロンプトなどが明らかになります。
It should also show how much time each step takes and its associated cost, if measurable.
また、測定可能であれば、各工程にかかる時間と関連するコストも示す必要がある。
As an example, this is a visualization of a Langsmith trace.
例として、これはラングスミスのトレースを視覚化したものである。

![](https://huyenchip.com/assets/pics/genai-platform/15-traces.png)

Ideally, you should be able to trace each query’s transformation through the system step-by-step.
**理想的には、各クエリがシステムを通じてどのように変化していくかを、ステップバイステップで追跡できるようにすること**である。
If a query fails, you should be able to pinpoint the exact step where it went wrong: whether it was incorrectly processed, the retrieved context was irrelevant, or the model generated a wrong response.
クエリが失敗した場合、失敗したステップを正確に突き止めることができるはずです: それが誤って処理されたか、取得されたコンテキストが関連性がなかったか、モデルが誤った応答を生成したかどうか。

<!-- ここまで読んだ -->

## AI Pipeline Orchestration AIパイプラインのオーケストレーション

An AI application can get fairly complex, consisting of multiple models, retrieving data from many databases, and having access to a wide range of tools.
A**Iアプリケーションはかなり複雑になり、複数のモデル、多くのデータベースからのデータの取得、さまざまなツールへのアクセスから構成される**ことがあります。
An orchestrator helps you specify how these different components are combined (chained) together to create an end-to-end application flow.
オーケストレーターは、エンド・ツー・エンドのアプリケーション・フローを作成するために、これらの異なるコンポーネントをどのように組み合わせる（連鎖させる）かを指定するのに役立つ。

At a high level, an orchestrator works in two steps: components definition and chaining (also known as pipelining).
高レベルでは、オーケストレーターは2つのステップで動作する: コンポーネントの定義とチェーン化（またはパイプライン化）。

### Components Definition コンポーネントの定義

You need to tell the orchestrator what components your system uses, such as models (including models for generation, routing, and scoring), databases from which your system can retrieve data, and actions that your system can take.
モデル（生成、ルーティング、スコアリングのモデルを含む）、システムがデータを取得できるデータベース、システムが実行できるアクションなど、システムが使用するコンポーネントをオーケストレーターに伝える必要がある。
Direct integration with model gateways can help simplify model onboarding, and some orchestrator tools want to be gateways.
モデルゲートウェイとの直接統合は、モデルのオンボーディングを簡素化するのに役立ち、一部のオーケストレーターツールはゲートウェイであることを望んでいる。
Many orchestrators also support integration with tools for evaluation and monitoring.
多くのオーケストレーターは、評価やモニタリングのためのツールとの統合もサポートしている。

### Chaining (or pipelining) チェーン化（またはパイプライン化）

You tell the orchestrator the sequence of steps your system takes from receiving the user query until completing the task.
あなたはオーケストレーターに、ユーザからの問い合わせを受けてからタスクを完了するまでにシステムが取る一連のステップを指示する。
In short, chaining is just function composition.
要するに、チェイニングとは単なる関数の合成である。
Here’s an example of what a pipeline looks like.
これがパイプラインの例だ。

1. Process the raw query.
生のクエリを処理する。

2. Retrieve the relevant data based on the processed query.
処理されたクエリに基づいて関連データを取得する。

3. The original query and the retrieved data are combined to create a prompt in the format expected by the model.
元のクエリと検索されたデータが組み合わされ、モデルが期待する形式のプロンプトが作成される。

4. The model generates a response based on the prompt.
モデルは、プロンプトに基づいて応答を生成する。

5. Evaluate the response.
対応を評価する。

6. If the response is considered good, return it to the user.
返答が良いと判断されれば、それをユーザーに返す。
If not, route the query to a human operator.
そうでない場合は、人間のオペレーターにクエリをルーティングする。

The orchestrator is responsible for passing data between steps and can provide toolings that help ensure that the output from the current step is in the format expected by the next step.
オーケストレーターは、ステップ間のデータの受け渡しを担当し、現在のステップからの出力が次のステップで期待される形式であることを保証するのに役立つツーリングを提供することができる

---

When designing the pipeline for an application with strict latency requirements, try to do as much in parallel as possible.
レイテンシが厳しく要求されるアプリケーションのパイプラインを設計する場合、可能な限り並列処理を行うようにする。
For example, if you have a routing component (deciding where to send a query to) and a PII removal component, they can do both at the same time.
例えば、ルーティング・コンポーネント（クエリの送信先を決定する）と PII(個人を特定する情報)削除コンポーネントがある場合、両方を同時に行うことができる。

There are many AI orchestration tools, including LangChain, LlamaIndex, Flowise, Langflow, and Haystack.
**LangChain、LlamaIndex、Flowise、Langflow、Haystackなど、多くのAIオーケストレーションツール**がある。
Each tool has its own APIs so I won’t show the actual code here.
それぞれのツールは独自のAPIを持っているので、ここでは実際のコードは示さない。

While it’s tempting to jump straight to an orchestration tool when starting a project, start building your application without one first.
プロジェクトを始めるとき、すぐにオーケストレーション・ツールに飛びつきたくなるが、**まずはオーケストレーション・ツールなしでアプリケーションの構築を始めよう**。
Any external tool brings added complexity.
**外部ツールは複雑さをもたらす**。
An orchestrator can abstract away critical details of how your system works, making it hard to understand and debug your system.
オーケストレーターは、システムがどのように動作するかという重要な詳細を抽象化し、システムを理解したりデバッグしたりすることを難しくする。

As you advance to the later stages of your application development process, you might decide that an orchestrator can make your life easier.
アプリケーション開発プロセスの後半に進むにつれて、オーケストレーターを使えばもっと楽になると思うかもしれない。
Here are three aspects to keep in mind when evaluating orchestrators.
**オーケストレーターを評価する際に留意すべき点**を3つ挙げる。

1. Integration and extensibility 統合性と拡張性

Evaluate whether the orchestrator supports the components you’re already using or might adopt in the future.
オーケストレーターが、すでに使用している、あるいは将来採用する可能性のあるコンポーネントをサポートしているかどうかを評価する。
For example, if you want to use a Llama model, check if the orchestrator supports that.
例えば、Llamaモデルを使いたい場合、オーケストレーターがそれをサポートしているかどうかを確認する。
Given how many models, databases, and frameworks there are, it’s impossible for an orchestrator to support everything.
モデル、データベース、フレームワークの数を考えると、オーケストレーターがすべてをサポートすることは不可能だ。
Therefore, you’ll also need to consider an orchestrator’s extensibility.
したがって、オーケストレーターの拡張性も考慮する必要がある。
If it doesn’t support a specific component, how hard it is to change that?
特定のコンポーネントをサポートしていない場合、それを変更するのは難しいのでしょうか？

2. Support for complex pipelines 複雑なパイプラインのサポート

As your applications grow in complexity, you might need to manage intricate pipelines involving multiple steps and conditional logic.
アプリケーションが複雑になってくると、複数のステップや条件ロジックを含む複雑なパイプラインを管理する必要が出てくる。
An orchestrator that supports advanced features like branching, parallel processing, and error handling will help you manage these complexities efficiently.
分岐、並列処理、エラー処理などの高度な機能をサポートするオーケストレーターは、こうした複雑な処理を効率的に行うのに役立つ。

1. Ease of use, performance, and scalability 使いやすさ、パフォーマンス、スケーラビリティ

Consider the user-friendliness of the orchestrator.
オーケストレーターの使いやすさを考えてみよう。
Look for intuitive APIs, comprehensive documentation, and strong community support, as these can significantly reduce the learning curve for you and your team.
直感的なAPI、包括的なドキュメント、強力なコミュニティ・サポートを探すこと。
Avoid orchestrators that initiate hidden API calls or introduce latency to your applications.
隠れたAPI呼び出しを開始したり、アプリケーションに遅延を導入するオーケストレーターは避けるべきだ。
Additionally, ensure that the orchestrator can scale effectively as the number of applications, developers, and traffic grows.
さらに、アプリケーション数、開発者数、トラフィック数の増加に応じて、オーケストレータが効率的にスケーリングできることを確認する。

<!-- ここまで読んだ -->

## Conclusion 結論

This post started with a basic architecture and then gradually added components to address the growing application complexities.
この投稿は、基本的なアーキテクチャから始まり、複雑化するアプリケーションに対応するために徐々にコンポーネントを追加していった。
Each addition brings its own set of benefits and challenges, requiring careful consideration and implementation.
それぞれの追加は、独自の利点と課題をもたらし、慎重な検討と実装が必要となる。

While the separation of components is important to keep your system modular and maintainable, this separation is fluid.
コンポーネントの分離は、システムをモジュール化し、保守可能に保つために重要ですが、この分離は流動的です。
There are many overlaps between components.
コンポーネント間には多くの重複がある。
For example, a model gateway can share functionalities with guardrails.
例えば、モデル・ゲートウェイはガードレールと機能を共有することができる。
Cache can be implemented in different components, such as in vector search and inference services.
キャッシュは、ベクトル検索や推論サービスなど、さまざまなコンポーネントで実装できる。

This post is much longer than I intended it to be, and yet there are many details I haven’t been able to explore further, especially around observability, context construction, complex logic, cache, and guardrails.
この投稿は、私が意図していたよりもずっと長くなってしまった。それでも、特にobservability、context construction、complex logic、cache、guardrailsなど、さらに掘り下げることができなかった詳細がたくさんある。
I’ll dive deeper into all these components in my upcoming book AI Engineering.
これらの構成要素については、近々出版予定の拙著『AIエンジニアリング』でさらに深く掘り下げるつもりだ。

This post also didn’t discuss how to serve models, assuming that most people will be using models provided by third-party APIs.
**この投稿では、ほとんどの人がサードパーティのAPIから提供されたモデルを使うことを想定して、モデルを提供する方法についても触れていない**。
AI Engineering will also have a chapter dedicated to inference and model optimization.
また、AIエンジニアリングでは、推論とモデルの最適化に関する章も設けられる。

## References and Acknowledgments

Special thanks to Luke Metz, Alex Li, Chetan Tekur, Kittipat “Bot” Kampa, Hien Luu, and Denys Linkov for feedback on the early versions of this post.
この記事の初期バージョンに対するフィードバックをいただいたLuke Metz、Alex Li、Chetan Tekur、Kittipat “Bot” Kampa、Hien Luu、Denys Linkovに特別な感謝を申し上げます。
Their insights greatly improved the content.
彼らの洞察が内容を大きく改善した。
Any remaining errors are my own.
残りの誤りは私の責任である。

I read many case studies shared by companies on how they adopted generative AI, and here are some of my favorites.
私は、企業がどのようにジェネレーティブAIを採用したかについて共有した多くのケーススタディを読んだ。

Musings on Building a Generative AI Product (LinkedIn, 2024)
ジェネレーティブAI製品の構築に関する考察（LinkedIn、2024年）

How we built Text-to-SQL at Pinterest (Pinterest, 2024)
PinterestでText-to-SQLをどのように構築したか（Pinterest、2024年）
(あ、これ読んだやつだ!:point_up:)

From idea to reality: Elevating our customer support through generative AI (Vimeo, 2023)
アイデアから現実へ： ジェネレーティブAIによるカスタマーサポートの向上（Vimeo、2023年）

A deep dive into the world’s smartest email AI (Shortwave, 2023)
世界一賢いメールAIを深堀りする（短波、2023年）

LLM-powered data classification for data entities at scale (Grab, 2023)
LLMによるデータ・エンティティの大規模分類（Grab, 2023）

From Predictive to Generative - How Michelangelo Accelerates Uber’s AI Journey (Uber, 2024)
予測から生成へ - ミケランジェロが加速するウーバーのAIの旅（Uber, 2024）

<!-- ここまで読んだ -->
