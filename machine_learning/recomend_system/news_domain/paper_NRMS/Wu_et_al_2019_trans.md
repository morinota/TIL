## 0.1. link リンク

https://aclanthology.org/D19-1671/
[empty]

## 0.2. title タイトル

(NRMS) Neural News Recommendation with Multi-Head Self-Attention
多頭自己注意を用いたニューラル・ニュース推薦

## 0.3. abstract 抄録

News recommendation can help users find interested news and alleviate information overload.
ニュースのレコメンデーションは、ユーザが興味のあるニュースを見つけ、情報過多を緩和するのに役立つ。
Precisely modeling news and users is critical for news recommendation, and capturing the contexts of words and news is important to learn news and user representations.
ニュースとユーザを正確にモデル化(=encode?)することはニュース推薦のために重要であり、言葉とニュースの文脈を捉えることはニュースとユーザの表現を学習するために重要である。
In this paper, we propose a neural news recommendation approach with multi-head selfattention (NRMS).
本稿では、多頭自己注意を用いたニューラル・ニュース推薦アプローチ（NRMS）を提案する。
The core of our approach is a news encoder and a user encoder.
**我々のアプローチの中核は、ニュース・エンコーダーとユーザー・エンコーダーである。**
In the news encoder, we use multi-head self-attentions to learn news representations from news titles by modeling the interactions between words.
ニュースエンコーダでは、単語間の相互作用をモデル化することにより、ニュースタイトルからニュース表現を学習するために、多頭自己注意を用いる。
In the user encoder, we learn representations of users from their browsed news and use multihead self-attention to capture the relatedness between the news.
ユーザーエンコーダでは、**閲覧したニュースからユーザーの表現を学習**し、マルチヘッド自己注意を用いてニュース間の関連性を捉える。
Besides, we apply additive attention to learn more informative news and user representations by selecting important words and news.
さらに、additive attentionを適用して、重要な単語やニュースを選択することで、より有益なニュースやユーザ表現を学習する。
Experiments on a realworld dataset validate the effectiveness and efficiency of our approach.
実世界のデータセットを用いた実験により、本アプローチの有効性と効率性が検証された。

# 1. Introduction はじめに

Online news platforms such as Google News1 and MSN News2 have attracted many users to read news online (Das et al., 2007).
Google News1やMSN News2のようなオンライン・ニュース・プラットフォームは、オンラインでニュースを読む多くのユーザーを惹きつけている（Das et al, 2007）。
Massive news articles are generated everyday and it is impossible for users to read all news to find their interested content (Phelan et al., 2011).
毎日大量のニュース記事が生成され、**ユーザが興味のあるコンテンツを見つけるためにすべてのニュースを読むことは不可能**である（Phelan et al, 2011）。
Thus, personalized news recommendation is very important for online news platforms to target user interests and alleviate information overload (IJntema et al., 2010).
したがって、オンライン・ニュース・プラットフォームにとって、**ユーザの関心に的を絞り、情報過多を緩和するため**に、パーソナライズされたニュース推薦が非常に重要である（IJntema et al.）

Learning accurate representations of news and users are two core tasks in news recommendation (Okura et al., 2017).
ニュースとユーザに関する正確な表現(=embedding?)を学習することは、ニュース推薦における2つの中核タスクである（Okura et al, 2017）。
Several deep learning based methods have been proposed for these tasks (?Kumar et al., 2017; Khattar et al., 2018; Wu et al., 2019b,c,a; Zhu et al., 2019; An et al., 2019).
これらのタスクに対して、いくつかの深層学習に基づく手法が提案されている（?Kumar et al., 2017; Khattar et al., 2018; Wu et al., 2019b,c,a; Zhu et al., 2019; An et al.）
For example, Okura et al.(2017) proposed to learn news representations from news bodies via auto-encoders, and learn representations of users from their browsed news via GRU.
例えば、Okura et al.(2017)は、オートエンコーダによってニュース本文からニュース表現を学習し、**GRUによって閲覧したニュースからユーザの表現を学習する**ことを提案している。(あ、okura et al のuser encoderはRNN系手法だったのか...!)
However, GRU is quite time-consuming, and their method cannot capture the contexts of words.
しかし、GRUは非常に時間がかかり、その方法では単語の文脈を捉えることができない。
Wang et al.(2018) proposed to learn news representations from news titles via a knowledge-aware convolutional neural network (CNN), and learn representations of users based on the similarities between candidate news and their browsed news.
Wangら(2018)は、知識認識畳み込みニューラルネットワーク(CNN)を介してニュースタイトルからニュース表現を学習し、**候補ニュースと閲覧したニュースとの類似性に基づいてユーザの表現を学習する**ことを提案した。(これはシンプルに内積とるような感じかな?)
However, CNN cannot capture the long-distance contexts of words, and their method cannot model the relatedness between browsed news.
しかし、CNNは単語の長距離文脈を捉えることができず、彼らの方法では閲覧したニュース間の関連性をモデル化することができない。

