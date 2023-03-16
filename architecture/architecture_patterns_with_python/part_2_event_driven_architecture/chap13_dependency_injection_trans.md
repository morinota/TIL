# chapter 13. Dependency Injection (And Bootstrapping) 第13章 依存性注入（とブートストラップ）。

Dependency injection (DI) is regarded with suspicion in the Python world.
Pythonの世界では、**Dependency injection(依存性注入, DI)**は疑惑の目で見られています.
And we’ve managed just fine without it so far in the example code for this book!.
そして、本書のサンプルコードでは、これまでそれを使わずにうまくやりくりしてきたのである!

In this chapter, we’ll explore some of the pain points in our code that lead us to consider using DI, and we’ll present some options for how to do it, leaving it to you to pick which you think is most Pythonic.
この章では、DIの利用を検討するきっかけとなったコードの問題点を探り、その方法についていくつかの選択肢を提示し、あなたが最もPythonicだと思うものを選んでもらう.

We’ll also add a new component to our architecture called bootstrap.py; it will be in charge of dependency injection, as well as some other initialization stuff that we often need.
また、**bootstrap.pyという新しいコンポーネントをアーキテクチャに追加する**. このコンポーネントは、 Dependency Injection や、よく必要とされるその他の初期化を担当する.
We’ll explain why this sort of thing is called a composition root in OO languages, and why bootstrap script is just fine for our purposes..
このようなものをOO言語では **composition root** と呼ぶが、なぜ**bootstrap スクリプト**が我々の目的にはちょうどいいのか、その理由を説明する.

Figure 13-1 shows what our app looks like without a bootstrapper: the entrypoints do a lot of initialization and passing around of our main dependency, the UoW..
図13-1は、bootstrapper を使わない場合のアプリの様子を示している.
エントリーポイントは、多くの初期化と主要な依存関係であるUoWの受け渡しを行う.

---.
---.

TIP.
TIP.

If you haven’t already, it’s worth reading Chapter 3 before continuing with this chapter, particularly the discussion of functional versus object-oriented dependency management..
この章を読み進める前に、第3章を読んでおくとよいでしょう. 特に、**関数型依存性管理(functional-oriented dependency managementF)とオブジェクト指向型依存性管理(object-oriented dependency management)の違い**について説明している.

---.
---.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1301.png)

---.
---.

TIP.
TIPです.

The code for this chapter is in the chapter_13_dependency_injection branch on GitHub:.
この章のコードはGitHub: の chapter_13_dependency_injection ブランチにあります。

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout chapter_13_dependency_injection
# or to code along, checkout the previous chapter:
git checkout chapter_12_cqrs
```

---.
---.

Figure 13-2 shows our bootstrapper taking over those responsibilities..
図13-2は、ブートストラッパーがこれらの責任を引き継いでいる様子を示している.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1302.png)

## Implicit Versus Explicit Dependencies Implicit Versus Explicit Dependencies (暗黙の依存と明示の依存).

Depending on your particular brain type, you may have a slight feeling of unease at the back of your mind at this point.
あなたの脳のタイプによっては、この時点で心の奥底にちょっとした不安を感じるかもしれない.
Let’s bring it out into the open.
表に出していきましょう.
We’ve shown you two ways of managing dependencies and testing them..
依存関係を管理し、テストする2つの方法を紹介した.

For our database dependency, we’ve built a careful framework of explicit dependencies and easy options for overriding them in tests.
データベースの依存関係については、明示的な依存関係と、テストでそれを上書きするための簡単なオプションという、慎重な枠組みを構築した.
Our main handler functions declare an explicit dependency on the UoW:.
私たちのメインハンドラ関数は、UoW:への明示的な依存を宣言している.

Our handlers have an explicit dependency on the UoW (src/allocation/service_layer/handlers.py).
私たちのハンドラは、UoWに明示的に依存している.(まあuowを引数にとってるから分かる...)

```python
def allocate(
        cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork
):
```

And that makes it easy to swap in a fake UoW in our service-layer tests:.
そのため、サービスレイヤーのテストでは、偽のUoWを簡単に入れ替えることがで着る:

Service-layer tests against a fake UoW: (tests/unit/test_services.py).
偽UoWに対するサービスレイヤーのテスト：（テスト

```python
    uow = FakeUnitOfWork()
    messagebus.handle([...], uow)
```

The UoW itself declares an explicit dependency on the session factory:.
UoW自身は、session factory:への依存を明示的に宣言している. (**explicit depencyを宣言している=>引数に取ってる...!!**)

The UoW depends on a session factory (src/allocation/service_layer/unit_of_work.py).
UoWは、セッションファクトリ（src）に依存している.

```python
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
        ...
