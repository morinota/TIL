# Chapter 6. Unit of Work Pattern 第6章 ユニットオブワークパターン

In this chapter we’ll introduce the final piece of the puzzle that ties together the Repository and Service Layer patterns: the Unit of Work pattern.
この章では、Repository Pattern と Service layer Pattern を結びつけるパズルの最後のピース、 **Unit of Work Pattern** を紹介する.

If the Repository pattern is our abstraction over the idea of persistent storage, the Unit of Work (UoW) pattern is our abstraction over the idea of atomic operations.
Repositoryパターンが永続的ストレージの概念を抽象化したものだとすれば、**Unit of Work（UoW）パターンはアトミック操作の概念を抽象化したもの**である.
It will allow us to finally and fully decouple our service layer from the data layer.
これにより、最終的に **Service Layer をデータ層から完全に切り離す**ことができる.

Figure 6-1 shows that, currently, a lot of communication occurs across the layers of our infrastructure: the API talks directly to the database layer to start a session, it talks to the repository layer to initialize `SQLAlchemyRepository`, and it talks to the service layer to ask it to allocate.
図 6-1 は、**現在、多くの通信がインフラストラクチャの層(=Repository Layerの事?)を越えて行われている**ことを示している. API はセッションを開始するためにデータベース層と直接対話し、`SQLAlchemyRepository` を初期化するためにRepository Layer と対話し、Service Layer に割り当てを依頼するために対話するのである.

TIP
ヒント

The code for this chapter is in the chapter_06_uow branch on GitHub:
この章のコードは、GitHubのchapter_06_uowブランチにあります。

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_06_uow
# or to code along, checkout Chapter 4:
git checkout chapter_04_service_layer
```

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0601.png)

Figure 6-2 shows our target state.
図6-2は、私たちの目標状態を示している.
The Flask API now does only two things: 
Flask APIは今、たった2つのことしかしていない：
- it initializes a unit of work, and it invokes a service. unit of work を初期化し、サービスを呼び出す.
- The service collaborates with the UoW (we like to think of the UoW as being part of the service layer), but neither the service function itself nor Flask now needs to talk directly to the database. サービスはUoWと連携しますが（**UoWをService Layer の一部と考えたい**）、**サービス関数自体もFlaskもデータベースと直接会話する必要はなくなった**.

And we’ll do it all using a lovely piece of Python syntax, a context manager.
そして、**Pythonの素敵な構文であるcontext manager(??)**を使って、全てを行う.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0602.png)

## The Unit of Work Collaborates with the Repository 

Let’s see the unit of work (or UoW, which we pronounce “you-wow”) in action.
それでは、**unit of work（UoW、私たちは“you-wow”と発音しています）**を実際に見てみよう.
Here’s how the service layer will look when we’re finished:
サービスレイヤーが完成したら、こんな感じになる.

Preview of unit of work in action (src/allocation/service_layer/services.py)

```python
def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow: 1 
        batches = uow.batches.list()  2
        ...
        batchref = model.allocate(line, batches)
        uow.commit()  3
