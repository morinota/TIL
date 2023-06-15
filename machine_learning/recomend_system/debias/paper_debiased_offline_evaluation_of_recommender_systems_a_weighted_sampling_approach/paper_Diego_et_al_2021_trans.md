## link リンク

https://link.springer.com/article/10.1007/s10844-021-00651-y
https://link.springer.com/article/10.1007/s10844-021-00651-y

## abstract アブストラクト

Offline evaluation of recommender systems (RSs) mostly relies on historical data, which is often biased.
レコメンダーシステム（RS）のオフライン評価は、そのほとんどが過去のデータに依存しており、そのデータには偏りがあることが多い。
The bias is a result of many confounders that affect the data collection process.
バイアスは、データ収集プロセスに影響する多くの交絡因子の結果である。
In such biased data, user-item interactions are Missing Not At Random (MNAR).
このような偏ったデータでは、ユーザーとアイテムの相互作用はMNAR（Missing Not At Random）である。
Measures of recommender system performance on MNAR test data are unlikely to be reliable indicators of real-world performance unless something is done to mitigate the bias.
MNARテストデータによる推薦システムの性能測定は、バイアスを軽減するための工夫がない限り、実世界の性能の信頼できる指標にはなりにくい。
One widespread way that researchers try to obtain less biased offline evaluation is by designing new, supposedly unbiased performance metrics for use on MNAR test data.
研究者がより偏りのないオフライン評価を得ようとする一つの方法として、MNARテストデータで使用するための新しい、本来は偏りのないパフォーマンスメトリクスを設計することが挙げられる。
We investigate an alternative solution, a sampling approach.
私たちは、別の解決策であるサンプリング・アプローチについて調査しています。
The general idea is to use a sampling strategy on MNAR data to generate an intervened test set with less bias — one in which interactions are Missing At Random (MAR) or, at least, one that is more MAR-like.
一般的なアイデアは、MNARデータのサンプリング戦略を用いて、よりバイアスの少ない介入テストセット（相互作用がMAR（Missing At Random）であるもの、あるいは少なくともよりMARに近いもの）を生成することです。
An existing example of this approach is SKEW, a sampling strategy that aims to adjust for the confounding effect that an item’s popularity has on its likelihood of being observed.
このアプローチの既存の例として、アイテムの人気が観察される可能性に与える交絡効果を調整することを目的としたサンプリング戦略であるSKEWがあります。
In this paper, after extensively surveying the literature on the bias problem in the offline evaluation of RSs, we propose and formulate a novel sampling approach, which we call WTD; we also propose a more practical variant, which we call WTD_H.
本論文では、RSのオフライン評価におけるバイアス問題に関する文献を幅広く調査した後、WTDと呼ぶ新しいサンプリングアプローチを提案・定式化し、さらにWTD_Hと呼ぶより実用的なバリエーションも提案する。
We compare our methods to SKEW and to two baselines which perform a random intervention on MNAR data.
本手法とSKEW、およびMNARデータに対してランダム介入を行う2つのベースラインを比較した。
We empirically validate for the first time the effectiveness of SKEW and we show our approach to be a better estimator of the performance that one would obtain on (unbiased) MAR test data.
SKEWの有効性を初めて実証的に検証し、我々のアプローチが（不偏の）MARテストデータで得られる性能のより良い推定値であることを示すことができました。
Our strategy benefits from high generality (e.g.it can also be employed for training a recommender) and low overheads (e.g.it does not require any learning).
我々の戦略は、高い汎用性（例：レコメンダーのトレーニングにも使用可能）と低いオーバーヘッド（例：学習を必要としない）の利点があります。

# Introduction 序章

Offline evaluation of a recommender system is done using an observed dataset, which records interactions (e.g.clicks, purchases, ratings) that occur between users and items during a given period in the operation of the recommender system.
レコメンダーシステムのオフライン評価は、レコメンダーシステムの運用期間中にユーザーとアイテムの間で発生したインタラクション（クリック、購入、評価など）を記録した観測データセットを用いて行われます。
However, this dataset is biased, not only due to the freedom that users have in choosing which items to interact with, but also due to other factors, known as confounders (Chaney et al., 2018; Wang et al., 2018).
しかし、このデータセットは、ユーザーがどのアイテムと対話するかを自由に選べるだけでなく、交絡因子と呼ばれる他の要因によって、偏りが生じます（Chaney et al, 2018; Wang et al, 2018）。
For example, the recommender system’s user interface acts as a source of confounding factors: differences in the ways that items are exposed to users (e.g.position on the screen) influence the likelihood of a user interacting with those items (Liang et al., 2016b).
例えば、レコメンドシステムのユーザーインターフェースは交絡因子の源として機能します。アイテムがユーザーにさらされる方法（画面上の位置など）の違いは、ユーザーがそれらのアイテムと対話する可能性に影響します（Liang et al., 2016b）。
The recommender itself sets up a feedback loop, which results in another confounder: users are often more likely to interact with the recommender’s suggestions than with other items.
レコメンダー自体がフィードバックループを作り、その結果、もう一つの交絡要因である、ユーザーは他のアイテムよりもレコメンダーの提案に接する傾向が強いことが多い。
The user’s preferences are also a confounder: for example, Marlin et al.demonstrate that, in a dataset of numeric ratings, the probability of not observing a specific user-item interaction depends on the rating value — informally, users tend to rate items that they like (Marlin et al., 2007).
例えば、Marlinらは、数値評価のデータセットにおいて、特定のユーザーとアイテムの相互作用を観察しない確率が評価値に依存することを実証している（非公式に、ユーザーは自分が好きなアイテムを評価する傾向がある）。
Because of these and other confounders, interactions that are missing from an observed dataset are Missing Not At Random (MNAR) (Marlin et al., 2007).
これらや他の交絡因子のために、観測されたデータセットから欠落している相互作用はMNAR（Missing Not At Random）である（Marlin et al, 2007）。

Classical offline evaluations using such an observed dataset are in effect making the assumption that interactions that are missing from the observed dataset are either Missing Completely At Random (MCAR) or Missing At Random (MAR) (Marlin et al., 2007).
このような観測データセットを用いた古典的なオフライン評価は、実質的に、観測データセットから欠落した相互作用はMCAR（Missing Completely At Random）またはMAR（Missing At Random）のいずれかであるという仮定を置いています（Marlin et al, 2007）。
(For the distinction between MCAR and MAR, see Section 2.2).
(MCARとMARの区別については、2.2項を参照ください）。
Using MNAR data in an evaluation as if it were MCAR or MAR, results in biased estimates of a recommender’s performance (Marlin et al., 2007): for example, such experiments tend to incorrectly reward recommenders that recommend popular items or that make recommendations to the more active users (Pradel et al., 2012; Cremonesi et al., 2010).
MNARデータをMCARやMARと同じように評価で使用すると、レコメンダーの性能の推定に偏りが生じます（Marlin et al., 2007）。例えば、このような実験は、人気のアイテムを推奨したり、よりアクティブなユーザーに推奨したりするレコメンダーに不正確に報いる傾向にあります（Pradel et al., 2012; Cremonesi et al., 2010）。

There are three ways of addressing this problem.
この問題に対して、3つの方法があります。
The most straightforward approach (in theory, at least) is to collect and employ a MAR dataset, instead of an MNAR one, for the offline evaluation.
最も簡単なアプローチは（少なくとも理論的には）、オフライン評価のために、MNARの代わりにMARデータセットを収集し採用することです。
Using (unbiased) MAR data for the evaluation would give an unbiased estimate of the recommender’s performance.
評価に（偏りのない）MARデータを使用することで、レコメンダーの性能を偏りなく推定することができます。
In some domains, there are ways of collecting small MAR-like datasets (see Section 2.3).
ドメインによっては、小さなMARのようなデータセットを収集する方法がある（2.3節参照）。
But, in many domains, it is either impractical or too expensive to obtain MAR-like datasets.
しかし、多くのドメインでは、MARのようなデータセットを入手するのは非現実的であったり、コストがかかりすぎたりします。

Because of the difficulty of collecting MAR-like data, the other two ways of addressing the problem focus on using MNAR data (which is usually available and in larger quantities) but mitigating its bias.
MARのようなデータの収集が困難なため、他の2つの方法では、MNARデータ（通常入手可能で量も多い）を使用しつつ、そのバイアスを軽減することに焦点を当てています。
One way of doing this is to design evaluation metrics which compensate for the bias in the MNAR test data.
その一つの方法として、MNARテストデータのバイアスを補正する評価指標を設計することが挙げられます。
Although this achieves the desired goal to some extent, unbiased metrics suffer from two potential drawbacks.
これはある程度望ましい目標を達成するものですが、不偏的なメトリクスは2つの潜在的な欠点に悩まされます。
The first is that they may not be general enough to overcome all sources of bias, i.e.they are often designed to compensate for a specific kind of bias: for example, the accuracy metric that is proposed in Steck (2011) is able to correct only for the long-tail popularity bias in a dataset.
例えば、Steck (2011)で提案されている精度指標は、データセットのロングテール人気バイアスのみを補正することができるものである。
The second drawback is that the unbiasedness of these metrics might be proven only if the data satisfies some specific conditions: the ATOP estimator proposed in Steck (2010), for example, is unbiased only if the data satisfies certain conditions.
第二の欠点は、これらの指標の不偏性が、データが特定の条件を満たす場合にのみ証明される可能性があることである。例えば、Steck (2010) で提案されたATOP推定量は、データが特定の条件を満たす場合にのみ不偏である。

The third approach is to intervene on MNAR test data before using it for the evaluation.
3つ目のアプローチは、評価に使う前にMNARのテストデータに介入することです。
In practice, such intervention is performed by means of a sampling strategy which samples from the available MNAR test data.
実際には、このような介入は、利用可能なMNARテストデータからサンプリングするサンプリング戦略によって実行されます。
The sampling strategy is chosen so that the intervened test set which results from the sampling is supposed to be less biased (more MAR-like) and therefore more suitable for evaluation of the recommender’s performance.
サンプリング戦略は、サンプリングの結果、介在するテストセットが偏りにくく（よりMAR的に）、レコメンダーの性能評価に適していると考えられるように選択される。
One such sampling strategy is known as SKEW (Liang et al., 2016a): it samples user-item interactions in inverse proportion to item popularity, thus producing test data with reduced popularity bias.
そのようなサンプリング戦略の1つはSKEW（Liang et al, 2016a）として知られており、アイテムの人気に反比例してユーザーとアイテムの相互作用をサンプリングし、人気バイアスを低減したテストデータを作成します。

In this paper, we investigate a new alternative for generating intervened data.
この論文では、介入されたデータを生成するための新しい選択肢を調査する。
Our main contributions are as follows:
私たちの主な貢献は以下の通りです：

- We survey the bias problem in the offline evaluation of RSs and the solutions that have been explored to cope with it. In particular, we describe the use of unbiased datasets and unbiased metrics, as well as the generation of intervened datasets to debias the evaluation; and we discuss the pros and the cons for each of them. RSのオフライン評価におけるバイアス問題と、それに対処するために検討されてきた解決策を調査する。 特に、偏りのないデータセットと偏りのないメトリクスの使用、および評価の偏りを解消するための介入データセットの生成について説明し、それぞれの長所と短所について議論する。

- We propose our own solution to debias the evaluation of an RS. Our method, which we designate WTD (and its variant WTD_H), intervenes on biased data to generate data that is less biased. WTD and WTD_H use a weighted sampling strategy in which the weights are calculated by considering the divergence between the distribution of users and items in the MNAR data and their corresponding target (unbiased) MAR distributions. RSの評価をデビアスするための独自のソリューションを提案します。 WTD（およびその変種WTD_H）と呼ぶこの方法は、偏ったデータに介入して、より偏りの少ないデータを生成するものである。 WTDとWTD_Hは、MNARデータにおけるユーザーとアイテムの分布と、それに対応するターゲット（不偏）のMAR分布との間の乖離を考慮して重みを計算する、重み付きサンプリング戦略を使用しています。

- We compare WTD and WTD_H with SKEW (Liang et al., 2016a), which is the closest intervention approach to ours. For the first time in the literature, we provide empirical evidence that WTD, WTD_H and SKEW are valid methods to perform the desired debiasing action. With experimental results for two publicly-available datasets, we demonstrate that our solution more closely approximates the unbiased performances of different recommender algorithms. Additionally, we show that it enjoys low overheads and high generality. For example, although in this paper we employ our technique to generate a test set for an offline recommender evaluation, our approach is general and can also be employed to debias the data used for training a recommender. WTDとWTD_Hを、私たちのものに最も近い介入アプローチであるSKEW（Liang et al, 2016a）と比較します。 文献上初めて、WTD、WTD_H、SKEWが所望のデビアス作用を行う有効な方法であることを実証的に証明した。 一般に公開されている2つのデータセットに対する実験結果を用いて、我々のソリューションが異なるレコメンダーアルゴリズムの不偏の性能をより忠実に再現することを実証する。 さらに、低いオーバーヘッドと高い汎用性を持つことを示す。 例えば、本稿ではオフラインのレコメンダー評価用のテストセットを生成するために本手法を採用していますが、本手法は一般的であり、レコメンダーのトレーニングに使用するデータをデビアスするために採用することも可能です。

This paper is an extension of Carraro and Bridge (2020), drawing additional material from Carraro (2021).
本稿は、Carraro and Bridge (2020) を拡張し、Carraro (2021) から追加資料を引用したものである。
The rest of its content is organised as follows.
その残りの内容は、以下のように整理されています。
Section 2 presents related work in the literature.
第2節では、文献における関連作業を紹介する。
In Section 3, we propose our own contribution to debiasing, which we call WTD (and its variant WTD_H).
セクション3では、WTD（およびその変形であるWTD_H）と呼ぶ、デビアスへの独自の貢献を提案する。
Section 4 describes the experiments we have run to assess the effectiveness of our approach.
セクション4では、本アプローチの有効性を評価するために実施した実験について説明する。
We analyse the results of the experiments in Section 5.
5節で実験結果を分析する。
We discuss our findings and future research directions in Section 6.
第6節では、得られた知見と今後の研究の方向性について述べる。

# Related work 関連作品

In this paper, we focus on the offline evaluation of recommender systems.
本稿では、レコメンダーシステムのオフライン評価に焦点を当てます。
In Section 2.1, we describe a general framework for the classic evaluation of an RS.
セクション2.1では、RSの古典的な評価のための一般的なフレームワークを説明します。
In Section 2.2, we give an overview of the bias problem that affects such evaluation.
2.2項では、このような評価に影響するバイアス問題の概要を説明する。
Then, in Sections 2.3, 2.4, 2.5, we review three different solutions to this problem that have been explored in the literature.
次に、セクション2.3、2.4、2.5では、この問題に対する文献で検討された3つの異なる解決策をレビューします。

## Offline evaluation of recommender systems 推薦者システムのオフライン評価

We consider a recommendation scenario where we define a user-item space, U × I, of size |U|⋅|I|.
U
We denote with u ∈ U = {1,..,|U|} a generic user, and with i ∈ I = {1,..,|I|} a generic item.
U
Offline evaluation of a recommender system is done using an observed dataset D, which, within the user-item space, records interactions that occur between users and items during a given period in the operation of the recommender system platform.
推薦システムのオフライン評価は、ユーザー・アイテム空間内で、推薦システムプラットフォームの運用において、ある期間にユーザーとアイテムの間で発生するインタラクションを記録した観測データセットDを用いて行われる。
Without loss of generality and because our experiments are performed with datasets of explicit ratings (see Section 4), from now on, we will consider such interactions to be numeric ratings.
一般性を損なわず、また、我々の実験は明示的な評価のデータセット（セクション4参照）を用いて行われるため、今後は、このようなやり取りを数値による評価とみなすことにする。

We visualize D as a |U|×|I| matrix, i.e.HCode D∈(R∪{⊥})|U|×|I|
U

, where the ru,i entry records the rating given by the user u to the item i if the rating is observed, ⊥ otherwise.
ここで、ru,iの項目は、ユーザuがアイテムiに与えた評価が観測された場合はその評価を、そうでない場合は⊥を記録する。
We write ru,i ∈ D if the rating is observed, i.e.ru,i≠⊥, and ru,i∉D if the rating is not observed, i.e.ru,i = ⊥.
評価が観測された場合、すなわちru,i≠⊥、評価が観測されなかった場合、すなわちru,i＝⊥の場合はru,i∉Dと表記します。
For RS, D is typically sparse, i.e.the number of observed ratings in D is much smaller than all the possible ratings in the whole user-item space.
RSの場合、Dは一般的にスパースである。つまり、Dで観測される評価の数は、ユーザーアイテム空間全体で可能なすべての評価よりもはるかに小さい。
We will write |D| for the number of real-valued entries, i.e.|D| = |{ru,i ∈ D}|.
D
Then, sparsity of the observed dataset means that |D| << |U|⋅|I|.
D
We denote with Du the observed ratings of the user u and with Di the observed ratings of the item i.
ユーザuの観測された評価をDu、アイテムiの観測された評価をDiと表記する。
We will also define the binary random variable O:U×I→{0,1}
また、二値確率変数O:U×I→{0,1}を定義しておく。

over the set of user-item pairs in D as O=1
Dに含まれるユーザーとアイテムのペアの集合をO=1としたとき

if the user-item rating is observed (real-valued) and O=0
ユーザーアイテムのレーティングが観測された場合（実数値）、O=0

otherwise (equal to ⊥).
でなければ（⊥に等しい）。
(Later, however, when writing probabilities, we will use abbreviation P(O)
(ただし、後に確率を表記する場合はP(O)と略記する)

in place of P(O=1)
に代わって、P(O=1)

).
).

