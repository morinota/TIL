# Meta Knowledge for Retrieval Augmented Large Language Models 大規模言語モデルを拡張した検索のためのメタ知識

## Abstract

Retrieval Augmented Generation (RAG) is a technique used to augment Large Language Models (LLMs) with contextually relevant, time-critical, or domain-specific information without altering the underlying model parameters.
検索拡張生成（RAG）は、ラージ・ランゲージ・モデル（LLM）を、基本的な**モデル・パラメータを変更することなく、文脈に関連する情報、タイムクリティカルな情報、またはドメイン固有の情報で拡張するために**使用される手法である。
However, constructing RAG systems that can effectively synthesize information from large and diverse set of documents remains a significant challenge.
しかし、大量かつ多様な文書群から効率的に情報を合成できるRAGシステムを構築することは、依然として大きな課題である。
We introduce a novel data-centric RAG workflow for LLMs, transforming the traditional retrieve-then-read system into a more advanced prepare-then-rewrite-then-retrieve-then-read framework, to achieve higher domain expert-level understanding of the knowledge base.
我々は、LLMのための新しいデータ中心のRAGワークフローを導入し、従来のretrieve-then-readシステムを、より高度なprepare-then-rewrite-hen-retrieve-then-readフレームワークへと変換することで、知識ベースのより高いドメインエキスパートレベルの理解を達成する。
Our methodology relies on generating metadata and synthetic Questions and Answers (QA) for each document, as well as introducing the new concept of Meta Knowledge Summary (MK Summary) for metadata-based clusters of documents.
我々の方法論は、各文書のメタデータと合成QA（Question and Answers）を生成し、メタデータベースの文書クラスタのためにメタ知識要約（Meta Knowledge Summary：MK要約）という新しい概念を導入することに依存している。
The proposed innovations enable personalized user-query augmentation and in-depth information retrieval across the knowledge base.
提案された技術革新は、パーソナライズされたユーザ・クエリの拡張と、知識ベース全体にわたる詳細な情報検索を可能にする。
Our research makes two significant contributions: using LLMs as evaluators and employing new comparative performance metrics, we demonstrate that (1) using augmented queries with synthetic question matching significantly outperforms traditional RAG pipelines that rely on document chunking (p <0.01), and (2) meta knowledge-augmented queries additionally significantly improve retrieval precision and recall, as well as the final answer’s breadth, depth, relevancy, and specificity.
我々の研究は2つの重要な貢献をしている： (1)合成質問マッチングで拡張クエリを使用することで、文書チャンキングに依存する従来のRAGパイプラインを有意に上回ること(p <0.01)、(2)メタ知識で拡張されたクエリは、検索精度とリコール、さらに最終的な回答の幅、深さ、関連性、特異性を有意に向上させること。
Our methodology is cost-effective, costing less than $20 per 2000 research papers using Claude 3 Haiku, and can be adapted with any fine-tuning of either the language or embedding models to further enhance the performance of end-to-end RAG pipelines.
我々の方法論は**費用対効果が高く**、Claude 3 Haikuを使用した2000本の研究論文あたり20ドル以下であり、エンドツーエンドのRAGパイプラインの性能をさらに向上させるために、言語またはエンベッディングモデルのいずれかを微調整して適応させることができる。

## Introduction

Figure 1.Data-centric workflow for Retrieval Augmented Generation (RAG) systems.
図1.RAG（Retrieval Augmented Generation）システムのデータ中心ワークフロー。
Prior to inference, documents are augmented with Claude 3, and clustered into metadata-based sets of synthetic questions and answers for personalized downstream retrieval.
推論に先立ち、文書はクロード3で補強され、パーソナライズされた下流検索のために、合成質問と回答のメタデータベースのセットにクラスタ化される。
Meta Knowledge Summaries are used to guide the query augmentation step with clusters information.
メタ知識要約は、クラスタ情報によるクエリ拡張ステップのガイドとして使用される。

Retrieval Augmented Generation (RAG) is a standard technique used to augment Large Language Models (LLMs) with the capability to integrate contextually relevant, time-critical, or domain-specific information without altering the underlying model weights.
検索拡張生成（RAG）は、ラージ・ランゲージ・モデル（LLM）に、基本的なモデルの重みを変更することなく、文脈に関連する情報、タイムクリティカルな情報、またはドメイン固有の情報を統合する機能を追加するために使用される標準的な手法である。
This approach is particularly effective for knowledge-intensive tasks where proprietary or timely data is required to guide the language model’s response, and has become an attractive solution for reducing model hallucinations and ensuring alignment with the latest and most relevant information for the task at hand.
このアプローチは、言語モデルの応答を導くために独自のデータやタイムリーなデータが必要とされる知識集約型のタスクに特に効果的であり、モデルの幻覚を減らし、目の前のタスクに最新かつ最も関連性の高い情報との整合性を確保するための魅力的なソリューションとなっている。
In practice, RAG pipelines consist of several modules structured around the traditional retrieve-then-read framework (lewis2020retrieval,).
実際には、RAGパイプラインは、伝統的なretrieve-then-readフレームワーク(lewis2020retrieval,)を中心に構造化された複数のモジュールで構成されている。
Given a user question, a retriever is tasked with dynamically searching for related document chunks and providing them as context for the LLM to predict the answer, rather than relying solely on pre-trained model knowledge (also known as in-context learning).
ユーザーの質問が与えられると、レトリーバーは、事前に学習されたモデルの知識だけに頼るのではなく、関連するドキュメントのチャンクを動的に検索し、LLMが答えを予測するためのコンテキストとして提供するタスクを負う（コンテキスト内学習とも呼ばれる）。
A simple, yet powerful and cost-effective retriever framework involves using a dual-encoder dense retrieval model to encode both the query and the documents individually into a high-dimensional vector space, and computing their inner product as a measure of similarity (karpukhin2020dense,).
**シンプルで強力かつコスト効率の良い検索フレームワークは、クエリと文書をそれぞれ高次元ベクトル空間にエンコードし、その内積を類似度の尺度として計算する、dual-encoder dense retrieval model(デュアルエンコーダ密検索モデル)**を用いる(karpukhin2020dense,)。
(dual-encoderって表現されるのか、tow-towerモデルと意味合いは近そう...!:thinking:)

