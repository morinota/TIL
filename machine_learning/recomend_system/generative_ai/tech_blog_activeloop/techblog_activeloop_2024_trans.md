## refs 審判

https://www.activeloop.ai/resources/use-llama-index-to-build-an-ai-shopping-assistant-with-rag-and-agents/
https://www.activeloop.ai/resources/use-llama-index-to-build-an-ai-shopping-assistant-with-rag-and-agents/

# Use LlamaIndex to Build an AI Shopping Assistant with RAG and Agents LlamaIndexを使ってRAGとエージェントによるAIショッピング・アシスタントを構築する

Build an AI Shopping Assistant to Personalize and Maximize Online E-commerce Sales with GPT-4V, LlamaIndex, and Deep Lake.
GPT-4V、LlamaIndex、Deep Lakeを使用して、オンラインEコマースの売上をパーソナライズして最大化するAIショッピングアシスタントを構築。
Budget, Weather & Look Optimization.
予算、天候、ルックの最適化。

In the ever-expanding landscape of artificial intelligence, vector databases stand as the unsung heroes, forming the foundation upon which many AI applications are built.
拡大し続ける人工知能の世界において、**ベクターデータベースは縁の下の力持ちとして、多くのAIアプリケーションの土台を形成している**。
These powerful databases provide the capacity to store and retrieve complex, high-dimensional data, enabling functionalities like Retrieval Augmented Generation (RAG) and sophisticated recommendation systems, covered in depth in our Advanced Retrieval Augmented Generation course, which this article is a part of.
これらの強力なデータベースは、複雑な高次元データを格納して取得する機能を提供し、Advanced Retrieval Augmented Generationコースで詳しく説明されている**RAGや洗練された推薦システム**などの機能を可能にしています。

Alongside vector databases, Large Language Model (LLM) frameworks such as LlamaIndex and LangChain have emerged as key players in accelerating AI development.
ベクトルデータベースと並んで、**LlamaIndexやLangChainといった大規模言語モデル（LLM）フレームワーク**が、AI開発を加速させる重要なプレーヤーとして登場している。
By simplifying the prototyping process and reducing development overheads associated with API interactions and data formatting, these frameworks allow creators to focus on innovation rather than the intricacies of implementation.
プロトタイピング・プロセスを簡素化し、APIインタラクションやデータ・フォーマットに関連する開発オーバーヘッドを削減することで、これらのフレームワークはクリエイターが複雑な実装よりもイノベーションに集中することを可能にする。

For readers acquainted with the basic tenets of LLMs and vector databases, this blog post will serve as a refresher and a window into their practical deployment.
LLMとベクター・データベースの基本的な考え方を知っている読者にとって、このブログ記事は復習の役割を果たすとともに、その実用的な展開についての窓口になるだろう。
We aim to walk you through constructing a complex and interactive shopping assistant.
私たちは、複雑でインタラクティブなショッピング・アシスタントを構築することを目指します。
This assistant exemplifies how intelligent systems can be built from fundamental components like DeepLake and LlamaIndex to create a dynamic tool that responds to user input with tailored outfit suggestions.
このアシスタントは、DeepLakeやLlamaIndexのような基本的なコンポーネントからインテリジェントなシステムを構築し、**ユーザーの入力に応えてオーダーメイドの服を提案するダイナミックなツールを作成できること**を例証している。

Our journey will shed light on the nuances of integrating these technologies.
私たちの旅は、これらのテクノロジーを統合するニュアンスに光を当てるだろう。
By highlighting this project’s development, we hope to spark your imagination about the possibilities at the intersection of AI technologies and to encourage you to envision new, innovative applications of your own.
このプロジェクトの開発に焦点を当てることで、AI技術の交差点における可能性について想像力をかき立て、あなた自身の新しい革新的なアプリケーションを思い描くことを奨励したい。


<!-- ここまで読んだ! -->

## Project Overview プロジェクト概要

