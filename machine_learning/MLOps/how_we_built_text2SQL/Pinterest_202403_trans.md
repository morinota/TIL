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
最初のバージョンは、LLMを利用した簡単なText-to-SQLソリューションでした。
Let’s take a closer look at its architecture:
そのアーキテクチャを詳しく見てみよう：

The user asks an analytical question, choosing the tables to be used.
ユーザーは分析的な質問をし、使用するテーブルを選択する。

The relevant table schemas are retrieved from the table metadata store.
関連するテーブル・スキーマは、テーブル・メタデータ・ストアから取得される。

The question, selected SQL dialect, and table schemas are compiled into a Text-to-SQL prompt.
質問、選択されたSQL方言、およびテーブルスキーマは、Text-to-SQLプロンプトにコンパイルされます。

The prompt is fed into the LLM.
プロンプトはLLMに入力される。

A streaming response is generated and displayed to the user.
ストリーミング・レスポンスが生成され、ユーザーに表示される。

Table Schema
テーブル・スキーマ

The table schema acquired from the metadata store includes:
メタデータ・ストアから取得したテーブル・スキーマには以下のものがある：

Table name
テーブル名

Table description
表の説明

Columns
コラム

Column name
カラム名

Column type
カラムタイプ

Column description
カラムの説明

Low-Cardinality Columns
低基数列

Certain analytical queries, such as “how many active users are on the ‘web’ platform”, may generate SQL queries that do not conform to the database’s actual values if generated naively.
例えば、「「web 」プラットフォーム上のアクティブユーザー数」のような特定の分析クエリは、素朴に生成された場合、データベースの実際の値に適合しないSQLクエリを生成する可能性がある。
For example, the where clause in the response might bewhere platform=’web’ as opposed to the correct where platform=’WEB’.
例えば、レスポンスのwhere節は、正しいwhere platform='WEB'に対して、where platform='WEB'かもしれません。
To address such issues, unique values of low-cardinality columns which would frequently be used for this kind of filtering are processed and incorporated into the table schema, so that the LLM can make use of this information to generate precise SQL queries.
このような問題に対処するため、この種のフィルタリングに頻繁に使われるような、カーディナリティの低いカラムのユニークな値を処理してテーブルスキーマに組み込み、LLMがこの情報を利用して正確なSQLクエリを生成できるようにする。

Context Window Limit
コンテクスト・ウィンドウの制限

Extremely large table schemas might exceed the typical context window limit.
非常に大きなテーブル・スキーマは、一般的なコンテキスト・ウィンドウの制限を超える可能性がある。
To address this problem, we employed a few techniques:
この問題に対処するため、我々はいくつかのテクニックを採用した：

Reduced version of the table schema: This includes only crucial elements such as the table name, column name, and type.
テーブルスキーマの縮小版： テーブル名、カラム名、型などの重要な要素のみを含む。

Column pruning: Columns are tagged in the metadata store, and we exclude certain ones from the table schema based on their tags.
カラムの刈り込み： カラムはメタデータストアでタグ付けされ、そのタグに基づいてテーブルスキーマから特定のカラムを除外する。

### Response Streaming レスポンス・ストリーミング

A full response from an LLM can take tens of seconds, so to avoid users having to wait, we employed WebSocket to stream the response.
LLMからの完全なレスポンスには数十秒かかるので、ユーザーを待たせないために、レスポンスをストリーミングするためにWebSocketを採用した。
Given the requirement to return varied information besides the generated SQL, a properly structured response format is crucial.
生成されたSQL以外に様々な情報を返す必要があることを考えると、適切に構造化されたレスポンス・フォーマットは非常に重要である。
Although plain text is straightforward to stream, streaming JSON can be more complex.
プレーン・テキストのストリーミングは簡単だが、JSONのストリーミングはより複雑になる。
We adopted Langchain’s partial JSON parsing for the streaming on our server, and then the parsed JSON will be sent back to the client through WebSocket.
サーバーでのストリーミングにはLangchainの部分的JSONパースを採用し、パースされたJSONはWebSocketを通じてクライアントに送り返される。

### Prompt プロンプト

Here is the current prompt we’re using for Text2SQL:
これが現在Text2SQLで使用しているプロンプトです：

### Evaluation & Learnings 評価と教訓

