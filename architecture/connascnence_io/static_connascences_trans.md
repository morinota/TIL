## link リンク

- https://connascence.io/name.html https

# Static Connascences スタティック・コナシオン

## Connascence of Name

Connascence of name is when multiple components must agree on the name of an entity.
Connascence of nameとは、あるエンティティの名前について、複数のコンポーネントが同意しなければならない場合である.
Method names are an example of this form of connascence: if the name of a method changes, callers of that method must be changed to use the new name..
**メソッド名が変われば、そのメソッドの呼び出し元も新しい名前を使うように変更しなければならない**.(ようなカップリングの状況?)

Almost any code example involves connascence of name.
ほとんどのコード例では、名前の連結を伴う.
Consider the following class declaration taken from the Python standard library (method implementation has been omitted for clarity):.
Python標準ライブラリから引用した次のクラス宣言を考えてみましょう(わかりやすくするためにメソッドの実装は省略されている).

```python
class Request:

    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False,
                 method=None):
        pass

    def set_proxy(self, host, type):
        pass
```

Changing the name of any part of this code will cause code that uses this class to break, including:.
このコードのいずれかの部分の名前を変更すると、このクラスを使用するコードが次のように壊れることがある.

- Changing the class name from Request. クラス名をRequest...から変更する
- Changing any of the method names (such as set_proxy). メソッド名（set_proxyなど）を変更する.
- Changing the name of any of the parameters to either **init** or set_proxy. パラメータ名を **init** または set_proxy のいずれかに変更する.

Connascence of name is unavoidable, since we refer to entities using labels.
**ラベルを使って Entity を参照するため(そりゃそうだ!!)、Connascence of nameは避けられない**.
If we change the name of an entity when we declare it, we must also change all code that refers to that entity.
エンティティの宣言時に名前を変更した場合、そのエンティティを参照するすべてのコードも変更しなければならない.
For this reason, connascence of name is the weakest connascence.
そのため、**connascence of nameは最も弱い連結となる**.
However, it also illustrates how important it is to name entities in code well..
しかし同時に、**コード内のEntityにうまく名前をつけることがいかに重要であるかということも示している**.

## Connascence of Type Connascence of Type.

Connascence of type is when multiple components must agree on the type of an entity.
Connascence of typeとは、**複数のコンポーネントがエンティティのタイプに同意する必要がある場合である**.
In a statically typed language, these issues are often (but not always) caught by the compiler.
静的型付け言語では、このような問題はコンパイラによって捕捉されることが多い(しかし、常にそうとは限らない).
Consider the following trivial C++ code:.
次のような些細なC++コードを考えてみましょう:

```
std::string cost;

cost = 10.95; // OOPS!
```

Dynamically typed languages typically suffer from less obvious instances of connascence of type.
**動的型付けされた言語は、一般的に、あまり目立たないconnascence of typeに悩まされる**.
Consider a function that calculates your age, given your day, month, and year of birth:.
生年月日、月、年が与えられて、年齢を計算する関数を考えてみよう.

```python
def calculate_age(birth_day, birth_month, birth_year): # do the calculation here:
```

How is this function supposed to be called? Here are a few different options:.
この関数はどのように呼び出すのでしょうか？以下は、いくつかの異なる選択肢です：

```python
calculate_age(1, 9, 1984)
calculate_age(1, 9, 84)
calculate_age('1', '9', '1984')
calculate_age('1', 'September', '1984')
```

## Connascence of Meaning Connascence of Meaning.

Connascence of meaning is when multiple components must agree on the meaning of particular values.
Conascence of meaningとは、複数のコンポーネントが特定の値の意味について合意する必要がある場合.
Consider some code that processes credit card payments.
クレジットカードの決済を処理するコードを考えてみよう.
The following function might be used to determine if a given credit card number is valid or not:.
次の関数は、与えられたクレジットカード番号が有効かどうかを判断するために使用されるかもしれない：

```python
def is_credit_card_number_valid(card_number):
    # Check for 'test' credit card numbers:
    if card_number == "9999-9999-9999-9999":
        return True
    # Do normal validation:
    # ...
```

