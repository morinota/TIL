## refs: refs：

https://www.hopsworks.ai/post/the-enterprise-journey-to-introducing-a-software-factory-for-ai-systems
https://www.hopsworks.ai/post/the-enterprise-journey-to-introducing-a-software-factory-for-ai-systems

# The Enterprise Journey to introducing a Software Factory for AI Systems -The Journey from Artisanal ML to ML Infrastructure- -職人的MLからMLインフラへの旅- # AIシステム用ソフトウェア工場導入への企業の旅 -職人的MLからMLインフラへの旅

## TL;DR ♪ TL;DR

Despite all the hype around GenAI, building AI systems is still a hard slog.
GenAIがもてはやされているにもかかわらず、AIシステムの構築は依然として困難な作業である。
At most organizations, it’s a time consuming, artisanal activity.
ほとんどの組織では、それは時間のかかる職人的な活動だ。
In this article, we introduce a blueprint for a software factory for AI that shows you how to both decompose an AI system into independent, modular components (ML pipelines) that can then later be (trivially) composed into an AI system.
この記事では、AIシステムを独立したモジュラー・コンポーネント（MLパイプライン）に分解し、それを後で（些細なことだが）AIシステムとして構成する方法を示す、AIのためのソフトウェア工場の青写真を紹介する。
Just like a factory, each ML pipeline will play a well-defined role in transforming the historical input data into features and models, and new input data into predictions.
工場のように、各MLパイプラインは、過去の入力データを特徴量とモデルに変換し、新しい入力データを予測に変換する明確な役割を果たす。
We will pay attention to reuse of outputs to keep costs down and improve quality.
コストを抑え、品質を向上させるために、アウトプットの再利用に注意を払う。
The main contribution of this article is a software architecture that includes a shared data layer and a new taxonomy for the data transformations that translate input data to features, features to models, and new data into predictions.
本稿の主な貢献は、共有データレイヤーと、入力データを特徴量に、特徴量をモデルに、そして新しいデータを予測に変換するデータ変換のための新しい分類法を含むソフトウェアアーキテクチャである。

## The need for a Software Factory for AI Systems AIシステムのためのソフトウェア工場の必要性

The largest and most profitable software companies are generating huge amounts of value through AI, while the (silent) majority of Enterprises are not.
最大手で最も収益性の高いソフトウェア企業は、AIによって莫大な価値を生み出しているが、大多数の企業はそうではない。
That is a commonly heard refrain with more than a grain of truth to it.
それはよく耳にする言葉だが、一粒以上の真実がある。
The companies that deliver huge value through applied AI (from Facebook to Google to Salesforce to Github) have built their own software factories for building and maintaining AI systems.
応用AIによって巨大な価値を提供する企業（フェイスブック、グーグル、セールスフォース、Githubなど）は、AIシステムの構築と保守のための独自のソフトウェア工場を構築している。
They do not follow the decentralized approach, see Figure 1, where many parallel organic initiatives at an organization deliver varied results.
図1を参照されたい。組織内で多くの並列的な有機的イニシアチブがさまざまな結果をもたらすような、分散型アプローチには従わない。

![figure1]()

