## link

- https://arxiv.org/pdf/1901.07555.pdf? httpsを使用しています。

- [後処理による人気アイテムの“格下げ”で確保する推薦多様性](https://takuti.me/ja/note/reranking-for-popularity-bias/) [Diversity of recommendations secured by "downgrading" popular items through post-processing](https:

## abstruct abstruct

Many recommender systems suffer from popularity bias: popular items are recommended frequently while less popular, niche products, are recommended rarely or not at all.
多くのレコメンダーシステムは、人気のある商品は頻繁に推薦され、人気のないニッチな商品はほとんど推薦されないか、まったく推薦されないという人気度バイアスに悩まされている。
However, recommending the ignored products in the “long tail” is critical for businesses as they are less likely to be discovered.
しかし、「ロングテール」にある無視された商品を推薦することは、発見される可能性が低いため、ビジネスにとって重要である。
In this paper, we introduce a personalized diversification re-ranking approach to increase the representation of less popular items in recommendations while maintaining acceptable recommendation accuracy.
本論文では、許容できる推薦精度を維持しながら、推薦における人気のない商品の表現力を高めるために、パーソナライズされた多様化再順位付けアプローチを紹介する。
Our approach is a post-processing step that can be applied to the output of any recommender system.
**本アプローチは、あらゆる推薦システムの出力に適用可能な後処理ステップ**である。
We show that our approach is capable of managing popularity bias more effectively, compared with an existing method based on regularization.
我々は、正則化に基づく既存の手法と比較して、我々のアプローチが人気度バイアスをより効果的に管理できることを示す。
We also examine both new and existing metrics to measure the coverage of long-tail items in the recommendation.
また，推薦におけるロングテール項目の網羅性を測定するために，新しい指標と既存の指標の両方を検討する．

# title タイトル

Managing Popularity Bias in Recommender Systems with Personalized Re-ranking
推薦システムにおける人気度バイアスをパーソナライズされた再順位付けにより管理する方法

## Introduction イントロダクション

Recommender systems have an important role in e-commerce and information sites, helping users find new items.
電子商取引や情報サイトでは，ユーザが新しい商品を見つけるのを支援するレコメンダーシステムが重要な役割を担っている．
One obstacle to the effectiveness of recommenders is the problem of popularity bias [6]: collaborative filtering recommenders typically emphasize popular items (those with more ratings) over other “long-tail” items [16] that may only be popular among small groups of users.
レコメンダーが有効であるための一つの障害は、人気度バイアス [6] の問題である。協調フィルタリングによるレコメンダーは、一般的に、少数のユーザーグループにしか人気がないかもしれない他の「ロングテール」アイテム [16] に対して、人気のあるアイテム（より多くの評価を得たもの）を強調する。
Although popular items are often good recommendations, they are also likely to be well-known.
人気のあるアイテムは良いレコメンデーションであることが多いのですが、有名である可能性も高いです。
So delivering only popular items will not enhance new item discovery and will ignore the interests of users with niche tastes.
そのため、人気のあるアイテムだけを配信することは、新しいアイテムの発見を促進せず、ニッチな嗜好を持つユーザーの興味を無視することになる。
It also may be unfair to the producers of less popular or newer items since they are rated by fewer users.
また、人気のないアイテムや新しいアイテムは、より少ないユーザーによって評価されるため、製作者にとって不公平になる可能性がある。

![Figure 1: The long-tail of item popularity. ](https://d3i71xaburhd42.cloudfront.net/6d77d7467f993780d02f3d8ea563959643d48f89/1-Figure1-1.png)

Figure 1 illustrates the long-tail phenomenon in recommender systems.
図1は、レコメンダーシステムにおけるロングテール現象を説明するための図である。
The y axis represents the number of ratings per item and the x axis shows the product rank.
Y軸は項目ごとの評価数、X軸は商品ランクを表している。
The first vertical line separates the top 20% of items by popularity – these items cumulatively have many more ratings than the 80% tail items to the right.
最初の縦線は、人気順で上位20%の項目を分けている。これらの項目は、右側の80%テールの項目よりも累積で多くの評価を受けている。
These “short head” items are the very popular items, such as blockbuster movies in a movie recommender system, that garner much more viewer attention.
これらの「ショートヘッド」アイテムは、映画推薦システムにおけるブロックバスター映画のような、視聴者の注目を集める非常に人気の高いアイテムです。
Similar distributions can be found in other consumer domains.
同様の分布は、他の消費者領域でも見られる。

The second vertical line divides the tail of the distribution into two parts.
2本目の縦線は、分布の尾を2つに分けています。
We call the first part the long tail: these items are amenable to collaborative recommendation, even though many algorithms fail to include them in recommendation lists.
最初の部分をロングテールと呼びます。これらの項目は、多くのアルゴリズムが推薦リストに含めないにもかかわらず、協調的推薦が可能な項目です。
The second part, the distant tail, are items that receive so few ratings that meaningful cross-user comparison of their ratings becomes unreliable.
一方、「遠いテール」と呼ばれるのは、評価が非常に少なく、ユーザー間の比較が困難なアイテムです。
For these cold-start items, content-based and hybrid recommendation techniques must be employed.
このようなコールドスタート商品に対しては、コンテンツベースやハイブリッド型の推薦技術を採用しなければならない。
Our work in this paper is concerned with collaborative recommendation and therefore focuses on the long-tail segment.
本稿では、協調推薦に関する研究であるため、ロングテール区分に注目する。

We present a general and flexible approach for controlling the balance of item exposure in different portions of the item catalog as a post-processing phase for standard recommendation algorithms.
我々は、標準的な推薦アルゴリズムの後処理段階として、アイテムカタログの異なる部分におけるアイテム露出のバランスを制御するための一般的で柔軟なアプローチを提示する。
Our work is inspired by [18] where authors introduced a novel probabilistic framework called xQuAD for Web search result diversification which aims to generate search results that explicitly account for various aspects associated with an under-specified query.
我々の研究は、著者らがウェブ検索結果の多様化のために**xQuAD**と呼ばれる新しい確率的フレームワークを導入した[18]に触発されたもので、これは、指定されないクエリに関連する様々な側面を明示的に考慮した検索結果を生成することを目的としている。
We adapt the xQuAD approach to the popularity bias problem.
我々はxQuADのアプローチを人気度バイアス問題に適応させる。
Our approach enables the system designer to tune the system to achieve the desired trade-off between accuracy and better coverage of long-tail, less popular items.
本アプローチにより、システム設計者は、精度とロングテールかつ人気のない項目をより良くカバーすることの間の望ましいトレードオフを達成するためにシステムを調整することができる。

# Related work 関連作品

Recommending serendipitous items from the long tail is generally considered to be a key function of recommendation [5], as these are items that users are less likely to know about.
ロングテールからセレンディピティを推薦することは、一般に推薦の重要な機能であると考えられている[5]。
Authors in [7] showed that 30-40% of Amazon book sales are represented by titles that would not normally be found in brick-and-mortar stores.
7]の著者は、Amazonの書籍売上の30-40%は、通常実店舗で見つけられないようなタイトルで占められていることを示した。

Long-tail items are also important for generating a fuller understanding of users’ preferences.
ロングテール項目は、ユーザーの嗜好をより深く理解するためにも重要です。
Systems that use active learning to explore each user’s profile will typically need to present more long tail items because these are the ones that the user is less likely to know about, and where user’s preferences are more likely to be diverse [17].
アクティブラーニングを利用して各ユーザーのプロファイルを探索するシステムでは、一般的に、より多くのロングテール項目を提示する必要があります。これらは、ユーザーがあまり知らない項目であり、ユーザーの嗜好が多様である可能性が高いからです[17]。

Finally, long-tail recommendation can also be understood as a social good.
最後に、ロングテール推薦も社会的な善と理解することができる。
A market that suffers from popularity bias will lack opportunities to discover more obscure products and will be, by definition, dominated by a few large brands or well-known artists [11].
人気バイアスに苦しむ市場は、より無名な商品を発見する機会に欠け、定義上、少数の大きなブランドや有名なアーティストに支配されることになる [11]。
Such a market will be more homogeneous and offer fewer opportunities for innovation and creativity.
このような市場は同質性が高く、革新性や創造性を発揮する機会が少なくなる。

The idea of the long-tail of item popularity and its impact on recommendation quality has been explored by some researchers [7, 16].
項目人気のロングテールという考え方と、それが推薦品質に与える影響については、いくつかの研究者によって検討されてきた[7, 16]。
In those works, authors tried to improve the performance of the recommender system in terms of accuracy and precision, given the long-tail in the ratings.
これらの研究において，著者らは評価におけるロングテールを考慮して，推薦システムの性能を精度と正確さの観点から向上させようとした．
Our work, instead, focuses on reducing popularity bias and balancing the representation of items across the popularity distribution.
本論文では，人気度バイアスを低減し，人気度分布の中で項目の表現のバランスをとることに焦点をあてる．

A regularization-based approach to improving long tail recommendations is found in [2].
ロングテール推薦を改善する正則化ベースのアプローチは[2]にあります。
One limitation with that work is that this work is restricted to factorization models where the long-tail preference can be encoded in terms of the latent factors.
この研究の限界は、ロングテールの嗜好が潜在的な要因の観点から符号化できる因子分解モデルに限定されていることである。
In contrast, a re-ranking approach can be applied to the output of any algorithm.
これに対して、再順位付けのアプローチは、任意のアルゴリズムの出力に適用することができる。
Another limitation of that work is that it does not account for user tolerance towards long-tail items: the fact that there may be some users only interested in popular items.
この研究のもう一つの限界は、ロングテール項目に対するユーザの耐性、つまり、**人気のある項目だけに興味を持つユーザが存在する可能性を考慮していない**ことである。
In our model, we take personalization of long-tail promotion into account as well.
我々のモデルでは、**ロングテールプロモーションのパーソナライズ**も考慮に入れている。

And finally, there is substantial research in recommendation diversity, where the goal is to avoid recommending too many similar items [10, 23, 24].
そして最後に、レコメンデーションダイバーシティの研究も盛んで、類似したアイテムをあまり多く推薦しないことが目標とされています [10、23、24]。
Personalized diversity is also another related area of research where the amount of diversification is dependent on the user’s tolerance for diversity [12, 21].
また，パーソナライズされた多様性も関連する研究分野であり，多様性の量はユーザーの多様性に対する耐性に依存します [12, 21]．
Another similar work to ours is [20] where authors used a modified version of xQuAD called relevance based xQuAD for intent-oriented diversification of search results and recommendations.
私たちと似たような研究として[20]があり、著者らは検索結果と推薦の意図指向の多様化のために関連性ベースのxQuADと呼ばれるxQuADの修正版を使用しています。
Another work used a similar approach but for fairness-aware recommendation [14] where xQuAD was used to make a fair representation of items from different item providers.
この研究では、異なるアイテムプロバイダーからのアイテムの公正な表現を行うためにxQuADが使用されました。
Our work is different from all these previous diversification approaches in that it is not dependent on the characteristics of items, but rather on the relative popularity of items.
我々の研究は、アイテムの特性に依存せず、むしろアイテムの相対的な人気度に依存するという点で、これら全ての過去の多様化アプローチと異なっている。

# CONTROLLING POPULARITY BIAS xQuAD ♪大衆性バイアスを制御する xQuAD

Result diversification has been studied in the context of information retrieval, especially for web search engines, which have a similar goal to find a ranking of documents that together provide a complete coverage of the aspects underlying a query [19].
結果の多様化は情報検索の文脈で研究されており、特にウェブ検索エンジンでは、クエリの根底にある側面を完全にカバーする文書のランキングを一緒に見つけるという類似の目標があります[19]。
EXplicit Query Aspect Diversification (xQuAD) [18] explicitly accounts for the various aspects associated with an under-specified query.
EXplicit Query Aspect Diversification (xQuAD) [18]は、指定されないクエリに関連する様々なアスペクトを明示的に考慮するものである。
Items are selected iteratively by estimating how well a given document satisfies an uncovered aspect.
与えられた文書がカバーされていないアスペクトをどの程度満たしているかを推定することにより、項目が反復的に選択される。

In adapting this approach, we seek to recognize the difference among users in their interest in long-tail items.
この手法を応用することで、ロングテール商品に対するユーザーの関心の違いを認識することを目指した。
Uniformly-increasing diversity of items with different popularity levels in the recommendation lists may work poorly for some users.
推薦リストにおいて、人気度の異なるアイテムの多様性を一律に高めることは、一部のユーザにとってうまく機能しない可能性がある。
We propose a variant that adds a personalized bonus to the items that belong to the underrepresented group (i.e. the long-tail items).
我々は、人気度の低いグループに属するアイテム（すなわち、ロングテール・アイテム）にパーソナライズド・ボーナスを追加する変形を提案する。
The personalization factor is determined based on each user’s historical interest in long-tail items.
パーソナライズ係数は、各ユーザのロングテール項目に対する過去の興味に基づいて決定される。

# Methodology メソドロジー

We build on the xQuAD model to control popularity bias in recommendation algorithms. We assume that for a given user u, a ranked recommendation list R has already been generated by a base recommendation algorithm. The task of the modified xQuAD method is to produce a new re-ranked list $S$ ($|S| < |R|$) that manages popularity bias while still being accurate.
我々は、推薦アルゴリズムにおける人気度バイアスを制御するために、xQuADモデルを構築する。与えられたユーザーuに対して、ランク付けされた推薦リストRがベース推薦アルゴリズムによって既に生成されていると仮定する。修正xQuAD法のタスクは、正確でありながら人気の偏りを管理する新しい再順位付けリスト$S$（$|S| < |R|$）を生成することである。

The new list is built iteratively according to the following criterion:
新しいリストは、以下の基準に従って繰り返し構築される。

$$
P(v|u) + \lambda P(v, S'|u) \tag*{1}
$$

where $P(v|u)$ is the likelihood of user $u \in U$ being interested in item $v \in V$ , independent of the items on the list so far as, predicted by the base recommender. The second term $P(v, S'|u)$ denotes the likelihood of user $u$ being interested in an item $vS$ as an item not in the currently generated list $S$.
ここで、$P(v|u)$は、ユーザ$u \in U$が、ベース・レコメンダーによって予測された、これまでのリスト上のアイテムとは独立に、$V$内のアイテム$v \に興味を持つ尤度である。第2項$P(v, S'|u)$は、ユーザー$u$が現在生成されているリスト$S$にないアイテム$v$に興味を持つ尤度である。

Intuitively, the first term incorporates ranking accuracy while the second term promotes diversity between two different categories of items (i.e. short head and long tail).
直感的には、第1項はランキング精度を、第2項は2つの異なるカテゴリのアイテム（すなわち、ショートヘッドとロングテール）間の多様性を促進する。
The parameter λ controls how strongly controlling popularity bias is weighted in general.
パラメータλは、一般に人気度バイアスをどの程度強く制御するかを制御する。
The item that scores most highly under the equation 1 is added to the output list S and the process is repeated until S has achieved the desired length.
式1のもとで最も高いスコアを得た項目が出力リストSに追加され、Sが所望の長さになるまでこの処理が繰り返される。

To achieve more diverse recommendation containing items from both short head and long tail items, the marginal likelihood $P(v, S′|u)$ over both item categories long-tail head ($\Gamma$) and short head ($\Gamma'$) is computed by:
短頭種と長尾種のアイテムを含むより多様な推薦を実現するために、長尾種($Gamma$)と短尾種($Gamma'$)の両方のアイテムカテゴリに対する周辺尤度$P(v, S′|u)$ を以下のように計算する。

$$
P(v, S'|u) = \sum_{d \in {\Gamma, \Gamma'}} P(v, S'|d) P(d|u)
\tag{2}
$$

($d$: $\Gamma$ or $\Gamma'$...??, $v \in d$という条件でのP(v,S'))

Following the approach of [18], we assume that the remaining items are independent of the current contents of S and that the items are independent of each other given the short head and long tail categories. Under these assumptions, we can compute $P(v, S′|d)$ in Eq.2 as
[18]のアプローチに従い、残りのアイテムは$S$の現在の内容から独立しており、short-headとlong-tailのカテゴリが与えられているアイテムは互いに独立していると仮定します.(i.e. $\Gamma$と$\Gamma'$は重複していない!!)
これらの仮定の下で、式.2の$P(v, S′|d)$を次のように計算することができます.

$$
P(v, S'|d) = P(v|d) P(S'|d) = P(v|d) \Pi_{i \in S} (1 - P(i|d, S))
\tag{3}
$$

By substituting equation 3 into equation 2, we can obtain
式3に式2を代入することにより

$$
score = (1 - \lambda)P(v|u)+\lambda \sum_{c \in {\Gamma, \Gamma'}} P(c|u) P(v|c) \Pi_{i \in S} (1 - P(i|c, S))
\tag{4}
$$

where $P(v|d)$ is equal to 1 if $v \in d$ and 0 otherwise.
ここで$P(v|d)$は、$v \in d$の場合は1, そうでない場合は0

We measure $P(i|d, S)$ in two different ways to produce two different algorithms. The first way is to use the same function as $P(v|d)$, an indicator function where it equals to 1 when item i in list S already covers category d and 0 otherwise. We call this method Binary xQuAD and it is how original xQuAD was introduced. Another method that we present in this paper is to find the ratio of items in list S that covers category d. We call this method Smooth xQuAD.
P(i|d, S)$を2つの異なる方法で測定し、2つの異なるアルゴリズムを作成します.
最初の方法は$P(v|d)$と同じ関数で、リストSのアイテムiが既にカテゴリdをカバーしているとき1に等しく、それ以外は0となる指標関数を使用する方法である。この方法はバイナリxQuADと呼ばれ、オリジナルのxQuADはこの方法で導入された。本論文で紹介するもう一つの方法は、リストS中の項目がカテゴリdをカバーしている比率を求める方法である。

The likelihood $P(d|u)$ is the measure of user preference over different item categories. In other words, it measures how much each user is interested in short head items versus long tail items. We calculate this likelihood by the ratio of items in the user profile which belong to category d.
尤度 $P(d|u)$ は、**異なるアイテム・カテゴリに対するユーザーの嗜好を表す尺度**である。言い換えれば、各ユーザーがロングテール・アイテムに対してショートヘッド・アイテムにどれだけ興味があるかを測定するものである。我々はこの尤度を、ユーザープロファイルの中でカテゴリdに属するアイテムの比率で計算する。

In order to select the next item to add to S, we compute a reranking score for each item in $R and S$ according to Eq. 4. For an item $v′ \in d$, if $S$ does not cover d, then an additional positive term will be added to the estimated user preference $P(v′|u)$. Therefore, the chance that it will be selected is larger, balancing accuracy and popularity bias.
次にSに追加するアイテムを選択するために、式4に従って$RとS$の各アイテムについて再ランク付けスコアを計算します.
あるアイテム$v′ \in d$に対して、$S$がdをカバーしていない場合、推定ユーザー嗜好度$P(v′|u)$に正の項が追加されることになります.
したがって、選択される確率が大きくなり、精度と人気度バイアスのバランスをとることができます.

In Binary xQuAD, the product term $\Pi_{i\in S} (1 - P(i|c, S))$ is only equal to 1 if the current items in S have not covered the category d yet. Binary xQuAD is, therefore, optimizing for a minimal re-ranking of the original list by including the best long-tail item it can, but not seeking diversity beyond that.
バイナリxQuADでは、積項 $Pi_{i\in S}(1 - P(i|c,S))$ は、Sに含まれる現在の項目がまだカテゴリdをカバーしていない場合のみ、1になる。したがって、バイナリxQuADは、最も良いロングテール項目を含むことによって、元のリストの最小限の再順位を最適化するが、それ以上の多様性は求めない。

# Experiment 実験

In this section, we test our proposed algorithm on two public datasets.
本節では，提案アルゴリズムを2つの公開データセットでテストする．
The first is the well-known Movielens 1M dataset that contains 1,000,209 anonymous ratings of approximately 3,900 movies made by 6,040 MovieLens users [13].
1つ目は，よく知られたMovielens 1Mデータセットであり，6,040人のMovieLensユーザによる約3,900本の映画に対する1,000,209件の匿名の評価が含まれる[13]．
The second dataset is the Epinions dataset, which is gathered from a consumers opinion site where users can review items [15].
2つ目のデータセットはEpinionsデータセットであり，ユーザがアイテムをレビューできる消費者意見サイトから収集されたものである[15]．
This dataset has the total number of 664,824 ratings given by 40,163 users to 139,736 items.
このデータセットには，40,163人のユーザが139,736のアイテムに対して与えた664,824の評価の合計が含まれている．
In Movielens, each user has a minimum of 20 ratings but in Epinions, there are many users with only a single rated item.
Movielensでは、各ユーザは最低20の評価を持っているが、Epinionsでは、1つの評価項目しか持たないユーザが多数存在する。

Following the data reduction procedure in [2], we removed users who had fewer than 20 ratings from the Epinion dataset, as users with longer profiles are much more likely to have long-tail items in their profiles.
2]のデータ削減手順に従って、長いプロフィールを持つユーザはロングテールのアイテムを持つ可能性が非常に高いため、20未満の評価を持つユーザをEpinionデータセットから削除しました。
MovieLens dataset already consists of only users with more than 20 ratings.
MovieLensのデータセットは、すでに20以上の評価を持つユーザーのみで構成されています。
The retained users were those likely to have rated enough long-tail items so that our objective could be evaluated in a train
そのため、MovieLensのデータセットには、20件以上の評価を持つユーザのみが登録されています。

After filtering, the MovieLens dataset has 6,040 users who rated 3043 movies with a total number of 995,492 ratings, a reduction of about 0.4%.
フィルタリング後、MovieLensデータセットには、6,040人のユーザーが3043本の映画を評価し、総評価数は995,492件となり、約0.4%の減少となっています。
Applying the same criteria to the Epinions dataset decreases the data to 220,117 ratings given by 8,144 users to 5,195 items, a reduction of around 66%.
Epinionsのデータセットに同じ基準を適用すると、8,144人のユーザが5,195のアイテムに与えた220,117の評価になり、約66%の減少になります。
We split the items in both datasets into two categories: long-tail ($\Gamma$) and short head ($\Gamma'$)in a way that short head items correspond to %80 of the ratings while long-tail items have the rest of the %20 of the ratings.
両データセットのアイテムをlong-tail($techamma$)とshort head($techamma'$)に分割し、short headアイテムが評価の80%に、long-tailアイテムが評価の残りの20%に対応するようにしました。
We plan to consider other divisions of the popularity distribution in future work.
今後、他の人気度分布の分割も検討する予定である。
For MovieLens, the short-head items were those with more than 506 ratings.
MovieLensでは、短頭項目は506件以上の評価を持つ項目であった。
In Epinions, a short-head item needed only to have more than 73 ratings.
Epinionsでは、ショートヘッドのアイテムは73以上のレーティングを持つものであればよい。

# Evaluation 評価

The experiments compare four algorithms.
実験では4つのアルゴリズムを比較した．
Since we are concerned with ranking performance, we chose as our baseline algorithm RankALS, a pair-wise learning-to-rank algorithm.
我々はランキングの性能に関心があるため、**ベースラインアルゴリズム**として、ペアワイズ学習によるランキングアルゴリズムであるRankALS(=損失関数にランクの成分を追加したALS、という認識)を選択した。
We also include the **regularized long-tail diversification algorithm** in [2] (indicated as LT-Reg in the figures.) We used the output from RankALS as input for the two re-ranking variants described above:
また、[2]の正則化ロングテール分散アルゴリズム（図中ではLT-Regと表記）を含めた。
Binary xQuAD and Smooth xQuAD, marked Binary and Smooth in the figures.
そしてBinary xQuADとSmooth xQuADです. 図中ではBinaryとSmoothと表記しています。
We compute lists of length 100 from RankALS and pass these to the reranking algorithms to compute the final list of 10 recommendations for each user.
RankALSの出力から長さ100のリストを計算し、それを再ランク付けアルゴリズムに渡すことで、各ユーザーの最終的な推奨リスト10個を計算しています。
We used the implementation of RankALS in LibRec 2.0 for all experiments.
すべての実験にLibRec 2.0のRankALSを使用した。

In order to evaluate the effectiveness of algorithms in mitigating popularity bias we use four different metrics:
人気度バイアスを緩和するアルゴリズムの有効性を評価するために、4つの異なるメトリクスを使用しています。

### Average Recommendation Popularity (ARP): 平均レコメンデーション人気度（ARP）。

This measure from [22] calculates the average popularity of the recommended items in each list.
この[22]の指標は、各リストの推奨項目の平均人気度を計算する。
For any given recommended item in the list, we measure the average number of ratings for those items.
リスト内の任意の推奨アイテムについて、それらのアイテムの平均評価数を測定します。
More formally:
より正式には

$$
ARP = \frac{1}{|U_t|} \sum_{u \in U_t} \frac{\sum_{i \in L_u} \phi(i)}{|L_u|}
\tag{5}
$$

where ϕ(i) is the number of times item i has been rated in the training set. $L_u$ is the recommended list of items for user u and $|U_t|$ is the number of users in the test set.
ここで、φ(i)はトレーニングセットでアイテムiが評価された回数である。
$L_u$ はユーザ u の推奨アイテムリスト、$|U_t|$ はテストセットにおけるユーザ数である。

### Average Percentage of Long Tail Items (APLT): 平均ロングテール項目比率（APLT）。

As used in [2], this metric measures the average percentage of long tail items in the recommended lists and it is defined as follows:
2]で使用されているように、この指標は推奨リストにおけるロングテール項目の平均的な割合を測定し、次のように定義されています。

$$
APLT = \frac{1}{|U_t|}\sum_{u \in U_t} \frac{|{i,i \in (L_u \cap \Gamma)}|}{|L_u|}
\tag{6}
$$

This measure gives us the average percentage of items in users’ recommendation lists that belong to the long tail set.
この指標は、ユーザーの推薦リストにおいて、ロングテール集合に属するアイテムの平均的な割合を示しています。

### Average Coverage of Long Tail items (ACLT): ロングテール項目の平均カバー率（ACLT）。

We introduce another metric to evaluate how much exposure long-tail items get in the entire recommendation.
そこで，ロングテール項目が推薦全体の中でどの程度露出するかを評価する別の指標を導入する．
One problem with APLT is that it could be high even if all users get the same set of long tail items.
APLT の問題点の一つは、すべてのユーザが同じロングテール項目セットを得たとしても、それが高くなる可能性があることです。
ACLT measures what fraction of the long-tail items the recommender has covered:
ACLT は推薦者がロングテール項目の何割をカバーしたかを測定する。

$$
ACLT = \frac{1}{|U_t|} \sum_{u \in U_t} \sum_{i \in L_u} \mathbb{1}(i \in \Gamma)
\tag{7}
$$

where $\mathbb{1}(i \in \Gamma)$ is an indicator function and it equals to 1 when i is in Γ.
ここで、$mathbb{1}(i \in \Gamma)$ は指標関数であり、i がΓにあるとき 1 になる。
This function is related to the Aggregate Diversity metric of [4] but it looks only at the long-tail part of the item catalog.
この関数は[4]のAggregate Diversity metricと関連しているが、アイテムカタログのロングテール部分のみを見るものである。

In addition to the aforementioned long tail diversity metrics, we also evaluate the accuracy of the ranking algorithms in order to examine the diversity-accuracy trade-offs.
前述のロングテール多様性指標に加えて、多様性と精度のトレードオフを検証するために、ランキング・アルゴリズムの精度も評価しました。
For this purpose we use the standard Normalized Discounted cumulative Gain (NDCG) measure of ranking accuracy.
この目的のために、我々はランキング精度の標準的なNDCG（Normalized Discounted cumulative Gain）指標を使用します。

# Result 結果

Figure 2 shows the results for the Epinions dataset across the different algorithms using a range of values for λ. (Note that the LT-Reg algorithm uses the parameter λ to control the weight placed on the long-tail regularization term.)
図 2 は，Epinions データセットに対して，様々な λ の値を使用した結果を示している（LT-Reg アルゴリズムは，パラメータ λ を使用して，ロングテール正則化項の重みを制御していることに注意）．
All results are averages from five-fold cross-validation using a %80 -%20 split for train and test, respectively.
すべての結果は、訓練とテストのそれぞれで%80 -%20 の分割を使用した 5 回のクロスバリデーションからの平均値である。
As expected, the diversity scores improve for all algorithms, with some loss of ranking accuracy.
予想通り、すべてのアルゴリズムで多様性スコアが向上しているが、ランキングの精度は若干低下している。
Differences between the algorithms are evident, however.
しかし、アルゴリズム間の差は明らかである。
The exposure metric (ACLT) plot shows that the two re-ranking algorithms, and especially the Smooth version, are doing a much better job of exposing items across the long-tail inventory than the regularization method.
露出度指標（ACLT）プロットは、2つの再ランキングアルゴリズム、特にSmoothバージョンは、正則化手法よりもロングテール在庫全体のアイテムを露出させるのに非常に良い仕事をしていることを示しています。
The ranking accuracy shows that, as expected, the Binary version does slightly better as it performs minimal adjustment to the ranked lists.
ランキング精度を見ると、予想通り、ランク付けされたリストに対して最小限の調整を行うバイナリ版の方がわずかに優れていることがわかります。
LT-Reg is not as effective at promoting long-tail items, either by the list-wise APLT measure or by the catalog-wise ACLT.
LT-Regはリスト単位のAPLTでもカタログ単位のACLTでも、ロングテール・アイテムを促進する効果はそれほど高くはありません。

Another view of the same results is provided in Figure 3.
同じ結果を別の角度から見たのが図3です。
Here we look at the long-tail diversity metrics relative to NDCG loss, which clarifies the patterns seen in Figure 2.
ここでは、NDCG損失に対するロングテールの多様性メトリクスを見て、図2に見られるパターンを明確にしています。
We see that the Binary and Smooth algorithms are fairly similar in terms of diversity-accuracy trade-off, while LT-Reg has a distinctly lower and flatter improvement curve with increased loss of ranking accuracy.
BinaryとSmoothアルゴリズムは多様性と精度のトレードオフの点でかなり似ていることがわかりますが、LT-Regはランキング精度の損失が大きくなると明らかに低く、平坦な改善曲線を描くことがわかります。
ARP metric is the only one where the algorithms are fairly similar, especially at lower values of NDCG loss.
ARPメトリックは、特にNDCGロスの値が低い場合に、アルゴリズムがかなり類似している唯一のものです。

The MovieLens dataset shows different relative performance across the algorithms as seen in Figure 4.
MovieLensデータセットでは、図4に見られるように、アルゴリズム間で相対的な性能の違いが見られます。
The Smooth re-ranking method shows a more distinct benefit and LT-Reg is somewhat more effective.
Smooth re-ranking法は、より明確な利益を示し、LT-Regはより効果的である。
This finding is confirmed in the relative results shows in Figure 5, which also shows the algorithms having quite similar values for the ARP metric, in spite of the differences on the other metrics.
この発見は、図5の相対的な結果でも確認され、他のメトリクスでは差があるにもかかわらず、ARPメトリクスではアルゴリズムが非常に似た値を示していることがわかります。

Comparing the two datasets, we see that long-tail diversification is more of a challenge in the sparser Epinions dataset.
2つのデータセットを比較すると、ロングテールの多様化は、より疎なEpinionsのデータセットではより困難であることがわかります。
With 10% NDCG loss, it is possible to bring exposure to around 15% of the long-tail catalog in Epinions; whereas for MovieLens, 0.2% loss yields an equivalent or greater benefit.
10%のNDCG損失で、Epinionsのロングテール・カタログの約15%に露出させることが可能です。一方、MovieLensでは、0.2%の損失で同等以上の利益がもたらされます。
LT-Reg is much less effective.
LT-Regはあまり効果がありません。
(In both datasets, the baseline value is very close to zero.) The average number of long-tail items in each recommendation list shows a similar pattern.
(両データセットとも、ベースライン値はゼロに非常に近い値です。）各推奨リストにおけるロングテール商品の平均数も、同様のパターンを示しています。

In the sparser dataset, the Binary and Smooth measures are similar in performance, but differences appear in MovieLens, where the Smooth algorithm shows stronger improvement in the ACLT measure, particularly.
Sparserデータセットでは、BinaryとSmoothの性能はほぼ同じですが、MovieLensでは違いが現れ、Smoothアルゴリズムは特にACLTメジャーでより強い改善を示しています。
This effect is most likely due to the fact that in the sparser data, it is more difficult to find a single long-tail item to promote into a recommendation list, with greater accuracy cost in doing so.
この効果は、より疎なデータでは、推薦リストに昇格させる単一のロングテール項目を見つけることがより困難であり、そうすることでより大きな精度コストがかかるという事実による可能性が高い。
In MovieLens, these higher-quality items appear more often and the Smooth objective values the promotion of multiple such items into the recommendation lists.
MovieLensでは、このような質の高いアイテムが頻繁に登場し、Smooth目的では、このようなアイテムを複数推薦リストに昇格させることが重要視されています。

Another conclusion we can draw is that the ARP measure is not a good measure of long-tail diversity when it is used only on its own.
もう一つの結論は、ARP尺度を単独で使用した場合、ロングテールの多様性を測る尺度としては不十分であるということです。
It has the benefit of not requiring the experimenter to set a threshold distinguishing long-tail and short-head items.
ARPには、ロングテールとショートヘッドのアイテムを区別する閾値を実験者が設定する必要がないという利点があります。
However, as we see here, algorithms can have very similar ARP performance and be quite different in terms of their ability to cover the long-tail catalog and to promote long-tail items to users.
しかし、ここで見るように、アルゴリズムは非常に似たARPパフォーマンスを持ちながら、ロングテール・カタログをカバーする能力と、ロングテール・アイテムをユーザにプロモートする能力において、全く異なる場合があります。
So it is important to look at all these metrics together.
したがって、これらの指標をすべて一緒に見ることが重要です。

# Conclusiton and Future Work 結論と今後の課題

Adequate coverage of long-tail items is an important factor in the practical success of business-to-consumer organizations and information providers.
B to Cの組織や情報提供者にとって、ロングテール商品を適切にカバーすることは重要な要素である。
Since short-head items are likely to be well known to many users, the ability to recommend items outside of this band of popularity will determine if a recommender system can introduce users to new products and experiences.
ショートテール項目は多くのユーザーに知られている可能性が高いため、この人気帯以外の項目を推薦できるかどうかが、レコメンデーションシステムがユーザーに新しい商品や体験を紹介できるかどうかを左右する。
Yet, it is well-known that recommendation algorithms have biases towards popular items.
しかし、推薦アルゴリズムには人気アイテムへのバイアスがあることはよく知られている。

In this paper, we presented re-ranking approaches for long-tail promotion and compared them to a state-of-the-art model-based approach.
本論文では、ロングテール促進を目的とした再順位付け手法を提示し、最先端のモデルベース手法と比較した。
On two datasets, we were able to show that the re-ranking methods boost long-tail items while keeping the accuracy loss small, compared to the model-based technique.
2つのデータセットにおいて，モデルベース手法と比較して，再ランキング手法が精度の損失を小さく抑えながらロングテール項目をブーストすることを示すことができた．
We also showed that the average recommendation popularity (ARP) measure from [22] is not a good metric on its own for evaluating long-tail promotion, as algorithms might have similar ARP performance but quite different performance on other measures of popularity bias.
また，[22]の平均推薦人気度（ARP）指標は，それ自体ではロングテール促進を評価するための良い指標ではないことを示しました．なぜなら，アルゴリズムはARPのパフォーマンスが似ていても，人気の偏りに関する他の指標では全く異なるパフォーマンスを持っているかもしれないからです．
So it is better to use it along with other metrics such as APLT and ACLT to get the right picture of the effectiveness of the algorithms.
そのため，アルゴリズムの有効性を正しく把握するためには，APLT や ACLT などの他の評価指標と併用することが望ましいと言えます．

One interesting area for future work would be using this model for multistakeholder recommendation where the system needs to make recommendations in the presence of different stakeholders providing the products [1, 3, 8, 9].
将来的に、このモデルをマルチステークホルダーレコメンデーション に使用することが考えられます。
In those cases, another parameter could be used to control the priority of each stakeholder in the system.
このような場合、システム内の各ステークホル ダーの優先順位を制御するために、別のパラメータを使 用することができる。

# References リファレンス

- [1] Himan Abdollahpouri, Gediminas Adomavicius, Robin Burke, Ido Guy, Dietmar Jannach, Toshihiro Kamishima, Jan Krasnodebski, and Luiz Pizzato. 2019. Beyond Personalization: Research Directions in Multistakeholder Recommendation. arXiv preprint arXiv:1905.01986 (2019). 1] Himan Abdollahpouri, Gediminas Adomavicius, Robin Burke, Ido Guy, Dietmar Jannach, Toshihiro Kamishima, Jan Krasnodebski, and Luiz Pizzato. 2019. Beyond Personalization: Research Directions in Multistakeholder Recommendation. arXiv preprint arXiv:1905.01986 (2019).

- [2] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2017. Controlling Popularity Bias in Learning-to-Rank Recommendation. In Proceedings of the Eleventh ACM Conference on Recommender Systems. ACM, 42–46. [2] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2017. Learning-to-Rank Recommendation における Popularity Bias の制御． In Proceedings of the Eleventh ACM Conference on Recommender Systems. ACM, 42-46.

- [3] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2017. Recommender systems as multi-stakeholder environments. In Proceedings of the 25th Conference on User Modeling, Adaptation and Personalization (UMAP2017). ACM. [3] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2017. マルチステークホルダー環境としてのリコメンダーシステム。 In Proceedings of the 25th Conference on User Modeling, Adaptation and Personalization (UMAP2017). ACM.

- [4] Gediminas Adomavicius and YoungOk Kwon. 2012. Improving aggregate recommendation diversity using ranking-based techniques. IEEE Transactions on Knowledge and Data Engineering 24, 5 (2012), 896–911. 4] Gediminas Adomavicius and YoungOk Kwon. 2012. ランキングベースの技術を用いた集約的な推薦の多様性の改善. IEEE Transactions on Knowledge and Data Engineering 24, 5 (2012), 896-911.

- [5] Chris Anderson. 2006. The long tail: Why the future of business is selling more for less. Hyperion. [5] Chris Anderson. 2006. The long tail: Why the future of business is selling more for less. Hyperion.

- [6] Alejandro Bellogín, Pablo Castells, and Iván Cantador. 2017. Statistical biases in Information Retrieval metrics for recommender systems. Information Retrieval Journal 20, 6 (2017), 606–634. [6] Alejandro Bellogín, Pablo Castells, and Iván Cantador. 2017. レコメンダーシステムのための情報検索メトリクスにおける統計的偏り。 情報検索ジャーナル 20, 6 (2017), 606-634.

- [7] Erik Brynjolfsson, Yu Jeffrey Hu, and Michael D Smith. 2006. From niches to riches: Anatomy of the long tail. Sloan Management Review (2006), 67–71. 7] Erik Brynjolfsson, Yu Jeffrey Hu, and Michael D Smith. 2006. From niches to riches: Anatomy of the long tail. Sloan Management Review (2006), 67-71.

- [8] Robin Burke and Himan Abdollahpouri. 2016. Educational Recommendation with Multiple Stakeholders. In Third International Workshop on Educational Recommender Systems. Omaha. [8] ロビン・バーク、ヒマン・アブドラフリ。 2016. Multiple Stakeholders を用いた教育推薦. In Third International Workshop on Educational Recommender Systems. オマハ。

- [9] Robin D. Burke, Himan Abdollahpouri, Bamshad Mobasher, and Trinadh Gupta. 2016. Towards Multi-Stakeholder Utility Evaluation of Recommender Systems. In Workshop on Surprise, Opposition, and Obstruction in Adaptive and Personalized Systems, UMAP 2016. [9] Robin D. Burke, Himan Abdollahpouri, Bamshad Mobasher, and Trinadh Gupta. 2016. Towards Multi-Stakeholder Utility Evaluation of Recommender Systems. In Workshop on Surprise, Opposition, and Obstruction in Adaptive and Personalized Systems, UMAP 2016.

- [10] Pablo Castells, Saúl Vargas, and Jun Wang. 2011. Novelty and diversity metrics for recommender systems: choice, discovery and relevance. In Proceedings of International Workshop on Diversity in Document Retrieval (DDR). ACM Press, 29–37. 10] Pablo Castells, Saúl Vargas, and Jun Wang. 2011. このような場合、「recommender」（レコメンダー）は、「recommender」（レコメンダー）と「discovery」（ディスカバリー）の2種類に分けられる。 このような場合、「recommender.com」は、「recommender.com」を「recommender.com」と呼ぶことにする。 ACM Press, 29-37.

- [11] Òscar Celma and Pedro Cano. 2008. From hits to niches?: or how popular artists can bias music recommendation and discovery. In Proceedings of the 2nd KDD Workshop on Large-Scale Recommender Systems and the Netflix Prize Competition. ACM, 5. 11] オスカー・セルマとペドロ・カノ。 2008. そのため、このような場合、「曖昧さ」を解消することが重要である。 ACM, 5.

- [12] Farzad Eskandanian, Bamshad Mobasher, and Robin Burke. 2017. A Clustering Approach for Personalizing Diversity in Collaborative Recommender Systems. In Proceedings of the 25th Conference on User Modeling, Adaptation and Personalization. ACM, 280–284. 12] Farzad Eskandanian, Bamshad Mobasher, and Robin Burke. 2017. A Clustering Approach for Personalizing Diversity in Collaborative Recommender Systems（協調型推薦システムにおける多様性のパーソナライゼーションのためのクラスタリング・アプローチ）． In Proceedings of the 25th Conference on User Modeling, Adaptation and Personalization. ACM, 280-284.

- [13] F Maxwell Harper and Joseph A Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4(2015), 19. 13] F Maxwell Harper and Joseph A Konstan. 2015. ムービーレンズ・データセット。 歴史と文脈. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4(2015), 19.

- [14] Weiwen Liu and Robin Burke. 2018. Personalizing Fairness-aware Re-ranking. arXiv preprint arXiv:1809.02921 (2018). 14] Weiwen Liu and Robin Burke. 2018. Personalizing Fairness-aware Re-ranking. arXiv preprint arXiv:1809.02921 (2018).

- [15] Paolo Massa and Paolo Avesani. 2007. Trust-aware recommender systems. In Proceedings of the 2007 ACM conference on Recommender systems. ACM, 17–24. 15] Paolo Massa and Paolo Avesani. 2007. このような場合，"recommender "という言葉を使う． このような場合、「曖昧さ」を回避することが重要である。 ACM, 17-24.