However, several challenges specifically hinder the quality of the knowledge augmented context.
しかし、知識補強されたコンテキストの質を特に妨げている課題がいくつかある。
First, knowledge base documents may contain substantial noise, either intrinsic for the task at hand or as a result of the lack of standardization across the documents of interest (from various documents layouts or formats such as .pdf, .ppt, .wordx, etc.).
第一に、**知識ベース文書には多大なノイズが含まれている可能性**があり、それは、手元のタスクに固有のものであるか、または興味のある文書間の標準化の欠如によるものである可能性がある（さまざまな文書のレイアウトや形式（.pdf、.ppt、.wordxなど））。
Second, little to no human-labelled information or relevance labels are typically available to support the document chunking, embedding, and retrieval processes, making the overall retrieval problem a largely unsupervised approach and challenging to personalize for a given user.
第二に、文書のチャンキング、埋め込み、および検索プロセスをサポートするための人間によるラベル付け情報や関連性ラベルはほとんどないか、一般的に利用できないため、全体的な検索問題は主に教師なしアプローチであり、特定のユーザに対してパーソナライズすることが難しい。
Third, chunking and separately encoding long documents pose a challenge in extracting relevant information for the retrieval models (gao2023retrieval,).
第三に、**長い文書をチャンキングし、別々にエンコードすること**(確かにこれは、直感的にもよくなさそう:thinking:)は、検索モデルにとって関連情報を抽出する際の課題となる(gao2023retrieval,)。
Indeed, document chunks do not conserve the semantic context of the entire document, and the larger the chunk, the less precise the context of the chunk is maintained for further retrieval.
**実際、文書チャンクは全文書の意味的コンテキストを保存しておらず**、チャンクが大きいほど、チャンクのコンテキストがさらなる検索に保持されるのが不正確になる。
This makes the choice of document chunking strategy non-trivial for a given use-case, although critical for the quality of the subsequent steps due to potentially significant information loss.
このため、文書のチャンキング戦略の選択は、与えられたユースケースにとって自明なことではないが、潜在的に重大な情報損失のため、後続のステップの品質にとって重要である。
Fourth, user queries are typically short, ambiguous, may contain vocabulary mismatches, or are complex enough to require multiple documents to address, making it generally difficult to precisely capture the user’s intents and subsequently identify the most appropriate documents to retrieve (zhu2023large,).
第四に、ユーザクエリは一般的に短く、曖昧で、語彙の不一致があるか、複数の文書を必要とするほど複雑であり、ユーザの意図を正確に捉え、その後、最適な文書を特定するのが一般的に難しい（zhu2023large,)。
Finally, there is no guarantee that the relevant information is localized in the knowledge base, but rather spread across multiple documents.
最後に、**関連情報が知識ベースに局在していることは保証されておらず、むしろ複数の文書に分散している可能性がある**。
As a result, domain expert-level usage of the knowledge base is made dramatically more challenging with automated information retrieval systems.
その結果、自動化された情報検索システムを用いた知識ベースのドメインエキスパートレベルの使用は、著しく困難になる。
Such high level reasoning across the knowledge base is a yet unsolved problem and constitutes the basis for recent LLM-based retrieval agent frameworks research.
このような知識ベース全体にわたる高レベルの推論は、未解決の問題であり、最近のLLMベースの検索エージェントフレームワークの研究の基礎をなしている。

<!-- ここまで読んだ! -->

In this work, we are interested in cases where user queries require the information search to be specific to users interests or profile, are ambiguous, and require high level reasoning across documents (for example: “What challenges are associated with applying machine learning for marketing?”), making recall, specificity, and depth our metrics of interest.
この研究では、ユーザクエリがユーザの興味やプロフィールに特化している必要があり、曖昧であり、文書全体にわたる高レベルの推論が必要な場合に興味がある（例：「マーケティングに機械学習を適用する際に関連する課題は何ですか？」）、リコール、特異性、深さが興味の対象となるメトリクスとなる。
To improve the search results performance across those metrics, query augmentation has been a widely used technique in both traditional Information Retrieval (IR) use cases such as e-commerce search (peng2024large,), as well as in the more recent RAG frameworks leveraging LLMs (gao2022precise,).
これらのメトリクス全体にわたる検索結果のパフォーマンスを向上させるために、**query augmentation**は、従来の情報検索（IR）のユースケース（例：電子商取引検索(peng2024large,)）だけでなく、LLMを活用した最近のRAGフレームワーク(gao2022precise,)でも広く使用されている技術である。
Query augmentation consists in explicitly rewriting or extending the original user query into one or more tailored queries that better match search results, alleviating issues related to query underspecification.
**クエリ拡張とは、元のユーザクエリを明示的に書き換えたり拡張したりして、検索結果により適合するクエリにする**ことで、クエリの不十分な指定に関連する問題を緩和するものである。
This adjustment adds a module to the RAG framework and transforms it into the more sophisticated rewrite-then-retrieve-then-read workflow.
この調整により、RAGフレームワークにモジュールが追加され、**より洗練された「rewrite(書き換え)→retrieve(検索)→read(読む)」のワークフロー**に変換される。
Leveraging their vast underlying parametric world knowledge, LLMs constitute a fitting choice to understand and enhance users queries, subsequently boosting the relevance of the retrieve step (gao2022precise,; ma2023query,; mackie2023generative,; mackie2023grm,; shen2023large,; jagerman2023query,; srinivasan2022quill,).
膨大なパラメトリックな基礎知識を活用することで、LLM（大規模言語モデル）はユーザーのクエリを理解し強化するため(=**rewriteプロセス...!**)の適切な選択となり、これにより検索ステップの関連性が向上します(gao2022precise,; ma2023query,; mackie2023generative,; mackie2023grm,; shen2023large,; jagerman2023query,; srinivasan2022quill,)。  

