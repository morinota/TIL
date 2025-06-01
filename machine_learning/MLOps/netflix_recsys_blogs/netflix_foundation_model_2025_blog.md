# Foundation Model for Personalized Recommendation 個人化推薦のための基盤モデル

Netflix Technology Blog·Follow  
Netflix Technology Blog·フォロー  

Published inNetflix TechBlog·11 min read·Mar 22, 2025  
Netflix TechBlogに掲載·11分で読める·2025年3月22日  

ByKo-Jen Hsiao,Yesu FengandSudarshan Lamkhede  
著者：コー・ジェン・シャオ、イエス・フェン、スダルシャン・ラムケデ  

# Motivation 動機

Netflix’s personalized recommender system is a complex system, boasting a variety of specialized machine learned models each catering to distinct needs including “Continue Watching” and “Today’s Top Picks for You.” 
Netflixのパーソナライズされたレコメンダーシステムは複雑なシステムであり、「続けて視聴」と「今日のあなたへのおすすめトップピック」を含む、**異なるニーズに応じたさまざまな専門的な機械学習モデル**を誇っています。（詳細については、最近の概要を参照してください）。 
However, as we expanded our set of personalization algorithms to meet increasing business needs, maintenance of the recommender system became quite costly. 
しかし、ビジネスニーズの増加に対応するためにパーソナライズアルゴリズムのセットを拡大するにつれて、**レコメンダーシステムの維持が非常にコストがかかるように**なりました。 
Furthermore, it was difficult to transfer innovations from one model to another, given that most are independently trained despite using common data sources. 
さらに、**ほとんどのモデルが共通のデータソースを使用しているにもかかわらず、独立してトレーニングされているため、モデル間での革新の移転が困難**でした。 
This scenario underscored the need for a new recommender system architecture where member preference learning is centralized, enhancing accessibility and utility across different models. 
この状況は、**ユーザの嗜好の学習を集中化**し、異なるモデル間でのアクセス性と有用性が向上する新しいレコメンダーシステムアーキテクチャの必要性を強調しました。 

<!-- ここまで読んだ -->

Particularly, these models predominantly extract features from members’ recent interaction histories on the platform. 
特に、**これらのモデルは主にプラットフォーム上でのメンバーの最近のインタラクション履歴から特徴を抽出**します。 
Yet, many are confined to a brief temporal window due to constraints in serving latency or training costs. 
しかし、多くのモデルは、サービスのレイテンシやトレーニングコストの制約により、短い時間的ウィンドウに制限されています。 
This limitation has inspired us to develop a foundation model for recommendation. 
この制限は、私たちに推薦のための基盤モデルを開発するインスピレーションを与えました。 
This model aims to assimilate information both from members’ comprehensive interaction histories and our content at a very large scale. 
このモデルは、**メンバーの包括的なインタラクション履歴と私たちのコンテンツからの情報を非常に大規模に同化すること**を目指しています。 
(ここで同化って、共通の埋め込み空間にmappingする、みたいなイメージなのかな...!:thinking:)
It facilitates the distribution of these learnings to other models, either through shared model weights for fine tuning or directly through embeddings.
これにより、**ファインチューニングのための共有モデルウェイトを介して、または埋め込みを通じて、これらの学習を他のモデルに分配する**ことが可能になります。 
(なるほど、各ユースケースの下流モデルへの知識の伝搬方法は2種類っぽい! 1つはfine-tuning前のモデル初期パラメータによる伝搬、もう一つは基盤モデルから出力される埋め込みを下流モデルの入力として使う伝搬...!!:thinking:)

<!-- ここまで読んだ -->

The impetus for constructing a foundational recommendation model is based on the paradigm shift in natural language processing (NLP) to large language models (LLMs). 
**基盤となる推薦モデルを構築するモチベーションは、自然言語処理（NLP）における大規模言語モデル（LLMs）へのパラダイムシフトに基づいています**。 (うんうん)
In NLP, the trend is moving away from numerous small, specialized models towards a single, large language model that can perform a variety of tasks either directly or with minimal fine-tuning. 
NLPでは、トレンドは多数の小さな専門モデルから、さまざまなタスクを直接または最小限のファインチューニングで実行できる単一の大規模言語モデルへと移行しています。 
Key insights from this shift include:
このシフトから得られた重要な洞察には以下が含まれます:

1. A Data-Centric Approach: Shifting focus from model-centric strategies, which heavily rely on feature engineering, to a data-centric one. 
2. データ中心のアプローチ：特徴エンジニアリングに大きく依存するモデル中心の戦略から、デ**ータ中心のアプローチに焦点を移す**。
This approach prioritizes the accumulation of large-scale, high-quality data and, where feasible, aims for end-to-end learning. 
このアプローチは、大規模で高品質なデータの蓄積を優先し、可能な場合はエンドツーエンドの学習を目指します。 

1. Leveraging Semi-Supervised Learning: The next-token prediction objective in LLMs has proven remarkably effective. 
2. 半教師あり学習の活用：**LLMsにおける次のトークン予測の目的関数は、非常に効果的である**ことが証明されています。 
It enables large-scale semi-supervised learning using unlabeled data while also equipping the model with a surprisingly deep understanding of world knowledge. 
これにより、**ラベルのないデータを使用した大規模な半教師あり学習**が可能になり、モデルに驚くほど深い世界知識の理解を与えます。 

