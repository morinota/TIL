## 0.1. link リンク

- https://dl.acm.org/doi/10.1145/3341105.3375759 https://dl.acm.org/doi/10.1145/3341105.3375759

## 0.2. title タイトル

Debiased offline evaluation of recommender systems: a weighted-sampling approach
推薦システムの偏ったオフライン評価：加重サンプリングアプローチ

## 0.3. abstract アブストラクト

Offline evaluation of recommender systems mostly relies on historical data, which is often biased by many confounders.
レコメンダーシステムのオフライン評価は、多くの場合、多くの**交絡因子**によって偏りがある過去のデータに依存しています。
In such data, user-item interactions are Missing Not At Random (MNAR).
このようなデータでは、**ユーザとアイテムの interactions はMNAR（Missing Not At Random）**である。
Measures of recommender system performance on MNAR test data are unlikely to be reliable indicators of real-world performance unless something is done to mitigate the bias.
**MNARテストデータによる**推薦システムの性能測定は、バイアスを軽減するための工夫がない限り、実世界の性能の信頼できる指標にはなりにくい。(**やっぱり学習ではなく評価の話なのかな...!!**)
One way that researchers try to obtain less biased offline evaluation is by designing new supposedly unbiased performance estimators for use on MNAR test data.
研究者がより偏りの少ないオフライン評価を得ようとする一つの方法は、**MNARテストデータで使用するための、新しい不偏の性能推定器**を設計することです。
We investigate an alternative solution, a sampling approach.
私たちは、**別の解決策であるサンプリング・アプローチ**について調査しています。
The general idea is to use a sampling strategy on MNAR data to generate an intervened test set with less bias --- one in which interactions are Missing At Random (MAR) or, at least, one that is more MAR-like.
一般的なアイデアは、MNARデータのサンプリング戦略を用いて、よりバイアスの少ない介入テストセット（相互作用がMAR（Missing At Random）であるもの、あるいは少なくともよりMARに近いもの）を生成することです。
An example of this is SKEW, a sampling strategy that aims to adjust for the confounding effect that an item's popularity has on its likelihood of being observed.
その一例がSKEWで、アイテムの人気が観測される可能性に及ぼす交絡効果を調整することを目的としたサンプリング戦略である。

In this paper, we propose a novel formulation for the sampling approach.
本論文では、サンプリング・アプローチのための新しい定式化を提案する。
We compare our solution to SKEW and to two baselines which perform a random intervention on MNAR data (and hence are equivalent to no intervention in practice).
SKEWと、MNARデータに対してランダムな介入を行う2つのベースライン（つまり実際には介入しないのと同じ）とを比較した結果、SKEWの方が優れていた。
We empirically validate for the first time the effectiveness of SKEW and we show our approach to be a better estimator of the performance one would obtain on (unbiased) MAR test data.
SKEWの有効性を初めて実証的に検証し、我々のアプローチが（不偏の）MARテストデータで得られる性能のより良い推定者であることを示すことができました。
Our strategy benefits from high generality properties (e.g.it can also be employed for training a recommender) and low overheads (e.g.it does not require any learning).
本戦略は、**高い汎用性(例：レコメンダーの学習にも利用可能)**と**低いオーバーヘッド(例：学習を必要としない)**の利点があります。

# 1. Introduction 序章

Offline evaluation of a recommender system is done using an observed dataset, which records interactions (e.g.clicks, purchases, ratings) that occur between users and items during a given period in the operation of the recommender system.
推薦システムのオフライン評価は、推薦システムの運用期間中にユーザーとアイテムの間で発生したインタラクション（クリック、購入、評価など）を記録した観測データセットを用いて行われます。
However, this dataset is biased, not only due to the freedom that users have in choosing which items to interact with, but also due to other factors, known as confounders ([5, 27]).
しかし，このデータセットは，ユーザがどのアイテムと対話するかを自由に選べるだけでなく，交絡因子と呼ばれる他の要因によって，偏りがある（[5, 27]）。
For example, the user-interface plays an important role: differences in the ways that items are exposed to users (e.g.position on the screen) influence the likelihood of a user interacting with those items [14].
例えば、ユーザインターフェースは重要な役割を果たします。アイテムがユーザに露出される方法（画面上の位置など）の違いは、ユーザがそのアイテムと対話する可能性に影響する[14]。
The recommender itself sets up a feedback loop, which results in another confounder: users are typically more likely to interact with the recommender’s suggestions than with other items.
レコメンダー自体がフィードバックループを構築しているため(i.e. 推薦システムが推薦したアイテムはユーザに見られやすく、)、別の交絡要因が発生します。ユーザは通常、他のアイテムよりもレコメンダーの提案に接する可能性が高いのです。
The user’s preferences are also a confounder: for example, Marlin et al.demonstrate that, in a dataset of numeric ratings, the probability of not observing a specific user-item interaction depends on the value associated with that particular interaction (i.e.the rating value): informally, users tend to rate items that they like [18].
例えば、Marlinらは、数値評価のデータセットにおいて、特定のユーザーとアイテムの相互作用を観察しない確率が、その特定の相互作用に関連する値（すなわち、評価値）に依存することを実証している：非公式に、ユーザーは自分が好きなアイテムを評価する傾向がある [18] 。
Because of these and other confounders, interactions that are missing from an observed dataset are Missing Not At Random (MNAR) [18].
これらや他の交絡因子のために、観測されたデータセットから欠落している相互作用は**MNAR（Missing Not At Random）**[18]となる。

Classical offline evaluations using such an observed dataset are in effect making the assumption that interactions that are missing from the observed dataset are either Missing Completely At Random (MCAR) or Missing At Random (MAR) [18].
このような観測データセットを用いた古典的なオフライン評価は、実質的に、観測データセットから欠落した相互作用はMCAR（Missing Completely At Random）またはMAR（Missing At Random）のいずれかであると仮定している [18].
(For the distinction between MCAR and MAR, see Section 2.) Using MNAR data in an evaluation as if it were MCAR or MAR, results in biased estimates of a recommender’s performance [18]: for example, such experiments tend to incorrectly reward recommenders that recommend popular items or that make recommendations to the more active users [8, 21].
(MCARとMARの区別については、セクション2を参照)MCARやMARであるかのようにMNARデータを評価で使用すると、推薦システムの性能の偏った推定結果になります[18]。例えば、このような実験は、人気のアイテムを推薦する推薦者やよりアクティブなユーザの為に推薦する推薦者を不正に評価する傾向があります[8、 21]。

There are three ways of addressing this problem.
この問題に対しては、3つの方法があります。
The most straightforward approach (in theory, at least) is to collect and employ a MAR dataset instead of an MNAR one for the offline evaluation.
最も簡単なアプローチは（少なくとも理論的には）、オフライン評価のためにMNARデータセットの代わりにMARデータセットを収集し採用することです。
Using (unbiased) MAR data for the evaluation would give an unbiased estimate of the recommender’s performance.
評価に（偏りのない）MARデータを使用することで、レコメンダーの性能を偏りなく推定することができます。
In some domains, there are ways of collecting small MAR-like datasets (see Section 2).
ドメインによっては、小さなMARのようなデータセットを収集する方法があります（セクション2参照）。
But, in many domains it is either impractical or too expensive to obtain MAR-like datasets.
しかし、多くのドメインでは、MARのようなデータセットを入手するのは非現実的であったり、コストがかかりすぎたりします。

Because of the difficulty of collecting MAR-like data, the other two ways of addressing the problem focus on using MNAR data (which is usually available and in larger quantities) but mitigating its bias.
MARのようなデータの収集が困難なため、他の2つの方法では、MNARデータ（通常入手可能で量も多い）を使用しつつ、そのバイアスを軽減することに焦点を当てています。
One way of doing this is to design estimators (i.e.evaluation metrics) which compensate for the bias in the MNAR test data.
その一つの方法として、MNARテストデータのバイアスを補正する推定量（＝評価指標）を設計する。
Although this achieves the desired goal to some extent, unbiased estimators suffer from two potential drawbacks.
これはある程度望ましい目標を達成するものであるが、不偏推定量には2つの潜在的な欠点がある。
The first is that they may not be general enough to overcome all sources of bias, i.e.they are often designed to compensate for a specific kind of bias: for example, the accuracy metric that is proposed in [24] is able to correct only for the long-tail popularity bias in a dataset.
第一に，バイアスのすべての原因を克服するのに十分な汎用性がない可能性があることである．
例えば、[24]で提案されている精度指標は、データセットのロングテール人気バイアスのみを補正することができます。
The second drawback that affects unbiased estimators is that their unbiasedness might be proven only if the data satisfies some specific conditions: the ATOP estimator proposed in [23], for example, is unbiased only if the data satisfies two conditions.
不偏推定量に影響を与える2つ目の欠点は，データがいくつかの特定の条件を満たす場合にのみ不偏性が証明される可能性があるということである．
例えば，[23]で提案されたATOP推定器は，データが2つの条件を満たした場合にのみ不偏であることが証明されている．

The third approach is to intervene on MNAR test data before using it for the evaluation.
3つ目のアプローチは、評価に使う前にMNARのテストデータに介入することです。
In practice, such intervention is performed by means of a sampling strategy which samples from the available MNAR test data.
実際には、このような介入は、利用可能なMNARテストデータからサンプリングするサンプリング戦略によって実行されます。
The sampling strategy is chosen so that the intervened test set which results from the sampling is supposed to be less biased (more MAR-like) and therefore more suitable for evaluation of the recommender’s performance.
サンプリング戦略は、サンプリングの結果、介在するテストセットが偏りにくく（よりMAR的に）、レコメンダーの性能評価に適していると考えられるように選択される。
One such sampling strategy is known as SKEW [13]: it samples user-item interactions in inverse proportion to item popularity, thus producing test data with reduced popularity bias.
このようなサンプリング戦略の1つは、SKEW [13]として知られています。これは、アイテムの人気度に反比例してユーザーとアイテムの相互作用をサンプリングし、人気のバイアスを低減したテストデータを作成します。

