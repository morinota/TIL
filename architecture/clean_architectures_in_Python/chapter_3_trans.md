## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-03/
https://www.thedigitalcatbooks.com/pycabook-chapter-03/

# Chapter 3 - A basic example 第3章 基本的な例

Joshua/WOPR: Wouldn't you prefer a good game of chess?
ジョシュア／WOPR チェスの方がいいんじゃない？

David: Later.
デビッド：後でね。
Let's play Global Thermonuclear War.
世界熱核戦争をやろう。

The goal of the "Rent-o-Matic" project is to create a simple search engine for a room renting company.
Rent-o-Matic "プロジェクトの目標は、部屋を貸す会社のためのシンプルな検索エンジンを作ることだ。(**代わりに卓球コートを貸す会社の為のシンプルな検索エンジンを作ってみよう...!**)
Objects in the dataset (rooms) are described by some attributes and the search engine shall allow the user to set some filters to narrow the search.
データセット(部屋)内のオブジェクトはいくつかの属性によって記述され、検索エンジンは、検索を絞り込むためのいくつかのフィルタをユーザーが設定できるようにしなければならない。

A room is stored in the system through the following values:
部屋は以下の値を通してシステムに保存される：

- A unique identifier 一意の識別子
- A size in square meters 広さ（平方メートル
- A renting price in Euro/day 賃料（ユーロ／日
- Latitude and longitude 緯度と経度

The description is purposely minimal so that we can focus on the architectural problems and how to solve them.
archtecture上の問題とその解決方法に焦点を当てるため、説明はあえて最小限にとどめている.
The concepts that I will show are then easily extendable to more complex cases.
これから紹介するコンセプトは、より複雑なケースにも簡単に拡張できる。

As pushed by the clean architecture model, we are interested in separating the different layers of the system.
クリーン・アーキテクチャ・モデルによって推し進められるように、我々は**システムの異なるレイヤーを分離すること**に興味がある。
Remember that there are multiple ways to implement the clean architecture concepts, and the code you can come up with strongly depends on what your language of choice allows you to do.
**クリーン・アーキテクチャのコンセプトを実装する方法は複数あり、**あなたが思いつくコードは、**選択した言語で何ができるかに強く依存する**ことを覚えておいてほしい。
The following is an example of clean architecture in Python, and the implementation of the models, use cases and other components that I will show is just one of the possible solutions.
以下は、Pythonによるクリーンなアーキテクチャの例であり、これから紹介するmodel、usecase、その他の components の実装は、**(クリーンアーキテクチャのconceptを実装する為の!)可能なソリューションの一つに過ぎない.**

## Project setup プロジェクトのセットアップ

Clone the project repository and move to the branch second-edition.
プロジェクトリポジトリをクローンし、second-editionブランチに移動する。
The full solution is contained in the branch second-edition-top, and the tags I will mention are there.
完全な解決策はsecond-edition-topブランチにあり、これから述べるタグはそこにある。
I strongly advise to code along and to resort to my tags only to spot errors.
私のタグはエラーを発見するためだけに使うことを強く勧める。

```
$ git clone https://github.com/pycabook/rentomatic
$ cd rentomatic
$ git checkout --track origin/second-edition
```

Create a virtual environment following your preferred process and install the requirements
お好みのプロセスに従って仮想環境を作成し、必要なものをインストールする。

```
$ pip install -r requirements/dev.txt
```

You should at this point be able to run
この時点で

```
$ pytest -svv
```

and get an output like
のような出力が得られる。

Later in the project you might want to see the output of the coverage check, so you can activate it with
プロジェクトの後半で、カバレッジ・チェックの出力を見たくなるかもしれない。

```
$ pytest -svv --cov=rentomatic --cov-report=term-missing
```

In this chapter, I will not explicitly state when I run the test suite, as I consider it part of the standard workflow.
この章では、テスト・スイートをいつ実行するかは、標準的なワークフローの一部と考えているので、明示しない。
Every time we write a test you should run the suite and check that you get an error (or more), and the code that I give as a solution should make the test suite pass.
**テストを書くたびに、テスト・スイートを実行し、エラー（またはそれ以上）が出るかどうかをチェックする**必要があります。そして、私が解決策として与えるコードは、テスト・スイートをパスさせるはずです。
You are free to try to implement your own code before copying my solution, obviously.
私の解決策をコピーする前に、あなた自身のコードを実装してみるのは自由だ.

