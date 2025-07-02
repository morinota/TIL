import pandera.polars as pa
import polars as pl


class Schema(pa.DataFrameModel):
    state: str
    city: str
    price: int = pa.Field(in_range={"min_value": 5, "max_value": 20})


lf = pl.LazyFrame(
    {
        "state": ["FL", "FL", "FL", "CA", "CA", "CA"],
        "city": ["Orlando", "Miami", "Tampa", "San Francisco", "Los Angeles", "San Diego"],
        "price": [8, 12, 10, 16, 20, 18],
    }
)

# バリデーションを実行
Schema.validate(lf)
