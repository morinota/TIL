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
様々な推薦のユースケースがある場合、多くの推薦システムはそれぞれのユースケースを別々の機械学習タスクとして扱い、それぞれのタスクのために特注のMLモデルを訓練する。
In contrast, our approach generates recommendations for multiple use cases from a single, multi-task machine learning model.
対照的に、我々のアプローチは、単一のマルチタスク機械学習モデルから、複数のユースケースに対するレコメンデーションを生成する。
This not only improves the model performance but also simplifies the system architecture, thus improving maintainability.
これはモデルの性能を向上させるだけでなく、システム・アーキテクチャを単純化し、保守性を向上させる。
Additionally, building a common extensible framework for search and recommendations has allowed us to build systems for new use-cases faster.
さらに、検索とレコメンデーションのための共通の拡張可能なフレームワークを構築することで、新しいユースケースに対応したシステムをより早く構築できるようになった。
We describe the trade-offs we made for achieving this consolidation and lessons we learnt that can be applied generally.
この統合を達成するために行ったトレードオフと、一般的に適用できる教訓について述べる。

# Background 背景

Figure 1: Multiple use cases in a typical recommendation system
図1： 
典型的な推薦システムにおける複数のユースケース

In large real world recommender system applications like e-commerce, streaming services, and social media, multiple machine learning models are trained to optimize item recommendations for different parts of the system.
電子商取引、ストリーミングサービス、ソーシャルメディアなどの大規模な実世界のレコメンダーシステムアプリケーションでは、システムのさまざまな部分に対してアイテムの推奨を最適化するために、複数の機械学習モデルが学習される。
There are separate models for different use-cases like notifications (user-to-item recommendations), related items (item-to-item based recommendations), search (query-to-item recommendations), and category exploration (category-to-item recommendations) (Figure 1).
通知（ユーザーからアイテムへのレコメンデーション）、関連アイテム（アイテムからアイテムへのレコメンデーション）、検索（クエリからアイテムへのレコメンデーション）、カテゴリー探索（カテゴリーからアイテムへのレコメンデーション）のような、異なるユースケースに対して別々のモデルがある（図1）。
However, this can rapidly result in systems management overhead and hidden technical debt in maintaining a large number of specialized models (Sculley et al., 2015).
しかし、これはシステム管理のオーバーヘッドや、多数の専門モデルを維持するための隠れた技術的負債を急速にもたらす可能性がある(Sculley et al., 2015)。
This complexity can lead to increased long-term costs, and reduce the reliability and effectiveness of ML systems (Ehsan & Basillico, 2022).
この複雑さは長期的なコスト増につながり、MLシステムの信頼性と有効性を低下させる（Ehsan & Basillico, 2022）。

Figure 2 shows how such an ML system with model proliferation might look.
図2は、このようなモデル拡散を伴うMLシステムがどのように見えるかを示している。
The different use-cases like notifications, related items, search and category exploration have different UI canvases where the user interacts with them.
通知、関連アイテム、検索、カテゴリー探索のような異なるユースケースは、ユーザーがそれらと相互作用する異なるUIキャンバスを持っている。
ML systems for these different use-cases often evolve to have multiple offline pipelines that have similar steps such as label generation, featurization and model training.
このようなさまざまなユースケースに対応するMLシステムは、ラベル生成、特徴づけ、モデル学習といった同様のステップを持つ複数のオフラインパイプラインを持つように進化することが多い。
On the online side, different models might be hosted in different services with different inference APIs.
オンライン側では、異なるモデルが異なる推論APIを持つ異なるサービスにホストされているかもしれない。
However, there are a number of commonalities in both offline pipelines and online infrastructure, which such a design does not leverage.
しかし、オフラインのパイプラインとオンラインのインフラストラクチャーには多くの共通点があり、このような設計では活用できない。

Figure 2: Model Proliferation in ML Systems
図2： 
MLシステムにおけるモデルの増殖

In this blog, we describe our efforts to leverage the commonalities across these tasks to consolidate the offline and online stacks for these models.
このブログでは、これらのタスクの共通点を活用し、これらのモデルのオフライン・スタックとオンライン・スタックを統合する取り組みについて説明する。
This methodology not only reduces technical debt but also enhances the effectiveness of the models by leveraging knowledge gained from one task to improve another related task.
この方法論は技術的負債を減らすだけでなく、あるタスクから得た知識を別の関連タスクの改善に活用することで、モデルの有効性を高める。
Additionally, we noticed advantages in terms of efficiently implementing innovative updates across multiple recommendation tasks.
さらに、複数の推薦タスクにまたがる革新的な更新を効率的に実施できるという点でも、利点があることに気づいた。

