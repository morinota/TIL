## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-06/
https://www.thedigitalcatbooks.com/pycabook-chapter-06/

# Chapter 6 - Integration with a real external system - Postgres 第6章 実際の外部システムとの統合 - Postgres

Ooooh, I'm very sorry Hans.
ハンス、申し訳ない。
I didn't get that memo.
私はそのメモを受け取っていない。

Maybe you should've put it on the bulletin board.
掲示板に書いた方がよかったんじゃない？

Die Hard, 1988
ダイ・ハード, 1988

The basic in-memory repository I implemented for the project is enough to show the concept of the repository layer abstraction.
私がプロジェクト用に実装した基本的なインメモリーリポジトリは、**repository層の抽象化(外部システムのDBのInterface的な??)の概念**を示すのに十分である.
It is not enough to run a production system, though, so we need to implement a connection with a real storage like a database.
しかし、本番システムを動かすにはこれだけでは不十分なので、**データベースのような実際のストレージとの接続を実装する必要がある**。
Whenever we use an external system and we want to test the interface we can use mocks, but at a certain point we need to ensure that the two systems actually work together, and this is when we need to start creating integration tests.
しかし、ある時点で、2つのシステムが実際に一緒に動作することを確認する必要がある。

In this chapter I will show how to set up and run integration tests between our application and a real database.
この章では、アプリケーションと実際のデータベースとの統合テストをセットアップして実行する方法を紹介する.
At the end of the chapter I will have a repository that allows the application to interface with PostgreSQL, and a battery of tests that run using a real database instance running in Docker.
この章の終わりには、**アプリケーションがPostgreSQLとinterfaceする(=接する?)ための Repositoryクラス と**、Dockerで動作する実際のデータベースインスタンスを使って実行する一連のテスト(=共有依存であるDBを使う統合テスト?)を用意する予定です。

This chapter will show you one of the biggest advantages of a clean architecture, namely the simplicity with which you can replace existing components with others, possibly based on a completely different technology.
この章では、**クリーン・アーキテクチャの最大の利点のひとつ**である、**既存のcomponentを、場合によってはまったく異なるテクノロジーをベースにした他のcomponentに置き換えることができるシンプルさ**について紹介する.

## Decoupling with interfaces インターフェイスによるデカップリング

The clean architecture we devised in the previous chapters defines a use case that receives a repository instance as an argument and uses its list method to retrieve the contained entries.
前の章で考案したクリーンなアーキテクチャでは、Repositoryインスタンスを引数として受け取り、そのリストメソッドを使って含まれるエントリーを取得するusecaseを定義しています。
This allows the use case to form a very loose coupling with the repository, being connected only through the API exposed by the object and not to the real implementation.
これにより、ユースケースはリポジトリと非常に緩い結合を形成することができ、オブジェクトによって公開されたAPIを通じてのみ接続され、実際の実装には接続されない.
In other words, the use cases are polymorphic with respect to the method list.
言い換えれば、usecaseは`list`methodに関して **polymorphic(多相的. 同じInterfaceに基づく具象クラスを同じ様に扱える事...!)**である。

This is very important and it is the core of the clean architecture design.
これは非常に重要なことで、クリーン・アーキテクチャ・デザインの核となるものだ。
Being connected through an API, the use case and the repository can be replaced by different implementations at any time, given that the new implementation provides the requested interface.
APIを介して接続されているため、usecase と Repository は、新しい実装が要求されたインターフェースを提供する限り、いつでも異なる実装に置き換えることができる。

It is worth noting, for example, that the initialisation of the object is not part of the API that the use cases are using since the repository is initialised in the main script and not in each use case.
例えば、**リポジトリはメインスクリプトで初期化され、各usecase内では初期化されない**ため、オブジェクトの初期化はユースケースが使用しているAPIの一部ではないことは注目に値する。
The method **init**, thus, doesn't need to be the same among the repository implementations, which gives us a great deal of flexibility, as different storage systems may need different initialisation values.
このため、`__init__`メソッドは、リポジトリの実装間(i.e. 具象クラス間)で同じである必要はありません。

The simple repository we implemented in one of the previous chapters is
前の章で実装したシンプルなリポジトリは次のとおりだ。

```python
from rentomatic.domain.room import Room


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self, filters=None):

        result = [Room.from_dict(i) for i in self.data]

        if filters is None:
            return result

        if "code__eq" in filters:
            result = [r for r in result if r.code == filters["code__eq"]]

        if "price__eq" in filters:
            result = [
                r for r in result if r.price == int(filters["price__eq"])
            ]

        if "price__lt" in filters:
            result = [
                r for r in result if r.price < int(filters["price__lt"])
            ]

        if "price__gt" in filters:
            result = [
                r for r in result if r.price > int(filters["price__gt"])
            ]

        return result
```

