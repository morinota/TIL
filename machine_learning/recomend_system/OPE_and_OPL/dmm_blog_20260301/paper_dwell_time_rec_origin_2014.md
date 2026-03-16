refs: https://www.hongliangjie.com/publications/recsys2014.pdf

Beyond Clicks: Dwell Time for Personalization  
クリックを超えて：パーソナライズのための滞在時間  

### 0.1. Xing Yi Liangjie Hong Erheng Zhong Nathan Nan Liu Suju Rajan  
### 0.2. シン・イー・リャンジー・ホン・エルヘン・ジョン・ナサン・ナン・リウ・スジュ・ラジャン  

{xingyi, liangjie, erheng, nanliu, suju}@yahoo-inc.com  
{xingyi, liangjie, erheng, nanliu, suju}@yahoo-inc.com  

### 0.3. Personalization Sciences, Yahoo Labs, Sunnyvale, CA 94089, USA  
### 0.4. パーソナライズ科学、Yahoo Labs、アメリカ合衆国カリフォルニア州サニーベール94089  


### 0.5. ABSTRACT 要約

Many internet companies, such as Yahoo, Facebook, Google and Twitter, rely on content recommendation systems to deliver the most relevant content items to individual users through personalization. 
Yahoo、Facebook、Google、Twitterなどの多くのインターネット企業は、パーソナライズを通じて個々のユーザーに最も関連性の高いコンテンツアイテムを提供するために、コンテンツ推薦システムに依存しています。
Delivering such personalized user experiences is believed to increase the long term engagement of users. 
そのようなパーソナライズされたユーザー体験を提供することは、ユーザーの長期的なエンゲージメントを高めると考えられています。
While there has been a lot of progress in designing effective personalized recommender systems, by exploiting user interests and historical interaction data through implicit (item click) or explicit (item rating) feedback, directly optimizing for users’ satisfaction with the system remains challenging. 
ユーザーの興味や過去のインタラクションデータを、暗黙的（アイテムクリック）または明示的（アイテム評価）なフィードバックを通じて活用することで、効果的なパーソナライズ推薦システムの設計には多くの進展がありましたが、システムに対するユーザーの満足度を直接最適化することは依然として困難です。
In this paper, we explore the idea of using item-level dwell time as a proxy to quantify how likely a content item is relevant to a particular user. 
本論文では、**アイテムレベルの滞在時間を使用して、特定のユーザーに対してコンテンツアイテムが関連性が高いかどうかを定量化するアイデア**を探ります。
We describe a novel method to compute accurate dwell time based on client-side and server-side logging and demonstrate how to normalize dwell time across different devices and contexts. 
クライアント側およびサーバー側のログに基づいて正確な滞在時間を計算する新しい方法を説明し、異なるデバイスやコンテキスト間で滞在時間を正規化する方法を示します。
In addition, we describe our experiments in incorporating dwell time into state-of-the-art learning to rank techniques and collaborative filtering models that obtain competitive performances in both offline and online settings. 
さらに、オフラインおよびオンラインの両方の設定で競争力のあるパフォーマンスを得るために、**滞在時間を最先端のランキング学習技術や協調フィルタリングモデルに組み込む**実験について説明します。

<!-- ここまで読んだ! -->

**Categories and Subject Descriptors: H.3.5 [Information Storage and Retrieval]: Online Information Services**  
**一般的な用語: 理論、実験**  
**Keywords:** Content Recommendation, Personalization, Dwell Time, Learning to Rank, Collaborative Filtering  
**キーワード:** コンテンツ推薦、パーソナライズ、滞在時間、ランキング学習、協調フィルタリング  

## 1. INTRODUCTION はじめに

Content recommendation systems play a central role in today’s Web ecosystems. 
コンテンツ推薦システムは、今日のウェブエコシステムにおいて中心的な役割を果たしています。 
Companies like Yahoo, Google, Facebook and Twitter are striving to deliver the most relevant content items to individual users. 
Yahoo、Google、Facebook、Twitterなどの企業は、個々のユーザーに最も関連性の高いコンテンツを提供しようと努力しています。 
For example, visitors to these sites are presented with a stream of articles, slideshows and videos that they may be interested in viewing. 
例えば、これらのサイトの訪問者には、興味を持ちそうな記事、スライドショー、動画のストリームが表示されます。 
With a personalized recommendation system, these companies aim to better predict and rank content of interest to users by using historical user interactions on the respective sites. 
パーソナライズされた推薦システムを使用することで、これらの企業は、各サイトでの過去のユーザーインタラクションを利用して、ユーザーの興味に関連するコンテンツをより良く予測し、ランク付けすることを目指しています。 
The underlying belief is that personalization increases long term user engagement and as a side-benefit, also drives up other aspects of the services, for instance, revenue. 
**その根底にある信念は、パーソナライズが長期的なユーザーエンゲージメントを高め、付随的な利益として、サービスの他の側面、例えば収益をも向上させるというものです。** (うんうん...!)
Therefore, there has been a lot of work in designing and improving personalized recommender systems. 
したがって、パーソナライズされたレコメンダーシステムの設計と改善に関する多くの研究が行われています。 

<!-- ここまで読んだ! -->

Traditionally, simplistic user feedback signals, such as click through rate (CTR) on items or user-item ratings, have been used to quantify users’ interest and satisfaction. 
従来、アイテムに対するクリック率（CTR）やユーザー-アイテム評価などの単純なユーザーフィードバック信号が、ユーザーの興味と満足度を定量化するために使用されてきました。 
Based on these readily available signals, most content recommendation systems essentially optimize for CTR or attempt to fill in a sparse user-item rating matrix with missing ratings. 
これらの容易に入手可能な信号に基づいて、**ほとんどのコンテンツ推薦システムは基本的にCTRを最適化するか、欠落した評価を持つまばらなユーザー-アイテム評価行列を埋めることを試みます。** 
Specifically for the latter case, with the success of the Netflix Prize competition, matrix-completion based methods have dominated the field of recommender systems. 
特に後者の場合、Netflix Prizeコンペティションの成功により、行列補完に基づく手法がレコメンダーシステムの分野を支配しています。 
However, in many content recommendation tasks users rarely provide explicit ratings or direct feedback (such as ‘like’ or ‘dislike’) when consuming frequently updated online content. 
しかし、多くのコンテンツ推薦タスクでは、ユーザーは頻繁に更新されるオンラインコンテンツを消費する際に、明示的な評価や直接的なフィードバック（「いいね」や「嫌い」など）を提供することはほとんどありません。
Thus, explicit user ratings are too sparse to be usable as input for matrix factorization approaches. 
したがって、明示的なユーザー評価は、行列分解アプローチの入力として使用するにはあまりにもまばらです。 
On the other hand, item CTR as implicit user interest signal does not capture any post-click user engagement. 
一方、アイテムCTRは暗黙のユーザー興味信号として、クリック後のユーザーエンゲージメントを捉えません。 
For example, users may have clicked on an item by mistake or because of link bait, but are truly not engaged with the content being presented. 
例えば、ユーザーは誤ってアイテムをクリックしたり、リンクベイトのためにクリックしたりすることがありますが、実際には提示されているコンテンツに関与していません。 
Thus, it is arguable that leveraging the noisy click-based user engagement signal for recommendation can achieve the best long term user experience. 
したがって、**ノイズの多いクリックベースのユーザーエンゲージメント信号を推薦に活用することが、最高の長期的なユーザー体験を実現できるとは言い難い**です。
In fact, a recommender system needs to have different strategies to optimize short term metrics like CTR and long term metrics like how many visits a user would pay in several months. 
実際、レコメンダーシステムは、CTRのような短期的な指標と、数ヶ月後にユーザーがどれだけ訪問するかのような長期的な指標を最適化するために異なる戦略を持つ必要があります。 
Thus, it becomes critical to identify signals and metrics that truly capture user satisfaction and optimize these accordingly. 
**したがって、ユーザーの満足度を真に捉える信号と指標を特定し、それに応じて最適化することが重要**になります。 

<!-- ここまで読んだ! -->

We argue that the amount of time that users spend on content items, the dwell time, is an important metric to measure user engagement on content and should be used as a proxy to user satisfaction for recommended content, complementing and/or replacing click based signals. 
私たちは、**ユーザーがコンテンツアイテムに費やす時間、すなわち滞在時間が、コンテンツに対するユーザーエンゲージメントを測定するための重要な指標であり、推薦されたコンテンツのユーザー満足度の代理として使用されるべき**であると主張します。これは、クリックベースの信号を補完または置き換えるものです。
However, utilizing dwell time in a personalized recommender system introduces a number of new research and engineering challenges. 
**しかし、パーソナライズされたレコメンダーシステムで滞在時間を利用することは、多くの新しい研究およびエンジニアリングの課題を引き起こします。** 
For instance, a fundamental question would be how to measure dwell time effectively. 
例えば、基本的な質問は、滞在時間を効果的に測定する方法です。 
Furthermore, different users exhibit different content consumption behaviors even for the same piece of content on the same device. 
さらに、異なるユーザーは、同じデバイス上の同じコンテンツに対しても異なるコンテンツ消費行動を示します。 
In addition, for the same user, depending on the nature of the content item and the context, the user’s content consumption behavior can be significantly different. 
加えて、同じユーザーでも、コンテンツアイテムの性質やコンテキストによって、ユーザーのコンテンツ消費行動は大きく異なる可能性があります。 
Therefore, it would be beneficial to normalize dwell time across different devices and contexts. 
したがって、**異なるデバイスやコンテキストにわたって滞在時間を正規化することが有益**です。(なるほど、モバイルとwebみたいな感じかな...??:thinking:)
Also, recommender systems usually employ machine learning-to-rank (MLR) techniques and collaborative filtering (CF) models, with a wide range of features, to obtain state-of-the-art performance. 
また、レコメンダーシステムは通常、機械学習によるランキング（MLR）技術や協調フィルタリング（CF）モデルを使用し、幅広い特徴を持って最先端のパフォーマンスを得ています。 
Using dwell time in these frameworks is not straight-forward. 
**これらのフレームワークで滞在時間を使用することは簡単ではありません。** 

