refs: https://shopify.engineering/leveraging-multimodal-llms?utm_source=chatgpt.com


# Leveraging multimodal LLMs for Shopify’s global catalogue: Recap of expo talk at ICLR 2025 ShopifyのグローバルカタログにおけるマルチモーダルLLMの活用：ICLR 2025でのエクスポトークの要約

Our Global Catalogue demonstrates the impact of multimodal LLMs on one of commerce’s hardest problems: building a unified, structured, and continuously evolving understanding of billions of product listings created by millions of merchants.
私たちのグローバルカタログは、商業の最も難しい問題の一つである、数百万の商人によって作成された数十億の製品リストの統一された、構造化された、そして継続的に進化する理解を構築する上でのマルチモーダルLLMの影響を示しています。

## I. Introduction はじめに

As the world of commerce rapidly evolves—shifting from browsing websites to conversing with AI agents—the need for high-quality, standardized product data has never been greater. 
商業の世界が急速に進化し、ウェブサイトの閲覧からAIエージェントとの会話へと移行する中で、**高品質で標準化された製品データの必要性**はかつてないほど高まっています。
The future of shopping increasingly looks like this: “Show me sustainable running shoes under $150”, but the answer you get depends entirely on the quality of the data the AI has access to. 
ショッピングの未来はますますこうなっています：**「150ドル以下の持続可能なランニングシューズを見せてください」、しかし、得られる答えはAIがアクセスできるデータの質に完全に依存**しています。(なるほど、構造化ってここにも効いてくるのか...!:thinking:)

<!-- ここまで読んだ! -->

For Shopify merchants, that’s both an opportunity and a challenge. 
Shopifyの商人にとって、それは機会でもあり、課題でもあります。
Merchants need their products to be fluently understood by machines, not just humans. 
商人は、自分の製品が人間だけでなく、機械にも流暢に理解される必要があります。
The challenge? Shopify hosts millions of merchants who describe billions of products in wonderfully unique ways. 
その課題とは？ Shopifyは、数百万の商人が数十億の製品を素晴らしくユニークな方法で説明するプラットフォームです。
That diversity, while an incredible strength for commerce, is kryptonite for machine understanding. 
その多様性は商業にとっては驚くべき強みですが、機械の理解にとってはクリプトナイトです。

That’s where Shopify’s Global Catalogue comes in—a new intelligence layer that unifies, standardizes, and enriches product data across Shopify. 
そこで登場するのがShopifyのGlobal Catalogueです。これは、**Shopify全体の製品データを統一、標準化、強化する新しいインテリジェンスレイヤー**です。
At the International Conference on Learning Representations (ICLR) 2025 Expo in Singapore, we presented the core engineering behind this initiative—how we use multimodal Large Language Models (LLMs) to organize and augment every item sold across our platform. 
私たちは、シンガポールで開催された国際学習表現会議（ICLR）2025エキスポで、このイニシアチブの背後にあるコアエンジニアリングを発表しました。つまり、**私たちがどのようにマルチモーダル大規模言語モデル（LLMs）を使用して、プラットフォーム上で販売されるすべてのアイテムを整理し、強化しているか**です。(論文とかあったら参考になりそう...!:thinking:)

In this recap post of our presentation, you’ll get a technical summary of our approach: from data curation through model fine-tuning and training, to the infrastructure that lets us make 40 million multimodal LLM-powered inferences daily. 
このプレゼンテーションの**要約記事**(あ、上述の国際会議の発表の要約なのね!:good:)では、私たちのアプローチの技術的な概要をお届けします。データのキュレーションからモデルのファインチューニングとトレーニング、そして私たちが毎日4000万のマルチモーダルLLM駆動の推論を行うためのインフラストラクチャまでを含みます。
We will also cover the impact of these new data pipelines across Shopify’s search, recommendations, conversational commerce, and where we are heading next. 
また、これらの新しいデータパイプラインがShopifyの検索、推薦、会話型コマースに与える影響と、私たちが次に向かう方向についても触れます。

<!-- ここまで読んだ! -->

## II. 問題: 断片化した製品データと発見の課題

Historically, Shopify revolved around the merchant and their shop. 
歴史的に、Shopifyは商人とそのショップを中心に展開してきました。
Each shop was an independent island, with the merchant free to create products with virtually any structure they desired. 
**各ショップは独立した島であり、商人はほぼ任意の構造で製品を作成する自由**がありました。 
This approach dramatically lowered the barrier for entrepreneurs, and encouraged merchants’ creativity and freedom. 
このアプローチは起業家にとっての障壁を大幅に下げ、商人の創造性と自由を促進しました。 
However, this flexibility came with a few important challenges: 
しかし、この柔軟性にはいくつかの重要な課題が伴いました：