whose interface is made of two parts: the initialisation and the method list.
そのインターフェイスは、初期化とメソッドリストの2つの部分から構成されている。
The method **init** accepts values because this specific object doesn't act as long-term storage, so we are forced to pass some data every time we instantiate the class.
メソッド**init**は値を受け付けるが、これはこの特定のオブジェクトが長期記憶として機能しないからで、クラスをインスタンス化するたびに何らかのデータを渡さざるを得ない。

A repository based on a proper database will not need to be filled with data when initialised, its main job being that of storing data between sessions, but will nevertheless need to be initialised at least with the database address and access credentials.
適切なデータベースをベースにしたリポジトリは、初期化時にデータで満たされる必要はなく、主な仕事はセッション間のデータの保存ですが、それでも少なくともデータベースのアドレスとアクセス認証情報で初期化される必要があります。

Furthermore, we have to deal with a proper external system, so we have to devise a strategy to test it, as this might require a running database engine in the background.
さらに、適切な外部システムを扱わなければならないので、バックグラウンドでデータベース・エンジンを動かす必要があるかもしれないので、それをテストする戦略を考えなければならない。
Remember that we are creating a specific implementation of a repository, so everything will be tailored to the actual database system that we will choose.
私たちはリポジトリの特定の実装を作成しているので、すべては私たちが選択する実際のデータベースシステムに合わせて調整されることを覚えておいてください。

## A repository based on PostgreSQL PostgreSQLベースのリポジトリ

Let's start with a repository based on a popular SQL database, PostgreSQL.
一般的なSQLデータベースである**PostgreSQLをベースにしたRepositoryクラス**から始めましょう。
It can be accessed from Python in many ways, but the best one is probably through the SQLAlchemy interface.
**Python からはいろいろな方法でアクセスできますが、一番よいのは SQLAlchemy インタフェースでしょう.**(bestとは大きく出たな...!)
SQLAlchemy is an ORM, a package that maps objects (as in object-oriented) to a relational database.
**SQLAlchemyはORMであり、(オブジェクト指向のように)オブジェクトをリレーショナルデータベースにマッピングするパッケージ**です。
ORMs can normally be found in web frameworks like Django or in standalone packages like the one we are considering.
ORMは通常、DjangoのようなWebフレームワークや、私たちが検討しているようなスタンドアロンパッケージで見つけることができます。

The important thing about ORMs is that they are very good examples of something you shouldn't try to mock.
ORMについて重要なことは、**モックを試みてはいけない**ものの非常に良い例だということだ。
Properly mocking the SQLAlchemy structures that are used when querying the DB results in very complex code that is difficult to write and almost impossible to maintain, as every single change in the queries results in a series of mocks that have to be written again[1].
DBに問い合わせるときに使われるSQLAlchemyの構造を適切にモックすると、非常に複雑なコードになり、書くのが難しく、保守もほとんど不可能になります。

We need therefore to set up an integration test.
したがって、統合テストを設定する必要がある.
The idea is to create the DB, set up the connection with SQLAlchemy, test the condition we need to check, and destroy the database.
アイデアは、DB を作成し、SQLAlchemy で接続をセットアップし、チェックする必要のある 条件をテストし、データベースを破棄することです。
Since the action of creating and destroying the DB can be expensive in terms of time, we might want to do it just at the beginning and at the end of the whole test suite, but even with this change, the tests will be slow.
DBを作成したり破棄したりする動作は時間的に高くつく可能性があるので、テスト・スイート全体の最初と最後だけに行いたいかもしれないが、この変更でもテストは遅くなる。
This is why we will also need to use labels to avoid running them every time we run the suite.
このため、スイートを実行するたびにラベル(??)が実行されるのを避けるために、ラベルも使用する必要がある。
Let's face this complex task one step at a time.
この複雑な仕事に一歩ずつ向き合っていこう。

## Label integration tests¶ ラベル統合テスト

The first thing we need to do is to label integration tests, exclude them by default and create a way to run them.
最初にやるべきことは、**統合テストにラベルを付け(=単体テストと区別する為??)**、デフォルトで除外し、実行する方法を作ることだ。
Since pytest supports labels, called marks, we can use this feature to add a global mark to a whole module.
pytestは**マークと呼ばれるラベル**をサポートしているので、この機能を使ってモジュール全体にグローバルマークを追加することができます.
Create the file tests/repository/postgres/test_postgresrepo.py and put in it this code
tests/repository/postgres/test_postgresrepo.pyファイルを作成し、次のコードを記述します。

```python
import pytest

pytestmark = pytest.mark.integration


def test_dummy():
    pass
```

The module attribute pytestmark labels every test in the module with the tag integration.
モジュール属性の pytestmark は、モジュール内のすべてのテストに integration というタグを付けます。
To verify that this works I added a test_dummy test function which always passes.
これが機能することを確認するために、常にパスするtest_dummyテスト関数を追加した。

The marker should be registered in pytest.ini
マーカーはpytest.iniに登録する必要があります。

