refs: https://medium.com/pinterest-engineering/identify-user-journeys-at-pinterest-b517f6275b42


# Identify User Journeys at Pinterest Pinterestにおけるユーザージャーニーの特定

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

We define a journey as the intersection of a user’s interests, intent, and context at a specific point in time. 
私たちは、ジャーニーを特定の時点におけるユーザーの興味、意図、コンテキストの交差点として定義します。
A user journey is a sequence of user-item interactions, often spanning multiple sessions, that centers on a particular interest and reveals a clear intent — such as exploring trends or making a purchase. 
ユーザージャーニーは、特定の興味に焦点を当て、トレンドを探求したり購入を行ったりする明確な意図を明らかにする、複数のセッションにわたるユーザーとアイテムの相互作用の連続です。
For example, a journey might involve an interest in “summer dresses,” an intent to “learn what’s in style,” and a context of being “ready to buy.” 
例えば、ジャーニーは「夏のドレス」に対する興味、「流行を学ぶ」という意図、そして「購入の準備ができている」というコンテキストを含むかもしれません。
Users can have multiple, sometimes overlapping, journeys occurring simultaneously as their interests and goals evolve. 
ユーザーは、興味や目標が進化する中で、同時に複数の、時には重複するジャーニーを持つことができます。

Inferring user journeys goes beyond understanding immediate interests, it allows us to comprehend the underlying, long-term goals of our users. 
ユーザージャーニーを推測することは、即時の興味を理解することを超え、ユーザーの根底にある長期的な目標を理解することを可能にします。
By identifying user journeys, we can move from simple content recommendations to becoming a platform that assists users in achieving their goals, whether it’s planning a wedding, renovating a kitchen, or learning a new skill. 
**ユーザージャーニーを特定することで、私たちは単純なコンテンツ推薦から、結婚式の計画、キッチンの改装、新しいスキルの習得など、ユーザーが目標を達成するのを支援するプラットフォームへと移行できます。**
This aligns with Pinterest’s mission to be an inspiration-to-realization platform, and provides the foundation for journey-aware recommendations.
これは、Pinterestの「インスピレーションから実現へ」という使命と一致し、ジャーニーを意識した推薦の基盤を提供します。

![]()
Figure 1: Example of notifications based on user journey

<!-- ここまで読んだ! -->

## Our Solution Philosophy 私たちの解決策の哲学

From the outset, we knew we were building a new product without large amounts of training data. 
開発当初に私たちは、今回の新しいプロダクトを開発する上で「大量のトレーニングデータが存在しない」という制約があることを認識していました。
(確かに、Journeyの正解ラベルは基本ほぼないよね。あるとしても人手で少量付与するくらいしかない。)
This constraint shaped our engineering philosophy for this project:
この制約が、このプロジェクトの以下のエンジニアリング哲学を形成しました: 
(参考になりそう...!:thinking:)

- Be Lean（リーンであること）:Minimize the development of new components where no data exists. スリムであること：データが存在しない場所で新しいコンポーネントの開発を最小限に抑えます。
  - 森田メモ:
    - 不確実な状態で複雑な仕組みを作り込むのではなく、必要最小限の機能で効率的に開発を進めることを重視する。

- Start Small (小さく始める) :Begin with a small, high-quality dataset of a few hundred human-annotated examples. 小さく始める：数百の人間によって注釈された例からなる小さく高品質なデータセットで始めます。
  - 森田メモ: 
    - 最初から大規模なデータセットを集めようとするのではなく、まずは「数百件程度の人間がアノテーションした高品質なデータセット」から開始。量よりも質を重視する。
- Leverage Foundation Models:Utilize pretrained models, like pretrainedSearchSagefor keyword embeddings, to maximize cost efficiency and effectiveness. 基盤モデルを活用する：キーワード埋め込みのためのpretrainedSearchSageのような事前学習モデルを利用して、コスト効率と効果を最大化します。
  - 森田メモ:
    - コスト効率と有効性を最大化するために、ゼロからモデルを学習させるのではなく、既存の「事前学習済みモデル（Pretrained models）」を活用する。