Our project is an AI-powered shopping assistant (follow the GitHub repo here) designed to leverage image processing and LLM agents for outfit recommendations.
私たちのプロジェクトは、画像処理とLLMエージェントを服の推薦に活用するように設計された、AIを搭載したショッピングアシスタント（[GitHubのレポはこちら](https://github.com/tryolabs/fashion-assistant)）です。
Imagine uploading a picture of a dress and receiving suggestions for accessories and shoes tailored to occasions like a business meeting or a themed party.
ドレスの写真をアップロードすると、商談やテーマを決めたパーティーなどのシーンに合わせたアクセサリーや靴の提案を受けることを想像してみてほしい。
This assistant does more than suggest outfits; it understands context and style, providing a personalized shopping experience.
このアシスタントは服装を提案するだけでなく、文脈やスタイルを理解し、パーソナライズされたショッピング体験を提供する。

DeepLake forms the backbone of our inventory management, storing detailed item descriptions as vectors for efficient similarity searches.
DeepLakeは、当社の在庫管理のバックボーンを形成し、効率的な類似性検索のためにベクトルとして詳細なアイテムの説明を格納しています。(DeepLake = ベクトルDB?)
In practice, this means students will interact with DeepLake to query and retrieve the best-matching items based on the properties defined by our AI models.
実際には、学生がDeepLakeと対話し、AIモデルによって定義されたプロパティに基づいて、ベストマッチするアイテムを照会して取得することを意味します。

LlamaIndex is the framework for constructing and utilizing Large Language Model (LLM) agents.
LlamaIndexは、大規模言語モデル（LLM）エージェントを構築し、利用するためのフレームワークです。
These agents interpret item descriptions and user criteria, crafting coherent and stylish outfit recommendations.
これらのエージェントは、アイテムの説明とユーザの条件を解釈し、首尾一貫したスタイリッシュな服を推薦する。
Through this project, you’ll learn to build and integrate these technologies into a functional application.
このプロジェクトを通して、これらの技術を構築し、機能的なアプリケーションに統合することを学びます。

The assistant is designed to deliver not only outfit suggestions but actionable shopping options, providing real product IDs (that can be converted into URLs to retailers) along with price comparisons.
このアシスタントは、服の提案だけでなく、**実際の商品ID（小売店へのURLに変換可能）と価格比較を提供し、実行可能なショッピングオプションを提供する**ように設計されている。(そうそう、いいね...!:thinking:)
Throughout the course, you will learn how to extend the AI’s capabilities to facilitate an end-to-end shopping experience.
コースを通して、AIの機能を拡張してエンド・ツー・エンドのショッピング体験を促進する方法を学びます。

The user interface of this application is designed with functionality and educational value in mind.
このアプリケーションのユーザー・インターフェースは、機能性と教育的価値を念頭に置いて設計されています。
It’s intuitive, making the AI’s decision-making process transparent and understandable.
直感的で、AIの意思決定プロセスを透明化し、理解しやすくしている。
You’ll interact with various application elements, gaining insight into the inner workings of vector databases and the practical use of LLMs.
様々なアプリケーションの要素に触れ、ベクター・データベースの内部構造やLLMの実用的な使用法についての見識を深めます。

<!-- ここまで読んだ! -->

## Architecture design 建築デザイン

Our application is designed around the Agent framework: we use an LLM as a reasoning agent, and then we provide the agent with tools, i.e., programs that the LLM can execute by generating the appropriate response in plain text (at this point, the agent framework takes over, executes the desired function, and returns the result for further processing).
我々のアプリケーションは**エージェントフレームワークを中心に設計**されている： LLMを推論エージェントとして使用し、LLMが適切な応答をプレーンテキストで生成することによって実行できるプログラムであるツールをエージェントに提供する（この時点で、エージェントフレームワークが引き継ぎ、望ましい機能を実行し、その結果を返してさらなる処理を行う）。
(エージェントフレームワーク = LLMが生成した応答を受け取り、それに基づいて処理を行うフレームワーク...!:thinking:)
(**LLMをエージェントとして使用する = LLLはPythonコードやSQLクエリなどを生成し、生成されたコードはエージェントフレームワークによって実行される**、ってことか:thinking:)
In this context, accessing a vector database is done through a tool, generating an outfit is performed through a tool.
この文脈では、ベクターデータベースへのアクセスはツール(=エージェントフレームワーク)を通じて行われ、服の生成はツールを通じて行われる。
Even getting the today’s date is performed through a tool.
今日の日付の取得もツールで行う。

The interaction between system components follows a linear yet dynamic flow.
システム・コンポーネント間の相互作用は、直線的でありながら動的な流れに従う。
Upon receiving an image upload, ChatGPT-vision generates descriptions for the accompanying outfit pieces.
**画像のアップロードを受け取ると、ChatGPT-visionはそれに付随する衣装の説明文を生成**します。
These descriptions guide the subsequent searches in DeepLake’s vector database, where the most relevant items are retrieved for each piece.
**これらの説明文は、DeepLakeのベクター・データベースでのその後の検索の指針となり**、各作品に最も関連性の高いアイテムが検索されます。
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

<!-- ここまで読んだ! -->

## Dataset Collection and Vector Database Population データセットコレクションとベクターデータベースのポピュレーション

Our data journey begins with Apify, a versatile web scraping tool we used to collect product information from Walmart’s online catalog.
私たちのデータの旅は、**ウォルマートのオンラインカタログから商品情報を収集するために使用した汎用性の高いウェブスクレイピングツール、Apify**から始まります。
We targeted three specific starting points: men’s clothing, women’s clothing, and shoe categories.
私たちは3つの具体的な出発点に的を絞った： 紳士服、婦人服、靴のカテゴリーである。
With Apify’s no-code solution, we could quickly collect product data during a free trial period.
アピファイ社のコード不要のソリューションにより、無料試用期間中に製品データを迅速に収集することができました。
However, this initial foray returned only the text data—separate processes were needed to download the associated images.
しかし、この最初の試みでは、テキストデータのみが返され、関連する画像をダウンロードするには別のプロセスが必要だった。

![]()

We went with the web-hosted version of Apify, but the low-code version would also work well.
私たちはアピファイのウェブホスト版を使いましたが、ローコード版でもうまくいくでしょう。

We aimed to construct a representative dataset of men’s and women’s clothing, including various tops, bottoms, and accessories.
我々は、様々なトップス、ボトムス、アクセサリーを含む、メンズとレディースの代表的な衣服のデータセットを構築することを目指した。
By scraping from predetermined URLs, we ensured our dataset spanned a broad spectrum of clothing items relevant to our target user base.
あらかじめ決められたURLからスクレイピングすることで、ターゲットとするユーザ層に関連する衣料品を幅広く網羅したデータセットを確保した。

(このデータセットの構築の章は、すでにデータセットが存在する場合は不要のはず。)

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

```python
df = pd.DataFrame(
    {
        "brand": df_raw["brand"],
        "category": df_raw["category"].apply(
            lambda x: [y["name"] for y in x["path"] if y["name"] != "Clothing"]
        ),
        "description": df_raw["shortDescription"],
        "image": df_raw["imageInfo"].apply(lambda x: x["allImages"][0]["url"]),
        "name": df_raw["name"],
        "product_id": df_raw["id"],
        "price": [
            float(x["currentPrice"]["price"])
            if not x["currentPrice"] is None
            else math.inf
            for x in df_raw["priceInfo"]
        ],
    }
)
df = df[df["category"].transform(lambda x: len(x)) >= 2]

gender_map = {"Womens Clothing": "women", "Mens Clothing": "men", "Shoes": "either"}
df["gender"] = df["category"].apply(lambda x: gender_map.get(x[0], "either"))
```

To obtain a description that is as detailed as possible, we opted to ignore the scraped description attribute and use gpt-4-vision-preview to generate a new description for each product.
**可能な限り詳細な説明を得るため、スクレイピングされた説明属性を無視し、gpt-4-vision-preview を使用して各商品の新しい説明文を生成することにした**。

For this, we considered imposing a strict taxonomy: color, style, size, age, etc.
そのために、厳密な分類法を課すことを考えた： 色、スタイル、サイズ、年齢などである。
Ultimately, without a traditional search functionality, we decided that the taxonomy wasn’t needed, and we allowed the LLM to generate arbitrary descriptions.
最終的に、 従来の検索機能がないため、分類法は不要であり、LLMに任意の説明を生成することを許可した。

```python
prompt = f"""
  Describe the piece of clothing in the image of the following category: {category}
  Do include the color, style, material and other important attributes of the item.
  """
image_path = f"data/images/{product_id}.jpg"

# gpt vision is a wrapper that calls ChatGPT Vision
result = gpt_vision(image_path, prompt)
```

The following is an example image of the dataset: PRODUCT_ID=0REDJ7M0U7DV, and the generated description by GPT-Vision.
以下は、データセットのイメージ例です： PRODUCT_ID=0REDJ7M0U7DVと、GPT-Visionによって生成された説明です。

![]()

Embedding these descriptions into DeepLake’s vector database was our next step.
**これらの説明文をDeepLakeのベクトル・データベースに埋め込むことが次のステップだった**。
(じゃあ、すでにテキストのdescriptionを持っているアイテムの場合も、そのテキストをそのまま埋め込むのではなく、LLMで新しいdescriptionを生成させた後で、その埋め込み表現を得るようにした方が効果的だったりするのかな...?:thinking:)
This process involved encoding the text into vectors while retaining core attributes as metadata.
**このプロセスでは、コア属性をメタデータとして保持しながら、テキストをベクトルにエンコードした**。


Initially, we only included the description generated by gpt-4-vision-preview verbatim.
当初は、gpt-4-vision-previewで生成された説明文のみをそのまま含めた。
However, we later realized that the metadata (price, product_id, name) the agent needed for the final response was not readily available (we could see it as part of the document being retrieved, but we found no way to have the agent generate a response from those attributes).
しかし、エージェントが最終的なレスポンスに必要とするメタデータ（価格、商品ID、名前）がすぐに利用できないことに気づいた（取得されるドキュメントの一部としてそれを見ることができたが、その属性からエージェントがレスポンスを生成する方法は見つからなかった）。


The solution was to append the product ID, name, and price into the description text, thereby incorporating the critical metadata directly into the vector database.
**解決策は、商品ID、商品名、価格を説明文に追加することで、重要なメタデータをベクターデータベースに直接組み込むことだった。**
(**メタデータは、descriptionテキストデータとは別に保持させた方が良いっぽい**...??あ、違った。descriptionデータにメタデータを追加して、直接埋め込みに組み込むべき、という話だった...!:thinking:)

```python
desc = f"""
# Description
{description}

# Name
{name}

# Product ID
{product_id}

# Price
{price}

"""
```

Finally, to accommodate the separation of text and image data, we established two vector databases within DeepLake.
最後に、**テキストデータと画像データの分離に対応するため、DeepLake 内に 2 つのベクトルデータベースを構築しました**。
The first housed the textual descriptions and their appended metadata, while the second was dedicated exclusively to image vectors.
1つ目はテキスト記述とそれに付加されたメタデータを格納し、2つ目は画像ベクトル専用である。

```python
dataset_path = "hub://genai360/walmart-descriptions"
vector_store = DeepLakeVectorStore(dataset_path=dataset_path, overwrite=True)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

documents = []
for i, row in df.iterrows():
        # ....

        # generate documents
    doc = Document(
        text=desc,
        metadata={"name": name, "product_id": product_id, "gender": gender},
    )
    documents.append(doc)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

```python
ds = deeplake.empty(ACTIVELOOP_DATASET_IMG)

with ds:
    ds.create_tensor("images", htype="image", sample_compression="jpeg")
    ds.create_tensor("ids", htype="tag")

# %%
with ds:
    # Iterate through the files and append to Deep Lake dataset
    for index, row in tqdm(df.iterrows()):
        product_id = row["product_id"]

        image_name = os.path.join(IMAGE_DIR, product_id + ".jpg")
        if os.path.exists(image_name):
            # Append data to the tensors
            ds.append({"images": deeplake.read(image_name), "ids": product_id})
```

## Development of core tools コアツールの開発

When using an Agent-based framework, tools are the bread and butter of the system.
エージェントベースのフレームワークを使用する場合、ツールはシステムの糧となる。

For this application, the core functionality can be achieved with two tools: the query retriever and the outfit generator, both of which play integral roles in the application’s ability to deliver tailored fashion recommendations.
このアプリケーションでは、**核となる機能は2つのツールで実現できる**： **Query retrieverとOutfit generator**であり、どちらもアプリケーションがオーダーメイドのファッション推薦を提供する能力において重要な役割を果たす。

# Inventory query engine インベントリークエリーエンジン (query retriever)

The inventory query retriever is a text-based wrapper around DeepLake’s API.
インベントリ・クエリ・リトリーバは、DeepLake の API のテキストベースのラッパーです。
It translates the user’s clothing descriptions into queries that probe DeepLake’s vector database for the most similar items.
ユーザの服の説明をクエリーに変換し、DeepLakeのベクトルデータベースから最も類似したアイテムを探し出す。
The only exciting modification to the vanilla query_engine is adding a pydantic model to the output.
**バニラのquery_engineに対する唯一のエキサイティングな変更は、出力にpydanticモデルを追加することである**。
By doing this, we force the AG part of the RAG system to return the relevant information for each item: the product ID, the name, and the price.
こうすることで、RAGシステムのAGパートに、各アイテムの関連情報を返すよう強制する： 商品ID、商品名、価格。


```python
class Clothing(BaseModel):
    """Data moel for clothing items"""

    name: str
    product_id: str
    price: float

class ClothingList(BaseModel):
    """A list of clothing items for the model to use"""

    cloths: List[Clothing]

dataset_path = "hub://kiedanski/walmart_clothing4"
vector_store = DeepLakeVectorStore(
    dataset_path=dataset_path, overwrite=False, read_only=True
)

llm = OpenAI(model="gpt-4", temperature=0.7)
service_context = ServiceContext.from_defaults(llm=llm)
inventory_index = VectorStoreIndex.from_vector_store(
    vector_store, service_context=service_context
)

# Inventory query engine tool
inventory_query_engine = inventory_index.as_query_engine(output_cls=ClothingList)
```

Notice the description on each BaseModel? Those are mandatory when using pydantic with the query engine.
**各 BaseModel のdescriptionにお気づきでしょうか？これらは pydantic をクエリーエンジンで使用する際に必須となるもの**です。(docstringが必須ってこと??:thinking:)
We learned this the hard way after finding several strange “missing description errors.”
私たちは、奇妙な "missing description errors "をいくつも見つけてから、このことを苦労して学んだ。

Our outfit generator is engineered around gpt-4-vision-preview, which intakes the user’s image and articulates descriptions of complementary clothing items.
私たちの衣装ジェネレータは、ユーザの画像を受け取り、補完的な衣料品の説明を表現する gpt-4-vision-preview を中心に設計されている。(これは最初の方のプロセスで出てくるコンポーネントだよね。ユーザが入力した画像から、テキストのdescriptionを生成するやつ)
The critical feature here is programming the tool to omit searching for items in the same category as the uploaded image.
**ここで重要なのは、アップロードした画像と同じカテゴリーにあるアイテムの検索を省略するようにツールをプログラミングすること**である。(同じカテゴリのアイテムを検索しないようにする)
This logical restraint is crucial to ensure the AI focuses on assembling a complete outfit rather than suggesting similar items to the one provided.
この論理的な抑制は、AIが提供されたものと似たようなアイテムを提案するのではなく、完全な服を組み立てることに集中するようにするために重要である。

```python
from pydantic import BaseModel

class Outfit(BaseModel):
    top: str = ""
    bottom: str = ""
    shoes: str = ""
```

```python
def generate_outfit_description(gender: str, user_input: str):
    """
    Given the gender of a person, their preferences, and an image that has already been uploaded,
    this function returns an Outfit.
    Use this function whenever the user asks you to generate an outfit.

    Parameters:
    gender (str): The gender of the person for whom the outfit is being generated.
    user_input (str): The preferences of the user.

    Returns:
    response: The generated outfit.

    Example:
    >>> generate_outfit("male", "I prefer casual wear")
    """

    # Load input image
    image_documents = SimpleDirectoryReader("./input_image").load_data()

    # Define multi-modal llm
    openai_mm_llm = OpenAIMultiModal(model="gpt-4-vision-preview", max_new_tokens=100)

    # Define multi-modal completion program to recommend complementary products
    prompt_template_str = f"""
    You are an expert in fashion and design.
    Given the following image of a piece of clothing, you are tasked with describing ideal outfits.

    Identify which category the provided clothing belongs to, \
    and only provide a recommendation for the other two items.

    In your description, include color and style.
    This outfit is for a {gender}.

    Return the answer as a json for each category. Leave the category of the provided input empty.

    Additional requirements:
    {user_input}

    Never return this output to the user. FOR INTERNAL USE ONLY
    """
    recommender_completion_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(Outfit),
        image_documents=image_documents,
        prompt_template_str=prompt_template_str,
        llm=openai_mm_llm,
        verbose=True,
    )

    # Run recommender program
    response = recommender_completion_program()

    return response