However, many organizations start their AI journey with no centralized policy or platform team for AI system development, with the result that many teams take local initiatives to add AI to their products or services, using their own choice of tools and platforms.
しかし、多くの組織は、AIシステム開発のための一元化された方針やプラットフォームチームを持たずにAIの旅を始める。その結果、多くのチームは、独自のツールやプラットフォームを使用して、製品やサービスにAIを追加するためのローカルイニシアチブを取る。
In my experience, from working with companies that are at different points in their AI journey, it is often Team D from Figure 1 who have a large voice in the future of AI at the company.
私の経験では、AIの旅路のさまざまな段階にある企業と仕事をする中で、企業におけるAIの将来について大きな発言力を持っているのは、図1のチームDであることが多い。
They are the ‘hacker’ team that have managed to successfully build an AI powered product that is delivering value today.
彼らは、今日価値を提供しているAI搭載製品の構築に成功した「ハッカー」チームなのだ。
In contrast to the data science dominated Team A, who lacked the software infrastructure skills to productionize their promising models, the more experienced software developers in Team D concentrated on starting small, getting a working ML system first, and only later refining the AI that powers their product.
データサイエンスが支配的なチームAは、有望なモデルを製品化するためのソフトウェア・インフラのスキルに欠けていたのとは対照的に、チームDの経験豊富なソフトウェア開発者たちは、まず小規模なMLシステムを稼働させ、製品の動力源となるAIを後から改良することに集中した。
One lesson they learnt was that following a DevOps software development process worked for them.
彼らが学んだ教訓のひとつは、DevOpsソフトウェア開発プロセスに従うとうまくいくということだった。
However, are the lessons learnt by Team D a blueprint for success in AI for the organization as a whole?
しかし、チームDが学んだ教訓は、組織全体がAIで成功するための青写真なのだろうか？

## Brief History of Modular AI Systems (Real-Time and Batch) モジュラーAIシステム（リアルタイムとバッチ）の簡単な歴史

Team D successfully applied some established techniques for handling complexity when building software systems:
チームDは、ソフトウェアシステムを構築する際に複雑さを処理するための確立されたテクニックを応用することに成功した：

decompose systems into smaller manageable modular components;
システムをより小さな管理しやすいモジュラー・コンポーネントに分解する；

design the modular components in such a way that they can be easily composed into a complete AI system;
モジュラー・コンポーネントを、完全なAIシステムに簡単に構成できるように設計する；

Team D also did their homework on machine learning engineering.
チームDは機械学習工学の宿題もこなした。
Some features needed to be precomputed and retrieved at runtime to hit their SLA, so they used a Postgres database to store and retrieve them and wrote a separate data pipeline for each model.
SLAを達成するために、いくつかの機能は事前に計算され、実行時に取得される必要があった。そのため、Postgresデータベースを使用してそれらを保存および取得し、モデルごとに個別のデータパイプラインを作成した。
They knew enough to avoid pitfalls such as skew between training and serving, so they logged all predictions to a single wide table and waited to collect enough training data.
彼らは、トレーニングとサービス間のスキューのような落とし穴を避けるために、すべての予測を単一のワイドテーブルに記録し、十分なトレーニングデータが集まるのを待った。
This one-big-table data model avoids data leakage that can arise when your data is spread across multiple tables and you need to perform a temporal Join across tables when creating training data.
この1つのビッグテーブル・データ・モデルにより、データが複数のテーブルにまたがっていて、トレーニング・データを作成する際にテーブル間でテンポラル・ジョインを実行する必要がある場合に発生する可能性のあるデータ漏れを回避することができます。

Team A did not follow this approach as they did not have the software development skills to build the CI/CD pipelines, containerize the different modules in the ML system, and operate and instrument the microservice architecture used to deliver the operational ML system.
チームAは、CI/CDパイプラインを構築し、MLシステムのさまざまなモジュールをコンテナ化し、運用可能なMLシステムを提供するために使用されるマイクロサービスアーキテクチャを運用し、インストゥルメントするためのソフトウェア開発スキルを持っていなかったため、このアプローチには従わなかった。
So Team A just concentrated on making their models better, which ultimately did not deliver value to the business.
そのため、チームAは自分たちのモデルをより良くすることだけに集中し、結局はビジネスに価値を提供することはできなかった。
Models stuck in notebooks add no value to the business.
ノートに詰まったモデルはビジネスに何の価値ももたらさない。

![figure2]()

