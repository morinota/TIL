import abc
import random
from typing import Any


class CommunitySearcherAbstruct(abc.ABC):
    def __init__(self) -> None:
        pass

    def search(
        self,
        graph: Any,
        num_communities: int,
        num_epochs: int,
    ) -> Any:
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
        graph: Any,
        num_communities: int,
    ) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def _proposal(
        self,
        u: int,
        graph: Any,
        Z: Any,
        num_communities: int,
    ) -> Any:
        raise NotImplementedError

    def _get_replace_probability(self, u: int, Z: Any, Z_updated: Any) -> float:
        """Zの置き換え確率を出力"""
        pass

    def _is_replace(self, p: float) -> bool:
        """ベルヌーイ分布のパラメータpを受け取りbinaryの乱数を生成.boolで返す."""
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1 inclusive.")
        binary_val = 1 if random.random() < p else 0
        return bool(binary_val)


class RandomMetropolisHastings(CommunitySearcherAbstruct):
    def _initialize(self, graph: Any, num_communities: int) -> Any:
        pass

    def _proposal(self, u: int, graph: Any, Z: Any, num_communities: int) -> Any:
        pass


class NeighborhoodAwareMetropolisHastings(CommunitySearcherAbstruct):
    def _initialize(self, graph: Any, num_communities: int) -> Any:
        pass

    def _proposal(self, u: int, graph: Any, Z: Any, num_communities: int) -> Any:
        pass