- **Make it Extensible (拡張性を持たせる)**:Design a system that supports more complex models as we collect more data, with a clear path to incorporating more advanced ML and LLM techniques. 拡張可能にする：データを収集するにつれて、より複雑なモデルをサポートするシステムを設計し、より高度なMLおよびLLM技術を組み込む明確な道筋を持たせます。
  - 森田メモ:
    - 初期段階はシンプルであっても、将来的にデータが蓄積された際には、より複雑なモデルや高度な機械学習技術、そしてLLM（大規模言語モデル）を組み込めるようにシステムを設計。
    - 技術の進化に合わせてシステムを成長させるための長期的な視点。

<!-- ここまで読んだ! -->

## System Architecture: A Walkthrough システムアーキテクチャ: 概要

To identify these journeys, we evaluated two primary approaches: 
これらのジャーニーを特定するために、私たちは2つの主要なアプローチを評価しました。

1. Predefined Journey Taxonomy: Building a fixed set of journeys and mapping users to them. 
事前定義されたジャーニーの分類：固定されたジャーニーのセットを構築し、ユーザーをそれらにマッピングします。
While this offers consistency, it risks overlapping with existing systems, requiring significant maintenance, and being slow to adapt to new trends. 
これは一貫性を提供しますが、既存のシステムと重複するリスクがあり、重要なメンテナンスが必要で、新しいトレンドに適応するのが遅くなります。

2. Dynamic Keyword Extraction: Directly extracting journeys from a user’s activities, representing each journey as a cluster of keywords (queries, annotations, interests, etc.). 
動的キーワード抽出: ユーザの活動から直接ジャーニーを抽出し、**各ジャーニーをキーワード（クエリ、注釈、興味など）のクラスターとして表現**します。

We chose the Dynamic Extraction approach to generate journeys based on the user’s information.
私たちは、**ユーザの情報に基づいてジャーニーを生成するために、動的抽出アプローチを選択**しました。
It offered greater flexibility, personalization, and adaptability, allowing the system to respond to emerging trends and unique user behaviors. 
このアプローチは、より大きな柔軟性、パーソナライズ、適応性を提供し、システムが新たなトレンドやユニークなユーザの行動に応じることを可能にしました。
This method also allowed us to leverage existing infrastructure and simplify the modeling process by focusing on clustering activities for individual users. 
この方法は、**既存のインフラを活用し、個々のユーザの活動をクラスタリングすることに焦点を当てる**ことで、モデリングプロセスを簡素化することも可能にしました。

![]()
Figure 2: High-level journey aware notification system design
図2: 高レベルのジャーニー認識通知システム設計

At a high level, we extract keywords from multiple sources and employ hierarchical clustering to generate keyword clusters; each cluster is a journey candidate.
高いレベルでは、**私たちは複数のソースからキーワードを抽出し、階層的クラスタリングを用いてキーワードクラスターを生成**します; 各クラスターはジャーニー候補です。
We then build specialized models for journey ranking, stage prediction, naming, and expansion. 
次に、ジャーニーのランキング、ステージ予測、命名、拡張のための専門的なモデルを構築します。
This inference pipeline runs on a streaming system, allowing us to run full inference if there’s algorithm change, or daily incremental inference for recent active users so the journeys respond quickly to a user’s most recent activities. 
この推論パイプラインはストリーミングシステム上で動作し、アルゴリズムの変更があった場合には完全な推論(=たぶん洗い替え的なやつ!:thinking:)を実行したり、最近のアクティブユーザに対して日次のincremental推論を実行することができるため、ジャーニーがユーザの最新の活動に迅速に対応します。

![]()
Figure 3: User journey inference pipeline via Streaming system
図3: ストリーミングシステムを介したユーザージャーニー推論パイプライン

Let’s break down the key components of this innovative system: 
この革新的なシステムの主要なコンポーネントを分解してみましょう:

<!-- ここまで読んだ! -->

## 1. User Journey Extraction and Clustering ユーザージャーニーの抽出とクラスタリング