```

1. We’ll start a UoW as a context manager. コンテキストマネージャーとしてUoWを起動する.
2. `uow.batches` is the batches repo, so the UoW provides us access to our permanent storage. `uow.batches` はバッチレポ(??)なので、UoWは私たちの恒久的なストレージへのアクセスを提供する.
3. When we’re done, we commit or roll back our work, using the UoW. 作業が終わったら、UoWを使ってコミットしたりロールバックしたりする.

The UoW acts as a single entrypoint to our persistent storage, and it keeps track of what objects were loaded and of the latest state.1
**UoWは、永続記憶装置への単一のエントリポイントとして機能**し、どのオブジェクトがロードされたか、最新の状態を記録する1.

This gives us three useful things:
これによって、3つの便利なことが得られる:

- A stable snapshot of the database to work with, so the objects we use aren’t changing halfway through an operation データベースの安定したスナップショットを使用する(=**定期的にDBの中身をメモリに取ってきておく事**??)ことで、**操作の途中で使用するオブジェクトが変更されることがない**. 
- A way to persist all of our changes at once, so if something goes wrong, we don’t end up in an inconsistent state すべての変更を一度に永続化できる方法.
- A simple API to our persistence concerns and a handy place to get a repository 永続化に関する簡単なAPIと、リポジトリを取得するための便利な場所である.

## Test-Driving a UoW with Integration Tests インテグレーションテストによるUoWのテストドライブ

Here are our integration tests for the UOW:
UOWの統合テストを紹介する.

A basic “round-trip” test for a UoW (tests/integration/test_uow.py)
UoWの基本的な「ラウンドトリップ」テスト（テスト

```python
def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory()
    insert_batch(session, 'batch1', 'HIPSTER-WORKBENCH', 100, None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)  1
    with uow:
        batch = uow.batches.get(reference='batch1')  2
        line = model.OrderLine('o1', 'HIPSTER-WORKBENCH', 10)
        batch.allocate(line)
        uow.commit()  3

    batchref = get_allocated_batch_ref(session, 'o1', 'HIPSTER-WORKBENCH')
    assert batchref == 'batch1'
```

1. We initialize the UoW by using our custom session factory and get back a uow object to use in our with block. custom session factory を使用してUoWを初期化し、withブロックで使用するuowオブジェクトを取得する.
2. The UoW gives us access to the batches repository via uow.batches. UoWは、`uow.batches`を介してバッチリポジトリにアクセスできるようにしてくれている.
3. We call commit() on it when we’re done. 完了したら、その上で`commit()`を呼び出す.

For the curious, the `insert_batch` and `get_allocated_batch_ref` helpers look like this:
興味深いことに、 `insert_batch` と `get_allocated_batch_ref` ヘルパーは次のようなもの: 

Helpers for doing SQL stuff (tests/integration/test_uow.py)
SQL を行うためのヘルパー (テスト)

```python
def insert_batch(session, ref, sku, qty, eta):
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta)'
        ' VALUES (:ref, :sku, :qty, :eta)',
        dict(ref=ref, sku=sku, qty=qty, eta=eta)
    )


def get_allocated_batch_ref(session, orderid, sku):
    [[orderlineid]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        dict(orderid=orderid, sku=sku)
    )
    [[batchref]] = session.execute(
        'SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id'
        ' WHERE orderline_id=:orderlineid',
        dict(orderlineid=orderlineid)
    )
    return batchref
```

## Unit of Work and Its Context Manager Unit of Work and Its Context Manager (仕事の単位とそのコンテキストマネージャー)

In our tests we’ve implicitly defined an interface for what a UoW needs to do.
このテストでは、**UoWが何をする必要があるのか**、暗黙のうちにインターフェースを定義している. 
Let’s make that explicit by using an abstract base class:
**abstract base クラス**を使って、それを**明示的に**してみよう.

Abstract UoW context manager (src/allocation/service_layer/unit_of_work.py)
抽象的な UoW コンテキストマネージャ

```python
class AbstractUnitOfWork(abc.ABC):
    batches: repository.AbstractRepository  1

    def __exit__(self, *args):  2
        self.rollback()  4

    @abc.abstractmethod
    def commit(self):  3
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):  4
        raise NotImplementedError
