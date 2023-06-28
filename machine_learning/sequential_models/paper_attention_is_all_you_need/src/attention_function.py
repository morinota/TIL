import abc
from typing import Optional, Tuple

import torch
from torch import Tensor, nn


class AttentionInterface(nn.Module):
    """attention function内には学習可能なparametersは存在しない.
    内積と荷重平均のみで構成されている.
    - Attention(Q, K, V) は、基本的には Atteniton(Q, X, X)である.(Keys=Values)
        - Q = X の場合、 self-attention と呼ぶ.
        - Q != X の場合、source-to-target atteniton と呼ぶ.
    - 機械翻訳タスクにおいては、以下の3通りのAttentionの使われ方が存在する(Transformerにおいてもこの三種が組み合わされている.):
        - Q = X = 翻訳元の文章 としたself attention(in Encoder)
        - Q = X = 翻訳対象の文章 としたself attention(in Decoder)
        - Q = 翻訳対象の文章, X = 翻訳元の文章 とした source-to-target-atteniton (in Decoder)
    """

    @abc.abstractmethod
    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
    ) -> Tuple[Tensor, Tensor]:
        """
        Parameters
        ----------
        query : Tensor
            Query行列. (seq_len * d_embed 行列)
        key : Tensor
            Key行列. (seq_len * d_embed 行列)
        value : Tensor
            Value行列. (seq_len * d_embed 行列)

        Returns
        Tensor
            attention_output: atteniton functionの出力 (seq_len * d_embed 行列)
        -------
        """
        raise NotImplementedError


class ScaledDotProductAttention(AttentionInterface):
    def __init__(self, d_k: int) -> None:
        super().__init__()
        self.d_k = d_k

    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
        mask: Optional[Tensor] = None,
    ) -> Tuple[Tensor, Tensor]:
        attention_weights = self._calc_attention_weights(query, key)

        if mask is None:
            return torch.matmul(attention_weights, value), attention_weights

        if mask.dim() != attention_weights.dim():
            raise ValueError(
                f"mask.dim != attention_weight.dim, mask.dim={mask.dim()}, attention_weight.dim={attention_weights.dim()}"
            )

        attention_weights_masked = attention_weights.data.masked_fill_(mask, -torch.finfo(torch.float).max)
        return torch.matmul(attention_weights_masked, value), attention_weights_masked

    def _calc_attention_weights(self, query: Tensor, key: Tensor) -> Tensor:
        Q_K_T = torch.matmul(
            query,
            key.transpose(-2, -1),
        )
        sqrt_d_k = torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))
        return torch.softmax(Q_K_T / sqrt_d_k, dim=-1)