This foundational component is designed to generate fresh, personalized journeys for each user.
この基盤コンポーネントは、各ユーザーのために新鮮でパーソナライズされたジャーニーを生成するように設計されています。

- Input Data: We leverage a rich set of user data, including:
入力データ：私たちは、以下を含む豊富なユーザーデータセットを活用します：
  — User search history: Aggregated queries and timestamps.
  — ユーザ検索履歴：集約されたクエリとタイムスタンプ。
  — User activity history: Interactions like Pin closeups, repins, and clickthroughs, extract the annotations and interests from the engaged Pins.
  — ユーザ活動履歴：Pinのクローズアップ、再ピン、クリックスルーなどのインタラクションから、関与したPinsの注釈と興味を抽出します。
  — User’s boards: Extract the annotations and interests from the Pins in the user’s boards.
  — ユーザのボード：ユーザーのボード内のPinsから注釈と興味を抽出します。

- User Journey Clustering: We treat all the queries, annotations, and interests as keywords with metadata.
ユーザージャーニークラスタリング：私たちは、すべてのクエリ、注釈、および興味をメタデータを持つキーワードとして扱います。
Then we adopt the pretrained text embedding for the keywords to perform hierarchical clustering to form journey clusters.
次に、**キーワードに対して事前学習されたテキスト埋め込みを採用し、階層的クラスタリングを実行してジャーニークラスタを形成**します。(k-meansなどの非階層的クラスタリング手法と比べて、クラスタ数を事前に決める必要がないから?:thinking:)

<!-- ここまで読んだ! -->

- メモ: 
  - このセクションは、User Journey特定システムの最初のステップ「ユーザージャーニーの抽出とクラスタリング」に関する話。
    - システム全体の基盤となる部分で、ユーザの多様な行動データを整理して、「ジャーニーの候補(キーワードのクラスター)」を生成する役割を担う。
  - 入力データ:
    - システムは、ユーザ行動から得られる以下の**3種類のテキストデータ**を収集する.
      - ユーザ検索履歴: 
        - ユーザが過去に行った検索クエリとそのタイムスタンプ.
      - ユーザアクティビティ履歴: 
        - ユーザがPin(=アイテム)に対して行ったインタラクション(例: Pinのクローズアップ、再ピン、クリック)。ここでは、interactしたPinに付与されている注釈や興味タグを抽出する。
      - ユーザのボード:
        - Pinterestにおける「ボード」機能は、ユーザがPin(アイテム)を手動で保存・整理する場所。「ユーザ自身が明示的に作成した興味の集合」という非常に重要な意味を持つ。ここからもPinに付与されている注釈や興味タグを抽出する。
    - これら3つのデータソースから得られた**テキストデータ(クエリ、注釈、興味タグ)**を「キーワード」として扱う。
  - クラスタリングプロセス:
    - 収集されたキーワード達は、以下の手順で、意味のあるグループ(ジャーニークラスター)にまとめられる.
      - 1. 事前学習済みのテキスト埋め込みモデル(pretrained text embedding)を用いて、各キーワードをベクトル化。これにより、キーワード間の意味的な類似性を数値的に表現できる。
      - 2. ベクトル化されたキーワード達に対して、階層的クラスタリング(hierarchical clustering)を実行。これにより、類似したキーワードが自然にグループ化され、「ジャーニーの候補」となるクラスターが形成される。

## 2. Journey Naming & Expansion ジャーニーの命名と拡張

Clear and intuitive journey names are crucial for user experience.  
明確で直感的なジャーニー名は、ユーザ体験にとって非常に重要です。

- Journey Naming: The current production model is to apply a ranking model to pick the top keyword extracted from each cluster as the journey name.  
ジャーニーの命名：現在のproductionモデルは、**各クラスターから抽出された上位キーワードをジャーニーの名前として選ぶためにランキングモデルを適用**することです。  
It balances personalization and simplicity by choosing the most relevant keywords from the cluster.  
これは、**クラスターから最も関連性の高いキーワードを選ぶ**ことで、パーソナライズとシンプルさのバランスを取ります。
We are working with scaling LLM for Journey Name Generation, which promises highly personalized and adaptable names.  
私たちは、非常にパーソナライズされ適応可能な名前を約束するジャーニー名生成のために、LLMのスケーリングに取り組んでいます。