These insights have shaped the design of our foundation model, enabling a transition from maintaining numerous small, specialized models to building a scalable, efficient system. 
これらの洞察は、私たちの基盤モデルの設計に影響を与え、多数の小さな専門モデルの維持から、スケーラブルで効率的なシステムの構築への移行を可能にしました。 
By scaling up semi-supervised training data and model parameters, we aim to develop a model that not only meets current needs but also adapts dynamically to evolving demands, ensuring sustainable innovation and resource efficiency. 
**半教師ありトレーニングデータとモデルパラメータを拡大することで**、私たちは現在のニーズを満たすだけでなく、進化する要求に動的に適応するモデルを開発し、持続可能な革新とリソース効率を確保することを目指しています。

<!-- ここまで読んだ!-->

# Data データ

At Netflix, user engagement spans a wide spectrum, from casual browsing to committed movie watching. 
Netflixでは、ユーザーのエンゲージメントはカジュアルなブラウジングから本格的な映画視聴まで幅広い範囲にわたります。
With over 300 million users at the end of 2024, this translates into hundreds of billions of interactions — an immense dataset comparable in scale to the token volume of large language models (LLMs). 
**2024年末までに3億人以上のユーザーを抱えることで、これは数百億のインタラクションに相当し、大規模言語モデル（LLMs）のトークン量に匹敵する膨大なデータセットとなります**。
However, as in LLMs, the quality of data often outweighs its sheer volume. 
しかし、LLMsと同様に、データの質はその単純な量をしばしば上回ります。
To harness this data effectively, we employ a process of interaction tokenization, ensuring meaningful events are identified and redundancies are minimized. 
このデータを効果的に活用するために、私たちは**インタラクションのトークン化プロセスを採用**し、意味のあるイベントが特定され、冗長性が最小限に抑えられるようにしています。

**Tokenizing User Interactions**: Not all raw user actions contribute equally to understanding preferences. 
ユーザーインタラクションのトークン化：すべての生のユーザアクションが好みを理解するために同じように寄与するわけではありません。(うんうん、重要なtokenとそうでないtokenがあるよね...!:thinking:)
Tokenization helps define what constitutes a meaningful “token” in a sequence. 
トークン化は、シーケンスにおいて意味のある「トークン」を構成するものを定義するのに役立ちます。
Drawing an analogy to Byte Pair Encoding (BPE) in NLP, we can think of tokenization as merging adjacent actions to form new, higher-level tokens. 
自然言語処理（NLP）におけるバイトペアエンコーディング（BPE）に例えると、**トークン化は隣接するアクションを結合して新しい高次のトークンを形成すること**と考えられます。
However, unlike language tokenization, creating these new tokens requires careful consideration of what information to retain. 
しかし、言語のトークン化とは異なり、これらの新しいトークンを作成するには、保持すべき情報について慎重に考慮する必要があります。
For instance, the total watch duration might need to be summed or engagement types aggregated to preserve critical details. 
**例えば、合計視聴時間を合算したり、エンゲージメントタイプを集約したりして、重要な詳細を保持する必要があるかも**しれません。

This tradeoff between granular data and sequence compression is akin to the balance in LLMs between vocabulary size and context window. 
粒度の細かいデータとシーケンス圧縮の間のこのトレードオフは、LLMsにおける語彙サイズとコンテキストウィンドウのバランスに似ています。
In our case, the goal is to balance the length of interaction history against the level of detail retained in individual tokens. 
私たちの場合、目標はインタラクション履歴の長さと個々のトークンに保持される詳細レベルのバランスを取ることです。
Overly lossy tokenization risks losing valuable signals, while too granular a sequence can exceed practical limits on processing time and memory. 
過度に情報を失うトークン化は貴重な信号を失うリスクがあり、逆に細かすぎるシーケンスは処理時間とメモリの実用的な限界を超える可能性があります。

Even with such strategies, interaction histories from active users can span thousands of events, exceeding the capacity of transformer models with standard self attention layers. 
このような戦略を用いても、アクティブユーザーのインタラクション履歴は数千のイベントにわたることがあり、標準的な自己注意層を持つトランスフォーマーモデルの能力を超えます。
In recommendation systems, context windows during inference are often limited to hundreds of events — not due to model capability but because these services typically require millisecond-level latency. 
**推薦システムでは、推論中のコンテキストウィンドウは通常数百のイベントに制限されます。これはモデルの能力によるものではなく、これらのサービスが通常ミリ秒レベルのレイテンシを必要とするため**です。
This constraint is more stringent than what is typical in LLM applications, where longer inference times (seconds) are more tolerable. 
この制約は、LLMアプリケーションで一般的なものである長い推論時間（秒）がより許容されるのとは異なり、より厳しいものです。

To address this during training, we implement two key solutions: 
この問題に対処するために、私たちは2つの重要な解決策を実装します：
1. Sparse Attention Mechanisms: By leveraging sparse attention techniques such as low-rank compression, the model can extend its context window to several hundred events while maintaining computational efficiency. 
1. スパースアテンションメカニズム：低ランク圧縮などのスパースアテンション技術を活用することで、モデルは計算効率を維持しながらコンテキストウィンドウを数百のイベントに拡張できます。
This enables it to process more extensive interaction histories and derive richer insights into long-term preferences. 
これにより、より広範なインタラクション履歴を処理し、長期的な好みに関するより豊かな洞察を得ることができます。
2. Sliding Window Sampling: During training, we sample overlapping windows of interactions from the full sequence. 
2. スライディングウィンドウサンプリング：トレーニング中に、完全なシーケンスから重複するインタラクションのウィンドウをサンプリングします。
This ensures the model is exposed to different segments of the user’s history over multiple epochs, allowing it to learn from the entire sequence without requiring an impractically large context window. 
これにより、モデルは複数のエポックにわたってユーザーの履歴の異なるセグメントにさらされ、非現実的に大きなコンテキストウィンドウを必要とせずに全シーケンスから学習できるようになります。