<!-- ここまで読んだ! -->

In this paper, we use the problem of recommending items for the content feed or stream on the Yahoo’s homepage, shown in Figure 1, as a running example to demonstrate how dwell time can be embedded into a personalized recommendation system. 
本論文では、図1に示すYahooのホームページのコンテンツフィードまたはストリームのアイテムを推薦する問題を、滞在時間をパーソナライズされた推薦システムに組み込む方法を示すための実例として使用します。
We have designed several approaches for accurately computing item-level user content consumption time from large-scale web browsing log data. 
私たちは、大規模なウェブブラウジングログデータからアイテムレベルのユーザーコンテンツ消費時間を正確に計算するためのいくつかのアプローチを設計しました。 
We first use the log data to determine when each item page gains or loses the user attention. 
まず、ログデータを使用して、各アイテムページがユーザーの注意を引くか失うかを判断します。 
Capturing the user’s attention on an item page enables us to compute per-user item-level dwell time. 
アイテムページでのユーザーの注意を捉えることで、ユーザーごとのアイテムレベルの滞在時間を計算することができます。 
In addition, we leverage content consumption dwell time distributions of different content types for normalizing users’ engagement signals, so that we can use this engagement signal for recommending multiple content type items to the user in the content stream. 
さらに、**異なるコンテンツタイプのコンテンツ消費滞在時間分布を活用して、ユーザーのエンゲージメント信号を正規化し、このエンゲージメント信号を使用して、コンテンツストリーム内の複数のコンテンツタイプのアイテムをユーザーに推薦できるように**します。
(そっか、記事 vs 動画とかだと滞在時間の分布はまた変わったりするよね...!:thinking:)
We then incorporate dwell time into machine learning-to-rank (MLR) techniques and collaborative filtering (CF) models. 
次に、滞在時間を機械学習によるランキング（MLR）技術と協調フィルタリング（CF）モデルに組み込みます。 
For MLR, we propose to use per-user item-level dwell time as the learning target, which can be easily considered in all existing MLR models, and demonstrate that it can result in better performances. 
**MLRにおいては、ユーザーごとのアイテムレベルの滞在時間を学習ターゲットとして使用することを提案**し、これはすべての既存のMLRモデルで簡単に考慮でき、より良いパフォーマンスをもたらすことを示します。(あれ? 直接報酬関数を回帰する感じだ...??:thinking:)
For CF, we use dwell time as a form of implicit feedback from users and demonstrate that a state-of-the-art matrix factorization model to incorporate this information can yield competitive and even better performances than the click-optimized counterpart. 
CFにおいては、滞在時間をユーザーからの暗黙のフィードバックの一形態として使用し、この情報を組み込む最先端の行列分解モデルが、クリック最適化されたモデルよりも競争力のある、さらにはそれ以上のパフォーマンスを発揮できることを示します。
To be more specific, we have made the following contributions in this paper: 
より具体的には、本論文では以下の貢献を行いました： 
_• A novel method to compute fine-grained item-level user content consumption time for better understanding users’ interests is proposed._ 
_• ユーザーの興味をよりよく理解するための、細粒度のアイテムレベルのユーザーコンテンツ消費時間を計算する新しい方法を提案します。_ 
_• A novel solution to normalize dwell time for multiple content-type items across different devices is proposed and presented._ 
_• 異なるデバイスにわたる複数のコンテンツタイプのアイテムの滞在時間を正規化する新しい解決策を提案し、提示します。_ 
_• An empirical study of dwell time in the context of content recommendation system is presented in this paper._ 
_• コンテンツ推薦システムの文脈における滞在時間の実証研究を本論文で提示します。_ 
_• A MLR framework to utilize dwell time is proposed and its effectiveness in real-world settings is demonstrated._ 
_• 滞在時間を利用するためのMLRフレームワークを提案し、実世界の設定におけるその有効性を示します。_ 
_• A CF framework to utilize dwell time is proposed and its effectiveness against non-trivial baselines is presented._ 
_• 滞在時間を利用するためのCFフレームワークを提案し、非自明なベースラインに対するその有効性を提示します。_ 

<!-- ここまで読んだ! -->

The paper is organized as follows. 
本論文は以下のように構成されています。 
In §2, we review three related research directions. 
§2では、3つの関連研究の方向性をレビューします。 
In §3, we demonstrate how dwell time can be measured and present some of its interesting characteristics. 
§3では、滞在時間をどのように測定できるかを示し、その興味深い特性のいくつかを提示します。 
In the following sections, we show two important use cases for dwell time. 
次のセクションでは、滞在時間の2つの重要なユースケースを示します。 
In §4, we show how dwell time can be used in MLR to obtain superior performance than the models that optimize CTR. 
§4では、滞在時間がMLRでどのように使用され、CTRを最適化するモデルよりも優れたパフォーマンスを得ることができるかを示します。 
In §5, we plug dwell time into the state-of-the-art CF models and demonstrate that we can obtain competitive performance. 
§5では、滞在時間を最先端のCFモデルに組み込み、競争力のあるパフォーマンスを得られることを示します。 
We conclude the paper in §6. 
§6で本論文を締めくくります。

<!-- ここまで読んだ! -->

## 2. RELATED WORK 関連研究

In this section, we review three related research directions. 
このセクションでは、3つの関連研究の方向性をレビューします。
First, we examine how dwell time is studied and used in web search or IR domains. 
まず、ウェブ検索や情報検索（IR）分野における滞在時間の研究とその利用方法を検討します。
We will carefully analyze which of the existing practices and experiences, on dwell time computation, can be utilized in the context of personalization. 
滞在時間の計算に関する既存の実践や経験の中で、パーソナライズの文脈で利用できるものを慎重に分析します。
We then list several pointers for MLR as it has been extensively studied in the past decade, followed by a brief discussion on CF, paying special attention to how implicit user feedback is used in CF. 
次に、過去10年間にわたって広く研究されてきたMLRに関するいくつかの指針を挙げ、その後、CFに関する簡単な議論を行い、CFにおける暗黙のユーザーフィードバックの使用方法に特に注意を払います。

<!-- ここまで読んだ! -->

### 2.1. Dwell Time in Other Domains: 

A significant amount of previous research on web search has investigated using post-click dwell time of each search result as an indicator of its relevance for web queries and how it can be applied for different web search tasks. 
ウェブ検索に関する以前の研究の多くは、各検索結果のクリック後の滞在時間をウェブクエリに対する関連性の指標として使用することを調査し、さまざまなウェブ検索タスクにどのように適用できるかを検討してきました。
All such previous research focused on examining the dwell time’s utility for improving search results. 
これらの以前の研究はすべて、検索結果を改善するための滞在時間の有用性を検討することに焦点を当てていました。
For instance, White and Kelly [15] demonstrated that using dwell time can potentially help improve the performance of implicit relevance feedback. 
例えば、WhiteとKelly [15]は、滞在時間を使用することで暗黙の関連フィードバックのパフォーマンスを改善できる可能性があることを示しました。
Kim et al. [8] and Xu et al. [17, 18] showed that using webpage-level dwell time can help personalize the ranking of the web search results. 
Kimら [8]やXuら [17, 18]は、ウェブページレベルの滞在時間を使用することで、ウェブ検索結果のランキングをパーソナライズできることを示しました。
Liu et al. [11] investigated the necessity of using different thresholds of dwell time, in order to derive meaningful document relevance information from the dwell time for helping different web search tasks. 
Liuら [11]は、異なるウェブ検索タスクを支援するために、滞在時間から意味のある文書の関連情報を導き出すために、異なる滞在時間の閾値を使用する必要性を調査しました。
To the best of our knowledge, we are the first to use dwell time for personalized content recommendation. 
**私たちの知る限り、私たちはパーソナライズされたコンテンツ推薦のために滞在時間を使用する最初の研究**です。
Furthermore, we consider different types of content (news articles, slideshows and videos), present several approaches to accurately measure content consumption time, and use the dwell time for understanding users’ daily habit and interests. 
さらに、私たちは異なるタイプのコンテンツ（ニュース記事、スライドショー、動画）を考慮し、コンテンツ消費時間を正確に測定するためのいくつかのアプローチを提示し、滞在時間を使用してユーザーの日常の習慣や興味を理解します。
Most recently, Youtube has started to use users’ video time spent instead of the click event [1] to better measure the users’ engagement with video content. 
最近、YouTubeはユーザーの動画視聴時間をクリックイベントの代わりに使用し、ユーザーの動画コンテンツへのエンゲージメントをより良く測定することを始めました。
In contrast, we focus on 
対照的に、私たちは以下に焦点を当てます。

<!-- ここまで読んだ! -->

### 2.2. Learning To Rank in Web Search: 

