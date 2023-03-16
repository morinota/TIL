## link リンク

- https://connascence.io/execution.html https

# Dynamic Connascences ダイナミックコナスセンス

## Connascence of Execution Connascence of Execution.

Connascence of execution is when the order of execution of multiple components is important.
Conascence of executionとは、複数のコンポーネントの実行順序が重要である場合です。
Common examples include locking and unlocking resources, where locks must be acquired and released in the same order everywhere in the entire codebase..
よくある例としては、リソースのロックとアンロックがあり、コードベース全体のどこでも同じ順序でロックの取得と解放を行う必要があります。

Connascence of execution can also occur when using objects that encapsulate a state machine, and that state machine only allows certain operations in certain states.
また、ステートマシンをカプセル化したオブジェクトを使用し、そのステートマシンが特定の状態でのみ特定の操作を許可する場合にも、実行のコナカンが発生することがあります。
For example, consider a hypothetical EmailSender class that allows a caller to generate and send an email:.
例えば、呼び出し元が電子メールを生成して送信することを可能にする、仮想のEmailSenderクラスを考えてみましょう:.

```python
email = Email()
email.setRecipient("foo@example.comp")
email.setSender("me@mydomain.com")
email.send()
email.setSubject("Hello World")
```

The last two lines show a trivial example of connascence of execution.
最後の2行は、実行のコナシの些細な例を示しています。
The setSubject method cannot be called after the send method (at best it will do nothing).
setSubjectメソッドは、sendメソッドの後に呼び出すことはできません（せいぜい何もしない程度）。
In this example the locality of the coupling is very low, but cases where the locality is very high can be much harder to find and fix (consider, for example a scenario where the last two lines are called on separate threads)..
この例では、結合の局所性は非常に低いですが、局所性が非常に高い場合は、発見して修正するのが非常に難しくなります（例えば、最後の2行が別々のスレッドで呼び出されるシナリオを考えてみてください）。

## Connascence of Timing Connascence of Timing.

Connascence of timing is when the timing of the execution of multiple components is important..
複数のコンポーネントの実行タイミングが重要である場合に、タイミングのコナクションが発生する。

## Connascence of Value Connascence of Value.

Connascence of value is when several values must change together.
価値の共振とは、いくつかの価値が一緒に変化しなければならないことです。
This frequently occurs between production code and test code.
これは、プロダクションコードとテストコードの間で頻繁に発生します。
For example, consider an Article class, which represents a blog article.
例えば、ブログの記事を表すArticleクラスを考えてみましょう。
When it is instantiated, it is given some text contents, and its initial 'state' is 'draft':.
インスタンス化されると、いくつかのテキストコンテンツが与えられ、その初期「状態」は「draft」:となる。

```python
class ArticleState(Enum):
    Draft = 1
    Published = 2


class Article(object):

    def __init__(self, contents):
        self.contents = contents
        self.state = ArticleState.Draft

    def publish(self):
        # do whatever is required to publish the article.
        self.state = ArticleState.Published
```

Now imagine a hypothetical test that ensures that the publish method works:.
ここで、パブリッシュメソッドが機能することを保証する仮説的なテストを想像してください：。

```python
article = Article("Test Contents")
assert article.state == ArticleState.Draft
article.publish()
assert article.state == ArticleState.Published
```

The problem here is that the test requires knowledge of the initial state of the Article class: if the Article's initial state is ever changed, this test will break (this is arguably a bad test, since the first assertion has little to do with the intent of the test, but it's a common mistake).
ここでの問題は、このテストが Article クラスの初期状態の知識を必要とすることです：もし Article の初期状態がこれまでに変更されたなら、このテストは壊れます（最初のアサーションがテストの意図とほとんど関係がないので、これは間違いなく悪いテストです、しかしそれはよくある間違いなのです）。
This code can be improved by adding an InitialState label to ArticleClass, and changing both the Article class and the test to refer to that label instead:.
このコードは、ArticleClassにInitialStateラベルを追加し、Articleクラスとテストの両方をそのラベルの代わりに参照するように変更することによって改善することができます：。

```python
class ArticleState(Enum):
    Draft = 1
    Published = 2
    InitialState = Draft


class Article(object):

    def __init__(self, contents):
        self.contents = contents
        self.state = ArticleState.InitialState
```

The test now becomes:.
今、テストは次のようになります。

```python
article = Article("Test Contents")
assert article.state == ArticleState.InitialState
article.publish()
assert article.state == ArticleState.Published
```

Should we need to change the state machine of the Article class, we can do so by changing the ArticleState enumeration:.
Articleクラスのステートマシンを変更する必要がある場合、ArticleState列挙を変更することによってそうすることができます。

```python
class ArticleState(Enum):
    Preproduction = 1
    Draft = 2
    Published = 3
    InitialState = Preproduction
```

We have effectively introduced a level of indirection between the Article class and its initial state value..
Articleクラスとその初期状態の値との間に、事実上、間接的なレベルを導入しました。

## Connascence of Identity Connascence of Identity.

Connascence of identity is when multiple components must reference the same entity..
複数のコンポーネントが同じエンティティを参照する必要がある場合、アイデンティティのコナスカンス（Connascence）が発生します。