Our work is motivated by several observations.
私たちの研究は、いくつかの観察によって動機づけられている。
First, the interactions between words in news title are important for understanding the news.
まず、ニュースのタイトルに含まれる単語間の相互作用は、ニュースを理解する上で重要である。(このあたりはnews encoderの話なので、LLM時代にはあんまり気にしなくて良さそう。)
For example, in Fig.1, the word “Rockets” has strong relatedness with “Bulls”.
例えば図1では、"Rockets "という単語は "Bulls "と強い関連性を持っている。
Besides, a word may interact with multiple words, e.g., “Rockets” also has semantic interactions with “trade”.
さらに、ある単語が複数の単語と相互作用することもある。例えば、「ロケッツ」は「トレード」とも意味的に相互作用する。
Second, different news articles browsed by the same user may also have relatedness.
第二に、同じユーザが閲覧した異なるニュース記事にも関連性があるかもしれない。
For example, in Fig.1 the second news is related to the first and the third news.
例えば図1では、2番目のニュースは1番目と3番目のニュースに関連している。
Third, different words may have different importance in representing news.
第三に、ニュースを表現する上で、単語によって重要性が異なる場合がある。
In Fig.1, the word “NBA” is more informative than “2018”.
図1では、"2018 "よりも "NBA "の方が情報量が多い。
Besides, different news articles browsed by the same user may also have different importance in representing this user.
さらに、**同じユーザが閲覧したニュース記事でも、そのユーザを表す重要度が異なる場合がある**。(これはuser encoderの部分...!)
For example, the first three news articles are more informative than the last one.
例えば、最初の3つのニュース記事は最後の1つよりも情報量が多い。

In this paper, we propose a neural news recommendation approach with multi-head selfattention (NRMS).
本稿では、multi-head self-attentionを用いたニューラル・ニュース推薦アプローチ（NRMS）を提案する。
The core of our approach is a news encoder and a user encoder.
我々のアプローチの中核は、ニュース・エンコーダーとユーザー・エンコーダーである。
In the news encoder, we learn news representations from news titles by using multi-head self-attention to model the interactions between words.
ニュースエンコーダでは、単語間の相互作用をモデル化するために多頭自己注意を用いてニュースタイトルからニュース表現を学習する。
In the user encoder, we learn representations of users from their browsing by using multi-head self-attention to capture their relatedness.
ユーザーエンコーダでは、多頭の自己注意を用いてユーザーの関連性を捉えることで、ブラウジングからユーザの表現を学習する。
Besides, we apply additive attentions to both news and user encoders to select important words and news to learn more informative news and user representations.
さらに、重要性の高い単語やニュースを選択してより有益なニュースやユーザ表現を学習するために、ニュースとユーザのエンコーダの両方にadditive attentionを適用する。
Extensive experiments on a real-world dataset show that our approach can effectively and efficiently improve the performance of news recommendation.
実世界のデータセットを用いた広範な実験により、我々のアプローチが効果的かつ効率的にニュース推薦のパフォーマンスを改善できることが示された。

# 2. Our Approach 我々のアプローチ

Our NRMS approach for news recommendation is shown in Fig.2.It contains three modules, i.e., news encoder, user encoder and click predictor.
ニュース推薦のためのNRMSアプローチは、図2に示すように、ニュースエンコーダ、ユーザーエンコーダ、クリック予測器の3つのモジュールから構成される。

## 2.1. News Encoder ニュースエンコーダ

The news encoder module is used to learn news representations from news titles.
ニュースエンコーダー・モジュールは、ニュースのタイトルからニュース表現を学習するために使われる。
It contains three layers.
**3層構造**になっている。