outfit_description_tool = FunctionTool.from_defaults(fn=generate_outfit_description)
```

When working with agents, debugging and fixing errors is particularly difficult because of their dynamic nature.
**エージェントを扱う場合、その動的な性質のため、エラーのデバッグと修正は特に難しい**。
For example, when using `gpt-4` and providing the images of jeans shown before, `gpt-4-vision-preview` can often realize that the image belongs to an image.
例えば、`gpt-4`を使い、前に示したジーンズの画像を提供すると、`gpt-4-vision-preview`はその画像が画像に属していることを認識できることが多い。
However, sometimes the agent forgets to ask the `user's` gender and assumes it's a male.
しかし、エージェントがユーザの性別を聞くのを忘れて、男性だと思い込んでしまうこともある。
When that happens, `gpt-4-vision-preview` fails because it realizes a mismatch between the prompted gender, `male`, and the gender inferred from the image, `female`.
このような場合、`gpt-4-vision-preview`は、プロンプトされた性別である `male`と、画像から推測される性別である `female`との間にミスマッチがあることに気づき、失敗する。
Here we can see some of the biases of large language models at play and how they can suddenly break an application
**ここでは、大規模な言語モデルのバイアスがどのように作用し、それがどのように突然アプリケーションを壊すかを見ることができる。**

