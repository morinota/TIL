## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-04/
https://www.thedigitalcatbooks.com/pycabook-chapter-04/

# Chapter 4 - Add a web application 第4章 ウェブアプリケーションの追加

For your information, Hairdo, a major network is interested in me.
ちなみにヘアード、ある大手ネットワークが私に興味を持っている。

Groundhog Day, 1993
グラウンドホッグ・デイ（1993年

In this chapter, I will go through the creation of an HTTP endpoint for the room list use case.
この章では、**部屋リストのユースケースのためのHTTPエンドポイントの作成**について説明します。
An HTTP endpoint is a URL exposed by a Web server that runs a specific logic and returns values in a standard format.
HTTPエンドポイントは、ウェブ・サーバーが公開するURLで、特定のロジックを実行し、標準フォーマットで値を返す。

I will follow the REST recommendation, so the endpoint will return a JSON payload.
エンドポイントはJSONペイロードを返す。
REST is however not part of the clean architecture, which means that you can choose to model your URLs and the format of returned data according to whatever scheme you prefer.
しかし、RESTはクリーン・アーキテクチャの一部ではない。つまり、URLや返されるデータのフォーマットを、好きな方式でモデル化することができる。

To expose the HTTP endpoint we need a web server written in Python, and in this case, I chose Flask.
**HTTPエンドポイントを公開するには、Pythonで書かれたウェブ・サーバーが必要**で、今回はFlaskを選んだ。
Flask is a lightweight web server with a modular structure that provides just the parts that the user needs.
Flaskは、ユーザーが必要とする部分だけを提供するモジュール構造を持つ軽量なWebサーバーである。
In particular, we will not use any database/ORM, since we already implemented our own repository layer.
特に、我々はすでに独自のリポジトリ・レイヤーを実装しているので、データベース／ORMは使用しない。

## Flask setup フラスコのセットアップ

Let us start updating the requirements files.
要件ファイルの更新を始めよう。
The file requirements/prod.txt shall mention Flask, as this package contains a script that runs a local webserver that we can use to expose the endpoint
requirements/prod.txtファイルでは、Flaskについて触れている。このパッケージには、エンドポイントを公開するために使用できる、ローカルのウェブサーバーを実行するスクリプトが含まれているからだ。

```
Flask
```

The file requirements/test.txt will contain the pytest extension to work with Flask (more on this later)
requirements/test.txtファイルには、Flaskで動作するためのpytest extensionが含まれます。

```
-r prod.txt
pytest
tox
coverage
pytest-cov
pytest-flask
```

Remember to run pip install -r requirements/dev.txt again after those changes to install the new packages in your virtual environment.
仮想環境に新しいパッケージをインストールするために、変更後に再度pip install -r requirements/dev.txtを実行することを忘れないでください。

