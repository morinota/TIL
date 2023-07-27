# Off-Policy Evaluation for Large Action Spaces via Embeddings

published date: 16 June 2022
authors: Yuta Saito, Thorsten Joachims
url(paper): https://arxiv.org/pdf/2202.06317.pdf
(勉強会発表者: morinota)

---

## どんなもの?

- オンライン環境で稼働中の意思決定システム(ex. 推薦システム) logging policy $\pi_{0}$ のログを使って、開発中のtarget policy $\pi$ のオンライン性能を推定する Off-Policy Evaluation(OPE)に関する論文。
- 先々週のwantedlyさん主催の勉強会に参加させていただいた際に、登壇者の斉藤さんが紹介されていたので興味を持って読んでみました!
- 人気なOPE推定量である IPS(Inverse Propensity Score)推定量は、大規模行動空間であるほど真の target policy の性能に対する Bias と Variance がどんどん増える可能性がある。
- なので本論文では、**大規模行動空間に耐えうるOPE推定量**として、**IPS推定量のaction を action embedding(i.e. action の特徴量?) で置き換えた Marginalized IPS(MIPS)推定量**を提案している。
- 行動空間が大きい場合の実証実験にて、MIPS推定量はIPSや関連推定量よりも大幅に良いパフォーマンスを示した。
- 行動空間が大きい場合だけでなく、**logging policy と target policy が大きく異なっている場合**にもIPSよりも有効みたい。(IPSの仮定よりもMIPSの仮定の方がだいぶ成立しやすいもんなぁ...:thinking:)
- (特に確率論的な意思決定モデルを採用してるケースでは、MIPS推定量はオフライン評価の方法として有効なのでは...!:thinking:)

## 先行研究と比べて何がすごい？

