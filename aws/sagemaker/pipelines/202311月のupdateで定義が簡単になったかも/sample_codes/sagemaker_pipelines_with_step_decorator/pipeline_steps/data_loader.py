import polars as pl


def load_news_metadata_from_s3(parquet_s3_uri: str) -> pl.DataFrame:
    import polars as pl

    return pl.read_parquet(parquet_s3_uri)
