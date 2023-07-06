---
format:
  revealjs:
    # incremental: false
    theme: [default, quarto_custom_style.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: hogehogeな論文を読んだ
subtitle: n週連続推薦システム系論文読んだシリーズ 20週目
date: 2023/07/05
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 論文の基本情報

- title: Denoising Self-Attentive Sequential Recommendation
- published date: September 2022,
- authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
- url(paper): [https://arxiv.org/pdf/2212.04120.pdf](https://arxiv.org/pdf/2212.04120.pdf)

## ざっくり論文概要

# Introduction

## sequential 推薦の発展

- しかし、**sequential推薦器のrobustness**についてはあまり研究されていない.
- 実世界の多くのitem sequences(特にimplicit feedback!)は自然にノイズが多く、**真陽性(true-positive)と偽陽性(false-positive) の両方のinteractionを含む** [6, 45, 46].
  - 偽陽性の例: 好きじゃないけどクリックしてしまった. 購入してみたが嫌いだった.
  - 実際、クリックの大部分はユーザの嗜好に合わず、多くの購入された製品は否定的なレビューで終わったり、返品されたりする.
  - (next-token-predictionと比較しても、こういったノイズが多かったりするのかな:thinking:)
- そのため、**ノイズに強いアルゴリズムを開発することは、sequential推薦において大きな意義がある**.

## self-atteniton networkがノイズの多いsequenceに弱い問題

- 残念ながら、vanillaなself-attention networkは、**Lipschitz連続ではなく(?)**、**入力sequenceの質に弱いという問題**がある[28]
- 図1は、左から右へのsequential recommendationの一例.
- ex.) ある父親が息子に(携帯電話、ヘッドフォン、ノートパソコン)、娘に(カバン、ズボン)を購入する場合、(携帯電話、カバン、ヘッドフォン、ズボン、ノートPC)という順序になったとする.
- sequential recommendation の設定では、**ユーザの以前の行動(ex. 電話、カバン、ヘッドホン、ズボン)から、次のアイテム(ex. ノートPC)を推論すること**を意図している.
- しかし、アイテム間のcorrelationsが不明確であり、**直感的にパンツとノートPCの関連を納得できない**ため、この予測はuntrustworthyである.
- trustworthyなモデルは、sequence内の無関係なアイテムを無視し、相関のあるアイテムのみを捉えることができるはず.

## ノイズの多いsequenceにどう対応すべきか?

- 既存のself-attentive sequential model(ex. SASRec [26], BERT4Rec [41])は、full attention distributionが密である事から、全てのitemに一定以上のcredit(=attention weight?)を割り当ててしまう為、sequence内のノイズに対処するには不十分.
- 一つの簡単な戦略は、**attention layersの接続をsparseにした**Transformerアーキテクチャを設計すること[10, 58].(LMタスクで活発に研究されてるらしい)
  - しかし、これらのモデルは事前に定義されたattention schemas(??)に大きく依存しており、柔軟性や適応性に欠けている.
  - また、エンドツーエンドの学習アプローチとは異なり、言語モデルタスクのsparseパターンがsequential推薦にうまく一般化できるかどうかは不明.

## 本論文の目的 & 提案手法の概要

- 本論文の目的は、**ノイズの多いimplicit feedbackからのnext-item-predictionタスク**において、self-attention型sequential推薦モデルをより良く学習させるための**ノイズ除去戦略(Rec-Denoiser)**を提案する事.
- 提案手法のアイデアは、**全てのattentionは必要ではなく、冗長なattentionを刈り取ることでさらに性能が向上する**、という最近の知見に由来[10, 12, 40, 55, 58].
- Rec-Denoiserは、タスクと無関係なattentionをself-attention layersで削除する様な、学習可能なmaskを導入する.
  - 利点1: sequenceからより情報量の多いアイテムのsubsetを抜き出し、明示的にnext-token-predictionを実行できる.
  - 利点2: Transformerのアーキテクチャを変更せず、**attention分布のみを変更する**為、実装が容易 & あらゆるTransformerに適用可能で、その解釈可能性を向上できる.
- 実世界のベンチマークデータセットを使った実験で、手法の有効性を検証.

## 提案手法 Rec-Denoiser の２つの大きな課題 とその対応

Rec-Denoiserでは、2つの大きな課題がある.

- 課題1: binary mask(i.e. 0は削除され、1は保持される)は、その離散性に依ってback-propropagation実行不可能.
  - ->本論文では、probabilistic reparameterization(確率的再パラメータ化?)[25]により、離散変数を連続的な近似値で緩和する.(ここが結構頑張りどころっぽい:thinking:)
  - この工夫によって、提案手法の微分可能なmaskは、Transformerとend-to-endで一緒に学習可能.
- 課題2: scaled dot-product attention は Lipschitz連続(?)ではない為、input perturbations(入力摂動?ノイズ??)に対して脆弱[28].
  - ->本論文では、Transformerブロック全体にヤコビアン正則化[21, 24]を適用.

# Sequential Recommender と Sparse Transformer に関する既存研究

## Sequential Recommender

## Sparse Transformer

# Sequential Recommendation タスクの定式化

## Sequential Recommendation タスクにおける notation

- sequential推薦において、$U$ をユーザ集合、$I$ をアイテム集合、$S= \{S^1,S^2, \cdots, S^{|U|} \}$ をユーザ行動の集合とする.
- $S^u = (S^{u}_{1}, S^{u}_{2}, \cdots, S^{u}_{|S^u|})$ は、あるユーザ $u \in U$ の時系列に並んだ行動履歴(=item sequence)を表す.
  - $S^{u}_{t} \in I$ は time step $t$ (=sequence内の要素の識別子的な意味合い)にユーザ $u$ がinteractしたアイテム.
  - $|S^u|$ はsequenceの長さを表す.

## Sequential Recommendation タスクの定式化

- sequential推薦のタスクは、interaction history $S^u$ が与えられた状態で、time step $|S^{u}+1|$ における next item $S^u_{|S^{u}+1|}$ を予測する事.
- モデルの学習プロセス[26, 41]では、モデルの入力sequenceを $(S^{u}_{1}, S^{u}_{2}, \cdots, S^{u}_{|S^u - 1|})$ とし、入力sequence を1 time step分後ろにシフトしたもの $(S^{u}_{2}, S^{u}_{3}, \cdots, S^{u}_{|S^{u}|})$ を expected output(i.e. 正解ラベル!) とみなす事が多い.

# self-attentive recommender モデルを見直そう.

Transformerアーキテクチャ[43]は長いsequenceを学習することができるため、sequential推薦において**SASRec** [26], BERT4Rec [41], TiSASRec [30] など広く利用されている.
ここでは、SASRecの設計を簡単に紹介し、その限界について考察する.

## Embedding Layer

- Transformerベースのレコメンダーは、アイテムの **embedding table $T \in R^{|I| \times d}$** を保持する. ここで、$d$ は embeddingのサイズ. (embedding tableは、アイテムid -> embedding vector のmapみたいなイメージ:thinking:).
- 各sequence $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$ に対して、**fixed-length(固定長)のsequence $(s_1, s_2, \cdots s_n)$ に変換**する. ここで、$n$は、sequenceの最大長. (ex. sequenceを truncating したりpadding したりして、各sequence長を最新の$n$個のアイテムにする)
- **$(s_1, s_2, \cdots s_n)$ の embedding を $E \in R^{n \times d}$** と表す.(= 埋め込みベクトル行列 ...!)(各埋め込みベクトルは embedding table $T$ から取得する)

## Positional Encoding

- sequence内の順序情報を捉えるために、学習可能な(固定値もあるよな～:thinking:) positonal embedding $P \in R^{n \times d}$ を入力 $E$ にinject(注入)する(i.e. positional encoding vector):

$$
\hat{E} = E + P \tag{1}
$$

- ここで、$\hat{E} \in R^{n \times d}$ は order-awareな(=sequence内の順序を考慮した) 埋め込みベクトル行列.

## Transformer Block 1: Self-attention 層(scaled-dot-product attentionの話, etc.)

- Transformer Block は、self-attention 層 と point-wise feed-forward 層で構成される.
- self-attention層は、sequentialな依存関係を捉える為に効果的であり、Transformerブロックの重要なcomponent. (scaled-dot-product attentionのmulti-head attentionを採用)

$$
\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d}}) V
\tag{2}
$$

