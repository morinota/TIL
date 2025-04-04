## Quick Startメモ

### グラフ定義のざっくりした流れ

- グラフを定義する際の最初のステップは、**グラフの状態(state)を定義する**こと。
  - stateには、スキーマと、**状態更新を処理するreducer関数**が含まれる。
  - reducer関数について。
    - reducerアノテーションのないキーは、以前の値を上書きする。
    - reducer関数`add_messages`がアノテーションとして指定されてる場合、新しい値がlistに追加されていき、上書きされることはない。

```python
class State(TypedDict):
    messages: Annotated[list, add_messages] 
    is_ask_human: bool

graph_builder = StateGraph(State)
```

- 第二のステップとして、ノード(Node)を追加する。
  - **ノードは、作業の単位を表す**。
  - ノードは通常、**stateを受け取りstateを返すPython関数**として定義される。
    - 下の例では、`chatbot`ノード関数は、stateを受け取り、`messages`キーに新しいメッセージをリスト型で指定して返している。これにより、前述の`add_messages`reducer関数が`messages`キーに新しい値を追加してくれるっぽい...!:thinking: 
      - つまり、**ノード関数内で明示的に、state["messages"] + [response] みたいなことをする必要はないっぽい...!**
- ノード関数を定義後、`graph_builder.add_node`メソッドを使って、ノードをグラフに登録する。
  - 第一引数は、ユニークなノード名。
  - 第二引数は、ノードが使われるたびに呼び出される関数orオブジェクト。

```python

llm = ChatOpenAI(model="gpt-4o-mini")

def chatbot(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": [response], "is_ask_human": False}

graph_builder.add_node("chatbot", chatbot)
```

- 第三のステップとして、エントリーポイントとフィニッシュポイントを設定する。
  - エントリーポイントは、**グラフが起動するたびに作業を開始する場所(ノード)**のこと。
    - STARTという特別なノードを使うことで、エントリーポイントを設定できる。
  - フィニッシュポイントは、**このノードが実行されるたびにグラフの作業を終了する場所(ノード)**のこと。
    - ENDという特別なノードを使うことで、フィニッシュポイントを設定できる。

```python
from langgraph.graph import END, START

# STARTノードからchatbotノードへのエッジを追加
graph_builder.add_edge(START, "chatbot")
# chatbotノードからENDノードへのエッジを追加
graph_builder.add_edge("chatbot", END)
```

- 最後のステップとして、グラフを実行できるようにする。
  - グラフビルダーの`compile()`メソッドを呼ぶことで、グラフを実行可能な関数に変換できる。
    - compile()の返り値として、「CompiledGraph」オブジェクトが返される。
    - CompiledGraphオブジェクトは、**stateを入力とした`invoke()`メソッドや`stream()`メソッド**を持つ。
      - チャットボットの例では、ユーザからの入力メッセージをstateに詰めて、`invoke()`メソッドや`stream()`メソッドを呼び出すことで、チャットボットの応答を取得できる。

```python
graph = graph_builder.compile()
```

### グラフにtoolを追加する

- まずLLMに、どんなtoolが利用できるかを知らせる方法として、`bind_tools`メソッドを使う。
  - これにより、**LLMは各種toolを使用したい場合の正しいJSON形式を知る**ことができる。
  - `bind_tools`はtool以外にも色々llmに情報を渡せるっぽいが、今回では、彼らがどんなtoolを呼び出せるかを知るために使われている。

```python
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)
```

- 次に、**toolが呼び出された場合に実際に実行される関数**を作成する。
  - toolは、langchainのtoolデコレーターを使って自前で定義することもできれば、`TavilySearchResults`などの`langchain_community.tools`で事前に定義されたものを使うこともできる。
- tool関数をノードにして、グラフに登録する。
  - 実際には、LangGraph側でpre-buildされた`ToolNode`クラスを使えばよい!!
    - chatbotとは別の、**ツールボックス的なノードを定義**する感じ...!
    - 引数が`tools`なので、1つのtoolで1つのノードではなく、複数のtoolセットに対して1つのノードになるイメージ...!:thinking:

```python
from langchain_community.tools.tavily_search import TavilySearchResults

# TavilySearchResultsを使って、検索用toolを定義
tool = TavilySearchResults(max_results=2)

# ToolNodeクラスを使って、ツールボックス的なノードを定義
tool_node = ToolNode(tools=[tool])
# ツールノードをグラフに登録
graph_builder.add_node("tools", tool_node)
```

### グラフに条件付きエッジを追加する

- エッジは、1つのノードから次のノードへの制御フローをルーティングする。
  - 前述では、グラフビルダーの`add_edge()`メソッドでエントリーポイント`START`と`chatbot`ノードの間にエッジを追加していた。
  - **条件付きエッジは、通常「if」文を含み、現在のグラフ状態に応じて異なるノードにルーティング**する。