You may notice that I configured the project to use black with an unorthodox line length of 75.
このプロジェクトでは黒を使い、線の長さを75という異例の長さに設定したことにお気づきだろうか。
I chose that number trying to find a visually pleasant way to present code in the book, avoiding wrapped lines that can make the code difficult to read.
この数字を選んだのは、コードを読みにくくする折り返し行を避け、本の中でコードを見せる視覚的に楽しい方法を見つけようとしたためだ。

## Domain models ドメインモデル

Let us start with a simple definition of the model `Room`.
モデル・ルームの簡単な定義から始めよう.
As said before, the clean architecture models are very lightweight, or at least they are lighter than their counterparts in common web frameworks.
先に述べたように、クリーン・アーキテクチャ・モデルは非常に軽量であり、少なくとも一般的なウェブ・フレームワークの同等品よりは軽量である。

Following the TDD methodology, the first thing that I write are the tests.
**TDD手法に従って、私が最初に書くのはテストだ**。
This test ensures that the model can be initialised with the correct values
このテストは、モデルが正しい値で初期化できることを保証する。

```python
import uuid
from rentomatic.domain.room import Room


def test_room_model_init():
    code = uuid.uuid4()
    room = Room(
        code,
        size=200,
        price=10,
        longitude=-0.09998975,
        latitude=51.75436293,
    )

    assert room.code == code
    assert room.size == 200
    assert room.price == 10
    assert room.longitude == -0.09998975
    assert room.latitude == 51.75436293
```