The field of MLR has significantly matured in the past decade, mainly due to the popularity of search engines. 
**ランク学習の分野は、主に検索エンジンの人気のおかげで**、過去10年間で大幅に成熟しました。
Liu [12] and Li [10] provide an in-depth survey on this topic. 
Liu [12]とLi [10]は、このトピックに関する詳細な調査を提供しています。
Here, we point out that a fundamental issue with all existing MLR models is that they all optimize for relevance, an abstract yet important concept in IR. 
ここで、すべての既存のMLRモデルに共通する根本的な問題は、すべてが関連性という、IRにおいて抽象的でありながら重要な概念を最適化していることです。
In the standard setting, the “relevance” between a particular query and a list of documents is objective and the same for all users. 
標準的な設定では、特定のクエリと文書のリストとの「関連性」は客観的であり、すべてのユーザーに対して同じです。
For IR, “relevance” is judged by human experts through a manual process and is difficult to scale to millions of real queries. 
IRにおいて、「関連性」は人間の専門家によって手動プロセスを通じて判断され、数百万の実際のクエリにスケールするのは困難です。
In order to personalize IR, a natural alternative to “relevance” is to optimize CTR. 
IRをパーソナライズするために、「関連性」の自然な代替手段はCTRを最適化することです。
In this paper, we explore the possibility of optimizing for dwell time under the existing framework of gradient boosted decision trees [6]. 
本論文では、勾配ブースト決定木の既存のフレームワークの下で滞在時間を最適化する可能性を探ります。
However, other MLR models can also be used such as pair-wise models (e.g., RankBoost [5] and AdaRank [16]) and list-wise models (e.g., RankNet [3] and ListNet [4]). 
ただし、RankBoost [5]やAdaRank [16]のようなペアワイズモデルや、RankNet [3]やListNet [4]のようなリストワイズモデルなど、他のMLRモデルも使用できます。
Note that, we do not seek to propose new MLR models, but instead show the advantage of utilizing dwell time in existing models. 
私たちは新しいMLRモデルを提案することを目指しているのではなく、既存のモデルにおける滞在時間の利用の利点を示すことを目指しています。

### 2.3. **Collaborative Filtering: 

In CF systems, users’ satisfaction with the items is usually not considered. 
CFシステムでは、ユーザーのアイテムに対する満足度は通常考慮されません。
Almost all previous work in CF (e.g., [9, 1]) take only explicit feedback such as ratings, or “implicit” click-based feedback into account. 
CFにおけるほとんどの以前の研究（例：[9, 1]）は、評価などの明示的なフィードバックや「暗黙の」クリックベースのフィードバックのみを考慮しています。
Hu et al. [7] considered implicit feedback signal, such as whether a user clicks or reviews an item, and incorporated it into the matrix factorization framework. 
Huら [7]は、ユーザーがアイテムをクリックするかレビューするかといった暗黙のフィードバック信号を考慮し、それを行列因子分解フレームワークに組み込みました。
Rendle et al. [13] proposed a learning algorithm for binary implicit feedback datasets, which is essentially similar to AUC optimization. 
Rendleら [13]は、バイナリの暗黙のフィードバックデータセットに対する学習アルゴリズムを提案しましたが、これは本質的にAUC最適化に類似しています。
None of them went beyond binary implicit feedback to investigate the interactions between users and items. 
彼らのいずれも、バイナリの暗黙のフィードバックを超えて、ユーザーとアイテムの相互作用を調査することはありませんでした。
The approach of Yin et al. [19] is the closest to our work. 
Yinら [19]のアプローチは、私たちの研究に最も近いものです。
In that paper, the authors used a graphical model on the explicit feedback signals and dwell time data to predict the user’s score. 
その論文では、著者は明示的なフィードバック信号と滞在時間データにグラフィカルモデルを使用して、ユーザーのスコアを予測しました。
Our work is different in that our model does not require the presence of explicit user feedback.  
私たちの研究は、私たちのモデルが明示的なユーザーフィードバックの存在を必要としない点で異なります。

<!-- ここまで読んだ! -->

![]()
**Table 1: Client-side Logging Example**
**表1：クライアントサイドのログ例**

- メモ: テーブル1の内容
  - ユーザ行動, クライアントサイドイベント
  - 「ユーザーがニュース記事のページを開く」, {DOM-ready, t_1}
  - 「彼は数秒間記事を読む」, {Focus, t_2}
  - 「彼は他の記事を読むために別のブラウザのタブまたはウィンドウに切り替える」, {Blur, t_3}
  - 「彼は記事ページに戻り、コメントをする」, {Focus, t_4}
  - 「彼は記事ページを閉じるか、戻るボタンをクリックして別のページに移動する」, {BeforeUnload, t_5}

<!-- 
**Table 2: Comparison of dwell time measurement. The first two** 
**表2：滞在時間測定の比較。最初の2つの列はLE、中央の2つの列はFB、最後の2つの列はクライアントサイドのログに関するものです。**

**columns are for LE, the middle two columns are for FB and** 
**列はLE用、中央の2つの列はFB用、最後の2つの列はクライアントサイドのログ用です。**

**the last two columns are for client-side logs. Each row contains** 
**各行には1日のデータが含まれています。**

**data from a day.** 
**#** **DT. (LE)** **#** **DT. (FB)** **#** **DT. (C)**

**#** **DT. (LE)** **#** **DT. (FB)** **#** **DT. (C)**

3, 322 86.5 3, 197 134.4 3, 410 130.3 
3, 322 86.5 3, 197 134.4 3, 410 130.3

5, 711 85.4 5, 392 132.6 5, 829 124.0 
5, 711 85.4 5, 392 132.6 5, 829 124.0

|86.5|3, 197|134.4|3, 410| 
|---|---|---|---|  
G [G G ]G  
G G G G G G G  
G  
G G G G G G G G G G  
G G G G G G G G G G G  
 -->

<!-- ここまで読んだ! -->

## 3. MEASURING ITEM DWELL TIME アイテム滞在時間の測定

In this section, we describe how dwell time can be measured from web logs and show its basic characteristics. 
このセクションでは、ウェブログから滞在時間をどのように測定できるかを説明し、その基本的な特性を示します。

### 3.1. 滞在時間の計算

Accurately computing item-level dwell time from web-scale user browsing activity data is a challenging problem. 
**ウェブスケールのユーザーブラウジング活動データからアイテムレベルの滞在時間を正確に計算することは、難しい問題**です。 
As an example, most modern browsers have a multi-tabbed interface in which users can open multiple stories simultaneously and switch between them. 
例えば、ほとんどの現代のブラウザはマルチタブインターフェースを持っており、ユーザーは複数のストーリーを同時に開いてそれらの間を切り替えることができます。 
In the multi-tabbed setting, figuring out the tab that captured the user’s attention is non-trivial. 
マルチタブの設定では、ユーザーの注意を引いたタブを特定することは簡単ではありません。 
In this paper we describe two complementary methods to derive dwell time, one via client-side logging and the other via server-side logging. 
本論文では、滞在時間を導出するための2つの補完的な方法を説明します。一つはクライアントサイドのログを通じて、もう一つはサーバーサイドのログを通じてです。 
We have also conducted a simple study comparing these two approaches. 
また、これら2つのアプローチを比較する簡単な研究も行いました。 
Although client-side logging can capture fine-grained user behavior and has the potential of being highly useful, there is a lot of dependency on browser implementation and potential for large amounts of data loss. 
クライアントサイドのログは詳細なユーザー行動をキャプチャでき、高い有用性を持つ可能性がありますが、ブラウザの実装に依存する部分が多く、大量のデータ損失の可能性があります。 
Therefore, when the client-side data is not available, we resort to reasonable approximation methods through server-side logging. 
したがって、クライアントサイドのデータが利用できない場合、サーバーサイドのログを通じて合理的な近似方法に頼ります。 
Thus, we can reliably compute dwell time in a real world setting. 
これにより、実世界の設定で信頼性の高い滞在時間を計算できます。 

<!-- ここまで読んだ! -->

**Client-Side** **Dwell** **Time:** Client-side logging utilizes Javascript/DOM events to record how users interact with the content story pages. 
**クライアントサイドの滞在時間:** クライアントサイドのログは、ユーザーがコンテンツストーリーページとどのように相互作用するかを記録するためにJavascript/DOMイベントを利用します。 
Let us imagine the scenario demonstrated in Table 1 where the left column is a sequence of user interactions with a news article and the right column contains the corresponding client-side events, in the form of {event name, time stamp} tuples. 
表1に示されているシナリオを想像してみましょう。左の列はニュース記事に対するユーザーの相互作用のシーケンスで、右の列には対応するクライアントサイドのイベントが{イベント名、タイムスタンプ}のタプルの形で含まれています。 
In these events, DOM-ready indicates the ready-time of the body of the page, which can be considered as the start of the dwell time. 
これらのイベントでは、DOM-readyはページのボディの準備完了時間を示し、滞在時間の開始と見なすことができます。 
Focus indicates that the user’s focus was back on the body of the news article. 
Focusは、ユーザーの焦点がニュース記事のボディに戻ったことを示します。 
Blur means that the article body lost the user attention. 
Blurは、記事のボディがユーザーの注意を失ったことを意味します。 
BeforeUnload is the time point immediately prior to the page being unloaded. 
BeforeUnloadは、ページがアンロードされる直前の時間点です。 
Based on these events, we can compute dwell time on the client-side by simply accumulating time differences between Focus event and Blur events. 
これらのイベントに基づいて、FocusイベントとBlurイベントの間の時間差を単純に累積することで、クライアントサイドでの滞在時間を計算できます。 
From the above example, we have the dwell time as: (t3 − _t2) + (t5 −_ _t4). 
上記の例から、滞在時間は次のようになります: $(t3 − t2) + (t5 − t4)$。 
We can clearly see that client-side approach can accurately capture users’ actual attention even in multi-tabbed modern browsers. 
クライアントサイドのアプローチは、マルチタブの現代のブラウザでもユーザーの実際の注意を正確にキャプチャできることが明らかです。 
The major drawback of client-side logging is that it relies on the correctness of Javascript execution and on servers successfully receiving and logging client-sent data. 
クライアントサイドのログの主な欠点は、Javascriptの実行の正確性と、サーバーがクライアントから送信されたデータを正常に受信し、ログに記録することに依存していることです。 
Data loss in this client-server interaction can be very high, for example, because of loss in internet connection. 
このクライアント-サーバー間の相互作用におけるデータ損失は非常に高くなる可能性があります。例えば、インターネット接続の喪失によるものです。 
In addition, users may also disable Javascript in their browsers. 
さらに、ユーザーはブラウザでJavascriptを無効にすることもあります。 

