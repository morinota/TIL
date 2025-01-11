# Serverless Retrieval Augmented Generation (RAG) on AWS AWSにおけるサーバーレスリトリーバル拡張生成（RAG）

このコンテンツはいかがでしたか?
In the evolving landscape of generative AI,
この進化する生成AIの領域において、
integrating external, up-to-date information into large language models
(LLMs) presents a significant advancement.
外部の最新情報を大規模言語モデル（LLMs）に統合することは、重要な進展を示しています。
In this post, we’re going to
この投稿では、
build up to a truly serverless Retrieval Augmented Generation (RAG) solution,
真のサーバーレスリトリーバル拡張生成（RAG）ソリューションを構築することを目指します。
facilitating the creation of applications that produce
より正確で文脈に関連した応答を生成するアプリケーションの作成を促進します。
Our goal is to help
私たちの目標は、
you create your GenAI powered application as fast as possible,
あなたがGenAIを活用したアプリケーションをできるだけ早く作成できるようにすることです、
keeping an eye on your costs,
コストに注意を払い、
and making sure you don’t pay for compute you’re not using.
使用していない計算リソースに対して支払わないようにすることです。

### Serverless RAG: an overview サーバーレスRAGの概要

Serverless RAG combines the advanced language processing capabilities of foundational models with the agility and cost-effectiveness of serverless architecture.
サーバーレスRAGは、基盤モデルの高度な言語処理能力とサーバーレスアーキテクチャの機敏さおよびコスト効率を組み合わせています。

This integration allows for the dynamic retrieval of information from external sources—be it databases, the internet, or custom knowledge bases—enabling the generation of content that is not only accurate and contextually rich but also up-to-date with the latest information.
この統合により、データベース、インターネット、またはカスタム知識ベースなどの外部ソースからの情報を動的に取得できるようになり、正確で文脈に富んだ、最新の情報に基づいたコンテンツの生成が可能になります。

Amazon Bedrock simplifies the deployment of serverless RAG applications, offering developers the tools to create, manage, and scale their GenAI projects without the need for extensive infrastructure management.
Amazon Bedrockは、サーバーレスRAGアプリケーションの展開を簡素化し、開発者が広範なインフラ管理を必要とせずにGenAIプロジェクトを作成、管理、スケールするためのツールを提供します。

In addition to that, developers can harness the power of AWS services like Lambda and S3, alongside innovative open-source vector databases such as LanceDB, to build responsive and cost-effective AI-driven solutions.
さらに、開発者は、LambdaやS3などのAWSサービスの力を活用し、LanceDBのような革新的なオープンソースベクターデータベースと組み合わせて、応答性が高くコスト効率の良いAI駆動のソリューションを構築できます。

### Ingesting documents ドキュメントの取り込み

The journey to your serverless RAG solution involves several key steps, each tailored to ensure the seamless integration of foundational models with external knowledge.
サーバーレスRAGソリューションへの旅は、基盤モデルと外部知識のシームレスな統合を確保するために調整された、いくつかの重要なステップを含みます。

The process starts with the ingestion of documents into a serverless architecture, where event-driven mechanisms trigger the extraction and processing of textual content to generate embeddings.
このプロセスは、ドキュメントをサーバーレスアーキテクチャに取り込むことから始まり、イベント駆動型メカニズムがテキストコンテンツの抽出と処理をトリガーして埋め込みを生成します。

These embeddings, created using models like Amazon Titan, transform the content into numerical vectors that machines can easily understand and process.
これらの埋め込みは、Amazon Titanのようなモデルを使用して作成され、コンテンツを機械が簡単に理解し処理できる数値ベクトルに変換します。

Storing these vectors in LanceDB, a serverless vector database backed by Amazon S3, facilitates efficient retrieval and management, ensuring that only relevant information is used to augment the LLM's responses.
**これらのベクトルをAmazon S3にバックアップされたサーバーレスベクトルデータベースであるLanceDBに保存する**ことで、効率的な取得と管理が可能になり、LLMの応答を補強するために関連情報のみが使用されることが保証されます。

