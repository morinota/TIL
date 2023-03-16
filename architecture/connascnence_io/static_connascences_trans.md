## link リンク

- https://connascence.io/name.html https

# Static Connascences スタティック・コナシオン

## Connascence of Name 名前のコナシです。

Connascence of name is when multiple components must agree on the name of an entity.
Connascence of nameとは、あるエンティティの名前について、複数のコンポーネントが同意しなければならない場合である。
Method names are an example of this form of connascence: if the name of a method changes, callers of that method must be changed to use the new name..
メソッド名が変われば、そのメソッドの呼び出し元も新しい名前を使うように変更しなければなりません。

Almost any code example involves connascence of name.
ほとんどのコード例では、名前の連結を伴います。
Consider the following class declaration taken from the Python standard library (method implementation has been omitted for clarity):.
Python標準ライブラリから引用した次のクラス宣言を考えてみましょう（わかりやすくするためにメソッドの実装は省略されています）。

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
このコードのいずれかの部分の名前を変更すると、このクラスを使用するコードが次のように壊れることがあります。

- Changing the class name from Request. クラス名をRequest...から変更する

- Changing any of the method names (such as set_proxy). メソッド名（set_proxyなど）を変更する。

- Changing the name of any of the parameters to either **init** or set_proxy. パラメータ名を **init** または set_proxy のいずれかに変更する。

Connascence of name is unavoidable, since we refer to entities using labels.
ラベルを使って実体を参照するため、名前の共起は避けられない。
If we change the name of an entity when we declare it, we must also change all code that refers to that entity.
エンティティの宣言時に名前を変更した場合、そのエンティティを参照するすべてのコードも変更しなければなりません。
For this reason, connascence of name is the weakest connascence.
そのため、名前の連結は最も弱い連結となります。
However, it also illustrates how important it is to name entities in code well..
しかし、コード内のエンティティにうまく名前をつけることがいかに重要であるかということも示しています。

## Connascence of Type Connascence of Type.

Connascence of type is when multiple components must agree on the type of an entity.
Connascence of typeとは、複数のコンポーネントがエンティティのタイプに同意する必要がある場合です。
In a statically typed language, these issues are often (but not always) caught by the compiler.
静的型付け言語では、このような問題はコンパイラによって捕捉されることが多い（しかし、常にそうとは限らない）。
Consider the following trivial C++ code:.
次のような些細なC++コードを考えてみましょう。

```
std::string cost;

cost = 10.95; // OOPS!
```

Dynamically typed languages typically suffer from less obvious instances of connascence of type.
動的型付けされた言語は、一般的に、あまり目立たないタイプの共起に悩まされる。
Consider a function that calculates your age, given your day, month, and year of birth:.
生年月日、月、年が与えられて、年齢を計算する関数を考えてみましょう。

```python
def calculate_age(birth_day, birth_month, birth_year): # do the calculation here:
```

How is this function supposed to be called? Here are a few different options:.
この関数はどのように呼び出すのでしょうか？以下は、いくつかの異なる選択肢です：。

```python
calculate_age(1, 9, 1984)
calculate_age(1, 9, 84)
calculate_age('1', '9', '1984')
calculate_age('1', 'September', '1984')
```

## Connascence of Meaning Connascence of Meaning.

Connascence of meaning is when multiple components must agree on the meaning of particular values.
Conascence of meaningとは、複数のコンポーネントが特定の値の意味について合意する必要がある場合です。
Consider some code that processes credit card payments.
クレジットカードの決済を処理するコードを考えてみましょう。
The following function might be used to determine if a given credit card number is valid or not:.
次の関数は、与えられたクレジットカード番号が有効かどうかを判断するために使用されるかもしれません：。

```
def is_credit_card_number_valid(card_number):
    # Check for 'test' credit card numbers:
    if card_number == "9999-9999-9999-9999":
        return True
    # Do normal validation:
    # ...
```