- Journey Expansion: We leverage LLMs to generate new journey recommendations based on a user’s past or ongoing journeys, with an emphasis on balancing the predictive power of LLMs and efficiently serving through pre-generated recommendations.
ジャーニーの拡張：私たちは、ユーザーの過去または進行中のジャーニーに基づいて新しいジャーニーの推薦を生成するためにLLMを活用し、LLMの予測力と事前生成された推薦を通じて効率的に提供することのバランスに重点を置いています。
In the initial stage, we focus on creating non-personalized, related journeys based on a given input journey.
初期段階では、与えられた入力ジャーニーに基づいて、非パーソナライズされた関連ジャーニーの作成に焦点を当てています。
Since the total number of journeys is limited, we can use LLMs to generate this data offline and store it in a key-value store.
ジャーニーの総数が限られているため、私たちはLLMを使用してこのデータをオフラインで生成し、キー・バリュー・ストアに保存することができます。
For personalized recommendations, we will apply the journey ranking model online to rank related journeys for each user.
パーソナライズされた推薦については、ジャーニーランキングモデルをオンラインで適用して、各ユーザーの関連ジャーニーをランク付けします。

- メモ: 
  - このセクションは、第2ステップ「ジャーニーの命名と拡張」について説明している。
  - その1: Journey Naming(ジャーニーの命名):
    - 第1ステップで抽出された無機質なキーワードクラスターに対して、直感的で分かりやすい名前をつけるプロセス。ユーザ体験にとって非常に重要。
    - 現在productionで使われてるアプローチ(ranking model):
      - 専用のランキングモデルで、1クラスターに含まれる大量のキーワードの中から、最も代表的なキーワードを1つ選び出してジャーニー名とする。
    - 今後の進化の方向性(LLM):
      - 将来的には、既存の単語を選ぶだけでなく、大規模言語モデル（LLM）を使って、より自然で高度にパーソナライズされた名前（例：「夏の結婚式の準備」など）を生成する方向で開発が進んでいる。
  - その2: Journey Expansion(ジャーニーの拡張):
    - ユーザが現在進めているジャーニーに関連する、「新しいジャーニー」を推薦する機能。
    - 目的: 
      - ユーザの現在の関心（例：「結婚式の計画」）に基づいて、次に興味を持ちそうなこと（例：「新婚ジャーニー行」や「新居のインテリア」）を予測・提案するイメージ。
    - オフライン生成(LLM活用):
      - 「AというジャーニーにはBが関連する」という一般的な関連性を、LLMを使って事前に大量生成し、キー・バリュー・ストア(高速なDB)に保存しておく。
    - オンライン提供:
      - ユーザがアクセスした際に、事前に生成しておいた関連リストの中から、そのユーザに最も関連性の高いジャーニーを、ランキングモデルを使ってリアルタイムに選び出し、推薦として提供する。

<!-- ここまで読んだ! -->

## 3. Journey Ranking & Diversification ジャーニーのランキングと多様化

To ensure the most relevant journeys are presented, and to prevent monotony, we built a ranking model and applied diversification afterwards.
最も関連性の高いジャーニーが提示されるようにし、単調さを防ぐために、私たちはランキングモデルを構築し、その後に多様化を適用しました。

### Journey Ranking ジャーニーランキング

Similar to traditional ranking problems, our initial approach is to build a point-wise ranking model. 
従来のランキング問題と同様に、私たちの**初期のアプローチはポイントワイズランキングモデルを構築すること**です。
We get labels from user email feedback and human annotation. 
私たちは、ユーザのメールフィードバックと人間の注釈からラベルを取得します。
The model takes user features, engagement features (how frequently the user engaged on this journey through search, actions on Pins, etc.) and recency features. 
このモデルは、ユーザの特徴、エンゲージメント特徴量（ユーザがこのジャーニーにどれだけ頻繁に関与したか、検索やピンに対するアクションなど）および新しさの特徴を考慮します。
This provides a simple, immediate baseline. 
これにより、シンプルで即時的なベースラインが提供されます。

