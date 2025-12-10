refs: https://medium.com/pinterest-engineering/identify-user-journeys-at-pinterest-b517f6275b42

# Identify User Journeys at Pinterest Pinterestにおけるユーザージャーニーの特定

Pinterest EngineeringFollow
Pinterest Engineering
Follow
Follow
8 min read·Oct 22, 2025
8分で読めます·2025年10月22日

Lin Zhu | シニアスタッフ機械学習エンジニア、Jaewon Yang | プリンシパル機械学習エンジニア、Ravi Kiran Holur Vijay | 機械学習エンジニアリングディレクター

Pinterest has always been a go-to destination for inspiration, a place where users explore everything from daily meal ideas to major life events like planning a wedding or renovating a home. 
Pinterestは常にインスピレーションのための行き先であり、ユーザーが日々の食事のアイデアから、結婚式の計画や家の改装といった大きなライフイベントまで、さまざまなことを探求する場所です。
Our core mission is to be an inspiration-to-realization platform. 
私たちのコアミッションは、インスピレーションから実現へとつなげるプラットフォームになることです。
To fulfill this, we recognized a critical challenge: we needed to move beyond understanding immediate interests and comprehend the underlying, long-term goals of our users. 
これを実現するために、私たちは**重要な課題を認識しました。それは、即時の興味を理解することを超えて、ユーザーの根底にある長期的な目標を理解する必要があるということ**です。
Therefore, we introduce user journeys as the foundation for recommendations. 
したがって、私たちはユーザージャーニーを推薦の基盤として導入します。

- メモ: Pinterestにおける「User Journey (ユーザージャーニー)」の定義
  - 定義と概念:
    - 特定の時点における「興味(interest)」、「意図(intent)」、「コンテキスト(context)」の交差点。
    - これは単なる一時的な興味の把握を超えて、ユーザの根本的な長期的目標を理解するためのもの。
  - 主な特徴:
    - 構成要素:
      - 特定の興味を中心とした一連のinteractions(検索, 保存,etc.)で構成され、「スタイルの探索」や「購入」などの明確な意図を含む。
    - 同時並行:
      - ある1ユーザは、複数の重複するジャーニーを同時に進行させることがある。
    - 分類:
      - 常にアクティブな「Evergreen Journey」と、特定の機関で完結する「Situational Journey」に分類される。
      - さらに、進行中か終了したかのステージ判定も行われる。
  - 技術的な仕組み:
    - 抽出方法:
      - ユーザの検索履歴や活動履歴からキーワードを抽出し、階層的クラスタリングを用いてジャーニー候補を生成する。
    - 出力:
      - 各ジャーニーは、簡潔な「ジャーニー名」、関連する「キーワード」、現在の「ステージ(ex. 進行中/終了)」、および「信頼度スコア」として出力される。
    - LLMの活用:
      - ジャーニーの命名や、将来的には推論プロセス全体(抽出、クラスタリング、ステージ予測など)の統合にLLMの活用が進められてる。
  - 効果:
    - 従来の興味ベースの通知と比較して、ジャーニーを意識した通知（Journey-Aware Notifications）は、メールのクリック率が88%、プッシュ通知の開封率が32%向上するなど、ユーザーエンゲージメントに大きな成果を上げている。
    - 例えるなら...
      - 従来の推薦が「過去に一度見た商品をランダムに勧めてくる店員」だとすれば、User Journeyを活用した推薦は「お客様が『結婚式の準備』というプロジェクトを進めていることを理解し、今が『ドレス選び』の段階なのか『会場装飾』の段階なのかを把握した上で、適切な提案をしてくれる専属コンシェルジュ」のような存在と言える。

We define a journey as the intersection of a user’s interests, intent, and context at a specific point in time. 
私たちは、ジャーニーを特定の時点におけるユーザーの興味、意図、コンテキストの交差点として定義します。
A user journey is a sequence of user-item interactions, often spanning multiple sessions, that centers on a particular interest and reveals a clear intent — such as exploring trends or making a purchase. 
ユーザージャーニーは、特定の興味に焦点を当て、トレンドを探求したり購入を行ったりする明確な意図を明らかにする、複数のセッションにわたるユーザーとアイテムの相互作用の連続です。

