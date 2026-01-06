## CHAPTER 12: Agents and LLM Workflows 第12章: エージェントとLLMワークフロー

LLM workflows and agents are easy to spot, as they are AI-powered services that provide a natural language API. 
LLMワークフローとエージェントは、自然言語APIを提供するAI駆動のサービスであるため、見分けるのは簡単です。

The first LLM-powered chatbots were simple wrappers for LLMs. 
最初のLLM駆動のチャットボットは、LLMのシンプルなラッパーでした。

But they couldn’t answer questions on any event that happened after their training cutoff date. 
しかし、彼らはトレーニングのカットオフ日以降に起こったイベントに関する質問には答えられませんでした。

So they rapidly evolved into the complex multistep engines that can answer questions on even today’s events, using vector indexes, search engines, feature stores, and other data sources to add context information to prompts. 
そのため、彼らは急速に進化し、ベクトルインデックス、検索エンジン、フィーチャーストア、その他のデータソースを使用してプロンプトにコンテキスト情報を追加し、今日のイベントに関する質問にも答えられる複雑なマルチステップエンジンになりました。

With the help of tools and new protocols, LLM workflows have transmogrified into agents that have a level of autonomy in how to plan and execute tasks to achieve goals. 
ツールと新しいプロトコルの助けを借りて、LLMワークフローは、目標を達成するためにタスクを計画し実行する方法において自律性を持つエージェントに変貌しました。

Agents are more than just LLM wrappers. 
エージェントは単なるLLMラッパー以上のものです。

They can use external tools, they have memory, and they can plan strategies to achieve goals. 
彼らは外部ツールを使用でき、メモリを持ち、目標を達成するための戦略を計画できます。

Agents are mostly interactive services, but there are also background agents that execute tasks autonomously, automating routine tasks such as workflow execution, process optimization, and proactive maintenance. 
エージェントは主にインタラクティブなサービスですが、ワークフローの実行、プロセスの最適化、プロアクティブなメンテナンスなどのルーチン作業を自動的に実行するバックグラウンドエージェントも存在します。

In this chapter, we will descend the rabbit hole of building LLM workflows and agents. 
この章では、LLMワークフローとエージェントの構築の深淵に降りていきます。

We will learn the art of context engineering, providing as much context and prior knowledge as possible for every interaction with an LLM. 
私たちは、LLMとのすべてのインタラクションに対して、できるだけ多くのコンテキストと事前知識を提供するコンテキストエンジニアリングの技術を学びます。

For this, you may need to query diverse data sources (vector indexes, search engines, feature stores, etc.), call external APIs, and even use other agents. 
そのためには、さまざまなデータソース（ベクトルインデックス、検索エンジン、フィーチャーストアなど）にクエリを実行し、外部APIを呼び出し、他のエージェントを使用する必要があるかもしれません。

We will also introduce two protocols—Model Context Protocol (MCP) and Agent-to-Agent (A2A)—that standardize access to diverse tools and agents, respectively. 
また、さまざまなツールとエージェントへのアクセスを標準化する2つのプロトコル、モデルコンテキストプロトコル（MCP）とエージェント間（A2A）を紹介します。

Standardized protocols make it possible for agents to discover and use tools and other agents at runtime—one challenge with current LLMs is their limited planning capabilities. 
標準化されたプロトコルにより、エージェントはランタイムでツールや他のエージェントを発見し使用することが可能になります。現在のLLMの課題の1つは、計画能力が限られていることです。

We will also look at LLM workflow patterns, such as routing, to constrain the autonomy granted to agents to ensure they deliver something useful. 
また、エージェントに与えられる自律性を制約し、役立つものを提供することを保証するために、ルーティングなどのLLMワークフローパターンを見ていきます。

Finally, as agents are software components, we will look at a software development process to iteratively develop and deploy agents. 
最後に、エージェントはソフトウェアコンポーネントであるため、エージェントを反復的に開発および展開するためのソフトウェア開発プロセスを見ていきます。

We will cover testing and monitoring of agents later in Chapters 13 and 14.  
エージェントのテストと監視については、後の第13章と第14章で取り上げます。  
-----
###### From LLMs to Agents LLMからエージェントへ

The first chatbots that worked with LLMs combined a user query with the chatbot’s system prompt. 
LLMと連携した最初のチャットボットは、ユーザーのクエリとチャットボットのシステムプロンプトを組み合わせました。

The system prompt helped responses follow expected guidelines by saying things like “Be a helpful chat assistant and don’t be evil.” 
システムプロンプトは、「役に立つチャットアシスタントになり、悪事を働かないでください」といったことを言うことで、期待されるガイドラインに従った応答を助けました。

The combined system prompt and user query was sent to the LLM, and the LLM response was output to the client. 
結合されたシステムプロンプトとユーザーのクエリはLLMに送信され、LLMの応答がクライアントに出力されました。

Quickly, it became clear that LLMs could not answer questions about anything that happened after their training cutoff time. 
すぐに、LLMはトレーニングのカットオフ時間以降に起こったことに関する質問には答えられないことが明らかになりました。

For example, in July 2025, if I asked who won the NBA championship in 2025, the LLM would not have been able to answer correctly. 
例えば、2025年7月に「2025年のNBAチャンピオンは誰か」と尋ねた場合、LLMは正しく答えることができなかったでしょう。

Retrieval-augmented generation (RAG) was introduced as a way to dynamically add examples retrieved at query time to the system prompt. 
リトリーバル拡張生成（RAG）は、クエリ時に取得された例をシステムプロンプトに動的に追加する方法として導入されました。

The first RAG implementations used the user query to retrieve similar chunks of text from a vector index. 
最初のRAG実装では、ユーザーのクエリを使用してベクトルインデックスから類似のテキストチャンクを取得しました。

Figure 12-1 shows an LLM RAG architecture with a vector index. 
図12-1は、ベクトルインデックスを持つLLM RAGアーキテクチャを示しています。

_Figure 12-1. RAG with a vector index, a prompt template, and an LLM._  
-----
For RAG to work, you need to regularly update the vector index with new data. 
RAGが機能するためには、定期的に新しいデータでベクトルインデックスを更新する必要があります。

A vector-embedding pipeline updates the vector index with text, which is first chunked and then encoded with an embedding model: 
ベクトル埋め込みパイプラインは、テキストをチャンク化し、次に埋め込みモデルでエンコードすることで、ベクトルインデックスを更新します。

1. Chunking involves splitting text documents into smaller chunks. 
1. チャンク化は、テキストドキュメントを小さなチャンクに分割することを含みます。

2. A vector embedding is then computed independently for each chunk using an embedding model. 
2. 次に、埋め込みモデルを使用して各チャンクに対して独立してベクトル埋め込みが計算されます。

3. The vector embeddings are stored in a vector index for later retrieval. 
3. ベクトル埋め込みは、後で取得するためにベクトルインデックスに保存されます。

A client uses the vector index to retrieve chunks to add to the system prompt: 
クライアントは、システムプロンプトに追加するためのチャンクを取得するためにベクトルインデックスを使用します。

1. The user query is fed through the same embedding model to produce a vector (or query) embedding. 
1. ユーザーのクエリは、同じ埋め込みモデルを通じて処理され、ベクトル（またはクエリ）埋め込みが生成されます。

2. You send your query embedding to the vector index and retrieve the k most similar chunks of text. 
2. クエリ埋め込みをベクトルインデックスに送信し、最も類似したk個のテキストチャンクを取得します。

3. You augment the prompt by adding the returned chunks to the prompt template. 
3. 返されたチャンクをプロンプトテンプレートに追加することで、プロンプトを拡張します。

4. You generate a response by sending the prompt (query and examples) to the LLM. 
4. プロンプト（クエリと例）をLLMに送信することで、応答を生成します。

I use the term _vector index instead of_ _vector database, as I cannot assume you are using a vector database. 
私は「ベクトルデータベース」を使用しているとは限らないため、「ベクトルインデックス」という用語を使用します。

There are an increasing number of databases that support similarity search over vector embeddings, including relational databases, document stores, graph databases, etc. 
リレーショナルデータベース、ドキュメントストア、グラフデータベースなど、ベクトル埋め込みに対する類似検索をサポートするデータベースが増えています。

For our RAG system to answer our question on who won the NBA championship in 2025, I would need to add a document to the vector index with that information and hope (remember, similarity search is probabilistic!) that the relevant document chunk containing the answer is returned and included in the system prompt. 
私たちのRAGシステムが「2025年のNBAチャンピオンは誰か」という質問に答えるためには、その情報を含むドキュメントをベクトルインデックスに追加し、関連するドキュメントチャンクが返されてシステムプロンプトに含まれることを期待する必要があります（類似検索は確率的であることを忘れないでください！）。

The LLM would then leverage in-context learning to answer the question about the NBA winner by using the example document chunks included in the prompt. 
その後、LLMはプロンプトに含まれる例のドキュメントチャンクを使用してNBAの勝者に関する質問に答えるために、インコンテキスト学習を活用します。

There are many challenges related to building a reliable RAG AI system with a vector database, including what text to encode, how large chunk sizes should be, and how to handle nondeterministic chunk retrieval. 
ベクトルデータベースを使用して信頼性の高いRAG AIシステムを構築する際には、どのテキストをエンコードするか、チャンクサイズはどのくらいにすべきか、非決定的なチャンク取得をどのように処理するかなど、多くの課題があります。

RAG has moved beyond vector indexes to also include web search. 
RAGはベクトルインデックスを超えて、ウェブ検索も含むようになりました。

Modern chatbots can answer questions about recent events through retrieving web search results and adding them to the prompt as examples. 
現代のチャットボットは、ウェブ検索結果を取得し、それを例としてプロンプトに追加することで、最近のイベントに関する質問に答えることができます。

In other words, LLM chatbots have moved quickly from only having the user query to adding context information to the prompt at query time from a variety of data sources.  
言い換えれば、LLMチャットボットは、ユーザーのクエリだけを持つ状態から、さまざまなデータソースからクエリ時にプロンプトにコンテキスト情報を追加する状態に迅速に移行しました。  
-----
But what happens when you want to move beyond chatbots and build agents that perform tasks? 
しかし、チャットボットを超えてタスクを実行するエージェントを構築したい場合はどうなりますか？

For example, if you design a coding agent to write a program, you may want the agent to write code using a programming language API that the LLM was not trained on. 
例えば、プログラムを書くためのコーディングエージェントを設計する場合、LLMがトレーニングされていないプログラミング言語APIを使用してコードを書くようにエージェントに求めるかもしれません。

You will need to add multiple examples of how the API is used to the system prompt for the LLM to reliably generate code that uses the API. 
LLMがAPIを使用するコードを信頼性高く生成するためには、APIの使用方法の複数の例をシステムプロンプトに追加する必要があります。

Few-shot prompting is important when you want to show an LLM behavior that you want it to imitate. 
少数ショットプロンプティングは、LLMに模倣してほしい動作を示したいときに重要です。

Agents are more complex than the first generation of RAG LLM applications, as they have a level of autonomy and can take actions. 
エージェントは、ある程度の自律性を持ち、行動を取ることができるため、最初の世代のRAG LLMアプリケーションよりも複雑です。

Figure 12-2 shows an agent architecture that: 
図12-2は、次のようなエージェントアーキテクチャを示しています。

- Uses external APIs/services/databases as a _tool via the MCP. Each tool provides_ an MCP-compliant server to handle requests and return results. 
- MCPを介して外部API/サービス/データベースをツールとして使用します。各ツールは、リクエストを処理し結果を返すMCP準拠のサーバーを提供します。

- Makes calls to one or more LLMs with a prompt (created from a prompt template it manages for the LLM task in question) that may also include context retrieved via an MCP server (using RAG). 
- 1つまたは複数のLLMにプロンプト（該当するLLMタスクのために管理されるプロンプトテンプレートから作成された）を使用して呼び出しを行い、MCPサーバーを介して取得されたコンテキスト（RAGを使用）を含む場合もあります。

- Logs its calls to tools and LLM queries as traces. 
- ツールへの呼び出しとLLMクエリをトレースとして記録します。

- Exposes its capabilities via the A2A protocol, which standardizes communications between agents, improving their interoperability. 
- A2Aプロトコルを介してその機能を公開し、エージェント間の通信を標準化し、相互運用性を向上させます。

The MCP protocol provides a generic mechanism for an agent to access any external service or RAG data sources as a tool. 
MCPプロトコルは、エージェントが任意の外部サービスやRAGデータソースにツールとしてアクセスするための一般的なメカニズムを提供します。

The agent can ask a tool what actions it can execute. 
エージェントは、ツールにどのようなアクションを実行できるかを尋ねることができます。

Tools execute actions and return the result of their actions to the agent. 
ツールはアクションを実行し、その結果をエージェントに返します。

An agent, in its purest form, takes the user query and asks the LLM which available tool it should execute. 
エージェントは、その最も純粋な形で、ユーザーのクエリを受け取り、どの利用可能なツールを実行すべきかをLLMに尋ねます。

It executes the tool and includes the tool response as context in the LLM’s prompt, asking the LLM if it should use another tool or return a response to the client. 
ツールを実行し、ツールの応答をLLMのプロンプトのコンテキストとして含め、LLMに別のツールを使用すべきか、クライアントに応答を返すべきかを尋ねます。

In this view of agents, they have complete autonomy in producing results, but later in this chapter, we will look at techniques, such as workflows, that restrict the agent’s autonomy in this planning step. 
このエージェントの見方では、彼らは結果を生成する際に完全な自律性を持っていますが、この章の後半では、エージェントの自律性を制約するワークフローなどの技術を見ていきます。

The agent has an API, standardized with the A2A protocol, that is not limited to a user query string. 
エージェントは、ユーザーのクエリ文字列に限定されないA2Aプロトコルで標準化されたAPIを持っています。

It can be extended to include application context for queries (such as IDs for users, articles, sessions, etc.). 
それは、クエリのアプリケーションコンテキスト（ユーザー、記事、セッションなどのIDなど）を含むように拡張できます。

Agents can use these IDs to retrieve application activity and state from the feature store. 
エージェントは、これらのIDを使用してフィーチャーストアからアプリケーションのアクティビティと状態を取得できます。

For example, an ecommerce agent can retrieve recent orders for a user, because queries from the application can include the userID as context. 
例えば、eコマースエージェントは、アプリケーションからのクエリにユーザーIDをコンテキストとして含めることができるため、ユーザーの最近の注文を取得できます。  
-----
_Figure 12-2. Agentic architecture that uses LLMs and tools (a vector index, external services, and a feature store) via MCP to add context to prompts. Agent trace logs are stored for error analysis, and Agent APIs are exposed via the A2A protocol._  
図12-2. LLMとツール（ベクトルインデックス、外部サービス、フィーチャーストア）を使用してプロンプトにコンテキストを追加するエージェントアーキテクチャ。エージェントトレースログはエラー分析のために保存され、エージェントAPIはA2Aプロトコルを介して公開されます。  

In the following sections, we will go through the main components of this agentic architecture from designing prompts and developing agent programs in LlamaIndex to RAG with vector indexes, RAG with a feature store, and RAG with a graph database, MCP, and A2A protocols. 
次のセクションでは、プロンプトの設計やLlamaIndexでのエージェントプログラムの開発から、ベクトルインデックスを使用したRAG、フィーチャーストアを使用したRAG、グラフデータベース、MCP、およびA2Aプロトコルを使用したRAGまで、このエージェントアーキテクチャの主要なコンポーネントを見ていきます。  
###### Prompt Management プロンプト管理

When you use a chatbot, such as ChatGPT, it will provide its own system prompt and append your query to that system prompt. 
ChatGPTのようなチャットボットを使用すると、チャットボットは独自のシステムプロンプトを提供し、あなたのクエリをそのシステムプロンプトに追加します。

The system prompt defines how an LLM should behave. 
システムプロンプトは、LLMがどのように振る舞うべきかを定義します。

For chatbots, this includes instructions such as to be helpful and polite, avoid speculative answers, be clear about your limitations, protect privacy, use styles for responses, and avoid opinions and promotion. 
チャットボットにとって、これは役に立ち、礼儀正しく、推測的な回答を避け、限界を明確にし、プライバシーを保護し、応答のスタイルを使用し、意見や宣伝を避けるといった指示を含みます。

Claude’s system prompt in mid-2025 is 16,739 words long (or 110 KB). 
2025年中頃のClaudeのシステムプロンプトは16,739語（または110KB）です。

However, Claude is more than a chatbot; it has a reputation as a high-quality coding assistant. 
しかし、Claudeは単なるチャットボット以上のものであり、高品質なコーディングアシスタントとしての評判があります。

Roughly two-thirds of its system prompt is dedicated to tool definitions for MCP, search instructions, and artifact instructions. 
そのシステムプロンプトの約3分の2は、MCPのツール定義、検索指示、およびアーティファクト指示に割り当てられています。

