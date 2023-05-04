## link リンク

https://pchandar.github.io/files/papers/Gruson2019.pdf
https://pchandar.github.io/files/papers/Gruson2019.pdf

## title タイトル

Offline Evaluation to Make Decisions About Playlist Recommendation Algorithms
プレイリスト推薦アルゴリズムの判断材料となるオフライン評価

## abstract アブストラクト

Evaluating algorithmic recommendations is an important, but difficult, problem.
アルゴリズムによるレコメンデーションを評価することは、重要であるが難しい問題である。
Evaluations conducted offline using data collected from user interactions with an online system often suffer from biases arising from the user interface or the recommendation engine.
オンラインシステムを利用したユーザーとの対話から収集したデータを用いてオフラインで行う評価では、ユーザーインターフェースや推薦エンジンに起因するバイアスに悩まされることが多い。
Online evaluation (A/B testing) can more easily address problems of bias, but depending on setting can be time-consuming and incur risk of negatively impacting the user experience, not to mention that it is generally more difficult when access to a large user base is not taken as granted.
オンライン評価（A/Bテスト）は、バイアスの問題に対処しやすいのですが、設定によっては手間がかかり、ユーザーエクスペリエンスに悪影響を及ぼすリスクがありますし、一般的に多くのユーザーベースへのアクセスが当たり前でない場合は、より困難です。
A compromise based on counterfactual analysis is to present some subset of online users with recommendation results that have been randomized or otherwise manipulated, log their interactions, and then use those to de-bias offline evaluations on historical data.
反実仮想分析に基づく妥協案としては、オンラインユーザーの一部に対して、無作為化またはその他の方法で操作された推薦結果を提示し、そのやりとりを記録し、それを使って過去のデータに基づいてオフラインでの評価を偏らせる方法がある。
However, previous work does not offer clear conclusions on how well such methods correlate with and are able to predict the results of online A/B tests.
しかし、このような手法がオンラインのA/Bテストとどの程度相関し、結果を予測できるのかについては、これまでの研究では明確な結論は得られていません。
Understanding this is crucial to widespread adoption of new offline evaluation techniques in recommender systems.
このことを理解することは、レコメンダーシステムに新しいオフライン評価技術を広く採用する上で非常に重要です。
In this work we present a comparison of offline and online evaluation results for a particular recommendation problem: recommending playlists of tracks to a user looking for music.
本研究では、音楽を探しているユーザーに対して楽曲のプレイリストを推薦するという特定の推薦問題に対して、オフラインとオンラインの評価結果の比較を行った結果を発表した。
We describe two different ways to think about de-biasing offline collections for more accurate evaluation.
オフラインコレクションをより正確に評価するためのバイアス除去について、2つの異なる方法について説明します。
Our results show that, contrary to much of the previous work on this topic, properly-conducted offline experiments do correlate well to A/B test results, and moreover that we can expect an offline evaluation to identify the best candidate systems for online testing with high probability.
その結果、このテーマに関する多くの先行研究とは異なり、適切に実施されたオフライン実験は、A/Bテストの結果と良好な相関を示し、さらに、オフライン評価によって、オンラインテストに最適な候補システムを高い確率で特定できることが期待できる。

# Introduction 序章

Recommender systems are in wide use today, used for everything from recommending video and music to recommending products for purchase to recommending things to do and places to go.
リコメンダーシステムは、映像や音楽の推薦、購入商品の推薦、行動や場所の推薦など、あらゆる用途に使用され、今日広く普及しています。
Recommendation system technology is now in search engines, advertising services, and even personal fashion assistance.
レコメンデーションシステムの技術は、検索エンジンや広告サービス、さらには個人のファッション支援にも応用されています。

Many of the use cases for recommendation concern contextual personalization: getting the right results to the right users at the right time.
レコメンデーションのユースケースの多くは、適切なユーザーに適切な結果を適切なタイミングで提供するという、文脈に応じたパーソナライゼーションに関連しています。
Evaluating this, however, can be challenging.
しかし、これを評価するのは難しいことです。
Broadly speaking, there are two ways to evaluate recommender systems: online, using A/B tests to compare different approaches by their effect on logged user interactions, and offline, using some log of historical user interactions under the assumption that the users of that system would like the same items if they were served by different approaches.
大まかに言えば、レコメンダーシステムの評価には、A/Bテストを使って、ログに残るユーザーとのインタラクションに対する効果で異なるアプローチを比較するオンラインと、そのシステムのユーザーが異なるアプローチでサービスを受けた場合、同じアイテムを好むと仮定して、過去のユーザーインタラクションのログを使うオフラインの2つのやり方があります。

It is hard to capture context in offline evaluations.
オフラインの評価では、文脈を捉えることが難しい。
Logged interactions are often biased by the user interface and by the recommendation engine itself: the engine is trained such that it will prefer certain types of content over others, and the types of content it prefers will naturally see more user interactions.
ログに記録されたインタラクションは、ユーザーインターフェースやレコメンデーションエンジン自体によって偏りが生じます。エンジンは、ある種のコンテンツを他のコンテンツよりも好むように訓練されており、好むタイプのコンテンツは、当然ユーザーとのインタラクションが多くなります。
This could be alleviated by building test collections with additional human judgments, but that is costly and moreover very difficult to do in a way that captures the personal nature of recommendations.
これは、人間の判断を加えたテストコレクションを構築することで軽減できますが、コストがかかり、さらに、推薦の個人的な性質をとらえた方法で行うことは非常に困難です。

Online evaluation is an attractive alternative because it does not require such strong assumptions about user’s interactions.
オンライン評価は、ユーザーのインタラクションについてそのような強い仮定を必要としないので、魅力的な代替案です。
It does, however, require a reasonably large user base and some time to collect enough data to be able to make a decision about the experimental systems being tested.
しかし、それなりに大規模なユーザーベースと、テスト中の実験システムについての判断を下せるだけのデータを収集するための時間が必要であることは確かです。
Furthermore, there is risk in exposing users to results that are harmful in some way—even if the harm is just that the user is disinterested and leaves the platform.
さらに、何らかの形で有害な結果にユーザーをさらすことにはリスクがある。たとえ、その有害性が、ユーザーが興味を失ってプラットフォームから離れることだけだとしても。
Offline evaluation prior to online evaluation can mitigate this by giving some indication of which experiments are likely to perform well online and which aren’t.
オンライン評価の前にオフライン評価を行うことで、どの実験がオンラインでうまくいきそうで、どの実験がそうでないかをある程度把握することができ、これを軽減することができます。

Even with an initial online evaluation, it is not likely that we can take everything that performs well offline into an online test.
最初のオンライン評価でも、オフラインでうまくいっているものをすべてオンラインテストに持ち込めるとは思えません。
Figure 1 illustrates the problem: we can often test hundreds of ideas each week just by changing feature sets and hyperparameters, but what we can test online is always limited by time and the size of the user population.
図1はその問題を示しています。特徴セットやハイパーパラメーターを変えるだけで、毎週何百ものアイデアをテストできることがよくありますが、オンラインでテストできるものは、常に時間とユーザー集団のサイズによって制限されています。
Thus we need an offline evaluation that not only separates good systems from bad, but can also help us make reliable decisions about which experimental systems are the best candidates to test online.
したがって、良いシステムと悪いシステムを分けるだけでなく、どの実験的なシステムをオンラインでテストするのが最適な候補なのか、信頼できる決定を下すのに役立つオフライン評価が必要なのです。

In this work we present a new study showing offline evaluation results can predict online A/B test results under the right approach to de-biasing.
この研究では、バイアス除去の適切なアプローチにより、オフラインの評価結果がオンラインのA/Bテスト結果を予測できることを示す新しい研究を紹介します。
We present a simulation-based approach to deciding on the experimental systems with the highest potential for success in an A/B test.
A/Bテストにおいて、成功の可能性が高い実験システムを決定するためのシミュレーションベースのアプローチを紹介する。
We also demonstrate how offline evaluation can be used to identify the most promising individual system components or characteristics.
また、オフライン評価を用いて、最も有望な個々のシステムコンポーネントや特性を特定できることを実証しています。

