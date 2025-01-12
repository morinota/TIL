https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics

# Practical text-to-SQL for data analytics 実用的なテキストからSQLへの変換によるデータ分析
December 9, 2024 2024年12月9日
Co-authors:Co-authored byAlbert Chen,Co-authored byManas Bundele,Co-authored byGaurav Ahlawat,Co-authored byPatrick Stetz,Co-authored byZhitao (James) W.,Co-authored byQiang Fei,Co-authored byDonghoon (Don) Jung,Co-authored byAudrey Chu,Co-authored byBharadwaj Jayaraman,Co-authored byAyushi  Panth,Co-authored byYatin Arora,Co-authored bySourav Jain,Co-authored byRenjith Varma,Co-authored byAlex Ilin,Co-authored byIuliia Melnychuk 🇺🇦,Co-authored byChelsea C.,Co-authored byJoyan Sil, andCo-authored byXiaofeng Wang
共著者：アルバート・チェン、マナス・バンデレ、ガウラブ・アーラワット、パトリック・ステッツ、ジータオ（ジェームズ）W.、チアン・フェイ、ドンフーン（ドン）・ジョン、オードリー・チュー、バラドワジ・ジャヤラマン、アユシ・パン、ヤティン・アローラ、ソウラブ・ジェイン、レンジス・ヴァルマ、アレックス・イリン、ユリア・メルニチュク 🇺🇦、チェルシー・C.、ジョヤン・シル、そしてシャオフェン・ワン

In most tech companies, data experts spend a significant amount of their time helping colleagues find data they need – time that could be spent on complex analysis and strategic initiatives. 
ほとんどのテクノロジー企業では、**データ専門家は同僚が必要とするデータを見つける手助けに多くの時間を費やしています**。この時間は、複雑な分析や戦略的な取り組みに使うことができるはずです。
This bottleneck not only frustrates data teams but also creates delays for business partners waiting for crucial insights. 
**このボトルネックはデータチームを苛立たせるだけでなく、重要な洞察を待っているビジネスパートナーに遅延を引き起こします**。

Generative AI presents an opportunity to improve this workflow. 
生成AIは、このワークフローを改善する機会を提供します。
As part of our data democratization efforts at LinkedIn, we've developed SQL Bot, an AI-powered assistant integrated within our DARWIN data science platform. 
LinkedInでのデータ民主化の取り組みの一環として、私たちはDARWINデータサイエンスプラットフォームに統合されたAI駆動のアシスタントであるSQL Botを開発しました。
This internal tool transforms natural language questions into SQL: it finds the right tables, writes queries, fixes errors, and enables employees across functions to independently access the data insights they need under the appropriate permissions. 
この内部ツールは、自然言語の質問をSQLに変換します：適切なテーブルを見つけ、クエリを作成し、エラーを修正し、適切な権限の下で各機能の従業員が必要なデータの洞察に独立してアクセスできるようにします。
Behind the scenes, SQL Bot is a multi-agent system built on top of LangChain and LangGraph. 
SQL Botは、LangChainとLangGraphの上に構築されたマルチエージェントシステムです。

![fig]()

While creating a proof of concept for a Text-to-SQL tool is straightforward, the challenge lies in navigating complex enterprise data warehouses to identify authoritative data sources that accurately answer user questions. 
テキストからSQLへのツールの概念実証を作成することは簡単ですが、**課題は複雑な企業データウェアハウスをナビゲートして、ユーザの質問に正確に答える権威あるデータソースを特定すること**にあります。
In this post, we share key strategies that enabled us to deploy a practical text-to-SQL solution, now utilized by hundreds of employees across LinkedIn’s diverse business verticals.
この投稿では、私たちが**実用的なtext-to-sqlソリューションを展開するために採用した重要な戦略**を共有します。このソリューションは、LinkedInの多様なビジネス分野で数百人の従業員によって利用されています。

<!-- ここまで読んだ! -->

## Strategy #1: Quality table metadata and personalized retrieval 戦略 #1: 高品質なテーブルメタデータとパーソナライズされた検索

