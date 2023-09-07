# Text Is All You Need: Learning Language Representations for Sequential Recommendation

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/abs/2305.13731
(勉強会発表者: morinota)

---

## どんなもの?

- KDD'23に採択されたAmazonの論文

## 先行研究と比べて何がすごい？

Sequential推薦システムって?

- Sequential推薦システムは、**過去のuser-itemのinteractionを時間的に順序付けられたsequenceとして**モデル化し、ユーザが潜在的に興味を持っているアイテムを推薦する。
  - Sequential推薦の利点は、ユーザの短期的嗜好と長期的嗜好の両方を捉える事ができること。

Sequential推薦の既存手法の多くは、**ID-basedな手法でありtransferable(移行可能)でない**点。

- Sequential推薦の既存研究では、マルコフ連鎖モデル[9, 25] -> RNN/CNNモデル[11, 17, 28, 34] -> self-attention型モデル[14, 19, 27]の順で、様々な手法が提案されてる。
- **基本的にはID-basedな手法**であり、成果物としてitem embedding tableを作成する。(もちろんいくつかの手法では、itemのcontextを特徴量としてID embeddingに組み込んでいる。)
- ID-basedな手法は、コールドスタートアイテムの理解や、**モデルを学習した後に異なる推薦シナリオに適用するcross-domain推薦(??)**の実施に難がある。
  - アイテム固有のIDは、コールドスタートアイテムや新しいデータセットのトレーニングデータからモデルが移行可能な知識を学習することを妨げる。
  - 結果として、アイテムIDはコールドスタートアイテムに対する逐次レコメンダーの性能を制限し、**継続的に追加される新しいアイテムに対して逐次レコメンダーを再トレーニングしなければならない**。

transferableな推薦システムは、cold-start itemや、cross domain推薦においても利益をもたらす。

- 最近の研究[7, 12]では、知識の**効果的なcross-domain dransfer**を行うために、異なるドメインで共通の知識を得るために**自然言語テキスト(ex. タイトル、アイテムの説明文)の一般性を活用**し、有効な性能を出している。
  - 基本的な考え方: BERT [6]のような事前に訓練された言語モデルを採用してテキスト表現を取得し、テキスト表現からアイテム表現への変換を学習すること

しかし、**言語からitemへの変換を学習するアプローチには、いくつかの限界がある**:

- (1) 事前学習済みの言語モデルは、通常、一般的な言語corpus(ex. Wikipedia)で学習され、推薦タスク用のテキスト情報とは異なる言語domainの自然言語タスクに適している。
  - (ex. 推薦タスク用のテキスト情報=本論文の手法のケースでは、item's attributeの連結)
  - よって、**事前学習済み言語モデルによるアイテムのテキスト表現は、通常、推薦タスクにおいて最適ではない**。
- (2) 事前学習済みの言語モデルから得られるテキスト表現は、**粗い粒度(文レベル)のテキスト特徴を提供するだけ**で、推薦のための細かい粒度(単語レベル)のユーザの好み(ex. 服の推薦のために最近のインタラクションで同じ色を見つける)を学習することができない。
- (3)事前学習済みの言語モデル(ex. 言語理解タスク)と変換モデル(ex. 推薦タスク)はindependent training。
  - **joint trainingできたほうが推薦タスクの為の言語理解モデルとして性能良くなるよね**...!!

本論文の提案手法 Recformer は、言語理解タスクと推薦タスクのアプローチを統合、**ID-freeのsequential推薦モデル**。
基本的な考え方は、**言語理解と逐次推薦のjoint training**を通じて、言語モデルの汎用性を利用しtransferableな推薦システムを作る事。

## 技術や手法の肝は?

### モデルの入力情報にitem_idを含めない

テキストとitem idの両方を入力データとして使用する既存研究のsequential推薦モデルとは異なり、**recformerではsequential推薦にテキストのみを使用する**。

- sequential推薦の問題設定では、アイテム集合 $I$ とユーザのinteraction sequence $s = {i_1, i_2, \cdots, i_n}$ が時間順に与えられ、$s$ に基づいてnext itemを予測する。
- $s$ 内の各 interacted item $i$ は、既存手法では一意のitem idと関連付けられるが、**Recformerではその代わりに、属性辞書(attribute dictionary) $D_i$ と関連付けられる**。
  - $D_i$ は key-value型の属性情報 ${(k_1, v_1), (k_2, v_2), \cdots, (k_m, v_m)}$ を含む。
    - ここで $k$ はあるattribute名(ex. Color), $v$ は対応する値(ex. Black)。
  - **$k$ と $v$ は共に自然言語で記述され**、単語のsequence $(k, v) = {w_1^{k}, \cdots, w_c^{k}, w_1^{v}, \cdots, w_c^{v}}$ を含む。
    - ここで $w^{k}$ と $w^{v}$ は言語モデルの共有語彙(shared vocabulary)にある $k$ と $v$ の各単語、$c$ はテキストの切り捨て(truncated)長さ。
  - アイテム $i$ の属性辞書 $D_i$ には、タイトル、説明文、色など、あらゆる種類のアイテムのテキスト情報を含めることができる。
  - 図2で示す様に、$D_i$ を言語モデルに投入する為に、key-value attribute ペア達を $T_{i} = {k_1, v_1, k_2, v_2, \cdots, k_m, v_m}$ の様に平滑化して、**入力データとして item "sentence" $T_{i}$**を得る。

![fig2]()

### Recformer のモデルアーキテクチャ

図3(a)はRecformerのアーキテクチャ。**Longformer(Long Document Transformer)[2]と同様の構造を持ち**、**多層双方向トランスフォーマー[30]を採用**し、配列の長さに応じて線形にスケールする(=計算量が??)アテンションメカニズムを持つ。Longformerだけでなく他の双方向Transformer構造にも適用可能。

![fig3]()

### モデルの入力:

- ユーザのinteraction sequence $s = {i_{1}, i_{2}, \cdots, i_{n}}$ をモデル入力用にencodeする為に、まずsequenceのアイテムを ${i_{n},i_{n-1}, \cdots, $i_{1}}$ に**逆変換**する。
  - これは直感的に**最近のアイテム (i.e.$, i_n, i_{n-1}, \cdots$) の方が次のアイテム予測に重要**であり、sequence逆変換により最近のアイテムが入力データに確実に含まれる様にしたいから。
  - (i.e. sequenceを指定した最大長でtruncateするので、最新のinteractionが切れない様したいから!:thinking:)
- 続いて、$s$ 内のアイテム $i$ を対応する item sequence $T_{i}$ で置換する。
- 最後にsequenceの先頭に特別なトークン[CLS]を追加する。

したがって、モデルの入力は次のように表記される:

$$
X = \{[CLS], T_n, T_{n-1}, \cdots, T_{1}\}
\tag{1}
$$

ここで $X$ は、過去のinteraction sequence $s$ の中でユーザがinteractしたすべてのアイテムに対応する属性辞書 を含む単語達 **$T_{i}$ のsequence**(=**sequence of sequences**) である。(各 $T_{i}$ を平滑化して、sentence of wordsになる、という認識:thinking:)

$X$ は後述する埋め込み層に入力される。

### 4種類の埋め込み層

Recformerの目標は、**言語理解と推薦のsequentialパターンの両面からモデル入力 $X$ を理解する**こと。
本手法での重要なアイデアは、言語モデルとself-attention型seuquential推薦モデルの埋め込み層を組み合わせること。
その為にRecformerは、以下の**4種の埋め込み**を含む:

(ちなみに**最終的なTransformerへの入力は、4種の埋め込みベクトルのlayer Normalization後の和になる**。)

- **トークン埋め込みベクトル(Token embedding)**:
  - 各単語tokenの意味を表現する。
  - 言語モデル由来の埋め込み。
  - $A \in \mathbb{R}^{V_w \times d}$
  - ここで、$V_w$ はvocabularyに登録されている単語数、$d$ は埋め込み次元。
  - $A$ のサイズはアイテム数に依らない。
- **トークン位置埋め込みベクトル(Token position embedding)**:
  - sequence内のトークンの位置を表現する。
  - これも言語モデル由来の埋め込み。
  - $B_{i} \in \mathbb{R}^{d}$
  - 通常のTransformer論文と同様に、tokenの連続パターンを理解するのを助ける為の埋め込み。
- **トークンタイプ埋め込みベクトル(Token type embedding)**:
  - 各tokenの種類を表現する。
  - この埋め込みベクトルは、Recformerの入力データの形状ゆえに必要!
  - 具体的には、token type embedding は、3つのベクトル $C_{[CLS]}, C_{Key}, C_{Value} \in \mathbb{R}^{d}$ を含み、tokenがそれぞれ[CLS]、属性key、属性valueのどれかを表す。
- **アイテム位置埋め込みベクトル(Item position embedding)**:
  - interaction sequence内のアイテムの位置を表現する。
  - sequential推薦モデル由来の埋め込み。
  - sequence $X$ の $k$ 番目のアイテムの属性からの単語は、$D_{k} \in \mathbb{R}^{d}$ と $D \in \mathbb{n \times d}$ として表現される ($n$ はユーザのinteraction sequence $s$ の最大長)。

入力sequence $X$ から各単語token $w$ が与えられると、token $w$ の埋め込みベクトルは、4つの異なるembeggings の和のLayer Normalizationとして計算される:
(ここでのword $w$ は、itemを意味するのではなく、あるitemの"item sentence" $T_i$ に含まれる一つの単語、という認識:thinking:)

$$
\mathbf{E}_{w} = LayerNorm(\mathbf{A}_{w} + \mathbf{B}_{w} + \mathbf{C}_{w} + \mathbf{D}_{w})
\tag{2}
$$

ここで、$\mathbf{E}_{w} \in \mathbb{R}^{d}$。
よってモデル入力 $X$ の埋め込みベクトルは、$\mathbf{E}_{w}$ のsequenceになる:

$$
\mathbf{E}_{X} = [E_{[CLS]}, E_{w_1}, \cdots, E_{w_l}]
\tag{3}
$$

ここで、$\mathbf{E}_{X} \in \mathbb{R}^{(l+1) \times d}$ であり、$l$ はユーザのinteraction sequence におけるtokenの最大長。($s$ の最大長ではなく、$X$ の最大長である点に注意...! $+1$ は[CLS]の意味。)

### Transfomerに通して、アイテム表現またはSequence表現を得る。

$E_{X}$ を符号化するために、**双方向トランスフォーマー構造Longformer(Longformer = Long Document Transformer...!)**をencoderとして採用する。
**$X$ は通常長いsequenceなので、Longformerのlocal windowed attention**(=対象tokenのすぐ近くのtoken達に対するattention weightのみを保持するattention pattern。)は、$E_{x}$ を効率的にencodeするのに役立つ。
特別なトークン[CLS]はグローバルなattentionを持たせるが、他のトークンはlocal windowed attentionを使う。

よって、Recformerは以下の様な $l+1$ 個の $d$ 次元の単語token表現 $\mathbf{h}_{w}$ を計算する:

$$
[\mathbf{h}_{[CLS]}, \mathbf{h}_{w_1}, \cdots, \mathbf{h}_{w_l}]
= Longformer([E_{[CLS]}, E_{w_1}, \cdots, E_{w_l}])
\tag{4}
$$

ここで $\mathbf{h}_{w} \in \mathbb{R}^{d}$ である。
言語モデルが[CLS]のtoken表現をsentence表現として使用するのと同様に、**最初のトークン[CLS]の表現 $\mathbf{h}_{[CLS]}$ がFsequence表現として使用される**。

また、Recformerでは、**アイテムの埋め込みテーブルを保持しない**。(RecformerはID-freeなモデルだから...!:thinking:)
その代わりに、各アイテムを「interaction sequence $s$ にitemが一つしか無い」特別なケースとみなす。
よってRecformerのアイテム表現は、各アイテム $i$ について、そのitem sequence $T_i$ を構成し、$X = \{[CLS],T_i\}$ をモデル入力として、そのsequence表現 $h_{[CLS]}$ をアイテム表現 $\mathbf{h}_{i}$ として取得する。

### Recformerの推論

## どうやって有効だと検証した?

- オンライン実験ではなく、オフラインデータセットを用いた評価のみだった。
-

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