```

We take advantage of it in our integration tests to be able to sometimes use SQLite instead of Postgres:.
私たちの統合テストでは、Postgres:の代わりにSQLiteを使用することができるように、この機能を活用している.

Integration tests against a different DB (tests/integration/test_uow.py).
異なるDBに対する統合テスト.

```python
def test_rolls_back_uncommitted_work_by_default(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)  1
```

1. Integration tests swap out the default Postgres session_factory for a SQLite one. 統合テストでは、デフォルトのPostgresのsession_factoryをSQLiteのsession_factoryに置き換えている.

## Aren’t Explicit Dependencies Totally Weird and Java-y? Explicit Dependencies Aren't Totally Weird and Java-y?

If you’re used to the way things normally happen in Python, you’ll be thinking all this is a bit weird.
Pythonで普通に物事が起こる方法に慣れていると、このすべてが少し奇妙に思えることだろう.
The standard way to do things is to declare our dependency implicitly by simply importing it, and then if we ever need to change it for tests, we can monkeypatch, as is Right and True in dynamic languages:.
標準的なやり方は、**インポートすることで暗黙のうちに依存関係を宣言**(=implicit dependencyの宣言はimport文なんだ...!!)し、テスト用に変更する必要がある場合は、動的言語におけるRight and Trueのように、monkeypatchで対応する.

Email sending as a normal import-based dependency (src/allocation/service_layer/handlers.py).
通常のインポートベースの依存関係としてのメール送信.

```python
from allocation.adapters import email, redis_eventpublisher  1
...