In this paper we investigate a new alternative to the SKEW sampling strategy for generating intervened data.
本論文では、介入データを生成するためのSKEWサンプリング戦略に代わる新しい方法を調査する。
We propose a weighted sampling strategy in which the weights are calculated by considering the divergence between the distribution of users and items in the MNAR data and their corresponding target (unbiased) MAR distributions.
MNARデータにおけるユーザとアイテムの分布と、それらに対応するターゲット（不偏）のMAR分布との間の乖離を考慮して重みを計算する、重み付けサンプリング戦略を提案する。

We compare our sampling approach with SKEW.
このサンプリング手法をSKEWと比較します。
Our experiments allow us: to empirically evaluate for the first time the effectiveness of SKEW; to verify that both strategies successfully perform the desired debiasing action; but also to demonstrate that our strategy more closely approximates the unbiased performances of different recommender algorithms.
この実験により、SKEWの有効性を初めて実証的に評価することができました。また、両戦略が望ましいデビアス動作を正常に行うことを検証し、さらに、我々の戦略が異なる推薦アルゴリズムの不偏性能により近いことを実証することができました。

Although in this paper we employ our technique to generate a test set for offline recommender evaluation, our approach is general and can also be employed to debias the data used for training a recommender.
本論文では、オフラインでのレコメンダー評価のためのテストセットを生成するために本手法を採用していますが、本手法は一般的であり、**レコメンダーのトレーニングに使用するデータをデビアスするためにも採用できます**。

The rest of this paper is organized as follows.
本稿の残りの部分は、以下のように構成されている。
Section 2 presents related work.
第2節では、関連する仕事を紹介する。
In Section 3, we propose a probabilistic framework to study properties of MAR and MNAR datasets.
セクション3では、MARとMNARのデータセットの特性を研究するための確率的フレームワークを提案する。
In Section 4 we use the properties presented in Section 3 to derive our weighted sampling strategy, which is used to generate intervened test sets.
セクション4では、セクション3で示した特性を用いて、介在するテストセットの生成に用いる重み付けサンプリング戦略を導き出す。
Section 5 describes the experiments we have run to assess the effectiveness of our approach.
セクション5では、本アプローチの有効性を評価するために実施した実験について説明する。
We analyse the results of the experiments in Section 6.
第6節で実験結果を分析する。
We discuss our findings in Section 7.
第7節でその結果について述べる。

# 2. Related Work 関連作品

A distinction is sometimes drawn between Missing Completely At Random (MCAR) and Missing At Random (MAR).
MCAR（Missing Completely At Random）とMAR（Missing At Random）は区別されることがあります。
The distinction is based on missing data analysis theory and is first proposed by [16] and later introduced into the recommender systems literature by [18].
この区別は、欠損データ分析理論に基づいており、最初に[16]によって提案され、後に[18]によって推薦者システムの文献に紹介されました。
Indeed, MCAR, MAR and MNAR are terms used to denote different missing data mechanisms which describe the process that generates the observation pattern in the data.
実際、MCAR、MAR、MNARは、データの観察パターンを生成するプロセスを記述する異なる欠損データメカニズム(missing data mechanisms)を示すために使用される用語である。
In work on causal inference, the same process is typically called the assignment mechanism instead [10].
因果推論に関する研究では、同じプロセスは通常、代わりに割り当てメカニズムと呼ばれる[10]。
In [16, 18], MCAR means that whether a user-item interaction is missing does not depend on interaction values (such as ratings in a recommender) at all, i.e.it depends neither on the observed interaction values nor the missing interaction values.
[16,18]では、MCARとは、ユーザとアイテムの相互作用が欠損しているかどうかは、interaction values(レコメンダーにおける評価など)に全く依存しない、つまり、観測された相互作用値にも欠損した相互作用値にも依存しないことを意味する.
MAR, on the other hand, means that whether a user-item interaction is missing may depend on the observed interaction values, but is independent of the missing interaction values.
一方、MARは、ユーザーとアイテムのインタラクションが欠損しているかどうかは、観測されたインタラクション値に依存するかもしれないが、欠損したインタラクション値には依存しないことを意味します。

In this paper, we use MNAR and MAR in a more informal and general way.
本論文では、MNARとMARをより非公式かつ一般的な方法で使用します。
We use MNAR to indicate that data is biased (missing interactions depend on some confounders in the data), and we use MAR to mean that data is unbiased (missing interactions do not depend on any confounder in the data, whether it is observed or not).
MNARはデータが偏っている（欠損相互作用がデータ中のある交絡因子に依存している）ことを意味し、MARはデータが偏っていない（欠損相互作用がデータ中の交絡因子に依存していない、それが観測されているかどうかに関わらず）ことを意味する。
Although these more informal usages are not properly in line with the categorization in [16] and [18], our choice is broadly in line with other work in the recommender systems literature: what we refer to as MAR is also called MAR in papers such as [4, 23] and what we call MAR is referred to as MCAR in, e.g., [22].
これらの非公式な使い方は、[16]や[18]の分類と正しく一致していませんが、我々の選択は、推薦システムの文献における他の仕事と広く一致しています：我々がMARと呼ぶものは、[4、23]などの論文でMARとも呼ばれ、我々がMARと呼ぶものは、[22]などでMCARと呼ばれています。

A substantial body of work has been done in the last few years to cope with bias in recommenders, both for their training and their offline evaluation.
ここ数年、レコメンダーの訓練とオフライン評価の両方で、推薦者のバイアスに対処するための相当な研究が行われている。
We focus here more on the latter, as it is more relevant to our work in this paper.
**本稿では、より後者に焦点を当てます**。なぜなら、後者の方が本論文での研究に関連するからです。

As we mentioned in Section 1, one approach is to collect a separate MAR-like dataset (i.e.one that is as devoid of bias as possible) to use for the evaluation of the recommender’s performance.
セクション1で述べたように、推薦者の性能評価に使用するMARのようなデータセット（できるだけ偏りのないもの）を別途収集するのも一つの方法です。
This is usually done by means of what we will call a “forced rating approach” [4].
これは通常、**“forced rating approach”(強制格付けアプローチ)**と呼ばれる方法によって行われる[4]。
User-item pairs are chosen uniformly at random and for each user-item pair that gets selected the user is required (forced) to provide a rating for the item.
ユーザとアイテムのペアは一様にランダムに選択され、選択された各ユーザーとアイテムのペアに対して、ユーザーはアイテムに対する評価を提供することを要求される（強制される）。
In this way, from the data that we collect we remove biases such as the item discovery bias (because items are randomly chosen for users), item consumption bias (because users are forced to consume or interact with the item so that they can rate it, unless the item was already known to the user) and rating decision bias (because users are not free whether to rate the chosen item or not, they are forced to do it) [4].
このようにして、収集したデータから、アイテム発見バイアス（アイテムがユーザのためにランダムに選ばれるため）、アイテム消費バイアス（アイテムがすでにユーザに知られていた場合を除き、ユーザがアイテムを評価できるようにアイテムを消費または対話することを強いられるため）、評価決定バイアス（選ばれたアイテムを評価するかどうかはユーザーの自由ではなく、それを強いられるため）などのバイアスを除去します[4]。

Datasets collected by the “forced rating approach” are MAR-like, rather than MAR: they may still carry some bias.
強制評価アプローチ」で収集されたデータセットは、MARというよりMAR的なもの(少しbiasを含んでいるって意味?)です。
When building such a dataset, for example, although invitations are sent to users who are chosen uniformly at random, those who agree to participate may be atypical, thus introducing bias.
例えば、このようなデータセットを構築する場合、ランダムに選ばれた一様なユーザに招待状を送るものの、**参加に同意したユーザが非典型的(=要は何らかの傾向がある?)である可能性があり**、バイアスが発生することがあります。
Equally, the fact that, for each user, items to rate are presented sequentially introduces bias: the rating a user assigns to a particular item may be influenced by the items she has rated so far.
また、各ユーザの評価項目が順次表示されるため、ある項目に対する評価が、それまでに評価した項目の影響を受けてしまうというバイアスが発生します。
Although this means that these datasets are less biased, rather than unbiased, to the best of our knowledge, this is still the best way of collecting this type of data.
これは、これらのデータセットが、私たちの知る限りでは、偏りがないどころか、むしろ偏りが少ないことを意味しますが、それでもこの種のデータを収集するには、これが最良の方法です。

Datasets of this kind include Webscope R3 [18] and cm100k [4] in the music domain, and CoatShopping [22] in the clothing domain.
この種のデータセットとしては、音楽分野ではWebscope R3[18]やcm100k[4]、衣服分野ではCoatShopping[22]などがある。
The “forced rating approach” can only work in certain domains; for example, it requires that a user who is presented with an item can quickly consume that item so as to provide a rating.
強制レーティングアプローチ」は、例えば、アイテムを提示されたユーザが、そのアイテムを素早く消費してレーティングを提供できることが必要であるなど、特定の領域でしか機能しない。
In the movie domain, for example, we almost certainly cannot require a user to watch an entire movie (although we could require them to watch a movie trailer).
例えば映画の領域では、ユーザーに映画全体を見ることを要求することはほぼ不可能です（映画の予告編を見ることを要求することは可能です）。

