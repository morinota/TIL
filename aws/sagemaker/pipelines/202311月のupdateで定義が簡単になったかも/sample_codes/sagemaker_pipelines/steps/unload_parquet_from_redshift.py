import argparse
from pathlib import Path
from utils import loader
import polars as pl


def main(params: argparse.Namespace) -> None:
    """サンプルの処理を実行する"""
    # 入力データを読み込む
    news_df = loader.load_news(INPUT_DATA_DIR / "news")

    # ニュースデータをベクトルにencodeする
    vector_df = vectorize_news_texts(news_df)

    # ベクトル化されたニュースデータを保存する
    vector_output_dir = OUTPUT_DATA_DIR / "news_vector"
    vector_output_dir.mkdir(parents=True, exist_ok=True)
    vector_df.write_parquet(vector_output_dir / "vectors.parquet")


def vectorize_news_texts(news_df: pl.DataFrame) -> pl.DataFrame:
    # ニュースデータをベクトルにencodeする処理を実装する
    return pl.DataFrame(
        [
            {"content_id": "xxxx", "vector": [1, 2, 3]},
            {"content_id": "yyyy", "vector": [4, 5, 6]},
            {"content_id": "zzzz", "vector": [7, 8, 9]},
        ]
    )


if __name__ == "__main__":
    # コマンドライン引数をパースする
    parser = argparse.ArgumentParser()

    # モデルのハイパーパラメータ引数
    parser.add_argument(
        "--sample_hyperparameter1",
        type=int,
        default=10,
        help="サンプルのハイパーパラメータ1",
    )
    parser.add_argument(
        "--sample_hyperparameter2",
        type=float,
        default=0.1,
        help="サンプルのハイパーパラメータ2",
    )
    parser.add_argument(
        "--sample_hyperparameter3",
        type=str,
        default="sample",
        help="サンプルのハイパーパラメータ3",
    )
    parser.add_argument(
        "--INPUT_DATA_DIR",
        type=str,
        default="/opt/ml/processing/input",
        help="入力データが格納されるディレクトリ",
    )
    parser.add_argument(
        "--OUTPUT_DATA_DIR",
        type=str,
        default="/opt/ml/processing/output",
        help="出力データを格納するディレクトリ",
    )
    params, _ = parser.parse_known_args()
    main(params)