Remember to create an empty file **init**.py in every subdirectory of tests/ that you create, in this case tests/domain/**init**.py.
**作成した `tests/` のサブディレクトリ、この場合は `tests/domain/**init**.py`に空のファイル`**init**.py` を作成することを忘れないでください**.

Now let's write the class Room in the file rentomatic/domain/room.py.
Roomクラスをrentomatic/domain/room.pyに書いてみましょう。

```python
import uuid
import dataclasses


@dataclasses.dataclass
class Room:
    code: uuid.UUID
    size: int
    price: int
    longitude: float
    latitude: float
```

The model is very simple and requires little explanation.
このモデルは非常にシンプルで、説明はほとんど必要ない。
I'm using dataclasses as they are a compact way to implement simple models like this, but you are free to use standard classes and to implement the method **init** explicitly.
**データクラスを使うのは、このような単純なモデルを実装するコンパクトな方法だからだが、標準クラスを使ったり、メソッド**init**を明示的に実装したりするのは自由**だ。

Given that we will receive data to initialise this model from other layers, and that this data is likely to be a dictionary, it is useful to create a method that allows us to initialise the model from this type of structure.
**このモデルを初期化するためのデータを他のレイヤーから受け取ること**、そして**受け取るデータが辞書である可能性が高いこと**を考えると、この種の構造からモデルを初期化できるメソッドを作成することは有用である.
The code can go into the same file we created before, and is
このコードは、前に作ったのと同じファイルに入れることができる。

```python
def test_room_model_from_dict():
    code = uuid.uuid4()
    init_dict = {
        "code": code,
        "size": 200,
        "price": 10,
        "longitude": -0.09998975,
        "latitude": 51.75436293,
    }

    room = Room.from_dict(init_dict)

    assert room.code == code
    assert room.size == 200
    assert room.price == 10
    assert room.longitude == -0.09998975
    assert room.latitude == 51.75436293
```

A simple implementation of it is then
これを簡単に実装すると次のようになる。

```python
@dataclasses.dataclass
class Room:
    code: uuid.UUID
    size: int
    price: int
    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
```

For the same reason mentioned before, it is useful to be able to convert the model into a dictionary, so that we can easily serialise it into JSON or similar language-agnostic formats.
前述したのと同じ理由で、**モデルを辞書に変換できると便利**です。そうすれば、**JSON等の言語に依存しないフォーマットに簡単にシリアライズできます**。
The test for the method to_dict goes again in tests/domain/test_room.py
to_dict メソッドのテストは tests/domain/test_room.py にあります。

and the implementation is trivial using dataclasses
実装はデータクラスを使えば簡単だ。

```python
    def to_dict(self):
        return dataclasses.asdict(self)
```

If you are not using dataclasses you need to explicitly create the dictionary, but that doesn't pose any challenge either.
データクラスを使用しない場合は、明示的に辞書を作成する必要があるが、これも特に問題はない。(pydanticの場合は、`__dict__`を使えばOK...!)
Note that this is not yet a serialisation of the object, as the result is still a Python data structure and not a string.
結果はまだPythonのデータ構造であり、文字列ではないので、**これはまだオブジェクトのシリアライズではない**ことに注意してください。

It is also very useful to be able to compare instances of a model.
**モデルのインスタンスを比較**できるのも非常に便利だ.
The test goes in the same file as the previous test
このテストは前のテストと同じファイルに入れる。

```python
def test_room_model_comparison():
    init_dict = {
        "code": uuid.uuid4(),
        "size": 200,
        "price": 10,
        "longitude": -0.09998975,
        "latitude": 51.75436293,
    }

    room1 = Room.from_dict(init_dict)
    room2 = Room.from_dict(init_dict)

    assert room1 == room2
```

Again, dataclasses make this very simple, as they provide an implementation of **eq** out of the box.
繰り返しになるが、データクラスは`__eq__`の実装をすぐに提供してくれるので、これは非常に簡単である. (dataclassはvalue objectとしてインスタンスを比較する)
If you implement the class without using dataclasses you have to define this method to make it pass the test.
データクラスを使わずにクラスを実装する場合は、テストをパスするためにこのメソッドを定義しなければならない.

## Serializers

Outer layers can use the model Room, but if you want to return the model as a result of an API call you need a serializer.
アウターレイヤーはモデルRoomを使用(i.e. 参照)できますが、API呼び出しの結果としてモデルを返したい場合は、シリアライザーが必要です。

"Serialize": 直列化? 変換的なイメージ.

The typical serialization format is JSON, as this is a broadly accepted standard for web-based APIs.
**典型的なシリアライズ形式はJSON**で、これはウェブベースのAPIで広く受け入れられている標準だからだ。
The serializer is not part of the model but is an external specialized class that receives the model instance and produces a representation of its structure and values.
シリアライザーはモデルの一部ではなく、モデルのインスタンスを受け取り、その構造と値の表現を生成する外部の特殊なクラスです。

This is the test for the JSON serialization of our class Room
これは、我々のクラス・ルームのJSONシリアライゼーションのテストである。

```python
import json
import uuid

from rentomatic.serializers.room import RoomJsonEncoder
from rentomatic.domain.room import Room


def test_serialize_domain_room():
    code = uuid.uuid4()

    room = Room(
        code=code,
        size=200,
        price=10,
        longitude=-0.09998975,
        latitude=51.75436293,
    )

    expected_json = f"""
        {{
            "code": "{code}",
            "size": 200,
            "price": 10,
            "longitude": -0.09998975,
            "latitude": 51.75436293
        }}
    """

    json_room = json.dumps(room, cls=RoomJsonEncoder)

    assert json.loads(json_room) == json.loads(expected_json)
```

Here we create the object Room and write the expected JSON output (please note that the double curly braces are used to avoid clashes with the f-string formatter).
ここでは、オブジェクト・ルームを作成し、期待されるJSON出力を記述する（二重中括弧は、f-stringフォーマッターとの衝突を避けるために使用されていることに注意してください）。
Then we dump the object Room to a JSON string and compare the two.
次に、オブジェクト・ルームをJSON文字列にダンプし、両者を比較する。
To compare the two we load them again into Python dictionaries, to avoid issues with the order of the attributes.
この2つを比較するために、属性の順序の問題を避けるために、Python辞書に再度ロードする。
Comparing Python dictionaries, indeed, doesn't consider the order of the dictionary fields, while comparing strings obviously does.
Pythonの辞書の比較では、辞書のフィールドの順序は考慮されませんが、文字列の比較では明らかに考慮されます。

Put in the file rentomatic/serializers/room.py the code that makes the test pass
rentomatic/serializers/room.pyにテストをパスするコードを記述します。

```python
import json


class RoomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "code": str(o.code),
                "size": o.size,
                "price": o.price,
                "latitude": o.latitude,
                "longitude": o.longitude,
            }
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(o)
```

Providing a class that inherits from json.JSONEncoder let us use the syntax json_room = json.dumps(room, cls=RoomJsonEncoder) to serialize the model.
**json.JSONEncoderを継承したクラスを用意することで、`json_room = json.dumps(room, cls=RoomJsonEncoder)`という構文を使ってモデルをシリアライズすることができます**。
Note that we are not using the method as_dict, as the UUID code is not directly JSON serialisable.
UUIDコードは直接JSONシリアライズできないので、as_dictメソッドは使わないことに注意。
This means that there is a slight degree of code repetition in the two classes, which in my opinion is acceptable, being covered by tests.
つまり、この2つのクラスではコードの繰り返しが若干あるが、テストによってカバーされているので許容範囲だと私は考えている。
If you prefer, however, you can call the method as_dict and then adjust the code field converting it with str.
しかし、お望みなら、as_dictメソッドを呼び出してから、strで変換するコード・フィールドを調整することもできる。

## Use cases 使用例

It's time to implement the actual business logic that runs inside our application.
アプリケーション内部で実行される実際の**ビジネス・ロジック**を実装する時が来た。(重要性 & 複雑性が高いが、依存の数は少ないべき...!)
Use cases are the places where this happens, and they might or might not be directly linked to the external API of the system.
ユースケースは、これが起こる場所であり、システムの外部APIに直接リンクされている場合もあれば、そうでない場合もある.

The simplest use case we can create is one that fetches all the rooms stored in the repository and returns them.
**最も単純なユースケースは、リポジトリに保存されているすべての部屋をフェッチして返すもの**です。
In this first part, we will not implement the filters to narrow the search.
この最初のパートでは、検索を絞り込むためのフィルターは実装しない。
That code will be introduced in the next chapter when we will discuss error management.
このコードについては、次の章でエラー管理について説明する。

The repository is our storage component, and according to the clean architecture it will be implemented in an outer level (external systems).
**リポジトリは我々の storage component** であり、**クリーン・アーキテクチャによれば、それは外部レベル(external systems)に実装される**。
We will access it as an interface, which in Python means that we will receive an object that we expect will expose a certain API.
これはPythonでは、あるAPIを公開するオブジェクトを受け取ることを意味する。
From the testing point of view the best way to run code that accesses an interface is to mock the latter.
テストの観点からは、インターフェイスにアクセスするコードを実行する最善の方法は、後者(Repositoryクラス?)をモックすることである。(道具としてのmockを、テストダブル的にはstub的な使い方をする...!!)
Put this code in the file tests/use_cases/test_room_list.py
このコードを tests/use_cases/test_room_list.py に記述します。

```python
import pytest
import uuid
from unittest import mock

from rentomatic.domain.room import Room
from rentomatic.use_cases.room_list import room_list_use_case


@pytest.fixture
def domain_rooms():
    room_1 = Room(
        code=uuid.uuid4(),
        size=215,
        price=39,
        longitude=-0.09998975,
        latitude=51.75436293,
    )

    room_2 = Room(
        code=uuid.uuid4(),
        size=405,
        price=66,
        longitude=0.18228006,
        latitude=51.74640997,
    )

    room_3 = Room(
        code=uuid.uuid4(),
        size=56,
        price=60,
        longitude=0.27891577,
        latitude=51.45994069,
    )

    room_4 = Room(
        code=uuid.uuid4(),
        size=93,
        price=48,
        longitude=0.33894476,
        latitude=51.39916678,
    )

    return [room_1, room_2, room_3, room_4]


def test_room_list_without_parameters(domain_rooms):
    repo = mock.Mock()
    repo.list.return_value = domain_rooms

    result = room_list_use_case(repo)

    repo.list.assert_called_with()
    assert result == domain_rooms
```

I will make use of pytest's powerful fixtures, but I will not introduce them.
pytestの強力なフィクスチャを利用しますが、紹介はしません。
I highly recommend reading the official documentation, which is very good and covers many different use cases.
公式ドキュメントを読むことを強くお勧めする。

The test is straightforward.
テストは簡単だ。
First, we mock the repository so that it provides a method list that returns the list of models we created above the test.
まず、リポジトリがメソッドリストを提供し、テストの上で作成したモデルのリストを返すようにモックします。(テストダブルの使い方的にはmockではなくstub...!!)
Then we initialise the use case with the repository and execute it, collecting the result.
次に、リポジトリでユースケースを初期化し、実行し、結果を収集する。
The first thing we check is that the repository method was called without any parameter, and the second is the effective correctness of the result.
最初にチェックするのは、リポジトリ・メソッドがパラメーターなしで呼び出されたかどうかであり、2番目にチェックするのは、結果の実効的な正しさである。

Calling the method list of the repository is an outgoing query action that the use case is supposed to perform, and according to the unit testing rules, we should not test outgoing queries.
**リポジトリのメソッドリストを呼び出すことは、ユースケースが実行することになっているoutgoing query(発信クエリ)のアクション**であり、ユニットテストのルールによれば、発信クエリをテストすべきではありません。(古典派の単体テストの定義から見ると全然OKな気がする...!1 unitはクラスではなく振る舞いなので!)
We should, however, test how our system runs the outgoing query, that is the parameters used to run the query.
しかし、システムがどのように発信クエリを実行するか、つまりクエリ実行に使用されるパラメータをテストする必要がある。

Put the implementation of the use case in the file rentomatic/use_cases/room_list.py
ユースケースの実装をrentomatic/use_cases/room_list.pyに記述します。

```python
def room_list_use_case(repo):
    return repo.list()
```

Such a solution might seem too simple, so let's discuss it.
このような解決策は単純すぎると思われるかもしれない。
First of all, this use case is just a wrapper around a specific function of the repository, and it doesn't contain any error check, which is something we didn't take into account yet.
まず第一に、このユースケースはリポジトリの特定の機能の wrapper にすぎず、エラーチェックを含んでいません.
In the next chapter, we will discuss requests and responses, and the use case will become slightly more complicated.
次の章では、リクエストとレスポンスについて説明し、ユースケースは少し複雑になる。

The next thing you might notice is that I used a simple function.
次にお気づきかもしれないが、私はシンプルな関数を使っている。
In the first edition of this book I used a class for the use case, and thanks to the nudge of a couple of readers I started to question my choice, so I want to briefly discuss the options you have.
本書の初版では、ユースケースにクラスを使用したが、何人かの読者の後押しのおかげで、その選択に疑問を持ち始めた。

The use case represents the business logic, a process, which means that the simplest implementation you can have in a programming language is a function: some code that receives input arguments and returns output data.
**ユースケースはビジネス・ロジック、つまりプロセスを表している**。つまり、プログラミング言語でできる最も単純な実装は関数であり、入力引数を受け取って出力データを返すコードである. (数学的関数 = 純粋関数 = 関数型プログラミング...!!)
A class is however another option, as in essence it is a collection of variables and functions.
しかし、クラスは別の選択肢であり、要するに変数と関数の集まりである。
So, as in many other cases, the question is if you should use a function or a class, and my answer is that it depends on the degree of complexity of the algorithm that you are implementing.
だから、他の多くのケースと同じように、**関数を使うべきかクラスを使うべきかが問題になるのだが、私の答えは、実装するアルゴリズムの複雑さの度合いに依る**というものだ。

Your business logic might be complicated, and require the connection with several external systems, though, each one with a specific initialisation, while in this simple case I just pass in the repository.
あなたのビジネスロジックは複雑で、複数の外部システムとの接続を必要とするかもしれない。
So, in principle, I don't see anything wrong in using classes for use cases, should you need more structure for your algorithms, but be careful not to use them when a simpler solution (functions) can perform the same job, which is the mistake I made in the previous version of this code.
しかし、**よりシンプルなソリューション(関数)で同じことができるのに、クラスを使わないように注意**してほしい。
Remember that code has to be maintained, so the simpler it is, the better.
**コードはメンテナンスされなければならないので、シンプルであればあるほど良い**ということを覚えておいてほしい。

## The storage system ストレージシステム

During the development of the use case, we assumed it would receive an object that contains the data and exposes a `list` function.
ユースケースの開発では、データを含むオブジェクトを受け取り、リスト関数を公開することを想定していた.
This object is generally nicknamed "repository", being the source of information for the use case.
**このオブジェクトは一般的に"repository"という愛称で呼ばれ、ユースケースの情報源となる**.
It has nothing to do with the Git repository, though, so be careful not to mix the two nomenclatures.
Gitリポジトリとは何の関係もないので、2つの呼び方を混ぜないように注意してください。

The storage lives in the fourth layer of the clean architecture, the external systems.
**ストレージはクリーンなアーキテクチャーの第4層、外部システムにある**。
The elements in this layer are accessed by internal elements through an interface, which in Python just translates to exposing a given set of methods (in this case only list).
**このレイヤーの要素は、インターフェイスを通じて内部要素からアクセスされる**。インターフェイスとは、Pythonで言えば、与えられたメソッド群（この場合はリストのみ）を公開することである.
It is worth noting that the level of abstraction provided by a repository in a clean architecture is higher than that provided by an ORM in a framework or by a tool like SQLAlchemy.
クリーンアーキテクチャのリポジトリが提供する抽象化レベルは、フレームワークの ORM や SQLAlchemy のようなツールが提供する抽象化レベルよりも高いことは注目に値する.(repositoryの方がORMよりも抽象度が高い -> repository が interface で、ORM が実装の詳細のイメージ??)
The repository provides only the endpoints that the application needs, with an interface which is tailored to the specific business problems the application implements.
リポジトリは、**アプリケーションが必要とするエンドポイントのみ**を提供し、アプリケーションが実装する**特定のビジネス問題に合わせたインターフェースを持つ. (ORMを使って実装の詳細を書くみたいな...!!)**

To clarify the matter in terms of concrete technologies, SQLAlchemy is a wonderful tool to abstract the access to an SQL database, so the internal implementation of the repository could use it to access a PostgreSQL database, for example.
具体的な技術の観点から問題を明確にすると、SQLAlchemyはSQLデータベースへのアクセスを抽象化する素晴らしいツールです。したがって、**Repositoryの内部実装は、たとえばPostgreSQLデータベースにアクセスするためにSQLAlchemyを使うことができます**。(やっぱり、Repositoryの振る舞いを、ORMを使って実装の詳細を書くみたいな感じだった...!!)
But the external API of the layer is not that provided by SQLAlchemy.
しかし、レイヤの外部 API は SQLAlchemy が提供するものではありません。
The API is a reduced set of functions that the use cases call to get the data, and the internal implementation can use a wide range of solutions to achieve the same goal, from raw SQL queries to a complex system of remote calls through a RabbitMQ network.
APIは、ユースケースがデータを取得するために呼び出す関数の縮小されたセット(=特定のビジネス問題に合わせたInterface=endpointのみを公開...!)であり、内部実装は、生のSQLクエリからRabbitMQネットワークを介したリモートコールの複雑なシステムまで、同じ目標を達成するために幅広いソリューションを使用することができます。

A very important feature of the repository is that it can return domain models, and this is in line with what framework ORMs usually do.
**Repositoryの非常に重要な特徴は、Domain Modelを返すことができること**であり、これはフレームワークORMが通常行うことと一致している. (ほうほう...!)
The elements in the third layer have access to all the elements defined in the internal layers, which means that domain models and use cases can be called and used directly from the repository.
第3レイヤー(=External system もしくは Gateways. まあGatewaysはExternal systemsのInterfaceなので意味は同じ.)の要素は、内部レイヤーで定義されたすべての要素にアクセスできる。**つまり、ドメインモデルとユースケースは、リポジトリから直接呼び出して使用できる**.

For the sake of this simple example, we will not deploy and use a real database system.
この簡単な例では、実際のデータベースシステムを導入して使用することはしない.
Given what we said, we are free to implement the repository with the system that better suits our needs, and in this case I want to keep everything simple.
私たちが言ったことを考えれば、私たちのニーズにより適したシステムでリポジトリを実装するのは自由であり、今回はすべてをシンプルに保ちたい。
We will thus create a very simple in-memory storage system loaded with some predefined data.
こうして、いくつかの定義済みデータをロードした非常にシンプルなインメモリー・ストレージ・システムを作成する.

The first thing to do is to write some tests that document the public API of the repository.
最初にすべきことは、リポジトリの公開APIを文書化するテストをいくつか書くことです。
The file containing the tests is tests/repository/test_memrepo.py.
テストを含むファイルは tests/repository/test_memrepo.py です。

```python
import pytest

from rentomatic.domain.room import Room
from rentomatic.repository.memrepo import MemRepo


@pytest.fixture
def room_dicts():
    return [
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


def test_repository_list_without_parameters(room_dicts):
    repo = MemRepo(room_dicts)

    rooms = [Room.from_dict(i) for i in room_dicts]

    assert repo.list() == rooms
```

In this case, we need a single test that checks the behaviour of the method `list`.
この場合、`list` method の振る舞いをチェックする単一のテストが必要だ.
The implementation that passes the test goes in the file rentomatic/repository/memrepo.py
テストに合格した実装は、rentomatic/repository/memrepo.pyにあります。

```python
from rentomatic.domain.room import Room


class MemRepo:
    def __init__(self, data):
        self.data = data

    def list(self):
        return [Room.from_dict(i) for i in self.data]
```

You can easily imagine this class being the wrapper around a real database or any other storage type.
この**Repository クラスが実際のデータベースやその他のストレージ・タイプの Wrapper になる**ことは容易に想像できる。
While the code might become more complex, its basic structure would remain the same, with a single public method list.
コードはより複雑になるかもしれないが、基本的な構造は変わらない.
I will dig into database repositories in a later chapter.
データベース・レポジトリについては、後の章で詳しく説明する。

## A command-line interface コマンドラインインターフェイス

So far we created the domain models, the serializers, the use cases and the repository, but we are still missing a system that glues everything together.
これまでのところ、Domain Model、Serializer、Use case、Repositoryを作成したが、すべてを統合するシステムがまだ欠けている.
This system has to get the call parameters from the user, initialise a use case with a repository, run the use case that fetches the domain models from the repository, and return them to the user.
このシステムは、ユーザから呼び出しパラメータを取得し、リポジトリでユースケースを初期化し、リポジトリからドメインモデルをフェッチするユースケースを実行し、ユーザにそれらを返さなければならない.(Controller的な??)
(=External Systemsに入るはず...!)

Let's see now how the architecture that we just created can interact with an external system like a CLI.
それでは、今作成したアーキテクチャが、CLIのような外部システムとどのように相互作用できるかを見てみよう.
The power of a clean architecture is that the external systems are pluggable, which means that we can defer the decision about the detail of the system we want to use.
クリーン・アーキテクチャーの威力は、外部システムがプラグイン可能であることで、つまり、使いたいシステムの詳細についての決定を先延ばしにできることだ。
In this case, we want to give the user an interface to query the system and to get a list of the rooms contained in the storage system, and the simplest choice is a command-line tool.
この場合、ユーザにシステムを照会し、ストレージシステムに含まれる部屋のリストを取得するためのインターフェイスを与えたいのだが、最も単純な選択肢はコマンドラインツールである。

Later we will create a REST endpoint and we will expose it through a Web server, and it will be clear why the architecture that we created is so powerful.
後で**RESTエンドポイントを作成し**、それをウェブ・サーバーを通して公開する.

For the time being, create a file cli.py in the same directory that contains setup.cfg.
とりあえず、setup.cfg を含む同じディレクトリに cli.py を作成します。
This is a simple Python script that doesn't need any specific option to run, as it just queries the storage for all the domain models contained there.
これはシンプルなPythonスクリプトで、実行するために特別なオプションは必要ありません。
The content of the file is the following
ファイルの内容は以下の通り。

```python
#!/usr/bin/env python

from rentomatic.repository.memrepo import MemRepo
from rentomatic.use_cases.room_list import room_list_use_case

repo = MemRepo([])
result = room_list_use_case(repo)

print(result)
```

You can execute this file with python cli.py or, if you prefer, run chmod +x cli.py (which makes it executable) and then run it with ./cli.py directly.
このファイルはpython cli.pyで実行することもできますし、chmod +x cli.py（実行可能にする）を実行し、./cli.pyで直接実行することもできます。
The expected result is an empty list
期待される結果は空リスト

```
$ ./cli.py
[]
```

which is correct as the class MemRepo in the file cli.py has been initialised with an empty list.
cli.pyのMemRepoクラスは空のリストで初期化されているので、これは正しいです。
The simple in-memory storage that we use has no persistence, so every time we create it we have to load some data in it.
我々が使用している単純なインメモリ・ストレージには永続性がないため、作成するたびにデータをロードしなければならない。
This has been done to keep the storage layer simple, but keep in mind that if the storage was a proper database this part of the code would connect to it but there would be no need to load data in it.
これはストレージ・レイヤーをシンプルに保つためだが、もしストレージが適切なデータベースであれば、コードのこの部分はそれに接続するが、データをロードする必要はないことを覚えておいてほしい。

The most important part of the script is
スクリプトの最も重要な部分は

```python
repo = MemRepo([])
result = room_list_use_case(repo)
```

which initialises the repository and runs the use case.
**リポジトリを初期化し、ユースケースを実行します**。
This is in general how you end up using your clean architecture and whatever external system you will plug into it.
これは一般的に、クリーンなアーキテクチャと、それに接続するExternal Systemsをどのように使うかということだ。
You initialise other systems, run the use case passing the interfaces, and you collect the results.
**他のシステムを初期化し、インターフェースを渡してユースケースを実行し、結果を収集する。**

For the sake of demonstration, let's define some data in the file and load them in the repository
デモンストレーションのために、ファイルにいくつかのデータを定義し、それをリポジトリにロードしてみましょう。

```python
#!/usr/bin/env python

from rentomatic.repository.memrepo import MemRepo
from rentomatic.use_cases.room_list import room_list_use_case

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

repo = MemRepo(rooms)
result = room_list_use_case(repo)

print([room.to_dict() for room in result])
```

Again, remember that we need to hardcode data due to the trivial nature of our storage, and not to the architecture of the system.
繰り返しになるが、私たちがデータをハードコードする必要があるのは、ストレージの些細な性質のためであり、システムのアーキテクチャのためではないことを覚えておいてほしい。
Note that I changed the instruction print as the repository returns domain models and printing them would result in a list of strings like `<rentomatic.domain.room.Room object at 0x7fb815ec04e0>`, which is not really helpful.
リポジトリがドメイン モデルを返すため、それらを印刷すると `<rentomatic.domain.room.Room object at 0x7fb815ec04e0>` のような文字列のリストになり、あまり役に立たないので、印刷命令を変更しました。

If you run the command line tool now, you will get a richer result than before
今コマンドラインツールを実行すると、以前よりも豊かな結果が得られるだろう。

Please note that I formatted the output above to be more readable, but the actual output will be on a single line.
上の出力は読みやすいように書式を整えましたが、実際の出力は1行になることに注意してください。

What we saw in this chapter is the core of the clean architecture in action.
この章で見たのは、**クリーン・アーキテクチャーの核心部分**である。

We explored the standard layers of entities (the class Room), use cases (the function room_list_use_case), gateways and external systems (the class MemRepo) and we could start to appreciate the advantages of their separation into layers.
**私たちは、Entities(`Room`クラス)、Usecase（`room_list_use_case`関数）、Gateways(RepositoryクラスのInterfaceがココに来るはず)、External Systems( `MemRepo`クラス)の標準的なレイヤーを探索し、レイヤーに分離することの利点を理解し始めた**.

Arguably, what we designed is very limited, which is why I will dedicate the rest of the book to showing how to enhance what we have to deal with more complicated cases.
そのため、本書の残りの部分を、**より複雑なケースに対応するための強化方法を紹**介することに割く。
We will discuss a Web interface in chapter 4, a richer query language and error management in chapter 5, and the integration with real external systems like databases in chapters 6, 7, and 8.
第4章ではWeb Interface について、第5章ではより豊富なクエリ言語とエラー管理について、第6章、第7章、第8章ではデータベースのような実際の外部システムとの統合について述べる. 
