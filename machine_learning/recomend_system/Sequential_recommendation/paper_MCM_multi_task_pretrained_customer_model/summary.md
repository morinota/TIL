# MCM: A Multi-task Pre-trained Customer Model for Personalization

published date: hogehoge September 2023,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://www.amazon.science/publications/mcm-a-multi-task-pre-trained-customer-model-for-personalization
(勉強会発表者: morinota)

---

## どんなもの?

- パーソナライズ推薦は、各usecaseによって推薦するコンテンツ、推薦対象のユーザ、UI等の条件が異なるが、

## 先行研究と比べて何がすごい？

- GPTの様なBERTベースの事前学習済みモデルは、NLPやCVの領域で成功している。
- 推薦分野では、Sequential推薦の設定下で、session-based推薦のような特定のタスクにおいてBERTベースのモデルが提案されている。しかし、**BERTをつかった大規模な事前学習は、推薦システムの分野ではまだほとんど研究されてない**。
  - (様々な下流タスクにfine-tuning可能な汎用的な事前学習済みモデル、ではなく、特定のタスクに特化したend-to-endなモデルとしての活用 :thinking:)
- 本論文では、**Multi-task pre-trained Customer Model(MCM, マルチタスク事前学習済み顧客モデル?)**を提案している。
  - BERT4Recをベースとしたマルチタスク事前学習済みモデル。
  - Amazonの膨大な行動データを用いて事前学習され、1000万個のパラメータを持つ。
  - オフライン実験の結果、MCMはマルチタスクにおいて、SOTAであるBERT4Recを平均17%上回った。

## 技術や手法の肝は？

### 工夫1: Heterogeneous(異種の) Embedding Module

- 要するに、「ユーザAがアイテムXを購入した」「ユーザBがアイテムYを検索した」等のheterogeneousな各user-item interactionの生の入力情報(raw input)を、embedding lookupに通して、分散表現(distributed representation=embedding=latent vector=hidden representation?)に変換するmodule。
  - (embedding lookup=sparseベクトルをdenceベクトルに変換するプロセス。"lookup" = あるデータセットやテーブルから特定の情報を探し出す操作。じゃあ、embedding lookupは、embedding table的なものから対象entityのembeddingを探し出す操作、みたいなイメージ??:thinking:)
- 具体的なembedding lookupの手順...!
  - raw inputは購入行動と非購入行動を含むheterogeneousな(異種な)interaction sequenceの各interaction $i$(=いろんな種類のアクションのログ)
  - embedding moduleにraw inputを渡す前に、**$i$ を 特徴量 $f_{i}^{j}$ の集合 ($j \in 1, 2, \cdots, |J|$) で表現**する。($|J|$ は各interaction $i$ の特徴量の総数)
    - よって、あるユーザ $c$ (customerのc) の入力sequenceは、$|J|$ 個のsequencesになる。
    - $j$ 番目のsequenceは、j番目の特徴量のsequence。$F^{j} = [f_{1}^{j}, f_{2}^{j}, \cdots, f_{n_i}^{j}]$ の形。
    - 本論文で採用してる特徴量は 5つ。($|J| = 5$)
      - product line(大分類), category(中分類), subcategory(小分類), brand(製品のブランド. 極小分類), token type(interactionの種類。モデルがheterogeneousなinteractionを区別しやすくする為。)
    - 各特徴量 (=各$f_{n}^{j}$ の事?) には固有のembeddingが割り当てられる。
- embedding lookupの後の手順:
  - embedding lookupを経て、あるユーザの入力sequenceは $|J|$ 個のsequencesに変換された状態。
  - $|J|$ 個のsequencesにaverage poolingを行い、1個のsequence $\mathbf{E}$ を作る: $\mathbf{E} = [\mathbf{e}_1, \mathbf{e}_2, \cdots, \mathbf{e}_{n_i}]$
    - つまり、 $\mathbf{e}_1 = ave[f_{1}^{1}, f_{1}^{2}, \cdots, f_{1}^{|J|}]$ って事かな:thinking:
  - その後、position embedding を追加して、最終的なembedding moduleの出力sequence $\mathbf{H}$ を得る: $\mathbf{H} = \mathbf{E} + \mathbf{P}$
    - (BERTなどのself-attention-basedなモデルは、sequenceの順番を参照する為に position embedding を必要とするので...!)
    - position embedding sequence $\mathbf{P}$ は学習可能なパラメータ(ランダムに初期化)。

### 工夫2: Task-AwareなAttentional Readout Module

- Embedding Module と Readout Module(i.e. score prediction module?:thinking:) の中間に位置するモジュール Sequential Encoding Module は BERT4Recと同じなので割愛する。
  - (Sequential Encoding Moduleについては、BERT4Recの元論文 or [n週連続hogehoge]()等 を参照)
