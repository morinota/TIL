## 0.1. link

- https://dl.acm.org/doi/10.1145/3523227.3547393

## 0.2. title タイトル

Optimizing product recommendations for millions of merchants
何百万もの販売店への商品推奨の最適化

## 0.3. abstruct abstruct

At Shopify, we serve product recommendations to customers across millions of merchants’ online stores.
Shopifyでは、何百万ものマーチャントのオンラインストアで、お客様に商品のレコメンデーションを提供しています。
It is a challenge to provide optimized recommendations to all of these independent merchants; one model might lead to an overall improvement in our metrics on aggregate, but significantly degrade recommendations for some stores.
あるモデルが**全体的な指標を向上させたとしても、一部の店舗ではレコメンデーションを大幅に悪化させる可能性**があります。
To ensure we provide high quality recommendations to all merchant segments, we develop several models that work best in different situations as determined in offline evaluation.
このため、オフライン評価で決定された様々な状況下で最適なレコメンデーションを提供できるよう、複数のモデルを開発しました。
Learning which strategy best works for a given segment also allows us to start off new stores with good recommendations, without necessarily needing to rely on an individual store amassing large amounts of traffic.
また、**特定のセグメントに対してどの戦略が最も効果的か**を学習することで、必ずしも個々の店舗が大量のトラフィックを蓄積することに依存する必要なく、新しい店舗に良いレコメンデーションを開始することができるようになりました。
In production, the system will start out with the best strategy for a given merchant, and then adjust to the current environment using multi-armed bandits.
本番では、システムはまず特定の商材に最適な戦略でスタートし、その後マルチアームドバンディットを用いて現在の環境に適応していきます。
Collectively, this methodology allows us to optimize the types of recommendations served on each store.
この方法論により、各店舗で提供されるレコメンデーションの種類を最適化することができます。

# 1. Introduction はじめに

Building a good product recommendation system for an e-commerce site is challenging.
Eコマースサイトに優れた商品推薦システムを構築することは困難です。
What about building millions of them?
しかし、それを何百万個も作るとなるとどうでしょう？
Shopify powers millions of diverse businesses, from small artisanal mom and pop shops, to large established businesses.
Shopifyは、職人気質の小さなショップから、大規模な老舗まで、何百万もの多様なビジネスを支援しています。
These businesses span a wide range of industries, including apparel, electronics, house wares, food and drink, etc., and similarly have diverse customer bases and behavior.
これらのビジネスは、アパレル、家電、家庭用品、食品、飲料など、幅広い業界にまたがっており、同様に、顧客基盤や行動も多様化しています。
These merchants are also located in over 175 different countries.
また、これらのマーチャントは175カ国以上に存在しています。
While Shopify is the platform powering these stores, each merchant’s storefront is a standalone website, customized to suit their brand and preferences.
Shopifyはこれらの店舗を支えるプラットフォームですが、各商業者の店舗は独立したWebサイトであり、それぞれのブランドや好みに合わせてカスタマイズされています。
When we build recommender systems for Shopify’s merchants, we must consider the diversity of merchants and their needs to ensure that these systems will benefit all of them, rather than optimizing for only a small subset.
Shopifyの加盟店向けにレコメンダーシステムを構築する場合、一部の加盟店のみに最適化するのではなく、加盟店の多様性とそのニーズを考慮し、すべての加盟店にメリットがあるシステムを構築する必要があります。
Therefore while some companies may have a big data problem, at Shopify we instead have many small data problems!
そのため、ビッグデータの問題を抱えている企業もあるかもしれませんが、Shopifyでは、代わりに多くのスモールデータの問題を抱えています。

# 2. SEGMENT OPTIMIZATION セグメント最適化

