## 0.1. link リンク

- https://arxiv.org/abs/1907.05559 https://arxiv.org/abs/1907.05559

## 0.2. title タイトル

NPA: Neural News Recommendation with Personalized Attention
NPA パーソナライズド・アテンションを備えたニューラル・ニュースレコメンデーション

## 0.3. abstract アブストラクト

News recommendation is very important to help users find interested news and alleviate information overload.
ニュースレコメンデーションは、ユーザーが興味のあるニュースを見つけ、情報過多を緩和するために非常に重要です。
Different users usually have different interests and the same user may have various interests.
通常、ユーザーによって興味は異なり、**同じユーザでも様々な興味を持つことがあります**。
Thus, different users may click the same news article with attention on different aspects.
このように、同じニュース記事でも、異なるユーザが異なる側面に注目してクリックすることがあります。
In this paper, we propose a neural news recommendation model with personalized attention (NPA).
本論文では、パーソナライズド・アテンションを用いたニューラル・ニュース推薦モデル（NPA）を提案する。
The core of our approach is a news representation model and a user representation model.
このアプローチの核となるのは、**ニュース表現モデル**と**ユーザー表現モデル**です。
In the news representation model we use a CNN network to learn hidden representations of news articles based on their titles.
**ニュース表現モデルでは、CNNネットワークを用いて**、ニュース記事のタイトルに基づく隠れた表現を学習します。
In the user representation model we learn the representations of users based on the representations of their clicked news articles.
ユーザ表現モデルでは、クリックされたニュース記事の表現に基づいて、ユーザーの表現を学習します。(こっちを知りたい)
Since different words and different news articles may have different informativeness for representing news and users, we propose to apply both word- and news-level attention mechanism to help our model attend to important words and news articles.
異なる単語や異なるニュース記事は、ニュースやユーザを表現するための情報量が異なる可能性があるため、**単語レベルとニュースレベルのattentionメカニズムを適用**することで、モデルが重要な単語やニュース記事に注意することを支援することを提案する。
In addition, the same news article and the same word may have different informativeness for different users.
また、同じニュース記事でも、同じ単語でも、**ユーザによって情報性が異なる場合**があります。(この辺りはNRMSのadditive attentionを導入する動機と同じ:thinking:)
Thus, we propose a personalized attention network which exploits the embedding of user ID to generate the query vector for the wordand news-level attentions.
そこで、ユーザIDの埋め込みを利用し、単語やニュースレベルのアテンションに対するクエリベクトル(=additive attentionの?)を生成するパーソナライズド・アテンション・ネットワークを提案する。
Extensive experiments are conducted on a real-world news recommendation dataset collected from MSN news, and the results validate the effectiveness of our approach on news recommendation.
MSNニュースから収集した実世界のニュース推薦データセットを用いて広範な実験を行い、その結果、ニュース推薦における本アプローチの有効性が検証された。

# 1. Introduction 序章

Online news platforms such as MSN News and Google News have attracted a huge number of users to read digital news [7, 18].
MSN NewsやGoogle Newsなどのオンラインニュースプラットフォームは、デジタルニュースを読むために膨大な数のユーザーを引きつけている [7, 18]。
However, massive news articles are emerged everyday, and it is impractical for users to seek for interested news from a huge volume of online news articles [26, 34].
しかし，日々大量のニュース記事が出現しており，ユーザが膨大な量のオンラインニュース記事から興味のあるニュースを探すのは非現実的である [26, 34] ．
Therefore, it is an important task for online news platforms to target user interests and make personalized news recommendation [1, 8, 14], which can help users to find their interested news articles and alleviate information overload [32, 35].
したがって、オンラインニュースプラットフォームにとって、ユーザの興味をターゲットにして、パーソナライズされたニュース推薦を行うことは重要な課題であり [1, 8, 14] 、これにより、ユーザは興味のあるニュース記事を見つけ、情報過多を緩和することができます [32, 35] 。

There are two common observations in the news recommendation scenario.
ニュースレコメンデーションシナリオには、**2つの共通した見解**があります。

First, not all news clicked by users can reflect the preferences of users.
**まず、ユーザがクリックしたすべてのニュースが、ユーザの嗜好を反映できるわけではありません。**(うんうん、User Encoder部分にattentionを導入するモチベ...!)
For example, as illustrated in Figure 1, user-1 clicked all the three news, but he/she was only interested in the first and the second news.
例えば、図1に示すように、ユーザー1は3つのニュースをすべてクリックしたが、彼/彼女は1つ目と2つ目のニュースにしか興味がなかった。
In addition, the same news should also have different informativeness for modeling different users.
また、同じニュースは、異なるユーザをモデル化するためにも、異なる情報量を持つべきである。(うんうん)
For example, if user-1 is very interested in sports news but user-2 rarely reads, the news “Dolphins May Have Found A Head Coach” is very informative for characterizing user-1, but less informative for user-2.
例えば、ユーザー-1はスポーツニュースに非常に興味があるが、ユーザー-2はほとんど読まない場合、「Dolphins May Have Found A Head Coach」というニュースは、ユーザー-1を特徴付けるために非常に有益であるが、ユーザー-2にとってはあまり有益でない。

Second, different words in news titles usually have different informativeness for learning news representations.
**第二に、ニュースのタイトルに含まれる単語は、通常、ニュース表現を学習するための情報量が異なる**。(news encoder部分にattentionを導入するモチベ...!)
For example, the word “Crazy” in the first news title is informative, while the word “That” is uninformative.
例えば、最初のニュースタイトルの「Crazy」という言葉は情報的であり、「That」という言葉は情報的でない。
Moreover, the same words within a news title may also have different informativeness for revealing preferences of different users.
**また、ニュースタイトルに含まれる同じ単語でも、ユーザによって嗜好を明らかにする情報性が異なる場合があります**。(NRMSではこの点は考慮できてない気がする)
For example, user-1 may be attracted by the word “Crazy”, and user-2 may pay more attention to the words “Actually Work”.
例えば、ユーザ1は「Crazy」という言葉に惹かれ、ユーザ2は「Actually Work」という言葉に注目することがあるのではないでしょうか。
Therefore, modeling the different informativeness of words and news for different users may be useful for learning better representations of users for accurate news recommendation.
したがって、**ユーザーごとに異なる単語やニュースの情報性をモデル化すること**は、正確なニュース推薦のために、より良いユーザー表現を学習するのに有用であると考えられる。

Existing news recommendation methods are usually based on collaborative filtering (CF) techniques and news content[20–22, 24].
既存のニュース推薦手法は、通常、協調フィルタリング（CF）技術とニュースコンテンツに基づく[20-22, 24]。
For example, Liu et al.[21] proposed a CF-based approach for news recommendation based on user interests.
例えば、Liuら[21]は、**ユーザの興味に基づくニュース推薦のためのCFベース**のアプローチを提案した。
They use a Bayesian model to extract the interest features of users based on the click distributions on news articles in different categories.
彼らはベイズモデルを用いて、異なるカテゴリのニュース記事に対するクリック分布から、ユーザの興味特徴を抽出しています。
Okura et al.[24] proposed to first learn the distributed representations of news articles based on similarity and then use recurrent neural networks to learn user representations from browsing histories for click prediction.
Okuraら[24]は、まず類似性に基づいてニュース記事の分散表現を学習し、次にRNNを用いて閲覧履歴からユーザ表現を学習し、クリック予測に利用することを提案した。
Lian et al.[20] proposed a deep fusion model (DMF) to learn representations of users and news using combinations of fully connected networks with different depth.
Lianら[20]は、深さの異なる完全連結ネットワークの組み合わせを用いて、ユーザーやニュースの表現を学習する深層融合モデル（DMF）を提案した。
They also used attention mechanism to select important user features.
また、重要なユーザ特徴量を選択するために、アテンション機構を使用した。
However, all these existing methods cannot model the different informativeness of news and their words for different users, which may be useful for improving the quality of personalized news recommendation.
しかし、これらの既存手法は、**異なるユーザにとってのニュースとその単語の情報量の違いをモデル化することができていない**。(NRMSは前者は考慮できているが、後者は考慮できていない気がする:thinking:)そしてそれは、パーソナライズされたニュース推薦の品質を向上させるのに役立つ可能性がある。

