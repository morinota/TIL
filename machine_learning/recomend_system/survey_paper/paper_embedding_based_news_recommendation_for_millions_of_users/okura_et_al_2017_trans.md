### 0.1. link 0.1. リンク

- https://dl.acm.org/doi/abs/10.1145/3097983.3098108?casa_token=E2V72vGAK60AAAAA:b1coQnhN8zeSe6KNZrv_2T3HC5NfMI5LtYH7Mrj9ckNTblQQuiP9FEvoPtpGYnIN5hbNA7zEwefO6qvo
- httpsを使用しています。

### 0.2. title 0.2. タイトル

Embedding-based News Recommendation for Millions of Users
数百万人のユーザーを対象にした埋め込み型ニュース推薦システム

### 0.3. ABSTRACT 0.3. ABSTRACT

It is necessary to understand the content of articles and user preferences to make effective news recommendations. While ID-based methods, such as collaborative filtering and low-rank factorization, are well known for making recommendations, they are not suitable for news recommendations because candidate articles expire quickly and are replaced with new ones within short spans of time. Word-based methods, which are often used in information retrieval settings, are good candidates in terms of system performance but have issues such as their ability to cope with synonyms and orthographical variants and define "queries" from users' historical activities. This paper proposes an embedding-based method to use distributed representations in a three step end-to-end manner: (i) start with distributed representations of articles based on a variant of a denoising autoencoder, (ii) generate user representations by using a recurrent neural network (RNN) with browsing histories as input sequences, and (iii) match and list articles for users based on inner-product operations by taking system performance into consideration. The proposed method performed well in an experimental offline evaluation using past access data on Yahoo! JAPAN's homepage. We implemented it on our actual news distribution system based on these experimental results and compared its online performance with a method that was conventionally incorporated into the system. As a result, the click-through rate (CTR) improved by 23% and the total duration improved by 10%, compared with the conventionally incorporated method. Services that incorporated the method we propose are already open to all users and provide recommendations to over ten million individual users per day who make billions of accesses per month.
効果的なニュース推薦を行うためには、記事の内容やユーザの嗜好を理解する必要がある。 推薦を行う手法としては、協調フィルタリングや低ランク因子分解などのIDベースの手法がよく知られているが、候補となる記事はすぐに期限切れとなり、短いスパンで新しい記事に入れ替わるため、ニュース推薦には適さない。 また、情報検索の分野でよく用いられる単語ベースの手法は、システム性能の点では良い候補であるが、同義語や表記ゆれへの対応や、ユーザの過去の行動から「クエリ」を定義するなどの問題がある。 本論文では、(i)ノイズ除去オートエンコーダの変形に基づく記事の分散表現から始め、(ii)閲覧履歴を入力列とするリカレントニューラルネットワーク（RNN）を用いてユーザ表現を生成し、(iii)システム性能を考慮した内積演算に基づいてユーザの記事を照合・リスト化するという3段階でエンドツーエンドで利用する埋め込み型方式を提案する。 提案手法は、Yahoo! JAPANのホームページの過去のアクセスデータを用いたオフラインでの実験評価において、良好な結果を得ました。 この実験結果をもとに実際のニュース配信システムに実装し、従来からシステムに組み込まれている手法とオンライン性能を比較しました。 その結果、従来手法と比較して、クリックスルー率（CTR）が23％、総時間が10％改善されました。 私たちが提案する手法を取り入れたサービスは、すでにすべてのユーザーに公開されており、1日1千万人以上、1カ月に数十億回のアクセスをする個人ユーザーにおすすめ情報を提供しています。

## 1. INTRODUCTION 1. はじめに

It is impossible for users of news distributions to read all available articles due to limited amounts of time. Thus, users prefer news services that can selectively provide articles. Such selection is typically done manually by editors and a common set of selected stories are provided to all users in outmoded media such as television news programs and newspapers. However, we can identify users before they select articles that will be provided to them on the Internet by using information, such as that in user ID cookies, and personalize the articles for individual users [3, 22].
ニュース配信の利用者は，限られた時間の中で，配信されているすべての記事を読むことは不可能. そのため，ユーザは記事を選択的に提供できるニュースサービスを好む。 テレビのニュース番組や新聞のような時代遅れのメディアでは、このような選択は通常編集者の手作業で行われ、選択された記事の共通のセットが全ユーザに提供される。 しかし，インターネット上では，ユーザIDクッキーなどの情報を利用して，提供される記事を選択する前にユーザを特定し，個々のユーザに対して記事をパーソナライズすることができる[3, 22]。

ID-based methods, such as collaborative filtering and low-rank factorization, are well known in making recommendations. However, Zhong et al. [22] suggested that such methods were not suitable for news recommendations because candidate articles expired too quickly and were replaced with new ones within short time spans. Thus, the three keys in news recommendations are: Understanding the content of articles, • Understanding user preferences, and • Listing selected articles for individual users based on content and preferences.
ID ベースの推薦方法としては，協調フィルタリングや低ランク因子法などがよく知られている． しかし，Zhong ら[22]は，候補となる記事の期限が切れるのが早く，短時間で新しい記事に置き換わるため，こうした手法はニュース推薦には適さないとしている． このように、ニュース推薦における鍵は以下の3つである。 このように，ニュース推薦の鍵は，記事の内容を理解すること， - ユーザーの嗜好を理解すること， - 内容と嗜好に基づいて個々のユーザーに対して選択された記事をリストアップすることの 3 点である．

In addition, it is important to make recommendations in the real world [14] that respond to scalability and noise in learning data [14]. Applications also need to return responses within hundreds of milliseconds with every user access.
さらに、学習データのスケーラビリティやノイズに対応した実世界でのレコメンデーション[14]が重要である。 また、アプリケーションは、ユーザーのアクセスごとに数百ミリ秒以内にレスポンスを返す必要がある。

A baseline implementation to cover the three keys would be as follows. An article is regarded as a collection of words included in its text. A user is regarded as a collection of words included in articles he/she has browsed. The implementation learns click probability using co-occurrence of words between candidates of articles and browsing histories as features.
3つの鍵をカバーする基本的な実装は以下のようになる。 記事は、そのテキストに含まれる単語の集まりとみなされる。 ユーザは、自分が書いた記事に含まれる単語の集まりとみなす。

This method has some practical advantages. It can immediately reflect the latest trends because the model is very simple so that the model can be taught to learn and update in short periods of time. The estimation of priority can be quickly calculated using existing search engines with inverted indices on words.
この方法には、実用的な利点がある。 モデルが非常に単純であるため、短期間で学習・更新が可能であるため、最新のトレンドを即座に反映できる。 優先度の推定は、単語の転置インデックスを持つ既存の検索エンジンを用いて迅速に計算することができる。

The previous version of our implementation was based on this method for these reasons. However, it had some issues that may have had a negative impact on the quality of recommendations. The first regarded the representation of words. When a word was used as a feature, two words that had the same meaning were treated as completely different features if the notations were different. This problem tended to emerge in news articles when multiple providers separately submitted articles on the same event. The second regarded the handling of browsing histories. Browsing histories were handled as a set in this approach. However, they were actually a sequence, and the order of browsing should have represented the transition of user interests. We also had to note large variances in history lengths by users that ranged from private browsing to those who visited sites multiple times per hour. Deep-learning-based approaches have recently been reported to be effective in various domains. Distributed representations of words thoroughly capture semantic information [11, 16]. Recurrent neural networks (RNNs) have provided effective results as a method of handling input sequences of variable length [9, 15, 17].
前バージョンの実装は、これらの理由からこの方法に基づいていました。 しかし、レコメンデーションの品質に悪影響を及ぼす可能性のある問題がいくつかあった。 ひとつは、単語の表現方法である。 単語を特徴量とした場合、同じ意味の単語でも表記が違えば全く別の特徴量として扱われてしまう。 この問題は、同じ出来事について複数のプロバイダが別々に記事を投稿したニュース記事で発生しがちであった。 二つ目は、閲覧履歴の扱いである。 本手法では、閲覧履歴を集合として扱っている。 しかし、履歴は連続したものであり、本来であれば閲覧の順番がユーザの興味の変遷を表すものである。 また、私的な閲覧から1時間に何度もサイトを訪れるユーザーまで、履歴の長さに大きなばらつきがあることに注意する必要がありました。 近年、様々な領域でディープラーニングを用いたアプローチが有効であることが報告されています。 単語の分散表現により、意味情報を徹底的に捉える[11, 16]。 リカレントニューラルネットワーク（RNN）は、可変長の入力列を扱う手法として有効な結果を出している[9, 15, 17]。