We have developed a variety of product recommendation models using the rich signals available to us.
私たちは、豊富なシグナルを活用し、さまざまな商品推薦モデルを開発してきました。
These include content-based models that leverage product metadata, as well as models based on customer behavior.
その中には、商品のメタデータを活用したコンテンツベースのモデルや、顧客行動をベースとしたモデルなどがあります。
**Naturally, stores with more traffic will benefit from collaborative filtering models more so than stores with sparse user behavior data.当然ながら、ユーザーの行動データが乏しい店舗よりも、トラフィックが多い店舗の方が協調フィルタリングモデルの恩恵を受けることができる。**
Moreover, the type of products a merchant sells will affect the performance of each model on that merchant’s store. また、**どのような商品を販売しているか**によって、その店舗における各モデルの性能は異なります。
For example, a merchant selling large appliances may not benefit much from a collaborative filtering model that predicts frequently bought together products, but rather from a model whose intent is to showcase alternative similar products. 例えば、大型家電の販売店では、**よく一緒に購入される商品を予測する協調フィルタリングモデル**はあまり役に立たず、**むしろ類似の代替商品を紹介することを目的としたモデルの方が役に立つかも**しれません。

When evaluating the performance of a given model, it’s important to not only look at performance metrics in aggregate, but also examine performance for different segments of merchants.あるモデルの性能を評価する場合、性能指標を総合的に見るだけでなく、**異なるセグメントの加盟店に対する性能も調べることが重要**です。
It’s possible that a change to a model may improve predictions for one segment of merchants, while degrading them for another.**モデルを変更すると、あるセグメントの加盟店の予測は向上するが、別のセグメントの予測は低下するということ**があり得ます。
It is therefore not enough to look at one overall metric, but rather we must analyze changes carefully to ensure we understand their impact on all merchants, and ideally refrain from degrading performance for anyone. したがって、1つの全体的な指標を見るだけでは不十分で、変更を慎重に分析して、すべての加盟店に対する影響を理解し、理想的には誰に対してもパフォーマンスを低下させないようにする必要があります。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/m/m3tech/20221218/20221218110012.png)

Figure 1: Click-through rates for 3 different models across different merchant segments.
図1：異なるマーチャントセグメントにおける3種類のモデルのクリックスルー率。
Different models perform best for different segments.
異なるセグメントでは、異なるモデルが最適なパフォーマンスを発揮します。

Figure 1 illustrates the click-through rate of three models, compared between several merchant segments. 図1は、**3つのモデルのclick-through rate**を、いくつかのマーチャントセグメントで比較したものです。
One can note that different models perform best for different segments, as is indicated by different colored bars being higher for different segments. 異なるセグメントでは、異なる色のバーがより高いことを示しているように、**異なるモデルが異なるセグメントで最高のパフォーマンスを発揮している**ことがわかります。

One can also note that in this example, certain segments (e.g. segments F, K) do not have predictions from every model; this is due to some models having limited coverage. また、この例では、**特定のセグメント（セグメントF、Kなど）がすべてのモデルから予測されていないこと**に注目することができます。
This highlights the need for developing multiple models that rely on different types of available signals, rather than simply using the model which performs best on average. このことは、単に平均的に最も良い性能を示すモデルを使用するのではなく、利用可能なさまざまな種類の信号に依存する複数のモデルを開発する必要性を強調しています。

We can further combine one or more models to create a recommendation strategy.
さらに、1つまたは複数のモデルを組み合わせて、推薦戦略を作成することができる。
This strategy defines how to surface recommendations from different models to the user. この戦略では、異なるモデルからのレコメンデーションをどのようにユーザーに提示するかを定義します。
We optimize these strategies at a merchant segment level by analyzing the segment’s product content and customer engagement trends. 私たちは、セグメントの商品コンテンツと顧客エンゲージメントの傾向を分析することで、これらの戦略をマーチャントセグメントレベルで最適化します。
After determining the best strategy for a segment, we use it to generate recommendations for a given merchant. セグメントに最適な戦略を決定した後、その戦略を使用して、特定のマーチャントに対するレコメンデーションを生成します。
Knowing the best strategy for a segment also helps new merchants hit the ground running.
また、セグメントごとの最適な戦略を知ることで、新規参入のマーチャントもスムーズに対応できるようになります。

Since the strategies are created based on historical data, the analysis can become stale, resulting in sub-optimal configurations.
戦略は過去のデータに基づいて作成されるため、分析が古くなり、最適とは言えない構成になることがある。
We therefore see these strategies as bootstrapping for a multi-armed bandit framework [3] which continuously optimizes the strategy.
したがって、我々はこれらの戦略を、戦略を継続的に最適化する多腕バンディットフレームワーク[3]のブートストラップとして捉える。
We describe this in more detail in Section 4.
これについてはセクション4でより詳細に述べる。