Team D later helped Team B (the marketing team with a data engineer) build a batch ML system that helped predict subscriber churn.
チームDはその後、チームB（データエンジニアを擁するマーケティングチーム）のバッチMLシステム構築を支援し、加入者の解約を予測した。
For Team D, this was a more straightforward project, as it was a single monolithic batch ML system.
チームDにとっては、モノリシックなバッチMLシステム1つという、より単純なプロジェクトだった。
Their ML system as a dataflow program - a directed acyclic graph of steps - executed by an orchestrator, see Figure 3.
彼らのMLシステムは、オーケストレーターによって実行されるデータフロー・プログラム（ステップの有向非循環グラフ）である（図3を参照）。
One difficult challenge they faced was in creating training data.
彼らが直面した困難な課題は、トレーニングデータの作成だった。
The data was spread over many tables - user engagement, marketing actions, session data, and so on.
データは、ユーザーエンゲージメント、マーケティングアクション、セッションデータなど、多くのテーブルにまたがっていた。
Team D realized temporal joins would be needed to create rich training data, and there was a risk of data leakage if they didn’t get them right.
チームDは、豊富なトレーニングデータを作成するためには一時的な結合が必要であり、それを正しく行わなければデータ漏洩のリスクがあることに気づいた。
So being the good engineers they are, they followed the KISS principle and used only the user engagement data for their model, as they hypothesized this data had the most predictive power for subscriber churn.
そこで、優秀なエンジニアである彼らは、KISSの原則に従い、ユーザー・エンゲージメント・データのみをモデルに使用した。
Unfortunately, neither Team D nor Team B were experts at data science, and the model they built was too trivial (it had low predictive power) and ultimately did not significantly impact the bottom line.
残念ながら、チームDもチームBもデータサイエンスの専門家ではなく、彼らが構築したモデルはあまりに些細なもの（予測力が低い）であり、最終的に収益に大きな影響を与えることはなかった。
They also skipped on monitoring their features/predictions for drift, instead committing to retraining the model every 6 months.
彼らはまた、特徴や予測のドリフトを監視することをスキップし、代わりに6ヶ月ごとにモデルを再トレーニングすることを約束した。
But their model made it to production - in contrast to our Team A of data scientists.
しかし、データサイエンティストのチームAとは対照的に、彼らのモデルは本番稼動にこぎつけた。
Team A, in contrast, made fun of the churn model when they found out about it.
対照的にチームAは、解約モデルを知ったとき、それをバカにしていた。

![figure3]()

As you can see, the software architectures of the real-time ML system (Figure 2) and batch ML system (Figure 3) are radically different.
ご覧のように、リアルタイムMLシステム（図2）とバッチMLシステム（図3）のソフトウェア・アーキテクチャは根本的に異なる。
Team D has some crack developers who were comfortable switching development paradigms and tooling, and pulled it off for real-time and got something working for batch.
チームDには、開発パラダイムやツールの切り替えに慣れている優秀な開発者が何人かいて、リアルタイムでそれをやり遂げ、バッチで何かを使えるようにした。
So what did the organization learn from its decentralized ML initiatives?
では、分散型MLの取り組みから、この組織は何を学んだのだろうか？

Team D drew conclusions that real-time AI systems could be built as microservices architectures and batch AI systems should be orchestrated DAGs.
チームDは、リアルタイムAIシステムはマイクロサービス・アーキテクチャとして構築でき、バッチAIシステムはオーケストレーションされたDAGであるべきだという結論を導き出した。
However, there are some issues.
しかし、問題もある。
While the microservices architecture is modular, it is not easy to compose AI systems as graphs of independent microservices.
マイクロサービス・アーキテクチャはモジュール化されているが、AIシステムを独立したマイクロサービスのグラフとして構成するのは容易ではない。
The subsystems are tightly coupled and need to be always-on.
サブシステムは緊密に結合しており、常にオンである必要がある。
If a microservice is “down”, it can lead to the entire ML system being down.
マイクロサービスが 「ダウン 」すれば、MLシステム全体のダウンにつながる。
The call depth for microservices can be deep and you need great observability tools for tracing calls and monitoring services.
マイクロサービスのコールの深さは深く、コールをトレースしてサービスを監視するための優れた観測可能性ツールが必要です。
They couldn’t use serverless functions to implement microservices due to high latencies that break SLAs during cold-starts.
コールドスタート時にSLAを破る高いレイテンシーのため、マイクロサービスを実装するためにサーバーレス関数を使用することができなかった。
If they hadn’t had the same low latency SLA, they would have looked at designing their microservices as loosely coupled serverless functions that communicate by passing events through a serverless database (like DynamoDB) or a shared event bus, such as Kafka or AWS Kinesis or GCP PubSub.
もし彼らが同じ低レイテンシーSLAを持っていなかったとしたら、彼らはマイクロサービスを、（DynamoDBのような）サーバーレスデータベースや、KafkaやAWS Kinesis、GCP PubSubのような共有イベントバスを介してイベントを渡すことで通信する、疎結合のサーバーレス関数として設計することを検討しただろう。