- [16] Yoon-Joo Park and Alexander Tuzhilin. 2008. The long tail of recommender systems and how to leverage it. In Proceedings of the 2008 ACM conference on Recommender systems. ACM, 11–18. 16] Yoon-Joo Park and Alexander Tuzhilin. 2008. このような場合、recommender system は、"recommender "を "recommender "と呼ぶことにする。 というのも、"recommender "は "recommender "を意味するからである。 ACM, 11-18.

- [17] Paul Resnick, R Kelly Garrett, Travis Kriplean, Sean A Munson, and Natalie Jomini Stroud. 2013. Bursting your (filter) bubble: strategies for promoting diverse exposure. In Proceedings of the 2013 conference on Computer supported cooperative work companion. ACM, 95–100. 17] Paul Resnick, R Kelly Garrett, Travis Kriplean, Sean A Munson, and Natalie Jomini Stroud. 2013. Bursting your (filter) bubble: strategies for promoting diverse exposure. コンピュータがサポートする協調作業コンパニオンの2013年会議の議事録。 ACM, 95-100.

- [18] Rodrygo LT Santos, Craig Macdonald, and Iadh Ounis. 2010. Exploiting query reformulations for web search result diversification. In Proceedings of the 19th international conference on World wide web. ACM, 881–890. 18] Rodrygo LT Santos, Craig Macdonald, and Iadh Ounis. 2010. このような場合、「曖昧さ」を解消することが重要です。 このような場合、「曖昧さ」を回避することが重要です。 ACM, 881-890.