The problem here is that all parts of this system must agree that 9999-9999-9999-9999 is the test credit card number.
ここで問題になるのは、このシステムのすべての部分が、9999-9999-9999がテスト用クレジットカード番号であることに同意しなければならないということです。
If that value changes in one place, it must also change in another..
ある場所でその価値が変われば、別の場所でも変わるはずです。

Here's another example where user roles are encoded as integers:.
以下は、ユーザーのロールが整数としてエンコードされている例です。

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
他の場所では、次のように、指定されたユーザー名が管理者であるかどうかをチェックする必要がある場合があります。

```
if get_user_role(username) != 2:
    raise PermissionDenied("You must be an administrator")
```

Connascence of meaning can be improved to connascence of name by moving the "magic values" to named constants, and referring to the constants instead of the values.
意味の連結は、「魔法の値」を名前付き定数に移し、値の代わりに定数を参照することで、名前の連結に改善することができます。
However in doing so, we have increased the amount of connascence of name (since we now need a third location to store the constant)..
しかし、そうすることで、名前の連結が増えました（定数を保存するために3つ目の場所が必要になったからです）。

Another common example of connascence of meaning is when None is used as a return value.
また、「None」が戻り値として使われる場合も、意味の連鎖がよく起こる例です。
This frequently occurs in functions that are tasked with finding an object.
これは、オブジェクトを見つけることをタスクとする機能で頻繁に発生します。
If that object isn't found, the function might return None..
そのオブジェクトが見つからない場合、関数は None を返すかもしれません。

```python
def find_user_in_database(username):
    return database.find_user(username=username) or None
```

However, the function might also return None in an error condition:.
しかし、この関数は、エラー時にNoneを返すこともあります：。

```
def find_user_in_database(username):
    try:
        return database.find_user(username=username) or None
    except DatabaseError:
        return None
```

The problem in both these cases is that a semantic meaning is being assigned to the None value.
いずれの場合も、Noneの値に意味づけがされていることが問題である。
If multiple different meanings are assigned to the same None value in the same codebase, the programmer must remember which meaning applies to which case.
同じコードベースにおいて、同じNone値に複数の異なる意味が付与されている場合、プログラマはどのような場合にどの意味が適用されるかを覚えておかなければならない。
This can be improved to connascence of name by returning an explicit object that represents the case in question:.
これは、問題のケースを表す明示的なオブジェクトを返すことで、名前の連結に改善することができます：。

```
def find_user_in_database(username):
    try:
        return database.find_user(username=username) or ObjectNotFound
    except DatabaseError:
        return None
```

We still have connascence of meaning in the error case, but at least the None value is no longer ambigous.
エラーの場合はまだ意味の連結がありますが、少なくともNoneの値はもう曖昧ではありません。
The error case could also be improved to connascence of name in a similar way..
また、エラーケースも同様にconnascence of nameに改善される可能性があります。

Another common example of connascence of meaning is when we use primitive numeric types to represent more complex values.
また、原始的な数値型を使用してより複雑な値を表現する場合も、意味の連鎖が起こりやすい例と言えます。
Consider this line of code in a codebase that processes payments:.
決済を処理するコードベースにおいて、次のようなコード行を考えてみましょう。

```
unit_cost = 49.95
```

What currency is that cost expressed in? US dollars? British pounds? How do you ensure that two costs with different currencies are not added together? Similar to the examples above, the problem is that a semantic meaning is being added to the primitive type.
そのコストはどのような通貨で表現されているのでしょうか？USドル？イギリスポンド？通貨が異なる2つのコストが一緒に加算されないようにするにはどうしたらいいでしょうか？上の例と同様、プリミティブ型に意味的な意味が付加されていることが問題なのです。
It can be improved to connascence of type by creating a 'Cost' type that disallows operations between different currencies:.
異なる通貨間の操作を禁止する「コスト」タイプを作成することで、タイプの連結を改善することができます：。

```
unit_cost = Cost(49.95, 'USD')
```