To evaluate an RS, the observed ratings in D are typically partitioned into a training set matrix Dtr and a test set matrix Dte; more generally, a training set and a test set are sampled from D.
RSを評価するために、Dで観測された評価は、通常、訓練セット行列Dtrとテストセット行列Dteに分割され、より一般的には、訓練セットとテストセットは、Dからサンプリングされます。
The training and test sets are typically obtained by performing a random split of the real-valued ratings in D but ignoring the values of the ratings.
訓練セットとテストセットは、通常、D中の実数値の評価をランダムに分割するが、評価の値を無視することによって得られる。
Other, more specific protocols are sometimes used.
その他、より具体的なプロトコルが使用されることもあります。
For example, we might split the ratings on a per-user basis, or we might leverage side information such as the timestamp of the ratings to obtain a temporal split (Koren, 2009; Lathia, 2010).
例えば、ユーザー単位で評価を分割したり、評価のタイムスタンプなどのサイド情報を活用して時間的な分割を行ったりします（Koren, 2009; Lathia, 2010）。

Once the data is prepared, the experiment consists of using the algorithm under evaluation to train a recommender model on the training set Dtr; then, the model is tested using the test set Dte to provide one or more measures of the quality of the algorithm under evaluation.
データを準備したら、実験では、評価対象のアルゴリズムを使用して、トレーニングセットDtrでレコメンダーモデルをトレーニングし、テストセットDteでモデルをテストして、評価対象のアルゴリズムの品質に関する1つまたは複数の尺度を提供します。
Sometimes this process is performed k times, with k different training-test splits and results averaged across the k experiments.
時にはこの処理をk回行い、k種類のトレーニングとテストの分割を行い、結果をk回の実験で平均化します。

In early work in this field, there was a focus on accurate prediction of users’ ratings.
この分野の初期の研究では、ユーザーの評価を正確に予測することに焦点が当てられていました。
Hence, experiments used evaluation metrics that compare predicted and actual ratings for items in the test set Dte.
そこで、実験では、テストセットDteに含まれるアイテムの予測評価と実際の評価を比較する評価指標を用いた。
Examples of such metrics are the Root Mean Square Error (RMSE) and the Mean Absolute Error (MAE).
例えば、RMSE（Root Mean Square Error）やMAE（Mean Absolute Error）などが挙げられます。
More recently, the focus has shifted to top-n recommendation, i.e.whether a recommender model correctly ranks the set of a user’s heldout test items and especially whether it correctly identifies and ranks the first n such items.
最近では、推薦モデルが、ユーザーの保留されたテスト項目の集合を正しくランク付けするか、特に最初のn個の項目を正しく識別してランク付けするかという、トップnレコメンデーションに焦点が当てられています。
For this, we use evaluation metrics such as Precision, Mean Average Precision (MAP), Recall and Normalized Discounted Cumulative Gain (NDCG).
そのために、Precision、Mean Average Precision（MAP）、Recall、Normalized Discounted Cumulative Gain（NDCG）などの評価指標を使用します。
They require a definition of what it means for a test item that is recommended during the experiment to be relevant.
実験中に推奨されるテスト項目が関連性を持つとはどういうことなのか、その定義が必要なのです。
The typical definition is that a test item i is relevant to user u if ru,i exceeds some threshold.
典型的な定義は、ru,iがある閾値を超えた場合、テスト項目iはユーザーuに関連しているとするものである。
Specifically, for 1-5 star ratings datasets used in this paper, we define the item i to be relevant to the user u if ru,i > 3.F
具体的には、本稿で使用する1～5の星評価データセットにおいて、ru,i > 3.Fの場合、アイテムiはユーザーuに関連すると定義する。

## The bias problem バイアスの問題

It has been widely recognised in the literature that the observed datasets used in the offline evaluation of RSs are biased.
RSのオフライン評価で使用される観測データセットが偏っていることは、文献で広く認識されています。
The bias in a dataset is caused by many factors, known as confounders, that influenced the collection of the dataset (Chaney et al., 2018; Wang et al., 2018).
データセットのバイアスは、データセットの収集に影響を与えた交絡因子と呼ばれる多くの要因によって引き起こされる（Chaney et al.、2018；Wang et al.、2018）。
For example, users usually experience what we can call item discovery bias because the RS acts as a confounder in the way that items are exposed to users (Cañamares and Castells, 2018).
例えば、アイテムがユーザーに露出する方法においてRSが交絡因子として働くため、ユーザーは通常、アイテム発見バイアスと呼べるものを経験します（Cañamares and Castells, 2018）。
Indeed, the recommender’s user-interface plays an important role as a confounder, e.g.the position of items on the screen influences the likelihood of a user interacting with those items (Liang et al., 2016b).
実際、レコメンダーのユーザーインターフェースは交絡因子として重要な役割を果たしており、例えば、画面上のアイテムの位置は、ユーザーがそれらのアイテムと対話する可能性に影響を与えます（Liang et al., 2016b）。
Also, the recommender’s algorithm sets up a feedback loop, which results in another confounder: users are typically more likely to interact with the recommender’s suggestions than with other items.
また、レコメンダーのアルゴリズムは、フィードバックループを設定し、その結果、別の交絡要因が発生します：ユーザーは通常、他のアイテムよりもレコメンダーの提案と対話する傾向があります。
The user’s preferences are also a confounder because they influence whether to consume an item or not (item consumption bias) and whether to rate an item or not (rating decision bias).
また、ユーザーの嗜好は、アイテムを消費するかしないか（アイテム消費バイアス）、アイテムを評価するかしないか（評価決定バイアス）に影響するため、交絡因子となる。
In a typical RS scenario, users are free to consume the item if they wish and, usually afterwards, they are free to rate the item or not.
典型的なRSシナリオでは、ユーザーは希望すれば自由にアイテムを消費し、通常はその後に、アイテムを評価するかしないかを自由に決めることができます。
Their behaviour is often guided by their preferences on those items: for example, Marlin et al.demonstrate that, in a dataset of numeric ratings, the probability of not observing a specific user-item rating depends on the value associated with that particular rating — informally, users tend to rate items that they like (Marlin et al., 2007).
例えば、Marlinらは、数値評価のデータセットにおいて、特定のユーザーとアイテムの評価を観察しない確率が、その特定の評価に関連する値に依存することを実証している（非公式には、ユーザーは自分が好きなアイテムを評価する傾向がある）（Marlin et al.
User preferences and the characteristics of an RS are confounders that may also contribute to the so-called item popularity bias, i.e.the tendency of users to interact with popular or mainstream items rather than unpopular or niche items.
ユーザーの好みやRSの特性は、いわゆるアイテム人気バイアス（不人気アイテムやニッチなアイテムよりも、人気アイテムやメインストリームに接する傾向がある）の原因となる交絡因子である可能性がある。
This bias gives rise to the long-tail popularity curve (Hart, 2007), a well-known phenomenon in many RS datasets, where the distribution of the user interactions with items is skewed towards a few popular items (Celma, 2008; Abdollahpouri et al., 2017); see Fig.1 for an example.
このバイアスは、多くのRSデータセットでよく知られている現象であるロングテール人気曲線（Hart, 2007）を生じさせ、アイテムに対するユーザーインタラクションの分布が少数の人気アイテムに偏る（Celma, 2008; Abdollahpouri et al, 2017）；例として図1参照。
There are many publications that measure and explore popularity bias, for example, Pradel et al.(2012) and Abdollahpouri et al.(2017).
例えば、Pradel et al(2012)やAbdollahpouri et al(2017)など、人気バイアスを測定・探求した論文は数多く存在します。

