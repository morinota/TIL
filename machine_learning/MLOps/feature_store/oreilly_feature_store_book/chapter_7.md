## CHAPTER 7: Model-Dependent and On-Demand Transformations
## 第7章: モデル依存型およびオンデマンド変換

In this chapter, we will look at data transformations in training and inference pipelines and how to ensure that transformations in both pipelines are equivalent. 
この章では、トレーニングと推論パイプラインにおけるデータ変換と、両方のパイプラインでの変換が等価であることを保証する方法について見ていきます。

We introduced model-dependent transformations (MDTs) in Chapter 2 as data transformations that are performed on data after it has been read from the feature store and that create features that are specific to one model. 
第2章では、特徴ストアから読み取ったデータに対して行われ、特定のモデルに固有の特徴を生成するデータ変換として、モデル依存型変換（MDT）を紹介しました。

There are two broad classes of MDTs—feature transformations (for numerical and categorical features) and transformations that are tightly coupled to only one model. 
MDTには大きく分けて2つのクラスがあります。数値およびカテゴリ特徴のための特徴変換と、特定のモデルに密接に結びついた変換です。

An example of the former is one-hot encoding of categorical variables, while an example of the latter is text encoding for an LLM. 
前者の例はカテゴリ変数のワンホットエンコーディングであり、後者の例はLLMのためのテキストエンコーディングです。

We also look at how to prevent _skew between MDTs that are applied separately in_ training and inference pipelines. 
また、トレーニングと推論パイプラインで別々に適用されるMDT間の_偏りを防ぐ方法_についても見ていきます。

This is not always as trivial as applying the same versioned function in both training and inference pipelines, as many MDTs are stateful, requiring the same state (the model’s training data statistics) as a parameter in both training and inference pipelines. 
これは、トレーニングと推論パイプラインの両方で同じバージョンの関数を適用することが常に簡単ではないためです。多くのMDTは状態を持ち、トレーニングと推論パイプラインの両方で同じ状態（モデルのトレーニングデータ統計）をパラメータとして必要とします。

We start by introducing common examples of feature transformations and different classes of model-specific transformations. 
まず、一般的な特徴変換の例と、モデル固有の変換の異なるクラスを紹介します。

We then look at different mechanisms for preventing skew, including Scikit-Learn pipelines, PyTorch transforms, and transformation functions in feature views for Hopsworks. 
次に、Scikit-Learnパイプライン、PyTorch変換、Hopsworksの特徴ビューにおける変換関数など、偏りを防ぐためのさまざまなメカニズムを見ていきます。

We also cover our final class of data transformation—on-demand transformations (ODTs) that are found in online inference pipelines and feature pipelines and are typically stateless transformation functions. 
最後に、オンライン推論パイプラインや特徴パイプラインに見られるオンデマンド変換（ODT）というデータ変換の最終クラスについても説明します。これらは通常、状態を持たない変換関数です。

Then, we finish the chapter with unit testing of transformation functions with pytest. 
最後に、pytestを使用した変換関数の単体テストで章を締めくくります。

###### Feature Transformations
###### 特徴変換

Feature transformations can enhance the performance and convergence of various types of ML models. 
特徴変換は、さまざまなタイプのMLモデルのパフォーマンスと収束を向上させることができます。

For example, most ML algorithms cannot accept strings as input, and they need to be transformed into a numerical format. 
例えば、ほとんどのMLアルゴリズムは文字列を入力として受け入れることができず、数値形式に変換する必要があります。

The final input to an ML model is typically a numeric array. 
MLモデルへの最終入力は通常、数値配列です。

Similarly, deep learning models often require numerical features to be normalized or transformed to follow a normal distribution to help ensure proper convergence. 
同様に、深層学習モデルは、数値特徴が正規分布に従うように正規化または変換されることを必要とし、適切な収束を確保します。

Different feature transformations are performed on a specific feature type (categorical or numerical). 
異なる特徴変換は、特定の特徴タイプ（カテゴリまたは数値）に対して実行されます。

The feature type helps identify which feature transformation is appropriate. 
特徴タイプは、どの特徴変換が適切であるかを特定するのに役立ちます。

For example, encoding is used to convert categorical variables into a numerical format, while scaling adjusts the range or distribution of numerical variables. 
例えば、エンコーディングはカテゴリ変数を数値形式に変換するために使用され、スケーリングは数値変数の範囲や分布を調整します。

These transformations are often parameterized by properties of the training data, such as the set of categories or descriptive statistics (min, max, mean, standard deviation, or mode). 
これらの変換は、カテゴリのセットや記述統計（最小値、最大値、平均、標準偏差、または最頻値）など、トレーニングデータの特性によってパラメータ化されることがよくあります。

For example, when you one-hot encode a categorical variable, you first enumerate all of the categories in the training data, before you can encode the string as a binary vector. 
例えば、カテゴリ変数をワンホットエンコーディングする場合、まずトレーニングデータ内のすべてのカテゴリを列挙し、その後に文字列をバイナリベクトルとしてエンコードします。

Similarly, when applying standardization (also called z-score normalization) to numerical variables, the mean and standard deviation must first be computed from the training data and then used to consistently scale all feature values in the dataset. 
同様に、数値変数に標準化（zスコア正規化とも呼ばれる）を適用する場合、平均と標準偏差はまずトレーニングデータから計算され、その後、データセット内のすべての特徴値を一貫してスケーリングするために使用されます。

###### Encoding Categorical Variables
###### カテゴリ変数のエンコーディング

In feature-encoding algorithms, the set of categories may change over time, and to handle this, you should include a special category (called “unknown” or “other”) for any new categories that appear during inference. 
特徴エンコーディングアルゴリズムでは、カテゴリのセットは時間とともに変化する可能性があり、これに対処するために、推論中に現れる新しいカテゴリのために特別なカテゴリ（「不明」または「その他」と呼ばれる）を含めるべきです。

For example, the merchant category code given for a credit card payment is important for many bonus rewards programs that give points for a specific type of spending, such as travel. 
例えば、クレジットカード支払いに対して与えられる商業カテゴリコードは、旅行などの特定の支出タイプに対してポイントを付与する多くのボーナス報酬プログラムにとって重要です。

Each merchant typically has a single category that is added to a credit card payment. 
各商業者は通常、クレジットカード支払いに追加される単一のカテゴリを持っています。

In Table 7-1, we one-hot encode the categories. 
表7-1では、カテゴリをワンホットエンコーディングします。

For simplicity, I only show four categories, whereas in reality, there are hundreds. 
簡単のために、私は4つのカテゴリのみを示しますが、実際には数百あります。

Each one-hot-encoded array represents a category with a 1 in the category’s position in the array and a 0 in all other positions. 
各ワンホットエンコーディングされた配列は、配列内のカテゴリの位置に1を持ち、他のすべての位置に0を持つカテゴリを表します。

_Table 7-1. One-hot encoding of the merchant category for a credit card payment_
**表7-1. クレジットカード支払いのための商業カテゴリのワンホットエンコーディング**
**Merchant category** **One-hot encoded**
**商業カテゴリ** **ワンホットエンコーディング**
Airlines [1,0,0,0]  
Eating places and restaurants [0,1,0,0]  
Car rental [0,0,1,0]  
Hotels, motels, and resorts [0,0,0,1]  

One-hot encoding is not recommended when there is _high cardinality (i.e., a large_ number of categories), as each category adds a new dimension, increasing memory usage. 
高いカーディナリティ（すなわち、多くのカテゴリ）がある場合、ワンホットエンコーディングは推奨されません。各カテゴリが新しい次元を追加し、メモリ使用量が増加するためです。

It is also unsuitable when there is an ordinal relationship between categories, as it does not preserve order, as shown in Table 7-2. 
また、カテゴリ間に順序関係がある場合にも不適切です。表7-2に示すように、順序を保持しないためです。

If there is an ordinal relationship between the variables, then the ordinal encoder preserves ordering in the transformed categories. 
変数間に順序関係がある場合、順序エンコーダは変換されたカテゴリの順序を保持します。

_Table 7-2. Popular algorithms for encoding categorical feature data_
**表7-2. カテゴリ特徴データのエンコーディングに関する一般的なアルゴリズム**
**Algorithm** **Purpose** **Use case**  
**アルゴリズム** **目的** **使用例**  
One-hot encoder Transforms categorical data into one-hot-encoded vectors (an array of bytes, with each category representing one bit)  
ワンホットエンコーダは、カテゴリデータをワンホットエンコーディングされたベクトル（各カテゴリが1ビットを表すバイトの配列）に変換します。  
Transforming to one-hot encoder when there is no ordinal relationship and low to medium cardinality  
順序関係がなく、カーディナリティが低いから中程度のときにワンホットエンコーダに変換します。  
Ordinal encoder Transforms categorical data into an integer  
順序エンコーダは、カテゴリデータを整数に変換します。  
Encoding features that have an ordinal relationship  
順序関係のある特徴をエンコードします。  
Feature hasher Uses the hashing trick to transform categorical data into a fixed-size vector  
特徴ハッシャーは、ハッシングトリックを使用してカテゴリデータを固定サイズのベクトルに変換します。  
High-dimensional data with many unique categories  
多くのユニークなカテゴリを持つ高次元データ  

For features with a very large number of categories, feature hashing (the _feature_ _hasher encoding algorithm) reduces dimensionality by mapping categories to a fixed-size hash table, though this introduces the risk of hash collisions (that is, different cat‐ egories mapping to the same value). 
非常に多くのカテゴリを持つ特徴に対して、特徴ハッシング（_特徴_ _ハッシャーエンコーディングアルゴリズム）は、カテゴリを固定サイズのハッシュテーブルにマッピングすることによって次元を削減しますが、これによりハッシュ衝突（異なるカテゴリが同じ値にマッピングされるリスク）が生じます。

Be sure that your ML algorithm can tolerate possible hash collisions if you use a feature hasher. 
特徴ハッシャーを使用する場合は、MLアルゴリズムが可能なハッシュ衝突に耐えられることを確認してください。

Finally, label encoding is often used for encoding the target/label variable as integers, thus preserving ordering. 
最後に、ラベルエンコーディングは、ターゲット/ラベル変数を整数としてエンコードするためにしばしば使用され、これにより順序が保持されます。

Many ML algorithms, such as Scikit-Learn’s logistic regression and XGBoost’s multiclass classification, require labels (target variables) to be integer encoded. 
Scikit-Learnのロジスティック回帰やXGBoostの多クラス分類など、多くのMLアルゴリズムは、ラベル（ターゲット変数）が整数エンコードされることを要求します。

