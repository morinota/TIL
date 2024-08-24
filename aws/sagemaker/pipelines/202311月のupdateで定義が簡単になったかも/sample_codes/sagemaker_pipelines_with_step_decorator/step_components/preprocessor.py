import polars as pl


def preprocess(
    raw_data_s3_path: str, output_prefix: str
) -> tuple[str, str, str, pl.DataFrame]:
    """raw_dataをfor_train, for_valid, for_testの3つに分割する処理を仮定する"""
    # Loguruを使ったlogging
    from loguru import logger
    import polars as pl

    # raw_data_s3_pathディレクトリ以下のparquetファイルを読み込む
    df = pl.read_parquet(f"{raw_data_s3_path}/000.parquet")
    logger.debug(f"{raw_data_s3_path=}")
    logger.debug(f"{output_prefix=}")
    logger.debug(f"{df=}")

    _private_func1()

    train_s3_path = f"{output_prefix}/for_train.parquet"
    valid_s3_path = f"{output_prefix}/for_valid.parquet"
    test_s3_path = f"{output_prefix}/for_test.parquet"
    return (train_s3_path, valid_s3_path, test_s3_path, df)


def _private_func1() -> None:
    print("run _private_func1")
