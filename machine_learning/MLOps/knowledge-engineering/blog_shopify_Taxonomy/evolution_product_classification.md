refs: https://shopify.engineering/evolution-product-classification?utm_source=chatgpt.com

# Evolution of Product Classification at Shopify: From Categories to Comprehensive Product Understanding Shopifyにおける製品分類の進化：カテゴリから包括的な製品理解へ

Shopify’s product classification system has evolved from basic categorization to an AI-driven framework using Vision Language Models and the Shopify Product Taxonomy. 
Shopifyの製品分類システムは、基本的なカテゴリ分けから、Vision Language ModelsとShopify Product Taxonomyを使用したAI駆動のフレームワークへと進化しました。
It accurately classifies products, extracts attributes, and processes over 30 million predictions daily, improving search, discovery, trust, and efficiency for merchants and buyers.
これは、製品を正確に分類し、属性を抽出し、毎日3000万件以上の予測を処理することで、商人と購入者のための検索、発見、信頼、効率を向上させます。

At Shopify, we help millions of businesses sell products across our platform, ranging from handcrafted jewelry to industrial equipment. 
Shopifyでは、手作りのジュエリーから産業機器まで、数百万のビジネスが私たちのプラットフォームで製品を販売するのを支援しています。
Understanding these products, including their categories, attributes, and characteristics, is crucial for providing better search, discovery, and recommendation experiences for both merchants and buyers.
**これらの製品、特にそのカテゴリ、属性、特性を理解することは、商人と購入者の両方にとって、より良い検索、発見、推奨体験を提供するために重要**です。

Our journey through product classification has evolved significantly over the years. 
私たちの製品分類の旅は、年々大きく進化しています。
What started as a basic categorization system has evolved into a system that is built on two key foundations, which we’ll introduce in this post: Vision Language Models and the Shopify Product Taxonomy.
基本的なカテゴリ分けシステムから始まったものが、この記事で紹介する2つの重要な基盤に基づいたシステムへと進化しました：Vision Language ModelsとShopify Product Taxonomyです。

<!-- ここまで読んだ! -->

## The Journey to Better Product Understanding 製品理解の向上への旅

(あ! これ気になる...!!:thinking:)

### Early Days: Basic Classification 初期の頃: 基本的な分類

Our initial approach to product classification in 2018 focused on basic categorization using traditional machine learning methods with our first model baseline being a logistic regression with TF-IDF classifier. 
私たちの**2018年の製品分類に対する初期のアプローチは、伝統的な機械学習手法を用いた基本的なカテゴリ分け**に焦点を当て、最初のモデルのベースラインはTF-IDF分類器を用いたロジスティック回帰でした。 
While effective for simple cases, this system struggled with the increasing complexity and diversity of products on our platform.
このシステムは**単純なケースには効果的でしたが、私たちのプラットフォーム上の製品の複雑さと多様性の増加に苦しみ**ました。

### The Multi-Modal Evolution マルチモーダルの進化

In 2020, we implemented a multi-modal approach combining image and text data for classification. 
2020年には、画像とテキストデータを組み合わせたマルチモーダルアプローチを実装しました。 
This multi-modal approach improved our ability to understand products, especially in cases where either text or image alone might be ambiguous. 
**このマルチモーダルアプローチは、特にテキストまたは画像のいずれかだけでは曖昧な場合に、製品を理解する能力を向上**させました。 
However, we recognized that category classification alone wasn't enough to fully understand products.
しかし、**カテゴリ分類だけでは製品を完全に理解するには不十分である**ことを認識しました。

<!-- ここまで読んだ! -->

### The Need for Comprehensive Understanding 包括的な理解の必要性

By early 2023, as our platform grew, we identified several key requirements:
2023年初頭、私たちのプラットフォームが成長するにつれて、**いくつかの重要な要件**を特定しました:
(これが)

