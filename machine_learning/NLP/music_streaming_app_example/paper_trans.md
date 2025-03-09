
## Carousel Personalization in Music Streaming Apps with Contextual Bandits  
### WALID BENDADA, GUILLAUME SALHA, and THÉO BONTEMPELLI, Deezer, France  
音楽ストリーミングプラットフォームなどのメディアサービスプロバイダーは、ユーザーにパーソナライズされたコンテンツを推薦するために、スワイプ可能なカルーセルを頻繁に活用しています。 
However, selecting the most relevant items (albums, artists, playlists...) to display in these carousels is a challenging task, as items are numerous and as users have different preferences. 
しかし、これらのカルーセルに表示する最も関連性の高いアイテム（アルバム、アーティスト、プレイリストなど）を選択することは、アイテムが多数あり、ユーザーの好みが異なるため、困難な作業です。 
In this paper, we model carousel personalization as a contextual multi-armed bandit problem with multiple plays, cascade-based updates and delayed batch feedback. 
本論文では、カルーセルのパーソナライズを、複数のプレイ、カスケードベースの更新、および遅延バッチフィードバックを伴う文脈付きマルチアームバンディット問題としてモデル化します。 
We empirically show the effectiveness of our framework at capturing characteristics of real-world carousels by addressing a large-scale playlist recommendation task on a global music streaming mobile app. 
私たちは、グローバルな音楽ストリーミングモバイルアプリにおける大規模なプレイリスト推薦タスクに取り組むことで、実世界のカルーセルの特性を捉えるためのフレームワークの効果を実証的に示します。 
Along with this paper, we publicly release industrial data from our experiments, as well as an open-source environment to simulate comparable carousel personalization learning problems. 
この論文とともに、私たちの実験からの産業データを公開し、比較可能なカルーセルパーソナライズ学習問題をシミュレートするためのオープンソース環境も提供します。  
CCS Concepts: • Information systems → _Recommender systems; Personalization; Content ranking; • Computing methodologies_  
CCS概念: • 情報システム → _推薦システム; パーソナライズ; コンテンツランキング; • 計算方法論_  
→ _Learning paradigms; Online learning settings; Sequential decision making._  
→ _学習パラダイム; オンライン学習設定; シーケンシャル意思決定._  
Additional Key Words and Phrases: Multi-Armed Bandits with Multiple Plays, Contextual Bandits, Cascade Models, Expected Regret,  
追加のキーワードとフレーズ: 複数プレイのマルチアームバンディット、文脈付きバンディット、カスケードモデル、期待される後悔、  
Carousel Personalization, Playlist Recommendation, Music Streaming Platforms, A/B Testing  
カルーセルパーソナライズ、プレイリスト推薦、音楽ストリーミングプラットフォーム、A/Bテスト  
**ACM Reference Format:**  
**ACM参照形式:**  
Walid Bendada, Guillaume Salha, and Théo Bontempelli. 2020. Carousel Personalization in Music Streaming Apps with Contextual Bandits.  
Walid Bendada, Guillaume Salha, and Théo Bontempelli. 2020. 文脈付きバンディットを用いた音楽ストリーミングアプリにおけるカルーセルパーソナライズ。  
In Fourteenth ACM Conference on Recommender Systems (RecSys ’20), September 22–26, 2020, Virtual Event, Brazil.  
第14回ACM推薦システム会議（RecSys ’20）、2020年9月22日～26日、バーチャルイベント、ブラジル。  
ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/3383313.3412217  
ACM, ニューヨーク、NY、アメリカ、9ページ。 https://doi.org/10.1145/3383313.3412217  



## 1 INTRODUCTION はじめに

Recommending relevant and personalized content to users is crucial for media services providers, such as news [28], video [8] or music streaming [37] platforms.  
ユーザに関連性の高いパーソナライズされたコンテンツを推薦することは、ニュース [28]、ビデオ [8]、音楽ストリーミング [37] プラットフォームなどのメディアサービスプロバイダーにとって重要です。  
Indeed, effective recommender systems improve the users’ experience and engagement on the platform, by helping them navigate through massive amounts of content, enjoy their favorite videos or songs, and discover new ones that they might like [4, 37, 46].  
実際、効果的なレコメンダーシステムは、ユーザが膨大なコンテンツをナビゲートし、お気に入りのビデオや曲を楽しみ、気に入るかもしれない新しいものを発見する手助けをすることで、プラットフォーム上でのユーザの体験とエンゲージメントを向上させます [4, 37, 46]。  
As a consequence, significant efforts were initiated to transpose promising research on these aspects to industrial-level applications [8, 11, 17, 27, 32, 45].  
その結果、これらの側面に関する有望な研究を産業レベルのアプリケーションに移行するための重要な努力が始まりました [8, 11, 17, 27, 32, 45]。  

In particular, many global mobile apps and websites, notably from the music streaming industry, currently leverage _swipeable carousels to display recommended content on their homepages.  
特に、音楽ストリーミング業界の多くのグローバルなモバイルアプリやウェブサイトは、現在、推奨コンテンツをホームページに表示するために _スワイプ可能なカルーセルを活用しています。  
These carousels, also referred to as sliders or _shelves [32], consist in ranked lists of items or cards (albums, artists, playlists...).  
これらのカルーセルは、スライダーや _シェルフ [32] とも呼ばれ、アイテムやカード（アルバム、アーティスト、プレイリストなど）のランク付けされたリストで構成されています。  
A few cards are initially displayed to the users, who can click on them or swipe on the screen to see some of the additional cards from the carousel.  
最初にいくつかのカードがユーザに表示され、ユーザはそれらをクリックしたり、画面をスワイプしてカルーセルの追加カードを表示したりできます。  
Selecting and ranking the most relevant cards to display is a challenging task [12, 15, 31, 32], as the catalog size is usually significantly larger than the number of available slots in a carousel, and as users have different preferences.  
表示する最も関連性の高いカードを選択し、ランク付けすることは困難な作業です [12, 15, 31, 32]。カタログのサイズは通常、カルーセルの利用可能なスロット数よりも大幅に大きく、ユーザの好みも異なるためです。  
While being close to _slate recommendation [16, 18, 20, 40] and to learning to rank settings [30, 34, 36], carousel personalization also requires dealing with user feedback to adaptively improve the recommended content via online learning strategies [2, 6, 13], and integrating that some cards from the carousel might not be seen by users due to the swipeable structure.  
_slates推薦 [16, 18, 20, 40] やランク付け設定 [30, 34, 36] に近いものである一方で、カルーセルのパーソナライズには、ユーザのフィードバックを扱い、オンライン学習戦略 [2, 6, 13] を通じて推奨コンテンツを適応的に改善する必要があり、スワイプ可能な構造のためにカルーセルの一部のカードがユーザに見られない可能性があることを統合する必要があります。  

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page.  
この作業のすべてまたは一部のデジタルまたは印刷コピーを個人または教室で使用するために作成する許可は、コピーが利益または商業的利益のために作成または配布されず、コピーがこの通知と最初のページに完全な引用を含む限り、無料で付与されます。  
Copyrights for components of this work owned by others than the author(s) must be honored.  
著者以外の者が所有するこの作業のコンポーネントの著作権は尊重されなければなりません。  
Abstracting with credit is permitted.  
クレジット付きの要約は許可されています。  
To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee.  
それ以外の方法でコピーしたり、再出版したり、サーバーに投稿したり、リストに再配布したりするには、事前の特定の許可および/または料金が必要です。  
Request permissions from permissions@acm.org.  
permissions@acm.org から許可をリクエストしてください。  
© 2020 Copyright held by the owner/author(s). Publication rights licensed to ACM.  
© 2020 著作権は所有者/著者に帰属します。出版権はACMにライセンスされています。  
Manuscript submitted to ACM  
原稿はACMに提出されました。  