The problem here is that all parts of this system must agree that 9999-9999-9999-9999 is the test credit card number.
ここで問題になるのは、このシステムのすべての部分が、9999-9999-9999がテスト用クレジットカード番号であることに同意しなければならないという事である.
If that value changes in one place, it must also change in another..
ある場所でそのvalueが変われば、別の場所でも変わるはず.

Here's another example where user roles are encoded as integers:.
以下は、ユーザのロールが整数としてencode(符号化)されている例.

```python
def get_user_role(username):
    user = database.get_user_object_for_username(username)
    if user.is_admin:
        return 2
    elif user.is_manager:
        return 1
    else:
        return 0
```

Elsewhere, code might need to check that a given username is an administrator, like so:.
他の場所では、次のように、指定されたユーザ名が管理者であるかどうかをチェックする必要がある場合がある.

```
if get_user_role(username) != 2:
    raise PermissionDenied("You must be an administrator")
```

Connascence of meaning can be improved to connascence of name by moving the "magic values" to named constants, and referring to the constants instead of the values.
Connascence of meaningは、"magic values"を名前付き定数に移し、**変数の代わりに定数を参照することで**、connascence of nameに改善することができる.
However in doing so, we have increased the amount of connascence of name (since we now need a third location to store the constant)..
しかし、そうすることで、名前の連結が増えた(定数を保存するために3つ目の場所が必要になったからである)

Another common example of connascence of meaning is when None is used as a return value.
また、**「None」が戻り値として使われる場合も、connascence of meaningがよく起こる例**.
This frequently occurs in functions that are tasked with finding an object.
これは、**オブジェクトを見つけることをタスクとする機能で頻繁に発生する**.
If that object isn't found, the function might return None..
そのオブジェクトが見つからない場合、関数は None を返すかもしれない.

```python
def find_user_in_database(username):
    return database.find_user(username=username) or None
```

However, the function might also return None in an error condition:.
しかし、この関数は、エラー時にNoneを返すこともある：

```python
def find_user_in_database(username):
    try:
        return database.find_user(username=username) or None
    except DatabaseError:
        return None
```

The problem in both these cases is that a semantic meaning is being assigned to the None value.
いずれの場合も、**Noneの値に意味づけがされていることが問題**である.
If multiple different meanings are assigned to the same None value in the same codebase, the programmer must remember which meaning applies to which case.
**同じコードベースにおいて、同じNone値に複数の異なる意味が付与されている場合、プログラマはどのような場合にどの意味が適用されるかを覚えておかなければならない**.
This can be improved to connascence of name by returning an explicit object that represents the case in question:.
これは、**問題のケースを表す明示的なオブジェクトを返すことで、connascence of nameに改善**することができる：

```python
def find_user_in_database(username):
    try:
        return database.find_user(username=username) or ObjectNotFound
    except DatabaseError:
        return None
```

We still have connascence of meaning in the error case, but at least the None value is no longer ambigous.
エラーの場合はまだconnascence of meaningがありますが、少なくともNoneの値はもう曖昧ではない.
The error case could also be improved to connascence of name in a similar way..
また、エラーケースも同様に connascence of name に改善される可能性がある.

Another common example of connascence of meaning is when we use primitive numeric types to represent more complex values.
また、**primitiveな数値型を使用してより複雑な値を表現する場合も、connascence of meaningが起こりやすい例**と言える.
Consider this line of code in a codebase that processes payments:.
決済を処理するコードベースにおいて、次のようなコード行を考えてみましょう:

```
unit_cost = 49.95
```

What currency is that cost expressed in? US dollars? British pounds? How do you ensure that two costs with different currencies are not added together? Similar to the examples above, the problem is that a semantic meaning is being added to the primitive type.
そのコストはどのような通貨で表現されているのでしょうか？USドル？イギリスポンド？通貨が異なる2つのコストが一緒に加算されないようにするにはどうしたらいいでしょうか？**上の例と同様、primitive型にsemantic(意味論的??=明示的みたいな?)な意味が付加されていることが問題なのである**.
It can be improved to connascence of type by creating a 'Cost' type that disallows operations between different currencies:.
**異なる通貨間の操作を禁止する'Cost'タイプを作成することで、connascence of typeに改善することができる**:

```
unit_cost = Cost(49.95, 'USD')
```

