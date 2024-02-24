## refs

- [サーバーサイド Kotlin のテストフレームワーク事情](https://www.slideshare.net/mikeneck/kotlin-237365895)
- https://kotest.io/
- [Kotestでのユニットテスト - Kotest基本構文編](https://zenn.dev/maiya/articles/2e6d7575cc1e87)
- [Kotest Testing Styles](https://kotest.io/docs/framework/testing-styles.html)

# サーバサイドkotlinで主に使われるtest framework

- 主なtest frameworkは以下の通り。
  - JUnit Jupiter: Javaっぽいやつ? JavaのJUnit5の後継。
  - Spek: BDD(Behavior Driven Development)っぽいフレームワーク
  - Kotest: 様々なテストスタイルをサポートするフレームワーク。以前はKotlintestという名前だったらしい。

# Kotest:

## KotestのSpec(Specification)という概念:

以下は公式のサンプルコード。

> Kotest allows tests to be created in **several styles**, so you can choose the style that suits you best.

色んなスタイルで記述できるのが特徴っぽい。

```kotlin
class MyTests : StringSpec({
   "length should return size of string" {
      "hello".length shouldBe 5
   }
   "startsWith should test for a prefix" {
      "world" should startWith("wor")
   }
})
```

- **Spec(Specification)**という概念について:
  - テストの構造や形式を定義するもの。
  - テストケースをグループ化し、テストの文脈や意図を明確に表現するためのもの。
    - Specは、テストされる機能(function)の「仕様(=観察可能な振る舞い)」を記述するためのコンテナとして機能し、**テストケース(or テスト)の集まり**を定義する。
  - Kotestは複数のSpecスタイルをサポート。
    - それぞれが異なるテストの表現やアプローチを提供する。
    - 開発者はプロジェクトの要件や個人のテスト哲学に合わせて、最適な書き方を選択できる。
- 以下はSpec(Specification)の種類:

### String Spec:

- 最もシンプルなスタイル。テストケースも文字列で記載。
- ブロック単位でテストする。
- ただし階層的なテスト構造は作れない。(i.e. nestedはできない)

```kotlin
class CalcServiceStringSpecTest : StringSpec() {
    private val sut = Calc()

    init {
        "1 + 1 は2になる" { // 文字列が単一のテストケース
            sut.plus(1, 1) shouldBe 2
        }
        "5 ÷ 0 は例外が投げられる" {
            shouldThrow<ArithmeticException> { sut.divide(5, 0) }
        }
    }
}
```

### Fun Spec:

- testという関数を実行して処理を呼び出す。
- `context`という関数を使って、テストケースを階層構造にすることができる。

```kotlin
class CalcServiceFunSpecTest : FunSpec() {
    private val calc = Calc()

    init {
        context("CalcServiceTest") {
            context("正常系") {
                test("1 + 1 は2になる") {
                    calc.plus(1, 1) shouldBe 2
                }
            }
            context("異常系") {
                test("5 ÷ 0 は例外が投げられる") {
                    shouldThrow<ArithmeticException> { calc.divide(5, 0) }
                }
            }
        }
    }
}
```

### Expect Spec

- Fun Specのtestの代わりにexpectという関数を実行して処理を呼び出す。

### Should Spec

- Fun Specのtestの代わりにshouldという関数を実行して処理を呼び出す。
- `context`関数だけではなく、文字列によってもテストケースをグループ化できる。

### Describe Spec

- context関数だけでなく、descrpibe関数を使って、テストケースを階層構造にすることができる。
- Fun Specのtest関数の代わりにit関数を使ってテストケースを記述する。

### Behavior Spec

- given, when, thenでテストを定義して処理を呼び出す。

### Free Spec

- 文字列テキストと `-`を定義して処理を呼び出す。
- 階層化できる。
- どういったスタイルのテストか判別しづらく分かりづらい。

## KotestのAssertion

- shouldBe, shouldNotBe:
- shouldThrow:
  - 例外が投げられることを確認する。
-

# kotlinにおけるテストダブルの用意の仕方とmock機能

- テストダブル = 単体テストにおいて、対象の振る舞いが依存している外部リソースやクラスを置き換えるためのもの。
- テストダブを用意する方法の一つとして、mock機能を使う方法がある。
  - (テストダブルの種類の1つのmockではなく、機能としてのmockのこと!)
- kotlinにおけるmock機能としては、mockkというライブラリが一般的っぽい。

## mockkについて

- Mockkは、kotlin専用のmockingライブラリ。

### 主要なfunction 1. mockオブジェクトを作る。

- mockk(): mockオブジェクトを生成する。
  - 通常のmockオブジェクトは、特定のメソッドの振る舞いを`every{}`で明示的に定義しない限り、未定義のメソッドを呼び出すと例外 `io.mockk.MockKException` が投げられる。
- `mockk(relaxed = true)`: relaxed mockオブジェクトを生成する。
  - **relaxed mockオブジェクト**: 未定義のメソッドを呼び出しても例外が投げられずに、**データ型のデフォルト値を良い感じにdummyとして返す**mockオブジェクト。
  - ex.
    - 返り値がInt型のメソッドを呼び出すと0が返る。
    - Boolean型のメソッドを呼び出すとfalseが返る。
    - nullableなオブジェクトであればnullが返る。
    - non-nullなオブジェクトであれば新しいmockインスタンスが返る。
- 各テストの用途に応じて、通常のmockオブジェクトとrelaxed mockオブジェクトを使い分ける必要がある...!:thinking_face:
  - relaxed mockオブジェクトは、返り値の検証を必要としないテストケースとかで使えて、振る舞いを指定する手間が省けるので便利。

ex.

```kotlin
val mockUserRepo = mockk<UserRepository>() // テストダブルを用意して
val sut = UserService(mockUserRepo) // sutにdependency injection
```

- every関数でmockオブジェクトの特定のメソッドの振る舞いを明示的に定義する。
  - 通常のmockオブジェクトの場合は、基本的にpublicなメソッドの振る舞いはeveryで明示的に定義しておく必要がありそう...!:thinking_face:
  - 例外を発生させる事も可能。

```kotlin
// example
every { mockUserRepo.getUser(userId) } returns expectedUser

every { mockUserRepo.getUser(userId) } throws NoSuchElementException("User not found")
```

- relaxed mockオブジェクトの注意点:ジェネリクスメソッド (=返り値の型がジェネリクス, i.e. 具体的じゃない) の場合、`ClassCastException`が発生してしまう!
  - なぜ?
    - relaxed mockオブジェクトは、返り値のデータ型に基づいてデフォルトの値を返そうとする。**ジェネリクスメソッドの場合、返り値の具体的なデータ型が実行時までわからない為**、mockkは正しいデータ型のオブジェクトを生成して返す事ができない。
  - 対処法:
    - relaxed mockオブジェクトを使用する場合でも、ジェネリクスメソッドを呼び出す必要がある場合は、可能な限り`every {} returns {}`で振る舞いを明示的に定義する!
- ex.

```kotlin
// ジェネリクスメソッドを持つfactoryクラス
interface Factory {
    fun <T> create(): T
}

@Test
fun testMockKSample() {
    val factory = mockk<Factory>(relaxed = true) //
    every { factory.create<Car>() } returns Car() // 明示的に振る舞いを定義しないとClassCastExceptionが発生する

    val car = factory.create<Car>()
}
```

- [参考](https://qiita.com/sadashi/items/81c64583a0112cfe6f8d)によると、オブジェクトもモック化できたり、返り値がUnit型(=値を返さない! voidみたいな!)のメソッドだけをrelaxex mockしてくれるoptionがあったりする。
  - 返り値がUnit型、つまり値を返さないということは、副作用のみを持つメソッド(ex. ログの記録、状態の更新)などをテストする時に便利。(i.e. 返り値の検証が不要なテスト。じゃあこの場合はvarifyでメソッド呼び出しを検証するのかな...?:thinking_face:)

### 主要なfunction 2. verifyでメソッド呼び出しを検証

- verify関数はモックオブジェクトのメソッド呼び出しを検証するための関数。
  - 例えば、特定のメソッドが特定の回数呼び出されたかどうかを検証することができる。

```kotlin
// example
verify(exactly = 1) { mockUserRepo.getUser(userId) }
```
