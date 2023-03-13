## link リンク

- https://grouplens.org/site-content/uploads/evaluating-TOIS-20041.pdf https

## title タイトルです。

Evaluating Collaborative Filtering Recommender Systems.
協調フィルタリング・レコメンダーシステムの評価。

## abstract abstract.

Recommender systems have been evaluated in many, often incomparable, ways.
レコメンダーシステムは、多くの、しばしば比較できない方法で評価されています。
In this article, we review the key decisions in evaluating collaborative filtering recommender systems: the user tasks being evaluated, the types of analysis and datasets being used, the ways in which prediction quality is measured, the evaluation of prediction attributes other than quality, and the user-based evaluation of the system as a whole.
本稿では、協調フィルタリング推薦システムの評価における重要な決定事項である、評価対象となるユーザータスク、使用する分析・データセットの種類、予測品質の測定方法、品質以外の予測属性の評価、システム全体に対するユーザーベースの評価について概説します。
In addition to reviewing the evaluation strategies used by prior researchers, we present empirical results from the analysis of various accuracy metrics on one content domain where all the tested metrics collapsed roughly into three equivalence classes.
先行研究者が用いた評価戦略のレビューに加え、テストしたすべてのメトリクスが3つの等価クラスに大別されるあるコンテンツドメインについて、様々な精度メトリクスを分析した実証結果を紹介します。
Metrics within each equivalency class were strongly correlated, while metrics from different equivalency classes were uncorrelated..
各等価クラス内のメトリクスは強い相関があり、異なる等価クラスのメトリクスは無相関であった。

# Introduction 紹介します。

Recommender systems use the opinions of a community of users to help individuals in that community more effectively identify content of interest from a potentially overwhelming set of choices [Resnick and Varian 1997].
レコメンダーシステムは、ユーザーのコミュニティの意見を利用して、そのコミュニティ内の個人が、潜在的に圧倒的な選択肢の中から興味のあるコンテンツをより効果的に特定できるようにするものである [Resnick and Varian 1997] 。
One of the most successful technologies for recommender systems, called collaborative filtering, has been developed and improved over the past decade to the point where a wide variety of algorithms exist for generating recommendations.
推薦システムの最も成功した技術の一つである協調フィルタリングは、過去10年間に開発・改良され、推薦文を生成するための多様なアルゴリズムが存在するまでになりました。
Each algorithmic approach has adherents who claim it to be superior for some purpose.
各アルゴリズムのアプローチには、何らかの目的に対して優れていると主張する信奉者がいます。
Clearly identifying the best algorithm for a given purpose has proven challenging, in part because researchers disagree on which attributes should be measured, and on which metrics should be used for each attribute.
ある目的に対して最適なアルゴリズムを明確に特定することは困難であることが証明されていますが、その理由の一つは、どの属性を測定すべきか、また各属性に対してどのメトリクスを使用すべきかについて研究者の間で意見が分かれているためです。
Researchers who survey the literature will find over a dozen quantitative metrics and additional qualitative evaluation techniques..
研究者が文献を調査すると、十数種類の定量的な評価指標と、さらに定性的な評価技法が見つかります。

Evaluating recommender systems and their algorithms is inherently difficult for several reasons.
レコメンダーシステムとそのアルゴリズムの評価は、いくつかの理由から本質的に困難である。
First, different algorithms may be better or worse on different data sets.
まず、異なるデータセットでは、異なるアルゴリズムが良くも悪くもなる可能性があります。
Many collaborative filtering algorithms have been designed specifically for data sets where there are many more users than items (e.g., the MovieLens data set has 65,000 users and 5,000 movies).
多くの協調フィルタリングアルゴリズムは、アイテムよりも多くのユーザーが存在するデータセット（例えば、MovieLensデータセットは、65,000人のユーザーと5,000本の映画を持っています）専用に設計されています。
Such algorithms may be entirely inappropriate in a domain where there are many more items than users (e.g., a research paper recommender with thousands of users but tens or hundreds of thousands of articles to recommend).
このようなアルゴリズムは、ユーザーよりもアイテムの数が多いドメイン（例えば、ユーザーは数千人だが、推薦する論文は数万から数十万件ある研究論文推薦装置）では全く不適切かもしれません。
Similar differences exist for ratings density, ratings scale, and other properties of data sets..
評価密度や評価スケールなど、データセットの特性にも同様の違いがあります。

The second reason that evaluation is difficult is that the goals for which an evaluation is performed may differ.
評価が難しい理由の2つ目は、評価を行う目標が異なる場合があることです。
Much early evaluation work focused specifically on the “accuracy” of collaborative filtering algorithms in “predicting” withheld ratings.
初期の評価作業の多くは、特に、保留された評価を「予測」する協調フィルタリングアルゴリズムの「精度」に焦点を当てていました。
Even early researchers recognized, however, that when recommenders are used to support decisions, it can be more valuable to measure how often the system leads its users to wrong choices.
しかし、初期の研究者たちも、レコメンダーが意思決定を支援するために使われる場合、システムがユーザーを間違った選択に導く頻度を測定することの方が価値があることを認識していた。
Shardanand and Maes [1995] measured “reversals”—large errors between the predicted and actual rating; we have used the signal-processing measure of the Receiver Operating Characteristic curve [Swets 1963] to measure a recommender’s potential as a filter [Konstan et al.
Shardanand and Maes [1995]は、予測された評価と実際の評価の間に大きな誤差がある「逆転」を測定しました。私たちは、信号処理の指標であるReceiver Operating Characteristic curve [Swets 1963] を使って、フィルタとしての推薦者の可能性を測定しました [Konstan et al.
1997].
1997].
Other work has speculated that there are properties different from accuracy that have a larger effect on user satisfaction and performance.
他の研究では、ユーザーの満足度や性能に大きな影響を与える、正確さとは異なる特性があると推測されています。
A range of research and systems have looked at measures including the degree to which the recommendations cover the entire set of items [Mobasher et al.
様々な研究やシステムで、推奨が項目全体をカバーする度合いなどの尺度が検討されている [Mobasher et al.
2001], the degree to which recommendations made are nonobvious [McNee et al.
2001]、推奨されたものが自明でない度合い[McNee et al.
2002], and the ability of recommenders to explain their recommendations to users [Sinha and Swearingen 2002].
2002]、推薦者が推薦内容をユーザーに説明する能力[Sinha and Swearingen 2002]などである。
A few researchers have argued that these issues are all details, and that the bottom-line measure of recommender system success should be user satisfaction.
一部の研究者は、これらの問題はすべて細部であり、推薦システムの成功の最重要指標はユーザー満足度であるべきだと主張しています。
Commercial systems measure user satisfaction by the number of products purchased (and not returned!), while noncommercial systems may just ask users how satisfied they are..
商業システムでは、ユーザーの満足度を購入した商品の数（返品されない数！）で測りますが、非商業システムでは、ユーザーに満足度を聞くだけでいいかもしれません。

Finally, there is a significant challenge in deciding what combination of measures to use in comparative evaluation.
最後に、比較評価において、どのような尺度の組み合わせを用いるかを決定することには、大きな課題がある。
We have noticed a trend recently—many researchers find that their newest algorithms yield a mean absolute error of 0.73 (on a five-point rating scale) on movie rating datasets.
多くの研究者が、映画の評価データセットにおいて、最新のアルゴリズムによる平均絶対誤差が0.73（5段階評価）であることに最近気がついたのです。
Though the new algorithms often appear to do better than the older algorithms they are compared to, we find that when each algorithm is tuned to its optimum, they all produce similar measures of quality.
新しいアルゴリズムは、比較対象となる古いアルゴリズムよりも優れているように見えることが多いのですが、各アルゴリズムを最適にチューニングすると、どれも同じような品質尺度になることがわかります。
We—and others—have speculated that we may be reaching some “magic barrier” where natural variability may prevent us from getting much more accurate.
私たちや他の人々は、自然変動によって精度を上げることができない "魔法の壁 "に到達しているのではないかと推測しています。
In support of this, Hill et al.
これを裏付けるように、Hill et al.
[1995] have shown that users provide inconsistent ratings when asked to rate the same movie at different times.
[1995]は、同じ映画を異なる時間に評価するよう求められたとき、ユーザーが一貫性のない評価をすることを示しました。
They suggest that an algorithm cannot be more accurate than the variance in a user’s ratings for the same item..
彼らは、アルゴリズムが、同じアイテムに対するユーザーの評価のばらつきよりも正確であることはあり得ないと示唆している。

Even when accuracy differences are measurable, they are usually tiny.
精度の差が測定可能であっても、通常は微小なものです。
On a five-point rating scale, are users sensitive to a change in mean absolute error of 0.01? These observations suggest that algorithmic improvements in collaborative filtering systems may come from different directions than just continued improvements in mean absolute error.
5段階評価で、平均絶対誤差が0.01の変化に対して、ユーザーは敏感に反応するのだろうか？これらの観察から、協調フィルタリングシステムのアルゴリズムの改良は、平均絶対誤差の継続的な改善とは異なる方向からもたらされる可能性があることが示唆される。
Perhaps the best algorithms should be measured in accordance with how well they can communicate their reasoning to users, or with how little data they can yield accurate recommendations.
おそらく、最高のアルゴリズムは、どれだけユーザーに自分の推論を伝えることができるか、あるいはどれだけ少ないデータで正確な推奨を得られるかによって評価されるべきなのでしょう。
If this is true, new metrics will be needed to evaluate these new algorithms..
もしこれが本当なら、これらの新しいアルゴリズムを評価するための新しい指標が必要になる。

This article presents six specific contributions towards evaluation of recommender systems..
本稿では、レコメンダーシステムの評価に関する6つの具体的な貢献を紹介する。

(1) We introduce a set of recommender tasks that categorize the user goals for a particular recommender system..
(1)特定のレコメンダーシステムに対するユーザーの目標を分類したレコメンダータスクのセットを紹介する。

(2) We discuss the selection of appropriate datasets for evaluation.
(2) 評価に適したデータセットの選択について説明します。
We explore when evaluation can be completed off-line using existing datasets and when it requires on-line experimentation.
既存のデータセットを使ってオフラインで評価できる場合と、オンラインでの実験が必要な場合について検討します。
We briefly discuss synthetic data sets and more extensively review the properties of datasets that should be considered in selecting them for evaluation..
合成データセットについて簡単に説明し、評価のためにデータセットを選択する際に考慮すべきデータセットの特性についてより広範に検討する。

(3) We survey evaluation metrics that have been used to evaluation recommender systems in the past, conceptually analyzing their strengths and weaknesses..
(3) 過去に推薦システムの評価に用いられた評価指標を調査し、その長所と短所を概念的に分析する。

(4) We report on experimental results comparing the outcomes of a set of different accuracy evaluation metrics on one data set.
(4) 1つのデータセットについて、異なる精度評価指標の結果を比較した実験結果を報告する。
We show that the metrics collapse roughly into three equivalence classes..
その結果、このメトリクスは3つの同値クラスに大別されることを示す。

(5) By evaluating a wide set of metrics on a dataset, we show that for some datasets, while many different metrics are strongly correlated, there are classes of metrics that are uncorrelated.
(5) データセット上で幅広いメトリクスを評価することで、あるデータセットでは、多くの異なるメトリクスが強い相関を持つ一方で、無相関のメトリクスクラスが存在することを示すことができます。
(6) We review a wide range of nonaccuracy metrics, including measures of the degree to which recommendations cover the set of items, the novelty and serendipity of recommendations, and user satisfaction and behavior in the recommender system..
(6)推奨がアイテムセットをカバーする度合い、推奨の新規性・セレンディピティ、推奨システムにおけるユーザーの満足度・行動などの指標を含む、幅広い非正確性指標を検討した結果。

Throughout our discussion, we separate out our review of what has been done before in the literature from the introduction of new tasks and methods..
この議論では、これまでの文献のレビューと、新しいタスクや手法の紹介を分けて考えています。

We expect that the primary audience of this article will be collaborative filtering researchers who are looking to evaluate new algorithms against previous research and collaborative filtering practitioners who are evaluating algorithms before deploying them in recommender systems..
この記事の主な読者は、新しいアルゴリズムを過去の研究に対して評価しようとする協調フィルタリング研究者や、推薦システムに導入する前にアルゴリズムを評価する協調フィルタリング実務者であると予想されます。

There are certain aspects of recommender systems that we have specifically left out of the scope of this paper.
レコメンダーシステムには、特に本稿の範囲から外している部分がある。
In particular, we have decided to avoid the large area of marketing-inspired evaluation.
特に、マーケティングを意識した評価という大きな領域は避けることにしました。
There is extensive work on evaluating marketing campaigns based on such measures as offer acceptance and sales lift [Rogers 2001].
オファーアクセプタンスやセールスリフトなどの指標に基づいてマーケティングキャンペーンを評価する研究が盛んである [Rogers 2001]。
While recommenders are widely used in this area, we cannot add much to existing coverage of this topic.
レコメンダーはこの分野で広く使われていますが、このトピックに関する既存のカバーに多くを加えることはできません。
We also do not address general usability evaluation of the interfaces.
また、インターフェースの一般的な使用感評価については触れていません。
That topic is well covered in the research and practitioner literature (e.g., Helander [1988] and Nielsen [1994]) We have chosen not to discuss computation performance of recommender algorithms.
このトピックは、研究や実務家の文献で十分にカバーされています（例えば、Helander [1988] や Nielsen [1994]）。 我々は、推薦アルゴリズムの計算性能について議論しないことにしました。
Such performance is certainly important, and in the future we expect there to be work on the quality of time-limited and memory-limited recommendations.
このような性能は確かに重要であり、将来的には時間制限やメモリ制限のあるレコメンデーションの品質に関する研究が行われることを期待します。
This area is just emerging, however (see for example Miller et al.’s recent work on recommendation on handheld devices [Miller et al.
しかし、この分野はまだ始まったばかりである（例えば、Millerらのハンドヘルドデバイスでの推薦に関する最近の研究 [Miller et al.を参照）。
2003]), and there is not yet enough research to survey and synthesize.
2003年]）、調査・統合するほどの研究はまだない。
Finally, we do not address the emerging question of the robustness and transparency of recommender algorithms.
最後に、レコメンダーアルゴリズムの堅牢性と透明性という新たな問題には取り組んでいません。
We recognize that recommender system robustness to manipulation by attacks (and transparency that discloses manipulation by system operators) is important, but substantially more work needs to occur in this area before there will be accepted metrics for evaluating such robustness and transparency.
我々は、攻撃による操作に対する推薦システムの堅牢性（およびシステムオペレータによる操作を開示する透明性）が重要であると認識しているが、そのような堅牢性と透明性を評価するための受け入れ可能なメトリックが存在する前に、この分野で大幅に多くの作業が行われる必要がある。
The remainder of the article is arranged as follows:.
残りの部分は、次のように整理されています。

- —Section 2. We identify the key user tasks from which evaluation methods have been determined and suggest new tasks that have not been evaluated extensively. 評価方法が決定された主要なユーザータスクを特定し、広範囲に評価されていない新しいタスクを提案します。

- —Section 3. A discussion regarding the factors that can affect selection of a data set on which to perform evaluation. 評価を行うデータセットの選択に影響を与える要因について説明します。

- —Section 4. An investigation of metrics that have been used in evaluating the accuracy of collaborative filtering predictions and recommendations. Accuracy has been by far the most commonly published evaluation method for collaborative filtering systems. This section also includes the results from an empirical study of the correlations between metrics. 協調フィルタリングの予測や推薦の精度を評価する際に使用されてきたメトリクスの調査。 協調フィルタリングシステムの評価方法として、これまで最も多く発表されてきたのが「精度」です。 また、メトリクス間の相関性に関する実証研究の結果も掲載しています。

- —Section 5. A discussion of metrics that evaluate dimensions other than accuracy. In addition to covering the dimensions and methods that have been used in the literature, we introduce new dimensions on which we believe evaluation should be done. 精度以外の次元を評価するメトリクスについての考察。 これまでの文献で用いられてきた次元と方法を網羅することに加え、評価を行うべきと考える新たな次元を紹介する。

- —Section 6. Final conclusions, including a list of areas were we feel future work is particularly warranted. 最終的な結論は、今後の研究が特に必要だと思われる分野のリストを含む。

Sections 2–5 are ordered to discuss the steps of evaluation in roughly the order that we would expect an evaluator to take.
第2節から第5節は、評価のステップを、評価者に期待するのとほぼ同じ順序で論じています。
Thus, Section 2 describes the selection of appropriate user tasks, Section 3 discusses the selection of a dataset, and Sections 4 and 5 discuss the alternative metrics that may be applied to the dataset chosen.
そこで、第2節では適切なユーザタスクの選択について、第3節ではデータセットの選択について、第4節と第5節では選択したデータセットに適用可能な代替メトリクスについて説明する。
We begin with the discussion of user tasks—the user task sets the entire context for evaluation..
まず、ユーザータスクについて説明します。ユーザータスクは、評価のためのすべてのコンテキストを設定します。

C:\Users\Masat\AppData\Local\Microsoft\WindowsApps.
C:¥Users¥Masat¥AppData¥Local¥Microsoft¥WindowsApps.

# User Tasks for Recommender systems 推薦システムのためのユーザーのタスク」。

To properly evaluate a recommender system, it is important to understand the goals and tasks for which it is being used.
レコメンダーシステムを正しく評価するためには、そのシステムが使用される目的とタスクを理解することが重要です。
In this article, we focus on end-user goals and tasks (as opposed to goals of marketers and other system stakeholders).
今回は、（マーケターなどシステム関係者の目標ではなく）エンドユーザーの目標やタスクに焦点を当てます。
We derive these tasks from the research literature and from deployed systems.
これらのタスクは、研究文献や導入されたシステムから導き出されます。
For each task, we discuss its implications for evaluation.
各タスクについて、その評価への示唆を述べています。
While the tasks we’ve identified are important ones, based on our experience in recommender systems research and from our review of published research, we recognize that the list is necessarily incomplete.
私たちが特定したタスクは重要なものですが、レコメンダー・システム研究の経験や公表された研究のレビューに基づくと、このリストは必ずしも不完全なものであることが認識されます。
As researchers and developers move into new recommendation domains, we expect they will find it useful to supplement this list and/or modify these tasks with domain-specific ones.
研究者や開発者が新たなレコメンデーション領域を開拓する際には、このリストを補足することが有用であると考えます。
Our goal is primarily to identify domain-independent task descriptions to help distinguish among different evaluation measures..
私たちの目標は、主に、異なる評価指標を区別するのに役立つ、ドメインに依存しないタスク記述を特定することです。

We have identified two user tasks that have been discussed at length within the collaborative filtering literature:.
協調フィルタリングの文献で長く議論されてきた、次の2つのユーザータスクを特定しました。

- Annotation in Context. アノテーション・イン・コンテキスト...

- The original recommendation scenario was filtering through structured discussion postings to decide which ones were worth reading. Tapestry [Goldberg et al. 1992] and GroupLens [Resnick et al. 1994] both applied this to already structured message databases. This task required retaining the order and context of messages, and accordingly used predictions to annotate messages in context. In some cases the “worst” messages were filtered out. This same scenario, which uses a recommender in an existing context, has also been used by web recommenders that overlay prediction information on top of existing links [Wexelblat and Maes 1999]. Users use the displayed predictions to decide which messages to read (or which links to follow), and therefore the most important factor to evaluate is how successfully the predictions help users distinguish between desired and undesired content. A major factor is the whether the recommender can generate predictions for the items that the user is viewing. 当初の推奨シナリオは、構造化されたディスカッションの投稿をフィルタリングして、どれが読むに値するかを決めるというものでした。 タペストリー［Goldberg et al. 1992]とGroupLens [Resnick et al. 1994]はいずれも、すでに構造化されたメッセージデータベースにこれを適用したものである。 このタスクでは、メッセージの順序と文脈を保持する必要があるため、予測を使ってメッセージの文脈に注釈を付けています。 場合によっては、"最悪 "のメッセージがフィルタリングされることもありました。 これと同じシナリオで、既存の文脈の中でレコメンダーを使用することは、既存のリンクの上に予測情報を重ねるウェブレコメンダーでも使われている[Wexelblat and Maes 1999]。 ユーザーは表示された予測をもとに、どのメッセージを読むか（あるいはどのリンクをたどるかを決める）ので、予測によってユーザーが望ましいコンテンツとそうでないコンテンツをどれだけうまく区別できるかが最も重要な評価要素になります。 レコメンダーは、ユーザーが見ているアイテムの予測値を生成できるかどうかが大きなポイントになります。

- Find Good Items. 良いものを探す...

- Soon after Tapestry and GroupLens, several systems were developed with a more direct focus on actual recommendation. Ringo [Shardanand and Maes 1995] and the Bellcore Video Recommender [Hill et al. 1995] both provided interfaces that would suggest specific items to their users, providing users with a ranked list of the recommended items, along with predictions for how much the users would like them. This is the core recommendation task and it recurs in a wide variety of research and commercial systems. In many commercial systems, the “best bet” recommendations are shown, but the predicted rating values are not. TapestryやGroupLensの後すぐに、実際のレコメンデーションにもっと直接的に焦点を当てたシステムがいくつか開発されました。 Ringo [Shardanand and Maes 1995]とBellcore Video Recommender [Hill et al. 1995]では、ユーザーに特定のアイテムを提案するインターフェースを提供し、ユーザーに推奨アイテムのランク付けされたリストと、ユーザーがそのアイテムをどの程度気に入るかの予測を提供しました。 これは推薦の核となるタスクであり、さまざまな研究・商業システムで繰り返されている。 多くの市販システムでは、「ベストベット」の推奨値は表示されるが、予測される評価値は表示されない。

- While these two tasks can be identified quite generally across many different domains, there are likely to be many specializations of the above tasks within each domain. We introduce some of the characteristics of domains that influence those specializations in Section 3.3. この2つのタスクは、多くの異なるドメインで非常に一般的に識別することができますが、各ドメインの中で上記のタスクの多くの特殊化があると思われます。 3.3節では、それらの特殊化に影響を与えるドメインの特徴を紹介する。

- While the Annotation in Context and the Find Good Items are overwhelmingly the most commonly evaluated tasks in the literature, there are other important generic tasks that are not well described in the research literature. Below we describe several other user tasks that we have encountered in our interviews with users and our discussions with recommender system designers. We mention these tasks because we believe that they should be evaluated, but because they have not been addressed in the recommender systems literature, we do not discuss them further. Annotation in ContextとFind Good Itemsは圧倒的に文献で評価されているタスクですが、他にも研究文献にあまり書かれていない重要な汎用タスクがあります。 以下では、ユーザーへのインタビューやレコメンダーシステム設計者とのディスカッションで遭遇した、その他のユーザータスクについて説明します。 これらのタスクは評価されるべきであると考えるからであるが、推薦システムの文献では扱われていないため、これ以上の議論は行わないこととする。

- Find All Good Items. 良いものを探す...

- Most recommender tasks focus on finding some good items. This is not surprising; the problem that led to recommender systems was one of overload, and most users seem willing to live with overlooking some good items in order to screen out many bad ones. Our discussions with firms in the legal databases industry, however, led in the opposite direction. Lawyers searching for precedents feel it is very important not to overlook a single possible case. Indeed, they are willing to invest large amounts of time (and their client’s money) searching for that case. To use recommenders in their practice, they first need to be assured that the false negative rate can be made sufficiently low. As with annotation in context, coverage becomes particularly important in this task. レコメンダーのタスクのほとんどは、いくつかの良いアイテムを見つけることに焦点を当てています。 レコメンダーシステムが誕生した背景には、過負荷という問題があり、多くのユーザーは、多くの悪いものを除外するために、いくつかの良いものを見落としても構わないと考えているようです。 しかし、リーガルデータベース業界の企業との話し合いは、逆の方向に進みました。 判例を探す弁護士は、一つの可能性も見逃さないことが非常に重要だと考えています。 実際、彼らはそのケースを探すために、大量の時間（とクライアントのお金）を費やすことも厭わない。 レコメンダーを実務で使うには、まず、偽陰性率を十分に低くできることが保証される必要がある。 文脈に沿ったアノテーションと同様に、この課題ではカバレッジが特に重要になります。

- Recommend Sequence. レコメンドシーケンス.

- We first noticed this task when using the personalized radio web site Launch (launch.yahoo.com) which streams music based on a variety of recommender algorithms. Launch has several interesting factors, including the desirability of recommending “already rated” items, though not too often. What intrigued us, though, is the challenge of moving from recommending one song at a time to recommending a sequence that is pleasing as a whole. This same task can apply to recommending research papers to learn about a field (read this introduction, then that survey, ... ). While data mining research has explored product purchase timing and sequences, we are not aware of any recommender applications or research that directly address this task. 私たちがこの課題に気づいたのは、さまざまな推薦アルゴリズムに基づいて音楽を流すパーソナライズド・ラジオ・ウェブサイト「Launch」（launch.yahoo.com）を使ったときでした。 Launchには、あまり頻繁ではないものの、「すでに評価されている」ものを勧めることが望ましいなど、興味深い要素がいくつかあります。 しかし、私たちが興味を持ったのは、1曲ずつレコメンドするのではなく、全体として心地よいシークエンスをレコメンドするというチャレンジです。 この作業は、ある分野について学ぶために研究論文を推薦すること（この紹介文を読み、次にその調査結果を読む、...）にも当てはまります。 ). データマイニングの研究では、商品の購入タイミングや順序について研究されているが、この課題に直接取り組むレコメンダーアプリケーションや研究は知られていない。

- Just Browsing. Recommenders are usually evaluated based on how well they help the user make a consumption decision. In talking with users of our MovieLens system, of Amazon.com, and of several other sites, we discovered that many of them use the site even when they have no purchase imminent. They find it pleasant to browse. Whether one models this activity as learning or simply as entertainment, it seems that a substantial use of recommenders is simply using them without an ulterior motive. For those cases, the accuracy of algorithms may be less important than the interface, the ease of use, and the level and nature of information provided. ジャストブラウジングです。 レコメンダーは通常、ユーザーが消費を決定する際にどれだけ役立つかを基準に評価されます。 当社のMovieLensシステム、Amazon.com、その他いくつかのサイトの利用者に話を聞くと、購入の目処が立っていなくてもサイトを利用している人が多いことがわかりました。 閲覧することに快感を覚えるのです。 この活動を学習とするか、単なる娯楽とするかは別として、レコメンダーの実質的な使い方は、下心なく使うことだと思われます。 そのような場合、アルゴリズムの正確さは、インターフェースや使いやすさ、提供される情報のレベルや性質よりも重要ではないかもしれません。

- Find Credible Recommender. 信頼できるレコメンダーを見つける。

