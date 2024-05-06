## refs: refs：

- https://continuousdelivery.com/foundations/ https://continuousdelivery.com/foundations/

# Foundations ファウンデーション

Continuous delivery rests on three foundations: comprehensive configuration management, continuous integration, and continuous testing.
**継続的デリバリーは、3つの基盤の上に成り立っている**: すなわち、包括的な設定管理、継続的インテグレーション、継続的テストである。

In this section, you can read an overview of each of these foundations.
このセクションでは、それぞれの財団の概要をお読みいただけます。
You’ll also discover how to find out more about each of them, and find answers to some frequently-asked questions.
また、それぞれの詳細を調べる方法や、よくある質問に対する回答もご覧いただけます。

# Configuration Management コンフィギュレーション管理

refs: https://continuousdelivery.com/foundations/configuration-management/
を参照してください： https://continuousdelivery.com/foundations/configuration-management/

Automation plays a vital role in ensuring we can release software repeatably and reliably.
自動化は、ソフトウェアを繰り返し、信頼性を持ってリリースできることを保証する上で重要な役割を果たしている。
One key goal is to take repetitive manual processes like build, deployment, regression testing and infrastructure provisioning, and automate them.
**重要な目標のひとつは、ビルド、デプロイ、リグレッション・テスト、インフラ・プロビジョニングのような繰り返しの多い手作業プロセスを自動化すること**だ。
In order to achieve this, we need to version control everything required to perform these processes, including source code, test and deployment scripts, infrastructure and application configuration information, and the many libraries and packages we depend upon.
**これを実現するためには、これらのプロセスを実行するために必要なすべてのものをバージョン管理する必要がある**。(version管理の重要さってこれか...!:thinking:) これには、ソースコード、テストおよびデプロイメントスクリプト、インフラストラクチャおよびアプリケーションのコンフィギュレーション情報、および依存する多くのライブラリやパッケージが含まれる。
We also want to make it straightforward to query the current—and historical—state of our environments.
また、環境の現在と過去の状態を簡単に照会できるようにしたい。(これこそversion管理だよね...!)

We have two overriding goals:
私たちには**2つの最優先目標**がある：

- 1. **Reproducibility**: We should be able to provision any environment in a fully automated fashion, and know that any new environment reproduced from the same configuration is identical.
     **再現性**： 完全に自動化された方法でどのような環境でもプロビジョニングでき、同じコンフィギュレーションから再現される新しい環境はすべて同じであることがわかるべきである。
- 2. **Traceability**: We should be able to pick any environment and be able to determine quickly and precisely the versions of every dependency used to create that environment.
     **追跡性**： どの環境でも選択し、その環境を作成するために使用されたすべての依存関係のバージョンを迅速かつ正確に特定できるようにする必要がある。
     We also want to to be able to compare previous versions of an environment and see what has changed between them.
     また、ある環境の過去のバージョンを比較し、その間に何が変わったかを確認できるようにしたい。

These capabilities give us several very important benefits:
これらの能力(再現性、追跡性)は、私たちにいくつかの非常に重要な利点を与えてくれる：

- 1. **Disaster recovery**: When something goes wrong with one of our environments, for example a hardware failure or a security breach, we need to be able to reproduce that environment in a deterministic amount of time in order to be able to restore service.
     **災害復旧**： 例えばハードウェアの故障やセキュリティ侵害など、私たちの環境のひとつに何か問題が発生した場合、サービスを復旧させるためには、決定論的な時間内にその環境を再現できる必要があります。
- 2. **Auditability**: In order to demonstrate the integrity of the delivery process, we need to be able to show the path backwards from every deployment to the elements it came from, including their version.
     **監査可能性**： デリバリー・プロセスの完全性を証明するためには、すべてのデプロイメントから、そのエレメントのバージョンも含めて、デプロイメントの出所までの経路を示すことができる必要がある。
     Comprehensive configuration management, combined with deployment pipelines, enable this.
     包括的なコンフィギュレーション管理とデプロイメント・パイプラインの組み合わせが、これを可能にする。
- 3. **Higher quality**: The software delivery process is often subject to long delays waiting for development, testing and production environments to be prepared.
     **より高い品質**： ソフトウェアのデリバリープロセスでは、開発、テスト、本番環境の準備に時間がかかることが多い。
     When this can be done automatically from version control, we can get feedback on the impact of our changes much more rapidly, enabling us to build quality in to our software.
     これをバージョン管理から自動的に行うことができれば、変更の影響に関するフィードバックをより迅速に得ることができ、ソフトウェアに品質を組み込むことができる。
- 4. **Capacity management**: When we want to add more capacity to our environments, the ability to create new reproductions of existing servers is essential.
     **容量管理**： 環境に容量を追加したい場合、既存のサーバの複製を新たに作成する機能が不可欠だ。(スケーラビリティ的な??)
     This capability enables the horizontal scaling of modern cloud-based distributed systems.
     この機能により、最新のクラウドベースの分散システムの水平スケーリングが可能になる。