(ここからアプローチ2の既存研究の説明)
Therefore, because in some domains obtaining a MAR-like dataset may be impractical, most work on unbiased offline evaluation of recommenders still relies on the use of MNAR datasets.
そのため、ドメインによってはMARのようなデータセットを得ることが現実的でない場合もあり、推薦者の公平なオフライン評価に関する研究の多くは、依然としてMNARデータセットの使用に依存しています。
The majority of the literature tries to overcome the bias in an MNAR test set by proposing new estimators (i.e.evaluation metrics) which provide unbiased or nearly unbiased measures of performance on the MNAR test data.
多くの文献は、MNARテストセットにおける偏りを克服するために、MNARテストデータにおける性能の不偏またはほぼ不偏の測定値を提供する新しい推定量（すなわち評価メトリック）を提案することを試みています。
Steck describes ATOP, for example, a new ranking estimator which is unbiased under specific mild assumptions about the data employed [23, 25].
Steckは、例えばATOPについて、採用したデータに関する特定の穏やかな仮定の下で不偏である新しいランキング推定器を説明している[23, 25]。
Steck also proposes an accuracy metric that is able to correct for the long-tail popularity bias in the data, resulting in a nearly unbiased estimate of the true accuracy under the assumption that no other confounders besides the so-called popularity bias occurs [24].
Steckはまた、データ中のロングテールの人気バイアスを補正できる精度指標を提案しており、その結果、いわゆる人気バイアス以外の交絡因子が発生しないと仮定した場合、真の精度をほぼ不偏に推定できる[24]。
There is work too on unbiased estimators for implicit MNAR data.
暗黙のMNARデータに対する不偏推定量に関する研究も行われている。
An example of this appears in [15], where the authors proposed a missing data model and a novel evaluation measure, i.e.Average Discounted Gain (ADG), built upon the widely used NDCG metric.
この例として、[15]では、著者が欠落データモデルと、広く使われているNDCGメトリックをベースにした新しい評価尺度、すなわちAverage Discounted Gain（ADG）を提案している。
They show ADG allows unbiased estimation with respect to their missing data model, unlike NDCG.
彼らは、ADGがNDCGとは異なり、彼らの欠損データモデルに関して不偏推定を可能にすることを示した。
Other work uses Inverse-Propensity-Scoring (IPS) techniques (e.g.[22, 28]).
他の研究では、Inverse-Propensity-Scoring（IPS）技術を使用しています（例：[22, 28]）。
A propensity is the probability that a particular user-item pair is observed.
propensity(傾向)とは、特定のユーザとアイテムのペアが観察される確率のことである。
This work on IPS uses propensities as a proxy to build unbiased estimators on explicit ([22]) and implicit ([28]) data respectively.
IPSに関するこの研究は、プロペンシティをプロキシとして使用し、陽的データ（[22]）と陰的データ（[28]）それぞれについて不偏推定量を構築する。
One drawback of propensities is that their estimation might require an expensive learning step (e.g.[22, 28]).
propensityの欠点は、その推定に高価な学習ステップが必要な場合があることである（例えば[22, 28]）。

(ここからアプローチ3の既存研究の説明)
There are those who use what we are calling an intervention approach.
私たちが介入アプローチと呼んでいるものを使っている人たちがいます。
They sample from the MNAR test set to produce a smaller MAR-like test set (the intervened set), which they use in the evaluation in place of the MNAR test set.
**MNARテストセットからサンプリングして、より小さなMARのようなテストセット（intervened set）を作成**し、MNARテストセットの代わりに評価で使用するのです。
One such method is Lang et al.’s SKEW method, which samples user-item pairs in inverse proportion to the item popularity.
その一つがLangらのSKEW法で、アイテムの人気度に反比例してユーザーとアイテムのペアをサンプリングする。
This generates an intervened test set which has roughly uniform exposure distribution across items, thus reducing the item popularity bias in the test set [13].
これにより、アイテム間の露出分布がほぼ均一な介在テストセットが生成され、テストセットにおけるアイテムの人気バイアスが軽減されます[13]。
Lang et al.in [13, 27] and Bonner et al.in [3] use this technique for test set generation to evaluate causal approaches to recommendation.
Langら[13, 27]やBonnerら[3]は、この技術を推薦の因果的アプローチを評価するためのテストセット生成に用いている。
However, none of the three works that we have just cited either explain or verify empirically why SKEW should be effective as a debiasing technique.
しかし、今挙げた3つの著作は、いずれもSKEWがデビアス技術として有効である理由を実証的に説明・検証したものではありません。
In this paper we fill the gap by providing such contributions.
本論文では、そのような貢献を提供することでギャップを埋める。
Also, because of the similarity with our work, we use SKEW as a state-of-the-art strategy to compare against our own approach.
また、私たちの研究と類似しているため、私たちのアプローチと比較するために、SKEWを最先端の戦略として使用します。

Bellogin et al.also sample an MNAR dataset to try to obtain a fairer evaluation [2].
Belloginらは、より公平な評価を得るために、MNARデータセットをサンプリングしています[2]。
Their first approach is a form of stratification, in which test items are sampled from a popularity-based partition of the data.
最初のアプローチは層別化であり、テスト項目はデータの人気ベースのパーティションからサンプリングされるものである。
Their second approach builds a test set with the same number of ratings for each item.
第二のアプローチは、各項目について同じ数の評価を持つテストセットを構築するものである。
Compared with our work, their approaches are more limited since both have the goal only of reducing popularity bias.
私たちの研究と比較すると、**両者とも人気の偏りを減らすことだけを目的としているため、より限定的なアプローチ**となっています。
Their approaches may also result in quite small tests sets, especially if the popularity curve in the original dataset is quite steep.
また、これらのアプローチでは、特に元のデータセットの人気曲線が非常に急な場合、非常に小さなテストセットになることがあります。

(最後に、MNARデータを使った学習の話。)
To conclude this review, and for completeness, we mention some of the work that has applied debiasing techniques when training recommender systems.
このレビューの締めくくりとして、また完全性を期すために、推薦システムのトレーニングにデビアス技術を適用した研究のいくつかを紹介する。
In [9, 12, 17], for example, existing algorithms are adapted to include explicit MNAR data models.
例えば、[9, 12, 17]では、既存のアルゴリズムを、明示的なMNARデータモデルを含むように適応している。
Others employ unbiased estimators as a loss function to train their model and therefore correct for the bias in the training set (e.g.[15, 23, 24]), while others take a causal inference perspective (e.g.[11, 13, 14, 26]).
また、モデルを訓練するための損失関数として不偏推定量を採用することで、訓練セットのバイアスを補正するもの（[15, 23, 24]など）や、因果推論の視点を持つもの（[11, 13, 14, 26]など）などがある。

# 3. Properties of Datasets: A Probabilistic Framework データセットの特性 確率論的な枠組み

In this section, we define a probabilistic framework to analyse properties of MAR and MNAR datasets.
本節では、MARとMNARのデータセットの特性を分析するための確率的フレームワークを定義する。
Then, in Section 4, we use these properties to design our approach that generates intervened test sets for ‘unbiased’ evaluation.
そして、セクション4では、これらの特性を利用して、**「‘unbiased’(不偏)」な評価**のために介在するテストセットを生成する我々のアプローチを設計する.

We consider a user-item space, $U × I$, of size |U | · |I |.
U
We denote with u ∈ U = {1, .., |U |} a generic user and with i ∈ I = {1, .., |I |} a generic item.
U
We denote with D = {O ∈ {0, 1} U ×I ,Y ∈ R U ×I } a generic observed dataset.
一般的な観測データセット を $D = {O \in {0, 1}^{U \times I}, Y \in \mathbb{R}^{U \times I}}$と表記する。
The binary matrix O records which interactions between users and items have been observed: Ou,i = 1 if an interaction is observed and Ou,i = 0 otherwise.
二値行列$O$には、ユーザとアイテムの間のどのようなインタラクションが観察されたかが記録される： interactionが観測された場合はO*{u,i} = 1、そうでない場合はO*{u,i} = 0である。
We also define the associated matrix Y ∈ R U ×I which records the value of the interactions of the corresponding observed entries in O: we have Yu,i , 0 where Ou,i = 1, Yu,i = 0 otherwise.
また、Oの対応する観測項目のinteractionの値を記録する関連行列 $Y \in R^{U \times I}$ を定義する：O*{u,i} = 1のとき$Y*{u,i} \neq 0$、それ以外は $Y\_{u,i} = 0$ とする。
When discussing Y, we use the general term “interaction value”, rather than “rating”, to emphasize the generality of our framework: Y can take values of any kind in R whether they denote ratings, number of clicks, number of views, listening frequencies, etc.
$Y$ について議論するとき、**本フレームワークの一般性を強調するため**に、"rating"ではなく、「**interaction value(相互作用値)**」という一般的な用語を使用する： Yは、評価、クリック数、閲覧数、聴取頻度など、 $\mathbb{R}$ のあらゆる種類の値を取ることができます。(フレームワークの一般性、素晴らしい...!!)
We also define the binary random variable O : U ×I → {0, 1} over the set of user-item pairs in O as O = 1 if the user-item interaction is observed and O = 0 otherwise.
また、**Oに含まれるユーザアイテム対の集合を対象とした二値確率変数** $Q: U \times I → {0, 1}$を、ユーザアイテム間のinteractionが観測された場合にQ = 1、それ以外の場合にQ = 0と定義する。(**Oとの違いが難しい...?**)
(But later we will use abbreviation P(O) in place of P(O = 1).)
(ただし、後にP(Q = 1)の代わりにP(Q)という略語を使う)。
Using this notation, we can refer to two kinds of datasets over the same U ×I space, Dmnar = {O mnar ,Y mnar } and Dmar = {O mar ,Y mar }, which have MNAR and MAR properties respectively.
これらの表記(notation)を用いると、同じU×I空間上の2種類のデータセット、$D_{mnar} = {O^{mnar},Y^{mna}}$と $D_{mar} = {O^{mar} ,Y^{mar}}$ を、それぞれMNARとMARの特性を持つものとして参照することができます。

## 3.1. Properties of a MAR dataset MARデータセットの特性

