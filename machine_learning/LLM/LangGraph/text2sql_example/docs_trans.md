https://langchain-ai.github.io/langgraph/tutorials/sql-agent/

# An agent for interacting with a SQL database¶ SQLデータベースと対話するエージェント

In this tutorial, we will walk through how to build an agent that can answer questions about a SQL database. 
このチュートリアルでは、SQLデータベースに関する質問に答えることができるエージェントの構築方法を説明します。

At a high level, the agent will: 
高レベルでは、エージェントは以下のことを行います：

1. Fetch the available tables from the database 
1. データベースから利用可能なテーブルを取得します。

2. Decide which tables are relevant to the question 
2. 質問に関連するテーブルを決定します。

3. Fetch the DDL for the relevant tables 
3. 関連するテーブルのDDL（データ定義言語）を取得します。

4. Generate a query based on the question and information from the DDL 
4. 質問とDDLからの情報に基づいてクエリを生成します。

5. Double-check the query for common mistakes using an LLM 
5. LLM（大規模言語モデル）を使用して、一般的な間違いがないかクエリを再確認します。

6. Execute the query and return the results 
6. クエリを実行し、結果を返します。

7. Correct mistakes surfaced by the database engine until the query is successful 
7. クエリが成功するまで、データベースエンジンによって浮上した間違いを修正します。

8. Formulate a response based on the results 
8. 結果に基づいて応答を形成します。

The end-to-end workflow will look something like below: 
エンドツーエンドのワークフローは以下のようになります：

## Setup セットアップ

First let's install our required packages and set our API keys
まず、必要なパッケージをインストールし、APIキーを設定しましょう。

```
%%capture--no-stderr%pipinstall-Ulanggraphlangchain_openailangchain_community
```

```
importgetpassimportosdef_set_env(key:str):ifkeynotinos.environ:os.environ[key]=getpass.getpass(f"{key}:")_set_env("OPENAI_API_KEY")
```

Set up LangSmith for LangGraph development
LangGraph開発のためにLangSmithを設定します。

Sign up for LangSmith to quickly spot issues and improve the performance of your LangGraph projects. 
LangSmithにサインアップして、問題を迅速に特定し、LangGraphプロジェクトのパフォーマンスを向上させましょう。

LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph — read more about how to get started here.
LangSmithを使用すると、LangGraphで構築したLLMアプリをデバッグ、テスト、監視するためにトレースデータを利用できます — こちらで始める方法について詳しく読むことができます。

<!-- ここまで読んだ! -->

## Configure the database データベースの設定

We will be creating a SQLite database for this tutorial. 
このチュートリアルでは、SQLiteデータベースを作成します。

SQLite is a lightweight database that is easy to set up and use. 
SQLiteは、セットアップと使用が簡単な軽量データベースです。

We will be loading the chinook database, which is a sample database that represents a digital media store. 
デジタルメディアストアを表すサンプルデータベースであるchinookデータベースを読み込みます。

Find more information about the database here. 
データベースに関する詳細情報はここで確認できます。

For convenience, we have hosted the database (Chinook.db) on a public GCS bucket. 
便宜上、データベース（Chinook.db）を公共のGCSバケットにホストしています。

```python
import requests
url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
response = requests.get(url)
if response.status_code == 200:
    # Open a local file in binary write mode
    with open("Chinook.db", "wb") as file:
        # Write the content of the response (the file) to the local file
        file.write(response.content)
    print("File downloaded and saved as Chinook.db")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
```

```
File downloaded and saved as Chinook.db
```

We will use a handy SQL database wrapper available in the langchain_community package to interact with the database. The wrapper provides a simple interface to execute SQL queries and fetch results. We will also use the langchain_openai package to interact with the OpenAI API for language models later in the tutorial.
**langchain_communityパッケージで利用可能な便利なSQLデータベースラッパーを使用して、データベースと対話**します。このラッパーは、SQLクエリを実行して結果を取得するためのシンプルなインターフェースを提供します。また、後でチュートリアルで言語モデルのOpenAI APIと対話するためにlangchain_openaiパッケージを使用します。