<!-- ここまで読んだ! -->

**Server-Side Dwell Time:** When client-side logs are not available, we resort to server-side logging to infer users’ attention on item pages. 
**サーバーサイドの滞在時間:** クライアントサイドのログが利用できない場合、アイテムページに対するユーザーの注意を推測するためにサーバーサイドのログに頼ります。 
The computation of dwell time on server-side are built on a number of heuristics. 
サーバーサイドでの滞在時間の計算は、いくつかのヒューリスティックに基づいています。 
One approach is to simulate client-side user attention events by identifying pseudo Focus and Blur events from server logs. 
一つのアプローチは、サーバーログから擬似FocusおよびBlurイベントを特定することによって、クライアントサイドのユーザー注意イベントをシミュレートすることです。 
Consider the following sequence of logging events: 
次のログイベントのシーケンスを考えてみましょう: 

$_{i, Click, t1} →{j, Click, t2} →{k, Click, t3}$

where each events is a tuple of item ID, event type and time stamp.
ここで、各イベントはアイテムID、イベントタイプ、タイムスタンプのタプルです。 
The dwell time for i and j can be computed as $t2 − t1$ and $t3 − t2$ respectively. 
アイテムiとjの滞在時間はそれぞれ$t2 − t1$および$t3 − t2$として計算できます。 
A more complicated example is: 
より複雑な例は次の通りです: 

$_{i, Click, t1} →{j, Click, t2} →{k, Click, t3} →_{i, Comment, t4} →{n, Click, t5}$  

where the dwell time for page $i$ can be computed as $(t_2 − t1) + (t5 − t4)$.
ここで、ページ$i$の滞在時間は$(t_2 − t1) + (t5 − t4)$として計算できます。
We denote this as FB (Focus/Blur) method. 
この方法をFB（Focus/Blur）法と呼びます。
Another simpler heuristic is called LE (Last Event) method, which is to take the last event of the page as the end-page event and compute the interval of the first-event timestamp and the last one. From the example above, the dwell time of page i by LE would be t4 − t1. 
別のより単純なヒューリスティックは、LE（Last Event）法と呼ばれ、ページの最後のイベントを終了ページイベントとして取り、最初のイベントのタイムスタンプと最後のイベントのタイムスタンプの間隔を計算することです。上記の例から、LEによるページiの滞在時間はt4 − t1になります。
Both approximation methods have their own weaknesses: 1) The FB approach can over-estimate the dwell time because servers do not know the exact time the target story page loses its user attention.
両方の近似方法にはそれぞれ弱点があります: 1) FBアプローチは、サーバーがターゲットストーリーページがユーザーの注意を失う正確な時間を知らないため、滞在時間を過大評価する可能性があります。
For the above example, if the last click happens on some other page, (t5 − t4) interval could includes some user time spent outside the target page. The FB approach might also under-estimate the dwell time because servers also do not accurately know the time the target page gains user attention. 
上記の例では、最後のクリックが他のページで発生した場合、(t5 − t4)の間隔にはターゲットページ外でのユーザーの時間が含まれる可能性があります。FBアプローチは、サーバーもターゲットページがユーザーの注意を引く時間を正確に知らないため、滞在時間を過小評価する可能性もあります。
For the above example, if users have returned to the target page and read it for some additional time before commenting at t4, the dwell time computation will not include the additional time. 
上記の例では、ユーザーがターゲットページに戻り、t4でコメントする前に追加の時間を読んでいた場合、滞在時間の計算にはその追加の時間が含まれません。 
The LE approach does not consider the scenario in which the users’ reading focus could switch among multiple browser page tabs, thus over-estimating the dwell time. 
LEアプローチは、ユーザーの読書の焦点が複数のブラウザページタブの間で切り替わるシナリオを考慮していないため、滞在時間を過大評価します。 
On the other hand, because the LE approach conservatively uses the last event on the target page to compute dwell time and servers do not know when the user abandons or closes the page (without the client-side unload event), it can also under-estimate the dwell time. 
一方、LEアプローチはターゲットページの最後のイベントを保守的に使用して滞在時間を計算し、サーバーはユーザーがページを放棄または閉じる時期を知らないため（クライアントサイドのアンロードイベントなしで）、滞在時間を過小評価する可能性もあります。 

<!-- ここまで読んだ! -->

Because both approaches could over-estimate or under-estimate the item-level dwell time, we conducted a simple comparison study among FB, LE and the client-side logging. 
両方のアプローチがアイテムレベルの滞在時間を過大評価または過小評価する可能性があるため、FB、LE、およびクライアントサイドのログの間で簡単な比較研究を行いました。 
The results are shown in Table 2. 
結果は表2に示されています。 
The purpose of this study is to explore which server-side approach can be used to better approximate the client-side logging. 
この研究の目的は、どのサーバーサイドアプローチがクライアントサイドのログをより良く近似できるかを探ることです。 
We use two days’ server-side logging events and client-side logging events for article pages, and compute the average dwell time by each method. 
記事ページのために2日間のサーバーサイドログイベントとクライアントサイドログイベントを使用し、各方法によって平均滞在時間を計算します。 
Note that even for the same time period, different approaches use different sets of events to compute dwell time (see above example) and client-side events can be lost. 
同じ期間であっても、異なるアプローチは滞在時間を計算するために異なるイベントセットを使用し（上記の例を参照）、クライアントサイドのイベントが失われる可能性があります。 
Thus, the total number of articles considered varies (the first, the third and the fifth column). 
したがって、考慮される記事の総数は異なります（最初の列、3番目の列、5番目の列）。 
From the table, we can see that the average dwell time computed by the FB approach is very close to the client-side logging. 
表から、FBアプローチによって計算された平均滞在時間がクライアントサイドのログに非常に近いことがわかります。 
Meantime, the LE approach greatly under-estimates the dwell time, compared with the client-side events. 
一方、LEアプローチはクライアントサイドのイベントと比較して滞在時間を大幅に過小評価しています。 
This result shows: through simulating users’ reading attention switch events from server-side, the FB approach better handles item-level dwell time computation in multi-tabbed modern browser setting. 
この結果は、サーバーサイドからユーザーの読書注意の切り替えイベントをシミュレートすることによって、FBアプローチがマルチタブの現代のブラウザ設定におけるアイテムレベルの滞在時間計算をより適切に処理することを示しています。
Therefore, we now use FB as a relative reliable fall-back proxy to measure the item-level dwell time from server-side logging events when client-side logging is not available. 
したがって、クライアントサイドのログが利用できない場合、FBを相対的に信頼できるフォールバックプロキシとして使用して、サーバーサイドのログイベントからアイテムレベルの滞在時間を測定します。

<!-- ここまで雑に読んだ! 滞在時間の計算方法は一旦困ってないので!-->

### 3.2. 3.2 Dwell Time Analysis 滞在時間分析

![]()
図2

In order to understand the nature of it, we analyze per-item peruser dwell time from a large real-world data collection from Yahoo.
**その性質を理解するために、私たちはYahooからの大規模な実世界データコレクションから、アイテムごとのユーザごとの滞在時間を分析**します。
We plot the unnormalized distribution of log of dwell time in Figure 2. 
滞在時間の対数の非正規化分布を図2にプロットします。
The data used for this figure is from one month’s Yahoo homepage sample traffic. 
この図に使用されるデータは、1か月間のYahooホームページのサンプルトラフィックからのものです。
It is obvious that the log of dwell time follows a bell-curve. 
**滞在時間の対数がベルカーブに従うことは明らか**です。
Many would guess the distribution of log of dwell time is a Gaussian distribution. 
多くの人は、滞在時間の対数の分布がガウス分布であると推測するでしょう。
However, Q-Q plot and also Shapiro–Wilk test [14] reject such an assertion. 
しかし、Q-QプロットとShapiro–Wilk検定[14]はそのような主張を否定します。
A further study of its formal distribution is in future work. 
その正式な分布に関するさらなる研究は今後の作業です。
Regardless of its normality, we observe that the bell-curve pattern holds for different time periods and different types of devices (see Figure 5 and 6, which we will discuss later).
その正規性に関係なく、異なる時間帯や異なる種類のデバイスに対してベルカーブパターンが保持されることを観察します（後で議論する図5と6を参照）。

<!-- ここまで読んだ! -->

