import polars as pl


def main():
    feature_df = pl.DataFrame(
        {
            "user_id": ["user_1", "user_2", "user_3"],
            "職種": ["営業", "デザイナー", "エンジニア"],
            "趣味": ["釣り", "サッカー", "盆栽"],
        }
    )
    print(feature_df)

    feature_hashed_df = _feature_hashing(
        df=feature_df,
        feature_cols=["職種", "趣味"],
        hash_size=8,
    )
    print(feature_hashed_df)


def _feature_hashing(df: pl.DataFrame, feature_cols: list[str], hash_size: int) -> pl.DataFrame:
    """Hashing Trick (Feature Hashing)を適用して特徴量を圧縮するサンプル関数

    Args:
        df (pl.DataFrame): 入力データフレーム
        feature_cols (list[str]): ハッシュ化する特徴量の列名リスト
        hash_size (int): ハッシュテーブルのサイズ（圧縮後の次元数）

    Returns:
        pl.DataFrame: ハッシュ化された特徴量を含むデータフレーム
    """
    # return df  # TODO: 実装する


if __name__ == "__main__":
    main()