```
%%capture --no-stderr --no-display
!pip install langgraph langchain_community langchain_openai
```

```python
from langchain_community.utilities import SQLDatabase
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")
```

API Reference: SQLDatabase
```
sqlite['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
```

```
"[(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains'), (6, 'Antônio Carlos Jobim'), (7, 'Apocalyptica'), (8, 'Audioslave'), (9, 'BackBeat'), (10, 'Billy Cobham')]"
```

<!-- ここまで読んだ! -->


## Utility functions ユーティリティ関数

We will define a few utility functions to help us with the agent implementation. 
エージェントの実装を助けるために、いくつかのユーティリティ関数を定義します。 

Specifically, we will wrap aToolNode with a fallback to handle errors and surface them to the agent.
具体的には、エラーを処理し、それをエージェントに表示するために、ToolNodeをフォールバックでラップします。

```python
from typing import Any
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from langgraph.prebuilt import ToolNode

# ToolNodeを作成する。
# with_fallbacksってなんだ??
def create_tool_node_with_fallback(tools: list) -> RunnableWithFallbacks[Any, dict]:
    """Create a ToolNode with a fallback to handle errors and surface them to the agent."""
    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\nplease fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }
```

API Reference: ToolMessage | RunnableLambda | RunnableWithFallbacks | ToolNode
APIリファレンス: ToolMessage | RunnableLambda | RunnableWithFallbacks | ToolNode

<!-- ここまで読んだ! -->

## Define tools for the agent¶ エージェントのためのツールの定義

We will define a few tools that the agent will use to interact with the database.  
エージェントがデータベースと対話するために使用する**いくつかのツールを定義**します。

1. `list_tables_tool`: Fetch the available tables from the database  
   1. list_tables_tool: データベースから利用可能なテーブルを取得します。
2. `get_schema_tool`: Fetch the DDL for a table  
   2. get_schema_tool: テーブルのDDLを取得します。
3. `db_query_tool`: Execute the query and fetch the results OR return an error message if the query fails  
   3. db_query_tool: クエリを実行し、結果を取得するか、クエリが失敗した場合はエラーメッセージを返します。

For the first two tools, we will grab them from the SQLDatabaseToolkit, also available in the langchain_community package.  
**最初の2つのツールは、SQLDatabaseToolkitから取得します。これは、langchain_communityパッケージでも利用可能**です。(最初の二つのツールは、自前で実装しなくて良いってことか)

```python
from langchain_community.agent_toolkits import SQLDatabaseToolkit  
from langchain_openai import ChatOpenAI  

toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(model="gpt-4o"))  
tools = toolkit.get_tools()
# pre-buildのtool関数達を取得
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")  
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")  

print(list_tables_tool.invoke(""))  
print(get_schema_tool.invoke("Artist"))  
```

API Reference: SQLDatabaseToolkit | ChatOpenAI  
APIリファレンス: SQLDatabaseToolkit | ChatOpenAI

```
Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track  
CREATE TABLE "Artist" ("ArtistId" INTEGER NOT NULL, "Name" NVARCHAR(120), PRIMARY KEY ("ArtistId"))  
/*3 rows from Artist table:  
ArtistId    Name  
1   AC/DC  
2   Accept  
3   Aerosmith*/  
```

The third will be defined manually. For the db_query_tool, we will execute the query against the database and return the results.
3番目のツールは手動で定義します。db_query_toolの場合、データベースに対してクエリを実行し、結果を返します。