- 条件付きエッジを追加するステップ
  - まず、**if文を含むルーティング関数**を定義する。
    - ルーティング関数は、**現在のグラフのstateを入力とし、次に呼び出すノードを示す`str`もしくは`list[str]`を返す**。
  - 次に、グラフビルダーの`add_conditional_edges()`メソッドを呼び出し、ルーティング関数を渡して、条件付きエッジをグラフに登録する。
    - これにより**ソースノードが完了するたびに、グラフはルーティング関数を呼び出し、次に呼び出すノードを決定するようになる**...!
    - 引数:
      - `source`: 条件付きエッジの始点となるノード名
      - `path`: ルーティング関数(グラフのstateを引数にとり、`str`もしくは`list[str]`を返す)
      - `path_map`: ルーティング関数の返り値の`str`に対応する、ノード名のmap。デフォルトでは、恒等関数(i.e. key=valueのmap!)になる。

```python
def route_tools(state: State) -> str | list[str]:
    """
    現在のグラフ状態を受け取り、次に呼び出すノードを示す 文字列or文字列のlist を返す。
    """
    # まずグラフのstateから、条件分岐に必要な情報を取得(この例では、最後のメッセージ)
    if isinstance(state, list):
        # stateをlist形式で定義している場合は、最後尾の要素を取得
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        # stateをdict形式で定義している場合は、messagesキーの最後尾の要素を取得
        ai_message: AIMessage = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    # if文を使って、次に呼び出すノードを決定するロジック
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools" # 次に呼び出すノードを表すstrを返す。
    return END

graph_builder.add_conditional_edges(
    source="chatbot", # 条件付きエッジの始点
    path=route_tools, # ルーティング関数
    path_map={"tools": "tools", END: END}, # ルーティング関数の返り値に対応するノード名のmap
```

- なお、上のコード例では、**state内の最新のAI Messageに`tool_calls`があるか否かで、toolsノードに遷移するかフィニッシュポイントに遷移するかを決定**している。
  - このルーティングのロジックは頻出なので、LangGraphでは`tools_condition`関数として実装ずみ。
  - `tools_condition()`関数は、グラフのstateを引数にとり、最新のAI Messageに`tool_calls`が含まれる場合は、`"tools"`を返し、それ以外の場合は`END`を返す。(まさに上のコード例と振る舞いが同じ関数!:thinking:)
  - もし仮にノード名を`"my_tools"`などにした場合は、path_map引数にて`{"tools": "my_tools", END: END}`と指定すればOK!

### グラフにメモリ(チェックポイント)を追加する

- 前述までの技術で、チャットbotがユーザの質問に答えるためにtoolを使用できるようになった。しかし、以前のやり取りのコンテキストを記憶していない。
- LangGraphは、**永続的なチェックポイント**を使用して、この問題を解決できる。
  - **グラフをコンパイルする際にチェックポインタ(thread_id)を提供し、グラフを呼び出す際にthread_idを指定する**と、LangGraphは各ステップの後に自動的に状態を保存する。
  - 同じthread_idを使用してグラフを再度呼び出すと、**グラフは保存された状態を読み込み、以前のやり取りのコンテキストを維持**できる。
- 後述されるかもだが、チェックポイントは単純なチャットメモリよりもはるかに強力。
  - エラー回復や人間の介入が必要なワークフロー、タイムトラベルインタラクションなどのために、**いつでも複雑な状態を保存して再開できる**...!

- チェックポイントを追加するために、まず**checkpointのクラスをインスタンス化**する。
  - 下のコード例では、in-memoryのcheckpointerである`MemorySaver()`クラスを使っている。(=**全てをメモリ内に保存する!**)
  - **おそらく本番アプリケーションでは、`SqliteSaver()`や`PostgresSaver()`などを使って本番DBに保存することが多いかも**。

```python
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
```

- 次に、チェックポイントをグラフに渡してコンパイルする
  - 具体的には、`checkpointer` 引数にチェックポイントを指定する。
  - グラフの形は変わらない。
  - この指定によって変わったのは、**グラフが各ノードを通過する際にStateをcheckpoint(記録)することだけ**。
    - (各ノードの処理がよばれるたびに、その時点のStateをそれぞれ保存しておくってこと。再利用やエラー時の再開に便利そう...!:thinking:)

```python
graph = graph_builder.compile(checkpointer=memory)
```

- 最後に、グラフの実行時には、stateを記録するためのスレッドを指定するようにする。
  - `config`は、グラフの`invoke()`メソッドや`stream()`メソッドの第二位置引数として指定できる。

