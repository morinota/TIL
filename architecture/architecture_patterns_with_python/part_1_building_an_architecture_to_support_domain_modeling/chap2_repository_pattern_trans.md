# 2. Repository Pattern 2. リポジトリパターン

It’s time to make good on our promise to use the dependency inversion principle as a way of decoupling our core logic from infrastructural concerns.
コアロジックをインフラから切り離す方法として、依存関係の逆転原理を使うという約束を実行する時が来たのです。

We’ll introduce the Repository pattern, a simplifying abstraction over data storage, allowing us to decouple our model layer from the data layer.
データストレージを単純化し、モデル層をデータ層から切り離すことを可能にするRepositoryパターンを紹介します。
We’ll present a concrete example of how this simplifying abstraction makes our system more testable by hiding the complexities of the database.
この単純化された抽象化によって、データベースの複雑さを隠すことができ、システムがよりテストしやすくなることを具体例で紹介します。

Figure 2-1 shows a little preview of what we’re going to build: a `Repository` object that sits between our domain model and the database.
図2-1は、これから作るもののプレビューです。ドメインモデルとデータベースの間に位置する `Repository` オブジェクトです。

![Figure 2-1. Before and after the Repository pattern](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0201.png)

The code for this chapter is in the chapter_02_repository branch on GitHub.
この章のコードは、GitHubのchapter_02_repositoryブランチにあります。

## Persisting Our Domain Model ドメインモデルを持続させる

In Chapter 1 we built a simple domain model that can allocate orders to batches of stock.
第1章では、注文を在庫のバッチに割り当てることができるシンプルなドメインモデルを作成しました。
It’s easy for us to write tests against this code because there aren’t any dependencies or infrastructure to set up.
このコードに対してテストを書くのは簡単です。なぜなら、依存関係や設定するインフラがないからです。
If we needed to run a database or an API and create test data, our tests would be harder to write and maintain.
もしデータベースや API を動かしてテストデータを作成する必要があるなら、 テストを書いたり維持したりするのはもっと大変になることでしょう。

Sadly, at some point we’ll need to put our perfect little model in the hands of users and contend with the real world of spreadsheets and web browsers and race conditions.
悲しいことに、ある時点で、私たちの完璧な小さなモデルをユーザーの手に渡して、スプレッドシートやウェブブラウザやレースコンディションの現実世界と闘う必要が出てくるのです。
For the next few chapters we’re going to look at how we can connect our idealized domain model to external state.
次の数章では、理想化されたドメインモデルを外部の状態にどのように接続するかを見ていきます。

We expect to be working in an agile manner, so our priority is to get to a minimum viable product as quickly as possible.
私たちはアジャイルで仕事をすることを想定しているので、できるだけ早く最小限の製品に仕上げることを優先しています。
In our case, that’s going to be a web API.
私たちの場合、それはWeb APIになります。
In a real project, you might dive straight in with some end-to-end tests and start plugging in a web framework, test-driving things outside-in.
実際のプロジェクトでは、エンドツーエンドのテストを行い、Webフレームワークを接続し、アウトサイドインのテストドライブを始めるかもしれません。

But we know that, no matter what, we’re going to need some form of persistent storage, and this is a textbook, so we can allow ourselves a tiny bit more bottom-up development and start to think about storage and databases.
しかし、何があっても何らかの永続的なストレージが必要なことは分かっていますし、これは教科書ですから、ほんの少しボトムアップの開発を許容して、ストレージやデータベースについて考え始めることができます。

## Some Pseudocode: What Are We Going to Need? いくつかの疑似コード 何が必要なのか？

When we build our first API endpoint, we know we’re going to have some code that looks more or less like the following.
最初のAPIエンドポイントを構築するとき、多かれ少なかれ以下のようなコードがあることは分かっている。

What our first API endpoint will look like
最初のAPIエンドポイントはどのようなものになるのでしょうか

```python
@flask.route.gubbins
def allocate_endpoint():
    # extract order line from request
    line = OrderLine(request.params, ...)
    # load all batches from the DB
    batches = ...
    # call our domain service
    allocate(line, batches)
    # then save the allocation back to the database somehow
    return 201
```

- NOTE 注

- We’ve used Flask because it’s lightweight, but you don’t need to be a Flask user to understand this book. In fact, we’ll show you how to make your choice of framework a minor detail. 軽量であることからFlaskを使用していますが、本書を理解するためにFlaskのユーザーである必要はありません。 むしろ、フレームワークの選択を些細なことにする方法を紹介します。

We’ll need a way to retrieve batch info from the database and instantiate our domain model objects from it, and we’ll also need a way of saving them back to the database.
データベースからバッチ情報を取得し、そこからドメインモデルオブジェクトをインスタンス化する方法と、データベースに保存する方法が必要です。

What?
え？
Oh, “gubbins” is a British word for “stuff.”
"gubbins "は英国語で "物 "だ
You can just ignore that.
それは無視していい
It’s pseudocode, OK?
これは擬似コードだ

## Applying the DIP to Data Access DIPをデータアクセスに適用する

As mentioned in the introduction, a layered architecture is a common approach to structuring a system that has a UI, some logic, and a database (see Figure 2-2).
冒頭で述べたように、レイヤーアーキテクチャは、UI、いくつかのロジック、データベースを持つシステムを構成する一般的なアプローチである（図2-2参照）。

![Figure 2-2. Layered architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0202.png)