```
[pytest]
minversion = 2.0
norecursedirs = .git .tox requirements*
python_files = test*.py
markers =
        integration: integration tests
```

You can now run pytest -svv -m integration to ask pytest to run only the tests marked with that label.
`pytest -svv -m integration`を実行すると、**そのラベルが付いたテストだけを実行するようにpytestに指示できます**。
The option -m supports a rich syntax that you can learn by reading the documentation.
mオプションは豊富なシンタックスをサポートしており、[ドキュメント](https://docs.pytest.org/en/latest/example/markers.html)を読めば学ぶことができる.

```
$ pytest -svv -m integration
========================= test session starts ===========================
platform linux -- Python XXXX, pytest-XXXX, py-XXXX, pluggy-XXXX --
cabook/venv3/bin/python3
cachedir: .cache
rootdir: cabook/code/calc, inifile: pytest.ini
plugins: cov-XXXX
collected 36 items / 35 deselected / 1 selected

tests/repository/postgres/test_postgresrepo.py::test_dummy PASSED

=================== 1 passed, 35 deselected in 0.20s ====================
```

While this is enough to run integration tests selectively, it is not enough to skip them by default.
統合テストを選択的に実行するにはこれで十分だが、デフォルトでスキップするには不十分だ。(`pytest`コマンドで単体テストだけ実行したいってことか.)
To do this, we can alter the pytest setup to label all those tests as skipped, but this will give us no means to run them.
これを行うには、pytestのセットアップを変更して、これらのテストをすべてskippedとラベル付けすることができますが、これではテストを実行する手段がありません.
The standard way to implement this is to define a new command-line option and to process each marked test according to the value of this option.
これを実装する標準的な方法は、新しいコマンドラインオプションを定義し、このオプションの値に従って各マーク付きテストを処理することである。

To do it open the file tests/conftest.py that we already created and add the following code
これを行うには、既に作成した tests/conftest.py ファイルを開き、以下のコードを追加します。

```python
def pytest_addoption(parser):
    parser.addoption(
        "--integration", action="store_true", help="run integration tests"
    )


def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getvalue(
        "integration"
    ):
        pytest.skip("need --integration option to run")
```

The first function is a hook into the pytest CLI parser that adds the option --integration.
最初の関数は、--integrationオプションを追加するpytest CLIパーサへのフックです。
When this option is specified on the command line the pytest setup will contain the key integration with value True.
このオプションがコマンドラインで指定された場合、pytestセットアップには値Trueのintegrationキーが含まれます。

The second function is a hook into the pytest setup of every single test.
2番目の関数は、すべてのテストのpytestセットアップにフックします。
The variable item contains the test itself (actually a \_pytest.python.Function object), which in turn contains two useful pieces of information.
変数itemはテストそのもの（実際には`_pytest.python.Function`オブジェクト）を含み、その中に2つの有用な情報が含まれています。
The first is the attribute item.keywords, that contains the test marks, alongside many other interesting things like the name of the test, the file, the module, and also information about the patches that happen inside the test.
1つ目はitem.keywords属性で、テストのマークと、テスト名、ファイル名、モジュール名、テスト内で発生するパッチに関する情報など、多くの興味深い情報が含まれている。
The second is the attribute item.config that contains the parsed pytest command line.
2つ目は、解析されたpytestコマンドラインを含むitem.config属性です。

So, if the test is marked with integration ('integration' in item.keywords) and the option --integration is not present (not item.config.getvalue("integration")) the test is skipped.
そのため、**テストにintegration（item.keywordsの'integration'）ラベルが指定されていて、--integrationオプションが指定されていない（item.config.getvalue("integration")ではない）場合、テストはスキップされます。**

This is the output with --integration
これは--integrationの出力である。

```
$ pytest -svv --integration
========================= test session starts ===========================
platform linux -- Python XXXX, pytest-XXXX, py-XXXX, pluggy-XXXX --
cabook/venv3/bin/python3
cachedir: .cache
rootdir: cabook/code/calc, inifile: pytest.ini
plugins: cov-XXXX
collected 36 items

...
tests/repository/postgres/test_postgresrepo.py::test_dummy PASSED
...

========================= 36 passed in 0.26s ============================
```

and this is the output without the custom option
そしてこれがカスタムオプションなしの出力です。

```
$ pytest -svv
========================= test session starts ===========================
platform linux -- Python XXXX, pytest-XXXX, py-XXXX, pluggy-XXXX --
cabook/venv3/bin/python3
cachedir: .cache
rootdir: cabook/code/calc, inifile: pytest.ini
plugins: cov-XXXX
collected 36 items

...
tests/repository/postgres/test_postgresrepo.py::test_dummy SKIPPED
...

=================== 35 passed, 1 skipped in 0.27s =======================
```

## Create SQLAlchemy classes SQLAlchemy クラスの作成

Creating and populating the test database with initial data will be part of the test suite, but we need to define somewhere the tables that will be contained in the database.
テスト用データベースの作成と初期データの投入はテスト・スイートの一部となるが、**データベースに含まれるテーブルをどこかで定義する必要がある**。
This is where SQLAlchemy's ORM comes into play, as we will define those tables in terms of Python objects.
ここで SQLAlchemy の ORM が活躍します。テーブルを Python オブジェクトで定義します。

Add the packages SQLAlchemy and psycopg2 to the requirements file prod.txt
SQLAlchemy と psycopg2 のパッケージを prod.txt に追加してください。

```
Flask
SQLAlchemy
psycopg2
```

and update the installed packages with
でインストールされたパッケージを更新する。

```
$ pip install -r requirements/dev.txt
```

Create the file rentomatic/repository/postgres_objects.py with the following content
以下の内容で rentomatic/repository/postgres_objects.py ファイルを作成します。

```
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)

    code = Column(String(36), nullable=False)
    size = Column(Integer)
    price = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
```

Let's comment it section by section
セクションごとにコメントしよう

```python
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

We need to import many things from the SQLAlchemy package to set up the database and to create the table.
データベースをセットアップし、テーブルを作成するために、SQLAlchemy パッケージから多くのものをインポートする必要があります。
Remember that SQLAlchemy has a declarative approach, so we need to instantiate the object Base and then use it as a starting point to declare the tables/objects.
SQLAlchemy は宣言的なアプローチなので、**オブジェクト `Base` をインスタンス化し、それを起点としてテーブルやオブジェクトを宣言する必要がある**ことを覚えておいてください。

```python
class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)

    code = Column(String(36), nullable=False)
    size = Column(Integer)
    price = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