- [19] Rodrygo LT Santos, Craig Macdonald, Iadh Ounis, et al. 2015. Search result diversification. Foundations and Trends® in Information Retrieval 9, 1 (2015), 1–90. 19] Rodrygo LT Santos, Craig Macdonald, Iadh Ounis, et al. 2015. 検索結果の多様化. 情報検索における基礎と傾向® 9, 1 (2015), 1-90.

- [20] Saúl Vargas, Pablo Castells, and David Vallet. 2012. Explicit relevance models in intent-oriented information retrieval diversification. In Proceedings of the 35th international ACM SIGIR conference on Research and development in information retrieval. ACM, 75–84. 20] Saúl Vargas, Pablo Castells, and David Vallet. 2012. このような場合，情報検索の多様化における明示的な関連性モデル． このような場合、「情報検索における研究開発」の第35回国際会議ACM SIGIRの議事録。 ACM, 75-84.

- [21] Jacek Wasilewski and Neil Hurley. 2018. Intent-aware Item-based Collaborative Filtering for Personalised Diversification. In Proceedings of the 26th Conference on User Modeling, Adaptation and Personalization. ACM, 81–89. 21] Jacek Wasilewski and Neil Hurley. 2018. Intent-aware Item-based Collaborative Filtering for Personalised Diversification. In Proceedings of the 26th Conference on User Modeling, Adaptation and Personalization. ACM, 81-89.