- Readout Module の入力: **元の入力sequenceと同じ長さの隠れ表現sequence**(=Sequential Encoding Module の出力)
  - (つまりEmbedding Moduleの出力sequence $\mathbf{H}$ とも同じ長さ!)
- 先行研究BERT4RecのReadout Moduleではmulti-taskに対応できないかもしれない話:
  - BERT4Recでは、**入力sequenceの最後尾token**(=推論時にsequenceの最後に追加する特殊token "mask":thinking:)の隠れ表現を用いて、推薦候補アイテムのembeddingとの内積を計算して、アイテムスコア(next-item確率!)を計算してた。
  - ただ、最後尾tokenの隠れ表現はユーザの行動sequence全体の傾向を表すfixedな表現である。(ここで、fixed = 固定された表現とは、たぶん各下流タスクに合わせて変更できるような柔軟性がない表現、みたいな認識:thinking:)
  - -> **各推薦タスクにおける推薦候補アイテムやタスクの特徴の違いを考慮していない**為、これは最適とは言えない可能性あり(=たぶんmulti-taskなモデルを目指してるから??:thinking:)
  - 異なる推薦タスクは、ユーザの行動sequence全体の中の、異なる一部の行動に強く関連しているかもしれないので。
- 提案手法MCMでは、task-awareな新しいattentional readout modulを提案。
  - (task-awareな = 各タスクの特徴に合わせて調整可能な?:thinking:)
  - 各タスクに特化した隠れ表現を生成する為に、attentionメカニズムを採用する。
    - attentionによって、各タスクと 各タスクの推薦候補アイテムが、**隠れ表現sequence(=Readout Moduleの入力sequence = Sequential Encoding Moduleの出力sequence)の異なる部分sequenceに注目できるように**する。

具体的には、attentional readout (=attentionによるscore prediction ...!:thinking:)操作は以下のように行われる。

$$
a_{w, i} = \frac{\exp((\mathbf{e}_{w})^T \mathbf{h}_{i})}{\sum_{i} \exp((\mathbf{e}_{w})^T \mathbf{h}_{i})}
\\
\mathbf{r}_{w} = \sum_{i} a_{w, i} \cdot \mathbf{h}_{i}
\tag{2}
$$

ここで、

- 隠れ表現sequenceの $i$ 番目のembedding を $\mathbf{h}_{i}$ とする。
  - (Embedding Moduleの出力も $\mathbf{H}$ で表記してたから分かりづらい...!:thinking:)
- あるタスクの特定のitem (=推薦候補アイテム? groud-truthアイテム?) $w$ に対するembeddingを $\mathbf{e}_{w}$ とする。
- $\mathbf{r}_w$ は、あるタスクの推薦候補アイテム $w$ 固有のreadout moduleへの入力sequenceの隠れ表現。

あるタスクにおける推薦候補アイテム $w$ の予測スコアは次のようになる(シンプルにdot-product):

$$
s(w) = \mathbf{r}_{w}^T \mathbf{e}_{w}
\tag{3}
$$

最終的な分布(=next-itemの確率質量分布関数:thinking:)を生成するために、スコア $s(w)$ に対してソフトマックス演算が実行される。

### 工夫3: prefix-augmentationによるMCMの事前学習(どうやって事前学習させるかの話)

- 先行研究 BERT4Recでは、**masked languamge model** というNLPでよく使われるaugumentation手法を採用している。
  - (=要はmasked-item-predictionの学習タスク。元論文だとClozeタスクと呼ばれてたやつ:thinking:)
  - (next-item(token)-predictionやnext-sentence-predictionと同様に「学習タスクの種類」という認識だけど、augumentation手法と表現するのか。確かに、いずれの手法も入力sequenceからtraining exampleを作ってるので、data augumentationと言えるのか...??:thinking:)
  - masked languamge model(i.e. masked-item-prediction)は、言語モデリングには適しているが、**推薦タスクでは将来の情報が漏れてしまう為、問題がある**と本論文では主張。(=要は、bi-directionalなモデルであるBERT4Recの場合は、将来の情報が漏れてしまうので学習タスクを簡単に解けてしまい、有効なパラメータを見つけられない、って話:thinking:)
    - (この件は確かBERT4Recの論文では、まずmasked-item-predictionタスクで学習させて、その後にfine-tuningとして最後尾のnext-item-predictionタスクを学習させる事で対処を試みてた:thinking:)
- MCMでは、masked-item-predictionに変わる新しいaugmentation手法(i.e. 学習タスク)を提案する = "**random prefix augmentation**"
  - 具体的には、入力sequence全体からランダムに prefix (=部分sequence)をサンプリングし、モデルに最後のitem (=入力sequenceの最後? それともサンプリングした部分sequenceの最後??:thinking:)を予測させる。
  - ex) 元の入力sequenceが $[i_1,i_2,i_3]$ の場合、有効なprefixは $[i_1]$ と $[i_1,i_2]$ になる。(つまり予測すべきラベル = 入力sequenceの最後のitem $i_3$ ってこと?:thinking:)
  - メモリを節約するため、augumentation処理はデータの前処理中ではなく、batch時(=mini batch学習の各batch実行時:thinking:)に実行される。

