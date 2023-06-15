## link リンク

https://analyticsindiamag.com/how-to-measure-the-success-of-a-recommendation-system/
https://analyticsindiamag.com/how-to-measure-the-success-of-a-recommendation-system/

## title タイトル

How to Measure the Success of a Recommendation System?
レコメンデーションシステムの成功度を測るには？

## Intro Intro

Recommender systems are used in a variety of domains, from e-commerce to social media to offer personalized recommendations to customers.
レコメンダーシステムは、電子商取引からソーシャルメディアまで、さまざまな領域で使用され、顧客にパーソナライズされた推奨を提供しています。
The benefit of recommendations for customers, such as reduced information overload, has been a hot topic of research.
情報過多の軽減など、レコメンデーションがお客様にもたらすメリットは、これまでも研究テーマとして注目されてきました。
However, it’s unclear how and to what extent recommender systems produce commercial value.
しかし、レコメンダーシステムがどのように、どの程度商業的価値を生み出すかは不明である。
It’s challenging to create a reliable product suggestion system.
信頼性の高い商品提案の仕組みを作るのは、難しいですね。
However, defining what it means to be reliable is also a challenging task.
しかし、「信頼できる」とはどういうことなのかを定義することは、難しい課題でもあります。
Measuring the success of any recommender system is very necessary from a business point of view.
推薦システムの成功度を測ることは、ビジネスの観点からも非常に必要なことです。
In this post, we go through the most important and popularly used evaluation parameters to measure the success of a recommendation system.
この記事では、推薦システムの成功を測るために最も重要かつ一般的に使用されている評価パラメータについて説明します。
The major points to be discussed in this article are outlined below.
今回取り上げる主なポイントは、以下の通りです。

## Table of Contents 目次

- Challenges Faced by Recommendation Systems レコメンデーションシステムが直面する課題

- Common metrics used よく使われる指標

- Business Specific Measures 事業別施策

Let’s start the discussion by understanding the challenges that are faced by recommendation systems.
まずは、レコメンデーションシステムが抱える課題を理解することから始めましょう。

# Challenges Faced by Recommendation Systems レコメンデーションシステムが直面する課題

Any predictive model or recommendation systems with no exception rely heavily on data.
予測モデルやレコメンデーションシステムも例外ではなく、データに大きく依存しています。
They make reliable recommendations based on the facts that they have.
彼らは、自分たちが持っている事実に基づいて、信頼できる提案をします。
It’s only natural that the finest recommender systems come from organizations with large volumes of data, such as Google, Amazon, Netflix, or Spotify.
Google、Amazon、Netflix、Spotifyなど、大量のデータを持つ組織から優れたレコメンダーシステムが生まれるのは自然なことです。
To detect commonalities and suggest items, good recommender systems evaluate item data and client behavioral data.
共通点を発見してアイテムを提案するために、優れたレコメンダーシステムはアイテムデータとクライアントの行動データを評価します。
Machine learning thrives on data; the more data the system has, the better the results will be.
機械学習は、データがあればあるほど、より良い結果が得られます。

Data is constantly changing, as are user preferences, and your business is constantly changing.
データは常に変化し、ユーザーの嗜好も変化し、あなたのビジネスも常に変化しています。
That’s a lot of new information.
新しい情報が多いですね。
Will your algorithm be able to keep up with the changes? Of course, real-time recommendations based on the most recent data are possible, but they are also more difficult to maintain.
アルゴリズムは変化についていけるのか？もちろん、最新のデータに基づくリアルタイムのレコメンデーションは可能ですが、維持するのが難しくなります。
Batch processing, on the other hand, is easier to manage but does not reflect recent data changes.
一方、バッチ処理は管理が簡単ですが、最近のデータの変化を反映することができません。

The recommender system should continue to improve as time goes on.
レコメンダーシステムは、時間が経てば経つほど、改良を続けていくはずです。
Machine learning techniques assist the system in “learning” the patterns, but the system still requires instruction to give appropriate results.
機械学習の技術は、システムがパターンを「学習」することを支援しますが、適切な結果を出すためには、システムによる指示が必要です。
You must improve it and ensure that whatever adjustments you make continue to move you closer to your business goal.
それを改善し、どのような調整でもビジネス目標に近づき続けるようにしなければなりません。

# Common Metrics Used よく使われる指標

Predictive accuracy metrics, classification accuracy metrics, rank accuracy metrics, and non-accuracy measurements are the four major types of evaluation metrics for recommender systems.
レコメンダーシステムの評価指標として、予測精度指標、分類精度指標、順位精度指標、非精密度指標が大きく4種類あります。

