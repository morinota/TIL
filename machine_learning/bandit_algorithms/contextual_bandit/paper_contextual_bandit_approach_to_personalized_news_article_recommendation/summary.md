# A contextual-bandit approach to personalized news article recommendation

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/pdf/1003.0146.pdf
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

context-freeなbanditアルゴリズムである UCB を、contextual banditアルゴリズムとして拡張したいが、既存の手法では**各armの報酬推定値のUCBの推定コスト(=計算量)**が高い...。
本論文では、**報酬モデルが線形**である場合(i.e. 報酬と特徴量の関係が線形と仮定できる場合)に、**報酬推定値のUCBをclosed-formで(=解析的に=計算コスト少なく!)計算できる**事を示し、LinUCBアルゴリズムを提案する。

論文では、まず**disjointな線形モデルに対するLinUCBアルゴリズム**を説明している。(=異なるarm間でパラメータが共有されないケース!)
続いて、より一般的な **hyblidな線形モデルに対するLinUCBアルゴリズム**を説明している。(=arm固有のパラメータに加えて、全てのarmで共有されるparameterも使用するケース!)

### disjointな線形モデルに対するLinUCBアルゴリズム

- 仮定:
  - ある arm $a$ の期待報酬が、その $d$ 次元特徴量 $x_{t,a}$ について線形な関係である。
  - i.e. 全ての試行 $t$ において、以下を満たす様なcoefficient vector $\mathbf{\theta}_{a}^{*}$ が存在する。

$$
\mathbb{E}[r_{t,a}|\mathbf{x}_{t,a}] = \mathbf{x}_{t,a}^{T} \mathbf{\theta}_{a}^{*}
$$

このモデルは、**異なるarm間でパラメータが共有されない(=arm $a$ 毎にユニークなパラメータを持つ:thinking:)**ため、"disjoint"と呼ばれる。

学習用データ ($D_{a}, \mathbf{c}_{a}$) にridge回帰を適用すると、以下のparameter推定値が得られる(=OLS推定量とほぼ同じ形に見えるけど、どこが違うんだっけ?):

$$
\hat{\mathbf{\theta}}_{a} = (D_{a}^T D_{a} + I_{d})^{-1} D_a^{T} \mathbf{c}_{a}
\tag{3}
$$

ここで、

- $D_{a} \in \mathbb{R}^{m \times d}$ は $m$ 個のtraining input(ex. 記事 $a$ について過去に観察された $m$ 個の $d$ 次元のcontext)
- $\mathbf{c}_{a} \in \mathbb{R}^{m}$ はresponce vector(ex. 記事 $a$ について過去に観察された $m$ 個のクリック/クリックなしのユーザフィードバック)
- $I_{d}$ はd×dのidentity matrix(単位行列)。

そして、$\mathbf{c}_{a}$ の成分が $D_a$ の対応する行を条件として独立である(i.e. contextで条件付けた場合に各feedbackの結果は独立になる?)時、少なくとも $1-\delta$ の確率(ex. 90%とか?)で以下が示される:
(=これが**期待報酬の推定値のUCBがclosed-formで計算できる**って話!:thinking:)

$$
|\mathbf{x}_{t,a}^{T} \hat{\mathbf{\theta}}_{a} - \mathbb{E}[r_{t,a}|\mathbf{x}_{t,a}]|
\leq
\alpha \sqrt{\mathbf{x}_{t,a}^T (D_a^T D_a + I_d)^{-1} \mathbf{x}_{t,a}}
\tag{4}
$$

上式は、全ての $\delta > 0$ と $x_{t,a} \in \mathbb{R}^{d}$ で成立する。ここで、 $\alpha = 1 + ln(2/\delta)/2$ は定数である。(ユーザによって指定されるハイパーパラメータ)

なお、式(4)の信頼区間のclosed-formに関しては、いくつか導出方法があるらしい。
(ex. ridge回帰をベイジアンアプローチによる点推定として解釈。微分エントロピー的に。etc. )

式(4)の不等式を用いて、contextual bandit × UCBの arm 選択戦略を導出できる。即ち 各試行 $t$ において、以下のようにarm $a_{t}$ を選択する:

$$
a_{t} := \argmax_{a \in A_t} (
  \mathbf{x}_{t,a}^{T} \hat{\mathbf{\theta}}_{a}
  + \alpha \sqrt{\mathbf{x}_{t,a}^T A_{a}^{-1} \mathbf{x}_{t,a}}
  )
\\
\text{where} A_{a} := D_a^T D_a + I_d
\tag{5}
$$

($\argmax$ の中身は、各arm の期待報酬のUCB。context-freeなUCB手法と同様に、LinUCBは常に最も高いUCBを持つアームを選択する)

![algorithm 1]()

アルゴリズム1は、LinUCBアルゴリズム全体の詳細な説明であり、唯一の入力パラメータ(=ハイパーパラメータ)は $\alpha$。

(あと疑似コード中にて、たぶん $\mathbf{b}_{a} \in \mathbb{R}^{d} := D_{a}^T \mathbf{c}_{a}$ )

### hyblidな線形モデルに対するLinUCBアルゴリズム

disjoint LinUCBの報酬モデルに別の線形項を追加する。

$$
\mathbb{E}[r_{t,a}|x_{t,a}]
= \mathbf{z}_{t,a}^T \mathbf{\beta}^*
+ \mathbf{x}_{t,a}^T \mathbf{\theta}_{a}^*
\tag{6}
$$

ここで、

- $z_{t,a} \in \mathbb{R}^{k}$ は 試行 $t$ 時点でのユーザと記事の組み合わせの特徴量。
- $\beta^{*} \in \mathbb{R}^{k}$ はすべてのアームに共通する未知のcoefficient vector。

このモデルは、共有された係数 $\beta^{*}$ と 非共有の係数 $\theta_{a}^{*}$ の両方を持つ、という意味でhyblid。

![algorithm 2]()

## どうやって有効だと検証した?

logging policyによって収集されたデータを使って、target policyの性能を推定する OPE をしてた!

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装

$$
$$
