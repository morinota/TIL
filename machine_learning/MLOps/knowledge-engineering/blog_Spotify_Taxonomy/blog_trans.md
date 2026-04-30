refs: https://engineering.atspotify.com/2024/10/how-we-generated-millions-of-content-annotations


# How We Generated Millions of Content Annotations 私たちが数百万のコンテンツ注釈を生成した方法

With the fields of machine learning (ML) and generative AI (GenAI) continuing to rapidly evolve and expand, it has become increasingly important for innovators in this field to anchor their model development on high-quality data.
機械学習（ML）と生成AI（GenAI）の分野が急速に進化し拡大し続ける中で、この分野の革新者が**高品質なデータに基づいてモデル開発を行うことがますます重要に**なっています。

As one of the foundational teams at Spotify focused on understanding and enriching the core content in our catalogs, we leverage ML in many of our products.
私たちは、**Spotifyのカタログ内のコアコンテンツを理解し、豊かにすることに焦点を当てた基盤チーム**の1つであり、私たちの多くの製品でMLを活用しています。
For example, we use ML to detect content relations so a new track or album will be automatically placed on the right Artist Page.
例えば、私たちはMLを使用してコンテンツの関係を検出し、新しいトラックやアルバムが自動的に正しいアーティストページに配置されるようにしています。
We also use it to analyze podcast audio, video, and metadata to identify platform policy violations.
また、ポッドキャストの音声、ビデオ、メタデータを分析してプラットフォームポリシーの違反を特定するためにも使用しています。
To power such experiences, we need to build several ML models that cover entire content catalogs — hundreds of millions of tracks and podcast episodes.
このような体験を実現するためには、数億のトラックやポッドキャストエピソードをカバーするいくつかのMLモデルを構築する必要があります。
To implement ML at this scale, we needed a strategy to collect high-quality annotations to train and evaluate our models.
この規模でMLを実装するためには、**モデルを訓練し評価するための高品質な注釈を収集する戦略**が必要でした。
We wanted to improve the data collection process to be more efficient and connected and to include the right context for engineers and domain experts to operate more effectively.
私たちは、データ収集プロセスをより効率的でつながりのあるものにし、エンジニアやドメイン専門家がより効果的に操作できるように適切なコンテキストを含めることを望んでいました。

![]()
Figure 1: Ad hoc data collection processes.
図1: アドホックデータ収集プロセス

To address this, we had to evaluate the end-to-end workflow.
これに対処するために、私たちはエンドツーエンドのワークフローを評価する必要がありました。
We took a straightforward ML classification project, identified the manual steps to generate annotations, and aimed to automate them.
私たちは、シンプルなML分類プロジェクトを取り上げ、注釈を生成するための手動ステップを特定し、それらを自動化することを目指しました。

We developed scripts to sample predictions, served data for operator review, and integrated the results with model training and evaluation workflows.
予測をサンプリングするためのスクリプトを開発し、オペレーターのレビュー用にデータを提供し、結果をモデルの訓練および評価ワークフローに統合しました。

We increased the corpus of annotations by 10 times and did so with three times the improvement in annotator productivity.
私たちは注釈のコーパスを10倍に増やし、注釈者の生産性を3倍向上させることができました。

Taking that as a promising sign, we further experimented with this workflow for other ML tasks.
それを有望な兆候と捉え、私たちは他のMLタスクに対してもこのワークフローをさらに実験しました。

Once we confirmed the benefits of our approach, we decided to invest in this solution in earnest.
私たちのアプローチの利点を確認した後、私たちはこのソリューションに本格的に投資することを決定しました。

Our next objective was to define the strategy to build a platform that would scale to millions of annotations.
私たちの次の目標は、数百万の注釈にスケールするプラットフォームを構築するための戦略を定義することでした。



## Building and scaling our annotation platform 注釈プラットフォームの構築と拡張

We centered our strategy around three main pillars:  
私たちは、戦略を3つの主要な柱に中心を置きました：

1. Scaling human expertise.  
   1. 人間の専門知識の拡張。

2. Implementing annotation tooling capabilities.  
   2. 注釈ツール機能の実装。

3. Establishing foundational infrastructure and integration.  
   3. 基盤となるインフラストラクチャと統合の確立。

Figure 2: Pillars of the annotation platform.  
図2: 注釈プラットフォームの柱。



## 1. Scaling human expertise. 人間の専門知識の拡張

Figure 3: Annotation workflow diagram.  
図3: アノテーションワークフローダイアグラム。

