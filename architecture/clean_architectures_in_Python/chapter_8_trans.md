## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-08/
https://www.thedigitalcatbooks.com/pycabook-chapter-08/

# Chapter 8 - Run a production-ready system 第8章 生産準備システムの稼動

Vilos Cohaagen said troops would be used to ensure full production.
ヴィロス・コーハーゲンは、フル生産を確保するために軍隊を投入すると述べた。

Total Recall, 1990
1990年『トータル・リコール

Now that we developed a repository that connects with PostgreSQL we can discuss how to properly set up the application to run a production-ready system.
PostgreSQLと接続するリポジトリを開発したので、本番稼働可能なシステムを実行するためにアプリケーションを適切にセットアップする方法について説明します。
This part is not strictly related to the clean architecture, but I think it's worth completing the example, showing how the system that we designed can end up being the core of a real web application.
この部分はクリーン・アーキテクチャとは厳密には関係ないが、私たちが設計したシステムが実際のウェブ・アプリケーションの中核となり得ることを示すために、この例を完成させる価値があると思う。

Clearly, the definition "production-ready" refers to many different configuration that ultimately depend on the load and the business requirements of the system.
明らかに、"production-ready "の定義は、最終的にはシステムの負荷とビジネス要件に依存する多くの異なる構成を指す。
As the goal is to show a complete example and not to cover real production requirements I will show a solution that uses real external systems like PostgreSQL and Nginx, without being too concerned about performances.
目標は完全な例を示すことであり、実際の生産要件をカバーすることではないので、パフォーマンスにあまりこだわらず、PostgreSQLやNginxのような実際の外部システムを使用するソリューションを示します。

## Build a web stack ウェブスタックの構築

Now that we successfully containerised the tests we might try to devise a production-ready setup of the whole application, running both a web server and a database in Docker containers.
さて、テストのコンテナ化に成功したので、Dockerコンテナでウェブサーバとデータベースの両方を実行する、アプリケーション全体の本番環境でのセットアップを考案してみよう。
Once again, I will follow the approach that I show in the series of posts I mentioned in one of the previous sections.
もう一度、前のセクションで紹介した一連の投稿で示したアプローチに従おう。

To run a production-ready infrastructure we need to put a WSGI server in front of the web framework and a Web server in front of it.
プロダクション・レディのインフラを動かすには、ウェブ・フレームワークの前にWSGIサーバーを置き、その前にウェブ・サーバーを置く必要がある。
We will also need to run a database container that we will initialise only once.
また、一度だけ初期化するデータベース・コンテナを実行する必要がある。

The steps towards a production-ready configuration are not complicated and the final setup won't be ultimately too different form what we already did for the tests.
本番用のコンフィギュレーションに向けたステップは複雑ではないし、最終的なセットアップも、すでにテスト用に行ったものと最終的に大きく変わることはないだろう。
We need to
そのためには

- Create a JSON configuration with environment variables suitable for production 本番環境に適した環境変数を含むJSONコンフィギュレーションを作成する。

- Create a suitable configuration for Docker Compose and configure the containers Docker Composeに適した設定を作成し、コンテナを設定する。

- Add commands to manage.py that allow us to control the processes プロセスをコントロールするコマンドを manage.py に追加する。

Let's create the file config/production.json, which is very similar to the one we created for the tests
config/production.jsonファイルを作成しよう。テスト用に作成したものとよく似ている。

Please note that now both FLASK_ENV and FLASK_CONFIG are set to production.
FLASK_ENVとFLASK_CONFIGの両方がproductionに設定されていることに注意してください。
Please remember that the first is an internal Flask variable with two possible fixed values (development and production), while the second one is an arbitrary name that has the final effect of loading a specific configuration object (ProductionConfig in this case).
1つ目は2つの固定値（developmentとproduction）を持つFlaskの内部変数で、2つ目は特定の設定オブジェクト（この場合はProductionConfig）をロードする最終的な効果を持つ任意の名前であることを覚えておいてください。
I also changed POSTGRES_PORT back to the default 5432 and APPLICATION_DB to application (an arbitrary name).
また、POSTGRES_PORTをデフォルトの5432に戻し、APPLICATION_DBをアプリケーション（任意の名前）に変更した。

