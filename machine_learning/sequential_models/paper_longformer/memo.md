## refs

- [【論文解説】Longformerを理解する](https://data-analytics.fun/2020/12/14/understanding-longformer/)

# 概要:

- Longformerとは?
  - The Long-Document Transformerの意味。
  - Transformterが長い文章(i.e. sequence)に対してメモリ消費量が急激に増加する事($O(n^2)$)の解決を目的としたarchitecture.
  - 同様の目的を持つモデルとして、ReformerやSparse Transformerがある。
- なんでTransformerは長い文章だと困るの??
  - Transformerの中で使うscaled-dot-product attentionが、**full $n^2$ pattern**を採用してるから。(Rec-denoiserの論文だとfull attention distributionと表現されてたはず)
- 4種のself-attention pattern:
  - 1. full $n^2$ attention
    - 全てのtokenから全てのtokenに対するattention weightを保持する
    - メモリ使用量は $O(n^2)$
  - 2. Sliding window attention
    - token自身のすぐ近くのtoken達のみのattention weightを保持する
    - window sizeを $w$ とし、対象tokenから左右それぞれ $\frac{1}{2} w$ 個のtokenにattentionを向ける。
    - メモリ使用量は $O(n \times w)$ 。token数 $n$ に対して線形。
    - layerによって $w$ を変える事も可能。
  - 3. Dilated sliding window attention
    - gap sizeを $d$ として、 attention を向けるtokenを $d$ 個ずつ飛ばす。
  - 4. Global+sliding window attention
    - **特定のpositionのtokenのみ**、他の全てのtokenに対してattentionを向け、また全てのtokenはその特定のpositionのtokenにattentionを向ける様にする。
    - ex. sequenceの先頭に置くspecial token `[CLS]` にはglobal attention patternを採用する。
    - ex2. Question-Answeringタスクでは、Question文に対してglobal attention pattern を採用する。
    - 特定のtoken positionはあくまでも数箇所なので、空間計算量は $O(n)$ のまま。