At inference time, when multi-step decoding is needed, we can deploy KV caching to efficiently reuse past computations and maintain low latency. 
推論時にマルチステップデコーディングが必要な場合、過去の計算を効率的に再利用し、低レイテンシを維持するためにKVキャッシングを展開できます。
These approaches collectively allow us to balance the need for detailed, long-term interaction modeling with the practical constraints of model training and inference, enhancing both the precision and scalability of our recommendation system. 
これらのアプローチは、詳細で長期的なインタラクションモデリングの必要性とモデルのトレーニングおよび推論の実用的な制約とのバランスを取ることを可能にし、推薦システムの精度とスケーラビリティの両方を向上させます。

Information in Each ‘Token’: While the first part of our tokenization process focuses on structuring sequences of interactions, the next critical step is defining the rich information contained within each token. 
各「トークン」の情報：トークン化プロセスの最初の部分がインタラクションのシーケンスを構造化することに焦点を当てているのに対し、次の重要なステップは各トークンに含まれる豊富な情報を定義することです。
Unlike LLMs, which typically rely on a single embedding space to represent input tokens, our interaction events are packed with heterogeneous details. 
LLMsとは異なり、通常は入力トークンを表現するために単一の埋め込み空間に依存するのに対し、私たちのインタラクションイベントは異種の詳細で満たされています。
These include attributes of the action itself (such as locale, time, duration, and device type) as well as information about the content (such as item ID and metadata like genre and release country). 
これには、**アクション自体の属性（ロケール、時間、期間、デバイスタイプなど）や、コンテンツに関する情報（アイテムIDやジャンル、リリース国などのメタデータ）**が含まれます。
Most of these features, especially categorical ones, are directly embedded within the model, embracing an end-to-end learning approach. 
これらの特徴のほとんど、特にカテゴリカルなものは、モデル内に直接埋め込まれ、エンドツーエンドの学習アプローチを採用しています。
However, certain features require special attention. 
しかし、特定の特徴は特別な注意を必要とします。
For example, timestamps need additional processing to capture both absolute and relative notions of time, with absolute time being particularly important for understanding time-sensitive behaviors. 
例えば、タイムスタンプは絶対的および相対的な時間の概念を捉えるために追加の処理が必要であり、絶対的な時間は時間に敏感な行動を理解するために特に重要です。

To enhance prediction accuracy in sequential recommendation systems, we organize token features into two categories: 
シーケンシャル推薦システムにおける予測精度を向上させるために、**トークンの特徴を2つのカテゴリに整理**します：
1. Request-Time Features: These are features available at the moment of prediction, such as log-in time, device, or location. 
1. リクエスト時間特徴：これらは、予測の瞬間に利用可能な特徴で、ログイン時間、デバイス、または位置情報などがあります。
2. Post-Action Features: These are details available after an interaction has occurred, such as the specific show interacted with or the duration of the interaction. 
2. アクション後の特徴：これらは、インタラクションが発生した後に利用可能な詳細で、具体的にインタラクションしたショーやインタラクションの期間などがあります。

To predict the next interaction, we combine request-time features from the current step with post-action features from the previous step. 
**次のインタラクションを予測するために、現在のステップのリクエスト時間特徴と前のステップのアクション後の特徴を組み合わせ**ます。
This blending of contextual and historical information ensures each token in the sequence carries a comprehensive representation, capturing both the immediate context and user behavior patterns over time. 
この文脈情報と歴史的情報のブレンドにより、シーケンス内の各トークンが包括的な表現を持ち、即時の文脈と時間を通じたユーザー行動パターンの両方を捉えることが保証されます。

<!-- ここまで読んだ -->

# Considerations for Model Objective and Architecture モデルの目的とアーキテクチャに関する考慮事項

As previously mentioned, our default approach employs the autoregressive next-token prediction objective, similar to GPT. 
前述のように、私たちのデフォルトのアプローチは、**GPTに似た自己回帰的なnext-token prediction目的関数を採用**しています。(このnext-token predictionタスクが、よく「半教師あり学習」って呼ばれるやつだっけ...!:thinking:)
This strategy effectively leverages the vast scale of unlabeled user interaction data. 
**この戦略は、ラベルのないユーザインタラクションデータの膨大なスケールを効果的に活用します。**
The adoption of this objective in recommendation systems has shown multiple successes [1–3]. 
この目的の推薦システムへの採用は、いくつかの成功を示しています[1–3]。 
However, given the distinct differences between language tasks and recommendation tasks, we have made several critical modifications to the objective. 
しかし、言語タスクと推薦タスクの間には明確な違いがあるため、私たちは目的にいくつかの重要な修正を加えました。

