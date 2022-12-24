## link

https://dl.acm.org/doi/10.1145/3523227.3547393

## title

Optimizing product recommendations for millions of merchants

## abstruct

At Shopify, we serve product recommendations to customers across millions of merchants’ online stores. It is a challenge to provide optimized recommendations to all of these independent merchants; one model might lead to an overall improvement in our metrics on aggregate, but significantly degrade recommendations for some stores. To ensure we provide high quality recommendations to all merchant segments, we develop several models that work best in different situations as determined in offline evaluation. Learning which strategy best works for a given segment also allows us to start off new stores with good recommendations, without necessarily needing to rely on an individual store amassing large amounts of traffic. In production, the system will start out with the best strategy for a given merchant, and then adjust to the current environment using multi-armed bandits. Collectively, this methodology allows us to optimize the types of recommendations served on each store.

# Introduction

Building a good product recommendation system for an e-commerce site is challenging. What about building millions of them? Shopify powers millions of diverse businesses, from small artisanal mom and pop shops, to large established businesses. These businesses span a wide range of industries, including apparel, electronics, house wares, food and drink, etc., and similarly have diverse customer bases and behavior. These merchants are also located in over 175 different countries. While Shopify is the platform powering these stores, each merchant’s storefront is a standalone website, customized to suit their brand and preferences. When we build recommender systems for Shopify’s merchants, we must consider the diversity of merchants and their needs to ensure that these systems will benefit all of them, rather than optimizing for only a small subset. Therefore while some companies may have a big data problem, at Shopify we instead have many small data problems!

# SEGMENT OPTIMIZATION

We have developed a variety of product recommendation models using the rich signals available to us. These include content-based models that leverage product metadata, as well as models based on customer behavior. Naturally, stores with more traffic will benefit from collaborative filtering models more so than stores with sparse user behavior data. Moreover, the type of products a merchant sells will affect the performance of each model on that merchant’s store. For example, a merchant selling large appliances may not benefit much from a collaborative filtering model that predicts frequently bought together products, but rather from a model whose intent is to showcase alternative similar products.

When evaluating the performance of a given model, it’s important to not only look at performance metrics in aggregate, but also examine performance for different segments of merchants. It’s possible that a change to a model may improve predictions for one segment of merchants, while degrading them for another. It is therefore not enough to look at one overall metric, but rather we must analyze changes carefully to ensure we understand their impact on all merchants, and ideally refrain from degrading performance for anyone.