If we build a model with a deep network using an RNN to estimate the degree of interest between users and articles, on the other hand, it is difficult to satisfy the response time constraints on accesses in real systems. This paper proposes an embedding-based method of using distributed representations in a three step endto-end manner from representing each article to listing articles for each user based on relevance and duplication: Start with distributed representations of articles based on a variant of the denoising autoencoder (which addresses the first issue in Section 3). • Generate user representations by using an RNN with browsing histories as input sequences (which addresses the second issue in Section 4). • Match and list articles for each user based on the inner product of article-user for relevance and article-article for de-duplication (outlined in Section 2).
一方、RNNを用いたディープネットワークでモデルを構築し、ユーザと記事の間の関心度を推定すると、**実システムにおけるアクセスの応答時間制約を満たすことが困難**となる。 本論文では、各記事の表現から、関連性と重複に基づく各ユーザーの記事のリストアップまで、3段階のエンドツーエンドで分散表現を利用する埋め込みベースの手法を提案する。 **ノイズ除去オートエンコーダの変形に基づく記事の分散表現**から始める（これはセクション3で最初の問題に対処する）。 - 閲覧履歴を入力列とするRNNを用いてユーザ表現を生成する（セクション4の第二の課題に対応）。 - 記事-ユーザ間の関連性と記事-記事の重複排除の内積に基づいて、各ユーザの記事をマッチングしリスト化する（セクション2で概説）。

The key to our method is using a simple inner product to estimate article-user relevance. We can calculate article representations and user representations before user visits in sufficient amounts of time. When a user accesses our service, we only select his/her representations and calculate the inner product of candidate articles and the representations. Our method therefore both expresses complex relations that are included in the user’s browsing history and satisfies the response time constraints of the real system.
我々の手法の鍵は、記事とユーザーの関連性を推定するために単純な内積を使うことである。 我々は、ユーザーがアクセスする前に、十分な量の記事表現とユーザー表現を計算することができる。 ユーザが我々のサービスにアクセスしたとき、我々は彼の

The proposed method was applied to our news distribution service for smartphones, which is described in the next section. We compared our method to a conventional approach, and the results (see Section 6) revealed that the proposed method outperformed the conventional approach with a real service as well as with static experimental data, even if disadvantages, such as increased learning time and large latency in model updates, are taken into consideration.
提案手法を次節で述べるスマートフォン向けニュース配信サービスに適用しました。 提案手法を従来手法と比較した結果（6章参照），学習時間の増加やモデル更新の遅延が大きいなどのデメリットを考慮しても，実サービスや静的実験データにおいて提案手法が従来手法を上回る性能を持つことが明らかとなった．

## 2. OUR SERVICE AND PROCESS FLOW 2. 当社のサービスおよびプロセスの流れ

The methods discussed in this paper were designed to be applied to the news distribution service on the homepage of Yahoo! JAPAN on smartphones. The online experiments described in Section 6 were also conducted on this page. This section introduces our service and process flow.
本稿で取り上げた手法は，スマートフォンにおけるYahoo! JAPANのトップページでのニュース配信サービスに適用することを想定している． また，6 章で述べたオンライン実験もこのページで行った． 本節では，サービスおよび処理の流れについて紹介する．

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/2-Figure1-1.png">

Figure 1: Example of Yahoo! JAPAN’s homepage on smartphones. This paper discusses methods of providing articles in Personalized module.
図1：スマートフォンにおけるYahoo! JAPANのトップページの例。 本稿では、Personalizedモジュールでの記事提供方法について述べる。

Figure 1 has a mockup of our service that was renewed in May 2015. There is a search window and links to other services at the top as a header. The middle part, called the Topics module, provides six articles on major news selected by human professionals for a general readership. The bottom part, called the Personalized module, provides many articles and advertising that has been personalized for individual users. Users in the Personalized module can see as many articles as they want if they scroll down to the bottom. Typical users scroll down to browse the approximately top 20 articles. This paper describes optimization to provide articles in the Personalized module
図1には、2015年5月にリニューアルした当社サービスのモックアップがあります。 ヘッダーとして上部に検索窓と他サービスへのリンクがあります。 中段はTopicsモジュールと呼ばれ、人間の専門家が選んだ主要なニュースを一般読者向けに6記事提供しています。 下はPersonalizedモジュールと呼ばれ、個々のユーザー向けにパーソナライズされた多くの記事や広告が提供されます。 パーソナライズドモジュールのユーザーは、一番下までスクロールすれば、好きなだけ記事を見ることができます。 一般的なユーザーは、スクロールダウンして上位20記事程度を閲覧する。 本稿では、Personalizedモジュールで記事を提供するための最適化について説明する。

Five processes are executed to select articles for millions of users for each user access.Identify: Obtain user features calculated from user history in advance. • Matching: Extract articles from all those available using user features. • Ranking: Rearrange list of articles on certain priorities. • De-duplication: Remove articles that contain the same information as others. • Advertising: Insert ads if necessary.
ユーザーアクセスごとに数百万人分の記事を選択するため、5つのプロセスを実行する.Identify: ユーザー履歴から算出したユーザーの特徴を事前に取得する。 - マッチング：ユーザーの特徴を用いて、利用可能なすべての記事から記事を抽出する。 - ランキング ある優先順位で記事のリストを並べ替える。 - 重複排除 他の記事と同じ情報を含む記事を削除する。 - 広告 必要であれば、広告を挿入します。

These processes have to be done within hundreds of milliseconds between user requests and when they are displayed because available articles are constantly changing. In fact, as all articles in our service expire within 24 hours from the viewpoint of information freshness, tens of thousands of new articles are posted every day, and the same number of old articles are removed due to expiration. Thus, each process adopts computationally light methods that leverage pre-computed distributed article representations (described in Section 3) and user representations (described in Section 4).
これらの処理は、利用可能な記事が常に変化しているため、ユーザーがリクエストしてから表示されるまでの数百ミリ秒の間に行わなければならない。 実際、本サービスでは情報の鮮度の観点から全ての記事が24時間以内に失効するため、毎日数万件の新しい記事が投稿され、同数の古い記事が失効により削除されている。 そこで、各プロセスでは、あらかじめ計算された分散記事表現（第3章で説明）とユーザ表現（第4章で説明）を活用した計算量の少ない方法を採用している。

We use the inner product of distributed representations of a user and candidate articles in matching to quantify relevance and select promising candidates. We determine the order of priorities in ranking by considering additional factors, such as the expected number of page views and freshness of each article, in addition to the relevance used for matching. We skip similar articles in a greedy manner in de-duplication based on the cosine similarity of distributed representations. An article is skipped when the maximum value of its cosine similarity with articles with higher priorities is above a threshold. This is an important process in real news distribution services because similar articles tend to have similar scores in ranking. If similar articles are displayed close to one another, a real concern is that user satisfaction will decrease due to reduced diversity on the display. Details on comparison experiments in this process have been discussed in a report on our previous study [12]. Advertising is also important, but several studies [2, 10] have already reported on the relationship between advertising and user satisfaction, so such discussion has been omitted here.
マッチングに用いるユーザと候補記事の分散表現の内積を用いて、関連性を定量化し、有望な候補を選択する。 マッチングに用いる関連性に加えて、各記事の予想ページビュー数や鮮度などの要素を加味して、ランキングの優先順位を決定している。 重複排除では、分散表現のコサイン類似度に基づいて、類似記事を貪欲にスキップする。 より優先度の高い記事とのコサイン類似度の最大値が閾値を超えると、その記事はスキップされる。 これは実際のニュース配信サービスにおいて重要な処理である。なぜなら、類似した記事はランキングにおいて類似したスコアを持つ傾向があるからである。 類似記事同士が近くに表示されると、表示の多様性が損なわれるため、ユーザーの満足度が低下することが懸念される。 この過程での比較実験の詳細については、我々の先行研究報告[12]で述べている。 広告も重要であるが、広告とユーザ満足度の関係については、すでにいくつかの研究[2, 10]で報告されているので、ここではその議論は省略した。

## 3. ARTICLE REPRESENTATIONS 3. 記事表示

Section 1 discussed a method of using words as features for an article that did not work well in certain cases of extracting and de-duplicating. This section describes a method of dealing with articles as a distributed representation. We proposed a method in our previous study [12], from which part of this section has been excerpted.
セクション1では、記事の特徴として単語を用いる方法について述べたが、これは抽出や重複排除の特定のケースでうまく機能しなかった。 本節では、記事を分散表現として扱う方法について述べる。 我々は以前の研究[12]でこの方法を提案したが、本節はその一部を抜粋したものである。

### 3.1. Generating Method 3.1. 生成方法

Our method generates distributed representation vectors on the basis of a denoising autoencoder [19] with weak supervision. The conventional denoising autoencoder is formulated as:
本手法は，弱い監視を伴うノイズ除去オートエンコーダ[19]に基づいて，分散表現ベクトルを生成する． 従来のノイズ除去オートエンコーダは以下のように定式化される。

