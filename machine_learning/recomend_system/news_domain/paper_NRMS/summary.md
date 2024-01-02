# NRMS: Neural News Recommendation with Multi-Head Self-Attention

published date: November 2019,
authors: Chuhan Wu, Fangzhao Wu, Suyu Ge, Tao Qi, Yongfeng Huang, Xing Xie
url(paper): https://aclanthology.org/D19-1671/
(勉強会発表者: morinota)

---

n週連続推薦システム系論文読んだシリーズ hoge週目の記事になります。
ちなみにhoge-1週目は [タイトル](url) でした!

## どんなもの?

## 先行研究と比べて何がすごい？

- ニュースとユーザに関する正確な埋め込み表現を学習することは、ニュース推薦における中核タスク。
  - (ここで「正確な」という意味は、「推薦タスクに有用な」とか「特徴をより良く表現した」みたいなイメージ:thinking:)
- 深層学習ベースの既存手法:
  - Okura et al.(2017): Triplet loss損失関数 & auto-encodersでニュース本文からニュース表現を学習し、GRU(RNN系の手法)によって閲読履歴からユーザ表現を学習させてた。
    - 単語間の相互作用や重要度の違いを考慮できない。GRUは計算量が多くて時間がかかる。
  - Wang et al.(2018): knowledge-awareなCNNでニュースタイトルからニュース表現を学習し、閲読履歴のニュースの類似性に基づいてユーザ表現を学習させてた
    - CNNは単語間の長距離の相互作用を考慮できない。閲覧ニュース間の相互作用も考慮できない。

## 技術や手法の肝は？

### 提案手法 NRMSのモチベーション

本論文の提案手法 NRMS は、ニュース推薦に関する4つの洞察に動機づけられている:

- 洞察1: **ニュースタイトルに含まれる単語間の相互作用は、ニュースを理解するのに重要。**
  - ex. 図1において、RocketsとBullsは強い関連性を持っており、これらの単語の組み合わせが対象ニュースの特徴となりうる。
  - (i.e. 単語Aと単語Bが一緒の文章に含まれていることが対象ニュースの特徴を表現する上で重要。特徴量間の相互作用を考慮したいって話だよね:thinking:)
- 洞察2: **ユーザの閲覧履歴に関するニュース間の相互作用は、ユーザを理解するのに重要。**
  - ex. 図1において、2番目のニュースは1番目と3番目のニュースと関連性を持っており、これらのニュースの組み合わせが対象ユーザの興味の特徴となりうる。
- 洞察3: **品質の高いニュース表現を得る上で、ニュースタイトル内の単語によって重要性の高さが異なる**。
  - ex. 図1において、"2018"よりも"NBA"の方が、ニュースの特徴を表現する上で有用そうである(i.e. 情報量が多い)。
- 洞察4: **品質の高いユーザ表現を得る上で、閲覧履歴内のニュースによって重要性の高さが異なる。**
  - ex. 図1において、4番目のニュースよりも1 ~ 3番目のニュースの方が、ユーザの特徴を表現する上で有用そうである(i.e. 情報量が多い)。

上記の**4つの洞察を考慮できる手法**として、本論文ではNRMS (Neural news Recommendation approach with Multi-head Self-attention) を提案している。

### NRMSのアーキテクチャ概要

NRMSのアーキテクチャは、大きく **news encoder** と **user encoder** と **click predictor** の3つのcomponentから構成される:

- news encoder:
  - ニュースタイトルからニュース表現を学習する。
  - 洞察1を考慮するためにmulti-head self-attentionを、洞察3を考慮するためにadditive attentionを採用してる。
- user encoder:
  - ユーザのニュース閲覧履歴からユーザ表現を学習する。
  - 洞察2を考慮するためにmulti-head self-attentionを、洞察4を考慮するためにadditive attentionを採用してる。
- click predictor:
  - ユーザ表現とニュース表現を用いて、ユーザが対象ニュースをクリックする確率を予測する。
  - ここは既存研究に習い、シンプルにdot productを用いてる。他の種類のスコアリング方法も試したが、**ドット積が最も優れた性能と効率を示したらしい**。(効率はそりゃそうだと思うけど、性能も優れてたんだ...!:thinking:)

### News Encoderのアーキテクチャ

News encoderは以下の3層で構成されている:

- 1. word embedding層
- 2. word-level multi-head self-attention層
- 3. word-level additive attention層

#### 1層目はword embedding層:

- 観察可能な振る舞い:
  - 入力: 記事タイトルのテキスト(単語のsequence) $[w_1, w_2, ..., w_M]$ (Mは単語数)
  - 出力: 単語埋め込みベクトルのsequence $[e_1, e_2, ..., e_M]$
- 実装の詳細:
  - 何らかのNLP手法や言語モデルによって各単語を埋め込む。

#### 2層目はword-level multi-head self-attention層:

観察可能な振る舞い:

- 入力: 単語埋め込みベクトルのsequence $[e_1, e_2, ..., e_M]$
- 出力: 単語間の相互作用を考慮した単語表現ベクトルのsequence $[h^{w}_1, h^{w}_2, ..., h^{w}_M]$

実装の詳細:

- k番目のattention headによって得られる、i番目の単語の隠れ表現 $h_{i,k}^{w}$ は以下のように計算される:

$$
\alpha^{k}_{i,j} = \frac{exp(e_{i}^T Q_{k}^{w} e_{j})}{\sum_{m=1}^{M} exp(e_{i}^T Q_{k}^{w} e_{m})}
\tag{1}
$$

$$
\mathbf{h}_{i,k}^{w} = V_{k}^{w} (\sum_{j=1}^{M} \alpha^{k}_{i,j} e_{j})
\tag{2}
$$

- ここで...
  - $Q_{k}^{w}$ と $V_{k}^{w}$ は、k番目のself-attention headの線形投影パラメータ。
  - $alpha_{i,j}^{k}$ は、k番目のattention headによって得られる単語 $w_{i}$ と単語 $w_{j}$ 間のattention weight。
- 最終的なi番目の単語の、単語間の相互作用を考慮した表現 $h_{i}^{w}$ は、h個の別々のself-attention headによって出力された単語表現 $\mathbf{h}_{i,k}^{w}$ のconcatになる。
  - すなわち、 $h_{w}^{i} = [h_{w}^{i,1} ; h_{w}^{i,2} ; ...; h_{w}^{i,h}]$

#### 3層目はword-level additive attention層:

観察可能な振る舞い:

- 入力: 単語間の相互作用を考慮した単語埋め込みベクトルのsequence $[h^{w}_1, h^{w}_2, ..., h^{w}_M]$
- 出力: 単語間の相互作用 & 各単語の重要度を考慮した最終的なニュース埋め込みベクトル $\mathbf{r}$

実装の詳細:

- まずi番目の単語の attention weight $\alpha^{w}_{i}$ は以下のように計算される：
  - (式3はadditive attentionの式。$q_{w}$ と $V_{w}$ と $v_{w}$ は学習可能なパラメータ。一層のFFNになってる。self-attentionと異なり、添字がiだけなのか...!:thinking:)
  - (式4のように、最終的なattention weightはsoftmaxで正規化される)

$$
a^{w}_{i} = q^T_{w} tanh(V_{w} h^{w}_{i} + v_{w})
\tag{3}
$$

$$
\alpha^{w}_{i} = \frac{exp(a^{w}_{i})}{\sum_{j=1}^{M} exp(a^{w}_{j})}
\tag{4}
$$

- ここで...
  - $V_{w}$ と $v_{w}$ は線形投影パラメータ。$q_{w}$ はクエリベクトル。いずれもadditive attentionの学習可能なパラメータ。
- **最終的なニュース表現**は以下。
  - **contextual word representations(2層目の出力)の重み付き合計として定式化**される：

$$
\mathbf{r} = \sum_{i=1}^{M} \alpha^{w}_{i} h^{w}_{i}
\tag{5}
$$

### User Encoderのアーキテクチャ

User encoderは以下の2層で構成されている:

- news-level multi-head self-attention層
- news-level additive attention層

#### 1層目はnews-level multi-head self-attention層:

観察可能な振る舞い:

- 入力: ユーザの閲覧履歴のニュース埋め込み表現のsequence $[r_1, r_2, ..., r_N]$ (Nは閲覧履歴内のニュース数) (各 $r$ は news encoderの3層目の出力を用いる)
- 出力: ニュース間の相互作用を考慮したニュース埋め込み表現のsequence $[h^{n}_1, h^{n}_2, ..., h^{n}_N]$

実装の詳細:

- (基本的にnews encoderの2層目と同じ。ニュースをユーザに、単語をニュースに置き換えたver.)

#### 2層目はnews-level additive attention層:

観察可能な振る舞い:

- 入力: ニュース間の相互作用を考慮したニュース埋め込み表現のsequence $[h^{n}_1, h^{n}_2, ..., h^{n}_N]$
- 出力: ニュース間の相互作用 & 各ニュースの重要度を考慮した最終的なユーザ埋め込みベクトル $\mathbf{u}$

実装の詳細:

- (基本的にnews encoderの3層目と同じ。ニュースをユーザに、単語をニュースに置き換えたver.)

### NRMSの学習方法

- negative sampling技術を使用してpositive exampleとnegative exampleを用意して教師あり学習をする。
  - 具体的には、ユーザによって閲覧された各ニュース(positive sample)について、**同じインプレッションに表示されたがユーザによってクリックされなかったニュース(negative sample)**をK個無作為にサンプリングする。
  - (一般的なimplicit feedbackのpositive sampleしか観測されない状況での未観測アイテムを頑張って工夫してnegative samplingする、という感じではなかった。シンプルでありがたい...!:thinking:)
