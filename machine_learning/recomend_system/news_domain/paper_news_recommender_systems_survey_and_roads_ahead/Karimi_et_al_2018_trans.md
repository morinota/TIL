## 0.1. link リンク

- [pdf](https://web-ainf.aau.at/pub/jannach/files/Journal_IPM_2018.pdf)F

## 0.2. title タイトル

News Recommender Systems - Survey and Roads Ahead
ニュースレコメンダーシステム - 調査とその先にある道

## 0.3. abstract アブストラクト

More and more people read the news online, e.g., by visiting the websites of their favorite newspapers or by navigating the sites of news aggregators.
お気に入りの新聞のウェブサイトや、ニュースアグリゲーターのサイトを閲覧するなど、オンラインでニュースを読む人が増えている.
However, the abundance of news information that is published online every day through different channels can make it challenging for readers to locate the content they are interested in.
しかし、さまざまなチャネルを通じて毎日オンラインで公開される豊富なニュース情報は、読者が興味のあるコンテンツを探し出すことを困難にしている.
The goal of News Recommender Systems (NRS) is to make reading suggestions to users in a personalized way.
ニュースレコメンダーシステム（NRS）の目標は、ユーザーにパーソナライズされた方法で読書提案を行うことである.
Due to their practical relevance, a variety of technical approaches to build such systems have been proposed over the last two decades.
その実用性の高さから、過去20年以上にわたって、このようなシステムを構築するためのさまざまな技術的アプローチが提案されてきた.
In this work, we review the state-of-the-art of designing and evaluating news recommender systems over the last ten years.
本研究では、過去10年間のニュースレコメンダーシステムの設計と評価の最先端をレビューする.
One main goal of the work is to analyze which particular challenges of news recommendation (e.g., short item life times and recency aspects) have been well explored and which areas still require more work.
この研究の主な目的の一つは、ニュース推薦の特定の課題（例えば、短いアイテムのライフタイムや再放送の側面）がよく研究されており、どの領域がまだ多くの仕事を必要としているかを分析する事である.
Furthermore, in contrast to previous surveys, the paper specifically discusses methodological questions and today’s academic practice of evaluating and comparing different algorithmic news recommendation approaches based on accuracy measures.
さらに、これまでの調査とは対照的に、精度指標に基づいて異なるアルゴリズムによるニュース推薦アプローチを評価・比較するという方法論上の疑問と今日の学術的実践について具体的に論じている.

# 1. Introduction 序章

The newspaper industry has experienced a substantial transformation during the last twenty years.
新聞業界は、この20年間で大きな変貌を遂げた.
Today, readers can find various sources of news online, e.g., on the web presences of traditional newspaper companies, on digitalonly news sites, or on news aggregation platforms provided, for example, by Google2 or Yahoo!3 .
今日、読者は、伝統的な新聞社のウェブプレゼンス、デジタル専用のニュースサイト、あるいはGoogle2やYahoo！3が提供するニュースアグリゲーションプラットフォームなど、さまざまなニュースソースをオンラインで見つけることができる.
Additionally, the digital form of information delivery allows publishers to distribute new or updated content in real-time, leading to an increased speed of publication.
さらに、情報配信のデジタル化により、出版社は新しいコンテンツや更新されたコンテンツをリアルタイムで配信することができ、出版のスピードアップにつながります。
The availability of the various (often free) online news sources has led to a constant increase of users of such platforms [138].
さまざまな（しばしば無料の）オンライン・ニュース・ソースが利用できるようになったことで、そうしたプラットフォームの利用者が絶えず増加している[138]。
At the same time, however, the abundance of available information and the constant update cycle make it increasingly challenging for readers to keep track of news that are most relevant to them.
しかし、その一方で、膨大な量の情報と絶え間ない更新サイクルにより、読者が自分に最も関係のあるニュースを把握することはますます困難になっている.

Recommender Systems have shown to be a valuable tool to help users in such situations of information overload [84].
リコメンダーシステムは、このような情報過多の状況にあるユーザーを支援する貴重なツールであることが示されている[84]。
The main tasks of such systems are typically to filter incoming streams of information according to the users’ preferences or to point them to additional items of interest in the context of a given object.
このようなシステムの主なタスクは、通常、ユーザの好みに応じて入力される情報のストリームをフィルタリングしたり、与えられたオブジェクトのコンテキストで興味のある追加アイテムを紹介したりすることです。
During the past decades, significant advances in recommendation technology have been made.
過去数十年の間に、推薦技術の著しい進歩がありました。
Recommenders have been successfully applied in a variety of domains , and the recommendable objects include movies, books, travel and tourism services, research articles, search queries, and many more [9, 15, 144].
レコメンダーは様々な領域で応用され、映画、書籍、旅行・観光サービス、研究論文、検索クエリなど、推薦可能な対象は多岐にわたる [9, 15, 144] 。

News recommendation in general represents another application domain in which several of the known techniques for building automated recommendations can be applied.
ニュースレコメンデーションは、自動レコメンデーション構築のための既知の技術のいくつかが適用可能な、もう一つの応用領域である。
In fact, there have been a number of reported instances where such systems are being used in live environments to deliver news recommendations on popular websites (see, e.g., [32, 39, 93, 115, 118]).
実際、このようなシステムがライブ環境で使用され、人気のあるウェブサイトのおすすめニュースを配信している例が数多く報告されている（[32, 39, 93, 115, 118]など参照）。
However, news recommendation problems often have certain characteristics that are either not present at all or that are at least less pronounced in other domains.
**しかし、ニュース推薦問題は、他のドメインでは全く存在しないか、少なくともあまり顕著でないある種の特徴を持つことが多い。**
For example, in contrast to other domains like movie recommendation, the relevance of news items can change very rapidly (i.e., decline or re-increase due to recent real-life events) [5, 141] and the “item churn” is generally high [39].
例えば、映画推薦のような他のドメインとは対照的に、**ニュースアイテムの関連性は非常に急速に変化し（すなわち、最近の現実の出来事によって減少したり再増加したり） [5, 141] 、“item churn”は概して高い**[39].
In fact, since news web sites are often continuously updated, some articles can be superseded by a “breaking news” article on the same topic several times during a single day, which might require constant updates to the recommendation models.
実際、ニュースサイトは継続的に更新されることが多いため、1日のうちに何度も同じトピックに関する「速報」記事が更新されることがあり、**推薦モデルの更新が必要になることがある**.
Another typical challenge in the news domain is that a user’s interest can dynamically change, depending on different contextual factors like the time of the day, the features of the user’s device (e.g., mobile phone vs.
ニュース領域におけるもう一つの典型的な課題は、**ユーザの関心が、時間帯、ユーザーのデバイスの特徴（例：携帯電話対デスクトップ）、ユーザの現在地[20, 90, 125]など、さまざまな文脈的要因によって動的に変化すること**である.

Due to the high practical relevance of the news recommendation problem and its specific challenges, a considerable number of research works has been published on this topic in particular within the last ten years.
ニュース推薦問題の実用的な関連性の高さとその特有の課題から、特に過去10年間にかなりの数の研究論文が発表されています。
Many of these works propose novel algorithmic approaches to generate personalized recommendations.
これらの作品の多くは、パーソナライズされたレコメンデーションを生成するための新しいアルゴリズムアプローチを提案しています。
These algorithms are typically evaluated using offline experimental designs and existing log data.
これらのアルゴリズムは、**通常、オフラインの実験デザインと既存のログデータを使用して評価されます。**
In recent years, however, recommender systems research in a variety of domains has shown that it is also important to evaluate recommendations in a more user- or system utility-oriented way [48, 78, 83, 96, 151].
しかし近年、様々なドメインにおけるレコメンダーシステムの研究により、**よりユーザやシステムの実用性を重視した形でレコメンデーションを評価することも重要であることが示されている**[48, 78, 83, 96, 151]。
These developments have also led to a number of alternative forms of assessing the quality of the recommendations, e.g., in terms of diversity [80, 161, 172].
また、これらの発展により、多様性の観点からなど、**推薦の質を評価するための代替的な形態**も多く見られるようになった[80, 161, 172]。

With this work, we consider these recent developments and provide an overview of what has been achieved in the last ten years with respect to the different challenges in the news recommendation domain.
**本研究では、このような最近の動向を考慮し、ニュース推薦領域におけるさまざまな課題に関して、過去10年間に達成されたことの概要を説明するもの**である。
Based in this analysis, we identify existing research gaps and potential areas for future research.
この分析に基づき、既存の研究ギャップと将来の潜在的な研究領域を特定します。
In contrast to some previous overview works like [14, 109, 141], we however focus not only on the underlying algorithmic approaches used to create the recommendations, but also on questions related to the empirical evaluation and the user perception of such systems.
**[14、109、141]のような過去の概説書とは対照的に、我々は、推薦文を作成するために使用される基本的なアルゴリズムアプローチだけでなく、このようなシステムの経験的評価とユーザの知覚に関する問題にも焦点を当てている。**
To provide a starting point for future research, we finally also report insights from a set of experiments, which highlight the importance of short-term model updates when standard accuracy measures are applied in the evaluation.
将来の研究の出発点となるよう、最後に一連の実験から得られた知見を報告し、**評価に標準的な精度尺度を適用した場合の短期的なモデル更新の重要性**を強調します。

The paper is organized as follows.
本論文の構成は以下の通りである。
Next, in Section 2, we briefly summarize how we selected existing research works for consideration in our survey.
次に、第2節では、本調査で検討対象とした既存の研究作品をどのように選定したかを簡単にまとめる。
Afterwards, in Section 3, we discuss the various challenges of news recommendation in more detail and review existing algorithmic approaches to deal with these challenges.
その後、セクション3では、ニュース推薦の様々な課題についてより詳細に議論し、これらの課題に対処するための既存のアルゴリズムアプローチをレビューします。
Then, in Section 4, we provide a survey of today’s academic practice of benchmarking and evaluating different technical approaches.
そして、第4節では、異なる技術的アプローチのベンチマークと評価に関する今日の学術的実践のサーベイを提供する。
Our paper ends with an outlook on possible directions for future research in Section 5.
本論文は、第5節で今後の研究の可能な方向性を展望して終わる。

# 2. Survey Method and Research Scope 調査方法と調査範囲

To develop the survey part of the paper, we investigated, in a structured way, more than 140 research articles that appeared between 2005 and 2016 in relevant computer science and information systems publication outlets.
論文の調査部分を展開するために、2005年から2016年の間に関連するコンピュータサイエンスと情報システムの出版物に掲載された140以上の研究論文を、構造的に調査しました。
Figure 1 shows how many NRS papers were considered in this time frame per year.
図1は、この時期に検討されたNRS論文が年間何本あったかを示したものです。
The trend of the graph indicates that research interest in the topic of news recommendation has grown steadily over the years to the point that news has become an important sub-topic in the RS research field.
グラフの傾向から、ニュースレコメンデーションというテーマに対する研究の関心は、RS研究分野においてニュースが重要なサブテーマとなるまでに、年々着実に高まってきていることがわかります。

Figure 1: Number of NRS papers per year.
図1：年間のNRS論文数。
As the survey only covered 2016 until August, this year was excluded.
調査対象が2016年8月までしかないため、本年は除外しています。

Regarding the scope of our review, we focus on papers that describe approaches for “classical” news recommendation scenarios, e.g., on news aggregation sites.
**今回のレビューでは、ニュースアグリゲーションサイトなどの「古典的な」ニュース推薦シナリオに対するアプローチを記述した論文に焦点を当てます。**
Similar technical approaches can in many cases be applied for “news feed filtering” problems, for example on Facebook or Twitter, where the content of social news feeds are personalized to the users.
同様の技術的アプローチは、例えばFacebookやTwitterのような、ソーシャルニュースフィードの内容がユーザーにパーソナライズされる「ニュースフィードフィルタリング」の問題にも、多くの場合適用できます。
These scenarios feature many of the same challenges, e.g., an emphasis on freshness and an overwhelming number of new items every day.
これらのシナリオでは、鮮度が重視され、毎日新しいアイテムが溢れかえるなど、同じ課題が多くあります。
However, news feed filtering on social networks has some unique aspects that are different from news recommendation.
**しかし、ソーシャルネットワーク上のニュースフィードフィルタリングは、ニュース推薦とは異なるユニークな側面を持っています。**
For example, the recommendable items are not necessarily news items but can be some currently trending viral videos that are not related to a recent event in the real world.
例えば、推奨されるアイテムは、必ずしもニュースアイテムである必要はなく、現実世界での最近の出来事とは関係のない、現在トレンドとなっているいくつかのバイラルビデオであることも可能です。
Also, on news sites, information about a visitor’s social network friends and general interest profile is in many cases non-existent.
**また、ニュースサイトでは、訪問者のソーシャルネットワーク上の友人や一般的な関心のあるプロフィールに関する情報は、多くの場合存在しません。**
However, this information oftentimes plays a central role in news feed personalization.
**しかし、この情報はニュースフィードのパーソナライズにおいて中心的な役割を果たすことが多い。**

The identification of papers for our survey was done according to the following strategy.
本調査の対象となる論文の特定は、以下の戦略に従って行われた。
We first scanned the proceedings and volumes of a set of relevant conference series (RecSys, WWW, SIGIR, and KDD) and journals (Expert Systems with Applications and Knowledge-Based Systems) for articles that fall into the above-described scope.
まず、**関連する一連の会議シリーズ（RecSys、WWW、SIGIR、KDD）とジャーナル（Expert Systems with Applications、Knowledge-Based Systems）**のプロシーディングスや巻号をスキャンして、上記の範囲に該当する記事を探しました。
Additionally, we used the keywords “news recommendation” and “news recommender” to search for papers in Google Scholar.
さらに、「ニュースレコメンデーション」「ニュースレコメンダー」というキーワードで、Google Scholarの論文検索を行いました。
Using the resulting set of articles as a starting point, we followed the references of the retrieved articles to find additional papers on the topic.
その結果得られた論文群を出発点として、検索された論文の参考文献をたどって、このテーマに関する追加の論文を探しました。
The survey methodology is therefore not that of a traditional “systematic review” in the sense of, e.g., [94], where pre-defined search queries and inclusion and exclusion criteria are used.
したがって、この調査方法は、例えば[94]のような、あらかじめ定義された検索クエリーや包含・除外基準が使用される伝統的な「システマティックレビュー」の方法とは異なっている。
Nonetheless, as we followed a defined search strategy, had a defined research scope, and used pre-structured forms to classify the papers along different dimensions, we are confident that the risk of the introduction of a researcher bias into the survey is low.
しかしながら、我々は、定義された検索戦略に従い、定義された研究範囲を持ち、異なる次元で論文を分類するために事前構造化されたフォームを使用したため、調査に研究者バイアスが導入されるリスクは低いと確信しています。

A few other survey works on the topic of news recommendation already exist.
ニュース推薦をテーマとした調査研究は、他にもいくつか存在する。
When looking at these existing works, we find that some challenges of news recommendation that we identify in our work were also summarized by Ozg ¨ obek et al.[141].
これらの既存研究を見ると、我々が発見したニュース推薦の課題のいくつかは、Ozg ¨obekら[141]もまとめていることがわかります。
The authors of this work however only consider a small number of (twelve) papers and do not ¨ consider evaluation aspects in their survey.
しかし、この作品の著者は、少数の論文（12本）のみを対象としており、評価面を考慮した調査を行っていない。
Li et al.[109] also discuss challenges of news recommendation, but do not discuss existing approaches to deal with these issues in depth.
Liら[109]もニュース推薦の課題を論じているが、これらの課題に対処する既存のアプローチについては深く論じてはいない。
The survey paper by Borges and Lorena [14], finally, discusses news recommendation mostly from a quite general perspective and focuses the analysis on different aspects of six specific papers.
BorgesとLorenaによるサーベイ論文[14]は、ニュース推薦について、主にかなり一般的な観点から論じ、6つの特定の論文の異なる側面に焦点を当てた分析を行っている。

# 3. News Recommendation – Challenges and Algorithmic Approaches ニュースレコメンデーション - 課題とアルゴリズムアプローチ

Before we discuss the challenges of the domain in more detail along with algorithmic approaches that were proposed in the literature, we will briefly review which types of algorithms are generally used for the news recommendation problem.
文献で提案されたアルゴリズムアプローチとともに、この領域の課題をより詳細に議論する前に、ニュース推薦問題に対して一般的にどのような種類のアルゴリズムが使用されているかを簡単にレビューする。

## 3.1. Recommendation Paradigms in News Recommendation ニュース推薦における推薦パラダイム

Recommender systems are often classified into four main categories [84, 108]: collaborative filtering (CF), contentbased filtering (CB), knowledge-based techniques (KB), and hybrid approaches.
レコメンダーシステムは、協調フィルタリング（CF）、コンテンツベースフィルタリング（CB）、知識ベース技術（KB）、ハイブリッドアプローチの**4つ**に分類されることが多い [84, 108]。
In academic settings, collaborative filtering is the most common approach in the recommender systems literature according to the survey presented in [85], while all other approaches are much less frequently employed.
学術的には、[85]の調査によると、協調フィルタリングは推薦システムの文献で最も一般的なアプローチであり、他のすべてのアプローチはあまり採用されていない。
The general dominance of collaborative filtering is in some sense not surprising because this method, whose recommendations are based on the “wisdom of the crowd”, is domain-independent and does not require detailed (and domain-specific) information about the recommendable items.
**協調フィルタリングの優位性はある意味当然である。なぜなら、この手法は「群衆の知恵」に基づいて推薦されるため、ドメインに依存せず、推薦されるアイテムに関する詳細な（そしてドメイン固有の）情報を必要としないた**めである。
Furthermore, a number of public benchmark data sets, e.g., from MovieLens4 , are available, which has been a driving factor for the academic community.
さらに、MovieLens4 などの公開ベンチマークデータセットが多数用意されており、これが学術界の推進力となっている。

In the news recommendation domain, however, things are different.
**しかし、ニュースレコメンデーションの領域では、事情が異なりま**す。
An analysis of the 112 (of 144) papers in our survey that propose one or more recommendation algorithms reveals the following.5 Content-based filtering, which is, roughly speaking, based on analyzing a reader’s past documents of interest and recommending “more of the same”, was used as an underlying paradigm in 59 of the analyzed papers.
推薦アルゴリズムが提案されている論文 112 件（144 件中）を分析した結果、以下のことが明らかになった5。 コンテンツベースフィルタリングは、大まかに言えば、読者の過去の興味ある文書を分析し、「同じものをもっと」推薦するというもので、59 件の論文が基本パラダイムとして使用されていた。
Approaches, like the Google News personalization system [39], that rely on collaborative filtering and on interest patterns in a community without considering the content of a news article are only proposed in 19 of the 112 papers.
**Google News Personalization System [39]のように、ニュース記事の内容を考慮せず、協調フィルタリングやコミュニティ内の関心パターンに依存するアプローチは、112本の論文のうち19本しか提案されていない。**
However, 45 of the papers use a hybrid approach and combine content-based filtering and collaborative filtering.
しかし、**45の論文ではハイブリッドアプローチを採用し、コンテンツベースフィルタリングと協調フィルタリングを組み合わせています。**
This means that although collaborative filtering alone is not the method of choice for most researchers, relying on patterns in the community behavior in addition to contentbased user profiles is often considered to be promising.
つまり、協調フィルタリングだけでは多くの研究者が選択する手法ではないが、コンテンツベースのユーザープロファイルに加えて、コミュニティの行動パターンに依存することが有望視されることが多いのである。
Knowledge-based techniques, which are based on explicit domain knowledge to map user preferences to article features, were not applied in any of the analyzed papers, neither in isolation nor in combination with other techniques.
**知識ベース技術とは、明示的なドメイン知識に基づいてユーザーの嗜好を記事の特徴に対応付ける技術であるが、分析したどの論文でも、単独でも他の技術との組み合わせでも、適用されていなかった**。
This is, however, not very surprising, since such approaches are generally only employed in high-involvement product domains with a long life cycle.
しかし、このようなアプローチは、**一般的にライフサイクルの長い高関与度の製品領域でのみ採用されているため**、あまり驚くべきことではありません。

Since the recommendable objects in the news domain are text documents, which can be automatically analyzed with standard techniques from Information Retrieval (IR), it is in fact not too surprising that many researchers rely on content-based techniques.
ニュース領域で推奨される対象はテキスト文書であり、情報検索（IR）の標準的な技術で自動的に分析できるため、多くの研究者がコンテンツベースの技術に頼っていることは、実はそれほど驚くべきことではありません。
However, in general, content-based techniques are considered not to be very accurate in offline experiments when using IR measures like precision and recall [80].
**しかし、一般的に、コンテンツベースの技術は、オフラインの実験では、精度や想起などのIR指標を用いた場合、あまり正確ではないと考えられている**[80]。
As in other domains, the main dilemma of academic research – and to some extent also for recommendation service providers – is that it is not always clear to what extent high accuracy in offline experiments translates into online success [60].
他の領域と同様に、学術研究の主なジレンマは、そしてある程度は推薦サービスプロバイダーにとっても、**オフラインの実験での高い精度が、オンラインでの成功にどの程度結びつくかが必ずしも明確でないことである**[60]。
Only very few studies are available that compare the offline and online performance of recommendation algorithms, e.g., [10] in the field of research paper recommendation.
推薦アルゴリズムのオフラインとオンラインの性能を比較した研究は、研究論文推薦の分野では[10]など、ごくわずかしかありません。
In the news domain, a comparative offline/online experiment was recently conducted by Garcin et al.[55], who also found that offline performance is not necessarily a predictor of online success.
**ニュース領域では、最近、Garcinら[55]がオフライン／オンラインの比較実験を行い、オフラインの成績が必ずしもオンラインの成功の予測因子にはならないことも明らかにした。**
In their case, a popularity-based method performed best offline, but, in the end, showed the worst results in an online test, placing far behind a more sophisticated algorithm.
彼らの場合、オフラインでは人気に基づく方法が最も良い結果を示したが、結局オンラインテストでは最悪の結果を示し、より洗練されたアルゴリズムに大きく遅れをとった。

As we will discuss later, the effectiveness of pure collaborative filtering methods might be overestimated in offline experiments, which calls for the design of novel hybrid approaches that combine multiple sources of preference signals and which are able to balance prediction accuracy with other quality factors like novelty or diversity.
後述するように、**純粋な協調フィルタリング手法の有効性はオフライン実験では過大評価される可能性があり**、複数の嗜好信号源を組み合わせ、予測精度と新規性や多様性といった他の品質要因のバランスをとることができる新しいハイブリッドアプローチの設計が求められています。

## 3.2. Challenges of User Modeling for News Recommendation ニュースレコメンデーションのためのユーザーモデリングへの挑戦

To be able to personalize the reading suggestions, recommender systems have to create and maintain user profiles that capture each user’s reading preferences over time.
読書提案をパーソナライズするために、推薦システムは、**各ユーザーの読書嗜好を長期にわたって把握するユーザープロファイル**を作成・維持する必要があります。
How these user profiles are built and which information is collected and used is usually related to the chosen recommendation paradigm.
このようなユーザープロファイルをどのように構築し、どの情報を収集・使用するかは、通常、選択された推薦パラダイムと関連しています。
Similar to other application domains of recommender systems, one can in general try to stimulate users to provide explicit preference information, e.g., in the form of “like” or “dislike” statements, or monitor and interpret the user’s past behavior (implicit feedback) over time.
**推薦システムの他の応用領域と同様に、一般的には、例えば「好き」「嫌い」の表明という形で、ユーザに明示的な嗜好情報の提供を促すか、ユーザの過去の行動（暗黙のフィードバック）を時間経過とともに監視し解釈しようとすることができます。**
Typical implicit feedback signals in the news domain include reading an article, sharing it, printing it, or commenting on it.
**ニュース領域における典型的な暗黙のフィードバック信号には、記事を読む、共有する、印刷する、コメントする、などがあります。**
On a more fine-grained level, it is also possible to record dwelling times or mouse movements as interest indicators.
**また、より細かいレベルでは、滞在時間やマウスの動きなどを interest indicator として記録することも可能**です。
Generally, different types of information can be used to construct the user profiles.
一般に、ユーザープロファイルを構築するために、さまざまな種類の情報を使用することができる。
Many papers rely mainly on the content of the news articles inspected by a user to infer the interest profiles.
**多くの論文では、興味プロファイルを推論するために、主にユーザーが閲覧したニュース記事の内容に依存しています。**(=つまりContent base??)
Some works, in addition, consider features of the users and the community they belong to to create the profiles.
さらに、ユーザや所属するコミュニティの特徴を考慮してプロフィールを作成する作品もある.(SimClusterもこの一種に該当する感じかな...:think:)
Other approaches finally use various types of information in parallel.
また、最終的に様々な情報を並行して利用するアプローチもある.
An example of a system that relies mostly on content information is the Athena news recommendation system [74], where the user profile is based on the keywords of the articles that were read by a user.
**コンテンツ情報に多くを依存するシステムの例**として、Athenaニュース推薦システム[74]があり、ユーザープロファイルは、ユーザーが読んだ記事のキーワードに基づくものである。
New or not yet viewed articles are then ranked according to the similarity of their content with the aggregated user profile.
そして、新しい記事やまだ閲覧されていない記事は、集約されたユーザープロファイルとの内容の類似性に従ってランク付けされる.
A similar approach was used by Rao et al.[153], who employ user profiles that have a “bag-of-concepts” format with DBPedia as a knowledge base in the background.
同様のアプローチはRaoら[153]によっても用いられており、彼らはDBPediaをバックグラウンドの知識ベースとした“bag-of-concepts”形式を持つユーザプロファイルを採用している。(???)
Standard distance measures like cosine similarity or the Jaccard coefficient can then be used to assess the relevance of a news article for a given profile.
コサイン類似度やジャカード係数のような標準的な距離尺度は、与えられたプロファイルに対するニュース記事の関連性を評価するために使用されます。(うんうん、推薦スコアの算出ね)
Similar to these approaches, Chu and Park [31] rely on the content of the read articles for profile construction, and additionally consider demographic aspects to assess the relevance of new articles for a user.
これらのアプローチと同様に、Chu and Park [31]は、プロファイル構築のために読まれた記事の内容に依存し、さらに、ユーザにとっての新しい記事の関連性(新しく追加されたアイテムのこと?それともSerendipity的な新しさ?)を評価するために人口統計学的側面(??)を考慮する。
Another work that considers demographic information as a key factor for user profiling is [103].
また、デモグラフィック情報をユーザープロファイリングの重要な要素として考慮した作品として、[103]がある。
In this approach, the users were first segmented according to their demographics and article access patterns.
このアプローチでは、まず、**ユーザの属性と記事へのアクセスパターンに応じてセグメンテーション**が行われました。
The relevance of a new article for a given user was then calculated based on various factors, including the estimated interest of the user’s segment in the topic of the article or the number of users in the segment who have already read the article.
そして、あるユーザにとっての新しい記事の関連性は、その記事のトピックに対するそのユーザーのセグメントの推定関心度や、そのセグメントですでにその記事を読んでいるユーザ数など、さまざまな要因に基づいて算出されました。
Instead of clustering the users, Li et al.[112] applied a graph-based model based on which the logical relationship and similarities between a newly posted article and user comments about the article on a social media site were calculated.
Liら[112]は、ユーザをクラスタリングする代わりに、**グラフベースのモデルを適用し、新しく投稿された記事とソーシャルメディアサイト上のその記事に関するユーザーコメントとの論理的関係や類似性を算出した**.
This topicbased model was then used to retrieve other relevant news articles.
このトピックベースモデルは、その後、他の関連するニュース記事を検索するために使用されました。
The basis for the user modeling approach in [5] is a weighted term vector, which is generated by considering the topics of the articles that were read by a user.
[5]のユーザーモデリングアプローチの基礎は、ユーザーが読んだ記事のトピックを考慮して生成される重み付き用語ベクトルである。
Different from other approaches, however, the authors propose to maintain a short-term and a long-term model, where the short-term model only considers the 20 most recently read articles of each user.
しかし、他のアプローチとは異なり、著者らは短期モデルと長期モデルを維持することを提案し、短期モデルは各ユーザーの最近読んだ20件の記事のみを考慮する。
Besides being able to capture long-term and short-term interests for recommending, the topicbased approach of Ahn et al.[5] was designed in a way that users can be put in control of their recommendations.
Ahnら[5]のトピックベースアプローチは、**推薦のための長期的・短期的な興味を把握できることに加え、ユーザーが推薦をコントロールできるように工夫されている**。(ほうほう...?)
For each recommended article, the relevant topics were displayed and users could then update their profile accordingly when they did not agree with the system’s assumptions about the preferences.
**推薦された記事ごとに、関連するトピックが表示され、ユーザは、システムが想定した嗜好に同意できない場合、それに応じて自分のプロフィールを更新することができました**。

(以下は、記事の内容を考慮しないアプローチの既存研究の話。)

An example of a work that solely relies on click behavior and does not consider article content is presented by Das et al.[39], who describe the inner workings of the Google News Personalization system at that time.
**クリック行動のみに依存し、記事の内容を考慮しない研究の例**として、Dasら[39]が当時のGoogle News Personalizationシステムの内部構造を紹介している。
Similar to Lee and Park [103], they clustered the user community, this time however based mainly on the past article reading behavior.
Lee and Park [103]と同様に、彼らはユーザーコミュニティをクラスタリングしたが、今回は主に過去の記事閲覧行動に基づいている。
To predict the relevance of an item, they then used both a long-term collaborative filtering model and a short-term model based on article co-visitations.
そして、アイテムの関連性を予測するために、**長期的な協調フィルタリングモデルと記事の共参照に基づく短期的なモデルの両方を使用しました。**
In a later paper, Liu et al.[115] present an alternative approach that was also implemented for the Google News service.
後の論文で、Liuら[115]は、Google Newsサービスにも実装された代替アプローチを紹介している.
In contrast to the previous approach, their newer model takes both content information as well as the reading patterns in the community into account.
従来のアプローチとは対照的に、彼らの新しいモデルは、コンテンツ情報だけでなく、コミュニティにおける読書パターンも考慮に入れています。
Their proposed Bayesian framework tries to remove the community bias from the user’s consumption behavior in each topic to extract the user’s “genuine” long-term interests.
彼らの提案するベイズフレームワークは、**各トピックにおけるユーザーの消費行動からコミュニティのバイアスを取り除き、ユーザーの「真の」長期的な興味を抽出しようとするもの**である。
Furthermore, it is also designed to take short-term changes in the user’s interests into account.
さらに、ユーザーの興味の短期的な変化も考慮した設計になっています。
To predict the relevance of new articles, the proposed approach finally also considers the user’s location and the reading behavior of the user community in the past hour.
新しい記事の関連性を予測するために、提案されたアプローチは最終的に、**ユーザーの位置情報と過去1時間におけるユーザーコミュニティの読書行動も考慮**します。
Generally, considering long-term and short-term preferences and balancing their importance represent an important problem in news recommendation [72, 110]; see also the discussion later in Section 3.4 on recency aspects.
**一般に、ニュース推薦では、長期的な選好と短期的な選好を考慮し、その重要性をバランスさせることが重要な問題**である[72, 110]; 再現性の側面については、セクション 3.4 の後の議論も参照。
One of the key design questions is whether two separate models should be maintained (as, e.g., in [6]) or an integrated model with a time decay factor (as in [111]).
設計上の重要な問題の一つは、**2つの別々のモデルを維持すべきか**（例えば[6]のように）、**それとも時間減衰係数を持つ統合モデル**（[111]のように）か、ということです。
A comparison of different strategies of considering the long-term and short-term preferences was done by Huy et al.[72], who observed that a combination of both models in a hybrid approach led to the best results.
長期的な選好と短期的な選好を考慮した異なる戦略の比較はHuyら[72]によって行われ、ハイブリッドアプローチで両方のモデルの組み合わせが最良の結果をもたらすことが観察された。

## 3.3. Cold-Start Problems and Data Sparsity Issues in News Recommendation ニュース推薦におけるコールドスタート問題とデータのスパース性問題

Cold-start situations are a common problem in many application domains of recommender systems.
コールドスタート状況は、レコメンダーシステムの多くの応用領域で共通の問題である。
User coldstart refers to situations where little is known about the preferences of the user for which a recommendation is requested; item cold-start means that a new recommendable item (i.e., an article) was added that was not viewed or rated by many people yet.
ユーザーコールドスタートとは、推薦を求めるユーザーの嗜好がほとんどわかっていない状態のことで、アイテムコールドスタートとは、まだ多くの人に閲覧・評価されていない新しい推薦アイテム（記事など）が追加された状態のことです。
The problem of general data sparsity is often connected to this problem and in particular relevant for collaborative filtering approaches.
一般的なデータの疎密の問題は、この問題としばしば関連しており、特に協調フィルタリングのアプローチに関連している。

### 3.3.1. The Permanent Cold-Start Problem 永久Cold-start問題

In principle, many of the technical and domain-independent approaches that were proposed over the years to deal with cold-start situations can be applied in the news recommendation context.
原理的には、コールドスタートの状況に対処するために長年提案されてきた技術的かつドメインに依存しないアプローチの多くが、ニュース推薦の文脈で適用可能である。
One general approach is to try to incorporate additional information (e.g., about the user’s context) into the recommendation process when little is known about the current user.
一般的なアプローチとしては、現在のユーザについてほとんど知られていない(=reading historyが殆どないケース)場合に、**追加情報（例えば、ユーザーのコンテキストに関する情報）を推薦プロセスに組み込む**ことを試みることが挙げられる。
In the news recommendation domain, for example, works exist that consider the user’s location [49, 132, 166], the time of the day [40, 49, 132], or demographic information [103].
例えば、ニュース推薦の領域では、ユーザーの位置情報 [49, 132, 166]、時間帯 [40, 49, 132]、あるいは人口統計情報 [103] を考慮した作品が存在します。
Other examples of contextual information explored in the literature include the website (or domain) that the user has visited before landing on the news page or the type of the device used to access the news [40, 168].
文献で検討された文脈情報の他の例としては、ユーザーがニュースページにたどり着く前に訪れたウェブサイト（またはドメイン）、またはニュースへのアクセスに使用したデバイスのタイプなどがある[40, 168]。
Instead of considering only the limited information of the user’s history, Lin et al.[113] propose to construct an implicit social network of other users with similar reading behavior.
Linら[113]は、**ユーザの履歴という限られた情報のみを考慮するのではなく、読書行動が似ている他のユーザーとの暗黙のソーシャルネットワークを構築することを提案している**。
The authors then suggest to determine a set of “experts” whose opinion is used to make recommendations for users for which only a short reading history is available.
そして、短い読書履歴しかないユーザに対して、その意見を参考に推薦する「専門家」のセットを決めることを提案している。(暗黙のソーシャル・ネットワークを使って、SimClustersと同じような事をするアプローチなのかな...)
To identify these experts, they considered other users who have read the same articles in a given time frame, and they subsequently involved these users more heavily in the factorization process if they have a high probability of being a good proxy for a cold-start user.
これらのエキスパートを特定するために、ある時間帯に同じ記事を読んだ他のユーザを考慮し、コールドスタートユーザの良い代理人となる確率が高い場合は、その後、これらのユーザを因数分解プロセスにより大きく関与させるようにした。
Along the same lines, Zheng et al.[186] propose to enrich the profiles of cold-start users with the profiles of a group of similar other users based on the general news topics they seem to be interested in.
同じ路線で、Zhengら[186]は、コールドスタートユーザーのプロファイルを、彼らが興味を持っていると思われる一般的なニューストピックに基づいて、類似した他のユーザーグループのプロファイルで豊かにすることを提案している。
An alternative to incorporating additional aspects related to the user is to consider certain features of the news articles themselves when assessing their relevance for a cold-start user, e.g., the freshness of the article or its general popularity.
ユーザに関連する追加的な側面を取り入れる事の代替案は、コールドスタートのユーザーに対する関連性を評価する際に、ニュース記事自体の特定の特徴、例えば、記事の新鮮さやその一般的な人気度を考慮することである。
Also, one can default to a non-personalized strategy in case of too little information.
**また、情報が少なすぎる場合には、パーソナライズされない戦略をデフォルトにすることもできます**。
The “YourNews” system [5], for example, first shows a list of recently published articles and starts the personalization process after the first article has been read.
例えば、「YourNews」システム[5]では、まず最近発表された記事のリストを表示し、最初の記事が読まれた後にパーソナライズ処理を開始します。
In another approach, Montes-Garc´ıa et al.[132] consider the geographical proximity of the news event to the user and the credibility of a news source as factors that can determine the relevance of an item to a cold-start user.
別のアプローチでは、Montes-Garc´àaら[132]は、ニュースイベントのユーザへの地理的近接性とニュースソースの信頼性を、コールドスタートのユーザーに対するアイテムの関連性を決定できる要因として考慮しています。
In their case, the credibility of the news source was determined manually by a team of journalists.
彼らの場合、ニュースソースの信頼性は、ジャーナリストチームによって手動で判断されました。
The context-tree approach by Garcin et al.[53] also takes the recency of the news items into account, but in addition factors the item’s popularity into the recommendation process.
Garcinら[53]によるコンテキストツリーアプローチも、ニュースアイテムの新着度を考慮するが、それに加えてアイテムの人気度を推薦プロセスに反映する。
By design, their method is also suitable for one-time or first-time users, which are not uncommon for news platforms.
デザイン上、彼らの方法は、ニュースプラットフォームでは珍しくない、1回限りのユーザーや初めてのユーザーにも適しています。
Finally, Tavakolifard et al.[166] propose to use external data sources – in their case Twitter – to estimate an item’s current popularity more precisely and correspondingly obtain a better picture of its potential relevance for the current user.
最後に、Tavakolifardら[166]は、外部データソース（彼らの場合はTwitter）を使用して、アイテムの現在の人気をより正確に推定し、それに対応して、現在のユーザーに対する潜在的な関連性のより良い画像を得ることを提案する。

For the item cold-start problem, adopting a content-based recommendation strategy already solves a major part of the problem.
アイテムのコールドスタート問題については、**コンテンツベースのレコメンデーション戦略を採用することで、すでに問題の大部分を解決している**.
In content-based approaches, items are generally recommended based on the past content-wise preferences of individual users, which are usually determined by their past navigation or item rating behavior.
コンテンツベースのアプローチでは、一般的に、アイテムは、個々のユーザーの過去のナビゲーションやアイテムの評価行動によって決定される、過去のコンテンツワイズプリファレンスに基づいて推薦されます。
Therefore, the required information about a news article can be extracted easily, e.g., from its keywords, making it instantly recommendable without the need for a detailed click history.
そのため、ニュース記事のキーワードなどから必要な情報を簡単に抽出することができ、詳細なクリック履歴を必要とせず、即座に推薦できるようになります。
Different alternative technical approaches are possible to infer the user preferences.
ユーザーの嗜好を推測するためには、さまざまな代替技術的アプローチが可能です。
Li et al.[108], for example, propose a hybrid approach to construct the user profiles which considers factors such as similarities between access patterns for different news items.
例えば、Liら[108]は、異なるニュース項目に対するアクセスパターンの類似性などを考慮したハイブリッドなアプローチでユーザプロファイルを構築することを提案している。
In addition, their approach utilizes item properties that are specific to news, like the news content itself, as well as the user’s preferences for named entities appearing in the news item.
さらに、ニュースの内容そのものや、ニュース中に登場する名前付きエンティティに対するユーザーの好みなど、ニュースに特化したアイテム特性を利用する。

### 3.3.2. Data Sparsity Issues データスパース性の問題

When applying collaborative filtering approaches, the recommendation problem is often considered as a matrix completion task, with users and items as rows and columns, respectively, and matrix entries representing the relevance of items for users.
協調フィルタリングアプローチを適用する場合、推薦問題は、しばしば、ユーザーとアイテムをそれぞれ行と列とし、マトリックスエントリーがユーザーに対するアイテムの関連性を表すマトリックス補完タスクとして考慮されます。
In many domains, including the news domain, this matrix can be extremely sparse and only a tiny fraction of the matrix entries are known.
ニュース領域を含む多くの領域では、この行列は極めて疎なものとなり、行列エントリのごく一部しか知られていないことがあります。
Finding a sufficient number of similar users, for example, in a nearestneighbors collaborative filtering approach, can therefore be very challenging [143].
そのため、例えば最近接協調フィルタリングのアプローチにおいて、十分な数の類似ユーザーを見つけることは、非常に困難である[143]。
Correspondingly, a number of approaches have been proposed in the context of news recommender systems to deal with the sparsity problem, e.g., by incorporating additional sources of knowledge, predominantly for collaborative filtering, but also for other approaches.
そのため、ニュースレコメンダーシステムでは、協調フィルタリングを中心に、その他のアプローチも含め、追加的な知識ソースを取り入れるなどして、スパース性の問題に対処するアプローチが数多く提案されています。
Mannens et al.[127], for example, propose a recommendation method that mitigates sparsity by complementing binary consumption values in the matrix with “potential consumption” values between 0 and 1 based on a collaborative filtering algorithm, which is then re-executed until the matrix is dense enough.
例えば、Mannens ら[127]は、協調フィルタリングアルゴリズムに基づき、**行列内の二値消費値を0～1の「潜在消費値」で補完**し、行列が十分に密になるまで再実行することで疎密を緩和する推薦手法を提案している。
Furthermore, to reduce the uncertainty introduced by this probabilistic approach, they also suggest to post-filter the news articles based on Linked Data sources.
さらに、この確率論的アプローチによってもたらされる不確実性を低減するために、Linked Dataソースに基づいてニュース記事をポストフィルターすることも提案しています。
In contrast, Morales et al.[133] propose to use information from social network sites to deal with the sparsity problem.
一方、Moralesら[133]は、スパースティ問題に対処するために、ソーシャルネットワークサイトからの情報を利用することを提案しています。
In their work, they analyzed the posts of users and their social friends on Twitter and generated a mapping between tweets and news articles based on the entities in the articles.
彼らの研究では、Twitter上のユーザーとそのソーシャルフレンドの投稿を分析し、記事中のエンティティに基づいて、ツイートとニュース記事の間のマッピングを生成したものである。
Leveraging information about the relationships between users is also the idea of the work presented in [114] and [113], which has already been mentioned in Section 3.3.1.
**ユーザー間の関係に関する情報を活用**することは、3.3.1節で既に述べた[114]や[113]で発表された研究のアイデアでもある。
In contrast to other approaches, the authors create an implicit virtual network, based on the users’ access logs.
他のアプローチとは対照的に、著者らは**ユーザーのアクセスログに基づいて、暗黙の仮想ネットワーク**を作成する。
In their approach, which combines content information and collaborative filtering, the idea is to identify (two) expert users who are considered as influencers for users without a sufficiently large consumption history.
コンテンツ情報と協調フィルタリングを組み合わせた彼らのアプローチでは、十分に大きな消費履歴を持たないユーザーに対して、インフルエンサーとみなされるエキスパートユーザーを（2人）特定することをアイデアとしている.
These suspected influence relationships are then used to make the rating matrix denser.
そして、これらの影響関係が疑われるものを用いて、レーティングマトリックスをより密にするのである。
Instead of using social network information, Lu et al.[120] propose to combine different forms of user behavior, context, and content features of the news items to find similar users in sparse-data situations.
Luら[120]は、ソーシャルネットワーク情報を使う代わりに、ニュースアイテムのユーザー行動、コンテキスト、コンテンツ特徴の異なる形態を組み合わせて、スパースデータ状況下で**類似ユーザーを見つける**ことを提案している。
Specifically, they consider the user’s browsing, commenting, and publishing behavior as implicit feedback signals.
具体的には、ユーザーの閲覧、コメント、出版などの行動を暗黙のフィードバック信号とみなしています。
An even richer set of preference signals was combined in the News@hand system presented in [11, 24, 25].
[11,24,25]で紹介したNews@handシステムでは、さらに豊富な嗜好信号のセットを組み合わせている。
The authors use ontologies and Semantic Web technology to represent the knowledge about users and items and utilize a variety of preference indicators, such as page clicks, rating, and comments.
著者らは、ユーザーやアイテムに関する知識を表現するためにオントロジーとセマンティックWeb技術を用い、ページのクリック数、評価、コメントなど様々な嗜好指標を活用しています。
To deal with the sparsity problem, they then propose a graph-based method to spread the information via the semantic relations of the network of concepts.
そして、スパース性の問題に対処するために、概念のネットワークの意味関係を通じて情報を拡散するグラフベースの方法を提案している。
Li et al.[105] address the data sparsity issue by framing the recommendation task as a so called contextual bandit problem.
Liら[105]は、推薦タスクをいわゆる文脈的バンディット問題として構成することで、データスパース性の問題に対処している。
In such a problem formulation [101], every recommendation task is represented as a choice between k possible “arms” of a multi-armed bandit.
このような問題定式化 [101] では、すべての推薦タスクは、多腕バンディットのk個の可能な「腕」からの選択として表現される。
The recommendation strategy makes this choice only based on a context vector, for which Li et al.[105] chose a compact representation of users and articles (e.g., based on demographic information, location, and news categories).
推薦戦略は、この選択をコンテキストベクトルにのみ基づいて行うが、そのためにLiら[105]は、ユーザーと記事のコンパクトな表現（例えば、デモグラフィック情報、場所、ニュースカテゴリに基づく）を選択した。
Afterwards, a reward is observed based on the user reaction (click).
その後、ユーザーの反応（クリック）に応じて報酬が観測されます。
The advantage of contextual bandit approaches is that they can be used to balance exploration of the item space and exploitation of previous knowledge even in sparse data situations.
コンテキストバンディットアプローチの利点は、疎なデータ状況でもアイテム空間の探索と前知識の活用をバランスよく行うことができる点である。
Generally, one of several well-studied optimization strategies can be used to optimize the expected reward, i.e., in this case, the overall number of clicks.
一般に、よく研究されたいくつかの最適化戦略のうちの1つを使用して、期待報酬、すなわちこの場合、全体のクリック数を最適化することができる。
To evaluate the usefulness of their approach, the authors tested it on data sets with various sparsity levels.
このアプローチの有用性を評価するために、著者らは様々なスパースレベルのデータセットでテストを行いました。
Generally, when considering recommendation as a matrix completion problem, different forms of rating imputation and other forms of advanced statistical methods can be applied.
**一般に、レコメンデーションを行列補完問題として考える場合、さまざまな形式のレーティング・インピュテーションや、高度な統計的手法を適用することが可能**である。
Agarwal et al.[3], for example, analyze the correlations between different post-read actions (such as sharing, commenting, printing, or emailing article links) and are thus able to interchange the information across actions types to derive additional data points to feed into the recommendation process.
例えば、**Agarwalら[3]は、異なる読後行動（記事リンクの共有、コメント、印刷、メール送信など）間の相関を分析**し、行動タイプ間の情報を交換して、推薦プロセスに与える追加のデータポイントを導き出すことができるようにしている。
Overall, a number of techniques for dealing with the data sparsity issue in the news domain were presented over the years.
全体として、ニュース領域におけるデータスパース性の問題に対処するための多くの技術が長年にわたって発表されました。
Since data sparsity is such a central problem in news recommendation, many papers evaluate their algorithmic proposals – even when they are not explicitly focusing on data augmentation – on data sets of different densities to analyze their behavior in such situations.
データの疎密はニュース推薦の中心的な問題であるため、多くの論文では、データ増強に明確に着目していない場合でも、異なる密度のデータセットでアルゴリズムの提案を評価し、そのような状況での挙動を分析しています。

## 3.4. The Importance of Considering the Recency of News Articles ニュース記事の新着順を考慮することの重要性

Whatever algorithm is used for making personalized reading suggestions, the recency or “freshness” of an article will impact its relevance for the readers in many cases.
パーソナライズされた読書提案を行うためにどのようなアルゴリズムが使われるにせよ、**記事の"recency"や“freshness”は、多くの場合、読者にとっての関連性に影響を与えます**。
Clearly, there are recommendation scenarios where a reader might be interested in older news as well, e.g., when investigating the development of a story over time or when looking for articles related to the currently read one.
例えば、ある記事の時間経過に伴う展開を調べる場合や、現在読んでいる記事に関連する記事を探す場合など、**読者が古いニュースにも興味を持つようなレコメンデーションシナリオがあることは明らか**である。
On typical landing pages of news sites, however, the recency of the articles is typically one important ranking criterion besides other factors such as the estimated general attractiveness of an article.
しかし、一般的なニュースサイトのランディングページでは、記事の新しさは、記事の一般的な魅力度などの他の要素に加えて、重要なランキング基準の1つとなっているのが普通です。
Technically, the recency of an article can be considered in the recommendation process at three stages.
**技術的には、レコメンデーションプロセスにおいて、記事のrecencyを3段階で考慮することができます**。
We can filter assumedly outdated news before computing relevance predictions or an item ranking (pre-filtering); we can incorporate the recency factor into the algorithms themselves (recency modeling); or we can filter or downrank articles after the main ranking process (post-filtering).
関連性予測やアイテムのランキングを計算する前に、古いと思われるニュースをフィルタリングする（プリフィルタリング）、アルゴリズム自体に新着度要素を組み込む（新着度モデリング）、あるいはランキング処理の後で記事をフィルタリングしたりダウンランクしたりする（ポストフィルタリング）。
However, one key design question in this context is how we balance the possible trade-off between article freshness and assumed relevance for the individual user.
しかし、この文脈における重要な設計上の問題は、記事のfreshnessと個々のユーザにとっての想定される関連性との間で起こりうる**トレードオフ**のバランスをどのようにとるかということです.(recencyの高いニュースか、古いがユーザとのrelevanceの高いニュースか、どちらを選ぶべきかのトレードオフ??)
Examples of works that apply a pre-filtering strategy are [39, 41], and [159].
プレフィルタリング戦略を適用した作品の例としては、[39, 41]や[159]がある。
In one of the news recommendation approaches by Desarkar and Shinde [41], for example, the authors selected the 100 most recent articles from the user’s preferred publisher websites and considered only these articles in the subsequent ranking process.
例えば、Desarkar and Shinde [41]によるニュース推薦アプローチの1つでは、著者はユーザーが好む出版社のウェブサイトから最新の100記事を選択し、その後のランキングプロセスでこれらの記事のみを考慮しました。
Das et al.[39], on the other hand, considered recency as one of several factors for item pre-filtering; other factors being, for example, the user’s language preferences or user-defined topics of interest.
一方、Dasら[39]は、アイテムのプレフィルタリングのためのいくつかの要因の1つとして、他の要因、例えば、ユーザの言語嗜好やユーザが定義した興味のあるトピックを考慮して、再検索性を考慮した。

In recency modeling approaches, the freshness of an article is considered simultaneously in conjunction with different other features of the item or the user.
Recencyモデリングアプローチでは、記事の新鮮さは、アイテムやユーザの他の異なる特徴量と同時に考慮される。
In principle, such an approach has the advantage that the different factors can more easily be balanced in an integrated way compared to when assumedly outdated items are filtered in a separate process and with separate heuristics.
原則的に、このようなアプローチは、**古いと想定されるアイテムを別々のプロセスで、別々のヒューリスティックでフィルタリングする場合に比べ、異なる要素をより簡単に統合的にバランスさせることができる**という利点があります。
Examples of recency modeling approaches include [12, 148], and [182].
recency モデリングアプローチの例として、[12, 148]、[182]がある。
In the work by Pon et al.[148], freshness is considered along with a “multiple topic tracking” technique for users with several interests to train a news classifier.
Ponら[148]の研究では、ニュース分類器を学習するために、複数の興味を持つユーザーのための「複数トピック追跡」技術とともに、鮮度が考慮されています。
To this end, users are represented by a number of vectors instead of just a single average Term Frequency-Inverse Document Frequency (TF-IDF) vector, which is commonly used to weight the importance of keywords.
このため、キーワードの重要度を重み付けするために一般的に用いられる平均的なTF-IDF（Term Frequency-Inverse Document Frequency）ベクトル1つではなく、**複数のベクトルでユーザーを表現しています。**
In this way, short-term topic interest can be accounted for by giving preference to user profile vectors that have the highest similarity to the recently consumed news articles.
このように、最近消費されたニュース記事との類似度が高いユーザープロファイルベクトルを優先することで、短期的な話題の関心を説明することができるのです。
Yeung and Yang [182] propose an approach that relies on a variety of features to predict the relevance of news articles (e.g., user features, item features, usage patterns, and context factors).
Yeung and Yang [182]は、ニュース記事の関連性を予測するために、様々な特徴（例：ユーザー特徴、アイテム特徴、使用パターン、コンテキスト要因）に依存するアプローチを提案する。
The freshness of an article is considered as one of the item features and more recent articles receive a higher weight in the ranking process.
**記事の鮮度をアイテムの特徴量の1つと考え**、より新しい記事ほどランキングで高いウェイトを占めます。
Similarly, Bielikova et al.[12] integrated the ´ publication time of an article as one of the factors in their tree-based model for computing the relevance of the articles.
同様に、Bielikovaら[12]は、記事の関連性を計算するためのツリーベースのモデルにおいて、記事の出版時間（´）を要因の1つとして統合した。

Post-filtering based on article recency was applied, for example, in [108, 186], and [129].
例えば、[108, 186]や[129]では、記事の再録に基づくポストフィルタが適用された。
In the method by Zheng et al.[186], news articles are first ranked according to their estimated relevance based on the interest groups the user belongs to.
Zhengら[186]の方法では、まずニュース記事が、ユーザーが所属するインタレストグループに基づく推定関連性に従ってランク付けされる。
In a second step, the ranking is adjusted based on item freshness and popularity.
第2ステップでは、アイテムの鮮度や人気度に基づいてランキングを調整する。
A similar two-stage approach was adopted by Li et al.[108], which was already explained in detail in Section 3.3.1.
同様の2段階アプローチを採用したのはLiら[108]で、これはすでに3.3.1節で詳しく説明したとおりである。
A decay-based method has been proposed by Medo et al.[129].
減衰に基づく方法がMedoらによって提案されている[129]。
In their work, they tested different score decay strategies for old news (no decay, medium decay, strong decay) and evaluated the impact of these strategies on the performance of the news recommender system.
彼らの研究では、古いニュースに対するさまざまなスコア減衰戦略（減衰なし、中程度の減衰、強い減衰）をテストし、これらの戦略がニュース推薦システムの性能に与える影響を評価しました。
Generally, to what extent older articles should be filtered can depend on different factors.
**一般的に、古い記事をどの程度フィルタリングするかは、さまざまな要因によります。**
First, in case of cold-start users with a very short reading history, we can resort to focusing the recommendations on articles that were recently added and which are relatively popular [49, 53, 166].
まず、読書履歴が非常に短いコールドスタートユーザーの場合、最近追加された、比較的人気のある記事に推薦を集中させるという方法がある [49, 53, 166]。
Such non-personalized recommendations might however lead to lower user satisfaction.
しかし、このような非個性的なレコメンデーションは、ユーザーの満足度を下げることにつながるかもしれません。
Filtering out older articles can also be problematic if there are many readers who are interested in investigating developing stories and in reading older news articles on the same topic.
**また、同じ話題の古い記事を読みたい読者が多い場合、古い記事をフィルタリングしてしまうことも問題**です。
Finally, whether or not it is good to focus strongly on the latest news in the recommendations can even depend on the individual user and his or her current context and goals.
最後に、**レコメンデーションで最新のニュースに強くフォーカスすることが良いかどうかは、個々のユーザやその人の現在の状況や目標に依存することさえある**のです。
One might be interested to catch up with the latest news in the morning during the week, but be more interested in longer (and perhaps older) stories when visiting the news site on the weekend.
平日の朝は最新のニュースをチェックしたいが、週末にニュースサイトを訪れると、より長い（そしておそらく古い）ストーリーに興味を持つかもしれない。
In any case, an open question seems to be how to select a threshold to filter old news or how to set a decay factor.
いずれにしても、古いニュースをフィルタリングするための閾値をどう選ぶか、あるいは減衰係数をどう設定するかが未解決の問題のようです。
When reviewing the literature, a number of different strategies and threshold values are used and it is not clear if an approach that is working well in one setting will also be suitable for another use case.
文献を調べると、さまざまな戦略や閾値が使われており、ある環境でうまくいっているアプローチが、別のユースケースにも適しているかどうかは明らかではありません。
In many cases, details about the specific settings are not reported in the research papers, which makes these works hard to reproduce.
また、研究論文では具体的な設定の詳細が報告されていない場合が多く、再現が難しい作品です。
Table 1 gives an overview of approaches that consider item recency as a relevant factor.
表1は、アイテムの再利用性を関連する要素として考慮するアプローチの概要を示している。
In the last two columns, we show which thresholds were applied in case they were reported and which time windows were used to decrease the relevance of an article based on its recency.
最後の2列では、報告された場合にどの閾値を適用したのか、また、どのタイムウィンドウを使用して、記事の再来性に基づいて関連性を低下させたのかを示しています。
We can observe significant differences.
大きな違いを観察することができます。
Some works only focus on articles of the last six hours [49], whereas others consider articles of the last twenty days [136].
過去6時間の記事のみに着目した作品[49]もあれば、過去20日の記事を考慮した作品もある[136]。
Some authors add a decay penalty for every second since the article was published [38], whereas others do this only for each hour [183].
ある著者は、記事が公開されてから1秒ごとに減衰ペナルティを追加する[38]が、他の著者は1時間ごとにのみこれを行う[183]。
In many cases, however, this detailed information is unfortunately not reported at all.
しかし、このような詳細な情報は、残念ながら全く報告されていないケースも多いのです。

Table 1: Overview of news recommendation approaches that consider recency as a factor.
表1： recency を要因として考慮したニュース推薦アプローチの概要
The first column categorizes the papers according to their recency strategy.
最初の列は、再録戦略によって論文を分類したものである。
The next two columns list the paper’s author(s) and its publication year.
次の2列は、論文の著者名と発表年です。
The fourth column shows the employed recommendation strategy (CB = Content-based filtering, CF = Collaborative filtering, H = Hybrid).
4列目は採用した推薦戦略（CB＝コンテンツベースフィルタリング、CF＝協調フィルタリング、H＝ハイブリッド）を示しています。
The fifth column lists the data sets used in the paper.
5列目は論文で使用したデータセットの一覧です。
The last two columns show (a) how old articles can be at most to be considered recent and (b) the granularity of applying a decay factor, e.g., for every hour after the initial publication.
最後の2列は、(a)どの程度古い記事であれば最近の記事とみなせるか、(b)減衰係数を適用する粒度（例えば、最初の公開から1時間ごと）を示しています。

## 3.5. Considering Quality Factors Beyond Prediction Accuracy 予測精度を超えた品質要素を考慮する

The main optimization goal of researchers in academia is to accurately predict the relevance of a news item for a user.
学術界の研究者の主な最適化目標は、ユーザにとってのニュースの関連性を正確に予測することです。
Most commonly, classification or ranking accuracy measures are used for that purpose (see Section 4 for more details).
最も一般的には、そのために分類やランキングの精度測定が用いられる（詳細はセクション4参照）。
However, in practice, predicting the relevance of an item is in many cases not enough.
しかし、実際には、アイテムの関連性を予測するだけでは不十分な場合が多い。
If, for example, a user is interested in politics and has shown strong interest in articles about an ongoing presidential election in the past, recommending more articles about this topic is probably a good choice.
例えば、ユーザが政治に興味があり、過去に現在進行中の大統領選に関する記事に強い関心を示した場合、このトピックに関する記事をより多く推薦することは、おそらく良い選択であると思います。
However, recommending solely articles about the election, or solely about politics, might be too monotonous for users and would probably not lead to high user engagement in the future.
しかし、選挙に関する記事だけ、あるいは政治に関する記事だけをレコメンドするのは、ユーザーにとってあまりにも単調で、将来的に高いユーザーエンゲージメントにつながらないかもしれません。
In case of a news aggregation site, it is furthermore important that the recommended news are not too similar to each other.
ニュースアグリゲーションサイトの場合、さらに、推薦されたニュースがあまりに類似していないことも重要である。
Presenting three articles from three different sources about, e.g., the same plane accident might be of little value for users.
例えば同じ飛行機事故について、3つの異なるソースから3つの記事を提示しても、ユーザーにとってはあまり意味がないかもしれません。
Therefore, one additional challenge, besides accurately predicting whether an article is relevant for a user or not, is to take additional quality factors into account.
したがって、ユーザーにとって関連性のある記事かどうかを正確に予測すること以外に、さらに品質要素を考慮することが一つの課題となっています。
In the recommender systems literature, diversity, novelty, and serendipity are often considered as such quality factors that have to be balanced with prediction accuracy (see, e.g., [29]).
推薦システムの文献では、多様性、新規性、セレンディピティは、しばしば予測精度とバランスを取らなければならない品質要因として考えられている（例えば、[29]を参照）。

### 3.5.1. Diversity 多様性

Users of news recommender systems can be interested in a variety of topics.
ニュースレコメンダーシステムのユーザーは、様々なトピックに興味を持つことができます。
A recommender system should therefore be able to address these varied tastes and generate diversified recommendation lists [171].
したがって、レコメンダーシステムは、このような多様な嗜好に対応し、多様な推薦リストを生成することができる必要がある[171]。
Empirical research suggests that increasing the diversity of the recommendations can lead to a better quality perception by users [48, 151, 188].
経験的な研究によると、推薦文の多様性を高めることで、ユーザーによる品質認識の向上につながることが示唆されている [48, 151, 188]．
An example for a work that considers diversity in the news recommendation domain is presented in [108], which we already mentioned earlier in the context of recency filtering and cold-start techniques.
ニュース推薦の領域で多様性を考慮した例としては、先に再帰性フィルタリングとコールドスタート技術の文脈で紹介した[108]がある。
In the proposed two-stage approach, articles were clustered in the first phase, and the recommendations were personalized and adapted, e.g., with respect to recency, in the second phase.
提案された2段階のアプローチでは、第1段階で記事がクラスター化され、第2段階で推薦文がパーソナライズされ、例えば、再来性に関して適応される。
In both stages, the authors propose to add some level of diversification.
どちらの段階でも、ある程度の分散を加えることを提案しています。
According to the authors, the first-level clustering strategy implicitly introduces some level of topic diversity, while the second stage implements a greedy approach that explicitly minimizes the similarity among items in a recommendation set.
著者らによると、第一段階のクラスタリング戦略は、暗黙のうちにある程度のトピックの多様性を導入し、第二段階では、推薦セット内のアイテム間の類似性を明示的に最小化する貪欲なアプローチを実装しているとのことである。
In the latter case, the diversity was measured by computing the average pairwise (dis-)similarity of documents, and an experimental evaluation showed that their approach was beneficial in terms of both accuracy and diversity when compared to the works presented in [31, 39, 105, 115].
後者の場合、多様性は文書の平均的なペアワイズ（dis-）類似度を計算することで測定され、実験的評価では、[31, 39, 105, 115]で示された作品と比較して、彼らのアプローチが精度と多様性の両方の面で有益であることが示された。
Later on, Li and Li [107] followed an alternative and more advanced approach to diversify news recommendations in the context of a learning-to-rank optimization scheme.
その後、LiとLi [107]は、学習ランク最適化スキームの文脈で、ニュース推薦を多様化するための代替的かつより高度なアプローチを踏襲した。
In their work, they propose a framework that relies on a hypergraph to model the relations between different “media objects”, which included users, news articles, topics, and named entities.
彼らは、ユーザー、ニュース記事、トピック、名前付きエンティティなどの異なる「メディアオブジェクト」間の関係をモデル化するために、ハイパーグラフに依存するフレームワークを提案しました。
Using the same experimental setup as in their previous work [108], the authors were able to demonstrate further improvements both in terms of accuracy and diversity.
前作[108]と同じ実験装置を用いて、精度と多様性の両面でさらなる向上を実証することができた。
Typically, there is a trade-off between accuracy, e.g., in terms of classification accuracy, and diversity, e.g., in terms of intra-list similarity [188].
一般的に、分類精度などの精度と、リスト内類似度などの多様性との間にはトレードオフがある[188]。
To address this issue, Desarkar and Shinde [41] analyzed two possible approaches of balancing these goals in the news domain and tested them for a special privacy-targeted scenario where no past interaction history is available for the users and the relevance of each candidate item is consequently estimated only by its popularity.
この問題に対処するため、Desarkar and Shinde [41]は、ニュース領域でこれらの目標をバランスさせる2つの可能なアプローチを分析し、ユーザが過去の対話履歴を利用できず、各候補アイテムの関連性が結果としてその人気のみによって推定される、プライバシーを対象とした特殊シナリオでそれらをテストしました。
In their case, diversification is described as a bi-criteria optimization problem where both the relevance and the dissimilarity between the news objects should be high.
彼らの場合、多様化は、ニュース対象間の関連性と非類似性の両方が高いことが望ましいという二基準最適化問題として記述されている。
Outside the domain of news recommendation, a number of works have been published over the past ten years on the topic of diversifying recommendations [29].
ニュース推薦の領域以外でも、推薦の多様化というテーマで過去10年間に多くの研究が発表されている[29]。
Besides the question of how to balance diversity with accuracy, researchers investigated to what extent the level of diversification should be determined by the preferences of the individual user [162] or how diversity preferences can depend on time aspects [102].
多様性と精度のバランスをどうとるかという問題以外にも、研究者は、多様化のレベルは個々のユーザーの好みによってどの程度決定されるべきか[162]、あるいは多様性の好みは時間的側面によってどのように変わるか[102]を調査しました。
In the news domain, these aspects have not been investigated much yet, even though some of these aspects – like the consideration of the time of the day when recommending [40] – might have an effect on the user’s short-term diversity preferences.
ニュース領域では、これらの側面はまだあまり研究されていません。推薦時に時間帯を考慮する [40] などの側面が、ユーザーの短期的な多様性選好に影響を与える可能性があるにもかかわらずです。

### 3.5.2. Novelty ノベルティ

Novelty, as a quality criterion for recommendations, was defined in terms of the non-obviousness of the item suggestions by Herlocker et al.[68].
レコメンデーションの品質基準としての新規性は、Herlockerら[68]によってアイテム提案の非自明性という観点から定義されている。
Informally, novel items are, according to their definition, those that the user has not seen yet, but which are relevant to him or her.
非公式には、その定義によれば、新規性のあるアイテムとは、ユーザーがまだ見たことのないもので、かつ、ユーザーにとって関連性のあるものである。
An alternative definition was provided by Vargas and Castells [172], who defined novelty as the inverse general popularity of an item.
VargasとCastells [172]は、新規性を項目の一般的な人気の逆数として定義している。
The assumption here is that less popular items are more likely to be unknown to users and recommending long-tail items will, in general, lead to higher novelty levels.
ここでは、人気のないアイテムはユーザーにとって未知のものである可能性が高く、ロングテールのアイテムを推奨することで、一般的に新規性レベルが高くなると仮定しています。
Several ways of numerically quantifying the degree of novelty are possible, including alternative ways of considering popularity information [187] or the distance of a recommendable item to the user’s profile [137, 154].
新規性の程度を数値化する方法としては、人気情報を考慮する代替方法[187]や、ユーザーのプロフィールと推奨アイテムの距離[137, 154]など、いくつかの方法が考えられます。
Like diversity and accuracy, novelty and accuracy aspects can represent a trade-off.
多様性と正確性のように、新規性と正確性の側面はトレードオフを表すことがあります。
In their work on news recommendation, Garcin et al.[53] relied on the definition by Herlocker et al.[68] and tested different configurations of weighting the two factors to achieve both high accuracy and high novelty.
Garcinら[53]は、ニュース推薦に関する研究において、Herlockerら[68]の定義に依拠し、高精度と高新奇性を両立させるための2要素の重み付けの異なる構成を検証した。
Rao et al.[154] followed an approach where the novelty of an item is defined by its distance to the user’s profile.
Raoら[154]は、アイテムの新規性をユーザーのプロファイルとの距離で定義するアプローチに従った。
Specifically, they compared the distance of the concepts appearing in the user profile and the news article, where the taxonomy was constructed from encyclopedic knowledge.
具体的には、百科事典的な知識からタクソノミーを構築したユーザープロフィールとニュース記事に登場する概念の距離を比較したのです。
The evaluation results of their user study show that this approach cannot only be used to increase accuracy but also reduce the perceived redundancy among news articles.
彼らのユーザー研究の評価結果は、このアプローチが精度を高めるだけでなく、ニュース記事間で認識される冗長性を低減するために使用されることを示しています。
Generally, as for diversity, the “optimal” degree of novelty can depend on the user’s current situation and context, as discussed recently by Kapoor et al.[89] in the context of the music domain.
一般に、多様性については、Kapoorら[89]が音楽領域の文脈で最近議論したように、新規性の「最適」な程度はユーザの現在の状況や文脈に依存し得る。
Determining the right balance of recommending (a) things that are most likely relevant for the user and (b) recommending items that help the user discover new things remains challenging.
(a)ユーザーにとって関連性の高いものを推薦し、(b)ユーザーの新しい発見を助けるものを推薦する、というバランスを取るのは難しいことです。
Limited research on these aspects exists in the news recommendation domain.
ニュース推薦の領域では、これらの側面に関する研究は限られています。
As discussed in Section 3.3.1, the news domain has the special characteristic that most of the recommendable items are usually new and unknown to the readers.
3.3.1節で述べたように、ニュース領域は、推奨されるアイテムのほとんどが、通常、読者にとって新しく、未知のものであるという特別な特徴を持つ。
In terms of some of the definitions from above, all recommendations are novel.
上記のいくつかの定義からすると、すべての推奨事項は新規性のあるものです。
Therefore, novelty can probably not be determined on the basis of the individual item itself, but rather in terms of the content the news item is about, e.g., based on whether or not the user already knows about the real-world event the news item is reporting on.
したがって、新規性は、おそらく個々の項目それ自体に基づいて決定されるのではなく、ニュース項目に関する内容、例えば、ニュース項目が報道している現実世界の出来事についてユーザーが既に知っているか否かに基づいて決定され得るのである。

### 3.5.3. Serendipity セレンディピティ

Serendipity is sometimes also mentioned as a desirable quality characteristic of recommendations.
また、セレンディピティは、レコメンデーションの望ましい品質特性として挙げられることもあります。
Herlocker et al.[68] describe serendipitous recommendations as those that help users find surprising and interesting items that they might not have noticed otherwise.
Herlockerら[68]は、セレンディピタス推奨とは、ユーザーが他の方法では気づかなかったかもしれない、意外で興味深いアイテムを見つけるのを助けるものであると説明している。
Ge et al.[57], based on an earlier approach by Murakami et al.[135], defined serendipitous recommendations as items that are not only novel but also positively surprising for the user and proposed a generic metric based on the concepts of unexpectedness and usefulness.
Geら[57]は、Murakamiら[135]による先行アプローチに基づき、セレンディピタス推薦を、新規性だけでなく、ユーザーにとって積極的に驚くようなアイテムと定義し、意外性と有用性の概念に基づく汎用的なメトリックを提案している。
Zhang et al.[185] finally proposed a related conceptualization in the context of a music recommendation application in which the level of serendipity is determined based on the distance between the recommendations and the user’s expected content.
Zhangら[185]は、音楽推薦アプリケーションの文脈で、セレンディピティのレベルを推薦内容とユーザーの期待するコンテンツとの距離に基づいて決定する、関連する概念化をついに提案した。
To our knowledge, only limited research on serendipity aspects of the news recommendation problem exist so far.
私たちの知る限り、ニュース推薦問題におけるセレンディピティの側面に関する研究は、これまで限られたものでしかありませんでした。
In principle, one can apply techniques based on Latent Dirichlet Allocation (LDA) models – as proposed by Zhang et al.[185] for music recommendation – to the news domain and focus on recommending news items that are content-wise dissimilar to the user’s typical latent topics.
原理的には、Zhangら[185]が音楽推薦のために提案したLDA（Latent Dirichlet Allocation）モデルに基づく技術をニュース領域に適用し、ユーザーの典型的な潜在的話題と内容的に異質なニュース項目を推薦することに焦点を当てることができます。
However, whether or not this will lead to higher levels of user satisfaction in this domain, still has to be explored.
しかし、それがこの領域でのユーザー満足度の向上につながるかどうかは、まだ検討の余地があります。
Overall, one key question today is how to quantify the level of serendipity of a recommendation list and how such serendipity measures would be related to existing novelty measures.
全体として、今日の一つの重要な問題は、推薦リストのセレンディピティのレベルをどのように定量化するか、そしてそのようなセレンディピティ測定が既存の新規性測定とどのように関連するかということです。
Again, adding serendipitous items to the recommendations comes with the risk of decreasing the average relevance of the recommendation lists.
この場合も、セレンディピティなアイテムを推薦文に加えることは、推薦文の平均的な関連性を低下させるリスクを伴います。
Furthermore, Kotkov et al.[99] recently discussed the problem that today in many (general RS) research data sets used for offline experimentation not enough information about the user’s context (e.g., time, location, or mood) is available.
さらに、Kotkovら[99]は最近、オフライン実験に使われる多くの（一般的なRS）研究データセットにおいて、ユーザーのコンテキスト（時間、場所、気分など）に関する情報が十分に得られないという問題を論じている。
The user’s context can however have a significant impact on the user’s perception of serendipitous item recommendations.
しかし、ユーザーの文脈は、セレンディピティなアイテム推薦に対するユーザーの認識に大きな影響を与える可能性があります。
In our view, more research is therefore required also outside the field of news recommendations to better understand the concept of serendipity in recommender systems and how to measure it.
したがって、推薦システムにおけるセレンディピティの概念とその測定方法をよりよく理解するためには、ニュース推薦の分野以外でもさらなる研究が必要だと考えています。

## 3.6. Scalability Issues スケーラビリティの問題

Scalability is the last of the main challenges of news recommendation that we discuss in this section.
スケーラビリティは、本節で述べるニュースレコメンデーションの主な課題の最後である。
Large news websites like Google News can have hundreds of millions of users per month.
Google Newsのような大規模なニュースサイトでは、1ヶ月に数億人のユーザーが利用することもあります。
At the same time, the number of articles that can be searched and recommended can be huge as well, with thousands of new items appearing every day.6 A common approach to deal with these huge amounts of data is to apply clustering techniques of different types.
同時に、検索や推薦できる記事の数も膨大で、毎日何千もの新しいアイテムが登場します6。**このような膨大なデータを扱うための一般的なアプローチとして、さまざまなタイプのクラスタリング技術を適用することが挙げられ**ます。
Clustering can in many cases help to speed up the computations; it can however also lead to compromises with respect to the accuracy of the relevance predictions.
クラスタリングは多くの場合、計算を高速化するのに役立ちますが、関連性予測の精度に関しても妥協することになりかねません。
In addition to such algorithmic approaches that, e.g., allow us to do the computations on a more coarse-grained level, researchers often propose to rely on distributed computing mechanisms and to execute the calculations on multiple servers in parallel.
このようなアルゴリズム的なアプローチに加え、例えば、より粗い粒度で計算を行うことができるように、研究者はしばしば分散コンピューティング機構に依存し、複数のサーバーで並行して計算を実行することを提案します。
The application of various forms of clustering techniques for different aspects of the news recommendation problem has been proposed, e.g., in [39, 120, 129], and [174].
ニュース推薦問題の様々な側面に対して、様々な形式のクラスタリング技術の適用が、例えば[39, 120, 129]、[174]で提案されています。
In some of these cases, the main goal is to search for similar users (neighbors) only within a smaller cluster of users without the need to scan the entire database.
このような場合、データベース全体をスキャンする必要がなく、より小さなクラスタ内で類似したユーザ（ネイバー）だけを検索することが主な目的である場合があります。
In the case of the Google News system, as described in [39], the authors use a combination of (MinHash) clustering and distributed computing based on the MapReduce framework to make the approach scalable.
Google Newsシステムの場合、[39]に記載されているように、著者らは、アプローチをスケーラブルにするために、（MinHash）クラスタリングとMapReduceフレームワークに基づく分散コンピューティングを組み合わせて使用しています。
Lu et al.[120] also combine MapReduce and a clustering technique to increase the scalability.
Luら[120]もMapReduceとクラスタリング技術を組み合わせて、スケーラビリティを高めている。
Specifically, they use a “Jaccard–Kmeans” based clustering technique where the similarity of users is computed in multiple dimensions, e.g., based on their past behavior and the content the users preferred in the past.
具体的には、「Jaccard-Kmeans」ベースのクラスタリング手法を用い、ユーザーの過去の行動や過去にユーザーが好んだコンテンツなどに基づいて、ユーザーの類似性を多次元的に計算します。
Other examples of works on news recommendation that rely on distributed computing include [156] and [159].
分散コンピューティングに依存したニュース推薦の他の例として、[156]や[159]がある。
Besides clustering the users, one can also try to cluster the available news articles and group them based on their features and the user’s preferences.
ユーザーをクラスタリングする以外に、利用可能なニュース記事をクラスタリングし、その特徴やユーザーの好みに基づいてグループ化することも試みられます。
In [108], for example, the authors propose a two-stage recommendation approach in which they apply different clustering techniques to create a hierarchy of news clusters.
例えば、[108]では、**異なるクラスタリング技術を適用してニュースクラスターの階層を作成する2段階推薦アプローチを提案**している。
This hierarchy can then be efficiently traversed from top to bottom to find a set of news articles similar to the user’s reading interest.
この階層を上から下へ効率的に走査することで、ユーザーの読書関心に近いニュース記事群を見つけることができる。
Medo et al.[129] adopt a different approach to achieve scalability in the context of a news platform where users can post news items.
Medoら[129]は、ユーザーがニュースを投稿できるニュースプラットフォームの文脈で、スケーラビリティを達成するために異なるアプローチを採用しています。
In their method, they construct a local neighborhood network of users based on the similarity of their rating behavior (likes/dislikes).
彼らの手法では、ユーザーの評価行動（好き嫌い）の類似性に基づいて、ユーザーの局所近傍ネットワークを構築する。
In contrast to traditional k-nearest-neighbor (kNN) approaches, they do not store the whole neighborhood, but only the most similar neighbors for each user.
従来のk-nearest-neighbor（kNN）アプローチとは異なり、近傍全体を保存するのではなく、各ユーザーの最も類似した近傍のみを保存することができます。
Once a user posts a new article on the system, it is propagated along the directed edges of the graph to their “followers”, who can spread it further by liking it.
ユーザーが新しい記事をシステムに投稿すると、その記事はグラフの有向辺に沿って「フォロワー」に伝播され、フォロワーはその記事を「いいね！」することでさらに拡散することができます。
The final ranking of the news items is then determined by a score, which is based on the like/dislike statements of the target user’s neighbors.
そして、最終的なニュースの順位は、対象ユーザーの近隣住民の「いいね！」「嫌だ」の発言に基づくスコアによって決定されます。
In a follow-up work, Wei et al.[174], expand the method by adapting it to take the users’ reading patterns into account.
Weiら[174]は、ユーザーの読書パターンを考慮するよう適応させることで、この手法を拡張している。
Additionally, they propose different stochastic solutions to the problem of updating the neighborhood that improve the scalability of their approach further, e.g., by randomly selecting new neighbors.
さらに、近傍の更新問題に対して、新しい近傍をランダムに選択するなど、アプローチのスケーラビリティをさらに向上させるさまざまな確率的解決策を提案しています。
Many of above-mentioned approaches describe how to achieve scalability on a theoretical level or give an account of how real-world systems implement large-scale operations, as in the case of [39].
上記のアプローチの多くは、理論的なレベルでスケーラビリティを実現する方法を説明したり、[39]のように実世界のシステムがどのように大規模なオペレーションを実現しているかを説明したりするものである。
What sets the news domain apart from other domains that are investigated in recommender systems research, however, are the live news recommendation challenges organized by Plista, which we will explain in detail in Section 4.2.Such challenges give researchers the opportunity to test the scalability of their approaches “in the wild”.
しかし、ニュース領域が推薦システム研究で研究される他の領域と異なるのは、4.2節で詳しく説明するPristaが主催する**ライブニュース推薦チャレンジ(?)**です。このチャレンジは、研究者がアプローチの拡張性を「野生の」状態でテストする機会を提供します。
An example is the work by Doychev et al.[45], whose content-based recommender system addresses the requirement of the Plista challenge to respond quickly to a large amount of recommendation requests using a variety of state-of-the-art data processing and management technologies.
その一例として、Doychevら[45]によるコンテンツベースのレコメンダーシステムは、様々な最先端のデータ処理・管理技術を用いて、大量の推薦リクエストに素早く対応するというPrista challengeの要件に対応している。
These range from a two-tiered load balancing stage (Nginx, Tornado), to query execution using a nonrelational database and full-text search engine (MongoDB, ElasticSearch), to a recommendation cache based on an in-memory database (Redis).7 In practice, this results in average response times of about only 3 ms.
2層の負荷分散ステージ（Nginx、Tornado）から、非リレーショナルデータベースと全文検索エンジン（MongoDB、ElasticSearch）を使ったクエリ実行、インメモリデータベース（Redis）に基づくレコメンデーションキャッシュまで、さまざまなものがあります7 。
In conclusion, the amount of literature on this issue shows that the scalability problem has been addressed to a certain degree by the news recommender research community.
結論として、この問題に関する文献の多さは、ニュースレコメンダー研究コミュニティによってスケーラビリティ問題がある程度解決されていることを示しています。
Nonetheless, because of the constant increase in the amount of available online news articles, scalability remains one of the key problems in this domain, and, thus, more sophisticated solutions and further scalability-oriented evaluations are necessary.
しかしながら、利用可能なオンラインニュース記事の量は常に増加しているため、スケーラビリティはこの領域における重要な問題の1つであり、したがって、より洗練されたソリューションとスケーラビリティを重視した評価が必要である。

## 3.7. Discussion ディスカッション

The review of recent works in this section shows that during the last ten years substantial efforts went into the development of new techniques to deal with the particular challenges of news recommendation.
このセクションで最近の研究成果を概観すると、過去10年間、ニュース推薦という特殊な課題に対処するための新しい技術の開発に多大な努力が払われてきたことがわかる。
Figure 2 shows the distribution of topics and challenges that were addressed in the reviewed works.
図2は、レビューされた作品で扱われたトピックと課題の分布を示したものです。
The diagram shows that the largest number of papers was devoted to the problems of user profiling, which is a common challenge for all recommender systems domains.
この図から、すべてのレコメンダーシステムドメインに共通する課題であるユーザープロファイリングの問題に、最も多くの論文が割かれていることがわかります。
Additionally, a number of papers focus on the specific problems of data sparsity and user and item cold-start.
さらに、データの疎密やユーザーとアイテムのコールドスタートという特定の問題に焦点を当てた論文も多数あります。
This is in fact expected, given that news recommendation systems face a continuous item cold-start situation, and personalization techniques that work well, e.g., for movie recommendation, do not always work well under such circumstances.
これは、ニュース推薦システムが連続アイテムのコールドスタート状態に直面しており、例えば映画の推薦ではうまく機能するパーソナライズ技術が、このような状況では必ずしもうまく機能しないことを考えると、実際、予想されることである。
Also, it is not very surprising that recency aspects received a lot of interest, due to the unique short-livedness of the items in the domain.
また、ドメインに含まれるアイテムのユニークな短命性から、recencyの側面が多くの関心を集めたことはあまり驚くべきことではありません。

Figure 2: Distribution of research challenges (other than accuracy) addressed by news recommendation papers published in the last decade.
図2：過去10年間に発表されたニュース推薦論文が取り上げた研究課題（精度以外）の分布。
Each paper can fall into multiple categories.
各論文は、複数のカテゴリーに分類することができます。

Beginning around the year 2011, we observe more and more papers on beyond-accuracy quality aspects like diversity, novelty, and serendipity, i.e., topics that were not strongly in the focus of researchers in earlier years.
2011年頃から、多様性、新規性、セレンディピティなど、精度を超えた品質に関する論文が多く見られるようになり、以前はあまり注目されていなかったテーマが注目されています。
This recent trend can be considered as a positive development, since it has already been shown in other domains in which recommenders have been applied that focusing solely on accuracy measures to compare algorithms can be insufficient and potentially misleading [80, 128].
というのも、**アルゴリズムを比較するために精度の指標だけに注目するのは不十分であり、誤解を招く可能性があることが、推薦者が適用された他のドメインですでに示されているから**です[80, 128]。
Nonetheless, more work is needed to better understand how to balance the sometimes competing goals of achieving high prediction accuracy and, for example, list diversity in parallel.
それでも、高い予測精度を達成することと、例えばリストの多様性を並列に実現することなど、時に相反する目標を両立させる方法をよりよく理解するためには、さらなる研究が必要です。
Looking at the different challenges discussed in this section so far, we can identify a number of additional areas in which more work is still required.
このセクションで説明したさまざまな課題を見ると、さらに多くの課題があることがわかります。
In the context of user modeling, for example, a number of papers differentiate between long-term preferences and short-term interests.
例えば、**ユーザーモデリングの文脈では、多くの論文が長期的な嗜好と短期的な興味を区別しています。**
In our view, it is however not fully clear yet how these aspects should be balanced, how we can deal with an interest drift over longer periods of time, or how we should deal with exceptional events and specific contextual conditions, which induce a probably only short-lived interest at the user’s side.
しかし、これらのバランスをどのようにとるべきか、また、より長い期間にわたる興味のドリフトにどのように対処するか、あるいは、ユーザー側でおそらく短期間の興味を引き起こすような例外的な出来事や特定の文脈的条件にどのように対処すべきかは、まだ十分に明らかになっていない、と私たちは考えている。

Furthermore, in terms of user modeling, today’s news sites also provide only limited ways for users to explicitly inform the recommender about their preferences or to give the system feedback on individual recommendations.
さらに、ユーザーのモデル化という点でも、現在のニュースサイトでは、ユーザーが自分の好みを推薦者に明示的に伝えたり、個々の推薦に対してシステムにフィードバックしたりする方法は限られています。
More research is therefore required to put users into control of their recommendations.
そのため、**ユーザーが自分のレコメンデーションをコントロールできるようにするため**に、さらなる研究が必要である。
Today, Amazon.com implements a small set of such features on their website and provides users with explanations for the recommendations.
現在、Amazon.comでは、このような機能の一部を自社サイトに実装し、ユーザーにレコメンデーションの解説を提供しています。
Many users however seem to make limited use of these functionalities [88].
しかし、多くのユーザーはこれらの機能を限定的にしか利用していないようです[88]。
From the data perspective, more and more types of information are becoming accessible regarding the user’s current context, e.g., the current location, weather conditions, other people nearby etc.
データの観点からは、ユーザーの現在の状況（例えば、現在地、天候、近くにいる他の人々など）について、より多くの種類の情報にアクセスできるようになってきています。
Also, continuously new data sources like DBPedia and other sources containing structured information, e.g., in terms of ontologies, become available.
また、DBPediaなどの新しいデータソースや、オントロジーのような構造化された情報を含むソースも継続的に利用できるようになっています。
Some works exist which try to leverage structured information about named entities or other concepts mentioned in the news articles to find similar articles.
ニュース記事で言及された名前付きエンティティやその他の概念に関する構造化情報を活用して、類似の記事を見つけようとする研究がいくつか存在する。
Still, we see a lot of remaining potential to build even better news recommenders that rely on such additional data sources.
しかし、このような追加的なデータソースに依存した、より優れたニュースレコメンダーを構築する可能性は残されていると考えています。
As discussed in the section on aspects of item freshness, there is a number of further open questions.
アイテムの鮮度に関する側面で述べたように、さらに多くの未解決の質問があります。
Looking at existing works, it is not fully clear yet how quickly older news should be discarded in the recommendation process.
既存の研究を見ると、推薦プロセスにおいて、古いニュースをどの程度早く切り捨てるべきかは、まだ十分に明らかになっていない。
In fact, this aspect might even depend on the category of the news items.
実はこの点は、ニュースのカテゴリーに依存することもある。
Some breaking news article might be outdated with the next incoming article on the same topic.
ある速報記事は、同じトピックに関する次の着信記事で古くなる可能性があります。
An article about a sports event might not be very relevant anymore after the weekend.
スポーツイベントに関する記事は、週末を過ぎるともうあまり関連性がないかもしれません。
In contrast, an in-depth news report on a certain topic might be an interesting read even after months.
それに対して、あるテーマについて深く掘り下げた報道は、何ヶ月経っても興味深く読めるかもしれません。
In addition, whether the focus should be more on recent articles or not could also depend on the preferences of the individual user and the time of the day.
また、**最近の記事に重点を置くかどうかは、個々のユーザーの嗜好や時間帯にも左右される可能性があります**。
Some first steps toward a better understanding of these aspects have been taken, but in our view a substantial amount of further investigation is still required.
このような点をよりよく理解するための第一歩が踏み出されたわけですが、私たちは、まだかなりの量のさらなる調査が必要だと考えています。

# 4. Evaluating and Benchmarking News Recommender Systems ニュースレコメンダーシステムの評価とベンチマーキング

Having reviewed the general challenges and current algorithmic approaches in news recommendation, we will discuss methodological questions related to the evaluation of news recommendation approaches in this section.
ニュース推薦における一般的な課題と現在のアルゴリズムアプローチを概観した上で、本節では、ニュース推薦アプローチの評価に関連する方法論的な疑問について述べることにする。
To this end, we will review today’s academic practice of evaluating and benchmarking different algorithms and then reflect on possible limitations in this context caused by the availability of public evaluation data sets.
このため、さまざまなアルゴリズムの評価とベンチマークを行う今日の学術的な実践を検証し、公開された評価データセットがもたらすこの文脈での可能な限界について考察します。
Finally, we will compare open source frameworks that can be used for news recommendation evaluation.
最後に、ニュース推薦評価に利用可能なオープンソースのフレームワークを比較します。

## 4.1. Evaluation Approaches 評価アプローチ

Figure 3: Distribution of evaluation approaches used in news recommendation papers published in the last decade.
図3：過去10年間に発表されたニュース推薦論文で使用された評価アプローチの分布。
Each paper can fall into multiple categories.
各論文は、複数のカテゴリーに分類することができます。

Recommender systems are typically evaluated in one of the following three approaches: through offline experimentation and simulation based on historical data, through laboratory studies, or through A/B (field) tests on real-world websites.
レコメンダーシステムの評価は、一般的に、過去のデータに基づくオフラインでの実験やシミュレーション、ラボでの研究、実際のWebサイトでのA/B（フィールド）テストの3つのアプローチのいずれかになります。
Sometimes, parts of the theoretic properties of the proposed algorithms can be demonstrated using a formal proof.
提案されたアルゴリズムの理論的な特性の一部が、形式的な証明を使って実証されることもあります。
Figure 3 shows the distribution of the different evaluation approaches for the examined papers.
図3は、調査対象論文の評価手法の違いによる分布を示したものである。
Our analysis shows that offline experimentation is the predominant way of evaluating and comparing different algorithms in the field of news recommendation.
我々の分析によると、ニュース推薦の分野で異なるアルゴリズムを評価・比較する方法としては、オフラインでの実験が主流であることがわかります。
User studies are done to a much smaller extent and field tests (A/B studies) are still comparably rare, even though we observe more of such papers in the recent past.
また、ユーザースタディは非常に少なく、フィールドテスト（A/Bスタディ）は、最近になって論文が増えてきたとはいえ、まだ比較にならないほど少ないです。
Comparable analyses have been conducted by Jannach et al.[85] on recommender systems in general and by Beel et al.[9] in the domain of research article recommendation, which both revealed a similar distribution of evaluation methods.
レコメンダーシステム全般についてはJannachら[85]、研究論文推薦の領域についてはBeelら[9]が同様の分析を行っており、いずれも同様の評価方法の分布を明らかにしている。
Figure 4 shows which measures were used by researchers to quantify the performance and characteristics of the evaluated approaches.
図4は、評価したアプローチの性能や特徴を定量化するために、研究者がどのような指標を用いたかを示したものである。
The results show that most of the works focus on accuracy measures of one type or another, including information retrieval measures like precision and recall, rank-based measures like Mean Reciprocal Rank or Normalized Discounted Cumulative Gain, or prediction measures like the Root Mean Square Error.
その結果、ほとんどの論文が、precisionやrecallといった情報検索の尺度、Mean Reciprocal Rank や Normalized Discounted Cumulative Gain といったrank-basedの尺度、あるいはRoot Mean Square Errorといった予測の尺度など、ある種のaccuracy測定に焦点を当てていることがわかった。

Figure 4: Distribution of evaluation measures/metrics used in news recommendation papers published in the last decade.
図4：過去10年間に発表されたニュース推薦論文で使用された評価指標/メトリクスの分布。
Each paper can fall into multiple categories.
各論文は、複数のカテゴリーに分類することができます。

Among the 112 surveyed papers that introduce one or more new algorithms, only 19 used click-based metrics (such as the Click-Through-Rate) as an evaluation measure, even though such metrics are typically considered as success measures in practice, e.g., in the advertising industry.
1つ以上の新しいアルゴリズムを導入した112の調査対象論文のうち、クリックベースのメトリクス（Click-Through-Rateなど）を評価指標として使用したのは、広告業界などで実際に成功指標として一般的に考えられているにもかかわらず、19件のみでした。
Measuring click rates, however, requires access to past navigation data and/or to a real-world system, which might explain the infrequent usage of these measures.
しかし、クリック率の測定には、過去のナビゲーションデータや実システムへのアクセスが必要であるため、これらの指標の使用頻度が低いのかもしれません。
An even smaller number of papers (about 10 out of 112) also considered aspects like diversity, novelty, or serendipity in their evaluations.
また、多様性、新規性、セレンディピティなどの側面を評価対象とした論文は、さらに少数であった（112件中10件程度）。
Scalability, even though an important problem in practice, was also in the focus of only a few research works.
スケーラビリティは、実用上重要な問題であるにもかかわらず、わずかな研究成果にしか焦点が当てられていませんでした。
Note in this context that while some papers take aspects like diversity or novelty into consideration in the design process of their algorithm, they do not explicitly quantify any improvements w.r.t.
この文脈では、アルゴリズムの設計プロセスにおいて多様性や新規性といった側面を考慮した論文もあるが、それらの論文では、改善点を明確に定量化していないことに留意されたい。
these aspects with standard metrics in their experimental evaluation.
を、標準的な評価基準で実験的に評価しています。
A complete list of challenges addressed by each paper and the metrics that were used in the evaluation process can be found in the appendix in Table A.3.
各論文が取り上げた課題と、評価プロセスで使用されたメトリクスの完全なリストは、付録の表A.3に記載されています。

## 4.2. Research Data Sets 研究データセット

The types of evaluations that can be done in academic research often depend on the characteristics of publicly available data sets, e.g., their size or the amount of user and item information.
学術研究においてどのような評価が可能かは、公開されているデータセットの特性（例えば、そのサイズやユーザーやアイテムの情報量など）に依存することが多い。
In the following, we will review a number of such data sets used in the literature and discuss their limitations in terms of what kind of research can be done with them.
以下では、文献で使われているこのようなデータセットをいくつか紹介し、それらを使ってどのような研究ができるかという観点から、その限界について議論します。
A list of the papers that present or analyze news recommendation data sets can be found in the appendix in Table A.4.
ニュースレコメンデーションデータセットを発表または分析した論文のリストは、付録の表A.4で見ることができる。

### 4.2.1. Yahoo!’s Data Sets. Yahoo！のデータセット。

A number of research works in news recommendation are based on different data sets provided by Yahoo! (see, e.g., [124, 126, 139]).
ニュース推薦における多くの研究成果は、Yahoo！が提供する異なるデータセットに基づいている（例えば、[124, 126, 139]を参照）。
One prominent example is the “Yahoo! Front Page Today Module (R6A)” data set, which contains information about news articles that were displayed on the “Featured Tab” on Yahoo!’s landing page and (a fraction of) the click data for these articles.8 The data was collected during the first ten days of May 2009 and contains over 45 million user visits.
このデータセットには、ヤフーのランディングページの「注目タブ」に表示されたニュース記事に関する情報と、その記事のクリックデータ（の一部）が含まれています8。このデータは2009年5月の最初の10日間に収集され、4500万以上のユーザー訪問が含まれています。
For each visit, the timestamp and the displayed article ID is available, as well as a six-dimensional feature vector that was extracted from the item-user interactions via a specific form of regression analysis [32].
各訪問に対して、タイムスタンプと表示された記事ID、および特定の形式の回帰分析によって項目とユーザーの相互作用から抽出された6次元の特徴ベクトルが利用可能である[32]。
Later on, an alternative data set taken from the same website was published (named R6B), which contains data collected during fourteen days and comprising over 130 anonymized user features like age, gender, extracted behavioral variables etc.
このデータセットには、14日間に収集されたデータが含まれており、年齢、性別、抽出された行動変数など、130以上の匿名化されたユーザーの特徴から構成されています。
The two Front Page data sets were specifically constructed in a way so that an unbiased evaluation of recent explore-exploit based techniques (using contextual bandits) is possible [31, 106].
Front Pageの2つのデータセットは、最近のexplore-exploitベースの技術（contextual banditsを使用）の偏りのない評価が可能なように、特に構築されている[31, 106]。
In 2016, Yahoo! released a huge “News Feed” data set containing interactions of about 20 million users collected on different Yahoo! websites over the period of three months in February 2015.
2016年、ヤフーは、2015年2月の3ヶ月間にヤフーのさまざまなウェブサイトで収集された約2000万人のユーザーのインタラクションを含む巨大な「ニュースフィード」データセットを公開しました。
Again, different user and item features are part of this data set, which contained about 110 billion lines.
このデータセットにも、ユーザーやアイテムの特徴があり、約1100億行が収録されています。
Currently, however, the data is no longer available, perhaps due to issues related to the privacy of users.9 While very valuable for researchers, one of the limitations of the still available “Front Page” data sets is that the data collection period is very short (i.e., at most 14 days), making it impossible to conduct research on personalization based on long-term user models.
しかし、現在では、ユーザーのプライバシーに関わる問題からか、このデータは利用できなくなっている9。研究者にとって非常に貴重なデータではあるが、現在利用できる「Front Page」データセットの限界として、データの収集期間が非常に短い（最大でも14日間）ため、長期間のユーザーモデルに基づくパーソナライゼーションに関する研究を行うことができない。
Also, given that the data was sampled only during one specific period, certain events that happened exactly during this period might have lead to certain biases in the data.
また、ある特定の期間にのみデータをサンプリングしているため、その期間にぴったりと起こった特定の出来事によって、データに偏りが生じた可能性があります。

### 4.2.2. SmartMedia Adressa Data Set. SmartMedia Adressaのデータセットです。

Recently, a click log data set with approximately 20 million page visits from a Norwegian news portal as well as a sub-sample with 2.7 million clicks (referred to as “light version”) were released.10 The data set was collected during ten weeks in the first quarter of 2017 and contains the click events of about 2 million users and about 13 thousand articles (light version: one week, 15 thousand users, one thousand articles).
最近、ノルウェーのニュースポータルの約2000万ページ訪問のクリックログデータセットと、270万クリックのサブサンプル（「ライト版」と呼ぶ）が公開されました10。 このデータセットは2017年第1四半期の10週間に収集され、約200万ユーザー、約13千記事のクリックイベントが含まれています（ライト版：1週間、15千ユーザー、1千記事）。
However, according to Gulla et al.[64], the clicks exhibit a strong concentration bias on only small subset of the items.
しかし、Gullaら[64]によれば、クリックはアイテムのごく一部だけに強い集中バイアスを示すという。
In addition to the click logs, the data set contains some contextual information about the users such as geographical location, active time (time spent reading an article), and session boundaries.
このデータセットには、クリックログに加えて、地理的な位置、アクティブタイム（記事を読んでいる時間）、セッションの境界線など、ユーザーに関するいくつかのコンテキスト情報が含まれています。
Furthermore, subscribed users who pay for access to the “pluss” category of articles can be identified; they make up 10.2 % of the user base.
さらに、「プラス」カテゴリの記事へのアクセス料を支払っている購読ユーザーを特定することができ、彼らはユーザーベースの10.2 %を占めています。
This subscription information could enable future investigations that focus on the willingness to pay for news content and the effect of a paid subscription on the consumption and interest patterns of users.
この購読者情報によって、ニュースコンテンツに対する支払い意欲や、有料購読がユーザーの消費・関心パターンに与える影響に着目した今後の調査が可能になります。
Finally, even though the public data set contains some basic information about the news articles themselves in the form of keywords, the article content is only available upon request.
最後に、公開されたデータセットには、ニュース記事自体の基本情報がキーワードの形で含まれているにもかかわらず、記事の内容はリクエストに応じてのみ公開されています。

### 4.2.3. Outbrain Data Set. アウトブレインデータセット

In the context of the 2016/2017 Outbrain Click Prediction challenge hosted on Kaggle11, participants were asked to predict clicks on targeted content ads.
Kaggle11で開催された2016/2017 Outbrain Click Predictionチャレンジの文脈で、参加者はターゲットコンテンツ広告のクリックを予測するよう求められました。
The data set that was used for this challenge contains roughly 2 billion page visits for about 560 US publishers generated by a user base of approximately 700 million visitors during two weeks in June 2016.
今回のチャレンジに使用したデータセットには、2016年6月の2週間に約7億人のユーザーによって生成された、約560の米国パブリッシャーの約20億ページ分の訪問が含まれています。
Even though the challenge focused on ad click prediction, the main click log of page visits, which contains the unique item and user IDs, timestamps, geolocations, etc., can be used for news recommendation evaluation as well.
広告クリック予測に焦点を当てたチャレンジであっても、ユニークなアイテムやユーザーID、タイムスタンプ、ジオロケーションなどを含むページ訪問のメインクリックログは、ニュースレコメンデーション評価にも利用することができます。
In contrast to other news recommendation data sets, however, the content of the news articles is not released.
しかし、他のニュースレコメンドデータセットとは異なり、ニュース記事の内容は公開されていません。
Instead only keywords, categories, and entities are provided as article metadata in the form of IDs.
その代わりに、キーワード、カテゴリー、エンティティのみがIDの形で記事のメタデータとして提供されます。
In fact, since even the publisher can only be identified by ID, researchers cannot be sure which type of news (or other textual content) the respective publishers provide.
実際、出版社もIDでしか特定できないため、研究者はそれぞれの出版社がどのようなニュース（またはその他のテキストコンテンツ）を提供しているのか、確信が持てない。
Therefore, while the possibilities to evaluate content-based recommendation schemes on this data set are rather limited, the massive amount of data offers a great opportunity to test more complex machine learning models.
そのため、このデータセットでコンテンツベースの推薦方式を評価する可能性はかなり限られていますが、膨大なデータ量は、より複雑な機械学習モデルをテストする絶好の機会を提供します。

### 4.2.4. Proprietary and Non-Public Data Sets. 専有および非公開のデータセット。

Unfortunately, much research in the field of news recommendation is based on proprietary and non-public data sets.
残念ながら、ニュース推薦の分野における多くの研究は、独自の非公開データセットに基づくものである。
This in particular holds for research works like [39, 55, 93], which investigate the relationship between offline performance (measured in terms of accuracy metrics) and online success (measured in terms of click-through-rates).
これは特に、オフラインのパフォーマンス（正確さの指標で測定）とオンラインの成功（クリックスルー率で測定）の関係を調査する[39, 55, 93]のような研究作品に当てはまる。
Often, additional application-specific ways of evaluating the performance of the algorithms in the live setting are used in these papers.
多くの場合、これらの論文では、ライブ環境におけるアルゴリズムの性能を評価する追加のアプリケーション固有の方法が使用されています。
In some cases, like in [55], the used real-world data sets were again collected only during a short period of time and contain a comparably small number of user interactions.
55]のように、使用された実世界のデータセットが短期間しか収集されておらず、ユーザーインタラクションの数が比較的に少ないケースもある。

In some cases, researchers who use their own proprietary data sets in addition demonstrate the effectiveness of their methods on non-news data sets (e.g., from MovieLens as done in [39]).
場合によっては、さらに独自のデータセットを使用する研究者は、非ニュースのデータセット（例えば、[39]で行われたMovieLensから）でその方法の有効性を実証しています。
Such data sets are however often very different in terms of their characteristics (e.g., with respect to their sparsity or the fact that there exists no constant item cold-start situation), and it therefore remains unclear whether or not evaluations on such non-news data sets are truly representative of the news domain [142].
しかし、このようなデータセットは、その特性（例えば、スパース性や一定項目のコールドスタート状況が存在しないこと）が大きく異なることが多く、このような非ニュースデータセットでの評価が本当にニュース領域を代表しているかどうかは不明なままである [142]。

### 4.2.5. The Plista Data Set and the NewsREEL Challenge. プリスタデータセットとニュースリールチャレンジ。

In 2013, the Plista12 data set was released [90] for research purposes.
2013年、研究用にPrista12のデータセットが公開されました[90]。
Plista is a German company that provides content and advertisement recommendations for a large number of websites.
Pristaは、ドイツの企業で、多数のウェブサイトに対してコンテンツや広告のレコメンデーションを提供しています。
The data set contains different types of activities by news editors (Create, Update) and news readers (Impression, Click) recorded for about one dozen web portals during June 2013.
このデータセットには、2013年6月に約12のポータルサイトで記録された、ニュース編集者（作成、更新）とニュース読者（印象、クリック）のさまざまなタイプの行動が含まれています。
The data set is comparably large and contains about 80 million article impressions and about 1 million clicks on recommended items.
データセットは比較的に大きく、約8000万件の記事インプレッションと約100万件の推奨アイテムのクリックが含まれています。
A small number of features of the users and the news items are provided as well.
ユーザーの特徴やニュースも少しずつ紹介しています。
The various challenges of news recommendations mentioned in previous sections – e.g., data sparsity, recency biases, very few recorded interactions for many users – become once again apparent when analyzing the data set.
前節で述べたニュース推薦の様々な課題（例えば、データの希少性、再来性バイアス、多くのユーザーに対して記録された非常に少ないインタラクションなど）は、データセットを分析する際に再び明らかになります。
In addition to making the data set publicly available, Plista holds regular contests (the CLEF-NewsREEL challenge13) in which researchers can test their recommendation algorithms in a live environment, which is a unique opportunity in the entire research field.
Pristaでは、データセットの公開に加え、研究者がライブ環境で推薦アルゴリズムをテストできるコンテスト（CLEF-NewsREEL challenge13）を定期的に開催しており、研究分野全体でもユニークな機会となっています。
During the contest, participants receive recommendation requests, which they have to answer within a limited time frame.
コンテストでは、参加者に推薦依頼が届き、限られた時間内に回答する必要があります。
If the recommendations are generally considered “recommendable”, e.g., because they are not too old, they are served to real users, and feedback is given to the participating researchers in case their recommendation was clicked.
古すぎないなど、一般的に「おすすめできる」と判断されたものは、実際のユーザーに提供され、自分のおすすめがクリックされた場合には、参加研究者にフィードバックされます。
One main insight of these contests is that simply recommending those items that have been published within the last few minutes and which have been popular in this time frame seems to be a hard-to-beat approach when the click-through-rate is taken as a success measure [121].
これらのコンテストの主な洞察として、クリックスルー率を成功の指標とした場合、過去数分以内に公開され、この時間帯に人気のあったアイテムを単に推奨することは、困難なアプローチであるようだ[121]というものがある。
A recent analysis of the performance of other approaches that took part in the NewsREEL challenge can be found in [46].
NewsREELチャレンジに参加した他のアプローチの性能に関する最近の分析は、[46]に掲載されています。

## 4.3. Open Source News Evaluation Frameworks オープンソースニュース評価フレームワーク

As discussed above, the availability and quality of public news-related data sets can be a problem when evaluating news recommendation algorithms.
上述したように、ニュース推薦アルゴリズムを評価する際に、公共ニュース関連のデータセットの入手可能性と質が問題になることがあります。
However, even if researchers have access to a data set that fulfills their requirements, they need to compare their own algorithm implementation with other well-known approaches in a reproducible way to demonstrate the viability of their strategy.
しかし、たとえ研究者が自分の要求を満たすデータセットを入手できたとしても、その戦略の実行可能性を実証するために、再現可能な方法で独自のアルゴリズム実装を他のよく知られたアプローチと比較する必要があります。
To this end, a small number of open source frameworks are available that are either specifically targeted towards evaluating news recommendation algorithms or can be adapted to this purpose.
このため、ニュース推薦アルゴリズムの評価に特化した、あるいはこの目的に適応できるオープンソースのフレームワークが少数ながら存在します。
In theory, any recommender system evaluation framework, such as the popular LensKit14 or LibRec15 libraries, could be used to benchmark news recommendation algorithms.
理論的には、人気のあるLensKit14やLibRec15ライブラリのような推薦システム評価フレームワークであれば、ニュース推薦アルゴリズムのベンチマークに使用することができます。
However, as discussed earlier, one unique aspect of the news domain is the importance of article freshness.
しかし、先に述べたように、ニュース領域の特徴として、記事の鮮度が重要視されることが挙げられます。
Since most general purpose RS evaluation frameworks use cross-validation or sliding window schemes, the freshness problem cannot be treated adequately.
一般的なRS評価フレームワークでは、クロスバリデーションやスライディングウィンドウ方式を採用しているため、鮮度の問題を十分に処理することができません。
However, a few frameworks exist that implement a “streaming” evaluation scheme, which aims to simulate real-life recommendation scenarios more closely.
しかし、現実の推薦シナリオをより忠実にシミュレートすることを目的とした「ストリーミング」評価スキームを実装したフレームワークがいくつか存在します。
In such an evaluation scheme, clicks in the data set are processed in a chronological way, and after every click in the data set, algorithms have to generate a recommendation list that is then compared with the actual next clicks of the user.
このような評価方式では、データセットのクリックは時系列で処理され、データセットのすべてのクリックの後に、アルゴリズムが推薦リストを生成し、ユーザーの実際の次のクリックと比較する必要があります。
Table 2 shows a summary of the above-mentioned streaming evaluation frameworks for news recommendation algorithms.
表2は、上記のニュース推薦アルゴリズムのストリーミング評価フレームワークの概要を示したものである。
Of the four available frameworks, only one is designed explicitly for the news domain and, as such, includes special-purpose algorithms for news recommendation.
4つのフレームワークのうち、ニュース領域に特化して設計されているのは1つだけで、ニュース推薦のための特別なアルゴリズムが含まれています。
The variety of algorithms in the IR & E framework, however, is rather low, with only a few baselines and one contextual bandit approach.
しかし、IR & Eフレームワークのアルゴリズムの種類は、いくつかのベースラインと1つのコンテキストバンディットアプローチのみで、むしろ少ないです。
In contrast, the general-purpose frameworks FluRS and Alpenglow offer a number of more complex algorithm implementations, such as incremental learning versions of kNN and matrix factorization.
一方、汎用フレームワークであるFluRSやAlpenglowは、kNNのインクリメンタル学習版や行列分解など、より複雑なアルゴリズムの実装を数多く提供しています。
However, as discussed earlier, these general-purpose collaborative filtering strategies can often not deal with new items quickly enough.
しかし、先に述べたように、これらの汎用的な協調フィルタリング戦略では、新しいアイテムに十分迅速に対応できないことが多い。
Idomaar does not provide any algorithms of its own except for a few simple baselines.
Idomaarは、いくつかのシンプルなベースラインを除いて、独自のアルゴリズムを提供しません。
The idea behind this framework is instead to offer a standardized evaluation environment.
このフレームワークの背景にあるのは、代わりに標準化された評価環境を提供するという考え方です。
In contrast to the other frameworks, where algorithms are implemented as drop-in classes in Python or C++ respectively, in Idomaar each recommendation strategy has to be implemented as a web service endpoint to provide maximum separation between implementation and evaluation and to offer flexibility in the programming language, at the possible cost of efficiency.
他のフレームワークでは、アルゴリズムはそれぞれPythonやC++のドロップインクラスとして実装されていますが、Idomaarでは、実装と評価の分離を最大限に行い、プログラミング言語の柔軟性を提供するため、効率を犠牲にする可能性はありますが、各推薦戦略をWebサービスエンドポイントとして実装する必要があります。
Finally, StreamingRec, an open-source news recommendation framework developed by the authors of this paper, offers a range of baseline approaches and more advanced algorithms in an extensible Java environment.
最後に、本論文の著者らが開発したオープンソースのニュース推薦フレームワークであるStreamingRecは、拡張可能なJava環境において、さまざまなベースラインアプローチとより高度なアルゴリズムを提供している。
Similar to Idomaar, StreamingRec’s evaluation procedure aims to simulate real-life click behavior in the news domain, but without the overhead of implementing algorithms as web-service endpoints.
Idomaarと同様に、StreamingRecの評価手順は、ニュース領域における実際のクリック行動をシミュレートすることを目的としていますが、アルゴリズムをウェブサービスエンドポイントとして実装するオーバーヘッドはありません。
In our view, in particular Idomaar and the more recent StreamingRec framework represent the most valuable starting points for researchers.
特にIdomaarと最近のStreamingRecフレームワークは、研究者にとって最も価値のある出発点であると私たちは考えています。
Idomaar has the advantage of defining language-agnostic interfaces.
Idomaarは、言語にとらわれないインターフェースを定義できるという利点がある。
The framework does, however, not include any pre-implemented algorithms.
ただし、このフレームワークには、あらかじめ実装されたアルゴリズムは含まれていません。
StreamingRec, on the other hand, while being tied to the Java language, offers a wide range of pre-implemented news recommendation algorithms that can be used as baselines in comparative evaluations.
一方、StreamingRecは、Java言語という縛りがある一方で、比較評価のベースラインとして利用できる、あらかじめ実装されたニュース推薦アルゴリズムが豊富に用意されているのが特徴です。
Many of these algorithms are also capable of immediately considering new articles without costly model retraining.
また、これらのアルゴリズムの多くは、コストのかかるモデルの再トレーニングを行うことなく、新しい記事を即座に考慮することが可能です。

## 4.4. Discussion ディスカッション

Research on the topic of news recommendation was historically often subject to a number of constraints and limitations with respect to the evaluation methodology.
ニュース推薦をテーマとした研究は、歴史的に評価方法に関して多くの制約や限界にさらされることが多かった。
Up to the very recent past, only very few public data sets containing user-item interactions for news specific applications were available.
ごく最近まで、ニュースに特化したアプリケーションのユーザーとアイテムのインタラクションを含む公開データセットは、ごくわずかしかありませんでした。
While some of the data sets are comparably large, many only cover the user interactions of a few consecutive days, which makes learning of long-term preference models more or less impossible.
データセットの中には比較的大きなものもありますが、多くは数日間の連続したユーザーインタラクションしかカバーしておらず、長期的な嗜好モデルの学習は多かれ少なかれ不可能といえます。
A further practical problem in this context is that researchers often use subsamples of the larger data sets to test their often computationally complex methods.
この文脈におけるさらなる現実的な問題は、研究者がしばしば、計算上複雑な手法をテストするために、より大きなデータセットのサブサンプルを使用することである。
Since these subsamples or the specific procedures to create them are usually not publicly shared, the reproducibility of the research results often remains limited.
これらのサブサンプルや具体的な作成手順は通常公開されていないため、研究結果の再現性には限界がある場合が多い。
In some cases, researchers resort to data sets from other domains (e.g., movies) to test their news recommendation methods.
また、ニュース推薦手法の検証のために、他のドメイン（映画など）のデータセットを利用するケースもあります。
Such approaches however come with a number of limitations as discussed in [142].
しかし、このようなアプローチには、[142]で述べたように、多くの制約があります。
In particular, the aspects of recency and general popularity play a much less pronounced role in other domains, which makes it unclear to what extent algorithms that work well for other domains are suitable for news recommendation.
特に、他のドメインでは、recencyやgeneral popularityという側面はあまり顕著な役割を果たさないため、**他のドメインでうまく機能するアルゴリズムが、どの程度ニュース推薦に適しているかは不明**である。
To our knowledge, only one data set in the news recommendation domain is available which contains explicit feedback on news articles.21 The YOW data set22, which is described in detail by Ozg ¨ obek et al.[142], contains ¨ ratings for about 380 articles, which were collected from 21 paid users over a period of four weeks.
Ozg¨obekら[142]が詳述しているYOWデータセット22は、21人の有料ユーザーから4週間にわたって収集された約380の記事に対する¨評価¨を含んでいる。
The data set is therefore comparably small and in addition does not contain information about the news articles themselves, which makes experimentation with content-based or hybrid approaches infeasible.
そのため、データセットが比較的に小さく、さらにニュース記事自体の情報も含まれていないため、コンテンツベースやハイブリッドなアプローチの実験ができないのです。
From a methodological perspective, classical IR accuracy measures like precision or recall dominate the research landscape.
方法論の観点からは、精度や想起といった古典的なIRの精度測定が研究の主流となっています。
These measures are often, like in the CLEF-NewsREEL challenge, based on click-through data.
これらの指標は、CLEF-NewsREELの課題のように、クリックスルーデータに基づくことが多い。
While these measures are therefore based on real-world user interactions, a number of limitations remain.
そのため、これらの指標は現実のユーザーインタラクションに基づくものですが、多くの制約が残されています。
First, it is not fully clear today whether being able to successfully predict clicks in an offline experiments will translate into longterm business success in a deployed application [55], which can be a general problem of offline evaluations [10, 78].
まず、オフラインの実験でクリック数をうまく予測できたことが、デプロイされたアプリケーションの長期的なビジネスの成功につながるかどうかは、今日では完全には明らかになっていません[55]が、これはオフライン評価の一般的な問題であると言えます[10、78]。
Past live studies in the domain of mobile game recommendation show for example that recommending comparably popular items leads to high click-through-rates in an online shop but not to the strongest effect in sales [79].
モバイルゲームのレコメンデーション領域における過去のライブスタディでは、例えば、**比較的に人気のある商品を推薦することは、オンラインショップでの高いクリックスルー率につながるが、売上に強い影響を与えないことが示されている**[79]。
In addition, the click-through-rate might only be an indicator of the user’s attention, but not necessarily a sign of genuine interest in the topic and thus proof of the recommender system’s success.
**また、クリックスルー率はユーザーの注目度を示す指標に過ぎず、必ずしもその話題に対する真の興味、ひいてはレコメンダーシステムの成功の証明にはならないかもしれない**。
A second potential issue in the context of measuring in offline experiments is that high values for precision and recall can in different domains be achieved by recommending mostly popular items [80].
オフライン実験での測定という文脈における2つ目の潜在的な問題は、異なるドメインにおいて、主に人気のあるアイテムを推薦することによって、精度とリコールに高い値が達成される可能性があることである[80]。
In some cases, and depending on the specific variant of the measures, popularity-based baseline methods are often hard to beat by more complex methods [36].
場合によっては、また、尺度の特定の変種によっては、人気ベースのベースライン手法は、より複雑な手法に打ち勝つことが難しいことが多い[36]。
In practice, however, users can easily recognize that the recommendations of such a popularity-based method are not based on the currently viewed news article and not tailored to their personal viewing history, which might lead to limited acceptance of the recommendations.
しかし、実際には、このような人気度ベースの手法による推薦は、現在閲覧しているニュース記事に基づくものではなく、個人の閲覧履歴に合わせたものではないことをユーザーが容易に認識できるため、推薦に対する受け入れが限定的になる可能性がある。
This intuition is also supported by the experiments in Garcin et al.[55], where a popularity-based method was the winner in the offline evaluation, but performed poorly in an online scenario.
この直感は、Garcinら[55]の実験でも支持されており、オフライン評価では人気ベースの手法が勝者となったが、オンラインシナリオでは劣勢だった。
Finally, a number of protocols variations can be applied in offline experiments.
最後に、オフラインの実験で適用できるプロトコルのバリエーションをいくつか紹介します。
The simplest approach is to apply a time-agnostic cross-validation protocol, which is often done in the literature to evaluate recommenders, e.g., in the movie domain.
最も単純なアプローチは、時間にとらわれないクロスバリデーションプロトコルを適用することであり、これは映画ドメインなどで推薦者を評価するために文献でよく行われている。
However, splitting up user interactions into training and test sets without considering the consumption order disregards the importance of item freshness in the news domain.
しかし、消費順序を考慮せずにユーザーインタラクションをトレーニングセットとテストセットに分割することは、ニュースドメインにおけるアイテムの鮮度の重要性を無視することになります。
Therefore, the obtained results might be not very representative of an algorithm’s true performance.
そのため、得られた結果は、アルゴリズムの真の性能をあまり代表していない可能性があります。
Another approach is to split the data using one of several time-aware evaluation protocols (see [20] for an overview), and use several consecutive days for training and the last one for testing.
また、時間を意識した評価プロトコル（概要は[20]を参照）を用いてデータを分割し、連続した数日間をトレーニングに、最後の1日間をテストに使用する方法もあります。
The outcomes of such an evaluation might depend on the specific protocol variant, which, as a result, might limit the comparability of the results of different researchers.
このような評価の結果は、特定のプロトコルのバリエーションに依存する可能性があり、その結果、異なる研究者の結果の比較可能性を制限する可能性があります。
Furthermore, the results of the 2017 CLEFNewsREEL challenge indicate [122] that being able to very quickly react to incoming news articles, e.g., within a few minutes, is very important to achieve high click-through rates.
さらに、2017年のCLEFNewsREELチャレンジの結果から、入ってくるニュース記事に非常に素早く、例えば数分以内に反応できることが、高いクリックスルー率を達成するために非常に重要であることが示されています［122］。
It therefore remains unclear how effective complex recommendation algorithms are that can only be re-trained overnight.
そのため、一晩で再トレーニングを行うしかない複雑なレコメンデーションアルゴリズムがどの程度有効なのかは不明なままです。

# 5. Conclusions and Future Directions 結論と今後の方向性

Our review has shown that news recommendation is an active topic of research and that in recent years significant advances have been made in different directions.
我々のレビューでは、ニュース推薦が活発な研究テーマであり、近年、さまざまな方向で大きな進歩が見られることを示した。
In this concluding section, we summarize some key challenges (as discussed in more detail in Sections 3.7 and Section 4.4) and sketch possible directions for future work.
この結論のセクションでは、（セクション3.7とセクション4.4でより詳細に議論された）いくつかの重要な課題を要約し、将来の仕事の可能な方向性をスケッチします。
In our analysis of algorithmic approaches in Section 3, we found that content-based methods are quite frequently used in the academic literature, i.e., in almost half of the papers.
第3節のアルゴリズムアプローチの分析では、コンテンツベースの手法が学術文献でかなり頻繁に、つまりほぼ半数の論文で使用されていることがわかった。
The observations from our experimental evaluation and from news recommendation challenges in the real world, however, suggest that relying solely on content-based techniques can be insufficient.
しかし、私たちの実験的な評価や、現実世界でのニュース推薦の課題から、コンテンツベースの技術にのみ依存するのは不十分であることが示唆されました。
Factors like general article popularity and recency are highly important in the domain and collaborative-content-based hybrid techniques, as used in the field study by Kirshenbaum et al.[93], are therefore the method of choice when it comes to optimizing IR accuracy measures or click-through rates.
general article popularity や recency といった要素は、この領域では非常に重要であり、Kirshenbaumら[93]のフィールドスタディで用いられたような協調コンテンツベースのハイブリッド技術は、したがって、IR精度測定やクリックスルー率の最適化に関しては、選択すべき手法である。
However, in this context, more research is needed to better understand how factors like diversity, novelty, or popularity contribute to the quality perception of users, as focusing only on accuracy measures might lead to mostly non-personalized recommendations and little discovery.
しかし、このような状況では、多様性、新規性、人気といった要素がユーザーの品質認識にどのように寄与するかをよりよく理解するために、さらなる研究が必要です。
Better personalization is however only possible if more is known about the preferences of the individual users.
しかし、より良いパーソナライゼーションは、個々のユーザーの嗜好をより深く知ることで初めて可能になります。
It is therefore important to further investigate the relative importance of long-term and short-term (contextual) preference models.
したがって、長期的な選好モデルと短期的な（文脈的な）選好モデルの相対的な重要性をさらに調査することが重要である。
Research in that direction is however still hampered by the lack of data sets that contain longer user interaction histories.
しかし、この方向での研究は、より長いユーザインタラクションの履歴を含むデータセットがないために、まだ妨げられています。
From an algorithmic perspective, questions regarding scalability were addressed in a number of the reviewed papers.
アルゴリズムの観点からは、スケーラビリティに関する疑問が多くの論文で取り上げられている。
Nowadays, the tools for collecting and storing big amounts of interaction data seem to have reached a high enough maturity level to support basic data processing in real-time.
現在、大量のインタラクションデータを収集・蓄積するためのツールは、リアルタイムで基本的なデータ処理をサポートできるほど高い成熟度に達しているようです。
However, training and continuously updating the machine learning models (as done in other domains, e.g., in [81, 82]), remains a challenge, in particular when the models are based on deep learning strategies.
しかし、機械学習モデルの訓練と継続的な更新は（他のドメインで行われているように、例えば[81, 82]）、特にモデルが深層学習戦略に基づいている場合、依然として課題となっています。
In the news domain, new articles that are possibly relevant for a larger number of users can appear several times a day, and these articles have to be immediately considered by the recommendation methods.
ニュース領域では、より多くのユーザーに関連する可能性のある新しい記事が1日に何度も登場することがあり、これらの記事は推薦手法によってすぐに考慮されなければならない。
Otherwise, the performance of such models can be limited.
そうでなければ、このようなモデルの性能は制限される可能性があります。
This calls for more research on hybrid methods that are, for example, based on sophisticated long-term models and computationally efficient shortterm adaptation heuristics.
そのため、例えば、**高度な長期モデル**と、**計算効率の良い短期適応ヒューリスティック**に基づくハイブリッド手法の研究が求められています。
With respect to the data perspective, today’s research data sets comprise a number of user features and item features, and quite recently, two large news recommendation data sets have been made publicly available.
データの観点では、今日の研究データセットは、多くのユーザ特徴量とアイテム特徴量から構成されており、ごく最近、2つの大規模なニュース推薦データセットが公開された。
These new data sets represent a promising starting point for further reproducible research into scalability, sparsity, and user modeling aspects of news recommendation.
これらの新しいデータセットは、ニュース推薦のスケーラビリティ、スパース性、およびユーザーモデリングの側面に関するさらなる再現性のある研究の出発点として有望です。
Additionally, researchers are nowadays able to test their approaches on a variety of data set and publishers, which can give further insight into the generalizability of newly proposed algorithms; a crucial aspect of RS design, which has not yet been given enough attention in the literature.
さらに、研究者は今日、様々なデータセットや出版社でアプローチをテストすることができ、新たに提案されたアルゴリズムの一般化可能性についてさらなる洞察を得ることができます。
At the same time, with the continuous development of the Social Web, the Semantic Web, and the Internet of Things (IoT), a variety of additional data sources will continue to become available in the future.
一方、ソーシャルウェブ、セマンティックウェブ、IoT（Internet of Things）の継続的な発展により、今後も様々な追加データソースが利用可能になります。
These data sources, for example, include information about the user’s behavior on Social Web platforms, additional information about the relationships between concepts and named entities in the news articles, or contextual information about the user’s situation derived from smartphone sensors or future IoT devices.
これらのデータソースには、例えば、ソーシャルウェブプラットフォームにおけるユーザーの行動に関する情報、ニュース記事における概念と名前付きエンティティの関係に関する追加情報、あるいはスマートフォンのセンサーや将来のIoTデバイスから得られるユーザーの状況に関する文脈的な情報などがあります。
A number of research avenues, therefore, exist on how to leverage these possibly huge amounts of additional types of information in the news recommendation process.
そのため、ニュース推薦プロセスにおいて、これらの膨大な量の追加情報をどのように活用するかについて、多くの研究手段が存在する。
Looking at methodological aspects, we found that IR measures and click-through rates are the prevalent evaluation measures in the academic literature.
方法論的な側面から見てみると、IR measures やクリック率が学術的な評価指標として浸透していることがわかりました。
Whether or not optimizing algorithms for such measures leads to the best value for the different stakeholders (consumer, news provider, news aggregator) has not been investigated to a large extent in the recommender systems literature in general.
このような**accuracyに基づく尺度でアルゴリズムを最適化することが、異なるステークホルダー（消費者、ニュースプロバイダー、ニュースアグリゲーター）にとって最高の価値をもたらすかどうかは、一般に推薦システムの文献ではあまり調査されていません。**
More research and more public data sets that include explicit information about the business value are therefore required to understand, e.g., the economic perspective of news recommenders (“RECO-nomics”) [78] and how to balance the interests of the involved stakeholders.
したがって、例えばニュースレコメンダー（「レコノミクス」）[78]の経済的観点や、関係するステークホルダーの利益のバランスをどのようにとるかを理解するためには、ビジネス価値に関する明確な情報を含む、より多くの研究と公開データセットが必要となる。
In this context, extended cooperations with news publishers or third-party recommendation providers are also required to better understand the business value of news recommendations.
また、ニュースレコメンデーションのビジネス価値をより深く理解するために、ニュース出版社やサードパーティーのレコメンデーションプロバイダーとの協力も必要です。