As a designer of LLM workflows and agents, you will have to write a system prompt for every task your agent performs. 
LLMワークフローとエージェントの設計者として、エージェントが実行する各タスクのためにシステムプロンプトを書く必要があります。

You will also have to design the enclosing prompt template that includes the: 
また、次の内容を含む囲むプロンプトテンプレートを設計する必要があります。

_System prompt_ The task description, including any examples and placeholders for any examples that will be retrieved at query time using RAG 
_システムプロンプト_ タスクの説明、RAGを使用してクエリ時に取得される例やプレースホルダーを含む

_User prompt_ The user query 
_ユーザープロンプト_ ユーザーのクエリ

_Assistant prompt_ The response 
_アシスタントプロンプト_ 応答

The prompt template can be defined in a markup language, called the prompt format (or chat template). 
プロンプトテンプレートは、プロンプトフォーマット（またはチャットテンプレート）と呼ばれるマークアップ言語で定義できます。

OpenAI developed an internal format, ChatML, as a markup language with three roles: system, user, and assistant: 
OpenAIは、システム、ユーザー、アシスタントの3つの役割を持つマークアップ言語として、内部フォーマットChatMLを開発しました。

<|system|> 
You are a helpful assistant. 
<|system|> 
あなたは役に立つアシスタントです。

<|user|> 
What’s the capital of France? 
<|user|> 
フランスの首都はどこですか？

<|assistant|> 
The capital of France is Paris. 
フランスの首都はパリです。

DeepSeek-V3 uses the same ChatML format as OpenAI. 
DeepSeek-V3はOpenAIと同じChatMLフォーマットを使用しています。

With multimodal LLMs, you need additions to the markup format to support images and other file formats. 
マルチモーダルLLMでは、画像やその他のファイル形式をサポートするためにマークアップフォーマットに追加が必要です。



. With multimodal LLMs, you need additions to the markup format to support images and other file formats. 
マルチモーダルLLMを使用する場合、画像やその他のファイル形式をサポートするためにマークアップ形式に追加が必要です。

For example, the Llama 4 prompt format enables users to define up to five images in the prompt. 
例えば、Llama 4のプロンプト形式では、ユーザーがプロンプト内で最大5つの画像を定義できるようになっています。

In this snippet, we ask the LLM to describe in two sentences the image enclosed between <|image_start|> and <|image_end|> tags: 
このスニペットでは、LLMに<|image_start|>と<|image_end|>タグで囲まれた画像を2文で説明するように依頼します：

<|begin_of_text|><|header_start|>user<|header_end|>  
<|image_start|><|image|><|patch|>...<|patch|><|image_end|>  
Describe this image in two sentences<|eot|>  
<|header_start|>assistant<|header_end|>  
The image depicts a dog standing on a skateboard….  
その画像は、スケートボードの上に立っている犬を描写しています…。

The response comes after the assistant word in the header tags. 
応答は、ヘッダータグ内のアシスタントの単語の後に続きます。

The preceding example is for a small image. 
前述の例は、小さな画像に関するものです。

