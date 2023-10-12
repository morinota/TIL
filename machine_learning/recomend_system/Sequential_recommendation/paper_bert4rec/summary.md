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

### BERT4Recのモデルアーキテクチャ

![figure 1]()

- BERT4Recは、図1bの様に $L$ 個のTransformer層(ブロック?)を重ねた Transformer Encoder で構成される。(要はBERTと同じモデルアーキテクチャ)
- 図1dのRNNベースの手法との違い:
  - 図1dのRNNベースの手法ではsequence内の各位置の情報を段階的に前方に伝えて学習させる。一方で図1bのBERT4Recや図1cのSASRecのような self-attention ベースの手法はsequence内の各位置の情報を直接補足する。
  - またRNNベースの手法と比較してself-attentionは並列化が簡単。
- 図1cのSASRecとの違い:
  - 同じself-attentionベースの手法でも、SASRecはleft-to-rightなuni-directionalなself-attentionを採用しており、BERT4Recはbi-directionalなself-attentionを採用している。

以下で、Transformerブロックの説明をまとめておく(論文にも書かれてたので復習も兼ねて!)

#### Transformer layer (Block?)

- 図1bに示す様に、長さ $t$ の入力sequenceが与えられると、Transformer層の適用によって、sequence内の各position $i$ に対して、各Transformer層 $l$ で hidden representation $\mathbf{h}^{l}_{i}$ を計算する。
  - $\mathbf{h}^{l}_{i} \in \mathbb{R}^{d}$ を積み重ねた行列を $\mathbf{H}^{l} \in \mathbb{R}^{t \times d}$ と表記。
- 図1aに示す様に、Transformer層 ($Trm$ と表記) は 2つのsub layersを含む: Multi-Head Self-Attention 層 ($MH$ と表記)と Position-wise Feed-Forward Network 層($PFFN$ と表記)。

#### Multi-Head Self-Attention 層

- attentionメカニズムは、様々なタスクにおける sequence modeling の不可欠な要素。**sequence内の距離に関係なく**、ペア間の依存関係を捉えることができる。
- 既存研究から、異なる位置にある**異なるrepresentation subspaces(表現部分空間?)からの情報に共同で注意を向けることが有益**である事が示されている為、単一のattentionよりもmulti-head attentionが採用される事が多い。(これがmulti-head attetionを採用する理由なのか...!:thinking:)
- multi-head attentionの振る舞い:
  - まず、入力表現 $\mathbf{H}^{l}$ を学習可能な異なる $h$ 個のlinear projection層 (i.e. 3h個の投影行列)に通して、$h$ 個の部分空間に線形投影する。($l$ 番目の隠れ表現が入力ってことは、$l+1$ 番目のTransformerブロクを想定してる??:thinking:)
  - 次に、$h$ 個のself-attetion関数を並列に適用して $h$ 個の出力表現を生成する。
  - 最後に、$h$ 個の出力表現を連結した上で、1個のlinear projection層に通し、最終的な出力表現 $MH(\mathbf{H}^{l})$ を得る。

$$
MH(\mathbf{H}^l) = [head_1;head_2; \cdots, ;head_{h}] \mathbf{W}^O
\\
head_i = Attention(\mathbf{H}^l \mathbf{W}^Q_{i}, \mathbf{H}^l \mathbf{W}^K_{i}, \mathbf{H}^l \mathbf{W}^V_{i})
\tag{1}
$$

- ここで、各headの投影行列 $\mathbf{W}^Q_i \in \mathbb{R}^{d × d/h}$, $\mathbf{W}^K_i \in \mathbb{R}^{d × d/h}$, $\mathbf{W}^V_i \in \mathbb{R}^{d × d/h}$ と、全headの出力表現を結合したあとに通す投影行列 $\mathbf{W}^O \in \mathbb{R}^{d×d}$ は学習可能なパラメータ。

  - (注意: ここの添字 $i$ はsequence内のpositionではなく、各headを識別する為の添字!:thinking:)
  - (注意: 各Transformer層で、これらの投影行列は共有していない! 簡略化の為に省略しているが、実際には添字 $l$ が付く!:thinking:)

- $Attention$ 関数にはScaled Dot-Product Attentionを採用:

$$
Attention(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = softmax(\frac{QK^T}{\sqrt{d/h}}) V
\tag{2}
$$

- ここで、Query $\mathbf{Q}$、Key $\mathbf{K}$、Value $\mathbf{V}$ は、各headの投影行列によって同じ行列 $\mathbf{H}^l$ から線形投影されるもの。
- 温度 $\sqrt{d/h}$ は、極端に小さな勾配を避けるために、よりソフトなattention分布を作り出すために導入されている[16, 52]。(うんうん、Transformer論文でやったやつ:thinking:。softmax関数の温度パラメータみたいな...!:thinking:)

#### Position-wise Feed-Forward Network 層

- 上述した通り、self-attentionサブレイヤーは主に**線形投影(linear projection)に基づいている**。(このパートだけだと線形モデル...!)
  - -> **モデルに非線形性と、異なる次元間(=$d$ 次元の隠れ表現の各次元の意味!:thinking:)の相互作用を持たせるために**、self-attentionサブレイヤーの出力に対して、PFFNを適用する。
  - (Position-wise = sequence内の各positionで別々に、かつ同一に!:thinking:)
- PFFNは、2つのアフィン変換と、その間のGELU(Gaussian Error Linear Unit)活性化関数からなる。
  - (アフィン変換 = 線形変換と平行移動の組み合わせによる図形や形状の変形方法らしい...! 要は重みを乗じてbias項を足す、って話か!:thinking:)
  - (GELU活性化関数: Gaussianなので正規分布の累積分布関数を使って入力を0 ~ 1の範囲に滑らかにするやつっぽい。じゃあ形はsigmoid関数と似てそう??:thinking:) (BERTとOpenAI GPTの論文に従って採用したらしい。)

$$
PFFN(\mathbf{H}^l) = [FFN(\mathbf{h}^l_1)^T; \cdots; FFN(\mathbf{h}^l_t)^T]^T
\\
FFN(\mathbf{x}) = GELU(\mathbf{x}\mathbf{W}^1 + \mathbf{b}^1)\mathbf{W}^2 + \mathbf{b}^2
\\
GELU(x) = x \Phi(x)
\tag{3}
$$

- ここで、$\Phi(x)$ は標準ガウス分布の累積分布関数。
- $W^(1) \in \mathbb{R}^{d \times 4d}$, $W^(2) \in \mathbb{R}^{4d×\times d}$, $\mathbf{b}^(1) \in \mathbb{R}^{4d}$ および $\mathbf{b}^(2) \in \mathbb{R}^{d}$ は学習可能なパラメータであり、**すべてのposition(=sequence内のposition $1 ~ t$!!)で共有される**(=これがPosition-wiseな点!)。
- (注意: 各Transformer層でこれらのパラメータは共有していない! 簡略化の為に省略しているが、実際には添字 $l$ が付く!:thinking:)

#### サブレイヤー間の接続

- self-attentionのレイヤーを重ねる事で、より複雑な表現を学習できる。しかし、ネットワークが深くなるにつれて学習が難しくなる。
- そこで図1aのような工夫を行う:
  - 2つのサブレイヤーそれぞれの周囲に**残差接続(residual connection)[9]**を採用。
  - **レイヤー正規化[1]**を使用し、同じレイヤーにあるすべての隠れユニットの入力を正規化する(大きさを揃えるってこと??)。
  - 正規化する前に、各サブレイヤーの出力にドロップアウトを適用。
- よって、各サブレイヤーの出力は $LN(x + Dropout(sublayer(x)))$ となる.
  - $sublayer(\cdot)$ はサブレイヤー自身の関数。$LN$ はレイヤー正規化関数。
  - (3つの工夫が何もない場合は、出力は $sublayer(x)$ だけになるはず。じゃあ $x$ を足しているのがresidual connectionなのか :thinking:)
- 要するに、BERT4Rec は各層の隠れ表現を以下のように洗練する:

$$
\mathbf{H}^{l} = Trm(\mathbf{H}^{l-1}), \forall i \in [1, \cdots, L]
\tag{4}
$$

(↑前のTransformerブロックの出力が、次のTransformerブロックの入力になる)

$$
Trm(\mathbf{H}^{l-1}) = LN(A^{l-1} + Dropout(PFFN(A^{l-1})))
\tag{5}
$$

(↑PFFNサブレイヤーの出力表現に、DropoutとResidual Connectionとレイヤー正規化を適用したものが、ある1つのTransformerブロックの出力表現になる。)

$$
A^{l-1} = LN(\mathbf{H}^{l} + Dropout(MH(\mathbf{H}^{l-1})))
\tag{6}
$$

(↑MHサブレイヤーの出力表現に、DropoutとResidual Connectionとレイヤー正規化を適用したものが、PFFNサブレイヤーへの入力表現になる)

### BERT4Recの学習(Clozeタスクについて)

- BERT4Recは、SASRec等のnext-item-predictionタスクではなく、Clozeタスクによって学習される。

- Clozeタスクの利点:
- ## BERTと異なる点:

### BERT4Recの推論

- BERT4Recの学習に用いるClozeタスクの欠点: 最終タスク(=Sequential推薦=next-item-prediction的なタスク)と整合性がない事。
- 推論時は sequenceの最後尾に[]tokenを追加し、

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