![image](https://github.com/wantedly/machine-learning-round-table/assets/72015657/bbb3660e-6959-495f-8bec-453629e0e24e)

- 人気なOPE推定量である IPS推定量は、以下の **Common Support Assumption** を満たす場合に 真の性能に対して不偏になる:

$$
\pi(a|x) > 0 → \pi_{0}(a|x) > 0, \forall a \in A, x \in X
$$

- ここで、$a$ はaction(ex. 推薦アイテムの選択肢), $x$ は context (ex. ユーザの特徴量)
  - (なるほど...!この仮定は、決定論的な推薦モデルよりも確率論的な推薦モデルの方が遥かに満たしやすいよなぁ...。というか、決定論的なモデルでこの仮定を満たせるのって $\pi = \pi_{0}$ だけじゃないか...?:thinking:)
- **でも大規模行動空間であるほど Common Support Assumption が成立しづらくなり、IPS推定量の真の性能に対するBiasとVarianceがどんどん増えていく...**!

  - -> これは、logged dataset $D$ に(i.e. $\pi_0$ に)サポートされていないactionの情報が含まれなくなる事に起因する。
  - (i.e. context $x$ を受け取った際に target policy $\pi$ では選択され得るが、logging policy $pi_0$ では選択され得ないアイテムの情報が $D$ 内で欠如するので...:thinking:)

- 本論文では、大規模行動空間を持つ意思決定タスクに適用可能なIPS推定量のaction $a$ を action embedding(i.e. action の特徴量的な認識) $e$ で置き換えた **Marginalized IPS(MIPS)推定量**を提案している。

## 技術や手法の肝は？

![image](https://github.com/wantedly/machine-learning-round-table/assets/72015657/c98ae013-4f9e-4472-81a6-359530cc0e07)

MIPS推定量が不偏になる為の条件として、以下の "**Common Embedding Support Assumption**" を満たす必要がある。

$$
p(e|x, \pi) > 0 → p(e|x, \pi_{0}) > 0, \forall e \in E,  x \in X
$$

- 大規模行動空間において common support assumption は厳しいけど、common embedding support assumption の方が遥かに成立させやすいので、MIPS推定量は有効。
- (やっぱり common embedding support assumption も確率論的な推薦モデルの方が遥かに満たしやすいよなぁ...。OPEの観点では決定論的な推薦モデルはご法度というか、かなり扱いづらそう...。:thinking:)

MIPS推定量が不偏になる条件としてもう一つ "No Direct Effect Assumption" を満たす必要もある: $a \perp r | x, e$

ただ論文内では、**意図的にno direct effect assumptionを破るような action embedding $e$ を選択すること**で、推定量のbiasはやや増えるが variance を減らす事ができて、真の性能に対するMSEを減らす事ができる、という戦略を提案していた。

## どうやって有効だと検証した?

- synthetic data と real-world data (Open Bandit Dataset) を使用して、MIPS推定量の性能を検証している。

### synthetic data (擬似的な合成データ)の実験

target policy の ground truth 値とOPE推定値を比較できるように、合成データを作成。

図2は、action数を10から5000まで変化させたときの推定値の性能を評価。(logged dataset $D$ のサンプルサイズは $n = 10000$ に固定。)

![]()

- 特に大規模なaction集合において、MIPS は IPS や DR よりも MSE が優れていた。
- また大規模なaction集合において、`MIPS(true)`(=周辺重要度重みが既知の場合のMIPS) は `MIPS`(=周辺重要度重みが未知で、ロジスティック回帰で推定した場合のMIPS) よりも優れていた。

図3は、logged dataset $D$ のサンプル数($n \in \{800, 1600, 3200, 6400, 12800, 25600\}$)を変化させた場合の各種OPE推定量のパフォーマンス。

![]()

- MIPSは特にサンプルサイズが小さい場合に、IPSやDRよりも大きく優れている。
- サンプルサイズが大きくなるにつれて、MIPS、IPS、DRは分散が小さくなりMSEが改善される。
- DM(=唯一IPS系の推定量ではないbaseline)の精度はサンプルサイズが異なっても変わらない。(DM推定量は**低variance 高biasの特徴を持つ推定量**だから...! 高biasというか 報酬予測モデル $\hat{q}(x, a)$ の精度に依存するって感じ)。大規模行動空間においては、分散が爆発するIPSやDRよりも優れているといえる。
- MIPSのバイアスはDMのバイアスよりもはるかに小さいため、MIPSはDMよりも優れた性能。サンプルサイズが大きくなるほど、MIPSはDMよりもどんどん良くなる。
  - (IPS系のOPE推定量の特徴は、仮定を満たせば 低bias 高variance なので、サンプルサイズが増えると variance が減少して性能が上がっていく。)

No Direct Effect Assumption を満たしているか否かが、MIPSの性能(MSE)にどう影響を与えるかの実験の話。
図5は、**action embedding の未観測の次元数**を変えることによって、MIPS推定量のMSE & Bias^2 & Variance が、どのように変化するかを示した結果。

![]()

- MIPSとMIPS(true)は、action embedding が多少欠落した状態でも、他の推定量と比べて良い性能を発揮した。(no direct effect assumptionが破られた事により、Biasが大きくなってもVarianceが減少したから??:thinking:)
- 未観測の次元数が増えるにつれて、**MIPSとMIPS(true)の Variance が大幅に減少する**一方、Bias は仮定に違反するにつれて(i.e. 仮定の違反度合いが大きくなるに連れて)増加する.

### Open Bandit Datasetを使った実験

- Open Bandit Datasetは、**2つの異なる policy(一様ランダムサンプリングとトンプソンサンプリング)のA/Bテストで収集された2セットの logged dataset** から構成される。
  - logged datasetには、 user context $x$, action(推薦アイテム) $a \in A (|A| = 240)$, reward(クリック有無) $r \in \{0, 1\}$ が含まれる。
    - (行動空間の大きさ的にはまあまあなのかな:thinking:)
  - 加えて、推薦アイテムのカテゴリ情報っぽい4次元の action embedding $e$ を含む。
- 一様無作為サンプリングとトンプソンサンプリングをそれぞれ loggint policy とtarget policy とみなして、OPE推定量の評価を行う。

![]()

- `MIPS(w/ SLOPE)`(=SLOPEという手法で action embedding 選択を行った場合のMIPS) はシミュレーションの約80%でIPSを上回り、`MIPS(w/o SLOPE)`(action embedding 選択無しの場合のMIPS)を含む他の推定量はIPSと同様に機能した。
- MIPS推定量の実世界での適用可能性あり! action embedding selectionを適用する事の重要性!

## 議論はある?

今後の研究課題。

- action embedding $e$ の選択・最適化方法。
- 周辺重要度重みがhogehogeな場合の、周辺重要度重みのより正確な推定方法の開発。
- action embedding を用いて off-policy learning
- DR推定量のようなIPS推定量の派生系に関連して、MIPS推定量の応用の可能性。

## 次に読むべき論文は？

- 決定論的な推薦モデルでは common support assumption も common embedding support assumption も厳しい気がするので、決定論的な推薦モデルをシンプルに確率論的な推薦モデルに拡張する手法か、決定論的な推薦モデルでも適用しやすいオフライン評価手法を探したいな...。もしオススメの解法等があれば教えていただきたいです...!

## お気持ち実装

今回はスキップです! コードも公開してくださってるので後で触ってみたい。
