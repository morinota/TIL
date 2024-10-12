# How we built Text-to-SQL at Pinterest PinterestでText-to-SQLを構築した方法

Writing queries to solve analytical problems is the core task for Pinterest’s data users.
分析的な問題を解決するためにクエリを書くことは、Pinterestのデータユーザーにとって中心的な仕事である。
However, finding the right data and translating an analytical problem into correct and efficient SQL code can be challenging tasks in a fast-paced environment with significant amounts of data spread across different domains.
しかし、**多くのデータが異なるドメインに分散している高速な環境で、適切なデータを見つけ、分析的な問題を正確かつ効率的なSQLコードに変換することは、難しいタスク**である。

We took the rise in availability of Large Language Models (LLMs) as an opportunity to explore whether we could assist our data users with this task by developing a Text-to-SQL feature which transforms these analytical questions directly into code.
我々は、大規模言語モデル（LLM）の利用可能性が高まっていることを契機として、このような分析的な質問を直接コードに変換するText-to-SQL機能を開発することで、このタスクでデータユーザーを支援できないかを検討しました。

## How Text-to-SQL works at Pinterest PinterestにおけるText-to-SQLの仕組み

Most data analysis at Pinterest happens through Querybook, our in–house open source big data SQL query tool.
Pinterestのデータ分析のほとんどは、社内のオープンソースのビッグデータSQLクエリツールであるQuerybookを通じて行われます。
This tool is the natural place for us to develop and deploy new features to assist our data users, including Text-to-SQL.
このツールは、Text-to-SQLを含め、データユーザーを支援する新機能を開発し、展開するための自然な場所です。

## Implementing Text-to-SQL テキストをSQLに変換する

### The Initial Version: A Text-to-SQL Solution Using an LLM 初期バージョン LLMを使ったText-to-SQLソリューション

The first version incorporated a straightforward Text-to-SQL solution utilizing an LLM.
**最初のバージョンは、LLMを利用した簡単なText-to-SQLソリューション**でした。
Let’s take a closer look at its architecture:
そのアーキテクチャを詳しく見てみよう：

![]()

The user asks an analytical question, choosing the tables to be used.
ユーザは分析的な質問をし、**使用するテーブルを選択**する。(ここはユーザ自身が選ぶのか!)

- The relevant table schemas are retrieved from the table metadata store.
関連するテーブル・スキーマは、テーブル・メタデータ・ストアから取得される。

- The question, selected SQL dialect, and table schemas are compiled into a Text-to-SQL prompt.
質問、選択されたSQL方言(MySQLなど、SQLの文法を選択)、およびテーブルスキーマは、**Text-to-SQLプロンプトにコンパイルされます**。

- The prompt is fed into the LLM.
プロンプトはLLMに入力される。

- A streaming response is generated and displayed to the user.
ストリーミング・レスポンスが生成され、ユーザに表示される。

#### Table Schema テーブル・スキーマ

The table schema acquired from the metadata store includes:
メタデータ・ストアから取得したテーブル・スキーマには以下のものがある：

- Table name
テーブル名
- Table description
表の説明

- Columns
コラム

- Column name
カラム名

- Column type
カラムタイプ

- Column description
カラムの説明

#### Low-Cardinality Columns 低カーディナリティ・カラム

Certain analytical queries, such as “how many active users are on the ‘web’ platform”, may generate SQL queries that do not conform to the database’s actual values if generated naively.
例えば、「'web'プラットフォームにアクティブなユーザーが何人いるか」というような分析クエリは、単純に生成された場合、データベースの実際の値に準拠しないSQLクエリを生成するかもしれません。
For example, the where clause in the response might bewhere platform=’web’ as opposed to the correct where platform=’WEB’.
例えば、レスポンスのwhere節は、正しいwhere platform='WEB'に対して、where platform='web'になるかもしれません。
To address such issues, unique values of low-cardinality columns which would frequently be used for this kind of filtering are processed and incorporated into the table schema, so that the LLM can make use of this information to generate precise SQL queries.
このような問題に対処するため、**この種のフィルタリングに頻繁に使用される低カーディナリティ・カラムの一意の値が処理され、テーブル・スキーマに組み込まれる**ため、LLMはこの情報を利用して正確なSQLクエリを生成することができる。(LLMに渡すテーブルスキーマの中に、low-cardinalityカラムのユニーク値一覧を含めるのか...!:thinking:)