Since dwell time approximates the time users spend on an item, it is natural to assume that given the same content quality, a longer news article would attract longer average dwell time across all users.
滞在時間はユーザがアイテムに費やす時間を近似するため、同じコンテンツ品質が与えられた場合、長いニュース記事はすべてのユーザに対してより長い平均滞在時間を引き付けると仮定するのは自然です。
In order to demonstrate this behavior, we investigate this issue on text heavy news article [3], and plot a scatter-plot of average dwell time per article versus article length in Figure 3 where X-axis is the length of article and the Y-axis is the average dwell time of that particular article from all users.
この挙動を示すために、テキストが多いニュース記事[3]に関してこの問題を調査し、図3において、記事ごとの平均滞在時間と記事の長さの散布図をプロットします。ここで、X軸は記事の長さ、Y軸はすべてのユーザからの特定の記事の平均滞在時間です。
In order to show things clearly, the dwell times and article lengths are binned into smaller buckets where each point represents a bucket.
物事を明確に示すために、滞在時間と記事の長さは小さなバケットに分けられ、各点はバケットを表します。
We show the scatterplot of the dwell time against the length of the article on different devices, namely desktop, tablet and mobile devices.
**デスクトップ、タブレット、モバイルデバイスなど、異なるデバイスにおける記事の長さに対する滞在時間の散布図**を示します。
The black line is a fitted linear line for a particular device type with the 0.95 confidence interval in the grey area.
黒い線は特定のデバイスタイプに対するフィッティングされた線形線で、灰色の領域は0.95の信頼区間を示しています。
From the figure, it is very clear that the length of the article has good linear correlation with the average dwell time across devices.
図から、**記事の長さがデバイス全体での平均滞在時間と良好な線形相関を持つことが非常に明らか**です。
Also, matching our intuition, the average dwell time on desktop is longer for long articles and the reading behavior on tablet and mobile devices are similar.
また、**私たちの直感に合致して、デスクトップでの長い記事の平均滞在時間は長く、タブレットとモバイルデバイスでの読書行動は似ています。**
Furthermore, the correlation becomes weaker when articles are very long: for desktop when the article is longer than 1,000 words, the plot has big variance; this indicates that users may have run out of their time-budget to consume the complete long story.
さらに、**記事が非常に長い場合、相関は弱くなります。デスクトップの場合、記事が1,000語を超えると、プロットには大きな分散が見られます。これは、ユーザが完全な長いストーリーを消費するための時間予算を使い果たしている可能性があることを示しています。**
Although the high correlation between the length of articles and average dwell time naturally leads to using the length of articles as a feature to predict average dwell time, we point out based on the observed data: 
記事の長さと平均滞在時間の間の高い相関は、自然に記事の長さを平均滞在時間を予測するための特徴として使用することにつながりますが、観察されたデータに基づいて以下の点を指摘します：
(1) per-user dwell time (rather than binned average dwell time over all users) has little correlation with the article length; 
(1) ユーザごとの滞在時間（すべてのユーザのバケット化された平均滞在時間ではなく）は、記事の長さとの相関がほとんどありません。
and (2) long dwell time may not necessarily reflect that users are really interested in the article.
(2) 長い滞在時間は、ユーザが本当にその記事に興味を持っていることを必ずしも反映しているわけではありません。
In other words, content length alone can hardly explain the per-user per-item dwell time, and we need to be careful of the bias of dwell time based user engagement measurements towards long length content stories.
言い換えれば、**コンテンツの長さだけでは、ユーザごとのアイテムごとの滞在時間を説明することはほとんどできず**、**長いコンテンツストーリーに対する滞在時間ベースのユーザーエンゲージメント測定のバイアスに注意する必要があります**。
(We will revisit this issue in §3.4.)
（この問題については§3.4で再検討します。）

<!-- ここまで読んだ! -->

For slideshows, a natural assumption would be that the larger the number of photos/slides, the longer the average dwell time these items would receive over all users. 
**スライドショーに関しては、写真やスライドの数が多いほど、すべてのユーザーに対する平均滞在時間が長くなるという自然な仮定**があります。 
We demonstrate the relationships between the number of photos and the average dwell time on slideshows in Figure 4. 
私たちは、図4において、写真の数とスライドショーの平均滞在時間との関係を示します。 
Again, we binned the number of photos and the average dwell time. 
再度、写真の数と平均滞在時間をビン分けしました。 
It is clear that the correlation is not as strong as the length of articles. 
記事の長さほど相関が強くないことは明らかです。 
For videos, we also observe the similar weak correlations between the duration of a video clips’ and it’s average dwell time. 
動画に関しても、動画クリップの長さとその平均滞在時間との間に似たような弱い相関が見られます。

<!-- ここまで読んだ! -->

### 3.3. Normalized Dwell Time 正規化滞在時間

As may be obvious, users’ consumption of content items varies by context. 
明らかに、ユーザーのコンテンツアイテムの消費は文脈によって異なります。 
For example, in historical data, we found that users have on average less dwell time per article on mobile or tablet devices than on desktops. 
例えば、**過去のデータでは、ユーザーはデスクトップよりもモバイルやタブレットデバイスでの記事あたりの滞在時間が平均して短い**ことがわかりました。 
Also, users on average spend less time per slideshow than per article. 
また、ユーザーは平均してスライドショーあたりの時間を記事あたりよりも少なく費やします。 
Indeed, different content types, by their nature, would result in different browsing behaviors; thus we would expect different dwell times among these content types. 
実際、異なるコンテンツタイプはその性質上、異なるブラウジング行動を引き起こすため、これらのコンテンツタイプ間で異なる滞在時間が期待されます。 
In order to extract comparable user engagement signals, we introduce the normalized user dwell time to handle users’ different content consumption behaviors on different devices for personalization. 
**比較可能なユーザーエンゲージメント信号を抽出するために、異なるデバイスでのユーザーの異なるコンテンツ消費行動を扱うために正規化ユーザー滞在時間を導入**します。 
The technique discussed here can also be used to blend multiple content sources (e.g., slide-shows and articles) into a unified stream. 
**ここで議論されている技術は、複数のコンテンツソース（例：スライドショーや記事）を統一されたストリームに統合するためにも使用**できます。 

<!-- ここまで読んだ! -->

![]()
figure5

![]()
figure6

Although the distributions of users’ per-item dwell time (from all users) for each content type is different, we found that each content type’s distribution remains similar over a long time period. 
**各コンテンツタイプに対するユーザーのアイテムごとの滞在時間の分布（すべてのユーザーから）は異なりますが、各コンテンツタイプの分布は長期間にわたって類似している**ことがわかりました。
To demonstrate this observation, we further plot the log of dwell time of two important types of content: slideshows and videos in Figure 5 and Figure 6, respectively. 
この観察を示すために、スライドショーとビデオという2つの重要なコンテンツタイプの滞在時間の対数をそれぞれ図5と図6にプロットします。 
Similar to the article case, we do not report the absolute values for both types. 
記事の場合と同様に、両方のタイプの絶対値は報告しません。 
However, the patterns are again obvious. 
しかし、パターンは再び明らかです。 
In all these cases, the log of dwell time has Gaussian-like distributions. 
**これらすべてのケースにおいて、滞在時間の対数はガウス分布のような分布を持っています。**
Indeed, most of the dwell time distributions for each different content-type on different device platforms all surprisingly share the similar pattern. 
実際、異なるデバイスプラットフォーム上の各異なるコンテンツタイプの滞在時間分布は驚くべきことにすべて類似のパターンを共有しています。 
The same conclusion holds for different lengths of the time period. 
異なる期間の長さに対しても同じ結論が成り立ちます。 
Also, we can easily see that the peak of log of dwell time is highest for videos, followed by articles and slideshows, which matches our intuitive understanding of these three types of content items. 
また、滞在時間の対数のピークはビデオが最も高く、次に記事、スライドショーの順であり、これはこれら3つのコンテンツアイテムの直感的な理解と一致します。 

<!-- ここまで読んだ! -->

Thus, the basic idea is, for each consumed item, we would like to extract its dwell time based user engagement level such that it is comparable across different context (e.g. content types, devices, instrumentations, etc.). 
したがって、基本的なアイデアは、消費された各アイテムについて、その滞在時間に基づくユーザーエンゲージメントレベルを抽出し、異なる文脈（例：コンテンツタイプ、デバイス、計測など）で比較可能にすることです。 
We do this by normalizing out the variance of the dwell time due to differences in context. 
これは、文脈の違いによる滞在時間の分散を正規化することによって行います。 
In particular, we adopt the following procedure to normalize dwell time into a comparable space: 
特に、滞在時間を比較可能な空間に正規化するために、以下の手順を採用します： 

1. For each content consumption context C, collect the historical per-item time spent data and compute the mean µC and standard deviation σC, both in log space. 
   1. 各コンテンツ消費文脈Cについて、アイテムごとの過去の時間データを収集し、平均µCと標準偏差σCを対数空間で計算します。 

2. Given a new content item i’s time spent tI in its context Ci, compute the z-value in log space: zi = log(tσiCi)−µCi . 
   1. 新しいコンテンツアイテムiの文脈Ciにおける時間tIを考慮し、対数空間でz値を計算します：$z_i = \log(t_{i}^{\sigma}C_i) - \mu_{C_i}$。 

3. Compute the normalized dwell time of item i in the article space: ti,article = exp(µarticle + σarticle × zi). 
   1. アイテムiの正規化滞在時間を記事空間で計算します：$t_{i,\text{article}} = \exp(\mu_{\text{article}} + \sigma_{\text{article}} \times z_i)$。 

In other words, all other types of items are now “comparable” after this transformation, and the normalized user engagement signals are then used for training recommendation models to handle different content types and can be deployed in different contexts. 
**言い換えれば、この変換の後、他のすべてのタイプのアイテムは「比較可能」になり**、正規化されたユーザーエンゲージメント信号は異なるコンテンツタイプを扱うための推薦モデルのトレーニングに使用され、異なる文脈で展開できます。