The first one is word embedding, which is used to convert a news title from a sequence of words into a sequence of low-dimensional embedding vectors.
最初のものは単語埋め込みで、**ニュースのタイトルを単語の列から低次元の埋め込みベクトルのsequenceに変換する**のに使われる。
Denote a news title with M words as [w1, w2, ..., wM].
M個の単語からなるニュースタイトルを $[w_1, w_2, ..., w_M]$ とする。
Through this layer it is converted into a vector sequence [e1, e2, ..., eM].
この層を通してベクトルsequence $[e_1, e_2, ..., e_M]$ に変換される。
(この層は学習済み言語モデルで代替できるよね:thinking:)

The second layer is a word-level multi-head self-attention network (Vaswani et al., 2017; Wu et al., 2018).
第2層は単語レベルの多頭自己注意ネットワークである（Vaswani et al, 2017; Wu et al, 2018）。
The interactions between words are important for learning news representations.
**単語間の相互作用**は、ニュース表現を学習する上で重要である。(単語Aと単語Bが一緒の文章に含まれていることが重要...!みたいな? 特徴量間の相互作用を考慮したいって話だよね:thinking:)
For example, in the news title “Rockets Ends 2018 with a Win”, the interaction between “Rockets” and “Win” is useful for understanding this news, and such long-distance interactions usually cannot be captured by CNN.
例えば、"Rockets Ends 2018 with a Win "というニュースタイトルでは、"Rockets "と "Win "の相互作用がこのニュースを理解するのに有効であり、このような長距離の相互作用は通常CNNでは捉えることができない。
In addition, a word may interact with multiple words in the same news.
さらに、ひとつの単語が同じニュース内の複数の単語と相互作用することもある。
For instance, in above example the word “Rockets” has interactions with both “Ends” and “Win”.
例えば、上記の例では、"Rockets "という単語は "End "と "Win "の両方と相互作用する。
Thus, we propose to use multi-head self-attention to learn contextual representations of words by capturing their interactions.
そこで、多頭自己注意を用いて、単語間の相互作用を捉えることにより、単語の文脈表現を学習することを提案する。
The representation of the ith word learned by the kth attention head is computed as:
k番目のアテンション・ヘッドが学習した単語の表現は、次のように計算される:

$$
\alpha^{k}_{i,j} = \frac{exp(e_{i}^T Q_{k}^{w} e_{j})}{\sum_{m=1}^{M} exp(e_{i}^T Q_{k}^{w} e_{m})}
\tag{1}
$$

$$
\mathbf{h}_{i,j}^{w} = V_{k}^{w} (\sum_{j=1}^{M} \alpha^{k}_{i,j} e_{j})
$$

where Qw k and Vw k are the projection parameters in the kth self-attention head, and α k i,j indicates the relative importance of the interaction between the ith and jth words.
ここで、$Q_{k}^{w}$ と $V_{k}^{w}$ は、k番目のself-attention headの線形投影パラメータであり、$\alpha^{k}_{i,j}$ はi番目とj番目の単語の相互作用の相対的重要度を示す。(これがattention weightになるのかな?)
The multi-head representation h w i of the ith word is the concatenation of the representations produced by h separate self-attention heads, i.e., h w i = [h w i,1 ; h w i,2 ; ...; h w i,h].
i番目の単語のmulti-heads表現 $h_{w}^{i}$ は、h個の別々のself-attention headによって生成された表現の連結であり、すなわち、$h_{w}^{i} = [h_{w}^{i,1} ; h_{w}^{i,2} ; ...; h_{w}^{i,h}]$ である。

The third layer is an additive word attention network.
第3層はadditiveな単語注目ネットワークである。
Different words in the same news may have different importance in representing this news.
同じニュース内の異なる単語は、このニュースを表現する上で異なる重要性を持つかもしれない。
For example, in the second news of Fig.1, the word “NFL” is more informative than “Today” for understanding this news.
例えば、図1の2番目のニュースでは、「NFL」という単語は「Today」よりもこのニュースを理解する上で有益である。(うんうん、単語によってテキストの特徴を表す度合いが異なるよね、って話。だから簡単に平均とるだけじゃだめだよね、みたいなこと??)
Thus, we propose to use attention mechanism to select important words in news titles for learning more informative news representations.
そこで我々は、より有益なニュース表現を学習するために、**ニュースタイトル中の重要な単語を選択するアテンション・メカニズムを用いる**ことを提案する。
The attention weight α w i of the i-th word in a news title is computed as:
ニュースのタイトルに含まれるi番目の単語の attention weight $\alpha^{w}_{i}$ は次のように計算される：

