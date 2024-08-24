import polars as pl
import patito as pt


# 出力データの構造の定義
class Item2ItemRecommendation(pt.Model):
    target_item_title: str
    rank: int
    recommended_item_title: str
    score: float


def offline_evaluation(
    recommendation_df: pl.DataFrame, news_metadata_df: pl.DataFrame
) -> dict[str, float]:
    import polars as pl

    # 推薦結果のオフライン評価
    evaluator = OfflineEvaluator()
    metrics = evaluator.evaluate(recommendation_df, news_metadata_df)

    return metrics


class OfflineEvaluator:
    def __init__(self) -> None:
        pass

    def evaluate(
        recommendation_df: pl.DataFrame, news_metadata_df: pl.DataFrame
    ) -> dict[str, float]:
        pass