<!-- ここまで読んだ! -->

### 3.4. Predicting Dwell Time 滞在時間の予測

The average dwell time of a content item can be viewed as one of the item’s inherent characteristic, which provides important average user engagement information on how much time the user will spend on this item. 
**コンテンツアイテムの平均滞在時間は、そのアイテムの固有の特性の一つと見なすことができ、ユーザーがそのアイテムにどれだけの時間を費やすかに関する重要な平均ユーザーエンゲージメント情報を提供**します。(うんうん。めちゃめちゃ重要な情報なんだよね...!!:thin k)
Predicting average dwell time for each content item can help labeling items when their dwell time are not available/missing. 
各コンテンツアイテムの平均滞在時間を予測することは、滞在時間が利用できない/欠落している場合にアイテムにラベルを付けるのに役立ちます
For example, content items that have never been shown to users (such as new items) will not have available dwell time. 
例えば、ユーザーに一度も表示されたことのないコンテンツアイテム（新しいアイテムなど）は、利用可能な滞在時間を持ちません。
As another example, a user’s dwell time on her clicked story may not be always be computed because there may be no subsequent server-side events from the same user. 
別の例として、ユーザーがクリックしたストーリーに対する滞在時間は、同じユーザーからのその後のサーバーサイドイベントがないために常に計算されるわけではありません。
Therefore, leveraging predicted average dwell time can greatly improve the “coverage” (or alleviate the missing data issue). 
**したがって、予測された平均滞在時間を活用することで、「カバレッジ」を大幅に改善できる（または欠損データの問題を軽減できる）可能性**があります。
Not handling these situations, could degrade the effectiveness of applying dwell time in personalization applications. 
これらの状況に対処しないと、パーソナライズアプリケーションにおける滞在時間の適用の効果が低下する可能性があります。
In this sub-section, we present a machine learning method to predict dwell time of article stories using simple features. 
この小節では、**シンプルな特徴を使用して記事のストーリーの滞在時間を予測するための機械学習手法**を紹介します。

<!-- ここまで読んだ! -->

The features we consider are topical category of the article and the context in which the article would be shown (e.g., desktop, tablet or mobile). 
**私たちが考慮する特徴は、記事のトピカルカテゴリと、記事が表示されるコンテキスト（例：デスクトップ、タブレット、またはモバイル）**です。
We use Support Vector Regression (SVR) models to predict dwell time. 
滞在時間を予測するために、サポートベクタ回帰（SVR）モデルを使用します。
The model is trained from a sample of user-article interaction data. 
モデルは、ユーザーと記事のインタラクションデータのサンプルからトレーニングされます。
We show the features and their corresponding weights in Table 3. 
特徴とそれに対応する重みを表3に示します。
Most features are categorical and we use log(Dwell Time) as the model response. 
ほとんどの特徴はカテゴリカルであり、モデルの応答としてlog(Dwell Time)を使用します。
We can loosely interpret the weights of these features as how much that feature contributes to the article’s average dwell time prediction. 
これらの特徴の重みは、記事の平均滞在時間予測にその特徴がどれだけ寄与するかを大まかに解釈できます。
The feature weights match our current expectation for average users’ article reading behavior: longer articles can lead to higher predicted average dwell time; 
**特徴の重みは、平均的なユーザーの記事読書行動に対する現在の期待と一致**しています：長い記事は、より高い予測平均滞在時間につながる可能性があります。
people spend a longer time reading articles on desktop devices than mobile devices; more serious topics can lead users to dwell longer. 
ユーザーはモバイルデバイスよりもデスクトップデバイスで記事を読むのに長い時間を費やします。より深刻なトピックはユーザーがより長く滞在することにつながる可能性があります。
Potentially, the predicted average dwell time could be leveraged to normalize the dwell time-based user engagement signal (as discussed in §3.3); 
予測された平均滞在時間は、滞在時間に基づくユーザーエンゲージメント信号を正規化するために活用できる可能性があります（§3.3で議論したように）。
however, this is non-trivial as the interplay between the dwell time features and users’ experience is not obvious. 
ただし、これは非自明であり、滞在時間の特徴とユーザーの体験との相互作用は明らかではありません。
For example, will recommending more serious topics that have long average dwell lead to better or worse user experience? 
**例えば、平均滞在時間が長いより深刻なトピックを推奨することは、より良いユーザー体験につながるのでしょうか、それとも悪化させるのでしょうか？**
We will leave answering this question for future work. 
この質問への回答は今後の研究に委ねます。

<!-- ここまで読んだ! -->

## 4. USE CASE I: LEARNING TO RANK　使用例 I: ランキング学習

In this section, we investigate how to leverage item-level dwell time to train machine-learned ranking (MLR) models for content recommendation.
このセクションでは、アイテムレベルの滞在時間を活用して、コンテンツ推薦のための機械学習ランキング（MLR）モデルをトレーニングする方法を調査します。

<!-- ここまで読んだ! -->

**The Basic MLR Setting: In traditional MLR, a query q is repre-**
基本的なMLR設定: 従来のMLRでは、クエリ$q$は特徴ベクトル$q$として表現され、文書$d$は特徴ベクトル$d$として表現されます。
represented as a feature vector q while a document d is represented as a feature vector d. A function g takes these two feature vectors and outputs a feature vector $x_{q,d} = g(q, d)$ for this query-document pair $(q, d)$. 
関数$g$はこれら2つの特徴ベクトルを受け取り、このクエリ-文書ペア$(q, d)$に対して特徴ベクトル$x_{q,d} = g(q, d)$を出力します。 
Note that g could be as simple as a concatenation. 
$g$は単純な連結である可能性もあります。 
Each query-document pair has a response $y_{q,d}$, in traditional IR, which is usually the relevance judgment. 
各クエリ-文書ペアには、従来の情報検索（IR）において通常は関連性判断である応答$y_{q,d}$があります。 
Typically this judgment is common to all users, that is, there is no user-specific personalization.
通常、この判断はすべてのユーザーに共通であり、ユーザー特有のパーソナライズはありません。
Depending on the particular paradigm (e.g., point-wise, pair-wise or list-wise), a machine learned model imposes a loss function $l$ which takes one or all documents belonging to a query $q$ as the input, approximating the individual relevance judgment, pair-wise relevance preferences or the whole list ordering. 
特定のパラダイム（例: ポイントワイズ、ペアワイズ、リストワイズ）に応じて、機械学習モデルは損失関数$l$を課し、クエリ$q$に属する1つまたはすべての文書を入力として受け取り、個々の関連性判断、ペアワイズの関連性の好み、または全体のリスト順序を近似します。 
In the context of content recommendation, we can simply borrow the idea of MLR by treating user interests as queries and articles (or other types of items) as documents. 
コンテンツ推薦の文脈では、ユーザーの興味をクエリとして扱い、記事（または他のタイプのアイテム）を文書として扱うことで、MLRのアイデアを単純に借用できます。 
Although this formulation looks promising, there are two challenges. 
この定式化は有望に見えますが、2つの課題があります。 
One is how to construct a feature vector for queries (users) and the second is how to utilize user activities to infer relevancy between users and documents. 
1つは、クエリ（ユーザー）のための特徴ベクトルをどのように構築するか、もう1つは、ユーザーの活動をどのように利用してユーザーと文書の関連性を推測するかです。 
The discussion of the first question is out of this paper’s scope. 
最初の質問の議論は本論文の範囲外です。 
Here, we focus on the second question. 
ここでは、2つ目の質問に焦点を当てます。 
While the definition of relevance judgments might be unambiguous in IR, it is not straightforward in the context of content personalization. 
関連性判断の定義はIRでは明確かもしれませんが、コンテンツパーソナライズの文脈では簡単ではありません。 
One cheap and easy approach is to use users’ click-through data as relevance judgments. 
**安価で簡単なアプローチの1つは、ユーザーのクリックデータを関連性判断として使用すること**です。 
Essentially, in such case, we use $y_{d,u} = \{0, 1\}$, a binary variable, to indicate whether an article $d$ (the “document” in IR setting) is clicked by the user $u$ (the “query” in IR setting). 
本質的に、その場合、記事$d$（IR設定における「文書」）がユーザー$u$（IR設定における「クエリ」）によってクリックされたかどうかを示すために、バイナリ変数$y_{d,u} = \{0, 1\}$を使用します。 
Under this formalism, a MLR model indeed optimizes (CTR). 
この形式の下で、MLRモデルは確かに（CTR）を最適化します。

<!-- ここまで読んだ! -->

In this paper, we use the Gradient Boosted Decision Tree (GBDT) algorithm [6] to learn the ranking functions. 
本論文では、ランキング関数を学習するために勾配ブースティング決定木（GBDT）アルゴリズム[6]を使用します。 
GBDT is an additive regression algorithm consisting of an ensemble of trees, fitted to current residuals, gradients of the loss function, in a forward stepwise manner. 
GBDTは、現在の残差、損失関数の勾配に適合した木のアンサンブルからなる加法回帰アルゴリズムです。 
It iteratively fits an additive model as: 
それは反復的に加法モデルを次のように適合させます：

$$
f_t(x) = T_t(x; \Theta) + \lambda \sum_{t=1}^{T} \beta_t T_t(x; \Theta_t)
$$