In this paper, we propose a neural approach with personalized attention (NPA) for news recommendation.
本稿では、ニュース推薦のためのパーソナライズド・アテンションを用いたニューラル・アプローチ（NPA）を提案する。
The core of our approach is a news representation model and a user representation model.
**このアプローチの核となるのは、ニュース表現モデルとユーザー表現モデル**です。
In the news representation model we use a CNN network to learn the contextual representations of news titles, and in the user representation model we learn representations of users from their clicked news.
ニュース表現モデルでは、CNNネットワークを用いてニュースタイトルの文脈表現を学習し、ユーザ表現モデルでは、クリックしたニュースからユーザ表現を学習しています。
Since different words and news articles usually have different informativeness for learning representations of news and users, we propose to apply attention mechanism at both word- and news-level to select and highlight informative words and news.
通常、単語やニュース記事は、ニュースやユーザに関する表現を学習するための情報量が異なるため、単語レベルとニュースレベルの両方でattentionメカニズムを適用し、情報量の多い単語やニュースを選択して強調することを提案します。
In addition, since the informativeness of the same words and news may be different for different users, we propose a personalized attention network by using the embedding of user ID as the query vector of the word- and news-level attention networks to differentially attend to important words and news according to user preferences.
また、**同じ単語やニュースでもユーザによって情報量が異なる場合がある**ため、ユーザIDを埋め込みとして使用し、単語レベルとニュースレベルのアテンションネットワークのクエリベクトルとして使用することで、ユーザの好みに応じて重要な単語やニュースに差別的に注意を払うパーソナライズド・アテンション・ネットワークを提案します。(self-attentionじゃなくadditive attentionを使う箇所があるのかな??)
Extensive experiments on a real-world dataset collected from MSN news validate the effectiveness of our approach on news recommendation.
MSNニュースから収集した実世界のデータセットを用いた広範な実験により、ニュース推薦における本アプローチの有効性が検証された。

# 2. Related Work 関連作品

## 2.1. News Recommendation ニュースレコメンド

News recommendation is an important task in the data mining field, and have been widely explored over years.
ニュースレコメンデーションはデータマイニングの分野で重要なタスクであり、長年にわたって広く研究されてきた。
Traditional news recommendation methods usually based on news relatedness [23], semantic similarities [3] and human editors’ demonstration [33].
従来のニュース推薦手法は、通常、ニュースの関連性 [23]、意味的類似性 [3]、人間の編集者のデモンストレーション [33] に基づいています。
However, the preferences of users cannot be effectively modeled.
しかし、ユーザーの嗜好を効果的にモデル化することはできません。
Therefore, most news recommendation methods are based on CF techniques.
そのため、**ニュース推薦手法の多くはCF手法に基づくもの**である。(CBに基づく方が多そうだけど...?)
The earliest study on CF methods for news recommendation is the Grouplens project [17], which applied CF methods to aggregate news from Usenet.
ニュース推薦のためのCF手法に関する最も古い研究は、Usenetからのニュースを集約するためにCF手法を適用したGrouplensプロジェクト[17]である。
However, pure CF methods usually suffer from the sparsity and the cold-start problems, which are especially significant in news recommendation scenarios [19].
しかし、純粋なCF手法は、通常、スパース性とコールドスタートの問題に悩まされており、これはニュース推薦のシナリオにおいて特に重要である[19]。
Thus, content-based techniques are usually complementary methods to CF [2, 20, 21, 24, 27, 29, 32, 39].
したがって、コンテンツベースの手法は、通常、CFを補完する手法である[2, 20, 21, 24, 27, 29, 32, 39]。
For example, Liu et al.[21] proposed to incorporate user interests for news recommendation.
例えば、Liuら[21]は、ニュース推薦にユーザの興味を取り入れることを提案しています。
They use a Bayesian model to predict the interests of users based on the distributions of their clicked news articles in different categories.
彼らは、ベイズモデルを用いて、異なるカテゴリのニュース記事をクリックした分布から、ユーザーの興味を予測します。
Okura et al.[24] proposed to learn news embeddings based on the similarities between news articles in the same and different categories.
大倉ら[24]は、同じカテゴリと異なるカテゴリのニュース記事間の類似性に基づいて、ニュース埋め込みを学習することを提案した。
They use recurrent neural networks to learn user representations from the browsing histories through time to predict the score of news.
リカレントニューラルネットワークを用いて、経時的な閲覧履歴からユーザー表現を学習し、ニュースのスコアを予測するのだ。
Lian et al.[20] proposed a deep fusion model (DMF) to learn representations of users from various features extracted from their news reading, general web browsing and web searching histories.
Lianら[20]は、ニュース閲覧履歴、一般Web閲覧履歴、Web検索履歴から抽出した様々な特徴からユーザーの表現を学習する深層融合モデル（DMF）を提案した。
They used an inception network with attention mechanism to select important user features and combine the features learned by networks with different depths.
彼らは、アテンション機構を持つインセプションネットワークを用いて、重要なユーザー特徴を選択し、異なる深さのネットワークで学習した特徴を組み合わせています。
Wang et al.[32] proposed to use the embeddings of the entities extracted from a knowledge graph as a separate channel of the CNN input.
Wangら[32]は、知識グラフから抽出したエンティティの埋め込みを、CNN入力の別チャネルとして利用することを提案した。
However, these existing methods cannot simultaneously model the informativeness of words and news.
しかし、これらの既存手法は、単語とニュースの情報量を同時にモデル化することはできません。
Different from all these methods, we propose to use personalized attention mechanism at both word- and new-level to dynamically recognize different informative words and news according to the preference of different users.
これらの方法とは異なり、我々は、**単語とニュースの両方のレベルでパーソナライズされたアテンションメカニズムを使用**し、**異なるユーザの好みに応じて異なる有益な単語とニュースを動的に認識する**ことを提案します。
Experimental results validate the effectiveness of our approach.
実験結果は、本アプローチの有効性を検証するものです。

## 2.2. Neural Recommender Systems ニューラル・レコメンダー・システム