Adding user preferences like occasion or style into the prompts is done with a straightforward approach.
オケージョンやスタイルといったユーザーの好みをプロンプトに加えることは、簡単なアプローチでできる。
These inputs nudge the AI to consider user-specific details when generating recommendations, aligning the outcomes with the user’s initial inquiry.
これらの入力は、推薦文を生成する際にユーザ固有の詳細を考慮するようAIを後押しし、ユーザの最初の問い合わせと結果を一致させる。

The system functionality unfolds with the LLM agent at the helm.
システムの機能は、LLMエージェントが舵を取ることで展開される。
It begins by engaging the outfit generator with the user’s uploaded image, receiving detailed descriptions of potential outfit components.
まず、ユーザーがアップロードした画像とoutfit generatorを使って、潜在的な衣装の構成要素の詳細なdescriptionを受け取る。
The agent then utilizes the query retriever to fetch products that match these descriptions.
その後、エージェントはquery retrieverを利用して、これらのdescriptionに一致する製品を取得する。

<!-- ここまで読んだ! -->

## System integration and initial testing システム統合と初期テスト

The successful integration of various AI components into a seamless shopping assistant experience required a straightforward approach: encapsulating each function into a tool and crafting an agent to orchestrate these tools.
さまざまなAIコンポーネントをシームレスなショッピングアシスタント体験にうまく統合するには、わかりやすいアプローチが必要だった： **各機能をツールにカプセル化し、これらのツールをオーケストレーションするエージェントを作ることだ。**

