

# QueryGPT – Natural Language to SQL Using Generative AI
# QueryGPT – 自然言語からSQLへの生成AIの利用

September 19, 2024/Global
2024年9月19日/グローバル

# Introduction はじめに

SQL is a vital tool used daily by engineers, operations managers, and data scientists at Uber to access and manipulate terabytes of data. 
SQLは、エンジニア、オペレーションマネージャー、データサイエンティストがUberで日常的に使用し、テラバイトのデータにアクセスし操作するための重要なツールです。
Crafting these queries not only requires a solid understanding of SQL syntax, but also deep knowledge of how our internal data models represent business concepts. 
これらのクエリを作成するには、SQLの構文をしっかり理解するだけでなく、**私たちの内部データモデルがビジネス概念をどのように表現しているかについての深い知識も必要**です。
QueryGPT aims to bridge this gap, enabling users to generate SQL queries through natural language prompts, thereby significantly enhancing productivity. 
QueryGPTはこのギャップを埋めることを目指しており、ユーザーが自然言語のプロンプトを通じてSQLクエリを生成できるようにし、生産性を大幅に向上させます。
QueryGPT uses large language models (LLM), vector databases, and similarity search to generate complex queries from English questions that are provided by the user as input. 
QueryGPTは、大規模言語モデル（LLM）、ベクターデータベース、および類似性検索を使用して、ユーザーが入力として提供する英語の質問から複雑なクエリを生成します。
This article chronicles our development journey over the past year and where we are today with this vision. 
この記事では、過去1年間の開発の旅と、私たちがこのビジョンにおいて現在どこにいるのかを記録します。

<!-- ここまで読んだ! -->

## Motivation 動機

![]()

At Uber, our data platform handles approximately 1.2 million interactive queries each month. 
Uberでは、私たちのデータプラットフォームは毎月約120万件のインタラクティブクエリを処理しています。
The Operations organization, one of the largest user cohorts, contributes to about 36% of these queries. 
オペレーション組織は、最も大きなユーザ群の一つであり、これらのクエリの約36%を占めています。
Authoring these queries generally requires a fair amount of time between searching for relevant datasets in our data dictionary and then authoring the query inside our editor. 
これらのクエリを作成するには、一般的にデータ辞書で関連するデータセットを検索し、その後エディタ内でクエリを作成するまでにかなりの時間がかかります。
Given that each query can take around 10 minutes to author, the introduction of QueryGPT, which can automate this process and generate reliable queries in just about 3 minutes, represents a major productivity gain. 
各クエリの作成に約10分かかると仮定すると、QueryGPTの導入はこのプロセスを自動化し、わずか3分で信頼性のあるクエリを生成できるため、大きな生産性向上を意味します。

If we make a conservative estimate that each query takes about 10 minutes to author, QueryGPT can automate this process and provide sufficiently reliable queries in about 3 minutes. 
各クエリの作成に約10分かかるという保守的な見積もりを行うと、QueryGPTはこのプロセスを自動化し、約3分で十分に信頼性のあるクエリを提供できます。
This would result in a major productivity gain for Uber. 
これはUberにとって大きな生産性向上をもたらすでしょう。

![Figure 2: Querybuilder Usage.]()

![Figure 3: QueryGPT Impact.]()

<!-- ここまで読んだ! -->

## Architecture アーキテクチャ

QueryGPT originated as a proposal during Uber’s Generative AI Hackdays in May 2023. 
QueryGPTは、2023年5月にUberのGenerative AI Hackdaysで提案として始まりました。
Since then, we have iteratively refined the core algorithm behind QueryGPT, transitioning it from concept to a production-ready service. 
それ以来、**私たちはQueryGPTのコアアルゴリズムを反復的に洗練させ、PoCから生産準備が整ったサービスへと移行**しました。
Below, we detail the evolution of QueryGPT and its current architecture, highlighting key enhancements. 
以下に、**QueryGPTの進化と現在のアーキテクチャを詳述し、重要な改善点を強調**します。

We’ve described below our current version of QueryGPT. 
私たちは、以下に現在のQueryGPTのバージョンを説明します。
Please bear in mind that there were about 20+ iterations of the algorithm between the 2 detailed below and if we were to list and describe each, the length of this blog article would put Ayn Rand’s Atlas Shrugged to shame. 
**以下に詳述する2つ**の間には約20回以上のアルゴリズムの反復があり、もしそれぞれをリストアップして説明した場合、このブログ記事の長さはアイン・ランドの『肩をすくめるアトラス』を恥じ入らせることになることを考慮してください。

### Hackdayz (version 1) Hackdayz（バージョン1）