- 1. More granular product understanding beyond just categories
  - カテゴリだけでなく、**より詳細な製品理解** (うんうん、わかる...!!:thinking:)
    - ニュースアプリでの例: 
      - 記事を単に「スポーツ」や「政治」という大枠のバケツに入れるだけでなく、その記事のテーマをより深く理解することを指す!
        - 「スポーツ」カテゴリの記事であっても、それが「試合の勝敗速報」なのか「選手の怪我の経過報告」なのか「球団の経営・ビジネス問題」なのかまで解像度を上げて内容を把握するイメージ...!!
        - 「政治」カテゴリの記事であっても、それが「選挙の情勢分析や当落速報」なのか「新しい法案の解説や国会での審議状況」なのか「政治資金問題などの不祥事の追求」なのか「他国との外交や首脳会談の成果」なのかまで解像度をあげて内容を把握するイメージ...!!
- 2. Consistent taxonomy across the platform
  - **プラットフォーム全体での一貫した分類体系** (うんうん、これもわかる...!!:thinking:)
    - ニュースアプリでの例:
      - アプリ内の「トップ画面のタブ」「検索機能」「ユーザ別のおすすめフィード」「プッシュ通知設定」などの全ての領域で、共通のカテゴリ基準やタグ付けのルールが適用されてる状態。
      - ある画面では「IT」という分類なのに、別の画面では「テクノロジー」という異なる基準で記事が整理されているような、システムごとの不一致による混乱を防ぐ目的...!!
- 3. Ability to extract meaningful product attributes depending on category.
  - **カテゴリに応じて意味のある製品属性を抽出する能力** (なるほど、ニュース記事の場合はどうだろ?? カテゴリに応じて付与すべき属性って変わるだろうか?? このカテゴリについては、"具体的なニュースストーリー"というattributeを付与すべき、みたいな感じかな?? インタビュー系のコンテンツだったらインタビュアーやインタビュー対象者、番組だったら出演者とかかな...!:thinking:)
- 4. Need for more metadata, including things like simplified product descriptions, content tags, and product characteristics
  - より多くのメタデータの必要性。これには、**簡略化された製品説明、コンテンツタグ、製品の性質など**が含まれる。
  - ニュースアプリでの例:
    - 記事本文のテキスト情報だけでなく、システムが扱いやすく、ユーザにとっても便利な追加データ(メタデータ)を豊富に生成すること。
    - 長文の記事から「3行の簡略化された要約」を自動生成したり、「#速報」「#独占インタビュー」「#図解あり」といったコンテンツタグや記事の特徴を付与したりして、多様な画面表示や検索体験の向上に役立てるイメージ...!:thinking:
- 5. Content safety and trust features
  - コンテンツの安全性と信頼性の機能。
  - ニュースアプリでの例:
    - ユーザに有害な情報や不適切なコンテンツを届けないための機能。
    - 具体的には、フェイクニュースの疑いがある情報の検知、過度な暴力・差別表現が含まれる記事の自動フィルタリング、あるいは閲覧注意の画像が含まれる場合は「センシティブなコンテンツ」という警告ラベルを貼るなど。**プラットフォームの品質と信頼を守るための監視・制御機能**を指す。

The emergence of Vision Language Models presented the perfect opportunity to address these needs comprehensively.
Vision Language Modelsの出現は、これらのニーズに包括的に対処する絶好の機会を提供しました。

<!-- ここまで読んだ! -->

### Current Generation 現在の世代