Text-to-SQL is often framed as a Retrieval-Augmented Generation (RAG) application, where context such as table schemas, example queries, and other domain knowledge are retrieved and passed to a Large Language Model (LLM) to answer the question.
Text-to-SQLは、テーブルスキーマ、例のクエリ、その他のドメイン知識などのコンテキストが取得され、大規模言語モデル（LLM）に渡されて質問に答えるRetrieval-Augmented Generation（RAG）アプリケーションとしてしばしば位置づけられます。

We use Embedding-Based Retrieval (EBR) to retrieve context semantically relevant to the user’s question. 
私たちは、ユーザの質問に意味的に関連するコンテキストを取得するために、Embedding-Based Retrieval (EBR)を使用します。(以降、このブログでは、埋め込みベースの検索をEBRと呼んでる...!:thinking:)
One challenge in retrieving tables and fields is the frequent absence or incompleteness of descriptions. 
**テーブルやフィールドを取得する際の一つの課題は、説明の頻繁な欠如や不完全さ**です。
To address this, we initiated a dataset certification effort to collect comprehensive descriptions for hundreds of important tables. 
これに対処するために、私たちは**数百の重要なテーブルの包括的な説明を収集するためのデータセット認証**の取り組みを開始しました。
Domain experts identified key tables within their areas and provided mandatory table descriptions and optional field descriptions. 
ドメインの専門家は、**自分の分野内の重要なテーブルを特定し、必須のテーブル説明と任意のフィールド説明を提供**しました。
These descriptions were augmented with AI-generated annotations based on existing documentation and Slack discussions, further enhancing our ability to retrieve the right tables and use them properly in queries. 
これらの説明は、既存の文書やSlackの議論に基づいてAI生成の注釈で補完され、正しいテーブルを取得し、クエリで適切に使用する能力がさらに向上しました。

Another challenge is the sheer volume of tables—at LinkedIn, it’s in the millions—and the implicit context embedded in user questions. 
もう一つの課題は、テーブルの数が膨大であることです。LinkedInでは、数百万に及びます。そして、ユーザの質問に埋め込まれた暗黙のコンテキストです。
We can quickly narrow down the volume of tables to a few thousand by looking at access popularity. 
**アクセスの人気を見ることで、テーブルの数を数千に簡単に絞り込むことができる**。
However, addressing the implicit context is more subtle. 
しかし、暗黙のコンテキストに対処することはより微妙です。
For instance, the question "What was the average CTR yesterday?" should be answered differently depending on whether the employee is interested in email notifications, ads or search quality. 
**例えば、「昨日の平均CTRは何でしたか？」という質問は、従業員がメール通知、広告、または検索品質に興味があるかどうかによって異なる答えが必要**です。
To address this, we infer the default datasets for a user based on the organizational chart. 
これに対処するために、私たちは**組織図に基づいてユーザのデフォルトデータセットを推測**します。
We also apply Independent Component Analysis (ICA) across user-dataset access history to develop components (sets of datasets) that correspond to different business use cases. 
また、ユーザとデータセットのアクセス履歴に対して独立成分分析（ICA）を適用し、異なるビジネスユースケースに対応するコンポーネント（データセットのセット）を開発します。
Results are personalized by using the top components relevant to each user. 
結果は、各ユーザに関連するトップコンポーネントを使用することで**パーソナライズ**されます。
Users are able to change the default filter values if needed. 
ユーザは必要に応じてデフォルトのフィルタ値を変更することができます。

In practice, tables and fields are deprecated or added over time. 
実際には、テーブルやフィールドは時間とともに廃止されたり追加されたりします。
It is typical for a table to be used for a few years before it is replaced with another table with improved performance, schema, and/or logic. 
テーブルは、パフォーマンス、スキーマ、またはロジックが改善された別のテーブルに置き換えられるまで数年間使用されるのが一般的です。
Thus, the source of truth to answer a question can change. 
したがって、質問に答えるための真実の源は変わる可能性があります。
To automate the process of picking up new tables, we automatically ingest popular queried tables into our vector store. 
新しいテーブルを取得するプロセスを自動化するために、**人気のあるクエリテーブルを自動的にベクターストアに取り込み**ます。
DataHub, our metadata search and discovery tool, allows users to mark datasets and fields as deprecated – we use this signal to automatically offboard datasets and fields. 
私たちのメタデータ検索および発見ツールであるDataHubは、**ユーザがデータセットやフィールドを廃止としてマークする**ことを可能にします。私たちは**この信号を使用して、データセットやフィールドを自動的にオフボード(退職)**します。