Let's define which containers we want to run in our production environment, and how we want to connect them.
本番環境で稼働させたいコンテナと、その接続方法を定義しよう。
We need a production-ready database and I will use Postgres, as I already did during the tests.
本番で使えるデータベースが必要なので、テスト時にすでに使ったようにPostgresを使うつもりだ。
Then we need to wrap Flask with a production HTTP server, and for this job I will use gunicorn.
それから、Flaskを本番のHTTPサーバーでラップする必要がある。
Last, we need a Web Server to act as load balancer.
最後に、ロードバランサーとして機能するウェブサーバーが必要だ。

The file docker/production.yml will contain the Docker Compose configuration, according to the convention we defined in manage.py
docker/production.ymlファイルには、manage.pyで定義した規約に従って、Docker Composeの設定を記述します。

As you can see the Postgres configuration is not different from the one we used in the file testing.yml, but I added the option volumes (both in db and at the end of the file) that allows me to create a stable volume.
ご覧の通り、Postgresのコンフィギュレーションはtesting.ymlで使用したものと変わりませんが、安定したボリュームを作成するためのオプションvolumes（db内とファイル末尾の両方）を追加しました。
If you don't do it, the database will be destroyed once you shut down the container.
そうしないと、コンテナをシャットダウンした時点でデータベースが破壊されてしまう。

The container web runs the Flask application through gunicorn.
コンテナ・ウェブは、gunicornを通してFlaskアプリケーションを実行する。
The environment variables come once again from the JSON configuration, and we need to define them because the application needs to know how to connect with the database and how to run the web framework.
環境変数は再びJSONコンフィギュレーションから来たもので、アプリケーションはデータベースとの接続方法とウェブ・フレームワークの実行方法を知る必要があるため、定義する必要がある。
The command gunicorn -w 4 -b 0.0.0.0 wsgi:app loads the WSGI application we created in wsgi.py and runs it in 4 concurrent processes.
gunicorn -w 4 -b 0.0.0.0 wsgi:app コマンドは wsgi.py で作成した WSGI アプリケーションをロードし、4 つの同時プロセスで実行します。
This container is created using docker/web/Dockerfile.production which I still have to define.
このコンテナはdocker/web/Dockerfile.productionを使って作成される。

The last container is nginx, which we will use as it is directly from the Docker Hub.
最後のコンテナはnginxで、Docker Hubから直接入手できるのでこれを使う。
The container runs Nginx with the configuration stored in /etc/nginx/nginx.conf, which is the file we overwrite with the local one ./nginx/nginx.conf.
コンテナは/etc/nginx/nginx.confに保存されたコンフィギュレーションでNginxを実行します。このファイルはローカルの./nginx/nginx.confで上書きします。
Please note that I configured it to use port 8080 instead of the standard port 80 for HTTP to avoid clashing with other software that you might be running on your computer.
お使いのコンピューターで実行中の他のソフトウェアとの衝突を避けるため、HTTPの標準ポート80ではなく8080を使用するように設定したことにご注意ください。

The Dockerfile for the web application is the following
ウェブ・アプリケーションのDockerfileは以下の通り。

This is a very simple container that uses the standard python:3 image, where I added the production requirements contained in requirements/prod.txt.
これは標準のpython:3イメージを使った非常にシンプルなコンテナで、requirements/prod.txtに含まれるプロダクション要件を追加した。
To make the Docker container work we need to add gunicorn to this last file
Dockerコンテナを動作させるには、この最後のファイルにgunicornを追加する必要がある。

The configuration for Nginx is
Nginxの設定は

As for the rest of the project, this configuration is very basic and lacks some important parts that are mandatory in a real production environment, such as HTTPS.
プロジェクトの他の部分に関しては、この構成は非常に基本的なもので、HTTPSのような実際の本番環境で必須となる重要な部分が欠けている。
In its essence, though, it is however not too different from the configuration of a production-ready Nginx container.
しかし、その本質は、本番環境用のNginxコンテナの構成とあまり変わらない。

