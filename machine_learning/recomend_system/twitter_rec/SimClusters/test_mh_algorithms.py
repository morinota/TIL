import math

import mh_algorithms as mh
import numpy as np

# def test_random_metropolis_hastings():
#     # テスト用のsimilarityグラフ
#     similarity_graph = np.array(
#         [
#             [0, 1, 1, 0],  # u = 0に対して
#             [1, 0, 1, 1],
#             [1, 1, 0, 1],
#             [0, 1, 1, 0],
#         ]
#     )
#     num_communities = 2
#     num_epochs = 10
#     alpha = 10

#     searcher = mh.RandomMetropolisHastings(alpha)

#     Z = searcher._initialize(similarity_graph, num_communities)
#     assert Z.shape == (len(similarity_graph), num_communities)

#     u = 0  # 0番目の頂点を選択
#     Z_updated = searcher._proposal(u, similarity_graph, Z, num_communities)
#     assert Z_updated.shape == (num_communities,)

#     p = searcher._get_replace_probability(u, Z, Z_updated)
#     assert 0 <= p <= 1

#     # search()のテスト
#     Z = searcher.search(similarity_graph, num_communities, num_epochs)
#     assert Z.shape == (len(similarity_graph), num_communities)


def test_objective_function_calculator() -> None:
    alpha = 10
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )
    u = 0
    Z = np.array(
        [
            [0, 1],  # u=0と同じコミュニティに所属してるのはv=2,3
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )

    neigbors_expected = [1, 2]  # u=0と接しているのはv=1, 2
    neigbors_actual = mh.ObjectiveFunction._get_neigbor_node_indices(u, similarity_graph)
    assert neigbors_actual == neigbors_expected

    v = 2
    count_shared_community_expected = 1
    count_shared_community_actual = mh.ObjectiveFunction._count_shared_community(
        assignments_vector_u=Z[u],
        assignments_vector_v=Z[v],
    )
    assert count_shared_community_actual == count_shared_community_expected

    f_uZ_expected = alpha * (0 + 1) + (0)
    f_uZ_actual = mh.ObjectiveFunction.calc_f_uZ(
        u,
        similarity_graph,
        Z,
    )
    assert math.isclose(f_uZ_actual, f_uZ_expected)