<!-- ここまで読んだ! -->

### Journey Diversification ジャーニーの多様化

To prevent the top ranked journeys from always being similar, we implement a diversifier after the journey ranking stage. 
上位にランク付けされたジャーニーが常に似たようなものであるのを防ぐために、ジャーニーのランク付け段階の後に多様化機能を実装します。
The most straightforward approach is to apply a penalty if the journey is similar to the journeys that ranked higher (the similarity is measured using pretrained keyword embedding). 
**最も簡単なアプローチは、ジャーニーが上位にランク付けされたジャーニーと似ている場合にペナルティを適用することです（類似性は事前学習されたキーワード埋め込みを使用して測定されます）**。
For each journey i, score will be updated based on the formula below. 
各ジャーニー $i$ に対して、スコアは以下の式に基づいて更新されます。
Finally, we re-rank the journeys according to the updated score. 
最後に、更新されたスコアに基づいてジャーニーを再ランク付けします。

$$
score_{i} = score_{i} * penalty^{occurrence}
$$

Occurrence is the number of similar journeys ranked before the current journey, and penalty is a hyperparameter to tune, usually chosen as 0.95. 
Occurrenceは現在のジャーニーの前にランク付けされた類似ジャーニーの数であり、penaltyは調整するハイパーパラメータで、通常は0.95に選ばれます。
(類似ジャーニーの判定ってどうやってるんだろう？事前学習済みキーワード埋め込みのコサイン類似度が閾値超えたら類似とみなすとか？:thinking:)

- メモ:
  - このセクションは、第3ステップ「ジャーニーのランキングと多様化」について説明している。
    - 第1ステップ・第2ステップまでで生成されたジャーニーの集合の中から、「今、ユーザにとって最も重要で、かつ飽きさせないリスト」を作成するための工程。
  - その1: Journey Ranking(ジャーニーランキング):
    - ジャーニー集合の中から、ユーザにとって最も関連性の高いジャーニーを上位にランク付けするプロセス。
    - 現在はシンプルにpoitn-wise ranking modelを使ってる。
      - つまり、特にランキングを意識しないCTR予測モデル的なイメージ。
    - 使ってる特徴量(スコアの判断基準)
      - ユーザの特徴: その人の基本的な属性情報など。
      - エンゲージメント特徴量: ユーザが、そのジャーニーに対してどれだけ頻繁に検索やPinに対するアクションを行ったか。
      - 新しさ(Recency features): 最近の活動に関する情報?
    - 学習用のラベルの収集方法:
      - ユーザからのメールフィードバックと、人間によるアノテーションを収集して、正解ラベルとして使用。
  - その2: Journey Diversification(ジャーニーの多様化):
    - ランキング上位が似たような話題ばかりになるのを防ぐための処理。
    - 仕組み:
      - ランキングの上位から見ていき、「既に上位にあるジャーニーと似ている場合、そのジャーニーのスコアを下げる（ペナルティを与える）」という処理を行う。
      - 類似度の判定:
        - 事前学習済みキーワード埋め込みを使って、ジャーニー間の類似度を計算し、一定の閾値を超えたら「似ている」とみなす。
      - ペナルティの計算:
        - 自分より上位に似たジャーニーがいくつあるか（Occurrence）に応じてスコアを減点する。通常、ペナルティ係数として0.95を使用し、似たものが上にあるほど順位が下がりやすくなる。
  - ex. ニュースアプリのトップ画面に例えると...
    - Ranking: あなたが最近よく読んでいる「野球」や「政治」の記事を、重要度順にピックアップ。結果ごして1位〜5位がすべて「大谷選手の速報」になってしまうかも。
    - Diversification: 「全部野球だと飽きるだろう」と判断し、2位以下の野球記事の優先度を少し下げ、代わりに「グルメ」や「天気予報」の記事を間に差しこむ。

<!-- ここまで読んだ! -->

## 4. Journey Stage Prediction ジャーニーの段階予測

