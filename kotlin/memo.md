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

## functions

関数本体は式にすることができる. その場合,戻り値の型は推測(infer)される.

```kotlin
fun sum(a: Int, b: Int): Int {
    return a + b
}
fun sum(a: Int, b: Int) = a + b

```

## Nullable values and null checks

NULL値が可能な場合、参照は明示的にNULL可能であるとマークする必要がある。Nullableな型名には末尾に`?`が付く.

`str`が整数を保持していない場合は`null`を返す。

```kotlin
fun parseInt(str: String): Int? {
    // ...
}
```