The rest of this paper is organized as follows.
本稿の残りの部分は、以下のように構成されている。
In Section 2 we review previous and recent work on evaluation in recommender systems.
第2節では、推薦システムにおける評価に関する過去と最近の研究をレビューする。
Section 3 describes our specific problem setting and the evaluation challenges it presents.
セクション3では、我々の特定の問題設定と、それがもたらす評価の課題について説明する。
In Section 4 we compare offline and online evaluation results for 12 experimental runs, presenting analysis on relative rankings, statistical significance, and probability of identifying the experimental runs that perform best in online tests.
セクション4では、12の実験ランについてオフラインとオンラインの評価結果を比較し、相対的な順位、統計的有意性、オンラインテストで最高のパフォーマンスを発揮する実験ランを特定する確率に関する分析を示す。
We conclude in Section 5.
第5節で結論を出す。

# Background その背景

Evaluation of recommender systems has been [21] and still is [19] an important topic of ongoing research with several open questions.
推薦システムの評価は[21]、現在も[19]、いくつかの未解決の問題を抱えた重要な研究テーマである。
Since the early work by Resnick et.
Resnickらによる初期の研究以来。
al [36] in 1994, evaluation has proceeded from predicting missing ratings of items in an offline setting to complicated models of user satisfaction using implicit online signals such as clicks, dwell time, etc [14, 13].
1994年、al [36]は、オフライン環境におけるアイテムの欠落評価の予測から、クリック数、滞在時間などの暗黙のオンラインシグナルを用いたユーザー満足度の複雑なモデルへと評価を進めてきた[14, 13]。
Other dimensions such as novelty, serendipity, diversity, etc.
新規性、セレンディピティ、多様性など、その他の次元。
have been considered for evaluating recommendation quality as well [21, 25, 42, 16].
は、推薦の質を評価するためにも考慮されている[21, 25, 42, 16]。

## Online evaluation 

A direct way of measuring recommendation quality is to measure the consumption of recommended items.
推薦品質を測定する直接的な方法は、推薦されたアイテムの消費量を測定することです。
In other words, a system that recommends music should probably focus on how often the recommendation leads to a stream.
つまり、音楽を推薦するシステムでは、その推薦がストリームにつながる頻度を重視すべきなのでしょう。
In this setting, online A/B tests are conducted to compare two systems by exposing them to real users [31].
この設定では、オンラインA/Bテストが実施され、2つのシステムを実際のユーザーにさらすことで比較します[31]。
A predefined metric is used to quantify recommendation quality (e.g., total stream per session).
推薦品質を定量化するために、あらかじめ定義されたメトリックが使用されます（例：セッションごとの総ストリーム）。
Recently, more sophisticated ways of modeling user satisfaction from implicit user feedback such as clicks, streams, etc.
最近では、クリックやストリームなどの暗黙のユーザーフィードバックから、ユーザー満足度をモデル化する方法がより洗練されてきています。
have been proposed in the context of music recommendations [14] and other domains [26].
は、音楽推薦[14]や他のドメイン[26]の文脈で提案されています。

Interleaving approaches that merge items from different engines have been used to limit the risk of poor recommendation [6].
異なるエンジンからのアイテムを統合するインターリーブアプローチは、貧弱な推薦のリスクを制限するために使用されている[6]。
Interleaving methods consist of two steps: (1) merging two or more ranked lists before presenting to the user; (2) interpreting interactions on the interleaved results.
インターリーブ法は2つのステップから構成される： (1)ユーザーに提示する前に2つ以上のランク付けされたリストをマージする、(2)インターリーブされた結果に対するインタラクションを解釈する。
Several variants has been proposed in the literature, including team-draft interleaving [35], probabilistic interleaving [23], etc.
チームドラフトインターリーブ[35]、確率的インターリーブ[23]など、いくつかのバリエーションが文献で提案されている。
(see [22] for a complete overview).
(完全な概要については[22]を参照)。

Reliably comparing systems in an online setting can take a considerable amount of time.
オンライン上で確実にシステムを比較することは、かなりの時間を要する。
In practice, A/B tests might need to be run for several weeks to get enough data to detect a statistically significant effect.
実際には、統計的に有意な効果を検出するのに十分なデータを得るために、A/Bテストを数週間実施する必要がある場合があります。
This is particularly true when there is periodicity in user behavior that may affect metrics.
特に、指標に影響を与える可能性のあるユーザー行動の周期性がある場合は、その傾向が顕著です。
Further, transforming every idea into a production-ready system to experiment online is prohibitively expensive.
さらに、すべてのアイデアを生産可能なシステムに変換し、オンラインで実験することは、法外なコストがかかります。
Thus there is some limit on the number of A/B tests that can be run depending on the total size of the user population, the size of samples needed for each cell, and the amount of time the tests need to run for.
このように、ユーザー集団の総規模、各セルに必要なサンプルのサイズ、テストの実行時間によって、実行できるA/Bテストの数にはある程度の制限があります。
Additionally, we likely do not want to A/B test every potential system we can think of.
また、考えられるすべてのシステムをA/Bテストしたいとは思わないはずです。
Many are simply going to perform poorly, and it would be better to know that in advance so that we do not risk exposing users to them.
ただ、その多くは性能が低いものであり、それを事前に知っておくことで、ユーザーを危険にさらすことはないでしょう。
Thus, A/B testing is not suitable for many common evaluation cases.
このように、A/Bテストは多くの一般的な評価ケースに適していません。

## Offline evaluation オフライン評価

It is common in the academic study of recommender systems and search to use offline test collections for experimentation.
推薦システムや検索の学術研究では、オフラインのテストコレクションを実験に使うのが一般的です。
In search, the TREC initiative has produced large test collections that are reliable for testing new models for search.
検索では、TRECイニシアチブは、検索のための新しいモデルをテストするために信頼性の高い大規模なテストコレクションを生産しています。
These collections involve a large cost in acquiring human assessments of the relevance of documents to queries which has traditionally been infeasible for academics.
これらのコレクションは、クエリに対する文書の関連性を人間が評価するために大きなコストがかかるため、従来は学術的に実現不可能とされていました。
But they do not require any search systems to be running online.
しかし、これらは検索システムがオンラインで稼働している必要はありません。
Instead, they rely on expert assessors to develop search needs and judge the relevance of documents retrieved by experimental systems offline [43].
その代わりに、専門家である評価者が検索ニーズを開発し、オフラインで実験システムによって検索された文書の関連性を判断することに頼っている[43]。
Such collections are rare for recommender systems because it is difficult for assessors to judge relevance when it is personal and contextual.
個人的で文脈的である場合、評価者が関連性を判断することが難しいため、このようなコレクションはレコメンダーシステムでは稀である。
However, some recent work has applied ideas from personalized recommendation to search with experiments on large human-annotated collections such as the MSLR-WEB30k data [41].
しかし、最近の研究では、MSLR-WEB30kデータのような大規模な人間注釈付きコレクションを用いた実験により、パーソナライズド・レコメンデーションのアイデアを検索に適用したものがある[41]。

