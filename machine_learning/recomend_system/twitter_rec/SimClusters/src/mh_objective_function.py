import abc
from typing import Dict, List, Union

import numpy as np


class ObjectiveFunctionInterface(abc.ABC):
    def __init__(self, alpha: float = 10.0) -> None:
        self.alpha = alpha

    @abc.abstractmethod
    def calc_f_uZ(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
    ) -> float:
        raise NotImplementedError


class ObjectiveFunction(ObjectiveFunctionInterface):
    def calc_f_uZ(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
    ) -> float:
        node_indices: List[int] = range(graph.shape[0])
        neigbor_node_indices = self._get_neigbor_node_indices(u, graph)
        not_neigbor_node_indices = [idx for idx in node_indices if idx not in neigbor_node_indices]
        # 各nodesのshared_communityの数をカウントする.
        shared_community_count_map = {
            node_idx: self._count_shared_community(Z[u], Z[node_idx])
            for node_idx in neigbor_node_indices + not_neigbor_node_indices
        }
        # f(u,Z)を算出.
        return self._calc_f_u_Z(
            neigbor_node_indices,
            not_neigbor_node_indices,
            shared_community_count_map,
        )

    def _get_neigbor_node_indices(self, u: int, graph: np.ndarray) -> List[int]:
        similarity_vec_u: List[float] = graph[u].tolist()
        u_neigbor_node_indices = [u_idx for u_idx, sim_val in enumerate(similarity_vec_u) if sim_val > 0]
        return u_neigbor_node_indices

    def _count_shared_community(
        self,
        assignments_vector_u: np.ndarray,
        assignments_vector_v: np.ndarray,
    ) -> int:
        community_set_u = assignments_vector_u.tolist()
        community_set_v = assignments_vector_v.tolist()
        return sum(
            [
                1
                for is_community_u, is_community_v in zip(community_set_u, community_set_v)
                if is_community_u == is_community_v == 1
            ]
        )

    def _calc_f_u_Z(
        self,
        neigbor_node_indices: List[int],
        not_neigbor_node_indices: List[int],
        shared_community_count_map: Dict[int, int],
    ) -> float:
        f_u_Z = 0
        f_u_Z += self.alpha * sum([1 if shared_community_count_map[idx] > 0 else 0 for idx in neigbor_node_indices])
        f_u_Z += sum([1 if shared_community_count_map[idx] == 0 else 0 for idx in not_neigbor_node_indices])
        return f_u_Z
