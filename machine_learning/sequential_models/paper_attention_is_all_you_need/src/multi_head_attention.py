import abc

import torch
from torch import Tensor, nn

from machine_learning.sequential_models.paper_attention_is_all_you_need.src.attention_function import (
    ScaledDotProductAttention,
)


class MultiHeadAttentionInterface(nn.Module):
    @abc.abstractmethod
    def calc(self, query: Tensor, key: Tensor, value: Tensor) -> Tensor:
        raise NotImplementedError


class MultiHeadAttention(MultiHeadAttentionInterface):
    def __init__(self, d_model: int, num_heads: int) -> None:
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # query&keyもvalueも同じ埋め込み次元数の想定?
        self.d_v = d_model // num_heads

        self.attention_func = ScaledDotProductAttention()

        # 以下のW^{Q}_{i}, W^{K}_{i}, W^{V}_{i}, W^{O}は学習すべきパラメータ.
        self.query_linear_projectors = [nn.Linear(d_model, self.d_k) for _ in range(self.num_heads)]
        self.key_linear_projectors = [nn.Linear(d_model, self.d_k) for _ in range(self.num_heads)]
        self.value_linear_projectors = [nn.Linear(d_model, self.d_v) for _ in range(self.num_heads)]
        self.output_linear_projector = nn.Linear(self.num_heads * self.d_v, d_model)

    def calc(self, query: Tensor, key: Tensor, value: Tensor) -> Tensor:
        batch_size = query.size(0)

        heads = []
        for i in range(self.num_heads):
            # linear projection for getting the inputs of each heads.
            query_projected = self.query_linear_projectors[i].forward(query)
            key_projected = self.key_linear_projectors[i].forward(key)
            value_projected = self.value_linear_projectors[i].forward(value)

            attention_output, _ = self.attention_func.calc(
                query_projected,
                key_projected,
                value_projected,
            )
            heads.append(attention_output)

        concatted_output = self._concat_heads(heads)
        return self.output_linear_projector.forward(concatted_output)

    def _concat_heads(self, heads: list[Tensor]) -> Tensor:
        pass