![Figure 4: QueryGPT Hackdayz version]()

The first version of QueryGPT relied on a fairly simple RAG to fetch the relevant samples we needed to include in our query generation call to the LLM (Few Shot Prompting). 
QueryGPTの最初のバージョンは、LLM（Few Shot Prompting）へのクエリ生成呼び出しに含める必要がある関連サンプルを取得するために、**かなりシンプルなRAG**に依存していました。
We would take the user’s natural language prompt, vectorize it and do a similarity search (using k-nearest neighbor search) on the SQL samples and schemas to fetch 3 relevant tables and 7 relevant SQL samples. 
**ユーザの自然言語プロンプトを取得し、それをベクトル化して、SQLサンプルとスキーマに対して類似性検索（k近傍探索を使用）を行い、3つの関連テーブルと7つの関連SQLサンプルを取得**しました。(今の我々のやり方と同じだ!:thinking:)

The first version used 7 tier 1 tables and 20 SQL queries as our sample data set. 
最初のバージョンでは、**7つのTier 1テーブル**と20のSQLクエリをサンプルデータセットとして使用しました。(最初は、検索対象のテーブルをtier1のみに絞ってたのか...!:thinking:)
The SQL queries were supposed to provide the LLM guidance on how to use the table schemas provided and the table schemas provided the LLM information about the columns that existed on those tables. 
SQLクエリは、提供されたテーブルスキーマの使用方法についてLLMにガイダンスを提供し、テーブルスキーマはそれらのテーブルに存在する列に関する情報をLLMに提供することを意図していました。

For example, for a tier 1 table, uber.trips_data (not a real table), this is what the schema would look like: 
例えば、Tier 1テーブルであるuber.trips_data（実際のテーブルではありません）の場合、スキーマは次のようになります：

![Figure 5: uber.trips_data table.]()

To help the LLM understand internal Uber lingo and work with Uber datasets, we also included some custom instructions in the LLM call. 
**LLMが内部のUber用語を理解し、Uberデータセットで作業できるように、LLM呼び出しにカスタム指示**も含めました。
Shown below is a snippet of how we wanted the LLM to work with dates: 
以下に、LLMが日付とどのように連携することを望んでいたかのスニペットを示します：

![Figure 6: Custom Instructions for handling dates in Uber datasets.]()

We would wrap all the relevant schema samples, SQL samples, user’s natural language prompt, and Uber Business instructions around a system prompt and send the request to the LLM. 
関連するすべてのスキーマサンプル、SQLサンプル、ユーザーの自然言語プロンプト、およびUberビジネス指示をシステムプロンプトで囲み、LLMにリクエストを送信しました。

The response would include an “SQL Query” and an “Explanation” of how the LLM generated the query: 
**応答には「SQLクエリ」と、LLMがクエリを生成した方法の「説明」が含まれます**：
(このレスポンスの構造は、Pinterestと同じだな...!:thinking:)

![Figure 7: Generated SQL with Explanation.]()

While this version of the algorithm worked well for a small set of schemas and SQL samples, as we started to onboard more tables and their associated SQL samples into the service, we started seeing declining accuracy in the generated queries. 
このバージョンのアルゴリズムは、小規模なスキーマとSQLサンプルのセットではうまく機能しましたが、**より多くのテーブルとそれに関連するSQLサンプルをサービスにオンボードし始めると、生成されたクエリの精度が低下し始めました**。(そうなんだ...!:thinking:)

<!-- ここまで読んだ! -->

### Better RAG (RAGの品質向上の話かな)

Doing a simple similarity search for a user’s natural language prompt (“Find the number of trips completed yesterday in Seattle”) on schema samples (CREATE TABLE…) and SQL queries (SELECT a, b, c FROM uber.foo…) doesn’t return relevant results.
ユーザーの自然言語プロンプト（「昨日シアトルで完了した旅行の数を見つける」）に対して、スキーマサンプル（CREATE TABLE…）やSQLクエリ（SELECT a, b, c FROM uber.foo…）で単純な類似性検索を行っても、関連する結果は返ってきません。

### Understanding User’s Intent ユーザの意図の理解

Another issue we found was that it’s incredibly challenging to go from a user’s natural language prompt to finding the relevant schemas. 
私たちが見つけた別の問題は、**ユーザの自然言語のプロンプトから関連するスキーマを見つけることが非常に難しい**ということです。
What we needed was an intermediate step, which classifies the user’s prompt into an “intent” that maps to relevant schemas and SQL samples.
**私たちに必要だったのは、中間ステップ**であり、ユーザのプロンプトを関連するスキーマとSQLサンプルにマッピングされる「意図」に分類するものでした。
(ここで意図分類器, intent classifierを使うのか...!)