This approach not only enhances the accuracy and relevance of generated content but also significantly reduces operational costs by leveraging a pay-for-what-you-use model.
このアプローチは、生成されたコンテンツの精度と関連性を向上させるだけでなく、**pay-for-what-you-use(使用した分だけ支払う)モデル**を活用することで、運用コストを大幅に削減します。
(なるほど、こういう言い方するんだ...!:thinking:)

Have a look at the code here.
ここにコードを見てください。

<!-- ここまで読んだ! -->

### What are embeddings? 埋め込みとは何ですか？

In the realm of Natural Language Processing (NLP), embeddings are a pivotal concept that enable the translation of textual information into numerical form that machines can understand and process.
自然言語処理（NLP）の領域において、埋め込みは、テキスト情報を機械が理解し処理できる数値形式に変換することを可能にする重要な概念です。

It’s a way to translate semantic relationships into geometric relationships, something that computers can understand way better than human language.
これは、意味的関係を幾何学的関係に変換する方法であり、コンピュータは人間の言語よりもはるかに理解しやすいものです。

Essentially, through embedding, we’ll transform the content of a document into vectors in a high dimensional space.
本質的に、埋め込みを通じて、私たちは文書の内容を高次元空間のベクトルに変換します。

This way, geometric distance in this space assumes a semantic meaning.
このようにして、この空間における幾何学的距離は意味的な意味を持つようになります。

In this space, vectors representing different concepts will be far from each other, and similar concepts will be grouped together.
この空間では、異なる概念を表すベクトルは互いに遠く離れ、類似の概念は一緒にグループ化されます。

This is achieved through models like Amazon Titan Embedding which employs neural networks trained on massive corpora of text to calculate the likelihood of groups of words to appear together in various contexts.
これは、Amazon Titan Embeddingのようなモデルを通じて実現され、膨大なテキストコーパスで訓練されたニューラルネットワークを使用して、さまざまな文脈で単語のグループが一緒に出現する可能性を計算します。

Luckily you don’t have to build this system from scratch.
幸運なことに、このシステムをゼロから構築する必要はありません。

Bedrock is there to provide access to embedding models, as well as to other foundational models.
Bedrockは、埋め込みモデルや他の基盤モデルへのアクセスを提供するために存在します。

### I’ve embedded my knowledge base, now what? 知識ベースを埋め込んだが、次は何をすべきか？

You need to store them somewhere! A vector database, to be precise.
それらをどこかに保存する必要があります！正確には、ベクトルデータベースです。

And this is where the truly serverless magic happens.
そして、ここで本当にサーバーレスの魔法が起こります。

LanceDB is an open-source vector database designed for vector-search with persistent storage, simplifying retrieval, filtering, and management of embeddings.
**LanceDBは、永続的なストレージを持つベクトル検索用に設計されたオープンソースのベクトルデータベースで、埋め込みの取得、フィルタリング、および管理を簡素化**します。

The standout feature for us was the ability to connect LanceDB directly to S3.
私たちにとっての際立った特徴は、**LanceDBを直接S3に接続できる**能力でした。

This way we don’t need idle computing.
この方法により、アイドル状態のコンピューティングが不要になります。

We’ll use the database only while the lambda function is running.
私たちは、Lambda関数が実行されている間だけデータベースを使用します。

Our load tests have shown that we can ingest documents up to 500MB in size without LanceDB, Bedrock, or Lambda breaking a sweat.
私たちの負荷テストでは、LanceDB、Bedrock、またはLambdaが苦労することなく、最大500MBのサイズのドキュメントを取り込むことができることが示されています。

A known limitation of this system are Lambda cold starts, but we have measured that the process that takes the majority of time is actually the calculation of embeddings, which happens outside of Lambda.
**このシステムの既知の制限は、Lambdaのコールドスタート**ですが、実際に時間の大部分を要するプロセスは、Lambdaの外で行われる埋め込みの計算であることを測定しました。