```

1. The UoW provides an attribute called `.batches`, which will give us access to the batches repository. UoWは `.batches` という属性を提供しており、この属性によってbatchesリポジトリにアクセスすることができます。

2. If you’ve never seen a context manager, `__enter__` and `__exit__` are the two magic methods that execute when we enter the `with` block and when we exit it, respectively. They’re our setup and teardown phases. コンテキストマネージャーを見たことがない人は、 `__enter__` と `__exit__` がそれぞれ `with` ブロックに入るときと出るときに実行される2つのマジックメソッドであることを確認してください。 これらはセットアップとティアダウンフェーズです。

3. We’ll call this method to explicitly commit our work when we’re ready. 準備ができたら、このメソッドを呼び出して、明示的に作業をコミットします。

4. If we don’t commit, or if we exit the context manager by raising an error, we do a rollback. (The rollback has no effect if `commit()` has been called. Read on for more discussion of this.) コミットしない場合、またはエラーを発生させてコンテキストマネージャを終了する場合、ロールバックを行う。 (ロールバックは `commit()` が呼び出された場合には何の効果もありません。 これについては続きを読んでください)。

### The Real Unit of Work Uses SQLAlchemy Sessions 本当の作業単位はSQLAlchemyのセッションを使用する

The main thing that our concrete implementation adds is the database session:
この具体的な実装が追加する主なものは、データベース・セッションです。

The real SQLAlchemy UoW (src
本物のSQLAlchemy UoW (src

```python
DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(  1
    config.get_postgres_uri(),
))

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory  1

    def __enter__(self):
        self.session = self.session_factory()  # type: Session  2
        self.batches = repository.SqlAlchemyRepository(self.session)  2
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  3

    def commit(self):  4
        self.session.commit()

    def rollback(self):  4
        self.session.rollback()
```

1. The module defines a default session factory that will connect to Postgres, but we allow that to be overridden in our integration tests so that we can use SQLite instead. このモジュールは Postgres に接続するデフォルトのセッションファクトリを定義していますが、統合テストではそれをオーバーライドして SQLite を代わりに使えるようにしています。

2. The `__enter__` method is responsible for starting a database session and instantiating a real repository that can use that session. enter__` メソッドは、データベースセッションを開始し、そのセッションを使用できる実際のリポジトリのインスタンスを作成する役割を担います。

3. We close the session on exit. 終了時にセッションを終了します。

4. Finally, we provide concrete `commit()` and `rollback()` methods that use our database session. 最後に、データベースセッションを使用する具体的な `commit()` と `rollback()` メソッドを提供します。

### Fake Unit of Work for Testing テストのための偽の作業単位

Here’s how we use a fake UoW in our service-layer tests:
ここでは、サービスレイヤーのテストに偽のUoWを使用する方法を説明します。