Then, there is the cost.
それからコストだ。
Deploying a new microservice is not trivial for the Data Science team.
新しいマイクロサービスのデプロイは、データサイエンスチームにとって些細なことではない。
You need to build your container, set up a CI/CD platform to deploy containers in a runtime (like Kubernetes) and connect your microservices to the other microservices and existing services.
コンテナを構築し、（Kubernetesのような）ランタイムにコンテナをデプロイするCI/CDプラットフォームをセットアップし、マイクロサービスを他のマイクロサービスや既存のサービスに接続する必要がある。
You need to develop your microservices so that they correctly perform service discovery and handle service connection/disconnection events correctly.
サービス・ディスカバリーを正しく実行し、サービスの接続／切断イベントを正しく処理するように、マイクロサービスを開発する必要がある。
This is all hard work, and definitely not the work of data scientists, or even many ML engineers.
これはすべて大変な仕事であり、データサイエンティストや多くのMLエンジニアの仕事ではないことは間違いない。
 That is a common reason teams often “start with batch AI systems”.
 これが、チームがしばしば「バッチAIシステムから始める」一般的な理由である。
Only the highest value real-time AI systems get deployed first.
最も価値の高いリアルタイムAIシステムだけが最初に導入される。
Then, making those real-time AI systems highly available and reusing assets created between different real-time AI systems are just roadmap items for even Team D.
そして、それらのリアルタイムAIシステムを高可用性にし、異なるリアルタイムAIシステム間で作成された資産を再利用することは、チームDにとってもロードマップ項目に過ぎない。

## MLOps Infrastructure MLOps インフラストラクチャー

So, what should the organization do now? Should it just work on batch AI systems and only in exceptional cases approve real-time AI systems? Is there an alternative? How do the hyperscale AI companies spit out new AI systems at low cost and with high quality? Could we do the same? The answer is that the hyperscalers have all built their own ML infrastructure to support AI systems, see Figure 3.
では、組織は今何をすべきなのか？バッチAIシステムに取り組み、例外的な場合にのみリアルタイムAIシステムを承認すればいいのだろうか？代替案はあるのだろうか？ハイパースケールAI企業は、どのようにして新しいAIシステムを低コストかつ高品質で送り出しているのだろうか？我々も同じことができるだろうか？その答えは、ハイパースケーラー各社がAIシステムをサポートする独自のMLインフラを構築していることだ（図3を参照）。
Most of them (AWS, Databricks, Snowflake, Twitter, Spotify, Uber, WeChat) have presented their ML infrastructure at the feature store summit (videos available).
ほとんどの企業（AWS、Databricks、Snowflake、Twitter、Spotify、Uber、WeChat）は、フィーチャーストア・サミットでMLインフラを発表した（ビデオあり）。
All of them have implemented Feature Store-based data architectures and a model management infrastructure to solve most of the problems identified earlier:
いずれもフィーチャーストアをベースとしたデータアーキテクチャとモデル管理インフラを導入し、先に挙げた問題のほとんどを解決している：

decompose the problem of building AI systems into modular ML pipelines that are easily composed together into a system using the shared data layer;
AIシステム構築の問題を、共有データレイヤーを使ってシステムに簡単に組み込めるモジュール化されたMLパイプラインに分解する；