$$
a^{w}_{i} = q^T_{w} tanh(V_{w} h^{w}_{i} + v_{w})
\tag{3}
$$

(↑additive attentionの式。$q_{w}$ と $V_{w}$ と $v_{w}$ は学習可能なパラメータ。一層のFFNになってる。self-attentionと異なり、添字がiだけなのか...!)

$$
\alpha^{w}_{i} = \frac{exp(a^{w}_{i})}{\sum_{j=1}^{M} exp(a^{w}_{j})}
$$

(最終的なattention weightは上式のようにsoftmaxで正規化される)

where Vw and vw are projection parameters, and qw is the query vector.
ここで、$V_{w}$ と $v_{w}$ は線形投影パラメータであり、$q_{w}$ はクエリベクトルである。
The final representation of a news is the weighted summation of the contextual word representations, formulated as:
ニュースの最終的な表現は、contextual word representationsの重み付き合計であり、次のように定式化される：

$$
\mathbf{r} = \sum_{i=1}^{M} \alpha^{w}_{i} h^{w}_{i}
$$

## 2.2. User Encoder ユーザーエンコーダ

The user encoder module is used to learn the representations of users from their browsed news.
ユーザーエンコーダーモジュールは、閲覧したニュースからユーザの表現を学習するために使用される。
It contains two layers.
**2層構造**になっている。

The first one is a newslevel multi-head self-attention network.
最初のものは、ニュースレベルのマルチヘッド自己アテンション・ネットワークである。
Usually, news articles browsed by the same user may have some relatedness.
**通常、同じユーザが閲覧したニュース記事には関連性がある**。
For example, in Fig.1, the first two news articles are related.
例えば図1では、最初の2つのニュース記事が関連している。
In addition, a news article may interact with multiple news articles browsed by the same user.
さらに、ニュース記事は、同じユーザが閲覧した**複数のニュース記事と相互作用**する可能性がある。(単一の記事Aを読んでいる、以外にも記事Aと記事Bの組み合わせを読んでいる、という事がユーザの特徴として重要になる可能性、の話??)
Thus, we propose to apply multi-head self-attention to enhance the representations of news by capturing their interactions.
このように、我々はmulti-head self-attentionを適用して、**ニュース間の相互作用を捉えることによってニュース表現を強化する**ことを提案する。
The representation of the ith news learned by the kth attention head is formulated as follows:
k番目のアテンション・ヘッドが学習した $i$ 番目 (=閲覧履歴の!)のニュースの表現は以下のように定式化される:

$$
\beta^{k}_{i,j} = \frac{exp(r_{i}^T Q_{k}^{n} r_{j})}{\sum_{m=1}^{N} exp(r_{i}^T Q_{k}^{n} r_{m})}
\tag{6}
$$

(i番目とj番目の記事間のattention weight)

$$
h^{n}_{i,j} = V_{k}^{n} (\sum_{j=1}^{N} \beta^{k}_{i,j} r_{j})
$$

where Qn k and Vn k are parameters of the kth news self-attention head, and β k i,j represents the relative importance of the interaction between the jth and the kth news.
ここで、$Q_{k}^{n}$ と $V_{k}^{n}$ は、k番目のニュース自己注意ヘッドのパラメータであり、$\beta^{k}_{i,j}$ はj番目とk番目のニュースの相互作用の相対的重要度を表す。
The multi-head representation of the ith news is the concatenation of the representations output by h separate self-attention heads, i.e., h n i = [h n i,1 ; h n i,2 ; ...; h n i,h].
i番目のニュースのmulti-heads表現 $h_{n}^{i}$ は、h個の別々のself-attention headによって出力された表現の連結であり、すなわち、$h_{n}^{i} = [h_{n}^{i,1} ; h_{n}^{i,2} ; ...; h_{n}^{i,h}]$ である。