where $w_i$ is the weight for data instance $i$, which is usually set to 1, and $G_{it}$ is the gradient over the current prediction function: $G_{it} = \left[ \frac{\partial L}{\partial f_{y_i}(f_{x_i})} \right]_{f = f_{t-1}}$. 
ここで、$w_i$はデータインスタンス$i$の重みで、通常は1に設定され、$G_{it}$は現在の予測関数に対する勾配です：$G_{it} = \left[ \frac{\partial L}{\partial f_{y_i}(f_{x_i})} \right]_{f = f_{t-1}}$。 
The optimal weights of tree $\beta_t$ are determined by 
木の最適な重み$\beta_t$は次のように決定されます：

$$
\beta_t = \arg \min_{\beta} \sum_{i=1}^{N} \left[ L(y_i, f_{t-1}(x_i)) + \beta^T \phi(x_i, \theta) \right]
$$

More details about GBDT, please refer to [20]. 
GBDTの詳細については、[20]を参照してください。 
As mentioned above, if we use click/non-click as responses, we simply treat $x_i = x_{q,d}$ and $y_i = y_{d,u}$. 
上記のように、クリック/非クリックを応答として使用する場合、単に$x_i = x_{q,d}$および$y_i = y_{d,u}$と扱います。 
In fact, all previous research on MLR-based content recommendation system has been focusing on using click-based information for training and evaluation. 
**実際、MLRベースのコンテンツ推薦システムに関するすべての以前の研究は、トレーニングと評価のためにクリックベースの情報を使用することに焦点を当ててきました。** 
For example, Bian et al. [2] and Agarwal et al. [1] have used users’ click/view data in Today module in Yahoo for optimizing CTR for content recommendation.
例えば、Bianら[2]やAgarwalら[1]は、YahooのTodayモジュールでユーザーのクリック/ビューデータを使用してコンテンツ推薦のCTRを最適化しています。

<!-- ここまで読んだ! -->

**Dwell Time for MLR:** There are two intuitive ways to incorpo-rate dwell time into MLR frameworks. 
**滞在時間をMLRフレームワークに組み込むための2つの直感的な方法**があります。 
Let $\gamma_d$ be the average dwell time for article $d$. 
記事$d$の平均滞在時間を$\gamma_d$とします。 
Taking the GBDT algorithm mentioned above, we could have: 
上記のGBDTアルゴリズムを考慮すると、次のようにできます:

1) Use the per-article dwell time as the response, treating $y_i = h(\gamma_d)$ and 
   1) 記事ごとの滞在時間を応答として使用し、$y_i = h(\gamma_d)$と扱います。 
2) Use the per-article dwell time as the weight for sample instances, treating $w_i = h(\gamma_d)$ where the function $h$ is a transformation of the dwell time. 
   1) **記事ごとの滞在時間をサンプルインスタンスの重みとして使用**し、$w_i = h(\gamma_d)$と扱います。ここで、関数$h$は滞在時間の変換です。 

In both cases, we promote articles that have high average dwell time and try to learn models that can optimize for user engagements. 
**どちらの場合も、平均滞在時間が高い記事を促進し、ユーザーエンゲージメントを最適化できるモデルを学習しようとします。**
In all our experiments, we found that $h = \log(x)$ yields the best performance.
**すべての実験で、$h = \log(x)$が最良のパフォーマンスを発揮すること**がわかりました。
(あ、だから他論文や事例でもlogとってることが多いのか...!!:thinking:)

<!-- ここまで読んだ! -->

We show the effectiveness of MLR model firstly from an offline experiment. 
まず、オフライン実験からMLRモデルの有効性を示します。
We use data from a bucket of traffic of a Yahoo property and split it uniformly at random into training and test sets, using a 70-30 split. 
Yahooのプロパティのトラフィックのバケットからデータを使用し、70-30の分割を使用して、トレーニングセットとテストセットに均等にランダムに分割します。
We repeat this sampling multiple times and the average results across all train-test splits are shown in Table 4.
このサンプリングを複数回繰り返し、すべてのトレーニング-テスト分割にわたる平均結果を表4に示します。
The first observation is that either method of using dwell time as learning target or instance weight can improve three major ranking metrics. 
**最初の観察は、滞在時間を学習ターゲットまたはインスタンス重みとして使用するいずれの方法も、3つの主要なランキング指標を改善できるということ**です。 
The second observation is that, dwell time as an instance weight leads to the best performance. 
**2つ目の観察は、インスタンス重みとしての滞在時間が最良のパフォーマンスをもたらすということ**です。 
We further validate these findings in online buckets, shown in Figure 7. 
これらの発見をオンラインバケットでさらに検証し、図7に示します。 
Without disclosing the absolute numbers, we show the same three buckets with respect to two types of performance metrics: 
絶対数を開示せずに、2種類のパフォーマンス指標に関して同じ3つのバケットを示します：

1) CTR (shown on the top) and 
   1) CTR（上部に表示）と 
2) a user engagement metric(shown on the bottom). 
   1) ユーザーエンゲージメント指標（下部に表示）。 

The user engagement metric is a proprietary one, which can be explained as the quality of users’ engagement with Yahoo homepage’s content stream. 
ユーザーエンゲージメント指標は独自のもので、Yahooのホームページのコンテンツストリームに対するユーザーのエンゲージメントの質として説明できます。 
Each data point represents the metric on a particular day.
各データポイントは特定の日の指標を表します。
We report the bucket metrics for a three month period between June 2013 and August 2013. 
**2013年6月から2013年8月の3か月間のバケット指標を報告**します。 
Initially, the three buckets were running the same linear model and we can see from the first three data points (three-day data), both CTR and the user engagement metric are similar. 
最初は、3つのバケットが同じ線形モデルを実行しており、最初の3つのデータポイント（3日間のデータ）から、CTRとユーザーエンゲージメント指標の両方が類似していることがわかります。 (A/Aテストってことね...!:thinking:)
Then, we update the models as follows: 
次に、モデルを次のように更新します：

1) A: a linear model optimizes click/non-click, 
   1) A: 線形モデルがクリック/非クリックを最適化します。 
2) B: a GBDT model optimizes click and 
   1) B: GBDTモデルがクリックを最適化します。 
3) C: a GBDT model optimizes dwell time $h(\gamma_d)$. 
   1) C: GBDTモデルが滞在時間$h(\gamma_d)$を最適化します。 

It is interesting that after updating models, we observe a divergence of the performances.
モデルを更新した後、パフォーマンスの乖離が観察されるのは興味深いです。 
Bucket A becomes the worst performing bucket in both metrics while bucket C outperforms other buckets consistently for almost two months time until all buckets were ended.
バケットAは両方の指標で最もパフォーマンスが悪くなり、バケットCはほぼ2か月間他のバケットを一貫して上回りました。
Therefore, from our empirical experiences, optimizing dwell time not only achieves better user engagement metrics but also improves CTR as well. 
**したがって、私たちの経験から、滞在時間を最適化することは、より良いユーザーエンゲージメント指標を達成するだけでなく、CTRも改善します。** 
One plausible cause is when optimizing towards dwell-based engaging signals rather than high CTR, users may better like the content recommended, come back to the site and click more. 
**一つの考えられる原因は、高いCTRではなく滞在時間に基づくエンゲージメント信号を最適化する際に、ユーザーが推薦されたコンテンツをより好み、サイトに戻ってきてさらにクリックする可能性があること**です。(まさにリテンションじゃん...!!:thinking:)
We leave the thorough analysis of this finding as future work.
この発見の徹底的な分析は今後の課題とします。

![]()
figure7

![]()
table 4

| Signal | MAP | NDCG | NDCG@10 |
|---|---|---|---|
| Click as Target | 0.4111 | 0.6125 | 0.5680 |
| Dwell Time as Target | 0.4210 | 0.6201 | 0.5793 |
| Dwell Time as Weight | 0.4232 | 0.6226 | 0.5820 |

<!-- ここまで読んだ! -->

## 5. USE CASE II: COLLABORATIVE FILTERING

In the previous section, we elaborated how dwell time can be used in the context of MLR, requiring enough per-item interaction activities from a user to build usable interest profile. 
前のセクションでは、滞在時間がMLRの文脈でどのように使用できるかを詳述しました。これは、ユーザーが使用可能な興味プロファイルを構築するために、アイテムごとの十分なインタラクション活動を必要とします。
Thus, it is very challenging for the previous approach to recommend content to users who are not very active (e.g. new users), or to recommend new content that has no overlap with the users’ historically read items. 
したがって、以前のアプローチでは、あまりアクティブでないユーザー（例えば、新しいユーザー）にコンテンツを推薦したり、ユーザーが過去に読んだアイテムと重複しない新しいコンテンツを推薦することが非常に困難です。 
CF techniques utilize user engagement signals on particular stories to discover users who have similar reading interest from a broad audience and target them with the same or similar content. 
CF技術は、特定のストーリーに対するユーザーのエンゲージメント信号を利用して、広範なオーディエンスから類似の読書興味を持つユーザーを発見し、同じまたは類似のコンテンツでターゲットにします。 
In this section, we validate how dwell time can be used in CF frameworks to better improve the performance. 
このセクションでは、滞在時間がCFフレームワークでどのように使用できるかを検証し、パフォーマンスを向上させる方法を示します。