In this paper, we model carousel personalization as a multi-armed bandit with multiple plays [2] learning problem.  
本論文では、カルーセルのパーソナライズを複数のプレイを持つマルチアームバンディット [2] 学習問題としてモデル化します。  
Within our proposed framework, we account for important characteristics of real-world swipeable carousels, notably by considering that media services providers have access to contextual information on user preferences, that they might not know which cards from a carousel are actually seen by users, and that feedback data from carousels might not be available in real time.  
私たちの提案するフレームワーク内では、メディアサービスプロバイダーがユーザの好みに関する文脈情報にアクセスできること、カルーセルのどのカードが実際にユーザに見られているかを知らない可能性があること、カルーセルからのフィードバックデータがリアルタイムで利用できない可能性があることなど、実世界のスワイプ可能なカルーセルの重要な特性を考慮します。  
Focusing on music streaming applications, we show the effectiveness of our approach by addressing a large-scale carousel-based playlist recommendation task on the global mobile app Deezer[1].  
音楽ストリーミングアプリケーションに焦点を当て、グローバルモバイルアプリDeezer[1]における大規模なカルーセルベースのプレイリスト推薦タスクに取り組むことで、私たちのアプローチの効果を示します。  
With this paper, we also release industrial data from our experiments, as well as an open-source environment to simulate comparable carousel personalization learning problems.  
本論文では、実験からの産業データと、比較可能なカルーセルパーソナライズ学習問題をシミュレートするためのオープンソース環境も公開します。  
This paper is organized as follows.  
本論文は以下のように構成されています。  
In Section 2, we introduce and formalize our multi-armed bandit framework for carousel personalization.  
第2節では、カルーセルのパーソナライズのためのマルチアームバンディットフレームワークを紹介し、形式化します。  
We detail our data, our playlist recommendation task and our experimental setting in Section 3.  
第3節では、データ、プレイリスト推薦タスク、および実験設定の詳細を説明します。  
We present and discuss our results in Section 4, and we conclude in Section 5.  
第4節では結果を提示し、議論し、第5節で結論を述べます。  



## 2 A CONTEXTUAL MULTI-ARMED BANDIT FRAMEWORK FOR CAROUSEL PERSONALIZATION
## 2 カルーセルパーソナライズのための文脈的マルチアームバンディットフレームワーク

In this section, after reviewing key notions on multi-armed bandits with multiple plays, we introduce our framework.
このセクションでは、複数プレイを持つマルチアームバンディットの重要な概念をレビューした後、私たちのフレームワークを紹介します。

**2.1** **Background on Multi-Armed Bandits with Multiple Plays**
**2.1** **複数プレイを持つマルチアームバンディットの背景**

Multi-armed bandits are among the most famous instances of sequential decision making problems [23, 38, 39]. 
マルチアームバンディットは、逐次的意思決定問題の中で最も有名な例の一つです [23, 38, 39]。 
Multi armed bandits with multiple plays [2, 22] involve K entities called arms. 
複数プレイを持つマルチアームバンディット [2, 22] は、アームと呼ばれるK個のエンティティを含みます。 
At each round $t = 1, 2, ..., T$, a forecaster has to select a set $S_t \subset \{1, ..., K\}$ of $L < K$ arms (while $L = 1$ in the single play version of the problem [38]). 
各ラウンド$t = 1, 2, ..., T$において、予測者は$L < K$のアームの集合$S_t \subset \{1, ..., K\}$を選択しなければなりません（問題の単一プレイバージョンでは$L = 1$です [38]）。 
The forecaster then receives some rewards from the selected arms, that we assume to be binary. 
予測者は次に、選択したアームから報酬を受け取りますが、これをバイナリであると仮定します。 
The reward associated to an arm $i \in S_t$ is a sample drawn from a Bernoulli($p_i$) distribution, with $p_i \in [0, 1]$ being an unknown parameter. 
アーム$i \in S_t$に関連する報酬は、未知のパラメータ$p_i \in [0, 1]$を持つベルヌーイ分布から引き出されたサンプルです。 
Bernoulli distributions of arms $1, ..., K$ are assumed independent, which we later discuss. 
アーム$1, ..., K$のベルヌーイ分布は独立であると仮定され、これについては後で議論します。 
The objective of the forecaster is to maximize the sum of rewards received from the selected arms over time. 
予測者の目的は、選択したアームから受け取る報酬の合計を時間の経過とともに最大化することです。 
It requires identifying the optimal set $\delta^*(L) \subset \{1, ..., K\}$ of the $L$ arms associated to the top-$L$ highest Bernoulli parameters, i.e. the $L$ highest expected rewards, as fast as possible. 
これは、最適な集合$\delta^*(L) \subset \{1, ..., K\}$を特定することを必要とし、これはトップ-$L$の最高ベルヌーイパラメータに関連する$L$アーム、すなわち$L$の最高期待報酬です。 
In such problems, the forecaster faces an exploration-exploitation dilemma. 
このような問題では、予測者は探索と活用のジレンマに直面します。 
As the environment does not reveal the rewards of the unselected arms, the forecaster needs to try all arms over time to identify the best ones (exploration). 
環境が未選択のアームの報酬を明らかにしないため、予測者は時間の経過とともにすべてのアームを試して最良のものを特定する必要があります（探索）。 
However, selecting underperforming arms also leads to lower expected rewards, which encourages the forecaster to repeatedly select the assumed best ones (exploitation). 
しかし、パフォーマンスの悪いアームを選択することは期待報酬を低下させるため、予測者は仮定された最良のものを繰り返し選択することを促されます（活用）。 
Over the past years, several strategies have been proposed and studied, aiming at providing efficient trade-offs between these two opposite objectives when sequentially selecting sets $S_t$. 
過去数年間、$S_t$の集合を逐次的に選択する際に、これら二つの相反する目的の間で効率的なトレードオフを提供することを目指したいくつかの戦略が提案され、研究されてきました。 
Notable examples include the Upper Confidence Bound (UCB) [3, 6, 26, 44] and Thompson Sampling [5, 22, 42] algorithms (see Section 3). 
注目すべき例には、上限信頼区間（UCB） [3, 6, 26, 44] とトンプソンサンプリング [5, 22, 42] アルゴリズムが含まれます（セクション3を参照）。 
The expected cumulative regret $Reg(T) = \sum_{t=1}^{T} \sum_{i \in \delta^*(L)} p_i - \sum_{i \in S_t} p_i$, which represents the expected total loss endured by the forecaster by selecting non-optimal sets of arms at rounds 1 to $T$, is a common measure to compare the performances of strategies addressing this top-$L$ best arms identification problem [2, 6, 22, 38, 39, 44]. 
期待累積後悔$Reg(T) = \sum_{t=1}^{T} \sum_{i \in \delta^*(L)} p_i - \sum_{i \in S_t} p_i$は、ラウンド1から$T$までの非最適なアームの集合を選択することによって予測者が被る期待総損失を表し、このトップ-$L$の最良アーム識別問題に対処する戦略の性能を比較するための一般的な指標です [2, 6, 22, 38, 39, 44]。