Our current product understanding system is built on two key foundations: Shopify's Standard Product Taxonomy and Vision Language Models.
私たちの現在の製品理解システムは、**2つの主要な基盤**に基づいています: Shopifyの標準製品分類法(Shopify's Standard Product Taxonomy)とVision Language Modelsです。

The Shopify Product Taxonomy is a comprehensive library of product data spanning more than 26 business verticals, mapping over 10,000 product categories with over 1,000 associated product attributes.
Shopify製品分類法は、26以上のビジネス分野にわたる製品データの包括的なライブラリで、**10,000以上の製品カテゴリと1,000以上の関連製品属性をマッピング**しています。
It offers:
それは以下を提供します:

- Hierarchical Classification: Products are mapped to specific categories within a detailed hierarchy (e.g., Furniture > Chairs > Kitchen & Dining Room Chairs).
  - **階層的分類**: 製品は詳細な階層内の特定のカテゴリにマッピングされます (例: 家具 > 椅子 > キッチンとダイニングルームの椅子)。
- Category-Specific Attributes: Each category has its own set of relevant attributes, ensuring comprehensive product description.
  - **カテゴリ固有の属性**: 各カテゴリには関連する属性のセットがあり、包括的な製品説明を保証します。
  - (たぶんだけど、カテゴリ固有の属性もあれば、すべてのカテゴリで紐づけるべき属性もありそうだよね...!:thinking:)
- Standardized Values: Pre-defined attribute values help maintain consistency while allowing customization.
  - 標準化された値: 事前定義された属性値は、一貫性を維持しつつカスタマイズを可能にします。
  - これどういう話??:thinking:
    - 一貫性を保つ(maintain consistency) = 
      - 「表記ゆれ」を防ぐために、属性値の集合をあらかじめ定義しておくこと。例えば、同じ国に関する記事でも「アメリカ「米国」「USA」というバラバラな属性が抽出されると、「アメリカのニュース」として一覧化・検索できなくて困る。
      - 「アメリカ合衆国」という標準値(standardized value)を事前定義しておくことで、システム全体で一貫して正確な属性が抽出されるようにするイメージ...!!
    - カスタマイズ可能にする(allowing customization) = 
      - **すべての属性値をガチガチの標準値だけに絞ってしまうと、今度はそのアイテムならではの特殊な情報を表現できなくなってしまうかも**!
      - 基本的には標準化された一貫性のある値を使用しつつも、そのアイテム特有の情報(キーワードなど)は、**カスタム属性**として柔軟に付与できるようにしてるっぽい...??
- Cross-Channel Compatibility: The taxonomy aligns with other platforms' classification systems through cross walks that we provide, facilitating multi-channel selling.
  - クロスチャネル互換性: この分類法は、私たちが提供するクロスウォークを通じて他のプラットフォームの分類システムと整合し、マルチチャネル販売を促進します。

Vision Language Models complement this taxonomy by providing several breakthrough capabilities:
Vision Language Modelsは、**いくつかの画期的な機能を提供することでこの分類法を補完**します:

- True Multi-Modal Understanding: Unlike previous systems that processed images and text separately, Vision Language Models can understand the intricate relationships between visual and textual product information.
  - 真のマルチモーダル理解: 画像とテキストを別々に処理していた以前のシステムとは異なり、Vision Language Modelsは視覚的およびテキスト的な製品情報の複雑な関係を理解できます。
- Zero-Shot Learning: In addition, they can understand and classify products they've never seen before by leveraging their broad knowledge.
  - ゼロショット学習: さらに、彼らは広範な知識を活用して、これまで見たことのない製品を理解し、分類することができます。
- Natural Language Reasoning: These models can process and generate human-like descriptions, enabling them to extract rich metadata from complex product listings.
  - 自然言語推論: これらのモデルは人間のような説明を処理し生成することができ、複雑な製品リストから豊富なメタデータを抽出することを可能にします。
- Contextual Understanding: They also excel at understanding products in context, considering not just what an item is, but also its intended use, style, and characteristics.
  - 文脈理解: 彼らはまた、製品が何であるかだけでなく、その意図された使用法、スタイル、特性を考慮して、文脈で製品を理解するのに優れています。

Together, these technologies enable us to automatically classify products within our taxonomy while extracting relevant attributes and generating consistent product descriptions.
**これらの技術を組み合わせることで、私たちは分類法(taxonomy)内で製品を自動的に分類し、関連する属性を抽出し、一貫した製品説明を生成する**ことができます。

<!-- ここまで読んだ! -->

## Technical Deep Dive: Our System Architecture 技術的深堀：私たちのシステムアーキテクチャ

### Model Evolution and Optimization モデルの進化と最適化

Our journey with Vision Language Models reflects our commitment to continuous learning. 
私たちのVision Language Modelsとの旅は、継続的な学習への私たちのコミットメントを反映しています。
Each model transition - from LlaVA 1.5 7B to LLaMA 3.2 11B, and now to Qwen2VL 7B - has brought significant improvements in prediction quality while maintaining operational efficiency. 
各モデルの移行（LlaVA 1.5 7BからLLaMA 3.2 11B、そして現在のQwen2VL 7Bへの移行）は、**運用効率を維持しながら予測品質において重要な改善**をもたらしました。
We carefully evaluate each new model against our existing pipeline, considering both performance metrics and computational costs. 
私たちは、パフォーマンス指標と計算コストの両方を考慮しながら、**既存のパイプラインに対して各新モデルを慎重に評価**します。

<!-- ここまで読んだ! ここ気になるんだよな。継続的改善のしやすいシステムをどうやって作ってるか...!!:thinking: -->

### Technical Deep Dive: Inference Optimization 技術的深堀：推論の最適化

Our inference stack employs several key optimization techniques: 
私たちの推論スタックは、いくつかの重要な最適化技術を採用しています。

#### FP8 Quantization FP8量子化

We've implemented FP8 quantization for our current Qwen2VL model, which provides three key benefits: 
私たちは現在のQwen2VLモデルにFP8量子化を実装しており、これにより3つの主要な利点があります。

- Reduced GPU memory footprint, allowing for more efficient resource utilization. 
  - GPUメモリのフットプリントが削減され、より効率的なリソース利用が可能になります。
- Minimal impact on prediction accuracy, maintaining high-quality results. 
  - 予測精度への影響が最小限であり、高品質な結果を維持します。
- Enables more efficient in-flight batch processing due to the smaller model size. 
  - モデルサイズが小さいため、より効率的なインフライトバッチ処理が可能になります。

<!-- ここまで読んだ! -->

#### In-Flight Batching インフライトバッチ処理

Our system uses an approach through Nvidia Dynamo that improves throughput: 
私たちのシステムは、Nvidia Dynamoを通じてスループットを改善するアプローチを使用しています。

- Dynamic Request Handling: Instead of pre-defining fixed batch sizes, our system dynamically groups incoming product requests based on real-time arrival patterns. 
  - 動的リクエスト処理：固定バッチサイズを事前に定義するのではなく、システムはリアルタイムの到着パターンに基づいて、到着する製品リクエストを動的にグループ化します。
- Adaptive Processing: The system adjusts batch composition on the fly, preventing resource underutilization. 
  - 適応処理：システムはバッチの構成を即座に調整し、リソースの過少利用を防ぎます。
- Efficient Resource Usage: By processing products as they arrive, we minimize GPU idle time and maximize throughput. 
  - 効率的なリソース使用：製品が到着するたびに処理することで、GPUのアイドル時間を最小限に抑え、スループットを最大化します。

When processing product updates, our system improves efficiency by: 
製品の更新を処理する際、私たちのシステムは効率を向上させます。

- Starting to process a batch as soon as new products arrive, rather than waiting for a fixed batch size. 
  - **固定バッチサイズを待つのではなく、新しい製品が到着次第、バッチの処理を開始**します。
- Accepting additional products during this processing time and immediately forming new batches with incoming items. 
  - この処理時間中に追加の製品を受け入れ、到着するアイテムで新しいバッチを即座に形成します。
- Maximizing GPU utilization by minimizing idle times and adaptively managing workload fluctuations to optimize both latency and throughput. 
  - アイドル時間を最小限に抑え、レイテンシとスループットの両方を最適化するために、ワークロードの変動を適応的に管理することで、GPUの利用率を最大化します。

<!-- ここまで読んだ! -->

#### KV Cache Optimization KVキャッシュ最適化

We've implemented a Key-Value (KV) cache system that significantly improves our LLM inference speed: 
私たちは、**LLMの推論速度を大幅に改善するKey-Value（KV）キャッシュシステムを実装**しました。

- Memory Management: The system stores and reuses previously computed attention patterns. 
  - メモリ管理：システムは以前に計算された注意パターンを保存し再利用します。
- Token Generation Efficiency: Particularly effective for our two-stage prediction process, where we generate both categories and attributes. 
  - トークン生成の効率：特に、カテゴリと属性の両方を生成する二段階の予測プロセスにおいて効果的です。

<!-- ここまで読んだ! -->

### Pipeline Architecture パイプラインアーキテクチャ

Our near real-time processing pipeline incorporates these optimizations while maintaining robust error handling and consistency: 
私たちの**near real-time(ほぼリアルタイム)処理パイプライン**は、これらの最適化を取り入れつつ、堅牢なエラーハンドリングと一貫性を維持しています。

![]()

The diagram shows our production architecture where a Dataflow pipeline orchestrates the end-to-end process, making two separate calls to our Vision LM service for category and attribute predictions. 
図は、データフローパイプラインがエンドツーエンドのプロセスを調整し、**カテゴリと属性の予測のためにVision LMサービスに2回の別々の呼び出しを行う**productionアーキテクチャを示しています。(両者は直列。この理由は、2回目のattribute prediction呼び出しが、1回目のcategory prediction呼び出しの出力に依存しているから...!:thinking:)
The prompt of the second call is dependent on the output of the first call, as the attributes we predict for a product depend on the category of the product. 
2回目の呼び出しのプロンプトは、1回目の呼び出しの出力に依存しており、製品の属性は製品のカテゴリに依存します。(あ、上で思ったことがまさに一文下に書いてあった笑...!:thinking:)
The service runs on a Kubernetes cluster with NVIDIA GPUs, using Dynamo for model serving. 
このサービスは、NVIDIA GPUを使用したKubernetesクラスター上で実行され、モデルサービングにはDynamoを使用しています。

1. Input Processing 入力処理
    - Dynamic request batching based on arrival patterns 到着パターンに基づく動的リクエストバッチ処理
    - Preliminary validation of product data 製品データの初期検証
    - Resource allocation based on current system load 現在のシステム負荷に基づくリソース割り当て
2. Two-Stage Prediction 二段階予測
    - Category prediction with simplified description generation 簡略化された説明生成によるカテゴリ予測
      - (**カテゴリ予測の際に、同時に「人間が読んでわかりやすい、短く整理された商品説明文」も生成させてるっぽい...??**:thinking:)
      - なんで...?? コスト効率とか処理スピードの観点だろうか??:thinking: もしくは同時に推論させた方が精度が上がるから??:thinking:
    - Attribute prediction using category context **カテゴリコンテキストを使用した属性予測**
    - Both stages leverage optimized inference 両方のステージは最適化された推論を活用します
3. Consistency Management 一貫性管理
    - Transaction-like handling of predictions 予測のトランザクションのような処理
    - **Both category and attribute predictions must succeed カテゴリと属性の予測は両方とも成功しなければなりません**
    - Automatic retry mechanism for partial failures 部分的な失敗に対する自動再試行メカニズム
    - Monitoring and alerting for prediction quality 予測品質の監視とアラート
4. Output Processing 出力処理
    - Validation against taxonomy rules タクソノミールールに対する検証
    - Result formatting and storage 結果のフォーマットと保存
    - Notification system for completed predictions 完了した予測の通知システム

<!-- ここまで読んだ! -->

### Building Robust Training Data ロバストなトレーニングデータの構築

(ここは、OSSのLLMを自社でfine-tuningしてhostingしてる企業ゆえの工夫の話...!:thinking:)

Training data quality directly influences system reliability, so we developed a multi-stage annotation system to ensure consistency and high standards. 
トレーニングデータの品質はシステムの信頼性に直接影響を与えるため、一貫性と高い基準を確保するためにマルチステージのアノテーションシステムを開発しました。
At the core is our multi-LLM annotation system, where several large language models independently evaluate each product. 
その中心には、複数の大規模言語モデルが各製品を独立して評価する**マルチLLMアノテーションシステム**があります。
Each model contributes unique strengths, and structured prompting is used to maintain annotation quality. 
各モデルは独自の強みを持ち、構造化されたプロンプトを使用してアノテーションの品質を維持します。
Products thus receive multiple, independent annotations, maximizing coverage and robustness. 
そのため、製品は複数の独立したアノテーションを受け取り、カバレッジとロバスト性を最大化します。
When annotations disagree, a dedicated arbitration system comes into play, employing specialized models that act as impartial judges to resolve conflicts. 
アノテーションが一致しない場合、専用の仲裁システムが機能し、対立を解決するために中立的な判断を行う専門モデルを使用します。
This system enforces careful ruling logic to address edge cases, ensuring that all annotations remain aligned with our taxonomy standards and are consistent across millions of products. 
このシステムは、エッジケースに対処するために慎重なルールロジックを強制し、すべてのアノテーションが私たちのタクソノミー基準に沿っており、数百万の製品にわたって一貫性を保つことを保証します。

To further reinforce quality, we incorporate a human validation layer focused on strategic manual review of complex edge cases and novel product types. 
品質をさらに強化するために、複雑なエッジケースや新しい製品タイプの戦略的手動レビューに焦点を当てた人間の検証レイヤーを組み込みます。
This introduces a continuous feedback loop for ongoing improvement and adaptability. 
これにより、継続的な改善と適応のためのフィードバックループが導入されます。
Regular quality audits are conducted as part of this process, guaranteeing that our annotation standards remain high and our training data remains both reliable and representative. 
このプロセスの一環として定期的な品質監査が行われ、アノテーション基準が高く保たれ、トレーニングデータが信頼性が高く、代表的であることが保証されます。

<!-- ここまで読んだ! -->

## Impact and Results 影響と結果

The integration of Vision LMs with our structured taxonomy has delivered substantial improvements for both merchants and buyers across several key dimensions. 
Vision LMsと私たちの構造化された分類法の統合は、商人と購入者の両方において、いくつかの重要な次元で大幅な改善をもたらしました。
For merchants, our metrics reveal an impressive 85% acceptance rate of predicted categories, reflecting high trust in the system’s accuracy. 
商人にとって、**私たちの指標は予測されたカテゴリの受け入れ率が85%という印象的な数字であることを示しており、システムの精度に対する高い信頼を反映**しています。
This has led to enhanced product discoverability and more consistent organization within merchant catalogs. 
これにより、製品の発見性が向上し、商人のカタログ内での一貫した整理が実現しました。
Accurate categorization also drives better search relevance, facilitates precise tax calculations, and streamlines product management by automating attribute tagging and reducing manual effort. 
正確なカテゴリ分けは、検索の関連性を向上させ、正確な税計算を促進し、属性タグ付けの自動化と手作業の削減によって製品管理を効率化します。

Buyers, in turn, benefit from more accurate search results, highly relevant product recommendations, and a consistently organized browsing experience. 
購入者は、**より正確な検索結果、高い関連性を持つ製品推薦、そして一貫して整理されたブラウジング体験の恩恵**を受けます。
The use of structured attributes clarifies product information, empowering customers to make more informed decisions. 
構造化された属性の使用は製品情報を明確にし、**顧客がより情報に基づいた意思決定を行えるように**します。

At the platform level, these advancements have enabled the processing of over 30 million predictions daily, while hierarchical precision and recall have doubled compared to our earlier neural network approach. 
プラットフォームレベルでは、これらの進展により、毎日3000万件以上の予測を処理できるようになり、階層的な精度と再現率は以前のニューラルネットワークアプローチと比較して2倍になりました。
Our structured attribute system now spans all product categories, fostering more effective automated content screening and ultimately enhancing overall trust and safety on the platform. 
私たちの構造化された属性システムは現在、すべての製品カテゴリにわたり、より効果的な自動コンテンツスクリーニングを促進し、最終的にはプラットフォーム全体の信頼性と安全性を向上させています。

<!-- ここまで読んだ! -->

## Future Directions 将来の方向性

While our current system is already delivering meaningful improvements for merchants, we are committed to its continuous evolution and have identified several avenues for future development. 
現在のシステムはすでに商人にとって意義のある改善を提供していますが、私たちはその継続的な進化にコミットしており、将来の開発のためのいくつかの道筋を特定しました。

On the technical front, we aim to incorporate new Vision LM architectures as they become available, expand attribute prediction to encompass more specialized product categories, and improve the system’s ability to handle multi-lingual product descriptions. 
技術的な面では、新しいVision LMアーキテクチャが利用可能になるにつれてそれを取り入れ、属性予測をより専門的な製品カテゴリに拡張し、システムの多言語製品説明を処理する能力を向上させることを目指しています。
Additionally, we plan to further optimize our inference pipelines to achieve even greater throughput. 
さらに、私たちは推論パイプラインをさらに最適化し、より高いスループットを達成する計画です。

At the platform level, a major upcoming enhancement is the migration from our current tree-based taxonomy to a Directed Acyclic Graph (DAG) structure. 
プラットフォームレベルでは、今後の主要な強化は、**現在の木構造の分類法から有向非巡回グラフ（DAG）構造への移行**です。
This shift will allow for multiple valid categorization paths per product, supporting more flexible relationships and accommodating cross-category products more effectively. 
この移行により、製品ごとに複数の有効な分類パスが可能になり、より柔軟な関係をサポートし、カテゴリを超えた製品をより効果的に扱うことができます。

We also intend to enhance metadata extraction for finer-grained details such as product measurements, specifications, material composition, and design elements, as well as broaden attribute coverage across all branches of the taxonomy. 
私たちはまた、製品の測定、仕様、材料構成、デザイン要素などのより詳細な情報のメタデータ抽出を強化し、**分類法のすべての枝にわたる属性のカバレッジを広げること**を意図しています。
(はいはい、属性の追加がしやすいシステムであることが重要だよなぁ〜...!!:thinking:)

These developments will ensure our system remains at the forefront of accuracy and adaptability. 
これらの開発により、私たちのシステムは精度と適応性の最前線に留まり続けることが保証されます。

<!-- ここまで読んだ! -->

## Conclusion 結論

The evolution of Shopify's product understanding system represents a significant leap forward in how we help merchants succeed through better search relevance, better tax calculations, better analytics and many other features built on top of this system. 
**Shopifyの製品理解システムの進化**は、より良い検索関連性、より良い税計算、より良い分析、そしてこのシステムの上に構築された多くの他の機能を通じて、商人が成功するのを助ける方法において重要な前進を示しています。
By combining cutting-edge Vision Language Models with our structured taxonomy, we've created a system that not only understands products better but also delivers practical benefits across our entire platform. 
最先端のVision Language Modelsと私たちの構造化された分類法を組み合わせることで、私たちは製品をよりよく理解するだけでなく、**私たちの全プラットフォームにわたって実用的な利点を提供するシステム**を作成しました。

Our approach demonstrates a novel application of Vision Language Models beyond their typical use cases. 
私たちのアプローチは、Vision Language Modelsの典型的な使用ケースを超えた新しい応用を示しています。
We've pushed these models beyond basic image classification tasks to complex product understanding at scale. 
私たちは、これらのモデルを**基本的な画像分類タスクを超えて、大規模な複雑な製品理解へ**と押し進めました。
Our system now processes millions of products daily, extracting detailed metadata, ensuring accurate categorization, and enabling everything from improved search relevance to precise tax calculations. 
私たちのシステムは現在、毎日数百万の製品を処理し、詳細なメタデータを抽出し、正確な分類を保証し、改善された検索関連性から正確な税計算まで、すべてを可能にしています。

The success of our system in handling such a massive scale, with 30 million daily predictions and billions of historical products, shows how Vision Language Models can be effectively optimized and deployed to handle large-scale production workloads. 
毎日3000万の予測と数十億の歴史的製品を処理するというこのような大規模なシステムの成功は、Vision Language Modelsが大規模な生産ワークロードを処理するために効果的に最適化され、展開できる方法を示しています。

As we look ahead, we remain committed to pushing the boundaries of what's possible in product understanding. 
私たちは前を見据え、製品理解における可能性の限界を押し広げることに引き続きコミットしています。
With continued advances in AI technology and our deep understanding of merchant needs, we’re empowering merchants and delivering net new capabilities to the Shopify ecosystem. 
AI技術の継続的な進歩と商人のニーズに対する深い理解をもって、私たちは商人を支援し、Shopifyエコシステムに新たな能力を提供しています。

<!-- ここまで読んだ! -->
