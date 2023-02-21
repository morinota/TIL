# 1. Bayesian Personalized Ranking from Implicit Feedback

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## 1.1. どんなもの?

- implicit feedbackからアイテムを推薦する手法として行列因子分解(Matrix Factorization, MF)や適応的最近防探索法(Adaptive K-nearest Negibhor: kNN)等の手法が存在するが、これらの手法はパーソナライズされたアイテムランキングを予測するタスクの為に設計されているのにも関わらず、**ランキングの為に直接最適化されていない(=ランキングを考慮した損失関数ではない、って事??)**.
- 本論文では、Personalized Rankingの為の汎用的なOptimization Criterion(i.e. Loss Functionや目的関数だよね...??)として、**BPR-Opt**を提案する.
  - BPR-Optは、ランキング問題のBayesian Analysisから導出される事後確率最大化(Maximum Porserior, MAP)に基づく推定法(estimator)である.
- また、BPR-Optを基準にモデルを最適化する為の、汎用的な学習アルゴリズム**LearnBPR** を提案する.
  - LearnBPR は、bootstrap samplingによる確率的勾配降下法(stochastic gradient descent)にもとづく最適化手法である.
- 本論文では、Personalized Rankingタスクに対して、提案手法がMFとkNNの標準的な学習手法を凌駕する事を示した.
- この結果は、**正しい criterion**で モデルを最適化する事の重要性を示している.

## 1.2. 先行研究と比べて何がすごい？

- 1. Personalizedされた最適なランキングのための事後確率最大推定量から導かれる汎用的なOptimization Criterion(=目的関数、損失関数)としてBPR-Optを提案.
- 2. BPR-Optに関してモデルを最適化するために、我々は確率的勾配降下法とブートストラップサンプリングに基づく汎用学習アルゴリズム **LearnBPR** を提案.
- 3. BPR-Opt & LearnBPR を2つの最先端(当時の!)推薦モデルに適用する方法を示した.
- 4. 実験の結果、Personalized Rankingのタスクに対して、BPRによるモデル学習が他の学習方法よりも優れている事が示された.

## 1.3. 技術や手法の肝は？

### 1.3.1. Formalization & 問題設定

Uを全ユーザの集合、Iを全アイテムの集合として、implicit feedback $S \subset U×I$を想定する.

ここで推薦システムのタスクは、ユーザ毎にパーソナライズされた全アイテムの合計順位 $>_u \subset I^2$ を提供することである. (ここで、$I^2$のサブセットなのは、I内の任意の２種類のアイテムに対して、ユーザ毎にパーソナライズされたPairwiseのrankingを予測するから...??)

ここで$>_u$は、以下の total order の特性(?)を満たさなければならない。

$$
\forall i, j \in I: i \neq j => i >_u j \lor j >_u i \tag{totality}
$$

$$
\forall i, j \in I:  i >_u j \land j >_u i =>i=j \tag{antisymmetry}
$$

$$
\forall i, j, k \in I:  i >_u j \land j >_u k => i >_u k \tag{transitivity}
$$

- $\forall$=任意の、全ての $\forall$=arbitrary, all

- $\lor$ = 論理和(or), "または" $\lor$ = logical OR, "or"

- $\land$ = 論理積(and), "かつ" $\land$ = logical product(and), "and"

- $\subset$ = 部分集合. subset$ = 部分集合。

また、便宜上、以下のように定義する.

$$
I_u^+ := {i \in I : (u,i) \in S}
\\
U_i^+ := {u \in U : (u,i) \in S}
$$

### 1.3.2. 問題設定の分析から Bayesian Personalized Ranking(BPR)へ

implicit feedback システムでは、positiveのクラスのみが観測される.
残りのデータは、実際には**負の値や欠損値が混在**している.
欠損値問題に対処する最も一般的なアプローチは、欠損値をすべて無視する事だが、そうすると典型的な機械学習モデルは、2つのレベルを区別できなくなり、何も学習できなくなる.

