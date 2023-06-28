import abc

import torch
from torch import Tensor, nn

from machine_learning.sequential_models.paper_attention_is_all_you_need.src.multi_head_attention import (
    MultiHeadAttentionInterface,
)
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.position_wise_feed_forward_newwork import (
    PositionWiseFFNInterface,
)
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.positional_encoding import (
    PositionalEncodingInterface,
)


class TranformerDecoderInterface(nn.Module):
    """
    - Transformer Decoderは以下の層で構成される:
        - Embedding Layer:
        - Positional Encoding Layer:
        - Transformer Decoder Block × N:
            - 各blockは(Masked multi-head attention + Multi-head attention + Feed Forward Network)で構成.
    """

    @abc.abstractmethod
    def calc(
        self,
        tgt: Tensor,
        src: Tensor,
        mask_src_tgt: Tensor,
        mask_self: Tensor,
    ) -> Tensor:
        raise NotImplementedError


class TransformerDecoderBlockInterface(nn.Module):
    """
    (Masked multi-head attention + Multi-head attention + Feed Forward Network)で構成される.
    """

    @abc.abstractmethod
    def forward(
        self,
        tgt: Tensor,  # Decoder input
        src: Tensor,  # Encoder output
        mask_src_to_tgt: Tensor,
        mask_self: Tensor,
    ) -> Tensor:
        raise NotImplementedError


class TransformerDecoderBlock(TransformerDecoderBlockInterface):
    def __init__(
        self,
        d_model: int,
        self_attention: MultiHeadAttentionInterface,
        src_to_tgt_attention: MultiHeadAttentionInterface,
        feed_forward_network: PositionWiseFFNInterface,
        dropout_rate: float,
        layer_norm_epsilon: float,
    ) -> None:
        super().__init__()

        # self-attention インスタンス
        self.self_attention = self_attention
        self.dropout_self_attention = nn.Dropout(dropout_rate)
        self.layer_norm_self_attention = nn.LayerNorm(d_model, layer_norm_epsilon)

        # source-to-target attention インスタンス
        self.src_to_tgt_attention = src_to_tgt_attention
        self.dropout_src_to_tgt_attention = nn.Dropout(dropout_rate)
        self.layer_norm_src_to_tgt_attention = nn.LayerNorm(d_model, layer_norm_epsilon)

        # feed forward network インスタンス
        self.ffn = feed_forward_network
        self.dropout_ffn = nn.Dropout(dropout_rate)
        self.layer_norm_ffn = nn.LayerNorm(d_model, layer_norm_epsilon)

    def forward(
        self,
        tgt: Tensor,
        src: Tensor,
        mask_src_to_tgt: Tensor,
        mask_self: Tensor,
    ) -> Tensor:
        # input to self-attention function
        tgt_self_attentioned = self.dropout_self_attention(
            self.self_attention.forward(tgt, tgt, tgt, mask_self),
        )
        tgt_self_attentioned_norm = self.layer_norm_self_attention(
            tgt + tgt_self_attentioned,
        )

        # input to src-to-tgt-attention function
        x_src_to_tgt_attentioned = self.dropout_src_to_tgt_attention(
            self.src_to_tgt_attention.forward(tgt_self_attentioned_norm, src, src, mask_src_to_tgt)
        )
        x_src_to_tgt_attentioned_norm = self.layer_norm_src_to_tgt_attention(
            tgt_self_attentioned + x_src_to_tgt_attentioned
        )

        # input to feed forward network
        x_ffn = self.dropout_ffn(self.ffn.calc(x_src_to_tgt_attentioned_norm))
        return self.layer_norm_ffn(x_src_to_tgt_attentioned_norm + x_ffn)


class TransformerDecoder(TranformerDecoderInterface):
    def __init__(
        self,
        d_model: int,
        N: int,
        positional_encoding: PositionalEncodingInterface,
        self_attention: MultiHeadAttentionInterface,
        src_to_tgt_attention: MultiHeadAttentionInterface,
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

        self.decoder_blocks = nn.ModuleList(
            [
                TransformerDecoderBlock(
                    d_model,
                    self_attention,
                    src_to_tgt_attention,
                    feed_forward_network,
                    dropout_rate,
                    layer_norm_epsilon,
                )
                for _ in range(N)
            ]
        )

    def calc(
        self,
        tgt: Tensor,
        src: Tensor,
        mask_src_tgt: Tensor,
        mask_self: Tensor,
    ) -> Tensor:
        tgt = self.embedding(tgt)
        tgt = self.positional_encoding.forward(tgt)
        for decoder_block in self.decoder_blocks:
            tgt = decoder_block.forward(
                tgt,
                src,
                mask_src_tgt,
                mask_self,
            )
        return tgt