### Handling Large Schemas 大規模スキーマの取り扱い

We have some really large schemas on some Tier 1 tables at Uber, with some spanning over 200 columns. 
私たちは、**UberのいくつかのTier 1テーブルに非常に大きなスキーマを持っており、その中には200列を超えるものもあります**。(大規模スキーマを持つテーブル、うちでもたまにあるやつだ...!!:thinking:)
These large tables could use up as much as 40-60K tokens in the request object. 
これらの大規模テーブルは、リクエストオブジェクト内で40-60Kトークンを消費する可能性があります。
Having 3 or more of these tables would break the LLM call since the largest available model (at the time) only supported 32K tokens. 
これらのテーブルが3つ以上あると、当時利用可能な最大モデルが32Kトークンしかサポートしていなかったため、LLM呼び出しが失敗します。

<!-- ここまで読んだ -->

## Current Design 現在の設計

The diagram below shows the current design of QueryGPT that we’re running in production. 
以下の図は、私たちが運用中のQueryGPTの現在の設計を示しています。
The current version includes many iterative changes from the first version.
現在のバージョンは、最初のバージョンからの多くの反復的な変更を含んでいます。

![Figure 8: QueryGPT (current).]()

### Workspaces 作業スペース

In our current design, we introduced “workspaces,” which are curated collections of SQL samples and tables tailored to specific business domains such as Ads, Mobility, and Core Services. 
現在の設計では、「**作業スペース**」を導入しました。これは、広告、モビリティ、コアサービスなどの**特定のビジネスドメインに合わせたSQLサンプルとテーブルのキュレーションされたコレクション**です。(これが前述されてた、意図分類器のラベル...?? もしくはユーザ自身が指定するものかも...??)
These workspaces help narrow the focus for the LLM, improving the relevance and accuracy of generated queries.
これらの作業スペースは、LLMの焦点を絞り、生成されるクエリの関連性と正確性を向上させるのに役立ちます。

We’ve identified some of the more common business domains inside Uber and created those in the backend as “System Workspaces.” 
私たちは、Uber内の一般的なビジネスドメインのいくつかを特定し、それらをバックエンドで「システム作業スペース」として作成しました。
Mobility is one of these system workspaces that we identified as foundational domains that could be used for query generation.
モビリティは、クエリ生成に使用できる基盤となるドメインとして特定したこれらのシステム作業スペースの1つです。

Mobility: Queries that include trips, driver, document details, etc.
モビリティ：旅行、ドライバー、ドキュメントの詳細などを含むクエリ。

Along with these, we also shipped 11 other system workspaces, including “Core Services,” “Platform Engineering,” “IT,” “Ads,” etc.
これらに加えて、「コアサービス」、「プラットフォームエンジニアリング」、「IT」、「広告」など、11の他のシステム作業スペースも提供しました。
We also included a feature that allows users to create “Custom Workspaces” if none of the existing system workspaces fit their requirement and use those for query generation.
また、既存のシステム作業スペースが要件に合わない場合にユーザーが「カスタム作業スペース」を作成し、それをクエリ生成に使用できる機能も含めました。

### Intent Agent インテントエージェント

Every incoming prompt from the user now first runs through an “intent” agent. 
すべてのユーザからの入力プロンプトは、まず「インテント」エージェントを通過します。
The purpose of this intent agent is to map the user’s question to one or more business domains/workspaces (and by extension a set of SQL samples and tables mapped to the domain). 
このインテントエージェントの目的は、**ユーザの質問を1つ以上のビジネスドメイン/ワークスペース （およびそれに関連するSQLサンプルとドメインにマッピングされたテーブルのセット）にマッピングすること**です。(あ、じゃあやっぱりworkspaceが意図分類器の出力ラベルっぽい...!)
We use an LLM call to infer the intent from the user question and map these to “system” workspaces or “custom” workspaces. 
私たちは、ユーザの質問からインテントを推測し、これを「システム」ワークスペースまたは「カスタム」ワークスペースにマッピングするためにLLMコールを使用します。
(意図分類器のモデルは、内製ではなくLLMコール...!)

Picking a business domain allowed us to drastically narrow the search radius for RAG. 
ビジネスドメインを選択することで、**RAGの検索範囲を大幅に狭める**ことができました。
(目的は、検索範囲を狭めてRAGのretrieveの品質を向上することなのか...!)

### Table Agent テーブルエージェント

Allowing users to select the tables used in the query generation came up as feedback from some users who saw that the tables that were eventually picked by QueryGPT were not correct.
**クエリ生成に使用されるテーブルをユーザが選択できるようにすること**は、QueryGPTによって最終的に選ばれたテーブルが正しくないと感じた一部のユーザからのフィードバックとして提案されました。

