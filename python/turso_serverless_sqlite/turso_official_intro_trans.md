## refs:

- https://turso.tech/blog/turso-the-next-evolution-of-sqlite

# Introducing the first alpha of Turso: The next evolution of SQLite Tursoの最初のアルファを紹介します：SQLiteの次の進化

Glauber Costa
グラウバー・コスタ

Almost six months ago, we announced a bold project: we were going to invest in a full rewrite of SQLite from scratch. 
約6ヶ月前、私たちは大胆なプロジェクトを発表しました：SQLiteをゼロから完全に書き直すことに投資するつもりです。
Codenamed "Project Limbo", it quickly amassed palpable interest, and a community of contributors. 
「プロジェクト・リンボ」と名付けられたこのプロジェクトは、すぐに実感できる関心を集め、貢献者のコミュニティが形成されました。

Today, we reached the point where we are confident enough in its quality that we are ready for the first alpha release. 
今日、私たちはその品質に自信を持てる段階に達し、最初のアルファリリースの準備が整いました。

Now officially named "Turso" — the next evolution of SQLite. 
今や正式に「Turso」と名付けられ、SQLiteの次の進化となります。

We've built Turso using advanced testing techniques, both our own and through our partnership with Antithesis, an autonomous testing platform. 
私たちは、独自の高度なテスト技術と、自律型テストプラットフォームであるAntithesisとの提携を通じて、Tursoを構築しました。
This approach will allow us to match SQLite's legendary reliability. 
このアプローチにより、SQLiteの伝説的な信頼性に匹敵することが可能になります。
We're so confident in our methodology that we'll pay you $1,000 if you find a data corruption bug that our testing missed. 
**私たちは自分たちの方法論に非常に自信を持っており、私たちのテストで見逃したデータ破損バグを見つけた場合には、1,000ドルをお支払いします**。

<!-- ここまで読んだ! -->

## #Why rewrite SQLite? なぜSQLiteを再構築するのか？

We believe SQLite is the best piece of software on the planet. 
私たちは、**SQLiteが地球上で最高のソフトウェアである**と信じています。
It is fast, reliable, and it fits everywhere. 
それは高速で信頼性が高く、どこにでも適合します。
But modern applications require access patterns that SQLite often can’t handle. 
**しかし、現代のアプリケーションは、SQLiteがしばしば処理できないアクセスパターンを必要とします。**
After more than a year operating a cloud service based on SQLite, those are the common complaints we hear: 
SQLiteに基づくクラウドサービスを運営して1年以上経った今、私たちが耳にする一般的な不満は次のとおりです：

- SQLite cannot handle concurrent writes. SQLiteは同時書き込みを処理できません。
This not only limits the throughput of SQLite for use cases like data collection and logging, but also makes writing to SQLite unreliable, since concurrent writes can fail even at low throughput, leading to a bad experience. 
これは、データ収集やログ記録のようなユースケースにおけるSQLiteのスループットを制限するだけでなく、同時書き込みが低スループットでも失敗する可能性があるため、SQLiteへの書き込みを信頼性のないものにし、悪い体験をもたらします。

- Writing realtime applications that react to data changes is a challenge with SQLite, since there is no good support for capturing a stream of changes. データの変更に反応するリアルタイムアプリケーションを書くことは、SQLiteでは難しい課題です。なぜなら、**変更のストリームをキャプチャするための良いサポートがない**からです。

- SQLite has limited support for non-relational data, such as vector embeddings and timeseries. SQLiteは、ベクトル埋め込みや時系列などの非relationalデータに対するサポートが限られています。

- SQLite exposes a synchronous API, which makes it harder for it to work well on some environments, like the browser. 
SQLiteは同期APIを公開しており、これによりブラウザのような特定の環境でうまく機能するのが難しくなります。(i.e. 非同期APIが公開されていないので、パフォーマンスやUXの面で不利になり得る)

- Evolving the schema of applications with SQLite is a challenge. 
- SQLiteを使用したアプリケーションのスキーマを進化させることは難しい課題です。
  - 補足:
    - カラム追加とカラム名変更しな基本サポートされてなくて、カラム削除・型変更・複雑な制約変更はサポートされてない。
    - これらの操作を行うには、テーブルの作り直しになる!