```python
from langchain_core.tools import tool  

@tool  
def db_query_tool(query: str) -> str:
    """Execute a SQL query against the database and get back the result.  
    If the query is not correct, an error message will be returned.  
    If an error is returned, rewrite the query, check the query, and try again.""" 
    result = db.run_no_throw(query)  
    if not result:  
        return "Error: Query failed. Please rewrite your query and try again."  
    return result

print(db_query_tool.invoke("SELECT * FROM Artist LIMIT 10;"))  
```

```
[(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains'), (6, 'Antônio Carlos Jobim'), (7, 'Apocalyptica'), (8, 'Audioslave'), (9, 'BackBeat'), (10, 'Billy Cobham')]  
```

While not strictly a tool, we will prompt an LLM to check for common mistakes in the query and later add this as a node in the workflow.
厳密にはツールではありませんが、**クエリの一般的な間違いをチェックするためにLLMにプロンプトを表示し、後でこれをワークフローのノードとして追加**します。

```python
from langchain_core.prompts import ChatPromptTemplate  

query_check_system = """You are a SQL expert with a strong attention to detail.  
Double check the SQLite query for common mistakes, including:  
- Using NOT IN with NULL values  
- Using UNION when UNION ALL should have been used  
- Using BETWEEN for exclusive ranges  
- Data type mismatch in predicates  
- Properly quoting identifiers  
- Using the correct number of arguments for functions  
- Casting to the correct data type  
- Using the proper columns for joins  
If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.  
You will call the appropriate tool to execute the query after running this check."""  

query_check_prompt = ChatPromptTemplate.from_messages([("system", query_check_system), ("placeholder", "{messages}")])  
query_check = query_check_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([db_query_tool], tool_choice="required")  
query_check.invoke({"messages": [("user", "SELECT * FROM Artist LIMIT 10;")]})  
```

```
AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_la8JTjHox6P1VjTqc15GSgdk', 'function': {'arguments': '{"query":"SELECT * FROM Artist LIMIT 10;"}', 'name': 'db_query_tool'}, 'type': 'function'}], 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 20, 'prompt_tokens': 221, 'total_tokens': 241}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_a2ff031fb5', 'finish_reason': 'stop', 'logprobs': None}, id='run-dd7873ef-d2f7-4769-a5c0-e6776ec2c515-0', tool_calls=[{'name': 'db_query_tool', 'args': {'query': 'SELECT * FROM Artist LIMIT 10;'}, 'id': 'call_la8JTjHox6P1VjTqc15GSgdk', 'type': 'tool_call'}], usage_metadata={'input_tokens': 221, 'output_tokens': 20, 'total_tokens': 241})
```

<!-- ここまで読んだ! -->

## Define the workflow¶ ワークフローの定義

We will then define the workflow for the agent. 
次に、エージェントのワークフローを定義します。
The agent will first force-call the list_tables_tool to fetch the available tables from the database, then follow the steps mentioned at the beginning of the tutorial.
エージェントはまず、データベースから利用可能なテーブルを取得するために `list_tables_tool` を強制的に呼び出し、その後、チュートリアルの最初に述べた手順に従います。