A possible compromise between fully-online and fully-offline evaluation with test collections is offline evaluation using historical data collected online.
テストコレクションを用いた完全オンライン評価と完全オフライン評価の妥協点として、オンラインで収集した履歴データを用いたオフライン評価が考えられる。
This involves curating a dataset using historical logs generated from users interacting with a recommender system, including “ground truth” inferred from interactions such as ratings or clicks.
これは、レコメンダーシステムと対話するユーザーから生成された履歴ログを使用してデータセットをキュレーションするもので、評価やクリックなどの対話から推測される「ground truth」を含んでいます。
This dataset is used to evaluate experimental systems in an offline setting, i.e., without having to expose the experimental system to real users.
このデータセットは、オフライン環境、すなわち実際のユーザーに実験システムを公開することなく、実験システムを評価するために使用されます。
This has become the favored approach for offline evaluation of recommender systems.
これは、レコメンダーシステムのオフライン評価で好まれるアプローチとなっています。

Early on, the focus was on predicting ratings that the user would provide to an item.
初期には、ユーザーがアイテムに与える評価を予測することに重点を置いていました。
In this setting, error-based metrics such as mean absolute error (MAE) and root mean squared error (RMSE) are commonly used to measure the prediction accuracy.
この設定では、平均絶対誤差（MAE）や二乗平均誤差（RMSE）などの誤差ベースのメトリクスが、予測精度を測定するために一般的に使用されています。
As recommender systems became more sophisticated with UI advancements, there was a need to take into account the user’s natural browsing behavior [19].
UIの進化に伴いレコメンダーシステムが高度化するにつれ、ユーザーの自然な閲覧行動を考慮する必要性が出てきた[19]。
Rank-based metrics that gave more importance to the top-k results were used to evaluate systems [10, 3, 39].
システムの評価には、トップkの結果をより重要視するランクベースのメトリクスが用いられた[10, 3, 39]。
Metrics such as precision, recall, and mean-average-precision commonly used in information retrieval were adopted [1].
情報検索でよく使われるprecision、recall、mean-average-precisionなどの指標を採用した[1]。
Other IR metrics such as normalized discounted cumulative gain (nDCG) [27] and mean reciprocal rank (MRR) have also been used to evaluate systems [1].
正規化割引累積利得（nDCG）[27]や平均逆数順位（MRR）など、他のIR指標もシステムの評価に用いられてきた[1]。

Incorporating historical log data for evaluation in practice is challenging due to various biases present.
過去のログデータを使って評価することは、様々なバイアスが存在するため、実際には困難です。
Some of the most common datasets used in recommender systems research such as MovieLens, Last.FM, etc [20, 4] suffer from biases due to their UI or underlying recommendation algorithms, which the researchers have no control over.
MovieLens、Last.FMなど、推薦システムの研究で最もよく使われるデータセット [20, 4] は、そのUIや基礎となる推薦アルゴリズムによるバイアスに悩まされており、研究者がコントロールすることができない。
Examples of biases include position bias [28] (that users are more likely to pay attention to top-ranked items even if they are not as relevant), popularity bias (that many systems have a tendency to promote more popular content), attractiveness bias [45], trust bias [30], and what we call “selection bias”, that is the propensity of the system to lean towards particular types of content due to how it was trained or how content is modeled.
バイアスの例としては、ポジション・バイアス[28]（たとえ関連性が低くても、ユーザーは上位のアイテムに注目する傾向がある）、人気バイアス（多くのシステムはより人気のあるコンテンツを促進する傾向がある）、魅力バイアス[45]、信頼バイアス[30]、そして我々が「選択バイアス」と呼ぶもの、つまりシステムが訓練されたかコンテンツのモデル化方法によって特定の種類のコンテンツに傾く傾向がある。
A commonly used approach to handle bias in historical log data is to model user’s behavior when interacting recommendation results and then use them to minimize the effect of the bias in click data [12, 7, 8].
履歴ログデータの偏りを処理するためによく使われるアプローチは、推薦結果と対話する際のユーザーの行動をモデル化し、それを用いてクリックデータの偏りの影響を最小化することです[12、7、8]。

However, studies have pointed out that error-based, rank-based and other metrics computed on offline dataset do not correlate with online evaluation results [2, 38, 15, 17] and researchers have questioned validity of offline evaluation.
しかし、オフラインのデータセットで計算されたエラーベース、ランクベース、その他のメトリクスは、オンラインの評価結果と相関がないことが指摘されており [2, 38, 15, 17] 、研究者はオフライン評価の妥当性を疑問視している。

## Counterfactual analysis 反実仮想分析

Recently, approaches based on importance sampling [24] have been proposed for evaluating recommender systems in an unbiased manner [32, 41].
近年、推薦システムを偏りなく評価するために、重要度サンプリング [24] に基づくアプローチが提案されている [32, 41]。
The proposed techniques are based on propensity weighting originally used in causal inference [37], and more recently in other domains such as IR evaluation [29, 44] and computational advertising [5].
提案する技術は、もともと因果推論[37]で使われ、最近ではIR評価[29, 44]や計算広告[5]などの他の領域でも使われている傾向重み付けに基づくものです。
These approaches rely on propensity scores that are computed and logged.
これらのアプローチは、計算され記録される傾向スコアに依存している。
In order to ensure data is collected on combinations that wouldn’t happen with a production system, some random exploration is often included.
生産システムでは起こりえないような組み合わせのデータを確実に収集するために、ランダムな探索が含まれることが多いのです。

In this setting, the estimator uses the logs collected using a production policy µ to compute the expected reward of a target policy π.
この設定では、推定器は、生産ポリシーμを用いて収集したログを用いて、ターゲットポリシーπの期待報酬を計算する。
However, the importance sampling estimator and its variants such as capped importance sampling [5], normalized importance sampling [34] and doubly robust estimation [11], suffer from high variance.
しかし，重要度サンプリング推定量とその変形であるキャップド重要度サンプリング [5]，正規化重要度サンプリング [34]，二重ロバスト推定 [11] は，高い分散に悩まされている．
Swaminathan et al.[40] proposed the normalized capped importance sampling (NCIS) estimator using control variates to address this issue.
Swaminathanら[40]は、この問題に対処するため、制御変数を用いた正規化キャップド・インポータンス・サンプリング（NCIS）推定器を提案した。
Gilotte et al.[18] successfully demonstrated the use of NCIS to evaluate recommender systems.
Gilotteら[18]は、NCISを利用してレコメンダーシステムを評価することに成功した。

In this work, we present a new study showing offline evaluation results can predict online A/B test results under the right approach to de-biasing.
本研究では、バイアス除去の適切なアプローチにより、オフラインの評価結果がオンラインのA/Bテスト結果を予測できることを示す新しい研究を発表する。
We present a simulation-based approach to deciding on the experimental systems with the highest potential for success in an A/B test.
A/Bテストにおいて、成功の可能性が高い実験システムを決定するためのシミュレーションベースのアプローチを紹介する。
We also demonstrate how offline evaluation can be used to identify the most promising individual system components or characteristics.
また、オフライン評価を用いて、最も有望な個々のシステムコンポーネントや特性を特定できることを実証しています。

# Problem Setting 問題設定

The specific recommendation problem we are considering is illustrated in Figure 2: a user comes to a recommender system (in this case, a music recommendation system) via a mobile interface and is presented with recommendations for playlists, called cards in this setting, organized into thematically-related shelves.
図2に示すように、あるユーザーがモバイルインターフェースを通じて推薦システム（この場合、音楽推薦システム）を訪れ、テーマに関連した棚に整理されたプレイリスト（この設定ではカードと呼ぶ）の推薦文を提示される。

