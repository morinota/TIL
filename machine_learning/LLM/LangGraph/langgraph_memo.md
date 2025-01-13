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