```python
config = {"configurable": {"thread_id": "1"}}

events = graph.stream({"messages": [("user", "My name is Will.")]}, config, stream_mode="values")

# やり取りの結果を表示
for event in events:
    event["messages"][-1].pretty_print()
# ================================[1m Human Message [0m=================================
# My name is Will.
# ==================================[1m Ai Message [0m==================================
# Hello Will! It's nice to meet you. How can I assist you today? Is there anything specific you'd like to know or discuss?
```

- 動作確認として、再度グラフを`invoke()`して、前回のコンテキストを覚えているかを確認する
  - (続けて上のコードの下に書く! 今回はメモリ上にcheckpointingしてるので、一回アプリケーションを落とすとメモリが解放されてしまう...! :thinking:)
  - (ちなみに、指定するthread_idを変えると、元のthread_idのメモリは読み込まれないので、名前を覚えていない状態になる...!:thinking_face:)

```python
user_input = "Remember my name?"
events = graph.stream({"messages": [("user", user_input)]}, config, 
streammode="values")

# やり取りの結果を表示
for event in events:
    event["messages"][-1].pretty_print()
# ================================[1m Human Message [0m=================================
# Remember my name?
# ==================================[1m Ai Message [0m==================================
# Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.
```

上記までの技術で、**セッションを跨いでグラフのstateを維持できる**ようになった!
では**checkpointにはどんな情報が保存されている??**

- 指定したconfigに対して、グラフの状態を確認するには、`graph.get_state(config)`メソッドを使う。返り値として`StateSnapshot`オブジェクトが返される。
  - `StateSnapshot`オブジェクトは以下のfieldを持つ。
    - `values`: 現在のグラフのstateを表す。
    - `next`: 次のstateを表す。
      - 最新のstateの`StateSnapshot`オブジェクトの場合は、空。
    - `config`: 設定やsnapshotの関連情報を記録。
    - `metadata`: snapshotのメタデータを記録。(よくわかってない!)
    - `created_at`: snapshotの作成日時を記録。
    - `parent_config`: 親snapshotのconfig。(よくわかってない!)
    - `tasks`: snapshotに関連するタスクのリスト。(よくわかってない!)

```python
# 現在保存されている、グラフのstateを取得
snapshot = graph.get_state(config)
prin(snapshot)

# StateSnapshot(values={'messages': [HumanMessage(content='My name is Will.', additional_kwargs={}, response_metadata={}, id='8c1ca919-c553-4ebf-95d4-b59a2d61e078'), AIMessage(content="Hello Will! It's nice to meet you. How can I assist you today? Is there anything specific you'd like to know or discuss?", additional_kwargs={}, response_metadata={'id': 'msg_01WTQebPhNwmMrmmWojJ9KXJ', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 405, 'output_tokens': 32}}, id='run-58587b77-8c82-41e6-8a90-d62c444a261d-0', usage_metadata={'input_tokens': 405, 'output_tokens': 32, 'total_tokens': 437}), ... 'is_ask_human': False}, thread_id='1')
```

### グラフに、Human-in-the-Loop的に、人間の承認アクションを追加する1

- LangGraphの`interrupt_before`機能を使って、特定のノードの実行時にグラフ実行を中断し、人間の承認アクションを挿入する。
  - 具体的には、グラフのコンパイル時に`interrupt_before`引数を指定すれば良い。

```python
graph = graph_builder.compile(
    checkpointer=memory,
    # toolsノードの実行前に、必ずグラフの実行を中断する
    interrupt_before=["tools"], 
    # interrupt_after=["tools"]
)
```

- 動作確認してみると...

```python
user_input = "I'm learning LangGraph. Could you do some research on it for me?"
config = {"configurable": {"thread_id": "1"}}
events = graph.stream({"messages": [("user", user_input)]}, config, stream_mode="values")

# グラフの一連の実行結果を確認
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
# 以下の出力を見ると、chatbotノードの実行後に、toolsノードが実行される前に、グラフの実行が中断されていることがわかる。

# ================================[1m Human Message [0m=================================

# I'm learning LangGraph. Could you do some research on it for me?
# ==================================[1m Ai Message [0m==================================

# [{'text': "Certainly! I'd be happy to research LangGraph for you. To get the most up-to-date and comprehensive information, I'll use the Tavily search engine to look this up. Let me do that for you now.", 'type': 'text'}, {'id': 'toolu_01R4ZFcb5hohpiVZwr88Bxhc', 'input': {'query': 'LangGraph framework for building language model applications'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]
# Tool Calls:
#   tavily_search_results_json (toolu_01R4ZFcb5hohpiVZwr88Bxhc)
#  Call ID: toolu_01R4ZFcb5hohpiVZwr88Bxhc
#   Args:
#     query: LangGraph framework for building language model applications

# ちなみにsnapshotを取得して、次に実行されるノードを確認すると...
snapshot = graph.get_state(config)
snapshot.next
# >>> ('tools',)

# ちなみにsnapshotから、現在のstateの最後のメッセージを確認すると...
existing_message = snapshot.values["messages"][-1]
existing_message.tool_calls
# [{'name': 'tavily_search_results_json', 'args': {'query': 'LangGraph framework for building language model applications'}, 'id': 'toolu_01R4ZFcb5hohpiVZwr88Bxhc', 'type': 'tool_call'}]
```