We will formally describe how D mar is generated.
$D_{mar}$ の生成方法について正式に説明します。
We make use of the forced ratings approach that we described in Section 2.
2章で説明した**forced ratings approach**(あれ?アプローチ1だっけ...?)という手法を活用しています。
First, we need to randomly sample a set of user-item pairs in order to generate O mar .
まず、ユーザとアイテムのペアをランダムにサンプリングして、$O^{mar}$を生成する必要があります。
Then, a preference (interaction value) for each pair in O mar is collected so that Y mar is obtained.
そして、$O^{mar}$の各ペアのプリファレンス(Interaction value)を収集し、$Y^{mar}$を得ることができる.
Note that, in order to satisfy the MAR property, the generation ofO mar is totally independent fromY mar and from the particular user-item pair (u,i) as well.
なお、**MAR特性を満たすために、$O^{mar}$の生成は$Y^{mar}$から完全に独立しており、特定のユーザとアイテムのペア（u,i）からも独立していることを特徴とする。**
We also assume that, once O mar is determined, we can obtain interaction values Y mar for all user-item pairs in O mar .
また、O marが決まれば、O marに含まれるすべてのユーザとアイテムのペアのinteraction value $Y^{mar}$を得ることができると仮定する。
(In practice, of course, users may decline the invitation to participate or may refuse to give some ratings, which is one reason why in reality these datasets are MAR-like and not MAR.)
(もちろん実際には、ユーザーは参加の誘いを断ったり、一部の評価を拒否したりすることがあり、これが現実にはこれらのデータセットがMAR的でありMARではない理由の一つである)。(=これは現実の話だよね...!!アプローチ1の!)

To achieve the goal, we make use of the probability distribution Pmar (O|u,i), defined over the space U × I, that leads to O mar .
この目的を達成するために、U×I空間上で定義される確率分布$P_{mar}(Q|u,i)$ を利用し、$O^{mar}$を導きます。
A straightforward choice is to set Pmar (O|u,i) = P(O) = ρmar , where ρmar represents the desired ratio of observed entries from U × I.
素直な選択は、$P_{mar}(Q|u,i) = P(Q) = \rho_{mar}$ とすること. ここで$\rho_{mar}$ は、U×Iから観測されたエントリーの望ましい比率を表す.
Now, assuming that a dataset D mar has been collected using such an approach, we should empirically verify that user and item posterior probabilities are (roughly) uniformly distributed:
さて、このような手法で収集されたデータセット $D_{mar}$ を想定して、**ユーザとアイテムの事後確率が（ほぼ）一様に分布していることを経験的に検証する**必要があります：

$$
P_{mar}(u|Q) = \frac{|O_{u}^{mar}|}{O^{mar}} \sim \frac{1}{|U|}, \forall u \in U
\tag{1}
$$

$$
P_{mar}(i|Q) = \frac{|O_{i}^{mar}|}{O^{mar}} \sim \frac{1}{|I|}, \forall i \in I
\tag{2}
$$

where O mar u and O mar i are the observed interactions in O mar for user u and item i respectively.
ここで、$O^{mar}_{u}$と$O^{mar}_{i}$はそれぞれ、ユーザuとアイテムiの$O^{mar}$で観測されたInteractionである.

Also, because users and items are drawn independently, we have that their posteriors are independent and we can write:
また、ユーザとアイテムは独立に描かれるため、それらの事後分布は独立であることがわかり、こう書くことができる：

$$
P_{mar}(u,i|Q) = P_{mar}(u|Q) \cdot P_{mar}(i|Q) \in \frac{1}{|U||I|}, \forall(u,i) \in U \times I
\tag{3}
$$

for the joint posterior of a specific user-item pair.
$P_{mar}(u,i|Q)$は、特定のユーザとアイテムのペアの同時事後分布(=事後分布の同時分布、みたいな?)を表す。

## 3.2. Properties of an MNAR dataset MNARデータセットの特性

MNAR data is, of course, usually collected during the operation of a recommender system.
MNARデータは、もちろん、通常、レコメンダーシステムの運用中に収集されます。
But, similarly to the way we modelled the generation of MAR data, we can model the generation of a MNAR dataset Dmnar = {O mnar ,Y mnar } in terms of a drawing process which determines O mnar first and Y mnar subsequently.
しかし、MARデータの生成をモデル化したのと同様に、MNARデータセット $D_{mnar} = {O^{mnar},Y^{mnar}}$ の生成過程を、最初にO mnar、その後にY mnarを決定する描画プロセスでモデル化することができます。

Differently from the MAR scenario, due to the presence of bias, we cannot assume the sampling distribution Pmnar to be independent from the interaction values Y mnar (or from other confounders too, including, e.g., the specific user and item (u,i)).
MARシナリオとは異なり，バイアスが存在するため，**サンプリング分布**$P_{mnar}$がinteraction value $Y^{mnar}$（あるいは特定のユーザーとアイテム（u,i）を含む他の交絡因子からも）から独立していると仮定することはできない．
In other words, in an MNAR dataset the draw is generally guided by some unknown probability Pmnar (O|u,i,Y, X), where Y ⊃ Y mnar represents the complete set of user-item interactions and X represents a set of features (covariates, confounders) which influences the sampling probability (e.g.user demographics, item features, characteristics of the system such as the way it exposes items to users, and so on).
つまり、MNARデータセットでは、一般的に未知の確率 $P_{mnar}(Q|u,i,Y,X)$ によって抽選が導かれる.
ここで、$Y⊃Y^{mnar}$は**ユーザとアイテムのinteraction valueの完全なセット**(答えって事だろうか...??ゼロ要素が存在しない評価行列)を表し、Xはサンプリング確率に影響を与える特徴(共変量、交絡因子)のセット(例えば、ユーザのデモグラフィック、アイテムの特徴、アイテムをユーザーに公開する方法などのシステムの特徴など)を表します。

If a MNAR dataset D mnar has been collected, we can examine user and item posterior probabilities in O mnar , as we did for the MAR dataset but now, in general, we will find:
MNARデータセット $D_{mnar}$ が収集されている場合、MARデータセットで行ったように、 $O^{mnar}$ のユーザとアイテムの事後確率を調べることができるが、今度は一般的に、次のことが分かる：
(ここでいう事後確率は、O=1のinteractionをランダムに取得した時に、それがユーザuのinteractionである確率、みたいなイメージ...!)

$$
P_{mnar}(u|Q) = \frac{|O^{mnar}_{u}|}{O^{mnar}} \neq = \frac{1}{|U|}, \forall u \in U
\tag{4}
$$

$$
P_{mnar}(i|Q) = \frac{|O^{mnar}_{u}|}{O^{mnar}} \neq = \frac{1}{|U|}, \forall u \in U
\tag{5}
$$

In general, the users and items are not uniformly distributed and thus, given that a specific entry is observed, i.e.O = 1, we cannot assume the user and item posterior independence for the joint posterior Pmnar (u,i|O), i.e.
**一般に、ユーザとアイテムは一様に分布しているわけではない**ので、特定のエントリーが観測された場合、すなわち$Q = 1$の場合、共同事後確率$P_{mnar}(u,i|Q)$ に対してユーザとアイテムの事後独立性は仮定できない、すなわち

$$
P_{mnar}(u,i|Q) \neq P_{mnar}(u|Q) \cdot P_{mnar}(i|Q), \forall (u,i) \in U \times I
\tag{6}
$$

However, the formulation that we have given here provides us with a solid framework to design our debiasing strategy in the next section.
しかし、**ここで示した定式化は、次のセクションでデビアス戦略を設計するための強固なフレームワークを提供します**。(なるほど...?これらの事後確率の定式化をサンプリング戦略で使うのか!)
(このセクションは、MARデータやMNARデータの性質はかくあるべき、というような話だっけ??)

# 4. Intervened Test Sets 介在型テストセット

To conduct unbiased evaluation from biased data, we generate and use intervened test sets in place of classical random heldout test sets.
**偏ったデータから偏りのない評価を行うため**に、古典的なランダムなhold-out テストセットの代わりに、**intervenedテストセット**を生成して使用します。
We begin by presenting this approach in general (Section 4.1), and then we present the specifics of our approach (Sections 4.2 and 4.3).
まず、このアプローチを一般的に紹介し（4.1節）、次に我々のアプローチの具体的な内容を紹介する（4.2節と4.3節）。

## 4.1. The sampling approach サンプリングアプローチ(一般的な紹介)

The sampling approach consists in performing a debiasing intervention on MNAR data D mnar by means of a given sampling strategy, denoted with S.
サンプリングアプローチは、$S$で示される所定のサンプリング戦略によって、MNARデータ$D^{mnar}$に対してデビアス介入を行うことからなる。
The result of the intervention is the dataset DS = {O S ⊂ O mnar ,Y S ⊂ Y mnar }, with the objective that DS has unbiased-like properties.
介入の結果、データセット$D_S = {O^S \cap O^{mnar},Y^S \cap Y^{mnar}}$となり、$D_s$が不偏的な性質を持つことが目的となる.(ふむふむ...!)
We follow the same reasoning adopted to study properties of MAR and MNAR datasets.
MARとMNARのデータセットの特性を研究するために採用したのと同じreasoning(方法論?)に従う.
Thus, we generate O S first and then we obtain Y S accordingly.
したがって、まず$O_S$を生成し、それに応じて$Y_S$を得ることになります。

The sampling is performed on the space O mnar , ignoring interaction values in Y mnar .
サンプリングは空間$O^{mnar}$に対して行われ，$Y^{mnar}$のinteraction valueは無視される.
We denote with S : U × I → {0, 1} the binary random variable that guides the sampling.
**サンプリングを導く二値確率変数**を$\mathcal{S} : U × I → {0, 1}$とする。
S = 1 when a particular user-item pair is sampled from O mnar , 0 otherwise.
$O^{mnar}$から特定のユーザとアイテムのペアがサンプリングされている場合はS = 1、そうでない場合は0とする. (i.e. ある(u,i)ペアがサンプリングされるか否かのbinaryの確率変数=bernouli分布に従うやつか...!)
(Again, we will use abbreviation P(S) in place of P(S = 1).)
(ここでも$P(S=1)$の代わりに $P(S)$ という略語を使う).
In practice, a particular strategy S is characterized by the expression of the probability PS (S|u,i), ∀(u,i) ∈ O mnar , which is the probability distribution responsible for guiding the sampling on O mnar .
実際には、特定の戦略S は、確率$P_S(\mathcal{S}|u,i) \forall(u,i) \in O^{mnar}$ の表現によって特徴付けられ、これは$O^{mnar}$上の**サンプリングを誘導する役割を持つ確率分布**である.
(i.e. u,iを条件づけた時にS=1となる確率が決定される関数みたいな?? つまりこの関数の出力値はbernouli分布のパラメータlambda...!!)
We present our sampling approach in the next subsection.
次のサブセクションで、本論文が提案するサンプリングのアプローチを紹介する.
In Section 5, we will also define PS for SKEW and for two baseline approaches that we compare against in the experiments.
セクション 5 では、SKEW の $P_S$ と、実験で比較した 2 つのベースラインアプローチの $P_S$ も定義する.