random prefix augmentationにおける各prefixの損失関数は、label item(=入力sequenceの最後のitem)の負の対数尤度として定義される:

$$
\mathcal{L} = - \log P(i = i_{gt}|S)
\tag{4}
$$

ここで、

- $i_{gt}$ は ground-truth item (=つまり入力sequenceの最後のアイテムの正解アイテム)
- $S$ は、最後のアイテム以外の全てのアイテムを含む入力Sequence(=これは実際にはprefixであり、入力sequenceの部分sequenceなのかな。モデルに入力するのはprefixだけだと思うけど、表記する上では$S$ を書く??:thinking:)
- $P(i|S)$ は、モデルに $S$ を入力した際に出力される item $i$ のnext item確率。(式(3)で得られるやつ)
- muiti-task learningでは、全てのタスクの損失が合計される。(予測すべきラベルがitem_idのタスクと、categoryのタスクと、subcategoryのタスクの損失が合計される?)

## どうやって有効だと検証した?

- オフライン実験のデータセット:
  - Amazonの6年間の顧客履歴からサンプリングしたユーザ行動データを使用。
  - 40Mのユーザと10Bのinteractionで構成される。
  - 行動sequenceには3種類のheterogeneous interactionが含まれる:
    - アイテムの購入, クリック, valuable actions(=たぶん検索とか、その他のアクション:thinking:)
    - 各interactionには、アイテムのカテゴリカルな特徴量を含む。
      - なお、これらの特徴量はモデルを訓練するタスクでも使用する(next-item-predictionだけでなく、next-category-predictionでも学習するってことっぽい:thinking:)
- モデル性能の評価方法:
  - データセットを**時間毎に**(大事:thinking:)学習用、検証用、テスト用に分割する。
  - 評価指標には ランキングmetricsを使用(主にNDCG, recall, precision)
- モデルの実装:
  - BERT encoderの設定: Transformerブロック数 $L = 3$, ヘッダー数 $h = 4$, 最大sequence長 $N=3$
    - (うんうん、推薦用のarchitectureは小さくて良いんだよね!:thinking:)

## 議論はある？

### モデル性能の比較結果

![figure1]()

- MCMとBERT4Recの性能比較の結果:
  - MCM_final はbert4recを約11%大幅に上回った。
- また、 MCM_Single と MCM_MTL という2つのvariantを用いて、MCMモデルのablation実験も行った。
  - MCM_final: 工夫1 ~ 3の全てを採用したMCMモデル。
  - MCM_Single: 工夫1のみ採用したMCMモデル。
  - MCM_MTL: 工夫1と工夫2を採用したMCMモデル。
- 結果として、特に工夫1が最も性能向上に寄与する事が示された。工夫2のMTL(multi-task learning)と工夫3のprefix augumentationも性能向上に寄与している事がわかった。
  - (各モデルの性能の差分を取っての判断かな。BERT4RecとMCM_Singleの差が最も大きいので:thinking:)

### MCMの拡張性の実験結果

- MCMの柔軟性と拡張性を実証するために、next-action推薦のusecaseについて、MCMをfine-tuningする事で、どのような性能を発揮するか実験を行った。
  - このタスクは、インセンティブ(ex. キャッシュバックなど)を提供することで、顧客に1つのアクションタスクを推薦することを目的としている。
    - (じゃあこのタスクの推薦コンテンツは、「〇〇アクションをしてくれたら△△を提供するよ!」という内容であり、ユーザが実際にそのアクションをしたか否か = conversionしたかどうかが正解ラベルとしてある、ようなケースかな:thinking:)
    - 推薦候補のアクションタスクは全部で28種類(=next-action推薦の行動空間の大きさ:thinking:)
      - ex. 新しい商品ラインから商品を購入する、カメラ検索を試す、ビデオ配信サービスを試す、etc.
- 3つを比較:
  - GBDT: treeベースのタスク予測モデル(分類モデル的な?)
  - MCM: 事前学習しただけのやつ。
  - MCM_finetuned: 事前学習 + fine-tuningしたやつ。
    - 具体的には、sequential encoderの上に新しいヘッドを追加し、インセンティブ効果を予測し、インセンティブ下の顧客行動データ(30Kアクションのクリックとconversionの記録)を使ってモデルをfine-tuningする。
- 結果:
  - MCM は GBDT の conversion NDCG を25% 上回り、MCM_finetunedはMCMのconversion NDCG を35% 上回った。
  - MCM_finetuned は GBDTモデルをconversion rateを60%以上改善した。(あれ?これは本番環境でのABテストっぽい??:thinking:)

## 次に読むべき論文は？