- さて、人間の手によって、中断したグラフの実行を再開させてみる。
  - **stateとして`None`を渡すことで、グラフは新しい状態を追加することなく、元の位置から続行する**。
    - Noneは現在のstateに何も追加しないことを意味する。
  - checkpointerを追加済みであれば、グラフは無期限に一時停止でき、いつでも再開できる。

```python
# stream()メソッドにNoneを渡して、現在の状態から再開する
events = graph.stream(None, config, stream_mode="values")

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
# 最初のユーザーのメッセージが再度表示されて...
# その後に、toolsノードの実行結果も表示されて...
# 最終的にフィニッシュポイントに到達する
```

### グラフの状態を、手動で更新する

前述のセクションでは、グラフの実行を中断して、人間の承認アクションを挿入する方法を見た。これで人間はグラフの状態を読み取れる。しかし、**エージェントの進路を変更したい場合は、書き込みアクセスが必要**。

#### `graph.update_state()`で、現在のグラフの状態に手動で新しいメッセージを追加する

- エージェントの進路を変更するには、**checkpointされた状態を更新すれば良い**。
  - まず`graph.get_state(config)`メソッドで、現在のグラフ状態のsnapshotを取得。
  - 新しいメッセージを作成。
  - `graph.update_state()`メソッドを使って、新しいメッセージを現在のstateに追加する。
    - (下のコードの例では、今回定義したstateのmessagesはappend-onlyなので、現在のstateのmessagesは上書きされず、新しいmessageが追加される。`add_messages`アノテーションを指定したやつ!)
      - **`graph.update_state()`メソッドの振る舞いも、stateの状態更新を処理するreducer関数に従うことに注意！**
    - update_state()メソッドは、グラフ内のノードの1つであるかのように、stateを更新する。
      - `as_node`引数に任意のノード名を指定することで、そのノードによってstateが更新されたかのように振る舞うこともできる。

```python
# 前回同様に、toolsノードの実行前にグラフの実行を中断するように、グラフをコンパイル
graph = graph_builder.compile(
    checkpointer=memory,
    interrupt_before=["tools"], 
)

# グラフの実行を開始(toolsノードの実行前に中断される)
user_input = "I'm learning LangGraph. Could you do some research on it for me?"
config = {"configurable": {"thread_id": "1"}}
events = graph.stream({"messages": [("user", user_input)]}, config)

# checkpointされた現在のグラフの状態を取得
snapshot = graph.get_state(config)

# 
answer = "LangGraph is a library for building stateful, multi-actor applications with LLMs."
new_messages = [
    ToolMessage(
        content=answer,
        tool_call_id=existing_message.tool_calls[0]["id"],
    ),
    AIMessage(content=answer),
]

# グラフの現在のstateを更新
# stateの定義で、messagesはadd_messagesアノテーションを指定しているので、既存のmessagesの上書きはされず、新しいmessagesが追加される
graph.update_state(
    config,
    {"messages": new_messages},
)
```

#### append-onlyなstateのmessages属性を上書きする方法!

- stateの定義で、messagesは`add_messages` reducer関数を指定した。なので、append-onlyに新しいメッセージを追加していく振る舞いになってる。この場合に、**既存のメッセージを上書き**するにはどうしたら良い??
  - `add_messages()`の実装の詳細として、`messages`リスト内の各メッセージをIDで管理している。
  - よって、**IDが既存の状態のメッセージと一致する場合、`add_messages` recuder関数は既存のメッセージを新しいコンテンツで上書きする**。

```python
# 現在のグラフのstateを取得
snapshot = graph.get_state(config)
# stateのsnapshotから、最後尾のメッセージを取得
existing_message = snapshot.values["messages"][-1]

# 既存のメッセージを上書きするために、新しいメッセージを作成する
new_tool_call = existing_message.tool_calls[0].copy()
# 例として、AIのツール呼び出しを「LangGraph」から「LangGraph human-in-the-loop workflow」に変更してる...!
new_tool_call["args"]["query"] = "LangGraph human-in-the-loop workflow"
new_message = AIMessage(
    content=existing_message.content, 
    tool_calls=[new_tool_call],
    # 既存のメッセージと同一のIDを指定!!
    id=existing_message.id,
    )

# 現在のstateを更新(同一のIDを指定してるので、メッセージが追加ではなく上書きされる!)
graph.update_state(config, {"messages": [new_message]})

# stream()にNoneを渡して、現在の状態からグラフの実行を再開!
events = graph.stream(None, config, stream_mode="values")
```

