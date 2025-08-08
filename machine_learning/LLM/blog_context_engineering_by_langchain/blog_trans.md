refs: https://blog.langchain.com/the-rise-of-context-engineering/

# The rise of "context engineering" 「コンテキストエンジニアリング」の台頭

Header image from Dex Horthy on Twitter. ヘッダー画像はTwitterのDex Horthyからのものです。

Context engineering is building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task. 
コンテキストエンジニアリングとは、**LLM（大規模言語モデル）がタスクを信頼性を持って達成できるように、適切な情報とツールを適切な形式で提供する動的システムを構築すること**です。

Most of the time when an agent is not performing reliably the underlying cause is that the appropriate context, instructions and tools have not been communicated to the model. 
エージェントが信頼性を持って機能しない場合、その根本的な原因は、適切なコンテキスト、指示、およびツールがモデルに伝達されていないことです。

LLM applications are evolving from single prompts to more complex, dynamic agentic systems. 
LLMアプリケーションは、単一のプロンプトからより複雑で動的なエージェントシステムへと進化しています。

As such, context engineering is becoming the most important skill an AI engineer can develop. 
そのため、コンテキストエンジニアリングはAIエンジニアが身につけるべき最も重要なスキルになりつつあります。

<!-- ここまでよんだ! -->

## What is context engineering? コンテキストエンジニアリングとは？

Context engineering is building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task.  
コンテキストエンジニアリングとは、LLM（大規模言語モデル）がタスクを実行できるように、適切な情報とツールを適切な形式で提供する動的システムを構築することです。

This is the definition that I like, which builds upon recent takes on this from Tobi Lutke, Ankur Goyal, and Walden Yan. Let’s break it down.  
これは、Tobi Lutke、Ankur Goyal、Walden Yanの最近の見解に基づいた私の好きな定義です。それを分解してみましょう。

### Context engineering is a system  コンテキストエンジニアリングはシステムです。

Complex agents likely get context from many sources.  
複雑なエージェントは、多くのソースからコンテキストを取得する可能性があります。
Context can come from the developer of the application, the user, previous interactions, tool calls, or other external data.  
コンテキストは、アプリケーションの開発者、ユーザー、以前のインタラクション、ツールの呼び出し、または他の外部データから得られることがあります。
Pulling these all together involves a complex system.  
これらすべてを統合することは、複雑なシステムを必要とします。

### This system is dynamic このシステムは動的です。

Many of these pieces of context can come in dynamically.  
これらのコンテキストの多くは動的に入ってくる可能性があります。
As such, the logic for constructing the final prompt needs to be dynamic as well.  
したがって、最終的なプロンプトを構築するためのロジックも動的である必要があります。
It is not just a static prompt.  
それは単なる静的なプロンプトではありません。

### You need the right information   適切な情報が必要です。

A common reason agentic systems don’t perform is they just don’t have the right context.  
エージェントシステムが機能しない一般的な理由は、適切なコンテキストを持っていないからです。
LLMs cannot read minds - you need to give them the right information.  
LLMは心を読むことができません - 彼らに適切な情報を与える必要があります。
**Garbage in, garbage out.**  
ゴミを入れれば、ゴミが出るのです。

### You need the right tools  適切なツールが必要です。

It may not always be the case that the LLM will be able to solve the task just based solely on the inputs.  
LLMが入力だけでタスクを解決できるとは限りません。
In these situations, if you want to empower the LLM to do so, you will want to make sure that it has the right tools.  
このような状況では、LLMにその能力を与えたい場合、適切なツールを持っていることを確認する必要があります。
These could be tools to look up more information, take actions, or anything in between.  
これらは、より多くの情報を調べたり、アクションを実行したり、その中間の何かである可能性があります。
Giving the LLM the right tools is just as important as giving it the right information.  
**LLMに適切なツールを与えることは、適切な情報を与えることと同じくらい重要**です。

### The format matters  形式も重要です。

