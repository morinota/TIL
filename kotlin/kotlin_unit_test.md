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