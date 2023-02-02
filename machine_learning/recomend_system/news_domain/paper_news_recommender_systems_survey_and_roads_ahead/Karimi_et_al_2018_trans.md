## link 

- [pdf](https://web-ainf.aau.at/pub/jannach/files/Journal_IPM_2018.pdf) pdf](https:

-
-

## title タイトル

News Recommender Systems - Survey and Roads Ahead
ニュース推薦システム - 調査と今後の課題

## abstract アブストラクト

More and more people read the news online, e.g., by visiting the websites of their favorite newspapers or by navigating the sites of news aggregators.
お気に入りの新聞のウェブサイトを訪れたり、ニュースアグリゲーターのサイトを閲覧するなど、オンラインでニュースを読む人はますます増えています。
However, the abundance of news information that is published online every day through different channels can make it challenging for readers to locate the content they are interested in.
しかし、さまざまなチャネルを通じて毎日オンラインで発表される豊富なニュース情報は、読者が興味のあるコンテンツを見つけることを困難にしている場合があります。
The goal of News Recommender Systems (NRS) is to make reading suggestions to users in a personalized way.
ニュース推薦システム（NRS）の目標は、パーソナライズされた方法でユーザーに読書提案を行うことです。
Due to their practical relevance, a variety of technical approaches to build such systems have been proposed over the last two decades.
その実用的な関連性から、過去20年間にそのようなシステムを構築するための様々な技術的アプローチが提案されてきた。
In this work, we review the state-of-the-art of designing and evaluating news recommender systems over the last ten years.
本研究では、過去10年間のニュース推薦システムの設計と評価に関する最先端技術をレビューする。
One main goal of the work is to analyze which particular challenges of news recommendation (e.g., short item life times and recency aspects) have been well explored and which areas still require more work.
この研究の主な目的の一つは、ニュース推薦の特定の課題（例えば、短いアイテムのライフタイムや再帰性の側面など）がよく研究されており、どの領域がまだ多くの研究を必要としているかを分析することである。
Furthermore, in contrast to previous surveys, the paper specifically discusses methodological questions and today’s academic practice of evaluating and comparing different algorithmic news recommendation approaches based on accuracy measures.
さらに、これまでの調査とは対照的に、本論文では、精度指標に基づいて異なるアルゴリズムによるニュース推薦アプローチを評価・比較する方法論的な質問と今日の学術的な実践について具体的に議論している。

# Introduction はじめに

The newspaper industry has experienced a substantial transformation during the last twenty years.
新聞業界は、過去20年間に大きな変化を経験した。
Today, readers can find various sources of news online, e.g., on the web presences of traditional newspaper companies, on digitalonly news sites, or on news aggregation platforms provided, for example, by Google2 or Yahoo!3 .
今日、読者は、伝統的な新聞社のウェブプレゼンス、デジタル専用のニュースサイト、あるいはGoogle2やYahoo！3が提供するニュース集約プラットフォームなど、さまざまなニュースソースをオンラインで見つけることができる。
Additionally, the digital form of information delivery allows publishers to distribute new or updated content in real-time, leading to an increased speed of publication.
さらに、デジタル形式の情報配信により、出版社は新しいコンテンツや更新されたコンテンツをリアルタイムで配信することができ、出版スピードの向上につながる。
The availability of the various (often free) online news sources has led to a constant increase of users of such platforms [138].
さまざまな（しばしば無料の）オンライン・ニュース・ソースが利用可能であるため，このようなプラットフォームの利用者は常に増加している[138]。
At the same time, however, the abundance of available information and the constant update cycle make it increasingly challenging for readers to keep track of news that are most relevant to them.
しかし同時に、利用可能な情報の多さと絶え間ない更新サイクルにより、読者が自分に最も関係のあるニュースを追跡することは、ますます困難になっている。

Recommender Systems have shown to be a valuable tool to help users in such situations of information overload [84].
リコメンダーシステムは、このような情報過多の状況下でユーザーを支援するための貴重なツールであることが示されている[84]。
The main tasks of such systems are typically to filter incoming streams of information according to the users’ preferences or to point them to additional items of interest in the context of a given object.
このようなシステムの主なタスクは、典型的には、ユーザの好みに応じて入ってくる情報の流れをフィルタリングしたり、与えられたオブジェクトのコンテキストで興味のある追加のアイテムを指し示したりすることである。
During the past decades, significant advances in recommendation technology have been made.
過去数十年の間に、推薦技術には大きな進歩があった。
Recommenders have been successfully applied in a variety of domains , and the recommendable objects include movies, books, travel and tourism services, research articles, search queries, and many more [9, 15, 144].
レコメンダーは様々な分野で応用され、映画、書籍、旅行・観光サービス、研究論文、検索クエリなど、多くの分野で成功を収めている [9, 15, 144]。

News recommendation in general represents another application domain in which several of the known techniques for building automated recommendations can be applied.
一般に、ニュース推薦もまた、自動推薦を構築するための既知の技術のいくつかが適用可能な応用領域である。
In fact, there have been a number of reported instances where such systems are being used in live environments to deliver news recommendations on popular websites (see, e.g., [32, 39, 93, 115, 118]).
実際、このようなシステムが人気のあるウェブサイトのニュース推薦を配信するために実環境で使用されている例が多数報告されている（例えば、[32, 39, 93, 115, 118]を参照）。
However, news recommendation problems often have certain characteristics that are either not present at all or that are at least less pronounced in other domains.
しかし、ニュース推薦問題には、他のドメインでは全く存在しないか、少なくともあまり顕著でないある種の特徴があることが多い。
For example, in contrast to other domains like movie recommendation, the relevance of news items can change very rapidly (i.e., decline or re-increase due to recent real-life events) [5, 141] and the “item churn” is generally high [39].
例えば，映画推薦のような他の領域とは対照的に，ニュースアイテムの関連性は非常に急速に変化し（すなわち，最近の現実の出来事によって低下したり再上昇したり） [5, 141] ，「アイテムチャーン」は一般に高い [39].
In fact, since news web sites are often continuously updated, some articles can be superseded by a “breaking news” article on the same topic several times during a single day, which might require constant updates to the recommendation models.
実際、ニュースの Web サイトは継続的に更新されることが多いため、1 日の間に何度も同じトピックに関する「速報」記事が更新されることがあり、推薦モデルの更新が常に必要になる場合があります。
Another typical challenge in the news domain is that a user’s interest can dynamically change, depending on different contextual factors like the time of the day, the features of the user’s device (e.g., mobile phone vs. desktop), or the user’s current location [20, 90, 125].
また，ニュース領域におけるもうひとつの典型的な課題は， ユーザーの関心が，時間帯，ユーザーのデバイスの機能（例： 携帯電話対デスクトップ），ユーザーの現在地などの異なるコンテクスト 要因によって動的に変化することである [20, 90, 125]．このような状況に対応するた めには，推薦モデルの更新が必要となる．

Due to the high practical relevance of the news recommendation problem and its specific challenges, a considerable number of research works has been published on this topic in particular within the last ten years.
ニュース推薦問題は，その実用性の高さと特有の課題から，特に過去10年間にかなりの数の研究論文が発表されている．
Many of these works propose novel algorithmic approaches to generate personalized recommendations.
これらの研究の多くは、パーソナライズされた推薦文を生成するための新しいアルゴリズムアプローチを提案している。
These algorithms are typically evaluated using offline experimental designs and existing log data.
これらのアルゴリズムは、オフラインの実験デザインと既存のログデータを用いて評価されるのが一般的である。
In recent years, however, recommender systems research in a variety of domains has shown that it is also important to evaluate recommendations in a more user- or system utility-oriented way [48, 78, 83, 96, 151].
しかし，近年，さまざまな領域におけるレコメンダーシステムの研究により，よりユーザやシステムの効用を重視した方法でレコメンダーを評価することも重要であることが示されている[48, 78, 83, 96, 151]．
These developments have also led to a number of alternative forms of assessing the quality of the recommendations, e.g., in terms of diversity [80, 161, 172].
また，これらの発展により，レコメンデーションの品質を多様性などの観点から評価する代替的な形態も多く見られるようになった [80，161，172]．

With this work, we consider these recent developments and provide an overview of what has been achieved in the last ten years with respect to the different challenges in the news recommendation domain.
本研究では、これらの最近の動向を考慮し、ニュース推薦領域における様々な課題に関して、過去10年間に達成されたことの概要を提供する。
Based in this analysis, we identify existing research gaps and potential areas for future research.
この分析に基づき、我々は既存の研究ギャップと将来の研究のための潜在的な領域を特定する。
In contrast to some previous overview works like [14, 109, 141], we however focus not only on the underlying algorithmic approaches used to create the recommendations, but also on questions related to the empirical evaluation and the user perception of such systems.
しかし、[14, 109, 141]のような過去の概説的な研究とは対照的に、我々は推薦を作成するために使用される基本的なアルゴリズムのアプローチだけでなく、経験的評価とそのようなシステムのユーザーの知覚に関する問題にも焦点を当てている。
To provide a starting point for future research, we finally also report insights from a set of experiments, which highlight the importance of short-term model updates when standard accuracy measures are applied in the evaluation.
また、将来の研究のための出発点となるように、標準的な精度評価を適用した場合の短期的なモデル更新の重要性を強調する一連の実験から得られた知見を報告する。

The paper is organized as follows.
本論文は以下のように構成されている。
Next, in Section 2, we briefly summarize how we selected existing research works for consideration in our survey.
次に、セクション 2 では、本調査で検討対象とする既存の研究成果をどのように選択したかを簡単にまとめる。
Afterwards, in Section 3, we discuss the various challenges of news recommendation in more detail and review existing algorithmic approaches to deal with these challenges.
その後、セクション 3 では、ニュース推薦の様々な課題についてより詳細に議論し、これらの課題に対処するための既存のアルゴリズム的アプローチをレビューする。
Then, in Section 4, we provide a survey of today’s academic practice of benchmarking and evaluating different technical approaches.
そして、セクション4では、様々な技術的アプローチのベンチマークと評価に関する今日の学術的実践についてのサーベイを行う。
Our paper ends with an outlook on possible directions for future research in Section 5.
最後に、セクション5において、今後の研究の方向性について展望を述べる。

# Survey Method and Research Scope 調査方法と調査範囲

To develop the survey part of the paper, we investigated, in a structured way, more than 140 research articles that appeared between 2005 and 2016 in relevant computer science and information systems publication outlets.
本論文の調査部分を展開するために、2005年から2016年の間に関連するコンピュータ科学と情報システムの出版物に掲載された140以上の研究論文を構造化された方法で調査しました。
Figure 1 shows how many NRS papers were considered in this time frame per year.
図1は、この期間に検討されたNRSの論文が1年あたり何本であったかを示している。
The trend of the graph indicates that research interest in the topic of news recommendation has grown steadily over the years to the point that news has become an important sub-topic in the RS research field.
このグラフの傾向から、ニュース推薦というトピックに対する研究上の関心は、RS研究分野においてニュースが重要なサブトピックとなるまでに、年々着実に高まっていることがわかります。

Figure 1: Number of NRS papers per year.
図 1：年ごとの NRS 論文数。
As the survey only covered 2016 until August, this year was excluded.
調査対象が2016年8月までしかないため、本年は除外した。

Regarding the scope of our review, we focus on papers that describe approaches for “classical” news recommendation scenarios, e.g., on news aggregation sites.
本稿では、「古典的な」ニュース推薦シナリオ（例：ニュースアグリゲーションサイト）を対象としたアプローチを中心にレビューしている。
Similar technical approaches can in many cases be applied for “news feed filtering” problems, for example on Facebook or Twitter, where the content of social news feeds are personalized to the users.
同様の技術的アプローチは、例えばFacebookやTwitterのような「ニュースフィードフィルタリング」問題にも適用できる場合が多く、ソーシャルニュースフィードのコンテンツがユーザーに合わせてパーソナライズされるような場合です。
These scenarios feature many of the same challenges, e.g., an emphasis on freshness and an overwhelming number of new items every day.
これらのシナリオでは、例えば、鮮度が重視され、毎日圧倒的な数の新しいアイテムが提供されるなど、多くの同じ課題があります。
However, news feed filtering on social networks has some unique aspects that are different from news recommendation.
しかし、ソーシャルネットワーク上のニュースフィードフィルタリングには、ニュース推薦とは異なるユニークな側面がある。
For example, the recommendable items are not necessarily news items but can be some currently trending viral videos that are not related to a recent event in the real world.
例えば、推薦されるアイテムは必ずしもニュースとは限らず、現実世界での最近の出来事とは関係のない、現在トレンドとなっているバイラルビデオの一部である場合もある。
Also, on news sites, information about a visitor’s social network friends and general interest profile is in many cases non-existent.
また、ニュースサイトでは、訪問者のソーシャルネットワーク上の友人や一般的な興味に関する情報は存在しない場合が多い。
However, this information oftentimes plays a central role in news feed personalization.
しかし、この情報はニュースフィードのパーソナライズにおいて中心的な役割を果たすことがよくあります。

The identification of papers for our survey was done according to the following strategy.
調査対象論文の抽出は、次のような方針で行った。
We first scanned the proceedings and volumes of a set of relevant conference series (RecSys, WWW, SIGIR, and KDD) and journals (Expert Systems with Applications and Knowledge-Based Systems) for articles that fall into the above-described scope.
まず、関連する一連の会議シリーズ（RecSys、WWW、SIGIR、KDD）と雑誌（Expert Systems with Applications、Knowledge-Based Systems）のプロシーディングスと巻号をスキャンし、上記の範囲に該当する論文を探し出した。
Additionally, we used the keywords “news recommendation” and “news recommender” to search for papers in Google Scholar.
また、Google Scholarでは、「ニュース推薦」「ニュース推薦者」のキーワードで論文を検索した。
Using the resulting set of articles as a starting point, we followed the references of the retrieved articles to find additional papers on the topic.
その結果得られた論文群を出発点として、検索された論文の参考文献をたどり、このテーマに関する追加的な論文を探した。
The survey methodology is therefore not that of a traditional “systematic review” in the sense of, e.g., [94], where pre-defined search queries and inclusion and exclusion criteria are used.
したがって、この調査方法は、例えば[94]のような、あらかじめ定義された検索クエリや包含・除外基準を用いる伝統的な「系統的レビュー」の方法ではない。
Nonetheless, as we followed a defined search strategy, had a defined research scope, and used pre-structured forms to classify the papers along different dimensions, we are confident that the risk of the introduction of a researcher bias into the survey is low.
しかしながら、我々は定義された検索戦略に従い、定義された研究範囲を持ち、異なる次元で論文を分類するために事前に構造化されたフォームを使用したので、我々は調査に研究者バイアスが導入されるリスクは低いと確信している。

A few other survey works on the topic of news recommendation already exist.
このほかにも、ニュース推薦をテーマとした調査研究は、すでにいくつか存在します。
When looking at these existing works, we find that some challenges of news recommendation that we identify in our work were also summarized by Ozg ¨ obek et al. [141].
これらの既存文献を見ると，我々の研究で明らかにしたニュース推薦のいくつかの課題は，Ozg ¨obekら[141]でも要約されていることがわかります．
The authors of this work however only consider a small number of (twelve) papers and do not ¨ consider evaluation aspects in their survey.
しかし，この研究の著者は，少数の（12 の）論文を検討しただけであり，評価の側面は考慮していません．
Li et al. [109] also discuss challenges of news recommendation, but do not discuss existing approaches to deal with these issues in depth.
Liら[109]もニュース推薦の課題を論じているが，これらの課題に対処するための既存のアプローチについては深く論じていない．
The survey paper by Borges and Lorena [14], finally, discusses news recommendation mostly from a quite general perspective and focuses the analysis on different aspects of six specific papers.
Borges and Lorena [14]のサーベイ論文は，主に一般的な観点からニュース推薦について議論し，6つの特定の論文のさまざまな側面に分析を集中させています．

# News Recommendation – Challenges and Algorithmic Approaches ニュースレコメンデーション - 課題とアルゴリズム的アプローチ

Before we discuss the challenges of the domain in more detail along with algorithmic approaches that were proposed in the literature, we will briefly review which types of algorithms are generally used for the news recommendation problem.
文献で提案されたアルゴリズム的アプローチとともに、この領域の課題をより詳細に議論する前に、ニュース推薦問題で一般的にどのような種類のアルゴリズムが使われているかを簡単におさらいしておく。

## Recommendation Paradigms in News Recommendation ニュース推薦におけるレコメンデーションパラダイム

Recommender systems are often classified into four main categories [84, 108]: collaborative filtering (CF), contentbased filtering (CB), knowledge-based techniques (KB), and hybrid approaches.
推薦システムは、協調フィルタリング（CF）、コンテンツベースフィルタリング（CB）、知識ベース技術（KB）、およびハイブリッドアプローチの4つの主要カテゴリに分類されることが多い[84, 108]。
In academic settings, collaborative filtering is the most common approach in the recommender systems literature according to the survey presented in [85], while all other approaches are much less frequently employed.
学術的な環境では、[85]で示された調査によると、協調フィルタリングは推薦システムの文献で最も一般的なアプローチであり、他のすべてのアプローチははるかに頻繁に採用されていない。
The general dominance of collaborative filtering is in some sense not surprising because this method, whose recommendations are based on the “wisdom of the crowd”, is domain-independent and does not require detailed (and domain-specific) information about the recommendable items.
なぜなら、この方法は「群衆の知恵」に基づいて推薦されるため、ドメインに依存せず、推薦可能なアイテムに関する詳細な（そしてドメイン特有の）情報を必要としないためです。
Furthermore, a number of public benchmark data sets, e.g., from MovieLens4 , are available, which has been a driving factor for the academic community.
さらに、MovieLens4 などの公開ベンチマークデータセットが多数用意されていることも、学術界を牽引する要因となっている。

In the news recommendation domain, however, things are different.
しかし、ニュース推薦の分野では事情が異なる。
An analysis of the 112 (of 144) papers in our survey that propose one or more recommendation algorithms reveals the following.5 Content-based filtering, which is, roughly speaking, based on analyzing a reader’s past documents of interest and recommending “more of the same”, was used as an underlying paradigm in 59 of the analyzed papers.
大まかに言えば、読者が過去に興味を持った文書を分析し、「同じものをより多く」推薦するコンテンツベースフィルタリングは、分析対象論文のうち59論文で基本的なパラダイムとして用いられている。
Approaches, like the Google News personalization system [39], that rely on collaborative filtering and on interest patterns in a community without considering the content of a news article are only proposed in 19 of the 112 papers.
Google News Personalization System [39]のように、協調フィルタリングと、ニュース記事の内容を考慮せずにコミュニティ内の関心パターンに依存するアプローチは、112論文中19論文でしか提案されていない。
However, 45 of the papers use a hybrid approach and combine content-based filtering and collaborative filtering.
しかし，45の論文ではハイブリッドアプローチを採用し，コンテンツベースフィルタリングと協調フィルタリングを組み合わせている．
This means that although collaborative filtering alone is not the method of choice for most researchers, relying on patterns in the community behavior in addition to contentbased user profiles is often considered to be promising.
つまり、協調フィルタリング単独では多くの研究者が選択する手法ではないが、コンテンツベースのユーザプロファイルに加えて、コミュニティの行動パターンに依存することが有望視される場合が多いということである。
Knowledge-based techniques, which are based on explicit domain knowledge to map user preferences to article features, were not applied in any of the analyzed papers, neither in isolation nor in combination with other techniques.
知識ベース技術は、明示的なドメイン知識に基づいてユーザーの嗜好を記事の特徴に対応付けるものですが、分析したどの論文にも、単独でも他の技術との組み合わせでも適用されていませんでした。
This is, however, not very surprising, since such approaches are generally only employed in high-involvement product domains with a long life cycle.
しかし、このようなアプローチは、一般的にライフサイクルの長い、関与の高い製品領域でのみ採用されているため、これはあまり驚くべきことではありません。

Since the recommendable objects in the news domain are text documents, which can be automatically analyzed with standard techniques from Information Retrieval (IR), it is in fact not too surprising that many researchers rely on content-based techniques.
ニュース領域で推奨される対象はテキスト文書であり、情報検索（IR）の標準的な技術で自動的に分析できるため、多くの研究者がコンテンツベースの技術に依存していることは実際あまり驚くことではありません。
However, in general, content-based techniques are considered not to be very accurate in offline experiments when using IR measures like precision and recall [80].
しかし、一般的に、コンテンツ・ベースの技術は、オフラインの実験では、精度や再現率といったIRの指標を使う場合、あまり正確でないと考えられています[80]。
As in other domains, the main dilemma of academic research – and to some extent also for recommendation service providers – is that it is not always clear to what extent high accuracy in offline experiments translates into online success [60].
他の領域と同様、学術研究の主なジレンマは、推薦サービス・プロバイダーにとってもある程度はそうですが、オフライン実験での高い精度が、オンラインでの成功にどの程度つながるかが必ずしも明確でないことです[60]。
Only very few studies are available that compare the offline and online performance of recommendation algorithms, e.g., [10] in the field of research paper recommendation.
また、推薦アルゴリズムのオフラインとオンラインの性能を比較した研究は、研究論文推薦の分野では [10] など、ごくわずかしかありません。
In the news domain, a comparative offline
ニュース分野では，オフラインとオンラインを比較した

As we will discuss later, the effectiveness of pure collaborative filtering methods might be overestimated in offline experiments, which calls for the design of novel hybrid approaches that combine multiple sources of preference signals and which are able to balance prediction accuracy with other quality factors like novelty or diversity.
後述するように、純粋な協調フィルタリング手法の有効性はオフライン実験では過大評価される可能性があり、複数の嗜好信号源を組み合わせ、予測精度と新規性や多様性などの他の品質要素のバランスを取ることができる新しいハイブリッドアプローチの設計が必要となる。

## Challenges of User Modeling for News Recommendation ニュース推薦のためのユーザーモデリングの課題

Generally, considering long-term and short-term preferences and balancing their importance represent an important problem in news recommendation [72, 110]; see also the discussion later in Section 3.4 on recency aspects.
一般に，長期的選好と短期的選好を考慮し，それらの重要性をバラン スさせることは，ニュース推薦における重要な問題である [72, 110]; 後述のセクション 3.4 の recency aspects に関する議論も参照されたい。
One of the key design questions is whether two separate models should be maintained (as, e.g., in [6]) or an integrated model with a time decay factor (as in [111]).
そのため，[6]のような2つのモデルを維持するのか， それとも[111]のような時間減衰を考慮した統合モデルを維持 するのかが重要な設計問題の一つである．
A comparison of different strategies of considering the long-term and short-term preferences was done by Huy et al. [72], who observed that a combination of both models in a hybrid approach led to the best results.
長期と短期のプリファレンスを考慮した異なる戦略の比較は、Huyら [72]によって行われ、ハイブリッドアプローチにおける両モデルの組み合わせが最良の結果を導くことが観察された。

## Cold-Start Problems and Data Sparsity Issues in News Recommendation ニュース推薦におけるコールドスタート問題とデータスパース性問題

Cold-start situations are a common problem in many application domains of recommender systems.
コールドスタートは、レコメンダーシステムの多くの応用領域で共通する問題である。
User coldstart refers to situations where little is known about the preferences of the user for which a recommendation is requested; item cold-start means that a new recommendable item (i.e., an article) was added that was not viewed or rated by many people yet.
ユーザーコールドスタートとは、推薦を求めるユーザーの好みについてほとんど知られていない状況を意味し、アイテムコールドスタートとは、まだ多くの人が見ていない、あるいは評価されていない新しい推薦可能なアイテム（すなわち、記事）が追加されたことを意味します。
The problem of general data sparsity is often connected to this problem and in particular relevant for collaborative filtering approaches.
一般的なデータの疎密の問題は、しばしばこの問題に関連しており、特に協調フィルタリングのアプローチに関連している。

### The Permanent Cold-Start Problem 永久冷却始動問題

In principle, many of the technical and domain-independent approaches that were proposed over the years to deal with cold-start situations can be applied in the news recommendation context.
原理的には、コールドスタート状況に対処するために長年にわたって提案されてきた技術的かつドメインに依存しないアプローチの多くは、ニュース推薦の文脈でも適用可能である。
One general approach is to try to incorporate additional information (e.g., about the user’s context) into the recommendation process when little is known about the current user.
一般的なアプローチのひとつは、現在のユーザーについてほとんど知られていない場合に、推薦プロセスに追加情報（例えば、ユーザーのコンテキストについて）を組み込もうとするものである。
In the news recommendation domain, for example, works exist that consider the user’s location [49, 132, 166], the time of the day [40, 49, 132], or demographic information [103].
例えば、ニュース推薦の分野では、ユーザーの位置情報 [49、132、166]、時間帯 [40、49、132]、人口統計情報 [103] を考慮した研究が存在する。
Other examples of contextual information explored in the literature include the website (or domain) that the user has visited before landing on the news page or the type of the device used to access the news [40, 168].
文脈情報の他の例としては，ユーザがニュースページに到達する前に訪れたウェブサイト（またはドメイン），またはニュースへのアクセスに使用されたデバイスの種類などがある[40, 168]．
Instead of considering only the limited information of the user’s history, Lin et al. [113] propose to construct an implicit social network of other users with similar reading behavior.
Linら[113]は，ユーザの履歴という限られた情報のみを考慮するのではなく，同様の読書行動をとる他のユーザからなる暗黙のソーシャルネットワークを構築することを提案している．
The authors then suggest to determine a set of “experts” whose opinion is used to make recommendations for users for which only a short reading history is available.
そして，短い読書履歴しか持たないユーザに対して推薦を行うために，その意見を利用する「専門家」の集合を決定することを提案している．
To identify these experts, they considered other users who have read the same articles in a given time frame, and they subsequently involved these users more heavily in the factorization process if they have a high probability of being a good proxy for a cold-start user.
これらの専門家を特定するために、彼らは与えられた時間枠の中で同じ記事を読んでいる他のユーザーを考慮し、その後、これらのユーザーがコールドスタートユーザーの良い代理人である確率が高い場合、因子分解プロセスにより大きく関与している。
Along the same lines, Zheng et al. [186] propose to enrich the profiles of cold-start users with the profiles of a group of similar other users based on the general news topics they seem to be interested in.
同じ線上で、Zhengら[186]は、cold-startユーザのプロファイルを、彼らが興味を持っていると思われる一般的なニューストピックに基づく類似の他のユーザグループのプロファイルで充実させることを提案しています。
An alternative to incorporating additional aspects related to the user is to consider certain features of the news articles themselves when assessing their relevance for a cold-start user, e.g., the freshness of the article or its general popularity.
ユーザーに関連する追加の側面を取り入れる代替案は、コールドスタート・ユーザーに対する関連性を評価するときに、ニュース記事自体の特定の特徴、例えば記事の鮮度やその一般的な人気度を考慮することです。
Also, one can default to a non-personalized strategy in case of too little information.
また、情報が少なすぎる場合は、パーソナライズされていない戦略に切り替えることもできます。
The “YourNews” system [5], for example, first shows a list of recently published articles and starts the personalization process after the first article has been read.
たとえば、「YourNews」システム [5] は、最初に最近出版された記事のリストを表示し、最初の記事が読まれた後にパーソナライズプロセスを開始します。
In another approach, Montes-Garc´ıa et al. [132] consider the geographical proximity of the news event to the user and the credibility of a news source as factors that can determine the relevance of an item to a cold-start user.
別のアプローチでは、Montes-Garc´aら [132] が、ニュースイベントのユーザーへの地理的な近さとニュースソースの信頼性を、コールドスタート・ユーザーに対するアイテムの関連性を決定することができる要素として考えています。
In their case, the credibility of the news source was determined manually by a team of journalists.
彼らの場合、ニュースソースの信頼性は、ジャーナリストのチームによって手動で決定された。
The context-tree approach by Garcin et al. [53] also takes the recency of the news items into account, but in addition factors the item’s popularity into the recommendation process.
Garcinら[53]によるコンテキスト・ツリーのアプローチも、ニュースアイテムの再来性を考慮に入れつつ、さらにアイテムの人気度を推薦プロセスに反映させる。
By design, their method is also suitable for one-time or first-time users, which are not uncommon for news platforms.
彼らの手法は，ニュースプラットフォームでは珍しくない，1回限りのユーザーや初めてのユーザーにも適した設計になっています．
Finally, Tavakolifard et al. [166] propose to use external data sources – in their case Twitter – to estimate an item’s current popularity more precisely and correspondingly obtain a better picture of its potential relevance for the current user.
最後に、Tavakolifardら[166]は、外部データソース（彼らの場合はTwitter）を使用して、アイテムの現在の人気をより正確に推定し、それに対応して現在のユーザーに対するその潜在的関連性のより良い画像を取得することを提案しています。
For the item cold-start problem, adopting a content-based recommendation strategy already solves a major part of the problem.
アイテムのコールドスタート問題については、コンテンツベースの推薦戦略を採用することで、すでに問題の主要な部分が解決されている。
In content-based approaches, items are generally recommended based on the past content-wise preferences of individual users, which are usually determined by their past navigation or item rating behavior.
コンテンツベースのアプローチでは、一般に、個々のユーザーの過去のナビゲーションやアイテムの評価行動によって決定される、過去のコンテンツ単位の嗜好に基づいてアイテムが推薦される。
Therefore, the required information about a news article can be extracted easily, e.g., from its keywords, making it instantly recommendable without the need for a detailed click history.
そのため、ニュース記事に関する必要な情報は、例えばキーワードから簡単に抽出することができ、詳細なクリック履歴を必要とせず、即座に推薦することが可能となる。
Different alternative technical approaches are possible to infer the user preferences.
ユーザの嗜好を推測するために，異なる別の技術的アプローチが可能である．
Li et al. [108], for example, propose a hybrid approach to construct the user profiles which considers factors such as similarities between access patterns for different news items.
例えば，Li ら [108] は，ユーザプロファイルを構築するために，異なるニュース項目へのアクセスパターン間の類似性などの要因を考慮したハイブリッドアプローチを提案している．
In addition, their approach utilizes item properties that are specific to news, like the news content itself, as well as the user’s preferences for named entities appearing in the news item.
さらに，彼らのアプローチは，ニュースコンテンツ自体や，ニュースアイテムに登場する名前付きエンティティに対するユーザの嗜好など，ニュースに特有のアイテムプロパティを利用する．

### Data Sparsity Issues データスペーサーの問題

When applying collaborative filtering approaches, the recommendation problem is often considered as a matrix completion task, with users and items as rows and columns, respectively, and matrix entries representing the relevance of items for users.
協調フィルタリングアプローチを適用する場合、推薦問題はしばしば、ユーザーとアイテムをそれぞれ行と列とし、ユーザーに対するアイテムの関連性を表す行列の補完タスクとみなされる。
In many domains, including the news domain, this matrix can be extremely sparse and only a tiny fraction of the matrix entries are known.
ニュース領域を含む多くの領域では、この行列は非常に疎であり、行列のエントリのごく一部しか知られていないことがある。
Finding a sufficient number of similar users, for example, in a nearestneighbors collaborative filtering approach, can therefore be very challenging [143].
したがって、例えば最近傍協調フィルタリングアプローチにおいて、十分な数の類似ユーザを見つけることは非常に困難です[143]。
Correspondingly, a number of approaches have been proposed in the context of news recommender systems to deal with the sparsity problem, e.g., by incorporating additional sources of knowledge, predominantly for collaborative filtering, but also for other approaches.
そのため、ニュース推薦システムの文脈では、主に協調フィルタリングのために、しかし他のアプローチでも、例えば、知識の追加ソースを組み込むことによって、スパース性問題に対処するための多くのアプローチが提案されている。
Mannens et al. [127], for example, propose a recommendation method that mitigates sparsity by complementing binary consumption values in the matrix with “potential consumption” values between 0 and 1 based on a collaborative filtering algorithm, which is then re-executed until the matrix is dense enough.
例えば、Mannensら[127]は、行列内の二値消費値を協調フィルタリングアルゴリズムに基づく0と1の間の「潜在的消費」値で補完し、行列が十分に密になるまで再実行することによって疎性を緩和する推薦方法を提案している。
Furthermore, to reduce the uncertainty introduced by this probabilistic approach, they also suggest to post-filter the news articles based on Linked Data sources.
さらに、この確率的アプローチによってもたらされる不確実性を低減するために、彼らはまた、リンクされたデータソースに基づいてニュース記事をポストフィルタリングすることを提案している。
In contrast, Morales et al. [133] propose to use information from social network sites to deal with the sparsity problem.
対照的に、Moralesら[133]は、スパースティ問題に対処するために、ソーシャルネットワークサイトからの情報を利用することを提案している。
In their work, they analyzed the posts of users and their social friends on Twitter and generated a mapping between tweets and news articles based on the entities in the articles.
彼らの研究では，Twitter上のユーザとそのソーシャルフレンドの投稿を分析し，記事中のエンティティに基づいて，ツイートとニュース記事間のマッピングを生成した．
Leveraging information about the relationships between users is also the idea of the work presented in [114] and [113], which has already been mentioned in Section 3.3.1.
ユーザ間の関係性の情報を活用することは，3.3.1 節で既に述べた [114] や [113] で示された研究のアイデアでもある。
In contrast to other approaches, the authors create an implicit virtual network, based on the users’ access logs.
他のアプローチとは対照的に，著者らはユーザのアクセスログに基づいて暗黙の仮想ネットワークを構築している．
In their approach, which combines content information and collaborative filtering, the idea is to identify (two) expert users who are considered as influencers for users without a sufficiently large consumption history.
コンテンツ情報と協調フィルタリングを組み合わせた彼らのアプローチでは，十分に大きな消費履歴を持たないユーザに対して影響力を持つと考えられる（2人の）専門家ユーザを特定することである。
These suspected influence relationships are then used to make the rating matrix denser.
そして、これらの影響関係が疑われるユーザーを用いて、評価行列をより密にする。
Instead of using social network information, Lu et al. [120] propose to combine different forms of user behavior, context, and content features of the news items to find similar users in sparse-data situations.
Luら[120]は、ソーシャルネットワーク情報を使う代わりに、異なる形式のユーザー行動、コンテキスト、ニュースアイテムのコンテンツ特徴を組み合わせて、データが疎な状況で類似ユーザーを見つけることを提案している。
Specifically, they consider the user’s browsing, commenting, and publishing behavior as implicit feedback signals.
具体的には、彼らはユーザーの閲覧、コメント、出版行動を暗黙のフィードバック信号とみなしている。
An even richer set of preference signals was combined in the News@hand system presented in [11, 24, 25].
さらに豊富な嗜好シグナルのセットは、[11, 24, 25]で紹介されたNews@handシステムで結合されている。
The authors use ontologies and Semantic Web technology to represent the knowledge about users and items and utilize a variety of preference indicators, such as page clicks, rating, and comments.
著者らは，ユーザーとアイテムに関する知識を表現するためにオントロジーとセマンティックウェブ技術を使用し，ページのクリック，評価，コメントなどの様々な嗜好指標を利用している．
To deal with the sparsity problem, they then propose a graph-based method to spread the information via the semantic relations of the network of concepts.
そして、スパースティ問題に対処するために、彼らは、概念のネットワークの意味的関係を通じて情報を拡散するグラフベースの方法を提案している。
Li et al. [105] address the data sparsity issue by framing the recommendation task as a so called contextual bandit problem.
また、Li ら[105]は推薦タスクをいわゆる文脈的バンディット問題として定式化することで、データのスパース性に対処している。
In such a problem formulation [101], every recommendation task is represented as a choice between k possible “arms” of a multi-armed bandit.
このような問題定式化[101]では、すべての推薦タスクは、多腕バンディットのk本の可能な「腕」の間の選択として表現される。
The recommendation strategy makes this choice only based on a context vector, for which Li et al. [105] chose a compact representation of users and articles (e.g., based on demographic information, location, and news categories).
この推薦戦略は、文脈ベクトルにのみ基づいてこの選択を行う。Li ら [105] は、ユーザーと記事のコンパクトな表現（例えば、人口統計情報、場所、ニュースカテゴリに基づく）を選択した。
Afterwards, a reward is observed based on the user reaction (click).
その後、ユーザの反応（クリック）に基づき報酬が観測される。
The advantage of contextual bandit approaches is that they can be used to balance exploration of the item space and exploitation of previous knowledge even in sparse data situations.
文脈バンディットアプローチの利点は、データが疎な状況でも項目空間の探索と既知の知識の活用をバランスよく行えることである。
Generally, one of several well-studied optimization strategies can be used to optimize the expected reward, i.e., in this case, the overall number of clicks.
一般に、期待報酬、すなわち、この場合は全体のクリック数を最適化するために、よく研究されたいくつかの最適化戦略のうちの1つを用いることができる。
To evaluate the usefulness of their approach, the authors tested it on data sets with various sparsity levels.
このアプローチの有用性を評価するために、著者らは様々なスパースレベルのデータセットでテストを行った。
Generally, when considering recommendation as a matrix completion problem, different forms of rating imputation and other forms of advanced statistical methods can be applied.
一般に、推薦を行列補完問題として考える場合、様々な形式の評価インピュテーションや他の形式の高度な統計的手法を適用することができる。
Agarwal et al. [3], for example, analyze the correlations between different post-read actions (such as sharing, commenting, printing, or emailing article links) and are thus able to interchange the information across actions types to derive additional data points to feed into the recommendation process.
例えば、Agarwalら[3]は、異なる読後行動（記事リンクの共有、コメント、印刷、メール送信など）間の相関を分析し、その結果、行動タイプ間で情報を交換し、推薦プロセスに投入する追加データポイントを導き出すことができるようになっています。
Overall, a number of techniques for dealing with the data sparsity issue in the news domain were presented over the years.
全体として、ニュース領域におけるデータの疎密の問題に対処するための技術は、長年にわたって数多く発表されています。
Since data sparsity is such a central problem in news recommendation, many papers evaluate their algorithmic proposals – even when they are not explicitly focusing on data augmentation – on data sets of different densities to analyze their behavior in such situations.
データの疎密はニュース推薦における中心的な問題であるため、多くの論文が、たとえデータの増強に明確な焦点を置いていない場合でも、アルゴリズムの提案を異なる密度のデータセットで評価し、そのような状況での挙動を分析している。

## The Importance of Considering the Recency of News Articles ニュース記事のRecencyを考慮することの重要性

When reviewing the literature, a number of different strategies and threshold values are used and it is not clear if an approach that is working well in one setting will also be suitable for another use case.
文献を調べると、多くの異なる戦略や閾値が使われており、ある設定でうまくいっているアプローチが、別のユースケースにも適しているかどうかは不明である。
In many cases, details about the specific settings are not reported in the research papers, which makes these works hard to reproduce.
多くの場合、研究論文では具体的な設定に関する詳細が報告されていないため、これらの著作物を再現することは困難である。
Table 1 gives an overview of approaches that consider item recency as a relevant factor.
表1は項目の再利用性を関連する要素として考慮したアプローチの概要を示している。
In the last two columns, we show which thresholds were applied in case they were reported and which time windows were used to decrease the relevance of an article based on its recency.
最後の2列では、報告された場合にどの閾値が適用されたのか、また、どの時間窓を使用して、記事の再来時に基づいて関連性を低下させたのかを示している。
We can observe significant differences.
大きな違いを観察することができます。
Some works only focus on articles of the last six hours [49], whereas others consider articles of the last twenty days [136].
ある研究は過去6時間の記事のみに注目し[49]、他の研究は過去20日の記事を考慮します[136]。
Some authors add a decay penalty for every second since the article was published [38], whereas others do this only for each hour [183].
また、記事が公開されてから 1 秒ごとに減衰ペナルティを加えるもの [38]もあれば、1 時間ごとに減衰ペナルティを加えるもの [183]もあります。
In many cases, however, this detailed information is unfortunately not reported at all.
しかし、多くの場合、このような詳細な情報は残念ながら全く報告されていない。

Table 1:
表1．
Overview of news recommendation approaches that consider recency as a factor.
表 1: 再現性を考慮したニュース推薦手法の概要
The first column categorizes the papers according to their recency strategy.
最初の列は再来日戦略によって論文が分類されている。
The next two columns list the paper’s author(s) and its publication year.
次の2列は論文の著者と出版年である。
The fourth column shows the employed recommendation strategy (CB = Content-based filtering, CF = Collaborative filtering, H = Hybrid).
4列目は採用した推薦手法（CB = Content-based Filtering, CF = Collaborative Filtering, H = Hybrid）である。
The fifth column lists the data sets used in the paper.
5列目は、論文で使用されたデータセットである。
The last two columns show (a) how old articles can be at most to be considered recent and (b) the granularity of applying a decay factor, e.g., for every hour after the initial publication.
最後の2列は、(a)どの程度古い記事までが最近の記事とみなされるか、(b)最初の出版から1時間ごとなど、減衰因子を適用する粒度を示している。

##  Considering Quality Factors Beyond Prediction Accuracy 予測精度を超えた品質要素を考慮する

The main optimization goal of researchers in academia is to accurately predict the relevance of a news item for a user.
学術界の研究者の主な最適化目標は、ユーザーにとってのニュースアイテムの関連性を正確に予測することである。
Most commonly, classification or ranking accuracy measures are used for that purpose (see Section 4 for more details).
最も一般的には、分類やランキングの精度尺度がその目的に使われます（詳しくはセクション4を参照）。
However, in practice, predicting the relevance of an item is in many cases not enough.
しかし，実際には，ある項目の関連性を予測するだけでは十分でない場合が多い．
If, for example, a user is interested in politics and has shown strong interest in articles about an ongoing presidential election in the past, recommending more articles about this topic is probably a good choice.
たとえば，ユーザが政治に関心があり，過去に進行中の大統領選挙に関する記事に強い関心を示した場合，このトピックに関する記事をより多く推薦することはおそらく良い選択である．
However, recommending solely articles about the election, or solely about politics, might be too monotonous for users and would probably not lead to high user engagement in the future.
しかし、選挙に関する記事だけ、あるいは政治に関する記事だけを推薦しても、ユーザーにとっては単調すぎて、将来的に高いユーザーエンゲージメントにつながらないかもしれません。
In case of a news aggregation site, it is furthermore important that the recommended news are not too similar to each other.
ニュースアグリゲーションサイトの場合、さらに重要なのは、推薦されるニュースが互いに似すぎていないことである。
Presenting three articles from three different sources about, e.g., the same plane accident might be of little value for users.
例えば、同じ飛行機事故について3つの異なるソースから3つの記事を提示しても、ユーザーにとってはあまり価値がないかもしれません。
Therefore, one additional challenge, besides accurately predicting whether an article is relevant for a user or not, is to take additional quality factors into account.
したがって、ある記事がユーザーにとって関連性があるかどうかを正確に予測することに加えて、さらなる品質要因を考慮することが一つの課題である。
In the recommender systems literature, diversity, novelty, and serendipity are often considered as such quality factors that have to be balanced with prediction accuracy (see, e.g., [29]).
推薦システムの文献では、多様性、新規性、セレンディピティは、しばしば予測精度とバランスを取らなければならないそのような品質要因として考えられている（例えば、[29]を参照）。

### Diversity 多様性

Users of news recommender systems can be interested in a variety of topics.
ニュース推薦システムの利用者は、様々なトピックに興味を持つ可能性がある。
A recommender system should therefore be able to address these varied tastes and generate diversified recommendation lists [171].
そのため、レコメンダーシステムは、こうした多様な嗜好に対応し、多様なレコメンデーションリストを生成できる必要がある[171]。
Empirical research suggests that increasing the diversity of the recommendations can lead to a better quality perception by users [48, 151, 188].
経験的な研究によれば，推薦の多様性を高めることは，ユーザーによる質の高い知覚につながることが示唆されている[48, 151, 188]．
An example for a work that considers diversity in the news recommendation domain is presented in [108], which we already mentioned earlier in the context of recency filtering and cold-start techniques.
ニュース推薦の領域で多様性を考慮した研究の例として、先に再帰性フィルタリングとコールドスタート技術の文脈で既に述べた[108]が提示されています。
In the proposed two-stage approach, articles were clustered in the first phase, and the recommendations were personalized and adapted, e.g., with respect to recency, in the second phase.
提案された二段階のアプローチでは、第一段階で記事がクラスタリングされ、第二段階で推薦が個人化され、例えば、recencyに関して適応される。
In both stages, the authors propose to add some level of diversification.
両段階において、著者らはあるレベルの多様化を加えることを提案している。
According to the authors, the first-level clustering strategy implicitly introduces some level of topic diversity, while the second stage implements a greedy approach that explicitly minimizes the similarity among items in a recommendation set.
著者らによれば、第一段階のクラスタリング戦略は、あるレベルのトピックの多様性を暗黙的に導入し、第二段階では、推薦セット内のアイテム間の類似性を明示的に最小化する貪欲なアプローチを実装している。
In the latter case, the diversity was measured by computing the average pairwise (dis-)similarity of documents, and an experimental evaluation showed that their approach was beneficial in terms of both accuracy and diversity when compared to the works presented in [31, 39, 105, 115].
後者の場合、多様性は文書の平均ペアワイズ（dis-）類似度を計算することによって測定され、実験的評価により、彼らのアプローチは[31, 39, 105, 115]で示された作品と比較して、精度と多様性の両面で有益であることが示された。
Later on, Li and Li [107] followed an alternative and more advanced approach to diversify news recommendations in the context of a learning-to-rank optimization scheme.
その後，Li and Li [107]は，learning-to-rank最適化スキームの文脈で，ニュース推薦を多様化するための代替的かつより高度なアプローチを追った．
In their work, they propose a framework that relies on a hypergraph to model the relations between different “media objects”, which included users, news articles, topics, and named entities.
彼らの研究では、ユーザー、ニュース記事、トピック、名前付きエンティティなどの異なる「メディアオブジェクト」間の関係をモデル化するために、ハイパーグラフに依存するフレームワークを提案している。
Using the same experimental setup as in their previous work [108], the authors were able to demonstrate further improvements both in terms of accuracy and diversity.
彼らの以前の仕事[108]と同じ実験設定を使用して、著者らは精度と多様性の両方の点でさらなる改善を実証することができた。
Typically, there is a trade-off between accuracy, e.g., in terms of classification accuracy, and diversity, e.g., in terms of intra-list similarity [188].
一般に、分類精度などの精度とリスト内類似度などの多様性との間にはトレードオフが存在する[188]。
To address this issue, Desarkar and Shinde [41] analyzed two possible approaches of balancing these goals in the news domain and tested them for a special privacy-targeted scenario where no past interaction history is available for the users and the relevance of each candidate item is consequently estimated only by its popularity.
この問題に対処するため、Desarkar and Shinde [41]はニュース領域でこれらの目標のバランスをとるための2つの可能なアプローチを分析し、ユーザが過去の交流履歴を利用できず、結果として各候補項目の関連性がその人気度によってのみ推定される、プライバシーをターゲットにした特別なシナリオでそれらをテストしました。
In their case, diversification is described as a bi-criteria optimization problem where both the relevance and the dissimilarity between the news objects should be high.
彼らの場合、多様化は、ニュースオブジェクト間の関連性と非類似度の両方が高いことが望ましい2基準最適化問題として記述されている。
Outside the domain of news recommendation, a number of works have been published over the past ten years on the topic of diversifying recommendations [29].
ニュース推薦の分野以外でも，推薦の多様化というトピックで過去10年間に多くの研究が発表されている[29]．
Besides the question of how to balance diversity with accuracy, researchers investigated to what extent the level of diversification should be determined by the preferences of the individual user [162] or how diversity preferences can depend on time aspects [102].
多様性と精度のバランスをどうとるかという問題に加えて，研究者は多様化のレベルが個々のユーザーの好みによってどの程度決定されるべきか［162］，あるいは多様性の好みが時間的側面にどのように依存しうるか［102］を調査しています．
In the news domain, these aspects have not been investigated much yet, even though some of these aspects – like the consideration of the time of the day when recommending [40] – might have an effect on the user’s short-term diversity preferences.
ニュース領域では，これらの側面はまだあまり研究されていないが，推薦時に時間帯を考慮すること[40]などは，ユーザの短期的な多様性選好に影響を与える可能性がある．

### Novelty 

Novelty, as a quality criterion for recommendations, was defined in terms of the non-obviousness of the item suggestions by Herlocker et al. [68].
レコメンデーションの品質基準としての新規性は、Herlockerら[68]によってアイテム提案の非自明性という観点で定義された。
Informally, novel items are, according to their definition, those that the user has not seen yet, but which are relevant to him or her.
非公式には、新規性のあるアイテムとは、彼らの定義によると、ユーザーがまだ見たことがないが、彼または彼女に関連しているものである。
An alternative definition was provided by Vargas and Castells [172], who defined novelty as the inverse general popularity of an item.
別の定義はVargas and Castells [172]によって提供され、彼らは新規性をアイテムの逆一般的な人気と定義した。
The assumption here is that less popular items are more likely to be unknown to users and recommending long-tail items will, in general, lead to higher novelty levels.
ここでは、人気のないアイテムはユーザーにとって未知の可能性が高く、ロングテールのアイテムを推奨することは、一般的に高い新規性レベルにつながるという仮定がなされている。
Several ways of numerically quantifying the degree of novelty are possible, including alternative ways of considering popularity information [187] or the distance of a recommendable item to the user’s profile [137, 154].
新規性の程度を数値的に定量化する方法はいくつかあり、人気情報を考慮する別の方法[187]や、推薦可能な項目とユーザーのプロファイルの距離[137, 154]があります。
Like diversity and accuracy, novelty and accuracy aspects can represent a trade-off.
多様性と正確性のように，新規性と正確性はトレードオフの関係にあります．
In their work on news recommendation, Garcin et al. [53] relied on the definition by Herlocker et al. [68] and tested different configurations of weighting the two factors to achieve both high accuracy and high novelty.
ニュース推薦に関する研究において，Garcin ら [53] は Herlocker ら [68] による定義に依拠し，高精度と高新奇性の両方を達成するために，2 つの要素の重み付けの異なる構成をテストしました．
Rao et al. [154] followed an approach where the novelty of an item is defined by its distance to the user’s profile.
Raoら[154]は、アイテムの新規性をユーザーのプロファイルとの距離によって定義するアプローチをとった。
Specifically, they compared the distance of the concepts appearing in the user profile and the news article, where the taxonomy was constructed from encyclopedic knowledge.
具体的には，百科事典的な知識から構成された分類法を用いて，ユーザプロファイルとニュース記事に現れる概念の距離を比較した．
The evaluation results of their user study show that this approach cannot only be used to increase accuracy but also reduce the perceived redundancy among news articles.
彼らのユーザー調査の評価結果から、このアプローチは精度を高めるだけでなく、ニュース記事間で知覚される冗長性を低減するためにも利用できることが示された。
Generally, as for diversity, the “optimal” degree of novelty can depend on the user’s current situation and context, as discussed recently by Kapoor et al. [89] in the context of the music domain.
一般に、多様性と同様に、「最適な」新規性の程度は、Kapoor ら [89] が音楽領域の文脈で最近議論したように、ユーザの現在の状況や文脈に依存する可能性がある。
Determining the right balance of recommending (a) things that are most likely relevant for the user and (b) recommending items that help the user discover new things remains challenging.
このような場合、(a) ユーザにとって最も関連性の高いものを推奨し、(b) ユーザが新しいものを発見するのに役立つアイテムを推奨することのバランスを適切に判断することは、依然として困難である。
Limited research on these aspects exists in the news recommendation domain.
このような観点からの研究は、ニュース推薦領域では限られている。
As discussed in Section 3.3.1, the news domain has the special characteristic that most of the recommendable items are usually new and unknown to the readers.
このように，ニュース推薦領域は，読者にとって未知なものが多いという特 徴がある．
In terms of some of the definitions from above, all recommendations are novel.
このため，ニュース推薦の領域では，新規性を評価することができない。
Therefore, novelty can probably not be determined on the basis of the individual item itself, but rather in terms of the content the news item is about, e.g., based on whether or not the user already knows about the real-world event the news item is reporting on.
したがって，新規性はおそらく個々のアイテムそのものではなく，ニュースアイテムの内容，例えば，ニュースアイテムが報道している現実世界の出来事についてユーザがすでに知っているかどうかに基づいて決定することができる。

### Serendipity セレンディピティ

Serendipity is sometimes also mentioned as a desirable quality characteristic of recommendations.
セレンディピティは、推薦の望ましい品質特性として言及されることもある。
Herlocker et al. [68] describe serendipitous recommendations as those that help users find surprising and interesting items that they might not have noticed otherwise.
Herlocker ら[68]は、セレンディピティ・レコメンデーションとは、ユーザーが他の方法では気づかなかったかもしれない意外で興味深いアイテムを見つけるのを助けるものであると述べている。
Ge et al. [57], based on an earlier approach by Murakami et al. [135], defined serendipitous recommendations as items that are not only novel but also positively surprising for the user and proposed a generic metric based on the concepts of unexpectedness and usefulness.
Ge ら[57]は、Murakami ら[135]による初期のアプローチに基づき、セレンディピタス推薦を、新規性があるだけでなく、ユーザにとって積極的に驚くべき項目と定義し、意外性と有用性の概念に基づく一般的な指標を提案している。
Zhang et al. [185] finally proposed a related conceptualization in the context of a music recommendation application in which the level of serendipity is determined based on the distance between the recommendations and the user’s expected content.
Zhang ら[185]は、音楽推薦アプリケーションの文脈で、推薦内容とユーザの期待する内容との距離に基づいてセレンディピティのレベルを決定する、関連する概念化を最終的に提案した。
To our knowledge, only limited research on serendipity aspects of the news recommendation problem exist so far.
我々の知る限り、ニュース推薦問題におけるセレンディピティの側面に関する研究は、これまでに限られたものしか存在しない。
In principle, one can apply techniques based on Latent Dirichlet Allocation (LDA) models – as proposed by Zhang et al. [185] for music recommendation – to the news domain and focus on recommending news items that are content-wise dissimilar to the user’s typical latent topics.
原理的には、音楽推薦のために Zhang ら [185] が提案した Latent Dirichlet Allocation (LDA) モデルに基づく技術をニュース領域に適用し、ユーザーの典型的な潜在的話題と内容的に異なるニュース項目を推薦することに焦点を当てることができる。
However, whether or not this will lead to higher levels of user satisfaction in this domain, still has to be explored.
しかし、これがこの領域でより高いユーザー満足度につながるかどうかは、まだ検討の余地がある。
Overall, one key question today is how to quantify the level of serendipity of a recommendation list and how such serendipity measures would be related to existing novelty measures.
全体として、今日の重要な問題の一つは、推薦リストのセレンディピティのレベルをどのように定量化するか、また、そのようなセレンディピティ指標は既存の新規性指標とどのように関連するかということである。
Again, adding serendipitous items to the recommendations comes with the risk of decreasing the average relevance of the recommendation lists.
また、セレンディピティなアイテムを推薦リストに加えることは、推薦リストの平均的な関連性を低下させるというリスクも伴います。
Furthermore, Kotkov et al. [99] recently discussed the problem that today in many (general RS) research data sets used for offline experimentation not enough information about the user’s context (e.g., time, location, or mood) is available.
さらに、Kotkovら[99]は最近、オフライン実験に使用される多くの（一般的なRS）研究データセットにおいて、ユーザーのコンテキスト（例えば、時間、場所、気分）についての十分な情報が利用できないという問題を論じています。
The user’s context can however have a significant impact on the user’s perception of serendipitous item recommendations.
しかし、ユーザーのコンテキストは、セレンディピティアイテムの推薦に対するユーザーの知覚に大きな影響を与える可能性がある。
In our view, more research is therefore required also outside the field of news recommendations to better understand the concept of serendipity in recommender systems and how to measure it.
したがって、推薦システムにおけるセレンディピティの概念とその測定方法をよりよく理解するためには、ニュース推薦の分野以外でもさらなる研究が必要であると我々は考えている。

## Scalability Issues スケーラビリティの問題

Scalability is the last of the main challenges of news recommendation that we discuss in this section.
スケーラビリティは、このセクションで述べるニュース推薦の主要な課題の最後である。
Large news websites like Google News can have hundreds of millions of users per month.
Googleニュースのような大規模なニュースサイトでは、1ヶ月に数億人のユーザーが利用することがあります。
At the same time, the number of articles that can be searched and recommended can be huge as well, with thousands of new items appearing every day.6 A common approach to deal with these huge amounts of data is to apply clustering techniques of different types.
同時に、検索・推薦可能な記事の数も膨大になり、毎日何千もの新しい項目が出現する6 。これらの膨大なデータを扱うための一般的なアプローチは、さまざまな種類のクラスタリング技術を適用することである。
Clustering can in many cases help to speed up the computations; it can however also lead to compromises with respect to the accuracy of the relevance predictions.
クラスタリングは多くの場合、計算の高速化に役立ちますが、関連性予測の精度に関しても妥協することになります。
In addition to such algorithmic approaches that, e.g., allow us to do the computations on a more coarse-grained level, researchers often propose to rely on distributed computing mechanisms and to execute the calculations on multiple servers in parallel.
このようなアルゴリズムによるアプローチに加えて、例えば、より粗い粒度での計算を可能にするために、研究者はしばしば分散コンピューティング機構に依存し、複数のサーバで並行して計算を実行することを提案しています。
The application of various forms of clustering techniques for different aspects of the news recommendation problem has been proposed, e.g., in [39, 120, 129], and [174].
ニュース推薦問題の様々な側面に対して、様々な形式のクラスタリング技術の適用が、例えば、[39, 120, 129]、[174]で提案されている。
In some of these cases, the main goal is to search for similar users (neighbors) only within a smaller cluster of users without the need to scan the entire database.
これらの事例の中には，データベース全体を走査することなく，より小さなクラスタ内でだけ類似のユーザ（隣人）を検索することを主目的とするものがある．
In the case of the Google News system, as described in [39], the authors use a combination of (MinHash) clustering and distributed computing based on the MapReduce framework to make the approach scalable.
Google News システムの場合、[39]で説明されているように、著者らはアプローチをスケーラブルにするために、（MinHash）クラスタリングと MapReduce フレームワークに基づく分散コンピューティングを組み合わせて使用しています。
Lu et al. [120] also combine MapReduce and a clustering technique to increase the scalability.
Luら[120]もMapReduceとクラスタリング技術を組み合わせて、スケーラビリティを高めています。
Specifically, they use a “Jaccard–Kmeans” based clustering technique where the similarity of users is computed in multiple dimensions, e.g., based on their past behavior and the content the users preferred in the past.
具体的には、彼らは「Jaccard-Kmeans」ベースのクラスタリング技術を使用しており、ユーザーの類似性を、例えば、過去の行動やユーザーが過去に好んだコンテンツに基づいて、多次元で計算します。
Other examples of works on news recommendation that rely on distributed computing include [156] and [159].
また、分散コンピューティングに依存したニュース推薦に関する他の研究例として、[156]や[159]がある。
Besides clustering the users, one can also try to cluster the available news articles and group them based on their features and the user’s preferences.
ユーザをクラスタリングする以外に，利用可能なニュース記事をクラスタリングし，その特徴やユーザの嗜好に基づいてグループ化することを試みることもできる．
In [108], for example, the authors propose a two-stage recommendation approach in which they apply different clustering techniques to create a hierarchy of news clusters.
例えば、[108]では、著者らは2段階の推薦アプローチを提案し、異なるクラスタリング技術を適用して、ニュースクラスタの階層を作成する。
This hierarchy can then be efficiently traversed from top to bottom to find a set of news articles similar to the user’s reading interest.
この階層を上から下へ効率的に走査し，ユーザの読書関心に近いニュース記事の集合を見つけることができる．
Medo et al. [129] adopt a different approach to achieve scalability in the context of a news platform where users can post news items.
Medoら[129]は，ユーザがニュース項目を投稿できるニュース・プラットフォームの文脈でスケーラビリティを達成するために，異なるアプローチを採用しています．
In their method, they construct a local neighborhood network of users based on the similarity of their rating behavior (likes
彼らの手法では，ユーザの評価行動の類似性（「いいね」「いいね」「いいね」「いいね」）に基づき，ユーザの局所近傍ネットワークを構築する．

## Discussion ディスカッション

The review of recent works in this section shows that during the last ten years substantial efforts went into the development of new techniques to deal with the particular challenges of news recommendation.
本節で紹介する最近の研究成果から、過去10年間にニュース推薦という特殊な課題に対処するための新しい技術の開発に多大な努力が払われてきたことがわかる。
Figure 2 shows the distribution of topics and challenges that were addressed in the reviewed works.
図 2 は、レビューされた論文の中で扱われたトピックと課題の分布を示したものである。
The diagram shows that the largest number of papers was devoted to the problems of user profiling, which is a common challenge for all recommender systems domains.
この図から、最も多くの論文が、すべての推薦システムのドメインに共通する課題であるユーザープロファイリングの問題に費やされていることがわかります。
Additionally, a number of papers focus on the specific problems of data sparsity and user and item cold-start.
また、多くの論文がデータの疎密やユーザとアイテムのコールドスタートという特定の問題に焦点を当てています。
This is in fact expected, given that news recommendation systems face a continuous item cold-start situation, and personalization techniques that work well, e.g., for movie recommendation, do not always work well under such circumstances.
これは、ニュース推薦システムが連続的なアイテムのコールドスタートの状況に直面しており、例えば映画推薦でうまく機能する個人化技術が、このような状況下では必ずしもうまく機能しないことを考えると、実際、予想されたことではある。
Also, it is not very surprising that recency aspects received a lot of interest, due to the unique short-livedness of the items in the domain.
また、この領域ではアイテムの寿命が短いという特徴があるため、recencyの側面が注目されるのはあまり驚くことではない。

Figure 2: Distribution of research challenges (other than accuracy) addressed by news recommendation papers published in the last decade.
図2：過去10年間に発表されたニュース推薦論文で扱われた研究課題（正確性以外）の分布。
Each paper can fall into multiple categories.
各論文は、複数のカテゴリーに分類される。

Beginning around the year 2011, we observe more and more papers on beyond-accuracy quality aspects like diversity, novelty, and serendipity, i.e., topics that were not strongly in the focus of researchers in earlier years.
2011年頃から、多様性、新規性、セレンディピティなど、精度を超えた品質面に関する論文が増え、以前はあまり注目されていなかったトピックが注目されるようになりました。
This recent trend can be considered as a positive development, since it has already been shown in other domains in which recommenders have been applied that focusing solely on accuracy measures to compare algorithms can be insufficient and potentially misleading [80, 128].
というのも，アルゴリズムを比較するために精度の指標にのみ注目することは不十分であり，誤解を招く可能性があることが，推薦者が適用された他のドメインで既に示されているからです[80, 128]。
Nonetheless, more work is needed to better understand how to balance the sometimes competing goals of achieving high prediction accuracy and, for example, list diversity in parallel.
しかし，高い予測精度を達成することと，例えばリストの多様性を達成することという，時に競合する目標をどのように並行してバランスをとるかをよりよく理解するためには，さらなる研究が必要です。
Looking at the different challenges discussed in this section so far, we can identify a number of additional areas in which more work is still required.
このセクションで議論されたさまざまな課題を見ると，さらに多くの作業が必要な領域があることがわかります．
In the context of user modeling, for example, a number of papers differentiate between long-term preferences and short-term interests.
例えば、ユーザーモデリングの文脈では、多くの論文が長期的な嗜好と短期的な興味を区別しています。
In our view, it is however not fully clear yet how these aspects should be balanced, how we can deal with an interest drift over longer periods of time, or how we should deal with exceptional events and specific contextual conditions, which induce a probably only short-lived interest at the user’s side.
しかし、私たちの見解では、これらの側面をどのようにバランスさせるべきか、長期間にわたる興味のドリフトにどのように対処すべきか、あるいは、ユーザー側でおそらく短期間の興味を引き起こす例外的なイベントや特定のコンテキスト条件にどのように対処すべきかは、まだ十分に明確ではありません。



# Evaluating and Benchmarking News Recommender Systems ニュース推薦システムの評価とベンチマーク

Having reviewed the general challenges and current algorithmic approaches in news recommendation, we will discuss methodological questions related to the evaluation of news recommendation approaches in this section.
ニュース推薦における一般的な課題と現在のアルゴリズムアプローチを概観した後、本セクションではニュース推薦アプローチの評価に関連する方法論的な問題を議論する。
To this end, we will review today’s academic practice of evaluating and benchmarking different algorithms and then reflect on possible limitations in this context caused by the availability of public evaluation data sets.
この目的のために、さまざまなアルゴリズムの評価とベンチマークを行う今日の学術的実践をレビューし、次に、公開評価データセットの利用可能性に起因するこの文脈の限界の可能性について考察する。
Finally, we will compare open source frameworks that can be used for news recommendation evaluation.
最後に、ニュース推薦の評価に利用可能なオープンソースのフレームワークについて比較する。

## Evaluation Approaches 評価アプローチ

Figure 3: Distribution of evaluation approaches used in news recommendation papers published in the last decade.
図3：過去10年間に発表されたニュース推薦論文で用いられた評価手法の分布。
Each paper can fall into multiple categories.
各論文は、複数のカテゴリーに分類される。

Recommender systems are typically evaluated in one of the following three approaches: through offline experimentation and simulation based on historical data, through laboratory studies, or through A
レコメンダーシステムの評価は、一般的に、過去のデータに基づくオフラインの実験やシミュレーション、ラボラトリースタディ、またはA

Figure 4: Distribution of evaluation measures
図4：評価指標の分布

Among the 112 surveyed papers that introduce one or more new algorithms, only 19 used click-based metrics (such as the Click-Through-Rate) as an evaluation measure, even though such metrics are typically considered as success measures in practice, e.g., in the advertising industry.
1つ以上の新しいアルゴリズムを導入した112の調査対象論文のうち、クリックベースのメトリクス（Click-Through-Rateなど）を評価指標として用いた論文は、広告業界などで実際に成功指標として一般的に考えられているにもかかわらず、わずか19件でした。
Measuring click rates, however, requires access to past navigation data and
しかし、クリック率を測定するには、過去のナビゲーションデータにアクセスする必要があり

## Research Data Sets 研究データセット

The types of evaluations that can be done in academic research often depend on the characteristics of publicly available data sets, e.g., their size or the amount of user and item information.
学術研究においてどのような評価が可能かは、一般に公開されているデータセットの特徴、例えばそのサイズやユーザ情報・項目情報の量に依存することが多い。
In the following, we will review a number of such data sets used in the literature and discuss their limitations in terms of what kind of research can be done with them.
以下では、文献で使われているそのようなデータセットをいくつかレビューし、それらを使ってどのような研究ができるのかという観点から、その限界について議論することにする。
A list of the papers that present or analyze news recommendation data sets can be found in the appendix in Table A.4.
ニュース推薦のデータセットを紹介・分析した論文のリストは付録の表A.4にある。

### Yahoo!’s Data Sets. ヤフーのデータセット



### SmartMedia Adressa Data Set. SmartMedia Adressaのデータセットです。

Recently, a click log data set with approximately 20 million page visits from a Norwegian news portal as well as a sub-sample with 2.7 million clicks (referred to as “light version”) were released.10 The data set was collected during ten weeks in the first quarter of 2017 and contains the click events of about 2 million users and about 13 thousand articles (light version: one week, 15 thousand users, one thousand articles).
最近、ノルウェーのニュースポータルの約2000万ページ訪問のクリックログデータセットと270万クリックのサブサンプル（「ライト版」と呼ぶ）が公開された10。このデータセットは2017年第1四半期の10週間に収集され、約200万ユーザーと約1万3000記事のクリックイベントを含んでいる（ライト版：1週間、1万5000ユーザー、1000記事）。
However, according to Gulla et al. [64], the clicks exhibit a strong concentration bias on only small subset of the items.
しかし、Gullaら[64]によれば、クリックは小さなサブセットのみに強い集中バイアスを示している。
In addition to the click logs, the data set contains some contextual information about the users such as geographical location, active time (time spent reading an article), and session boundaries.
このデータセットには、クリックログに加えて、地理的な位置、アクティブタイム（記事を読むのに費やした時間）、セッションの境界など、ユーザーに関するいくつかの文脈情報が含まれています。
Furthermore, subscribed users who pay for access to the “pluss” category of articles can be identified; they make up 10.2 % of the user base.
さらに、「plus」カテゴリの記事へのアクセス料を支払っている購読ユーザーを特定することができ、彼らはユーザーベースの10.2 %を占めている。
This subscription information could enable future investigations that focus on the willingness to pay for news content and the effect of a paid subscription on the consumption and interest patterns of users.
この購読者情報によって、ニュース・コンテンツに対する支払い意思や、有料購読がユーザーの消費・関心パターンに及ぼす影響に焦点を当てた、今後の調査が可能になります。
Finally, even though the public data set contains some basic information about the news articles themselves in the form of keywords, the article content is only available upon request.
最後に、公開されたデータセットには、キーワードという形でニュース記事自体の基本情報が含まれていますが、記事の内容はリクエストに応じてのみ入手可能です。

### Outbrain Data Set. Outbrainのデータセット。

In the context of the 2016
2016年に開催された背景には

### Proprietary and Non-Public Data Sets. 専有・非専有データセット。

Unfortunately, much research in the field of news recommendation is based on proprietary and non-public data sets.
残念ながら、ニュース推薦の分野における多くの研究は、独占的な非公開のデータセットに基づいています。
This in particular holds for research works like [39, 55, 93], which investigate the relationship between offline performance (measured in terms of accuracy metrics) and online success (measured in terms of click-through-rates).
特に、オフラインのパフォーマンス（正確さの指標で測定）とオンラインの成功（クリックスルー率で測定）の関係を調査した [39, 55, 93] のような研究成果では、この傾向が顕著です。
Often, additional application-specific ways of evaluating the performance of the algorithms in the live setting are used in these papers.
多くの場合、これらの論文では、ライブ環境でのアルゴリズムのパフォーマン スを評価する追加のアプリケーション固有の方法が使用されています。
In some cases, like in [55], the used real-world data sets were again collected only during a short period of time and contain a comparably small number of user interactions.
55]のように、使用された実世界のデータセットは、やはり短期間のみ収集され、比較的に少ない数のユーザーインタラクションを含んでいる場合があります。

In some cases, researchers who use their own proprietary data sets in addition demonstrate the effectiveness of their methods on non-news data sets (e.g., from MovieLens as done in [39]).
また，独自のデータセットを使用する研究者は，ニュース以外のデータセット（例えば，[39]で行われたMovieLensからのデータ）でもその手法の有効性を実証する場合がある．
Such data sets are however often very different in terms of their characteristics (e.g., with respect to their sparsity or the fact that there exists no constant item cold-start situation), and it therefore remains unclear whether or not evaluations on such non-news data sets are truly representative of the news domain [142].
しかし，このようなデータセットは，その特性（例えば，スパース性や定数項目のコールドスタート状況が存在しないことに関して）が大きく異なることが多く，したがって，このような非ニュースデータセットでの評価が本当にニュース領域を代表しているかどうかは不明なままである[142]．

### The Plista Data Set and the NewsREEL Challenge. PlistaデータセットとNewsREELの挑戦。

In 2013, the Plista12 data set was released [90] for research purposes.
2013 年、Prista12 のデータセットが研究目的で公開された[90]。
Plista is a German company that provides content and advertisement recommendations for a large number of websites.
Plistaはドイツの企業で、多数のウェブサイトに対してコンテンツや広告の推薦を行っている。
The data set contains different types of activities by news editors (Create, Update) and news readers (Impression, Click) recorded for about one dozen web portals during June 2013.
このデータセットには，2013年6月に約12のウェブポータルについて記録された，ニュース編集者によるさまざまな種類の活動（作成，更新）とニュース読者による活動（Impression，Click）が含まれています．
The data set is comparably large and contains about 80 million article impressions and about 1 million clicks on recommended items.
データセットは比較的大きく、約8000万件の記事インプレッションと約100万件のおすすめアイテムのクリックが含まれています。
A small number of features of the users and the news items are provided as well.
また、ユーザーやニュースアイテムの特徴も少なからず提供されています。
The various challenges of news recommendations mentioned in previous sections – e.g., data sparsity, recency biases, very few recorded interactions for many users – become once again apparent when analyzing the data set.
前節で述べたニュース推薦の様々な課題（例えば、データの希少性、再帰性バイアス、多くのユーザーに対して記録されたインタラクションが非常に少ないなど）は、このデータセットを分析する際に再び明らかになる。
In addition to making the data set publicly available, Plista holds regular contests (the CLEF-NewsREEL challenge13) in which researchers can test their recommendation algorithms in a live environment, which is a unique opportunity in the entire research field.
Plistaでは、データセットの公開に加え、研究者が推薦アルゴリズムをライブ環境でテストできるコンテスト（CLEF-NewsREEL challenge13）を定期的に開催しており、これは研究分野全体においてユニークな機会である。
During the contest, participants receive recommendation requests, which they have to answer within a limited time frame.
コンテスト期間中、参加者は推薦リクエストを受け取り、限られた時間内にそれに答えなければならない。
If the recommendations are generally considered “recommendable”, e.g., because they are not too old, they are served to real users, and feedback is given to the participating researchers in case their recommendation was clicked.
推薦文が古すぎないなど、一般的に「推薦できる」と判断されれば、実際のユーザーに提供され、自分の推薦文がクリックされた場合には、参加した研究者にフィードバックが行われます。
One main insight of these contests is that simply recommending those items that have been published within the last few minutes and which have been popular in this time frame seems to be a hard-to-beat approach when the click-through-rate is taken as a success measure [121].
これらのコンテストの主な洞察は、クリックスルー率を成功の指標とした場合、過去数分以内に公開され、この時間枠で人気のあったアイテムを単に推薦することは、打ちにくいアプローチのようだということです [121]。
A recent analysis of the performance of other approaches that took part in the NewsREEL challenge can be found in [46].
NewsREELチャレンジに参加した他のアプローチのパフォーマンスに関する最近の分析は、[46]に記載されています。

## Open Source News Evaluation Frameworks 

As discussed above, the availability and quality of public news-related data sets can be a problem when evaluating news recommendation algorithms.
上述したように、ニュース推薦アルゴリズムを評価する際に、公共ニュース関連データセットの利用可能性と品質が問題になることがあります。
However, even if researchers have access to a data set that fulfills their requirements, they need to compare their own algorithm implementation with other well-known approaches in a reproducible way to demonstrate the viability of their strategy.
しかし、研究者は要件を満たすデータセットにアクセスできたとしても、自分の戦略の実行可能性を示すために、再現可能な方法で他のよく知られたアプローチと自分のアルゴリズム実装を比較する必要があります。
To this end, a small number of open source frameworks are available that are either specifically targeted towards evaluating news recommendation algorithms or can be adapted to this purpose.
このため、ニュース推薦アルゴリズムの評価に特化した、あるいはこの目的に適応可能なオープンソースのフレームワークがいくつか利用可能です。
In theory, any recommender system evaluation framework, such as the popular LensKit14 or LibRec15 libraries, could be used to benchmark news recommendation algorithms.
理論的には、一般的な LensKit14 や LibRec15 ライブラリのような推薦システム評価フレームワークは、ニュース推薦アルゴリズムのベンチマークに使用することができます。
However, as discussed earlier, one unique aspect of the news domain is the importance of article freshness.
しかし、先に述べたように、ニュース領域のユニークな側面として、記事の鮮度が重要であることが挙げられます。
Since most general purpose RS evaluation frameworks use cross-validation or sliding window schemes, the freshness problem cannot be treated adequately.
ほとんどの汎用的なRS評価フレームワークはクロスバリデーションやスライディングウィンドウスキームを使用しているため、鮮度の問題を適切に扱うことができない。
However, a few frameworks exist that implement a “streaming” evaluation scheme, which aims to simulate real-life recommendation scenarios more closely.
しかし、現実の推薦シナリオをより忠実に再現することを目的とした「ストリーミング」評価スキームを実装したフレームワークがいくつか存在する。
In such an evaluation scheme, clicks in the data set are processed in a chronological way, and after every click in the data set, algorithms have to generate a recommendation list that is then compared with the actual next clicks of the user.
このような評価方式では、データセット内のクリックは時系列に処理され、データセット内の各クリックの後に、アルゴリズムが推薦リストを生成し、それをユーザーの実際の次のクリックと比較する必要がある。
Table 2 shows a summary of the above-mentioned streaming evaluation frameworks for news recommendation algorithms.
表2は、上記のニュース推薦アルゴリズムのためのストリーミング評価フレームワークの概要を示している。
Of the four available frameworks, only one is designed explicitly for the news domain and, as such, includes special-purpose algorithms for news recommendation.
4つのフレームワークのうち、1つだけがニュース領域用に設計されており、ニュース推薦のための特別なアルゴリズムが含まれている。
The variety of algorithms in the IR & E framework, however, is rather low, with only a few baselines and one contextual bandit approach.
しかし、IR & E フレームワークのアルゴリズムの種類はかなり少なく、いくつかのベースラインと1つのコンテクスチュアルバンディットアプローチのみである。
In contrast, the general-purpose frameworks FluRS and Alpenglow offer a number of more complex algorithm implementations, such as incremental learning versions of kNN and matrix factorization.
一方、汎用フレームワークであるFluRSやAlpenglowでは、kNNのインクリメンタル学習版や行列分解など、より複雑なアルゴリズムの実装が多数用意されている。
However, as discussed earlier, these general-purpose collaborative filtering strategies can often not deal with new items quickly enough.
しかし、先に述べたように、これらの汎用的な協調フィルタリング戦略では、新しいアイテムに十分に迅速に対応できないことが多いのです。
Idomaar does not provide any algorithms of its own except for a few simple baselines.
Idomaarはいくつかの単純なベースラインを除いて、独自のアルゴリズムを提供しません。
The idea behind this framework is instead to offer a standardized evaluation environment.
このフレームワークの背後にある考え方は、代わりに標準化された評価環境を提供することである。
In contrast to the other frameworks, where algorithms are implemented as drop-in classes in Python or C++ respectively, in Idomaar each recommendation strategy has to be implemented as a web service endpoint to provide maximum separation between implementation and evaluation and to offer flexibility in the programming language, at the possible cost of efficiency.
他のフレームワークでは、アルゴリズムはPythonやC++のドロップインクラスとして実装されていますが、Idomaarでは、実装と評価の分離を最大化し、効率を犠牲にしながらもプログラミング言語の柔軟性を提供するために、それぞれの推薦戦略をWebサービスのエンドポイントとして実装する必要があります。
Finally, StreamingRec, an open-source news recommendation framework developed by the authors of this paper, offers a range of baseline approaches and more advanced algorithms in an extensible Java environment.
最後に、本稿の著者らが開発したオープンソースのニュース推薦フレームワークであるStreamingRecは、拡張可能なJava環境において、さまざまな基本アプローチとより高度なアルゴリズムを提供している。
Similar to Idomaar, StreamingRec’s evaluation procedure aims to simulate real-life click behavior in the news domain, but without the overhead of implementing algorithms as web-service endpoints.
Idomaarと同様に、StreamingRecの評価手順は、ニュース領域における実際のクリック行動をシミュレートすることを目的としていますが、アルゴリズムをウェブサービスエンドポイントとして実装するオーバーヘッドを伴わないのが特徴です。
In our view, in particular Idomaar and the more recent StreamingRec framework represent the most valuable starting points for researchers.
私たちは、特にIdomaarと最近のStreamingRecフレームワークが、研究者にとって最も価値のある出発点であると考えています。
Idomaar has the advantage of defining language-agnostic interfaces.
Idomaarは言語に依存しないインタフェースを定義しているという利点があります。
The framework does, however, not include any pre-implemented algorithms.
しかし、このフレームワークには、あらかじめ実装されたアルゴリズムは含まれていません。
StreamingRec, on the other hand, while being tied to the Java language, offers a wide range of pre-implemented news recommendation algorithms that can be used as baselines in comparative evaluations.
一方、StreamingRecはJava言語に縛られているが、比較評価のベースラインとして使用できる幅広いニュース推薦アルゴリズムがあらかじめ実装されている。
Many of these algorithms are also capable of immediately considering new articles without costly model retraining.
また、これらのアルゴリズムの多くは、コストのかかるモデルの再トレーニングを行うことなく、新しい記事を即座に考慮することが可能である。

## Discussion ディスカッション

Research on the topic of news recommendation was historically often subject to a number of constraints and limitations with respect to the evaluation methodology.
ニュース推薦に関する研究は、歴史的に評価方法に関して多くの制約や限界にさらされることが多かった。
Up to the very recent past, only very few public data sets containing user-item interactions for news specific applications were available.
ごく最近まで、ニュースに特化したアプリケーションのユーザーアイテムインタラクションを含む公開データセットは、ごくわずかしかありませんでした。
While some of the data sets are comparably large, many only cover the user interactions of a few consecutive days, which makes learning of long-term preference models more or less impossible.
データセットの中には比較的に大きなものもありますが、多くは連続した数日間のユーザーインタラクションしかカバーしておらず、長期的な嗜好モデルの学習は多かれ少なかれ不可能です。
A further practical problem in this context is that researchers often use subsamples of the larger data sets to test their often computationally complex methods.
さらに、この文脈における実用的な問題は、研究者がしばしば計算複雑な手法をテストするために、より大きなデータセットのサブサンプルを使用することです。
Since these subsamples or the specific procedures to create them are usually not publicly shared, the reproducibility of the research results often remains limited.
これらのサブサンプルやその作成方法は通常公開されていないため、研究結果の再現性はしばしば制限されたままである。
In some cases, researchers resort to data sets from other domains (e.g., movies) to test their news recommendation methods.
また、ニュース推薦手法の検証のために、他の領域（例えば、映画など）のデータセットを利用するケースもある。
Such approaches however come with a number of limitations as discussed in [142].
しかし，このようなアプローチには，[142]で議論されているように，いくつかの限界がある．
In particular, the aspects of recency and general popularity play a much less pronounced role in other domains, which makes it unclear to what extent algorithms that work well for other domains are suitable for news recommendation.
特に，他のドメインでは recency や一般的な人気という側面はあまり顕著ではなく，他のドメインでうまく機能するアルゴリズムがどの程度までニュース推薦に適しているかは不明である．
To our knowledge, only one data set in the news recommendation domain is available which contains explicit feedback on news articles.21 The YOW data set22, which is described in detail by Ozg ¨ obek et al. [142], contains ¨ ratings for about 380 articles, which were collected from 21 paid users over a period of four weeks.
YOW データセット22 は，Ozg ¨obekら[142]が詳述しているが，21人の有料ユーザーから4週 間にわたって収集した約380記事に対する¨評価を含んでいる。
The data set is therefore comparably small and in addition does not contain information about the news articles themselves, which makes experimentation with content-based or hybrid approaches infeasible.
したがって、このデータセットは比較的に小さく、さらに、ニュース記事自体に関する情報を含んでいないため、コンテンツベースまたはハイブリッドアプローチの実験を行うことは不可能である。
From a methodological perspective, classical IR accuracy measures like precision or recall dominate the research landscape.
方法論的な観点からは、精度や再現率といった古典的なIRの精度測定が研究の主流となっています。
These measures are often, like in the CLEF-NewsREEL challenge, based on click-through data.
これらの指標は、CLEF-NewsREELチャレンジのように、クリックスルーデータに基づいていることが多いです。
While these measures are therefore based on real-world user interactions, a number of limitations remain.
したがって、これらの測定は、現実のユーザーインタラクションに基づいていますが、多くの制限が残っています。
First, it is not fully clear today whether being able to successfully predict clicks in an offline experiments will translate into longterm business success in a deployed application [55], which can be a general problem of offline evaluations [10, 78].
まず、オフラインの実験でクリックをうまく予測できることが、配備されたアプリケーションの長期的なビジネスの成功につながるかどうかは、今日では完全に明らかではありません[55]が、これはオフラインの評価[10, 78]の一般的な問題である可能性があります。
Past live studies in the domain of mobile game recommendation show for example that recommending comparably popular items leads to high click-through-rates in an online shop but not to the strongest effect in sales [79].
このことは、オフライン評価の一般的な問題となりうる [10, 78]。モバイルゲーム推薦の領域における過去のライブスタディでは、例えば、比較的に人気のあるアイテムを推薦すると、オンラインショップでの高いクリックスルー率につながるが、売上では最も強い効果にはならないことを示している [79]。
In addition, the click-through-rate might only be an indicator of the user’s attention, but not necessarily a sign of genuine interest in the topic and thus proof of the recommender system’s success.
また、クリックスルー率はユーザーの注目度の指標にすぎず、必ずしもそのトピックへの真の関心の表れではなく、したがって推薦システムの成功の証明にはならない可能性があります。
A second potential issue in the context of measuring in offline experiments is that high values for precision and recall can in different domains be achieved by recommending mostly popular items [80].
オフライン実験での測定という文脈での第二の潜在的な問題は、異なるドメ インにおいて、高い精度と再現率が、主に人気のあるアイテムを推薦するこ とで達成される可能性があることです[80]。
In some cases, and depending on the specific variant of the measures, popularity-based baseline methods are often hard to beat by more complex methods [36].
このような場合、また、測定の具体的なバリエー ションによっては、人気に基づくベースライン手法は、より複雑 な手法に打ち勝つことが難しい場合があります [36]。
In practice, however, users can easily recognize that the recommendations of such a popularity-based method are not based on the currently viewed news article and not tailored to their personal viewing history, which might lead to limited acceptance of the recommendations.
しかし実際には，このような人気に基づく手法の推奨は，現在閲覧しているニュース記事に基づくものではなく，個人の閲覧履歴に合わせたものでもないことをユーザは容易に認識でき，推奨の受け入れに限界が生じる可能性がある．
This intuition is also supported by the experiments in Garcin et al. [55], where a popularity-based method was the winner in the offline evaluation, but performed poorly in an online scenario.
この直感は、Garcinら[55]の実験でも支持されており、オフライン評価では人気に基づく方法が勝者となったが、オンラインシナリオでは低いパフォーマンスであった。
Finally, a number of protocols variations can be applied in offline experiments.
最後に、オフラインの実験では多くのプロトコルのバリエーションを適用することができる。
The simplest approach is to apply a time-agnostic cross-validation protocol, which is often done in the literature to evaluate recommenders, e.g., in the movie domain.
最も単純なアプローチは、時間にとらわれないクロスバリデーションプロトコルを適用することであり、これは、例えば、映画のドメインでリコメンダーを評価するために、文献でしばしば行われている。
However, splitting up user interactions into training and test sets without considering the consumption order disregards the importance of item freshness in the news domain.
しかし，消費順序を考慮せずにユーザインタラクションをトレーニングセットとテストセットに分割すると，ニュースドメインにおけるアイテムの鮮度の重要性を無視することになる．
Therefore, the obtained results might be not very representative of an algorithm’s true performance.
そのため，得られた結果はアルゴリズムの真の性能をあまり代表していない可能性がある．
Another approach is to split the data using one of several time-aware evaluation protocols (see [20] for an overview), and use several consecutive days for training and the last one for testing.
また，時間を考慮した評価プロトコル（概要は[20]を参照）を用いてデータを分割し，連続した数日間をトレーニングに，最後の1日間をテストに使用するアプローチもあります．
The outcomes of such an evaluation might depend on the specific protocol variant, which, as a result, might limit the comparability of the results of different researchers.
このような評価の結果は、特定のプロトコルの変種に依存する可能性があり、その結果、異なる研究者の結果の比較可能性が制限されるかもしれません。
Furthermore, the results of the 2017 CLEFNewsREEL challenge indicate [122] that being able to very quickly react to incoming news articles, e.g., within a few minutes, is very important to achieve high click-through rates.
さらに、2017年のCLEFNewsREELチャレンジの結果は、入ってくるニュース記事に非常に迅速に、例えば数分以内に反応できることが、高いクリックスルー率を達成するために非常に重要であることを示しています[122]。
It therefore remains unclear how effective complex recommendation algorithms are that can only be re-trained overnight.
したがって、夜間にしか再トレーニングできない複雑なレコメンデーションアルゴリズムがどれほど効果的であるかは、依然として不明である。

# Conclusions and Future Directions 結論と今後の方向性

Our review has shown that news recommendation is an active topic of research and that in recent years significant advances have been made in different directions.
本稿では、ニュース推薦が活発な研究テーマであり、近年、さまざまな方向で大きな進展があったことを紹介した。
In this concluding section, we summarize some key challenges (as discussed in more detail in Sections 3.7 and Section 4.4) and sketch possible directions for future work.
本章では、（セクション 3.7 とセクション 4.4 で詳 細に議論した）いくつかの重要な課題を要約し、今後の研 究の方向性を示す。
In our analysis of algorithmic approaches in Section 3, we found that content-based methods are quite frequently used in the academic literature, i.e., in almost half of the papers.
セクション3のアルゴリズムアプローチの分析では、コンテンツベー スの手法は学術的な文献で非常に頻繁に、つまり、ほぼ半数の論文で使 われていることがわかった。
The observations from our experimental evaluation and from news recommendation challenges in the real world, however, suggest that relying solely on content-based techniques can be insufficient.
しかし、我々の実験的評価や実社会におけるニュース推薦の課題から得られた知見は、コンテンツベースの手法のみに依存することは不十分であることを示唆している。
Factors like general article popularity and recency are highly important in the domain and collaborative-content-based hybrid techniques, as used in the field study by Kirshenbaum et al. [93], are therefore the method of choice when it comes to optimizing IR accuracy measures or click-through rates.
一般的な記事の人気度や再来日のような要素はこの分野では非常に重要であり、Kirshenbaumら[93]のフィールドスタディで使われたような協調コンテンツベースのハイブリッド技術は、したがってIR精度指標やクリックスルー率の最適化に関しては、選択される手法であると言えるでしょう。
However, in this context, more research is needed to better understand how factors like diversity, novelty, or popularity contribute to the quality perception of users, as focusing only on accuracy measures might lead to mostly non-personalized recommendations and little discovery.
しかし、この文脈では、多様性、新規性、人気などの要因がユーザーの品質認識にどのように寄与するかをよりよく理解するために、さらなる研究が必要である。なぜなら、精度指標だけに注目すると、ほとんどパーソナライズされていない推薦とほとんど発見につながるかもしれないからである。
Better personalization is however only possible if more is known about the preferences of the individual users.
しかし、より良いパーソナライゼーションは、個々のユーザーの好みについてより多くの情報が得られて初めて可能になります。
It is therefore important to further investigate the relative importance of long-term and short-term (contextual) preference models.
したがって、長期的な嗜好モデルと短期的な嗜好モデルの相対的な重要性をさらに調査することが重要である。
Research in that direction is however still hampered by the lack of data sets that contain longer user interaction histories.
しかし、この方向での研究は、より長いユーザーとのインタラクションの履歴を含むデータセットがないために、まだ妨げられています。
From an algorithmic perspective, questions regarding scalability were addressed in a number of the reviewed papers.
アルゴリズムの観点からは、スケーラビリティに関する疑問が多くの論文で取り上げられています。
Nowadays, the tools for collecting and storing big amounts of interaction data seem to have reached a high enough maturity level to support basic data processing in real-time.
現在、大量のインタラクションデータを収集・保存するためのツールは、リアルタイムでの基本的なデータ処理をサポートするのに十分な成熟度に達しているようです。
However, training and continuously updating the machine learning models (as done in other domains, e.g., in [81, 82]), remains a challenge, in particular when the models are based on deep learning strategies.
しかし、機械学習モデルの学習と継続的な更新は、（他の領域、例えば[81,82]で行われているように）、特にモデルが深層学習戦略に基づいている場合には、依然として課題である。
In the news domain, new articles that are possibly relevant for a larger number of users can appear several times a day, and these articles have to be immediately considered by the recommendation methods.
ニュース領域では，より多くのユーザに関連する可能性のある新しい記事が1日に数回出現することがあり，これらの記事は推薦手法によって直ちに考慮されなければならない．
Otherwise, the performance of such models can be limited.
そうでなければ、そのようなモデルの性能は制限される可能性があります。
This calls for more research on hybrid methods that are, for example, based on sophisticated long-term models and computationally efficient shortterm adaptation heuristics.
このため、例えば、高度な長期モデルと計算効率の高い短期適応ヒューリスティックに基づくハイブリッド手法の研究が必要である。
With respect to the data perspective, today’s research data sets comprise a number of user features and item features, and quite recently, two large news recommendation data sets have been made publicly available.
データの観点からは、今日の研究データセットは多くのユーザ特徴とアイテム特徴から構成されており、ごく最近、2つの大規模なニュース推薦データセットが公開された。
These new data sets represent a promising starting point for further reproducible research into scalability, sparsity, and user modeling aspects of news recommendation.
これらの新しいデータセットは、ニュース推薦のスケーラビリティ、スパース性、およびユーザーモデリングの側面に関する再現可能な研究をさらに進めるための有望な出発点となっている。
Additionally, researchers are nowadays able to test their approaches on a variety of data set and publishers, which can give further insight into the generalizability of newly proposed algorithms; a crucial aspect of RS design, which has not yet been given enough attention in the literature.
さらに、研究者は最近、様々なデータセットや出版社で自分たちのアプローチをテストすることができるようになり、新たに提案されたアルゴリズムの一般化に関するさらなる洞察を得ることができるようになりました。
At the same time, with the continuous development of the Social Web, the Semantic Web, and the Internet of Things (IoT), a variety of additional data sources will continue to become available in the future.
同時に、ソーシャルウェブ、セマンティックウェブ、IoT（Internet of Things）の継続的な発展により、今後も様々なデータソースが利用可能になることが予想されます。
These data sources, for example, include information about the user’s behavior on Social Web platforms, additional information about the relationships between concepts and named entities in the news articles, or contextual information about the user’s situation derived from smartphone sensors or future IoT devices.
例えば、ソーシャルウェブプラットフォーム上でのユーザーの行動に関する情報、ニュース記事中の概念と名前付きエンティティの関係に関する追加情報、あるいはスマートフォンのセンサーや将来のIoTデバイスから得られるユーザーの状況に関する文脈情報などが、これらのデータソースに含まれる。
A number of research avenues, therefore, exist on how to leverage these possibly huge amounts of additional types of information in the news recommendation process.
このような膨大な量の付加情報をニュース推薦にどのように活用するかについては、様々な研究課題がある。
Looking at methodological aspects, we found that IR measures and click-through rates are the prevalent evaluation measures in the academic literature.
方法論的な側面から見ると、IR指標やクリックスルー率などが学術的な評価指標として一般的であることがわかりました。
Whether or not optimizing algorithms for such measures leads to the best value for the different stakeholders (consumer, news provider, news aggregator) has not been investigated to a large extent in the recommender systems literature in general.
このような評価指標に対してアルゴリズムを最適化することが、異なるステークホルダー（消費者、ニュースプロバイダー、ニュースアグリゲーター）にとって最良の価値につながるかどうかは、推薦システムに関する文献全般であまり調査されていない。
More research and more public data sets that include explicit information about the business value are therefore required to understand, e.g., the economic perspective of news recommenders (“RECO-nomics”) [78] and how to balance the interests of the involved stakeholders.
したがって、例えばニュース推薦者の経済的視点（"RECO-nomics"）[78]や、関係する利害関係者の利益のバランスをとる方法を理解するには、ビジネス価値に関する明確な情報を含むより多くの研究と公開データセットが必要である。
In this context, extended cooperations with news publishers or third-party recommendation providers are also required to better understand the business value of news recommendations.
この文脈では、ニュース推薦のビジネス価値をよりよく理解するために、ニュース出版社や第三者推薦プロバイダーとの拡張協力も必要である。