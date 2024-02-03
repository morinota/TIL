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
  - まず、入力されたニュースに対して、ニュースの内容を表す**テキストの各単語をknowledge graphのentityに関連付ける**。
  - また、**各entityのcontextual entitiesのセット**(i.e. knowledge graph内での直接の隣接ノード)も関連付ける。
  - 次に、DKNの主要なcomponentである**KCNN(knowledge-aware convolutional neural networks)**によって、ニューステキストのsemantic-level(i.e. word-level)の埋め込み表現とknowledge-level(i.e. entity-level)の埋め込み表現を**融合**し、**knowledge-awareなニュース表現を生成**する。
  - 続いて、attention moduleを使って現在の候補ニュースに関するユーザ閲読履歴の特徴を動的に集約して**ユーザ埋め込み表現を生成**する。
    - (ユーザ埋め込み表現が、候補ニュースによって変わりうる点に注意...!これは結構、他のcontent-based手法と比較したDKNの特徴な気がしている...!この場合、、ユーザ埋め込みは事前に計算せず、推論時に計算する形になるのかな:thinking:)
  - 最後に、候補ニュース埋め込みとユーザ埋め込みをCTR予測のためのDNNに入力し、出力としてCTR予測値を得る。
    - (この手法のscore prediction moduleは内積ではないのか...!だから推論コストがそこそこある感じなのかな:thinking:)

### (おまけ) knowledge graph埋め込みの作り方について何も知らなかったのでメモ

- knowledge graphの構成:
  - 典型的なknowledge graphは、数百万の**entity-relation-entityのtriplet** (三つ組) $(h, r, t)$ で構成されている。
  - ここで、h、r、tはそれぞれtripletのhead、relation、tailを表す。
- knowledge graph埋め込みの目的:
  - knowledge graph内の全てのtripletが与えられた時、**元のknowledge graphの構造情報を保持しつつ、各entityとrelationの低次元表現ベクトルを学習すること**。
- **translation-basedな** knowledge graph embedding手法:
  - translation-based(翻訳ベース?) knowledge graph embedding手法は、簡潔なモデルと優れたパフォーマンスにより近年人気らしい。(2018年頃はそうだったらしい。2024年現在はどうなんだろう?)
- 論文内では、読者がself-containedできるように、以下のxつのtranslation-basedなknowledge graph embedding手法を簡単に紹介してくれてた...! (たぶん、スコア関数 i.e. 良い埋め込みの定義が少し違うだけっぽいかな...??:thinking:)

  - 1. TransE
  - 2. TransH
  - 3. TransR
  - 4. TransD

- 1つ目: TransEの概要:
  - knowledge graph内のtriplet $(h, r, t)$ に対して、$\mathbf{h} + \mathbf{r} \approx \mathbf{t}$ となるように、entityとrelationの埋め込みを学習する手法。
    - 参考: https://yamaguchiyuto.hatenablog.com/entry/2016/02/25/080356
  - よってTransEは、以下のスコア関数を仮定する:
    - このスコア関数は、$(h, r, t)$ が成立(=tripletの正例)するときに低く、そうでない(=tripletの負例)ときに高くなる。
    - (**このスコア関数をグラフ内の全てのtripletに対して最小化するような損失関数を設計して、entityとrelationの埋め込みを学習する感じ...!**:thinking)

$$
f_r(h,t) = \|\mathbf{h} + \mathbf{r} - \mathbf{t}\|^{2}_{2}
\tag{1}
$$

- 2つ目: TransHの概要:
  - entityの埋め込みをrelation 超平面に射影することで、異なるrelationに関与するときに異なる表現を持てるようにした手法。
  - スコア関数は以下:
    - ここで、$\mathbf{h}_{\perp} = \mathbf{h} - \mathbf{w}_{r}^{\top} \mathbf{h} \mathbf{w}_{r}$ と $\mathbf{t}_{\perp} = \mathbf{t} - \mathbf{w}_{r}^{\top} \mathbf{t} \mathbf{w}_{r}$ は、それぞれ $\mathbf{h}$ と $\mathbf{t}$ を超平面 $\mathbf{w}_{r}$ に射影したもの。
    - $\|\mathbf{w}_{r}\|_{2} = 1$。

$$
f_r(h,t) = || \mathbf{h}_{\perp} + \mathbf{r} - \mathbf{t}_{\perp} ||^{2}_{2}
\tag{2}
$$

- 3つ目: TransRの概要:
  - 各 relation r に対して、entity埋め込みを対応するrelation空間にマッピングするための射影行列 $M_{r}$ を導入する。
  - スコア関数は以下:
    - ここで、$\mathbf{h}_{r} = \mathbf{h} M_{r}$ と $\mathbf{t}_{r} = \mathbf{t} M_{r}$。

$$
f_r(h,t) = ||\mathbf{h}_{r} + \mathbf{r} - \mathbf{t}_{r}||^{2}_{2}
\tag{3}
$$

- 4つ目: TransDの概要:
  - TransRの射影行列を、entity-relationペアの2つの射影ベクトルの積に置き換える。
  - スコア関数は以下。
    - ここで、$\mathbf{h}_{\perp} = (\mathbf{r}_{p} \mathbf{h}_{p}^{\top} + \mathbf{I}) \mathbf{h}$ 、 $\mathbf{t}_{\perp} = (\mathbf{r}_{p} \mathbf{t}_{p}^{\top} + \mathbf{I}) \mathbf{t}$ 、 $\mathbf{h}_{p}$ 、 $\mathbf{r}_{p}$ 、 $\mathbf{t}_{p}$ は、entityとrelationのべつのベクトル集合。$\mathbf{I}$ は単位行列。