Just like communicating with humans, how you communicate with LLMs matters.  
人間とコミュニケーションを取るのと同様に、LLMとのコミュニケーションの仕方も重要です。
A short but descriptive error message will go a lot further than a large JSON blob.  
短くても説明的なエラーメッセージは、大きなJSONの塊よりもはるかに効果的です。
This also applies to tools.  
これはツールにも当てはまります。
What the input parameters to your tools are matters a lot when making sure that LLMs can use them.  
ツールへの入力パラメータが何であるかは、LLMがそれらを使用できるようにするために非常に重要です。

### Can it plausibly accomplish the task?  それはタスクを実行できる可能性がありますか？

This is a great question to be asking as you think about context engineering.  
これは、コンテキストエンジニアリングについて考える際に尋ねるべき素晴らしい質問です。
It reinforces that LLMs are not mind readers - you need to set them up for success.  
これは、LLMが心を読むことができないことを強調します - 彼らを成功に導くための準備をする必要があります。
It also helps separate the failure modes.  
また、失敗モードを区別するのにも役立ちます。
Is it failing because you haven’t given it the right information or tools?  
それは、適切な情報やツールを与えていないために失敗しているのですか？
Or does it have all the right information and it just messed up?  
それとも、すべての適切な情報を持っているが、単に失敗したのですか？
These failure modes have very different ways to fix them.  
これらの失敗モードには、それぞれ異なる修正方法があります。

<!-- ここまでよんだ! -->

## Why is context engineering important なぜコンテキストエンジニアリングが重要なのか

When agentic systems mess up, it’s largely because an LLM messes. 
エージェントシステムが失敗するのは、主にLLMが失敗するからです。
Thinking from first principles, LLMs can mess up for two reasons: 
**第一原理から考えると、LLMが失敗する理由は2つ**あります。

1. The underlying model just messed up, it isn’t good enough  基本的なモデルが単に失敗した、十分ではない

1. The underlying model was not passed the appropriate context to make a good output 基本的なモデルに良い出力を生成するための適切なコンテキストが渡されなかった

More often than not (especially as the models get better) model mistakes are caused more by the second reason. 
**ほとんどの場合（特にモデルが改善されるにつれて）、モデルのミスは2つ目の理由によって引き起こされます。**
The context passed to the model may be bad for a few reasons: 
モデルに渡されるコンテキストが悪い理由はいくつかあります。

- There is just missing context that the model would need to make the right decision. 
  モデルが正しい決定を下すために**必要なコンテキストが欠けている**ことがあります。
    Models are not mind readers. 
    モデルは心を読むことはできません。
If you do not give them the right context, they won’t know it exists. 
適切なコンテキストを与えなければ、存在することすら分からないのです。

- The context is formatted poorly. 
- **コンテキストのフォーマットが不適切**です。

Just like humans, communication is important! 
人間と同様に、コミュニケーションは重要です！
How you format data when passing into a model absolutely affects how it responds 
モデルにデータを渡す際のフォーマットは、モデルの応答に絶対的に影響を与えます。

<!-- ここまでよんだ! -->

## How is context engineering different from prompt engineering? コンテキストエンジニアリングはプロンプトエンジニアリングとどのように異なるのか？

Why the shift from “prompts” to “context”? 
なぜ「プロンプト」から「コンテキスト」への移行があるのでしょうか？
Early on, developers focused on phrasing prompts cleverly to coax better answers. 
初期の頃、開発者はより良い回答を引き出すためにプロンプトを巧妙に表現することに注力していました。
But as applications grow more complex, it’s becoming clear that providing complete and structured context to the AI is far more important than any magic wording. 
しかし、アプリケーションがより複雑になるにつれて、**AIに完全で構造化されたコンテキストを提供すること**が、どんな魔法のような言葉よりもはるかに重要であることが明らかになっています。