<!-- ここまで読んだ! -->

## Strategy #2: Knowledge graph and LLMs for ranking, writing, self-correction
## 戦略 #2: 知識グラフとLLMsによるランキング、執筆、自己修正

The output of the first strategy is a candidate list of tables, selected by filtering and EBR. 
最初の戦略の出力は、フィルタリングとEBRによって選択された、テーブルの候補リストです。
In this section, we outline a few approaches that have helped us generate accurate queries. 
このセクションでは、正確なクエリを生成するのに役立ったいくつかのアプローチを概説します。

![fig]()
Figure 2: Knowledge graph. Users, table clusters, tables, and fields are nodes. The nodes have attributes derived from DataHub, query logs, crowdsourced domain knowledge, etc.
図2: 知識グラフ。ユーザ、テーブルクラスタ、テーブル、フィールドがノードです。ノードには、DataHub、クエリログ、クラウドソーシングされたドメイン知譆などから派生した属性があります。

First, we need a deep semantic understanding of concepts and datasets to generate accurate queries. 
まず、正確なクエリを生成するためには、概念とデータセットに対する深いsemantic understanding(意味理解)が必要です。
In addition to leveraging tables and fields, we organize additional information into a knowledge graph: 
**テーブルとフィールドを活用するだけでなく、追加情報を知識グラフに整理**します。

1. We use DataHub to look up table schemas, field descriptions, the top K values for categorical dimension fields, partition keys, and a classification of fields into metrics, dimensions, and attributes. 
私たちはDataHubを使用して、テーブルスキーマ、フィールドの説明、カテゴリ次元フィールドの上位K値、パーティションキー、およびフィールドの分類(metrics、dimensions、attributes)を調べます。

2. We collect domain knowledge from users in SQL Bot’s UI. SQL BotのUIからユーザのドメイン知識を収集します。

3. We use successful queries from query logs to derive aggregate information, such as table/field popularity and common table joins. 
クエリログから成功したクエリを使用して、**テーブル/フィールドの人気**や**一般的なテーブル結合**などの集約情報を導出します。

4. We incorporate example queries from internal wikis and from notebooks in DARWIN. 
**内部ウィキやDARWINのノートブックからの例クエリ**を取り入れます。
Because the quality of code in DARWIN can vary, we only include notebooks certified by users and those that meet a set of heuristics for recency and reliability – for instance, we prefer recently created notebooks titled by users that have a high number of executions. 
**DARWINのコードの品質はさまざまなので、ユーザによって認証されたノートブックと、最近性と信頼性のための一連のヒューリスティック(i.e. ルールベースでの判定ロジック!:thinking:)を満たすノートブックのみを含めます**。
ヒューリスティックの例: 高い実行回数を持つユーザによって、最近作成されたノートブックは有効とする。

<!-- ここまで読んだ! -->

Then, we use LLMs to filter and sort the results from EBR using the knowledge graph. 
次に、知識グラフを使用して、EBRからの結果をフィルタリングおよびソートするためにLLMsを使用します。(**EBRした結果に対して、知識グラフ*LLMで際フィルタリング&ソートするってことぽい...?**:thinking:)
After retrieving the top 20 tables via EBR, we employ a LLM re-ranker to select the top 7 tables for query writing. 
**EBRを介して上位20のテーブルを取得した後、クエリ作成のために上位7のテーブルを選択するためにLLM再ランキングを使用**します。
The inputs to table selection include table descriptions, example queries, domain knowledge, and explanations of internal jargon detected in the user’s question. 
**テーブル選択の入力には、テーブルの説明、例クエリ、ドメイン知識、およびユーザの質問で検出された内部用語の説明が含まれます**。
We use another LLM re-ranker to select fields from the selected tables. 
**選択されたテーブルからフィールドを選択するために、別のLLM再ランキングを使用**します。
The input to field selection includes the information used for table selection, plus the full table schemas with field descriptions, top K values, and other field attributes. 
フィールド選択の入力には、**テーブル選択に使用される情報に加えて、フィールドの説明、上位K値、および他のフィールド属性を含む完全なテーブルスキーマ**が含まれます。
Fields are ordered by access frequency over a recent time window. 
フィールドは、最近の時間ウィンドウでの**アクセス頻度によって順序付け**されます。

