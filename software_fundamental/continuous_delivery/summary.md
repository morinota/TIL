## Continuous Deliveryの5つの原則

継続的デリバリーの中心には、以下の5つの原則がある。

- 1. **品質を組み込む(Build Quality In)**
- 2. 小さいbatchで作業する(Work in Small Batches)
- 3. コンピュータに反復タスクをさせ、人間は問題解決に集中する(Computers Perform Repetitive Tasks, People Solve Problems)
- 4. 絶え間なく継続的改善を追求する(Relentlessly Pursue Continuous Improvement)
- 5. 皆が責任を持つ(Everyone is Responsible)

### 原則1 「品質を組み込む(Build Quality In)」

- リーン運動で有名らしいエドワーズ・デミングの「マネジメントの為の14の主要原則」の中の第3原則に基づく。
  - 第3原則「**品質を達成するために検査に依存するのをやめよ。最初からプロダクトに品質を組み込むことによって、大量の検査を必要としないようにせよ**」
  - (プロダクトに品質保証の振る舞いを組み込む、みたいな...??:thinking:プロダクトコードの一部としてのテストコードとかの話か...!)
- ローカル環境で自動テストを実行して、**問題や欠陥を即座に見つける事ができれば、理想的にはバージョン管理にチェックインされる前に見つけることができれば、問題や欠陥を修正するコストははるかに安くなる**。
  - 検査(手動テストなど)を通じて下流側で欠陥を見つけることは、時間がかかり、大規模なトリアージ(整理すること??:thinking:)が必要となる。
  - リリース後に欠陥を見つける場合、まずバージョン管理システム上で、原因となったPRやcommitを見つける必要がある。そして、**数日前、あるいは数週間前にcommitした時に考えていたことを思い出しながら、不具合を修正しなければならない...!** (早く発見できた方が圧倒的に楽...!:thinking:)
- 問題や欠陥を可能な限り早期に発見する為のfeedback loop (=CD pipeline?)を作り、それを進化させ続ける事は、継続的デリバリーにおいて不可欠な作業。
  - 探索的テスト(=開発者による不具合発生後のテスト??)で問題を見つけた場合、プロダクトコード内の原因箇所を修正するだけでなく、次にこう尋ねる必要がある
    - 「**その問題を、自動受け入れテストで検出する事は可能だったのか??**」
    - もし受け入れテストでその問題を検出できた場合...
      - 「**その問題を、ユニットテストで検出する事は可能だったのか??**」
    - (質問の答えがYesなのであれば、次回以降はその問題を自動テストで検知できるようにしていく...!全てのテストケースを最初から網羅する事はできないだろうし:thinking:)

### 原則2 「小ロットで仕事をする(Work in Small Batches)」

- 従来の段階的なソフトウェア開発アプローチでは...
  - 開発->テスト->テスト->運用へのリリース全体の流れは、数十人から数百人からなるチームによる、数カ月分の作業。
- 継続的デリバリーでは、逆のアプローチを取る。
  - **可能な限りすべての変更をバージョン管理に取り込み、できるだけ迅速に包括的なフィードバックを得る事を目指す**。
- 小ロットでの作業には多くの利点がある。
  - **仕事にフィードバックを得る時間を短縮**し、問題の整理と解決を用意にする(なるほど...!このPRが原因だってすぐに分かる!)
  - 効率とモチベーションを高める(確かに! PR mergeできると嬉しい)、
  - 沈没コストの誘惑から守る。(柔軟に方向転換できる、みたいな??:thinking:)
- なぜ従来は大ロットで作業をしていたのかというと...
  - (次の工程のチームに)変更を引き渡すための固定費が大きいから。
    - (そもそも開発、テスト、運用を別々のチームが担ってるから、この変更引き渡しのコストが大きい...??:thinking:)
- 継続的デリバリーの主要な目標のひとつ:
  - ソフトウェアデリバリープロセスの経済を変え、**小ロットでの作業が経済的に可能になるようにする事で**、このアプローチの多くの利点を得ること。
  - (小ロットでの作業を経済的に可能にする = 開発、テスト、運用のチームを一つのチームにまとめるってこと?:thinking:)