Firstly, during the pretraining phase of typical LLMs, such as GPT, every target token is generally treated with equal weight. 
まず、GPTのような典型的なLLMの事前学習フェーズでは、すべてのターゲットトークンは一般的に等しい重みで扱われます。 
In contrast, in our model, not all user interactions are of equal importance. 
**対照的に、私たちのモデルでは、すべてのユーザーインタラクションが等しい重要性を持つわけではありません**。 
For instance, a 5-minute trailer play should not carry the same weight as a 2-hour full movie watch. 
**例えば、5分間のトレーラー再生は、2時間のフルムービー視聴と同じ重みを持つべきではありません**。(なるほどimplicit feedbackの中でも、ユーザの嗜好を表す度合いには違いがあるよね...!:thinking:)
A greater challenge arises when trying to align long-term user satisfaction with specific interactions and recommendations. 
特定のインタラクションや推薦と長期的なユーザー満足度を一致させようとすると、より大きな課題が生じます。 
To address this, we can adopt a multi-token prediction objective during training, where the model predicts the next tokens at each step instead of a single token [4]. 
これに対処するために、トレーニング中にマルチトークン予測目的を採用し、モデルが単一のトークンの代わりに各ステップで次のトークンを予測することができます[4]。 
This approach encourages the model to capture longer-term dependencies and avoid myopic predictions focused solely on immediate next events. 
このアプローチは、モデルが長期的な依存関係を捉え、即時の次のイベントにのみ焦点を当てた短期的な予測を避けることを促します。

Secondly, we can use multiple fields in our input data as auxiliary prediction objectives in addition to predicting the next item ID, which remains the primary target. 
次に、次のアイテムIDを予測することに加えて、入力データの複数のフィールドを補助的な予測目的として使用することができます。 
For example, we can derive genres from the items in the original sequence and use this genre sequence as an auxiliary target. 
例えば、元のシーケンスのアイテムからジャンルを導出し、このジャンルシーケンスを補助的なターゲットとして使用することができます。 
This approach serves several purposes: it acts as a regularizer to reduce overfitting on noisy item ID predictions, provides additional insights into user intentions or long-term genre preferences, and, when structured hierarchically, can improve the accuracy of predicting the target item ID. 
このアプローチは、いくつかの目的を果たします：ノイズの多いアイテムID予測に対する過学習を減少させるための正則化器として機能し、ユーザーの意図や長期的なジャンルの好みに関する追加の洞察を提供し、階層的に構造化されると、ターゲットアイテムIDの予測精度を向上させることができます。 
By first predicting auxiliary targets, such as genre or original language, the model effectively narrows down the candidate list, simplifying subsequent item ID prediction. 
まずジャンルや原言語などの補助的なターゲットを予測することで、モデルは候補リストを効果的に絞り込み、その後のアイテムID予測を簡素化します。



# Unique Challenges for Recommendation FM 推薦FMのためのユニークな課題

In addition to the infrastructure challenges posed by training bigger models with substantial amounts of user interaction data that are common when trying to build foundation models, there are several unique hurdles specific to recommendations to make them viable. 
基盤モデルを構築する際に一般的なユーザーインタラクションデータの大量を用いて大きなモデルを訓練することによって生じるインフラストラクチャの課題に加えて、推薦を実現可能にするためのいくつかのユニークな障害があります。

One of unique challenges is entity cold-starting. 
ユニークな課題の一つは、エンティティのコールドスタートです。

At Netflix, our mission is to entertain the world. 
Netflixでは、私たちの使命は世界を楽しませることです。

New titles are added to the catalog frequently. 
新しいタイトルは頻繁にカタログに追加されます。

Therefore the recommendation foundation models require a cold start capability, which means the models need to estimate members’ preferences for newly launched titles before anyone has engaged with them. 
したがって、推薦基盤モデルはコールドスタート機能を必要とし、これはモデルが誰も新しく立ち上げられたタイトルに関与する前に、メンバーの好みを推定する必要があることを意味します。

To enable this, our foundation model training framework is built with the following two capabilities: Incremental training and being able to do inference with unseen entities. 
これを可能にするために、私たちの基盤モデルの訓練フレームワークは、以下の2つの機能を備えています：インクリメンタルトレーニングと未見のエンティティでの推論能力です。

1. Incremental training: Foundation models are trained on extensive datasets, including every member’s history of plays and actions, making frequent retraining impractical. 
1. インクリメンタルトレーニング：基盤モデルは、すべてのメンバーのプレイとアクションの履歴を含む広範なデータセットで訓練されており、頻繁な再訓練は非現実的です。

However, our catalog and member preferences continually evolve. 
しかし、私たちのカタログとメンバーの好みは常に進化しています。

Unlike large language models, which can be incrementally trained with stable token vocabularies, our recommendation models require new embeddings for new titles, necessitating expanded embedding layers and output components. 
安定したトークン語彙でインクリメンタルトレーニングが可能な大規模言語モデルとは異なり、私たちの推薦モデルは新しいタイトルのために新しい埋め込みを必要とし、埋め込み層と出力コンポーネントの拡張を必要とします。

To address this, we warm-start new models by reusing parameters from previous models and initializing new parameters for new titles. 
これに対処するために、私たちは以前のモデルからパラメータを再利用し、新しいタイトルのために新しいパラメータを初期化することで新しいモデルをウォームスタートします。

For example, new title embeddings can be initialized by adding slight random noise to existing average embeddings or by using a weighted combination of similar titles’ embeddings based on metadata. 
例えば、新しいタイトルの埋め込みは、既存の平均埋め込みにわずかなランダムノイズを加えるか、メタデータに基づいて類似タイトルの埋め込みの加重組み合わせを使用することで初期化できます。