Understanding a journey’s lifecycle helps us determine appropriate notification timing. 
ジャーニーのライフサイクルを理解することで、適切な通知のタイミングを決定するのに役立ちます。 
We simplify this into two objectives: 
これを二つの目的に簡略化します：

- Situational vs. Evergreen Classification: Journeys are categorized based on user engagement patterns and activity duration. 
Situational vs Evergreen分類: ジャーニーは、ユーザのエンゲージメントパターンと活動期間に基づいて分類されます。
If users engage with a journey consistently over an extended period, we classify it as “Evergreen” — these journeys remain perpetually active. 
**ユーザが長期間にわたってジャーニーに一貫して関与する場合、それを「エバーグリーン」と分類します。これらのジャーニーは常にアクティブな状態を保ちます。**
In contrast, journeys with engagement limited to a shorter timeframe are classified as “Situational,” as they are expected to conclude at a certain point. 
対照的に、短期間に限られたエンゲージメントを持つジャーニーは"Situational"と分類され、特定の時点で終了すると予想されます。

- Journey Stage (Ongoing vs. Ended) Classification: For situational journeys, we evaluate whether the journey is still ongoing or has ended, primarily by analyzing the time since the user’s last engagement. 
- ジャーニーの段階（進行中 vs. 終了）分類：Situationalジャーニーについては、主にユーザの最後のエンゲージメントからの時間を分析することで、ジャーニーがまだ進行中であるか終了しているかを評価します。
Future improvements will include incorporating user feedback and developing a supervised model for more accurate classification. 
今後の改善には、ユーザのフィードバックを取り入れ、より正確な分類のための教師ありモデルを開発することが含まれます。

- メモ:
  - このセクションは、第4ステップ「ジャーニーの段階予測」について説明している。
    - あるユーザに現在紐づいているジャーニーについて、そのジャーニーのタイプや進行状況を識別するプロセス。
  - その1 タイプの判定(Situational vs. Evergreen):
    - まず、そのジャーニーが「一過性のもの(Situational)」なのか「永続的なもの(Evergreen)」なのかを識別する。
    - Situational:
      - ユーザの関与が短期間に限られているジャーニー。
      - ex. 「結婚式の準備」「ハロウィンの衣装選び」「キッチンのリノベーション」など。
      - ユーザのエンゲージメントが特定の短期間に集中する。
    - Evergreen:
      - ユーザが趣味や習慣として常に持ち続けてる興味のジャーニー。
      - ex. 「毎日のレシピ」「メンズファッション」「ガーデニング」
      - 長期間にわたって一貫してエンゲージメントが発生する。
    - 現在の識別ロジック:
      - 基本的には特徴量 × ルールベース。今後の改善として、ユーザフィードバックを取り入れた教師ありモデルの活用や、LLMベースのアプローチも検討中。
      - ex. あるユーザの現在アクティブになってるジャーニーについて、過去半年間にわたって一定頻度で一貫してエンゲージメントが発生していればEvergreen、そうでなければSituationalと判定する。
        - たぶん実際にはPinterestプロダクト内でユーザはPin(=アイテム)に対してアクションを起こしてるので、そのPinに紐づくジャーニーを集計して判定してる感じだと思う...!:thinking:
  - その2 ステージの判定(Ongoing vs. Ended):
    - 「Situational(一過性)」と判定されたジャーニーに対して、あるユーザの対象ジャーニーが「現在進行中(Ongoing)」なのか「終了(Ended)」しているのかを識別する。
    - Ongoing:
      - まだユーザがそのジャーニーにアクティブに取り組んでる状態。通知を送れば喜ばれる可能性が高い。
    - Ended:
      - そのジャーニーが既に完了している状態。通知を送ってもあまり意味がない。
      - ex. すでに結婚式が終わったユーザに、いつまでも「ウェディングドレス」の通知を送り続けるのは、ユーザにとってノイズでしかない。
    - 現在の識別ロジック:
      - Situational/Evergreen分類と同様に、特徴量 × ルールベースで判定してるっぽい。今後の進化も同様。
        - 1. 教師あり学習モデルへの移行: 判定精度を高めるために、将来的にはユーザフィードバックを活用した教師あり学習モデルを導入する予定。
        - 2. LLMベースのアプローチ: これらの分類やステージ予測を個別のモデルやルールで行うのではなく、**「LLMにユーザーの行動履歴を読ませて、文脈から一発で判断させる」**という実験も進行中。
      - ex. あるユーザにおけるアクティブなジャーニーに対して、直近1ヶ月以内にそのジャーニーに関連するアクションが発生していればOngoing、そうでなければEndedと判定する。

