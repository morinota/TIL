# 1. chapter 2: Repository Pattern

コアロジックをインフラから切り離す方法として、**dependency inversion principle(依存関係の逆転原理)**を使う.

データストレージを単純化し、モデル層をデータ層から切り離すことを可能にするRepositoryパターンを紹介.
この単純化された抽象化によって、データベースの複雑さを隠すことができ、システムがよりテストしやすくなることを具体例で紹介.

図2-1は、これから作るもの=「**ドメインモデルとデータベースの間に位置する** `Repository` オブジェクト」のプレビューである.

![Figure 2-1. Before and after the Repository pattern](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0201.png)

## 1.1. Persisting Our Domain Model ドメインモデルを持続させる

第1章では、注文(オーダー)を在庫のバッチに割り当てることができるシンプルなドメインモデルを作成した.

このコードに対してテストを書くのは簡単! => **依存関係や設定するインフラがない**から!!
(データベースや API を動かしてテストデータを作成する必要があるなら、 テストを書いたり維持したりするのはもっと大変になる)

悲しいことに、必ずある時点で、私たちの完璧な小さなモデルをユーザーの手に渡して現実世界とのUIを作る必要がある.
次の数章(二章 ~ )では、「**理想化されたDomain Modelを外部の状態にどのように接続するか**」を考えていく.

例題の場合は、Web APIになる.

## 1.2. Some Pseudocode: What Are We Going to Need? いくつかの疑似コード 何が必要なのか？

最初のAPIエンドポイントを構築するとき、多かれ少なかれ以下のようなコード(疑似コード)が必要である事がわかっている.最初のAPIエンドポイントはどのようなものになるだろうか.
(API endpoint: APIが提供するサービスへアクセスする為のURL. クライアントはendpointに対してHTTPリクエストを送信し、応答としてデータを受け取る)

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

## 1.3. Applying the DIP to Data Access DIPをデータアクセスに適用する

introで述べたように、レイヤーアーキテクチャは、UI、いくつかのロジック、データベースを持つシステムを構成する一般的なアプローチである（図2-2参照）。

![Figure 2-2. Layered architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0202.png)

目的は、レイヤーを分離し (これは良いことです)、各レイヤーがその下のレイヤーにのみ依存するようにする事.
しかし、**Domain Modelには一切の依存性を持たせたくない**.
インフラの懸念がドメインモデルに影響を及ぼし、ユニットテストや変更に時間がかかるようでは困る.

その代わり、冒頭で述べたように、**モデルは「内側」にあり、データベースレイヤーとプレゼンテーションレイヤーとの依存関係はその内側(=モデル)に流れこんでいる**と考えることにします。これは、**オニオンアーキテクチャ**と呼ばれることもあります（図2-3参照）。

![Figure 2-3. Onion architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0203.png)

### 1.3.1. NOTE: Port? Adapters?

アーキテクチャーパターンについて読んでいると、こんな疑問が湧いてくるかもしれない.

## 1.4. 例題におけるドメインモデルのリマインド

allocation(割り当て)とは`OrderLine` を `Batch` にリンクさせる概念.
アロケーションは `Batch` オブジェクトのコレクションとして保存される.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0103.png)

これをリレーショナルデータベースに置き換えるとどうなるか.

### 1.4.1. The “Normal” ORM Way: Model Depends on ORM "普通の "ORMの方法。 モデルはORMに依存する

最近、チームメンバーが自分でSQLクエリを作成することはほとんどない. その代わりに、**モデルオブジェクトを基にSQLを生成するフレームワーク**を使用していることが多い.

これらのフレームワークは、オブジェクトとドメインモデリングの世界と、データベースとリレーショナル代数の世界の間の概念のギャップを埋めるために存在するため、**object-relational mappers（ORM）**と呼ばれる.

これは、特定のデータベース技術に直接依存することなく、ドメインをきれいに保つのに役立つ.

しかし、典型的なSQLAlchemyのチュートリアルに従うと、次のようにDomain ModelがORM に依存してしまう...

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

SQLAlchemyを理解しなくても、例題のDomain ModelがORMへの依存でいっぱいになり、さらに地獄のように醜くなり始めていることがわかる. このDomain Modelは本当にデータベースを無視している(Domain Model -> DBの依存関係がない)と言えるだろうか...？
(i.e Domain Modelの定義に、SQLAlchemyのクラスを参照してしまっている...!!)

django の ORMは基本的に同じだが、より制限的.

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

