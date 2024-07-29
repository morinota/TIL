import numpy as np
import polars as pl
import patito as pt


def news_encode(news_metadata_df: pl.DataFrame) -> pl.DataFrame:
    import polars as pl

    # 入力データのvalidation
    NewsMetadata.validate(news_metadata_df)

    # 前処理 (category, title, content を単一の文字列に連結)
    news_metadata_df = news_metadata_df.with_columns(
        (pl.col("category") + " " + pl.col("title") + " " + pl.col("content")).alias(
            "text"
        )
    )
    print(news_metadata_df)

    # ニュース記事のメタデータを埋め込んだニュースベクトルを作成
    model = NewsEncoderModel()
    news_vector_series = model.encode(news_metadata_df["text"])

    # title, vector のみを抽出
    news_vector_df = pl.DataFrame(
        {
            "title": news_metadata_df["title"],
            "vector": news_vector_series,
        }
    )

    # 出力データのvalidation
    NewsVector.validate(news_vector_df)
    return news_vector_df


class NewsEncoderModel:
    def __init__(self) -> None:
        pass

    def encode(self, text: pl.Series) -> pl.Series:
        return pl.Series("vector", [np.random.rand(100) for _ in range(len(text))])


# inputの構造の定義
class NewsMetadata(pt.Model):
    url: str
    date: str
    title: str
    content: str
    category: str


# outputの構造の定義
class NewsVector(pt.Model):
    title: str
    vector: list[float]


if __name__ == "__main__":
    news_metadata_df = pl.read_parquet("~/Documents/livedoor_news.parquet")

    # 100件だけ処理
    news_vector_df = news_encode(news_metadata_df.head(100))
