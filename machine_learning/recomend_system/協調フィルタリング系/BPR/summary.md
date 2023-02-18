# Bayesian Personalized Ranking from Implicit Feedback

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## どんなもの?

- implicit feedbackからアイテムを推薦する手法として行列因子分解(Matrix Factorization, MF)や適応的最近防探索法(Adaptive K-nearest Negibhor: kNN)等の手法が存在するが、これらの手法はパーソナライズされたアイテムランキングを予測するタスクの為に設計されているのにも関わらず、**ランキングの為に直接最適化されていない(=ランキングを考慮した損失関数ではない、って事??)**.
- 本論文では、Personalized Rankingの為の汎用的なOptimization Criterion(i.e. Loss Functionや目的関数だよね...??)として、**BPR-Opt**を提案する.
  - BPR-Optは、ランキング問題のBayesian Analysisから導出される事後確率最大化(Maximum Porserior, MAP)に基づく推定法(estimator)である.
- また、BPR-Optを基準にモデルを最適化する為の、汎用的な学習アルゴリズム**LearnBPR** を提案する.
  - LearnBPR は、bootstrap samplingによる確率的勾配降下法(stochastic gradient descent)にもとづく最適化手法である.
- 本論文では、Personalized Rankingタスクに対して、提案手法がMFとkNNの標準的な学習手法を凌駕する事を示した.
- この結果は、**正しい criterion**で モデルを最適化する事の重要性を示している.

## 先行研究と比べて何がすごい？

- 1. Personalizedされた最適なランキングのための事後確率最大推定量から導かれる汎用的なOptimization Criterion(=目的関数、損失関数)としてBPR-Optを提案.
- 2. BPR-Optに関してモデルを最適化するために、我々は確率的勾配降下法とブートストラップサンプリングに基づく汎用学習アルゴリズム **LearnBPR** を提案する.
- 3. BPR-Opt & LearnBPR を2つの最先端(当時の!)推薦モデルに適用する方法を示した.
- 4. 実験の結果、Personalized Rankingのタスクに対して、BPRによるモデル学習が他の学習方法よりも優れている事が示された.

## 技術や手法の肝は？

### Formalization & 問題設定

### 問題設定の分析から Bayesian Personalized Ranking(BPR)へ

### 損失関数:BPR-Opt

### 最適化手法:LearnBPR

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
LearnBPRはユーザーワイズ勾配降下法よりはるかに速く収束する事がわかる.

## どうやって有効だと検証した?

2つのデータセットを用いて、Personalized Rankingの精度を評価した.

まず、BPRで最適化された2つの手法は、予測品質において他のすべての手法を上回っている.
同じモデル同士を比較すると、optimization criterion & method の重要性がわかる.
例えば、すべてのMF手法（SVD-MF、WR-MF、BPR-MF）は全く同じモデルを共有していますが、その予測品質は大きく異なってる.

- SVD-MFは、要素ごとの最小二乗法に関しては学習データに最もフィットすることが知られているが、オーバーフィッティングになるため、implicit feedbackを用いたPersonalized Ranking タスクの予測手法としては不向き.
  - これは、SVD-MFの品質が次元数の増加とともに低下することからもわかる. 次元数が増える程、表現力が高くなる->overfitting しやすくなる. -> negative feedbackを等しくnegativeとして予測してしまう.
- WR-MFはランキングのタスクではより成功した学習方法.
  - 正則化により、WR-MFの性能は次元数の増加とともに低下することなく、着実に向上する.
- しかし、BPR-MFは両データセットにおいて、ランキングのタスクで明らかにWR-MFを上回る性能を示している.
  - 例えばNetflixでは、BPR-MFで最適化された8次元のMFモデルは、WR-MFで最適化された128次元のMFモデルと同等の品質を達成する

要約すると、我々の結果はモデルパラメータを**正しい基準(=ランキング問題なのだから、ランキングを考慮した損失関数を使って学習しよう！って話...!!)で最適化**することの重要性を示している.
実証結果は、LearnBPRによって学習された我々のBPR-Opt基準は、implicit feedback からPersonalized Rankingタスクのための他の最先端手法(当時の!)を凌駕していることを示している.

## 議論はある？

## 次に読むべき論文は？

- BPRの元論文を読んだので、これでBPR応用手法を読みやすくなった...!!

## お気持ち実装

実装するとしたら、なんとなくこんな感じ...?