This approach allows new titles to start with relevant embeddings, facilitating faster fine-tuning. 
このアプローチにより、新しいタイトルは関連する埋め込みで開始でき、より迅速なファインチューニングが可能になります。

In practice, the initialization method becomes less critical when more member interaction data is used for fine-tuning. 
実際には、ファインチューニングにより多くのメンバーインタラクションデータが使用されると、初期化方法はそれほど重要ではなくなります。

2. Dealing with unseen entities: Even with incremental training, it’s not always guaranteed to learn efficiently on new entities (ex: newly launched titles). 
2. 未見のエンティティへの対処：インクリメンタルトレーニングを行っても、新しいエンティティ（例：新しく立ち上げられたタイトル）で効率的に学習できる保証はありません。

It’s also possible that there will be some new entities that are not included/seen in the training data even if we fine-tune foundation models on a frequent basis. 
基盤モデルを頻繁にファインチューニングしても、訓練データに含まれていない新しいエンティティが存在する可能性もあります。

Therefore, it’s also important to let foundation models use metadata information of entities and inputs, not just member interaction data. 
したがって、基盤モデルがメンバーのインタラクションデータだけでなく、エンティティや入力のメタデータ情報を使用できるようにすることも重要です。

Thus, our foundation model combines both learnable item id embeddings and learnable embeddings from metadata. 
このようにして、私たちの基盤モデルは、学習可能なアイテムID埋め込みとメタデータからの学習可能な埋め込みの両方を組み合わせています。

The following diagram demonstrates this idea. 
以下の図はこのアイデアを示しています。

To create the final title embedding, we combine this metadata-based embedding with a fully-learnable ID-based embedding using a mixing layer. 
最終的なタイトル埋め込みを作成するために、私たちはこのメタデータベースの埋め込みを、ミキシングレイヤーを使用して完全に学習可能なIDベースの埋め込みと組み合わせます。

Instead of simply summing these embeddings, we use an attention mechanism based on the “age” of the entity. 
これらの埋め込みを単純に合計するのではなく、私たちはエンティティの「年齢」に基づいた注意メカニズムを使用します。

This approach allows new titles with limited interaction data to rely more on metadata, while established titles can depend more on ID-based embeddings. 
このアプローチにより、インタラクションデータが限られた新しいタイトルはメタデータにより依存し、確立されたタイトルはIDベースの埋め込みにより依存することができます。

Since titles with similar metadata can have different user engagement, their embeddings should reflect these differences. 
類似のメタデータを持つタイトルは異なるユーザーエンゲージメントを持つ可能性があるため、それらの埋め込みはこれらの違いを反映する必要があります。

Introducing some randomness during training encourages the model to learn from metadata rather than relying solely on ID embeddings. 
訓練中にいくつかのランダム性を導入することで、モデルはID埋め込みにのみ依存するのではなく、メタデータから学習することを促します。

This method ensures that newly-launched or pre-launch titles have reasonable embeddings even with no user interaction data. 
この方法により、新しく立ち上げられたタイトルやプレローンチタイトルは、ユーザーインタラクションデータがなくても合理的な埋め込みを持つことが保証されます。



# Downstream Applications and Challenges 下流アプリケーションと課題

Our recommendation foundation model is designed to understand long-term member preferences and can be utilized in various ways by downstream applications:
私たちの推薦基盤モデルは、長期的なメンバーの好みを理解するように設計されており、下流アプリケーションによってさまざまな方法で利用できます。

1. Direct Use as a Predictive Model
   1. 予測モデルとしての直接使用
   The model is primarily trained to predict the next entity a user will interact with. 
   このモデルは、ユーザーが次に対話するエンティティを予測するために主に訓練されています。
   It includes multiple predictor heads for different tasks, such as forecasting member preferences for various genres. 
   さまざまなジャンルに対するメンバーの好みを予測するなど、異なるタスクのための複数の予測ヘッドが含まれています。
   These can be directly applied to meet diverse business needs.
   これらは多様なビジネスニーズに応えるために直接適用できます。

2. Utilizing embeddings
   2. 埋め込みの利用
   The model generates valuable embeddings for members and entities like videos, games, and genres. 
   このモデルは、メンバーや動画、ゲーム、ジャンルなどのエンティティに対して貴重な埋め込みを生成します。
   These embeddings are calculated in batch jobs and stored for use in both offline and online applications. 
   これらの埋め込みはバッチジョブで計算され、オフラインおよびオンラインアプリケーションで使用するために保存されます。
   They can serve as features in other models or be used for candidate generation, such as retrieving appealing titles for a user. 
   これらは他のモデルの特徴として機能したり、ユーザーに魅力的なタイトルを取得するための候補生成に使用されたりします。
   High-quality title embeddings also support title-to-title recommendations. 
   高品質のタイトル埋め込みは、タイトル間推薦もサポートします。
   However, one important consideration is that the embedding space has arbitrary, uninterpretable dimensions and is incompatible across different model training runs. 
   しかし、重要な考慮事項は、埋め込み空間が任意の解釈不可能な次元を持ち、異なるモデルのトレーニング実行間で互換性がないことです。
   This poses challenges for downstream consumers, who must adapt to each retraining and redeployment, risking bugs due to invalidated assumptions about the embedding structure. 
   これは、下流の消費者にとって課題を引き起こし、各再トレーニングと再展開に適応しなければならず、埋め込み構造に関する無効化された仮定によるバグのリスクがあります。
   To address this, we apply an orthogonal low-rank transformation to stabilize the user/item embedding space, ensuring consistent meaning of embedding dimensions, even as the base foundation model is retrained and redeployed.
   これに対処するために、ユーザー/アイテム埋め込み空間を安定させるために直交低ランク変換を適用し、基盤モデルが再トレーニングおよび再展開される際にも埋め込み次元の意味が一貫していることを保証します。