### グラフの状態のカスタマイズ(オリジナルの様々なfieldを使う!)

- 上記の例では、シンプルなstate（メッセージのリストだけ）を使った。
  - このシンプルなstateでも十分に多くのことを達成できるが、メッセージリストに依存せずに複雑な動作を定義したい場合は、stateに任意のfieldを追加できる。
- 例: チャットボットが「人間に確認する」という選択肢を持たせる
  - 実現方法の1つは、"human"ノードを作成すること。
    - chatbotノードと、humanノードの間に条件付きエッジを追加し、必要に応じて「人間に確認する」という選択が取れるようにする。
    - このノードの実行時は、常にグラフが中断される。
  - 便宜のために、**`ask_human`というフィールドをグラフのstateに含める。
    - (これを含めるといいことがあるのかは、よくわかってない!このフィールド不要かも??)

- まず、stateに新しいfieldを追加する。

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]  
    ask_human: bool
```

- 次に、llmが「人間に確認する」という選択をとるべきかを決定させるための、スキーマ(?)を定義する。
  - (要するに、toolオブジェクト的なものを定義してるってこと??:thinking:)

```python
from pydantic import BaseModel

class RequestAssistance(BaseModel):
    """
    会話を専門家にエスカレーションします。
    直接支援できない場合や、ユーザーがあなたの権限を超えた支援を必要とする場合に使用します。
    この機能を使用するには、ユーザを中継して、専門家が適切なガイダンスを提供できるようにします。
    """
    request: str
```

- 次にchatbotノードを定義する。
  - bind_tools()メソッドには、ツール定義、pydanticモデル、またはjsonスキーマを含めることができる。(よくわかってない!要するに、llmに「こんなtool達が利用できますよ!」と伝えているイメージ...!:thinking:)

```python
llm = ChatOpenAI(model="gpt-4o-mini")
# RequestAssistanceをtoolsと一緒に、llmにバインドする。
llm_with_tools = llm.bind_tools(tools + [RequestAssistance])

# chatbotノードの実装を定義
def chatbot(state: State)-> State:
    response = llm_with_tools.invoke(state["messages"])
    ask_human = False

    # もし、ツール呼び出しがあって、そのツール呼び出しがRequestAssistanceである場合は、ask_humanをTrueにする
    if (response.tool_calls and response.tool_calls[0]["name"] == RequestAssistance.__name__):
        ask_human = True
    return {
        "messages": [response],
        "ask_human": ask_human
    }
```

- 次に、グラフビルダーを作成し、chatbotノードとtoolノードをグラフに登録する(前回と同様)
  - あ、下のコード例を見ると、toolノードにはRequestAssistanceを含めていない!
    - llmへはtoolsもRequestAssistanceも同様にバインドしているので、llm目線ではどちらも共通のツールボックスに入ってるが、グラフ目線では別々のノードにしてる...!:thinking:

```python
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools)) # あ、toolノードには、RequestAssistanceを含めてないんだ...!:thinking:
```

- 次に、humanノードを定義する。
  - humanノードは、**常にグラフの実行を中断する**。
  - このノードは、**人間が介入する必要がある場合にのみ実行される**。

```python
from langchain_core.messages import AIMessage, ToolMessagefrom langchain_core.messages import AIMessage, ToolMessage

def _create_response(response: str, ai_message: AIMessage):
    return ToolMessage(content=response, tool_call_id=ai_message.tool_calls[0]["id"],)

def human_node(state: State)-> State:
    new_messages = []

    # グラフ実行の中断にユーザが何らかstateを更新した場合、ToolMessageが最後のメッセージになるはず。
    # もしユーザが更新しないことを選択した場合、LLMが続行できるように仮のToolMessageを含める。
    if not isinstance(state["messages"][-1], ToolMessage):
        new_messages.append(_create_response("No response from human.", state["messages"][-1]))
    return {
        "messages": new_messages,
        "ask_human": False,
    }

graph_builder.add_node("human", human_node)
```

- 次に、条件付きエッジを追加する。
  - まずtoolsノード以外の新しい条件分岐ロジックが必要なので、LangGraphの`tools_condition`関数のみでは対応できない。よって、**自前でルーティング関数を定義する必要がある**。

```python
# 条件ロジックを示す、ルーティング関数を定義
def select_next_node(state: State)-> str | list[str]:
    if state["ask_human"]:
        return "human"
    # Otherwise, we can route as before
    return tools_condition(state)

