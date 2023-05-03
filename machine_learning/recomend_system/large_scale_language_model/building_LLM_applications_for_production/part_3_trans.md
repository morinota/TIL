## link リンク

- https://huyenchip.com/2023/04/11/llm-engineering.html#part_3_promising_use_cases https://huyenchip.com/2023/04/11/llm-engineering.html#part_3_promising_use_cases

# Part 3. Promising use cases 第3部 有望な使用例

The Internet has been flooded with cool demos of applications built with LLMs.
インターネット上には、LLMで構築されたアプリケーションのクールなデモがあふれています。
Here are some of the most common and promising applications that I’ve seen.
ここでは、よく見かける、有望なアプリケーションを紹介します。
I’m sure that I’m missing a ton.
きっとトンチンカンなことを言ってるんだろうな。

For more ideas, check out the projects from two hackathons I’ve seen:
より多くのアイデアを得るために、私が見た2つのハッカソンでのプロジェクトをご覧ください：

- GPT-4 Hackathon Code Results [Mar 25, 2023] GPT-4ハッカソンコード結果発表【2023年3月25日開催

- Langchain / Gen Mo Hackathon [Feb 25, 2023] Langchain／ゲンモハッカソン【2023年2月25日】のご案内

## AI assistant AIアシスタント

This is hands down the most popular consumer use case.
これは、消費者のユースケースとして最も人気のあるものです。
There are AI assistants built for different tasks for different groups of users – AI assistants for scheduling, making notes, pair programming, responding to emails, helping with parents, making reservations, booking flights, shopping, etc.
スケジュール管理、メモ作り、ペアプログラミング、メール対応、親の手伝い、予約、航空券予約、買い物などのAIアシスタントなど、ユーザーグループごとに異なるタスクのために作られたAIアシスタントが存在します。
– but, of course, the ultimate goal is an assistant that can assist you in everything.
- が、もちろん、最終的な目標は、すべてをアシストしてくれるアシスタントです。

This is also the holy grail that all big companies are working towards for years: Google with Google Assistant and Bard, Facebook with M and Blender, OpenAI (and by extension, Microsoft) with ChatGPT.
これは、すべての大企業が何年もかけて目指している聖杯でもあります： GoogleはGoogle AssistantとBardを、FacebookはMとBlenderを、OpenAIは（ひいてはMicrosoftも）ChatGPTを。
Quora, which has a very high risk of being replaced by AIs, released their own app Poe that lets you chat with multiple LLMs.
AIに取って代わられるリスクが非常に高いQuoraは、複数のLLMとチャットできる自社アプリ「Poe」をリリースしました。
I’m surprised Apple and Amazon haven’t joined the race yet.
アップルやアマゾンがまだ参戦していないのが不思議なくらいです。

## Chatbot チャットボット

Chatbots are similar to AI assistants in terms of APIs.
チャットボットは、APIという点ではAIアシスタントに近いものがあります。
If AI assistants’ goal is to fulfill tasks given by users, whereas chatbots’ goal is to be more of a companion.
AIアシスタントの目的がユーザーから与えられたタスクをこなすことであるのに対し、チャットボットの目的がよりコンパニオン的なものであるとすれば。
For example, you can have chatbots that talk like celebrities, game/movie/book characters, businesspeople, authors, etc.
例えば、有名人、ゲーム・映画・本のキャラクター、ビジネスマン、作家などのように話すチャットボットを用意することができます。

Michelle Huang used her childhood journal entries as part of the prompt to GPT-3 to talk to the inner child.
Michelle Huangは、GPT-3へのプロンプトの一部として、幼少期の日記を使い、インナーチャイルドと対話しました。