## 4.2. Our approach: weights for the sampling Our approach: サンプリングのための重み付け

In the presentation of our approach, we will start by assuming the availability of some MAR-like data O mar in addition to MNAR data O mnar .
本アプローチでは、MNARデータ$O^{mnar}$に加えて、MAR的なデータ$O^{mar}$があることを前提に説明します。(え! debiasアプローチ1で取得する様なMAR-likeなデータも必要なの??)
In fact, we will see in Section 4.3 that we can use our approach even in cases where we do not have any MAR data.
実際、4.3節では、**MARデータがない場合でも、本アプローチを使用できることを確認する。**(良かったー...!)

Our main idea is to make the posterior probability distribution of each user-item pair in the sampled O S , i.e.PS (u,i|S), approximately the same as the posterior probability distribution observed for the corresponding user-item pair in O mar , i.e.Pmar (u,i|O).
我々の主なアイデアは、サンプリングされた$O^S$の各ユーザ・アイテムペアの事後確率分布、すなわち$P_S(u，i|\mathcal{S})$を、**$O^mar$の対応するユーザ・アイテム・ペアについて観測された事後確率分布、すなわち $P_{mar}(u, i|O)$とほぼ同じにすること**である.
In other words, we want to make O S similar to O mar in terms of its posteriors.
つまり、$O^S$を$O^{mar}$に**後付けで似せたい**のです。
Writing this as a formula, we want:
これを数式で書くと、次のようになります：

$$
P_S(u,i|\mathcal{S}) \sim P_{mar}(u,i|\mathcal{O}), \forall(u,i) \in O^S
\tag{7}
$$

To obtain this approximation, we adjust the posterior distributions of the sampling space O mnar , i.e.Pmnar (u,i|O), using useritem weights w = (wui)u ∈U ,i ∈I (similarly to [19]).
この近似を得るために，ユーザアイテムの重み $w = (w_{ui})_{u \in U ,i \in I}$ を用いて，サンプリング空間 $O^{mnar}$ の事後分布，すなわち $P_{mnar}(u,i|\mathcal{O})$ を調整する（ [19] と同様である）．
We denote the modified weighted MNAR posteriors by Pmnar (u,i|O,w).
修正された**重み付きMNAR事後分布**を $P_{mnar}(u,i|\mathcal{O},w)$ と表記することにする。
The goal is to find weights w so that:
以下の等式を満たせるように重みwを見つけることが目的です：

$$
P_{mnar}(u,i|\mathcal{O},w) = P_{mar}(u,i|\mathcal{O}), \forall(u,i) \in O^{mnar}
\tag{8}
$$

From the fact that a typical MAR dataset is uniformly distributed over users and items, we use the independence of formula 3 to re-write the right-hand side of formula 8 to obtain:
**典型的なMARデータセットがユーザとアイテムに一様に分布していること**から、数式(3)の独立性を利用して数式8の右辺を書き換えて求める：

$$
P_{mnar}(u,i|\mathcal{O},w) = P_{mar}(i|\mathcal{O}) \times P_{mar}(u|\mathcal{O})
\tag{9}
$$

Similarly to formula 6 which considers user and item MNAR posteriors, user and item weighted MNAR posteriors will not in general be independent.
ユーザとアイテムのMNAR事後分布を検討した式(6)と同様に、重み付けMNAR事後分布においてもユーザとアイテムは一般に独立ではない.
However, we are going to treat them as if they were independent, to obtain the following:
しかし、**ここではそれらを独立したものとして扱い**、次のように求めます：

$$
P_{mnar}(u,i|\mathcal{O},w)
= P_{mnar}(i|\mathcal{O},w) \times P_{mnar}(u|\mathcal{O},w)
, \forall(u,i) \in O^{mnar}
\tag{10}
$$

While formula 10 is not true in general, we justify it by showing empirically in Section 6 that it does obtain good results.
**式10は一般的には正しくないが、第6節で経験的に良い結果が得られることを示し、これを正当化する**.(理論的には不当な式変形だけど、経験的に効果あるから採用！って話...!)
Now, using 10, we can split formula 9 into the two following equations:
さて、式10を使って、式9を次の2つの式に分割することができます：

$$
P_{mnar}(u|\mathcal{O},w) = P_{mar}(u|\mathcal{O})
\tag{11}
$$

$$
P_{mnar}(i|\mathcal{O},w) = P_{mar}(i|\mathcal{O})
\tag{12}
$$

As a consequence of formulas 11 and 12 for the weighted MNAR posteriors, we can define and calculate user-specific weights w = (wu )u ∈U and item-specific weights w = (wi)i ∈I instead of weights that are user-item specific.1
重み付き MNAR 事後分布に関する式 11 と式 12 の結果として、ユーザ&アイテムペアに特化した重みの代わりに、ユーザ固有の重み $w = (w_{u})_{u \in U}$ とアイテム固有の重み $w = (w_i)_{i \in I}$ を定義して計算することができる.
(Having independent user and item weights also has an advantage in terms of scalability. We need to calculate only |U | + |I | weights instead of |U × I |. This is good for scalability because |U × I | >> |U | + |I | for the values of |U | and |I | that we find in recommender domains.)
(また、ユーザとアイテムの重みが独立していることは、スケーラビリティの面でも有利である. $|U \times I|$の代わりに、$|U| + |I|$の重みだけを計算すればよいのです。これはスケーラビリティの点でも良いことで、レコメンダー領域で見られるような｜U｜と｜I｜の値に対しては、$|U×I| > |U|+|I|$となるので...!)

We propose the most straightforward solution to model the weighted MNAR posteriors, i.e.Pmnar (.|O,w) = w.Pmnar (.|O).
我々は、重み付けされたMNAR事後分布をモデル化する最も簡単な解決策、すなわち.$P_{mnar}(.|\mathcal{O},w) = w_{.} \cdot P_{mnar}(.|\mathcal{O})$ を提案します。(**元々の事後確率を重み付けする...!シンプルな作戦**!)
We plug this into formulas 11 and 12 and we obtain wuPmnar (u|O) = Pmar (u|O), wiPmnar (i|O) = Pmar (i|O) for each user and item weighted distribution respectively.
これを数式11及び数式12に当てはめると、各ユーザ及びアイテムの重み付け分布について、それぞれ$w_u \cdot P_{mnar}(u|\mathcal{O})＝P_{mar}(u|\mathcal{O})$、$w_i \cdot P_{mnar}(i｜\mathcal{O})＝P_{mar}(i｜\mathcal{O})$が得られる.
(重み計算の為には、どうしても$P_{mar}(.|\mathcal{O})$の値が必要になる気がするんだけど...、理想的なMARデータとみなして理論値$1/|.|$を使えばいいのかな...!)
Simply reversing these last two formulas, we have the expressions for calculating the weights:
この2つの式を逆にすれば、重みの計算式ができあがります：

$$
w_{u} = \frac{P_{mar}(u｜\mathcal{O})}{P_{mnar}(u｜\mathcal{O})}, \forall u \in U
\tag{13}
$$

$$
w_{i} = \frac{P_{mar}(i｜\mathcal{O})}{P_{mnar}(i｜\mathcal{O})}, \forall i \in I
\tag{14}
$$

We can think of the calculated weights as quantities that measure the divergence between the MNAR distributions of the sampling space and the target MAR distribution.
算出された重みは、**サンプリング空間のMNAR分布と目標のMAR分布との乖離を測る量**と考えることができます。
Because a specific weight adjusts the corresponding MNAR distribution, we directly use weights to model the sampling distribution, i.e.PS (S|u,i) = wuwi .
特定のウェイトが対応するユーザorアイテムのMNAR分布を調整するため、ウェイトを直接使用してサンプリング分布をモデル化する、すなわち$P_S(\mathcal{S}|u,i) = w_u \cdot w_i$ 。
During the sampling, the effect of the weights is to increase or decrease the probability that a particular user-item pair is sampled depending on how divergent are the user and item posterior probabilities in the MNAR sampling space with respect to the MAR distributions.
サンプリングにおける重みの効果は、**MAR分布に対するMNARサンプリング空間のユーザとアイテムの事後確率がどれだけ乖離しているか**によって、**特定のユーザとアイテムのペアがサンプリングされる確率が増減する**ことである.

In fact, based on preliminary experiments, we use PS (S|u,i) = wu (wi) 2 instead.
実際には、予備実験に基づき、$P_S(\mathcal{S}|u,i) = w_u \cdot (w_i)^2$ を代わりに使用する.(アイテムのbias対処により重きを置いた方が経験的に結果が良かった??)
This variant, denoted by WTD in the rest of this paper, raises the importance of the item-weight relative to the user weight.
この変形は、本論文の残りの部分では **WTD** と表記され、**ユーザウェイトに対してアイテムウェイトの重要性を高めて**います。(WTDはなんの略だろう...)
Specifically, (wi) 2 will be bigger than wi if wi is greater than one, and (wi) 2 will be smaller than wi if wi is less than one.
具体的には、$w_i$が1より大きい場合は$w_i^2$がw_iより大きくなり、w_iが1より小さい場合はw_i^2がw_iより小さくなります。
This choice makes sense in the light of previous research reported in the literature which identifies item popularity as one of the most impactful confounders in MNAR data, e.g.[21, 24].
この選択は、**MNARデータにおいてアイテムの人気が最も影響力のある交絡因子の1つであるとする文献で報告された先行研究**（例：[21, 24]）に照らして理にかなっています。(popularity biasが最も影響のある交絡因子の一つ...!)