We formalize the problem into the classic matrix factorization framework where latent features of items and user latent features are jointly learnt from a user-item interaction matrix. 
私たちは、この問題を古典的な行列因子分解フレームワークに形式化し、アイテムの潜在特徴とユーザーの潜在特徴をユーザー-アイテムインタラクション行列から共同で学習します。 
Matrix factorization models have provided state-of-the-art performance in many CF problems. 
行列因子分解モデルは、多くのCF問題において最先端のパフォーマンスを提供しています。 
In prior work, MF models were developed to operate on discrete user ratings (e.g., movie ratings) as labels, thus making it difficult to directly apply these models in settings where explicit ratings are usually missing or hard to collect. 
以前の研究では、MFモデルはラベルとして離散的なユーザー評価（例：映画評価）で動作するように開発されており、したがって、明示的な評価が通常欠落しているか収集が困難な設定でこれらのモデルを直接適用することが難しくなっています。 
For where $r_{i,j}$ refers to positive examples, $r_{i,k}$ refers to negative examples. 
ここで、$r_{i,j}$は正の例を指し、$r_{i,k}$は負の例を指します。 
The difference between the training process of dwell time and click is the bootstrap process of negative examples. 
**滞在時間とクリックのトレーニングプロセスの違いは、負の例のブートストラッププロセス**です。 
For click, no-click feedbacks are treated as negative data. 
クリックの場合、ノークリックのフィードバックは負のデータとして扱われます。 
For dwell time, for each click with dwell time, we randomly sample another click feedback with less dwell time or non-click feedback. 
滞在時間の場合、滞在時間を伴う各クリックについて、滞在時間が短い別のクリックフィードバックまたはノークリックフィードバックをランダムにサンプリングします。 

<!-- ここまで読んだ! -->

**Dataset: The data used in this experiment is collected from a bucket (a small sample traffic) of a Yahoo property, spanning a three month period.** 
**データセット：この実験で使用されるデータは、Yahooのプロパティのバケット（小さなサンプルトラフィック）から収集され、3か月間にわたります。** 
We perform training on the first three months and prediction on last month. 
最初の3か月でトレーニングを行い、最後の1か月で予測を行います。 
We further remove the users and items with less than 10 clicks. 
さらに、10回未満のクリックを持つユーザーとアイテムを削除します。 
In this dataset, we have 147,069 distinct users and 11,535 distinct items, yielding 4,358,066 events in the training set and 199,420 events in the test set. 
このデータセットには、147,069の異なるユーザーと11,535の異なるアイテムが含まれており、トレーニングセットには4,358,066のイベント、テストセットには199,420のイベントがあります。 

**Evaluation Method and Metrics: We group users by time periods and construct sessions of all items a user consumed in a particular time period (e.g., months, day, hour and etc.).** 
**評価方法とメトリクス：ユーザーを時間の期間でグループ化し、特定の時間期間（例：月、日、時間など）にユーザーが消費したすべてのアイテムのセッションを構築します。** 
Instead of evaluating how well we can predict clicks/non-clicks, we evaluate the proposed methods in terms of ranking metrics. 
クリック/ノークリックをどれだけ正確に予測できるかを評価するのではなく、提案された方法をランキングメトリクスの観点から評価します。 
We use Mean Average Precision (MAP) and Normalized Discounted Cumulative Gain (NDCG) as main evaluation metrics. 
主な評価メトリクスとして、平均平均精度（MAP）と正規化割引累積ゲイン（NDCG）を使用します。 
We start the definition of metrics by focusing on a particular user. 
メトリクスの定義は、特定のユーザーに焦点を当てることから始めます。 
Let Precision@k for a particular user in one session as: 
特定のユーザーの1つのセッションにおけるPrecision@kを次のように定義します： 

$$
\text{Prec@k} = \frac{1}{k} \sum_{j=1}^{k} r[j]
$$

where $k$ denotes the truncation position and $r[j]$ is whether the ranked document at the $j$ position is relevant or not. 
ここで、$k$は切り捨て位置を示し、$r[j]$は$j$位置のランク付けされたドキュメントが関連しているかどうかを示します。 
Average Precision, the measure using two levels of relevance judgement, is depended on the basis of Precision 
平均精度は、2つのレベルの関連性判断を使用する測定値で、精度に基づいています。 

$$
AP = \frac{|D^+|}{\sum_{j} r[j] \times \text{Prec@j}}
$$

where $|D^+|$ denotes the number of relevant items with respect to the user in this session. 
ここで、$|D^+|$は、このセッションにおけるユーザーに関連するアイテムの数を示します。 
Given a ranked list for a session, we can compute an AP for this session. 
セッションのためのランク付けされたリストが与えられた場合、このセッションのAPを計算できます。 
Then MAP is defined as the mean of AP over all sessions for all users. 
次に、MAPはすべてのユーザーのすべてのセッションにわたるAPの平均として定義されます。 
NDCG@k is a measure for evaluating top k positions of a ranked list using multiple levels (labels) of relevance judgement. 
NDCG@kは、複数のレベル（ラベル）の関連性判断を使用して、ランク付けされたリストの上位k位置を評価するための測定値です。 
It is defined as 
それは次のように定義されます。 

$$
NDCG@k = \frac{1}{N_k} \sum_{j=1}^{k} \frac{r[j]}{\log_2(j+1)}
$$
where NDCG is just for all positions. 
ここで、NDCGはすべての位置に対してのものです。 

**Experimental Results: There are two different strategies for evaluation.** 
**実験結果：評価には2つの異なる戦略があります。** 
The first experiment takes the data from first three months as training data while the last one as test data. 
最初の実験では、最初の3か月のデータをトレーニングデータとして使用し、最後の1か月をテストデータとして使用します。 
The second one is to use sliding window to perform daily or weekly prediction. 
2つ目は、スライディングウィンドウを使用して日次または週次の予測を行うことです。 
The overall performance is shown in Table 5 where the table is split into three parts, the first part about monthly prediction, the middle part about weekly prediction and the bottom part about daily prediction. 
全体のパフォーマンスは表5に示されており、表は3つの部分に分かれています。最初の部分は月次予測に関するもので、中間部分は週次予測に関するもので、下部は日次予測に関するものです。 
For weekly prediction and daily prediction, the metrics are averaged numbers across multiple weeks or days. 
週次予測と日次予測の場合、メトリクスは複数の週または日の平均値です。 
We also vary the latent dimension K for both click version and the dwell time version and only report the best performance across different K values. 
クリックバージョンと滞在時間バージョンの両方について潜在次元Kを変化させ、異なるK値の中で最良のパフォーマンスのみを報告します。 
We can observe that in all evaluation methods and all metrics, the model to optimize dwell time has a comparable performance as the one to optimize clicks. 
**すべての評価方法とすべてのメトリクスにおいて、滞在時間を最適化するモデルはクリックを最適化するモデルと同等のパフォーマンスを持つ**ことが観察できます。 
In addition, the performance of dwell time based models are consistently better than the click based ones. 
さらに、滞在時間に基づくモデルのパフォーマンスは、クリックに基づくモデルよりも一貫して優れています。 
One plausible reason, for the small overall improvement, is that content features or user-side information may be needed for better predicting dwell time based rating. 
**全体的な改善が小さい一因として、コンテンツの特徴やユーザー側の情報が滞在時間に基づく評価をより良く予測するために必要かも**しれません。 
Deeper analysis and experimentation on the benefit of dwell time based CF models is future work. 
滞在時間に基づくCFモデルの利点に関するより深い分析と実験は今後の課題です。

<!-- ここまで読んだ! -->

## 6. DISCUSSION AND CONCLUSIONS 議論と結論

In this paper, we demonstrated how dwell time is computed from a large scale web log and how it can be incorporated into a personalized recommendation system. 
本論文では、大規模なウェブログからどのように滞在時間が計算され、どのようにパーソナライズされた推薦システムに組み込むことができるかを示しました。
Several approaches are proposed for accurately computing item-level user content consumption time from both client side and server side logging data. 
クライアント側とサーバー側のログデータの両方から、アイテムレベルのユーザーコンテンツ消費時間を正確に計算するためのいくつかのアプローチが提案されています。
In addition, we exploited the dwell time distributions of different content types for normalizing users’ engagement signals into the same space. 
さらに、異なるコンテンツタイプの滞在時間分布を利用して、ユーザーのエンゲージメント信号を同じ空間に正規化しました。
For MLR, we proposed using per-user per-item dwell time as the learning target and demonstrated that it can result in better performances. 
MLR（多重線形回帰）においては、ユーザーごとアイテムごとの滞在時間を学習ターゲットとして使用することを提案し、それがより良いパフォーマンスをもたらすことを示しました。
For CF, we used dwell time as a form of implicit feedback from users and demonstrated how it can be incorporated into a state-of-the-art matrix factorization model, yielding competitive and even better performances than the click-optimized counterpart. 
CF（協調フィルタリング）においては、滞在時間をユーザーからの暗黙的フィードバックの一形態として使用し、最先端の行列因子分解モデルにどのように組み込むことができるかを示し、クリック最適化されたモデルよりも競争力があり、さらにはそれを上回るパフォーマンスを得られることを示しました。
For future work, we would like to design dwell time based user engagement metrics and explore how to optimize these metrics directly. 
今後の研究では、滞在時間に基づくユーザーエンゲージメント指標を設計し、これらの指標を直接最適化する方法を探求したいと考えています。
We would also like to investigate better ways to normalize dwell time. 
また、滞在時間を正規化するためのより良い方法を調査したいと考えています。
This will enable us to extract better user engagement signals for training recommendation systems thereby optimizing for long term user satisfaction. 
これにより、推薦システムのトレーニングのためにより良いユーザーエンゲージメント信号を抽出し、長期的なユーザー満足度を最適化することが可能になります。


<!-- ここまで読んだ! -->