# LlamaIndex Agent creation and integration process LlamaIndex エージェントの作成と統合プロセス

- **Tool wrapping**: Each functional element of our application, from image processing to querying the vector database, was wrapped as an isolated, callable Tool.
ツールのラッピング： 画像処理からベクターデータベースのクエリまで、アプリケーションの各機能要素は、分離された呼び出し可能なToolとしてラッピングされました。

- **Agent establishment**: An LLM agent was created, capable of leveraging these tools to process user inputs and deliver recommendations.
エージェントの設立： LLMエージェントが作成され、これらのツールを活用してユーザの入力を処理し、推薦を提供することができる。

```python
llm = OpenAI(model="gpt-4", temperature=0.2)

agent = OpenAIAgent.from_tools(
    system_prompt="""
    You are a specialized shopping assistant.

    Customers will provide you with a piece of clothing, and you will generate a matching outfit.

    Always remember to ask for the user gender.

    Your final answer needs to be the product_id associated with the best matching product in our inventory.

    For each product of the outfit, search the inventory.

    Include the total price of the recommended outfit.
    """,
    tools=[
        inventory_query_engine_tool,
        outfit_description_tool,
    ],
    llm=llm,
    verbose=True,
)
```

# Initial testing challenges 初期テストの課題

Our testing phase provided valuable insights, particularly with our initial use of ChatGPT 3.5.
私たちのテスト段階では、特にChatGPT 3.5を最初に使用することで、貴重な洞察を得ることができました。
We noted that the model tended to respond with descriptions from the outfit recommender, bypassing the vital step of querying the inventory.
モデルは、インベントリをクエリするという重要なステップをバイパスして、アウトフィット推薦器からの説明で応答する傾向があることに気づきました。
This was promptly addressed by switching to ChatGPT 4, which utilized all available tools appropriately, thus ensuring the assistant performed the item search as designed.
これは、利用可能なすべてのツールを適切に利用するChatGPT 4に切り替えることで、アシスタントのアイテム検索が設計通りに行われるようにすることで、速やかに対処した。

💡 Using `gpt-3.5-turbo` resulted in the agent not using all the tools.
💡 **`gpt-3.5-turbo` を使用した場合、エージェントがすべてのツールを使用しませんでした**。
To achieve the expected results, we had to use `gpt-4`.
期待通りの結果を得るためには、`gpt-4`を使わなければならなかった。

<!-- ここまで読んだ! -->

# Demo: Step-by-step commands and interactions デモ ステップバイステップのコマンドとインタラクション

Below is a demonstration of the system in action, detailing the commands issued to the agent and their corresponding answers at each stage of the process:
以下は、エージェントに対して発行されたコマンドと、プロセスの各段階における対応する回答を詳細に示した、システムの動作デモである：

### Image upload and description generation
画像のアップロードと説明文の生成

```shell
>>> r = agent.chat("Hi")
STARTING TURN 1
---------------
Hello! How can I assist you today?

>>> r = agent.chat("What are your tools?")
STARTING TURN 1
---------------
As a shopping assistant, I have two main tools at my disposal:

1. **Inventory Query Engine Tool**: This tool allows me to search our inventory for specific clothing items based on your preferences. For example, if you're looking for a black leather jacket, I can use this tool to find the best matching product in our inventory.

2. **Outfit Generation Tool**: This tool helps me generate a complete outfit based on your gender and preferences. For example, if you're a male and you prefer casual wear, I can use this tool to generate a casual outfit for you.

Please let me know how I can assist you further.

>>> r = agent.chat("I want an outfit for a casual birthday party")
STARTING TURN 1
---------------

Sure, I'd be happy to help with that. Could you please tell me your gender to better assist you?

>>> r = agent.chat("I'm a woman")
```