**2.2** **Multi-Armed Bandits with Multiple Plays for Carousel Personalization**
**2.2** **カルーセルパーソナライズのための複数プレイを持つマルチアームバンディット**

Throughout this paper, the K arms will correspond to a list of K cards/items, such as a catalog of albums or playlists in a music streaming app. 
本論文を通じて、Kアームは音楽ストリーミングアプリのアルバムやプレイリストのカタログなど、K枚のカード/アイテムのリストに対応します。 
They can be recommended to N users through a swipeable carousel containing $L \ll K$ slots. 
これらは、$L \ll K$のスロットを含むスワイプ可能なカルーセルを通じてNユーザーに推奨されることができます。 
As users have various preferences, different cards can be displayed to different users. 
ユーザーにはさまざまな好みがあるため、異なるカードが異なるユーザーに表示されることがあります。 
The $L$ recommended cards from the carousel of each user, i.e. the $L$ selected arms for each user, are updated at regular intervals or rounds, whose frequency depends on the technical constraints of the platform. 
各ユーザーのカルーセルからの$L$枚の推奨カード、すなわち各ユーザーの$L$選択アームは、プラットフォームの技術的制約に依存する頻度で定期的に更新されます。 
We aim at optimizing display-to-stream rates, i.e. at identifying the $L$ cards for which each user is the most likely to click and then to stream the underlying content, at least once during the round. 
私たちは、表示からストリームへの率を最適化することを目指しており、すなわち、各ユーザーがラウンド中に少なくとも一度クリックし、その後基礎となるコンテンツをストリーミングする可能性が最も高い$L$枚のカードを特定することを目指しています。 
When a card $i$ is displayed to a user $u$, such streaming activity, i.e. a reward of 1, occurs during the round with an unknown probability $p_{ui} \in [0, 1]$. 
カード$i$がユーザー$u$に表示されると、そのストリーミング活動、すなわち報酬1が、未知の確率$p_{ui} \in [0, 1]$でラウンド中に発生します。 
Here, we assume that the number of cards, the number of users, and the display-to-stream probabilities $p_{ui}$ are fixed; we later discuss these assumptions. 
ここでは、カードの数、ユーザーの数、および表示からストリームへの確率$p_{ui}$が固定されていると仮定します。これらの仮定については後で議論します。 
A naive way to tackle this problem would consist in simultaneously running $N$ standard bandit algorithms, aiming at individually identifying the top-$L$ cards with highest $p_{ui}$ probabilities for each user $u$. 
この問題に対処するための単純な方法は、$N$の標準バンディットアルゴリズムを同時に実行し、各ユーザー$u$に対して$p_{ui}$確率が最も高いトップ-$L$カードを個別に特定することです。 
This approach is actually unsuitable and would require a too long training time to reach convergence. 
このアプローチは実際には不適切であり、収束に達するために非常に長いトレーニング時間を必要とします。 
Indeed, the number of display-to-stream parameters to estimate would be $K \times N$, which is very large in practice as platforms often have millions of active users. 
実際、推定する必要のある表示からストリームへのパラメータの数は$K \times N$となり、プラットフォームには通常数百万のアクティブユーザーがいるため、実際には非常に大きいです。 
In Section 2.3, we describe two strategies to address this problem by leveraging contextual information on user preferences.
セクション2.3では、ユーザーの好みに関する文脈情報を活用してこの問題に対処するための2つの戦略を説明します。

**2.3** **Leveraging Contextual Information on User Preferences**
**2.3** **ユーザーの好みに関する文脈情報の活用**

_2.3.1_ _Semi-Personalization via User Clustering. First, let us assume that we have access to a clustering of users, constructed from users’ past behaviours on the platform. 
_2.3.1_ _ユーザークラスタリングによるセミパーソナライズ。まず、プラットフォーム上のユーザーの過去の行動から構築されたユーザーのクラスタリングにアクセスできると仮定しましょう。 
Each user belongs to one of the $Q$ groups $C_1, C_2, ..., C_Q$ with $Q \ll N$. 
各ユーザーは、$Q \ll N$のグループ$C_1, C_2, ..., C_Q$のいずれかに属します。 
For instance, on a music streaming app, users from a same group would have homogeneous musical tastes. 
例えば、音楽ストリーミングアプリでは、同じグループのユーザーは均質な音楽の好みを持つと考えられます。 
We propose to assume that users from a same group have identical expected display-to-stream probabilities for each card: 
私たちは、同じグループのユーザーが各カードに対して同一の期待表示からストリームへの確率を持つと仮定することを提案します： 
$$
\forall c \in \{C_1, ..., C_Q\}, \forall u \in c, \forall i \in \{1, ..., K\}, p_{ui} = p_c.
$$
$$
\forall c \in \{C_1, ..., C_Q\}, \forall u \in c, \forall i \in \{1, ..., K\}, p_{ui} = p_c.
$$
Then, we simultaneously run $Q$ bandit algorithms, one for each cluster, to identify the top-$L$ best cards to recommend to each group. 
次に、各クラスタごとに1つの$Q$バンディットアルゴリズムを同時に実行し、各グループに推奨するトップ-$L$の最良カードを特定します。 
This strategy reduces the number of parameters to estimate to $K \times Q$, which is significantly fewer than $K \times N$ in practice. 
この戦略は、推定するパラメータの数を$K \times Q$に減少させ、実際には$K \times N$よりも大幅に少なくなります。 
Moreover, thanks to such users gathering, platforms receive more feedback on each displayed card w.r.t. the previous naive setting. 
さらに、このようなユーザーの集まりのおかげで、プラットフォームは以前の単純な設定に対して各表示カードに関するより多くのフィードバックを受け取ります。 
This ensures a faster and more robust identification of optimal sets. 
これにより、最適なセットの特定がより迅速かつ堅牢になります。 
However, the empirical performance of this strategy also strongly depends on the quality of the underlying user clustering. 
しかし、この戦略の経験的なパフォーマンスは、基盤となるユーザークラスタリングの質にも大きく依存します。 

