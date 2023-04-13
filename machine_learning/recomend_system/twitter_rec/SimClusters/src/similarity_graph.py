import abc
import itertools

import numpy as np
from colorama import reinit


class SimilarityGraphInterface(abc.ABC):
    @abc.abstractclassmethod
    def build(cls, bi_partite_graph: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class SimilarityGraph(SimilarityGraphInterface):
    @classmethod
    def build(cls, bi_partite_graph: np.ndarray) -> np.ndarray:
        len_R = bi_partite_graph.shape[1]
        similarity_graph = np.zeros(shape=(len_R, len_R))
        for u, v in itertools.combinations_with_replacement(list(range(len_R)), r=2):
            if u == v:
                similarity_graph[u, u] = 1.0
                continue
            x_u = bi_partite_graph[:, u]
            x_v = bi_partite_graph[:, v]
            cosime_sim = cls._calc_cosine_sim(x_u, x_v)
            similarity_graph[u, v] = cosime_sim
            similarity_graph[v, u] = cosime_sim
        return similarity_graph

    @classmethod
    def _calc_cosine_sim(cls, x_u: np.ndarray, x_v: np.ndarray) -> float:
        dot_product = np.dot(x_u, x_v)
        norm_u = np.linalg.norm(x_u)
        norm_v = np.linalg.norm(x_v)
        return dot_product / (norm_u * norm_v)
