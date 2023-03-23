## link リンク

- https://connascence.io/execution.html

# Dynamic Connascences

## Connascence of Execution

Connascence of execution is when the order of execution of multiple components is important.
**Conascence of executionとは、複数のコンポーネントの実行順序が重要である場合**である.
Common examples include locking and unlocking resources, where locks must be acquired and released in the same order everywhere in the entire codebase..
よくある例としては、**リソースのロックとアンロック**があり、コードベース全体のどこでも同じ順序でロックの取得と解放を行う必要がある.

Connascence of execution can also occur when using objects that encapsulate a state machine, and that state machine only allows certain operations in certain states.
また、state machine をカプセル化したオブジェクトを使用し、その**state machineが特定のstateでのみ特定の操作を許可する場合にも、Connascence of Execution が発生することがある**.
For example, consider a hypothetical EmailSender class that allows a caller to generate and send an email:.
例えば、呼び出し元が電子メールを生成して送信することを可能にする、仮想の`EmailSender`クラスを考えてみよう:

```python
email = Email()
email.setRecipient("foo@example.comp")
email.setSender("me@mydomain.com")
email.send()
email.setSubject("Hello World")
```

The last two lines show a trivial example of connascence of execution.
最後の2行は、connascence of execution の些細な例を示している.
The setSubject method cannot be called after the send method (at best it will do nothing).
`setSubject`メソッドは、`send`メソッドの**後に呼び出すことはできない**(せいぜい何もしない程度).
In this example the locality of the coupling is very low, but cases where the locality is very high can be much harder to find and fix (consider, for example a scenario where the last two lines are called on separate threads)..
**この例では、結合の locality は非常に低い(=近い??)ですが、localityが非常に高い(=遠い??)場合は、発見して修正するのが非常に難しくなる**(例えば、最後の2行が別々のスレッドで呼び出される(=localityが大きい=遠い?)シナリオを考えてみてください).

## Connascence of Timing

Connascence of timing is when the timing of the execution of multiple components is important..
**複数のコンポーネントの実行タイミングが重要である場合に、Connascence of timing**が発生する.

## Connascence of Value Connascence of Value.

Connascence of value is when several values must change together.
**Connascence of value とは、いくつかのvalueが一緒に変化しなければならないケース**である.
This frequently occurs between production code and test code.
これは、**プロダクションコードとテストコードの間で頻繁に発生**する.
For example, consider an Article class, which represents a blog article.
例えば、ブログの記事を表す`Article`クラスを考えてみよう.
When it is instantiated, it is given some text contents, and its initial 'state' is 'draft':.
インスタンス化されると、いくつかのテキストコンテンツが与えられ、そのinitial `state`は`draft`となる:

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
ここで、`publish`メソッドが機能することを保証する仮説的なテストを想像してください：

```python
article = Article("Test Contents")
assert article.state == ArticleState.Draft
article.publish()
assert article.state == ArticleState.Published
```

The problem here is that the test requires knowledge of the initial state of the Article class: if the Article's initial state is ever changed, this test will break (this is arguably a bad test, since the first assertion has little to do with the intent of the test, but it's a common mistake).
ここでの問題は、このテストが `Article` クラスのinitial `state` の知識を必要とすることである：もし Article のinitial `state` がこれまでに変更されたなら、このテストは壊れる(**最初のアサーションがテストの意図とほとんど関係がないので、これは間違いなく悪いテストである、しかしそれはよくある間違いなのだ**).
This code can be improved by adding an InitialState label to ArticleClass, and changing both the Article class and the test to refer to that label instead:.
このコードは、`ArticleState`に`InitialState`ラベルを追加し、`Article`クラス **(production code)とテストの両方をそのラベルの代わりに参照するように変更することによって改善することができる**：

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
今、テストは次のようになる.

```python
article = Article("Test Contents")
assert article.state == ArticleState.InitialState
article.publish()
assert article.state == ArticleState.Published
```

Should we need to change the state machine of the Article class, we can do so by changing the ArticleState enumeration:.
Articleクラスのstate machineを変更する必要がある場合、`ArticleState` classを変更することによってそうすることができる.

```python
class ArticleState(Enum):
    Preproduction = 1
    Draft = 2
    Published = 3
    InitialState = Preproduction
```

We have effectively introduced a level of indirection between the Article class and its initial state value..
`Article`クラスとそのinitial `state`のvalueとの間に、事実上、**間接的なレベルを導入**した.(これによってどの種類のconnascenceに改善されたんだろう...connascence of name??)

## Connascence of Identity

Connascence of identity is when multiple components must reference the same entity..
**複数のコンポーネントが同じEntityを参照する必要がある場合、Connascence of Identityが発生する**.