For example, a journey might involve an interest in “summer dresses,” an intent to “learn what’s in style,” and a context of being “ready to buy.” 
例えば、ジャーニーは「夏のドレス」に対する興味、「流行を学ぶ」という意図、そして「購入の準備ができている」というコンテキストを含むかもしれません。

Users can have multiple, sometimes overlapping, journeys occurring simultaneously as their interests and goals evolve. 
ユーザーは、興味や目標が進化する中で、同時に複数の、時には重複するジャーニーを持つことができます。



## Get Pinterest Engineering’s stories in your inbox

Join Medium for free to get updates from this writer.
Pinterest Engineeringのストーリーをあなたの受信箱に届けるために、Mediumに無料で参加して、この作家からの更新を受け取りましょう。

Inferring user journeys goes beyond understanding immediate interests, it allows us to comprehend the underlying, long-term goals of our users. 
ユーザージャーニーを推測することは、即時の興味を理解することを超え、ユーザーの根底にある長期的な目標を理解することを可能にします。

By identifying user journeys, we can move from simple content recommendations to becoming a platform that assists users in achieving their goals, whether it’s planning a wedding, renovating a kitchen, or learning a new skill. 
ユーザージャーニーを特定することで、私たちは単純なコンテンツ推薦から、結婚式の計画、キッチンの改装、新しいスキルの習得など、ユーザーが目標を達成するのを支援するプラットフォームへと移行できます。

This aligns with Pinterest’s mission to be an inspiration-to-realization platform, and provides the foundation for journey-aware recommendations. 
これは、Pinterestの「インスピレーションから実現へ」という使命と一致し、ジャーニーを意識した推薦の基盤を提供します。

Press enter or click to view image in full size
画像をフルサイズで表示するには、Enterキーを押すかクリックしてください。



## Our Solution Philosophy 私たちの解決策の哲学

From the outset, we knew we were building a new product without large amounts of training data. 
最初から、私たちは大量のトレーニングデータなしで新しい製品を構築していることを認識していました。この制約は、このプロジェクトのエンジニアリング哲学を形作りました：

- Be Lean:Minimize the development of new components where no data exists.  
- スリムであること：データが存在しない場所で新しいコンポーネントの開発を最小限に抑えます。

- Start Small:Begin with a small, high-quality dataset of a few hundred human-annotated examples.  
- 小さく始める：数百の人間によって注釈された例からなる小さく高品質なデータセットで始めます。

- Leverage Foundation Models:Utilize pretrained models, like pretrainedSearchSagefor keyword embeddings, to maximize cost efficiency and effectiveness.  
- 基盤モデルを活用する：キーワード埋め込みのためのpretrainedSearchSageのような事前学習モデルを利用して、コスト効率と効果を最大化します。

- Make it Extensible:Design a system that supports more complex models as we collect more data, with a clear path to incorporating more advanced ML and LLM techniques.  
- 拡張可能にする：データを収集するにつれて、より複雑なモデルをサポートするシステムを設計し、より高度なMLおよびLLM技術を組み込む明確な道筋を持たせます。



## System Architecture: A Walkthrough システムアーキテクチャ: 概要

To identify these journeys, we evaluated two primary approaches: 
これらの旅を特定するために、私たちは2つの主要なアプローチを評価しました。

1. Predefined Journey Taxonomy: Building a fixed set of journeys and mapping users to them. 
1. 事前定義された旅の分類: 固定された旅のセットを構築し、ユーザをそれにマッピングします。

While this offers consistency, it risks overlapping with existing systems, requiring significant maintenance, and being slow to adapt to new trends. 
これは一貫性を提供しますが、既存のシステムと重複するリスクがあり、重要なメンテナンスが必要で、新しいトレンドに適応するのが遅くなります。

2. Dynamic Keyword Extraction: Directly extracting journeys from a user’s activities, representing each journey as a cluster of keywords (queries, annotations, interests, etc.). 
2. 動的キーワード抽出: ユーザの活動から直接旅を抽出し、各旅をキーワードのクラスター（クエリ、注釈、興味など）として表現します。