The user can scroll up and down to reveal shelves, and left and right within a shelf to see additional cards.
ユーザーは、上下にスクロールして棚を表示し、棚の中で左右にスクロールして追加のカードを表示することができます。
The presentation of both shelves and cards is personalized to user and context.
棚もカードも、ユーザーや文脈に合わせてパーソナライズされた演出が可能です。
One user’s top shelf may not be the same as another user’s, and within a given shelf, the top cards recommended to one user may not be the same as those recommended to another user, and the same user may not see the same layout if they visit the page a second time.
あるユーザーのトップシェルフが他のユーザーのトップシェルフと同じとは限りませんし、あるシェルフの中で、あるユーザーに推奨されるトップカードと他のユーザーに推奨されるカードが同じとは限りませんし、同じユーザーが2度目にページを訪れたときに同じレイアウトが表示されないかもしれません。
Importantly, the set of cards available for recommendation on this page is relatively small: about 200 algorithmic or editorially-curated playlists in addition to playlists from the user’s recent listening history, each of which is manually assigned to one or more shelves.
重要なのは、このページで推薦できるカードのセットが比較的小さいことです。ユーザーの最近のリスニング履歴からのプレイリストに加えて、アルゴリズムまたは編集者がキュレーションした約200のプレイリストがあり、それぞれ1つまたは複数の棚に手動で割り当てられているのです。

In principle, the goal of the personalized recommendation engine is to assemble a layout of shelves and cards that maximizes user satisfaction.
原則として、パーソナライズド・レコメンデーション・エンジンは、ユーザーの満足度を最大化する棚やカードのレイアウトを組み立てることを目標としています。
This problem is made more tractable in practice by assuming that cards can be selected independently of one another as well as independently of shelves, and the full layout can be assembled post hoc from a simple ranking of cards.
この問題は、カードが互いに独立して選択され、棚からも独立して選択されると仮定することで、実際には、カードの単純なランキングから完全なレイアウトを事後的に組み立てることができるようになる。
Thus the goal of the personalized recommendation engine is to learn a reward function f : C × X → R that accurately predicts the likelihood of a user engaging with a recommended card c ∈ C for a given context x ∈ X.
したがって、パーソナライズド・レコメンデーション・エンジンの目標は、与えられたコンテキストx∈Xに対して、ユーザが推奨カードc∈Cに関与する可能性を正確に予測する報酬関数f : C × X → Rを学習することである。
Given that reward function, we wish to identify a policy π(C = c|x ∈ X) for picking a card to be presented to the user/context x such that total reward V = Í i f (ci , xi) · π(ci |xi) is maximized.
x ∈ X) for picking a card to be presented to the user/context x such that total reward V = Í i f (ci , xi) · π(ci
In this work, we adopt a contextual bandits approach similar to the one proposed by McInerney et al.[33].
この作品では、McInerneyら[33]が提案したものと同様のコンテキストバンディットアプローチを採用しています。
A contextual bandit requires that we specify a reward model, a representation of context x, an action space, and a policy for selecting an action given a context.
文脈バンディットでは、報酬モデル、文脈xの表現、行動空間、文脈を与えられた行動を選択するためのポリシーを指定する必要があります。

The reward model we currently use is impression-to-stream, that is, whether a card was seen by the user, and if so, whether the user streamed at least one track from the playlist represented by the card for at least 30 seconds.
現在使用している報酬モデルは、インプレッション・トゥ・ストリーム、つまり、カードがユーザーに見られたかどうか、見られた場合は、カードが表すプレイリストの中から少なくとも1曲を30秒以上ストリーミングしたかどうかというものです。
This is a binary rather than real-valued reward, which we use for simplicity; we note that it can be replaced by more complex measures of user satisfaction.
この報酬は実数値ではなく2値であり、ここでは簡略化のために使用しています。

The context is essentially the user request.
コンテキストは、基本的にユーザーのリクエストです。
It is typically represented using features such as user demographic characteristics, the time of the request, the affinity the user has for particular tracks, the user’s recent play history, and other contextual features.
一般的には、ユーザーの人口統計学的特徴、リクエストの時間、ユーザーが特定の楽曲に持つ親和性、ユーザーの最近の再生履歴、およびその他の文脈的特徴などの特徴を用いて表現されます。

The action space is the set of cards C.We simplify the problem by assuming that the set of cards for the context is static1 .
行動空間はカードの集合Cである。文脈に応じたカードの集合は静的であると仮定して、問題を単純化する1 。
Furthermore, we have a set of manual constraints specifying the cards that are to be grouped into each shelf.
さらに、各棚にまとめるカードを指定する手動制約があります。
Shelves are not explicitly part of the action space; instead, the policy is based on a machine-learned model that scores cards and uses those scores along with the shelf constraints to rank shelves.
その代わりに、カードに点数をつけ、その点数と棚の制約を利用して棚をランク付けする機械学習モデルに基づいて、ポリシーを決定しています。
In this way the selection of shelves follows deterministically from the scoring of cards2.
このように、棚の選択はカードの採点から決定論的に導かれる2。

There are several factors we can manipulate to optimize impressionto-stream rate: the feature sets that represent the user context, the particular machine learning models that score cards, the way a model is instantiated and optimized, the model hyperparameters, and so on.
ユーザーのコンテキストを表す特徴量、カードをスコアリングする特定の機械学習モデル、モデルのインスタンス化と最適化の方法、モデルのハイパーパラメーターなど、インプレッションからストリームまでの速度を最適化するために操作できる要素がいくつかあります。
Identifying the best combination of variables for a recommendation policy demands a reliable evaluation methodology.
推薦政策に最適な変数の組み合わせを特定するためには、信頼性の高い評価方法が必要です。

## Online evaluation 

Different approaches to selecting the factors listed above can be compared by a set of A/B tests: given several possible sets of factors, a test cell is configured for each one and each user is randomly assigned to a test cell or to a control group.
上記の要因を選択するための異なるアプローチは、一連のA/Bテストによって比較することができます：いくつかの可能な要因のセットが与えられ、それぞれにテストセルが設定され、各ユーザーはテストセルまたはコントロールグループにランダムに割り当てられます。
Users in a particular test cell see recommendations based on a particular policy, with about 1% of users assigned to each cell.
特定のテストセルのユーザーは、特定のポリシーに基づいたレコメンデーションを見ることができ、各セルには約1％のユーザーが割り当てられています。
We record relevant information about cards (such as features, scores, shelves, etc.) and user interactions (impressions, streams, etc).
カードに関する関連情報（機能、スコア、棚など）やユーザーインタラクション（インプレッション、ストリームなど）を記録します。
After some time has passed we can compare each test cell on various metrics.
時間が経過したら、各テストセルを様々な指標で比較することができます。
As mentioned above, our reward is impression-to-stream, so impression-to-stream rate is the metric we are interested in.
前述の通り、我々の報酬はimpression-to-streamなので、impression-to-stream rateが気になる指標になります。

## Offline evaluation with historical logs ヒストリカルログによるオフライン評価

The offline evaluation problem is to estimate mean reward V = 1 n Ín i ri · π(ci |xi) using a historical log of length n.
xi) using a historical log of length n.
We obtain historical logs from systems running in production.
本番で稼働しているシステムの履歴ログを取得します。
Production systems are performing some level of exploration, which is captured in the policy.
生産システムはある程度の探査を行っており、それはポリシーで把握されている。
As we described in Section 2.2, these logs are biased; in order to use them for offline evaluation, they need to be de-biased in some way.
セクション2.2で説明したように、これらのログは偏っている。オフライン評価に使用するためには、何らかの方法で偏りをなくす必要がある。
We explore three estimators for V :
V の3つの推定量を検討する．

- (1) the inverse propensity score estimate, also known as the importance sampling estimate (IS); (1) 重要度サンプリング推定値（IS）とも呼ばれる逆性向スコア推定値；

- (2) a capped importance sampling estimate (CIS); (2) キャップ付き重要度サンプリング推定値（CIS）；

- (3) a normalized and capped importance sampling estimate (NCIS). (3) 正規化され、キャップされた重要度サンプリング推定値（NCIS）。

In each case, the system being logged has a particular policy which we call the logging policy and denote µ(ci |xi).
xi).
The goal of offline evaluation is to estimate the value of a new target policy π to be evaluated against the logging policy µ.
オフライン評価の目的は、ロギングポリシーμに対して評価すべき新しいターゲットポリシーπの値を推定することである。