To address this feedback, we added another LLM agent (Table Agent) that would pick the right tables and send those out to the user to either “ACK” or edit the given list and set the right tables.
このフィードバックに対処するために、正しいテーブルを選択し、それをユーザに送信して「ACK」または与えられたリストを編集して正しいテーブルを設定できる別のLLMエージェント（テーブルエージェント）を追加しました。
A screenshot of what the user would see is shown below:
ユーザが見ることになるスクリーンショットは以下に示されています。

![Figure 9: Table Agent.](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe5HZ4tiL_nVjtwxiqbzBEliN6R1jI6h5GoGhK0_DGBWp4d46ohXoYpgj0Pcud6Jjz-W3EiwsvH23i-XoyCpTbizCa8xtNEDclrJ8HqMvXiZGgl1OlF_94PdLqons1RdiTBbJxbMYERhVaq-wvxIon-YJRA?key=FDiTashaNIm84IIOQgmW9w)
(チャットUIで、ユーザが質問を投げると、retrieveされた候補テーブルが表示されて、ユーザは短時間表示される"Looks Good"ボタンを押すか、手動でテーブル名を指定できる検索窓に入力できる...!)

The user would either select the “Looks Good” button or edit the existing list and modify the list of tables to be used by the LLM for query generation.
ユーザは「Looks Good」ボタンを選択するか、既存のリストを編集してLLMによるクエリ生成に使用されるテーブルのリストを修正します。

<!-- ここまで読んだ! -->

### Column Prune Agent カラムプルーニングエージェント

Another interesting issue we ran into after rolling QueryGPT out to a larger set of users was the “intermittent” token size issue during query generation for some requests. 
QueryGPTをより多くのユーザーに展開した後に直面したもう一つの興味深い問題は、一部のリクエストにおけるクエリ生成中の「断続的」なトークンサイズの問題でした。
We were using the OpenAI GPT-4 Turbo model with 128K token limit (1106), but were still seeing token limit issues because some requests included one or more tables that each consumed a large amount of tokens. 
私たちは、128Kトークン制限（1106）のOpenAI GPT-4 Turboモデルを使用していましたが、**一部のリクエストにはそれぞれ大量のトークンを消費する1つ以上のテーブルが含まれていたため、トークン制限の問題が依然として発生していました**。(前述されてた大規模スキーマのテーブルの問題かな??)

To address this issue, we implemented a “Column Prune” agent, wherein we use an LLM call to prune the irrelevant columns from the schemas we provided to the LLM. 
この問題に対処するために、私たちは**“Column Prune”エージェント**を実装しました。
("prune"の動詞の意味 = 切る、刈る、切り落とす、剪定する)
**このエージェントでは、LLMに提供したスキーマから無関係なカラムを切り落とすためにLLMコールを使用**します。(ここのモデルも、内製モデルではなくLLMコール...!)

Here’s what the output from the agent looks like: 
エージェントからの出力は次のようになります：

![Figure 10: Column Prune Agent]()

The output would include a skinnier version of each schema that we needed for query generation. 
出力には、クエリ生成に必要な**各スキーマのスリムなバージョン**が含まれます。
This change massively improved not just the token size and by extension the cost of each LLM call, but also reduced the latency since the input size was much smaller. 
**この変更により、トークンサイズだけでなく、各LLM呼び出しのコストも大幅に改善され、入力サイズがはるかに小さくなったため、レイテンシも減少しました**。(あ、これは嬉しいな! ナイス改善...!!)

### Output 出力

No changes were made to the output structure with the current design. 
現在のデザインでは、出力構造に変更はありませんでした。
The response would include a SQL Query and an explanation from the LLM about how the query was generated similar to what’s shown in Figure 7.
応答にはSQLクエリと、クエリがどのように生成されたかについてのLLMからの説明が含まれ、これは図7に示されているものと類似しています。

<!-- ここまで読んだ! -->

## Evaluation 評価

To track incremental improvements in QueryGPT’s performance, we needed a standardized evaluation procedure. 
**QueryGPTのパフォーマンスの漸進的な改善を追跡するために、標準化された評価手順が必要**でした。 (うんうん、継続的改善を果たすために必要だ...!!:thinking:)
This enabled us to differentiate between repeated vs. anomalous shortcomings of the service and ensure algorithm changes were incrementally improving performance in aggregate.
これにより、サービスの繰り返しの欠点と異常な欠点を区別し、アルゴリズムの変更が全体的にパフォーマンスを漸進的に改善していることを確認できました。

