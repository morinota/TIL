# Denoising Self-Attentive Sequential Recommendation

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/pdf/2212.04120.pdf
(勉強会発表者: morinota)

---

## どんなもの?

- Transformer-basedのsequentialな推薦モデルは、短期的 & 長期的なsequential itemの依存関係を捉えるのに非常に強力.(アイテムAを見た後は、アイテムBを見がち、みたいな??)
  - これは主に、sequence内のpairwiseアイテム-アイテムの相互作用を利用する為の、ユニークなself-attentionネットワークに起因している.
- しかし、real-worldのimplicit feedbackのアイテムsequenceはしばしばノイズが多い.
  - ex)クリックの大部分はユーザのpreferenceに合わない.
  - ex)多くのアイテムは購入後、否定的なレビューを受けたり、返品されることになる.
  - このように、現在のuser actionはsequence全体ではなく、itemのsubset(?)にのみ依存する.
- 既存のTransformerベースのモデルの多くは、full attention distribution(??)を使用しており、必然的に無関係なアイテムに一定のcredits(?)を割り当てることになる.
- 本論文では、self-attentive型の推薦システムのより良い学習のために、**Rec-denoiserモデル**を提案する.
  - Rec-denoiserでは、次のアイテム予測に関係のないノイズの多いアイテムを適応的に(adaptively)刈り取ることを目的とする.
    - そのために、各self-attention layerに学習可能なbinary maskを付加し、ノイズの多いattentionsを除去することで、sparseでclearなattention distributionが得られる.
    - これにより、item-itemの依存性がほぼ除去され、モデルの解釈可能性が向上する.
  - さらに、self-attentionネットワークは一般的にLipschitz連続(??)ではなく、小さなperturbations(摂動)に弱い.
  - さらにヤコビアン正則化をTransformerブロックに適用し、ノイズの多いsequenceに対するTransformerのrobustness(頑健性)を向上させる.
  - 我々のRec-denoiserは多くのTransformerに対応する汎用的なplugin(拡張機能みたいな?)である.
- 実世界のデータセットにおける定量的な結果は、Rec-denoiserが最先端のベースラインを凌駕することを示している.

## 先行研究と比べて何がすごい？

- 初期のマルコフ連鎖モデル:
  - ユーザの次の決定がいくつかの先行行動から導かれると仮定.
  - 短期的なアイテムの遷移を捉えるために提案されたが、長期的な嗜好は無視されたままだった.

しかし、sequential recommenderのrobustnessについてはあまり研究されていない.

実世界の多くのアイテムsequence(主にimplicit feedback)は自然にノイズが多く、真陽性(true-positive)と偽陽性(false-positive. ex. **好きじゃないけどクリックしてしまった. 購入してみたが嫌いだった...??**)の両方の相互作用を含んでいる.

## 技術や手法の肝は？

![](https://camo.qiitausercontent.com/e45f54ea48f0c70fc48dac65a3e2a883cf9d385c/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f38303632363439632d623162302d336163382d383335622d6236383765363465366239372e706e67)

図1は、左から右へのsequential recommendationの一例である.

- ex)ある父親が息子に（携帯電話、ヘッドフォン、ノートパソコン）、娘に（カバン、ズボン）を購入する場合、（携帯電話、カバン、ヘッドフォン、ズボン、ノートパソコン）という順序になる.
- sequential recommendationの設定では、**ユーザの以前の行動、例えば（電話、カバン、ヘッドホン、ズボン）から、次のアイテム、例えばノートパソコンを推論すること**を意図している.
- しかし、アイテム間の相関が不明確であり、**直感的にズボンとノートパソコンは補完関係にも相容れない**ため、この予測は信頼できない.

信頼できるモデルは、sequence内のこれらの無関係なアイテムを無視し、相関のあるアイテムのみを捉えることができるはず...!
既存のself-attentive sequential model達（例えば、SASRec [26]やBERT4Rec [41]）は、sequence内のノイズの多いアイテムに対処するには不十分.
その理由は、それらの完全な注意分布が密であり、無関係な項目を含むすべての項目に一定のクレジットを割り当ててしまうからである。


## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