- 5. **Response to defects**: When we discover a critical defect, or a vulnerability in some component of our system, we want to get a new version of our software released as quickly as possible.
     **欠陥への対応**： システムのコンポーネントに重大な欠陥や脆弱性が発見された場合、私たちはできるだけ早くソフトウェアの新バージョンをリリースしたいと考えています。
     Many organizations have an emergency process for this type of change which goes faster by bypassing some of the testing and auditing.
     多くの組織では、この種の変更のための緊急プロセスを持っており、テストや監査の一部をバイパスすることで、より迅速に行っている。(特殊なリリース手続きになるってこと??)
     This presents an especially serious dilemma in safety-critical systems.
     これは、特にセーフティ・クリティカルなシステムにおいて深刻なジレンマをもたらす。
     Our goal should be to be able to use our normal release process for emergency fixes—which is precisely what continuous delivery enables, on the basis of comprehensive configuration management.
     私たちのゴールは、**緊急修正に通常のリリースプロセスを使用できるようにすることであるべき**だ。**それこそが、包括的なコンフィギュレーション管理に基づいて継続的デリバリーを可能にするもの**である。(なるほど...??:thinking:)

As environments become more complex and heterogeneous, it becomes progressively harder to achieve these goals.
環境がより複雑で異質なものになればなるほど、こうした目標を達成するのは徐々に難しくなる。
Achieving perfect reproducibility and traceability to the last byte for a complex enterprise system is impossible (apart from anything else, every real system has state).
複雑な企業システムにおいて、完璧な再現性と追跡性を最後のバイトまで達成することは不可能である（それ以外にも、すべての実際のシステムには状態がある）。(version管理できない状態がどうしても存在するってことかな...!:thinking:)
Thus a key part of configuration management is working to simplify our architecture, environments and processes to reduce the investment required to achieve the desired benefits.
したがって、コンフィギュレーション管理の重要な部分は、望ましい利益を得るために必要な投資を削減するために、**アーキテクチャ、環境、プロセスを単純化することに取り組むこと**である。

When working to achieve the benefits, we should always start by defining in measurable terms the goals we want to achieve.
**利益を達成するために努力する場合、私たちは常に、達成したい目標を測定可能な言葉で定義することから始めるべき**である。(なるほど、これはgoal setting的にも大事だよなぁ...!:thinking:)
This allows us to determine which of the possible paths to reach our goal are likely to be the best, and to change direction or reassess our goals if we discover our approach is going to be too expensive or take too long.
これによって、目標に到達するための可能な経路のうち、最も良いものが何であるかを判断し、アプローチが高すぎるか時間がかかりすぎることがわかった場合には、方向を変えたり、目標を再評価したりすることができる。

## Resources リソース (参考資料)

My talk on lean configuration management
リーン構成管理に関する私の講演

Kief Morris’ entry on ImmutableServer in Martin Fowler’s bliki is a good place to start, along with Kief’s forthcoming book.
Kief MorrisのMartin FowlerのblikiのImmutableServerに関するエントリーは、Kiefの近刊の本とともに、手始めとして良い場所だ。

Tom Limoncelli et al’s encyclopedic book The Practice of Cloud System Administration: Designing and Operating Large Distributed Systems, Volume 2
トム・リモンチェリらの百科事典的書籍『クラウド・システム管理の実践』： 大規模分散システムの設計と運用 第2巻

Pedro Canahuati on scaling operations at Facebook.
ペドロ・カナワティ、フェイスブックでの事業拡大について語る。

## FAQ FAQ

### What tools should I use? どのようなツールを使えばよいですか？

Tool choice is a complex topic, and in many cases (unless you use something wholly unsuitable) tool choice is not the critical factor in success.
道具の選択は複雑なテーマであり、**多くの場合（まったく適さないものを使わない限り）道具の選択は成功の決定的な要因ではない**。(うんうん...!:thinking:)
I recommend doing some research to whittle down a shortlist based on what technologies your team is familiar with, what has the widest level of usage, and what is under active development and support, and then setting a short-term goal and trying to achieve it using each of the tools on your shortlist.

**チームが慣れている技術、最も広く使用されているもの**に基づいて、ショートリストを絞り込むためのいくつかの調査を行うことをお勧めします。(うんうん...!:thinking:)
**そして、アクティブな開発とサポートを受けているもの**を選択し、その後、ショートリストにある各ツールを使用して短期目標を設定し、それを達成しようとすることです。

### How do containers / the cloud / virtualization technologies affect this topic? コンテナ/クラウド/仮想化技術は、このトピックにどのように影響しますか？