- Unstructured data: Most product information is provided in free-form text instead of being organized in structured and standardized fields. 
  - **非構造化データ: ほとんどの製品情報は、構造化された標準化されたフィールドに整理されるのではなく、自由形式のテキストで提供**されます。 
    There is no uniformity. 
    一貫性がありません。 
    One merchant might give us a novel’s worth of product description, while another might provide just a title and price. 
    ある商人は小説のような製品説明を提供する一方で、別の商人はタイトルと価格だけを提供するかもしれません。

- Schema heterogeneity: Each merchant on Shopify can define their own keys (attribute names) and values for these options, leading to non-uniform data structures. 
  - **スキーマの異質性**: Shopifyの各商人は、これらのオプションに対して独自のキー（属性名）と値を定義できるため、非一様なデータ構造が生じます。

- Data quality and sparsity: Product listings can have typos, missing values, misclassifications, or irrelevant content. 
  - **データの質と希薄性**: 製品リストには誤字、欠損値、誤分類、または無関係なコンテンツが含まれることがあります。 
    Structured product records may not consistently contain the correct value in the correct field (e.g., the brand of the product is listed in the title but omitted in the brand field). 
    構造化された製品記録は、正しいフィールドに正しい値を一貫して含まない場合があります（例: 製品のブランドがタイトルに記載されているが、ブランドフィールドには省略されている）。

- Multimodality: Information about a product may be present in text, images or videos. 
  - マルチモーダリティ: **製品に関する情報は、テキスト、画像、または動画に存在する**場合があります。 
    Key attributes may only be featured in an image and omitted from text fields. 
    重要な属性は画像にのみ表示され、テキストフィールドから省略されることがあります。

- Multilingual: Merchants are present in every continent and leverage different languages and market terminologies. 
  - 多言語: 商人はすべての大陸に存在し、異なる言語や市場用語を活用しています。

<!-- ここまで読んだ! -->

Traditionally, this patchwork of product data leads to classic e-commerce pain points: difficulty in semantic search, poor faceting, duplicate or hard-to-find listings, and limited ability to surface the best—or most relevant—choices for buyers. 
伝統的に、**この断片的な製品データは、セマンティック検索の難しさ、ファセットの不備、重複または見つけにくいリスト、そして購入者にとって最良または最も関連性の高い選択肢を提示する能力の制限といった、古典的なeコマースの痛点**を引き起こします。(高品質に構造化された製品データさえあれば、ユーザが求める商品を正確に見つけられるようになるってことか...!!:thinking:)

As commerce shifts toward AI-driven experiences, the impact of fragmentation becomes even more acute. 
商取引がAI駆動の体験にシフトするにつれて、断片化の影響はさらに深刻になります。 
Even the most advanced AI agents are limited by messy, inconsistent product data—without unified, structured information, they struggle to deliver accurate, trustworthy, and efficient product discovery experiences. 
**最も高度なAIエージェントでさえ、混乱した一貫性のない製品データに制約されており、統一された構造化情報がなければ、正確で信頼できる効率的な製品発見体験を提供するのに苦労します。** (高品質に構造化された製品データがあれば、LLMの性能もenrichできるってことか...!!:thinking:)

Unlocking the full potential of AI-driven commerce requires product data that machines can reliably understand, compare, and act upon at scale. 
AI駆動の商取引の完全な可能性を引き出すには、機械が信頼性を持って理解し、比較し、大規模に行動できる製品データが必要です。

<!-- ここまで読んだ! -->

## III. The solution: The global catalogue powered by multimodal LLMs 解決策：マルチモーダルLLMによって支えられたグローバルカタログ

The Global Catalogue is a unified foundation for product knowledge, built to organize and enrich product data across all of Shopify. 
グローバルカタログは、**Shopify全体の製品データを整理し、豊かにするために構築された製品知識の統一された基盤**です。
It operates through four integrated layers: product data, product understanding, product matching, and reconciliation.
これは、**製品データ、製品理解、製品マッチング、および調整の4つの統合層**を通じて機能します。(4つの層、ふむふむ...!:thinking:)

### Layer 1: Product data foundation 層1：製品データ基盤

(あ、商品が追加されたり変更されたりをcatchするための仕組みね...!!:thinking:)

Handles the full variety, volume, and volatility of commerce data. 
商取引データの多様性、ボリューム、および変動性を完全に処理します。
We process over 10 million product updates daily from merchant uploads, APIs, apps, and integrations, in a streaming fashion. 
私たちは、商人のアップロード、API、アプリ、および統合から、毎日1000万件以上の製品更新をストリーミング方式で処理します。
A custom schema-evolution system keeps data compatible as merchants innovate. 
カスタムスキーマ進化システムは、商人が革新する際にデータの互換性を保ちます。
A change data capture mechanism records all product modifications, enabling consistent historical views and robust incremental processing. 
変更データキャプチャメカニズムは、すべての製品変更を記録し、一貫した履歴ビューと堅牢な増分処理を可能にします。

<!-- ここまで読んだ! -->

### Layer 2: Product understanding 層2：製品理解