We chose the Dynamic Extraction approach to generate journeys based on the user’s information. 
私たちは、ユーザの情報に基づいて旅を生成するために動的抽出アプローチを選びました。

It offered greater flexibility, personalization, and adaptability, allowing the system to respond to emerging trends and unique user behaviors. 
このアプローチは、より大きな柔軟性、パーソナライズ、適応性を提供し、システムが新たなトレンドやユニークなユーザの行動に応じることを可能にしました。

This method also allowed us to leverage existing infrastructure and simplify the modeling process by focusing on clustering activities for individual users. 
この方法は、既存のインフラを活用し、個々のユーザの活動をクラスタリングすることに焦点を当てることで、モデリングプロセスを簡素化することも可能にしました。

At a high level, we extract keywords from multiple sources and employ hierarchical clustering to generate keyword clusters; each cluster is a journey candidate. 
高いレベルでは、私たちは複数のソースからキーワードを抽出し、階層的クラスタリングを用いてキーワードクラスターを生成します; 各クラスターは旅の候補です。

We then build specialized models for journey ranking, stage prediction, naming, and expansion. 
次に、旅のランキング、ステージ予測、命名、拡張のための専門モデルを構築します。

This inference pipeline runs on a streaming system, allowing us to run full inference if there’s algorithm change, or daily incremental inference for recent active users so the journeys respond quickly to a user’s most recent activities. 
この推論パイプラインはストリーミングシステム上で動作し、アルゴリズムの変更があった場合には完全な推論を実行したり、最近のアクティブユーザに対して日次の増分推論を実行することができるため、旅はユーザの最近の活動に迅速に応答します。

Let’s break down the key components of this innovative system: 
この革新的なシステムの主要なコンポーネントを分解してみましょう:



## 1. User Journey Extraction and Clustering ユーザージャーニーの抽出とクラスタリング

This foundational component is designed to generate fresh, personalized journeys for each user.
この基盤コンポーネントは、各ユーザーのために新鮮でパーソナライズされたジャーニーを生成するように設計されています。

- Input Data: We leverage a rich set of user data, including:
- 入力データ：私たちは、以下を含む豊富なユーザーデータセットを活用します：
  — User search history: Aggregated queries and timestamps.
  — ユーザー検索履歴：集約されたクエリとタイムスタンプ。
  — User activity history: Interactions like Pin closeups, repins, and clickthroughs, extract the annotations and interests from the engaged Pins.
  — ユーザー活動履歴：Pinのクローズアップ、再ピン、クリックスルーなどのインタラクションから、関与したPinsの注釈と興味を抽出します。
  — User’s boards: Extract the annotations and interests from the Pins in the user’s boards.
  — ユーザーのボード：ユーザーのボード内のPinsから注釈と興味を抽出します。

- User Journey Clustering: We treat all the queries, annotations, and interests as keywords with metadata.
- ユーザージャーニークラスタリング：私たちは、すべてのクエリ、注釈、および興味をメタデータを持つキーワードとして扱います。
Then we adopt the pretrained text embedding for the keywords to perform hierarchical clustering to form journey clusters.
次に、キーワードに対して事前学習されたテキスト埋め込みを採用し、階層的クラスタリングを実行してジャーニークラスタを形成します。



## 2. Journey Naming & Expansion 旅の命名と拡張

Clear and intuitive journey names are crucial for user experience.  
明確で直感的な旅の名前は、ユーザー体験にとって重要です。

- Journey Naming: The current production model is to apply a ranking model to pick the top keyword extracted from each cluster as the journey name.  
- 旅の命名：現在の生産モデルは、各クラスターから抽出された上位キーワードを旅の名前として選ぶためにランキングモデルを適用することです。  
It balances personalization and simplicity by choosing the most relevant keywords from the cluster.  
これは、クラスターから最も関連性の高いキーワードを選ぶことで、パーソナライズとシンプルさのバランスを取ります。  
We are working with scaling LLM for Journey Name Generation, which promises highly personalized and adaptable names.  
私たちは、非常にパーソナライズされ適応可能な名前を約束する旅の名前生成のために、LLMのスケーリングに取り組んでいます。