In recent years, deep learning techniques have been widely used in recommender systems [31].
近年、推薦システムにおいて、深層学習技術が広く利用されています[31]。
For example, Xue et al.[37] proposed to use multi-layer neural networks to learn the latent factors of users and items in matrix factorization.
例えば、Xueら[37]は、行列因数分解において、ユーザーやアイテムの潜在的な要因を学習するために多層ニューラルネットワークを使用することを提案した。
However, the content of users and items cannot be exploited, which is usually important for recommender systems.
しかし、通常レコメンダーシステムで重要となる、ユーザーやアイテムの内容を利用することはできない。
Different from using neural networks within traditional matrix factorization frameworks, many methods apply neural networks to learn representations of users and items from raw features [5, 6, 9, 11–13].
従来の行列分解フレームワークでニューラルネットワークを使用するのとは異なり、**多くの手法は、生の特徴量からユーザーやアイテムの表現を学習するためにニューラルネットワークを適用します**[5, 6, 9, 11-13].
For example, Huang et al.[13] proposed a deep structured semantic model (DSSM) for click-through rate (CTR) prediction.
例えば、Huangら[13]は、クリックスルー率（CTR）予測のための深層構造化セマンティックモデル（DSSM）を提案した。
They first hashed the very sparse bag-of-words vectors into low-dimensional feature vectors based on character n-grams, then used multi-layer neural networks to learn the representations of query and documents, and jointly predicted the click score of multiple documents.
彼らはまず、非常に疎なBag-of-Wordsベクトルを文字n-gramに基づく低次元特徴ベクトルにハッシュ化し、多層ニューラルネットワークを用いてクエリと文書の表現を学習し、複数の文書のクリックスコアを共同で予測した。
Cheng et al.[5] proposed a Wide & Deep approach to combine a wide channel using a linear transformer with a deep channel using multi-layer neural networks.
Chengら[5]は、線形トランスを用いた広いチャネルと多層ニューラルネットワークを用いた深いチャネルを組み合わせるWide & Deepアプローチを提案しました。
Guo et al.[11] proposed a DeepFM approach which combines factorization machines with deep neural networks.
Guoら[11]は、因数分解マシンとディープニューラルネットワークを組み合わせたDeepFMアプローチを提案しています。
The two components share the same input features and the final predicted score is calculated from the combination of the output from both components.
2つのコンポーネントは同じ入力特徴を共有し、最終的な予測スコアは、両方のコンポーネントからの出力の組み合わせから計算されます。
However, these methods usually rely on handcrafted features, and the dimension of feature vectors is usually huge.
しかし、これらの方法は通常、手作業で作られた特徴量に依存しており、特徴量ベクトルの次元は通常巨大である。
In addition, they cannot effectively recognize the important contexts when learning news and user representations.
また、ニュースやユーザ表現を学習する際に、重要な文脈を効果的に認識することができません。
Different from the aforementioned methods, our approach can dynamically select important words and news for recommendation based on user preferences, which may be useful for learning more informative user representations for personalized news recommendation.
本手法は、前述の方法とは異なり、ユーザーの嗜好に基づき、重要な単語やニュースを動的に選択して推薦することができるため、パーソナライズされたニュース推薦のために、より情報量の多いユーザー表現を学習するのに有用であると考えられる。

# 3. Our Approach 私たちのアプローチ

In this section, we introduce our NPA approach with personalized attention for news recommendation.
本節では、ニュース推薦のためのパーソナライズド・アテンションを用いたNPAアプローチについて紹介する。
There are three major modules in our model.
私たちのモデルには、大きく分けて**3つのモジュール**があります。
The first one is a news encoder, which aims to learn the representations of news.
まず、ニュースの表現を学習することを目的とした "**news encoder**"です。
The second one is a user encoder, which aims to learn user representations based on the representations of his/her clicked news.
**2つ目は**"user encoder"で、自分のクリックしたニュースの表現からユーザー表現を学習することを目的としています。
The third one is a click predictor, which is used to predict the click score of a series of candidate news.
3つ目は、一連の候補ニュースのクリックスコアを予測するための"**click predictor**"です。
In the news encoder and user encoder module, we apply personalized attention networks at both word- and news-level to differentially select informative words and news according to user preferences.
ニュースエンコーダとユーザーエンコーダモジュールでは、単語レベルと記事レベルのパーソナライズド・アテンション・ネットワークを適用し、ユーザーの好みに応じて有益な単語とニュースを差別的に選択します。
The architecture of our approach is shown in Figure 2.
本アプローチのアーキテクチャを図2に示します。
We will introduce the details of our approach in the following sections.
以下、アプローチの詳細について紹介する。

## 3.1. News Encoder ニュースエンコーダ

Since users’ click decisions on news platforms are usually made based on the titles of news articles, in our approach the news encoder module aims to learn news representations from news titles.
ニュースプラットフォームにおける**ユーザのクリック判断は、通常、ニュース記事のタイトルに基づいて行われる**ため、我々のアプローチでは、ニュースエンコーダーモジュールは、**ニュースタイトルからニュース表現を学習する**ことを目的としています。(CTRを最大化するようなKPIなのかな...)
As shown in Figure 2, there are three sub-modules in the news encoder module.
図2に示すように、ニュースエンコーダーモジュールには**3つのサブモジュール**が存在する。

The first one is **word embedding**.
まず1つ目は、単語の埋め込みです。
It is used to convert a sequence of words within news title into a sequence of low-dimensional dense vectors.
ニュースタイトル内の単語列を、低次元の密なベクトル列に変換するために使用されます。
We denote the word sequence of the news Di as Di = [w1,w2, ...,wM ], where M is the number of words in the news title.
ニュースDiの単語列をDi = [w1,w2, ...,wM ]とし、Mはニュースのタイトルの単語数であるとする。
The word sequence Di is transformed into a sequence of vector E w = [e1, e2, ..., eM ] using a word embedding matrix We ∈ RV ×D , where V denotes the vocabulary size and D denotes the dimension of word embedding vectors.
単語列Diは、単語埋め込み行列We∈RV×D（ここで、Vは語彙の大きさ、Dは単語埋め込みベクトルの次元を表す）を用いて、ベクトルE w = [e1, e2, ..., eM ] の列に変換される。

The second one is a **convolutional neural network (CNN)** [15].
2つ目は、畳み込みニューラルネットワーク（CNN）[15]である。
CNN is an effective neural architecture for capturing local information [36].
CNNは局所的な情報を捉えるのに有効な神経アーキテクチャである[36]。
Usually, local contexts within news are important for news recommendation.
通常、ニュースの推薦には、ニュース内のローカルな文脈が重要である。
For example, in the news title “best Fiesta bowl moments”, the local combination of the words “Fiesta” and “bowl” is very important to infer the topic of this news.
例えば、「best Fiesta bowl moments」というニュースタイトルでは、「Fiesta」と「bowl」という単語のローカルな組み合わせが、このニュースの話題を推測する上で非常に重要です。
Thus, we apply a CNN network to the word sequences to learn contextual representations of words within news titles by capturing their local contexts.
そこで、単語列にCNNネットワークを適用し、ニュースタイトル内の単語の局所的な文脈を捉えて、文脈表現を学習します。
Denote the representation of the i-th word as ci , which is calculated as:
i 番目の単語の表現を ci とし、次のように計算する：

$$
c_i = \text{ReLU}(F_w \times e_{(i-k):(i+k)} + b_w)
\tag{1}
$$

where $e_{(i-k):(i+k)}$ denotes the concatenation of the word embeddings from the position (i − k) to (i + k).
ここで、$e_{(i-k):(i+k)}$ は、位置(i - k)から(i + k)までの単語埋め込みを連結したものを表す.
$F_w \in R^{N_f \times (2k+1)D}$ and $b_w \in R^{N_f}$ denote the parameters of the CNN filters, where Nf is the number of CNN filters and 2k+1 is their window size.
$F_w \in R^{N_f \times (2k+1)D}$ と $b_w \in R^{N_f}$ はCNNフィルタのパラメータを示し、NfはCNNフィルタの数、2k+1はそのウィンドウサイズを示しています。
ReLU [10] is used as the non-linear function for activation.
活性化のための非線形関数としてReLU [10]が使用されています。
The output of the CNN layer is the sequence of contextual word representation vectors, denoted as [c1, c2, ..., cM ].
CNN層の出力は、[c1, c2, ..., cM ]と表記される**文脈上の単語表現ベクトルの列**である。

