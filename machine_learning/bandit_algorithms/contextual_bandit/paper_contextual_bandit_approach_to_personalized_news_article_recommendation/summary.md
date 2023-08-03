# A contextual-bandit approach to personalized news article recommendation

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## どんなもの?

## 先行研究と比べて何がすごい？

### 個別化推薦における contextual multi-armed bandit の定式化

試行$t$において,

- 1. アルゴリズムは、ユーザ $u_t$ と action(arm)の集合 $A_{t}$ をその特徴量ベクトル $x_{t,a}, a \in A_{t}$ とともに観察する。ここで、**ベクトル $x_{t,a}$ は、ユーザ $u_{t}$ と action $a$ の両方の情報を要約しており、contextと呼ばれる**。
- 2. 過去の試行で観察されたpayoffs(=報酬?)に基づいて、アルゴリズムはあるaction $a \in A_{t}$ を選択し、報酬 $r_{t, a_t}$ を受け取る。(報酬の期待値は $u_t$ と action $a_t$ の両方に依存する)
- 3. その後アルゴリズムは、新しい観測値 $(x_{t, a_t}, a_t, r_{t, a_t})$ でaction選択戦略を改善する。ここで重要な事は、選ばれてないarms $a \neq a_{t}$ にはfeedback(=報酬 $r_{t, a}$)が観測されない、という事。

## 技術や手法の肝は？

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