The second layer is an additive news attention network.
第2層は、additiveなニュース注目ネットワークである。
Different news may have different informativeness in representing users.
**ニュースによって、ユーザを表現するための情報量は異なる場合がある**。(うんうん、全員が読んでる記事とかね...!)
For example, in Fig.1 the first news is more informative than the fourth news in modeling user interest, since the latter one is usually browsed by massive users.
例えば、**図1では、4番目のニュース(天気)よりも1番目のニュース(NBA)の方が、ユーザの興味をモデル化する上で有益**である。
Thus, we propose to apply the additive attention mechanism to select important news to learn more informative user representations.
そこで我々は、より有益なユーザ表現を学習するための重要なニュースを選択するために、additive attentionメカニズムを適用することを提案する。
The attention weight of the ith news is computed as:
i番目のニュースのattention weight $\alpha^{n}_{i}$ は次のように計算される:

$$
a^{n}_{i} = q^T_{n} tanh(V_{n} h^{n}_{i} + v_{n})
\tag{8}
$$

$$
\alpha^{n}_{i} = \frac{exp(a^{n}_{i})}{\sum_{j=1}^{N} exp(a^{n}_{j})}
$$

where Vn, vn and qn are parameters in the attention network, and N is the number of the browsed news.
ここで $V_{n}$ 、 $v_{n}$ 、 $q_{n}$ はアテンション・ネットワークのパラメータであり、Nは閲覧したニュースの数である。
The final user representation is the weighted summation of the representations of the news browsed by this user, which is formulated as:
最終的なユーザ表現は、このユーザが閲覧したニュース表現の重み付き合計であり、次のように定式化される:

$$
\mathbf{u} = \sum_{i=1}^{N} \alpha^{n}_{i} h^{n}_{i}
$$

## 2.3. Click Predictor クリック予測

The click predictor module is used to predict the probability of a user clicking a candidate news.
クリック予測モジュールは、ユーザがニュース候補をクリックする確率を予測するために使用される。
Denote the representation of a candidate news Dc as r c .
候補ニュース $D^c$ の表現を $r^{c}$ とする。
Following (Okura et al., 2017), the click probability score yˆ is computed by the inner product of the user representation vector and the news representation vector, i.e., yˆ = u T r c .
(Okura et al., 2017)に従って、クリック確率スコア $\hat{y}$ は、ユーザ表現ベクトルとニュース表現ベクトルの内積によって計算される。すなわち、$\hat{y} = \mathbf{u}^T \mathbf{r}^{c}$ である。
We also explored other kinds of scoring methods such as perception, but dot product shows the best performance and efficiency.
パーセプトロンなどの他の種類のスコアリング方法も試したが、**ドット積が最も優れたパフォーマンスと効率を示した**。(そうなのか...!)

## 2.4. Model Training モデルトレーニング

Motivated by (Huang et al., 2013), we use negative sampling techniques for model training.
(Huang et al., 2013)に動機づけられ、我々はモデル学習に**ネガティブサンプリング技術を使用**する。
For each news browsed by a user (regarded as a positive sample), we randomly sample K news which are shown in the same impression but not clicked by the user (regarded as negative samples).
ユーザによって閲覧された各ニュース(positive sample)について、**同じインプレッションに表示されたがユーザによってクリックされなかったニュース(negative sample)**をK個無作為にサンプリングする。
We shuffle the orders of these news to avoid possible positional biases.
可能な位置バイアスを避けるために、これらのニュースの順序をシャッフルする。
Denote the click probability score of the positive and the K negative news as yˆ + and [ˆy − 1 , yˆ − 2 , ..., yˆ − K] respectively.
正のニュースとK個の負のニュースのクリック確率スコアをそれぞれ $\hat{y}^{+}$ と $[\hat{y}^{-}_{1}, \hat{y}^{-}_{2}, ..., \hat{y}^{-}_{K}]$ とする。
These scores are normalized by the softmax function to compute the posterior click probability of a positive sample as follows:
これらのスコアはソフトマックス関数によって正規化され(=総和が1になるようにされ!)、以下のように陽性サンプルの事後クリック確率を計算する:

$$
p_{i} = \frac{exp(y^{+}_{i})}{exp(y^{+}_{i}) + \sum_{j=1}^{K} exp(y^{-}_{j})}
\tag{11}
$$

We re-formulate the news click probability prediction problem as a pseudo (K + 1)-way classification task, and the loss function for model training is the negative log-likelihood of all positive samples S, which is formulated as follows:
ニュースのクリック確率予測問題を、**擬似的な(K + 1)個分類タスクとして定式化**し、モデル学習のための損失関数は、すべての正のサンプル $S$ の負の対数尤度であり、次のように定式化される(要はmaximum likelihood estimation...!):