After that, our query writing process is iterative, so that SQL Bot generates a plan and solves each step of the plan incrementally to build to the final query. 
その後、私たちの**クエリ作成プロセスはiterative**であり、SQL Botは計画を生成し、最終クエリを構築するために計画の**各ステップを段階的に解決**します。(やっぱり分業させるのが有効なのか...!:thinking:)
Solutions to previous tasks are stored in our chatbot’s internal state to be provided to the next step. 
以前のタスクの解決策は、次のステップに提供されるために、私たちのチャットボットの内部状態に保存されます。(=これはLangGraphのノード間の通信の話っぽい...!:thinking:)
While this method is effective for complex questions, we found it can result in overly complicated queries for simple questions, so we instruct the query planner to minimize the number of steps it creates. 
この方法は複雑な質問には効果的ですが、単純な質問に対して過度に複雑なクエリを生成することがあるため、クエリプランナーに作成するステップの数を最小限に抑えるよう指示します。
This condenses queries for simple questions while maintaining performance on complex questions. 
これにより、単純な質問のクエリが簡潔になり、複雑な質問に対するパフォーマンスが維持されます。

Finally, we run a set of validators on the output followed by a self-correction agent to fix errors. 
最後に、**出力に対して一連のバリデーターを実行**し、その後にエラーを修正するための自己修正エージェントを実行します。
Validators work best when they access new information not available to the query writer. 
**バリデーターは、クエリ作成者が利用できない新しい情報にアクセスする際に最も効果的**です。
We verify the existence of tables and fields, and execute the EXPLAIN statement on the query to detect syntax and other errors. 
テーブルとフィールドの存在を確認し、**クエリに対してEXPLAIN文を実行**して構文やその他のエラーを検出します。
These errors are fed into a self-correction agent, which is equipped with tools to retrieve additional tables or fields if needed before updating the query. 
これらのエラーは自己修正エージェントに送られ、必要に応じてクエリを更新する前に追加のテーブルやフィールドを取得するためのツールが装備されています。

![](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics)
Figure 3: Modeling architecture. The user’s question is classified and delegated to the appropriate flow. Open-ended follow-up chats are handled by an agent.
図3: モデリングアーキテクチャ。ユーザの質問は分類され、適切なフローに委任されます。オープンエンドのフォローアップチャットはエージェントによって処理されます。

<!-- ここまで読んだ! -->

## Strategy #3: User experience with rich chat elements
## 戦略 #3: リッチチャット要素を用いたユーザ体験

User experience is central to gaining adoption. 
ユーザ体験は、採用を得るための中心的な要素です。
Users prioritize ease of use and fast responses. 
ユーザーは**使いやすさと迅速な応答**を重視します。

We integrated SQL Bot directly into DARWIN, allowing users to access it within the same browser window as they write and execute their queries. 
私たちは**SQL BotをDARWINに直接統合し、ユーザがクエリを作成して実行する際に同じブラウザウィンドウ内でアクセスできる**ようにしました。
This integration increased adoption by 5-10x compared to our prototype chatbot application launched as a standalone app. 
この統合により、**スタンドアロンアプリとして立ち上げたプロトタイプチャットボットアプリケーションと比較して、採用が5〜10倍増加**しました。
To aid discovery, DARWIN has entry points for SQL Bot in the sidebar, as well as a “Fix with AI” button that appears whenever a query execution fails. 
発見を助けるために、DARWINにはサイドバーにSQL Botへのエントリーポイントがあり、クエリの実行が失敗するたびに「AIで修正」ボタンが表示されます。
Chat history is saved so users can continue previous conversations. 
チャット履歴は保存されるため、ユーザは以前の会話を続けることができます。
They can also submit in-product feedback or add custom instructions to personalize the bot’s behavior. 
ユーザーは製品内フィードバックを送信したり、ボットの動作をパーソナライズするためのカスタム指示を追加することもできます。