The product understanding layer transforms unstructured data into standardized metadata through multiple tasks: 
製品理解層は、複数のタスクを通じて非構造化データを標準化されたメタデータに変換します：

(この層で、以下のような色んな観点での抽出やら分類やら = 製品理解を行うのね...!!:thinking:)

- Product classification: Assigns each product to a hierarchical taxonomy. 
  - 製品分類：各製品を階層的な分類法に割り当てます。

- Attribute extraction: Identifies and normalizes key features such as color, size, material, brand, and model. 
  - 属性抽出：色、サイズ、素材、ブランド、モデルなどの主要な特徴を特定し、標準化します。

- Image understanding: Extracts color (as hex codes), evaluates image quality, and detects visual product attributes. 
  - 画像理解：色（16進数コードとして）を抽出し、画像の品質を評価し、視覚的な製品属性を検出します。

- Title standardization: Normalizes verbose merchant titles (e.g., “iPhone 16 Pro 256GB Silver” → “iPhone 16”). 
  - タイトル標準化：冗長な商人のタイトルを標準化します（例：“iPhone 16 Pro 256GB Silver” → “iPhone 16”）。

- Description analysis: Summarizes descriptions and surfaces key selling points. 
  - 説明分析：説明を要約し、主要な販売ポイントを浮き彫りにします。

- Review summarization: Generates aggregated quality and sentiment signals from customer reviews. 
  - レビュー要約：顧客レビューから集約された品質と感情の信号を生成します。

![]()

We structure these as a multi-task, multi-entity problem. 
**これらをマルチタスク、マルチエンティティの問題として構成**します。
Each entity represents a different grain of the catalogue. 
**各エンティティはカタログの異なる粒度を表します。**
In the diagram, we have highlighted three key entities: media, products, and variants. 
図では、メディア、製品、およびバリアントの3つの主要なエンティティを強調しています。
Other examples of entities include sellers and reviews. 
他のエンティティの例には、販売者やレビューが含まれます。
(entity = Shopifyにおける「もの」の概念。製品entity、バリアントentity、メディアentity、販売者entity、レビューentityなどがある:thinking:)

For each catalogue entity, we fine-tune a vision large language model to perform multiple tasks simultaneously, rather than following the traditional approach of building separate models for each task. 
各カタログエンティティに対して、複数のタスクを同時に実行するためにビジョン大規模言語モデルをファインチューニングします。これは、**各タスクのために別々のモデルを構築する従来のアプローチに従うのではありません。**
(うーん。複数のタスクを一つのモデルでやらせるのか...!!これは悪手じゃないか?? 新しいタスクが出てきた時に追加しづらくないだろうか...!!:thinking:)
This architectural choice was not only efficient, we found that these tasks have strong interdependencies—category inferences provide crucial context for text summarization, while text summarization can refine classification decisions—yielding higher quality inferences than a siloed approach. 
このアーキテクチャの選択は効率的であるだけでなく、**これらのタスクには強い相互依存性があることがわかりました。カテゴリの推論はテキスト要約に重要な文脈を提供し、テキスト要約は分類決定を洗練させることができ、サイロ化されたアプローチよりも高品質な推論を生み出します。** (なるほど、そういう判断なのね...!LLMはjoint inferenceが得意、って言われてるっぽい...!:thinking:)

<!-- ここまで読んだ! -->

#### Shopify’s taxonomy Shopifyの分類体系

Shopify’s open-source product taxonomy defines the inference space for categories and attributes. 
Shopifyの**オープンソース製品taxonomyは、カテゴリと属性の推論空間(=行動空間, 分類の選択肢、うんうんわかる...!!:thinking:)を定義**します。
We leverage LLMs to continuously identify new attribute and category requirements by analyzing product listing patterns, with changes validated through both automated and human-in-the-loop review. 
私たちは、**製品リストパターンを分析することで新しい属性とカテゴリの要件を継続的に特定するためにLLMを活用し、変更は自動化されたレビューと人間のレビューの両方を通じて検証**されます。(LLMで製品リストのパターンを分析して、必要なカテゴリや属性が新たにあれば、LLMと人手によるレビューを経てtaxonomyに追加していくわけね...!!:thinking:)
The taxonomy attributes are linked to taxonomy nodes, ensuring each product type receives relevant attributes; these propagate hierarchically and adapt as the taxonomy evolves. 
taxonomy属性はtaxonomyノードにリンクされており、各製品タイプが関連する属性を受け取ることを保証します。これらは階層的に伝播し、taxonomyの進化に伴って適応します。
(taxonomyノードの例 = スマホ, taxonomy属性の例 = 色、ストレージサイズ、ブランドなど。両者はリンクしてる。例えばtaxonomyノード=Tシャツには別のtaxonomy属性がリンクしてて、それらの製品にはその属性が付与されることを保証する、みたいな??:thinking:)

<!-- ここまで読んだ! -->