# 3. A/B TESTING A

After evaluating our models offline and selecting candidate models that look promising, the next step is online evaluation.
オフラインでモデルを評価し、有望なモデル候補を選んだら、次はオンライン評価です。
We evaluate our models online by running A/B tests, in which each store’s traffic is split such that each customer is assigned to either a control or treatment group.
このテストでは、各店舗のトラフィックを分割し、各顧客をコントロールグループとトリートメントグループのいずれかに割り当てます。
The treatment group will be served recommendations from the model being evaluated, whereas control will receive recommendations from the previous baseline model.
トリートメントグループには、評価対象のモデルのレコメンデーションが配信され、コントロールグループには、以前のベースラインモデルのレコメンデーションが配信されます。
It’s helpful to split traffic for each store rather than assign a given store to one experiment group, in order to control for differences between stores.
店舗間の差異をコントロールするために、ある店舗を一つの実験グループに割り当てるのではなく、店舗ごとにトラフィックを分割することが有効である。
For example, each store’s layout is different, which affects customer behavior.
例えば、店舗ごとにレイアウトが異なるため、顧客の行動に影響を与える。
It’s also the case that key business metrics such as conversion rate and average order value vary greatly between stores, depending on the store’s business maturity, customer base, marketing campaigns, product catalog, and so on.
また、コンバージョン率や平均注文額などの主要なビジネス指標は、店舗のビジネスの成熟度、顧客層、マーケティングキャンペーン、商品カタログなどによって、店舗間で大きく異なるということもあります。
After running the experiment for a sufficient amount of time, we compute business metrics for the two experiment groups and test for statistical significance in order to establish a causal relationship between the new model and the observed business impact.
十分な期間実験を行った後、2つの実験グループのビジネス指標を計算し、統計的な有意性を検証することで、新しいモデルと観測されたビジネスインパクトの因果関係を確立します。

In our experience, running reliable A/B tests in a modern production setting is not as straightforward as one might expect [2]. There are many factors that must be accounted for when designing and analyzing the results of an A/B test: caching, novelty effects, redundant systems, and even adversarial users (bots). To help mitigate these effects and ensure that our testing framework is sound, it’s advisable to run an A/A test before starting to run regular A/B tests. An A/A test is a null test, in which we expect there to be no statistically significant differences between the two groups [2]. Running a successful A/A test can help ensure that we have accounted for all factors, and that results from the upcoming A/B tests can be trusted.
私たちの経験では、最新のプロダクション環境で信頼性の高いA/Bテストを実行することは、期待されるほど簡単ではありません[2]。A/Bテストを設計し、その結果を分析する際には、キャッシュ、新規性効果、冗長システム、さらには敵対するユーザー（ボット）など、考慮しなければならない要素がたくさんあります。これらの影響を軽減し、テストの枠組みが健全であることを確認するために、通常のA/Bテストの実行を開始する前にA/Aテストを実行することが推奨されます。A/Aテストとは、2つのグループの間に統計的に有意な差がないことを期待するヌルテストです[2]。A/Aテストを成功させることで、すべての要因を考慮し、これから行うA/Bテストの結果が信頼できるものであることを確認することができます。

# 4. MULTI-ARMED BANDITS ♪多腕の盗賊

While A bandit allows to both explore and exploit the problem space, in order to eventually surface recommendations from the best strategy while still exploring and collecting information about other strategies.
バンディットは問題空間の探索と開拓の両方を可能にし、他の戦略を探索し情報を収集しながら、最終的に最適な戦略から推薦を浮上させることを目的としている。
The system continuously updates each strategy’s performance based on the observed reward signals.
システムは観測された報酬信号に基づいて、各戦略の性能を継続的に更新する。
Whenever a new recommendation request arrives, the bandit will either explore or exploit with some probability based on its latest knowledge of the models’ performance.
新しい推薦要求が届くたびに、バンディットはモデルの性能に関する最新の知識に基づいて、ある確率で探索または開拓のいずれかを行う。

