import abc
import math
import random
from ast import List
from typing import Union

import numpy as np


class ObjectiveFunction:
    @staticmethod
    def calc_f_uZ(
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
    ) -> float:
        # graphからuと接しているnodesのindicesを取得する.
        pass

    @staticmethod
    def _get_neigbor_node_indices(u: int, graph: np.ndarray) -> List[int]:
        similarity_vec_u: List[Union[int, float]] = graph[u].tolist()
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


class CommunitySearcherAbstruct(abc.ABC):
    def __init__(self, alpha: float = 10) -> None:
        self.alpha = alpha

    def search(
        self,
        graph: np.ndarray,
        num_communities: int,
        num_epochs: int,
    ) -> np.ndarray:
        Z = self._initialize(graph, num_communities)
        len_V = len(graph)  # TODO:独立集合 R の長さ(頂点数)を取得.
        for t in range(num_epochs):
            for u in random.sample([u for u in range(len_V)], len_V):
                Z_uppdated = self._proposal(u, graph, Z, num_communities)
                p = self._get_replace_probability(u, Z, Z_uppdated)
                if not self._is_replace(p):
                    continue
                Z[u] = Z_uppdated
        return Z

    @abc.abstractmethod
    def _initialize(
        self,
        graph: np.ndarray,
        num_communities: int,
    ) -> np.ndarray:
        raise NotImplementedError

    @abc.abstractmethod
    def _proposal(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
        num_communities: int,
    ) -> np.ndarray:
        raise NotImplementedError

    def _get_replace_probability(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
        Z_updated: np.ndarray,
    ) -> float:
        """Zの置き換え確率を出力"""
        f_uZ_updated = ObjectiveFunction.calc_f_uZ(u, graph, Z_updated)
        f_uZ = ObjectiveFunction.calc_f_uZ(u, graph, Z)
        return min(1, math.e ** (f_uZ_updated - f_uZ))

    def _is_replace(self, p: float) -> bool:
        """ベルヌーイ分布のパラメータpを受け取りbinaryの乱数を生成.boolで返す."""
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1 inclusive.")
        binary_val = 1 if random.random() < p else 0
        return bool(binary_val)


class RandomMetropolisHastings(CommunitySearcherAbstruct):
    def _initialize(self, graph: np.ndarray, num_communities: int) -> np.ndarray:
        len_V = len(graph)
        return np.random.randint(
            low=0,
            high=2,
            size=(len_V, num_communities),
        )

    def _proposal(self, u: int, graph: np.ndarray, Z: np.ndarray, num_communities: int) -> np.ndarray:
        return np.random.randint(low=0, high=2, size=(num_communities))


class NeighborhoodAwareMetropolisHastings(CommunitySearcherAbstruct):
    def _initialize(self, graph: np.ndarray, num_communities: int) -> np.ndarray:
        pass

    def _proposal(self, u: int, graph: np.ndarray, Z: np.ndarray, num_communities: int) -> np.ndarray:
        pass