$$
\tilde{x} \sim q(\tilde{x}|x) \\
h = f(W\tilde{x} + b) \\
y =f(W'h + b') \\
\theta = \argmin_{W, W', b, b'} \sum_{x \in X} L_R(y, x)
$$

where $x \in X$ is the original input vector and $q(·|·)$ is the corrupting distribution. The stochastically corrupted vector, $\tilde{x}$, is obtained from $q(·|x)$. The hidden representation, h, is mapped from $\tilde{x}$ through the network, which consists of an activation function, $f(·)$, parameter matrix W , and parameter vector b. In the same way, the reconstructed vector, y, is also mapped from h with parameters $W'$ and $b'$ . Using a loss function, $L_{R}(·, ·)$, we learn these parameters to minimize the reconstruction errors of y and x.
·)$ is the corrupting distribution. The stochastically corrupted vector, $\tilde{x}$, is obtained from $q(·

The h is usually used as a representation vector that corresponds to x. However, h only holds the information of x. We want to interpret that the inner product of two representation vectors $h_0^T h_1$ is larger if $x_0$ is more similar to $x_1$. To achieve that end, we use a triplet, $(x_0, x_1, x_2) \in X^3$ , as input for training and modify the objective function to preserve their categorical similarity as:
hは通常xに対応する表現ベクトルとして用いられるが、hはxの情報しか持たない。2つの表現ベクトルの内積$h_0^T h_1$は$x_0$が$x_1$とより似ていればより大きくなると解釈されたい。 そのために、三重項、$(x_0, x_1, x_2) \in X^3$ を学習の入力とし、それらのカテゴリ的類似性を保持するように目的関数を次のように修正する。

$$
\tilde{x}_n \sim q(\tilde{x}_n|x_n) \\
h_n = f(W\tilde{x}_n + b) - f(b) \\
y_n = f(W'h_n + b')
L_T(h_0, h_1, h_2) = \log (1+ \exp(h_0^T h_2 - h_0^T h_1)) \\
\theta = \argmin_{W,W',b, b'} \sum_{x_0,x_1,x_2 \in T}
\sum_{n=0}^2 L_R(y_n,x_n) + \alpha L_T(h_0, h_1, h_2) \\
\tag{1}
$$

where $T \subset X^3$ , such that $x_0$ and $x_1$ are in the same category/similar categories and $x_0$ and $x_2$ are in different categories. The h in Eq.1 satisfies the property, $x = 0 ⇒ h = 0$. This means that an article that has no available information is not similar to any other article. The notation, $L_T (·, ·, ·)$ is a penalty function for article similarity to correspond to categorical similarity, and α is a hyperparameter for balancing. Figure 2 provides an overview of this method.
ここで、$T \subset X^3$ , $x_0$と$x_1$が同じカテゴリにあるようなものである。

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/3-Figure2-1.png">

We use the elementwise sigmoid function, $\sigma(x)_i = 1/(1+exp(-x_i))$, as $f(·)$, elementwise cross entropy as $L_R(·, ·)$, and masking noise as $q(·|·)$. We train the model, $\theta = {W ,W′, b, b′}$, by using mini-batch stochastic gradient descent (SGD).
要素別シグモイド関数$Σsigma(x)\_i = 1を使用する。

We construct x˜ in the application phase by using constant decay, instead of stochastic corruption in the training phase, as:
応用段階では、学習段階での確率的な破損の代わりに、一定の減衰を用いて、x〜を次のように構成する。

$$
\tilde{x} = (1-p)x \\
h = f(W\tilde{x} + b) - f(b)
$$

where $p$ is the corruption rate in the training phase. Thus, $h$ is uniquely determined at the time of application. Multiplying $1 − p$ has the effect of equalizing the input distribution to each neuron in the middle layer between learning with masking noise and that without the application of this noise.
ここで、$p$は学習段階での破損率である。 したがって、$h$は適用時に一意に決定される。 1 - p$を掛けると、マスキングノイズを適用した学習と適用しない学習とで、中間層の各ニューロンへの入力分布が等しくなる効果がある。

We use the $h$ generated above in three applications as the representation of the article: (i) to input the user-state function described in Section 4, (ii) to measure the relevance of the user and the article in matching, and (iii) to measure the similarity between articles in de-duplication.
上記で生成された$h$を記事の表現として3つの用途で用いる。 (i) セクション4で述べるユーザ状態関数の入力、(ii) マッチングにおけるユーザと記事の関連性測定、(iii) 重複排除における記事間の類似度測定である。

## 4. USER REPRESENTATIONS 4. ユーザー表現

This section describes several variations of the method to calculate user preferences from the browsing history of the user. First, we formulate our problem and a simple word-based baseline method and discuss the issues that they have. We then describe some methods of using distributed representations of articles, as was explained in the previous section.
ここでは、ユーザの閲覧履歴からユーザの嗜好を算出する方法について、いくつかのバリエーションを説明する。 まず、我々の問題と単純な単語ベースのベースライン法を定式化し、それらが持つ問題点を議論する。 次に、前節で説明したように、記事の分散表現を利用するいくつかの方法について説明する。

### 4.1. Notation 4.1. 表記方法

Let $A$ be the entire set of articles. Representation of element $a \in A$ depends on the method. The $a$ is a sparse vector in the word-based method described in Section 4.2, and each element of a vector corresponds to each word in the vocabulary (i.e., $x$ in Section 3). However, $a$ is a distributed representation vector of the article (i.e., $h$ in Section 3) in the method using distributed representations described in Sections 4.3 and 4.4.
冠詞の全集合を$A$とする。 A$の要素$a \の表現は手法に依存する。 a$ は4.2節で述べた単語ベースの手法ではスパースベクトルであり、ベクトルの各要素は語彙の各単語に対応する（すなわち、3節では$x$）。 しかし、セクション4.3および4.4で述べた分散表現を用いる方法では、$a$は記事の分散表現ベクトル（すなわち、セクション3では$h$）である。

Browse means that the user visits the uniform resource locator (URL) of the page of an article. Let ${_t^u \in A}_{t=1,\cdots,T_u}$ be the browsing history of user $u \in U$.
閲覧とは、ユーザが記事のページのURL(Uniform Resource Locator)を訪問することである。 ここで、${_t^u \in A}_{t=1,\cdots,T_u}$ をユーザ $u \in U$ のブラウズ履歴とする。

Session means that the user visits our recommendation service and clicks one of the articles in the recommended list.
セッションとは、ユーザーが当社のレコメンデーションサービスにアクセスし、おすすめリストの記事をクリックすることを指します。

When $u$ clicks an article in our recommendation service (a session occurs), he/she will immediately visit the URL of the clicked article (a browse occurs). Thus, there is never more than one session between browses $a_t^u$ and $a^u_{t+1}$ ; therefore, this session is referred to as $s_t^u$ . However, $u$ can visit the URL of an article without our service, e.g., by using a Web search. Therefore, $s_t^u$ does not always exist.
u$がレコメンドサービスの記事をクリックしたとき（セッションが発生したとき）に

Since a session corresponds to the list presented to $u$, we express a session, $s^u_t$, by a list of articles ${s^u_{t,p} \in A}_{p \in P}$. The notation, $P \subseteq N$, is the set of positions of the recommended list that is actually displayed on the screen in this session. Let $P_{+} \subseteq P$ be the clicked positions and $P_{-} = P \ P_{+}$ be non-clicked positions. Although $P$, $P_{+}$, and $P_{-}$ depend on $u$ and $t$, we omit these subscripts to simplify the notation. Figure 3 outlines the relationships between these notations.
セッションは$u$に提示されたリストに対応するので、セッション$s^u_t$を記事のリスト${s^u_{t,p}で表現する。 \のリストで表現する。 このとき、$P \subseteq N$という表記は、このセッションで実際に画面に表示される推奨リストの位置の集合である。 P_{+} \subseteq P$をクリックされた位置、$P_{-} = P \ P_{+}$を非クリックの位置とする。 P$、$P*{+}$、$P*{-}$は$u$、$t$に依存するが、表記を簡略化するためにこれらの添え字を省略する。 図3にこれらの表記の関係の概略を示す。

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/4-Figure3-1.png">

Figure 3: Browsing history and session
図3：閲覧履歴とセッション

Let $u_t$ be the user state depending on $a_1^u , \cdots, a_t^u$, i.e., $u_t$ represents the preference of $u$ immediately after browsing $a_t^u$. Let $R(u_t, a)$ be the relevance between the user state, $u_t$, and the article, $a$, which represents the strength of $u$’s interest in a in time t. Our main objective is to constitute user-state function $F(·, . . . , ·)$ and relevance function $R(·, ·)$ that satisfy the property:
u_t$を$a_1^u , \cdots, a_t^u$に依存するユーザ状態、すなわち$u_t$は$a_t^u$を閲覧した直後の$u$の嗜好を表すとする。 R(u_t, a)$はユーザ状態$u_t$と記事$a$の間の関連性で、時間tにおける$u$のaへの興味の強さを表す。我々の主な目的は、この性質を満たすユーザ状態関数$F(-, ... , -)$と関連性関数$R(-, -)$を構成することである。

$$
u_t = F(a_1^u, \cdots, a_t^u) \\
\forall{s_t^u} \forall{p_{+}} \in P_{+} \forall{p_{-}}
\in P_{-} R(u_t, s_{t,p_{+}}^u) > R(u_t, s_{t, p_{-}}^u). \\
\tag{2}
$$

($\forall$は"任意の、全称記号"を表す論理記号。全称量化子とも呼ばれる。)
($\forall$ is a logic symbol for "any, all symbol". Also called the full-symmetry quantifier)

When considering the constrained response time of a real news distribution system with large traffic volumes, $R(·, ·)$ must be a simple function that can be quickly calculated. Because candidate articles are frequently replaced, it is impossible to pre-calculate the relevance score, $R(u_t, a)$, for all users ${u_t |u \in U }$ and all articles ${a \in A}$. Thus, it is necessary to calculate this in a very short time until the recommended list from visiting our service page is displayed. However, we have sufficient time to calculate the user state function, $F (·, \cdots, ·)$, until the next session occurs from browsing some article pages.
u \in U }$ and all articles ${a \in A}$. Thus, it is necessary to calculate this in a very short time until the recommended list from visiting our service page is displayed. However, we have sufficient time to calculate the user state function, $F (·, \cdots, ·)$, until the next session occurs from browsing some article pages.

We restrict relevance function $R(·, ·)$ to a simple inner-product relation, $R(u_t , a) = u_t^T a$, for these reasons and only optimize the user state function, $F (·, \cdots, ·)$, to minimize the objective:
これらの理由から関連性関数$R(-, -)$を単純な内積関係$R(u_t , a) = u_t^T a$に限定し、ユーザ状態関数$F (-, \cdots, -)$のみを最適化して目的を最小化することにした。

$$
\sum_{s_t^u} \sum_{p_{+} \in P_{+}, p_{-} \in P_{-}}
- \frac{
\log (\sigma(R(u_t, s_{t, p_{+}}^u) - R(u_t, s_{t,p_{-}}^u)))
}{
|P_{+}||P_{-}|
}
\tag{3}
$$

where $\sigma(·)$ is the logistic sigmoid function. Equation 4.1 is a relaxation of Eq. 2. As there is a bias, in practice, in the probability of clicks depending on the displayed position when articles are vertically arranged, we use the following objective including the bias term, $B(·,·)$, to correct such effects. Although $B(·,·)$ is a parameter to be determined by learning, its description has been omitted below since it is a common term in the models that follow
ここで、$sigma(-)$はロジスティックシグモイド関数である。 4.1式は2式を緩和したものである。 実際には、記事が縦に並んでいる場合、表示位置によってクリックされる確率に偏りがあるため、その影響を補正するために、バイアス項$B(-,-)$を含む次の目的語を用いる。 B(-,-)$は学習によって決定されるパラメータであるが、以降のモデルで共通する用語であるため、以下ではその説明を省略する。

$$
\sum_{s_t^u} \sum_{p_{+} \in P_{+}, p_{-} \in P_{-}}
- \frac{
\log (\sigma(R(u_t, s_{t, p_{+}}^u) - R(u_t, s_{t,p_{-}}^u)) + B(p_{+}, p_{-}))
}{
|P_{+}||P_{-}|
}
$$

### 4.2. Word-based Model 4.2. 単語ベースモデル

We formulate the word-based baseline model introduced in Section 1 as a baseline implementation on the basis of the notations in the previous section.
前節の表記をもとに、第1節で紹介した単語ベースのベースラインモデルをベースライン実装として定式化する。

Recall the three steps in the baseline implementation.
ベースラインの実装における3つのステップを思い出してください。

- An article is represented by a collection of words included in its text,
- 記事は、そのテキストに含まれる単語の集まりで表現される。

- A user is represented by a collection of words included in articles he/she has browsed, and
- ユーザは、自分が書いた記事に含まれる単語の集まりで表現される。

- The relevance between the user and article is expressed by a linear function on the co-occurrences of words between them.
- ユーザーと記事の関連性は、両者間の単語の共起度に関する線形関数で表現される。

This model can be regarded as a special case of the notation in
の表記の特殊なケースとみなすことができる。

the previous section, if article representation $a$ and user function $F$ are defined as:
前節で、記事表現$a$とユーザー関数$F$を次のように定義した。

$$
V : \text{Vocabulary set} \\
a, u_t \in {0, 1}^V \\
(a)_{v} = \left\{
\begin{array}{cc}
1 (\text{if the article contains the word v}) \\
0 (\text{otherwise}) \\
\end{array}
\right. \\
(u_t)_v = (F(a_1^u, \cdots, a_t^u))_v = \alpha_v \max_{1 \leq t' \leq t} (a_{t'}^u)_{v'}
\tag{4}
$$

where $(x)_v$ is the $v$-th element of $x$. Then, the relevance function becomes a simple linear model with parameters ${\alpha_v}$ as:
ここで、$(x)_v$は$x$の$v$番目の要素である。 すると、関連性関数は、パラメータ${alpha_v}$を次のように持つ単純な線形モデルとなる。

$$
R(u_t, a) = u_t^T a \\
= \sum_{v \in V} (u_t)_v (a)_v \\
= \sum_{v \in V} \alpha_v 1_{v \in u_{t} \cap a}
$$

There are two major issues with this model, as was explained in Section 1.
このモデルには、第1章で説明したように、2つの大きな問題点がある。

The first is the sparseness of the representation. The $R(u_t, a)$ in this model increases if only if $u_t$ and $a$ contain the same words. Thus, even if a user is interested in similar articles, the relevance scores may greatly differ depending on whether they have been written using the same words as the articles in his/her browsing histories.
第一は表現の疎密である。 このモデルにおける$R(u_t, a)$は$u_t$と$a$が同じ単語を含んでいる場合にのみ増加する。 このように、ユーザが同じような記事に興味を持っていても、それが自分の記事と同じ単語を使って書かれたものかどうかによって、関連性のスコアが大きく異なることがある。

The second issue is intensity. Because the browsing history is regarded as a set, the information about the browsing order and frequency are lost. Thus, the model is very vulnerable to noise that is mixed into the browsing history.
第二の問題は強度である。 閲覧履歴を集合とみなすため、閲覧の順序や頻度に関する情報が失われる。 そのため、閲覧履歴に混入するノイズに対して非常に脆弱なモデルとなっている。

We describe other models by using distributed representations by taking into account these issues in the subsections below.
これらの問題を考慮した上で、分散表現を用いた他のモデルについて、以下の小項目で説明する。

### 4.3. Decaying Model 4.3. 減衰モデル

We introduce a simple model with distributed representations to solve these issues. Two changes in this model from that of the baseline are:
これらの問題を解決するために、分散表現を用いた簡単なモデルを導入する。 このモデルのベースラインからの変更点は2点である。

- It uses the distributed representation constructed in Section 3 as the representation vector, a, of an article, instead of a bag-of-words (BoW) representation (which addresses the first issue).
- 記事の表現ベクトルaとして、Bag-of-Words（BoW）表現ではなく、第3節で構築した分散表現を用いる（第1の問題点を解決）。

- It uses the weighted average to aggregate browsing histories, instead of the maximum value. More specifically, we increase the weights for recent browses and reduce the weights for the previous days’ browses (which addresses the second issue).
- 閲覧履歴の集計に、最大値ではなく、加重平均を使用している。 具体的には、最近の閲覧の重みを増やし、前日の閲覧の重みを減らす（2番目の問題に対応する）。

$$
u_t = \alpha \odot
\frac{1}{\sum_{1\leq t' \leq t} \beta^{t-t'}}
\sum_{1 \leq t' \leq t} \beta^{t-t'} a_{t'}^u
$$

($\odot$はドット積を表すもの。ベクトルの演算方法の一つ。二つのベクトルが与えられたとき、対応する要素同士の掛け算をした結果を要素とする新しいベクトルを求める。)
($\odot$ is the dot product. One of the methods of vector arithmetic. Given two vectors, find a new vector whose elements are the result of multiplication between corresponding elements).

where $\alpha$ is a parameter vector that has the same dimension as $a_t^u$, ⊙ is the elementwise multiplication of two vectors, and 0 < β ≤ 1 is a scalar value that is a hyperparameter that represents the strength of time decay. If β is 1, aggregation is the simple average, so that the browsing order is not taken into consideration. Training parameters are only α in this model, which are similar to those in the baseline model.
ここで、$alpha$は$a_t^u$と同じ次元のパラメータベクトル、⊙は二つのベクトルの要素別乗算、0 < β ≤ 1はスカラー値で、時間の減衰の強さを表すハイパーパラメータである。 βが1の場合、集計は単純平均となり、閲覧順は考慮されない。 学習パラメータは本モデルではαのみであり、ベースラインモデルと同様である。

### 4.4. Recurrent Models 4.4. リカレントモデル

![](https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/6-Figure4-1.png)

#### 4.4.1. Simple Rqcurrent Unit 4.4.1. 簡易Rq電流ユニット

Although the decaying model in the previous subsection took into account issues with the wordbased model, it had limitations such as being linear with respect to frequency and that the forgetting effect was limited to exponential decay with hyperparameters.
前節の減衰型モデルは単語ベースのモデルの問題点を考慮したものであるが、周波数に対して線形であること、忘却効果がハイパーパラメータによる指数関数的減衰に限定されていることなどの制約があった。

More generally, $u_t$ should be determined by a previous state, $u_{t−1}$, and previous browse $a_t^u$ as:
より一般的には、$u_t$は以前の状態、$u_{t-1}$と以前のブラウズ$a_t^u$によって次のように決定されるはずである。

$$
u_t = f(a_t^u, u_{t-1})
$$

Therefore, we try to learn this function by using an RNN. A simple RNN is formulated by:
そこで、RNNを用いて、この関数を学習することを試みる。 単純なRNNは、以下のように定式化される。

$$
u_t = \phi(W^{in} a_t^u + W^{out} u_{t-1} + b)
$$

where φ(·) is the activation function; therefore, we subsequently use hyperbolic tangent function tanh(·). Training parameters are square matrices $W^{in}$ ,$W^{out}$ , bias vector $b$, and initial state vector $u_0$ in this model, where $u_0$ is a common initial value that does not depend on $u$.
ここでφ(-)は活性化関数であるため、以後は双曲線正接関数tanh(-)を用いる。 学習パラメータは、このモデルでは正方行列$W^{in}$ ,$W^{out}$ , バイアスベクトル$b$, 初期状態ベクトル$u_0$であり、$u_0$は$u$に依存しない共通の初期値である.初期状態ベクトル$u_0$は、$u$に依存しない。

We learn these parameters by end-to-end mini-batch SGD with the objective function in Eq. 4.1. However, when the input sequence is too long, simple RNN makes it too difficult to learn this due to gradient vanishing and explosion problems [5]. Additional structures that are attached to the hidden layer are able to alleviate these problems in such cases.
これらのパラメータを、式4.1の目的関数を用いたend-to-endのミニバッチSGDによって学習する。 しかし、入力シーケンスが長すぎる場合、単純なRNNでは勾配の消失や爆発問題により、これを学習することが困難となる[5]。 このような場合、隠れ層に付加される追加構造によって、これらの問題を緩和することができる。

The following subsections introduce two models that use such structures.
以下では、このような構造を利用した2つのモデルを紹介する。

#### 4.4.2. Long-short Term Memory Unit 4.4.2. ロング・ショート・ターム・メモリー・ユニット

Long-short term memory (LSTM) [6] is a well-known structure for vanishing and exploding gradients [5]. We formulate an LSTM-based model as:
Long-short term memory (LSTM) [6] は消失勾配と爆発勾配に対するよく知られた構造である [5]． 我々はLSTMに基づくモデルを次のように定式化する。

$$
gi_t = \sigma(W_{gi}^{in}a_t^u + W_{gi}^{out} u_{t-1} + W_{gi}^{mem}h_{t-1}^u + b_{gi})
\\
gf_t = \sigma(W_{gf}^{in}a_t^u + W_{gf}^{out} u_{t-1} + W_{gf}^{mem}h_{t-1}^u + b_{gf})
\\
enc_t = \phi(W_{enc}^{in}a_t^u + W_{enc}^{out} u_{t-1} + b_{gf})
\tag{5}
$$

$$
h_t^u = gi_t \odot enc_t + gf_t \odot h_{t-1}^u
\tag{6}
$$

$$
go_t = \sigma(W_{go}^{in}a_t^u + W_{go}^{out} u_{t-1} + W_{go}^{mem}h_{t}^u + b_{go})
\\
dec_t = \phi(W_{dec}^{mem}h_t^u +  b_{dec}) \tag{7}
$$

$$
u_t = go_t \odot dec_t \tag{8}
$$

where σ (·) is the elementwise logistic sigmoid function, and $h^u_t$ is a hidden memory state. Figure 4 has a network image of the structure of the LSTM-based model.
ここで、σ (-) は要素ごとのロジスティックシグモイド関数、$h^u_t$ は隠れ記憶状態である。 図4は、LSTMを用いたモデルの構造を示すネットワークイメージである。

The center flows are the main flows from input (browsed article) to output (user state). The input, $a^u_t$, is encoded from article vector space to hidden space (Eq. 5), merged into the previous hidden state (Eq. 6), and decoded to the article vector space (Eq. 7, Eq. 8) as the user state.
中央のフローは入力（閲覧した記事）から出力（ユーザ状態）への主なフローである。 入力である$a^u_t$は、記事ベクトル空間から隠れ空間へ符号化され（式5）、前の隠れ状態にマージされ（式6）、ユーザー状態として記事ベクトル空間へ復号される（式7、式8）。

In addition, this unit has three gates, called input gate ($gi_t$ ), forget gate ($gf_t$), and output gate ($go_t$). We assumed each gate would conceptually play the following roles in this case. The input gate filters unnecessary inputs to construct a user state, such as that caused by sudden interest. The forget gate represents the decline in interest by the user. It can represent a more complex forgetting effect than the exponential decay that is used in the decaying model. The output gate filters components that should not be focused on in the next session.
また、このユニットには、入力ゲート（$gi_t$）、忘却ゲート（$gf_t$）、出力ゲート（$go_t$）と呼ばれる3つのゲートが存在します。 このとき、各ゲートは概念的に以下のような役割を果たすと仮定した。 入力ゲートは、不要な入力をフィルタリングして、急激な興味によるものなど、ユーザーの状態を構築する。 忘却ゲートは、ユーザーによる興味の減退を表す。 逓減モデルで用いられる指数関数的な減衰よりも複雑な忘却効果を表現することができる。 出力ゲートは、次回のセッションで注目されるべきではない成分をフィルタリングする。

Training parameters are weight matrices $W$, bias vectors $b$ and initial state vectors $u_0$ and $h^u_0$ in this model, where $u_0$ and $h^u_0$ are common initial values that do not depend on u.
学習パラメータは、このモデルにおける重み行列$W$、バイアスベクトル$b$、初期状態ベクトル$u_0$と$h^u_0$であり、$u_0$と$h^u_0$はuに依存しない共通の初期値である。

#### 4.4.3. Gated Recurrent Unit 4.4.3. ゲート式リカレントユニット

![](https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/6-Figure5-1.png)

Gated recurrent unit (GRU) [1] is another structure to avoid gradient vanishing and explosion problems [5]. We formulate a GRU-based model as:
Gated recurrent unit (GRU) [1] は勾配の消失と爆発問題 [5] を回避するためのもう一つの構造である． 我々はGRUに基づくモデルを次のように定式化する。

We describe these formulations using symbols that correspond to those of the LSTM-based model as much as possible. More precisely, this model is constructed using one GRU layer and one fully connected layer because Eq. 10 is not contained in the original GRU configuration. Figure 5 outlines a network image of the GRUbased model structure.
これらの定式化を、LSTMを用いたモデルとなるべく対応する記号を用いて説明する。 より正確には、式 10 が本来の GRU の構成に含まれないため、1 つの GRU 層と 1 つの完全連結層を用いてこのモデルを構成している。 図5にGRUベースのモデル構造のネットワークイメージを示す。

Except for the omission of some arrows, this structure is similar to that of the LSTM-based model. However, there is an important difference between Eqs. 6 and 9. The $gz_t$ gate in this model plays the role of two gates, i.e., $gi_t$ and $gf_t$ in the LSTM-based model. As a result, the following difference in the upper limit of norm $||h_t^u||_{\infty}$ occurs.
|h_t^u

$$
\sup_{u} ||h_t^u||_{\infty} = \left \{
\begin{array}{cc}
||h_0^u||_{\infty} + t \sup_{x}|\phi(x)| \text{in LSTM} \\
\max (||h_0^u||_{\infty}, \sup_{x}|\phi(x)|) \text{in GRU}
\end{array}
\right.
\tag{11,12}
$$

Equation 11 can be a large value for a very long input sequence; however, Eq. 12 never exceeds the constant. Therefore, we think the GRU-based model has a higher aptitude to solve the gradient explosion problem than the LSTM-based model.
式11は非常に長い入力列に対して大きな値となりうるが、式12は定数を超えることはない。 したがって、GRUベースモデルはLSTMベースモデルよりも勾配爆発問題の解法に適性があると考えられる。

The LSTM-based model occasionally failed in training due to gradient explosion when we did not use gradient clipping [13] in the experiments that are described in the next section. However, the GRU-based model did not cause gradient explosion without any supplementary processing.
LSTMベースのモデルは、次節で述べる実験において勾配クリッピング[13]を用いない場合、勾配爆発により学習に失敗することがありました。 しかし、GRUベースのモデルでは、何も補助的な処理を行わなくても勾配爆発は起こりませんでした。

## 5. Offline Experiments 5. オフライン実験

This section discusses the effectiveness of the distributed representationbased method with the models in the previous section by offline evaluation using past serving logs. We compared the three wordbased models that were variants of the model introduced in Section 4.2 and five distributed representation-based models introduced in Sections 4.3 and 4.4. These models are summarized in Table 1.
本節では、過去の配信ログを用いたオフライン評価により、前節のモデルによる分散表現ベース手法の有効性を議論する。 4.2節で紹介したモデルの変形である3つの単語ベースモデルと、4.3節と4.4節で紹介した5つの分散表現ベースモデルを比較検討した。 これらのモデルを表 1 にまとめる。

![](https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/500px/7-Table1-1.png)

### 5.1. Training Dataset 5.1. トレーニングデータセット

First, we sampled approximately 12 million users who had clicked at least one article from the service logs of Yahoo! JAPAN’s homepage on smartphones between January and September 2016. We extracted logs for each user over a two-week period chosen at random to include at least one click. This method of extraction was used to mitigate the impact of epidemic articles within a specific period.
まず、2016年1月～9月の間にスマートフォンでYahoo！JAPANのホームページのサービスログから1記事以上クリックしたことがあるユーザー約1200万人をサンプリングしました。 各ユーザーのログは、1回以上のクリックが含まれるようにランダムに選んだ2週間分のログを抽出しました。 この抽出方法によって、特定期間内の流行記事の影響を緩和した。

As a result, there were about 166 million sessions, one billion browses, and two million unique articles in the training data. We also created another dataset for the same period and used it as a validation dataset to optimize the hyperparameters.
その結果、学習データには約1億6600万セッション、10億ブラウズ、200万ユニーク記事が含まれることになった。 また、同期間の別のデータセットを作成し、検証用データセットとして使用し、ハイパーパラメータの最適化を行いました。

### 5.2. Test Dataset 5.2. テストデータセット

We sampled 500,000 sessions, in which users clicked articles above position 20 on October 2016. We extracted browse logs in the previous two weeks for each session. We used the article data from positions 1 to 20 for evaluation regardless of whether they were actually displayed on the screen. This was based on our observation with timeline-based user-interfaces. Users scrolled from top to bottom and tended to leave our service when they clicked one article. That is, if we only used data actually displayed for evaluation, the method of arranging the actual displayed order in reverse was evaluated as being disproportionately better.
2016年10月にユーザーが20位以上の記事をクリックした、50万セッションをサンプリングしました。 各セッションについて、過去2週間の閲覧ログを抽出した。 1位から20位までの記事データは、実際に画面に表示されているかどうかに関わらず、評価に使用しました。 これは、タイムラインベースのユーザーインターフェイスでの観察に基づくものである。 ユーザーは上から下へスクロールし、一つの記事をクリックした時点でサービスから離脱する傾向があった。 つまり、実際に表示されているデータのみを評価対象とした場合、実際に表示されている順番を逆に並べた方法の方が不釣り合いに優れていると評価されたのです。

### 5.3. Offline Metrics 5.3. オフラインメトリクス

We evaluated the rankings provided by each model by using three popular metrics, i.e., the area under the ROC curve (AUC), mean reciprocal rank (MRR), and normalized discounted cumulative gain (nDCG), which regarded clicks as positive labels.
各モデルが提供するランキングは，クリックを正ラベルと見なし，ROC曲線下面積（AUC），平均逆数ランク（MRR），正規化割引累積利得（nDCG）という一般的な3つの指標を用いて評価した．

Let $S$ be the set of sessions for the evaluation, $c_{s,i}$ be one when the article at position $i$ is clicked, and zero otherwise. Each metric is formulated as:
評価の対象となるセッションの集合を$S$とし、$c_{s,i}$は位置$i$の記事がクリックされたとき1、それ以外は0とする。 各指標は以下のように定式化される。

$$
\text{AUC} = hogehoge \\
\text{MRR} = \frac{1}{|S|} \sum_{s=1}^{|S|} \frac{1}{\min_{c_{s,i}=1} i} \\
\text{nDCG} = \frac{\text{DCG}}{\text{IDCG}} \\
\text{DCG} = \sum_{i=1}^n \frac{2^{rel_i}-1}{\log_2(i+1)} \\
\text{iDCG} = \sum_{i=1}^n \frac{2^{rel_i}-1}{\log_2(i+1)}
$$

where π is an arbitrary permutation of positions.
ここで、πは位置の任意の並べ換えである。

The AUC is the metric directly related to the objective of training (see Eq.2). The MRR and nDCG are popular ranking metrics; the former focuses on the first occurrence of positive instances, and the latter evaluates ranks for all the positive instances. Each metric is a value between zero and one, which is calculated as the average score for each session; i.e., the larger the better.
AUCは学習の目的に直接関係する指標である（式2参照）。 MRR と nDCG は一般的なランキング指標であり、前者はポジティブなインスタンスの最初の出現に注目し、後者はすべてのポジティブなインスタンスについてランクを評価するものである。 各メトリクスは0から1の間の値で、各セッションの平均スコアとして計算される；つまり、大きければ大きいほど良いということである。

### 5.4. Models and Training 5.4. モデルおよびトレーニング

We evaluated the eight models listed in Table 1.
表1に示す8つのモデルを評価した。

As was described in Section 4.2, word-based models can be regarded as simple linear logistic regressions for pairwise data with sparse feature vectors, like the ranking support vector machine (SVM) [7]. Thus, we used LIBLINEAR [4] for training L2-regularized logistic regression (solver type 0).
4.2節で述べたように、単語ベースモデルは、ランキングサポートベクトルマシン（SVM）[7]のように、特徴ベクトルが疎なペアワイズデータに対する単純な線形ロジスティック回帰とみなすことができる。 そこで、L2正則化ロジスティック回帰の学習にはLIBLINEAR [4]を用いた（ソルバーtype 0）。

We used mini-batch SGD with RMS-prop to adjust the learning rate for the other models. The mini-batch size was 20 and the initial learning rate was 0.005. The numbers of dimensions of the distributed representations of article a and user state ut were 500. The number of dimensions of internal state $h^u_t$ was 200 in LSTM and GRU. These parameters were determined by using the development dataset.
他のモデルの学習率を調整するために、RMS-propを用いたミニバッチSGDを使用した。 ミニバッチサイズは20で、初期学習率は0.005である。 記事aの分散表現とユーザ状態utの次元数は500であった。 内部状態$h^u_t$の次元数はLSTMとGRUで200であった。 これらのパラメータは開発データセットを用いて決定した。

We used the gradient clipping technique [13] to avoid gradient explosion in RNN and LSTM. GRU did not cause gradient explosion when this technique was not used in these experiments.
RNNとLSTMの勾配爆発を避けるために、勾配クリッピング技術[13]を使用しました。 この実験でこの手法を用いなかった場合、GRUは勾配爆発を起こさない。

### 5.5. Experimental results 5.5. 実験結果

![](https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/500px/7-Table2-1.png)

Table 2 lists all metrics used in the experiments. We split the test dataset into ten sub-datasets and calculated each metric per subdataset. The values in Table 2 are the averages for each metric of the sub-datasets and each metric’s 99% confidence intervals that were estimated based on the t-distribution.
表 2 は実験で使用したすべてのメトリクスの一覧である。 テストデータセットを10のサブデータセットに分割し、サブデータセットごとに各メトリクスを計算した。 表2の値は、サブデータセットの各メトリクスの平均値と、t分布に基づいて推定された各メトリクスの99%信頼区間である。

GRU had the best score for all metrics with a sufficient margin, and it yielded a significant difference against all other models according to a paired t-test with p < 0.01.
GRUは、すべての指標において十分なマージンをもって最高のスコアを獲得し、p<0.01のペアt検定により、他のすべてのモデルに対して有意な差をもたらしました。

Because Average exhibited a significant improvement from BoWAve, distributed representations of articles should work better than BoW representations.
平均はBoWAveから大きな改善を示したので、記事の分散表現はBoW表現よりもうまくいくはずである。

Decay and BoW-Dec were worse than Average and BoW-Ave. This suggests that browsing-order information cannot be expressed with simple attenuation. RNN also exhibited a slight improvement on AUC against Average. However, LSTM and GRU were significantly better than Average. We believe this was because it was able to express more complex relations for the order of browsing sequences by using the gate structures in these models.
DecayとBoW-Decは、AverageとBoW-Aveよりも悪い結果となった。 これは、閲覧順の情報は単純な減衰では表現できないことを示唆している。 RNNもAverageに対してAUCが若干改善された。 しかし、LSTMとGRUはAverageに対して大幅に改善されました。 これは、これらのモデルのゲート構造を利用することで、より複雑な閲覧順序の関係を表現することができたためと考えられる。

## 6. Deployment 6. デプロイメント

We began using GRU on December 2016 for the main traffic in our service (which we denoted the Proposed bucket). However, we continued to apply the conventional BoW model to 1 % of users to enable comparisons of performance (which we denoted the Control bucket). This section reports the results obtained from comparisons after deployment.
2016年12月より、本サービスの主要トラフィック（これをProposedバケットと表記）に対してGRUの利用を開始しました。 しかし、性能比較を可能にするため、1 %のユーザーには従来のBoWモデルを適用し続けました（これをControlバケットと表記）。 本節では、導入後の比較の結果を報告する。

### 6.1. Settings 6.1. 設定項目

Our system presents articles to users who visit our service page according to a three step procedure.
本システムでは、サービスページにアクセスしたユーザーに対して、3つのステップで記事を紹介します。

- The user state, $u_t$, of each model should be calculated from the browsing history in advance.
- 各モデルのユーザ状態$u_t$は、あらかじめ閲覧履歴から算出しておく必要がある。

- When user $u$ visits our service, we calculate the relevance scores, $R(u_t , a) = u_t^Ta$, for all articles a that were newly published within a certain period of time.
- ユーザ $u$ が我々のサービスにアクセスしたとき、ある期間内に新しく公開されたすべての記事 a に対して、関連性スコア $R(u_t , a) = u_t^Ta$ を計算する。

- We present the articles to the user in order from the highest relevance score by applying de-duplication.
- 重複排除を行い、関連度スコアの高いものから順番にユーザーに提示する。

The representation of $u_t$ and a for relevance scores depends on the bucket. We applied de-duplication by using the distributed representations described in Section 2 to both Control and Proposed buckets. As the effects of de-duplication on users are not discussed here, refer to our past paper [12] for details on an experiment on these effects.
関連性スコアの$u_t$とaの表現はバケットに依存する． 我々は、Control と Proposed の両バケットに対して、セクション 2 で述べた分散表現を用いて重複排除を行なった。 重複排除がユーザに与える影響についてはここでは触れないが，その実験については過去の論文[12]を参照されたい．

We can identify the user from browser cookies in addition to the ID for login. Therefore, we can extract some histories for most users including those who are not logged in. However, there are some users who have no history such as new users or who have been privately browsing. Although we can provide articles to them with other methods by using popularity, diversity, and freshness, instead of relevance scores, all results on them have been excluded from the following reports.
ログイン用のIDに加え、ブラウザのCookieからもユーザーを特定することができます。 そのため、ログインしていないユーザーを含め、ほとんどのユーザーについて、ある程度の履歴を抽出することが可能です。 しかし、新規ユーザーや個人的に閲覧しているユーザーなど、履歴のないユーザーも存在します。 彼らに対しては、関連性スコアの代わりに、人気度、多様性、鮮度を用いることで、他の方法で記事を提供することができるが、以下のレポートでは、彼らに関する結果は全て除外している。

### 6.2. Online Metrics 6.2. オンラインメトリクス

The list below represents the four online metrics we used.
以下のリストは、私たちが使用した4つのオンライン指標を表しています。

- Sessions: The average number of times one user utilized our service per day.
- セッション数。 1人のユーザーが1日に平均何回サービスを利用したか。

- Duration: The average time (in seconds) that the user spent with our service per session. It was the total time the user took looking at the recommendation list and the time it took him/her to read the article after clicking on it.
- 継続時間。 ユーザーが1回のセッションで弊社サービスを利用した平均時間（秒）。 これは、ユーザーがレコメンドリストを見るのにかかった時間と、レコメンドリストを見るのにかかった時間の合計である。

- Clicks: The average number of clicks per session (which corresponded to |P+| in Section 4).
  P+

- Click through rate (CTR): Clicks/number of displayed articles. These were decreased if article retrieval became inefficient and users spent more time exploring the recommendation list.
- クリックスルー率（CTR）。 クリック数

A session in this section means the collection of accesses by a user. It is regarded as another session if there is a gap of more than 10 min between accesses.
本項におけるセッションとは、あるユーザーによるアクセスの集合体を意味する。 10分以上の間隔が空くと別のセッションとみなされます。

Our most important metric is the total duration per user, which is the product of Sessions and Duration.
最も重要な指標は、「セッション」と「期間」の積である、ユーザーごとの総時間です。

### 6.3. Experimental Results 6.3. 実験結果

![](https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/500px/9-Figure6-1.png)

![](https://pic3.zhimg.com/80/v2-9c926fa7e7ffb79f710bc7bef9f4b5d6_720w.webp)

![](https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/8-Table4-1.png)

The results obtained from comparison are summarized in Figure 6 and Table 3.
比較の結果、得られた結果を図6と表3にまとめた。

Figure 6 plots the daily transition in the lift rate of each metric (i.e., that with the Proposed and metric with Control). All metrics improved significantly with the Proposed bucket. Duration, Clicks, and CTR indicated a certain rate of improvement from the first day the new model was applied. However, Sessions demonstrated a relatively small rate of improvement on the first day but gradually improved a great deal. This meant that a good recommendation model first increases clicks, and multiple click experiences encourage users to gradually use the service more frequently.
図 6 は，各メトリックス (Proposed と Control) のリフト率の日次推移をプロットしたものである． Proposed バケツでは，すべての指標が大きく改善された． Duration, Clicks, CTR は，新モデルを適用した初日から一定の改善率を示している． しかし，Sessions は初日の改善率は比較的小さいが，徐々に大きく改善した． これは、良いレコメンデーションモデルは、まずクリック数を増やし、複数回のクリック体験をすることで、徐々に利用頻度を高めていくことを意味しています。

Table 3 summarizes the average metric lift rates in the seventh week and those by user segments split according to the frequency of visits. The definitions for segments are three fold. The user composition ratios are roughly Heavy : Medium : Liдht = 3 : 2 : 1.
表3は、7週目の平均指標リフト率と、訪問頻度によって分割されたユーザーセグメントごとの指標リフト率をまとめたものである。 セグメントの定義は3つある。 ユーザーの構成比は、おおよそ、Heavy : Medium : Liдht = 3 : 2 : 1 である。

- Heavy:Users who have visited for more than five days during the previous week.
- ヘビー：前週に5日以上訪問したユーザー。

- Medium: Users who have visited for between two and five days during the previous week.
- ミディアム 前週2日以上5日未満の訪問ユーザー。

- Light: Users who have visited for less than two days during the previous week.
- ライト 前週の訪問日数が2日未満のユーザー。

Improvements in the metrics were confirmed for all segments. Light users demonstrated particularly large improvement rates. Therefore, we derived the following hypotheses. Users who had little history were strongly influenced by feature sparsity if we used BoW representations. Also, some noisy browsing caused by sudden interest seriously affected the accuracy of recommendations. Our method with the GRU-based model might successfully prevent these problems with distributed representations and the gate structures of GRU. This is why the Proposed bucket worked better than the Control bucket with the word-based model, especially for light users.
すべてのセグメントで指標の改善が確認された。 特にライトユーザーでは大きな改善率を示した。 そこで、以下の仮説を導出した。 履歴の少ないユーザは，BoW 表現を用いた場合，特徴量の疎密の影響を強く受ける． また、突発的な興味によるノイズの多い閲覧は、推薦の精度に深刻な影響を与えることがわかった。 GRUを用いた我々の手法は、分散表現とGRUのゲート構造により、これらの問題をうまく回避できる可能性がある。 このように、提案バケツは、特にライトユーザーに対して、単語ベースモデルを用いたControlバケツよりも有効であることが示された。

In addition to the improvement in metrics within each segment, we also observed a shift in users from Light to Medium, and Medium to Heavy, as listed in Table 4. This is why the overall rate of increase in Sessions was higher than the increase in each segment in Table 3.
各セグメント内の指標の改善に加えて、表4のように、ライトからミディアム、ミディアムからヘビーへのユーザーのシフトも確認されました。 そのため、表3の各セグメントでの増加率よりも、セッション数全体の増加率の方が高くなっています。

### 6.4. Deployment challenges to large-scale deep-learning-based services 6.4. 大規模な深層学習ベースのサービスに対するデプロイメントの課題

It is very important to keep updating models with the latest data when applying machine learning to actual news distribution systems. In fact, the Control bucket described in the previous section uses the latest article data and session data every three hours to update the model. The Proposed bucket using the GRU-based model, on the other hand, could not update the model as frequently due to four reasons.
実際のニュース配信システムに機械学習を適用する場合、最新のデータでモデルを更新し続けることが非常に重要です。 実際、前項のControlバケットでは、3時間ごとに最新の記事データとセッションデータを用いてモデルを更新している。 一方、GRUベースのモデルを用いたProposedバケットでは、4つの理由により、これほど頻繁にモデルを更新することができませんでした。

- It takes a long time to learn the model. In fact, the model actually used in main traffic is calculated over a week using GPU.
- モデルの学習には長い時間がかかります。 実際、メインのトラフィックで実際に使われているモデルは、GPUを使って1週間かけて計算されています。

- If we update the article-representation model (discussed in Section 3), we have to re-calculate representations for all available articles and re-index to the article search engine.
- もし、記事表現モデル（第3章で説明）を更新すれば、利用可能なすべての記事に対して表現を再計算し、記事検索エンジンに再インデックスしなければならない。

- If we update the user-representation model (discussed in Section 4), we have to re-calculate the user state from the first browse in the past. In practice, there is no choice but to give up on re-calculating old histories over a certain period of time.
- 4 章で説明するユーザー表現モデルを更新すると、過去 の最初の閲覧からユーザーの状態を再計算しなければならな い。 実際には、一定期間の古い履歴を再計算することはあきらめるしかない。

- The data store holding the user representations and the search index holding the article representations must be synchronously updated.
- ユーザー表現を保持するデータストアと記事表現を保持する検索インデックスは、同期的に更新される必要がある。

Therefore, we prepared two identical systems and switched them alternately to update the model once every two weeks. Of course, adding fresh articles and updating user states by users’ browsing are executed more frequently because they require fewer calculations than those for updating models.
そこで、同じシステムを2つ用意し、交互に切り替えて2週間に1回モデルを更新するようにした。 もちろん、新鮮な記事の追加やユーザーの閲覧によるユーザー状態の更新は、モデルの更新に比べて計算量が少ないため、より頻繁に実行される。

As word-based models in our experience have responded sensitively to buzz-words, they deteriorate as soon as a few days after stops have been updated; however, the distributed representationbased model maintains sufficient accuracy at this frequency of model updates. When we left the GRU-based model for about three months, it had deteriorated to the same accuracy as the word-based model with updates every three hours in experiments without model updates.
経験上、単語ベースモデルは流行語に敏感に反応するため、ストップ更新後数日で劣化するが、分散表現ベースモデルはこの程度のモデル更新頻度でも十分な精度を保つことができる。 GRUベースのモデルを3ヶ月ほど放置したところ、モデル更新のない実験では、3時間ごとに更新する単語ベースモデルと同等の精度まで劣化していた。

## 7. Related work 7. 関連作品

This section presents related work to our proposed approach.
このセクションでは、我々の提案するアプローチに関連する研究を紹介します。

We generated distributed representations of articles by using a denoising autoencoder with weak supervision, as described was in Section 3 and our previous paper [12]. There have been many studies on generating distributed representations of sentences. The conventional denoising auto-encoder [19], its variant [20], and Paragraph Vector [11] are well-known methods of unsupervised learning. Representations of articles generated with these methods may be used for our problem setting. While there have been reports [11, 16] that the representations generated with these methods provide helpful features for sentiment classification tasks, it has not been clarified whether these representations would be suitable for our purposes because these methods are unsupervised approaches.
我々は、セクション3および我々の前論文[12]で説明したように、弱い監視を伴うノイズ除去オートエンコーダを用いて記事の分散表現を生成した。 文の分散表現については多くの研究がなされている。 教師なし学習の手法としては、従来のノイズ除去オートエンコーダ[19]、その変形[20]、パラグラフベクトル[11]がよく知られている。 これらの手法で生成された記事の表現が我々の問題設定に利用される可能性がある。 これらの手法で生成された表現は、感情分類タスクに有用な特徴を提供するという報告[11, 16]があるが、これらの手法は教師なしアプローチであるため、これらの表現が我々の目的に適しているかどうかは明らかにされていない。

Of course, fully supervised methods can be applied if we obtain a sufficient amount of human-annotated data for article pairs, but this is too costly since news articles and the proper nouns they contain change over time. Therefore, our proposed method uses a weakly supervised method with an objective function that includes loss terms that correspond to the similarities between categories of articles, as well as reconstruction terms for the denoising autoencoder of words. As these categories, such as politics, sports, and entertainment, are provided by news publishers, they are easy to obtain. In addition, as distributed representations, which are generated by optimizing objective functions that consist of two terms, are expected to represent reasonable granularity of similarity, they inherit the properties of both words and categories.
もちろん，記事対の人間による注釈データが十分に得られれば完全教師付き手法を適用できるが，ニュース記事とそれに含まれる固有名詞は時間とともに変化するため，コストがかかりすぎる． そこで、提案手法では、記事のカテゴリ間の類似度に対応する損失項と、単語のノイズ除去オートエンコーダの再構成項を含む目的関数を用いた弱教師付き手法を用いる。 政治、スポーツ、芸能といったカテゴリーはニュース出版社から提供されているため、入手が容易である。 また、2つの項からなる目的関数を最適化することで生成される分散表現は、適度な粒度の類似度を表現することが期待されるため、単語とカテゴリの両方の特性を受け継いでいる。

There have been some studies [18, 21] on obtaining the representations of user interests from the sequence of users’ behaviors on the Web. Zhang et al. [21] proposed a framework based on an RNN for click prediction of sponsored search advertising. Tagami et al. [18] applied Paragraph Vector [11] to users’ Web browsing sequences to obtain common features from user-related prediction tasks. RNN and its variants have recently been widely used to obtain sequential data in various research fields, such as speech recognition [15], machine translation [17], and image captioning [9]. Learning with standard RNNs often suffers from vanishing and exploding gradient problems. Thus, some architectures such as LSTM [6] and GRU [1] have been employed to overcome these problems. Jozefowicz et al. [8] empirically evaluated various RNN architectures and reported that GRU outperformed LSTM on almost all tasks they evaluated. Our experimental results presented in Section 5.5 also showed that the GRU-based model produced better results than the LSTM-based model.
Web上でのユーザの一連の行動から、ユーザの興味の表現を得ることについては、いくつかの研究[18, 21]がある。 Zhangら[21]は、RNNを用いたスポンサードサーチ広告のクリック予測のためのフレームワークを提案した。 田上ら[18]は、ユーザー関連の予測タスクから共通の特徴を得るために、ユーザーのWeb閲覧シーケンスにParagraph Vector[11]を適用した。 RNNとその亜種は、最近、音声認識[15]、機械翻訳[17]、画像キャプション[9]など、様々な研究分野で逐次データを得るために広く利用されています。 標準的なRNNを用いた学習は、しばしば消失勾配や爆発勾配の問題に悩まされる。 そこで、これらの問題を克服するために、LSTM [6]やGRU [1]などのいくつかのアーキテクチャが採用されてきた。 Jozefowiczら[8]は、様々なRNNアーキテクチャを経験的に評価し、評価したほぼ全てのタスクでGRUがLSTMを上回ると報告している。 5.5節で紹介した我々の実験結果でも、GRUベースのモデルがLSTMベースのモデルよりも良い結果を出すことが示された。

## 8. Conclusion 8. 結論

This paper proposed an embedding-based method to use distributed representations in a three step end-to-end manner: (i) start with distributed representations of articles based on a variant of a denoising autoencoder, (ii) generate user representations by using an RNN with browsing histories as input sequences, and (iii) match and list articles for individual users based on inner-product operations by considering system performance. We found that our method was effective even in a real news distribution system with large-scale traffic because it was designed with an awareness of implementation.
本稿では、(i)ノイズ除去オートエンコーダの変形に基づく記事の分散表現から始め、(ii)閲覧履歴を入力列とするRNNを用いてユーザ表現を生成し、(iii)システム性能を考慮して内積演算により個々のユーザに対して記事のマッチングとリスト化を行う、埋め込みベースの手法をエンドツーエンドで提案する。 本手法は実装を意識して設計されているため、大規模トラフィックを有する実際のニュース配信システムにおいても有効であることがわかった。

The method we propose has already been fully incorporated in all the traffic of Yahoo! JAPAN’s homepage on smartphones, and it recommends various articles to millions of users every day. We plan to further improve our recommendation service continuously in the future and apply this approach to other domains such as advertisements.
私たちが提案する手法は、すでにYahoo! JAPANのスマートフォン向けホームページの全トラフィックに本格的に導入されており、毎日数百万人のユーザーに対してさまざまな記事を推薦しています。 今後、さらに継続的にレコメンデーションサービスを改善し、広告など他の領域にも本手法を適用していく予定です。
