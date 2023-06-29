import abc

import torch
from torch import nn

from machine_learning.sequential_models.paper_attention_is_all_you_need.src.multi_head_attention import (
    MultiHeadAttentionInterface,
)
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.position_wise_feed_forward_newwork import (
    PositionWiseFFNInterface,
)
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.positional_encoding import (
    PositionalEncodingInterface,
)


class TransformerEncoderInterface(nn.Module):
    """
    - Transformer における Encoder は以下の層で構成される.
        - Embedding層
        - positional Encoding層
        - (multi-head attention層 + feed forward network層) = TransformerEncoderBlock層をn層重ねた層.
    """

    @abc.abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        - まずEmbedding
        - 次にPositional Encoding
        - TransformerEncoderBlock層 × n
        """
        raise NotImplementedError


class TransformderEncoderBlockInterface(nn.Module):
    """
    multi-head attention層 + feed forward network層で構成される.
    """

    @abc.abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """sequential特徴量ベクトル(n * d_{model} 行列)を受け取り、
        multi-head attention -> FFNに通して、
        同じ形状の(n * d_{model} 行列)を返す.
        """
        raise NotImplementedError


class TransformderEncoderBlock(TransformderEncoderBlockInterface):
    def __init__(
        self,
        d_model: int,
        self_attention: MultiHeadAttentionInterface,
        feed_forward_network: PositionWiseFFNInterface,
        dropout_rate: float,
        layer_norm_epsilon: float,
    ) -> None:
        super().__init__()

        self.multi_head_attention = self_attention
        self.dropout_self_attention = nn.Dropout(dropout_rate)
        self.layer_norm_self_attention = nn.LayerNorm(d_model, layer_norm_epsilon)

        self.ffn = feed_forward_network
        self.dropout_ffn = nn.Dropout(dropout_rate)
        self.layer_norm_ffn = nn.LayerNorm(d_model, layer_norm_epsilon)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.layer_norm_self_attention(self._self_attention_block)
        return self.layer_norm_ffn(self._feed_forward_block(x))

    def _self_attention_block(self, x: torch.Tensor) -> torch.Tensor:
        x = self.multi_head_attention.forward(x, x, x)
        return self.dropout_self_attention.forward(x)

    def _feed_forward_block(self, x: torch.Tensor) -> torch.Tensor:
        x = self.ffn.forward(x)
        return self.dropout_ffn.forward(x)


class TransformerEncoder(TransformerEncoderInterface):
    def __init__(
        self,
        d_model: int,
        N: int,
        positional_encoding: PositionalEncodingInterface,
        self_attention: MultiHeadAttentionInterface,
        feed_forward_network: PositionWiseFFNInterface,
        vocab_size: int,
        max_len: int,
        padding_idx: int,
        dropout_rate: float,
        layer_norm_epsilon: float,
        device: torch.device = torch.device("cpu"),
    ) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx)

        self.positional_encoding = positional_encoding

        self.encoder_blocks = nn.ModuleList(
            [
                TransformderEncoderBlock(
                    d_model, self_attention, feed_forward_network, dropout_rate, layer_norm_epsilon
                )
                for _ in range(N)
            ]
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        x = self.positional_encoding.forward(x)
        for encoder_block in self.encoder_blocks:
            x = encoder_block.forward(x)
        return x