Our approach introduces a new data-centric RAG workflow, prepare-then-rewrite-then-retrieve-then-read (PR3), where each document is processed by LLMs to create both custom metadata tailored to users characteristics and QA pairs to unlock new knowledge base reasoning capabilities through query augmentation.
我々のアプローチは、**新しいデータ中心のRAGワークフロー、prepare-then-rewrite-then-retrieve-then-read（PR3）を導入**しており、各文書はLLMによって処理され、ユーザの特性に合わせたカスタムメタデータとQAペアを作成し、クエリ拡張を通じて新しい知識ベース推論能力を開放する。
(query augmentationの3つのプロセスの手前に、prepareが追加されてるってことか...!:thinking:)
Our data preparation and retrieval pipeline mitigates the information loss inherent to large document chunking and embedding, as only QA are being encoded instead of documents chunks, while acting as a noise filtering approach for both noisy and irrelevant documents for the task at hand.
我々のデータ準備と検索パイプラインは、文書チャンクの代わりにQAのみがエンコードされるため、大規模文書のチャンキングと埋め込みに特有の情報損失を軽減する。
By introducing metadata-based clusters of QAs and Meta Knowledge Summary, our framework conditionally augment the initial user query into multiple dedicated queries, therefore increasing the specificity, breadth, and depth of the knowledge base search (see Figure 1).
QAとメタ知識要約のメタデータベースのクラスタを導入することで、我々のフレームワークは条件付きで**最初のユーザークエリを複数の専用クエリに拡張**(rewriteプロセス)し、知識ベース検索の特異性、幅、深さを向上させる（図1参照）。
The proposed out-of-the-shelve methodology is easily applicable to new datasets, does not rely on manual data labelling or model fine-tuning, and constitutes a step towards autonomous, agent-based documents database reasoning with LLMs, for which the literature remains limited to date (zhu2023large,).
提案された即席(out-of-the-shelve)の方法論は、**新しいデータセットに簡単に適用でき、手動データラベリングやモデルの微調整に依存せず**、LLMを用いた自律エージェントベースの文書データベース推論に向けた一歩となっている（zhu2023large,）。

<!-- ここまで読んだ! -->

## Related Work 関連作品

Our work integrates concepts from methodologies that generate QA from document collections for downstream fine-tuning of either LLMs or encoder models, with techniques leveraging query augmentation to boost the performance of retrievers in RAG pipelines.
我々の研究は、LLMやエンコーダモデルを下流で微調整するために、文書コレクションからQAを生成する手法の概念と、RAGパイプラインの検索器の性能を向上させるためのクエリ拡張を活用する技術を統合している。
Below, we outline related work relevant to these two areas of RAG enhancement.
以下では、RAG強化のこれら2つの分野に関連する研究を概説する。

### RAG Enhancement with Fine-tuning 微調整によるRAGの強化

Methodologies that aim at improving RAG pipelines based on fine-tuning generally constitute a higher barrier to entry for performing both the initial parameters update, and the maintenance of the accuracy of the model over time to new documents.
ファインチューニングに基づいてRAGパイプラインを改善することを目的とする方法論は、一般的に、最初のパラメータ更新と、新しい文書に対する時間の経過に伴うモデルの精度維持の両方を実行するための、より高い参入障壁を構成する。
They require careful data cleaning and (often manual) curation, and manual iterations across training hyperparameters sets to successfully adapt the model to the task at hand without causing catastrophic forgetting of the pre-trained model knowledge (luo2023empirical,).
これらは、注意深いデータクリーニングと（しばしば手作業による）キュレーションを必要とし、事前に訓練されたモデル知識の壊滅的な忘却を引き起こすことなく、手元のタスクにモデルをうまく適応させるために、訓練ハイパーパラメータセット間で手作業による反復が必要である（luo2023empirical,)。
In addition, model tuning may not be sustainable for frequent knowledge-base updates, and represents a generally higher cost due the underlying requirements of compute resources, despite the recent development of parameter-efficient fine-tuning (PEFT) techniques (hu2021lora,; dettmers2024qlora,).
加えて、モデルのチューニングは、頻繁な知識ベースの更新のために持続可能でない可能性があり、パラメータ効率の良いファインチューニング（PEFT）技術が最近開発されたにもかかわらず、計算リソースの根本的な要件により、一般的に高いコストを意味する（hu2021lora,; dettmers2024qlora,)。

