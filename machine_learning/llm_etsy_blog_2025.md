refs: https://www.etsy.com/codeascraft/building-etsy-buyer-profiles-with-llms

- メモ: 
  - このブログの取り組みを一言で言うと「ユーザ行動ログ → LLM → 構造化された"意味的ユーザ特徴"」


# Building Etsy Buyer Profiles with LLMs

By Isobel Scott
2025/09/03

# LLMを用いたEtsyバイヤープロファイルの構築
著者: イザベル・スコット
2025年9月3日

Every day, shoppers from Etsy's community of nearly 90M buyers visit our marketplace to search for unique, handmade, and vintage items. 
毎日、Etsyの約9000万人のバイヤーコミュニティからの買い物客が、ユニークで手作りのビンテージアイテムを探すために私たちのマーケットプレイスを訪れます。
But with over 100 million listings, how do we help each buyer find exactly what they're looking for? 
しかし、1億以上のリストがある中で、どのようにして各バイヤーが正確に探しているものを見つける手助けをするのでしょうか？
Traditional search and recommendation systems often fall short of capturing the nuanced interests that make each Etsy buyer unique, from specific styles to aesthetic preferences. 
従来の検索および推薦システムは、特定のスタイルや美的嗜好から、各Etsyバイヤーをユニークにする微妙な興味を捉えることがしばしば不足しています。
At Etsy, understanding our buyers' interests is central to delivering engaging, personalized experiences. 
**Etsyでは、バイヤーの興味を理解することが、魅力的でパーソナライズされた体験を提供するための中心的な要素**です。

<!-- ここまで読んだ! -->

Recently, we explored enhancing our personalization by leveraging large language models (LLMs) to create detailed buyer profiles based on buyers’ browsing and purchasing behaviors. 
最近、私たちは、バイヤーの閲覧および購入行動に基づいて詳細なバイヤープロファイルを作成するために、大規模言語モデル（LLMs）を活用してパーソナライズを強化することを探求しました。

We strive towards privacy by design and build these exploratory models with buyer privacy in mind. 
私たちはプライバシーを設計の段階から重視し、バイヤーのプライバシーを考慮してこれらの探索的モデルを構築しています。

While this work is still in experimentation, we’re excited to share our early efforts and what we’ve learned. 
この作業はまだ実験段階ですが、私たちは初期の取り組みと学んだことを共有できることに興奮しています。

# Understanding Buyer Profiles
# バイヤープロファイルの理解

Buyer profiles anonymously capture nuanced interests for each user, like preferred styles and product categories. 
バイヤープロファイルは、好ましいスタイルや製品カテゴリなど、各ユーザーの微妙な興味を匿名で捉えます。

For example, do they tend to prefer minimalist styles? 
例えば、彼らはミニマリストスタイルを好む傾向がありますか？

Do they mostly shop for home decor, or jewelry? 
彼らは主にホームデコやジュエリーを購入しますか？

They also offer insight into specific shopping missions a buyer may be on, like finding the perfect fall sweater. 
これらは、バイヤーが特定のショッピングミッション（例えば、完璧な秋のセーターを見つけること）に取り組んでいることについての洞察も提供します。

These profiles help us better understand our users, making the Etsy experience feel tailored to each individual buyer. 
これらのプロファイルは、私たちがユーザーをよりよく理解するのに役立ち、Etsyの体験を各バイヤーに合わせたものに感じさせます。

# Technical Implementation
# 技術的実装

Our process begins by retrieving user activity data and listing information from internal sources like our feature store and BigQuery. 
私たちのプロセスは、機能ストアやBigQueryなどの内部ソースからユーザーの活動データとリスト情報を取得することから始まります。

This includes users’ recent searches, item views, purchases, and favorites. 
これには、ユーザーの最近の検索、アイテムの閲覧、購入、お気に入りが含まれます。

Once we have the users’ session data with interactions, we then prompt the LLM to interpret this data and generate structured buyer profiles. 
ユーザーのインタラクションを含むセッションデータを取得したら、LLMにこのデータを解釈させ、構造化されたバイヤープロファイルを生成するように促します。