def send_out_of_stock_notification(
        event: events.OutOfStock, uow: unit_of_work.AbstractUnitOfWork,
):
    email.send(  2
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
```

1. Hardcoded import ハードコードされたimport文(=declaring implicit dependency...!)

2. Calls specific email sender directly 特定のメール送信者に直接連絡する.

Why pollute our application code with unnecessary arguments just for the sake of our tests? `mock.patch` makes monkeypatching nice and easy:.
テストのためだけに、不必要な引数でアプリケーションコードを汚すのはいかがなものでしょうか？mock.patch`を使えば、モンキーパッチ(?)を簡単に作成できる.

mock dot patch, thank you Michael Foord (tests/unit/test_handlers.py).

```python
    with mock.patch("allocation.adapters.email.send") as mock_send_mail:
        ...
```

The trouble is that we’ve made it look easy because our toy example doesn’t send real email (`email.send_mail` just does a `print`), but in real life, you’d end up having to call `mock.patch` for every single test that might cause an out-of-stock notification.
問題は、このおもちゃの例では実際のメールを送信しないので（`email.send_mail`は単に`print`を実行するだけ!）、簡単に見えるのですが、現実には、在庫切れの通知を引き起こすかもしれないテストごとに `mock.patch` を呼び出さなければならないことになってしまうという点である.
If you’ve worked on codebases with lots of mocks used to prevent unwanted side effects, you’ll know how annoying that mocky boilerplate gets..
**望まない副作用を防ぐためにモックを多用するコードベースで仕事をしたことがある人なら、モック的なボイラープレートがどれほど煩わしいかわかるだろう**.

And you’ll know that mocks tightly couple us to the implementation.
そして、モックは私たちと実装をしっかりと結びつけてくれる(?)ことがお分かりいただけると思う.
By choosing to monkeypatch `email.send_mail`, we are tied to doing `import email`, and if we ever want to do `from email import send_mail`, a trivial refactor, we’d have to change all our mocks..
email.send_mail`をmonkeypatchすることで、`import email`に縛られ、もし、`from email import send_mail`をしたい場合、些細なリファクターですが、モックを全て変更しなければならない.

So it’s a trade-off.
だから、トレードオフなんだ.
Yes, declaring explicit dependencies is unnecessary, strictly speaking, and using them would make our application code marginally more complex.
そうですね、**明示的な依存関係の宣言は厳密に言えば不要だし、それを使うとアプリケーションのコードがほんの少し複雑になるよね**.
But in return, we’d get tests that are easier to write and manage..
でも、**その代わり、書きやすく、管理しやすいテストが手に入る**.

On top of that, declaring an explicit dependency is an example of the dependency inversion principle—rather than having an (implicit) dependency on a specific detail, we have an (explicit) dependency on an abstraction:.
その上、明示的な依存関係を宣言することは、依存関係の逆転現象(**Dependency Inversion, SOLIDのD!!**)の一例である. 特定の詳細(ex. implementedクラス)に（暗黙の）依存するのではなく、抽象化(ex. interfaceクラス)に（明示的）依存するべきだ.

> **Explicit is better than implicit.**
> implicit より Explicit な方がいい＞。
> ---The Zen of Python.
> ---The Zen of Python.

The explicit dependency is more abstract (src/allocation/service_layer/handlers.py).
明示的な依存関係はより抽象的である.

```python
def send_out_of_stock_notification(
        event: events.OutOfStock, send_mail: Callable,
):
    send_mail(
        'stock@made.com',
        f'Out of stock for {event.sku}',
    )
```

But if we do change to declaring all these dependencies explicitly, who will inject them, and how? So far, we’ve really been dealing with only passing the UoW around: our tests use `FakeUnitOfWork`, while Flask and Redis eventconsumer entrypoints use the real UoW, and the message bus passes them onto our command handlers.
しかし、**もしこれらの依存関係をすべて明示的に宣言するように変更した場合**、誰がどのように注入(=引数として注入するって意味??)するのでしょうか？テストは `FakeUnitOfWork` を使い、Flask と Redis のイベントコンシューマエントリポイントは本物の UoW を使い、メッセージバスはそれらをコマンドハンドラに渡す.
If we add real and fake email classes, who will create them and pass them on?.
本物のメールクラスと偽物のメールクラスを追加した場合、誰がそれを作成し、伝えるのか.

That’s extra (duplicated) cruft for Flask, Redis, and our tests.
これは、Flask、Redis、そしてテストのための余分な（重複した）残骸である.
Moreover, putting all the responsibility for passing dependencies to the right handler onto the message bus feels like a violation of the SRP..
また、**依存関係を適切なハンドラに渡すための責任をすべてメッセージバスに押し付けるのは、SRP(=単一責任の原則, SOLIDのS=Single Reponsibility)に反するような気がする**.

Instead, we’ll reach for a pattern called Composition Root (a bootstrap script to you and me),1 and we’ll do a bit of “manual DI” (dependency injection without a framework).
その代わりに、**Composition Root(あなたと私のためのブートストラップスクリプト)というパターン**に手を伸ばし、**“manual DI” (フレームワークを使わない依存性注入)を少しやってみる**ことにしよう.
See Figure 13-3.2.
図13-3.2参照。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_1303.png)

## Preparing Handlers: Manual DI with Closures and Partials ハンドラーを準備する。クロージャとパーシャルを使った手動DI.

One way to turn a function with dependencies into one that’s ready to be called later with those dependencies already injected is to use closures or partial functions to compose the function with its dependencies:.
依存関係を持つ関数を、依存関係を注入(明示的に注入?)した状態で後で呼び出せるようにする方法の1つは、クロージャや部分関数を使って、関数とその依存関係を合成することである:

Examples of DI using closures or partial functions.
クロージャや部分関数を使ったDIの例.

```python
# existing allocate function, with abstract uow dependency
def allocate(
        cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork
):
    line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        ...

# bootstrap script prepares actual UoW

def bootstrap(..):
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    # prepare a version of the allocate fn with UoW dependency captured in a closure
    allocate_composed = lambda cmd: allocate(cmd, uow)

    # or, equivalently (this gets you a nicer stack trace)
    def allocate_composed(cmd):
        return allocate(cmd, uow)

    # alternatively with a partial
    import functools
    allocate_composed = functools.partial(allocate, uow=uow)  1

# later at runtime, we can call the partial function, and it will have
# the UoW already bound
allocate_composed(cmd)
```

1. The difference between closures (lambdas or named functions) and `functools.partial` is that the former use late binding of variables, which can be a source of confusion if any of the dependencies are mutable. クロージャ（ラムダや名前付き関数）と`functools.partial`の違いは、前者が変数の後期バインディングを使うことである(よくわからん...???)

Here’s the same pattern again for the `send_out_of_stock_notification()` handler, which has different dependencies:.
以下、同じパターンを `send_out_of_stock_notification()` ハンドラに対して再度示しますが、これは依存関係が異なる.

Another closure and partial functions example.
もう一つのクロージャと部分関数の例.

```python
def send_out_of_stock_notification(
        event: events.OutOfStock, send_mail: Callable,
):
    send_mail(
        'stock@made.com',
        ...


# prepare a version of the send_out_of_stock_notification with dependencies
sosn_composed  = lambda event: send_out_of_stock_notification(event, email.send_mail)

...
# later, at runtime:
sosn_composed(event)  # will have email.send_mail already injected in
```

## An Alternative Using Classes クラスを使った代替案

Closures and partial functions will feel familiar to people who’ve done a bit of functional programming.
**クロージャ(Closures)や部分関数(partial functions)**は、関数型プログラミングを少しやったことがある人には馴染み深いものだろう.(ふーん...なるほど??)
Here’s an alternative using classes, which may appeal to others.
ここでは、**クラスを使った代替案**を紹介しますが、これは他の人にもアピールできるかもしれない.
It requires rewriting all our handler functions as classes, though:.
そのためには、ハンドラ関数をすべてクラスとして書き換える必要がありますが......

DI using classes.
クラスを使用したDI.(Dependency Injection)

```python
# we replace the old `def allocate(cmd, uow)` with:

class AllocateHandler:

    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):  2
        self.uow = uow

    def __call__(self, cmd: commands.Allocate):  1
        line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
        with self.uow:
            # rest of handler method as before
            ...

# bootstrap script prepares actual UoW
uow = unit_of_work.SqlAlchemyUnitOfWork()

# then prepares a version of the allocate fn with dependencies already injected
allocate = AllocateHandler(uow)

...
# later at runtime, we can call the handler instance, and it will have
# the UoW already injected
allocate(cmd)
```

1. The class is designed to produce a callable function, so it has a `call` method. このクラスは呼び出し可能な関数を生成するように設計されているので、`call`メソッドを持っている.

2. But we use the `init` to declare the dependencies it requires. This sort of thing will feel familiar if you’ve ever made class-based descriptors, or a class-based context manager that takes arguments. しかし、それが必要とする依存関係を宣言するために、`init`を使用する. このようなことは、クラスベースのディスクリプタや、引数を受け取るクラスベースのコンテキストマネージャを作ったことがある人なら、よく感じることだろう.

Use whichever you and your team feel more comfortable with..
あなたやあなたのチームが使いやすいほうを選んでください.

## A Bootstrap Script Bootstrapスクリプト

We want our bootstrap script to do the following:.
私たちは、**ブートストラップ・スクリプト**に次のことをさせたいと考えている.

1. Declare default dependencies but allow us to override them デフォルトの依存関係を宣言するが、それを上書きすることができるようにする.

2. Do the “init” stuff that we need to get our app started アプリを起動するために必要な"init"処理を行う.

3. Inject all the dependencies into our handlers **すべての依存関係をハンドラーにインジェクト**する.(??)

4. Give us back the core object for our app, the message bus アプリのコアオブジェクトであるメッセージバスを返してほしい.

Here’s a first cut:.
以下、ファーストカット：

A bootstrap function (src/allocation/bootstrap.py).
ブートストラップ関数（src

```python
def bootstrap(
    start_orm: bool = True,  1
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),  2
    send_mail: Callable = email.send,
    publish: Callable = redis_eventpublisher.publish,
) -> messagebus.MessageBus:

    if start_orm:
        orm.start_mappers()  1

    dependencies = {'uow': uow, 'send_mail': send_mail, 'publish': publish}
    injected_event_handlers = {  3
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {  3
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(  4
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )
```

1. `orm.start_mappers()` is our example of initialization work that needs to be done once at the beginning of an app. We also see things like setting up the `logging` module. `orm.start_mappers()` は、アプリの開始時に一度だけ行う必要がある初期化作業の例です。 また、`logging`モジュールのセットアップなどについても見ていきます。

2. We can use the argument defaults to define what the normal/production defaults are. It’s nice to have them in a single place, but sometimes dependencies have some side effects at construction time, in which case you might prefer to default them to `None` instead. 引数defaultsを使用して、通常の しかし、依存関係が構築時に何らかの副作用をもたらすことがあります。そのような場合は、代わりに`None`をデフォルトにすることをお勧めします。

3. We build up our injected versions of the handler mappings by using a function called `inject_dependencies()`, which we’ll show next. 次に紹介する `inject_dependencies()` という関数を使って、注入されたバージョンのハンドラマッピングを構築していきます。

4. We return a configured message bus ready for use. 使用可能な状態に設定されたメッセージバスを返送します。

Here’s how we inject dependencies into a handler function by inspecting it:.
ここでは、ハンドラ関数を検査することによって、依存関係を注入する方法を説明します。

DI by inspecting function signatures (src/allocation/bootstrap.py).
関数のシグネチャを検査することでDIを行う（src

```python
def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters  1
    deps = {
        name: dependency
        for name, dependency in dependencies.items()  2
        if name in params
    }
    return lambda message: handler(message, **deps)  3
```

1. We inspect our command/event handler’s arguments. 私たちはコマンドを点検する

2. We match them by name to our dependencies. それらを名前から依存関係にマッチさせるのです。

3. We inject them as kwargs to produce a partial. これらをkwargsとして注入し、部分的に生成します。

---.
---.

- EVEN-MORE-MANUAL DI WITH LESS MAGIC より少ないマジックでより多くのマニュアルディ

If you’re finding the preceding `inspect` code a little harder to grok, this even simpler version may appeal to you..
もし、先ほどの `inspect` コードを理解するのが少し難しいと感じているのであれば、もっとシンプルなこのバージョンを使ってみてはいかがでしょうか？

Harry wrote the code for `inject_dependencies()` as a first cut of how to do “manual” dependency injection, and when he saw it, Bob accused him of overengineering and writing his own DI framework..
ハリーは、"手動 "の依存性注入を行う方法の最初の切り札として、`inject_dependencies()'のコードを書きました。それを見たボブは、彼はオーバーエンジニアリングで独自のDIフレームワークを書いていると非難しました。

It honestly didn’t even occur to Harry that you could do it any more plainly, but you can, like this:.
正直、これ以上わかりやすくできるなんてハリーにも思いつきませんでしたが、できるんですね、こういうの。

Manually creating partial functions inline (src/allocation/bootstrap.py).
インラインで部分関数を手動で作成する（src

```python
    injected_event_handlers = {
        events.Allocated: [
            lambda e: handlers.publish_allocated_event(e, publish),
            lambda e: handlers.add_allocation_to_read_model(e, uow),
        ],
        events.Deallocated: [
            lambda e: handlers.remove_allocation_from_read_model(e, uow),
            lambda e: handlers.reallocate(e, uow),
        ],
        events.OutOfStock: [
            lambda e: handlers.send_out_of_stock_notification(e, send_mail)
        ]
    }
    injected_command_handlers = {
        commands.Allocate: lambda c: handlers.allocate(c, uow),
        commands.CreateBatch: \
            lambda c: handlers.add_batch(c, uow),
        commands.ChangeBatchQuantity: \
            lambda c: handlers.change_batch_quantity(c, uow),
    }
```

Harry says he couldn’t even imagine writing out that many lines of code and having to look up that many function arguments manually.
ハリーは、あれだけのコードを書き出し、あれだけの関数の引数を手作業で調べなければならないなんて、想像すらできなかったと言います。
This is a perfectly viable solution, though, since it’s only one line of code or so per handler you add, and thus not a massive maintenance burden even if you have dozens of handlers..
ハンドラを1つ追加するごとに1行程度のコードで済むので、何十個もハンドラを追加してもメンテナンスの負担が大きくならないからです。

Our app is structured in such a way that we always want to do dependency injection in only one place, the handler functions, so this super-manual solution and Harry’s `inspect()`-based one will both work fine..
私たちのアプリは、依存性注入をハンドラ関数の一か所だけで行いたい構造になっているので、この超マニュアル的な解決策とハリーの `inspect() `ベースの解決策は、どちらもうまくいくはずです。

If you find yourself wanting to do DI in more things and at different times, or if you ever get into dependency chains (in which your dependencies have their own dependencies, and so on), you may get some mileage out of a “real” DI framework..
もし、もっといろいろなものを、いろいろなタイミングでDIしたいと思うようになったら、あるいは、依存関係の連鎖（依存関係にあるものが、さらに依存関係を持つなど）を考えるようになったら、「本物の」DIフレームワークを使うとよいかもしれませんね。

At MADE, we’ve used Inject in a few places, and it’s fine, although it makes Pylint unhappy.
MADEでは、Injectを数カ所で使っていますが、Pylintを不幸にするものの、問題ないです。
You might also check out Punq, as written by Bob himself, or the DRY-Python crew’s dependencies..
また、ボブ自身が書いたPunqや、DRY-Pythonクルーの依存関係をチェックするのもよいでしょう。

---.
---.

## Message Bus Is Given Handlers at Runtime Message Bus Is Given Handlers at Runtime.

Our message bus will no longer be static; it needs to have the already-injected handlers given to it.
メッセージバスはもはや静的なものではありません。すでに注入されたハンドラを与える必要があります。
So we turn it from being a module into a configurable class:.
そこで、モジュールから、設定可能なクラス：に変えます。

MessageBus as a class (src/allocation/service_layer/messagebus.py).
クラスとしてのMessageBus (src

```python
class MessageBus:  1

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],  2
        command_handlers: Dict[Type[commands.Command], Callable],  2
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):  3
        self.queue = [message]  4
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f'{message} was not an Event or Command')
```

1. The message bus becomes a class… メッセージバスがクラスになる...。

2. …which is given its already-dependency-injected handlers. ...依存性注入済みのハンドラが渡されます。

3. The main `handle()` function is substantially the same, with just a few attributes and methods moved onto `self`. メインの `handle()` 関数は、いくつかの属性とメソッドを `self` に移しただけで、実質的に同じです。

4. Using `self.queue` like this is not thread-safe, which might be a problem if you’re using threads, because the bus instance is global in the Flask app context as we’ve written it. Just something to watch out for. このように `self.queue` を使うことはスレッドセーフではないので、スレッドを使用している場合は問題になるかもしれません。 ただ、気をつけなければいけないことがあります。

What else changes in the bus?.
他にバスで何が変わるのでしょうか？

Event and command handler logic stays the same (src/allocation/service_layer/messagebus.py).
イベントやコマンドハンドラのロジックはそのままです（src

```python
    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:  1
            try:
                logger.debug('handling event %s with handler %s', event, handler)
                handler(event)  2
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception('Exception handling event %s', event)
                continue


    def handle_command(self, command: commands.Command):
        logger.debug('handling command %s', command)
        try:
            handler = self.command_handlers[type(command)]  1
            handler(command)  2
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise
```

1. `handle_event` and `handle_command` are substantially the same, but instead of indexing into a static `EVENT_HANDLERS` or `COMMAND_HANDLERS` dict, they use the versions on `self`. しかし、静的な `EVENT_HANDLERS` または `COMMAND_HANDLERS` ディクトにインデックスを作成するのではなく、 `self` のバージョンを使用します。

2. Instead of passing a UoW into the handler, we expect the handlers to already have all their dependencies, so all they need is a single argument, the specific event or command. ハンドラーにUoWを渡すのではなく、ハンドラーにはすでにすべての依存関係があり、必要なのは特定のイベントやコマンドという1つの引数だけです。

## Using Bootstrap in Our Entrypoints Bootstrapをエントリーポイントに使う。

In our application’s entrypoints, we now just call `bootstrap.bootstrap()` and get a message bus that’s ready to go, rather than configuring a UoW and the rest of it:.
アプリケーションのエントリポイントでは、UoWやその他を設定するのではなく、`bootstrap.bootstrap()`を呼び出して、すぐに使えるメッセージバスを取得するだけになりました:.

Flask calls bootstrap (src/allocation/entrypoints/flask_app.py).
Flaskはbootstrapを呼び出す（src

```python
-from allocation import views
+from allocation import bootstrap, views

 app = Flask(__name__)
-orm.start_mappers()  1
+bus = bootstrap.bootstrap()


 @app.route("/add_batch", methods=['POST'])
@@ -19,8 +16,7 @@ def add_batch():
     cmd = commands.CreateBatch(
         request.json['ref'], request.json['sku'], request.json['qty'], eta,
     )
-    uow = unit_of_work.SqlAlchemyUnitOfWork()  2
-    messagebus.handle(cmd, uow)
+    bus.handle(cmd)  3
     return 'OK', 201
```

1. We no longer need to call `start_orm()`; the bootstrap script’s initialization stages will do that. もはや `start_orm()` を呼び出す必要はありません。起動スクリプトの初期化ステージがそれを行います。

2. We no longer need to explicitly build a particular type of UoW; the bootstrap script defaults take care of it. 特定のタイプのUoWを明示的に構築する必要がなくなり、起動スクリプトのデフォルトで対応できるようになりました。

3. And our message bus is now a specific instance rather than the global module.3 そして、メッセージバスは、グローバルモジュールではなく、特定のインスタンスになりました3。

## Initializing DI in Our Tests テストでDIを初期化する。

In tests, we can use `bootstrap.bootstrap()` with overridden defaults to get a custom message bus.
テストでは、カスタムメッセージバスを取得するために、オーバーライドされたデフォルトで `bootstrap.bootstrap()` を使用することができます。
Here’s an example in an integration test:.
以下は、統合テストでの例です：。

Overriding bootstrap defaults (tests/integration/test_views.py).
ブートストラップのデフォルトをオーバーライドする（テスト

```python
@pytest.fixture
def sqlite_bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,  1
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),  2
        send_mail=lambda *args: None,  3
        publish=lambda *args: None,  3
    )
    yield bus
    clear_mappers()

def test_allocations_view(sqlite_bus):
    sqlite_bus.handle(commands.CreateBatch('sku1batch', 'sku1', 50, None))
    sqlite_bus.handle(commands.CreateBatch('sku2batch', 'sku2', 50, date.today()))
    ...
    assert views.allocations('order1', sqlite_bus.uow) == [
        {'sku': 'sku1', 'batchref': 'sku1batch'},
        {'sku': 'sku2', 'batchref': 'sku2batch'},
    ]
```

1. We do still want to start the ORM… まだORMを始めたいとは思っているのですが...。

2. …because we’re going to use a real UoW, albeit with an in-memory database. ...インメモリデータベースとはいえ、本物のUoWを使用するのですから。

3. But we don’t need to send email or publish, so we make those noops. でも、メールを送ったり、出版したりする必要はないので、そういうヌケを良くしています。

In our unit tests, in contrast, we can reuse our `FakeUnitOfWork`:.
一方、ユニットテストでは、`FakeUnitOfWork`: を再利用することができます。

Bootstrap in unit test (tests/unit/test_handlers.py).
ユニットテストでのBootstrap（テスト

```python
def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False,  1
        uow=FakeUnitOfWork(),  2
        send_mail=lambda *args: None,  3
        publish=lambda *args: None,  3
    )
```

1. No need to start the ORM… ORMを起動する必要がない...。

2. …because the fake UoW doesn’t use one. ...偽UoWは1つも使わないから。

3. We want to fake out our email and Redis adapters too. メールやRedisアダプタもフェイクアウトしたい。

So that gets rid of a little duplication, and we’ve moved a bunch of setup and sensible defaults into a single place..
そのため、重複を少し解消し、セットアップや感覚的なデフォルトを1つの場所に移動させました。

---.
---.

EXERCISE FOR THE READER 1.
読者のためのエクササイズ 1.

Change all the handlers to being classes as per the DI using classes example, and amend the bootstrapper’s DI code as appropriate.
クラスを使ったDIの例に従って、すべてのハンドラーをクラスであるように変更し、ブートストラッパーのDIコードを適切に修正します。
This will let you know whether you prefer the functional approach or the class-based approach when it comes to your own projects..
これによって、自分のプロジェクトに関して、機能的なアプローチとクラスベースのアプローチのどちらが好きかを知ることができるのです。

---.
---.

## Building an Adapter “Properly”: A Worked Example アダプターを "正しく "構築する。作業例。

To really get a feel for how it all works, let’s work through an example of how you might “properly” build an adapter and do dependency injection for it..
どのように動作するかを実感するために、「適切に」アダプターを構築し、依存性注入を行う方法の例を挙げてみましょう。

At the moment, we have two types of dependencies:.
現時点では、次の2種類の依存関係があります。

Two types of dependencies (src/allocation/service_layer/messagebus.py).
2種類の依存関係（src

```python
    uow: unit_of_work.AbstractUnitOfWork,  1
    send_mail: Callable,  2
    publish: Callable,  2    uow: unit_of_work.AbstractUnitOfWork,  1
    send_mail: Callable,  2
    publish: Callable,  2
```

1. The UoW has an abstract base class. This is the heavyweight option for declaring and managing your external dependency. We’d use this for the case when the dependency is relatively complex. UoWには、抽象的なベースクラスがあります。 これは、外部依存関係を宣言し、管理するためのヘビー級のオプションです。 依存関係が比較的複雑な場合に使用することになります。

2. Our email sender and pub/sub publisher are defined as functions. This works just fine for simple dependencies. 当社のメール送信者、パブ これは、単純な依存関係であれば問題なく動作します。

Here are some of the things we find ourselves injecting at work:.
ここでは、私たちが職場で注入しているものを紹介します：。

- An S3 filesystem client S3ファイルシステムクライアントです。

- A key/value store client Aキー

- A `requests` session object requests`のセッションオブジェクト。

Most of these will have more-complex APIs that you can’t capture as a single function: read and write, GET and POST, and so on..
これらのほとんどは、単一の関数として捕らえることができない、より複雑なAPIを持っています：読み取りと書き込み、GETとPOST、などなど。

Even though it’s simple, let’s use `send_mail` as an example to talk through how you might define a more complex dependency..
単純ではありますが、`send_mail`を例にして、より複雑な依存関係を定義する方法について説明しましょう。

### Define the Abstract and Concrete Implementations 抽象的な実装と具体的な実装を定義する。

We’ll imagine a more generic notifications API.
より汎用的な通知用APIをイメージします。
Could be email, could be SMS, could be Slack posts one day..
メールかもしれないし、SMSかもしれないし、ある日のSlackの投稿かもしれない。

An ABC and a concrete implementation (src/allocation/adapters/notifications.py).
ABCと具体的な実装（src

```python
class AbstractNotifications(abc.ABC):

    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError

...

class EmailNotifications(AbstractNotifications):

    def __init__(self, smtp_host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    def send(self, destination, message):
        msg = f'Subject: allocation service notification\n{message}'
        self.server.sendmail(
            from_addr='allocations@example.com',
            to_addrs=[destination],
            msg=msg
        )
```

We change the dependency in the bootstrap script:.
ブートストラップスクリプトの依存関係を次のように変更します。

Notifications in message bus (src/allocation/bootstrap.py).
メッセージバスでの通知（src

```python
 def bootstrap(
     start_orm: bool = True,
     uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
-    send_mail: Callable = email.send,
+    notifications: AbstractNotifications = EmailNotifications(),
     publish: Callable = redis_eventpublisher.publish,
 ) -> messagebus.MessageBus:
```

### Make a Fake Version for Your Tests テスト用のフェイクバージョンを作る。

We work through and define a fake version for unit testing:.
ユニットテスト用のフェイクバージョンを定義していきます。

Fake notifications (tests/unit/test_handlers.py).
偽の通知（テスト

```python
class FakeNotifications(notifications.AbstractNotifications):

    def __init__(self):
        self.sent = defaultdict(list)  # type: Dict[str, List[str]]

    def send(self, destination, message):
        self.sent[destination].append(message)
...
```

And we use it in our tests:.
そして、私たちはそれをテストに使っています：。

Tests change slightly (tests/unit/test_handlers.py).
テストが少し変わる（テスト

```python
    def test_sends_email_on_out_of_stock_error(self):
        fake_notifs = FakeNotifications()
        bus = bootstrap.bootstrap(
            start_orm=False,
            uow=FakeUnitOfWork(),
            notifications=fake_notifs,
            publish=lambda *args: None,
        )
        bus.handle(commands.CreateBatch("b1", "POPULAR-CURTAINS", 9, None))
        bus.handle(commands.Allocate("o1", "POPULAR-CURTAINS", 10))
        assert fake_notifs.sent['stock@made.com'] == [
            f"Out of stock for POPULAR-CURTAINS",
        ]
```

### Figure Out How to Integration Test the Real Thing 実物を統合テストする方法を考えよう。

Now we test the real thing, usually with an end-to-end or integration test.
次に、通常エンドツーエンドテストや統合テストを行い、本番に臨みます。
We’ve used MailHog as a real-ish email server for our Docker dev environment:.
MailHogは、Docker開発環境の本格的なメールサーバとして使用しています:.

Docker-compose config with real fake email server (docker-compose.yml).
本物の偽メールサーバーを使ったDocker-composeの設定(docker-compose.yml)。

```yaml
version: "3"

services:

  redis_pubsub:
    build:
      context: .
      dockerfile: Dockerfile
    image: allocation-image
    ...

  api:
    image: allocation-image
    ...

  postgres:
    image: postgres:9.6
    ...

  redis:
    image: redis:alpine
    ...

  mailhog:
    image: mailhog/mailhog
    ports:
      - "11025:1025"
      - "18025:8025"
```

In our integration tests, we use the real `EmailNotifications` class, talking to the MailHog server in the Docker cluster:.
統合テストでは、本物の `EmailNotifications` クラスを使用し、Docker クラスタ内の MailHog サーバと通信します:.

Integration test for email (tests/integration/test_email.py).
メールに関する統合テスト（テスト

```python
@pytest.fixture
def bus(sqlite_session_factory):
    bus = bootstrap.bootstrap(
        start_orm=True,
        uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
        notifications=notifications.EmailNotifications(),  1
        publish=lambda *args: None,
    )
    yield bus
    clear_mappers()


def get_email_from_mailhog(sku):  2
    host, port = map(config.get_email_host_and_port().get, ['host', 'http_port'])
    all_emails = requests.get(f'http://{host}:{port}/api/v2/messages').json()
    return next(m for m in all_emails['items'] if sku in str(m))


def test_out_of_stock_email(bus):
    sku = random_sku()
    bus.handle(commands.CreateBatch('batch1', sku, 9, None))  3
    bus.handle(commands.Allocate('order1', sku, 10))
    email = get_email_from_mailhog(sku)
    assert email['Raw']['From'] == 'allocations@example.com'  4
    assert email['Raw']['To'] == ['stock@made.com']
    assert f'Out of stock for {sku}' in email['Raw']['Data']
```

1. We use our bootstrapper to build a message bus that talks to the real notifications class. ブートストラッパーを使用して、実際の通知クラスと会話するメッセージバスを構築しています。

2. We figure out how to fetch emails from our “real” email server. 本物の」電子メールサーバーから電子メールを取得する方法を考え出す。

3. We use the bus to do our test setup. バスを使ってテストセットアップを行う。

4. Against all the odds, this actually worked, pretty much at the first go! 一発で成功したんです。

And that’s it really..
そして、本当にそれだけです。

---.
---.

EXERCISE FOR THE READER 2.
読者のためのエクササイズ 2.

You could do two things for practice regarding adapters:.
アダプターに関する練習のために、次の2つのことをすることができます。

1. Try swapping out our notifications from email to SMS notifications using Twilio, for example, or Slack notifications. Can you find a good equivalent to MailHog for integration testing? 私たちの通知をメールから、例えばTwilioを使ったSMS通知や、Slackの通知などに置き換えてみてください。 統合テスト用のMailHogと同等の良いものはないでしょうか。

2. In a similar way to what we did moving from `send_mail` to a `Notifications` class, try refactoring our `redis_eventpublisher` that is currently just a `Callable` to some sort of more formal adapter/base class/protocol. send_mail`から`Notifications`クラスに移行したのと同じように、現在単なる`Callable`である `redis_eventpublisher` を、より正式なアダプタにリファクタリングしてみましょう。

---.
---.

## Wrap-Up Wrap-Up.

Once you have more than one adapter, you’ll start to feel a lot of pain from passing dependencies around manually, unless you do some kind of dependency injection..
複数のアダプタを持つようになると、何らかの依存性注入を行わない限り、依存性を手動で受け渡すことに苦痛を感じるようになります。

Setting up dependency injection is just one of many typical setup/initialization activities that you need to do just once when starting your app.
依存性注入の設定は、多くの典型的な設定の1つに過ぎません。
Putting this all together into a bootstrap script is often a good idea..
これをまとめてブートストラップスクリプトにするのは、良いアイデアだと思います。

The bootstrap script is also good as a place to provide sensible default configuration for your adapters, and as a single place to override those adapters with fakes for your tests..
bootstrapスクリプトは、アダプタのデフォルト設定を適切に行う場所として、また、テスト用の偽アダプタを上書きするための一つの場所としても適しています。

A dependency injection framework can be useful if you find yourself needing to do DI at multiple levels—if you have chained dependencies of components that all need DI, for example..
依存性注入フレームワークは、複数のレベルでDIを行う必要がある場合、例えば、すべてのDIが必要なコンポーネントの依存関係が連鎖しているような場合に便利です。

This chapter also presented a worked example of changing an implicit/simple dependency into a “proper” adapter, factoring out an ABC, defining its real and fake implementations, and thinking through integration testing..
また、この章では、暗黙の了解を変更する作業例も紹介しました。

---.
---.

- DI AND BOOTSTRAP RECAP ディ、ブートストラップの総括を行います。

In summary:.
要約すると：。

1. Define your API using an ABC. ABCを使用してAPIを定義します。

2. Implement the real thing. 本物を実装する。

3. Build a fake and use it for unit/service-layer/handler tests. フェイクを作り、ユニットに使用する

4. Find a less fake version you can put into your Docker environment. Dockerの環境に入れることができる、より偽りのないバージョンを探してください。

5. Test the less fake “real” thing. より偽りのない「本物」を試す。

6. Profit! プロフィット！です。

---.
---.

These were the last patterns we wanted to cover, which brings us to the end of Part II.
これらは、最後に取り上げたいパターンでしたので、第二部の終わりとなります。
In the epilogue, we’ll try to give you some pointers for applying these techniques in the Real WorldTM..
エピローグでは、これらのテクニックを「Real WorldTM」で活用するためのポイントをお伝えしていきます。

1. Because Python is not a “pure” OO language, Python developers aren’t necessarily used to the concept of needing to compose a set of objects into a working application. We just pick our entrypoint and run code from top to bottom. Pythonは「純粋な」OO言語ではないため、Pythonの開発者は、オブジェクトのセットを組み合わせて動作するアプリケーションにする必要があるという概念に必ずしも慣れていません。 エントリーポイントを決めて、上から下へコードを走らせるだけです。

2. Mark Seemann calls this Pure DI or sometimes Vanilla DI. Mark SeemannはこれをPure DI、あるいはVanilla DIと呼んでいます。

3. However, it’s still a global in the `flask_app` module scope, if that makes sense. This may cause problems if you ever find yourself wanting to test your Flask app in-process by using the Flask Test Client instead of using Docker as we do. It’s worth researching Flask app factories if you get into this. ただし、`flask_app`のモジュールスコープではグローバルであることに変わりはありません、意味があるのかどうか。 これは、Flaskアプリをインプロセスでテストしたい場合、私たちのようにDockerを使うのではなく、Flask Test Clientを使うことで問題が発生する可能性があります。 これにハマるとFlaskのアプリ工場を研究する価値がありますね。