### Importance sampling. 重要度サンプリング。

The importance sampling estimator for V is based on re-weighting rewards by the propensity weight, which is the ratio of the target policy probability to the logging policy probability.
Vの重要度サンプリング推定器は、ロギング政策確率に対する目標政策確率の比率である傾向重みで報酬を再重量化することに基づいています。
In particular:
特に：

$$


$$

This estimator is unbiased in expectation, but its variance is high, as it grows polynomially with the size of the action space.
この推定器は期待値では不偏であるが、行動空間の大きさに応じて多項式に成長するため、分散は大きい。

### Capping propensities. キャッピングプロペンス

When propensities are taken from a production log that is performing exploration, some values may be very low because random exploration produces layouts that are unlikely to be selected otherwise.
探査中のプロダクションログからプロペンシティを取得した場合、ランダムな探査によって他の方法では選択されにくいレイアウトが生成されるため、一部の値は非常に低くなる可能性があります。
These low propensities can have an outsized effect on the estimator.
このような低いプロペンシティは、推定値に大きな影響を与える可能性があります。
For example, if a card selected by the logging policy with propensity 0.001 has much higher probability of being selected by the target system—say 0.5 or more—the reward for that card could be multiplied by a factor of over 500.
例えば、ロギングポリシーで0.001のカードが、ターゲットシステムで0.5以上の高い確率で選ばれた場合、そのカードの報酬を500倍以上にすることができます。
This is particularly a problem when interactions are sparse, as just a handful of low-propensity cards that received a user stream end up dominating the estimator.
これは特に相互作用が疎な場合に問題となり、ユーザーストリームを受信したほんの一握りの低比重のカードが推定量を支配してしまう。

One way to solve this problem is to cap the propensity weight π (ci |xi ) µ(ci |xi ) .
xi ) µ(ci
The capped importance sampling (CIS) estimator introduces a parameter λ which is the maximum value we allow the propensity weight can take:
キャップド・インポータンス・サンプリング（CIS）推定量では、傾向ウェイトが取り得る最大値であるパラメータλを導入している：

$$
\tag{}
$$

### Normalizing the estimator. 推定量を正規化する。

Another common technique to reduce variance is to normalize the CIS estimator by the sum of the propensity weights.
分散を減らすためのもう一つの一般的な手法は、傾向重みの合計によってCIS推定量を正規化することである。
This is normalized capped importance sampling (NCIS):
これがNCIS（Normalized Capped Important Sampling）です：

$$


$$

Note that while VIPS is unbiased in expectation, VCIS and VNCIS introduce bias in order to help control variance and to allow the use of more of the data from production logs.
なお、VIPSは期待値として不偏であるが、VCISとVNCISは分散を抑制するため、また生産ログのデータをより多く使用するためにバイアスがかかっている。

### Fully-shuffled logs. フルシャッフルされたログ。

Finally, a completely orthogonal way to address bias is by making sure some subset of users see recommendations unbiased by the UI or the recommendation engine.
最後に、バイアスに対処する完全に直交する方法として、一部のユーザーがUIや推薦エンジンによってバイアスのかかっていない推薦文を見ることができるようにすることが挙げられます。
The simplest way to do this is to simply shuffle the cards and show users a completely random layout.
最もシンプルな方法は、カードをシャッフルして、完全にランダムなレイアウトをユーザーに見せることです。
This ensures that over the group of users exposed to this treatment there is no bias from the UI or from the engine.
これにより、この治療を受けたユーザーグループには、UIやエンジンによる偏りがないことが保証されます。
This randomization comes at a cost: the user experience is almost certainly going to be worse, and that may translate to longer-term losses.
このランダム化にはコストがかかります。ユーザー体験はほぼ確実に悪化し、長期的な損失につながるかもしれません。
We can therefore only send a small fraction of traffic to fully-shuffled results.
そのため、完全にシャッフルされた結果には、トラフィックのごく一部しか送ることができません。

## Deciding on systems to test online オンラインでテストするシステムを決定する

As we wrote above, not all experiments that can be tested offline can or should be tested online.
先に書いたように、オフラインでテストできる実験がすべてオンラインでテストできるわけではなく、またすべきでもありません。
A good offline evaluation should help us select those that are the best candidates for online testing.
オフラインでしっかり評価することで、オンラインテストに最適な候補となるものを選ぶことができるはずです。
Since our goal is to improve recommendations overall, the best candidates for online testing are the systems that perform the best in offline evaluations, so we want our offline evaluations to be reliable.
レコメンデーション全体を改善することが目的なので、オンラインテストの最有力候補はオフライン評価で最高のパフォーマンスを発揮するシステムであり、オフライン評価が信頼できるものであることが望まれます。

We adopt a separate policy for selecting experiments to test.
テストする実験の選定については、別の方針を採っています。
This policy is based on simulating an offline evaluation over many different logs to determine which experiments are most likely to rank highly.
この方針は、多くの異なるログでオフライン評価をシミュレートし、どの実験が上位にランクされる可能性が高いかを判断することに基づいています。
Since variance is high, we do not necessarily expect the same experiments to consistently rank at the top; given a distribution of positions in a ranking for each experiment, we can sample from this distribution experiments to deploy in A/B tests.
分散が大きいので、同じ実験が常に上位に来るとは限りませんが、各実験のランキングの順位分布があれば、この分布からA/Bテストに展開する実験を抽出することができます。

As noted above, all of the offline evaluations are done using a single log.
前述の通り、オフラインでの評価はすべて1つのログを使って行っています。
This means the estimated rewards of experiments are highly correlated: two experiments are more likely than not to preserve their ordering relative to one another when evaluated against a new sample offline.
つまり、実験の推定報酬には高い相関性があり、オフラインで新しいサンプルに対して評価した場合、2つの実験が互いの順位を維持する可能性が高い。
We can assume rewards are sampled from some distribution that captures this correlation, then simulate new evaluations by sampling from that distribution repeatedly and seeing which systems come out on top.
この相関を捉えた分布から報酬をサンプリングすると仮定し、その分布から繰り返しサンプリングすることで新たな評価をシミュレートし、どのシステムが上位に来るかを確認することができます。

We assume a multivariate normal distribution with mean vector bµ estimated from the mean estimated rewards from a large offline evaluation and covariance matrix bΣ/n estimated from the covariance between each pair of experiments and divided by the log size.
大規模なオフライン評価による平均推定報酬から推定した平均ベクトルbμと、各実験ペア間の共分散から推定した共分散行列bΣ/nを対数サイズで割った多変量正規分布を仮定している。
Mean estimated reward r is sampled from the normal distribution:
平均推定報酬rは正規分布からサンプリングされる：

$$
\tag{}
$$

The simulated ordering experiments is the ordering of sampled rewards.
順序実験のシミュレーションは、サンプリングされた報酬の順序です。
Comparing simulated rankings over many of these trials, we can estimate a probability distribution over ranks for each experiment in the evaluation.
このような多くの試行でシミュレーションされた順位を比較することで、評価における各実験の順位に関する確率分布を推定することができます。

# Experiment 実験

In this section we present results and analysis of offline experiments on different recommendation algorithms with the goal of selecting the best subset for online testing.
このセクションでは、オンラインテストに最適なサブセットを選択することを目的として、さまざまな推薦アルゴリズムに関するオフライン実験の結果と分析を紹介します。

## Playlist recommendation algorithms プレイリスト推薦アルゴリズム

We compare 12 different recommendation methods.
12種類の推薦方法を比較しています。
Algorithms differ on three dimensions:
アルゴリズムは3つの次元で異なる：

- feature set used (two different feature sets); 使用した機能セット（2種類の機能セット）；

- source of training data (raw biased logs vs. logs debiased by the NCIS estimator vs. fully-shuffled logs); トレーニングデータのソース（生のバイアス・ログ vs． NCISの推定値対でログがデビる。 フルシャッフル・ログ)；

