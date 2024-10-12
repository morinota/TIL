## link リンク

- https://huyenchip.com/2023/04/11/llm-engineering.html#part_2_task_composability https://huyenchip.com/2023/04/11/llm-engineering.html#part_2_task_composability

# Part 2. Task composability パート2 タスクコンポーザビリティ

## Applications that consist of multiple tasks 複数のタスクからなるアプリケーション

The example controversy scorer above consists of one single task: given an input, output a controversy score.
上記の論争スコアラーの例は、入力が与えられたら論争スコアを出力するという1つのタスクで構成されています。
Most applications, however, are more complex.
しかし、ほとんどのアプリケーションはもっと複雑です。
Consider the “talk-to-your-data” use case where we want to connect to a database and query this database in natural language.
データベースに接続し、そのデータベースに自然言語で問い合わせるという「talk-to-your-data」ユースケースを考えてみましょう。
Imagine a credit card transaction table.
クレジットカードの取引テーブルをイメージしてください。
You want to ask things like: "How many unique merchants are there in Phoenix and what are their names?" and your database will return: "There are 9 unique merchants in Phoenix and they are …".
などと聞いてみたいものです： 「フェニックスには何人のユニークな商店があり、その名前は何ですか」と尋ねると、データベースは次のように返します： "Phoenixには9つのユニークマーチャントがあり、それらは... "となります。

One way to do this is to write a program that performs the following sequence of tasks:
その一つの方法として、次のような一連の作業を行うプログラムを作成することができます：

- Task 1: convert natural language input from user to SQL query [LLM] タスク1：ユーザーからの自然言語入力をSQLクエリに変換する【LLM

- Task 2: execute SQL query in the SQL database [SQL executor] タスク2：SQLデータベースでSQLクエリを実行する[SQLエクゼキュータ]。

- Task 3: convert the SQL result into a natural language response to show user [LLM] タスク3：SQLの結果を自然言語レスポンスに変換してユーザーに見せる【LLM

## Agents, tools, and control flows エージェント、ツール、コントロールフロー

I did a small survey among people in my network and there doesn’t seem to be any consensus on terminologies, yet.
私のネットワークの中で小さなアンケートを取ったのですが、用語に関するコンセンサスはまだ得られていないようです。

The word agent is being thrown around a lot to refer to an application that can execute multiple tasks according to a given control flow (see Control flows section).
エージェントという言葉は、与えられた制御フロー（制御フローの項を参照）に従って複数のタスクを実行することができるアプリケーションを指す言葉として、盛んに使われています。
A task can leverage one or more tools.
タスクは、1つまたは複数のツールを活用することができます。
In the example above, SQL executor is an example of a tool.
上記の例では、SQL executorがツールの一例です。

Note: some people in my network resist using the term agent in this context as it is already overused in other contexts (e.g.agent to refer to a policy in reinforcement learning).
注：私のネットワークでは、エージェントという言葉をこの文脈で使うことに抵抗がある人もいます。他の文脈ではすでに使い古されているからです（例えば、強化学習におけるポリシーを指すエージェントなど）。

### Tools vs. plugins ツール vs. プラグイン

Other than SQL executor, here are more examples of tools:
SQL executor以外のツールの例を挙げます：

search (e.g.by using Google Search API or Bing API)
検索（例：Google Search APIやBing APIを利用した検索など）

web browser (e.g.given a URL, fetch its content)
ウェブブラウザ

bash executor
バッシュエグゼキュータ

calculator
計算機

Tools and plugins are basically the same things.
ツールとプラグインは基本的に同じものです。
You can think of plugins as tools contributed to the OpenAI plugin store.
プラグインとは、OpenAIのプラグインストアに投稿されたツールのことだと考えてください。
As of writing, OpenAI plugins aren’t open to the public yet, but anyone can create and use tools.
執筆時点では、OpenAIプラグインはまだ公開されていませんが、誰でもツールを作って使うことができます。

### Control flows: sequential, parallel, if, for loop 制御フロー：逐次、並列、if、forループ

In the example above, sequential is an example of a control flow in which one task is executed after another.
上記の例では、シーケンシャルとは、あるタスクが次々と実行される制御フローの例です。
There are other types of control flows such as parallel, if statement, for loop.
制御の流れには、他にも並列、if文、forループなどの種類があります。