Django’s Model-View-Template structure is closely related, as is Model-View-Controller (MVC).
Django の Model-View-Template 構造は、 Model-View-Controller (MVC) と同様に、密接に関連しています。
In any case, the aim is to keep the layers separate (which is a good thing), and to have each layer depend only on the one below it.
いずれにせよ、目的は、レイヤーを分離し (これは良いことです)、各レイヤーがその下のレイヤーにのみ依存するようにすることです。

But we want our domain model to have no dependencies whatsoever.1 We don’t want infrastructure concerns bleeding over into our domain model and slowing our unit tests or our ability to make changes.
しかし、ドメインモデルには一切の依存性を持たせたくない。1 インフラの懸念がドメインモデルに影響を及ぼし、ユニットテストや変更に時間がかかるようでは困るのである。

Instead, as discussed in the introduction, we’ll think of our model as being on the “inside,” and dependencies flowing inward to it; this is what people sometimes call onion architecture (see Figure 2-3).
その代わり、冒頭で述べたように、モデルは「内側」にあり、依存関係はその内側に流れていると考えることにします。これは、オニオンアーキテクチャと呼ばれることもあります（図2-3参照）。

![Figure 2-3. Onion architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0203.png)

- IS THIS PORTS AND ADAPTERS? は、ポートやアダプターのことでしょうか？

- If you’ve been reading about architectural patterns, you may be asking yourself questions like this: アーキテクチャーパターンについて読んでいると、こんな疑問が湧いてくるかもしれません。

- Is this ports and adapters? Or is it hexagonal architecture? Is that the same as onion architecture? What about the clean architecture? What’s a port, and what’s an adapter? Why do you people have so many words for the same thing? これはポートやアダプターでしょうか？ それともヘキサゴンアーキテクチャ？ オニオン・アーキテクチャと同じなのでしょうか？ クリーンアーキテクチャはどうなんだろう？ ポートってなんだ、アダプタってなんだ？ どうしてあなた方は同じものを表すのにたくさんの言葉を持っているのですか？

- Although some people like to nitpick over the differences, all these are pretty much names for the same thing, and they all boil down to the dependency inversion principle: high-level modules (the domain) should not depend on low-level ones (the infrastructure).2 その違いを指摘する人もいるが、これらはすべて同じものの名称であり、依存関係逆転の原則に帰結する。高位モジュール（ドメイン）は低位モジュール（インフラ）に依存すべきではない、ということだ2。

- We’ll get into some of the nitty-gritty around “depending on abstractions,” and whether there is a Pythonic equivalent of interfaces, later in the book. See also “What Is a Port and What Is an Adapter, in Python?”. 抽象化に依存する」あたりの細かい話や、インターフェイスに相当するものがPythonにあるかどうかについては、この本の後半で紹介する予定です。 Pythonにおけるポートとは何か、アダプタとは何か」も参照してください。

## Reminder: Our Model Reminder 当社モデル

Let’s remind ourselves of our domain model (see Figure 2-4): an allocation is the concept of linking an `OrderLine` to a `Batch`.
ドメインモデル (図 2-4 参照) を思い出してみましょう。アロケーションとは、 `OrderLine` を `Batch` にリンクさせる概念です。
We’re storing the allocations as a collection on our `Batch` object.
アロケーションは `Batch` オブジェクトのコレクションとして保存されます。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0103.png)

Let’s see how we might translate this to a relational database.
これをリレーショナルデータベースに置き換えるとどうなるか見てみよう。

### The “Normal” ORM Way: Model Depends on ORM "普通の "ORMの方法。 モデルはORMに依存する

These days, it’s unlikely that your team members are hand-rolling their own SQL queries.
最近、チームメンバーが自分でSQLクエリを作成することはほとんどありません。
Instead, you’re almost certainly using some kind of framework to generate SQL for you based on your model objects.
その代わりに、モデルオブジェクトを基にSQLを生成するフレームワークを使用していることがほとんどでしょう。

These frameworks are called object-relational mappers (ORMs) because they exist to bridge the conceptual gap between the world of objects and domain modeling and the world of databases and relational algebra.
これらのフレームワークは、オブジェクトとドメインモデリングの世界と、データベースとリレーショナル代数の世界の間の概念のギャップを埋めるために存在するため、オブジェクトリレーショナルマッパー（ORM）と呼ばれています。

The most important thing an ORM gives us is persistence ignorance: the idea that our fancy domain model doesn’t need to know anything about how data is loaded or persisted.
ORMが与えてくれる最も重要なものは、永続性の無視です。つまり、空想的なドメインモデルは、データの読み込みや永続化の方法について何も知る必要がないという考えです。
This helps keep our domain clean of direct dependencies on particular database technologies.3
これは、特定のデータベース技術に直接依存することなく、ドメインをきれいに保つのに役立ちます3。

But if you follow the typical SQLAlchemy tutorial, you’ll end up with something like this:
しかし、典型的なSQLAlchemyのチュートリアルに従うと、次のようなものができてしまいます。

SQLAlchemy “declarative” syntax, model depends on ORM (orm.py)
SQLAlchemy の "宣言的" 構文、モデルは ORM に依存する (orm.py)

```python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Order(Base):
    id = Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer(String(250))
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)

class Allocation(Base):
    ...
```

