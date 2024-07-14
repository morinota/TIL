## refs 審判

https://www.activeloop.ai/resources/use-llama-index-to-build-an-ai-shopping-assistant-with-rag-and-agents/
https://www.activeloop.ai/resources/use-llama-index-to-build-an-ai-shopping-assistant-with-rag-and-agents/

# Use LlamaIndex to Build an AI Shopping Assistant with RAG and Agents LlamaIndexを使ってRAGとエージェントによるAIショッピング・アシスタントを構築する

Build an AI Shopping Assistant to Personalize and Maximize Online E-commerce Sales with GPT-4V, LlamaIndex, and Deep Lake.
GPT-4V、LlamaIndex、Deep Lakeを使用して、オンラインEコマースの売上をパーソナライズして最大化するAIショッピングアシスタントを構築。
Budget, Weather & Look Optimization.
予算、天候、ルックの最適化。

In the ever-expanding landscape of artificial intelligence, vector databases stand as the unsung heroes, forming the foundation upon which many AI applications are built.
拡大し続ける人工知能の世界において、ベクターデータベースは縁の下の力持ちとして、多くのAIアプリケーションの土台を形成している。
These powerful databases provide the capacity to store and retrieve complex, high-dimensional data, enabling functionalities like Retrieval Augmented Generation (RAG) and sophisticated recommendation systems, covered in depth in our Advanced Retrieval Augmented Generation course, which this article is a part of.
これらの強力なデータベースは、複雑な高次元データの保存と検索を可能にし、検索拡張生成（RAG）や高度な推薦システムのような機能を実現する。

Alongside vector databases, Large Language Model (LLM) frameworks such as LlamaIndex and LangChain have emerged as key players in accelerating AI development.
ベクトルデータベースと並んで、LlamaIndexやLangChainといった大規模言語モデル（LLM）フレームワークが、AI開発を加速させる重要なプレーヤーとして登場している。
By simplifying the prototyping process and reducing development overheads associated with API interactions and data formatting, these frameworks allow creators to focus on innovation rather than the intricacies of implementation.
プロトタイピング・プロセスを簡素化し、APIインタラクションやデータ・フォーマットに関連する開発オーバーヘッドを削減することで、これらのフレームワークはクリエイターが複雑な実装よりもイノベーションに集中することを可能にする。

For readers acquainted with the basic tenets of LLMs and vector databases, this blog post will serve as a refresher and a window into their practical deployment.
LLMとベクター・データベースの基本的な考え方を知っている読者にとって、このブログ記事は復習の役割を果たすとともに、その実用的な展開についての窓口になるだろう。
We aim to walk you through constructing a complex and interactive shopping assistant.
私たちは、複雑でインタラクティブなショッピング・アシスタントを構築することを目指します。
This assistant exemplifies how intelligent systems can be built from fundamental components like DeepLake and LlamaIndex to create a dynamic tool that responds to user input with tailored outfit suggestions.
このアシスタントは、DeepLakeやLlamaIndexのような基本的なコンポーネントからインテリジェントなシステムを構築し、ユーザーの入力に応えてオーダーメイドの服を提案するダイナミックなツールを作成できることを例証している。

Our journey will shed light on the nuances of integrating these technologies.
私たちの旅は、これらのテクノロジーを統合するニュアンスに光を当てるだろう。
By highlighting this project’s development, we hope to spark your imagination about the possibilities at the intersection of AI technologies and to encourage you to envision new, innovative applications of your own.
このプロジェクトの開発に焦点を当てることで、AI技術の交差点における可能性について想像力をかき立て、あなた自身の新しい革新的なアプリケーションを思い描くことを奨励したい。

## Project Overview プロジェクト概要

Our project is an AI-powered shopping assistant (follow the GitHub repo here) designed to leverage image processing and LLM agents for outfit recommendations.
私たちのプロジェクトは、画像処理とLLMエージェントを服の推薦に活用するように設計された、AIを搭載したショッピングアシスタント（GitHubのレポはこちら）です。
Imagine uploading a picture of a dress and receiving suggestions for accessories and shoes tailored to occasions like a business meeting or a themed party.
ドレスの写真をアップロードすると、商談やテーマを決めたパーティーなどのシーンに合わせたアクセサリーや靴の提案を受けることを想像してみてほしい。
This assistant does more than suggest outfits; it understands context and style, providing a personalized shopping experience.
このアシスタントは服装を提案するだけでなく、文脈やスタイルを理解し、パーソナライズされたショッピング体験を提供する。

