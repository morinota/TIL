---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: Sequential な推薦モデルやSentence BERT等の論文を理解する為に、遅ればせながら(?) Attention Is All You Needを読んだ.
subtitle: n週連続 推薦システム系論文読んだシリーズ 19週目
date: 2023/06/28
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## ざっくり論文概要

- hogehoge

## この論文を読むモチベーション

- Sequential なモデルを使った推薦手法の論文を理解するのに必要になりそう.
- SentenceBERT等を用いたContent base系の推薦手法を開発・運用する上で、まずはAttention functionやTransformerが何をやってるかくらいは理解しておきたい.

# まず Transformerの全体像はこうだ!

## Transformerの全体像

# Transformerの各パーツを確認していく.

## Attention function について1

- $Attention(Q, K, V)$ で表される関数.
  - **Query行列**, **Key行列**, **Value行列** を引数に取る.(行数がsequenceデータの長さ. 列数が各tokenの特徴量ベクトルの長さのイメージ.)
  - 出力値は、value行列 を 重みづけ合計したもの.(形状はvalue行列と同じ.)
  - 各valueに割り当てられた重みは、対応する key と query の compatibility function(親和性関数?)によって計算される.
  - 各queryに最も親和性があるkeysを選び、対応するvaluesを取得するイメージ??:thinking:
- $Attention(Q, K, V)$ は、基本的には $Atteniton(Q, X, X)$ らしい.(i.e. Keys=Values)
  - $Q = X$ の場合、 **self-attention** と呼ぶ.
  - $Q \neq X$ の場合、**source-to-target atteniton** と呼ぶ.

## Attention function について2

- ちなみに、機械翻訳タスクにおいては、以下の**3通りのAttentionの使われ方**が存在するらしい(Transformer内においてもこの3通りの使われ方が組み合わされている.):
  - Q = X = 翻訳元の文章 とした self attention(in Encoder)
  - Q = X = 翻訳対象の文章 とした self attention(in Decoder)
  - Q = 翻訳対象の文章, X = 翻訳元の文章 とした source-to-target-atteniton (in Decoder)

## Attention functionのお気持ち実装

Attention functionには、何種類かあるようなので、今回はInterfaceとしてお気持ち実装します.

```python
class AttentionInterface(nn.Module):
    @abc.abstractmethod
    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
    ) -> Tensor:
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
            Atteniton functionの出力 (seq_len * d_embed 行列)
        -------
        """
        raise NotImplementedError
```

## Scaled-dot-product Attention

以下で定義されるattention functionの一種.(Transformer内で採用されている)

$$
Attention(Q, K, V) = softmax(\frac{Q K^{T}}{\sqrt{d_k}}) V
\tag{1}
$$

- ここで, $d_k$ をQuery行列 $Q$ とKey行列 $K$ の列数, $d_v$ を Value行列の列数とする. (どちらも i.e. 各tokenの特徴量ベクトルの次元数のイメージ).
- 各queryと全てのkeyのdot productを計算し、それぞれを $\sqrt{d_k}$ で割り、softmax関数を適用して各valueの重みを求めている.
- (このattention function内には、**学習可能なパラメータは存在しないっぽい?**. 内積と重み付け和のみで構成されてる:thinking:)
- 論文執筆時点で最も一般的なattention functionは、additive(加法) attention と dot-product (multiplicative=乗法) attention とのこと.
- dot-product attention の場合、$d_k$ の大きさに依って出力値が影響を受ける為、その性質を打ち消す為に $\sqrt{d_k}$ でscaling(正規化みたいな)している.

## Scaled-dot-product Attention のお気持ち実装

`AttentionInterface`を継承した`ScaledDotProductAttention`をお気持ち実装してみた.

```python
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
    ) -> Tensor:
        attention_weights = self._calc_attention_weights(query, key)

        if mask is None:
            return torch.matmul(attention_weights, value)

        if mask.dim() != attention_weights.dim():
            raise ValueError(
                f"mask.dim != attention_weight.dim, mask.dim={mask.dim()}, attention_weight.dim={attention_weights.dim()}"
            )

        attention_weights_masked = attention_weights.data.masked_fill_(mask, -torch.finfo(torch.float).max)
        return torch.matmul(attention_weights_masked, value)

    def _calc_attention_weights(self, query: Tensor, key: Tensor) -> Tensor:
        Q_K_T = torch.matmul(
            query,
            key.transpose(-2, -1),
        )
        sqrt_d_k = torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))
        return torch.softmax(Q_K_T / sqrt_d_k, dim=-1)
```