### Evaluation Set 評価セット

Curating a set of golden question-to-SQL answer mappings for evaluation required manual upfront investment. 
評価のための**ゴールデンなquestion-to-SQLの回答マッピングのセットを作成するには、手動での事前投資が必要**でした。(まあここは一定頑張ってでも、手動で作る価値があるのかな...!)
We identified a set of real questions from the QueryGPT logs, and manually verified the correct intent, schemas required to answer the question, and the golden SQL.
私たちは、QueryGPTのログから実際の質問のセットを特定し、正しい意図、質問に答えるために必要なスキーマ、およびゴールデンSQLを手動で検証しました。
(最初にText2SQLアプリを導入してから、実用的な良い評価用質問を探してる感じ...??)
The question set covers a variety of datasets and business domains. 
この質問セットは、さまざまなデータセットとビジネスドメインをカバーしています。

### Evaluation Procedure 評価手順

We developed a flexible procedure that can capture signals throughout the query generation process in production and staging environments using different product flows:
私たちは、異なる製品フローを使用して、プロダクションおよびステージング環境におけるクエリ生成プロセス全体で信号をキャッチできる柔軟な手順を開発しました。

- **Vanilla** (これらはテストケースの分類って感じ! 人間から補足情報を受け取るケースと質問だけのケース...!!:thinking:)
  - **Purpose** 目的 
    Measures QueryGPT’s baseline performance. QueryGPT の基本的な性能を測定する。
  - **Procedure** 手順
    - Input a question.  質問を入力する。
    - QueryGPT infers the intent and datasets needed to answer the question.  質問の意図と必要なデータセットを推定する。
    - Generate the SQL using inferred datasets and intent. 推定されたデータセットと意図を使ってSQLを生成する。
    - Evaluate intent, datasets, and SQL. 意図、データセット、SQLをそれぞれ評価する。
- **Decoupled**
  - **Purpose** 目的:  
    Measures QueryGPT performance with the human-in-the-loop experience.  
    Enables component-level evaluation by removing dependencies on performance on earlier outcomes.
    **人間が介在する状態(i.e. 真の値を使う場合)での QueryGPT の性能を測定する**。さらに、前段の結果に依存しないコンポーネント単位の評価を可能にする。
  - **Procedure** 手順:  
    - Input a question, intent, and datasets needed to answer the question.  質問、意図、必要なデータセットを手動で入力する。 
    - QueryGPT infers the intent and datasets. QueryGPT が意図とデータセットを解釈する。 
    - Generate the SQL using the actual (not inferred) intent and datasets. 実際の（推定されたのではない）意図とデータセットを使って SQL を生成する
    - Evaluate intent, datasets, and SQL. 意図、データセット、SQL を評価する
    (あれ、ここで評価されるのはSQLだけじゃないの??)

For each question in the evaluation, we capture the following signals:
評価の各質問に対して、以下の信号をキャッチします：

**Intent**: Is the intent assigned to the question as accurate?
意図：質問に割り当てられた意図は正確ですか？

**Table Overlap**: Are the tables identified via Search + Table Agent correct? This is represented as a score between 0 and 1. 
テーブルの重複：Search + Table Agentを介して特定されたテーブルは正しいですか？これは0から1のスコアで表されます。
For example, if the query needed to answer the questions “How many trips were canceled by drivers last week in Los Angeles?” required the use of [fact_trip_state, dim_city], and QueryGPT identified [dim_city, fact_eats_trip], the Search Overlap Score for this output would be 0.5, because one of the two tables required to answer the question was selected.
例えば、「先週ロサンゼルスでドライバーによってキャンセルされた旅行の数は？」という質問に答えるために[fact_trip_state, dim_city]の使用が必要で、QueryGPTが[dim_city, fact_eats_trip]を特定した場合、この出力のSearch Overlap Scoreは0.5になります。なぜなら、**質問に答えるために必要な2つのテーブルのうち1つが選択されたから**です。

**Successful Run**: Does the generated query run successfully?
成功した実行：生成されたクエリの実行は成功しますか？

**Run Has Output**: Does the query execution return > 0 records. 
出力がある実行：クエリの実行は0件を超えるレコードを返しますか？
(Sometimes, QueryGPT hallucinates filters like WHERE status = “Finished” when, the filter should have been WHERE status = “Completed” resulting in a successful run with no output).
（**時には、QueryGPTがWHERE status = “Finished”のようなフィルターを誤って生成することがあり**ますが、フィルターはWHERE status = “Completed”であるべきで、結果として出力のない成功した実行になります）。

