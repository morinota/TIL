## 0.1. link リンク

- https://dl.acm.org/doi/10.1145/2792838.2800184 https://dl.acm.org/doi/10.1145/2792838.2800184

## 0.2. title タイトル

Predicting Online Performance of News Recommender Systems Through Richer Evaluation Metrics
より豊かな評価指標によるニュース推薦システムのオンライン性能の予測

## 0.3. abstract アブストラクト

We investigate how metrics that can be measured offline can be used to predict the online performance of recommender systems, thus avoiding costly A-B testing.
オフラインで測定できる指標を利用して、推薦システムのオンライン性能を予測することで、コストのかかるA-Bテストを回避する方法を調査している.
In addition to accuracy metrics, we combine diversity, coverage, and serendipity metrics to create a new performance model.
精度の指標に加えて、多様性、カバー率、セレンディピティの指標を組み合わせて、新しいパフォーマンスモデルを作成します。
Using the model, we quantify the trade-off between different metrics and propose to use it to tune the parameters of recommender algorithms without the need for online testing.
このモデルを用いて、異なる指標間のトレードオフを定量化し、オンラインテストを必要としない**レコメンダーアルゴリズムのパラメータ調整に使用すること**を提案します。
Another application for the model is a self-adjusting algorithm blend that optimizes a recommender's parameters over time.
また、このモデルの応用として、レコメンダーのパラメータを時間経過とともに最適化する自己調整アルゴリズムブレンドがある.
We evaluate our findings on data and experiments from news websites.
ニュースサイトのデータと実験により評価する.

# 1. Introduction 序章

It was recognized early on in the history of recommender systems (recsys) that the most accurate recommendations were not always the best.
レコメンダーシステム（Recsys）の歴史の中で、**最も精度の高いレコメンデーションが必ずしもベストではない**ということが早くから認識されていました。
The first approaches for diversifying recommendations were made by Zhang et al.[29] and Ziegler et al.[31].
レコメンデーションの多様化については、Zhangら[29]とZieglerら[31]が最初のアプローチを行った。
Later, many different metrics - such as novelty, coverage, diversity, and serendipity [17] - have been introduced with the aim of enhancing the quality of recommendations.
その後、レコメンデーションの品質を高める目的で、新規性、網羅性、多様性、セレンディピティ[17]など、さまざまな指標が導入されている.
It has even been suggested that the focus on optimizing the accuracy of recsys has been detrimental to the field [13].
**レクシスの精度を最適化することに注力した結果、この分野に悪影響を及ぼしたという指摘もあるほど**だ[13].
Ordering algorithms with respect to their offline accuracy can result in the exact inverse of ordering them with respect to the online click-through rate (CTR), which is the metric most site owners care about [6, 27].
**オフラインでの精度を基準にアルゴリズムを並べると、サイト運営者が最も気にする指標であるオンラインでのクリックスルー率（CTR）を基準に並べるのと全く逆の結果になることがある**[6, 27].

The main reason for this is that recommending popular items is usually accurate – they are popular because people do indeed rate them highly – but such recommendations have little to no effect as people have already seen the items elsewhere.
その主な理由は、人気のあるものを勧めるのは正確で、実際に高い評価を得ているから人気なのですが、そのようなものを勧めても、人々はすでに他の場所で見ているので、ほとんど効果がないのである.
A contributing factor in the domain of news recommendations is that users are often interested in something entirely new.
ニュースレコメンデーションの領域では、ユーザが全く新しいものに興味を持つことが多いことが要因として挙げられる.
Finally, users often view recommendations concerning a variety of different topics more favorably than the ones concerning several interesting but similar items.
最後に、ユーザは、いくつかの興味深い、しかし類似したアイテムに関する推薦よりも、様々な異なるトピックに関する推薦をより好意的に見ることが多い.

All of the above factors indicate that optimizing the accuracy of recommendations using offline data, gathered from past behavior without a running recommender algorithm, is neither an effective nor efficient way to select the best algorithm [13, 19].
以上のことから、**推薦アルゴリズムが稼働していない過去の行動から収集したオフラインデータを用いて推薦の精度を最適化することは、最適なアルゴリズムを選択する方法として有効でも効率的でもないことがわかる**[13, 19].
The fairest way to compare algorithms is to launch them online and compare the actual reactions of users to the recommendations.
アルゴリズムを比較する最も公平な方法は、オンラインでアルゴリズムを公開し、推薦に対するユーザの実際の反応を比較することである.
However, this requires the existence of an online environment and a set of dedicated users, and it takes a long time.
しかし、そのためには、オンライン環境の存在と熱心なユーザの存在が必要であり、長い時間がかかる.
Another problem is the need of constant re-evaluation of algorithms, especially if they are sensitive to changes in the item or user set over time [2, 10].
また、特にアイテムやユーザセットの経年変化に敏感な場合、アルゴリズムを常に再評価する必要があるという問題もある[2, 10].
Simulation of an online environment is a potential alternative [11, 27].
**オンライン環境のシミュレーション(オフライン環境での...!)**は、その代替となりうるものである[11, 27].
We discuss these solutions later in the paper.
これらの解決策については、後述する.

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/1-Figure1-1.png)

In this work, we leverage recommendations from real news websites to model their CTR (Fig.1).
本研究では、実際のニュースサイトのレコメンデーションを活用し、その**CTRをモデル化**した(図1).
Our main contributions are threefold.
私たちの主な貢献は3つある.
First, in Sec.2, we review the different metrics, find those that are most likely to affect online performance, and indicate the presence of a trade-off between them.
まず、Sec.2では、様々なメトリクスをレビューし、**オンラインパフォーマンスに最も影響を与えそうなメトリクスを見つけ出し**、それらの間のトレードオフの存在を示す.
Next, in Sec.3, we combine a selected subset of metrics into a prediction model of online performance.
次に、Sec.3では、選択したメトリクスのサブセットを組み合わせて、**オンラインパフォーマンスの予測モデルを作成**します。
Finally, in Sec.4, using this model and the metric trade-offs, we show how to select the best version of an algorithm and its parameters using limited online evaluation, and how to create a blend of several recommender algorithms that adjusts over time for optimal performance.
最後に、第4章では、このモデルとメトリックのトレードオフを利用して、限られたオンライン評価でアルゴリズムの最適版とそのパラメータを選択する方法と、最適なパフォーマンスを得るために時間と共に調整する複数の推薦アルゴリズムのブレンドを作成する方法を示す.
Results reported in Sec 5 show that given limited access to online environment, it is possible to model performance over time far better than by averaging performance over time.
第5章で報告された結果は、オンライン環境へのアクセスが限られている場合、経時的なパフォーマンスを平均化するよりもはるかに優れたモデル化が可能であることを示している.

# 2. Evaluation Metrics 評価指標

Over the years, various metrics have been suggested for evaluating recsys.
長年にわたり、recsysを評価するためのさまざまな指標が提案されています。
In the approach presented here, we considered 17 metrics classified into five different groups [17].
ここで紹介するアプローチでは、5つの異なるグループに分類される17のメトリクスを考慮しました[17]。

## 2.1. Metric Groups メトリックグループ

Accuracy/Error metrics compute the quality of predictions (i.e., rating movies or a correct/incorrect guess of the next news item visited).
Accuracy/Errorメトリクスは、予測（映画の評価や、次に訪れるニュースの正誤判定など）の品質を計算します。
Error metrics usually penalize errors, whereas accuracy metrics reward correct answers.
エラーメトリクスは通常、エラーにペナルティを与えるが、精度メトリクスは正しい答えに報酬を与える。
We ignored metrics, such as RMSE or MAE, that penalize each item separately; we concentrated instead on metrics for the task of top-N recommendation.
RMSEやMAEのような、各項目に個別にペナルティを与える指標は無視し、トップN推薦のタスクのための指標に集中したのです。
We investigated the following metrics: Precision, NDPM, Kendall’s τ , Spearman’s ρ [8], Success [6], Markedness, Informedness, and Matthew’s Correlation [15].
以下の指標を調査した： Precision、NDPM、Kendallのτ、Spearmanのρ [8]、Success [6]、Markedness、Informedness、Matthewの相関 [15]です。
All these metrics compute the accuracy of prediction and, for the case of top-1 recommendation, turn into binary indicators of the success of recommendation.
これらの指標はすべて予測精度を計算するもので、トップ1推薦の場合は推薦の成功を示す二値指標となる。