_2.3.2_ _Contextual Multi-Armed Bandits. Instead of relying on clusters, let us now assume that we directly have access to a D-dimensional attribute vector $x_u \in \mathbb{R}^D$ for each user $u$. 
_2.3.2_ _文脈的マルチアームバンディット。クラスタに依存するのではなく、各ユーザー$u$に対して直接$D$次元の属性ベクトル$x_u \in \mathbb{R}^D$にアクセスできると仮定しましょう。 
These vectors aim at summarizing user preferences on the platform, e.g. their musical tastes (in terms of genres, moods, countries...) for a music streaming app. 
これらのベクトルは、プラットフォーム上のユーザーの好みを要約することを目的としており、例えば音楽ストリーミングアプリにおける音楽の好み（ジャンル、ムード、国など）を示します。 
We assume that the expected display-to-stream probabilities of a user $u$ are functions of his/her attribute vector: 
ユーザー$u$の期待表示からストリームへの確率は、彼/彼女の属性ベクトルの関数であると仮定します： 
$$
\forall i \in \{1, ..., K\}, p_{ui} = \sigma(x_u^T \theta_i),
$$
$$
\forall i \in \{1, ..., K\}, p_{ui} = \sigma(x_u^T \theta_i),
$$
where $\theta_1, ..., \theta_K$ are $D$-dimensional weight vectors to learn for each of the $K$ arms, and where $\sigma(\cdot)$ is the sigmoid function: $\sigma(x) = \frac{1}{1 + e^{-x}}$. 
ここで、$\theta_1, ..., \theta_K$は各$K$アームのために学習する$D$次元の重みベクトルであり、$\sigma(\cdot)$はシグモイド関数です：$\sigma(x) = \frac{1}{1 + e^{-x}}$。 
This corresponds to the contextual bandit setting [1, 7, 28], a popular learning paradigm for online recommender systems [12, 28, 29, 32, 35, 41, 43, 47, 48]. 
これは文脈的バンディット設定 [1, 7, 28] に対応し、オンラインレコメンダーシステムのための人気のある学習パラダイムです [12, 28, 29, 32, 35, 41, 43, 47, 48]。 
Strategies to learn weight vectors are detailed e.g. in [5, 32]. 
重みベクトルを学習するための戦略は、例えば[5, 32]で詳述されています。 
As $D \ll N$ in practice, such strategy also significantly reduces the number of parameters, to $K \times D$. 
実際には$D \ll N$であるため、この戦略はパラメータの数を$K \times D$に大幅に削減します。 
By design, users with similar preferences will have close expected display-to-stream probabilities. 
設計上、類似の好みを持つユーザーは、期待表示からストリームへの確率が近くなります。 
Moreover, all $N$ users can end up with different optimal carousels, contrary to the aforementioned semi-personalized clustering approach. 
さらに、すべての$N$ユーザーは、前述のセミパーソナライズされたクラスタリングアプローチとは異なり、異なる最適なカルーセルを持つことができます。 

**2.4** **Capturing Characteristics of Real-World Carousels: Cascade-Based Updates, Delayed Feedback**
**2.4** **実世界のカルーセルの特性を捉える：カスケードベースの更新、遅延フィードバック**

In our framework, we also aim at capturing other important characteristics of real-world swipeable carousels. 
私たちのフレームワークでは、実世界のスワイプ可能なカルーセルの他の重要な特性を捉えることも目指しています。 
In particular, while standard bandit algorithms usually consider that the forecaster receives rewards (0 or 1) from each of the $L$ selected arms at each round, in our setting some selected cards might actually not be seen by users. 
特に、標準的なバンディットアルゴリズムは通常、予測者が各ラウンドで選択された$L$のアームから報酬（0または1）を受け取ると考えますが、私たちの設定では、選択されたカードのいくつかは実際にはユーザーに見られない可能性があります。 
As illustrated in Figure 1, only a few cards, say $L_{init} < L$, are initially displayed on a user’s screen. 
図1に示すように、最初にユーザーの画面に表示されるのはごく少数のカード、例えば$L_{init} < L$です。 
The user needs to swipe right to see additional cards. 
ユーザーは追加のカードを見るために右にスワイプする必要があります。 
As we later verify, ignoring this important aspect, and thus returning a reward of 0 for all unclicked cards at each round whatever their rank in the carousel, would lead to underestimating display-to-stream probabilities. 
後で確認するように、この重要な側面を無視し、したがってカルーセル内のランクに関係なく、各ラウンドでクリックされなかったすべてのカードに対して報酬0を返すことは、表示からストリームへの確率を過小評価することにつながります。 
In this paper, we assume that we do not exactly know how many cards were seen by each user. 
本論文では、各ユーザーが何枚のカードを見たかを正確には知らないと仮定します。 
Such assumption is consistent with Deezer’s actual usage data and is realistic. 
この仮定は、Deezerの実際の使用データと一致しており、現実的です。 
Indeed, on many real-world mobile apps carousels, users usually do not click on any button to discover additional cards, but instead need to continuously swipe left and right on the screen. 
実際、多くの実世界のモバイルアプリのカルーセルでは、ユーザーは追加のカードを発見するためにボタンをクリックすることはなく、代わりに画面上で左に右にスワイプし続ける必要があります。 
As a consequence, the card display information is ambiguous, and is technically hard to track with accuracy. 
その結果、カードの表示情報はあいまいであり、技術的に正確に追跡することが難しいです。 
Here, to address this problem, we consider and later evaluate a cascade-based arm update model. 
ここで、この問題に対処するために、カスケードベースのアーム更新モデルを考慮し、後で評価します。 
We draw inspiration from the cascade model [9], a popular approach to represent user behaviours when facing ranked lists of recommended items in an interface, with numerous applications and extensions [21, 24, 25, 49]. 
私たちは、インターフェースで推奨アイテムのランク付けされたリストに直面したときのユーザーの行動を表現するための人気のあるアプローチであるカスケードモデル [9] からインスピレーションを得ており、多くのアプリケーションや拡張があります [21, 24, 25, 49]。 
At each round, we consider that: 
各ラウンドで、私たちは次のことを考慮します： 
- An active user who did not stream any card during the round only saw the $L_{init}$ first ones. 
- ラウンド中にカードをストリーミングしなかったアクティブユーザーは、最初の$L_{init}$枚だけを見ました。 
- An active user who streamed the $i^{th}$ card, with $i \in \{1, ..., L\}$, saw all cards from ranks 1 to $\max(L_{init}, i)$. 
- $i \in \{1, ..., L\}$のカードをストリーミングしたアクティブユーザーは、ランク1から$\max(L_{init}, i)$までのすべてのカードを見ました。 
For instance, let $L_{init} = 3$ and $L = 12$. 
例えば、$L_{init} = 3$および$L = 12$としましょう。 
The reward vectors obtained from users who a) did not stream during the round, b) only streamed the 2nd card, and c) streamed the 2nd and 6th cards, are as follows, with $X$ denoting no reward: 
ラウンド中にストリーミングしなかったユーザー、b) 2番目のカードのみをストリーミングしたユーザー、c) 2番目と6番目のカードをストリーミングしたユーザーから得られる報酬ベクトルは次のとおりで、$X$は報酬なしを示します： 
$$
a : [0, 0, 0, X, X, X, X, X, X, X, X, X]
$$
$$
a : [0, 0, 0, X, X, X, X, X, X, X, X, X]
$$
$$
b : [0, 1, 0, X, X, X, X, X, X, X, X, X]
$$
$$
b : [0, 1, 0, X, X, X, X, X, X, X, X, X]
$$
$$
c : [0, 1, 0, 0, 0, 1, X, X, X, X, X, X]
$$
$$
c : [0, 1, 0, 0, 0, 1, X, X, X, X, X, X]
$$
Last, to be consistent with real-world constraints, we assume that rewards are not processed on the fly but by batch, at the end of each round e.g. every day. 
最後に、実世界の制約と一致させるために、報酬はその場で処理されるのではなく、各ラウンドの終わりにバッチで処理されると仮定します（例えば、毎日）。 
We study the impact of such delayed batch feedback in our upcoming experiments. 
私たちは、今後の実験でこのような遅延バッチフィードバックの影響を研究します。 

