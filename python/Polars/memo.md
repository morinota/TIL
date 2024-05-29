## refs:

- [Polars日本語ユーザガイド](https://polars-ja.github.io/docs-ja/user-guide/getting-started/#polars)


# データ構造

Polarsが提供する基本データ構造は Series と DataFrame。

- Series
  - 1次元のデータ構造。
  - Series内の全ての要素は同じデータ型を持つ。
- DataFrame
  - 2次元のデータ構造。
  - Seriesのcollection(listなど)の抽象化と見なすことができる。
  - DataFrameで実行できる操作は SQL クエリと非常によく似ている。
    - ex. GROUP BY, JOIN, PIVOT, etc.
    - カスタム関数を定義する事もできる。

データの表示は、pandasと似たような感じ。

- head()
- tail()
- describe()
- sample()

# データ変換

