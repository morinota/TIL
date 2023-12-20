## link リンク

https://www.moderndatastack.xyz/category/feature-store
https://www.moderndatastack.xyz/category/feature-store

# What is a Feature Store? フィーチャーストアとは何か？

Feature stores orchestrate the data processes that power ML models.
フィーチャーストアは、MLモデルにパワーを与えるデータ処理をオーケストレーションする。
ML models have unique data access requirements to facilitate both model training and production inference.
MLモデルには、モデルのトレーニングと本番推論の両方を容易にするために、独自のデータアクセス要件がある。
The Feature Store serves an abstraction between your raw data, and the interfaces required by the model.
フィーチャーストアは、生データとモデルで必要とされるインターフェースの間の抽象化の役割を果たします。
Feature Stores create this abstraction by enabling data scientists to automate the processing of feature values, generate training datasets, and serve features online with production-grade service levels.
フィーチャーストアは、データサイエンティストがフィーチャー値の処理を自動化し、トレーニングデータセットを生成し、本番レベルのサービスレベルでフィーチャーをオンラインで提供できるようにすることで、この抽象化を実現します。

# Why do I need a Feature Store? なぜフィーチャーストアが必要なのか？

ML models will only ever be as good as the data that we feed to them.
MLモデルは、私たちが彼らに与えるデータと同じくらい良いものでしかない。
To deploy a model to production, data teams have to build production data pipelines to transform and serve features online.
モデルをプロダクションにデプロイするために、データチームはプロダクション・データ・パイプラインを構築し、機能を変換してオンラインで提供しなければならない。
These production ML pipelines are different from traditional analytics pipelines.
これらのプロダクションMLパイプラインは、従来のアナリティクス・パイプラインとは異なる。
They need to process both historical data for training, and fresh data for online serving.
トレーニング用の過去のデータと、オンラインサービス用の新しいデータの両方を処理する必要がある。
They must ensure training/serving parity, and provide point-in-time correctness.
トレーニング／サービングのパリティを保証し、ポイント・イン・タイムの正しさを提供しなければならない。
Features must be served online at high scale and low latency to support production workloads.
本番ワークロードをサポートするために、機能は大規模かつ低レイテンシーでオンラインに提供されなければならない。
These challenges are difficult to tackle with traditional data orchestration tools, and can often add weeks or months to the delivery time of new ML projects.
これらの課題は、従来のデータ・オーケストレーション・ツールでは取り組むことが難しく、新しいMLプロジェクトの納期に数週間から数カ月を要することが多い。

Feature Stores solve these problems by enabling data teams to:
フィーチャーストアは、データチームが以下のことを可能にすることで、これらの問題を解決する：

- Build a library of features collaboratively using standard feature definitions 標準的な機能定義を使用して、共同で機能ライブラリを構築する。

- Generate accurate training datasets with just a few lines of code わずか数行のコードで正確なトレーニングデータセットを生成

- Deploy features to production instantly using DevOps-like engineering best practices DevOpsのようなエンジニアリングのベストプラクティスを用いて、機能を即座に本番環境にデプロイする。

- Share, discover and re-use features across an organizatio 組織全体で機能を共有、発見、再利用する

# Common Components of Feature Stores フィーチャーストアの共通構成要素

The Feature Store is a relatively new concept, and so the exact definition is still evolving.
フィーチャーストアは比較的新しいコンセプトなので、正確な定義はまだ発展途上だ。
The key components of a feature store commonly include:
フィーチャーストアの主な構成要素には、一般的に以下のようなものがある：

- Feature Registry: Features are defined as version-controlled code. The feature registry contains a central catalog of all the feature definitions and feature metadata. It allows data scientists to search, discover, and collaborate on new features. フィーチャー・レジストリ： フィーチャーはバージョン管理されたコードとして定義される。 フィーチャーレジストリには、すべてのフィーチャー定義とフィーチャーメタデータの中央カタログが含まれる。 データ・サイエンティストが新機能を検索し、発見し、コラボレーションすることを可能にする。

- Transformations: Feature stores orchestrate data pipelines to transform raw data into feature values. They can consume batch, streaming, and real-time data to combine historical context with the freshest information available. 変換： フィーチャーストアは、生データをフィーチャー値に変換するデータパイプラインをオーケストレーションする。 バッチ、ストリーミング、リアルタイムのデータを利用し、過去のコンテキストと最も新しい情報を組み合わせることができる。

- Storage: Feature values are organized in feature storage. Feature stores provide both online storage for low-latency retrieval at scale, and offline storage to curate historical datasets cost-effectively. ストレージ： フィーチャー値はフィーチャーストレージに整理される。 フィーチャーストアは、低レイテンシーで大規模な検索を行うためのオンラインストレージと、過去のデータセットをコスト効率よくキュレーションするためのオフラインストレージの両方を提供する。

