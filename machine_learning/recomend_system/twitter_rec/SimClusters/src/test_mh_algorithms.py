import math

import mh_algorithms as mh
import numpy as np
from mh_objective_function import ObjectiveFunction


def test_random_metropolis_hastings():
    # テスト用のsimilarityグラフ
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],  # u = 0に対して
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )
    num_communities = 2
    num_epochs = 10
    alpha = 10
    objective_func = ObjectiveFunction()
    searcher = mh.RandomMetropolisHastings(objective_func, alpha)

    Z = searcher._initialize(similarity_graph, num_communities)
    assert Z.shape == (len(similarity_graph), num_communities)

    u = 0  # 0番目の頂点を選択
    Z_updated = searcher._proposal(u, similarity_graph, Z, num_communities)
    assert Z_updated.shape == (num_communities,)

    p = searcher._get_replace_probability(u, Z, Z_updated)
    assert 0 <= p <= 1

    # search()のテスト
    Z = searcher.search(similarity_graph, num_communities, num_epochs)
    assert Z.shape == (len(similarity_graph), num_communities)