The third one is a **word-level personalized attention network**.
3つ目は、単語レベルのパーソナライズド・アテンション・ネットワークです。
Different words in a news title usually have different informativeness for characterizing the topics of news.
**ニュースのタイトルに含まれる単語は、通常、ニュースのトピックを特徴付けるための情報量が異なる**。
For example, in the news entitled with “NBA games in this season” the word “NBA” is very informative for learning news representations, since it conveys important clues about the news topic, while the word “this” is less informative for recommendation.
例えば、「NBA games in this season」と題されたニュースでは、「NBA」という単語はニューストピックに関する重要な手がかりを伝えるため、ニュース表現の学習にとって非常に有益であるが、「this」という単語は推薦にとってあまり有益でない、ということが言える。(**わかりやすいexample!**)
In addition, the same word may also have different informativeness for the recommendation of different users.
また、**同じ単語でも、ユーザによって推薦のための情報量が異なる**場合があります。
For example, in the news title “Genesis G70 is the 2019 MotorTrend Car of the Year”, the words “Genesis” and “MotorTrend” are informative for the recommendation of users who are interested in cars, but may be less informative for users who are not interested.
例えば、ニュースタイトル「Genesis G70 is the 2019 MotorTrend Car of the Year」において、「Genesis」「MotorTrend」という言葉は、**車に興味のあるユーザの推薦には有益**ですが、興味のないユーザーには有益性が低いかもしれない。
Thus, recognizing important words for different users is useful for news recommendation.
このように、**ユーザごとに重要な単語を認識することは、ニュース推薦に有効**です。
However, in vanilla non-personalized attention networks [20], the attention weights are only calculated based on the input representation sequence via a fixed attention query vector, and the user preferences are not incorporated.
しかし、バニラな非パーソナライズド・アテンションネットワーク[20]では、固定されたアテンションクエリーベクトルを介した入力表現シーケンスに基づいてアテンションウェイトが計算されるだけで、ユーザのプリファレンスは組み込まれていない。
To model the informativeness of each word for the recommendation of different users, we propose to use a personalized attention network to recognize and highlight important words within news titles according to user preferences.
異なるユーザの推薦のために各単語の情報性をモデル化するために、**ユーザの好みに応じてニュースタイトル内の重要な単語を認識し強調する**パーソナライズド・アテンション・ネットワークを使用することを提案する。
The architecture of our personalized attention module is shown in Figure 3.
私たちのパーソナライズド・アテンション・モジュールのアーキテクチャを図3に示します。
In order to obtain the representation of user preferences, we first embed the ID of users into a representation vector eu ∈ RDe , where De denotes the size of user embedding.
ユーザの嗜好の表現を得るために、まずユーザのIDを表現ベクトル$e_u \in R^{D_e}$に埋め込みます（$D_e$ はユーザ埋め込みのサイズを表す）。
Then we use a dense layer to learn the word-level user preference query qw as:
次に、密な層(=全結合層?)を使って、単語レベルのユーザ嗜好クエリ$q_w$を次のように学習する：

$$
q_w = \text{ReLU}(V_w \times e_u + v_w)
\tag{2}
$$

where $V_w \in R^{D_e \times D_q}$ and $v_w \in R^{D_q}$ are parameters, $D_q$ is the preference query size.
ここで、$V_w \in R^{D_e \times D_q}$、$v_w \in R^{D_q}$ はパラメータ、$D_q$ はプリファレンスクエリのサイズである。
In this module, the attention weight of each word is calculated based on the interactions between the preference query and word representations.
このモジュールでは、嗜好クエリと単語表現の相互作用に基づいて、**各単語の注目度が計算**される。
We denote the attention weight of the i-th word as αi , which is formulated as:
i 番目の単語の注目重みを$\alpha_{i}$とし、次のように定式化する：

$$
a_i = c_{i}^{T} \tanh(W_p \times q_w + b_p)
\tag{3}
$$

$$
\alpha_{i} = \frac{\exp(a_i)}{\sum_{j=1}^{M} \exp(a_j)}
\tag{4}
$$

where Wp ∈ RDq×Nf and bp ∈ RNf are projection parameters.
ここで、Wp∈RDq×Nf、bp∈RNfは射影パラメータである。
The final contextual representation ri of the i-th news title is the summation of the contextual representations of words weighted by their attention weights:
i番目のニュースタイトルの最終的な文脈表現riは、単語の文脈表現を注目重みで重み付けした総和である：

$$
r_{i} = \sum_{j=1}^{M} \alpha_{j} c_{j}
\tag{5}
$$

We apply the news encoder to all users’ clicked news and candidate news.
全ユーザーのクリックしたニュース、候補のニュースに対してニュースエンコーダーを適用する。
The representations of clicked news of a user and candidate news are respectively denoted as [r1, r2, ..., rN ] and [r ′ 0 , r ′ 1 , ..., r ′ K ], where N is the number of clicked news and K + 1 is the number of candidate news.
あるユーザのクリックしたニュースと候補となるニュースの表現をそれぞれ[r1, r2, ..., rN ]、[r′ 0 , r′ 1 , ..., r′ K ]とし、Nはクリックしたニュースの数、K + 1は候補ニュースの数であるとする。

## 3.2. User Encoder ユーザーエンコーダ

The user encoder module in our approach aims to learn the representations of users from the representations of their clicked news, as shown in Figure 2.
我々のアプローチにおけるユーザーエンコーダーモジュールは、図2に示すように、クリックされたニュースの表現からユーザの表現を学習することを目的としています。
In this module, a news-level personalized attention module is used to build informative user representations.
このモジュールでは、ニュースレベルのパーソナライズド・アテンション・モジュールが、情報量の多いユーザー表現を構築するために使用されます。
Usually the news clicked by the same user have different informativeness for learning user representations.
**通常、同じユーザーがクリックしたニュースは、ユーザー表現を学習するための情報量が異なる**。
For example, the news “10 tips for cooking” is very informative for modeling user preferences, but the news “It will be Rainy next week” is less informative.
例えば、「料理のコツ10選」というニュースはユーザーの嗜好をモデル化する上で非常に有益ですが、「来週は雨」というニュースはあまり有益ではない。(exampleがいちいちわかりやすい...!)
In addition, the same news also has different informativeness for modeling different users.
また、同じニュースでも、ユーザのモデリングによって情報量が異なる。
For example, the news “100 Greatest Golf Courses” is informative for characterizing users who are interested in golf, but is noisy for modeling users who are actually not interested in.
例えば、「ゴルフ場100選」というニュースは、ゴルフに興味のあるユーザーを特徴付けるには有益だが、実は興味のないユーザーをモデル化するにはノイジーである。
To model the different informativeness of the same news for different users, we also apply personalized attention mechanism to the representations of news clicked by the same user.
同じニュースでもユーザーによって情報量が異なることをモデル化するため、同じユーザーがクリックしたニュースの表現にもパーソナライズド・アテンション・メカニズムを適用しています。
Similar with the word-level attention network, we first transform the user embedding vector into a news preference query qd , which is formulated as:
単語レベルの注意ネットワークと同様に、まずユーザー埋め込みベクトルをニュース選好クエリqd に変換し、次のように定式化する：

$$
\tag{6}
$$

where Vd ∈ RDe×Dd and vd ∈ RDd are parameters, Dd is the dimension of the news preference query.
ここで、Vd∈RDe×Dd、vd∈RDdはパラメータ、Ddはニュース選好クエリの次元である。

We denote the attention weight of the i-th news as α ′ i , which is calculated by evaluating the importance of the interactions between the news preference query and news representations as follows:
i番目のニュースの注目度をα ′ i とし，ニュース選好クエリとニュース表現との間の相互作用の重要度を以下のように評価して算出する．

$$
\tag{7}
$$

$$
\tag{8}
$$

where Wd ∈ RDd×Nf and bd ∈ RNf are projection parameters.
ここで、Wd∈RDd×Nf、bd∈RNfは射影パラメータである。
The final user representation u is the summation of the news contextual representations weighted by their attention weights:
最終的なユーザー表現uは、ニュース文脈表現をその注目重みで重み付けしたものの総和である：

$$
\tag{9}
$$

## 3.3. Click Predictor クリックプレディクター