Diversity is usually defined as a measure of dissimilarity between items in the recommendation list with respect to a similarity metric.
多様性とは、通常、推薦リストのアイテム間の類似性メトリックに関する非類似性の尺度として定義される。
This “intra-list” diversity has been presented and used in several forms [29, 31, 28].
この「リスト内」の多様性は、いくつかの形で発表され、利用されてきた[29, 31, 28]。
Lathia et al.[10] proposed a definition of the temporal diversity of a recsys which was dependent on the number of new items a user was shown during different visits.
Lathiaら[10]は、ユーザが異なる訪問時に表示された新しいアイテムの数に依存する、レクシスの時間的多様性の定義を提案した。
For news recommendations where users are often anonymous, we modified the definition to compute the amount of new items the system recommends to all users at a later time.
ユーザが匿名であることが多いニュースレコメンデーションについては、システムが後日全ユーザーに推奨する新しいアイテムの量を計算するように定義を変更しました。
Zhou et al.[30] proposed a metric called “personalization” that is effectively the normalized pairwise Jaccard similarity between items recommended to each pair of users; it can be viewed as the “extra-list” diversity.
Zhouら[30]は，パーソナライゼーションと呼ばれる指標を提案したが，これは，各ユーザーのペアに推奨されたアイテム間の正規化ペアワイズJaccard類似度であり，「エクストラリスト」の多様性と見なすことができる．

Novelty is the quality of an item of being new to a user (i.e., the recommendation of an item from the category that the user already likes is not novel).
新規性とは、あるアイテムがユーザーにとって新しいものであること（つまり、ユーザーがすでに好きなカテゴリのアイテムを推薦することは新規性がないこと）。
A variation of such a metric, called “surprisal”, is a weighted sum of negative log frequencies of the items in the recommendation list [30].
このようなメトリックのバリエーションとして、"surprisal "と呼ばれる、推薦リストの項目の負の対数頻度の加重和がある [30]．

Coverage is defined as the percentage of items that are ever recommended, and prediction coverage is the number of users for whom a recommendation can be made.
カバレッジとは、これまでに推薦されたことのあるアイテムの割合のことで、予測カバレッジとは、推奨が可能なユーザー数のことです。
We also considered the Gini Index and Shannon’s Entropy [17].
また、ジニ指数やシャノンのエントロピー[17]も考慮しました。

Serendipity is the quality of being both unexpected and useful.
セレンディピティとは、予想外であると同時に役に立つという性質である。
One component penalizes the expectedness of the most popular items, whereas the other component measures usefulness – typically just accuracy [7, 14].
一方の成分は、最も人気のあるアイテムの期待値をペナルティとして与え、他方の成分は有用性-典型的には単なる精度-を測定する[7, 14]。

## 2.2. Metric correlations メトリックの相関関係

We investigated the correlation between the metrics in each group by applying three different algorithms to the Swissinfo dataset, described later.
後述するSwissinfoデータセットに3種類のアルゴリズムを適用し、各グループのメトリクス間の相関を調査した。
Each data point was generated by averaging metric values for all the recommendations at equal time intervals.
各データポイントは、等間隔に配置されたすべての推薦者のメトリック値を平均化することで生成されました。
For metrics that are computed cumulatively over recommendations (i.e., temporal diversity) we computed the metric value at each point in time and used the cumulative difference as the metric value.
レコメンデーションで累積的に計算されるメトリクス（＝時間的多様性）については、各時点でのメトリクス値を計算し、その累積差分をメトリクス値として使用した。

The metrics in the Accuracy group (NDPM, Kendall’s τ , Success, Spearman’s ρ, Markedness, Informedness and Matthews correlation) showed correlations higher than 0.9 between all the pairs of metrics for the recommendation lists given by the algorithms.
精度グループの指標（NDPM、Kendallのτ、Success、Spearmanのρ、Markedness、Informedness、Matthews相関）は、アルゴリズムが与えた推薦リストについて、すべての指標のペア間で0.9以上の相関が見られた。
The same results were obtained for the other metric groups – Diversity (Intralist diversity, Personalization, and Temporal diversity), Coverage (Gini Index, Shannon’s Entropy, and Coverage), and Serendipity (Serendipity by Ge [7], and Serendipity by Murakami [14]).
他の指標群である多様性（Intralist diversity、Personalization、Temporal diversity）、網羅性（Gini Index、Shannon's Entropy、Coverage）、セレンディピティ（Serendipity by Ge [7], Serendipity by Murakami [14] ）でも同じ結果が得られています。
We therefore examined correlation between pairs of “representative” metrics from each of these groups (Fig.2).
そこで、それぞれのグループの「代表的な」メトリクスのペア間の相関を調べました（図2）。
There was no strong agreement between metric groups (except for Coverage and Serendipity).
指標グループ間で強い一致は見られなかった（CoverageとSerendipityを除く）。
This indicates that different metric groups all express different features of the recommendations and therefore at least one representative of each group should be used as a feature of the performance model.
これは、異なるメトリックグループがすべてレコメンデーションの異なる特徴を表現していることを示しており、したがって、各グループの少なくとも1つの代表をパフォーマンスモデルの特徴として使用する必要があることを示しています。

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/2-Figure2-1.png)

Points often formed three distinct clusters.
ポイントは3つのクラスターを形成していることが多い。
The clusters corresponded to recommendations given by the different algorithms, indicating that the relationship between metrics might be different for recommendations given by different algorithms.
このクラスターは、異なるアルゴリズムによるレコメンデーションに対応しており、異なるアルゴリズムによるレコメンデーションでは、指標間の関係が異なる可能性があることを示しています。

The results in Fig.2 were obtained from the recommendation lists comprising three items.
図2の結果は、3つのアイテムからなるレコメンドリストの結果である。
We studied the effect of the length of recommendation lists on metric correlations (Fig.3).
推薦リストの長さが指標相関に与える影響を調査した（図3）。
For all metric pairs, we first observed a drop, and then almost no change in the absolute value of correlations.
すべての指標ペアについて、推薦リストの長さが大きくなるにつれて、まず相関の絶対値が低下し、その後ほとんど変化がないことが確認された。
This indicates that different sets of metrics might be important for domains with different numbers of items to be recommended.
これは、推薦アイテムの数が異なるドメインでは、異なるメトリクスセットが重要である可能性を示しています。

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/2-Figure3-1.png)

## 2.3. Metric trade-off メトリックトレードオフ

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/3-Figure4-1.png)

Algorithms often have hyperparameters that affect their performance, and by varying the values of such hyperparameters different sets of recommendations can be obtained.
アルゴリズムは、その性能に影響を与えるハイパーパラメーターを持つことが多く、そのようなハイパーパラメーターの値を変えることで、異なるレコメンデーションセットを得ることができます。
The average metric values for all the sets of recommendations given can be computed in order to observe how they change when varying a hyperparameter.
ハイパーパラメータを変化させたときにどのように変化するかを観察するために、与えられた推薦結果のすべてのセットの平均メトリック値を計算することができる。
The example shown in Fig.4 was obtained using the Yahoo dataset and several variations of the Context Tree (CT) algorithm, described later in the paper.
図4の例は、Yahooデータセットと後述するCT（Context Tree）アルゴリズムのいくつかのバリエーションを用いて得られたものです。
Each of the algorithms produced a curve that clearly indicated the trade-off between metrics – in this case, Accuracy and Coverage.
各アルゴリズムは、測定基準(この場合はAccuracyとCoverage)の間のトレードオフを明確に示す曲線を作成しました。
We also observed these tradeoffs using other datasets and algorithms.
また、他のデータセットやアルゴリズムを用いて、これらのトレードオフを観察しました。
Getting the best performance requires selecting which metrics to optimize.
最高のパフォーマンスを得るためには、どの指標を最適化するかを選択する必要があります。
The next section describes how we build a regression model of performance to achieve this.
次節では、これを実現するためのパフォーマンスの回帰モデルの構築について説明する。

# 3. Predicting Online From Offline オフラインからオンラインを予測する

In this section, we first briefly describe the definitions of offline and online accuracy, and click-through rate.
本節ではまず、オフライン精度とオンライン精度の定義、クリックスルー率の定義について簡単に説明する。
We then describe our method of feature selection for the regression model of online metrics, and finally the model itself.
次に、オンラインメトリクスの回帰モデルに対する特徴選択方法について説明し、最後にモデルそのものについて説明する。

