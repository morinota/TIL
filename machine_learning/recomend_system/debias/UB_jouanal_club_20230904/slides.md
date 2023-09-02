---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: ABテストする前に機械学習モデルの性能を確度高く評価したいけど、皆どうやってるんだろう?について色々調べている話
subtitle: 論文読み会
date: 2023/09/04
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 参考文献:

- usaitoさんの資料: [Off-Policy Evaluationの基礎とOpen Bandit Dataset & Pipelineの紹介](https://speakerdeck.com/usaito/off-policy-evaluationfalseji-chu-toopen-bandit-dataset-and-pipelinefalseshao-jie)
- 大規模行動空間におけるOPEの論文: [Off-Policy Evaluation for Large Action Spaces via Embeddings](https://arxiv.org/pdf/2202.06317.pdf)
- 複数のオフラインmetricsからオンライン性能を予測する論文: [Predicting Online Performance of News Recommender Systems Through Richer Evaluation Metrics](https://dl.acm.org/doi/10.1145/2792838.2800184)
- netflixのtechブログ: [Innovating Faster on Personalization Algorithms at Netflix Using Interleaving](https://netflixtechblog.com/interleaving-in-online-experiments-at-netflix-a04ee392ec55)
- naiveだけど有効なオフライン評価方法をしてた contextual bandit の論文: [A contextual-bandit approach to personalized news article recommendation](https://arxiv.org/pdf/1003.0146.pdf)

## 今回のテーマを選んだ経緯

- 推薦や広告配信等の意思決定タスクに機械学習を適用する上で、オフライン評価とオンライン評価の結果の乖離問題がある。
-

## ABテストする前に機械学習モデルの性能を確度高く評価できたらどんな点が嬉しい?

:::: {.columns}

::: {.column width="50%"}

できる場合

- ABテスト前に有効そうな施策を絞り込む事ができ、仮説 -> 施策 -> 検証をより高速に回す事ができる。
- ハイパーパラメータチューニングができる。
- ユーザ体験を悪化させ得る施策を、オンライン環境に出す前に検知する事ができる。

:::

::: {.column width="50%"}

できない場合

- 全ての仮説に対してABテストする必要があり、仮説 -> 施策 -> 検証の速度が下がる。(ABテストの運用コストを下げても、どうしてもオフライン実験するよりは時間がかかる。10倍くらい?)
- 誤った基準でハイパーパラメータチューニングしてしまう可能性。
- ユーザ体験を悪化させ得る施策を、オンライン環境に出す可能性。

:::

::::

## 色々調べたオフライン評価の確度をあげるアプローチ達

- 1. 理論的に保証されてる!: Off-Policy Evaluation手法を用いて過去のログデータからオンライン性能を推定(@ ファッションアイテムの推薦)
- 2. 力技!: オフライン観測可能なmetricsからオンライン性能の予測モデルを作る(@ ニュース記事の推薦)
- 3. naiveだけど導入しやすさと効果は高そう: 一定期間のみ、一様ランダムなモデルを本番適用してログデータ収集 (@ ニュース記事の推薦)
- 4. より高速なオンライン評価手法 Interleaving をABテストの前に導入する(@ 動画の推薦)

今日は主にアプローチ1について紹介し、アプローチ2 ~ 4はさらっと紹介程度の予定。

# 調べた方法1. 理論的に保証されてる!: Off-Policy Evaluation手法を用いて過去のログデータからオンライン性能を推定(@ ファッションアイテムの推薦)

- 自分はusaitoさん & wantedlyさんの勉強会に参加してこのOff-Policy Evaluation(以下、OPE) 分野を知った。
- 今回は概要紹介 & 自分の感想を話すので、更に詳しくはusaitoさんの資料やOPE関連の論文を読むと良さそう!

## Off-Policy Evaluation(OPE)とは?

OPEは新しいpolicyを製品に導入することなく、その性能を正確に評価する事を目的とした方法論。具体的には、稼働中の意思決定システム **logging policy $\pi_{0}$** で得たログを使って、施策 **target policy $\pi$** のオンライン性能を推定したい。

OPE文献で用いられるnotation

- $\mathbf{x} \in X$: contextベクトル(モデルに入力する特徴量...!)
- $a \in A$: 意思決定タスクにおいて選択される行動(action)。基本的には離散変数。$A$ は行動空間。
- $\pi(a|\mathbf{x})$: 意思決定policyが context $\mathbf{x}$ を受け取って行動 $a$ を選択する確率。
- $r \sim p(r|\mathbf{x}, a)$: 選択された行動に基づいて得られる報酬(reward)(ex. click, 購入, 翌週も継続利用してくれる)

強化学習っぽいnotation...!Off-Policy Learningという分野もあるっぽいし、 contextual banditを想定したOPE論文が多い印象...!:thinking:

## OPEが解きたい問題:

まず、任意の**意思決定policyの性能**を以下の様に定義(=要は報酬の期待値!:thinking:):

$$
V(\pi)
:= \mathbb{E}_{p(\mathbf{x})\pi(a|\mathbf{x})p(r|\mathbf{x},a)}[r]
= \mathbb{E}_{p(\mathbf{x})\pi(a|\mathbf{x})}[q(\mathbf{x},a)]
$$

ここで $q(\mathbf{x}, a) := \mathbb{E}[r|\mathbf{x}, a]$ は、あるcontext $\mathbf{x}$ において行動 $a$ を選択した場合の報酬 $r$ の期待値。
(ex. 報酬 $r$ をclickするか否かと定義した場合は、$V(\pi)$ はCTRになる:thinking:)

OPEでは、**$\pi_{0}$ で得られた過去の $n$ 個のログデータ $D := {(\mathbf{x}_i, a_i , r_i)}_{i=1}^{n}$ のみ**を用いて、($\pi_{0}$ とは異なる) **$\pi$ の性能 $V(\pi)$ を高い精度で推定したい**。その為にOPE推定量 $\hat{V}(\pi)$ を開発したい。

そしてOPE推定量の精度は、MSE(平均二乗誤差)によって定量化される:

$$
MSE(\hat{V}(\pi)) = \mathbb{E}_{D} [(V(\pi) - \hat{V}(\pi;D))^2]
$$

## 各OPE推定量を比較する為の視点: biasとvariance

OPE推定量の評価に用いるMSE(平均二乗誤差)は、以下の様に **$(推定量のbias)^2$ と $(推定量のvariance)$ に分解**できる。

$$
MSE(\hat{V}(\pi)) = \mathbb{E}_{D} [(V(\pi) - \hat{V}(\pi;D))^2]
\\
= Bias[\hat{V}(\pi)]^2 + \mathbb{V}_{D}[\hat{V}(\pi;D)]
$$

よって、**各OPE推定量の良し悪しを比較する際はbiasとvarianceに注目すると良い**らしい。
(ex. 推定量Aは biasは小さいがvarianceが大きい。推定量Bはbiasは大きいがvarianceが小さい)

## 代表的な3つのOPE推定量

基本的にこれら3つのOPE推定量が、OPE研究の基礎になっているらしい:

- DM(Direct Method)推定量
- IPS(Inverse Propensity Scoring)推定量
- DR(Doubly Robust)推定量

この3つのOPE推定量さえ抑えておけば、他の多くのOPE論文が読みやすいはず...!

## 代表的なOPE推定量① DM(Direct Method)

:::: {.columns}

::: {.column width="60%"}

過去の観測データから**事前に報酬期待値 $q(\mathbf{x}, a) := \mathbb{E}[r|\mathbf{x}, a]$ の予測モデル $\hat{q}(\mathbf{x}, a)$ を学習しておき**、それをOPEに用いる。

$$
\hat{V}_{DM}(\pi;D) = \frac{1}{n} \sum_{i=1}^{n} \hat{q}(\mathbf{x}_{i}, \pi(\mathbf{x}_{i});D)
$$

- 特徴: OPEの精度が報酬予測モデル $\hat{q}$ に大きく依存する為、biasは大きい。一方でvarianceは小さい。
- ただそもそも精度の良い報酬予測モデル $\hat{q}$ を作れる時点で、それを使った意思決定policyを運用すれば良いので、OPEとしての実用性は低め。

:::

::: {.column width="40%"}

横軸=観測データ数 n, 縦軸=MSE(& bias^2 と variance)の図

:::

::::

## 代表的なOPE推定量② IPS(Inverse Propensity Scoring)

:::: {.columns}

::: {.column width="60%"}

観測された各報酬 $r_i$ を、logging policy による**行動の選ばれやすさ(=propensity score) の逆数で観測報酬を重み付け**したOPE推定量。

$$
\hat{V}_{IPS}(\pi;D) = \frac{1}{n} \sum_{i=1}^{n} \frac{\mathbb{I}[\pi(\mathbf{x}_{i}) = a_i]}{\pi_{0}(a_i|\mathbf{x}_i)} r_{i}
$$

- biasは小さい(=仮定を満たせば不偏: $\mathbb{E}_{D} [\hat{V}_{IPS}(\pi)] = V(\pi)$)。
- varianceは大きめ、データ $n$ が増える程小さくなっていく。
- 先進的なOPE推定量の多くが、このIPS推定量に基づいている。

:::

::: {.column width="40%"}

横軸=観測データ数 n, 縦軸=MSE(& bias^2 と variance)の図

:::

::::

## 代表的なOPE推定量③ DR(Doubly Robust)

:::: {.columns}

::: {.column width="60%"}

DMとIPSを組み合わせた推定量。
**DM推定量をベースライン**としつつ、報酬期待値予測モデル $\hat{q}$ の誤差を**IPS重み付けで補正**している。

$$
\hat{V}_{DR}(\pi;D) = \hat{V}_{DR}(\pi;D)
\\
+ \frac{1}{n} \sum_{i=1}^{n} (r_{i} - \hat{q}(\mathbf{x}_i, a_i)) \frac{\mathbb{I}[\pi(\mathbf{x}_{i}) = a_i]}{\pi_{0}(a_i|\mathbf{x}_i)}
$$

- 特徴: DM推定量の性質によりvarianceを抑えつつ、IPS推定量の性質(=仮定を満たせば不偏)を受けてbiasを小さくしている。

:::

::: {.column width="40%"}

横軸=観測データ数 n, 縦軸=MSE(& bias^2 と variance)の図

:::

::::

## 大規模行動空間を持つ意思決定タスクでOPEが難しい問題

行動空間が小さい(=行動の選択肢が少ない)場合、IPS推定量に基づく信頼性の高い手法が多く登場した。しかしこれらの手法は、**行動空間が大きい程、真のpolicy性能に対する Bias と Variance がどんどん増える可能性**がある。(=後述するIPSの仮定を満たせなくなるから!)

(論文読んでた感じでは、行動数が1000を超えたくらいから"大規模行動空間"と言える印象:thinking:)

よって、**大規模行動空間に耐えうるOPE推定量**は最近のOPE研究の主要なトピックらしい。
先日の勉強会でusaitoさんが紹介されてた[「大規模行動空間に耐えうるOPE推定量の開発」の論文](https://arxiv.org/pdf/2202.06317.pdf)を読み、概要と感想を紹介します..!

## IPS推定量が不偏推定量になる為の仮定

IPS推定量 $\hat{V}_{IPS}(\pi;D)$ は、以下の**Common Support Assumption**を満たした場合に真の性能 $V(\pi)$ に対して不偏になる:

$$
\pi(a|\mathbf{x}) > 0 \rightarrow \pi_{0}(a|\mathbf{x}) > 0, \forall a \in A, \mathbf{x} \in X
$$

つまり、「**target policy $\pi$ がsupportする(=選択し得る)全ての行動を、logging policy $\pi_{0}$ もsupportしていてくれ！**」という仮定...!

**大規模行動空間であるほどこの仮定が成立しづらくなり**、IPS推定量の bias & variance が増大していく。

この仮定って、 **$\pi_{0}$ が決定論的な意思決定policyの場合**(= context $\mathbf{x}$ が定まると選択する行動 $a$ が一意に定まるpolicy)、**基本的には成立できないよなぁ**:thinking:

逆に、 $\pi_{0}$ が全てのcontext $\mathbf{x}$ に対して全ての行動 $a$ を選び得る場合(ex. 一様ランダムに行動を選ぶpolicy)は仮定が成立するので、観察データさえ増やせばIPS推定量で真の性能を確度高く推定できるはず...!:thinking:

## 大規模行動空間に耐えうるOPE推定量: MIPS推定量の提案

論文では、大規模行動空間に耐えうるOPE推定量として、**IPS推定量のaction を action embedding(i.e. action の特徴量みたいな!:thinking:) で置き換えた Marginalized IPS(MIPS)推定量**を提案。

$$
\hat{V}_{MIPS}(\pi:D)
= \frac{1}{n} \sum_{i=1}^{n} \frac{p(e_i|x_i, \pi)}{p(e_i|x_i, \pi_{0})} r_{i}
$$

## MIPS推定量が不偏推定量になる為の仮定

MIPS推定量が不偏になる為の条件として、以下の "**Common Embedding Support Assumption**" を満たす必要がある:

$$
p(e|x, \pi) > 0 → p(e|x, \pi_{0}) > 0, \forall e \in E,  x \in X
$$

大規模行動空間では、前述のcommon support assumption よりも common embedding support assumption の方が遥かに成立させやすい(**部分一致がOK**なので...!:thinking:)。

(MIPSが不偏推定量になる為の条件はもう一つあるが割愛:No Direct Effect仮定)

(ただ結局この仮定も、logging policy $\pi_{0}$ が決定論的なモデルの場合はかなり厳しいんだよなぁ...。OPEの観点では決定論的な推薦モデルはご法度というか、かなり扱いづらそうな印象:thinking:)

## 決定論的なモデルは無理かと思いつつも...

hoge(決定論的なモデル用のIPS推定量の式も紹介し、無理じゃないんだろうけど、仮定を満たせないよなぁ。。。みたいな話をしたい)

## ちなみにOPEの実験はこんなデータがあればいいらしい！

hoge(Open bandit datasetを紹介しつつ、こんなデータがあれば自社データで、自社の環境に適したOPE推定量を探したり実験できそう!みたいな内容を紹介)

# 調べた方法2. 力技!: オフライン観測可能なmetricsからオンライン性能を予測する回帰モデルを作る(@ ニュース記事の推薦)

## 力技!オフライン観測可能なmetricsからオンライン性能を予測する回帰モデルを作る

- この論文では、accuracy metricsもbeyond-accuracy metricsも含めてオフライン算出可能なmerticsをたくさん使って、推薦システムのオンライン性能(論文ではCTR と online accuracy という指標を定義していた) を予測する回帰モデルを教師あり学習的に作る、という手法を提案していた。
- OPE推定量とは別のアプローチ。シンプル。決定論的な推薦モデルでも適用しやすい気はする:thinking:
- OPE推定量を使うアプローチと組み合わせても良いのでは?? その場合は、低bias高varianceな推定量よりも高bias低varianceな推定量を説明変数として有効そう:thinking:
- また本論文では、オンライン性能予測モデルを用いて、推薦アルゴリズムのハイパーパラメータを自動調整する手法も提案していた。(論文の例では、複数の推薦結果のブレンドの際の重み付け設定をself-adjustingしていました)

# 調べた方法3. naiveだけど導入しやすさと効果は高そう: 一定期間のみ、一様ランダムなモデルを本番適用してログデータ収集 (@ ニュース記事の推薦)

- 2011年のyahooさんの論文。([自分のまとめ記事](https://qiita.com/morinota/items/eb92c63d9ad15f24182b))
- 論文の内容はOPE関連ではないが、実験方法がオフライン評価方法としてnaiveだが効果的だと思い紹介。

## 一定期間、一様ランダムなモデルを本番適用

:::: {.columns}

::: {.column width="50%"}

- 推薦枠の内の1箇所に、選択ロジックとして一様ランダムなpolicyを適用し(=logging policy $\pi_{0}$)、評価用データを収集してた。
- オフライン評価難しい問題の、一番シンプルな解決策かも??**複数の推薦枠のうち、1つだけ一様ランダムにしてもユーザへの悪影響は大きくない気がするし**...!:thinking:
- 1週間とか1ヶ月とかのみ、推薦枠の1箇所のみ、であれば実際に適用可能性あるのでは...?:thinking: その試用期間で得られたログデータをオフライン評価で使い続ければ良いし。

:::

::: {.column width="50%"}

![論文より引用。4つの推薦枠の内、F1のみに適用](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1697279%2Faab2e050-057b-789e-a277-2b6f50a89376.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=6952430697b2b90fd04518ac8a9e7e4a)

:::

::::

# 調べた方法4. より高速なオンライン評価手法 Interleaving をABテストの前に導入する(@ 動画の推薦)

## Interleaving をABテストの前に導入する

:::: {.columns}

::: {.column width="50%"}

- Netflixの推薦システムでは、**Interleaving -> ABテストの2段階のオンライン実験プロセス**を採用してるという話。
- 本内容はオフライン評価ではないが、「**短期間で多くのモデル候補の中から、ABテストするに値するモデルを絞り込む**」という点が共通している為、紹介。(Netflixさんがオフライン評価してないとは言ってない)
- Interleavingは、推薦や検索などのランキングモデルに対するオンライン評価方法の一種。複数のモデルが出力したランキングを Interleaveする(交互に混ぜ合わせ)。同一ユーザに対して複数のモデル出力を表示させ、性能を相対評価する。

:::

::: {.column width="50%"}

Interleaving の説明の図。

:::

::::