- hyperparameter values and modeling decisions. ハイパーパラメータの値とモデリングの決定。

We number experiments 1–12.
実験に1～12の番号をつけています。
Experiment 1 is the baseline.
実験1がベースラインです。

These algorithms were tested online for a period during the summer of 2018.
これらのアルゴリズムは、2018年夏の期間、オンラインでテストされました。
We have logs from these online tests, as well as logs from production systems that are not identical to these A/B tested systems.
これらのオンラインテストのログと、これらのA/Bテストを行ったシステムと同一でない本番システムのログがあります。
We also have a small log of user traffic that saw fully-shuffled results as described above.
また、上記のように完全にシャッフルされた結果を見たユーザーのトラフィックの小さなログがあります。

## Metrics and gold standard メトリクスとゴールドスタンダード

Evaluation of the online tests is by impression-to-stream rate, which is 1 if a card was seen by a user and at least one track from the corresponding playlist was streamed for at least 30 seconds, and 0 if the card was seen but no track was streamed for 30 seconds.
オンラインテストの評価は、インプレッション・ツーストリーム率で行い、カードがユーザーに見られ、対応するプレイリストの少なくとも1曲が30秒以上ストリーミングされた場合は1、カードが見られたが30秒間曲がストリーミングされなかった場合は0とします。
We denote this V.
これをVとする。
The online test results are the gold standard.
オンラインテストの結果は、金字塔です。

An offline evaluation is attempting to estimate what impressionto-stream rate would have been had the target policy been deployed.
オフライン評価とは、対象施策が導入されていたら、インプレッションからストリームの割合がどうなっていたかを推定しようとするものです。
We use the VIS, VCIS, VNCIS estimators defined above.
上記で定義したVIS, VCIS, VNCISの推定量を使用する。

When reporting results, we normalize impression-to-stream rate and its estimates by the baseline (experiment 1) value, so that the baseline experiment will always receive a score of 1.000 in each online and offline evaluation.
結果を報告する際、ベースライン（実験1）の値でインプレッション対ストリーム率とその推定値を正規化し、オンラインとオフラインの各評価で、ベースラインの実験が常に1.000のスコアを受け取るようにしました。
The other experiments will be evaluated by how many times better they are than the baseline.
他の実験は、ベースラインより何倍優れているかで評価します。

## Statistical testing 統計的検定

Here we briefly discuss statistical testing.
ここでは、統計的検定について簡単に説明します。
Typically an A/B test is started with the goal of detecting a statistically significant effect when it is finished.
一般的にA/Bテストは、終了時に統計的に有意な効果を検出することを目標に開始されます。
Since A/B tests are done online by randomly sampling the user population to receive the treatment or control groups, the correct statistical testing procedure is a two-sample or unpaired test.
A/Bテストは、オンラインでユーザー集団を無作為にサンプリングして、治療グループまたは対照グループを作成するため、正しい統計的テスト手順は、2標本または非対称テストです。
Offline experiments, on the other hand, are done by computing the metric repeatedly on the same historical sample, and thus statistical significance testing can be done offline using onesample or paired tests.
一方、オフライン実験では、同じ履歴サンプルに対して繰り返しメトリックを計算するため、1標本または対の検定を用いてオフラインで統計的有意差検定を行うことができる。
Paired tests have the advantage of requiring fewer samples to find a significant effect.
ペアテストは、有意な効果を見つけるために必要なサンプル数が少ないという利点があります。

The t-test is a common test that has both unpaired and paired variants, but sometimes criticized for requiring the data to conform to a normal distribution.
t検定は、対になっていないものと対になっているものの両方がある一般的な検定ですが、データが正規分布に適合していることを要求するため、批判されることもあります。
An alternative is the bootstrap test, which involves sampling with replacement from the data to form a distribution of the mean.
ブートストラップテストは、データから置換を伴うサンプリングを行い、平均値の分布を形成するものである。
Bootstrapping is slow when sample sizes are large, so we would like to avoid bootstrapping if we can.
ブートストラップはサンプルサイズが大きいと時間がかかるので、できる限りブートストラップは避けたいところです。
To validate whether we could rely on the much more computationally efficient t-test, we compared bootstrap estimates of mean and variance to standard frequentist estimates.
計算効率の良いt検定に頼るかどうかを検証するために、平均と分散のブートストラップ推定値を標準的なFrequentist推定値と比較しました。
There is no difference between them, meaning we incur no loss in validity by using the t-test.
両者に差はなく、t検定による妥当性の損失はない。

## Online vs offline evaluation オンラインとオフラインの比較

Table 1 shows the relative ordering of experimental cells after the online test by normalized impression-to-stream ratio, along with statistical significance (by a two-sample t-test) between each pair of experiments.
表1は、正規化された印象対ストリーム比によるオンラインテスト後の実験セルの相対的な順序と、各組の実験間の統計的有意性（2標本t検定による）を示しています。
We consider this the “gold standard”.
私たちはこれを「ゴールドスタンダード」と考えています。
Each online test is attempting to match this table as closely as possible.
各オンラインテストは、この表とできるだけ一致するように試みられています。

### Offline evaluation with CIS and NCIS. CISやNCISとオフラインで評価する。

Table 2 shows the relative ordering of experimental cells by one baseline offline evaluation setting using the CIS estimator with a high cap (λ =1,000,000) and no normalization.
表2は、ハイキャップ（λ =1,000,000）かつ正規化なしのCIS推定器を用いた、あるベースラインのオフライン評価設定による実験セルの相対順序を示す。
Since the cap is so high, this is similar to an un-capped estimate.
キャップが高いので、キャップなしの見積もりと同様です。
We note the following:
以下のように注意します：

- (1) The ordering of experiments differs substantially from the online experiment. The Kendall’s τ rank correlation between the two is 0.424. This is not statistically significant, which means we cannot rule out the possibility that the offline evaluation is just ordering experiments randomly. (1) 実験の順序がオンライン実験と大きく異なる。 両者のKendall's τ順位相関は0.424であった。 これは統計的に有意ではないので、オフライン評価で実験をランダムに発注しているだけの可能性も否定できません。

- (2) Sample size is identical for every experiment. This is because each experiment is evaluated using the same offline data. (2)サンプルサイズは、すべての実験において同一である。 これは、各実験が同じオフラインデータを使って評価されるためです。

- (3) Standard errors in this table are much higher than in Table 1: Table 1 reports standard errors ×105 , while this table reports them ×101—the latter are 104 times larger than the former! (3) 本表の標準誤差は、表1の標準誤差×105に対して、本表の標準誤差×101と、表1の標準誤差の104倍である！

- (4) Because the standard errors are so much higher, statistical significance signals are lost en masse. Thirty-seven pairs that were significantly different in the online evaluation are not significant in the offline evaluation. (4) 標準誤差が大きくなるため、統計的有意性のシグナルが一斉に失われてしまう。 オンライン評価で有意差があった37組が、オフライン評価では有意差がない。

- (5) The best experiment by the online evaluation—experiment 12—is only 4th-best by the offline evaluation, and is statistically indistinguishable from the 5th-worst experiment. (5) オンライン評価で最も優れている実験12は、オフライン評価では4位であり、5位の実験と統計的に区別がつかない。

- (6) The best experiment by the offline evaluation—experiment 4—is 4th-worst by the online evaluation. (6) オフライン評価で最も優れていた実験4が、オンライン評価ではワースト4となった。

