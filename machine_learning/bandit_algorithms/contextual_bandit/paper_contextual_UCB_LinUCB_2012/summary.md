# A contextual-bandit approach to personalized news article recommendation

published date: 1 May 2012,
authors: Lihong Li, Wei Chu, John Langford, Robert E. Schapire
url(paper): <https://arxiv.org/pdf/1003.0146.pdf>
(勉強会発表者: morinota)

---

## どんなもの?

- **UCB(Upper Confidence Bound)アルゴリズムを contextual bandit に拡張**し、Yahooのニュース推薦に適用した論文。
- UCB手法 × contextual bandit を組み合わせたいが、既存研究ではUCBを推定する際の計算コストが高くなる欠点があった。
- しかし本論文で提案した **LinUCB** では、**報酬とcontext(特徴量)の関係が線形と仮定できる場合**に、UCBをclosed-formで (i.e. 解析的に => コスト効率がめちゃいい!) 計算でき、実用性が高い。
- あと開発中のpolicyのオフライン評価方法として、**logging policyとして一様ランダム policy を一定期間稼働させてlogデータを収集**し、biasなくpolicyの性能を推定する方法も提案していた。(この方法が個人的には収穫だった...!!シンプルだが実環境でも適用しやすいし...!!:thinking:)

### (補足) パーソナライズ推薦における contextual multi-armed bandit の定式化

試行$t$において,

- 1. アルゴリズムは、ユーザ $u_t$ と action(arm)の集合 $A_{t}$ をその特徴量ベクトル $x_{t,a}, a \in A_{t}$ とともに観察する。ここで、**特徴量ベクトル $x_{t,a}$ は、ユーザ $u_{t}$ と action $a$ の両方の情報を要約しており、contextと呼ばれる**。
- 2. 過去の試行で観察されたpayoffs(=報酬?)に基づいて、アルゴリズムはあるaction $a \in A_{t}$ を選択し、報酬 $r_{t, a_t}$ を受け取る。(報酬の期待値は ユーザ $u_t$ と行動 $a_t$ の両方に依存する)
- 3. その後アルゴリズムは、新しい観測値 $(x_{t, a_t}, a_t, r_{t, a_t})$ でaction選択戦略を改善する。ここで重要な事は、選ばれてないarms $a \neq a_{t}$ にはfeedback(=報酬 $r_{t, a}$)が観測されない、という事。
  - 反実仮想的な問題設定!

## 先行研究と比べて何がすごい？

context-freeなbanditアルゴリズムである UCB を、contextual banditアルゴリズムとして拡張したいが、既存の手法では**各armの報酬推定値のUCBの推定コスト(=計算量)**が高い...。
本論文では、**報酬モデルが線形**である場合(i.e. 報酬と特徴量の関係が線形と仮定できる場合)に、**報酬推定値のUCBをclosed-formで(=解析的に=計算コスト少なく!)計算できる**事を示し、LinUCBアルゴリズムを提案してる。

## 技術や手法の肝は？

論文内では、まず**disjointな線形モデルに対するLinUCBアルゴリズム**を説明している。(=異なるarm間でモデルパラメータが共有されないケース!)
続いて、より一般的な **hyblidな線形モデルに対するLinUCBアルゴリズム**を説明している。(=arm固有のパラメータに加えて、全てのarmで共有されるパラメータも使用するケース!)

### disjoint(arm間でモデルパラメータが独立!)な線形モデルに対するLinUCBアルゴリズム

- LinUCBモデルの仮定:
  - **ある arm $a$ の期待報酬が、その $d$ 次元特徴量 $x_{t,a}$ について線形な関係である。**
  - i.e. 全ての試行 $t$ において、以下を満たす様な coefficient vector $\mathbf{\theta}_{a}^{*}$ が存在する。

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

ちなみに、式(4)の信頼区間のclosed-formに関しては、いくつか導出方法があるらしい。
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

($\argmax$ の中身は、各 arm の期待報酬のUCB。context-freeなUCB手法と同様に、LinUCBは常に最も高いUCBを持つアームを選択する)

![algorithm 1]()

上の疑似コードは、disjointなLinUCBアルゴリズムの各armの全体の流れ(期待報酬のUCBの導出、arm選択、報酬の獲得、モデルパラメータの更新)を示している。
本アルゴリズムの唯一のハイパーパラメータは $\alpha$。

(あと疑似コード中にて、たぶん $\mathbf{b}_{a} \in \mathbb{R}^{d} := D_{a}^T \mathbf{c}_{a}$ )