Our initial prototype answered every question with a SQL query, but users actually wanted to find tables, ask questions about the datasets, see reference queries, or ask general questions about query syntax. 
私たちの初期プロトタイプはすべての質問にSQLクエリで回答しましたが、**ユーザは実際にはテーブルを見つけたり、データセットに関する質問をしたり、参考クエリを見たり、クエリ構文に関する一般的な質問をしたい**と考えていました。
We now use intent classification to classify the question and decide how to respond. 
現在、私たちは意図分類を使用して質問を分類し、どのように応答するかを決定しています。

It’s essential for a chatbot to be conversational so that users can ask follow-up questions. 
**チャットボットが会話形式であることは重要であり、ユーザがフォローアップの質問をすることができる**ようにします。(なるほど、ユーザが補足情報を書き足して出力を調整できるという点で、会話形式であることが重要なのか...!:thinking:)
We provide “quick replies” such as “update query,” “update table selections,” and “explain these tables” to guide users on the types of follow-ups they could try. 
私たちは“**quick replies**”として「クエリを更新」、「テーブル選択を更新」、「これらのテーブルを説明」などを提供し、ユーザが試すことができるフォローアップの種類を案内します。(UIの工夫!)
Additionally, users have the option to enable a guided experience, where SQL Bot walks them through each step of the query writing process—finding tables, and solving each step in the query.
さらに、ユーザはガイド付き体験を有効にするオプションがあり、SQL Botがクエリ作成プロセスの各ステップを案内します—テーブルを見つけ、クエリの各ステップを解決します。
The user can interact at each step to provide feedback on the table or queries. 
ユーザーは各ステップでインタラクションを行い、テーブルやクエリに対するフィードバックを提供できます。
This helps users understand the query and gives them more control over the query-writing process. 
これにより、**ユーザはクエリを理解し、クエリ作成プロセスに対するコントロールを強化できます**。(Langgraphだとこの辺りの実装もやりやすいのかな...!:thinking:)

To help users understand the bot’s output, we have incorporated rich display elements for tables and queries. 
ユーザがボットの出力を理解できるように、テーブルとクエリのためのリッチ表示要素を組み込みました。
The table element shows the retrieved tables, their descriptions, tags indicating whether the dataset is “certified” or “popular”, average monthly access frequency, commonly joined tables, and a link to DataHub for more information. 
テーブル要素は、取得したテーブル、その説明、データセットが「認定」または「人気」であるかを示すタグ、平均月間アクセス頻度、一般的に結合されるテーブル、および詳細情報のためのDataHubへのリンクを表示します。
In the guided experience, users may use these checkboxes to select the tables they want the bot to use. 
ガイド付き体験では、ユーザはこれらのチェックボックスを使用して、ボットに使用してほしいテーブルを選択できます。
The query element displays the formatted query, explanation, and validation checks on whether the tables exist, fields exist, and the syntax is correct. 
クエリ要素は、フォーマットされたクエリ、説明、およびテーブルが存在するか、フィールドが存在するか、構文が正しいかの検証チェックを表示します。
This helps users understand the output and identify any issues that need fixing. 
これにより、ユーザーは出力を理解し、修正が必要な問題を特定できます。
They can ask the bot to make updates. 
ユーザーはボットに更新を依頼することができます。

![]()
Figure 5: Query output includes validation checks, explanation, and tables.
図5: クエリ出力には、検証チェック、説明、およびテーブルが含まれます。

Each dataset at LinkedIn has its own access control list which permits dataset read access to only specific users or groups. 
LinkedInの各データセットには、特定のユーザまたはグループにのみデータセットの読み取りアクセスを許可する独自のアクセス制御リストがあります。(うんうん...!:thinking:)
To prevent issues where a user runs a query and is denied access, we check if the user is a member of a group with the appropriate access and if so, we automatically provide the code necessary to leverage the group's credentials. 
ユーザがクエリを実行してアクセスを拒否される問題を防ぐために、ユーザが適切なアクセス権を持つグループのメンバーであるかどうかを確認し、そうであれば、グループの資格情報を利用するために必要なコードを自動的に提供します。
This reduces frustration for the user, especially for those new to SQL at LinkedIn. 
これにより、特にLinkedInでSQLに不慣れなユーザのフラストレーションが軽減されます。

<!-- ここまで読んだ! -->

## Strategy #4: Options for user customization 戦略 #4: ユーザーカスタマイズのオプション