The most important thing is that every new advance makes it easier and cheaper to achieve the benefits described.
最も重要なことは、新たな進歩があるたびに、説明したような利益をより簡単に、より安く達成できるようになるということだ。
However in themselves, technologies such as containerization are not a silver bullet.
**しかし、コンテナ化などの技術は、それ自体が特効薬というわけではない**。(それ自体が特効薬、ってケースはほぼなさそう:thinking:)
For example, it’s not uncommon to see developers create “snowflake” containers whose contents are hard to audit or reproduce.
例えば、開発者が「スノーフレーク」コンテナを作成し、その中身を監査したり再現したりするのが難しいというケースは珍しくない。
We still need to apply the discipline of comprehensive use of version control and the deployment pipeline in order to achieve our goals.
**目標を達成するためには、引き続きバージョン管理とデプロイメント・パイプラインの包括的な使用の原則を適用する必要がある**。(うんうん...!:thinking:)

<!-- ここまで読んだ! -->

# Continuous Integration 継続的インテグレーション

refs: https://continuousdelivery.com/foundations/continuous-integration/

Combining the work of multiple developers is hard.
**複数の開発者の仕事を組み合わせるのは難しい**。
Software systems are complex, and an apparently simple, self-contained change to a single file can easily have unintended consequences which compromise the correctness of the system.
ソフトウェア・システムは複雑であり、一見単純で自己完結的な単一ファイルへの変更でも、簡単に意図しない結果をもたらし、システムの正確性を損なうことがある。
As a result, some teams have developers work isolated from each other on their own branches, both to keep trunk / master stable, and to prevent them treading on each other’s toes.
その結果、チームによっては、trunk / masterを安定させるために、開発者が互いに孤立して自分のブランチで作業することがある。また、お互いの足を踏まないようにするためでもある。

However, over time these branches diverge from each other.
しかし、時間の経過とともに、これらの枝は互いに分岐していく。
While merging a single one of these branches into mainline is not usually troublesome, the work required to integrate multiple long-lived branches into mainline is usually painful, requiring significant amounts of re-work as conflicting assumptions of developers are revealed and must be resolved.
これらのブランチのうちの1つをメインラインにマージすることは通常問題にならないが、**複数の長期ブランチをメインラインに統合するために必要な作業は通常苦痛であり**、開発者の相反する前提が明らかになり、解決されなければならないため、**大量の再作業が必要になる**。
(Continuous Integrationは、長期ブランチをなるべく使わないように、継続的に統合していきましょう、みたいな戦略のこと??:thinking:)

Teams using long-lived branches often require code freezes, or even integration and stabilization phases, as they work to integrate these branches prior to a release.
長期ブランチを使用しているチームは、リリース前にこれらのブランチを統合するために、コードフリーズ、あるいは統合と安定化のフェーズが必要になることがよくあります。
Despite modern tooling, this process is still expensive and unpredictable.
近代的な ツールを使っても、このプロセスはまだ高価で予測不可能である。
On teams larger than a few developers, the integration of multiple branches requires multiple rounds of regression testing and bug fixing to validate that the system will work as expected following these merges.
数人以上の開発者がいるチームでは、複数のブランチを統合するために、リグレッションテストとバグフィックスを何度も繰り返し、マージ後にシステムが期待通りに動くかどうかを検証する必要がある。
This problem becomes exponentially more severe as team sizes grow, and as branches become more long-lived.
**この問題は、チームの規模が大きくなるにつれて、またブランチの寿命が長くなるにつれて、指数関数的に深刻になっていく**。

The practice of continuous integration was invented to address these problems.
継続的インテグレーションのプラクティスは、こうした問題に対処するために考案された。(こうした問題 = 長期ブランチによる統合が難しい問題?)
CI (continuous integration) follows the XP (extreme programming) principle that if something is painful, we should do it more often, and bring the pain forward.
**CI（継続的インテグレーション）は、XP（エクストリーム・プログラミング）の原則に従っている**。つまり、**「何かが痛いときは、より頻繁に行い、痛みを前に出すべきだ」という原則**だ。
Thus in CI developers integrate all their work into trunk (also known as mainline or master) on a regular basis (at least daily).
このように**CIでは、開発者は定期的に（少なくとも毎日）すべての作業をトランク（メインラインまたはマスターとも呼ばれる）に統合する**。(ええ！？CI難しそう...!:thinking:)
A set of automated tests is run both before and after the merge to validate that no regressions are introduced.
自動テストのセットは、リグレッションが発生しないことを検証するために、マージ前とマージ後の両方で実行される。
If these automated tests fail, the team stops what they are doing and someone fixes the problem immediately.
これらの自動テストが失敗した場合、チームは自分たちの作業を中断し、誰かが直ちに問題を修正する。

Thus we ensure that the software is always in a working state, and that developer branches do not diverge significantly from trunk.
こうして、ソフトウェアが常に稼働状態にあること、開発者ブランチがtrunkから大きく分岐しないことを確認する。(trunk = 主要な開発ラインや基盤となるブランチを指す)
The benefits of continuous integration are very significant—research shows that it leads to higher levels of throughput, more stable systems, and higher quality software.
継続的インテグレーションの利点は非常に大きく、スループットの向上、システムの安定性、ソフトウェアの品質の向上につながることが研究によって示されている。
However the practice is still controversial, for two main reasons.
**しかし、この慣行は、主に2つの理由から、いまだに議論の的となっている**。