You don’t need to understand SQLAlchemy to see that our pristine model is now full of dependencies on the ORM and is starting to look ugly as hell besides.
SQLAlchemyを理解しなくても、私たちの原始的なモデルがORMへの依存でいっぱいになり、さらに地獄のように醜くなり始めていることがわかるでしょう。
Can we really say this model is ignorant of the database?
このモデルは本当にデータベースを無視していると言えるのでしょうか？
How can it be separate from storage concerns when our model properties are directly coupled to database columns?
モデルのプロパティがデータベースのカラムに直接結合されているのに、どうしてストレージの問題から切り離されるのでしょうか？

- DJANGO’S ORM IS ESSENTIALLY THE SAME, BUT MORE RESTRICTIVE django の orm は基本的に同じですが、より制限的です。

- If you’re more used to Django, the preceding “declarative” SQLAlchemy snippet translates to something like this: もしあなたが Django に慣れているなら、先の「宣言的な」 SQLAlchemy のスニペットは、次のように翻訳されます。

Django ORM example
Django ORM の例

```python
class Order(models.Model):
    pass

class OrderLine(models.Model):
    sku = models.CharField(max_length=255)
    qty = models.IntegerField()
    order = models.ForeignKey(Order)

class Allocation(models.Model):
    ...
```

- The point is the same—our model classes inherit directly from ORM classes, so our model depends on the ORM. We want it to be the other way around. ポイントは同じで、モデルクラスは ORM クラスを直接継承しているので、モデルは ORM に依存しています。 私たちはその逆を望んでいます。

- Django doesn’t provide an equivalent for SQLAlchemy’s classical mapper, but see Appendix D for examples of how to apply dependency inversion and the Repository pattern to Django. Django は SQLAlchemy の古典的なマッパーに相当するものを提供しませんが、 Django に依存性反転と Repository パターンを適用する例については、付録 D を参照してください。

### Inverting the Dependency: ORM Depends on Model 依存関係を逆転させる。 ORMはモデルに依存する

Well, thankfully, that’s not the only way to use SQLAlchemy.
さて、ありがたいことに、これだけが SQLAlchemy を使う唯一の方法ではありません。
The alternative is to define your schema separately, and to define an explicit mapper for how to convert between the schema and our domain model, what SQLAlchemy calls a classical mapping:
スキーマを別に定義し、スキーマとドメインモデルの間の変換を行う明示的なマッパーを定義する方法もあります（SQLAlchemy では古典的マッピングと呼んでいます）。

Explicit ORM mapping with SQLAlchemy Table objects (orm.py)
SQLAlchemyのテーブルオブジェクトを用いた明示的なORMマッピング(orm.py)

```python
from sqlalchemy.orm import mapper, relationship

import model  1


metadata = MetaData()

order_lines = Table(  2
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

...

def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)  3
```

1. The ORM imports (or “depends on” or “knows about”) the domain model, and not the other way around. ORMはドメインモデルをインポートする（あるいは「依存する」あるいは「知っている」）のであって、その逆ではない。

2. We define our database tables and columns by using SQLAlchemy’s abstractions.4 SQLAlchemy の抽象化機能を使って、データベースのテーブルとカラムを定義し ます4。

3. When we call the mapper function, SQLAlchemy does its magic to bind our domain model classes to the various tables we’ve defined. マッパー関数を呼び出すと、SQLAlchemy はドメインモデルクラスを定義された様々なテーブルにバインドする魔法をかけます。

The end result will be that, if we call `start_mappers`, we will be able to easily load and save domain model instances from and to the database.
最終的には、`start_mappers` を呼び出せば、ドメインモデルインスタンスを簡単にデータベースからロードしたり、データベースへ保存したりできるようになります。
But if we never call that function, our domain model classes stay blissfully unaware of the database.
しかし、もしこの関数を呼ばなければ、ドメインモデルクラスはデータベースを意識することなく、至ってシンプルなままです。

This gives us all the benefits of SQLAlchemy, including the ability to use `alembic` for migrations, and the ability to transparently query using our domain classes, as we’ll see.
これによって、SQLAlchemy のすべての利点、たとえばマイグレーションに `alembic` を使えたり、これから説明するように、ドメインクラスを使って透過的にクエリを実行できたりするようになります。

When you’re first trying to build your ORM config, it can be useful to write tests for it, as in the following example:
最初にORMの設定を構築しようとするとき、次の例のようにテストを書いておくと便利です。

Testing the ORM directly (throwaway tests) (test_orm.py)
ORMを直接テストする(捨て身のテスト) (test_orm.py)

```python
def test_orderline_mapper_can_load_lines(session):  1
    session.execute(
        'INSERT INTO order_lines (orderid, sku, qty) VALUES '
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
```

1. If you haven’t used pytest, the session argument to this test needs explaining. You don’t need to worry about the details of pytest or its fixtures for the purposes of this book, but the short explanation is that you can define common dependencies for your tests as “fixtures,” and pytest will inject them to the tests that need them by looking at their function arguments. In this case, it’s a SQLAlchemy database session. もしあなたがpytestを使ったことがないなら、このテストのsession引数について説明が必要です。 この本の目的のために pytest やそのフィクスチャの詳細を心配する必要はありませんが、簡単に説明すると、テストのための共通の依存関係を「フィクスチャ」として定義することができ、pytest はその関数の引数を見ることによって、それを必要とするテストに注入するということです。 この場合、それは SQLAlchemy データベースセッションです。