The click predictor module is used to predict the click score of a user on each candidate news.
クリック予測モジュールは、各候補ニュースに対するユーザーのクリックスコアを予測するために使用されます。
A common observation in news recommendation is that most users usually only click a few news displayed in an impression.
ニュースレコメンデーションにおいて、多くのユーザーは、表示されたニュースのうち数件しかクリックしないことが一般的である。
Thus, the number of positive and negative news samples is highly imbalanced.
このように、ポジティブなニュースとネガティブなニュースのサンプル数は、非常にアンバランスです。
In many neural news recommendation methods [20, 32], the model only predicts the click score for a single piece of news (the sigmoid activation function is usually used in these methods).
多くのニューラル・ニュース推薦法[20, 32]では、モデルは単一のニュースのクリックスコアを予測するだけです（これらの方法では通常シグモイド活性化関数が使用されます）。
In these methods, positive and negative news samples are manually balanced by randomly sampling, and the rich information provided by negative samples is lost.
これらの方法では、ポジティブなニュースサンプルとネガティブなニュースサンプルを無作為にサンプリングして手作業でバランスを取っているため、ネガティブなサンプルが提供する豊富な情報が失われています。
In addition, since the total number of news samples is usually huge, the computational cost of these methods is usually heavy during model training.
また、ニュースサンプルの総数が膨大になるため、モデル学習時の計算コストが重くなるのが一般的です。
Thus, these methods are sub-optimal for simulating realworld news recommendation scenarios.
したがって、これらの方法は、現実世界のニュース推薦シナリオをシミュレートするためには最適とは言えない。
Motivated by [13] and [38], we propose to apply negative sampling techniques by jointly predicting the click score for K +1 news during model training to solve the two problems above.
13]と[38]に動機づけられ、上記の2つの問題を解決するために、モデル学習中にK +1ニュースのクリックスコアを共同で予測することで、ネガティブサンプリング技術を適用することを提案します。
The K + 1 news consist of one positive sample of a user, and K randomly selected negative samples of a user.
K＋1ニュースは、あるユーザーの1つのポジティブサンプルと、ランダムに選ばれたK個のネガティブサンプルで構成されています。
The score yˆi of the candidate news D ′ i is calculated by the inner product of the news and user representation vector first, and then normalized by the softmax function, which is formulated as:
候補ニュースD′iのスコアyˆiは、まずニュースとユーザ表現ベクトルの内積で計算され、次にソフトマックス関数で正規化され、次のように定式化される：

$$
\tag{10}
$$

$$
\tag{11}
$$

For model training, we formulate the click prediction problem as a pseudo K + 1 way classification task, i.e., the clicked news is the positive class and all the rest news are negative classes.
すなわち、クリックされたニュースを正クラスとし、それ以外のニュースを負クラスとする。
We apply maximum likelihood method to minimize the log-likelihood on the positive class:
最尤法を適用し、正クラスでの対数尤度を最小化する：

$$
\tag{12}
$$

where yj is the gold label, S is the set of the positive training samples.
ここで、yjは金ラベル、Sは正の訓練サンプルの集合である。
By optimizing the loss function L via gradient descend, all parameters can be tuned in our model.
損失関数Lを勾配降下法で最適化することで、本モデルではすべてのパラメータを調整することが可能です。
Compared with existing news recommendation methods, our approach can effectively exploit the useful information in negative samples, and further reduce the computational cost for model training (nearly divided by K).
既存のニュース推薦手法と比較して、本アプローチはネガティブサンプルに含まれる有用な情報を効果的に利用することができ、モデル学習のための計算コスト（ほぼK分の1）をさらに削減することができます。
Thus, our model can be trained more easily on a large collection of news click logs.
このため、ニュースのクリックログの大規模なコレクションに対して、より容易にモデルを学習させることができる。

# 4. Experiments 実験

## 4.1. Datasets and Experimental Settings データセットと実験設定

Our experiments were conducted on a real-world dataset, which was constructed by randomly sampling user logs from MSN News1 in one month, i.e., from December 13rd, 2018 to January 12nd, 2019.
実験は、MSN News1のユーザーログを1ヶ月間、すなわち2018年12月13日から2019年1月12日までランダムにサンプリングして構築した実世界のデータセットで実施しました。
The detailed statistics of the dataset is shown in Table 12 .
データセットの詳細な統計は表12に示す通りである。
We use the logs in the last week as the test set, and the rest logs are used for training.
直近1週間のログをテストセットとして使用し、残りのログはトレーニングに使用します。
In addition, we randomly sampled 10% of samples for validation.
また、10％のサンプルを無作為に抽出し、検証を行いました。

In our experiments, the dimension D of word embedding was set to 300.
実験では、単語埋め込みの次元Dを300に設定した。
we used the pre-trained Glove embedding3 [25], which is trained on a corpus with 840 billion tokens, to initialize the embedding matrix.
の埋め込み行列を初期化するために、8,400億個のトークンを持つコーパスで学習済みのGlove埋め込み3 [25]を使用しました。
The number of CNN filters Nf was set to 400, and the window size was 3.
CNNのフィルター数Nfは400、ウィンドウサイズは3に設定した。
The dimension of user embedding De was set to 50.
ユーザー埋め込みDeの次元は50に設定された。
The sizes of word and news preferences queries (Dq and Dd ) were both set to 200.
単語とニュースの嗜好性クエリ（Dq、Dd）のサイズはいずれも200に設定した。
The negative sampling ratio K was set to 4.
負のサンプリング比Kは4とした。
We randomly sampled at most 50 browsed news articles to learn user representations.
ユーザー表現を学習するために、閲覧されたニュース記事を最大50件ランダムにサンプリングしました。
We applied dropout strategy [30] to each layer in our approach to mitigate overfitting.
オーバーフィッティングを軽減するために、本アプローチでは各層にドロップアウト戦略[30]を適用しました。
The dropout rate was set to 0.2.Adam [16] was used as the optimization algorithm for gradient descend.
ドロップアウト率は0.2.Adam [16]をgradient descendの最適化アルゴリズムとして使用しました。
The batch size was set to 100.
バッチサイズは100に設定しました。
Due to the limitation of GPU memory, the maximum number of clicked news for learning user representations was set to 50 in neural network based methods, and the maximum length of news title was set to 30.
GPUメモリの制限から、ニューラルネットワークベースの手法では、ユーザー表現を学習するためのクリックされたニュースの最大数を50に、ニュースのタイトルの最大長を30に設定しました。
These hyperparameters were selected according to the validation set.
これらのハイパーパラメータは、検証セットに従って選択された。
The metrics in our experiments include the average AUC, MRR, nDCG@5 and nDCG@10 scores over all impressions.
実験での指標は、全インプレッションの平均AUC、MRR、NDCG@5、NDCG@10スコアです。
We independently repeated each experiment for 10 times and reported the average performance.
各実験を独立して10回繰り返し、その平均値を報告した。

## 4.2. Performance Evaluation パフォーマンス評価

First, we will evaluate the performance of our approach by comparing it with several baseline methods.
まず、いくつかのベースライン手法と比較することで、本アプローチの性能を評価します。
The methods to be compared include:
比較する方式は以下の通りです：

- LibFM [28], which is a state-of-the-art feature-based matrix factorization and it is a widely used method for recommendation. In our experiments, we extract the TF-IDF features from users’ clicked news and candidate news, and concatenate both types of features as the input for LibFM. LibFM [28]は、最先端の特徴に基づく行列分解法であり、推薦に広く用いられている手法です。 実験では、ユーザーのクリックしたニュースと候補のニュースからTF-IDF特徴を抽出し、両特徴を連結してLibFMの入力としました。

- CNN [15], applying CNN to the word sequences in news titles and use max pooling technique to keep the most salient features, which is widely used in content-based recommendation [4, 40]. CNN [15]は、ニュースタイトルの単語列にCNNを適用し、最も顕著な特徴を保持するために最大プーリング技術を使用し、コンテンツベースの推薦に広く使用されている[4, 40]。

- DSSM [13], a deep structured semantic model with word hashing via character trigram and multiple dense layers. In our experiments, we concatenate all user’s clicked news as a long document as the query, and the candidate news are documents. The negative sampling ratio was set to 4. DSSM [13]は、文字トリグラムを介した単語ハッシュと複数の密な層を持つ深層構造化意味モデルである。 実験では、ユーザーがクリックしたニュースをすべて連結して長い文書としたものをクエリ、候補となるニュースを文書とした。 負のサンプリング比は4としました。

