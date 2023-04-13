import abc
import math
import random
from typing import List, Union

import numpy as np


class ObjectiveFunctionInterface(abc.ABC):
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
        # graphからuと接しているnodesのindicesを取得する.
        pass

    @staticmethod
    def _get_neigbor_node_indices(u: int, graph: np.ndarray) -> List[int]:
        similarity_vec_u: List[float] = graph[u].tolist()
        u_neigbor_node_indices = [u_idx for u_idx, sim_val in enumerate(similarity_vec_u) if sim_val > 0]
        return u_neigbor_node_indices

    @staticmethod
    def _count_shared_community(
        assignments_vector_u: np.ndarray,
        assignments_vector_v: np.ndarray,
    ) -> int:
        community_set_u = set(assignments_vector_u.tolist())
        community_set_v = set(assignments_vector_v.tolist())
        return len(community_set_u.intersection(community_set_v))