This particular problem is often called "Primitive Obsession", and can be generically described as using primitive data types to represent more complex domains..
この問題は"**Primitive Obsession**"と呼ばれ、一般的には"より複雑な領域を表現するためにprimitiveなデータ型を使用する(してしまう)"と表現されることが多い.

## Connascence of Position

Connascence of position is when multiple entities must agree on the order of values..
Connascence of position とは、**複数の entity が value の順序について合意しなければならない場合**である.

### In Data Structures.

データ構造において.

For example, consider a function that retrieves a user's details:.
例えば、ユーザの詳細情報を取得する関数を考えてみよう:

```python
def get_user_details():
    # Returns a user's details as a list:
    # first_name, last_name, year_of_birth, is_admin
    return ["Thomas", "Richards", 1984, True]
```

This is a somewhat contrived example, but it's not uncommon to see data returned in lists or tuples.
これはやや不自然な例だが、**データがリストやタプルで返されることは珍しくない**.
Elsewhere in the code we might need to perform some check on whether the user is an administrator or not:.
コードの別の場所で、ユーザが管理者であるかどうかのチェックを行う必要があるかもしれない:

```python
def launch_nukes(user):
    if user[3]:
        # actually launch the nukes
    else:
        raise PermissionDeniedError("User is not an administrator!")
```

These two functions are linked by connascence of position.
**この2つのfunctionは、connascence of positionでつながっている**.
If the order of the values in the user list ever changes, both locations must be updated (this example is particularly scary if someone were to update the user list to be [first_name, initials, last_name, year_of_birth, is_admin] without updating the check inside launch_nukes)..
**ユーザリストのvalueの順序が変わることがあれば、両方の場所を更新しなければならない**(=これこそconnascenceの定義??)(この例は、誰かがlaunch_nukes内のチェックを更新せずにユーザリストを`[first_name, initials, last_name, year_of_birth, is_admin]`に更新した場合に特に怖い).

This connascence can be improved to connascence of name by turning the list into a dictionary or class.
このconnascenceは、**リストを辞書やクラス(特にdata class?)にすることで、connascence of nameに改善することができる**.
The following example shows how the above functions might look as a dictionary:.
次の例は、上記の関数が辞書としてどのように見えるかを示している:

```python
def get_user_details():
    return {
        "first_name": "Thomas",
        "last_name": "Richards",
        "year_of_birth": 1984,
        "is_admin": True,
    }


def launch_nukes(user):
    if user['is_admin']:
        # actually launch the nukes
    else:
        raise PermissionDeniedError("User is not an administrator!")
```

Note that these two functions are still coupled, but we've turned connascence of position into the weaker connascence of name.
この2つの関数はまだ結合していますが、**connascence of positionをより弱いconnascence(connascence of name)に変えている**ことに注意してください!!
This has also increased the readability of the get_user_details function - the explicit comment is no longer needed to document the order of the keys..
これにより、`get_user_details`**関数の可読性が向上し、キーの順序を示す明示的なコメントが不要になった**.

A similar solution is to use a class instead of a dictionary, and this can be beneficial if the structure being returned has constraints or operations associated with it..
同様の解決策として、辞書の代わりにクラスを使用する方法がある. これは、返される構造体に制約(constraints)や操作(operations)が関連付けられている場合に有効.

### In Function Arguments.

Connascence of position also frequently occurs in function argument lists.
**また、関数の引数リストでも、位置の連結が頻繁に発生する**.
Consider the following function declaration from a mythical email-sending utility library:.
神話に登場する電子メール送信ユーティリティ・ライブラリの次のような関数宣言を考えてみまよう.

```python
def send_email(firstname, lastname, email, subject, body, attachments=None):
```

Code calling this send_email function must remember the order of arguments.
この**send_email関数を呼び出すコードは、引数の順番を覚えておく必要がある**.
Should that order ever change, all calling locations must also be updated.
この順番が変われば、すべての呼び出し位置も更新されなければならない.
This example could also be improved to connascence of name by passing a structured object (a class or dictionary) instead of a number of parameters..
この例でもData Structureのケースと同様に、**いくつかのパラメータを渡す代わりに、構造化されたオブジェクト(クラスや辞書)を渡すことで、connascence of nameへ改善することができる**.

## Connascence of Algorithm