- Wide & Deep [5], using the combination of a wide channel using a linear transformer and a deep channel with multiple dense layers. The features we used are the same with LibFM for both channels. リニアトランスを使ったワイドチャンネルと、複数の緻密な層を持つディープチャンネルの組み合わせで、Wide & Deep [5] を実現しました。 使用した機能は、両チャンネルともLibFMで同じです。

- DeepFM [11], which is also a widely used neural recommendation method, using a combination with factorization machines and deep neural networks. We use the same TF-IDF features to feed for both components. 因数分解マシンとディープニューラルネットワークとの組み合わせによるニューラル推薦手法として、こちらも広く使われているDeepFM [11]。 両成分のフィードには、同じTF-IDF特徴を使用します。

- DFM [20], a deep fusion model by using combinations of dense layers with different depths. We use both TF-IDF features and word embeddings as the input for DFM. DFM[20]は、深さの異なる緻密なレイヤーの組み合わせによるディープフュージョンモデル。 DFMの入力として、TF-IDF特徴量と単語埋め込み量の両方を使用します。

- DKN [32], a deep news recommendation method with Kim CNN and news-level attention network. They also incorporated entity embeddings derived from knowledge graphs. DKN [32]は、Kim CNNとニュースレベルのアテンションネットワークによるディープニュース推薦手法です。 また、知識グラフから得られるエンティティ埋め込みを取り入れた。

- NPA, our neural news recommendation approach with personalized attention. パーソナライズされた注意を喚起するニューラル・ニュースレコメンデーション・アプローチ、NPA。

The experimental results on news recommendation are summarized in Table 2.
ニュース推薦に関する実験結果を表2にまとめた。
According to Table 2, We have several observations.
表2によると、我々はいくつかの観察結果を得た。

First, the methods based on neural networks (e.g., CNN, DSSM and NPA) outperform traditional matrix factorization methods such as LibFM.
まず、ニューラルネットワークに基づく手法（CNN、DSSM、NPAなど）は、LibFMのような従来の行列分解法を凌駕しています。
This is probably because neural networks can learn more sophisticated features than LibFM, which is beneficial for learning more informative latent factors of users and news.
これは、ニューラルネットワークがLibFMよりも高度な特徴量を学習できるため、ユーザーやニュースのより情報量の多い潜在因子を学習するのに有利なためと考えられます。

Second, the methods using negative sampling (DSSM and NPA) outperform the methods without negative sampling (e.g., CNN, DFM and DKN).
次に、ネガティブサンプリングを用いた手法（DSSM、NPA）は、ネガティブサンプリングを用いない手法（CNN、DFM、DKNなど）を上回った。
This is probably because the methods without negative sampling are usually trained on a balanced dataset with the same number of positive and negative samples, and cannot effectively exploit the rich information conveyed by negative samples.
これは、ネガティブサンプリングを行わない手法が、通常、ポジティブサンプルとネガティブサンプルを同数含むバランスのとれたデータセットで学習されるため、ネガティブサンプルが伝える豊富な情報を効果的に利用できないためと思われます。
DSSM and our NPA approach can utilize the information from three more times of negative samples than other baseline methods, which is more suitable for real-world news recommendation scenarios.
DSSMと我々のNPAアプローチは、他のベースライン手法よりも3倍以上のネガティブサンプルからの情報を利用することができ、これは実世界のニュース推薦シナリオにより適している。

Third, the deep learning methods using attention mechanism (DFM, DKN and NPA) outperform most of the methods without attention mechanism (CNN, Wide & Deep and DeepFM).
第三に、注意メカニズムを用いた深層学習法（DFM、DKN、NPA）は、注意メカニズムを用いない方法（CNN、Wide & Deep、DeepFM）のほとんどを凌駕しています。
This is probably because different news and their contexts usually have different informativeness for recommendation, and selecting the important features of news and users is useful for achieving better recommendation performance.
これは、ニュースやその文脈が異なれば、推薦のための情報量も異なるため、ニュースやユーザーの重要な特徴を選択することが、より良い推薦性能を実現するために有効であるためと思われる。

Fourth, our approach can consistently outperform all compared baseline methods.
第四に、我々のアプローチは、比較したすべてのベースライン手法を一貫して上回ることができる。
Although DSSM also use negative sampling techniques to incorporate more negative samples, it cannot effectively utilize the contextual information and word orders in news titles.
DSSMもネガティブサンプリングの手法を用いて、より多くのネガティブサンプルを取り込むことができますが、ニュースタイトルの文脈情報や語順を有効に活用することはできません。
Thus, our approach can outperform DSSM.
したがって、我々のアプローチはDSSMを凌駕することができます。
In addition, although DFM uses attention mechanism to select important user features, it also cannot effectively model the contexts within news titles, and cannot select important words in the candidate news titles.
また、DFMはアテンションメカニズムを用いて重要なユーザー特徴を選択しますが、ニュースタイトル内のコンテキストを効果的にモデル化することができず、ニュースタイトル候補に含まれる重要な単語を選択することができないことも特徴です。
Besides, although DKN uses a news-level attention network to select the news clicked by users, it cannot model the informativeness of different words.
また、DKNはニュースレベルのアテンションネットワークを使って、ユーザーがクリックしたニュースを選択しますが、異なる単語の情報性をモデル化することはできません。
Different from all these methods, our approach can dynamically recognize important words and news according to user preferences.
これらの方法とは異なり、私たちのアプローチは、ユーザーの好みに応じて重要な単語やニュースを動的に認識することができます。
Thus, our approach can outperform these methods.
したがって、我々のアプローチはこれらの方法を凌駕することができます。

Next, we will compare the computational cost of our approach and the baseline methods.
次に、我々のアプローチとベースライン手法の計算コストを比較します。
To summarize, the comparisons are shown in Table 34 .
要約すると、比較対象は表34に示すとおりである。
We assume that during the online test phase, the model can directly use the intermediate results produced by hidden layers.
オンラインテストの段階では、モデルは隠れ層が生成した中間結果を直接利用できると仮定しています。
From Table 3, we have several observations.
表3から、いくつかの観察結果が得られた。

First, comparing our NPA approach with feature-based methods, the computational cost on time and memory during training is lower if N is not large, since the dimension Df of the feature vector is usually huge due to the dependency on bag-of-words features.5 In addition, the computational cost in the test phase is only a little more expensive than these methods since De is not large.
まず、特徴量ベースの手法と比較すると、特徴量ベクトルの次元Dfは、通常、Bag-of-Words特徴量に依存するため、Nが大きくない場合、学習時の時間とメモリに関する計算コストが低くなる5。また、テスト段階での計算コストは、Deが大きくないため、これらの手法よりも少し高い程度である。

Second, comparing our NPA approach with CNN, DFM and DKN, the training cost is actually divided by K with the help of negative sampling.
次に、我々のNPAアプローチとCNN、DFM、DKNを比較すると、ネガティブサンプリングの助けを借りて、実際に学習コストをKで割っています。
In addition, the computational cost of NPA in the test phase much smaller than DKN and DFM, since DKN needs to use the representations of the candidate news as the query of the news-level attention network and the score needs to be predicted by encoding all news clicked by a user, which is very computationally expensive.
また、DKNはニュースレベルのアテンションネットワークのクエリとして候補ニュースの表現を使用する必要があり、ユーザーがクリックしたすべてのニュースを符号化してスコアを予測する必要があるため、非常に計算コストがかかるため、テストフェーズにおけるNPAの計算コストはDKNやDFMよりもはるかに小さくなっています。
DFM needs to take the sparse feature vector as input, which is also computationally expensive.
DFMはスパースな特徴ベクトルを入力とする必要があり、これも計算量が多い。
Different from these baseline methods, our approach can be trained at a low computational cost, and can be applied to online services to handle massive users at a satisfactory computational cost.
これらのベースライン手法とは異なり、我々のアプローチは低い計算コストで学習させることができ、満足のいく計算コストで大規模なユーザーを扱うオンラインサービスに適用することができる。