Note that for some tree-based algorithms, such as _[CatBoost, you do not need to](https://catboost.ai)_ encode categorical variables. 
_[CatBoost](https://catboost.ai)などの一部の木ベースのアルゴリズムでは、カテゴリ変数をエンコードする必要はありません。_

CatBoost can handle categorical variables with high cardinality, and it preserves ordinal information—without the need to spend CPU cycles encoding the categorical data. 
CatBoostは高いカーディナリティを持つカテゴリ変数を処理でき、カテゴリデータをエンコードするためにCPUサイクルを費やす必要なく、順序情報を保持します。

CatBoost can also train models with lots of categorical variables with better performance than XGBoost, for example, through automatically extracting complex interactions between categorical features and by reducing overfitting. 
CatBoostは、カテゴリ特徴間の複雑な相互作用を自動的に抽出し、過剰適合を減少させることによって、XGBoostよりも優れたパフォーマンスで多くのカテゴリ変数を持つモデルをトレーニングすることもできます。

###### Distributions of Numerical Variables
###### 数値変数の分布

Many ML algorithms only work well when a numerical feature follows a particular data distribution. 
多くのMLアルゴリズムは、数値特徴が特定のデータ分布に従う場合にのみうまく機能します。

For example, if the distribution of your numerical feature data is skewed and your ML algorithm is based on gradient descent (such as neural networks or linear regression), you should standardize the data. 
例えば、数値特徴データの分布が歪んでいて、MLアルゴリズムが勾配降下法（ニューラルネットワークや線形回帰など）に基づいている場合、データを標準化する必要があります。

Standardization transforms a numerical variable’s distribution to have a mean of zero and a unit variance (standard deviation) of one. 
標準化は、数値変数の分布を平均0、分散（標準偏差）1に変換します。

This will improve gradient descent’s convergence speed and subsequent model stability. 
これにより、勾配降下法の収束速度とその後のモデルの安定性が向上します。

Figure 7-1 shows some of the most common distributions for numerical variables. 
図7-1は、数値変数の最も一般的な分布のいくつかを示しています。

It is good practice to identify the distribution of each numerical variable, so that when you use an ML algorithm with that feature, you know which transformation algorithm, if any, to apply to the feature data. 
各数値変数の分布を特定することは良い習慣であり、その特徴を持つMLアルゴリズムを使用する際に、どの変換アルゴリズムを特徴データに適用すべきかを知ることができます。

_Figure 7-1. An illustrative guide to some common numerical feature distributions. The_ _log-normal distribution has a longer tail than the exponential distribution and is not a_ _max at 0 on the x-axis._  
_図7-1. 一部の一般的な数値特徴分布に関する説明ガイド。対数正規分布は指数分布よりも長い尾を持ち、x軸の0で最大ではありません。_

Returning to our credit card fraud system, we give examples of these distributions for credit card transactions: 
クレジットカード詐欺システムに戻ると、クレジットカード取引のこれらの分布の例を示します。

- The `credit_rating for a bank typically follows a` _normal distribution, with a_ small number of banks having the highest and lowest ratings and most banks clustered around the mean rating. 
- 銀行の`credit_ratingは通常、_正規分布に従い、最も高いおよび最も低い評価を持つ銀行は少数であり、ほとんどの銀行は平均評価の周りに集まっています。_

- A _uniform distribution means each possible value has an equal probability of_ occurring. 
- _一様分布は、各可能な値が発生する確率が等しいことを意味します。_

None of our features in the credit card model are truly uniform. 
クレジットカードモデルの特徴の中には、真に一様なものはありません。

Often, variables may start with a uniform distribution, but through grouping or transformation, you can extract new features that have more informative, non‐ uniform distributions. 
しばしば、変数は一様分布から始まることがありますが、グループ化や変換を通じて、より情報量の多い非一様分布を持つ新しい特徴を抽出することができます。

- The binomial distribution models discrete outcomes (success/failure) over multiple independent trials. 
- _二項分布は、複数の独立した試行における離散的な結果（成功/失敗）をモデル化します。_

Although not a feature in our credit card model, the probability that a merchant terminal will work or not could be represented as a binomial distribution with a reliability probability of, say, 0.98; that is, 98% of transactions would be successfully processed without errors. 
クレジットカードモデルの特徴ではありませんが、商業端末が機能するかどうかの確率は、信頼性確率が0.98である二項分布として表すことができます。つまり、98%の取引がエラーなしで正常に処理されることになります。

- The _Poisson distribution models the number of times independent events occur_ within a fixed interval of time. 
- _ポアソン分布は、固定された時間間隔内で独立したイベントが発生する回数をモデル化します。_

For example, we could model how many credit card fraud detections occur on average per day as a Poisson distribution. 
例えば、1日に平均して何件のクレジットカード詐欺検出が発生するかをポアソン分布としてモデル化できます。

The model can decide when to generate alerts if the number of credit card fraud detections is deemed to be anomalous. 
モデルは、クレジットカード詐欺検出の数が異常であると見なされる場合にアラートを生成するタイミングを決定できます。

- The _exponential distribution can model the time between independent transac‐_ tions, when events occur continuously and independently at a constant average rate. 
- _指数分布は、イベントが一定の平均レートで連続的かつ独立に発生する場合の独立した取引間の時間をモデル化できます。_

For example, the average waiting time between card transactions is three hours, meaning short intervals (minutes) are common and much longer waits (days) are less frequent. 
例えば、カード取引間の平均待機時間は3時間であり、短い間隔（数分）が一般的で、はるかに長い待機時間（数日）は少ないことを意味します。

- The amount spent in a credit card transaction follows a skewed distribution, with a large number of small amounts and a small number of large amounts. 
- クレジットカード取引での支出額は歪んだ分布に従い、多くの小額と少数の大額があります。

- The bimodal distribution can help us model the amount spent by each customer on a holiday using two different subgroups—each of which follows a normal distribution. 
- バイモーダル分布は、異なる2つのサブグループを使用して、休日に各顧客が支出した金額をモデル化するのに役立ちます。各サブグループは正規分布に従います。

Regular shoppers spend a mean of $200 (the first peak) and holiday shoppers spend a mean of $800 (the second peak). 
通常の買い物客は平均200ドル（最初のピーク）を支出し、休日の買い物客は平均800ドル（2番目のピーク）を支出します。

- Finally, the amount spent in individual credit card transactions typically follows a type of skewed distribution called the log-normal distribution. 
- 最後に、個々のクレジットカード取引での支出額は、通常、対数正規分布と呼ばれるタイプの歪んだ分布に従います。

Its characteristics are that the amounts are nonnegative and it is positively skewed to the right (most payments are small, with fewer large payments). 
その特徴は、金額が非負であり、右に正の歪みがあることです（ほとんどの支払いは小額で、大きな支払いは少ない）。



. Its characteristics are that the amounts are nonnegative and it is positively skewed to the right (most payments are small, with fewer large payments).  
その特徴は、金額が非負であり、右に正の歪みがあることです（ほとんどの支払いは小額で、大きな支払いは少ないです）。  

###### Transforming Numerical Variables
###### 数値変数の変換

Standardizing numerical feature distributions is a common transformation that should be performed on many ML algorithms—not just the gradient descent mentioned earlier but also kNN and support vector machines (SVMs).  
数値特徴の分布を標準化することは、多くの機械学習アルゴリズムで行うべき一般的な変換です。これは、前述の勾配降下法だけでなく、kNNやサポートベクターマシン（SVM）にも当てはまります。

An alternative to standardization is _normalization (also known as_ _min-max scaling), which similarly_ improves model convergence speed but does so by only scaling the range of values.  
標準化の代替手段は、_正規化（min-maxスケーリングとも呼ばれる）_であり、同様にモデルの収束速度を改善しますが、値の範囲をスケーリングするだけで行います。

Normalization rescales values to a fixed range, such as 0 to 1, while preserving their original distribution shape.  
正規化は、値を0から1のような固定範囲に再スケーリングし、元の分布の形状を保持します。

Standardization, in contrast, also transforms the distribution shape.  
対照的に、標準化は分布の形状も変換します。

For example, credit card transaction amounts can range from $0.01 to $10,000, and account balances can range from $0 to millions of dollars.  
例えば、クレジットカードの取引金額は$0.01から$10,000までの範囲であり、口座残高は$0から数百万ドルまでの範囲です。

If you don’t standardize or normalize the amounts and balances, gradient descent can produce large, erratic updates during training.  
金額や残高を標準化または正規化しないと、勾配降下法はトレーニング中に大きく不規則な更新を生成する可能性があります。

Clustering algorithms, like kNN and SVMs, rely on distance values and also benefit from standardization or normalization, as do probabilistic models, like Gaussian Naive Bayes.  
kNNやSVMのようなクラスタリングアルゴリズムは距離値に依存し、標準化や正規化の恩恵を受けます。ガウスナイーブベイズのような確率モデルも同様です。

In such models, without standardization or normalization, an amount or account balance with a large range of values can dominate other features in a model.  
そのようなモデルでは、標準化や正規化がないと、大きな範囲の値を持つ金額や口座残高がモデル内の他の特徴を支配する可能性があります。

So when should you choose normalization over standardization?  
では、いつ正規化を標準化の代わりに選ぶべきでしょうか？

Here are two rules of thumb:  
以下に2つの経験則を示します：

- Normalization is often a good fit for neural networks and when the original feature distribution is important.  
  正規化は、ニューラルネットワークや元の特徴分布が重要な場合に適していることが多いです。

- For example, if outliers in your data are meaningful and not anomalies, normalization may be preferred because it preserves the original shape of the distribution.  
  例えば、データ内の外れ値が意味のあるものであり異常でない場合、正規化は元の分布の形状を保持するため好まれることがあります。

- Standardization is usually preferred for linear models, distance-based algorithms, and when you assume features should be normally distributed.  
  標準化は通常、線形モデル、距離ベースのアルゴリズム、および特徴が正規分布であるべきと仮定する場合に好まれます。

Ultimately, the best choice depends on your data and model, so you may need to experiment with both approaches.  
最終的には、最適な選択はデータとモデルに依存するため、両方のアプローチを試す必要があるかもしれません。

Another important class of transformation is _log transformations.  
もう一つの重要な変換のクラスは、_対数変換_です。

Highly skewed numerical variables, such as transaction amounts, can negatively impact model performance, especially when outliers dominate the data.  
取引金額のような高度に歪んだ数値変数は、特に外れ値がデータを支配する場合、モデルのパフォーマンスに悪影響を及ぼす可能性があります。

Log transformations help reduce skewness and compress the range of values, making the distribution closer to normal and reducing the influence of extreme values.  
対数変換は歪みを減少させ、値の範囲を圧縮し、分布を正規に近づけ、極端な値の影響を減少させます。

Log transformations are especially effective for right-skewed data.  
対数変換は特に右に歪んだデータに対して効果的です。

However, your data should not contain zeros or negative values, since the logarithm is undefined for those cases.  
ただし、データにはゼロや負の値が含まれてはいけません。なぜなら、対数はその場合に定義されないからです。

If your data does include zeros, you can use a modified transformation such as log 1 + x .  
データにゼロが含まれている場合は、log 1 + xのような修正された変換を使用できます。

Not all ML algorithms require transformation of numerical features, though.  
ただし、すべての機械学習アルゴリズムが数値特徴の変換を必要とするわけではありません。

There is no need to transform numerical features for tree-based models, such as gradient-boosted decision trees and random forests, since they are unaffected by the scale of features when splitting nodes.  
勾配ブースト決定木やランダムフォレストのような木ベースのモデルでは、ノードを分割する際に特徴のスケールに影響されないため、数値特徴を変換する必要はありません。

However, certain transformations, such as reducing extreme skewness or simplifying feature interactions, improve tree model performance.  
ただし、極端な歪みを減少させたり、特徴の相互作用を単純化したりするような特定の変換は、木モデルのパフォーマンスを向上させます。

For example, log-transforming a highly skewed variable can help balance splits and allow the model to better capture patterns across the data range.  
例えば、高度に歪んだ変数を対数変換することで、分割をバランスさせ、モデルがデータ範囲全体のパターンをよりよく捉えることができます。

When you’re computing transformations, you must first make a full pass of the feature values of some of them to compute descriptive statistics, such as the mean, standard deviation, minimum, and maximum values.  
変換を計算する際は、まずいくつかの特徴値の完全なパスを実行して、平均、標準偏差、最小値、最大値などの記述統計を計算する必要があります。

The second pass can then update each data point by applying the transformation.  
次のパスでは、変換を適用して各データポイントを更新できます。

Here are examples of how common transformations are computed:  
以下は、一般的な変換がどのように計算されるかの例です：

- Normalization involves adjusting the range of feature values so that they fit within a specific range, typically between zero and one.  
  正規化は、特徴値の範囲を調整して特定の範囲（通常は0から1の間）に収めることを含みます。

- The most common method of normalization is min-max scaling, where, for each data point, you subtract the minimum value and divide by the maximum value minus the minimum value:  
  正規化の最も一般的な方法はmin-maxスケーリングであり、各データポイントについて最小値を引き、最大値から最小値を引いた値で割ります：  
  $$  
  x_{\text{normalized}} = \frac{x - x_{\text{min}}}{x_{\text{max}} - x_{\text{min}}}  
  $$  

- Standardization involves subtracting the mean and dividing by the standard deviation for every data point.  
  標準化は、各データポイントについて平均を引き、標準偏差で割ることを含みます。

- It centers the data around zero and scales it based on the standard deviation:  
  これはデータをゼロの周りに中心化し、標準偏差に基づいてスケーリングします：  
  $$  
  x_{\text{standardized}} = \frac{x - \mu}{\sigma}  
  $$  
  ここで、$\sigma$は標準偏差、$\mu$は平均です。

- Log transformations apply a logarithmic function to each data point, typically base 10 or base e (denoted as ln):  
  対数変換は、各データポイントに対数関数を適用します。通常は底10または底e（lnとして示される）です：  
  $$  
  x_{\text{log}} = \ln x  
  $$  

- Reciprocal transformation takes the reciprocal (i.e., the inverse) of each value.  
  逆数変換は、各値の逆数（すなわち逆）を取ります。

- The reciprocal of a number x is 1/x.  
  数字$x$の逆数は$1/x$です。

- It can help reduce the skewness of a dataset and stabilize its variance:  
  これはデータセットの歪みを減少させ、分散を安定させるのに役立ちます：  
  $$  
  x_{\text{reciprocal}} = \frac{1}{x}  
  $$  

- Exponential transformation of a numerical variable x involves applying an exponential function.  
  数値変数$x$の指数変換は、指数関数を適用することを含みます。

- It can linearize relationships between variables when dealing with exponential growth or decay patterns, or it can give greater weight to larger values in a dataset:  
  これは、指数的成長または減衰パターンを扱う際に変数間の関係を線形化したり、データセット内の大きな値により大きな重みを与えたりすることができます：  
  $$  
  x_{\text{exp}} = a \cdot e^{b \cdot x}  
  $$  
  ここで、$a$はスケーリング係数、$b$は成長率を制御します。

- Box-Cox transformation stabilizes the variance in a numerical variable, making it more closely approximate a normal distribution.  
  Box-Cox変換は数値変数の分散を安定させ、正規分布により近づけます。

- A good value for the hyperparameter, _λ, can be estimated using maximum likelihood estimation, such that it_ minimizes the skewness of the transformed data, making it as close to normal as possible.  
  ハイパーパラメータ_λ_の良い値は、最大尤度推定を使用して推定でき、変換されたデータの歪みを最小化し、できるだけ正規に近づけます。

- When 𝜆 = 0, the Box-Cox transformation becomes the natural log:  
  𝜆 = 0のとき、Box-Cox変換は自然対数になります：  
  $$  
  x_{\text{box-cox}}^{\lambda} = \frac{x^{\lambda} - 1}{\lambda}  
  $$  

###### Storing Transformed Feature Data in a Feature Group
###### 特徴グループに変換された特徴データを保存する

In general, you should not store transformed feature data in feature groups, as it precludes feature reuse by models and introduces write amplification when new data is written to a feature group.  
一般的に、変換された特徴データを特徴グループに保存すべきではありません。なぜなら、それはモデルによる特徴の再利用を妨げ、新しいデータが特徴グループに書き込まれるときに書き込みの増幅を引き起こすからです。

However, in a case where you require the lowest possible latency in a real-time ML system, precomputing as much as possible can help shave off microseconds or milliseconds from prediction request latency.  
ただし、リアルタイムの機械学習システムで可能な限り低いレイテンシを要求する場合、できるだけ多くを事前計算することで、予測リクエストのレイテンシからマイクロ秒またはミリ秒を削減するのに役立ちます。

Milliseconds can be worth millions for some companies.  
ミリ秒は、いくつかの企業にとって何百万ドルの価値があります。

If you absolutely have to apply your feature transformations before the feature store, you can create a separate online-only feature group for your model, including its own dedicated feature pipeline.  
もし、どうしても特徴ストアの前に特徴変換を適用する必要がある場合は、モデルのために専用の特徴パイプラインを含むオンライン専用の特徴グループを作成できます。

The feature pipeline should use the training dataset statistics for your model to apply feature transformations.  
特徴パイプラインは、モデルのためにトレーニングデータセットの統計を使用して特徴変換を適用する必要があります。

This “transformed” feature group should be online only, so it will only store the latest feature values and you will not need to recompute existing feature data for every write.  
この「変換された」特徴グループはオンライン専用であるべきで、最新の特徴値のみを保存し、すべての書き込みに対して既存の特徴データを再計算する必要はありません。

If some of the features are reused in other models, you should update your feature pipeline to first compute the untransformed features and write them to the shared, untransformed feature group.  
他のモデルで一部の特徴が再利用される場合は、最初に未変換の特徴を計算し、それを共有の未変換特徴グループに書き込むように特徴パイプラインを更新する必要があります。

Then, after applying the feature transformations, you should write the transformed features to the transformed online feature group.  
その後、特徴変換を適用した後、変換された特徴を変換されたオンライン特徴グループに書き込む必要があります。

This works for both batch and streaming feature pipelines.  
これは、バッチおよびストリーミングの特徴パイプラインの両方で機能します。

###### Model-Specific Transformations
###### モデル特有の変換

_Model-specific transformations are a catchall for any data transformation that is not a_ feature transformation but is specific to one model.  
_モデル特有の変換は、特徴変換ではなく、特定のモデルに特有のデータ変換の総称です。

We will look at a couple of examples of such transformations.  
このような変換のいくつかの例を見ていきます。

For example, a popular way to impute missing inference data is to first compute the mean/median/mode for features in the training data and replace the missing values with one of the computed values.  
例えば、欠損した推論データを補完する一般的な方法は、まずトレーニングデータの特徴の平均/中央値/最頻値を計算し、欠損値を計算された値の1つで置き換えることです。

Another example, which does not require training data statistics, is determining how to transform timestamps for features so that they are aligned with the timestamps for targets/labels.  
もう一つの例は、トレーニングデータの統計を必要とせず、特徴のタイムスタンプをターゲット/ラベルのタイムスタンプに合わせるためにどのように変換するかを決定することです。

This transformation enables you to create training data with a more efficient `INNER JOIN` instead of an ASOF LEFT JOIN.  
この変換により、ASOF LEFT JOINの代わりにより効率的な`INNER JOIN`を使用してトレーニングデータを作成できます。

###### Outlier Handling Methods
###### 外れ値処理方法

_Outlier detection identifies and handles anomalous data points that can skew model_ training and lead to poor predictions.  
_外れ値検出は、モデルのトレーニングを歪め、予測の質を低下させる可能性のある異常なデータポイントを特定し処理します。

Where possible, it is preferable to not ingest anomalous data points into a feature group, for example, by using Great Expectations to identify and remove them in feature pipelines.  
可能な限り、外れ値データポイントを特徴グループに取り込まない方が望ましいです。例えば、Great Expectationsを使用して特徴パイプラインでそれらを特定し削除します。

Sometimes, however, feature groups can contain anomalous data, and you’ll then have to perform outlier detection as MDTs.  
ただし、場合によっては、特徴グループに異常なデータが含まれることがあり、その場合はMDTとして外れ値検出を実行する必要があります。

Scikit-Learn has good support for both univariate (one-feature) and multivariate (multiple-feature) approaches.  
Scikit-Learnは、単変量（1つの特徴）および多変量（複数の特徴）アプローチの両方に対して良好なサポートを提供しています。

For univariate data, it includes statistical techniques such as the z-score and the interquartile range (IQR) method.  
単変量データの場合、zスコアや四分位範囲（IQR）法などの統計的手法が含まれています。

For multivariate data, it provides algorithms like the Isolation Forest and Local Outlier Factor (LOF).  
多変量データの場合、Isolation ForestやLocal Outlier Factor（LOF）などのアルゴリズムが提供されています。

Here is an example that removes small outlier payments (the bottom 0.2% of amounts) in credit card transactions:  
以下は、クレジットカード取引における小さな外れ値の支払い（金額の下位0.2%）を削除する例です：  
```  
Q1 = df['amount'].quantile(0.002)  
outliers = df[(df['amount'] < Q1)]  
```  

If large outlier payments remain, a log transformation can help reduce their influence by compressing high values.  
大きな外れ値の支払いが残っている場合、対数変換は高い値を圧縮することでその影響を減少させるのに役立ちます。

Generally, you should perform outlier removal before log transformations, and remember, log transformations do not help with small or negative outliers.  
一般的に、対数変換の前に外れ値の削除を行うべきであり、対数変換は小さな外れ値や負の外れ値には効果がないことを覚えておいてください。

###### Imputing Missing Values
###### 欠損値の補完

Missing values can sometimes be identified in EDA and handled by not including features in a feature view.  
欠損値は、探索的データ分析（EDA）で特定されることがあり、特徴ビューに特徴を含めないことで処理されます。

For example, you may not select a feature for a model because it has too many missing values.  
例えば、欠損値が多すぎるためにモデルのために特徴を選択しないことがあります。

In a production feature pipeline, a missing value in a row may be so important that it invalidates all of the other values in that row—in which case the entire row is dropped.  
生産環境の特徴パイプラインでは、行内の欠損値が非常に重要であり、その行内の他のすべての値を無効にする場合、その行全体が削除されます。

Often, however, we choose to deal with missing values by imputing them in training and inference pipelines.  
しかし、しばしば、トレーニングおよび推論パイプラインで欠損値を補完することで対処することを選択します。

A list of popular techniques for imputing missing data is shown in Figure 7-2.i  
欠損データを補完するための一般的な手法のリストは、図7-2.iに示されています。



_Figure 7-2. Different techniques for the imputation of missing data in training and inference pipelines, based on whether the data is time-series data or not. For non-time-series data, we can use descriptive statistics computed from the training dataset to impute missing values._
_Figure 7-2. トレーニングおよび推論パイプラインにおける欠損データの補完のための異なる手法。データが時系列データであるかどうかに基づいています。非時系列データの場合、トレーニングデータセットから計算された記述統計を使用して欠損値を補完できます。_

_In Pandas, we can impute missing time-series data using forward filling as follows:_
_次のように、Pandasを使用して欠損した時系列データを前方補完で補完できます：_

```  
df_forward_filled = df.sort_values("event_time").groupby("cc_num")["amount"].ffill()
```  
```  
df_forward_filled = df.sort_values("event_time").groupby("cc_num")["amount"].ffill()
```  
_Forward filling takes the last valid (nonmissing) value, uses it to fill in the missing values forward for all columns in the DataFrame, and stores the output in a new DataFrame._
_前方補完は、最後の有効（欠損でない）値を取り、それを使用してDataFrame内のすべての列の欠損値を前方に補完し、出力を新しいDataFrameに保存します。_

_It is also possible to impute missing values with backward filling that takes the next valid (nonmissing) value and uses it to fill in the missing values backward._
_次の有効（欠損でない）値を取り、それを使用して欠損値を後方に補完するバックワードフィリングでも欠損値を補完できます。_

_In this Pandas operation, we only backfill the `amount` column and update the same DataFrame:_
_このPandas操作では、`amount`列のみを後方補完し、同じDataFrameを更新します：_

```  
df["amount"] = df.sort_values("event_time").groupby("cc_num")["amount"].bfill()
```  
```  
df["amount"] = df.sort_values("event_time").groupby("cc_num")["amount"].bfill()
```  
_What happens if you have large volumes of data (10s of GBs or more) that Pandas cannot scale to process?_
_もしPandasが処理できないほどの大容量データ（数十GB以上）がある場合はどうなりますか？_

_You could use PySpark instead of Pandas. PySpark doesn’t have native library support, but you can use a window function (unboundedPreceding or unboundedFollowing) to implement forward and backward filling, respectively, for a specific column._
_Pandasの代わりにPySparkを使用できます。PySparkにはネイティブライブラリのサポートはありませんが、ウィンドウ関数（unboundedPrecedingまたはunboundedFollowing）を使用して、特定の列に対して前方および後方補完を実装できます。_

_Here, we forward-fill `amount` and specify the primary key as the orderBy column:_
_ここでは、`amount`を前方補完し、主キーをorderBy列として指定します：_

```  
window_spec = Window.partitionBy("cc_num").orderBy("event_time")     
.rowsBetween(Window.unboundedPreceding, Window.currentRow)   
# Forward fill the 'amount' column with missing values   
df_forward_filled = df.withColumn(     
"filled_amount", F.last("amount", ignoreNulls=True).over(window_spec)   
)
```  
```  
window_spec = Window.partitionBy("cc_num").orderBy("event_time")     
.rowsBetween(Window.unboundedPreceding, Window.currentRow)   
# 欠損値を持つ'amount'列を前方補完します   
df_forward_filled = df.withColumn(     
"filled_amount", F.last("amount", ignoreNulls=True).over(window_spec)   
)
```  
_This will sort the data by `event_time` within each `cc_num. So if there is a missing `amount, it will be replaced by the most recent credit card amount on that card._
_これにより、各`cc_num`内で`event_time`によってデータがソートされます。したがって、欠損した`amount`がある場合、それはそのカードの最新のクレジットカードの金額に置き換えられます。_

_Here is the same example for backward-filling missing values:_
_欠損値を後方補完するための同じ例は次のとおりです：_

```  
window_spec_back = Window.partitionBy("cc_num").orderBy("event_time")     
.rowsBetween(Window.currentRow, Window.unboundedFollowing)   
# Backward fill the 'amount' column with missing values   
df_backward_filled = df.withColumn(     
"filled_amount", F.first("amount", ignoreNulls=True).over(window_spec_back))
```  
```  
window_spec_back = Window.partitionBy("cc_num").orderBy("event_time")     
.rowsBetween(Window.currentRow, Window.unboundedFollowing)   
# 欠損値を持つ'amount'列を後方補完します   
df_backward_filled = df.withColumn(     
"filled_amount", F.first("amount", ignoreNulls=True).over(window_spec_back))
```  
_Note that these operations are expensive in Spark and require shuffling and sorting the data over all workers._
_これらの操作はSparkでは高コストであり、すべてのワーカー間でデータのシャッフルとソートが必要です。_

_To scale window functions in PySpark, you need to set a partition key and make sure partition sizes are balanced (if there is a skew in the partition sizes, performance will be negatively impacted)._
_PySparkでウィンドウ関数をスケールするには、パーティションキーを設定し、パーティションサイズが均等であることを確認する必要があります（パーティションサイズに偏りがある場合、パフォーマンスに悪影響を及ぼします）。_

_In contrast, sorting in Pandas is a relatively cheap in-memory operation._
_対照的に、Pandasでのソートは比較的安価なメモリ内操作です。_

_What about filling non-time-series data using imputation?_
_欠損値補完を使用して非時系列データを補完する場合はどうなりますか？_

_In Scikit-Learn pipelines, we can impute missing values using classes in their `impute module, such as the`_
_Scikit-Learnのパイプラインでは、`impute`モジュール内のクラスを使用して欠損値を補完できます。例えば、_

```  
from sklearn.impute import SimpleImputer   
from sklearn.pipeline import Pipeline   
pipeline = Pipeline(steps=[     
('imputer', SimpleImputer(strategy='mean'))   
])   
df_imputed = pd.DataFrame(     
pipeline.fit_transform(df[["amount"]]),     
columns=["amount"]   
)
```  
```  
from sklearn.impute import SimpleImputer   
from sklearn.pipeline import Pipeline   
pipeline = Pipeline(steps=[     
('imputer', SimpleImputer(strategy='mean'))   
])   
df_imputed = pd.DataFrame(     
pipeline.fit_transform(df[["amount"]]),     
columns=["amount"]   
)
```  
_This code replaces all missing values with the mean value computed over the selected columns in your DataFrame._
_このコードは、DataFrame内の選択された列に対して計算された平均値で、すべての欠損値を置き換えます。_

_If the DataFrame stores the training set, this works well._
_もしDataFrameがトレーニングセットを保存している場合、これはうまく機能します。_

_Pipeline objects can be stored with their embedded model in the model registry._
_パイプラインオブジェクトは、モデルレジストリ内の埋め込まれたモデルと共に保存できます。_

_This enables the same Scikit-Learn pipeline object to be downloaded to an inference pipeline, applying the same imputation transformations during inference and thus ensuring no training-serving skew._
_これにより、同じScikit-Learnパイプラインオブジェクトを推論パイプラインにダウンロードでき、推論中に同じ補完変換を適用し、トレーニングとサービスの偏りがないことを保証します。_

_Again, what happens if your data is too large to fit on a single machine?_
_再度、もしデータが単一のマシンに収まらないほど大きい場合はどうなりますか？_

_Scikit-Learn pipelines only work on a single machine, so in this case, you can use declarative MDTs on feature views in Hopsworks._
_Scikit-Learnのパイプラインは単一のマシンでのみ機能するため、この場合はHopsworksのフィーチャービューで宣言的MDTを使用できます。_

_Hopsworks can use either Pandas or Spark as a backend for creating training datasets with feature views, so this solution scales to very large-sized (TBs or larger) training datasets._
_Hopsworksは、フィーチャービューを使用してトレーニングデータセットを作成するためのバックエンドとしてPandasまたはSparkのいずれかを使用できるため、このソリューションは非常に大きなサイズ（TB以上）のトレーニングデータセットにスケールします。_

_In this example, we min_max_scale the amount feature when we create training data using the feature view object:_
_この例では、フィーチャービューオブジェクトを使用してトレーニングデータを作成する際に、amountフィーチャーをmin_max_scaleします：_

```  
from hopsworks.hsfs.builtin_transformations import min_max_scaler   
feature_view = fs.create_feature_view(     
name='transactions_view',     
query=query,     
labels=["fraud_label"],     
transformation_functions = [min_max_scaler("amount")]   
)   
# missing values will be imputed during training data creation   
feature_view.create_training_data(test_size=0.2)
```  
```  
from hopsworks.hsfs.builtin_transformations import min_max_scaler   
feature_view = fs.create_feature_view(     
name='transactions_view',     
query=query,     
labels=["fraud_label"],     
transformation_functions = [min_max_scaler("amount")]   
)   
# トレーニングデータ作成中に欠損値が補完されます   
feature_view.create_training_data(test_size=0.2)
```  
_For more advanced use cases, you can try model-based imputation that uses statistical models to estimate and fill in missing values._
_より高度なユースケースでは、統計モデルを使用して欠損値を推定し補完するモデルベースの補完を試すことができます。_

_See Statistical Analysis with Missing Data by Roderick Little and Donald Rubin (Wiley) for details._
_詳細については、Roderick LittleとDonald Rubin（Wiley）の「欠損データの統計分析」を参照してください。_

###### Data Cleaning as Model-Based Transformations
###### モデルベースの変換としてのデータクリーニング

_Data cleaning can be guided by heuristics, training data statistics, or a model trained on the data._
_データクリーニングは、ヒューリスティック、トレーニングデータの統計、またはデータに基づいてトレーニングされたモデルによってガイドされることがあります。_

_Model-based cleaning is most effective when the features and their distributions remain relatively stable between training and inference._
_モデルベースのクリーニングは、特徴とその分布がトレーニングと推論の間で比較的安定している場合に最も効果的です。_

_An example of data cleaning is the preprocessing done by Meta to clean text data before pretraining LLMs._
_データクリーニングの例として、MetaがLLMの事前トレーニング前にテキストデータをクリーンアップするために行った前処理があります。_

_Pretraining benefits from removing noise from low-quality tokens._
_事前トレーニングは、低品質のトークンからノイズを除去することで利益を得ます。_

_Meta states that when they are training Llama 3.1, “We use a token-distribution Kullback-Leibler divergence to filter out documents containing excessive numbers of outlier tokens compared to the training corpus distribution…we developed a series of data-filtering pipelines…using heuristic filters, NSFW (not safe for work) filters, semantic deduplication approaches, and text classifiers to predict data quality.”_
_Metaは、Llama 3.1をトレーニングしているときに、「トークン分布のKullback-Leiblerダイバージェンスを使用して、トレーニングコーパス分布と比較して外れ値トークンの数が過剰な文書をフィルタリングします…ヒューリスティックフィルタ、NSFW（作業に適さない）フィルタ、意味的重複排除アプローチ、データ品質を予測するためのテキスト分類器を使用して、一連のデータフィルタリングパイプラインを開発しました。」と述べています。_

_This sounds like a chicken-and-egg problem._
_これは鶏と卵の問題のように聞こえます。_

_How do you know what the training corpus distribution is when you are trying to create a clean training corpus?_
_クリーンなトレーニングコーパスを作成しようとしているとき、トレーニングコーパスの分布が何であるかをどうやって知ることができますか？_

_Their solution was, “We used Llama 2 to generate the training data for the text-quality classifiers that are powering Llama 3.”_
_彼らの解決策は、「Llama 2を使用してLlama 3を支えるテキスト品質分類器のトレーニングデータを生成しました。」でした。_

_That is, they assumed that the text for pretraining LLMs follows a stable distribution from version 2 to version 3._
_つまり、彼らはLLMの事前トレーニング用のテキストがバージョン2からバージョン3までの安定した分布に従うと仮定しました。_

_So training data for Llama 3.1 could also be used to train text-quality classifiers for Llama 4, and so on._
_したがって、Llama 3.1のトレーニングデータはLlama 4のテキスト品質分類器をトレーニングするためにも使用できるでしょう。_

_Note that the LLM’s text-quality classifiers only run in the training dataset (or feature) pipeline._
_注意すべきは、LLMのテキスト品質分類器はトレーニングデータセット（またはフィーチャー）パイプラインでのみ実行されるということです。_

_They are not MDTs that run in both training and inference pipelines._
_彼らはトレーニングと推論の両方のパイプラインで実行されるMDTではありません。_

_Data cleaning is needed before training, but you make predictions on unclean data, so you shouldn’t apply data cleaning transformations during inference._
_トレーニングの前にデータクリーニングが必要ですが、汚れたデータに対して予測を行うため、推論中にデータクリーニング変換を適用すべきではありません。_

_There are many good open source libraries that can be used for model-based data cleaning._
_モデルベースのデータクリーニングに使用できる優れたオープンソースライブラリが多数あります。_

_For example, Cleanlab is a Python package that identifies and corrects label errors in training datasets, providing confidence estimates for the correctness of each label._
_例えば、Cleanlabはトレーニングデータセット内のラベルエラーを特定し修正するPythonパッケージであり、各ラベルの正確性に対する信頼度を提供します。_

_[Lightly is an open library for computer vision that creates image embeddings](https://oreil.ly/DKg48) and then uses clustering and similarity search to help select, prioritize, or pseudo-label samples without full manual annotation._
_[Lightlyは、画像埋め込みを作成するコンピュータビジョン用のオープンライブラリであり](https://oreil.ly/DKg48)、その後、クラスタリングと類似性検索を使用して、完全な手動注釈なしでサンプルを選択、優先順位付け、または擬似ラベル付けを支援します。_

_This makes Lightly useful in image tasks where acquiring labeled data is challenging or expensive._
_これにより、ラベル付きデータの取得が困難または高価な画像タスクでLightlyが役立ちます。_

_Cleanlab is more widely used on tabular datasets where it can identify and correct label errors, although it can also be used on text and image datasets._
_Cleanlabは、ラベルエラーを特定し修正できるため、表形式データセットでより広く使用されていますが、テキストや画像データセットにも使用できます。_

###### Target-/Label-Dependent Transformations
###### ターゲット/ラベル依存の変換

_There are some data transformations that are parameterized by properties of the label/target, such as its timestamp._
_ラベル/ターゲットのプロパティ（例えば、タイムスタンプ）によってパラメータ化されるデータ変換があります。_

_Sometimes, you can delay computing features until the label and its properties become known._
_時には、ラベルとそのプロパティが知られるまで特徴の計算を遅らせることができます。_

_This enables you to compute these features only when needed._
_これにより、必要なときにのみこれらの特徴を計算できます。_

_A good example of a label-dependent transformation in the context of credit card fraud detection is time_since_last_transaction, which is calculated relative to the current transaction’s timestamp and the timestamp for the most recent previous transaction:_
_クレジットカード詐欺検出の文脈におけるラベル依存の変換の良い例は、time_since_last_transactionであり、これは現在のトランザクションのタイムスタンプと最も最近の前のトランザクションのタイムスタンプに対して相対的に計算されます：_

```  
def time_since_last_transaction(event_time, prev_ts_transaction):     
return event_time - prev_ts_transaction
```  
```  
def time_since_last_transaction(event_time, prev_ts_transaction):     
return event_time - prev_ts_transaction
```  
###### Expensive Features Are Computed When Needed
###### 高コストの特徴は必要なときに計算される

_Sometimes it is too expensive to precompute features for all entities in feature pipelines._
_時には、フィーチャーパイプライン内のすべてのエンティティの特徴を事前に計算するのは高コストすぎることがあります。_

_If your AI system will not consume all of the features that have been precomputed, you can compute them as MDTs._
_もしあなたのAIシステムが事前に計算されたすべての特徴を消費しない場合、それらをMDTとして計算できます。_

_For example, imagine you write a batch feature pipeline that runs daily to compute `days_since_bank_cr_changed. But your` (re)training pipeline only runs monthly, and the batch inference pipeline using the feature only runs weekly._
_例えば、毎日実行されるバッチフィーチャーパイプラインを書いたと想像してください。`days_since_bank_cr_changed`を計算します。しかし、あなたの（再）トレーニングパイプラインは月に1回しか実行されず、フィーチャーを使用するバッチ推論パイプラインは週に1回しか実行されません。_

_Then you have to recompute `days_since_bank_cr_changed` 7 times before it is used for inference and 30 times before it is used for training._
_そのため、推論に使用される前に`days_since_bank_cr_changed`を7回、トレーニングに使用される前に30回再計算する必要があります。_

_That is a lot of wasteful computation._
_これは非常に無駄な計算です。_

_Instead, your training pipeline can compute `days_since_bank_cr_changed` as a MDT in training and batch inference pipelines._
_その代わりに、トレーニングパイプラインはトレーニングおよびバッチ推論パイプラインでMDTとして`days_since_bank_cr_changed`を計算できます。_

_If all of your features can be implemented as MDTs, you may even be able to eliminate your feature pipelines and thus reduce your operational burden._
_もしすべての特徴をMDTとして実装できるなら、フィーチャーパイプラインを排除し、運用負担を軽減できるかもしれません。_

###### Tokenizers and Chat Templates for LLMs
###### LLMのためのトークナイザーとチャットテンプレート

_When you pass text to an LLM for training or for inference, that text needs to be first transformed into tokens by the LLM’s tokenizer before it is fed into the LLM._
_トレーニングまたは推論のためにテキストをLLMに渡すとき、そのテキストは最初にLLMのトークナイザーによってトークンに変換される必要があります。その後、LLMに供給されます。_

_Every LLM has its own tokenizer, and the process is known as tokenization._
_すべてのLLMには独自のトークナイザーがあり、このプロセスはトークン化として知られています。_

_For example, Llama 3’s tokenizer, on average, tokenizes one word into two to three tokens—each token is, on average, four characters long._
_例えば、Llama 3のトークナイザーは、平均して1つの単語を2〜3のトークンにトークン化します—各トークンは平均して4文字の長さです。_

_Llama 3 has a tokenization dictionary with a vocabulary of 128K tokens._
_Llama 3には、128Kトークンの語彙を持つトークン化辞書があります。_

_Tokenization is an MDT, as it is tightly coupled to the version of your LLM._
_トークン化はMDTであり、あなたのLLMのバージョンに密接に結びついています。_

_For example, Llama 3 tokenized text cannot be fed into a Llama 2 or Llama 4 model._
_例えば、Llama 3でトークン化されたテキストはLlama 2またはLlama 4モデルに供給することはできません。_

_A common problem I have seen among practitioners who fine-tune LLMs is that they encounter skew between training and inference time, due to different versions of_
_私がLLMをファインチューニングする実務者の間で見た一般的な問題は、異なるバージョンのためにトレーニングと推論の時間に偏りが生じることです。_



tokenizers in their training pipeline and online inference pipeline. 
トークナイザーは、トレーニングパイプラインとオンライン推論パイプラインで使用されます。

A solution is to use the Hugging Face (HF) chat template. 
解決策は、Hugging Face (HF) チャットテンプレートを使用することです。

HF chat templates are tightly coupled with the tokenizer, and they define a conversation as a single string that can be tokenized in the format expected by the model: 
HFチャットテンプレートはトークナイザーと密接に結びついており、会話をモデルが期待する形式でトークン化できる単一の文字列として定義します：

```   
from transformers import AutoTokenizer   
tokenizer=AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")   
chat = [     
    {"role": "user", "content": "How do I prevent training/inference skew for tokenization in LLMs?"},     
    {"role": "assistant", "content": "A chat template can help"}   
]   
tokenized_prompt = tokenizer.apply_chat_template(chat, tokenize=True)
``` 
このHFチャットテンプレートを使用することで、トークン化による歪みを防ぐために、トレーニングと推論で同じモデルバージョンがインスタンス化されていることを確認するだけで済みます。

_Text chunking for LLMs for fine-tuning and RAG breaks documents into pieces (pages, paragraphs, sentences, etc.) and is an MIT performed in a feature pipeline._ 
LLMsのファインチューニングとRAGのためのテキストチャンクは、ドキュメントを部分（ページ、段落、文など）に分割し、特徴パイプラインで実行されるMITです。

The chunked text can then be reused at inference time with RAG. 
チャンク化されたテキストは、推論時にRAGで再利用できます。

_Text tokenization, however, is model dependent and, therefore, performed in training and inference pipelines._ 
ただし、テキストトークン化はモデル依存であるため、トレーニングおよび推論パイプラインで実行されます。

You should not couple text chunking with text tokenization if you want to index reusable chunked text for LLMs in a vector index. 
ベクトルインデックスでLLMsの再利用可能なチャンク化されたテキストをインデックス化したい場合、テキストチャンクとテキストトークン化を結びつけるべきではありません。

###### Transformations in Scikit-Learn Pipelines
###### Scikit-Learnパイプラインにおける変換

Scikit-Learn provides a library of transformers that can implement MDTs in both training and inference pipelines without skew. 
Scikit-Learnは、トレーニングおよび推論パイプラインの両方で歪みなくMDTを実装できるトランスフォーマーのライブラリを提供します。

Scikit-Learn also provides a pipeline object to manage both a sequence of transformers and the model. 
Scikit-Learnは、トランスフォーマーのシーケンスとモデルの両方を管理するためのパイプラインオブジェクトも提供します。

You can pickle and save the pipeline object in a model registry, instead of just saving the model. 
モデルを保存するだけでなく、パイプラインオブジェクトをモデルレジストリにピクル化して保存できます。

The pipeline object includes both the transformers and the model, as well as any training data parameters (mean, min, max, and encoding maps) needed to apply the feature transformations. 
パイプラインオブジェクトには、トランスフォーマーとモデルの両方、ならびに特徴変換を適用するために必要なトレーニングデータパラメータ（平均、最小、最大、エンコーディングマップ）が含まれています。

Then, in an inference pipeline, you download the pipeline object (not the model) and use it to apply MDTs and make predictions in a single method call. 
次に、推論パイプラインでは、パイプラインオブジェクト（モデルではなく）をダウンロードし、それを使用してMDTを適用し、単一のメソッド呼び出しで予測を行います。

In the training pipeline, you create and use the pipeline as follows: 
トレーニングパイプラインでは、次のようにパイプラインを作成して使用します：

```   
import joblib   
X_train, X_test, y_train, y_test = fv.train_test_split(test_size=0.2)   
categorical_features = \     
    [ col for col in X_train.columns if X_train[col].dtype == object ]   
numerical_features = \     
    [ col for col in X_train.columns if X_train[col].dtype != object ]   
numeric_transformer = Pipeline(     
    steps=[
        ("imputer", SimpleImputer(strategy="median")),       
        ("scaler", StandardScaler()),     
    ]   
)   
categorical_transformer = Pipeline(     
    steps=[       
        ("encoder", OneHotEncoder(handle_unknown="ignore")),     
    ]   
)   
preprocessor = ColumnTransformer(     
    transformers=[       
        ("num", numeric_transformer, numerical_features),       
        ("cat", categorical_transformer, categorical_features),     
    ]   
)   
clf = Pipeline(     
    steps=[       
        ("preprocessor", preprocessor),       
        ("classifier", LogisticRegression()),     
    ]   
)   
clf.fit(X_train, y_train)   
joblib.dump(clf, "cc_fraud/cc_fraud.pkl")   
mr_model = mr.register_sklearn_model(name=”cc_fraud”, feature_view=fv,..)   
mr_model.save("cc_fraud")
``` 
私たちは、Scikit-Learnパイプラインで一般的に遭遇する大きなNumPy配列を保存/読み込む際に、Pythonのネイティブピクルライブラリよりも効率的であるため、joblibを使用します。

In batch inference, we read a batch of feature values to score from the feature store, download the pipeline object (including the transformers and the model), and make predictions: 
バッチ推論では、特徴ストアからスコアリングするための特徴値のバッチを読み込み、パイプラインオブジェクト（トランスフォーマーとモデルを含む）をダウンロードし、予測を行います：

```   
model_dir = mr.download_model(name="cc_fraud", version=1)   
clf = joblib.load(os.path.join(model_dir, "cc_fraud.pkl"))   
# Get feature data arrived since yesterday for scoring   
df = fv.get_batch_data(start_time=datetime.now()-timedelta(days=1))   
df["predicted_fraud"] = clf.predict(df)
``` 
The model.predict() method applies all of the pipeline transformations before calling predict on the model. 
model.predict()メソッドは、モデルのpredictを呼び出す前に、すべてのパイプライン変換を適用します。

You need to be careful to use the same version of joblib when building the containers for your training and inference pipelines; otherwise, you may have problems deserializing the pipeline. 
トレーニングおよび推論パイプラインのコンテナを構築する際には、同じバージョンのjoblibを使用するように注意が必要です。さもなければ、パイプラインのデシリアライズに問題が発生する可能性があります。



Scikit-Learn has a number of built-in transformations that may be useful in your training and inference pipelines. 
Scikit-Learnには、トレーニングおよび推論パイプラインで役立つ可能性のある多くの組み込み変換があります。

For imputing values, Scikit-Learn transformers can replace missing values, NaNs (“not a number”), or other placeholders with either default values or computed values. 
値を補完するために、Scikit-Learnのトランスフォーマーは、欠損値、NaN（「数値ではない」）、または他のプレースホルダーをデフォルト値または計算された値で置き換えることができます。

The SimpleImputer is a univariate algorithm that imputes missing values for a feature using only nonmissing values for that feature. 
SimpleImputerは、特定の特徴の非欠損値のみを使用して、その特徴の欠損値を補完する単変量アルゴリズムです。

You can define what a missing value is with the `missing_values` parameter (the default is np.nan). 
欠損値が何であるかは、`missing_values`パラメータ（デフォルトはnp.nan）で定義できます。

The available SimpleImputer strategies are mean, median, constant (also set the fill_value parameter to the default value to replace the missing value with), and most_frequent, the mode of that feature. 
利用可能なSimpleImputerの戦略は、平均、中央値、定数（欠損値を置き換えるためのデフォルト値にfill_valueパラメータを設定することも含む）、およびその特徴の最頻値（most_frequent）です。

In contrast, the IterativeImputer implements model-based imputation and uses all features to estimate a missing value (it is a multivariate algorithm). 
対照的に、IterativeImputerはモデルベースの補完を実装し、すべての特徴を使用して欠損値を推定します（これは多変量アルゴリズムです）。

Another more sophisticated technique is to generate multiple imputations and apply an analysis pipeline to the imputations. 
もう一つのより洗練された技術は、複数の補完を生成し、それに分析パイプラインを適用することです。

For categorical variables, Scikit-Learn supports the OneHotEncoder, which is suitable for categorical variables with a low or medium cardinality. 
カテゴリ変数に対して、Scikit-LearnはOneHotEncoderをサポートしており、これは低または中程度のカーディナリティを持つカテゴリ変数に適しています。

You can exclude infrequent categories with the min_frequency parameter, which removes categories with a cardinality smaller than min_frequency. 
min_frequencyパラメータを使用して、頻度の低いカテゴリを除外できます。これにより、カーディナリティがmin_frequencyより小さいカテゴリが削除されます。

You can also specify a default category called infrequent by setting the handle_unknown parameter to 'infrequent_if_exist', which will set the category for any new category encountered in inference to infrequent. 
handle_unknownパラメータを'infrequent_if_exist'に設定することで、infrequentというデフォルトカテゴリを指定することもでき、推論中に遭遇した新しいカテゴリのカテゴリをinfrequentに設定します。

You can also set handle_unknown to ignore, which will produce a one-hot encoded array with zeros for all columns. 
handle_unknownをignoreに設定すると、すべての列に対してゼロの値を持つワンホットエンコードされた配列が生成されます。

The default for handle_unknown is to raise an error if a new category is encountered during inference. 
handle_unknownのデフォルトは、推論中に新しいカテゴリが遭遇した場合にエラーを発生させることです。

Scikit-Learn also supports an OrdinalEncoder for categories with a natural ordering and a TargetEncoder for encoding unordered categories with high cardinality, for example, a zip code in the United States (US). 
Scikit-Learnは、自然な順序を持つカテゴリ用のOrdinalEncoderと、高カーディナリティの順序なしカテゴリをエンコードするためのTargetEncoderもサポートしています。例えば、アメリカ合衆国の郵便番号などです。

For numerical variables, Scikit-Learn provides a number of classes in the sklearn.preprocessing package. 
数値変数に対して、Scikit-Learnはsklearn.preprocessingパッケージ内にいくつかのクラスを提供しています。

The StandardScaler class standardizes a numerical feature, and it implements Scikit-Learn’s Transformer API to compute the mean and standard deviation of a training set (X_train), which are then saved in the Pipeline object. 
StandardScalerクラスは数値特徴を標準化し、Scikit-LearnのトランスフォーマーAPIを実装してトレーニングセット（X_train）の平均と標準偏差を計算し、それらはPipelineオブジェクトに保存されます。

The MinMaxScaler scales features to lie between zero and one (or some other minimum and maximum), preserving the shape of the distribution. 
MinMaxScalerは特徴をゼロと一の間（または他の最小値と最大値の間）にスケーリングし、分布の形状を保持します。

MaxAbsScaler is better at preserving sparsity than MinMaxScaler. 
MaxAbsScalerはMinMaxScalerよりもスパース性を保持するのに優れています。

Other important numerical transformations are quantile and power transforms that perform monotonic transformations to approximate the Gaussian, preserving the rank order of the data. 
他の重要な数値変換には、データの順位を保持しながらガウス分布を近似する単調変換を行う分位数変換とパワー変換があります。

They can both map feature data from any distribution to a distribution that approximates the Gaussian distribution. 
これらはどちらも、任意の分布からガウス分布を近似する分布に特徴データをマッピングできます。

From the power transforms, Scikit-Learn supports both the Box-Cox and Yeo-Johnson algorithms. 
パワー変換から、Scikit-LearnはBox-CoxおよびYeo-Johnsonアルゴリズムの両方をサポートしています。

In Scikit-Learn, you can normalize a NumPy array (or Pandas DataFrame backed by a NumPy array) by applying the `preprocessing.normalize` function to specify one of the available norms: l1, l2 (default), or max. 
Scikit-Learnでは、`preprocessing.normalize`関数を適用して、利用可能なノルムの1つ（l1、l2（デフォルト）、またはmax）を指定することで、NumPy配列（またはNumPy配列に基づくPandas DataFrame）を正規化できます。

The l1 norm updates (scales) the values so that the sum of the absolute values is one, the l2 norm scales the values so that the sum of the squares of the values is equal to one, and the max norm scales the values so that the largest absolute value within each sample is 1. 
l1ノルムは値を更新（スケーリング）して絶対値の合計が1になるようにし、l2ノルムは値をスケーリングして値の二乗の合計が1になるようにし、maxノルムは各サンプル内の最大絶対値が1になるように値をスケーリングします。

For example, with the l2 norm, the array of values [3, 4, 0] would be normalized to [0.6, 0.8, 0]. 
例えば、l2ノルムを使用すると、値の配列[3, 4, 0]は[0.6, 0.8, 0]に正規化されます。

As of 2025, the transformation algorithms in Scikit-Learn’s preprocessing package operate on NumPy arrays and do not natively support Arrow-backed DataFrames. 
2025年現在、Scikit-Learnの前処理パッケージの変換アルゴリズムはNumPy配列で動作し、ArrowバックのDataFrameをネイティブにサポートしていません。

Arrow-backed DataFrames, such as those in PySpark and Pandas, are more scalable for large datasets. 
PySparkやPandasのようなArrowバックのDataFrameは、大規模データセットに対してよりスケーラブルです。

In the next section, we will introduce feature transformations for Hopsworks Feature Views that work with Arrow-backed DataFrames. 
次のセクションでは、ArrowバックのDataFrameで動作するHopsworks Feature Viewsのための特徴変換を紹介します。

###### Transformations in Feature Views
###### 特徴ビューにおける変換

Feature views in Hopsworks support the execution of transformation functions when reading features from the feature store. 
Hopsworksの特徴ビューは、特徴ストアから特徴を読み込む際に変換関数の実行をサポートしています。

There are built-in transformation functions—such as one_hot_encoder, min_max_scalar, and label_encoder—that can be defined as part of a feature view. 
one_hot_encoder、min_max_scalar、label_encoderなどの組み込み変換関数があり、これらは特徴ビューの一部として定義できます。

They take features in the feature view as input parameters and return one or more transformed feature values. 
これらは特徴ビュー内の特徴を入力パラメータとして受け取り、1つ以上の変換された特徴値を返します。

You can also write your own user-defined (custom) transformation functions for features in a feature view. 
特徴ビュー内の特徴に対して独自のユーザー定義（カスタム）変換関数を書くこともできます。

Transformation functions are executed in the Hopsworks client after it has read data with a feature view but before it returns the feature data. 
変換関数は、Hopsworksクライアントが特徴ビューでデータを読み込んだ後、特徴データを返す前に実行されます。

Feature view transformations are MDTs that guarantee no skew between training and inference. 
特徴ビューの変換は、トレーニングと推論の間に偏りがないことを保証するMDTです。

Any training data parameters (mean, min, max, and encoding maps) needed to apply feature transformations are stored in training dataset objects that are saved in the model registry, along with the model and the feature view used to create the training data. 
特徴変換を適用するために必要なトレーニングデータパラメータ（平均、最小、最大、エンコーディングマップ）は、トレーニングデータを作成するために使用されたモデルおよび特徴ビューとともにモデルレジストリに保存されるトレーニングデータセットオブジェクトに保存されます。

Then in an inference pipeline, the model, along with its feature view and training data object, is downloaded, and its feature view retrieves feature data and applies MDTs to create feature vectors used for model prediction. 
その後、推論パイプラインでは、モデルとその特徴ビューおよびトレーニングデータオブジェクトがダウンロードされ、特徴ビューが特徴データを取得し、MDTを適用してモデル予測に使用される特徴ベクトルを作成します。

In the following code snippet, we define a feature view over credit card transaction features and declaratively apply three built-in feature transformations to three different features—min_max_scaler to the amount feature, one_hot_encoder to the category feature, and label_encoder to the fraud label. 
次のコードスニペットでは、クレジットカード取引の特徴に対する特徴ビューを定義し、amount特徴にmin_max_scaler、category特徴にone_hot_encoder、fraudラベルにlabel_encoderという3つの異なる特徴に3つの組み込み特徴変換を宣言的に適用します。

```python
from hopsworks.hsfs.builtin_transformations import min_max_scaler, label_encoder, one_hot_encoder
fv = fs.create_feature_view(
    name='transactions',
    query=fg_credit_card.select_features(),
    labels=["fraud"],
    transformation_functions = [
        one_hot_encoder("category"),
        min_max_scaler("amount"),
        label_encoder("fraud")
    ]
)
```

When you create a feature view, the transformation_functions list specifies transformations that are applied to named features in the feature view. 
特徴ビューを作成するとき、transformation_functionsリストは特徴ビュー内の名前付き特徴に適用される変換を指定します。

Each entry in the list contains the name of the transformation function and the names of features from the feature view as input parameters. 
リスト内の各エントリには、変換関数の名前と特徴ビューからの特徴の名前が入力パラメータとして含まれています。

You can also include index columns or helper columns as parameters to a transformation function. 
インデックス列やヘルパー列を変換関数のパラメータとして含めることもできます。

In the above example, the transformation functions are univariate (one-to-one) functions that take a single feature as input and return a transformed value as output. 
上記の例では、変換関数は単変量（1対1）関数であり、単一の特徴を入力として受け取り、変換された値を出力として返します。

You can also write custom multivariate functions that can take one to many features as input and return one to many transformed features as output. 
1つ以上の特徴を入力として受け取り、1つ以上の変換された特徴を出力として返すカスタム多変量関数を書くこともできます。

If no feature names are provided explicitly in the transformation_functions list, the transformation function will default to using the feature name(s) in the feature view that matches the name of the parameter(s) in the transformation function definition. 
transformation_functionsリストに特徴名が明示的に提供されていない場合、変換関数は変換関数定義内のパラメータ名と一致する特徴ビュー内の特徴名を使用することがデフォルトとなります。

This works well with user-defined transformations, but not with built-in transformations. 
これはユーザー定義の変換にはうまく機能しますが、組み込みの変換には機能しません。

It’s good practice to be explicit in the feature view definition and provide feature names so that developers can see what transformations are applied to which features. 
特徴ビューの定義で明示的に特徴名を提供することは良い習慣であり、開発者がどの特徴にどの変換が適用されているかを確認できるようにします。

Let’s look at how transformation functions for feature views work in practice. 
特徴ビューの変換関数が実際にどのように機能するかを見てみましょう。

In the following code snippet, we use a feature view to read DataFrames containing the features and labels in the training and test sets. 
次のコードスニペットでは、特徴ビューを使用してトレーニングセットとテストセットの特徴とラベルを含むDataFrameを読み込みます。

By default, the transformation functions are executed inside the train_test_split method and the returned DataFrames contain the transformed feature data: 
デフォルトでは、変換関数はtrain_test_splitメソッド内で実行され、返されるDataFrameには変換された特徴データが含まれます。

```python
X_train, X_test, y_train, y_test = fv.train_test_split(test_size=0.1)
```

Similarly, when we read a batch of inference data, it will, by default, return transformed feature data. 
同様に、推論データのバッチを読み込むと、デフォルトで変換された特徴データが返されます。

Here, however, we read untransformed inference data with the feature view by setting Transformed=False: 
ただし、ここではTransformed=Falseを設定することで、特徴ビューを使用して変換されていない推論データを読み込みます。

```python
features = fv.get_batch_data(
    start_date=(datetime.now() - timedelta(1)), transformed=False
)
```

For the feature view’s online APIs, when you read feature vectors, the transformation functions are, again, executed transparently in the client by default (transformed=True is default): 
特徴ビューのオンラインAPIでは、特徴ベクトルを読み込むとき、変換関数は再びクライアント内で透明に実行されます（transformed=Trueがデフォルトです）。

```python
features = fv.get_feature_vector(serving_keys={"cc_num": "1234 0432 0122 9833"})
```

Transformation functions can change the schema of the feature data read from the feature view, as they can return more or fewer columns than there are features in the feature view. 
変換関数は、特徴ビューから読み込まれた特徴データのスキーマを変更することができ、特徴ビューにある特徴の数よりも多くまたは少ない列を返すことができます。

For example, one_hot_encoding can transform a string column into
例えば、one_hot_encodingは文字列列を変換できます。



hundreds of columns in a returned DataFrame (one column for each category). 
返されたDataFrameには数百の列があり（各カテゴリごとに1列）、

The feature view, however, ensures that the number and order of columns in the returned data will be consistent when reading training and inference data. 
しかし、フィーチャービューは、トレーニングデータと推論データを読み込む際に、返されるデータの列の数と順序が一貫していることを保証します。

As a developer, you only need to work with the model’s feature view and the training/inference data created by it. 
開発者としては、モデルのフィーチャービューとそれによって作成されたトレーニング/推論データのみを扱えばよいです。

You generally do not work with the model signature—the schema of the DataFrame input to the model. 
一般的に、モデルのシグネチャ（モデルへのDataFrame入力のスキーマ）を扱うことはありません。

The feature view is responsible for mapping its features to and from the model signature. 
フィーチャービューは、その特徴をモデルのシグネチャにマッピングする責任があります。

This means, for example, that when working with categorical features, you only work with the string column (in the feature view), not with the one-hot encoded columns (in the training/inference data). 
例えば、カテゴリカルフィーチャーを扱う場合、フィーチャービュー内の文字列列のみを扱い、トレーニング/推論データ内のワンホットエンコードされた列は扱いません。

You can also define your own custom transformations for feature views as user-defined transformation functions. 
フィーチャービューに対して、ユーザー定義の変換関数として独自のカスタム変換を定義することもできます。

A user-defined transformation function is a Python or Pandas UDF with the @hopsworks.udf annotation. 
ユーザー定義の変換関数は、@hopsworks.udfアノテーションを持つPythonまたはPandas UDFです。

Pandas UDFs can be scaled to process large volumes of data, in either Pandas or PySpark, while Python UDFs do not scale well. 
Pandas UDFは、PandasまたはPySparkのいずれかで大量のデータを処理するためにスケールできますが、Python UDFはうまくスケールしません。

Python UDFs, however, have lower latency in online inference pipelines than Pandas UDFs. 
ただし、Python UDFはPandas UDFよりもオンライン推論パイプラインでのレイテンシが低くなります。

For this reason, when possible, the best practice is to write transformation functions as Python functions that can be executed as either a Pandas UDF (in a feature/training/batch-inference pipeline) or a Python UDF (in an online inference pipeline). 
このため、可能な限り、変換関数はPandas UDF（フィーチャー/トレーニング/バッチ推論パイプライン内）またはPython UDF（オンライン推論パイプライン内）として実行できるPython関数として記述するのがベストプラクティスです。

We call these types of transformation functions _mixed-mode_ UDFs, as they can run as either Pandas UDFs or Python UDFs, depending on the context. 
これらのタイプの変換関数を_mixed-mode_ UDFと呼びます。これは、文脈に応じてPandas UDFまたはPython UDFとして実行できるためです。

In general, only simple UDFs can be written as mixed-mode UDFs. 
一般的に、単純なUDFのみがmixed-mode UDFとして記述できます。

Here is an example of a mixed-mode transformation function that encodes information about how much a transaction deviates from the mean transaction amount from the training dataset. 
以下は、トレーニングデータセットの平均取引額からの取引の偏差をエンコードするmixed-mode変換関数の例です。

Hopsworks automatically fills in statistics for the training dataset in the stats object: 
Hopsworksは、statsオブジェクト内のトレーニングデータセットの統計を自動的に埋め込みます：

```   
stats = TransformationStatistics("amount")   
@hopsworks.udf(float)   
def transaction_amount_deviation(amount, statistics=stats):     
    return amount / statistics.amount.mean
```

In a training pipeline, `amount is a` `pd.Series and` `statistics.amount.mean is a` scalar, so it executes as a vectorized function in Pandas. 
トレーニングパイプラインでは、`amountは` `pd.Seriesであり、` `statistics.amount.meanは` スカラーであるため、Pandas内でベクトル化された関数として実行されます。

However, in online inference, ``` amount is a float, so the function executes as a low-latency Python UDF. 
ただし、オンライン推論では、``` amountはfloatであるため、関数は低レイテンシのPython UDFとして実行されます。

We can also explicitly define a user-defined transformation function to run in Pandas _mode, in both training and inference. 
トレーニングと推論の両方でPandas _modeで実行されるユーザー定義の変換関数を明示的に定義することもできます。

This can be executed as a Pandas UDF by_ PySpark. 
これは、PySparkによってPandas UDFとして実行できます。

Here, we compute days_to_card_expiry in a transformation function that takes as inputs two features from a feature view, the `cc_expiry_date and` ``` event_time, that it expects are pd.Series containing dates. 
ここでは、`cc_expiry_date`と``` event_timeの2つのフィーチャーを入力として受け取り、日付を含むpd.Seriesであることを期待する変換関数内でdays_to_card_expiryを計算します。

It computes and returns days_to_card_expiry with int value for each input:   
@hopsworks.udf(return_type=int, mode="pandas")   
def days_to_card_expiry(cc_expiry_date, event_time):     
    return (cc_expiry_date - event_time).dt.days
```

In online inference, this transformation function will also take a Pandas DataFrame as input, which can add a few hundreds of microseconds of additional latency compared with Python UDFs. 
オンライン推論では、この変換関数もPandas DataFrameを入力として受け取り、Python UDFと比較して数百マイクロ秒の追加レイテンシを加える可能性があります。

As this transformation function does not include training data statistics, it can also be used as ODT in feature/online inference pipelines in Hopsworks (see the next section). 
この変換関数はトレーニングデータの統計を含まないため、Hopsworksのフィーチャー/オンライン推論パイプラインでODTとしても使用できます（次のセクションを参照）。

Sometimes features can be implemented as either an MIT or an MDT. 
時には、フィーチャーはMITまたはMDTのいずれかとして実装できます。

For example, in Chapter 6 we described how to compute days_to_card_expiry with an MIT in a feature pipeline. 
例えば、第6章では、フィーチャーパイプラインでMITを使用してdays_to_card_expiryを計算する方法について説明しました。

The feature pipeline, however, will have to run daily to ensure ``` days_to_card_expiry is correct. 
ただし、フィーチャーパイプラインは、``` days_to_card_expiryが正しいことを保証するために、毎日実行する必要があります。

If the feature pipeline fails to run on a given day (or runs at any time other than midnight), then clients risk reading incorrect feature data. 
特定の日にフィーチャーパイプラインが実行されなかった場合（または真夜中以外の時間に実行された場合）、クライアントは不正確なフィーチャーデータを読み取るリスクがあります。

There is also the operational overhead of operating the feature pipeline, which you don’t have with the MDT that is only run when needed in training and inference pipelines. 
フィーチャーパイプラインを運用するための運用オーバーヘッドもありますが、これはトレーニングおよび推論パイプラインで必要なときにのみ実行されるMDTにはありません。

Figure 7-3 shows flowcharts that help guide you in how to implement ``` days_to_card_expiry: as an MIT, MDT, or ODT. 
図7-3は、``` days_to_card_expiryをMIT、MDT、またはODTとして実装する方法をガイドするフローチャートを示しています。

_Figure 7-3. These flowcharts guide you on how to implement the days_to_card_expiry_ _feature, depending on whether it will be (a) used by batch ML systems or (b) computed_ _at real time._ 
_図7-3. これらのフローチャートは、days_to_card_expiryフィーチャーを実装する方法をガイドします。これは、（a）バッチMLシステムで使用されるか、（b）リアルタイムで計算されるかによります。_

If the feature will be used by a batch ML system, you should implement the feature as an MDT if you will not reuse the computed feature or if you don’t want the overhead of the feature pipeline. 
フィーチャーがバッチMLシステムで使用される場合、計算されたフィーチャーを再利用しない場合やフィーチャーパイプラインのオーバーヘッドを避けたい場合は、フィーチャーをMDTとして実装する必要があります。

Otherwise, it should be an MIT. 
そうでなければ、それはMITであるべきです。

If days_to_card_expiry is a real-time feature that requires at least one request time parameter to be computed, you should implement it as an MDT if you do not want to be able to precompute the feature using historical data and save it in the feature store for use by many models. 
days_to_card_expiryが、計算に少なくとも1つのリクエスト時間パラメータを必要とするリアルタイムフィーチャーである場合、歴史的データを使用してフィーチャーを事前計算し、多くのモデルで使用するためにフィーチャーストアに保存したくない場合は、MDTとして実装する必要があります。

Otherwise, it should be an ODT. 
そうでなければ、それはODTであるべきです。

In our other example user-defined transformation, transaction_amount_deviation has to be an MDT as it takes amount as a request time parameter and a training data statistic (amount.mean) as a parameter. 
別の例のユーザー定義変換であるtransaction_amount_deviationは、amountをリクエスト時間パラメータとして受け取り、トレーニングデータ統計（amount.mean）をパラメータとして受け取るため、MDTでなければなりません。

ODTs do not have training data statistics as parameters, as they are computed offline in feature pipelines (where there is no training data, only reusable feature data). 
ODTはトレーニングデータ統計をパラメータとして持たず、フィーチャーパイプラインでオフラインで計算されます（トレーニングデータはなく、再利用可能なフィーチャーデータのみがあります）。

User-defined transformation functions are attached to feature views in the same way as built-in transformation functions are: 
ユーザー定義の変換関数は、組み込みの変換関数と同様にフィーチャービューに添付されます：

```   
fv = fs.create_feature_view(     
    ... 
    transformation_functions = \       
        [ days_to_card_expiry("cc_expiry_date", "event_time")     ]   
)
```

You can read the preceding syntax as follows: the days_to_card_expiry transforma‐ tion function is applied to the `cc_expiry_date and` `event_time features in the fea‐` ture view. 
前述の構文は次のように読むことができます：days_to_card_expiry変換関数は、フィーチャービュー内の`cc_expiry_date`と`event_time`フィーチャーに適用されます。

There is no days_to_card_expiry feature defined in the feature view, just the transformation function to create it. 
フィーチャービューにはdays_to_card_expiryフィーチャーは定義されておらず、それを作成するための変換関数のみがあります。

The days_to_card_expiry function is run as a Pandas UDF in a training pipeline and a batch inference pipeline. 
days_to_card_expiry関数は、トレーニングパイプラインとバッチ推論パイプラインでPandas UDFとして実行されます。

If you need to create large volumes of training data, you should write a training dataset pipeline in PySpark that uses one of the `fv.create_train*(..) methods to save the training` data as files. 
大量のトレーニングデータを作成する必要がある場合は、`fv.create_train*(..)`メソッドの1つを使用してトレーニングデータをファイルとして保存するPySparkのトレーニングデータセットパイプラインを記述する必要があります。

PySpark will partition the DataFrame across many workers and execute the transformation function as a Pandas UDF at each worker, with the workers inde‐ pendently saving the training data they create as files. 
PySparkはDataFrameを多くのワーカーに分割し、各ワーカーでPandas UDFとして変換関数を実行し、ワーカーは独立して作成したトレーニングデータをファイルとして保存します。

###### On-Demand Transformations
同じ変換関数は、フィーチャービューで使用されるのと同様に、トレーニングデータ統計をパラメータとして含まない限り、HopsworksでODTとして使用できます。

The same transformation functions used in feature views can be used as ODTs in Hopsworks as long as they do not include training data statistics as a parameter. 
ODTは、リクエスト時間パラメータとフィーチャービューで読み取られる事前計算されたフィーチャーの組み合わせを持つことがあります。

ODTs may have a combination of request-time parameters and precomputed features read with the feature view. 
時には、推論ヘルパー列をフィーチャービューに追加します。これにより、ODTを計算するために使用される事前計算されたフィーチャーデータが提供されます。

Sometimes you add inference helper columns to the feature view, as they provide precomputed feature data that is used to compute an ODT. 
ODTs differ from MDTs in where they are registered. 
ODTは、MDTとは異なり、どこに登録されるかが異なります。

You register ODTs with a feature group rather than with a feature view, as ODTs can be executed in feature pipelines. 
ODTはフィーチャーパイプラインで実行できるため、フィーチャービューではなくフィーチャーグループに登録します。

Feature views know which of their features are computed as ODTs and compute them in online inference pipelines. 
フィーチャービューは、どのフィーチャーがODTとして計算されるかを知っており、オンライン推論パイプラインでそれらを計算します。

ODTs can also be univariate or multivariate functions. 
ODTは、単変量または多変量関数であることもできます。

In the following code, a real-time feature, days_to_card_expiry, is defined for ``` cc_trans_fg: 
以下のコードでは、リアルタイムフィーチャーであるdays_to_card_expiryが``` cc_trans_fgのために定義されています：

```   
fg = feature_store.create_feature_group(name="cc_trans_fg",           
    version=1,           
    description="Transaction Features",           
    online_enabled=True,           
    primary_key=['id'],           
    event_time='event_time'           
    transformation_functions=             
        [days_to_card_expiry("cc_expiry_date", "event_time")]           
)   
fg.insert(df) # transformation functions are run on insertion
```

The ODT is executed in this feature pipeline when you call `fg.insert(df). 
ODTは、`fg.insert(df)`を呼び出すと、このフィーチャーパイプラインで実行されます。

The names of the parameters for the `days_to_card_expiry function need to match the` names of columns in df; otherwise, you will get an error. 
`days_to_card_expiry`関数のパラメータ名は、df内の列名と一致する必要があります。そうでなければ、エラーが発生します。

Sometimes a df can contain columns used to compute the ODT, but those columns are not features in the feature group. 
時には、dfがODTを計算するために使用される列を含むことがありますが、それらの列はフィーチャーグループ内のフィーチャーではありません。

In this case, you can tell the ODT to `drop those columns from` `df after the` feature has been computed: 
この場合、ODTに対して、フィーチャーが計算された後に`dfからこれらの列を削除する`ように指示できます：

```   
@hopsworks.udf(return_type=float, drop=["cc_expiry_date"])
```

MDTs can also use the same `drop syntax to drop columns. 
MDTも同じ`drop構文を使用して列を削除できます。

In Chapter 11, we will look at how both ODTs and MDTs are executed in online inference pipelines. 
第11章では、ODTとMDTの両方がオンライン推論パイプラインでどのように実行されるかを見ていきます。

###### PyTorch Transformations
We switch tracks now to look at transformations on unstructured data (image, audio, video, or text data). 
ここで、非構造化データ（画像、音声、動画、またはテキストデータ）に対する変換を見ていきます。

ML systems trained with unstructured data typically use deep learning algorithms and transform the data into tensors for model input. 
非構造化データでトレーニングされたMLシステムは、通常、深層学習アルゴリズムを使用し、データをモデル入力用のテンソルに変換します。

_Convolu‐_ _tional neural networks (CNNs) and_ _transformer architectures (transformers) are the_ most popular deep learning model architectures. 
_畳み込みニューラルネットワーク（CNN）と_ _トランスフォーマーアーキテクチャ（トランスフォーマー）は、最も人気のある深層学習モデルアーキテクチャです。

PyTorch is the most popular frame‐ work for deep learning, with alternatives including TensorFlow and JAX. 
PyTorchは深層学習のための最も人気のあるフレームワークであり、TensorFlowやJAXなどの代替手段もあります。

In ML systems built with PyTorch, we can also benefit from refactoring our data transformation code into MITs, MDTs, and ODTs in FTI pipelines. 
PyTorchで構築されたMLシステムでは、FTIパイプライン内でデータ変換コードをMIT、MDT、およびODTにリファクタリングすることで利益を得ることができます。

These data trans‐ formations will, however, output tensors or work with tensors—up to now, we have only looked at MITs, MDTs, and ODTs that work with tabular data. 
ただし、これらのデータ変換はテンソルを出力するか、テンソルで作業します。これまで、私たちは表形式データで動作するMIT、MDT、およびODTのみを見てきました。



We will look at PyTorch transformations from the context of an example ML system that predicts your celebrity twin using an image classification model.[1] 
私たちは、画像分類モデルを使用してあなたの有名人の双子を予測する例のMLシステムの文脈からPyTorchの変換を見ていきます。[1]

Figure 7-4 shows a real-time ML system based on the FTI architecture. 
図7-4は、FTIアーキテクチャに基づくリアルタイムMLシステムを示しています。

The training pipeline fine-tunes a ResNet model using the CelebA dataset. 
トレーニングパイプラインは、CelebAデータセットを使用してResNetモデルを微調整します。

The online inference pipeline takes an uploaded image of a person as input, the image is transformed into an input tensor, and the model predicts the closest-matching celebrity by using the input tensor. 
オンライン推論パイプラインは、アップロードされた人物の画像を入力として受け取り、その画像を入力テンソルに変換し、モデルは入力テンソルを使用して最も一致する有名人を予測します。

The source code for this example is found in the book’s GitHub repository. 
この例のソースコードは、本のGitHubリポジトリにあります。

_Figure 7-4. A real-time ML system that predicts your celebrity twin using image classification. It uses PyTorch and Torchvision. Some image preprocessing is offloaded to the feature pipeline and executed in ODTs and image augmentation. Other image preprocessing tasks are executed as MDTs in both the training and online inference pipelines._ 
_図7-4. 画像分類を使用してあなたの有名人の双子を予測するリアルタイムMLシステム。PyTorchとTorchvisionを使用しています。一部の画像前処理はフィーチャーパイプラインにオフロードされ、ODTsおよび画像拡張で実行されます。他の画像前処理タスクは、トレーニングおよびオンライン推論パイプラインの両方でMDTsとして実行されます。_

The benefit of the FTI architecture in this example is that it shifts image transformations from the training pipeline to the feature pipeline. 
この例におけるFTIアーキテクチャの利点は、画像変換をトレーニングパイプラインからフィーチャーパイプラインに移すことです。

This reduces the number of image transformations that are performed on CPUs in the training pipeline, before the input tensors are passed to the GPU for model training. 
これにより、入力テンソルがモデルのトレーニングのためにGPUに渡される前に、トレーニングパイプラインでCPU上で実行される画像変換の数が減ります。

If training is bottlenecked on high CPU load due to a large amount of image preprocessing, offloading transformations to the feature pipeline will increase GPU utilization during training. 
トレーニングが大量の画像前処理による高いCPU負荷でボトルネックになっている場合、変換をフィーチャーパイプラインにオフロードすることで、トレーニング中のGPUの利用率が向上します。

The feature pipeline performs the following tasks: image resizing, image centering, jitter control, and image augmentation. 
フィーチャーパイプラインは、次のタスクを実行します：画像のリサイズ、画像のセンタリング、ジッター制御、および画像拡張。

Image augmentation occurs when you create many variations on the same input image for training data—you can flip an image, change its colors, or erase part of an image randomly (for self-supervised learning with transformers). 
画像拡張は、トレーニングデータのために同じ入力画像の多くのバリエーションを作成する際に発生します。画像を反転させたり、色を変更したり、画像の一部をランダムに消去したりできます（トランスフォーマーを使用した自己教師あり学習のために）。

Image augmentation helps CNNs generalize better, as the different variations of the same image prevent the model from overfitting on a single image by learning features that are invariant to transformations. 
画像拡張は、同じ画像の異なるバリエーションが、変換に対して不変な特徴を学ぶことによってモデルが単一の画像に過剰適合するのを防ぐため、CNNがより良く一般化するのに役立ちます。

Image augmentation happens after we resize, center crop, and color jitter images. 
画像拡張は、画像をリサイズし、センタークロップし、色のジッターを適用した後に行われます。

So if we want to migrate `ImageAugmentation from the training pipeline to the feature` pipeline, we also need to migrate `Resize,` `CenterCrop, and` `ColorJitter to the feature pipeline to run as ODTs. 
したがって、`ImageAugmentationをトレーニングパイプラインからフィーチャーパイプラインに移行したい場合、`Resize、` `CenterCrop、および` `ColorJitterをフィーチャーパイプラインに移行してODTsとして実行する必要があります。

We will also need to run those transformations in the online inference pipeline on uploaded images. 
また、アップロードされた画像に対してオンライン推論パイプラインでそれらの変換を実行する必要があります。

The feature pipeline will output transformed and augmented images as PNG files. 
フィーチャーパイプラインは、変換された拡張画像をPNGファイルとして出力します。

In both training and online inference, we need to convert the PNG files to tensors, which we perform in MDTs. 
トレーニングとオンライン推論の両方で、PNGファイルをテンソルに変換する必要があり、これはMDTsで実行します。

PyTorch provides a library for image transformations called Torchvision v2, and it supports built-in transformations for images. 
PyTorchは、Torchvision v2という画像変換用のライブラリを提供しており、画像のための組み込み変換をサポートしています。

The following code snippet shows how to define a custom ImageAugmentation transformation by composing transformation functions: 
以下のコードスニペットは、変換関数を組み合わせてカスタムImageAugmentation変換を定義する方法を示しています：

```  
import torchvision.transforms.v2 as v2  
class ImageAugmentation(nn.Module):     
    def __init__(self, flip_prob=0.5, rotation_range=(-30, 30)):       
        self.flip_prob = flip_prob       
        self.rotation_range = rotation_range     
    def forward(self, img):       
        …   
on_demand_transforms = v2.Compose([     
    v2.Resize(...),     
    v2.CenterCrop(...),   
])   
model_independent_transforms = v2.Compose([     
    v2.Resize(...),     
    v2.CenterCrop(...),     
    ImageAugmentation(...)   
])   
model_dependent_transforms = v2.Compose([     
    v2.ToImage(...),     
    v2.ToDtype(...),     
    v2.Normalize(...)   
])
```

PyTorch provides datasets as a data structure to store your features and labels. 
PyTorchは、特徴とラベルを保存するためのデータ構造としてデータセットを提供します。

There are pre-created datasets, and you can create your own custom datasets using the provided base classes. 
事前に作成されたデータセットがあり、提供されたベースクラスを使用して独自のカスタムデータセットを作成できます。

You can apply the transformations to a dataset in PyTorch before training a model, as shown here:  
PyTorchでモデルをトレーニングする前に、データセットに変換を適用できます。以下に示します：

```  
dataset = datasets.ImageFolder(root='images/train',     
    transform=model_independent_transforms )   
dataloader = DataLoader(dataset, batch_size=32, num_workers=4)   
for images, labels in dataloader:     
    # Your training code goes here
```

From this example PyTorch system, you can see the benefits of the FTI pipeline architecture in improved code modularity and preprocessing images using feature pipelines. 
この例のPyTorchシステムから、FTIパイプラインアーキテクチャの利点が、コードのモジュール性の向上とフィーチャーパイプラインを使用した画像の前処理にあることがわかります。

###### Using pytest
Transformation functions and feature functions from feature pipelines create features. 
フィーチャーパイプラインからの変換関数とフィーチャー関数は、フィーチャーを作成します。

Once a feature has been created and is used by downstream training or inference pipelines, then between the function that creates the feature and the user of the feature, there is an implicit agreement that the feature logic should not change unexpectedly. 
フィーチャーが作成され、下流のトレーニングまたは推論パイプラインで使用されると、フィーチャーを作成する関数とフィーチャーのユーザーの間には、フィーチャーロジックが予期せず変更されないという暗黙の合意があります。

Changes in how a feature is computed can break clients. 
フィーチャーの計算方法の変更は、クライアントを壊す可能性があります。

Unit tests help ensure that developers do not make unexpected changes to how features are computed, and that helps developers make safe, incremental upgrades to their ML pipelines. 
ユニットテストは、開発者がフィーチャーの計算方法に予期しない変更を加えないようにし、開発者がMLパイプラインに安全で段階的なアップグレードを行うのに役立ちます。

As much of the focus of this book is on Python, we will look in detail at the most popular unit testing framework in Python, pytest, and how we can use it to test transformation functions and, later, feature pipelines. 
この本の多くの焦点がPythonにあるため、Pythonで最も人気のあるユニットテストフレームワークであるpytestを詳細に見ていき、変換関数や後のフィーチャーパイプラインをテストするためにどのように使用できるかを見ていきます。

If you write feature pipelines in another language, such as SQL or Java/Spark, then you can use other testing frameworks, such as unit testing with dbt and JUnit, respectively. 
SQLやJava/Sparkなどの別の言語でフィーチャーパイプラインを書く場合は、それぞれdbtやJUnitを使用したユニットテストなど、他のテストフレームワークを使用できます。

###### Unit Tests
Let’s look at our example feature, days_to_card_expiry, and how and why we would test it: 
例のフィーチャーであるdays_to_card_expiryを見て、そのテスト方法と理由を考えてみましょう：

```  
def days_to_card_expiry(cc_expiry_date, event_time):     
    return (cc_expiry_date - event_time).dt.days
```

This is a straightforward but undocumented function. 
これは簡単ですが、文書化されていない関数です。

A junior developer discovered that the function would not work with a log transformation if the card expired on the same day as it was used. 
ジュニア開発者は、カードが使用された同じ日に期限切れになった場合、関数がログ変換で機能しないことを発見しました。

Log transformations are undefined if the value is zero or negative. 
値がゼロまたは負の場合、ログ変換は未定義です。

So the developer changed the code to return 1 rather than a negative number: 
そこで、開発者は負の数ではなく1を返すようにコードを変更しました：

```  
def days_to_card_expiry(cc_expiry_date, event_time):     
    days_remaining = (cc_expiry_date - event_time).dt.days     
    return max(days_remaining, 1)
```

A senior developer, stressed from their current project, performs a cursory review, approves the code, and lets it go into production. 
現在のプロジェクトにストレスを感じているシニア開発者は、ざっとレビューを行い、コードを承認し、プロダクションに投入します。

Suddenly, the credit card fraud detection model performance degrades. 
突然、クレジットカード詐欺検出モデルのパフォーマンスが低下します。

The senior developer reverts the change to the transformation function and removes the log transformation, resolving the bug for now. 
シニア開発者は変換関数の変更を元に戻し、ログ変換を削除して、今のところバグを解決します。

How could we have identified this problem before it rolled out? 
この問題を展開前にどのように特定できたでしょうか？

Studies have shown that code reviews and documentation are not very effective in finding many bugs. 
研究によると、コードレビューや文書化は、多くのバグを見つけるのにあまり効果的ではありません。

Performing unit tests is a more structured way of finding bugs earlier—before code review. 
ユニットテストを実施することは、コードレビューの前にバグを早期に見つけるためのより構造化された方法です。

Here are a few unit tests for days_to_card_expiry. 
days_to_card_expiryのいくつかのユニットテストを以下に示します。

The test_days_to_today_expiry test would have failed as a result of the junior developer’s changes, and the change would never have made it to production: 
test_days_to_today_expiryテストは、ジュニア開発者の変更の結果として失敗しており、その変更は決してプロダクションに到達しなかったでしょう：

```  
import pytest   
def test_days_to_future_expiry():     
    future_date = datetime.date.today() + datetime.timedelta(days=30)     
    assert days_to_card_expiry(future_date, datetime.date.today()) == 30   
def test_days_to_today_expiry():     
    today_date = datetime.date.today()     
    assert days_to_card_expiry(today_date, today_date) == 0   
def test_expired_card():     
    past_date = datetime.date.today() - datetime.timedelta(days=10)     
    with pytest.raises(ValueError, match="Credit card is expired."):       
        days_to_card_expiry(past_date, datetime.date.today())
```

These unit tests were suggested to me by an LLM—I copied in the function and asked it to write some pytest unit tests for me. 
これらのユニットテストは、LLMによって提案されました。私は関数をコピーし、いくつかのpytestユニットテストを書くように頼みました。

The unit tests cover the following potential error cases: 
ユニットテストは、以下の潜在的なエラーケースをカバーしています：

``` 
test_days_to_future_expiry
``` 
これは、カードが未来の数日後に期限切れになる「通常の」ケースです（LLMは30日を合理的な未来の日付として選びました）。これは10日、40日、80日でも構いません。おそらく10,000日ではありません。実際、ここには未来の日数が多すぎる場合のテストはありません。これは演習として追加できます。

``` 
test_days_to_today_expiry
``` 
コンピュータ科学者はゼロから数え始めますが、一般の人々は1から数え始めるため、オフバイワンエラーが発生することがよくあります。これは良いエッジケーステストです。

``` 
test_expired_card
``` 
days_to_card_expiryの新しい実装は、cc_expiry_dateが取引日より前である場合にValueErrorがスローされることを確認します。

The LLM worked reasonably well at generating the unit tests for our function, as its function name, parameter names, and variable names are human readable. 
LLMは、関数名、パラメータ名、および変数名が人間にとって読みやすいため、私たちの関数のユニットテストを生成するのにかなりうまく機能しました。

The LLM understood the semantics of the function—what the function is supposed to do. 
LLMは関数の意味を理解しており、関数が何をするべきかを把握しています。

Naturally, I did a code review of LLM-generated unit tests, and I was happy with them. 
当然のことながら、私はLLMが生成したユニットテストのコードレビューを行い、満足しました。

If you want more complicated feature functions, you will probably have to write them yourself—or at least handle some edge cases yourself. 
より複雑なフィーチャー関数が必要な場合は、おそらく自分で書く必要があります。あるいは、少なくともいくつかのエッジケースを自分で処理する必要があります。

Don’t just blindly trust LLMs to generate correct unit tests. 
LLMが正しいユニットテストを生成することを盲目的に信頼しないでください。

Trust is good, but validation is better. 
信頼は良いですが、検証はさらに良いです。



A failure to introduce automated testing is what brought global IT infrastructure to its knees in mid-2024, when a bug was introduced into the Windows kernel by the security company CrowdStrike, causing Windows to crash. 
自動テストを導入しなかったことが、2024年中頃に世界のITインフラを麻痺させた原因です。これは、セキュリティ会社CrowdStrikeによってWindowsカーネルにバグが導入され、Windowsがクラッシュしたことによるものです。

The bug was that a developer did not check whether an element in a struct was null before using it. 
そのバグは、開発者が構造体内の要素がnullであるかどうかを使用する前に確認しなかったことに起因しています。

They admitted that they hadn’t tested the code change that was rolled out to servers worldwide, causing widespread delays at airports and railways and problems at many retailers and other internet companies. 
彼らは、世界中のサーバに展開されたコード変更をテストしていなかったことを認めており、その結果、空港や鉄道での広範な遅延や、多くの小売業者や他のインターネット企業での問題を引き起こしました。

I wouldn’t have wanted to be that junior developer, but they weren’t the main culprit. 
私はそのジュニア開発者になりたくはありませんでしたが、彼らが主な原因ではありませんでした。

Engineering leaders didn’t introduce automated testing, a fundamental software engineering practice that would have detected the bug before it was rolled out into production. 
エンジニアリングリーダーは、自動テストを導入しませんでした。これは、バグが本番環境に展開される前に検出できた基本的なソフトウェアエンジニアリングの実践です。

###### Implementing pytest unit tests
###### pytestユニットテストの実装

Unit tests are defined on Python functions. 
ユニットテストはPython関数に対して定義されます。

If you want to unit-test individual features, you should factor your code so that each feature is computed by a single function. 
個々の機能をユニットテストしたい場合は、各機能が単一の関数によって計算されるようにコードを整理する必要があります。

As we use Python functions to implement the feature logic, we can use a unit test to validate that the code that computes a feature correctly follows a specification defined by the unit test itself. 
私たちはPython関数を使用して機能ロジックを実装するため、ユニットテストを使用して、機能を計算するコードがユニットテスト自体によって定義された仕様に正しく従っていることを検証できます。

That is, the unit test is a specification of the invariants, _preconditions, and postconditions for the feature logic:_ 
つまり、ユニットテストは機能ロジックの不変条件、_前提条件、及び後続条件の仕様です：

_Invariant_ A condition that remains true throughout the lifetime of the function—it is true before and after the function call and also within the scope of the function. 
_不変条件_ 関数のライフタイム全体にわたって真である条件です。関数呼び出しの前後および関数のスコープ内でも真です。

Invariants are more applicable to stateful objects, where certain properties need to hold true across multiple function calls. 
不変条件は、特定のプロパティが複数の関数呼び出しにわたって真である必要がある状態を持つオブジェクトにより適用されます。

_Precondition_ Must be true before a function can be executed correctly. 
_前提条件_ 関数が正しく実行される前に真でなければなりません。

It defines a valid input and/or state for the function to be executed without error. 
それは、関数がエラーなしに実行されるための有効な入力および/または状態を定義します。

_Postcondition_ A condition or set of conditions that must hold true after a function or method completes its execution. 
_後続条件_ 関数またはメソッドが実行を完了した後に真でなければならない条件または条件のセットです。

Often, they are related to stateful functions—functions that modify external state—but you can also validate the output of stateless functions. 
しばしば、これらは外部状態を変更する状態を持つ関数に関連していますが、無状態関数の出力を検証することもできます。

In our days_to_card_expiry function, we can see examples of our conditions: 
私たちのdays_to_card_expiry関数では、条件の例を見ることができます：

_Precondition_ The cc_expiry_date cannot be earlier than the transaction_date. 
_前提条件_ cc_expiry_dateはtransaction_dateよりも早くてはなりません。

_Postcondition_ Our function is stateless (it depends only on its input arguments), but we can still validate a postcondition—if it doesn’t throw an exception, it should return either zero or a positive integer value. 
_後続条件_ 私たちの関数は無状態です（入力引数のみに依存します）が、後続条件を検証することはできます。例外をスローしない場合、ゼロまたは正の整数値を返すべきです。

_Invariant_ There are no invariants tested in our preceding unit tests, mostly because it is a stateless function call we are testing. 
_不変条件_ 前のユニットテストでは不変条件はテストされていません。主に、私たちがテストしているのは無状態の関数呼び出しだからです。

You need to understand three additional concepts to write unit tests in pytest: _test_ _functions, assertions, and test setup. 
pytestでユニットテストを書くためには、3つの追加の概念を理解する必要があります：_テスト_ _関数、アサーション、およびテストセットアップ。

Unit tests may be written either as functions (as in the preceding example) or as methods in classes. 
ユニットテストは、関数（前の例のように）またはクラス内のメソッドとして書くことができます。

Also, pytest has a naming convention to automatically discover test modules/classes/functions. 
また、pytestにはテストモジュール/クラス/関数を自動的に発見するための命名規則があります。

A test class must be named Test*, and test functions or methods must be named test_* (as in the preceding example). 
テストクラスはTest*という名前でなければならず、テスト関数またはメソッドはtest_*という名前でなければなりません（前の例のように）。

[In Figure 7-5, we can see that pytest is run during development as offline tests—not](https://oreil.ly/Qy5aN) when pipelines have been deployed to production (as online tests). 
[図7-5では、pytestが開発中にオフラインテストとして実行される様子が見えます。これは、パイプラインが本番環境に展開されたとき（オンラインテストとして）ではありません。]

_Figure 7-5. Diagram showing pytest running unit tests offline. They should run with zero friction during development._ 
_図7-5. pytestがオフラインでユニットテストを実行している様子を示す図。開発中は摩擦なく実行されるべきです。_

You typically run unit tests in your development environment before you create a pull request (PR). 
通常、プルリクエスト（PR）を作成する前に、開発環境でユニットテストを実行します。

When you submit your PR to a staging branch, a CI/CD environment should also run the unit tests and ask you to fix your code and resubmit your PR if any of the unit tests are failing. 
PRをステージングブランチに提出すると、CI/CD環境もユニットテストを実行し、ユニットテストが失敗した場合はコードを修正してPRを再提出するように求めるべきです。

With our directory structure from Chapter 6 (you depend on the default Python behavior of putting the current directory in sys.path), you can run your unit tests in your development environment from the root directory of the credit card project’s directory in the source code repository: 
第6章のディレクトリ構造を使用すると（現在のディレクトリをsys.pathに置くというPythonのデフォルトの動作に依存します）、ソースコードリポジトリ内のクレジットカードプロジェクトのルートディレクトリから開発環境でユニットテストを実行できます：

```   
python -m pytest
```

You only need to install the pytest library during development or when automated tests are run after you commit code to GitHub. 
pytestライブラリは、開発中またはコードをGitHubにコミットした後に自動テストが実行されるときにのみインストールする必要があります。

You don’t need pytest installed in your production pipelines. 
本番環境のパイプラインにはpytestをインストールする必要はありません。

###### Running pytest as part of a GitHub Action
###### GitHub Actionの一部としてpytestを実行する

You can define a GitHub Action that will run the pytest unit tests whenever code is pushed to the main branch or whenever a pull request is created for the main branch: 
コードがメインブランチにプッシュされるたび、またはメインブランチにプルリクエストが作成されるたびにpytestユニットテストを実行するGitHub Actionを定義できます：

```   
name: Credit Card Fraud Test   
on:    
  push:     
    branches:      
      - main    
  pull_request:     
    branches:      
      - main   
jobs:    
  test:     
    runs-on: ubuntu-latest     
    steps:     
      - name: Check out repository code      
        uses: actions/checkout@v3     
      - name: Set up Python      
        uses: actions/setup-python@v5      
        with:       
          python-version: '3.12'     
      - name: Install dependencies      
        run: |       
          cd ccfraud       
          python -m pip install --upgrade pip       
          pip install -r requirements.txt     
      - name: Run tests      
        run: |       
          pytest
```

You can click on failed actions in GitHub to see the logs for why a unit test failed. 
GitHubで失敗したアクションをクリックすると、ユニットテストが失敗した理由のログを見ることができます。

Finally, when the test passes and after a code review, you want to merge the new PR to the main branch. 
最後に、テストが合格し、コードレビューが完了したら、新しいPRをメインブランチにマージしたいと思います。

When you merge the PR, you should squash your commits (turn all your commits into one big commit) to get rid of your messy trail of commits. 
PRをマージするときは、コミットをスクワッシュする（すべてのコミットを1つの大きなコミットに変換する）べきです。これにより、混乱したコミットの履歴を取り除くことができます。

In the long run, it pays to keep your house tidy! 
長期的には、整理整頓を保つことが重要です！

###### A Testing Methodology
###### テスト方法論

After covering all that tactical work on defining unit tests, running tests, and automating tests, we need to consider how we write tests and what we should test. 
ユニットテストの定義、テストの実行、自動化に関するすべての戦術的作業をカバーした後、私たちはテストを書く方法と何をテストすべきかを考慮する必要があります。

For that, we need a methodology for structuring test cases. 
そのためには、テストケースを構造化するための方法論が必要です。

I recommend using [the](https://oreil.ly/Tjokv) _[arrange, act, assert pattern that arranges the inputs and targets, acts on the target](https://oreil.ly/Tjokv)_ behavior, and asserts expected outcomes. 
私は、入力とターゲットを整理し、ターゲットに対して行動し、期待される結果を主張する_ [arrange, act, assertパターン](https://oreil.ly/Tjokv)の使用をお勧めします。

This is the structure we use in the examples here. 
これは、ここでの例で使用する構造です。

However, how do you know what to test and how to test it? 
しかし、何をテストすべきか、どのようにテストすべきかをどうやって知るのでしょうか？

Testing is not always required for all features. 
テストはすべての機能に対して常に必要なわけではありません。

If the feature is a revenue driver at your company, then you probably should test it thoroughly, but if your feature is experimental, then maybe it requires minimal or no testing for now. 
その機能が会社の収益を生むものであれば、徹底的にテストするべきですが、機能が実験的であれば、今のところ最小限のテストまたはテストなしで済むかもしれません。

That said, our preferred testing methodology for features is a simple recipe: 
とはいえ、機能に対する私たちの推奨するテスト方法論はシンプルなレシピです：

1. Write unit tests for all feature and transformation functions (MITs, MDTs, and ODTs) and check your test code coverage (what percentage of the code paths are covered by unit tests). 
1. すべての機能および変換関数（MIT、MDT、ODT）に対してユニットテストを書き、テストコードカバレッジ（ユニットテストでカバーされているコードパスの割合）を確認します。

2. Test feature pipelines, training pipelines, and batch inference pipelines with end-to-end tests. 
2. エンドツーエンドテストを使用して、機能パイプライン、トレーニングパイプライン、およびバッチ推論パイプラインをテストします。

3. Write unit tests for utility functions and other important untested code paths. 
3. ユーティリティ関数や他の重要な未テストのコードパスに対してユニットテストを書きます。

This methodology will help get you started, but it is not a panacea. 
この方法論は、あなたを始める手助けをしますが、万能ではありません。

For example, imagine you write a feature to compute monthly aggregations but forget to include code handling the leap year. 
例えば、月次集計を計算する機能を書いたが、うるう年を処理するコードを含めるのを忘れたとします。

With this methodology, you would not see that the leap year code path was not covered in test code coverage. 
この方法論では、うるう年のコードパスがテストコードカバレッジにカバーされていないことに気づかないでしょう。

Only when you first discover the bug will you fix it, and then you should write a unit test to ensure that you don’t have a regression where the leap year bug appears again. 
最初にバグを発見したときに修正し、その後、うるう年のバグが再発しないことを確認するためにユニットテストを書くべきです。

What will help is testing with more edge cases in your input data and anticipating edge cases. 
役立つのは、入力データでより多くのエッジケースをテストし、エッジケースを予測することです。

You should use LLMs to help suggest edge cases for testing. 
テストのためのエッジケースを提案するためにLLMを使用すべきです。

Although there are different schools of thought regarding test-driven development, we do not think that test-first development is productive when you are experimenting. 
テスト駆動開発に関する異なる考え方があるものの、実験中にテストファースト開発が生産的であるとは考えていません。

A good way to start is to list out what you want to test. 
始める良い方法は、テストしたいことをリストアップすることです。

Then decide what you should test offline using pytest and what to test at runtime with data validation checks, A/B tests, and feature/model monitoring. 
次に、pytestを使用してオフラインでテストすべきことと、データ検証チェック、A/Bテスト、機能/モデルモニタリングで実行時にテストすべきことを決定します。

###### Summary and Exercises
###### まとめと演習

In this chapter, we looked at MDTs and ODTs from both a data science perspective and an engineering perspective. 
この章では、データサイエンスの視点とエンジニアリングの視点の両方からMDTとODTを見てきました。

We presented why and how you transform both categorical variables and numerical features into numerical representations. 
カテゴリ変数と数値特徴を数値表現に変換する理由と方法を示しました。

We looked at different frameworks for implementing MDTs without any skew between training and inference pipelines. 
トレーニングパイプラインと推論パイプラインの間に歪みがないMDTを実装するためのさまざまなフレームワークを見てきました。

We introduced pipelines and transformers in Scikit-Learn, which work well with smaller data volumes in NumPy arrays. 
NumPy配列の小さなデータボリュームでうまく機能するScikit-Learnのパイプラインとトランスフォーマーを紹介しました。

We looked at transformation functions in Hopsworks, how they scale to handle large data volumes with Pandas UDFs, and how they can be used to implement both MDTs and ODTs. 
Hopsworksの変換関数、Pandas UDFを使用して大規模データボリュームを処理する方法、そしてそれらがどのようにMDTとODTの両方を実装するために使用できるかを見てきました。

We then looked at how to organize transformations in FTI pipelines using an example PyTorch system. 
次に、例としてPyTorchシステムを使用してFTIパイプラインで変換を整理する方法を見てきました。

This included writing different MITs, MDTs, and ODTs for images and tensor data. 
これには、画像やテンソルデータのためのさまざまなMIT、MDT、ODTを書くことが含まれます。

Finally, we concluded with an introduction to pytest and how it can be used to unit-test transformation functions. 
最後に、pytestの紹介と、それが変換関数のユニットテストにどのように使用できるかを結論付けました。

Now that we have covered the MITs, MDTs, and ODTs for creating features, we can look at how we write pipelines to run them. 
機能を作成するためのMIT、MDT、ODTをカバーしたので、これらを実行するためのパイプラインを書く方法を見ていきましょう。

The following exercises will help you learn how to design your own MDTs and ODTs: 
以下の演習は、独自のMDTとODTを設計する方法を学ぶのに役立ちます：

- I have a feature I would like to implement that is specific to one model but is quite computationally complex. 
- 特定のモデルに特有で、計算的に複雑な機能を実装したいと思っています。

I want to minimize online latency for retrieving or computing it. 
それを取得または計算する際のオンラインレイテンシを最小限に抑えたいです。

Should I implement it as an MIT, MDT, or ODT? 
それをMIT、MDT、またはODTとして実装すべきですか？

- I am building a batch ML system that requires daily retraining and makes daily predictions. 
- 毎日再トレーニングを必要とし、毎日予測を行うバッチMLシステムを構築しています。

Can I implement it as a single monolithic pipeline with MITs or MDTs? 
それをMITまたはMDTを使用して単一のモノリシックパイプラインとして実装できますか？