$$
\mathcal{L} = - \sum_{i \in S} log(p_{i})
\tag{12}
$$

# 3. Experiments 実験

## 3.1. Datasets and Experimental Settings データセットと実験設定

We conducted experiments on a real-world news recommendation dataset collected from MSN News3 logs in one month (Dec.13, 2018 to Jan.12, 2019).
MSN Newsのログから収集した1ヶ月間(2018年12月13日から2019年1月12日まで)の実世界のニュース推薦データセットで実験を行った。(要はMINDデータセットか)
The detailed statistics are shown in Table 1.
詳細な統計は表1に示す。
The logs in the last week were used for test, and the rest were used for training.
**最後の週のログはテストに使われ**、残りはトレーニングに使われた。
We randomly sampled 10% of training data for validation.
検証のために、トレーニングデータの10％を無作為にサンプリングした。(ここは時系列を気にしてないのかな)

In our experiments, the word embeddings are 300-dimensional and initialized by the Glove embedding (Pennington et al., 2014).
我々の実験では、単語埋め込みは300次元で、Glove埋め込み（Pennington et al, 2014）によって初期化される。
The selfattention networks have 16 heads, and the output of each head is 16-dimensional.
自己注意ネットワークは**16個のヘッド**を持ち、**各ヘッドの出力は16次元**である。
The dimension of the additive attention query vectors is 200.
additive attentionのクエリベクトルの次元は200である。
Following (Wu et al., 2019b), the negative sampling ratio K is 4.
(Wu et al., 2019b)に従い、負のサンプリング比 $K$ は4である。(positive sample1つに対して、negative sampleは4)
Adam (Kingma and Ba, 2014) is used for model optimization.
モデルの最適化にはAdam（Kingma and Ba, 2014）を使用。
We apply 20% dropout to the word embeddings to mitigate overfitting.
オーバーフィッティングを軽減するために、**単語の埋め込みに20％のドロップアウトを適用**する。
The batch size is 64.
バッチサイズは64。
These hyperparameters are tuned on validation set.
これらのハイパーパラメータは検証セットで調整される。
We conducted experiments on a machine with Xeon E5-2620 v4 CPUs and a GTX1080Ti GPU.
Xeon E5-2620 v4 CPUとGTX1080Ti GPUを搭載したマシンで実験を行った。
We independently repeated each experiment 10 times and reported average results in terms of AUC, MRR, nDCG@5 and nDCG@10.
各実験を独立に10回繰り返し、AUC、MRR、nDCG@5、nDCG@10の平均結果を報告した。

## 3.2. Performance Evaluation パフォーマンス評価

We evaluate the performance of our approach by comparing it with several baseline methods, including: (1) LibFM (Rendle, 2012), a matrix factorization based recommendation method; (2) DSSM (Huang et al., 2013), deep structured semantic model; (3) Wide&Deep (Cheng et al., 2016), a popular neural recommendation method; (4) DeepFM (Guo et al., 2017), another popular neural recommendation method; (5) DFM (Lian et al., 2018), deep fusion model for news recommendation; (6) DKN (Wang et al., 2018), deep knowledge-aware network for news recommendation; (7) Conv3D (Khattar et al., 2018), a neural news recommendation method with 3-D CNNs to learn user representations; (8) GRU (Okura et al., 2017), a neural news recommendation method using GRU to learn user representations; (9) NRMS, our approach.
我々は、以下のようないくつかのベースライン手法と比較することで、本アプローチの性能を評価する：