Fake UoW (tests
偽のUoW（テスト

```python
class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.batches = FakeRepository([])  1
        self.committed = False  2

    def commit(self):
        self.committed = True  2

    def rollback(self):
        pass



def test_add_batch():
    uow = FakeUnitOfWork()  3
    services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)  3
    assert uow.batches.get("b1") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()  3
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)  3
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)  3
    assert result == "batch1"
...
```

1. `FakeUnitOfWork` and `FakeRepository` are tightly coupled, just like the real `UnitofWork` and `Repository` classes. That’s fine because we recognize that the objects are collaborators. FakeUnitOfWork` と `FakeRepository` は、本物の `UnitofWork` と `Repository` クラスと同じように密に結合されています。 オブジェクトが共同作業者であることを認識しているので、それでいいのです。

2. Notice the similarity with the fake `commit()` function from `FakeSession` (which we can now get rid of). But it’s a substantial improvement because we’re now faking out code that we wrote rather than third-party code. Some people say, “Don’t mock what you don’t own”. FakeSession` の偽の `commit()` 関数と似ていることに注意してください (これはもう取り除くことができます)。 しかし、サードパーティのコードではなく、私たちが書いたコードをフェイクアウトしているので、実質的な改善と言えます。 自分のものでないものをモックにするな」と言う人がいます。

3. In our tests, we can instantiate a UoW and pass it to our service layer, rather than passing a repository and a session. This is considerably less cumbersome. 私たちのテストでは、リポジトリやセッションを渡すのではなく、UoWをインスタンス化してサービス層に渡すことができます。 これはかなり面倒なことではありません。

- DON’T MOCK WHAT YOU DON’T OWN 無い物ねだりはいけない

- Why do we feel more comfortable mocking the UoW than the session? Both of our fakes achieve the same thing: they give us a way to swap out our persistence layer so we can run tests in memory instead of needing to talk to a real database. The difference is in the resulting design. なぜ、セッションよりも UoW をモックするほうが快適なのでしょうか? どちらも同じことを実現します。永続化レイヤーを交換することで、 実際のデータベースと通信する必要がなくなり、 メモリ上でテストを実行できるようになるからです。 違いは、結果として得られるデザインにあります。

- If we cared only about writing tests that run quickly, we could create mocks that replace SQLAlchemy and use those throughout our codebase. The problem is that `Session` is a complex object that exposes lots of persistence-related functionality. It’s easy to use `Session` to make arbitrary queries against the database, but that quickly leads to data access code being sprinkled all over the codebase. To avoid that, we want to limit access to our persistence layer so each component has exactly what it needs and nothing more. もし速く走るテストを書くことだけを考えるなら、SQLAlchemy を置き換えるモックを作って、コードベース全体でそれを使うことができます。 問題は `Session` が複雑なオブジェクトで、多くの永続化関連の機能を公開していることです。 データベースに対して任意の問い合わせをするために `Session` を使うのは簡単ですが、そうするとデータアクセスのコードがコードベース全体に散らばってしまうことになります。 それを避けるために、永続化レイヤへのアクセスを制限して、各コンポーネントが必要なものだけを持つようにしたいのです。

- By coupling to the `Session` interface, you’re choosing to couple to all the complexity of SQLAlchemy. Instead, we want to choose a simpler abstraction and use that to clearly separate responsibilities. Our UoW is much simpler than a session, and we feel comfortable with the service layer being able to start and stop units of work. Session` インターフェースにカップリングすることは、SQLAlchemy の複雑な部分をすべてカップリングすることを選んでいることになります。 その代わりに、より単純な抽象化を選択し、それを使って責任を明確に分けたいと思います。 私たちの UoW はセッションよりもずっと単純で、サービス層が仕事の単位を開始したり停止したりできることに安心感を覚えます。

- “Don’t mock what you don’t own” is a rule of thumb that forces us to build these simple abstractions over messy subsystems. This has the same performance benefit as mocking the SQLAlchemy session but encourages us to think carefully about our designs. "Don't mock what you don't own" は経験則で、面倒なサブシステムの上に、このような単純な抽象化を構築することを強要します。 これは SQLAlchemy のセッションをモックするのと同じ性能上の利点がありますが、設計について注意深く考えることを促します。

## Using the UoW in the Service Layer サービスレイヤーでのUoWの活用

Here’s what our new service layer looks like:
新しいサービスレイヤーは、こんな感じです。

Service layer using UoW (src
UoWを利用したサービス層（src

```python
def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork  1
):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork  1
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref
```

1. Our service layer now has only the one dependency, once again on an abstract UoW. サービスレイヤーは1つの依存関係を持つだけで、またもや抽象的なUoWに依存する。

## Explicit Tests for Commit/Rollback Behavior コミットに対する明示的なテスト

To convince ourselves that the commit
コミットメントを納得させるために

Integration tests for rollback behavior (tests
ロールバック動作の統合テスト（テスト

```python
def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session, 'batch1', 'MEDIUM-PLINTH', 100, None)

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, 'batch1', 'LARGE-FORK', 100, None)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "batches"'))
    assert rows == []
```

- TIP ヒント

- We haven’t shown it here, but it can be worth testing some of the more “obscure” database behavior, like transactions, against the “real” database—that is, the same engine. For now, we’re getting away with using SQLite instead of Postgres, but in Chapter 7, we’ll switch some of the tests to using the real database. It’s convenient that our UoW class makes that easy! ここでは紹介しませんでしたが、トランザクションのような、より「不明瞭な」データベースの動作のいくつかを、「本当の」データベース、つまり同じエンジンに対してテストする価値があるかもしれません。 今のところ、Postgres の代わりに SQLite を使っていますが、第7章では、いくつかのテストを本物のデータベースを使うように変更します。 UoW のクラスはそれが簡単にできるのが便利ですね!

## Explicit Versus Implicit Commits 明示的コミットと暗黙的コミットの比較

Now we briefly digress on different ways of implementing the UoW pattern.
ここで、UoWパターンのさまざまな実装方法について簡単に触れておく。

We could imagine a slightly different version of the UoW that commits by default and rolls back only if it spots an exception:
デフォルトでコミットし、例外が見つかった場合のみロールバックするような、少し変わったバージョンのUoWを想像することもできます。

A UoW with implicit commit… (src
暗黙のコミットを持つUoW... (src)

```python
class AbstractUnitOfWork(abc.ABC):

    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()  1
        else:
            self.rollback()  2
