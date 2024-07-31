import polars as pl
import patito as pt
import torch
from transformers import MLukeTokenizer, LukeModel


# 入力データのschemaの定義
class NewsMetadata(pt.Model):
    url: str
    date: str
    title: str = pt.Field(unique=True)
    content: str
    category: str


# 出力データのschemaの定義
class NewsVector(pt.Model):
    title: str = pt.Field(unique=True)
    vector: list[float]


def news_encode(news_metadata_df: pl.DataFrame) -> pl.DataFrame:
    import polars as pl
    import patito as pt

    # 入力データのvalidation
    try:
        NewsMetadata.validate(news_metadata_df)
    except pt.exceptions.DataFrameValidationError as exc:
        print(exc)

    # 前処理 (category, title, content を単一の文字列に連結)
    news_metadata_df = news_metadata_df.with_columns(
        (pl.col("category") + " " + pl.col("title") + " " + pl.col("content")).alias(
            "text"
        )
    )

    # ニュース記事のメタデータを埋め込んだニュースベクトルを作成
    model = NewsEncoderModel()
    news_vectors = model.encode(news_metadata_df["text"].to_list())

    # title, vector のみを抽出
    news_vector_df = pl.DataFrame(
        {
            "title": news_metadata_df["title"],
            "vector": pl.Series(news_vectors),
        }
    )

    # 出力データのvalidation
    NewsVector.validate(news_vector_df)
    return news_vector_df


# 学習済み言語モデルのクラス
class NewsEncoderModel:
    DEFAULT_MODEL_NAME = "sonoisa/sentence-luke-japanese-base-lite"

    def __init__(self) -> None:
        # トークナイザーの読み込み
        self.tokenizer = MLukeTokenizer.from_pretrained(self.DEFAULT_MODEL_NAME)
        # 学習済みモデルの読み込み
        self.model = LukeModel.from_pretrained(self.DEFAULT_MODEL_NAME)
        self.model.eval()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    @torch.no_grad()
    def encode(self, texts: list[str], batch_size: int = 50) -> list[list[float]]:
        # ミニバッチで推論させる
        all_embeddings = []
        for batch_idx in range(0, len(texts), batch_size):
            batch_texts = texts[batch_idx : batch_idx + batch_size]

            # テキストのトークン化
            inputs = self.tokenizer(
                batch_texts, padding=True, truncation=True, return_tensors="pt"
            )
            # デバイスに転送
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # ニュース記事のメタデータを埋め込んだニュースベクトルを作成
            outputs = self.model(**inputs)
            # プーリングされた出力を取得
            pooled_output = outputs.pooler_output

            all_embeddings.extend(pooled_output.cpu().numpy().tolist())

        return all_embeddings


if __name__ == "__main__":
    news_metadata_df = pl.read_parquet("~/Documents/livedoor_news.parquet")

    # 100件だけ処理
    news_vector_df = news_encode(news_metadata_df.head(100))

    print(news_vector_df.head(5))

    # 対象ニュースと最も近いベクトル10件を取得
    target_news_title = "急成長を遂げるFacebookに忍び寄る影"
    target_news_vector = news_vector_df.filter(pl.col("title") == target_news_title)[
        "vector"
    ][0]
    print(target_news_vector)
    print(type(target_news_vector))
    # ベクトルの次元数
    print(len(target_news_vector))
