## refs: refs：

- CDの公式っぽい資料 [Patterns](https://continuousdelivery.com/implementing/patterns/) CDの公式っぽい資料 [パターン](https://continuousdelivery.com/implementing/patterns/)

# Patterns パターン

Linda Rising defines a pattern as “a named strategy for solving a recurring problem”.
リンダ・ライジングは、パターンを「繰り返し起こる問題を解決するための、名前のついた戦略」と定義している。
The concept of patterns comes from the work of architect Christopher Alexander, who observes “Each pattern describes a problem that occurs over and over again in our environment and then describes the core of the solution to that problem in such a way that you can use this solution a million times over without ever doing it the same way twice.”
パターンの概念は、建築家クリストファー・アレクサンダーの研究に由来している。彼は、「各パターンは、私たちの環境で何度も繰り返し発生する問題を記述し、その問題に対する解決策の中核を記述する。

## The Deployment Pipeline デプロイメント・パイプライン

The key pattern introduced in continuous delivery is the deployment pipeline.
継続的デリバリーに導入された重要なパターンは、デプロイメント・パイプラインである。
This pattern emerged from several ThoughtWorks projects where we were struggling with complex, fragile, painful manual processes for preparing testing and production environments and deploying builds to them.
このパターンは、テスト環境と本番環境を準備し、ビルドをそれらにデプロイするための、複雑で壊れやすく、骨の折れる手作業プロセスに苦労していたThoughtWorksのいくつかのプロジェクトから生まれた。
We’d already worked to automate a significant amount of the regression and acceptance testing, but it was taking weeks to get builds to integrated environments for full regression testing, and our first deployment to production took an entire weekend.
すでにかなりの量の回帰テストと受け入れテストの自動化に取り組んでいたが、完全な回帰テストのために統合環境へビルドするのに数週間かかり、本番環境への最初のデプロイには週末を丸々使ってしまった。

We wanted to industrialize the process of taking changes from version control to production.
私たちは、バージョン管理から本番への変更プロセスを工業化したかったのです。
Our goal was to make deployment to any environment a fully automated, scripted process that could be performed on demand in minutes (on the original project we got it down to less than an hour, which was a big deal for an enterprise system in 2005).
私たちの目標は、あらゆる環境へのデプロイを完全に自動化し、スクリプト化されたプロセスで、オンデマンドで数分以内に実行できるようにすることだった（当初のプロジェクトでは、1時間以内に完了させたが、これは2005年当時のエンタープライズ・システムとしては大変なことだった）。
We wanted to be able to configure testing and production environments purely from configuration files stored in version control.
私たちは、バージョン管理に保存されている設定ファイルだけで、テスト環境と本番環境を設定できるようにしたいと考えていました。
The apparatus we used to perform these tasks (usually in the form of a bunch of scripts in bash or ruby) became known as deployment pipelines, which Dan North, Chris Read and I wrote up in a paper presented at the Agile 2006 conference.
これらのタスクを実行するために使った装置（通常はbashやrubyのスクリプトの束の形）は、デプロイメント・パイプラインとして知られるようになり、ダン・ノース、クリス・リード、そして私は、アジャイル2006カンファレンスで発表した論文に書いた。

In the deployment pipeline pattern, every change in version control triggers a process (usually in a CI server) which creates deployable packages and runs automated unit tests and other validations such as static code analysis.
デプロイメント・パイプライン・パターンでは、バージョン管理におけるすべての変更が、デプロイ可能なパッケージを作成し、自動ユニットテストや静的コード解析などのその他の検証を実行するプロセス（通常はCIサーバー）をトリガーする。
This first step is optimized so that it takes only a few minutes to run.
この最初のステップは、実行に数分しかかからないように最適化されている。
If this initial commit stage fails, the problem must be fixed immediately—nobody should check in more work on a broken commit stage.
この最初のコミット段階で失敗した場合、問題は直ちに修正されなければならない。
Every passing commit stage triggers the next step in the pipeline, which might consist of a more comprehensive set of automated tests.
コミット段階を通過するたびに、パイプラインの次の段階がトリガーされ、より包括的な自動テストのセットで構成されるかもしれない。
Versions of the software that pass all the automated tests can then be deployed on demand to further stages such as exploratory testing, performance testing, staging, and production, as shown below.
すべての自動テストに合格したソフトウェアのバージョンは、次に示すように、探索的テスト、パフォーマンステスト、ステージング、本番といったさらなる段階にオンデマンドでデプロイすることができる。

Deployment pipelines tie together configuration management, continuous integration and test and deployment automation in a holistic, powerful way that works to improve software quality, increase stability, and reduce the time and cost required to make incremental changes to software, whatever domain you’re operating in.
デプロイメント・パイプラインは、構成管理、継続的インテグレーション、テストとデプロイの自動化を総合的かつ強力な方法で結びつけ、ソフトウェアの品質を向上させ、安定性を高め、どのようなドメインで運用されている場合でも、ソフトウェアに段階的な変更を加えるために必要な時間とコストを削減します。
When building a deployment pipeline, we’ve found the following practices valuable:
デプロイメント・パイプラインを構築する際、私たちは以下のプラクティスが有用であることを発見した：

Only build packages once.
パッケージのビルドは一度だけ。
We want to be sure the thing we’re deploying is the same thing we’ve tested throughout the deployment pipeline, so if a deployment fails we can eliminate the packages as the source of the failure.
デプロイするものが、デプロイパイプライン全体を通してテストしたものと同じであることを確認したい。そうすれば、デプロイが失敗した場合、失敗の原因としてパッケージを除外することができる。

Deploy the same way to every environment—including development.
開発を含むすべての環境に同じ方法でデプロイする。
This way, we test the deployment process many, many times before it gets to production, and again, we can eliminate it as the source of any problems.
こうすることで、デプロイメント・プロセスを本番稼動前に何度も何度もテストし、問題の原因として排除することができる。

Smoke test your deployments.
デプロイメントをスモークテストする。
Have a script that validates all your application’s dependencies are available, at the location you have configured your application.
アプリケーションを設定した場所で、アプリケーションの依存関係がすべて利用可能かどうかを検証するスクリプトを用意しましょう。
Make sure your application is running and available as part of the deployment process.
デプロイメントプロセスの一環として、アプリケーションが実行され、利用可能であることを確認してください。

Keep your environments similar.
環境を似せておく。
Although they may differ in hardware configuration, they should have the same version of the operating system and middleware packages, and they should be configured in the same way.
ハードウェア構成は違っても、オペレーティング・システムとミドルウェア・パッケージのバージョンは同じで、同じように設定されているはずだ。
This has become much easier to achieve with modern virtualization and container technology.
これは、最新の仮想化とコンテナ技術によって、はるかに簡単に実現できるようになった。

With the advent of infrastructure as code, it has became possible to use deployment pipelines to create a fully automated process for taking all kinds of changes—including database and infrastructure changes—from version control into production in a controlled, repeatable and auditable way.
インフラストラクチャー・アズ・コードの出現により、デプロイメント・パイプラインを使用して、データベースやインフラストラクチャーの変更を含むあらゆる種類の変更を、管理され、反復可能で、監査可能な方法で、バージョン管理から本番環境に取り込むための完全に自動化されたプロセスを作成することが可能になった。
This pattern has also been successfully applied in the context of user-installed software (including apps), firmware, and mainframes.
このパターンは、ユーザー・インストール・ソフトウェア（アプリを含む）、ファームウェア、メインフレームの文脈でもうまく適用されている。
In The Practice of Cloud System Administration the resulting system is known as a software delivery platform.
クラウド・システム・アドミニストレーションの実践』では、その結果生まれたシステムはソフトウェア・デリバリー・プラットフォームとして知られている。

Deployment pipelines are described at length in Chapter 5 of the Continuous Delivery book, which is available for free.
デプロイメント・パイプラインについては、無料で入手できる「継続的デリバリー」の第5章で詳しく説明されている。
I introduce them on this site in the context of continuous testing.
このサイトでは、継続的テストの文脈で紹介している。

## Patterns for Low-Risk Releases 低リスクリリースのためのパターン

In the context of web-based systems there are a number of patterns that can be applied to further reduce the risk of deployments.
ウェブベースのシステムに関しては、配備のリスクをさらに減らすために適用できるパターンがいくつかある。
Michael Nygard also describes a number of important software design patterns which are instrumental in creating resilient large-scale systems in his book Release It!
マイケル・ナイガード（Michael Nygard）もまた、著書『Release It』の中で、弾力性のある大規模システムの構築に役立つ重要なソフトウェア・デザイン・パターンを数多く紹介している！

The four key principles that enable low-risk releases (along with many of the following patterns) are described in my article Four Principles of Low-Risk Software Releases.
低リスクのリリースを可能にする4つの重要な原則（以下の多くのパターンとともに）は、私の記事「低リスクのソフトウェア・リリースの4つの原則」に記載されています。
These principles are:
これらの原則とは

Low-risk Releases are Incremental.
低リスクのリリースはインクリメンタルである。
Our goal is to architect our systems such that we can release individual changes (including database changes) independently, rather than having to orchestrate big-bang releases due to tight coupling between multiple different systems.
私たちの目標は、複数の異なるシステム間の緊密な結合のために大規模なリリースのオーケストレーションが必要になるのではなく、個々の変更（データベースの変更を含む）を独立してリリースできるようにシステムを構築することです。
This typically requires building versioned APIs and implementing patterns such as circuit breaker.
そのためには通常、バージョン管理されたAPIを構築し、サーキット・ブレーカーのようなパターンを実装する必要がある。

Decouple Deployment and Release.
デプロイメントとリリースを切り離す。
Releasing new versions of your system shouldn’t require downtime.
システムの新バージョンをリリースするのに、ダウンタイムは必要ないはずだ。
In the 2005 project that began my continuous delivery journey, we used a pattern called blue-green deployment to enable sub-second downtime and rollback, even though it took tens of minutes to perform the deployment.
私の継続的デリバリーの旅の始まりとなった2005年のプロジェクトでは、ブルーグリーンデプロイメントと呼ばれるパターンを使い、デプロイメント実行に数十分かかっても、秒以下のダウンタイムとロールバックを可能にした。
Our ultimate goal is to separate the technical decision to deploy from the business decision to launch a feature, so we can deploy continuously but release new features on demand.
私たちの最終的な目標は、デプロイする技術的な決定と、機能を立ち上げるビジネス上の決定を分離することです。
Two commonly-used patterns that enable this goal are dark launching and feature toggles.
この目標を可能にする2つのよく使われるパターンは、ダークランチングとフィーチャートグルである。

Focus on Reducing Batch Size.
バッチサイズの縮小に焦点を当てる。
Counterintuitively, deploying to production more frequently actually reduces the risk of release when done properly, simply because the amount of change in each deployment is smaller.
直感に反するかもしれないが、本番環境へのデプロイをより頻繁に行うことは、適切に行われた場合、リリースのリスクを実際に低減する。
When each deployment consists of tens of lines of code or a few configuration settings, it becomes much easier to perform root cause analysis and restore service in the case of an incident.
各配備が数十行のコードまたは数個のコンフィギュレーション設定で構成されている場合、根本原因の分析やインシデント発生時のサービス復旧が非常に容易になる。
Furthermore, because we practice the deployment process so frequently, we’re forced to simplify and automate it which further reduces risk.
さらに、私たちはデプロイメント・プロセスを頻繁に実践しているため、デプロイメント・プロセスを単純化し、自動化せざるを得ない。

Optimize for Resilience.
レジリエンスの最適化。
Once we accept that failures are inevitable, we should start to move away from the idea of investing all our effort in preventing problems, and think instead about how to restore service as rapidly as possible when something goes wrong.
故障は避けられないものであることを受け入れれば、問題を防ぐことに全力を注ぐという考えから脱却し、その代わりに、何か問題が起きたときにいかに迅速にサービスを復旧させるかを考えるようになるはずだ。
Furthermore, when an accident occurs, we should treat it as a learning opportunity.
さらに、事故が起きたら、それを学習の機会として扱うべきだ。
The patterns described on this page are known to work at scale in all kinds of environments, and demonstrably increase throughput while at the same time increasing stability in production.
このページで説明するパターンは、あらゆる環境でスケールアップして機能することが知られており、本番での安定性を高めると同時にスループットを向上させることが実証されている。
However resilience isn’t just a feature of our systems, it’s a characteristic of our culture.
しかし、レジリエンスは単に私たちのシステムの特徴ではなく、私たちの文化の特徴でもある。
High performance organizations are constantly working to improve the resilience of their systems by trying to break them and implementing the lessons learned in the course of doing so.
高業績組織は、システムの破壊を試み、その過程で学んだ教訓を実行に移すことによって、シス テムの回復力を向上させようと絶えず努力している。