### 原則3 「コンピュータに反復タスクをさせ、人間は問題解決に集中する(Computers Perform Repetitive Tasks, People Solve Problems)」

- トヨタ伝統の哲学的思想の一つに「自動化」がある。
  - その目的は、**regression testの様な単純で反復的な作業はコンピュータに行わせ、人間は問題解決に集中できるようにする事**。
  - ↑のように、コンピュータと人間は互いに補完し合う。
  - (ABテストダッシュボード作成業務を自動化してぇ～)
- 多くの人は、自動化によって仕事がなくなるのではないかと心配するが...
  - まず、人々は頭を使わない雑務から解放され、より価値の高い活動に集中することができる。
    - 成功している会社で仕事が不足することはない。
  - また、品質を向上させる利点もある。
    - なぜなら、人間は、頭を使わない作業をするときに最もミスを犯しやすいからだ。

### 原則4 「絶え間なく継続的改善を追求する(Relentlessly Pursue Continuous Improvement)」

- 継続的改善(Continuous Improvement)も、リーン運動の重要なアイデアの一つ。
  - トヨタ自動車のTaiichi Ohno の言葉「カイゼンの機会は無限にある」が有名。
  - **以前よりも良くなったと思って安心してはいけない**。
    - 剣術で3回中2回師匠に勝ったという生徒が誇りに思うのと同じ。
  - 改善アイデアの芽を1つ摘むと、日常の仕事の中で、**1つの改善アイデアのすぐ下にもう1つの改善アイデアがある**という態度を持つことが重要。
    - (この「改善アイデアの芽を摘む」という表現は、low hanging fruit的な表現と似てるな...!)
- "改善"を1つのプロジェクトとして扱って完了してしまい、日常業務に戻るべきではない。
  - **最良の組織とは、全員が改善活動を日常業務の不可欠な一部として扱い、誰も現状に満足しない組織**である

### 原則5 「皆が責任を持つ(Everyone is Responsible)」

- 高い業績を上げている組織では、"誰か他の人の問題"は存在しない
  - 開発チームは、自分たちが構築したソフトウェアの品質と安定性(i.e. 運用しやすさ)に責任を持つ。一方で、運用チームは、開発チームの品質構築を支援する責任がある。
  - **自分のチームや部署に最適なものを最適化するのではなく、組織全体の目標を達成するためにみんなで協力する**。
    - (うーん、これはABテストで最適化すべきmetricsについても言えることだよなぁ...:thinking:)
- 人々が局所的な最適化を行うと、組織全体としてのパフォーマンスが低下することがある。
  - ↑はしばしば、間違った行動にインセンティブを与えるようなシステム的な問題が原因だったりする。
    - ex.) 開発者に対して速度を上げることや多くのコードを書くことを報酬とし、テスターには見つけたバグの数に基づいて報酬を与えること。
    - (これはよく例で挙げられてるやつ! :thinking:)
- 多くの人間は正しい事をしたいと思っている。しかし、人間は報酬に基づいて行動を適応させるもの。
  - -> **本当に重要なことからのフィードバック・ループを作成することが非常に重要!**(重要なmetricsを考える...!)
    - ex. 我々が開発したプロダクトにユーザがどのように反応しているか、組織への利益は??

## 継続的デリバリーの3つの基盤(foundations)について

継続的デリバリーは、以下の**3つの基盤**に基づいている。

- 1. 包括的な設定管理(comprehensive configuration management)
- 2. 継続的インテグレーション(continuous integration)
- 3. 継続的テスト(continuous testing)

### 基盤1: 包括的な設定管理(configuration management)について