Table 2 represents one possible case for the offline evaluation with de-biased data.
表2は、偏りのないデータを用いてオフラインで評価する場合に考えられるケースを示したものである。
Table 3, with λ = 100 and no normalization, represents something close to a worst-case scenario.
表3は、λ=100で正規化しない場合、最悪のシナリオに近いものを表しています。
The ranking is inaccurate (Kendall’s tau correlation of 0.333), the best experiment by the online gold standard is ranked in the middle, and the fourth-worst experiment is ranked highest.
ランキングは不正確で（ケンドールのタウ相関0.333）、オンラインゴールドスタンダードによるベストの実験が中間に位置し、ワースト4位の実験が最高位に位置しています。
Yet the confidence in results is high: most pairs are thought to be statistically significantly different from one another.
しかし、結果の信頼度は高く、ほとんどのペアが統計的に有意な差があると考えられています。
Table 4, with normalization and λ = 105 , represents a much better outcome.
表4は、正規化し、λ=105としたもので、より良い結果を示している。
The ranking is more accurate (Kendall’s tau of 0.636, which is significant), and moreover the best two experiments are ranked in the top two positions.
ランキングはより正確で（Kendallのタウは0.636で有意）、しかもベスト2の実験が上位2位にランクインしています。
The confidence in results is much lower as well; if we can believe that the 11th experiment could be the best, experiments 10, 3, 9, 6, 8, and 12 are all within the confidence interval of experiment 11 and thus could have a claim to being the best as well.
11番目の実験がベストだと信じられるなら、10、3、9、6、8、12はすべて11番目の実験の信頼区間内にあり、ベストだと主張することができるだろう。
This group contains the actual 5 best experiments, though it also contains one clear miss (experiment 3).
このグループには、実際のベスト5の実験が含まれていますが、明らかに失敗した実験も含まれています（実験3）。
Counterintuitively, the lower confidence (represented by wider confidence intervals) gives us greater confidence that this offline evaluation is providing results that are usable.
逆に言えば、信頼度が低いほど（信頼区間が広いほど）、このオフライン評価が使える結果を出しているという確信が持てるのです。

Figures 3a and 3b show Table 3 and 4 (respectively) as scatterplots.
図3a、3bは、表3、表4（それぞれ）を散布図として示したものです。
The discrepancies in ordering from the former evaluation are easy to see, as are the narrow confidence intervals that make nearly every pair look significantly different.
前者の評価では、順序のズレがわかりやすく、また信頼区間が狭いため、ほぼすべてのペアが大きく異なるように見えます。
In contrast, the latter evaluation clearly indicates the uncertainty present from evaluating offline, suggesting immediately which experiments are in contention.
一方、後者の評価では、オフラインでの評価による不確実性が明確に示され、どの実験が競合しているかが一目瞭然です。

It is important to understand the interpretation of the confidence bars in these figures.
この図の信頼棒の解釈を理解することが重要である。
Note in the right figure that the confidence intervals for experiment 2 and experiment 6 overlap by a small amount, but in Table 4, experiment 2 is statistically significantly worse than experiment 6.
右の図では、実験2と実験6の信頼区間が少し重なっていますが、表4では、実験2は実験6より統計的に有意に悪いことに注意してください。
This is because non-overlapping confidence intervals is a sufficient but not necessary condition for statistical significance.
信頼区間が重なっていないことは、統計的有意性の十分条件ではあるが、必要条件ではないからである。
In the offline case, the sample data is the same for both experiments, which means we can use a one-sample (paired) test.
オフラインの場合、サンプルデータは両実験とも同じなので、1標本（ペア）検定を使うことができます。
This means that the confidence interval used for statistical testing is the confidence interval on the difference in means, not the intervals on the means themselves.
つまり、統計的検定に用いる信頼区間は、平均値の差に対する信頼区間であり、平均値そのものに対する区間ではないのです。
It is certainly possible that two confidence intervals on means could be overlapping, yet the confidence interval on the difference in means does not contain 0.
平均値に関する2つの信頼区間が重なっていても、平均値の差に関する信頼区間に0が含まれないということは確かにあり得る。

### Offline evaluation with shuffled data. シャッフルされたデータを用いてオフラインで評価。

We also wanted to try to verify the use of fully-shuffled data for offline evaluation.
また、フルシャッフルしたデータをオフラインで評価する際の検証も試みたいと考えていました。
Table 5 shows the relative ordering of experiments by an evaluation over fully-shuffled logs only, with theVIS estimator with no capping and no normalization.
表5は、完全シャッフルされたログのみを対象に、キャッピングなし、正規化なしのVIS推定方式で評価した実験の相対的な順序を示している。
The sample size in this case is quite small: only 6,285 sessions that had at least one user impression.
この場合のサンプルサイズは非常に小さく、少なくとも1回のユーザーインプレッションがあったセッションは6,285回のみです。
As a result the variance is much higher than the online case.
その結果、分散はオンラインの場合よりはるかに大きくなります。
Note that the standard errors shown in this table are three orders of magnitude larger than those in Table 1.
なお、この表で示された標準誤差は、表1のものと比べて3桁も大きい。
This translates to fewer experiment pairs being found statistically significantly different: 20 pairs that had been statistically significantly different in the online evaluation are no longer significant (by a one-sample t-test).
オンライン評価で統計的に有意な差があった20組が有意でなくなった（1標本t検定による）。

The ranking of experiments is also substantially different.
また、実験の順位も大幅に異なっています。
The best system and the 7th-best system by the online evaluation swap positions so that the 7th-best is ranked best by the offline evaluation.
オンライン評価でベストのシステムと7位のシステムの位置が入れ替わり、オフライン評価では7位のシステムがベストとなります。
The Kendall’s τ rank correlation between the two is only 0.3943 .
両者のKendallのτ順位相関は0.3943に過ぎない。
This is not statistically significant, which means that we cannot rule out that the offline evaluation is just producing a random shuffling of experiments.
これは統計的に有意ではなく、オフライン評価では実験のランダムなシャッフルが発生しているだけと断定できないことを意味する。

Figure 3c compares the online and offline evaluation with shuffled logs.
図3cは、ログをシャッフルした状態でオンラインとオフラインの評価を比較したものです。
It is evident from the plot that the correlation is not very strong, and moreover the error bars do not give us much confidence that more data would improve the result.
プロットから明らかなように、相関はあまり強くなく、しかもエラーバーは、より多くのデータによって結果が改善されるという確信を与えるものではありません。

## Deciding on systems to test online オンラインでテストするシステムを決定する

In this section we use the simulation-based policy described in Section 3.3 to identify the systems with highest probability of providing good online results.
このセクションでは、セクション3.3で説明したシミュレーションベースのポリシーを使用して、良いオンライン結果を提供する確率が最も高いシステムを特定します。
We sample from the multivariate normal distribution fit to offline evaluation results, then transform the resulting simulated means to rank positions.
オフライン評価結果に適合する多変量正規分布からサンプリングし、得られたシミュレーション平均値を順位に変換します。

Figure 4 shows the probability that each system is identified as the “best” over 100,000 simulations of an offline evaluation.
図4は、オフライン評価で10万回のシミュレーションを行い、各システムが「ベスト」と認定される確率を示したものです。
The left plot is with no normalization; the right plot uses normalization.
左のプロットは正規化なし、右のプロットは正規化を使用したものです。
Both plots have as their x-axis the log10 of the value used for capping propensities.
どちらのプロットも、キャッピングプロペンスに使用した値のlog10をX軸としています。
The assignment of point types to experiments is identical to Figure 3.
ポイントタイプの実験への割り当ては、図3と同じです。