### hyblidな線形モデルに対するLinUCBアルゴリズム

disjoint LinUCBの報酬モデルに**別の線形項を追加**する。

$$
\mathbb{E}[r_{t,a}|x_{t,a}]
= \mathbf{z}_{t,a}^T \mathbf{\beta}^*
+ \mathbf{x}_{t,a}^T \mathbf{\theta}_{a}^*
\tag{6}
$$

ここで、

- $z_{t,a} \in \mathbb{R}^{k}$ は 試行 $t$ 時点での**ユーザと記事の組み合わせの特徴量**。
  - (一方で、$x_{t,a} \in \mathbb{R}^{d}$ は 試行 $t$ 時点での**記事 $a$ の特徴量**)
- $\beta^{*} \in \mathbb{R}^{k}$ はすべてのアームに共通する未知のcoefficient vector。

このモデルは、共有された係数 $\beta^{*}$ と 非共有の係数 $\theta_{a}^{*}$ の両方を持つ、という意味でhyblid。

![algorithm 2]()

上の疑似コードは、hybridなLinUCBアルゴリズムの各armの全体の流れ(期待報酬のUCBの導出、arm選択、報酬の獲得、モデルパラメータの更新)を示している。
本アルゴリズムの唯一のハイパーパラメータは、同様に $\alpha$。

## どうやって有効だと検証した?

contextual banditアルゴリズムのオフライン評価(i.e. Off-Policy Evaluation)方法も提案していた。

本論文のオフライン評価方法を実施する上で満たすべき仮定は以下。

- 個々のイベントがi.i.d.である。(各試行が独立、みたいな認識:thinking:)
- ログデータを収集するために使用された **logging policy が各試行で一様にランダムに各アームを選択する**。

上記の仮定を満たした上で、本論文では naive なOPEで推定してた。(実際には、以下の疑似コードの方法。)
(**OPEはlogging policyのarmの選択傾向に影響を受けた結果になってbiasが発生するはずだが、一様ランダムなlogging policyの場合は、naiveなOPEでも問題ないのか...**!:thinking:)

![]()

実験は、上で提案されたオフライン評価方法をYahoo!Todayモジュール(今日のトップニュース的な!)で集めた適用し、LinUCBの有効性を評価してた。方法の概要は以下:

- Yahoo Todayモジュールでは、記事プールの中から品質の高い**4つの記事**を編集者によってcurateしている。**4つの記事のうち、1つをハイライト**している
  - 図1の様にフッターの位置には4つの記事があり、F1-F4でindex付けされている。
- 一定期間、**F1の記事の選択ロジックに一様ランダムなpolicyを適用**し(=logging policy)、logデータを収集した。
  - この方法は、推薦システムオフライン評価難しい問題の、一番シンプルな解決策かも??**複数の推薦アイテムのうち、1つだけ一様ランダムにしてもユーザへの悪影響は大きくない気がするし**...!:thinking:
  - ずっと一様ランダムなpolicyを適用するのではなく、1週間とか1ヶ月とかのみ、推薦モジュールの1箇所のみ、であれば実際に適用可能性あるのでは...?:thinking: その試用期間で得られたlog dataをオフライン評価で使い続ければ良いし。
- 論文では、LinUCBに入力するcontextの特徴量エンジニアリング頑張ってた。
- ３種のアルゴリズム群を比較検証していた:context-free手法, "warm-start"を含んだ手法, "contextual-bandit"系手法。
- ビジネス上の機密情報を保護する為、**各アルゴリズムのCTR推定値を logging policy (=random policy) のCTRで割ったrelative CTR**を報告している。(なるほど...!確かに「このサービスってCTRこれくらいなんだ」って思わせちゃうしなー:thinking:)

![]()

### 特徴量エンジニアリング的な話