$$
f_r(h,t) = ||\mathbf{h}_{\perp} + \mathbf{r} - \mathbf{t}_{\perp}||^{2}_{2}
\tag{4}
$$

- 上記の全てのembedding手法について、スコア関数をもとにした以下のランキング損失関数を使って学習する。
  - $\gamma$ はマージン、 $\Delta$ と $\Delta'$ は正しいtripletと正しくないtripletの集合。
  - (正例と負例をペアにして渡す、pairwiseのランキング損失関数だ:thinking:)

$$
L = \sum_{(h,r,t) \in \Delta} \sum_{(h',r,t') \in \Delta'} \max(0, \gamma + f_r(h,t) - f_r(h',t'))
\tag{5}
$$

### Knowledge Distillation(ニューステキストから知識を蒸留する?)について

![figure4]()

- DKNの最初のステップ。
- Knowledge Distillationは以下の4つのステップから構成される(図4)

  - 1. entity linking:
    - ニューステキスト中の単語をknowledge graphのentityに関連付ける。
  - 2. knowledge graph construction:
    - 関連付けられたentityに基づいて、knowledge graphからサブグラフを抽出する。
    - (元のknowledge graph全体が必要なわけじゃなくて、今回のデータに登場するentityだけが含まれるサブグラフを作るってことかな...!:thinking:)
    - このとき、関連付けられたentityだけじゃなくて、1ホップ以内のすべてのentityをサブグラフに含める。(これがcontextual entityのセットになる)
  - 3. knowledge graph embedding:
    - 抽出したサブグラフに対して、knowledge graph embedding手法を適用して、各entityとrelationの埋め込みを学習する。(論文ではTransDを採用してた)
  - 4. entity embedding:
    - ニューステキスト中の単語に関連付けられた各entityの埋め込みを、knowledge graph embeddingから取得する。
    - この際、対象entityそのもの埋め込みに加えて、文脈情報を追加するためにcontextual entities集合のentity embeddingから算出するcontexutal embeddingも取得する。

- ちなみに、DKNでは**contextual entities集合**を「知識グラフ内のその直接の隣接ノードの集合」と定義してる。
  - 数式で表すと以下:
    - ここで $r$ はrelationであり、$G$ はknowledge graph。
    - (orだから矢印の向きは問わないってことか)

$$
context(e) = \{
    e_{i} | (e, r, e_{i}) \in G
    or
    (e_{i}, r, e) \in G\}
\tag{9}
$$

- contextual entitiesを使う動機:
  - 通常、semanticとlogicの観点から、contextual entitiesは対象entityと密接に関連している。よって、**contextual entitiesはより補完的な情報を提供し、対象entityの識別性を向上させられるはず**...!
  - contextの例(図5):
    - 表現したい対象entity = “Fight Club”(映画の名前)
    - contexutal entities = “Suspense”(ジャンル), “Brad Pitt”(俳優), “United States”(国), “Oscars”(賞)
    - 対象entityの特徴を表現するために、“Fight Club”自体の埋め込みを使用するだけでなく、そのcontext、例えば“Suspense”（ジャンル）、“Brad Pitt”（俳優）、“United States”（国）および“Oscars”（賞）をその識別情報として使用したい...!
  - 実験セクションにて、contextual entitiesを使うことの有効性を検証してた。
- contexual embeddingの算出方法:
  - 対象entity $e$ のcontext ($context(e)$) が与えられた時、contexual embedding $\bar{\mathbf{e}}$ はcontextのentity embeddingの平均として算出される。
  - 数式だと以下。
    - ここで、$\mathbf{e}_{i}$ はknowledge graph embeddingで取得したentity $e_{i}$ の埋め込み。

$$
\bar{\mathbf{e}} = \frac{1}{|context(e)|} \sum_{e_{i} \in context(e)} \mathbf{e}_{i}
\tag{10}
$$

### DKNの重要なcomponent: KCNNについて

- KCNN(knowledge-aware convolutional neural networks)の2つの特徴:

  - ニュースの単語埋め込み、entity埋め込み、contextual entity埋め込みを、stackされた**3つのチャンネルとして扱う**。(つまり、**カラー画像のようなデータ**として扱う...!:thinking:)
  - **3種の埋め込みをalign**させ、単語埋め込み空間とentity埋め込み空間のheterogeneity(異質性, i.e. 違い)を除去するために、transformation function(変換関数?)を用いる。**word-entity-aligned**である。

- KCNNの入力データが作られる流れ:
  - 1. 長さ $n$ のニュースタイトル $t$ の単語sequenceを入力として受け取る。
    - $t = w_{1:n} = [w_{1}, w_{2}, \cdots, w_{n}]$
  - 2. 言語モデル等によって、各単語 $w_{i}$ は、対応する単語埋め込み $\mathbf{w}_{i}$ を関連付けられる。(これはsemanticな埋め込み:thinking:) ($d$ はsemantic埋め込みの次元数。)
    - よって単語埋め込みsequenceはこんな感じ: $\mathbf{w}_{1:n} = [\mathbf{w}_{1} \mathbf{w}_{2} \cdots \mathbf{w}_{n}] \in \mathbb{R}^{d \times n}$
  - 3. さらにKnowledge Distillationによって、各単語 $w_{i}$ は、entity埋め込み $e_{i} \in \mathbb{R}^{k \times 1}$ とcontextual埋め込み $\bar{e}_{i} \in \mathbb{R}^{k \times 1}$ に関連付けられる。($k$ は知識グラフ埋め込みの次元数)
    - (どのentityにも紐づかない助詞みたいな単語もあるだろうけど、それらは削除するのかな:thinking:)
  - よって、1つのニュースのKCNNへの入力sequenceは、**各単語に対して3種の埋め込み(単語埋め込み、entity埋め込み、contexual埋め込み)が紐付けられたsequence**になる。

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