```

This is the class that represents the room in the database.
これはデータベース内の部屋を表すクラスです。
It is important to understand that this is not the class we are using in the business logic, but the class that defines the table in the SQL database that we will use to map the Room entity.
**これはビジネスロジックで使用するクラスではなく、ルーム・エンティティをマッピングするために使用するSQLデータベースのテーブルを定義するクラスである**ことを理解することが重要です。(Entities層のDomain Modelとは別物だって話...!)
The structure of this class is thus dictated by the needs of the storage layer, and not by the use cases.
したがって、**このクラスの構造は、usecaseではなく、Storage層のニーズによって決まる**。
You might want for instance to store longitude and latitude in a JSON field, to allow for easier extendibility, without changing the definition of the domain model.
例えば、ドメインモデルの定義を変更することなく、より簡単に拡張できるように、**経度と緯度をJSONフィールドに格納したいと思うかも**しれません.
In the simple case of the Rent-o-matic project, the two classes almost overlap, but this is not the case generally speaking.
レント・オ・マティック・プロジェクトの**今回の例のような単純なケースでは、この2つのクラスはほぼ重なっているが、一般的にはそうではない**.(i.e. Domain Modelクラスと、DBへのmapping用に定義されるORMクラスは、重なっている必要はないし、異なる事も多い...!!)

Obviously, this means that you have to keep the storage and the domain levels in sync and that you need to manage migrations on your own.
これは明らかに、**ストレージとドメインのレベルを同期させておく必要があり**(i.e. Domain Modelとテーブルの1レコードの単位を一致させておく?? fieldは別に一致してなくてもよいが...!)、移行を自分で管理する必要があることを意味する。
You can use tools like Alembic, but the migrations will not come directly from domain model changes.
Alembicのようなツールを使うこともできるが、移行はドメインモデルの変更から直接もたらされるものではない。

## Orchestration management¶ オーケストレーション管理

When we run the integration tests the Postgres database engine must be already running in the background, and it must be already configured, for example, with a pristine database ready to be used.
**統合テストを実行するとき、Postgres データベースエンジンはすでにバックグラウンドで動作している必要があり**(うんうん...!テストダブルを使わないから!)、例えば、原始的なデータベースを使用できるように設定済みでなければなりません.
Moreover, when all the tests have been executed the database should be removed and the database engine stopped.
さらに、すべてのテストが実行されたら、データベースを削除し、データベースエンジンを停止しなければならない.(clean-up的な動作...!)

This is a perfect job for Docker, which can run complex systems in isolation with minimal configuration.
これは、複雑なシステムを最小限の構成で分離して実行できるDockerにとって完璧な仕事だ。
We have a choice here: we might want to orchestrate the creation and destruction of the database with an external script or try to implement everything in the test suite.
外部スクリプトでデータベースの作成と破棄をオーケストレーションするか、テスト・スイートですべてを実装するか。
The first solution is what many frameworks use, and what I explored in my series of posts Flask Project Setup: TDD, Docker, Postgres and more, so in this chapter I will show an implementation of that solution.
最初の解決策は、多くのフレームワークが使っているもので、Flaskプロジェクトのセットアップという記事で紹介したものだ： TDD、Docker、Postgresなど。この章では、そのソリューションの実装を紹介しよう。

As I explained in the posts I mentioned the plan is to create a management script that spins up and tears down the required containers, runs the tests in between.
私が言及した投稿で説明したように、計画では、必要なコンテナをスピンアップして破棄し、その間にテストを実行する管理スクリプトを作成することです。
The management script can be used also to run the application itself, or to create development setups, but in this case I will simplify it to manage only the tests.
管理スクリプトは、アプリケーション自体の実行や開発セットアップの作成にも使用できるが、今回はテストだけを管理するために簡略化する。
I highly recommend that you read those posts if you want to get the big picture behind the setup I will use.
私が使うセットアップの全体像を知りたければ、これらの記事を読むことを強くお勧めする.

The first thing we have to do if we plan to use Docker Compose is to add the requirement to requirements/test.txt
Docker Composeを使用する場合、最初にしなければならないことは、requirements/test.txtに要件を追加することです。

```
-r prod.txt
tox
coverage
pytest
pytest-cov
pytest-flask
docker-compose
```

and install it running pip install -r requirements/dev.txt.
を実行し、pip install -r requirements/dev.txtを実行してインストールする。
The management script is the following
管理スクリプトは以下の通り。

```python
#! /usr/bin/env python

