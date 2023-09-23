## 0.1. link

- https://12factor.net/ja/

## 0.2. Twelve-Factor Appって何?

- Twelve-Factor Appは、クラウドネイティブなアプリケーションの開発手法に関する方法論である。アプリケーションの設計や運用におけるベストプラクティスを提唱している。
  - 以下、各要素:
  - 1. 宣言的なフォーマットを使用
  - 2. クラウドプラットフォームに適したデプロイ
- Twelve-Factorの方法論は、ど**のようなプログラミング言語で書かれたアプリケーションに**でも適用できる。また、**どのようなバックエンドサービス（データベース、メッセージキュー、メモリキャッシュなど）の組み合わせ**を使っていても適用できる。

## 0.3. 背景:

- Twelve-Factor appは、多種多様なSaaSアプリケーション開発現場での私たちの経験と観察をすべてまとめたもの。
  - 特に、以下の3点に注目している:
  - 1. アプリケーションが時間と共に有機的に成長する力学
  - 2. アプリケーションのコードベースに取り組む開発者間のコラボレーションの力学
  - 3. ソフトウェア腐敗によるコストの回避に注目している。

# 1. Codebase: バージョン管理されている1つのCodebaseと複数のDeploy

- Codebase=git等で管理されるコードリポジトリ。
- **CodebaseとApplicationの間には、常に1対1の関係**。
  - もし1つのApplicationに対して複数のCodebaseがある場合、それはApplicationではなく分散システム。分散システムの各ComponentがApplicationであり、個別にTwelve-Factorの理論を適用可能。
  - もしひとつのCodebaseに対して複数のApplicationを共有している場合、それはTwelve-Factorに違反している状態。
- **1つのCodebase、1つのApplicationに対して、Deployは複数存在する**。
  - Deploy = Applicationの実行中のInstance。
  - ex) production環境のInstanceやstaging環境のInstanceは、それぞれDeploy。
  - Codebaseは全てのDeployに対して同一。
  - ex) 開発者はstaging環境にまだデプロイされていないコミットを抱えているし、staging環境には本番環境にデプロイされていないコミットが含まれている。
  - しかし、これらのDeploy達はすべて同一のCodebaseを共有しているため、同一のApplicationの異なるデプロイである

# 2. Dependency: 依存関係を明示的に宣言し分離する

- 依存関係宣言(dependency declaration)と依存関係分離(dependency isolation)の話。
- ほとんどのプログラミング言語は、サポートライブラリを配布するための**パッケージ管理システム**を提供している。
  - パッケージ管理システムを使ったライブラリのインストール先は二種類:
  - システム全体("site packages"と呼ばれる)
  - 単一のApplicationを含むディレクトリのスコープ("vendoring"または"bundling")
- **Twelve-factor appでは、system-wide packages(=site packages? 上述したインストール先の前者??)の暗黙の依存関係を決して使用しない**。
  - 全ての依存関係を明示的に**宣言**する。(ex. Pythonではpip等を使う)
  - かつ、周囲のシステムから暗黙的な依存関係が"漏れる"事がないように、依存関係を**分離**する。(ex. Pythonではvirtualenv等を使う)
  - 宣言と分離の為のツールは何であれ、依存関係の宣言と分離は常にセットで適用される必要がある。片方のみではTwelve-Factorを満たせない。
- 明示的に依存関係を宣言したい理由(利点):
  - ->Applicationに新しい開発者がjoinした際のセットアップを単純化できる。(うんうん。requirements.txtで明示的に宣言されてた方がいいもんね:thinking:)
- 暗黙的なsystem-wide packagesに頼らない理由(利点):
  - 仮に依存しているsystem-wide packagesが、Applicationが将来にかけて実行され得るすべてのシステム環境に存在するかどうか、何の保証もない。
  - Applicationが対象のpackageに依存すべきならば、その依存を明示的にApplication内に組み込むべき。

# 3. config: configを環境変数に格納する

- (要はconfigration的な情報をハードコーディングするな、って話だろうか:thinking:)
- ApplicationのConfigは、**Deploy(staging, 本番、開発環境, etc.)の間で異なり得る唯一のもの**。
- configには以下の情報が含まれる:
  - データベースや他のバックエンドサービスへのResource handle(接続情報や識別子)
  - Amazon S3やTwitterなどの外部サービスへのcredential(認証情報)
  - Deploy毎に異なるホスト名など
