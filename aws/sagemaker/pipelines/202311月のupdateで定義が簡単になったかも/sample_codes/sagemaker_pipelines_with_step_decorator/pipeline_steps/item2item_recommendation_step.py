import itertools
import numpy as np
import polars as pl
import patito as pt


# 入力データの構造の定義
class ItemVector(pt.Model):
    title: str
    vector: list[float]


# 出力データの構造の定義
class Item2ItemRecommendation(pt.Model):
    target_item_title: str
    rank: int
    recommended_item_title: str
    score: float


def item2item_recommend(
    target_vector_df: pl.DataFrame,
    candidate_vector_df: pl.DataFrame,
) -> pl.DataFrame:
    import itertools
    import numpy as np
    import polars as pl
    import patito as pt

    # 入力データのvalidation
    ItemVector.validate(target_vector_df)
    ItemVector.validate(candidate_vector_df)

    # 推薦結果を作る
    recommender = Item2ItemRecommender()
    item2item_recommendation_df_list = [
        recommender.recommend(
            target_title=target_title,
            target_vector=target_vector,
            candidate_vector_df=candidate_vector_df,
        )
        for target_title, target_vector in zip(
            target_vector_df["title"].to_list(), target_vector_df["vector"].to_list()
        )
    ]
    item2item_recommendation_df = pl.DataFrame(
        itertools.chain(*item2item_recommendation_df_list)
    )

    # 出力データのvalidation
    Item2ItemRecommendation.validate(item2item_recommendation_df)
    return item2item_recommendation_df


class Item2ItemRecommender:
    def __init__(self) -> None:
        pass

    def recommend(
        self,
        target_title: str,
        target_vector: list[float],
        candidate_vector_df: pl.DataFrame,
        k: int = 10,
    ) -> list[Item2ItemRecommendation]:
        """単一のtargetアイテムとcandidateアイテム集合を受け取り、item2itemの推薦結果を返す"""
        # 行列積で一気にスコアを計算するためにnumpy配列に変換
        candidate_vectors: np.ndarray = np.vstack(
            candidate_vector_df["vector"].to_numpy()
        )

        scores = np.dot(np.array(target_vector), candidate_vectors.T)
        candidate_scores = zip(candidate_vector_df["title"], scores)

        top_k_scores = sorted(
            candidate_scores, key=lambda title_score: title_score[1], reverse=True
        )[:k]

        return [
            Item2ItemRecommendation(
                target_item_title=target_title,
                rank=idx + 1,
                recommended_item_title=recommended_title,
                score=score,
            )
            for idx, (recommended_title, score) in enumerate(top_k_scores)
        ]


if __name__ == "__main__":
    target_vector_df = ItemVector.examples(
        {"vector": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "title": ["a", "b"]}
    )
    candidate_vector_df = ItemVector.examples(
        {
            "vector": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
            "title": ["a", "b", "c"],
        }
    )

    # 100件だけ処理
    item2item_recommendation_df = item2item_recommend(
        target_vector_df.head(100), candidate_vector_df
    )

    print(item2item_recommendation_df.head(5))
