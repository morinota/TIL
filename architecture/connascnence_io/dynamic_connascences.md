## link

- https://connascence.io/execution.html

# Dynamic Connascences

## Connascence of Execution

Connascence of execution is when the order of execution of multiple components is important. Common examples include locking and unlocking resources, where locks must be acquired and released in the same order everywhere in the entire codebase.

Connascence of execution can also occur when using objects that encapsulate a state machine, and that state machine only allows certain operations in certain states. For example, consider a hypothetical EmailSender class that allows a caller to generate and send an email:

```python
email = Email()
email.setRecipient("foo@example.comp")
email.setSender("me@mydomain.com")
email.send()
email.setSubject("Hello World")
```

The last two lines show a trivial example of connascence of execution. The setSubject method cannot be called after the send method (at best it will do nothing). In this example the locality of the coupling is very low, but cases where the locality is very high can be much harder to find and fix (consider, for example a scenario where the last two lines are called on separate threads).

## Connascence of Timing

Connascence of timing is when the timing of the execution of multiple components is important.

## Connascence of Value

Connascence of value is when several values must change together. This frequently occurs between production code and test code. For example, consider an Article class, which represents a blog article. When it is instantiated, it is given some text contents, and its initial 'state' is 'draft':

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

Now imagine a hypothetical test that ensures that the publish method works:

```python
article = Article("Test Contents")
assert article.state == ArticleState.Draft
article.publish()
assert article.state == ArticleState.Published
```

The problem here is that the test requires knowledge of the initial state of the Article class: if the Article's initial state is ever changed, this test will break (this is arguably a bad test, since the first assertion has little to do with the intent of the test, but it's a common mistake). This code can be improved by adding an InitialState label to ArticleClass, and changing both the Article class and the test to refer to that label instead:

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

The test now becomes:

```python
article = Article("Test Contents")
assert article.state == ArticleState.InitialState
article.publish()
assert article.state == ArticleState.Published
```

Should we need to change the state machine of the Article class, we can do so by changing the ArticleState enumeration:

```python
class ArticleState(Enum):
    Preproduction = 1
    Draft = 2
    Published = 3
    InitialState = Preproduction
```

We have effectively introduced a level of indirection between the Article class and its initial state value.

## Connascence of Identity

Connascence of identity is when multiple components must reference the same entity.