I would also argue that prompt engineering is a subset of context engineering. 
私も、**プロンプトエンジニアリングはコンテキストエンジニアリングの一部である**と主張します。
Even if you have all the context, how you assemble it in the prompt still absolutely matters. 
たとえすべてのコンテキストを持っていても、それをプロンプトにどのように組み立てるかは依然として非常に重要です。
The difference is that you are not architecting your prompt to work well with a single set of input data, but rather to take a set of dynamic data and format it properly. 
違いは、単一の入力データセットに対してうまく機能するようにプロンプトを設計するのではなく、動的なデータセットを取り込み、それを適切にフォーマットすることです。

I would also highlight that a key part of context is often core instructions for how the LLM should behave. 
また、コンテキストの重要な部分は、LLMがどのように振る舞うべきかに関する基本的な指示であることが多いと強調したいです。
This is often a key part of prompt engineering. 
これはしばしばプロンプトエンジニアリングの重要な部分です。
Would you say that providing clear and detailed instructions for how the agent should behave is context engineering or prompt engineering? 
エージェントがどのように振る舞うべきかについて明確で詳細な指示を提供することは、コンテキストエンジニアリングですか、それともプロンプトエンジニアリングですか？
I think it’s a bit of both. 
私はそれは両方の要素を含んでいると思います。

<!-- ここまでよんだ! -->

## Examples of context engineering コンテキストエンジニアリングの例

Some basic examples of good context engineering include:
良いコンテキストエンジニアリングの基本的な例には以下が含まれます：

- Tool use: Making sure that if an agent needs access to external information, it has tools that can access it. 
- ツールの使用：エージェントが外部情報にアクセスする必要がある場合、それにアクセスできるツールを持っていることを確認します。
When tools return information, they are formatted in a way that is maximally digestable for LLMs.
ツールが情報を返すとき、それはLLM（大規模言語モデル）にとって最大限に消化しやすい形式でフォーマットされます。

- Short term memory: If a conversation is going on for a while, creating a summary of the conversation and using that in the future.
    短期記憶：会話がしばらく続いている場合、その会話の要約を作成し、将来それを使用します。

- Long term memory: If a user has expressed preferences in a previous conversation, being able to fetch that information.
    長期記憶：ユーザーが以前の会話で好みを表明した場合、その情報を取得できること。

- Prompt Engineering: Instructions for how an agent should behave are clearly enumerated in the prompt.
    プロンプトエンジニアリング：エージェントがどのように振る舞うべきかの指示がプロンプトに明確に列挙されています。

- Retrieval: Fetching information dynamically and inserting it into the prompt before calling the LLM.
    リトリーバル：情報を動的に取得し、LLMを呼び出す前にそれをプロンプトに挿入します。

<!-- ここまでよんだ! -->

## How LangGraph enables context engineering LangGraphがコンテキストエンジニアリングを可能にする方法

When we built LangGraph, we built it with the goal of making it the most controllable agent framework. 
私たちがLangGraphを構築したとき、最も制御可能なエージェントフレームワークを作ることを目指しました。 
This also allows it to perfectly enable context engineering. 
これにより、コンテキストエンジニアリングを完璧に実現することができます。

With LangGraph, you can control everything. 
**LangGraphを使用すると、すべてを制御できます**。
You decide what steps are run. 
どのステップを実行するかを決定します。
You decide exactly what goes into your LLM. 
LLMに何を正確に入れるかを決定します。
You decide where you store the outputs. 
**出力をどこに保存するか**を決定します。
You control everything. 
すべてを制御します。

This allows you do all the context engineering you desire. 
これにより、望むすべてのコンテキストエンジニアリングを行うことができます。
One of the downsides of agent abstractions (which most other agent frameworks emphasize) is that they restrict context engineering. 
**エージェントの抽象化（ほとんどの他のエージェントフレームワークが強調するもの）の欠点の一つは、コンテキストエンジニアリングを制限すること**です。(なるほど。まあこれはトレードオフか〜:thinking:)
There may be places where you cannot change exactly what goes into the LLM, or exactly what steps are run beforehand. 
LLMに何を正確に入れるか、または事前にどのステップが実行されるかを正確に変更できない場所があるかもしれません。