## 5. User Journeys Output ユーザージャーニーの出力

The user journeys could be used in downstream applications for retrieval and ranking. 
ユーザージャーニーは、取得およびランキングのための下流アプリケーションで使用される可能性があります。
The desired output is a list of distinct user journeys. 
**望ましい出力は、異なるユーザージャーニーのリスト**です。
Each journey should ideally be represented with: 
各ジャーニーは理想的には以下のように表現されるべきです：

- Journey Name: A concise and descriptive name (e.g., “Kitchen Renovation,” “Improving Home Organization,” “Engagement Ring Selection”). 
ジャーニー名：簡潔で説明的な名前（例：「キッチンリノベーション」、「家庭の整理改善」、「婚約指輪の選択」）。

- Keywords: List of keywords related to this journey; it could be the corresponding interests, annotations, queries, or any keywords. 
キーワード：このジャーニーに関連するキーワードのリスト；それは対応する興味、注釈、クエリ、または任意のキーワードである可能性があります。

- Stage: An indicator of where the user is within that journey (e.g., “inspiration,” “action”); we simplified it to “ongoing” or “ended” in the initial launch. 
ステージ：ユーザーがそのジャーニーの中でどこにいるかを示す指標（例：「インスピレーション」、「アクション」）；私たちは、初期のローンチで「進行中」または「終了」に簡略化しました。(第四ステップで説明したやつ)

- Confidence Score: The confidence score for this predicted journey. 
信頼度スコア：この予測されたジャーニーの信頼度スコアです。


- メモ: 
  - このセクションは、最終ステップ「ユーザージャーニーの出力」について説明している。
    - これまでの工程（抽出、命名、ランク付け、段階予測）を経て、最終的にシステムが**「このユーザについては、こういうデータを使う」**と決定した、完成品のフォーマット。
    - この出力は、通知システムや検索エンジンなどの下流アプリケーション(downstream applications)で利用される。
  - 望ましい出力フォーマット:
    - あるユーザに対する、異なるジャーニーのリスト。
    - 各ジャーニーは以下の情報を含む:
      - ジャーニー名: 簡潔で説明的なタイトル。
      - キーワード: そのジャーニーに関連するキーワードの集合。
      - ステージ: そのジャーニーにおけるユーザの現在の段階。
        - 現状: 初期ローンチではシンプルに「進行中（ongoing）」か「終了（ended）」かの二択で管理される。
        - 理想: 本来は「インスピレーション段階（inspiration）」や「実行段階（action）」といった細かい粒度が想定されてる。
      - 信頼性スコア
        - そのユーザジャーニー予測の信頼度を示すスコア。

```json
{
  "user_id": "12345",
  "inferred_journeys": [
    {
      "journey_name": "Kitchen Remodel",
      "keywords": ["kitchen renovation", "modern kitchen ideas", "kitchen storage solutions"],
      "stage": "Inspiration",
      "confidence_score": 0.95,
    },
    {
      "journey_name": "Wedding Planning",
      "keywords": ["wedding dresses", "bridal shower ideas", "wedding venues"],
      "stage": "Research",
      "confidence_score": 0.89,
    },
    {
      "journey_name": "Christmas Gift Ideas",
      "keywords": ["holiday gifts", "Christmas shopping", "gift wrapping ideas"],
      "stage": "Research",
      "confidence_score": 0.72,
    }
  ]
}
```


## 6. Relevance Evaluation 関連性評価