In order to scale operations, it was imperative that we defined processes to centralize and organize our annotation resources.  
オペレーションを拡張するためには、アノテーションリソースを中央集約し整理するプロセスを定義することが不可欠でした。

We established large-scale expert human workforces in several domains to address our growing use cases, with multiple levels of experts, including the following:  
私たちは、増加するユースケースに対応するために、いくつかの分野で大規模な専門家の人材を確立し、以下のような複数の専門家レベルを設けました。

- Core annotator workforces: These workforces are domain experts, who provide first-pass review of all annotation cases.  
- コアアノテーター人材: これらの人材はドメインの専門家であり、すべてのアノテーションケースの初回レビューを提供します。

- Quality analysts: Quality analysts are top-level domain experts, who act as the escalation point for all ambiguous or complex cases identified by the core annotator workforce.  
- 品質アナリスト: 品質アナリストはトップレベルのドメイン専門家であり、コアアノテーター人材によって特定されたすべての曖昧または複雑なケースのエスカレーションポイントとして機能します。

- Project managers: This includes individuals who connect engineering and product teams to the workforce, establish and maintain training materials, and organize feedback on data collection strategies.  
- プロジェクトマネージャー: これには、エンジニアリングチームと製品チームを人材に接続し、トレーニング資料を作成・維持し、データ収集戦略に関するフィードバックを整理する個人が含まれます。

Beyond human expertise, we also built a configurable, LLM-based system that runs in parallel to the human experts.  
人間の専門知識を超えて、私たちは人間の専門家と並行して動作する構成可能なLLMベースのシステムも構築しました。

It has allowed us to significantly grow our corpus of high-quality annotation data with low effort and cost.  
これにより、低い労力とコストで高品質なアノテーションデータのコーパスを大幅に増やすことができました。



## 2. Implementing annotation tooling capabilities. アノテーションツール機能の実装

Figure 4: Annotation tooling capabilities.  
図4: アノテーションツール機能。

Although we started with a simple classification annotation project (the annotation task being answering a question), we soon realized that we had more complex use cases — such as annotating audio/video segments, natural language processing, etc. — which led to the development of custom interfaces, so we could easily spin up new projects.  
私たちはシンプルな分類アノテーションプロジェクト（アノテーションタスクは質問に答えること）から始めましたが、すぐに音声/ビデオセグメントのアノテーションや自然言語処理など、より複雑なユースケースがあることに気付きました。これにより、カスタムインターフェースの開発が進み、新しいプロジェクトを簡単に立ち上げることができるようになりました。

In addition, we invested in tools to manage backend work, such as project management, access control, and distribution of annotations across multiple experts.  
さらに、プロジェクト管理、アクセス制御、複数の専門家間でのアノテーションの配布など、バックエンド作業を管理するためのツールに投資しました。

This enabled us to deploy and run dozens of annotation projects in parallel, all while ensuring that experts remained productive across multiple projects.  
これにより、私たちは数十のアノテーションプロジェクトを並行して展開し実行できるようになり、専門家が複数のプロジェクトで生産的であり続けることを保証しました。

Another focus area was project metrics — such as project completion rate, data volumes, annotations per annotator, etc.  
もう一つの焦点は、プロジェクトメトリクスでした。プロジェクト完了率、データ量、アノテーターごとのアノテーション数などです。

These metrics helped project managers and ML teams track their projects.  
これらのメトリクスは、プロジェクトマネージャーやMLチームがプロジェクトを追跡するのに役立ちました。

We also examined the annotation data itself.  
私たちはアノテーションデータ自体も調査しました。

For some of our use cases, there were nuances in the annotation task — for example, detecting music that was overlaid in a podcast episode audio snippet.  
私たちのいくつかのユースケースでは、アノテーションタスクに微妙な違いがありました。例えば、ポッドキャストエピソードの音声スニペットに重ねられた音楽を検出することです。

In these cases, different experts may have different answers and opinions, so we started to compute an overall “agreement” metric.  
これらのケースでは、異なる専門家が異なる回答や意見を持つ可能性があるため、私たちは全体的な「合意」メトリクスを計算し始めました。

Any data points without a clear resolution were automatically escalated to our quality analysts.  
明確な解決策のないデータポイントは、自動的に私たちの品質アナリストにエスカレーションされました。

This ensures that our models receive the highest confidence annotation for training and evaluation.  
これにより、私たちのモデルはトレーニングと評価のために最高の信頼性のアノテーションを受け取ることが保証されます。



## 3. 基盤インフラストラクチャの確立と統合

Figure 5: Infrastructure to integrate with the tooling.  
図5: ツールと統合するためのインフラストラクチャ。

