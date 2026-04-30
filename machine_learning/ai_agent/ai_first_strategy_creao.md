refs: https://x.com/intuitiveml/article/2043545596699750791


# Why Your "AI-First" Strategy Is Probably Wrong あなたの「AIファースト」戦略はおそらく間違っている

Peter Pang
Peter Pang

@intuitiveml
@intuitiveml

· 4月13日
・4月13日

99% of our production code is written by AI. Last Tuesday, we shipped a new feature at 10 AM, A/B tested it by noon, and killed it by 3 PM because the data said no. We shipped a better version at 5 PM. Three months ago, a cycle like that would have taken six weeks.
私たちのプロダクションコードの99%はAIが書いている。先週の火曜日、午前10時に新機能をリリースし、正午までにA/Bテストを行い、データが「NO」と告げたので午後3時にキルした。午後5時にはより良いバージョンをリリースした。3ヶ月前なら、このサイクルは6週間かかっていただろう。

We didn't get here by adding Copilot to our IDE. We dismantled our engineering process and rebuilt it around AI. We changed how we plan, build, test, deploy, and organize the team. We changed the role of everyone in the company.
ここに到達したのはIDEにCopilotを追加したからではない。エンジニアリングプロセスを解体し、AIを中心に再構築した。計画、ビルド、テスト、デプロイ、チーム編成のすべての方法を変えた。社内全員の役割を変えた。

CREAO is an agent platform. Twenty-five employees, 10 engineers. We started building agents in November 2025, and two months ago I restructured the entire product architecture and engineering workflow from the ground up.
CREAOはエージェントプラットフォームだ。従業員25人、エンジニア10人。2025年11月にエージェントの構築を開始し、2ヶ月前にプロダクトアーキテクチャとエンジニアリングワークフロー全体をゼロから再構築した。

OpenAI published a concept in February 2026 that captured what we'd been doing. They called it harness engineering: the primary job of an engineering team is no longer writing code. It is enabling agents to do useful work. When something fails, the fix is never "try harder." The fix is: what capability is missing, and how do we make it legible and enforceable for the agent?
OpenAIは2026年2月に、我々がやってきたことを的確に表現するコンセプトを公開した。彼らはそれを「ハーネスエンジニアリング(harness engineering)」と呼んだ。**エンジニアリングチームの主な仕事はもはやコードを書くことではない。エージェントが有用な仕事をできるようにすること**だ。何かが失敗したとき、修正は決して「もっと頑張れ」ではない。修正とは「どの能力が欠けているのか、そしてそれをエージェントにとって読み取り可能で強制可能なものにするにはどうすればよいのか」だ。

We arrived at that conclusion on our own. We didn't have a name for it.
私たちは自力でその結論にたどり着いた。名前は持っていなかった。

<!-- ここまで読んだ! -->

## AI-First Is Not the Same as Using AI AIファーストはAIを使うこととは違う

Most companies bolt AI onto their existing process. An engineer opens Cursor. A PM drafts specs with ChatGPT. QA experiments with AI test generation. The workflow stays the same. Efficiency goes up 10 to 20 percent. Nothing structurally changes.
**ほとんどの企業は既存のプロセスにAIを後付けする。エンジニアはCursorを開く。PMはChatGPTで仕様書を書く。QAはAIテスト生成を試す。ワークフローは変わらない。効率は10〜20%向上する。構造的には何も変わらない。**
That is AI-assisted.
それは「AI支援(AI-assisted)」だ。

<!-- ここまで読んだ! -->

AI-first means you redesign your process, your architecture, and your organization around the assumption that AI is the primary builder. You stop asking "how can AI help our engineers?" and start asking "how do we restructure everything so AI does the building, and engineers provide direction and judgment?"
**AIファーストとは、AIが主たる構築者であるという前提のもとで、プロセス、アーキテクチャ、組織を再設計すること**だ。「AIはどうすれば我々のエンジニアを助けられるか？」と問うのをやめ、「AIが構築を行い、エンジニアが方向性と判断を提供するように、すべてをどう再構築するか？」と問い始める。

The difference is multiplicative.
その違いは乗算的(multiplicative)だ。

I see teams claim AI-first while running the same sprint cycles, the same Jira boards, the same weekly standups, the same QA sign-offs. They added AI to the loop. They didn't redesign the loop.
**AIファーストを謳いながら、同じスプリントサイクル、同じJiraボード、同じ週次スタンドアップ、同じQAサインオフを回しているチームを目にする。彼らはループにAIを追加しただけ。ループを再設計していない。**