import os
import json
import subprocess
import time

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


APPLICATION_CONFIG_PATH = "config"
DOCKER_PATH = "docker"


def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")


def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f"{config}.yml")


def read_json_configuration(config):
    # Read configuration from the relative JSON file
    with open(app_config_file(config)) as f:
        config_data = json.load(f)

    # Convert the config into a usable Python dictionary
    config_data = dict((i["name"], i["value"]) for i in config_data)

    return config_data


def configure_app(config):
    configuration = read_json_configuration(config)

    for key, value in configuration.items():
        setenv(key, value)


@click.group()
def cli():
    pass


def docker_compose_cmdline(commands_string=None):
    config = os.getenv("APPLICATION_CONFIG")
    configure_app(config)

    compose_file = docker_compose_file(config)

    if not os.path.isfile(compose_file):
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker-compose",
        "-p",
        config,
        "-f",
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    return command_line


def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode("utf-8"):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)


@cli.command()
@click.argument("args", nargs=-1)
def test(args):
    os.environ["APPLICATION_CONFIG"] = "testing"
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("logs postgres")
    wait_for_logs(cmdline, "ready to accept connections")

    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    cmdline = [
        "pytest",
        "-svv",
        "--cov=application",
        "--cov-report=term-missing",
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)


if __name__ == "__main__":
    cli()
```

Let's see what it does block by block.
ブロックごとに見てみよう。

```python
#! /usr/bin/env python

import os
import json
import subprocess
import time

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


APPLICATION_CONFIG_PATH = "config"
DOCKER_PATH = "docker"
```

Some Docker containers (like the PostgreSQL one that we will use shortly) depend on environment variables to perform the initial setup, so we need to define a function to set environment variables if they are not already initialised.
いくつかのDockerコンテナ（まもなく使用するPostgreSQLのような）は、初期設定を行うために環境変数に依存しているため、環境変数がまだ初期化されていない場合は、**環境変数を設定する関数を定義する必要がある**。
We also define a couple of paths for configuration files.
また、コンフィギュレーション・ファイル用のパスもいくつか定義する。

```python
def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")


def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f"{config}.yml")


def read_json_configuration(config):
    # Read configuration from the relative JSON file
    with open(app_config_file(config)) as f:
        config_data = json.load(f)

    # Convert the config into a usable Python dictionary
    config_data = dict((i["name"], i["value"]) for i in config_data)

    return config_data


def configure_app(config):
    configuration = read_json_configuration(config)

    for key, value in configuration.items():
        setenv(key, value)
```

As in principle I expect to have a different configuration at least for development, testing, and production, I introduced app_config_file and docker_compose_file that return the specific file for the environment we are working in.
原則的には、少なくとも開発、テスト、本番で異なるコンフィギュレーションを持つことを想定しているので、作業環境に応じた特定のファイルを返すapp_config_fileとdocker_compose_fileを導入した。
The function read_json_configuration has been isolated from configure_app as it will be imported by the tests to initialise the database repository.
関数 read_json_configuration は、データベースリポジトリを初期化するためにテストによってインポートされるため、configure_app から分離された。

```python
@click.group()
def cli():
    pass