We want users to have the ability to improve SQL Bot’s performance without making requests to the platform team. 
私たちは、**ユーザがプラットフォームチームにリクエストをせずにSQL Botのパフォーマンスを向上させる能力を持つこと**を望んでいます。(評価に基づく改善だ...!:thinking:)
To this end, we provide three levers that allow users to customize the experience for their product area: 
この目的のために、私たちはユーザが自分の製品領域に対する体験をカスタマイズできる3つの手段を提供します。

1. **Dataset customization**: Users can define the datasets for a product area by providing email group(s) or by explicitly specifying the users and datasets to use. 
データセットのカスタマイズ: ユーザは、メールグループを提供するか、使用するユーザとデータセットを明示的に指定することによって、製品領域のデータセットを定義できます。 
The product area’s datasets are those commonly used by the group of users in that area, with the option to include or exclude additional datasets as specified. 
製品領域のデータセットは、その領域のユーザーグループによって一般的に使用されるものであり、指定された追加のデータセットを含めるか除外するオプションがあります。 
Users can select product areas to use through the UI. 
ユーザはUIを通じて使用する製品領域を選択できます。

2. **Custom instructions**: Users can provide custom textual instructions to SQL Bot directly in DARWIN. 
カスタム指示: ユーザは、DARWIN内でSQL Botに直接カスタムテキスト指示を提供できます。 
The instructions can either enrich the overall domain knowledge of SQL Bot or provide guidelines for SQL Bot to behave in a specific manner to match user preferences. 
これらの指示は、SQL Botの全体的なドメイン知識を豊かにするか、ユーザの好みに合わせて特定の方法で動作するためのガイドラインを提供します。 
The user-supplied instructions are used when selecting tables and fields, and when writing and fixing queries. 
**ユーザが提供した指示は、テーブルやフィールドを選択する際、またクエリを書く際や修正する際に使用**されます。

3. Example queries: Users can create example queries to be indexed into our vector store. 
例示クエリ: **ユーザは、ベクトルストアにインデックスされる例示クエリを作成できます**。(これはいいね!:thinking:)
These can be added directly in DARWIN by creating a notebook and tagging it as “certified.” 
これらは、ノートブックを作成し、「certified」とタグ付けすることで、DARWINに直接追加できます。(Snowflakeでもnotebookを作る感じだから、この辺りの実装もやりやすいかも...!:thinking:)

<!-- ここまで読んだ! -->

## Strategy #5: Ongoing Benchmarking 戦略 #5: 継続的なベンチマーキング

There are many hyperparameters for the bot, such as what text to embed, what context to pass to each LLM, how to represent the context and meta prompts, how to manage agent memory, how many items to retrieve, how many times to run self-correction, and which steps to include in the model architecture. 
**ボットには多くのハイパーパラメータがあり**、どのテキストを埋め込むか、各LLMにどのコンテキストを渡すか、コンテキストとメタプロンプトをどのように表現するか、エージェントのメモリをどのように管理するか、取得するアイテムの数、自己修正を実行する回数、モデルアーキテクチャに含めるステップなどがあります。 
Therefore, it is crucial to develop a benchmark set to assess both quality and performance.
したがって、**品質とパフォーマンスの両方を評価するためのベンチマークセットを開発することが重要**です。

A benchmark should preferably be tailored to the specific application, as text-to-SQL requirements can vary widely depending on factors like the target user, number of datasets, the clarity of table and column names, the complexity of the desired queries, the SQL dialect, target response time, and the degree of specialized domain knowledge required. 
ベンチマークは、特定のアプリケーションに合わせて調整されるべきであり、text-to-SQLの要件は、ターゲットユーザ、データセットの数、テーブルおよびカラム名の明確さ、望ましいクエリの複雑さ、SQLダイアレクト、ターゲット応答時間、必要な専門的ドメイン知識の程度などの要因によって大きく異なる可能性があります。 
We collaborated with domain experts across 10 product areas to define a set of over 130 benchmark questions. 
私たちは、**10の製品分野にわたるドメイン専門家と協力して、130以上のベンチマーク質問のセットを定義しました**。 
Each question includes a well-formulated question and ground truth answers.
各質問には、**適切に構成された質問と真実の回答**が含まれています。