- ユーザ特徴量の扱い方:
  - 生の特徴量は以下:
    - 性別(カテゴリ特徴量)
    - 年齢を10個のビンに分割したもの(カテゴリ特徴量)
    - 世界のどの都市にいるかの地理情報(カテゴリ特徴量)
    - 過去にクリックした記事のカテゴリのヒストグラム?(list型の数値特徴量)
  - 前処理:
    - 元々は、上述のカテゴリ特徴1000次元以上のone-hotやbinary表現で表される1000次元以上の疎ベクトル。
    - "support"値(ユーザの何割がその特徴量を持っているか)が0.1以上の特徴量のみを残す。
    - 次元削減で密な特徴量ベクトルに変換した上で、k-meansクラスタリングを適用しユーザを5つのクラスタに分割。
    - その後、ユーザが各クラスタにどれだけ近いか(混合度)を「ガウスカーネル」みたいな計算で算出し、5次元の連続値の密な特徴量ベクトルに変換(各クラスタへの所属度!)
    - 5次元の密ベクトルを合計1になるように正規化する。
    - バイアス項として1を追加し、最終的に6次元の密なユーザ特徴量ベクトルに。
  - disjoint LinUCBでは、上記の6次元のユーザ特徴量ベクトルをそのまま使用する。
    - これが論文内の $x_{t,a} \in \mathbb{R}^{d}$ (d=6)$ に該当する!
- ニュース特徴量の扱い方 (hybrid LinUCBではニュース特徴量も使用する!):
  - 生の特徴量は以下:
    - URLから推定したカテゴリ情報
    - publisherがタグ付けした内容カテゴリ情報
  - 前処理:
    - まずユーザ特徴量と同じように処理して、同様に6次元の密な特徴量ベクトルを得る。
    - そこから、外積(outer product)で相互作用特徴量を作る!
      - 具体的には、ユーザ特徴量ベクトル6次元 × ニュース特徴量ベクトル6次元 = **36次元の相互作用を含んだ特徴量ベクトルを作る。**
      - これが論文内の $z_{t,a} \in \mathbb{R}^{k}$ (k=36)$ に該当する!

## 議論はある？

実験結果の概要:

- contextual-bandit系 > warm-start系 > context-free系 でrelative CTRが優れていた。
- $\epsilon$-greedyのアルゴリズム達は、適切なパラメータ(epsilon)を使用した場合に、UCBアルゴリズム達と同様のrelative CTRを達成した。
- contextual-bandit系のアルゴリズムは、ベースラインのcontext-freeな$\epsilon$-greedyと比較して、約10%のCTR lift を達成した。

## 次に読むべき論文は？

- thompson sampling系のcontextual-banditの論文を読んでみようか迷い中。

## お気持ち実装

disjoint なLinUCBの疑似コードのお気持ち実装。

```python
from collections import defaultdict
from typing import Any

import numpy as np


class LinUCBDisjoint:
    def __init__(self, alpha: float, dimension: int) -> None:
        self.alpha = alpha
        self.d = dimension
        self.D_a_by_arm = defaultdict()  # training input : D_a in R^{m * d}
        self.A_a_by_arm: dict[Any, np.ndarray] = defaultdict()  # A_a := D_{a}^T D_{a} + I_{d}
        self.b_a_by_arm: dict[Any, np.ndarray] = defaultdict()  # b_a := D_{a}^T * responce_vector(c_{a})

    def run(self, T: int) -> None:
        for t in range(1, T + 1):
            # Observe features of all arms a in A_t: x_{t,a} in R^{d}
            A_t = self._fetch_item_pool(t)
            context_a_t_of: dict[Any, np.ndarray] = self._observe_context_of_items(A_t)

            theta_a_hat_of: dict[Any, np.ndarray] = defaultdict()
            payoff_hat_of: dict[Any, float] = defaultdict()
            for a in A_t:
                if self._is_new_arm(a):
                    # initialize A_a and b_a
                    self.A_a_by_arm[a] = np.identity(self.d)
                    self.b_a_by_arm[a] = np.zeros(self.d)
                # update parameter & estimate payoff expectation
                theta_a_hat_of[a] = self.A_a_by_arm[a] ** (-1) * self.b_a_by_arm[a]
                payoff_hat_of[a] = theta_a_hat_of[a] + self.alpha * np.sqrt(
                    context_a_t_of[a].T * np.linalg.inv(self.A_a_by_arm[a]) * context_a_t_of[a]
                )

            # choose a_{t} and observe a real-valud payoff r_{t}
            a_t = self._select_arm()
            r_t = self._observe_real_valued_payoff(a_t)
            # update A_a and b_a
            self.A_a_by_arm[a_t] = self.A_a_by_arm[a_t] + context_a_t_of[a_t] * context_a_t_of[a_t].T
            self.b_a_by_arm[a_t] = self.b_a_by_arm[a_t] + r_t * context_a_t_of[a_t]

    def _fetch_item_pool(self, trial_idx: int) -> set[Any]:
        """get item pool of trial t: A_t"""
        pass

    def _observe_context_of_items(self, items: set[Any]) -> dict:
        """各a in items の x_{t,a} を観測する"""
        pass

    def _is_new_arm(self, item: Any) -> bool:
        pass

    def _select_arm(self) -> Any:
        pass

    def _observe_real_valued_payoff(self, selected_arm: Any) -> Any:
        pass
```

