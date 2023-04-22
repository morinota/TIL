import abc
import math
import random
from typing import Dict, List, Union

import numpy as np
from mh_objective_function import ObjectiveFunctionInterface
from this import d


class CommunitySearcherAbstruct(abc.ABC):
    def __init__(
        self,
        objective_function: ObjectiveFunctionInterface,
        num_communities: int = 10,
    ) -> None:
        self.objective_func = objective_function
        self.num_communities = num_communities

    def search(
        self,
        graph: np.ndarray,
        num_epochs: int,
    ) -> np.ndarray:
        Z = self._initialize_Z(graph)
        len_V = len(graph)  # TODO:独立集合 R の長さ(頂点数)を取得.
        for t in range(num_epochs):
            for u in random.sample([u for u in range(len_V)], len_V):
                Z_updated = self._proposal_Z_updated(u, graph, Z)
                p = self._get_replace_probability(u, graph, Z, Z_updated)
                if not self._is_replace(p):
                    continue
                Z = Z_updated
        return Z

    @abc.abstractmethod
    def _initialize_Z(
        self,
        graph: np.ndarray,
        num_communities: int,
    ) -> np.ndarray:
        raise NotImplementedError

    @abc.abstractmethod
    def _proposal_Z_updated(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
        num_communities: int,
    ) -> np.ndarray:
        """updateするのはベクトルZ(u)だが、returnはZのu行目をreplaceした行列で返す"""
        raise NotImplementedError

    def _get_replace_probability(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
        Z_updated: np.ndarray,
    ) -> float:
        """Zの置き換え確率を出力"""
        f_uZ_updated = self.objective_func.calc_f_uZ(u, graph, Z_updated)
        f_uZ = self.objective_func.calc_f_uZ(u, graph, Z)
        return min(1, math.e ** (f_uZ_updated - f_uZ))

    def _is_replace(self, p: float) -> bool:
        """ベルヌーイ分布のパラメータpを受け取りbinaryの乱数を生成.boolで返す."""
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1 inclusive.")
        binary_val = 1 if random.random() < p else 0
        return bool(binary_val)


class RandomMetropolisHastings(CommunitySearcherAbstruct):
    def _initialize_Z(self, graph: np.ndarray) -> np.ndarray:
        len_V = len(graph)
        return np.random.randint(
            low=0,
            high=2,
            size=(len_V, self.num_communities),
        )

    def _proposal_Z_updated(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
    ) -> np.ndarray:
        Z_updated_u = np.random.randint(low=0, high=2, size=(self.num_communities))
        Z_updated = Z.copy()
        Z_updated[u] = Z_updated_u
        return Z_updated


class NeighborhoodAwareMetropolisHastings(CommunitySearcherAbstruct):
    def _initialize_Z(self, graph: np.ndarray) -> np.ndarray:
        for i in range(self.num_communities):
            # 各コミュニティ毎にグラフ内のnodeをランダムに一つ選ぶ.
            len_V = len(graph)
            sampled_node_idx = np.random.randint(low=0, high=len_V)
            # 選ばれたnodeのneigbhborhoodをそのコミュニティに所属させる.
            neighbor_indices: List[int] = graph[sampled_node_idx].tolist()
            pass

    def _proposal_Z_updated(
        self,
        u: int,
        graph: np.ndarray,
        Z: np.ndarray,
        l: int,  # 任意の1 nodeが所属可能なコミュニティの数(l << num_communities)
    ) -> np.ndarray:
        N_u = self._get_neighbor_indices(graph, u)
        S = self._get_neighbors_communities(Z, N_u)

        s_idx_f_map = {}
        for s_idx in S:
            # Z(u)' = sとした場合のf(u, Z)を計算し、mapping
            Z_updated_by_s = self._get_Z_updated_by_s(u, s_idx, Z)
            s_idx_f_map[s_idx] = self.objective_func.calc_f_uZ(u, graph, Z_updated_by_s)

        Z_updated = self._sampling_by_softmax(s_idx_f_map, Z, l)
        return Z_updated

    def _get_neighbor_indices(
        self,
        graph: np.ndarray,
        node_idx: int,
    ) -> List[int]:
        """node uのneigborsを取得"""
        pass

    def _get_neighbors_communities(
        self,
        Z: np.ndarray,
        neigbors: List[int],
    ) -> List[int]:
        """neigborsの一人以上が所属しているコミュニティ集合Sを取得"""
        pass

    def _get_Z_updated_by_s(self, u: int, s_idx: int, Z: np.ndarray) -> np.ndarray:
        pass

    def _sampling_by_softmax(
        self,
        s_idx_f_map: Dict[int, float],
        Z: np.ndarray,
        l: int,
    ) -> np.ndarray:
        """s_idx_f_mapに基づいて、Sからl個のコミュニティをサンプリングし、Z_updatedを作成"""
        pass