```python
from typing import Annotated, Literal
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import AnyMessage, add_messages

# グラフのstateを定義
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# グラフビルダーを定義
workflow = StateGraph(State)

# エントリーポイントにつながる、最初に必ず呼び出されるノード関数を定義
def first_tool_call(state: State) -> State:
    return {
        "messages": [
            AIMessage(content="", tool_calls=[{"name": "sql_db_list_tables", "args": {}, "id": "tool_abcd123",}]),
        ]
    }

# クエリが正しいかどうかを実行するツールを定義
def model_check_query(state: State) -> dict[str, list[AIMessage]]:
    """Use this tool to double-check if your query is correct before executing it."""
    return {
        "messages": [query_check.invoke({"messages": [state["messages"][-1]]})]
    }

# グラフビルダーに、定義したノードたちを登録していく
workflow.add_node("first_tool_call", first_tool_call)
# tool関数は、ToolNodeにwrapしてから登録
workflow.add_node("list_tables_tool", create_tool_node_with_fallback([list_tables_tool]))
workflow.add_node("get_schema_tool", create_tool_node_with_fallback([get_schema_tool]))

# Add a node for a model to choose the relevant tables based on the question and available tables
# 質問と利用可能なテーブル一覧を元に関連テーブルを選ぶ、モデルのノードを追加
model_get_schema = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([get_schema_tool])
workflow.add_node("model_get_schema", lambda state: {"messages": [model_get_schema.invoke(state["messages"])],})

# 終了状態を表すツールを記述
class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""
    final_answer: str = Field(..., description="The final answer to the user")

# 質問と、関連テーブルのスキーマを元にクエリを生成するモデルのノードを追加
query_gen_system = """You are a SQL expert with a strong attention to detail. Given an input question, output a syntactically correct SQLite query to run, then look at the results of the query and return the answer. DO NOT call any tool besides SubmitFinalAnswer to submit the final answer. When generating the query: Output the SQL query that answers the input question without a tool call. Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results. You can order the results by a relevant column to return the most interesting examples in the database. Never query for all the columns from a specific table, only ask for the relevant columns given the question. If you get an error while executing a query, rewrite the query and try again. If you get an empty result set, you should try to rewrite the query to get a non-empty result set. NEVER make stuff up if you don't have enough information to answer the query... just say you don't have enough information. If you have enough information to answer the input question, simply invoke the appropriate tool to submit the final answer to the user. DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database."""
query_gen_prompt = ChatPromptTemplate.from_messages([("system", query_gen_system), ("placeholder", "{messages}")])
query_gen = query_gen_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([SubmitFinalAnswer])

def query_gen_node(state: State)-> State:
    message = query_gen.invoke(state)
    # Sometimes, the LLM will hallucinate and call the wrong tool. We need to catch this and return an error message.
    tool_messages = []
    if message.tool_calls:
        for tc in message.tool_calls:
            if tc["name"] != "SubmitFinalAnswer":
                tool_messages.append(ToolMessage(content=f"Error: The wrong tool was called: {tc['name']}. Please fix your mistakes. Remember to only call SubmitFinalAnswer to submit the final answer. Generated queries should be outputted WITHOUT a tool call.", tool_call_id=tc["id"],))
    else:
        tool_messages = []
    return {"messages": [message] + tool_messages}

workflow.add_node("query_gen", query_gen_node)

# クエリを実行する前に、モデルがクエリをチェックするノードを登録
workflow.add_node("correct_query", model_check_query)

# クエリを実行するノードを登録
workflow.add_node("execute_query", create_tool_node_with_fallback([db_query_tool]))

# 条件付きエッジを登録するための、ルーティング関数を定義
def should_continue(state: State) -> Literal[END, "correct_query", "query_gen"]:
    messages = state["messages"]
    last_message = messages[-1]
    # If there is a tool call, then we finish
    if getattr(last_message, "tool_calls", None):
        return END
    if last_message.content.startswith("Error:"):
        return "query_gen"
    else:
        return "correct_query"

# エッジを登録
workflow.add_edge(START, "first_tool_call")
workflow.add_edge("first_tool_call", "list_tables_tool")
workflow.add_edge("list_tables_tool", "model_get_schema")
workflow.add_edge("model_get_schema", "get_schema_tool")
workflow.add_edge("get_schema_tool", "query_gen")
workflow.add_conditional_edges("query_gen", should_continue,)
workflow.add_edge("correct_query", "execute_query")
workflow.add_edge("execute_query", "query_gen")

# ワークフローを実行できるようにコンパイル
app = workflow.compile()
```

## Run the agent エージェントの実行

```python
# invoke()メソッドに、最初のstateを渡して、グラフを実行
messages = app.invoke(
    {"messages": [("user", "2009年に最も売上を上げた営業担当者は誰ですか？")]}
)
# 最後のメッセージのツールコールから、最終的な回答を取得
json_str = messages["messages"][-1].tool_calls[0]["args"]["final_answer"]
json_str

# '2009年に最も売上を上げた営業担当者はスティーブ・ジョンソンで、総売上は164.34です。'
```