- This is another task gleaned from discussions with users. It is not surprising that users do not automatically trust a recommender. Many of them “play around” for a while to see if the recommender matches their tastes well. We’ve heard many complaints from users who are looking up their favorite (or least favorite) movies on MovieLens—they don’t do this to learn about the movie, but to check up on us. Some users even go further. Especially on commercial sites, they try changing their profiles to see how the recommended items change. They explore the recommendations to try to find any hints of bias. A recommender optimized to produce “useful” recommendations (e.g., recommendations for items that the user does not already know about) may fail to appear trustworthy because it does not recommend movies the user is sure to enjoy but probably already knows about. We are not aware of any research on how to make a recommender appear credible, though there is more general research on making websites evoke trust [Bailey et al. 2001]. これも、ユーザーとのディスカッションから得た課題です。 ユーザーがレコメンダーを自動的に信頼しないのは当然である。 レコメンダーが自分の好みにうまくマッチするかどうか、しばらく「遊んでみる」方も多いようです。 MovieLensで自分の好きな（あるいは嫌いな）映画を調べているユーザーから、「映画のことを知るためではなく、私たちのことを調べるためにやっている」という不満をよく耳にします。 さらに踏み込んだユーザーもいます。 特に商用サイトでは、プロフィールを変えてみて、おすすめアイテムがどう変わるか確認するそうです。 彼らは、勧告を探って、バイアスのヒントを見つけようとします。 有用な」レコメンデーション（例えば、ユーザーがまだ知らないアイテムのレコメンデーション）を生成するように最適化されたレコメンダーは、ユーザーが確実に楽しめるがおそらく既に知っている映画をレコメンデーションしないため、信頼できるように見えないことがある。 ウェブサイトが信頼を呼び起こすための一般的な研究はありますが、レコメンダーを信頼できるように見せる方法についての研究は知りません [Bailey et al. 2001]..

- Most evaluations of recommender systems focus on the recommendations; however if users don’t rate items, then collaborative filtering recommender systems can’t provide recommendations. Thus, evaluating if and why users would contribute ratings may be important to communicate that a recommender system is likely to be successful. We will briefly introduce several different rating tasks. 推薦システムの評価の多くは、推薦に重点を置いています。しかし、ユーザーがアイテムを評価しなければ、協調フィルタリング推薦システムは推薦を提供することができません。 このように、ユーザーが評価を投稿するかどうか、またその理由を評価することは、レコメンダーシステムが成功する可能性があることを伝えるために重要であると考えられます。 ここでは、いくつかの異なるレーティングタスクを簡単に紹介します。

- Improve Profile. プロファイルの改善...

- the rating task that most recommender systems have assumed. Users contribute ratings because they believe that they are improving their profile and thus improving the quality of the recommendations that they will receive. 多くのレコメンダーシステムが想定しているレーティングタスク。 ユーザーは、自分のプロフィールを向上させることで、自分が受け取るレコメンデーションの質を向上させることができると考え、評価を投稿します。

- Express Self. エクスプレス・セルフ...

- Some users may not care about the recommendations—what is important to them is that they be allowed to contribute their ratings. Many users simply want a forum for expressing their opinions. We conducted interviews with “power users” of MovieLens that had rated over 1000 movies (some over 2000 movies). What we learned was that these users were not rating to improve their recommendations. They were rating because it felt good. We particularly see this effect on sites like Amazon.com, where users can post reviews (ratings) of items sold by Amazon. For users with this task, issues may include the level of anonymity (which can be good or bad, depending on the user), the feeling of contribution, and the ease of making the contribution. While recommender algorithms themselves may not evoke self-expression, encouraging self-expression may provide more data which can improve the quality of recommendations. ユーザーによっては、レコメンデーションはどうでもよくて、自分の評価を投稿できるようにすることが重要なのです。 多くのユーザーは、単に自分の意見を表明する場を求めているに過ぎません。 1000本以上（中には2000本以上）の映画を評価したMovieLensの "パワーユーザー "にインタビューを実施しました。 そこでわかったのは、これらのユーザーはレコメンドを改善するための評価をしていない、ということでした。 気持ちいいから評価されていたのです。 特に、Amazon.comのような、Amazonが販売する商品に対してユーザーがレビュー（評価）を投稿できるサイトでは、この効果が顕著に現れています。 この課題を持つユーザーにとって、匿名性の高さ（これはユーザーによって良くも悪くもなる）、貢献感、貢献のしやすさなどが問題になることがあります。 レコメンダーアルゴリズム自体は自己表現を喚起するものではありませんが、自己表現を促すことで、レコメンデーションの質を向上させることができるデータが増える可能性があります。

- Help Others. Some users are happy to contribute ratings in recommender systems because they believe that the community benefits from their contribution. In many cases, they are also entering ratings in order to express themselves (see previous task). However, the two do not always go together. 他人を助ける。 推薦システムで評価を提供することで、コミュニティが恩恵を受けると信じて喜んでいるユーザーもいます。 また、自分を表現するために視聴率に応募しているケースも多いようです（前回の課題参照）。 しかし、この2つは必ずしも相性がいいとは限りません。

- Influence Others. 他者に影響を与える...

- An unfortunate fact that we and other implementers of web-based recommender systems have encountered is that there are users of recommender systems whose goal is to explicitly influence others into viewing or purchasing particular items. For example, advocates of particular movie genres (or movie studios) will frequently rate movies high on the MovieLens web site right before the movie is released to try and push others to go and see the movie. This task is particularly interesting, because we may want to evaluate how well the system prevents this task. 私たちやウェブベースのレコメンダーシステムの実装者が遭遇した残念な事実は、レコメンダーシステムの利用者の中には、特定のアイテムを見たり購入したりするように他者に明示的に影響を与えることを目的とする人がいることです。 例えば、特定の映画ジャンルの支持者（または映画会社）は、映画が公開される直前にMovieLensのウェブサイトで映画を高く評価し、他の人にその映画を観に行くよう働きかけることがよくあります。 特にこのタスクは、システムがどの程度防げるかを評価したい場合もありますから、興味深いですね。

- While we have briefly mentioned tasks involved in contributing ratings, we will not discuss them in depth in this paper, and rather focus on the tasks related to recommendation. これまで、評価の投稿に関わるタスクについて簡単に触れてきたが、本稿では深くは触れず、推薦に関わるタスクに焦点を当てることにする。

- We must once again say that the list of tasks in this section is not comprehensive. Rather, we have used our experience in the field to filter out the task categories that (a) have been most significant in the previously published work, and (b) that we feel are significant, but have not been considered sufficiently. このセクションのタスクのリストは、包括的なものではないことを、もう一度言っておかなければなりません。 むしろ、これまでの経験をもとに、(a)既発表の研究で最も重要であったもの、(b)重要であるが十分に検討されていないと思われるタスクカテゴリーをフィルタリングしています。

- In the field of Human-Computer Interaction, it has been strongly argued that the evaluation process should begin with an understanding of the user tasks that the system will serve. When we evaluate recommender systems from the perspective of benefit to the user, we should also start by identifying the most important task for which the recommender will be used. In this section, we have provided descriptions of the most significant tasks that have been identified. Evaluators should consider carefully which of the tasks described may be appropriate for their environment. ヒューマン・コンピュータ・インタラクションの分野では、システムが果たすべきユーザーのタスクを理解することから評価プロセスを始めるべきであると強く主張されてきた。 ユーザーにとってのメリットという観点からレコメンダーシステムを評価する場合、レコメンダーが使用される最も重要なタスクを特定することから始めることも必要です。 このセクションでは、特定された最も重要なタスクについての説明を行いました。 評価者は、記載されているタスクのうち、どのタスクが自分の環境に適しているかを慎重に検討する必要があります。

Once the proper tasks have been identified, the evaluator must select a dataset to which evaluation methods can be applied, a process that will most likely be constrained by the user tasks identified..
適切なタスクが特定された後、評価者は評価手法を適用できるデータセットを選択しなければなりませんが、このプロセスは、特定されたユーザータスクによって制約を受ける可能性が高いです。

# Selecting Data sets for Evaluation 評価用のデータセットを選択する。

Several key decisions regarding data sets underlie successful evaluation of a recommender system algorithm.
レコメンダーシステムアルゴリズムの評価を成功させるためには、データセットに関するいくつかの重要な決定が必要です。
Can the evaluation be carried out offline on an existing data set or does it require live user tests? If a data set is not currently available, can evaluation be performed on simulated data? What properties should the dataset have in order to best model the tasks for which the recommender is being evaluated? A few examples help clarify these decisions:.
既存のデータセットでオフラインで評価できるか、ライブのユーザーテストを必要とするか。データセットが現在入手できない場合、シミュレーションデータで評価を行うことは可能か？レコメンダーが評価されるタスクを最適にモデル化するために、データセットが持つべき特性は何か？これらの決定を明確にするために、いくつかの例を挙げます。

—When designing a recommender algorithm designed to recommend word processing commands (e.g., Linton et al.
-ワープロのコマンドを推奨するように設計されたレコメンダーアルゴリズムを設計する場合（例：Linton et al.
[1998]), one can expect users to have experienced 5–10% (or more) of the candidates.
[1998]）では、ユーザーは候補の5～10％（またはそれ以上）を経験していると予想される。
Accordingly, it would be unwise to select recommender algorithms based on evaluation results from movie or e-commerce datasets where ratings sparsity is much worse..
したがって、映画や電子商取引のデータセットの評価結果に基づいて推薦アルゴリズムを選択することは、視聴率スパースティがより悪化するため、賢明ではありません。

—When evaluating a recommender algorithm in the context of the Find Good Items task where novel items are desired, it may be inappropriate to use only offline evaluation.
-新奇なアイテムを求めるFind Good Itemsタスクの文脈でレコメンダーアルゴリズムを評価する場合、オフライン評価だけでは不適切な場合があります。
Since the recommender algorithm is generating recommendations for items that the user does not already know about, it is probable that the data set will not provide enough information to evaluate the quality of the items being recommended.
レコメンダーアルゴリズムは、ユーザーがまだ知らないアイテムの推奨を生成するため、データセットは推奨されるアイテムの品質を評価するのに十分な情報を提供しない可能性があります。
If an item was truly unknown to the user, then it is probable that there is no rating for that user in the database.
もし、あるアイテムが本当にユーザーにとって未知のものであった場合、そのユーザーに対するレーティングはデータベースに存在しない可能性が高いです。
If we perform a live user evaluation, ratings can be gained on the spot for each item recommended..
ライブでユーザー評価を行えば、推奨する項目ごとにその場で評価を得ることができます。

—When evaluating a recommender in a new domain where there is significant research on the structure of user preferences, but no data sets, it may be appropriate to first evaluate algorithms against synthetic data sets to identify the promising ones for further study.
-ユーザーの嗜好の構造に関する重要な研究はあるが、データセットがない新しい領域でレコメンダーを評価する場合、まず合成データセットに対してアルゴリズムを評価し、さらなる研究のために有望なものを特定することが適切である場合があります。
We will examine in the following subsections each of the decisions that we posed in the first paragraph of this section, and then discuss the past and current trends in research with respect to collaborative filtering data sets..
以下では、本節の最初の段落で提起した各決定事項を検討し、協調フィルタリングデータセットに関する過去と現在の研究動向について考察することにする。

## Live User Experiments vs. Offline Analyses Live User Experiments vs. オフラインで分析する。

Evaluations can be completed using offline analysis, a variety of live user experimental methods, or a combination of the two.
オフラインでの解析、ライブユーザーによる様々な実験方法、またはその組み合わせで評価を行うことができます。
Much of the work in algorithm evaluation has focused on off-line analysis of predictive accuracy.
アルゴリズム評価に関する研究の多くは、予測精度のオフライン分析に焦点を当てています。
In such an evaluation, the algorithm is used to predict certain withheld values from a dataset, and the results are analyzed using one or more of the metrics discussed in the following section.
このような評価では、アルゴリズムを使用してデータセットから特定の保留値を予測し、その結果を次のセクションで説明する1つまたは複数のメトリクスを使用して分析します。
Such evaluations have the advantage that it is quick and economical to conduct large evaluations, often on several different datasets or algorithms at once.
このような評価は、一度に複数の異なるデータセットやアルゴリズムで大規模な評価を行うことが多く、迅速かつ経済的であるという利点があります。
Once a dataset is available, conducting such an experiment simply requires running the algorithm on the appropriate subset of that data.
データセットがあれば、そのデータの適切なサブセットに対してアルゴリズムを実行するだけで、このような実験を行うことができます。
When the dataset includes timestamps, it is even possible to “replay” a series of ratings and recommendations offline.
データセットにタイムスタンプが含まれている場合、一連の評価と推奨をオフラインで「再生」することも可能です。
Each time a rating was made, the researcher first computes the prediction for that item based on all prior data; then, after evaluating the accuracy of that prediction, the actual rating is entered so the next item can be evaluated..
評価を行うたびに、研究者はまず、すべての先行データをもとにその項目の予測値を計算し、その予測値の正確さを評価した後、次の項目の評価を行うために実際の評価値を入力します。

Offline analyses have two important weaknesses.
オフライン分析には2つの重要な弱点があります。
First, the natural sparsity of ratings data sets limits the set of items that can be evaluated.
まず、視聴率のデータセットには自然な疎密があるため、評価できる項目が限定されます。
We cannot evaluate the appropriateness of a recommended item for a user if we do not have a rating from that user for that item in the dataset.
データセットにそのアイテムに対するユーザーからの評価がない場合、あるユーザーに対する推奨アイテムの適切性を評価することはできません。
Second, they are limited to objective evaluation of prediction results.
第二に、予測結果の客観的な評価に限定されることである。
No offline analysis can determine whether users will prefer a particular system, either because of its predictions or because of other less objective criteria such as the aesthetics of the user interface..
オフラインの分析では、ユーザーが特定のシステムを好むかどうかを、その予測や、ユーザーインターフェースの美しさなど、より客観的でない基準で判断することはできません。

An alternative approach is to conduct a live user experiment.
別のアプローチとして、ライブでユーザー実験を行う方法もあります。
Such experiments may be controlled (e.g., with random assignment of subjects to different conditions), or they may be field studies where a particular system is made available to a community of users that is then observed to ascertain the effects of the system.
このような実験は、コントロールされたもの（例えば、被験者を異なる条件にランダムに割り当てる）である場合もあれば、特定のシステムをユーザーのコミュニティに提供し、そのシステムの効果を確認するために観察するフィールドスタディである場合もあります。
As we discuss later in Section 5.5, live user experiments can evaluate user performance, satisfaction, participation, and other measures..
5.5節で後述するように、ライブユーザー実験では、ユーザーのパフォーマンス、満足度、参加度などを評価することができる。

## Synthesized vs. Natural Data Sets Synthesized vs. ナチュラルデータセット。

Another choice that researchers face is whether to use an existing dataset that may imperfectly match the properties of the target domain and task, or to instead synthesize a dataset specifically to match those properties.
研究者が直面するもう一つの選択は、対象領域やタスクの特性に不完全にマッチする可能性のある既存のデータセットを使用するか、代わりにそれらの特性にマッチするように特別にデータセットを合成するかということです。
In our own early work designing recommender algorithms for Usenet News [Konstan et al.
私たち自身の初期の研究では、ユーズネットニュースのための推薦アルゴリズムを設計していました [Konstan et al.
1997; Miller et al.
1997; Miller et al.
1997], we experimented with a variety of synthesized datasets.
1997]では、様々な合成データセットで実験しました。
We modeled news articles as having a fixed number of “properties” and users as having preferences for those properties.
ニュース記事は一定の「プロパティ」を持ち、ユーザーはそのプロパティに対する嗜好性を持っているとモデル化しました。
Our data set generator could cluster users together, spread them evenly, or present other distributions.
データセットジェネレーターは、ユーザーをまとめたり、均等に広げたり、他の分布を提示することができます。
While these simulated data sets gave us an easy way to test algorithms for obvious flaws, they in no way accurately modeled the nature of real users and real data.
このようなシミュレートされたデータセットは、アルゴリズムに明らかな欠陥がないかをテストする簡単な方法を提供してくれましたが、実際のユーザーや実際のデータの性質を正確にモデル化しているわけではありません。
In their research on horting as an approach for collaborative filtering, Aggarwal et al.
協調フィルタリングのアプローチとしてのホーテイングに関する研究において、Aggarwal et al.
[1999] used a similar technique, noting however that such synthetic data is “unfair to other algorithms” because it fits their approach too well, and that this is a placeholder until they can deploy their trial..
[1999]は同様の手法を用いたが、このような合成データは自分たちのアプローチに適合しすぎているため「他のアルゴリズムに不公平」であると指摘し、これは自分たちの試行を展開するまでのプレースホルダーであるとしている。

Synthesized data sets may be required in some limited cases, but only as early steps while gathering data sets or constructing complete systems.
合成されたデータセットが必要な場合もありますが、それはデータセットを収集したり、完全なシステムを構築する際の初期段階としてのみです。
Drawing comparative conclusions from synthetic datasets is risky, because the data may fit one of the algorithms better than the others..
合成データから比較結論を出すのは危険です。なぜなら、データはどちらかのアルゴリズムが他のアルゴリズムよりも適しているかもしれないからです。

On the other hand, there is new opportunity now to explore more advanced techniques for modeling user interest and generating synthetic data from those models, now that there exists data on which to evaluate the synthetically generated data and tune the models.
一方、ユーザーの興味をモデル化し、そのモデルから合成データを生成するためのより高度な技術を探求する新たな機会が、合成データを評価し、モデルを調整するためのデータが存在する今、到来しています。
Such research could also lead to the development of more accurate recommender algorithms with clearly defined theoretical properties..
このような研究は、理論的特性が明確に定義された、より精度の高いレコメンダーアルゴリズムの開発にもつながるでしょう。

## Properties of Data Sets データセットの特性

The final question we address in this section on data sets is “what properties should the dataset have in order to best model the tasks for which the recommender is being evaluated?” We find it useful to divide data set properties into three categories: Domain features reflect the nature of the content being recommended, rather than any particular system.
データセットに関するこのセクションで扱う最後の質問は、"レコメンダーが評価されるタスクを最適にモデル化するために、データセットが持つべき特性は何か "というものです。我々は、データセットの特性を3つのカテゴリーに分けることが有用であると考える。ドメイン特性は、特定のシステムではなく、推薦されるコンテンツの性質を反映する。
Inherent features reflect the nature of the specific recommender system from which data was drawn (and possibly from its data collection practices).
内在する特徴は、データが収集された特定のレコメンダーシステムの性質（およびおそらくそのデータ収集方法）を反映しています。
Sample features reflect distribution properties of the data, and often can be manipulated by selecting the appropriate subset of a larger data set.
サンプルの特徴は、データの分布特性を反映しており、多くの場合、より大きなデータセットから適切なサブセットを選択することで操作することができます。
We discuss each of these three categories here, identifying specific features within each category..
ここでは、この3つのカテゴリーごとに、それぞれの特徴を説明します。

Domain Features of interest include.
注目のドメイン機能は以下の通りです。

(a) the content topic being recommended/rated and the associated context in which rating/recommendation takes place;.
(a) 推奨されるコンテンツトピック

(b) the user tasks supported by the recommender;.
(b）前記レコメンダーによってサポートされるユーザタスク；である。

(c) the novelty need and the quality need;.
(c) 新規性ニーズと品質ニーズ；。

(d) the cost/benefit ratio of false/true positives/negatives;.
(d）コスト

(e) the granularity of true user preferences..
(e)真のユーザーの好みの粒度。

Most commonly, recommender systems have been built for entertainment content domains (movies, music, etc.), though some testbeds exist for filtering document collections (Usenet news, for example).
推薦システムは、映画、音楽などのエンターテインメントコンテンツ領域で構築されることがほとんどですが、文書コレクション（Usenetニュースなど）をフィルタリングするためのテストベッドも存在します。
Within a particular topic, there may be many contexts.
あるトピックの中に、多くの文脈が存在することがあります。
Movie recommenders may operate on the web, or may operate entirely within a video rental store or as part of a set-top box or digital video recorder..
映画レコメンダーは、ウェブ上で動作する場合もあれば、レンタルビデオ店内やセットトップボックス、デジタルビデオレコーダーの一部として動作する場合もあります。

In our experience, one of the most important generic domain features to consider lies in the tradeoff between desire for novelty and desire for high quality.
私たちの経験では、最も重要な一般的なドメインの特徴の1つは、新規性への欲求と高品質への欲求のトレードオフにあることを考慮しています。
In certain domains, the user goal is dominated by finding recommendations for things she doesn’t already know about.
ある種のドメインでは、ユーザーのゴールは、自分がまだ知らないものを推薦してもらうことである。
McNee et al.
McNeeら。
[2002] evaluated recommenders for research papers and found that users were generally happy with a set of recommendations if there was a single item in the set that appeared to be useful and that the user wasn’t already familiar with.
[2002]は、研究論文の推薦者を評価し、推薦セットの中に有用と思われる項目が1つでもあり、ユーザーがまだよく知らない項目があれば、ユーザーは推薦セットに概ね満足することを発見した。
In some ways, this matches the conventional wisdom about supermarket recommenders—it would be almost always correct, but useless, to recommend bananas, bread, milk, and eggs.
バナナ、パン、牛乳、卵を薦めるのは、ほとんど正しいが、無駄である」というスーパーマーケットのレコメンダーに関する常識と、ある意味で一致している。
The recommendations might be correct, but they don’t change the shopper’s behavior.
レコメンデーションは正しいかもしれないが、ショッパーの行動を変えることはない。
Opposite the desire for novelty is the desire for high quality.
新しさへの欲求と対極にあるのが、高品質への欲求です。
Intuitively, this end of the tradeoff reflects the user’s desire to rely heavily upon the recommendation for a consumption decision, rather than simply as one decision-support factor among many.
直感的には、このトレードオフの末端は、ユーザーが、数ある意思決定支援要因のうちの1つとしてではなく、消費の意思決定において推薦に大きく依存することを望んでいることを反映していると言える。
At the extreme, the availability of highconfidence recommendations could enable automatic purchase decisions such as personalized book- or music-of-the-month clubs.
極端な話、信頼性の高いレコメンデーションを利用することで、パーソナライズされた「今月の本」や「今月の音楽」のような自動購入の意思決定が可能になるかもしれません。
Evaluations of recommenders for this task must evaluate the success of high-confidence recommendations, and perhaps consider the opportunity costs of excessively low confidence..
この課題に対する推薦者の評価は、高信頼度の推薦の成功を評価し、過度に低信頼度の推薦の機会コストを考慮する必要があるのではないだろうか。

Another important domain feature is the cost/benefit ratio faced by users in the domain from which items are being recommended.
また、ドメインの特徴として重要なのが、コスト
In the video recommender domain, the cost of false positives is low (S3 and two to three hours of your evening), the cost of false negatives is almost zero, and the benefit of recommendations is huge (an enormous quantity of movies have been released over the years, and browsing in the video store can be quite stressful—particularly for families).
ビデオレコメンダーの領域では、偽陽性のコストは低く（S3と夜の2～3時間）、偽陰性のコストはほぼゼロであり、推奨のメリットは大きい（長年にわたり膨大な量の映画がリリースされており、ビデオショップでの閲覧は特に家族にとってかなりのストレスになり得る）。
This analysis explains to a large extent why video recommenders have been so successful.
この分析は、ビデオレコメンダーが成功した理由を大きく説明しています。
Other domains with similar domain features, such as books of fiction, are likely to have datasets similar to the video domain and results demonstrated on video data may likely translate somewhat well to those other domains (although books of fiction are likely to have different sample features—see below).
フィクションの本など、ドメインが似ている他のドメインでは、ビデオドメインと同様のデータセットがある可能性が高く、ビデオデータで実証された結果は、他のドメインでもある程度うまく変換できる可能性があります（ただし、フィクションの本はサンプルの特徴が異なる可能性があります-下記参照）。
See Konstan et al.
Konstanら参照。
[1997] for a slightly more detailed discussion of cost/benefit tradeoff analysis in collaborative filtering recommender systems..
コストについては、[1997]がやや詳しい。

Another subtle but important domain feature is the granularity of true user preferences.
もう一つ、微妙だが重要なドメインの特徴は、真のユーザーの好みの粒度である。
How many different levels of true user preference exist? With binary preferences, users only care to distinguish between good and bad items (“I don’t necessarily need the best movie, only a movie I will enjoy”).
ユーザーの真の嗜好は、何段階まで存在するのでしょうか？二元的な嗜好では、ユーザーは良いものと悪いものを区別することにしか関心がありません（「必ずしも最高の映画が必要なのではなく、自分が楽しめる映画であれば良い」）。
In such a case, distinguishing among good items is not important, nor is distinguishing among bad items.
このような場合、良いものを区別することは重要ではなく、悪いものを区別することも重要ではありません。
Note that the granularity of user preference may be different than the range and granularity of the ratings (which is an inherent feature of data sets).
ユーザーの好みの粒度は、評価の範囲や粒度とは異なる場合があることに注意してください（これは、データセットの固有の特徴です）。
Users may rank movies on a 1–10 scale, but then only really care if recommendations are good (I had a good time watching the movie) or bad (I was bored out of my mind!)..
ユーザーは映画を1～10でランク付けすることがありますが、その場合、おすすめが良いか（映画を見るのが楽しかった）、悪いか（退屈だった！）しか気にしません。

Overall, it would probably be a mistake to evaluate an algorithm on data with significantly different domain features.
全体として、ドメインの特徴が大きく異なるデータでアルゴリズムを評価するのは、おそらく間違いでしょう。
In particular, it is very important that the tasks your algorithm is designed to support are similar to the tasks supported by the system from which the data was collected.
特に、アルゴリズムがサポートするように設計されたタスクが、データを収集したシステムがサポートするタスクと類似していることが非常に重要です。
If the user tasks are mismatched, then there are likely to be many other feature mismatches.
ユーザーのタスクが不一致であれば、他にも多くの特徴の不一致があると思われます。
For example, the MovieLens system supported primarily the Find Good Items user task.
例えば、MovieLensでは、主に「良いものを探す」というユーザータスクに対応していました。
As the result, the user was always shown the “best bets” and thus there are many more ratings for good items than bad items (the user had to explicitly request to rate a poor item in most cases).
その結果、ユーザーには常に「ベストベット」が表示されるため、悪いアイテムよりも良いアイテムの評価が多くなっています（ほとんどの場合、ユーザーは悪いアイテムの評価を明示的にリクエストする必要がありました）。
So MovieLens data is less likely to have many ratings for less popular items.
だから、MovieLensのデータは、あまり人気のないものの評価が多くなりにくいのです。
It would probably be inappropriate to use this data to evaluate a new algorithm whose goal was to support Annotation In Context.
このデータを使って、Annotation In Contextをサポートすることを目的とした新しいアルゴリズムを評価することは、おそらく不適切なことでしょう。
Of course, if an algorithm is being proposed for general use, it is best to select data sets that span a variety of topics and contexts.
もちろん、一般的なアルゴリズムを提案する場合は、さまざまなトピックやコンテキストにまたがるデータセットを選択することが最善です。

Inherent features include several features about ratings:.
固有の機能として、視聴率に関するいくつかの機能があります：。

(a) whether ratings are explicit, implicit, or both;.
(a) 評価が明示的、暗黙的、またはその両方であるか。

(b) the scale on which items are rated;.
(b) 項目が評価される尺度；。

(c) the dimensions of rating; and.
(c) レーティングの寸法；及び。

(d) the presence or absence of a timestamp on ratings..
(d) 視聴率に関するタイムスタンプの有無。

Explicit ratings are entered by a user directly (i.e., “Please rate this on a scale of 1–5”), while implicit ratings are inferred from other user behavior.
明示的な評価は、ユーザーが直接入力するもの（例：「これを1～5で評価してください」）であり、暗黙的な評価は、他のユーザーの行動から推測されるものです。
For example, a music recommender may use implicit data such as play lists or music listened to, or it may use explicit scores for songs or artists, or a combination of both.
例えば、音楽レコメンダーは、プレイリストや聴いた音楽などの暗黙のデータを使うこともあれば、曲やアーティストに対する明示的なスコアを使うこともあり、またその両方を組み合わせることもあります。
The ratings scale is the range and granularity of ratings.
レーティングスケールとは、評価の範囲と粒度のことです。
The simplest scale is unary-liked items are marked, all others are unknown.
最もシンプルなスケールは、好きなものには印をつけ、それ以外は不明とするものです。
Unary is common in commerce applications, where all that is known is whether the user purchased an item or not.
ユナリーは、ユーザーが商品を購入したかどうかだけを知ることができるコマースアプリケーションで一般的です。
We call the data unary instead of binary because a lack of purchase of item X does not necessarily mean that the user would not like X.
アイテムXを購入しないことが、必ずしもユーザーがXを好まないことを意味しないため、バイナリーではなくユニアリーデータと呼んでいます。
Binary items include a separate designation for disliked.
バイナリ項目には、嫌われ者の別指定があります。
Systems that operate on explicit ratings often support 5-point, 7-point, or 100-point scales.
明示的な評価で運用するシステムでは、5点、7点、100点のスケールをサポートすることが多い。
While most recommenders have had only a single rating dimension (described by Miller et al.
ほとんどの推薦者は、単一の評価次元しか持っていなかったが（Miller et al.によって記述されている。
[1997] as “what predictions should we have displayed for this item?”), both research and commercial systems are exploring systems where users can enter several ratings for a single item.
[1997]を「このアイテムにはどんな予測を表示するべきだったか」としている）、研究・商用ともに、ユーザーが1つのアイテムに対して複数の評価を入力できるシステムを模索している。
Zagat’s restaurant guides, for example, traditionally use food, service, and decor as three independent dimen- ´ sions.
例えば、ザガットのレストランガイドでは、伝統的に料理、サービス、内装を3つの独立した次元として使用しています。
Movie recommenders may separate story, acting, and special effects.
映画の推薦者は、ストーリー、演技、特撮を分けて考えることがあります。
Data sets with multiple dimensions are still difficult to find, but we expect several to become available in the future.
多次元を持つデータセットはまだ入手困難ですが、今後いくつか入手できるようになると思われます。
Timestamps are a property of the data collection, and are particularly important in areas where user tastes are expected to change or where user reactions to items likely depend on their history of interaction with other items..
タイムスタンプはデータ収集の特性であり、ユーザーの嗜好が変化することが予想される分野や、アイテムに対するユーザーの反応が他のアイテムとの相互作用の履歴に依存する可能性が高い分野では特に重要である。

Other inherent features concern the data collection practices:.
その他の固有の特徴は、次のようなデータ収集方法に関するものです。

(e) whether the recommendations displayed to the user were recorded; and.
(e)ユーザーに表示されたレコメンドが記録されているかどうか、である。

(f) the availability of user demographic information or item content information..
(f) ユーザーのデモグラフィック情報またはアイテムのコンテンツ情報を利用できること。

Unfortunately, few datasets recorded the recommendations that were displayed, making it difficult to retrospectively isolate, for example, ratings that could not have been biased by previously displayed predictions.
しかし、残念ながら、表示されたレコメンデーションを記録したデータセットはほとんどなく、例えば、以前に表示された予測に偏らない評価をレトロスペクティブに分離することは困難であった。
Some logs may keep time-stamped queries, which could be used to reconstruct recommendations if the algorithm is known and fully deterministic.
ログによっては、タイムスタンプ付きのクエリを保存している場合があり、アルゴリズムが既知で完全に決定論的であれば、それを使ってレコメンデーションを再構築できる可能性があります。
The availability of demographic data varies with the specific system, and with the specific data collected.
デモグラフィック・データの利用可能性は、特定のシステム、および収集された特定のデータによって異なります。
The EachMovie and MovieLens datasets both collected limited demographics.
EachMovieとMovieLensのデータセットでは、どちらも限られたデモグラフィックを収集しました。
Researchers speculate, however, that a large percentage of the demographic answers may be false (based on user suspicion of “marketing questions”).
しかし、研究者は、（「マーケティング質問」に対するユーザーの疑念に基づき）人口統計学的な回答の大部分が虚偽である可能性があると推測しています。
We would expect greater reliability for demographic data that users believe actually serves a constructive purpose in the recommender (either for recommendation or for related purposes).
レコメンダーにおいて実際に建設的な目的を果たすとユーザーが考えている人口統計データ（推薦のため、または関連する目的のため）については、より高い信頼性が期待されるでしょう。
A film recommender that uses zip code to narrow the theater search, such as Miller et al.’s [2003] MovieLens Unplugged, seems more likely to provide meaningful data..
Millerら[2003]のMovieLens Unpluggedのように、郵便番号を使って映画館を絞り込む映画レコメンダーは、意味のあるデータを提供できる可能性が高いようです。

Finally, we consider:.
最後に、次のことを検討する。

(g) the biases involved in data collection..
(g) データ収集に伴うバイアス。

Most data sets have biases based on the mechanism by which users have the opportunity to rate items.
ほとんどのデータセットには、ユーザーがアイテムを評価する機会を持つメカニズムに基づくバイアスがあります。
For example, Jester [Goldberg et al.
例えば、Jester［Goldberg et al.
2001] asked all users to rate the same initial jokes, creating a set of dense ratings for those jokes which would not otherwise occur.
2001]では、すべてのユーザーに同じ初期ジョークを評価してもらい、通常では発生しないようなジョークの濃い評価セットを作成しました。
MovieLens has experimented with different methods to select items to have the first-time user rate before using the recommender system [Rashid et al.
MovieLensでは、レコメンダーシステムを使う前に、初回利用率が高いアイテムを選択するために、さまざまな方法で実験を行っています［Rashid et al.
2002], and in the process demonstrated that each method leads to a different bias in initial ratings..
2002年]、その過程で、各手法が初期評価に異なるバイアスをもたらすことを実証しました。