### Layer 3: Product matching 層3：製品マッチング

After understanding individual products, we must identify when different merchants sell the same item. 
個々の製品を理解した後、**異なる商人が同じアイテムを販売しているとき**にそれを特定する必要があります。
(これをニュースに例えると、異なるメディアが同じニュースストーリーを報じてる時、それらを特定する、みたいな...??:thinking:)
This involves a multi-stage process to cluster related listings.
これは、関連するリスティングをクラスタリングするためのマルチステージプロセスを含みます。

Candidate generation focuses on producing high-recall candidate clusters. 
候補生成は、高リコールの候補クラスタを生成することに焦点を当てています。
We use locality-sensitive hashing, embedding-based clustering and other probabilistic methods to create fuzzier connections between products. 
私たちは、局所感度ハッシュ、埋め込みベースのクラスタリング、および他の確率的手法を使用して、製品間にあいまいな接続を作成します。
We also identify deterministic matches through features like universal product codes and high-confidence feature combinations, such as “same-title and same-image match.” 
また、ユニバーサル製品コードや「同じタイトルと同じ画像のマッチ」のような高信頼度の特徴の組み合わせを通じて決定的なマッチを特定します。

A cascade of discriminator models validates these matches. 
一連の識別モデルがこれらのマッチを検証します。
The system maintains high-precision through what we call 'edge pruning.' 
システムは、私たちが「エッジプルーニング」と呼ぶ方法を通じて高精度を維持します。
After identifying candidate matches, we apply these discriminators to remove potentially incorrect edges. 
候補マッチを特定した後、これらの識別器を適用して潜在的に不正確なエッジを削除します。
This is crucial because a single incorrect edge can create a large cluster of mismatched products. 
これは重要です。なぜなら、1つの不正確なエッジが不一致の製品の大きなクラスタを作成する可能性があるからです。

We formulate the matching problem as a bipartite graph where: 
マッチング問題を二部グラフとして定式化します：

- Products form the left-hand nodes 
  - 製品は左側のノードを形成します
- Attributes, such as deterministic features and fuzzier candidate matches, form the right-hand nodes 
  - 属性（決定的な特徴やあいまいな候補マッチなど）は右側のノードを形成します

![]()

By computing connected components on this graph, we obtain initial product clusters to which we assign Universal Product IDs. 
このグラフ上で連結成分を計算することにより、ユニバーサル製品IDを割り当てる初期製品クラスタを取得します。

<!-- ここまで読んだ! -->

### Layer 4: Reconciliation 層4：調整

For identified product clusters, the reconciliation layer constructs a canonical product record by aggregating all inferred metadata: 
特定された製品クラスタに対して、調整層はすべての推論されたメタデータを集約して標準的な製品レコードを構築します：

- Attribute merging: Complementary data from multiple listings is combined to yield the broadest, most accurate set of attributes (technical specs, options, etc.). 
  - 属性のマージ：複数のリスティングからの補完データを組み合わせて、最も広範で正確な属性セット（技術仕様、オプションなど）を生成します。

- Variant normalization: Different representations of variants (e.g., color names, size choices) are standardized and unified. 
  - バリアントの標準化：バリアントの異なる表現（例：色名、サイズ選択）が標準化され、統一されます。

- Content aggregation: Descriptions, technical information, and review summaries are merged; highest-quality media are selected to represent the item. 
  - コンテンツの集約：説明、技術情報、およびレビュー要約が統合され、アイテムを表すために最高品質のメディアが選択されます。

The resulting canonical product serves as the authoritative source for downstream systems. 
**結果として得られる標準的な製品は、下流システムの権威あるソースとして機能**します。

All four layers depend on the use of multimodal LLMs for product understanding, entity resolution, and to create a canonical representation of each item. 
4つの層すべては、製品理解、エンティティ解決、および各アイテムの標準的な表現を作成するためにマルチモーダルLLMの使用に依存しています。
The following sections detail our approach to model training, data generation, and production deployment at scale. 
次のセクションでは、モデルのトレーニング、データ生成、および大規模な生産展開に対する私たちのアプローチの詳細を説明します。

<!-- ここまで読んだ! -->

## IV. Fine-tuning for flexibility and performance 柔軟性とパフォーマンスのためのファインチューニング

Fine-tuning LLMs involves taking a pre-trained language model and training it further on a specific dataset for a particular task. 
LLMのファインチューニングは、事前に訓練された言語モデルを取り、特定のタスクのために特定のデータセットでさらに訓練することを含みます。
While commercial APIs like OpenAI and Gemini work well at a smaller scale, our volume makes them prohibitively expensive. 
**OpenAIやGeminiのような商業APIは小規模ではうまく機能しますが、私たちのボリュームではそれらは非常に高価になります。** (あ〜性能が理由っていうよりは、コストが理由でOSSのLLMをfine-tuningして自社ホストしてるのね...!!:thinking:)
We achieved better performance and control by fine-tuning smaller open source vision large language models. 
私たちは、より小さなオープンソースのビジョン大規模言語モデルをファインチューニングすることで、より良いパフォーマンスと制御を達成しました。