```python
# グラフの実行状況を、逐次的に確認
for event in app.stream(
    {"messages": [("user", "Which sales agent made the most in sales in 2009?")]}
):
    print(event)
```

<!-- ここまで読んだ! -->

## Eval 評価

Now, we can evaluate this agent! 
さて、私たちはこのエージェントを評価することができます！

We previously defined simple SQL agent as part of our LangSmith evaluation cookbooks, and evaluated responses to 5 questions about our database. 
私たちは以前、LangSmith評価クックブックの一部としてシンプルなSQLエージェントを定義し、**データベースに関する5つの質問への応答を評価**しました。(ベンチマークか!)
We can compare this agent to our prior one on the same dataset. 
私たちはこのエージェントを同じデータセット上の以前のエージェントと比較することができます。
Agent evaluation can focus on 3 things: 
**エージェントの評価は3つの点に焦点を当てることができます**:

- **Response**: The inputs are a prompt and a list of tools. The output is the agent response.応答：入力はプロンプトとツールのリストです。出力はエージェントの応答です。
- **Single tool**: As before, the inputs are a prompt and a list of tools. The output the tool call. 単一ツール：以前と同様に、入力はプロンプトとツールのリストです。出力はツールの呼び出しです。
- **Trajectory**: As before, the inputs are a prompt and a list of tools. The output is the list of tool calls. 軌跡：以前と同様に、入力はプロンプトとツールのリストです。出力はツールの呼び出しのリストです。

![]()

### Response

We'll evaluate end-to-end responses of our agent relative to reference answers.
私たちは、エージェントのエンドツーエンドの応答を参照回答に対して評価します。
Let's run response evaluation on the same dataset. 
同じデータセットで応答評価を実行しましょう。

```python
import json

def predict_sql_agent_answer(example: dict)-> dict:
    """Use this for answer evaluation
    クエリを入力として受け取り、LLMアプリケーションが回答を作り、最終的な回答を返す
    """
    # Arrange
    msg = {"messages": ("user", example["input"])}

    # Act
    messages = app.invoke(msg)

    # Assert
    json_str = messages["messages"][-1].tool_calls[0]["args"]
    response = json_str["final_answer"]
    return {"response": response}
```

```python
from langchain import hub
from langchain_openai import ChatOpenAI

grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")

def answer_evaluator(run, example) -> dict:
    """A simple evaluator for RAG answer accuracy
    クエリに対する正解とエージェントの回答を入力として受け取り、最終的に評価スコアを返す
    """
    # Get question, ground truth answer, chain
    input_question = example.inputs["input"]
    reference = example.outputs["output"]
    prediction = run.outputs["response"]

    # LLM grader
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    # Structured prompt
    answer_grader = grade_prompt_answer_accuracy | llm

    # Run evaluator
    score = answer_grader.invoke({"question": input_question, "correct_answer": reference, "student_answer": prediction,})
    score = score["Score"]
    return {"key": "answer_v_reference_score", "score": score}
```

(langsmithにevaluate()メソッドっていうのがあるっぽい。これを使うとLLM-as-judgeが楽に実装できるのか??:thinking_face:)

```python
from langsmith.evaluation import evaluate

dataset_name = "SQL Agent Response"
try:
    experiment_results = evaluate(predict_sql_agent_answer, data=dataset_name, evaluators=[answer_evaluator], num_repetitions=3, experiment_prefix="sql-agent-multi-step-response-v-reference", metadata={"version": "Chinook, gpt-4o multi-step-agent"},)
except:
    print("Please setup LangSmith")
```

<!-- ここまで読んだ! -->

### Trajectory 軌道

Let's run trajectory evaluation on this same dataset.
この同じデータセットで軌道評価を実行しましょう。