As we will use Docker Compose, the script manage.py needs a simple change, which is a command that wraps docker-compose itself.
Docker Composeを使うので、manage.pyスクリプトには簡単な変更が必要です。それはdocker-compose自身をラップするコマンドです。
We need the script to just initialise environment variables according to the content of the JSON configuration file and then run Docker Compose.
JSON設定ファイルの内容に従って環境変数を初期化し、Docker Composeを実行するだけのスクリプトが必要です。
As we already have the function docker_compose_cmdline the job is pretty simple
すでに関数 docker_compose_cmdline があるので、作業はとても簡単です。

As you can see I forced the variable APPLICATION_CONFIG to be production if not specified.
ご覧のように、APPLICATION_CONFIG変数が指定されていなければ、強制的にproductionになるようにした。
Usually, my default configuration is the development one, but in this simple case I haven't defined one, so this will do for now.
通常、私のデフォルトのコンフィギュレーションは開発用のものだが、この単純なケースでは定義していない。

The new command is compose, that leverages Click's argument decorator to collect subcommands and attach them to the Docker Compose command line.
新しいコマンドはcomposeで、Clickの引数デコレーターを活用してサブコマンドを集め、Docker Composeのコマンドラインにアタッチする。
I also use the signal library, which I added to the imports, to control keyboard interruptions.
キーボードの中断をコントロールするために、インポートに追加したシグナル・ライブラリも使っている。

When all this changes are in place we can test the application Dockerfile building the container.
すべての変更が完了したら、アプリケーションのDockerfileをテストしてコンテナを構築することができる。

This command runs the Click command compose that first reads environment variables from the file config/production.json, and then runs docker-compose passing it the subcommand build web.
このコマンドは、まずconfig/production.jsonファイルから環境変数を読み込み、build webサブコマンドを渡してdocker-composeを実行するClickコマンドcomposeを実行する。

You output should be the following (with different image IDs)
出力は以下のようになるはずだ（画像IDは異なる）。

If this is successful you can run Docker Compose
これが成功したら、Docker Composeを実行できます。

and the output of docker ps should show three containers running
docker psの出力には、以下の3つのコンテナが稼働していることが示されている。

Note that I removed several columns to make the output readable.
出力を読みやすくするために、いくつかの列を削除したことに注意してほしい。

At this point we can open http://localhost:8080/rooms with our browser and see the result of the HTTP request received by Nginx, passed to gunicorn, and processed by Flask using the use case room_list_use_case.
この時点で、ブラウザで http://localhost:8080/rooms を開き、Nginxが受け取ったHTTPリクエストの結果を見ることができる。gunicornに渡され、room_list_use_caseというユースケースを使ってFlaskが処理する。

The application is not actually using the database yet, as the Flask endpoint room_list in application/rest/room.py initialises the class MemRepo and loads it with some static values, which are the ones we see in our browser.
application/rest/room.pyのFlaskエンドポイントroom_listはMemRepoクラスを初期化し、いくつかの静的な値をロードします。

## Connect to a production-ready database 本番環境にあるデータベースに接続する

Before we start changing the code of the application remember to tear down the system running
アプリケーションのコードを変更し始める前に、以下を実行しているシステムを解体することを忘れないでほしい。

Thanks to the common interface between repositories, moving from the memory-based MemRepo to PostgresRepo is very simple.
リポジトリ間の共通インターフェースのおかげで、メモリベースのMemRepoからPostgresRepoへの移行は非常に簡単です。
Clearly, as the external database will not contain any data initially, the response of the use case will be empty.
明らかに、外部データベースには初期状態ではデータが含まれていないため、ユースケースのレスポンスは空になる。

First of all, let's move the application to the Postgres repository.
まずはアプリケーションをPostgresのリポジトリに移動しよう。
The new version of the endpoint is
エンドポイントの新しいバージョンは

As you can see the main change is that repo = MemRepo(rooms) becomes repo = PostgresRepo(postgres_configuration).
主な変更点は、repo = MemRepo(rooms)がrepo = PostgresRepo(postgres_configuration)になったことです。
Such a simple change is made possible by the clean architecture and its strict layered approach.
このようなシンプルな変更は、クリーンなアーキテクチャと厳格なレイヤーアプローチによって可能になった。
The only other notable change is that we replaced the initial data for the memory-based repository with a dictionary containing connection data, which comes from the environment variables set by the management script.
その他の注目すべき変更点は、メモリベースのリポジトリの初期データを、管理スクリプトによって設定された環境変数に由来する接続データを含む辞書に置き換えたことだけである。