Our evaluation metrics include recall of tables and fields compared to the ground truth, table/field hallucination rate, syntax correctness, and response latency. 
**私たちの評価指標には、真実と比較したテーブルおよびフィールドの再現率、テーブル/フィールドのhallucination率、構文の正確性、応答のレイテンシが含まれます**。
These are easy to compute and we focused on these during the first phase of development while we worked on finding the right tables/fields and avoiding obvious query issues.
これらは計算が容易であり、私たちは最初の開発段階で、適切なテーブル/フィールドを見つけ、明らかなクエリの問題を避けることに注力しました。

For example, this chart shows the increase in table recall from adding re-rankers, descriptions, and example queries:
例えば、このチャートは、再ランカー、説明、および例のクエリを追加することによるテーブルの再現率の増加を示しています。

![]()
Figure 6: Re-rankers, descriptions, and example queries help SQL Bot identify the correct tables.
図6: 再ランカー、説明、および例のクエリは、SQL Botが正しいテーブルを特定するのに役立ちます。

<!-- ここまで読んだ! -->

However, those metrics are not sufficient to assess query accuracy. 
しかし、**これらの指標だけではクエリの正確性を評価するには不十分**です。 
For that, we use a combination of human evaluation and LLM-as-a-judge to evaluate responses given the question, the table schemas, and the ground truths. 
そのために、私たちは**人間の評価とLLM-as-a-judgeの組み合わせを使用**して、質問、テーブルスキーマ、および真実に基づいて応答を評価します。 
The rubric includes overall score and dimensions on correctness in terms of tables, columns, joins, filters, aggregations, etc. as well as the quality of the answer in terms of efficiency and complexity. 
評価基準には、テーブル、列、結合、フィルタ、集計などの観点での正確性に加えて、効率性と複雑さの観点での回答の品質に関する総合スコアと次元が含まれています。
This approach was more practical for us than running SQL queries and comparing outputs because it does not require data access, allows us to assess how close the query is to being correct, and gives deeper insights on how the model can be improved.
このアプローチは、SQLクエリを実行して出力を比較するよりも実用的でした。なぜなら、データアクセスを必要とせず、クエリがどれだけ正確であるかを評価でき、モデルを改善するためのより深い洞察を提供するからです。
(このセクションよくわかってない...!:thinking:)

We discovered early on that there can be multiple ways to answer a question. 
私たちは早い段階で、**質問に対する回答方法が複数存在する可能性**があることを発見しました。 
About ~60% of our benchmark questions now have multiple answers. 
現在、私たちのベンチマーク質問の約60%には複数の回答があります。 
Without these additional answers, we underreported recall by 10-15%. 
これらの追加の回答がなければ、私たちは再現率を10-15%過小報告していました。 
We use expert human review every 3 months to add accepted answers to our benchmark. 
私たちは、**3か月ごとに専門家によるレビューを行い、受け入れられた回答をベンチマークに追加**します。 
LLM-as-a-judge facilitates this process: we’ve found that it returns a score within 1 point of the human score 75% of the time, and larger disagreements often indicate that there’s a correct answer not in our SOT. 
LLM-as-a-judgeはこのプロセスを容易にする。私たちは、LLMが人間のスコアから1ポイント以内のスコアを75%の確率で返すことを発見しました。また、大きな不一致は、私たちのSOTにない正しい回答が存在することを示すことがよくあります。 
We ask experts to review these cases and update our benchmark if needed.
私たちは専門家にこれらのケースをレビューしてもらい、必要に応じてベンチマークを更新してもらいます。

<!-- ここまで読んだ! -->

## Conclusion 結論

We have been building SQL Bot for over 1 year across a virtual team that has domain expertise in our priority product areas. 
私たちは、優先製品分野におけるドメイン専門知識を持つバーチャルチームで、**1年以上にわたりSQL Botを構築**してきました。 
Our early pilots gathered a lot of interest from users, and we’ve seen sustained adoption in the months following integration into DARWIN. 
初期のパイロットでは多くのユーザの関心を集め、DARWINへの統合後の数ヶ月間で持続的な採用が見られました。 
In a recent survey, ~95% rated SQL Bot’s query accuracy “Passes” or above, and ~40% rated the query accuracy “Very Good” or “Excellent”. 
最近の調査では、約95%がSQL Botのクエリ精度を「合格」以上と評価し、約40%が「非常に良い」または「優秀」と評価しました。 