Finally, we want to evaluate the performance of our approach in each day to explore the influence of user click behaviors over time.
最後に、ユーザーのクリック行動の経時的な影響を探るため、各日における本アプローチの性能を評価したいと思います。
The performance of our approach in each day of the week for test (1/6/2019-1/12/2019) is shown in Figure 4.
テスト用の各曜日（2019/1/6～2019/1/12）における本アプローチのパフォーマンスを図4に示します。
According to the results, the performance of our approach is best on the first day in the test week (1/6/2019).
結果によると、テスト週の初日（2019/1/6）に、本アプローチのパフォーマンスが最も良くなっています。
This is intuitive because the relevance of user preferences is usually strong between neighbor days.
これは、ユーザーの嗜好の関連性が、通常、近隣の日間で強くなるため、直感的に理解できる。
In addition, as time went by, the performance of our approach begins to decline.
また、時間が経つにつれて、私たちのアプローチの性能は低下し始めます。
This is probably because news are usually highly timesensitive and most articles in common news services will be no longer recommended for users within several days (Usually two days for MSN news).
これは、通常、ニュースは非常にタイムセンシティブであり、一般的なニュースサービスの記事のほとんどは、数日以内にユーザーに推奨されなくなる（通常、MSNニュースでは2日）ためと思われます。
Thus, more news will not appear in the training set over time, which leads to the performance decline.
そのため、時間の経過とともにトレーニングセットに登場しないニュースが増え、性能低下につながります。
Fortunately, we also find the performance of our approach tends to be stable after three days.
幸いなことに、私たちのアプローチの性能は、3日後にも安定する傾向があることがわかりました。
It shows that our model does not simply memorize the news appear in the training set and can make personalized recommendations based on user preferences and news topics.
この結果は、本モデルが単にトレーニングセット内のニュースを記憶しているのではなく、ユーザーの好みやニュースのトピックに基づいてパーソナライズされたレコメンデーションを行うことができることを示しています。
Thus, our model is robust to the news update over time.
したがって、我々のモデルは、時間の経過に伴うニュースの更新に対して頑健である。

## 4.3. Effectiveness of Personalized Attention パーソナライズド・アテンションの有効性

In this section, we conducted several experiments to explore the effectiveness of the personalized attention mechanism in our NPA approach.
このセクションでは、私たちのNPAアプローチにおけるパーソナライズド・アテンション・メカニズムの有効性を探るために、いくつかの実験を行いました。
First, we want to validate the advantage of personalized attention on vanilla non-personalized attention for news recommendation.
まず、ニュース推薦において、バニラの非パーソナライズド・アテンションに対するパーソナライズド・アテンションの優位性を検証したいと思います。
The performance of NPA and its variant using vanilla attention and without attention is shown in Figure 5.
バニラアテンションを使用したNPAとその変形の性能とアテンションなしの性能を図5に示します。
According to Figure 5, we have several observations.
図5によると、いくつかの観察結果があります。
First, the models with attention mechanism consistently outperform the model without attention.
まず、注目機構を持つモデルは、注目機構を持たないモデルを一貫して上回ります。
This is probably because different words and news usually have different informativeness for news recommendation.
これは、単語やニュースが異なると、ニュース推薦のための情報量が異なるためと考えられます。
Therefore, using attention mechanism to recognize and highlight important words and news is useful for learning more informative news and user representations.
したがって、重要な単語やニュースを認識し強調するアテンション機構を用いることで、より有益なニュースやユーザー表現を学習するのに有効です。
In addition, our model with personalized attention outperforms its variant with vanilla attention.
さらに、パーソナライズド・アテンションを用いたモデルは、バニラ・アテンションを用いたモデルを凌駕しています。
This is probably because the same words and news should have different informativeness for the recommendation of different users.
これは、同じ言葉やニュースでも、ユーザーによって推薦のための情報量が異なるためと思われます。
However, vanilla attention networks usually use a fixed query vector, and cannot adjust to different user preferences.
しかし、バニラアテンションネットワークは通常、固定されたクエリベクトルを使用し、異なるユーザーの嗜好に適応することができません。
Different from vanilla attention, our personalized attention approach can dynamically attend to important words and news according to user characteristics, which can benefit news and user representation learning.
バニラアテンションとは異なり、パーソナライズドアテンションは、ユーザーの特性に合わせて重要な単語やニュースに動的にアテンションすることができ、ニュースやユーザー表現の学習に役立てることができます。

Then, we want to validate the effectiveness of the personalized attention at word-level and news-level.
そして、単語レベル、ニュースレベルでパーソナライズド・アテンションの効果を検証したいと思います。
The performance of NPA and its variant with different combinations of personalized attention is shown in Figure 6.
パーソナライズド・アテンションの組み合わせを変えたNPAとその変形のパフォーマンスを図6に示します。
According to Figure 6, we have several observations.
図6によると、いくつかの観察結果があります。
First, the word-level personalized attention can effectively improve the performance of our approach.
まず、単語レベルのパーソナライズド・アテンションは、我々のアプローチのパフォーマンスを効果的に向上させることができます。
This is probably because words are basic units to convey the meanings of news titles and selecting the important words according to user preferences is useful for learning more informative news representations for personalized recommendation.
これは、単語がニュースタイトルの意味を伝える基本単位であり、ユーザーの好みに応じて重要な単語を選択することで、より情報量の多いニュース表現を学習し、パーソナライズド推薦に役立てるためと考えられる。
Second, the news-level personalized attention can also improve the performance of our approach.
第二に、ニュースレベルのパーソナライズされた注目は、我々のアプローチのパフォーマンスを向上させることもできます。
This is probably because news clicked by users usually have different informativeness for learning user representations, and recognizing the important news is useful for learning high quality user representations.
これは、ユーザーがクリックしたニュースは、通常、ユーザー表現を学習するための情報量が異なるため、重要なニュースを認識することが、質の高いユーザー表現を学習するために有効であるためと考えられる。
Third, combining both word- and news-level personalized attention can further improve the performance of our approach.
第三に、単語レベルとニュースレベルのパーソナライズド・アテンションを組み合わせることで、本アプローチの性能をさらに向上させることができます。
These results validate the effectiveness of the personalized attention mechanism in our approach.
これらの結果は、本アプローチにおけるパーソナライズド・アテンション・メカニズムの有効性を検証するものです。

## 4.4. Influence of Negative Sampling #ネガティブサンプリングの影響

In this section, we will explore the influence of the negative sampling technique on the performance of our approach.
このセクションでは、ネガティブサンプリング技術が本アプローチの性能に及ぼす影響を探る。
To validate the effectiveness of negative sampling, we compare the performance of our approach with its variant without negative sampling.
ネガティブサンプリングの有効性を検証するため、本アプローチの性能をネガティブサンプリングなしのバリアントと比較しました。
Following [20, 32], we choose to train this variant on a balanced training set by predicting the click scores of news articles one by one (the final activation function is changed to sigmoid).
20,32]に倣って，この変種はバランスのとれた訓練セットで，ニュース記事のクリックスコアを一つずつ予測することで訓練することにした（最後の活性化関数はシグモイドに変更した）．
The experimental results are shown in Figure 7.
実験結果を図7に示します。
According to Figure 7, the performance of our approach can be effectively improved via negative sampling.
図7によれば、ネガティブサンプリングによって、本アプローチの性能を効果的に向上させることができる。
Since negative samples are dominant in the training set, they usually contain rich information for recommendation.
学習セットにはネガティブなサンプルが多く含まれるため、通常、推薦に必要な情報が豊富に含まれています。
However, the information provided by negative samples cannot be effectively utilized due to the limitation of balanced sampling.
しかし、バランスサンプリングの限界から、ネガティブサンプルから得られる情報を有効活用することはできません。
Therefore, the performance is usually sub-optimal.
そのため、通常、性能は最適でない。
Different from this variant, our NPA approach can incorporate richer information in negative samples, which may be very useful for achieving better performance on news recommendation.
このようなアプローチとは異なり、我々のNPAアプローチは、ネガティブサンプルに豊富な情報を取り込むことができ、ニュース推薦のパフォーマンスを向上させるのに非常に有用であると考えられる。