First, it requires developers to break up large features and other changes into smaller, more incremental steps that can be integrated into trunk / master.
**第一に、 開発者に、大きな機能やその他の変更を、トランク／マスターに統合できるより小さな、よりインクリメンタルなステップに分割する**ことを求める。
This is a paradigm shift for developers who are not used to working in this way.
このようなやり方に慣れていない開発者にとってはパラダイムシフトだ。
It also takes longer to get large features completed.
また、大きな機能を完成させるのにも時間がかかる。
However in general we don’t want to optimize for the speed at which developers can declare their work “dev complete” on a branch.
しかし一般的には、開発者が自分の作業をブランチで「開発完了」と宣言できる速度を最適化したいわけではない。
Rather, we want to be able to get changes reviewed, integrated, tested and deployed as fast as possible—and this process is an order of magnitude faster and cheaper when the changes are small and self-contained, and the branches they live on are short-lived.
**むしろ、変更をレビューし、統合し、テストし、デプロイすることができる速度をできるだけ速くしたい**のであり、これは、変更が小さく自己完結しており、それが存在するブランチが短命である場合、1桁速く、安価になる。
Working in small batches also ensures developers get regular feedback on the impact of their work on the system as a whole—from other developers, testers, customers, and automated performance and security tests—which in turn makes any problems easier to detect, triage, and fix.
**小ロットで作業すること**は、開発者が他の開発者、テスター、顧客、自動パフォーマンスおよびセキュリティテストからシステム全体に与える影響について定期的なフィードバックを受けることを保証し、その結果、問題を検出、トリアージ、修正することが容易になる。
(CIって、タスクを小さく分割して、短命ブランチでincrementalに開発していけってこと??:thinking:)

Second, continuous integration requires a fast-running set of comprehensive automated unit tests.
**第二に、継続的インテグレーションには、包括的な自動ユニットテストを高速に実行する必要がある**。(CI = 自動テストじゃないけど、CIと自動テストは相互に関係してるってことかも...!:thinking:)
These tests should be comprehensive enough to give a good level of confidence that the software will work as expected, while also running in a few minutes or less.
これらのテストは、ソフトウェアが期待通りに動作するという高い信頼レベルを提供するために十分包括的であるべきであり、数分以内に実行されるべきである。
If the automated unit tests take longer to run, developers will not want to run them frequently, and they will become harder to maintain.
自動ユニットテストの実行に時間がかかると、開発者は頻繁に実行したくなくなり、メンテナンスが難しくなる。
Creating maintainable suites of automated unit tests is complex and is best done through test-driven development (TDD), in which developers write failing automated tests before they implement the code that makes the tests pass.
自動ユニットテストのメンテナンス可能なスイートを作成することは複雑であり、開発者は、テストが成功するコードを実装する前に、失敗する自動化テストを書くテスト駆動開発（TDD）を通じて最もよく行われる。
TDD has several benefits, the most important of which is that it ensures developers write code that is modular and easy to test, reducing the maintenance cost of the resulting automated test suites.
TDDにはいくつかの利点があるが、最も重要なのは、開発者がモジュール化され、テストしやすいコードを書くことを保証し、**その結果の自動化テストスイートのメンテナンスコストを削減することである**。(TDDによって、自動テストの包括さを推進することができるのか...!:thinking:)
But TDD is still not sufficiently widely practiced.
しかし、TDDはまだ十分に普及していない。

Despite these barriers, helping software development teams implement continuous integration should be the number one priority for any organization wanting to start the journey to continuous delivery.
このような障壁があるにもかかわらず、継続的デリバリーの旅を始めたいと考えている組織にとって、ソフトウェア開発チームが継続的インテグレーションを実装するのを支援することは、最優先事項であるべきだ。
By creating rapid feedback loops and ensuring developers work in small batches, CI enables teams to build quality into their software, thus reducing the cost of ongoing software development, and increasing both the productivity of teams and the quality of the work they produce.
**CIは、迅速なフィードバックループを作成し、開発者が小ロットで作業することを保証することにより**、チームがソフトウェアに品質を組み込むことを可能にし、これにより、継続的なソフトウェア開発のコストを削減し、チームの生産性と彼らが生み出す作業の品質を向上させる。

<!-- ここまで読んだ! -->

## Resources リソース

Martin Fowler’s canonical article on Continuous Integration.
マーティン・ファウラー（Martin Fowler）の継続的インテグレーションに関する代表的な記事。

My personal favourite introduction, James Shore’s CI on a dollar a day.
個人的に好きな紹介は、ジェームス・ショアの『CI on a dollar a day』だ。