DeepLake forms the backbone of our inventory management, storing detailed item descriptions as vectors for efficient similarity searches.
DeepLakeは、当社の在庫管理のバックボーンを形成し、効率的な類似検索のためのベクトルとして詳細な商品説明を保存します。
In practice, this means students will interact with DeepLake to query and retrieve the best-matching items based on the properties defined by our AI models.
実際には、学生がDeepLakeと対話し、AIモデルによって定義されたプロパティに基づいて、ベストマッチするアイテムを照会して取得することを意味します。

LlamaIndex is the framework for constructing and utilizing Large Language Model (LLM) agents.
LlamaIndexは、大規模言語モデル（LLM）エージェントを構築し、利用するためのフレームワークです。
These agents interpret item descriptions and user criteria, crafting coherent and stylish outfit recommendations.
これらのエージェントは、アイテムの説明とユーザーの条件を解釈し、首尾一貫したスタイリッシュな服を推薦する。
Through this project, you’ll learn to build and integrate these technologies into a functional application.
このプロジェクトを通して、これらの技術を構築し、機能的なアプリケーションに統合することを学びます。

The assistant is designed to deliver not only outfit suggestions but actionable shopping options, providing real product IDs (that can be converted into URLs to retailers) along with price comparisons.
このアシスタントは、服の提案だけでなく、実際の商品ID（小売店へのURLに変換可能）と価格比較を提供し、実行可能なショッピングオプションを提供するように設計されている。
Throughout the course, you will learn how to extend the AI’s capabilities to facilitate an end-to-end shopping experience.
コースを通して、AIの機能を拡張してエンド・ツー・エンドのショッピング体験を促進する方法を学びます。

The user interface of this application is designed with functionality and educational value in mind.
このアプリケーションのユーザー・インターフェースは、機能性と教育的価値を念頭に置いて設計されています。
It’s intuitive, making the AI’s decision-making process transparent and understandable.
直感的で、AIの意思決定プロセスを透明化し、理解しやすくしている。
You’ll interact with various application elements, gaining insight into the inner workings of vector databases and the practical use of LLMs.
様々なアプリケーションの要素に触れ、ベクター・データベースの内部構造やLLMの実用的な使用法についての見識を深めます。

## Architecture design 建築デザイン

Our application is designed around the Agent framework: we use an LLM as a reasoning agent, and then we provide the agent with tools, i.e., programs that the LLM can execute by generating the appropriate response in plain text (at this point, the agent framework takes over, executes the desired function, and returns the result for further processing).
我々のアプリケーションはエージェントフレームワークを中心に設計されている： LLMを推論エージェントとして使用し、LLMが適切な応答をプレーンテキストで生成することによって実行できるプログラム、すなわちツールをエージェントに提供する（この時点で、エージェントフレームワークが引き継ぎ、目的の関数を実行し、さらなる処理のために結果を返す）。
In this context, accessing a vector database is done through a tool, generating an outfit is performed through a tool.
この文脈では、ベクターデータベースへのアクセスはツールを通じて行われ、アウトフィットの生成はツールを通じて行われる。
Even getting the today’s date is performed through a tool.
今日の日付の取得もツールで行う。

The interaction between system components follows a linear yet dynamic flow.
システム・コンポーネント間の相互作用は、直線的でありながら動的な流れに従う。
Upon receiving an image upload, ChatGPT-vision generates descriptions for the accompanying outfit pieces.
画像のアップロードを受け取ると、ChatGPT-visionはそれに付随する衣装の説明文を生成します。
These descriptions guide the subsequent searches in DeepLake’s vector database, where the most relevant items are retrieved for each piece.
これらの説明は、DeepLakeのベクター・データベースでのその後の検索の指針となり、各作品に最も関連性の高いアイテムが検索されます。
The LLM then takes the helm, sifting through the results to select and present the best cohesive outfit options to the user.
そして、LLMが舵を取り、結果をふるいにかけて、最もまとまりのある衣装の選択肢を選び、ユーザーに提示する。

The system is designed to replicate the personalized experience of working with a fashion stylist.
このシステムは、ファッション・スタイリストと仕事をするときのパーソナライズされた体験を再現するように設計されている。
When a user uploads a garment image, our AI stylist gets to work.
ユーザーが衣服の画像をアップロードすると、AIスタイリストが作業を開始します。
It discerns the style, consults our extensive inventory, and selects pieces that complement the user’s choice.
スタイルを見極め、当社の豊富な在庫を参照し、ユーザーの選択を補完する作品を選択します。
It’s a streamlined end-to-end process that delivers personalized recommendations with ease and efficiency.
これは、簡単かつ効率的にパーソナライズされた推奨を提供する合理化されたエンド・ツー・エンドのプロセスである。