## 4.5. Hyperparameter Analysis ハイパーパラメータ解析

In this section, we will explore the influence of an important hyperparameter in our approach, i.e., the negative sampling ratio K, which aims to control the number of negative samples to combine with a positive sample.
このセクションでは、我々のアプローチにおける重要なハイパーパラメータ、すなわち、正のサンプルと組み合わせる負のサンプルの数を制御することを目的とする負のサンプリング比Kの影響を探る。
The experimental results on K are shown in Figure 8.
Kでの実験結果を図8に示します。
According to Figure 8, we find the performance of our approach first consistently improves when K increases.
図8によると、Kが増加すると、我々のアプローチの性能がまず一貫して向上することがわかります。
This is probably because when K is too small, the number of negative samples incorporated for training is also small, and the useful information provided by negative samples cannot be fully exploited, which will lead to sub-optimal performance.
これは、Kが小さすぎると、学習に組み込むネガティブサンプルの数も少なくなり、ネガティブサンプルが提供する有用な情報を十分に活用できず、最適とは言えない性能になるためと思われます。
However, when K is too large, the performance will start to decline.
ただし、Kが大きすぎると、性能が低下し始めます。
This is probably because when too many negative samples are incorporated, they may become dominant and it is difficult for the model to correctly recognize the positive samples, which will also lead to sub-optimal performance.
これは、ネガティブサンプルを多く取り込みすぎると、ネガティブサンプルが支配的になり、ポジティブサンプルをモデルが正しく認識することが難しくなり、これも最適なパフォーマンスではなくなるためと思われます。
Thus, a moderate setting of K may be more appropriate (e.g., K = 4).
したがって、Kを適度に設定することがより適切であると考えられる（例：K＝4）。

## 4.6. Case Study ケーススタディ

In this section, we will conduct several case studies to visually explore the effectiveness of the personalized attention mechanism in our approach.
このセクションでは、いくつかのケーススタディを行い、本アプローチにおけるパーソナライズド・アテンション・メカニズムの有効性を視覚的に探っていきます。
First, we want to explore the effectiveness of the word-level personalized attention.
まず、単語レベルのパーソナライズド・アテンションの有効性を探りたい。
The visualization results of the clicked and candidate news from two sample users are shown in Figure 9(a).
サンプルユーザー2名のクリックしたニュースと候補のニュースの可視化結果を図9（a）に示す。
From Figure 9(a), we find the attention network can effectively recognize important words within news titles.
図9(a)から、アテンションネットワークは、ニュースタイトル内の重要な単語を効果的に認識できることがわかります。
For example, the word “nba” in the second news of user 1 is assigned high attention weight since it is very informative for modeling user preferences, while the word “survey” in the same title gains low attention weight since it is not very informative.
例えば、ユーザー1の2つ目のニュースに含まれる「nba」という単語は、ユーザーの嗜好をモデル化する上で非常に有益であるため注目度が高く、同じタイトルの「survey」という単語はあまり有益でないため注目度が低くなっています。
In addition, our approach can calculate different attention weights for the words in the same news titles to adjust to the preferences of different users.
また、本アプローチでは、同じニュースタイトルに含まれる単語に対して異なる注目度の重みを計算し、異なるユーザーの嗜好に合わせることができます。
For example, according to the clicked news, user 1 may be interested in sports news and user 2 may be interested in movie related news.
例えば、クリックされたニュースによると、ユーザー1はスポーツのニュースに興味があり、ユーザー2は映画関連のニュースに興味がある可能性があります。
The words “super bowl” are highlighted for user 1 and the words “superheroes” and “movies” are highlighted for user 2.
ユーザー1には「スーパーボール」の文字が、ユーザー2には「スーパーヒーロー」「映画」の文字がハイライト表示されます。
These results show that our approach can learn personalized news representations by incorporating personalized attention.
これらの結果は、本アプローチがパーソナライズされた注意を取り入れることで、パーソナライズされたニュース表現を学習できることを示しています。

Then, we want to explore the effectiveness of the news-level attention network.
次に、ニュースレベルのアテンションネットワークの有効性を探りたい。
The visualization results of the clicked news are shown in Figure 9(b).
クリックされたニュースの可視化結果を図9(b)に示す。
From Figure 9(b), we find our approach can also effectively recognize important news of a user.
図9(b)から、本アプローチはユーザーの重要なニュースも効果的に認識できることがわかります。
For example, the news “nfl releases playoff schedule : cowboys-seahawks on saturday night” gains high attention weight because it is very informative for modeling the preferences of user 1, since he/she is very likely to be interested in sports according to the clicked news.
例えば、「nfl releases playoff schedule : cowboys-seahawks on saturday night」というニュースは、クリックしたニュースからスポーツに興味がありそうなユーザー1の嗜好をモデル化するのに非常に参考になるため、高い注目度を獲得する。
The news “new year’s eve weather forecast” is assigned low attention weight, since it is uninformative for modeling user preferences.
大晦日の天気予報」というニュースは、ユーザーの嗜好をモデル化する上で参考にならないため、注目度は低く設定されています。
In addition, our approach can model the different informativeness of news for learning representations of different users.
さらに、本アプローチでは、ユーザーごとに異なる学習表現に対するニュースの情報量の違いをモデル化することができます。
For example, the same sports news “10 nfl coaches who could be fired on black monday” is assigned high attention weight for user 1, but relatively low for user 2.
例えば、同じスポーツニュース「10 nfl coaches who could be fired on black monday」でも、ユーザー1には高い注目度が割り当てられるが、ユーザー2には比較的低い注目度となる。
According to the clicked news of both users, user 1 is more likely to be interested in sports than user 2 and this news may be noisy for user 2.
両ユーザーのクリックしたニュースによると、ユーザー1はユーザー2よりもスポーツに興味がある可能性が高く、このニュースはユーザー2にとってノイズとなり得る。
These results show that our model can evaluate the different importance of the same news for different users according to their preferences.
これらの結果は、本モデルが、同じニュースでもユーザーによって異なる重要度を、ユーザーの好みに応じて評価できることを示しています。

# 5. Conclusion 結論

In this paper, we propose a neural news recommendation approach with personalized attention (NPA).
本論文では、パーソナライズド・アテンションを用いたニューラル・ニュース推薦アプローチ（NPA）を提案する。
In our NPA approach, we use a news representation model to learn news representations from titles using CNN, and use a user representation model to learn representations of users from their clicked news.
NPAのアプローチでは、CNNを用いてタイトルからニュース表現を学習するニュース表現モデルと、クリックされたニュースからユーザーの表現を学習するユーザー表現モデルを用いています。
Since different words and news articles usually have different informativeness for representing news and users, we proposed to apply attention mechanism at both word- and news to help our model to attend to important words and news articles.
通常、単語やニュース記事は、ニュースやユーザーを表現するための情報量が異なるため、単語とニュースの両方で注目メカニズムを適用し、モデルが重要な単語やニュース記事に注目することを支援することを提案しました。
In addition, since the same words and news usually have different importance for different users, we propose a personalized attention network which exploits the embeddings of user ID as the queries of the word- and news-level attention networks.
また、同じ単語やニュースでもユーザによって重要度が異なるため、ユーザIDの埋め込みを単語レベルとニュースレベルのアテンションネットワークのクエリとして利用するパーソナライズド・アテンションネットワークを提案します。
The experiments on the real-world dataset collected from MSN news validate the effectiveness of our approach.
MSNニュースから収集した実世界のデータセットでの実験により、本アプローチの有効性が検証された。