We have measured that our userbase is affected by cold start only in 10% of the cases.
私たちは、**ユーザベースがコールドスタートの影響を受けるのは、実際には10%のケースのみ**であることを測定しました。

To mitigate this, you can think of creating batch jobs in a next phase of an MVP and potentially make use of other serverless AWS services such as Batch or ECS Fargate, taking advantage of Spot pricing too to save even further.
これを軽減するために、MVPの次のフェーズでバッチジョブを作成し、BatchやECS Fargateなどの他のサーバーレスAWSサービスを利用し、さらにコストを削減するためにスポット価格を活用することを考えることができます。
(全部Lambdaでやらなくていいよね、ってことか:thinking:)

<!-- ここまで読んだ! -->

### Querying クエリ

Users can forward their input to our Inference function via Lambda URL.
ユーザーは、**Lambda URLを介して私たちの推論関数に入力を転送**できます。
(AWS API Gatewayは使う必要あると思ってたけど、Lambda URLっていうのだけでいける...??:thinking:)

This is fed into Titan Embedding model via Bedrock, which calculates a vector.
これは、Bedrockを介してTitan Embeddingモデルに供給され、ベクトルが計算されます。

We then use this vector to source a handful of similar documents in our vector databases, and we add them to the final prompt.
次に、このベクトルを使用して、私たちのベクトルデータベースからいくつかの類似文書を取得し、それらを最終プロンプトに追加します。

We send the final prompt to the LLM the user chose and, if it supports streaming, the response is streamed back in real time to the user.
最終プロンプトをユーザーが選択したLLMに送信し、ストリーミングをサポートしている場合、応答はリアルタイムでユーザーにストリーミングされます。

Again we do not have long-running idle computation here, and because the user input is usually smaller than the documents we ingest, you can expect shorter times for the calculation of its embedding.
ここでは長時間アイドル状態の計算はなく、ユーザーの入力は通常、取り込む文書よりも小さいため、その埋め込みの計算にかかる時間は短くなることが期待できます。

A known limitation of this inference system is cold-starting-up our vector database within a new Lambda function.
**この推論システムの既知の制限は、新しいLambda関数内でのベクトルデータベースのコールドスタート**です。

Since LanceDB references a database stored in S3, when a new Lambda execution environment is created - we have to load in the database to be able to make our vector searches.
**LanceDBはS3に保存されたデータベースを参照するため、新しいLambda実行環境が作成されると、ベクトル検索を行うためにデータベースをロードする必要があります**。
(S3のデータをメモリにloadするI/Oが発生??:thinking:)

This only happens when you’re scaling up or nobody has asked a question in awhile, which means it’s a rather small trade-off for the cost-savings of a fully serverless architecture.
これは、スケールアップしているときや、しばらく誰も質問していないときにのみ発生します。つまり、完全なサーバーレスアーキテクチャのコスト削減のための非常に小さなトレードオフです。

Have a look at the code here.
こちらのコードを見てください。

<!-- ここまで読んだ! -->

## Navigating the Economics of Serverless RAG サーバーレスRAGの経済学を探る

Understanding the cost implications is crucial for adopting serverless RAG.
コストの影響を理解することは、サーバーレスRAGを採用する上で重要です。

Amazon Bedrock's pricing model, based on token usage and serverless resource consumption, allows developers to estimate costs accurately.
トークン使用量とサーバーレスリソース消費に基づくAmazon Bedrockの価格モデルは、開発者がコストを正確に見積もることを可能にします。

Whether processing documents for embedding or querying the model for responses, the pay-as-you-go pricing ensures that costs are directly tied to usage,
ドキュメントを埋め込むために処理する場合でも、モデルに対して応答を照会する場合でも、従量課金制の価格設定により、コストが使用量に直接結びつくことが保証されます。