## Dataset Collection and Vector Database Population データセットコレクションとベクターデータベース人口

Our data journey begins with Apify, a versatile web scraping tool we used to collect product information from Walmart’s online catalog.
私たちのデータの旅は、ウォルマートのオンラインカタログから商品情報を収集するために使用した汎用性の高いウェブスクレイピングツール、Apifyから始まります。
We targeted three specific starting points: men’s clothing, women’s clothing, and shoe categories.
私たちは3つの具体的な出発点に的を絞った： 紳士服、婦人服、靴のカテゴリーである。
With Apify’s no-code solution, we could quickly collect product data during a free trial period.
アピファイ社のコード不要のソリューションにより、無料試用期間中に製品データを迅速に収集することができました。
However, this initial foray returned only the text data—separate processes were needed to download the associated images.
しかし、この最初の試みでは、テキストデータのみが返され、関連する画像をダウンロードするには別のプロセスが必要だった。

We went with the web-hosted version of Apify, but the low-code version would also work well.
私たちはアピファイのウェブホスト版を使いましたが、ローコード版でもうまくいくでしょう。

We aimed to construct a representative dataset of men’s and women’s clothing, including various tops, bottoms, and accessories.
我々は、様々なトップス、ボトムス、アクセサリーを含む、メンズとレディースの代表的な衣服のデータセットを構築することを目指した。
By scraping from predetermined URLs, we ensured our dataset spanned a broad spectrum of clothing items relevant to our target user base.
あらかじめ決められたURLからスクレイピングすることで、ターゲットとするユーザー層に関連する衣料品を幅広く網羅したデータセットを確保した。

The collected data is fairly rich and contains a wide variety of attributes.
収集されたデータはかなり豊富で、さまざまな属性を含んでいる。
For the purpose of this project, we kept the attributes used to a minimum.
このプロジェクトの目的のため、使用する属性は最小限にとどめた。
We selected the product ID, category, price, name, and image.
商品ID、カテゴリー、価格、名前、画像を選択した。
The image was included as a URL, so we had to download them separately once the scraper had finished.
画像はURLとして含まれていたため、スクレイパーが終了したら別途ダウンロードする必要があった。
Overall, we collected 1344 items.
全部で1344アイテムを集めた。

We used pandas to read the scraped JSONs and clean the collected data.
スクレイピングされたJSONを読み込み、収集したデータをクリーニングするためにpandasを使用した。
In particular, we used the product categories to create a new attribute gender.
特に、商品カテゴリーを使用して、新しい属性「性別」を作成した。

To obtain a description that is as detailed as possible, we opted to ignore the scraped description attribute and use gpt-4-vision-preview to generate a new description for each product.
可能な限り詳細な説明を得るため、スクレイピングされた説明属性を無視し、gpt-4-vision-preview を使用して各商品の新しい説明を生成することにした。
For this, we considered imposing a strict taxonomy: color, style, size, age, etc.
そのために、厳密な分類法を課すことを考えた： 色、スタイル、サイズ、年齢などである。
Ultimately, without a traditional search functionality, we decided that the taxonomy wasn’t needed, and we allowed the LLM to generate arbitrary descriptions.
最終的に、従来の検索機能がなければ、分類法は必要ないと判断し、LLMが任意の記述を生成できるようにした。

The following is an example image of the dataset: PRODUCT_ID=0REDJ7M0U7DV, and the generated description by GPT-Vision.
以下は、データセットのイメージ例です： PRODUCT_ID=0REDJ7M0U7DVと、GPT-Visionによって生成された説明です。

Embedding these descriptions into DeepLake’s vector database was our next step.
これらの説明をDeepLakeのベクトル・データベースに埋め込むことが次のステップだった。
This process involved encoding the text into vectors while retaining core attributes as metadata.
このプロセスでは、コア属性をメタデータとして保持しながら、テキストをベクトルにエンコードした。