Sample features include many of the statistical properties that are commonly considered in evaluating a data set:.
サンプルの特徴には、データセットの評価で一般的に考慮される次のような統計的特性が多く含まれます。

(a) the density of the ratings set overall, sometimes measured as the average percentage of items that have been rated per user; since many datasets have uneven popularity distributions, density may be artificially manipulated by including or excluding items;.
(a)評価セット全体の密度。ユーザーごとに評価されたアイテムの平均割合として測定されることもある。多くのデータセットには不均一な人気分布があるため、密度はアイテムを含めたり除外することで人為的に操作されることがあります。

(b) the number or density of ratings from the users for whom recommendations are being made, which represents the experience of the user in the system at the time of recommendation; ratings from users with significant experience can be withheld to simulate the condition when they were new users; and.
(b) 推薦が行われるユーザーからの評価の数または密度であって、推薦時のシステムにおけるユーザーの経験を表すもの。重要な経験を有するユーザーからの評価は、新規ユーザーであったときの状態をシミュレートするために保留されることができる。

(c) the general size and distribution properties of the data set—some data sets have more items than users, though most data sets have many more users than items..
(c) データセットの一般的なサイズと分布特性-データセットによっては、ユーザーよりもアイテムの数が多いものもあるが、ほとんどのデータセットでは、アイテムよりもユーザーの数が多い。

Each of these sample features can have substantial effect on the success of different algorithms, and can reflect specific policies of the recommender.
これらのサンプルの特徴は、それぞれ異なるアルゴリズムの成功に大きな影響を与え、レコメンダーの特定のポリシーを反映することができます。
Density (both individual and overall) reflects both the overall size of the recommender’s item space and the degree to which users have explored it.
密度（個別と全体の両方）は、レコメンダーのアイテム空間の全体的なサイズと、ユーザーがそれを探索した度合いの両方を反映しています。
One policy decision that significantly affects density is the level of rating required to participate in the community.
密度に大きく影響する政策判断として、地域社会への参加に必要な格付けのレベルがある。
Systems that either require an extensive level of start-up rating or require recurring ratings to maintain membership or status levels will generally have greater density than low-commitment recommenders in the same domain.
一般に、同じドメインにおいて、広範なレベルのスタートアップ評価を必要とするシステムや、メンバーシップやステータスレベルを維持するために繰り返し評価を必要とするシステムは、低コミットメントのレコメンダーよりも密度が高くなります。
Density also interacts with the type of rating—implicit ratings are likely to lead to greater density, since less effort is needed by the user.
密度は、評価の種類にも影響されます。暗黙の評価は、ユーザーの労力が少なくて済むため、密度が高くなる可能性が高いです。
Finally, system that allow automated software “agents” to participate may have a significantly higher density than other systems, even if the underlying item space is similar (see, e.g., Good et al.
最後に、自動化されたソフトウェア「エージェント」が参加できるシステムは、基礎となるアイテム空間が類似していても、他のシステムよりも密度が著しく高い場合がある（例えば、Good et al.参照）。
[1999]).
[1999]).
Because software agents are not limited in attention, they can rate much more extensively than humans..
ソフトウェアエージェントは注意力に制限がないため、人間よりもはるかに広範囲に評価することができます。

Two particular distribution properties are known to be highly important.
特に2つの分布特性は非常に重要であることが知られている。
The relationship between the numbers of users and numbers of items can determine whether it is easier to build correlations among users or among items— this choice can lead to different relative performance among algorithms.
ユーザー数とアイテム数の関係から、ユーザー間の相関を取りやすいか、アイテム間の相関を取りやすいかを判断することができ、この選択によって、アルゴリズム間の相対的な性能に差が出ることがあります。
The ratings distribution of items and users also may affect both algorithm and evaluation metric choice.
また、アイテムやユーザーの評価分布は、アルゴリズムや評価指標の選択に影響を与える可能性がある。
Systems where there is an exponential popularity curve (some items have exponentially more ratings than others) may be able to find agreement among people or items in the dense subregion and use that agreement to recommend in the sparse space.
指数関数的な人気曲線（あるアイテムは他のアイテムより指数関数的に評価が高い）があるシステムでは、密な部分領域で人々やアイテムの間の合意を見つけ、その合意を疎な空間での推薦に利用することができるかもしれない。
(Jester, mentioned above, does this directly by creating a highly dense region of jokes rated by all users.) Systems with a more even ratings distribution may be more challenged to cope with sparsity unless they incorporate dimensionality reduction techniques..
(前述のJesterは、すべてのユーザーによって評価されたジョークの高密度な領域を作成することによって、これを直接行っています)。より均等な評価分布を持つシステムは、次元削減技術を取り入れない限り、スパース性に対処することが困難である可能性があります。

To complete the discussion of domain features, inherent features, and sample features, it is important to note that there are significant interactions between these categories of features.
ドメイン特徴、固有特徴、サンプル特徴の議論を終えるにあたり、これらの特徴のカテゴリー間に有意な相互作用があることに注目することが重要である。
For example, the type of task supported by a recommender system (a domain feature) will significantly affect the distribution of ratings collected (a sample feature).
例えば、レコメンダーシステムがサポートするタスクの種類（ドメイン特徴）は、収集した評価の分布（サンプル特徴）に大きく影響します。
However, each of these features represents a dimension which may be useful in explaining differences in evaluation results..
しかし、これらの特徴は、それぞれ評価結果の違いを説明するのに有用な次元を表しています。

Evaluation of a recommender algorithm on a data set with features that conflict with the end goal of the recommender algorithm could still be useful.
推薦アルゴリズムの最終目標と相反する特徴を持つデータセットで推薦アルゴリズムを評価することは、依然として有用である。
By explicitly identifying the features that conflict, we can reason about whether those conflicts will unreasonably bias the evaluation results..
対立する特徴を明示することで、その対立が評価結果に不当な偏りを与えるかどうかを推論することができるのです。

##  Past and Current Trends in Datasets データセットの過去と現在の動向。

The most widely used common dataset was the EachMovie Dataset (http:// research.compaq.com/SRC/eachmovie/).
最も広く使われた共通データセットは、EachMovie Dataset（http:
This extensive dataset has over 2.8 million ratings from over 70,000 users, and it includes information such as timestamps and basic demographic data for some of the users.
この広範なデータセットには、7万人以上のユーザーによる280万件以上の評価があり、一部のユーザーのタイムスタンプや基本的な人口統計データなどの情報も含まれています。
In addition to seeding our MovieLens system (http://www.movielens.org), the EachMovie Dataset was used in dozens of machine learning and algorithmic research projects to study new and potentially better ways to predict user ratings.
また、当社のMovieLensシステム（http:
Examples include Canny’s [2002] factor analysis algorithm, Domingos and Richardson’s [2003] algorithm for computing network value, and Pennock et al’s [2000] work on recommending through personality diagnosis algorithms..
例えば、Canny [2002]の因子分析アルゴリズム、Domingos and Richardson [2003]のネットワーク価値計算アルゴリズム、Pennock et al [2000]の性格診断アルゴリズムによる推薦の研究などがある。

Extracts (100,000 ratings and 1 million ratings) of the MovieLens dataset have also been released for research use; these extracts have been used by several researchers, including Schein et al.
MovieLensデータセットの抽出物（10万件の評価と100万件の評価）も研究用に公開されており、これらの抽出物はSchein et al.を含むいくつかの研究者によって使用されている。
[2001] in their investigation of coldstart recommendations, Sarwar et al.
[2001]はコールドスタート推奨の調査において、Sarwar et al.
[2001] in their evaluation of item-based algorithms, Reddy et al.
[2001]はアイテムベースアルゴリズムの評価で、Reddy et al.
[2002] in their community extraction research, and Mui et al.
[2002]はコミュニティ抽出の研究で、Mui et al.
[2001] in their work on “collaborative sanctioning.”.
[2001年]の「協調的制裁」に関する研究においてである。

More recently, several researchers have been using the Jester dataset, which was collected from the Jester joke recommendation website [Goldberg et al.
最近では、いくつかの研究者が、ジョーク推薦サイトJesterから収集されたJesterデータセットを使用している [Goldberg et al.
2001].
2001].
Statistically, the Jester dataset has different characteristics than the MovieLens and Eachmovie data.
Jesterデータセットは、統計的にMovieLensやEachmovieのデータとは異なる特性を持っています。
First of all, there is a set of training items (jokes) that are rated by every single user, providing complete data on that subset of items.
まず、すべてのユーザーによって評価されたトレーニングアイテム（ジョーク）のセットがあり、そのアイテムのサブセットに関する完全なデータが提供されます。
Second, in the Jester user interface, the user clicks on a unlabeled scale bar to rate a joke, so the ratings are much less discrete and may suffer from different kinds of biases since it is hard for the user to intentionally create a ranking among their rated items..
第二に、Jesterのユーザーインターフェースでは、ユーザーはラベルのないスケールバーをクリックしてジョークを評価するため、評価ははるかに不連続であり、ユーザーが意図的に評価項目のランキングを作成することは困難であるため、異なる種類のバイアスに悩まされるかもしれません。

The majority of publications related to collaborative filtering recommender algorithms have used one of the three data sets described above.
協調フィルタリング型レコメンダーアルゴリズムに関連する出版物の大半は、上記の3つのデータセットのいずれかを使用しています。
A few other data sets have been used, but most of them are not publicly available for verification.
その他にもいくつかのデータセットが使用されていますが、そのほとんどは検証のために公開されていません。
The lack of variety in publicly available collaborative filtering data sets (particularly with significant numbers of ratings) remains one of the most significant challenges in the field.
一般に公開されている協調フィルタリングのデータセット（特に評価数が多いもの）の種類が少ないことは、この分野の最も大きな課題の1つです。
Most researchers do not have the resources to build production-quality systems that are capable of collecting enough data to validate research hypotheses, and thus are often forced to constrain their research to hypotheses that can be explored using the few existing datasets..
多くの研究者は、研究仮説を検証するのに十分なデータを収集できる生産品質のシステムを構築するリソースを持っていないため、既存の数少ないデータセットを使って探求できる仮説に研究を限定せざるを得ないことが多い。

With the maturation of collaborative filtering recommender technology, more live systems have been built that incorporate recommender algorithms.
協調フィルタリングによるレコメンダー技術の成熟に伴い、レコメンダーアルゴリズムを組み込んだライブシステムがより多く構築されています。
As a result, we have recently seen an increased number of studies that have used live systems.
そのため、最近ではライブシステムを使用した研究も増えてきました。
Herlocker’s explanation experiments [Herlocker et al.
Herlockerの説明実験［Herlocker et al.
2000] explored the use of 23 different graphical displays to “explain” why each recommendation was given.
2000年]は、各推薦の理由を「説明」するために、23種類のグラフ表示を使用することを検討しました。
Schafer’s MetaLens [Schafer et al.
SchaferのMetaLens [Schafer et al.
2002] was built to incorporate MovieLens and other systems into a new interface; his evaluation focused entirely on the interface and user experience.
2002]は、MovieLensと他のシステムを新しいインターフェースに組み込むために作られました。彼の評価は、インターフェースとユーザーエクスペリエンスに完全に焦点を当てています。
Other recent work has combined different evaluations.
その他、最近の作品では、異なる評価を組み合わせています。
Our work on “value of information” [Rashid et al.
情報の価値」についての我々の研究［Rashid et al.
2002] leads users through different sign-up processes, and then evaluates both the quality of resulting predictions and the subjective user experience..
2002]では、ユーザーをさまざまなサインアッププロセスに誘導し、その結果得られる予測の品質と主観的なユーザー体験の両方を評価しました。

In the near future, we expect to see a lot more results from live experiments, as recommender algorithms make their way into more production systems.
近い将来、レコメンダーアルゴリズムがより多くのプロダクションシステムに導入され、ライブ実験の結果がより多く見られるようになることが期待されます。
We also hope that new datasets will be released with data from new domains, causing new explosions in collaborative filtering recommender algorithm research similar to what happened with the release of the EachMovie data..
また、新たなドメインからのデータセットが公開され、EachMovieのデータ公開のように協調フィルタリング推薦アルゴリズム研究に新たな爆発が起こることを期待しています。

# Accuracy Metrics アキュラシーメトリックス

Establishing the user tasks to be supported by a system, and selecting a data set on which performance enables empirical experimentation—scientifically repeatable evaluations of recommender system utility.
システムがサポートするユーザーのタスクを設定し、パフォーマンスを発揮するデータセットを選択することで、レコメンダーシステムの有用性を科学的に繰り返し評価する実証実験が可能になります。
A majority of the published empirical evaluations of recommender systems to date has focused on the evaluation of a recommender system’s accuracy.
これまで発表されてきたレコメンダーシステムの実証評価の大半は、レコメンダーシステムの精度の評価に焦点が当てられています。
We assume that if a user could examine all items available, they could place those items in a ordering of preference.
もし、ユーザーがすべてのアイテムを調べることができれば、それらのアイテムを優先的に配置することができると仮定しています。
An accuracy metric empirically measures how close a recommender system’s predicted ranking of items for a user differs from the user’s true ranking of preference.
精度とは、あるユーザーに対して推薦システムが予測したアイテムの順位が、そのユーザーの真の好み順位とどれだけ近いかを経験的に測定するものです。
Accuracy measures may also measure how well a system can predict an exact rating value for a specific item..
精度は、特定の項目に対する正確な評価値をシステムがどれだけ予測できるかを測定することもできる。

Researchers who want to quantitatively compare the accuracy of different recommender systems must first select one or more metrics.
異なるレコメンダーシステムの精度を定量的に比較したい研究者は、まず1つまたは複数のメトリクスを選択する必要があります。
In selecting a metric, researchers face a range of questions.
研究者は、指標を選択する際に、さまざまな疑問に直面することになる。
Will a given metric measure the effectiveness of a system with respect to the user tasks for which it was designed? Are results with the chosen metric comparable to other published research work in the field? Are the assumptions that a metric is based on true? Will a metric be sensitive enough to detect real differences that exist? How large a difference does there have to be in the value of a metric for a statistically significant difference to exist? Complete answers to these questions have not yet been substantially addressed in the published literature..
与えられた指標は、そのシステムが設計されたユーザーのタスクに関して、そのシステムの有効性を測定することができるか？選択した指標を用いた結果は、その分野で公表されている他の研究成果と比較可能か？メトリクスが基づいている仮定は正しいか？あるメトリクスは、実際に存在する差異を検出するのに十分な感度を持つか？統計的に有意な差があるためには、指標の値にどれくらいの差が必要なのか？これらの疑問に対する完全な答えは、出版された文献の中でまだ実質的に扱われていない。

The challenge of selecting an appropriate metric is compounded by the large diversity of published metrics that have been used to quantitatively evaluate the accuracy of recommender systems.
レコメンダーシステムの精度を定量的に評価するために使用されるメトリクスは、非常に多様であるため、適切なメトリクスを選択する課題はさらに深刻です。
This lack of standardization is damaging to the progress of knowledge related to collaborative filtering recommender systems.
このような標準化の欠如は、協調フィルタリング推薦システムに関連する知識の進歩に損害を与えている。
With no standardized metrics within the field, researchers have continued to introduce new metrics when they evaluate their systems.
この分野では標準的な評価基準がないため、研究者はシステムを評価する際に新しい評価基準を導入し続けています。
With a large diversity of evaluation metrics in use, it becomes difficult to compare results from one publication to the results in another publication.
多様な評価指標が使用されているため、ある出版物の結果を別の出版物の結果と比較することが難しくなっています。
As a result, it becomes hard to integrate these diverse publications into a coherent body of knowledge regarding the quality of recommender system algorithms..
その結果、推薦システムアルゴリズムの品質に関して、これらの多様な論文を首尾一貫した知識体系として統合することは難しくなっています。

To address these challenges, we examine in the advantages and disadvantages of past metrics with respect to the user tasks and data set features that have been introduced in Sections 2 and 3.
これらの課題を解決するために、第2節と第3節で紹介したユーザータスクとデータセットの特徴に関して、過去のメトリクスの長所と短所を検証します。
We follow up the conceptual discussion of advantages and disadvantages with empirical results comparing the performance of different metrics when applied to results from one class of algorithm in one domain.
我々は、利点と欠点の概念的な議論に続いて、1つのドメインで1つのクラスのアルゴリズムから得られた結果に適用した場合の異なるメトリクスの性能を比較する経験的な結果を示します。
The empirical results demonstrate that some conceptual differences among accuracy evaluation metrics can be more significant than others..
実証結果は、精度評価指標間の概念的な差異が、他よりも大きくなる可能性があることを示した。

## Evaluation of Previously Used Metrics これまで使われてきた評価指標を評価する

Recommender system accuracy has been evaluated in the research literature since 1994 [Resnick et al.
レコメンダーシステムの精度は、1994年から研究文献で評価されている［Resnick et al.
1994].
1994].
Many of the published evaluations of recommender systems used different metrics.
発表されたレコメンダーシステムの評価の多くは、異なる評価基準で行われていました。
We will examine some of the most popular metrics used in those publications, identifying the strengths and the weaknesses of the metrics.
それらの出版物で使用されている代表的なメトリクスを検証し、メトリクスの長所と短所を明らかにします。
We broadly classify recommendation accuracy metrics into three classes: predictive accuracy metrics, classification accuracy metrics, and rank accuracy metrics..
推薦精度指標を予測精度指標、分類精度指標、ランク精度指標の3つに大別している。

### Predictive Accuracy Metrics. 予測精度の指標...

Predictive accuracy metrics measure how close the recommender system’s predicted ratings are to the true user ratings.
予測精度の指標は、推薦システムの予測した評価が、真のユーザー評価にどれだけ近いかを測定します。
Predictive accuracy metrics are particularly important for evaluating tasks in which the predicting rating will be displayed to the user such as Annotation in Context.
予測精度メトリクスは、Annotation in Contextのような予測評価がユーザーに表示されるタスクを評価する際に特に重要です。
For example, the MovieLens movie recommender [Dahlen et al.
例えば、映画レコメンダー「MovieLens」[Dahlen et al.
1998] predicts the number of stars that a user will give each movie and displays that prediction to the user.
1998]は、ユーザーが各映画に与える星の数を予測し、その予測をユーザーに表示する。
Predictive accuracy metrics will evaluate how close MovieLens’ predictions are to the user’s true number of stars given to each movie.
予測精度の指標は、MovieLensの予測が、各映画に与えられたユーザーの真の星数にどれだけ近いかを評価します。
Even if a recommender system was able to correctly rank a user’s movie recommendations, the system could fail if the predicted ratings it displays to the user are incorrect.1 Because the predicted rating values create an ordering across the items, predictive accuracy can also be used to measure the ability of a recommender system to rank items with respect to user preference.
予測された評価値は項目間の順序を作成するため、予測精度は、ユーザーの好みに関して項目をランク付けする推薦システムの能力を測定するために使用することもできます。
On the other hand, evaluators who wish to measure predictive accuracy are necessarily limited to a metric that computes the difference between the predicted rating and true rating such as mean absolute error..
一方、予測精度を測定したい評価者は、平均絶対誤差のような予測評価と真の評価との差を計算する指標にどうしても限定されてしまう。

Mean Absolute Error and Related Metrics.
平均絶対誤差とその関連指標。
Mean absolute error (often referred to as MAE) measures the average absolute deviation between a predicted rating and the user’s true rating.
平均絶対誤差（しばしばMAEと呼ばれる）は、予測された評価とユーザーの真の評価との間の平均絶対偏差を測定します。
Mean absolute error (Eq.
平均絶対誤差（Eq.
(1)) has been used to evaluate recommender systems in several cases [Breese et al.
(1)）は、いくつかのケースでレコメンダーシステムの評価に使用されている［Breese et al.
1998, Herlocker et al.
1998年、Herlocker et al.
1999, Shardanand and Maes 1995]..
1999, Shardanand and Maes 1995]である。

$$
\tag{1}
$$

Mean absolute error may be less appropriate for tasks such as Find Good Items where a ranked result is returned to the user, who then only views items at the top of the ranking.
平均絶対誤差は、ランキングされた結果がユーザーに返され、ユーザーはランキングの上位のアイテムのみを閲覧する「良いアイテムを探す」のようなタスクにはあまり適していないかもしれません。
For these tasks, users may only care about errors in items that are ranked high, or that should be ranked high.
このようなタスクでは、ユーザーは、上位にランクされている、あるいは上位にランクされるべきアイテムのエラーだけを気にすることができます。
It may be unimportant how accurate predictions are for items that the system correctly knows the user will have no interest in.
ユーザーが興味を示さないことをシステムが正しく認識している項目の予測精度は重要ではないかもしれません。
Mean absolute error may be less appropriate when the granularity of true preference (a domain feature) is small, since errors will only affect the task if they result in erroneously classifying a good item as a bad one or vice versa; for example, if 3.5 stars is the cut-off between good and bad, then a one-star error that predicts a 4 as 5 (or a 3 as 2) makes no difference to the user..
平均絶対誤差は、真の嗜好の粒度（ドメインの特徴）が小さい場合には、あまり適切ではないかもしれません。なぜなら、誤差は、良いものを悪いものに誤って分類したり、その逆の場合にのみタスクに影響するからです。

Beyond measuring the accuracy of the predictions at every rank, there are two other advantages to mean absolute error.
すべてのランクにおける予測の精度を測定する以外にも、平均絶対誤差には2つの利点があります。
First, the mechanics of the computation are simple and easy to understand.
まず、計算の仕組みがシンプルでわかりやすいことです。
Second, mean absolute error has well studied statistical properties that provide for testing the significance of a difference between the mean absolute errors of two systems..
第二に、平均絶対誤差は、2つのシステムの平均絶対誤差の差の有意性を検証するために、よく研究された統計的性質を持っています。

Three measures related to mean absolute error are mean squared error, root mean squared error, and normalized mean absolute error.
平均絶対誤差に関連する指標として、平均二乗誤差、平均二乗根誤差、正規化平均絶対誤差の3つがある。
The first two variations square the error before summing it.
最初の2つのバリエーションは、合計する前に誤差を2乗する。
The result is more emphasis on large errors.
その結果、大きな誤差がより強調されることになります。
For example, an error of one point increases the sum of error by one, but an error of two points increases the sum by four.
例えば、1ポイントの誤差は誤差の合計を1つ増やすが、2ポイントの誤差は合計を4つ増やす。
The third related measure, normalized mean absolute error [Goldberg et al.
第3の関連指標である正規化平均絶対誤差［Goldberg et al.
2001], is mean absolute error normalized with respect to the range of rating values, in theory allowing comparison between prediction runs on different datasets (although the utility of this has not yet been investigated)..
2001]では、平均絶対誤差を評価値の範囲に関して正規化したもので、理論的には異なるデータセットでの予測実行間の比較が可能である（ただし、その有用性はまだ調査されていない）。

In addition to mean absolute error across all predicted ratings, Shardanand and Maes [1995] measured separately mean absolute error over items to which users gave extreme ratings.
Shardanand and Maes [1995]は、予測されたすべての評価に対する平均絶対誤差に加えて、ユーザーが極端な評価をした項目に対する平均絶対誤差を個別に測定した。
They partitioned their items into two groups, based on user rating (a scale of 1 to 7).
彼らは、ユーザーの評価（1～7段階）に基づき、アイテムを2つのグループに分けました。
Items rated below three or greater than five were considered extremes.
3点以下、5点以上の項目は極端な評価とした。
The intuition was that users would be much more aware of a recommender system’s performance on items that they felt strongly about.
それは、「自分の思い入れが強いものほど、ユーザーはレコメンダーシステムの性能を意識する」という直感です。
From Shardanand and Maes’ results, the mean absolute error of the extremes provides a different ranking of algorithms than the normal mean absolute error.
ShardanandとMaesの結果から、極値の平均絶対誤差は、通常の平均絶対誤差とは異なるアルゴリズムのランキングを提供します。
Measuring the mean absolute error of the extremes can be valuable.
極値の平均絶対誤差を測定することは、価値あることです。
However, unless users are concerned only with how their extremes are predicted, it should not be used in isolation..
しかし、ユーザーが自分の極限値をどのように予測するかにのみ関心を持つのでなければ、単独で使用することはできないはずです。

### Classification Accuracy Metrics. 分類精度の指標.

Classification metrics measure the frequency with which a recommender system makes correct or incorrect decisions about whether an item is good.
分類指標は、推薦システムが、あるアイテムが良いかどうかの判断を正しく行うか、あるいは間違って行うかの頻度を測定するものです。
Classification metrics are thus appropriate for tasks such as Find Good Items when users have true binary preferences..
このため、分類指標は、ユーザーが真の二項対立的な好みを持つ場合に、「良い品物を探す」などのタスクに適している。

When applied to nonsynthesized data in offline experiments, classification accuracy metrics may be challenged by data sparsity.
オフライン実験で非合成データに適用する場合、データの疎密によって分類精度の指標に問題が生じることがあります。
The problem occurs when the collaborative filtering system being evaluated is generating a list of top recommended items.
この問題は、評価対象の協調フィルタリングシステムが、上位推奨アイテムのリストを生成している場合に発生します。
When the quality of the list is evaluated, recommendations may be encountered that have not been rated.
リストの品質を評価する際、評価されていない推奨品に出会うことがあります。
How those items are treated in the evaluation can lead to certain biases..
それらの項目が評価の中でどのように扱われるかで、ある種のバイアスがかかってしまうのです。

One approach to evaluation using sparse data sets is to ignore recommendations for items for which there are no ratings.
疎なデータセットを用いた評価の一つのアプローチとして、評価がない項目については推奨を無視するというものがあります。
The recommendation list is first processed to remove all unrated items.
レコメンドリストは、まず、未評価のものをすべて削除する処理を行います。
The recommendation task has been altered to “predict the top recommended items that have been rated.” In tasks where the user only observes the top few recommendations, this could lead to inaccurate evaluations of recommendation systems with respect to the user’s task.
推薦タスクは、"評価された上位の推薦アイテムを予測する "に変更された。ユーザーが上位数点の推奨品しか観察しないタスクでは、ユーザーのタスクに関して推奨システムの評価が不正確になる可能性があります。
The problem is that the quality of the items that the user would actually see may never be measured..
問題は、ユーザーが実際に目にするアイテムの品質が測れない可能性があることです。

In an example of how this could be significant, consider the following situation that could occur when using the nearest neighbor algorithm described in Herlocker et al.
このことがいかに重要であるかを示す例として、Herlocker et al.に記載されている最近傍アルゴリズムを使用した場合に起こりうる以下の状況を考えてみましょう。
[2002]: when only one user in the dataset has rated an eclectic item I, then the prediction for item I for all users will be equal to the rating given by that user.
[2002]：データセットの中で、折衷的なアイテムIを評価したユーザーが1人しかいない場合、すべてのユーザーに対するアイテムIの予測値は、そのユーザーによって与えられた評価と同じになる。
If a user gave item I a perfect rating of 5, then the algorithm will predict a perfect 5 for all other users.
あるユーザーがアイテムIに満点の5をつけた場合、アルゴリズムは他のすべてのユーザーにも満点の5をつけると予測します。
Thus, item I will immediately be placed at the top of the recommendation list for all users, in spite of the lack of confirming data.
このため、確認データがないにもかかわらず、すべてのユーザーに対して、アイテムIが即座にレコメンドリストの最上位に位置することになります。
However, since no other user has rated this item, the recommendation for item I will be ignored by the evaluation metric, which thus will entirely miss the flaw in the algorithm..
しかし、このアイテムは他のユーザーから評価されていないため、アイテムIの推薦文は評価指標から無視され、アルゴリズムの欠陥を完全に見逃してしまうことになる。

Another approach to evaluation of sparse data sets is to assume default ratings, often slightly negative, for recommended items that have not been rated [Breese et al.
疎なデータセットの評価に対するもう一つのアプローチは、評価されていない推奨アイテムに対して、デフォルトの評価（多くの場合、わずかにネガティブ）を仮定することです[Breese et al.
1998].
1998].
The downside of this approach is that the default rating may be very different from the true rating (unobserved) for an item..
この方法の欠点は、デフォルトのレーティングが、あるアイテムの真のレーティング（未観測）と大きく異なる可能性があることである。

A third approach that we have seen in the literature is to compute how many of the highly rated items are found in the recommendation list generated by the recommender system.
文献で見かけた3つ目のアプローチは、推薦システムが生成した推薦リストに、高評価のアイテムがどれだけ含まれているかを計算するものです。
In essence, we are measuring how well the system can identify items that the user was already aware of.
要するに、ユーザーがすでに認識していた項目を、システムがどれだけ識別できるかを測っているのです。
This evaluation approach may result in collaborative filtering algorithms that are biased towards obvious, nonnovel recommendations or perhaps algorithms that are over fitted—fitting the known data perfectly, but new data poorly.
この評価方法では、協調フィルタリングアルゴリズムが、自明で斬新でないレコメンデーションに偏ってしまったり、アルゴリズムがオーバーフィットしてしまい、既知のデータには完璧にフィットするが、新しいデータにはうまくフィットしないことがある。
In Section 5 of this article, we discuss metrics for evaluating novelty of recommendations..
本論文のセクション5では、推薦文の新規性を評価するための指標について述べる。

Classification accuracy metrics do not attempt to directly measure the ability of an algorithm to accurately predict ratings.
分類精度メトリクスは、アルゴリズムが正確に評価を予測する能力を直接測定しようとするものではありません。
Deviations from actual ratings are tolerated, as long as they do not lead to classification errors.
実際の評価との乖離は、分類の誤りにつながらない限り許容されます。
The particular metrics that we discuss are Precision and Recall and related metrics and ROC.
特に議論するメトリクスは、PrecisionとRecallとその関連メトリクスとROCである。
We also briefly discuss some ad hoc metrics..
また、いくつかのアドホックなメトリクスについても簡単に説明します。

#### Precision and Recall and Related Measures PrecisionとRecallと関連する尺度。