You probably wouldn’t keep these tests around—as you’ll see shortly, once you’ve taken the step of inverting the dependency of ORM and domain model, it’s only a small additional step to implement another abstraction called the Repository pattern, which will be easier to write tests against and will provide a simple interface for faking out later in tests.
まもなくわかるように、ORM とドメインモデルの依存関係を逆転させるというステップを踏めば、 リポジトリパターンという別の抽象化を実装するのはほんの少しの追加ステップに過ぎず、 それに対するテストを書くのはより簡単になり、 テストにおいて後でフェイクアウトするためのシンプルなインターフェイスを提供することができます。

But we’ve already achieved our objective of inverting the traditional dependency: the domain model stays “pure” and free from infrastructure concerns.
しかし、私たちはすでに、伝統的な依存関係を逆転させるという目的を達成しました。ドメインモデルは「純粋」なままであり、インフラの懸念から解放されたままです。
We could throw away SQLAlchemy and use a different ORM, or a totally different persistence system, and the domain model doesn’t need to change at all.
SQLAlchemyを捨てて、別のORMや、まったく別の永続化システムを使っても、ドメインモデルはまったく変わる必要がありません。

Depending on what you’re doing in your domain model, and especially if you stray far from the OO paradigm, you may find it increasingly hard to get the ORM to produce the exact behavior you need, and you may need to modify your domain model.5 As so often happens with architectural decisions, you’ll need to consider a trade-off.
ドメインモデルで何をしているかによりますが、特にOOパラダイムから大きく外れた場合、ORMに必要な動作を正確にさせることがますます難しくなり、ドメインモデルを修正する必要があるかもしれません。5 アーキテクチャの決定でよく起こるように、トレードオフを考慮する必要があるでしょう。
As the Zen of Python says, “Practicality beats purity!”
Pythonの禅が言うように、「実用性は純粋さに勝る！」のです。

At this point, though, our API endpoint might look something like the following, and we could get it to work just fine:
しかし、この時点では、APIエンドポイントは次のようなもので、うまく動作させることができるかもしれません。

Using SQLAlchemy directly in our API endpoint
SQLAlchemyをAPIエンドポイントで直接使う

```python
@flask.route.gubbins
def allocate_endpoint():
    session = start_session()

    # extract order line from request
    line = OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )

    # load all batches from the DB
    batches = session.query(Batch).all()

    # call our domain service
    allocate(line, batches)

    # save the allocation back to the database
    session.commit()

    return 201
```

## Introducing the Repository Pattern リポジトリパターンを導入する

The Repository pattern is an abstraction over persistent storage.
Repositoryパターンは、永続記憶装置に対する抽象化です。
It hides the boring details of data access by pretending that all of our data is in memory.
すべてのデータがメモリ上にあるかのように見せかけることで、データアクセスの退屈な詳細を隠します。

If we had infinite memory in our laptops, we’d have no need for clumsy databases.
もし、ノートパソコンに無限のメモリがあれば、不器用なデータベースは必要ない。
Instead, we could just use our objects whenever we liked.
その代わり、好きなときに好きなオブジェクトを使うことができる。
What would that look like?
それはどのようなものだろうか？

You have to get your data from somewhere
どこからかデータを入手する必要がある

```python
import all_my_data

def create_a_batch():
    batch = Batch(...)
    all_my_data.batches.add(batch)

def modify_a_batch(batch_id, new_quantity):
    batch = all_my_data.batches.get(batch_id)
    batch.change_initial_quantity(new_quantity)
```

Even though our objects are in memory, we need to put them somewhere so we can find them again.
オブジェクトはメモリ上にあるけれども、それをどこかに置いて、また見つけられるようにする必要がある。
Our in-memory data would let us add new objects, just like a list or a set.
メモリ内のデータでは、リストやセットのように新しいオブジェクトを追加することができます。
Because the objects are in memory, we never need to call a .save() method; we just fetch the object we care about and modify it in memory.
オブジェクトはメモリ上にあるので、.save()メソッドを呼び出す必要はなく、気になるオブジェクトをフェッチしてメモリ上で変更するだけでよい。

### The Repository in the Abstract 要約の中のリポジトリ

The simplest repository has just two methods: `add()` to put a new item in the repository, and `get()` to return a previously added item.6 We stick rigidly to using these methods for data access in our domain and our service layer.
最も単純なリポジトリは，新しいアイテムをリポジトリに登録するための `add()` と，以前に登録されたアイテムを返すための `get()` の2つのメソッドだけです6．
This self-imposed simplicity stops us from coupling our domain model to the database.
この自制したシンプルさが、ドメインモデルとデータベースを結合させないのです。

Here’s what an abstract base class (ABC) for our repository would look like:
リポジトリの抽象ベースクラス(ABC)はこんな感じです。

The simplest possible repository (repository.py)
最もシンプルなリポジトリ(repository.py)

```python
class AbstractRepository(abc.ABC):

    @abc.abstractmethod  1
    def add(self, batch: model.Batch):
        raise NotImplementedError  2

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
```

1. Python tip: `@abc.abstractmethod` is one of the only things that makes ABCs actually “work” in Python. Python will refuse to let you instantiate a class that does not implement all the `abstractmethods` defined in its parent class.7 Pythonのヒント： `@abc.abstractmethod` はPythonでABCを実際に「機能」させる唯一のものの1つです。 Pythonは親クラスで定義されているすべての `abstractmethods` を実装していないクラスのインスタンスを作成することを拒否します7。

2. `raise NotImplementedError` is nice, but it’s neither necessary nor sufficient. In fact, your abstract methods can have real behavior that subclasses can call out to, if you really want. 2. `raise NotImplementedError` は良いものですが、必要でも十分でもありません。 実際、本当に必要であれば、抽象的なメソッドに、サブクラスが呼び出せるような実際の振る舞いを持たせることができます。