so that you pay only for what you use.
そのため、使用した分だけを支払うことになります。

### Ingestion Economics 取り込みの経済学

Let’s dive a bit deeper into the economics of using serverless architectures for document processing.
サーバーレスアーキテクチャを使用した文書処理の経済学について、もう少し深く掘り下げてみましょう。
We base our calculations on a couple of assumptions: processing time is roughly estimated at 1 minute per megabyte of data, and a document of this size typically contains just under 30,000 tokens.
私たちは、いくつかの仮定に基づいて計算を行います：処理時間はデータの1メガバイトあたり約1分と推定され、このサイズの文書には通常30,000トークン未満が含まれています。
While these figures provide a baseline, the reality is often more favorable, with many documents being processed significantly quicker.
これらの数値は基準を提供しますが、実際には多くの文書が大幅に早く処理されるため、より好ましいことがよくあります。

Processing a single 1MB document incurs a minimal expense, less than half a cent in most cases.
1MBの文書を1つ処理する際の費用は最小限であり、ほとんどの場合、半セント未満です。
When scaling up to a thousand documents, each 1MB in size, the total cost remains remarkably low, under $4.
1MBのサイズの文書を1000件にスケールアップすると、総コストは驚くほど低く、4ドル未満のままです。
This example not only demonstrates the cost-effectiveness of serverless architectures for document processing but also highlights the efficiency of the token-based pricing model used in platforms like Amazon Bedrock.
この例は、文書処理におけるサーバーレスアーキテクチャのコスト効率を示すだけでなく、Amazon Bedrockのようなプラットフォームで使用されるトークンベースの価格モデルの効率性も強調しています。
This is also a one-off process: once you have processed your documents, they’ll live in your vector database until you decide to delete them.
これは一度限りのプロセスでもあります：文書を処理すると、それらは削除することを決定するまでベクトルデータベースに保存されます。

<!-- ここまで読んだ! -->

### Querying Economics クエリの経済学

Switching gears to the interactive part of our setup, let's talk about what happens when you actually start asking your AI some questions.
私たちのセットアップのインタラクティブな部分に切り替え、実際にAIに質問をし始めたときに何が起こるかについて話しましょう。

Here are a few of our assumptions: we're thinking it'll take about 20 seconds for AWS Lambda to embed our prompt get back to you with an answer, and we're assuming each question and its answer to be about 1000 tokens each.
いくつかの仮定があります：AWS Lambdaがプロンプトを埋め込み、回答を返すのに約20秒かかると考えており、各質問とその回答はそれぞれ約1000トークンであると仮定しています。

Compared to the inference cost, the charges associated with requests to S3 are negligible.
**推論コストと比較すると、S3へのリクエストに関連する料金は無視できるほど**です。

With assumptions out of the way, let's dive into the costs.
仮定が終わったところで、コストについて詳しく見ていきましょう。

Firing off a single query to the Claude V2 model by Anthropic is going to cost about 3 cents.
AnthropicのClaude V2モデルに対して単一のクエリを送信するのに約3セントかかります。

If you opt for something a bit lighter, like Claude Instant, the cost drops dramatically to just a fraction of a cent per query.
Claude Instantのようなもう少し軽いものを選ぶと、コストは劇的に下がり、クエリごとにわずか数分の1セントになります。

Ramp that up to 1000 queries with Claude V2, and you're looking at an overall expense of around $33.
Claude V2で1000クエリに増やすと、全体の費用は約33ドルになります。

This covers the whole journey—sending your question over to the LLM, pulling similar documents from your database to enrich and bound your query to contextual documents, and getting a tailored answer.
これは、質問をLLMに送信し、データベースから類似の文書を引き出してクエリを文脈に関連する文書で豊かにし、カスタマイズされた回答を得るという全体のプロセスをカバーしています。

The real cherry on top with this whole setup is how it's designed to work on a per-request basis, thanks to its serverless nature.
この全体のセットアップの本当の魅力は、サーバーレスの特性のおかげで、リクエストごとに機能するように設計されていることです。