Paul Hammant has a series of detailed articles describing how Amazon, Google, Facebook and others practice trunk-based development.
ポール・ハマントは、アマゾン、グーグル、フェイスブックなどがどのようにトランク・ベースの開発を実践しているかについて、一連の詳細な記事を掲載している。

A video in which Google’s John Penix describes how Google practices CI at scale.
グーグルのジョン・ペニックスが、グーグルがどのようにCIを大規模に実践しているかを説明するビデオ。

Paul Duvall’s book on Continuous Integration.
継続的インテグレーションに関するポール・デュバルの本。

## FAQ FAQ

How do I know if my team is really doing CI?
自分のチームが本当にCIを実践しているかどうかは、どうすればわかるのか？

I have a simple test I use to determine if teams are really practicing CI.1) are all the engineers pushing their code into trunk / master (not feature branches) on a daily basis? 2) does every commit trigger a run of the unit tests? 3) When the build is broken, is it typically fixed within 10 minutes? If you can answer yes to all three questions, congratulations! You are practicing continuous integration.
チームが本当にCIを実践しているかどうかを判断するために使っている簡単なテストがある。1) すべてのエンジニアが毎日トランク／マスター（フィーチャーブランチではない）にコードをプッシュしているか？2) すべてのコミットがユニットテストの実行のトリガーになっているか？3) ビルドが壊れたとき、通常10分以内に修正されるか？3つの質問すべてに「はい」と答えられるなら、おめでとう！あなたは継続的インテグレーションを実践している。
In my experience, less than 20% of teams that think they are doing CI can actually pass the test.
私の経験では、CIをやっていると思っているチームのうち、実際にテストに合格できるのは20％以下である。
Note that it’s entirely possible to do CI without using a CI tool, and conversely, just because you’re using a CI tool does not mean you are doing CI!
CIツールを使わなくてもCIを行うことは十分に可能であるし、逆にCIツールを使っているからといってCIを行っているとは限らない！

Don’t modern tools such as Git make CI unnecessary?
Gitのような最新のツールはCIを不要にするのではないか？

No.
いや。
Distributed version control systems are an incredibly powerful tool that I fully endorse (and have been using since 2008).
分散バージョン管理システムは、私が全面的に支持する（そして2008年から使っている）信じられないほど強力なツールだ。
However like all powerful tools, they can be used in a multitude of ways, not all of them good.
しかし、あらゆる強力なツールと同様、さまざまな使い方ができる。
It’s perfectly possible to practice CI using Git, and indeed recommended for full-time teams.
Gitを使ってCIを実践することは完全に可能であり、実際フルタイムのチームには推奨されている。
The main scenario where trunk-based development is not appropriate is open-source projects, where most contributors should be working on forks of the codebase rather than on master.
トランクベースの開発が適切でない主なシナリオは、オープンソースのプロジェクトであり、そこでは、ほとんどの貢献者はマスターではなく、コードベースのフォークで作業するはずである。
There’s more discussion of CI and DVCS in a blog post I wrote on the topic.
CIとDVCSについては、私が書いたブログ記事に詳しい。

Does trunk-based development mean using feature toggles?
トランクベースの開発とは、フィーチャー・トグルを使うことですか？

No.
いや。
Feature toggles are a new-fangled term for an old pattern: configuration options.
フィーチャートグルは、古いパターンに対する新しい用語である： コンフィギュレーション・オプション。
In this context, we use them to hide from users features that are not “ready”, so we can continue to check in on trunk.
この文脈では、「準備ができていない 」機能をユーザーから隠すために使用し、トランクのチェックを続けることができる。
However feature toggles are only really necessary when practicing continuous deployment, in which we release multiple times a day.
しかし、機能トグルが本当に必要なのは、1日に何度もリリースする継続的デプロイを実践する場合だけだ。
For teams releasing every couple of weeks, or less frequently, they are unnecessary.
2、3週間に1度、あるいはそれ以下の頻度でリリースするチームには不要だ。
There are, however, two important practices to enable trunk-based development without using feature toggles.
しかし、フィーチャートグルを使わずにトランクベースの開発を可能にするには、2つの重要なプラクティスがある。
First, we should build out our APIs before we create the user interface that relies on them.
まず、APIに依存するユーザー・インターフェースを作成する前に、APIを構築すべきである。
APIs (including automated tests running against them) can be created and deployed to production “dark” (that is, without anything calling them), enabling us to work on the implementation of a story on trunk.
API（それに対して実行される自動テストを含む）を作成し、「ダーク」（つまり、それらを呼び出すものが何もない状態）でプロダクションにデプロイすることができ、トランクでストーリーの実装に取り組むことができる。
The UI (which should almost always be a thin layer over the API) is written last.
UI（ほとんどの場合、APIの上に薄いレイヤーがあるはずだ）は最後に書かれる。
Second, we should aim to break down large features into small stories (1-3 days’ work) in a way that they build upon each other iteratively, not incrementally.
第二に、大規模な機能を小さなストーリー（1～3日の作業）に分解し、漸進的ではなく反復的に積み重ねていく方法を目指すべきである。
In this way, we ensure we can continue to release increments of the feature.
こうすることで、機能のインクリメントをリリースし続けることができるのだ。
Only in the cases where an iterative approach is not possible for some reason (and this is less often than you think, given sufficient imagination) do we need to introduce feature toggles.
繰り返しのアプローチが何らかの理由で不可能な場合（十分な想像力があれば、このようなケースは案外少ないものだ）にのみ、機能トグルを導入する必要がある。