We have deployed three successive open-source models: LlaVA 1.5 7B, LLaMA 3.2 11B, and currently Qwen2VL 7B. 
私たちは、LlaVA 1.5 7B、LLaMA 3.2 11B、そして現在のQwen2VL 7Bという3つの連続したオープンソースモデルを展開しました。
Each transition delivered higher accuracy while reducing GPU requirements. 
各移行は、GPUの要件を削減しながら、より高い精度を提供しました。
We continuously assess emerging models, weighing accuracy gains against computational costs. 
私たちは新たに出現するモデルを継続的に評価し、精度の向上と計算コストを天秤にかけています。

<!-- ここまで読んだ! -->

#### Selective field extraction 選択的フィールド抽出

Returning to our multi-task, multi-entity setup, while we found that tackling multiple tasks simultaneously led to improved performance across each individual task, we also found that asking the model to predict all fields during fine-tuning led to a loss of generalizability at inference time. 
マルチタスク・マルチエンティティの設定に戻ると、**複数のタスクを同時に扱うことで各個別タスクのパフォーマンスが向上する**ことがわかりましたが、**ファインチューニング中にモデルにすべてのフィールドを予測させることは、推論時の一般化能力の喪失につながること**もわかりました。(推論は一斉にやらせるけど、学習というかfine-tuningは個別にやらせる、みたいな感じ??:thinking:)

Instead of training our models to extract all fields, we adjusted our training strategy to randomly select for each training instance which fields the model should predict. 
**すべてのフィールドを抽出するようにモデルを訓練するのではなく、各トレーニングインスタンス(=training example)に対してモデルが予測すべきフィールドをランダムに選択するように訓練戦略を調整**しました。
During training, a model might be asked to extract only the category for one example, then category plus title for another, and perhaps just the standardized description for a third. 
トレーニング中、モデルは1つの例に対してカテゴリのみを抽出するように求められ、次に別の例に対してカテゴリとタイトルを、そしておそらく3つ目の例に対して標準化された説明のみを抽出するように求められることがあります。
This approach teaches the model to adapt to different extraction requirements at inference time without retraining. 
このアプローチは、モデルに再訓練なしで推論時の異なる抽出要件に適応することを教えます。

The benefits of this strategy became clear in production. 
この戦略の利点は、実運用で明らかになりました。
Not only did models trained with selective field extraction retain better generalization capabilities, but we reduced median latency from 2 seconds to 500 milliseconds. 
**選択的フィールド抽出で訓練されたモデルは、より良い一般化能力を保持するだけでなく、中央値のレイテンシを2秒から500ミリ秒に削減**しました。
Moreover, by generating fewer tokens, we substantially reduced GPU usage by 40%, allowing us to serve more requests with the same hardware, which has made our system more cost-effective. 
さらに、トークンの生成を減らすことで、GPUの使用量を40%削減し、同じハードウェアでより多くのリクエストに対応できるようになり、システムのコスト効率が向上しました。

<!-- ここまで読んだ! -->

## V. Data generation and continuous improvement データ生成と継続的改善

Shipping fine-tuned models starts with high-quality data for training and evaluation. 
ファインチューニングされたモデルの出荷は、**トレーニングと評価のための高品質なデータ**から始まります。 
We developed an annotation pipeline that combines LLM agents and human expertise. 
私たちは、LLMエージェントと人間の専門知識を組み合わせたアノテーションパイプラインを開発しました。

### Automated annotation pipeline 自動アノテーションパイプライン:

We structure our training datasets around each individual catalog entity. 
私たちは、各個別のカタログエンティティを中心にトレーニングデータセットを構成します。 
We begin by sampling data and taking a temporal snapshot of the entity data. 
データをサンプリングし、**エンティティデータの時間的スナップショットを取得**することから始めます。 
Then, for each extraction task, such as category classification, we deploy multiple LLM agents that act as annotators. 
次に、カテゴリ分類などの各抽出タスクに対して、アノテーターとして機能する複数のLLMエージェントを展開します。 
These agents independently analyze the product and suggest appropriate categories. 
これらのエージェントは独立して製品を分析し、適切なカテゴリを提案します。

- For test samples, suggestions from these agents are presented to human annotators using a specialized interface. 
  - テストサンプルの場合、これらのエージェントからの提案は、専門のインターフェースを使用して人間のアノテーターに提示されます。(まずLLMがアノテーションして、その後人間がレビューする、みたいな感じ...!:thinking:)
    Humans resolve ambiguities and provide gold labels; consensus is established for evaluation. 
    **人間が曖昧さを解消し、ゴールドラベルを提供します。評価のために合意が形成**されます。

