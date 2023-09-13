from dataclasses import dataclass
from typing import Any
import numpy as np


@dataclass
class ItemFeatureTable:
    array: np.ndarray
    d: int
    I_length: int


@dataclass
class RecformerParams:
    params: np.ndarray


@dataclass
class Item:
    item_sequence: list[str]  # T_{i}


class TwoStageFinetune:
    def __init__(self, epoch_num: int) -> None:
        self.epoch_num = epoch_num
        pass

    def train(
        self,
        D_train,
        D_valid,
        items: set[Item],
        M: RecformerParams,
    ) -> tuple[ItemFeatureTable, RecformerParams]:
        p = 0.0  # metrics are initialized with 0

        # stage1
        for n in range(self.epoch_num):
            I = self._encode(M, items)
            M = self._train(M, I, D_train)
            p_prime = self._evaluate(M, I, D_valid)

            if p_prime > p:
                M_prime, I_prime = M, I
                p = p_prime

        # stage2
        M = M_prime
        for n in range(self.epoch_num):
            M = self._train(M, I_prime, D_train)
            p_prime = self._evaluate(M, I_prime, D_valid)
            if p_prime > p:
                M_prime = M
                p = p_prime

        return M_prime, I_prime

    def _encode(self, M: RecformerParams, items: set[Item]) -> ItemFeatureTable:
        # Recformerで 各itemのアイテム表現 h_{i} を取得する(推論する)
        pass

    def _train(self, M: RecformerParams, I: ItemFeatureTable, D_train: Any) -> RecformerParams:
        # item-item contractice(next-item prediction)タスクを学習させる
        pass

    def _evaluate(self, M: RecformerParams, I: ItemFeatureTable, D_valid: Any) -> float:
        # 精度指標(損失関数の逆数?)を検証用データで算出?
        pass
