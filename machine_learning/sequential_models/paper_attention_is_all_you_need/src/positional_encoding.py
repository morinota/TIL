import abc

import torch
from torch import Tensor

"""
- multi-head attentionはsequential(系列)データの要素間の関係を学習できるが、sequentialデータの順序までは考慮してくれない.
- そこでPositional Encodingを用いて、sequential データ内のposition情報を入力へ追加する.
"""


class PositionalEncodingInterface(abc.ABC):
    @abc.abstractmethod
    def calc(self, position_idx: int, d_model: int) -> Tensor:
        """_summary_

        Parameters
        ----------
        position_idx : int
            sequentialデータにおける位置
        d_model : int
            特徴量ベクトルの次元数
        Returns
        -------
        Tensor
            positional encoding (d_model, )のベクトル.
        """
        raise NotImplementedError


class PositionalEncoding(PositionalEncodingInterface):
    def calc(self, position_idx: int, d_model: int) -> Tensor:
        pe = torch.zeros(d_model)
        odd_indices = torch.arange(0, d_model, 2)
        even_indices = torch.arange(1, d_model, 2)
        pe[odd_indices] = torch.cos(position_idx / (10000 ** (odd_indices.float() / d_model)))
        pe[even_indices] = torch.sin(position_idx / (10000 ** (even_indices.float() / d_model)))
        return pe
