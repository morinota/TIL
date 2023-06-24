## Link リンク

- http://old-eclass.uop.gr/modules/document/file.php/DIT104/%CE%92%CE%B9%CE%B2%CE%BB%CE%B9%CE%BF%CE%B3%CF%81%CE%B1%CF%86%CE%AF%CE%B1%202017-2018/Diversity%2C%20Serendipity%2C%20Novelty%2C%20and%20Coverage.pdf http://old-eclass.uop.gr/modules/document/file.php/DIT104/%CE%92%CE%B9%CE%B2%CE%BB%CE%B9%CE%BF%CE%B3%CF%81%CE%B1%CF%86%CE%AF%CE%B1%202017-2018/Diversity%2C%20Serendipity%2C%20Novelty%2C%20and%20Coverage.pdf

- https://dl.acm.org/doi/abs/10.1145/2926720 https://dl.acm.org/doi/abs/10.1145/2926720

## title タイトル

Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems
多様性、セレンディピティ、新規性、カバレッジ： 推薦システムにおける精度を超える目標のサーベイと実証分析

## abstract 抄録

What makes a good recommendation or good list of recommendations?
良い推薦文、良い推薦リストとは何か？

Research into recommender systems has traditionally focused on accuracy, in particular how closely the recommender’s predicted ratings are to the users’ true ratings.
レコメンダー・システムの研究は、伝統的に精度、特にレコメンダーが予測した評価がユーザーの真の評価にどれだけ近いかに焦点を当ててきた。
However, it has been recognized that other recommendation qualities—such as whether the list of recommendations is diverse and whether it contains novel items—may have a significant impact on the overall quality of a recommender system.
しかし、他の推薦品質、例えば推薦リストが多様であるかどうか、新規項目を含んでいるかどうか、が推薦システムの全体的な品質に大きな影響を与える可能性があることが認識されている。
Consequently, in recent years, the focus of recommender systems research has shifted to include a wider range of “beyond accuracy” objectives.
その結果、近年、レコメンダー・システム研究の焦点は、「正確さを超えた」幅広い目標を含むようになった。

In this article, we present a survey of the most discussed beyond-accuracy objectives in recommender systems research: diversity, serendipity, novelty, and coverage.
本稿では、推薦システム研究において最も議論されている、多様性、セレンディピティ、新規性、カバレッジといった、精度を超えた目的についてのサーベイを紹介する。
We review the definitions of these objectives and corresponding metrics found in the literature.
これらの目的の定義と、文献に見られる対応する指標をレビューする。
We also review works that propose optimization strategies for these beyond-accuracy objectives.
また、このような精度を超えた目標に対する最適化戦略を提案した研究もレビューする。
Since the majority of works focus on one specific objective, we find that it is not clear how the different objectives relate to each other.
大半の作品が特定の1つの目的に焦点を当てているため、異なる目的が互いにどのように関連しているのかが明確でないことがわかる。

Hence, we conduct a set of offline experiments aimed at comparing the performance of different optimization approaches with a view to seeing how they affect objectives other than the ones they are optimizing.
そこで、異なる最適化アプローチのパフォーマンスを比較し、最適化する目的以外の目的にどのような影響を与えるかを見ることを目的としたオフライン実験を実施する。
We use a set of state-of-the-art recommendation algorithms optimized for recall along with a number of reranking strategies for optimizing the diversity, novelty, and serendipity of the generated recommendations.
我々は、リコールのために最適化された最先端の推薦アルゴリズムのセットと、生成された推薦の多様性、新規性、セレンディピティを最適化するための多くの再ランク戦略を使用する。
For each reranking strategy, we measure the effects on the other beyond-accuracy objectives and demonstrate important insights into the correlations between the discussed objectives.
それぞれのリランキング戦略について、他の精度を超えた目標への影響を測定し、議論された目標間の相関に関する重要な洞察を示す。
For instance, we find that rating-based diversity is positively correlated with novelty, and we demonstrate the positive influence of novelty on recommendation coverage.
例えば、レーティングベースの多様性は新規性と正の相関があり、新規性がレコメンデーションカバレッジに正の影響を与えることを実証している。

# Introduction はじめに

Traditionally, the focus of recommender systems (RS) research has been the accurate prediction of users’ ratings for unseen items.
従来、レコメンダーシステム（RS）研究の焦点は、未見のアイテムに対するユーザーの評価を正確に予測することであった。
However, accuracy is not the only important objective of recommendation [McNee et al.2006].
しかし、推薦の重要な目的は正確さだけではない[McNee et al.2006]。
In recent years, the focus of RS research has shifted to such objectives as correctly ranking a set of items (known as the learning-to-rank problem [Shi et al.2010]) as well as ensuring that the set of recommended items is diverse [Vargas et al.2014] and that it contains novel items [Oh et al.2011].
近年、RS研究の焦点は、アイテムの集合を正しくランク付けすること（学習ランク付け問題[Shi et al.2010]として知られている）、推奨アイテムの集合が多様であること[Vargas et al.2014]や新規のアイテムが含まれていること[Oh et al.2011]を保証することなどにシフトしている。
These qualities are of particular importance in real-life systems since users are most likely to consider only a small set of top-N recommendations.
このような性質は、現実のシステムにおいて特に重要である。なぜなら、ユーザーはトップNの推薦文の小さなセットしか考慮しない可能性が高いからである。
It is therefore crucial to make sure that this set is as interesting and engaging as possible.
そのため、このセットをできるだけ面白く、魅力的なものにすることが重要だ。
In this article, we survey and analyze the most discussed objectives that relate to the quality of recommender systems beyond accuracy—diversity, serendipity, novelty, and coverage.
この論文では、正確性以上に推薦システムの品質に関連する最も議論されている目的-多様性、セレンディピティ、新規性、網羅性-を調査・分析する。
Before receiving attention in RS research, diversity and its relationship to accuracy were studied in information retrieval (IR) [Carbonell and Goldstein 1998] and, before that, in economics research.
RS研究で注目される以前、多様性とその正確さとの関係は、情報検索（IR）[Carbonell and Goldstein 1998]で研究され、それ以前は経済学研究でも研究されていた。
Markowitz [1952] introduced the Modern Portfolio Theory where investment is modeled as a tradeoff between risk and expected return.
マーコウィッツ[1952]は、投資がリスクと期待リターンのトレードオフとしてモデル化される現代ポートフォリオ理論を導入した。
Maximizing the expected return results in higher investment risk, while diversification of stock portfolios reduces the risk.
期待リターンを最大化すれば投資リスクは高くなるが、株式ポートフォリオを分散すればリスクは軽減される。
This idea has been adopted in IR [Carbonell and Goldstein 1998; Clarke et al.2008; Wang and Zhu 2009; Agrawal et al.2009], where it is argued that ranking retrieved items by only their predicted relevance (i.e., maximizing retrieval accuracy) increases the risk of producing results that do not satisfy users because the items tend to be too similar to each other.
この考え方はIRでも採用されており[Carbonell and Goldstein 1998; Clarke et al.2008; Wang and Zhu 2009; Agrawal et al.2009]、検索されたアイテムを予測される関連性だけでランク付けする（つまり、検索精度を最大化する）ことは、アイテムが互いに類似しすぎる傾向があるため、ユーザーを満足させない結果を生み出すリスクを高めると論じられている。
Conversely, diversifying the retrieval results reduces this risk by increasing the chance of introducing items the user will be interested in.
逆に、検索結果を多様化することで、ユーザーが興味を持つアイテムが紹介される可能性が高くなり、このリスクを減らすことができる。
In RS research, diversity is becoming an increasingly important topic, with a growing consensus that users are more satisfied with diverse recommendation lists, even if the diversity comes at a cost of some loss of accuracy [Ziegler et al.2005; Shi et al.2012; Vargas et al.2014].
RS研究において、多様性はますます重要なトピックとなりつつあり、たとえ多様性によって精度が多少損なわれるとしても、多様な推薦リストがあった方がユーザーは満足するというコンセンサスが高まっている[Ziegler et al.2005; Shi et al.2012; Vargas et al.2014]。
Serendipity is another objective that has received substantial attention in RS research.
セレンディピティもまた、RS研究で注目されている目的のひとつである。
The term serendipity, referring to the process of “finding valuable or pleasant things that are not looked for,”1 was coined in the 18th century [Van Andel 1994].
セレンディピティ（serendipity）という言葉は、「探してもない貴重なもの、楽しいものを見つける」プロセスを意味し、1 18世紀に作られた［Van Andel 1994］。
This objective is frequently mentioned in the IR and RS research literature [Toms 2000; Andre et al.2009; Herlocker et al.2004; Ge et al.2010], where it is commonly agreed ´ that serendipity consists of two components—surprise and relevance [Herlocker et al.2004].
この目的はIRとRSの研究文献で頻繁に言及されており[Toms 2000; Andre et al.2009; Herlocker et al.2004; Ge et al.2010]、セレンディピティはサプライズと関連性という2つの要素から構成されることが一般的に合意されている[Herlocker et al.2004]。
Until recently, however, few works provided formal definitions of metrics for measuring the serendipity of recommended items.
しかし最近まで、推奨アイテムのセレンディピティを測定するメトリクスの正式な定義を提供した研究はほとんどなかった。
This is not surprising, as the notion of an item being surprising or unexpected is difficult to define and measure.
これは驚くべきことではなく、ある項目が意外であるとか、予期せぬものであるといった概念を定義し、測定することは難しいからである。
Novelty is a recommendation quality that seems to be closely related to serendipity [McNee et al.2006].
新規性は、セレンディピティと密接な関係があると思われる推薦の質である[McNee et al.2006]。
A novel recommended item is one that is previously unknown to the user.
斬新なおすすめアイテムとは、ユーザーにとって未知のアイテムである。
While the definitions may overlap [Zhang 2013], several authors distinguish novelty from serendipity.
定義は重複しているかもしれないが[Zhang 2013]、いくつかの著者は新規性とセレンディピティを区別している。
Herlocker et al.[2004] argued that an item that is novel to a user is not necessarily serendipitous for that user (it needs only to be unknown to the user), while a serendipitous item must be both novel and surprising; hence, the set of items that are serendipitous to a user is a subset of the set of items that are novel to that user.
Herlockerら[2004]は、あるユーザーにとって斬新なアイテムは、必ずしもそのユーザーにとってセレンディピティである必要はない（ユーザーにとって未知であればよい）が、セレンディピティなアイテムは斬新であると同時に驚くべきものでなければならないと主張した。したがって、あるユーザーにとってセレンディピティなアイテムの集合は、そのユーザーにとって斬新なアイテムの集合の部分集合である。
Adamopoulos and Tuzhilin [2014], on the other hand, defined a new objective (closely related to serendipity)—unexpectedness—and did not require an unexpected item to be novel.
一方、Adamopoulos and Tuzhilin [2014]は、（セレンディピティと密接に関連する）新しい目的である「意外性」を定義し、意外なアイテムが新規であることを必要としなかった。
To better distinguish these two objectives, it is increasingly common to define the novelty of an item in a user-independent way, rather than the novelty of a recommended item to a target user.
この2つの目的をよりよく区別するために、ターゲットユーザーに対する推奨アイテムの新規性ではなく、ユーザーに依存しない方法でアイテムの新規性を定義することが一般的になってきている。
Typically, the novelty of an item is estimated by the inverse of its popularity (e.g., measured by the number of ratings it has received): items with low popularity are more likely to be new to target users [Celma 2009; Zhou et al.2010].
通常、アイテムの新規性は、そのアイテムの人気度（例えば、そのアイテムが獲得した評価数によって測定される）の逆数によって推定される：人気の低いアイテムは、ターゲットユーザーにとって新しいものである可能性が高い[Celma 2009; Zhou et al.2010]。
By this definition, an item with high novelty will not necessarily be serendipitous for a user, and a serendipitous recommendation will not necessarily be novel.
この定義によれば、新規性の高いアイテムが必ずしもユーザーにとってセレンディピティであるとは限らず、セレンディピティな推薦が必ずしも新規性の高いものであるとは限らない。

Coverage reflects the degree to which the generated recommendations cover the catalog of available items [Herlocker et al.2004; Ge et al.2010; Adomavicius and Kwon 2012].
カバレッジは、生成された推奨が利用可能なアイテムのカタログをカバーする度合いを反映する[Herlocker et al.2004; Ge et al.2010; Adomavicius and Kwon 2012]。
Higher coverage may benefit both system users and business owners—exposing the users to a wider range of recommended items may increase their satisfaction with the system [Adomavicius and Kwon 2012] and also increase overall product sales [Anderson 2006].
カバレッジが高ければ、システム・ユーザーとビジネス・オーナーの双方にメリットがある。ユーザーに幅広い推奨アイテムを提供することで、システムに対するユーザーの満足度が高まり[Adomavicius and Kwon 2012]、製品全体の売上も増加する[Anderson 2006]。
In the literature, coverage is often linked to other beyond-accuracy objectives, particularly to novelty [Anderson 2006; Fleder and Hosanagar 2009; Adomavicius and Kwon 2012].
文献では、カバレッジはしばしば、他の精度以外の目的、特に新規性と関連している［Anderson 2006; Fleder and Hosanagar 2009; Adomavicius and Kwon 2012］。
However, the relation between these objectives has not been extensively studied.
しかし、これらの目的間の関係については、これまであまり研究されてこなかった。
It is important to note that beyond-accuracy objectives may be pursued to a different extent in different recommendation scenarios, since the need for diversity, novelty, or serendipity may vary depending on the system’s domain or user’s needs.
多様性、新規性、セレンディピティの必要性は、システムのドメインやユーザーのニーズによって異なる可能性があるため、異なる推薦シナリオでは、精度を超える目的が異なる程度まで追求される可能性があることに注意することが重要である。
For instance, when recommending music, it is not always desirable to recommend unknown or surprising artists, as it may be important to include artists the user is familiar with but has not listened to in a while [Kapoor et al.2015].
例えば、音楽を推薦する場合、ユーザーがよく知っているがしばらく聴いていないアーティストを含めることが重要な場合があるため、未知のアーティストや意外なアーティストを推薦することが常に望ましいとは限らない[Kapoor et al.2015]。
Indeed, in many domains, including a few familiar items among the recommendations may build trust in the system [Swearingen and Sinha 2001].
実際、多くの領域において、推薦文の中に馴染みのある項目をいくつか含めることで、システムに対する信頼が高まる可能性がある[Swearingen and Sinha 2001]。
Moreover, the extent to which these objectives should be pursued may need to be adapted to each user’s needs or preferences.
さらに、これらの目的をどの程度追求するかは、各ユーザーのニーズや好みに合わせる必要があるかもしれない。
For instance, when recommending movies, the level of diversity may be adapted to the user’s range of tastes [Shi et al.2012].
例えば、映画を推薦する場合、多様性のレベルはユーザーの好みの範囲に合わせることができる[Shi et al.2012]。
Likewise, the level of recommendation novelty may reflect the extent to which the user is interested in novel items [Oh et al.2011].
同様に、レコメンデーションの新規性のレベルは、ユーザーが新規のアイテムにどの程度興味を持っているかを反映しているかもしれない[Oh et al.2011]。
While the adaptive aspect of beyondaccuracy objectives has not been extensively researched, in the following sections we highlight works that address this important problem.
beyondaccuracy目標の適応的な側面はあまり研究されていないが、以下のセクションでは、この重要な問題に取り組んでいる作品を紹介する。
In this article, we survey the definitions and optimization strategies for each of the objectives, and, using an empirical analysis, we investigate the relationships between them.
本稿では、各目標の定義と最適化戦略についてサーベイし、実証的分析を用いて各目標間の関係を調査する。
Our work complements other surveys that cover various topics in RS research, such as recommendation algorithms [Ekstrand et al.2011; Cacheda et al.2011], side information in rating-based recommender systems [Shi et al.2014], and evaluation metrics [Gunawardana and Shani 2009; Bellog´ın et al.2011].
我々の研究は、推薦アルゴリズム[Ekstrand et al.2011; Cacheda et al.2011]、評価ベースの推薦システムにおけるサイド情報[Shi et al.2014]、評価指標[Gunawardana and Shani 2009; Bellog´n et al.2011]など、RS研究における様々なトピックをカバーする他の調査を補完するものである。
Recently, Castells et al.[2015] presented a survey closely related to ours.
最近、Castellsら[2015]が我々の調査と密接に関連する調査を発表した。
They reviewed different formulations of the diversity and novelty objectives found in the RS literature and analyzed the corresponding metrics.
彼らは、RSの文献に見られる多様性と新規性の目標のさまざまな定式化をレビューし、対応する指標を分析した。
Compared to the work of Castells et al., we extend the analysis of beyond-accuracy objectives with experiments demonstrating how optimizing one beyond-accuracy criterion affects the other objectives.
Castellsらの研究と比較して、我々は、精度を超えた目標の分析を拡張し、1つの精度を超えた基準を最適化することが他の目標にどのような影響を与えるかを実証する実験を行った。
Thus, the contribution of our work is twofold: (1) we provide an extensive review of definitions and optimization techniques for the beyond-accuracy objectives, and (2) we conduct a number of experiments that demonstrate important insights into relationships between diversity, serendipity, novelty, and coverage.
(2)多様性、セレンディピティ、新規性、カバレッジの関係について重要な洞察を示す実験を数多く行った。
We hope that this work will become a useful reference for both researchers and practitioners working on beyond-accuracy objectives in recommender systems and will contribute to further growth of this research area.
本研究が、推薦システムにおける精度を超えた目標に取り組む研究者と実務家の双方にとって有用な参考文献となり、この研究領域のさらなる発展に寄与することを期待している。
Finally, we note that the terminology concerning beyond-accuracy objectives in the RS literature is not consistent.
最後に、RSの文献における精度を超える目標に関する用語は一貫していないことに注意したい。
For instance, the term diversity is often used in reference to the system’s ability to recommend different items to different users, or to the portion of the item catalog recommended across all users (i.e., coverage).
例えば、多様性という用語は、異なるユーザーに異なるアイテムを推奨するシステムの能力、またはすべてのユーザーにわたって推奨されるアイテムカタログの部分（すなわち、カバレッジ）に関して使用されることが多い。
In the ensuing sections, we cite existing works in the places where they best fit conceptually, regardless of the terminology used by the authors.
以下のセクションでは、著者の使用する用語に関係なく、概念的に最も適している箇所で既存の作品を引用する。

# Diversity 多様性

In this section, we first discuss the definition of diversity and the metrics proposed for measuring the diversity of recommendations.
このセクションでは、まず多様性の定義と、推奨の多様性を測定するために提案された指標について説明する。
Subsequently, we review the techniques for increasing diversity.
続いて、多様性を高めるためのテクニックをレビューする。

## Defining and Measuring Diversity 多様性の定義と測定

The notion of diversity in recommender systems originates from ideas in information retrieval research.
レコメンダーシステムにおける多様性という概念は、情報検索研究のアイデアに由来する。
In the IR literature, it has been acknowledged that the value of a retrieved document is influenced not just by the document’s similarity to a query (its relevance), but also by its similarity to other documents retrieved with it [Carbonell and Goldstein 1998].
IRの文献では、検索された文書の価値は、クエリに対する文書の類似性（関連性）だけでなく、一緒に検索された他の文書との類似性にも影響されることが認められている[Carbonell and Goldstein 1998]。
In information retrieval, the role of diversity is typically associated with possible ambiguity in a user’s query—a search term jaguar may refer to the car, the animal, or the classic Fender guitar, for example [Clarke et al.2008].
情報検索において、多様性の役割は一般的に、ユーザーのクエリに含まれる可能性のある曖昧さと関連している。例えば、検索語のジャガーは、車、動物、またはクラシックなフェンダーギターを指すかもしれない[Clarke et al.2008]。
In the absence of disambiguating information, it is impossible to know which topic the user is interested in.
曖昧さをなくす情報がない場合、ユーザーがどのトピックに興味があるのかを知ることは不可能である。
Thus, ensuring that the list of retrieved documents covers a broad area of the information space increases the chance of satisfying the user’s information need.
このように、検索された文書のリストが情報空間の広い領域をカバーするようにすることで、ユーザーの情報ニーズを満たす可能性が高まる。
This can be achieved by optimizing the diversity of the document list, which can be measured in terms of features (e.g., document types, information facts, topics) that the documents in the list possess [Carbonell and Goldstein 1998; Clarke et al.2008; Wang and Zhu 2009; Agrawal et al.2009].
これは、文書リストの多様性を最適化することで達成できる。多様性は、リスト内の文書が持つ特徴（文書の種類、情報ファクト、トピックなど）で測ることができる[Carbonell and Goldstein 1998; Clarke et al.2008; Wang and Zhu 2009; Agrawal et al.2009]。

In recommender systems research, Smyth and McClave [2001] suggested measuring the diversity of a recommendation list R (|R| > 1) as the average pairwise distance between items in the list:
R| > 1) as the average pairwise distance between items in the list:

$$
\tag{1}
$$

Similarly, Ziegler et al.[2005] defined the “intra-list similarity” metric as the aggregate (rather than the average) pairwise similarity of items in the list, with higher scores denoting lower diversity of the list.
同様に、Zieglerら[2005]は「リスト内類似度」指標をリスト内の項目の（平均ではなく）ペアワイズ類似度の総和と定義し、スコアが高いほどリストの多様性が低いことを示す。

Measuring diversity as the average or aggregate dissimilarity of items in the recommendation list has been widely adopted in the RS literature.
多様性の測定は、推奨リスト内の項目の平均的または集約的な非類似度として、RSの文献で広く採用されている。
What often differs is the item distance function that is used (dist(i, j) in Equation (1)).
しばしば異なるのは、使用される項目距離関数である（式（1）のdist(i, j)）。
For instance, where items are represented by content descriptors, the distance between items has been measured using a taxonomy-based metric [Ziegler et al.2005], the complement of Jaccard similarity [Vargas and Castells 2011], or the complement of cosine similarity on term vectors [Ekstrand et al.2014].
例えば、項目がコンテンツ記述子によって表現される場合、項目間の距離は、分類法に基づくメトリック[Ziegler et al.2005]、Jaccard類似度の補数[Vargas and Castells 2011]、または用語ベクトル上の余弦類似度の補数[Ekstrand et al.2014]を使用して測定されている。
Alternatively, where items are represented by rating vectors, item distance has been measured using Hamming distance [Kelly and Bridge 2006], the complement of Pearson correlation [Vargas and Castells 2011], or the complement of cosine similarity [Ribeiro et al.2012].
あるいは、項目が評価ベクトルで表現されている場合、項目距離はハミング距離[Kelly and Bridge 2006]、ピアソン相関の補数[Vargas and Castells 2011]、コサイン類似度の補数[Ribeiro et al.2012]を使って測定されている。

Yu et al.[2009] suggested measuring item distance using the neighborhoods that are used for rating prediction in collaborative filtering (CF).
Yuら[2009]は協調フィルタリング(CF)の評価予測に用いられる近傍領域を用いて項目距離を測定することを提案している。
In the case of item-based CF, each recommended item is represented by a neighborhood of items, while in the case of user-based CF, an item is represented by a neighborhood of users who rated the item.
アイテムベースCFの場合、各推奨アイテムはアイテムの近傍によって表現され、ユーザーベースCFの場合、アイテムはそのアイテムを評価したユーザーの近傍によって表現される。
Item distance can then be computed as, for example, the complement of Jaccard or cosine similarity between the two items’ neighborhoods.
アイテム距離は、例えば、2つのアイテムの近傍間のJaccardまたはcosine類似度の補数として計算することができる。

Finally, item distance can also be obtained from the latent feature vectors in matrix factorization approaches [Vargas et al.2011; Willemsen et al.2011; Shi et al.2012; Su et al.2013].
最後に、項目距離は行列因数分解アプローチで潜在特徴ベクトルから求めることもできる[Vargas et al.2011; Willemsen et al.2011; Shi et al.2012; Su et al.2013]。

Diversity metrics based on item dissimilarity were criticized by Vargas et al.[2014], who argued that the metrics fail to ensure that lists with high metric values will also be perceived by users as diverse.
項目の非類似度に基づく多様性メトリクスは、Vargasら[2014]によって批判され、メトリクス値が高いリストも多様であるとユーザーに認識されることを保証できないと主張した。
In domains where items can be described by sets of genres, Vargas et al.suggested using the genres for defining the diversity of an item list, arguing that genre diversity better corresponds to users’ perception of diverse recommendations.
アイテムがジャンルのセットで記述できるドメインでは、Vargasらは、ジャンルの多様性が多様なレコメンデーションに対するユーザーの知覚によりよく対応するとして、アイテムリストの多様性を定義するためにジャンルを使用することを提案した。
They proposed three criteria that a genre-based diversity metric should capture—coverage, redundancy, and size awareness.
彼らは、ジャンルに基づく多様性指標が捉えるべき3つの基準（網羅性、冗長性、サイズ認識）を提案した。
In other words, a diversity metric value should reflect how well a list of items covers the genres a user is interested in and how well genre redundancies are avoided.
言い換えれば、多様性メトリックの値は、アイテムのリストがユーザーの関心のあるジャンルをどれだけカバーしているか、ジャンルの冗長性がどれだけ回避されているかを反映するものでなければならない。
Moreover, it should be sensitive to the size of the recommendation list, since coverage and redundancy need to be treated differently for lists of different length.
さらに、推薦リストの長さが異なると、カバー率と冗長性の扱いが異なるため、推薦リストのサイズに敏感でなければならない。
Vargas et al.claimed that the optimal distribution of genres (in terms of diversity) is achieved when sampling items randomly.
Vargasらは、アイテムを無作為にサンプリングすることで、（多様性の点で）最適なジャンル分布が達成されると主張している。
This idea is similar to the “diversity by proportionality” information retrieval approach by Dang and Croft [2012], who considered a list of retrieved documents most diverse when the number of documents covering each topic is proportional to the topic’s popularity in the document corpus.
この考え方は、Dang and Croft [2012]による「比例による多様性」情報検索アプローチに似ている。彼らは、各トピックをカバーする文書の数が、文書コーパスにおけるトピックの人気度に比例する場合に、検索された文書のリストが最も多様になると考えた。
Vargas et al.suggested a probabilistic model to measure genre diversity in a recommendation list.
Vargasらは、推薦リストにおけるジャンルの多様性を測定する確率モデルを提案した。
They proposed a “binomial diversity” metric that captures how closely the genre distribution in the item list matches the distribution that would be obtained by randomly sampling items from the dataset.
彼らは、アイテムリストのジャンル分布が、データセットからランダムにアイテムをサンプリングした場合に得られる分布にどれだけ近いかを捉える「二項多様性」メトリックを提案した。
Since the balance between the diversity and accuracy of results is a widely discussed topic in information retrieval and recommender systems research, some works defined metrics that combine diversity and relevance.
情報検索や推薦システムの研究において、結果の多様性と正確性のバランスは広く議論されているトピックであるため、多様性と関連性を組み合わせたメトリクスを定義した研究もある。
For instance, in IR research, Clarke et al.[2008] described α-nDCG—a diversity-aware ranking measure, where the score of retrieved documents is penalized if they share features with documents ranked higher in the list.
例えば、IR研究において、Clarkeら[2008]はα-nDCGという多様性を考慮したランキング尺度を提案している。
In RS research, Vargas and Castells [2011] proposed a framework in which the diversity of a recommendation list can be computed with a relevance and ranking discount.
RS研究では、VargasとCastells [2011]が、推薦リストの多様性を関連性とランキング割引で計算できるフレームワークを提案した。
The authors argued that irrelevant recommendations add little to the perceived diversity of a recommender, making it necessary to weight the diversity score with the items’ relevance.
著者らは、関連性のないレコメンデーションはレコメンデーションの多様性にほとんど寄与しないため、アイテムの関連性で多様性スコアを重み付けする必要があると主張した。

Other diversity definitions, not referring to the quality of a single recommendation list, can also be found in the RS literature.
単一の推薦リストの品質に言及しない多様性の定義は、RSの文献にも見られる。
For instance, Lathia et al.[2010] analyzed how recommendations generated for the same user change over time.
例えば、Lathiaら[2010]は、同じユーザーに対して生成されたレコメンデーションが時間とともにどのように変化するかを分析した。
They defined “temporal diversity” as the normalized set theoretic difference between top-N recommendation lists received by the same user at two different time points.
彼らは「時間的多様性」を、2つの異なる時点で同じユーザーが受け取ったトップNの推薦リスト間の正規化された集合論的差異と定義した。
Averaging the values across all users gives an estimate of the system’s ability to provide users with diverse recommendations over time.
全ユーザーの値を平均することで、システムがユーザーに多様なレコメンデーションを提供する能力の推定値が得られる。
Diversity has also been defined from a system-centric perspective, for example, as the average pairwise distance between recommendation lists generated for different users [Zhou et al.2010; Liu et al.2012].
多様性は、システム中心の観点からも定義されており、例えば、異なるユーザーに対して生成された推薦リスト間の平均ペアワイズ距離として定義されている[Zhou et al.2010; Liu et al.2012]。
These definitions do not fit the view of diversity that we adopt in this article.
これらの定義は、本稿で採用するダイバーシティの考え方にはそぐわない。
Therefore, in the next section, we focus on works that optimize the diversity of an individual user’s recommendation list.
そこで次のセクションでは、個々のユーザーの推薦リストの多様性を最適化する研究に焦点を当てる。

## Increasing Diversity 多様性を高める

Most diversification techniques in the RS (and also IR) literature are based on reranking the result lists generated by existing recommendation (and retrieval) algorithms to increase their diversity while maintaining relevance.
RS（およびIR）の文献における多様化技術のほとんどは、既存の推薦（および検索）アルゴリズムによって生成された結果リストを、関連性を維持しながら多様性を高めるために再ランク付けすることに基づいている。
Another group of approaches includes works that define new models for diversity-oriented recommendation.
また、多様性を重視した推薦のための新しいモデルを定義した研究もある。
We discuss both groups of techniques in detail.
この2つのテクニックについて詳しく説明する。

### Recommendation Reranking for Diversity. 多様性のための再ランキング

The reranking diversification approaches produce a list of recommended items R of size N from a larger set of candidate recommendations C (|C| > N).
C| > N).
The candidates C are generated by an existing recommendation algorithm (e.g., user-based collaborative filtering), and hence have been chosen for their relevance.
候補Cは、既存の推薦アルゴリズム（例えば、ユーザーベースの協調フィルタリング）によって生成され、したがって、その関連性のために選択されている。
Reranking typically follows a greedy strategy: at each iteration, the item in C that maximizes an objective function is moved from C to result list R.
各反復において、目的関数を最大化するCの項目がCから結果リストRに移動される。
The objective function is defined as a combination of an item’s relevance and its relative diversity with respect to items already in the result list R.
目的関数は、アイテムの関連性と、すでに結果リストRにあるアイテムに対する相対的な多様性の組み合わせとして定義される。
The greedy reranking is illustrated in Algorithm 1.
貪欲なリランキングはアルゴリズム1に示されている。

One of the early diversification techniques to use greedy reranking is the Maximal Marginal Relevance (MMR) approach proposed by Carbonell and Goldstein [1998] in the IR literature.
貪欲な再ランク付けを使用する初期の多様化手法の1つは、IRの文献でCarbonellとGoldstein [1998]によって提案された最大限界関連性（MMR）アプローチである。
The MMR approach defined the objective function fobj as a linear combination of the item’s relevance and the negative of its maximum similarity to items already in the result list.
MMRアプローチでは、目的関数fobjをアイテムの関連性と、すでに結果リストにあるアイテムとの最大類似度の負の線形結合として定義した。
The greedy reranking technique has been adopted by a number of recommendation approaches [Smyth and McClave 2001; Ziegler et al.2005; Kelly and Bridge 2006], which defined the objective reranking function as a linear combination of the item’s relevance and its average distance to items already in the result list:
SmythとMcClave 2001; Ziegler et al.2005; Kelly and Bridge 2006]は、アイテムの関連性と、すでに結果リストにあるアイテムとの平均距離の線形結合として、目的の再ランク関数を定義した：

$$
\tag{2}
$$

In the equation, rel(i) denotes the item’s relevance and parameter α controls the tradeoff between the influence of relevance and diversity in the reranking procedure.
式中、rel(i)は項目の関連性を表し、パラメータαは再ランク付け手順における関連性と多様性の影響のトレードオフを制御する。
Similarly to the diversity metric (see Section 2.1, Equation (1)), the distance between two items dist(i, j) can be computed using a variety of approaches.
多様性メトリック（セクション2.1、式(1)参照）と同様に、2つのアイテム間の距離dist(i, j)は、様々なアプローチを用いて計算することができる。
Smyth and McClave [2001] applied the technique in a case-based recommender where, given a user’s query, the database of cases is searched to retrieve the most relevant cases.
Smyth and McClave [2001]は、ユーザのクエリが与えられると、最も関連性の高いケースを検索するためにケースのデータベースが検索されるケースベースのレコメンダーにこの技術を適用した。
In this setting, rel(i) represents the similarity between the user’s query and a case, while dist(i, j) is the complement of the similarity between two cases.
この設定において、rel(i)はユーザーのクエリとケースの類似度を表し、dist(i, j)は2つのケースの類似度の補数である。
Ziegler et al.[2005] applied the reranking technique for book recommendation, where the list of recommendations is generated based on the user’s rating profile (i.e., using a CF algorithm).
Zieglerら[2005]は書籍推薦にリランキング技術を応用し、ユーザーの評価プロファイルに基づいて推薦リストを生成している（つまりCFアルゴリズムを使っている）。
The authors defined rel(i) as the item’s relevance predicted by the recommender, and dist(i, j) as the distance between two items, this being obtained from a genre taxonomy-based metric.
著者らはrel(i)をレコメンダーによって予測されたアイテムの関連性と定義し、dist(i, j)を2つのアイテム間の距離と定義した。
Ziegler et al.were also the first to conduct a user study analyzing the impact of diversification on user satisfaction with the recommendation list (see Section 6).
また、Zieglerらは、多様化が推奨リストに対するユーザーの満足度に与える影響を分析した最初のユーザー研究を行った（セクション6参照）。
Kelly and Bridge [2006] applied the greedy reranking strategy in a conversational CF recommender, where recommendations are presented to a user through a series of interaction cycles—after receiving a set of recommendations, the user provides feedback, which influences the next set of recommendations.
KellyとBridge [2006]は、会話型CFレコメンダーに貪欲な再ランク戦略を適用し、レコメンデーションが一連のインタラクションサイクルを通じてユーザーに提示される。
The dialog is repeated until the user is satisfied with the provided recommendations.
このダイアログは、ユーザーが提供された推薦文に満足するまで繰り返される。
The authors proposed to diversify the set of recommendations at each interaction cycle, with rel(i) as the predicted item’s relevance and dist(i, j) computed as the normalized Hamming distance of the two items’ binary rating vectors.
著者らは、rel(i)を予測されたアイテムの関連性、dist(i, j)を2つのアイテムの2値評価ベクトルの正規化ハミング距離として計算し、各交流サイクルで推薦のセットを多様化することを提案した。
The setting of conversational recommendations poses additional challenges for result diversification.
会話型レコメンデーションの設定は、結果の多様化にとってさらなる課題となる。
McGinty and Smyth [2003] pointed out that the level of diversity can be varied in different recommendation cycles.
McGinty and Smyth [2003]は、推薦サイクルによって多様性のレベルを変えることができると指摘している。
The authors described a system where at each recommendation cycle, the user selects the best-quality recommendation, which is used as a query for the next cycle.
著者らは、推薦サイクルごとに、ユーザーが最も質の高い推薦を選択し、それが次のサイクルのクエリーとして使用されるシステムを説明した。
The selected recommendation is carried over to the next cycle and displayed alongside the newly generated recommendations.
選択されたレコメンデーションは次のサイクルに引き継がれ、新しく生成されたレコメンデーションとともに表示される。
If the user selects the carry-over item again, the system concludes that no progress toward the user’s goal has been made and injects more diversity in the next cycle.
ユーザーがキャリーオーバーの項目を再度選択した場合、システムはユーザーの目標に向けた進展がなかったと判断し、次のサイクルでさらに多様性を注入する。
If, however, the user selects a recommendation different from the carry-over item, the system assumes positive progress has been made and generates more similar recommendations for the next cycle.
しかし、ユーザーが繰り越し項目とは異なる推薦を選択した場合、システムは積極的な進歩があったとみなし、次のサイクルに向けてより類似した推薦を生成する。
Recent work on recommendation reranking for diversity has focused on designing more advanced objective functions that combine item relevance and diversity.
多様性を考慮したレコメンデーション・リランキングに関する最近の研究では、アイテムの関連性と多様性を組み合わせた、より高度な目的関数の設計に焦点が当てられている。
For example, Vargas et al.[2011] suggested applying diversification techniques and metrics from IR research to the recommender systems domain.
例えば、Vargasら[2011]は、IR研究の多様化技術や指標をレコメンダーシステム領域に適用することを提案している。
They adopted the objective function from the IA-Select approach proposed by Agrawal et al.[2009].
彼らは、Agrawalら[2009]が提案したIA-Selectアプローチの目的関数を採用した。
IA-Select is a probabilistic model similar to the greedy reranking approach (see Algorithm 1), which assumes a feature space of information topics, such that both documents and user queries can be represented with a distribution over the feature space.
IA-Selectは、貪欲なリランキングアプローチ（アルゴリズム1を参照）に似た確率論的モデルであり、情報トピックの特徴空間を仮定し、文書とユーザークエリの両方を特徴空間上の分布で表現できるようにする。
The model defines an objective reranking function that considers both document relevance and topic distribution, thus avoiding topic redundancy in the result list.
このモデルは、文書の関連性とトピックの分布の両方を考慮する客観的な再ランク関数を定義し、結果リストにおけるトピックの冗長性を回避する。
To adapt the IA-Select model to a recommender setting, Vargas et al.suggested replacing the topic feature space with either item labels (e.g., genres) or the latent item feature space (extracted using a matrix factorization approach).
IA-Selectモデルをレコメンダー設定に適応させるために、Vargasらは、トピック特徴空間をアイテムラベル（ジャンルなど）または潜在アイテム特徴空間（行列因数分解アプローチを使って抽出）に置き換えることを提案した。
Other recent reranking work by Vargas et al.[2014] proposed a “binomial diversity” metric to measure genre diversity in a recommendation list (see previous section).
その他、Vargasら[2014]による最近のリランキング研究では、推薦リストにおけるジャンルの多様性を測定する「二項多様性」メトリックが提案されている（前節参照）。
The authors used greedy reranking with an objective function that combines item relevance with its relative binomial diversity (i.e., the difference in the binomial diversity of the result set before and after adding the item).
著者らは、項目の関連性と相対的な二項多様性（すなわち、項目を追加する前と後の結果集合の二項多様性の差）を組み合わせた目的関数を持つ貪欲な再ランク付けを使用した。
Barraza-Urbina et al.[2015] proposed another formulation of the objective function for the greedy reranking strategy.
Barraza-Urbinaら[2015]は、貪欲なリランキング戦略に対する目的関数の別の定式化を提案した。
They suggested explicitly controlling the level to which diversification promotes items that are dissimilar to the user’s profile items.
彼らは、多様化がユーザーのプロファイル項目と異なる項目を促進するレベルを明示的に制御することを提案した。
This was achieved by multiplying the diversity component ( 1 |R| j∈R dist(i, j) in Equation (2)) by a weighted combination of exploration and exploitation scores for item i: β · xploit(i) + (1 − β) · xplore(i).
R| j∈R dist(i, j) in Equation (2)) by a weighted combination of exploration and exploitation scores for item i: β · xploit(i) + (1 − β) · xplore(i).
The exploitation score xploit(i) measures the probability that items in the user’s profile that are similar to i have been highly rated by the user, and the exploration score xplore(i) captures the item’s average dissimilarity from the items in the user’s profile.
エクスプロイトスコアxploit(i)は、iに類似するユーザーのプロファイル内のアイテムがユーザーによって高く評価されている確率を測定し、エクスプロアスコアxplore(i)は、ユーザーのプロファイル内のアイテムからのアイテムの平均的な非類似度をキャプチャする。
The β parameter thus controls the balance between a more “safe” diversification, picking diverse items that are within the user’s known taste range, and a more “explorative” diversification, promoting serendipitous items (see Section 3).
βパラメータは、このように、ユーザーの既知の味覚の範囲内にある多様なアイテムを選ぶ、より「安全な」多様化と、セレンディピティアイテムを促進する、より「探索的な」多様化の間のバランスを制御する（セクション3参照）。
There are also reranking techniques that do not use a greedy reranking strategy.
貪欲なリランキング戦略を使わないリランキング技術もある。
Typically, they rely on solving optimization problems to find the optimal ranking for a list of candidate recommendations.
一般的には、最適化問題を解くことで、推薦候補リストの最適なランキングを見つける。
For instance, Zhang and Hurley [2008] used an item-based CF approach to compute an item-to-item similarity matrix and then solved a number of optimization problems to find the set of recommended items that maximizes the diversity while maintaining a certain level of accuracy.
例えば、ZhangとHurley [2008]は、項目ベースのCFアプローチを使って項目間の類似度行列を計算し、その後、一定の精度を維持しながら多様性を最大化する推奨項目の集合を見つけるために多くの最適化問題を解いた。
The authors used the term “item novelty” to denote the amount of additional diversity that an item brings to the recommendation set.
著者らは、あるアイテムが推薦セットにもたらす追加的な多様性の量を示すために、「アイテムの新規性」という用語を使用した。
Jambor and Wang [2010] proposed a generic constrained optimization framework that supports multiple beyond-accuracy objectives.
Jambor and Wang [2010]は、複数の精度を超える目標をサポートする汎用的な制約付き最適化フレームワークを提案した。
The authors suggested predicting item relevance scores using existing recommendation techniques and weighting them with utility weights.
著者らは、既存の推薦技術を用いて項目の関連性スコアを予測し、効用重みで重み付けすることを提案した。
Item relevance is specified as the main objective in the framework, and additional constraints can be defined for the utility weights to optimize for diversity or novelty (Section 4).
アイテムの関連性は、フレームワークの主な目的として指定され、多様性や新規性を最適化するために、ユーティリティの重みに追加の制約を定義することができる（セクション4）。

Ribeiro et al.[2012] proposed an optimization approach similar to recommendation reranking—rather than reordering recommendations generated by a single algorithm, they used the relevance scores predicted by different algorithms in a weighted combination to determine the final item utility score.
Ribeiroら[2012]は、レコメンデーションのリランキングに似た最適化アプローチを提案した。単一のアルゴリズムによって生成されたレコメンデーションを並べ替えるのではなく、異なるアルゴリズムによって予測された関連性スコアを重み付けされた組み合わせで使用し、最終的なアイテムの効用スコアを決定した。
They focused on three objectives— accuracy, diversity, and novelty—and hypothesized that a hybrid combination of different algorithms can provide a better balance of the objectives.
彼らは3つの目的-正確性、多様性、新規性-に焦点を当て、異なるアルゴリズムのハイブリッドな組み合わせが、目的のより良いバランスを提供できるという仮説を立てた。
The baseline algorithms used within the weighted combination included three variants of the matrix factorization approach, user-based and item-based nearest-neighbor approaches, a popularitybased approach, and simple content-based and demographic-based nearest-neighbor methods.
重み付けされた組み合わせの中で使用されたベースラインアルゴリズムは、行列因数分解アプローチの3つのバリエーション、ユーザーベースとアイテムベースの最近傍アプローチ、人気度ベースのアプローチ、単純なコンテンツベースと人口統計ベースの最近傍手法などである。
The weights for each algorithm were learned using a genetic algorithm.
各アルゴリズムの重みは、遺伝的アルゴリズムを用いて学習された。
Since the three objectives are potentially conflicting, the approach selected the weight combinations that are optimal on the Pareto frontier, that is, the solutions where none of the three objectives can be improved without hurting the other two.
3つの目的は相反する可能性があるため、このアプローチではパレートフロンティア上で最適となる重みの組み合わせを選択した。
Diversity and novelty were defined using the rank-aware metrics proposed by Vargas and Castells [2011].
多様性と新規性は、Vargas and Castells [2011]によって提案されたランクを意識した測定基準を用いて定義された。

### Diversity Modeling. 多様性のモデリング。

The reranking techniques described in the previous section treat recommendation algorithms as a “black box.” They work by postprocessing lists of items that are generated by the recommendation algorithms.
前節で説明したリランキング技術は、推薦アルゴリズムを "ブラックボックス "として扱う。それらは、推薦アルゴリズムによって生成されたアイテムのリストを後処理することによって機能する。
An obvious advantage of the reranking techniques is their ease of deployment in existing recommender systems, where a diversification component may be incorporated alongside existing recommendation algorithms and the level of diversification can be explicitly controlled.
リランキング技術の明らかな利点は、既存の推薦システムに容易に導入できることであり、多様化要素を既存の推薦アルゴリズムと一緒に組み込むことができ、多様化のレベルを明示的に制御することができる。
However, there is a growing body of research that addresses the diversification problem by defining new recommendation algorithms that directly optimize for diversity when generating recommendations.
しかし、推奨を生成する際に多様性を直接的に最適化する新しい推奨アルゴリズムを定義することで、多様化問題に取り組む研究が増えている。
These approaches mostly extend matrix factorization techniques, which have become the state-of-the-art recommendation methods in recent years.
これらのアプローチは、近年最先端の推薦手法となっている行列分解法を拡張したものである。
For instance, Shi et al.[2012] combined matrix factorization with the portfolio theory from IR proposed by Wang and Zhu [2009] (whose work in turn was inspired by the Modern Portfolio Theory from economics [Markowitz 1952]).
例えば、Shiら[2012]は、WangとZhu[2009]によって提案されたIRからのポートフォリオ理論（その研究は、経済学からの現代ポートフォリオ理論[Markowitz 1952]に触発されている）に行列分解を組み合わせた。
The IR portfolio theory considers the predicted document relevance as an uncertain outcome whose expected value may be over- or underestimated (due to query ambiguity, incomplete user profile, imperfect retrieval algorithm, etc.).Given the uncertainty of document retrieval, a probabilistic model is used to represent the expected overall relevance of the retrieved document list and its variance.
IRポートフォリオ理論では、予測される文書の関連性は、（クエリの曖昧さ、不完全なユーザプロファイル、不完全な検索アルゴリズムなどのために）期待値が過大または過小評価される可能性のある不確実な結果と考えられている。
The variance of the list represents the likelihood that the relevance of the documents was estimated incorrectly and is computed using the covariance of document relevance scores for each document pair in the list.
リストの分散は、文書の関連性が誤って推定された可能性を表し、リスト内の各文書ペアの文書関連性スコアの共分散を用いて計算される。
The covariance of document relevance scores can be approximated by term co-occurrence in the documents.
文書の関連性スコアの共分散は、文書内の用語の共起によって近似できる。
The basic idea of the portfolio theory is to minimize the risk of generating an item list with low relevance for the user.
ポートフォリオ理論の基本的な考え方は、ユーザーにとって関連性の低いアイテムリストを生成するリスクを最小化することである。
This is achieved by maximizing the expected relevance and minimizing the variance of the result list.
これは、期待される関連性を最大化し、結果リストの分散を最小化することによって達成される。
Shi et al.adapted this idea to a recommendation setting and defined an objective function that balances the predicted relevance and variance of the recommendation list.
Shi et al.はこの考え方を推薦の設定に適応させ、予測される関連性と推薦リストの分散のバランスをとる目的関数を定義した。
Differently from the IR work, where variance was approximated by term co-occurrence in documents, Shi et al.used latent factor vectors (obtained from the matrix factorization approach) to model the variance of recommendations.
分散が文書内の用語の共起によって近似されていたIRの仕事とは異なり、Shiらは潜在因子ベクトル（行列因数分解のアプローチから得られる）を使って推薦の分散をモデル化した。
An important aspect of the approach of Shi et al.is adapting the level of diversification to the user’s scope of tastes.
Shiらのアプローチの重要な点は、多様化のレベルをユーザーの嗜好の範囲に合わせることである。
They showed that the latent factors of a user who rates diverse items have higher variance compared to a user who rates similar items.
彼らは、多様な項目を評価するユーザーの潜在因子は、類似した項目を評価するユーザーに比べて分散が大きいことを示した。
This is reflected in the proposed model.
これは提案されたモデルに反映されている。
Therefore, a user who tends to rate similar items (e.g., only science fiction movies) will get less diversification compared to a user who rates diverse items (e.g., movies from different genres).
従って、似たような項目（例えば、SF映画のみ）を評価する傾向があるユーザーは、多様な項目（例えば、異なるジャンルの映画）を評価するユーザーと比較して、多様化が少なくなる。

Hurley [2013] presented a modification of the pairwise learning-to-rank approach for implicit feedback datasets.
Hurley[2013]は、暗黙的フィードバックデータセットに対するペアワイズ学習からランク付けへのアプローチの修正を発表した。
The original pairwise ranking model learns the user and item factors by minimizing an objective function defined on the difference between the predicted and original ranking for item pairs.
元のペアワイズ・ランキング・モデルは、アイテム・ペアの予測ランキングと元のランキングの差で定義される目的関数を最小化することによって、ユーザーとアイテムの要素を学習する。
In the modified diversity-aware version of the model, Hurley proposed including item dissimilarity in the objective function.
多様性を考慮したモデルの修正版において、Hurleyは項目の非類似度を目的関数に含めることを提案した。
Although the learning model is not sensitive to the size of recommendation list N (when generating top-N recommendations), an initial evaluation of the approach using the “intralist distance” metric [Smyth and McClave 2001; Ziegler et al.2005] (Equation (1)) showed promising results.
学習モデルは推薦リストNのサイズに敏感ではないが（トップNの推薦を生成する場合）、「リスト内距離」メトリック[Smyth and McClave 2001; Ziegler et al.2005]（式(1)）を用いたアプローチの初期評価は有望な結果を示した。
Su et al.[2013] proposed a pairwise learning-to-rank model that works at the item set level (rather than the individual item level).
Suら[2013]は、（個々の項目レベルではなく）項目集合レベルで動作するペアワイズ学習ランク付けモデルを提案した。
The training data is constructed by creating pairs of item sets.
学習データは、項目セットのペアを作成することによって構築される。
The model is trained by comparing each pair of item sets using both relevance and diversity criteria.
このモデルは、関連性と多様性の両方の基準を用いてアイテムセットの各ペアを比較することによって学習される。
Diversity of a set is included in the model through a “diversity bias” component, defined as the aggregate similarity of all item pairs in the set.
セットの多様性は、セット内のすべてのアイテム・ペアの類似度の集約として定義される「多様性バイアス」コンポーネントを通してモデルに含まれる。
The similarity of an item pair is computed as the product of the two items’ latent factor vectors.
項目ペアの類似度は、2つの項目の潜在因子ベクトルの積として計算される。

# Serendipity セレンディピティ

## Defining and Measuring Serendipity セレンディピティの定義と測定

Defining serendipity largely relies on the definition of its core component—surprise.
セレンディピティの定義は、その核となる要素である「驚き」の定義に大きく依存している。
In the cognitive science literature, surprise has been linked to events that are different from one’s expectations [Meyer et al.1997] or are difficult to explain [Foster and Keane 2013].
認知科学の文献では、驚きは自分の予想と異なる出来事[Meyer et al.1997]や説明が困難な出来事[Foster and Keane 2013]と関連している。
Such definitions are not trivial to operationalize in the information retrieval or recommender systems domain.
このような定義は、情報検索や推薦システムの領域で運用するのは容易ではない。
The first studies that recognized the importance of facilitating serendipity in information systems were reported in the IR literature [Toms 2000].
情報システムにおいてセレンディピティを促進することの重要性を認識した最初の研究は、IRの文献で報告された[Toms 2000]。
Rather than providing formal definitions of serendipity, early works analyzed the process of serendipitous information discovery and the paradox of designing for unexpected results [Foster and Ford 2003; McBirnie 2008].
初期の研究は、セレンディピティの正式な定義を提供するのではなく、セレンディピティによる情報発見のプロセスや、予期せぬ結果のためにデザインすることのパラドックスを分析していた[Foster and Ford 2003; McBirnie 2008]。
In the RS literature, Herlocker et al.[2004] informally defined a serendipitous recommendation as one that helps the user find a “surprisingly interesting item he might not have otherwise discovered.” In the RS literature, approaches designed to increase serendipity rely on various heuristics to generate more surprising recommendations.
RSの文献において、Herlockerら[2004]はセレンディピティ・レコメンデーション（serendipitous recommendation）を非公式に定義している。RSの文献では、セレンディピティを高めるためにデザインされたアプローチは、より驚くべき推薦を生成するために様々なヒューリスティックに依存している。
For instance, an item can be considered serendipitous if a classifier is uncertain about its relevance for the user [Iaquinta et al.2008], if the item is different from the user’s profile [Adamopoulos and Tuzhilin 2014], if the item is connected to a distinct area in a user-item graph [Onuma et al.2009; Nakatsuji et al.2010; Zhang et al.2012], or if the item possesses a mixture of two input items’ features [Oku and Hattori 2011] (see next section for details).
例えば、分類器がユーザとの関連性を不確かな場合[Iaquinta et al.2008]、ユーザのプロファイルと異なる場合[Adamopoulos and Tuzhilin 2014]、ユーザアイテムグラフの異なる領域に接続されている場合[Onuma et al.2009; Nakatsuji et al.2010; Zhang et al.2012]など、アイテムはセレンディピティとみなされる。 中辻ら2010; Zhangら2012]、またはアイテムが2つの入力アイテムの特徴の混合を持つ場合[奥と服部2011]（詳細は次のセクションを参照）。
When using offline experiments to evaluate the quality of results produced by these ad hoc approaches, a common practice among the authors is to compare the generated recommendations with recommendations produced by a primitive baseline system (i.e., one that is not optimized for serendipity).
これらのアドホックなアプローチによって生成された結果の品質を評価するためにオフライン実験を使用する場合、著者の間で一般的なプラクティスは、生成されたレコメンデーションと、プリミティブなベースラインシステム（すなわち、セレンディピティに最適化されていないシステム）によって生成されたレコメンデーションを比較することである。
This approach to measuring serendipity was first proposed by Murakami et al.[2008], who argued that a primitive method produces easily predictable items, while the goal of a serendipitous recommender is to suggest items that are difficult to predict.
セレンディピティを測定するこのアプローチは、村上ら[2008]によって最初に提案された。彼らは、原始的な方法は予測しやすいアイテムを作り出すが、セレンディピティ・レコメンダーの目標は予測しにくいアイテムを提案することであると主張した。
This idea was later adopted by Ge et al.[2010], who proposed a formulation of serendipity that combines this notion of unexpectedness with item relevance:
この考え方は後にGeら[2010]によって採用され、彼らはこの意外性の概念と項目の関連性を組み合わせたセレンディピティの定式化を提案した：

$$
\tag{3}
$$

where R is the set of recommendations generated for user u, Runexp is the subset of items in R that are unexpected for the user u, and Ruseful is the subset of items in R that are useful for the user.
ここで、Rはユーザーuのために生成された推奨のセットであり、Runexpはユーザーuにとって予期しないRのアイテムのサブセットであり、Rusefulはユーザーにとって有用なRのアイテムのサブセットである。
Following the idea of Murakami et al., the set of unexpected recommendations is obtained by subtracting from R items that are recommended by a primitive prediction model PM for user u: Runexp = R \ PMu.
村上らの考えに従い、ユーザーuに対する原始予測モデルPMが推奨するアイテムをRから引くことで、予期しない推奨の集合を得る： Runexp = R \ PMu.
The usefulness of recommendations may be judged by the user or, in an offline setting, approximated by the user’s ratings for the items [Adamopoulos and Tuzhilin 2014].
レコメンデーションの有用性は、ユーザーによって判断されるか、オフラインの設定では、アイテムに対するユーザーの評価によって近似される[Adamopoulos and Tuzhilin 2014]。
A limitation of this comparative approach to serendipity measurement is its sensitivity to the choice of the primitive baseline system.
セレンディピティ測定に対するこの比較アプローチの限界は、原始的なベースライン・システムの選択に敏感であることである。
Recently, Adamopoulos and Tuzhilin [2014] suggested another way to measure the unexpectedness of recommendations.
最近、AdamopoulosとTuzhilin [2014]は、レコメンデーションの意外性を測定する別の方法を提案した。
The authors defined Runexp as R\ Eu, where Eu is the set of expected recommendations for a user u, which contains items rated by the user and items that are similar to the rated ones (in terms of content similarity).
著者らは、RunexpをRpha Euと定義した。ここで、Euは、ユーザーuに対する期待されるレコメンデーションの集合であり、ユーザーによって評価されたアイテムと、（コンテンツの類似性の観点から）評価されたアイテムに類似するアイテムを含む。
Note that contrary to the original (informal) definition of serendipity by Herlocker et al.[2004], metrics like these—based on item unexpectedness—do not require serendipitous items to be novel to the user, but only relevant and different from the user’s expectations.
Herlockerら[2004]によるセレンディピティのオリジナルの（非公式な）定義に反して、アイテムの意外性に基づくこれらのようなメトリクスは、セレンディピティアイテムがユーザーにとって斬新である必要はなく、ユーザーの期待とは異なる関連性があればよいことに注意してください。
The idea of measuring an item’s unexpectedness as its distance from a set of expected items has been exploited by a few previous works.
アイテムの意外性を、予想されるアイテムの集合からの距離として測定するというアイデアは、いくつかの先行研究で利用されてきた。
Nakatsuji et al.[2010] proposed an approach based on a taxonomy of genres and defined what they called “item novelty” as the smallest distance (in the taxonomy) from the item’s genre to the genre of items previously accessed by user.
中辻ら[2010]は、ジャンルの分類法に基づくアプローチを提案し、彼らが「アイテムの新規性」と呼ぶものを、アイテムのジャンルと、ユーザーが過去にアクセスしたアイテムのジャンルとの（分類法上の）最小距離と定義した。
Vargas and Castells [2011], in their framework for measuring diversity and novelty, defined what they called a “personalized novelty” metric based on computing an item’s average distance from the user’s profile items.
VargasとCastells [2011]は、多様性と新規性を測定するためのフレームワークの中で、ユーザーのプロファイルアイテムからのアイテムの平均距離を計算することに基づいて、「パーソナライズされた新規性」と呼ばれるメトリックを定義しました。
In our experiments (see Section 7), we adopt the idea of measuring an item’s unexpectedness (or surprise) as its distance from the set of expected items.
我々の実験（セクション7参照）では、アイテムの意外性（または驚き）を、予想されるアイテムの集合からの距離として測定するという考え方を採用した。
Furthermore, we follow the idea of Nakatsuji et al.to measure an item’s surprise as the minimum distance from the user’s profile items and we hypothesize that, by contrast, averaging the distances between items results in a loss of information, particularly for users with diverse profiles [Kaminskas and Bridge 2014].
さらに、我々は中辻らの考えに従い、アイテムの驚きをユーザーのプロファイル・アイテムからの最小距離として測定し、対照的に、アイテム間の距離を平均化すると、特に多様なプロファイルを持つユーザーにとって、情報の損失につながるという仮説を立てる[Kaminskas and Bridge 2014]。

## Increasing Serendipity セレンディピティを高める

The first attempts to increase the serendipity of retrieved results were reported in the IR literature.
検索結果のセレンディピティを高める最初の試みは、IRの文献で報告されている。
For example, Campos and de Figueiredo [2001] designed a software agent to support serendipitous information discovery through web crawling.
例えば、Campos and de Figueiredo [2001]は、ウェブクローリングによるセレンディピティな情報発見を支援するソフトウェアエージェントを設計した。
Andre´ et al.[2009] suggested viewing serendipity as a combination of chance discovery and usefulness of the discovered information.
Andre´ら[2009]は、セレンディピティを偶然の発見と発見された情報の有用性の組み合わせとして捉えることを提案している。
They provided guidelines to design information systems with better support for both components of serendipity: supporting chance encounters and enhancing the user’s ability to recognize serendipitous content.
彼らは、セレンディピティの両要素、すなわち偶然の出会いをサポートすることと、セレンディピティなコンテンツを認識するユーザーの能力を高めることを、よりよくサポートする情報システムを設計するためのガイドラインを提供した。
In the RS literature, Iaquinta et al.[2008] were among the first to introduce serendipity in a recommender system.
RSの文献では、Iaquintaら[2008]が推薦システムにセレンディピティを導入した最初の一人である。
They described a content-based recommender with items represented by text descriptions.
彼らは、テキスト記述で表現されたアイテムを持つコンテンツベースのレコメンダーについて述べた。
A supervised learning method was used to predict the probability that an unseen item was either relevant or nonrelevant to the user.
教師あり学習法を用いて、未見のアイテムがユーザーにとって関連または非関連である確率を予測した。
Items for which the classification outcome was uncertain (i.e., where the absolute difference between the two probabilities was large) were considered as potentially serendipitous and were included in the recommendations.
分類結果が不確実な項目（すなわち、2つの確率の差の絶対値が大きい項目）は、セレンディピティの可能性があるとみなし、推奨項目に含めた。
Onuma et al.[2009] designed a system that uses a graph-based algorithm for supporting surprising recommendations.
大沼ら[2009]は、グラフベースのアルゴリズムを用いて、意外性のあるレコメンデーションを支援するシステムを設計した。
The authors introduced the idea of computing a “bridging score” for item nodes in the user-item bipartite graph.
著者らは、ユーザー-項目二部グラフの項目ノードの「橋渡しスコア」を計算するというアイデアを紹介した。
Nodes connecting separate interconnected areas in the graph receive high bridging scores as they bridge different subspaces in the item information space.
グラフの別々の相互接続領域を結ぶノードは、アイテム情報空間の異なる部分空間を橋渡ししているため、高い橋渡しスコアを受ける。
The bridging score may be combined with an item relevance score when generating recommendations.
ブリッジングスコアは、レコメンデーションを生成する際に、アイテムの関連性スコアと組み合わされることがある。
Another graph-based approach was proposed by Nakatsuji et al.[2010].
中辻ら[2010]によって提案されたグラフベースのアプローチもある。
They applied a Random Walk algorithm on a user similarity graph to identify users that are related (but not too similar) to the target user, arguing that such users provide a good source of surprising recommendations.
彼らは、ユーザーの類似性グラフにランダムウォークアルゴリズムを適用して、ターゲットユーザーと関連性のある（しかしあまり似ていない）ユーザーを特定し、そのようなユーザーは意外な推薦の良い情報源になると主張している。
Oku and Hattori [2011] presented a system that induced possibly serendipitous recommendations by selecting items whose content is a mixture of the content features of two items from the user’s profile.
奥・服部[2011]は、ユーザのプロフィールから2つのアイテムの内容の特徴を混合したアイテムを選択することで、セレンディピティの可能性があるレコメンデーションを誘導するシステムを発表した。
Zhang et al.[2012] presented a music recommender for Last.fm artists that uses a generative Latent Dirichlet Allocation (LDA) model to build latent clusters of Last.fm users and to represent artists by a distribution over these clusters.
Zhangら[2012]は、Last.fmアーティストのための音楽レコメンダーを発表した。このレコメンダーは、Last.fmユーザーの潜在的なクラスタを構築し、これらのクラスタ上の分布によってアーティストを表現するために、生成的なLDA（Latent Dirichlet Allocation）モデルを使用している。
Representing artists as LDA vectors gives a way of computing a similarity score between any artist and the artists in a user’s listening profile.
アーティストをLDAベクトルとして表現することで、任意のアーティストとユーザーのリスニングプロファイル内のアーティストとの間の類似度スコアを計算する方法が得られます。
Moreover, the vector representation allows artists to be clustered.
さらに、ベクトル表現によってアーティストのクラスタリングが可能になる。
The recommender generates serendipitous recommendations by promoting artists that are outside of the user’s “musical bubbles” (clusters of liked artists).
このレコメンダーは、ユーザーの "音楽の泡"（好きなアーティストのクラスタ）の外にいるアーティストを宣伝することで、セレンディピティなレコメンデーションを生成する。
Finally, Adamopoulos and Tuzhilin [2014] presented an approach to recommend serendipitous items based on how distant they are from the set of items expected by the user.
最後に、AdamopoulosとTuzhilin [2014]は、ユーザーが期待するアイテムのセットからどれだけ離れているかに基づいてセレンディピタスアイテムを推薦するアプローチを提示した。
The authors defined an item utility function as a linear combination of the item’s relevance score (predicted by a standard recommendation algorithm, e.g., a collaborative filtering approach) and its unexpectedness (computed as a distance between the item and a set of expected items).
著者らは、項目の効用関数を、項目の関連性スコア（協調フィルタリングアプローチなどの標準的な推薦アルゴリズムによって予測される）と、項目の意外性（項目と予想される項目のセットとの間の距離として計算される）の線形結合として定義した。
The set of expected items includes items rated by the target user and items similar to the rated ones in terms of content (e.g., in a movie domain, movies produced by the same director and belonging to the same genre).
期待されるアイテムのセットには、ターゲットユーザーによって評価されたアイテムや、評価されたアイテムと内容的に類似したアイテム（例えば、映画領域では、同じ監督によって制作され、同じジャンルに属する映画）が含まれる。
For computing the distance between an item and a set of items, the authors suggested averaging the individual distance values or computing the centroid of the set and measuring the target item’s distance from the centroid.
アイテムとアイテムのセット間の距離を計算するために、著者らは個々の距離値を平均化するか、セットの重心を計算し、重心からのターゲットアイテムの距離を測定することを提案した。
Both rating- and contentbased distance metrics were evaluated.
評価指標と内容ベースの距離指標の両方が評価された。
Given the target user and a set of the user’s expected items, the proposed recommendation approach computes the utility score for each candidate item and recommends those with the highest utility values.
ターゲットユーザとユーザが期待するアイテムの集合が与えられると、提案された推薦アプローチは、各候補アイテムの効用スコアを計算し、最も高い効用値を持つアイテムを推薦する。

## Novelty ノベルティ

Novelty is closely related to serendipity, discussed in the previous section.
新規性は、前節で述べたセレンディピティと密接な関係がある。
Here, we first discuss the relation between these two objectives and motivate our choice of novelty definition.
ここではまず、この2つの目的の関係について説明し、新規性の定義を選択する動機付けとする。
Subsequently, we discuss research that addressed novelty optimization in recommender systems.
続いて、レコメンダーシステムにおける新規性最適化を扱った研究について述べる。

## Defining and Measuring Novelty 目新しさの定義と測定

Similarly to other objectives discussed in this work, the definition of novelty in the RS literature is inspired by IR research.
本作品で論じた他の目的と同様に、RS文献における新規性の定義はIR研究に触発されたものである。
Baeza-Yates and Ribeiro-Neto [1999] were among the first to discuss novelty as an important quality in information retrieval.
Baeza-YatesとRibeiro-Neto [1999]は、情報検索における重要な品質として新規性を最初に論じた。
They defined the novelty of a set of retrieved documents as the fraction of relevant documents that are unknown to the user.
彼らは、検索された文書集合の新規性を、ユーザーにとって未知の関連文書の割合と定義した。
Another view on novelty was offered by Zhang et al.[2002], who considered the novelty of a single retrieved document as the opposite of its redundancy.
新規性についての別の見解は、Zhangら[2002]によって提供され、彼は検索された一つの文書の新規性をその冗長性の反対と考えた。
They proposed a number of redundancy metrics based on the distance between the document and documents previously seen by the user.
彼らは、文書とユーザーが以前に見た文書との間の距離に基づく多くの冗長性メトリックを提案した。
The aforementioned views of novelty are both related to how novelty is commonly perceived—“the quality or state of being new, different, and interesting.”2 Definitions of novelty in the RS literature typically focus on two aspects of novelty—an item being unknown to the user and an item being different from what the user has seen before.
前述の新規性についての考え方は、いずれも新規性が一般的にどのように認識されているかということ、つまり「新しい、異なる、興味深い」という性質や状態に関連している2。
Some works focused only on the latter aspect and proposed novelty metrics that measure an item’s distance from the user’s profile (i.e., previously seen items) [Yang and Li 2005; Nakatsuji et al.2010].
いくつかの研究は後者の側面だけに注目し、ユーザーのプロファイル（つまり、以前に見たアイテム）からのアイテムの距離を測定する新規性のメトリクスを提案しました[Yang and Li 2005; Nakatsuji et al.2010]。
Vargas and Castells [2011] proposed different variants of a novelty metric that support both the unknown and the different aspects of novelty.
VargasとCastells [2011]は、新規性の未知の側面と異なる側面の両方をサポートする新規性メトリックの異なるバリエーションを提案した。
Zhang [2013] identified three qualities of a novel recommendation: being unknown to the user, being relevant to the user, and being dissimilar to items in the user’s profile.
Zhang[2013]は、新しい推薦の3つの質を特定した：ユーザーにとって未知であること、ユーザーに関連性があること、そしてユーザーのプロファイルにあるアイテムに類似していないこと。
We note that the quality of an item being different from the user’s profile is closely related to the surprise of recommendations, which we identify as a core component of serendipity (see Section 3).
アイテムの質がユーザーのプロフィールと異なることは、セレンディピティの核となる要素であるレコメンデーションのサプライズと密接に関係している（セクション3参照）。
As discussed in Section 1, novelty and serendipity are closely related and their definitions in the literature often overlap.
セクション1で述べたように、新規性とセレンディピティは密接に関連しており、文献上の定義もしばしば重複している。
A distinction between the two objectives was proposed by Herlocker et al.[2004], who argued that a novel item does not have to be surprising, but only unknown to the user.
Herlockerら[2004]は、この2つの目的を区別することを提案し、新奇なアイテムは驚くべきものである必要はなく、ユーザーにとって未知のものであればよいと主張した。
Kapoor et al.[2015] extended the definition of novel items to include those that are known but forgotten by the user (i.e., items the user has not accessed in a while).
Kapoorら[2015]は、新規アイテムの定義を拡張し、既知だがユーザーが忘れてしまったアイテム（ユーザーがしばらくアクセスしていないアイテム）を含めるようにした。
A “temporal novelty” formulation like this one is only applicable to domains with frequent repeated item consumption, for example, music recommendation.
このような「時間的新規性」定式化は、例えば音楽推薦のような、アイテム消費が頻繁に繰り返されるドメインにのみ適用可能である。
To better structure the discussion of serendipity and novelty, in this section we follow the definition of Herlocker et al.[2004] and view novel recommendations only as those that are unknown to the user.
セレンディピティと新規性の議論をよりよく構成するために、このセクションではHerlocker et al.
The quality of an item being unknown is not trivial to define formally.
アイテムが未知であることの質を正式に定義するのは容易ではない。
While a typical recommender provides a user with suggestions for unrated items, an absent rating does not necessarily imply an unknown item—a user rarely provides ratings for all known items.
一般的なレコメンダーは、未評価のアイテムに対するサジェストをユーザーに提供するが、評価がないからといって必ずしも未知のアイテムであるとは限らない。
Therefore, without acquiring the user’s feedback (e.g., through a user study), it is impossible to know if an unrated item is truly novel.
したがって、（ユーザー調査などを通じて）ユーザーのフィードバックを得なければ、未評価の項目が本当に目新しいかどうかを知ることはできない。
Hijikata et al.[2009] proposed a CF system where two types of rating profiles were created for each user— the traditional rating profile, containing the item preferences, and the “acquaintance profile,” containing binary ratings of item familiarity (i.e., “known/unknown”).
土方ら[2009]は、各ユーザに2種類の評価プロファイルを作成するCFシステムを提案した。すなわち、アイテムの嗜好を含む従来の評価プロファイルと、アイテムの馴染み度（すなわち「知っている／知らない」）の二値評価を含む「知り合いプロファイル」である。
The authors suggested a number of hybrid CF algorithms exploiting the two types of profiles to generate both unknown and accurate recommendations.
著者らは、未知のレコメンデーションと正確なレコメンデーションの両方を生成するために、2つのタイプのプロファイルを利用した多くのハイブリッドCFアルゴリズムを提案した。
The approach, although explicitly addressing the issue of item novelty, doubles the cognitive load of user profile construction as the users need to provide both types of ratings.
このアプローチは、項目の新規性の問題に明確に対処しているが、ユーザーが両方のタイプの評価を提供する必要があるため、ユーザープロファイル構築の認知的負荷が倍増する。
More commonly, an item’s novelty is approximated using its popularity among users of the recommender system—the less popular an item is, the more likely it is to be unknown to the user.
より一般的には、アイテムの新規性はレコメンダーシステムのユーザー間での人気度を使って近似される。
Although an item’s unpopularity is not always a good indication of it being unknown—a user familiar with one rare item is likely to know similar rare items [Celma 2009]—it provides a cheap approximation for measuring novelty offline, without conducting costly user studies.
アイテムの不人気は、それが未知であることの良い兆候とは限らないが、-あるレアアイテムに精通しているユーザーは、同様のレアアイテムを知っている可能性が高い[Celma 2009]-コストのかかるユーザー調査を実施することなく、オフラインで新規性を測定するための安価な近似値を提供する。
Item popularity has been estimated using rating variance [Jambor and Wang 2010] in the dataset or using external sources of information, such as box office earnings for movies [Oh et al.2011].
項目の人気度は、データセットの評価分散[Jambor and Wang 2010]を使用するか、映画の興行収入[Oh et al.2011]などの外部情報源を使用して推定されている。
However, the most common approach is based on the number of ratings an item has received from users.
しかし、最も一般的なアプローチは、アイテムがユーザーから受けた評価の数に基づいている。
Formally, then, novelty is typically defined as the complement of the item’s popularity in the dataset: 1 − p(i), where p(i) = |{u∈U,rui=∅}| |U| is the fraction of users who rated item i.
{u∈U,rui=∅}
A slight variation is to define novelty as the negative of the log of the ratio: − log p(i).
若干のバリエーションとして、新規性を比率の対数の負の値として定義することもできる： - log p(i)。
This formulation is called the self-information of an item i [Zhou et al.2010; Vargas and Castells 2011] and, compared to the simple complement of popularity, gives more importance to very rare items.
この定式化は、アイテムiの自己情報と呼ばれ[Zhou et al.2010; Vargas and Castells 2011]、単純な人気の補完と比較して、非常にまれなアイテムをより重視する。
In order to evaluate recommendation techniques with respect to novelty, the novelty of individual recommendations is aggregated into a single score for a list of recommendations R:
新規性に関して推薦技術を評価するために、個々の推薦の新規性は推薦のリストRに対して単一のスコアに集約される：

$$
\tag{4}
$$

Given the previous definition of novelty, novel items are identified with the “long tail” items, that is, the part of the item catalog seen (rated or purchased) by a small part of the user community [Anderson 2006].
前述の新規性の定義を踏まえると、新規性のあるアイテムは「ロングテール」アイテム、つまりアイテムカタログのうち、ユーザーコミュニティのごく一部によって見られる（評価される、または購入される）部分と識別される[Anderson 2006]。
A detailed analysis of the long-tail phenomenon and its influence on recommendation novelty was given by Celma [2009].
ロングテール現象とそのレコメンデーションの新規性への影響については、Celma [2009]が詳細に分析している。
Celma analyzed the long-tail item distribution and its relation to item similarity in a music recommender.
Celmaは、音楽レコメンダーにおけるロングテール項目の分布と項目の類似度との関係を分析した。
The recommender system was modeled as a fully connected graph with nodes representing items; edges were weighted by similarities between items.
レコメンダーシステムは、アイテムを表すノードを持つ完全連結グラフとしてモデル化され、エッジはアイテム間の類似性によって重み付けされた。
Two versions of the recommender were analyzed—an item-based CF approach and a content-based (CB) approach.
項目ベースのCFアプローチとコンテンツベース（CB）のアプローチである。
The item similarities on the edges were rating based for the CF system and content based for the CB system.
エッジの項目の類似性は、CFシステムではレーティングベース、CBシステムではコンテンツベースであった。
Celma compared the long-tail distribution of item popularity with the item similarity graph and showed that, in the CF system, popular items tend to form highly interconnected clusters in the graph, meaning that the long-tail (i.e., novel) items are difficult to reach and therefore difficult to recommend to users.
Celmaは、アイテムの人気度のロングテール分布とアイテムの類似度グラフを比較し、CFシステムでは、人気アイテムはグラフ内で高度に相互接続されたクラスターを形成する傾向があり、ロングテール（すなわち新規）アイテムは到達しにくく、したがってユーザーに推薦しにくいことを示した。
Conversely, in the CB system, item connections in the graph are independent of their popularity, therefore making CB recommendations more novelty oriented.
逆に、CBシステムでは、グラフ内のアイテムのつながりはその人気度とは無関係であるため、CBレコメンデーションはより新規性重視のものとなる。

## Increasing Novelty 目新しさを増す

Based on the definition of novelty adopted in this work (i.e., based on item popularity), in this section, we focus on works that increase recommendation novelty by promoting rare items (also known as the “long tail” items).
このセクションでは、この研究で採用された新規性の定義（すなわち、アイテムの人気度に基づく）に基づき、レアアイテム（「ロングテール」とも呼ばれる）を促進することでレコメンデーションの新規性を高める作品に焦点を当てる。
One of the early efforts to analyze the long-tail phenomenon in recommender systems was presented by Park and Tuzhilin [2008].
レコメンダーシステムにおけるロングテール現象を分析した初期の取り組みのひとつが、Park and Tuzhilin [2008]によって発表された。
Although not directly related to novelty optimization, this work dealt with improving rating prediction accuracy for the long-tail items.
新規性の最適化とは直接関係ないが、この研究ではロングテール項目の視聴率予測精度の向上を扱った。
They observed that when using rating-based prediction algorithms, prediction accuracy for rare items is lower than for popular items (caused by the smaller number of ratings on which the prediction is based).
彼らは、レーティングベースの予測アルゴリズムを使用した場合、レアアイテムの予測精度が人気アイテムよりも低くなることを観察した（予測のベースとなるレーティングの数が少ないことが原因）。
Their suggested solution for improving the prediction accuracy was based on clustering the long-tail items and creating joint rating profiles for the clusters.
予測精度を向上させるために彼らが提案した解決策は、ロングテール項目をクラスタリングし、そのクラスタに対して共同の評価プロファイルを作成することに基づいている。
Then, for a given long-tail item, rating prediction could be made using all ratings in its cluster.
そして、与えられたロングテール項目について、そのクラスター内のすべての評価を用いて評価予測を行うことができる。
Experiments with the MovieLens dataset showed reduced error rates using the proposed approach.
MovieLensデータセットを用いた実験では、提案アプローチを用いることでエラー率が減少した。
However, the proposed technique did not guarantee promotion of the long-tail items into users’ top-N recommendation lists.
しかし、提案された技術では、ロングテール項目がユーザーのトップN推薦リストに入ることは保証されなかった。
Ishikawa et al.[2008] addressed the long-tail phenomenon in the context of recommending knowledge resources (web pages) in an information portal.
石川ら[2008]は、情報ポータルにおける知識資源（ウェブページ）の推薦という文脈で、ロングテール現象を取り上げた。
They proposed an approach based on innovation diffusion theory, claiming that new information spreads among users according to observable patterns, with the first users to access a resource playing the role of “innovators.” The proposed algorithm therefore requires a “seed” long-tail item and exploits the users who first “discovered” it as a source of novel recommendations (by recommending other items that were accessed by these users).
彼らはイノベーション拡散理論に基づくアプローチを提案し、新しい情報は観察可能なパターンに従ってユーザー間に拡散し、リソースに最初にアクセスしたユーザーが "イノベーター "の役割を果たすと主張した。したがって、提案されたアルゴリズムでは、"種 "となるロングテールアイテムを必要とし、それを最初に "発見 "したユーザーを（そのユーザーがアクセスした他のアイテムを推薦することによって）新規推薦のソースとして利用する。
Experiments with the portal’s log data showed 10 to be the optimal number of “innovators.” Since the approach was designed within a very specific domain, it would be interesting to evaluate it in more common recommendation domains, such as movies or music.
ポータルのログデータを使った実験では、"イノベーター "の最適な数は10人であった。このアプローチは非常に特殊な領域で設計されているため、映画や音楽など、より一般的な推薦領域で評価することは興味深い。
Zhou et al.[2010] exploited item popularity information to increase both novelty (measured as the self-information of recommended items, see Equation (4)) and interuser diversity (average pairwise distance between recommendation lists generated for different users).
Zhouら[2010]は、アイテムの人気度情報を利用して、新規性（推奨アイテムの自己情報として測定、式(4)参照）とユーザー間の多様性（異なるユーザーのために生成された推奨リスト間の平均ペア間距離）の両方を高めている。
The authors proposed an algorithm based on weight spreading in a bipartite user-item graph.
著者らは、2部構成のユーザー項目グラフにおける重み拡散に基づくアルゴリズムを提案した。
The algorithm works by assigning weights to items rated by the target user and then equally distributing the weight of each item to other users who rated it.
このアルゴリズムは、ターゲットユーザーが評価したアイテムに重みを割り当て、各アイテムの重みを評価した他のユーザーに均等に配分することで機能する。
The weight of each user is then distributed among his or her rated items.
そして、各ユーザーのウェイトが、彼の評価項目に分配される。
This weight spreading procedure favors item nodes with few graph links (i.e., rare items), resulting in novel recommendations.
このウェイト拡散手順は、グラフリンクの少ないアイテムノード（つまり、レアアイテム）を優先し、その結果、斬新なレコメンデーションが得られる。
In similar research, Liu et al.[2012] described a graph-based algorithm with weight spreading and showed that assigning more weight to users with small profiles enhances both interuser diversity and the novelty of recommendations.
同様の研究において、Liuら[2012]は、重み拡散を用いたグラフベースのアルゴリズムについて述べ、プロフィールが小さいユーザーにより多くの重みを割り当てることで、ユーザー間の多様性と推薦の新規性の両方が向上することを示した。

Oh et al.[2011] followed the idea that novelty is related to both popularity and the interuser diversity of recommendations.
Ohら[2011]は、新規性が推奨の人気とユーザー間の多様性の両方に関連するという考えに従った。
They worked with the MovieLens dataset and measured item popularity using movie box office earnings (applying a log scale to smooth the effects of the power-law distribution).
彼らはMovieLensデータセットを使用し、映画の興行収入を使ってアイテムの人気を測定した（べき乗分布の影響を平滑化するために対数スケールを適用）。
The work demonstrated that a state-of-the-art method for item-based collaborative filtering and a novelty-optimized recommender (the Tangent system [Onuma et al.2009], which we discussed in the context of serendipity, see Section 3) both perform poorly in terms of popularity and interuser diversity; that is, their generated recommendations are clustered around popular items.
この研究は、アイテムベースの協調フィルタリングのための最先端の手法と、新規性に最適化されたレコメンダー（セレンディピティの文脈で議論したTangentシステム[Onuma et al.2009]。
Oh et al.argued that the users’ preferences for popular items should partly determine the recommendations.
Ohらは、人気のあるアイテムに対するユーザーの嗜好が、レコメンデーションを部分的に決定するべきだと主張した。
From the users’ rating histories, they identified different types of “personal popularity tendency,” that is, different levels of user interest in rare/popular items.
ユーザーの評価履歴から、さまざまなタイプの「個人的な人気傾向」、つまりレアアイテムや人気アイテムに対するユーザーの関心度の違いを特定した。
Their proposed novelty optimization approach reranks recommendations by penalizing items that do not fit the user’s popularity tendency.
彼らの提案する新規性最適化アプローチは、ユーザーの人気傾向に合わないアイテムにペナルティを課すことで、レコメンデーションのランクを変更する。
Another graph-based approach was proposed by Shi [2013], who defined a cost flow model for a bipartite user-item graph.
別のグラフベースのアプローチは、Shi [2013]によって提案されたものであり、彼は二部ユーザアイテムグラフのコストフローモデルを定義した。
The model is based on assigning a transition cost for each edge between a user node and an item node.
このモデルは、ユーザーノードとアイテムノード間の各エッジに遷移コストを割り当てることに基づいている。
Given a target user and candidate items, the cost to reach the target user node from a candidate item node can be computed by propagating the cost score through the edges.
ターゲット・ユーザーと候補アイテムが与えられた場合、候補アイテム・ノードからターゲット・ユーザー・ノードに到達するためのコストは、エッジを通してコスト・スコアを伝播することによって計算することができる。
Items that obtain the lowest-cost scores are then recommended to the user.
そして、最も低コストのスコアを得たアイテムがユーザーに推奨される。
Shi proposed different strategies for defining the edge transition costs, including the “long tail” strategy that sets the costs to be proportional to the popularity of item nodes they connect, thus promoting rare items.
Shiは、エッジ遷移コストを定義するためのさまざまな戦略を提案した。その中には、コストを接続するアイテムノードの人気に比例するように設定し、レアアイテムを促進する「ロングテール」戦略も含まれる。
We observe that works addressing the long-tail recommendation problem often measure algorithm performance not only in terms of novelty but also in terms of interuser diversity [Zhou et al.2010; Liu et al.2012] and coverage [Shi 2013].
ロングテール推薦問題に取り組んでいる研究では、アルゴリズムの性能を新規性だけでなく、ユーザー間の多様性[Zhou et al.2010; Liu et al.2012]やカバレッジ[Shi 2013]の観点から測定することが多い。
This indicates that novelty is closely related to these system-level objectives.
このことは、新規性がこれらのシステムレベルの目標と密接に関係していることを示している。
Interuser diversity measures the difference between recommendations across different users, while coverage measures how well the recommender covers the available item catalog.
ユーザー間の多様性は、異なるユーザー間のレコメンデーションの違いを測定し、カバレッジは、レコメンダーが利用可能なアイテムカタログをどれだけカバーしているかを測定する。
In this article, we do not discuss the interuser diversity but focus on the more popular system-level objective—coverage.
この記事では、ユーザー間の多様性については議論せず、より一般的なシステムレベルの目的-カバレッジに焦点を当てる。

# Coverage カバレッジ

Unlike the beyond-accuracy objectives that we have discussed so far, coverage is not defined at the level of an individual user, but rather at the level of the system.
これまで議論してきた精度を超える目標とは異なり、カバレッジは個々のユーザーのレベルではなく、システムのレベルで定義される。
There are two general approaches to measuring recommendation coverage—“user coverage,” which measures the degree to which the system covers its users (e.g., the ratio of users for which a recommender is able to deliver recommendations [Bellog´ın et al.2013]), and “item coverage,” which measures the degree to which recommendations cover the set of available items (i.e., the item catalog).
レコメンデーションのカバレッジを測定する2つの一般的なアプローチがある-システムがユーザーをカバーする度合いを測定する「ユーザーカバレッジ」（例えば、レコメンダーがレコメンデーションを提供できるユーザーの比率[Bellog´ın et al.2013]）と、レコメンデーションが利用可能なアイテムのセット（すなわち、アイテムカタログ）をカバーする度合いを測定する「アイテムカバレッジ」である。
Since the latter formulation is more commonly found in the RS literature [Herlocker et al.2004; Ge et al.2010; Adomavicius and Kwon 2012] and to be consistent with the other discussed beyondaccuracy objectives (which are item properties rather than user properties), in this work we focus on “item coverage” and henceforth refer to it simply by the term coverage.
後者の定式化は、RSの文献[Herlocker et al.2004; Ge et al.2010; Adomavicius and Kwon 2012]ではより一般的であり、また、精度を超えた他の議論された目的（ユーザーの特性ではなく項目の特性である）との一貫性を保つため、本研究では「項目のカバレッジ」に焦点を当て、以後、単にカバレッジという用語で呼ぶ。
Since measures of coverage show how well the system’s recommendations cover the catalog of available items, higher coverage means exposing the users to a wider range of recommended items, which may both increase the users’ satisfaction with the system (e.g., by recommending items the user would not otherwise discover) [Adomavicius and Kwon 2012] and benefit business owners (increasing the sales of the long-tail items).
カバレッジの測定は、システムの推奨が利用可能なアイテムのカタログをどの程度カバーしているかを示すので、カバレッジが高いということは、推奨されるアイテムの広い範囲にユーザーをさらすことを意味する。
For instance, Anderson [2006] argued that aggregate sales of the long-tail products may match (or even outnumber) the sales of the top-selling products.
例えば、アンダーソン[2006]は、ロングテール商品の総売上高は、トップセラー商品の売上高に匹敵する（あるいは上回る）可能性があると論じている。

## Defining and Measuring Coverage カバレッジの定義と測定

As with other beyond-accuracy objectives, the terminology used to identify the coverage objective varies across different works.
他の精度を超える目標と同様に、カバレッジ目標を特定するために使用される用語は、作品によって異なる。
Coverage has been referred to as “aggregate diversity” [Adomavicius and Kwon 2011, 2012], “sales diversity” [Vargas and Castells 2014], or simply “diversity” [Shi 2013].
カバレッジは、「集約的多様性」［Adomavicius and Kwon 2011, 2012］、「販売多様性」［Vargas and Castells 2014］、あるいは単に「多様性」［Shi 2013］と呼ばれている。
To avoid confusion with the diversity objective, which is applicable to a single user’s list of recommendations (see Section 2), we use the term coverage and adopt its most widespread definition—the fraction of items that appear in the users’ recommendation lists:
一人のユーザーの推薦リストに適用される多様性目標（セクション2参照）との混同を避けるため、カバレッジという用語を使用し、その最も一般的な定義（ユーザーの推薦リストに表示されるアイテムの割合）を採用する：

$$
\tag{5}
$$

where Ru is the set of all recommendations generated for user u, U is the set of all users of the system, and I is the item catalog.
ここで、Ruはユーザーuに対して生成されたすべての推奨の集合、Uはシステムのすべてのユーザーの集合、Iはアイテムカタログである。
Herlocker et al.[2004] distinguished between two forms of item coverage— “prediction coverage,” which captures the ratio of items for which predictions can be made by the recommendation algorithm, and “catalog coverage,” which captures the ratio of items that effectively appear in the recommendation lists presented to users of the system.
Herlockerら[2004]は、「予測カバレッジ」と「カタログカバレッジ」という2種類のアイテムカバレッジを区別している。
The metric adopted in our work (Equation (5)) corresponds to catalog coverage and we do not discuss prediction coverage separately.
我々の研究で採用した指標（式(5)）はカタログカバレッジに対応するものであり、予測カバレッジについては別に論じない。
A few works have suggested taking recommendation relevance into account when measuring coverage, that is, measuring the fraction of relevant items that are recommended to all users [Herlocker et al.2004; Bellog´ın et al.2013].
いくつかの研究では、カバレッジを測定する際に推薦の関連性を考慮することを提案している。つまり、すべてのユーザーに推薦される関連アイテムの割合を測定することである[Herlocker et al.2004; Bellog´ın et al.2013]。
Such definitions require that we know all the potentially relevant items for each user.
このような定義では、各ユーザーに関連する可能性のある項目をすべて知っている必要がある。
Ge et al.[2010] proposed a more general definition where each item contributing to the coverage score is weighted by its usefulness.
Geら[2010]は、カバレッジスコアに寄与する各項目をその有用性によって重み付けする、より一般的な定義を提案している。
The authors suggested that the usefulness weights may be computed using item relevance, novelty, or serendipity scores.
著者らは、項目の関連性、新規性、セレンディピティのスコアを用いて有用性の重みを計算することを提案した。
All the variants of the coverage metric discussed previously share a common feature—since all recommended items are aggregated into a single score, an item recommended once contributes to the coverage score the same amount as an item recommended a thousand times.
すべての推奨アイテムは1つのスコアに集約されるため、1回推奨されたアイテムは1000回推奨されたアイテムと同じだけカバレッジスコアに貢献する。
An alternative definition, which overcomes this limitation, was proposed by Fleder and Hosanagar [2009].
この制限を克服する別の定義が、FlederとHosanagar [2009]によって提案された。
They used the Gini coefficient, ranging in [0, 1], to measure the distribution of recommendations across all users.
ジニ係数は[0, 1]の範囲で、全ユーザーのレコメンデーションの分布を測定するために使用される。
High values of the coefficient mean that recommendations are concentrated around a few frequently recommended items (i.e., there is a high concentration bias [Jannach et al.2015b]), while lower values signify a more uniform distribution of recommendations.
係数の値が高いということは、推薦が少数の頻繁に推薦される項目の周りに集中している（すなわち、高い集中バイアス[Jannach et al.2015b]がある）ことを意味し、値が低いということは、推薦の分布がより均一であることを意味する。
Vargas and Castells [2014] adopted the complement of the Gini coefficient so that higher values of the metric correspond to better (more uniform) catalog coverage.
VargasとCastells [2014]は、ジニ係数の補数を採用し、指標の値が高いほど、より良い（より均一な）カタログカバレッジに対応するようにしている。
Shani and Gunawardana [2011] identified Shannon entropy as another option for measuring the distribution of recommendations across users.
ShaniとGunawardana [2011]は、ユーザー間の推薦の分布を測定するための別のオプションとして、シャノンエントロピーを同定した。
For an item catalog of size n, the Shannon entropy metric ranges between 0 (when the same single item is always recommended) and log n (when all items are recommended equally often).
サイズnのアイテムカタログの場合、シャノンエントロピーの指標は、0（同じ1つのアイテムが常に推奨される場合）からlog n（すべてのアイテムが同じ頻度で推奨される場合）の範囲である。
Despite being a system-level objective, coverage is related to other objectives discussed in this article, particularly to novelty.
システムレベルの目的であるにもかかわらず、カバレッジは本稿で論じた他の目的、特に新規性と関連している。
As discussed in Section 4, novelty is typically measured as the complement of item popularity.
セクション4で述べたように、新規性は一般的にアイテムの人気の補完として測定される。
Highly novel recommendations are therefore those belonging to the long tail of the item popularity distribution.
したがって、新規性の高いレコメンデーションとは、アイテム人気分布のロングテールに属するものである。
Intuitively, a high coverage of the item catalog requires recommending the long-tail items to users, which corresponds to a high average novelty (see Equation (4)).
直感的に言えば、アイテムカタログのカバー率が高ければ、ロングテールのアイテムをユーザーに推薦する必要があり、これは平均新規性が高いことに対応する（式（4）参照）。
However, the relation between coverage and novelty is not always straightforward, as has been shown by Jannach et al.[2013].
しかし、Jannachら[2013]が示したように、カバー率と新規性の関係は必ずしも単純ではない。
The authors compared a number of state-of-the-art recommendation algorithms in terms of coverage and the tendency to focus on popular items.
著者らは、カバレッジと人気アイテムにフォーカスする傾向の観点から、多くの最新レコメンデーション・アルゴリズムを比較した。
In experiments performed on the MovieLens dataset, a learning-to-rank algorithm achieved a high level of coverage but also suffered from popularity bias (i.e., having higher average popularity of recommended items compared to other algorithms).
MovieLensデータセットで行われた実験では、学習ランク付けアルゴリズムは高いカバレッジレベルを達成したが、人気バイアス（他のアルゴリズムに比べて推奨アイテムの平均人気が高いこと）にも悩まされた。
Coverage has also been discussed in relation to diversity.
カバレージは多様性との関連でも議論されている。
Adomavicius and Kwon [2012] discussed the difference between diversity (which they call “individual diversity,” i.e., the diversity of a recommendation list presented to a single user) and coverage (which they call “aggregate diversity,” i.e., the range of items recommended across all system users).
Adomavicius and Kwon [2012]は、多様性（彼らは「個別多様性」と呼び、一人のユーザーに提示される推薦リストの多様性を指す）とカバレッジ（彼らは「集約多様性」と呼び、全システムユーザーにわたって推薦されるアイテムの範囲を指す）の違いについて議論した。
They argued that high diversity does not imply high coverage.
彼らは、高い多様性は高いカバー率を意味しないと主張した。
For instance, if different users are recommended the same diverse set of items, the average diversity of the system will be high, but the coverage will remain low.
例えば、異なるユーザーが同じ多様なアイテムのセットを推奨する場合、システムの平均多様性は高くなるが、カバレッジは低いままである。
Similarly, Fleder and Hosanagar [2009] discussed a scenario where (during the evolution of an e-commerce recommender) the system helps users discover new items, but the Gini coefficient increases (i.e., the coverage deteriorates).
同様に、FlederとHosanagar [2009]は、（電子商取引のレコメンダーの進化の過程で）システムがユーザーの新しいアイテムの発見を助けるが、ジニ係数が増加する（すなわち、カバレッジが悪化する）シナリオについて議論した。
This happens if the users are exposed to new items, but these are the same items other users have seen before.
これは、ユーザーが新しいアイテムに触れても、それが他のユーザーが以前見たものと同じである場合に起こる。
Ge et al.[2010] briefly discussed the relation between coverage and serendipity.
Geら[2010]は、カバレッジとセレンディピティの関係について簡潔に論じている。
They argued that high serendipity implies high coverage, but an increase in coverage will not necessarily improve serendipity.
彼らは、セレンディピティの高さはカバー率の高さを意味するが、カバー率を上げてもセレンディピティが向上するとは限らないと主張した。
The authors, however, offered no experiments to support this hypothesis.
しかし、著者たちはこの仮説を支持する実験結果を提示していない。
In summary, the close relation between coverage and other beyond-accuracy objectives has been recognized in the literature.
要約すると、カバレッジとその他の精度を超えた目標との間には密接な関係があることが文献で認識されている。
However, there is a lack of experiments that study the relationships between the different metrics.
しかし、異なる測定基準間の関係を研究する実験が不足している。
We contribute to the analysis of this research problem with experiments presented in Section 7.
我々は、セクション7で紹介する実験によって、この研究課題の分析に貢献する。

## Increasing Coverage カバレッジの拡大

As discussed earlier, coverage can be linked to the novelty of recommendations.
前述したように、カバー率は推薦の新規性と連動することがある。
This is reflected in work that addresses the coverage optimization problem, with most approaches relying on reducing the popularity bias of recommendations (i.e., increasing the number of long-tail items recommended to users).
これは、カバレッジ最適化問題に取り組む研究に反映されており、ほとんどのアプローチは、推奨の人気バイアスを減らすこと（すなわち、ユーザーに推奨されるロングテールのアイテムの数を増やすこと）に依存している。
Consequently, the approaches discussed in this section overlap with those described in Section 4.2.To avoid repetition, here we discuss works that explicitly target increasing the coverage of recommendations.
その結果、このセクションで議論されるアプローチは、セクション4.2で説明されたものと重複している。繰り返しを避けるため、ここでは、推薦のカバレッジを高めることを明確にターゲットとした作品について議論する。
Adomavicius and Kwon [2011] modeled the item-to-user recommendations (precomputed using a standard recommendation algorithm) as a graph, where an edge connects an item to a user only if the item is predicted as relevant to that user (a prediction threshold may be used when constructing the graph).
Adomavicius and Kwon [2011]は、アイテムからユーザーへのレコメンデーション（標準的なレコメンデーションアルゴリズムを使用して事前計算）をグラフとしてモデル化し、エッジは、アイテムがそのユーザーに関連すると予測される場合にのみ、アイテムとユーザーを接続する（グラフを構築する際に予測しきい値を使用することができる）。
They then solve the maximum flow problem on the constructed graph; that is, they find the maximum number of edges that connect users and items, such that each user is connected to no more than N items.
つまり、各ユーザーがN個以下のアイテムと接続されるように、ユーザーとアイテムを接続する辺の最大数を求める。
The solution of this problem results in each user being assigned up to N recommendations with the maximum coverage of the available items.
この問題を解決すると、各ユーザーは、利用可能なアイテムの最大カバレッジを持つ最大N個の推奨を割り当てられることになる。
Another work by Adomavicius and Kwon [2012] described a coverage optimization approach based on reranking the recommendation list to promote the long-tail items.
Adomavicius and Kwon [2012]による別の研究では、ロングテールのアイテムを促進するために推薦リストを再ランク付けすることに基づいたカバレッジ最適化アプローチについて述べている。
The approach reranks items whose predicted rating is above a certain threshold by their popularity (ranking rare items higher).
このアプローチは、予測された評価がある閾値を超えたアイテムを、その人気度によって再ランク付けする（レアなアイテムを上位にランク付けする）。
The threshold parameter guarantees a certain level of accuracy in the list and can be varied for a tradeoff between accuracy and coverage.
閾値パラメータは、リストの精度を一定レベル保証するもので、精度とカバレッジのトレードオフのために変化させることができる。
Offline evaluation with the MovieLens dataset showed the approach to improve coverage with a minimal loss in recommendation accuracy.
MovieLensデータセットを用いたオフライン評価では、推薦精度の損失を最小限に抑えつつ、カバレッジを向上させるアプローチが示された。
Vargas and Castells [2014] proposed an approach to increase coverage by reducing the popularity bias in nearest-neighbor CF algorithms.
VargasとCastells[2014]は、最近傍CFアルゴリズムにおける人気度バイアスを低減することで、カバレッジを向上させるアプローチを提案した。
They suggested inverting the neighbor selection process in user-based or item-based CF: for instance, in the case of item-based nearest-neighbor CF, instead of selecting the top-k most similar neighbors for an item, they suggested constructing the neighborhood by selecting those items in whose neighborhoods the target item appears.
例えば、項目ベースの最近傍CFの場合、ある項目の上位k個の最も類似した近傍項目を選択する代わりに、対象項目が出現する近傍項目を選択して近傍を構築することを提案した。
(A similar inversion can be used for user-based neighborhood techniques.) The authors demonstrated that such inversion results in a reduced popularity bias, since all items appear in the same number of the newly defined neighborhoods and therefore rating prediction is less influenced by the popular items.
(同様の反転は、ユーザーベースの近傍技術にも使用できる。) 著者らは、このような反転は、すべてのアイテムが新しく定義された近傍の同じ数に表示されるため、評価予測が人気アイテムの影響を受けにくくなり、人気バイアスが減少することを実証した。
Offline experiments with Netflix data and the Million Song Dataset showed that the inverted item-based CF approach outperformed the standard itembased technique in both accuracy and coverage (measured as the complement of Gini coefficient).
NetflixデータとMillion Song Datasetを用いたオフライン実験では、逆項目ベースのCF手法が、精度とカバー率（ジニ係数の補数として測定）の両方で標準的な項目ベースの手法を上回ることが示された。
The inverted user-based approach showed better coverage results but did not outperform the standard user-based technique in terms of accuracy.
逆ユーザーベースの手法は、より良いカバレッジ結果を示したが、精度の点では標準的なユーザーベースの手法を上回らなかった。

# Measuring the User's Perception of beryond-accuracy objectives 

Any evaluation of recommendation diversity, serendipity, or novelty not involving user feedback is limited in terms of the reliability of the findings.
ユーザーからのフィードバックを伴わない推薦の多様性、セレンディピティ、新規性の評価は、調査結果の信頼性という点で限界がある。
For instance, without asking the end-user of the system, it is not evident that an item that was shown to be serendipitous by some metric will be perceived as such by the user.
例えば、システムのエンドユーザーに尋ねなければ、何らかの指標でセレンディピティであると示された項目が、ユーザーによってそのように認識されるかどうかはわからない。
Likewise, it is not evident that a diversification algorithm that considers pairwise dissimilarity of recommended items will produce recommendation lists that users perceive as diverse.
同様に、推奨アイテムのペアごとの非類似度を考慮する多様化アルゴリズムが、ユーザーが多様であると認識する推奨リストを生成することは明らかではない。
However, despite the obvious need for user feedback on the beyond-accuracy qualities of recommendations, few research works in this area include user studies, the majority of results being obtained from offline experiments.
しかし、レコメンデーションの精度を超えた品質に関するユーザーからのフィードバックが必要であることは明らかであるにもかかわらず、この分野ではユーザー研究を含む研究成果はほとんどなく、オフラインの実験から得られた結果が大半を占めている。
This can be explained by the many challenges in designing and conducting such studies: recruiting a sufficiently large number of participants, correctly formulating survey questions, avoiding judgment biases, and so forth.
これは、このような研究を計画・実施する際の多くの課題、すなわち、十分な数の参加者を集めること、調査質問を正しく作成すること、判断バイアスを避けること、などによって説明することができる。
Moreover, when recommending items that take a long time to consume (e.g., movies), relevance, diversity, or serendipity judgments are difficult to obtain for items that are unknown to users.
さらに、消費に時間のかかるアイテム（映画など）を推薦する場合、ユーザーにとって未知のアイテムでは、関連性、多様性、セレンディピティの判断が難しい。
In this section, we provide an overview of the limited number of works that do rely on user studies when analyzing beyond-accuracy objectives.
このセクションでは、精度を超えた目標を分析する際に、ユーザー調査に依存している限られた数の研究の概要を説明する。
We split such works into two general categories: (1) research studies where beyond-accuracy objectives are evaluated as a part of larger multicriteria experiments that measure relationships between the different recommendation qualities perceived by users (e.g., the impact of perceived novelty on diversity perception) [Pu et al.2011; Knijnenburg et al.2012; Ekstrand et al.2014], and (2) works that analyze the impact of the proposed algorithms (or user interface modifications) on specific beyond-accuracy objectives [Ziegler et al.2005; Ge et al.2012; Hu and Pu 2011].
(1)精度を超える目標が、ユーザーによって知覚される様々な推薦品質間の関係を測定する、より大規模な多基準実験の一部として評価される研究[Pu et al.2011; Knijnenburg et al.2012; Ekstrand et al.2014]、 (2)提案されたアルゴリズム(またはユーザインタフェースの修正)が特定の精度を超える目標に与える影響を分析する研究[Ziegler et al.2005; Ge et al.2012; Hu and Pu 2011]。
Of the beyond-accuracy objectives discussed in our work, diversity and novelty are the ones that are most frequently investigated in user studies.
我々の研究で議論されている精度を超えた目標のうち、多様性と新規性はユーザー研究で最も頻繁に調査されているものである。
Serendipity has been reported to be difficult to explain to users [Said et al.2013] or has been left out of the studies as being too similar to novelty [Pu et al.2011].
セレンディピティは、ユーザーに説明するのが難しいと報告されたり[Said et al.2013]、新規性と類似しすぎているとして研究対象から外されたりしている[Pu et al.2011]。
Coverage is not measured in user studies since it is not directly related to individual user experiences.
カバレッジは、個々のユーザーの経験とは直接関係がないため、ユーザー調査では測定されない。
Besides the perceived accuracy, diversity, and novelty, user studies often also measure user satisfaction with the system.
知覚される正確さ、多様性、新規性に加えて、ユーザー調査はしばしばシステムに対するユーザーの満足度も測定する。
Although satisfaction is a concept easily understood by users, we consider it as a higher-level quality that can be influenced by many perceived qualities (relevance, diversity, novelty, serendipity) and therefore do not analyze it in this article.
満足度はユーザーにとって理解しやすい概念であるが、私たちはそれを多くの知覚品質（関連性、多様性、新規性、セレンディピティ）に影響されうる高次の品質と考え、本稿では分析しない。

## Beyond-Accuracy Objectives in Multicriteria User Studies 多基準ユーザー研究における超越精度目標

Pu et al.[2011] conducted a user study to determine a set of recommendation quality criteria that accurately reflect the users’ perception of a recommender system’s usefulness.
Puら[2011]は、推薦システムの有用性に対するユーザの認識を正確に反映する推薦品質基準のセットを決定するためのユーザ研究を行った。
Of the beyond-accuracy objectives, diversity and novelty were included.
精度を超えた目標のうち、多様性と新規性が含まれた。
Serendipity was discarded as it was considered too similar to novelty.
セレンディピティはノベルティに似すぎていると判断され、破棄された。
The users were asked to find an information item using a recommender system of their choice and to answer a set of questions regarding the perceived qualities of the service.
ユーザーは、自分の選んだレコメンダー・システムを使って情報アイテムを見つけ、そのサービスの知覚品質に関する一連の質問に答えるよう求められた。
Having analyzed the correlations between answers, the authors validated a model consisting of 32 criteria grouped into 15 categories.
著者らは回答間の相関関係を分析し、15のカテゴリーに分類された32の基準からなるモデルを検証した。
The results of the study showed the perceived usefulness of a recommender to be influenced by the perceived accuracy and novelty, and to a lesser extent by the perceived diversity.
研究の結果、レコメンダーの知覚される有用性は、知覚される正確さと新規性に影響され、知覚される多様性にはそれほど影響されないことが示された。
Knijnenburg et al.[2012] proposed a framework for evaluating users’ experience of recommender systems, including the perceived accuracy, satisfaction, choice difficulty, and diversity.
Knijnenburgら[2012]は、ユーザのレコメンダーシステムに対する経験を評価するためのフレームワークを提案した。
The framework consists of a set of structurally related concepts including objective system aspects (e.g., the recommendation algorithm) and user characteristics (e.g., the user’s age) that are connected to subjective user experiences (e.g., the perceived diversity).
このフレームワークは、主観的なユーザー体験（知覚される多様性など）に関連する、客観的なシステム側面（推薦アルゴリズムなど）とユーザー特性（ユーザーの年齢など）を含む、構造的に関連する一連の概念で構成されている。
The authors proposed a set of questions to record the subjective user experiences and conducted a series of experiments to investigate the relationships between framework components.
著者らは、主観的なユーザー体験を記録するための一連の質問を提案し、フレームワークの構成要素間の関係を調べるために一連の実験を行った。
The results showed that diversification (implemented using the greedy reranking approach, see Algorithm 1) is perceived differently for different algorithms.
その結果、多様化（貪欲な再ランク付けアプローチで実施、アルゴリズム1を参照）はアルゴリズムによって受け止め方が異なることがわかった。
For example, the users perceived recommendations of the k-NN algorithm with no diversification as more diverse than diversified recommendations of the same algorithm, while this was not observed for the factorization algorithm.
例えば、多様化されていないk-NNアルゴリズムの推奨は、同じアルゴリズムの多様化された推奨よりも多様であるとユーザーは認識したが、因数分解アルゴリズムではこのような傾向は見られなかった。
When the users did perceive recommendations as diverse, this had a positive relationship with the perceived accuracy, the ease of choice, and consequently the overall satisfaction with the system.
利用者がレコメンデーションを多様であると認識した場合、これは認識された正確さ、選択のしやすさ、ひいてはシステムに対する全体的な満足度と正の関係を示した。
Ekstrand et al.[2014] adapted the questions used by Knijnenburg et al.[2012] for a comparative study where users of the MovieLens recommender system were asked to compare pairs of movie recommendation lists and answer questions regarding the perceived accuracy, diversity, and novelty of the recommendation lists and their overall satisfaction.
Ekstrandら[2014]は、Knijnenburgら[2012]によって使用された質問を、MovieLensレコメンダーシステムのユーザーが映画の推薦リストのペアを比較し、推薦リストの知覚精度、多様性、新規性、および全体的な満足度に関する質問に答えるように求められた比較研究のために適応させた。
Three state-of-the-art algorithms were used for generating recommendations: an SVD factor model and both a user-user and an item-item collaborative filtering approach.
レコメンデーション生成には、SVD因子モデル、ユーザー-ユーザー協調フィルタリング、アイテム-アイテム協調フィルタリングの3つの最新アルゴリズムが用いられた。
To address the possible item familiarity effects, the authors limited the set of recommendable items to popular ones, thus avoiding recommendation lists with too many obscure items.
アイテムの馴染み効果に対処するため、著者らは推薦可能なアイテムのセットを人気のあるものに限定し、無名のアイテムが多すぎる推薦リストを避けた。
The study results revealed that the users were equally satisfied with the SVD and item-item algorithms, while being less satisfied with the user-user algorithm.
研究の結果、ユーザーはSVDアルゴリズムとアイテム-アイテムアルゴリズムに同じように満足したが、ユーザー-ユーザーアルゴリズムには満足しなかった。
The perceived satisfaction with the recommendations was found to positively correlate with the perceived diversity and negatively with perceived novelty.
レコメンデーションに対する満足度は、多様性の認知とは正の相関があり、新規性の認知とは負の相関があることがわかった。
The observed negative influence of novelty on users’ satisfaction seems to contradict the findings of Pu et al.[2011], who found novelty to positively influence the perceived system usefulness (and consequently users’ satisfaction).
ユーザーの満足度に対する新規性の悪影響が観察されたことは、システムの有用性の認知（ひいてはユーザーの満足度）に新規性が正の影響を与えることを発見したPuら[2011]の知見と矛盾するように思われる。
The findings may differ due to different recommendation domains (Pu et al.conducted the survey using a number of online recommender services including Amazon, while Ekstrand et al.focused on movie recommendations).
推薦の領域が異なるため、調査結果は異なる可能性がある（Puらはアマゾンを含む多くのオンライン推薦サービスを用いて調査を実施し、Ekstrandらは映画に焦点を当てた）。
Another possible explanation lies in the different formulations of the novelty-related questions the users had to answer during the two studies.
もう1つの可能性は、2つの研究でユーザーが答えなければならなかった新規性に関連する質問の形式の違いにある。
Pu et al.analyzed the perceived novelty by measuring the users’ agreement with the statement “The recommender system helped me discover new products,” while Ekstrand et al.compared the perceived novelty of two movie lists with such questions as “Which list has more movies you do not expect?” and “Which list has more movies you would not have thought to consider?” Therefore, in the first case, novelty feedback was gathered by means of a positive question, while in the second case, the negative tone of the survey questions may have tied negative user experiences to the measured objective, that is, novelty.
Puらは "The recommender system helped me discover new products"（レコメンダーシステムは新しい製品を発見するのに役立った）というステートメントに対するユーザーの同意を測定することで知覚された新規性を分析し、Ekstrandらは "どちらのリストに予想外の映画が多いか？"と "どちらのリストに検討しようと思わなかった映画が多いか？"というような質問で2つの映画リストの知覚された新規性を比較した。したがって、最初のケースでは、新規性のフィードバックは、肯定的な質問によって収集されましたが、2番目のケースでは、アンケートの質問の否定的なトーンは、測定された目的、すなわち新規性に否定的なユーザーの経験を結びつけた可能性があります。
This example shows the impact that the formulation of survey questions may have on the outcome of studies measuring users’ perception of multiple recommendation qualities.
この例は、ユーザーの複数の推奨品質に対する認識を測定する研究の結果に、調査質問の定式化が影響を与える可能性があることを示している。

## Beyond-Accuracy Objectives in Targeted User Studies ターゲットユーザー調査におけるビヨンド・アキュラシー目標

Targeted user studies are conducted to validate the usefulness of a certain technique, for example, a diversity-oriented algorithm, or a modification of the user interface optimized for diversity perception.
例えば、多様性志向のアルゴリズムや、多様性を認識するために最適化されたユーザー・インターフェースの修正など、特定の手法の有用性を検証するために、ターゲットを絞ったユーザー・スタディが実施される。
Ziegler et al.[2005] evaluated their greedy diversification technique on a BookCrossing dataset.3 Given a list of book recommendations, each user was asked to evaluate the relevance of each recommendation, the diversity of the list of recommendations, and their overall satisfaction with the recommendations.
Zieglerら[2005]は、BookCrossingデータセットを用いて、彼らの貪欲な多様化技法を評価した。3 書籍の推薦リストが与えられたとき、各ユーザーは、各推薦の関連性、推薦リストの多様性、推薦に対する総合的な満足度を評価するよう求められた。
The users were randomly assigned either a user-based or item-based CF recommender, and the diversification algorithm was based on comparing the genres of items (using a genre taxonomy-based metric).
ユーザーは、ユーザーベースまたはアイテムベースのCFレコメンダーのいずれかをランダムに割り当てられ、多様化アルゴリズムは、アイテムのジャンルを比較することに基づいていた（ジャンル分類学ベースのメトリックを使用）。
The results of the study showed that light diversification (changing up to four items in a list of 10 recommendations) positively influences user satisfaction with the item-based CF recommender.
研究の結果、軽い多様化（10個のレコメンドリストから最大4個のアイテムを変更）は、アイテムベースのCFレコメンダーに対するユーザーの満足度にプラスの影響を与えることが示された。
In the case of the user-based CF recommender, the results showed no measurable effect on satisfaction.
ユーザーベースのCFレコメンダーの場合、満足度に対する測定可能な効果は見られなかった。
Celma [2009] evaluated the users’ perception of item relevance and novelty in a music recommender.
Celma[2009]は、音楽レコメンダーにおけるアイテムの関連性と新規性に対するユーザーの認識を評価した。
The author conducted a study with 288 Last.fm users who were asked to rate their familiarity and appreciation of the songs recommended by three algorithms—an item-based collaborative approach, a content-based approach, and a hybrid combination of the two.
著者は、288人のLast.fmユーザーを対象に、3つのアルゴリズム（アイテムベースの協調アプローチ、コンテンツベースのアプローチ、そして2つのハイブリッドな組み合わせ）によって推薦された曲の親しみやすさと素晴らしさを評価してもらう研究を行った。
The results showed that the users perceived the recommendations of the content-based approach to be the most novel (i.e., they were least familiar with them), but also the least accurate (i.e., they assigned the lowest ratings to the tracks).
その結果、ユーザーは、コンテンツ・ベース・アプローチの推薦が最も目新しい（つまり、最も馴染みがない）と認識したが、同時に最も正確でない（つまり、楽曲に最も低い評価を付けた）と認識した。
Conversely, the collaborative approach was shown to produce the least novel but highest-rated recommendations.
逆に、コラボレーション・アプローチでは、新規性は低いものの、最も評価の高い推薦文が得られることが示された。
Celma hypothesizes that the low ratings of novel recommendations may be improved by providing explanations about why particular unknown songs are recommended.
セルマは、新規レコメンデーションの低評価は、特定の未知の曲がなぜレコメンデーションされるのかについての説明を提供することで改善されるかもしれないという仮説を立てている。
Hu and Pu [2011] analyzed how a standard list-based user interface compares to a more organized interface that groups recommendations into categories in terms of perceived diversity.
HuとPu [2011]は、標準的なリストベースのユーザーインターフェイスと、知覚される多様性の観点から推奨をカテゴリーにグループ化した、より組織化されたインターフェイスとの比較を分析した。
The authors conducted a within-subject user study with 20 participants in which each user viewed two versions of product recommendations (“customers who viewed this item also viewed”)—one version showed the standard list of products; the other version showed groups of products in separate tabs (organized by brand or price range).
1つのバージョンでは標準的な商品リストが表示され、もう1つのバージョンでは（ブランドや価格帯で整理された）別々のタブで商品グループが表示される。
The users provided feedback regarding the perceived categorical diversity (i.e., items being of different kinds) and item-to-item diversity (i.e., items being dissimilar to each other) as well as the perceived ease of use and usefulness of the system.
ユーザーは、知覚されたカテゴリー的多様性（すなわち、項目が異なる種類であること）および項目間の多様性（すなわち、項目が互いに類似していないこと）、ならびに知覚されたシステムの使いやすさと有用性に関するフィードバックを提供した。
While the results showed no significant difference in perceived item-to-item diversity, the perceived categorical diversity was shown to be larger in the second version of the interface, which also had a positive influence on the perceived ease of use and the usefulness of the system.
その結果、知覚される項目間の多様性に有意な差は見られなかったが、知覚されるカテゴリカルな多様性は、2番目のバージョンのインターフェースでより大きいことが示され、このことは、知覚される使いやすさとシステムの有用性にも良い影響を与えた。
Willemsen et al.[2011] described a user study where diversification was based on latent item features in a matrix factorization model.
Willemsenら[2011]は、多様化が行列因数分解モデルにおける潜在的項目特徴に基づくユーザー研究について述べている。
A within-subjects study with 97 participants required each user to evaluate three lists of movie recommendations representing different levels of diversification: low-level, midlevel, and high-level diversity.
97人の参加者を対象とした被験者内調査では、各ユーザーに、多様性のレベルが異なる3つの推奨映画リスト（低レベル、中間レベル、高レベルの多様性）を評価させた。
For each of the three conditions, the perceived recommendation diversity and attractiveness were measured.
3つの条件それぞれについて、知覚された推薦の多様性と魅力が測定された。
The results showed that lists with high levels of diversity were perceived as most diverse by the users.
その結果、多様性の高いリストが最も多様性があるとユーザーに認識された。
Interestingly, the perceived attractiveness of recommendations increased from low- to midlevel diversification, but did not further increase for the high level of diversification.
興味深いことに、レコメンデーションの魅力は、低水準の分散から中水準の分散へと増加したが、高水準の分散ではそれ以上増加しなかった。
This result suggests that after a certain level of diversity is achieved, users may not appreciate further diversification.
この結果は、あるレベルの多様性が達成された後、ユーザーはそれ以上の多様化を評価しない可能性があることを示唆している。
Ge et al.analyzed the impact that the placement of items within a recommendation list has on users’ perception of diversity.
Ge et al.は、推薦リスト内のアイテムの配置がユーザーの多様性の認識に与える影響を分析した。
The authors conducted a pilot user study with 10 participants [Ge et al.2011] and a later study with 52 participants [Ge et al.2012].
著者らは、10人の参加者によるパイロット・ユーザー・スタディ[Ge et al.2011]と、52人の参加者による後期スタディ[Ge et al.2012]を実施した。
The users were asked to evaluate the diversity of precomputed movie lists.
ユーザーには、事前に計算された映画リストの多様性を評価してもらった。
The same lists were displayed to all the users.
同じリストがすべてのユーザーに表示された。
Each list contained movies from one genre, with a small number of different genre items inserted for diversity.
各リストには1つのジャンルの映画が含まれ、多様性のために少数の異なるジャンルの項目が挿入されている。
The authors called the items whose genre was different from the list’s dominant genre “diverse items.” Three experimental conditions were compared: inserting all “diverse items” at the end of the list, inserting them in the middle of the list, and distributing them throughout the list.
著者らは、リストの支配的なジャンルとは異なるジャンルのアイテムを "多様なアイテム "と呼んだ。すべての「多様な項目」をリストの最後に挿入する、リストの真ん中に挿入する、リスト全体に分散させる、という3つの実験条件が比較された。
The later study showed that distributing “diverse items” throughout the list or placing them together at the bottom of the list led to higher perceived diversity and higher surprise than placing them close to each other in the middle of the list.
後の研究では、「多様な項目」をリスト全体に分散させたり、リストの一番下にまとめて配置したりすると、リストの真ん中に近くに配置するよりも、多様性の認知度が高くなり、驚きも高くなることが示された。
Moreover, having recognized the presence of “diverse items,” users in the pilot study were interested in additional information about such items (possibly trying to understand why they were recommended).
さらに、「多様なアイテム」の存在を認識したパイロット・スタディのユーザーは、そのようなアイテムに関する追加情報に興味を持った（おそらく、なぜそのアイテムが推奨されるのかを理解しようとした）。
This result indicates the potential use of explanations in diversityaware systems.
この結果は、多様性認識システムにおける説明の活用の可能性を示している。
The importance of explanations in recommendation diversification is also mentioned by Castagnos et al.[2013], who conducted a user study with a specially created movie dataset consisting of around 500 movies, 3,000 users, and 173,000 ratings.
レコメンデーションの多様化における説明の重要性については、Castagnosら[2013]も言及している。彼らは、約500の映画、3,000のユーザー、173,000の評価からなる特別に作成された映画データセットを用いてユーザー調査を行った。
The study involved 250 participants divided into five groups, with each group evaluating recommendations produced by one of the five algorithms—a baseline popularity approach, a content-based approach, an item-based collaborative filtering approach, and two collaborative filtering reranking techniques (variations of the greedy reranking technique, see Algorithm 1).
この研究では、250人の参加者を5つのグループに分け、各グループが5つのアルゴリズム（ベースライン人気度アプローチ、コンテンツベースアプローチ、アイテムベース協調フィルタリングアプローチ、2つの協調フィルタリングリランキング技法（貪欲なリランキング技法のバリエーション、アルゴリズム1を参照）のうちの1つによって生成された推薦文を評価した。
The study results showed that, while the users positively perceived the diversification (movies suggested by the two diversity-aware techniques received the highest ratings on average), they had more confidence in recommendations produced by the least diverse approach—the content-based technique.
研究の結果、ユーザーは多様化を肯定的に受け止めたが（2つの多様性を考慮した手法によって提案された映画が平均して最も高い評価を得た）、最も多様性のない手法（コンテンツ・ベースの手法）によって作成されたレコメンデーションに対する信頼度は高かった。
Castagnos et al.explain this result in terms of the users’ appreciation of recommendation transparency: the users were more confident when they clearly understood why a particular item was recommended (e.g., being very similar to a previously rated item).
Castagnosらはこの結果を、推薦の透明性に対するユーザーの評価という観点から説明している。ユーザーは、特定のアイテムが推薦された理由（例えば、以前に評価されたアイテムに非常に似ているなど）を明確に理解することで、より自信を持つことができた。
This result suggests that while diversity may be positively perceived by users, additional explanations may be important for improving the acceptance of such recommendations.
この結果は、多様性はユーザーに肯定的に受け止められるかもしれないが、そのような推奨の受容性を高めるためには、さらなる説明が重要かもしれないことを示唆している。
Zhang et al.[2012] performed a small-scale user study (21 participants) to evaluate a serendipity-enhancing recommender for Last.fm music artists (see also Section 3.2).
Zhangら[2012]は、Last.fm音楽アーティストのセレンディピティを高めるレコメンダーを評価するために、小規模なユーザー研究（21人の参加者）を行った（セクション3.2も参照）。
Participants of the study were asked to provide six artists they like as a “seed” for the recommender and subsequently to evaluate two recommendation lists generated by a baseline recommender and the serendipity-enhancing version of the system.
研究参加者は、レコメンダーの "種 "として好きなアーティストを6人提供し、その後、ベースライン・レコメンダーとセレンディピティを強化したバージョンのシステムによって生成された2つの推薦リストを評価するよう求められた。
The perceived enjoyment (from “dislike the song” to “will definitely listen again”) and serendipity (from “exactly what I listen to normally” to “something I would never have listened to otherwise”) of the recommendations were measured on a 5-point Likert scale.
推薦された曲の楽しさ（「嫌いな曲」から「また必ず聴く曲」まで）とセレンディピティ（「普段聴いている曲と同じ」から「他では絶対に聴かなかった曲」まで）を5段階のリッカート尺度で測定した。
The users’ familiarity with the recommended artists was also recorded.
また、推薦されたアーティストに対するユーザーの馴染み度も記録された。
The study results showed the users to perceive recommendations generated by the serendipity-enhancing system version as less enjoyable, but more serendipitous.
研究の結果、セレンディピティ強化システムバージョンによって生成されたレコメンデーションは、ユーザーにとってあまり楽しいものではなかったが、よりセレンディピティなものであった。
The serendipity-enhancing version was also shown to provide more recommendations of novel artists (i.e., ones unknown to the users).
また、セレンディピティを強化したバージョンは、新規のアーティスト（つまり、ユーザーにとって未知のアーティスト）をより多く推薦することが示された。
Interestingly, despite providing less enjoyable recommendations, the serendipity-enhancing system version was preferred over the baseline system as the users were willing to sacrifice recommendation accuracy for the sake of discovering new interesting artists.
興味深いことに、あまり楽しくないレコメンデーションを提供するにもかかわらず、セレンディピティ強化システムのバージョンはベースラインシステムよりも好まれた。
An important question is whether users in domains where the cost of receiving inaccurate recommendations is higher (e.g., movie recommendations) would also be prepared to sacrifice accuracy for serendipity.
重要な疑問は、不正確なレコメンデーションを受けるコストがより高いドメイン（例えば映画のレコメンデーション）のユーザーが、セレンディピティのために正確さを犠牲にする用意があるかどうかである。
Finally, we observe that research discussed in this section deals with user studies in which participants are aware of their involvement in the experiments.
最後に、このセクションで議論されている研究は、参加者が実験への関与を自覚しているユーザー研究を扱っていることを観察する。
While such studies may reveal important findings, they can only offer an approximation of the user behavior in real-life settings.
このような研究は重要な発見をもたらすかもしれないが、現実の環境におけるユーザー行動の近似値しか提供できない。
There is a lack of reported A/B evaluation studies (i.e., online experiments where the users are unaware of their participation) that analyze the impact of beyond-accuracy objectives on user behavior.
精度を超えた目標がユーザーの行動に与える影響を分析したA/B評価研究（つまり、ユーザーが参加したことを意識しないオンライン実験）が報告されていない。

# Offline Analysis of Beyond-accuracy objectives ビヨンド精度目標のオフライン分析

Having reviewed research that addresses the definition, optimization, and measurement of the different beyond-accuracy objectives, we aim to further contribute to the beyond-accuracy recommendation research with a novel analysis of relationships between the different objectives.
精度を超える様々な目標の定義、最適化、測定に取り組む研究をレビューしてきたが、我々は、異なる目標間の関係の斬新な分析によって、精度を超える推薦研究にさらに貢献することを目指す。
While existing research on diversity, novelty, serendipity, or coverage typically addresses one specific objective, we believe it is important to understand which objectives are corelated, which are in conflict, and how optimizing for one objective can affect the other objectives.
多様性、新規性、セレンディピティ、カバレッジに関する既存の研究は、通常1つの特定の目的を扱っているが、我々は、どの目的が重なり合っているのか、どの目的が対立しているのか、1つの目的を最適化することが他の目的にどのような影響を与えるのかを理解することが重要だと考えている。
A number of previous works report on experiments where multiple beyond-accuracy objectives are measured in offline settings.
多くの先行研究が、複数の精度を超える目標をオフライン設定で測定する実験について報告している。
Next we review their findings and position our work with respect to these previous efforts.
次に、これらの研究成果をレビューし、私たちの研究をこれらの先行研究に対して位置づける。
Ribeiro et al.[2012] proposed an approach for balancing recommendation accuracy, diversity, and novelty using a weighted combination of the predicted relevance scores that come from a number of different recommendation algorithms.
Ribeiroら[2012]は、複数の異なる推薦アルゴリズムから得られる関連性予測スコアの加重結合を用いて、推薦精度、多様性、新規性のバランスをとるアプローチを提案している。
The authors have measured the performance of various state-of-the-art recommendation approaches (including popularity-based, content-based, k-nearest-neighbor, and matrix factorization techniques) in terms of accuracy, diversity, and novelty.
著者らは、様々な最先端の推薦アプローチ（人気度ベース、コンテンツベース、k-最近傍、行列因数分解技術を含む）の性能を、精度、多様性、新規性の観点から測定した。
Offline evaluation results on MovieLens and Last.fm datasets showed that none of the algorithms dominates in all three objectives: on the MovieLens dataset, the SVD factor model with 50 factors provided the most accurate recommendations, the popularity-based approach the most diverse, and the SVD model with 150 factors the most novel.
MovieLensデータセットとLast.fmデータセットを用いたオフライン評価の結果、どのアルゴリズムも3つの目的すべてにおいて優位に立つことはなかった。MovieLensデータセットでは、50因子を持つSVD因子モデルが最も正確な推薦を提供し、人気度ベースのアプローチが最も多様性に富み、150因子を持つSVDモデルが最も斬新であった。
On Last.fm data, the factor model for implicit data generated the most accurate recommendations, the SVD model with 150 factors the most novel, and the user-based k-NN approach the most diverse.
Last.fmのデータでは、暗黙データの因子モデルが最も正確なレコメンデーションを生成し、150因子のSVDモデルが最も斬新で、ユーザーベースのk-NNアプローチが最も多様であった。
Combining predictions generated by the different algorithms resulted in hybrid solutions that performed similarly to the best algorithms in each individual objective (accuracy, diversity, or novelty), but better in the other two objectives.
異なるアルゴリズムによって生成された予測を組み合わせることで、個々の目的（正確性、多様性、新規性）において最良のアルゴリズムと同様のパフォーマンスを示すハイブリッドソリューションが得られたが、他の2つの目的においてはより優れていた。
Bellog´ın et al.[2013] evaluated the performance of a number of recommendation approaches that the authors grouped into three categories: rating-based techniques, content-based techniques (exploiting content labels), and social techniques (exploiting friendship relations between users).
Bellog´ınら[2013]は、著者らが3つのカテゴリーに分類した多くの推薦アプローチのパフォーマンスを評価した：レーティングベースのテクニック、コンテンツベースのテクニック（コンテンツラベルを利用）、ソーシャルテクニック（ユーザー間の友情関係を利用）。
In addition to the traditional precision and recall metrics, the performance metrics included diversity (α-nDCG metric [Clarke et al.2008]), novelty, and coverage.
従来の精度と想起の指標に加え、多様性（α-nDCG指標[Clarke et al.2008]）、新規性、カバレッジをパフォーマンス指標とした。
Experiments on three datasets—Delicious, Last.fm, and MovieLens—showed the content-based approach to achieve the highest coverage and novelty on the Last.fm and Delicious datasets.
Delicious、Last.fm、MovieLensの3つのデータセットで実験した結果、Last.fmとDeliciousのデータセットでは、コンテンツベースのアプローチが最も高いカバレッジと新規性を達成した。
Interestingly, on the MovieLens dataset, a user-based k-NN method provided the most novel recommendations.
興味深いことに、MovieLensデータセットでは、ユーザーベースのk-NN法が最も新しいレコメンデーションを提供した。
On Last.fm and Delicious data, the social recommenders were best in terms of diversity.
Last.fmとDeliciousのデータでは、ソーシャル・レコメンダーが多様性の点で最も優れていた。
(Social recommenders could not be applied to the MovieLens dataset as the data contains no user-to-user relations.) On the MovieLens dataset, content-based approaches were shown to outperform rating-based techniques in terms of α-nDCG diversity.
(ソーシャル・リコメンダーはMovieLensデータセットに適用できなかった。） MovieLensデータセットでは、α-nDCGの多様性において、コンテンツベースのアプローチがレーティングベースのテクニックを上回ることが示された。
Pamp´ın et al.[2014] analyzed the performance of item-based and user-based k-NN approaches in terms of accuracy, diversity, and novelty.
Pamp´ınら[2014]は、アイテムベースとユーザーベースのk-NNアプローチの性能を、精度、多様性、新規性の観点から分析した。
They conducted offline experiments on the MovieLens dataset with different values of the neighborhood size k for the user-based approach and a fixed value of k = 300 for the item-based approach.
彼らはMovieLensデータセットで、ユーザーベースのアプローチでは近傍サイズkの値を変え、アイテムベースのアプローチではk = 300の固定値でオフライン実験を行った。
The evaluation results showed that at small values of k, the user-based approach provides more novel recommendations than the item-based approach, but the novelty decreases for larger values of k and matches the novelty of item-based recommendations at k = 100.
評価結果は、kの値が小さいときには、ユーザーベースのアプローチはアイテムベースのアプローチよりも新規性の高い推薦を提供するが、kの値が大きくなるにつれて新規性は低下し、k = 100ではアイテムベースの推薦の新規性と一致することを示している。
The user-based approach was also shown to provide more diverse recommendations compared to the item-based approach, with diversity decreasing for larger values of k but remaining higher compared to the diversity of item-based recommendations (which were computed with k = 300).
また、ユーザーベースのアプローチは、アイテムベースのアプローチと比較して、より多様な推奨を提供することが示され、多様性はkの値が大きいほど減少するが、アイテムベースの推奨の多様性（k = 300で計算された）と比較して高いままであった。

Jannach et al.[2013] analyzed the tendency of various recommendation approaches to focus on certain parts of the item catalog.
Jannachら[2013]は、アイテムカタログの特定の部分に焦点を当てる様々な推薦アプローチの傾向を分析した。
They evaluated recommendations in terms of coverage (measured as the aggregate number of items appearing in top-10 recommendation lists and as the Gini coefficient metric [Fleder and Hosanagar 2009]) and popularity bias (measured as the average rating value of recommended items and as the average number of ratings per item).
彼らは、レコメンデーションをカバレッジ（トップ10レコメンデーションリストに登場するアイテムの総数とジニ係数指標[Fleder and Hosanagar 2009]として測定）と人気バイアス（レコメンデーションされたアイテムの平均評価値とアイテムごとの平均評価数として測定）の観点から評価した。
The recommendation techniques that they evaluated included state-of-the-art neighbor-based and matrix factorization algorithms, a learning-to-rank approach for implicit rating data, and a content-based approach based on item labels.
彼らが評価した推薦技術には、最新の近傍ベースおよび行列分解アルゴリズム、暗黙の評価データに対する学習ランクアプローチ、項目ラベルに基づくコンテンツベースアプローチなどがある。
The evaluation results on the MovieLens dataset showed that the most accurate algorithm—the learning-to-rank approach—tends to focus on the popular items in the catalog, being also the worst in terms of novelty.
MovieLensデータセットでの評価結果は、最も精度の高いアルゴリズム（ランク付け学習アプローチ）は、カタログの人気アイテムに集中する傾向があり、新規性の点でも最悪であることを示した。
Interestingly, the learning-to-rank approach performed well in terms of coverage, being second only to the content-based approach.
興味深いことに、学習順位のアプローチはカバー率の点で良い結果を出し、コンテンツ・ベースのアプローチに次ぐものであった。
The SVD matrix factorization approach also performed well in terms of coverage, while neighbor-based approaches achieved low coverage, showing a tendency to focus on a small portion of the item catalog.
SVD行列分解アプローチもカバレッジの点で良い結果を示したが、ネイバーベースのアプローチはカバレッジが低く、アイテムカタログのごく一部にフォーカスする傾向が見られた。
Overall, all ratingbased algorithms were shown to suffer to some extent from popularity bias, the contentbased approach being the only approach that was not biased toward popular items.
全体として、すべてのレーティングベースのアルゴリズムは、ある程度人気バイアスに悩まされることが示されたが、コンテンツベースのアプローチは、人気アイテムに偏らない唯一のアプローチであった。
Compared to the previous efforts discussed, our work contains a broader set of performance metrics, covering the most popular recommender system beyond-accuracy objectives.
これまで議論されてきた取り組みと比較して、我々の研究は、最も一般的な推薦システムの精度を超えた目標をカバーする、より広範なパフォーマンスメトリクスのセットを含んでいる。
For diversity, novelty, and coverage, we employed the metric definitions most widely encountered in the literature, while for the serendipity objective, we propose two alternative ways of measuring surprise, which constitutes the core component of serendipity.
多様性、新規性、網羅性については、文献で最も広く使われている指標定義を採用した。一方、セレンディピティの目的については、セレンディピティの中核的要素を構成する驚きを測定する2つの代替方法を提案した。
Recently, Maksai et al.[2015] analyzed a wide range of beyond-accuracy metrics— multiple variants of diversity, novelty, coverage, and serendipity—in an offline setting.
最近、Maksaiら[2015]は、多様性、新規性、カバレッジ、セレンディピティの複数のバリエーションなど、精度を超える幅広いメトリクスをオフライン設定で分析した。
The authors suggested predicting the online performance of a news recommender (measured by the click-through rate) using the offline metric values.
著者らは、オフラインの指標値を用いてニュース推薦者のオンラインパフォーマンス（クリックスルー率で測定）を予測することを提案した。
To identify which offline metrics are most likely to influence online performance of the system, Maksai et al.analyzed correlations between the metrics by measuring their values at equal time intervals on a news recommendation dataset.
Maksaiらは、どのオフライン指標がシステムのオンラインパフォーマンスに最も影響を与える可能性が高いかを特定するために、ニュース推薦データセット上で等間隔に値を測定し、指標間の相関関係を分析した。
The obtained results indicate no strong correlations between the metrics, with the exception of a strong (positive) correlation between coverage (computed using Shannon entropy [Shani and Gunawardana 2011]) and serendipity (computed using the definition of Murakami et al.[2008]).
得られた結果は、カバレッジ（Shannon entropy [Shani and Gunawardana 2011]を用いて計算）とセレンディピティ（Murakami et al[2008]の定義を用いて計算）の間に強い（正の）相関があることを除いて、メトリクス間に強い相関がないことを示している。
Our approach to measure metric correlations differs from that of Maksai et al.— rather than observing the change of metric values over time, we analyze how optimizing a recommender system for a specific objective affects other beyond-accuracy objectives.
メトリクス相関を測定する我々のアプローチは、Maksaiらのアプローチとは異なる-経時的なメトリクス値の変化を観察するのではなく、特定の目的のためにレコメンダーシステムを最適化することが、他の精度を超えた目的にどのような影響を与えるかを分析する。
We address this problem by evaluating a number of greedy reranking approaches against the different beyond-accuracy metrics.
我々はこの問題に対処するため、様々な貪欲なリランキングアプローチを様々な精度を超えるメトリクスに対して評価する。

## Reranking Approaches 再ランキングのアプローチ

In earlier sections of this article, we reviewed a number of the different approaches that have been proposed to enable recommender systems to generate not only accurate but also novel and surprising recommendations and diverse lists of recommendations.
本稿の前のセクションでは、レコメンダーシステムが正確なだけでなく、斬新で驚くべきレコメンデーションや多様なレコメンデーションリストを生成できるようにするために提案されてきた様々なアプローチについてレビューした。
One approach relies on reranking the lists of recommendations that are generated using baseline algorithms [Smyth and McClave 2001; Ziegler et al.2005; Kelly and Bridge 2006; Adomavicius and Kwon 2012].
1つのアプローチは、ベースラインアルゴリズムを使用して生成されたレコメンデーションリストの再ランク付けに依存している[Smyth and McClave 2001; Ziegler et al.2005; Kelly and Bridge 2006; Adomavicius and Kwon 2012]。
Other approaches require the development of new recommendation models where accuracy and additional objectives are addressed simultaneously [Vargas et al.2011; Oku and Hattori 2011; Hurley 2013; Su et al.2013].
他のアプローチでは、精度と付加的な目的に同時に取り組む新しい推薦モデルの開発が必要となる[Vargas et al.2011; Oku and Hattori 2011; Hurley 2013; Su et al.2013]。
In our experiments, we chose to use the reranking approach, since it allows us to use existing state-of-the-art recommendation algorithms and allows us to explicitly control the tradeoff between recommendation accuracy and diversity, novelty, or serendipity.
我々の実験では、リランキング・アプローチを使用することにした。リランキング・アプローチは、既存の最先端の推薦アルゴリズムを使用することができ、推薦精度と多様性、新規性、セレンディピティとの間のトレードオフを明示的に制御することができるからである。
The reranking approach that we adopt follows the greedy algorithm described by Smyth and McClave [2001] (see Section 2.2.1, Algorithm 1), where a list of candidate recommendations is reranked by greedily maximizing an objective function:
我々が採用するリランキングアプローチは、Smyth and McClave [2001] (セクション2.2.1、アルゴリズム1を参照)によって記述された貪欲アルゴリズムに従う：

$$
\tag{6}
$$

The function combines recommendation accuracy and one of the beyond-accuracy objectives: given an item i, the item’s predicted relevance, rel(i), is combined with its diversity, novelty, or surprise score relative to the items already in the result list R, which we denote by obj(i, R).
この関数は、レコメンデーションの精度と、精度を超えた目標の1つを組み合わせたものである。アイテムiが与えられた場合、そのアイテムの予測される関連性rel(i)は、結果リストRに既にあるアイテムに対する多様性、新規性、驚きのスコアと組み合わされ、これをobj(i, R)と呼ぶ。
To control the balance between accuracy and the alternative objectives, the rel(i) and obj(i, R) scores were standardized and the α parameter was set to 0.5 in all the experiments.
精度と代替目的のバランスを制御するために、rel(i)とobj(i, R)のスコアは標準化され、αパラメータはすべての実験で0.5に設定された。
In the following, we describe the different implementations of obj(i, R) that were used in the experiments.
以下では、実験に使われたobj(i, R)のさまざまな実装について説明する。

### Diversity Reranking. 多様性の再ランキング

We adopted the definition of diversity that is based on the average pairwise item distance, which is widely accepted in the RS literature [Smyth and McClave 2001; Ziegler et al.2005; Kelly and Bridge 2006; Vargas and Castells 2011] (see Section 2.2.1, Equation (2)):
多様性の定義として、RSの文献で広く受け入れられている平均対項目間距離に基づく定義を採用した [Smyth and McClave 2001; Ziegler et al.2005; Kelly and Bridge 2006; Vargas and Castells 2011]。(セクション2.2.1の式(2)を参照）：

$$
\tag{7}
$$

As mentioned in Section 2.1, the item distance function dist(i, j) has been defined using a variety of metrics.
セクション2.1で述べたように、項目距離関数dist(i, j)は様々な測定基準を用いて定義されてきた。
In our experiments, we evaluate two variants of the distance function—one based on item content labels and the other based on item ratings.
実験では、2種類の距離関数を評価した。1つは項目の内容ラベルに基づくもの、もう1つは項目の評価に基づくものである。

Content-Based Diversity.
コンテンツに基づく多様性。
We employ the complement of the Jaccard similarity metric for comparing items described with a set of content labels (e.g., movies or artists labeled with genres):
私たちは、コンテンツ・ラベルの集合（例えば、ジャンルでラベル付けされた映画やアーティスト）で記述されたアイテムを比較するために、Jaccard類似度メトリックの補集合を採用する：

$$
\tag{8}
$$

where Li and Lj are the sets of labels describing items i and j, respectively.
ここで、LiとLjはそれぞれアイテムiとjを表すラベルの集合である。
Rating-Based Diversity.
格付けに基づく多様性。
An alternative formulation of item distance is based on userassigned ratings.
項目距離の別の定式化は、ユーザーが割り当てた評価に基づく。
We use the complement of the adjusted cosine similarity normalized to [0,1]:
我々は、[0,1]に正規化された調整済み余弦類似度の補数を使用する：

$$
\tag{9}
$$

where ¯ri and ¯rj are the average rating values for items i and j, respectively.
ここで、¯riと¯rjはそれぞれアイテムiとjの平均評価値である。
Only users who rated both items are considered for the diversity computation.
多様性の計算には、両方の項目を評価したユーザーのみが考慮される。

### Surprise Reranking. サプライズ再ランキング

Our approach to measuring surprise is based on the intuition that a recommendation is surprising if it is unlike any item the user has seen before.
驚きを測定するための我々のアプローチは、推薦が、ユーザーが以前に見たどのアイテムとも異なっている場合、驚きであるという直感に基づいている。
We use the lower-bound item distance from the items in the user’s profile as an indicator of surprise.
ユーザーのプロファイルの項目からの下限項目距離を驚きの指標として使用する。
We chose the lower-bound distance function rather than the more commonly used average distance since we believe that averaging the distance scores results in information loss, especially if the user has diverse items in his or her rating profile (see Kaminskas and Bridge [2014] for details).
我々は、距離スコアを平均化すると、特にユーザーが自分の評価プロファイルに多様な項目を持っている場合、情報損失が生じると考えているため、より一般的に使用される平均距離ではなく、下界距離関数を選択した（詳細はKaminskas and Bridge [2014]を参照）。
We propose two alternative definitions of surprise, based on different item distance functions.
我々は、異なる項目距離関数に基づく、2つの代替的な驚きの定義を提案する。
The first metric exploits users’ rating behavior to measure the likelihood for a pair of items to be seen by the same user.
1つ目の指標は、ユーザーの評価行動を利用して、2つのアイテムのペアが同じユーザーに見られる可能性を測定する。
While this information is not direct evidence of item dissimilarity, it provides a reasonable approximation—items that are rarely observed together are likely to be different.
この情報は項目の非類似性の直接的な証拠ではないが、合理的な近似値を提供する。
The second metric employs a more straightforward item distance function, based on content labels.
2つ目のメトリックは、コンテンツラベルに基づく、より単純なアイテム距離関数を採用している。

Given the target item and the user’s profile (a set of items rated by the user), both metrics produce a score that indicates the level of surprise the target item brings to the user.
ターゲット・アイテムとユーザーのプロファイル（ユーザーによって評価されたアイテムのセット）が与えられると、両方のメトリクスは、ターゲット・アイテムがユーザーにもたらす驚きのレベルを示すスコアを生成する。
Note that, unlike some previous works [Vargas and Castells 2011; Adamopoulos and Tuzhilin 2014], we do not consider item relevance in our definitions of surprise.
いくつかの先行研究[Vargas and Castells 2011; Adamopoulos and Tuzhilin 2014]とは異なり、われわれはサプライズの定義においてアイテムの関連性を考慮していないことに留意されたい。
While relevance is an important component of serendipity, we leave it to be measured by dedicated accuracy metrics.
関連性はセレンディピティの重要な要素であるが、私たちはそれを専用の精度メトリクスで測定することに委ねている。
Furthermore, neither metric is presently rank aware, although they could be adapted to discount items that appear lower in the recommendation list.
さらに、どちらの指標も今のところランクを意識していないが、推薦リストの下位に表示されるアイテムを割り引くように適応させることはできるだろう。
Co-occurrence-Based Surprise.
共起ベースのサプライズ。
The first definition is based on the probability for the item to be seen (i.e., rated) together with the items in the user’s profile.
最初の定義は、アイテムがユーザーのプロフィールにあるアイテムとともに見られる（つまり評価される）確率に基づいている。
To measure the pairwise co-occurrence of items, we employed normalized point-wise mutual information (PMI) [Bouma 2009], which measures the probability of observing specific outcomes of two independent random variables together.
アイテムのペアごとの共起度を測定するために、2つの独立した確率変数の特定の結果を一緒に観測する確率を測定する正規化ポイントワイズ相互情報（PMI）[Bouma 2009]を採用した。
Given a pair of items i and j, we compute their PMI value as
アイテムiとjのペアが与えられたとき、それらのPMI値を次のように計算する。

$$
\tag{10}
$$

where p(i) and p(j) represent the probabilities for the items to be rated by any user, that is, p(i) = |{u∈U,rui=∅}| |U| , and p(i, j) is the probability for the same user to rate both items, that is, p(i, j) = |{u∈U,rui=∅∧ruj=∅}| |U| .
{u∈U,rui=∅}
PMI values range from −1 (in the limit) to 1, with −1 meaning the two items are never rated together, 0 signifying independence of the items, and 1 meaning complete co-occurrence of the items.
PMIの値は-1（限界値）から1まであり、-1は2つの項目が一緒に評価されることがないこと、0は項目の独立性、1は項目の完全な共起を意味する。
In order to measure the surprise of a recommended item i, we compute its PMI with each item in the user’s profile.
推薦されたアイテムiの驚きを測定するために、ユーザーのプロファイル内の各アイテムとのPMIを計算する。
Since higher values of PMI(i, j) signify higher cooccurrence of items i and j (and therefore low surprise of seeing the two items together), we take the complement of the PMI normalized to [0,1].
PMI(i,j)の値が高いほど、iとjのアイテムの共起性が高い（つまり、2つのアイテムが一緒に表示される驚きが低い）ことを意味するので、[0,1]に正規化されたPMIの補数をとります。
Taking the minimum of these values indicates the lower bound of the surprise perceived by the user when item i is recommended:
これらの値の最小値をとることで、アイテムiが推薦されたときにユーザーが感じる驚きの下限を示す：

$$
\tag{11}
$$

where P is the user’s profile (i.e., his or her set of rated items).
ここで、Pはユーザーのプロファイル（すなわち、評価されたアイテムのセット）である。
(In this equation, and in Equations (12) and (13), we drop the parameter R, i.e., we write objco−occ surprise(i) rather than objco−occ surprise(i, R), since these metrics do not depend on the items already in the result list.) Content-Based Surprise.
(この式、および式(12)と式(13)では、パラメータRを削除する。つまり、objco-occ surprise(i, R)ではなく、objco-occ surprise(i)と書く。） 内容ベースの驚き。
Our second surprise metric is based on distance applied to item content labels:
私たちの第二のサプライズ・メトリックは、アイテムの内容ラベルに適用される距離に基づく：

$$
\tag{12}
$$

where the distance is computed as the complement of Jaccard similarity (see Equation (8)).
ここで、距離はJaccard類似度の補数として計算される（式(8)参照）。
Similarly to the co-occurrence-based definition, the distance is computed for all pairs consisting of the target item i and the items in the user’s profile.
共起に基づく定義と同様に、距離はターゲット・アイテムiとユーザーのプロファイルのアイテムからなるすべてのペアについて計算される。
Taking the minimum distance value as the overall surprise represents the lower bound of how surprising the item is with respect to the seen items.
距離の最小値を総合的な驚きとすることで、そのアイテムが見たアイテムに対してどの程度驚くかの下限を表す。

### Novelty Reranking. ノベルティ再ランキング

For novelty, we use the item’s self-information or inverse user frequency [Zhou et al.2010; Vargas and Castells 2011], which is the fraction of users in the dataset who rated the item i:
新規性については、項目の自己情報または逆ユーザー頻度[Zhou et al.2010; Vargas and Castells 2011]を使用する：

$$
\tag{13}
$$

The logarithm is used to emphasize the novelty of the most rare items.
対数は、最も希少なアイテムの目新しさを強調するために使われる。

## Experimental Setup 実験セットアップ

To study the relationships between the different beyond-accuracy objectives, we conducted a number of offline experiments using four state-of-the-art recommendation algorithms and the five variants of the greedy reranking approach described previously— two variants for both diversity (Equations (8) and (9)) and surprise (Equations (11) and (12)) and one for novelty (Equation (13)).
様々な精度を超える目的間の関係を調べるために、4つの最新の推薦アルゴリズムと、前述の貪欲な再ランク付けアプローチの5つのバリエーション（多様性（式(8)と(9)）と驚き（式(11)と(12)）の両方に対応する2つのバリエーションと、新規性（式(13)）に対応する1つのバリエーション）を用いて、多くのオフライン実験を行った。
In each experiment, a recommendation algorithm was used to generate a ranked list of candidate recommendations C (|C| = 50).
C| = 50).
Then, we reranked C using each of the five beyond-accuracy objectives (Equation (6), α = 0.5).
次に、5つの精度を超える目標（式(6)、α = 0.5）をそれぞれ用いてCを再ランク付けした。
Finally, we obtained the list of top-N recommendations (N = 10 was used in all the experiments) from the reranked lists.
最後に、再ランク付けされたリストからトップNの推薦リスト（すべての実験でN = 10が使用された）を得た。
The value of C = 50 has been chosen to allow for a sufficiently large pool of candidate items while not slowing the performance significantly.
C=50の値は、性能を著しく低下させることなく、候補アイテムのプールを十分に大きくできるように選択されている。
Using the value of α = 0.5 allowed a good balance between the predicted relevance and the beyond-accuracy objective (the scores of the two components in Equation (6) were standardized).
α=0.5の値を使用することで、予測される関連性と精度を超えた目的との間で良好なバランスをとることができた（式(6)の2つのコンポーネントのスコアは標準化された）。
Next, we describe the evaluation methodology, performance metrics, datasets, and recommendation algorithms that were employed in the experiments.
次に、実験に採用した評価方法、パフォーマンス指標、データセット、推薦アルゴリズムについて説明する。

### Evaluation Methodology. 評価方法

In recent years, rating-based accuracy metrics for offline RS evaluations have been replaced by precision-oriented metrics that more closely reflect the users’ interaction with the system—considering only a small set of topranked recommendations, ignoring the lower-ranked items [Bellog´ın et al.2011].
近年、オフラインのRS評価における評価ベースの精度メトリクスは、ユーザーのシステムとのインタラクションをより忠実に反映する精度指向のメトリクスに取って代わられている-つまり、ランキング下位のアイテムを無視して、ランキング上位の推奨アイテムの小さなセットのみを考慮するのである[Bellog´ın et al.2011]。
In accordance with these state-of-the-art evaluation strategies, in this work we adopt the one plus random methodology [Koren 2008].
このような最先端の評価戦略に従い、本研究では、1プラスランダム手法[Koren 2008]を採用する。
The methodology is based on randomly splitting each user’s ratings to give a training set M and probe set P.
この方法は、各ユーザーの評価をランダムに分割し、トレーニングセットMとプローブセットPを与えることに基づいている。
The test set T is constructed by selecting all highly rated items (e.g., those having a five-star rating on a 1 to 5 scale) from the user’s probe set P.
テストセットTは、ユーザーのプローブセットPから高評価のアイテム（例えば、1～5の5段階評価のもの）をすべて選択することによって構築される。
Then, for each user u and for each test item (from T), predictions are computed for 1,000 random unrated items plus the one test item.
次に、各ユーザーuと各テスト項目（Tから）に対して、1,000個のランダムな未評価項目と1個のテスト項目について予測を計算する。
The set of 1,001 items is ranked according to the recommender’s predicted scores and the top-N recommendations are selected.
1,001アイテムのセットは、レコメンダーの予測スコアに従ってランク付けされ、上位N個のレコメンデーションが選択される。
If the test item is among the top-N items, we have a hit.
テスト項目が上位N項目の中にあればヒット。
The overall performance of the system—recall—is calculated as the ratio of the number of hits over the total number of test cases.
システムの総合的な性能（recall）は、テストケースの総数に対するヒット数の比率として計算される。
In this article, results were obtained using a slight modification of the methodology— rather than selecting all highly rated items for each user’s test set T, we only used one randomly selected test item per user.
この論文では、手法を少し変更し、各ユーザーのテストセットTに高評価のアイテムをすべて選択するのではなく、ユーザーごとにランダムに選択した1つのテストアイテムのみを使用して結果を得た。
This way equal importance is given to all test users, whereas the original methodology allows users with larger test profiles to have more impact on the evaluation results.4 The underlying assumption of the one plus random methodology that the 1,000 unseen items are irrelevant is clearly undervaluing the performance, as certain items among the 1,000 may be actually relevant for the user.
1,000の未見項目は無関係であるというone plus random法の基本的な仮定は、明らかにパフォーマンスを過小評価している。
However, we believe this methodology to be appropriate when measuring the beyond-accuracy objectives of recommendations as it involves items the user has not discovered (i.e., unrated items), whereas other offline evaluation strategies only employ items the user has had no trouble discovering (i.e., already-rated items).
しかし、他のオフライン評価戦略では、ユーザが発見するのに苦労しなかった項目（すなわち、すでに評価された項目）のみを使用するのに対し、この方法は、ユーザが発見していない項目（すなわち、未評価の項目）を含むため、推奨の精度を超える目標を測定する場合に適切であると考える。

All experiment results reported in the following sections were computed using fivefold cross-validation with 80%/20% training/probe set split.
以下のセクションで報告されるすべての実験結果は、80%/20%のトレーニング/プローブセット分割による5重クロスバリデーションを用いて計算された。

### Performance Metrics. パフォーマンス指標。

In addition to the Recall metric, for each test user’s top-N recommendation list R, we compute the following beyond-accuracy metrics:
Recall指標に加えて、各テストユーザーのトップN推薦リストRについて、以下のbeyond-accuracy指標を計算する：

#### Two variants of the diversity metric—the rating-based diversity and the contentbased diversity: 評価ベースの多様性とコンテンツベースの多様性である：

$$
\tag{14}
$$

where for Divcont, dist(i, j) is computed based on item content labels (Equation (8)), and for Divratings, dist(i, j) is computed using the rating-based item distance (Equation (9))
ここで、Divcontの場合、dist(i, j)は項目内容ラベルに基づいて計算され（式(8)）、Divratingsの場合、dist(i, j)は評価に基づく項目距離を使って計算される（式(9)）。

#### Two variants of the surprise metric—the co-occurrence-based surprise and the content-based surprise: 共起ベースのサプライズとコンテンツベースのサプライズである：

$$
\tag{15}
$$

$$
\tag{16}
$$

where P is the target user’s profile (i.e., the set of rated items), PMI(i, j) is computed using Equation (10), and dist(i, j) uses Equation (8)
ここで、Pはターゲットユーザーのプロファイル（すなわち、評価されたアイテムのセット）であり、PMI(i, j)は式(10)を使用して計算され、dist(i, j)は式(8)を使用します。

#### The Novelty metric computed as the average item self-information: 平均的な項目の自己情報として計算される新規性の指標：

$$
\tag{17}
$$

where U is the set of all users in the dataset and novmax = − log2 1 |U| is the maximal possible novelty value, which is used to normalize the novelty score of each individual item into [0,1].
U
The previous metric values are averaged across all test users.
前の指標値は、すべてのテストユーザーの平均値である。
Finally, we measure the Coverage metric as the aggregate number of distinct items appearing in top-N lists of all test users:
最後に、すべてのテスト・ユーザーのトップ N リストに表示されるアイテムの総数として、カバレッジ・メトリクスを測定する：

$$
\tag{18}
$$

where Ru is the set of top-N recommendations generated for user u and U is the set of all test users.
ここで、Ruはユーザーuに対して生成されたトップNレコメンデーションの集合であり、Uはすべてのテストユーザーの集合である。
Note that five of the performance metrics (the ones related to diversity, surprise, and novelty) correspond to the five reranking approaches described in Section 7.1.For convenience, we adapt the notation of each reranking approach to the corresponding metric.
パフォーマンスメトリクスの5つ（多様性、驚き、新規性に関連するもの）は、セクション7.1で説明した5つのリランキングアプローチに対応していることに注意されたい。
For instance, we refer to the rating-based diversity metric as Divratings and we refer to the corresponding reranking approach (i.e., that reranks using this metric) as Divr ratings (Section 7.1.1, Equations (7) and (9)).
例えば、評価ベースの多様性指標をDivratingsと呼び、対応する再ランク付けアプローチ（すなわち、この指標を用いて再ランク付けを行うもの）をDivr ratingsと呼ぶ（セクション7.1.1、式（7）と式（9））。
The Recall and Coverage metrics do not have corresponding reranking approaches.
RecallとCoverageのメトリクスには、対応するリランキング・アプローチがない。
Thus, in total, we have seven metrics and five reranking approaches.
したがって、合計で7つのメトリクスと5つのリランキング・アプローチがある。

### Datasets. データセット

We tested the proposed beyond-accuracy reranking approaches on two benchmark datasets for offline recommender system evaluation—the MovieLens 1M dataset5 and the Last.fm 1K dataset.6 The MovieLens dataset contains ∼1 million ratings, 6,040 users, and 3,706 movies.
MovieLensデータセットには、約100万件の評価、6,040人のユーザー、3,706本の映画が含まれている。
The movies are annotated using a vocabulary of 18 genres (on average 1.65 genres per movie).
映画は、18のジャンル（映画1本あたり平均1.65ジャンル）の語彙を使って注釈付けされている。
To obtain richer content descriptors for the movies, we additionally scraped IMDb plot keywords for each movie and kept those labels that appeared in the profiles of at least 10 movies.
映画のより豊かなコンテンツ記述子を得るために、さらに各映画のIMDbプロットキーワードをスクレイピングし、少なくとも10本の映画のプロファイルに現れるラベルを保持した。
This resulted in an average of 60 labels per movie.
その結果、映画1本につき平均60枚のラベルが貼られた。
The Last.fm dataset contains the listening events for 992 users and more than 100K artists.
Last.fmデータセットには、992人のユーザーと10万人以上のアーティストのリスニングイベントが含まれている。
As the dataset is extremely sparse, we cleaned the set of artists by leaving only those for which we could obtain at least three Last.fm tags (using the artist.getTopTags method of the Last.fm API7) and discarding artists who were listened to by fewer than 20 users.
データセットが非常にまばらであるため、少なくとも3つのLast.fmタグ（Last.fm APIのartist.getTopTagsメソッドを使用7）を取得できたアーティストだけを残し、20人未満のユーザーが聴いたアーティストを除外することで、アーティストのセットをクリーニングした。
This resulted in 992 users and 7,280 artists, with a total of 500K ratings.
その結果、992人のユーザーと7,280人のアーティストが参加し、総評価数は50万件に達した。
The listening frequencies of the artists were transformed into ratings from 1 to 5 using the standard approach for converting frequency-based implicit feedback into numerical ratings [Celma 2009].
アーティストのリスニング周波数は、周波数ベースの暗黙的フィードバックを数値評価に変換するための標準的な手法[Celma 2009]を用いて、1から5までの評価に変換された。
To avoid noisy data, we retrieved a maximum of the 10 most popular labels for every artist and kept the labels that appeared in the profiles of at least 10 artists.
ノイジーなデータを避けるため、各アーティストについて最も人気のあるラベルを最大10個取得し、少なくとも10人のアーティストのプロフィールに登場するラベルを保持した。
This resulted in eight labels per artist on average.
その結果、1人のアーティストにつき平均8つのレーベルに所属することになった。

### Recommendation Algorithms. 推薦アルゴリズム

The reranking approaches described in Section 7.1 were evaluated with four state-of-the-art recommendation algorithms: a pairwise learning-to-rank algorithm [Weston et al.2010] (LTR), a PureSVD [Cremonesi et al.2010] matrix factorization algorithm implemented using the sparsesvd library8 (MF), and two k-nearest-neighbor algorithms—a user-based collaborative filtering method (UB) and an item-based collaborative filtering method (IB) [Desrosiers and Karypis 2011].
セクション7.1で説明したリランキングアプローチは、4つの最先端の推薦アルゴリズムで評価された。ペアワイズ学習ランクアルゴリズム[Weston et al.2010](LTR)、sparsesvdライブラリ8を使用して実装されたPureSVD[Cremonesi et al.2010]行列分解アルゴリズム(MF)、2つのk-nearest-neighborアルゴリズム、ユーザーベース協調フィルタリング法(UB)とアイテムベース協調フィルタリング法(IB)[Desrosiers and Karypis 2011]である。
We note that to achieve an optimal accuracy on the Last.fm dataset (which consists of implicit feedback data converted to explicit numeric ratings), an algorithm designed for implicit feedback may be a better choice.
Last.fmデータセット（明示的な数値評価に変換された暗黙的フィードバックデータから成る）で最適な精度を達成するためには、暗黙的フィードバック用に設計されたアルゴリズムの方が良い選択かもしれないことに注意。
However, since the goal of our experiments was not achieving the highest possible accuracy on both datasets but rather investigating the behavior of state-of-the-art algorithms with respect to beyondaccuracy metrics, we chose the four algorithms as representatives of the techniques most commonly discussed in the RS literature and evaluated the same set of algorithms with both datasets.
しかし、我々の実験の目的は、両方のデータセットで可能な限り高い精度を達成することではなく、beyondaccuracyメトリクスに関して最先端のアルゴリズムの挙動を調査することであったため、RSの文献で最も一般的に議論されている技術の代表として4つのアルゴリズムを選択し、両方のデータセットで同じアルゴリズムセットを評価した。
We optimized each algorithm’s parameters (using a grid search strategy) to maximize recommendation accuracy (i.e., the Recall metric) as this is the standard practice in RS research.
各アルゴリズムのパラメー タは、RS 研究の標準的な手法である推奨精度（Recall メトリク ス）を最大化するように（グリッド探索戦略を用いて）最適化した。
For the LTR algorithm, we optimized the regularization constant C ∈ {1, 10, 100, 1000}, the learning rate γ ∈ {0.01, 0.001, 0.0001}, and the number of factors f ∈ {25, 50, 75, 100}; for the MF algorithm, we optimized the number of factors f ∈ {25, 50, 75, 100, 150, 175, 200, 250}; and for the k-NN algorithms, the neighborhood size k ∈ [20, 250].
LTRアルゴリズムでは、正則化定数C∈{1, 10, 100, 1000}、学習率γ∈{0.01, 0.001, 0.0001}、因子数f∈{25, 50, 75, 100}を最適化した。 0001}、因子数f∈{25, 50, 75, 100}、MFアルゴリズムでは因子数f∈{25, 50, 75, 100, 150, 175, 200, 250}、k-NNアルゴリズムでは近傍サイズk∈[20, 250]を最適化した。
The selected parameter values for each algorithm/dataset combination are as follows:
各アルゴリズム／データセットの組み合わせで選択されたパラメータ値は以下の通り：

- LTR LTR

- MF MF

- UB UB

- IB 国際バカロレア

For comparison, we note that Jannach et al.[2013] in their analysis of beyondaccuracy objectives used item-based and user-based k-NN algorithms with k = 100 and an SVD matrix factorization algorithm with the number of factors f = 50.
比較のために、Jannachら[2013]のbeyondaccuracy objectivesの分析では、k = 100のアイテムベースとユーザーベースのk-NNアルゴリズムと、因子の数f = 50のSVD行列分解アルゴリズムが使用されている。
Bellog´ın et al.[2013] conducted experiments with k = 15 for both k-NN algorithms and f = 50 for the matrix factorization algorithm.
Bellog´ınら[2013]は、k-NNアルゴリズムではk = 15、行列因数分解アルゴリズムではf = 50で実験を行った。
Pamp´ın et al.[2014] found the accuracy of the user-based k-NN algorithm to improve with increasing k until k = 90 and to thereafter remain constant at least until k = 200.
Pamp´ınら[2014]は、ユーザーベースのk-NNアルゴリズムの精度は、k = 90まではkの増加とともに向上し、その後は少なくともk = 200までは一定であることを発見した。
(They did not optimize the item-based algorithm and fixed the value at k = 300 for their experiments.) In the following sections, we report our findings and compare the results with the previous works discussed in Section 7.
(彼らはアイテムベースのアルゴリズムを最適化せず、実験ではk = 300に固定した)。以下のセクションでは、我々の結果を報告し、セクション7で議論した先行研究と結果を比較する。
It is important to note that any reported differences should not be treated as definite conclusions but rather as indications for further research, as they may be influenced by a number of factors, such as the differences in preprocessing of the datasets, tuning of the algorithm parameters, and evaluation methodologies [Said and Bellog´ın 2014].
データセットの前処理、アルゴリズム・パラメーターのチューニング、評価方法の違いなど、多くの要因に影響される可能性があるため、報告された違いは明確な結論として扱われるべきものではなく、むしろさらなる研究の示唆として扱われるべきものであることに注意することが重要である[Said and Bellog´ın 2014]。
In particular, the one plus random methodology adopted in our experiments has been shown to favor approaches recommending more popular items [Cremonesi et al.2010; Jannach et al.2015b].
特に、我々の実験で採用された1プラスランダム手法は、より人気のあるアイテムを推奨するアプローチを好むことが示されている[Cremonesi et al.2010; Jannach et al.2015b]。
Consequently, optimizing a recommendation algorithm’s parameters using this methodology may result in the algorithm’s configuration being more popularity oriented compared to the parameter settings used in other studies.
その結果、この方法を用いて推薦アルゴリズムのパラメータを最適化すると、他の研究で用いられたパラメータ設定と比較して、より人気志向のアルゴリズム構成になる可能性がある。
However, we believe that the possible popularity biases of individual algorithms do not invalidate the findings of this research since we focus on the relative comparison of reranking strategies applied to the output of individual algorithms.
しかし、我々は、個々のアルゴリズムの出力に適用されるリランキング戦略の相対的な比較に焦点を当てているため、個々のアルゴリズムの人気のバイアスの可能性は、この研究の結果を無効にしないと信じています。

## Results and Discussion 結果と考察

We conducted two main sets of experiments.
主に2つの実験を行った。
One was aimed at comparing the performance of the four recommender algorithms (optimized for recall, as discussed in the previous section) in terms of the different beyond-accuracy performance metrics (Section 7.3.1).
一つは、4つのレコメンダーアルゴリズム（前節で議論したように、リコールに最適化されたもの）のパフォーマンスを、異なるbeyond-accuracyパフォーマンスメトリクス（セクション7.3.1）の観点から比較することを目的としたものである。
The other was aimed at evaluating the five reranking approaches: we used each reranking of the results of each of the four recommendation algorithms and recorded all performance measures (Section 7.3.2).
もうひとつは、5つのリランキング・アプローチの評価を目的としたもので、4つの推薦アルゴリズムそれぞれの結果の各リランキングを使用し、すべてのパフォーマンス指標を記録した（セクション7.3.2）。
Furthermore, we report initial observations regarding the influence of algorithm parameters on the performance metrics and reranking effectiveness (Section 7.3.3).
さらに、アルゴリズム・パラメータが性能指標とリランキング効果に及ぼす影響に関する初期的な観察結果を報告する（セクション7.3.3）。

### Comparison of Recommendation Algorithms. 推薦アルゴリズムの比較。

Figures 1 and 2 show the results obtained for each of the four recommendation algorithms on the MovieLens and Last.fm datasets, respectively.
図1と図2は、それぞれMovieLensとLast.fmデータセットにおける4つの推薦アルゴリズムそれぞれの結果を示している。
On the MovieLens dataset (Figure 1), the LTR and MF algorithms show a similar performance: both are the best in accuracy (Recall) and diversity (Divcont and Divratings) and lose to the k-NN algorithms in surprise (Scont and Sco−occ).
MovieLensデータセット（図1）において、LTRアルゴリズムとMFアルゴリズムは同様の性能を示した：両者とも精度（Recall）と多様性（DivcontとDivratings）で最高であり、驚き（ScontとSco-occ）ではk-NNアルゴリズムに負ける。
However, the LTR algorithm significantly outperforms the MF algorithm in Novelty and Coverage, which indicates a tendency of the matrix factorization algorithm to focus on popular items (i.e., ones with low novelty).
しかし、LTRアルゴリズムは、新規性とカバレッジにおいてMFアルゴリズムを大幅に上回っている。これは、行列因数分解アルゴリズムが、人気のある項目（すなわち、新規性の低い項目）に注目する傾向を示している。
We compare these results with the findings of Jannach et al.[2013], who used the MovieLens dataset (although rather than using the 1 million rating set, Jannach et al.used a subset of the 10 million rating set) and a different learning-to-rank approach (the Bayesian Personalized Ranking algorithm, which was designed for implicit feedback data).
Jannachら[2013]は、MovieLensデータセットを使用し（ただし、Jannachらは100万レーティングセットではなく、1000万レーティングセットのサブセットを使用した）、異なる学習ランク付けアプローチ（暗黙的フィードバックデータ用に設計されたベイズパーソナライズランキングアルゴリズム）を使用した。
Jannach et al.report that both learning-to-rank and matrix factorization achieve high catalog coverage but perform poorly in terms of novelty (the learning-to-rank algorithm being particularly vulnerable to the popularity bias).
Jannachらの報告によれば、ランク学習と行列分解はともに高いカタログカバレッジを達成するが、新規性という点では劣る（ランク学習アルゴリズムは特に人気バイアスの影響を受けやすい）。
In our results, we observe a more direct link between high coverage and novelty—the LTR algorithm doing well at both and the MF algorithm showing inferior performance.
我々の結果では、高いカバレッジと新規性の間には、より直接的な関係があり、LTRアルゴリズムはその両方において優れているが、MFアルゴリズムは劣っている。

The IB and UB k-NN algorithms show a similar performance in terms of Recall, Divcont, and Divratings metrics, both losing to the LTR and MF algorithms.
IBとUBのk-NNアルゴリズムは、Recall、Divcont、Divratingsの指標において同様の性能を示し、どちらもLTRとMFアルゴリズムに負けている。
The IB k-NN algorithm achieves second-best performance in Novelty (losing only to the LTR algorithm) and is the best in Coverage.
IB k-NNアルゴリズムは、新規性で2位（LTRアルゴリズムにのみ負ける）の性能を達成し、カバレッジでは最高である。
On the other hand, the UB algorithm is generating the most surprising recommendations (Scont and Sco−occ) but shows the worst performance among the four algorithms in terms of Novelty and Coverage, which indicates a tendency to recommend popular items.
一方、UBアルゴリズムは最も意外性のある推薦（ScontとSco-occ）を生成しているが、新規性とカバレッジの点では4つのアルゴリズムの中で最悪のパフォーマンスを示しており、これは人気のあるアイテムを推薦する傾向を示している。
The observed performance of the UB algorithm is in contrast with results reported by Bellog´ın et al.[2013], who found the user-based k-NN algorithm to generate the most novel recommendations on the MovieLens dataset (compared to an item-based k-NN and an SVD algorithm).
UBアルゴリズムの観察された性能は、Bellog´nら[2013]によって報告された結果とは対照的である。Bellog´nらは、MovieLensデータセットにおいて、ユーザーベースのk-NNアルゴリズムが（アイテムベースのk-NNとSVDアルゴリズムと比較して）最も新しい推奨を生成することを発見した。
This difference may be explained by their neighborhood size (k = 15), as smaller neighborhood size corresponds to higher novelty (see Section 7.3.3).
この違いは、近傍サイズ（k = 15）によって説明できるかもしれない。近傍サイズが小さいほど新規性が高いからだ（セクション7.3.3参照）。
Jannach et al.found the UB algorithm to perform poorly in terms of coverage, which matches our findings.
Jannachらは、UBアルゴリズムがカバレッジの点で劣っていることを発見したが、これは我々の発見と一致する。
They also report a tendency of the UB algorithm to recommend either the most popular or the most novel items (with approximately equal frequency)—a result that could not be confirmed by our experiments, since we measure the algorithm’s novelty by averaging the novelty scores of items in recommendation lists (Equation (17)).
彼らはまた、UBアルゴリズムが最も人気のあるアイテムか、最も新規性の高いアイテムのどちらかを推奨する傾向があると報告している（頻度はほぼ同じ）。
On the Last.fm dataset (Figure 2), the results show a few differences compared to the MovieLens dataset.
Last.fmデータセット（図2）では、MovieLensデータセットと比較していくつかの違いが見られた。
The main difference in the results is the behavior of the LTR algorithm, which now loses to other algorithms in terms of Recall, Divratings, Novelty, and Coverage.
結果の主な違いは、LTRアルゴリズムの挙動であり、LTRアルゴリズムは、Recall、Divratings、Novelty、Coverageの点で他のアルゴリズムに負けている。
Moreover, the LTR algorithm shows the best results in surprise (Scont and Sco−occ).
さらに、LTRアルゴリズムはサプライズ（ScontとSco-occ）において最高の結果を示した。
The inferior performance of the LTR algorithm in terms of Recall could be caused by the recommender algorithms we chose to use and the rating data in the dataset— implicit feedback converted to numeric ratings (Section 7.2.4).
LTRアルゴリズムがRecallの点で劣っているのは、我々が選択したレコメンダーアルゴリズムと、データセットの評価データ（暗黙的フィードバックを数値評価に変換したもの）に起因している可能性がある（セクション7.2.4）。
The MF algorithm is the best in diversity (particularly Divcont) and is also second best in Novelty and Coverage, losing to the I B algorithm.
MFアルゴリズムは、多様性（特にDivcont）で最も優れており、新規性とカバレッジでもI Bアルゴリズムに負けて2番目に優れている。
Differently from the MovieLens results, the MF algorithm also performs better than the k-NN algorithms in terms of content-based surprise Scont.
MovieLensの結果とは異なり、MFアルゴリズムは、コンテンツベースのサプライズScontの点でもk-NNアルゴリズムよりも優れています。
Interestingly, the results on Last.fm data also show both k-NN algorithms to achieve the best Recall, slightly outperforming the MF algorithm.
興味深いことに、Last.fmデータでの結果も、k-NNアルゴリズムがともに最良のRecallを達成し、MFアルゴリズムをわずかに上回った。
This is in line with previous works showing that, when evaluating top-N recommendations (particularly using the one plus random methodology), the accuracy of simple techniques may be similar to that of the more advanced algorithms [Cremonesi et al.2010; Jannach et al.2013].
これは、トップNレコメンデーションを評価する場合（特に1プラスランダム手法を使用する場合）、単純な手法の精度がより高度なアルゴリズムの精度と同等である可能性があることを示す以前の研究と一致している[Cremonesi et al.2010; Jannach et al.2013]。
We compare our results on Last.fm data to the findings of Bellog´ın et al.[2013], who evaluated (among other techniques) item-based and user-based k-NN algorithms as well as an SVD factorization algorithm on a Last.fm dataset (the authors built a dedicated dataset with 1.9K users and 17.6K artists).
我々は、Last.fmデータ上での我々の結果を、Last.fmデータセット（著者らは1.9Kユーザーと17.6Kアーティストからなる専用データセットを構築した）上で（他の手法と同様に）アイテムベースとユーザーベースのk-NNアルゴリズムとSVD因数分解アルゴリズムを評価したBellog´nら[2013]の結果と比較する。
Results reported by Bellog´ın et al.confirm the high novelty and coverage achieved by the item-based k-NN algorithm.
Bellog´ınらによって報告された結果は、項目ベースのk-NNアルゴリズムによって達成された高い新規性と網羅性を裏付けている。
However, the authors also report the user-based k-NN algorithm to achieve second-best novelty and the best coverage results.
しかし、著者らは、ユーザーベースのk-NNアルゴリズムが、2番目に優れた新規性と最高のカバレッジ結果を達成したことも報告している。
As said earlier, this result can be explained by their small neighborhood size (k = 15).
先に述べたように、この結果は近傍サイズが小さい（k = 15）ことで説明できる。

### Comparison of Reranking Approaches. 再ランキング手法の比較。

Figure 3 shows the performance measure values obtained using the different reranking approaches with the MF algorithm on the MovieLens dataset.
図3は、MovieLensデータセットにおいて、MFアルゴリズムによるさまざまなリランキング・アプローチを使用して得られたパフォーマンス測定値を示している。
Analogous sets of results were obtained for every datasetalgorithm combination (eight sets of results in total).
すべてのデータとアルゴリズムの組み合わせについて、同様の結果が得られた（合計8セットの結果）。
To better describe the results, in this section, we outline the findings that are largely consistent across both datasets.
このセクションでは、結果をより明確に説明するために、両データセットでほぼ一貫している発見を概説する。
A full set of result figures is presented in the appendix.
結果の数値一式は付録に掲載されている。
In Figure 3 (and all the figures in the appendix), each individual chart (a) through (g) shows the values for one performance metric (named on the y-axis), with the different reranking approaches displayed along the x-axis.
図3（および付録のすべての図）では、個々のグラフ（a）～（g）は、1つのパフォーマンス指標（y軸に名前）の値を示しており、x軸に沿ってさまざまなリランキング・アプローチが表示されている。
The Baseliner approach corresponds to the original recommendation ranking generated by the respective algorithm.
Baselinerのアプローチは、それぞれのアルゴリズムによって生成されたオリジナルの推薦ランキングに対応する。
In other words, in the baseline there is no reranking.
言い換えれば、ベースラインでは再ランキングはない。
As said in Section 7.2.2, each performance metric except for Recall and Coverage corresponds to a reranking approach.
セクション7.2.2で述べたように、RecallとCoverage以外の各パフォーマンス指標は、リランキング・アプローチに対応している。
For instance, the diversity reranking Divr ratings is the approach that reranks the list of candidate recommendations according to the rating-based diversity objective (see Section 7.1.1) and therefore corresponds to the Divratings metric (see Equation (14)).
例えば、多様性再ランキングDivrレーティングは、レーティングベースの多様性目的（セクション7.1.1参照）に従って推奨候補リストを再ランキングするアプローチであり、したがってDivratingsメトリック（式（14）参照）に対応する。
As expected, Recall has its highest value when using the Baseliner ranking for each algorithm and is lowered using any of the reranking approaches (chart (a) in each figure).
予想通り、Recallは、各アルゴリズムでBaselinerランキングを使用した場合に最高値となり、どのリランキング・アプローチを使用しても低下する（各図の(a)）。
This illustrates the well-known tradeoff between recommendation accuracy and beyond-accuracy objectives.
これは、推薦の精度と精度を超える目的との間のトレードオフをよく表している。
For the diversity, surprise, and novelty metrics (charts (b)– (f) in each figure), the highest values are achieved using the corresponding reranking approaches, which is the expected outcome.
多様性、驚き、新規性の指標（各図の(b)～(f)）については、対応するリランキング・アプローチを用いると最高値が得られ、これは期待された結果である。
As said in Section 7, our main focus in these experiments was observing how each beyond-accuracy metric is affected by reranking approaches that are not directly optimizing the metric.
セクション7で述べたように、これらの実験における我々の主な焦点は、精度を超える各指標が、その指標を直接最適化しないリランキング・アプローチによってどのような影響を受けるかを観察することであった。
These observations allow us to identify positive or negative correlations between the different beyond-accuracy objectives: if a reranking approach significantly improves a metric compared to the baseline ranking, we can assume there exists a positive correlation between the reranking objective and the metric; on the other hand, if a reranking approach results in a value for the metric that is lower than the baseline, we assume a negative correlation between the reranking objective and the metric.
一方、リランキング・アプローチの結果、メトリックの値がベースラインよりも低くなった場合、リランキング目的とメトリックの間に負の相関があると仮定する。
Here we outline the discovered correlations between the different objectives.
ここでは、発見されたさまざまな目的間の相関関係を概説する。
As said earlier, the results for the Last.fm dataset are largely consistent with those obtained with the MovieLens data (the few notable exceptions are mentioned later).
先に述べたように、Last.fmデータセットの結果は、MovieLensデータで得られた結果とほぼ一致している（いくつかの顕著な例外は後述する）。

- Reranking the recommendations for novelty (i.e., using the Noveltyr reranking) hurts accuracy the most (see Figure 3, chart (a)). This is not surprising in the offline evaluation setting, as any offline evaluation methodology is (to a certain extent) biased toward popular items: user ratings in the test set are more likely to belong to popular items. It is worth noting that in three cases (MF, UB, and IB algorithms on Last.fm dataset), Noveltyr reranking has the second-worst Recall performance, with the largest accuracy loss shown for the Sr cont reranking approach (see the appendix, Figure 12(a)). 新規性のために推奨順位を付け直す（つまり、Noveltyrの再ランク付けを使用する）と、精度が最も低下する（図3のチャート(a)を参照）。 オフライン評価では、どのようなオフライン評価手法も（ある程度）人気アイテムに偏るため、これは驚くべきことではない。 注目すべきは、3つのケース（Last.fmデータセットのMF、UB、IBアルゴリズム）において、NoveltyrリランキングのRecall性能が2番目に悪く、Sr contリランキングアプローチで最大の精度損失が示されたことである（付録、図12（a）を参照）。

- Rating-based diversity is positively correlated with novelty, since reranking Noveltyr positively influences the rating-based diversity metric Divratings (Figure 3(c)) and vice versa—reranking Divr ratings positively influences the Novelty metric (Figure 3(f)). 評価ベースの多様性は、新規性と正の相関がある。なぜなら、Noveltyrの再ランク付けは、評価ベースの多様性指標Divratingsに正の影響を与え（図3(c)）、逆に、Divrの格付けの再ランク付けは、新規性指標に正の影響を与えるからである（図3(f)）。

- There is a positive correlation between the content-based diversity and the contentbased surprise (Figures 3(b) and 3(d)). This correlation might be explained by the fact that both Divcont and Scont metrics as well as the corresponding reranking approaches Divr cont and Sr cont use the Jaccard item distance function based on the content labels (Equation (8)). 内容ベースの多様性と内容ベースの驚きには正の相関がある（図3(b)と図3(d)）。 この相関関係は、Divcont と Scont の両メトリクス、および対応する再ランク付けアプローチ Divr cont と Sr cont が、コンテンツ・ラベルに基づく Jaccard 項目間距離関数を使用している（式 (8)）。

- A negative correlation is observed among the co-occurrence-based surprise and novelty, since reranking Noveltyr results in Sco−occ values lower than the baseline (Figure 3(e)) and reranking Sr co−occ results in Novelty values slightly lower than the baseline (appendix, Figure 8(f)). This indicates that the Sco−occ metric is scoring the long-tail items lower than the popular items. The finding confirms previous results: the metric is sensitive to item popularity. This is because its core component—pointwise mutual information (Equation (10))—is sensitive to pairs of rare items (see Kaminskas and Bridge [2014] for more discussion). For future use, the metric may need to be modified to avoid such bias. Noveltyrを再ランク付けするとSco-occの値がベースラインより低くなり（図3(e)）、Sr-co-occを再ランク付けするとNoveltyの値がベースラインよりわずかに低くなる（付録、図8(f)）。 これは、Sco-occメトリックがロングテールのアイテムを人気アイテムよりも低く評価していることを示している。 この発見はこれまでの結果を裏付けるもので、この指標はアイテムの人気に敏感である。 これは、その中心的な構成要素であるポイントワイズ相互情報（式(10)）が、レアアイテムのペアに敏感であるためである（詳細な議論については、Kaminskas and Bridge [2014]を参照）。 将来的には、このようなバイアスを避けるために指標を修正する必要があるかもしれない。

- Coverage is positively influenced by the Divr ratings and Noveltyr rerankings (Figure 3(g)). The positive relationship between coverage and novelty is expected, as discussed in Section 5, while the positive influence of rating-based diversity may be linked to its correlation with novelty (see earlier). Interestingly, for the UB and IB kNN algorithms (appendix, Figure 8(g)), the highest Coverage value is achieved when reranking for rating-based diversity Divr ratings (with Noveltyr reranking achieving the second-best value). カバレッジは、Divrの評価とNoveltyrの再ランク付けにプラスの影響を受けている（図3(g)）。 カバレッジと新規性の正の関係は、セクション5で論じたように予想される。一方、レーティングに基づく多様性の正の影響は、新規性との相関に関連している可能性がある（前述参照）。 興味深いことに、UB および IB kNN アルゴリズム（付録、図 8(g)）では、レーティングに基づく多様性 Divr レーティングで再ランク付けした場合に、最も高い Coverage 値が達成される（Noveltyr 再ランク付けでは、2 番目の値が達成される）。

- An exception to the previous finding is the negative influence on Coverage obtained by the Noveltyr reranking with the LTR algorithm on the Last.fm dataset (appendix, Figure 10(g)). This may indicate that the LTR algorithm tends to focus on a particular section of the long-tail item distribution in the Last.fm dataset; however, more detailed analysis of the issue is needed before reaching definite conclusions. 前述の発見に対する例外は、Last.fm データセットで LTR アルゴリズムを使用した Noveltyr リランキングによって得られたカバレッジへの負の影響である（付録、図 10(g)）。 これは、LTRアルゴリズムがLast.fmデータセットのロングテール・アイテム分布の特定のセクションにフォーカスする傾向があることを示しているのかもしれない。しかし、明確な結論に達する前に、この問題についてより詳細な分析が必要である。

As discussed in Section 7.2.4, the evaluation methodology adopted in our experiments may favor popularity-oriented algorithm configurations.
セクション7.2.4で議論したように、我々の実験で採用した評価方法は、人気志向のアルゴリズム構成を好むかもしれない。
This may have an impact on the results obtained by the reranking strategies, as certain algorithms can have more popular items among the reranking candidates.
あるアルゴリズムでは、再ランキング候補の中に人気のある項目がより多く含まれることがあるため、これは再ランキング戦略によって得られる結果に影響を与える可能性がある。
However, we are only interested in comparison of reranking techniques within the same algorithm recommendations.
しかし、我々は、同じアルゴリズム推薦の中でのリランキング技術の比較にしか興味がない。
To conduct a cross-algorithm comparison of reranking strategies, additional popularity bias metrics (such as the average rating of recommended items [Jannach et al.2015b]) could be employed.
リランキング戦略のアルゴリズム横断的な比較を行うために、追加の人気バイアスメトリクス（推奨アイテムの平均評価[Jannach et al.2015b]など）を採用することができる。
We leave this to future work.
これは今後の研究に委ねたい。

### The Impact of Algorithm Parameters. アルゴリズム・パラメータの影響。

We also conducted experiments aimed at investigating the influence of recommendation algorithm parameters on the different performance metrics.
また、推薦アルゴリズムのパラメータが様々なパフォーマンス指標に与える影響を調査することを目的とした実験も行った。
For the UB and IB k-NN algorithms, we computed all the performance metrics while varying the value of the neighborhood size parameter k.
UBとIBのk-NNアルゴリズムについて、近傍サイズパラメータkの値を変化させながら、すべての性能指標を計算した。
For the MF algorithm, we varied the number of factors f.
MFアルゴリズムでは、因子の数fを変化させた。
We did not include the learning-torank (LTR) algorithm in this set of experiments, since the algorithm’s three parameters result in a much larger parameter search space.
LTRアルゴリズムは3つのパラメータを持つため、パラメータ探索空間が非常に大きくなるため、この実験セットにはLTRアルゴリズムを含めなかった。
Due to the large number of experiment runs required for the different parameter values, the results reported in this section were computed with a random sample of 1,000 users on the MovieLens dataset (rather than the full set of 6,040 users).
さまざまなパラメータ値で多数の実験を実行する必要があるため、このセクションで報告する結果は、（6,040人のユーザーのフルセットではなく）MovieLensデータセットの1,000人のユーザーのランダムサンプルで計算した。
Figures 4 and 5 show results for the different parameter values of the MF and UB algorithms, respectively.
図4と図5は、それぞれMFアルゴリズムとUBアルゴリズムのパラメータ値を変えた場合の結果である。

- For the MF algorithm, the results show that increasing the number of factors leads to a loss in accuracy (Recall). However, the beyond-accuracy performance metrics increase for higher f values. For instance, Coverage goes up from approximately 700 items for f = 25 to almost 1, 200 items for f = 250. The increase is also evident for the diversity metrics, Novelty, and content-based surprise Scont. The co-occurrencebased surprise Sco−occ decreases slightly for higher f values, which may be linked to the metric’s sensitivity to item popularity. MFアルゴリズムでは、因子数を増やすと精度（Recall）が低下するという結果が出た。 しかし、精度を超える性能指標は、f値が高いほど高くなる。 例えば、カバレッジは、f=25の場合の約700アイテムから、f=250の場合の約1,200アイテムに増加する。 また、多様性の指標であるノベルティや、コンテンツに基づくサプライズ・スコントも増加している。 共起に基づくサプライズSco-occはf値が高いほどわずかに減少するが、これはアイテムの人気度に対するメトリックの感度と関連している可能性がある。

- For the UB algorithm, the results present an “inverted” picture: higher k values significantly decrease Coverage as well as the diversity metrics, Novelty, and Scont, while Sco−occ values are slightly increasing. The Recall is increasing with the value of k, with the maximum reached at k = 150. Further increase of k does not improve the performance. UBアルゴリズムでは、結果は "反転 "した図を示している：高いk値は、多様性メトリクス、新規性、Scontと同様にカバレッジを大幅に減少させ、Sco-occ値はわずかに増加している。 Recallはkの値とともに増加し、k = 150で最大となる。 kをさらに増やしても性能は向上しない。

- For IB, the trend of decreasing Novelty and Coverage values for larger k values could be observed. However, we do not show this in a figure, as the observed impact of k on the metrics was much less pronounced. For instance, Coverage decreased from approximately 900 items for k = 20 to approximately 800 items for k = 250. IBでは、k値が大きいほど、新規性とカバレッジの値が小さくなる傾向が観察された。 しかし、kがメトリクスに与える影響はそれほど顕著ではなかったため、図には示していない。 例えば、カバレッジはk=20の約900項目からk=250の約800項目に減少した。

We note that the decreasing coverage values for larger neighborhood sizes in both k-NN approaches may seem counterintuitive as a larger user/item neighborhood leads to more items being considered for recommendation.
k-NNアプローチでは、近傍サイズが大きいほどカバレッジ値が小さくなる。
However, this trend can only be measured using the “prediction coverage” metric (i.e., the ratio of items for which prediction can be made, see Section 5.1).
しかし、この傾向は「予測カバレッジ」指標（すなわち、予測が可能な項目の割合、セクション5.1参照）を使ってしか測定できない。
Since we focus on the coverage of items that appear in the top-N recommendation lists, we obtain results that are caused by more popular items appearing among the top recommendations for larger neighborhood sizes.
我々は、トップNの推奨リストに現れるアイテムのカバレッジに焦点を当てているため、近傍サイズが大きいほど、より多くの人気アイテムがトップ推奨リストに現れるという結果が得られる。
An aspect of beyond-accuracy optimization that we did not fully address in our experiments is the influence of recommendation algorithm parameters on the effectiveness of reranking approaches.
精度を超えた最適化において、我々の実験では十分に扱わなかった側面として、推薦アルゴリズムのパラメータがリランキング・アプローチの有効性に与える影響がある。
We observed interesting changes in the Coverage results for the different values of neighborhood size k with the UB algorithm (on MovieLens data).
UBアルゴリズム（MovieLensのデータ）では、近傍サイズkの値の違いにより、カバレッジ結果に興味深い変化が見られました。
When using the best-performing (in terms of Coverage value) reranking Divr ratings with the neighborhood size k = 50, we achieved a 30% higher coverage compared to that of k = 150 (Figure 6, bottom charts).
近傍サイズk = 50で（カバレッジ値の点で）最も優れたリランキングDivrレーティングを使用した場合、k = 150の場合と比較して30%高いカバレッジを達成した（図6、下図）。
While the difference in Recall for the Baseliner rankings of UB with k = 50 and k = 150 is approximately 0.01 (see Figure 6, upper charts), it increases to approximately 0.05 for the Divr ratings rankings.
k=50とk=150のUBのベースライナー・ランキングのRecallの差が約0.01であるのに対し（図6の上図参照）、Divrの格付けランキングでは約0.05に増加する。
Although more analysis is needed to investigate this tradeoff, it is likely that a 0.05 loss in accuracy is a price worth paying for a 30% increase in recommendation coverage.
このトレードオフを調べるにはさらなる分析が必要だが、0.05の精度の低下は、推薦のカバー率を30％高めるために支払う価値のある代償だと思われる。
A detailed analysis of the impact of algorithm parameters on beyond-accuracy objectives is out of the scope of this article.
アルゴリズムのパラメータが精度を超えた目標に与える影響の詳細な分析は、本稿の範囲外である。
We refer interested readers to Jannach et al.[2015b], where a number of state-of-the-art algorithms (with different parameter configurations) are analyzed with respect to various recommendation metrics (including popularity and concentration bias).
Jannachら[2015b]では、様々な推薦指標（人気度や集中度バイアスなど）に関して、（様々なパラメータ構成を持つ）多くの最先端アルゴリズムが分析されている。

# Discussion and Conclustions 討論と結論

In this article, we have reviewed the state-of-the-art research on beyond-accuracy objectives in recommender systems.
本稿では、推薦システムにおける精度を超える目標に関する最先端の研究をレビューした。
We have focused on the four most widely discussed objectives—diversity, serendipity, novelty, and coverage.
私たちは、多様性、セレンディピティ、新規性、網羅性という、最も広く議論されている4つの目的に焦点を当てた。
For each objective, we reviewed the relevant definitions found in the literature and methods for optimizing each objective.
それぞれの目的について、文献にある関連する定義と、それぞれの目的を最適化するための方法を検討した。
Furthermore, we conducted offline experiments aimed at evaluating how the stateof-the-art recommendation algorithms perform in terms of the beyond-accuracy objectives and at studying the relationships between the objectives themselves.
さらに、最新の推薦アルゴリズムが、精度を超えた目的に対してどのようなパフォーマンスを発揮するかを評価し、目的自体の関係を調べることを目的としたオフライン実験を行った。
We have implemented a number of optimization strategies for improving diversity, serendipity, and novelty and investigated how optimizing each objective affects recommendation accuracy and beyond-accuracy metrics.
我々は、多様性、セレンディピティ、新規性を向上させるための最適化戦略を数多く実施し、それぞれの目的を最適化することが、推薦精度や精度を超える指標にどのような影響を与えるかを調査した。
The main goal of this work was to provide a reference point for further research into improving the different beyond-accuracy qualities of recommender systems.
この研究の主な目的は、レコメンダー・システムのさまざまな精度を超える品質を向上させるためのさらなる研究のための参照点を提供することである。
We aimed both to survey the existing literature and to identify important relationships between the different objectives.
我々は、既存の文献を調査し、異なる目的間の重要な関係を特定することを目的とした。
There are still many interesting challenges to address in this research area.
この研究分野には、まだまだ興味深い課題がたくさんある。
We believe the following research directions to be of particular importance:
私たちは、以下の研究の方向性が特に重要であると考えている：

## Evaluation of Beyond-Accuracy Objectives. Beyond-Accuracy Objectives の評価。

As stated in Section 6, offline evaluation is limited when it comes to understanding the real impact of beyond-accuracy objectives on the users’ experience.
セクション6で述べたように、精度を超えた目標がユーザーの経験に与える実際の影響を理解する上で、オフラインでの評価は限界がある。
The gap between offline metrics and the users’ perception of recommendation qualities has been exemplified in a recent study [Said et al.2013], which showed that two algorithms recommending an almost disjoint set of items and obtaining significantly different accuracy scores in offline settings were perceived as equally useful by participants of a user study.
オフラインの評価指標と推薦の質に対するユーザーの認識との間のギャップは、最近の研究[Said et al.2013]で例証されている。この研究では、ほぼ不連続なアイテムのセットを推薦し、オフラインの設定で有意に異なる精度スコアを得た2つのアルゴリズムが、ユーザー研究の参加者によって同じように有用であると認識されたことを示している。
Even when performing user studies, a number of factors such as the domain of recommended items, the type of survey questions, or item familiarity effects can influence the results.
ユーザー調査を実施する場合でも、推奨項目のドメイン、調査質問のタイプ、項目の親しみ効果など、多くの要因が結果に影響を与える可能性がある。
For instance, it has been shown that item familiarity has a strong correlation with user appreciation of recommendations [Jannach et al.2015a].
例えば、アイテムの親しみやすさは、レコメンデーションに対するユーザーの評価と強い相関関係があることが示されている[Jannach et al.2015a]。
Ultimately, no results will be complete without conducting A/B experiments, where the users would be unaware of their involvement in the evaluation.
結局のところ、A/B実験を実施しなければ、ユーザーが評価に関与していることに気づかないような結果は得られない。

## Adaptivity of Beyond-Accuracy Objectives. Beyond-Accuracy Objectives の適応性.

Another important challenge in beyondaccuracy research is developing optimization solutions that are adapted to specific recommendation domains, since different items may require different levels of recommendation diversity or novelty.
beyondaccuracy研究におけるもう一つの重要な課題は、特定の推薦ドメインに適応した最適化ソリューションを開発することである。
For instance, the same novelty-enhancing algorithm may not suit both a movie recommender (where obvious recommendations are not desired) and a music streaming service (where well-known items may be among the desirable recommendations) [Kapoor et al.2015].
例えば、同じ新規性強調アルゴリズムは、映画レコメンダー（明らかなレコメンデーションが望まれていない）と音楽ストリーミングサービス（よく知られたアイテムが望ましいレコメンデーションの中にあるかもしれない）の両方に合わないかもしれない[Kapoor et al.2015]。
An equally important challenge is to tailor the beyond-accuracy optimization to the needs or preferences of individual users.
同様に重要な課題は、精度を超えた最適化を個々のユーザーのニーズや好みに合わせて調整することである。
Solutions that adapt to users’ needs or preferences for diversity, serendipity, or novelty may do so implicitly, for example, based on the users’ rating behavior [Shi et al.2012] or the type of consumed items [Oh et al.2011; Kapoor et al.2015].
多様性、セレンディピティ、新規性といったユーザーのニーズや嗜好に適応するソリューションは、例えば、ユーザーの評価行動[Shi et al.2012]や消費アイテムのタイプ[Oh et al.2011; Kapoor et al.2015]に基づいて、暗黙的にそうすることができる。
Alternatively, users may be given explicit control over their recommendations, for example, choosing to see more (or fewer) popular items [Harper et al.2015].
あるいは、例えば、人気のあるアイテムをより多く（または少なく）見ることを選択するなど、ユーザーにレコメンデーションを明示的に制御させることもできる[Harper et al.2015]。
Additionally, the solutions may be improved by ensuring transparency of beyondaccuracy recommendations.
さらに、精度を超えた推奨事項の透明性を確保することで、解決策は改善されるかもしれない。
For instance, it has been argued that user acceptance of diversification may suffer if no explanation of the diversity level is provided [Castagnos et al.2013].
例えば、多様性のレベルの説明が提供されない場合、多様化に対するユーザーの受容が損なわれる可能性があると論じられている[Castagnos et al.2013]。