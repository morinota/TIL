## link リンク

https://netflixtechblog.medium.com/lessons-learnt-from-consolidating-ml-models-in-a-large-scale-recommendation-system-870c5ea5eb4a
https://netflixtechblog.medium.com/lessons-learnt-from-consolidating-ml-models-in-a-large-scale-recommendation-system-870c5ea5eb4a

## title タイトル

Lessons Learnt From Consolidating ML Models in a Large Scale Recommendation System
大規模推薦システムにおけるMLモデルの統合から得られた教訓

## abstruct abstruct

In this blog post, we share system design lessons from consolidating several related machine learning models for large-scale search and recommendation systems at Netflix into a single unified model.
このブログポストでは、Netflixの大規模検索とレコメンデーションシステムに関連する複数の機械学習モデルを単一の統一モデルに統合したことから得られたシステム設計の教訓を共有する。
Given different recommendation use cases, many recommendation systems treat each use-case as a separate machine-learning task and train a bespoke ML model for each task.
様々な推薦のユースケースがある場合、**多くの推薦システムはそれぞれのユースケースを別々の機械学習タスクとして扱い、それぞれのタスクのために特注のMLモデルを訓練する**。
In contrast, our approach generates recommendations for multiple use cases from a single, multi-task machine learning model.
対照的に、我々のアプローチは、**単一のマルチタスク機械学習モデルから、複数のユースケースに対するレコメンデーションを生成する**。
This not only improves the model performance but also simplifies the system architecture, thus improving maintainability.
これはモデルの性能を向上させるだけでなく、システム・アーキテクチャを単純化し、保守性を向上させる。
Additionally, building a common extensible framework for search and recommendations has allowed us to build systems for new use-cases faster.
さらに、**検索とレコメンデーションのための共通の拡張可能なフレームワークを構築する**ことで、新しいユースケースに対応したシステムをより早く構築できるようになった。
We describe the trade-offs we made for achieving this consolidation and lessons we learnt that can be applied generally.
この統合を達成するために行ったトレードオフと、一般的に適用できる教訓について述べる。

# Background 背景

![](https://miro.medium.com/v2/resize:fit:1400/0*y_4rboMNZHFb9Fmn)

Figure 1: Multiple use cases in a typical recommendation system
図1：
典型的な推薦システムにおける複数のユースケース

In large real world recommender system applications like e-commerce, streaming services, and social media, multiple machine learning models are trained to optimize item recommendations for different parts of the system.
電子商取引、ストリーミングサービス、ソーシャルメディアなどの大規模な実世界のレコメンダーシステムアプリケーションでは、システムのさまざまな部分に対してアイテムの推薦を最適化するために、複数の機械学習モデルが学習される。
There are separate models for different use-cases like notifications (user-to-item recommendations), related items (item-to-item based recommendations), search (query-to-item recommendations), and category exploration (category-to-item recommendations) (Figure 1).
通知(ユーザからアイテムへのレコメンデーション)、関連アイテム（アイテムからアイテムへのレコメンデーション）、検索（クエリからアイテムへのレコメンデーション）、カテゴリー探索（カテゴリーからアイテムへのレコメンデーション）のような、異なるユースケースに対して別々のモデルがある（図1）。
However, this can rapidly result in systems management overhead and hidden technical debt in maintaining a large number of specialized models (Sculley et al., 2015).
しかし、これはシステム管理のオーバーヘッド(=負荷?)や、**多数の専門モデルを維持するための隠れた技術的負債を急速にもたらす可能性がある**(Sculley et al., 2015)。
This complexity can lead to increased long-term costs, and reduce the reliability and effectiveness of ML systems (Ehsan & Basillico, 2022).
**この複雑さは長期的なコスト増につながり、MLシステムの信頼性と有効性を低下させる**（Ehsan & Basillico, 2022）。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*gv5s3OasfIg7Gv1dRX4x1g.png)

Figure 2: Model Proliferation in ML Systems MLシステムにおけるモデルの増殖