Figure 3 shows the consolidated system design.
図3は、統合されたシステム設計を示している。
After an initial step of use-case-specific label preparation, we unify the rest of the offline pipeline and train a single multi-task model.
ユースケースに特化したラベル準備の最初のステップの後、残りのオフラインパイプラインを統一し、単一のマルチタスクモデルを訓練する。
On the online side, a flexible inference pipeline hosts models in different environments based on the latency, data freshness and other requirements, and the model is exposed via a unified canvas-agnostic API.
オンライン側では、柔軟な推論パイプラインがレイテンシー、データの鮮度、その他の要件に基づいて異なる環境でモデルをホストし、モデルはキャンバスにとらわれない統一されたAPIを介して公開される。

Figure 3: Consolidated ML System
図3： 
統合MLシステム

## Offline Design オフラインデザイン

In an offline model training pipeline, each recommendation task maps to a request context where recommendations need to be shown.
オフラインモデル学習パイプラインでは、各推薦タスクは、推奨を表示する必要があるリクエストコンテキストにマッピングされる。
The request context schema varies depending on the specific task.
リクエストコンテキストスキーマは特定のタスクによって異なる。
For instance, for query-to-item recommendation, the request context would consist of elements like the query, country, and language.
例えば、クエリから商品への推薦の場合、リクエストコンテキストはクエリ、国、言語などの要素で構成される。
On the other hand, for item-to-item recommendation, the request context would also include the source item and country information.
一方、アイテム間の推薦では、リクエストコンテキストはソースアイテムと国情報も含む。
The composition of the request context schema is tailored to suit the requirements of each recommendation task.
リクエストコンテキストスキーマの構成は、それぞれの推薦タスクの要求に合わせて調整される。

An offline pipeline trains models from logged interaction data in these stages:
オフラインのパイプラインは、これらの段階でログに記録された相互作用データからモデルを訓練する：

- Label preparation: Clean logged interaction data and generate (request_context, label) pairs. ラベルの準備： 
ログに記録されたインタラクションデータをクリーニングし、(request_context, label)のペアを生成する。

- Feature Extraction: Generate feature vectors for the above generated (request_context, label) tuples. 特徴抽出： 
上記の生成された(request_context, label)タプルの特徴ベクトルを生成する。

- Model Training: Train a model based on (feature_vector, label) rows. モデルのトレーニング： 
(feature_vector,label)行に基づいてモデルを学習する。

- Model Evaluation: Assess the performance of the trained model using appropriate evaluation metrics. モデルの評価： 
適切な評価指標を用いて学習済みモデルの性能を評価する。

- Deployment: Make the model available for online serving. 配備する： 
モデルをオンラインで提供できるようにする。

For model consolidation, we set the unified request context to the union of all context elements across tasks.
モデル連結のために、統一されたリクエストコンテキストを、タスク間の すべてのコンテキスト要素の和に設定する。
For specific tasks, missing or unnecessary context values are substituted by sentinel (default) values.
特定のタスクでは、欠落している、または不要なコンテキスト値は、センチネル（デフォルト）値で置き換えられる。
We introduce a task_type categorical variable as part of the unified request context to inform the model of target recommendation task.
推薦タスクのモデルに情報を提供するために、統一されたリクエストコンテキストの一部としてtask_typeカテゴリ変数を導入する。

In label preparation, data from each canvas are cleaned, analyzed and stored with the unified request context schema.
ラベルの準備では、各キャンバスのデータがクリーニングされ、分析され、統一されたリクエストコンテキストスキーマで保存される。
This label data from different canvases is then merged together with appropriate stratification to get a unified labeled data set.
異なるキャンバスからのこのラベルデータは、適切な層別化によって統合され、統一されたラベル付きデータセットとなる。
In feature extraction, not all features contain values for certain tasks and are filled with appropriate default values.
特徴抽出では、すべての特徴に特定のタスクの値が含まれているわけではなく、適切なデフォルト値で埋められます。

# Online Design オンラインデザイン

Serving a single ML model at-scale presents certain unique online MLOps challenges (Kreuzberger et al., 2022).
単一のMLモデルをアットスケールで提供することは、オンラインMLOps特有の課題をもたらす（Kreuzberger et al.）
Each use-case may have different requirements with respect to:
それぞれのユースケースは、以下の点に関して異なる要求を持っているかもしれない：