- ここで、$\text{Attention}(Q, K, V) \in R^{n \times d}$ は output item representations.
- $Q = \hat{E} W^Q$, $K =\hat{E} W^K$, and $V = \hat{E} W^V$ はそれぞれ Query, Key, Value. (QもKもVも、埋め込みベクトル行列Eを元にしてるので、attention関数のself-attention的な使い方...!). ${W^Q, W^K, W^V} \in R^{d \times d}$ は3つのprojection行列.
- $\sqrt{d}$ はscale-factor.(正規化的なイメージ!)

## Transformer Block 2: Self-attention 層(multi-head attentionの話, etc.)

- sequential推薦では、**left-to-right uni-directional attentions(左から右への一方向のattention)**(ex. SASRec [26]やTiSASRec [30])や、もしくは**bi-directional attention(双方向のattention)** (ex. BERT4Rec [41])を利用して、次のアイテムを予測することができる.
- さらに、$H$ 個のattention関数を並列に適用することで、表現力を高めることができる：$\mathbf{H} \leftarrow \text{MultiHead}(\hat{E})$ [43]. (元のtransformerでも採用してる、multi-head attentionね:thinking:)

## Transformer Block 3: Point-wise Feed-forward 層

- self-attention層はlinear projectionで構築されているので、**Point-wise Feed-forward層を導入することで、非線形性を付与する(モデルの表現力を高める為の非線形変換!)**ことができる(あ、そういうモチベーションなのか...!中間層１つのやつ! :thinking:):