What about GitHub-style development?
GitHubスタイルの開発についてはどうだろう？

In general, I am fine with GitHub’s “flow” process—provided branches don’t live longer than a day or so.
一般的に、私はGitHubの 「flow 」プロセスに満足しています。
If you’re breaking features down into stories and practicing incremental development (see previous FAQ entry), this is not a problem.
もしあなたが機能をストーリーに分解し、インクリメンタル開発を実践しているなら（前回のFAQエントリーを参照）、これは問題ではない。
I also believe that code review should be done in process—ideally by inviting someone to pair with you (perhaps using screenhero if you’re working on a remote team) when you’re ready to check in, and reviewing the code then and there.
私はまた、コードレビューはプロセスで行うべきだと考えている。理想的には、チェックインの準備ができたときに誰かをペアに誘い（リモートチームで作業している場合は、おそらくscreenheroを使用する）、その場でコードをレビューすることだ。
Code review is best done continuously, and working in small batches enables this.
コードレビューは継続的に行うのが最善であり、小ロットで作業することでそれが可能になる。
Nobody enjoys reviewing pages and pages of diff that are the result of several day’s work because it’s impossible to reason about the impact of large changes on the system as a whole.
数日かけて作成されたdiffを何ページも何ページも見直すのは、誰にとっても楽しいことではない。

What tools should I use?
どのような道具を使うべきか？

Tool choice is a complex topic, and in many cases (unless you use something wholly unsuitable) tool choice is not the critical factor in success.
道具の選択は複雑なテーマであり、多くの場合（まったく適さないものを使わない限り）道具の選択は成功の決定的な要因ではない。
I recommend doing some research to whittle down a shortlist based on what technologies your team is familiar with, what has the widest level of usage, and what is under active development and support, and then setting a short-term goal and trying to achieve it using each of the tools on your shortlist.
あなたのチームがどのようなテクノロジーに精通しているか、どのようなものが最も広く使われているか、どのようなものが活発に開発されサポートされているかなどを基に、候補を絞り込むための調査を行い、短期的な目標を設定し、候補の各ツールを使ってその達成を試みることをお勧めする。

# Continuous Testing 継続的テスト

refs: https://continuousdelivery.com/foundations/test-automation/
を参照してください： https://continuousdelivery.com/foundations/test-automation/

The key to building quality into our software is making sure we can get fast feedback on the impact of changes.
私たちのソフトウェアに品質を組み込む鍵は、変更の影響に関するフィードバックを迅速に得られるようにすることです。
Traditionally, extensive use was made of manual inspection of code changes and manual testing (testers following documentation describing the steps required to test the various functions of the system) in order to demonstrate the correctness of the system.
従来は、システムの正しさを実証するために、コード変更の手作業による検査や手作業によるテスト（システムのさまざまな機能をテストするために必要な手順を記述した文書に従って、テスターがテストを行う）が多用されていた。
This type of testing was normally done in a phase following “dev complete”.
この種のテストは通常、「開発完了」に続く段階で行われた。
However this strategy have several drawbacks:
しかし、この戦略にはいくつかの欠点がある：

Manual regression testing takes a long time and is relatively expensive to perform, creating a bottleneck that prevents us releasing software more frequently, and getting feedback to developers weeks (and sometimes months) after they wrote the code being tested.
手動のリグレッション・テストには長い時間と比較的高価な費用がかかるため、ソフトウェアを頻繁にリリースすることができず、テスト対象のコードを書いてから数週間（場合によっては数カ月）後に開発者にフィードバックを得ることができないボトルネックになっている。

Manual tests and inspections are not very reliable, since people are notoriously poor at performing repetitive tasks such as regression testing manually, and it is extremely hard to predict the impact of a set of changes on a complex software system through inspection.
リグレッション・テストのような反復作業を手作業で行うことは、人間には苦手なことで有名であり、複雑なソフトウェア・システムに対する一連の変更の影響を検査によって予測することは極めて困難であるため、手作業によるテストや検査は、あまり信頼できるものではない。

When systems are evolving over time, as is the case in modern software products and services, we have to spend considerable effort updating test documentation to keep it up-to-date.
最近のソフトウェア製品やサービスのように、システムが時とともに進化していく場合、テスト文書を最新のものに更新するために、かなりの労力を費やさなければならない。