## Predictive Accuracy Metrics 予測精度の指標

Predictive accuracy or rating prediction measures address the subject of how near a recommender’s estimated ratings are to genuine user ratings.
予測精度や評価予測指標は、レコメンダーの推定評価が本物のユーザー評価にどれだけ近いかというテーマに取り組むものです。
This sort of measure is widely used for evaluating non-binary ratings.
この種の指標は、二値でない評価のために広く使われている。

It is best suited for usage scenarios in which accurate prediction of ratings for all products is critical.
全商品の評価を正確に予測することが重要な利用シーンに最適です。
Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and Normalized Mean Absolute Error (NMAE) are the most important measures for this purpose.
平均絶対誤差（MAE）、平均二乗誤差（MSE）、ルート平均二乗誤差（RMSE）、正規化平均絶対誤差（NMAE）がこの目的のための最も重要な尺度です。

In comparison to the MAE metric, MSE and RMSE employ squared deviations and consequently emphasize bigger errors.
MSEとRMSEは、MAEと比較して、偏差の二乗を採用しているため、より大きな誤差を強調することができます。
The error is described by MAE and RMSE in the same units as the obtained data, whereas MSE produces squared units.
誤差は、MAEやRMSEが得られたデータと同じ単位で表現するのに対し、MSEは2乗単位を出す。

To make results comparable among recommenders with different rating scales, NMAE normalizes the MAE measure to the range of the appropriate rating scale.
異なる評価尺度を持つ推薦者間で結果を比較できるように、NMAEはMAE尺度を適切な評価尺度の範囲に正規化します。
In the Netflix competition, the RMSE measure was utilized to determine the improvement in comparison to the Cinematch algorithm, as well as the prize winner.
Netflixのコンペティションでは、Cinematchアルゴリズムとの比較で改善度を判断するためにRMSE尺度が利用され、賞の受賞も決定されました。

## Classification Accuracy Metrics 分類精度の指標

Classification accuracy measures attempt to evaluate a recommendation algorithm’s successful decision-making capacity (SDMC).
分類精度の測定は、推薦アルゴリズムの成功した意思決定能力（SDMC）を評価しようとするものである。
They are useful for user tasks such as identifying nice products since they assess the number of right and wrong classifications as relevant or irrelevant things generated by the recommender system.
レコメンダーシステムが生成した、関連するもの、関連しないものという分類の正誤数を評価するため、素敵な商品を特定するようなユーザータスクに有用である。

The exact rating or ranking of objects is ignored by SDMC measures, which simply quantify correct or erroneous classification.
SDMCの測定では、オブジェクトの正確な評価やランキングは無視され、分類の正誤が単純に数値化されます。
This type of measure is particularly well suited to e-commerce systems that attempt to persuade users to take certain actions, such as purchasing products or services.
特に、商品やサービスの購入など、ユーザーを説得して特定の行動を起こさせようとするEコマースシステムに適した施策です。

## Rank Accuracy Metrics ランク精度の指標

In statistics, a rank accuracy or ranking prediction metric assesses a recommender’s ability to estimate the correct order of items based on the user’s preferences, which is known as rank correlation measurement.
統計学では、順位精度または順位予測指標は、ユーザーの好みに基づいてアイテムの正しい順序を推定する推薦者の能力を評価するものであり、順位相関測定として知られています。
As a result, if the user is given a long, sorted list of goods that are recommended to him, this type of measure is most appropriate.
その結果、ユーザーにお勧めするグッズを長いソートされたリストで提供する場合、このタイプの施策が最も適していると言えます。

The relative ordering of preference values is used in a rank prediction metric, which is independent of the exact values assessed by a recommender.
嗜好値の相対的な順序は、レコメンダーが評価する正確な値とは独立した順位予測指標に使用されます。
A recommender that consistently overestimates item ratings to be lower than genuine user preferences, for example, might still get a perfect score as long as the ranking is correct.
例えば、アイテムの評価を常に過大評価し、本物のユーザーの好みよりも低くしてしまうレコメンダーは、ランキングが正しい限り、満点を取ることができるかもしれません。

Mean Average Precision @ K and Mean Average Recall @ K
平均平均Precision @ Kおよび平均Recall @ K

