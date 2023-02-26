import abc
import math
from typing import Dict, List

from scipy.stats import spearmanr


class AbstructRankSimEvaluator(abc.ABC):
    def eval(self, item_id_ranking1: List[str], item_id_ranking2: List[str]) -> float:

        # アイテムIDを辞書で表現する
        item_id_idx_map = {item_id: idx for idx, item_id in enumerate(sorted(set(item_id_ranking1 + item_id_ranking2)))}

        # Listのidx=item_id, 要素=順位のListを作る.
        item_idx_rank_list1 = self._create_item_idx_rank_list(item_id_ranking1, item_id_idx_map)
        item_idx_rank_list2 = self._create_item_idx_rank_list(item_id_ranking2, item_id_idx_map)

        return self._calc_metric(item_idx_rank_list1, item_idx_rank_list2)

    def _create_item_idx_rank_list(self, item_id_ranking: List[str], item_id_idx_map: Dict[str, int]) -> List[int]:
        """返り値は"idx=item_id, value=順位"であるList"""
        item_idx_rank_list = [0] * len(item_id_idx_map)
        for rank_idx, item_id in enumerate(item_id_ranking):
            item_idx = item_id_idx_map[item_id]
            item_idx_rank_list[item_idx] = rank_idx + 1
        return item_idx_rank_list

    @abc.abstractmethod
    def _calc_metric(self, item_idx_rank_list1: List[int], item_idx_rank_list2: List[int]) -> float:
        raise NotImplementedError


class SpearmanRankCorrelation(AbstructRankSimEvaluator):
    def _calc_metric(self, item_idx_rank_list1: List[int], item_idx_rank_list2: List[int]) -> float:
        correlation_coefficiet, p_value = spearmanr(item_idx_rank_list1, item_idx_rank_list2)
        return correlation_coefficiet


class WeightedSpearmanRankCorrelation(AbstructRankSimEvaluator):
    def _calc_metric(self, item_idx_rank_list1: List[int], item_idx_rank_list2: List[int]) -> float:
        len_rank = len(item_idx_rank_list1)
        for x_i, y_i in zip(item_idx_rank_list1, item_idx_rank_list2):
            pass

    def _calc_numerator(
        self,
        fitem_idx_rank_list1: List[int],
        item_idx_rank_list2: List[int],
        len_rank: int,
    ) -> float:
        pass


def test_calculate_spearman_rank_correlation() -> None:
    # テストケース1: 同じリストを比較する場合、スピアマンの順位相関係数は1になる
    speaman_rank_corr = SpearmanRankCorrelation()

    list1 = ["a", "b", "c", "d", "e", "f"]
    list2 = ["a", "b", "c", "d", "e", "f"]
    assert speaman_rank_corr.eval(list1, list2) == 1.0

    # テストケース2: 1つのリストを逆順にした場合、スピアマンの順位相関係数は-1になる
    list1 = ["a", "b", "c", "d", "e", "f"]
    list2 = ["f", "e", "d", "c", "b", "a"]
    assert speaman_rank_corr.eval(list1, list2) == -1.0

    # テストケース6: 空のリストを比較する場合、スピアマンの順位相関係数はNaNになる
    list1 = []
    list2 = []
    assert math.isnan(speaman_rank_corr.eval(list1, list2))

    # _calc_metricのテスト. (https://qiita.com/dacciinfo/items/88debe69f9f4e927aafc のサンプルデータの値と比較)
    math_rank = [6, 4, 5, 10, 2, 8, 3, 9, 1, 7]
    english_rank = [10, 1, 4, 9, 3, 8, 6, 5, 2, 7]
    assert speaman_rank_corr._calc_metric(math_rank, english_rank) == 0.6727272727272726
