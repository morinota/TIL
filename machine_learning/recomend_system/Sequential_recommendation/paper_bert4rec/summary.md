# BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer

published date: 21 August 2019,
authors: Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, Peng Jiang
url(paper): https://arxiv.org/abs/1904.06690
(勉強会発表者: morinota)

---

## どんなもの?

- Amazonの2019年のhogehoge。
- sequential推薦タスクにおけるいくつかのベンチマークデータセットで、当時のSOTAを達成。

## 先行研究と比べて何がすごい?

### Sequential推薦についての説明:

- ユーザの興味を正確に把握する事は、効果的な推薦システムを作る上で重要。
- しかし多くの実世界のアプリケーションでは、**ユーザの現在の興味は、過去の過去の行動に影響され、本質的にdynamicでevolivingである**。
- このようなdynamicに変化するユーザの興味をモデル化する為に、ユーザの過去のinteractionsに基づいてsequentialな推薦を行う手法が提案 = Sequential推薦。

### Sequential推薦の既存研究における、手法の発展の流れ:

手法の発展の流れは以下の様な感じ

- マルコフ連鎖モデルを活用(推薦を逐次最適化問題とみなす)
- -> MF(=協調フィルタリング手法の一つ)とMCモデルの合せ技(Factorizing Personalized Markov Chains, etc.)
- -> RNN系手法(ex. GRU4Rec, DREAM, user-based GRU, attention-based GRU, etc. )やCNN系手法(ex. Carser)で、ユーザ行動履歴をベクトル(=user preference representation)にencode
  - GRU4RECやCaserは他のsequential recommenderの論文のベースラインとして出てきた気がする:thinking:
  - attenitionメカニズムをオリジナルモデルのattitional componentとして採用する手法も出てきてる。
- -> self-attentionに基づく手法(ex. SASRec)
  - (SASRecはself-attentionを使ったsequential recommenderで有名なやつ! Transformter decoderを使った手法で、本論文時点でいくつかのベンチマークデータセットでSOTAを達成してる:thinking:)
- **しかし、上記の既存研究はいずれも、uni-directionlな(left-to-rightな)sequentialモデル**である。

### Sequential推薦はuni-directionlモデルは最適ではないという話

- 本論文では、以下の２つの制限から、**uni-directionalなモデルは逐次推薦タスクに適したuser preference表現を学習するには不十分**であると主張。
  - 制限1: uni-directionalなモデルでは、各interactionがそれよりも過去のinteractionsからの情報しか考慮できないため、hidden representationの品質が制限される。
  - 制限2: uni-directionalなモデルは、**rigid order assumption (厳密な順序の仮定??)**を満たすテキストデータや時系列データ等には有効。しかし、**実アプリケーション上のユーザ行動は必ずしもその仮定を満たさない**。
    - (テキストや時系列データと比べて、実アプリケーション上のユーザ行動は、Sequence内のノイズがとても多く含まれているから、ridgidly ordered sequenceを前提としたuni-directionalなモデルは最適ではない、みたいな話かな:thinking:)
- よって本論文では、**uni-directionalではなくbi-directionalなモデル(要はBERTのような bi-directional self-attention model)を採用したBERT4Rec**を提案し、Sequential推薦タスクにより適したuser preference 表現の学習を目指す。
  - モデルの学習には、Clozeタスク(=要は、BERTの事前学習タスクの1つ、masked-item-predictionの認識:thinking:)を採用。

## 技術や手法の肝は？

### BERT4Recのアーキテクチャ

### BERT4Recの学習(Clozeタスクについて)

- Clozeタスクの利点
- Clozeタスクの欠点: 最終タスク(=Sequential推薦=next-item-prediction的なタスク)と整合性がない事

### BERT4Recの推論

## どうやって有効だと検証した?

- 4種のベンチマークデータセットによる、オフライン実験で評価してた。

## 議論はある？

### BERT4Rec vs ベースライン手法の推薦性能の比較

#### 疑問1: BERT4Recの性能の高さはbi-directionalモデルだから? それともClozeタスクを学習させてるから?

#### 疑問2: なぜ、どのようにbi-directionalモデルはuni-directionalモデルよりも性能が良い??

### 各ハイパーパラメータの影響

#### hidden representation の次元数 $d$ の影響

![figure3]()

#### Clozeタスクのmask proprtion $\rho$ の影響

![figure4]()

#### sequence最大長 $N$ の影響

![table4]()

### Ablation(切除)実験

#### PE(positional embedding)の有無の影響

#### PFFN(Position-wise Feed Forward Network)の有無の影響

#### LN(), RC(), Dropoutの有無の影響

#### Transformer Layerの数 $L$ の影響

#### multi-head attettionのhead数 $h$ の影響

### 今後の拡張性:

- 1. BERT4Rec自体は、ID-basedな(ID-onlyな)手法。様々なアイテムの特徴量を組み込む事で表現力の向上が見込める。
- 2. **ユーザが複数のセッションを持っている場合**、user componentをモデルに導入する事で、ユーザモデリングの能力の向上が見込める。(同一ユーザの複数のsessionの関連性を考慮するって事か...!:thinking:)

## 次に読むべき論文は？

## お気持ち実装
