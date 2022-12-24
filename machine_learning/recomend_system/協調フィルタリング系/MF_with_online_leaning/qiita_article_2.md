# 1. はじめに

まず始めに本記事は、「Fast Matrix Factrization for Online Recommendation with Implicit Feedback」という論文を読み、内容を自分なりに噛み砕きつつまとめた＋実装してみたものになります。

この論文を読み始めた背景としてはいくつか理由があるのですが、主要な理由の一つが、この論文を読む事で私の感じた課題の解法が得られる、気がした事なんです。

というのも、私は一ヶ月程前からConvMF(Convolutional Matrix Factorization for Document Context-Aware Recommendation)の論文を読んで実装してみているのですが、その際にALSによるMatrix Factirizationの**ハイパーパラメータである$k$(latent vectorの次元数)を大きくすると、パラメータ推定の時間がめちゃめちゃ長くなってしまう**な...と感じていました。
$k$はMFの表現力を高める為に重要なハイパーパラメータなので、ある程度大きくすべき(ex. $k = 100 ~ 200 ?$)だし...。その一方で、新しく観測されたデータを使ってコンスタントにモデルを更新していくスピードも、推薦すべきアイテムに鮮度があるような推薦システムにおいては特に重要そうです...！
そしてConvMFでは、CNN(Convolutional Neural Network)のパートと、ALSによるMF(Matrix Factirization)のパートを交互に学習させるのですが、「CNNパートの学習はGPUを使うなり色々高速化の工夫がありそうだけど、MFパートの学習はどのような工夫をしたら高速化できるんだろう...」と思っていたところに、この論文と出会い、よし読もうとなった訳なんです。
(ちなみConvMFの論文ではExplicit Feedback、本論文ではImplicit Feedbackを扱っています。でもまあ、どちらの論文の手法も、もう一方の種類のデータにも応用できそうな気がします...!)

ちなみに本記事の作成者である私は、非情報系(理系＆MLや統計解析は研究で使ったりする！)の博士学生です。KaggleのPersonalized Recommendationコンペへの参加をきっかけに推薦システムに魅力を感じ、以降、ちょくちょく独学で論文や技術書を読んだり実装してみたりしています。暖かい目で見ていただきつつ、なにか気になった点があればぜひコメントいただけますと嬉しいです：）

# 2. 本論文で提案されたImplicit MF Method

## 2.1. Item-Oriented Weighting on Missing Data 欠損データに対するアイテム指向の重み付け

### 2.1.1. Popularity-aware Weighting Strategy 人気を考慮した重み付け戦略

### 2.1.2. Relationship to Negative Sampling

## 2.2. Fast eALS Learning Algorithm 高速なeALSアルゴリズム

### 2.2.1. Time Complexity

### 2.2.2. Computing the Objective Function

### 2.2.3. Parallel Learning

## 2.3. Online Update

### 2.3.1. Incremental Updating

### 2.3.2. Weight of New Interactions 新規Interactionの重み付け

### 2.3.3. Time Complexity

# 3. 実装してみる

# 4. おわりに

「implicit feedbackに対するALS手法の前置き」と「eALSによる高速化」の内容だけで結構長くなってしまったので、ここで一旦記事を分けようと思います。

このelement-wiseのパラメータ更新の工夫は、Explicit feedbackに対するALSにも適用できそうですね...!
ConvMF(Convolutional Matrix Factorization for Document Context-Aware Recommendation)の場合はどうなんでしょうか...。
少なくともuser latent vector側の更新式は通常のALSと同じなので適用できるとして、item latent vectorの更新式にはCNNの項が入ってくるので...、うーん。
でもまあ、結局は他のパラメータを固定して一つのパラメータを順番に最適化していく点は同じなので、item latent vector側にもelement-wiseなパラメータ更新を適用できそうな気がします。

次の記事では、論文のMain partである、eALSによって高速化された & Online学習が可能なMatrix Factrizationについて理論面をまとめ、試しに実装してみます...!
読んでいただきありがとうございました：）
何か指摘や感想がありましたら、ぜひコメントしていただければ嬉しいです：）