<!-- ここまで読んだ! -->

#### Context Window Limit コンテクスト・ウィンドウの制限

Extremely large table schemas might exceed the typical context window limit.
**非常に大きなテーブル・スキーマ**は、一般的なコンテキスト・ウィンドウの制限を超える可能性がある。(情報量がめちゃ多いテーブルだと、LLMが考慮可能なcontext長を超える可能性がある)
To address this problem, we employed a few techniques:
この問題に対処するため、我々はいくつかのテクニックを採用した：

- Reduced version of the table schema: This includes only crucial elements such as the table name, column name, and type.
**テーブルスキーマの縮小版**： テーブル名、カラム名、型などの重要な要素のみを含む。

- Column pruning: Columns are tagged in the metadata store, and we exclude certain ones from the table schema based on their tags.
カラムの刈り込み： カラムはメタデータストアでタグ付けされ、そのタグに基づいてテーブルスキーマから特定のカラムを除外する。
(使わなさそうなカラムを除外するってこと...??:thinking:)

### Response Streaming レスポンス・ストリーミング

A full response from an LLM can take tens of seconds, so to avoid users having to wait, we employed WebSocket to stream the response.
LLMからの完全なレスポンスには数十秒かかるので、**ユーザを待たせないために、WebSocketを使用してレスポンスをストリーミングする。**
Given the requirement to return varied information besides the generated SQL, a properly structured response format is crucial.
生成されたSQL以外に様々な情報を返す必要があることを考えると、**適切に構造化されたレスポンス・フォーマットは非常に重要**である。
Although plain text is straightforward to stream, streaming JSON can be more complex.
プレーン・テキストのストリーミングは簡単だが、JSONのストリーミングはより複雑になる。
We adopted Langchain’s partial JSON parsing for the streaming on our server, and then the parsed JSON will be sent back to the client through WebSocket.
サーバーでのストリーミングには**Langchainのpartial JSON parsingを採用**し、その後、パースされたJSONはWebSocketを介してクライアントに送信される。

<!-- ここまで読んだ! -->

### Prompt プロンプト

Here is the current prompt we’re using for Text2SQL:
これが現在Text2SQLで使用しているプロンプトです：

---

You are a {dialect} expert.

Please help to generate a {dialect} query to answer the question. Your response
should ONLY be based on the given context and follow the response guidelines and
format instructions.

===Tables
{table_schemas}

===Original Query
{original_query}

===Response Guidelines

1. If the provided context is sufficient, please generate a valid query without any
   explanations for the question. The query should start with a comment containing the
   question being asked.
2. If the provided context is insufficient, please explain why it can't be
   generated.
3. Please use the most relevant table(s).
5. Please format the query before responding.
6. Please always respond with a valid well-formed JSON object with the following
   format

===Response Format
{{
   "query": "A generated SQL query when context is sufficient.",
   "explanation": "An explanation of failing to generate the query."
}}

===Question
{question}

---

### Evaluation & Learnings 評価と教訓

Our initial evaluations of Text-to-SQL performance were mostly conducted to ensure that our implementation had comparable performance with results reported in the literature, given that the implementation mostly used off-the-shelf approaches.
Text-to-SQLの性能に関する初期の評価は、**実装のほとんどが既製のアプローチを使用**していることから、我々の実装が文献で報告されている結果と同等の性能を持つことを確認するために行われました。
We found comparable results to those reported elsewhere on the Spider dataset, although we noted that the tasks in this benchmark were substantially easier than the problems our users face, in particular that it considers a small number of pre-specified tables with few and well-labeled columns.
Spiderデータセットに関しては、他の場所で報告されている結果と同等の結果を見つけましたが、このベンチマークのタスクは、特に事前に指定された少数のテーブルと少数でよくラベル付けされたカラムを考慮しているため、ユーザーが直面する問題よりもはるかに簡単であることに注意しました。