- **Applicationはたまにconfigを定数としてコード内に格納するが、これはTwelve-Factorに違反**している。
  - **Twelve-FactorはConfigをコードから厳密に分離する事を求める**。
  - ConfigはDeploy毎に異なるが、コードはそうではない。
- 「Applicationが全てのConfigをコードの外部に正しく分離できているか否か」の簡単なテストは、**Codebaseを今すぐオープンソースとして公開できるか否か**。
- "Config"の定義において、**Application内部の設定は含まれない**点に注意!
  - 内部の設定とはDeploy間で変わらない設定であり、この場合はコードの内部に含めるべき。
- Configに対するもう一つのアプローチは、バージョン管理システムにcheckinされないconfigファイルを使う事:
  - ex.) Railsの`config/database.yml`
  - Codebase内の定数に含めるアプローチよりは大分マシ。(これはcheckinされているので...!)
  - ただ弱点もある:
    - configファイルが誤ってリポジトリにcheckinされやすい。
    - configファイルが異なる場所に異なるフォーマットで散乱し、全てのconfigを1つの場所で見たり管理しづらくなりがち
- Twelve-Factor AppはConfigを環境変数に格納する利点:
  - 環境変数は、Deploy毎に簡単に変更できる。
  - Configファイルと異なり、誤ってリポジトリにcheckinされにくい。
  - Configファイルと異なり、言語やOSに依存しない。(yamlとかjson等は、ほぼ言語やOSに依存しないConfigファイルと言っても良い気がする:thinking:)
- config管理のもう一つの側面はGrouping:
  - Applicationはconfigを名前付きのグループ(="環境", "environment")にまとめたりする。(ex. dev環境、test環境、prod環境, etc.)
  - だがこの方法は、スケールしない。
    - -> Deployが増えるにつれて、新しい環境名が必要になる。プロジェクトが拡大すると、開発者は自分用の環境を追加したりする。
    - -> 結果としてconfigが組み合わせ的に爆発し、ApplicationのDeployの管理が非常に不安定になる。

# 4. backing(バックエンド)サービス: バックエンドサービスをattachされたリソースとして扱う

- ここで"backing(バックエンド)サービス"は、Applicationが通常の動作の中でネットワーク越しに利用する全てのサービスの事を言う。
  - datastore(ex. MySQL), messaging/queueing system, 電子メールを送信する為のSMTPサービス, caching system(ex. Memcached)
- Twelve-Factor Appでは、ローカルサービスとサードパーティサービスを区別しない。
  - **Applicationにとってはどちらもattachされたリソースであり、configに格納されたURLや認証情報でアクセスする**。
    - ("attachされたリソース"という表現は、applicationとリソースが疎結合である、って意味っぽい...?:thinking:)
  - Twelve-Factorを満たすApplicationのDeployは、**Applicationのコードを修正する事なく、configの中のresource handleを切り替えるだけで**、ローカルサービスのMySQLデータベースを、サードパーティサービスのAmazon RDSに切り替える事ができるべき...!!(なるほど...!:thinking:)

# 5. Build, release, run: ビルド、リリース、実行の3つのステージを厳密に分離する

- Codebaseは(実際には"Codebaseでは"なのかな。一つのApplication、一つのCodebaseに対して、複数のDeployがあるはずだし:thinking:)、3つのstageを経て(たぶんprod環境の!)Deployへと変換される:
  - build stage:
    - code repositoryを"build"と呼ばれる実行可能な塊に変換する。
  - release stage:
    - build stageで生成されたbuildを受け取り、それをDeployの現在のconfigと結合する。
    - できあがる"release"には"build"と"config"の両方が含まれ、実行環境の中ですぐにでも実行できるように準備が整った状態。
  - run stage("runtime"とも呼ぶ):
    - 選択された"release"に対して、ApplicationのいくつかのProcessを起動する事で、Applicationを実行環境の中で走らせる。
- **Twelve-Factor Appでは、3つのstagesを厳密に分離する**!

# 6. Process: Applicationを1つもしくは複数のStatelessなProcessとして実行する

- "Process"=Applicationを実行する為の操作??:thinking:
  - コンピュータプログラムが実行される際における基本的な操作単位。
  - ex. コマンドラインから実行する`python app.py`(最もシンプルな例。実行の為に複数のProcessを持つApplicationもある。)
  - i.e. コンピュータ上で実行されるプログラムの実体であり、アプリケーションの動作を担当するらしい。