- ABSTRACT BASE CLASSES, DUCK TYPING, AND PROTOCOLS 抽象ベースクラス、ダックタイピング、プロトコル

- We’re using abstract base classes in this book for didactic reasons: we hope they help explain what the interface of the repository abstraction is. この本で抽象的な基底クラスを使用しているのは、教則的な理由からです。リポジトリの抽象化のインターフェイスが何であるかを説明するのに役立つと期待しています。

- In real life, we’ve sometimes found ourselves deleting ABCs from our production code, because Python makes it too easy to ignore them, and they end up unmaintained and, at worst, misleading. In practice we often just rely on Python’s duck typing to enable abstractions. To a Pythonista, a repository is any object that has `add(thing)` and `get(id)` methods. 実際のところ、PythonはABCを無視するのが簡単すぎて、結局メンテナンスされず、最悪の場合誤解を招くので、私たちはプロダクションコードからABCを削除してしまうことがあります。 実際には、私たちはしばしば、抽象化を可能にするためにPythonのアヒルの型付けに頼っています。 Pythonistaにとって、リポジトリとは `add(thing)` と `get(id)` メソッドを持つあらゆるオブジェクトのことです。

- An alternative to look into is PEP 544 protocols. These give you typing without the possibility of inheritance, which “prefer composition over inheritance” fans will particularly like. PEP544プロトコルを検討するのも一案です。 このプロトコルでは、継承の可能性を排除した型付けを行うことができます。

### What Is the Trade-Off? トレードオフとは？

> You know they say economists know the price of everything and the value of nothing?
> 経済学者はあらゆるものの価格を知り、無の価値を知る、と言われるのをご存知でしょうか。
> Well, programmers know the benefits of everything and the trade-offs of nothing.
> プログラマーはあらゆるものの利点と、何もないところでのトレードオフを知っているんだ。
> Rich Hickey
> リッチ・ヒッキー

Whenever we introduce an architectural pattern in this book, we’ll always ask, “What do we get for this?
この本でアーキテクチャ・パターンを紹介するときは、必ず「これで何が得られるのか？
And what does it cost us?”
そして、その代償は何なのか？

Usually, at the very least, we’ll be introducing an extra layer of abstraction, and although we may hope it will reduce complexity overall, it does add complexity locally, and it has a cost in terms of the raw numbers of moving parts and ongoing maintenance.
通常、少なくとも抽象化のレイヤーを追加することになります。全体として複雑さが軽減されることを期待しても、局所的には複雑さが増し、可動部品の数や継続的なメンテナンスという点で、コストが発生します。

The Repository pattern is probably one of the easiest choices in the book, though, if you’re already heading down the DDD and dependency inversion route.
もしあなたが既にDDDや依存関係の逆転の道を歩んでいるのであれば、Repositoryパターンはこの本の中で最も簡単な選択肢の一つでしょう。
As far as our code is concerned, we’re really just swapping the SQLAlchemy abstraction (`session.query(Batch)`) for a different one (`batches_repo.get`) that we designed.
このコードに関しては、SQLAlchemy の抽象化機能 (`session.query(Batch)`) を、私たちが設計した別のもの (`batches_repo.get`) に置き換えただけなのですが、このパターンを使うことで、SQLAlchemy の抽象化機能を、私たちが設計した別の抽象化機能 (`session.query(Batch)`) に置き換えることができます。

We will have to write a few lines of code in our repository class each time we add a new domain object that we want to retrieve, but in return we get a simple abstraction over our storage layer, which we control.
取得したい新しいドメインオブジェクトを追加するたびに、リポジトリクラスに数行のコードを書かなければなりませんが、その見返りとして、私たちがコントロールするストレージ層上のシンプルな抽象化を得ることができます。
The Repository pattern would make it easy to make fundamental changes to the way we store things (see Appendix C), and as we’ll see, it is easy to fake out for unit tests.
リポジトリパターンを使えば、物事を保存する方法を根本的に変更することが容易になります（付録C参照）。また、これから見るように、ユニットテストのためにごまかすことも簡単です。

In addition, the Repository pattern is so common in the DDD world that, if you do collaborate with programmers who have come to Python from the Java and C# worlds, they’re likely to recognize it.
また、RepositoryパターンはDDDの世界では非常に一般的なパターンなので、JavaやC#の世界からPythonに来たプログラマーと共同作業をする場合、このパターンを認識できる可能性が高いです。
Figure 2-5 illustrates the pattern.
図2-5はそのパターンを示しています。

![Figure 2-5. Repository pattern](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0205.png)

As always, we start with a test.
いつものように、まずはテストから始めます。
This would probably be classified as an integration test, since we’re checking that our code (the repository) is correctly integrated with the database; hence, the tests tend to mix raw SQL with calls and assertions on our own code.
なぜなら、私たちのコード (リポジトリ) がデータベースと正しく統合されているかどうかをチェックしているからです。そのため、テストには生の SQL と私たち自身のコードの呼び出しやアサーションが混在する傾向があります。

- tip

- Unlike the ORM tests from earlier, these tests are good candidates for staying part of your codebase longer term, particularly if any parts of your domain model mean the object-relational map is nontrivial. 先ほどの ORM テストとは異なり、これらのテストはコードベースの一部として長期的に使用するのに適しています。特に、ドメインモデルの一部でオブジェクトリレーショナルマップが自明ではない場合です。