The setup of a Flask application is not complex, but there are a lot of concepts involved, and since this is not a tutorial on Flask I will run quickly through these steps.
Flaskアプリケーションのセットアップは複雑ではないが、多くのコンセプトが関係している。
I will provide links to the Flask documentation for every concept, though.
すべてのコンセプトについて、Flaskのドキュメントへのリンクを提供します。
If you want to dig a bit deeper in this matter you can read my series of posts Flask Project Setup: TDD, Docker, Postgres and more.
この件についてもう少し掘り下げたい場合は、私の一連の投稿[Flask Project Setup： TDD、Docker、Postgres等](https://www.thedigitalcatonline.com/blog/2020/07/05/flask-project-setup-tdd-docker-postgres-and-more-part-1/)をお読みください。

The Flask application can be configured using a plain Python object (documentation), so I created the file application/config.py that contains this code
Flaskアプリケーションは、プレーンなPythonオブジェクト（ドキュメント）を使って設定できるので、次のコードを含むapplication/config.pyファイルを作成した。

```python
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""


class ProductionConfig(Config):
    """Production configuration"""


class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
```

Read this page to know more about Flask configuration parameters.
Flaskの設定パラメータについて詳しくは、[このページ](http://flask.pocoo.org/docs/latest/config/)を読んでください.

Now we need a function that initialises the Flask application (documentation), configures it, and registers the blueprints (documentation).
ここで、Flaskアプリケーション（ドキュメント）を初期化し、設定し、ブループリント（ドキュメント）を登録する関数が必要になります。
The file application/app.py contains the following code, which is an app factory
application/app.pyファイルには以下のコードが含まれています。

```python
from flask import Flask

from application.rest import room


def create_app(config_name):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    app.register_blueprint(room.blueprint)

    return app
```

## Test and create an HTTP endpoint HTTP エンドポイントのテストと作成

Before we create the proper setup of the webserver, we want to create the endpoint that will be exposed.
ウェブサーバーの適切なセットアップを行う前に、公開するエンドポイントを作成したい。
Endpoints are ultimately functions that are run when a user sends a request to a certain URL, so we can still work with TDD, as the final goal is to have code that produces certain results.
**エンドポイントとは、最終的にはユーザが特定のURLにリクエストを送ったときに実行される関数のこと**で、最終的なゴールは特定の結果を生み出すコードを持つことなので、TDDで作業することはできる.

The problem we have testing an endpoint is that we need the webserver to be up and running when we hit the test URLs.
エンドポイントをテストする際に問題になるのは、テストURLをヒットする際にウェブサーバーが稼働している必要があるということだ。
The webserver itself is an external system so we won't test it, but the code that provides the endpoint is part of our application[1].
ウェブサーバ自体は外部のシステムなのでテストしませんが、**エンドポイントを提供するコードはアプリケーションの一部**です[1].
It is actually a gateway, that is an interface that allows an HTTP framework to access the use cases.
これは実際にはGateways(endpointはExternal Systemsではないのか...!:thinking:)であり、HTTPフレームワークがユースケースにアクセスするためのインターフェースである.

The extension pytest-flask allows us to run Flask, simulate HTTP requests, and test the HTTP responses.
**pytest-flaskという拡張機能(ここではpackage!)を使うと、Flaskを実行してHTTPリクエストをシミュレートし、HTTPレスポンスをテストすることができます。**
This extension hides a lot of automation, so it might be considered a bit "magic" at a first glance.
このエクステンションは多くの自動化を隠しているため、一見するとちょっと「マジック」と思われるかもしれない.
When you install it some fixtures like client are available automatically, so you don't need to import them.
インストールすると、`client`のようないくつかのフィクスチャが自動的に利用可能になるので、それらをインポートする必要はありません.
Moreover, it tries to access another fixture named app that you have to define.
さらに、**あなたが定義しなければならない `app` という別のフィクスチャ**にアクセスしようとします。
This is thus the first thing to do.
したがって、これが最初にすべきことである。

Fixtures can be defined directly in your test file, but if we want a fixture to be globally available the best place to define it is the file conftest.py which is automatically loaded by pytest.
フィクスチャはテストファイルで直接定義することができますが、フィクスチャをグローバルに利用できるようにするには、pytestによって自動的にロードされる `conftest.py` ファイルが最適です。
As you can see there is a great deal of automation, and if you are not aware of it you might be surprised by the results, or frustrated by the errors.
ご覧の通り、非常に多くの自動化が行われており、それに気づかなければ、結果に驚いたり、エラーに苛立ったりするかもしれない。

```python
import pytest


from application.app import create_app


@pytest.fixture
def app():
    app = create_app("testing")

    return app
```

The function app runs the app factory to create a Flask app, using the configuration testing, which sets the flag TESTING to True.
関数`app`は、フラグ`TESTING`をTrueに設定する設定 `testing` を使用して、Flaskアプリを作成するためにアプリファクトリーを実行します。
You can find the description of these flags in the official documentation.
これらのフラグの説明は公式ドキュメントにある。

At this point, we can write the test for our endpoint.
この時点で、エンドポイントのテストを書くことができます。

```python
import json
from unittest import mock

from rentomatic.domain.room import Room

room_dict = {
    "code": "3251a5bd-86be-428d-8ae9-6e51a8048c33",
    "size": 200,
    "price": 10,
    "longitude": -0.09998975,
    "latitude": 51.75436293,
}

rooms = [Room.from_dict(room_dict)]


@mock.patch("application.rest.room.room_list_use_case")
def test_get(mock_use_case, client):
    mock_use_case.return_value = rooms

    http_response = client.get("/rooms")

    assert json.loads(http_response.data.decode("UTF-8")) == [room_dict]
    mock_use_case.assert_called()
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"
```

Let's comment it section by section.
セクションごとにコメントしよう。

```python
import json
from unittest import mock

from rentomatic.domain.room import Room

room_dict = {
    "code": "3251a5bd-86be-428d-8ae9-6e51a8048c33",
    "size": 200,
    "price": 10,
    "longitude": -0.09998975,
    "latitude": 51.75436293,
}

rooms = [Room.from_dict(room_dict)]
```

The first part contains some imports and sets up a room from a dictionary.
最初のパートは、いくつかのインポートを含み、辞書からRoomを設定する.
This way we can later directly compare the content of the initial dictionary with the result of the API endpoint.
こうすることで、初期辞書の内容とAPIエンドポイントの結果を後で直接比較することができる。
Remember that the API returns JSON content, and we can easily convert JSON data into simple Python structures, so starting from a dictionary will come in handy.
APIはJSONコンテンツを返し、JSONデータを単純なPython構造に簡単に変換できることを忘れないでください。

```python
@mock.patch("application.rest.room.room_list_use_case")
def test_get(mock_use_case, client):
```

This is the only test that we have for the time being.
今のところ、これが唯一のテストだ。
During the whole test, we mock the use case, as we are not interested in running it, as it has been already tested elsewhere.
テスト全体を通して、ユースケースをモックする。
We are however interested in checking the arguments passed to the use case, and a mock can provide this information.
しかし、私たちはユースケースに渡された引数をチェックすることに興味があり、モックがこの情報を提供してくれる。
The test receives the mock from the decorator patch and the fixture client, which is one of the fixtures provided by pytest-flask.
テストはデコレーターパッチとフィクスチャークライアントからモックを受け取ります。フィクスチャークライアントはpytest-flaskが提供するフィクスチャの1つです。
The fixture automatically loads app, which we defined in conftest.py, and is an object that simulates an HTTP client that can access the API endpoints and store the responses of the server.
フィクスチャは自動的にappをロードします。appはconftest.pyで定義したもので、APIのエンドポイントにアクセスし、サーバーのレスポンスを保存できるHTTPクライアントをシミュレートするオブジェクトです。

```python
    mock_use_case.return_value = rooms

    http_response = client.get("/rooms")

    assert json.loads(http_response.data.decode("UTF-8")) == [room_dict]
    mock_use_case.assert_called()
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"
```

The first line initialises the mock use case, instructing it to return the fixed rooms variable that we created previously.
最初の行はモック・ユースケースを初期化し、前回作成した固定ルーム変数を返すように指示している. (テストダブルとしてstubを設定している!)
The central part of the test is the line where we get the API endpoint, which sends an HTTP GET request and collects the server's response.
**テストの中心部分は、APIエンドポイントを取得する行で、HTTP GETリクエストを送信し、サーバのレスポンスを収集する**.

After this, we check that the data contained in the response is a JSON that contains the data in the structure room_dict, that the method use_case has been called, that the HTTP response status code is 200, and last that the server sends the correct MIME type back.
この後、レスポンスに含まれるデータがroom_dict構造体のデータを含むJSONであること、use_caseメソッドが呼び出されたこと、HTTPレスポンス・ステータス・コードが200であること、そして最後にサーバーが正しいMIMEタイプを送り返すことをチェックする。

It's time to write the endpoint, where we will finally see all the pieces of the architecture working together, as they did in the little CLI program that we wrote previously.
エンドポイントを書くときが来た。ここでようやく、以前に書いた小さなCLIプログラムのように、アーキテクチャーのすべてのピースが一緒に動くのを見ることができる。
Let me show you a template for the minimal Flask endpoint we can create
最小限のFlaskエンドポイントのテンプレートをお見せしましょう。

```python
blueprint = Blueprint('room', __name__)


@blueprint.route('/rooms', methods=['GET'])
def room_list():
    # [LOGIC] (ドメインロジックがここで実行される.)
    return Response([JSON DATA],
                    mimetype='application/json',
                    status=[STATUS])
```

As you can see the structure is really simple.
ご覧の通り、構造は実にシンプルだ.
Apart from setting the blueprint, which is the way Flask registers endpoints, we create a simple function that runs the endpoint, and we decorate it assigning the enpoint /rooms that serves GET requests.
**Flaskがエンドポイントを登録する方法であるブループリントの設定とは別に、エンドポイントを実行するシンプルな関数を作成**し、GETリクエストに対応するenpoint `/rooms`を割り当てて装飾します.
The function will run some logic and eventually return a Response that contains JSON data, the correct MIME type, and an HTTP status that represents the success or failure of the logic.
この関数はいくつかのロジックを実行し、最終的にJSONデータ、正しいMIMEタイプ、ロジックの成否を表すHTTPステータスを含む`Response`を返す.

The above template becomes the following code
上記のテンプレートは以下のコードになる。

```python
import json

from flask import Blueprint, Response

from rentomatic.repository.memrepo import MemRepo
from rentomatic.use_cases.room_list import room_list_use_case
from rentomatic.serializers.room import RoomJsonEncoder

blueprint = Blueprint("room", __name__)

rooms = [
    {
        "code": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "size": 215,
        "price": 39,
        "longitude": -0.09998975,
        "latitude": 51.75436293,
    },
    {
        "code": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        "size": 405,
        "price": 66,
        "longitude": 0.18228006,
        "latitude": 51.74640997,
    },
    {
        "code": "913694c6-435a-4366-ba0d-da5334a611b2",
        "size": 56,
        "price": 60,
        "longitude": 0.27891577,
        "latitude": 51.45994069,
    },
    {
        "code": "eed76e77-55c1-41ce-985d-ca49bf6c0585",
        "size": 93,
        "price": 48,
        "longitude": 0.33894476,
        "latitude": 51.39916678,
    },
]


@blueprint.route("/rooms", methods=["GET"])
def room_list():
    repo = MemRepo(rooms)
    result = room_list_use_case(repo)

    return Response(
        json.dumps(result, cls=RoomJsonEncoder),
        mimetype="application/json",
        status=200,
    )
```

Please note that I initialised the memory storage with the same list used for the script cli.py.
メモリストレージは cli.py スクリプトと同じリストで初期化しました。
Again, the need of initialising the storage with data (even with an empty list) is due to the limitations of the storage MemRepo.
繰り返しになるが、ストレージをデータで初期化する必要があるのは（たとえ空のリストであっても）、ストレージMemRepoの制限によるものである。
The code that runs the use case is
ユースケースを実行するコードは

```python
def room_list():
    repo = MemRepo(rooms)
    result = room_list_use_case(repo)
```

which is exactly the same code that we used in the command-line interface.
これは、**コマンドライン・インターフェイスで使ったコードとまったく同じもの**だ。
The last part of the code creates a proper HTTP response, serializing the result of the use case using RoomJsonEncoder, and setting the HTTP status to 200 (success)
コードの最後の部分は、RoomJsonEncoderを使用してユースケースの結果をシリアライズし、HTTPステータスを200（成功）に設定し、適切なHTTPレスポンスを作成する>(返り値を生成する処理以外は、REST APIだろうとCLIだろうと同じ...!! ドメインロジックは影響を受けない!)

```python
    return Response(
        json.dumps(result, cls=RoomJsonEncoder),
        mimetype="application/json",
        status=200,
    )
```

This shows you the power of the clean architecture in a nutshell.
これはクリーン・アーキテクチャの威力を端的に示している。
Writing a CLI interface or a Web service is different only in the presentation layer, not in the logic, which is the same, as it is contained in the use case.
**CLIインターフェイスやウェブサービスを書くことは、プレゼンテーションレイヤー(External Systems層??)においてのみ異なる**.

Now that we defined the endpoint, we can finalise the configuration of the webserver, so that we can access the endpoint with a browser.
これでエンドポイントを定義したので、ブラウザでエンドポイントにアクセスできるように、ウェブサーバの設定を確定することができる.
This is not strictly part of the clean architecture, but as I did with the CLI interface I want you to see the final result, to get the whole picture and also to enjoy the effort you put in following the whole discussion up to this point.
これは厳密にはクリーン・アーキテクチャの一部ではないが、CLIインターフェイスで行ったように、最終結果を見て全体像を掴んでもらいたいし、ここまでの議論に費やした労力を楽しんでもらいたい。

## WSGI WSGI

Python web applications expose a common interface called Web Server Gateway Interface or WSGI.
PythonのWebアプリケーションは、**Web Server Gateway Interface(WSGI)**と呼ばれる共通のインターフェースを公開している.
So to run the Flask development web server, we have to define a wsgi.py file in the main folder of the project, i.e.in the same directory of the file cli.py
**Flaskの開発用Webサーバを動かすには、プロジェクトのメインフォルダ、つまりcli.pyと同じディレクトリにwsgi.pyファイルを定義する必要がある.**

```python
import os

from application.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
```

When you run the Flask Command Line Interface (documentation), it automatically looks for a file named wsgi.py and loads it, expecting it to contain a variable named app that is an instance of the object Flask.
Flaskコマンドラインインターフェイス（ドキュメント）を実行すると、**自動的にwsgi.pyという名前のファイルを探し、それを読み込み、その中にFlaskオブジェクトのインスタンスであるappという変数が含まれていることを期待します**。
As the function create_app is a factory we just need to execute it.
関数`create_app`はファクトリーなので、これを実行するだけでよい。

At this point, you can execute FLASK_CONFIG="development" flask run in the directory that contains this file and you should see a nice message like
この時点で、このファイルを含むディレクトリで`FLASK_CONFIG="development" flask run`を実行すると、以下のような素敵なメッセージが表示されるはずだ。

```
hogehoge
```

At this point, you can point your browser to http://127.0.0.1:5000/rooms and enjoy the JSON data returned by the first endpoint of your web application.
この時点で、ブラウザをhttp://127.0.0.1:5000/rooms、ウェブ・アプリケーションの最初のエンドポイントから返されるJSONデータを楽しむことができる。

I hope you can now appreciate the power of the layered architecture that we created.
私たちが作り上げた Layered Architecture のパワーを理解していただけただろうか。
We definitely wrote a lot of code to "just" print out a list of models, but the code we wrote is a skeleton that can easily be extended and modified.
**モデルのリストを "ただ "プリントアウトするために多くのコードを書いたのは確かだが、私たちが書いたコードは、簡単に拡張したり修正したりできる**スケルトン(??)である。(ヘキサゴナルアーキテクチャ的なものによって、拡張や修正、良質な単体テストを作りやすくなった事は分かるが、skeletonって??:thinking: )
It is also fully tested, which is a part of the implementation that many software projects struggle with.
また、多くのソフトウェア・プロジェクトが苦労している実装の部分であるテストも完全に実施されている。

The use case I presented is purposely very simple.
私が提示した usecase は、意図的にとてもシンプルなものだ。
It doesn't require any input and it cannot return error conditions, so the code we wrote completely ignored input validation and error management.
入力を必要とせず、エラー条件を返すこともできないので、私たちが書いたコードは**入力検証(input validation)とエラー管理(error management)を完全に無視していた**。
These topics are however extremely important, so we need to discuss how a clean architecture can deal with them.
しかし、これらのトピックは非常に重要であるため、クリーンなアーキテクチャがどのように対処できるかを議論する必要がある.