The most interesting company in the consuming-chatbot space is probably Character.ai.
消費型チャットボットの領域で最も興味深い企業は、Character.aiでしょう。
It’s a platform for people to create and share chatbots.
チャットボットを作成し、共有するためのプラットフォームです。
The most popular types of chatbots on the platform, as writing, are anime and game characters, but you can also talk to a psychologist, a pair programming partner, or a language practice partner.
プラットフォーム上のチャットボットの種類は、ライティングの通り、アニメやゲームのキャラクターが人気ですが、心理学者やペアプログラミングのパートナー、語学練習のパートナーに話しかけることもできます。
You can talk, act, draw pictures, play text-based games (like AI Dungeon), and even enable voices for characters.
話す、演じる、絵を描く、テキストベースのゲーム（AIダンジョンなど）をする、さらにキャラクターのボイスを有効にすることも可能です。
I tried a few popular chatbots – none of them seem to be able to hold a conversation yet, but we’re just at the beginning.
人気のあるチャットボットをいくつか試してみましたが、どれもまだ会話が成立していないようで、まだ始まったばかりです。
Things can get even more interesting if there’s a revenue-sharing model so that chatbot creators can get paid.
チャットボットのクリエイターが報酬を得られるようなレベニューシェアモデルがあれば、さらに面白くなりますね。

## Programming and gaming プログラミングとゲーム

This is another popular category of LLM applications, as LLMs turn out to be incredibly good at writing and debugging code.
LLMはコードを書いたりデバッグしたりするのが得意なので、これもLLMアプリケーションの人気カテゴリーです。
GitHub Copilot is a pioneer (whose VSCode extension has had 5 million downloads as of writing).
GitHub Copilotはその先駆者です（そのVSCode拡張は執筆時点で500万ダウンロードを記録しています）。
There have been pretty cool demos of using LLMs to write code:
LLMを使ってコードを書くという、かなりクールなデモが行われています：

- 1. Create web apps from natural languages 1. 自然言語からWebアプリを作る

- 2. Find security threats: Socket AI examines npm and PyPI packages in your codebase for security threats. When a potential issue is detected, they use ChatGPT to summarize findings. 2. セキュリティの脅威を見つける： Socket AIは、コードベース内のnpmやPyPIパッケージを調査し、セキュリティ上の脅威がないかどうかを確認します。 潜在的な問題が検出された場合、ChatGPTを使って調査結果をまとめているそうです。

- 3. Gaming 3. ゲーミング

- 3.1 Create games: e.g. Wyatt Cheng has an awesome video showing how he used ChatGPT to clone Flappy Bird. 3.1 ゲームを作る：例えばWyatt Chengは、ChatGPTを使ってFlappy Birdのクローンを作る方法を紹介した素晴らしいビデオを持っています。

- 3.2 Generate game characters. 3.2 ゲームキャラクターを生成する。

- 3.3 Let you have more realistic conversations with game characters: check out this awesome demo by Convai! 3.3 ゲームキャラクターとよりリアルな会話ができる：Convaiによる素晴らしいデモをご覧ください！

## Learning 

Whenever ChatGPT was down, OpenAI discord is flooded with students complaining about not being to complete their homework.
ChatGPTがダウンするたびに、OpenAIのdiscordは、宿題を完成させられないと文句を言う学生で溢れかえっています。
Some responded by banning the use of ChatGPT in school altogether.
学校でのChatGPTの使用を全面的に禁止することで対応したところもありました。
Some have a much better idea: how to incorporate ChatGPT to help students learn even faster.
ChatGPTを取り入れることで、生徒の学習スピードをさらに上げることができるという、もっと優れたアイデアもあります。
All EdTech companies I know are going full-speed on ChatGPT exploration.
私が知っているEdTech企業はみな、ChatGPTの探索に全速力で取り組んでいます。

Some use cases:
使用例もあります：

- Summarize books 本を要約する

- Automatically generate quizzes to make sure students understand a book or a lecture. Not only ChatGPT can generate questions, but it can also evaluate whether a student’s input answers are correct. 書籍や講義の内容を理解させるための小テストを自動生成する。 ChatGPTは問題を生成するだけでなく、生徒が入力した答えが正しいかどうかを評価することも可能です。

- I tried and ChatGPT seemed pretty good at generating quizzes for Designing Machine Learning Systems. Will publish the quizzes generated soon! 試してみたところ、ChatGPTは「Designing Machine Learning Systems」のクイズを生成するのにかなり適しているようでした。 近日中に生成されたクイズを公開する予定です！

- Grade / give feedback on essays エッセイの採点・フィードバック