For each user in the test set, a recommender system normally generates an ordered list of recommendations.
テストセットの各ユーザーに対して、レコメンダーシステムは通常、レコメンデーションの順序付きリストを生成する。
MAP@K indicates how relevant the list of recommended items is, whereas MAR@K indicates how well the recommender can recall all of the items in the test set that the user has rated positively.
MAP@Kは、推奨アイテムのリストがどれだけ関連性があるかを示し、MAR@Kは、推奨者がテストセットの中でユーザーが肯定的に評価したアイテムすべてをどれだけ思い出すことができるかを示します。

# Business Specific Measures 事業別施策

The way businesses evaluate the effects and business value of a deployed recommender system is influenced by a number of factors, including the application domain and, more crucially, the company’s business strategy.
企業が導入したレコメンダーシステムの効果やビジネス価値を評価する方法は、アプリケーションドメインや、より重要な企業のビジネス戦略など、さまざまな要因に影響されます。
Ads can be used in part or entirely to support such business strategies (e.g., YouTube or news aggregation sites).
広告は、そのようなビジネス戦略（YouTubeやニュースアグリゲーションサイトなど）の一部または全部をサポートするために使用することができます。
The goal in this scenario could be to increase the amount of time people spend using the service.
このシナリオでは、人々がサービスを利用する時間を増やすことを目標にすることができます。
Increased engagement is also a goal for firms with an at-rate subscription model (e.g., music streaming services).
エンゲージメントの向上は、定額制のサブスクリプションモデルを持つ企業（例：音楽ストリーミングサービス）の目標でもあります。

The underlying business models and objectives govern how firms judge the value of a recommender in all of the examples above.
上記のすべての例において、企業がレコメンダーの価値をどのように判断するかは、基本的なビジネスモデルと目標が支配している。
The diagram below depicts the basic measuring methodologies identified in the literature, which we are going to discuss further one by one.
下図は、文献で確認された基本的な測定方法を描いたもので、これからさらに一つずつ解説していきます。

## Click-Through Rates 

The click-through rate (CTR) is a metric that measures how many people click on the recommendations.
クリックスルー率（CTR）は、おすすめ商品を何人がクリックしたかを示す指標です。
The basic notion is that if more people click on the recommended things, the recommendations are more relevant to them.
基本的な考え方は、より多くの人が推奨されるものをクリックすれば、推奨されるものがよりその人に関連したものになるというものです。

In news recommendations, the CTR is a widely used metric.
ニュースレコメンデーションでは、CTRが広く使われている指標です。
Das et al.discovered that personalized suggestions resulted in a 38 percent increase in clicks compared to a baseline that merely recommends popular articles in an early paper on Google’s news personalization engine.
Dasらは、Googleのニュースパーソナライゼーションエンジンに関する初期の論文で、パーソナライズされた提案によって、単に人気記事を推薦するベースラインと比較して、クリック数が38％増加することを発見しました。
However, on some days, when there was a lot of attention to celebrity news, the baseline actually fared better.
しかし、有名人のニュースが注目された日には、実はベースラインの方が成績が良かったということもありました。

## Adoption and Conversion Adoption and Conversion

Click-through rates are often not the final success measure to pursue in recommendation scenarios, unlike online business models dependent on adverts.
レコメンデーションシナリオでは、広告に依存するオンラインビジネスモデルとは異なり、クリックスルー率が最終的な成功指標にならないことが多い。
While the CTR can measure user attention or interest, it can’t tell you whether users liked the recommended news article they clicked on or if they bought something based on a recommendation.
CTRはユーザーの注目度や関心度を測ることができますが、ユーザーがクリックしたおすすめのニュース記事を気に入ったかどうか、おすすめをもとに何かを購入したかどうかはわかりません。

As a result, alternative adoption measures are frequently utilized, which are ostensibly more suited to determining the effectiveness of the suggestions and are ostensibly based on domain-specific considerations.
その結果、表向きは提案の効果を判断するのに適しており、表向きはドメイン固有の考慮事項に基づく代替的な採用指標が頻繁に利用されるようになりました。
YouTube employs the idea of “long CTRs,” in which a user’s clicks on suggestions are only tallied if they view a particular percentage of a video.
YouTubeでは、ユーザーが動画の特定の割合を視聴した場合にのみサジェストのクリック数が集計される「ロングCTR」という考え方が採用されています。
Similarly, Netix utilizes a metric called “take-rate” to determine how many times a video or movie was actually watched after being recommended.
同様に、Netixでは「テイクレート」と呼ばれる指標を利用して、動画や映画が推奨された後、実際に何回視聴されたかを判断しています。

## Salves and Revenue Salves and Revenue