## Multi-head Attention について1

- $d_{model}$ 次元の Query, Key, Value で単一のattention関数を実行するのではなく、**学習した重み(線形モデル)を用いて** Query, Key, Value をそれぞれ $d_k$ 、$d_k$ 、$d_v$ に**線形投影(=linearly project)**する事を$h$ 回行うのが有効だと判明しているらしい. これを実現するのが**Multi-head attention**.
- 投影された Query, Key, Value に対して、**$h$ 個のattention functionを並行して適用**し、$h$ 個の $n \times d_v$ 次元の出力値を得る.
- これをconcatenate($n \times h d_v$ 次元になる?)して再び線形投影すると、最終的な $n \times d_{model}$ 次元の出力値が得られる.

$$
MultiHead(Q,K,V) = Concat(head_{1}, \cdots, head_{h}) W^{O}
\\
\text{where } head_{i} = Attention(QW^{Q}_{i}, KW^{K}_{i}, VW^{V}_{i})
\tag{2}
$$

ここで、各線形投影に用いるパラメータ行列は以下:

$$
W^{Q}_{i} \in \mathbb{R}^{d_{model} \times d_k},
W^{K}_{i} \in \mathbb{R}^{d_{model} \times d_k},
W^{V}_{i} \in \mathbb{R}^{d_{model} \times d_v},
W^{O} \in \mathbb{R}^{h * d_{v}\times d_{model}}
$$

## Multi-head Attention について2

- 論文のTransformerでは、 $h = 8$ のparallel attention layers(i.e. head)を採用してる.
- $d_{model} = 512$ として、$d_k = d_v = \frac{d_{model}}{h} = 64$ と設定している.
- 各headsの扱う次元数が小さくなる為、総計算コストは元々のQ, K, Vにsingle head のattentionを適用する場合と同じになる. (線形投影して行列の次元数が$n \times d_{model}$ -> $n × d_k$ と低次元になるから...!!)
- 本論文で提案されているTransformerでは、前述した3通りのattentionの使い方で multi-head attention を使用している.

## Multi-head Attention のお気持ち実装

`ScaledDotProductAttention`に依存する`MultiHeadAttention`をお気持ち実装してみた.

```python
import abc
from typing import Optional

import torch
from torch import Tensor, nn

from src.attention_function import ScaledDotProductAttention

class MultiHeadAttentionInterface(nn.Module):
    @abc.abstractmethod
    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
        mask_3d: Optional[Tensor] = None,
    ) -> Tensor:
        raise NotImplementedError


class MultiHeadAttention(MultiHeadAttentionInterface):
    def __init__(self, d_model: int, num_heads: int) -> None:
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # query&keyもvalueも同じ埋め込み次元数の想定?
        self.d_v = d_model // num_heads

        self.attention_func = ScaledDotProductAttention(self.d_k)

        # 以下のW^{Q}_{i}, W^{K}_{i}, W^{V}_{i}, W^{O}は学習すべきパラメータ.
        self.query_linear_projectors = [nn.Linear(d_model, self.d_k) for _ in range(self.num_heads)]
        self.key_linear_projectors = [nn.Linear(d_model, self.d_k) for _ in range(self.num_heads)]
        self.value_linear_projectors = [nn.Linear(d_model, self.d_v) for _ in range(self.num_heads)]
        self.output_linear_projector = nn.Linear(self.num_heads * self.d_v, d_model)

    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
        mask_3d: Optional[Tensor] = None,
    ) -> Tensor:
        batch_size, seq_len = query.size(0), query.size(1)

        if mask_3d is not None:
            mask_3d = mask_3d.repeat(self.num_heads, 1, 1)

        heads = []
        for i in range(self.num_heads):
            # linear projection for getting the inputs of each heads.
            query_projected = self.query_linear_projectors[i].forward(query)
            key_projected = self.key_linear_projectors[i].forward(key)
            value_projected = self.value_linear_projectors[i].forward(value)

            attention_output, _ = self.attention_func.forward(
                query_projected,
                key_projected,
                value_projected,
                mask_3d,
            )
            heads.append(attention_output)

        # concat heads
        concatted_output = torch.cat(heads, dim=0)

        # linear projection for output
        return self.output_linear_projector.forward(concatted_output)
```

## Position-wise Feed-Forward Networks について

## Position-wise Feed-Forward Networks のお気持ち実装

## Positional Encoder について

## Positional Encoder のお気持ち実装

# Transformer を組み立てていく

## Transformer Encoder

## Transformer Decoder

## Tranformer のお気持ち実装

```

```