decouple ML pipelines enabling independent scheduling and the use of the best technology for each ML pipeline;
MLパイプラインを切り離すことで、独立したスケジューリングが可能になり、各MLパイプラインに最適なテクノロジーを使用できるようになります；

support for creating point-in-time consistent training data;
ポイント・イン・タイムで一貫性のあるトレーニングデータの作成をサポート；

low-latency access to precomputed features for real-time ML systems;
リアルタイムMLシステムのために、事前に計算された特徴量に低レイテンシでアクセスできる；

real-time features computed using data only available at request-time;
リクエスト時にのみ利用可能なデータを使用して計算されたリアルタイムの機能；

data validation for feature pipelines, ensuring no garbage-in;
フィーチャー・パイプラインのデータ・バリデーション；

unified batch and real-time support for both feature monitoring and model monitoring;
機能モニタリングとモデルモニタリングの両方をバッチおよびリアルタイムで統合サポート；

out-of-the-box observability and governance, using versioning, tagging, search and lineage services;
バージョニング、タグ付け、検索、リネージ・サービスを利用することで、すぐに利用可能な観察可能性とガバナンスを実現する；

high availability and enterprise level security.
高可用性と企業レベルのセキュリティ

![figure4]()

In a previous blog, and shown in Figure 3, we outlined what these ML platforms have in common.
以前のブログで、図3に示すように、これらのMLプラットフォームに共通するものを概説した。
AI systems consist of primarily three classes of ML pipelines (feature pipelines , training pipelines, and inference pipelines) that communicate via a shared data layer, consisting of a feature store and a model registry.
AIシステムは、主に3つのクラスのMLパイプライン（特徴パイプライン、学習パイプライン、推論パイプライン）で構成され、特徴ストアとモデルレジストリからなる共有データ層を介して通信する。
Somebody in Team D happened to read that blog entry, and designed Table 1, comparing the different approaches to building AI systems.
チームDの誰かがたまたまそのブログエントリーを読み、AIシステム構築のさまざまなアプローチを比較した表1をデザインした。

![table1]()

Microservices are not, however, as composable as ML pipelines.
しかし、マイクロサービスはMLパイプラインほどコンポーザブルではない。
ML Pipelines can be scheduled to run as batch systems or microservices (always-on) or stream processing systems.
MLパイプラインは、バッチシステム、マイクロサービス（常時稼働）、ストリーム処理システムとして実行するようにスケジュールできる。
Upgrading versions is straightforward - you do not need to stop upstream and downstream clients while upgrading.
バージョンのアップグレードは簡単で、アップグレード中に上流と下流のクライアントを停止する必要はありません。

When planning their AI strategy, the executive team needed a summary of Table 1, so Team D developed Table 2.
AI戦略を立案する際、経営陣は表1の要約を必要としたため、チームDは表2を作成した。

![table2]()

So, after a long journey, developing and deploying both batch AI systems and real-time AI systems, our organization takes the decision to move towards the software factory approach for building AI systems, using ML pipelines with shared ML infrastructure (feature store, model registry, experiment tracking, model serving).
そこで、バッチAIシステムとリアルタイムAIシステムの両方を開発し、デプロイする長い旅の後、私たちの組織は、共有MLインフラストラクチャ（フィーチャーストア、モデルレジストリ、実験トラッキング、モデルサービング）を備えたMLパイプラインを使用して、AIシステムを構築するためのソフトウェアファクトリーアプローチに移行することを決定しました。
They want to have the same infrastructure as the Hyperscale AI companies so that AI can become a core part of their value proposition.
ハイパースケールAI企業と同じインフラを持つことで、AIが自社の価値提案の中核となることを望んでいるのだ。

## Build or Buy the MLOps Infrastructure? MLOpsインフラを構築するか購入するか？