def docker_compose_cmdline(commands_string=None):
    config = os.getenv("APPLICATION_CONFIG")
    configure_app(config)

    compose_file = docker_compose_file(config)

    if not os.path.isfile(compose_file):
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker-compose",
        "-p",
        config,
        "-f",
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    return command_line
```

This is a simple function that creates the Docker Compose command line that avoids repeating long lists of options whenever we need to orchestrate the containers.
これは、Docker Composeコマンドラインを作成するシンプルな関数で、コンテナのオーケストレーションが必要なときに、オプションの長いリストを繰り返すのを避けることができます。

```python
def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode("utf-8"):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)
```

The function run_sql allows us to run SQL commands on a running Postgres database, and will come in handy when we will create the empty test database.
`run_sql`関数を使用すると、実行中のPostgresデータベース上でSQLコマンドを実行することができます。
The second function, wait_for_logs is a simple way to monitor the Postgres container and to be sure it's ready to be used.
番目の関数 `wait_for_logs` は、Postgres コンテナを監視し、使用可能な状態にあることを確認する簡単な方法である。
Whenever you spin up containers programmatically you need to be aware that they have a certain startup time before they are ready, and act accordingly.
プログラムでコンテナをスピンアップするときは常に、準備が整うまでに一定の起動時間があることを認識し、それに従って行動する必要がある。

```python
@cli.command()
@click.argument("args", nargs=-1)
def test(args):
    os.environ["APPLICATION_CONFIG"] = "testing"
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("logs postgres")
    wait_for_logs(cmdline, "ready to accept connections")

    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    cmdline = [
        "pytest",
        "-svv",
        "--cov=application",
        "--cov-report=term-missing",
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)


if __name__ == "__main__":
    cli()
```

This function is the last that we define, and the only command provided by our management script.
この関数は最後に定義するもので、管理スクリプトが提供する唯一のコマンドである。
First of all the application is configured with the name testing, which means that we will use the configuration file config/testing.json and the Docker Compose file docker/testing.yml.
まず最初に、アプリケーションをtestingという名前で設定します。つまり、設定ファイルconfig/testing.jsonとDocker Composeファイルdocker/testing.ymlを使います。
All these names and paths are just conventions that comes from the arbitrary setup of this management script, so you are clearly free to structure your project in a different way.
これらの名前とパスはすべて、この管理スクリプトの任意の設定から生まれた慣習にすぎない。

The function then spins up the containers according to the Docker Compose file, running docker-compose up -d.
この関数は、Docker Composeファイルに従ってコンテナをスピンアップし、docker-compose up -dを実行する。
It waits for the log message that communicates the database is ready to accept connections and runs the SQL command that creates the testing database.
データベースが接続を受け入れる準備ができたことを伝えるログメッセージを待ち、テスト用データベースを作成するSQLコマンドを実行する。

After this it runs Pytest with a default set of options, adding all the options that we will provide on the command line, and eventually tears down the Docker Compose containers.
この後、デフォルトのオプションセットでPytestを実行し、コマンドラインで指定するすべてのオプションを追加し、最終的にDocker Composeコンテナを破棄する。

To complete the setup we need to define a configuration file for Docker Compose
セットアップを完了するには、Docker Compose用の設定ファイルを定義する必要があります。

```yml
version: "3.8"

services:
  postgres:
    image: postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
