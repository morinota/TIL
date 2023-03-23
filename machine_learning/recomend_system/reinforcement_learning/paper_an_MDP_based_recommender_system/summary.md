# An MDP-Based Recommender System

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://www.jmlr.org/papers/volume6/shani05a/shani05a.pdf
(勉強会発表者: morinota)

---

## どんなもの?

## 先行研究と比べて何がすごい？

- 推薦システムにおいてMDP()を定義した、最初の論文.(たぶん)

## 技術や手法の肝は？

### 推薦システムにおけるMDPを定義する

MDPを定義するためには、状態(state)、行動(action)、遷移関数(transition function)、報酬関数(reward function)のセットを提供する必要がある.

#### state:

- アイテム（例えば、本、CD）の k-tuples(interaction履歴?)に対応.
- そのうちのいくつかの接頭辞は、アイテムの欠落に対応するNULL値を含むことができる.(ユーザのinteractionがk個に満たないケース)

#### action:

- アイテムの推薦に対応.
- 複数の推奨アイテムリストを検討することも可能だが、本論文ではシンプルに、一つの推薦アイテムを検討している.

#### reward:

- プロダクトが定義する interaction (ex. 商品を売る, ウェブページを見せる, etc.)の効用を符号化したもの.
- state は interaction したアイテムのリストを符号化するため、reward は現在の state を定義する最後のアイテムにのみ依存する.
- ex) state $(x1, x2, x3)$の reward は、アイテム$x3$ への interaction からサイトが生み出す報酬.
- 本論文では、reward　として net profit(アイテムの購入による純利益?)を使用している.

#### state transition:

- 各action(アイテム推薦)後のstateは、その推薦に対するユーザのresponceによって決まる.
- アイテム $x'$ を推薦した場合、ユーザには次の3つの選択肢がある.
  - この推薦を受け入れることで、state $(x1, x2, x3)$ から $(x2, x3, x')$に移行する.
  - $x'$とは別の、非推薦アイテム$x''$を選択することで、state $(x1, x2, x3)$ から $(x2, x3, x'')$に移行する.
  - 何もしない(ex. ユーザーがセッションを終了する)事で、そのままの state を維持する.

したがって、本MDPモデルにおける**state transitionの確率的要素は、ユーザの実際の選択**である.

上のケースのtransition functionは以下:

$$
tr^{1}_{MDP} (<x_1, x_2, x_3>, x', <x_2, x_3, x''>)
\tag{13}
$$

これは、state $<x1, x2, x3>$ でアイテム $x'$ が推薦されてる場合に、ユーザがアイテム $x''$ を選択する確率.
ここで、k=1のsingle item recommendationsを表すために、$tr^{1}_{MDP}$と表記している.

### transition function の初期化方法の工夫

**transition functionの適切な初期化**は、推薦システムのMDPにおける重要な実装課題である.
従来のモデルベースの強化学習アルゴリズムが、遷移関数の適切な値(i.e. 最適な方策と言ってもいい?今回の場合はtransition function)をオンラインで学習するのとは異なり、**推薦システムの場合、最初に展開するときにかなり正確である必要がある.**

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
