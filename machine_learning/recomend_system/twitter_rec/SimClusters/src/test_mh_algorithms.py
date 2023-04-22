import math

import mh_algorithms as mh
import numpy as np
from mh_objective_function import ObjectiveFunction


def test_community_searcher_abstruct_get_relace_probability() -> None:
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )  # u=0と接しているのはv=1, 2. u=0と接してないのはv=3
    u = 0
    Z = np.array(
        [
            [0, 1],  # u=0と一つ以上同じコミュニティに所属してるのはv=2,3
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    Z_updated_u = np.array([1, 0])
    Z_updated = np.array(
        [
            [1, 0],  # u=0と一つ以上同じコミュニティに所属してるのはv=1,2
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    alpha = 10
    objective_func = ObjectiveFunction(alpha)

    f_uZ_updated = objective_func.calc_f_uZ(u, similarity_graph, Z_updated)
    f_uZ = objective_func.calc_f_uZ(u, similarity_graph, Z)
    replace_probability_expected = min(1, math.e ** (f_uZ_updated - f_uZ))

    # abcはインスタンス化できない為、子クラスをインスタンス化している.
    searcher = mh.RandomMetropolisHastings(objective_func)
    replace_probability_actual = searcher._get_replace_probability(
        u,
        similarity_graph,
        Z,
        Z_updated,
    )

    assert replace_probability_actual == replace_probability_expected


def test_community_searcher_abstruct_is_replace() -> None:
    p = 0.5
    alpha = 10
    objective_func = ObjectiveFunction(alpha)

    searcher = mh.RandomMetropolisHastings(objective_func)
    is_replace_actual = searcher._is_replace(p)
    assert type(is_replace_actual) is bool


def test_random_metropolis_hastings() -> None:
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )  # u=0と接しているのはv=1, 2. u=0と接してないのはv=3
    u = 0
    Z = np.array(
        [
            [0, 1],  # u=0と一つ以上同じコミュニティに所属してるのはv=2,3
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    Z_updated_u = np.array([1, 0])
    Z_updated = np.array(
        [
            [1, 0],  # u=0と一つ以上同じコミュニティに所属してるのはv=1,2
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    alpha = 10
    objective_func = ObjectiveFunction(alpha)
    num_communities = 2
    num_epochs = 10

    searcher = mh.RandomMetropolisHastings(objective_func, num_communities)

    Z = searcher._initialize_Z(similarity_graph)
    assert Z.shape == (similarity_graph.shape[0], num_communities)

    u = 0  # 0番目の頂点を選択
    Z_updated = searcher._proposal_Z_updated(u, similarity_graph, Z)
    assert Z_updated.shape == Z.shape

    # search()のテスト
    Z = searcher.search(similarity_graph, num_epochs)
    assert Z.shape == (len(similarity_graph), num_communities)


def test_neighborhood_aware_MH_inizitalize_Z() -> None:
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )  # u=0と接しているのはv=1, 2. u=0と接してないのはv=3
    alpha = 10
    objective_func = ObjectiveFunction(alpha)
    num_communities = 2

    searcher = mh.NeighborhoodAwareMetropolisHastings(objective_func, num_communities)
    Z_init = searcher._initialize_Z(similarity_graph)

    assert Z_init.shape == (len(similarity_graph), num_communities)


def test_neighborhood_aware_MH_proposal_Z_updated() -> None:
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )  # u=0と接しているのはv=1, 2. u=0と接してないのはv=3
    u = 0
    Z = np.array(
        [
            [0, 1],  # u=0と一つ以上同じコミュニティに所属してるのはv=2,3
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    alpha = 10
    objective_func = ObjectiveFunction(alpha)
    num_communities = 2
    upper_bound_assign_per_node = 1

    searcher = mh.NeighborhoodAwareMetropolisHastings(objective_func, num_communities)
    Z_updated = searcher._proposal_Z_updated(u, similarity_graph, Z)
    assert Z_updated.shape == Z.shape


def test_neighborhood_aware_MH_get_neigbor_indices() -> None:
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )  # u=0と接しているのはv=1, 2. u=0と接してないのはv=3

    u = 0
    neibor_indices_expected = [1, 2]

    searcher = mh.NeighborhoodAwareMetropolisHastings(ObjectiveFunction(alpha=10))


def test_neighborhood_aware_MH_get_neighbors_communities() -> None:
    pass


def test_neighborhood_aware_MH_get_Z_updated_by_s() -> None:
    pass