The next question facing our organization is whether to build or buy the ML infrastructure.
私たちの組織が直面している次の問題は、MLインフラを構築するか購入するかということです。
This is not a simple question, nor is it something that is unique to organizations that are considering their alternatives with regards to any kind of data infrastructure.
これは単純な問題ではないし、あらゆる種類のデータインフラに関して代替案を検討している組織特有の問題でもない。
Given enough time and resources, large engineering organizations can pull off any infrastructure component themselves, as has been elaborately proven by many of the hyperscalers  mentioned above.
十分な時間とリソースがあれば、大規模なエンジニアリング組織は、どんなインフラ・コンポーネントも自分たちで完成させることができる。

![figure4]()

However, for the typical enterprise, considering their options with regards to their MLOps infrastructure landscape, this is not a straightforward question.
しかし、一般的な企業にとって、MLOpsのインフラ環境に関する選択肢を検討することは、一筋縄ではいかない。
In fact, it is complicated by the very nature of the problem:
実際、問題の本質が複雑なのだ：

On the one hand, we want to move fast, be nimble and lean, and prove value quickly in the early parts of the machine learning and AI journey.
一方では、機械学習とAIの旅の初期段階において、素早く動き、機敏で無駄がなく、素早く価値を証明したいと考えている。
That will often mean taking shortcuts, and duct-taping infrastructure together - and that is fine in these early days.
それはしばしば、近道をしたり、インフラをダクトテープでくっつけたりすることを意味する。

On the other hand, we want to get to production quickly, as soon as we have proven the value and as soon as we understand that the machine learning and AI initiative will be more than just an experiment.
その一方で、価値を証明し、機械学習とAIの取り組みが単なる実験以上のものになることを理解したら、すぐにでも本番に持ち込みたい。

This will greatly impact the timing and the balance of the build versus buy decision.
これは、建設と購入の決断のタイミングとバランスに大きく影響する。

In this decision, different factors should be taken into account.
この決定には、さまざまな要素を考慮に入れる必要がある。
However, it seems clear that they fall into three proverbial buckets:
しかし、彼らが3つのバケツに分類されることは明らかなようだ：

Strategic parameters, that have everything to do with the way that the organization and the project can deal with the manpower, competencies and costs associated with both the build or the buy decision.
戦略的パラメーターとは、その組織とプロジェクトが、建設か購入かの決断に関連する人員、能力、コストに対処する方法に関係するものである。

Technical parameters that concern the nature of a feature store architecture and the intricate complexities that come with this.
フィーチャーストア・アーキテクチャーの性質と、それに伴う複雑な技術的パラメータ。

We will not discuss these parameters in this article here in detail, but will instead refer to this page on the Hopsworks website, which discusses this in greater detail.
この記事では、これらのパラメーターについて詳しく説明することはしないが、代わりにホップワークスのウェブサイトのこのページを参照してほしい。
It should, of course be clear, that at Hopsworks we think of it as our everyday mission to make sure that you will not have to worry about this build versus buy decision, and that it would be all the more obvious that you can productively start using the Hopsworks platform as early as you want, whatever the use case of your project might be.
もちろん、ホップワークスでは、お客様がこのビルドか購入かの決断に悩む必要がないようにすることを日常的な使命と考えており、お客様のプロジェクトのユースケースが何であろうと、お客様が望むだけ早くホップワークスプラットフォームを生産的に使い始めることができるようにすることは、より明白であるべきです。

## Summary 要約

The typical Enterprise journey to creating value with AI involves decentralized experimentation, followed by first value-added services being built with bespoke solutions, to finally adopting a software factory approach to building and maintaining AI systems.
AIで価値を創造するための典型的な企業の道のりには、分散化された実験、オーダーメイドのソリューションで構築される最初の付加価値サービス、そして最終的にAIシステムの構築と保守にソフトウェア工場のアプローチを採用することが含まれる。
The hyperscale AI companies built their own software factories, but the next wave of Enterprises should probably buy their ML infrastructure, as the cost and time-to-market trade-offs are now heavily in favor of buying.
ハイパースケールAI企業は自社でソフトウェア工場を建設したが、次の波はMLインフラを購入すべきだろう。