Connascence of algorithm is when multiple components must agree on a particular algorithm..
複数のコンポーネントが特定のアルゴリズムに合意する必要がある場合、 Connascence of algorithm が発生する.

### In Data Transmission データ通信において。

Connascence of algorithm frequently occurs when two entities must manipulate data in the same way.
Connascence of algorithm は、2つの Entity が同じ方法でデータを操作する必要がある場合(?)に頻繁に発生する.
For example, if data is being transmitted from one service to another, some sort of checksum algorithm is commonly used.
例えば、あるサービスから別のサービスへデータを送信する場合、何らかのchecksum algorithm(=データ転送の成功失敗を調べる検出手法?)を使用するのが一般的.
The sender and receiver must agree on which algorithm is to be used.
**どのアルゴリズムを使用するかは、送信側と受信側で合意する必要がある**.
If the sender changes the algorithm used, the receiver must change as well.
**送信者が使用するアルゴリズムを変更した場合、受信者も変更する必要がある.**

### In Data Validation and Encoding. データバリデーションとエンコードにおいて

Consider a hypothetical piece of software that required users to provide a valid email address when creating an account.
アカウント作成時に有効な電子メールアドレスの入力が必要なソフトウェアがあったとする.
The software must validate that the email address is valid, but this might happen in several places, including:.
ソフトウェアは、電子メールアドレスが有効であることを検証する必要がありますが、これは次のようないくつかの場所で発生する可能性がある.

- In a database model object..データベースモデルオブジェクトで...
- In a webapp 'controller' class method.. Webアプリの「コントローラ」クラスで、メソッドを...
- In a form field in the front-end UI.. フロントエンドのUIにあるフォームフィールドで

These pieces of code might well be in different languages, and will almost certainly be far apart from each other.
**これらのコードの断片は、異なる言語である可能性が高く、ほぼ確実に互いに離れていることだろう**.
The consequence of these algorithms being different might include users not being able to register, but recieving no feedback as to why..
これらのアルゴリズムが異なる結果、ユーザは登録できないが、その理由についてはフィードバックされないということがあるかもしれない.

Another common example of connascence of algorithm is when unicode strings are written to disk.
また、**connascence of algorithmの例として、unicode文字列をディスクに書き込む場合**がよくある.
Imagine a hypothetical piece of software that writes a data string to a cache file on disk:.
disk:上のcacheファイルにデータ列を書き込む仮想のソフトウェアを想像してください.

```python
def write_data_to_cache(data_string):
    with open('/path/to/cache', 'wb') as cache_file:
        cache_file.write(data_string.encode('utf8'))
```

A matching function is used to retrieve the data from the cache file:.
マッチング機能により、cacheファイルからデータを取得する:

```python
def read_data_from_cache():
    with open('/path/to/cache', 'rb') as cache_file:
        return cache_file.read().decode('utf8')
```

The connascence of algorithm here is that both functions must agree on the encoding being used.
**ここでいうアルゴリズムとは、両functionが使用するencodingに同意することである**.
If the write_data_to_cache function changes to encrypt the data on disk (the data being stored is potentially sensitive), the read_data_from_cache must also be updated..
write_data_to_cache関数がディスク上のデータを暗号化するように変更された場合(保存されているデータは潜在的に機密である)、read_data_from_cacheも更新する必要がある.

### In Test Code.テストコードで。

Test code often contains connascence of algorithm.
**テストコードには、多くの場合、アルゴリズムの組み合わせが含まれている**.
Consider this hypothetical test:.
次のような仮説的なテストを考えてみよう.

```python
def test_user_fingerprint(self):
    user = User.new(name="Thomi Richards")
    actual = user.fingerprint()
    expected = hashlib.md5(user.name).hexdigest()
    self.assertEqual(expected, actual)
```

This test is supposed to be testing that the 'fingerprint' method of the User class works as expected.
このテストは、Userクラスの'fingerprint'メソッドが期待通りに動作することをテストするものだと思われる.
However, it contains connascence of algorithm, which limits it's effectiveness.
しかし、アルゴリズムの連結を含んでいるため、その効果は限定的である.
If the User class ever changes the way fingerprints are calculated, this test will fail..
**Userクラスがfingerprints(指紋)の算出(出力)方法を変更することがあれば、このテストは失敗する**.
