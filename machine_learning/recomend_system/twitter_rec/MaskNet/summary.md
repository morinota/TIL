# MaskNet: Introducing Feature-Wise Multiplication to CTR Ranking Models by Instance-Guided Mask

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

## どんなもの?

- twitterの個別化推薦システム内のrankerモデル(i.e. 2-stages推薦の2ステップ目!)として使われていた(今も?)CTR予測モデル MaskNet を提案した論文。

## 先行研究と比べて何がすごい？

## 技術や手法の肝は？

### MaskNetのモデルアーキテクチャ

#### Embedding layerについて

#### Instance-Guided Maskについて

#### MaskBlockについて

### 二種類のMaskNetモデル

### MaskNetの学習方法

## どうやって有効だと検証した?

以下の4つのresearch questionsへの回答を目的として、オフライン実験を行った。

- RQ1: MaskBlockに基づく提案手法 MaskNet は、既存のdeep learningベースのCTR予測モデルよりも予測性能が高いか?
- RQ2: MaskBlockアーキテクチャにおける各Componentsの有効性は? **効果的なランキングシステムを構築するために必要なのか**??
- RQ3: MaskNetのハイパーパラメータはどのように予測性能に影響するか?
- RQ4: MaskBlock内のInstance-Guided Maskは、**入力データに応じて重要な要素を強調**できているのか??(i.e. 想定通りに機能してくれているか?)

以下は、オフライン実験の設定:

- 使用するデータセット達:
  - Criteoデータセット:
    - ユーザへの広告表示とクリックフィードバックからなるデータセット。
  - Malwareデータセット:
    - MicrosoftのMalware予測で公開されたKaggleコンペのデータセット。CTR予測タスクと同様に2値分類タスクとして定式化できるため採用した。
  - Avazuデータセット:
    - Criteo同様に、ユーザへの広告表示とクリックフィードバックからなるデータセット。
- 学習 & テスト用データの分割方法:
  - training, validation, testの割合は8:1:1で、ランダムにインスタンスを分割した。
  - (**時系列に沿ってデータを分割した方が良さそう**...!:thinking:)
- オフライン評価指標:
  - 1. AUC (そうか、CTR予測タスクだから、必ずしもランキング指標じゃなくてもいいのか:thinking:)
  - 2. 「RelaImp」= **ベースラインモデルに対する相対的なAUCの改善度合い**。
    - (数式中の0.5という数値は、random strategyによるAUCの理論値を意味する。)

$$
RelaImp = \frac{AUC(Measured Model) - 0.5}{AUC(Base model) - 0.5} - 1
\tag{20}
$$

- ベースラインモデル:
  - 既存のdeep learningベースのCTR予測モデル達(FM, DNN, DeepFM, Deep&Cross Network(DCN), xDeepFM, AutoInt Model)
- 実装の詳細:
  - バッチサイズ=1024, Adam optimizer, learning rate=0.001
  - 全てのモデルでfield embeddingの次元数を10に固定。
  - DNN部分を持つモデルでは、隠れ層の深さを3に固定。1層辺りのニューロン数を400に固定。活性化関数は全てReLUで固定。
  - MaskBlockのハイパーパラメータ:
    - Instance-Guided Maskのreduction ratio(縮小率)を2に固定。

## 議論はある？

### オフライン性能の比較

- 結果(表2)からわかったこと:
  - (1) hogehoge
  - (2) hogehoge

### abration studyによるMaskブロックの各componentsの有効性評価

- MaskBlockの各componentsの効果を理解するために、MaskBlockの主要componentsであるmask module, レイヤー正規化(LN)、feed forward層(FFN)の有無を変化させたモデルを作成し、オフライン評価を行った。
- 結果(表3)からわかったこと:
  - (1) **instance-guided maskとレイヤー正規化のどちらかを削除するとモデルの性能が低下した**
    - -> 両componentsはMaskBlockの有効性を高めるために重要な役割を果たしている。
  - (2) feed forward層を削除すると、パラレルモデルでは大きな影響はないが、シリアルモデルでは性能が劇的に低下した。

### MaskNetの各ハイパーパラメータの影響評価

- 1つのハイパーパラメータを変更し、他の設定を維持したまま実験を行った。
- 特徴量埋め込みの次元数の影響(表4):
  - hoge
- MaskBlock数の影響(表5):
  - hoge
- instance-guided maskのreduction ratio(縮小率)の影響(表6):
  - hoge

## 次に読むべき論文は？

## お気持ち実装