**Qualitative Query Similarity**: How similar is the generated query relative to the golden SQL? 
定性的クエリ類似性：生成されたクエリはゴールデンSQLに対してどれくらい類似していますか？
We use an LLM to assign a similarity score between 0 and 1. 
私たちは**LLMを使用して0から1の間の類似性スコアを割り当てます**。
(ここもLLMコールを使ってる...!:thinking:)
This allows us to quickly see if a generated query that is failing for a syntactic reason is on the right track in terms of columns used, joins, functions applied, etc.
これにより、構文的な理由で失敗している生成されたクエリが、**使用される列、結合、適用される関数などの観点から正しい方向に進んでいるかどうか**を迅速に確認できます。
(うんうん、構文エラーのSQLでも使ってるカラムとか集計方法とかがあってると、このmetricsは高い評価になる...!:thinking:)
---

We visualize progress over time to identify regressions and patterns revealing areas for improvement.
私たちは、進捗を時間の経過とともに可視化し、後退や改善の余地を示すパターンを特定します。

The figure below is an example of question-level run results enabling us to see repeated shortcomings at individual question level.
以下の図は、個々の質問レベルで繰り返される短所を確認できる質問レベルの実行結果の例です。

![Figure 11A: SQL Query Evaluation.]()

![Figure 11B: SQL Query Evaluation across environments.]()

For each question, we can view the generated SQL, reason for the error, and related performance metrics.
各質問について、生成されたSQL、エラーの理由、および関連するパフォーマンスメトリックを確認できます。
Below is a question whose generated query is regularly failing because it is not applying a partition filter in the where clause.
以下は、生成されたクエリがwhere句でパーティションフィルターを適用していないために定期的に失敗している質問です。
However, according to the qualitative LLM-based evaluation, the generated SQL is otherwise similar to the golden SQL.
しかし、定性的なLLMベースの評価によれば、生成されたSQLは他の点ではゴールデンSQLに類似しています。

![Figure 12: SQL Evaluation Stats.]()

We also aggregate accuracy and latency metrics for each evaluation run to track performance over time.
私たちは、各評価実行の精度とレイテンシメトリックを集約し、**時間の経過に伴うパフォーマンスを追跡**します。

![Figure 13: SQL Evaluation criterions.]()

<!-- ここまで読んだ! -->

### Limitations 制限事項 (i.e. 評価における難しいポイントたち...!:thinking:)

Due to the non-deterministic nature of LLMs, running the same evaluation with no changes to the underlying QueryGPT service can result in different outcomes. 
**LLMの非決定論的な性質のため、基盤となるQueryGPTサービスに変更を加えずに同じ評価を実行すると、異なる結果が得られる可能性があります**。(うんうん...!)
In general, we do not over-index decisions based on ~5% run-to-run changes in most metrics. 
一般的に、**私たちはほとんどの指標における約5%の実行間変動**に基づいて決定を過剰にインデックス化することはありません。
(i.e. 5%の変動では嬉しくも悲しくもならないように意識してたよ、って話...!)
Instead, we identify error patterns over longer time periods that can be addressed by specific feature improvements. 
代わりに、特定の機能改善によって対処できるエラーパターンを長期間にわたって特定します。

Uber has hundreds of thousands of datasets with varying levels of documentation. 
Uberには、さまざまな文書化レベルを持つ数十万のデータセットがあります。
Thus, it is impossible for the set of evaluation questions to fully cover the universe of business questions that a user may ask. 
したがって、評価質問のセットがユーザーが尋ねる可能性のあるビジネス質問の全体を完全にカバーすることは不可能です。
Instead, we curated a set of questions that represent the current usage of the product. 
代わりに、私たちは製品の現在の使用状況を表す質問のセットをキュレーションしました。
As we improve accuracy and new bugs arise, the evaluation set will evolve to capture the direction of the product. 
精度を向上させ、**新たなバグが発生するにつれて、評価セットはプロダクトの方向性を捉えるために進化**します。

There is not always one correct answer. 
常に正しい答えが一つだけあるわけではありません。
Often, the same question could be answered by querying different tables or writing queries in different styles. 
しばしば、同じ質問は異なるテーブルをクエリしたり、異なるスタイルでクエリを書いたりすることで回答される可能性があります。
By visualizing the golden vs. returned SQL and using the LLM-based evaluation score, we can understand if the generated query is written in a different style, but has a similar intent related to the golden SQL. 
ゴールデンSQLと返されたSQLを視覚化し、LLMベースの評価スコアを使用することで、生成されたクエリが異なるスタイルで書かれているかどうかを理解できますが、ゴールデンSQLに関連する同様の意図を持っています。

<!-- ここまで読んだ --> 

## Learnings 学び