In the case that the LLM does not have enough supporting data to infer a user's categorical interests (i.e. these interests would also not be obvious to a human looking at this user's interactions), these fields and the confidence hashmap can be empty. 
LLMがユーザーのカテゴリカルな興味を推測するための十分なサポートデータを持っていない場合（つまり、これらの興味はこのユーザーのインタラクションを見ている人間にも明らかではない）、これらのフィールドと信頼度ハッシュマップは空になる可能性があります。

The LLM will always include an explanation and any observed interests in the explanation section of the buyer profile. 
LLMは常に説明とバイヤープロファイルの説明セクションに観察された興味を含めます。

# Bringing Personalization to Scale
# パーソナライズをスケールする

Initially, using this method to generate profiles for our roughly 90 million buyers would have been exceedingly costly and taken weeks to update. 
最初は、この方法を使用して約9000万人のバイヤーのプロファイルを生成することは非常に高額で、更新に数週間かかるものでした。

We optimized this by: 
私たちはこれを最適化しました：

- Shifting our listings data source from API endpoints to BigQuery tables that are clustered and partitioned for efficient querying. 
- リストデータソースをAPIエンドポイントから、効率的なクエリのためにクラスタリングおよびパーティション化されたBigQueryテーブルに移行しました。

- Decreasing the volume of input tokens. 
- 入力トークンの量を減少させました。

Initially, we were including about 2 years of session data. 
最初は約2年分のセッションデータを含めていました。

Now, we’ve reduced this to just the last 9 months. 
現在、これを過去9ヶ月分に減らしました。

The 9 month timeframe also allowed us to lighten the prompt corrections (and cached input tokens) by reducing the weight of holiday shopping. 
9ヶ月の期間は、ホリデーショッピングの重みを減らすことで、プロンプトの修正（およびキャッシュされた入力トークン）を軽減することも可能にしました。

- Increasing LLM and BigQuery batch sizes for data processing. 
- データ処理のためにLLMとBigQueryのバッチサイズを増加させました。

- Introducing parallel processing with managed concurrency to avoid request rate limits. 
- リクエストレート制限を回避するために、管理された同時実行で並列処理を導入しました。

- Scaling up computational resources for session data retrieval and LLM processing tasks. 
- セッションデータの取得とLLM処理タスクのために計算リソースを拡大しました。

These improvements reduced buyer profile generation time dramatically — from 21 days down to 3 days for 10 million users. 
これらの改善により、バイヤープロファイルの生成時間が劇的に短縮されました — 1000万人のユーザーに対して21日から3日へと。

Cost management was also crucial. 
コスト管理も重要でした。

By adjusting the prompt to get high quality results with a smaller model, we significantly lowered the cost and made large-scale personalization economically feasible. 
プロンプトを調整して小さなモデルで高品質の結果を得ることで、コストを大幅に削減し、大規模なパーソナライズを経済的に実現可能にしました。

Through these various cost management techniques, we were able to reduce the estimated cost by 94% per million users. 
これらのさまざまなコスト管理技術を通じて、私たちは推定コストを100万人あたり94%削減することができました。

Additionally, to scale and schedule buyer profile refreshes, we used Airflow as an orchestration tool. 
さらに、バイヤープロファイルのリフレッシュをスケールし、スケジュールするために、Airflowをオーケストレーションツールとして使用しました。

By batching and staggering tasks by user_id, we parallelize some tasks while avoiding too many concurrent requests on BigQuery & OpenAI APIs (as visualized in this Directed Acyclic Graph). 
ユーザーIDによってタスクをバッチ処理および段階的に実行することで、いくつかのタスクを並列化し、BigQueryおよびOpenAI APIへの同時リクエストが多すぎないようにしました（この有向非巡回グラフで視覚化されています）。

# Experiments and Applications
# 実験と応用

With these powerful insights in hand, we’ve started to explore several key applications of buyer profiles that would make the Etsy search experience feel unique to each shopper. 
これらの強力な洞察を手に入れたことで、私たちはEtsyの検索体験を各買い物客にユニークに感じさせるバイヤープロファイルのいくつかの重要な応用を探求し始めました。



## Query Rewriting クエリの書き換え