A common version of this is what people call vibe coding. Open Cursor, prompt until something works, commit, repeat. That produces prototypes. A production system needs to be stable, reliable, and secure. You need a system that can guarantee those properties when AI writes the code. You build the system. The prompts are disposable.
よくあるパターンは、いわゆる「vibe coding」だ。Cursorを開き、何かが動くまでプロンプトを打ち、コミットし、繰り返す。それはプロトタイプは生む。だがプロダクションシステムには安定性、信頼性、セキュリティが必要だ。AIがコードを書くときにそれらの性質を保証できるシステムが必要だ。あなたが構築すべきは「システム」。プロンプトは使い捨てだ。

<!-- ここまで読んだ! -->

## Why We Had to Change なぜ変えなければならなかったのか

Last year, I watched how our team worked and saw three bottlenecks that would kill us.
昨年、チームの働き方を観察していて、我々を殺しかねない3つのボトルネックが見えた。

### The Product Management Bottleneck プロダクトマネジメントのボトルネック

Our PMs spent weeks researching, designing, specifying features. Product management has worked this way for decades. But agents can implement a feature in two hours. When build time collapses from months to hours, a weeks-long planning cycle becomes the constraint.
我々のPMは数週間かけてリサーチ、設計、機能仕様化を行っていた。プロダクトマネジメントは何十年もこのやり方で機能してきた。**しかしエージェントは機能を2時間で実装できる**。ビルド時間が数ヶ月から数時間に縮まると、数週間の計画サイクルが制約条件になる。

It doesn't make sense to think about something for months and then build it in two hours.
**何かを数ヶ月考えてから、それを2時間で構築するのは筋が通らない。**

PMs needed to evolve into product-minded architects who work at the speed of iteration, or step out of the build cycle. Design needed to happen through rapid prototype-ship-test-iterate loops, not specification documents reviewed in committee.
PMはイテレーション速度で動く「プロダクトマインドを持ったアーキテクト」へ進化するか、ビルドサイクルから降りる必要があった。**設計は委員会でレビューされる仕様書ではなく、高速なプロトタイプ→出荷→テスト→反復のループを通じて行われる必要があった。**

<!-- ここまで読んだ! -->

### The QA Bottleneck QAのボトルネック

Same dynamic. After an agent shipped a feature, our QA team spent days testing corner cases. Build time: two hours. Test time: three days.
同じ力学だ。**エージェントが機能をリリースした後、QAチームはコーナーケースのテストに何日もかけていた。**ビルド時間：2時間。テスト時間：3日。

We replaced manual QA with AI-built testing platforms that test AI-written code. Validation has to move at the same speed as implementation. Otherwise you've built a new bottleneck ten feet downstream from the old one.
手動QAを、AIが書いたコードをテストするAI製テスティングプラットフォームに置き換えた。**検証は実装と同じ速度で動かなければならない。さもなくば、古いボトルネックの10フィート下流に新しいボトルネックを作っただけ**だ。

<!-- ここまで読んだ! -->

### The Headcount Bottleneck 人員のボトルネック

Our competitors had 100x or more people doing comparable work. We have 25. We couldn't hire our way to parity. We had to redesign our way there.
競合は同じような仕事を100倍以上の人数でやっていた。我々は25人。採用で同等になることはできない。設計し直して同等に達するしかなかった。

Three systems needed AI running through them: how we design product, how we implement product, and how we test product. If any single one stays manual, it constrains the whole pipeline.
**3つのシステムにAIを通す必要があった：プロダクトの設計、実装、テストの方法だ。どれか1つでも手動のままなら、それがパイプライン全体を制約する。**

## The Bold Decision: Unifying the Architecture 大胆な決断：アーキテクチャの統合

I had to fix the codebase first.
まずコードベースを直す必要があった。

Our old architecture was scattered across multiple independent systems. A single change might require touching three or four repositories. From a human engineer's perspective, it is manageable. From an AI agent's perspective, opaque. The agent can't see the full picture. It can't reason about cross-service implications. It can't run integration tests locally.
旧アーキテクチャは複数の独立したシステムにまたがっていた。1つの変更で3〜4のリポジトリを触らなければならないこともあった。人間エンジニア視点では何とか管理できる。AIエージェント視点では不透明だ。エージェントは全体像が見えない。サービス横断的な影響について推論できない。統合テストをローカルで実行できない。

I had to unify all the code into a single monorepo. One reason: so AI could see everything.
**すべてのコードを単一のmonorepoに統合しなければならなかった。理由は1つ：AIがすべてを見られるようにするためだ。**

This is a harness engineering principle in practice. The more of your system you pull into a form the agent can inspect, validate, and modify, the more leverage you get. A fragmented codebase is invisible to agents. A unified one is legible.
これがハーネスエンジニアリングの原則の実践だ。システムをエージェントが検査・検証・修正できる形に多く引き込むほど、レバレッジが効く。断片化されたコードベースはエージェントには見えない。統合されたコードベースは読み取り可能だ。

I spent one week designing the new system: planning stage, implementation stage, testing stage, integration testing stage. Then another week re-architecting the entire codebase using agents.
新システムの設計に1週間費やした：計画ステージ、実装ステージ、テスティングステージ、統合テスティングステージ。その後さらに1週間、エージェントを使ってコードベース全体を再アーキテクトした。

CREAO is an agent platform. We used our own agents to rebuild the platform that runs agents. If the product can build itself, it works.
CREAOはエージェントプラットフォームだ。エージェントを動かすそのプラットフォーム自体を、自分たちのエージェントを使って再構築した。プロダクトが自分自身を構築できるなら、それは機能している証拠だ。

<!-- ここまで読んだ! -->

## The Stack スタック構成

Here is our stack and what each piece does.
以下が我々のスタックと各コンポーネントの役割だ。

### Infrastructure: AWS インフラ：AWS

We run on AWS with auto-scaling container services and circuit-breaker rollback. If metrics degrade after a deployment, the system reverts on its own.
オートスケーリングのコンテナサービスとサーキットブレーカー型ロールバックを備えたAWS上で動かしている。デプロイ後にメトリクスが悪化すれば、システムは自動で巻き戻る。

CloudWatch is the central nervous system. Structured logging across all services, over 25 alarms, custom metrics queried daily by automated workflows. Every piece of infrastructure exposes structured, queryable signals. If AI can't read the logs, it can't diagnose the problem.
CloudWatchが中枢神経系だ。全サービスを通じた構造化ロギング、25以上のアラーム、自動化ワークフローで毎日クエリされるカスタムメトリクス。インフラの一部一部が構造化されクエリ可能なシグナルを公開している。AIがログを読めなければ、問題を診断できない。

### CI/CD: GitHub Actions CI/CD：GitHub Actions

Every code change passes through a six-phase pipeline:
**すべてのコード変更は6フェーズのパイプラインを通過する**：

Verify CI → Build and Deploy Dev → Test Dev → Deploy Prod → Test Prod → Release
CI検証 → Devビルドとデプロイ → Devテスト → 本番デプロイ → 本番テスト → リリース

The CI gate on every pull request enforces typechecking, linting, unit and integration tests, Docker builds, end-to-end tests via Playwright, and environment parity checks. No phase is optional. No manual overrides. The pipeline is deterministic, so agents can predict outcomes and reason about failures.
すべてのプルリクエスト上のCIゲートは、型チェック、リント、ユニット/統合テスト、Dockerビルド、Playwrightによるエンドツーエンドテスト、環境パリティチェックを強制する。どのフェーズも省略不可。手動オーバーライドなし。パイプラインは決定論的なので、エージェントは結果を予測し失敗について推論できる。

<!-- ここまで読んだ! -->

### AI Code Review: Claude AIコードレビュー：Claude

Every pull request triggers three parallel AI review passes using Claude Opus 4.6:
すべてのプルリクエストは、Claude Opus 4.6を使った3つの並列AIレビューパスをトリガーする：

Pass 1: Code quality. Logic errors, performance issues, maintainability.
パス1：コード品質。ロジックエラー、パフォーマンス問題、保守性。

Pass 2: Security. Vulnerability scanning, authentication boundary checks, injection risks.
パス2：セキュリティ。脆弱性スキャン、認証境界チェック、インジェクションリスク。

Pass 3: Dependency scan. Supply chain risks, version conflicts, license issues.
パス3：依存関係スキャン。サプライチェーンリスク、バージョン衝突、ライセンス問題。

These are review gates, not suggestions. They run alongside human review, catching what humans miss at volume. When you deploy eight times a day, no human reviewer can sustain attention across every PR.
**これらは「サジェスト」ではなくレビューの「ゲート」だ。人間レビューと並走し、量のなかで人間が見落とすものを拾う。1日8回デプロイすれば、どの人間レビュアーもすべてのPRに注意を維持できない。**

Engineers also tag @claude in any GitHub issue or PR for implementation plans, debugging sessions, or code analysis. The agent sees the whole monorepo. Context carries across conversations.
エンジニアはまた、実装プラン、デバッグセッション、コード解析が必要なGitHub issueやPRで @claude をタグ付けする。エージェントはmonorepo全体を見ている。コンテキストは会話をまたいで保持される。

## The Self-Healing Feedback Loop 自己修復するフィードバックループ

This is the centerpiece.
これが本丸だ。

Every morning at 9:00 AM UTC, an automated health workflow runs. Claude Sonnet 4.6 queries CloudWatch, analyzes error patterns across all services, and generates an executive health summary delivered to the team via Microsoft Teams. Nobody had to ask for it.
毎朝UTC 9:00、自動化されたヘルスワークフローが走る。Claude Sonnet 4.6 がCloudWatchをクエリし、全サービスのエラーパターンを分析し、Microsoft Teams経由でチームにエグゼクティブヘルスサマリを配信する。誰も依頼する必要がない。

One hour later, the triage engine runs. It clusters production errors from CloudWatch and Sentry, scores each cluster across nine severity dimensions, and auto-generates investigation tickets in Linear. Each ticket includes sample logs, affected users, affected endpoints, and suggested investigation paths.
1時間後、トリアージエンジンが走る。CloudWatchとSentryから本番エラーをクラスタリングし、各クラスタを9つの深刻度次元でスコアリングし、Linearに自動で調査チケットを作る。各チケットにはサンプルログ、影響を受けたユーザー、影響を受けたエンドポイント、推奨される調査経路が含まれる。

The system deduplicates. If an open issue covers the same error pattern, it updates that issue. If a previously closed issue recurs, it detects the regression and reopens.
システムはデデュープする。同じエラーパターンをカバーするオープンissueがあれば、それを更新する。以前クローズしたissueが再発したら、リグレッションを検知して再オープンする。

When an engineer pushes a fix, the same pipeline handles it. Three Claude review passes evaluate the PR. CI validates. The six-phase deploy pipeline promotes through dev and prod with testing at each stage. After deployment, the triage engine re-checks CloudWatch. If the original errors are resolved, the Linear ticket auto-closes.
エンジニアが修正をプッシュすると、同じパイプラインがそれを処理する。3つのClaudeレビューパスがPRを評価する。CIが検証する。6フェーズのデプロイパイプラインが各ステージでテストしながらdevと本番にプロモートする。デプロイ後、トリアージエンジンが再度CloudWatchをチェックする。元のエラーが解消していれば、Linearチケットは自動でクローズされる。

Each tool handles one phase. No tool tries to do everything. The daily cycle creates a self-healing loop where errors are detected, triaged, fixed, and verified with minimal manual intervention.
各ツールは1つのフェーズを担う。何でもやろうとするツールは存在しない。日次サイクルが、エラーを検知・トリアージ・修正・検証する自己修復ループを作り出し、手作業の介入は最小限で済む。

I told a reporter from Business Insider: "AI will make the PR and the human just needs to review whether there's any risk."
Business Insiderの記者にこう話した：「AIがPRを作り、人間はリスクがあるかどうかをレビューするだけでいい」。

<!-- ここまで読んだ! -->

### Feature Flags and the Supporting Stack フィーチャーフラグと補助スタック

Statsig handles feature flags. Every feature ships behind a gate. The rollout pattern: enable for the team, then gradual percentage rollout, then full release or kill. The kill switch toggles a feature off instantly, no deploy needed. If a feature degrades metrics, we pull it within hours. Bad features die the same day they ship. A/B testing runs through the same system.
フィーチャーフラグはStatsigが扱う。あらゆる機能はゲートの裏側でリリースされる。**ロールアウトパターン：チーム向けに有効化 → 段階的にパーセンテージで展開 → 完全リリースまたはキル。キルスイッチは機能を即座にオフにし、デプロイ不要。機能がメトリクスを悪化させれば、数時間以内に取り下げる。悪い機能はリリース当日のうちに死ぬ。A/Bテストも同じシステムで走る。**(rolloutいいね!:thinking:)

Graphite manages PR branching: merge queues rebase onto main, re-run CI, merge only if green. Stacked PRs allow incremental review at high throughput.
PRブランチングはGraphiteが管理する：マージキューがmainの上にrebaseし、CIを再実行し、グリーンの場合のみマージする。Stacked PRが高スループットでの段階的レビューを可能にする。

Sentry reports structured exceptions across all services, merged with CloudWatch by the triage engine for cross-tool context. Linear is the human-facing layer: auto-created tickets with severity scores, sample logs, and suggested investigation. Deduplication prevents noise. Follow-up verification auto-closes resolved issues.
Sentryは全サービスにわたる構造化例外を報告し、トリアージエンジンがCloudWatchと統合してツール横断的なコンテキストを作る。Linearは人間向けのレイヤーだ：深刻度スコア、サンプルログ、推奨調査が付いた自動作成チケット。デデュープがノイズを防ぐ。フォローアップ検証が解決済みissueを自動クローズする。

<!-- ここまで読んだ! -->

## How a Feature Moves from Idea to Production 機能がアイデアから本番に到達する流れ

### New Feature Path 新機能パス

1. The architect defines the task as a structured prompt with codebase context, goals, and constraints.
アーキテクトがコードベースのコンテキスト、ゴール、制約を含む構造化プロンプトとしてタスクを定義する。

2. An agent decomposes the task, plans implementation, writes code, and generates its own tests.
エージェントがタスクを分解し、実装を計画し、コードを書き、自分でテストを生成する。

3. A PR opens. Three Claude review passes evaluate it. A human reviewer checks for strategic risk, not line-by-line correctness.
PRがオープンする。3つのClaudeレビューパスが評価する。人間レビュアーは行ごとの正しさではなく戦略的リスクをチェックする。

4. CI validates: typecheck, lint, unit tests, integration tests, end-to-end tests.
CIが検証：型チェック、リント、ユニットテスト、統合テスト、エンドツーエンドテスト。

5. Graphite's merge queue rebases, re-runs CI, merges if green.
GraphiteのマージキューがrebaseしCIを再実行し、グリーンならマージする。

6. Six-phase deploy pipeline promotes through dev and prod with testing at each stage.
6フェーズのデプロイパイプラインが各ステージでテストしつつdevと本番にプロモートする。

7. Feature gate turns on for the team. Gradual percentage rollout. Metrics monitored.
フィーチャーゲートをチーム向けにオン。段階的なパーセンテージロールアウト。メトリクス監視。

8. Kill switch available if anything degrades. Circuit-breaker auto-rollback for severe issues.
何か悪化すればキルスイッチを使用可能。深刻な問題にはサーキットブレーカーで自動ロールバック。

<!-- ここまで読んだ! -->

### Bug Fix Path バグ修正パス

1. CloudWatch and Sentry detect errors.
CloudWatchとSentryがエラーを検知する。

2. Claude triage engine scores severity, creates a Linear issue with full investigation context.
Claudeトリアージエンジンが深刻度をスコア化し、完全な調査コンテキスト付きのLinear issueを作る。

3. An engineer investigates. AI has already done the diagnosis. The engineer validates and pushes a fix.
エンジニアが調査する。AIはすでに診断済み。エンジニアは検証して修正をプッシュする。

4. Same review, CI, deploy, and monitoring pipeline.
同じレビュー、CI、デプロイ、モニタリングのパイプライン。

5. Triage engine re-verifies. If resolved, ticket auto-closes.
トリアージエンジンが再検証する。解決していればチケットは自動クローズ。

Both paths use the same pipeline. One system. One standard.
両方のパスが同じパイプラインを使う。1つのシステム。1つの標準。



## The Results 結果

Over 14 days, we averaged three to eight production deployments per day. Under our old model, that entire two-week period would have produced not even a single release to production.
14日間で1日平均3〜8回の本番デプロイ。旧モデルでは、その2週間で本番リリースは1回も出せなかっただろう。

Bad features get pulled the same day they ship. New features go live the same day they're conceived. A/B tests validate impact in real time.
**悪い機能はリリース当日に取り下げられる。新機能は構想された当日にライブになる。A/Bテストはインパクトをリアルタイムで検証する。**

People assume we're trading quality for speed. User engagement went up. Payment conversion went up. We produce better results than before, because the feedback loops are tighter. You learn more when you ship daily than when you ship monthly.
**人々は我々が速度のために品質を犠牲にしていると思い込む。ユーザーエンゲージメントは上がった。決済コンバージョンも上がった。フィードバックループがタイトになった分、以前より良い結果を生んでいる。月次でリリースするより日次でリリースした方が学びは多い。**

<!-- ここまで読んだ! -->

## The New Engineering Org 新しいエンジニアリング組織

Two types of engineers will exist.
エンジニアは2種類存在する。

### The Architect アーキテクト

One or two people. They design the standard operating procedures that teach AI how to work. They build the testing infrastructure, the integration systems, the triage systems. They decide architecture and system boundaries. They define what "good" looks like for the agents.
1〜2人。AIに働き方を教える標準作業手順(SOP)を設計する。テスティング基盤、統合システム、トリアージシステムを構築する。アーキテクチャとシステム境界を決める。エージェントにとっての「良い」を定義する。

This role requires deep critical thinking. You criticize AI. You don't follow it. When the agent proposes a plan, the architect finds the holes. What failure modes did it miss? What security boundaries did it cross? What technical debt is it accumulating?
**この役割には深い批判的思考が要る。AIを批判する。AIに従うのではなく。エージェントが計画を提案したら、アーキテクトは穴を見つける。**どんな失敗モードを見落としたか？どんなセキュリティ境界を越えたか？どんな技術的負債を溜めているか？

I have a PhD in physics. The most useful thing my PhD taught me was how to question assumptions, stress-test arguments, and look for what's missing. The ability to criticise AI will be more valuable than the ability to produce code.
私は物理学のPhDを持っている。PhDから学んだ最も有用なことは、前提を疑い、議論をストレステストし、欠けているものを探す方法だ。**AIを批判する能力は、コードを生み出す能力よりも価値を持つようになる。**

This is also the hardest role to fill.
そしてこの役割が最も埋めるのが難しい。

<!-- ここまで読んだ! -->

### The Operator オペレーター

Everyone else. The work matters. The structure is different.
それ以外の全員。仕事には意味がある。構造が違うだけだ。

AI assigns tasks to humans. The triage system finds a bug, creates a ticket, surfaces the diagnosis, and assigns it to the right person. The person investigates, validates, and approves the fix. AI makes the PR. The human reviews whether there's risk.
AIが人間にタスクを割り当てる。トリアージシステムがバグを見つけ、チケットを作り、診断を表に出し、適切な人にアサインする。その人は調査し、検証し、修正を承認する。AIがPRを作る。人間はリスクの有無をレビューする。

The tasks are bug investigation, UI refinement, CSS improvements, PR review, verification. They require skill and attention. They don't require the architectural reasoning the old model demanded.
タスクはバグ調査、UI洗練、CSS改善、PRレビュー、検証だ。スキルと注意は必要。だが旧モデルが要求したアーキテクチャ推論は不要だ。

### Who Adapts Fastest 最も早く適応するのは誰か

I noticed a pattern I didn't expect. Junior engineers adapted faster than senior engineers.
予想外のパターンに気づいた。ジュニアエンジニアの方がシニアエンジニアより早く適応した。

Junior engineers with less traditional practice felt empowered. They had access to tools that amplified their impact. They didn't carry a decade of habits to unlearn.
従来式の経験が少ないジュニアエンジニアは力を得た気がしていた。インパクトを増幅するツールにアクセスできた。アンラーンすべき10年分の習慣を持っていなかった。

Senior engineers with strong traditional practice had the hardest time. Two months of their work could be completed in one hour by AI. That is a hard thing to accept after years of building a rare skill set.
従来式の経験が強いシニアエンジニアが最も苦労した。彼らの2ヶ月分の仕事がAIによって1時間で完了し得る。希少なスキルセットを年月をかけて築き上げた後では受け入れがたい事実だ。

I'm not making a judgment. I'm describing what I observed. In this transition, adaptability matters more than accumulated skill.
判断を下しているのではない。観察したことを述べている。この移行期では、蓄積されたスキルよりも適応力の方が重要だ。

<!-- ここまで読んだ! -->

## The Human Side 人間の側面

### Management Collapsed　マネジメントは崩壊した

Two months ago, I spent 60% of my time managing people. Aligning priorities. Running meetings. Giving feedback. Coaching engineers.
2ヶ月前、私の時間の60%は人をマネジメントすることに費やされていた。優先順位の整合、ミーティング、フィードバック、エンジニアのコーチング。

Today: below 10%.
今日：10%未満。

The traditional CTO model says to empower your team to do architecture work, train them, delegate. But if the system only needs one or two architects, I need to do it myself first. I went from managing to building. I code from 9 AM to 3 AM most days. I design the SOPs and architecture of the system. I maintain the harness.
従来のCTOモデルは、チームに権限委譲してアーキテクチャを担当させ、教育し、委譲しろと言う。しかしシステムがアーキテクトを1〜2人しか必要としないなら、まず自分でやらねばならない。マネジメントからビルドへ移った。ほとんどの日、午前9時から午前3時までコードを書いている。システムのSOPとアーキテクチャを設計する。ハーネスを保守する。

More stressful. But I'm enjoying building, not aligning.
よりストレスフルだ。だが、整合作業ではなくビルドを楽しんでいる。

### Less Arguing, Better Relationships 議論は減り、関係は良くなった

My relationships with co-founders and engineers are better than before.
共同創業者やエンジニアとの関係は以前より良好だ。

Before the transition, most of my interaction with the team was alignment meetings. Discussing trade-offs. Debating priorities. Disagreeing about technical decisions. Those conversations are necessary in a traditional model. They're also draining.
移行前、チームとのやり取りの大半はアライメントミーティングだった。トレードオフの議論、優先順位の論争、技術判断の対立。これらは従来モデルでは必要な会話だ。同時に消耗もする。

Now I still talk to my team. We talk about other things. Non-work topics. Casual conversations. Offsite trips. We get along better because we stopped arguing about work that can be easily done by our system.
今もチームと話す。だが他のことを話す。仕事以外の話題。雑談。オフサイト旅行。我々のシステムに容易に任せられる仕事について議論するのをやめたから、関係が良くなった。

### Uncertainty Is Real 不確実性は現実だ

I won't pretend everyone is happy.
全員がハッピーだとは言わない。

When I stopped talking to people every day, some team members felt uncertain. What does the CTO not talking to me mean? What is my value in this new world? Reasonable concerns.
毎日人と話すのをやめたら、不安を覚えるメンバーが出た。「CTOが話してくれないのは何を意味するのか？」「この新世界での私の価値は？」もっともな懸念だ。

Some people spend more time debating whether AI can do their work than doing the work. The transition period creates anxiety. I don't have a clean answer for it.
仕事をするより、AIにその仕事ができるかを議論するのに多くの時間を費やす人もいる。移行期は不安を生む。それに対する綺麗な答えは持っていない。

I do have a principle: we don't fire an engineer because they introduced a production bug. We improve the review process. We strengthen testing. We add guardrails. The same applies to AI. If AI makes a mistake, we build better validation, clearer constraints, stronger observability.
**1つ原則はある：プロダクションバグを混入させたからといってエンジニアを解雇しない。レビュープロセスを改善する。テストを強化する。ガードレールを追加する。AIにも同じことが当てはまる。AIがミスをすれば、より良い検証、より明確な制約、より強いオブザーバビリティを作る。**

<!-- ここまで読んだ! -->

## Beyond Engineering エンジニアリングを超えて

I see other companies adopt AI-first engineering and leave everything else manual.
他社がAIファーストエンジニアリングを採用しつつ、他はすべて手動のまま放置しているのを見る。

If engineering ships features in hours but marketing takes a week to announce them, marketing is the bottleneck. If the product team still runs a monthly planning cycle, planning is the bottleneck.
エンジニアリングが数時間で機能をリリースしてもマーケティングが告知に1週間かければ、マーケティングがボトルネックだ。**プロダクトチームが月次の計画サイクルを回していれば、計画がボトルネックだ。**

At CREAO, we pushed AI-native operations into every function:
CREAOではAIネイティブな運用をあらゆる機能に押し広げた：

Product release notes: AI-generated from changelogs and feature descriptions.
プロダクトリリースノート：チェンジログと機能記述からAI生成。

Feature intro videos: AI-generated motion graphics.
機能紹介動画：AI生成のモーショングラフィックス。

Daily posts on socials: AI-orchestrated and auto-published.
SNSでの日次投稿：AIが調整し自動公開。

Health reports and analytics summaries: AI-generated from CloudWatch and production databases.
ヘルスレポートとアナリティクスサマリ：CloudWatchと本番DBからAI生成。

Engineering, product, marketing, and growth run in one AI-native workflow. If one function operates at agent speed and another at human speed, the human-speed function constrains everything.
エンジニアリング、プロダクト、マーケティング、グロースが1つのAIネイティブワークフローで動く。ある機能がエージェント速度で動き、別の機能が人間速度で動くなら、人間速度の機能がすべてを制約する。

## What This Means これが意味するもの

### For Engineers エンジニアへ

Your value is moving from code output to decision quality. The ability to write code fast is worth less every month. The ability to evaluate, criticize, and direct AI is worth more.
**あなたの価値はコードのアウトプットから判断の質へ移っている。速くコードを書く能力の価値は毎月下がっている。AIを評価し、批判し、方向づける能力の価値は上がっている。**

Product sense or taste matters. Can you look at a generated UI and know it's wrong before the user tells you? Can you look at an architecture proposal and see the failure mode the agent missed?
プロダクトセンスやテイストが重要だ。生成されたUIを見て、ユーザーに言われる前に「これは違う」と分かるか？アーキテクチャ提案を見て、エージェントが見落とした失敗モードを見抜けるか？

I tell our 19-year-old interns: train critical thinking. Learn to evaluate arguments, find gaps, question assumptions. Learn what good design looks like. Those skills compound.
19歳のインターンにこう伝えている：**批判的思考を鍛えよ。議論を評価し、ギャップを見つけ、前提を疑え。良い設計とは何かを学べ。それらのスキルは複利で効く。**

<!-- ここまで読んだ! -->

### For CTOs and Founders CTOと創業者へ

If your PM process takes longer than your build time, start there.
PMプロセスがビルド時間より長くかかっているなら、そこから始めよ。

Build the testing harness before you scale agents. Fast AI without fast validation is fast-moving technical debt.
エージェントをスケールする前にテスティングハーネスを作れ。高速な検証を伴わない高速なAIは、高速に動く技術的負債だ。

Start with one architect. One person who builds the system and proves it works. Onboard others into operator roles after the system runs.
1人のアーキテクトから始めよ。システムを構築し、それが機能することを証明する1人だ。システムが回り始めてから、他のメンバーをオペレーター役としてオンボードする。

Push AI-native into every function.
AIネイティブをあらゆる機能に押し広げよ。

Expect resistance. Some people will push back.
抵抗を予期せよ。反発する人は出る。

### For the Industry 業界へ

OpenAI, Anthropic, and multiple independent teams converged on the same principles: structured context, specialized agents, persistent memory, and execution loops. Harness engineering is becoming a standard.
OpenAI、Anthropic、そして複数の独立したチームが**同じ原則に収斂**している：構造化されたコンテキスト、専門化されたエージェント、永続的メモリ、実行ループ。ハーネスエンジニアリングは標準になりつつある。

Model capability is the clock driving this. I attribute the entire shift at CREAO to the last two months. Opus 4.5 couldn't do what Opus 4.6 does. Next-gen models will accelerate it further.
これを駆動する時計はモデルの能力だ。CREAOにおけるシフト全体を直近2ヶ月に帰属させる。Opus 4.5にはOpus 4.6ができることはできなかった。次世代モデルはこれをさらに加速させるだろう。

I believe one-person companies will become common. If one architect with agents can do the work of 100 people, many companies won't need a second employee.
一人会社が一般的になると私は信じている。エージェントを持つ1人のアーキテクトが100人分の仕事をできるなら、多くの企業は2人目の従業員を必要としない。

<!-- ここまで読んだ! -->

## We're Early まだ初期段階だ

Most founders and engineers I talk to still operate the traditional way. Some think about making the shift. Very few have done it.
私が話す創業者やエンジニアの多くは今も従来式で動いている。シフトを考えている人もいる。実行した人はごく僅かだ。
A reporter friend told me she'd talked to about five people on this topic. She said we were further along than anyone: "I don't think anyone's just totally rebuilt their entire workflow the way you have."
記者の友人は、このテーマで5人ほどに話を聞いたと教えてくれた。彼女曰く、我々は誰よりも先を行っているという：「あなた方のようにワークフロー全体を完全に再構築した人はいないと思う」。
The tools exist for any team to do this. Nothing in our stack is proprietary.
どのチームでもこれを行うためのツールは存在する。我々のスタックに独自のものはない。

The competitive advantage is the decision to redesign everything around these tools, and the willingness to absorb the cost. The cost is real: uncertainty among employees, the CTO working 18-hour days, senior engineers questioning their value, a two-week period where the old system is gone and the new one isn't proven.
競争優位は、これらのツールを中心にすべてを再設計するという「決断」と、そのコストを引き受ける「意思」だ。コストは現実のものだ：従業員間の不確実性、1日18時間働くCTO、自身の価値を問い直すシニアエンジニア、旧システムは消え新システムはまだ証明されていない2週間の谷。

We absorbed that cost. Two months later, the numbers speak.
我々はそのコストを引き受けた。2ヶ月後、数字が物語っている。
We build an agent platform. We built it with agents.
我々はエージェントプラットフォームを作る。我々はそれをエージェントで作った。

---

Peter Pang
Peter Pang

@intuitiveml
@intuitiveml

🚀 Co-founder, CreaoAI. Previously GenAI @ Meta (LLaMA). xApple. Join the journey ↓
🚀 CreaoAI共同創業者。元 Meta GenAI（LLaMA）、元Apple。一緒に旅しよう ↓

<!-- ここまで読んだ! -->
