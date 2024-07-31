## refs:

- [Polars日本語ユーザガイド](https://polars-ja.github.io/docs-ja/user-guide/getting-started/#polars)
- [patitoのREADME](https://github.com/JakobGM/patito/blob/main/README.md)


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


# Patitoによるデータ検証

## data valiadionの基本

```python
# models.py
from typing import Literal

import patito as pt


class Product(pt.Model):
    product_id: int = pt.Field(unique=True)
    temperature_zone: Literal["dry", "cold", "frozen"]
    is_for_sale: bool
```

```python
import polars as pl

df = pl.DataFrame(
    {
        "product_id": [1, 1, 3],
        "temperature_zone": ["dry", "dry", "oven"],
    }
)
try:
    Product.validate(df)
except pt.exceptions.DataFrameValidationError as exc:
    print(exc)
# 3 validation errors for Product
# is_for_sale
#   Missing column (type=type_error.missingcolumns)
# product_id
#   2 rows with duplicated values. (type=value_error.rowvalue)
# temperature_zone
#   Rows with invalid values: {'oven'}. (type=value_error.rowvalue)
```

## Synthesize valid test data (有効なテストデータの生成)

- Patitoはデータフレーム入力を厳密に検証し、実行時の正確性を保証することを推奨している。
- しかし、正確さを強制することは、特に単体テストにおいて多くのfriction(摩擦？制約?)が発生してしまう

### テストデータの作成が面倒になる例

以下の純粋関数をテストしたいとする。

```python
import polars as pl
import patito as pt

class Product(pt.Model):
    product_id: int = pt.Field(unique=True)
    temperature_zone: Literal["dry", "cold", "frozen"]
    is_for_sale: bool


def num_products_for_sale(products: pl.DataFrame) -> int:
    """販売中の商品の数を返す""" 
    Product.validate(products)
    return products.filter(pl.col("is_for_sale")).height
```

- この純粋関数の観察可能な振る舞いは、`is_for_sale`列の値が`True`である行の数を返すこと
  - -> よって 入力データ products内で本テストのために重要なカラムは `is_for_sale` のみ...! 
  - なので、`is_for_sale` カラムを強調したテストデータを用意したい。たとえば以下。

```python
def test_num_products_for_sale():
    products = pl.DataFrame({"is_for_sale": [True, True, False]})
    assert num_products_for_sale(products) == 2
```

- しかし、PatitoによってDataFrameがProductモデルを満たすか否かの厳密な検証が行われるため、上記のシンプルでわかりやすいテストケースは `patito.exceptions.DataFrameValidationError` で失敗してしまう。
- このテストを通すためには、`temperature_zone` や `product_id` カラムに有効なダミーデータを追加する必要がある。
  - **しかし、データ検証をパスするために、全てのテストデータに多くのボイラープレート(定型文)が追加されてしまい、各テストで実際に何がテストされているのかがわかりにくくなってしまう...!** (わかる、辛い...!:sob:)
  - このような問題を解決するために、**Patitoでは、与えられたモデルスキーマに完全に準拠したテストデータを生成するための `examples()` constructor** を提供してる

```python
Product.examples({"is_for_sale": [True, True, False]})
# shape: (3, 3)
# ┌─────────────┬──────────────────┬────────────┐
# │ is_for_sale ┆ temperature_zone ┆ product_id │
# │ ---         ┆ ---              ┆ ---        │
# │ bool        ┆ str              ┆ i64        │
# ╞═════════════╪══════════════════╪════════════╡
# │ true        ┆ dry              ┆ 0          │
# ├╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ true        ┆ dry              ┆ 1          │
# ├╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┤
# │ false       ┆ dry              ┆ 2          │
# └─────────────┴──────────────────┴────────────┘
```

- `examples()`メソッドは通常のDataFrameコンストラクタと同様の引数を受け取る。
  - **主な違いは、指定されていない列に対して、有効なダミーデータを入力すること!**
- よって前述の単体テストは、以下のように書き換えられる。
  - `examples()`メソッドを使って、`is_for_sale`カラムのみを強調したテストデータを生成できる! -> テストケースの意図が明確にしたまま、データ検証をパスすることができる...!:thinking:

```python
def test_num_products_for_sale():
    products = Product.examples({"is_for_sale": [True, True, False]})
    assert num_products_for_sale(products) == 2
```

## Representing rows as classes(クラスとして行を表現する)

- DataFrameは、オブジェクト集合(=行集合?) に対して、ベクトル化された操作を実行するのに適している。
- **しかし、1つの行を取り出して、それを操作する場合、DataFrameのAPIは少し冗長になることがある**。(確かに...!:sob:)
  - Patitoは、モデル上で定義されたメソッドに、1行レベルのロジックを埋め込める...!

```python
class Product(pt.Model):
    product_id: int = pt.Field(unique=True)
    name: str

    @property
    def url(self) -> str:
        return (
            "https://example.com/no/products/"
            f"{self.product_id}-"
            f"{self.name.lower().replace(' ', '-')}"
        )
```

- このモデルクラスは、`from_row()`メソッドを使用して、**DataFrameの単一行からインスタンス化**できる。

```python
products = pl.DataFrame(
    {
        "product_id": [1, 2],
        "name": ["Skimmed milk", "Eggs"],
    }
)
milk_row = products.filter(pl.col("product_id" == 1))
milk = Product.from_row(milk_row)
print(milk.url)
# https://example.com/no/products/1-skimmed-milk
```

- `patito.DataFrame.set_model()`あるいは直接 `Product.DataFrame()` を使用してProductモデルとDataFrameを「接続」すると、`.get()`メソッドを使用してデータフレームから単一行に絞り込み、それをモデルインスタンスにcastできる。

```python
products = Product.DataFrame(
    {
        "product_id": [1, 2],
        "name": ["Skimmed milk", "Eggs"],
    }
)
milk = products.get(pl.col("product_id") == 1)
print(milk.url)
# https://example.com/no/products/1-skimmed-milk
```