- Walk through math solutions ウォークスルー数学ソリューション

- Be a debate partner: ChatGPT is really good at taking different sides of the same debate topic. ディベートのパートナーになる ChatGPTは、同じディベートトピックで異なる立場を取るのがとても上手です。

With the rise of homeschooling, I expect to see a lot of applications of ChatGPT to help parents homeschool.
ホームスクーリングが盛んになってきたこともあり、保護者のホームスクーリングを支援するためにChatGPTの応用が期待されますね。

## Talk-to-your-data Talk-to-your-data

This is, in my observation, the most popular enterprise application (so far).
これは、私の観察では、最も人気のあるエンタープライズアプリケーションです（今のところ）。
Many, many startups are building tools to let enterprise users query their internal data and policies in natural languages or in the Q&A fashion.
多くのスタートアップ企業が、企業ユーザーが自然言語やQ&A方式で社内のデータやポリシーを照会できるツールを構築しています。
Some focus on verticals such as legal contracts, resumes, financial data, or customer support.
法律上の契約書、履歴書、財務データ、カスタマーサポートなど、垂直方向に焦点を当てたものもあります。
Given a company’s all documentations, policies, and FAQs, you can build a chatbot that can respond your customer support requests.
企業のすべての文書、ポリシー、FAQがあれば、カスタマーサポートの要求に応えることができるチャットボットを構築することができます。

The main way to do this application usually involves these 4 steps:
このアプリケーションの主な方法は、通常、次の4つのステップを踏むことになります：

- 1. Organize your internal data into a database (SQL database, graph database, embedding/vector database, or just text database) 1. 社内データをデータベース（SQLデータベース、グラフデータベース、埋め込み/ベクトルデータベース、または単なるテキストデータベース）に整理する。

- 2. Given an input in natural language, convert it into the query language of the internal database. For example, if it’s a SQL or graph database, this process can return a SQL query. If it’s embedding database, it’s might be an ANN (approximate nearest neighbor) retrieval query. If it’s just purely text, this process can extract a search query. 2. 自然言語で入力された場合、内部データベースのクエリ言語に変換する。 例えば、SQLやグラフのデータベースであれば、この処理でSQLクエリを返すことができます。 埋め込みデータベースであれば、ANN（近似最近傍）検索クエリかもしれませんね。 純粋なテキストだけであれば、この処理で検索クエリを抽出することができます。

- 3. Execute the query in the database to obtain the query result. 3. データベースでクエリを実行し、クエリ結果を取得する。

- 4. Translate this query result into natural language. 4. このクエリ結果を自然言語に翻訳する。

While this makes for really cool demos, I’m not sure how defensible this category is.
これはとてもクールなデモになりますが、このカテゴリーがどの程度守備範囲なのかはわかりません。
I’ve seen startups building applications to let users query on top of databases like Google Drive or Notion, and it feels like that’s a feature Google Drive or Notion can implement in a week.
Google DriveやNotionのようなデータベースの上でユーザーにクエリを実行させるアプリケーションを構築しているスタートアップを見たことがありますが、それはGoogle DriveやNotionが1週間で実装できる機能であるように感じられます。

OpenAI has a pretty good tutorial on how to talk to your vector database.
OpenAIには、ベクターデータベースと会話する方法について、かなり良いチュートリアルがあります。

### Can LLMs do data analysis for me? LLMはデータ解析をしてくれるのか？

I tried inputting some data into gpt-3.5-turbo, and it seems to be able to detect some patterns.
gpt-3.5-turboにデータを入力してみたところ、いくつかのパターンを検出することができるようです。
However, this only works for small data that can fit into the input prompt.
ただし、これは入力プロンプトに収まるような小さなデータに対してのみ有効です。
Most production data is larger than that.
ほとんどのプロダクションデータはそれよりも大きいです。

## Search and recommendation 検索・推薦