This bandit approach is particularly helpful in the Shopify context, since it allows us to learn and leverage the optimal strategy for a given segment, merchant, or perhaps even a specific product or page of a merchant’s store.
このバンディットアプローチはShopifyの文脈では特に有用で、特定のセグメント、マーチャント、あるいはマーチャントのストアの特定の製品やページに対する最適な戦略を学習し活用することができるからです。
For example, it’s reasonable that a customer shopping for a sofa would be interested in complementary pillows, whereas one who’s looking for pillows would be unlikely to impulsively add a sofa to their purchase.
例えば、ソファを購入する顧客が枕に興味を持つことは合理的ですが、枕を探している顧客が衝動的にソファを追加購入することはないでしょう。
In this case, the bandit would learn that different recommendation models are more suitable for certain pages of the store or to the customers’ contexts.
このような場合、バンディットは、店の特定のページや顧客の文脈に応じて、異なる推薦モデルがより適していることを学習することになる。

Finally, we can also analyze the optimal strategies obtained for each merchant as a way of better understanding our user segments and model improvement opportunities, which is helpful in iterating on the next generation of models and strategies.
最後に、各商材で得られた最適な戦略を分析することで、ユーザーセグメントやモデルの改善機会をより深く理解し、次世代モデルや戦略の反復に役立てることも可能です。

# 5. CONCLUSION 結論

Shopify has millions of diverse and unique merchants with different needs.
Shopifyには、多様でユニークなニーズを持つ数百万人のマーチャントがいます。
By leveraging the network effect and wealth of data available, we can provide optimized recommendations for each merchant.
ネットワーク効果や豊富なデータを活用することで、それぞれのマーチャントに最適なレコメンデーションを提供することができます。
Techniques such as segmentation, A
セグメンテーションなどのテクニック、A

# 6. PRESENTER BIO 発表者略歴

## 6.1. Kim Falk ♪キム・フォーク

Kim Falk is a Staff Recommender Engineer at Shopify, where he is the technical lead of the Product Recommendations team.
Kim Falk は Shopify の Staff Recommender Engineer で、Product Recommendations チームの技術リーダーを務めています。
Kim has experience in machine learning but is specialized in Recommender systems.
Kimは機械学習の経験がありますが、レコメンダーシステムを専門としています。
He has previously worked on recommenders for customers like British Telecom and RTL+, added user segmentation in Sitecore CMS and worked on Danish NLP models for named entity extraction as well as Deep Learning classifiers to predict verdicts of legal cases.
以前は、British Telecom や RTL+ などの顧客向けのレコメンダー、Sitecore CMS のユーザーセグメンテーション、Danish NLP モデルによる固有表現抽出、および Deep Learning 分類器による訴訟判決予測に携わっています。
Kim is also the author of Practical Recommender Systems [1].
Kimは、「Practical Recommender Systems」[1]の著者でもあります。

## 6.2. Chen Karako ♪ チェン・カラコ

Chen is a Data Science Lead at Shopify, where she leads the Discovery Experience data team.
ChenはShopifyのデータサイエンスリードで、Discovery Experienceのデータチームを率いています。
Chen has focused on building search and discovery products using machine learning techniques, experimenting and running A
機械学習技術を用いた検索・発見プロダクトの構築、実験、ASPの運用に注力。

# 7. References リファレンス

- [1] K. Falk. 2019. Practical Recommender Systems. Manning. https://www.manning. com/books/practical-recommender-systems 1] K. Falk. 2019. 実践的なリコメンダーシステム. マニング. https:

- [2] R. Kohavi, D. Tang, and Y. Xu. 2020. Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing. Cambridge University Press. https://books.google. dk/books?id=TFjPDwAAQBAJ [2] R. Kohavi, D. Tang, and Y. Xu. 2020. Trustworthy Online Controlled Experiments（信頼できるオンライン対照実験）。 A Practical Guide to A

- [3] Aleksandrs Slivkins. 2019. Introduction to Multi-Armed Bandits. (2019). https: //doi.org/10.48550/ARXIV.1904.07272 3】Aleksandrs Slivkins. 2019. 多腕バンディット入門. (2019). https:
