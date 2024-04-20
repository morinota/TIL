## refs 審判

https://medium.com/@m.nusret.ozates/good-design-practices-with-python-design-by-contract-a2a2d07b37d0
https://medium.com/@m.nusret.ozates/good-design-practices-with-python-design-by-contract-a2a2d07b37d0

# Good Design Practices with Python — Design by Contract Pythonによるグッドデザインの実践 - 契約によるデザイン

## Introduction 

As software engineers, we write code most of the time.
ソフトウェア・エンジニアとして、私たちはほとんどの時間、コードを書いている。
We have some tight deadlines and because of these deadlines, we tend to write code fast without thinking about the design.
私たちには厳しい納期があり、そのためにデザインを考えずにコードを速く書いてしまいがちだ。
This choice comes with consequences.
この選択には結果が伴う。
It actually makes you slower because you write the code so urgently that you forgot that client’s requests will change faster than you thought and when that time comes to you, it will be very hard to change your code.
なぜなら、クライアントの要求が思ったよりも速く変化することを忘れて、コードを急いで書いてしまうからだ。
You will look at the code and say “oh I need to change this part and it is done” and then you will realize that the change broke a completely different part of the code, you will change that too and realize this change broke another part of your code and so on…
コードを見て、「ああ、この部分を変更すれば完了だ」と言っても、その変更がコードのまったく別の部分を壊していることに気づき、その部分も変更して、この変更がコードの別の部分を壊していることに気づく......といった具合だ。

We don’t want that, think before coding, and give yourself some time to design architecture.
コーディングの前に考え、アーキテクチャーの設計に時間を割く。
Think about how you could test that chunk of code and only after that start coding.
そのコードの塊をどのようにテストできるかを考え、その後でコーディングを始める。
To make your life easier, there are some design “principals” out there and I will explain them with examples using Python.
あなたの生活を楽にするために、世の中にはいくつかの設計の「原則」があり、Pythonを使った例で説明します。
This is part 1 and I will explain “Design by Contract” in this part.
今回はその1で、「契約によるデザイン」について説明する。

## Design by Contract 

We write code to be used by some clients using APIs or libraries.
私たちは、APIやライブラリを使って、あるクライアントが使用するコードを書く。
When creating a function, we decide what is needed for making that function run and what we will return if conditions are met.
関数を作成する際には、その関数を実行するために必要なものと、条件が満たされた場合に返すものを決定する。
For a basic example:
基本的な例を挙げよう：

```python
def sum(first: int, second: int) -> int:

	return first + second
```

In this function, we basically say “I want you to give me to integer and as a result, I will give you another integer, which is the sum of these two integers”.
この関数では、基本的に「整数を与えてほしい。その結果として、この2つの整数の和であるもう1つの整数を与える」と言う。
If we don’t check the type of the variables, our program will crash or not work as expected.
変数の型をチェックしないと、プログラムがクラッシュしたり、期待通りに動作しなかったりする。
This was a basic example and you shouldn’t think that “Oh okay it is just type checking!”.
これは基本的な例であり、「そうか、ただのタイプチェックか！」と思ってはいけない。
Because just doing this would be just trying to make python a statically typed language.
なぜなら、これをやるだけでは、パイソンを静的型付け言語にしようとしているだけだからだ。

To make a function work properly, we need to design a contract.
機能を適切に機能させるためには、契約を設計する必要がある。
A contract has these elements:
契約には以下の要素がある：

Preconditions: They are checks we need to do before running the function.
前提条件： 関数を実行する前に必要なチェックです。
If these values are not as expected, running the function would be pointless.
これらの値が期待通りでない場合、関数を実行することは無意味である。
We could check for the type of the parameter, the value range of the parameter, or maybe if it is a string and we are expecting that string must contain an e-mail, we should check if it contains an e-mail using a regex.
パラメータのタイプや値の範囲をチェックすることもできるし、文字列で、その文字列にEメールが含まれていることを期待しているのであれば、正規表現を使ってEメールが含まれているかどうかをチェックすることもできる。
If there is a problem with the condition check, we need to raise an exception with a meaningful message.
条件チェックに問題があれば、意味のあるメッセージとともに例外を発生させる必要がある。
We can even raise a custom exception if needed.
必要であれば、カスタム例外を発生させることもできる。

Postconditions: This is what we promise to give.
後条件： これが私たちの約束だ。
We need to check if the returned value of our function satisfies the conditions of what we will promise to give.
関数の戻り値が、私たちが約束する条件を満たすかどうかをチェックする必要がある。
If these conditions return False, which means there is a problem with our code.
これらの条件がFalseを返した場合、コードに問題があることを意味する。

Let’s do an example:
例を挙げてみよう：

```python
from typing import Union

def check_id(user_id: str) -> bool:
    """
    Check if user_id is valid
    Args:
        user_id: user id
    Returns:
        True if user_id is valid, raise Error otherwise
    """
    if not isinstance(user_id, str):
        raise TypeError("user_id must be a string")
    if not user_id.isdigit():
        raise ValueError("user_id must be a number")
    if not len(user_id) == 8:
        raise ValueError("user_id must be 8 digits")
    return True


def get_user(user_id: str) -> Union[User, None]:
    """ Get user info from database

    Args:
        user_id: user id
    Returns:
         User object
    """
    return User.from_id(user_id)


def check_user(user: User):
    """
    Check if user is valid
    Args:
        user: user object
    Returns:
        Nothing if user is valid, raise Error otherwise
    """
    if user is None:
        raise ValueError("user not found")


def user_info(user_id: str) -> User:
    """ Get user info from database
    user_id must be valid:
        - user_id must be a string
        - user_id must be a number
        - user_id must be 8 digits

    Args:
        user_id: user id
    Returns:
        User object if user_id is valid and user can be found, raise Error otherwise
    """
    check_id(user_id)
    user = get_user(user_id)
    check_user(user)
    return user
```

This is still not an advanced example but I think it gives a good idea.
これはまだ高度な例ではないが、良いアイデアを与えてくれると思う。
First, we check if the given input is a string with a length of 8 and contains only digits.
まず、与えられた入力が長さ8で数字だけの文字列かどうかをチェックする。
Then we search for the user and check if we can give the result as promised.
そして、ユーザーを検索し、約束通りの結果が得られるかどうかをチェックする。
If we can’t we return an error.
できなければエラーを返す。

> Don’t forget that you need to document those conditions in the docstrings!
> その条件をdocstringsに文書化する必要があることをお忘れなく！

Now a little bit fun part! I have access to Github Copilot and just wrote: “ # Design by contract example” and add a “def” to help it.
さて、ちょっと楽しい部分だ！GithubのCopilotにアクセスして、こう書いてみた： " # 契約例による設計 "と、それを助けるための "def "を追加します。
Here is the beautiful result for checking preconditions using annotations:
アノテーションを使った前提条件チェックの美しい結果がここにある：

```python
# Design by contract example

def contract(func):
    def wrapper(*args, **kwargs):
        if len(args) + len(kwargs) != func.__code__.co_argcount:
            raise TypeError("Wrong number of arguments")
        return func(*args, **kwargs)

    return wrapper


@contract
def add(x, y):
    return x + y
```

By using the design by contract, you can be sure where was the problem if the function doesn’t work.
契約による設計を使用することで、機能が機能しない場合、どこに問題があったのかを確認することができる。
As result, you will have more robust code.
その結果、より堅牢なコードを手に入れることができる。
Using this approach will cause doing extra work but it will be better for you in the long run.
この方法を使えば、余計な仕事をすることになるが、長い目で見ればその方がいい。
At least, you should use this approach in the critical parts of your program.
少なくとも、プログラムの重要な部分ではこのアプローチを使うべきだ。

And that’s all! Thank you for reading!
以上です！お読みいただきありがとうございました！