Initially, we only included the description generated by gpt-4-vision-preview verbatim.
当初は、gpt-4-vision-previewで生成された説明文のみをそのまま掲載していた。
However, we later realized that the metadata (price, product_id, name) the agent needed for the final response was not readily available (we could see it as part of the document being retrieved, but we found no way to have the agent generate a response from those attributes).
しかし、エージェントが最終的なレスポンスに必要とするメタデータ（価格、product_id、name）は、すぐに利用できないことに後で気づきました（取得されたドキュメントの一部として見ることはできましたが、エージェントがそれらの属性からレスポンスを生成する方法は見つかりませんでした）。

The solution was to append the product ID, name, and price into the description text, thereby incorporating the critical metadata directly into the vector database.
解決策は、商品ID、商品名、価格を説明文に追加することで、重要なメタデータをベクターデータベースに直接組み込むことだった。

Finally, to accommodate the separation of text and image data, we established two vector databases within DeepLake.
最後に、テキストデータと画像データの分離に対応するため、DeepLake 内に 2 つのベクトルデータベースを構築しました。
The first housed the textual descriptions and their appended metadata, while the second was dedicated exclusively to image vectors.
1つ目はテキスト記述とそれに付加されたメタデータを格納し、2つ目は画像ベクトル専用である。

## Development of core tools コアツールの開発

When using an Agent-based framework, tools are the bread and butter of the system.
エージェントベースのフレームワークを使用する場合、ツールはシステムの糧となる。

For this application, the core functionality can be achieved with two tools: the query retriever and the outfit generator, both of which play integral roles in the application’s ability to deliver tailored fashion recommendations.
このアプリケーションでは、核となる機能は2つのツールで実現できる： クエリーリトリーバーとアウトフィットジェネレーターである。

# Inventory query engine インベントリークエリーエンジン

The inventory query retriever is a text-based wrapper around DeepLake’s API.
インベントリ・クエリ・リトリーバは、DeepLake の API のテキストベースのラッパーです。
It translates the user’s clothing descriptions into queries that probe DeepLake’s vector database for the most similar items.
ユーザーの服の説明をクエリーに変換し、DeepLakeのベクトルデータベースから最も類似したアイテムを探し出す。
The only exciting modification to the vanilla query_engine is adding a pydantic model to the output.
バニラのquery_engineに対する唯一のエキサイティングな変更は、出力にpydanticモデルを追加することである。
By doing this, we force the AG part of the RAG system to return the relevant information for each item: the product ID, the name, and the price.
こうすることで、RAGシステムのAGパートに、各アイテムの関連情報を返すよう強制する： 商品ID、商品名、価格。

Notice the description on each BaseModel? Those are mandatory when using pydantic with the query engine.
各 BaseModel の説明にお気づきでしょうか？これらは pydantic をクエリーエンジンで使用する際に必須となるものです。
We learned this the hard way after finding several strange “missing description errors.”
私たちは、奇妙な "missing description errors "をいくつも見つけてから、このことを苦労して学んだ。

Our outfit generator is engineered around gpt-4-vision-preview, which intakes the user’s image and articulates descriptions of complementary clothing items.
このジェネレーターは、gpt-4-vision-previewを中心に設計されており、ユーザーの画像を取り込み、それを補完する服の説明を表現します。
The critical feature here is programming the tool to omit searching for items in the same category as the uploaded image.
ここで重要なのは、アップロードした画像と同じカテゴリーにあるアイテムの検索を省略するようにツールをプログラミングすることである。
This logical restraint is crucial to ensure the AI focuses on assembling a complete outfit rather than suggesting similar items to the one provided.
この論理的な抑制は、AIが提供されたものと似たようなアイテムを提案するのではなく、完全な服を組み立てることに集中するようにするために重要である。

When working with agents, debugging and fixing errors is particularly difficult because of their dynamic nature.
エージェントを扱う場合、その動的な性質のため、エラーのデバッグと修正は特に難しい。
For example, when using `gpt-4` and providing the images of jeans shown before, `gpt-4-vision-preview` can often realize that the image belongs to an image.
例えば、`gpt-4`を使い、前に示したジーンズの画像を提供すると、`gpt-4-vision-preview`はその画像が画像に属していることを認識できることが多い。
However, sometimes the agent forgets to ask the `user's` gender and assumes it's a male.
しかし、エージェントがユーザーの性別を聞くのを忘れて、男性だと思い込んでしまうこともある。
When that happens, `gpt-4-vision-preview` fails because it realizes a mismatch between the prompted gender, `male`, and the gender inferred from the image, `female`.
このような場合、`gpt-4-vision-preview`は、プロンプトされた性別である `male`と、画像から推測される性別である `female`との間にミスマッチがあることに気づき、失敗する。
Here we can see some of the biases of large language models at play and how they can suddenly break an application
ここでは、大規模な言語モデルのバイアスがどのように作用し、それがどのように突然アプリケーションを壊すかを見ることができる。

