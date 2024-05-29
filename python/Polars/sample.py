import numpy as np
import polars as pl
from datetime import datetime


def main():
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


if __name__ == "__main__":
    main()