Figure 2 shows how such an ML system with model proliferation might look.
図2は、このような**モデル拡散(model proliferation)を伴うMLシステム**がどのように見えるかを示している。
The different use-cases like notifications, related items, search and category exploration have different UI canvases where the user interacts with them.
通知、関連アイテム、検索、カテゴリ探索のような異なるユースケースは、ユーザがそれらと相互作用する異なるUIキャンバスを持っている。(それは絶対だよね:thinking:)
ML systems for these different use-cases often evolve to have multiple offline pipelines that have similar steps such as label generation, featurization and model training.
このようなさまざまなユースケースに対応するMLシステムは、ラベル生成、特徴づけ、モデル学習といった同様のステップを持つ複数のオフラインパイプラインを持つように進化することが多い。
On the online side, different models might be hosted in different services with different inference APIs.
オンライン側では、異なるモデルが異なる推論APIを持つ異なるサービスにホストされているかもしれない。(クライアント側からみたら、そんなにmodel proliferationは感じない...:thinking:)
However, there are a number of commonalities in both offline pipelines and online infrastructure, which such a design does not leverage.
しかし、オフラインのパイプラインとオンラインのインフラストラクチャーには多くの共通点があり、このような設計では活用できない。

In this blog, we describe our efforts to leverage the commonalities across these tasks to consolidate the offline and online stacks for these models.
このブログでは、これらのタスクの共通点を活用し、これらのモデルのオフライン・スタックとオンライン・スタックを統合する取り組みについて説明する。
This methodology not only reduces technical debt but also enhances the effectiveness of the models by leveraging knowledge gained from one task to improve another related task.
**この方法論は技術的負債を減らすだけでなく、あるタスクから得た知識を別の関連タスクの改善に活用することで、モデルの有効性を高める**。(事前学習は共通のモデルでやって、各下流タスク毎にfine-tuningする感じだろうか:thinking:)
Additionally, we noticed advantages in terms of efficiently implementing innovative updates across multiple recommendation tasks.
さらに、複数の推薦タスクにまたがる革新的な更新を効率的に実施できるという点でも、利点があることに気づいた。

![fig3]()

Figure 3 shows the consolidated system design.
図3は、統合されたシステム設計を示している。
After an initial step of use-case-specific label preparation, we unify the rest of the offline pipeline and train a single multi-task model.
各ユースケースに特化したラベル(=教師ラベル)準備の最初のステップの後、残りのオフラインパイプラインを統一し、**単一のマルチタスクモデルを訓練**する。
On the online side, a flexible inference pipeline hosts models in different environments based on the latency, data freshness and other requirements, and the model is exposed via a unified canvas-agnostic API.
オンライン側では、柔軟な推論パイプラインがレイテンシー、データの鮮度、その他の要件に基づいて異なる環境でモデルをホストし、モデルはキャンバスにとらわれない統一されたAPIを介して公開される。

Figure 3: Consolidated ML System
図3: 統合MLシステム

## Offline Design オフラインデザイン

In an offline model training pipeline, each recommendation task maps to a request context where recommendations need to be shown.
オフラインモデル学習パイプラインでは、各推薦タスクは、推薦を表示する必要があるリクエストコンテキストにマッピングされる。(??)
The request context schema varies depending on the specific task.
リクエストコンテキストスキーマは特定のタスクによって異なる。
For instance, for query-to-item recommendation, the request context would consist of elements like the query, country, and language.
例えば、query-to-item推薦の場合、リクエストコンテキストはクエリ、国、言語などの要素で構成される。(requenst contextはモデルの入力情報的な意味合いっぽい。意思決定policyに入力する context $x$ みたいな)
On the other hand, for item-to-item recommendation, the request context would also include the source item and country information.
一方、item-to-item推薦では、リクエストコンテキストはソースアイテムと国情報も含む。
The composition of the request context schema is tailored to suit the requirements of each recommendation task.
リクエストコンテキストスキーマの構成は、それぞれの推薦タスクの要求に合わせて調整される。

An offline pipeline trains models from logged interaction data in these stages:
オフラインのパイプラインは、これらの段階でログに記録されたinteractionデータからモデルを訓練する:

- Label preparation: Clean logged interaction data and generate (request_context, label) pairs. ラベルの準備: ログに記録されたインタラクションデータをクリーニングし、**(request_context, label)のペアを生成**する。

- Feature Extraction: Generate feature vectors for the above generated (request_context, label) tuples. 特徴抽出: 上記の生成された(request_context, label)タプルの特徴ベクトルを生成する。(textの埋め込みベクトル使ったりとか?)