In order to build quality in to software, we need to adopt a different approach.
ソフトウェアに品質を組み込むためには、異なるアプローチを採用する必要がある。
Our goal is to run many different types of tests—both manual and automated—continually throughout the delivery process.
私たちの目標は、デリバリー・プロセスを通じて、手動と自動の両方で多くの異なるタイプのテストを継続的に実行することです。
The types of tests we want to run are nicely laid out the quadrant diagram created by Brian Marick, below:
ブライアン・マリックが作成したクワドラント・ダイアグラム（象限図）には、私たちが実行したいテストのタイプがきれいにレイアウトされている：

Once we have continuous integration and test automation in place, we create a deployment pipeline (the key pattern in continuous delivery).
継続的インテグレーションとテストの自動化が整ったら、デプロイメント・パイプラインを作成する（継続的デリバリーの重要なパターン）。
In the deployment pipeline pattern, every change runs a build that a) creates packages that can be deployed to any environment and b) runs unit tests (and possibly other tasks such as static analysis), giving feedback to developers in the space of a few minutes.
デプロイメント・パイプライン・パターンでは、すべての変更がビルドを実行し、a) あらゆる環境にデプロイ可能なパッケージを作成し、b) ユニットテスト（および場合によっては静的解析などの他のタスク）を実行し、数分のうちに開発者にフィードバックを与える。
Packages that pass this set of tests have more comprehensive automated acceptance tests run against them.
この一連のテストに合格したパッケージには、より包括的な自動受け入れテストが実行される。
Once we have packages that pass all the automated tests, they are available for self-service deplyment to other environments for activities such as exploratory testing, usability testing, and ultimately release.
すべての自動テストに合格したパッケージができたら、探索的テスト、ユーザビリティ・テスト、そして最終的なリリースといった活動のために、他の環境にセルフサービスでデプリメントできるようにする。
Complex products and services may have sophisticated deployment pipelines; a simple, linear pipeline is shown below:
複雑な製品やサービスには、洗練された配備パイプラインがあるかもしれない：

In the deployment pipeline, every change is effectively a release candidate.
デプロイメント・パイプラインでは、すべての変更が事実上リリース候補となる。
The job of the deployment pipeline is to catch known issues.
デプロイメント・パイプラインの仕事は、既知の問題をキャッチすることだ。
If we can’t detect any known problems, we should feel totally comfortable releasing any packages that have gone through it.
もし既知の問題が検出されなければ、それを通過したパッケージを安心してリリースできるはずだ。
If we aren’t, or if we discover defects later, it means we need to improve our pipeline, perhaps adding or updating some tests.
そうでない場合、あるいは後になって欠陥が見つかった場合は、パイプラインを改善する必要があることを意味する。

Our goal should be to find problems as soon as possible, and make the lead time from check-in to release as short as possible.
私たちの目標は、できるだけ早く問題を見つけ、チェックインからリリースまでのリードタイムをできるだけ短くすることだ。
Thus we want to parallelize the activities in the deployment pipeline, not have many stages executing in series.
したがって、デプロイメント・パイプラインのアクティビティを並列化し、多くのステージが直列に実行されないようにしたい。
There is also a feedback process: if we discover bugs in exploratory testing, we should be looking to improve our automated tests.
フィードバックのプロセスもある： 探索的テストでバグを発見したら、自動テストを改善するようにしなければならない。
If we discover a defect in the acceptance tests, we should be looking to improve our unit tests (most of our defects should be discovered through unit testing).
もし受け入れテストで不具合を発見したら、単体テストの改善に目を向けるべきだ（不具合のほとんどは単体テストで発見されるはずだ）。

Get started by building a skeleton deployment pipeline—create a single unit test, a single acceptance test, an automated deployment script that stands up an exploratory testing envrionment, and thread them together.
単体テスト、受け入れテスト、探索的テスト環境を立ち上げる自動デプロイメントスクリプトを作成し、それらをつなぎ合わせる。
Then increase test coverage and extend your deployment pipeline as your product or service evolves.
そして、製品やサービスの進化に合わせてテストカバレッジを拡大し、デプロイメントパイプラインを拡張する。

## Resources リソース

A 1h video in which Badri Janakiraman and I discuss how to create maintainable suites of automated acceptance test
Badri Janakiramanと私が、自動化された受け入れテストの保守可能なスイートを作成する方法について議論する1時間のビデオ。

Lisa Crispin and Janet Gregory have two great books on agile testing: Agile Testing and More Agile Testing
Lisa Crispin氏とJanet Gregory氏には、アジャイル・テストに関する2冊の素晴らしい本がある： アジャイルテストともっとアジャイルテスト

Elisabeth Hendrickson has written an excellent book on exploratory testing, Explore It!.
エリザベス・ヘンドリクソンは、探索的テストに関する優れた本『Explore It!
I recorded an interview with her where we discuss the role of testers, acceptance test driven development, and the impact of continuous delivery on testing.
テスターの役割、受け入れテスト主導の開発、継続的デリバリーがテストに与える影響などについて、彼女とのインタビューを収録した。
Watch her awesome 30m talk On the Care and Feeding of Feedback Cycles.
フィードバック・サイクルのケアとフィーディングについて」の30分間の講演をご覧ください。