Once our Text-to-SQL solution was in production, we were also able to observe how users interacted with the system.
Text-to-SQLソリューションが本番稼動してからは、ユーザがどのようにシステムとやりとりしているかも観察することができました。
As our implementation improved and as users became more familiar with the feature, our first-shot acceptance rate for the generated SQL increased from 20% to above 40%.
実装が改善され、ユーザがこの機能に慣れてくるにつれて、**生成されたSQLの初回受け入れ率は20％から40％以上に上昇**しました。
In practice, most queries that are generated require multiple iterations of human or AI generation before being finalized.
**実際には、生成されたクエリのほとんどは、最終的なクエリになるまで、人間やAIによる生成を何度も繰り返す必要がある**。
In order to determine how Text-to-SQL affected data user productivity, the most reliable method would have been to experiment.
Text-to-SQLがデータユーザーの生産性にどのような影響を与えるかを判断するためには、最も確実な方法は実験することであっただろう。
Using such a method, previous research has found that AI assistance improved task completion speed by over 50%.
このような方法を用いた先行研究では、**AIの支援によってタスク完了速度が50％以上向上した**ことが判明している。
In our real world data (which importantly does not control for differences in tasks), we find a 35% improvement in task completion speed for writing SQL queries using AI assistance.
我々の実世界のデータ（重要なのはタスクの違いをコントロールしていない）では、AIの支援を利用して**SQLクエリを書くタスクの完了速度が35％向上**している。
(firstバージョンでさえ35%向上! いいね! でも2倍良くなると思いたい!:thinking:)

<!-- ここまで読んだ! -->

## Second Iteration: Incorporating RAG for Table Selection 第二の反復： テーブル選択にRAGを組み込む

While the first version performed decently — assuming the user is aware of the tables to be employed — identifying the correct tables amongst the hundreds of thousands in our data warehouse is actually a significant challenge for users.
**最初のバージョンは、ユーザが使用するテーブルを把握していると仮定すれば、まずまずの性能を発揮しましたが**、データウェアハウスに数十万のテーブルがある中から正しいテーブルを特定することは、**実際にはユーザにとってかなりの課題**です。(うんうん...!:thinking:)
To mitigate this, we integrated Retrieval Augmented Generation (RAG) to guide users in selecting the right tables for their tasks.
これを軽減するために、我々は**RAG(Retrieval Augmented Generation)を統合し、ユーザのタスクに適したテーブルの選択をガイドするようにした**。(RAGを使わないとガイドできない??:thinking:)
Here’s a review of the refined infrastructure incorporating RAG:
ここでは、RAGを組み込んだ洗練されたインフラについてレビューする:

![]()

- 1. An offline job is employed to generate a vector index of tables’ summaries and historical queries against them.
オフラインジョブ は、**テーブルのサマリーとそれらに対する過去のクエリのベクトルインデックスを生成**するために使用される。
(ここで、クエリはそのまま埋め込む? もしくは自然言語に変換してから埋め込みにする??:thinking:)

- 2. If the user does not specify any tables, their question is transformed into embeddings, and a similarity search is conducted against the vector index to infer the top N suitable tables.
ユーザがテーブルを指定しない場合、彼らの**質問は埋め込みに変換**され、ベクトルインデックスに対して類似性検索が行われ、**上位N個の適切なテーブルが推測**される。(RAGチックだ...!:thinking:)

- 3. The top N tables, along with the table schema and analytical question, are compiled into a prompt for LLM to select the top K most relevant tables.
上位N個のテーブルは、テーブルスキーマと分析的なクエリとともに、LLMが最も関連性の高い上位K個のテーブルを選択するための**プロンプトにコンパイル**される。

- 4. The top K tables are returned to the user for validation or alteration.
トップKのテーブルは、検証または変更のためにユーザに返される。

- 5. The standard Text-to-SQL process is resumed with the user-confirmed tables.
ユーザが確認したテーブルで、標準のText-to-SQLプロセスが再開される。(ここからfirstバージョンの手順が続く??)

### Offline Vector Index Creation オフライン・ベクトル・インデックスの作成

There are two types of document embeddings in the vector index:
ベクトルインデックスには**2種類の文書埋め込み**がある：
(うんうん:thinking:)

- Table summarization
表の要約

- Query summarization
クエリの要約

### Table Summarization 表の要約

There is an ongoing table standardization effort at Pinterest to add tiering for the tables.
Pinterestでは、テーブルに階層化(Tier)を追加するためのテーブル標準化の取り組みが進行中である。
We index only top-tier tables, promoting the use of these higher-quality datasets.
**トップtierのテーブルのみにインデックスを付け**、より質の高いデータセットの利用を促進している。(品質が低くて使ってほしくないテーブルとかを除外するってことかな:thinking:)
The table summarization generation process involves the following steps:
表の要約生成プロセスには以下のステップがある：

- 1. Retrieve the table schema from the table metadata store.
テーブル・メタデータ・ストアからテーブル・スキーマを取得する。

- 2. Gather the most recent sample queries utilizing the table.
テーブルを利用した最新のサンプルクエリを収集する。

- 3. Based on the context window, incorporate as many sample queries as possible into the table summarization prompt, along with the table schema.
コンテキストウィンドウに基づいて、**テーブルスキーマとともに、できるだけ多くのサンプルクエリ**をテーブルの要約プロンプトに組み込む。
(サンプルクエリもtable summaryを作るために渡すの:thinking:)
(コンテキストウィンドウは各モデルによって異なるのか:thinking:)

- 4. Forward the prompt to the LLM to create the summary.
プロンプトをLLMに転送し、**要約を作成**する。

- 5. Generate and store embeddings in the vector store.
埋め込みを生成し、ベクトルストアに保存する。(summaryを埋め込む)

The table summary includes description of the table, the data it contains, as well as potential use scenarios.
表サマリーには、表の説明、含まれるデータ、潜在的な使用シナリオが含まれる。
Here is the current prompt we are using for table summarization:
現在、表の要約に使用しているプロンプトはこちら：

---

You are a data analyst that can help summarize SQL tables.

Summarize below table by the given context.

===Table Schema
{table_schema}

===Sample Queries
{sample_queries}

===Response guideline

- You shall write the summary based only on provided information.
- Note that above sampled queries are only small sample of queries and thus not all
  possible use of tables are represented, and only some columns in the table are used.
- Do not use any adjective to describe the table. For example, the importance of
  the table, its comprehensiveness or if it is crucial, or who may be using it. For
  example, you can say that a table contains certain types of data, but you cannot say
  that the table contains a 'wealth' of data, or that it is 'comprehensive'.
- Do not mention about the sampled query. Only talk objectively about the type of
  data the table contains and its possible utilities.
- Please also include some potential usecases of the table, e.g. what kind of
  questions can be answered by the table, what kind of analysis can be done by the
  table, etc.

---

### Query Summarization クエリの要約

Besides their role in table summarization, sample queries associated with each table are also summarized individually, including details such as the query’s purpose and utilized tables.
表の要約における役割に加えて、**各テーブルに関連付けられたサンプルクエリも個別に要約**され、クエリの目的や使用されたテーブルなどの詳細が含まれる。
Here is the prompt we are using:
これが、私たちが使っているプロンプトです：
(summarize対象のクエリ + クエリ内で使われているテーブルスキーマを渡す:thinking:)

---
You are a helpful assistant that can help document SQL queries.
あなたはSQLクエリを文書化するのに役立つアシスタントです。

Please document below SQL query by the given table schemas.
以下のSQLクエリを、与えられたテーブルスキーマによって文書化してください。

===SQL Query
{query}

===Table Schemas
{table_schemas}

===Response Guidelines
Please provide the following list of descriptions for the query:

- The selected columns and their description
- The input tables of the query and the join pattern
- Query's detailed transformation logic in plain english, and why these
  transformation are necessary
- The type of filters performed by the query, and why these filters are necessary
- Write very detailed purposes and motives of the query in detail
- Write possible business and functional purposes of the query

---

<!-- ここまで読んだ! -->

### NLP Table Search NLP テーブル検索

When a user asks an analytical question, we convert it into embeddings using the same embedding model.
ユーザが分析的な質問をすると、**同じ埋め込みモデルを使用して埋め込みに変換**する。(RAGの前半のステップだ:thinking:)
Then we conduct a search against both table and query vector indices.
次に、テーブルとクエリーベクトルの両方のインデックスに対して検索を行う。
We’re using OpenSearch as the vector store and using its built in similarity search ability.
**我々はベクターストアとしてOpenSearchを使用**しており、その組み込みの類似検索機能を使用している。

Considering that multiple tables can be associated with a query, a single table could appear multiple times in the similarity search results.
複数のテーブルがクエリに関連付けられる可能性があるため、**単一のテーブルが類似性検索結果に複数回表示されることがあります**。(なんでかよくわかってない:thinking:)
Currently, we utilize a simplified strategy to aggregate and score them.
現在は、それらを集約してスコアリングするための簡略化された戦略を利用している。
Table summaries carry more weight than query summaries, a scoring strategy that could be adjusted in the future.
**テーブルサマリはクエリサマリよりも重要視され**、将来調整される可能性のあるスコアリング戦略である。

Other than being used in the Text-to-SQL, this NLP-based table search is also used in the general table search in Querybook.
Text-to-SQLで使用されるだけでなく、このNLPベースのテーブル検索は、Querybookの一般的なテーブル検索にも使用されています。

<!-- ここまで読んだ! -->

### Table Re-selection テーブルの再選択

(質問に利用できそうなテーブルk個を選ぶステップ!)

Upon retrieving the top N tables from the vector index, we engage an LLM to choose the most relevant K tables by evaluating the question alongside the table summaries.
ベクトルインデックスから上位N個のテーブルを検索すると、LLMがテーブルの要約とともに質問を評価し、最も関連性の高いK個のテーブルを選択する。
Depending on the context window, we include as many tables as possible in the prompt.
コンテクストウィンドウによって、プロンプトにできるだけ多くのテーブルを含める。
Here is the prompt we’re using for the table re-selection:
以下は、テーブルの再選択に使用するプロンプトである：

---

You are a data scientist that can help select the most relevant tables for SQL query tasks.

Please select the most relevant table(s) that can be used to generate SQL query for the question.

===Response Guidelines

- Only return the most relevant table(s).
- Return at most {top_n} tables.
- Response should be a valid JSON array of table names which can be parsed by Python
  json.loads(). For a single table, the format should be ["table_name"].

===Tables
{table_schemas}

===Question
{question}

---

Once the tables are re-selected, they are returned to the user for validation before transitioning to the actual SQL generation stage.
テーブルが再選択されると、実際のSQL生成段階に移行する前に、ユーザに返されて検証される。

### Evaluation & Learnings 評価と教訓

We evaluated the table retrieval component of our Text-to-SQL feature using offline data from previous table searches.
我々は、過去のテーブル検索のオフラインデータを使用して、Text-to-SQL機能の**テーブル検索コンポーネント**(=secondバージョンで追加されたやつ...!)を評価した。
This data was insufficient in one important respect: it captured user behavior before they knew that NLP-based search was available.
このデータは、1つの重要な点で不十分であった：NLPベースの検索が利用可能であることを知る前のユーザの行動を捉えていた。
(オフラインデータを使うから、どうしても実際の運用時の性能を完璧には推定できないよ、ってことっぽい:thinking:)
Therefore, this data was used mostly to ensure that the embedding-based table search did not perform worse than the existing text-based search, rather than attempting to measure improvement.
したがって、このデータは、改善を測定するためというよりも、**埋め込みベースのテーブル検索が既存のテキストベースの検索よりもパフォーマンスが悪くないことを確認するため**に主に使用された。(あくまでも健康診断だ、という認識を持ってるのが素敵だ...!:thinking:)
We used this evaluation to select a method and set weights for the embeddings used in table retrieval.
この評価を用いて、テーブル検索に使用する埋め込み方法の選択と重みの設定を行った。(ハイパーパラメータ調整はオフライン評価で...!:thinking:)
This approach revealed to us that the table metadata generated through our data governance efforts was of significant importance to overall performance: the search hit rate without table documentation in the embeddings was 40%, but performance increased linearly with the weight placed on table documentation up to 90%.
このアプローチにより、データガバナンスの取り組みを通じて生成された**テーブルメタデータが全体的なパフォーマンスに重要である**ことが明らかになった：埋め込みにテーブルのドキュメントがない場合の検索ヒット率は40％だったが、テーブルのドキュメントに置かれた重みが90％まで増加すると、パフォーマンスが線形に向上した。
(データカタログの充実が重要だったってことか...!:thinking:)