This means you're only ever paying for what you use.
つまり、使用した分だけしか支払わないということです。

<!-- ここまで読んだ! -->

### Expanding Horizons with Serverless RAG サーバーレスRAGによる視野の拡大

Looking ahead, the potential applications of serverless RAG extend far beyond current use cases.
今後、サーバーレスRAGの潜在的な応用は、現在の使用例をはるかに超えています。

By incorporating additional strategies such as re-ranking models for relevance, embedding adapters for enhanced semantic search, and exploring multimodal information integration, developers can further refine and expand their GenAI applications.
関連性のための再ランキングモデル、強化された意味的検索のための埋め込みアダプタ、およびマルチモーダル情報統合などの追加戦略を組み込むことで、開発者はGenAIアプリケーションをさらに洗練し拡大することができます。

Amazon Bedrock's support for serverless RAG opens up new avenues for innovation in the field of generative AI.
Amazon BedrockのサーバーレスRAGへのサポートは、生成AIの分野における革新の新たな道を開きます。

By reducing the barriers to entry and offering a scalable, cost-effective platform, AWS is empowering developers to explore the full potential of AI-driven applications.
参入障壁を低減し、スケーラブルでコスト効果の高いプラットフォームを提供することで、AWSは開発者がAI駆動アプリケーションの可能性を最大限に探求できるようにしています。

As we continue to explore and expand the capabilities of serverless RAG, the possibilities for creating more intelligent, responsive, and relevant AI solutions are boundless.
私たちがサーバーレスRAGの能力を探求し、拡張し続ける中で、より知的で応答性が高く、関連性のあるAIソリューションを創造する可能性は無限です。

Join us on this journey and discover how serverless RAG on Amazon Bedrock can transform your AI projects into reality.
この旅に参加し、Amazon Bedrock上のサーバーレスRAGがどのようにあなたのAIプロジェクトを現実に変えることができるかを発見してください。

<!-- ここまで読んだ! -->

### Resources リソース

Giuseppe Battista  
Giuseppe Battistaは、Amazon Web Services の Senior Solutions Architect です。  
Giuseppe Battista is a Senior Solutions Architect at Amazon Web Services.  
英国とアイルランドの初期段階のスタートアップのソリューションアーキテクチャを指揮しています。  
He leads solution architecture for early-stage startups in the UK and Ireland.  
Giuseppe は twitch.tv/aws で Twitch Show の「Let's Build a Startup」を主催しており、  
Giuseppe hosts the Twitch Show "Let's Build a Startup" on twitch.tv/aws,  
Unicorn's Den アクセラレーターの責任者でもあります。  
and is also the head of the Unicorn's Den accelerator.  
LinkedIn で Giuseppe をフォロー  
Follow Giuseppe on LinkedIn.  

Kevin Shaffer-Morrison  
Kevin Shaffer-Morrisonは、Amazon Web Services の Senior Solutions Architect です。  
Kevin Shaffer-Morrison is a Senior Solutions Architect at Amazon Web Services.  
Kevin は、何百ものスタートアップが迅速に軌道に乗ってクラウドに移行できるようサポートしてきました。  
Kevin has helped hundreds of startups quickly get on track and migrate to the cloud.  
Kevin は、コードサンプルと Twitch ライブストリームを利用して、  
Kevin focuses on supporting founders in their earliest stages using code samples and Twitch live streams,  
創業者の最初期の段階をサポートすることに重点的に取り組んでいます。  
and is dedicated to helping founders in their earliest stages.  
LinkedIn で Kevin をフォロー  
Follow Kevin on LinkedIn.  

このコンテンツはいかがでしたか?  
How did you find this content?  

© 2024 Amazon Web Services, Inc. or its affiliates. All rights reserved.  
© 2024 Amazon Web Services, Inc. またはその関連会社。全著作権所有。  
