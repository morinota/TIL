import numpy as np
import polars as pl


def train(
    train_s3_path: str,
    validation_s3_path: str,
    input_df: pl.DataFrame,
) -> np.ndarray:
    """trainデータとvalidデータを使って、モデル(np.ndarray)を作るステップを仮定する"""
    from loguru import logger

    logger.debug(f"receive {train_s3_path=}")
    logger.debug(f"receive {validation_s3_path=}")
    logger.debug(f"receive {input_df=}")
    return np.array([[1, 2, 3], [4, 5, 6]])