- ソフトウェアを反復的にかつ信頼性高くリリースすることを保証する上で、**自動化は重要な役割を果たす**。
  - 自動化が果たす重要な役割の1つ
    - -> ビルド、デプロイ、退行テスト、インフラプロビジョニング(インフラのリソースを予測して提供すること?)のような、繰り返しの多い手作業プロセスを自動化すること。
    - -> これを実現するためには、**これらのプロセスを実行するために必要な全てのものをバージョン管理する必要がある**。
      - ex. ソースコード、テスト及びデプロイメントスクリプト、インフラおよびアプリケーションのconfig、依存する多くのライブラリやパッケージ, etc...
      - (version管理の重要さって、自動化するためなのか...!:thinking:)
    - また、ソフトウェア環境の現在と過去の状態を簡単に紹介できるようにしたい、というモチベーションもある。
      - (うん、これはversion管理のメリットとして想像しやすい:thinking:)
- configurationに関して、2つの最優先目標がある。

  - 1. **再現性(Reproducibility)**
    - 完全に自動化された方法で、どのような環境でもソフトウェアをビルド・デプロイ・テストでき、**同じconfigurationから再現される新しい環境は全て同じ結果を返す**ようにする必要がある。
  - 2. **追跡性(Traceability)**
    - 任意の環境を選んだときに、**その環境を作成するために使用された全ての依存関係のバージョンを迅速かつ正確に特定できる**ようにする必要がある。
    - また、任意の環境の過去のバージョンを比較し、**その間に何が変更されたかを特定できるようにする**必要がある。

- 達成したい上記の2つの能力(再現性、追跡性)は、開発組織に以下の重要な利点を与えてくれる:

  - 1. 迅速な災害復旧(disaster recovery)
  - 2. 高い監査可能性(Auditability)
  - 3. より高い品質(higher quality)
    - ソフトウェアのデリバリープロセスでは、開発・テスト・本番環境の準備を待つために、長い遅延が発生することがよくある。
    - これらを**バージョン管理から自動的に行うことができれば、変更影響に対するfeedbackをより迅速に得ることができ、ソフトウェアに品質を組み込むことができる**...!
  - 4. 容量管理(capacity management):
    - インフラの定義をバージョニング
  - 5. 欠陥への迅速な対応(quick response to defects)
    - システムに欠陥や脆弱性が見つかった時、できるだけ早くソフトウェアの新バージョンをリリースしたい。
      - 多くの組織では、緊急リリースのためのプロセスを持ってる。(ex. テストや監査の一部をバイパス、スキップする)
      - しかしこれは、safety-criticalなアプリケーションにおいて深刻なジレンマをもたらす。(テストスキップしちゃってるからじゃん...!:thinking:)
    - **理想的には、緊急リリースに通常のリリースプロセスが適用できるようになってることが望ましい! これが、包括的なconfiguration managementによって継続的デリバリーが実現したいこと...!**

- 全てのconfigをversion管理したいと言いつつも、完璧な再現性と追跡性を達成する事は不可能。

  - (version管理できない状態がどうしても存在するってことかな...!:thinking:)
  - **従って、configuration管理の重要なポイントは、投資に対して利益をより多く得るために、アーキテクチャ & 実行環境 & プロセスの単純化に取り組むこと...!!**
    - 投資(i.e. 費用) = 全てのconfig情報をversion管理するためのコスト
    - 利益(i.e. 効果) = 高い再現性と追跡性を達成することで得られるpositiveな効果

- 利益を達成するために努力する場合、我々は常に、**達成したい目標を測定可能な言葉で定義することから始めるべき**。
  - -> 目標に到達するための可能な経路のうち、最も良いものが何かを判断し、アプローチが高価すぎるか、時間がかかりすぎることがわかった場合には、**方向を変えたり、目標を再評価したりすることができる**。
    - (ABテストにおいてもmetricsを検討・feedbackを経て推敲し続けることが大事、みたいな話があったなぁ:thinking:)

#### FAQ

- どんなツールを使えば良い?
  - 多くの場合(全く適さないものを使わない限り)、道具の選択は成功の決定的な要因ではない。
- コンテナ/クラウド/仮想化技術は、このトピックにどのように影響する??
  - 最も重要なことは、**新たな進歩があるたびに、前述したような利益を、より簡単により安く達成できるようになる**ということ。
  - しかし、それ自体が特効薬というわけではない。
  - 我々が目標を達成するためには、引き続きバージョン管理とデプロイメント・パイプラインの包括的な使用の原則を適用する必要がある。

