refs: https://pandera.readthedocs.io/en/latest/polars.html

- Panderaはデータフレームのバリデーション（検証）をするPythonライブラリ
- panderaのPolars統合は、バージョン0.19.0で導入された。これにより、Pythonでpanderaスキーマを定義し、Polarsデータフレームの検証を行うことができる。
- 
- 


## ざっくり使い方

```python
import pandera.polars as pa
import polars as pl

class Schema(pa.DataFrameModel):
    state: str
    city: str
    price: int = pa.Field(in_range={"min_value": 5, "max_value": 20})

lf = pl.LazyFrame({
    'state': ['FL','FL','FL','CA','CA','CA'],
    'city': ['Orlando', 'Miami', 'Tampa', 'San Francisco', 'Los Angeles', 'San Diego'],
    'price': [8, 12, 10, 16, 20, 18],
})

# バリデーションを実行
Schema.validate(lf).collect()
```

## Polars DataFrameのスキーマ定義

- panderaでは、Polars DataFrameのスキーマを定義するために、**主にクラスベースAPIとオブジェクトベースAPIの2つの方法**がある。
  - クラスベースAPI (`DataFrameModel`)  
    - Pythonのクラスと型ヒントを使用してスキーマを定義する。これは、**より宣言的で読みやすい方法**である。
    - ex. pandera.polars.DataFrameModelを継承し、列名と型をアノテーションとして指定する。pa.Fieldを使用して、min_valueやmax_valueのような制約を追加できる。
  - オブジェクトベースAPI (`DataFrameSchema`)
    - pandera.polars.DataFrameSchemaをインスタンス化してスキーマを定義します。これは、**より柔軟な定義が可能**。
    - pa.Columnを使用して各列の型を指定し、pa.Checkを使用してチェックを追加できる。

## タイプヒントとデコレータ

- pandera.typing.polars.LazyFrameを使用して、関数の引数と戻り値に型ヒントを付けることができる。
- @pa.check_typesデコレータを使用すると、ランタイムでこれらのアノテーションをvalidateできる。

## PolarsのLazy/Eagerな特性と検証の仕組み

- pl.LazyFrame：遅延評価。バリデーションは「スキーマレベル（型やカラム名）」だけ先にやって、値チェックは.collect()で実行される。
- pl.DataFrame：即時評価。バリデーションは「スキーマ＋値」どっちも一気にやる。

panderaは、PolarsのLazy API (遅延評価) を最大限に活用することで、クエリ最適化のメリットを享受しようとする。

validate()の流れは以下:

1. パーサーの適用: `add_missing_columns=True`であれば不足している列を追加し、`coerce=True`であればデータ型を強制変換し、`strict="filter"`であれば列をフィルタリングし、`default=<value>`であればデフォルト値で穴埋めする。
2. チェックの適用: コア、組み込み、カスタムのすべてのチェックを実行する。メタデータに対するチェックは.collect()操作なしで行われるが、データ値を検査するチェックは.collect()を伴う。
3. エラーの発生: データエラーが見つかった場合、`SchemaError`が即座に発生する。もし`validate`メソッドが`lazy=True`で呼び出された場合、データ内の全てのvalidationエラーを含む`SchemaErrors`例外が返される。
4. validate済み出力の返却: データエラーが見つからなかった場合、validate済みのオブジェクトが返される。

### Pl.LazyFrameとPl.DataFrameの検証動作

- panderaの検証動作は、**PolarsがLazy (遅延) 操作とEager (即時) 操作をどのように扱うかに整合**している。
- polars.LazyFrameのvalidation操作:
  - schema.validate()をpolars.LazyFrameに対して呼び出す場合、panderaはスキーマレベルのプロパティのみを検証する。
  - これは、列名やデータ型など、.collect()操作を必要としない検証のみが行われることを意味する。
  - データ型の強制変換も.collect()なしで行われる。
  - 例: データ値の範囲チェックなどのデータレベルのチェックは、デフォルトでは実行されない。
- polars.DataFrameのvalidation操作:
  - panderaはpolars.DataFrameオブジェクトも検証できる。**polars.DataFrameは計算を即座に実行するオブジェクト**である。
  - polars.DataFrameをvalidateする場合、panderaはスキーマレベルとデータレベルの両方の検証を実行する。
  - 内部的な変換: 
    - **panderaは、内部的にpolars.DataFrameをpolars.LazyFrameに変換してから検証を実行する**。これは、PolarsのLazy APIが提供する最適化を利用するため。
    - **validate後も、入力がpolars.DataFrameであれば、polars.DataFrameとして返されます (これはソースには明示されていないが、一般的な挙動として推測される)**。
      - あ、だからタイプヒントで赤線が出てしまうのか! ソースに明示されてないから...!

## エラーレポート

panderaは、検証エラーが発生した場合に、以下のようにエラーを報告する。
