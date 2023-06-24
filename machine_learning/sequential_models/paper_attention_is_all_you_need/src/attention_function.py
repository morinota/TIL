import abc
from typing import Tuple

import torch
from torch import Tensor


class AttentionInterface(abc.ABC):
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
    def calc(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
    ) -> Tuple[Tensor, Tensor]:
        """
        「入力されたqueryに最も近しいkeyを選び、対応するvalueを得る」イメージ.
        Parameters
        ----------
        query : Tensor
            query集合の行列. (n * d_k 行列)
        key : Tensor
            key行列. (n * d_k 行列)
        value : Tensor
            value行列. (n * d_v 行列)
        ここで、nはtoken長. d_kはクエリベクトルの長さ. d_vはhogehoge.

        Returns
        -------
        Tuple[Tensor, Tensor]
            - attention_output: atteniton functionの出力. (n * d_v 行列)
            - attention_weights: queryとkeyの類似度. (n * n 行列)
        """
        raise NotImplementedError


class ScaledDotProductAttention(AttentionInterface):
    def calc(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
    ) -> Tuple[Tensor, Tensor]:
        attention_weights = self._calc_attention_weights(query, key)
        attention_output = torch.matmul(attention_weights, value)
        return attention_output, attention_weights

    def _calc_attention_weights(self, query: Tensor, key: Tensor) -> Tensor:
        d_k = query.size(-1)
        print(d_k)
        Q_K_T = torch.matmul(
            query,
            key.transpose(-2, -1),
        )
        sqrt_d_k = torch.sqrt(torch.tensor(d_k, dtype=torch.float32))
        return torch.softmax(Q_K_T / sqrt_d_k, dim=-1)
