import numpy as np
import polars as pl
from datetime import datetime

from typing import Literal, Optional

import patito as pt

df = pl.DataFrame(
    {
        "integer": [1, 2, 3],
        "date": [
            datetime(2025, 1, 1),
            datetime(2025, 1, 2),
            datetime(2025, 1, 3),
        ],
        "float": [4.0, 5.0, 6.0],
        "string": ["a", "b", "c"],
    }
)
print(df)
print(df.columns)

# select columns
df.select(pl.col("*"))  # select all columns
df.select(pl.col("integer", "float"))  # select specific columns

# 抽出 (filter)
# filterによりDataFrameのsubsetを作成できる
df.filter(pl.col("date").is_between(datetime(2025, 1, 1), datetime(2025, 1, 2)))
# 複数のカラムを含む、より複雑な条件を指定することも可能
df.filter(
    (pl.col("integer") == 1) & (pl.col("float") == 4.0) & (pl.col("string") == "a")
)

# add column
# with_columnを使って新しいカラムを追加できる
df.with_columns((pl.col("integer") * 2).alias("integer_double"))

# グループ化して新しいDataFrameを作成する
## group_byで得られた新しいDataFrameは、グループ分けしたい複数の「グループ」を持つ
df2 = pl.DataFrame(
    {
        "x": range(8),
        "y": ["A", "A", "A", "B", "B", "C", "X", "X"],
    }
)
df2_groupby = df2.group_by("y", maintain_order=True).agg(
    pl.col("x").sum().alias("sum_x"),
    pl.col("x").count().alias("count_x"),
)
print(df2_groupby)

# method chainで複数の操作を組み合わせて行う
df_x = df.with_columns((pl.col("integer") * 2).alias("integer_double")).select(
    pl.all().exclude(["integer"])
)
print(df_x)

# 複数のDataFrameを組み合わせる
## usecaseに応じて、2つの方法がある: join と concat
## join (left, right, inner, outer)
df = pl.DataFrame(
    {
        "a": range(8),
        "b": np.random.rand(8),
        "d": [1, 2.0, float("nan"), float("nan"), 0, -5, -42, None],
    }
)
df2 = pl.DataFrame(
    {
        "x": range(8),
        "y": ["A", "A", "A", "B", "B", "C", "X", "X"],
    }
)
joined = df.join(df2, left_on="a", right_on="x", how="inner")
print(joined)

## concat (2つのDataFrameを、水平方向 or 垂直方向に連結する)
## 水平方向に連結(horizontally stacked) (多分、行数が一致してる必要がある...!)
stacked = df.hstack(df2)
print(stacked)

# PatitoでpolarsのDataFrameのレコードをpydantic的にvalidate & parseする


## data modelの定義
class Product(pt.Model):
    # int型で値がユニークな必要がある
    pruduct_id: int = pt.Field(unique=True)
    # 有効な値をenumで指定する
    perature_zone: Literal["dry", "cold", "frozen"]
    is_for_sale: bool


## データを取得
invalid_df = pl.DataFrame(
    {
        # id = 1が重複してるので、エラーが発生する
        "pruduct_id": [1, 1, 3],
        # overは有効な値ではないので、エラーが発生する
        "perature_zone": ["dry", "cold", "oven"],
        # is_for_sale列が存在しないので、エラーが発生する
    }
)
valid_df = pl.DataFrame(
    {
        "pruduct_id": [1, 2, 3],
        "perature_zone": ["dry", "cold", "frozen"],
        "is_for_sale": [True, False, True],
    }
)

## 取得したデータのvalidate & parse
# Product.validate(invalid_df) # -> ValidationError
Product.validate(valid_df)

# polarsのDataFrameへの処理をSQLで書く
## SQLContextオブジェクトを作成 (初期化時にdfをテーブルとして登録)
ctx = pl.SQLContext(hogehoge_table=valid_df, fugafuga_table=df)
## executeメソッドを使って、SQLクエリを実行する(eager=Trueを指定すると、結果をDataFrameで返す)
print(
    ctx.execute(
        query="SELECT * FROM hogehoge_table WHERE is_for_sale = True", eager=True
    )
)
print(ctx.execute(query="SELECT * FROM fugafuga_table", eager=True))
## Polars SQLで利用可能な構文については、例えば以下を参照
### https://qiita.com/oba_atsushi/items/d40d17ca4e2acb0b71c5#polars-sql%E3%81%A7%E5%88%A9%E7%94%A8%E5%8F%AF%E8%83%BD%E3%81%AA%E6%A7%8B%E6%96%87
