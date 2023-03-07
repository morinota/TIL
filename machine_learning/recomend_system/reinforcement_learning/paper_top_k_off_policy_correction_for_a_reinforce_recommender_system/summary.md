# Top-K Off-Policy Correction for a REINFORCE Recommender System

published date: hogehoge September 2019,
authors: Chen
url(paper): https://arxiv.org/abs/1812.02353
(勉強会発表者: morinota)

---

## どんなもの?

- 推薦システムにおいては、膨大な量のimplicit feedback(ex. ユーザのクリック数、滞在時間など)が学習用に利用できる.
- しかし、ログに記録されたfeedbackからの学習は、現在運用している推薦システムによって選択された推薦アイテムリストに対するfeedback のみ を観測することによって引き起こされるbiasに左右される.
- 本論文では、REINFORCEアルゴリズム[48]を、非常に大きなaction space と state space を持つneural candidate generator(top-K推薦システム)に適応させた経験を紹介する.
  - REINFORCEアルゴリズム[48]:
    - 強化学習の一種であるpolicy勾配法の中で、最も基本的なアプローチ.
    - policy勾配法 = agentのpolicy(行動選択戦略)を直接最適化することで、最適な行動を選択するようにagentを訓練する方法.

## 先行研究と比べて何がすごい？

## 技術や手法の肝は？

### 問題設定

まず、本論文における推薦システムの構成と、RLに基づく推薦のアプローチについて説明する.

**推薦システムとユーザとの過去のInteraction**(=推薦システムがある動画アイテムをオススメして、それに対してユーザがどのようなreactionを示したか!)の **sequence(順序)**を考慮する.
(ex. 各ユーザについて、推薦システムが行ったaction(i.e. 推薦するアイテム)、および、クリックや視聴時間などのuser feedbackを記録したデータ.)

このような一連の動作が与えられると、クリック数や視聴時間などのユーザ満足度の指標を向上させるような、次にとるべきaction(i.e.推薦する動画アイテム)を予測する.

この設定を 以下のようなマルコフ決定過程(Markov Decision Process, MDP)$(S, A, P, R, \rho_0,\gamma)$に置き換える:

- $S$: ユーザーの状態を記述するcontinuous(連続的)なstate space.
- $A$: 推薦可能なアイテムを含む、discrete(離散的)な action space.(i.e. 推薦アイテムの選択肢=候補?)
- $P$: $S \times A \times S \rightarrow \mathbb{R}$ は state transition probability(状態遷移確率).
  - agentのactionを受けてstateが変化する時の**確率分布**.
  - (stateはcontinuous valueだから、たぶん確率密度関数)
  - $p(s', r|s, a) = P(S_{t+1}=s', R_{t+1}=r|S_t=s, A_t=a)$
- $R$: $S \times A \rightarrow \mathbb{R}$ は reward function(報酬関数).
  - ex) $r(s, a)$はユーザのstate $s$においてaction $a$ を行うことによって得られる immediate reward(即時報酬)である.
  - 下の期待累積報酬を最大化する数式を見た感じでは、$R$はcumulative rewardを返すような関数? 一方で小文字$r$はimmediate rewardを返すような関数.
- $\rho_0$: initial state distribution(初期状態分布).
- $\gamma$: 将来の報酬に対するdiscount factor(割引係数).

そして推薦システムが得る**expected cumulative reward(期待累積報酬)を最大化するような**, policy $\pi(a|s)$ を模索する.
(policy $\pi(a|s)$は、ユーザのstate $s \in S$を条件づけた上で推薦アイテム $a \in A$ を選択する確率(確率質量)を返すような 確率分布関数.)

$$
\max_{\pi} J(\pi) = E_{\tau \sim \pi}[R(\tau)],
\\
\text{where } R(\tau) = \sum_{t=0}^{|\tau|} r(s_t, a_t)
$$

ここで、上式における期待値は、policy に従って action した事で得られる**trajectories(軌跡 = stateとactionの結果)**$\tau = (s_0, a_0, s_1, \cdots)$ を入力として計算される.

よって上式の$J(\pi)$を書き換えると、以下のようになる.