- Latency and throughput: Different service-level agreements (SLAs) to guarantee a latency and throughput target to deliver an optimal end-user experience. レイテンシーとスループット： 
最適なエンドユーザー・エクスペリエンスを提供するために、レイテンシーとスループットの目標を保証するさまざまなサービス・レベル・アグリーメント（SLA）。

- Availability: Different guarantees of model serving uptime, without resorting to fallbacks. 可用性： 
フォールバックに頼ることなく、さまざまなモデルのサービス稼働時間を保証。

- Candidate Sets: Different types of items (e.g. videos, games, people, etc) that may be further curated by use-case-specific business requirements. 候補セット： 
さまざまなタイプのアイテム（ビデオ、ゲーム、人物など）で、ユースケース固有のビジネス要件によってさらに分類される。

- Budget: Different budget targets for model inferencing costs. 予算： 
モデル推論コストの予算目標が異なる。

- Business Logic: Different pre- and post- processing logic. ビジネスロジック： 
処理前と処理後のロジックが異なる。

Historically, use-case-specific models are tuned to satisfy the unique requirements.
歴史的に、ユースケースに特化したモデルは、固有の要件を満たすように調整される。
The core online MLOps challenge is to support a wide variety of use-cases without regressing towards the lowest-common denominator in terms of model performance.
オンラインMLOpsの核となる課題は、モデルのパフォーマンスという点で、最小公倍数に逆行することなく、多様なユースケースをサポートすることである。

We approached this challenge by:
私たちはこの課題にこう取り組んだ：

- Deploying the same model in different system environments per use-case. Each environment has “knobs” to tune the characteristics of the model inference, including model latency, model data freshness and caching policies and, model execution parallelism. ユースケースごとに異なるシステム環境に同じモデルを展開する。 各環境には、モデルのレイテンシー、モデルデータの鮮度とキャッシュポリシー、モデルの実行並列性など、モデル推論の特性を調整するための「つまみ」がある。

- Exposing a generic, use-case-agnostic API for consuming systems. To enable this flexibility, the API enables heterogeneous context input (User, Video, Genre, etc.), heterogeneous candidate selection (User, Video, Genre, etc.), timeout configuration, and fallback configuration. システムを消費するための汎用的でユースケースにとらわれないAPIを公開する。 この柔軟性を可能にするために、APIは異種コンテキスト入力（ユーザー、ビデオ、ジャンルなど）、異種候補選択（ユーザー、ビデオ、ジャンルなど）、タイムアウト設定、フォールバック設定を可能にします。

# Lessons Learnt 教訓

Consolidating ML models into a single model can be thought of as a form of software refactoring (Cinnéide et al., 2016).
MLモデルを単一のモデルに統合することは、ソフトウェアのリファクタリングの一形態と考えることができる（Cinnéide et al.）
Similar to software refactoring, where related code modules are restructured and consolidated to eliminate redundancy and improve maintainability, model consolidation can be thought of as combining different prediction tasks into a single model, and leveraging shared knowledge and representations.
ソフトウェアのリファクタリング（関連するコードモジュールを再構築して統合し、冗長性を排除して保守性を向上させること）と同様に、モデルの統合は、異なる予測タスクを単一のモデルに統合し、共有された知識と表現を活用することと考えることができる。
There are several benefits to this.
これにはいくつかの利点がある。

## Reduced code and deployment footprint コードと配備のフットプリントを削減

Supporting a new ML model requires significant investment in code, data and computational resources.
新しいMLモデルをサポートするには、コード、データ、計算リソースに多大な投資が必要である。
There is complexity involved in setting up training pipelines to generate labels, features, train the model and manage deployments.
ラベル、特徴の生成、モデルのトレーニング、デプロイの管理など、トレーニングパイプラインの設定には複雑さが伴う。
Maintaining such pipelines requires constant upgrades to underlying software frameworks and rolling out bug fixes.
このようなパイプラインを維持するには、基盤となるソフトウェアフレームワークを常にアップグレードし、バグフィックスを展開する必要がある。
Model consolidation acts as an essential leverage in reducing such costs.
モデルの統合は、そうしたコストを削減するために不可欠なテコの役割を果たす。

## Improved Maintainability 保守性の向上