In many cases, the adoption and conversion measures outlined in the previous section are more telling of a recommender’s prospective business value than CTR measures alone.
多くの場合、前節で説明した採用率やコンバージョンの指標は、CTRの指標だけよりも、レコメンダーの将来のビジネス価値を示すものである。
When customers choose more than one item from a list of suggestions, This is a good indicator that a new algorithm was successful in identifying later purchases or views.
顧客が提案されたリストから複数のアイテムを選択した場合、これは新しいアルゴリズムが後の購入や閲覧を特定するのに成功したことを示す良い指標となります。
stuff that the user is interested in.
ユーザーが興味を持っているものを

Nonetheless, determining how such improvements in adoption translate into greater business value remains difficult.
しかし、このような採用率の向上が、どのようにビジネス価値の向上につながるかを判断することは、依然として困難です。
Because a recommender may provide numerous suggestions to consumers that they would buy otherwise, the rise in company value may be lower than what we can expect based on adoption rate increases alone.
レコメンダーは、消費者がそうでなければ購入しないような提案を数多く行う可能性があるため、企業価値の上昇は、採用率の上昇だけで期待できるものよりも低くなる可能性があります。
Furthermore, if the relevance of suggestions was already poor, i.e., nearly no one clicked on them, raising the adoption rate by 100% could result in very little absolute additional value for the company.
さらに、提案の関連性がすでに低く、ほとんど誰もクリックしなかった場合、採用率を100％上げても、企業にとっての付加価値の絶対値はほとんどない。

## User Behavior and Engagement ユーザーの行動とエンゲージメント

Higher levels of user engagement are thought to contribute to increased levels of user retention in various application domains, such as video streaming, which, in turn, often immediately converts into corporate value.
動画配信をはじめとする様々なアプリケーション領域において、ユーザーエンゲージメントが高まれば、ユーザーリテンションが向上し、それが即座に企業価値に結びつくことが多いと考えられています。
A number of real-world tests of recommender systems have found that having a recommender increases user activity.
レコメンダーシステムの実際のテストでは、レコメンダーがあることでユーザーのアクティビティが向上することが多数確認されています。
Depending on the application domain, different measurements are used.
アプリケーションのドメインによって、異なる測定値が使用されます。

In the field of music recommendation, researchers compared various recommendation strategies and discovered that a recommendation strategy that combines usage and content data (dubbed Mix) not only led to higher acceptance rates but also to a 50% higher level of activity in terms of playlist additions than the individual strategies.
音楽推薦の分野では、様々な推薦戦略を比較した結果、利用状況とコンテンツデータを組み合わせた推薦戦略（Mixと命名）は、個々の戦略に比べて、受容率が高いだけでなく、プレイリスト追加という活動レベルも50％高くなることがわかりました。

Overall, the use of a specific measure is not limited; it just depends on the type of business problem that the system is being used to solve.
全体として、特定の尺度の使用は制限されるものではなく、そのシステムがどのようなビジネス上の問題を解決するために使用されるかに依存するだけです。
An overview of some of our findings may be found in the table below.
調査結果の概要は、以下の表のとおりです。

Apart from all of this, we can also leverage our standard ML evaluation metrics to evaluate ratings and predictions that are as follows.
これとは別に、標準的なMLの評価指標を活用して、以下のような評価や予測を行うことも可能です。

- Precision 精密

- Recall リコール

- F1-measure F1メジャー

- False-positive rate 偽陽性率（False-positive rate

- Mean average precision 平均平均精度

- Mean absolute error 平均絶対誤差

- The area under the ROC curve (AUC) ROC曲線下面積(AUC)

# Conclusion 結論

Through this post, we have learned what different metrics are used when it comes to evaluating the performance of a recommendation system.
この記事を通じて、推薦システムの性能を評価する際に、どのような異なる指標が用いられるかを学びました。
Firstly we have seen what are some common challenges that are involved with the recommendation system.
まず、推薦システムに関わる一般的な課題にはどのようなものがあるのかを見てきました。
Later we have seen some commonly used performance metrics and lastly, we have seen how well established businesses like Netflix, YouTube have defined these evaluation strategies.
そして最後に、NetflixやYouTubeのような優れた企業が、どのように評価戦略を定めているのかを見てきました。

References
参考文献

- Measuring the Business Value of Recommender Systems レコメンダーシステムのビジネス価値を測定する

- Choosing Metrics for Recommender System Evaluations リコメンダーシステム評価のための評価指標の選択