- [22] Hongzhi Yin, Bin Cui, Jing Li, Junjie Yao, and Chen Chen. 2012. Challenging the long tail recommendation. Proceedings of the VLDB Endowment 5, 9 (2012), 896–907. 22] Hongzhi Yin, Bin Cui, Jing Li, Junjie Yao, and Chen Chen. 2012. ロングテール推薦に挑む。 Proceedings of the VLDB Endowment 5, 9 (2012), 896-907.

- [23] Mi Zhang and Neil Hurley. 2008. Avoiding monotony: improving the diversity of recommendation lists. In Proceedings of the 2008 ACM conference on Recommender systems. ACM, 123–130. 23] Mi Zhang and Neil Hurley. 2008. このような場合、「曖昧さ」を解消することが重要である。 そのため、このような場合、「曖昧さ」を解消する必要がある。 ACM, 123-130.

- [24] Tao Zhou, Zoltán Kuscsik, Jian-Guo Liu, Matúš Medo, Joseph Rushton Wakeling, and Yi-Cheng Zhang. 2010. Solving the apparent diversity-accuracy dilemma of recommender systems. Proceedings of the National Academy of Sciences 107, 10 (2010), 4511–4515. 24] Tao Zhou, Zoltán Kuscsik, Jian-Guo Liu, Matúš Medo, Joseph Rushton Wakeling, and Yi-Cheng Zhang. 2010. このような場合、「recommender system」の多様性と精度のジレンマを解決する。