3. Fine-Tuning with Specific Data
   3. 特定データによるファインチューニング
   The model’s adaptability allows for fine-tuning with application-specific data. 
   このモデルの適応性により、アプリケーション特有のデータでファインチューニングが可能です。
   Users can integrate the full model or subgraphs into their own models, fine-tuning them with less data and computational power. 
   ユーザーは、完全なモデルまたはサブグラフを自分のモデルに統合し、少ないデータと計算リソースでファインチューニングできます。
   This approach achieves performance comparable to previous models, despite the initial foundation model requiring significant resources.
   このアプローチは、初期の基盤モデルが多くのリソースを必要とするにもかかわらず、以前のモデルと同等のパフォーマンスを達成します。



# Scaling Foundation Models for Netflix Recommendations Netflixの推薦のための基盤モデルのスケーリング

In scaling up our foundation model for Netflix recommendations, we draw inspiration from the success of large language models (LLMs).  
Netflixの推薦のための基盤モデルをスケールアップするにあたり、私たちは大規模言語モデル（LLMs）の成功からインスピレーションを得ています。

Just as LLMs have demonstrated the power of scaling in improving performance, we find that scaling is crucial for enhancing generative recommendation tasks.  
LLMsがパフォーマンス向上におけるスケーリングの力を示しているように、私たちはスケーリングが生成的推薦タスクを向上させるために重要であることを発見しました。

Successful scaling demands robust evaluation, efficient training algorithms, and substantial computing resources.  
成功するスケーリングには、堅牢な評価、効率的なトレーニングアルゴリズム、および substantial computing resources（相当な計算リソース）が必要です。

Evaluation must effectively differentiate model performance and identify areas for improvement.  
評価は、モデルのパフォーマンスを効果的に区別し、改善の余地を特定しなければなりません。

Scaling involves data, model, and context scaling, incorporating user engagement, external reviews, multimedia assets, and high-quality embeddings.  
スケーリングは、データ、モデル、およびコンテキストのスケーリングを含み、ユーザーエンゲージメント、外部レビュー、マルチメディア資産、および高品質の埋め込みを取り入れます。

Our experiments confirm that the scaling law also applies to our foundation model, with consistent improvements observed as we increase data and model size.  
私たちの実験は、スケーリング法則が私たちの基盤モデルにも適用されることを確認しており、データとモデルのサイズを増やすにつれて一貫した改善が観察されました。



# Conclusion 結論

In conclusion, our Foundation Model for Personalized Recommendation represents a significant step towards creating a unified, data-centric system that leverages large-scale data to increase the quality of recommendations for our members. 
結論として、私たちのパーソナライズド推薦のためのファウンデーションモデルは、メンバーへの推薦の質を向上させるために大規模データを活用する統一されたデータ中心のシステムを作成するための重要なステップを示しています。

This approach borrows insights from Large Language Models (LLMs), particularly the principles of semi-supervised learning and end-to-end training, aiming to harness the vast scale of unlabeled user interaction data. 
このアプローチは、大規模言語モデル（LLMs）からの洞察を借りており、特に半教師あり学習とエンドツーエンドトレーニングの原則を取り入れ、ラベルのないユーザーインタラクションデータの膨大なスケールを活用することを目指しています。

Addressing unique challenges, like cold start and presentation bias, the model also acknowledges the distinct differences between language tasks and recommendation. 
コールドスタートやプレゼンテーションバイアスのような独自の課題に対処しながら、このモデルは言語タスクと推薦の間の明確な違いも認識しています。

The Foundation Model allows various downstream applications, from direct use as a predictive model to generate user and entity embeddings for other applications, and can be fine-tuned for specific canvases. 
ファウンデーションモデルは、予測モデルとしての直接使用から他のアプリケーションのためのユーザーおよびエンティティの埋め込みを生成することまで、さまざまなダウンストリームアプリケーションを可能にし、特定のキャンバスに合わせてファインチューニングすることができます。

We see promising results from downstream integrations. 
私たちは、ダウンストリーム統合からの有望な結果を見ています。

This move from multiple specialized models to a more comprehensive system marks an exciting development in the field of personalized recommendation systems. 
複数の専門モデルからより包括的なシステムへの移行は、パーソナライズド推薦システムの分野におけるエキサイティングな進展を示しています。



# Acknowledgements 謝辞