Precision and recall are the most popular metrics for evaluating information retrieval systems.
情報検索システムを評価する指標としては、PrecisionとRecallが有名である。
In 1968, Cleverdon proposed them as the key metrics [Cleverdon and Kean 1968], and they have held ever since.
1968年にクレバードンがキーメトリクスとして提唱し［Cleverdon and Kean 1968］、それ以来、キーメトリクスを維持している。
For the evaluation of recommender systems, they have been used by Billsus and Pazzani [1998], Basu et al.
推薦システムの評価には、Billsus and Pazzani [1998]、Basu et al.が使用している。
[1998], and Sarwar et al.
[1998]、Sarwar et al.
[2000a, 2000b].
[2000a、2000b］。
Precision and recall are computed from a 2 × 2 table, such as the one shown in Table I.
PrecisionとRecallは、表Iに示すような2×2の表から計算される。
The item set must be separated into two classes—relevant or not relevant.
アイテムセットは、関連するものとそうでないものの2つのクラスに分けなければならない。
That is, if the rating scale is not already binary, we need to transform it into a binary scale.
つまり、評価尺度がすでに2値化されていない場合は、2値化する必要があるのです。
For example, the MovieLens dataset [Dahlen et al.
例えば、MovieLensデータセット[Dahlen et al.
1998] has a rating scale of 1–5 and is commonly transformed into a binary scale by converting every rating of 4 or 5 to “relevant” and all ratings of 1–3 to “notrelevant.” For precision and recall, we also need to separate the item set into the set that was returned to the user (selected/recommended), and the set that was not.
1998]は1～5の評価スケールを持ち、4または5のすべての評価を "related "に、1～3のすべての評価を "notrelevant "に変換することで2値スケールに変換するのが一般的です。精度と想起については、アイテムセットを、ユーザーに返されたセット（selected
We assume that the user will consider all items that are retrieved..
ユーザは、検索されたすべてのアイテムを考慮すると仮定する。

Precision is defined as the ratio of relevant items selected to number of items selected, shown in Eq.
精度は、選択された項目数に対する選択された項目の割合として定義され、式（1）で示される。
(2).
(2).

$$
\tag{2}
$$

Precision represents the probability that a selected item is relevant.
精度は、選択された項目が関連性を持つ確率を表します。
Recall, shown in Eq.
式で示されるリコール。
(3), is defined as the ratio of relevant items selected to total number of relevant items available.
(3)は、利用可能な関連項目の総数に対する選択された関連項目の比率と定義される。
Recall represents the probability that a relevant item will be selected.
Recallは、関連する項目が選択される確率を表します。

$$
\tag{3}
$$

Precision and recall depend on the separation of relevant and nonrelevant items.
PrecisionとRecallは、関連項目と非関連項目の分離に依存します。
The definition of “relevance” and the proper way to compute it has been a significant source of argument within the field of information retrieval [Harter 1996].
関連性」の定義とそれを計算する適切な方法は、情報検索の分野では重要な議論の種となっている[Harter 1996]。
Most information retrieval evaluation has focused on an objective version of relevance, where relevance is defined with respect to a query, and is independent of the user.
情報検索の評価の多くは、関連性がクエリに対して定義され、ユーザに依存しない、関連性の客観的バージョンに焦点を当てています。
Teams of experts can compare documents to queries and determine which documents are relevant to which queries.
専門家チームは、文書とクエリを比較し、どの文書がどのクエリに関連しているかを判断することができます。
However, objective relevance makes no sense in recommender systems.
しかし、客観的な関連性はレコメンダーシステムでは意味をなさない。
Recommender systems recommend items based on the likelihood that they will meet a specific user’s taste or interest.
レコメンダーシステムは、特定のユーザーの好みや興味に合う可能性に基づいてアイテムを推薦するシステムです。
That user is the only person who can determine if an item meets his taste requirements.
自分の好みに合うかどうかを判断できるのは、そのユーザーだけなのです。
Thus, relevance is more inherently subjective in recommender systems than in traditional document retrieval..
このように、レコメンダーシステムでは、従来の文書検索よりもレリバンスが本質的に主観的である。

In addition to user tastes being different, user rating scales may also be different.
ユーザーの嗜好が異なるだけでなく、ユーザーの評価尺度も異なる場合があります。
One user may consider a rating of 3- on a 5-point scale to be relevant, while another may consider it irrelevant.
あるユーザーは、5段階評価の3-を関連性があると考え、別のユーザーは無関係と考えるかもしれません。
For this reason, much research using multipoint scales (such as in Hill et al.
このため、多点尺度を用いた多くの研究（Hill et al.のような。
[1995], Resnick et al.
[1995]、Resnick et al.
[1994], and Shardanand and Maes [1995]) has focused on other metrics besides Precision/Recall.
[1994]、Shardanand and Maes [1995]）は、Precision以外のメトリクスにも着目している。
One interesting approach that has been taken to identify the proper threshold is to assume that a top percentile of items rated by a user are relevant [Basu et al.
適切な閾値を特定するために取られた興味深いアプローチの1つは、ユーザーによって評価されたアイテムの上位パーセンタイルが関連性があると仮定することです[Basu et al.
1998]..
1998]..

Recall, in its purest sense, is almost always impractical to measure in a recommender system.
最も純粋な意味での「リコール」は、レコメンダーシステムで測定することはほとんど現実的ではありません。
In the pure sense, measuring recall requires knowing whether each item is relevant; for a movie recommender, this would involve asking many users to view all 5000 movies to measure how successfully we recommend each one to each user.
純粋な意味で、リコールを測定するには、各項目が関連しているかどうかを知る必要があります。映画レコメンダーの場合、多くのユーザーに5000本の映画をすべて見てもらい、各ユーザーにどれだけうまく映画を推薦できたかを測定することになります。
IR evaluations have been able to estimate recall by pooling relevance ratings across many users, but this approach depends on the assumption that all users agree on which items are relevant, which is inconsistent with the purpose of recommender systems..
IRの評価では、多くのユーザーの関連性評価をプールすることでリコールを推定することができますが、このアプローチは、すべてのユーザーがどのアイテムが関連するかについて同意するという仮定に依存しており、レコメンダーシステムの目的とは矛盾しています。

Several approximations to recall have been developed and used to evaluate recommender systems.
リコールの近似値はいくつか開発され、レコメンダーシステムの評価に使用されている。
Sarwar et al.
Sarwarら。
[2000a] evaluate their algorithms by taking a dataset of user ratings which they divide into a training set and a test set.
[2000a]は、ユーザー評価のデータセットを学習セットとテストセットに分け、アルゴリズムを評価している。
They train the recommender algorithm on the training set, and then predict the top N items that the user is likely to find valuable, where N is some fixed value.
学習セットで推薦アルゴリズムを学習し、ユーザーが価値を見出す可能性の高い上位N個のアイテムを予測します（Nはある固定値）。
They then compute recall as the percentage of known relevant items from the test set that appear in the top N predicted items.
そして、テストセットからの既知の関連項目が、上位N個の予測項目に現れる割合として、リコールを計算する。
Since the number of items that each user rates is much smaller than the number of items in the entire dataset (see the discussion on data sparsity at the beginning of this section), the number of relevant items in the test set may be a small fraction of the number of relevant items in the entire dataset.
各ユーザが評価する項目の数は、データセット全体の項目数よりもはるかに少ないため（本節冒頭のデータスパース性に関する議論を参照）、テストセットの関連項目数は、データセット全体の関連項目数のごく一部となる可能性がある。
While this metric can be useful, it has underlying biases that researchers must be aware of.
この指標は有用である一方、研究者が注意しなければならない根本的なバイアスがある。
In particular, the value of this metric depends heavily on the percentage of relevant items that each user has rated.
特に、この指標の値は、各ユーザーが評価した関連アイテムの割合に大きく依存します。
If a user has rated only a small percentage of relevant items, a recommender with high “true recall” may yield a low value for measured recall, since the recommender may have recommended unrated relevant items.
ユーザーが関連するアイテムのわずかな割合しか評価していない場合、「真のリコール」が高いレコメンダーは、レコメンダーが評価されていない関連アイテムを推奨している可能性があるため、測定されたリコールは低い値を示すかもしれません。
Accordingly, this metric should only be used in a comparative fashion on the same dataset; it should not be interpreted as an absolute measure..
従って、この指標は同一データセットでの比較にのみ使用されるべきであり、絶対的な指標として解釈されるべきではありません。

We have also seen precision measured in the same fashion [Sarwar et al.
また、同じ方法で精度を測定しているのを見たことがある[Sarwar et al.
2000a] with relevant items being selected from a small pool of rated items and predicted items being selected from a much larger set of items.
2000a]では、関連項目は評価された項目の小さなプールから選択され、予測項目ははるかに大きな項目のセットから選択されます。
Similarly, this approximation to precision suffers from the same biases as the recall approximation..
同様に、この精度への近似は、想起への近似と同じバイアスに悩まされる。

Perhaps a more appropriate way to approximate precision and recall would be to predict the top N items for which we have ratings.
精度や想起の近似値としては、評価がある上位N項目を予測するのが適切かもしれませんね。
That is, we take a user’s ratings, split them into a training set and a test set, train the algorithm on the training set, then predict the top N items from that user’s test set.
つまり、あるユーザーの評価を得て、それをトレーニングセットとテストセットに分け、トレーニングセットでアルゴリズムを訓練し、そのユーザーのテストセットから上位N個のアイテムを予測するのです。
If we assume that the distribution of relevant items and nonrelevant items within the user’s test set is the same as the true distribution for the user across all items, then the precision and recall will be much closer approximations of the true precision and recall.
もし、ユーザーのテストセット内の関連項目と非関連項目の分布が、すべての項目にわたるユーザーの真の分布と同じであると仮定すれば、精度とリコールは真の精度とリコールにもっと近い近似値になる。
This approach is taken in Basu et al.
このアプローチは、Basu et al.
[1998]..
[1998]..

In information retrieval, precision and recall can be linked to probabilities that directly affect the user.
情報検索において、精度や想起は、ユーザーに直接影響を与える確率と結びつけることができる。
If an algorithm has a measured precision of 70%, then the user can expect that, on average, 7 out of every 10 documents returned to the user will be relevant.
あるアルゴリズムの測定精度が70％である場合、ユーザーは、平均して、ユーザーに返される10個の文書のうち7個は関連性があると期待できることになります。
Users can more intuitively comprehend the meaning of a 10% difference in precision than they can a 0.5-point difference in mean absolute error..
平均絶対誤差が0.5ポイント違うよりも、精度が10％違う方が、ユーザーは直感的にその意味を理解できるのです。

One of the primary challenges to using precision and recall to compare different algorithms is that precision and recall must be considered together to evaluate completely the performance of an algorithm.
異なるアルゴリズムを比較するために精度とリコールを使用する主な課題の1つは、アルゴリズムの性能を完全に評価するためには精度とリコールを一緒に考慮する必要があることです。
It has been observed that precision and recall are inversely related [Cleverdon and Kean 1968] and are dependent on the length of the result list returned to the user.
精度と想起は反比例の関係にあり［Cleverdon and Kean 1968］、ユーザーに返す結果リストの長さに依存することが確認されている。
When more items are returned, then the recall increases and precision decreases.
より多くのアイテムが返されると、リコールが増加し、プレシジョンが減少します。
Therefore, if the information system doesn’t always return a fixed number of items, we must provide a vector of precision/recall pairs to fully describe the performance of the system.
したがって、情報システムが常に一定の数を返すわけではない場合、精度の高いベクトルを用意する必要があります
While such an analysis may provide a detailed picture of the performance of a system, it makes comparison of systems complicated, tedious, and variable between different observers.
このような分析は、システムの性能を詳細に把握することができる反面、システムの比較が複雑で面倒であり、異なる観察者間で変動することになります。
Furthermore, researchers may carefully choose at which levels of recall (or search length) they report precision and recall to match the strengths in their system..
さらに、研究者は、システムの強みに合わせて、どのレベルのリコール（または検索長）で精度やリコールを報告するかを慎重に選択することができます。

Several approaches have been taken to combine precision and recall into a single metric.
精度とリコールを1つの指標にまとめるために、いくつかのアプローチがとられてきた。
One approach is the F1 metric (Eq.
一つのアプローチとして、F1メトリック（Eq.
(4)), which combines precision and recall into a single number The F1 has been used to evaluate recommender systems in Sarwar et al.
(4)）は、PrecisionとRecallを一つの数値にまとめたものである。 F1は、Sarwar et al.
[2000a, 2000b].
[2000a、2000b］。
An alternate approach taken by the TREC community is to compute the average precision across several different levels of recall or the average precision at the rank of each relevant document [Harman 1995].
TRECコミュニティによって取られた別のアプローチは、いくつかの異なるレベルのリコールにわたる平均精度、または各関連文書のランクにおける平均精度を計算することである [Harman 1995]。
The latter approach was taken in all but the initial TREC conference.
後者のアプローチは、最初のTREC会議を除くすべての会議で採用されました。
This approach is commonly referred to as Mean Average Precision or MAP.
このアプローチは、一般に平均平均精度（Mean Average Precision）またはMAPと呼ばれる。
F1 and mean average precision may be appropriate if the underlying precision and recall measures on which it is based are determined to be appropriate.
F1および平均平均精度は、その根拠となる精度および想起の尺度が適切であると判断される場合には、適切であると考えられる。

$$
\tag{4}
$$

Precision alone at a single search length or a single recall level can be appropriate if the user does not need a complete list of all potentially relevant items, such as in the Find Good Items task.
Find Good Itemsタスクのように、ユーザーが潜在的に関連するすべてのアイテムの完全なリストを必要としない場合、単一の検索長または単一のリコールレベルでの精度のみが適切である場合があります。
If the task is to find all relevant items in an area, then recall becomes important as well.
あるエリアにある関連アイテムをすべて見つけるというタスクであれば、リコールも重要になる。
However, the search length at which precision is measured should be appropriate for the user task and content domain..
ただし、精度を測定する検索長は、ユーザーのタスクとコンテンツドメインに適したものでなければならない。

As with all classification metrics, precision and recall are less appropriate for domains with non-binary granularity of true preference.
すべての分類指標と同様に、真の嗜好の粒度が二値でないドメインでは、精度と回収はあまり適切ではありません。
For those tasks, at any point in the ranking, we want the current item to be more relevant than all items lower in the ranking.
このようなタスクでは、ランキングのどの時点でも、現在のアイテムがランキングの下位にあるすべてのアイテムよりも関連性が高いことが望まれます。
Since precision and recall only measure binary relevance, they cannot measure the quality of the ordering among items that are selected as relevant..
PrecisionとRecallは二値的な関連性を測定するだけなので、関連するものとして選択されたアイテム間の順序付けの質を測定することはできない。

#### ROC Curves, Swets’ A Measure, and Related Metrics ROC曲線、Swets' A Measure、および関連指標。

ROC curve-based metrics provide a theoretically grounded alternative to precision and recall.
ROC曲線に基づく指標は、精度や想起に代わる理論的根拠のある指標を提供します。
There are two different popularly held definitions for the acronym ROC.
頭字語ROCには、一般的に言われている2種類の定義があります。
Swets [1963, 1969] introduced the ROC metric to the information retrieval community under the name “relative operating characteristic.” More popular however, is the name “receiver operating characteristic,” which evolved from the use of ROC curves in signal detection theory [Hanley and McNeil 1982].
Swets [1963, 1969]は、ROC指標を "relative operating characteristic "という名称で情報検索界に紹介した。しかし、より一般的なのは、信号検出理論におけるROC曲線の使用から発展した「受信者動作特性」という名前である[Hanley and McNeil 1982]。
Regardless, in both cases, ROC refers to the same underlying metric..
ただし、どちらの場合も ROC は同じ基礎指標を指している。

The ROC model attempts to measure the extent to which an information filtering system can successfully distinguish between signal (relevance) and noise.
ROCモデルは、情報フィルタリングシステムが信号（関連性）とノイズをどの程度うまく区別できるかを測定しようとするものです。
The ROC model assumes that the information system will assign a predicted level of relevance to every potential item.
ROCモデルは、情報システムがすべての潜在的なアイテムに予測された関連性のレベルを割り当てることを想定している。
Given this assumption, we can see that there will be two distributions, shown in Figure 1.
この仮定を踏まえると、図1に示すような2つの分布になることがわかります。
The distribution on the left represents the probability that the system will predict a given level of relevance (the x-axis) for an item that is in reality not relevant to the information need.
左側の分布は、実際には情報ニーズと関連性のない項目に対して、システムがあるレベルの関連性（X軸）を予測する確率を表しています。
The distribution on the right indicates the same probability distribution for items that are relevant.
右の分布は、関連性のある項目については同じ確率分布を示しています。
Intuitively, we can see that the further apart these two distributions are, the better the system is at differentiating relevant items from nonrelevant items..
直感的には、この2つの分布が離れているほど、システムが関連項目と非関連項目を区別するのに優れていることがわかります。

With systems that return a ranked list, the user will generally view the recommended items starting at the top of the list and work down until the information need is met, a certain time limit is reached, or a predetermined number of results are examined.
ランク付けされたリストを返すシステムでは、一般に、ユーザーは、情報ニーズが満たされるか、一定の制限時間に達するか、または所定の数の結果を調べるまで、リストの最上位から順に推奨項目を表示します。
In any case, the ROC model assumes that there is a filter tuning value zc, such that all items that the system ranks above the cutoff are viewed by the user, and those below the cutoff are not viewed by the user.
いずれにせよ、ROCモデルは、システムがカットオフ以上のランク付けをしたアイテムはすべてユーザーが閲覧し、カットオフ以下のアイテムはユーザーが閲覧しないようなフィルターチューニング値zcが存在すると仮定している。
This cutoff defines the search length.
このカットオフが、サーチレングスを決定します。
As shown in Figure 1, at each value of zc, there will be a different value of recall (percentage of good items returned, or the area under the relevant probability distribution to the right of zc) and fallout (percentage of bad items returned, or the area under the nonrelevant probability distribution to the right of zc).
図1に示すように、zcの値ごとに、リコール（良品の返却率、またはzcの右側の関連確率分布下の面積）とフォールアウト（不良品の返却率、またはzcの右側の非関連確率分布下の面積）が異なる値となります。
The ROC curve represents a plot of recall versus fallout, where the points on the curve correspond to each value of zc.
ROC曲線は、リコール対フォールアウトのプロットを表しており、曲線上の点はzcの各値に対応している。
An example of an ROC curve is shown in Figure 2..
ROC曲線の一例を図2に示す。

A common algorithm for creating an ROC curve goes as follows:.
ROC曲線を作成するための一般的なアルゴリズムは以下の通りです。

- (1) Determine how you will identify if an item is relevant or nonrelevant. (1) 項目が関連するか非関連かを識別する方法を決定する。

- (2) Generate a predicted ranking of items. (2) アイテムの予測順位を生成する。

- (3) For each predicted item, in decreasing order of predicted relevance (starting the graph at the origin): (3) 各予測項目について、予測された関連性の高い順に（原点からグラフを開始）：。

- (a) If the predicted item is indeed relevant, draw the curve one step vertically. (a) 予測された項目が本当に関連するのであれば、曲線を一段階垂直に描く。

- (b) If the predicted item is not relevant, draw the curve one step horizontally to the right. (b) 予測された項目が関係ない場合、曲線を右へ一歩水平に描く。

- (c) If the predicted item has not been rated (i.e., relevance is not known), then the item is simply discarded and does not affect the curve negatively or positively. (c) 予測された項目が評価されていない場合（すなわち、関連性がわからない場合）、その項目は単に廃棄され、曲線に負または正の影響を与えない。

An example of an ROC curve constructed in this manner is shown in Figure 2..
このように構成されたROC曲線の例を図2に示す。

A perfect predictive system will generate an ROC curve that goes straight upward until 100% of relevant items have been encountered, then straight right for the remaining items.
完璧な予測システムは、ROC曲線が、関連する項目が100%になるまでまっすぐ上向き、残りの項目についてはまっすぐ右向きになるように生成されます。
A random predictor is expected to produce a straight line from the origin to the upper right corner.2.
ランダム予測器は、原点から右上隅までの直線を生成することが期待されます.2。

ROC curves are useful for tuning the signal/noise tradeoff in information systems.
ROC曲線は、信号のチューニングに有効です
For example, by looking at an ROC curve, you might discover that your information filter performs well for an initial burst of signal at the top of the rankings, and then produces only small increases of signal for moderate increases in noise from then on..
例えば、ROCカーブを見ると、情報フィルターは、ランキングの上位にある最初の信号のバーストに対してはよく機能し、それ以降はノイズが適度に増加しても信号の増加はわずかであることがわかるかもしれません。

Similar to Precision and Recall measures, ROC curves make an assumption of binary relevance.
PrecisionとRecallの測定と同様に、ROC曲線は二値的な関連性を仮定している。
Items recommended are either successful recommendations (relevant) or unsuccessful recommendation (nonrelevant).
推奨される項目は、推奨に成功したもの（関連）または推奨に失敗したもの（非関連）のいずれかです。
One consequence of this assumption is that the ordering among relevant items has no consequence on the ROC metric—if all relevant items appear before all nonrelevant items in the recommendation list, you will have a perfect ROC curve..
この仮定がもたらす一つの結果は、関連する項目の順序がROC指標に影響を与えないということです。推薦リストにおいて、すべての関連項目がすべての非関連項目の前に表示されていれば、完璧なROC曲線が得られます。

Comparing multiple systems using ROC curves becomes tedious and subjective, just as with precision and recall.
ROC曲線を使って複数のシステムを比較するのは、精度や想起と同じように面倒で主観的なものになる。
However, a single summary performance number can be obtained from an ROC curve.
しかし、ROC曲線から1つの要約された性能数値を得ることができる。
The area underneath an ROC curve, also known as Swet’s A measure, can be used as a single metric of the system’s ability to discriminate between good and bad items, independent of the search length.
ROC曲線の下の面積は、SwetのA指標とも呼ばれ、検索長に依存せず、システムの良品と不良品の識別能力を示す一つの指標として用いることができる。
According to Hanley and McNeil [1982], the area underneath the ROC curve is equivalent to the probability that the system will be able to choose correctly between two items, one randomly selected from the set of bad items, and one randomly selected from the set of good items.
Hanley and McNeil [1982]によれば、ROC曲線の下の面積は、システムが、悪い項目の集合からランダムに選ばれた1つと、良い項目の集合からランダムに選ばれた1つの2つの項目の間で正しく選択できる確率に相当します。
Intuitively, the area underneath the ROC curve captures the recall of the system at many different levels of fallout.
直感的には、ROC曲線の下の領域は、多くの異なるレベルの落下物におけるシステムの想起を捉えています。
It is also possible to measure the statistical significance of the difference between two areas [Hanley and McNeil 1982; Le and Lindren 1995]..
また、2つの領域の差の統計的有意性を測定することも可能である［Hanley and McNeil 1982; Le and Lindren 1995］。

The ROC area metric has the disadvantage that equally distant swaps in the rankings will have the same affect on ROC area regardless of whether they occur near the top of the ranking or near the end of the ranking.
ROC面積の指標は、ランキングの上位と下位のどちらで入れ替わっても、ROC面積に与える影響が同じになるという欠点がある。
For example, if a good item is ranked 15 instead of 10, it will have roughly the same affect on the ROC area as if a good item is ranked 200 instead of 195.
例えば、良いものを10位ではなく15位にした場合、良いものを195位ではなく200位にした場合とほぼ同じ影響をROC領域に与えることになります。
This disadvantage could be significant for tasks such as Find Good Items where the first situation is likely to have a greater negative affect on the user.
このデメリットは、「良いものを探す」のように、最初の状況がユーザーにより大きな悪影響を与える可能性が高いタスクにおいて、大きな意味を持つと考えられます。
This disadvantage is somewhat minimized by the fact that relevance is binary and exchanges within a relevance class have no affect (if items ranked 10–15 are all relevant, an exchange between 10 and 15 will have no affect at all).
この欠点は、関連性が二値であり、関連性クラス内の交換は影響を及ぼさないという事実によって、いくらか軽減される（10～15位のアイテムがすべて関連する場合、10～15位の交換はまったく影響を及ぼさない）。
On the other hand, for tasks such as Find All Good Items, the discussed disadvantage may not be significant..
一方、"Find All Good Items "のようなタスクでは、議論されたデメリットはそれほど大きくないかもしれません。

Hanley and McNeil [1982] present a method by which one can determine the number of data points necessary to ensure that a comparison between two areas has good statistical power (defined as a high probability of identifying a difference if one exists).
Hanley and McNeil [1982]は、2つの領域の比較が良好な統計的検出力（差異が存在する場合、それを識別する確率が高いと定義）を持つことを保証するために必要なデータポイントの数を決定することができる方法を提示した。
Hanley’s data suggests that many data points may be required to have a high level of statistical power.
Hanleyのデータから、高い統計的検出力を得るためには、多くのデータポイントが必要である可能性があることが示唆された。
The number of required data points for significance becomes especially large when the two areas being compared are very close in value.
特に、比較する2つの領域の値が非常に近い場合、有意性を示すために必要なデータ点数が大きくなります。
Thus, to confidently compare the results of different algorithms using ROC area, the potential result set for each user must also be large.
したがって、ROC領域を用いて異なるアルゴリズムの結果を確信を持って比較するためには、各ユーザーの潜在的な結果集合も大きくなければならない。
The advantages of ROC area metric are that it (a) provides a single number representing the overall performance of an information filtering system, (b) is developed from solid statistical decision theory designed for measuring the performance of tasks such as those that a recommender system performs, and (c) covers the performance of the system over all different recommendation list lengths..
ROCエリアメトリックの利点は、(a)情報フィルタリングシステムの総合的な性能を表す単一の数値が得られること、(b)推薦システムが実行するようなタスクの性能を測定するために設計された確固たる統計決定理論から開発されていること、(c)すべての異なる推薦リストの長さに対するシステムの性能をカバーしていること、です。

To summarize the disadvantages of the ROC area metric: (a) a large set of potentially relevant items is needed for each query; (b) for some tasks, such as Find Good Items users are only interested in performance at one setting, not all possible settings; (c) equally distant swaps in rankings have the same effect no matter where in the ranking they occur; and (d) it may need a large number of data points to ensure good statistical power for differentiating between two areas..
ROCエリアメトリクスの欠点をまとめると、(a)各クエリに潜在的に関連するアイテムの大規模なセットが必要、(b)Find Good Itemsのような一部のタスクでは、ユーザーは可能なすべての設定ではなく、ある設定でのパフォーマンスにしか興味がない、(c) ランキングで等距離の交換は、どのランキングで発生しても同じ効果がある、(d) 二つのエリアの違いを識別するために、統計力を確保できる多数のデータ点を必要とするかもしれません。

The ROC area measure is most appropriate when there is a clear binary relevance relationship and the task is similar to Find Good Items, where the user wants to see as many of the relevant answers as possible within certain resource limitations..
ROCエリア測定は、明確な2値関連性があり、タスクがFind Good Itemsに似ていて、ユーザーが一定のリソース制限の中でできるだけ多くの関連する答えを見たいと考えている場合に最も適しています。

#### Ad Hoc Classification Accuracy Measures アドホック分類の精度測定。

Ad hoc measures of classification accuracy have attempted to identify error rates and, in particular, large errors.
分類精度のアドホックな測定は、エラー率、特に大きなエラーを特定することを試みている。
Error rate can be measured in a manner derived from Precision and Recall.
エラー率は、PrecisionとRecallから派生する方法で測定することができます。
Specifically, the error rate for a system is the number of incorrect recommendations it makes divided by the total number of recommendations.
具体的には、あるシステムのエラーレートは、誤った推薦をした数を推薦の総数で割ったものです。
If a system recommends only a few items, it is possible to measure error rate experimentally.
数点しか推薦しないシステムであれば、実験的にエラーレートを測定することが可能です。
Jester, for example, which presents jokes to users, can evaluate the error rate based on the immediate feedback users give to each joke [Goldberg et al.
例えば、ジョークをユーザに提示するJesterは、ユーザが各ジョークに与える即時フィードバックに基づいてエラー率を評価できる[Goldberg et al.
2001].
2001].
More commonly, the error rate computation is limited to the subset of recommended items for which a rating is available; this approach introduces the bias that users commonly avoid consuming (and therefore rating) items that don’t interest them, and therefore this approximate error rate is likely to be lower than the true error rate..
より一般的には、評価可能な推奨アイテムのサブセットに限定してエラーレート計算を行う。このアプローチでは、ユーザーが興味のないアイテムの消費（したがって評価）を避けるというバイアスが生じるため、この近似エラーレートは真のエラーレートより低くなる可能性がある。

Another ad hoc technique specifically identifies large errors.
もう一つのアドホックな手法は、特に大きなエラーを識別するものです。
Sarwar et al.
Sarwarら。
[1998] measured reversals when studying agent-boosted recommendations.
[1998]は、エージェントブーストによる推薦を研究する際に、逆転現象を測定した。
Errors of three or more points on a five-point scale were considered significant enough to potentially undermine user confidence, and therefore were tallied separately.
5段階評価で3点以上の誤差は、ユーザーの信頼性を損なう可能性があると判断し、別途集計しています。
Such a measurement mixes aspects of classification and prediction accuracy, but has not been generally used by later researchers.
このような測定は、分類と予測精度の側面をミックスしたものであるが、後進の研究者により一般的に使用されることはなかった。
It might be particularly appropriate for the Evaluate Recommender task..
特に「Evaluate Recommender」のタスクに適しているかもしれません。

### Rank Accuracy Metrics. ランク精度指標.

Rank accuracy metrics measure the ability of a recommendation algorithm to produce a recommended ordering of items that matches how the user would have ordered the same items.
ランク精度の指標は、推薦アルゴリズムが、ユーザーが同じアイテムをどのように注文したかに一致するアイテムの推奨順序を生成する能力を測定します。
Unlike classification metrics, ranking metrics are more appropriate to evaluate algorithms that will be used to present ranked recommendation lists to the user, in domains where the user’s preferences in recommendations are nonbinary..
分類指標と異なり、ランキング指標は、推薦におけるユーザーの好みが二値でない領域において、ランク付けされた推薦リストをユーザーに提示するために使用されるアルゴリズムを評価するために、より適切です。

Rank accuracy metrics may be overly sensitive for domains where the user just wants an item that is “good enough” (binary preferences) since the user won’t be concerned about the ordering of items beyond the binary classification.
ランク精度の指標は、ユーザーが「十分に良い」項目（二値嗜好）を求めるだけのドメインでは、二値分類を超えた項目の順序には関心がないため、過度に敏感になる可能性があります。
For example, even if the top ten items ranked by the system were relevant, a rank accuracy metric might give a nonperfect value because the best item is actually ranked 10th.
例えば、システムがランク付けした上位10項目が適切であったとしても、実際にはベストの項目が10位にランクされているため、ランク精度の指標は非完全な値を与えるかもしれません。
By the same token, rank accuracy metrics can distinguish between the “best” alternatives and just “good” alternatives and may be more appropriate for domains where that distinction is important.
同じ意味で、ランク精度メトリクスは、「最良の」選択肢と単なる「良い」選択肢を区別することができ、その区別が重要なドメインに適しているかもしれません。
In such domains it is possible for all the top recommended items to be relevant, but still not be the “best” items..
このようなドメインでは、上位に推薦されたアイテムがすべて関連性があっても、「ベスト」なアイテムではないことがあり得ます。

Ranking metrics do not attempt to measure the ability of an algorithm to accurately predict the rating for a single item—they are not predictive accuracy metrics and are not appropriate for evaluating the Annotation in Context task.
ランキングメトリクスは、アルゴリズムが1つの項目の評価を正確に予測する能力を測定しようとするものではなく、予測精度メトリクスではなく、Annotation in Contextタスクの評価には適していません。
If a recommender system will be displaying predicted rating values, it is important to additionally evaluate the system using a predictive accuracy metric as described above.
レコメンダーシステムが予測された評価値を表示する場合、上記のような予測精度の指標を用いてシステムを追加評価することが重要である。
We examine several correlation metrics, a half-life utility metric, and the NDPM metric..
いくつかの相関指標、半減期効用指標、NDPM指標を検討した。

### Prediction-Rating Correlation. 予測-評価相関.

Two variables are correlated if the variance in one variable can be explained by the variance in the second.
つの変数の分散が2つ目の変数の分散で説明できる場合、2つの変数は相関がある。
Three of the most well known correlation measures are Pearson’s product–moment correlation, Spearman’s ρ, and Kendall’s Tau..
相関尺度は、ピアソンの積率相関、スピアマンのρ、ケンダルのタウの3つがよく知られている。

Pearson correlation measures the extent to which there is a linear relationship between two variables.
ピアソン相関は、2つの変数の間にどの程度直線的な関係があるかを測定します。
It is defined as the covariance of the z-scores, shown in Eq.
式で示されるzスコアの共分散として定義される。
(5)..
(5)..

$$
\tag{5}
$$

Rank correlations, such as Spearman’s ρ (Eq.
スピアマンのρ（式）のような順位相関。
(6)) and Kendall’s Tau, measure the extent to which two different rankings agree independent of the actual values of the variables.
(6)）、ケンドールのタウは、変数の実際の値とは無関係に、異なる2つの順位がどの程度一致するかを測定するものです。
Spearman’s ρ is computed in the same manner as the Pearson product–moment correlation, except that the x’s and y’s are transformed into ranks, and the correlations are computed on the ranks..
スピアマンのρは、ピアソンの積率相関と同じ方法で計算されます。ただし、xとyはランクに変換され、相関はランクで計算されます。

$$
\tag{6}
$$

Kendall’s Tau represents a different approach to computing the correlation of the rankings that is independent of the variable values.
Kendall's Tauは、変数値に依存しないランキングの相関を計算するための異なるアプローチを表しています。
One approximation to Kendall’s Tau is shown in Eq.
Kendall's Tauの近似値の1つを式に示す。
(7).
(7).
C stands for the number of concondant pairs—pairs of items that the system predicts in the proper ranked order.
Cは、システムが適切な順位で予測するペアの数です。
D stands for the number of discordant pairs—pairs that the system predicts in the wrong order.
Dは、システムが間違った順序で予測した不一致のペアの数です。
TR is number of pairs of items in the true ordering (the ranking determined by the user’s ratings) that have tied ranks (i.e., the same rating) while TP is the number of pairs of items in the predicted ordering that have tied ranks (the same prediction value).
TRは、真の順序（ユーザーの評価によって決定される順位）の中で、順位が同順位（同じ評価）である項目のペアの数であり、TPは、予測順序の中で、順位が同順位（同じ予測値）である項目のペアの数である。

$$
\tag{7}
$$

In spite of their simplicity, the above correlation metrics have not been used extensively in the measurement of recommender systems or information retrieval systems.
上記の相関指標は、そのシンプルさにもかかわらず、レコメンダーシステムや情報検索システムの測定に広く使用されていません。
Pearson correlation was used by Hill et al.
ピアソン相関は、Hill et al.
[1995] to evaluate the performance of their recommender system..
[1995]の推薦者システムの性能を評価する。

The advantages of correlation metrics are (a) they compare a non-binary system ranking to a non-binary user ranking, (b) they are well understood by the scientific community, and (c) they provide a single measurement score for the entire system..
相関メトリクスの利点は、（a）二値でないシステムランキングと二値でないユーザーランキングを比較すること、（b）科学界でよく理解されていること、（c）システム全体に対して単一の測定スコアを提供すること、である。

There may be weaknesses in the way in which the “badness” of an interchange is calculated with different correlation metrics.
異なる相関指標でインターチェンジの「悪さ」を算出する方法には弱点があるかもしれません。
For example, Kendall’s Tau metric applies equal weight to any interchange of equal distance, no matter where it occurs (similar to the ROC area metric).
例えば、KendallのTau指標は、等距離のインターチェンジがどこに発生しても、等しい重みを適用します（ROC面積指標に似ています）。
Therefore, an interchange between recommendations 1 and 2 will be just as bad as an interchange between recommendations 1000 and 1001.
したがって、推奨品1と推奨品2の交換は、推奨品1000と推奨品1001の交換と同じように悪くなるのです。
However, if the user is much more likely to consider the first five, and will probably never examine items ranked in the thousands, the interchange between 1 and 2 should have a more substantial negative impact on the outcome of the metric..
しかし、ユーザーが最初の5つを検討する可能性が高く、数千のランク付けされたアイテムを検討することはおそらくないとすれば、1と2の間の交換は、メトリックの結果に、より実質的にマイナスの影響を与えるはずである。

The Spearman correlation metric does not handle weak (partial) orderings well.
スピアマンの相関指標は弱い（部分的な）順序をうまく扱えません。
Weak orderings occur whenever there are at least two items in the ranking such that neither item is preferred over the other.
弱順位は、ランキングの中に少なくとも2つの項目があり、どちらの項目も他より優先されない場合に発生します。
If a ranking is not a weak ordering then it is called a complete ordering.
順位が弱い順序でない場合は、完全な順序と呼ばれます。
If the user’s ranking (based on their ratings) is a weak ordering and the system ranking is a complete ordering, then the Spearman correlation will be penalized for every pair of items which the user has rated the same, but the system ranks at different levels.
ユーザーのランキング（評価に基づく）が弱い順序で、システムのランキングが完全な順序である場合、スピアマン相関は、ユーザーが同じ評価をしたが、システムが異なるレベルでランク付けした項目のすべてのペアでペナルティを受ける。
This is not ideal, since the user shouldn’t care how the system orders items that the user has rated at the same level.
これは理想的ではありません。なぜなら、ユーザーは、ユーザーが同じレベルで評価したアイテムを、システムがどのように注文するかを気にするべきではありません。
Kendall’s Tau metric also suffers the same problem, although to a lesser extent than the Spearman correlation..
KendallのTau指標も、Spearmanの相関よりも程度は低いですが、同じ問題を抱えています。

#### Half-life Utility Metric Half-life Utility Metric.

Breese et al.
Breeseら。
[1998], presented a new evaluation metric for recommender systems that is designed for tasks where the user is presented with a ranked list of results, and is unlikely to browse very deeply into the ranked list.
[1998）は、推薦システムの新しい評価指標を提示した。この評価指標は、ユーザーが結果のランク付けされたリストを提示され、ランク付けされたリストをあまり深く閲覧する可能性がないタスクのために設計されている。
Another description of this metric can be found in Heckerman et al.
このメトリックの別の説明は、Heckerman et al.にあります。
[2000].
[2000].
The task for which the metric is designed is an Internet web-page recommender.
この指標を設計したタスクは、インターネット上のウェブページのレコメンダーである。
They claim that most Internet users will not browse very deeply into results returned by search engines..
多くのインターネットユーザーは、検索エンジンが返す結果を深く見ることはないだろうというのです。

This half-life utility metric attempts to evaluate the utility of a ranked list to the user.
この半減期の効用指標は、ユーザーにとってランク付けされたリストの効用を評価しようとするものである。
The utility is defined as the difference between the user’s rating for an item and the “default rating” for an item.
効用は、あるアイテムに対するユーザーの評価と、あるアイテムに対する「デフォルトの評価」の差として定義されます。
The default rating is generally a neutral or slightly negative rating.
デフォルトの格付けは、一般的に中立またはわずかにマイナスの格付けです。
The likelihood that a user will view each successive item is described with an exponential decay function, where the strength of the decay is described by a half-life parameter.
ユーザーが連続したアイテムを閲覧する可能性は、指数関数的な減衰関数で記述され、減衰の強さは半減期パラメータで記述される。
The expected utility (Ra) is shown in Eq.
期待効用（Ra）は、式（1）で示される。
(8).
(8).
ra, j represents the rating of user a on item j of the ranked list, d is the default rating, and α is the half-life.
ra、jはランクリストのアイテムjに対するユーザーaの評価、dはデフォルトの評価、αは半減期を表しています。
The half-life is the rank of the item on the list such that there is a 50% chance that the user will view that item.
半減期とは、ユーザーがそのアイテムを閲覧する確率が50%になるようなリスト上のアイテムのランクを指します。
Breese et al.
Breeseら。
[1998] used a half-life of 5 for his experiments, but noted that using a half-life of 10 caused little additional sensitivity of results.
[1998]では、半減期を5として実験を行ったが、半減期を10にすると、結果の感度がほとんど上がらないことを指摘した。

$$
\tag{8}
$$

The overall score for a dataset across all users (R) is shown in Eq.
全ユーザーを対象としたデータセットの総合スコア（R）は、式（1）で示される。
(9).
(9).
Rmax a is the maximum achievable utility if the system ranked the items in the exact order that the user ranked them.
Rmax aは、システムがユーザがランク付けした順番通りにアイテムをランク付けした場合に、達成可能な最大効用である。

$$
\tag{9}
$$

The half-life utility metric is best for tasks domains where there is an exponential drop in true utility (one could consider utility from a cost/benefit ratio analysis) as the search length increases, assuming that the half-life α and default vote d are chosen appropriately in the utility metric.
半減期の効用指標は、真の効用が指数関数的に低下するようなタスク領域に最適である（コストから効用を考えることもできる）。
The utility metric applies most of the weight to early items, with every successive rank having exponentially less weight in the measure.
実用性の指標は、初期のアイテムに最も重みがあり、ランクが上がるごとに指数関数的に重みが減っていきます。
To obtain high values of the metric, the first predicted rankings must consist of items rated highly by the user.
メトリックの高い値を得るためには、最初に予測される順位が、ユーザーによって高く評価されたアイテムで構成されている必要があります。
The downside is that if the true function describing the likelihood of accessing each rank is significantly different from the exponential used in the metric then the measured results may not be indicative of actual performance.
欠点は、各ランクにアクセスする可能性を表す真の関数が、指標に使用される指数と大きく異なる場合、測定結果が実際のパフォーマンスを示すものではない可能性があることです。
For example, if the user almost always searches 20 items into the ranked recommendation list, then the true likelihood function is a step function which is constant for the first 20 items and 0 afterwards..
例えば、ユーザがほとんど常に20個のアイテムをランク付けされた推薦リストに検索する場合、真の尤度関数は、最初の20個のアイテムに対して一定で、それ以降は0であるステップ関数となる。

The half-life utility metric may be overly sensitive in domains with binary user preferences where the user only requires that top recommendations be “good enough” or for user tasks such as Find All Good Items where the user wants to see all good items..
半減期ユーティリティは、ユーザが「十分に良い」ことを要求する二項対立のユーザープレファレンスを持つドメインや、ユーザが全ての良いアイテムを見たいと思うFind All Good Itemsのようなユーザタスクでは、過度に敏感である可能性があります。

There are other disadvantages to the half-life utility metric.
半減期の効用指標には、他にもデメリットがあります。
First, weak orderings created by the system will result in different possible scores for the same system ranking.
まず、システムによって作成された弱い順序付けは、同じシステムランキングでも異なる可能性のあるスコアとなる。
Suppose the system outputs a recommendation list, with three items sharing the top rank.
例えば、3つのアイテムが上位にランクされた推薦リストが出力されたとします。
If the user rated those three items differently, then depending on what order the recommender outputs those items, the metric could have very different values (if the ratings were significantly different)..
もし、その3つの項目の評価が異なれば、レコメンダーがどのような順番でその項目を出力するかによって、（評価が大きく異なれば）メトリックは大きく異なる値になる可能性があります。

Second, due to the application of the max() function in the metric (Eq.
第二に、メトリックにmax()関数を適用しているため（Eq.
(8)), all items that are rated less than the default vote contribute equally to the score.
(8)）、デフォルトの投票より低い評価を受けたすべての項目が等しくスコアに寄与する。
Therefore, an item occurring at system rank 2 that is rated just slightly less than the default rating (which usually indicates ambivalence) will have the same effect on the utility as an item that has the worst possible rating.
したがって、システムランク2で発生した項目のうち、デフォルトの評価（通常、両価性を示す）よりもわずかに低い評価を受けた項目は、最悪の評価を受けた項目と同じ効果を効用に及ぼすことになります。
The occurrence of extremely wrong predictions in the high levels of a system ranking can undermine the confidence of the user in the system.
システムランキングの上位で極端に間違った予測が発生すると、システムに対するユーザーの信頼が損なわれてしまう。
Metrics that penalize such mistakes more severely are preferred..
このようなミスをより厳しく罰するメトリクスが好まれる。

To summarize, the half-life utility metric is the only one that we have examined that takes into account non-uniform utility.
要約すると、半減期の効用指標は、我々が検討した中で唯一、非均一な効用を考慮した指標である。
Thus, it could be appropriate for evaluation of the Find Good Items tasks in domains such nonuniform utility is believed to exist.
そのため、実用性が一様でないと考えられる領域での「良いものを探す」タスクの評価に適している可能性がある。
On the other hand, it has many disadvantages, in particular when considering standardization across different researchers.
一方で、特に異なる研究者間での標準化を考えた場合、多くのデメリットがあります。
Different researchers could use significantly different values of alpha or the default vote—making it hard to compare results across researchers and making it easy to manipulate results.
研究者によってα値やデフォルトの投票値が大きく異なるため、研究者間の比較が難しく、結果の操作がしやすくなります。
Furthermore, the half-life parameter is unlikely to be the same for all users (different users need/desire different numbers of results)..
さらに、半減期パラメータは、すべてのユーザーで同じになるとは考えにくい（ユーザーによって必要な

#### The NDPM Measure NDPMの施策。

NDPM was used to evaluate the accuracy of the FAB recommender system [Balabanov´ıc and Shoham 1997].
FABレコメンダーシステム[Balabanov´ıc and Shoham 1997]の精度評価には、NDPMを使用しました。
It was originally proposed by Yao [1995].
もともとはYao [1995]によって提案されたものです。
Yao developed NDPM theoretically, using an approach from decision and measurement theory.
ヤオは、決定論と測定論からのアプローチで、NDPMを理論的に発展させた。
NDPM stands for “normalized distance-based performance measure.” NDPM (Eq.
NDPMとは、"Normalized Distance-based Performance Measure "の略です。NDPM（Eq.
(10)) can be used to compare two different weakly ordered rankings.
(10)）は、2つの異なる弱順序のランキングを比較するために使用することができます。

$$
\tag{10}
$$

C−is the number of contradictory preference relations between the system ranking and the user ranking.
C-は、システムランキングとユーザーランキングの間で矛盾する選好関係の数である。
A contradictory preference relation happens when the system says that item 1 will be preferred to item 2, and the user ranking says the opposite.
システムが「アイテム1がアイテム2より優先される」と言いながら、ユーザーランキングが「その逆」と言う場合、矛盾した選好関係が発生する。
Cu is the number of compatible preference relations, where the user rates item 1 higher than item 2, but the system ranking has item 1 and item 2 at equal preference levels.
Cuは、ユーザーがアイテム1をアイテム2より高く評価しているが、システムランキングではアイテム1とアイテム2が同じ優先度になっているような、両立する優先関係の数である。
Ci is the total number of “preferred” relationships in the user’s ranking (i.e., pairs of items rated by the user for which one is rated higher than the other).
Ciは、ユーザーのランキングにおける「好ましい」関係の総数（すなわち、ユーザーが評価した項目のうち、一方が他方よりも高く評価されているものの組）である。
This metric is comparable among different datasets (it is normalized), because the numerator represents the distance, and the denominator represents the worst possible distance..
この指標は、分子が距離を表し、分母が最悪の距離を表すため、異なるデータセット間で比較可能です（正規化されています）。

NDPM is similar in form to the Spearman and Kendall’s Tau rank correlations, but provides a more accurate interpretation of the effect of tied user ranks.
NDPMはSpearmanやKendall's Tauのランク相関と形式が似ていますが、結びついたユーザーランクの効果をより正確に解釈することができます。
However, it does suffer from the same interchange weakness as the rank correlation metrics (interchanges at the top of the ranking have the same weight as interchanges at the bottom of the ranking)..
しかし、順位相関の指標と同じ交流の弱点（ランキングの上位の交流と下位の交流が同じ重みを持つ）を抱えているのが現状です。

Because NDPM does not penalize the system for system orderings when the user ranks are tied, NDPM may be more appropriate than the correlation metrics for domains where the user is interested in items that are “good-enough.” User ratings could be transformed to binary ratings (if they were not already), and NDPM could be used to compare the results to the system ranking..
NDPMは、ユーザーランクが同点である場合に、システムの順序付けにペナルティを与えないので、ユーザーが "good-enough "なアイテムに興味を持つドメインでは、相関メトリクスよりもNDPMがより適切かもしれません。ユーザーの評価を（まだそうでなければ）二値評価に変換し、その結果をシステムランキングと比較するためにNDPMを使用することができる。

As NDPM only evaluates ordering and not prediction value, it is not appropriate for evaluating tasks where the goal is to predict an actual rating value..
NDPMは順序のみを評価し、予測値を評価しないため、実際の評価値を予測することを目的としたタスクの評価には適さない。

### An Empirical Comparison of Evaluation Metrics. 評価指標の実証的な比較.

After conceptually analyzing the advantages and disadvantages, a natural question is: “which of these advantages and disadvantages have a significant effect on the outcome of a metric?” In an effort to quantify the differences between the above-mentioned evaluation metrics, we computed a set of different evaluation metrics on a set of results from different variants of a collaborative filtering prediction algorithm and examined the extent to which the different evaluation metrics agreed or disagreed..
メリットとデメリットを概念的に分析した後、自然な疑問として、"これらのメリットとデメリットのうち、どの評価指標の結果に大きな影響を与えるのか？"がある。上記の評価指標の違いを定量化するために、協調フィルタリング予測アルゴリズムの異なる亜種の結果一式に対して異なる評価指標を計算し、異なる評価指標がどの程度一致するか、あるいは一致しないかを調べました。

We examined the predictions generated by variants of a classic nearestneighbor collaborative filtering algorithm formed by perturbing many different key parameters.
我々は、古典的な最近接協調フィルタリングアルゴリズムの様々な主要なパラメータに摂動を与えることによって生成される予測値を調べた。
We used this data for examination of evaluation metrics.
このデータを使って、評価指標の検討を行いました。
There were 432 different variants of the algorithm tested, resulting in the same number of sets of predictions.
432種類のアルゴリズムがテストされ、その結果、同じ数の予測セットが得られました。
The parameters of the algorithms that were varied to produce the different results included: size of neighborhood, similarity measure used to compute closeness of neighbors, threshold over which other users were considered neighbors, and type of normalization used on the ratings.
近傍のサイズ、近接度を計算するための類似性尺度、他のユーザーを近傍とみなす閾値、評価に使用する正規化の種類など、異なる結果を得るためにアルゴリズムのパラメータを変化させた。
(see Herlocker et al.
(Herlockerら参照)。
[2002] for more information on the algorithm).
アルゴリズムの詳細については[2002]を参照）。

For each of these result sets, we computed mean absolute error, Pearson correlation, Spearman rank correlation, area underneath an ROC-4 and ROC-53 curve, the half-life utility metric, mean average precision at relevant documents and the NDPM metric.
これらの結果セットそれぞれについて、平均絶対誤差、Pearson相関、Spearman順位相関、ROC-4およびROC-53曲線下の面積、半減期効用指標、関連文書での平均平均精度、NDPM指標を計算した。
For several of the metrics, there are two different variants: overall and per-user.
いくつかの指標については、全体とユーザーごとの2種類のバリエーションがあります。
The difference between these two variants is the manner in which averaging was performed.
この2つのバリエーションの違いは、平均化の方法です。
In the overall case, predictions for all the users were pooled together into a single file and then sorted.
全体の場合、全ユーザーの予測値を1つのファイルにプールして、ソートしています。
Likewise, the ratings for those items were pooled into a single file and sorted.
同様に、それらの項目の評価を1つのファイルにプールし、ソートした。
A ranking metric was then applied once to compare those two files.
そして、その2つのファイルを比較するために、ランキングの指標を一度適用しました。
In the per-user case, predictions were computed for each user, and the ranking metric was computed for each user.
ユーザーごとの場合、予測値は各ユーザーごとに計算され、ランキング指標は各ユーザーごとに計算された。
Then the ranking metric was averaged over all users..
そして、ランキングの指標を全ユーザーで平均化した。

The experiment was performed with data taken from the MovieLens webbased movie recommender (www.movielens.org).
実験は、ウェブベースの映画レコメンダー「MovieLens」（www.movielens.org）から取得したデータで行いました。
The data were sampled from the data collected over a seven-month period from September 19th, 1997 through April 22nd, 1998.
1997年9月19日から1998年4月22日までの7ヶ月間に収集されたデータからサンプリングされたものです。
The data consisted of 100,000 movie ratings from 943 users on 1682 items.
データは、943人のユーザーが1682の項目に対して行った10万件の映画評価で構成されています。
Each user sampled had rated at least 20 items.
各ユーザーの評価は20項目以上でした。
For each of the users, 10 rated items are withheld from the training.
各ユーザーに対して、10個の評価項目が訓練から保留されます。
After training the system with all the other ratings, predictions are generated for the 10 withheld items.
他のすべての評価でシステムを学習させた後、保留された10個のアイテムについて予測を生成する。
Then the predictions were compared to the user’s ratings, and the list ranked by predictions was compared to the list ranked by user ratings.
そして、予測値とユーザーの評価を比較し、予測値でランク付けされたリストとユーザーの評価でランク付けされたリストを比較しました。
The data are freely available from www.grouplens.org, and we encourage researchers using other families of collaborative filtering algorithms to replicate this work using the same data set for comparability..
データは www.grouplens.org から自由に入手できます。他の協調フィルタリングアルゴリズムのファミリーを使用している研究者は、比較のために同じデータセットを使用してこの研究を複製することをお勧めします。

This analysis is performed on a single family of algorithms on a single dataset, so the results should not be considered comprehensive.
この分析は、1つのデータセットで1つのアルゴリズムファミリーを対象に行われたものであり、その結果は包括的なものと考えるべきではありません。
However, we believe that the results show evidence of relationships between the metrics that should be investigated further.
しかし、この結果は、さらに調査すべき指標間の関係の証拠を示していると考えています。
Our goal is not to provide a deep investigation of the empirical results, which would constitute a entire article by itself..
しかし、このような経験的な結果については、それだけで1つの論文になるような、深い考察をすることが目的ではありません。

Figure 3 is a scatter plot matrix showing an overview of all the results.
図3は、すべての結果の概要を示す散布図マトリクスである。
Each cell of the matrix represents a comparison between two of the metrics.4 Each point of the scatter plot represents a different variant of the recommender algorithm.
散布図の各ポイントは、レコメンダーアルゴリズムの異なるバリエーションを表しています。
In the following paragraphs (and figures), we will look more closely at subsets of the results..
以下の段落（および図）では、結果のサブセットについてより詳しく見ていきます。

In analyzing the data in Figure 3, we notice that there is very strong linear agreement among different subsets of the metrics tested.
図3のデータを分析すると、テストしたメトリクスの異なるサブセット間で、非常に強い線形一致があることに気づきます。
One subset with strong agreement includes the per-user correlation metrics and mean average precision.
強い一致を示すサブセットとして、ユーザーごとの相関指標と平均平均精度がある。
This subset is shown expanded in Figure 4.
このサブセットは、図4に拡大して示されています。
For the data and algorithms tested, Figure 4 suggests that rank correlations do not provide substantially different outcomes from each other or from Pearson correlation.
テストしたデータとアルゴリズムについて、図4は、ランク相関が互いに、あるいはピアソン相関と実質的に異なる結果を提供しないことを示唆している。
Figure 4 also indicates that mean average precision is highly correlated with the peruser correlation metrics..
また、図4から、平均平均精度は、ユーザ相関指標と高い相関があることがわかる。

Figure 5 shows a different, mutually exclusive subset of the evaluation metrics that includes the per-user Half-life Utility metric as well as the per-user ROC-4 and ROC-5 area metrics.
図5は、評価指標の異なる、相互に排他的なサブセットを示し、ユーザーごとの半減期ユーティリティ指標と、ユーザーごとのROC-4およびROC-5エリア指標を含んでいます。
We can see that these three metrics are strongly correlated, even more so that the previous subset of metrics..
この3つの指標には強い相関があり、前の指標のサブセットよりもさらに強い相関があることがわかります。

The final subset that we shall examine contains all the metrics that are computed overall as opposed to the metrics depicted in Figures 4 and 5, which are per-user.
図4と図5に示したユーザーごとのメトリクスとは対照的に、全体として計算されるすべてのメトリクスが含まれています。
Figure 6 shows that the metrics computed overall (mean absolute error,5 Pearson Correlation, and ROC-4) have mostly linear relationships..
図6から、全体として計算された指標（平均絶対誤差、5 ピアソン相関、ROC-4）は、ほぼ直線的な関係であることがわかる。

To bring the analysis back to the entire set of metrics, we have chosen one representative from each of the subsets that were depicted in Figures 4– 6.
図4-6に示したサブセットから、それぞれ1つずつ代表的なものを選び、メトリクスのセット全体に分析を戻しました。
Figure 7 shows a comparison between these representatives.
図7は、これらの代表的なものを比較したものです。
Pearson peruser represents the subset of per-user metrics and Mean Average Precision that are depicted in Figure 4.
Pearson peruserは、図4に描かれているユーザーごとのメトリクスとMean Average Precisionのサブセットを表しています。
ROC-4 per user represents the ROC-4, ROC5, and Half-life Utility metrics, all averaged per-user.
ROC-4 per user は、ROC-4、ROC5、Half-life Utility の指標を、すべてユーザーごとに平均したものです。
Mean Absolute Error represents the subset of overall metrics depicted in Figure 6.
平均絶対誤差は、図6に描かれた全体的なメトリクスのサブセットを表しています。
We can see that while there is strong agreement within each subset of algorithms (as seen in Figures 4–6), there is little agreement between algorithms from different subsets.
各アルゴリズムのサブセット内では強い一致が見られるが（図4～6）、異なるサブセットのアルゴリズム間ではほとんど一致が見られないことがわかる。
Algorithms averaged per-user do not seem to agree with algorithms averaged overall.
ユーザーごとに平均化されたアルゴリズムは、全体で平均化されたアルゴリズムと一致しないようです。
The ROC-4, ROC-5, and Half-life Utility metrics averaged per user do not agree with the other metrics that are averaged per user..
ユーザーごとに平均化されたROC-4、ROC-5、半減期ユーティリティの指標は、ユーザーごとに平均化された他の指標と一致しない。

Several interesting observations can be taken from that data in Figures 3–7..
図3-7は、そのデータからいくつかの興味深い考察を得ることができます。

—Metrics that are computed per user and then averaged provide different rankings of algorithms that metrics that are computed overall..
-ユーザーごとに計算され、平均化された指標は、全体的に計算された指標とは異なるアルゴリズムのランキングを提供します。

—There doesn’t appear to be a substantial difference between the Pearson correlation metrics and rank correlation metrics, although a good number of outliers exist..
-ピアソン相関指標と順位相関指標の間には、かなりの数の外れ値が存在するが、実質的な差はないようだ。

—Mean Average Precision provides roughly the same ordering of algorithms as the correlation metrics that are computed per user and averaged..
-平均平均精度は、ユーザーごとに計算され平均化された相関メトリックとほぼ同じアルゴリズムの順序を提供します。

—The ROC area metrics (ROC-4 and ROC-5) when computed overall perform very similar to the other overall metrics, such as Mean Absolute Error and Pearson Overall.
-ROCエリアメトリクス（ROC-4、ROC-5）は、全体的に計算すると、平均絶対誤差やピアソンオーバーオールなどの他の全体的なメトリクスと非常によく似た性能を示す。
However, when they are averaged per user, they provide different rankings of algorithms than other per-user metrics, with the exception of the Half-life Utility metric.
しかし、これらをユーザーごとに平均化すると、Half-life Utility指標を除いて、他のユーザーごとの指標とは異なるアルゴリズムのランキングを提供します。

—The Half-life utility metric, which is averaged per user provides different rankings of algorithms than the per-user correlation metrics and mean average precision, yet produces rankings similar to the ROC area metrics when computed per user..
-ユーザーごとに平均化されたHalf-life効用指標は、ユーザーごとの相関指標や平均平均精度とは異なるアルゴリズムのランキングを提供しますが、ユーザーごとに計算するとROC領域指標と同様のランキングを生成します。

In support of these observations, Schein et al.
これらの観察結果を裏付けるように、Schein et al.
[2002] have also observed that overall metrics and per-user metric can provide conflicting results.
また、[2002]は、全体的なメトリクスとユーザーごとのメトリクスが相反する結果を提供する可能性があることを確認しています。
They observed differences between an overall ROC (which they call Global ROC) and a per-user ROC (which they call a Customer ROC)..
彼らは、全体的なROC（Global ROCと呼ぶ）とユーザーごとのROC（Customer ROCと呼ぶ）に違いがあることを確認した。

One should hold in mind that these empirical results, while based on numerous data points, all represent perturbations of the same base algorithm.
これらの経験的な結果は、多くのデータポイントに基づくとはいえ、すべて同じ基本アルゴリズムの摂動であることを念頭に置く必要があります。
The range in rank scores do not vary that much.
ランクスコアの幅は、それほど大きくは変わりません。
Future work could extend the comparison of these evaluation metrics across significantly different recommendation algorithms..
将来的には、これらの評価指標を大幅に異なる推薦アルゴリズムで比較できるように拡張することも可能である。

## 2 Accuracy Metrics—Summary 2 Accuracy Metrics-Summary.

We have examined a variety of accuracy evaluation metrics that have been used before to evaluate collaborative filtering systems.
これまで協調フィルタリングシステムの評価に使われてきた様々な精度評価指標を検証しました。
We have examined them both conceptually and empirically.
それらを概念的、実証的に検証しています。
The conceptual analysis suggests that certain evaluation metrics are more appropriate for certain tasks.
概念的な分析では、特定の評価指標が特定のタスクに適していることが示唆されています。
Based on this analysis, there appears to be a potential for inaccurate measurement of certain tasks if the wrong metric is used.
この分析によると、誤った指標を用いると、特定のタスクの測定が不正確になる可能性があるようです。
Our empirical analysis of one class of collaborative filtering algorithm demonstrates that many of the argued conceptual mismatches between metrics and tasks do not manifest themselves when evaluating the performance of predictive algorithms on movie rating data.
あるクラスの協調フィルタリングアルゴリズムの実証分析では、映画評価データに対する予測アルゴリズムの性能を評価する際に、メトリクスとタスクの間で議論された概念的なミスマッチの多くが顕在化しないことが示された。
On the other hand, we were able to demonstrate that different outcomes in evaluation can be obtained by carefully choosing evaluation metrics from different classes that we identified..
一方、識別した異なるクラスから評価指標を注意深く選択することで、評価において異なる結果が得られることを示すことができた。

The empirical analysis that we have performed represents only a sample— one class of algorithm and one dataset.
今回実施した実証分析は、1クラスのアルゴリズムと1つのデータセットというサンプルに過ぎない。
A TREC-like environment for collaborative filtering algorithms, with different tracks (and datasets) for different tasks would provide algorithmic results from many different algorithms and systems.
協調フィルタリングアルゴリズムのためのTRECのような環境では、タスクごとに異なるトラック（およびデータセット）が用意されており、多くの異なるアルゴリズムやシステムによるアルゴリズム結果を提供することができます。
These results would provide valuable data for the further verification of the properties of metrics discussed in this section..
この結果は、本節で取り上げたメトリクスの特性をさらに検証するための貴重なデータとなるだろう。

A final note is that a similar (but very brief) analysis has been performed on metrics for evaluating text retrieval systems.
最後に、テキスト検索システムを評価するためのメトリクスについても、同様の（しかし非常に簡潔な）分析が行われていることを紹介する。
Voorhees and Harman [1999] report the strength of correlations computed between different evaluation metrics used in the TREC-7 analysis.
Voorhees and Harman [1999]は、TREC-7分析で使用された異なる評価指標間で計算された相関の強さを報告しています。
Instead of showing scatterplots relating metrics, they computed correlation values between different metrics.
メトリクスを関連付けた散布図を示す代わりに、異なるメトリクス間の相関値を計算した。
Their results focused primarily on different variants of precision/recall that we do not discuss here.
彼らの成果は、主に精度の異なるバリエーションに焦点を当てたものです。
As the domain features of the document retrieval context are significantly different from the recommender systems context, we do not attempt to incorporate their results here..
文書検索とレコメンダーシステムではドメイン特性が大きく異なるため、ここではその結果を取り入れることはしない。

#  Beyond Accuracy アキュラシーを超える

There is an emerging understanding that good recommendation accuracy alone does not give users of recommender systems an effective and satisfying experience.
推薦の精度が高いだけでは、推薦システムの利用者に効果的で満足のいく体験を与えることはできないという理解が広まりつつあります。
Recommender systems must provide not just accuracy, but also usefulness.
レコメンダーシステムは、正確さだけでなく、有用性も提供する必要があります。
For instance, a recommender might achieve high accuracy by only computing predictions for easy-to-predict items—but those are the very items for which users are least likely to need predictions.
例えば、レコメンダーは、予測しやすい項目についてのみ予測計算を行うことで高い精度を達成することができますが、そのような項目は、ユーザーが予測を必要とする可能性が最も低いものです。
Further, a system that always recommends very popular items can promise that users will like most of the items recommended—but a simple popularity metric could do the same thing.
また、常に人気の高いアイテムを推薦するシステムは、ユーザーが推薦されたアイテムのほとんどを気に入ることを約束することができますが、単純な人気指標でも同じことが可能です。
(Recommending only very unpopular items and promising that users won’t like them is even less useful.).
(非常に不人気なものだけを推薦し、ユーザーがそれを好まないことを約束することは、さらに役に立ちません)。

By recalling that performance of a recommender system must be evaluated with respect to specific user tasks and the domain context, we can deepen the argument for moving beyond accuracy.
推薦システムの性能は、特定のユーザーのタスクとドメインのコンテキストに関して評価されなければならないことを思い起こすことで、正確さを超えるための議論を深めることができます。
For example, consider the Find Good Items task in a domain where the user wants to select a single item whose value exceeds a threshold—and suppose that the system follows a typical strategy of offering a relatively small, ordered set of recommendations.
例えば、ユーザーが閾値を超えるアイテムを1つだけ選びたいというドメインにおける「良いアイテムを探す」タスクを考え、システムが比較的小さな、順序付けられた推奨セットを提供するという典型的な戦略に従っているとする。
In this case, it may be best for the system to try to generate a few highly useful recommendations, even at the risk of being off the mark with the others.
このような場合、システムは、他が的外れであることを覚悟の上で、有用性の高いいくつかの推薦文を生成するよう努めるのがベストかもしれません。
If the supporting information about the items is good enough, then the user will be able to identify the best recommendation quickly.
アイテムに関するサポート情報が十分であれば、ユーザーは最適なレコメンドを素早く特定することができます。
Turpin and Hersh’s [2001] study of search engines provides support for this position.
Turpin and Hersh [2001]による検索エンジンの研究は、この立場を支持するものである。
Their subjects were divided into two sets, with half using a simple, baseline search engine, and the others using a state of the art engine.
被験者を2組に分け、半数はシンプルなベースラインの検索エンジンを使い、他の半数は最新の検索エンジンを使いました。
While the latter returned significantly more accurate results, subjects in both cases were about as successful at completing their tasks (e.g., finding the answer to a question such as “Identify a set of Roman ruins in present-day France”).
後者の方がより正確な結果を得ることができましたが、どちらの場合も、被験者は自分の課題（例えば、「現在のフランスにあるローマ時代の遺跡を特定せよ」というような質問に対する答えを見つけること）を達成することにほぼ成功したのです。
Turpin and Hersh believed that this showed that the difference between (say) 3 and 5 relevant documents in a list of 10 documents was not really material to the user; nor did it matter much if the relevant documents were right at the top of the list or a bit further down.
ターピンとハーシュは、10個の文書リストの中で、例えば3個の文書と5個の文書の違いは、ユーザーにとってあまり重要ではない、また関連文書がリストの一番上にあるか少し下にあるかはあまり重要ではないことを示すものだと考えた。
Subjects were able to scan through the titles and brief synopses and quickly locate a relevant document..
被験者は、タイトルと簡単な概要に目を通し、関連する文書を素早く探し出すことができました。

This section considers measures of recommender system usefulness that move beyond accuracy to include suitability of the recommendations to users.
ここでは、推薦システムの有用性を測る尺度として、正確さだけでなく、ユーザーに対する推薦の適切さも含めて考える。
Suitability includes coverage, which measures the percentage of a dataset that the recommender system is able to provide predictions for; confidence metrics that can help users make more effective decisions; the learning rate, which measures how quickly an algorithm can produce good recommendations; and novelty/serendipity, which measure whether a recommendation is a novel possibility for a user.
適性には、推薦システムが予測を提供できるデータセットの割合を示すカバレッジ、ユーザーがより効果的な意思決定を行うのに役立つ信頼性の指標、アルゴリズムがどれだけ早く良い推薦を生成できるかを示す学習率、新規性などが含まれます。
Finally, we explore measures of recommender system utility based on user satisfaction with and performance on a system..
最後に、ユーザーのシステムに対する満足度やパフォーマンスから、レコメンダーシステムの有用性を評価する方法を検討する。

## Coverage カバレッジ

The coverage of a recommender system is a measure of the domain of items in the system over which the system can form predictions or make recommendations.
レコメンダーシステムのカバレッジとは、システムが予測や推奨を行うことができる、システム内のアイテムの領域を示す尺度である。
Systems with lower coverage may be less valuable to users, since they will be limited in the decisions they are able to help with.
カバー率が低いシステムは、ユーザーにとって、助けられる判断が限定されるため、価値が低くなる可能性があります。
Coverage is particularly important for the Find All Good Items task, since systems that cannot evaluate many of the items in the domain cannot find all of the good items in that domain.
ドメイン内の多くのアイテムを評価できないシステムは、そのドメイン内のすべての良いアイテムを見つけることができないため、カバレッジはFind All Good Itemsタスクで特に重要です。
Coverage is also very important for the Annotate In Context task, as no annotation is possible for items where no prediction is available.
また、Annotate In Contextタスクでは、予測値がない項目にはアノテーションができないため、カバレッジは非常に重要です。
Coverage can be most directly defined on predictions by asking “What percentage of items can this recommender form predictions for?” This type of coverage is often called prediction coverage.
カバレッジは、予測について最も直接的に定義することができます。"このレコメンダーは、何パーセントのアイテムについて予測を形成することができますか？"と問うことによって。このタイプのカバレッジは、しばしば予測カバレッジと呼ばれます。
A different sort of coverage metric can be formed for recommendations, more along the lines of “What percentage of available items does this recommender ever recommend to users?” For an e-commerce site, the latter form of coverage measures how much of the merchant’s catalog of items are recommended by the recommender; for this reason we’ll call it catalog coverage..
レコメンデーションについては、「このレコメンダーは、利用可能なアイテムの何パーセントをユーザーに推奨しているのか」というような、別の種類のカバレッジメトリクスを形成することができます。ECサイトの場合、後者のカバレッジは、レコメンダーによって推奨された商品のカタログのうち、どの程度が推奨されたかを測定するものです。

Coverage has been measured by a number of researchers in the past [Good et al.
カバレッジは、過去に多くの研究者によって測定されてきた[Good et al.
1999, Herlocker et al.
1999年、Herlocker et al.
1999, Sarwar et al.
1999, Sarwar et al.
1998].
1998].
The most common measure for coverage has been the number of items for which predictions can be formed as a percentage of the total number of items.
カバレッジの指標としては、予測形成が可能な項目数が全項目数に占める割合が最も一般的であった。
The easiest way to measure coverage of this type is to select a random sample of user/item pairs, ask for a prediction for each pair, and measure the percentage for which a prediction was provided.
この種のカバレッジを測定する最も簡単な方法は、ユーザーから無作為にサンプルを選択することです。
Much as precision and recall must be measured simultaneously, coverage must be measured in combination with accuracy, so recommenders are not tempted to raise coverage by making bogus predictions for every item..
精度と再現性を同時に測定する必要があるのと同様に、カバー率も精度と組み合わせて測定する必要があり、レコメンダーがすべてのアイテムについて偽の予測をすることでカバー率を上げる誘惑に駆られることはありません。

An alternative way of computing coverage considers only coverage over items in which a user may have some interest.
カバレッジの計算方法として、ユーザーが何らかの関心を持つ可能性のある項目に対するカバレッジのみを考慮する方法もあります。
Coverage of this type is not usually measured over all items, but only over those items a user is known to have examined.
このタイプのカバレッジは、通常、すべてのアイテムについて測定されるのではなく、ユーザーが調べたことがあるとわかっているアイテムについてのみ測定されます。
For instance, when the predictive accuracy is computed by hiding a selection of ratings and having the recommender compute a prediction for those ratings, the coverage can be measured as the percentage of covered items for which a prediction can be formed.
例えば、評価の選択を非表示にして、それらの評価に対する予測をレコメンダーに計算させることによって予測精度を計算する場合、カバー率は、予測を形成することができるカバー項目の割合として測定することができる。
The advantage of this metric is it may correspond better to user needs, since it is not important whether a system can recommend items a user has no interest in.
この指標は、ユーザーが興味のないものを推薦できるかどうかは重要ではないため、よりユーザーのニーズに対応できる可能性があるのが利点です。
(For instance, if a user has no interest in particle physics, it is not a disadvantage that a particular recommender system for research papers cannot form predictions for her about particle physics.).
(例えば、あるユーザーが素粒子物理学に興味がない場合、ある研究論文推薦システムが素粒子物理学に関する予測を立てられないことはデメリットとはならない）。

Catalog coverage, expressed as the percentage of the items in the catalog that are ever recommended to users, has been measured less often.
カタログに掲載されているアイテムのうち、ユーザーに推薦されたことのあるアイテムの割合で表される「カタログカバレッジ」は、これまであまり測定されてきませんでした。
Catalog coverage is usually measured on a set of recommendations formed at a single point in time.
カタログのカバー率は、通常、ある時点で形成された推薦文のセットで測定されます。
For instance, it might be measured by taking the union of the top 10 recommendations for each user in the population.
例えば、母集団に属する各ユーザーの推奨度トップ10の和を取ることで測定することができる。
Similarly to all coverage metrics, this metric distorts if it is not considered in combination with accuracy.
すべてのカバレッジメトリクスと同様に、このメトリクスは、精度と組み合わせて考慮しないと歪む。
For instance, if there is an item in the catalog that is uninteresting to all users, a good algorithm should never recommend it, leading to lower coverage—but higher accuracy..
例えば、カタログの中にすべてのユーザーにとって興味のないアイテムがあった場合、優れたアルゴリズムはそのアイテムを推奨しないはずで、カバー率は低くなりますが、精度は高くなります。

We know of no perfect, general coverage metric.
私たちは、完璧で一般的なカバレッジの指標を知りません。
Such a metric would have the following characteristics: (1) It would measure both prediction coverage and catalog coverage; (2) For prediction coverage it would more heavily weight items for which the user is likely to want predictions; (3) There would be a way to combine the coverage measure with accuracy measures to yield an overall “practical accuracy” measure for the recommender system.
(1)予測カバレッジとカタログカバレッジの両方を測定する。(2)予測カバレッジでは、ユーザーが予測を必要とする可能性の高い項目をより重視する。(3)カバレッジ測定と精度測定を組み合わせて、推薦システムの全体的な「実用精度」測定とする方法が存在する。
Recommender systems researchers must continue to work to develop coverage metrics with these properties.
リコメンダーシステムの研究者は、このような特性を持つカバレッジメトリクスの開発に今後も取り組んでいかなければならない。
In the meantime, we should continue to use the best available metrics, and it is crucial that we continue to report the coverage of our recommender systems.
その間、私たちは利用可能な最良の指標を使い続けるべきであり、私たちの推薦システムのカバレッジを報告し続けることが極めて重要である。
Best practices are to report the raw percentage of items for which predictions can be formed, and to also report catalog coverage for recommender algorithms.
ベストプラクティスは、予測を形成することができるアイテムの生の割合を報告することであり、レコメンダーアルゴリズムのカタログカバレッジも報告することです。
Where practical, these metrics should be augmented with measures that more heavily weight likely items.
現実的であれば、これらの指標は、可能性の高い項目をより重視した指標で補強する必要がある。
These metrics should be considered experimental, but will eventually lead to more useful coverage metrics.
これらのメトリクスは実験的なものと考えるべきですが、いずれはより有用なカバレッジメトリクスにつながるでしょう。
Comparing recommenders along these dimensions will ensure that new recommenders are not achieving accuracy by “cherry-picking” easy-to-recommend items, but are providing a wide range of useful recommendations to users..
このような次元でレコメンダーを比較することで、新しいレコメンダーが、レコメンドしやすいアイテムを「選んで」精度を上げるのではなく、ユーザーに幅広く役立つレコメンドを提供することができるようになるのです。

## Learning Rate 学習率

Collaborative filtering recommender systems incorporate learning algorithms that operate on statistical models.
協調フィルタリング・レコメンダーシステムは、統計的なモデルで動作する学習アルゴリズムを組み込んでいます。
As a result, their performance varies based on the amount of learning data available.
そのため、利用可能な学習データの量に応じて、その性能は変化します。
As the quantity of learning data increases, the quality of the predictions or recommendations should increase.
学習データの量が増えれば、予測や推薦の質も上がるはずです。
Different recommendation algorithms can reach “acceptable” quality of recommendations at different rates.
推薦アルゴリズムが異なれば、推薦の「許容」品質に到達する速度も異なる。
Some algorithms may only need a few data points to start generating acceptable recommendations, while others may need extensive data points.
アルゴリズムによっては、数個のデータポイントだけで許容できるレコメンデーションを生成し始めるものもあれば、膨大なデータポイントを必要とするものもあります。
Three different learning rates have been considered in recommender systems: overall learning rate, per item learning rate, and per user learning rate.
レコメンダーシステムでは、全体学習率、項目別学習率、ユーザー別学習率の3種類の学習率が考慮されている。
The overall learning rate is recommendation quality as a function of the overall number of ratings in the system (or the overall number of users in the system).
全体学習率とは、システム全体の評価数（またはシステム全体のユーザー数）の関数としての推薦品質のことです。
The per-item learning rate is the quality of predictions for an item as a function of the number of ratings available for that item.
項目ごとの学習率は、その項目で利用可能な評価の数の関数として、その項目の予測品質を示します。
Similarly the per-user learning rate is the quality of the recommendations for a user as a function of the number of ratings that user has contributed..
同様に、ユーザーごとの学習率は、そのユーザーが投稿した評価数の関数として、そのユーザーに対する推薦の質を表します。

The issue of evaluating the learning rates in recommender systems has not been extensively covered in the literature, although researchers such as Schein et al.
推薦システムにおける学習率の評価の問題は、Schein et al.のような研究者がいるものの、文献で広く取り上げられているわけではない。
[2001] have looked at evaluating the performance of recommender systems in “cold-start” situations.
[2001]では、「コールドスタート」状態での推薦システムの性能評価について検討しました。
“Cold-start” situations (commonly referred to as the startup problem) refer to situations where there are only a few ratings on which to base recommendations.
"コールドスタート "状況（一般にスタートアップ問題と呼ばれる）とは、推奨の根拠となる評価が少ない状況のことを指す。
Learning rates are non-linear and asymptotic (quality can’t improve forever), and thus it is challenging to represent them compactly.
学習率は非線形で漸近的（品質が永遠に向上しない）であるため、コンパクトに表現することは困難である。
The most common method for comparing the learning rates of different algorithms is to graph the quality versus the number of ratings (quality is usually accuracy)..
異なるアルゴリズムの学習率を比較する最も一般的な方法は、品質と評価数のグラフです（品質は通常、精度です）。

The lack of evaluation of learning rates is due largely to the size of the Eachmovie, MovieLens, and Jester datasets, all of which have a substantial number of ratings.
学習率の評価ができないのは、Eachmovie、MovieLens、Jesterの各データセットのサイズが大きく、いずれも相当数の評価を有しているためです。
As recommender systems spread into the more data-sparse domains, algorithm learning rates will become a much more significant evaluation factor..
レコメンダーシステムがよりデータスパースな領域に広がっていくにつれ、アルゴリズムの学習率はより重要な評価要素になっていきます。

## Novelty and Serendipity Novelty and Serendipity（ノベルティとセレンディピティ）。

Some recommender systems produce recommendations that are highly accurate and have reasonable coverage—and yet that are useless for practical purposes.
レコメンダーシステムの中には、精度が高く、カバー率も高いのに、実用に耐えないレコメンダーがあります。
For instance, a shopping cart recommender for a grocery store might suggest bananas to any shopper who has not yet selected them.
例えば、食料品店のショッピングカートのレコメンダーは、まだバナナを選択していない買い物客にバナナを勧めるかもしれません。
Statistically, this recommendation is highly accurate: almost everyone buys bananas.
統計的に見ても、この推奨は非常に正確で、ほとんどの人がバナナを買っています。
However, everyone who comes to a grocery store to shop has bought bananas in the past, and knows whether or not they want to purchase more.
しかし、スーパーに買い物に来る人は皆、過去にバナナを買ったことがあり、さらに買いたいかどうかもわかっています。
Further, grocery store managers already know that bananas are popular, and have already organized their store so people cannot avoid going past the bananas.
さらに、食料品店の店長は、バナナが人気であることをすでに知っており、人々がバナナの前を避けて通ることができないように、店内を整理している。
Thus, most of the time the shopper has already made a concrete decision not to purchase bananas on this trip, and will therefore ignore a recommendation for bananas.
したがって、ほとんどの場合、買い物客は今回の旅行でバナナを購入しないという具体的な決定をすでに下しているので、バナナの勧めを無視することになる。
Much more valuable would be a recommendation for the new frozen food the customer has never heard of—but would love.
それよりも、お客様が聞いたこともないような新しい冷凍食品を勧めるほうが、よほど価値があると思います。
A similar situation occurs in a music store around very well known items, like the Beatles’ famous White Album.
ビートルズのホワイトアルバムのような有名な商品を扱う楽器店でも、同じようなことが起こります。
Every music aficionado knows about the White Album—and most already own it.
音楽ファンなら誰もが知っている「ホワイトアルバム」は、ほとんどの人がすでに持っています。
Those who do not own it already have likely made a conscious decision not to own it.
すでに所有していない人は、意識的に所有しないことを決めている可能性が高いです。
A recommendation to purchase it is therefore unlikely to lead to a sale.
そのため、購入を勧めても、販売につながる可能性は低いです。
In fact, the White Album is an even worse recommendation than bananas, since most people only buy one copy of any given album.
実は、ホワイトアルバムはバナナよりもさらに悪い推奨品で、ほとんどの人はどのアルバムも1枚しか買わないからです。
Much more valuable would be a recommendation for an obscure garage band that makes music that this customer would love, but will never hear about through a review or television ad..
それよりも、この顧客が好きそうな音楽を作っている無名のガレージバンドを推薦するほうが、レビューやテレビ広告では知ることのできない価値があります。

Bananas in a grocery store, and the White Album in a music store, are examples of recommendations that fail the obviousness test.
八百屋のバナナ、楽器屋のホワイトアルバムは、自明性テストに失敗する推奨例である。
Obvious recommendations have two disadvantages: first, customers who are interested in those products have already purchased them; and second, managers in stores do not need recommender systems to tell them which products are popular overall.
1つ目は、その商品に興味のあるお客様がすでに購入されていること、2つ目は、店舗の管理者は、どの商品が全体的に人気があるのかを教えてくれるレコメンダーシステムを必要としていないことです。
They have already invested in organizing their store so those items are easily accessible to customers..
彼らはすでに、それらのアイテムがお客さまに届きやすいように、店内の整理整頓に投資しています。

Obvious recommendations do have value for new users.
新しいユーザーにとって、当たり前の推奨は価値があります。
Swearingen and Sinha [2001] found that users liked receiving some recommendations of items that they already were familiar with.
Swearingen and Sinha [2001]は、ユーザーがすでによく知っているアイテムの推薦を受けることを好むことを発見した。
This seems strange since such recommendations do not give users any new information.
このようなレコメンデーションは、ユーザーに新しい情報を与えないので、不思議な感じがします。
However, what they do accomplish is to increase user confidence in the system which is very important for the Find Credible Recommender task.
しかし、これらの課題によって達成されるのは、システムに対するユーザーの信頼性を高めることであり、これは「信頼できる推薦者を見つける」という課題にとって非常に重要です。
Additionally, users were more likely to say they would buy familiar items than novel ones.
さらに、ユーザーは、新規のものよりも身近なものを買うと答える傾向が強かった。
This contrasts with the situation when users were asked about downloading material for free (e.g., as is the case for many technical papers on the Web or for many mp3 music files).
これは、ユーザーが無料で素材をダウンロードした場合（例えば、ウェブ上の多くの技術論文や多くのmp3音楽ファイルがそうであるように）の状況と対照的である。
Here, users tended to prefer more novel recommendations.
ここでは、ユーザーはより斬新なレコメンドを好む傾向にありました。
The general lesson to take away is that a system may want to try to estimate the probability that a user will be familiar with an item.
一般的な教訓として、システムは、ユーザーがあるアイテムに精通している確率を推定することを試みるとよいでしょう。
For some tasks (and perhaps early in the course of user’s experience with the system), a greater number of familiar items should be recommended; for others, fewer or none should be included..
あるタスク（そしておそらくユーザーがシステムを使い始めて間もない頃）には、馴染みのあるアイテムをより多く推奨し、他のタスクには、より少ない、あるいは全く含まれないようにすることが望ましいと思います。

We need new dimensions for analyzing recommender systems that consider the “nonobviousness” of the recommendation.
推奨システムの分析には、推奨の「非自明性」を考慮した新しい次元が必要です。
One such dimension is novelty, which has been addressed before in information retrieval literature (see BaezaYates and Ribiero-Neto [1999] for a brief discussion of novelty in information retrieval).
そのような次元の1つが新規性であり、情報検索の文献で以前から取り上げられている（情報検索における新規性については、BaezaYates and Ribiero-Neto [1999] を参照）。
Another related dimension is serendipity.
また、関連する次元として、セレンディピティがあります。
A serendipitous recommendation helps the user find a surprisingly interesting item he might not have otherwise discovered.
セレンディピット・レコメンデーションは、ユーザーが他の方法では発見できなかったような、驚くほど興味深いアイテムを見つけるのに役立ちます。
To provide a clear example of the difference between novelty and serendipity, consider a recommendation system that simply recommends movies that were directed by the user’s favorite director.
新規性とセレンディピティの違いを分かりやすく説明するために、ユーザーの好きな監督の映画を推薦するだけのレコメンデーションシステムを考えてみましょう。
If the system recommends a movie that the user wasn’t aware of, the movie will be novel, but probably not serendipitous.
ユーザーが意識していなかった映画をシステムが推薦した場合、その映画は斬新ではあっても、おそらくセレンディピティではないでしょう。
The user would have likely discovered that movie on their own.
そのムービーは、ユーザーが自分で発見したものでしょう。
On the other hand, a recommender that recommends a movie by a new director is more likely to provide serendipitous recommendations.
一方、新しい監督の映画を推薦するレコメンダーは、セレンディピティな推薦をする可能性が高いです。
Recommendations that are serendipitous are by definition also novel.
セレンディピティ（偶然の産物）であるレコメンデーションは、定義上、新規性のあるものでもあります。
The distinction between novelty and serendipity is important when evaluating collaborative filtering recommender algorithms, because the potential for serendipitous recommendations is one facet of collaborative filtering that traditional content-based information filtering systems do not have.
新規性とセレンディピティの区別は、協調フィルタリング推薦アルゴリズムを評価する際に重要です。セレンディピティによる推薦の可能性は、従来のコンテンツベースの情報フィルタリングシステムにはない協調フィルタリングの一面であるからです。
It is important to note that the term, serendipity, is sometimes incorrectly used in the literature when novelty is actually being discussed..
なお、セレンディピティという言葉は、文献上、新規性が議論されているときに誤って使われていることがある。

Several researchers have studied novelty and serendipity in the context of collaborative filtering systems [Sarwar et al.
いくつかの研究者が協調フィルタリングシステムの文脈で新規性とセレンディピティを研究している [Sarwar et al.
2001].
2001].
They have modified their algorithms to capture serendipity by preferring to recommend items that are more preferred by a given user than by the population as a whole.
彼らは、セレンディピティを捉えるために、母集団全体よりも特定のユーザーによってより好まれるアイテムを優先的に推薦するようにアルゴリズムを変更しました。
A simple modification is to create a list of “obvious” recommendations, and remove the obvious ones from each recommendation list before presenting it to users.
簡単な修正としては、「明らかな」推薦リストを作成し、ユーザーに提示する前に各推薦リストから明らかなものを削除することです。
A disadvantage of this approach is that the list of obvious items might be different for each user, since each person has had different experiences in the past.
この方法の欠点は、各人が過去に経験したことが異なるため、明白な項目のリストが各ユーザーによって異なる可能性があることです。
An alternative would combine what is known about the user’s tastes with what is known about the community’s tastes.
別の方法として、ユーザーの嗜好について知られていることと、コミュニティの嗜好について知られていることを組み合わせる方法があります。
For instance, consider a hypothetical recommender that can produce a list of the probabilities for each item in the system that a given user will like the item.
例えば、システム内の各アイテムについて、与えられたユーザーがそのアイテムを気に入る確率のリストを作成できる仮想的なレコメンダーを考えてみよう。
A naive recommender would recommend the top 10 items in the list—but many of these items would be “obvious” to the customer.
素朴なレコメンダーは、リストの上位10位までを勧めるが、その多くはお客様にとって「当たり前」のことである。
An alternative would be to divide each probability by the probability that an average member of the community would like the item, and re-sort by the ratio.
また、それぞれの確率を、コミュニティの平均的なメンバーがそのアイテムを好む確率で割り、その比率で並べ替えるという方法もあります。
Intuitively, each ratio represents the amount that the given user will like the product more than most other users.
直感的には、各比率は、与えられたユーザーが他の多くのユーザーよりも製品を好きになる量を表しています。
Very popular items will be recommended only if they are likely to be exceptionally interesting to the present user.
人気のあるアイテムは、現在のユーザーにとって特別に興味深いものである場合にのみ推奨されます。
Less popular items will often be recommended, if they are particularly interesting to the present user.
人気のないアイテムでも、現在のユーザーにとって特に興味深いものであれば、お勧めすることがあります。
This approach will dramatically change the set of recommendations made to each user, and can help users uncover surprising items that they like..
このアプローチによって、各ユーザーへのレコメンドが大きく変わり、ユーザーが意外と好きなアイテムを発見することができます。

Designing metrics to measure serendipity is difficult, because serendipity is a measure of the degree to which the recommendations are presenting items that are both attractive to users and surprising to them.
セレンディピティは、レコメンデーションがユーザーにとって魅力的であり、かつ意外性のあるアイテムを提示している度合いを測る指標であるため、セレンディピティを測る指標の設計は困難である。
In fact, the usual methods for measuring quality are directly antithetical to serendipity.
実は、通常の品質を測る方法は、セレンディピティと真っ向から対立するものなのです。
Using the items users have bought in the past as indicators of their interest, and covering items one by one to see if the algorithm can rediscover them, rewards algorithms that make the most obvious recommendations..
ユーザーが過去に購入したアイテムを指標に、アルゴリズムが再発見できるアイテムを1つずつ取り上げていくことで、最もわかりやすいレコメンドをするアルゴリズムに報酬を与えます。

A good serendipity metric would look at the way the recommendations are broadening the user’s interests over time.
セレンディピティの指標としては、レコメンデーションが時間とともにユーザーの興味を広げていく様を見るのがよいでしょう。
To what extent are they for types of things she has never purchased before? How happy is she with the items recommended? (Does she return a higher percentage of them than other items?) Good novelty metrics would look more generally at how well a recommender system made the user aware of previously unknown items.
今まで購入したことのないタイプのものは、どの程度あるのでしょうか？推薦されたアイテムにどの程度満足しているのか？(他の商品よりも高い割合で返品しているか？)優れた新規性指標は、推薦システムがユーザーに未知の商品をどれだけ認識させることができたかをより一般的に見るものである。
To what extent does the user accept the new recommendations? We know of no systematic attempt to measure all of these facets of novelty and serendipity, and consider developing good metrics for novelty and serendipity an important open problem..
ユーザーはどの程度、新しい推奨を受け入れるのか？我々は、新規性とセレンディピティのこれらの側面をすべて測定する体系的な試みを知りません。そして、新規性とセレンディピティの優れた測定基準を開発することは重要な未解決問題であると考えています。

## Confidence コンフィデンス

Users of recommender systems often face a challenge in deciding how to interpret the recommendations along two often conflicting dimensions.
推薦システムの利用者は、しばしば相反する2つの次元に沿った推薦文をどのように解釈するかを決めるという課題に直面します。
The first dimension is the strength of the recommendation: how much does the recommender system think this user will like this item.
最初の次元は、推薦の強さです。推薦システムは、このユーザーがこのアイテムを好むとどの程度考えているかということです。
The second dimension is the confidence of the recommendation: how sure is the recommender system that its recommendation is accurate.
第二の次元は、推薦の信頼性です。推薦システムが、その推薦が正確であるとどれだけ確信しているかということです。
Many operators of recommender systems conflate these dimensions inaccurately: they assume that a user is more likely to like an item predicted five stars on a five star scale than an item predicted four stars on the same scale.
推薦システムの運用者の多くは、これらの次元を不正確に混同しています。彼らは、ユーザーが5つ星スケールで5つ星と予測されたアイテムを、同じスケールで4つ星と予測されたアイテムよりも好む可能性が高いと仮定しています。
That assumption is often false: very high predictions are often made on the basis of small amounts of data, with the prediction regressing to the mean over time as more data arrives.
この仮定はしばしば誤りです。非常に高い予測値が少量のデータに基づいて作られることが多く、データが増えるにつれて予測値は時間とともに平均値に回帰していきます。
Of course, just because a prediction is lower does not mean it is made based on more data!.
もちろん、予測が低くなったからといって、より多くのデータに基づいて作られているわけではありませんよ。

Another, broader, take on the importance of confidence derives from considering recommender systems as part of a decision-support system.
また、レコメンダーシステムを意思決定支援システムの一部として考えることで、信頼性の重要性をより広範に理解することができます。
The goal of the recommendation is to help users make the best possible decision about what to buy or use given their interests and goals.
レコメンデーションの目的は、ユーザーの興味や目的に合わせて、何を買うか、何を使うか、最善の決断をすることを支援することです。
Different short-term goals can lead to different preferences for types of recommendations.
短期的な目標が異なれば、推奨されるタイプの好みも異なる。
For instance, a user selecting a research paper about agent programming might prefer a safe reliable paper that gives a complete overview of the area, or a risky, thought-provoking paper to stimulate new ideas.
例えば、エージェントプログラミングに関する研究論文を選ぶユーザーは、その分野の全体像を示す安全で信頼できる論文と、新しいアイデアを刺激するリスクの高い示唆に富む論文を好むかもしれません。
The same user might prefer the overview paper if she is looking for a paper to reference in a grant proposal, or the thoughtprovoking paper if she is looking for a paper to read with her graduate students.
同じユーザーでも、助成金申請で参考にする論文を探すなら「概説書」を、大学院生と一緒に読む論文を探すなら「示唆に富む論文」を好むかもしれません。
How can the recommender system help her understand which recommendation will fit her current needs?.
レコメンダーシステムは、どのレコメンドが彼女の今のニーズに合うかを理解するのに、どのように役立てることができるでしょうか。

To help users make effective decisions based on the recommendations, recommender systems must help users navigate along both the strength and confidence dimension simultaneously.
ユーザーが推薦に基づいて効果的な意思決定を行うためには、推薦システムは、ユーザーが強さと確信の両方の次元に沿って同時にナビゲートすることを支援しなければなりません。
Many different approaches have been used in practice.
実際には、さまざまなアプローチが行われています。
E-commerce systems often refuse to present recommendations that are based on datasets judged too small.6 They want recommendations their customers can rely on.
Eコマースシステムは、小さすぎると判断されたデータセットに基づくレコメンデーションを提示することを拒否することが多い6。
The Movie Critic system provided explicit confidence visualization with each recommendation: a target with an arrow in it.
映画評論家のシステムは、推薦のたびに、矢印の入ったターゲットという明示的な信頼度の可視化を行いました。
The closer the arrow was to the center, the more confident the recommendation.
矢印が中心に近いほど、自信をもって推薦していることになります。
Herlocker et al.
Herlockerら。
[2000] explored a wide range of different confidence displays, to study which ones influenced users to make the right decision.
[2000]では、さまざまな信頼度表示を検討し、どのような表示がユーザーに正しい判断をさせるかを研究しました。
The study found that the choice of confidence display made a significant difference in users’ decisionmaking.
その結果、信頼度表示の選択によって、ユーザーの意思決定に大きな違いがあることがわかりました。
The best confidence displays were much better than no display.
最高の自信作の展示は、展示しないよりずっと良かった。
The worst displays actually worsened decision-making versus simply not displaying confidence at all..
自信のなさそうな顔をしているときと、自信のなさそうな顔をしているときとでは、最悪のほうが意思決定がうまくいくのです。

Measuring the quality of confidence in a system is difficult, since confidence is itself a complex multidimensional phenomenon that does not lend itself to simple one-dimensional metrics.
システムに対する信頼の質を測定することは、信頼自体が複雑な多次元的現象であり、単純な一次元の指標には適さないため、困難です。
However, recommenders that do not include some measure of confidence are likely to lead to poorer decision-making by users than systems that do include confidence.
しかし、信頼性の尺度を含まないレコメンダーは、信頼性を含むシステムよりも、ユーザーの意思決定を悪くしてしまう可能性が高いです。
If the confidence display shows users a quantitative or qualitative probability of how accurate the recommendation will be, the confidence can be tested against actual recommendations made to users.
信頼度表示が、推薦がどの程度正確であるかの定量的または定性的な確率をユーザーに示すものであれば、実際にユーザーに対して行われた推薦に対して信頼度をテストすることができます。
How much more accurate are the recommendations made with high confidence than those made with lower confidence? If the confidence display is directly supporting decisions, measuring the quality of the decisions made may be the best way to measure confidence.
高い信頼度で行われた推奨は、低い信頼度で行われた推奨よりも、どれだけ正確なのでしょうか。信頼度表示が意思決定を直接サポートするものであれば、意思決定の質を測定することが信頼度を測定する最良の方法かもしれません。
How much better is decision-making when users are shown a measure of confidence than when not?.
ユーザーに自信の指標を示した場合、そうでない場合と比べて、どれだけ意思決定がうまくいくのでしょうか。

## User Evaluation ユーザー評価

The metrics that we have discussed so far involve measuring variables that we believe will affect the utility of a recommender system to the user and affect the reaction of the user to the system.
これまで述べてきたメトリクスは、ユーザーに対するレコメンダーシステムの有用性に影響すると思われる変数や、システムに対するユーザーの反応に影響すると思われる変数を測定するものです。
In this section, we face the question of how to directly evaluate user “reaction” to a recommender system.
ここでは、推薦システムに対するユーザーの "反応 "をどのように直接評価するかという問題に直面します。
The full space of user evaluation is considerably more complex than the space of the previously discussed metrics, so rather than examining specific metrics in detail, we broadly review the user evaluation space and past work in user evaluation of recommender systems.
ユーザー評価の完全な空間は、先に述べたメトリクスの空間よりもかなり複雑であるため、特定のメトリクスを詳細に検討するのではなく、ユーザー評価の空間と推薦システムのユーザー評価に関する過去の研究を大まかに検討する。
In order to better understand the space of user evaluation methods, we begin by proposing a set of evaluation dimensions.
ユーザー評価手法の空間をよりよく理解するために、まず評価次元のセットを提案することから始めます。
We use these dimensions to organize our discussion of prior work, showing the types of knowledge that can be gained through use of different methods.
私たちは、これらの次元を用いて先行研究を整理し、異なる方法を使用することで得られる知識の種類を示す。
We close by summarizing what we consider the best current practices for user evaluations of recommender systems..
最後に、レコメンダーシステムのユーザー評価について、現在のベストプラクティスを要約して締めくくります。

### Dimensions for User Evaluation ユーザー評価のためのディメンション。

—Explicit (ask) vs.
-Explicit (ask) vs.
implicit (observe).
implicit（観察する）。
A basic distinction is between evaluations that explicitly ask users about their reactions to a system and those that implicitly observe user behavior.
基本的な区別として、システムに対するユーザーの反応を明示的に尋ねる評価と、ユーザーの行動を暗黙的に観察する評価とがある。
The first type of evaluation typically employs survey and interview methods.
第一のタイプの評価は、一般的に調査やインタビューの方法を採用しています。
The second type usually consists of logging user behavior, then subjecting it to various sorts of analyses..
2つ目のタイプは、通常、ユーザーの行動を記録し、それをさまざまな種類の分析にかけるというものです。

—Laboratory studies vs.
-実験室での研究vs.
field studies.
フィールドの研究をしています。
Lab studies allow focused investigation of specific issues; they are good for testing well-defined hypotheses under controlled conditions.
ラボスタディは、特定の問題を集中的に調査することができ、コントロールされた条件下で明確に定義された仮説を検証するのに適しています。
Field studies can reveal what users actually do in their own real contexts, showing common uses and usage patterns, problems and unmet needs, and issues that investigators may not have thought of to consider in a lab study.
フィールドスタディでは、ユーザーが実際に行っていることを明らかにすることができ、一般的な使い方や使用パターン、問題点や満たされていないニーズ、研究者がラボスタディで考慮することを思いつかなかったような問題点などが示されます。
In particular, tasks such as Evaluate Recommender and Express Self may require field studies because user behavior may be highly context-sensitive..
特に、Evaluate RecommenderやExpress Selfのようなタスクは、ユーザーの行動が文脈に大きく左右される可能性があるため、フィールドスタディが必要かもしれません。

—Outcome vs.
-成果対成果
process.
の処理を行います。
For any task, appropriate metrics must be developed that define what counts as a successful outcome [Newman 1997].
どのようなタスクであっても、何をもって成功とみなすかを定義する適切な測定基準を開発する必要がある [Newman 1997]。
From a systems perspective, accuracy may be the fundamental metric.
システムの観点からは、精度が基本的な指標になるのかもしれません。
From a user perspective, however, metrics must be defined relative to their particular tasks.
しかし、ユーザーの視点に立つと、メトリクスは彼らの特定のタスクに関連して定義されなければならない。
For most tasks (such as Find Good Items) a successful outcome requires users to act on the system’s recommendations, and actually purchase a book, rent a movie, or download a paper.
多くのタスク（例えば「良いものを探す」）では、ユーザーがシステムの推薦に従って行動し、実際に本を買ったり、映画を借りたり、論文をダウンロードしたりすることが成功の条件とされています。
However, to simply measure whether a goal is achieved is not sufficient.
しかし、単に目標が達成されたかどうかを測定するだけでは十分ではありません。
Systems may differ greatly in how efficiently users may complete their tasks.
システムによって、ユーザーがいかに効率よくタスクをこなせるかは大きく異なる。
Such process factors as amount of time and effort required to complete basic tasks also must be measured to ensure that the cost of a successful outcome does not outweigh the benefit..
また、基本的な仕事をこなすのに必要な時間や労力などのプロセス要素も測定し、成功のためのコストが利益を上回らないようにする必要があります。

—Short-term vs.
-短期 vs. 長期
long-term.
を長期に渡って使用します。
Some issues may not become apparent in a shortterm study, particularly a lab study.
短期間の研究、特にラボの研究では明らかにならない問題もあります。
For example, recall that Turpin and Hersh found that subjects were able to perform information retrieval tasks just as successfully with a less accurate search engine.
例えば、TurpinとHershは、被験者が精度の低い検索エンジンを使っても、情報検索タスクを同じように成功させることができることを発見したことを思い出してください。
However, if subjects continually had to read more summaries and sift through more off-topic information, perhaps they would grow dissatisfied, get discouraged, and eventually stop using the system..
しかし、より多くの要約を読み、より多くのトピックに目を通さなければならないとしたら、おそらく被験者は不満を募らせ、落胆し、最終的にはシステムを使うのをやめてしまうでしょう。

We consider several studies to illustrate the use of these methods.
これらの手法の使い方を説明するために、いくつかの研究を考察します。
Studies by Cosley et al.
Cosleyらによる研究。
[2003], Swearingen and Sinha [2001], Herlocker et al.
[2003], Swearingen and Sinha [2001], Herlocker et al.
[2000], and McDonald [2001] occupy roughly the same portion of the evaluation space.
[2000]、McDonald[2001]は、評価空間のほぼ同じ部分を占めています。
They are short-term lab studies that explicitly gather information from users.
これらは、ユーザーから明示的に情報を収集する短期間の研究室での研究です。
They all do some study of both task and process, although this dimension was not an explicit part of their analysis.
彼らは皆、タスクとプロセスの両方を研究していますが、この次元は彼らの分析の明確な部分ではなかったのです。
Amento et al.
Amento et al.
[1999, 2003] also did a short-term lab study, but it gathered both implicit and explicit user information and explicitly measured both task outcomes and process.
[1999, 2003]も短期間のラボ研究を行ったが、暗黙的・明示的なユーザー情報を収集し、タスクの結果とプロセスの両方を明示的に測定した。
Finally, Dahlen et al.
最後に、Dahlen et al.
[1998] did a lab study that used offline analysis to “replay” the history of user interactions, defining and measuring implicit metrics of user participation over the long term..
[1998年）には、オフライン分析を使ってユーザーとのやりとりの履歴を「再生」し、ユーザー参加の暗黙の指標を長期にわたって定義・測定する研究を行っています。

Most recommender systems include predicted user ratings with the items they recommend.
ほとんどのレコメンダーシステムは、予測されたユーザーの評価を、レコメンドするアイテムに含めています。
Cosley et al.
Cosleyら。
[2003] conducted a lab study to investigate how these predicted ratings influence the actual ratings that users enter.
[2003]は、これらの予測された評価が、ユーザーが入力する実際の評価にどのような影響を与えるかを調査するためのラボ研究を行った。
They presented subjects with sets of movies they had rated in the past; in some cases, the predictions were identical to the subjects’ past ratings, in some cases, they were higher, and in some they were lower.
被験者が過去に評価した映画のセットを提示したところ、予測は被験者の過去の評価と同じ場合もあれば、高くなる場合もあり、低くなる場合もありました。
Cosley et al.
Cosleyら。
found that the predicted ratings did influence user ratings, causing a small, but significant bias in the direction of the prediction.
は、予測された評価がユーザーの評価に影響を与え、小さいながらも予測方向に有意なバイアスを引き起こすことを発見しました。
They also found that presenting inaccurate predictions reduced user satisfaction with the system.
また、不正確な予測を提示すると、システムに対するユーザーの満足度が低下することも判明しました。
Thus, the methods used in this study yielded some evidence that users are sensitive to the predictive accuracy of the recommendations they receive..
このように、本研究で用いた手法により、ユーザーは自分が受け取るレコメンデーションの予測精度に敏感であることを示すいくつかの証拠が得られた。

Swearingen and Sinha [2002, 2001] carried out a study to investigate the perceived usefulness and usability of recommender systems.
Swearingen and Sinha [2002, 2001]は、レコメンダーシステムの有用性と使いやすさの認知度を調査する研究を実施した。
Subjects used either three movie recommenders or three book recommenders.
被験者は、3人の映画推薦者と3人の書籍推薦者のいずれかを利用した。
They began by rating enough items for the system to be able to compute recommendations for them.
まずは、システムが推奨するアイテムを計算できるようにするために、十分な数のアイテムを評価することから始めました。
They then looked through the recommendations, rating each one as useful and/or new, until they found at least one item they judged worth trying.
そして、提言に目を通し、それぞれを有用と評価した上で
Finally, they completed surveys and were interviewed by the experimenters..
最後に、アンケートに答えてもらい、実験者のインタビューを受けました。

The methods used in this experiment let the researchers uncover issues other than prediction accuracy that affected user satisfaction.
今回の実験では、予測精度以外のユーザー満足度に影響する課題を発見することができました。
For example, users must develop trust in a recommender system, and recommendations of familiar items supports this process.
例えば、ユーザーはレコメンダーシステムに対して信頼感を持つ必要がありますが、その際に身近なものを勧めることはそのプロセスをサポートします。
Explanations of why an item was recommended also helped users gain confidence in a system’s recommendations.
また、なぜその商品が推奨されるのか、その理由を説明することで、システムが推奨する商品に対する信頼感を高めています。
Users also face the problem of evaluating a system’s recommendations—for example, a movie title alone is insufficient to convince someone to go see it.
例えば、映画のタイトルだけでは、その映画を観に行く気になれないということです。
Thus, the availability and quality of “supporting information” a system provided—for example, synopses, reviews, videos or sound samples—was a significant factor in predicting how useful users rated the system.
このように、システムが提供する「サポート情報」、例えば、あらすじ、レビュー、ビデオ、サウンドサンプルなどの有無や質は、ユーザーがそのシステムをどの程度有用と評価しているかを予測する上で重要な要素であったのです。
A final point shows that user reactions may have multiple aspects—satisfaction alone may be insufficient.
最後に、ユーザーの反応は多面的であり、満足度だけでは不十分な場合があることを示します。
For example, subjects liked Amazon more than MediaUnbound and were more willing to purchase from Amazon.
例えば、被験者はMediaUnboundよりもAmazonの方が好きで、Amazonから購入する意欲が高いことが分かりました。
However, MediaUnbound was rated as more useful, most likely to be used again, and as best understanding user tastes.
しかし、MediaUnboundは、「より便利である」「また使いたい」「ユーザーの嗜好を最もよく理解している」という評価を得ました。
Further analysis showed that Amazon’s greater use of familiar recommendations may be the cause of this difference.
さらに分析を進めると、アマゾンが身近なレコメンデーションを多用していることが、この差の原因である可能性があることがわかりました。
The general point, however, is that for some purposes, users prefer one system, and for other purposes, the other..
しかし、一般的なポイントは、ある目的ではユーザーがあるシステムを好み、ある目的では他のシステムを好むということです。

Herlocker et al.
Herlockerら。
[2000] carried out an in-depth exploration of explanations for recommender systems.
[2000]では、推薦システムの説明について徹底的な探求を行った。
After developing a conceptual model of the factors that could be used to generate an explanation, they empirically tested a number of different explanation types.
彼らは、説明を生成するために使用できる要因の概念モデルを開発した後、いくつかの異なる説明タイプを実証的に検証した。
They used traditional usability evaluation methods, discovering that users preferred explanations based on how a user’s neighbors rated an item, the past performance of the recommender system, similarity of an item to other items the user rated highly, and the appearance of a favorite actor or actress.
従来のユーザビリティ評価手法を用い、ユーザーの隣人からの評価、レコメンダーシステムの過去の実績、ユーザーが高く評価した他のアイテムとの類似性、好きな俳優や女優の容姿などを基にした説明が好まれることを発見したのです。
Specifically, they led users to increase their estimate of the probability that they would see a recommended movie.
具体的には、推奨された映画を見る確率の推定値を上げるようにユーザーを誘導しました。
McDonald [2001] conducted a controlled study of his Expertise Recommender system.
McDonald [2001]は、彼の専門家推薦システムに関する対照研究を行った。
This system was developed within a particular organizational context, and could suggest experts who were likely to be able to solve a particular problem and who were “socially close”to the person seeking help.
このシステムは、特定の組織の中で開発されたもので、特定の問題を解決できる可能性が高く、助けを求めている人に「社会的に近い」専門家を提案することができます。
The notable feature of McDonald’s study was that subjects were given a rich scenario for evaluating recommendations, which specified a general topic area and a specific problem.
マクドナルドの研究の特筆すべき点は、被験者に一般的な話題の分野と具体的な問題を指定した豊富な推薦評価のシナリオを与えたことである。
In other words, the study was explicit in attempting to situate users in a task context that would lead them to evaluate the recommendations within that context..
つまり、ユーザーをタスクのコンテキストに位置づけ、その中でレコメンデーションを評価するように仕向けることが、本研究では明示的に行われた。

Amento et al.
Amento et al.
[1999, 2003] evaluated their “topic management” system, which lets users explore, evaluate, and organize collections of websites.
[1999, 2003]は、ユーザーがウェブサイトのコレクションを探索、評価、整理することができる「トピック管理」システムを評価しました。
They compared their system to a Yahoo-style interface.
彼らは自分たちのシステムをYahooスタイルのインターフェイスに例えた。
They gathered independent expert ratings to serve as a site quality metric and used these ratings to define the task outcome metric as the number of high-quality sites subjects selected using each system.
彼らは、サイト品質の指標となる独立した専門家の評価を集め、この評価を用いて、各システムを使用して被験者が選択した高品質のサイトの数をタスク成果の指標として定義しました。
In addition, they measured task time and various effort metrics, such as the number of sites subjects browsed.
また、タスク時間や被験者が閲覧したサイト数など、さまざまな努力指標を測定しました。
Thus, a key feature of their methods was they were able to measure outcomes and process together; they found that users of their system achieved superior results with less time and effort.
このように、成果とプロセスを一緒に測定できるのが彼らの手法の大きな特徴であり、彼らのシステムを使用したユーザーは、より少ない時間と労力で優れた成果を得ることができることがわかったのです。
Appropriate metrics will vary between tasks and domains; however, often effort can be conceived in terms of the number of queries issued or the number of items for which detailed information is examined during the process of evaluating recommendations..
タスクやドメインによって適切な指標は異なりますが、多くの場合、クエリの発行数や、推奨品の評価プロセスで詳細情報を調査する項目の数で、労力を考えることができます。

Dahlen et al.
Dahlenら。
[1998] studied the value of jump-starting a recommender system by including “dead data”—that is, ratings from users of another, inactive system.
[1998]は、「デッドデータ」、つまり、休止中の他のシステムのユーザーからの評価を含めることによって、推薦システムをジャンプスタートさせることの価値を研究しました。
Their experimental procedure involved “replaying” the history of both systems, letting them evaluate the early experience of users in terms of their participation.
その実験方法は、両システムの履歴を「再生」することで、ユーザーの初期の参加体験を評価するものでした。
This was the only course of action open, since it was impossible to survey users of the previous system.
旧システムのユーザーを調査することは不可能であったため、この方法しかなかったのです。
They found that early users of the “jumpstarted” system participated more extensively—they used the system more often, at shorter intervals, and over a long period of time, and they also entered more ratings.
その結果、"ジャンプスタート "システムの初期ユーザーは、より頻繁に、より短い間隔で、より長期間にわたってシステムを使用し、より多くの評価を入力していることがわかりました。
We believe that, in general, user contribution to and participation in recommender systems in the long term is quite important and relatively under-appreciated.
一般に、推薦システムに対するユーザーの長期的な貢献と参加は、非常に重要であり、比較的低く評価されていると考えています。
And we believe that the metrics used in the jumpstarting study can be applied quite broadly..
そして、ジャンプスタートスタディで使用された指標は、かなり広範囲に適用できると考えています。

To summarize our observations on user evaluation, we emphasize that accurate recommendations alone do not guarantee users of recommender systems an effective and satisfying experience.
ユーザー評価に関する我々の見解をまとめると、正確なレコメンデーションだけでは、レコメンダーシステムのユーザーに効果的で満足のいく体験を保証するものではないことを強調しています。
Instead, systems are useful to the extent that they help users complete their tasks.
むしろ、システムは、ユーザーがタスクを完了するのを助ける程度に有用である。
A fundamental point proceeds from this basis: to do an effective user evaluation of a recommender system, researchers must clearly define the tasks the system is intended to support.7 Observations of actual use (if available) and interviews with (actual or prospective) users are appropriate techniques, since it often is the case that systems end up being used differently than the designers anticipated.
実際の使用状況の観察（可能であれば）や（実際のまたは将来の）ユーザーへのインタビューは、適切な手法である。
Once tasks are defined, they can be used in several ways.
タスクが定義されると、いくつかの方法で使用することができます。
First, they can be used to tailor algorithm performance.
まず、アルゴリズムの性能を調整するために使用することができます。
Second, clearly defined tasks can increase the effectiveness of lab studies.
第二に、明確に定義されたタスクは、ラボスタディの効果を高めることができます。
Subjects can be assigned a set of tasks to complete, and various algorithms or interfaces can be tested to find out which ones lead to the best task outcomes..
被験者に課題を与え、様々なアルゴリズムやインターフェースをテストし、どのような課題が最も良い結果につながるかを検証することができます。

We also recommend that evaluations combine explicit and implicit data collection whenever possible.
また、可能な限り、明示的なデータ収集と暗黙的なデータ収集を組み合わせて評価することを推奨します。
This is important because user preferences and performance may diverge: users may prefer one system to another, even when their performance is the same on both, or vice versa.
これは、ユーザーの好みと性能が乖離する可能性があるため、重要なことです。両者で性能が同じでも、ユーザーはあるシステムを好むこともあれば、その逆もあります。
One advantage of gathering data about both performance and preferences is that the two can be correlated.
性能と嗜好の両方についてデータを収集することの利点は、両者に相関性を持たせることができることです。
(This is analogous to work on correlating implicit and explicit ratings [Claypool et al.
(これは、暗黙の評価と明示的な評価の相関に関する研究［Claypool et al.］と類似している）。
2001, Morita and Shinoda 1994]) Having done this, future evaluations that can gather only one of these types of data can have some estimate of what the other type of data would show..
2001, Morita and Shinoda 1994]）このように、どちらか一方のデータしか収集できない将来の評価では、もう一方のデータが何を示すかをある程度推定することができます。

# Conclusion 結論

Effective and meaningful evaluation of recommender systems is challenging.
レコメンダーシステムの効果的で有意義な評価は困難である。
To date, there has been no published attempt to synthesize what is known about the evaluation of recommender systems, nor to systematically understand the implications of evaluating recommender systems for different tasks and different contexts.
これまで、推薦システムの評価について知られていることを統合し、異なるタスクや異なるコンテクストに対して推薦システムを評価することの意味を体系的に理解する試みは発表されていない。
In this article, we have attempted to overview the factors that have been considered in evaluations as well as introduced new factors that we believe should be considered in evaluation.
本稿では、これまで評価で考慮されてきた要素を概観するとともに、評価で考慮すべきと思われる新たな要素を紹介することを試みました。
In addition, we have introduced empirical results on accuracy metrics that provide some initial insight into how results from different evaluation metrics might vary.
さらに、異なる評価指標による結果がどのように異なるかについての最初の洞察を提供する、精度指標に関する経験的な結果を紹介しました。
Our hope is that this article will increase the awareness of potential biases in reported evaluations, increase the diversity of evaluation dimensions examined where it is necessary, and encourage the development of more standardized methods of evaluation..
この記事が、報告された評価における潜在的なバイアスに対する認識を高め、必要な場合には評価次元の多様性を検討し、より標準的な評価手法の開発を促すことを期待している。

##  Future Work 今後の課題

While there are many open research problems in recommender systems, we find four evaluation-related problems to be particularly worthy of attention..
レコメンダーシステムには多くの未解決の研究課題がありますが、その中でも特に注目すべきは、評価に関する4つの問題です。

- User Sensitivity to Algorithm Accuracy. アルゴリズムの精度に対するユーザーの感度.

- We know from recent work by Cosley et al. [2003] that user satisfaction is decreased when a significant level of error is introduced into a recommender system. The level of error introduced in that study, however, was many times larger than the differences between the best algorithms. Key questions deserving attention include: (a) For different metrics, what is the level of change needed before users notice or user behavior changes? (b) To which metrics are users most sensitive? (c) How does user sensitivity to accuracy depend on other factors such as the interface? (d) How do factors such as coverage and serendipity affect user satisfaction? If these questions are answered, it may be possible to build a predictive model of user satisfaction that would permit more extensive offline evaluation. Cosleyらによる最近の研究からわかっている。 [2003]によれば、推薦システムに大きな誤差が生じると、ユーザーの満足度が低下することが分かっています。 しかし、その研究で導入された誤差のレベルは、最良のアルゴリズム間の差よりも何倍も大きいものでした。 注目すべき主な質問は以下の通りです。(a)さまざまなメトリクスについて、ユーザーが気づいたり、ユーザーの行動が変わったりするまでに必要な変化のレベルはどの程度か？(b) どのメトリクスに対して、ユーザーは最も敏感か？(c)精度に対するユーザーの感度は、インターフェースなどの他の要素にどのように依存するか？ (d)カバレッジやセレンディピティなどの要素は、ユーザーの満足度にどのように影響するか？これらの疑問に答えることができれば、より広範なオフライン評価を可能にするユーザー満足度の予測モデルを構築することができるかもしれない。

- Algorithmic Consistency Across Domains. ドメイン間のアルゴリズムの整合性。

- While a few studies have looked at multiple datasets, no researchers have systematically compared a set of algorithms across a variety of different domains to understand the extent to which different domains are better served by different classes of algorithms. If such research did not find differences, it would simplify the evaluation of algorithms—system designers could select a dataset with the desired properties without needing domain-specific testing. 複数のデータセットに注目した研究はいくつかありますが、様々な異なるドメインで一連のアルゴリズムを体系的に比較し、異なるドメインが異なるクラスのアルゴリズムによってどの程度良く機能するのかを理解した研究者はいません。 もしこのような研究で違いが見つからなければ、アルゴリズムの評価を簡略化することができ、システム設計者はドメイン固有のテストを必要とせずに、望ましい特性を持つデータセットを選択することができます。

- Comprehensive Quality Measures. 総合的な品質対策...

- Most metrics to date focus on accuracy, and ignore issues such as serendipity and coverage. There are well-known techniques by which algorithms can trade-off reduced serendipity and coverage for improved accuracy (such as only recommending items for which there are many ratings). Since users value all three attributes in many applications, these algorithms may be more accurate, but less useful. We need comprehensive quality measures that combine accuracy with other serendipity and coverage, so algorithm designers can make sensible trade-offs to serve users better. これまでの多くの指標は正確さに重点を置いており、セレンディピティやカバレッジといった問題は無視されています。 アルゴリズムが、セレンディピティやカバレッジの低下をトレードオフにして精度を向上させる手法はよく知られている（例えば、多くの評価があるものだけを推奨する）。 ユーザーは多くのアプリケーションで3つの属性すべてを重視するため、これらのアルゴリズムは精度が高くても、有用性は低いかもしれません。 アルゴリズム設計者がユーザーにより良いサービスを提供するために賢明なトレードオフを行えるように、精度とその他のセレンディピティやカバレッジを組み合わせた包括的な品質測定が必要です。

- Discovering the Inherent Variability in Recommender Datasets. 推薦者データセットに内在する変動性を発見する．

- We speculate above that algorithms trying to make better predictions on movie datasets may have reached the optimal level of error given human variability. Such variability can be explored using test-retest situations and analyses of taste change over time. If we can find effective ways to analyze datasets and learn the inherent variability, we can discover sooner when researchers have mined as much data as possible from a dataset, and thus when they should shift their attention from accuracy to other attributes of recommender systems. 映画のデータセットでより良い予測をしようとするアルゴリズムは、人間のばらつきを考慮した上で最適な誤差のレベルに達しているのかもしれないと、我々は上記のように推測している。 このようなばらつきは、テスト・リトライの状況や味の経時変化を分析することで調べることができます。 データセットを分析し、固有のばらつきを学習する効果的な方法を見つけることができれば、研究者がデータセットから可能な限り多くのデータを採掘したとき、したがって、推奨システムの正確さから他の属性に注意を移すべきときをより早く発見することができます。