- Model Training: Train a model based on (feature_vector, label) rows. モデルのトレーニング: (feature_vector,label)データセットに基づいてモデルを学習する。

- Model Evaluation: Assess the performance of the trained model using appropriate evaluation metrics. モデルの評価: 適切な評価指標を用いて学習済みモデルの性能を評価する。

- Deployment: Make the model available for online serving. 配備する: モデルをオンラインで提供できるようにする。

For model consolidation, we set the unified request context to the union of all context elements across tasks.
モデル統合のために、**統合request context**を、タスク間のすべてのcontext要素を結合したものとして設定する。(concatenateするイメージ??:thinking:)
For specific tasks, missing or unnecessary context values are substituted by sentinel (default) values.
特定のタスクでは、欠落している、または不要なcontext値は、**sentinel(デフォルト)値で置き換えられる**。
We introduce a task_type categorical variable as part of the unified request context to inform the model of target recommendation task.
推薦タスクのモデルに情報を提供するために、統合requenst contextの一部として**task_typeカテゴリ変数を導入**する。

In label preparation, data from each canvas are cleaned, analyzed and stored with the unified request context schema.
ラベルの準備では、各キャンバスのデータがクリーニングされ、分析され、統合request contextスキーマとともに保存される。(統合request context, 各タスクのラベル)のタプル??:thinking:
This label data from different canvases is then merged together with appropriate stratification to get a unified labeled data set.
異なるキャンバスからのこのラベルデータは、適切な層別化によって統合され(=ラベルデータもconcatenateされるイメージ??:thinking:)、統合ラベル付きデータセットとなる。
In feature extraction, not all features contain values for certain tasks and are filled with appropriate default values.
特徴量抽出では、すべての特徴量に特定のタスクの値が含まれているわけではなく、適切なデフォルト値で埋められます。

# Online Design オンラインデザイン

Serving a single ML model at-scale presents certain unique online MLOps challenges (Kreuzberger et al., 2022).
単一のMLモデルをat-scale(=大規模?)で提供することは、オンラインMLOps特有の課題をもたらす(Kreuzberger et al., 2022)
Each use-case may have different requirements with respect to:
**各ユースケースは、以下の点に関して異なる要求(=このusecaseではレイテンシーhogehoge以下、みたいな制約??)を持っている可能性**がある:

- **Latency and throughput**: Different service-level agreements (SLAs) to guarantee a latency and throughput target to deliver an optimal end-user experience. Latencyとthroughput: 最適なユーザ体験を提供するために、レイテンシーとスループットの目標を保証するさまざまなサービス・レベル・アグリーメント（SLA）。
  - (throughput: 単位時間あたりに処理できるタスクやデータの量を示す指標:thinking:)
- **Availability**: Different guarantees of model serving uptime, without resorting to fallbacks. 可用性: フォールバック(予備手段)に頼ることなく、さまざまなモデルのサービス稼働時間を保証。
  - (Availability 可用性(%): システムやサービスが正常に稼働して利用可能な状態にある時間の割合:thinking:)
- **Candidate Sets**: Different types of items (e.g. videos, games, people, etc) that may be further curated by use-case-specific business requirements. 候補集合: さまざまなタイプのアイテム(ビデオ、ゲーム、人物など)で、ユースケース固有のビジネス要件によってさらに分類される。(usecase毎に行動空間が異なるのは、そりゃそうだよなぁ:thinking:)
- **Budget**: Different budget targets for model inferencing costs. 予算：モデル推論コストの予算目標が異なる。
- **Business Logic**: Different pre- and post- processing logic. ビジネスロジック: 処理前と処理後のロジックが異なる。(これもそりゃそう)

Historically, use-case-specific models are tuned to satisfy the unique requirements.
歴史的に、usecaseに特化したモデルは、固有の要件を満たすように調整される。
The core online MLOps challenge is to support a wide variety of use-cases without regressing towards the lowest-common denominator in terms of model performance.
**オンラインMLOpsの核となる課題は、モデル性能(requestの制約を維持しながら!)の観点で最も一般的で最低限の水準に後退する事なく、多様なusecaseをサポートすること**である。

We approached this challenge by:
私たちはこの課題にこう取り組んだ:

- Deploying the same model in different system environments per use-case. Each environment has “knobs” to tune the characteristics of the model inference, including model latency, model data freshness and caching policies and, model execution parallelism. **usecaseごとに異なるシステム環境に同じモデルを展開**する。(うんうんなんとなくイメージ通り:thinking:) 各環境には、モデルのレイテンシー、モデルデータの鮮度とキャッシュポリシー、モデルの実行並列性など、モデル推論の特性を調整するための「つまみ」がある。

- Exposing a generic, use-case-agnostic API for consuming systems. To enable this flexibility, the API enables heterogeneous context input (User, Video, Genre, etc.), heterogeneous candidate selection (User, Video, Genre, etc.), timeout configuration, and fallback configuration. **システムを消費するための汎用的でusecaseにとらわれないAPIを公開する**(ん?APIは一つって事?? 各usecaseをquery parameter等で切り替えるってこと?:thinking:)。 この柔軟性を可能にするために、APIは種類の異なるcontext入力(ユーザ、ビデオ、ジャンルなど)、種類の異なる候補選択(ユーザ、ビデオ、ジャンルなど)、タイムアウト設定、フォールバック設定を可能にする。

# Lessons Learnt 教訓

Consolidating ML models into a single model can be thought of as a form of software refactoring (Cinnéide et al., 2016).
**MLモデル達を単一のモデルに統合することは、ソフトウェアのリファクタリングの一形態と考えることができる**(Cinnéide et al., 2016)
Similar to software refactoring, where related code modules are restructured and consolidated to eliminate redundancy and improve maintainability, model consolidation can be thought of as combining different prediction tasks into a single model, and leveraging shared knowledge and representations.
ソフトウェアのリファクタリング(関連するコードモジュールを再構築して統合し、冗長性を排除して保守性を向上させること)と同様に、**モデルの統合は、異なる予測タスクを単一のモデルに統合し、共有された知識と表現を活用すること**と考えることができる。
There are several benefits to this.
これにはいくつかの利点がある。

## モデル統合の利点1: Reduced code and deployment footprint コードとデプロイのフットプリント(=コスト?)を削減

Supporting a new ML model requires significant investment in code, data and computational resources.
新しいMLモデルをサポートするには、コード、データ、計算リソースに多大な投資が必要である。
There is complexity involved in setting up training pipelines to generate labels, features, train the model and manage deployments.
ラベル、特徴の生成、モデルのトレーニング、デプロイの管理など、トレーニングパイプラインの設定には複雑さが伴う。(うんうん:thinking:)
Maintaining such pipelines requires constant upgrades to underlying software frameworks and rolling out bug fixes.
このようなパイプラインを維持するには、基盤となるソフトウェアフレームワークを常にアップグレードし、バグフィックスを展開する必要がある。
Model consolidation acts as an essential leverage in reducing such costs.
モデルの統合は、そうしたコストを削減するために不可欠なテコの役割を果たす。

## モデル統合の利点2: Improved Maintainability 保守性の向上

Production systems must have high availability: any problems must be detected and resolved quickly.
生産システムは**高い可用性**(=正常に稼働している時間の割合が高い状況)を持たなければならない: いかなる問題も迅速に検出され、解決されなければならない。
ML Teams often have on-call rotations to ensure continuity of operation.
MLチームは、業務の継続性を確保するため、しばしばon-callのローテーションを組んでいる。
(on-call rotations: 開発チームのメンバーが定期的にシフト制で当番になり、システムやサービスの運用中に発生する問題や障害に対応する役割を担当すること。運用当番か:thinking:)
A single unified code base makes the on-call work easier.
**単一の統一されたコードベースは、on-call作業を容易にする**。(確かに:thinking:)
The benefits include little to no context switching for the on-call, homogeneity of workflows, fewer points of failures, and fewer lines of code.
その利点とは、on-call時のcontext切り替えがほとんどないこと、ワークフローの均質性、障害発生ポイントの少なさ、コード行数の少なさなどである。

## モデル統合の利点3:Apply Model Advancements Quickly to Multiple Canvases 複数のキャンバスにモデルの進歩を素早く適用する