### 基盤2: 継続的インテグレーションについて

- **大前提、複数の開発者の仕事を組み合わせるのは難しい**。（これがCIのoriginなのか...!:thinking:）
  - ソフトウェアシステムは複雑であり、一見単純で自己完結的な単一ファイルへの変更でも、簡単に意図しない結果をもたらし、システムの正確性を損なうことがある。
  - trunk/masterブランチを安定させるために...
    - **開発者が互いに孤立して自分のブランチで作業する**。
    - これはまた、お互いの足を踏まないようにするためでもある。
    - (trunk = 主要な開発ラインや基盤となるブランチを指す)
- しかし...
  - 各ブランチは互いに離れていく。
    - 1つのブランチをmainにマージするのは簡単。でも、**複数の長期ブランチをメインに統合するためには**、苦痛が伴うような大量の再作業が必要になる。
    - (Continuous Integrationは、長期ブランチをなるべく使わないように、**短期ブランチで継続的に統合していきましょう**、みたいな戦略のこと??:thinking:)
  - 長期ブランチを採用してるチームはどうしてる??
    - -> リリース前に複数のブランチを統合するために、コードフリーズ、もしくは統合(integration)&安定化(stabilization)フェーズに時間を使ってる。
    - 近代的なツールを使っても、このプロセスはまだ高価で予測不可能。
    - この問題は、**チームの規模が大きくなるにつれて、またブランチの寿命が長くなるにつれて、指数関数的に深刻になっていく**。
- そこで、継続的インテグレーションのプラクティス!
  - CIは、XP(エクストリームプログラミング)の原則に従う。
    - i.e. 「**if something is painful, we should do it more often, and bring the pain forward(何かが痛いときは、より頻繁に行い、痛みを前に出すべきだ)**」という原則。
- CIでは、**開発者は定期的に（少なくとも毎日）すべての作業をトランク（メインラインまたはマスターとも呼ばれる）に統合**する。(ええ！？CI難しそう...!:thinking:)
  - 自動テスト集合は、regressionが発生しないことを検証するために、マージ前とマージ後の両方で実行される。
  - もし自動テストが失敗した場合、チームは自分達の作業を中断し、誰かが直ちに問題を修正する。
    - (特にtrunk base開発とか、誰かが失敗したらチーム全員の作業が止まって全員で解決するのであれば、チームのバス係数は下がりそう...?:thinking:)
  - -> これにより、**ソフトウェアが常に稼働状態にあること、また開発者ブランチがtrunkから大きく分岐しないこと**を確認する。

継続的インテグレーションの利点は非常に大きく、スループットの向上、システムの安定性、ソフトウェアの品質の向上につながることが研究によって示されている。しかし**CIの実践には以下の2つの障壁がある**。

- 理由1: CIは、開発者に次の要求を課す: 「**大きな機能変更などを、trunk/masterに頻繁に統合できるような、よりsmallな & よりincrementalなステップに分割せよ**」
  - 課題感:
    - このやり方に不慣れな開発者にとっては、パラダイムシフトになる。また、大きな機能を「完成」させるのにもより時間がかかる...。
  - しかしそもそも、我々が最適化したいのは...!
    - X 開発者が自分の作業をブランチ上で「開発完了!」と宣言できる速度
    - ○ **変更をレビューし、統合し、テストし、デプロイできる速度**
      - -> これは、変更が小さく、自己完結しており、変更が所属するブランチが短命である場合に大幅に速度向上できる...!
      - (じゃあCIのプラクティスって、タスクを小さく分割して、短命ブランチでincrementalに開発していけってこと??:thinking:)