Repository test for saving an object (test_repository.py)
オブジェクトを保存するためのリポジトリテスト(test_repository.py)

```python
def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)  1
    session.commit()  2

    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'  3
    ))
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
```

1. `repo.add()` is the method under test here. `repo.add()` は、ここでテストされているメソッドです。

2. We keep the `.commit()` outside of the repository and make it the responsibility of the caller. There are pros and cons for this; some of our reasons will become clearer when we get to Chapter 6. 私たちは `.commit()` をリポジトリの外側に置き、呼び出し側の責任とします。 これには賛否両論あります。第6章に入ると、私たちの理由のいくつかが明らかになるでしょう。

3. We use the raw SQL to verify that the right data has been saved. 生SQLを使用して、正しいデータが保存されているかどうかを検証します。

The next test involves retrieving batches and allocations, so it’s more complex:
次のテストでは、バッチやアロケーションの取得を行うので、より複雑なテストになります。

Repository test for retrieving a complex object (test_repository.py)
複雑なオブジェクトを取得するためのリポジトリテスト(test_repository.py)

```python
def insert_order_line(session):
    session.execute(  1
        'INSERT INTO order_lines (orderid, sku, qty)'
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return orderline_id

def insert_batch(session, batch_id):  2
    ...

def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)  3

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference  3
    assert retrieved.sku == expected.sku  4
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {  4
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
```

1. This tests the read side, so the raw SQL is preparing data to be read by the `repo.get()`. これは読み込み側のテストなので、生のSQLは `repo.get()` が読み込むデータを準備していることになります。

2. We’ll spare you the details of `insert_batch` and `insert_allocation`; the point is to create a couple of batches, and, for the batch we’re interested in, to have one existing order line allocated to it. 重要なのは、いくつかのバッチを作成することと、興味のあるバッチに対して、既存のオーダーラインを1つ割り当てる事.

3. And that’s what we verify here. The first `assert ==` checks that the types match, and that the reference is the same (because, as you remember, `Batch` is an entity, and we have a custom `eq` for it). そしてこれがここで検証する内容です。 最初の `assert ==` は、型が一致していることと、参照が同じであることをチェックします（覚えているように、`Batch` はエンティティであり、それ用のカスタム `eq` があるからです）。

4. So we also explicitly check on its major attributes, including `._allocations`, which is a Python set of `OrderLine` value objects. そのため、 `._allocations` を含む主要な属性も明示的にチェックします。これは、Python の `OrderLine` 値オブジェクトのセットです。

Whether or not you painstakingly write tests for every model is a judgment call.
すべてのモデルに対して丹念にテストを書くかどうかは、判断の分かれるところです。
Once you have one class tested for create
一旦、1つのクラスがテストされると

You end up with something like this:
結局、こんな感じになるんですね。

A typical repository (repository.py)
典型的なリポジトリ(repository.py)です。

```python
class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
```

And now our Flask endpoint might look something like the following:
そして、Flaskのエンドポイントは以下のような感じになります。

Using our repository directly in our API endpoint
APIエンドポイントで直接リポジトリを使用する

```python
@flask.route.gubbins
def allocate_endpoint():
    batches = SqlAlchemyRepository.list()
    lines = [
        OrderLine(l['orderid'], l['sku'], l['qty'])
         for l in request.params...
    ]
    allocate(lines, batches)
    session.commit()
    return 201
```

- EXERCISE FOR THE READER 読書運動

- We bumped into a friend at a DDD conference the other day who said, “I haven’t used an ORM in 10 years.” The Repository pattern and an ORM both act as abstractions in front of raw SQL, so using one behind the other isn’t really necessary. Why not have a go at implementing our repository without using the ORM? You’ll find the code on GitHub. 先日、DDDのカンファレンスで、"もう10年もORMを使っていない "と言っている友人とばったり会いました。 リポジトリパターンとORMはどちらも生のSQLの前での抽象化として機能するので、どちらかを後ろに使うことはあまり必要ではありません。 ORMを使わずにリポジトリを実装してみるのはどうでしょう？ GitHubにコードがあります。

- We’ve left the repository tests, but figuring out what SQL to write is up to you. Perhaps it’ll be harder than you think; perhaps it’ll be easier. But the nice thing is, the rest of your application just doesn’t care. リポジトリのテストは残したが、どのようなSQLを書くかはあなた次第だ。 おそらくあなたが思っているより難しいでしょうし、簡単かもしれません。 しかし、良いことに、アプリケーションの残りの部分は気にしません。

## Building a Fake Repository for Tests Is Now Trivial! テスト用の偽リポジトリを作るのは簡単だ!

Here’s one of the biggest benefits of the Repository pattern:
ここで、Repositoryパターンの最大の利点の1つを紹介します。

A simple fake repository using a set (repository.py)
セットを使った簡単な偽リポジトリ(repository.py)

```python
class FakeRepository(AbstractRepository):

    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
```

Because it’s a simple wrapper around a set, all the methods are one-liners.
セットの単純なラッパーなので、すべてのメソッドはワンライナーです。

Using a fake repo in tests is really easy, and we have a simple abstraction that’s easy to use and reason about:
テストで偽のレポを使うのは本当に簡単で、使いやすく、推論しやすいシンプルな抽象化されたものができました。

Example usage of fake repository (test_api.py)
偽リポジトリ(test_api.py)の使用例