Offline accuracy is the percentage of clicks predicted by the recsys when it is applied to a log of user browsing which occurred without the recommender system present.
オフライン精度とは、レコメンダーシステムが存在しない状態で発生したユーザーの閲覧ログに対して、レコメンダーシステムを適用した場合に予測されるクリック数の割合のことです。

Online accuracy is the percentage of clicks predicted by the recsys when it is online.
オンライン精度とは、オンライン時にrecsysが予測したクリック数の割合のことです。
If a recsys predicted that the user would browse to a particular page and she did so, but without clicking on its recommendations, this still counts towards online accuracy.
ユーザーが特定のページを閲覧すると予測し、そのページを閲覧したが、推奨されたページをクリックしなかった場合でも、オンライン精度にカウントされる。

Click-through rate (CTR) is the percentage of clicks made on recommendations.
クリックスルー率（CTR）は、レコメンデーションでクリックされた割合のことです。

For any random user, the model assumes that all the items she visits without a recsys are included in the set of items she would visit with one.
任意のランダムなユーザについて、このモデルは、彼女が推薦システムを使わずに訪問したすべてのアイテムが、推薦システムがあれば訪問するアイテムの集合に含まれると仮定している.
This means that if the user visits an item when using the recsys, that she would visit anyway when the recsys was absent, then that click should not be taken into account when measuring the impact of the recsys.
つまり、推薦システムを使用しているときに、推薦システムがないときにも訪問するようなアイテムをユーザが訪問した場合、**そのクリックは推薦システムの効果を測定する際に考慮されるべきではない**ということです.(ん? でもオンライン精度は考慮してしまっている、という事だよね...?! )
A broader discussion of this topic is presented by Garcin et al.[6].
このトピックに関するより広範な議論は、Garcinら[6]によって紹介されています。

CTR and online accuracy are both important metrics for recsys.
CTRとオンライン精度は、どちらもrecsysにとって重要な指標である.
Therefore, we build a regression model for each of them.
そこで、それぞれについて回帰モデルを構築する。
The regression model will use not only offline accuracy, as it is something different from the two above.
回帰モデルは、上記の2つとは異なるものであるため、オフライン精度以外のオフラインmetricsも使用します。

## 3.1. Feature selection 特徴の選択

To verify the finding that multiple groups of metrics, such as Diversity and Coverage, are important for predicting online performance metrics, we carried out feature selection using the Least Angle Regression (LAR, [4]).
オンラインパフォーマンス指標の予測には、DiversityやCoverageといった複数の指標群が重要であるという知見を検証するため、Least Angle Regression（LAR、[4]）を用いた特徴選択を実施しました。
The LAR assumes a linear model of the relationship between independent variable y and n dependent variables $x = (x_1,\cdots ,x_n)^T$, with an $L_{1}$ regularizer:
LARは、独立変数yとn個の従属変数$x = (x_1,\cdots ,x_n)^T$の関係の線形モデルを仮定し、$L_{1}$正則化する：

$$
y = \beta^T x + \lambda \sum_{j=1}^{n} |x_{j}|
$$

The L1 regularizer promotes sparsity in β.
L1正則化により、βのスパース性が促進される.(不要なパラメータが落とされる様な仕組み...!)
By decreasing λ, it is possible to assign each predictor a value of λ at which it first enters the model with a non-zero weight.
ハイパーパラメータλを減少させることで、各predictor(回帰分析の文脈なので、予測対象はパラメータ $\beta$ の事?) に、それが最初にゼロ以外の重みでモデルに入るλの値を割り当てることが可能である.(?)
The order of the predictors given by these λ values serves as a proxy for their importance.
これらのλ値によって与えられる predictors(推論すべきパラメータって意味?)の順序は、それらの重要性の代理として機能する。
The LAR allows efficient computation of this value for each regressor [4].
LARは、各レグレッサーについてこの値を効率的に計算することができます[4]。

The average order position among folds was calculated using average metric values in time intervals of length ∆t as predictors and average CTR as responses.
長さΔtの時間間隔におけるmetricsの平均値を predictors(=説明変数?) とし、平均的なCTRをresponses(=目的変数)として、folds間(?)の平均的な順序位置を算出した.
Details of this approach are given in Alg.1.Several ∆t interval sizes were tested, but all values of ten minutes or longer were found to work reasonably well.
この方法の詳細はAlg.1に記載されている。∆t間隔の大きさはいくつかテストされたが、10分以上のすべての値が合理的に機能することがわかった.
Ten minute intervals were chosen as shorter intervals gave results with very high variance and longer intervals meant fewer data points and, therefore, less significant results.
$\Delta t$ を**10分間隔**にしたのは、これより短い間隔では分散が大きく、長い間隔ではデータポイントが少なくなり、有意な結果が得られないからである.
We used F = 100 folds.
F＝100倍を使用しました.(fold=パラメータ推論のサンプリング回数?)

## 3.2. Regression model 回帰モデル

After identifying the best predictors, we used the multiple linear regression y = β |x.
最適な予測因子を特定した後、重回帰 $y =  \beta |x$ を用いた.
This simple model allowed us to interpret coefficients of β as trade-offs between different metrics for a particular model, or as derivatives of the performance with respect to metrics.
このシンプルなモデルにより、βの係数を、特定のモデルに対する異なるメトリクス間のトレードオフ(=同じCTRを得る場合に、あるmetricsを増やしたらあるmetricsを減らす必要がある、みたいな...??)として、あるいは**メトリクスに関する性能の微分**(=あるmetricが1単位増えたら、オンライン性能は...)として解釈することができました.
We expand on this idea in Sec.4.More complex models, such as Gaussian process regression or penalized linear regression, do not allow such a simple interpretation.
ガウス過程回帰や罰則付き線形回帰など、より複雑なモデルでは、このような単純な解釈はできない.
Nevertheless, the results obtained using simple linear regression were compared to those of more complex methods.
それでも、**単純な線形回帰で得られた結果を、より複雑な手法で得られた結果と比較**しました.
To build such a model, a limited amount of training data is required.
このようなモデルを構築するためには、限られた量の学習データが必要.
Features should be collected simultaneously using the metrics from a recsys run on a log of offline data (user browsing without the recsys), and the online performance metric should be collected from the live website that is using a recsys.
機能は、オフラインデータ(recsysを使用しないユーザーのブラウジング)のログで学習された推薦システムからのmetricsを使用して同時に収集し(説明変数側)、オンラインのパフォーマンスメトリクス(目的変数側)は、recsysを使用しているライブウェブサイトから収集する必要がある.

# 4. Algorithm Optimization アルゴリズムの最適化

In this section we discuss two possible ways of using the model of online performance metric.
このセクションでは、前セクションで作成した、オンラインパフォーマンスメトリクスの推論モデルの使用方法として考えられる**2つの方法**について説明します。
The first allows an effective comparison between several variations of the algorithm, without the need for lengthy access to online data, and the selection of the optimal hyperparameters.
1つ目は、オンラインデータに長時間アクセスすることなく、**アルゴリズムのいくつかのバリエーションを効果的に比較**し、最適なハイパーパラメータを選択することができます。
The second describes an algorithm able to rebuild the model over time, continually aiming for optimal online performance.
2つ目は、時間の経過とともにモデル(=推薦モデル?それともオンライン性能予測モデル?)を再構築し、常に最適なオンラインパフォーマンスを目指すアルゴリズムについて説明します。(?)

## 4.1. Optimal algorithm selection 最適なアルゴリズム選択

A typical task for recsys designers is the comparison of several variations of an algorithm, and the selection of the hyperparameter value and algorithm that perform best.
recsys設計者の典型的なタスクは、**あるアルゴリズムのいくつかのバリエーションを比較し、最も良いパフォーマンスを発揮するハイパーパラメータ値とアルゴリズムを選択**することです.
An obvious solution would be to evaluate each of the algorithms online using several values of hyperparameter.
明らかな解決策は、ハイパーパラメータのいくつかの値を用いて、各アルゴリズムをオンラインで評価することである。