This particular problem is often called "Primitive Obsession", and can be generically described as using primitive data types to represent more complex domains..
この問題は「プリミティブ・オブセッション」と呼ばれ、一般的には「より複雑な領域を表現するためにプリミティブなデータ型を使用する」と表現されることが多い。

## Connascence of Position Connascence of Position.

Connascence of position is when multiple entities must agree on the order of values..
地位の一致とは、複数の主体が価値観の順序について合意しなければならない場合である。

In Data Structures.
データ構造において。

For example, consider a function that retrieves a user's details:.
例えば、ユーザーの詳細情報を取得する関数を考えてみましょう：。

```python
def get_user_details():
    # Returns a user's details as a list:
    # first_name, last_name, year_of_birth, is_admin
    return ["Thomas", "Richards", 1984, True]
```

This is a somewhat contrived example, but it's not uncommon to see data returned in lists or tuples.
これはやや不自然な例ですが、データがリストやタプルで返されることは珍しくありません。
Elsewhere in the code we might need to perform some check on whether the user is an administrator or not:.
コードの別の場所で、ユーザーが管理者であるかどうかのチェックを行う必要があるかもしれません：。

```python
def launch_nukes(user):
    if user[3]:
        # actually launch the nukes
    else:
        raise PermissionDeniedError("User is not an administrator!")
```

These two functions are linked by connascence of position.
この2つの機能は、ポジションの連関でつながっています。
If the order of the values in the user list ever changes, both locations must be updated (this example is particularly scary if someone were to update the user list to be [first_name, initials, last_name, year_of_birth, is_admin] without updating the check inside launch_nukes)..
ユーザーリストの値の順序が変わることがあれば、両方の場所を更新しなければなりません（この例は、誰かがlaunch_nukes内のチェックを更新せずにユーザーリストを[first_name, initials, last_name, year_of_birth, is_admin]に更新した場合に特に怖いです）。

This connascence can be improved to connascence of name by turning the list into a dictionary or class.
このconnascenceは、リストを辞書やクラスにすることで、connascence of nameに改善することができます。
The following example shows how the above functions might look as a dictionary:.
次の例は、上記の関数が辞書としてどのように見えるかを示しています：。

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
この2つの関数はまだ結合していますが、位置の結合を名前の結合より弱いものに変えていることに注意してください。
This has also increased the readability of the get_user_details function - the explicit comment is no longer needed to document the order of the keys..
これにより、get_user_details関数の可読性が向上し、キーの順序を示す明示的なコメントが不要になりました。

A similar solution is to use a class instead of a dictionary, and this can be beneficial if the structure being returned has constraints or operations associated with it..
同様の解決策として、辞書の代わりにクラスを使用する方法があります。これは、返される構造体に制約や操作が関連付けられている場合に有効です。

In Function Arguments.
ファンクション・アーギュメントで。

Connascence of position also frequently occurs in function argument lists.
また、関数の引数リストでも、位置の連結が頻繁に発生する。
Consider the following function declaration from a mythical email-sending utility library:.
神話に登場する電子メール送信ユーティリティ・ライブラリの次のような関数宣言を考えてみましょう。

```python
def send_email(firstname, lastname, email, subject, body, attachments=None):
```

Code calling this send_email function must remember the order of arguments.
このsend_email関数を呼び出すコードは、引数の順番を覚えておく必要があります。
Should that order ever change, all calling locations must also be updated.
この順番が変われば、すべての呼び出し位置も更新されなければなりません。
This example could also be improved to connascence of name by passing a structured object (a class or dictionary) instead of a number of parameters..
この例では、いくつかのパラメータを渡す代わりに、構造化されたオブジェクト（クラスや辞書）を渡すことで、名前の接続を改善することができます。

## Connascence of Algorithm Connascence of Algorithm.

Connascence of algorithm is when multiple components must agree on a particular algorithm..
複数のコンポーネントが特定のアルゴリズムに合意する必要がある場合、アルゴリズムのコナスカンス（Connascence）が発生します。

In Data Transmission.
データ通信において。