```python
fake_repo = FakeRepository([batch1, batch2, batch3])
```

You’ll see this fake in action in the next chapter.
このフェイクは次章で実際に見ていただきます。

- TIP ヒント

- Building fakes for your abstractions is an excellent way to get design feedback: if it’s hard to fake, the abstraction is probably too complicated. 抽象化のための偽物を作ることは、設計のフィードバックを得るための優れた方法です。偽物を作るのが難しい場合は、その抽象化が複雑すぎるのでしょう。

## What Is a Port and What Is an Adapter, in Python? Pythonにおけるポート、アダプタとは？

We don’t want to dwell on the terminology too much here because the main thing we want to focus on is dependency inversion, and the specifics of the technique you use don’t matter too much.
ここであまり専門用語にこだわらないのは、私たちが注目したいのは依存関係の逆転であり、使用する技法の具体的な内容はあまり重要でないからです。
Also, we’re aware that different people use slightly different definitions.
また、人によって微妙に異なる定義を使っていることも承知しています。

Ports and adapters came out of the OO world, and the definition we hold onto is that the port is the interface between our application and whatever it is we wish to abstract away, and the adapter is the implementation behind that interface or abstraction.
ポートやアダプタはOOの世界から生まれたもので、私たちが抱いている定義は、ポートはアプリケーションと抽象化したいものとの間のインタフェースであり、アダプタはそのインタフェースや抽象化の背後にある実装である、というものだ。

Now Python doesn’t have interfaces per se, so although it’s usually easy to identify an adapter, defining the port can be harder.
Pythonにはインターフェイスがないので、アダプタを特定するのは簡単ですが、ポートを定義するのは難しいかもしれません。
If you’re using an abstract base class, that’s the port.
もし抽象的な基底クラスを使っていれば、それがポートになります。
If not, the port is just the duck type that your adapters conform to and that your core application expects—the function and method names in use, and their argument names and types.
そうでない場合、ポートとは、アダプタが準拠し、コアアプリケーションが期待する関数名やメソッド名、引数名、型などのダックタイプに過ぎません。

Concretely, in this chapter, `AbstractRepository` is the port, and `SqlAlchemyRepository` and `FakeRepository` are the adapters.
具体的には、本章では `AbstractRepository` がポート、 `SqlAlchemyRepository` と `FakeRepository` がアダプタとなる。

## Wrap-Up まとめ

Bearing the Rich Hickey quote in mind, in each chapter we summarize the costs and benefits of each architectural pattern we introduce.
Rich Hickeyの言葉を念頭に置きながら、各章では、紹介する各アーキテクチャパターンのコストと利点をまとめています。
We want to be clear that we’re not saying every single application needs to be built this way; only sometimes does the complexity of the app and domain make it worth investing the time and effort in adding these extra layers of indirection.
私たちは、すべてのアプリケーションをこの方法で構築する必要があると言っているわけではないことを明確にしておきたいと思います。アプリケーションとドメインの複雑さによって、これらの余分なインダイレクトの層を追加するために時間と労力を投資する価値があるときだけです。

With that in mind, Table 2-1 shows some of the pros and cons of the Repository pattern and our persistence-ignorant model.
それを踏まえて、表2-1にRepositoryパターンと我々の永続性無視モデルの長所と短所を示します。

Table 2-1.
表2-1.
Repository pattern and persistence ignorance: the trade-offs
リポジトリパターンと永続性無視：トレードオフの関係

- Pros 長所

- We have a simple interface between persistent storage and our domain model. 永続記憶装置とドメインモデルとの間に簡単なインターフェイスを用意した。

- It’s easy to make a fake version of the repository for unit testing, or to swap out different storage solutions, because we’ve fully decoupled the model from infrastructure concerns. モデルをインフラストラクチャから完全に切り離したので、ユニットテスト用に偽バージョンのリポジトリを作成したり、異なるストレージソリューションを交換したりすることも簡単です。

- Writing the domain model before thinking about persistence helps us focus on the business problem at hand. If we ever want to radically change our approach, we can do that in our model, without needing to worry about foreign keys or migrations until later. 永続化について考える前にドメインモデルを書いておくと、目の前のビジネス問題に集中することができます。 もしアプローチを根本的に変えたくなったら、モデルの中でそれを行うことができ、外部キーやマイグレーションについて後で心配する必要はありません。

- Our database schema is really simple because we have complete control over how we map our objects to tables. データベースのスキーマは、オブジェクトとテーブルの対応付けを完全に制御できるため、実にシンプルなものとなっています。

- Cons 短所

- An ORM already buys you some decoupling. Changing foreign keys might be hard, but it should be pretty easy to swap between MySQL and Postgres if you ever need to. ORMは、すでにいくつかのデカップリングを提供しています。 外部キーの変更は難しいかもしれませんが、MySQLとPostgresの間で交換する必要がある場合は、かなり簡単にできるはずです。

- Maintaining ORM mappings by hand requires extra work and extra code. ORM マッピングを手作業で維持するには、余分な作業と余分なコードが必要です。

- Any extra layer of indirection always increases maintenance costs and adds a “WTF factor” for Python programmers who’ve never seen the Repository pattern before. 余計なレイヤーは常にメンテナンスコストを増加させ、Repositoryパターンを見たことがないPythonプログラマーにとって「WTF要素」を追加することになります。

Figure 2-6 shows the basic thesis: yes, for simple cases, a decoupled domain model is harder work than a simple ORM
図2-6に示すように、単純なケースでは、非結合ドメインモデルは単純なORMより大変な作業です。