# グラフに条件付きエッジを登録
graph_builder.add_conditional_edges(
    "chatbot", 
    select_next_node, 
    {"human": "human", "tools": "tools", END: END},
)
```

- これで、chatbotが実行を中断して「人間に相談する」必要があるかどうかを自分で決定できるようになった!


### タイムトラベル: LLMアプリケーションの作業を巻き戻して修正などできるようにする!

- LangGraphの組み込み「タイムトラベル」機能を利用する
  - 具体的には、**`graph.get_state_history()`メソッドを使用してcheckpointの遷移を取得**することで、グラフを巻き戻す。
    - グラフの各ノードの遷移によって更新されたstateは、全てcheckpointされているはずなので...!
    - stateのイテラブルを返すっぽい! たぶん最後尾のmessagesから取得されるっぽい!
  - checkpointされた各stateは、それぞれconfigを持っており、その中に**チェックポイントIDのタイムスタンプが含まれている**。
    - **`graph.stream()`メソッドや`graph.invoke()`メソッド実行時に、このcheckpoint_idを指定することで、その時点のstateからグラフの実行を再開できる**


```python
# get_state_history()メソッドを使って、記録されたグラフのstateを順番に取得
for state in graph.get_state_history(config):
    print("Num Messages: ", len(state.values["messages"]), "Next: ", state.next)
    print("-" * 80)
    if len(state.values["messages"]) == 6:
        # We are somewhat arbitrarily selecting a specific state based on the number of chat messages in the state.
        to_replay = state
    
    print(state.config.keys())
    # >>> dict_keys(['thread_id', 'checkpoint_ns', 'checkpoit_id'])

# 特定のcheckpoint_idをconfigに含めて、stream()メソッドを呼ぶことで、その時点のstateからグラフの実行を再開できる
for event in graph.stream(None, to_replay.config, stream_mode="values"):
    if "messages" in event:
        event["messages"][-1].pretty_print()
```

## Text2SQLメモ

参考: https://langchain-ai.github.io/langgraph/tutorials/sql-agent/


## カスタムツールの定義メモ

- 独自のAgentを構築する際には、Agentが利用できるtoolのlistを提供する必要がある。

### toolの構成要素

- 呼び出される実際の関数に加えて、toolはいくつかの構成要素を持つ
  - **name(str)**:
    - 必須。Agentに提供されるtool集合の中で、一意である必要がある。
  - **description(str)**:
    - オプショナルだが推奨。Agentがtoolの使用を判断するために使用される。
  - **args_schema (Pydantic BaseModel)**:
    - オプショナルだが推奨。追加情報(ex. few-shot example)やパラメータの検証のために役立つ。
  - **return_direct(bool)**:
    - オプショナル。Agentにのみ関連する。Trueの場合、与えられたツールを起動したあと、Agentは停止し、結果をユーザに直接返す。

- tips: ツールに適切に選ばれた名前、説明、およびJSONスキーマがあると、モデルのパフォーマンスが向上する

### toolの定義方法

- 関数にtool decoratorを適用する方法
- BaseToolクラスを継承する方法
- StructuredToolデータクラスを使用する方法
- Runnablesからtoolを作成する方法

#### tool decoratorを使う方法

- **`@tool`デコレータは、custom toolを定義する最も簡単な方法**である。
  - デフォルトでは関数名をtool nameとして使用するが、第一引数としてnameを指定することでオーバーライドできる。
  - また、**decorateされた関数のdocstringをdescriptionとして使用する。従って、docstringは必須になる**...!

- 単一の入力値を受け取る関数の例

```python
@tool
def search(query: str) -> str:
    """Look up things online."""
    return "LangChain"

print(search.name)
print(search.description)
print(search.args)
# search
# Look up things online.
# {'query': {'title': 'Query', 'type': 'string'}}
```

- 複数の入力値を受け取る関数の例

```python
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)
# multiply
# Multiply two numbers.
# {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
```

- tool nameやargs_schema引数をカスタマイズする場合

```python
class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    return "LangChain"
```

- @toolデコレータは`parse_docstring`オプションでgoogleスタイルのdocstringを解析し、docstringのコンポーネント(引数の説明など)をtool schemaの関連部分に紐づけることができる。
  - デフォルトでは、@tool(parse_docstring=True)はドキュメンテーション文字列が正しく解析されない場合、ValueErrorを発生させてしまう。
  - 詳細はAPIリファレンスを参照。

```python
@tool(parse_docstring=True)
def foo(bar: str, baz: int) -> str:
    """The foo.
    Args:
        bar: The bar.
        baz: The baz.
    """
    return bar

foo.args_schema.schema()
# {
#     'description': 'The foo.',
#     'properties': {
#         'bar': {'description': 'The bar.', 'title': 'Bar', 'type': 'string'},
#         'baz': {'description': 'The baz.', 'title': 'Baz', 'type': 'integer'}
#     },
#     'required': ['bar', 'baz'],
#     'title': 'fooSchema',
#     'type': 'object'
# }
```

#### BaseToolクラスを継承する方法

- BaseToolクラスをサブクラス化することで、カスタムツールを明示的に定義することもできる。
  - tool decoratorと比較して、より柔軟にcustom toolを定義できる。一方で手間がかかる。

- 単一の入力値を受け取る関数の例

```python
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")