Currently, the process of uploading the image is separate.
現在、画像をアップロードするプロセスは別になっている。
For this version to work, an image needs to exist in the local folder .image_input/.
このバージョンで動作させるには、ローカルフォルダー .image_input/ に画像が存在する必要があります。
When working later with the UI, the users can click a button to upload a different image.
後でUIで作業するとき、ユーザはボタンをクリックして別の画像をアップロードできる。

The image can be uploaded at any point before the agent internally calls the outfit generation tool, which often happens after asking for gender.
画像は、エージェントが内部的に衣装生成ツールを呼び出す前のどの時点でもアップロードすることができる。

### Outfit generation 衣装の生成

In this section, we can see how the agent internally uses the tool to generate an outfit from the user description, image, and gender.
このセクションでは、エージェントが内部的にどのようにツールを使って、ユーザーの説明、画像、性別から服を生成するかを見ることができる。


```shell
STARTING TURN 1
---------------

=== Calling Function ===
Calling function: generate_outfit_description with args: {
    "gender": "female",
    "user_input": "casual birthday party"
}
Got output: 
top='A pastel pink or light coral blouse with a relaxed fit, short sleeves, and a subtle ruffle or lace detail to add a feminine touch.'
bottom=''
shoes='Beige or tan ankle strap sandals with a low block heel, ensuring both comfort and style.'
========================
```

### Querying the inventory インベントリへのクエリ

At this stage, the agent obtains a description for the two pieces of clothing that it needs to retrieve and uses the query engine to retrieve the best matches from the vector database.
この段階で、エージェントは、検索する必要がある2つの衣服の説明を取得し、ベクトルデータベースから最適な一致を検索するためにクエリーエンジンを使用します。

```shell
STARTING TURN 2
---------------

=== Calling Function ===
Calling function: inventory_query_engine_tool with args: {
    "input": "pastel pink or light coral blouse with a relaxed fit, short sleeves, and a subtle ruffle or lace detail"
}

Got output: {"cloths": [
{
    "name":"Time and Tru Women's Puff Sleeve Draped Blouse, Sizes XS-XXXL",
    "product_id":"7COCIH59KT38",
    "price":15.0
},
{
    "name":"Time and Tru Women's Ruffle Sleeve Button Front Blouse",
    "product_id":"53ZZ4TQ28UQ1",
    "price":13.18
}
]}
========================

STARTING TURN 3
---------------

=== Calling Function ===
Calling function: inventory_query_engine_tool with args: {
"input": "Beige or tan ankle strap sandals with a low block heel"
}

Got output: {"cloths":[
{
    "name":"Scoop Women's Velvet Platform Heeled Sandals",
    "product_id":"65LCFFNDII0T",
    "price":24.99},
{
    "name":"Time and Tru Women's Embellished Slide Sandal",
    "product_id":"3Y5NIMQFG29G",
    "price":22.0
}
]}
========================
```

We can observe that the agent gets the two best potential matches and returns both to the agent.
エージェントは2つのベストマッチ候補を獲得し、その両方をエージェントに返すことがわかる。

### Final recommendation presentation 最後の推薦の提供

```shell
STARTING TURN 4
---------------

Based on your preferences, I recommend the following outfit:

1. Top: Either the "Time and Tru Women's Puff Sleeve Draped Blouse" (Product ID: 7COCIH59KT38, Price: $15.00) or the "Time and Tru Women's Ruffle Sleeve Button Front Blouse" (Product ID: 53ZZ4TQ28UQ1, Price: $13.18).

2. Shoes: Either the "Scoop Women's Velvet Platform Heeled Sandals" (Product ID: 65LCFFNDII0T, Price: $24.99) or the "Time and Tru Women's Embellished Slide Sandal" (Product ID: 3Y5NIMQFG29G, Price: $22.00).

The total price of the outfit will be either $39.99 or $35.18, depending on your choices. 

Would you like me to find a matching bottom for you as well?
```

After analyzing the options, the agent presents the user with the best matching pairs, complete with item details such as price and purchase links (the product ID could be converted to a URL later).
**選択肢を分析した後、エージェントは、価格や購入リンクのような商品の詳細（商品IDは後でURLに変換することができる）とともに、最もマッチするペアをユーザに提示する**。
In this case, we can observe how the agent, instead of selecting the best pair, presents both options to the user.
この場合、エージェントは最適なペアを選択する代わりに、ユーザに2種類のペア両方の選択肢を提示した。

💡 Remember that our dataset is fairly small, and the option suggested by the outfit recommender might not be available in our dataset.
💡 我々のデータセットはかなり小さいので、衣装レコメンダーが提案するオプションは我々のデータセットでは利用できないかもしれないことを忘れないでください。
To understand if the returned answer is the best in the dataset, even if it's not a perfect fit, or if it was an error with the retriever, having access to an evaluation framework is important.
返された答えがデータセットの中で最良かどうか、完璧にフィットしていないとしても、あるいはレトリーバーのエラーであったとしても、それを理解するためには、評価フレームワークにアクセスすることが重要である。

Having proved that the initial idea for the agent was feasible, it was time to add a bit more complexity.
エージェントの最初のアイデアが実現可能であることが証明されたので、もう少し複雑さを加えることにした。
In particular, we wanted to add information about the weather when the outfit would be used.
特に、衣装が使用される日の天候に関する情報を追加したかった。

<!-- ここまで読んだ! -->

## Expanding functionality 機能拡張