Contributors to this work (name in alphabetical order): 
この研究に貢献した人々（アルファベット順）：
Ai-Lei Sun
Ai-Lei Sun  
Aish Fenton
Aish Fenton  
Anne Cocos
Anne Cocos  
Anuj Shah
Anuj Shah  
Arash Aghevli
Arash Aghevli  
Baolin Li
Baolin Li  
Bowei Yan
Bowei Yan  
Dan Zheng
Dan Zheng  
Dawen Liang
Dawen Liang  
Ding Tong
Ding Tong  
Divya Gadde
Divya Gadde  
Emma Kong
Emma Kong  
Gary Yeh
Gary Yeh  
Inbar Naor
Inbar Naor  
Jin Wang
Jin Wang  
Justin Basilico
Justin Basilico  
Kabir Nagrecha
Kabir Nagrecha  
Kevin Zielnicki
Kevin Zielnicki  
Linas Baltrunas
Linas Baltrunas  
Lingyi Liu
Lingyi Liu  
Luke Wang
Luke Wang  
Matan Appelbaum
Matan Appelbaum  
Michael Tu
Michael Tu  
Moumita Bhattacharya
Moumita Bhattacharya  
Pablo Delgado
Pablo Delgado  
Qiuling Xu
Qiuling Xu  
Rakesh Komuravelli
Rakesh Komuravelli  
Raveesh Bhalla
Raveesh Bhalla  
Rob Story
Rob Story  
Roger Menezes
Roger Menezes  
Sejoon Oh
Sejoon Oh  
Shahrzad Naseri
Shahrzad Naseri  
Swanand Joshi
Swanand Joshi  
Trung Nguyen
Trung Nguyen  
Vito Ostuni
Vito Ostuni  
Wei Wang
Wei Wang  
Zhe Zhang
Zhe Zhang  



# Reference 参考文献

1. C. K. Kang and J. McAuley, “Self-Attentive Sequential Recommendation,”2018 IEEE International Conference on Data Mining (ICDM), Singapore, 2018, pp. 197–206, doi: 10.1109/ICDM.2018.00035.
   C. K. KangとJ. McAuleyによる「自己注意型逐次推薦」、2018年IEEE国際データマイニング会議（ICDM）、シンガポール、2018年、pp. 197–206、doi: 10.1109/ICDM.2018.00035。

2. F. Sun et al., “BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer,”Proceedings of the 28th ACM International Conference on Information and Knowledge Management (CIKM ‘19), Beijing, China, 2019, pp. 1441–1450, doi: 10.1145/3357384.3357895.
   F. Sunらによる「BERT4Rec: Transformerからの双方向エンコーダ表現を用いた逐次推薦」、第28回ACM国際情報および知識管理会議（CIKM '19）予稿、北京、中国、2019年、pp. 1441–1450、doi: 10.1145/3357384.3357895。

3. J. Zhai et al., “Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations,”arXiv preprint arXiv:2402.17152, 2024.
   J. Zhaiらによる「行動は言葉よりも雄弁である: 生成的推薦のための兆候パラメータ逐次変換器」、arXivプレプリント arXiv:2402.17152、2024年。

4. F. Gloeckle, B. Youbi Idrissi, B. Rozière, D. Lopez-Paz, and G. Synnaeve, “Better & Faster Large Language Models via Multi-token Prediction,” arXiv preprint arXiv:2404.19737, Apr. 2024.
   F. Gloeckle、B. Youbi Idrissi、B. Rozière、D. Lopez-Paz、G. Synnaeveによる「マルチトークン予測によるより良く、より速い大規模言語モデル」、arXivプレプリント arXiv:2404.19737、2024年4月。



## Sign up to discover human stories that deepen your understanding of the world. 
世界の理解を深める人間の物語を発見するためにサインアップしてください。



## Free 無料

Distraction-free reading. No ads.  
気を散らさない読書。広告なし。

Organize your knowledge with lists and highlights.  
リストやハイライトで知識を整理しましょう。

Tell your story. Find your audience.  
あなたの物語を語りましょう。聴衆を見つけましょう。

Sign up for free  
無料でサインアップ



## Membership メンバーシップ

Read member-only stories
メンバー限定のストーリーを読む

Support writers you read most
最もよく読む作家をサポートする

Earn money for your writing
執筆でお金を稼ぐ

Listen to audio narrations
オーディオナレーションを聞く

Read offline with the Medium app
Mediumアプリでオフラインで読む

Try for $5/month
月額$5でお試し

969
969

969
969

18
18

Follow
フォロー



## Published inNetflix TechBlog

Published inNetflix TechBlog
Netflix TechBlogに掲載されました

162K Followers
162K フォロワー

·
·
Apr 1, 2025
2025年4月1日

Learn about Netflix’s world class engineering efforts, company culture, product developments and more.
Netflixの世界クラスのエンジニアリング努力、企業文化、製品開発などについて学びましょう。

Follow
フォロー



## Written byNetflix Technology Blog

Written byNetflix Technology Blog
Netflix Technology Blogによって書かれました。

433K Followers
433K フォロワー

·
·

Learn more about how Netflix designs, builds, and operates our systems and engineering organizations
Netflixがどのようにシステムとエンジニアリング組織を設計、構築、運営しているかについてもっと学びましょう。

Follow
フォローする



## Responses (18) 返信 (18)

Write a response 返信を書く  
What are your thoughts? あなたの考えは何ですか？  
What are your thoughts? あなたの考えは何ですか？  
Also publish to my profile プロフィールにも公開する  
Also publish to my profile プロフィールにも公開する  

Ademola Oduola  
Mar 23  
Mar 23  

Netflix’s personalized recommender system is a complex system, boasting a variety of specialized  
Netflixのパーソナライズされた推薦システムは、さまざまな専門的な機能を備えた複雑なシステムです。  