Production systems must have high availability: any problems must be detected and resolved quickly.
生産システムは高い可用性を持たなければならない： 
いかなる問題も迅速に検出され、解決されなければならない。
ML Teams often have on-call rotations to ensure continuity of operation.
MLチームは、業務の継続性を確保するため、しばしばオンコールのローテーションを組んでいる。
A single unified code base makes the on-call work easier.
単一の統一されたコードベースは、オンコール作業を容易にする。
The benefits include little to no context switching for the on-call, homogeneity of workflows, fewer points of failures, and fewer lines of code.
その利点とは、オンコール時のコンテキスト切り替えがほとんどないこと、ワークフローの均質性、障害発生ポイントの少なさ、コード行数の少なさなどである。

## Apply Model Advancements Quickly to Multiple Canvases 複数のキャンバスにモデルの進歩を素早く適用する

Building a consolidated ML system with a multi-task model allows us to apply advancements in one use-case quickly to other use-cases.
マルチタスクモデルで統合されたMLシステムを構築することで、あるユースケースの進歩を他のユースケースに迅速に適用することができる。
For example, if a certain feature is tried for a specific use-case, the common pipeline allows us to try it for other use-cases without additional pipeline work.
例えば、ある機能が特定のユースケースで試された場合、共通のパイプラインを使えば、パイプラインを追加することなく、他のユースケースでも試すことができる。
There is the trade-off of potential regression for other use-cases as features are introduced for one use-case.
あるユースケースのために機能を導入すると、他のユースケースのために機能が後退する可能性があるというトレードオフがある。
However, in practice, this has not been a problem if the different use-cases in the consolidated model are sufficiently related.
しかし実際には、連結モデル内の異なるユースケースが十分に関連していれば、これは問題にはなっていない。

## Better Extensibility より良い拡張性

Consolidating multiple use cases into a single model prompts a flexible design with extra thought in incorporating the multiple use cases.
複数のユースケースを1つのモデルに統合することで、複数のユースケースを取り込むための特別な配慮がなされた柔軟な設計が促される。
Such essential extensibility consequently future-proofs the system.
このような本質的な拡張性は、結果的にシステムの将来を保証する。
For example, we initially designed the model training infrastructure to consolidate a few use cases.
例えば、私たちは当初、いくつかのユースケースを統合するためにモデル・トレーニングのインフラを設計した。
However, the flexible design necessitated to incorporate these multiple use cases has proved effective to onboard new model training use cases on the same infrastructure.
しかし、このような複数のユースケースを組み込むために必要な柔軟な設計は、同じインフラ上に新しいモデルトレーニングのユースケースを搭載するのに有効であることが証明された。
In particular, our approach of including variable request context schemas has simplified the process of training models for new use-cases using the same infrastructure.
特に、可変リクエストコンテキストスキーマを含む我々のアプローチは、同じインフラストラクチャを使用して、新しいユースケースのモデルをトレーニングするプロセスを簡素化した。

# Final Thoughts 最終的な感想

Though ML system consolidation is not a silver bullet and may not be appropriate in all cases, we believe there are many scenarios where such consolidation simplifies code, allows faster innovation and increases the maintainability of systems.
MLシステムの統合は銀の弾丸ではないし、すべてのケースで適切であるとは限らないが、このような統合がコードを簡素化し、より迅速な技術革新を可能にし、システムの保守性を向上させる多くのシナリオがあると我々は信じている。
Our experience shows that consolidating models that rank similar targets leads to many benefits, but it’s unclear whether models that rank completely different targets and have very different input features would benefit from such consolidation.
しかし、全く異なるターゲットをランク付けし、全く異なる入力特徴を持つモデルが、そのような統合から恩恵を受けるかどうかは不明である。
In future work, we plan to establish more concrete guidelines for when ML model consolidation is most suitable.
今後の研究では、MLモデル連結がどのような場合に最適かについて、より具体的なガイドラインを確立する予定である。
Finally, large foundation models for NLP and recommendations might have significant impact on ML system design and could lead to even more consolidation at systems level.
最後に、NLPやレコメンデーションのための大規模な基礎モデルは、MLシステムの設計に大きな影響を与える可能性があり、システムレベルでの統合がさらに進む可能性がある。

# Acknowledgements 謝辞

We thank Vito Ostuni, Moumita Bhattacharya, Justin Basilico, Weidong Zhang, and Xinran Waibel for their contributions to the ML system.
Vito Ostuni、Moumita Bhattacharya、Justin Basilico、Weidong Zhang、Xinran WaibelのMLシステムへの貢献に感謝する。
Thanks also to Anne Cocos for her valuable feedback on a previous draft.
また、前回の草稿に貴重な意見を寄せてくれたアン・ココスに感謝する。