- **Twelve-Factor AppのProcessは、StatelessかつShare-nothingであるべき**。
  - "状態を持たない"かつ"共有するものがない"
  - i.e. Applicationの各実行は独立しており、1つの実行が終了しても次の実行には影響しない。
  - しかし、Applicationのusecaseによっては状態を保持したいケースもある。(ex. userのセッション情報, userやitemの属性情報, etc.)
  - ↑のような**persistしたい(i.e. 永続的に保持したい)データは、Applicationにではなく、データベース等の外部サービスに保存すべき**である...!
    - i.e. persistしたいデータをApplicationのメモリ空間やファイルシステムに保存するな。(短い単一のTransaction内でのキャッシュとしてならOK)
  - Applicationが状態を持たない事でScalabilityが向上し、より柔軟に運用できる...!
- 一部のウェブシステムは"sticky sessions"を利用しているが、これはTwelve-Factor Appの設計原則に反している。
  - sticky sessions: web applicationにおけるセッション管理の一種で、特定のユーザが同じサーバに送信されることを保証する管理方法。

# 7. Port binding: サービスはPort bindingを通して公開する

- "Port Binding"とは:
  - Applicationとの通信の為のgateway(=入り口)として機能する特定の番号(=port, ex. 80)に、Applicationを関連付ける事。
- Twelve-Factor Appでは、Application自身がportにbindし、リクエストを受け取る事を重要視してる。Application自身がHTTPサービスを提供する。
- Port bindingにより、一つのApplicationが他のApplicationのbackingサービスになる事ができる。
- この原則を満たさない例:
  - Applicationが特定のPortにbindする代わりに、固定のAPIエンドポイントのみを介してのみアクセス可能であり、外部からのリクエストを直接受け取らないケース。(セキュリティ的には良さそうだけど...!:thinking:)

# 8. Concurrency(並行性): Process ModelによってScale outする

- Twelve-Factor AppではProcessはshare-nothingなので、水平に分割可能!
  - より多くの同時実行を追加できる。
-

# 9. Disposability(廃棄しやすさ?): fast startup(高速な起動)と graceful shutdown(エレガントな段階的な?)によってrobust性を最大化する

- Twelve-Factor AppのProcess(=Applicationの動作)はDisposableである。(i.e. 即座に起動・終了できる!)
  - -> 迅速で柔軟なScaling、codeやconfigの高速なデプロイ、本番適用のrobust性!
- fast startup:
  - プロセスは起動時間を最小限に抑えるべき。
- graceful shutdown(エレガントな段階的な?):
- Twelve-Factor Appは予期せぬ、not gracefulな終了に対応できるように設計すべき。

# 10. Dev/prod parity(=一致性?): dev, staging, prod環境をできるだけ一致させた状態に保つ

- Twelve-Factor Appは、**Continuous Deployしやすいように開発環境と本番環境のギャップを小さく保つ**...!(逆に、伝統的なApplicationはこれらのギャップが大きい...!)
  - 時間のギャップを小さくすべき!:
    - 開発者が書いたコードは数時間後、さらには数分後にはデプロイされるべき。
  - 人材のギャップを小さくすべき!:
    - コードを書いた開発者はそのコードのデプロイに深く関わり、そのコードの本番環境での挙動をモニタリングするべき。
  - ツールのギャップを小さくすべき!:
    - できるだけツールを一致させるべき。
- backingサービスの違いは、僅かな非互換性が顕在化し、dev環境では正常に動作してテストを通過するコードが、prod環境でエラーを起こす事態を招き得る -> **この種のエラーはContinuous Deployを妨げる摩擦を生む**...!

# 11. Logs: ログをevent streamとして扱う

- Twelve-Factor Appは自分のログを直接管理せず、各プロセスは自身のイベントをstdoutに書き出すべき。

# 12. Admin processes: admin/management(=管理)タスクをone-off(=一回限りの)プロセスとして実行する

- 開発者はしばしば、データベースのマイグレーションやコンソールの実行など、アプリの管理やメンテナンス作業を行う必要がある。
- **Twelve-Factor Appは、REPL(Read-Eval-Print Loop, i.e. 対話型環境!)を提供し、一時的なスクリプトを実行することが容易な言語を採用すべき**!
  - 本番環境では、開発者は**ssh**やそのデプロイの実行環境で提供される他のリモートコマンド実行メカニズムを使う。