- (1) LibFM (Rendle, 2012), 行列因数分解に基づく推薦手法;
- (2) DSSM (Huang et al., 2013), 深い構造化意味モデル;
- (3) Wide&Deep (Cheng et al., 2016), 有名なニューラル推薦手法;
- (4) DeepFM (Guo et al., 2017), 別の有名なニューラル推薦手法;
- (5) DFM (Lian et al、 2018）、ニュース推薦のための深層融合モデル、
- （6）DKN（Wangら、2018）、ニュース推薦のための深層知識認識ネットワーク、
- （7）Conv3D（Khattarら、2018）、ユーザ表現を学習するための3次元CNNを用いたニューラルニュース推薦手法、
- （8）GRU（Okuraら、2017）、ユーザー表現を学習するためのGRUを用いたニューラルニュース推薦手法、
- （9）NRMS、我々のアプローチ。

In methods (1) and (3-5), we use one-hot encoded user ID, news ID and the TF-IDF features extracted from news titles as the model input.
(1)と(3-5)の方法では、one-hot encodingされたユーザID、ニュースID、およびニュースタイトルから抽出されたTF-IDF特徴量をモデルの入力として使用する。
In methods (6-9), we all use news titles for fair comparison.
(6-9)の方法では、公平な比較のために、すべてニュースのタイトルを使っている。
The results of these methods are summarized in Table 2.
これらの方法の結果を表2にまとめた。

![table2]()

We have several observations from Table 2.
表2からいくつかのことがわかった。

First, neural recommendation methods such as DSSM and NRMS outperform traditional recommendation methods such as LibFM on news recommendation.
第一に、DSSMやNRMSのようなニューラル推薦法は、ニュース推薦においてLibFMのような従来の推薦法を凌駕する。
This may be because neural networks can learn better representations of news and users than matrix factorization methods.
これは、ニューラルネットワークの方が、行列分解法よりもニュースやユーザに関するより優れた表現を学習できるからかもしれない。
Thus, it may be more appropriate to learn news and user representations via neural networks rather than craft them manually.
**したがって、ニュースやユーザ表現を手作業で作るよりも、ニューラルネットワークを使って学習する方が適切かもしれない**。

Second, among the deep learning based methods, the methods which exploit the relatedness between news (e.g., Conv3D, GRU and NRMS) can outperform other methods.
第二に、**ディープラーニングに基づく手法のうち、ニュース間の関連性を利用する手法（Conv3D、GRU、NRMSなど）は、他の手法を上回ることができる**。
This may be because the news browsed by the same user usually have relatedness, and capturing the news relatedness is useful for understanding these news and modeling user interests.
これは、同じユーザが閲覧したニュースには通常関連性があり、ニュースの関連性を把握することは、これらのニュースを理解し、ユーザの興味をモデル化するのに役立つからであろう。

Third, our approach performs better than all baseline methods.
第三に、我々のアプローチは、すべてのベースライン手法よりも優れた性能を発揮する。
This is because our approach can capture the interactions between both words and news via multi-head self-attention to enhance representation learning of news and users.
これは、我々のアプローチが、**ニュースとユーザの表現学習を強化するために、multi-head self-attentionを用いて単語間やニュース間の相互作用を捉えることができるから**である。
Besides, our approach employs additive attention to select important words and news for learning informative news and user representations.
加えて、我々のアプローチは、有益なニュース表現やユーザ表現を学習するために、**重要な単語やニュースを選択するadditive attentionを採用している**。
These results validate the effectiveness of our approach.
これらの結果は、我々のアプローチの有効性を証明するものである。

![table3]()

We also conducted experiments to compare the time efficiency of our approach with several popular news recommendation methods.
また、いくつかの一般的なニュース推薦手法と本アプローチの時間効率を比較する実験も行った。
The results are shown in Table 3.
結果を表3に示す。
From the results, we find our approach has a smaller parameter size and a lower time complexity in learning news and user representations than existing news recommendation methods.
その結果、本アプローチは既存のニュース推薦手法と比較して、**ニュースやユーザ表現を学習する際のパラメータサイズが小さく、時間計算量が低い**ことがわかった。
In addition, different from DKN, our approach does not need to memorize the news browsing histories of users when computing the click probability scores.
さらに、DKNとは異なり、クリック確率スコアを計算する際に、ユーザのニュース閲覧履歴を記憶する必要がない。
In addition, since our approach can be further accelerated by computing the hidden representations of different attention heads in parallel, our approach is more suitable for being deployed in large-scale news recommendation scenarios.
さらに、我々のアプローチは、異なるattention headsの隠れ表現 $h_{i}^{hoge}$ を並列に計算することでさらに高速化することができるため、大規模なニュース推薦シナリオに展開するのに適している。
These results validate the efficiency of our approach.
これらの結果は、我々のアプローチの効率性を検証するものである。

## 3.3. Effectiveness of Attention Mechanism 注意メカニズムの有効性

Next we explore the effectiveness of attentions in our approach.
次に、我々のアプローチにおけるattentionの有効性を探る。(ablation study)
First, we verify the word- and news-level attentions.
まず、単語レベルとニュースレベルのattentionを検証する。
The results are shown in Fig.3(a).
結果を図3(a)に示す。

![figure3 上図]()

We find the word-level attention is very useful.
私たちは**、word-level attentionが非常に有用**であることを発見した。
This is because modeling the interactions between words and selecting important words can help learn informative news representations.
単語間の相互作用をモデル化し(=self-attentionの効果!)、重要な単語を選択する(=additive attentionの効果!)ことで、有益なニュース表現を学習することができるからだ。

Besides, the news-level attention is also useful.
また、**news-level attentionも有用**である。
This is because capturing the relatedness of news and selecting important news can benefit the learning of user representations.
ニュース間の関連性を捉え(=self-attentionの効果)、重要なニュースを選択する(=additive attetionの効果)ことは、ユーザ表現の学習に役立つからである。
Moreover, combining both word- and news-level attentions can further improve the performance of our approach.
さらに、単語レベルとニュースレベルの両方の注意を組み合わせることで、我々のアプローチのパフォーマンスをさらに向上させることができる。

![figure3 下図]()

We also study the influence of additive and selfattentions on our approach.
また、私たちのアプローチにおけるadditive attentionとself-attentionの影響を研究した。
The results are shown in Fig.3(b).
結果を図3(b)に示す。
From these results, we find the selfattentions are very useful.
これらの結果から、self-attentionが非常に有効であることがわかった。
This is because the interactions between words and news are important for understanding news and modeling users.
単語間やニュース間の相互作用は、ニュースを理解し、ユーザをモデル化する上で重要だからだ。

In addition, the additive attentions are also helpful.
加えて、additive attentionも有用である。
This is because different words and news may usually have different importance in representing news and users.
というのも、**単語やニュースによって、ニュースやユーザを表現する際の重要度が異なるから**だ。(これもやりたいよね...!)
Thus, selecting important words and news can help learn more informative news and user representations.
このように、重要な単語やニュースを選択することで、より有益なニュースやユーザー表現を学ぶことができる。
Combining both additive and self-attention can further improve our approach.
アディショナルタイムと自己アテンションの両方を組み合わせることで、私たちのアプローチをさらに向上させることができる。
Thus, these results validate the effectiveness of the attention mechanism in our approach.
したがって、これらの結果は、我々のアプローチにおける注意メカニズムの有効性を証明するものである。

# 4. Conclusion and Future Work 結論と今後の課題

In this paper we propose a neural news recommendation approach with multi-head self-attention.
本稿では、マルチヘッド自己注意を用いたニューラル・ニュース推薦アプローチを提案する。
The core of our approach is a news encoder and a user encoder.
我々のアプローチの中核は、ニュース・エンコーダーとユーザー・エンコーダーである。
In both encoders we apply multihead self-attentions to learn contextual word and news representations by modeling the interactions between words and news.
どちらのエンコーダーでも、**単語間やニュース間の相互作用をモデル化**することによって、文脈に沿った単語とニュースの表現を学習するために、multi-head self-attentionを適用する。
In addition, we use additive attentions to select important words and news to learn more informative news and user representations.
さらに、より有益なニュースやユーザ表現を学習するために、**重要な単語やニュースを選択するaddtive-attention**を用いる。
Extensive experiments validate the effectiveness and efficiency of our approach.
広範な実験により、我々のアプローチの有効性と効率性が検証された。

In our future work, we will try to improve our approach in the following potential directions.
今後の研究では、以下の可能性のある方向で、我々のアプローチを改善しようと考えている。
First, in our framework we do not consider the positional information of words and news, but they may be useful for learning more accurate news and user representations.
まず、我々のフレームワークでは、単語やニュースの位置情報は考慮しないが、より正確なニュースやユーザ表現を学習するためには有用かもしれない。(=positional encoding技術を使って、sequential recommenderに拡張するって話か...!)
We will explore position encoding techniques to incorporate the word position and the time-stamps of news clicks to further enhance our approach.
今後、単語位置とニュースクリックのタイムスタンプを組み込んだ位置エンコーディング技術を探求し、我々のアプローチをさらに強化する予定である。
Second, we will explore how to effectively incorporate multiple kinds of news information in our framework, especially long sequences such as news body, which may challenge the efficiency of typical self-attention networks.
第二に、複数の種類のニュース情報、特に典型的な**self-attentionネットワークの効率性を脅かす可能性のあるニュース本文などの長いシーケンス**を、我々のフレームワークに効果的に組み込む方法を探求する予定である。
