## link

- https://towardsdatascience.com/do-you-need-a-feature-store-35b90c3d8963

# Do you need a feature store?

Feature Stores make it easier and cheaper to produce more accurate ML models.

A machine learning model is only going to be as good as the data it’s been fed. To be more precise, a model is only as good as the features it’s been given.

A feature is a useful metric or attribute taken from either a raw data point or an aggregation of several raw data points. The specific features used in a model will depend on the prediction the model is trying to make. If a model tries to predict fraudulent transactions, for example, relevant features may include whether or not the transaction was in a foreign country, if the purchase was larger than usual, or if the purchase doesn’t align with typical spending for the given customer. These features might be calculated from data points such as the location of the purchase, the value of the purchase, the value of an average purchase, and the aggregated spending patterns of the particular user making the purchase.

While the data an ML model is trained on is of the utmost importance, preparing good data is one of the most challenging tasks for data scientists. In fact, 80% of the average data scientist’s time is spent on data preparation. This includes collecting data, cleaning and organizing that data, and engineering it into features. This work is manual, monotonous, and tedious: 76% of data scientists rated data prep as the least enjoyable part of their work. Perhaps most importantly, this work might be unnecessary — many data scientists throughout a company end up slogging through the data to calculate the same features that another data scientist in the company has already found. Additionally, data scientists spend considerable effort replicating the same feature engineering pipelines each time they want to deploy a model.

If this seems inefficient, that’s because it is. Small businesses and leading AI companies are turning to feature stores to solve this problem.