Query rewriting is the process of transforming a user’s submitted search query on the backend to better represent their intent to the underlying search systems. 
クエリの書き換えは、ユーザが提出した検索クエリをバックエンドで変換し、基盤となる検索システムに対する意図をよりよく表現するプロセスです。
We already use query rewriting for different use cases at Etsy. 
私たちはすでにEtsyでさまざまなユースケースのためにクエリの書き換えを使用しています。
It can correct spelling, add specifics to ambiguous queries, adjust niche terminology, or complete incomplete queries (where the user accidentally pressed enter before they finished writing their query). 
それは、スペルを修正したり、あいまいなクエリに具体性を追加したり、ニッチな用語を調整したり、未完成のクエリ（ユーザがクエリの入力を終える前に誤ってEnterを押した場合）を完成させたりすることができます。

To further personalize Etsy’s search experience, we explored enriching search queries with predicted interests from buyer profiles. 
Etsyの検索体験をさらにパーソナライズするために、私たちはバイヤープロファイルから予測された興味を用いて検索クエリを豊かにすることを探求しました。
For instance, a simple query like "cool posters" becomes "cool posters + hippie|boho|vintage|nature," significantly boosting relevance. 
例えば、「cool posters」というシンプルなクエリは「cool posters + hippie|boho|vintage|nature」に変わり、関連性が大幅に向上します。

### Search results without personalization パーソナライズなしの検索結果
### Search results with personalization using example buyer profile パーソナライズされた検索結果（例のバイヤープロファイルを使用）



## Refinement Pills 改良ピル

On the Etsy website, “refinement pills” work as an interactive query reformulation. 
Etsyのウェブサイトでは、「改良ピル」はインタラクティブなクエリ再構成として機能します。
When a user clicks on an option, the path will be prefixed to the user’s query and a new search will be executed. 
ユーザーがオプションをクリックすると、そのパスがユーザーのクエリの前に追加され、新しい検索が実行されます。
A mix of different types of refinement pills are generated: single pills (just one word) and grouped pills (a dropdown of options). 
さまざまなタイプの改良ピルが生成されます：単一ピル（単語1つ）とグループ化されたピル（オプションのドロップダウン）。
With buyer profiles, we can present high-confidence buyer interests as clickable filters or refinement pills in the search interface, enabling users to effortlessly refine their searches based on predicted preferences. 
バイヤープロファイルを使用することで、高い信頼性のあるバイヤーの興味をクリック可能なフィルターや改良ピルとして検索インターフェースに表示でき、ユーザーは予測された好みに基づいて検索を簡単に絞り込むことができます。

### Refinement pills without personalization パーソナライズなしの改良ピル
### Refinement pills with personalization using example buyer profile パーソナライズを使用した改良ピルの例

For example, if a user clicks on a “daisy” refinement pill as in the example below, the search query "car accessories" would be reformulated to "daisy car accessories" and the new, more specific search will be executed. 
例えば、ユーザーが以下の例のように「デイジー」改良ピルをクリックすると、検索クエリ「カーアクセサリー」は「デイジーカーアクセサリー」に再構成され、新しい、より具体的な検索が実行されます。

# Measuring Success 成功の測定



## Validating Profile Accuracy プロファイル精度の検証

As we work to roll out buyer profile-based personalization, understanding the accuracy of our predictions is crucial. 
バイヤープロファイルに基づくパーソナライズを展開するにあたり、私たちの予測の精度を理解することは重要です。
Through systematic experimentation, we're working to establish how well our LLM-generated profiles reflect actual user interests and shopping behaviors.
体系的な実験を通じて、私たちはLLM生成プロファイルが実際のユーザーの興味や購買行動をどの程度反映しているかを確立しようとしています。



## Key Accuracy Metrics 主要な精度指標

- Click-through Rate (CTR) Lift: Comparing CTR on personalized search results versus baseline helps us quantify immediate engagement improvements
- クリック率（CTR）リフト：パーソナライズされた検索結果とベースラインのCTRを比較することで、即時のエンゲージメントの改善を定量化するのに役立ちます。

- Conversion Rate Impact: Tracking purchase rates from personalized searches reveals whether we're surfacing items users actually want to buy
- コンバージョン率の影響：パーソナライズされた検索からの購入率を追跡することで、ユーザーが実際に購入したいアイテムを表示できているかどうかが明らかになります。

- Refinement Pill Engagement: Monitoring clicks on suggested refinement pills helps measure how well we've predicted user interests
- リファインメントピルエンゲージメント：提案されたリファインメントピルのクリックを監視することで、ユーザーの興味をどれだけうまく予測できたかを測定するのに役立ちます。