```

And finally a JSON configuration file
最後にJSON設定ファイル

```json
[
  {
    "name": "FLASK_ENV",
    "value": "production"
  },
  {
    "name": "FLASK_CONFIG",
    "value": "testing"
  },
  {
    "name": "POSTGRES_DB",
    "value": "postgres"
  },
  {
    "name": "POSTGRES_USER",
    "value": "postgres"
  },
  {
    "name": "POSTGRES_HOSTNAME",
    "value": "localhost"
  },
  {
    "name": "POSTGRES_PORT",
    "value": "5433"
  },
  {
    "name": "POSTGRES_PASSWORD",
    "value": "postgres"
  },
  {
    "name": "APPLICATION_DB",
    "value": "test"
  }
]
```

A couple of notes about this configuration.
このコンフィギュレーションについて、いくつか注意点がある。
First of all it defines both FLASK_ENV and FLASK_CONFIG.
まず、FLASK_ENVとFLASK_CONFIGの両方を定義している。
The first is, as you might remember, and internal Flask variable that can only be development or production, and is connected with the internal debugger.
1つ目は、覚えているかもしれないが、Flaskの内部変数で、開発用か本番用しかなく、内部デバッガとつながっている。
The second is the variable that we use to configure our Flask application with the objects in application/config.py.
2つ目は、application/config.pyにあるオブジェクトを使ってFlaskアプリケーションを設定するために使う変数です。
For testing purposes we set FLASK_ENV to production as we don't need the internal debugger, and FLASK_CONFIG to testing, which will resul in the application being configured with the class TestingConfig.
テスト目的では、内部デバッガーを必要としないので、FLASK_ENVをproductionに設定し、FLASK_CONFIGをtestingに設定します。
This class sets the internal Flask parameter TESTING to True.
このクラスは、Flask の内部パラメータ TESTING を True に設定します。

The rest of the JSON configuration initialises variables whose names start with the prefix POSTGRES*.
JSONコンフィギュレーションの残りの部分は、プレフィックスPOSTGRES*で始まる名前の変数を初期化する。
These are variables required by the Postgres Docker container.
これらは Postgres Docker コンテナが必要とする変数である。
When the container is run, it automatically creates a database with the name specified by POSTGRES_DB.
コンテナが実行されると、POSTGRES_DB で指定された名前のデータベースが自動的に作成される。
It also creates a user with a password, using the values specified in POSTGRES_USER and POSTGRES_PASSWORD.
また、POSTGRES_USERとPOSTGRES_PASSWORDで指定された値を使用して、パスワード付きユーザーを作成する。

Last, I introduced the variable APPLICATION_DB because I want to create a specific database which is not the one the default one.
最後に、APPLICATION_DBという変数を導入したのは、デフォルトのデータベースではない特定のデータベースを作成したいからだ。
The default port POSTGRES_PORT has been changed from the standard value 5432 to 5433 to avoid clashing with any database already running on the machine (either natively or containerised).
POSTGRES_PORTのデフォルト・ポートが標準値の5432から5433に変更され、マシン上ですでに実行されているデータベース（ネイティブまたはコンテナ化されたもの）との衝突を避けるようになった。
As you can see in the Docker Compose configuration file this changes only the external mapping of the container and not the actual port the database engine is using inside the container.
Docker Composeのコンフィギュレーション・ファイルを見ればわかるように、これはコンテナの外部マッピングだけを変更するもので、コンテナ内部でデータベース・エンジンが使用する実際のポートを変更するものではない。

With all these files in place we are ready to start designing our tests.
これらのファイルがすべて揃ったので、テストの設計を始める準備ができた。

## Database fixtures データベース・フィクスチャ

As we defined the configuration of the database in a JSON file we need a fixture that loads that same configuration, so that we can connect to the database during the tests.
データベースの設定を JSON ファイルで定義したので、同じ設定をロードするフィクスチャが必要です。
As we already have the function read_json_configuration in the management script we just need to wrap that.
管理スクリプトにはすでにread_json_configuration関数があるので、それをラップするだけでよい。
This is a fixture that is not specific to the Postgres repository, so I will introduce it in tests/conftest.py
これは Postgres リポジトリに特有ではないフィクスチャなので、tests/conftest.py で紹介します。

As you can see I hardcoded the name of the configuration file for simplicity's sake.
見ての通り、簡単のためにコンフィギュレーション・ファイルの名前をハードコードした。
Another solution might be to create an environment variable with the application configuration in the management script and to read it from here.
別の解決策としては、管理スクリプトにアプリケーション・コンフィギュレーションを含む環境変数を作成し、ここから読み込む方法がある。

The rest of the fixtures contains code that is specific to Postgres, so it is better to keep the code separated in a more specific file conftest.py
フィクスチャの残りの部分には Postgres 固有のコードが含まれています。

The first fixture pg_session_empty creates a session to the empty initial database, while pg_test_data defines the values that we will load into the database.
最初のフィクスチャpg_session_emptyは空の初期データベースへのセッションを作成し、pg_test_dataはデータベースにロードする値を定義します。
As we are not mutating this set of values we don't need to create a fixture, but this is the easier way to make it available both to the other fixtures and to the tests.
この値のセットを変更するわけではないので、フィクスチャを作成する必要はありませんが、他のフィクスチャとテストの両方で利用できるようにするには、この方法が簡単です。
The last fixture pg_session fills the database with Postgres objects created with the test data.
最後のフィクスチャpg_sessionは、テストデータで作成されたPostgresオブジェクトでデータベースを埋めます。
Pay attention that these are not entities, but the Postgres objects we created to map them.
これらはエンティティではなく、それらをマッピングするために作成したPostgresオブジェクトであることに注意してください。

Note that this last fixture has a function scope, thus it is run for every test.
この最後のフィクスチャは関数スコープを持っているので、すべてのテストで実行されることに注意してください。
Therefore, we delete all rooms after the yield returns, leaving the database exactly as it was before the test.
従って、イールド・リターン後にすべての部屋を削除し、データベースをテスト前とまったく同じ状態にする。
Generally speaking you should always clean up after tests.
一般的に言って、テストの後には必ず後片付けをしなければならない。
The endpoint we are testing does not write to the database so in this specific case there is no real need to clean up, but I prefer to implement a complete solution from step zero.
私たちがテストしているエンドポイントはデータベースに書き込まないので、この特定のケースではクリーンアップの必要はない。

We can test this whole setup changing the function test_dummy so that it fetches all the rows of the table Room and verifying that the query returns 4 values.
このセットアップ全体をテストするために、関数test_dummyを変更し、テーブルRoomのすべての行を取得し、クエリが4つの値を返すことを確認します。

The new version of tests/repository/postgres/test_postgresrepo.py is
tests/repository/postgres/test_postgresrepo.pyの新しいバージョンは次のとおりです。

At this point you can run the test suite with integration tests.
この時点で、統合テストを含むテスト・スイートを実行できる。
You should notice a clear delay when pytest executes the function test_dummy as Docker will take some time to spin up the database container and prepare the data
Dockerがデータベースコンテナをスピンアップしてデータを準備するのに時間がかかるため、pytestが関数test_dummyを実行する際に明らかな遅延が発生することに気づくはずです。

Note that to pass the option --integration we need to use -- otherwise Click would consider the option as belonging to the script ./manage.py instead of passing it as a pytest argument.
オプション --integration を渡すには -- を使う必要があることに注意してください。そうしないと、Click はオプションを pytest の引数として渡すのではなく、スクリプト ./manage.py に属するものとみなしてしまいます。

## Integration tests 統合テスト

At this point we can create the real tests in the file test_postgresrepo.py, replacing the function test_dummy.
この時点で、test_postgresrepo.py で test_dummy 関数を置き換えて実際のテストを作成することができます。
All test receive the fixtures app_configuration, pg_session, and pg_test_data.
全てのテストはフィクスチャapp_configuration、pg_session、pg_test_dataを受け取ります。
The first fixture allows us to initialise the class PostgresRepo using the proper parameters.
最初のフィクスチャでは、適切なパラメータを使用してPostgresRepoクラスを初期化します。
The second creates the database using the test data that is then contained in the third fixture.
2番目は、3番目のフィクスチャーに含まれるテストデータを使ってデータベースを作成する。

The tests for this repository are basically a copy of the ones created for MemRepo, which is not surprising.
このリポジトリのテストは、基本的にMemRepo用に作成されたもののコピーである。
Usually, you want to test the very same conditions, whatever the storage system.
通常、どのようなストレージシステムであれ、まったく同じ条件でテストしたいものだ。
Towards the end of the chapter we will see, however, that while these files are initially the same, they can evolve differently as we find bugs or corner cases that come from the specific implementation (in-memory storage, PostgreSQL, and so on).
しかし、この章の終わりには、これらのファイルは最初は同じであっても、特定の実装（インメモリ・ストレージ、PostgreSQLなど）に由来するバグやコーナーケースを発見するにつれて、異なる進化を遂げる可能性があることがわかるだろう。

Remember that I introduced these tests one at a time and that I'm not showing you the full TDD workflow only for brevity's sake.
これらのテストを1つずつ紹介したこと、そして簡潔にするためにTDDのワークフロー全体をお見せしていないことを忘れないでほしい。
The code of the class PostgresRepo has been developed following a strict TDD approach, and I recommend you to do the same.
PostgresRepoクラスのコードは、厳格なTDDアプローチに従って開発されています。
The resulting code goes in rentomatic/repository/postgresrepo.py, the same directory where we created the file postgres_objects.py.
結果のコードは、postgres_objects.pyを作成したディレクトリと同じ、rentomatic/repository/postgresrepo.pyにあります。

You might notice that PostgresRepo is very similar to MemRepo.
PostgresRepoがMemRepoと非常によく似ていることにお気づきだろう。
This is the case because the case we are dealing with here, the list of Room objects, is pretty simple, so I don't expect great differences between an in-memory database an a production-ready relational one.
というのも、ここで扱っているルーム・オブジェクトのリストは非常にシンプルなものなので、インメモリ・データベースと本番用のリレーショナル・データベースの間に大きな違いはないと考えられるからだ。
As the use cases get more complex you will need to start leveraging the features provided by the engine that you are using, and methods such as list might evolve to become very different.
ユースケースが複雑になればなるほど、使用しているエンジンが提供する機能を活用し始める必要があり、リストのような方法はまったく異なるものに進化するかもしれない。

Note that the method list returns domain models, which is allowed as the repository is implemented in one of the outer layers of the architecture.
これは、リポジトリがアーキテクチャの外側のレイヤーの1つに実装されているため許される。

As you can see, while setting up a proper integration testing environment is not trivial, the changes that our architecture required to work with a real repository are very limited.
おわかりのように、適切な統合テスト環境を構築することは些細なことではないが、我々のアーキテクチャが実際のリポジトリで動作するために必要な変更は非常に限られている。
I think this is a good demonstration of the flexibility of a layered approach such as the one at the core of the clean architecture.
これは、クリーン・アーキテクチャーの中核にあるようなレイヤーアプローチの柔軟性を示す良いデモンストレーションだと思う。

Since this chapter mixed the setup of the integration testing with the introduction of a new repository, I will dedicate the next chapter purely to introduce a repository based on MongoDB, using the same structure that I created in this chapter.
この章では、統合テストのセットアップと新しいリポジトリの導入が混在していたので、次の章では純粋に、この章で作成したのと同じ構造を使って、MongoDBベースのリポジトリを導入することに専念する。
Supporting multiple databases (in this case even relational and non-relational) is not an uncommon pattern, as it allows you to use the approach that best suits each use case.
複数のデータベース（この場合はリレーショナルとノンリレーショナル）をサポートすることは、それぞれのユースケースに最適なアプローチを使うことができるため、珍しいパターンではない。
