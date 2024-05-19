## refs:

- [Boltzmann Explorationの概要とアルゴリズム及び実装例について](https://deus-ex-machina-ism.com/?p=58663)
- [Wantedly RecSys 2021 参加レポート⑤ - 推薦システムにおける"探索"の価値](https://www.wantedly.com/companies/wantedly/post_articles/351771)

# Boltzmann Explorationについて:

## なにそれ??

- Boltzmann Explorationは、強化学習分野において**探索と活用のバランスを取るための手法の1つ**。
- (要するに、**確率的な行動選択**を行うための手法の一つ...!:thinking:)
- よく epsilon-gredy法と比較される。
  - epsilon-greedy法: 確率 epsilon でランダムな行動を選択し、それ以外の確率 1-epsilon で最適な行動を選択する。
  - boltzmann exploration: **行動価値に基づいて選択確率を計算**し、その確率に従って行動を選択する。

## Boltzman Explorationのアルゴリズム:

以下の手順に従って、行動を選択する。

- 1. 各行動に対する行動価値を計算する。
- 2. 行動価値に基づいて、Boltzmann分布を計算する。
- 3. Boltzmann分布に従って、行動を選択する。

Boltzmann分布の確率密度関数は以下の通り:
(確率密度関数がSoftmax関数になってる...!:thinking:)

$$
P(a) = \frac{e^{Q(a) / \tau}}{\sum_{a'} e^{Q(a') / \tau}}
$$

ここで、

- $P(a)$: 行動 $a$ を選択する確率。
- $Q(a)$: 行動 $a$ に対する行動価値。
- $\tau$: 温度パラメータ。**温度が高いほど確率分布は均等になり、温度が低いほど最も高い行動価値を持つ行動に偏った分布になる**。

## Boltzmann Explorationの課題:

他の探索手法と同様に、Boltzmann Explorationにもいくつか課題がある。

- 1. 過剰探索(Over-exploration)
- 2. 低温度における局所解への収束
- 3. 温度パラメータの調整
- 4. モデルの不確実性の無視
- 5. 報酬の非線形性への対応
  - (これは強化学習の文脈なので、報酬という概念が出てきてる...!:thinking:)
  - 行動価値と報酬の関係性が非線形である場合、このアプローチでは報酬を最適化できないかも...! (線形な関係を仮定した手法なので!)