Search and recommendation has always been the bread and butter of enterprise use cases.
検索とレコメンデーションは、常に企業のユースケースの糧となっています。
It’s going through a renaissance with LLMs.
LLMでルネッサンスを迎えているのです。
Search has been mostly keyword-based: you need a tent, you search for a tent.
これまでの検索は、テントが必要だからテントを検索するというように、キーワードベースのものがほとんどでした。
But what if you don’t know what you need yet? For example, if you’re going camping in the woods in Oregon in November, you might end up doing something like this:
しかし、まだ何が必要なのかわからない場合はどうでしょう？例えば、11月にオレゴンの森にキャンプに行くとしたら、こんな感じになるかもしれません：

- 1. Search to read about other people’s experiences. 1. 他の人の体験談を読むために検索する。

- 2. Read those blog posts and manually extract a list of items you need. 2. それらのブログ記事を読み、必要なアイテムのリストを手動で抽出します。

- 3. Search for each of these items, either on Google or other websites. 3. それぞれの項目について、Googleなどで検索してみてください。

If you search for “things you need for camping in oregon in november” directly on Amazon or any e-commerce website, you’ll get something like this:
AmazonなどのECサイトで直接「things you need for camping in oregon in november」と検索すると、このようなものが出てきます：

But what if searching for “things you need for camping in oregon in november” on Amazon actually returns you a list of things you need for your camping trip?
しかし、Amazonで「things you need for camping in oregon in november」と検索すると、実際にキャンプに必要なもののリストが返ってくるとしたらどうでしょう。

It’s possible today with LLMs.
LLMで今日も可能です。
For example, the application can be broken into the following steps:
例えば、アプリケーションは次のようなステップに分けることができます：

- Task 1: convert the user query into a list of product names [LLM] タスク1：ユーザークエリを商品名のリストに変換する[LLM]。

- Task 2: for each product name in the list, retrieve relevant products from your product catalog. タスク2：リスト内の各商品名について、商品カタログから関連商品を取得する。

If this works, I wonder if we’ll have LLM SEO: techniques to get your products recommended by LLMs.
これがうまくいけば、「LLM SEO：LLMに商品を薦めてもらうためのテクニック」なんていうのも出てくるのかな。

## Sales 

The most obvious way to use LLMs for sales is to write sales emails.
LLMを営業に活用する方法として最もわかりやすいのは、営業メールの作成です。
But nobody really wants more or better sales emails.
しかし、誰も本当にもっともっと良いセールスメールを望んでいるわけではありません。
However, several companies in my network are using LLMs to synthesize information about a company to see what they need.
しかし、私のネットワークでは、LLMを使って企業の情報を総合的に判断し、何が必要かを確認する企業がいくつかあります。

## SEO SEO

SEO is about to get very weird.
SEOは非常に奇妙なことになろうとしている。
Many companies today rely on creating a lot of content hoping to rank high on Google.
今日、多くの企業が、Googleで上位に表示されることを期待して、多くのコンテンツを作成することに依存しています。
However, given that LLMs are REALLY good at generating content, and I already know a few startups whose service is to create unlimited SEO-optimized content for any given keyword, search engines will be flooded.
しかし、LLMはコンテンツを作るのが本当に上手で、与えられたキーワードに対してSEOに最適化されたコンテンツを無制限に作ることをサービスにしているスタートアップをすでにいくつか知っていることを考えると、検索エンジンは殺到することでしょう。
SEO might become even more of a cat-and-mouse game: search engines come up with new algorithms to detect AI-generated content, and companies get better at bypassing these algorithms.
検索エンジンはAIが生成したコンテンツを検出するための新しいアルゴリズムを考え出し、企業はそのアルゴリズムを回避することに長けているため、SEOはさらに猫とネズミのゲームになるかもしれません。
People might also rely less on search, and more on brands (e.g.trust only the content created by certain people or companies).
また、人々は検索に頼らず、ブランドに頼るようになるかもしれません（例えば、特定の人物や企業が作成したコンテンツだけを信頼する）。

And we haven’t even touched on SEO for LLMs yet: how to inject your content into LLMs’ responses!!
また、LLMのためのSEOについてはまだ触れていません。LLMの反応にあなたのコンテンツを注入する方法です！

# Conclusion 結論