Gojko Adzic’s Specification By Example has a series of interviews with successful teams worldwide and is a good distillation of effective patterns for specifying requirements and tests.
Gojko Adzicの『Specification By Example』には、世界中で成功を収めているチームへのインタビューが掲載されており、要件とテストを指定するための効果的なパターンがよくまとめられている。

Think that “a few minutes” is optimistic for running automated tests? Read Dan Bodart’s blog post Crazy fast build times
自動テストの実行に「数分」は楽観的だと思いますか？Dan Bodart氏のブログ記事「Crazy fast build times」をお読みください。

Martin Fowler discusses the Test Pyramid and its evil twin, the ice cream cone on his bliki.
マーティン・ファウラーが、テスト・ピラミッドとその邪悪な双子、アイスクリーム・コーンについて語る。

## FAQ FAQ

Does continuous delivery mean firing all our testers?
継続的デリバリーとは、テスターを全員解雇することなのだろうか？

No.
いや。
Testers have a unique perspective on the system—they understand how users interact with it.
テスターはシステムに対してユニークな視点を持っている-彼らはユーザーがどのようにシステムと相互作用するかを理解している。
I recommend having testers pair alongside developers (in person) to help them create and evolve the suites of automated tests.
私は、テスターが開発者と（直接）ペアを組み、自動テストのスイートの作成と進化を手助けすることを勧める。
This way, developers get to understand the testers’ perspective, and testers can start to learn test automation.
こうすることで、開発者はテスターの視点を理解できるようになり、テスターはテスト自動化を学び始めることができる。
Testers should also be performing exploratory testing continuously as part of their work.
また、テスターは業務の一環として、継続的に探索的テストを実施すべきである。
Certainly, testers will have to learn new skills—but that is true of anybody working in our industry.
確かに、テスターは新しいスキルを学ばなければならないが、それはこの業界で働く人すべてに当てはまることだ。

Should we be automating all of our tests?
すべてのテストを自動化すべきか？

No.
いや。
As shown in the quadrant diagram, there are still important manual activities such as exploratory testing and usability testing (although automation can help with these activities, it can’t replace people).
象限図に示されているように、探索的テストやユーザビリティ・テストといった重要な手作業はまだ残っている（自動化はこれらの活動を助けることはできるが、人の代わりにはならない）。
We should be aiming to bring all test activities, including security testing, into the development process and performing them continually from the beginning of the software delivery lifecycle for every product and service we build.
私たちは、セキュリティ・テストを含むすべてのテスト活動を開発プロセスに導入し、私たちが構築するすべての製品やサービスについて、ソフトウェア・デリバリー・ライフサイクルの最初から継続的に実施することを目指すべきである。

Should I stop and automate all of my manual tests right now?
今すぐ手動テストをすべて中止し、自動化すべきでしょうか？

No.
いや。
Start by writing a couple of automated tests—the ones that validate the most important functionality in the system.
システムの最も重要な機能を検証する自動テストをいくつか書くことから始めよう。
Get those running on every commit.
すべてのコミットでそれを実行させる。
Then the rule is to add new tests to cover new functionality that is added, and functionality that is being changed.
そして、新しく追加される機能や変更される機能をカバーするために、新しいテストを追加するのがルールだ。
Over time, you will evolve a comprehensive suite of automated tests.
時間をかけて、自動テストの包括的なスイートを進化させていく。
In general, it’s better to have 20 tests that run quickly and are trusted by the team than 2,000 tests that are flaky and constantly failing and which are ignored by the team.
一般的に、不安定で常に失敗し、チームから無視される2,000のテストよりも、素早く実行され、チームから信頼される20のテストの方が良い。

Who is responsible for the automated tests?
誰が自動テストに責任を持つのか？

The whole team.
チーム全員だ。
In particular, developers should be involved in creating and maintaining the automated tests, and should stop what they are doing and fix them whenever there is a failure.
特に、開発者は自動テストの作成と保守に携わるべきであり、失敗があるときはいつでも自分のやっていることを中断して修正すべきである。
This is essential because it teaches developers how to write testable software.
これは、テスト可能なソフトウェアを書く方法を開発者に教えるために不可欠である。
When automated tests are created and maintained by a different group from the developers, there is no force acting on the developers to help them write software that is easy to test.
自動テストが開発者とは別のグループによって作成され、管理されている場合、開発者がテストしやすいソフトウェアを書くのを助ける力は働かない。
Retrofitting automated tests onto such systems is painful and expensive, and poorly designed software that is hard to test is a major factor contributing to automated test suites that are expensive to maintain.
このようなシステムに自動テストを後付けするのは、手間とコストがかかる。また、テストしにくいお粗末な設計のソフトウェアは、自動テスト・スイートの維持にコストがかかる主な要因である。