hybrid なLinUCBの疑似コードのお気持ち実装。

```python
from collections import defaultdict
from typing import Any

import numpy as np


class LinUCBHyblid:
    def __init__(
        self,
        alpha: float,
        disjoint_dim: int,
        hyblid_dim: int,
    ) -> None:
        self.alpha = alpha
        self.d = disjoint_dim
        self.k = hyblid_dim
        self.A_0 = np.identity(self.k)  # k * k matrix
        self.b_0 = np.zeros(self.k)  # k vector
        self.A_a_by_arm: dict[Any, np.ndarray] = defaultdict()  # A_a := D_{a}^T D_{a} + I_{d}
        self.B_a_by_arm: dict[Any, np.ndarray] = defaultdict()  #
        self.b_a_by_arm: dict[Any, np.ndarray] = defaultdict()  # b_a := D_{a}^T * responce_vector(c_{a})

    def run(self, T: int) -> None:
        for t in range(1, T + 1):
            # Observe features of all arms a in A_t: x_{t,a} in R^{d}
            A_t = self._fetch_item_pool(t)
            context_a_t_of: dict[Any, np.ndarray] = self._observe_context_of_items(A_t)
            beta_hat = np.linalg.inv(self.A_0) * self.b_0

            theta_a_hat_of: dict[Any, np.ndarray] = defaultdict()
            payoff_hat_of: dict[Any, float] = defaultdict()
            for a in A_t:
                if self._is_new_arm(a):
                    # initialize A_a and b_a
                    self.A_a_by_arm[a] = np.identity(self.d)
                    self.b_a_by_arm[a] = np.zeros(self.d)
                # update parameter & estimate payoff expectation
                theta_a_hat_of[a] = self.A_a_by_arm[a] ** (-1) * self.b_a_by_arm[a]
                payoff_hat_of[a] = theta_a_hat_of[a] + self.alpha * np.sqrt(
                    context_a_t_of[a].T * np.linalg.inv(self.A_a_by_arm[a]) * context_a_t_of[a]
                )

            # choose a_{t} and observe a real-valud payoff r_{t}
            a_t = self._select_arm()
            r_t = self._observe_real_valued_payoff(a_t)
            # update A_a and b_a
            self.A_a_by_arm[a_t] = self.A_a_by_arm[a_t] + context_a_t_of[a_t] * context_a_t_of[a_t].T
            self.b_a_by_arm[a_t] = self.b_a_by_arm[a_t] + r_t * context_a_t_of[a_t]

    def _fetch_item_pool(self, trial_idx: int) -> set[Any]:
        """get item pool of trial t: A_t"""
        pass

    def _observe_context_of_items(self, items: set[Any]) -> dict:
        """各a in items の x_{t,a} を観測する"""
        pass

    def _is_new_arm(self, item: Any) -> bool:
        pass

    def _select_arm(self) -> Any:
        pass

    def _observe_real_valued_payoff(self, selected_arm: Any) -> Any:
        pass
```

疑似コードのお気持ち実装。(やってる事はnaiveなOPEに近い。)

```python
from typing import Any


class Policy:
    def select(self, prev_histories: list, contexts: Any) -> Any:
        pass


def off_policy_evaluation(
    T: int,
    target_policy: Policy,
    logged_events: list[dict],
):
    history_t_of = {0: []}  # initially empty history
    total_payoff_of = {0: 0}  # R_0 = initially zero total payoff
    for t in range(1, T + 1):
        # logged eventsを一つずつ見ていく
        for event in logged_events:
            # event := (x_1, ..., x_K, a, r_a)
            if target_policy(history_t_of[t - 1], event["contexts"]) != event["a"]:
                continue
            # もし現在のhistory h_{t-1} と contexts_{t} が与えられた上でtarget policyがlogging policyと同じ腕を選択する場合、
            # そのイベントはsupport(保持)される。 (i.e. historyと総報酬が更新される。)
            # (まさにnaiveなOPE!!)
            history_t_of[t] = history_t_of[t - 1] + [event]
            total_payoff_of[t] = total_payoff_of[t - 1] + event["r_a"]
            break

    return total_payoff_of[T] / T
```
