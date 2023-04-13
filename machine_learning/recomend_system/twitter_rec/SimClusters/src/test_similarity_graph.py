import numpy as np
from similarity_graph import SimilarityGraph


def test_similarity_graph_build() -> None:
    # 行:左の独立集合L, 列:右の独立集合Rを表す行列
    bi_partite_graph = np.array(
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ]
    )  # 各要素:binary.行ユーザが列ユーザをフォローしているか否か
    similarity_graph_expected = np.array(
        [
            [1.0, 0.66666667, 0.408248],
            [0.66666667, 1.0, 0.408248],
            [0.408248, 0.408248, 1.0],
        ]
    )  # (Rの数) * (Rの数)の正方行列. 無向グラフなので、対角線に対して線対称な値.

    similarity_graph_actual = SimilarityGraph.build(bi_partite_graph)
    assert similarity_graph_actual.shape == similarity_graph_expected.shape
    np.testing.assert_array_almost_equal(
        similarity_graph_actual,
        similarity_graph_expected,
        decimal=4,
    )


def test_similarity_calc_cosine_sim() -> None:
    x_u = np.array([0, 1, 0, 1, 1])
    x_v = np.array([1, 0, 0, 1, 1])
    cosine_sim_expected = np.dot(x_u, x_v) / (np.linalg.norm(x_u) * np.linalg.norm(x_v))

    cosine_sim_actual = SimilarityGraph._calc_cosine_sim(x_u, x_v)

    assert np.isclose(cosine_sim_actual, cosine_sim_expected)