We aim to establish a robust evaluation and monitoring pipeline to ensure consistent and reliable quality assessment of top-k user journey predictions. 
私たちは、**トップkのユーザージャーニー予測の一貫した信頼性のある品質評価を確保するために、堅牢な評価および監視パイプラインを確立することを目指しています**。
Because human evaluation is costly and sometimes inconsistent, we leverage LLMs to assess the relevance of predicted user journeys. 
人間による評価はコストがかかり、時には一貫性がないため、私たちはLLMs（大規模言語モデル）を活用して予測されたユーザージャーニーの関連性を評価します。
By providing user features and engagement history, we ask the LLM to generate a 5-level score with explanations. 
**ユーザの特徴とエンゲージメント履歴を提供することで、LLMに5段階のスコアとその説明を生成するよう依頼します。**
We have validated that LLM judgments closely correlate with human assessments in our use case, giving us confidence in this approach. 
私たちは、LLMの判断が私たちのユースケースにおける人間の評価と密接に相関していることを確認しており、このアプローチに自信を持っています。

<!-- ここまで読んだ! -->

- メモ:
  - 

## Experiment Results 実験結果

We applied user journeys inference to deliver notifications related to the user’s ongoing journeys. 
私たちは、ユーザージャーニー推論を適用して、ユーザーの進行中のジャーニーに関連する通知を提供しました。
Our initial experiments demonstrate the significant impact of Journey-Aware Notifications¹:
私たちの初期実験は、ジャーニーを考慮した通知の重要な影響を示しています¹：

- The system drove statistically significant gains in user engagements.
システムは、ユーザーエンゲージメントにおいて統計的に有意な向上をもたらしました。

- Compared to our existing interest-based notifications, journey-aware notifications demonstrated an 88% higher email click rate and a 32% higher push open rate.
**既存の興味ベースの通知と比較して、ジャーニー対応通知は88%高いメールクリック率と32%高いプッシュオープン率**を示しました。
(興味ベースって、Pinベースってこと??:thinking:)

- User surveys revealed a 23% increase in positive feedback rate compared to interest-based notifications.
ユーザー調査では、興味ベースの通知と比較して23%のポジティブフィードバック率の増加が明らかになりました。

<!-- ここまで読んだ! -->

## Ongoing Effort 進行中の取り組み

As a follow up, we are working on leveraging large language models (LLMs) to infer user journeys given user information and activities, while offering several key benefits:
その後、私たちはユーザー情報と活動に基づいてユーザーのジャーニーを推測するために大規模言語モデル（LLMs）を活用する作業を進めており、いくつかの重要な利点を提供しています。

- Simplification: Many existing components of the journey inference system — including keyword extraction, clustering, journey naming, and stage prediction models — can be consolidated and replaced with a single LLM.
簡素化：ジャーニー推測システムの多くの既存コンポーネント（キーワード抽出、クラスタリング、ジャーニーの命名、ステージ予測モデルを含む）は、単一のLLMに統合され、置き換えられる可能性があります。

- Quality Improvement: By utilizing the advanced capabilities of LLMs to understand user behavior, we aim to significantly enhance the accuracy and quality of user journey predictions.
品質向上：ユーザーの行動を理解するためのLLMの高度な機能を活用することで、ユーザーのジャーニーの予測の精度と品質を大幅に向上させることを目指しています。

We tuned our prompts and used GPT to generate ground truth labels for fine-tuning Qwen, enabling us to scale in-house LLM inference while maintaining competitive relevance.
私たちはプロンプトを調整し、GPTを使用してQwenのファインチューニングのためのグラウンドトゥルースラベルを生成し、競争力を維持しながら社内のLLM推論をスケールアップできるようにしました。
Next, we utilized Raybatch inference to improve the efficiency and scalability.
次に、Raybatch推論を利用して効率性とスケーラビリティを向上させました。
Finally, we are implementing full inference for all users and incremental inference for recently active users to reduce overall inference costs.
最後に、すべてのユーザーに対して完全な推論を実施し、最近アクティブなユーザーに対してはincremental推論を行い、全体の推論コストを削減しています。
All generated journeys will go through safety checks to ensure they meet our safety standards.
生成されたすべてのジャーニーは、安全基準を満たしていることを確認するために安全チェックを受けます。

<!-- ここまで読んだ! -->
