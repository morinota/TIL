import abc

import torch
from torch import Tensor, nn

from machine_learning.sequential_models.paper_attention_is_all_you_need.src.decoder import TransformerDecoder
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.encoder import TransformerEncoder
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.multi_head_attention import (
    MultiHeadAttention,
    MultiHeadAttentionInterface,
)
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.position_wise_feed_forward_newwork import (
    PositionWiseFFN,
    PositionWiseFFNInterface,
)
from machine_learning.sequential_models.paper_attention_is_all_you_need.src.positional_encoding import (
    PositionalEncoding,
    PositionalEncodingInterface,
)


class TransformerInterface(nn.Module):
    @abc.abstractmethod
    def forward(self, src: Tensor, tgt: Tensor) -> Tensor:
        """
        Parameters
        ----------
        src : Tensor
            翻訳元のsequential データ(各要素は単語のid)
        tgt : Tensor
            翻訳先のsequential データ(各要素は単語のid)
        """
        raise NotImplementedError


class Transformer(TransformerInterface):
    def __init__(
        self,
        src_vocab_size: int,
        tgt_vocab_size: int,
        max_len: int,
        d_model: int = 512,
        heads_num: int = 8,
        d_ff: int = 2048,
        N: int = 6,
        dropout_rate: float = 0.1,
        layer_norm_epsilon: float = 1e-5,
        pad_idx: int = 0,
        device: torch.device = torch.device("cpu"),
    ) -> None:
        super().__init__()

        self.src_vocab_size = src_vocab_size
        self.tgt_vocab_size = tgt_vocab_size
        self.d_model = d_model
        self.max_len = max_len
        self.heads_num = heads_num
        self.d_ff = d_ff
        self.N = N
        self.dropout_rate = dropout_rate
        self.layer_norm_epsilon = layer_norm_epsilon
        self.pad_idx = pad_idx
        self.device = device

        self.encoder = TransformerEncoder(
            self.d_model,
            self.N,
            PositionalEncoding(self.d_model, self.max_len, self.device),
            MultiHeadAttention(self.d_model, self.heads_num),
            PositionWiseFFN(self.d_model, self.d_ff),
            self.src_vocab_size,
            self.max_len,
            self.pad_idx,
            self.dropout_rate,
            self.layer_norm_epsilon,
            self.device,
        )

        self.decoder = TransformerDecoder(
            self.d_model,
            self.N,
            PositionalEncoding(self.d_model, self.max_len, self.device),
            MultiHeadAttention(self.d_model, self.heads_num),
            MultiHeadAttention(self.d_model, self.heads_num),
            PositionWiseFFN(self.d_model, self.d_ff),
            self.src_vocab_size,
            self.max_len,
            self.pad_idx,
            self.dropout_rate,
            self.layer_norm_epsilon,
            self.device,
        )

        self.linear = nn.Linear(d_model, tgt_vocab_size)

    def forward(self, src: Tensor, tgt: Tensor) -> Tensor:
        src_encoded = self.encoder.forward(src)

        decode_output = self.decoder.forward(tgt, src_encoded)

        return self.linear(decode_output)