- For train samples, we scale up using an LLM arbitrator—another model trained to select the best agent suggestion or abstain with human fallback as needed. 
  - トレインサンプルの場合、最良のエージェントの提案を選択するか、必要に応じて人間のフォールバックで控えるように訓練された別のモデルであるLLM仲裁者を使用してスケールアップします。(全部人間がアノテーションできるわけじゃないので、量的に。なのでここは別のLLMにレビューさせる、みたいな感じか...!:thinking:)
  This balances accuracy and scalability, allowing us to build high quality datasets much faster than by relying on human annotators alone. 
  これにより、精度とスケーラビリティのバランスが取れ、人間のアノテーターだけに依存するよりもはるかに速く高品質なデータセットを構築できます。

<!-- ここまで読んだ! -->

### Test set review interface テストセットレビューインターフェース:

- Annotators see the product image(s), raw description, and LLM suggestions. 
  - アノテーターは製品の画像、原始的な説明、およびLLMの提案を確認します。 
  They can pick, reject, or search for the best label in the taxonomy tree. 
  彼らは、分類ツリーの中で最適なラベルを選択、拒否、または検索できます。

- We leverage randomization to measure and correct for bias in human annotations and to encourage searching for the correct label when none of the agent annotations are appropriate. 
  - 私たちは、ランダム化を活用して人間のアノテーションのバイアスを測定し修正し、エージェントのアノテーションが適切でない場合に正しいラベルを探すことを促します。

<!-- ここまで読んだ! -->

### Comprehensive model evaluation 包括的なモデル評価:

Evaluating multi-task extraction models requires additional metrics that go beyond traditional machine learning metrics. 
**マルチタスク抽出モデルを評価するには、従来の機械学習メトリクスを超える追加のメトリクスが必要**です。
We developed three categories of evaluation metrics to ensure our models perform well across all dimensions. 
私たちは、**モデルがすべての次元で良好に機能することを保証するために、3つの評価メトリクスのカテゴリを開発**しました。

- Task-specific metrics: Precision/recall at multiple category hierarchy levels for classification; accuracy for attribute extraction. 
  - **タスク特有のメトリクス**：分類のための複数のカテゴリ階層レベルでの精度/再現率；属性抽出のための精度。 

- LLM judge metrics: For generative fields (like standardized title or description), synthetic “judges” grade outputs against detailed guidelines. 
  - **LLMジャッジメトリクス**：生成フィールド（標準化されたタイトルや説明など）に対して、合成の「ジャッジ」が詳細なガイドラインに基づいて出力を評価します。

- Instruction metrics: Since our models must respond to selective extraction requests, these metrics measure instruction following capability. 
  - **インストラクションメトリクス**：私たちのモデルは選択的抽出要求に応じる必要があるため、これらのメトリクスは**指示に従う能力を測定**します。 
  - Field compliance rate: How often the model outputs only the requested fields. 
    - **フィールドコンプライアンス率**：モデルが要求されたフィールドのみを出力する頻度。 

  - Field invariance rate: Consistency of answers for a given field, regardless of changes in the requested output schema. 
    - **フィールド不変率**：要求された出力スキーマの変更に関係なく、特定のフィールドに対する回答の一貫性。 

The instruction metrics are particularly important for maintaining model accuracy. 
インストラクションメトリクスは、モデルの精度を維持するために特に重要です。 
We need confidence that requesting additional fields at inference time will not change the model’s inference for previously requested information. 
**推論時に追加のフィールドを要求しても、以前に要求された情報に対するモデルの推論が変わらないという自信が必要**です。
(これは本当にそうなんだよな。だから自分としてはフィールドごとに独立した推論器を稼働させるのが安全でいいと思っているんだけど、Shopifyはそこを"instruction metrics"で担保してるのか...!:thinking:)

<!-- ここまで読んだ! -->

### Continuous improvement through active learning アクティブラーニングによる継続的改善:

We implemented an active learning loop that continuously identifies areas for improvement and incorporates new training data. 
私たちは、継続的に改善の余地を特定し、**新しいトレーニングデータを取り入れるアクティブラーニングループ**を実装しました。 
The active learning system operates on two fronts. 
アクティブラーニングシステムは2つの側面で機能します。

- First, LLM judges flag low-quality inferences in production, queuing them for additional human review and retraining. 
  - まず、**LLMジャッジがproductionで低品質の推論をフラグ付けし、追加の人間のレビューと再訓練のためにキューに入れます。**
- Second, we analyze the token probability distributions of model outputs. 
  - 次に、モデル出力のトークン確率分布を分析します。 
    We target samples where output token probabilities are low, signaling model uncertainty. 
    出力トークン確率が低いサンプルをターゲットにし、モデルの不確実性を示します。 
    These re-enter the training pipeline, improving robustness over time. 
    これらはトレーニングパイプラインに再投入され、時間とともに堅牢性が向上します。 
    (ステップ2は、ざっくりステップ1で選んだものの中から、さらにモデルが不確実なものを選んで再学習させる、みたいな感じ??:thinking:)