- Journey Expansion: We leverage LLMs to generate new journey recommendations based on a user’s past or ongoing journeys, with an emphasis on balancing the predictive power of LLMs and efficiently serving through pre-generated recommendations.  
- 旅の拡張：私たちは、ユーザーの過去または進行中の旅に基づいて新しい旅の推奨を生成するためにLLMを活用し、LLMの予測力と事前生成された推奨を効率的に提供することのバランスを重視しています。  
In the initial stage, we focus on creating non-personalized, related journeys based on a given input journey.  
初期段階では、与えられた入力旅に基づいて非パーソナライズされた関連旅の作成に焦点を当てています。  
Since the total number of journeys is limited, we can use LLMs to generate this data offline and store it in a key-value store.  
旅の総数が限られているため、私たちはLLMを使用してこのデータをオフラインで生成し、キー・バリュー・ストアに保存することができます。  
For personalized recommendations, we will apply the journey ranking model online to rank related journeys for each user.  
パーソナライズされた推奨のために、私たちはオンラインで旅のランキングモデルを適用し、各ユーザーに関連する旅をランク付けします。



## 3. Journey Ranking & Diversification 旅のランキングと多様化

To ensure the most relevant journeys are presented, and to prevent monotony, we built a ranking model and applied diversification afterwards.
最も関連性の高い旅が提示され、単調さを防ぐために、私たちはランキングモデルを構築し、その後に多様化を適用しました。



## Journey Ranking ジャーニーランキング

Similar to traditional ranking problems, our initial approach is to build a point-wise ranking model. 
従来のランキング問題と同様に、私たちの初期のアプローチはポイントワイズランキングモデルを構築することです。

We get labels from user email feedback and human annotation. 
私たちは、ユーザのメールフィードバックと人間の注釈からラベルを取得します。

The model takes user features, engagement features (how frequently the user engaged on this journey through search, actions on Pins, etc.) and recency features. 
このモデルは、ユーザの特徴、エンゲージメント特徴（ユーザがこのジャーニーにどれだけ頻繁に関与したか、検索やピンに対するアクションなど）および新しさの特徴を考慮します。

This provides a simple, immediate baseline. 
これにより、シンプルで即時的なベースラインが提供されます。



## Journey Diversification 旅程の多様化

To prevent the top ranked journeys from always being similar, we implement a diversifier after the journey ranking stage. 
上位にランク付けされた旅程が常に似たようなものであるのを防ぐために、旅程のランク付け段階の後に多様化機能を実装します。

The most straightforward approach is to apply a penalty if the journey is similar to the journeys that ranked higher (the similarity is measured using pretrained keyword embedding). 
最も簡単なアプローチは、旅程が上位にランク付けされた旅程と似ている場合にペナルティを適用することです（類似性は事前学習されたキーワード埋め込みを使用して測定されます）。

For each journey i, score will be updated based on the formula below. 
各旅程 $i$ に対して、スコアは以下の式に基づいて更新されます。

Finally, we re-rank the journeys according to the updated score. 
最後に、更新されたスコアに基づいて旅程を再ランク付けします。

Occurrence is the number of similar journeys ranked before the current journey, and penalty is a hyperparameter to tune, usually chosen as 0.95. 
Occurrenceは現在の旅程の前にランク付けされた類似の旅程の数であり、penaltyは調整するハイパーパラメータで、通常は0.95に設定されます。



## 4. Journey Stage Prediction 旅の段階予測

Understanding a journey’s lifecycle helps us determine appropriate notification timing. 
旅のライフサイクルを理解することで、適切な通知のタイミングを決定するのに役立ちます。 
We simplify this into two objectives: 
これを二つの目的に簡略化します：