In our model, online performance can be approximated by a weighted combination of two offline metrics (i.e.Accuracy and Coverage).
**本モデルでは、オンライン性能は、2つのオフライン指標（AccuracyとCoverage）の重み付けされた組み合わせで近似**することができる.(結局この２つなのか...!)
To simplify the argument below, we assume that weights are positive but approach trivially extends to the case when they are negative.
以下の議論を簡単にするため、重みは正であると仮定する(=以下の解説を読む上で重要な仮定!!)が、アプローチは重みが負である場合にも些か拡張される.
Such a model is learned by evaluating one of the algorithm variations online and is assumed to be similar for other variations.
このようなモデルは、アルゴリズムの**バリエーションの一つをオンラインで評価することで学習され**、他のバリエーションでも同様であると仮定される。

As described in Sec.2.3, varying an algorithm’s hyperparameter produces the metrics trade-off curve.
2.3節で説明したように、アルゴリズムのハイパーパラメータを変化させると、メトリクスのトレードオフ曲線が生成される.
When the curve for one algorithm is located above the curve for a second, the first algorithm is strictly better in terms of performance.
**あるアルゴリズムの曲線が、あるアルゴリズムの曲線よりも上に位置する場合、最初のアルゴリズムの方が性能的に厳密には優れていることになります**(<-CTR推論モデルのパラメータが全てpositiveと仮定しているから!)。
Note that curves are produced using offline data.
なお、曲線はオフラインのデータを使用して作成している.

Given the trade-off curves, there is no need for an online evaluation of all the combinations of algorithms and hyperparameters, but only those that produce points on the upper envelope of the curves.
**トレードオフ曲線があれば、アルゴリズムとハイパーパラメータのすべての組み合わせをオンラインで評価する必要はなく**、曲線の上側のエンベロープにポイントを生成するものだけを評価すればよい.
Furthermore, by inspecting the model coefficients it is possible to select an algorithm without evaluating it: if a model gives a much larger weight to one of the metrics, this can be used as a proxy for performance and the best algorithm is the one reaching the highest values for that metric.
さらに、モデルの係数を調べることで、アルゴリズムを評価せずに選択することも可能である. **モデルがあるmetricsに大きなウェイトを与えている場合、これをオンラインパフォーマンスの代理として使用することができ**、そのメトリクスで最高値に達したアルゴリズムが最良のアルゴリズムとなる.

Examples of real trade-off curves are shown in Fig.4.We used several variations of the CT recommender as a source of recommendations ordered by Accuracy [5].
私たちは、CTレコメンダーのいくつかのバリエーションを、Accuracy [5]で並べたレコメンデーションのソースとして使用した.
The standard CT algorithm makes predictions based on a count of the items viewed.
標準的なCTアルゴリズムでは、閲覧されたアイテムのカウントに基づいて予測を行う.
CT with additional experts exploit the item click count and the last time an item was clicked.
CT with additional expertsは、アイテムクリック数とアイテムが最後にクリックされた時刻を考慮して推薦する.
We used the items’ Shannon’s Entropy as a coverage score.
我々は**アイテムのシャノンエントロピーを coverage スコアとして使用**した.
Items were ordered by the weighted combinations of Accuracy and Coverage, and we varied the weight ratio, which was thus regarded as a hyperparameter for the algorithms.
アイテムはAccuracyとCoverageの組み合わせで重み付けされ、その重み比を変化させることで、アルゴリズムのハイパーパラメータと見なした.(これはCTアルゴリズムの特徴量の工夫か...!)
Curves were computed using the Yahoo dataset, described later.
曲線は、後述するYahooデータセットを用いて計算した.

Results such as these can be used for tuning a recommendation algorithm to a new site by picking the optimal value of a hyperparameter and the best algorithm.
このような結果は、ハイパーパラメータの最適値や最適なアルゴリズムを選ぶことで、新しいサイトへの推薦アルゴリズムのチューニングに利用することができます。
For example, for a site where the learned model gives a significant coefficient to coverage, the plain CT algorithm will be the best, whereas in cases where the accuracy coefficient dominates strongly, the ”fresh” expert will be useful.
例えば(Figure4の結果を見ると...!)、学習した**オンライン性能予測モデルがカバレッジに大きな係数を与える**サイトでは、プレーンCTアルゴリズムが最適となり、一方、精度係数が強く支配するケースでは、”fresh” expert ver.が有用となる.
Note also that the ”popular” expert is never going to be best.
また、”popular” expert ver.がベストであることは決してないことに注意してください.
The trade-off curves obtained from offline data can therefore be used to save on online experiments to determine the optimal algorithm and hyperparameter.
したがって、**オフラインデータから得られたトレードオフ曲線**は、最適なアルゴリズムとハイパーパラメータを決定するための**オンライン実験の省力化**に利用することができる。

## 4.2. Self-adjusting algorithm blend

We applied the online performance model to a setting where we wanted to optimize the blend of several algorithms over time, given full access to the online environment.
オンライン性能モデルを、オンライン環境に完全にアクセスできる状態で、**複数のアルゴリズムの(推薦結果の)ブレンドを時間経過とともに最適化したいという設定**に適用しました.
Let the algorithm give each item a rating based on the weighted combination of ratings assigned by several base recommenders: $F(i) = W^{T}(F_{1}(i), \cdots, F_m(i))$.
$F(i)=W^{T}(F_{1}(i), \cdots, F_m(i))$ のように、複数のベース推薦システムの評価を加味して各アイテムを評価するようにする. (推薦モデル1 ~ mの推薦結果を、Wで重み付けしてブレンドして、一つの推薦結果を作るケースを想定...!)
For each recommender Fa, we introduce a latent variable Za.
各推薦システム $F_a$ に対して、**潜在変数 $Z_a$ を導入**する.
Za(t) measures how close the items, recommended at time t by the main algorithm, are to the top items recommended by Fa(t).
$Z_a(t)$ は、メインアルゴリズム(現在稼働中の推薦システムのこと?)によって時刻$t$ に推薦されたアイテムが、$F_a(t)$ によって推薦されたトップアイテムに**どれだけ近いか**(=現在稼働中のrecommenderの推薦結果と、評価したいrecommenderの推薦結果の距離指標??)を測定する.
Alternatively, $Z_a(t)$ can measure how high this recommender rates them.
あるいは、$Z_a(t)$ は、このレコメンダーがどれだけ高く評価しているかを測ることができる.
We build a regression model of online performance at each time t, based on the regressors Z1(t), .
各時刻tにおけるオンライン性能の回帰モデルを、regressors(=説明変数) $Z_1(t), \cdots, F_{m}(t)$ に基づいて構築する.
In this model, the positive weight of a regressor Za suggests that giving recommendations with increased Za in the future would improve online performance.
このモデルでは、回帰変数 $Z_a$ の重みが正であれば、将来 $Z_b$ を増やした推薦を与えることでオンラインパフォーマンスが向上することが示唆される. (推論されたパラメータが高いrecommdner aを 強く採用すべきって意味?)
Coefficients of linear regression β | effectively form a gradient of online performance with respect to the latent variables.
線形回帰の係数 $\beta^T$ は、潜在変数に対するオンラインパフォーマンスの勾配を効果的に形成する.
We can therefore perform a gradient descent, updating the weights, with which we mix different base recommenders: WT +1 = WT + λ ∗ βT , with T and T + 1 corresponding to two consecutive time frames, and βT being the coefficients of LR model, fitted on the data from frame T.
そこで，勾配降下を行い，異なるベースレコメンダーを混合する重み $W$ を更新することができる: $W{T +1} = W_{T} + λ ∗ \beta_{T}$ 、TとT + 1は連続する2つの時間フレームに対応し、 $\beta_{T}$ はフレーム$T$のデータから学習させたLRモデルの係数である.
This could be an effective alternative to A–B testing, which is analogous to a grid search in the space of all possible weight coefficients.
これは、**すべての可能な重み係数の空間におけるグリッド検索に類似しているA-Bテスト**(そうなの...??)の効果的な代替となる可能性があある.
In a simple case where Za are ratings given by base recommenders to the items recommended by the main algorithm, and recommenders Fa optimize a particular set of metrics, this approach is equivalent to modeling CTR using the set of metrics as regressors over time.
$Z_a$ がメインアルゴリズムによって推薦されたアイテムに対して各ベース recommender が与える評価であり、recommender $F_a$ が特定の metrics セットを最適化するという単純なケースでは、このアプローチは、 metrics セットを時間的な regressors として使用してCTRをモデル化することと同等である.(=>あるmetricを元に最適化させた推薦結果がオンライン性能に強い影響を与えた! =>即ち、あるmetricの大小はオンライン性能に強い影響を与える、といえる...!)
This is especially important for sites with a dynamic user base, that, for example, prefers fresh news in the morning and a more diverse set in the evening.
特に、**朝は新鮮なニュースを、夕方はより多様なニュースを好むなど、ダイナミックなユーザ層を持つサイトでは重要**である.
(そうか! 時間frame $T$ の結果を使って、時刻 $T+1$ の重み付け$W$を更新する...!)