Because of these and other confounders, classical offline evaluations, which use biased observed datasets, result in biased (i.e.incorrect) estimates of a recommender’s performance (Marlin et al., 2007).
これらや他の交絡因子のために、偏った観測データセットを使用する古典的なオフライン評価は、推薦者の性能の偏った（すなわち不正確な）推定につながる（Marlin et al.）
They are biased evaluations.
偏った評価になってしまうのです。
For example, such experiments tend to incorrectly reward recommenders that recommend popular items or that make recommendations to the more active users; or they favour recommender approaches that exploit the bias in the dataset (Pradel et al., 2012; Cremonesi et al., 2010; Bellogín et al., 2017).
例えば、このような実験では、人気のあるアイテムを推奨するレコメンダーや、よりアクティブなユーザーに推奨を行うレコメンダーに不正に報酬を与える傾向があったり、データセットのバイアスを利用するレコメンダーアプローチが好まれたりします（Pradel et al., 2012; Cremonesi et al., 2010; Bellogín et al, 2017）．

Work in the RS field that seeks to handle the evaluation bias problem often leverages concepts from the fields of missing data analysis or causal inference.
評価バイアスの問題を扱うRSの分野では、しばしば欠損データ解析や因果推論の分野の概念を活用することがあります。
The missing data analysis theories, firstly proposed by Little and Rubin (1986) and later introduced into the recommender systems literature by Marlin et al.(2007), categorise different types of datasets based on so-called missing data mechanisms, which describe the process that generates the interaction patterns in the data.
LittleとRubin(1986)によって最初に提案され、後にMarlin et al.(2007)によって推薦システムの文献に導入された欠損データ分析理論は、いわゆる欠損データメカニズムに基づいて異なるタイプのデータセットを分類し、データ中の相互作用パターンを生成するプロセスを記述します。
According to those theories, interactions that are missing from an observed dataset are Missing Not At Random (MNAR) (Marlin et al., 2007) because of the many confounders, i.e.the dataset is biased.
これらの理論によれば、観測されたデータセットから欠落している相互作用は、多くの交絡因子のためにMNAR（Missing Not At Random）（Marlinら、2007）、すなわちデータセットが偏っていることになります。
Nevertheless, classical offline evaluations using such an observed dataset are in effect making the assumption that missing interactions are either Missing Completely At Random (MCAR) or Missing At Random (MAR) instead (Marlin et al., 2007).
しかし、このような観測データセットを用いた古典的なオフライン評価では、事実上、欠損した相互作用はMCAR（Missing Completely At Random）またはMAR（Missing At Random）のいずれかであると仮定しています（Marlin et al, 2007）．
(For the distinction between MCAR and MAR, see below).
(MCARとMARの区別については、下記参照）。
Using MNAR data in an evaluation as if it were MCAR or MAR results in a biased evaluation.
MNARのデータをMCARやMARと同じように評価すると、偏った評価になってしまいます。

In work on causal inference, the same missing data mechanisms are typically called the assignment mechanisms (Imbens and Rubin, 2015).
因果推論に関する研究では、同じ欠損データ機構を一般的に割り当て機構と呼ぶ（Imbens and Rubin, 2015）。
Roughly speaking, in a recommendation scenario the assignment mechanism exposes users to items and influences the interaction patterns of such users, e.g.analogously to exposing a patient to treatment and later observing its outcome in a medical study.
大雑把に言えば、推薦シナリオでは、例えば医学研究において患者に治療を施し、その結果を観察するように、割り当てメカニズムがユーザーにアイテムを公開し、そのユーザーの対話パターンに影響を与える。
As with the missing data mechanisms, ignoring the biased nature of the assignment mechanism most likely results in a biased evaluation.
欠測メカニズムと同様に、割り当てメカニズムの偏った性質を無視すると、偏った評価になってしまう可能性が高いです。

In this paper, we use the missing data analysis terminology, i.e.MNAR, MAR, MCAR, and we want to make clearer how we use it in the following.
本稿では、MNAR、MAR、MCARといった欠損データ解析の専門用語を用いているが、以下ではその使い分けを明確にしたいと思う。
In the literature, a distinction is sometimes drawn between Missing Completely At Random (MCAR) and Missing At Random (MAR).
文献では、MCAR（Missing Completely At Random）とMAR（Missing At Random）に区別されることがあります。
In Little and Rubin (1986) and Marlin et al.(2007), MCAR means that whether a user-item interaction is missing or not does not depend at all on interaction values (such as the values of the ratings in a recommender), i.e.it depends neither on the observed interaction values nor the missing interaction values.
Little and Rubin (1986) や Marlin et al. (2007) では、MCARとは、ユーザーとアイテムの相互作用が欠損しているかどうかは、相互作用値（レコメンダーにおける評価の値など）に全く依存しない、つまり、観察された相互作用値にも欠損した相互作用値にも依存しないことを意味している。
MAR, on the other hand, means that whether a user-item interaction is missing or not may depend on the observed interaction values, but is independent of the missing interaction values.
一方、MARは、ユーザーとアイテムのインタラクションが欠損しているかどうかは、観測されたインタラクション値に依存する可能性があるが、欠損したインタラクション値には依存しないことを意味します。
However, in this paper, we use MNAR and MAR in a more informal and general way.
しかし、本論文では、MNARとMARをより非公式かつ一般的な方法で使用します。
We use MNAR to indicate that data is biased because missing interactions depend on some confounders.
MNARは、欠損した相互作用が何らかの交絡因子に依存しているため、データに偏りがあることを示すために使用する。
Thus we use the terms MNAR and “biased” interchangeably.
そのため、MNARと "biased "という言葉を同じ意味で使っています。
We use MAR to refer to data that is unbiased, where missing interactions do not depend on any confounder.
欠損した相互作用がどの交絡因子にも依存しない、不偏性のあるデータを指してMARと呼んでいます。
Thus we use the terms MAR and “unbiased” interchangeably.
したがって、私たちはMARと「不偏不党」という言葉を使い分けています。
Although these more informal usages are not properly in line with the categorisation in Little and Rubin (1986) and Marlin et al.(2007), our choice is broadly in line with other work in the recommender systems literature: what we refer to as MAR is also called MAR in papers such as Steck (2010) and Cañamares and Castells (2018).
これらのより非公式な用法は、Little and Rubin (1986) や Marlin et al. (2007) の分類と正しく一致していませんが、私たちの選択は、推薦システム文献の他の仕事と広く一致しています：私たちがMARと呼ぶものは、Steck (2010) や Cañamares and Castells (2018) などの論文でもMARと呼ばれています。
But what we call MAR is also referred to as MCAR in papers such as Schnabel et al.(2016) and Kim and Choi (2014).
しかし、我々がMARと呼んでいるものは、Schnabel et al.(2016) やKim and Choi (2014) などの論文ではMCARとも呼ばれている。

There are three main ways by which experiment designers address the bias problem in the offline evaluation of RSs, and each of them will be reviewed in the following three sections.
RSのオフライン評価において、実験設計者がバイアス問題に対処する方法は主に3つあり、以下3つのセクションでそれぞれについてレビューする。
In Section 2.3, we describe a protocol to collect a MAR-like dataset which can be used instead of an MNAR dataset for the offline evaluation.
セクション2.3では、オフライン評価のためにMNARデータセットの代わりに使用できるMARライクなデータセットを収集するためのプロトコルについて説明する。
In Sections 2.4 and 2.5, we describe unbiased metrics and debiasing interventions, respectively — two solutions that allow ‘debiased’ evaluations on MNAR data.
セクション2.4と2.5では、MNARデータで「偏った」評価を可能にする2つのソリューションである、偏りのない測定基準と偏りのない介入について、それぞれ説明する。
Other approaches to unbiased evaluation have been published in recent years but in the specific context of RS that use Reinforcement Learning.
また、近年、強化学習を用いたRSに特化した偏りのない評価へのアプローチも発表されています。
A few examples for the interested reader are Huang et al.(2020), Ie et al.(2019), and Shi et al.(2019) We do not review these in any further detail because they are only partially related to the classical way of evaluating RSs (Section 2.1) and they do not always explicitly address the bias problem, tackling it only indirectly.
興味のある読者のためにいくつかの例を挙げると、Huang et al.(2020), Ie et al.(2019), Shi et al.(2019) これらをさらに詳しくレビューしないのは、RSの古典的評価方法（2.1節）と部分的にしか関係がなく、バイアス問題に必ずしも明示的に取り組まず、間接的にしか取り組んでいないためです。
There is also a substantial body of work that has been done in the last few years to cope with bias during the training of RSs models, but we do not review this either, since this paper focuses on the evaluation of RSs only.
また、RSモデルの学習時のバイアスに対処するための研究もここ数年で相当数行われているが、本稿ではRSの評価のみに焦点を当てるため、これについてもレビューしない。

## Collection of unbiased datasets 偏りのないデータセットの収集

The ‘straightforward’ approach for coping with bias in the offline evaluation of an RS is to separately collect some unbiased data and use it as the test set.
RSのオフライン評価でバイアスに対処するための「正攻法」は、バイアスのないデータを別途収集し、それをテストセットとして使用することです。
This can be done with what is sometimes called a “forced ratings approach” Cañamares and Castells (2018).
これは、「強制視聴率アプローチ」と呼ばれることもあるCañamares and Castells (2018)で行うことができます。
For a ratings dataset, user-item pairs are chosen uniformly at random and for each user-item pair that gets selected the user is required (“forced”) to provide a rating for the item.
評価データセットでは、ユーザーとアイテムのペアが一様にランダムに選ばれ、選ばれた各ユーザーとアイテムのペアに対して、そのアイテムに対する評価を提供することが求められる（「強制」）。
Thus, randomly-selected users are required to rate randomly-selected items.
このように、ランダムに選ばれたユーザーが、ランダムに選ばれたアイテムを評価することが求められている。
A dataset that is collected in this way will largely not exhibit the biases that we find in datasets that are collected during the normal operation of an RS (see Section 2.2).
このようにして収集されたデータセットには、RSの通常運用時に収集されるデータセットに見られるようなバイアスはほとんど見られない（セクション2.2参照）。
For example, we get rid of the item discovery bias and the popularity bias because items are randomly chosen: no confounders play any role in their selection.
例えば、項目発見バイアスや人気バイアスは、項目がランダムに選択されるため、交絡因子がその選択に関与しないため、取り除かれる。
Items are not ones that are being exposed by the RS on the one hand, and users are not free to select them on the other hand (Cañamares & Castells, 2018); therefore, it is unlikely that we observe long-tail phenomenona in such datasets.
アイテムは一方ではRSが公開しているものではなく、他方ではユーザーが自由に選択できるものでもない（Cañamares & Castells, 2018）ので、このようなデータセットでロングテール現象が観察されることはないだろう。
The forced ratings approach also removes the item consumption bias because, users are forced to consume or interact with the item so that they can rate it Cañamares and Castells (2018).
また、強制評価アプローチは、ユーザーがアイテムを評価するために、アイテムを消費したり対話したりすることを余儀なくされるため、アイテムの消費バイアスを取り除くことができます。
(Since the user must rate the item, the only legitimate reason for not consuming the item before supplying the rating is if the item was already known to the user).
(ユーザはアイテムを評価しなければならないので、評価を提供する前にアイテムを消費しない正当な理由は、そのアイテムがユーザにとって既に知られていた場合のみである）。
In a typical RS scenario, by contrast, users are free to consume the item if they wish.
一方、一般的なRSのシナリオでは、ユーザーは自由にアイテムを消費することができます。
The rating decision bias is also removed because users are not free to decide whether or not to rate the chosen item; they are required to rate it Cañamares and Castells (2018).
また、選ばれたアイテムを評価するかどうかをユーザーが自由に決められるわけではなく、評価することが求められるため、評価決定バイアスは取り除かれる Cañamares and Castells (2018).

However, datasets collected by the forced ratings approach are MAR-like, rather than MAR: they may still carry some bias.
しかし、強制視聴率方式で収集されたデータセットは、MARというよりMAR的なもので、やはり多少のバイアスがかかっている可能性があります。
When building such a dataset, for example, although invitations are sent to users who are chosen uniformly at random, those who agree to participate may be atypical, thus introducing bias.
例えば、このようなデータセットを構築する場合、ランダムに選ばれた一様なユーザーに招待状を送るものの、参加に同意したユーザーが非典型的である可能性があり、バイアスが発生することがあります。
Equally, the fact that, for each user, items to rate are presented sequentially introduces bias: the rating a user assigns to a particular item may be influenced by the items she has rated so far.
また、各ユーザーの評価項目が順次表示されるため、ある項目に対する評価が、それまでに評価した項目の影響を受けてしまうというバイアスが発生します。
Although this means that these datasets are less biased, rather than unbiased, to the best of our knowledge, this is still the best way of collecting this type of data.
これは、これらのデータセットが、私たちの知る限りでは、偏りがないどころか、むしろ偏りが少ないことを意味しますが、それでもこの種のデータを収集するには、これが最良の方法です。

Furthermore, the forced ratings approach can only work in certain domains; for example, it requires that a user who is presented with an item can quickly consume that item (or part of it) in order to form an opinion of it.
さらに、強制評価方式は、あるアイテムを提示されたユーザーが、そのアイテム（またはその一部）に対する意見を形成するために、そのアイテムを素早く消費できることが必要であるなど、特定のドメインでしか機能しません。
In the movie domain, for example, we almost certainly cannot require a user to watch an entire movie (although we could require them to watch a movie trailer).
例えば映画の領域では、ユーザーに映画全体を見ることを要求することはほぼ不可能です（映画の予告編を見ることを要求することは可能です）。
Similarly, the forced ratings approach is impracticable in a tourism domain where a recommender suggests point-of-interests to its users: users cannot really be expected to visit the selected places in order to ‘consume’ and rate them (although we could require them to watch an advertisement video about such places).
同様に、強制的な評価アプローチは、レコメンダーがユーザーに興味のある場所を提案する観光の領域では実用的ではありません。ユーザーは、「消費」して評価するために、選択した場所を実際に訪れることは期待できません（その場所に関する広告ビデオを見ることを要求することはできますが）。

Datasets collected by the forced ratings approach include Webscope R3 (Marlin et al., 2007) and cm100k (Cañamares & Castells, 2018) in the music domain, and CoatShopping (Schnabel et al., 2016) in the clothing domain.
強制評価アプローチで収集されたデータセットには、音楽領域ではWebscope R3 (Marlin et al, 2007)やcm100k (Cañamares & Castells, 2018)、衣類領域ではCoatShopping (Schnabel et al, 2016)があります。
We will present these datasets in more detail and use them in the experiments of Section 4.
これらのデータセットをより詳細に紹介し、セクション4の実験に使用することにする。

## Unbiased metrics 不偏不党の指標

The majority of the literature tries to overcome the bias in an MNAR test set by proposing new evaluation metrics which provide unbiased or nearly unbiased measures of performance on the MNAR test data.
多くの文献は、MNARテストセットにおける偏りを克服するために、MNARテストデータにおける性能の偏りのない、あるいはほぼ偏りのない測定値を提供する新しい評価指標を提案しています。
Such measures are supposed to be less affected by the bias in the data and, therefore, more suitable for estimating the true performance of a recommender model.
このような指標は、データのバイアスの影響を受けにくいため、レコメンダーモデルの真の性能を推定するのに適していると考えられています。
In some of the RS literature, e.g.Schnabel et al.(2016), Steck (2010, 2011) and Yang et al.(2018), metrics of this kind are often called ‘estimators’: estimators are used in statistics to calculate an estimate of a given quantity of interest (a recommender’s performance in our case) from observed data (test set data in our case).
RSの文献の一部、例えばSchnabel et al.(2016), Steck (2010, 2011) and Yang et al.(2018) では、この種のメトリクスはしばしば「推定量」と呼ばれます：推定量は、観測データ（我々の場合はテストセットデータ）から、ある関心量（我々の場合は推薦者の性能）の推定値を計算するために統計で用いられます。
This terminology might suit an RS evaluation that takes a statistical framework perspective, e.g.Schnabel et al.(2016).
この用語は、例えばSchnabel et al(2016)のような、統計的枠組みの視点を取り入れたRS評価に適しているかもしれません。
However, in this paper, we prefer the term ‘metric’ to indicate a ‘tool’ that measures a recommender performance based on available test data.
しかし、本論文では、利用可能なテストデータに基づいてレコメンダーの性能を測定する「ツール」を示す「メトリック」という用語を使用する。

In Steck (2010, 2013), Steck designs ATOP, a new ranking metric that corrects for the biased measurements of Recall on an MNAR test set.
Steck (2010, 2013)では、Steckは、MNARテストセットにおけるRecallの偏った測定値を補正する新しいランキングメトリックであるATOPを設計しています。
However, this metric is unbiased only under two assumptions that must hold for the test set data.
しかし、この指標は、テストセットデータに対して成立しなければならない2つの仮定の下でのみ不偏である。
The first is that relevant ratings (which are typically a tiny fraction of all the possible ratings in the user-item space) are Missing At Random in the observed data.
第一に、関連する評価（一般に、ユーザーアイテム空間におけるすべての可能な評価のごく一部である）が、観測データにおいてランダムに欠落していることである。
The second, regarding the non-relevant ratings, is that they are missing with a higher probability than the relevant ratings.
2つ目は、非関連評価について、関連評価よりも高い確率で欠落していることです。
In practice, the two assumptions allow the author to ‘ignore’ the missing data mechanism for non-relevant missing ratings (i.e.no missing data model is required).
実際には、この2つの仮定により、著者は関連性のない欠測については欠測メカニズムを「無視」することができます（すなわち、欠測モデルは必要ありません）。
Also, there is no need for a missing data model for the missing relevant ratings at all (because they are missing at random).
また、関連する評価の欠損については、欠損データモデルは全く必要ありません（ランダムに欠損するため）。
However, unbiasedness of ATOP is not always guaranteed, i.e.in datasets where these assumptions are unrealistic.
しかし、これらの仮定が非現実的なデータセットでは、ATOPの不偏性が必ずしも保証されません。

There is also work that tries to tackle specific biases in the data.
また、データの特定のバイアスに取り組もうとする仕事もある。
For example, in Steck (2011), Steck designs a modified version of the Recall metric that corrects for the long-tail item popularity bias.
例えば、Steck (2011) では、ロングテールの項目人気バイアスを補正する Recall メトリクスの修正版を設計しています。
He modifies the definition of Recall by introducing weights that are proportional to the inverse popularity of the test set items.
彼は、テストセット項目の逆人気に比例する重みを導入することで、Recallの定義を変更しました。
The resulting metric, which he calls Popularity-Stratified Recall, is considered a nearly unbiased metric under the assumption that no other confounders besides item popularity bias occur in the test data.
その結果、彼はPopularity-Stratified Recallと名付けたが、テストデータに項目の人気バイアス以外の交絡因子が発生しないと仮定した場合、ほぼ不偏の指標と考えられる。

In Schnabel et al.(2016), the authors derive ‘unbiased’ versions of many widely-used metrics, both for ratings prediction (e.g.MAE and Mean Square Error) and top-n recommendation (e.g.Precision and nDCG).
Schnabelら(2016)では、視聴率予測（MAEやMean Square Errorなど）とトップn推薦（PrecisionやnDCGなど）の両方で、広く使われている多くの指標の「不偏」バージョンを導出しています。
The ‘unbiased’ versions are based on the concept of Inverse-Propensity-Scoring (IPS) (Imbens and Rubin, 2015; Little & Rubin, 1986; Thompson, 2012).
不偏」バージョンは、Inverse-Propensity-Scoring（IPS）の概念に基づいている（Imbens and Rubin, 2015; Little & Rubin, 1986; Thompson, 2012）。
A propensity score of a particular user-item pair Pu,i is the probability of that pair being observed.
特定のユーザーとアイテムのペアPu,iの傾向スコアは、そのペアが観察される確率を示す。
IPS-based metrics use the propensity scores to weight the prediction/ranking errors on the test data computed by one of the standard metrics above.
IPSベースのメトリクスは、傾向スコアを使用して、上記の標準的なメトリクスの1つによって計算されたテストデータ上の予測/ランキングの誤差を重み付けする。
Schnabel et al.propose two different ways of estimating propensities for MNAR ratings datasets: one using Naive Bayes, and the other using Logistic Regression.
Schnabelらは、MNARの評価データセットに対して、ナイーブベイズとロジスティック回帰を用いた2種類の予感の推定方法を提案しています。
While the former is an inexpensive approach, it requires a sample of MAR data; their approach to the latter does not require any additional MAR data but it is instead more expensive and requires additional data (side data) about users and items (e.g.user gender and item features).
前者は安価なアプローチですが、MARデータのサンプルが必要です。後者に対する彼らのアプローチは、追加のMARデータを必要としませんが、代わりにユーザーやアイテムに関する追加データ（サイドデータ）（ユーザーの性別やアイテムの特徴など）が必要となり、より高価です。

There is other work that uses IPS-based techniques to design unbiased metrics.
他にも、IPSベースの技術を使って、不偏のメトリクスを設計する研究があります。
For example, similarly to Schnabel et al.(2016), Yang et al.propose new unbiased metrics to obtain widely-employed ranking measures (e.g.Recall and nDCG) on implicit MNAR datasets (2018).
例えば、Schnabelら(2016)と同様に、Yangら(2018)は暗黙のMNARデータセットで広く使われているランキング指標（e.g.Recall and nDCG）を得るために新しい不偏のメトリクスを提案しています。
The propensity score is modelled around the concept of item popularity and, in practice, it is calculated as the product of the probability that an item is recommended to the user and the probability that the user interacts with the item (given that the item has been recommended).
傾向スコアは、アイテムの人気度という概念でモデル化されており、実際には、アイテムがユーザーに推奨される確率と、（アイテムが推奨されたとして）ユーザーがそのアイテムと対話する確率の積として計算されます。
However, the calculation makes strong assumptions about how data is generated.
しかし、この計算では、データの生成方法について強い仮定が必要です。
The assumptions include, for example, that the propensity scores are user-independent (i.e.Pu,i = Pi); that the user interacts with all the items she likes in the recommended set; and that her preferences are not affected by such recommendations.
この仮定には、例えば、傾向スコアがユーザに依存しないこと（すなわちPu,i = Pi）、ユーザが推奨セット内の好きなアイテム全てと対話すること、そして、ユーザの好みがそのような推奨によって影響を受けないこと、が含まれる。
These assumptions do not hold in general, thus limiting the usefulness of this framework.
これらの仮定は一般的には成立しないため、このフレームワークの有用性は限定的である。

Lim et al.also propose a metric for implicit MNAR datasets (2015).
Lim et al.も暗黙のMNARデータセットに対するメトリックを提案している（2015）。
They first assume a missing data model under which the observed dataset has been collected.
まず、観測されたデータセットが収集された欠損データモデルを仮定する。
Essentially, this model is that items that are relevant to users are Missing At Random.
本来、このモデルは、ユーザーに関連するアイテムはMissing At Randomであるというものである。
(This is like one of the assumptions in Steck (2010)).
(これはSteck(2010)の前提の1つと同じです）。
Then, they design a novel evaluation measure, which they call Average Discounted Gain (ADG), that is built upon the nDCG metric.
そして、nDCG指標をベースに、Average Discounted Gain（ADG）と呼ぶ新しい評価指標を設計している。
Unlike nDCG, they show that ADG allows unbiased estimation of top-n recommendation performances on test data which complies with their missing data model.
nDCGとは異なり、ADGでは、欠損データモデルに準拠したテストデータにおいて、トップn推薦性能の不偏推定が可能であることを明らかにした。

Finally, Krichene and Rendle (2020) present another interesting piece of work on implicit datasets that investigates the effectiveness of what the authors call ‘sampled metrics’.
最後に、Krichene and Rendle (2020)は、暗黙のデータセットについて、著者らが「サンプリングメトリクス」と呼ぶものの有効性を調査した、別の興味深い作品を紹介しています。
Sampled metrics are common evaluation metrics such as, for example, Precision and Recall, but used to measure a recommender’s quality with a testing procedure that speeds up the evaluation (i.e.typically, the evaluation is performed by randomly sampling a small set of irrelevant items and ranking the relevant test set items only among this smaller set, instead of ranking test set items against the entire item catalogue), e.g.Cremonesi et al.(2010) and Ebesu et al.(2018).
サンプリングメトリクスは、例えばPrecisionやRecallなどの一般的な評価メトリクスですが、評価を高速化するテスト手順（すなわち、典型的には、アイテムカタログ全体に対してテストセットアイテムをランキングするのではなく、無関係なアイテムの小さなセットをランダムにサンプリングして、この小さなセットの中でだけ関連するテストセットアイテムをランキングすることによって評価を行う）で推薦者の品質を測定するために使用されています、例えばCremonesi et al(2010) とEbesu et al(2018).
The authors show that a sampled metric can be a poor estimator of the true performances of recommender algorithms and suggest that the use of sampling in the evaluation should be avoided when possible.
著者らは、サンプリングされたメトリックは、レコメンダーアルゴリズムの真の性能の低い推定値となり得ることを示し、評価におけるサンプリングの使用は可能な限り避けるべきであることを示唆している。
However, when sampling is required, the authors propose modifications that correct sampled metric measurements and give a better estimate of the true performances (however, at the cost of increased variance in the results).
しかし、サンプリングが必要な場合、著者らは、サンプリングされた測定値を修正し、真の性能のより良い推定値を与える修正を提案しています（ただし、結果の分散が増加する代償として）。

Although unbiased metrics, to some extent, achieve the desired goal of obtaining ‘unbiased’ measures of a recommender’s performance, they suffer from some potential drawbacks.
偏りのない測定基準は、ある程度、推薦者の性能の「偏りのない」測定値を得るという望ましい目標を達成するものの、いくつかの潜在的な欠点に悩まされている。
One of these is that they may not be general enough to overcome all sources of bias, i.e.they are often designed to compensate for a specific kind of bias (e.g.the popularity bias in Steck (2011)).
例えば、Steck (2011)の人気バイアスなど、特定の種類のバイアスを補正するように設計されていることがあります。
Another is that their unbiasedness might be proven only if the data used satisfies some specific conditions (e.g.the assumptions of Steck (2010, 2011) and Lim et al.(2015) or the somewhat artificial recommendation scenario in Yang et al.(2018)).
また、使用するデータが特定の条件を満たす場合にのみ、その不偏性が証明される可能性がある（例えば、Steck (2010, 2011) や Lim et al (2015) の仮定、Yang et al (2018) のやや人工的な推薦シナリオなど）ことです。
Another drawback is that unbiased metrics might need additional data (e.g user gender and item features in Schnabel et al.(2016)).
もう一つの欠点は、不偏のメトリクスが追加のデータ（例えばSchnabel et al(2016)におけるユーザーの性別やアイテムの特徴）を必要とするかもしれないことです。
Finally, they might require computationally expensive calculations (e.g.to estimate propensities in Schnabel et al.(2016)).
最後に、計算量の多い計算（例えばSchnabel et al(2016)のプロペンシティの推定など）が必要な場合がある。

## Intervened datasets 介入したデータセット

The third solution to the problem of bias uses what we will call an intervention approach, in contrast with what we might call the regular approach (in which there is no intervention).
バイアスの問題に対する3つ目の解決策は、通常のアプローチ（介入しない）と呼ばれるものとは対照的に、介入アプローチと呼ばれるものを使用します。
In the latter, which is widely used in literature and which was explained earlier, the test set is typically generated by randomly sampling a portion of the available MNAR data, which gives rise to a biased RS evaluation.
先に説明した文献で広く使われている後者では、テストセットは通常、利用可能なMNARデータの一部をランダムにサンプリングして生成されるため、偏ったRS評価を生じさせることになります。
The former, instead, uses non-random sampling to produce a MAR-like test set, the intervened test set, which is supposedly less biased.
前者はその代わりに、非ランダムサンプリングを用いて、偏りが少ないとされるMARのようなテストセット、intervened test setを作成します。
The intervened test set is used in place of the regular (MNAR) test set to perform an unbiased RS evaluation.
介入されたテストセットは、通常の（MNAR）テストセットの代わりに使用され、偏りのないRS評価を行う。

The SKEW method by Liang et al.(2016a) samples user-item pairs in inverse proportion to the item’s popularity.
Liangら(2016a)によるSKEW法は、アイテムの人気度に反比例して、ユーザーとアイテムのペアをサンプリングする。
This generates an intervened test set which has roughly uniform exposure distribution across items, thus reducing the item popularity bias in the test set.
これにより、アイテム間の露出分布がほぼ均一な介入テストセットが生成され、テストセットにおけるアイテムの人気バイアスが軽減されます。
Liang and co-authors in Liang et al.(2016a) and Wang et al.(2018) and Bonner and Vasile (2018) use this technique for test set generation to evaluate causal approaches to recommendation.
Liang et al.(2016a) and Wang et al.(2018) and Bonner and Vasile(2018)のLiangと共著者は、推薦の因果的アプローチを評価するためのテストセット生成にこの技術を使用しています。
However, none of the three works that we have just cited either explain or verify empirically why SKEW should be effective as a debiasing technique.
しかし、今挙げた3つの著作は、いずれもSKEWがデビアス技術として有効である理由を実証的に説明・検証したものではありません。
In this paper, we fill the gap by providing such contributions (see Section 4).
本論文では、そのような貢献を提供することでギャップを埋める（セクション4参照）。
Also, because of the similarity with our own work on debiased RS evaluation, we use SKEW as a state-of-the-art strategy to compare against our own approach (WTD and WTD_H, see Section 3).
また、デビアスRS評価に関する我々の研究と類似しているため、SKEWを我々のアプローチ（WTDとWTD_H、セクション3参照）と比較するための最先端戦略として使用する。

Cremonesi et al.construct an intervened test set by removing ratings for the most popular items in the dataset from the MNAR test set, with the goal of mitigating the item popularity bias of the evaluation (2010).
Cremonesi et al.は、評価の項目人気バイアスを緩和する目的で、MNARテストセットからデータセット内で最も人気のある項目の評価を削除して介入テストセットを構築する(2010)。
In this way, a recommender’s quality is assessed on long-tail items only, while the recommendation of frequently-rated items is ignored.
このように、レコメンダーの品質はロングテール項目のみで評価され、頻繁に評価される項目の推奨は無視されるのです。
This is different from SKEW, which does not remove popular items but, rather, samples in inverse proportion to item popularity.
これは、人気のあるアイテムを削除するのではなく、アイテムの人気度に反比例してサンプリングするSKEWとは異なります。
Discarding all popular items may lead to specific insights but is generally too restrictive for a comprehensive evaluation.
人気のあるものをすべて捨てることで、具体的な知見が得られる場合もありますが、一般的には制限されすぎていて、総合的な評価にはなりません。
There is also a technical difficulty: given a specific dataset, it is not always clear what proportion of the items should be removed, leaving the evaluation quite arbitrary.
また、技術的な難しさもあります。特定のデータセットがある場合、どの程度の割合で項目を削除すべきかは必ずしも明確ではなく、評価はかなり恣意的になってしまいます。

Bellogin et al.also sample an MNAR dataset to try to overcome the item popularity bias in the evaluation of a recommender, by means of two approaches (2017).
BelloginらもMNARデータセットをサンプリングし、2つのアプローチによって、レコメンダーの評価におけるアイテム人気バイアスの克服を試みています（2017）。
Their first approach (which is a percentile-based approach) is a form of stratification, in which training and test ratings are sampled from a partition of the data.
彼らの最初のアプローチ（パーセンタイルベースのアプローチ）は、層別化の一形態で、訓練とテストの評価がデータのパーティションからサンプリングされるものである。
In practice, the set of items is partitioned into m bins, based on item popularity, and the ratings of the items belonging to a bin form a popularity stratum.
実際には、アイテムの集合をアイテムの人気度に基づいてm個のビンに分割し、ビンに属するアイテムの評価を人気度層とする。
Then, for each stratum: a training set and a test set are sampled (typically by means of a random split of the ratings available in the stratum); and a recommender model is trained on the training set and tested on the test set.
そして、各層ごとに、トレーニングセットとテストセットをサンプリングし（典型的には、その層で利用可能な評価のランダムな分割によって）、トレーニングセットでレコメンダーモデルを学習し、テストセットでテストします。
Results for the whole evaluation are obtained by averaging the recommender’s performance across the m strata.
評価全体の結果は、m個の層でレコメンダーの性能を平均化することで得られます。
One drawback of this methodology is the need to choose a value for the parameter m: it is not clear what m should be.
この方法の欠点は、パラメータmの値を選択する必要があることで、mがどうあるべきかは明確ではありません。
The fact that the whole evaluation is broken down into m experiments is another drawback.
また、全体の評価がm個の実験に分かれていることも難点です。
The consequence is that an evaluation of this kind assesses to what extent a recommender is good at recommending items within a given popularity stratum.
その結果、この種の評価は、あるレコメンダーが、与えられた人気層内のアイテムをどの程度推薦するのが得意かを評価することになる。
Bellogin et al.’s second approach (which they call Uniform Test Item Profiles) builds a test set with the same number of ratings for each item.
Belloginらの2番目のアプローチ（彼らはUniform Test Item Profilesと呼んでいる）は、各項目について同じ数の評価を持つテストセットを構築することである。
However, this approach is very sensitive to the steepness of the item popularity curve.
しかし、この方法は、アイテムの人気曲線の急峻さに非常に敏感である。
It may result in: generating quite small tests sets; and generating test sets where only a few popular items are included, therefore limiting the scope of the evaluation.
その結果、「非常に小さなテストセットが生成される」「少数の人気アイテムだけが含まれるテストセットが生成され、評価の対象が限定される」ことがあります。

# Our approach to Debiased offline evaluation of recommender systems 推薦システムのオフライン評価に対する我々のアプローチ

Designing an offline evaluation methodology which overcomes the bias problem in the data is crucial to obtaining reliable estimates of recommender performance.
レコメンダー性能の信頼できる推定値を得るためには、データのバイアス問題を克服するオフライン評価手法を設計することが重要です。
In Section 2.1, we have presented different solutions that can be found in the literature of the field.
セクション2.1では、この分野の文献に見られるさまざまな解決策を紹介しました。
In this section, we explain and evaluate our own contribution to debiasing, which we call WTD (and its variant WTD_H).
本節では、WTD（およびその変形であるWTD_H）と呼ぶ、デビアスへの独自の貢献について説明し、評価する。
WTD and WTD_H are intervention methods (Section 2.5), where the intervention is performed on MNAR data before using it for the evaluation.
WTD と WTD_H は介入法（2.5 節）であり、評価に使用する前に MNAR データに介入を行うものである。

In this section, we first analyse properties of MAR and MNAR data (Sections 3.1 and 3.2).
本節では、まず MAR と MNAR のデータの特性を分析する（3.1 節と 3.2 節）。
Subsequently, we use those properties to shape our WTD/WTD_H intervention, a sampling strategy in which sampling weights are calculated by considering the divergence between the distribution of users and items in the MNAR data and their corresponding target MAR distributions (Section 3.3).
これは、MNARデータにおけるユーザーとアイテムの分布と、それに対応するターゲットMARの分布との乖離を考慮してサンプリングウェイトを算出するサンプリング戦略である（3.3節）。

## Intervened test sets 介在するテストセット

To conduct unbiased evaluation from biased data, we generate and use intervened test sets in place of classical random heldout test sets.
偏ったデータから偏りのない評価を行うために、古典的なランダムホールドアウトテストセットの代わりに、介在テストセットを生成して使用します。
We begin by presenting this approach in general (Section 3.3.1), and then we present the specifics of our approach (Sections 3.3.2 and 3.3.3).
まず、このアプローチを一般的に紹介し（3.3.1項）、次に我々のアプローチの具体的な内容を紹介する（3.3.2項、3.3.3項）。

# Experiments 実験

The goal of the offline experiments presented in this section is to assess the ‘goodness’ of different ways of producing intervened test sets.
このセクションで紹介するオフライン実験の目的は、介在するテストセットを作成するさまざまな方法の「良さ」を評価することである。
The measure of ‘goodness’ is how much results obtained by evaluating a recommender on an intervened test set resemble the results we would obtain on an unbiased test set.
良さ」の指標は、**介入したテストセットでレコメンダーを評価した結果が、偏りのないテストセットで得られる結果にどれだけ似ているか**ということです。
We assess our solutions, i.e.WTD and WTD_H, and compare them to SKEW (Liang et al., 2016a) and to two baselines, FULL and REG.
我々は、我々のソリューション、すなわちWTDとWTD_Hを評価し、SKEW（Liang et al, 2016a）および2つのベースライン（FULLとREG）と比較する。
We consider SKEW, which we presented in Section 2.5, to be the state-of-the-art strategy that most closely relates to our approach; FULL and REG perform a non intervention and a random intervention (which, in practice, is equivalent to no intervention) on MNAR data, respectively.
FULLとREGはそれぞれMNARデータに対して非介入とランダム介入（実際には介入なしと同じ）を行うものである。

When deciding which intervention strategies to include in our investigation, we discarded some of the ones described in Section 2.5.Cremonesi et al.’s approach (2010) is one of them because it generates a test set devoid of ratings on the most popular items: it turns out that, by doing this, it is impossible to assess the quality of a recommender when recommending popular items, thus limiting the evaluation.
Cremonesi et al.のアプローチ（2010）は、最も人気のあるアイテムの評価を含まないテストセットを生成するため、そのうちの1つである。
We also do not include the two strategies of Bellogin et al., i.e.the percentile-based approach and the Uniform Test Item Profiles approach (2017).
また、Belloginらの2つの戦略、すなわちパーセンタイルベースのアプローチとUniform Test Item Profilesのアプローチ（2017年）は含んでいません。
The percentile-based approach trains a recommender and tests its performance on separate popularity segments of the item catalogue.
パーセンタイルベースのアプローチは、レコメンダーを訓練し、アイテムカタログの別々の人気セグメントでその性能をテストします。
Even though the quality of a recommender is inferred by averaging the performances across the segments, we argue that this approach still carries a similar limitation to Cremonesi et al.’s one (i.e.it compromises the representativeness of the whole experiment).
セグメント間のパフォーマンスを平均化することで、レコメンダーの品質を推測することができますが、この方法は、Cremonesiらの方法と同様の限界（つまり、実験全体の代表性を損なう）を持っていることを主張します。
The Uniform Test Item Profiles method also most likely discards ratings of some items (the least popular ones this time); and it may result in quite small test sets if the long-tail curve is very steep.
また、「統一テスト項目プロファイル」方式では、いくつかの項目（今回は最も人気のない項目）の評価を捨ててしまう可能性が高く、ロングテール曲線が非常に急な場合は、かなり小さなテストセットになる可能性があります。

## Datasets データセット

We use two publicly available ratings datasets: Webscope R3Footnote1 (WBR3) from the music domain (Marlin et al., 2007) and CoatShoppingFootnote2 (COAT) from the clothing domain (Schnabel et al., 2016).
一般に公開されている2つの評価データセットを使用する： 音楽領域のWebscope R3Footnote1（WBR3）（Marlin et al., 2007）と衣服領域のCoatShoppingFootnote2（COAT）（Schnabel et al., 2016）です。
Both of them are ideal for our purposes because they are composed of two parts, one having MAR properties (Dmar), and the other having MNAR properties (Dmnar).
どちらも、MAR特性を持つ部分（Dmar）とMNAR特性を持つ部分（Dmnar）の2つで構成されているため、今回の目的には最適です。
However, the two datasets have been collected in quite different recommender scenarios which, we argue, might influence our experimental results (see Section 5).
しかし、この2つのデータセットは、全く異なるレコメンダーシナリオで収集されたものであり、実験結果に影響を与える可能性があると我々は主張する（セクション5参照）。
Note that we did mention earlier (Section 2.5) that we know of one other MAR-like dataset, collected by the forced ratings approach, namely cm100k from the music domain (Cañamares and Castells, 2018), but we cannot use this in our experiments because it does not have any corresponding MNAR data.
なお、先ほど（セクション2.5）、強制評価アプローチによって収集された他のMAR的データセット、すなわち音楽領域のcm100k（Cañamares and Castells, 2018）を知っているが、対応するMNARデータがないため、これを実験に用いることはできないことを述べた。

COAT’s users are Amazon Mechanical Turkers who were asked (through a simple web-shop interface with facets and paging) firstly to find the coat they would have liked to buy the most and, afterwards, to freely rate 24 coats among the ones they had explored; those are the ratings that compose the Dmnar portion of the dataset.
COATのユーザーは、Amazon Mechanical Turkersで、（ファセットとページングを備えたシンプルなウェブショップのインターフェースを通じて）まず、最も買いたいと思うコートを探し、その後、探したコートの中から24着を自由に評価するよう求められた。
It is not clear for how long users were allowed to interact with the system.
ユーザーがどの程度の時間、システムに接することができたかは不明です。
The forced ratings approach described earlier was used to additionally collect the Dmar portion of the dataset.
Dmarのデータセットを追加で収集するために、前述の強制評価アプローチを使用しました。

For WBR3, data was collected over a 20 day window.
WBR3では、20日間にわたってデータを収集しました。
During this period, users used the LaunchCast Radio player, which gave them the freedom to rate songs (at any time and in any quantity) and receive personalised recommendations, and this produced the Dmnar portion of the dataset.
この期間、ユーザーはLaunchCast Radioプレーヤーを使用し、楽曲を（いつでも、どれだけでも）自由に評価し、個人的な推薦を受けることができ、これがデータセットのDmnar部分を生み出しています。
Again, additionally the Dmar portion was collected using the forced ratings approach.
ここでもまた、Dmarの部分は強制評価法を用いて収集されました。
It follows, for the reasons we gave earlier (see Section 2.5), that the Dmar portions of both WBR3 and COAT are almost but not completely unbiased.
先に述べた理由（2.5節参照）から、WBR3とCOATのDmarの部分は、ほぼ不偏であるが完全ではないことがわかる。

For both datasets, ratings are on a 1 to 5 scale and we consider an item as relevant to a user if the item has a rating above 3, non-relevant otherwise.
両データセットとも、**評価は1～5段階であり、項目が3以上の場合、ユーザーにとって関連性があるとみなし、それ以外の場合は非関連**であるとみなします。

For each dataset, we applied a preprocessing step to ensure that both Dmar and Dmnar have a common user-item space U × I: specifically, we keep those users and items that belong to the intersection of the two portions.
各データセットについて、DmarとDmnarの両方が共通のユーザー・アイテム空間U×Iを持つようにする前処理ステップを適用した：具体的には、2つの部分の交点に属するユーザーとアイテムを残すようにした。
Table 1 gives statistics of the final resulting datasets that we used in the experiments.
表1は、実験に使用した最終的な結果のデータセットの統計です。

## Methodology 方法論

In our experiments, we randomly split Dmnar in each dataset into a training set Dtr and a heldout set Dhe with proportions 60%-40% respectively.
実験では、各データセットのDmnarを、トレーニングセットDtrとホールドアウトセットDheにそれぞれ60%〜40%の割合でランダムに分割しました。
Since the split is random, MNAR distributions are preserved.
分割はランダムに行われるため、MNARの分布は保たれます。
Dhe is what one would use as a traditional test set.
Dheは、従来のテストセットとして使用されていたものです。
But, in our case, we use Dhe as the sampling space: we sample it to obtain different intervened test sets DS.
しかし、我々の場合、Dheをサンプリング空間として使用し、それをサンプリングして異なる介在テストセットDSを得る。
For each sampling strategy (REG, SKEW, WTD, WTD_H, explained in Section 4.3), we generate 10 different intervened test sets, each of which is obtained by sampling a portion ρp from Dhe.
各サンプリング戦略（REG、SKEW、WTD、WTD_H、セクション4.3で説明）に対して、Dheから一部ρpをサンプリングして得た10種類の介在テストセットをそれぞれ生成する。
The parameter ρp takes all the values in {0.1,0.2,..,1} and represents the size of DS with respect to the size of Dhe (e.g.ρp = 0.5 means that |DS| = 0.5|Dhe|).
DS
We can view ρp as the parameter that guides the strength of the debiasing action on Dhe: the smaller is ρp, the smaller but more debiased is DS; the bigger is ρp, the bigger and less debiased is DS, i.e.because it is more similar to Dhe.
ρpは、Dheに対する蕩尽作用の強さを示すパラメータとみなすことができる。ρpが小さいほど、DSは小さくても蕩尽され、ρpが大きいほど、DSは大きくても蕩尽されない、つまりDheとより似ているから蕩尽される。
In Section 5, we will see the impact of different ρp values on the results.
第5節では、ρpの値の違いによる結果への影響について見ていく。
Hence, the experiments reported here extend the ones in Carraro and Bridge (2020), where we only report results for ρp = 0.5.
したがって、ここで報告した実験は、Carraro and Bridge (2020)のものを拡張したものであり、ρp = 0.5の結果のみを報告しているものである。

We also randomly split Dmar into three, i.e.Dw, Dval and Dgt with proportions 15%-15%-70% respectively.
また、DmarをDw、Dval、Dgtの3つにランダムに分割し、それぞれ15%-15%-70%の割合で配置しました。
Since the split is random, MAR distributions are preserved.
分割はランダムに行われるため、MARの分布は保たれます。
Dw is used to calculate the weights for WTD (see Section 4.3 for details of the calculation).
Dwは、WTDの重みの計算に使用される（計算の詳細は4.3節参照）。
We use Dval as the validation set to optimize recommender system hyperparameters (Section 4.4).
Dvalを検証セットとして、レコメンダーシステムのハイパーパラメーターを最適化する（4.4節）。
(In reality, the ratings one would use to optimize hyperparameters would either be a portion of Dtr or a portion of an intervened test set produced from Dhe.
(実際には、ハイパーパラメータを最適化するために使用する評価は、Dtrの一部か、Dheから生成されたテストセットを介在させるかのどちらかである。
We decided it was better in the experiments that we report here to minimise the effect of hyperparameter selection on our results.
ここで報告する実験では、ハイパーパラメータの選択が結果に与える影響を最小限にする方が良いと判断しました。
Hence, we selected hyperparameter values using ‘unbiased’ data, Dval).
そこで、「不偏」のデータを用いてハイパーパラメータ値を選択した（Dval）。

We use Dgt as an unbiased test set.
Dgtを不偏のテストセットとして使用します。
In other words, the performance of a given recommender on Dgt can be considered to be its “true”, unbiased performance (the ground-truth).
つまり、Dgtに対する推薦者の性能は、その推薦者の「真の」不偏性能（ground-truth）であると考えることができます。
We want the performance of a recommender on an intervened test set to be close to its performance on this unbiased test set.
介在するテストセットでの推薦者の性能は、この不偏のテストセットでの性能に近いものを求めます。
The best intervention strategy is the one that produces test sets where performance most closely resembles performance on Dgt.
最適な介入戦略は、性能がDgtの性能に最も近いテストセットを生成するものである。

We train the five recommender systems presented in Section 4.4 using ratings in Dtr.
Dtrの評価を用いて、4.4節で紹介した5つのレコメンダーシステムを学習させる。
Each recommender produces a ranked list of recommendations which are tested on the unbiased test set Dgt and the intervened test sets.
各推薦者は、非バイアスのテストセットDgtと介在するテストセットでテストされる推奨のランク付けされたリストを作成します。
We have computed Precision, Recall, MAP and NDCG on the top-10 recommendations.
トップ10のレコメンデーションについて、Precision、Recall、MAP、NDCGを算出した。
Results are averaged over 10 runs with different random splits.
結果は、異なるランダム分割で10回実行した平均値です。

## Sampling strategies for the intervention 介入のためのサンプリング戦略

We formally present here the sampling strategies that we use to produce the intervened test sets in our experiments.Footnote3 Each strategy samples an intervened test set DS from Dhe.
各戦略は、Dheから介在テストセットDSをサンプリングする。
For each strategy we give the corresponding probability sampling distribution, i.e.HCode PS(S|u,i)
各戦略に対応する確率サンプリング分布、すなわちHCode PS(S|u,i) を与える。

.
.
In addition to SKEW, WTD and WTD_H, we also employ two baselines.
SKEW、WTD、WTD_H に加えて、2 つのベースラインを採用しています。
Regular (REG) is a random sample from Dhe, corresponding to an intervention that does not try to compensate for bias.
正規（REG）はDheから無作為に抽出したサンプルで、バイアスを補おうとしない介入に対応する。
FULL represents the test set in the classic evaluation, where the test set is Dhe (therefore no intervention).
FULLは古典的な評価におけるテストセットを表しており、テストセットはDhe（したがって介入なし）である。

# Results 結果

We report the results of our experiments in Figs.3 and 4 and Tables 2 and 3.
実験結果を図3、図4、表2、表3に報告します。

To analyse the difference between the various sampling strategies, we plot the distribution of the rating values of each of the intervened test sets and we compare them with the unbiased test set Dgt (similarly to the analysis in Marlin et al.(2007)).
**様々なサンプリング戦略の違いを分析するために、介在する各テストセットの評価値の分布をプロット**し、不偏のテストセットDgtと比較する（Marlin et al(2007)の分析と同様である）。

Firstly, Fig.3 confirms the difference between unbiased (i.e.Dgt) and biased distributions (i.e.FULL and REG) for both datasets.
まず、Fig.3では、両データセットにおいて、非バイアス分布（Dgt）とバイアス分布（FULLとREG）の違いを確認することができます。
In general, unbiased distributions show a much higher proportion of low ratings than high ratings, confirming that in biased datasets users tend to rate items that they like (Marlin et al., 2007).
一般に、偏りのない分布(=真のY)では、高評価よりも低評価の割合が非常に高く、**偏ったデータセットでは、ユーザーは自分が気に入ったアイテムを評価する傾向がある**ことが確認された（Marlin et al, 2007）。
This difference is less evident in COAT than WBR3 and we argue that this is due to the more artificial conditions under which COAT’s MNAR portion was collected (Schnabel et al., 2016) compared with the MNAR portion of WBR3.
この違いは、WBR3よりもCOATの方が顕著ではなく、COATのMNAR部分がWBR3のMNAR部分と比較してより人工的な条件で収集されたため（Schnabel et al, 2016）であると主張しています。
WBR3’s users experienced a standard recommender scenario (see Section 4.1) whereas COAT’s users were not influenced by a recommender.
WBR3のユーザーは標準的なレコメンダーシナリオ（4.1節参照）を経験したのに対し，**COATのユーザはレコメンダーの影響を受けていない**．
The COAT users, being Mechanical Turkers, are mere executors of a task and therefore less likely to care about their experience of using the system; therefore, we argue that COAT is more randomized and accordingly less biased (i.e.more similar to an unbiased dataset).
COATの利用者はメカニカルターカーであり、単なるタスクの実行者であるため、システムを利用した経験を気にする可能性は低い。したがって、**COATはよりランダムであり、それゆえより偏りのない（すなわち、より不偏のデータセットに近い）データである**と主張されるのです。
To confirm those findings, we observe values for FULL and REG in Table 2 where we report Kullback-Leibler (KL) divergence scores between the intervened sets and the ground truth for both datasets.
これらの結果を確認するため、表2のFULLとREGの値を観察し、両データセットの介入セットとグランドトゥルースの間のKL（Kullback-Leibler）ダイバージェンススコアを報告しています。
This KL divergence is much greater for WBR3 (approximately 0.4) than it is for COAT (approximately 0.07).
このKLダイバージェンスは、COAT（約0.07）よりもWBR3（約0.4）の方がはるかに大きい。(COATのMNARデータはMARデータに比較的近い.)

Compared with FULL and REG, the distributions of rating values in the intervened test sets (i.e.SKEW, WTD and WTD_H) are closer to the distribution in the unbiased ground truth for both datasets (although only to a limited extent): this can be observed in both Fig.3 and Table 2.
FULLとREGに比べ、**介入テストセット（SKEW、WTD、WTD_H）の評価値の分布は、どちらのデータセットでも（限られた範囲ではあるが）不偏のグランドトゥルースの分布に近くなっている**。これは図3と表2の両方で観察できる。
Such results show the first evidence that intervention might be a good solution to unbiased evaluation.
このような結果は、**介入が公平な評価のための良い解決策になるかもしれないという最初の証拠**を示しています。
Indeed, the results we present in detail later (i.e.Table 3 and Fig.4) confirm that the relatively small increase in similarity between the SKEW, WTD and WTD_H test sets and the unbiased ground truth in terms of posteriors leads to a greater and much more appreciable similarity in the accuracy of the recommendations.
実際、後で詳しく紹介する結果（表 3 と図 4）では、**SKEW、WTD、WTD_H テストセットと不偏のグランドトゥルースの間の事後分布の類似度が比較的小さくなることで、推薦の精度がより高く評価できる類似度になる**ことが確認されました。

In Table 3, for each recommender, we show its ground-truth Recall@10 performance on the unbiased test set Dgt and its relative performance (in terms of percentage difference) on the baselines and intervened test sets with respect to this ground-truth.
表3では、各レコメンダーについて、バイアスのかかっていないテストセットDgtにおけるグランドトゥルースのRecall@10性能と、このグランドトゥルースに対するベースラインと介在するテストセットでの相対性能（差分パーセント）を示している。(2020の論文におけるtable 2と同じ...!)
For each of REG, SKEW, WTD and WTD_H, we show the best performance among the ones obtained in the 10 different test sets (one for each different ρp) and we show in brackets the test set size ρp for which this best performance is achieved.
REG、SKEW、WTD、WTD_Hのそれぞれについて、10種類のテストセット（異なるρpごとに1つずつ）で得られたものの中で最も優れた性能を示し、この最高の性能が達成されたテストセットサイズρpを括弧内に示します。
Results for Precision, NDCG and MAP are omitted because the percentage differences have a very similar trend to the Recall ones.
Precision、NDCG、MAPの結果は、差の割合がRecallと非常に似た傾向であるため、省略した。
The statistical significance of the results is assessed by performing a pairwise comparison test between the performance of each recommender on the five different test sets, i.e.the baseline sets (FULL, REG) and the intervened sets (SKEW, WTD and WTD_H).
結果の統計的有意性は、5つの異なるテストセット、すなわちベースラインセット（FULL、REG）と介入セット（SKEW、WTD、WTD_H）に対する各推薦機の性能間の一対比較テストを行うことで評価される。
For such tests, we use a two-tailed Wilcoxon signed rank testFootnote5 with p < 0.05, and the results are reported in Table 4.
このような検定には、p<0.05の両側ウィルコクソン符号付き順位検定Footnote5を用い、結果は表4に報告されている。

Results on WBR3 show that WTD and WTD_H outperform SKEW only for the MF recommender (where all differences are statistically significant).
WBR3での結果は、MFレコメンダーにおいてのみ、WTDとWTD_HがSKEWを上回った（すべての差が統計的に有意である場合）。
This is however a good result if we consider that WTD and WTD_H are best at debiasing the evaluation of one of the most successful and widely-used recommenders in the literature (Koren et al., 2009).
しかし、WTDとWTD_Hが、文献上最も成功し、広く使われている推薦者の1つ(**MFの事...!**)（Koren et al, 2009）の評価を落とすのに最適であることを考えれば、これは良い結果であると言えます。
SKEW is superior to WTD and WTD_H for the PosPop and IB_KNN recommenders (with statistically significant differences).
PosPopとIB_KNNのレコメンダーでは、SKEWがWTDとWTD_Hよりも優れている（統計的に有意な差がある）。
For the UB_KNN recommender, WTD_H and SKEW are equally good (their performances are not statistically significantly different) and superior to WTD; for the AvgRating recommender, all three are equally good because performances are not statistically significantly different from each other.
UB_KNNレコメンダーでは、WTD_HとSKEWが同等（性能に統計的有意差がない）でWTDより優れており、AvgRatingレコメンダーでは、性能に統計的有意差がないため3つとも同等であった。
The superiority of SKEW for PosPop is somehow expected because SKEW is an intervention that is specific to popularity-bias; its superiority for UB_KNN can be explained by a similar reason, i.e.UB_KNN has also been proved to be a recomender with a popularity-bias (Cañamares and Castells, 2017).
PosPopに対するSKEWの優位性は，SKEWが人気バイアスに特化した介入であることから何となく予想される。UB_KNNに対する優位性は，同様の理由，すなわち，UB_KNNも人気バイアスによるリコメンダであることが証明されている（Cañamares and Castells, 2017）ことから説明可能である．

We also observe that SKEW obtains its best performances on intervened sets that are smaller than the ones of WTD and WTD_H.
また、SKEWは、WTDやWTD_Hよりも小さい介入データ集合(=サンプリングのサイズが小さい状況で...!)で最高の性能を発揮することが確認された。
However, this fact could raise questions about the reliability of SKEW’s results due to discarding the majority of the available test data.
しかし、この事実は、入手可能なテストデータの大半を破棄したことによるSKEWの結果の信頼性に疑問を抱かせる可能性があります。

Comparing only WTD and WTD_H performances, we find that in general WTD is better than WTD_H, with the only exception being for the AvgRating recommender (where their performances are not statistically significantly different) and UB_KNN (where WTD_H is better than WTD).
WTDとWTD_Hの性能のみを比較すると、一般的にWTDがWTD_Hよりも優れていることがわかりますが、唯一の例外はAvgRatingレコメンダー（両者の性能に統計的な有意差はない）とUB_KNN（WTD_HがWTDよりも優れている）でした。

The results for COAT in the lower half of Table 3 show that WTD and WTD_H are equally good because performances are not statistically significantly different from each other.
表3の下半分のCOATの結果は、WTDとWTD_Hの性能が統計的に有意な差がないため、同等の性能であることを示しています。
Also, they more closely approximate the ground truth for the personalised recommenders but not for the non-personalised recommenders.
**また、パーソナライズド・レコメンダーでは、より真実の状態に近くなっていますが、ノンパーソナライズド・レコメンダーでは、そうではありません。**
Indeed, their performances are not statistically significantly different to the one of SKEW for PosPop and the ones of REG and SKEW for AvgRating.
実際、PosPopではSKEW、AvgRatingではREGとSKEWの性能に統計的に有意な差はない。

Finally, in both datasets, baselines FULL and REG are very far from the ground-truth, showing that ‘intelligent’ intervention strategies provide an effective debiasing technique in offline evaluations.
最後に、両データセットにおいて、**ベースラインFULLとREGはグランドトゥルースから非常に離れており**、「インテリジェント」な介入戦略がオフライン評価において有効なデビアス手法を提供することを示している。
Indeed, SKEW, WTD, WTD_H achieve statistically significantly different performances with respect to FULL and REG with the exception of SKEW for MF on COAT.
実際，SKEW，WTD，WTD_Hは，COAT上のMFではSKEWを除いて，FULLとREGに関して統計的に有意に異なる性能を達成した．
In general, FULL and REG have similar results, regardless of the fact that the best performances of REG is generally achieved on a test set which is much smaller than FULL (except for the one of AvgRating in WBR3).
一般に，FULLとREGは，REGの最高性能はFULLよりはるかに小さいテストセットで達成されるという事実にもかかわらず，同様の結果を示している（WBR3のAvgRatingのものを除く）．
This means that what matters is the strategy that performs the sampling, rather than the sampling itself.
つまり、重要なのはサンプリングそのものではなく、サンプリングを行う戦略なのです。

Figure 4 reports an additional investigation on the results of Table 3.
図4は、表3の結果に対する追加調査の報告である。(2020年の論文のtable 3, table 4に当たる.)
An offline evaluation typically ranks recommender algorithms from best to worst.
オフライン評価では、通常、レコメンダーアルゴリズムをベストからワーストにランク付けします。
This helps to narrow the number of different recommender algorithms that needs to be evaluated in costly user trials and online experiments.
これにより、コストのかかるユーザートライアルやオンライン実験で評価する必要のある、さまざまなレコメンダーアルゴリズムの数を絞ることができます。
In our case then, it is important that performance estimates on intervened test sets, not only get close to the ground truth performance, but also rank different recommenders in the same way they would be ranked by performance estimates on the unbiased test set.
この場合、介在テストセットでの性能推定が、真実の性能に近いだけでなく、公平なテストセットでの性能推定によってランク付けされるのと同じように、異なるレコメンダーをランク付けすることが重要である。

Before seeing whether the ranking of the recommenders on intervened sets corresponds to their ranking on the ground truth, we wanted to make sure that the ground truth ranking was reliable.
介入した集合における推薦者の順位が、ground-truthにおける順位と一致するかどうかを見る前に、**ground-truthの順位が信頼できるかどうかを確認したかった**のです。
Thus, we first computed statistical significance tests on the ground truth ranking.
そこで、まず、groud-truthのランキングについて統計的有意差検定を行った。
The statistical significance of the results is assessed by performing a pairwise comparison test between the performances of the recommenders on the unbiased test set Dgt, again using the two-tailed Wilcoxon signed rank test described earlier.
結果の統計的有意性は、偏りのないテストセットDgtにおける推薦者の性能の間で、再び前述の両側Wilcoxon符号付き順位検定を用いて一対比較検定を行うことで評価される。
Results of these tests are reported in Table 5.
これらのテストの結果は、表5に報告されている。
We found that, for WBR3, recommender performances are statistically significantly different from each other, except for the pair UB_KNN & IB_KNN.
その結果、WBR3では、UB_KNNとIB_KNNのペアを除き、推薦者の性能は統計的に有意に異なることがわかりました。
Unfortunately, for COAT, no recommender performance is statistically significantly different from any other, except for the pair MF & IB_KNN.
**残念ながら、COATでは、MFとIB_KNNのペアを除いて、どのレコメンダーの性能も他と統計的に有意な差はありませんでした。**
We argue that this is due to the small size of the COAT training set.
これは、COATのトレーニングセットのサイズが小さいためであると主張しています。
This means that for COAT there is no point in comparing the rankings produced by the different intervened test sets, because all recommenders are roughly equivalent according to the ground truth test set.
つまり**COATでは、介入したテストセットの違いによるランキングの比較は意味がなく、すべてのレコメンダーは、グランドトゥルーステストセットによればほぼ同等であることがわかります。**

We use Kendall’s concordance coefficient (τ) to compare the ground truth recommender ranking obtained on the unbiased test set with the ones produced by the different interventions.
Kendallの一致係数(τ)を用いて、偏りのないテストセットで得られたground-truthの推薦者ランキングと、異なる介入によって生成されたランキングを比較する。
For the reasons above, Fig.4 reports the results for WBR3 only: for each of the intervention approaches we show concordance coefficients obtained in their 10 different intervened test sets.
**図4は，上記の理由から，WBR3のみの結果で**ある。それぞれの介入アプローチについて，10種類の介入テストセットで得られたコンコーダンス係数を示している。
The figure shows that the ‘intelligent’ interventions are superior to FULL and REG, i.e.SKEW, WTD and WTD_H have values no smaller than the ones of REG (with the only exception of WTD & WTD_H when ρp = 0.1).
すなわち，**SKEW，WTD，WTD_H は REG の値より小さくない**（ρp = 0.1 のときの WTD & WTD_H のみが例外）．

In more detail, FULL, REG and SKEW have constant τ values (0.6, 0.6 and 0.8, respectively), with SKEW being the best of the three.
より詳細には、FULL、REG、SKEWはそれぞれ一定のτ値（0.6、0.6、0.8）を持ち、SKEWは3つの中で最も優れています。
WTD and WTD_H have different values, depending on the size of their test sets.
WTDとWTD_Hは、そのテストセットの大きさによって、異なる値を持つ。
In general, both are superior to SKEW from ρp = 0.9 down to ρp = 0.6, achieving perfect correlation (τ = 1) when ρp = 0.8 (WTD_H), ρp = 0.7 (WTD & WTD_H) and ρp = 0.6 (WTD).
一般に、ρp = 0.9 からρp = 0.6 までは、両者は SKEW よりも優れており、ρp = 0.8 (WTD_H), ρp = 0.7 (WTD & WTD_H), ρp = 0.6 (WTD) では完全相関（τ = 1）を達成しました。
SKEW, WTD and WTD_H have τ = 0.8 for ρp = 0.6, but SKEW is superior to all the other strategies from ρp = 0.1 up to ρp = 0.4 inclusive.
SKEW，WTD，WTD_Hはρp=0.6でτ=0.8となるが，**SKEWはρp=0.1からρp=0.4まで含めて他のすべての戦略よりも優れている．**
We would argue that, in general, the results obtained by our debiasing strategies are more valuable than those of SKEW and REG because they are superior when sampling most of the data available for testing (except for when ρp = 0.9, where SKEW, WTD and WTD_H achieve the same correlation value).
一般的に、我々のデビアス戦略によって得られた結果は、テストに利用可能なデータのほとんどをサンプリングした場合に優れているため、SKEW や REG の結果よりも価値があると言えるでしょう（ただし、ρp = 0.9 の場合は SKEW、WTD、WTD_H が同じ相関値を達成しています）。
Indeed, ρp values smaller than 0.5 can result in intervened test sets that are too small to give reliable results.
実際、**ρpの値が0.5より小さいと、介入テストセットが小さすぎて信頼できる結果が得られない**ことがあります。
At the same time, ρp values greater than 0.8 can result in intervened test sets that are too similar to a biased test set to provide substantially different results with respect to a biased evaluation.
同時に、**0.8より大きいρp値は**、偏った評価に関して実質的に異なる結果を提供するために、**偏ったテストセットにあまりにも類似している介在テストセットをもたらしうる**.

# Conclusions 結論

In this paper, we presented WTD and WTD_H, our new sampling strategies that generate intervened test sets with MAR-like properties from MNAR data.
本論文では、MNARデータからMAR的な性質を持つ介在型テストセットを生成する新しいサンプリング戦略であるWTDとWTD_Hを発表した。
These intervened test sets are more suitable for estimating how a recommender would perform on unbiased test data.
これらの介在するテストセットは、偏りのないテストデータでレコメンダーがどのように機能するかを推定するのに適しています。
One of the sampling strategies, WTD, requires that some MAR-like data be available since it approximates posterior probabilities calculated from that data.
サンプリング戦略の1つであるWTDは、そのデータから計算される事後確率を近似するため、MARのようなデータがあることが必要です。
The other strategy, WTD_H, approximates the probabilities that we expect MAR data to exhibit.
もう一つのストラテジーであるWTD_Hは、MARデータが示すと予想される確率を近似するものです。

## Findings Findings

The paper assesses the effectiveness of these two strategies and it assesses, for the first time, the effectiveness of an existing intervention strategy from the literature, namely SKEW, which samples from MNAR data in inverse proportion to item popularity.
本論文では、これら2つの戦略の有効性を評価するとともに、文献にある既存の介入戦略、すなわち、アイテムの人気度に反比例してMNARデータからサンプリングするSKEWの有効性を初めて評価した。
With the use of (essentially) unbiased test sets as ground-truth, we showed these three sampling approaches to be successful in mitigating the biases found in a classical random test set.
基本的に偏りのないテストセットを真実として使用することで、これら3つのサンプリングアプローチが、古典的なランダムテストセットに見られる偏りを軽減することに成功することを示しました。
In general, we found SKEW to be particularly good at reducing the bias for well-known recommenders that themselves suffer from a popularity-bias (i.e.PosPop and both nearest-neighbour recommenders (Cremonesi et al., 2010)).
一般的に、SKEW は、それ自体が人気バイアスに苦しむ有名な推薦者（PosPop や両最近隣接推薦者 (Cremonesi et al., 2010) など）に対するバイアスを軽減することに特に優れていることがわかりました。
Item popularity-bias is the kind of bias for which SKEW was designed.
アイテム人気バイアスは、SKEWが設計したバイアスの一種である。
But our new strategies are the most robust (even if sometimes by a limited extent) on various key recommenders (MF on WBR3 and all the personalized recommenders on COAT) since they most closely approximate their unbiased ground-truth performances.
しかし、我々の新しい戦略は、様々な主要な推薦者（WBR3のMFとCOATの全てのパーソナライズド推薦者）に対して最も頑健であり（時には限られた範囲であっても）、その理由は不偏のグランドトゥルースの性能に最も近いからである。
The WTD strategy requires MAR data, which is rarely available, but we found that WTD_H, which uses a hypothesized MAR distribution, does work well, so MAR data is not necessary.
WTD戦略ではMARデータが必要で、その入手は稀ですが、仮説のMAR分布を使うWTD_Hはうまくいくことがわかったので、MARデータは必要ありません。

Our approach brings several benefits.
私たちのアプローチは、いくつかのメリットをもたらします。
First of all, it enjoys low overheads.
まず、オーバーヘッドが少ないことが挙げられます。

- Its design is simple and easy to implement and it does not require any learning phase for the weights, contrary to some unbiased estimators which might require expensive learning (e.g. Schnabel et al. (2016), where propensities are found via logistic regression). その設計はシンプルで実装が容易であり，高価な学習を必要とする可能性のあるいくつかの不偏推定器（例えば，Schnabel et al(2016), where propensities are found via logistic regression）に反して，重みに対する学習段階を必要としない．

- Moreover, intervention reduces the computational costs of testing a recommender because it generates smaller test sets. さらに、介入はより小さなテストセットを生成するため、レコメンダーのテストにかかる計算コストを削減することができます。

Another advantage of our approach is that it has high generality.
また、本アプローチのもう一つの利点は、高い汎用性を持っていることです。

- It works for both implicit and explicit datasets because it is independent of the interaction values (e.g. ratings) in the dataset. データセット中の相互作用値（例えば評価）に依存しないため、暗黙的なデータセットでも明示的なデータセットでも機能します。

- Despite the fact that WTD and WTD_H are close to SKEW on some recommenders, our way of calculating weights is a better motivated heuristic than the one of SKEW and, unlike SKEW, it is not tailored to item popularity-bias. いくつかのレコメンダーでは、WTD と WTD_H が SKEW に近いという事実があるが、我々の重みの計算方法は、SKEW のものより動機付けされたヒューリスティックであり、SKEW とは異なり、アイテムの人気バイアスに合わせているわけでもない。

- Our approach can be extended to training a recommender, without any modification. Training a recommender on an intervened training set, instead of on a classical biased training set, might improve the recommender’s model and therefore boost prediction or top-n recommendation performances. 本アプローチは、そのままレコメンダーのトレーニングに拡張することが可能です。 従来の偏った訓練セットではなく、介入した訓練セットでレコメンダーを訓練することで、レコメンダーのモデルを改善し、予測やトップNレコメンデーションの性能を向上させることができるかもしれません。

- Intervened data can be used to train existing recommender systems and to test recommender systems using existing metrics. Debiased training and testing hence become widely applicable without designing special models and special metrics. This feature is particularly desirable when benchmarking new recommender approaches with respect to existing ones. 介入されたデータは、既存のレコメンダーシステムのトレーニングや、既存のメトリクスを用いたレコメンダーシステムのテストに使用することができます。 そのため、特別なモデルや指標を設計することなく、偏ったトレーニングやテストが広く適用できるようになります。 この特徴は、新しいレコメンダーアプローチを既存のレコメンダーアプローチと比較してベンチマークする場合に特に望ましい。

## Limitations of our study and future works 本研究の限界と今後の課題

Our work focuses on helping researchers to build reliable offline experiments.
私たちの仕事は、研究者が信頼性の高いオフライン実験を構築するための支援に重点を置いています。
A future step to reinforce the validity of our debiasing strategies is to run more experiments with different datasets, for example datasets that are larger or ones that come from other recommendation domains.
今後の課題として、より大きなデータセットや他の推薦領域からのデータセットなど、異なるデータセットを用いてより多くの実験を行うことで、我々のデビアス戦略の有効性を強化する。
However, even so, it is well-known that online experiments, such as A/B tests and user trials, are essential to give authentic insights into what has been investigated offline.
**しかし、そうはいっても、オフラインで調査したものに本物のインサイトを与えるためには、A/Bテストやユーザートライアルなどのオンライン実験が不可欠であることはよく知られていること**です。
Therefore, our studies should be extended with online experiments.
したがって、我々の研究はオンライン実験によって拡張されるべきです。
This is work for the future.
これは、未来に向けた仕事です。

In Section 2.3 we described how to collect unbiased-like datasets by using the forced ratings approach.
セクション2.3では、強制視聴率法を用いて偏りのないデータセットを収集する方法について説明した。
We also highlighted that those datasets are usually small and that this collection approach can only work in specific domains.
また、それらのデータセットは通常小規模であり、この収集方法は特定のドメインでしか機能しないことを強調しました。
Despite our work on debiasing data and other works in the literature too, we argue there is still the need for more unbiased data, allowing for more experiments on the testing (and, eventually, the training) of RSs.
私たちが行ったデータの偏り解消や他の文献での研究にもかかわらず、**私たちは、RSのテスト（そして最終的にはトレーニング）に関するより多くの実験を可能にする、より偏りのないデータが必要であると主張しています**。
When evaluating an RS, bigger unbiased datasets would give a more grounded reference of unbiased performance.
RSを評価する場合、より大きな不偏のデータセットがあれば、不偏の性能についてより根拠のあるリファレンスが得られるでしょう。
Alternatives to the forced ratings approach that are applicable across more domains and that generate bigger unbiased datasets might be investigated too.
より多くのドメインに適用でき、より大きな偏りのないデータセットを生成する、強制評価アプローチの代替案も研究されるかもしれません。
Additionally, similar approaches to collecting unbiased implicit datasets might also be useful.
さらに、偏りのない暗黙のデータセットを収集するための同様のアプローチも有用であろう。

Given the availability of a dataset collected by the forced ratings approach, there is still room for discussion to what extent this dataset can be considered an unbiased ground-truth for an RS evaluation.
**強制評価手法で収集されたデータセットが、どの程度RS評価のための不偏の根拠となりうるかについては、まだ議論の余地があるようです。**
As we have emphasized in this paper (see Section 2.3 in particular), such a dataset might still carry some bias which might affect findings of studies like ours.
本稿で強調してきたように（特に2.3節参照）、このようなデータセットには、我々のような研究の結果に影響を与える可能性のある**バイアスが残っている可能性があります。**
There is bias, for example, when a user rates an item she already knows (Loepp et al., 2018) or when items are rated in sequence.
例えば、ユーザーが既に知っている項目を評価する場合（Loepp et al, 2018）や、項目が順番に評価される場合など、偏りがある。
Even if we were able to remove many (if not all) of the effects of confounders from a dataset collection process in a real-world scenario, the rFesulting unbiased dataset still might not display a uniform rating probability in practice.
仮に、データ収集の過程で交絡因子の影響の多くを取り除くことができたとしても、実際にはrFesulting unbiased datasetは均一な評価確率を示さないかもしれません。
For these reasons, we believe further research on bias and its intrinsic mechanisms in an RS scenario need to be properly addressed in the future.
これらの理由から、RSシナリオにおけるバイアスとその本質的なメカニズムについて、今後さらに適切に研究する必要があると考えています。

Finally, another aim for the future is to investigate other ways of calculating the weights for WTD.
最後に、**WTDのウェイトを計算する他の方法を検討することも**、今後の目的のひとつです。
An alternative might be using techniques developed for causal inference, e.g.Cortes et al.(2008, 2010).
また、Cortes et al. (2008, 2010) のような因果関係推論のために開発された技術を利用することも考えられる。
Also, given the generality of our approach, it would be interesting to assess the effectiveness of WTD and WTD_H at debiasing implicit datasets, to complement the investigation performed in this paper.
また、本アプローチの一般性を考慮すると、本論文で行った調査を補完するために、暗黙のデータセットをデビアスするWTDとWTD_Hの有効性を評価することは興味深いことである。
