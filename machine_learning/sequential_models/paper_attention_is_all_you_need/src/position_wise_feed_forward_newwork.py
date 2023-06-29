import abc

import torch
from torch import nn


class PositionWiseFFNInterface(nn.Module):
    """
    - Position-wise Feed-Forward Networks(FFN)は、2つの全結合層を重ねただけのシンプルな層.(中間層は一つだけ.)
    - 活性化関数はRelu.
    - 定式化: FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
        - max(0, 1つ目の層の出力)の意味が気になる...。普通付いてないっけ?
    """

    @abc.abstractmethod
    def forward(self, x: torch.Tensor):
        raise NotImplementedError


class PositionWiseFFN(PositionWiseFFNInterface):
    def __init__(self, d_model: int, d_ff: int) -> None:
        """入力層と出力層の次元数が同じなので、linear transformation?"""
        super().__init__()
        self.linear_1 = nn.Linear(d_model, d_ff)
        self.linear_2 = nn.Linear(d_ff, d_model)
        self.activate_func = nn.functional.relu

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        middle_output = self.activate_func(self.linear_1.forward(x))
        return self.linear_2.forward(middle_output)