class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"
    args_schema: Type[BaseModel] = SearchInput

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return "LangChain"

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

search = CustomSearchTool()
print(search.name)
print(search.description)
print(search.args)
```

- 複数の入力値を受け取る関数の例

```python
class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

class CustomCalculatorTool(BaseTool):
    name = "Calculator"
    description = "useful for when you need to answer questions about math"
    args_schema: Type[BaseModel] = CalculatorInput
    return_direct: bool = True

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return a * b

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")

multiply = CustomCalculatorTool()
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)
```

#### StructuredToolデータクラスを使用する方法

- この方法は、前の2つ(tools decorator, BaseTool)の中間的な方法。
  - BaseToolを継承する方法よりも簡単で、tool decoratorを使う方法よりも柔軟。

```python
def search_function(query: str)->str:
    return "LangChain"

search = StructuredTool.from_function(
    func=search_function,
    name="Search",
    description="useful for when you need to answer questions about current events",
    # coroutine= ... <- you can specify an async method if desired as well
)

print(search.name)
print(search.description)
print(search.args)
```

- custom args_schemaを定義して、入力に関する詳細情報を提供することもできる。

```python
class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

calculator = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
    # coroutine= ... <- you can specify an async method if desired as well
)

print(calculator.name) 
# >>> Calculator
print(calculator.description) 
# >>> multiply numbers
print(calculator.args) 
# >>> {'a': {'description': 'first number', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}}

```

#### Runnablesからtoolを作成する方法

- 文字列または辞書入力を受け入れる**LangChain Runnables** (=chain的なやつ...??:thinking:)は、as_toolメソッドを使用してツールに変換でき、名前、説明、および引数の追加スキーマ情報を指定できる。

```python
from langchain_core.language_models import GenericFakeChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [("human", "Hello. Please respond in the style of {answer_style}.")]
)

# Placeholder LLM
llm = GenericFakeChatModel(messages=iter(["hello matey"]))
chain = prompt | llm | StrOutputParser()

as_tool = chain.as_tool(
    name="Style responder", description="Description of when to use tool."
)

as_tool.args
{'answer_style': {'title': 'Answer Style', 'type': 'string'}}
```

### toolのエラーハンドリング

- toolがエラーに遭遇し、例外がキャッチされない場合、agentは実行を停止する。
- Agentに実行を継続させたい場合は、`ToolException`をraiseさせ、`handle_tool_error`を適切に設定できる。
  - `ToolException`がthrowされると、Agentは作業を停止せず、toolの`handle_tool_error`変数にしたがって例外を処理し、処理結果がobservationとしてagentに返される。
    - (`ToolException`を発生させるだけでは意味がなく、`handle_tool_error`変数を適切に設定しないと、エラーが発生した際にAgentが停止してしまう...!!:thinking:)
- `handle_tool_error`変数について
  - bool型やstr型、関数として設定ができる。
    - 関数として設定されている場合は、その関数は`ToolException`を引数として受け取り、str型を返す必要がある。
  - デフォルト値は`False`

- もし`handle_tool_error`を設定しない場合はどうなる?? (i.e. `handle_tool_error=False`)

```python
from langchain_core.tools import ToolException

def search_tool1(s: str):
    raise ToolException("The search tool1 is not available.")

search = StructuredTool.from_function(
    func=search_tool1,
    name="Search_tool1",
    description="A bad tool",
)
search.run("test")

>>> ToolException   Traceback (most recent call last)
>>> ToolException: The search tool1 is not available.
...
```

- 次に、`handle_tool_error`をTrueに設定してみる

```python
search = StructuredTool.from_function(
    func=search_tool1,
    name="Search_tool1",
    description="A bad tool",
    handle_tool_error=True,
)
search.run("test")

>>> 'The search tool1 is not available.'  # 処理が停止せず、エラーが処理されていることがわかる
```

- また、`handle_tool_error`に、tool errorを処理するcustom関数を定義する場合
  
```python
def _handle_error(error: ToolException) -> str:
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
        + "Please try another tool."
    )

search = StructuredTool.from_function(
    func=search_tool1,
    name="Search_tool1",
    description="A bad tool",
    handle_tool_error=_handle_error,
)
search.run("test")