Building a consolidated ML system with a multi-task model allows us to apply advancements in one use-case quickly to other use-cases.
マルチタスクモデルで統合されたMLシステムを構築することで、あるusecaseの進歩を他のusecaseに迅速に適用することができる。
For example, if a certain feature is tried for a specific use-case, the common pipeline allows us to try it for other use-cases without additional pipeline work.
例えば、ある特徴量が特定のusecaseで試された場合、共通のパイプラインを使えば、パイプラインを追加することなく、他のusecaseでも試すことができる。
There is the trade-off of potential regression for other use-cases as features are introduced for one use-case.
あるusecaseのために特徴量を導入すると、他のユースケースのモデル性能が後退する可能性があるというトレードオフはある。(1つのusecaseが足を引っ張っちゃうみたいなイメージ:thinking:)
However, in practice, this has not been a problem if the different use-cases in the consolidated model are sufficiently related.
**しかし実際には、統合モデル内の異なるusecaseが十分に関連していれば、これは問題にはなっていない**。(ふむふむ...!)

## モデル統合の利点4:Better Extensibility より良い拡張性

Consolidating multiple use cases into a single model prompts a flexible design with extra thought in incorporating the multiple use cases.
複数のusecaseを1つのモデルに統合することで、**複数のusecaseを取り込むための特別な配慮がなされた柔軟な設計が促される**。(拡張しやすいシステム設計にしよう、ってモチベーションが生まれる:thinking:)
Such essential extensibility consequently future-proofs the system.
このような本質的な拡張性は、結果的にシステムの将来を保証する。
For example, we initially designed the model training infrastructure to consolidate a few use cases.
例えば、私たちは当初、いくつかのusecaseを統合するためにモデル学習のインフラを設計した。
However, the flexible design necessitated to incorporate these multiple use cases has proved effective to onboard new model training use cases on the same infrastructure.
しかし、このような複数のusecaseを組み込むために必要な柔軟な設計は、同じインフラ上に新しいモデルトレーニングのusecaseを搭載するのに有効であることが証明された。
In particular, our approach of including variable request context schemas has simplified the process of training models for new use-cases using the same infrastructure.
特に、**可変なrequest contextスキーマを含む我々のアプローチ**は、同じインフラストラクチャを使用して、新しいusecaseのモデルをトレーニングするプロセスを簡素化した。(=モデル入力値の長さを柔軟に変更できるシステムを背計したので、統合モデル以外の単一のモデルを同じインフラで動かせるってことか...!:thinking:)

# Final Thoughts 最終的な感想

Though ML system consolidation is not a silver bullet and may not be appropriate in all cases, we believe there are many scenarios where such consolidation simplifies code, allows faster innovation and increases the maintainability of systems.
**MLシステムの統合は銀の弾丸ではないし、すべてのケースで適切であるとは限らない**が、**このような統合がコードを簡素化し、より迅速な技術革新を可能にし、システムの保守性を向上させる多くのシナリオがあると我々は信じている**。
Our experience shows that consolidating models that rank similar targets leads to many benefits, but it’s unclear whether models that rank completely different targets and have very different input features would benefit from such consolidation.
我々の経験から、似たようなターゲットをランク付けするモデル達(i.e. **各usecase間の関連性が高い場合**)を統合することは、多くの利点につながることが分かっている。
しかし、全く異なるターゲットをランク付けし、全く異なる入力特徴量を持つモデル達(i.e. 各usecase間に関連性が低い場合...!:thinking:)が、そのような統合から恩恵を受けるかどうかは不明である。
In future work, we plan to establish more concrete guidelines for when ML model consolidation is most suitable.
今後の研究では、**MLモデル統合がどのような場合に最適か**について、より具体的なガイドラインを確立する予定である。
Finally, large foundation models for NLP and recommendations might have significant impact on ML system design and could lead to even more consolidation at systems level.
最後に、**NLPや推薦のための大規模基礎モデル(=LLMってこと?)は、MLシステムの設計に大きな影響を与える可能性があり、システムレベルでの統合がさらに進む可能性がある**。

# Acknowledgements 謝辞

We thank Vito Ostuni, Moumita Bhattacharya, Justin Basilico, Weidong Zhang, and Xinran Waibel for their contributions to the ML system.
Vito Ostuni、Moumita Bhattacharya、Justin Basilico、Weidong Zhang、Xinran WaibelのMLシステムへの貢献に感謝する。
Thanks also to Anne Cocos for her valuable feedback on a previous draft.
また、前回の草稿に貴重な意見を寄せてくれたアン・ココスに感謝する。