```python
# これらは、エージェントが使用することを期待しているtool達。
expected_trajectory = [
    "sql_db_list_tables",  # first: list_tables_tool node
    "sql_db_schema",  # second: get_schema_tool node
    "db_query_tool",  # third: execute_query node
    "SubmitFinalAnswer",
]  # fourth: query_gen
```

```python
def predict_sql_agent_messages(example: dict):
    """Use this for answer evaluation"""
    msg = {"messages": ("user", example["input"])}
    messages = app.invoke(msg)
    return {"response": messages}
```

```python
from langsmith.schemas import Example, Run

def find_tool_calls(messages)-> list:
    """
    返されたメッセージ内のすべてのツールコールを取得する
    """
    tool_calls = [tc["name"] for tc in messages["messages"] for m in getattr(tc, "tool_calls", [])]
    return tool_calls

def contains_all_tool_calls_in_order_exact_match(root_run: Run, example: Example) -> dict:
    """
    すべての期待されるツールが正確な順序で呼び出され、追加のツールコールがないことを保証するテストケース
    """
    expected_trajectory = ["sql_db_list_tables", "sql_db_schema", "db_query_tool", "SubmitFinalAnswer",]
    messages = root_run.outputs["response"]
    tool_calls = find_tool_calls(messages)
    # Print the tool calls for debugging
    print("Here are my tool calls:")
    print(tool_calls)
    # Check if the tool calls match the expected trajectory exactly
    if tool_calls == expected_trajectory:
        score = 1
    else:
        score = 0
    return {"score": int(score), "key": "multi_tool_call_in_exact_order"}

def contains_all_tool_calls_in_order(root_run: Run, example: Example) -> dict:
    """
    全ての期待されるツールが順番に呼び出されるか確認しますが、期待されるツールの間に他のツールが呼び出されることを許可するテストケース。
    """
    messages = root_run.outputs["response"]
    tool_calls = find_tool_calls(messages)
    # Print the tool calls for debugging
    print("Here are my tool calls:")
    print(tool_calls)
    it = iter(tool_calls)
    if all(ele in it for ele in expected_trajectory):
        score = 1
    else:
        score = 0
    return {"score": int(score), "key": "multi_tool_call_in_order"}
```

```python
try:
    # なるほど。langsmithのevaluate()関数で、前述で定義したテストケースたちをいい感じに評価できるのか...!:thinking_face:
    experiment_results = evaluate(
        predict_sql_agent_messages,
        data=dataset_name,
        evaluators=[contains_all_tool_calls_in_order, contains_all_tool_calls_in_order_exact_match,],
        num_repetitions=3,
        experiment_prefix="sql-agent-multi-step-tool-calling-trajectory-in-order",
        metadata={"version": "Chinook, gpt-4o multi-step-agent"},
    )
except:
    print("Please setup LangSmith")
```


The aggregate scores show that we never correctly call the tools in exact order:
集計スコアは、私たちがツールを正確な順序で呼び出すことができなかったことを示しています。
Looking at the logging, we can see something interesting -
ログを見ていると、興味深いことがわかります -

```
['sql_db_list_tables', 'sql_db_schema', 'sql_db_query', 'db_query_tool', 'SubmitFinalAnswer']
```

We appear to inject a hallucinated tool call, sql_db_query, into our trajectory for most of the runs.
私たちは、ほとんどの実行で軌道に幻覚のツールコールであるsql_db_queryを注入しているようです。
This is why multi_tool_call_in_exact_order fails, but multi_tool_call_in_order still passes.
これが、multi_tool_call_in_exact_orderが失敗する理由ですが、multi_tool_call_in_orderはまだ通過する理由です。
We will explore ways to resolve this using LangGraph in future cookbooks!
今後のクックブックでは、これを解決する方法をLangGraphを使用して探求します！

<!-- ここまで読んだ! -->