By identifying and retraining on these uncertain inferences, we systematically improve model performance across our corpus. 
これらの不確実な推論を特定し再訓練することで、私たちは体系的にコーパス全体のモデル性能を向上させます。

<!-- ここまで読んだ! -->

## VI. Scaling and deployment infrastructure スケーリングとデプロイメントインフラストラクチャ

Our inference infrastructure handles supports 40 million LLM calls daily, representing about 16 billion tokens inferred per day, through several optimization techniques:
私たちの推論インフラストラクチャは、毎日4000万回のLLMコールを処理し、1日あたり約160億トークンを推論しています。これは、いくつかの最適化技術を通じて実現されています。

- Triton inference server: Orchestrates model serving across our GPU fleet, handling request preprocessing, batching, and routing from multiple surfaces (admin UI, Shop app, APIs, bulk pipelines).
  - Triton推論サーバー：私たちのGPUファーム全体でモデルの提供を調整し、リクエストの前処理、バッチ処理、および複数のインターフェース（管理UI、Shopアプリ、API、大量パイプライン）からのルーティングを処理します。

- Dataflow streaming pipeline: Kafka-based architecture writes inferences back to all relevant data sinks in real-time.
  - データフローストリーミングパイプライン：Kafkaベースのアーキテクチャが、**リアルタイムで関連するすべてのデータシンクに推論結果を書き戻し**ます。

- FP8 quantization: Reduces GPU memory footprint while maintaining inference accuracy, enabling larger batch sizes.
  - FP8量子化：推論精度を維持しながらGPUメモリのフットプリントを削減し、より大きなバッチサイズを可能にします。

- Key value cache: Stores and reuses previously computed attention patterns.
  - キー値キャッシュ：以前に計算された注意パターンを保存し再利用します。

- Selective field prompting: Different surfaces request only required fields, reducing median latency from 2s to 500ms and GPU token usage by 40%.
  - 選択的フィールドプロンプティング：異なるインターフェースが必要なフィールドのみを要求し、中央値のレイテンシを2秒から500ミリ秒に、GPUトークンの使用量を40％削減します。

<!-- ここまで読んだ! -->

## VII. Impact and future applications 影響と今後の応用

The catalogue is actively integrated across Shopify’s ecosystem: 
カタログはShopifyのエコシステム全体に積極的に統合されています：

- Merchant admin: The system provides real-time suggestions on category classification and missing attributes during product creation, improving data quality at the point of entry. 
  - マーチャント管理：このシステムは、**商品作成時にカテゴリ分類や欠落属性に関するリアルタイムの提案を提供**し、入力時のデータ品質を向上させます。
- Search and recommendations: Enriched product data and universal identifiers enable better matching, faceting, and surfacing of relevant results. 
  - 検索と推薦：強化された商品データとユニバーサル識別子により、より良いマッチング、ファセット化、および関連結果の表示が可能になります。
- Embeddings creation: Product and variant representations, based on standardized output, inform core ML functionality for personalized ranking and recommendations. 
  - 埋め込みの作成：標準化された出力に基づく商品およびバリアントの表現は、個別のランキングと推薦のためのコアML機能に情報を提供します。

The Catalogue has already begun to unlock a powerful set of downstream benefits: 
カタログはすでに強力な一連の下流の利点を解放し始めています：

- Search: Canonicalized, enriched product metadata means semantic and keyword queries (e.g., “best local coffee in Singapore”) return diverse, high-relevance results—including long-tail gems, not just well-known brands. 
  - 検索：**標準化され、強化された製品メタデータ**は、意味的およびキーワードクエリ（例：「シンガポールの最高の地元のコーヒー」）が多様で高関連性の結果を返すことを意味します—有名ブランドだけでなく、ロングテールの宝石も含まれます。
- Personalization: The unified product catalogue enables advanced recommendation systems, using user interaction data and standardized attributes for surfacing of products, bundles, and merchants that match individual interests. 
  - パーソナライズ：**統一された商品カタログ**は、ユーザーのインタラクションデータと標準化された属性を使用して、個々の興味に合った商品、バンドル、およびマーチャントを表示する高度な推薦システムを可能にします。