**2.5** **Related Work**
**2.5** **関連研究**

Bandits are very popular models for online recommendation [28, 29, 33–36, 41, 43, 47]. 
バンディットはオンライン推薦のための非常に人気のあるモデルです [28, 29, 33–36, 41, 43, 47]。 
In particular, [12] and [32] also recently studied carousel personalization in mobile apps. 
特に、[12]および[32]は最近、モバイルアプリにおけるカルーセルパーソナライズを研究しました。 
[32] introduced a contextual bandit close to our Section 2.3.2. 
[32]は、私たちのセクション2.3.2に近い文脈的バンディットを紹介しました。 
However, their approach focuses more on explainability, they do not model cascade-based displays and do not integrate semi-personalized strategies. 
しかし、彼らのアプローチは説明可能性により重点を置いており、カスケードベースの表示をモデル化せず、セミパーソナライズされた戦略を統合していません。 
[12] also considered contextual bandits inspired from [32] for playlist recommendation in carousels, but did not provide details on their models. 
[12]もまた、カルーセルにおけるプレイリスト推薦のために[32]からインスパイアされた文脈的バンディットを考慮しましたが、彼らのモデルに関する詳細は提供していません。 
They instead aimed at predicting the online ranking of these models from various offline evaluations. 
彼らは代わりに、さまざまなオフライン評価からこれらのモデルのオンラインランキングを予測することを目指しました。 
Last, other different sets of ordered items have been studied [16, 18–20, 40, 49]. 
最後に、他の異なる順序付けされたアイテムのセットが研究されています [16, 18–20, 40, 49]。



## 3 EXPERIMENTAL SETTING 実験設定

In the following, we empirically evaluate and discuss the effectiveness of our carousel personalization framework.
以下に、私たちのカルーセルパーソナライズフレームワークの効果を実証的に評価し、議論します。

**3.1** **Playlist Recommendation on a Global Music Streaming App**
**3.1** **グローバル音楽ストリーミングアプリにおけるプレイリスト推薦**

We study a large-scale carousel-based playlist recommendation task on the global mobile app Deezer. 
私たちは、グローバルモバイルアプリDeezerにおける大規模なカルーセルベースのプレイリスト推薦タスクを研究します。

We consider _K = 862 playlists, that were created by professional curators from Deezer with the purpose of complying with a specific_ music genre, cultural area or mood, and that are among the most popular ones on the service. 
私たちは、特定の音楽ジャンル、文化的領域、またはムードに従うことを目的としてDeezerのプロのキュレーターによって作成された_K = 862のプレイリストを考慮し、これらはサービス上で最も人気のあるものの中にあります。

Playlists’ cover images constitute the cards that can be recommended to users on the app homepage in a carousel, updated on a daily basis, with L = 12 available slots and Linit = 3 cards initially displayed. 
プレイリストのカバー画像は、アプリのホームページでユーザーにカルーセル形式で推薦できるカードを構成し、毎日更新され、L = 12の利用可能なスロットと最初に表示されるLinit = 3のカードがあります。

Figure 1 provides an illustration of the carousel.
図1はカルーセルの例を示しています。

To determine which method would best succeed in making users click and stream the displayed playlists, extensive experiments were conducted in two steps. 
どの方法がユーザーにクリックさせ、表示されたプレイリストをストリーミングさせるのに最も成功するかを判断するために、広範な実験が2つのステップで実施されました。

First, offline experiments simulating users’ responses to carousel-based recommendations were run, on a simulation environment and on data that we both publicly release[2] with this paper (see Section 3.2). 
まず、カルーセルベースの推薦に対するユーザーの反応をシミュレートするオフライン実験が、シミュレーション環境と、私たちがこの論文と共に公開するデータ上で実施されました[2]（セクション3.2を参照）。

We believe that such industrial data and code release will benefit the research community and future works. 
私たちは、このような産業データとコードの公開が研究コミュニティや今後の研究に利益をもたらすと信じています。

Then, an online large-scale A/B test was run on the Deezer app to validate the findings of offline experiments. 
次に、オフライン実験の結果を検証するために、Deezerアプリでオンラインの大規模A/Bテストが実施されました。