$$
F_i = FFN(H_i) = \text{ReLU}(H_i W^{(1)} + b^{(1)})W^{(2)} + b^{(2)}
\tag{3}
$$

ここで、$W^{(\ast)} \in R^{d \times d}$, $b^{(\ast)} \in R^d$ は FFN層内の学習可能なparameters(重みとバイアス).

## Transformer Block 4: Point-wise Feed-forward 層の補足

- (補足: "point-wise" -> **要素毎に独立して操作を行う**、という意味. Transformerの場合はSequenceデータを入力に取るが、この層は、sequenceデータの各要素に対して個別に処理が行われる. つまり、sequenceデータの各要素に対して同じ操作が行われる.:thinking:)
  - (確かランク学習でも、point-wise, pair-wise, list-wiseってあったなー:thinking:)
- (補足: "feed-forward" -> データの入出力の流れが1方向=前方方向にのみ進む事を意味する.)
  - 逆に、"feed-forward"ではない層はRNNとか! CNNは"point-wise"ではないが"feed-forward"である気はする:thinking:

## Transformer Block 5

- 実際には、より多くのTransformerブロックを積み重ねることによって、階層的なアイテムの依存関係を学習することが通常有益.(元祖Transformerでも、$N$個のブロックを重ねるよね...:thinking:)
- また、**residual connection(残差接続), dropout, layer normalization(レイヤー正則化) などのトリックを採用することで、学習の安定化と高速化を図ることができる**.(そういう目的なんだ...!:thinking:)
- 本論文では、$L$ 個のTransformerブロックの出力(=L個のブロックが連結した最終的な出力の意味:thinking:)を単純に次のように表現する:

$$
F^{(L)} \leftarrow \text{Transformer}(\hat{E})
$$

## 学習の目的関数 1

- $L$ 個のTransformerブロックを積み重ねた後、最初の$t$個のitemが与えられると $F_t^{(L)}$ に基づいてnext-itemを予測できる.
- 内積を使ってアイテム $i$ の relevance(ユーザの行動履歴との) を次のように予測する.

$$
r_{i, t} = <F_{t}^{(L)}, T_i>,
$$

ここで $T_i \in R^d$ は、アイテム $i$ の埋め込みベクトル.

## 学習の目的関数 2

学習時にて、モデルは sequence $s = (s_{1}, s_{2}, \cdots, s_{n})$ を入力とし、出力の教師ラベルは同じ sequence をシフトしたもの $o = (o_{1}, o_{2}, \cdots, o_{n})$ である. なので、binary cross-entropy lossを適用できる:

(= $o_2$ は $s = (s_1, s_2)$ が与えられた時のnext-item predictionの正解ラベル、という認識. ~~$r_{i,t}$が最も高いアイテムを$o_2$として採用する、みたいなイメージ??~~ これは推論時ではなく学習時の話なので、$o_2 = s_3$ って事かな.:thinking:)