- Conversational commerce: AI assistants (e.g., Shopify Sidekick, Shop app’s chat) rely on catalogue data as structured context, guiding users through dynamic, needs-based shopping workflows—mimicking the expertise of an in-store associate. 
- 会話型コマース：AIアシスタント（例：Shopify Sidekick、Shopアプリのチャット）は、構造化されたコンテキストとしてカタログデータに依存し、ユーザーを動的でニーズに基づくショッピングワークフローに導きます—店内のアソシエイトの専門知識を模倣しています。
- Multi-channel integration: Having a common schema and universal product IDs makes Shopify’s ecosystem interoperable—not just internally, but across channels, partners, and emerging marketplaces. Our open-source taxonomy and standards help ensure Shopify data can power any commerce innovation. 
  - マルチチャネル統合：共通のスキーマとユニバーサル商品IDを持つことで、Shopifyのエコシステムは相互運用可能になります—内部だけでなく、チャネル、パートナー、および新興市場全体で。私たちのオープンソースの分類法と標準は、Shopifyデータがあらゆるコマースの革新を推進できることを保証します。
  - 森田メモ:
    - マルチチャネル統合 = 異なるサービス間で同じ商品データをそのまま使いまわせる! 的な話??
    - interoperable(相互運用可能) = システム同士が自然に連携できる状態。データ整形なしでシンプルに。
    - **shopifyのopen-source taxonomy** = Shopifyがオープンソースでこの商品の分類体系を公開してるってことっぽい。これにより、他の企業も同じ分類を使えてデータがズレない。
      - 正式名称は「Shopify Product Taxonomy」らしい。
      - ポイント1: ざっくり階層構造のカテゴリになってる。
        - ex. Apparel & Accessories > Clothing > Shirts > T-Shirts
        - ツリー構造(階層)で定義されてる。
      - ポイント2: カテゴリだけじゃなくて属性(attribute)もセットで定義されている。
        - ex. T-Shirtsカテゴリには、size, color, material, genderなどの属性が定義されている。
        - カテゴリごとに「持つべき属性」が定義されているイメージ。
      - つまり何をしてるか? -> 商品データの意味を標準化してる。
      - なぜopen-sourceにしてるか?
        - 利点1: 外部も同じ分類を使える
        - 利点2: データ連携が楽になる
        - 世界中のECデータを同じ意味空間に乗せるための基盤を提供してる、みたいな感じ??:thinking:

Ongoing challenges and next steps: 
進行中の課題と次のステップ：

- Balancing scalability, accuracy, latency: Ensuring quality without sacrificing speed or cost at our scale remains a central engineering challenge. 
  - スケーラビリティ、精度、レイテンシのバランス：私たちの規模でスピードやコストを犠牲にすることなく品質を確保することは、中心的なエンジニアリングの課題です。
- Unified vs. multi-model: Today, each key entity (media, product, etc.) has a dedicated, size-optimized model. We are actively exploring consolidation into a single, multi-entity model to streamline our architecture and potentially bring similar performance gains we have observed from tackling multiple tasks simultaneously. 
  - 統一モデル対マルチモデル：現在、**各主要エンティティ（メディア、商品など）は専用のサイズ最適化モデル**を持っています。私たちは、アーキテクチャを合理化し、複数のタスクに同時に取り組むことで観察されたのと同様のパフォーマンス向上をもたらす可能性のある単一のマルチエンティティモデルへの統合を積極的に探求しています。
- Graph-based reasoning: Exploiting inter-entity relationships using LLM reasoning over graphs is a promising direction for entity resolution. 
  - グラフベースの推論：グラフ上でのLLM推論を使用してエンティティ間の関係を活用することは、エンティティ解決のための有望な方向性です。
- Continuous pipeline improvement: As data and requirements constantly evolve, active learning, dynamic retraining, and infrastructure scaling remain a perpetual focus. 
  - 継続的なパイプライン改善：データと要件が常に進化する中で、アクティブラーニング、動的再訓練、およびインフラのスケーリングは常に焦点となります。

<!-- ここまで読んだ! -->

## VIII. Conclusion 結論

Building Shopify's Global Catalogue required rethinking how we approach product understanding at scale. 
Shopifyのグローバルカタログを構築するには、スケールでの製品理解へのアプローチを再考する必要がありました。
By combining multimodal LLMs with careful system design, we've created infrastructure that makes millions of merchants’ products truly understandable by machines. 
マルチモーダルLLMと慎重なシステム設計を組み合わせることで、私たちは**何百万もの商人の製品を機械が本当に理解できるインフラ**を作り上げました。
This isn't just about better search or recommendations—it's about enabling entirely new ways of discovering and interacting with products. 
これは**単により良い検索や推薦のためだけではなく、製品を発見し、相互作用する全く新しい方法を可能にすること**です。

As commerce continues its evolution toward AI-driven experiences, the importance of structured, reliable product data only grows. 
**商取引がAI駆動の体験へと進化し続ける中で、構造化された信頼できる製品データの重要性はますます高まり**ます。
We're excited to continue pushing the boundaries of what's possible and sharing our learnings with the community. 
私たちは、可能性の限界を押し広げ続け、コミュニティと学びを共有することに興奮しています。

For more details, watch our ICLR 2025 talk or explore our open-source taxonomy. 
詳細については、私たちのICLR 2025の講演を視聴するか、オープンソースのtaxonomyを探索してください。
Interested in these challenges? Join our team and help build the future of commerce. 
これらの課題に興味がありますか？私たちのチームに参加し、商取引の未来を築く手助けをしてください。

<!-- ここまで読んだ! -->