- Situational vs. Evergreen Classification: Journeys are categorized based on user engagement patterns and activity duration. 
- 状況別分類とエバーグリーン分類：旅はユーザのエンゲージメントパターンと活動の持続時間に基づいて分類されます。 
If users engage with a journey consistently over an extended period, we classify it as “Evergreen” — these journeys remain perpetually active. 
ユーザが長期間にわたって旅に一貫して関与する場合、それを「エバーグリーン」と分類します。これらの旅は常にアクティブな状態を保ちます。 
In contrast, journeys with engagement limited to a shorter timeframe are classified as “Situational,” as they are expected to conclude at a certain point. 
対照的に、短期間に限られたエンゲージメントを持つ旅は「状況別」と分類されます。これらは特定の時点で終了することが期待されます。

- Journey Stage (Ongoing vs. Ended) Classification: For situational journeys, we evaluate whether the journey is still ongoing or has ended, primarily by analyzing the time since the user’s last engagement. 
- 旅の段階（進行中 vs. 終了）分類：状況別の旅について、私たちはその旅がまだ進行中であるか、終了したかを評価します。主にユーザの最後のエンゲージメントからの時間を分析することによって行います。 
Future improvements will include incorporating user feedback and developing a supervised model for more accurate classification. 
今後の改善には、ユーザのフィードバックを取り入れ、より正確な分類のための教師ありモデルを開発することが含まれます。



## 5. User Journeys Output ユーザージャーニーの出力

The user journeys could be used in downstream applications for retrieval and ranking. 
ユーザージャーニーは、取得およびランキングのための下流アプリケーションで使用される可能性があります。

The desired output is a list of distinct user journeys. 
望ましい出力は、異なるユーザージャーニーのリストです。

Each journey should ideally be represented with: 
各ジャーニーは理想的には以下のように表現されるべきです：

- Journey Name: A concise and descriptive name (e.g., “Kitchen Renovation,” “Improving Home Organization,” “Engagement Ring Selection”). 
- ジャーニー名：簡潔で説明的な名前（例：「キッチンリノベーション」、「家庭の整理改善」、「婚約指輪の選択」）。

- Keywords: List of keywords related to this journey; it could be the corresponding interests, annotations, queries, or any keywords. 
- キーワード：このジャーニーに関連するキーワードのリスト；それは対応する興味、注釈、クエリ、または任意のキーワードである可能性があります。

- Stage: An indicator of where the user is within that journey (e.g., “inspiration,” “action”); we simplified it to “ongoing” or “ended” in the initial launch. 
- ステージ：ユーザーがそのジャーニーの中でどこにいるかを示す指標（例：「インスピレーション」、「アクション」）；私たちは、初期のローンチで「進行中」または「終了」に簡略化しました。

Confidence Score: The confidence score for this predicted journey. 
信頼度スコア：この予測されたジャーニーの信頼度スコアです。



## 6. Relevance Evaluation 関連性評価

We aim to establish a robust evaluation and monitoring pipeline to ensure consistent and reliable quality assessment of top-k user journey predictions. 
私たちは、トップkのユーザージャーニー予測の一貫した信頼性のある品質評価を確保するために、堅牢な評価および監視パイプラインを確立することを目指しています。
Because human evaluation is costly and sometimes inconsistent, we leverage LLMs to assess the relevance of predicted user journeys. 
人間による評価はコストがかかり、時には一貫性がないため、私たちはLLMs（大規模言語モデル）を活用して予測されたユーザージャーニーの関連性を評価します。
By providing user features and engagement history, we ask the LLM to generate a 5-level score with explanations. 
ユーザの特徴とエンゲージメント履歴を提供することで、LLMに5段階のスコアとその説明を生成するよう依頼します。
We have validated that LLM judgments closely correlate with human assessments in our use case, giving us confidence in this approach. 
私たちは、LLMの判断が私たちのユースケースにおける人間の評価と密接に相関していることを確認しており、このアプローチに自信を持っています。



## Experiment Results 実験結果