In e-commerce retrieval frameworks, TaoBao created a query rewriting framework based on company logs and rejection sampling to fine-tune a LLM in a supervised fashion, without QA generation.
電子商取引の検索フレームワークにおいて、TaoBaoは、QAを生成することなく、教師ありの方法でLLMを微調整するために、企業ログと拒絶サンプリングに基づいてクエリ書き換えフレームワークを作成した。
They further introduced a new contrastive learning methods to calibrate query generation probability to be aligned with desired search results, leading to a significant boost of merchandise volume, number of transactions and unique visitors (peng2024large,).
彼らはさらに、クエリ生成確率を望ましい検索結果に沿うように較正する新しい対照学習法を導入し、商品取扱高、取引件数、ユニークビジターを大幅に増加させた（peng2024large,)。
As an alternative, reinforcement learning methods based on black-box LLM evaluation has also been leveraged to train a smaller query-rewriter LLM, which showed a consistent performance improvement in open-domain and multiple-choice questions and answers (QA) in web search (ma2023query,).
その代替として、ブラックボックスLLM評価に基づく強化学習法も、より小さなクエリライタLLMを学習するために活用されており、ウェブ検索におけるオープンドメインと多肢選択式の質問と回答（QA）において一貫した性能向上を示した（ma2023query,)。
Reinforcement learning-based approaches, however, are subject to more instability during the training phase, and require a careful investigations of the trade-offs between generalization and specialization among downstream tasks (ma2023query,).
しかし、強化学習ベースのアプローチは、学習段階においてより不安定になりやすく、下流タスク間の汎化と特化のトレードオフを注意深く調査する必要がある（ma2023query,)。
Other approaches have focused on specifically improving the embedding space between the user query and the documents at hand, rather than augmenting the query itself.
他のアプローチでは、クエリそのものを拡張するのではなく、ユーザークエリと手元の文書との間の埋め込み空間を特に改善することに焦点が当てられている。
Authors of InPars (bonifacio2022inpars,) augmented their documents knowledge base by generating synthetic questions and answers pairs in a unsupervised fashion, and subsequently used them to fine-tune a T5 base embedding model.
InPars(bonifacio2022inpars,)の作者は、教師無しで合成質問と回答のペアを生成することによって文書知識ベースを増強し、その後、T5ベース埋め込みモデルを微調整するためにそれらを使用した。
They showed that using the fine-tuned embedding model followed by a neural reranker such as ColBERT (khattab2020colbert,) outperformed strong baselines such as BM25 (robertson2009probabilistic,).
彼らは、ColBERT(khattab2020colbert,)のようなニューラル・リランカーに続いて微調整された埋め込みモデルを使用することで、BM25(robertson2009probabilistic,)のような強力なベースラインを上回ることを示した。

Most recently, other types of approaches have been developed to improve the end-to-end pipeline performance, such as RAFT (zhang2024raft,), which consists in specifically training a reader to differentiate between relevant and irrelevant documents, or QUILL (srinivasan2022quill,) that aims at entirely replacing the RAG pipeline using RAG-augmented distillation training of another LLM.
例えば、RAFT（zhang2024raft,)は、関連文書と非関連文書を区別するために読者を特別に訓練するものであり、QUILL（srinivasan2022quill,)は、RAG-augmented distillation training of another LLMを用いてRAGパイプラインを完全に置き換えることを目的としている。

### RAG Enhancement without Fine-tuning 微調整なしのRAGエンハンスメント

As an alternative to fine-tuning LLMs or encoder models, query augmentation methodologies have been developed to increase the performance of the retrievers by transforming the user query pre-encoding.
LLMやエンコーダモデルを微調整する代わりに、ユーザクエリの事前エンコーディングを変換することで検索エンジンのパフォーマンスを向上させるクエリ拡張手法が開発されている。
These approaches can further be classified into two categories: either leveraging a retrieval pass through the documents, or zero-shot (without any example document).
これらのアプローチはさらに2つのカテゴリーに分類できる： ひとつは、文書を通過する検索を利用するもの、もうひとつは、ゼロショット（例となる文書なし）を利用するものである。

Among the zero-shot approaches, HyDE (gao2022precise,) introduced a data augmentation methodology that consists in generating an hypothetical response document to the user query by leveraging LLMs.
ゼロショット・アプローチの中で、HyDE（gao2022precise,)は、LLMを活用することで、ユーザーのクエリに対する仮説的な応答文書を生成するデータ増強手法を紹介した。
The underlying idea is to bring closer the user query and the documents of interest in the embedding space, therefore increasing the performance of the retrieval process.
基本的な考え方は、埋め込み空間において、ユーザーのクエリと関心のある文書を近づけることで、検索プロセスのパフォーマンスを向上させることである。
Their experiments showed performance comparable to fine-tuned retrievers across various tasks.
彼らの実験では、さまざまなタスクにおいて、微調整されたリトリーバーに匹敵する性能が示された。
The generated document, however, is a naïve data augmentation in the sense that it does not change given the underlying embedded data for the task at hand, such that it can lead to performance decrease in multiple situations, for there is inevitably a gap between the generated content and the knowledge base.
しかし、生成されたドキュメントは、手元のタスクのための基礎となる埋め込みデータが与えられても変化しないという意味で、ナイーブなデータ補強である。そのため、生成されたコンテンツと知識ベースとの間には必然的にギャップが生じるため、複数の状況でパフォーマンスの低下につながる可能性がある。
Alternatively, methodologies have been proposed to perform an initial pass through the embedding space of the documents first, and subsequently augment the initial query to perform a more informed search.
あるいは、文書の埋め込み空間を最初に通過させ、その後に最初のクエリを補強して、より情報に基づいた検索を行う方法も提案されている。
These Pseudo Relevance Feedback (PRF) (mackie2023generative,) and Generative Relevance Feedback (GRF) modeling approaches (mackie2023grm,) are typically dependent on the quality of the most highly-ranked documents used to first condition their query augmentation to, and are therefore prone to significant performance variation across queries, or may even forget the essence of the original query.
これらの擬似関連性フィードバック（PRF）（mackie2023generative,）や生成関連性フィードバック（GRF）モデリングアプローチ（mackie2023grm,）は、一般的に、クエリ拡張の最初の条件として使用される最も高ランクの文書の品質に依存しているため、クエリ間でパフォーマンスに大きなばらつきが生じやすく、元のクエリの本質を忘れてしまう可能性さえある。