We’re still in the early days of LLMs applications – everything is evolving so fast.
LLMの募集はまだ始まったばかりですが、すべてが急速に進化しています。
I recently read a book proposal on LLMs, and my first thought was: most of this will be outdated in a month.
最近、LLMに関する本の企画書を読んだのですが、最初に思ったのは、「この内容のほとんどは、1ヶ月後には時代遅れになってしまう」ということでした。
APIs are changing day to day.
APIは日々変化しています。
New applications are being discovered.
新しい用途が発見されています。
Infrastructure is being aggressively optimized.
インフラは積極的に最適化されています。
Cost and latency analysis needs to be done on a weekly basis.
コストやレイテンシーの解析は週単位で行う必要がある。
New terminologies are being introduced.
新しい用語が登場しています。

Not all of these changes will matter.
これらの変化のすべてが問題になるわけではありません。
For example, many prompt engineering papers remind me of the early days of deep learning when there were thousands of papers describing different ways to initialize weights.
例えば、多くのプロンプトエンジニアリング論文は、重みを初期化するさまざまな方法を記述した何千もの論文があったディープラーニングの初期を思い出させます。
I imagine that tricks to tweak your prompts like: "Answer truthfully", "I want you to act like …", writing "question: " instead of "q:" wouldn’t matter in the long run.
というように、プロンプトに手を加えるトリックを想像しています： "正直に答えてください"、"私はあなたが...のように行動してほしい"、"質問を書く： のように振る舞ってほしい」、「Q:」の代わりに「Question:」と書くなど、プロンプトに手を加えることは、長い目で見れば重要ではないでしょう。

Given that LLMs seem to be pretty good at writing prompts for themselves – see Large Language Models Are Human-Level Prompt Engineers (Zhou et al., 2022) – who knows that we’ll need humans to tune prompts?
LLMは自分自身のためにプロンプトを書くのが得意なようで、「Large Language Models Are Human-Level Prompt Engineers (Zhou et al., 2022)」を参照してください。プロンプトを調整するために人間が必要になるとは誰が知るでしょうか。

However, given so much happening, it’s hard to know which will matter, and which won’t.
しかし、多くのことが起きているため、どれが重要で、どれが重要でないかを知ることは難しい。

I recently asked on LinkedIn how people keep up to date with the field.
先日、LinkedInで「みんなどうやって現場を把握しているのか？
The strategy ranges from ignoring the hype to trying out all the tools.
その戦略は、誇大広告を無視するものから、すべてのツールを試してみるものまで様々です。

## Ignore (most of) the hype 誇大広告を（ほとんど）無視する

Vicki Boykis (Senior ML engineer @ Duo Security): I do the same thing as with any new frameworks in engineering or the data landscape: I skim the daily news, ignore most of it, and wait six months to see what sticks.
Vicki Boykis (Senior ML engineer @ Duo Security)： 私は、エンジニアリングやデータ環境における新しいフレームワークと同じことをしています：日々のニュースに目を通し、そのほとんどを無視し、何が定着するか6ヶ月待ちます。
Anything important will still be around, and there will be more survey papers and vetted implementations that help contextualize what’s happening.
重要なものはまだ残っていますし、何が起こっているのか文脈を理解するのに役立つ調査論文や検証された実装も増えていくでしょう。

## Read only the summaries サマリーだけを読む

Shashank Chaurasia (Engineering @ Microsoft): I use the Creative mode of BingChat to give me a quick summary of new articles, blogs and research papers related to Gen AI! I often chat with the research papers and github repos to understand the details.
Shashank Chaurasia（エンジニアリング@マイクロソフト）です： BingChatのCreativeモードを使って、Gen AIに関連する新しい記事、ブログ、研究論文を簡単にまとめています！研究論文やgithub reposでチャットして詳細を理解することが多いです。

## Try to keep up to date with the latest tools 最新ツールの導入に努めよう

Chris Alexiuk (Founding ML engineer @ Ox): I just try and build with each of the tools as they come out - that way, when the next step comes out, I’m only looking at the delta.
クリス・アレクシーク（創業者MLエンジニア@Ox）： そうすれば、次のステップが出てきたときに、その差分だけを見ることができるのです。

What’s your strategy?
あなたの戦略は？