Figure 4 clearly shows the importance of normalization.
図4は、正規化の重要性を明確に示しています。
Without it, only experiments 4, 10, and 11 are ever in contention.
これがないと、実験4、10、11しか候補に挙がらない。
The actual best experiment—experiment 12—never exceeds 0.01 probability of being identified as best.
実際に最良の実験である実験12が、最良と認定される確率が0.01を超えることはない。
The right plot, with normalization, shows more variety.
右のプロットは正規化したもので、よりバラエティに富んでいることがわかる。
With low cap values, experiment 7 is favored, but experiment 11 (the second best overall) quickly rises and remains most likely to be identified as best for cap ≥ 1.
キャップ値が低い場合は、実験7が有利ですが、実験11（全体で2番目に良い）はすぐに上昇し、キャップ≧1で最も良いものとして識別される可能性が残っています。
As cap increases over 10,000, experiment 12 (the actual best) takes some of the probability mass along with experiments 8 and 6.
capが10,000を超えると、実験12（実際のベスト）は、実験8と実験6とともに確率の塊の一部を占めるようになります。

Note that Figure 4 is only showing the probability of each experiment being identified as best.
なお、図4はあくまで各実験がベストと認定される確率を示したものである。
We could also look at distributions for second- and third-best.
また、セカンドベスト、サードベストの分布も見ることができる。
Figure 5 shows plots for the second- and third-best experiments.
図5は、セカンドベストとサードベストの実験のプロットである。
For second-best, at high cap values we have experiments 6, 8, 11, and 12 in contention.
セカンドベストでは、高いキャップ値では、実験6、8、11、12が競合しています。
For third-best, experiments 8, 12, 6, 11, 9, 3, and 1 0 are in contention.
第3位以下は、実験8、12、6、11、9、3、1 0が競合している。
Though we do note that there is not a very high probability of the actual third-best experiment ranking third or higher in an offline evaluation.
ただし、実際のサードベストの実験がオフラインの評価で3位以上になる確率はあまり高くないことに留意しています。

## System components and characteristics システムの構成と特徴

In Section 4.1 we noted that our 12 experiments used two different feature sets and three different sources of training data.
セクション4.1では、12回の実験で2つの異なる特徴セットと3つの異なる学習データソースを使用したことに言及した。
In this section we investigate whether we can reliably identify the best feature set and the best source of training data separately from the experimental systems.
このセクションでは、実験システムとは別に、最適な特徴セットと最適なトレーニングデータのソースを確実に特定できるかどうかを調査します。

The specific groupings are as follows:
具体的なグループ分けは以下の通りです：

- feature set 1: experiments 1, 2, 4, 11, and 12. 特徴セット1：実験1、2、4、11、12。

- feature set 2: experiments 3, 5, 6, 7, 8, 9, and 10. 特徴セット2：実験3、5、6、7、8、9、10。

- trained on biased data: experiments 1 and 11. 偏ったデータで学習させた：実験1、11。

- trained on shuffled data: experiments 3, 7, 8, and 10. シャッフルされたデータで訓練された：実験3、7、8、10。

- trained on de-biased (by NCIS) data: experiments 2, 4, 5, 6, 9, and 12. 非バイアス（NCISによる）データで訓練された：実験2、4、5、6、9、および12。

To try to predict which feature set or which source of training data is best, we use the same method as above, but collapse predictions by grouping samples by either feature set or training data source.
どの機能セットやトレーニングデータのソースが最適かを予測するために、上記と同じ方法を使いますが、機能セットやトレーニングデータのソースのいずれかによってサンプルをグループ化することで予測を崩すことができます。

The result for feature set is that there is a 59% chance that the first feature set is better than the second.It is not surprising that this result is uncertain, given that both the two best and two worst experiments used the first feature set.
ベストとワーストの2つの実験がともに最初の特徴セットを使っていることを考えると、この結果が不確実であることは驚くことではありません。

For training data source the result is clear.
トレーニング用データソースについては、明確な結果が得られています。
There is a 97% chance that using production log data de-biased by NCIS is the best source of training data, and only a 0.01% chance that the fully-shuffled data is.
NCISによってバイアス除去されたプロダクションログデータを使用することが最適なトレーニングデータのソースである可能性は97％で、完全にシャッフルされたデータがそうである可能性は0.01％だけです。
Of course, this is likely because the amount of fully-shuffled data is very small, as it must be due to the risk of degrading the user experience.
もちろん、これはユーザーエクスペリエンスを低下させる危険性があるため、完全シャッフルされたデータ量が非常に少ないからだと思われます。

# Conclusion 結論

We have presented a comparison and analysis of an online evaluation via A/B tests and offline evaluation with three different estimators computed from historical log data.
A/Bテストによるオンライン評価と、過去のログデータから算出した3種類の推定値によるオフライン評価の比較と分析を紹介しました。
Taking the online evaluation as the gold standard, we find best results in an offline evaluation using a normalized and capped estimator based on importance sampling, with a relatively high capping parameter providing the best tradeoff between variance and preserving the relative ordering of experiments.
オンライン評価をゴールドスタンダードとし、オフライン評価では、重要度サンプリングに基づく正規化・キャップ化された推定量を用い、比較的高いキャップ化パラメータにより、分散と実験の相対的順序の保持との間の最良のトレードオフが得られることを発見した。
We are thus able to use offline evaluation to predict the results of online evaluation more accurately than previous work.
このように、オフライン評価を用いて、オンライン評価の結果を従来よりも正確に予測することができるようになりました。

Our analysis illustrates that problems arising from both bias and variance in offline estimators are mitigated by the practical considerations of identifying the right experiments to A/B test and failing to miss good experiments.
我々の分析では、オフラインの推定器のバイアスと分散の両方から生じる問題は、A/Bテストに適した実験を特定し、良い実験を見逃さないという実用的な考慮によって軽減されることが示されています。
Variance may be high for the offline estimator of an individual experiment, but because the practical concern is whether one experiment is better than another and by how much, the variance we are more concerned with is the variance in the difference in the estimator.
分散は、個々の実験のオフラインの推定値では高いかもしれないが、現実的な関心事は、ある実験が他の実験より優れているかどうか、どのくらい優れているかであるので、我々がより関心を持つ分散は、推定値の差の分散である。
And because the two experiments are evaluated using the same sample, that variance is typically lower than the variance of either of the experiments separately.
そして、2つの実験は同じサンプルを使って評価されるため、その分散は通常、どちらかの実験を別々に行った場合の分散よりも低くなります。
Similarly, while capping and normalization may add bias to the estimator, as long as the bias does not affect the relative ordering of experiments it can be acceptable.
同様に、キャッピングや正規化によって推定値にバイアスがかかることがありますが、バイアスが実験の相対的な順序に影響を与えない限りは許容範囲となります。

It is worth discussing particular aspects of our problem setting that may help make the prediction of online test results easier.
オンラインテストの結果予測を容易にするために、今回の問題設定の特定の側面について議論する価値がある。
For one, the action space we are considering is relatively small—200 cards—compared to other settings.
ひとつは、今回検討しているアクションスペースが、他の設定と比較して200枚と比較的小さいことです。
For another, we are assuming independent rewards, which is likely not the case in reality: the expected reward of placing one card after another may depend highly on which card is placed first.
もうひとつは、独立した報酬を想定しているため、現実にはそうでない可能性が高いことです。あるカードを次に置いたときの期待報酬は、どのカードを先に置いたかに大きく依存する可能性があります。
This may also explain some of the discrepancy between the online and offline results.
これは、オンラインとオフラインの結果の不一致の一部を説明するものでもあります。

There are a number of directions for future work.
今後の課題として、様々な方向性があります。
Gilotte et al.proposed additional refinements to the NCIS estimator they call piecewise and pointwise NCIS.
Gilotteらは、NCIS推定器をさらに改良し、piecewiseおよびpointwise NCISと呼ぶことを提案した。
We believe these can be refined further and adapted to our problem.
これらをさらに改良し、我々の問題に適応させることができると考えています。
There is also potential for exploring rank loss functions and metrics.
また、ランク損失関数やメトリクスの探求の可能性もあります。
Finally, we plan to perform this analysis on offline-to-online prediction for other recommendation problems.
最後に、この分析を他の推薦問題に対するオフラインからオンラインへの予測について行う予定である。