$$
L_{BCE} = - \sum_{S^{u} \in S} \sum_{t=1}^{n}{[\log{\sigma(r_{o_t, t})} + \log{1 - \sigma (r_{o_t', t})}]} + \alpha \cdot ||\theta||^2_F
\tag{4}
$$

- ここで、$\theta$はmodel parameters. $sigma(\cdot)$ はシグモイド関数.
- $\alpha$はオーバーフィットを防ぐためのreqularizer(正則化パラメータ).
- $o_{t}' \notin S^{u}$ は $o_t$ に対応するnegative sample(??:thinking:).

(詳細は、SASRec[26]およびBERT4Rec[41]に記載)

## SASRecの noisy attention 問題

- 本論文では、SASRecではsequence中のノイズに十分に対処できないと主張している.
  - 理由は、**full attention分布（例えば式(2)）は密度が高く、無関係なitemに一定のcredit(=attention weight)を割り当ててしまうから**.
  - full attention分布はitem-itemの依存関係を複雑にし、学習の難易度を上げ、モデルの性能を低下させる.
- 言語モデリングタスクでは、この問題に対処する為の試みが提案されている(ex. sparse attention schemas の活用, attentionのごく一部だけを残すdropout技術の活用, etc.)

本論文は、**微分可能なmaskを用いて無関係なattentionのノイズを除去する**、シンプルかつ効果的な data-driven method(=確かに、固定的でもランダムでもない:thinking:)を提案している.

# 提案手法: Rec-Denoiserについて

## differentiableな(微分可能な) mask

## 学習可能なsparse Attention

## 効率的な勾配計算

## Jacobian Regularization(ヤコビアン正則化)

## 損失関数の最適化1

## 損失関数の最適化2: end-to-endの学習

## モデルのcomplexity(計算量?)

## 補足:ARM推定量 や AR推定量 ってなんだ?

## 補足:one-forward pass や two-forward passってなんだ?

## 補足:Lipschitz constraint (リプシッツ制約) ってなんだ?

## 補足:Hutchinson推定量 ってなんだ?

# 実験

実験の目的は、**提案された微分可能なmaskが、self-attention層におけるnoisyなitemの悪影響を軽減できるか否か**を確認すること.具体的には、以下のresearch questionsを明らかにする為に実験を行った.

- RQ1: 提案手法 Rec-Denoiserは、最新の逐次推薦器と比較してどの程度有効か？
- RQ2：Rec-Denoiserは、sequence内のnoisyなアイテムの悪影響をどのように軽減できるか？
- RQ3：異なる構成要素(微分可能 mask や Jacobian 正則化など)は、Rec-Denoiserの全体的な性能にどのような影響を与えるか？

## 実験の設定

- 5つのbenchmarkデータを用いて推薦モデルを評価する: Movielens5, Amazon6(うち3種のカテゴリを選択), Steam7.
- データをtrain/valid/testセットに分割: 各ユーザのsequenceの最後のアイテムをtestingに、最後から2番目のアイテムをvalidationに、残りのアイテムをtrainingに使用.

## 補足: 比較対象のbaselines(2つのbaselines group)

- group1: 一般的なsequential手法群.
  - FPMC [39]: 行列分解と一次マルコフ連鎖モデルの混合.
  - GRU4Rec [20]: RNNベースの手法.
  - Caser [42]: CNNベースの手法.
  - SASRec [26]: left-to-right selfattentionのTransformerベースの手法.
  - BERT4Rec [41]: bidirectional self-attentionのTransformerベースの手法.
  - TiSASRec [30]: 要素間の時間間隔を考慮したself-attentionモデル.
  - SSE-PT [50]: self-attention層にパーソナライズを導入したモデル.
  - Rec-Denoiser: 提案手法. 任意のself-attentionモデルに適用可能.
- group2: sparse Transformersの手法群.
  - Sparse Transformer [10]: 固定されたatteniton maskパターンを使用.
  - $\alpha$-entmax sparse attention [12]: softmax 関数を $\alpha$-entmax で代用.

## 結果: Overall Performance(RQ1)
## 結果: Overall Performance(RQ1)
## 結果: Overall Performance(RQ1)
  