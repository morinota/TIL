## refs: refs：

- CDの公式っぽい資料 [Patterns](https://continuousdelivery.com/implementing/patterns/) CDの公式っぽい資料 [パターン](https://continuousdelivery.com/implementing/patterns/)

# Patterns パターン

Linda Rising defines a pattern as “a named strategy for solving a recurring problem”.
リンダ・ライジングは、**パターンを「繰り返し起こる問題を解決するための、名前のついた戦略」**と定義している。(いい定義...!)
The concept of patterns comes from the work of architect Christopher Alexander, who observes “Each pattern describes a problem that occurs over and over again in our environment and then describes the core of the solution to that problem in such a way that you can use this solution a million times over without ever doing it the same way twice.”
パターンの概念は、建築家クリストファー・アレクサンダーの仕事から来ており、「各パターンは、私たちの環境で何度も起こる問題を記述し、その問題の解決の核心を記述する。この解決策を何百万回も使うことができ、二度と同じ方法で行うことはない」と述べている。(二度と同じ方法で??)

## The Deployment Pipeline デプロイメント・パイプライン

The key pattern introduced in continuous delivery is the deployment pipeline.
**継続的デリバリーに導入された重要なパターンは、デプロイメント・パイプライン**である。
This pattern emerged from several ThoughtWorks projects where we were struggling with complex, fragile, painful manual processes for preparing testing and production environments and deploying builds to them.
このパターンは、テスト環境と本番環境を準備し、ビルドをデプロイするための複雑で壊れやすく、**痛みを伴う手動プロセスに苦しんでいた**いくつかのThoughtWorksプロジェクトから生まれました。
We’d already worked to automate a significant amount of the regression and acceptance testing, but it was taking weeks to get builds to integrated environments for full regression testing, and our first deployment to production took an entire weekend.
**私たちはすでに、大量のリグレッションテストと受け入れテストを自動化する作業を行っていましたが、ビルドを統合環境に取り込んで完全なリグレッションテストを行うのに数週間かかり、本番環境への最初のデプロイメントには週末全体がかかっていました**。(自動化はしてたけど、時間かかってたってこと??:thinking:)

We wanted to industrialize the process of taking changes from version control to production.
私たちは、バージョン管理から本番への変更プロセスを工業化したかったのです。(これは、工芸じゃなくて工業、みたいな感じかな。スケールするようにしたい、みたいな...!:thinking:)
Our goal was to make deployment to any environment a fully automated, scripted process that could be performed on demand in minutes (on the original project we got it down to less than an hour, which was a big deal for an enterprise system in 2005).
私たちの目標は、**どの環境へのデプロイも、on-demand(=要求を受け取って?)で数分で完全に自動化されたスクリプト化されたプロセスを行う**ことでした（最初のプロジェクトでは、1時間未満にまで短縮しました。これは、2005年のエンタープライズシステムにとって大きな進歩でした）。
We wanted to be able to configure testing and production environments purely from configuration files stored in version control.
私たちは、バージョン管理に保存された設定ファイルからテスト環境と本番環境を純粋に設定できるようにしたかった。
The apparatus we used to perform these tasks (usually in the form of a bunch of scripts in bash or ruby) became known as deployment pipelines, which Dan North, Chris Read and I wrote up in a paper presented at the Agile 2006 conference.
**これらのタスクを実行するために使用した装置(通常はbashやrubyのスクリプトの形で)は、デプロイメント・パイプラインとして知られるようになり**、Dan North、Chris Read、私たちが2006年のアジャイル会議で発表した論文に記載されました。

In the deployment pipeline pattern, every change in version control triggers a process (usually in a CI server) which creates deployable packages and runs automated unit tests and other validations such as static code analysis.
deployment pipeline patternでは、**バージョン管理におけるすべての変更が、デプロイ可能なpackageを作成し**、自動ユニットテストや静的コード解析などのその他の検証を実行するプロセス（通常はCIサーバー）をトリガーする。 (全てのcommitが、みたいな??:thinking:) (これがpipelineの最初のstep...!)
This first step is optimized so that it takes only a few minutes to run.
この最初のステップは、実行に数分しかかからないように最適化されている。
If this initial commit stage fails, the problem must be fixed immediately—nobody should check in more work on a broken commit stage.
**この最初の commit stage が失敗した場合、問題は直ちに修正されなければならない**。壊れた commit stage にさらに作業をチェックインしてはいけない。(=次のstepに進めてはいけないってこと??:thinking:)
Every passing commit stage triggers the next step in the pipeline, which might consist of a more comprehensive set of automated tests.
commit stageが成功するたびに、次のステップがトリガーされ、より包括的な自動テストのセットで構成されるかもしれない。
Versions of the software that pass all the automated tests can then be deployed on demand to further stages such as exploratory testing, performance testing, staging, and production, as shown below.
すべての自動テストに合格したソフトウェアのバージョンは、探索的テスト、パフォーマンステスト、ステージング、本番などのさらなるstage (=pipelineにおけるstep) に必要に応じてデプロイできる。以下に示すように。
(探索的テストは = dev環境にデプロイして、開発者が手動でテストする、みたいな感じっぽい...?:thinking:)

![figure1]()

Deployment pipelines tie together configuration management, continuous integration and test and deployment automation in a holistic, powerful way that works to improve software quality, increase stability, and reduce the time and cost required to make incremental changes to software, whatever domain you’re operating in.
**deployment pipelineは、configuration management、continuous integration、test&deployment automation (CDの3つの基礎だ!) を統合的かつ強力な方法で結びつける**。これにより、ソフトウェアの品質を向上させ、安定性を高め、ソフトウェアへのインクリメンタルな変更に必要な時間とコストを削減する。どのドメインでも適用できる。
When building a deployment pipeline, we’ve found the following practices valuable:
デプロイメント・パイプラインを構築する際、私たちは以下のプラクティスが有用であることを発見した:

- **Only build packages once**.
  packageのビルドは一度だけ。
  We want to be sure the thing we’re deploying is the same thing we’ve tested throughout the deployment pipeline, so if a deployment fails we can eliminate the packages as the source of the failure.
  デプロイメントパイプライン全体でテストしたものと同じものをデプロイすることを保証したいので、**デプロイメントが失敗した場合、パッケージを失敗の原因として削除できるようにします**。

- **Deploy the same way to every environment—including development**.
  **開発を含むすべての環境に同じ方法でデプロイする**。
  This way, we test the deployment process many, many times before it gets to production, and again, we can eliminate it as the source of any problems.
  こうすることで、本番環境に到達する前にデプロイメントプロセスを何度もテストし、問題の原因として排除できる。

- **Smoke test your deployments**.
  デプロイメントをスモークテストする。
  (smoke test = **基本的な機能が正常に動作するかを簡単なテストケースで確認すること**。いくつかのテストケースをE2Eテストするみたいな??:thinking:)
  Have a script that validates all your application’s dependencies are available, at the location you have configured your application.
  アプリケーションを構成した場所に、すべてのアプリケーションの依存関係が利用可能であることを検証するスクリプトを用意してください。
  Make sure your application is running and available as part of the deployment process.
  **デプロイメントプロセスの一部として、アプリケーションが実行され、利用可能であることを確認してください**。

- **Keep your environments similar**.
  環境を似たように保つ。
  Although they may differ in hardware configuration, they should have the same version of the operating system and middleware packages, and they should be configured in the same way.
  ハードウェア構成は違っても、オペレーティングシステムとミドルウェアパッケージのバージョンが同じであり、同じ方法で構成されているべきです。
  This has become much easier to achieve with modern virtualization and container technology.
  これは、最新の仮想化とコンテナ技術によって、はるかに簡単に実現できるようになった。
  (ローカル環境とdev環境と本番環境を似たように保つ、みたいな話??:thinking:)

With the advent of infrastructure as code, it has became possible to use deployment pipelines to create a fully automated process for taking all kinds of changes—including database and infrastructure changes—from version control into production in a controlled, repeatable and auditable way.
**infrastructure as codeの登場により、デプロイメントパイプラインを使用して、バージョン管理から本番環境にデータベースやインフラの変更を含むあらゆる変更を、制御された、繰り返し可能な、監査可能な方法で完全に自動化するプロセスを作成することが可能になりました**。(インフラもコードで定義・管理できるようになった -> インフラもバージョン管理できるようになった -> インフラやDBの修正もdeployment pipelineで自動デプロイできるようになった、みたいな??:thinking:)
This pattern has also been successfully applied in the context of user-installed software (including apps), firmware, and mainframes.
このパターンは、ユーザがインストールしたソフトウェア（アプリを含む）、ファームウェア、メインフレームのコンテキストでも成功裏に適用されています。
In The Practice of Cloud System Administration the resulting system is known as a software delivery platform.
クラウド・システム・アドミニストレーションの実践』では、このようなシステムはソフトウェアデリバリープラットフォームとして知られています。

Deployment pipelines are described at length in Chapter 5 of the Continuous Delivery book, which is available for free.
デプロイメント・パイプラインについては、無料で入手できる「継続的デリバリー」の第5章で詳しく説明されている。
I introduce them on this site in the context of continuous testing.
このサイトでは、継続的テストの文脈で紹介している。

## Patterns for Low-Risk Releases 低リスクリリースのためのパターン

In the context of web-based systems there are a number of patterns that can be applied to further reduce the risk of deployments.
ウェブベースのシステムに関しては、**デプロイメントのリスクをさらに低減するために適用できるパターン**がいくつかあります。
Michael Nygard also describes a number of important software design patterns which are instrumental in creating resilient large-scale systems in his book Release It!
マイケル・ナイガード（Michael Nygard）もまた、著書『Release It』の中で、弾力性のある大規模システムの構築に役立つ重要なソフトウェア・デザイン・パターンを数多く紹介している！

The four key principles that enable low-risk releases (along with many of the following patterns) are described in my article Four Principles of Low-Risk Software Releases.
**低リスクのリリースを可能にする4つの重要な原則**（以下の多くのパターンとともに）は、私の記事「低リスクのソフトウェア・リリースの4つの原則」に記載されています。
These principles are:
これらの原則とは

- Low-risk Releases are Incremental.
  **低リスクのリリースはインクリメンタルである**。(漸近的??)
  Our goal is to architect our systems such that we can release individual changes (including database changes) independently, rather than having to orchestrate big-bang releases due to tight coupling between multiple different systems.
  私たちの目標は、複数の異なるシステム間の緊密な結合のために大規模なリリースのオーケストレーションが必要になるのではなく、**個々の変更（データベースの変更を含む）を独立してリリースできるようにシステムを構築する**ことです。
  This typically requires building versioned APIs and implementing patterns such as circuit breaker.
  そのためには通常、バージョン管理されたAPIを構築し、サーキット・ブレーカーのようなパターンを実装する必要がある。

- Decouple Deployment and Release.
  **デプロイメントとリリースを切り離す**。(システムの新しいversionを展開する作業と、実際にユーザに公開する作業を別々に扱う、ってことっぽい!:thinking:)
  Releasing new versions of your system shouldn’t require downtime.
  システムの新バージョンをリリースするのに、ダウンタイムは必要ないはずだ。
  In the 2005 project that began my continuous delivery journey, we used a pattern called blue-green deployment to enable sub-second downtime and rollback, even though it took tens of minutes to perform the deployment.
  私の継続的デリバリーの旅を始めた2005年のプロジェクトでは、デプロイメントに数十分かかったにもかかわらず、サブセカンドのダウンタイムとロールバックを可能にするために、**blue-green deploymentというパターンを使用しました**。(ブルーグリーンデプロイメントも、デプロイとリリースを分離するアプローチの一つ...!:thinking:)
  Our ultimate goal is to separate the technical decision to deploy from the business decision to launch a feature, so we can deploy continuously but release new features on demand.
  私たちの最終的な目標は、デプロイするための技術的な決定をビジネス的な機能のローンチから分離し、継続的にデプロイできるようにすることであり、新機能を必要に応じてリリースすることです。
  Two commonly-used patterns that enable this goal are dark launching and feature toggles.
  **この目標を可能にする2つのよく使われるパターンは、dark launchingとfeature togglesです**。

- (メモ)デプロイとリリースを分離するアプローチ達:

  - 1. blue-green deployment:
    - 2つの環境を用意する。**古いversionを青環境で稼働してる間に、新しいversionを緑環境に展開する**。緑環境でテストや準備が完了したあとにtrafficを緑環境に切り替える。
    - 問題が発生した場合はすぐに切り戻す事ができる。この方法により、ユーザにほぼ中断なくサービスが提供される。
  - 2. Dark Launching:
    - hoge
  - 3. Feature Toggles:
    - 特定の機能を有効or無効にするためのフラグを追加する方法。
    - 新機能は展開済みでも、ユーザにはまだ公開されていない状態にすることができる。feature togglesフラグで、適切なタイミングで新機能を公開することができる。

- Focus on Reducing Batch Size.
  **バッチサイズの縮小に焦点を当てる**。
  Counterintuitively, deploying to production more frequently actually reduces the risk of release when done properly, simply because the amount of change in each deployment is smaller.
  直感に反して、**適切に行うことができれば、本番環境への頻繁なデプロイメントは、実際にはリリースのリスクを低減します**。なぜなら、**各デプロイメントの変更量が小さくなるから**です。
  When each deployment consists of tens of lines of code or a few configuration settings, it becomes much easier to perform root cause analysis and restore service in the case of an incident.
  各デプロイメントが数行のコードや数個の設定で構成されている場合、インシデントが発生した場合にルート原因分析を行い、**サービスを復旧することがはるかに容易になります**。(うんうん、原因調査がしやすい...!:thinking:)
  Furthermore, because we practice the deployment process so frequently, we’re forced to simplify and automate it which further reduces risk.
  さらに、私たちはデプロイメントプロセスを頻繁に練習するため、リスクがさらに低減されるように簡素化し、自動化することが求められます。

- Optimize for Resilience.
  **回復力を最適化する**。
  Once we accept that failures are inevitable, we should start to move away from the idea of investing all our effort in preventing problems, and think instead about how to restore service as rapidly as possible when something goes wrong.
  一度、失敗は避けられないと受け入れると、問題を防ぐためにすべての努力を投資するという考え方から離れ、**何かがうまくいかないときにできるだけ迅速にサービスを復旧する方法について考える**べきです。
  Furthermore, when an accident occurs, we should treat it as a learning opportunity.
  さらに、事故が発生した場合、それを学習の機会として扱うべきです。
  The patterns described on this page are known to work at scale in all kinds of environments, and demonstrably increase throughput while at the same time increasing stability in production.
  このページで説明するパターンは、**あらゆる環境でスケールすることができ、生産性を向上させると同時に、本番環境での安定性を高めることができることが証明されています**。
  However resilience isn’t just a feature of our systems, it’s a characteristic of our culture.
  **しかし、resilience(=回復力)は、私たちのシステムの特徴だけでなく、私たちの文化の特徴でもあります**。
  High performance organizations are constantly working to improve the resilience of their systems by trying to break them and implementing the lessons learned in the course of doing so.
  高業績組織は、システムの回復力を向上させるために、システムを壊そうとしているところです。そして、その過程で学んだ教訓を実装しています。
  (=カオスエンジニアリングとか、システムを壊して学ぶ、みたいな話??:thinking:)

<!-- ここまで読んだ! -->