This is enough to make the application connect to the Postgres database that we are running in a container, but as I mentioned we also need to initialise the database.
コンテナで実行しているPostgresデータベースにアプリケーションを接続させるにはこれで十分だが、先ほど述べたように、データベースを初期化する必要もある。
The bare minimum that we need is an empty database with the correct name.
最低限必要なのは、正しい名前の空のデータベースだ。
Remember that in this particular setup we use for the application a different database (APPLICATION_DB) from the one that the Postgres container creates automatically at startup (POSTGRES_DB).
この特定のセットアップでは、Postgresコンテナが起動時に自動的に作成するデータベース（POSTGRES_DB）とは別のデータベース（APPLICATION_DB）をアプリケーションに使用していることを覚えておいてください。
I added a specific command to the management script to perform this task
このタスクを実行するために、管理スクリプトに特定のコマンドを追加した。

Now spin up your containers
コンテナをスピンアップする

and run the new command that we created
作成した新しいコマンドを実行する

Mind the change between the name of the function init_postgres and the name of the command init-postgres.
init_postgres関数の名前とinit-postgresコマンドの名前の変更に注意してください。
You only need to run this command once, but repeated executions will not affect the database.
このコマンドは一度だけ実行する必要があるが、繰り返し実行してもデータベースには影響しない。

We can check what this command did connecting to the database.
このコマンドがデータベースに接続して何をしたかを確認することができる。
We can do it executing psql in the database container
データベース・コンテナでpsqlを実行すればよい。

Please note that we need to specify the user -U postgres.
ユーザー -U postgres を指定する必要があることに注意してください。
That is the user that we created through the variable POSTGRES_USER in config/production.json.
これは、config/production.jsonの変数POSTGRES_USERで作成したユーザーです。
Once logged in, we can use the command \l to see the available databases
ログインしたら、" \l" コマンドで利用可能なデータベースを見ることができる。

Please note that the two databases template0 and template1 are system databases created by Postgres (see the documentation), postgres is the default database created by the Docker container (the name is postgres by default, but in this case it comes from the environment variable POSTGRES_DB in config/production.json) and application is the database created by ./manage.py init-postgres (from APPLICATION_DB).
template0とtemplate1の2つのデータベースはPostgresによって作成されたシステムデータベース（ドキュメントを参照）、postgresはDockerコンテナによって作成されたデフォルトのデータベース（名前はデフォルトでpostgresですが、この場合はconfig/production.jsonの環境変数POSTGRES_DBに由来します）、applicationは./manage.py init-postgresによって作成されたデータベース（APPLICATION_DBに由来します）であることに注意してください。

We can connect to a database with the command \c
データベースに接続するには、以下のコマンドを実行する。

Please note that the prompt changes with the name of the current database.
プロンプトは現在のデータベース名で変わることに注意してください。
Finally, we can list the available tables with \dt
最後に、利用可能なテーブルを一覧表示します。

As you can see there are no tables yet.
ご覧の通り、まだテーブルはない。
This is no surprise as we didn't do anything to make Postres aware of the models that we created.
私たちが作ったモデルをポストレスに知らせるために何もしなかったのだから、これは当然のことだ。
Please remember that everything we are doing here is done in an external system and it is not directly connected with entities.
私たちがここで行っていることはすべて外部のシステムで行われており、実体と直接関係するものではないことを覚えておいてほしい。

As you remember, we mapped entities to storage objects, and since we are using Postgres we leveraged SQLAlchemy classes, so now we need to create the database tables that correspond to them.
覚えているように、エンティティをストレージオブジェクトにマッピングし、Postgres を使っているので SQLAlchemy のクラスを利用しました。

## Migrations 移住

We need a way to create the tables that correspond to the objects that we defined in rentomatic/repository/postgres_objects.py.
rentomatic/repository/postgres_objects.pyで定義したオブジェクトに対応するテーブルを作成する方法が必要です。
The best strategy, when we use an ORM like SQLAlchemy, is to create and run migrations, and for this we can use Alembic.
SQLAlchemy のような ORM を使う場合の最良の戦略は、マイグレーションを作って実行することです。