Side note: a very good read is Dex Horthy's "12 Factor Agents". 
余談ですが、**非常に良い読み物はDex Horthyの「[12 Factor Agents](https://github.com/humanlayer/12-factor-agents?ref=blog.langchain.com)」です**。(へぇ〜読んでみるか〜:thinking:)
A lot of the points there relate to context engineering ("own your prompts", "own your context building", etc). 
そこにある多くのポイントは、コンテキストエンジニアリングに関連しています（「プロンプトを所有する」、「コンテキスト構築を所有する」など）。
The header image for this blog is also taken from Dex. 
このブログのヘッダー画像もDexから取られています。
We really enjoy the way he communicates about what is important in the space. 
私たちは、彼がこの分野で重要なことについてどのようにコミュニケーションをとるかを本当に楽しんでいます。

<!-- ここまでよんだ! -->

## How LangSmith helps with context engineering LangSmithがコンテキストエンジニアリングをどのように支援するか

LangSmith is our LLM application observability and evals solution. 
LangSmithは、私たちのLLMアプリケーションの可観測性と評価ソリューションです。
One of the key features in LangSmith is the ability to trace your agent calls. 
LangSmithの主要な機能の1つは、**エージェント呼び出しをtracingする能力**です。
Although the term "context engineering" didn't exist when we built LangSmith, it aptly describes what this tracing helps with. 
私たちがLangSmithを構築したとき、「コンテキストエンジニアリング」という用語は存在しませんでしたが、この追跡が助けることを的確に表現しています。

LangSmith lets you see all the steps that happen in your agent. 
LangSmithは、エージェント内で発生するすべてのステップを確認できるようにします。
This lets you see what steps were run to gather the data that was sent into the LLM. 
これにより、LLMに送信されたデータを収集するために実行されたステップを確認できます。

LangSmith lets you see the exact inputs and outputs to the LLM. 
**LangSmithは、LLMへの正確な入力と出力を確認**できるようにします。
This lets you see exactly what went into the LLM - the data it had and how it was formatted. 
これにより、LLMに何が入力されたのか、どのようなデータがあり、どのようにフォーマットされていたのかを正確に確認できます。
You can then debug whether that contains all the relevant information that is needed for the task. 
その後、それがタスクに必要なすべての関連情報を含んでいるかどうかをデバッグできます。
This includes what tools the LLM has access to - so you can debug whether it's been given the appropriate tools to help with the task at hand. 
これには、LLMがアクセスできるツールが含まれます。したがって、タスクを支援するために適切なツールが与えられているかどうかをデバッグできます。

<!-- ここまでよんだ! -->

## Communication is all you need コミュニケーションが全て

A few months ago I wrote a blog called "Communication is all you need". 
数ヶ月前、私は「コミュニケーションが全て」というタイトルのブログを書きました。 
The main point was that communicating to the LLM is hard, and not appreciated enough, and often the root cause of a lot of agent errors. 
主なポイントは、LLM（大規模言語モデル）とのコミュニケーションが難しく、十分に評価されておらず、多くのエージェントエラーの根本的な原因であることです。 
Many of these points have to do with context engineering! 
これらの多くのポイントは、コンテキストエンジニアリングに関係しています！

Context engineering isn't a new idea - agent builders have been doing it for the past year or two. 
コンテキストエンジニアリングは新しいアイデアではありません - エージェントビルダーは過去1、2年の間にそれを行ってきました。 
It's a new term that aptly describes an increasingly important skill. 
これは、ますます重要なスキルを適切に表現する新しい用語です。 
We'll be writing and sharing more on this topic. 
私たちはこのトピックについてさらに書き、共有していく予定です。 
We think a lot of the tools we've built (LangGraph, LangSmith) are perfectly built to enable context engineering, and so we're excited to see the emphasis on this take off. 
私たちは、私たちが構築した多くのツール（LangGraph、LangSmith）がコンテキストエンジニアリングを可能にするために完璧に作られていると考えており、この重要性が高まるのを見るのを楽しみにしています。

<!-- ここまでよんだ! -->