アイテム推薦の通常のアプローチは、アイテムに対するユーザの好みを反映したPersonalized Score $\hat{x}_{ui}$を予測することである.
そして、そのスコアに従ってアイテムをソートすることでランク付けを行う.
機械学習アプローチ[5, 10]では、$(u, i) \in S$にpositiveのクラスラベルを、 $(U × I) \setminus S$ に含まれる**0要素の組み合わせにnegativeのクラスラベルを与えてSから学習データを作成する**ことが一般的(図1参照).

![](https://camo.qiitausercontent.com/333cc14ac6adf74a453597ad237f139336fd4af9/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f30356564616461632d613132372d663638372d643566362d3663316631663430383535382e706e67)

つまり、Sに含まれる要素は値1、それ以外は値0と予測するようにモデルを最適化する.
この方法の問題点は、**学習時にモデルが将来順位をつけるべき要素**（$(U × I) \setminus S$）が全て負のフィードバックとして学習アルゴリズムに提示されることである.
つまり、十分な表現力を持つ（学習データにぴったりとフィットする）モデルは、0ばかりを予測してしまうため、全く順位がつけられない.
このアプローチが順位を予測できるのは、**正則化のようなオーバーフィッティングを防ぐための戦略**を適用した場合だけである. (なるほど...確かに正則化項を追加すれば、この手法でもなんとかなるのか...!)

![](https://camo.qiitausercontent.com/e13e09924f951aef991b41bb2361d6a60a98ab54/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f39333863653938652d333135642d306664662d613636322d6363383666376333396539392e706e67)

本手法では、学習データとしてアイテムペアを使用し、単アイテムのスコア(point-wise)ではなく、アイテムペアを正しくランク付けすることで最適化するアプローチ(**pair-wise**)をとっている. これは、単に欠損値を負の値で置き換えるよりも問題をよく表している.
Sから各ユーザーの$>_u$の部分を再構築することを試みる.
本手法において、「もしあるアイテムiがユーザuによって閲覧されたことがあれば（すなわち$(u, i) \in S$）、そのユーザは他のすべての非観測アイテムよりもこのアイテムを好む」と仮定する.
例えば図2において、ユーザ $u_1$ はアイテム $i_2$ を見たが、アイテム $i_1$ は見ていないので、このユーザはアイテム $i_2$ を $i_1$ より好むと仮定する.
これを定式化するために、学習データ $D_s:U × I × I$を定義する:

$$
D_s := {(u,i,j)|i \in I_u^+ \land j \in I\setminus I_u^+}
$$

任意のTriplet $(u, i, j)\in D_s$は、「ユーザ u はアイテムj よりも アイテムiを好む」という仮定を意味する.

### 1.3.3. 損失関数:BPR-Opt

尤度関数$p(i >_u j |\Theta)$ 及び モデルパラメータの事前確率$p(\Theta)$ を用いてベイズの定理に基づき、最適化基準BPR-Optを導出する.

全てのアイテム$i \in I$に対して正しい Personalized ranking を求めるベイズ定式化は、以下の事後確率を最大化することである.
($Theta$は任意の推薦モデルクラス(ex. 行列分解)のパラメータベクトル)

$$
p(\Theta|>_u) \propto p(>_u|\Theta) p(\Theta)
$$

ここで、以下の２つの仮定を採用する.

- 全てのユーザは互いに独立して行動する.
- あるユーザに対する任意のアイテム2つ組（i, j）の順序は、他のすべての2つ組の順序とは独立である.

この2つの仮定により、ユーザ毎の尤度関数$p(>_u|Theta)$を全ユーザの同時確率として、以下のように置き換えられる.

$$
\prod_{u \in U} p(>_u | \Theta) = \prod_{(u,i,j) \in U \times I \times I} p(i >_u j|\Theta)^{\epsilon((u,i,j)\in D_s)} \cdot (1 - p(i >_u j|\Theta))^{\epsilon((u,i,j)\in D_s)}
$$

ここで、$epsilon$は指標関数(indicator function).

$$
\epsilon(b) := 1 \text{ if b is true} \text{ else } 0
$$

$>_u$が満たすべきtotal order の特性(totality と antisymmetry)より,上の尤度関数は以下のように簡略化される.

$$
\prod_{u \in U} p(>_u | \Theta) = \prod_{(u,i,j) \in D_s} p(i >_u j|\Theta)
$$

↑を成立させるためには、total order の特性(全体性、非対称性、推移性)を満たす必要がある.(=まあだから尤度関数を簡略化できたのだし...!!)

そのために(??)、あるユーザーがアイテムjよりもアイテムiを本当に好む個別確率を次のように定義する.

$$
p(i >_u j|\Theta) := \sigma(\hat{x}_{uij}(\Theta))
$$

ここで、$sigma$はsigmoid関数.
$hat{x}_{uij}( \Theta)$ は、ユーザu、アイテムi、アイテムjの関係を捉えるモデルパラメータベクトル$\Theta$に基づく**任意**の実数値関数である.
言い換えれば、本論文で提案するBPR汎用フレームワークは、u、i、j間の関係のモデル化タスク(i.e. $\hat{x}_{uij}( \Theta)$ を推定する事)を任意の推薦モデルクラスに委ねる(ex. 行列分解, 適応的kNN).

ここまでが尤度関数に関する説明.
以下が事前分布に関する説明.

モデルパラメータの事前分布として、平均が0で分散共分散行列が$\Sigma_{\Theta}$の正規分布である一般的な事前確率密度(=事前分布)$p(\theta)$ を導入する.

$$
p(\Theta) \sim N(0, \Sigma_{\Theta})
$$

以下では、未知のハイパーパラメータの数を減らすために、$Sigma_{Theta} = \lambda_{Theta} I$と仮定する.(i.e. 各モデルパラメータの事前分布は、それぞれ独立 & 等しい分散を持つ & 同じ形状の確率分布に従う. = **i.i.d.**っていうんだっけ??)

ここまでで尤度関数と事前分布を定式化できたので、**最大事後推定量(MAP推定量)**を定式化し、Personalized rankingの汎用最適化基準BPR-Optを導出することができる.

$$
BPR-O_{PT}:= \ln \prod_{u \in U} p(\Theta| >_u) \\
= \ln \prod_{u \in U} p(>_u | \Theta) p(\Theta) \\
= \ln \prod_{(u,i,j) \in D_s} \sigma(\hat{x}_{uij}(\Theta)) p(\Theta) \\
= \sum_{(u,i,j) \in D_s} \ln \sigma(\hat{x}_{uij}(\Theta)) + \ln p(\Theta) \\
= \sum_{(u,i,j) \in D_s} \ln \sigma(\hat{x}_{uij}(\Theta)) -  \lambda_{\Theta}||\Theta||^2 \\
$$

ここで、$lambda_{Theta}$はモデル固有の正則化パラメータである. (=元々の意味合いは、モデルパラメータの事前分布をi.i.dの正規分布と仮定した時の、標準偏差...!)

#### 1.3.3.1. (おまけ)

BPR-Optを定式化すると、AUCとの類似性を把握できる.

ユーザーごとのAUCは通常次のように定義される:

$$
\text{AUC}(u) := \frac{1}{|I_u^+||I \setminus I_u^+|} \sum_{i \in I_u^+} \sum_{j \in |I \setminus I_u^+|} \epsilon(\hat{x}_{uij} > 0)
$$

したがって、全ユーザ平均のAUCは...

$$
\text{AUC} := \frac{1}{|U|} \sum_{u \in U} \text{AUC}(u)
$$

$D_s$による表記で、全ユーザ平均のAUCは以下のように書ける...!

$$
\text{AUC}(u):= \sum_{(u,i,j) \in D_S} z_u \epsilon(\hat{x}_{uij} > 0)
\\
z_u = \frac{1}{|U| |I_u^+||I \setminus I_u^+|}
\\
\epsilon(x > 0) = H(x) := 1 \text{ x>0, } \text{ else } 0
\tag{1}
$$

ここで、$z_u$は正規化定数(normalizing constant = ノルムを1にする為の定数??).

全ユーザ平均のAUCとBPR-Optは共通点が多く、異なる点は以下の2つ.

- 正規化定数$z_u$の有無.
- non-differentiable(微分不可能)な $\epsilon(x > 0)$か / differentiable(微分可能)な$\sigma(x)$か.
  - AUCを最適化する際に、微分不可能なHeaviside関数$\epsilon(x > 0)$を置き換えるのは一般的な方法らしい...!

### 1.3.4. 最適化手法:LearnBPR

BPR-Optはパラメータについて微分可能なので、勾配降下法(gradient descent)に基づくアルゴリズムがパッと選択肢になる.

しかし、後述するように、標準的な勾配硬化法はPersonalized Ranking問題において正しい選択とは言えない. (その理由を以下にまとめていく...!)

まずモデルパラメータに対するBPR-Optの勾配は以下である.

$$
\frac{\partial BPR-O_{PT}}{\partial \Theta}
= \sum_{(u,i,j) \in D_S} \frac{\partial}{\partial \Theta} \ln \sigma(\hat{x}_{uij})
- \lambda_{\Theta} \frac{\partial}{\partial \Theta} ||\Theta||^2
\\
\propto
\sum_{(u,i,j) \in D_S} \frac{-e^{-\hat{x}_{uij}}}{1 + e^{-\hat{x}_{uij}}} \frac{\partial}{\partial \Theta} \hat{x}_{uij}
- \lambda_{\Theta} \Theta
$$

勾配降下法(gradient descent)には、完全勾配降下法(full gradient descent)と確率的勾配降下法(stochastic gradient descent)の2種類があり、完全勾配法が最も一般的.

最初のケースでは、各ステップですべての学習データに対する完全勾配を計算し、学習率 $alpha$ でモデルパラメータを更新してみる.

$$
\Theta \leftarrow \Theta - \alpha \frac{\partial BPR-O_{PT}}{\partial \Theta}
$$

もう1つのケースは、確率的勾配降下法(stochastic gradient descent)である.
この場合、$D_S$の各トリプル $(u,i,j)$について、更新が行われる.

$$
\Theta \leftarrow \Theta - \alpha (\sum_{(u,i,j) \in D_S} \frac{e^{-\hat{x}_{uij}}}{1 + e^{-\hat{x}_{uij}}} \frac{\partial}{\partial \Theta} \hat{x}_{uij}
+ \lambda_{\Theta} \Theta)
$$

一般に確率的勾配降下法は今回のタスクに問題に対して良いアプローチだが、implicit feedbackの場合、1つのユーザ \* positive アイテムペア（u, i）に対して、$(u, i, j) \in D_S$を満たす多くのnegative アイテム j が存在する.

この問題を解決するために、Triplet をランダムに（一様に）選択する確率的勾配降下アルゴリズムを使用することを提案する.
このアプローチでは、連続した更新ステップで同じ Triplet の組み合わせを選択する可能性は小さい.
また、任意のステップで停止が可能であるため、replacementを伴う(??)bootstrap sampling アプローチを使用することを提案する.

全てのデータを学習に使うアイデアを放棄する事は、今回のタスクでは特に有効. (Tripletの数が非常に多い & positive アイテムが少ない??)

本論文では、観測されたpositive feedback (u,i)の数$S$に応じて、single ステップの数(=バッチサイズ?)を線形に選択する.

図5は、典型的なuserwise(=ユーザ毎??)確率的勾配降下法と我々のアプローチLearnBPR with bootstrappingの比較. (採用したモデルは、factor_size=16のBPRMF)

![](https://camo.qiitausercontent.com/8929a7f2017b44372b15de459522b479dfac7e7f/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f62623961623834382d346362612d323130332d306432352d3233346638376636666531332e706e67)

LearnBPRはユーザーワイズ勾配降下法よりはるかに速く収束する事がわかる.

## 1.4. どうやって有効だと検証した?

### 1.4.1. 検証方法

BPRを用いた学習を他の学習アプローチと比較した.
行列分解(MF)とk-nearest-neighborという**2つの一般的な推薦モデル**を選択.
他の学習アプローチ(SVD-MF, WR-MF, Cosine-kNN)と、提案されたBPRを用いて学習させたモデル(BPR-MF, BPR-kNN)を比較する.

2つの異なるアプリケーションのデータセットを使用: Rossmannデータセット(オンラインショップの購買履歴), the DVD rental dataset of Netflix.

評価方法: 各ユーザの履歴からランダムに一つのアクションを抜き出しテストデータ$S_{test}$を作る. 残りを訓練データ$S_{train}$とする.
モデルは$S_{train}$を用いて学習され、予測されたPersonalized Ranking は$S_{test}$上で平均AUC統計量によって評価される.

$$
AUC = \frac{1}{|U|} \sum_{u} \frac{1}{|E(u)|}
\sum_{(i,j) \in E(u)} \delta(\hat{x}_{ui} > \hat{x}_{uj})
\tag{2}
$$

ここで、任意のユーザu毎の２つ組(i,j)の集合$E(u)$は以下で表される.

$$
E(u) := {(i,j)|(u,i) \in S_{test} \And (u,j) \notin (S_{test} \cup S_{train})}
$$

AUCの値が高いほど精度が良いことを示している.
ランダムなモデルのAUCは0.5であり、達成可能な最高の精度は1.0である.

我々は、各ラウンドで新しいtrain/test分割を描くことによって、すべての実験を10回繰り返した.
すべての手法のハイパーパラメータは、最初のラウンドでグリッドサーチにより最適化され、その後、残りの9回の繰り返しで一定に保たれる.

### 1.4.2. 検証結果

![](https://camo.qiitausercontent.com/f7398661d4548afb6edea3eac2083493efeb3614/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f62346638363833322d386265352d646237662d633434662d6534383938613037323863352e706e67)

まず、BPRで最適化された2つの手法は、予測品質において他のすべての手法を上回っている.
同じモデル同士を比較すると、optimization criterion & method の重要性がわかる.
例えば、すべてのMF手法（SVD-MF、WR-MF、BPR-MF）は全く同じモデルを共有しているが、その予測品質は大きく異なってる.

- SVD-MFは、要素ごとの最小二乗法に関しては学習データに最もフィットすることが知られているが、オーバーフィッティングになるため、implicit feedbackを用いたPersonalized Ranking タスクの予測手法としては不向き.
  - これは、SVD-MFの品質が次元数の増加とともに低下することからもわかる. 次元数が増える程、表現力が高くなる->overfitting しやすくなる. -> negative feedbackを等しくnegativeとして予測してしまう.
- WR-MFはランキングのタスクではより成功した学習方法.
  - 正則化により、WR-MFの性能は次元数の増加とともに低下することなく、着実に向上する.
- しかし、BPR-MFは両データセットにおいて、ランキングのタスクで明らかにWR-MFを上回る性能を示している.
  - 例えばNetflixでは、BPR-MFで最適化された8次元のMFモデルは、WR-MFで最適化された128次元のMFモデルと同等の品質を達成する

## 1.5. 議論はある？

要約すると、我々の結果はモデルパラメータを**正しい基準(=ランキング問題なのだから、ランキングを考慮した損失関数を使って学習しよう！って話...!!)で最適化**することの重要性を示している.
実証結果は、LearnBPRによって学習された我々のBPR-Opt基準は、implicit feedback からPersonalized Rankingタスクのための他の最先端手法(当時の!)を凌駕していることを示している.

## 1.6. 次に読むべき論文は？

- BPRの元論文を読んだので、これでBPRの派生手法を読みやすくなった...!!
- [@guglilac 様の記事](https://qiita.com/guglilac/items/49bc35bd2631177624ce) にBPRの派生研究が紹介されているので読んでみる.
- 次週は、推薦モデルの効果(=推薦モデルがユーザの行動を変えたかどうかのcausal effect??)を適切に評価する為の"Uplift"に関する論文を読む. (最近、推薦モデルのオフライン評価方法について考えていたので...)

## 1.7. お気持ち実装

実装するとしたら、なんとなくこんな感じ...?