>>> 'The following errors occurred during tool execution:The search tool1 is not available.Please try another tool.' # 処理が停止せず、エラーが処理されていることがわかる
```

### 非同期(async)なtoolの作成方法

- 前提として、LangChainツールはRunnableインターフェースの実装である。そして、**全てのRunnableはinvokeおよびainvokeメソッド(およびbatch、abatch、astreamなどの他のメソッド)を公開**している。
- なのでtoolも同期処理の実装のみでも、ainvokeメソッドを使用できるが、注意すべき重要なことがある。
  - LangChainはデフォルトで、関数の計算にコストがかかると仮定して非同期実装を提供しており、そのため、実行を別のスレッドに委任する
  - なので、同期ツールではなく非同期ツールを作成する方が効率的。
    - **同期および非同期の両方の実装が必要な場合は、StructuredTool.from_functionを使用するか、BaseToolからサブクラス化する必要がある**。
      - ex. BaseToolの場合は、`def _run()`メソッドと`async def _arun()`メソッドの両方を実装する。
      - ex. StructuredToolの場合は、`func`引数に同期関数、`coroutine`引数に非同期関数を指定する。

### ツール実行の成果物を返す(結構使いそう!)

- 時には、**ツールの実行の成果物があり、それをチェーンやエージェントの下流コンポーネントではアクセス可能にしたいが、モデル自体には公開したくない場合**がある。
  - (うんうん、ありそう...!A/Bテストmetricsの実数値とか...!:thinking:)
  - ex. ツールがカスタムオブジェクト、データフレーム、画像、音声などを出力するときに、出力に関するメタデータはモデルに渡したいが、実際の出力は渡したくないケース。

- ToolおよびToolMessageインターフェースは、**ツール出力のモデル向けの部分（これはToolMessage.contentです）と、モデル外で使用するための部分（ToolMessage.artifact）を区別する**ことを可能にする
  - toolが message contentと他のartifactsを区別可能にするには、toolを定義する際に`response_format="content_and_artifact"`を指定し、`(content, artifact)`のタプルを返すようにする必要がある。
    - 詳細はtoolのAPI referenceを参照
- 例:

```python
import random
from typing import List, Tuple
from langchain_core.tools import tool

@tool(response_format="content_and_artifact")
def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
    """Generate size random ints in the range [min, max]."""
    array = [random.randint(min, max) for _ in range(size)]
    content = f"Successfully generated array of {size} random ints in [{min}, {max}]."
    return content, array

# ツールを直接呼び出すと、出力のコンテンツ部分のみが返される
generate_random_ints.invoke({"min": 0, "max": 9, "size": 10})

>>> 'Successfully generated array of 10 random ints in [0, 9].'

# もしtoolをToolCall（tool-callingモデルによって生成されるもの）で呼び出すと、toolが生成したcontentとartifactの両方を含むToolMessageが返される
generate_random_ints.invoke(
    {
        "name": "generate_random_ints",
        "args": {"min": 0, "max": 9, "size": 10},
        "id": "123",  # required
        "type": "tool_call",  # required
    }
)

>>> ToolMessage(content='Successfully generated array of 10 random ints in [0, 9].', name='generate_random_ints', tool_call_id='123', artifact=[4, 8, 2, 4, 1, 0, 9, 5, 8, 1])
```

## Langgraphにおける`graph.stream()`メソッドと`graph.invoke()`メソッドの違い

### invoke()メソッド:

- グラフ全体を一気に実行して、最終結果を返す。

```python
result = graph.invoke({"input": "ギャルのSQLを教えて"})
print(result)
# → 最終ノードまで実行した「最終結果」だけが返ってくる
```

### stream()メソッド:

- 各ステップの出力をストリーム(逐次)で返す。
  - もし LangGraph を Streamlit とかに組み込んで チャット風UIにしたいケースは、こっちを採用して「逐次表示」にしたほうがUX良さそう。

```python
for step in graph.stream({"input": "ギャルのSQLを教えて"}):
    print(step)
```
- 上記実装の説明:
  - `step`には、ノードごとの中間出力が順番に入ってくる。
    - 「どんな経路をたどったか」と「途中の出力内容」をリアルタイムで取得できる。

- `stream`で返ってくる`step`の中身は大体こんな感じ:
  - `stream_mode="values"`オプションを指定すると、出力stateのdictだけが返されるっぽい!!
    - dictはより詳細には`langgraph.pregel.io.AddableValuesDict`型らしい。

```python
{
  "{対象のノード名}": {
    "state_key1": "state_value1",
    "state_key2": "state_value2",
    ...
  },  # そのノードの出力stateをdict形式に変換したものがvalueに入るっぽい!
}
```

関数でwrapするならyieldとかを使う感じになりそう。例えば以下。

```python
def stream_response(user_input: str)-> Iterator[str]:
    for step in graph.stream({"input": user_input}):
        output = step.get("output")
        if isinstance(output, dict):
            yield output.get("response", str(output))
        else:
            yield str(output)
```