Working with nascent technologies like GPTs and LLMs over the past year allowed us to experiment and learn a lot of different nuances of how agents and LLMs use data to generate responses to user questions. 
過去1年間、**GPTやLLMのような新興技術を扱うことで、エージェントやLLMがデータを使用してユーザの質問に対する応答を生成する方法のさまざまなニュアンスを実験し、学ぶことができました**。(そうそう、この経験というか学びも、Text2SQLプロジェクトを行うモチベーションの1つになるはずだよね...!!:thinking:)
We’ve briefly described below some of the learnings from our journey: 
私たちの旅から得た学びのいくつかを以下に簡単に説明します：

### LLMs are excellent classifiers LLMは優れた分類器である

Our intermediate agents that we used in QueryGPT to decompose the user’s natural language prompt into better signals for our RAG improved our accuracy a lot from the first version and a lot of it was due to the fact that the LLMs worked really well when given a small unit of specialized work to do.
QueryGPTでユーザの自然言語プロンプトをRAGのためのより良い信号に分解するために使用した**中間エージェントたち**は、Text2SQLの精度を最初のバージョンから大幅に向上させました。その多くは、**LLMが特定の小さな作業単位を与えられたときに非常にうまく機能したため**です。

The intent agent, table agent, and column prune agent each did an excellent job because they were asked to work on a single unit of work rather than a broad generalized task.
**意図エージェント、テーブルエージェント、およびカラムプルーンエージェントは、それぞれが広範な一般化されたタスクではなく、単一の作業単位に取り組むように求められたため、優れた仕事をしました**。

### Hallucinations 幻覚

This remains an area that we are constantly working on, but in a nutshell, we do see instances where the LLM would generate a query with tables that don’t exist or with columns that don’t exist on those tables.
これは私たちが常に取り組んでいる分野であり、要するに、LLMが存在しないテーブルやそのテーブルに存在しないカラムを持つクエリを生成する事例を見ています。

We’ve been experimenting with prompts to reduce hallucinations, introduced a chat style mode where users can iterate on the generated query and are also looking to include a “Validation” agent that recursively tries to fix hallucinations, but this remains an area that we haven’t completely solved yet.
私たちは幻覚を減らすためのプロンプトを試行しており、**ユーザーが生成されたクエリを反復できるチャットスタイルのモードを導入**し、**幻覚を再帰的に修正しようとする「Validation」エージェント**を含めることも検討していますが、**これはまだ完全には解決されていない分野**です。(Uberも頑張ってるが、この問題はまだ解決してない。)

### User prompts are not always “context”-rich ユーザープロンプトは常に「コンテキスト」が豊富とは限らない

Questions entered by the users in QueryGPT ranged from very detailed with the right keywords to narrow the search radius to a 5 word question (with typos) to answer a broad question that would require joins across multiple tables.
QueryGPTに入力されたユーザの質問は、検索範囲を絞るための適切なキーワードを含む非常に詳細なものから、複数のテーブルを結合する必要がある広範な質問に答えるための5語の質問（誤字を含む）まで様々でした。

Solely relying on user questions as “good” input to the LLM caused issues with accuracy and reliability.
**ユーザの質問をLLMへの「良い」入力として単独で頼ることは、精度と信頼性に問題を引き起こしました**。(なるほど...!)
A “prompt enhancer” or “prompt expander” was needed to “massage” the user question into a more context-rich question before we sent those to the LLM.
ユーザの質問をLLMに送る前に、**よりコンテキストが豊富な質問に「マッサージ」するための「プロンプトエンハンサー」または「プロンプトエクスパンダー」が必要でした**。
(これも、必要に応じて追加すべきコンポーネント達だな...! 以前Chuhanさんのブログでも紹介されてた...!:thinking:)

### High bar for SQL output generated by the LLM LLMによって生成されたSQL出力の高い基準

While this version of QueryGPT is helpful for a broad set of personas, there is definitely an expectation from many that the queries produced will be highly accurate and “just work.” 
**このバージョンのQueryGPTは幅広いペルソナにとって役立ち**ますが、生成されるクエリが非常に正確で「そのまま動作する」という期待が多くの人から寄せられています。
The bar is high!
基準は高いです！
(そうそう、今のバージョンでも結構生産性向上には一定寄与すると思うんだよなぁ...)

In our experience, we found that it was best to target and test with the right persona(s) as your initial user base when building a product like this.
私たちの経験では、このようなプロダクトを構築する際には、**最初のユーザーベースとして適切なペルソナをターゲットにし、テストするのが最良である**ことがわかりました。


# Conclusion 結論

