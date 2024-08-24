import polars as pl
import patito as pt
import itertools
from operator import itemgetter
import numpy as np


class Content2ContentRanking(pt.Model):
    from_id: str
    rank: int
    to_id: str
    score: float


def create_content2content_rankings(
    from_vector_df: pl.DataFrame,
    to_vector_df: pl.DataFrame,
    k: int,
) -> pl.DataFrame:
    """fromコンテンツとtoコンテンツのベクトル間の距離が近い順に、
    各fromコンテンツに対するtop-kのtoコンテンツのランキングを作成する
    """
    import itertools
    from operator import itemgetter
    import numpy as np
    import polars as pl
    import patito as pt

    ranking_list = [
        _calculate(
            row["content_id"],
            row["vector"],
            to_vector_df,
            k=k,
        )
        for row in from_vector_df.iter_rows(named=True)
    ]

    # flatにしてDataFrameに変換
    ranking_df = pl.DataFrame(itertools.chain(*ranking_list))

    Content2ContentRanking.validate(ranking_df)
    return ranking_df


def _calculate(
    from_id: str,
    from_vector: np.ndarray,
    to_vector_df: pl.DataFrame,
    k: int,
) -> list[Content2ContentRanking]:
    """単一のfromコンテンツに対して、toコンテンツのランキングを作成する"""
    to_vectors = np.vstack(to_vector_df["vector"].to_numpy())

    normed_from_vector = from_vector / np.linalg.norm(from_vector)
    normed_to_vectors = _norm_vectors(to_vectors)

    scores = np.dot(normed_from_vector, normed_to_vectors.T)
    content_scores = zip(to_vector_df["content_id"], scores)

    top_k_scores = sorted(content_scores, key=itemgetter(1), reverse=True)[:k]

    rankings = [
        Content2ContentRanking(from_id=from_id, rank=idx + 1, to_id=to_id, score=score)
        for idx, (to_id, score) in enumerate(top_k_scores)
    ]
    return rankings


def _norm_vectors(vectors: np.ndarray) -> np.ndarray:
    """複数のベクトルをノルム正規化して返す"""
    norms = np.linalg.norm(vectors, axis=1)
    return vectors / norms[:, np.newaxis]