If you are still connected with psql please exit with \q, then edit requirements/prod.txt and add alembic
...

As usual, remember to run pip install -r requirements/dev.txt to update the virtual environment.
いつものように、pip install -r requirements/dev.txtを実行して仮想環境を更新するのを忘れないこと。

Alembic is capable of connecting to the database and run Python scripts (called "migrations") to alter the tables according to the SQLAlchemy models.
Alembic はデータベースに接続し、SQLAlchemy のモデルに従ってテーブルを変更する Python スクリプト（"migrations "と呼ばれます）を実行することができます。
To do this, however, we need to give Alembic access to the database providing username, password, hostname, and the database name.
ただし、そのためには、ユーザー名、パスワード、ホスト名、データベース名を指定して、Alembicにデータベースへのアクセス権を与える必要がある。
We also need to give Alembic access to the Python classes that represent the models.
また、モデルを表すPythonクラスにAlembicがアクセスできるようにする必要がある。

First of all let's initialise Alembic.
まずはAlembicを初期化しよう。
In the project's main directory (where manage.py is stored) run
プロジェクトのメインディレクトリ(manage.pyが格納されている)で以下を実行します。

which creates a directory called migrations that contains Alembic's configuration files, together with the migrations that will be created in migrations/versions.
これは、migrations/versionsに作成されるmigrationsとともに、Alembicの設定ファイルを含むmigrationsというディレクトリを作成します。
it will also create the file alembic.ini which contains the configuration values.
また、設定値を含むファイルalembic.iniも作成される。
The name migrations is completely arbitrary, so feel free to use a different one if you prefer.
マイグレーションという名前は完全に任意である。

The specific file we need to adjust to make Alembic aware of our models and our database is migrations/env.py.
Alembicがモデルやデータベースを認識できるようにするために調整するファイルは migrations/env.py です。
Add the highlighted lines
ハイライトされた行を追加する

Through config.set_section_option we are adding relevant configuration values to the main Alembic INI file section (config.config_ini_section), extracting them from the environment variables.
config.set_section_optionを通して、環境変数から関連する設定値を抽出して、メインのAlembic INIファイル・セクション（config.config_ini_section）に追加します。
We are also importing the file that contains the SQLAlchemy objects.
SQLAlchemy オブジェクトを含むファイルもインポートします。
You can find documentation on this procedure at https://alembic.sqlalchemy.org/en/latest/api/config.html.
この手順に関する文書は、https://alembic.sqlalchemy.org/en/latest/api/config.html。

Once this is done we need to change the INI file to use the new variables
これが完了したら、新しい変数を使用するようにINIファイルを変更する必要がある。

The syntax %(VARNAME)s is the basic variable interpolation used by ConfigParser (see the documentation).
構文%(VARNAME)sはConfigParserが使用する基本的な変数補間です（ドキュメントを参照）。

At this point we can run Alembic to migrate our database.
この時点で、Alembicを実行してデータベースを移行することができる。
In many cases, you can rely on Alembic's autogeneration functionality to generate the migrations, and this is what we can do to create the initial models.
多くの場合、Alembicの自動生成機能を使ってマイグレーションを生成することができます。
The Alembic command is revision with the --autogenerate flag, but we need to pass the environment variables on the command line.
Alembicコマンドは--autogenerateフラグで修正されるが、コマンドラインで環境変数を渡す必要がある。
This is clearly a job for migrate.py but let's first run it to see what happens to the database.
これは明らかにmigrate.pyの仕事ですが、まずこれを実行してデータベースに何が起こるか見てみましょう。
Later we will create a better setup to avoid passing variables manually
後ほど、手動で変数を渡すのを避けるために、より良いセットアップを作成します。

This will generate the file migrations/versions/4d4c19952a36_initial.py.
これは migrations/versions/4d4c19952a36_initial.py を生成します。
Pay attention that the initial hash will be different for you.
最初のハッシュはあなたによって異なることに注意してください。
If you want you can open that file and see how Alembic generates the table and creates the columns.
必要であれば、そのファイルを開いて、Alembicがどのようにテーブルを生成し、カラムを作成するかを見ることができます。