## Methodology 方法論

In both RAG pipeline enhancements approaches cited above, the retrievers are generally unaware of the distribution of the target collection of documents despite an initial pass through the retrieval pipeline.
上記で引用したRAGパイプラインの拡張アプローチでは、検索パイプラインを最初に通過するにもかかわらず、検索者は一般的に対象文書のコレクションの分布を知らない。
In our proposed framework, for each document and prior to inference, we create a set of dedicated metadata, and subsequently generate guided QA spanning across the documents using Chain of Thoughts (CoT) prompting with Claude 3 Haiku (anthropic2024claude,; wei2022chain,).
我々の提案するフレームワークでは、各文書について、推論の前に、専用のメタデータのセットを作成し、その後、クロード3俳句（anthropic2024claude,; wei2022chain,）を用いたChain of Thoughts（CoT）プロンプトを用いて、文書にまたがるガイド付きQAを生成する。
The synthetic questions are then encoded, and the metadata used for filtering purposes.
その後、合成問題はエンコードされ、メタデータはフィルタリングの目的で使用される。
For any user-relevant combination of metadata, we create a Meta Knowledge Summary (MK Summary), leveraging Claude 3 Sonnet, which consists in a summarization of the key concepts available in the database for a given filter.
ユーザーに関連するメタデータの組み合わせに対して、クロード3ソネットを活用してメタ知識要約（MK要約）を作成する。
At inference time, the user query is dynamically augmented by relying on the personalized MK Summary given the metadata of interest, therefore providing tailored response for this user.
推論時に、ユーザーのクエリは、関心のあるメタデータを与えられたパーソナライズされたMK要約に依存することによって動的に拡張され、その結果、このユーザーに合わせた応答が提供される。
By doing so, we provide the retriever with the capability to reason across multiple documents which may have required multiple retrieval and reasoning rounds otherwise.
そうすることで、他の方法では何度も検索と推論を繰り返す必要があったかもしれない、複数の文書にまたがる推論を行う機能をリトリーバーに提供する。
Our goal is to ultimately increase the quality of the end-to-end retrieval pipeline across multiple metrics, such as depth, coverage, and relevancy, by enabling complex reasoning across the database through tailored searches and the leverage of meta knowledge information.
私たちの目標は、カスタマイズされた検索とメタ知識情報の活用により、データベース全体にわたる複雑な推論を可能にすることで、深さ、カバレッジ、関連性などの複数のメトリクスにわたって、最終的にエンドツーエンドの検索パイプラインの品質を向上させることである。
Importantly, our approach does not rely on any model weights update, and may very well be combined with any fine-tuning of either the language or the encoding models to any domain to further improve the performance of the end-to-end RAG pipeline (gupta2024rag,).
重要なことは、我々のアプローチはモデルの重みの更新に依存していないことである。そして、エンド・ツー・エンドのRAGパイプラインの性能をさらに向上させるために、言語モデルや符号化モデルをどのようなドメインでも微調整できるように組み合わせることができる（gupta2024rag,)。
We represent our methodology pipeline in Figure 1, and describe the synthetic QA generation process and the concept of MK Summary below.
以下に、合成QA生成プロセスとMK要約の概念について説明する。

### Datasets データセット

Our public benchmark use case comprises a dataset of 2,000 research papers from 2024, collated using the arXiv API.
私たちの公開ベンチマークのユースケースは、arXiv APIを使用して照合された2024年からの2,000の研究論文のデータセットで構成されています。
This dataset represents a diverse spectrum of research in statistics, machine learning, artificial intelligence, and econometrics1, for a total of approximately 35M tokens.
このデータセットは、統計学、機械学習、人工知能、計量経済学1 の多様な研究スペクトルを表しており、合計で約3500万トークンとなっている。

### Synthetic QA Generation 合成QA生成