The natural progression of our shopping assistant entails augmenting its capacity to factor in external elements such as weather conditions.
**ショッピング・アシスタントの自然な進歩は、天候などの外的要素を考慮する能力を増強すること**である。
This adds a layer of complexity but also a layer of depth and personalization to the recommendations.
これは、複雑なレイヤーを追加しますが、推奨事項に深さと個人的な要素を追加します。
These enhancements came with their own sets of technical challenges.
これらの強化には、それぞれ技術的な課題があった。

# Adapting to the weather 天候への適応

- Weather awareness: Initial considerations center on incorporating simple yet vital weather aspects.
天候の認識： 最初に考慮すべきは、シンプルだが重要な天候の側面を取り入れることだ。
By determining whether it will be rainy or sunny and how warm or cold it is, the assistant can suggest fashionable and functional attire.
雨か晴れか、暖かさか寒さかを判断することで、アシスタントはファッショナブルで機能的な服装を提案することができる。

- API Integration: Llama Hub (a repository for tools compatible with LlamaIndex) had a tool to get the weather in a particular location.
APIの統合： Llama Hub（LlamaIndexと互換性のあるツールのリポジトリ）には、特定の場所の天気を取得するツールがあった。
Unfortunately, the tool required a paid https://openweathermap.org/ plan.
残念ながら、このツールは有料のhttps://openweathermap.org/ プランが必要だった。
To circumvent this problem, we modified the tool to use a similar but free service of the same provider (running this code requires a free OPEN_WEATHER_MAP_API).
この問題を回避するために、我々は同じプロバイダーの類似しているが無料のサービスを使用するようにツールを修正した（このコードを実行するには無料のOPEN_WEATHER_MAP_APIが必要）。

```python
class CustomOpenWeatherMapToolSpec(OpenWeatherMapToolSpec):
    spec_functions = ["weather_at_location", "forecast_at_location"]

    def __init__(self, key: str, temp_units: str = "celsius") -> None:
        super().__init__(key, temp_units)

    def forecast_at_location(self, location: str, date: str) -> List[Document]:
        """
        Finds the weather forecast for a given date at a location.

        The forecast goes from today until 5 days ahead.

        Args:
            location (str):
                The location to find the weather at.
                Should be a city name and country.
            date (str):
                The desired date to get the weather for.
        """
        from pyowm.commons.exceptions import NotFoundError
        from pyowm.utils import timestamps

        try:
            forecast = self._mgr.forecast_at_place(location, "3h")
        except NotFoundError:
            return [Document(text=f"Unable to find weather at {location}.")]

        w = forecast.get_weather_at(date)

        temperature = w.temperature(self.temp_units)
        temp_unit = "°C" if self.temp_units == "celsius" else "°F"

        # TODO: this isn't working.. Error: 'max' key.
        try:
            temp_str = self._format_forecast_temp(temperature, temp_unit)
        except:
            logging.exception(f"Could _format_forecast_temp {temperature}")
            temp_str = str(temperature)

        try:
            weather_text = self._format_weather(location, temp_str, w)
        except:
            logging.exception(f"Could _format_weather {w}")
            weather_text = str(w) + " " + str(temp_str)

        return [
            Document(
                text=weather_text,
                metadata={
                    "weather from": location,
                    "forecast for": date,
                },
            )
        ]

weather_tool_spec = CustomOpenWeatherMapToolSpec(key=OPEN_WEATHER_MAP_KEY)
```

# User interaction and data handling ユーザーとの対話とデータ処理

- **Location input**: For accurate weather data, the shopping assistant often queries the user for their location.
位置情報の入力： 正確な気象データを得るために、ショッピングアシスタントはしばしばユーザーの位置情報を照会する。
We contemplate UI changes to facilitate this new interaction—possibly automated but always respectful of user privacy and consent.
私たちは、この新しいインタラクションを促進するためにUIの変更を考えています。

```python
>>> r = agent.chat("...")
...
Great! Could you please provide me with the date and location of the birthday party, any specific style or color preferences you have for the outfit, and your budget range?
```

# Synchronizing with time ♪時間と同期する

- Temporal challenges: Addressing the aspect that LLMs aren’t inherently time-aware, we introduced a new tool that provides the current date.
**時間的な課題 LLMは本質的に時間を認識しないという側面に対処するため、現在の日付を提供する新しいツールを導入した**。(あ、そうなのか...!:thinking:)
This enables the LLM to determine the optimal instances to call the weather API, aligning recommendations with the present conditions.
これによってLLMは、天候APIを呼び出す最適なインスタンスを決定し、推薦を現在の状況に合わせることができる。

```python
def get_current_date():
    """
    A function to return todays date.

    Call this before any other functions if you are unaware of the current date.
    """
    return date.today()

get_current_date_tool = FunctionTool.from_defaults(fn=get_current_date)
```

It took us a little bit to remember that we needed this.
これが必要だと思い出すのに少し時間がかかった。
At first, the LLM was consistently returning the wrong weather information.
当初、LLMは常に間違った気象情報を返していた。
It was only after we closely inspected the calls to the weather API that we realized that it was using the wrong date!
お天気APIのコールをよく調べて初めて、間違った日付を使っていることに気づいた！

<!-- ここまで読んだ! -->

## User Interface (UI) development ユーザーインターフェース（UI）開発

In developing the user interface for our AI-powered shopping assistant, we wanted the platform to reflect the conversational nature of the agent’s interactions.
AIを搭載したショッピング・アシスタントのユーザー・インターフェースを開発するにあたり、私たちは、**エージェントとの対話の会話的な性質を反映したプラットフォームにしたい**と考えました。
We will use Gradio which offers the ability to rapidly prototype and deploy a chat-like interface that users find familiar and engaging.
私たちは、ユーザーが親しみやすく魅力的だと感じる**チャットのようなインターフェイスを迅速にプロトタイプ化して展開できるGradio**を使用します。