The development of QueryGPT at Uber has been a transformative journey, significantly enhancing productivity and efficiency in generating SQL queries from natural language prompts. 
UberにおけるQueryGPTの開発は、自然言語プロンプトからSQLクエリを生成する際の生産性と効率を大幅に向上させる、変革的な旅でした。
Leveraging advanced generative AI models, QueryGPT seamlessly integrates with Uber’s extensive data ecosystem, reducing query authoring time and improving accuracy, addressing both the scale and complexity of our data needs.
高度な生成AIモデルを活用することで、QueryGPTはUberの広範なデータエコシステムとシームレスに統合され、クエリ作成時間を短縮し、精度を向上させ、私たちのデータニーズの規模と複雑さの両方に対処しています。

While challenges such as handling large schemas and reducing hallucinations persist, our iterative approach and constant learning have enabled continuous improvements. 
大規模なスキーマの処理や幻覚の削減といった課題は依然として存在しますが、私たちの反復的なアプローチと継続的な学習により、継続的な改善が可能となっています。
QueryGPT not only simplifies data access but also democratizes it, making powerful data insights more accessible across various teams within Uber.
QueryGPTはデータアクセスを簡素化するだけでなく、それを民主化し、Uber内のさまざまなチームが強力なデータインサイトによりアクセスしやすくしています。

With our limited release to some teams in Operations and Support, we are averaging about 300 daily active users, with about 78% saying that the generated queries have reduced the amount of time they would’ve spent writing it from scratch.
オペレーションおよびサポートの一部のチームへの限定リリースにより、私たちは約300人のデイリーアクティブユーザーを平均しており、そのうち約78%が生成されたクエリがゼロから書くのにかかる時間を短縮したと述べています。

As we look forward, the integration of more sophisticated AI techniques and user feedback will drive further enhancements, ensuring that QueryGPT remains a vital tool in our data platform.
今後を見据えると、より高度なAI技術とユーザーフィードバックの統合がさらなる改善を促進し、QueryGPTが私たちのデータプラットフォームにおいて重要なツールであり続けることを保証します。


<!-- ここまで読んだ! -->

## Acknowledgements 謝辞

QueryGPT was a cross-discipline effort across Uber, requiring expertise and domain knowledge from folks working in Engineering, Product Management and Operations. 
QueryGPTは、Uber全体の学際的な取り組みであり、エンジニアリング、プロダクトマネジメント、オペレーションで働く人々の専門知識とドメイン知識を必要としました。
The product wouldn’t exist today without the great contributions by Abhi Khune, Callie Busch, Jeffrey Johnson, Pradeep Chakka, Saketh Chintapalli, Adarsh Nagesh, Gaurav Paul and Ben Carroll.
この製品は、Abhi Khune、Callie Busch、Jeffrey Johnson、Pradeep Chakka、Saketh Chintapalli、Adarsh Nagesh、Gaurav Paul、Ben Carrollの素晴らしい貢献がなければ、今日存在しなかったでしょう。

Jeffrey Johnson  
Jeffrey Johnson is a Staff Software Engineer on Uber’s Data Platform team. 
Jeffrey Johnsonは、Uberのデータプラットフォームチームのスタッフソフトウェアエンジニアです。
Jeffrey has been primarily focussed on leveraging LLM’s to improve productivity across different personas at Uber and leading security related initiatives for the Business Intelligence team. 
Jeffreyは、Uberのさまざまなペルソナの生産性を向上させるためにLLMを活用し、ビジネスインテリジェンスチームのセキュリティ関連のイニシアチブをリードすることに主に焦点を当てています。

Callie Busch  
Callie Busch is a Software Engineer II on Uber’s Data Platform team. 
Callie Buschは、UberのデータプラットフォームチームのソフトウェアエンジニアIIです。

Abhi Khune  
Abhi Khune is a Principal Engineer on Uber’s Data Platform team. 
Abhi Khuneは、Uberのデータプラットフォームチームのプリンシパルエンジニアです。
For the past 6 months, Abhi has been leading the technical strategy to modernize Uber’s Data Platform to a Cloud-based architecture. 
過去6ヶ月間、AbhiはUberのデータプラットフォームをクラウドベースのアーキテクチャに近代化するための技術戦略をリードしています。

Pradeep Chakka  
Pradeep Chakka is a Senior Software Engineer on Uber’s Data Platform team, based in Dallas, TX. 
Pradeep Chakkaは、テキサス州ダラスに拠点を置くUberのデータプラットフォームチームのシニアソフトウェアエンジニアです。

Posted by Jeffrey Johnson, Callie Busch, Abhi Khune, Pradeep Chakka  
投稿者: Jeffrey Johnson、Callie Busch、Abhi Khune、Pradeep Chakka