At Spotify’s scale, no one tool or application will satisfy all our needs — optionality is key.  
Spotifyの規模では、1つのツールやアプリケーションがすべてのニーズを満たすことはなく、選択肢が重要です。

When we designed integrations with annotation tools, we were intentional about building the right abstractions.  
私たちが注釈ツールとの統合を設計したとき、適切な抽象化を構築することに意図的でした。

They have to be flexible and adaptable to different tools so we can leverage the right tool for the right use case.  
それらは柔軟であり、異なるツールに適応できる必要があるため、適切なユースケースに対して適切なツールを活用できます。

Our data models, APIs, and interfaces are generic and can be used with multiple types of annotation tooling.  
私たちのデータモデル、API、およびインターフェースは汎用的であり、複数のタイプの注釈ツールで使用できます。

We built bindings for direct integration with ML workflows at various stages from inception to production.  
私たちは、発端から生産までのさまざまな段階でMLワークフローと直接統合するためのバインディングを構築しました。

For early/new ML development, we built CLIs and UIs for ad hoc projects.  
初期/新しいML開発のために、私たちはアドホックプロジェクト用のCLIとUIを構築しました。

For production workflows, we built integrations with internal batch orchestration and workflow infrastructure.  
生産ワークフローのために、私たちは内部バッチオーケストレーションおよびワークフローインフラストラクチャとの統合を構築しました。

Figure 6: Rate of annotations over time.  
図6: 時間に対する注釈の割合。



## Conclusion 結論

The annotation platform now allows for flexibility, agility, and speed within our annotation spaces. 
アノテーションプラットフォームは、現在、私たちのアノテーションスペース内で柔軟性、機敏性、そしてスピードを可能にしています。

By democratizing high-quality annotations, we’ve been able to significantly reduce the time it takes to develop new ML models and iterate on existing systems. 
高品質なアノテーションを民主化することで、新しいMLモデルの開発や既存システムの反復にかかる時間を大幅に短縮することができました。

Putting an emphasis from the onset on both scaling our human domain expertise and machine capabilities was key. 
最初から人間の専門知識と機械の能力の両方を拡張することに重点を置くことが重要でした。

Scaling humans without scaling technical capabilities to support them would have presented various challenges, and only focusing on scaling technically would have resulted in lost opportunities. 
彼らを支える技術的能力を拡張せずに人間を拡張することはさまざまな課題をもたらし、技術的な拡張のみに焦点を当てることは機会の喪失につながったでしょう。

It was a major investment to move from ad hoc projects to a full-scale platform solution to support ML and GenAI use cases. 
MLおよびGenAIのユースケースをサポートするために、アドホックプロジェクトからフルスケールのプラットフォームソリューションに移行することは大きな投資でした。

We continue to iterate on and improve the platform offering, incorporating the latest advancements in the industry. 
私たちは、業界の最新の進展を取り入れながら、プラットフォームの提供を継続的に反復し、改善しています。



## Acknowledgments 謝辞

A special thanks to Linden Vongsathorn and Marqia Williams for their support in launching this initiative and to the many people at Spotify today who continue to contribute to this important mission.
このイニシアティブの立ち上げに対するLinden VongsathornとMarqia Williamsの支援、そして今日Spotifyでこの重要な使命に引き続き貢献している多くの人々に特別な感謝を捧げます。

SHARE THIS ARTICLE
この記事を共有する

-
-
-
-

SHARE THIS ARTICLE
この記事を共有する

-
-
-
-

### Related articles 関連記事
#### Inside the Archive: The Tech Behind Your 2025 Wrapped Highlights アーカイブの内部：2025年のWrappedハイライトの背後にある技術
#### Our Multi-Agent Architecture for Smarter Advertising よりスマートな広告のためのマルチエージェントアーキテクチャ
#### Why We Use Separate Tech Stacks for Personalization and Experimentation パーソナライズと実験のために別々の技術スタックを使用する理由
#### Beyond Winning: Spotify’s Experiments with Learning Framework 勝利を超えて：Spotifyの学習フレームワークに関する実験

### Want to stay in the loop? 最新情報を受け取りたいですか？
Subscribe to our newsletter to never miss an update!
私たちのニュースレターに登録して、最新情報を見逃さないようにしましょう！

- Spotify.com
- Spotify Jobs
- Newsroom
- Spotify R&D Research
- Spotify for Backstage

-
-
-
-
-
-
- Legal 法律
- Privacy プライバシー
- Cookies クッキー
- About Ads 広告について

©2026Spotify AB