- Feature Serving: Feature stores provide an API endpoint to serve online feature values at low latency. フィーチャー・サービス： フィーチャーストアは、オンラインのフィーチャー値を低レイテンシーで提供するAPIエンドポイントを提供する。

- Monitoring: Feature stores monitor both data quality and operational metrics. They can validate data for correctness and detect data drift. They also monitor essential metrics related to feature storage (capacity, staleness) and feature serving (latency, throughput). モニタリング： フィーチャーストアは、データ品質と運用指標の両方を監視する。 データが正しいかどうかを検証し、データのドリフトを検出することができる。 また、特徴ストレージ（容量、陳腐化）および特徴サービング（待ち時間、スループット）に関連する重要なメトリクスも監視する。

# What to Look for When Choosing a Feature Store フィーチャーストアを選ぶ際のポイント

Users now have plenty of feature store offerings to choose from.
現在、ユーザーは多くの機能ストアの中から選ぶことができる。
AWS, Databricks, Google Cloud, Tecton, and Feast (open source) all come to mind.
AWS、Databricks、Google Cloud、Tecton、Feast（オープンソース）などが思い浮かぶ。
However, not all feature stores are created equal.
しかし、すべてのフィーチャーストアが同じように作られているわけではない。
The main things a user should pay attention to when choosing an offering are:
ユーザーがオファーを選ぶ際に注意すべき主な点は以下の通りである：

- Ecosystem and integrations: Some feature stores are tightly integrated with a very specific ecosystem. The AWS SageMaker feature store, for example, is designed to work well with the SageMaker ecosystem. Other feature stores, like Feast, are not tied to a specific ecosystem and work across clouds. Are you fully bought into a specific ecosystem or looking for a more flexible solution? エコシステムと統合： 一部のフィーチャーストアは、非常に特定のエコシステムと緊密に統合されている。 例えば、AWS SageMakerフィーチャーストアは、SageMakerエコシステムとうまく連携するように設計されています。 Feastのような他のフィーチャーストアは、特定のエコシステムに縛られず、クラウド全体で機能する。 特定のエコシステムを完全に買い込んでいるのか、それともより柔軟なソリューションを探しているのか。

- Delivery model: Some feature stores, like Tecton, are offered as fully-managed services. Other feature stores, like Feast, need to be self-deployed and managed. Do you prefer the flexibility of self-managed solutions or the ease of fully-managed services? 配信モデル： テクトンのように、フルマネージドサービスとして提供されるフィーチャーストアもある。 Feastのような他のフィーチャーストアは、自分でデプロイして管理する必要がある。 セルフマネージド・ソリューションの柔軟性と、フルマネージド・サービスの手軽さのどちらがお好みですか？

- Data infrastructure: Most feature stores are designed to orchestrate data flows on top of existing infrastructure. The Databricks feature store, for example, is designed to operate on Delta Lake. Some feature stores include their own data infrastructure including object storage and key-value stores. Do you prefer to re-use existing data infrastructure, or deploy new data infrastructure from scratch? データインフラ： ほとんどのフィーチャーストアは、既存のインフラストラクチャの上でデータフローをオーケストレーションするように設計されている。 例えば、DatabricksのフィーチャーストアはDelta Lake上で動作するように設計されている。 フィーチャーストアの中には、オブジェクトストレージやキーバリューストアを含む独自のデータインフラストラクチャを含むものもある。 既存のデータインフラを再利用するか、ゼロから新しいデータインフラを導入するか。

- Scope of feature management: The majority of feature stores are focused on solving the serving problem. They provide a consistent way to store and serve feature values, but those feature values have to be processed outside of the feature store. Other feature stores, like Tecton, manage the complete lifecycle of features - including feature transformations and automated pipelines. The latter is particularly useful if you’re doing complex transformations like streaming or real-time features. 機能管理の範囲： フィーチャーストアの大半は、サービング問題の解決に焦点を当てている。 これらは、特徴値を保存して提供するための一貫した方法を提供するが、それらの特徴値は特徴ストアの外部で処理されなければならない。 Tectonのような他のフィーチャーストアは、フィーチャーの変換や自動パイプラインなど、フィーチャーのライフサイクル全体を管理する。 後者は、ストリーミングやリアルタイム機能のような複雑な変換を行う場合に特に役立つ。

Want to learn more? You can check out Tecton’s ‘What is a Feature Store’ blog, or compare some of the leading offerings at the MLOps Community’s great feature store evaluation page here.
もっと詳しく知りたいですか？テクトンのブログ「フィーチャーストアとは」をご覧いただくか、MLOps Communityのフィーチャーストアの評価ページで、代表的な製品を比較してみてください。