Llama 4’s [chat template syntax also includes tile separator](https://oreil.ly/dYHWp) tokens for larger images and support for multiple image tags when you upload more than one image.  
Llama 4の[チャットテンプレート構文には、大きな画像用のタイルセパレーター](https://oreil.ly/dYHWp)トークンが含まれており、複数の画像をアップロードする際に複数の画像タグをサポートします。

-----
When you build an LLM agent, you will design your own prompt template for every LLM interaction supported by your agent. 
LLMエージェントを構築する際には、エージェントがサポートするすべてのLLMインタラクションのために独自のプロンプトテンプレートを設計します。

You can leverage open source frameworks such as LlamaIndex and Comet ML’s Opik to help manage your prompts. 
プロンプトを管理するために、LlamaIndexやComet MLのOpikなどのオープンソースフレームワークを活用できます。

In the following LlamaIndex example, the prompt template is called ChatPromptTemplate, and it includes both the system prompt (SystemMessage) loaded from a file (versioned in a source code repository) and the user query (UserMessage) provided as a parameter (user_input). 
以下のLlamaIndexの例では、プロンプトテンプレートはChatPromptTemplateと呼ばれ、ファイルから読み込まれたシステムプロンプト（SystemMessage）と、パラメータ（user_input）として提供されるユーザークエリ（UserMessage）の両方が含まれています。

This example also shows how to conditionally instantiate a different prompt and model depending on whether the target LLM is Mistral or a Llama model: 
この例では、ターゲットLLMがMistralかLlamaモデルかに応じて、異なるプロンプトとモデルを条件付きでインスタンス化する方法も示しています：

```  
from llama_index.prompts import ChatPromptTemplate, SystemMessage, UserMessage  
def load_system_prompt(filepath: str) -> str:  
    with open(filepath, "r", encoding="utf-8") as f:  
        return f.read().strip()  
def get_prompt_template(model_name: str) -> ChatPromptTemplate:  
    if model_name.startswith("mistral"):  
        system_prompt = load_system_prompt("mistral_system.txt")  
    elif model_name.startswith("llama"):  
        system_prompt = load_system_prompt("llama_system.txt")  
    return ChatPromptTemplate(  
        messages=[  
            SystemMessage(content=system_prompt),  
            UserMessage(content="{user_input}")  
        ]  
    )  
def get_model(model_name: str):  
    if model_name.startswith("llama"):  
        return TogetherLLM(model=f"meta-llama/{model_name}")  
    elif model_name.startswith("mistral"):  
        return MistralAI(model="mistral-large-latest")  
if __name__ == "__main__":  
    model_name = "llama-3-70b-chat-hf" # or "mistral-large-latest"  
    user_input = "What are the main differences between LlamaIndex and LangGraph?"  
    prompt_template = get_prompt_template(model_name)  
    messages = prompt_template.format_messages(user_input=user_input)  
    model = get_model(model_name)  
    response = model.chat(messages).message.content  
    print("Response:\n", response)  
```  
The preceding code is committed to a source code repository, and the prompt is versioned as a file along with the code. 
前述のコードはソースコードリポジトリにコミットされており、プロンプトはコードと共にファイルとしてバージョン管理されています。

An alternative approach is to version your prompts in a data platform, for example, using the Opik library. 
別のアプローチとして、データプラットフォームでプロンプトをバージョン管理する方法があります。例えば、Opikライブラリを使用することです。

In the following example code, the prompt is saved to an Opik server and then downloaded by the client when needed: 
以下の例のコードでは、プロンプトがOpikサーバーに保存され、必要に応じてクライアントによってダウンロードされます：



import opik
prompt = opik.Prompt( # Saves this Prompt to the Opik Server
name="MLFS Prompt",
prompt="Hi {{name}}. Welcome to {{location}}. How can I assist you today?"
)
client = opik.Opik() # Download a prompt with an Opik client
prompt = client.get_prompt(name="MLFS Prompt")
formatted_prompt = prompt.format(name="Alice", location="Wonderland")
```
```md
import opik
prompt = opik.Prompt( # このプロンプトをOpikサーバーに保存します
name="MLFS Prompt",
prompt="こんにちは{{name}}。{{location}}へようこそ。今日はどのようにお手伝いできますか？"
)
client = opik.Opik() # Opikクライアントでプロンプトをダウンロードします
prompt = client.get_prompt(name="MLFS Prompt")
formatted_prompt = prompt.format(name="Alice", location="Wonderland")
```

The benefits of storing versioned prompts in a data platform are easier governance, analytics, and search for prompts.
データプラットフォームにバージョン管理されたプロンプトを保存する利点は、ガバナンス、分析、およびプロンプトの検索が容易になることです。

Source code repositories are fine for versioning prompts when you’re getting started, and if you later have enterprise requirements, you can move to manage prompts as artifacts in a data platform.
ソースコードリポジトリは、始めたばかりのときにプロンプトのバージョン管理には適していますが、後に企業の要件がある場合は、データプラットフォームでアーティファクトとしてプロンプトを管理することに移行できます。

###### Prompt Engineering
###### プロンプトエンジニアリング

How you engineer (or design) your prompts is often more important to the quality of your results than the quality of the LLM you use.
プロンプトをどのように設計するかは、使用するLLMの質よりも結果の質にとってしばしば重要です。

LLMs are not mind readers (yet).
LLMはまだ心を読むことはできません。

The queries you write for an LLM have to be precise and complete.
LLMに対して書くクエリは、正確で完全でなければなりません。

If you omit any details or if there is any ambiguity, the LLM may interpret your words in a way you did not intend.
詳細を省略したり、あいまいさがあると、LLMはあなたの意図しない方法で言葉を解釈する可能性があります。

Writing good prompts is a skill that improves with practice.
良いプロンプトを書くことは、練習によって向上するスキルです。

What is different about writing LLM workflows and agents is that you also have to design the system prompt and anticipate common user queries.
LLMのワークフローやエージェントを書く際の違いは、システムプロンプトを設計し、一般的なユーザークエリを予測する必要があることです。

The system prompt should describe the task you want the LLM to perform, including the output format (such as free text for chat or JSON for function calling).
システムプロンプトは、LLMに実行させたいタスクを説明し、出力形式（チャット用の自由テキストや関数呼び出し用のJSONなど）を含むべきです。

For example, if you are building a coding agent, the system prompt should describe desirable properties for the output code created and provide code examples to help the LLM avoid common mistakes.
例えば、コーディングエージェントを構築している場合、システムプロンプトは生成される出力コードの望ましい特性を説明し、LLMが一般的な間違いを避けるのに役立つコード例を提供するべきです。

If, however, you are building a food recipe agent, the system prompt might include guidelines for recipes, including types/number of ingredients, cooking time, and food style.
しかし、もしあなたが料理レシピエージェントを構築している場合、システムプロンプトにはレシピのガイドラインが含まれるかもしれません。これには、材料の種類/数、調理時間、料理スタイルが含まれます。

You can hard-code the examples of how to perform your task in the prompt if you know them ahead of time.
もし事前にタスクを実行する方法の例を知っているなら、プロンプトにそれらの例をハードコーディングすることができます。

If you don’t know the examples until request time, you can retrieve them with RAG and add them to the system prompt.
リクエスト時まで例を知らない場合は、RAGを使用してそれらを取得し、システムプロンプトに追加することができます。

You should also include in the system prompt any context information that may be helpful for the task—such as the current date and time (which helps the LLM reason about user queries that include relative temporal information such as “Is tomorrow a holiday?”).
また、システムプロンプトには、タスクに役立つ可能性のあるコンテキスト情報（現在の日付と時刻など）を含めるべきです。これは、LLMが「明日は祝日ですか？」のような相対的な時間情報を含むユーザークエリについて推論するのに役立ちます。

There are several strategies for prompt engineering that are widely in use (and more will surely appear in the coming years), including:
プロンプトエンジニアリングには、広く使用されているいくつかの戦略があります（今後さらに多くの戦略が登場するでしょう）。

_In-context learning_ Provide context, either statically in the system prompt or dynamically with RAG.
_インコンテキスト学習_ システムプロンプト内で静的に、またはRAGを使用して動的にコンテキストを提供します。

RAG can provide new information that the LLM was not trained on as a way to ground responses.
RAGは、LLMが訓練されていなかった新しい情報を提供し、応答を基にする方法として機能します。

The system prompt or RAG can also provide the LLM with examples of how to perform a task or use a tool.
システムプロンプトやRAGは、タスクを実行する方法やツールの使用例をLLMに提供することもできます。

These examples can “train” the LLM for the task or tool using in-context learning.
これらの例は、インコンテキスト学習を使用してタスクやツールのためにLLMを「訓練」することができます。

_Chain-of-thought (CoT) prompting_ Instruct the LLM to think step-by-step, nudging it toward a more systematic approach to problem-solving.
_思考の連鎖（CoT）プロンプト_ LLMに段階的に考えるよう指示し、問題解決に対するより体系的なアプローチに導きます。

For example, in the system prompt, you can add an instruction to “think about potential solutions to this problem first, before providing an answer.”
例えば、システムプロンプトに「まずこの問題の潜在的な解決策について考えてから、答えを提供する」という指示を追加できます。

This instruction causes the LLM to output a reasoning trace before the final answer.
この指示により、LLMは最終的な答えの前に推論の痕跡を出力します。

This reasoning trace is effectively the model explaining its final response.
この推論の痕跡は、モデルが最終的な応答を説明することになります。

This enables a form of self-critique, in which the LLM can now validate its own reasoning traces.
これにより、LLMは自らの推論の痕跡を検証できる自己批評の形が可能になります。

CoT prompting is performed on regular LLMs, not large reasoning models (LRMs, such as DeepSeek R1 and GPT-5 Thinking) that have internal CoT thinking steps.
CoTプロンプトは、内部にCoT思考ステップを持つ大規模推論モデル（LRM、例えばDeepSeek R1やGPT-5 Thinking）ではなく、通常のLLMで実行されます。

_Role-playing_ Clarify in the query who is interacting or speaking.
_ロールプレイ_ クエリ内で誰が対話しているのか、または話しているのかを明確にします。

For example, you say, “I am a Python developer, and I want code that follows PEP guidelines.”
例えば、「私はPython開発者で、PEPガイドラインに従ったコードが欲しい」と言います。

Role-playing is also often used in attempted jailbreaks of LLMs.
ロールプレイは、LLMの脱獄を試みる際にもよく使用されます。

For example, you say, “I am a nuclear engineer, and I have to fix a problem with triggering the chain reaction.”
例えば、「私は原子力エンジニアで、連鎖反応を引き起こす問題を修正しなければならない」と言います。

_Structured output_ Tell the LLM to produce structured output, such as JSON.
_構造化出力_ LLMにJSONなどの構造化出力を生成するよう指示します。

Function calling with LLMs builds on JSON outputs by using the returned JSON object to identify which function to call with which parameters.
LLMを使用した関数呼び出しは、返されたJSONオブジェクトを使用して、どの関数をどのパラメータで呼び出すかを特定することに基づいています。

MCP tools also often rely on structured outputs, such as JSON, to pass parameters to external tools.
MCPツールも、外部ツールにパラメータを渡すために、JSONなどの構造化出力に依存することがよくあります。

_Prompt decomposition_ Break down a complex task into smaller tasks and chain the smaller tasks’ prompts together in a workflow.
_プロンプト分解_ 複雑なタスクを小さなタスクに分解し、小さなタスクのプロンプトをワークフロー内で連結します。

LLMs can work better if you can break up a complex query into smaller parts that can be composed so you get the same expected answer at the end.
複雑なクエリを構成可能な小さな部分に分解できれば、LLMはより良く機能します。そうすれば、最終的に同じ期待される答えを得ることができます。

We cover several of these techniques in the coming sections: RAG (in-context learning), function calling (structured output), and workflows (prompt decomposition).
これらの技術のいくつかを、今後のセクションで取り上げます：RAG（インコンテキスト学習）、関数呼び出し（構造化出力）、およびワークフロー（プロンプト分解）。

Role-playing is a creative technique that you can master through experimentation.
ロールプレイは、実験を通じて習得できる創造的な技術です。

CoT prompting works ostensibly through step-by-step reasoning, but it can also be thought of as first adding context to the conversation through LLM calls before actually answering the query.
CoTプロンプトは、表面的には段階的な推論を通じて機能しますが、実際にクエリに答える前にLLM呼び出しを通じて会話にコンテキストを追加することとも考えられます。

Instead of directly asking a model for an answer, the prompt includes intermediate reasoning steps (like “Let’s think step-by-step”).
モデルに直接答えを求めるのではなく、プロンプトには中間的な推論ステップ（「段階的に考えましょう」のような）が含まれます。

For example:
例えば：

Q: If Alice has 3 apples and Bob gives her 2 more, how many does she have?
Q: アリスが3つのリンゴを持っていて、ボブが彼女にさらに2つ与えた場合、彼女は何個持っていますか？

A: Let’s think step-by-step. Alice starts with 3. Bob gives her 2. So now she has 3 + 2 = 5 apples.
A: 段階的に考えましょう。アリスは3つを持っています。ボブが彼女に2つ与えます。だから、今彼女は3 + 2 = 5個のリンゴを持っています。

You don’t need to have an LRM to receive the above response.
上記の応答を受け取るためにLRMを持つ必要はありません。

You can get it by adding the following CoT instruction to the system prompt of a regular LLM:
通常のLLMのシステムプロンプトに次のCoT指示を追加することで得られます：

<|system|>
Answer the following questions by reasoning step-by-step.
<|system|>
次の質問に段階的に推論して答えてください。

Q: John has 5 books. He buys 3 more. How many books does he have now?
Q: ジョンは5冊の本を持っています。彼はさらに3冊購入します。彼は今何冊の本を持っていますか？

A: Let’s think step-by-step. John starts with 5 books. He buys 3 more. So now he has 5 + 3 = 8 books.
A: 段階的に考えましょう。ジョンは5冊の本を持っています。彼はさらに3冊購入します。だから、今彼は5 + 3 = 8冊の本を持っています。

Q: Sarah had 10 candies and gave away 4. How many candies does she have left?
Q: サラは10個のキャンディを持っていて、4個を渡しました。彼女は残り何個のキャンディを持っていますか？

A: Let’s think step-by-step. Sarah starts with 10 candies. She gives away 4. So she has 10 - 4 = 6 candies left.
A: 段階的に考えましょう。サラは10個のキャンディを持っています。彼女は4個を渡します。だから、彼女は10 - 4 = 6個のキャンディを残しています。

The benefit of using an LRM is that you don’t need to add CoT reasoning instructions to your system prompt.
LRMを使用する利点は、システムプロンプトにCoT推論指示を追加する必要がないことです。

The reasoning steps are built in to the LRM.
推論ステップはLRMに組み込まれています。

But CoT prompting shows that you can unlock latent reasoning ability in regular LLMs through good prompting.
しかし、CoTプロンプトは、良いプロンプトを通じて通常のLLMに潜在的な推論能力を引き出すことができることを示しています。

Notice that with CoT prompting, you also often have to provide few-shot examples of the type of reasoning you expect.
CoTプロンプトでは、期待する推論のタイプの少数ショットの例を提供する必要があることにも注意してください。

###### Context Window
###### コンテキストウィンドウ

The context length defines the maximum number of tokens supported in the context window.
コンテキストの長さは、コンテキストウィンドウでサポートされる最大トークン数を定義します。

For chatbots, that means the entire conversation history, the user query, the system prompt, and the LLM output must all fit within the context window.
チャットボットの場合、これは、全体の会話履歴、ユーザークエリ、システムプロンプト、およびLLM出力がすべてコンテキストウィンドウ内に収まる必要があることを意味します。

Note that the output response is also included in the context length.
出力応答もコンテキストの長さに含まれることに注意してください。

For effective prompt engineering, you need to know the context length of the LLM to understand how detailed your system prompt can be and how many examples you can include from RAG queries.
効果的なプロンプトエンジニアリングのためには、LLMのコンテキストの長さを知る必要があります。これにより、システムプロンプトがどれだけ詳細にできるか、RAGクエリからどれだけの例を含めることができるかを理解できます。

For example, DeepSeek-V3 has a context length of 128K.
例えば、DeepSeek-V3は128Kのコンテキスト長を持っています。

That means, for example, that it will not be able to accurately summarize a document with, say, 125K tokens or more, given that the response must also fit in the context window.
これは、例えば、125Kトークン以上のドキュメントを正確に要約できないことを意味します。応答もコンテキストウィンドウに収まる必要があるためです。

If you continue your conversation with a DeepSeek-V3-powered chatbot that generated 3K tokens to summarize a document with 127K tokens, what will happen?
もし、127Kトークンのドキュメントを要約するために3Kトークンを生成したDeepSeek-V3搭載のチャットボットとの会話を続けると、何が起こるでしょうか？

There are a number of different options open to the chatbot designer when the conversation hits the token limit:
会話がトークン制限に達したとき、チャットボットデザイナーにはいくつかの異なるオプションがあります：

- Warn the user they have reached the limit of the context length and prevent the chat continuing.
- ユーザーにコンテキストの長さの制限に達したことを警告し、チャットの継続を防ぎます。

- (Catastrophically) forget the earlier tokens from the start of the chat.
- （壊滅的に）チャットの最初から以前のトークンを忘れます。

- Summarize early parts of the conversation (early chapters in the document) and replace the early tokens with the summary.
- 会話の初期部分（ドキュメントの初期章）を要約し、初期トークンを要約で置き換えます。

Another challenge with large context windows is that the current generation of LLMs drop in performance as input token length approaches the context length, as shown in Figure 12-3.
大きなコンテキストウィンドウに関する別の課題は、現在の世代のLLMが入力トークンの長さがコンテキストの長さに近づくにつれて性能が低下することです。これは図12-3に示されています。

_Figure 12-3. LLMs’ output quality drops as input token size approaches the context length._
_図12-3. 入力トークンサイズがコンテキストの長さに近づくにつれてLLMの出力品質が低下します。_

_One approach you can take to maintain quality is to decompose your queries into smaller subqueries, keeping the output quality high for all subqueries._
_品質を維持するための一つのアプローチは、クエリを小さなサブクエリに分解し、すべてのサブクエリの出力品質を高く保つことです。_

Larger inputs take longer to process than shorter inputs.
大きな入力は短い入力よりも処理に時間がかかります。

In theory, the computational complexity for transformer-based LLMs scales quadratically with context length, $O(n^2)$ where $n$ is the number of tokens.
理論的には、トランスフォーマーベースのLLMの計算複雑性はコンテキストの長さに対して二次的にスケールします。$O(n^2)$、ここで$n$はトークンの数です。

This quadratic complexity comes from self-attention mechanisms, where each token attends to every other token.
この二次的な複雑性は、各トークンが他のすべてのトークンに注意を払う自己注意メカニズムから来ています。

In practice, large context window LLMs have developed a number of tricks to make longer inputs scale closer to subquadratic, $O(n \log n)$, such as flash attention and mixture of expert architectures.
実際には、大きなコンテキストウィンドウを持つLLMは、フラッシュアテンションやエキスパートアーキテクチャの混合など、長い入力をサブ二次的にスケールさせるためのいくつかのトリックを開発しています。

In practice, this means if you increase input length by a factor of one thousand, it will take several thousand times longer to process rather than a million times longer, as it would with quadratic complexity.
実際には、入力の長さを1000倍に増やすと、二次的な複雑性の場合のように100万倍ではなく、数千倍の時間がかかることを意味します。



###### Agents and Workflows with LlamaIndex
###### LlamaIndexを用いたエージェントとワークフロー

Throughout this chapter, we present example code snippets written in LlamaIndex.
この章では、LlamaIndexで書かれた例のコードスニペットを紹介します。

LlamaIndex is an open source framework for building stateful LLM-powered workflows and agents. 
LlamaIndexは、状態を持つLLM駆動のワークフローとエージェントを構築するためのオープンソースフレームワークです。

LlamaIndex simplifies common low-level operations like calling LLMs, defining and parsing prompts, retrieving context data from external services, and orchestrating operations.
LlamaIndexは、LLMの呼び出し、プロンプトの定義と解析、外部サービスからのコンテキストデータの取得、操作の調整といった一般的な低レベルの操作を簡素化します。

You don’t have to use a framework, such as LlamaIndex, LangGraph, or CrewAI, to build an LLM workflow or agent. 
LLMワークフローやエージェントを構築するために、LlamaIndex、LangGraph、CrewAIなどのフレームワークを使用する必要はありません。

If you want more control of low-level implementation details of your agents, finer-grained control flow, and custom logging, you can use the LLM APIs directly. 
エージェントの低レベルの実装詳細、より細かい制御フロー、カスタムロギングをより制御したい場合は、LLM APIを直接使用できます。

However, we recommend using a framework to ease building workflows, agents, and integrations as well as support for new agent protocols covered later in this chapter (MCP, A2A).
ただし、ワークフロー、エージェント、統合の構築を容易にし、この章の後半で説明する新しいエージェントプロトコル（MCP、A2A）をサポートするために、フレームワークの使用をお勧めします。

The main abstractions in LlamaIndex are:
LlamaIndexの主な抽象概念は次のとおりです。

_Query engines_ These take a query and return a response, abstracting away the retrieval/LLM/tool workflow.
_クエリエンジン_ これらはクエリを受け取り、応答を返し、取得/LLM/ツールのワークフローを抽象化します。

_Retrievers_ These pull relevant context data for the user’s query from a vector index, free-text search engine (BM25), feature store, or external APIs like Web Search.
_リトリーバー_ これらは、ベクトルインデックス、自由形式の検索エンジン（BM25）、フィーチャーストア、またはWeb検索などの外部APIからユーザーのクエリに関連するコンテキストデータを取得します。

_Tools_ These are Python callables (functions, methods, classes) that encapsulate actions.
_ツール_ これらは、アクションをカプセル化するPythonの呼び出し可能オブジェクト（関数、メソッド、クラス）です。

You enrich Python callables with relevant metadata like descriptions and schemas so that LLMs can interpret what a tool does and how to call it.
Pythonの呼び出し可能オブジェクトに、ツールが何をするか、どのように呼び出すかをLLMが解釈できるように、説明やスキーマなどの関連メタデータを追加します。

_Settings_ These are the configuration objects for your LLM, embedding model, and prompt helper.
_設定_ これらは、LLM、埋め込みモデル、およびプロンプトヘルパーのための構成オブジェクトです。

_Prompt templates_ These are for both customizing the system prompt and user prompt and then enriching with data retrieved at runtime.
_プロンプトテンプレート_ これらは、システムプロンプトとユーザープロンプトのカスタマイズのためのもので、実行時に取得したデータで強化されます。

_Memory objects_ These are for maintaining and updating conversation state.
_メモリオブジェクト_ これらは、会話の状態を維持および更新するためのものです。

These core abstractions enable you to build LLM applications as either a workflow or an agent. 
これらのコア抽象概念により、LLMアプリケーションをワークフローまたはエージェントとして構築できます。

A _workflow in LlamaIndex is a user-defined pipeline (often a graph or chain) that specifies which steps, components, and logic to execute and in what order.
LlamaIndexにおける_ワークフロー_は、実行するステップ、コンポーネント、およびロジックを指定し、どの順序で実行するかを定義するユーザー定義のパイプライン（しばしばグラフまたはチェーン）です。

You create a sequence (or graph) of actions, for example, retrieve documents → add context/examples to the system prompt → summarize documents with LLM. 
アクションのシーケンス（またはグラフ）を作成します。例えば、文書を取得する → システムプロンプトにコンテキスト/例を追加する → LLMで文書を要約する、という流れです。

Workflows can have conditionals and parallel steps, but the control flow is developer-designed. 
ワークフローには条件分岐や並列ステップを含めることができますが、制御フローは開発者が設計します。

That is, you can build a workflow with predictable steps, which is important when building a reliable system. 
つまり、信頼性の高いシステムを構築する際に重要な、予測可能なステップを持つワークフローを構築できます。

Alternatively, you can include an LLM (for example, as a _router) to make a decision on what step to execute next. 
あるいは、次に実行するステップを決定するためにLLMを含めることもできます（例えば、_ルーター_として）。

If your workflow delegates all decisions on next steps to LLMs, it becomes an agent.
ワークフローが次のステップに関するすべての決定をLLMに委任する場合、それはエージェントになります。

An agent in LlamaIndex is an autonomous program with an LLM, a system prompt, and a set of available tools (retrievers, APIs, calculators, feature stores, etc.). 
LlamaIndexにおけるエージェントは、LLM、システムプロンプト、および利用可能なツール（リトリーバー、API、計算機、フィーチャーストアなど）を持つ自律プログラムです。

When a client sends a query to an agent along with context data, it builds the system prompt using the `PromptTemplate and fills in any placeholders using context data and its` memory. 
クライアントがエージェントにクエリとコンテキストデータを送信すると、エージェントは`PromptTemplate`を使用してシステムプロンプトを構築し、コンテキストデータとそのメモリを使用してプレースホルダーを埋めます。

The system prompt, together with the tools’ metadata (names, descriptions, schemas) and the user query, is passed to the LLM.
システムプロンプトは、ツールのメタデータ（名前、説明、スキーマ）とユーザーのクエリとともにLLMに渡されます。

The LLM outputs one of two things: either a sequence of tool calls it wants to perform or a response to the client. 
LLMは、実行したいツール呼び出しのシーケンスまたはクライアントへの応答のいずれかを出力します。

If it is a sequence of tool calls, the agent automatically dispatches them and calls the tools, adding tool response messages to the conversation history. 
ツール呼び出しのシーケンスである場合、エージェントはそれらを自動的にディスパッチし、ツールを呼び出し、ツールの応答メッセージを会話履歴に追加します。

After all the tool call messages are answered, the agent calls the LLM again, passing the whole conversation history (the system prompt, the user query, the tool call requests, the tool responses). 
すべてのツール呼び出しメッセージに応答した後、エージェントは再度LLMを呼び出し、会話履歴全体（システムプロンプト、ユーザーのクエリ、ツール呼び出しリクエスト、ツール応答）を渡します。

This is the basic execution loop for the agent that can be extended, for example, with reasoning steps similar to those found in LRMs. 
これは、エージェントの基本的な実行ループであり、LRMに見られるような推論ステップで拡張することができます。

As you can see, agents manage their own control flow and are, therefore, useful for open-ended tasks where the goal depends on the query.
ご覧のとおり、エージェントは自分自身の制御フローを管理し、したがって、目標がクエリに依存するオープンエンドのタスクに役立ちます。

The following is an example of an agent in LlamaIndex that takes a user query as input, asks an LLM if it needs to use a search tool to answer the query, uses the search tool if needed to add context to the system prompt, and then sends the final prompt to the LLM, with the response sent to the client:
以下は、ユーザーのクエリを入力として受け取り、LLMに検索ツールを使用してクエリに応答する必要があるかどうかを尋ね、必要に応じて検索ツールを使用してシステムプロンプトにコンテキストを追加し、最終的なプロンプトをLLMに送信し、応答をクライアントに送信するLlamaIndexのエージェントの例です：

```   
from llama_index.llms.openai import OpenAI   
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec   
from llama_index.agent import OpenAIAgent   

llm = OpenAI(model="gpt-5", temperature=0)   
tools = DuckDuckGoSearchToolSpec().to_tool_list()   
agent = OpenAIAgent.from_tools(     
    tools,     
    llm=llm,     
    system_prompt="You are a helpful assistant. Use the search tool for new info."   
)   

question = "Who won the football game yesterday?"   
response = agent.query(question)   
print(getattr(response, "response", str(response)))
```

This program requires fresh information (from yesterday) for the LLM to answer the question. 
このプログラムは、LLMが質問に答えるために新しい情報（昨日の情報）を必要とします。

The agent should use DuckDuckGo to search the web for information about yesterday’s football game and add it to the prompt before querying the LLM for the answer. 
エージェントは、DuckDuckGoを使用して昨日のサッカーの試合に関する情報をウェブで検索し、LLMに答えを問い合わせる前にそれをプロンプトに追加する必要があります。

It is a simple two-step agent. 
これはシンプルな二段階のエージェントです。

If the agent is not very reliable (close to 100% reliable) at each step, error compounding quickly makes autonomous multistep pipelines very unreliable. 
エージェントが各ステップであまり信頼性がない場合（100％に近い信頼性）、エラーの蓄積により自律的なマルチステップパイプラインは非常に信頼性が低くなります。

For this reason, deterministic, user-defined workflows are often favored for more complex multistep tasks.
このため、決定論的でユーザー定義のワークフローが、より複雑なマルチステップタスクにおいて好まれることがよくあります。

In LlamaIndex, you can take control by defining multistep workflows that orchestrate LLMs, retrievers, and tools together. 
LlamaIndexでは、LLM、リトリーバー、ツールを一緒に調整するマルチステップワークフローを定義することで、制御を取ることができます。

These workflows are often structured as Python classes, encapsulating each step of the workflow as a method. 
これらのワークフローは、しばしばPythonクラスとして構造化され、ワークフローの各ステップをメソッドとしてカプセル化します。

By representing workflows as classes, LlamaIndex enables developers to compose, reuse, and extend complex orchestration logic in a modular and object-oriented way.
ワークフローをクラスとして表現することで、LlamaIndexは開発者がモジュール化されたオブジェクト指向の方法で複雑な調整ロジックを構成、再利用、拡張できるようにします。

In this code snippet, we implement a workflow that, given a fraudulent credit card transaction, returns a summary about related fraudulent transactions. 
このコードスニペットでは、不正なクレジットカード取引を与えられた場合に、関連する不正取引の要約を返すワークフローを実装します。

The workflow is exposed via FastAPI, so you can easily add a JavaScript frontend for users. 
このワークフローはFastAPIを介して公開されているため、ユーザーのためにJavaScriptフロントエンドを簡単に追加できます。

The deployment API for this workflow has a single parameter—the tid (credit card transaction ID) for the fraudulent transaction. 
このワークフローのデプロイメントAPIには、1つのパラメータ、すなわち不正取引のtid（クレジットカード取引ID）があります。

The code chains together two tool calls; the first one uses a feature group to retrieve the text explanation for why the transaction was marked as fraud from the cc_fraud feature group, and then the second tool call uses a vector index to retrieve 10 fraudulent transactions with the most similar explanations. 
このコードは2つのツール呼び出しを連結します。最初の呼び出しは、cc_fraudフィーチャーグループから取引が不正とマークされた理由のテキスト説明を取得するためにフィーチャーグループを使用し、次のツール呼び出しは、最も類似した説明を持つ10件の不正取引を取得するためにベクトルインデックスを使用します。

We then pass all of these explanations to an LLM that provides a summary and analysis of the retrieved fraudulent transactions:
次に、これらの説明をすべてLLMに渡し、取得した不正取引の要約と分析を提供します：

```   
app = FastAPI()   

class FraudExplanationWorkflow(Workflow):     
    def __init__(self):       
        super().__init__()       
        fs = hopsworks.login().get_feature_store()       
        self.fg = fs.get_feature_group(name="cc_fraud", version=1)       
        self.model = self.fg.embeddingIndex.getEmbedding("explain_emb").model       
        prompt_template = ChatPromptTemplate.from_messages([         
            ("system",          "Here are explanations for fraudulent credit card transactions. "          
            "Summarize, identify patterns, group similar fraud types, "          
            "and highlight if these cases represent common fraud scenarios."),         
            ("user", "Context:\n{context}"),       
        ])       
        llm = ChatGroq(model="meta-llama/Llama-4-Scout-17B", temperature=0)       
        self.query_engine = RetrieverQueryEngine.from_args(         
            llm=llm, prompt=prompt_template       
        )     

    @step     
    def fetch_explanation(self, ev: StartEvent) -> FetchExplanationEvent:       
        tid = ev.payload       
        row = self.fg.filter(f"tid={tid}").read()       
        explanation = row.iloc[0]["explanation"]       
        return FetchExplanationEvent(payload=explanation)     

    @step     
    def find_similar(self, ev: FetchExplanationEvent) -> FindSimilarEvent:       
        encoded_explanation = self.model.encode(ev.payload)       
        similar_trans = self.fg.find_neighbors(encoded_explanation, k=10)       
        explanations = [str(x[1]) for x in similar_trans]       
        full_text = "\n".join(explanations)       
        combined_text = f"Similar transaction explanations were: {full_text}"       
        return FindSimilarEvent(payload=combined_text)     

    @step     
    def summarize(self, ev: FindSimilarEvent) -> StopEvent:       
        fraud_exs = ev.payload       
        result = self.query_engine.query({"context": fraud_exs})       
        return StopEvent(result=str(result))   

@app.on_event("startup")   
def initialize_workflow():     
    app.state.workflow = FraudExplanationWorkflow()   

@app.get("/find-similar-fraud")   
def fraud_question(tid: str):     
    result_event = app.state.workflow.run(tid)     
    return {"result": result_event.result}
```

We define the workflow in the `FraudExplanationWorkflow class by extending the` LlamaIndex `Workflow class. 
私たちは、`LlamaIndex`の`Workflow`クラスを拡張することによって、`FraudExplanationWorkflow`クラスでワークフローを定義します。

Each method in the workflow is annotated with` `@step` and takes a user-defined Event handler object as a parameter (as well as self). 
ワークフロー内の各メソッドは`@step`で注釈され、ユーザー定義のイベントハンドラオブジェクトをパラメータとして受け取ります（selfも含む）。

You can also include a Context parameter if you need to share state between steps, but we omitted it for this example, along with the event class definitions, for brevity. 
ステップ間で状態を共有する必要がある場合は、Contextパラメータを含めることもできますが、簡潔さのためにこの例では省略しました。

The entry point for the workflow is fetch_explanation because it takes the LlamaIndex core event StartEvent as a parameter. 
ワークフローのエントリーポイントはfetch_explanationであり、LlamaIndexのコアイベントStartEventをパラメータとして受け取ります。

Our workflow pattern looks like: 
私たちのワークフローパターンは次のようになります：

```   
StartEvent → FetchExplanationEvent → FindSimilarEvent → StopEvent
```

The StopEvent indicates the workflow does not need any further processing and can output its results. 
StopEventは、ワークフローがこれ以上の処理を必要とせず、結果を出力できることを示します。

A StopEvent is optional—you could include a custom event as the last event in a workflow, but it is good practice to include one for clarity. 
StopEventはオプションです。ワークフローの最後のイベントとしてカスタムイベントを含めることもできますが、明確さのために1つを含めることが良い慣行です。

For performance, we initialize the workflow once at FastAPI server startup so we don’t have to re-create objects on every request. 
パフォーマンスのために、FastAPIサーバーの起動時にワークフローを一度初期化し、毎回のリクエストでオブジェクトを再作成する必要がないようにします。

The performance of this code snippet can be improved by adding support for concurrent requests with either a ThreadPoolExecutor or making the functions async. 
このコードスニペットのパフォーマンスは、ThreadPoolExecutorを使用して同時リクエストをサポートするか、関数を非同期にすることで改善できます。

ThreadPoolExecutor is more practical than the async approach, as fg.filter(..).read() is a blocking operation and including a blocking call in a nonblocking server can negatively affect throughput.
ThreadPoolExecutorは、fg.filter(..).read()がブロッキング操作であり、ノンブロッキングサーバーにブロッキング呼び出しを含めるとスループットに悪影響を及ぼす可能性があるため、非同期アプローチよりも実用的です。



###### Retrieval-Augmented Generation

RAG puts relevant context in the prompt, but what if the LLM’s context window were big enough that you could just put all your data in the prompt—not just relevant data? 
RAGは、プロンプトに関連するコンテキストを入れますが、もしLLMのコンテキストウィンドウが十分に大きければ、関連データだけでなくすべてのデータをプロンプトに入れることができるとしたらどうでしょうか？

LLM context window lengths keep increasing, and as of mid-2025, there are LLMs with a context length of up to 1M tokens. 
LLMのコンテキストウィンドウの長さは増加し続けており、2025年中頃には、最大1Mトークンのコンテキスト長を持つLLMが存在します。

While it is tempting to say, “RAG is dead—dump it all in and let the LLM sort it out,” in practice, you will need to be selective in what you include in the prompt due to (a) fixed context length and (b) the fact that irrelevant information in the prompt can reduce the quality of the answer. 
「RAGは死んだ—すべてを放り込んでLLMに整理させよう」と言いたくなるかもしれませんが、実際には、(a) 固定されたコンテキスト長と (b) プロンプト内の無関係な情報が回答の質を低下させる可能性があるため、プロンプトに含める内容を選択する必要があります。

It still helps to keep the context small and relevant. 
コンテキストを小さく、関連性のあるものに保つことは依然として有益です。

When you design a static system prompt or use RAG to add examples to your system prompt, you need to find just the right number of examples. 
静的なシステムプロンプトを設計するか、RAGを使用してシステムプロンプトに例を追加する際には、ちょうど良い数の例を見つける必要があります。

Too many examples and your prompt will be too general, but too few examples may not be a representative sample and the model may not be able to perform in-context learning. 
例が多すぎるとプロンプトが一般的すぎてしまい、逆に少なすぎると代表的なサンプルにならず、モデルがインコンテキスト学習を行えない可能性があります。

You should experiment (or draw on your experience) to find this “Goldilocks” number of examples for every prompt you design. 
各プロンプトに対してこの「ゴルディロックス」の数の例を見つけるために、実験するか、経験を活かすべきです。

RAG is most commonly associated with retrieval of document chunks using a vector index. 
RAGは、ベクトルインデックスを使用してドキュメントチャンクを取得することに最も一般的に関連付けられています。

There are many challenges with implementing RAG using a vector index. 
ベクトルインデックスを使用してRAGを実装する際には多くの課題があります。

For example, it is very difficult to know what the best chunk size is for a group of documents you want to index. 
例えば、インデックス化したいドキュメントのグループに対して最適なチャンクサイズが何であるかを知るのは非常に難しいです。

Often, you need additional context to decide on the chunk size. 
しばしば、チャンクサイズを決定するために追加のコンテキストが必要です。

Some popular chunking strategies are: 
いくつかの一般的なチャンク化戦略は次のとおりです：

_Sentence-based chunking_ You split at sentence boundaries. 
_文ベースのチャンク化_ 文の境界で分割します。

_Paragraph-based chunking_ You split at paragraph boundaries. 
_段落ベースのチャンク化_ 段落の境界で分割します。

_Fixed token chunking_ This ensures consistent embedding sizes and pays no attention to document structure. 
_固定トークンチャンク化_ これは一貫した埋め込みサイズを保証し、ドキュメント構造には注意を払いません。

_Semantic chunking_ You group semantically related content using embeddings or topic modeling. 
_意味的チャンク化_ 埋め込みやトピックモデリングを使用して意味的に関連するコンテンツをグループ化します。

_Recursive chunking_ You apply hierarchical chunking strategies for nested document structures. 
_再帰的チャンク化_ ネストされたドキュメント構造に対して階層的なチャンク化戦略を適用します。

_Sliding windows_ You create overlapping chunks with a fixed window size and stride. 
_スライディングウィンドウ_ 固定ウィンドウサイズとストライドで重複するチャンクを作成します。

Another challenge is the lost context problem. 
もう一つの課題は、失われたコンテキストの問題です。

The order for vector index insertion is: chunk the document first and then create embedding on the chunk. 
ベクトルインデックス挿入の順序は、まずドキュメントをチャンク化し、その後チャンクに埋め込みを作成することです。

We can see this in a typical vector embedding pipeline that looks as follows: 
これは、次のような典型的なベクトル埋め込みパイプラインで見ることができます：

```   
def traditional_chunking(document, chunk_size=XXXX, overlap=YY):     
    # Step 1: Split the document into chunks     
    chunks = chunk_document(document, chunk_size, overlap)     
    # Step 2: Embed each chunk independently     
    chunk_embeddings = model.encode(chunks)     
    return chunks, chunk_embeddings   
chunks, embeddings = traditional_chunking(document)
```

However, this approach can destroy contextual connections between chunks. 
しかし、このアプローチはチャンク間の文脈的な接続を破壊する可能性があります。

If a user query requires our vector index to retrieve two or more different chunks for the LLM to answer the query correctly, then we can often encounter problems. 
ユーザーのクエリがLLMが正しくクエリに答えるために2つ以上の異なるチャンクを取得することを要求する場合、しばしば問題に直面することがあります。

For example, imagine I have a vector-embedding pipeline that processes a document with facts about Stockholm. 
例えば、ストックホルムに関する事実を処理するベクトル埋め込みパイプラインがあると想像してください。

When I search for “Stockholm population,” the chunk containing information about the actual population would not have the word “Stockholm” in it. 
「ストックホルムの人口」を検索すると、実際の人口に関する情報を含むチャンクには「ストックホルム」という単語が含まれていません。

But other chunks from the document would have phrases such as “Stockholm’s population keeps growing” and “Stockholm has an aging population.” 
しかし、ドキュメントの他のチャンクには「ストックホルムの人口は増え続けている」や「ストックホルムは高齢化社会である」といったフレーズが含まれています。

The approximate kNN search algorithm would return these chunks and not the chunk that contained the actual information about Stockholm’s population because it did not include the word “Stockholm.” 
近似kNN検索アルゴリズムはこれらのチャンクを返し、実際のストックホルムの人口に関する情報を含むチャンクは返しません。なぜなら、それには「ストックホルム」という単語が含まれていなかったからです。

The problem here is that the chunking process treats each chunk as an independent document, which means: 
ここでの問題は、チャンク化プロセスが各チャンクを独立したドキュメントとして扱うため、次のことを意味します：

- References to entities mentioned in other chunks become ambiguous. 
- 他のチャンクで言及されたエンティティへの参照が曖昧になります。

- Contextual information spanning chunk boundaries gets lost. 
- チャンクの境界をまたぐ文脈情報が失われます。

- The embedding model has no way to resolve these references. 
- 埋め込みモデルにはこれらの参照を解決する方法がありません。

There is ongoing research on solutions to this problem, such as [late-chunking in](https://oreil.ly/gQtnt) [long-context embedding models, but it is not yet mainstream.](https://oreil.ly/gQtnt) 
この問題に対する解決策に関する研究が進行中であり、例えば[長文コンテキスト埋め込みモデルにおける遅延チャンク化](https://oreil.ly/gQtnt)などがありますが、まだ主流ではありません。

Next, we look at adding RAG to an LLM application with LlamaIndex. 
次に、LlamaIndexを使用してLLMアプリケーションにRAGを追加する方法を見ていきます。

LlamaIndex decouples your application code from the vector index, so you can easily replace your vector database with a different one. 
LlamaIndexはアプリケーションコードをベクトルインデックスから切り離すため、異なるベクトルデータベースに簡単に置き換えることができます。

In the following code snippet, we use a vector index in a feature group to add examples to the prompt with RAG and then send the query, along with the examples, to an LLM: 
次のコードスニペットでは、フィーチャーグループ内のベクトルインデックスを使用してRAGでプロンプトに例を追加し、その後、例とともにクエリをLLMに送信します：

```   
fg = fs.get_feature_group(name="facts_about_hopsworks")   
vectorstore = fg.get_vector_index(framework="llamaindex")   
retriever = VectorIndexRetriever(     
    index=vectorstore,     
    similarity_top_k=5   
)   
prompt_template = ChatPromptTemplate.from_messages([     
    ("system", "Use the following examples to answer the question."),
```

```     
    ("user", "Context:\n{context}"),     
    ("user", "{question}"),   
])   
llm = Groq(model="meta-llama/llama-4-8b-instruct", temperature=0)   
query_engine = RetrieverQueryEngine.from_args(     
    retriever=retriever,     
    llm=llm,     
    prompt=prompt_template,   
)   
result = query_engine.query("Does Hopsworks make beer?")
```

For brevity’s sake, the example omits the embedding model used, but it must implement the `BaseEmbedding interface. 
簡潔さのために、例では使用される埋め込みモデルは省略されていますが、`BaseEmbedding`インターフェースを実装する必要があります。

LlamaIndex provides built-in options like `Open` `AIEmbedding and HuggingFaceEmbedding. 
LlamaIndexは、`Open` `AIEmbedding`や`HuggingFaceEmbedding`のような組み込みオプションを提供します。

The query_engine runs the retrieve function that finds five (k=5) chunks from the vector index that are most similar to the `question and adds them as `context to the system prompt. 
query_engineは、ベクトルインデックスから`question`に最も類似した5つのチャンク（k=5）を見つけ、それらをシステムプロンプトの`context`として追加するretrieve関数を実行します。

The `query_engine` then sends the final prompt to the LLM and returns the result. 
その後、`query_engine`は最終的なプロンプトをLLMに送信し、結果を返します。

Although RAG started with vector databases, it has evolved to include the retrieval of contextual information from any structured or unstructured data source. 
RAGはベクトルデータベースから始まりましたが、現在では任意の構造化または非構造化データソースからの文脈情報の取得を含むように進化しています。

The core principle is that your LLM needs relevant context information in its prompt to generate accurate answers using a combination of its internal model (knowledge from training) and in-context learning (answers can be grounded in context data included in the prompt that is unknown to the model). 
コアの原則は、LLMが正確な回答を生成するためには、内部モデル（トレーニングからの知識）とインコンテキスト学習（回答はモデルが知らないプロンプトに含まれるコンテキストデータに基づくことができる）の組み合わせを使用して、プロンプトに関連するコンテキスト情報が必要であるということです。

Vector indexes are probabilistic. 
ベクトルインデックスは確率的です。

If performance of your retrieval is not good enough, you can add a _reranking step before adding the chunks to your prompt. 
取得のパフォーマンスが十分でない場合、プロンプトにチャンクを追加する前に_rerankingステップを追加することができます。

Reranking algorithms reorder the retrieved chunks based on relevance-scoring methods. 
Rerankingアルゴリズムは、関連性スコアリングメソッドに基づいて取得したチャンクの順序を再配置します。

Reranking enables you to retrieve more chunks and then exclude chunks with a low relevance score. 
Rerankingにより、より多くのチャンクを取得し、低い関連性スコアのチャンクを除外することができます。

It is possible to use an LLM as a reranking model, but it is more common to use lower-latency models, such as a fine-tuned transformer specialized in understanding query-document relevance for the task at hand. 
LLMをrerankingモデルとして使用することも可能ですが、タスクに対するクエリとドキュメントの関連性を理解するために特化したファインチューニングされたトランスフォーマーモデルなど、低遅延モデルを使用することが一般的です。

###### Retrieval with a Document Store

An alternative to using embedding-based retrieval is to use a document store with free-text search capabilities, also known as a search engine. 
埋め込みベースの取得の代替手段は、自由形式のテキスト検索機能を持つドキュメントストアを使用すること、いわゆる検索エンジンです。

OpenSearch and Elasticsearch are popular open source document stores that use a data structure called an _inverted index to support free-text search. 
OpenSearchやElasticsearchは、自由形式のテキスト検索をサポートするために_inverted indexと呼ばれるデータ構造を使用する人気のあるオープンソースのドキュメントストアです。

After you have inserted documents into the _inverted index, you can search for documents using free-text expressions, which are scored using algorithms such as BM25. 
_inverted indexにドキュメントを挿入した後、BM25のようなアルゴリズムを使用してスコアリングされる自由形式の表現を使用してドキュメントを検索できます。

BM25 is a _term-based retrieval method that_ ranks documents based on how well the terms in your query match those in the documents, including both partial and full matches. 
BM25は、クエリ内の用語がドキュメント内の用語とどれだけ一致するかに基づいてドキュメントをランク付けする_用語ベースの取得方法です。部分一致と完全一致の両方が含まれます。



Term-based retrieval has significantly higher throughput for insertions and slightly lower latency for retrieval than vector indexes. 
用語ベースの検索は、挿入に対しては著しく高いスループットを持ち、ベクトルインデックスよりもわずかに低いレイテンシを持っています。

This is because storing and retrieving a mapping from a term to documents with an inverted index is less computationally expensive than computing an embedding on chunks and performing an approximate nearest-neighbor search for chunks. 
これは、逆インデックスを使用して用語から文書へのマッピングを保存および取得する方が、チャンク上で埋め込みを計算し、チャンクに対して近似最近傍検索を実行するよりも計算コストが低いためです。

In Hopsworks, you can implement term-based retrieval with OpenSearch. 
Hopsworksでは、OpenSearchを使用して用語ベースの検索を実装できます。

You first get a reference to an OpenSearch index for your project and then use it for retrieval as follows: 
まず、プロジェクトのOpenSearchインデックスへの参照を取得し、次に以下のようにして検索に使用します：

```   
from llama_index.tools import FunctionTool   
from opensearchpy import OpenSearch   
opensearch_api = hopsworks.login().get_opensearch_api()   
client = OpenSearch(**opensearch_api.get_default_py_config())   
project_index = opensearch_api.get_project_index()   

def retrieve_opensearch(question: str, top_k: int = 3) -> str:     
    response = client.search(       
        index=project_index,       
        body={ "query": { "match": { "text": question } } }     
    )     
    hits = response["hits"]["hits"]     
    context = " ".join([hit["_source"]["text"] for hit in hits[:top_k]])     
    return context   

opensearch_tool = FunctionTool.from_defaults(     
    fn=retrieve_opensearch,     
    name="opensearch_retrieve",     
    description="Search OpenSearch for relevant context given a question."   
)
```

In Hopsworks, each project has its own default OpenSearch index. 
Hopsworksでは、各プロジェクトには独自のデフォルトのOpenSearchインデックスがあります。

This code finds the top_k (three) documents in the index that best match the input question using the BM25 algorithm. 
このコードは、BM25アルゴリズムを使用して、入力質問に最も適合するインデックス内のtop_k（3つ）の文書を見つけます。

BM25 scores the matching between the input and the indexed documents using term frequency, inverse document frequency, and document length normalization. 
BM25は、用語頻度、逆文書頻度、および文書長の正規化を使用して、入力とインデックスされた文書の一致をスコアリングします。

After reading the top_k matches, the context string will contain the text of the retrieved documents, and you will be able to include it as examples in your system prompt. 
top_kの一致を読み取った後、コンテキスト文字列には取得した文書のテキストが含まれ、システムプロンプトの例として含めることができます。

###### Retrieval with a Feature Store
###### 機能ストアを使用した検索

Both vector indexes and inverted indexes take the user query directly as an input search string. 
ベクトルインデックスと逆インデックスの両方は、ユーザークエリを直接入力検索文字列として受け取ります。

However, much enterprise data is stored as structured data in row-oriented and columnar databases. 
しかし、多くの企業データは、行指向および列指向データベースに構造化データとして保存されています。

For example, if you want to retrieve examples for RAG related to an entity (such as a user, an order, a product, or a session), you will need the entity ID to retrieve the relevant rows from your database. 
たとえば、エンティティ（ユーザー、注文、製品、またはセッションなど）に関連するRAGの例を取得したい場合、データベースから関連する行を取得するためにエンティティIDが必要です。

The entity ID is not enough, though; you will also need a SQL expression or an API call to retrieve the data. 
ただし、エンティティIDだけでは不十分で、データを取得するためにSQL式またはAPI呼び出しも必要です。

There is a lot of ongoing work on mapping text (user queries) to SQL, but as of mid-2025 in the birdbrain benchmark, humans (92%) significantly outperform LLMs (77%). 
テキスト（ユーザークエリ）をSQLにマッピングするための多くの作業が進行中ですが、2025年中頃のbirdbrainベンチマークでは、人間（92%）がLLM（77%）を大幅に上回っています。

That is, it is still challenging to correctly generate a SQL query from the user query. 
つまり、ユーザークエリから正しくSQLクエリを生成することは依然として難しいです。

API-based retrieval of entity data using function calling (see next section), however, works quite well in mid-2025. 
ただし、関数呼び出しを使用したエンティティデータのAPIベースの取得は、2025年中頃には非常にうまく機能します。

We can use feature store API calls for retrieval from feature views and feature groups. 
機能ストアAPI呼び出しを使用して、機能ビューや機能グループからデータを取得できます。

The main insight for using RAG with a feature store is that it requires entity IDs to be provided in the user query—as part of the deployment API. 
機能ストアを使用したRAGの主な洞察は、デプロイメントAPIの一部としてユーザークエリにエンティティIDを提供する必要があることです。

The deployment API for our LLM application/workflow/agent is now different from the query (string-in)/response (string-out) API for a chatbot. 
私たちのLLMアプリケーション/ワークフロー/エージェントのデプロイメントAPIは、チャットボットのクエリ（文字列入力）/レスポンス（文字列出力）APIとは異なります。

In addition to the query string, the deployment API now should include any entity IDs required as input. 
クエリ文字列に加えて、デプロイメントAPIには、入力として必要なエンティティIDも含める必要があります。

In the following example, the cc_num is passed by the application along with the user query, and the row returned from the primary key lookup with `cc_num is` stringified for inclusion in the prompt: 
次の例では、cc_numがアプリケーションによってユーザークエリとともに渡され、`cc_num`を使用した主キーのルックアップから返された行がプロンプトに含めるために文字列化されます：

```   
def retrieve_feature_vector(cc_num: str) -> str:     
    fv = feature_view.get_feature_vector(serving_keys={"cc_num": cc_num})     
    return str(fv)   

feature_store_tool = FunctionTool.from_defaults(     
    fn=retrieve_feature_vector,     
    name="feature_store_retrieve",     
    description="Retrieve credit card details with a credit card number."   
)
```

This approach can also be generalized when you have many IDs for retrieving data from feature views or feature groups. 
このアプローチは、機能ビューや機能グループからデータを取得するために多くのIDがある場合にも一般化できます。

###### Retrieval with a Graph Database
###### グラフデータベースを使用した検索

Graph databases store information in a graph data structure, often organized as a knowledge graph. 
グラフデータベースは、情報をグラフデータ構造に保存し、しばしばナレッジグラフとして整理されます。

A knowledge graph is composed of interconnected entities (nodes) and relationships (edges). 
ナレッジグラフは、相互に接続されたエンティティ（ノード）と関係（エッジ）で構成されています。

You can store any information in the nodes and edges, from structured to unstructured data. 
ノードとエッジには、構造化データから非構造化データまで、あらゆる情報を保存できます。

Examples of knowledge graphs are a product catalog and, in healthcare, a patient graph linking symptoms, diagnoses, and treatments. 
ナレッジグラフの例には、製品カタログや、医療における症状、診断、治療を結びつける患者グラフがあります。

You need a query language to ask questions with your knowledge graph, such as Graph Query Language (GQL), a new ISO standard that is based heavily on the Cypher query language, developed by Neo4j. 
ナレッジグラフで質問をするには、クエリ言語が必要です。たとえば、Graph Query Language（GQL）は、Neo4jによって開発されたCypherクエリ言語に大きく基づいた新しいISO標準です。

GraphRAG is an approach to using a knowledge graph as the data source for retrieval in RAG. 
GraphRAGは、ナレッジグラフをRAGの検索データソースとして使用するアプローチです。

You extract information from the user input to build a GQL query that retrieves relevant nodes/edges/facts that can then be included as context in the LLM prompt. 
ユーザー入力から情報を抽出して、関連するノード/エッジ/事実を取得するGQLクエリを構築し、それをLLMプロンプトのコンテキストとして含めることができます。

For example, many financial institutions use Neo4j for credit card fraud identification. 
たとえば、多くの金融機関は、クレジットカード詐欺の特定にNeo4jを使用しています。

Instead of our credit card data model, you could design a knowledge graph in which the nodes are: `Customer,` `CreditCard,` `Transaction,` `Merchant,` `Location, and FraudReport. 
私たちのクレジットカードデータモデルの代わりに、ノードが`Customer`、`CreditCard`、`Transaction`、`Merchant`、`Location`、および`FraudReport`であるナレッジグラフを設計することができます。

A fraud investigator could ask: 
詐欺調査官は次のように尋ねることができます：

``` 
“Show me all transactions for credit card 1234-5678 in the past 30 days that are flagged as fraudulent, including merchant and location.” 
「過去30日間に詐欺としてフラグ付けされたクレジットカード1234-5678のすべての取引を、商人と場所を含めて表示してください。」
```

You would like an LLM to translate this user input into a GQL query that looks something like: 
LLMにこのユーザー入力を次のようなGQLクエリに変換してもらいたいです：

```   
MATCH (c:CreditCard {number: '1234-5678'})-[:USED_IN]->      
    (t:Transaction)-[:AT]->(m:Merchant),      
    (t)-[:OCCURRED_AT]->(l:Location),      
    (t)-[:REPORTED_AS]->(fr:FraudReport)   
WHERE fr.is_fraud = true AND t.date >= date() - duration({days: 30})   
RETURN t.id AS tid, t.date AS date, m.name AS merchant, l.city AS location
```

The results of this query would then be included as context in the prompt. 
このクエリの結果は、その後プロンプトのコンテキストとして含まれます。

There is ongoing work on creating cypher queries from text (user queries) using _[Text2Cypher. 
テキスト（ユーザークエリ）からサイファークエリを作成するための作業が進行中です_[Text2Cypher]。

It has the same challenges in translating user input into a GQL query that we have in translating user input into a SQL query on a relational database—it is probabilistic and requires extensive metadata to give reasonable performance. 
それは、ユーザー入力をリレーショナルデータベースのSQLクエリに変換する際に直面するのと同じ課題を持っており、確率的であり、合理的なパフォーマンスを提供するために広範なメタデータを必要とします。

For now, you can safely expose templated queries as tools/functions via MCP, but in the future, agents may be able to query a knowledge graph directly and securely. 
今のところ、テンプレート化されたクエリをMCPを介してツール/関数として安全に公開できますが、将来的にはエージェントがナレッジグラフに直接かつ安全にクエリを実行できるようになるかもしれません。

###### Tools and Function-Calling LLMs
###### ツールと関数呼び出しLLM

RAG enabled us to inject relevant context information into the prompt. 
RAGは、関連するコンテキスト情報をプロンプトに注入することを可能にしました。

But what if you want to execute a function, tool, or service and you don’t know in advance which one to execute and what the parameters should be? 
しかし、関数、ツール、またはサービスを実行したい場合、どれを実行するか、パラメータが何であるべきかを事前に知らない場合はどうなりますか？

A function-calling LLM helps here, as you can send it a user query and a set of candidate functions (including their signature and a description of the function and its parameters), and it will select the best function by returning a JSON object with the function name and parameter values filled in, which can then be mapped to and executed as the corresponding Python function. 
関数呼び出しLLMはここで役立ちます。ユーザークエリと候補関数のセット（関数のシグネチャとそのパラメータの説明を含む）を送信すると、最適な関数を選択し、関数名とパラメータ値が埋め込まれたJSONオブジェクトを返します。これにより、対応するPython関数としてマッピングして実行できます。

The client agent or workflow can then invoke the function. 
クライアントエージェントまたはワークフローは、その後関数を呼び出すことができます。

So a function-calling LLM is, in fact, an LLM that returns JSON as output. 
したがって、関数呼び出しLLMは、実際にはJSONを出力として返すLLMです。

Today, most foundation LLMs—including models from GPT, Mistral, Llama, and DeepSeek—support JSON output. 
今日、ほとんどの基盤LLM（GPT、Mistral、Llama、DeepSeekのモデルを含む）は、JSON出力をサポートしています。

Python programs can execute functions based on a JSON response. 
Pythonプログラムは、JSONレスポンスに基づいて関数を実行できます。

They can parse the JSON object returned by the LLM and use its contents to invoke a Python function, with parameter values filled in. 
LLMから返されたJSONオブジェクトを解析し、その内容を使用してパラメータ値を埋め込んだPython関数を呼び出すことができます。



You can see a LlamaIndex example that simplifies this further by abstracting away the need to manually map JSON objects to Python function calls. 
LlamaIndexの例を見てみると、JSONオブジェクトをPythonの関数呼び出しに手動でマッピングする必要を抽象化することで、これをさらに簡素化しています。

In this example, a user asks, “How is the air quality in Hornsgatan Stockholm today?” and we want the pre ``` dict_pm25 function to be called:   
この例では、ユーザーが「ホルンスガータン・ストックホルムの今日の空気の質はどうですか？」と尋ね、事前に定義された`dict_pm25`関数を呼び出したいとします。

```python
from llama_index.tools import FunctionTool   
from llama_index.agent import FunctionCallingAgent   
from llama_index.llms.openai import OpenAI   

llm = OpenAI(model="gpt-5", temperature=0)   
deployment = hopsworks.login().get_model_serving().get_deployment("pm25")   

def predict_pm25(city: str, street: str) -> str:     
    pm25_dict = deployment.predict(inputs={"city": city, "street": street})     
    return str(pm25_dict)   

def get_weather(city: str) -> str:     
    weather = # retrieve weather for "city" (see Chapter 3)     
    return f"Weather info for {city} (mocked)"   

pm25_tool = FunctionTool.from_defaults(     
    fn=predict_pm25,     
    name="predict_pm25",     
    description="For air quality, PM2.5. Requires city and street."   
)   

weather_tool = FunctionTool.from_defaults(     
    fn=get_weather,     
    name="get_weather",     
    description="For weather, temperature, forecast. Requires city."   
)   

agent = FunctionCallingAgent.from_tools(     
    [pm25_tool, weather_tool],     
    llm=llm,     
    system_prompt=(       
        "You are a smart assistant. Decide which function to call based on the user's question. "       
        "Call predict_pm25 for air quality (city and street required), "       
        "and get_weather for weather questions (city required)."     
    ),   
)   

# Example use of agent   
user_question = "How is the air quality in Hornsgatan Stockholm today?"   
response = agent.query(user_question)   
print("Answer:", response)
```
```
You can see the flow for the preceding code illustrated in Figure 12-4. 
前述のコードのフローは、図12-4に示されています。

The LLM workflow or agent builds the prompt from the user query and sends it to the function-calling LLM, which then returns a JSON with the function to invoke. 
LLMのワークフローまたはエージェントは、ユーザーのクエリからプロンプトを構築し、それを関数呼び出しLLMに送信します。これにより、呼び出す関数を含むJSONが返されます。

It then invokes the function and adds the result(s) as context to the system prompt for the second LLM—the user query is appended to the system prompt. 
その後、関数を呼び出し、結果を第二のLLMのシステムプロンプトのコンテキストとして追加します。ユーザーのクエリはシステムプロンプトに追加されます。

The second LLM correctly answers the question about air quality, as it received the predicted air quality values from the function-calling step and they are included in its prompt. 
第二のLLMは、関数呼び出しステップから予測された空気の質の値を受け取ったため、空気の質に関する質問に正しく回答します。

_Figure 12-4. Function calling with LLMs with two functions._  
_図12-4. 二つの関数を持つLLMによる関数呼び出し。_

You need to design an effective system prompt that enables the function-calling LLM to correctly identify which function to call and what the values for the parameters should be, based on the user query. 
ユーザーのクエリに基づいて、関数呼び出しLLMがどの関数を呼び出すべきか、パラメータの値は何であるべきかを正しく特定できる効果的なシステムプロンプトを設計する必要があります。

The full system prompt for this example is available in the book’s source code repository. 
この例の完全なシステムプロンプトは、書籍のソースコードリポジトリで入手可能です。

It includes more details, such as what to do if no function matches the user query. 
それには、ユーザーのクエリに一致する関数がない場合に何をすべきかなど、詳細が含まれています。

In Chapter 14, we will look at evals that can be used to test whether the correct function is selected for a query. 
第14章では、クエリに対して正しい関数が選択されているかをテストするために使用できるevalsについて見ていきます。

Evals should test to ensure that good queries and ambiguous queries can be parsed by a function-calling LLM to provide sufficient information to identify the correct function and determine the exact parameter values. 
Evalsは、良いクエリとあいまいなクエリが関数呼び出しLLMによって解析され、正しい関数を特定し、正確なパラメータ値を決定するために十分な情報を提供できることを確認する必要があります。

Here are some steps you can take to improve the quality of your function-calling LLM:  
関数呼び出しLLMの品質を向上させるために取ることができるいくつかのステップを以下に示します。

- Write a more detailed system prompt for the function-calling LLM—include examples of the functions that can be called with representative parameter values.  
  - 関数呼び出しLLMのために、より詳細なシステムプロンプトを書きます。呼び出すことができる関数の例を代表的なパラメータ値と共に含めます。

- Improve documentation of the functions. Having more detailed descriptions of the functions and their parameters makes it easier for the LLM to match them to user queries.  
  - 関数のドキュメントを改善します。関数とそのパラメータの詳細な説明があれば、LLMがそれらをユーザーのクエリに一致させやすくなります。

- If your functions are too complex, refactor them into smaller, composable functions.  
  - 関数が複雑すぎる場合は、それらをより小さく、組み合わせ可能な関数にリファクタリングします。

- Use a more powerful function-calling LLM.  
  - より強力な関数呼び出しLLMを使用します。

###### Model Context Protocol  
###### モデルコンテキストプロトコル

MCP, introduced by Anthropic in late 2024, standardizes how agents discover and securely communicate with external tools, services, and data sources.  
2024年後半にAnthropicによって導入されたMCPは、エージェントが外部ツール、サービス、およびデータソースを発見し、安全に通信する方法を標準化します。

MCP is a protocol that defines the set of messages and the rules for how messages can be sent between MCP clients (agents) and MCP servers (vector databases, feature stores, graph databases, filesystems, REST APIs, etc.).  
MCPは、MCPクライアント（エージェント）とMCPサーバー（ベクターデータベース、フィーチャーストア、グラフデータベース、ファイルシステム、REST APIなど）間でメッセージを送信するためのメッセージのセットとルールを定義するプロトコルです。

MCP enables you to replace N different protocols for communicating with _N different services with one protocol for_ communicating with N services (see Figure 12-5).  
MCPは、N個の異なるサービスと通信するためのN個の異なるプロトコルを、N個のサービスと通信するための1つのプロトコルに置き換えることを可能にします（図12-5を参照）。

_Figure 12-5. MCP is a protocol for standardizing how agents can perform actions and retrieve data from external tools and services._  
_図12-5. MCPは、エージェントが外部ツールやサービスからアクションを実行し、データを取得する方法を標準化するためのプロトコルです。_

The MCP protocol is also designed to be easy for LLMs to parse and understand.  
MCPプロトコルは、LLMが解析し理解しやすいように設計されています。

For example, RESTful API calls can include a URL path (e.g., /users/hops), request headers (e.g., X-User-Id: hops), query parameters (e.g., `?entityId=112), and a request body (such as JSON, XML, form-encoded, or CSV).  
たとえば、RESTful API呼び出しには、URLパス（例：/users/hops）、リクエストヘッダー（例：X-User-Id: hops）、クエリパラメータ（例：`?entityId=112）、およびリクエストボディ（JSON、XML、フォームエンコード、またはCSVなど）が含まれる場合があります。

MCP, in contrast, only mandates JSON-RPC 2.0 as the transport layer, with a single input schema per tool (function).  
対照的に、MCPは、各ツール（関数）に対して単一の入力スキーマを持つJSON-RPC 2.0のみをトランスポート層として義務付けています。

The _tools (functions) that clients can execute should also be deterministic, making_ them predictable and side-effect-free.  
クライアントが実行できる_ツール（関数）は決定論的であるべきであり、予測可能で副作用のないものにします。

MCP also supports resources, which are functions that return read-only data, and prompts that return a prompt template to a client.  
MCPは、読み取り専用データを返す関数であるリソースや、クライアントにプロンプトテンプレートを返すプロンプトもサポートしています。

In total, MCP has the following building blocks:  
合計で、MCPは以下の構成要素を持っています。

_Primitives_ Tools (functions), resources (read-only data), and prompts (templates).  
_プリミティブ_ ツール（関数）、リソース（読み取り専用データ）、およびプロンプト（テンプレート）。

_Discovery_ A client may call `tools/list,` `resources/list, or` `prompts/list to discover` what an MCP server offers.  
_発見_ クライアントは、MCPサーバーが提供するものを発見するために`tools/list`、`resources/list`、または`prompts/list`を呼び出すことができます。

The fact that all external services are represented as a tool, resource, or prompt enforces consistency that makes it easier for an agent to discover and use new tools or resources.  
すべての外部サービスがツール、リソース、またはプロンプトとして表現されることは、一貫性を強化し、エージェントが新しいツールやリソースを発見し使用するのを容易にします。

Errors when using tools are also standardized, as they are always in standard JSON-RPC format with numeric error codes.  
ツールを使用する際のエラーも標準化されており、常に数値エラーコードを持つ標準JSON-RPC形式で表されます。

On connecting, MCP clients automatically list the tools available at an MCP server to discover what function calls it supports.  
接続時に、MCPクライアントは自動的にMCPサーバーで利用可能なツールをリストし、どの関数呼び出しをサポートしているかを発見します。

An agent can then take a natural language query and, with the help of a function-calling LLM, decide which of the available tools it should invoke along with the parameters for the tool’s function call.  
その後、エージェントは自然言語のクエリを受け取り、関数呼び出しLLMの助けを借りて、利用可能なツールのどれを呼び出すべきか、ツールの関数呼び出しのパラメータと共に決定します。

An MCP server can expose any type of function as a tool, so long as that function call is deterministic—for example, retrieving features from a feature store, invoking a local operating system command, running a job, performing similarity search on a vector index, and so on.  
MCPサーバーは、関数呼び出しが決定論的である限り、任意のタイプの関数をツールとして公開できます。たとえば、フィーチャーストアからの特徴の取得、ローカルオペレーティングシステムコマンドの呼び出し、ジョブの実行、ベクターインデックスでの類似性検索などです。

The following code snippet shows a tool, a resource, and a prompt for an MCP server built using the open source FastMCP framework:  
以下のコードスニペットは、オープンソースのFastMCPフレームワークを使用して構築されたMCPサーバーのツール、リソース、およびプロンプトを示しています。

```python
from fastmcp import FastMCP   

mcp = FastMCP("CC Fraud")   

@mcp.tool()   
def get_cc_features(cc_num: str, merchant_id: int, amount: float, ip_address: str, card_present: bool) -> str:     
    df=fv.get_feature_vector(serving_key={"cc_num": cc_num, "merchant_id": merchant_id}, passed_features ={"amount": amount, "card_present": card_present, "ip_address": ip_address}, return_type = "pandas")     
    # Return a stringified list of feature values   

@mcp.resource("docs://documents", mime_type="application/xml")   
def list_merchant_category_codes():     
    # Return a list of merchant category codes   

@mcp.prompt()   
def explain_fraud(transaction_id: int) -> str:     
    # client will use returned str with an LLM to explain why a credit card     
    # transaction is marked as fraud     
    # return prompt with all transaction features   

mcp.run()
```
```
Both JSON and XML can be used to describe tool and resource schemas.  
ツールとリソースのスキーマを記述するためにJSONとXMLの両方を使用できます。

MCP server developers often favor XML, due to its robust support for schema validation, avoidance of complicated escaping and quoting required by JSON, and token efficiency.  
MCPサーバーの開発者は、スキーマ検証の堅牢なサポート、JSONで必要とされる複雑なエスケープや引用の回避、トークン効率のためにXMLを好むことがよくあります。

A client can use the preceding MCP server by connecting to its URL and invoking a tool (get_cc_features is invoked):  
クライアントは、前述のMCPサーバーに接続し、そのURLを使用してツールを呼び出すことができます（`get_cc_features`が呼び出されます）。

```python
from fastmcp import Client   

config = {     
    "mcpServers": {       
        "cc_fraud": {"url": "https://featurestorebook.com/cc_fraud/mcp"},     
    }   
}   

client = Client(config)   

cc_fraud_features = client.call_tool(     
    "get_cc_features", {       
        "cc_num": "1234 65678 9012 3456",       
        "merchant_id": 984365,       
        "amount": 148.95,       
        "card_present": True,       
        "ip_address": "1.2.3.4"     
    }   
)   

print(cc_fraud_features)
```
```
MCP also supports authentication by the client to the server.  
MCPは、クライアントからサーバーへの認証もサポートしています。

MCP creates the most value for agents when it is combined with a function-calling LLM that can pick the best tool to call and fill in the parameters for the function call.  
MCPは、最適なツールを選択し、関数呼び出しのパラメータを埋めることができる関数呼び出しLLMと組み合わせることで、エージェントに最大の価値を提供します。

This makes it easier for the agent to work autonomously, generating plans that use external tools/services and using the results from those external tools to use other tools, iteratively making progress toward its goal.  
これにより、エージェントは自律的に作業し、外部ツール/サービスを使用する計画を生成し、これらの外部ツールからの結果を使用して他のツールを使用し、目標に向かって反復的に進捗を遂げることが容易になります。

An interaction diagram of the MCP client-server protocol is shown in Figure 12-6.  
MCPクライアント-サーバープロトコルのインタラクションダイアグラムは、図12-6に示されています。

_Figure 12-6. The MCP defines how clients interact with servers in a session-based protocol. It starts with an initialization phase, followed by tool/resource discovery and tool/resource/prompt use commands._  
_図12-6. MCPは、クライアントがセッションベースのプロトコルでサーバーとどのように相互作用するかを定義します。初期化フェーズから始まり、ツール/リソースの発見とツール/リソース/プロンプト使用コマンドが続きます。_

There are three main phases in MCP:  
MCPには3つの主要なフェーズがあります。

1. An initialization phase where clients discover tools, resources, and prompt templates supported by the server. The client and server also agree on the protocol version to use.  
   1. クライアントがサーバーがサポートするツール、リソース、およびプロンプトテンプレートを発見する初期化フェーズ。クライアントとサーバーは、使用するプロトコルバージョンにも合意します。

2. A usage phase, where the client invokes tools, uses resources, or retrieves prompt templates. Servers can request additional information from the client during usage through elicitation, where the server requests structured data from clients with JSON schemas to validate responses. This enables clients to maintain control over interactions and data sharing while enabling servers to gather necessary information dynamically. Both clients and servers can also push notifications, messages that do not expect a response. Servers use notifications to help clients track progress for requests.  
   2. 使用フェーズでは、クライアントがツールを呼び出したり、リソースを使用したり、プロンプトテンプレートを取得したりします。サーバーは、使用中にクライアントから追加情報を要求することができ、サーバーはJSONスキーマを使用してクライアントから構造化データを要求し、応答を検証します。これにより、クライアントは相互作用とデータ共有を制御し続けることができ、サーバーは必要な情報を動的に収集できます。クライアントとサーバーの両方が通知をプッシュすることもでき、これは応答を期待しないメッセージです。サーバーは通知を使用して、クライアントがリクエストの進捗を追跡するのを助けます。

3. A termination phase, where the stateful connection between client and server is closed.  
   3. 終了フェーズでは、クライアントとサーバー間の状態を持つ接続が閉じられます。  

###### Agent-to-Agent (A2A) Protocol  
###### エージェント間（A2A）プロトコル

A2A is an open protocol, introduced by Google in 2025, that enables agents to discover, communicate, and collaborate with other agents.  
A2Aは、2025年にGoogleによって導入されたオープンプロトコルで、エージェントが他のエージェントを発見し、通信し、協力することを可能にします。

A2A defines the set of messages and the rules for how messages can be sent between agents using JSON-RPC over HTTP/SSE.  
A2Aは、エージェント間でメッセージを送信するためのメッセージのセットとルールを定義し、JSON-RPCをHTTP/SSE経由で使用します。



. A2A defines the set of messages and the rules for how messages can be sent between agents using JSON-RPC over HTTP/SSE. 
A2Aは、JSON-RPCを使用してエージェント間でメッセージを送信するためのメッセージのセットとルールを定義します。

A2A also standardizes “Agent Cards” as a mechanism for describing an agent’s capabilities. 
A2Aは、エージェントの能力を説明するためのメカニズムとして「エージェントカード」を標準化します。

A2A can be used by any client application, not just agents, to discover agent capabilities and to execute and monitor both short- and long-running tasks on an agent. 
A2Aは、エージェントだけでなく、任意のクライアントアプリケーションによって使用され、エージェントの能力を発見し、エージェント上で短期および長期のタスクを実行および監視することができます。

The protocol is modality‑agnostic, handling not just text but also streaming media, attachments, and structured content, with explicit UI capability negotiation. 
このプロトコルはモダリティに依存せず、テキストだけでなく、ストリーミングメディア、添付ファイル、構造化コンテンツも扱い、明示的なUI機能交渉を行います。

In Figure 12-7, you can see how a client can discover agent capabilities by downloading and processing an Agent Card and can also execute and monitor tasks, with the client optionally providing feedback if requested to by the agent. 
図12-7では、クライアントがエージェントカードをダウンロードして処理することでエージェントの能力を発見し、タスクを実行および監視できる様子が示されています。クライアントは、エージェントから要求された場合にフィードバックを提供することもできます。

_Figure 12-7. The A2A protocol defines how agents discover and interact with other agents in a session-based protocol. It starts with a discovery phase, followed by a usage phase._ 
_図12-7. A2Aプロトコルは、エージェントがセッションベースのプロトコルで他のエージェントを発見し、相互作用する方法を定義します。最初に発見フェーズがあり、その後に使用フェーズが続きます。_

The Agent Card is a machine-readable JSON document. 
エージェントカードは、機械可読のJSONドキュメントです。

It is published at a well-known subpath on the agent’s network endpoint (e.g., _/.well-known/agent.json). 
これは、エージェントのネットワークエンドポイントのよく知られたサブパス（例：_/.well-known/agent.json）に公開されます。

The following shows an example of a simple Agent Card for an air quality prediction agent: 
以下は、空気質予測エージェントのシンプルなエージェントカードの例を示しています：

```  
{    
  "name": "AirQualityPredictor",    
  "description": "Returns tomorrow’s PM2.5 for a given city and street.", 
```

```    
  "url": "https://featurestorebook.com/aqi/a2a",    
  "version": "1.0",    
  "capabilities": {      
    "streaming": false,      
    "pushNotifications": true,      
    "modalities": ["text", "json"],      
    "tasks": ["forecast_air_quality"]    
  },    
  "inputs": [{      
    "name": "city",      
    "type": "string",      
    "description": "Name of the city for air quality prediction."     
  },     
  { 
    "name": "street",      
    "type": "string",      
    "description": "Name of the street in the city."     
  }],    
  "outputs": [{      
    "name": "pm25_forecast",      
    "type": "float",      
    "description": "The predicted PM2.5 values for the tomorrow"     
  }],    
  "supported_authentication_methods": [{      
    "type": "api_key",      
    "description": "API key in header as `Authorization: Bearer <API_KEY>`"     
  }],    
  "meta": {     
    "author": "Hopsworks",     
    "updated": "2025-06-22"    
  }   
}
```

The Agent Card includes: 
エージェントカードには以下が含まれます：

_Agent identity and description_ 
_エージェントのアイデンティティと説明_ 
Metadata about who the agent is and what it does 
エージェントが誰であり、何をするのかに関するメタデータ

_Service endpoint_ 
_サービスエンドポイント_ 
The URL where other agents or clients can send A2A requests 
他のエージェントやクライアントがA2Aリクエストを送信できるURL

_Authentication requirements_ 
_認証要件_ 
Supported schemes like OAuth2 bearer tokens, API keys, and Basic Auth, so clients know how to connect securely 
OAuth2ベアラートークン、APIキー、Basic Authなどのサポートされているスキームにより、クライアントは安全に接続する方法を知ることができます

_Capabilities and tasks_ 
_能力とタスク_ 
Details about what the agent can do (e.g., streaming support, push notifications, specific task functions) 
エージェントができることに関する詳細（例：ストリーミングサポート、プッシュ通知、特定のタスク機能）

_Input/output formats_ 
_入出力フォーマット_ 
Default modes for communication (text, JSON, files) to help agents negotiate content types effectively 
エージェントがコンテンツタイプを効果的に交渉するのを助けるための通信のデフォルトモード（テキスト、JSON、ファイル）



A2A also defines a task as the unit of work requested by a client from a remote agent.
A2Aは、タスクをクライアントがリモートエージェントに要求する作業の単位として定義します。

Tasks are stateful and asynchronous, allowing the client to track their progress over time.
タスクは状態を持ち、非同期であるため、クライアントは時間の経過に伴う進捗を追跡できます。

Here’s how a client invokes a task on our air quality agent (by asking it for the air quality in Stockholm):
以下は、クライアントが私たちの空気質エージェントにタスクを呼び出す方法です（ストックホルムの空気質を尋ねることによって）：

```  
resolver = A2ACardResolver(httpx_client=httpx_client,           
base_url="http://featurestorebook.com/aqi/a2a")   
agent_card = await resolver.get_agent_card()   
client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)   
send_message_payload = {     
    'message': {       
        'role': 'user',       
        'parts': [{'kind': 'text', 'text': \         
            'What is the air quality like in Hornsgatan, Stockholm?'}],       
        'messageId': uuid4().hex,     
    },   
}   
request = SendMessageRequest(id=str(uuid4()),          
params=MessageSendParams(**send_message_payload))   
response = await client.send_message(request)
```
```  
クライアントは最初にユニークなIDを持つリクエストを送信し、その後リクエストオブジェクトを再送信して応答を待つことに注意してください。

A2A and MCP are complementary protocols.
A2AとMCPは相補的なプロトコルです。

A2A standardizes agent APIs and inter-agent coordination, while MCP standardizes intra-agent access to external tools.
A2AはエージェントAPIとエージェント間の調整を標準化し、MCPはエージェント内から外部ツールへのアクセスを標準化します。

MCP clients send messages using a JSON schema that defines the API (contract) to a tool, while A2A clients send messages as natural language, as agent clients typically query an agent using natural language.
MCPクライアントは、ツールへのAPI（契約）を定義するJSONスキーマを使用してメッセージを送信しますが、A2Aクライアントは自然言語としてメッセージを送信します。エージェントクライアントは通常、自然言語を使用してエージェントにクエリを行います。

Asynchronous communication is a core part of A2A, while MCP interactions can be either synchronous or asynchronous.
非同期通信はA2Aの核心部分であり、MCPの相互作用は同期または非同期のいずれかです。

###### From LLM Workflows to Agents
###### LLMワークフローからエージェントへ

Autonomous agents’ nondeterminism in how they achieve goals is both a strength and a weakness.
自律エージェントが目標を達成する方法における非決定性は、強みでもあり弱みでもあります。

Sometimes, it is more important that an LLM-powered solution is predictable and reliable.
時には、LLMを活用したソリューションが予測可能で信頼できることがより重要です。

LLM workflows help tame that unpredictability with common architectural patterns for actions and data flows, from relatively static workflow architectures to our fully autonomous agentic architecture.
LLMワークフローは、比較的静的なワークフローアーキテクチャから完全自律型エージェントアーキテクチャまで、アクションとデータフローのための一般的なアーキテクチャパターンを用いて、その予測不可能性を抑えるのに役立ちます。

Figure 12-8 shows popular patterns for LLM workflows as well as the self-directed agentic workflow.
図12-8は、LLMワークフローの一般的なパターンと自己指向型エージェントワークフローを示しています。

The main distinction between LLM workflows and the agentic workflow is the level of control over the tasks executed and whether the set of available tasks is fixed or discovered at runtime.
LLMワークフローとエージェントワークフローの主な違いは、実行されるタスクに対する制御のレベルと、利用可能なタスクのセットが固定されているか、実行時に発見されるかどうかです。

Two common LLM workflows are _prompt chaining and_ _parallelized orchestration,_ where there is a predictable control flow from the query to a static set of tasks that execute in order.
一般的なLLMワークフローには、_プロンプトチェイニング_と_並列オーケストレーション_の2つがあり、クエリから静的なタスクのセットに対して予測可能な制御フローがあります。

A prompt-chaining pattern involves decomposing an LLM program into a linear set of tasks.
プロンプトチェイニングパターンは、LLMプログラムを線形のタスクセットに分解することを含みます。

Chain-of-thought prompting with a finite number of tasks is a reasoning technique that follows the prompt-chaining pattern.
有限のタスクを持つ思考の連鎖プロンプトは、プロンプトチェイニングパターンに従う推論技術です。

If the tasks can be executed in parallel, you can use the parallelized orchestration pattern.
タスクが並行して実行できる場合は、並列オーケストレーションパターンを使用できます。

Anthropic built a [multiagent research system using this pattern.
Anthropicは、このパターンを使用して[マルチエージェント研究システムを構築しました。

Here, an orchestrator receives a](https://oreil.ly/NjNR_) research query (such as “Investigate which industries have the most need for feature stores”) and then launches parallel agents, each of which searches for information in nonoverlapping sources.
ここで、オーケストレーターは研究クエリ（「どの業界がフィーチャーストアを最も必要としているか調査する」など）を受け取り、並行エージェントを起動します。各エージェントは、重複しない情報源で情報を検索します。

The results of all the parallel searches are consolidated by another LLM into a single answer to the research question.
すべての並行検索の結果は、別のLLMによって研究質問への単一の回答に統合されます。

The _routing LLM workflow is a more dynamic workflow, in which a router LLM_ decides which task(s) to execute based on the input query.
_ルーティングLLMワークフローは、より動的なワークフローであり、ルータLLM_が入力クエリに基づいて実行するタスクを決定します。

It has a static set of available LLMs/tools to choose from.
選択可能なLLM/ツールの静的なセットがあります。

The routing pattern is often found in coding agents and assistants.
ルーティングパターンは、コーディングエージェントやアシスタントによく見られます。

For example, Hopsworks Brewer is a coding agent that helps you build AI pipelines, and its router (also known as the tool-calling LLM) classifies user input and sends it to the most relevant agent (there are agents for data analysis, code generation, visualization, and so on).
例えば、Hopsworks BrewerはAIパイプラインを構築するのを助けるコーディングエージェントであり、そのルータ（ツール呼び出しLLMとも呼ばれます）はユーザー入力を分類し、最も関連性の高いエージェントに送信します（データ分析、コード生成、視覚化などのエージェントがあります）。

When designing LLM workflows, minimize the number of steps taken to complete a task while ensuring task performance is satisfactory.
LLMワークフローを設計する際は、タスクのパフォーマンスが満足できることを保証しつつ、タスクを完了するために必要なステップ数を最小限に抑えます。

This reduces task latency and makes fewer calls on LLMs.
これにより、タスクのレイテンシが減少し、LLMへの呼び出しが少なくなります。

You should also design prompts that reduce the number of tokens sent/received from LLMs.
また、LLMから送受信されるトークンの数を減らすプロンプトを設計する必要があります。

This will help you build more responsive, cheaper LLM workflows.
これにより、より応答性が高く、コストのかからないLLMワークフローを構築できます。

_Agentic workflows are often just called agents.
_エージェントワークフローはしばしばエージェントと呼ばれます。

An agent discovers available tools and_ agents, plans which tools or agents to use and in which order, and plans what parameters to use for each task.
エージェントは利用可能なツールとエージェントを発見し、どのツールまたはエージェントをどの順序で使用するかを計画し、各タスクに使用するパラメータを計画します。

The agent’s goal is to discover and use the best available tools/agents to answer the user query.
エージェントの目標は、ユーザーのクエリに答えるために最適な利用可能なツール/エージェントを発見し、使用することです。

In general, the main distinction is that LLM workflows are static graphs of nodes with limited planning and control.
一般的に、主な違いは、LLMワークフローが限られた計画と制御を持つノードの静的グラフであることです。

The agentic _workflow pattern moves beyond static DAGs, where agent control flow is determined_ on the fly.
エージェントワークフローパターンは、エージェントの制御フローがその場で決定される静的DAGを超えます。

Agents require LLMs that support JSON output that is then translated into tool calling.
エージェントは、JSON出力をサポートし、それがツール呼び出しに変換されるLLMを必要とします。

Agents use MCP and A2A to dynamically discover tools and agents, respectively.
エージェントは、それぞれMCPとA2Aを使用してツールとエージェントを動的に発見します。

Agents execute tasks using tools/agents, and they ask clients for feedback to clarify or refine their goal or how they plan to meet their goal.
エージェントはツール/エージェントを使用してタスクを実行し、クライアントにフィードバックを求めて目標を明確にしたり、目標を達成する方法を洗練させたりします。

The agent should autonomously decide when a generated answer is sufficient for the final response or when more work is needed.
エージェントは、生成された回答が最終応答に十分であるか、さらなる作業が必要であるかを自律的に決定する必要があります。

An agentic workflow should have the ability to reason and act to achieve its goal:
エージェントワークフローは、目標を達成するために推論し、行動する能力を持つべきです：

_Discovery_ Use MCP and A2A protocols to discover tools and agents, respectively.
_発見_ MCPとA2Aプロトコルを使用して、それぞれツールとエージェントを発見します。

_Planning_ Break down complex tasks into subtasks and plan the order of tasks. Acquire information needed to successfully execute a task.
_計画_ 複雑なタスクをサブタスクに分解し、タスクの順序を計画します。タスクを成功裏に実行するために必要な情報を取得します。

_Execution_ Use MCP and A2A protocols to execute tools and agents, respectively, and use LLMs for tasks.
_実行_ MCPとA2Aプロトコルを使用して、それぞれツールとエージェントを実行し、タスクにLLMを使用します。

_Reflection_ Examine task results and improve task performance.
_反省_ タスクの結果を検討し、タスクのパフォーマンスを改善します。

Rather than execute a task directly, acquire information about how to evaluate an example first.
タスクを直接実行するのではなく、まず例を評価する方法に関する情報を取得します。

If there are errors executing a task, pass the errors to an LLM to ask it to fix task execution.
タスクの実行にエラーがある場合は、そのエラーをLLMに渡してタスクの実行を修正するように依頼します。

For example, imagine we want to build a credit card customer support agent that can answer the following question: “Why was my credit card transaction flagged as fraud?”
例えば、クレジットカードのカスタマーサポートエージェントを構築したいと考えています。このエージェントは次の質問に答えることができます：「なぜ私のクレジットカード取引が詐欺としてフラグ付けされたのですか？」

You should perform the following actions to help our agent explain to a customer why the transaction was marked as fraud:
この取引が詐欺としてマークされた理由を顧客に説明するために、エージェントを助けるために次のアクションを実行する必要があります：

- Get the most recent credit card transaction for this user that was flagged as fraud.
このユーザーの最近のクレジットカード取引の中で、詐欺としてフラグ付けされたものを取得します。

Use MCP and the feature store along with the user ID.
MCPとフィーチャーストアをユーザーIDとともに使用します。

- As our credit card fraud features are interpretable, you can pass the feature values and their description to an LLM and ask it to explain why the transaction was flagged as fraud.
私たちのクレジットカード詐欺機能は解釈可能であるため、特徴値とその説明をLLMに渡し、なぜ取引が詐欺としてフラグ付けされたのかを説明するように依頼できます。

The more metadata you pass, such as feature importance data, the better the LLM will be at providing a human-understandable justification for why it was marked as fraud.
特徴の重要性データなど、より多くのメタデータを渡すほど、LLMはなぜそれが詐欺としてマークされたのかを人間が理解できる形で正当化するのが得意になります。

###### Planning
###### 計画

Agents use LLMs for planning, but LLMs are not great at planning.
エージェントは計画のためにLLMを使用しますが、LLMは計画が得意ではありません。

Yann LeCun, joint [winner of the Turing Award, has claimed that “auto-regressive LLMs can’t plan…[as](https://oreil.ly/j59au) they] produce their answers with a fixed amount of computation per token.
チューリング賞の共同受賞者であるヤン・ルカンは、「自己回帰型LLMは計画できない…[なぜなら](https://oreil.ly/j59au)彼らはトークンごとに固定された計算量で回答を生成するからです。

There is no way for them to devote more time and effort to solve difficult problems.
彼らが難しい問題を解決するために、より多くの時間と労力を注ぐ方法はありません。

True reasoning and planning would allow the system to search for a solution, using potentially unlimited time for it.”
真の推論と計画は、システムが解決策を探すことを可能にし、それに対して潜在的に無限の時間を使用することを許します。」

This critique indirectly led to the development of LRMs that engage in “thinking” steps.
この批判は、間接的に「思考」ステップに従事するLRMの開発につながりました。

LRMs are models specifically trained or architected for better reasoning capabilities, beyond what’s achieved through prompting alone.
LRMは、プロンプトだけでは達成できないより良い推論能力のために特別に訓練または設計されたモデルです。

LRMs add explicit reasoning processes between special `<think> and` `</think> tokens before producing` responses to clients.
LRMは、クライアントへの応答を生成する前に、特別な`<think>`と`</think>`トークンの間に明示的な推論プロセスを追加します。

As such, LRMs generate more tokens and take a longer time to reply to queries than do regular LLMs.
そのため、LRMは通常のLLMよりも多くのトークンを生成し、クエリに対する応答に時間がかかります。

There is an ongoing debate about whether LLMs and LRMs are able to generate novel plans or whether they just memorize and regurgitate plans.
LLMとLRMが新しい計画を生成できるか、単に計画を記憶して再生するだけなのかについては、現在も議論が続いています。

On the one hand, researchers argue that LRMs approximate Daniel [Kahneman’s System 2 model of the brain: slower, effortful, and deliberative.
一方で、研究者たちはLRMがダニエル・カーネマンの脳のシステム2モデルに近似していると主張しています：遅く、努力を要し、熟慮的です。

Similar to](https://oreil.ly/XImJt) how speech enables an inner monologue in humans, an LRM can state, self-reflect, and adapt its reasoning steps to improve its final response.
人間の内的独白を可能にするように、LRMは自らを述べ、自己反省し、推論ステップを適応させて最終的な応答を改善することができます。

Not all researchers agree, [though, as there is empirical evidence that shows that LRMs just memorize patterns](https://oreil.ly/cWW67) and do not create novel plans.
ただし、すべての研究者が同意しているわけではなく、LRMが単にパターンを記憶し、新しい計画を作成しないことを示す実証的証拠があります。

That said, developers still design agents to use an LLM or LRM to generate plans for which tools or agents to use in which order.
とはいえ、開発者は依然としてエージェントがどのツールやエージェントをどの順序で使用するかを計画を生成するためにLLMまたはLRMを使用するように設計します。

Planning is a search problem, and a router LLM is the simplest of planners: a _classifier, which takes the user query and_ classifies it as the best match with one of its available tools.
計画は探索問題であり、ルータLLMは最も単純なプランナーです：_分類器であり、ユーザーのクエリを受け取り、_利用可能なツールの中で最も適合するものとして分類します。

More general planning requires the agent to generate subgoals, estimate the reward for each potential step (using an LLM, a tool, or an agent), and select a path that maximizes the expected reward over a certain number of steps (the _time horizon).
より一般的な計画には、エージェントがサブゴールを生成し、各潜在的ステップの報酬を推定し（LLM、ツール、またはエージェントを使用）、特定のステップ数（_時間の視野）にわたって期待される報酬を最大化するパスを選択する必要があります。

Sometimes your agent might need to backtrack (LLMs are not good at this because they are autoregressive and only take forward actions), and sometimes your agent might decide that there is no feasible next step.
時には、エージェントがバックトラックする必要があるかもしれません（LLMは自己回帰的であり、前方のアクションしか取らないため、これが得意ではありません）。また、エージェントが実行可能な次のステップがないと判断することもあります。

Given the limitations of LLMs for planning, a good approach in building interactive AI systems is to validate plans by interacting with the client (the user or agent), if possible.
LLMの計画における制限を考慮すると、インタラクティブなAIシステムを構築する際の良いアプローチは、可能であればクライアント（ユーザーまたはエージェント）と対話して計画を検証することです。

The agent can define what it plans to do in a specification related to its task.
エージェントは、タスクに関連する仕様で何を計画しているかを定義できます。

The client can suggest refinements to the specification, and when the client is happy with it, the agent can execute the plan defined in the specification.
クライアントは仕様の改善を提案でき、クライアントが満足したときに、エージェントは仕様で定義された計画を実行できます。

If you cannot have the client validate the specification, you can use heuristics to validate a plan.
クライアントに仕様を検証させることができない場合は、ヒューリスティックを使用して計画を検証できます。

For example, one simple heuristic is to eliminate plans with invalid actions.
例えば、1つの単純なヒューリスティックは、無効なアクションを持つ計画を排除することです。

You can also encode domain-specific knowledge in your agent about the tasks it can execute, and it can use heuristics and reflection to validate a plan.
エージェントが実行できるタスクに関するドメイン固有の知識をエージェントにエンコードし、ヒューリスティックと反省を使用して計画を検証することもできます。

To make debugging agents easier, planning should be decoupled from execution of the plan.
エージェントのデバッグを容易にするために、計画は計画の実行から切り離されるべきです。

If the plan encounters problems, it may need to be refined and revalidated by the client before re-execution.
計画に問題が発生した場合、再実行の前にクライアントによって改善され、再検証される必要があるかもしれません。



. If the plan encounters problems, it may need to be refined and revalidated by the client before re-execution. 
計画に問題が発生した場合、再実行の前にクライアントによって洗練され、再検証される必要があるかもしれません。

It’s important to have a clear trace of an agent’s steps to be able to debug and improve it. 
エージェントのステップの明確なトレースを持つことは、デバッグや改善を行うために重要です。

In general, you should start writing LLM workflows and only progress to writing agents if your requirements demand it. 
一般的に、LLMワークフローの作成から始め、要件が必要とする場合にのみエージェントの作成に進むべきです。

Workflows are best for predictable tasks, and they can be optimized to complete a task faster and at lower cost (by reducing the number of steps and using specialized [cheaper] LLMs for some of the steps). 
ワークフローは予測可能なタスクに最適であり、タスクをより早く、低コストで完了するように最適化できます（ステップ数を減らし、一部のステップに特化した[安価な] LLMを使用することによって）。

You should develop an agent only if you need an autonomous system to solve a problem that is not well defined in advance and where existing services are available as MCP servers or behind A2A APIs. 
事前に明確に定義されていない問題を解決するために自律システムが必要であり、既存のサービスがMCPサーバーまたはA2A APIの背後にある場合にのみ、エージェントを開発すべきです。

###### Security Challenges
###### セキュリティの課題

There are many security challenges in building autonomous agents that generate plans to achieve their goal. 
目標を達成するための計画を生成する自律エージェントを構築する際には、多くのセキュリティの課題があります。

Professor Geoff Hinton, a Turing Award winner, preaches caution in giving agents carte blanche in generating plans, as they “will quickly realize that getting more control is a very good subgoal because it helps you achieve other goals… And if these things get carried away with getting more control, we [humans] are in trouble.” 
チューリング賞受賞者のジェフ・ヒントン教授は、エージェントに計画を自由に生成させることに対して注意を促しています。なぜなら、彼らは「より多くの制御を得ることが非常に良いサブゴールであることをすぐに理解するからです。それは他の目標を達成するのに役立ちます… そして、これらのことがより多くの制御を得ることに夢中になった場合、私たち[人間]は困ったことになります。」

In the near term, however, a common example of a security nightmare is to develop an agent that allows untrusted input but has access to private information that it should not disclose. 
しかし、短期的には、信頼できない入力を許可しながら、開示すべきでないプライベート情報にアクセスできるエージェントを開発することが一般的なセキュリティの悪夢の例です。

It is difficult enough to develop an application with a public API that has access to private data, never mind an agent with a public API that can potentially be circumvented by unscrupulous users. 
プライベートデータにアクセスできるパブリックAPIを持つアプリケーションを開発することは十分に難しいですが、悪意のあるユーザーによって回避される可能性のあるパブリックAPIを持つエージェントを開発することはさらに困難です。

The fundamental challenge is that agents follow instructions encoded in queries, and if untrusted users can provide arbitrary queries, they can attempt to inject their instructions into the LLM, any tools used, and other agents used. 
根本的な課題は、エージェントがクエリにエンコードされた指示に従うことであり、信頼できないユーザーが任意のクエリを提供できる場合、彼らは自分の指示をLLMや使用されるツール、他のエージェントに注入しようとする可能性があるということです。

You should aim to constrain input to agents so that it will be impossible for that input to trigger any negative side effects on the system or its environment. 
エージェントへの入力を制約し、その入力がシステムやその環境に対して悪影響を引き起こすことが不可能になるようにすることを目指すべきです。

In Chapter 14, we will look at using guardrails as a technique to help prevent dangerous inputs into and outputs from agents. 
第14章では、エージェントへの危険な入力や出力を防ぐための手法としてガードレールの使用について見ていきます。

You have to be similarly careful about the libraries you use when you develop an agent. 
エージェントを開発する際に使用するライブラリについても同様に注意が必要です。

If an unscrupulous actor can compromise any software artifact in your program, they can inject their own instructions to agents. 
悪意のある行為者があなたのプログラム内の任意のソフトウェアアーティファクトを侵害できる場合、彼らはエージェントに自分の指示を注入することができます。

Make sure you only use trusted libraries downloaded over secure connections from trusted sources—secure your software supply chain. 
信頼できるソースから安全な接続を介してダウンロードした信頼できるライブラリのみを使用するようにし、ソフトウェアサプライチェーンを確保してください。

This may mean more work for you, though. 
ただし、これはあなたにとってより多くの作業を意味するかもしれません。

For example, you may decide not to use the third-party library that could compromise the security of your agent, and instead reimplement the functionality it provides. 
たとえば、エージェントのセキュリティを脅かす可能性のあるサードパーティライブラリを使用しないことを決定し、その代わりに提供する機能を再実装することを選択するかもしれません。

###### Domain-Specific (Intermediate) Representations
###### ドメイン特化型（中間）表現

Another useful artifact that can be produced as part of an agent is a domain-specific (intermediate) representation of the agents’ proposed output/response. 
エージェントの一部として生成される別の有用なアーティファクトは、エージェントが提案する出力/応答のドメイン特化型（中間）表現です。

Intermediate representations enable user feedback in a domain language that is easily understood by the user. 
中間表現は、ユーザーが容易に理解できるドメイン言語でのユーザーフィードバックを可能にします。

For example, many users are now developing web pages with coding agents, such as Lovable, that provide the generated web page as a domain-specific (intermediate) representation. 
たとえば、多くのユーザーが現在、Lovableのようなコーディングエージェントを使用してウェブページを開発しており、生成されたウェブページをドメイン特化型（中間）表現として提供しています。

Users iteratively improve the web page and don’t need to ever edit or work with the generated TypeScript code. 
ユーザーはウェブページを反復的に改善し、生成されたTypeScriptコードを編集したり作業したりする必要はありません。

Similarly, the Hopsworks Brewer coding agent provides human-readable definitions of feature/training/inference pipeline specifications in YAML, and users can iteratively improve the intermediate representation of those pipelines without having to work directly with Python code generated from it. 
同様に、Hopsworks Brewerコーディングエージェントは、YAMLでの特徴/トレーニング/推論パイプライン仕様の人間が読める定義を提供し、ユーザーはそれから生成されたPythonコードに直接作業することなく、これらのパイプラインの中間表現を反復的に改善できます。

Users do not need to understand the syntax of function signatures with parameters and return types; instead, users can prompt their way to production ML pipelines. 
ユーザーはパラメータや戻り値の型を持つ関数シグネチャの構文を理解する必要はありません。代わりに、ユーザーはプロンプトを使って生産MLパイプラインに到達できます。

A well-crafted prompt that consistently generates good code becomes a valuable asset to save, reuse, and share with others. 
一貫して良いコードを生成する巧妙に作成されたプロンプトは、保存、再利用、他者と共有するための貴重な資産となります。

We already saw an example of this in Chapter 8 when we designed prompts for generating synthetic credit card transaction data. 
この例は、第8章で合成クレジットカード取引データを生成するためのプロンプトを設計したときにすでに見ました。

###### A Development Process for Agents
###### エージェントのための開発プロセス

In Chapter 2, we introduced the MVPS process for building ML systems. 
第2章では、MLシステムを構築するためのMVPSプロセスを紹介しました。

With LLMs and agents, the prediction problem you want to solve becomes a task you want the agent to perform. 
LLMとエージェントを使用すると、解決したい予測問題はエージェントに実行させたいタスクになります。

Agents can perform many tasks. 
エージェントは多くのタスクを実行できます。

Start with one task. 
1つのタスクから始めてください。

You will typically skip the training pipeline and work with a foundation LLM (using one behind an API is the easiest way to get started). 
通常、トレーニングパイプラインをスキップし、基盤となるLLMで作業します（APIの背後にあるものを使用するのが最も簡単な方法です）。

If you need RAG, you will need to write one or more feature pipelines for your RAG data source. 
RAGが必要な場合は、RAGデータソースのために1つ以上のフィーチャーパイプラインを書く必要があります。

However, the inference pipeline (the agent) will require its own development process, presented here. 
ただし、推論パイプライン（エージェント）は、ここで示す独自の開発プロセスを必要とします。

LLM workflows and agents are multistep workflows. 
LLMワークフローとエージェントはマルチステップワークフローです。

They need a more rigorous development methodology than vibe coding, where you experiment with different system prompts until the LLM workflow or agent’s performance “feels right.” 
彼らは、LLMワークフローやエージェントのパフォーマンスが「適切に感じる」まで異なるシステムプロンプトを試すvibe codingよりも、より厳密な開発方法論を必要とします。

A small change in the behavior or performance of any step in a workflow can lead to a massive drop in the quality of the response. 
ワークフロー内の任意のステップの動作やパフォーマンスの小さな変更が、応答の質の大幅な低下につながる可能性があります。

Figure 12-9 shows a simple but effective development process for LLM workflows and agents that involves logging the output and timing of all of the steps, from a user query to MCP calls (including queries and responses for RAG data sources), LLM calls along with the prompt, and the final user response. 
図12-9は、ユーザーのクエリからMCP呼び出し（RAGデータソースのクエリと応答を含む）、プロンプトとともにLLM呼び出し、最終的なユーザー応答までのすべてのステップの出力とタイミングをログに記録する、LLMワークフローとエージェントのためのシンプルで効果的な開発プロセスを示しています。

_Figure 12-9. An iterative development process for improving LLM workflows/agents through the curation of examples from logs, error analysis of the logged examples to derive insights, and use of evals to measure whether changes to agents produce improvements or not._  
_図12-9. ログからの例のキュレーション、ログされた例のエラー分析による洞察の導出、エージェントの変更が改善をもたらすかどうかを測定するための評価の使用を通じて、LLMワークフロー/エージェントを改善するための反復的な開発プロセス。_

The log traces should be stored and made available for error analysis (covered in Chapter 14) that will drive insights into how to improve agent behavior. 
ログトレースは保存され、エージェントの動作を改善する方法に関する洞察を促進するエラー分析（第14章で説明）に利用できるようにするべきです。

For example, you might manually inspect the agent responses and identify common mistakes made by the LLM that can be fixed by updating the system prompt. 
たとえば、エージェントの応答を手動で検査し、システムプロンプトを更新することで修正できるLLMによる一般的な間違いを特定することができます。

Or you might notice that a particular MCP call does not return good enough context information for the LLM. 
または、特定のMCP呼び出しがLLMにとって十分なコンテキスト情報を返さないことに気付くかもしれません。

Evaluations of traces should output a score that indicates whether changes to the agent or LLM workflow improved its performance or not. 
トレースの評価は、エージェントまたはLLMワークフローの変更がそのパフォーマンスを改善したかどうかを示すスコアを出力するべきです。

The most common method of evaluation is direct grading or scoring. 
最も一般的な評価方法は、直接評価またはスコアリングです。

Here, an evaluator assesses an output against a scale (e.g., 1–5 for faithfulness or helpfulness) or categorical labels (e.g., Pass/Fail). 
ここでは、評価者が出力をスケール（例：忠実度や有用性のための1〜5）またはカテゴリラベル（例：合格/不合格）に対して評価します。

Evaluators can be human annotators, domain experts, or a well-prompted “LLM-as-a-judge.” 
評価者は人間のアノテーター、ドメインの専門家、または適切にプロンプトされた「LLMを裁判官として」使用することができます。

Obtaining reliable direct grades demands extremely clear, unambiguous definitions for every possible score or label. 
信頼できる直接評価を得るためには、すべての可能なスコアやラベルに対して非常に明確であいまいでない定義が必要です。

Direct grading is most useful when your primary goal is assessing the absolute quality of a single step’s output against specific, predefined standards. 
直接評価は、主な目標が特定の事前定義された基準に対して単一ステップの出力の絶対的な質を評価することである場合に最も有用です。

Hamel Husain, a prominent LLM educator, claims a benevolent dictator is the best human evaluator—a single person who gives consistent (high-quality) feedback. 
著名なLLM教育者であるハメル・フサインは、善意の独裁者が最良の人間評価者であると主張しています。つまり、一貫した（高品質の）フィードバックを提供する単一の人物です。

We cover evals in more detail in Chapters 13 and 14. 
評価については、第13章と第14章でより詳しく説明します。

###### Agent Deployments in Hopsworks
###### Hopsworksにおけるエージェントの展開

Hopsworks supports deploying agents as LlamaIndex Python programs with A2A APIs for client interaction and MCP services, as illustrated in Figure 12-10. 
Hopsworksは、クライアントとのインタラクションとMCPサービスのために、エージェントをLlamaIndex PythonプログラムとしてA2A APIで展開することをサポートしています。図12-10に示されています。

_Figure 12-10. Agent deployments in Hopsworks wired up to LLMs, MCP services, and logging._  
_図12-10. LLM、MCPサービス、およびログに接続されたHopsworksのエージェント展開。_

In Hopsworks, agents run as Knative containers, and Hopsworks provides RAG services with the feature store and vector index, tracing/logs with Opik, and LLM serving with vLLM on KServe. 
Hopsworksでは、エージェントはKnativeコンテナとして実行され、Hopsworksはフィーチャーストアとベクトルインデックスを使用したRAGサービス、Opikを使用したトレース/ログ、およびKServe上のvLLMを使用したLLMサービスを提供します。

Agents support the A2A API, using `HOPSWORKS_API_KEY for` authentication and access control by adding an annotation to classes: 
エージェントはA2A APIをサポートしており、クラスにアノテーションを追加することで認証とアクセス制御のために`HOPSWORKS_API_KEY`を使用します：

```  
   @hopsworks.a2a.agent()  
   class MyAgent: # The name of the class is the name of the agent  
     # This decorator registers the method as a skill  
     @hopsworks.a2a.skill(...)  
     def skillA(...):  
       """Description of skill A."""  
```

Hopsworks supports the Envoy AI Gateway. 
HopsworksはEnvoy AI Gatewayをサポートしています。

An AI gateway decouples LLM clients from the target LLM, enabling you to easily replace one LLM with another for all agents in a system. 
AIゲートウェイはLLMクライアントをターゲットLLMから切り離し、システム内のすべてのエージェントに対して1つのLLMを別のLLMに簡単に置き換えることを可能にします。

The AI gateway also enables:
AIゲートウェイはまた、以下を可能にします：



- Rate limiting clients (agents) based on token throughput
- Token cost tracking and attribution to agents/projects in Hopsworks
- LLM metrics, such as token throughput and time-to-first-token
- Centralized security, governance, and auditing for LLMs
クライアント（エージェント）をトークンスループットに基づいて制限します。
KServe/vLLMは、サービスレベル契約（SLA）を満たすためにLLMを提供するために使用されるGPUの数を負荷分散し、弾力的にスケーリングアップ/ダウンします。最後に、エージェントは、KServeモデルが第11章でサポートしている青/緑デプロイメントと同様にA/Bテストを行う必要があります。

###### Summary and Exercises 要約と演習
In this chapter, we introduced LLM workflows and agents as programs with varying levels of autonomy that use system prompts and RAG to fill a prompt with just the right information needed to solve a task using an LLM. 
この章では、LLMワークフローとエージェントを、システムプロンプトとRAGを使用してタスクを解決するために必要な正確な情報でプロンプトを埋める、さまざまな自律性レベルを持つプログラムとして紹介しました。 
We saw that constraining autonomy with workflows helps build more reliable LLM-powered services. 
ワークフローで自律性を制約することが、より信頼性の高いLLM駆動のサービスを構築するのに役立つことがわかりました。 
We also saw that the trend is toward increasingly autonomous agents that discover and use tools and other agents to achieve their goals. 
また、目標を達成するためにツールや他のエージェントを発見し使用する、ますます自律的なエージェントへの傾向があることもわかりました。 
There are still challenges surrounding security and planning, and the interoperability standards, MCP and A2A, are important but still in their infancy. 
セキュリティと計画に関する課題は依然として存在し、相互運用性基準であるMCPとA2Aは重要ですが、まだ初期段階にあります。 
Despite this, it is an exciting time to build artificially intelligent programs that interact with their environment and work in a goal-directed manner. 
それにもかかわらず、環境と相互作用し、目標指向の方法で機能する人工知能プログラムを構築するのはエキサイティングな時期です。 

The following exercise will help you learn context engineering for an agent:
次の演習は、エージェントのコンテキストエンジニアリングを学ぶのに役立ちます：
Retail customer support agent: “Can I get a refund for product Foo that I ordered last week?”
小売顧客サポートエージェント：「先週注文した商品Fooの返金を受けることはできますか？」 
Design an agent that can:
エージェントを設計してください：
- Retrieve the order information using the order ID provided by the user. The order includes when the item was bought, its price, and any special conditions (such as a limited returns policy).
- ユーザーが提供した注文IDを使用して注文情報を取得します。注文には、アイテムが購入された日時、価格、および特別な条件（制限付き返品ポリシーなど）が含まれます。
- Retrieve and check the refund policy from a PDF document.
- PDFドキュメントから返金ポリシーを取得して確認します。
- Generate a refund plan and response.
- 返金計画と応答を生成します。

-----
###### PART VI #### MLOps and LLMOps

-----
-----