Connascence of algorithm frequently occurs when two entities must manipulate data in the same way.
アルゴリズムのコナスカンスは、2つのエンティティが同じ方法でデータを操作する必要がある場合に頻繁に発生します。
For example, if data is being transmitted from one service to another, some sort of checksum algorithm is commonly used.
例えば、あるサービスから別のサービスへデータを送信する場合、何らかのチェックサムアルゴリズムを使用するのが一般的です。
The sender and receiver must agree on which algorithm is to be used.
どのアルゴリズムを使用するかは、送信側と受信側で合意する必要があります。
If the sender changes the algorithm used, the receiver must change as well..
送信者が使用するアルゴリズムを変更した場合、受信者も変更する必要があります。

In Data Validation and Encoding.
データバリデーションとエンコードにおいて。

Consider a hypothetical piece of software that required users to provide a valid email address when creating an account.
アカウント作成時に有効な電子メールアドレスの入力が必要なソフトウェアがあったとします。
The software must validate that the email address is valid, but this might happen in several places, including:.
ソフトウェアは、電子メールアドレスが有効であることを検証する必要がありますが、これは次のようないくつかの場所で発生する可能性があります。

In a database model object..
データベースモデルオブジェクトで...

In a webapp 'controller' class method..
Webアプリの「コントローラ」クラスで、メソッドを...

In a form field in the front-end UI..
フロントエンドのUIにあるフォームフィールドで

These pieces of code might well be in different languages, and will almost certainly be far apart from each other.
これらのコードの断片は、異なる言語である可能性が高く、ほぼ確実に互いに離れていることでしょう。
The consequence of these algorithms being different might include users not being able to register, but recieving no feedback as to why..
これらのアルゴリズムが異なる結果、ユーザーは登録できないが、その理由についてはフィードバックされないということがあるかもしれません。

Another common example of connascence of algorithm is when unicode strings are written to disk.
また、アルゴリズムの共生の例として、ユニコード文字列をディスクに書き込む場合がよくあります。
Imagine a hypothetical piece of software that writes a data string to a cache file on disk:.
disk:上のキャッシュファイルにデータ列を書き込む仮想のソフトウェアを想像してください。

```python
def write_data_to_cache(data_string):
    with open('/path/to/cache', 'wb') as cache_file:
        cache_file.write(data_string.encode('utf8'))
```

A matching function is used to retrieve the data from the cache file:.
マッチング機能により、キャッシュファイル:からデータを取得します。

```python
def read_data_from_cache():
    with open('/path/to/cache', 'rb') as cache_file:
        return cache_file.read().decode('utf8')
```

The connascence of algorithm here is that both functions must agree on the encoding being used.
ここでいうアルゴリズムとは、両機能が使用するエンコーディングに同意することである。
If the write_data_to_cache function changes to encrypt the data on disk (the data being stored is potentially sensitive), the read_data_from_cache must also be updated..
write_data_to_cache関数がディスク上のデータを暗号化するように変更された場合（保存されているデータは潜在的に機密である）、read_data_from_cacheも更新する必要があります。

In Test Code.
テストコードで。

Test code often contains connascence of algorithm.
テストコードには、多くの場合、アルゴリズムの組み合わせが含まれています。
Consider this hypothetical test:.
次のような仮説的なテストを考えてみましょう。

```python
def test_user_fingerprint(self):
    user = User.new(name="Thomi Richards")
    actual = user.fingerprint()
    expected = hashlib.md5(user.name).hexdigest()
    self.assertEqual(expected, actual)
```

This test is supposed to be testing that the 'fingerprint' method of the User class works as expected.
このテストは、Userクラスの'fingerprint'メソッドが期待通りに動作することをテストするものだと思われます。
However, it contains connascence of algorithm, which limits it's effectiveness.
しかし、アルゴリズムの連結を含んでいるため、その効果は限定的である。
If the User class ever changes the way fingerprints are calculated, this test will fail..
ユーザークラスが指紋の算出方法を変更することがあれば、このテストは失敗します。