Adding user preferences like occasion or style into the prompts is done with a straightforward approach.
オケージョンやスタイルといったユーザーの好みをプロンプトに加えることは、簡単なアプローチでできる。
These inputs nudge the AI to consider user-specific details when generating recommendations, aligning the outcomes with the user’s initial inquiry.
これらの入力は、推薦文を生成する際にユーザー固有の詳細を考慮するようAIを後押しし、ユーザーの最初の問い合わせと結果を一致させる。

The system functionality unfolds with the LLM agent at the helm.
システムの機能は、LLMエージェントが舵を取ることで展開される。
It begins by engaging the outfit generator with the user’s uploaded image, receiving detailed descriptions of potential outfit components.
まず、ユーザーがアップロードした画像と衣装ジェネレーターが連動し、衣装の構成要素の詳細な説明を受け取る。
The agent then utilizes the query retriever to fetch products that match these descriptions.
その後、エージェントはクエリーリトリーバーを利用して、これらの説明に一致する商品をフェッチする。

## System integration and initial testing システム統合と初期テスト

The successful integration of various AI components into a seamless shopping assistant experience required a straightforward approach: encapsulating each function into a tool and crafting an agent to orchestrate these tools.
さまざまなAIコンポーネントをシームレスなショッピングアシスタント体験にうまく統合するには、わかりやすいアプローチが必要だった： 各機能をツールにカプセル化し、これらのツールをオーケストレーションするエージェントを作ることだ。

# LlamaIndex Agent creation and integration process LlamaIndex エージェントの作成と統合プロセス

Tool wrapping: Each functional element of our application, from image processing to querying the vector database, was wrapped as an isolated, callable Tool.
ツールのラッピング： 画像処理からベクターデータベースのクエリまで、アプリケーションの各機能要素は、分離された呼び出し可能なToolとしてラッピングされました。

Agent establishment: An LLM agent was created, capable of leveraging these tools to process user inputs and deliver recommendations.
エージェントの設立： LLMエージェントが作成され、これらのツールを活用してユーザーの入力を処理し、推奨を提供することができる。

# Initial testing challenges 初期テストの課題

Our testing phase provided valuable insights, particularly with our initial use of ChatGPT 3.5.We noted that the model tended to respond with descriptions from the outfit recommender, bypassing the vital step of querying the inventory.
私たちのテスト段階では、特にChatGPT 3.5を最初に使用することで、貴重な洞察を得ることができました。私たちは、モデルがインベントリを照会する重要なステップをバイパスして、服のレコメンダーからの説明で応答する傾向があることを指摘しました。
This was promptly addressed by switching to ChatGPT 4, which utilized all available tools appropriately, thus ensuring the assistant performed the item search as designed.
これは、利用可能なすべてのツールを適切に利用するChatGPT 4に切り替えることで、アシスタントのアイテム検索が設計通りに行われるようにすることで、速やかに対処した。

💡 Using `gpt-3.5-turbo` resulted in the agent not using all the tools.
💡 `gpt-3.5-turbo` を使用した場合、エージェントがすべてのツールを使用しませんでした。
To achieve the expected results, we had to use `gpt-4`.
期待通りの結果を得るためには、`gpt-4`を使わなければならなかった。

# Demo: Step-by-step commands and interactions デモ ステップバイステップのコマンドとインタラクション

Below is a demonstration of the system in action, detailing the commands issued to the agent and their corresponding answers at each stage of the process:
以下は、エージェントに対して発行されたコマンドと、プロセスの各段階における対応する回答を詳細に示した、システムの動作デモである：

Image upload and description generation
画像のアップロードと説明文の生成

Currently, the process of uploading the image is separate.
現在、画像をアップロードするプロセスは別になっている。
For this version to work, an image needs to exist in the local folder .image_input/.
このバージョンで動作させるには、ローカルフォルダー .image_input/ に画像が存在する必要があります。
When working later with the UI, the users can click a button to upload a different image.
後でUIで作業するとき、ユーザーはボタンをクリックして別の画像をアップロードできる。

The image can be uploaded at any point before the agent internally calls the outfit generation tool, which often happens after asking for gender.
画像は、エージェントが内部的に衣装生成ツールを呼び出す前のどの時点でもアップロードすることができる。