We applied user journeys inference to deliver notifications related to the user’s ongoing journeys. 
私たちは、ユーザージャーニー推論を適用して、ユーザーの進行中のジャーニーに関連する通知を提供しました。
Our initial experiments demonstrate the significant impact of Journey-Aware Notifications¹:
私たちの初期実験は、ジャーニー対応通知の重要な影響を示しています¹：
- The system drove statistically significant gains in user engagements.
- システムは、ユーザーエンゲージメントにおいて統計的に有意な向上をもたらしました。
- Compared to our existing interest-based notifications, journey-aware notifications demonstrated an 88% higher email click rate and a 32% higher push open rate.
- 既存の興味ベースの通知と比較して、ジャーニー対応通知は88%高いメールクリック率と32%高いプッシュオープン率を示しました。
- User surveys revealed a 23% increase in positive feedback rate compared to interest-based notifications.
- ユーザー調査では、興味ベースの通知と比較して23%のポジティブフィードバック率の増加が明らかになりました。



## Ongoing Effort 進行中の取り組み

As a follow up, we are working on leveraging large language models (LLMs) to infer user journeys given user information and activities, while offering several key benefits:
その後、私たちはユーザー情報と活動に基づいてユーザーの旅を推測するために大規模言語モデル（LLMs）を活用する作業を進めており、いくつかの重要な利点を提供しています。
- Simplification: Many existing components of the journey inference system — including keyword extraction, clustering, journey naming, and stage prediction models — can be consolidated and replaced with a single LLM.
- 簡素化：旅推測システムの多くの既存コンポーネント（キーワード抽出、クラスタリング、旅の命名、ステージ予測モデルを含む）は、単一のLLMに統合され、置き換えられる可能性があります。
- Quality Improvement: By utilizing the advanced capabilities of LLMs to understand user behavior, we aim to significantly enhance the accuracy and quality of user journey predictions.
- 品質向上：ユーザーの行動を理解するためのLLMの高度な機能を活用することで、ユーザーの旅の予測の精度と品質を大幅に向上させることを目指しています。

We tuned our prompts and used GPT to generate ground truth labels for fine-tuning Qwen, enabling us to scale in-house LLM inference while maintaining competitive relevance.
私たちはプロンプトを調整し、GPTを使用してQwenのファインチューニングのためのグラウンドトゥルースラベルを生成し、競争力を維持しながら社内のLLM推論をスケールアップできるようにしました。

Next, we utilized Raybatch inference to improve the efficiency and scalability.
次に、Raybatch推論を利用して効率性とスケーラビリティを向上させました。

Finally, we are implementing full inference for all users and incremental inference for recently active users to reduce overall inference costs.
最後に、すべてのユーザーに対して完全な推論を実施し、最近アクティブなユーザーに対しては増分推論を行い、全体の推論コストを削減しています。

All generated journeys will go through safety checks to ensure they meet our safety standards.
生成されたすべての旅は、安全基準を満たしていることを確認するために安全チェックを受けます。



## Acknowledgement 謝辞

We’d like to thank Kevin Che, Justin Tran, Rui Liu, Anya Trivedi, Binghui Gong, Randy Tumalle, Tianqi Wang, Fangzheng Tian, Eric Tam, Manan Kalra, Mengtian Hu and Mengying Yang for their contribution!
私たちは、Kevin Che、Justin Tran、Rui Liu、Anya Trivedi、Binghui Gong、Randy Tumalle、Tianqi Wang、Fangzheng Tian、Eric Tam、Manan Kalra、Mengtian Hu、Mengying Yangの貢献に感謝します！

Thanks Jeanette Mukai, Darien Boyd, Samuel Owens, Justin Pangilinan, Blake Weber, Gloria Lee, Jess Adamiak for the product insights!
Jeanette Mukai、Darien Boyd、Samuel Owens、Justin Pangilinan、Blake Weber、Gloria Lee、Jess Adamiakに製品の洞察について感謝します！

Thanks Tingting Zhu, Shivani Rao, Dimitra Tsiaousi, Ye Tian, Vishwakarma Singh, Shipeng Yu, Rajat Raina and Randall Keller for the support!
Tingting Zhu、Shivani Rao、Dimitra Tsiaousi、Ye Tian、Vishwakarma Singh、Shipeng Yu、Rajat Raina、Randall Kellerのサポートに感謝します！

¹Pinterest Internal Data, USA, April-May 2025
¹Pinterest内部データ、アメリカ、2025年4月-5月



## Published in Pinterest Engineering Blog Pinterest Engineering Blogに掲載

Published in Pinterest Engineering Blog
Pinterest Engineering Blogに掲載