# 5. Results 結果

In this section, the datasets used in the present experiments are described and then the results of several of those experiments are shown.
このセクションでは、今回の実験で使用したデータセットについて説明し、次にそのうちのいくつかの実験結果を示す。
First, feature selection showed that multiple groups of metrics were important for the prediction of online performance.
まず、特徴量の選択により、オンラインパフォーマンスの予測には複数のメトリクス群が重要であることが示されました。
Second, we demonstrate the regression model’s performance using different feature sets on different datasets.
次に、異なるデータセットで異なる特徴セットを用いて、回帰モデルの性能を実証する。
We subsequently offer examples of the applications we described in the previous section.
続いて、前項で説明したアプリケーションの例を紹介します。
We finish by describing the results obtained using unbiased offline evaluation [11] and by discussing why this method is not generally applicable.
最後に、偏りのないオフライン評価[11]で得られた結果を説明し、この方法が一般的に適用できない理由を説明します。

## 5.1. Datasets データセット

We use two news datasets which have online and offline browsing logs and online evaluation on a news website.
オンラインとオフラインの閲覧ログとニュースサイトでのオンライン評価を持つ2つのニュースデータセットを使用します。

Swissinfo dataset is a combination of three weeks’ worth of offline and online browsing logs from the live news website swissinfo.ch.
Swissinfoデータセットは、**ライブニュースサイトswissinfo.chの3週間分のオフラインおよびオンライン閲覧ログ**を組み合わせたものです。
The offline data includes more than 227k clicks on 28,525 stories by around 188k users.
オフラインデータには、約188kのユーザーが28,525のストーリーを227k以上クリックしたものが含まれています。
The online data was gathered in the presence of three recommendation algorithms – random recommendations, most popular recommendations, and Context Tree (CT, [5]).168k clicks were distributed almost equally between the three algorithms.
オンラインデータは、ランダムレコメンデーション、最も人気のあるレコメンデーション、コンテキストツリー（CT、[5]）の**3つの推薦アルゴリズムが存在する状態で収集**された。168kクリックは、3つのアルゴリズムにほぼ均等に分配された。
Three recommendations were made to each user, and items to be recommended were selected from the pool of the last 200 unique articles visited.
各ユーザに3つのレコメンドを行い、レコメンドするアイテムは、過去に訪れた200のユニークな記事の中から選択されました.
All users were identified solely by their browsing session, and the only information gathered about the users was from their browsing behavior.
すべてのユーザは、閲覧セッションによってのみ識別され、ユーザーに関する情報は閲覧行動からしか収集されませんでした。

Yahoo! Front page dataset is specifically tailored for unbiased offline evaluation [11].
Yahoo! Front pageのデータセットは、偏りのないオフライン評価用に特別に調整されています[11]。
It comprises 15 days’ worth of clicks data from the main page of Yahoo!News.
Yahoo！ニュースのメインページの15日分のクリックデータで構成されています。
Each visit to the page was described by a binary vector of features.
各ページへの訪問は、特徴の2値ベクトルによって記述された。
The item pool for recommendations always contains 20 items.
レコメンデーションのアイテムプールは常に20アイテムが含まれています。
The log consists of nearly 28M visits to a total of 653 items.
このログは、合計653のアイテムに対する約28Mの訪問で構成されています。

To make the dataset more suitable for news recommendations, we identified visits belonging to the same browsing session by selecting only visits with at least 50 binary features present.
ニュース推薦に適したデータセットにするため、少なくとも50個の二値特徴が存在する訪問のみ(=50人のユーザからの訪問があるアイテム?)を選択することで、同じブラウジングセッションに属する訪問を識別しました。
For visits with the same binary features, we assumed that visits were same session if the time between visits did not exceed 10 minutes.
同じ二値特徴を持つ訪問については、訪問間の時間が10分を超えない場合、同一セッションであるとした。(セッション識別子の情報をmetricsの算出にどこかで使ってる？？)
Otherwise, we assumed that these were visits from different sessions.
それ以外は、別のセッションからの訪問とみなしました。
This procedure decreased the total number of clicks in the log to ≈ 5.7M.
この手順により、ログの総クリック数は≈5.7M∽に減少しました。(単にログ情報を減らすためだけにsession情報を使った?)

With sessions established, online browsing logs were generated using the algorithm from [11] (Section 5.5).
セッションを確立した上で、[11]のアルゴリズムを用いて**オンラインブラウジングログ**を生成した（5.5項）。
For each algorithm, the number of clicks in the simulated browsing logs was around ≈ 285k.
各アルゴリズムとも、シミュレーションした閲覧ログのクリック数は≈285k∽程度でした。
To generate offline browsing logs, we took a random 10% of user sessions; they contained 573k clicks by 401k users.
オフラインの閲覧ログを作成するために、ユーザーセッションのうち無作為に10%を抽出しました。このログには、401kユーザーによる573k回のクリックが含まれています。

LePoint dataset contains 3.5 days worth of data from the live news website lepoint.fr (4.6M clicks and 3.3M users).
LePointデータセットには、ライブニュースサイトlepoint.frの3.5日分のデータ（4.6Mクリック、3.3Mユーザー）が含まれています。
Sessions that did not result in clicks on recommendations were used as offline data.
レコメンドのクリックに至らなかったセッションはオフラインデータとして使用しました。

## 5.2. Feature selection 特徴量の選択

The procedure for feature selection described in Section 3 was applied to the Swissinfo dataset using the CT algorithm.
セクション3で説明した特徴選択の手順を、CTアルゴリズムを用いてSwissinfoデータセットに適用した。
Due to the nature of the LAR, if there are several correlated predictors, one of them will enter the model earlier, and the others will enter much later (as their contribution would be smaller after first correlated predictor was used).
LARの性質上、いくつかの相関予測変数がある場合、そのうちの1つが早くモデルに入り、他のものはかなり遅れて入る（最初の相関予測変数が使用された後、それらの寄与が小さくなるため）。
However, the order in which correlated predictors will enter the model, is unknown.
しかし、相関のある予測変数がどのような順序でモデルに入るかは不明である。
As we are not interested in the predictors themselves, but rather in showing the importance of metric groups (Accuracy, Coverage, Diversity, Serendipity, and Novelty), we calculated the average time for the first metric of each metric group to enter the model (Tab.1).
予測因子そのものに興味があるのではなく、**メトリックグループ（Accuracy、Coverage、Diversity、Serendipity、Novelty）の重要性を示したい**ので、**各メトリックグループの最初のmetricがモデルに入るまでの平均時間**を計算した（Tab.1）。