### Outfit generation 衣装世代

In this section, we can see how the agent internally uses the tool to generate an outfit from the user description, image, and gender.
このセクションでは、エージェントが内部的にどのようにツールを使って、ユーザーの説明、画像、性別から服を生成するかを見ることができる。

### Querying the inventory インベントリーの照会

At this stage, the agent obtains a description for the two pieces of clothing that it needs to retrieve and uses the query engine to retrieve the best matches from the vector database.
この段階で、エージェントは、検索する必要がある2つの衣服の説明を取得し、ベクトルデータベースから最適な一致を検索するためにクエリーエンジンを使用します。

We can observe that the agent gets the two best potential matches and returns both to the agent.
エージェントは2つのベストマッチ候補を獲得し、その両方をエージェントに返すことがわかる。

### Final recommendation presentation 最終推薦プレゼンテーション

After analyzing the options, the agent presents the user with the best matching pairs, complete with item details such as price and purchase links (the product ID could be converted to a URL later).
選択肢を分析した後、エージェントは、価格や購入リンクのような商品の詳細（商品IDは後でURLに変換することができる）とともに、最もマッチするペアをユーザーに提示する。
In this case, we can observe how the agent, instead of selecting the best pair, presents both options to the user.
この場合、エージェントは最適なペアを選択する代わりに、ユーザーに両方の選択肢を提示する。

💡 Remember that our dataset is fairly small, and the option suggested by the outfit recommender might not be available in our dataset.
💡 我々のデータセットはかなり小さいので、衣装レコメンダーが提案するオプションは我々のデータセットでは利用できないかもしれないことを忘れないでください。
To understand if the returned answer is the best in the dataset, even if it's not a perfect fit, or if it was an error with the retriever, having access to an evaluation framework is important.
返された答えがデータセットの中で最良かどうか、完璧にフィットしていないとしても、あるいはレトリーバーのエラーであったとしても、それを理解するためには、評価フレームワークにアクセスすることが重要である。

Having proved that the initial idea for the agent was feasible, it was time to add a bit more complexity.
エージェントの最初のアイデアが実現可能であることが証明されたので、もう少し複雑さを加えることにした。
In particular, we wanted to add information about the weather when the outfit would be used.
特に、衣装が使用される日の天候に関する情報を追加したかった。

## Expanding functionality 機能拡張

The natural progression of our shopping assistant entails augmenting its capacity to factor in external elements such as weather conditions.
ショッピング・アシスタントの自然な進歩は、天候などの外的要素を考慮する能力を増強することである。
This adds a layer of complexity but also a layer of depth and personalization to the recommendations.
これは、複雑なレイヤーを追加しますが、レコメンデーションに深みとパーソナライゼーションのレイヤーも追加します。
These enhancements came with their own sets of technical challenges.
これらの強化には、それぞれ技術的な課題があった。

# Adapting to the weather 天候への適応

Weather awareness: Initial considerations center on incorporating simple yet vital weather aspects.
天候の認識： 最初に考慮すべきは、シンプルだが重要な天候の側面を取り入れることだ。
By determining whether it will be rainy or sunny and how warm or cold it is, the assistant can suggest fashionable and functional attire.
雨か晴れか、暖かさか寒さかを判断することで、アシスタントはファッショナブルで機能的な服装を提案することができる。

API Integration: Llama Hub (a repository for tools compatible with LlamaIndex) had a tool to get the weather in a particular location.
APIの統合： Llama Hub（LlamaIndexと互換性のあるツールのリポジトリ）には、特定の場所の天気を取得するツールがあった。
Unfortunately, the tool required a paid https://openweathermap.org/ plan.
残念ながら、このツールは有料のhttps://openweathermap.org/ プランが必要だった。
To circumvent this problem, we modified the tool to use a similar but free service of the same provider (running this code requires a free OPEN_WEATHER_MAP_API).
この問題を回避するために、我々は同じプロバイダーの類似しているが無料のサービスを使用するようにツールを修正した（このコードを実行するには無料のOPEN_WEATHER_MAP_APIが必要）。

# User interaction and data handling ユーザーとの対話とデータ処理

Location input: For accurate weather data, the shopping assistant often queries the user for their location.
位置情報の入力： 正確な気象データを得るために、ショッピングアシスタントはしばしばユーザーの位置情報を照会する。
We contemplate UI changes to facilitate this new interaction—possibly automated but always respectful of user privacy and consent.
私たちは、この新しいインタラクションを促進するためにUIの変更を考えています。