- Search Query Reformulation Success: Analyzing subsequent user actions after query rewriting indicates whether our enrichments align with user intent
- 検索クエリの再定式化の成功：クエリの書き換え後のユーザーの行動を分析することで、私たちの強化がユーザーの意図と一致しているかどうかを示します。



## Profile Refresh Strategy プロファイル更新戦略

We'll work to maintain profile accuracy through several methods:
私たちは、いくつかの方法を通じてプロファイルの正確性を維持するために取り組みます：
- Dynamically refreshing timing based on user activity levels. 
- ユーザの活動レベルに基づいて動的に更新タイミングを調整します。これには、最近のインタラクションの数と頻度が含まれます。例えば、ユーザは提案されたリファインメントピルをクリックしますか？パーソナライズされたアイテムは表示されていますか？
- Detecting interest drift when search patterns change significantly
- 検索パターンが大きく変化したときの興味の漂流を検出します。
- Taking into account seasonal considerations, such as the winter holiday shopping season
- 冬のホリデーショッピングシーズンなどの季節的な考慮事項を考慮します。
- Monitoring performance degradation signals when personalization effectiveness drops below thresholds of engagement listed above
- 上記のエンゲージメントのしきい値を下回ったときに、パーソナライズの効果が低下している信号を監視します。

# Future Work 今後の作業



## The Cold Start User Problem コールドスタートユーザ問題

To extend this personalized experience to new users who lack extensive session data, we experimented with "inheritance profiles" using collaborative filtering. 
新しいユーザに対して、広範なセッションデータが不足している場合でもこのパーソナライズされた体験を拡張するために、私たちはコラボレーティブフィルタリングを使用して「継承プロファイル」を実験しました。

By matching early interaction signals (like brief session data or initial search terms) to existing profiles of similar users, we could predict interests for new users earlier in their relationship with Etsy. 
初期のインタラクション信号（短いセッションデータや初期の検索用語など）を類似ユーザの既存プロファイルにマッチさせることで、新しいユーザのEtsyとの関係の初期段階での興味を予測することができました。

This user-based collaborative filtering approach would allow us to have profiles for as many users as possible, even those with minimal behavioral data. 
このユーザベースのコラボレーティブフィルタリングアプローチにより、最小限の行動データしか持たないユーザを含め、できるだけ多くのユーザのプロファイルを持つことが可能になります。

Below is a diagram for a sample new user who might inherit aspects of a similar profile as the one above, based on just a few searches. 
以下は、いくつかの検索に基づいて上記の類似プロファイルの側面を継承する可能性のあるサンプル新ユーザの図です。

# Conclusion 結論

As we continue to refine these profiles and expand their applications across the Etsy marketplace, we're excited about the possibilities, from more intuitive search experiences to discovery features that surface hidden gems aligned with each buyer's unique tastes. 
これらのプロファイルを洗練させ、Etsyマーケットプレイス全体での応用を拡大し続ける中で、私たちは、より直感的な検索体験から、各バイヤーのユニークな嗜好に合った隠れた宝石を浮き彫りにする発見機能まで、可能性にワクワクしています。

With nearly 90 million active buyers and over 100 million listings, the challenge of personalization at Etsy's scale is immense, but that's exactly what makes it worth solving. 
約9000万人のアクティブバイヤーと1億以上のリスティングを持つEtsyの規模におけるパーソナライズの課題は膨大ですが、それこそが解決する価値がある理由です。

Every improvement we make impacts millions of shopping journeys, helping buyers discover that perfect vintage find, custom wedding gift, or miniature dragon they didn't even know they were looking for. 
私たちが行うすべての改善は、何百万ものショッピングジャーニーに影響を与え、バイヤーが完璧なヴィンテージアイテム、カスタムウェディングギフト、または自分が探していることすら知らなかったミニチュアドラゴンを発見する手助けをします。

# Acknowledgements 謝辞

Huge thanks to Orson Adams, David Blincoe, Jugal Gala, Davis Kim, Haoming Chen, Yinlin Fu, Julia Zhou, and the entire Search Mission Understanding team for their invaluable support and guidance. 
オーソン・アダムス、デイビッド・ブリンコ、ジュガル・ガラ、デイビス・キム、ハオミン・チェン、インリン・フー、ジュリア・ジョウ、そしてSearch Mission Understandingチーム全体の貴重なサポートと指導に心から感謝します。