## 4.3. Hypothesized distributions for the weights 重みの分布の仮説

Up to this point, we assumed the availability of some MAR-like data in order to give us the posteriors that we need to approximate.
ここまでは、近似に必要な事後分布(=$P_{mar}(u,i|\mathcal{O})$)を与えるために、MAR-likeデータがあることを想定していました。
But MAR-like data is expensive or impossible to collect, as we discussed when presenting the “forced rating approach” earlier.
**しかし、MARのようなデータは、先ほどの“forced rating approach”の提示の際に述べたように、高価であったり、収集不可能であったりします**。(ウンウン.)
Furthermore, in those cases where we do have a reasonable amount of MAR-like data at hand, we could use it directly as an unbiased test set.
さらに、手元にそれなりの量のMARのようなデータがある場合には、それをそのまま不偏のテストセットとして使用することも可能です。
Using it to calculate weights so that we can intervene on MNAR data to produce a more MAR-like test set would then be pointless.
MNARのデータに介入して、よりMARに近いテストセットを作るために、重みを計算するために使うのは無意味なことです。(うんうん確かに...!そもそも...!)

In fact, when we do not have any MAR-like data, we can still use our approach.
実際、**MARのようなデータがない場合でも、私たちのアプローチを使うことは可能**です。
We know that the posterior probability distribution for MAR data is uniform (Pmar (u|O) = 1/|U |, Pmar (i|O) = 1/|I |), and this is all we need for our sampling approach.
MARデータの事後確率分布はユーザ & アイテムに対して一様である(i.e. $P_{mar}(u|\mathcal{O}) = 1/|U|, P_{mar}(i|\mathcal{O}) = 1/|I|$)ことが分かっており、この情報が本サンプリングアプローチに必要なすべてである.(うんうん!やっぱり!)
Therefore, we can use this hypothesized distribution when calculating the weights, avoiding the need for a MAR-like dataset.
そのため、**ウェイトを計算する際にこの仮説通りの分布を利用することで、MARのようなデータセットが不要になります。**
We call this strategy, WTD_H (where the H stands for “hypothesized”).
この戦略を **WTD_H（Hは "hypothesized "の略）**と呼んでいます。

# 5. Experiments 実験

We have assessed WTD and WTD_H in offline experiments, which we describe in this section.
WTDとWTD_Hをオフライン実験で評価しましたので、本項で説明します。

## 5.1. Datasets データセット

We use two publicly available datasets: CoatShopping2 from the clothing domain [22] and Webscope R33 from the music domain [18].
我々は2つの一般に公開されているデータセットを使用する： CoatShopping2（衣服領域）[22]とWebscope R33（音楽領域）[18]である.
Both of them are ideal for our purposes because they are composed of two parts, one having MAR properties (Dmar = {O mar ,Y mar }), and the other having MNAR properties (Dmar = {O mnar ,Y mnar }).
**どちらもMAR特性を持つ部分（Dmar = {O mar ,Y mar }）とMNAR特性を持つ部分（Dmar = {O mnar ,Y mnar }）で構成されている**ので、今回の目的にはぴったりです。
For both of them, interactions are in the form of ratings, so that Y ∈ {1, 2, 3, 4, 5} U ×I .
両者ともインタラクションはratingという形で、Y∈{1,2,3,4,5}となるように。U ×I となる。
We consider a rating to be positive if it is above 3, and negative otherwise.
3以上の場合はポジティブ、それ以外の場合はネガティブと判断しています。
Both the Dmar parts are collected using the forced ratings approach described earlier, therefore they are almost but not completely unbiased, for the reasons we gave earlier.
D*{mar}パートは、いずれも前述のforced ratings approachで収集されているため、先に述べた理由により、ほぼ偏りのないものとなっています。
The Dmnar portions are collected during the operation of a recommender system.
D*{mnar}部分は、レコメンダーシステムの運用中に収集されます。
Note that we did mention earlier that we know of one other MAR-like dataset, collected by the forced ratings approach, namely cm100k from the music domain [4], but we cannot use this in our experiments because it does not have any corresponding MNAR data.
なお、forced ratings approachによって収集されたMAR類似のデータセットとして、音楽領域のcm100k [4]を知っていることを先に述べましたが、対応するMNARデータがないため、今回の実験では使用することはできません。F

For each dataset, we apply a preprocessing step to ensure both Dmar and Dmnar having a common user-item space U × I: specifically, we keep those users and items that belong to the intersection of the two portions.
各データセットについて、D_marとD_mnarが共通のユーザー・アイテム空間U×Iを持つように、前処理を施す.
Table 1 gives statistics of the final resulting datasets that we used in the experiments.
表1は、実験に使用した最終的な結果のデータセットの統計です。

## 5.2. Methodology 方法論

The goal of the experiments is to assess the ‘goodness’ of different ways of producing intervened test sets.
実験の目的は、介**入テストセットを作成するさまざまな方法の「良さ」を評価すること**です。
The measure of ‘goodness’ is how much results obtained by evaluating a recommender on an intervened test set resemble the results we would obtain on an unbiased test set.
「良さ」の指標は、介入したテストセットでレコメンダーを評価した結果が、偏りのないテストセットで得られるであろう結果にどれだけ似ているかということです。

In order to do that, in our experiments, we randomly splitO mnar in each dataset into a training set O t r and a heldout set O he with proportions 60%-40% respectively.
そのため、実験では、各データセットの$O^{mnar}$を訓練セット$O^{tr}$とホールドアウトセット$O^{he}$にそれぞれ60%～40%の割合でランダムに分割しました。
Since the split is random, MNAR distributions are preserved.
分割はランダムに行われるため、MNARの分布は保たれる。
For both of them, we take the corresponding ratings from Y mnar and we produce Y t r and Y he .
その両方について、Y*{mnar}から対応する評価を取り出し、Y*{tr}と$Y_{he}$を作成します。
Y he is what one would use as a traditional test set.
$Y_{he}$は、従来のテストセットとして使用されていたものです。
In our case, we use O he as the sampling space: we sample it to obtain intervened test sets.
我々の場合、**$O_{he}$をサンプリング空間として使用し、それをサンプリングして介在するテストセットを取得**します。
There is one intervened test set per sampling strategy (REG, SKEW, WTD, WTD\*H, explained in Section 5.3).
サンプリング戦略（REG、SKEW、WTD、WTD_H、5.3節で説明）ごとに1つの介在するテストセットがある。
We make the REG, SKEW, WTD, WTD_H intervened test sets to be 50% of the size of O he .
REG、SKEW、WTD、WTD_Hが介在するテストセットは、\*\*$O^{he}$の50%のサイズ\*\*になるようにする.
(Smaller values than 50% can result in intervened test sets that are too small to give reliable results; larger values than 50% can mean that intervened test sets are not appreciably different from O he .)
(50%より小さい値は、介在するテストセットが小さすぎて信頼できる結果が得られないことを意味し、50%より大きい値は、介在するテストセットが$O\_{he}$と有意な差がないことを意味する。)(この"50%"は経験的に得られた値なのかな...!)