Sequential: executing task B after task A completes, likely because task B depends on Task A.
順次：タスクAが完了した後にタスクBを実行する。タスクBがタスクAに依存しているためと考えられる。
For example, the SQL query can only be executed after it’s been translated from the user input.
例えば、SQLクエリは、ユーザー入力から翻訳された後でなければ実行できません。

Parallel: executing tasks A and B at the same time.
並列：タスクAとBを同時に実行すること。

If statement: executing task A or task B depending on the input.
If文：入力に応じて、タスクAまたはタスクBを実行する。

For loop: repeat executing task A until a certain condition is met.
Forループ：ある条件が満たされるまで、タスクAの実行を繰り返す。
For example, imagine you use browser action to get the content of a webpage and keep on using browser action to get the content of links found in that webpage until the agent feels like it’s got sufficient information to answer the original question.
例えば、ブラウザのアクションでウェブページのコンテンツを取得し、エージェントが元の質問に答えるのに十分な情報を得たと感じるまで、ブラウザのアクションでそのウェブページで見つかったリンクのコンテンツを取得し続けることを想像してみてください。

Note: while parallel can definitely be useful, I haven’t seen a lot of applications using it.
注：パラレルは確かに便利ですが、それを使ったアプリケーションをあまり見たことがありません。

### Control flow with LLM agents LLMエージェントによる制御フロー

In traditional software engineering, conditions for control flows are exact.
従来のソフトウェア工学では、制御フローの条件は厳密なものでした。
With LLM applications (also known as agents), conditions might also be determined by prompting.
LLMアプリケーション（エージェントとも呼ばれる）では、プロンプトによって条件を決定することもある。

For example, if you want your agent to choose between three actions search, SQL executor, and Chat, you might explain how it should choose one of these actions as follows (very approximate), In other words, you can use LLMs to decide the condition of the control flow!
例えば、エージェントに検索、SQL実行、Chatの3つのアクションを選択させたい場合、どのようにこれらのアクションの1つを選択すべきかを次のように説明します（非常に近似しています）。 つまり、LLMを使って制御フローの条件を決めることができるのです！

```
You have access to three tools: Search, SQL executor, and Chat.

Search is useful when users want information about current events or products.

SQL executor is useful when users want information that can be queried from a database.

Chat is useful when users want general information.

Provide your response in the following format:

Input: { input }
Thought: { thought }
Action: { action }
Action Input: { action_input }
Observation: { action_output }
Thought: { thought }
```

### Testing an agent エージェントのテスト

For agents to be reliable, we’d need to be able to build and test each task separately before combining them.
エージェントの信頼性を高めるためには、各タスクを個別に構築してテストしてから組み合わせることが必要です。
There are two major types of failure modes:
故障モードは大きく分けて2種類あります：

One or more tasks fail.
1つまたは複数のタスクが失敗した。
Potential causes:
想定される原因

Control flow is wrong: a non-optional action is chosen
制御フローがおかしい：非選択的なアクションが選択される

One or more tasks produce incorrect results
1つまたは複数のタスクが不正な結果を出す

All tasks produce correct results but the overall solution is incorrect.
すべてのタスクが正しい結果を出すが、全体の解答は正しくない。
Press et al.(2022) call this “composability gap”: the fraction of compositional questions that the model answers incorrectly out of all the compositional questions for which the model answers the sub-questions correctly.
Pressら(2022)はこれを「コンポーザビリティ・ギャップ」と呼び、モデルが小問に正解するすべてのコンポーザル問題のうち、モデルが不正解になるコンポーザル問題の割合を示している。

Like with software engineering, you can and should unit test each component as well as the control flow.
ソフトウェア工学のように、制御フローだけでなく、各コンポーネントをユニットテストすることができますし、そうすべきです。
For each component, you can define pairs of (input, expected output) as evaluation examples, which can be used to evaluate your application every time you update your prompts or control flows.
各コンポーネントについて、（入力、期待出力）のペアを評価例として定義し、プロンプトやコントロールフローを更新するたびに、アプリケーションの評価に利用することが可能です。
You can also do integration tests for the entire application.
また、アプリケーション全体の統合テストを行うことも可能です。