First, for each document, we generate a set of metadata and subsequent QA using CoT prompting (see Appendix A).
まず、各文書について、CoTプロンプトを使用してメタデータとそれに続くQAのセットを生成する（付録A参照）。
The prompt aims at creating a list of metadata by classifying the documents into a predefined set of categories (such as research field, or applications types for our research papers benchmark).
このプロンプトは、文書をあらかじめ定義されたカテゴリー（研究分野や研究論文ベンチマークのアプリケーションの種類など）に分類し、メタデータのリストを作成することを目的としている。
Relying on these metadata, we generate a set of synthetic questions and answers, using teacher-student prompting and assess the knowledge of the student on the document.
これらのメタデータに基づき、教師と生徒のプロンプトを使用して合成質問と回答のセットを生成し、ドキュメントに関する生徒の知識を評価します。
We specifically leverage Claude 3 Haiku for its long-context reasoning abilities and potential to create synthetic QA pairs with context spanning across documents.
我々は特に、クロード3俳句の長い文脈推論能力と、文書にまたがる文脈を持つ合成QAペアを作成する可能性のために、クロード3俳句を活用する。
The generated metadata serve both as filtering parameters for the augmented search, and to select the synthetic QA used for the users queries augmentation in the form of meta knowledge information (MK Summary).
生成されたメタデータは、拡張検索のフィルタリングパラメータとして、また、メタ知識情報（MK要約）の形でユーザーのクエリ拡張に使用される合成QAを選択するために役立つ。
In addition, the synthetic QA are used for the retrieval, but only questions are vectorized for downstream retrieval.
また、検索には合成QAが使用されるが、下流の検索には質問のみがベクトル化される。
For our public scientific research papers use case, a total of 8657 QA were generated from the 2000 research documents, accounting for 5 to 6 questions for 70% of cases, and 2 questions in 21% of cases.
公開科学研究論文のユースケースでは、2000の研究文書から合計8657のQAが生成され、70％のケースで5～6問、21％のケースで2問のQAが生成された。
Examples of synthetic questions and answers are provided in Appendix B.
合成質問と回答の例は、付録Bに掲載されている。
The total number of token generated as parts of the processing step amount to approximately 8M output tokens, corresponding to a total of $20.17 for the entire processing pipeline of all 2000 documents (including input tokens) using Amazon Bedrock (pricingbedrock,).
処理ステップの一部として生成されたトークンの総数は、約8Mの出力トークンに相当し、Amazon Bedrock（pricingbedrock,）を使用した全2000ドキュメント（入力トークンを含む）の処理パイプラインの合計$20.17に相当する。
We investigated the redundancy of the generated QA across the document using hierarchical clustering on the embedding space of the questions using e5-mistral-7b-instruct (wang2023improving,), but did not de-duplicated the generated QA for our use cases due to the low QAs overlap.
e5-mistral-7b-instruct(wang2023improving,)を用いた質問の埋め込み空間に対する階層的クラスタリングを用いて、文書全体の生成QAの冗長性を調査したが、QAの重複が少ないため、我々のユースケースでは生成QAの重複除去は行わなかった。
QA Filtering can be application and metadata specific, and other high-dimensional approaches such as Determinantal Point Processes (DPP) (kulesza2012determinantal,) are left for future work, together with the automated discovery of metadata topics and self-correcting QA-generation (pan2023automatically,).
QAフィルタリングは、アプリケーションやメタデータに特化することができ、決定論的点過程（DPP）（kulesza2012determinantal,)のような他の高次元アプローチは、メタデータトピックの自動発見や自己修正QA生成（pan2023automatically,)と共に、将来の研究に残されている。

### Generation of Meta Knowledge Summary メタ知識要約の生成

For a given combination of metadata, we create a Meta Knowledge Summary (MK Summary) aiming at supporting the data augmentation phase for a given user query.
与えられたメタデータの組み合わせに対して、与えられたユーザークエリに対するデータ増強フェーズをサポートすることを目的としたメタ知識要約（MK要約）を作成する。
For our research papers use case, we limited our metadata to the specific field of research (such as reinforcement learning, supervised vs unsupervised learning, bayesian methods, econometrics, etc.) identified during the document processing phase by Claude 3 Haiku.
研究論文のユースケースでは、Claude 3 Haikuによる文書処理の段階で特定された特定の研究分野（強化学習、教師あり学習と教師なし学習、ベイジアン法、計量経済学など）にメタデータを限定した。
For this research, we create the MK Summary by summarizing the concepts across a set of questions tagged with the metadata of interest using Claude 3 Sonnet.
この研究では、クロード3ソネットを使用して、関心のあるメタデータでタグ付けされた一連の質問全体の概念を要約することにより、MKサマリーを作成する。
An alternative left for future work is that of prompt tuning to optimize for the content of the summary prompt (tam2022parameter,).
今後の課題として残されているのは、要約プロンプトの内容を最適化するためのプロンプトチューニングである（tam2022parameter,)。

### Augmented Generation of Queries and Retrieval クエリの拡張生成と検索

Given a user query and a set of pre-selected metadata of interests, we retrieve the corresponding pre-computed MK Summary and use it to condition the user query augmentation into the database subset.
ユーザークエリと、事前に選択された興味のあるメタデータのセットが与えられると、対応する事前に計算されたMKサマリーを取得し、データベースサブセットへのユーザークエリ拡張の条件付けに使用する。
For our research paper benchmark, we created a set of 20 MK Summary corresponding to research fields (e.g.deep learning for computer vision, statistical methods, bayesian analysis, etc.), relying on the metadata created in the processing phase.
研究論文のベンチマークでは、処理段階で作成されたメタデータに基づき、研究分野（コンピュータビジョンのディープラーニング、統計的手法、ベイジアン分析など）に対応する20のMKサマリーのセットを作成した。
We leverage the ”plan-and-execute” prompting methodology to address complex queries, reason across documents, and ultimately improve the recall, precision, and diversity of the provided answers (sun2023pearl,).
私たちは、複雑なクエリに対応し、ドキュメントを横断して推論し、最終的に提供された回答の再現性、精度、多様性を向上させるために、「計画と実行」のプロンプト手法を活用しています（sun2023pearl,)。
For example, for a user query related to the Reinforcement Learning research topic, the pipeline will first retrieve the meta knowledge (MK Summary) about Reinforcement Learning of the database, augment the user query into multiple sub queries based on the content of the MK Summary, and perform a parallel search in the filtered database relevant for manufacturing questions.
例えば、強化学習の研究トピックに関連するユーザークエリに対して、パイプラインはまずデータベースの強化学習に関するメタ知識（MK要約）を取得し、MK要約の内容に基づいてユーザークエリを複数のサブクエリに拡張し、製造に関する質問に関連するフィルタリングされたデータベースで並列検索を実行する。
For this purpose, the synthetic Questions are embedded, and replace the original documents chunk-based similarity matching, therefore mitigating the information loss due to document chunking discontinuity.
この目的のために、合成質問は埋め込まれ、元の文書のチャンクベースの類似性マッチングを置き換える。したがって、文書のチャンキングの不連続による情報損失を軽減する。
Once the best match of a synthetic question is found, the corresponding QA are retrieved, together with the original document title.
合成質問のベストマッチが見つかると、対応するQAが元の文書タイトルとともに検索される。
Only the document title, the synthetic question, and the answer are returned as a result of the retrieval.
検索結果として返されるのは、文書のタイトル、合成質問、答えのみである。
We use JSON formatting for downstream summarization performance.
JSONフォーマットを使用することで、下流の要約パフォーマンスを向上させている。
The final response of the RAG pipeline is obtained by providing the original query, the augmented queries, the retrieved context and few shot examples (see Figure 1).
RAGパイプラインの最終的なレスポンスは、元のクエリ、拡張されたクエリ、検索されたコンテキスト、およびいくつかのショット例を提供することによって得られる（図1を参照）。

