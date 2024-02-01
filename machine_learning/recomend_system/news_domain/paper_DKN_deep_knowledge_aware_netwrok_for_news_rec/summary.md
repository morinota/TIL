# DKN: Deep Knowledge-Aware Network for News Recommendation

published date: 30 January 2018,
authors: Hongwei Wang, Fuzheng Zhang, Xing Xie, Minyi Guo
url(paper): https://dl.acm.org/doi/fullHtml/10.1145/3178876.3186175
(勉強会発表者: morinota)

---

n週連続推薦システム系論文読んだシリーズ x週目の記事になります。
ちなみにx-1週目は [タイトル](url) でした!

## どんなもの?

## 先行研究と比べて何がすごい？

- ニュース推薦において、knowledge entitiesとcommon senseの考慮が大事という話:
  - ニュース推薦タスクでは、他の推薦タスクと比較して推薦アイテムのlifetimeが短く、推薦候補が頻繁に新しいニュースに置き換えられるため、id-basedな推薦手法は効果的ではない。
  - なので、ニュースのタイトルや本文などのテキスト情報から言語モデル等によって**semanticな埋め込み表現**を用いたcontent-basedな推薦手法が用いられる事が多い。
  - しかしsemanticな埋め込み表現は、semantic-levelな関係性は捉えやすいが、**knowledge-entities(固有名詞?)間のつながりやcommon sense(常識?)などのknowledge-levelな関係性は捉えにくい**。
  - ニューステキストは、大量のknowledge entitiesとcommon senseで構成されてる。
- knowledge graphの活用:
  - (knowledge graph = ノードがentityに対応し、エッジがentity間の関係性に対応する、有向異種グラフの一種)
  - **ニュース間の深い論理的つながりを抽出**するためには、ニュース推薦にknowledge graph情報を追加する必要がある...!
- 本論文は、ニュース推薦タスクにおいてknowledge graph を活用する最初の論文らしい。

## 技術や手法の肝は？

### DKNの概要

- 本論文は新しいコンテンツベース推薦手法 **DKN(deep knowledge-aware network)** を提案。
  - DKNは、ニュース推薦においてknowledge graphを組み込んで外部知識を活用する。
- DKN推論時の観察可能な振る舞い:
  - 入力: 1つのニュース候補と1人のユーザのクリック履歴
  - 出力: ユーザがそのニュースをクリックする確率。
  - (この振る舞いはまさに一般的なcontent-basedのニュース推薦モデルって感じ:thinking:)
- DKN推論時の内部のざっくりした動作:
  - まず、入力されたニュースに対して、ニュースの内容を表す**テキストの各単語をknowledge graphのentityに関連付け**、情報をenrichする。
  - また、**各entityのcontextual entitiesのセット**(i.e. knowledge graph内での直接の隣接ノード)を取得し、より補完的で識別可能な情報を付与する。
  - 次に、DKNの主要なcomponentである**KCNN(knowledge-aware convolutional neural networks)**によって、ニューステキストのsemantic-level(i.e. word-level)の埋め込み表現とknowledge-level(i.e. entity-level)の埋め込み表現を**融合**し、**knowledge-awareなニュース表現を生成**する。
  - 続いて、attention moduleを使って現在の候補ニュースに関するユーザ閲読履歴の特徴を動的に集約して**ユーザ埋め込み表現を生成**する。
    - (ユーザ埋め込み表現が、候補ニュースによって変わりうる点に注意...!これは結構、他のcontent-based手法と比較したDKNの特徴な気がしている...!この場合、、ユーザ埋め込みは事前に計算せず、推論時に計算する形になるのかな:thinking:)
  - 最後に、候補ニュース埋め込みとユーザ埋め込みをCTR予測のためのDNNに入力し、出力としてCTR予測値を得る。
    - (この手法のscore prediction moduleは内積ではないのか...!だから推論コストがそこそこある感じなのかな:thinking:)

### DKNの重要なcomponent: KCNNについて

- KCNN(knowledge-aware convolutional neural networks)の2つの特徴:
  - ニュースの単語埋め込み、entity埋め込み、contextual entity埋め込みを、stackされた**3つのチャンネルとして扱う**。(つまり、**カラー画像のようなデータ**として扱う...!:thinking:)
  - **3種の埋め込みをalign**させ、単語埋め込み空間とentity埋め込み空間のheterogeneity(異質性, i.e. 違い)を除去するために、transformation function(変換関数?)を用いる。**word-entity-aligned**である。

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