```
Beautiful write up  
```
```
美しい文章です  

9  
Reply 返信  

zahra eskandari  
Mar 22  
Mar 22  

```
thanks for sharing. This was an insightful post. Any reports on how this foundation model is performing?  
```
```
共有してくれてありがとう。これは洞察に満ちた投稿でした。この基盤モデルのパフォーマンスに関する報告はありますか？  

8  
Reply 返信  

ravi choudhary  
Mar 22  
Mar 22  

```
That's an insightful article; it appears that every big tech companies are converging on similar concepts, aiming to capitalize on approaches rooted in large language models.  
```
```
これは洞察に満ちた記事です。すべての大手テクノロジー企業が似たような概念に収束しているようで、大規模言語モデルに基づくアプローチを活用しようとしています。  

6  
Reply 返信  



## More from Netflix Technology Blog and Netflix TechBlog Netflix Technology BlogおよびNetflix TechBlogからのさらなる情報

In
Netflix TechBlog
by
Netflix Technology Blog
において



## Globalizing Productions with Netflix’s Media Production Suite  
### Jesse Korosi, Thijs van de Kamp, Mayra Vega, Laura Futuro, Anton Margoline
Apr 11675
Apr 1
167
5
In
Netflix TechBlog
by
Netflix Technology Blog

## Netflixのメディア制作スイートによる制作のグローバル化  
### ジェシー・コロシ、タイス・ファン・デ・カンプ、マイラ・ベガ、ローラ・フチューロ、アントン・マルゴリン
2023年4月11675
2023年4月1日
167
5
に
Netflix TechBlog
によって
Netflix Technology Blog



## HDR10+ Now Streaming on Netflix HDR10+がNetflixでストリーミング中

### Roger Quero, Liwei Guo, Jeff Watts, Joseph McCormick, Agata Opalach, Anush Moorthy
### ロジャー・ケロ、リウェイ・グオ、ジェフ・ワッツ、ジョセフ・マコーミック、アガタ・オパラチ、アヌシュ・ムールティ

Mar 25935  
2023年3月25日

In  
Netflix TechBlog  
による  
Netflix Technology Blog  



## Title Launch Observability at Netflix Scale タイトル Netflixスケールでのローンチ可観測性  
### Part 3: System Strategies and Architecture パート3: システム戦略とアーキテクチャ
Mar 52225  
Mar 5  
222  
5  
In  
Netflix TechBlog  
by  
Netflix Technology Blog  



## Java 21 Virtual Threads - Dude, Where’s My Lock?  
### Getting real with virtual threads
Java 21の仮想スレッド - ねえ、私のロックはどこ？  
### 仮想スレッドの実際の利用
Jul 30, 2024
2024年7月30日
2.6K
2.6K
34
34



## Recommended from Medium おすすめのMediumから

In
Coding Beauty
by
Tari Ibaba
において



## This new IDE from Google is an absolute game changer この新しいIDEはGoogleからの絶対的なゲームチェンジャーです  
### This new IDE from Google is seriously revolutionary. この新しいIDEはGoogleからの本当に革命的です。
Mar 123.8K203  
Mar 12  
3.8K  
203  
Sebastian Carlos  



## Fired From Meta After 1 Week: Here’s All The Dirt I Got  
### This is not just another story of a disgruntled ex-employee. I’m not shying away from the serious corporate espionage or the ethical…  
## メタから1週間で解雇された：私が得たすべての内部情報  
### これは不満を持つ元従業員のただの話ではありません。私は深刻な企業スパイ活動や倫理的な問題から逃げてはいません…
Jan 820K450  
Jan 8  
20K  
450  
In  
Quantum Information Review  
by  
Shubhransh Rai  
1月820K450  
1月8日  
20K  
450  
『Quantum Information Review』にて  
著者：Shubhransh Rai  



## A Tech Tsunami is Coming Very Soon.. 技術の津波が非常に近づいています..

### If you think technology is moving fast now, you haven’t seen anything yet. 
現在、技術が速く進んでいると思うなら、まだ何も見ていません。



## The Top 7 MCP-Supported AI Frameworks トップ7のMCPサポートAIフレームワーク

### Create AI apps with Python and Typescript frameworks that leverage MCP servers to provide context to LLMs. 
### PythonおよびTypescriptフレームワークを使用して、MCPサーバーを活用しLLMsにコンテキストを提供するAIアプリを作成します。

6d ago64116  
6日前64116

641  
641

16  
16

In  
に

Everyday AI  
Everyday AI

by  
著者

Manpreet Singh  
Manpreet Singh



## Craziest MCP Servers You Must Try クレイジーなMCPサーバーを試すべき理由

### I remember when I first heard about MCP (Model Context Protocol). 
MCP（モデルコンテキストプロトコル）について初めて聞いたときのことを思い出します。



## Cursor, “vibe coding,” and Manus: the UX revolution that AI needs  
### It’s time to move past the command-line era of AI.  
## カーソル、「バイブコーディング」、およびマナス：AIが必要とするUX革命  
### AIのコマンドライン時代を超える時が来た。  
6d ago4399  
6日前4399  
439  
9  
Help  
ヘルプ  
Status  
ステータス  
About  
概要  
Careers  
キャリア  
Press  
プレス  
Blog  
ブログ  
Privacy  
プライバシー  
Rules  
ルール  
Terms  
利用規約  
Text to speech  
テキスト読み上げ  