# Synchronizing with time ♪時間と同期する

Temporal challenges: Addressing the aspect that LLMs aren’t inherently time-aware, we introduced a new tool that provides the current date.
時間的な課題 LLMは本質的に時間を認識しないという側面に対処するため、現在の日付を提供する新しいツールを導入した。
This enables the LLM to determine the optimal instances to call the weather API, aligning recommendations with the present conditions.
これによってLLMは、天候APIを呼び出す最適なインスタンスを決定し、推奨を現在の状況に合わせることができる。

It took us a little bit to remember that we needed this.
これが必要だと思い出すのに少し時間がかかった。
At first, the LLM was consistently returning the wrong weather information.
当初、LLMは常に間違った気象情報を返していた。
It was only after we closely inspected the calls to the weather API that we realized that it was using the wrong date!
お天気APIのコールをよく調べて初めて、間違った日付を使っていることに気づいた！

## User Interface (UI) development ユーザーインターフェース（UI）開発

In developing the user interface for our AI-powered shopping assistant, we wanted the platform to reflect the conversational nature of the agent’s interactions.
AIを搭載したショッピング・アシスタントのユーザー・インターフェースを開発するにあたり、私たちは、エージェントとの対話の会話的な性質を反映したプラットフォームにしたいと考えました。
We will use Gradio which offers the ability to rapidly prototype and deploy a chat-like interface that users find familiar and engaging.
私たちは、ユーザーが親しみやすく魅力的だと感じるチャットのようなインターフェイスを迅速にプロトタイプ化して展開できるGradioを使用します。

# Embracing chat interface with Gradio Gradioでチャットインターフェースを採用

Chat interface principles: The decision to adopt a chat interface was rooted in the desire for simplicity and intuitiveness.
チャット・インターフェイスの原則 チャット・インターフェースを採用する決定は、シンプルさと直感性を求めることに根ざしていた。
We aimed to provide a natural communication flow where users can interact with the AI in a manner akin to messaging a friend for fashion advice.
私たちが目指したのは、ファッションのアドバイスを求める友人にメッセージを送るような感覚で、ユーザーがAIと対話できる自然なコミュニケーションの流れを提供することです。
Furthermore, one of the reasons to use LLM agents is to provide flexibility, in contrast to a traditional declarative programming approach.
さらに、LLMエージェントを使用する理由の1つは、従来の宣言的プログラミングアプローチとは対照的に、柔軟性を提供することである。
In that vein, we felt that the UI had to showcase that flexibility as much as possible.
その意味で、UIはその柔軟性をできるだけアピールするものでなければならないと考えた。

Gradio advantages: Gradio’s flexibility facilitated the integration of our agent into a UI that is not only conversational but also customizable.
Gradioの利点： Gradioの柔軟性により、会話だけでなくカスタマイズも可能なUIにエージェントを統合することができました。
Its ease of use and active community support made it a practical choice for an educational project focused on demonstrating the capabilities of LLM agents.
その使いやすさと活発なコミュニティ・サポートは、LLMエージェントの能力を実証することに焦点を当てた教育プロジェクトにとって、実用的な選択となった。
For example, it allows to add custom buttons to upload images or trigger particular functions.
例えば、画像をアップロードしたり、特定の機能をトリガーするためのカスタムボタンを追加することができる。

# Overcoming technical hurdles 技術的なハードルを乗り越える

Inline image display: One of the initial technical challenges was presenting images seamlessly in the chat interface.
インライン画像表示： 初期の技術的な課題の一つは、チャットインターフェイスで画像をシームレスに表示することでした。
Given the visual nature of fashion, it was crucial that users could see the clothing items recommended by the assistant without breaking the flow of conversation.
ファッションは視覚的なものであるため、ユーザーが会話の流れを断ち切ることなく、アシスタントが勧める服を見ることができることが重要だった。

Activeloop integration: To resolve this, we leveraged Activeloop’s integration with Gradio.
Activeloopとの統合： これを解決するために、ActiveloopとGradioの統合を活用しました。
This allowed us to filter through the image vector database directly within the UI, presenting users with visual recommendations that are interactive and integrated within the chat context.
これにより、UI内で画像ベクターデータベースを直接フィルタリングすることができ、チャットコンテキストの中でインタラクティブに統合されたビジュアルレコメンデーションをユーザーに提示することができました。