17K followers
17Kフォロワー

·
·

Nov 11, 2025
2025年11月11日

Inventive engineers building the first visual discovery engine, 300 billion ideas and counting.
発明的なエンジニアが初のビジュアルディスカバリーエンジンを構築し、3000億のアイデアを数えています。

Follow
フォロー
Follow
フォロー
Follow
フォロー
Follow
フォロー



## Written by Pinterest Engineering 著者: Pinterestエンジニアリング

Written by Pinterest Engineering
Pinterestエンジニアリングによって書かれました

60K followers
60Kフォロワー

·
·

https://medium.com/pinterest-engineering| Inventive engineers building the first visual discovery engine
https://medium.com/pinterest-engineering | 最初のビジュアルディスカバリーエンジンを構築する創造的なエンジニア

https://careers.pinterest.com/
https://careers.pinterest.com/
Follow
フォロー



## Responses (6) 返信 (6)

Write a response 返信を書く  
What are your thoughts? あなたの考えは？  
What are your thoughts? あなたの考えは？  
Pinsocial  
Nov 20 11月20日  
```
Great initiative! It’s always inspiring to see the engineering work that goes on behind the scenes. Kudos to the team for continuously pushing the algorithms forward and making the Pinterest experience smarter
素晴らしい取り組みです！裏で行われているエンジニアリング作業を見るのは常に刺激的です。アルゴリズムを前進させ、Pinterestの体験をよりスマートにしているチームに拍手を送りたいです。
```
Reply 返信  
John Hua ~ Design & Fries ~  
Oct 29 10月29日  
```
How have people applied this into new software and tooling recently? I use LLMs to do software engineering for front-landing pages. I do it to help people boost their branding, marketing, messaging, and more revenue conversions.
最近、人々はこれを新しいソフトウェアやツールにどのように適用していますか？私は、フロントランディングページのソフトウェアエンジニアリングにLLMsを使用しています。これは、人々のブランディング、マーケティング、メッセージング、そして収益の転換を向上させるために行っています。
```
Reply 返信  
AI enthusiast  
Oct 23 10月23日  
```
This is a great breakdown of user journey identification. I'm particularly interested in how you handle data from different sources.
これはユーザージャーニーの特定に関する素晴らしい分析です。私は特に、異なるソースからのデータをどのように扱うかに興味があります。
```
Reply 返信  



## More from Pinterest Engineering and Pinterest Engineering Blog Pinterest Engineeringの技術とPinterest Engineering Blogの最新情報

In
Pinterest Engineering Blog
Pinterest Engineering Blogにおいて
by
Pinterest Engineering
Pinterest Engineeringによる



## A Decade of AI Platform at Pinterest  
### Lessons on building platforms, driving adoption, and evolving foundations  
Pinterest Engineering Blog  
by Pinterest Engineering  

PinterestにおけるAIプラットフォームの10年  
プラットフォームの構築、採用の推進、基盤の進化に関する教訓  
Pinterest Engineering Blog  
Pinterest Engineeringによる  



## Slashing CI Wait Times: How Pinterest Cut Android Testing Build Times by 36%+  
### George Kandalaft | Software Engineer II, Test Tools; Alice Yang | Staff Software Engineer, Test Tools
Pinterest Engineering Blog
by
Pinterest Engineering

CI待機時間の削減：PinterestがAndroidテストビルド時間を36％以上短縮した方法  
### ジョージ・カンダラフト | ソフトウェアエンジニア II, テストツール; アリス・ヤン | スタッフソフトウェアエンジニア, テストツール
Pinterestエンジニアリングブログ
著者
Pinterestエンジニアリング



## Developer Experience at Pinterest: The Journey to PinConsole  
### Authors: Ashlin Jones, Engineering Manager; Haniel Martino, Software Engineer; Su Rong, Software Engineer; Viktoria Czaran, Software…

Pinterest Engineering Blog
by
Pinterest Engineering

## Pinterestにおける開発者体験：PinConsoleへの旅  
### 著者：アシュリン・ジョーンズ（エンジニアリングマネージャー）、ハニエル・マルティーノ（ソフトウェアエンジニア）、スー・ロン（ソフトウェアエンジニア）、ビクトリア・チャラン（ソフトウェア…）