Looking ahead, there are opportunities to improve the user experience, for example through faster response time, in-line query revisions, exposing the context that SQL Bot used to answer the question, and learning from user interactions over time. 
今後は、ユーザエクスペリエンスを改善する機会があり、例えば、応答時間の短縮、インラインクエリ修正、SQL Botが質問に答えるために使用したコンテキストの提示、ユーザーとのインタラクションからの学習などが考えられます。 
Additionally, improving semantic accuracy could be facilitated by identifying champions to lead self-serve context curation efforts within their respective areas. 
さらに、意味的精度の向上は、それぞれの分野でセルフサービスのコンテキストキュレーション活動をリードするチャンピオンを特定することで促進される可能性があります。 

One takeaway is that the “Fix with AI” feature was easy to develop but has very high usage—accounting for 80% of our sessions—frequently saving users time in debugging their queries. 
一つの教訓は、**“Fix with AI” 機能は開発が容易であったが、非常に高い使用率を誇り、私たちのセッションの80%を占め、ユーザがクエリのデバッグにかかる時間を頻繁に節約している**ということです。
Identifying high-ROI pain points like this is a good place to start the text-to-SQL journey. 
このような**高ROIのpain pointsを特定**することは、text-to-SQLの旅を始める良い出発点です。(俺もROIの高いpain point特定してぇ〜! 推薦だと、まずは1つの行動を推薦する意思決定最適化問題かな...!:thinking:)

<!-- ここまで読んだ! -->

## Acknowledgements 謝辞

Thanks to all contributors to the project across Engineering / Product, including Michael Cheng, Clarisse Rahbar, Sparsh Agarwal, Manohar Mohan Rao, Paul Lee, Vishal Chandawarkar. 
エンジニアリング/プロダクト全体のプロジェクトに貢献したすべての方々、特にMichael Cheng、Clarisse Rahbar、Sparsh Agarwal、Manohar Mohan Rao、Paul Lee、Vishal Chandawarkarに感謝します。

Thanks to Trino experts for brainstorming ideas, writing a query plan parser, and reviewing this blog post: Erik Krogen, Slim Bouguerra. 
アイデアをブレインストーミングし、クエリプランパーサーを作成し、このブログ投稿をレビューしてくれたTrinoの専門家、Erik Krogen、Slim Bouguerraに感謝します。

Thanks to Data Science experts for curating the benchmark dataset and evaluating query accuracy: Kavi Tan, Andrew Jabara, Noora Wu, Ruoyun Guo, Steve Na, Ashish Tripathy, Michael Kosk, Lingjun Chen, Cole Silva, Feiran Ji, Janet Luo, Franklin Marsh, Mengyao Yang, Tao Lin, Huanqi Zhu, Paul Matsiras, Andrew Kirk. 
ベンチマークデータセットをキュレーションし、クエリの精度を評価してくれたデータサイエンスの専門家、Kavi Tan、Andrew Jabara、Noora Wu、Ruoyun Guo、Steve Na、Ashish Tripathy、Michael Kosk、Lingjun Chen、Cole Silva、Feiran Ji、Janet Luo、Franklin Marsh、Mengyao Yang、Tao Lin、Huanqi Zhu、Paul Matsiras、Andrew Kirkに感謝します。

Thanks to Engineering partners for providing APIs for knowledge graph construction: Shailesh Jannu, Na Zhang, Leo Sun, Alex Bachuk, Steve Calvert. 
ナレッジグラフ構築のためのAPIを提供してくれたエンジニアリングパートナー、Shailesh Jannu、Na Zhang、Leo Sun、Alex Bachuk、Steve Calvertに感謝します。

Thanks to Leadership for supporting this project: Ya Xu, Zheng Li, Jia Ding, Kuo-Ning Huang, Harikumar Velayutham, Shishir Sathe, Justin Dyer. 
このプロジェクトを支援してくれたリーダーシップ、Ya Xu、Zheng Li、Jia Ding、Kuo-Ning Huang、Harikumar Velayutham、Shishir Sathe、Justin Dyerに感謝します。

Topics: Generative AI, Artificial intelligence, Data Management, Data Science 
トピック: ジェネレーティブAI、人工知能、データ管理、データサイエンス
