## link リンク

- https://towardsdatascience.com/do-you-need-a-feature-store-35b90c3d8963 https://towardsdatascience.com/do-you-need-a-feature-store-35b90c3d8963

# Do you need a feature store? フィーチャーストアが必要か？

Feature Stores make it easier and cheaper to produce more accurate ML models.
フィーチャーストアは、より正確なMLモデルをより簡単かつ安価に作成できる。

A machine learning model is only going to be as good as the data it’s been fed.
機械学習モデルは、与えられたデータと同程度にしかならない。
To be more precise, a model is only as good as the features it’s been given.
より正確に言えば、モデルというものは、そのモデルに与えられた機能によってのみ、その良さが発揮される。

A feature is a useful metric or attribute taken from either a raw data point or an aggregation of several raw data points.
特徴量とは、未加工のデータポイントまたは複数の未加工のデータポイントの集約のいずれかから取得される有用なメトリックまたは属性である。
The specific features used in a model will depend on the prediction the model is trying to make.
モデルで使われる具体的な特徴は、モデルが行おうとしている予測に依存する。
If a model tries to predict fraudulent transactions, for example, relevant features may include whether or not the transaction was in a foreign country, if the purchase was larger than usual, or if the purchase doesn’t align with typical spending for the given customer.
例えば、モデルが不正取引を予測しようとする場合、関連する特徴には、取引が外国で行われたかどうか、購入額が通常より大きいかどうか、購入額が特定の顧客の典型的な支出額と一致しないかどうかなどが含まれる。
These features might be calculated from data points such as the location of the purchase, the value of the purchase, the value of an average purchase, and the aggregated spending patterns of the particular user making the purchase.
これらの特徴は、購入場所、購入金額、平均的な購入金額、購入を行った特定のユーザーの集計された支出パターンなどのデータポイントから計算される可能性がある。

While the data an ML model is trained on is of the utmost importance, preparing good data is one of the most challenging tasks for data scientists.
MLモデルが学習されるデータは最も重要であるが、良いデータを準備することはデータサイエンティストにとって最も困難なタスクの1つである。
In fact, 80% of the average data scientist’s time is spent on data preparation.
実際、平均的なデータサイエンティストの時間の80％はデータの準備に費やされている。
This includes collecting data, cleaning and organizing that data, and engineering it into features.
これには、データの収集、データのクリーニングと整理、機能へのエンジニアリングが含まれる。
This work is manual, monotonous, and tedious: 76% of data scientists rated data prep as the least enjoyable part of their work.
この作業は手作業で、単調で退屈だ： データサイエンティストの76％は、データプリパレーションを仕事の中で最も楽しくない部分と評価している。
Perhaps most importantly, this work might be unnecessary — many data scientists throughout a company end up slogging through the data to calculate the same features that another data scientist in the company has already found.
おそらく最も重要なことは、この作業が不要になる可能性があるということだ。企業全体の多くのデータ・サイエンティストは、社内の別のデータ・サイエンティストがすでに発見しているのと同じ特徴を計算するために、データをのろのろと読み込んでしまうことになる。
Additionally, data scientists spend considerable effort replicating the same feature engineering pipelines each time they want to deploy a model.
さらに、データサイエンティストは、モデルをデプロイするたびに同じフィーチャーエンジニアリングパイプラインを繰り返すことに多大な労力を費やしている。

If this seems inefficient, that’s because it is.
これが非効率に見えるなら、そうだからだ。
Small businesses and leading AI companies are turning to feature stores to solve this problem.
中小企業や大手AI企業は、この問題を解決するためにフィーチャーストアに注目している。