<!-- ここまで読んだ! -->

## Next Steps 次のステップ

While our currently-implemented Text-to-SQL has significantly enhanced our data analysts’ productivity, there is room for improvements.
現在実装しているText-to-SQLは、データアナリストの生産性を大幅に向上させていますが、改善の余地はあります。
Here are some potential areas of further development:
さらなる発展の可能性がある分野をいくつか挙げてみよう：

### NLP Table Search NLP テーブル検索

#### Metadata Enhancement メタデータの強化

Currently, our vector index only associates with the table summary.
現在、我々のベクター・インデックスはテーブル・サマリーとしか関連付けられない。(あれ、クエリサマリもじゃない??:thinking:)
One potential improvement could be the inclusion of further metadata such as tiering, tags, domains, etc., for more refined filtering during the retrieval of similar tables.
より洗練されたテーブルの類似性検索中のフィルタリングのために、ティアリング、タグ、ドメインなどの追加のメタデータを含めることができる。

#### Scheduled or Real-Time Index Update インデックスのスケジュール更新またはリアルタイム更新

Currently the vector index is generated manually.
現在、ベクトルインデックスは手動で生成されている。
Implementing scheduled or even real-time updates whenever new tables are created or queries executed would enhance system efficiency.
新しいテーブルが作成されたり、クエリーが実行されたりするたびに、スケジュールされた、あるいはリアルタイムのアップデートを実装することで、システムの効率を高めることができる。

#### Similarity Search and Scoring Strategy Revision 類似性検索と採点戦略の見直し

Our current scoring strategy to aggregate the similarity search results is rather basic.
類似検索結果を集約するための現在のスコアリング戦略は、かなり基本的なものだ。
Fine-tuning this aspect could improve the relevance of retrieved results.
この点を微調整することで、検索結果の関連性を向上させることができる。

### Query validation クエリ検証

At present, the SQL query generated by the LLM is directly returned to the user without validation, leaving a potential risk that the query may not run as expected.
現在のところ、LLMによって生成されたSQLクエリは、検証されることなく直接ユーザに返されるため、クエリが期待通りに実行されない可能性がある。
Implementing query validation, perhaps using a constrained beam search, could provide an extra layer of assurance.
制約付きビームサーチを使用してクエリ検証を実装することで、追加の保証を提供できるかもしれない。

### User feedback ユーザーからのフィードバック

Introducing a user interface to efficiently collect user feedback on the table search and query generation results could offer valuable insights for improvements.
テーブル検索とクエリ生成結果に対するユーザーのフィードバックを効率的に収集するためのユーザーインターフェイスを導入することで、改善のための貴重な洞察が得られる可能性がある。
Such feedback could be processed and incorporated into the vector index or table metadata store, ultimately boosting system performance.
このようなフィードバックは処理され、ベクトル・インデックスやテーブル・メタデータ・ストアに組み込まれ、最終的にシステム・パフォーマンスを向上させることができる。

### Evaluation 評価

While working on this project, we realized that the performance of text-to-SQL in a real world setting is significantly different to that in existing benchmarks, which tend to use a small number of well-normalized tables (which are also prespecified).
このプロジェクトに取り組んでいる間に、**実世界の環境でのText-to-SQLの性能は**、一般的には少数のよく正規化されたテーブル（または事前に指定されたテーブル）を使用する**既存のベンチマークとは大きく異なる**ことに気づきました。
It would be helpful for applied researchers to produce more realistic benchmarks which include a larger amount of denormalized tables and treat table search as a core part of the problem.
より多くの非正規化テーブルを含む、より現実的なベンチマークを作成し、テーブル検索を問題の中核部分として扱うことは、応用研究者にとって有益であろう。

To learn more about engineering at Pinterest, check out the rest of our Engineering Blog and visit our Pinterest Labs site.
Pinterestのエンジニアリングについてもっと知りたい方は、エンジニアリングブログの他の部分をチェックし、Pinterest Labsサイトをご覧ください。
To explore and apply to open roles, visit our Careers page.
募集職種を検索して応募するには、採用ページをご覧ください。

<!-- ここまで読んだ! -->