- 理由2: CIは、システムに次の要求を課す: 「**包括的な自動ユニットテストを高速に実行させよ**」

  - (CIと自動テストは同一の概念ではないけど、CIのプラクティスを実現するために自動テストが必要なのか...!:thinking:)
  - 自動テストは、ソフトウェアが期待通りに動作するという高い信頼レベルを提供するために**十分包括的であるべき**。かつ、**数分以内に実行されるべき**。
    - もし自動テストの実行に時間がかかると -> 開発者は頻繁に実行したくなくなる。
  - 自動テストのテストスイートの作成に関しては、TDDを通じて最もよく行われる。
    - CIにおけるTDDの最も重要な利点:
      - **モジュール化されてテストしやすいコードを書くことを保証できる -> 結果として、自動テストスイートのメンテナンスコストを削減できる...**!
      - (TDDによって、CIを実践するための包括的な自動テストを推進できる...!:thinking:)
    - ただTDDはまだ十分に普及してない。

- 上記2点の障壁にもかかわらず、CDの度を始めたい組織にとって、開発チームがCIの実践を支援することは最優先事項:
  - -> **CIは、迅速なフィードバックループを作成し、開発者が小ロットで作業することを保証することにより**、チームがソフトウェアに品質を組み込むことを可能にし、これにより、継続的なソフトウェア開発のコストを削減し、チームの生産性と彼らが生み出す作業の品質を向上させる。

#### FAQ

- 自分のチームが本当にCIを実践しているかどうかを知る方法は?
  - 3つの質問に答えられるか
    - 1. チーム内の全エンジニアが毎日 trunk/masterブランチにコードをpushしているか。
    - 2. すべてのコミットがユニットテストの実行のトリガーになっているか？ (なってる!:thinking:)
    - 3. ビルドが壊れたとき、通常10分以内に修正されるか?
  - 経験則的には、CIを実施していると思ってるチームのうち、実際にテストに合格できるのは20％以下。
    - CIツールを使わずにCIを行うことも可能であり、逆に、CIツールを使っているからといって、CIを行っているわけではないことに注意。
- トランクベースの開発とは、feature togglesを使うこと??
  - いいえ。
    - feature toggles は congigオプションを使って、ユーザから特定の機能を隠すこと。
  - feature togglesを使わずにtrunk-basedな開発を可能にするためには、**2つの重要なプラクティス**がある。
    - 1. APIに依存するUIを作成する前に、APIを構築すべき。
      - **API(それに対して実行される自動テストを含む)は、「ダーク」（つまり、それを呼び出すものがない状態）で作成され、本番環境にデプロイされることができ**、私たちはトランクでストーリーの実装に取り組むことができる。
    - 2. **大きな機能を小さなストーリー（1〜3日の作業）に分解し、それらが互いに反復的に、増分的に構築されるようにすることを目指すべき**。

<!-- 以下のコードレビューの話が良かった! -->

- Github-styleのデプロイについてどう思う??
  - ->ブランチが1日以上生存しない限り、GitHubの「フロー」プロセスは問題ない。
    - **もしあなたが機能をストーリーに分解し、インクリメンタルな開発を実践しているならOK**...!
  - また、コードレビューはプロセスの中で行うべき!
    - 理想的には、チェックインの準備ができたときに誰かを招待してペアプログラミングを行い、その場でコードをレビューする
      - (うんうん...!ルールズオブプログラミングでも述べられてた...!:thinking:)
    - **コードレビューは継続的に行うのが最善であり、小ロットで作業することでそれが可能になる**
      - (なるほど! ペアプロ的にレビューを行いやすくするためにもsmall batchesで作業する必要があるのか...!:thinking:)
    - 何日もの作業の結果であるページ数の多いdiffをレビューするのは誰も楽しめない。**なぜなら、大きな変更がシステム全体に与える影響を理解することができないから**。
      - (確かに、大きな変更をレビューするのは大変で、小さな変更をレビューするのは簡単だ!:thinking:)

### 基盤3: 継続的テストについて

- **CDの原則1つ目「Build quality in(品質を組み込む)」を達成するポイントは、変更の影響に関するフィードバックを迅速に得られるようにすること**。
  - (そのために、継続的テストが重要...!)
  - 従来は...
    - 手動テストが主流!　この種のテストは「開発完了」の後のフェーズで行われてた。
    - 開発完了後の手動テスト戦略の3つの欠点:
      - 1. 手動テストには長い時間とコストがかかる -> ソフトウェアを頻繁にリリースできない。また、テスト対象のコードを書いて開発者にフィードバックを提供するのに数週間or数ヶ月かかる。
      - 2. regiressionテストのような反復作業を手作業で行うことは、人間には苦手で有名...!
        - 一連の変更の影響を検査で予測することは極めて困難であり、**手作業によるテストや検査は、そもそもあまり信頼できるものではない**...!!
      - 3. 最新のソフトウェアプロダクトは、システムの仕様がダイナミックに変化し得るので、テスト文書を最新の状態に保つことが困難。