[2 Data and code are available at: https://github.com/deezer/carousel_bandits](https://github.com/deezer/carousel_bandits)

**3.2** **A Simulation Environment and Dataset for Offline Evaluation of Carousel-Based Recommendation**
**3.2** **カルーセルベースの推薦のオフライン評価のためのシミュレーション環境とデータセット**

For offline experiments, we designed a simulated environment in Python based on 974 960 fully anonymized Deezer users. 
オフライン実験のために、974,960人の完全に匿名化されたDeezerユーザーに基づいてPythonでシミュレーション環境を設計しました。

We release a dataset in which each user u is described by a feature vector xu of dimension D = 97, computed internally by factorizing the interaction matrix between users and songs as described in [14] and then adding a bias term. 
私たちは、各ユーザーuが次元D = 97の特徴ベクトルxuで記述されるデータセットを公開します。これは、[14]で説明されているように、ユーザーと曲の間の相互作用行列を因数分解し、バイアス項を追加することによって内部的に計算されます。

A k-means clustering with Q = 100 clusters was also performed to assign each user to a single cluster. 
各ユーザーを単一のクラスターに割り当てるために、Q = 100のクラスターを用いたk-meansクラスタリングも実施されました。

In addition, for each user-playlist pair, we release a "ground-truth" display-to-stream probability $p_{ui} = \sigma (x_u^T \theta_i)$ where, as in [5], the _D-dimensional vectors $\theta_i$ were estimated by fitting a logistic regression on a click data history from January 2020._ 
さらに、各ユーザー-プレイリストペアについて、私たちは「真の」表示からストリームへの確率$p_{ui} = \sigma (x_u^T \theta_i)$を公開します。ここで、[5]のように、_D次元ベクトル$\theta_i$は2020年1月のクリックデータ履歴に対してロジスティック回帰を適合させることによって推定されました。_

Simulations proceed as follows. 
シミュレーションは次のように進行します。

At each round, a random subset of users (20 000, in the following) is presented to several sequential algorithms a.k.a. policies to be evaluated. 
各ラウンドで、ランダムなユーザーのサブセット（以下、20,000）が評価されるいくつかの逐次アルゴリズム、すなわちポリシーに提示されます。

These policies must then recommend an ordered set of $L = 12$ playlists to each user. 
これらのポリシーは、各ユーザーに$L = 12$のプレイリストの順序付けられたセットを推薦しなければなりません。

Streams, i.e. positive binary rewards, are generated according to the aforementioned display-to-stream probabilities and to a configurable cascading browsing model capturing that users explore the carousel from left to right and might not see all recommended playlists. 
ストリーム、すなわち正のバイナリ報酬は、前述の表示からストリームへの確率と、ユーザーがカルーセルを左から右に探索し、すべての推薦されたプレイリストを見ることができない可能性を捉えた構成可能なカスケードブラウジングモデルに基づいて生成されます。

At the end of each round, all policies update their model based on the set of users and on binary rewards received from displayed playlists. 
各ラウンドの終了時に、すべてのポリシーは、ユーザーのセットと表示されたプレイリストから受け取ったバイナリ報酬に基づいてモデルを更新します。

Expected cumulative regrets of policies [2, 22, 39] w.r.t. the optimal top-$L$ playlists sets according to $p_{ui}$ probabilities are computed.
ポリシー[2, 22, 39]の期待累積後悔は、$p_{ui}$確率に基づく最適なトップ-$L$プレイリストセットに対して計算されます。

**3.3** **Algorithms**
**3.3** **アルゴリズム**

In our experiments, we evaluate semi-personalized versions of several popular sequential decision making algorithms/policies, using the provided $Q = 100$ clusters, and compare their performances against fully-personalized methods. 
私たちの実験では、提供された$Q = 100$のクラスターを使用して、いくつかの人気のある逐次意思決定アルゴリズム/ポリシーのセミパーソナライズ版を評価し、完全にパーソナライズされた方法とそのパフォーマンスを比較します。

As detailed in Section 2.3.1, users within a given cluster share parameters for all semi-personalized policies; they are the ones whose names end with -seg in the following list. 
セクション2.3.1で詳述されているように、特定のクラスター内のユーザーはすべてのセミパーソナライズポリシーのパラメータを共有します。これらは、以下のリストで名前が-segで終わるものです。

We consider the following methods:
以下の方法を考慮します：

- random: a simple baseline that randomly recommends $L$ playlists to each user.
- random: 各ユーザーにランダムに$L$のプレイリストを推薦するシンプルなベースライン。

- ϵ-greedy-seg: recommends playlists randomly with probability ϵ, otherwise recommends the top-$L$ with highest mean observed rewards. 
- ϵ-greedy-seg: 確率ϵでランダムにプレイリストを推薦し、そうでなければ観測された平均報酬が最も高いトップ-$L$を推薦します。

Two versions, ϵ-greedy-seg-explore (ϵ=0.1) and ϵ-greedy-seg-exploit (ϵ=0.01) are evaluated.
2つのバージョン、ϵ-greedy-seg-explore (ϵ=0.1)とϵ-greedy-seg-exploit (ϵ=0.01)が評価されます。

- etc-seg: an explore then commit strategy, similar to random until all arms have been played n times, then recommends the top-$L$ playlists. 
- etc-seg: 探索してからコミットする戦略で、すべてのアームがn回プレイされるまでランダムに似ており、その後トップ-$L$プレイリストを推薦します。

Two versions, etc-seg-explore (n = 100) and etc-seg-exploit (n = 20) are evaluated.
2つのバージョン、etc-seg-explore (n = 100)とetc-seg-exploit (n = 20)が評価されます。

- kl-ucb-seg: the Upper Confidence Bound (UCB) strategy [3, 6, 26], that tackles the exploration-exploitation trade-off by computing confidence intervals for the estimation of each arm probability, then selecting the $L$ arms with highest upper confidence bounds. 
- kl-ucb-seg: 上限信頼区間（UCB）戦略[3, 6, 26]で、各アームの確率の推定に対する信頼区間を計算することによって探索と活用のトレードオフに対処し、次に最も高い上限信頼区間を持つ$L$アームを選択します。

Here, we use KL-UCB bounds [10], tailored for Bernoulli rewards.
ここでは、ベルヌーイ報酬に合わせたKL-UCB境界[10]を使用します。

- ts-seg: the Thompson Sampling strategy [5, 42], in which estimated display-to-stream probabilities are samples drawn from Beta distributions [42], whose parameters are updated at each round in a Bayesian fashion, such that variance tends towards zero and expectation converges to empirical mean as more rewards are observed.
- ts-seg: トンプソンサンプリング戦略[5, 42]で、推定された表示からストリームへの確率は、ベータ分布[42]から引き出されたサンプルであり、そのパラメータは各ラウンドでベイズ的に更新され、分散はゼロに近づき、期待値はより多くの報酬が観測されるにつれて経験的平均に収束します。

Two versions, ts-seg-naive (prior distributions are Beta(1, 1), i.e. Uniform(0, 1)) and ts-seg-pessimistic (priors are Beta(1, 99)) are evaluated.
2つのバージョン、ts-seg-naive（事前分布はBeta(1, 1)、すなわちUniform(0, 1)）とts-seg-pessimistic（事前分布はBeta(1, 99)）が評価されます。

As the UCB algorithm [6], Thompson Sampling is backed by strong theoretical guarantees [22] on speeds of expected cumulative regrets in the multi-armed bandit with multiple plays setting.
UCBアルゴリズム[6]と同様に、トンプソンサンプリングは、複数のプレイ設定における期待累積後悔の速度に関する強力な理論的保証[22]に支えられています。

- ts-lin: an extension of Thompson Sampling [5] to the linear contextual framework from Section 2.3.2. 
- ts-lin: セクション2.3.2の線形コンテキストフレームワークへのトンプソンサンプリング[5]の拡張です。

We follow the method of [5] to learn $\theta_i$ vectors for each arm $i$ from Gaussian prior distributions. 
私たちは、ガウス事前分布から各アーム$i$のための$\theta_i$ベクトルを学習するために[5]の方法に従います。

Two versions, ts-lin-naive (0 means for all dimensions of the prior) and ts-lin-pessimistic (-5 mean for the bias dimension prior) are evaluated.
2つのバージョン、ts-lin-naive（事前のすべての次元の平均は0）とts-lin-pessimistic（バイアス次元事前の平均は-5）が評価されます。

By default, policies always abide by the cascade model introduced in Section 2.4, meaning they do not update the parameters relative to recommended playlists that the cascade model labels as unseen. 
デフォルトでは、ポリシーは常にセクション2.4で導入されたカスケードモデルに従い、カスケードモデルが未表示とラベル付けした推薦プレイリストに関連するパラメータを更新しません。

For comparison, we also implemented versions of these policies that do not abide by this behaviour. 
比較のために、私たちはこの動作に従わないこれらのポリシーのバージョンも実装しました。

In the following, they are labelled no-cascade.
以下では、これらはno-cascadeとラベル付けされます。



## 4 EXPERIMENTAL RESULTS 実験結果

**4.1** **Offline Evaluation オフライン評価**  
Fig. 2. Offline evaluation of top-12 playlist recommendation: expected cumulative regrets of policies over 100 simulated rounds. 
図2. トップ12プレイリスト推薦のオフライン評価：100回のシミュレーションラウンドにおけるポリシーの期待累積後悔。 
The empirical gain of ts-seg-pessimistic w.r.t. others is statistically significant at the 1% level (p-value <0.01). 
ts-seg-pessimisticの他のポリシーに対する経験的な利得は、1%の水準で統計的に有意です（p値 <0.01）。

_4.1.1_ _Semi-Personalization vs Personalization. Figure 2 provides cumulative regrets over 100 rounds for the different policies, recommending playlists via our offline environment._  
_4.1.1_ _セミパーソナライズとパーソナライズ。図2は、オフライン環境を通じてプレイリストを推薦する異なるポリシーの100ラウンドにわたる累積後悔を示しています。_  
Both etc-seg-explore and etc-seg-exploit behave as badly as random in the exploration phase, then, shortly after starting to exploit, they both reach competitive performances as illustrated by the brutal flattening of their cumulative regret curves, with etc-seg-exploit transitioning 50 rounds earlier.  
etc-seg-exploreとetc-seg-exploitは、探索フェーズではランダムと同様に悪い挙動を示し、その後、利用を開始してから間もなく、累積後悔曲線の急激な平坦化によって示されるように、両者は競争力のあるパフォーマンスに達します。etc-seg-exploitは50ラウンド早く移行します。  
The later strategy also outperforms kl-ucb-seg, which shape suggests slow learning throughout the whole experiment.  
後者の戦略は、全体の実験を通じて遅い学習を示唆する形状のkl-ucb-segをも上回ります。  
Moreover, both ts-lin-pessimistic and ts-lin-naive appear to stabilize to non-flat linear cumulative regret curves after only a few rounds.  
さらに、ts-lin-pessimisticとts-lin-naiveの両方は、わずか数ラウンド後に非平坦な線形累積後悔曲線に安定するようです。  
Pessimistic policies are overall more effective than their naive counterparts, which is due to their lower prior display-to-stream probabilities, that are more realistic.  
悲観的ポリシーは全体的にナイーブな対策よりも効果的であり、これは彼らの低い事前表示からストリームへの確率によるもので、より現実的です。  
Overall, several semi-personalized policies eventually outclassed fully-personalized alternatives, with ts-seg-pessimistic already outperforming them all at the end of the first 25 rounds.  
全体として、いくつかのセミパーソナライズポリシーは最終的に完全にパーソナライズされた代替手段を上回り、ts-seg-pessimisticは最初の25ラウンドの終わりにすでにすべてを上回っています。  
This method manages to effectively exploit information and to quickly rank playlists, which is an interesting result, as fully-personalized contextual models were actually the only ones able to learn the exact display-to-stream probabilities (see generative process in Section 3.2), and as both frameworks have comparable numbers of parameters (K × Q vs K × D).  
この方法は情報を効果的に活用し、プレイリストを迅速にランク付けすることができ、これは興味深い結果です。なぜなら、完全にパーソナライズされたコンテキストモデルは実際には正確な表示からストリームへの確率を学習できる唯一のものであり（セクション3.2の生成プロセスを参照）、両方のフレームワークは比較可能な数のパラメータ（K × Q対K × D）を持っているからです。  
While fully-personalized methods have been the focus of previous works on carousel recommendation [12, 32], our experiments emphasize the empirical benefit of semi-personalization via user clustering that, assuming good underlying clusters, might appear as a suitable alternative for such large-scale real-world applications.  
完全にパーソナライズされた方法は、これまでのカルーセル推薦に関する研究の焦点であったが[12, 32]、私たちの実験は、良好な基盤クラスタを前提としたユーザクラスタリングによるセミパーソナライズの経験的な利点を強調しており、これはそのような大規模な実世界のアプリケーションに適した代替手段として現れるかもしれません。  

_4.1.2_ _Impact of Delayed Batch Feedback. In our experiments, to be consistent with real-world constraints, rewards are not processed on the fly but by batch, at the end of each round._  
_4.1.2_ _遅延バッチフィードバックの影響。私たちの実験では、実世界の制約と一致させるために、報酬はその場で処理されるのではなく、各ラウンドの終わりにバッチで処理されます。_  
We observe that, for semi-personalization, such setting tends to favor stochastic policies, such as the ts-seg or ϵ-greedy-seg ones, w.r.t. deterministic ones such as kl-ucb-seg.  
セミパーソナライズにおいて、このような設定は、kl-ucb-segのような決定論的なものに対して、ts-segやϵ-greedy-segのような確率的ポリシーを好む傾向があることを観察します。  
Indeed, as kl-ucb-seg selects arms in a deterministic fashion, it always proposes the same playlists to all users of a same cluster until the round is over.  
実際、kl-ucb-segは決定論的な方法でアームを選択するため、ラウンドが終了するまで同じクラスタのすべてのユーザに同じプレイリストを提案します。  
On the contrary, stochastic policies propose different playlists sets within a same cluster, ensuring a wider exploration during the round, which might explain why kl-ucb-seg underperforms in our experiments.  
対照的に、確率的ポリシーは同じクラスタ内で異なるプレイリストセットを提案し、ラウンド中により広い探索を確保します。これが、kl-ucb-segが私たちの実験で劣っている理由を説明するかもしれません。  

_4.1.3_ _Cascade vs No-Cascade. All policies from Figure 2 abide by the cascade model introduced in Section 2.4._  
_4.1.3_ _カスケード対ノーカスケード。図2のすべてのポリシーは、セクション2.4で導入されたカスケードモデルに従います。_  
In Figure 3, we report results from follow-up experiments, aiming at measuring the empirical benefit of taking into account this cascading behaviour of users when browsing a sequence of playlists.  
図3では、プレイリストのシーケンスを閲覧する際のユーザのこのカスケード行動を考慮することの経験的な利点を測定することを目的としたフォローアップ実験の結果を報告します。  
We compared policies to alternatives that ignored the cascade display model, and thus returned a 0 reward for all unstreamed playlists at each round, whatever their rank in the carousel.  
カスケード表示モデルを無視した代替手段とポリシーを比較し、そのため、カルーセル内のランクに関係なく、各ラウンドでストリーミングされなかったすべてのプレイリストに対して0の報酬を返しました。  
Only two policy pairs are displayed in Figure 3 for brevity.  
簡潔さのために、図3には2つのポリシーペアのみが表示されています。  
For both of them, the no-cascade variant is outperformed by policies integrating our proposed cascade-based update model from Section 2.4.  
両者において、ノーカスケードバリアントは、セクション2.4で提案したカスケードベースの更新モデルを統合したポリシーに劣ります。  
This result validates the relevance of capturing such phenomenon for our carousel-based personalization problem.  
この結果は、カルーセルベースのパーソナライズ問題においてこの現象を捉えることの重要性を検証します。  

**4.2** **Online Experiments オンライン実験**  
An industrial-scale A/B test has been run in February 2020, to verify whether results from the simulations would hold on the actual Deezer mobile app.  
2020年2月に、シミュレーションの結果が実際のDeezerモバイルアプリで保持されるかどうかを確認するために、産業規模のA/Bテストが実施されました。  
The 12 recommended playlists from each user’s carousel were updated on a daily basis on the app.  
各ユーザのカルーセルからの12の推奨プレイリストは、アプリ上で毎日更新されました。  
Due to industrial constraints, only a subset of policies, from (naive) Thompson Sampling, were tested in production.  
産業上の制約により、（ナイーブな）トンプソンサンプリングからのポリシーのサブセットのみが本番環境でテストされました。  
Also, for confidentiality reasons, we do not report the exact number of users involved in each cohort, nor the precise display-to-stream rates.  
また、機密保持の理由から、各コホートに関与するユーザの正確な数や正確な表示からストリームへの率は報告しません。  
Instead, results are expressed in Figure 4 in terms of relative display-to-stream rates gains w.r.t. random-top-100, an internal baseline that randomly recommends 12 playlists from a subset of 100, pre-selected for each cluster from internal heuristics.  
代わりに、結果は図4において、内部ベースラインであるrandom-top-100に対する相対的な表示からストリームへの率の利得として表現されています。これは、内部のヒューリスティックから各クラスタのために事前に選択された100のサブセットから12のプレイリストをランダムに推薦します。  
Results confirm the superiority of the proposed multi-armed bandit framework for personalization, notably the semi-personalized strategy, and the empirical benefit of integrating a cascade model for arms updates, although users might actually have more complex behaviours on the platform.  
結果は、パーソナライズのために提案されたマルチアームバンディットフレームワークの優位性、特にセミパーソナライズ戦略の優位性、およびアームの更新のためにカスケードモデルを統合することの経験的な利点を確認しますが、ユーザは実際にはプラットフォーム上でより複雑な行動を持つ可能性があります。



## 5 CONCLUSION AND DISCUSSION 結論と議論

In this paper, we modeled carousel personalization as a contextual multi-armed bandit problem with multiple plays.
本論文では、カルーセルのパーソナライズを複数回のプレイを伴う文脈的マルチアームバンディット問題としてモデル化しました。

By addressing a challenging playlist recommendation task, we highlighted the benefits of our framework, notably the
プレイリスト推薦の難しいタスクに取り組むことで、私たちのフレームワークの利点、特にカスケードモデルとユーザクラスタリングによる半パーソナライズの統合を強調しました。

integration of the cascade model and of semi-personalization via user clustering. Along with this paper, we publicly
この論文とともに、私たちはDeezer上のキュレーションされたプレイリストに対するユーザの好みの大規模データセットを公開し、

release a large-scale dataset of user preferences for curated playlists on Deezer, and an open-source environment
比較可能な学習問題を再現するためのオープンソース環境を提供します。

to recreate comparable learning problems. We believe that such release will benefit future research on carousel
私たちは、このようなリリースがカルーセルのパーソナライズに関する今後の研究に貢献すると信じています。

personalization. In particular, we assumed that the number of users and cards was fixed throughout the rounds, which
特に、私たちはラウンド全体でユーザとカードの数が固定されていると仮定しましたが、これは制限であり、

is a limit, that could initiate future studies on the integration of new users or new recommendable content in swipeable
新しいユーザやスワイプ可能なカルーセルにおける新しい推薦可能なコンテンツの統合に関する今後の研究を開始する可能性があります。

carousels. Moreover, our work, as most previous efforts, also assumes that arms/cards distributions are fixed and
さらに、私たちの研究は、ほとんどの以前の努力と同様に、アーム/カードの分布が固定されていると仮定していますが、

independent, which might be unrealistic. A playlist’s relative interest might depend on its neighbors in the carousel,
これは非現実的である可能性があります。プレイリストの相対的な興味はカルーセル内の隣接するプレイリストに依存する可能性があり、

and individually selecting the top-L playlists does not always lead to the best set of L playlists, e.g. in terms of musical
個別にトップLのプレイリストを選択することが、必ずしも音楽の多様性の観点から最良のLのプレイリストのセットにつながるわけではありません。

diversity. Future works in this direction would definitely lead towards the improvement of carousel personalization.
この方向での今後の研究は、カルーセルのパーソナライズの改善につながるでしょう。
