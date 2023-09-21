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

-