We also randomly split O mar into three, i.e.O w , O val and O дt with proportions 15%-15%-70% respectively.
また、$O^{mar}$をランダムに3つ、すなわち$O^w$、$O^{val}$、$O^{gt}$にそれぞれ15%-15%-70%の割合で分割しました.
Since the split is random, MAR distributions are preserved.
分割はランダムに行われるため、MARの分布は保たれます。
We obtain Y w , Y val and Y дt accordingly, as before.
これに応じて、従来と同様に、Y w、Y val、Y дtを求める。
O w is used to calculate the weights for WTD (see Section 5.3 for more details of the calculation).
$O^{w}$は、WTDの重みの計算に使用される（計算の詳細は5.3節を参照）。
We use Y val as the validation set to optimize recommender system hyperparameter values (Section 5.4).
Y valを検証セットとして、レコメンダーシステムのハイパーパラメータ値を最適化する（5.4項）。
(In reality, the ratings one would use to optimize hyperparameter values would either be a portion of Y t r or a portion of an intervened test set produced from Y he .
(実際には，ハイパーパラメータ値を最適化するために使用する評価は，Y t r の一部か，Y he から生成される介在テストセットの一部であろう）．
We decided it was better in the experiments that we report in this paper to minimise the effect of hyperparameter selection on our results.
この論文で報告する実験では、ハイパーパラメータの選択が結果に与える影響を最小限に抑える方が良いと判断しました。
Hence, we selected hyperparameter values using ‘unbiased’ data, Y val .)
そこで、「不偏」データであるY val を用いてハイパーパラメータ値を選択した...。）(今回の実験ではサンプリング戦略を評価したいので...!!)(実際にはハイパーパラメータ調整にもMNARなデータを使う必要があるんだろうけど...!)

We use Y дt as an unbiased test set.
$Y^{gt}$を不偏のテストセットとして使用する。
In other words, the performance of a given recommender on Y дt can be considered to be its “true”, unbiased performance (the ground-truth).
つまり、$Y^{gt}$に対する推薦者の性能は、その「真の」不偏性能（ground-truth）であると考えることができる。
We want the performance of a recommender on an intervened test set to be close to its performance on this unbiased test set.
介在するテストセットでの推薦者の性能が、この偏りのないテストセットでの性能に近くなることを望んでいるのです。
The best intervention strategy is the one that produces test sets where performance most closely resembles performance on Y дt .
**最適な介入戦略は、性能が$Y^{gt}$の性能に最も近いテストセット$Y^{S-hogehoge}$を作成するもの**である。

We train the five recommender systems presented in Section 5.4 using ratings in Y t r .
$Y^{tr}$ のratingを用いて、5.4 節で紹介した 5 つの推薦システムを学習させる.
Each recommender produces a ranked list of recommendations which are tested on the unbiased test set Y дt and the intervened test sets.
各推薦システムは、推薦結果(ランク付けされたリスト)を生成し、非バイアスのテストセット$Y^{gt}$とintervened test setsでテストされる.
We have computed Precision, Recall, MAP and NDCG on the top-10 recommendations.
**トップ10のレコメンデーション**について、Precision、Recall、MAP、NDCGを算出した.
Results are averaged over 10 runs with different random splits.
結果は、異なるランダム分割で10回実行した平均値です.

## 5.3. Sampling strategies サンプリング戦略

We formally present here the sampling strategies that we use to produce the intervened test sets in our experiments.
ここでは、実験にてintervened test setsを作成するために使用するサンプリング戦略を正式に紹介する.
Each strategy samples an intervened test setO S from O he (and the corresponding ratings from Y he , i.e.Y S ).
各戦略は、$O^{he}$から介在するテストセット$O^{S}$をサンプリングする(そして、$Y^{he}$から$O^{s}$に対応するrating、すなわち、$Y^{S}$ をサンプリングする).
For each strategy we give the corresponding probability sampling distribution, i.e.PS (S|u,i).
各戦略に対応する確率サンプリング分布、すなわち$P_{S}(\mathcal{S}|u,i)$ を与える.
In addition to SKEW, WTD and WTD_H, we also employ two baselines.
**SKEW、WTD、WTD_H に加えて、2 つのベースライン(REGとFULL)を採用**しています。
REG is a random sample from O he , corresponding to an intervention that does not try to compensate for bias.
REGは、偏りを補正しようとしないinterventionに対応する、$O^{he}$からのランダムなサンプルである。
FULL represents the classical test set generation in the evaluation, where the test set is O he (therefore no intervention).
FULLは、評価における古典的なテストセット生成を表し、テストセットは$O^{he}$(したがってinterventionなし)である.

- FULL: $P_S(\mathcal{S}|u,i) = 1$ so that $O^{he}$ is fully sampled and no intervention is performed.

- REG: $P_S(\mathcal{S}|u,i) = 1/|O^{he}|$. Every (u,i) has a constant probability to be sampled and we obtain a test set that is a random subset ofO he . We would expect this to behave very similarly to FULL. すべての (u,i) は一定の確率でサンプリングされ、$O^{he}$ のランダムな部分集合であるテストセットが得られます。 **FULLと非常に似た挙動になることが予想されます**。

- SKEW: $P_S(\mathcal{S}|u,i) = 1/pop(i)$, where $pop(i)$ counts the number of ratings that item $i$ has in $O^{tr}$ [3, 27].

- WTD, WTD*H: $P_S(\mathcal{S}|u,i) = w*{u}(w\_{i})^2$ . These are the two alternatives of our approach, presented in Sections 4.2 and 4.3. Weights are calculated using formulas 13 and 14. WTD uses formulas 1 and 2 to calculate the actual MAR posteriors from O w . WTD_H uses the hypothesized MAR posteriors instead. They both use formulas 4 and 5 to calculate exact MNAR posteriors from $O^{tr}$.これらは、4.2節と4.3節で紹介した我々のアプローチの2つの選択肢です。重みは、数式13と14を用いて計算します。 WTD は，式 1 と式 2 を用いて，$O^w$ から実際の MAR 事後分布を計算する． WTD_Hは、代わりに仮説のMAR 事後分布を使用します。 両者とも数式4と5を用いて、$O^{tr}$ から正確なMNARの事後分布を計算する。

Note that, in each of SKEW, WTD and WTD_H, if the distribution PS does not sum to 1 (necessary for a probability distribution), we include a normalization step on PS to ensure that this property is achieved.
**なお、SKEW、WTD、WTD_Hのそれぞれにおいて、分布$P_S$の和が1にならない場合(確率分布として必要な性質)、この性質が得られるようにPSの正規化ステップを含むようにしている**.

## 5.4. Recommender systems

We train five recommender models, all of them producing a ranked list of recommended items.
5つのレコメンダーモデルを学習し、すべてのモデルが推薦アイテムのランク付けリストを生成する.(AvgRating, PosPop, UB_KNN, IB_KNN, MF)
AvgRating and PosPop are non-personalized recommenders which rank items in descending order of their mean rating and number of positive ratings in the training set, respectively.
AvgRating と PosPop は、それぞれトレーニングセットにおける平均評価とポジティブ評価の数の降順でアイテムをランク付けする**非個人化レコメンダー**です。
UB_KNN and IB_KNN are user-based and item-based nearest-neighbour algorithms [8].
UB_KNNとIB_KNNは、ユーザベースとアイテムベースの**最近傍アルゴリズム**です[8]。
MF is the Matrix Factorization algorithm proposed by Pilaszy and Tikk [20].
MFはPilaszy and Tikk [20]が提案したMatrix Factorizationアルゴリズムです。
For UB_KNN, IB_KNN and MF we use the implementations available in the RankSys library4 .
UB_KNN、IB_KNN、MFについては、**RankSysライブラリ**で利用可能な実装を使用しています。
We used our own implementations of AvgRating and PosPop.
AvgRatingとPosPopは独自に実装したものを使用しました。

The UB_KNN, IB_KNN and MF algorithms have hyperparameters.
UB_KNN、IB_KNN、MFの各アルゴリズムはハイパーパラメータを持つ. (実験においてどのハイパーパラメータ設定を使用するか、という話.)
We select hyperparameter values that maximize Recall for top10 recommendations on Y val (Section 5.2).
$Y^{val}$のトップ10レコメンデーションのRecallを最大化するハイパーパラメータ値を選択する(セクション5.2)
For UB_KNN, IB_KNN, we choose the number of neighbors from {10, 20, .., 100}.
UB_KNN, IB_KNNについては、{10, 20, ..., 100}の中から近傍数kを選択する。
For MF, we choose the number of latent factors from {20, 40, .., 200} and the regularization term from {0.001, 0.006, 0.01, 0.06, 0.1, 0.6}.
MFでは、潜在因子数を{20, 40, ..., 200}から、正則化項を{0.001, 0.006, 0.01, 0.06, 0.1, 0.6} から選択した。

# 6. Results 結果

We report the results of our experiments in Table 2.
実験結果を表2に報告する.
For each recommender, we show its ground-truth Recall@10 performance on the unbiased test set Y дt and the relative performance (in terms of percentage difference) for the baselines and intervened test sets with respect to this ground-truth.
各レコメンダーについて、バイアスのかかっていないテストセットY дtに対するグランドトゥルースのRecall@10性能と、このグランドトゥルースに対するベースラインと介在するテストセットの相対性能（差分百分率）を示す。
Results for Precision, NDCG and MAP are omitted because the percentage differences are very similar to the Recall ones.
Precision、NDCG、MAPの結果は、Recallとほぼ同じ割合の差であるため、省略した。

Results for CoatShopping show that the baselines and all intervened test sets overestimate ground-truth performances for all recommenders with just one exception: PopPos on WTD_H.
CoatShoppingの結果は、ベースラインと介入したすべてのテストセットが、1つの例外を除いて、すべての推薦者の真実のパフォーマンスを過大評価することを示しています： WTD_HのPopPosです。
In general, our new approaches are superior in approximating groundtruth performances.
一般に、我々の新しいアプローチは、真実の性能を近似するのに優れています。
WTD is very close for non-personalized recommenders performances, while WTD_H is the best for the personalized ones.
WTDは非パーソナライズド推薦者の性能に非常に近く、WTD_Hはパーソナライズド推薦者の性能に最も優れている。
Although both of them outperform all the other strategies, WTD_H would probably be the best choice due to its ‘balance’, i.e.its percentage differences are not more than around 50% from the ground-truth for all the recommenders except MF, which anyway has the best approximation on WTD_H among all the strategies.
WTD_Hは、MFを除くすべてのレコメンダーにおいて、その「バランス」、すなわち、グランドトゥルースとの差の割合が約50%以下であることから、おそらく最良の選択となるであろう(MFは、すべての戦略の中でWTD_Hに最も近似している)

Results on Webscope R3 show something slightly different.
Webscope R3での結果では、少し違うことがわかります。
First of all, for the AvgRating recommender, ground-truth performances are underestimated by all strategies.
まず、AvgRatingレコメンダーでは、すべての戦略で真実の性能が過小評価されていることがわかる。
For this recommender, SKEW, WTD and WTD_H are equally good, but superior to FULL and REG anyway.
このレコメンダーでは、SKEW、WTD、WTD_Hは同等だが、とにかくFULLとREGより優れている。
We then find SKEW superior to WTD and WTD_H for the PosPop recommender.
そして、PosPopレコメンダーでは、SKEWがWTDやWTD_Hよりも優れていることがわかりました。
But WTD and WTD_H are better for the personalized recommenders.
しかし、パーソナライズド・レコメンダーではWTDとWTD_Hの方が優れています。
This fact is expected to some extent because SKEW is a popularity-bias specific intervention strategy.
この事実は、SKEWが人気バイアスに特化した介入戦略であることから、ある程度予想されることではある。
Comparing only WTD and WTD_H, we find that both are close to each other, but we also find that the former more closely approximates the ground truth for PosPop, UB_KNN and IB_KNN, while the latter does it for MF and AvgRating (but slightly in this case).
WTDとWTD_Hだけを比較すると、どちらも近いことがわかりますが、PosPop、UB_KNN、IB_KNNでは前者がよりグランドトゥルースに近いことがわかり、MFとAvgRatingでは後者がより近い（ただしこの場合は若干）ことがわかりました。

Finally, FULL and REG are very far from the ground-truth, showing that ‘intelligent’ intervention strategies (such as SKEW, WTD and WTD_H) provide an effective debiasing technique in offline evaluations.
最後に、FULLとREGは、グランドトゥルースから非常に離れており、「インテリジェント」介入戦略（SKEW、WTD、WTD_Hなど）は、オフライン評価において効果的なデビアス手法を提供することを示している。
Indeed, FULL and REG have very similar results, regardless of the fact that REG is 50% smaller in size.
実際、FULLとREGは、REGの方がサイズが50％小さいという事実にもかかわらず、非常によく似た結果となっています。
This means that what matters is the strategy that performs the sampling, rather than the sampling itself.
**つまり、重要なのはサンプリングする事そのものではなく、"いかにサンプリングを行うか"という戦略(というか意思決定?)なのです。**

Table 3 reports an additional investigation on the results of Table 2.
表3は、表2の結果に対する追加調査の報告である。
An offline evaluation typically ranks recommender algorithms from best to worst.
オフライン評価では、通常、レコメンダーアルゴリズムをベストからワーストにランク付けします。
This helps to narrow the number of different recommender algorithms that needs to be evaluated in costly user trials and online experiments.
これにより、コストのかかるユーザートライアルやオンライン実験で評価する必要のある、さまざまなレコメンダーアルゴリズムの**数を絞ることができます。**
In our case then, it is important that performance estimates on intervened test sets, not only get close to the ground truth performance, but also rank different recommenders in the same way they would be ranked by performance estimates on the unbiased test set.
この場合、介在するテストセットでの性能推定が、真実の性能に近いだけでなく、公平なテストセットでの性能推定によってランク付けされるのと同じように、異なるレコメンダーをランク付けすることが重要である。
We use Kendall’s concordance coefficient (τ ) to compare the ground truth recommender ranking obtained on the unbiased test set with the ones produced by the different interventions.
Kendallの一致係数(τ)を用いて、偏りのないテストセットで得られた真実の推薦者ランキングと、異なる介入によって生成されたランキングを比較する。

The τ values on CoatShopping are far from the maximum possible value (i.e.τ = 1).
CoatShoppingのτ値は、最大値（τ＝1）からは程遠い値です。
Also, in this case, ‘intelligent’ intervention seems to harm the concordance coefficient: SKEW, WTD and WTD_H have lower values (τ = 0) than FULL and REG (τ = 0.2).
また、この場合、「インテリジェント」な介入は、コンコーダンス係数を害するようである： SKEW、WTD、WTD_Hは、FULL、REG（τ=0.2）よりも低い値（τ=0）になっています。
For Webscope, the τ values are much closer to 1.
Webscopeの場合、τ値は1にかなり近い値になっています。
Also, the ‘intelligent’ intervention strategies improve the τ values (τ = 0.8) over the baseline ones (τ = 0.6).
また、「インテリジェント」な介入戦略は、ベースラインのもの（τ＝0.6）よりもτ値を向上させている（τ＝0.8）。
The concordance coefficients for CoatShopping seem to advise against using ‘intelligent’ intervention approaches such as SKEW, WTD or WTD_H.
CoatShoppingのコンコーダンス係数は、SKEW、WTD、WTD_Hのような「インテリジェント」な介入アプローチを使用しないことを勧めているようです。
However, we note that τ values are subject to great variability, depending on the set of recommenders being compared.
しかし、τの値は、**比較する推薦モデルの集合によって、大きく変動する**ことに注意する。
In fact, simply dropping the MF model from the comparison, we get very different τ values; see Table 4.
実際、MFモデルを比較対象から外しただけで、τの値が大きく異なることがわかる；表4参照。
Now τ values for Webscope are all the same (τ = 0.68).
これでWebscopeのτ値はすべて同じ（τ＝0.68）になりました。
But we have a completely different scenario for CoatShopping: SKEW, WTD and WTD_H improve concordance (from τ = 0 to τ = 0.7) and they outperform FULL and REG (which slightly improve from τ = 0.2 to τ = 0.3).
しかし、CoatShoppingでは全く異なるシナリオが描かれています： SKEW、WTD、WTD_Hは、コンコーダンス（τ=0からτ=0.7へ）を改善し、FULLとREG（τ=0.2からτ=0.3へわずかに改善）を上回りました。
Low τ values for CoatShopping in Table 3 are a consequence of the fact that all test sets incorrectly rank MF to be one of the best-performing models, while it is the worst according to the ground truth.
**表3のCoatShoppingのτ値が低いのは、すべてのテストセットで、MFを最も性能の良いモデルの1つと誤認した結果であり、真実では最も悪いモデルである**。

# 7. Conclustions コンクルージョン

In this paper, we presented new sampling strategies that generate intervened test sets with MAR-like properties from MNAR data.
本論文では、MNARデータからMAR的な性質を持つ介在テストセットを生成する新しいサンプリング戦略を提示した。
These intervened test sets are therefore more suitable for approximating the performance of a recommender on unbiased test data.
したがって、これらの介在するテストセットは、偏りのないテストデータにおけるレコメンダーの性能を近似するのに適している。
One of the sampling strategies, WTD, requires that some MAR-like data be available since it approximates posterior probabilities calculated from that data.
サンプリング戦略の1つであるWTDは、そのデータから計算される事後確率を近似するため、MARのようなデータがあることが必要です。
The other strategy, WTD_H, approximates the probabilities that we expect MAR data to exhibit.
もう一つのストラテジーであるWTD_Hは、MARデータが示すと予想される確率を近似するものです。

The paper assesses the effectiveness of these two strategies and it assesses, for the first time, the effectiveness of an existing intervention strategy from the literature, namely SKEW, which samples in inverse proportion to item popularity.
本論文では、これら2つの戦略の有効性を評価するとともに、文献にある既存の介入戦略、すなわちアイテムの人気度に反比例してサンプリングするSKEWの有効性を初めて評価した。
With the use of an essentially unbiased test set as a ground-truth, we showed these three sampling approaches to be successful in mitigating the biases found in a classical random test set.
偏りのないMARテストセットをground-truthとして使用することで、これら3つの**サンプリングアプローチが、古典的なランダムテストセットに見られるバイアスを軽減することに成功することを示しました**。
We found SKEW to be particularly good at reducing the bias for a popularity-based recommender (which is related to the popularity bias of the items for which SKEW was designed).
SKEWは、特に人気度ベースのレコメンダーのバイアス（これはSKEWが設計されたアイテムの人気度のバイアスに関係している）を低減するのに優れていることがわかった。
But our new strategies are the most robust across various recommenders since they most closely approximate the unbiased ground-truth performances.
しかし、**我々の新しい戦略は、バイアスのかかっていないground-truthのパフォーマンスに最も近いため、様々な推薦モデルにおいて最も堅牢(robust)**である。
The WTD strategy requires MAR data, which is rarely available, but we found that WTD_H, which uses a hypothesized MAR distribution, does work well, so MAR data is not necessary.
WTD戦略ではMARデータが必要で、その入手は稀ですが、**仮説のMAR分布を使うWTD_Hが上手く機能する事わかったので、MARデータは必要ありません。**

Our approach brings several intrinsic benefits.
私たちのアプローチは、いくつかの本質的な利点をもたらします。
First of all, it enjoys low overheads.
まず、オーバーヘッド(事業を営むのにかかる経常的な費用)が少ないことがあげられます。

- Its design is simple and easy to implement and it does not require any learning phase for the weights, contrary to some unbiased estimators which might require expensive learning (e.g. [22], where propensities are found via logistic regression). その**設計はシンプルで実装が容易**であり、高価な学習を必要とする可能性のあるいくつかの不偏推定器（例えば[22]、propensityはロジスティック回帰によって求められる）とは逆に、重みのための学習段階を必要としない。

- Moreover, intervention reduces the computational costs of testing a recommender because it generates smaller test sets. さらに、介入はより小さなテストセットを生成するため、推薦モデルのオフラインテストにかかる計算コストを削減することができます。(オフラインテストってそんな計算コストかかるイメージないけど、どうなんだろう...! 学習だったら計算コスト下げられそう...!)

Another advantage of our approach is that it has high generality.
また、本アプローチのもう一つの利点は、**高い汎用性**を持っていることです。

- It works for both implicit and explicit datasets because it is independent of the interaction values (e.g. ratings) in the dataset. **データセット中の相互作用値(例えば評価)に依存しないため、暗黙的なデータセットでも明示的なデータセットでも機能します**。

- Despite the fact that WTD and WTD_H are very close to SKEW, our way of calculating weights is less heuristic than the one of SKEW and, unlike SKEW, it is not tailored to item popularity bias. WTD と WTD_H は SKEW に非常に近いにもかかわらず、我々の重みの計算方法は SKEW のものよりも発見的でなく、SKEW とは異なり、アイテムの人気バイアスに合わせたものではありません。

- It can be extended to training a recommender, without any modification. Training a recommender on an intervened training set instead of on a classical biased training set, might improve the recommender’s model and therefore boost prediction or ranking performances. For this reason, at the time of writing we are investigating using our approach to debias training sets to complement this work on debiasing test sets. **そのままレコメンダーの学習に拡張することも可能**です。 従来の偏った訓練セットではなく、介入した訓練セットでレコメンダーを訓練することで、レコメンダーのモデルが改善され、予測やランキングの性能が向上する可能性があります。 このため、本稿執筆時点では、テストセットのデビアスに関するこの作業を補完するために、トレーニングセットのデビアスに関する我々のアプローチを使用することを検討しています。

- Intervened data can be used to train existing recommender systems and to test recommender systems using existing metrics. Debiased training and testing hence become widely applicable without designing special models and special metrics. 介入されたデータは、既存のレコメンダーシステムのトレーニングや、既存のメトリクスを用いたレコメンダーシステムのテストに使用することができます。 そのため、**特別なモデルや指標を設計することなく、偏ったトレーニングやテストが広く適用できるようになります**。

Apart from the use of our approach for training a recommender, our aim for the future is to investigate other ways of calculating the weights for the sampling.
レコメンダーのトレーニングに本アプローチを使用する以外にも、サンプリングの重みを計算する他の方法を調査することが今後の目標です。
An alternative might be using techniques developed for causal inference, e.g.[1, 6, 7].
別の方法として、因果推論用に開発された技術（例：[1, 6, 7]）を使用することもできるだろう。