$$
J(\pi) = E_{s_0 \sim \rho_0, a_t \sin \pi(\cdot|s_t), s_{t+1} \sim P(\cdot|s_t, a_t)}[\sum_{t=0}^{|\tau|} r(s_t, a_t)]
\\
= E_{s_t \sim d_t^{\pi}(\cdot), a_t \sin \pi(\cdot|s_t)}[\sum_{t'= t}^{|\tau|} r(s_{t'}, a_{t'})]
\tag{1}
$$

ここで、

- 式(1)の一段目に関して.
  - 初期状態 $s_0$ は、 initial state distributionに基づき生成される.
  - 時間tにおけるaction $a_t$ は、時間tにおけるstate $s_t$で条件づけた(=入力とした)policy関数に基づき生成される.
  - 時間t+1における state $s_{t+1}$ は、$a_t$ と $s_t$ で条件づけた(=入力とした)state transaction probability関数 $P$ に基づいて生成される.
- 式(1)の二段目に関して.
  - $d_t^{\pi}(\cdot)$ は、policy $\pi$ の下で時間tにおける (discounted) **state visitation frequency(状態訪問頻度)**を意味する.
    - state visitation frequency(状態訪問頻度): agentが学習中にどのstateにどの程度の頻度でvisitしたかを示す指標.
    - reward functionの推定に役立つらしい.

このような RL 問題を解くために、様々な手法が利用可能である.(なるほど...**期待累積報酬を最大化するようなpolicy関数を探索する事**がRLの基本的なタスクなのかな...!)
本論文では、policy-gradientに基づくアプローチ、すなわち、REINFORCE [48]を適用する.

### REINFORCE

policy $\pi_{\theta}$ は $\theta \in \mathbb{R}^{d}$ でパラメータ化された関数形式を仮定する. (dはパラメータ数. $\theta$ はパラメータベクトル.)
**policy関数のパラメータに対する期待累積報酬(expected cumulative reward)の勾配**は，"log-trick(??)"によって解析的(なるほど!じゃあ普通に解いたら得られる?)に導かれ，以下のREINFORCE gradientを得ることができる.

$$
\nabla_{\theta} J(\pi_{\theta}) =
E_{s_t \sim d_t^{\pi}(\cdot), a_t \sin \pi(\cdot|s_t)}
[(\sum_{t'= t}^{|\tau|} r(s_{t'}, a_{t'})) \nabla_{\theta} \log{\pi_{\theta}(a_t|s_t)}]
\\
= \sum_{s_t \sim d_t^{\pi}(\cdot), a_t \sin \pi(\cdot|s_t)}
R_{t}(s_t, a_t) \nabla_{\theta} \log \pi_{\theta}(a_t|s_t)
\tag{2}
$$

ここで、 $R_{t}(s_t, a_t)= \sum_{t'=t}^{|\tau|} r(s_{t'}, a_{t'})$ は時刻tにおけるactionに対する割引後の将来報酬(時刻t以降に獲得する報酬の合計の予測値??discountって何?)である.

### Off-Policy 補正

通常の強化学習とは異なり、本論文の学習器は、学習とインフラの制約から、推薦システムをリアルタイムにインタラクティブに制御することができない.
(i.e.学習器はオンラインでpolicyを更新し、更新されたpolicyに従った軌跡を即座に生成できない.)
その代わりに、更新対象のpolicyとは異なるaction space上の分布を持ちうる過去のpolicy(=現在運用中の推薦モデル?)により選択されたactionのログfeedbackを受け取る.
(=**新バージョンのpolicyを本番に導入する前に、現在運用中のモデルから得られるfeedbackを使って学習させる必要がある**...!)

本論文では、この設定のもとでpolicy-gradientアプローチを適用する際に生じるデータのbiasを解決することに焦点を当てる.
式(2)のgradientは更新対象のpolicy $\pi_{\theta}$ から軌道をサンプリングする事を想定している.
しかし、今回の問題設定にて収集した軌道は過去のpolicy $\beta$ からサンプリングされるため，単純な policy-gradient の推定器は不偏ではなくなる.
(なるほど...!**強化学習したいpolicyそのものを本番運用しているケース**では、受け取ったfeedback=軌道を用いてほぼ正しい勾配(不偏推定量=平均的に真の勾配と等しいみたいなイメージ)を計算可能で、結果として期待累積報酬を最大にするようなpolicyに更新=強化していけるはず.)
(しかし、強**化学習したいpolicyとは別のpolicyを本番運用しているケース**では、受け取ったfeedback=軌道を式(2)に当てはめて計算しても見当違いな勾配になってしまう. 結果として変な方向にpolicyを更新していってしまう...!)

分布の不一致には、**importance weighting(重要度重み付け)**[31, 33, 34]を用いて対処する.
behavior policy(現在運用中の方策?) $\beta$ に従ってサンプリングされた軌道 $\tau = (s0, a0, s1, \cdots)$ を考慮すると、off-policy-corrected gradient estimator(off-policy補正勾配推定器)は、次のようになる:

$$
\nabla_{\theta} J(\pi_{\theta})
= \sum_{s_t \sim d_t^{\beta}(\cdot), a_t \sin \beta(\cdot|s_t)}
w(s_t, a_t) R_{t}(s_t, a_t) \nabla_{\theta} \log \pi_{\theta}(a_t|s_t)
\tag{3}
$$

ここで、以下は重要度重みである.

$$
w(s_t, a_t)
= \frac{d_t^{\pi}(s_t)}{d_t^{\beta}(s_t)}
\times \frac{\pi_{\theta}(a_t|s_t)}{\beta(a_t|s_t)}
\times \Pi_{t'=t+1}^{|\tau|} \frac{\pi_{\theta}(a_{t'}|s_{t'})}{\beta(a_{t'}|s_{t'})}
$$

この補正により、別のpolicy $\beta$ に従ってサンプリングされたactionでtrajectories(軌道)が収集された場合は、常に不偏の推定値が得られる(ほう,
言うね...!).
しかし、更新対象のpolicy $\pi$ と 別のpolicy $\beta$ の違いが大きい(=>重要度重みが非常に小さくor大きくなる)場合には、**推定値の分散が大きくなる**可能性がある.(それでも不偏性は失われないのか...)

各勾配項の分散を小さくするために，1次近似(?)を行い，将来の軌道の重要度重みとして2つのpolicy下のstate visitationの差分を無視することで，分散を小さくしたpolicy-gradientのやや偏った(=不偏性は失われた)推定値を得ることができた．

$$
\nabla_{\theta} J(\pi_{\theta})
\approx \sum_{s_t \sim d_t^{\beta}(\cdot), a_t \sin \beta(\cdot|s_t)}
\frac{\pi_{\theta}(a_t|s_t)}{\beta(a_t|s_t)} % 重みがraughになった?
R_{t}(s_t, a_t) \nabla_{\theta} \log \pi_{\theta}(a_t|s_t)
\tag{4}
$$

この推定器は、正確なoff-policy補正の分散をトレードオフしつつ、非補正のpolicy-gradientの大きなバイアスを補正し、on-policy学習により適したものである.(いいとこ取り的なestimatorなのか...)

### policy関数 $\pi_{\theta}$ の設定

各時間 t におけるユーザのstateに関するpolicyをモデル化し、$s_t \in \mathbb{R}^n$(n次元ベクトル)を入力として、ユーザが興味を持つaction(dのアイテムを見せるか)を予測する.
軌跡(trajectory)に沿った各時刻$t$で取られた action は, $u_{a_t} \in \mathbb{R}^n$ を用いて埋め込まれている.
state transition(状態遷移)関数 $P$ : S×A×S を recurrent neural network でモデル化する:

$$
s_{t+1} = f(s_t, u_{a_t})
$$

本論文では、LSTM（Long Short-Term Memory) やGRU（Gated Recurrent Units）などの有名なRNNセルをいろいろと実験した結果、安定性と計算効率の点から、Chaos Free RNN(CFN)という簡易セルを使うことにした.
stateは、以下のように**再帰的(recursively)**に更新される.

$$
s_{t+1} =  f(s_t, u_{a_t}) = z_t \odot \tanh(s_t) + i_t \odot \tanh(W_{a}u_{a_t})
\\
z_t = \sigma(U_{z}s_{t} + W_{z}u_{a_t} + b_{z})
\\
i_t = \sigma(U_{i}s_{t} + W_{i}u_{a_t} + b_{i})
\\
\tag{5}
$$

ここで、 $z_t, i_t \in \mathbb{R}^n$ はそれぞれ update gate と input gate である.

ユーザのstate $s$ を条件として、policy $\pi_{\theta}(a|s)$は、**単純な softmax** でモデル化される.

$$
\pi_{\theta}(a|s) = \frac{\exp(s^T v_{a} / T)}{\sum_{a'\in A} \exp(s^T v_{a'}/T)}
\tag{6}
$$

ここで、

- $v_a \in \mathbb{R}^{n}$ は action space $A$ における各action $a$ の別の埋め込みベクトル(actionの埋め込みベクトルが二種類ある?)
- $T$ は通常 1 に設定される temperature である.
  - $T$ の値を大きくすることで、action space 上でより滑らか(=確率分布の傾斜が...!)なpolicyが実現される.

softmax の正規化項はすべての可能な action (=アイテム)を調べる必要があり、**推薦システムの設定では数百万のオーダー(=アイテム数)**となる.
この計算を高速化するために、本論文は学習時に sampled softmax[4]を実行している.
この時、効率的な最近傍探索アルゴリズムを用いて**上位のactionを取得し、これらのactionのみを用いてsoftmax確率を近似する**

まとめると、policy $\pi_{\theta}$ のパラメータ $\theta$ は、二種類の action 埋め込み $U \in \mathbb{R}^{m \times |A|}$ と $V \in \mathbb{R}^{n \times |A|}$ を 含んでいる.
また、重み行列 $U_z, U_i \in \mathbb{R}^{n \times n}$ と $W_u, W_i, W_a in \mathbb{R}^{n \times m}$ 及びバイアス項 $b_{u}, b_{i} \in \mathbb{R}^{n}$ を含んでいる.

図1は、policy関数 $\pi_{\theta}$ のneural architecture を説明する図.

![](https://camo.qiitausercontent.com/954f2c9e5dc4b35d672e8ceb543056e715acbcbf/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f36356338313937382d396638302d656665622d343434322d3030373030353364646365362e706e67)

policy $\beta$ からサンプリングされた観測されたtrajectory(軌道) $\tau = (s_0, a_0, s_1, \cdots)$ が与えられると、新しいpolicyはまずitinial state $s_0 \sim \rho_{0}$ で開始し、式(5) のように recurrent セルを反復して user state $s_{t+1}$ のモデルを生成する.
user state $s_{𝑡+1}$が与えられると，policy head(policyの先端?)は式(6)のようにsoftmaxを用いて **action space に分布(=確率質量分布)を投影する**．
$\pi_{\theta}(a_{t+1}|s_{t+1})$ が与えられFる事で、式(4) のように policy-gradient を生成し、policy を更新することができる(i.e. 期待累積報酬を最大化するようなpolicyに近づける事ができる...!).

### behavior policy (の確率分布) の推定

式(4)のoff-policy補正推定量を考える上で難しいのは、behavior policy(=現在運用中のpolicy?) $\beta$ を得ることである.
理想的には、**選択された action のフィードバックを記録するごとに、そのactionを選択するbehavior policy の確率(=policy関数の出力値, 確率分布の形?)も記録したいところ**である.

しかし、behavior policyの分布を直接ログに記録することは、本論文の問題設定では実現可能ではない.

本論文では、**記録された action を使用して、behavior policy $\beta$ の値を推定する**手法を採用している.
記録されたフィードバック $D = {(s_i, a_i), i = 1, \cdots N}$ のセットが与えられたとき、Strehlら[39]はコーパス全体のaction頻度を集約して user state に依存しない $\hat{\beta}_{\theta}$ を推定している.

これに対し、我々はcontextに依存(?)したニューラル推定を採用する.
収集した各state-actionペア $(s, a)$ について、aでパラメタライズされた別のsoftmaxを用いて、behavior policy がその action を選択する確率 $\hat{\beta_{\theta'}}(a|s)$ を推定する.
図1に示したmain policy のRNNモデルから生成された user state $s$ を**再利用**し、別のソフトマックス層で behavior policy をモデル化する.
(behavior head(=actionの最後尾?)が main policy のuser state に干渉するのを防ぐため、その勾配がRNNに逆流するのをブロックしている.)

2つのpolicy head($\pi_{\theta}$ と $\beta_{\theta'}$)の間でパラメータがかなり共有されているにもかかわらず、両者の間には2つの顕著な違いがある.

- (1) main policy(=更新したいpolicy??) $\pi_{\theta}$ が長期的な報酬を考慮した重み付きソフトマックスを効果的に用いて学習されるのに対し、behavior policy(=今運用されてるpolicy?) $\beta_{\theta'}$ はstate-actionペアのみを用いて学習される.
- (2) main policy head $\pi_{\theta}$ が軌道上の非ゼロ報酬のitemのみを用いて学習するのに対し、behavior policy $\beta_{\theta'}$ は軌道上の全てのitemを用いて学習し、$\beta$ の推定値に偏りが生じないようにする.

### Off-policy補正を top-Kアイテム推薦に応用する.

本論文の設定におけるもう一つの課題は、私たちの推薦システムが**一度にK個のアイテムをユーザに推薦すること**である.
i.e. policy $\Pi_{\theta}(A|s)$ を作る必要がある.(ここで各action $A$ は、"期待累積報酬を最大化するような**k個のアイテムのセット**")

$$
\max_{\theta} J(\Pi_{\theta}) E_{s_t \sim d_t^{\Pi}(\cdot), A_t \sim \Pi_{\theta}(\cdot|s_t)}[R_t(s_t, A_t)]
$$

ここで、$R_t(s_t, A_t)$ は、state $s_t$ におけるaction集合 $A_t$ の累積報酬を示す.
残念ながら、**この集合推薦の定式化ではaction space が指数関数的に増大**し、選択するアイテムの数が数百万のオーダーであることを考えると、法外に大きい. (action space は $nC_{K}$ 通り)

問題を扱いやすくするために、我々は、ユーザが返された集合 $A$ から最大1つのアイテムと interaction することを仮定する.
言い換えれば、"**$A$ の中でゼロでない累積報酬を持つアイテムは、せいぜい1つであろう**"という仮定をおく.
さらに，あるアイテムの期待リターンは，集合$A$の中で選ばれた他のアイテムとは独立であると仮定する．
これら二つの仮定により、集合問題は次のように縮小できる.

$$
J(\Pi_{\theta}) E_{s_t \sim d_t^{\Pi}(\cdot), a_t \in A_t \sim \Pi_{\theta}(\cdot|s_t)}[R_t(s_t, a_t)]
$$

ここで、

- $R_t(s_t, a_t)$ : ユーザがinteractionしたアイテム$at$の累積リターン、
- $a_t \in A_t \sim \Pi_{\theta}(\cdot|s_t)$ : set policy によって $a_t$ が選択されたことを表す.

さらに、式（6）で記述したソフトマックスポリシー $\pi_{\theta}$ に従って各アイテム $a$ を独立にサンプリングしてセットアクション$A$を生成し、重複を解除するという制約を設けている.
その結果、アイテム $a$ が最終的な非反復集合$A$に現れる確率は、単純に $\alpha_{\theta}(a|s) = 1 - (1 - \pi_{\theta}(a|s))^K$になる($K$はサンプリング回数).

そこで、REINFORCEアルゴリズムを集合推薦の設定に適応させるには、式（2）の勾配更新を次のように変更するだけでよい.

$$
\sum_{s_t \sim d_t^{\pi}(\cdot), a_t \sim \alpha_{\theta}(\cdot|s_t)} R_t(s_t, a_t) \nabla_{\theta} \log \alpha_{\theta}(a_t|s_t)
$$

したがって、式(4)の $\pi_{\theta}$ を $\alpha_{\theta}$ に置き換えてoff-policy補正勾配を更新すれば、**top-K off-policy補正係数**が得られる.

$$
\sum_{s_t \sim d_{t}^{\pi}(\cdot), a_t \sim \beta(\cdot|s_t)}
[\frac{\alpha_{\theta}(a_t|s_t)}{\beta_{\theta}(a_t|s_t)}
R_{t}(s_t, a_t)
\nabla_{\theta} \log \alpha_{\theta}(a_t|s_t)]
\\
= \sum_{s_t \sim d_{t}^{\pi}(\cdot), a_t \sim \beta(\cdot|s_t)}
[\frac{\pi_{\theta}(a_t|s_t)}{\beta_{\theta}(a_t|s_t)}
\frac{\partial \alpha_{\theta}(a_t|s_t)}{\partial \pi(a_t|s_t)}
R_{t}(s_t, a_t)
\nabla_{\theta} \log \pi_{\theta}(a_t|s_t)]
\tag{7}
$$

式（7）と式（4）を比較すると、top-K policy は、元の off-policy補正係数 $\frac{\pi_{\theta}(a_t|s_t)}{\beta_{\theta}(a_t|s_t)}$ に次の乗数(multiplier)を追加している.

$$
\lambda_{K}(s_t, a_t) = \frac{\partial \alpha_{\theta}(a_t|s_t)}{\partial \pi(a_t|s_t)}
= K(1 - \pi_{\theta}(a_t|s_t))^{K-1}
\tag{8}
$$

追加された乗数に関して:

- $\pi_{\theta}(a_t|s_t) -> 0$ 即ち $\lambda_{K}(s_t, a_t) -> K$ の場合、top-K off-policy補正は標準のoff-policy補正と比較して、policyの更新をK倍に増加させる.
- $\pi_{\theta}(a_t|s_t) -> 1$ 即ち $\lambda_{K}(s_t, a_t) -> 0$ の場合、この乗数はpolicyの更新をゼロにする.
- Kが大きい場合、この乗数は、$\pi_{\theta}(a_t|s_t)$ が合理的な範囲に達すると、より速く勾配(policy-gradient)をゼロにすることができる.(ゼロになったら更新が停止する.これって良いことなんだっけ?)

要約すると、ソフトマックス policy (関数) $\pi_{\theta}(a_t|s_t)$ においてdesirable item(望ましい?)の質量(=確率質量?)が小さい場合、**top-K補正係数は、標準の補正係数よりも積極的にその尤度(確率質量)を押し上げる**.
ソフトマックス policy $\pi_{\theta}(a_t|s_t)$ がdesirable itemに適度な質量(確率質量)を与えると(top-K に登場する可能性を確保するため)、補正係数は勾配をゼロにして尤度(=確率質量)を押し上げようとはしなくなる.

標準的なoff-policy補正は1つのアイテムを選択する際に最適なpolicyに収束するが、**top-K補正はtop-K推薦 を向上させることにつながる**. (シミュレーションと実環境での実験により検証している.)

### policy-gradient推定の分散を低減するテクニック

冒頭で詳述したように、policy-gradientの推定値の分散を減らすために一次近似(=１次関数で近似)を行う.
にもかかわらず、勾配は、top-K off-policy補正と同様に、式(4)に示すように、 $w(s,a) = \frac{\pi(a|s)}{\beta(a|s)}$ の**大きな重要度重みによって大きな分散に苦しむことがある**.
大きな重要度重みは、以下の２つの要因から発生しうる.

- (1)更新したい policy $\pi(\cdot|s)$ と behavior policy $\beta$ とで大きな乖離があるケース.
  - 特に、new policy が behavior policy によってあまり探索されない領域(=$\pi(a|s) >> \beta(a|s)$ となるようなaction space)を探索することに起因すると考えられる.
- (2) $\beta$ 推定値の分散が大きいケース.

本論文では、**勾配(policy-gradient)推定の分散を制御するため**に、反実仮想学習やRLの文献で提案されているいくつかの手法を検証した.
これらの手法のほとんどは、勾配推定値に何らかのバイアスをもたらす代償として、分散を減少させる.(=不偏推定量ではなくなるが、分散が減少するような手法)

#### Weight Capping.

importance weighet を単純に cap(=大きさに上限を設ける?)するアプローチ.

$$
\bar{w}_{c}(s,a) = \min(\frac{\pi(a|s)}{\beta(a|s)}, c)
\tag{9}
$$

$c$ の値を小さくすると、勾配推定の分散は小さくなるが、バイアスが大きくなる.

#### Normalized Importance Sampling (NIS). 正規化重要度サンプリング

第二の手法は、**ratio control variate(比率制御変数)**を導入すること.
ここで、classical weight normalizationを用いて、次のように定義する.

$$
\bar{w}_{n}(s,a) = \frac{w(s,a)}{\sum_{(s', a') \sim \beta} w(s', a')}
$$

### Exploration(探索)について

良いpolicyを学習するためには学習データの分布が重要である.
既存の推薦システムでほとんど行われない action を問い合わせる探索方針は広く研究されている.
しかし，**YouTube のようなシステムにおいて，𝜖-greedyに探索を行うことは，不適切な推薦やユーザ体験の低下を招く可能性があり，現実的でない**と考えられる.

我々は、最も確率の高い K アイテムを選ぶ(=確定的)のではなく、**$\pi$ から推薦をサンプリングする確率的なpolicyを使用すること**を検討する.
これは、**完全なソフトマックスを計算する必要がある(選択肢が多すぎる)**ため、計算効率が悪いという課題があり、action spaceを考慮すると法外なコストがかかる.
その代わりに、効率的な**近似最近傍システムを利用し、ソフトマックスの上位 M アイテムを検索**する.
次に、これらの **M アイテムの対数をより小さなソフトマックスに送り込み、確率を正規化し、この分布からサンプリング**する.
$M >> K$とすることで、確率の塊のほとんどを取り出すことができ、悪い推薦のリスクを制限し、計算効率の良いサンプリングを可能にする.
実際には、最も確率の高い上位 K' アイテムを返し、残りの $M - K'$ アイテムから $K - K'$ アイテムを抽出することで、探索と抽出のバランスをさらに取る.(**なるほど...! Kアイテムのうち、K'個は確定的に選び、K-K'個は確率的に選ぶ!**)

## どうやって有効だと検証した?

オフライン環境でのシミュレーション実験と、オンライン環境でのA/Bテストで、提案したアプローチの有効性を検証した.

### オフライン環境でのシミュレーション実験

off-policy補正のアイデアを明らかにするために、シミュレーション実験をおこなった.
シミュレーションを簡単にするために、我々は問題が stateless であると仮定する. 言い換えれば、**報酬 $R$ はユーザの状態(state)から独立しており、行動(action)はユーザの状態(state)も変えない**.

#### Off-policy 補正に関する実験.

最初のシミュレーションでは、アイテムが10個あると仮定し、すなわち $A = {a_i, i = 1,\cdots, 10}$ とする.
それぞれの報酬はそのインデックスに等しく、つまり $r(a_i) = i$.
一つのアイテムを選ぶとき、この設定の下での最適な方策(policy)は、最も多くの報酬を与えるので、常に i = 10 のアイテムを選ぶこと、である.

$$
\pi^*(a_i) = I(i = 10) % i=10の確率質量が1.0
$$

statelessなソフトマックスを用いて $\pi_{\theta}$ をパラメータ化すると以下.

$$
\pi(a_i) = \frac{e^{\theta_i}}{\sum_{j} e^{\theta_j}}
$$

あるbehavior policy $\beta$ からサンプリングされた観測値が与えられたとき，式(2)のようにデータの偏りを考慮せずに素朴にpolicy-gradientを適用すると，policyは以下のように収束する.

$$
\pi(a_i) = \frac{r(a_i) \beta(a_i)}{\sum_{j} r(a_j) \beta(a_j)}
$$

これには明らかな欠点がある. behavior policy $\beta$ が最適でないアイテムを選べば選ぶほど、新しいpolicy $\pi$ は同じアイテムを選ぶ方向に偏ってしまう.

図2は，behavior policy $\beta$ が 報酬の最も少ないアイテムを優先的に選択するような偏った場合において、SGD[7]を用いてオフポリシー補正 あり/なしで 学習したpolicy $\pi_{\theta}$ を比較したものである.

![](https://camo.qiitausercontent.com/b98629aa2b465f77dd9a6ccbe141bdc71860f541/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f30343334633138662d353362652d663462322d666633352d6166396161323930346264642e706e67)

図2（左）に示すように，データの偏りを考慮せずに素朴にpolicy-gradientを適用すると，最適とは言えない方策になる.(最適なのはi=10のアイテムを常に選ぶべき!)
最悪の場合、**behavior policy が常に報酬の最も少ないactionを選択する場合**、任意に貧弱なbehavior policy を模倣したpolicyになってしまう(つまり、報酬の最も少ないアイテムを選択するように収束してしまう...!).
一方、off-policy補正を適用すると、図2（右）のように、**データの収集方法に関わらず、最適なpolicy $\pi^*$ に収束させることができる**.

#### Top-K off-policy 補正の効果の実験

標準的なオフポリシー補正と提案された top-K オフポリシー補正の違いを理解するために、複数のアイテムを推薦できる別のシミュレーションを設計した.

- ここでも10個のアイテムがあり、$r(a_1) = 10$、$r(a_2) = 9$ 、残りのアイテムは報酬がかなり低い $r(a_i) = 1. \forall i = 3, \cdots 10$ とする.
- ここでは2個のアイテム、つまり $K = 2$ の推薦に焦点を合わせる.
- behavior policy関数 $\beta$ は一様分布に従う、つまり、各アイテムを等しい確率で選択する.

$\beta$ からサンプリングされた観測値$(a_i, r_i)$が与えられると、標準オフポリシー補正は以下の形式のSGD更新式を持つ.

$$
\theta_{j} = \theta_{j} + \eta \frac{\pi_{\theta}(a_j)}{\beta(a_j)} r(a_i)[I(j=i) - \pi_{\theta}(a_j)],
\forall j = 1, \cdots , 10
$$

ここで、$\eta$ は学習率である.
SGDは $\pi_{\theta}(a_i) = 1$ まで、$\pi_{\theta}$ の下で期待報酬に比例してアイテム $a_i$ の尤度(=確率質量)を上げ続け、その下で勾配は0になる.

一方、top-K off-policy 補正の場合、以下の形の更新式になる.

$$
\theta_{j} = \theta_{j} + \eta \lambda_{K}(a_j) \frac{\pi_{\theta}(a_j)}{\beta(a_j)}
r(a_i)[I(j=i) - \pi_{\theta}(a_j)],
\forall j = 1, \cdots , 10
$$

ここで、$\lambda_K(a_i)$ は 4.3 節で定義された追加の乗数である.
$\pi_{\theta}(a_i)$ が小さいときは、$\lambda_K(a_i) \simcolon K$ となり、SGD はより積極的にアイテム $a_i$ の可能性を増加させる.
$\pi_{\theta}(a_i)$ が十分に大きな値になると、$\lambda_K(a_i)$ は 0 になり、その結果、$\pi_{\theta}(a_i)$ がまだ 1 以下でも SGD はこのアイテムの尤度(=確率質量)を無理に上げなくなる. その代わりに学習した方針において、二番手のアイテムがある程度の量を占めれるようにすることができた.

図3は、標準的なオフポリシー補正(左)とtop-K Off-policy補正(右)で学習された方策 $\pi_{\theta}$ を示す.

![](https://camo.qiitausercontent.com/cd1c6598e667589ee90cf9315f8b80b006f2b1df/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f36323134636337612d333931392d376534352d333164622d3762346665363833646265342e706e67)

標準的なoff-policy補正では，**学習されたpolicyは期待報酬に対するアイテムの順序を維持**するという意味で較正[23]されているが，**トップ1のアイテムにほぼ全量を投じる方策**，すなわち，$\pi_{\theta}(a_1) \simcolon 1.0$ に収束していることが分かる.
その結果，学習されたpolicyは，わずかに最適でないアイテム (この例では $a_2$) と残りのアイテムとの間の差を見失う.
一方、**top-Kの補正は、アイテム間の最適性の順序を維持したまま、2番目に最適なアイテムに大きな質量(=確率質量)を持つ方策に収束させる**.

### オンライン環境でのA/Bテスト

新しい手法の効果を理解するためのシミュレーション実験は重要だが、**あらゆる推薦システムの目標は、最終的には実際のユーザ体験を向上させること**である.
そこで、これらのアプローチの効果を測定するために、実プロダクト環境でA/Bテストを実施した.

即時報酬 $r$ はさまざまなユーザの活動を反映するように設計されており、**推薦されてもクリックされないビデオはゼロ報酬を受け取る**.
長期報酬 $R$ は4-10時間の時間軸で集計される.
各実験において、コントロールモデルとテストモデルは同じ報酬関数(reward function)を使用する.

オンライン実験では推薦システムの様々な Online Metrics を見るが、ここでは、**ユーザがビデオを見るのに費やした時間(ViewTimeと呼ばれる)**に焦点をあてて議論する.

#### Eploration(探索)の効果に関する実験

まず，モデルの品質を向上させるための探索的なデータ の価値を理解することから始める.
特に, **ソフトマックスモデルからサンプリングする確率的な方策**が，ソフトマックスに従って常に最も高い確率で K個のアイテムを推薦する**決定論的な方策より良い推薦 をもたらすかどうか**を測定したい.

この実験では，control集団には決定論的な方策を適用し，test trafficの小片(=介入群, test集団)にはセクション 5 で述べたような確率論的な方策を適用した.
両policyとも**同じソフトマックスモデルにもとづくもの**である.
また，確率論的方策のrandomness量を制御するために，式(6)で使用するtemperatureを変化させた.
$T$が低いと確率論的policyが決定論的方策に近づき，$T$ が高いと任意のアイテムを等しい確率で推薦するランダム方策になる.
実験の結果、$T$を1に設定した場合には実験中に ViewTime に統計的に有意な変化は観察されず，これは**サンプリングによって生じるランダム性の量が直接ユーザ経験を損なわないこと**を示している.

しかし、この実験設定では、**学習中に探索的なデータを利用できることの利点が考慮されていない**.
ログデータからの学習における主なバイアスの1つは、**モデルが前回の推薦方針で選択されなかった行動(action)のフィードバックを観測しないこと**であり、探索データはこの問題を軽減する.
そこで、探索データを学習に導入する追試を行った.
そのために、プラットフォーム上のユーザーを90％、5％、5％の3つのバケットに分割した.
最初の2つのバケットには決定論的なモデルに基づく決定論的な方策でサービスを提供し、最後のバケットのユーザーには探索的なデータで学習したモデルに基づく確率論的な方策でサービスを提供する.
決定論的モデルは、最初の2つのバケットで取得したデータのみを使用して訓練され、確率論的モデルは、最初と3番目のバケットのデータで訓練される.
その結果、これら**2つのモデルは同じ量の学習データを受け取る**が、確率論的モデルは探索のため、いくつかの稀な状態(state)と行動(action)のペアの結果を観察する可能性が高くなる.

この実験手順に従うと、テスト母集団において、ViewTime が 0.07% と統計的に有意に増加することが確認された.(探索的データを使った方がより良い結果になったって事??)

#### Off-Policy 補正の効果を測る

確率論的方策に続いて、トレーニング中にoff-policy補正を組み込むことをテストした.
ここでは、より伝統的なA/Bテストの設定に従って、2つのモデルを訓練する.
testモデルは図 1 の構造に従っており，モデルは serving policy $\pi$ と behavior plicy $\beta$ の両方を学習する.
このとき、各例は報酬だけでなく、データの偏りに対処するための重要度重み $\frac{\pi}{\beta}$ も加味されるため、式（4）で表されるオフポリシー補正を用いて、serving policy が学習される.

![](https://camo.qiitausercontent.com/6f77a7301ba378a68f416a17e000119348e27592/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f65653362393236392d633664612d393034392d653730662d6432323965653334653939382e706e67)

実験中に，学習されたポリシー(test)(=$\pi$?)がトラフィックを獲得するためのbehavior policy(control)(=$\beta$?) から乖離し始めることが観察された.
図4は、control母集団における動画のランクに応じて、**controlとtestでノミネータが選択した動画(=アイテム)のCDF(=累積密度関数?)をプロットしたもの**である(ランク1はcontrolモデルによって最もノミネートが多い動画、右端は最もノミネートが少ない動画である).
データ収集に用いたモデル(青色で表示)を模倣するのではなく、testモデル(緑色で表示)はcontrolモデルであまり探索されていない動画を優先していることがわかる.(**i.e. 推薦のDiversityが広がっているイメージ?**)
実験では、上位ランク以外の動画からのノミネートの割合が、ほぼ1/3に増加することが観察された.
これは、図2に示したシミュレーションで観察されたものと一致している.
データ収集過程でのbiasを無視する場合、**behavior policyで多くノミネートされたからといって学習policyでノミネートされるという「金持ちがより金持ちになる」現象が生じる**が，off-policy補正を組み込むことでこの効果を低減することができる.

興味深いことに、ライブ実験では、control集団とtest集団の間で、ViewTime の統計的に有意な変化は観察されなかった.
しかし、**動画の視聴回数が0.53%増加し、統計的に有意であったことから、ユーザがより楽しめていることが伺えた**.

#### Top-K Off-Policy補正の効果について

「top-K off-policyアプローチが、標準的なoff-policyアプローチよりもユーザ体験を向上させるかどうか」を検証する.
この実験では，式 (9) で $K = 16$ と capping $c = e^3$ を使用した.

シミュレーションで示したように，以前テストした標準的なオフポリシー補正はトップ 1 のアイテムを正すことに過度に集中した方策を導くが，top-Kオフポリシー補正は，**ユーザが興味を持つ他のアイテムにもゼロではない質量**があるような，**より滑らかな方策に収束させる**.

これにより、より良いtop-Kの推薦につながる.

数のアイテムを推薦することができることを考えると、top-K オフポリシー補正は標準的なオフポリシー補正よりもユーザに良いフルページ体験を提供することにつながる.

特に、テストトラフィックでは、ViewTime の量が 0.85% 増加し、動画の視聴数は 0.16% とわずかに減少していることがわかった.

#### ハイパーパラメータの効果を理解する.

最後に、ハイパーパラメータの選択がtop-K off-policy補正、ひいてはプラットフォームでのユーザ体験にどのような影響を与えるかを直接比較した.
これらのテストは、**top-K off-policy補正がプロダクションモデル(=プロダクトに採用してるモデル?)になった後に実施**した.

##### action数$K$について

top-K off-policy補正におけるKの選択について検討する.
$K \in {1, 2, 16, 32}$ を用いて、3つの構造的に同一のモデルを訓練する. control(production)モデルは、$K = 16$ の top-K off-policy モデルである.
5 日間の実験の結果を図 5 にプロットする.

![](https://camo.qiitausercontent.com/dcb33dfab57f4572c29f6aa9f02db1aa6e546801/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f63353764313333622d373234352d323465312d633530662d3264323930653036613532372e706e67)

前述したように、K = 1 の場合、top-K off-policy の補正係数は標準の off-policy の補正係数と一致する.

K = 1 では、$K = 16$ のベースラインと比較して 0.66% の ViewTime の減少が観察された.
これは、標準のオフポリシー補正よりも、top-Kオフポリシー補正の方が効果が大きい事をさらに確認できるような結果.
K = 32はベースラインと同様の性能を達成した.
フォローアップ実験を行ったところ、K = 8 のときに、ViewTime がわずかに増加しました (+0.15% 統計的に有意).

##### importance weightのcappingについて

ここでは分散削減技術(=policy-gradient推定の!)の効果について考察する.
weight capping は初期の実験においてオンラインで最大の利得をもたらす.

本実験では、式(9)のcap $c = e^3$ (productionモデルと同じ)を用いて学習したモデルと， $c = e^5$を用いて学習したモデルを比較した.
importance weightの制限を解除すると，学習された方策$\pi_{\theta}$は**偶然に高い報酬を受け取る少数の記録された行動(action)に対して過剰に適合する可能性**がある.
オンライン実験では、importance weightの上限が解除されたときに、ViewTimeが0.52%という大幅な低下を観測している.

## 議論はある？

探索の話?

## 次に読むべき論文は？

- REINFORCEに基づく本論文の後継の論文(推薦における探索の効果の話?)[Values of User Exploration in Recommender Systems](https://dl.acm.org/doi/pdf/10.1145/3460231.3474236)

## お気持ち実装

時間的な余力がなく...!