Our initial evaluations of Text-to-SQL performance were mostly conducted to ensure that our implementation had comparable performance with results reported in the literature, given that the implementation mostly used off-the-shelf approaches.
Text-to-SQLの性能に関する初期の評価は、実装のほとんどが既製のアプローチを使用していることから、我々の実装が文献で報告されている結果と同等の性能を持つことを確認するために行われました。
We found comparable results to those reported elsewhere on the Spider dataset, although we noted that the tasks in this benchmark were substantially easier than the problems our users face, in particular that it considers a small number of pre-specified tables with few and well-labeled columns.
我々は、Spiderデータセットの他の場所で報告されている結果と同等の結果を得たが、このベンチマークのタスクは、我々のユーザーが直面している問題よりもかなり簡単であることに注意した。

Once our Text-to-SQL solution was in production, we were also able to observe how users interacted with the system.
Text-to-SQLソリューションが本番稼動してからは、ユーザーがどのようにシステムとやりとりしているかも観察することができました。
As our implementation improved and as users became more familiar with the feature, our first-shot acceptance rate for the generated SQL increased from 20% to above 40%.
実装が改善され、ユーザーがこの機能に慣れるにつれて、生成されたSQLの一発合格率は20％から40％以上に上昇した。
In practice, most queries that are generated require multiple iterations of human or AI generation before being finalized.
実際には、生成されたクエリのほとんどは、最終的なクエリになるまで、人間やAIによる生成を何度も繰り返す必要がある。
In order to determine how Text-to-SQL affected data user productivity, the most reliable method would have been to experiment.
Text-to-SQLがデータユーザーの生産性にどのような影響を与えるかを判断するためには、最も確実な方法は実験することであっただろう。
Using such a method, previous research has found that AI assistance improved task completion speed by over 50%.
このような方法を用いた先行研究では、AIの支援によってタスク完了速度が50％以上向上したことが判明している。
In our real world data (which importantly does not control for differences in tasks), we find a 35% improvement in task completion speed for writing SQL queries using AI assistance.
我々の実世界のデータ（重要なことは、タスクの違いを制御していない）では、AIの支援を使用してSQLクエリを記述する場合、タスク完了速度が35％向上することがわかった。

## Second Iteration: Incorporating RAG for Table Selection 第二の反復： テーブル選択にRAGを組み込む

While the first version performed decently — assuming the user is aware of the tables to be employed — identifying the correct tables amongst the hundreds of thousands in our data warehouse is actually a significant challenge for users.
最初のバージョンは、ユーザーが使用するテーブルを認識していることを前提に、まずまずのパフォーマンスを示したが、データウェアハウスにある数十万のテーブルの中から正しいテーブルを特定することは、ユーザーにとって大きな課題であった。
To mitigate this, we integrated Retrieval Augmented Generation (RAG) to guide users in selecting the right tables for their tasks.
これを軽減するために、我々はRAG(Retrieval Augmented Generation)を統合し、ユーザーのタスクに適したテーブルの選択をガイドするようにした。
Here’s a review of the refined infrastructure incorporating RAG:
ここでは、RAGを組み込んだ洗練されたインフラについてレビューする：

An offline job is employed to generate a vector index of tables’ summaries and historical queries against them.
オフラインジョブは、テーブルのサマリーとそれらに対する過去のクエリのベクトルインデックスを生成するために使用される。

If the user does not specify any tables, their question is transformed into embeddings, and a similarity search is conducted against the vector index to infer the top N suitable tables.
ユーザーがテーブルを指定しなかった場合、質問は埋め込みに変換され、上位N個の適切なテーブルを推測するためにベクトルインデックスに対して類似性検索が行われる。

The top N tables, along with the table schema and analytical question, are compiled into a prompt for LLM to select the top K most relevant tables.
上位N個のテーブルは、テーブルスキーマと分析問題とともに、LLMが最も関連性の高い上位K個のテーブルを選択するためのプロンプトにまとめられる。

The top K tables are returned to the user for validation or alteration.
トップKのテーブルは、検証または変更のためにユーザーに返される。

The standard Text-to-SQL process is resumed with the user-confirmed tables.
標準のText-to-SQL処理は、ユーザーが確認したテーブルで再開される。

### Offline Vector Index Creation オフライン・ベクトル・インデックスの作成

There are two types of document embeddings in the vector index:
ベクトルインデックスには2種類の文書埋め込みがある：

Table summarization
表の要約

Query summarization
クエリの要約

### Table Summarization 表の要約

There is an ongoing table standardization effort at Pinterest to add tiering for the tables.
Pinterestでは、テーブルの階層化を追加するために、テーブルの標準化を進めている。
We index only top-tier tables, promoting the use of these higher-quality datasets.
トップクラスのテーブルのみにインデックスを付け、より質の高いデータセットの利用を促進している。
The table summarization generation process involves the following steps:
表の要約生成プロセスには以下のステップがある：