![](https://d3i71xaburhd42.cloudfront.net/96b00351da3e0c281ce8c26b45bbba328b3d5f21/5-Table1-1.png)

Metrics from the Serendipity, Accuracy and Diversity groups are usually the first three to enter the model.
**Serendipity、Accuracy、Diversityの3つのグループのメトリクスは、通常、モデルに入る最初の3つ**である。
This is a strong indicator that these three groups relate to different parts of performance metric and are all important for predicting it.
これは、**これら3つのグループが(オンライン)パフォーマンス指標の異なる部分に関係し、いずれもそれを予測するために重要であることを示す強い指標**である.

We also noticed that if we removed the Diversity or Serendipity predictors, then Coverage metrics showed a low average first entry time.
また、**DiversityやSerendipityのpredictorsを取り除いた場合**、**Cverageの指標は平均初回入力時間が短くなる**ことに気づきました。
This indicates that two out of three groups from Diversity, Serendipity and Coverage might be enough.
これは、Diversity、Serendipity、Coverageの3つのグループのうち、2つで十分かもしれないということを示しています。(->結果と示唆の関係がよくわかってない...)
For Accuracy metrics, it did not matter which predictor was used, and Markedness was easily replaceable by precision or any of the other Accuracy metrics.
**Accuracyの指標では、どのpredictorを使っても問題なく**、Markednessはprecisionや他のAccuracyの指標に簡単に置き換えることができました。
A very strong correlation was seen to exist between different Accuracy group metrics.
異なるAccuracyグループ内のmetric間には、非常に強い相関があることが確認された.

The results obtained with the other two algorithms were similar to those above.
他の2つのアルゴリズムで得られた結果は、上記と同様であった。
In all of the results below, when we say that we have used a predictor from a certain metric group, we mean that we used the predictor that was first to enter in the LAR model from this metric group.
以下のすべての結果において、あるメトリックグループからの予測因子を使用したと言う場合、このメトリックグループからLARモデルで最初に入力された予測因子を使用したことを意味します。(あるmetrics group当たり、最速な一つのmetricのみがモデルに入る...!)

## 5.3. Regression model performance 回帰モデルの性能

We used the approach described in Section 2 to generate data points for the regression model.
回帰モデル用のデータポイントの生成には、セクション2で説明した手法を用いました。
We divided the time interval into parts of 30%, 50% and 20%.
時間間隔を30％、50％、20％のパートに分けました。
The first 30% were used for training the algorithm itself and were not used in the regression model.
最初の30%はアルゴリズム自体のトレーニングに使用され、回帰モデルには使用されませんでした。
The recommendations made by the algorithm on the next 50% were used to train the model, and the last 20% were used to test the model’s performance.
次の50%についてアルゴリズムが行った推薦は、モデル(=オンライン性能予測モデル)のトレーニングに使用され、最後の20%はモデルの性能テストに使用されました.

### 5.3.1. CTR prediction.

![](https://camo.qiitausercontent.com/fbaf88b0075e1ce297b5e445d172a65ca59b7e4f/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32646561373135392d366335622d363730372d646338642d3063646335636632396235352e706e67)

For CTR prediction (Tab.2), the lowest average error was indeed obtained using one predictor from each of the four metric groups (we omitted novelty here and later on due to its poor results in feature selection).
CTR予測（Tab.2）では、4つの指標群からそれぞれ1つずつpredictorを用いることで、確かに平均誤差が最も小さくなりました（**noveltyは特徴選択の結果が悪いため、ここでも後述でも割愛**）。
The error for the full set of metrics was much higher, probably due to overfitting.
metricsの全セットの誤差は、おそらくオーバーフィッティングのため、より高い値を示しました。(17個の説明変数?)
Diversity seemed to be very important in the first dataset, since it gave the best individual result as a predictor.
最初のデータセットでは、 Diversity が非常に重要であったようです。なぜなら、多様性は predictor として最も良い個人結果を与えたからです.(individual resultは相関係数的な意味だろうか? )
Combinations of different groups including diversity also gave better results than combinations that did not.
また、 **diversity を含む異なるグループの組み合わせは、そうでない組み合わせよりも良い結果(MSE?)**をもたらしました.
More complex models, such as penalized LR (All+L2) or the Gaussian process with an RBF kernel (GP+RBF), gave even better results, however these models are more difficult to interpret and use.
ペナルティ付きLR（All+L2）やRBFカーネル付きガウスプロセス（GP+RBF）など、より複雑なモデルはさらに良い結果(MSE?)を示したが、これらのモデルの解釈や使用はより困難である。
Note that results were consistent among datasets and that the best ones significantly outperformed the baseline model, which assumes constant CTR through time (Const).
なお、結果はデータセット間で一貫(diversity metricを含むとCTR予測のスコアは高くなる結果...!)しており、最も優れたものは、時間を通じて一定のCTRを仮定したベースラインモデルを大幅に上回っています（Const）。

![](https://camo.qiitausercontent.com/269f70a0ec79a22088733bd22b77bf063b3edde2/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32303931313066382d653631362d383962302d616531352d3862393463393164303065302e706e67)

Fig.5 shows that the aforementioned metrics indeed have a predictive power.
図5から、前述のmetricsが確かにオンライン性能の予測力を持つことがわかる.
The shape of the curve of the performance metric over time was repeated in the predicted results, indicating that there was high probability that the model would be able to predict the behavior and approximate values of the performance metric over time.
予測結果では、パフォーマンスメトリクスの経時的な曲線の形状が繰り返され、**モデルがパフォーマンスメトリクスの経時的な挙動やおおよその値を予測できる可能性が高い**ことが示されました.

The p-values associated with the regression coefficients of different metrics indicated that these predictors were significant for the model.
異なる指標の回帰係数に関連するp値は、これらのpredictorsがモデルにとって有意であることを示した。
A possible explanation for the only exception to this (Serendipity was not found to be an important predictor for Most Popular algorithm) is that all the Serendipity values for recommendations made by the Most Popular algorithm were 0 or close to 0.
**唯一の例外（SerendipityはMost Popularアルゴリズムの重要な予測因子であることが判明しなかった）**については、**Most Popularアルゴリズムによる推薦のSerendipity値がすべて0または0に近かったという説明が可能**である。
According to definitions of Serendipity, its values are high for items not recommended by the “naive” recommender, which is precisely the Most Popular recommender.
**Serendipityの定義によれば、その値は“naive”レコメンダー、つまりMost Popularレコメンダーが推薦しないアイテムに対して高くなる**。

Inspection of the coefficients revealed that the models were different for different datasets and algorithms.
係数を点検すると、データセットやアルゴリズムによって、モデルが異なることがわかった。
That is an expected indicator that a linear model made to predict the performance regardless of the algorithm, would perform worse than a set of models specifically trained for each algorithm.
これは、**アルゴリズムに関係なく性能を予測するために作られた線形モデルは、各アルゴリズムに特化して訓練されたモデルのセットよりも性能が低下する**ことを示す予想指標である。

### 5.3.2. Online accuracy prediction. オンライン精度予測。

(オンライン性能予測モデルの目的変数をCTRからオンライン精度に置き換えたもの.)
The results above were obtained assuming that the target online metric was CTR.
上記の結果は、対象となるオンライン指標をCTRと仮定して得られたものです。
We also trained a model to predict success, also called online accuracy (Tab.3).
また、オンライン精度とも呼ばれる成功予測モデルを学習させました（Tab.3）。

![](https://camo.qiitausercontent.com/4c8a1da25a386bf7995170daf2ad5a06ef1081f2/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f61336330386663642d363361622d333361662d333064302d3134326131626238383735392e706e67)

Prediction errors were less consistent among datasets, but a combination of Accuracy, Coverage, and Diversity predictors obtained high results for all datasets.
予測誤差はデータセット間であまり一致しなかったが、**Accuracy、Coverage、Diversityのpredictorsの組み合わせは、すべてのデータセットで高い結果を得た**.
On the Swissinfo dataset, best predictors came from three groups that did not include Diversity; on Yahoo, Diversity is the single best predictor (possibly due to the imperfect the visits were identified); and on the LePoint dataset the best predictors did not include Serendipity.
Swissinfoデータセットでは、最良の予測因子はDiversityを含まない3つのグループから得られた。Yahooでは、Diversityが唯一最良の予測因子であり（おそらく訪問の特定が不完全なため）、LePointデータセットでは、最良の予測因子にはSerendipityが含まれていない。
Note that the predicted results for the Random algorithm are more accurate than for the Most Popular algorithm – an expected result, as Random performance does not change much over time.
ランダムアルゴリズムの予測結果は、最も人気のあるアルゴリズムよりも正確であることに注意してください - ランダム性能は時間の経過とともにあまり変化しないので、これは予想された結果です。

## 5.4. Self-adjusting algorithm blend

For this experiment, we ran algorithms on a live news website.
今回の実験では、**ライブのニュースサイトでアルゴリズムを実行**しました。
We used four algorithms based on the linear combination of recommendations given by the Context Tree and Most Popular recommenders, as described in Section 4.2.We had two latent metrics, ZCT and Zpop, that measured the closeness of the recommendation to that of the two algorithms.
4.2節で説明したように，Context TreeとMost Popularの推薦者が与える**推薦の線形結合**に基づく**4つのアルゴリズム**(重み付け設定が異なる4種)を使用した。2つのアルゴリズムによる推薦に近いかどうかを測定する$Z_{CT}$と$Z_{pop}$という潜在的なメトリクスを用意した．
Weights for the recommendations from the Most Popular algorithm varied from 20% to 80% in steps of 20%.
Most Popularアルゴリズムによる推薦文の重みは、20%から80%まで20%刻みで変化しています。
In each time frame and for each recommender, the updated weight increased or decreased the trade-off.
各時間枠で、各推薦者について、更新されたウェイトはトレードオフを増減させた。
We examined whether changing the algorithm weighting in the direction indicated by the gradient really did give higher CTR (Fig.6).
そこで、アルゴリズムの重み付けをグラデーションで示す方向に変更することで、本当にCTRが高くなるのかどうかを検証しました（図6）。

![](https://camo.qiitausercontent.com/9d6e133271d568b8dca988aa4a83cd7eed03039c/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f31333466663762652d336434662d663733632d336565312d3835333036326237656666612e706e67)

In the third, fifth and seventh periods – during daytime – all coefficients suggested increasing the weight of the CT algorithm.
**第3期、第5期、第7期（日中）では、すべての係数がCTアルゴリズムのウェイトを高めることを示唆**しました。(i.e. 日中は、CTアルゴリズムの重み付けを高めるような予測結果になった)
At night, the algorithm with 20% of Most Popular was still best, but by a smaller margin, and the magnitude of the coefficients agreed with these results.
夜間では、Most Popularを20%使用したアルゴリズムが、より小さな差ではありますが、依然として最良であり、係数の大きさもこの結果と一致しました。

For the first two time periods the results were different, probably due to a lack of data.
最初の2つの期間については、データが不足しているためか、結果が異なっていました.
However, the changes suggested for increasing CTR were still consistent and correct – the regression coefficient for the algorithm using 40% of Most Popular was positive, suggesting an increase in weight, which lead to the algorithm using 60% of Most Popular, that did indeed obtain a higher CTR in this time frame.
しかし、CTRを向上させるために示唆された変化は、依然として一貫して正しいものでした。Most Popularの40%を使用するアルゴリズムの回帰係数はプラスで、重みの増加を示唆し、Most Popularの60%を使用するアルゴリズムにつながり、この時間枠で実際に高いCTRを得ることができました。

The performance clearly changed over time, but followed a periodic pattern.
性能は明らかに経年変化しているが、**周期的なパターン**を踏襲している。
This suggests that coefficients from the current time frame should provide suggestions to the same time frame next day, rather than the next chronological time frame.
これは、**現在の時間軸の係数が**、次の時系列の時間軸ではなく、**次の日の同じ時間軸への示唆を与えるべき**(i.e. 重み付け調整結果を次のtime frameではなく、次の日の同じ時間帯のtime frameの重み付けへ活用すべき...!)であることを示唆しています。

## 5.5. Unbiased offline evaluation オフラインでの偏りのない評価

In this subsection, we discuss and apply the unbiased offline evaluation procedure [11]; this is another approach to predicting an algorithm’s online performance.
このサブセクションでは、アルゴリズムのオンライン性能を予測するための別のアプローチである、**不偏のオフライン評価手順**[11]について説明し、適用します.
This procedure was developed for contextual bandit algorithms and requires the log of interaction with the world of an algorithm that recommends articles at random with equal probability.
この手順はコンテクストバンディットアルゴリズムのために開発されたもので、**等確率でランダムに記事を推薦するアルゴリズムの世界との対話のログが必要**です。
Based on this log, a simulation of online execution can be made for any other algorithm.
このログを元に、他のアルゴリズムでもオンライン実行のシミュレーションを行うことができます。
If the original log from the random algorithm had I events, then the simulation will contain approximately I/H events, where H is the number of items available for recommendation.
ランダムアルゴリズムによる元のログがI個のイベントであった場合、シミュレーションでは約$I/H$個のイベントが含まれることになる（$H$は推薦可能なアイテムの数）。
In the Yahoo dataset, which is specifically tailored to this procedure, H = 20.
この手順に特化したYahooのデータセットでは、H=20です。
However, in more realistic scenarios of news recommendations, such as the Swissinfo dataset, three out of 200 candidate items should be recommended, giving H = 2003 = 8M.
しかし、Swissinfoデータセットのような、より現実的なニュース推薦のシナリオでは、200の候補アイテムのうち3つを推薦する必要があり、$H = 200^3 = 8M$となります。
This does not produce enough events in the simulation to give significant results.
これでは、シミュレーションで十分なイベントが発生せず、有意な結果を得ることができません。

We used the Swissinfo dataset to test this algorithm.
このアルゴリズムのテストには、Swissinfoデータセットを使用した。
We used the output of the random algorithm to create a log and tested the CT algorithm on it.
ランダムアルゴリズムの出力を使ってログを作成し、その上でCTアルゴリズムをテストしました。
Due to the limitations described above, we were only able to compare algorithms for the task of top-1 recommendation.
上記の制限により、**トップ1レコメンデーションタスクのアルゴリズムのみを比較することができました**。
Even in the case of top-1 recommendation, after sampling we were left with only 266 points, compared to 55,587 points in the log.
トップ1推薦の場合でも、ログが55,587点であるのに対し、サンプリング後は266点しか残らなかった。
Fig.7 (bottom part) shows the plot using the real and predicted CTR values.
図7（下段）は、CTRの実測値と予測値を用いたプロットです。
If we ignore a slight bias, probably due to the small number of points sampled, the shapes of the curves are quite similar, which proves the effectiveness of the unbiased offline evaluation for single-item recommendation.
サンプリング点数の少なさに起因するわずかな偏りを無視すれば、曲線の形状は非常によく似ており、**single item推薦における不偏のオフライン評価の有効性**が証明された。
However, when we tried to use it for top-2 or top-3 recommendations, the number of sampled points decreased exponentially.
しかし、トップ2やトップ3の推薦に使おうとすると、サンプリング点数が指数関数的に減少してしまうのです。

![](https://camo.qiitausercontent.com/14c948970e81d36470e4cae8bdac19f2ec7a9ff6/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f30626563353037342d323862662d616231342d653634622d3231306630613463663336372e706e67)

To overcome this problem, we applied the same technique in order to predict the third recommendation only: all the algorithms returned their third best prediction and we computed a CTR using this data.
この問題を解決するために、同じ手法を3番目のレコメンデーションの予測にのみ適用しました。すべてのアルゴリズムが3番目に良い予測を返し、このデータを使ってCTRを計算しました。
However, it is clearly visible that there was little correlation between real and predicted values (Fig.7, top).
しかし、**実測値と予測値の間にはほとんど相関がない**ことがよくわかる（Fig.7、上）。(top-3推薦のうち3番目にのみ適用するのは無理そう...)
This was caused by the fact that the presence or absence of clicks on the third item depends on the first two items in the recommendation list, and this is not taken into consideration in this approach.
これは、3つ目の項目のクリックの有無が、レコメンドリストの最初の2つの項目に依存するため、このアプローチでは考慮されていないことが原因でした。
Statistical tests showed the significance of our findings (Student’s ttest, p-value < 0.05).
統計的検定により、今回の調査結果の有意性が示された（Student's ttest, p-value < 0.05）。

Other approaches for evaluating multiple recommendations by simulating clicks on the second and later items [23, 27] are not suitable for our task as they do not account for temporal effects in the data, and their hindsight models do not take into account parameters such as coverage, etc.
2つ目以降のアイテムへのクリックをシミュレートして複数の推薦を評価する他のアプローチ[23, 27]は、データにおける時間的効果を考慮しておらず、その後知恵モデルではカバー率などのパラメータを考慮していないため、我々のタスクには適さない。

# 6. Related work 関連作品

The work presented here concentrates on using different metrics to predict the online performance of news recommendations.
ここで紹介する研究は、ニュースレコメンデーションのオンラインパフォーマンスを予測するために、さまざまな指標を使用することに集中しています。
Several recommender systems have been implemented and evaluated on live news websites [3, 12, 20, 21].
いくつかの推薦システムが、ライブのニュースサイトで実装され、評価されている [3, 12, 20, 21]。
A number of previous works have advocated the use of multiple metrics for these evaluations [13, 17].
これらの評価には、多くの先行研究が複数のメトリクスの使用を提唱している[13, 17]。
Below, we describe separately works that introduced and optimized new metrics, and works that combined existing metrics into multi-objective optimization.
以下、新たな指標を導入して最適化した作品と、既存の指標を組み合わせて多目的最適化した作品に分けて説明する。

## 6.1. Recommendations using multiple metrics. 複数の指標を用いた推奨事項

The need to provide more diverse and unexpected recommendations that cover the items from the ’long tail’ was identified early in the history of recsys.
ロングテール」のアイテムをカバーする、より多様で意外性のあるレコメンデーションを提供する必要性は、recsysの歴史の中で早くから認識されていました。
Zhang et al.[29, 28] proposed optimizing the trade-off between the average accuracy of the recommendations and the average diversity between each pair of recommended items.
Zhangら[29, 28]は，推薦の平均精度と推薦項目の各ペア間の平均多様性のトレードオフを最適化することを提案した．
They pose this as a quadratic programming problem with binary variables that they relaxed by solving in the continuous domain.
彼らはこれを2値変数を持つ2次計画問題として提起し、連続領域で解くことで緩和しています。
However, they only measured the results via their newly introduced novelty metric and, they performed neither an online evaluation nor a user study.
しかし、彼らは新しく導入した新奇性という指標で結果を測定しただけで、オンライン評価もユーザー調査も行っていないのです。
Ziegler et al.[31] proposed a greedy strategy for solving a similar problem, where each item was selected in a way that minimized the average similarity to previously selected items.
Zieglerら[31]は、類似問題を解くために、以前に選択した項目との平均類似度を最小化する方法で各項目を選択する貪欲戦略を提案した。
The subsequent user survey and, as well as the regression model built on the top of it, indicated that both diversity and accuracy contributed positively to user satisfaction.
その後のユーザーアンケートと、その上に構築された回帰モデルから、多様性と精度の両方がユーザー満足度にプラスに寄与することが示されました。
To the best of our our knowledge, this work is the only one to have built a regression model to study how performance depends on metrics.
私たちの知る限り、パフォーマンスがメトリクスにどのように依存するかを研究するために回帰モデルを構築したのは、この作品だけです。
Two serendipity metrics [7, 14] have been proposed for the domains of music and TV show recommendation.
音楽とテレビ番組の推薦の領域では、2つのセレンディピティメトリクス[7, 14]が提案されています。
The authors compared different algorithms with respect to a newly introduced metric, without any attempt to draw a relationship between the desired performance metric and the serendipity metric.
著者らは、新たに導入された指標に関して異なるアルゴリズムを比較したが、望ましい性能指標とセレンディピティの指標との間に関係を描く試みは全くなかった。
Vargas et al.[24] proposed multiple probabilistic definitions of novelty and diversity metrics that incorporate certain previous definitions.
Vargasら[24]は、ある種の過去の定義を取り入れた、新規性と多様性のメトリックの複数の確率的定義を提案した。
They showed how probabilities can be used as building blocks for metric definitions and compared several state-of-the-art algorithms.
確率をメトリック定義のビルディングブロックとして使用できることを示し、いくつかの最先端のアルゴリズムを比較した。
Although the authors clarified the reasoning behind the probabilistic definitions they used, they proposed no algorithm to optimize towards any particular metric, and they drew no relationships with the performance metrics.
著者らは、使用した確率的定義の理由を明らかにしたが、特定の指標に向けて最適化するアルゴリズムを提案せず、パフォーマンス指標との関係も描かなかった。
Zhou et al.[30] proposed the concepts of “personalization” and “surprisal”, and they used a heat diffusion model on a bipartite graph representing links between items and users in order to optimize a linear combination of Accuracy and Diversity.
Zhouら[30]は，「パーソナライゼーション」と「サプライズ」という概念を提唱し，アイテムやユーザー間のリンクを表す2分木グラフに熱拡散モデルを用いて，精度と多様性の線形結合を最適化することを提案した．
The actual selection of tuning parameters, however, was done by hand.
しかし、実際のチューニングパラメーターの選定は、手作業で行っていました。

## 6.2. Multi-objective optimization. 多目的最適化を行う。

Multi-objective optimization of a list of items has been well investigated in the field of information retrieval [22, 25].
情報検索の分野では、項目リストの多目的最適化がよく研究されている[22, 25]。
In the area of recsys, one of the first attempts at multiobjective optimization [28] used a quadratic objective function that involved a linear combination of Accuracy and Diversity.
Recsysの分野では、多目的最適化の最初の試みの1つ[28]は、精度と多様性の線形結合を含む2次目的関数を使用しました。
Jambor et al.[9] enhanced this idea by adding the variance of ratings to the objective function in order to promote items from the “long tail”.
Jamborら[9]は、「ロングテール」からアイテムを促進するために、評価の分散を目的関数に加えることで、この考えを強化しました。
Rodriguez et al.[18] optimized a smoothed version of the average precision and normalized discounted cumulative gain (NDCG) metrics by using gradient-based methods.
Rodriguezら[18]は、平均精度と正規化割引累積利得（NDCG）メトリクスを勾配ベースの手法で平滑化したものを最適化した。
Their framework optimized the trade-off between the quality of recommendations and the deviation between given recommendations and the expected ground truth, but did not consider competing objectives.
彼らのフレームワークは、推薦の品質と、与えられた推薦と期待されるグランドトゥルースとの間の偏差の間のトレードオフを最適化したが、競合する目的を考慮しなかった。
Other works [1, 23] have expanded on ideas about optimizing a linear combination of metrics by using soft clustering of users.
他の作品[1, 23]では、ユーザーのソフトクラスタリングを使用することで、メトリクスの線形結合を最適化するというアイデアを拡張している。
In [23], a linear combination of Variance and Accuracy for a contextual bandit algorithm was optimized and the recommendations were shared between different clusters through the similarity of clusters, expressed as a Gaussian kernel.
23]では、コンテキストバンディットアルゴリズムのVarianceとAccuracyの線形結合を最適化し、ガウスカーネルで表現したクラスタの類似性によって、異なるクラスタ間で推薦文を共有しました。
Another line of research has been finding a Pareto-optimal frontier among multiple metrics, using genetic algorithms [16, 26].
また、遺伝的アルゴリズムを用いて、複数の指標の中からパレート最適なフロンティアを見つける研究も行われている[16, 26]。

# 7. Conclustion (ブックライブ)は月額制ではなくて、購入するConclustionを購入する際にお支払する方式になってます。

We investigated predicting the online performance of news recommendation algorithms by a regression model using offline metrics.
**オフラインの指標を用いた回帰モデルにより、ニュース推薦アルゴリズムのオンライン性能を予測することを検討**した。
Our results confirmed that there is more to online performance than just offline Accuracy.
この結果から**、オンラインのパフォーマンスには、オフラインのAccuracy以上のものがあることが確認できました**。
Other metrics, such as Coverage or Serendipity, play important roles in predicting or optimizing online metrics such as click-through rates.
また、カバレッジやセレンディピティといった指標は、クリックスルー率などのオンライン指標の予測や最適化において重要な役割を果たします。
The model can then be applied to trade-off curves for each algorithm constructed from offline data to select the optimal algorithm and parameters.
そして、オフラインデータから構築した各アルゴリズムのトレードオフ曲線にこのモデルを適用することで、最適なアルゴリズムとパラメータを選択することができます。

Regression models are best constructed for the particular user and item population; we did not find a universal formula for predicting online performance that would work for all settings.
**回帰モデルは、特定のユーザとアイテムの集団に対して構築するのが最適**です。すべての設定に通用するオンラインパフォーマンス予測の普遍的な公式は見つかりませんでした。
However, training a model separately from the algorithms still saves a lot of effort over blind A–B testing.
しかし、アルゴリズムとは別にモデルをトレーニングすることで、**ブラインドA-Bテストよりも多くの労力を節約することができます**。
Another application is to adapt parameters continuously in response to changes in user characteristics.
また、ユーザ特性の変化に応じて、**パラメータを連続的に適応させる**という応用もあります。(=複数の推薦アルゴリズムのブレンドの重み付けの事? もしくは単一の推薦アルゴリズムのハイパーパラメータを動的に変化させる事？多分次の文を見るに、前者の意味.)
In a setting where recommendations are obtained by mixing different algorithms, we proposed a method using latent metrics defined by the algorithms themselves, and showed that it correctly predicted the right adaptations in a live recommender system.
異なるアルゴリズムを混在させて推薦を得るという設定において、アルゴリズム自体が定義する潜在的なメトリクスを用いる方法を提案し、ライブ推薦システムにおいて正しい適応を正しく予測することを示しました。