上記の欠点から、「Build quality in(品質を組み込む)」を達成するためには、従来と異なるアプローチを採用する必要がある。
「我々の目標は、**デリバリープロセスの全体を通して、多くの異なるタイプのテスト(手動 & 自動)を継続的に実行させること**!」

以下の4象限図には、我々が実行させたいテストのタイプが示されている。

![](https://continuousdelivery.com/images/test-quadrant.png)

- 第一象限(左上): showcases usability testing, exploratory testing (manual)
  - 探索的なテスト、ユーザビリティテスト
- 第二象限(右上): functional testing (automated)
  - 機能要件に対するテスト
- 第三象限(左下): unit tests, component tests, system tests (automated)
  - 単体テスト、コンポーネントテスト、システムテスト
- 第四象限(右下): non-functional acceptance tests (ex. capacity, performance, security, etc...) (manual / automated)
  - 非機能要件に対するテスト

CIとテスト自動化が整理できたら、デプロイメントパイプライン(deployment pipeline)を作成する。(デプロイメントパイプラインは、CDにおける重要なパターン!)

- デプロイメントパイプラインパターンの各stepの流れ
  - 全てのcommitされた変更に対してビルドが実行され、packagingされ、ユニットテストなどの自動テストが実行され、数分の間に開発者にフィードバックを提供する。
  - 一連のテストに合格した後、より包括的な自動acceptanceテストが実行される。(pipelineの各stepが別れてるんだ...!)
  - 全ての自動テストに合格したパッケージは、usabilityテストや探索的テストができるtest環境にデプロイされる(手動テストのstep...!)
  - 最終的にOKと判断できればリリースされる。

以下は、簡単な直線状のデプロイメントパイプラインの例:

![](https://continuousdelivery.com/images/pipeline-sequence.png)

- デプロイメント・パイプラインでは、**すべての変更が実質的にリリース候補**(のpackage!)となる。
- デプロイメント・パイプラインのお仕事は、既知の問題をキャッチすること。
  - (これでcatchできない問題はincidentにつながるかもしれないが、その後の対応で既知の問題となり、次回以降はcatch可能になる...!:thinking:)
  - **もし既知の問題が検出されなければ、デプロイメントパイプラインを通過したパッケージをリリースしても全く問題ないと感じるべき**...!!
    - (うんうん、過度にビクビクする必要はなさそう。未知の問題はそもそもcatchできないので...!:thinking:)
    - デプロイメントパイプラインが成功しても、不安を感じてしまう場合、またはデプロイ後で不具合が発見された場合、テストの追加や更新など、パイプラインを改善する必要がある

デプロイメントパイプラインの導入に関して:

- まずはskeleton deployment pipeline (==スカスカのデプロイメントパイプライン??)を作成することから始める。
  - まずは最小限に、単一のユニットテスト、単一の受け入れテスト、探索的テスト環境を立ち上げる自動化デプロイメントスクリプトを作成し、それらを組み合わせる。
    - (曳光弾的な...!:thinking:)
  - そして、プロダクトの進化につれて、テストカバレッジを拡大し、デプロイメントパイプラインを拡張していく。

#### FAQ

継続的デリバリーとは、テスターを全員解雇すること??

- No!

すべてのテストを自動化すべき??

- No!

今すぐ手動テストをすべて中止し、自動化すべき??

- No!

誰が自動テストに責任を持つ??

- No!

# MLシステムと継続的デリバリーの話

参考: GCPさんのブログ [MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

- MLOpsは、MLシステム開発（Dev）とMLシステム運用（Ops）の一体化を目指すMLエンジニアリングの文化と実践。
-