import math

import numpy as np
from mh_objective_function import ObjectiveFunction


def test_objective_function_calculator_get_neighbor_node_indices() -> None:
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
    neigbors_actual = ObjectiveFunction._get_neigbor_node_indices(u, similarity_graph)
    assert neigbors_actual == neigbors_expected


def test_objective_function_calculator_count_shared_community() -> None:
    u = 0
    v = 2
    Z = np.array(
        [
            [0, 1],  # u=0と同じコミュニティに所属してるのはv=2,3
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    count_shared_community_expected = 1
    count_shared_community_actual = ObjectiveFunction._count_shared_community(
        assignments_vector_u=Z[u],
        assignments_vector_v=Z[v],
    )
    assert count_shared_community_actual == count_shared_community_expected


def test_objective_function_calculator_calc_f_uZ() -> None:
    similarity_graph = np.array(
        [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
        ]
    )
    alpha = 10
    u = 0
    Z = np.array(
        [
            [0, 1],  # u=0と同じコミュニティに所属してるのはv=2,3
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )
    f_uZ_expected = alpha * (0 + 1) + (0)
    f_uZ_actual = ObjectiveFunction.calc_f_uZ(
        u,
        similarity_graph,
        Z,
    )
    assert math.isclose(f_uZ_actual, f_uZ_expected)
