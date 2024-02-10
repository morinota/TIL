## link

- https://kotlinlang.org/docs/learning-materials-overview.html

# Basic syntax

## パッケージの定義とインポート

packageの指定は、ソースファイルの先頭で行う.
ディレクトリとパッケージを一致させる必要はなく、ソースファイルはファイルシステム内に任意に配置することができる.

```kotlin
package my.demo

import kotlin.text.*

// ...
```

## program entry point

An entry point of a Kotlin application is the `main` function.

mainのもう一つの形式は、可変数のString引数を受け取る方法.

```kotlin
fun main(args: Array<String>) {
    println(args.contentToString())
}
```

## Print to the standard output

# functions

参考:https://play.kotlinlang.org/byExample/01_introduction/02_Functions

関数本体は式にすることができる. その場合,戻り値の型は推測(infer)される.

```kotlin
fun sum(a: Int, b: Int): Int {
    return a + b
}
fun sum(a: Int, b: Int) = a + b

```

## Nullable values and null checks

NULL値が可能な場合、参照は明示的にNULL可能であるとマークする必要がある。Nullableな型名には末尾に`?`が付く.

ex. `str`が整数を保持していない場合は`null`を返す。

```kotlin
fun parseInt(str: String): Int? {
    // ...
}
```

## Infix notation(Infix function)

infix キーワードでマークされた関数は、infix記法（呼び出しのためのドットや括弧を省略する）でも呼び出すことができる。infix 関数は、以下の要件を満たす必要があります：

メンバ関数または拡張関数であること。

パラメータは1つでなければならない。

パラメータは1つで、可変数の引数を受け入れてはならず、デフォルト値を持ってはならない。

```kotlin
infix fun Int.shl(x: Int): Int { ... }

// calling the function using the infix notation
1 shl 2

// is the same as
1.shl(2)
```

## Operator function(operator notation)

一部のfunctionはoperatorに "アップグレード "することができ、対応するオペレーターシンボルでの呼び出しが可能になる。

Kotlinでは、型に対する演算子の定義済みのセットに対して、カスタム実装を提供することができる。
これらの演算子は、あらかじめ定義された記号表現（+や\*など）と優先順位を持つ。
演算子を実装するには、対応する型に対して特定の名前を持つメンバ関数または拡張関数を提供します。この型は、二項演算の場合は左辺の型になり、単項演算の場合は引数の型になります。

演算子をオーバーロードするには、対応する関数に operator 修飾子を付ける：

## 可変長引数を取る Functions with vararg Parameters

Vararg修飾語句(modifier)が付与された変数は、カンマで区切って任意の数の引数を渡すことができる。

```kotlin
fun printAll(vararg messages: String) {                            // 1
    for (m in messages) println(m)
}
printAll("Hello", "Hallo", "Salut", "Hola", "你好")
```

名前付きパラメータのおかげで、varargの後に同じ型の別のパラメータを渡す事も可能。

```kotlin
fun printAllWithPrefix(vararg messages: String, prefix: String) {  // 3
    for (m in messages) println(prefix + m)
}
printAllWithPrefix(
    "Hello", "Hallo", "Salut", "Hola", "你好",
    prefix = "Greeting: "                                          // 4
)
```

実行時、varargは単なる配列.
これを 別のfunctionのvararg パラメータに渡すには、特殊な拡散演算子(spread operator) `*` を使用する.
これにより、entries (Array<String>) の代わりに \*entries (String の vararg) を渡すことができる.

```kotlin
fun log(vararg entries: String) {
    printAll(*entries)                                             // 5
}
log("Hello", "Hallo", "Salut", "Hola", "你好")
```