Retrieve the table schema from the table metadata store.
テーブル・メタデータ・ストアからテーブル・スキーマを取得する。

Gather the most recent sample queries utilizing the table.
テーブルを利用した最新のサンプルクエリを収集する。

Based on the context window, incorporate as many sample queries as possible into the table summarization prompt, along with the table schema.
コンテキスト・ウィンドウに基づき、テーブル・スキーマとともに、できるだけ多くのサンプル・クエリをテーブル要約プロンプトに組み込みます。

Forward the prompt to the LLM to create the summary.
プロンプトをLLMに転送し、要約を作成する。

Generate and store embeddings in the vector store.
埋め込みを生成し、ベクトルストアに保存する。

The table summary includes description of the table, the data it contains, as well as potential use scenarios.
表サマリーには、表の説明、含まれるデータ、潜在的な使用シナリオが含まれる。
Here is the current prompt we are using for table summarization:
現在、表の要約に使用しているプロンプトはこちら：

### Query Summarization クエリの要約

Besides their role in table summarization, sample queries associated with each table are also summarized individually, including details such as the query’s purpose and utilized tables.
テーブルを要約する役割の他に、各テーブルに関連するサンプルクエリも個別に要約されており、クエリの目的や利用したテーブルなどの詳細が含まれている。
Here is the prompt we are using:
これが、私たちが使っているプロンプトです：

### NLP Table Search NLP テーブル検索

When a user asks an analytical question, we convert it into embeddings using the same embedding model.
ユーザーが分析的な質問をすると、同じ埋め込みモデルを使って埋め込みに変換する。
Then we conduct a search against both table and query vector indices.
次に、テーブルとクエリーベクトルの両方のインデックスに対して検索を行う。
We’re using OpenSearch as the vector store and using its built in similarity search ability.
我々はベクターストアとしてOpenSearchを使用しており、その組み込みの類似検索機能を使用している。

Considering that multiple tables can be associated with a query, a single table could appear multiple times in the similarity search results.
1つのクエリに複数のテーブルが関連づけられることを考えると、1つのテーブルが類似検索結果に複数回表示される可能性がある。
Currently, we utilize a simplified strategy to aggregate and score them.
現在、私たちは簡略化された戦略で集計と採点を行っている。
Table summaries carry more weight than query summaries, a scoring strategy that could be adjusted in the future.
テーブル・サマリーはクエリー・サマリーよりも重視されるが、これは将来的に調整可能な得点戦略である。

Other than being used in the Text-to-SQL, this NLP-based table search is also used in the general table search in Querybook.
Text-to-SQLで使用される以外に、このNLPベースのテーブル検索はQuerybookの一般的なテーブル検索でも使用されます。

### Table Re-selection テーブルの再選択

Upon retrieving the top N tables from the vector index, we engage an LLM to choose the most relevant K tables by evaluating the question alongside the table summaries.
ベクトルインデックスから上位N個のテーブルを検索すると、LLMがテーブルの要約とともに質問を評価し、最も関連性の高いK個のテーブルを選択する。
Depending on the context window, we include as many tables as possible in the prompt.
コンテクストウィンドウによって、プロンプトにできるだけ多くのテーブルを含める。
Here is the prompt we’re using for the table re-selection:
以下は、テーブルの再選択に使用するプロンプトである：

Once the tables are re-selected, they are returned to the user for validation before transitioning to the actual SQL generation stage.
テーブルが再選択されると、実際のSQL生成段階に移行する前に、検証のためにユーザーに戻される。

### Evaluation & Learnings 評価と教訓

We evaluated the table retrieval component of our Text-to-SQL feature using offline data from previous table searches.
我々は、過去のテーブル検索のオフラインデータを使用して、Text-to-SQL 機能のテーブル検索コンポーネントを評価した。
This data was insufficient in one important respect: it captured user behavior before they knew that NLP-based search was available.
このデータは、ある重要な点において不十分であった： それは、NLPベースの検索が利用可能であることを知る前のユーザーの行動を捉えているという点である。
Therefore, this data was used mostly to ensure that the embedding-based table search did not perform worse than the existing text-based search, rather than attempting to measure improvement.
したがって、このデータは、改善を測定するためというよりも、埋め込みベースのテーブル検索が既存のテキストベースの検索よりもパフォーマンスが悪くないことを確認するために主に使用された。
We used this evaluation to select a method and set weights for the embeddings used in table retrieval.
この評価を用いて、テーブル検索に使用する埋め込み方法の選択と重みの設定を行った。
This approach revealed to us that the table metadata generated through our data governance efforts was of significant importance to overall performance: the search hit rate without table documentation in the embeddings was 40%, but performance increased linearly with the weight placed on table documentation up to 90%.
このアプローチにより、データ・ガバナンスの取り組みを通じて生成されたテーブル・メタデータが、全体的なパフォーマンスにとって重要であることが明らかになった： 埋め込みにテーブル・ドキュメンテーションがない場合の検索ヒット率は40％でしたが、テーブル・ドキュメンテーションに重きを置くとパフォーマンスは直線的に向上し、90％まで上昇しました。