Djangoの例でも言いたい事は同じで、モデルクラスは ORM クラスを直接継承しているので、**ドメインモデルがORM に依存している状態**である. オニオンアーキテクチャではその逆を望んでいる.

### 1.4.2. Inverting the Dependency: ORM Depends on Model 依存関係を逆転させる. ORMはモデルに依存させる.

さて、ありがたいことに、上の例だけが SQLAlchemy を使う唯一の方法ではない.

スキーマを別に定義し、**スキーマとドメインモデルの間の変換を行う明示的なマッパー(=mappingを管理するオブジェクト)**を定義する方法もある(SQLAlchemy では古典的マッピングと呼んでいる).

SQLAlchemyの`Table`オブジェクトを用いた明示的なORMマッピング(orm.py)

```python
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Column, Integer, MetaData, String, Table

import model  # 1. ORMはドメインモデルをインポートする（あるいは「依存する」あるいは「知っている」）のであって、その逆ではない.


metadata = MetaData()

order_lines = Table(  # 2.SQLAlchemy の抽象化機能を使って、データベースのテーブルとカラムを定義する.
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

...

def start_mappers(): # 3.マッパー関数を呼び出すと、SQLAlchemy はドメインモデルクラスを定義された様々なテーブルにバインド(接続)する.
    lines_mapper = mapper(model.OrderLine, order_lines)  3
```

最終的には、`start_mappers` を呼び出せば、**Domain Modelインスタンスを簡単にデータベースからロード**したり、**データベースへ保存**したりできるようになる. この関数を呼ばなければ、ドメインモデルクラスはデータベースを意識することなく、至ってシンプルなまま.

上述した設計方法によって、SQLAlchemy のすべての利点、たとえばマイグレーションに `alembic` を使えたり、これから説明するように、Domainクラスを使って透過的にクエリを実行できたりするようになる.

また、最初にORMの設定を構築しようとするとき、次の例のようにテストを書いておくと便利.

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

ここで`session`引数はpytest.fixtureで定義する. (テストのための共通の依存関係を"fixture"として定義している). この場合のsessionはSQLAlchemy データベースセッション.

まもなくわかるように、**ORM とDomain Modelの依存関係を逆転させる**というステップを踏めば、 repository patternという別の抽象化を実装するのは、ほんの少しの追加ステップに過ぎない.
それに対するテストを書くのはより簡単になり、 テストにおいて後でフェイクアウトするためのシンプルなインターフェイスを提供することができる.

我々はすでに、伝統的な依存関係を逆転させるという目的を達成しました。domain modelは"pure"なままであり、インフラの懸念から解放されたまま. 仮にSQLAlchemyを捨てて、別のORMや、まったく別の永続化システムを使っても、**ドメインモデルはまったく変わる必要がない**. (domain model -> ormへの依存関係がないから.)

この時点では、APIエンドポイントは次のようなもので、うまく動作させることができるかもしれない.
SQLAlchemyをAPIエンドポイントで直接使う

```python
@flask.route.gubbins
def allocate_endpoint():
    session = start_session()

    # extract order line from request
    # クライアントのリクエストからOrderLineを抽出する.
    line = OrderLine(
        request.json['orderid'],
        request.json['sku'],
        request.json['qty'],
    )

    # load all batches from the DB
    # 全てのバッチ在庫の情報をDBから読み込む
    batches = session.query(Batch).all()

    # call our domain service
    allocate(line, batches)

    # save the allocation back to the database
    session.commit()

    return 201
```

## 1.5. Introducing the Repository Pattern リポジトリパターンを導入する

**Repositoryパターン**は、persistent storage(永続記憶装置 = データを永続的に保存できる装置. ハードドライブ、NAS, クラウドストレージ, etc.)に対する抽象化(abstraction).
すべてのデータがメモリ上にあるかのように見せかけることで、データアクセスの退屈な詳細を隠す(?)

もし、ノートパソコンに無限のメモリがあれば、不器用なデータベースは必要ない.
好きなときに好きなオブジェクトを使うことができる. それはどのようなものだろうか？
どこからかデータを入手する必要がある.

```python
import all_my_data

def create_a_batch():
    batch = Batch(...)
    all_my_data.batches.add(batch)

def modify_a_batch(batch_id, new_quantity):
    batch = all_my_data.batches.get(batch_id)
    batch.change_initial_quantity(new_quantity)
```