- TIP ヒント

- If your app is just a simple CRUD (create-read-update-delete) wrapper around a database, then you don’t need a domain model or a repository. もしあなたのアプリが、データベースの周りの単純なCRUD（create-read-update-delete）ラッパーであれば、ドメインモデルやリポジトリは必要ありません。

But the more complex the domain, the more an investment in freeing yourself from infrastructure concerns will pay off in terms of the ease of making changes.
しかし、ドメインが複雑になればなるほど、インフラへの懸念から解放されるための投資は、変更のしやすさという点で高く評価されるでしょう。

![Figure 2-6. Domain model trade-offs as a diagram](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0206.png)

Our example code isn’t complex enough to give more than a hint of what the right-hand side of the graph looks like, but the hints are there.
このサンプルコードは、グラフの右側がどのように見えるかのヒント以上のものを与えるほど複雑ではありませんが、ヒントはそこにあります。
Imagine, for example, if we decide one day that we want to change allocations to live on the `OrderLine` instead of on the `Batch` object: if we were using Django, say, we’d have to define and think through the database migration before we could run any tests.
例えば、ある日アロケーションを `Batch` オブジェクトではなく `OrderLine` で行うようにしたいと考えたとします。もし Django を使っていたら、テストを実行する前にデータベースの移行を定義して考えなければならないでしょう。
As it is, because our model is just plain old Python objects, we can change a `set()` to being a new attribute, without needing to think about the database until later.
このように、我々のモデルは単なる古い Python オブジェクトなので、 `set()` を新しい属性に変更することで、データベースのことを後々まで考える必要がないのです。

- REPOSITORY PATTERN RECAP レポジトリパターン再録

- Apply dependency inversion to your ORM ORMに依存性の逆転を適用する

- Our domain model should be free of infrastructure concerns, so your ORM should import your model, and not the other way around. 私たちのドメインモデルは、インフラストラクチャの懸念から解放されるべきです。したがって、ORMはあなたのモデルをインポートすべきであり、その逆ではありません。

- The Repository pattern is a simple abstraction around permanent storage Repositoryパターンは、永続的なストレージに関するシンプルな抽象化です。

- The repository gives you the illusion of a collection of in-memory objects. It makes it easy to create a FakeRepository for testing and to swap fundamental details of your infrastructure without disrupting your core application. See Appendix C for an example. リポジトリは、インメモリオブジェクトのコレクションのような錯覚を与えます。 これにより、テスト用の FakeRepository を作成したり、コアアプリケーションを中断することなくインフラの基本的な詳細を入れ替えたりすることが簡単にできるようになります。 例については、付録Cを参照してください。

You’ll be wondering, how do we instantiate these repositories, fake or real?
これらのリポジトリをどのようにインスタンス化するのか、偽物なのか本物なのか、気になるところです。
What will our Flask app actually look like?
Flaskアプリは実際にどのようなものになるのでしょうか？
You’ll find out in the next exciting installment, the Service Layer pattern.
次回は、Service Layerパターンを紹介します。

But first, a brief digression.
その前に、簡単な余談を。

- 1 I suppose we mean “no stateful dependencies.” Depending on a helper library is fine; depending on an ORM or a web framework is not. 1 "ステートフルな依存性がない "という意味だろう。 ヘルパーライブラリに依存するのは良いが、ORMやWebフレームワークに依存するのは良くない。

- 2 Mark Seemann has an excellent blog post on the topic. 2 Mark Seemann氏のブログ記事が秀逸です。

- 3 In this sense, using an ORM is already an example of the DIP. Instead of depending on hardcoded SQL, we depend on an abstraction, the ORM. But that’s not enough for us—not in this book! 3 この意味で、ORMの使用はすでにDIPの一例です。 ハードコードされたSQLに依存する代わりに、ORMという抽象化されたものに依存するのです。 しかし、この本では、それだけでは十分ではありません。

- 4 Even in projects where we don’t use an ORM, we often use SQLAlchemy alongside Alembic to declaratively create schemas in Python and to manage migrations, connections, and sessions. 4 ORM を使わないプロジェクトでも、SQLAlchemy を Alembic と一緒に使って、Python で宣言的にスキーマを作成し、マイグレーション、接続、セッションを管理することがよくあります。

- 5 Shout-out to the amazingly helpful SQLAlchemy maintainers, and to Mike Bayer in particular. 5 驚くほど親切な SQLAlchemy のメンテナたち、特に Mike Bayer に感謝します。

- 6 You may be thinking, “What about list or delete or update?” However, in an ideal world, we modify our model objects one at a time, and delete is usually handled as a soft-delete—i.e., batch.cancel(). Finally, update is taken care of by the Unit of Work pattern, as you’ll see in Chapter 6. 6 "listやdeleteやupdateはどうするんだ？"と思われるかもしれません。 しかし、理想的な世界では、モデルオブジェクトを一度に一つずつ修正します。削除は通常、ソフト削除、つまり batch.cancel() として処理されます。 最後に、updateはUnit of Workパターンで処理されます（第6章を参照）。

- 7 To really reap the benefits of ABCs (such as they may be), be running helpers like pylint and mypy.

- 8 Diagram inspired by a post called “Global Complexity, Local Simplicity” by Rob Vens. 8 Rob Vens氏の「Global Complexity, Local Simplicity」という投稿に触発されて作成した図。