## Evaluation

### Generating Evaluation Queries 評価クエリの生成

To evaluate our data-centric augmented retrieval pipeline, we generated 200 questions for the arXiv dataset using Claude 3 Sonnet (see Appendix C).
データ中心の拡張検索パイプラインを評価するために、クロード3ソネット（付録Cを参照）を使用して、arXivデータセットの200の質問を生成した。
In addition, we compared our methodology against traditional document chunking, query augmentation with document chunking, and naïve (not using MK Summary) augmentation with the QA processing of the documents.
さらに、従来の文書チャンキング、文書チャンキングを用いたクエリオーグメンテーション、ナイーブ（MK要約を用いない）オーグメンテーションと文書のQA処理との比較も行った。
As a comparison, we created documents chunks consisting of 256 tokens with 10% overlap.
比較として、10％の重複を持つ256個のトークンからなる文書チャンクを作成した。
For our use case, traditional chunking generated 69,334 documents chunks.
今回のユースケースでは、従来のチャンキングで69,334個の文書チャンクが生成された。

### Evaluation Metrics and Prompts 評価指標とプロンプト

Without relevance labels, we use Claude 3 Sonnet as a trusted evaluator (anthropic2024claude,) to compare the performance of all four benchmark methodologies considered: traditional chunking without any query augmentation, traditional document chunking with naive query augmentation, augmented search using our PR3 pipeline without MK Summary, and augmented search using our PR3 pipeline with MK Summary.
関連性ラベルなしで、Claude 3 Sonnetを信頼できる評価者(anthropic2024claude,)として使用し、4つのベンチマーク手法の性能を比較した： 従来のチャンキング（クエリ補強なし）、従来の文書チャンキング（素朴なクエリ補強あり）、PR3パイプライン（MK要約なし）、PR3パイプライン（MK要約あり）。
The query augmentation prompt is provided in Appendix D.
クエリ増強プロンプトは付録Dに記載されている。
We use the custom performance metrics defined below directly in the prompt to compare the results of both the retrieval model and the final response on a scale from 0 to 100.
以下に定義するカスタムパフォーマンスメトリクスをプロンプト内で直接使用し、検索モデルと最終的なレスポンスの結果を0から100までのスケールで比較する。
An example of Claude 3 Sonnet comparison answer is provided in Appendix E.
クロード3ソネットの比較解答例は付録Eに掲載されている。

- Recall: evaluates the coverage of key, highly relevant information contained in the retrieved documents リコール： 検索された文書に含まれる重要で関連性の高い情報の網羅性を評価する。

- Precision: evaluates the ratio of relevant documents against irrelevant ones 精度： 無関係な文書に対する関連文書の比率を評価する。

- Specificity: evaluates how precisely focused the final answer is on the query at hand, with clear and direct information that addresses the question 特異性： 最終的な回答が、質問に対応する明確で直接的な情報によって、どれだけ正確に手元のクエリに焦点を当てているかを評価する。

- Breadth: evaluates the coverage of all relevant aspects or areas related to the question, providing a complete overview 広さ： 設問に関連するすべての側面または分野をカバーし、完全な概要を提供しているかどうかを評価する。

- Depth: evaluates the extent to which the final answer provides a thorough understanding through detailed analysis and insights into the subject 深さ： 最終的な解答が、主題に関する詳細な分析と洞察を通じて、どの程度徹底した理解を提供しているかを評価する。

- Relevancy: evaluates how well-tailored the final answer is to the needs and interests of the audience or context, focusing on providing directly applicable and essential information while omitting extraneous details that do not contribute to addressing the specific question 関連性： 最終的な回答が、読者や文脈のニーズや関心にどの程度適合しているかを評価するもので、具体的な質問への対応に貢献しない余計な詳細は省き、直接適用できる重要な情報を提供することに重点を置く。

## Results 結果

We considered 4 cases for the evaluation of our retrieval pipeline: (1) traditional document chunking, without any augmentation, (2) traditional document chunking and augmentation, (3) QA-based search and retrieval, with naïve augmentation (our first proposal), and (4) QA-based search and retrieval, with the use of MK summary (our second proposal).
検索パイプラインの評価には4つのケースを考慮した： (1)オーグメンテーションなしの従来の文書チャンキング、(2)従来の文書チャンキングとオーグメンテーション、(3)ナイーブなオーグメンテーションを用いたQAベースの検索と検索（我々の第一の提案）、(4)MK要約を用いたQAベースの検索と検索（我々の第二の提案）。
For a single query, the computational latency of the end-to-end-pipeline amounts to  20-25 seconds.
一つのクエリに対して、エンド・ツー・エンドのパイプラインの計算待ち時間は20-25秒になる。

### Retrieval and End-to-end Evaluation Metrics 検索とエンド・ツー・エンドの評価指標