Pinterestエンジニアリングブログ
著者
Pinterestエンジニアリング



## How we built Text-to-SQL at Pinterest  
### Adam Obeng | Data Scientist, Data Platform Science; J.C. Zhong | Tech Lead, Analytics Platform; Charlie Gu | Sr. Manager, Engineering
私たちがPinterestでText-to-SQLをどのように構築したか  
### アダム・オベング | データサイエンティスト、データプラットフォームサイエンス; J.C. ゾン | テックリード、アナリティクスプラットフォーム; チャーリー・グー | シニアマネージャー、エンジニアリング
Apr 3, 2024A clap icon2.7KA response icon24
2024年4月3日　拍手アイコン2.7K　応答アイコン24
Apr 3, 2024
2024年4月3日
2.7K
2.7K
24
24



## Recommended from Medium おすすめのMediumから

ujjwal kumar
ujjwal kumar



## Stripe SDE 2 Interview Experience & Offer Breakdown (₹95.5L Total)  
## Stripe SDE 2の面接体験とオファーの内訳（総額₹95.5L）

### Role: Backend Engineer (L2)  
### 役職: バックエンドエンジニア（L2）

4d agoA clap icon2  
4日前に、拍手アイコン2



## The AI Bubble Is About To Burst, But The Next Bubble Is Already Growing  
### Techbros are preparing their latest bandwagon.  
AIバブルは間もなく崩壊するが、次のバブルはすでに成長している。  
### テックブロは最新の流行に乗る準備をしている。  
Sep 15A clap icon18.6KA response icon686  
9月15日 いいねアイコン18.6K 反応アイコン686  
Sep 15  
9月15日  
18.6K  
686  
In  
DataEmpire.AI  
by  
Prem Vishnoi(cloudvala)  
による  



## How I Cracked the Meta Product Analytics Interview And What Actually Mattered  
### When I first got the call for a Meta Product Analytics interview, my first reaction was pure panic and worry how it will go and perform.
## 私がMetaプロダクトアナリティクスの面接を突破した方法と実際に重要だったこと  
### Metaプロダクトアナリティクスの面接の電話を初めて受けたとき、私の最初の反応は純粋なパニックと、どのように進行し、パフォーマンスを発揮するかについての心配でした。



## Why everything looks the same in 2025 なぜ2025年にはすべてが同じに見えるのか  
### The Copy-Paste World コピー＆ペーストの世界
Sep 24A clap icon2.9KA response icon120  
Sep 24  
2.9K  
120  
In  
Pinterest Engineering Blog  
by  
Pinterest Engineering  



## Next-Level Personalization: How 16k+ Lifelong User Actions Supercharge Pinterest’s Recommendations  
次のレベルのパーソナライズ：16,000以上の生涯ユーザーアクションがPinterestの推薦を強化する方法  

### Xue Xia | Machine Learning Engineer, Home Feed Ranking; Saurabh Vishwas Joshi | Principal Engineer, ML Platform; Kousik Rajesh | Machine…  
### Xue Xia | 機械学習エンジニア、ホームフィードランキング; Saurabh Vishwas Joshi | プリンシパルエンジニア、MLプラットフォーム; Kousik Rajesh | 機械…

Jun 7A clap icon174A response icon4  
6月7日　拍手アイコン174　応答アイコン4  

Jun 7  
6月7日  

174  
174  

4  
4  

Saurav Mandal  
Saurav Mandal  



## Do Hard Things if You Want an Easy Life 難しいことをやれば楽な人生が手に入る

### The one skill that changes everything すべてを変える一つのスキル
Jun 14 6月14日
A clap icon 拍手アイコン 25K 25K
A response icon 反応アイコン 1017 1017
Jun 14 6月14日
25K 25K
1017 1017
Help ヘルプ
Status ステータス
About このサイトについて
Careers キャリア
Press プレス
Blog ブログ
Privacy プライバシー
Rules ルール
Terms 利用規約
Text to speech テキスト読み上げ
