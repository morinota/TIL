import abc
import math
import random
from typing import List, Union

import numpy as np


class ObjectiveFunctionInterface(abc.ABC):
    def __init__(self, alpha: float = 0.5) -> None:
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
        node_indices: List[int] = []
        # graphからuと接しているnodesのindicesを取得する.
        neigbor_node_indices = self._get_neigbor_node_indices(u, graph)
        # graphからuと接していないnodesのindicesを取得する.
        not_neigbor_node_indices = [idx for idx in node_indices if idx not in neigbor_node_indices]
        # 各nodesのshared_communityの数をカウントする.
        shared_community_count_map = {node_idx: self._count_shared_community() for node_idx in node_indices}
        # f(u,Z)を算出.
        pass

    def _get_neigbor_node_indices(self, u: int, graph: np.ndarray) -> List[int]:
        similarity_vec_u: List[float] = graph[u].tolist()
        u_neigbor_node_indices = [u_idx for u_idx, sim_val in enumerate(similarity_vec_u) if sim_val > 0]
        return u_neigbor_node_indices

    def _count_shared_community(
        self,
        assignments_vector_u: np.ndarray,
        assignments_vector_v: np.ndarray,
    ) -> int:
        community_set_u = set(assignments_vector_u.tolist())
        community_set_v = set(assignments_vector_v.tolist())
        return len(community_set_u.intersection(community_set_v))