```

1. Should we have an implicit commit in the happy path? ハッピーパスで暗黙のコミットをすべきなのか？

2. And roll back only on exception? そして、例外の時だけロールバック？

It would allow us to save a line of code and to remove the explicit commit from our client code:
これによって、1行のコードを節約し、クライアントコードから明示的なコミットを削除することができるようになるのです。

...would save us a line of code (src
...一行のコードを節約することができます（src

```python
def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], uow):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        # uow.commit()
```

This is a judgment call, but we tend to prefer requiring the explicit commit so that we have to choose when to flush state.
これは判断材料になりますが、私たちは状態をフラッシュするタイミングを選択するために、明示的なコミットを要求することを好む傾向にあります。

Although we use an extra line of code, this makes the software safe by default.
余分なコード行を使っていますが、これによってデフォルトで安全なソフトウェアになっています。
The default behavior is to not change anything.
デフォルトの動作は、何も変更しないことです。
In turn, that makes our code easier to reason about because there’s only one code path that leads to changes in the system: total success and an explicit commit.
なぜなら、システムの変更につながるコードパスはただ一つ、完全な成功と明示的なコミットだけだからです。
Any other code path, any exception, any early exit from the UoW’s scope leads to a safe state.
他のコードパス、例外、UoWのスコープからの早期終了はすべて安全な状態につながります。

Similarly, we prefer to roll back by default because it’s easier to understand; this rolls back to the last commit, so either the user did one, or we blow their changes away.
同様に、私たちはデフォルトでロールバックすることを好みます。その方が理解しやすいからです。これは最後のコミットまでロールバックするので、ユーザーが行ったか、あるいは私たちが彼らの変更を吹き飛ばしたかのどちらかです。
Harsh but simple.
厳しいですが、シンプルです。

## Examples: Using UoW to Group Multiple Operations into an Atomic Unit Examples: UoWを使用して複数の操作を原子単位にまとめる

Here are a few examples showing the Unit of Work pattern in use.
Unit of Workパターンを使用した例をいくつか紹介します。
You can see how it leads to simple reasoning about what blocks of code happen together.
どのようなコードのブロックが一緒に発生するのか、簡単な推論につながることがおわかりいただけると思います。

### Example 1: Reallocate 例1． 再割当

Suppose we want to be able to deallocate and then reallocate orders:
例えば、オーダーの割り当てを解除して、再度割り当てを行うことができるようにしたいとします。

Reallocate service function
サービス機能の再割り当て

```python
def reallocate(line: OrderLine, uow: AbstractUnitOfWork) -> str:
    with uow:
        batch = uow.batches.get(sku=line.sku)
        if batch is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batch.deallocate(line)  1
        allocate(line)  2
        uow.commit()
```

1. If `deallocate()` fails, we don’t want to call `allocate()`, obviously. もし `deallocate()` が失敗したら、当然 `allocate()` を呼び出したくはないですよね。

2. If `allocate()` fails, we probably don’t want to actually commit the `deallocate()` either. もし `allocate()` が失敗したら、おそらく `deallocate()` を実際にコミットすることもないでしょう。

### Example 2: Change Batch Quantity 例2：バッチ数量を変更する

Our shipping company gives us a call to say that one of the container doors opened, and half our sofas have fallen into the Indian Ocean.
コンテナの扉が開いて、ソファが半分ほどインド洋に落ちてしまったと、運送会社から連絡があったんです。
Oops!
あらら

Change quantity
変更量

```python
def change_batch_quantity(batchref: str, new_qty: int, uow: AbstractUnitOfWork):
    with uow:
        batch = uow.batches.get(reference=batchref)
        batch.change_purchased_quantity(new_qty)
        while batch.available_quantity < 0:
            line = batch.deallocate_one()  1
        uow.commit()
```

1. Here we may need to deallocate any number of lines. If we get a failure at any stage, we probably want to commit none of the changes. ここで、任意の数の行の割り当てを解除する必要があるかもしれません。 もしどこかの段階で失敗したら、おそらくその変更をコミットしないことになるでしょう。

## Tidying Up the Integration Tests 統合テストを片付ける

We now have three sets of tests, all essentially pointing at the database: test_orm.py, test_repository.py, and test_uow.py.
現在、3つのテストセットがあり、すべて基本的にデータベースを指しています: test_orm.py, test_repository.py, and test_uow.py.
Should we throw any away?
どれかを捨てるべきでしょうか？

```
└── tests
    ├── conftest.py
    ├── e2e
    │   └── test_api.py
    ├── integration
    │   ├── test_orm.py
    │   ├── test_repository.py
    │   └── test_uow.py
    ├── pytest.ini
    └── unit
        ├── test_allocate.py
        ├── test_batches.py
        └── test_services.py
```

You should always feel free to throw away tests if you think they’re not going to add value longer term.
もしテストが長期的に価値を持たないと思えば、いつでも自由に捨てることができます。
We’d say that test_orm.py was primarily a tool to help us learn SQLAlchemy, so we won’t need that long term, especially if the main things it’s doing are covered in test_repository.py.
test_orm.py は主に SQLAlchemy を学習するためのツールで、長期的には必要ないと思います。
That last test, you might keep around, but we could certainly see an argument for just keeping everything at the highest possible level of abstraction (just as we did for the unit tests).
最後のテストは残しておいてもいいかもしれませんが、（ユニットテストと同じように）可能な限り高い抽象度ですべてを維持するという議論もありえます。

- EXERCISE FOR THE READER 読書運動

- For this chapter, probably the best thing to try is to implement a UoW from scratch. The code, as always, is on GitHub. You could either follow the model we have quite closely, or perhaps experiment with separating the UoW (whose responsibilities are `commit()`, `rollback()`, and providing the `.batches` repository) from the context manager, whose job is to initialize things, and then do the commit or rollback on exit. If you feel like going all-functional rather than messing about with all these classes, you could use `@contextmanager` from contextlib. この章では、おそらくゼロからUoWを実装してみるのがベストでしょう。 コードはいつものようにGitHubにあります。 私たちのモデルに忠実に従うか、あるいは UoW (その責務は `commit()`, `rollback()` と `.batches` リポジトリの提供) をコンテキストマネージャ (その責務は初期化、終了時にコミットやロールバックを行う) から分離して実験してみるとよいでしょう。 もし、これらのクラスをいじくり回すよりも、全ての機能を使いたいのであれば、 contextlib の `@contextmanager` を使うことができます。

- We’ve stripped out both the actual UoW and the fakes, as well as paring back the abstract UoW. Why not send us a link to your repo if you come up with something you’re particularly proud of? 実際のUoWと偽物の両方を取り除き、また抽象的なUoWもパーにしました。 特に自慢できるものがあれば、あなたのレポにリンクを送ってみてはいかがでしょうか？

- TIP ヒント

- This is another example of the lesson from Chapter 5: as we build better abstractions, we can move our tests to run against them, which leaves us free to change the underlying details. これは、第5章で学んだことのもうひとつの例です。より優れた抽象概念を構築すれば、それに対してテストを実行することができるようになり、その結果、根本的な詳細を自由に変更することができるようになるのです。

## Wrap-Up まとめ

Hopefully we’ve convinced you that the Unit of Work pattern is useful, and that the context manager is a really nice Pythonic way of visually grouping code into blocks that we want to happen atomically.
うまくいけば、Unit of Workパターンが有用であること、そしてコンテキストマネージャはコードをアトミックに実行させたいブロックに視覚的にグループ化するための本当に素晴らしいPythonicな方法であることを納得してもらえたと思います。

This pattern is so useful, in fact, that SQLAlchemy already uses a UoW in the shape of the `Session` object.
このパターンはとても便利なので、実は SQLAlchemy はすでに `Session` オブジェクトの形をした UoW を使っています。
The `Session` object in SQLAlchemy is the way that your application loads data from the database.
SQLAlchemy の `Session` オブジェクトは、あなたのアプリケーションがデータベースからデータをロードする方法です。

Every time you load a new entity from the database, the session begins to track changes to the entity, and when the session is flushed, all your changes are persisted together.
データベースから新しいエンティティをロードするたびに、セッションはそのエンティ ティへの変更を追跡し始め、セッションがフラッシュされると、すべての変更が一緒に 保持されます。
Why do we go to the effort of abstracting away the SQLAlchemy session if it already implements the pattern we want?
SQLAlchemy のセッションは、すでに欲しいパターンを実装しているのに、なぜわざわざ 抽象化するのでしょうか？

Table 6-1 discusses some of the trade-offs.
表6-1では、トレードオフの関係について述べている。

Table 6-1.
表6-1.
Unit of Work pattern: the trade-offs
ユニットオブワークのパターン：トレードオフ

- Pros 長所

- We have a nice abstraction over the concept of atomic operations, and the context manager makes it easy to see, visually, what blocks of code are grouped together atomically. アトミック操作の概念を見事に抽象化し、コンテキスト・マネージャーによって、どのコードブロックがアトミックにグループ化されているかを視覚的に確認しやすくしています。

- We have explicit control over when a transaction starts and finishes, and our application fails in a way that is safe by default. We never have to worry that an operation is partially committed. トランザクションの開始と終了を明確に制御でき、アプリケーションはデフォルトで安全な方法で失敗します。 また、アプリケーションはデフォルトで安全な方法で失敗します。操作が部分的にコミットされることを心配する必要はありません。

- It’s a nice place to put all your repositories so client code can access them. これは、クライアントコードがアクセスできるように、すべてのリポジトリを置くのに適した場所です。

- As you’ll see in later chapters, atomicity isn’t only about transactions; it can help us work with events and the message bus. この後の章で説明するように、アトミック性はトランザクションだけでなく、イベントやメッセージバスを扱う際にも役立ちます。

- Cons 短所

- Your ORM probably already has some perfectly good abstractions around atomicity. SQLAlchemy even has context managers. You can go a long way just passing a session around. あなたのORMは、おそらくすでにアトミティに関する完璧な抽象化機能を備えています。 SQLAlchemyには、コンテキストマネージャまであります。 セッションを渡すだけで、ずいぶん遠くまで行くことができます。

- We’ve made it look easy, but you have to think quite carefully about things like rollbacks, multithreading, and nested transactions. Perhaps just sticking to what Django or Flask-SQLAlchemy gives you will keep your life simpler. 私たちは簡単に見えるようにしていますが、ロールバック、マルチスレッド、ネストされた トランザクションのようなものについて、かなり慎重に考えなければなりません。 おそらく、 Django や Flask-SQLAlchemy が与えてくれるものにこだわるだけで、あなたの人生をよりシンプルに保つことができるでしょう。

For one thing, the Session API is rich and supports operations that we don’t want or need in our domain.
一つには、セッションAPIは豊富で、私たちのドメインで必要としない操作をサポートしています。
Our `UnitOfWork` simplifies the session to its essential core: it can be started, committed, or thrown away.
私たちの `UnitOfWork` はセッションをその本質的なコアに単純化します：それは開始、コミット、または破棄することができます。

For another, we’re using the `UnitOfWork` to access our `Repository` objects.
もう一つは、`UnitOfWork` を使って `Repository` オブジェクトにアクセスしています。
This is a neat bit of developer usability that we couldn’t do with a plain SQLAlchemy `Session`.
これは、普通の SQLAlchemy の `Session` ではできない、開発者のためのちょっとした使い勝手の良さです。

- UNIT OF WORK PATTERN RECAP ユニット・ワーク・パターン・リキャップ

- The Unit of Work pattern is an abstraction around data integrity Unit of Workパターンは、データの整合性に関する抽象化です。

- It helps to enforce the consistency of our domain model, and improves performance, by letting us perform a single flush operation at the end of an operation. これは、ドメインモデルの一貫性を強化するのに役立ち、操作の最後にフラッシュ操作を1回実行することで、パフォーマンスを向上させることができます。

- It works closely with the Repository and Service Layer patterns リポジトリやサービスレイヤのパターンと密接に連携している

- The Unit of Work pattern completes our abstractions over data access by representing atomic updates. Each of our service-layer use cases runs in a single unit of work that succeeds or fails as a block. Unit of Workパターンは、アトミックな更新を表現することで、データアクセスに関する抽象化を完成させる。 サービスレイヤーのユースケースは、ブロックとして成功または失敗する1つのユニットオブワークで実行されます。

- This is a lovely case for a context manager これは、コンテキスト・マネージャーの素敵なケースです

- Context managers are an idiomatic way of defining scope in Python. We can use a context manager to automatically roll back our work at the end of a request, which means the system is safe by default. コンテキストマネージャーは、Pythonでスコープを定義する慣用的な方法です。 コンテキストマネージャーを使うことで、リクエストの終了時に自動的に作業をロールバックすることができます。つまり、デフォルトで安全なシステムになっているのです。

- SQLAlchemy already implements this pattern SQLAlchemy はすでにこのパターンを実装しています

- We introduce an even simpler abstraction over the SQLAlchemy `Session` object in order to “narrow” the interface between the ORM and our code. This helps to keep us loosely coupled. SQLAlchemy の `Session` オブジェクトをさらに単純に抽象化して、ORM と我々のコードの間のインターフェイスを「狭く」しています。 これは疎結合を維持するのに役立ちます。

Lastly, we’re motivated again by the dependency inversion principle: our service layer depends on a thin abstraction, and we attach a concrete implementation at the outside edge of the system.
最後に、私たちは依存関係逆転の原理によって、再び動機づけられています：私たちのサービス層は薄い抽象化に依存しており、システムの外側の端に具体的な実装を付けます。
This lines up nicely with SQLAlchemy’s own recommendations:
これは SQLAlchemy 自身が推奨していることとうまく一致しています。

> Keep the life cycle of the session (and usually the transaction) separate and external.
> セッション(および通常はトランザクション)のライフサイクルを分離し、外部に保つ。
The most comprehensive approach, recommended for more substantial applications, will try to keep the details of session, transaction, and exception management as far as possible from the details of the program doing its work.
最も包括的なアプローチは、より実質的なアプリケーションに推奨され、セッション、 トランザクション、例外管理の詳細を、仕事をするプログラムの詳細からできる限り 遠ざけようとします。
SQLALchemy “Session Basics” Documentation
SQLALchemy "セッションの基本" ドキュメント

1 You may have come across the use of the word collaborators to describe objects that work together to achieve a goal.
1 ある目標を達成するために協力し合うオブジェクトを表すのに、コラボレーターという言葉を使うのを目にしたことがあるかもしれません。
The unit of work and the repository are a great example of collaborators in the object-modeling sense.
作業単位やリポジトリは、オブジェクト・モデリング的な意味でのコラボレーターの好例と言えるでしょう。
In responsibility-driven design, clusters of objects that collaborate in their roles are called object neighborhoods, which is, in our professional opinion, totally adorable.
責任駆動設計では、それぞれの役割で協働するオブジェクトのクラスターをオブジェクト・ネイバーフッドと呼びますが、これは専門家の意見として、まったくもって可愛そうな話なのです。