So far we created the migration but we still need to apply it to the database.
ここまででマイグレーションを作成したが、まだそれをデータベースに適用する必要がある。
Make sure you are running the Docker containers (run ./manage.py compose up -d otherwise) as Alembic is going to connect to the database, and run
Alembicがデータベースに接続するため、Dockerコンテナを実行していることを確認してください（./manage.py compose up -dを実行します）。

At this point we can connect to the database and check the existing tables
この時点でデータベースに接続し、既存のテーブルをチェックすることができる。

Please note that I used the option -d of psql to connect directly to the database application.
データベース・アプリケーションに直接接続するために、psqlのオプション-dを使ったことに注意してほしい。
As you can see, now we have two tables.
ご覧のように、これで2つのテーブルができた。
The first, alembic_version is a simple one that Alembic uses to keep track of the state of the db, while room is the one that will contain our Room entities.
最初のalembic_versionは、Alembicがデータベースの状態を管理するために使うシンプルなもので、roomはRoomエンティティを格納するものだ。

We can double-check the Alembic version
Alembicのバージョンをダブルチェックすることができる。

As I mentioned before, the hash given to the migration will be different in your case, but that value that you see in this table should be consistent with the name of the migration script.
前にも述べたように、マイグレーションに与えられるハッシュはあなたのケースでは異なるだろうが、このテーブルに表示される値はマイグレーションスクリプトの名前と一致しているはずだ。

We can also see the structure of the table room
また、テーブルルームの構造も見ることができる。

Clearly, there are still no rows contained in that table
明らかに、そのテーブルにはまだ行がありません。

And indeed, if you open http://localhost:8080/rooms with your browser you will see a successful response, but no data.
そして実際に、ブラウザでhttp://localhost:8080/rooms を開くと、成功した応答が表示されるが、データは表示されない。

To see some data we need to write something into the database.
データを見るためには、データベースに何かを書き込む必要がある。
This is normally done through a form in the web application and a specific endpoint, but for the sake of simplicity in this case we can just add data manually to the database.
これは通常、ウェブ・アプリケーションのフォームと特定のエンドポイントを通して行われるが、今回は簡略化のため、データベースに手動でデータを追加すればよい。

You can verify that the table contains the new room with a SELECT
テーブルが新しい部屋を含んでいることは、SELECT

and open or refresh http://localhost:8080/rooms with the browser to see the value returned by our use case.
を開き、ブラウザでhttp://localhost:8080/rooms を開くか更新して、ユースケースから返された値を確認する。

This chapter concludes the overview of the clean architecture example.
本章で、クリーン・アーキテクチャ例の概要を終える。
Starting from scratch, we created domain models, serializers, use cases, an in-memory storage system, a command-line interface and an HTTP endpoint.
ゼロから始めて、ドメインモデル、シリアライザー、ユースケース、インメモリーストレージシステム、コマンドラインインターフェース、HTTPエンドポイントを作成した。
We then improved the whole system with a very generic request/response management code, that provides robust support for errors.
そして、システム全体を、非常に汎用的なリクエスト／レスポンス管理コードで改良した。
Last, we implemented two new storage systems, using both a relational and a NoSQL database.
最後に、リレーショナル・データベースとNoSQLデータベースの両方を使用して、2つの新しいストレージ・システムを導入した。

This is by no means a little achievement.
これは決して小さな成果ではない。
Our architecture covers a very small use case, but is robust and fully tested.
私たちのアーキテクチャは、非常に小さなユースケースをカバーしていますが、堅牢で完全にテストされています。
Whatever error we might find in the way we dealt with data, databases, requests, and so on, can be isolated and tamed much faster than in a system which doesn't have tests.
データ、データベース、リクエストなどの扱い方にどのようなエラーがあったとしても、テストのないシステムよりもずっと早く、エラーを分離し、手なずけることができる。
Moreover, the decoupling philosophy not only allows us to provide support for multiple storage systems, but also to quickly implement new access protocols, or new serialisations for our objects.
さらに、デカップリング哲学は、複数のストレージ・システムのサポートを可能にするだけでなく、新しいアクセス・プロトコルやオブジェクトの新しいシリアライゼーションを素早く実装することも可能にする。