![](https://cdn-ak.f.st-hatena.com/images/fotolife/m/m3tech/20221218/20221218110012.png)

Figure 1: Click-through rates for 3 different models across different merchant segments. Different models perform best for different segments.

Figure 1 illustrates the click-through rate of three models, compared between several merchant segments. One can note that different models perform best for different segments, as is indicated by different colored bars being higher for different segments.

One can also note that in this example, certain segments (e.g. segments F, K) do not have predictions from every model; this is due to some models having limited coverage. This highlights the need for developing multiple models that rely on different types of available signals, rather than simply using the model which performs best on average.

We can further combine one or more models to create a recommendation strategy. This strategy defines how to surface recommendations from different models to the user. We optimize these strategies at a merchant segment level by analyzing the segment’s product content and customer engagement trends. After determining the best strategy for a segment, we use it to generate recommendations for a given merchant. Knowing the best strategy for a segment also helps new merchants hit the ground running.

Since the strategies are created based on historical data, the analysis can become stale, resulting in sub-optimal configurations. We therefore see these strategies as bootstrapping for a multi-armed bandit framework [3] which continuously optimizes the strategy. We describe this in more detail in Section 4.

# A/B TESTING

After evaluating our models offline and selecting candidate models that look promising, the next step is online evaluation. We evaluate our models online by running A/B tests, in which each store’s traffic is split such that each customer is assigned to either a control or treatment group. The treatment group will be served recommendations from the model being evaluated, whereas control will receive recommendations from the previous baseline model. It’s helpful to split traffic for each store rather than assign a given store to one experiment group, in order to control for differences between stores. For example, each store’s layout is different, which affects customer behavior. It’s also the case that key business metrics such as conversion rate and average order value vary greatly between stores, depending on the store’s business maturity, customer base, marketing campaigns, product catalog, and so on. After running the experiment for a sufficient amount of time, we compute business metrics for the two experiment groups and test for statistical significance in order to establish a causal relationship between the new model and the observed business impact.

In our experience, running reliable A/B tests in a modern production setting is not as straightforward as one might expect [2]. There are many factors that must be accounted for when designing and analyzing the results of an A/B test: caching, novelty effects, redundant systems, and even adversarial users (bots). To help mitigate these effects and ensure that our testing framework is sound, it’s advisable to run an A/A test before starting to run regular A/B tests. An A/A test is a null test, in which we expect there to be no statistically significant differences between the two groups [2]. Running a successful A/A test can help ensure that we have accounted for all factors, and that results from the upcoming A/B tests can be trusted.

# MULTI-ARMED BANDITS

While A/B tests allow us to select the best performing model based on users’ behavior throughout the experiment, they may not be as suitable for capturing changing trends. Models trained on past signals are outdated as soon as they are computed, since online signals and trends change quickly. Winning models are therefore only used as starting points for the recommender system. Strategies can then be updated with online learning, using multi-armed bandits.

A bandit allows to both explore and exploit the problem space, in order to eventually surface recommendations from the best strategy while still exploring and collecting information about other strategies. The system continuously updates each strategy’s performance based on the observed reward signals. Whenever a new recommendation request arrives, the bandit will either explore or exploit with some probability based on its latest knowledge of the models’ performance.

This bandit approach is particularly helpful in the Shopify context, since it allows us to learn and leverage the optimal strategy for a given segment, merchant, or perhaps even a specific product or page of a merchant’s store. For example, it’s reasonable that a customer shopping for a sofa would be interested in complementary pillows, whereas one who’s looking for pillows would be unlikely to impulsively add a sofa to their purchase. In this case, the bandit would learn that different recommendation models are more suitable for certain pages of the store or to the customers’ contexts.

Finally, we can also analyze the optimal strategies obtained for each merchant as a way of better understanding our user segments and model improvement opportunities, which is helpful in iterating on the next generation of models and strategies.

# CONCLUSION

Shopify has millions of diverse and unique merchants with different needs. By leveraging the network effect and wealth of data available, we can provide optimized recommendations for each merchant. Techniques such as segmentation, A/B testing, and multi-armed bandits allow us to constantly iterate on our product recommendation models, in order to improve customers’ discovery experiences and make our merchants more successful.

# PRESENTER BIO

## Kim Falk

Kim Falk is a Staff Recommender Engineer at Shopify, where he is the technical lead of the Product Recommendations team. Kim has experience in machine learning but is specialized in Recommender systems. He has previously worked on recommenders for customers like British Telecom and RTL+, added user segmentation in Sitecore CMS and worked on Danish NLP models for named entity extraction as well as Deep Learning classifiers to predict verdicts of legal cases. Kim is also the author of Practical Recommender Systems [1].

## Chen Karako

Chen is a Data Science Lead at Shopify, where she leads the Discovery Experience data team. Chen has focused on building search and discovery products using machine learning techniques, experimenting and running A/B tests to improve and measure feature impact, and collaborating with cross-disciplinary teams. Chen is passionate about recommender systems and information retrieval and building discovery products with engaging user experiences. Chen is also interested in fairness in AI and has published research in this domain. Finally, Chen enjoys building and leading high impact data science teams, and providing technical and strategic leadership on product teams. Prior to joining Shopify, Chen obtained an M.Sc. in astrophysics from McGill University, where she discovered 30 radio pulsars by developing signal processing algorithms for telescope data

# References

- [1] K. Falk. 2019. Practical Recommender Systems. Manning. https://www.manning. com/books/practical-recommender-systems
- [2] R. Kohavi, D. Tang, and Y. Xu. 2020. Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing. Cambridge University Press. https://books.google. dk/books?id=TFjPDwAAQBAJ
- [3] Aleksandrs Slivkins. 2019. Introduction to Multi-Armed Bandits. (2019). https: //doi.org/10.48550/ARXIV.1904.07272