The rise of AI saw SQLite taking center stage. 
AIの台頭により、SQLiteは中心的な役割を果たすようになりました。
SQLite was already the top choice for physical systems like robots and cars. 
**SQLiteはすでにロボットや車のような物理システムにとっての最適な選択肢**でした。(エッジデバイス上での利用か...!:thinking:)
But we now see people reaching out for it for agentic memory, AI builders, and many other applications. 
しかし、私たちは今、エージェントメモリ、AIビルダー、そして多くの他のアプリケーションのためにそれ(=上述のSQLiteの弱み)を求める人々を見ています。

Ultimately, from a purely technical position, SQLite itself can evolve to provide all the features it needs to adapt to our new landscape. 
最終的には、純粋に技術的な観点から、SQLite自体は新しい環境に適応するために必要なすべての機能を提供するように進化できます。
However, the closed nature of its community - SQLite doesn’t accept contributions from anybody, makes changes unacceptably slow for today’s fast-paced development environment. 
しかし、そのコミュニティの閉鎖的な性質 - SQLiteは誰からの貢献も受け入れないため、変更が今日の急速な開発環境において受け入れがたいほど遅くなります。
(SQLiteって、学部の人が開発とかに自由に参加できない状態なの??:thinking:)

Since it was publicly announced six months ago, Turso now has more than 115 contributors. 
6ヶ月前に公に発表されて以来、Tursoには現在115人以上の貢献者がいます。
So we can confidently say: the most important feature we’re adding to our project is you: Turso gives you a seat at the table, and leverages the true power of Open Source. 
したがって、私たちは自信を持って言えます：私たちのプロジェクトに追加している最も重要な機能はあなたです：**Tursoはあなたに席を提供し、オープンソースの真の力を活用**します。

If you are interested in shaping what the next generation of SQLite can be, our community is open and waiting! 
次世代のSQLiteがどのようになるかを形作ることに興味があるなら、私たちのコミュニティはオープンで待っています！

<!-- ここまで読んだ! -->

## #SQLite is the most reliable software on the planet. SQLiteは地球上で最も信頼性の高いソフトウェアです。

We know. That’s why we like it so much! Ever since we started talking about rewriting SQLite, we hear the same opposition: SQLite is well known for its out-of-this-world reliability. 
私たちはそれを知っています。だからこそ、私たちはそれをとても好きなのです！SQLiteの書き直しについて話し始めて以来、私たちは同じ反対意見を耳にします：**SQLiteはその驚異的な信頼性**でよく知られています。なぜそれを再構築するのでしょうか？
The hidden assumption is that a rewrite will necessarily be less reliable than SQLite. 
**隠れた前提は、再構築は必然的にSQLiteよりも信頼性が低くなるということ**です。

We understand where this comes from: SQLite's legendary reliability comes from decades of testing and battle-hardening. 
私たちはこの考えがどこから来ているのか理解しています：**SQLiteの伝説的な信頼性は、数十年にわたるテストと耐久性の向上から**来ています。
But we're not just matching that standard — we're surpassing it using modern techniques that weren't available when SQLite was built. 
しかし、私たちはその基準に単に合わせるのではなく、SQLiteが構築されたときには利用できなかった現代の技術を使ってそれを超えています。

From day one, Turso uses Deterministic Simulation Testing (DST)— the same approach that made databases like FoundationDB and TigerBeetle incredibly robust. 
初日から、TursoはDeterministic Simulation Testing (DST)を使用しています—これはFoundationDBやTigerBeetleのようなデータベースを非常に堅牢にしたアプローチです。
DST systematically explores thousands of failure scenarios and edge cases, verifying that critical system properties hold under every condition. 
DSTは、数千の障害シナリオやエッジケースを体系的に探求し、重要なシステム特性がすべての条件下で保持されることを確認します。
Unlike traditional testing, DST doesn't just test what you think might break - it discovers failure modes you never considered. 
従来のテストとは異なり、DSTはあなたが壊れると思うものだけをテストするのではなく、あなたが考えもしなかった障害モードを発見します。

We've also partnered with Antithesis, an autonomous testing platform that runs our code in a deterministic hypervisor, injecting faults while continuously verifying system properties. 
私たちはまた、Antithesisという自律的なテストプラットフォームと提携しています。このプラットフォームは、決定論的ハイパーバイザーで私たちのコードを実行し、システム特性を継続的に検証しながら障害を注入します。
This catches bugs that even our own simulator might miss, including bugs in the simulator itself. 
これにより、私たち自身のシミュレーターが見逃す可能性のあるバグ、シミュレーター自体のバグもキャッチします。

The result? We can systematically test Turso against complex failure scenarios and edge cases that would be nearly impossible to reproduce with traditional testing methods, giving us a level of confidence and reliability that a rewrite of SQLite demands. 
その結果は？私たちは、従来のテスト方法では再現することがほぼ不可能な複雑な障害シナリオやエッジケースに対してTursoを体系的にテストでき、SQLiteの再構築が要求する信頼性と自信のレベルを得ることができます。
We're so confident in this approach that we're putting our money where our mouth is: find a data corruption bug that our testing missed, show us how to improve our simulator to catch it, and we'll pay you $1,000 through our partnership with Algora. 
私たちはこのアプローチに非常に自信を持っているので、実際に行動に移します：**私たちのテストが見逃したデータ破損バグを見つけ、それをキャッチするためにシミュレーターを改善する方法を示してくれれば、私たちはAlgoraとの提携を通じてあなたに$1,000を支払います。**

This is just the beginning. As we expand beyond alpha, both the scope and rewards will grow significantly. 
これは始まりに過ぎません。私たちがアルファを超えて拡大するにつれて、範囲と報酬は大幅に増加します。

<!-- ここまで読んだ! -->

## #What to expect from this Alpha? このアルファで期待できること

This alpha includes support for the basic features of SQLite, and introduces Turso's key differentiators: an asynchronous interface that replaces SQLite's synchronous API, and native vector search capabilities. 
このアルファは、SQLiteの基本機能のサポートを含み、**SQLiteの同期APIを置き換える非同期インターフェースと、ネイティブベクトル検索機能というTursoの主要な差別化要因**を紹介します。
On Linux, there is work-in-progress support for io_uring for high-performance async operations. 
Linuxでは、高性能な非同期操作のためのio_uringのサポートが進行中です。
The async interface makes Turso work seamlessly in environments where blocking isn't possible, like browsers, while vector search enables AI and ML applications without external dependencies. 
**非同期インターフェースにより、Tursoはブラウザのようなブロッキングが不可能な環境でシームレスに動作**し、**ベクトル検索は外部依存関係なしにAIおよびMLアプリケーションを可能にします**。

What works: Core database operations (SELECT, INSERT, DELETE, UPDATE, ALTER TABLE, JOIN, transactions), most SQLite functions including JSON support, and native vector search ported from Turso Cloud for AI and ML workloads. 
動作するもの: コアデータベース操作（SELECT、INSERT、DELETE、UPDATE、ALTER TABLE、JOIN、トランザクション）、JSONサポートを含むほとんどのSQLite機能、およびAIおよびMLワークロードのためにTurso Cloudから移植されたネイティブベクトル検索。

What's still in development: Indexes, multi-threading, savepoints, triggers, views, and VACUUM operations. 
まだ開発中のもの: インデックス、マルチスレッド、セーブポイント、トリガー、ビュー、およびVACUUM操作。

The complete feature status is tracked here and updated as development progresses. 
完全な機能のステータスはここで追跡され、開発が進むにつれて更新されます。

Our focus for this alpha has been building the rock-solid testing foundation that will sustain Turso for decades to come, ensuring every feature we ship meets our reliability standards. 
このアルファの焦点は、Tursoを今後数十年にわたって支える堅牢なテスト基盤を構築することであり、私たちが提供するすべての機能が信頼性基準を満たすことを保証します。

Yet, despite how early it is, Turso is already starting to find its way into existing projects, as a replacement for SQLite. 
しかし、まだ初期段階にもかかわらず、**TursoはすでにSQLiteの代替として既存のプロジェクトに取り入れられ始めています。**
One example is Spice.ai, a data and AI inference engine which uses local databases like SQLite and DuckDB as accelerators in their product. 
一例として、[Spice.ai](https://spiceai.org/)があります。これは、**SQLiteやDuckDBのようなローカルデータベースを製品のアクセラレーターとして使用するデータおよびAI推論エンジン**です。

The performance of the underlying accelerator is key to a great experience, and in some queries, they already see better performance with Turso versus their SQLite implementation, and expect even more performance gains to be unlocked once Turso implements concurrent writes. 
基盤となるアクセラレーターのパフォーマンスは素晴らしい体験の鍵であり、いくつかのクエリでは、すでにTursoの方がSQLiteの実装よりも優れたパフォーマンスを示しており、Tursoが同時書き込みを実装するとさらにパフォーマンスの向上が期待されます。

Turso’s Rust-based rewrite of SQLite brings cloud-native, concurrent performance to AI apps and agents. 
**TursoのRustベース**のSQLiteの書き換えは、AIアプリやエージェントにクラウドネイティブで同時実行可能なパフォーマンスをもたらします。
As workloads shift to fast, lightweight databases like SQLite and DuckDB, Turso takes SQLite beyond its concurrency limits, strengthening the ecosystem for scalable, data-driven apps. 
**ワークロードがSQLiteやDuckDBのような高速で軽量なデータベースに移行する中**、TursoはSQLiteをその同時実行の限界を超えて進化させ、スケーラブルでデータ駆動型のアプリのエコシステムを強化します。 — Luke Kim, Founder and CEO of Spice AI

- 「ワークロードがSQLiteやDuckDBのような高速で軽量なデータベースに移行する中...」について補足:
  - 今現在、アプリやサービスのデータ保存・分析のやり方が"高速・軽量DBMS"へどんどんシフトしていってるらしい。そうなの??
  - クラウドネイティブは「分散」「小さい単位で多数のDB」「高速リソース解放」がトレンドだから、巨大RDB & 集中型から徐々にローカル&軽量系にシフトしてるらしい。ほんと??
    - エッジデバイス上のDBとかそういうことなのかな...:thinking:

If you are working with applications that would benefit from concurrent writes, or any other functionality that you feel SQLite is missing, join us on Discord. 
同時書き込みから恩恵を受けるアプリケーションや、SQLiteに欠けていると感じる他の機能を扱っている場合は、Discordに参加してください。
We still have open slots for design partners. 
私たちはまだデザインパートナーのための空き枠があります。

<!-- ここまで読んだ! -->

## #Thanks to our partners パートナーへの感謝

Our alpha milestone was stability and reliability. 
私たちのアルファマイルストーンは、安定性と信頼性でした。
We have achieved this milestone in months. 
私たちは数ヶ月でこのマイルストーンを達成しました。
That is because aside from our own native simulator, we partner with Antithesis, an autonomous testing platform. 
それは、私たち自身のネイティブシミュレーターに加えて、私たちが**自律テストプラットフォームであるAntithesis**と提携しているからです。
Whatever bug our simulator doesn’t catch, including bugs in the simulator itself, is usually caught by Antithesis. 
私たちのシミュレーターが捕まえられないバグ、シミュレーター自体のバグを含めて、通常はAntithesisによって捕まえられます。

Antithesis provides a deterministic hypervisor that injects faults into the system while verifying that the system properties hold. 
Antithesisは、システムの特性が保持されていることを検証しながら、システムに故障を注入する決定論的ハイパーバイザーを提供します。
Because of them, we could flesh out bugs and get to the confidence level required to announce this release much sooner than we would otherwise. 
彼らのおかげで、私たちはバグを明らかにし、このリリースを発表するために必要な信頼レベルに、他の方法よりもはるかに早く到達することができました。

Constantly running all that testing infrastructure is also prohibitively expensive with Github Actions. 
そのすべてのテストインフラを常に稼働させることは、Github Actionsでは非常に高額です。
Thankfully, through our partnership with Blacksmith, this is one concern we don’t have. 
幸いなことに、Blacksmithとの提携により、これは私たちの懸念事項ではありません。
A high-performance CI infrastructure allows us to catch issues faster and keep the quality of our offering at all times. 
高性能なCIインフラは、私たちが問題をより早く捕まえ、常に提供する品質を維持することを可能にします。

Finally, we are ready to pay anyone $1,000 for bugs that lead to data corruption (and a higher dollar amount and scope in the future). 
**最後に、データの破損につながるバグに対して、誰にでも1,000ドルを支払う準備ができています（将来的にはより高額で範囲も広がる予定です）。**
While we are confident in the level of quality we have achieved, some bugs will invariably be there, lurking in the nastiest corner cases, especially in the beginning. 
私たちは達成した品質レベルに自信を持っていますが、特に初期段階では、最も厄介なコーナーケースに潜むバグが必ず存在します。
Paying people compliantly in whichever country they are is a challenge, and we are thankful for Algora's support on this. 
どの国にいる人々に対しても適切に支払うことは課題であり、私たちはこれに関してAlgoraのサポートに感謝しています。

<!-- ここまで読んだ! -->
