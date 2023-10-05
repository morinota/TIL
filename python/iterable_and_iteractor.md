## link

- https://utokyo-ipp.github.io/4/4-2.html

# for文とIterableとIterator

- for文によって繰り返す事ができるオブジェクトの総称 = **Iterable**
- for文が様々なデータ型をIterableとして統一的に扱えるのは、繰り返して取り出す操作を表現する **Iterator** を経由するから。

## build-in関数 `iter()`

- build-in関数 `iter()`は、IterableからIteratorを作る。
  - `iter()`に渡されるオブジェクトのデータ型によって、適切なIteratorが構成される。for文は`iter()`によって、様々なデータ型を統一的に扱える。

```
>>> it = iter([0,1,2])
>>> it
<list_iterator object at 0x000001F4B6103DC0>
```

## build-in関数 `next()`

- build-in関数 `next()`は、Iteratorに対して繰り返しを1回分先に進める操作を与える。`next()`を呼び出す度に、Iteratorから順に要素が取り出されていく。
  - `next()`に渡されたIteratorが、繰り返しの終端に到達していた場合には、`StopIteration`という例外が発生する。

```
>>> next(it)
0
>>> next(it)
1
>>> next(it)
2
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

## for文の仕組み

- for文は、`iter()`, `next()`, `StopIteration`を使ったwhile文の形で表現できる。
  - ex. 以下の2つのコードは等価。
    - try-except文は、発生した例外を捉えて、適切に処理する為の構文。
    -

```python
>>> for x in [0,1,2]:
...     print(x)
...
0
1
2
```

```python
>>> try:
...     it = iter([0,1,2])
...     while True:
...         x = next(it)
...         print(x)
... except StopIteration:
...     pass
...
0
1
2
```

## Iteratorは特殊なIterable

- Iterator自身もIterable。よって、Iteratorをfor文で繰り返せる。
  - しかし、1つのfor文で使い切りの特殊なIterable。
    - 1つ目のfor文で終端に到達したIteratorは、その後の`next()`において`StopIteration`を発生させ続ける。
  - これは、Iterator に対して `iter()`を適用した時に、そのままIterator自身が返される仕組みだから。

```python
>>> it = iter([0,1,2])
>>> it is iter(it)
True
```

## Iterable は Iteratorではない。

- Iterableは一般にIteratorではない。
  - よって`next()`を適用できない。
  - `iter()`の適用によって毎回別のIteratorが返される。
  - ->複数のfor文で何度も繰り返す処理が実行できる。

## `enumerate`はIterableを受け取りIteratorを返す

`next()`が使えるのでiteratorを返す。

```python
>>> it = enumerate([10,20,30])
>>> it
<enumerate object at 0x000001F4B62E4BC0>
>>> next(it)
(0, 10)
```

## IterableとIteratorの定義をまとめる

- Iterable:
  - `iter()`を適用可能。`__iter__`メソッドを持つ。(両者は等価)
- Iterator:
  - `next()`を適用可能。`__next__`メソッドを持つ。(両者は等価)
  - `iter()`を適用した時、引数のオブジェクトをそのまま返す。