It was not trivial to get Activeloop’s extension working for our project.
Activeloopのエクステンションを我々のプロジェクトで機能させるのは簡単なことではなかった。
Our solution consisted of having an HTML component in Gradio with an IFrame pointed to the image vector dataset.
私たちの解決策は、GradioのHTMLコンポーネントに、画像ベクトルデータセットを指すIFrameを持たせることでした。
We could update the URL every time the chatbot answered, but we needed a way to get the product IDS from its answer.
チャットボットが回答するたびにURLを更新することはできたが、その回答から製品IDSを取得する方法が必要だった。
Ultimately, since all the product IDs have the same pattern, we decided to go for a “hacky” approach.
結局、すべてのプロダクトIDが同じパターンを持っているため、「ハチャメチャ」なアプローチを取ることにした。
Search the agent’s response for the product IDs regex, and if there were more than 2 matches, update the iframe URL parameters.
エージェントのレスポンスをプロダクトIDsの正規表現で検索し、2つ以上マッチした場合、iframe URLパラメータを更新します。
Otherwise, do nothing.
そうでなければ何もしない。

## Conclusion 結論

As we’ve journeyed through the intricate process of developing an AI-powered shopping assistant, the roles of DeepLake and LlamaIndex have proven pivotal.
AIを搭載したショッピング・アシスタントを開発する複雑なプロセスを旅する中で、DeepLakeとLlamaIndexの役割が極めて重要であることが証明された。
From the versatile data handling in DeepLake’s database for AI to the adaptive LLM agents orchestrated by LlamaIndex, these technologies have showcased their robust capabilities and the potential for innovation in the AI space.
DeepLakeのAI用データベースにおける多彩なデータ処理から、LlamaIndexによって編成された適応型LLMエージェントに至るまで、これらのテクノロジーは、その強固な能力とAI分野におけるイノベーションの可能性を示してきた。

DeepLake has demonstrated its capacity to seamlessly manage and retrieve complex structures, enabling efficient and precise item matchings.
DeepLakeは、複雑な構造をシームレスに管理・検索し、効率的で正確なアイテムのマッチングを可能にする能力を実証しています。
Its architecture has been the backbone of the shopping assistant, proving that even complex data interactions can be handled with elegance and speed.
そのアーキテクチャーはショッピング・アシスタントのバックボーンであり、複雑なデータのやり取りもエレガントかつ迅速に処理できることを証明している。
In addition, it allowed for seamless visualization the data for the RAG application.
加えて、RAGアプリケーション用にデータをシームレスに可視化することができた。

LlamaIndex, on the other hand, has been instrumental in empowering the shopping assistant with natural language processing and decision-making abilities.
一方、ラマインデックスは、ショッピング・アシスタントに自然言語処理と意思決定能力を与えることに貢献してきた。
Its framework has enabled the LLM agents to interpret, engage, and personalize the shopping experience, charting new courses in user-AI interaction.
そのフレームワークは、LLMエージェントがショッピング体験を解釈し、関与し、パーソナライズすることを可能にし、ユーザーとAIとのインタラクションにおける新たな道を切り開いた。

Looking beyond the shopping assistant itself, the potential uses for these technologies span myriad domains.
ショッピング・アシスタントそのものにとどまらず、これらの技術の潜在的な用途は無数の領域に及ぶ。
The flexibility and power of DeepLake and LlamaIndex could drive innovation in fields ranging from healthcare to finance and from educational tools to creative industries.
DeepLakeとLlamaIndexの柔軟性とパワーは、ヘルスケアから金融、教育ツールからクリエイティブ産業まで、幅広い分野でイノベーションを推進する可能性がある。

Your insights and feedback are crucial as we continue to navigate and expand the frontiers of artificial intelligence.
私たちが人工知能のフロンティアをナビゲートし、拡大し続けるためには、皆さんの洞察力とフィードバックが不可欠です。
We are particularly eager to hear your views on the innovative applications of vector databases and LLM frameworks.
特に、ベクター・データベースとLLMフレームワークの革新的な応用についてのご意見をお聞かせください。
Additionally, your suggestions for topics you’d like us to delve into in future segments are highly appreciated.
さらに、今後のセグメントで掘り下げてほしいトピックのご提案も大歓迎です。
If you’re interested in partnering with Tryolabs to build similar projects with Deep Lake & LlamaIndex, feel free to reach out to us.
Tryolabsと提携し、Deep LakeとLlamaIndexで同様のプロジェクトを構築することに興味がある方は、お気軽にご連絡ください。