## Next Steps 次のステップ

While our currently-implemented Text-to-SQL has significantly enhanced our data analysts’ productivity, there is room for improvements.
現在実装しているText-to-SQLは、データアナリストの生産性を大幅に向上させていますが、改善の余地はあります。
Here are some potential areas of further development:
さらなる発展の可能性がある分野をいくつか挙げてみよう：

### NLP Table Search NLP テーブル検索

Metadata Enhancement
メタデータの強化

Currently, our vector index only associates with the table summary.
現在、我々のベクター・インデックスはテーブル・サマリーとしか関連付けられない。
One potential improvement could be the inclusion of further metadata such as tiering, tags, domains, etc., for more refined filtering during the retrieval of similar tables.
潜在的な改良点としては、類似したテーブルを検索する際に、より洗練されたフィルタリングを行うために、階層化、タグ、ドメインなどのメタデータを追加することである。

Scheduled or Real-Time Index Update
インデックスのスケジュール更新またはリアルタイム更新

Currently the vector index is generated manually.
現在、ベクトルインデックスは手動で生成されている。
Implementing scheduled or even real-time updates whenever new tables are created or queries executed would enhance system efficiency.
新しいテーブルが作成されたり、クエリーが実行されたりするたびに、スケジュールされた、あるいはリアルタイムのアップデートを実装することで、システムの効率を高めることができる。

Similarity Search and Scoring Strategy Revision
類似性検索と採点戦略の見直し

Our current scoring strategy to aggregate the similarity search results is rather basic.
類似検索結果を集約するための現在のスコアリング戦略は、かなり基本的なものだ。
Fine-tuning this aspect could improve the relevance of retrieved results.
この点を微調整することで、検索結果の関連性を向上させることができる。

### Query validation クエリ検証

At present, the SQL query generated by the LLM is directly returned to the user without validation, leaving a potential risk that the query may not run as expected.
現在のところ、LLMによって生成されたSQLクエリは、検証されることなく直接ユーザーに返されるため、クエリが期待通りに実行されない可能性がある。
Implementing query validation, perhaps using a constrained beam search, could provide an extra layer of assurance.
クエリ検証を実装することで、おそらくは制約付きビーム検索を使用することで、さらなる保証を提供することができるだろう。

### User feedback ユーザーからのフィードバック

Introducing a user interface to efficiently collect user feedback on the table search and query generation results could offer valuable insights for improvements.
テーブル検索とクエリ生成結果に対するユーザーのフィードバックを効率的に収集するためのユーザーインターフェイスを導入することで、改善のための貴重な洞察が得られる可能性がある。
Such feedback could be processed and incorporated into the vector index or table metadata store, ultimately boosting system performance.
このようなフィードバックは処理され、ベクトル・インデックスやテーブル・メタデータ・ストアに組み込まれ、最終的にシステム・パフォーマンスを向上させることができる。

### Evaluation 評価

While working on this project, we realized that the performance of text-to-SQL in a real world setting is significantly different to that in existing benchmarks, which tend to use a small number of well-normalized tables (which are also prespecified).
このプロジェクトに取り組んでいる間に、実環境におけるテキストからSQLへの変換の性能は、少数の十分に正規化されたテーブル（それも事前に指定されたもの）を使用する傾向にある既存のベンチマークにおける性能とは大きく異なることに気付きました。
It would be helpful for applied researchers to produce more realistic benchmarks which include a larger amount of denormalized tables and treat table search as a core part of the problem.
より多くの非正規化テーブルを含む、より現実的なベンチマークを作成し、テーブル検索を問題の中核部分として扱うことは、応用研究者にとって有益であろう。

To learn more about engineering at Pinterest, check out the rest of our Engineering Blog and visit our Pinterest Labs site.
Pinterestのエンジニアリングについてもっと知りたい方は、エンジニアリングブログの他の部分をチェックし、Pinterest Labsサイトをご覧ください。
To explore and apply to open roles, visit our Careers page.
募集職種を検索して応募するには、採用ページをご覧ください。