- positive sampleの事後クリック確率を定義:
  - 1個のpositive newsとK個のnegative newsのクリック確率スコアをそれぞれ $\hat{y}^{+}$ と $[\hat{y}^{-}_{1}, \hat{y}^{-}_{2}, ..., \hat{y}^{-}_{K}]$ とする。
  - スコアをsoftmax関数に通す事で、陽性サンプルの事後クリック確率を計算する:

$$
p_{i} = \frac{exp(y^{+}_{i})}{exp(y^{+}_{i}) + \sum_{j=1}^{K} exp(y^{-}_{j})}
\tag{11}
$$

- 損失関数:
  - ニュースのクリック確率予測問題を、**擬似的な(K + 1)個分類タスクとして定式化**し、損失関数を「全てのpositive sample $S$ の負の対数尤度」として以下のように定式化する
    - (要はmaximum likelihood estimation...!:thinking:)

$$
\mathcal{L} = - \sum_{i \in S} log(p_{i})
\tag{12}
$$

## どうやって有効だと検証した?

MINDデータセットを使ったオフライン実験

- 使用データセット:
  - MINDデータセット(Microsoft News Dataset)を使用。
  - MSN Newsの**1ヶ月間(2018年12月13日から2019年1月12日まで)のログ**から収集した実世界のニュースデータ。
  - 最終週のログはテスト用データ。残りが学習用データ。
  - 学習データのうち、ランダムに10%を検証用データとする。
- 実装の詳細:
  - 単語埋め込みは300次元。(Glove埋め込み)
  - self-attentionのhead数は16。各headの出力は16次元。
  - additive attentionのクエリベクトルの次元数は200。
  - negative sampling比 $K$ は4 (positive sample1つに対して、negative sampleは4つ)。
  - optimizerはAdam。
  - over fittingを防ぐために、単語埋め込みい20%の確率で0ベクトルに置き換えるdropoutを使用。
  - batch sizeは64
- 評価指標:
  - テストデータに対するAUC、MRR、nDCG@5、nDCG@10。
  - 各実験を独立に10回繰り返し、その平均値を報告。
- 比較するベースライン手法:
  - 非deepな推薦手法
  - ニュース間の相互作用を考慮しないdeepな推薦手法
  - ニュース間の相互作用を考慮するdeepな推薦手法

## 議論はある？

### オフライン精度の話

![]()
論文のtable2より引用

結果からわかった事:

- 1. deepな推薦手法は非deepな推薦手法よりもオフライン性能が高かった。
- 2. deepな推薦手法の中でも、ニュース間の相互作用を考慮する手法の方が、考慮しない手法よりもオフライン性能が高かった。
- 3. NRMSは、ニュース間の相互作用を考慮する手法の中でも最もオフライン性能が高かった。

### 時間計算量の話

![]()
論文のtable3より引用

結果からわかった事:

- NRMSは、既存のニュース推薦手法と比較して、時間計算量が小さい。
  - ニュース表現やユーザ表現を学習する際のパラメータサイズが小さいから。
  - また、推論時はニュース表現とユーザ表現のドット積を計算するだけだから。
  - 更にNRMSは、異なるattention headsの隠れ表現 $h_{i}^{hoge}$ を並列に計算することで更に高速化が可能。

### NRMSの各componentsの重要性の話

ablation studyを行った結果からわかった事:

- word-levelとnews-levelのattentionネットワークに関するablation study(figure 3 a):

  - word-levelのattentionが特に性能向上に寄与する事がわかった。
  - また、news-levelのattentionも、word-levelのattentionほどではないが、性能向上に寄与する事がわかった。
  - そして、word-levelとnews-levelのattentionを組み合わせたモデルが最も性能が高かった。

- multi-head self-attentionとadditive attentionに関するablation study(figure 3 b):
  - multi-head self-attentionが性能向上に寄与する事がわかった。
  - また、additive attentionも、multi-head self-attentionほどではないが、性能向上に寄与する事がわかった。
  - そして、multi-head self-attentionとadditive attentionを組み合わせたモデルが最も性能が高かった。

![]()
論文のfigure3より引用

### 今後の拡張性の話

- 単語やニュースのsequenceの順序情報の活用:
  - 実はNRMSは、単語やニュースのsequenceの順序情報を考慮していない。
    - (NRMSだと、attentionに入力する前にpositional encodingみたいな事をやってないので...!:thinking:)
  - (ニュースのsequenceの順序情報を使うってことは、つまりsequential recommenderへ拡張するってことか:thinking:)
- ニュースタイトル以外の属性情報の活用:
  - 特に、self-attentionネットワークの効率性を脅かす可能性のあるニュース本文などの長いsequence情報をいかに効果的に扱うか。

## 次に読むべき論文は？

## お気持ち実装

recboleで実験することを想定して、お気持ち実装。

```python



```