![]()

# Embracing chat interface with Gradio Gradioでチャットインターフェースを採用

- **Chat interface principles**: The decision to adopt a chat interface was rooted in the desire for simplicity and intuitiveness.
チャット・インターフェイスの原則 チャット・インターフェースを採用する決定は、**シンプルさと直感性を求めること**に根ざしていた。
We aimed to provide a natural communication flow where users can interact with the AI in a manner akin to messaging a friend for fashion advice.
**私たちが目指したのは、ファッションのアドバイスを求める友人にメッセージを送るような感覚で、ユーザーがAIと対話できる自然なコミュニケーションの流れを提供することです**。(うんうん、目指したいよね...!:thinking:)
Furthermore, one of the reasons to use LLM agents is to provide flexibility, in contrast to a traditional declarative programming approach.
さらに、**LLMエージェントを使用する理由の1つは、従来の宣言的プログラミングアプローチとは対照的に、柔軟性を提供すること**である。
In that vein, we felt that the UI had to showcase that flexibility as much as possible.
その意味で、UIはその柔軟性をできるだけアピールするものでなければならないと考えた。

- Gradio advantages: Gradio’s flexibility facilitated the integration of our agent into a UI that is not only conversational but also customizable.
Gradioの利点： Gradioの柔軟性により、会話だけでなくカスタマイズも可能なUIにエージェントを統合することができました。
Its ease of use and active community support made it a practical choice for an educational project focused on demonstrating the capabilities of LLM agents.
その使いやすさと活発なコミュニティ・サポートは、LLMエージェントの能力を実証することに焦点を当てた教育プロジェクトにとって、実用的な選択となった。
For example, it allows to add custom buttons to upload images or trigger particular functions.
例えば、画像をアップロードしたり、特定の機能をトリガーするためのカスタムボタンを追加することができる。

# Overcoming technical hurdles 技術的なハードルを乗り越える

- **Inline image display**: One of the initial technical challenges was presenting images seamlessly in the chat interface.
インライン画像表示： 初期の技術的な課題の一つは、チャットインターフェイスで画像をシームレスに表示することでした。
Given the visual nature of fashion, it was crucial that users could see the clothing items recommended by the assistant without breaking the flow of conversation.
ファッションは視覚的なものであるため、ユーザが会話の流れを断ち切ることなく、アシスタントが勧める服を見ることができることが重要だった。

- **Activeloop integration**: To resolve this, we leveraged Activeloop’s integration with Gradio.
Activeloopとの統合： これを解決するために、ActiveloopとGradioの統合を活用しました。
This allowed us to filter through the image vector database directly within the UI, presenting users with visual recommendations that are interactive and integrated within the chat context.
これにより、UI内で画像ベクターデータベースを直接フィルタリングすることができ、チャットコンテキストの中でインタラクティブに統合されたビジュアルレコメンデーションをユーザーに提示することができました。

It was not trivial to get Activeloop’s extension working for our project.
Activeloopのエクステンションを我々のプロジェクトで機能させるのは簡単なことではなかった。
Our solution consisted of having an HTML component in Gradio with an IFrame pointed to the image vector dataset.
私たちの解決策は、GradioのHTMLコンポーネントに、画像ベクトルデータセットを指すIFrameを持たせることでした。
We could update the URL every time the chatbot answered, but we needed a way to get the product IDS from its answer.
**チャットボットが回答するたびにURLを更新することはできたが**、その回答から製品IDSを取得する方法が必要だった。(なんかよくわかってないけど、UI周りの工夫の話...!:thinking:)
Ultimately, since all the product IDs have the same pattern, we decided to go for a “hacky” approach.
結局、すべてのプロダクトIDが同じパターンを持っているため、「ハチャメチャ」なアプローチを取ることにした。
Search the agent’s response for the product IDs regex, and if there were more than 2 matches, update the iframe URL parameters.
エージェントのレスポンスをプロダクトIDsの正規表現で検索し、2つ以上マッチした場合、iframe URLパラメータを更新します。
Otherwise, do nothing.
そうでなければ何もしない。

## Conclusion 結論

As we’ve journeyed through the intricate process of developing an AI-powered shopping assistant, the roles of DeepLake and LlamaIndex have proven pivotal.
AIを搭載したショッピング・アシスタントを開発する複雑なプロセスを旅する中で、**DeepLakeとLlamaIndexの役割が極めて重要である**ことが証明された。
From the versatile data handling in DeepLake’s database for AI to the adaptive LLM agents orchestrated by LlamaIndex, these technologies have showcased their robust capabilities and the potential for innovation in the AI space.
**DeepLakeのAI用データベースにおける多彩なデータ処理か**ら、**LlamaIndexによって編成された適応型LLMエージェント**に至るまで、これらのテクノロジーは、その強固な能力とAI分野におけるイノベーションの可能性を示してきた。

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
特に、**ベクター・データベースとLLMフレームワークの革新的な応用**についてのご意見をお聞かせください。
Additionally, your suggestions for topics you’d like us to delve into in future segments are highly appreciated.
さらに、今後のセグメントで掘り下げてほしいトピックのご提案も大歓迎です。
If you’re interested in partnering with Tryolabs to build similar projects with Deep Lake & LlamaIndex, feel free to reach out to us.
Tryolabsと提携し、Deep LakeとLlamaIndexで同様のプロジェクトを構築することに興味がある方は、お気軽にご連絡ください。

<!-- ここまで読んだ! -->