For each of the synthetic user queries generated, we ran a comparison prompt that includes the context retrieved as part of each approach, together with their final answers.
生成された各合成ユーザークエリに対して、各アプローチの一部として取得されたコンテキストと最終的な回答を含む比較プロンプトを実行した。
We prompted Claude 3 Sonnet to rate each of the metrics on a scale from 0 to 100, together with a justification text.
私たちは、クロード3ソネットに、それぞれの指標を0から100までの尺度で評価するよう促し、正当性を示す文章を添えた。
An example of the evaluation response is provided in Appendix E.
評価回答例は付録Eに記載されている。
The obtained metrics are then averaged across all queries and displayed below in Figure 2.
得られたメトリクスは、すべてのクエリで平均化され、以下の図2に表示されます。
We observe a clear benefit across all metrics but the precision of the retrieved documents by our two proposed QA-based methodologies.
我々は、提案する2つのQAに基づく方法論によって、検索された文書の精度を除く全ての指標において明確な利点があることを観察した。
The lack of strong improvement over the precision metric is consistent with the usage of a single encoding model and show that few documents are considered completely irrelevant.
精度の指標に対して強い改善が見られないことは、単一の符号化モデルを使用していることと一致しており、完全に無関係と考えられる文書がほとんどないことを示している。
Specifically, we note a significant performance boost in both the breadth and the depth of the final LLM response.
具体的には、最終的なLLM回答の幅と深さの両方において、パフォーマンスが大幅に向上した。
This result shows that the MK Summary is providing additional information that is leveraged by the query augmentation step.
この結果は、MKサマリーが、クエリー増強ステップで活用される追加情報を提供していることを示している。
Finally, the contribution of the MK summary to the conditioning of the search itself appears statistically significant across all metrics but the precision of the retriever (p<0.01 between the augmented QA search and the MK-Augmented QA search)(see Table 1).
最後に、検索自体のコンディショニングに対するMK要約の寄与は、検索精度を除くすべての指標において統計的に有意であった（増強QA検索とMK-増強QA検索の間でp<0.01）（表1参照）。
We observe that the the proposed methodology significantly improves the breadth of the search (by more than 20%, compared to traditional naïve search with chunking approaches), which aligns to the intuition that our proposal allows for effectively synthetizing more information from the content of the database, and leveraging its content more extensively.
これは、我々の提案がデータベースのコンテンツからより多くの情報を効果的に合成し、そのコンテンツをより広範囲に活用することを可能にするという直感に合致する。

Table 1.Performance benchmark across 200 Synthetic user queries
表1.200の合成ユーザークエリにおけるパフォーマンスベンチマーク

Figure 2.Summary of results obtained without any augmentation and with naïve document chunking, compared to results obtained using synthetic QA (proposal 1) and MK Summary (proposal 2).
図2.合成QA（提案1）とMK要約（提案2）を使った結果と比較した、オーグメンテーションなし、ナイーブな文書チャンキングを使った結果の要約。

## Conclusion and Discussion 結論と考察

We proposed a new data-centric RAG workflow which leverages synthetic QA generation instead of the traditional document chunking framework, and a query augmentation-based approach based on high level summary of the content metadata-based clusters of documents to improve the accuracy and quality of the end-to-end LLM augmentation pipeline.
我々は、従来の文書チャンキングフレームワークの代わりに合成QA生成を活用する新しいデータ中心のRAGワークフローと、エンドツーエンドのLLMオーグメンテーションパイプラインの精度と品質を向上させるために、文書のコンテンツメタデータベースのクラスタの高レベル要約に基づくクエリオーグメンテーションベースのアプローチを提案した。
Our methodology significantly outperforms traditional RAG pipelines relying on document chunking and naïve user query augmentation.
我々の方法論は、文書チャンキングとナイーブなユーザークエリ拡張に依存する従来のRAGパイプラインを大幅に凌駕する。
We introduced the concept of MK Summary to further boost the zero-shot search augmentation in the knowledge base, which subsequently increased the performance of the end-to-end RAG pipeline in our test case.
MKサマリーの概念を導入して、知識ベースにおけるゼロショット検索拡張をさらに強化し、テストケースにおけるエンドツーエンドのRAGパイプラインのパフォーマンスを向上させた。
In essence, our methodology improves on simple semantic matching information retrieval in the encoding vector space of the documents, where we allow for more diverse but highly relevant documents search, therefore providing more well-rounded, domain expert-level, and comprehensive answers to the user query.
要するに、我々の方法論は、文書の符号化ベクトル空間における単純な意味的マッチング情報検索を改善するものであり、より多様でありながら関連性の高い文書検索を可能にし、その結果、ユーザーのクエリに対して、より充実した、ドメイン専門家レベルの、包括的な回答を提供する。
On all metrics considered, recall, precision, specificity, breadth, depth, and relevancy, the proposed approach improved on state-of-the-art work.
リコール、精度、特異度、広さ、深さ、関連性など、考慮されたすべての指標において、提案されたアプローチは最先端の研究を上回った。
Finally, the approach is cost-effective, costing $20 for 2000 research papers.
最後に、このアプローチは費用対効果が高く、2000本の研究論文で20ドルである。
As a limitation, while we recognize the difficulty in crafting a set of metadata prior to document processing, the metadata generation can become an iterative approach to generate the metadata upon discovery.
制限として、文書処理の前にメタデータのセットを作成することの難しさは認識しているが、メタデータ生成は、発見時にメタデータを生成する反復的なアプローチになる可能性がある。
In addition, we left multi-hop iterative searches and improvement of the summary of the clustered knowledge base for future work.
さらに、マルチホップ反復検索と、クラスタ化された知識ベースの要約の改善は、今後の課題として残した。
