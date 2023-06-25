import abc

import torch
from torch import Tensor

"""
- multi-head attentionはsequential(系列)データの要素間の関係を学習できるが、sequentialデータの順序までは考慮してくれない.
- そこでPositional Encodingを用いて、sequential データ内のposition情報を入力へ追加する.
"""


class PositionalEncodingInterface(abc.ABC):
    @abc.abstractmethod
    def forward(self, x: Tensor) -> Tensor:
        raise NotImplementedError


class PositionalEncoding(PositionalEncodingInterface):
    def __init__(
        self,
        d_model: int,
        max_len: int,
        device: torch.device = torch.device("cpu"),
    ) -> None:
        """
        Parameters
        ----------
        d_model : int
            モデルの埋め込みベクトルの次元数
        max_len : int
            sequential データの最大長.
        device : torch.device, optional
            by default torch.device("cpu")
        """
        super().__init__()
        self.d_model = d_model
        self.max_len = max_len
        self.positional_encoding_weights = self._initialize_weight().to(device)

    def forward(self, x: Tensor) -> Tensor:
        seq_len = x.size(1)
        positional_encoding_weights = self.positional_encoding_weights[:seq_len, :]
        return x + positional_encoding_weights.unsqueeze(0)  # 次元をあわせて追加.

    def _initialize_weight(self) -> torch.Tensor:
        positional_encoding_weights = [self._calc_positional_encoding_vector(pos) for pos in range(1, self.d_model + 1)]
        return torch.tensor(positional_encoding_weights).float()

    def _calc_positional_encoding_vector(self, position_idx: int) -> Tensor:
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
        pe = torch.zeros(self.d_model)
        odd_indices = torch.arange(0, self.d_model, 2)
        even_indices = torch.arange(1, self.d_model, 2)
        pe[odd_indices] = torch.cos(position_idx / (10000 ** (odd_indices.float() / self.d_model)))
        pe[even_indices] = torch.sin(position_idx / (10000 ** (even_indices.float() / self.d_model)))
        return pe