オブジェクトはメモリ上にあるけれども、それをどこかに置いて、また見つけられるようにする必要がある.
メモリ内のデータでは、リストやセットのように新しいオブジェクトを追加することができる.
オブジェクトはメモリ上にあるので、.save()メソッドを呼び出す必要はなく、気になるオブジェクトをfetch(読み込み, ex. git fetch)してメモリ上で変更するだけでよい.

### 1.5.1. The Repository in the Abstract 抽象化の中のRepository

最も単純なリポジトリは，新しいアイテムをリポジトリに登録するための `add()` と，以前に登録されたアイテムを返すための `get()` の2つのメソッドを持つ.
この自制したシンプルさが、ドメインモデルとデータベースを結合させない為に重要.

```python
class AbstractRepository(abc.ABC):

    @abc.abstractmethod  1
    def add(self, batch: model.Batch):
        raise NotImplementedError  2

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError
```

ここで、

1. `@abc.abstractmethod` はPythonでABCを実際に「機能」させる唯一のものの1つ. **Pythonは「親クラスで定義されているすべての `abstractmethods`」達を実装していないクラスのインスタンスの作成を拒否**する.
2. `raise NotImplementedError` は良いだが、必要でも十分でもない. 実際、本当に必要であれば、abstract methodに、サブクラス(小クラス)が呼び出せるような処理(ex. 共通化した処理)を持たせることができる.

### 1.5.2. メモ: 抽象ベースクラス、ダックタイピング、プロトコル

- この本で抽象ベースクラスを使用しているのは、教則的な理由から. リポジトリの抽象化のインターフェイスが何であるかを説明するのに役立つ.
- しかし実際のところ、PythonはABCを無視するのが簡単すぎて、結局メンテナンスされず、最悪の場合誤解を招く. なので我々は、プロダクションコードからABCを削除してしまうことがある.
  実際には、私たちはしばしば、抽象化を可能にするためにPythonのアヒルの型付けに頼っている.
  Pythonistaにとって、リポジトリとは `add(thing)` と `get(id)` メソッドを持つあらゆるオブジェクトの事. (ダックタイピング = 抽象ベースクラスを定義しない事?)
- PEP544プロトコルを検討するのも一案です。 このプロトコルでは、継承の可能性を排除した型付けを行うことができる??

### 1.5.3. What Is the Trade-Off? トレードオフとは？

この本でアーキテクチャ・パターンを紹介するときは、必ず「これで何が得られるのか？そして、その代償は何なのか？」を検討する.

通常、少なくとも抽象化のレイヤー(ex. `AbstractRepository`)を追加することになる.
全体として複雑さが軽減されることを期待しても、局所的には複雑さが増し、可動部品の数や継続的なメンテナンスという点で、コストが発生する.

もしDDDや依存関係の逆転の道を歩んでいるのであれば、Repositoryパターンはこの本の中で最も簡単な選択肢の一つになりうる.
このコードに関しては、SQLAlchemy の抽象化機能 (`session.query(Batch)`) を、私たちが設計した別のもの (`batches_repo.get`) に置き換えただけだが、このパターンを使うことで、SQLAlchemy の抽象化機能を、私たちが設計した別の抽象化機能 (`session.query(Batch)`) に置き換えることができる.

また、**RepositoryパターンはDDDの世界では非常に一般的なパターン**なので、JavaやC#の世界からPythonに来たプログラマーと共同作業をする場合、このパターンを認識できる可能性が高い.

![Figure 2-5. Repository pattern](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0205.png)

いつものように、まずはテストから始める.

オブジェクトを保存するためのリポジトリテスト(test_repository.py)

```python
def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)  # 1. ここでテストされているメソッド
    session.commit()  # 2. 我々は`.commit()` をリポジトリの外側に置き、呼び出し側の責任とする.
    # commit: allocation結果をデータベースに保存する処理.

    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )) # 3. 生SQLを使用して、正しいデータが保存されているかどうかを検証する.
    assert rows == [("batch1", "RUSTY-SOAPDISH", 100, None)]
```

次のテストでは、バッチやアロケーションの取得を行うので、より複雑なテストになる.

複雑なオブジェクトを取得するためのリポジトリテスト(test_repository.py)

```python
def insert_order_line(session):
    session.execute( # 1. これは読み込み側のテストなので、生のSQLは `repo.get()` が取得する為のデータを準備している.
        'INSERT INTO order_lines (orderid, sku, qty)'
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[orderline_id]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid="order1", sku="GENERIC-SOFA")
    )
    return orderline_id

def insert_batch(session, batch_id): # 1.
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
    assert retrieved.sku == expected.sku  # 4. 以下、reference属性以外の主要な属性も明示的にチェックする
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {  4
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
```

テストを参考にRepositoryクラスを実装する.

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

そしてRepositoryパターンを踏まえると、Flaskのエンドポイントは以下のような感じになる.

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

### 1.5.4. EXERCISE FOR THE READER

ORMを使わずにRepositoryパターンを実装してみましょう.

## 1.6. Building a Fake Repository for Tests Is Now Trivial! テスト用の偽リポジトリを作るのは簡単

ここで、Repositoryパターンの最大の利点の1つを紹介する.
セットを使った簡単な偽リポジトリ(repository.py)

```python
class FakeRepository(AbstractRepository):
    def __init__(self, batches: List[model.Batch]):
        self._batches = set(batches)

    def add(self, batch: model.Batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
```

**テストでFake Repositoryを使うのは本当に簡単**で、使いやすく、推論しやすいシンプルな抽象化されたものができた.

Fake Repository(test_api.py)の使用例

```python
fake_repo = FakeRepository([batch1, batch2, batch3])
```

### 1.6.1. tips

抽象化されたクラスの偽物を作ることは、設計のフィードバックを得るための優れた方法.
偽物を作るのが難しい場合は、その抽象化が複雑すぎるという事である.

## 1.7. What Is a Port and What Is an Adapter, in Python? Pythonにおけるポート、アダプタとは？

ここであまり専門用語にこだわらないのは、私たちが注目したいのはあくまで**dependency inversion(依存関係の逆転)**であり、使用する技法の具体的な内容はあまり重要でないからである.
また、人によって微妙に異なる定義を使っているから.

Port(ポート)やAdapter(アダプタ)は**OO(Object Oriented, オブジェクト指向)**の世界から生まれた概念で、私たちが抱いている定義は以下.

- Port(ポート) : アプリケーションと抽象化したいものとの間のインタフェース.
- Adapter(アダプタ) : そのインタフェース(=Port?)や抽象化の背後にある実装.

Pythonにはインターフェイスがないので、アダプタを特定するのは簡単ですが、ポートを定義するのは難しいかもしれない. もしabstract base class(抽象ベースクラス)を使っていれば、それがポートになる.

具体的には、本章では `AbstractRepository` がPort(ポート)、 `SqlAlchemyRepository` と `FakeRepository` がAdapter(アダプタ)となる。

## 1.8. まとめ

表2-1にRepositoryパターンと我々の永続性無視モデルの長所と短所を示す.

Repository pattern and persistence ignorance: the trade-offs
リポジトリパターンと永続性無視：トレードオフの関係

- Pros 長所
  - 永続記憶装置とドメインモデルとの間に簡単なインターフェイスを用意した.
  - **ドメインモデルをインフラストラクチャから完全に切り離した**ので、ユニットテスト用に偽バージョンのリポジトリを作成したり、異なるストレージソリューションを交換したりすることも簡単.
  - 永続化について考える前にドメインモデルを書いておくと、目の前のビジネス問題に集中することができる.もしアプローチを根本的に変えたくなったら、モデルの中でそれを行うことができ、外部キーやマイグレーションについて後で心配する必要はない.
  - データベースのスキーマは、オブジェクトとテーブルの対応付けを完全に制御できるため、実にシンプルなものとなっている.
- Cons 短所
  - マッピングを手作業で維持するには、余分な作業と余分なコードが必要.
  - 余計なレイヤーは常にメンテナンスコストを増加させ、**Repositoryパターンを見たことがないPythonプログラマーにとって「WTF(What the Fuck)要素」を追加する**ことになる.
  -

## 1.9. REPOSITORY PATTERN RECAP

- ORMに依存性の逆転を適用する.
- 私たちのドメインモデルは、インフラストラクチャの懸念から解放されるべき. したがって、**ORMはモデルをインポートすべき**であり、その逆はない.
- Repositoryパターンは、永続的なストレージに関するシンプルな抽象化.
- **Repositoryは、インメモリオブジェクトのコレクションのような錯覚**を与える. これにより、**テスト用の FakeRepository を作成**したり、コアアプリケーションを中断することなくインフラの基本的な詳細を入れ替えたりすることが簡単にできるようになる.
-

Flaskアプリは実際にどのようなものになるのでしょうか？
次回は、Service Layerパターンを紹介する.
