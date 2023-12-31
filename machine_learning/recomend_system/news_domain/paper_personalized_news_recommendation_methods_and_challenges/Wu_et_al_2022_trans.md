### 0.0.1. link 0.1. リンク

- https://arxiv.org/abs/2106.08934 httpsを使用しています。

### 0.0.2. title 0.2. タイトル

Personalized News Recommendation:
パーソナライズされたニュースの推薦。
Methods and Challenges
その方法と課題

### 0.0.3. abstruct 0.3. アブストラクト

Personalized news recommendation is important for users to ind interested news information and alleviate informationoverload.
個人化されたニュース推薦を行うことは、ユーザが興味のあるニュース情報を見つけ、情報の過負荷を軽減するために重要である。
Although it has been extensively studied over decades and has achieved notable success in improving userexperience, there are still many problems and challenges that need to be further studied.
しかし、まだ多くの問題や課題が残っており、さらに研究を進める必要がある。
To help researchers master theadvances in personalized news recommendation, in this paper we present a comprehensive overview of personalized newsrecommendation.
本論文では、研究者が個人向けニュース推薦の進歩に対応できるように、個人向けニュース推薦の包括的な概観を示す。
Instead of following the conventional taxonomy of news recommendation methods, in this paper wepropose a novel perspective to understand personalized news recommendation based on its core problems and the associatedtechniques and challenges.
本稿では、従来のニュース推薦手法の分類に従うのではなく、ニュース推薦の中核的な問題とそれに関連する技術や課題に基づいて、個人化されたニュース推薦を理解するための新しい観点を提唱する。
We irst review the techniques for tackling each core problem in a personalized news recommendersystem and the challenges they face.
まず、個人向けニュース推薦システムにおいて、それぞれの中核的な問題に取り組むための技術とその課題について概説する。
Next, we introduce the public datasets and evaluation methods for personalized newsrecommendation.
次に、個人化されたニュース推薦のための公開データセットと評価方法を紹介する。
We then discuss the key points on improving the responsibility of personalized news recommender systems.Finally, we raise several research directions that are worth investigating in the future.
最後に、今後検討する価値のある研究の方向性をいくつか挙げる。
This paper can provide up-to-date andcomprehensive views on personalized news recommendation.
本論文は、個人化されたニュース推薦に関する最新かつ包括的な見解を提供することができる。
We hope this paper can facilitate research on personalizednews recommendation as well as related ields in natural language processing and data mining.
また、本論文が自然言語処理とデータマイニングの関連分野と同様に、個人化されたニュース推薦に関する研究を促進することができればと願っている。

# 1. Introduction 1. はじめに

In the era of the Internet, online news distributing platforms such as Microsoft News1have attracted hundredsof millions of users [223].
インターネットの時代には，Microsoft News1のようなオンライン・ニュース配信のプラットフォームが，何億人ものユーザーを引きつけている[223]。
Due to the convenience and timeliness of online news services, many users haveshifted their news reading habits from conventional newspapers to digital news content [144].
オンライン・ニュース・サービスの利便性と適時性のために，多くのユーザが，ニュースを読む習慣を従来の新聞からデジタル・ニュース・コンテンツに移行している[144]．
However, a largenumber of news articles are created and published every day, and it is impossible for users to browse throughall available news to seek their interested news information [204].
しかし，毎日膨大な数のニュース記事が作成・公開されており，ユーザが利用可能なすべてのニュースを閲覧し，興味のあるニュース情報を探し出すことは不可能である[204]．
Thus, personalized news recommendationtechniques, which aim to select news according to users’ personal interest, are critical for news platforms to helpusers alleviate their information overload of users and improve news reading experience [113].
このように，ユーザの個人的な興味に応じてニュースを選択することを目的としたパーソナライズド・ニュース推薦技術は，ユーザの情報過多を緩和し，ニュース読書体験を向上させるために，ニュースプラットフォームにとって重要である[113]．
Researches onpersonalized news recommendation have also attracted increasing attention from both academia and industry inrecent years [144, 203].
また，近年では，パーソナライズド・ニュースの推薦に関する研究も，学界と産業界の双方から注目を集めている[144, 203]。

An example worklow of personalized news recommender system is shown in Fig. 1.
パーソナライズド・ニュースレコメンダーシステムのワークフロー例をFig.1に示す。
When a user visits thenews platform, the news platform will recall a small set of candidate news from a large-scale news pool, andthe personalized news recommender will rank these candidate news articles according to the user interestsinferred from user proiles.
ユーザがニュースプラットフォームを訪問すると、ニュースプラットフォームは大規模なニュースプールから小さなニュース候補を呼び出し、パーソナライズド・ニュースレコメンダーはユーザプロファイルから推測されるユーザの興味に従って、これらのニュース候補をランク付けします。
Then, the top K ranked news will be displayed to the user, and the user behaviorson these news will be recorded by the platform to update the maintained user proile for providing futureservices.
そして、上位K位のニュースがユーザに表示され、これらのニュースに対するユーザの行動がプラットフォームによって記録され、未来サービスを提供するために維持されているユーザプロファイルが更新されます。
Although many prior works have extensively studied these problems in diferent aspects, personalizednews recommendation remains challenging.
**しかし、個人化されたニュースの推薦にはまだ課題が残されています**。
For example, news articles on news websites usually have shortlife cycles.
例えば、ニュースサイト上のニュース記事は、通常、ライフサイクルが短い。
Many new articles emerge every day, and old ones will expire after a short period of time.
ニュースサイトの記事は、毎日多くの新しい記事が作成され、古い記事は短期間で失効する。
Thus,news recommendation faces a severe cold-start problem.
そのため、ニュース推薦にはコールドスタートという問題がある。
In addition, news articles usually contain rich textualinformation such as title and body.
さらに、ニュース記事にはタイトルや本文などの豊富なテキスト情報が含まれている。
Thus, it is very important to understand news content from their texts withadvanced natural language processing techniques.
そのため、**高度な自然言語処理技術によりテキストからニュースの内容を理解することは非常に重要**である。
Moreover, there is usually no explicit user feedback such asreviews and ratings on news platforms.
さらに、**通常、ニュースプラットフォームにはレビューや評価のような明示的なユーザフィードバックが存在しない**。
Thus, we need to infer the personal interests of users from their implicitfeedback like clicks.
そのため、クリックなどの暗黙のフィードバックから、ユーザーの個人的な興味を推測する必要があります。
However, user interests are usually diverse and dynamic, which poses great challenges touser modeling algorithms.
しかし、ユーザの興味は多様で動的であるため、モデル化アルゴリズムには大きな課題がある。
The complexity of personalized news recommendation makes it a fascinating researchtopic with various challenges to be tackled [42].
このように、個人化されたニュース推薦の複雑性は、取り組むべき様々な課題を伴う魅力的な研究テーマとなっている[42]。

A comprehensive overview of existing personalized news recommendation approaches can provide usefulguidance for future research in this ield.
既存の個人化されたニュース推薦手法の包括的な概観は，この分野の将来の研究にとって有用なガイダンスを提供することができる．
Over the past years, there are many survey papers that review thetechniques of news recommendation [8,10,38ś40,42,64,87,110,113,146,162,181].
過去数年にわたり、ニュース推薦の技術について検討した多くのサーベイ論文が存在します[8,10,38ś40,42,64,87,110,113,146,162,181]。
For example, Li et al. [113]reviewed the personalized news recommendation methods based on handcrafted features to build news and userrepresentations.
例えば，Li ら[113]は，ニュースやユーザを表現するために手作業で作成した特徴量に基づくパーソナライズドニュースの推薦手法についてレビューしています．
They covered many traditional feature-based methods, including collaborative iltering (CF)based ones that use the IDs of users and news, content-based ones that use features extracted from the content ofnews and the user behaviors on news, and hybrid ones that rely on content-based collaborative iltering.
彼らは，ユーザとニュースのIDを利用する協調フィルタリング（CF）ベースの手法，ニュースの内容やユーザのニュース上での行動から抽出した特徴を利用するコンテンツベースの手法，コンテンツベースの協調フィルタリングに依存するハイブリッド手法など，従来の特徴ベースの手法を数多く取り上げています．
They alsostudied the datasets used by these methods and their techniques for user and news representation construction, data processing and user privacy protection.
また，これらの手法で使用されるデータセットと，ユーザとニュースの表現構築，データ処理，ユーザのプライバシー保護に関する技術も研究している．
Feng et al. [42] reviewed news recommendation approaches in manydiferent scenarios including personalized and non-personalized ones.
Feng ら [42] は，個人化されたものとそうでないものを含む，さまざまなシナリオにおけるニュース推薦アプローチをレビューしている．
For personalized news recommendationmethods, they also classify them into three categories, i.e., CF-based, content-based, and hybrid.
また，個人化されたニュース推薦手法については，CF ベース，コンテンツベース，ハイブリッドの 3 つのカテゴリーに分類している．
They mainlystudied the techniques adopted by diferent methods, the challenges they tackled, and the datasets and metricsfor evaluation.
また，各方式が採用している手法，取り組んでいる課題，評価のためのデータセットや評価指標についても主に研究している．
We summarize the taxonomy of news recommendation methods and the literature coverage ofseveral recent survey articles in Table 1.
表1では，ニュース推薦手法の分類と，最近のいくつかの調査論文の文献範囲をまとめている．
We ind that most surveys mainly focus on traditional feature-basedmethods and only a small part of deep learning-based methods are covered by a few recent surveys, whichis not beneicial for researchers to track recent advances in the personalized news recommendation ield.
このことは、研究者がパーソナライズドニュースレコメンデーション分野における最近の進歩を追跡する上で有益とは言えない。
Inaddition, most surveys follow the canonical taxonomy that categorizes news recommendation methods basedon whether they rely on collaborative or content-based iltering techniques.
さらに、ほとんどの調査は、協調的手法とコンテンツベースの手法のどちらに基づいてニュース推薦手法を分類するかという定型的な分類法に従っています。
However, it is diicult for thistaxonomy to distinguish between traditional methods and recent deep learning-based approaches.
しかし、この分類法では、従来の手法と最近の深層学習ベースのアプローチを区別することは困難である。
In addition,the hybrid category contains methods based on quite diverse techniques, e.g., traditional CF-enhanced contentmatching and graph neural network, which is not beneicial for researchers to be aware of the evolution of newsrecommendation technologies.
また、ハイブリッドカテゴリには、従来のCFを強化したコンテンツマッチングやグラフニューラルネットワークなど、非常に多様な技術に基づく手法が含まれており、研究者がニュース推薦技術の進化を認識する上で有益とは言えない。
Moreover, several key techniques in news recommender system design, such asranking and model training, are rarely discussed in this paradigm.
さらに、ランキングやモデル学習など、ニュース推薦システム設計におけるいくつかの重要な技術は、このパラダイムではほとんど議論されていない。
Thus, the conventional taxonomy used bymost existing surveys cannot meet the development of this ield, and a more systematic taxonomy of existingnews recommendation methods is needed to help understand their characteristics and inspire further research.
このように、既存のほとんどの調査で用いられている従来の分類法は、この分野の発展に対応することができず、既存のニュース推薦手法の特徴を理解し、さらなる研究を促すために、より体系的な分類法が必要である。

Table 1. The taxonomy and literature coverage of recent survey papers.
最近の調査論文の分類法と文献の範囲。
Traditional taxonomy means the collaborative, content-based, and hybrid categories.
従来のタクソノミは、協調型、コンテンツ型、ハイブリッドのカテゴリーを意味する。
DL stands for deep learning.
DLはディープラーニングを意味する。

In this paper, we present a comprehensive review of the personalized news recommendation ield.
本論文では、個人向けニュース推薦分野の包括的なレビューを行う。
Instead of reviewing existing personalized news recommendation methods based on the conventional taxonomy, in this survey we propose a novel perspective to review them based on the core problems involved in personalized news recommendation and the associated techniques and challenges.
本調査では、従来の分類法に基づいて既存の個人向けニュース推薦手法をレビューするのではなく、個人向けニュース推薦に関わる中核的な問題とそれに関連する技術や課題に基づいてレビューする新しい視点を提案する。
We irst introduce the framework of developing a personalized news recommender system in Section 2.
まず、第2章では、個人向けニュース推薦システムの開発フレームワークを紹介する。
Next, we systematically review the core problems, techniques and challenges in personalized news recommendation, including: news modeling, user modeling, personalized ranking, model training, datasets, benchmarks and evaluation, which are introduced in Sections 3-7, respectively.
次に、セクション3〜7でそれぞれ紹介する、ニュースモデリング、ユーザモデリング、パーソナライズドランキング、モデル学習、データセット、ベンチマーク、評価など、パーソナライズドニュース推薦に関わるコアな問題、技術、課題について系統的にレビューする。
Through our proposed framework, the characteristics of existing approaches can be more accurately described than using conventional taxonomy, and it is easier for researchers to track the technology evolution in diferent aspects.
提案するフレームワークを用いることで、既存のアプローチの特徴を従来の分類法よりも正確に記述することができ、研究者が様々な側面から技術の進化を追跡することが容易になる。
We then present some discussions on developing responsible news recommender systems in Section 9, which is an emerging research ield in recent years.
次に、セクション9では、近年の新しい研究分野である責任あるニュース推薦システムの開発に関するいくつかの議論を紹介する。
Finally, we raise several potential future directions and conclude this paper in Section 10.
最後に、いくつかの将来の方向性を提示し、セクション10で本論文を締めくくる。

<img src="https://d3i71xaburhd42.cloudfront.net/a867894db8f9d544a471e86d8844008861f6a2ec/4-Figure2-1.png">

Fig. 2. A framework of the key components in developing personalized news recommendation model.
パーソナライズドニュースレコメンデーションモデルを開発する際の主要な構成要素のフレームワーク。

# 2. FRAMEWORK OF PERSONALIZED NEWS RECOMMENDATION 2. 2 パーソナライズドニュースレコメンデーションのフレームワーク

Personalized news recommendation techniques have been widely used in many online news websites [144,223].Diferent from non-personalized news recommendation methods that suggest news articles solely based onnon-personalized factors [100] such as news popularity [27,127,130,227], editors’ demonstration [199] andgeographic information [21,178], personalized news recommendation can consider the personal interest of eachindividual user to provide personalized news services and better satisfy users’ need.
パーソナライズド・ニュース推薦技術は，多くのオンライン・ニュース・サイトで広く用いられている[144,223]。ニュースの人気度[27,127,130,227]や編集者の実演[199]，地理情報などの非パーソナライズド要素のみに基づいてニュース記事を推薦する非パーソナライズド・ニュース推薦手法とは異なり，個人化ニュースサービスを提供してユーザのニーズをより良く満足することができる．

Existing surveys on personalized news recommendation usually classify methods into three categories, i.e.,collaborative iltering-based, content-based and hybrid [113].
パーソナライズド・ニュースの推薦に関する既存の調査では，協調的フィルタリング・ベース，コンテンツ・ベース，ハイブリッドという3つのカテゴリに分類されることが多い[113]．
However, this taxonomy cannot adapt to therecent advances in news recommendation because many methods with diverse characteristics fall in the samecategory without distinguishment.
しかし，この分類法では，多様な特徴を持つ多くの手法が区別なく同じカテゴリに分類されるため，最近のニュース推薦の進歩に対応することができない．
For example, the category of content-based methods includes traditionalsemantic-based methods, contextual bandit-based methods and recent deep learning-based methods, which isdiicult to characterize the paradigm and technical evolution of personalized news recommendation.
例えば，コンテンツベースのカテゴリには，従来のセマンティックベースの手法，コンテクストバンディットベースの手法，最近のディープラーニングベースの手法が含まれ，パーソナライズドニュースの推薦のパラダイムと技術進化を特徴付けることは困難である．
Thus, amore systematic overview of existing techniques is required to help understand the development of this field.
したがって、この分野の発展を理解するためには、既存の技術をより体系的に概観することが必要である。

![figure2]()

Instead of following the conventional taxonomy, in this survey we propose a novel perspective to reviewexisting personalized news recommendation techniques based on the core problems involved in the developmentof a personalized news recommender system.
本調査では、従来の分類法ではなく、**personalizedニュース推薦システムの開発における中核的な問題に基づき、既存のpersonalizedニュース推薦技術をレビューする新たな視点を提案する**。
A common framework of personalized news recommendationmodel development is shown in Fig. 2.
図2に、personalizedニュース推薦モデル開発の共通フレームワークを示す。
We can see that there are several key problems in this framework.First, news modeling is the backbone of news recommendation and a core problem is how to understand thecontent and characteristics of news.
このフレームワークでは、いくつかの重要な問題があることがわかる。まず、ニュース推薦のバックボーンである**ニュースモデリング**は、ニュースの内容や特性をどのように理解するかが中核的な問題である。
In addition, user modeling is required to understand the personal interestof users in news, and it is critical to accurately infer user interest from user proiles like behaviors.
また、ニュースに対するユーザの個人的な興味を理解するためには、**ユーザモデリング**が必要であり、行動などのユーザプロファイルからユーザの興味を正確に推論することが重要である。
Based onthe news and user representations built by the news and user models, the next step is ranking candidate newsaccording to certain policies such as the relevance between news and user interest.
ニュースモデルとユーザモデルによって構築されたニュースとユーザの表現に基づき、次のステップでは、ニュースとユーザの関心の関連度合いなどの特定の方針に従って、**候補となるニュースをランク付け**します。
Then, it is important to train the recommendation model with proper objectives to make high-quality news recommendations, and evaluating the ranking results given by the recommendation model is also a core problem in the development ofpersonalized recommender systems.
そして、**適切な目的関数で推薦モデルをトレーニングすること**は、高品質のニュース推薦を行う上で重要である。また、推薦モデルによって与えられるラ**ンキング結果の評価方法(オフライン評価の話...!)**も、パーソナライズド推薦システムの開発における中核的な問題である。
Finally, the datasets and benchmarks for news recommendation are also important for researchers to evaluate the performance of their models.
Besides, the datasets and benchmarks for news recommendation are alsonecessities in designing personalized news recommendation models.
また，ニュース推薦のための**データセットやベンチマーク**は，個人向けニュース推薦モデルを設計する際に必要なものである。
Moreover, beyond developing accuratemodels, improving the responsibility of intelligent systems has been a spotlight problem in recent years.
さらに、**精度の高いモデルを開発するだけでなく、知的システムの責任能力(フィルターバブル的な話??)を向上させること**も、近年注目されている問題である。
How todevelop responsible news recommender systems is a less studied but extremely important problem in personalizednews recommendation.
このように、個人向けニュース推薦において、責任あるニュース推薦システムをいかに構築するかは、あまり研究されていないが、非常に重要な問題である。
Next, we briely discuss the key problems mentioned above in the following sections.
次に、上記の重要な問題について、以下の節で簡単に説明する。

## 2.1. News Modeling

News modeling aims to understand the characteristics and content of news, which is the backbone of newsrecommendation.
ニュースのモデリングは、ニュースの特徴や内容を理解することを目的としており、ニュースレコメンデーションの基幹となるものである。
There are mainly two kinds of techniques for news modeling, i.e., feature-based news modelingand deep learning-based news modeling.
ニュースモデリングには主に2種類の技術がある。すなわち、特徴ベースのニュースモデリングと深層学習ベースのニュースモデリングである。
Feature-based news modeling methods usually rely on handcraftedfeatures to represent news articles.
特徴量ベースのニュースモデリング手法は、通常、ニュース記事を表現するために手作業で作成された特徴量に依存します。
For instance, in many methods based on collaborative iltering (CF), newsarticles are represented by their IDs [29,168].
例えば，協調フィルタリング（CF）に基づく多くの手法では，ニュース記事はそのIDによって表現される[29,168]．
However, on most news websites novel news articles are publishedcontinuously and old ones soon vanish.
しかし，多くのニュースサイトでは，新しいニュース記事は継続的に公開され，古い記事はすぐに消えてしまう．
Thus, representing news articles with their IDs will sufer from severecold-start problems, and the performance is usually suboptimal.
しかし，多くのニュースサイトでは，新しい記事は継続的に公開され，古い記事はすぐに消えてしまうため，IDで表現した場合，古い記事から始まる問題が発生し，性能が低下することが多い．

Considering the drawbacks of ID-based news modeling methods, most approaches incorporate content featuresto represent news.
IDベースのニュースモデリング手法の欠点を考慮し，多くのアプローチはニュースを表現するためにコンテンツの特徴を取り入れている．
Among them, many methods use features extracted from news texts for news modeling.
その中で，多くの手法はニューステキストから抽出した特徴をニュースのモデリングに用いている．
For instance, Capelle et al. [16] proposed to represent news with Synset Frequency-Inverse Document Frequency(SF-IDF), which uses WordNet synonym set to replace the term frequencies in TF-IDF.
例えば，Capelleら[16]はSynset Frequency-Inverse Document Frequency(SF-IDF)を用いてニュースを表現することを提案しています．これは，TF-IDFの用語頻度をWordNetの同義語セットで置き換えるものです．
Besides the news texts,many methods also explore to incorporate various factors that may have inluence on users’ news browsingdecisions into news modeling, such as news popularity and recency [109].
また，ニューステキスト以外にも，ニュースの人気度や新着度など，ユーザのニュース閲覧の意思決定に影響を与える様々な要因をニュースモデリングに取り込むことを試みる手法も多く存在する[109]．
However, in these methods, the featuresto represent news are usually manually designed, which usually requires much efort and domain knowledge.
しかし，これらの手法では，ニュースを表現するための特徴は通常手作業で設計され，多くの労力とドメイン知識が必要とされる．
Inaddition, handcrafted features are usually not optimal in representing the semantic information encoded in newstexts.
さらに，手作業で設計された特徴量は，通常，ニューステキストにコード化された意味情報を表現する上で最適ではない．

With the development of natural language processing techniques in recent years, many methods employneural NLP models to learn deep representations of news.
近年の自然言語処理技術の発展に伴い、ニュースの深い表現を学習するためにニューラルNLPモデルを採用する手法も多くなっている。
For example, Okura et al. [144] proposed to useautoencoders to learn news representations from news content.
例えば、**大倉ら[144]は、オートエンコーダーを用いて、ニュースコンテンツからニュース表現を学習すること**を提案している。
Wang et al. [197] proposed to use a knowledge-aware convolutional neural network (CNN) to learn news representations from news titles and their entities.
Wangら[197]は、知識認識型畳み込みニューラルネットワーク（CNN）を用いて、ニュースのタイトルとその実体からニュース表現を学習することを提案している。
Wuet al. [207] proposed to learn news representations from news titles via a combination of multi-head self-attentionand additive attention networks.
Wuら[207]は、マルチヘッド自己注意ネットワークと付加的注意ネットワークの組み合わせによって、ニュースタイトルからニュース表現を学習することを提案した。
Wu et al. [214] studied to use pre-trained language models to encode news texts.These deep learning-based news modeling methods can automatically learn informative news representationswithout heavy efort on manual feature engineering, and they can usually better understand news content thantraditional feature-based methods.
Wuら[214]は、事前に学習した言語モデルを用いてニューステキストをエンコードすることを研究しました。これらの深層学習ベースのニュースモデリング手法は、マニュアルの特徴量エンジニアリングに大きな負担をかけずに情報量の多いニュース表現を自動的に学習でき、通常は従来の特徴ベースの手法よりもニュースコンテンツをよく理解することができます。

## 2.2. User Modeling

User modeling techniques in news recommendation aim to understand users’ personal interest in news.
ニュース推薦におけるユーザモデリング技術は，ユーザのニュースに対する個人的な興味を理解することを目的としている．
Similar tonews modeling, user modeling methods can also be roughly classiied into two categories, i.e., feature-based and deep learning-based.
ニュースのモデリングと同様に，ユーザモデ リング手法も特徴ベースと深層学習ベースの 2 種類に大別される．
Some feature-based methods like CF represent users with their IDs [29,168].
CF のような特徴ベースの手法は，ユーザを ID で表現する[29,168] がある．
However, theyusually sufer from the sparsity of user data and cannot model user interest accurately.
しかし，CF のような特徴に基づく手法は，ユーザデータの疎らさに悩まされ，ユーザの興味を正確にモデル化することができない．
Thus, most feature-basedmethods consider other user information such as click behaviors on news.
そこで，多くのFeature-based手法は，ニュースに対するクリック行動など，他のユーザ情報を考慮する．
For example, Garcin et al. [52] proposedto use Latent Dirichlet Allocation (LDA) to extract topics from the concatenation of news title, summary andbody.
例えば，Garcinら[52]は，Latent Dirichlet Allocation (LDA) を用いて，ニュースのタイトル，要約，本文を連結したものからトピックを抽出することを提案している．
The topic vectors of all clicked news are further aggregated into a user vector by averaging.
さらに、クリックされた全てのニュースのトピックベクトルを平均化することにより、ユーザベクトルに集約する。
There are alsoseveral works that explore to incorporate other user features into user modeling, such as demographics [104],location [43] and access patterns [109].
また，デモグラフィックス[104]，ロケーション[43]，アクセスパターン[109]などの他のユーザの特徴をユーザモデリングに組み込むことを検討した研究もいくつか存在する．
However, feature-based user modeling methods also require an enormousamount of domain knowledge to design informative user features in speciic scenarios, and they are usuallysuboptimal in representing user interests.
しかし，特徴ベースのユーザモデリング手法は，特定のシナリオにおいて有益なユーザ特徴を設計するために膨大なドメイン知識を必要とし，通常，ユーザの興味を表すには最適とはいえない．

There are several methods that use neural networks to learn user representations from users’ click behaviors.For example, Okura et al. [144] proposed to use a GRU network to learn user representations from clicked news.Wu et al. [204] proposed a personalized attention network to learn user representations from clicked news in apersonalized manner.
例えば，Okuraら[144]はGRUネットワークを用いてクリックされたニュースからユーザ表現を学習することを提案し，Wuら[204]はクリックされたニュースからユーザ表現を個人別に学習するpersonalized attention networkを提案している．
Qi et al. [160] proposed a hierarchical user interest representation method to model thehierarchical structure of user interest.
Qiら[160]は、ユーザの興味の階層構造をモデル化する階層的ユーザ興味表現手法を提案した。
These methods can automatically learn deep interest representations ofusers for personalized news recommendation, which are usually more accurate than handcrafted user interestfeatures.
これらの手法は，個人化されたニュース推薦のためにユーザの深い興味表現を自動的に学習することができ，通常，手作業で作成したユーザ興味特徴よりも精度が高い．

### 2.2.1. 2.3 Personalized Ranking 2.3. パーソナライズドランキング

On the basis of news and user interest modeling, the next step is ranking candidate news in a personalizedway according to user interest.
ニュースおよびユーザインタレストのモデリングに基づき、次のステップは、ユーザの興味に応じてパーソナライズされた方法でニュース候補をランク付けすることである。
Most methods rank news based on their relevance to user interest, and how toaccurately measure the relevance between user interest and candidate news is their core problem.
多くの手法は，ユーザの興味とニュースの関連性に基づいてニュースをランク付けしており，ユーザの興味とニュース候補の関連性をどのように正確に測定するかが問題の核心である．
Some methodsmeasure the user-news relevance based on their representations.
また，ユーザとニュースの関連性を表現に基づいて測定する手法もある．
For example, Goossen et al. [58] proposed tocompute the cosine similarity between the Concept Frequency-Inverse Document Frequency (CF-IDF) featuresextracted from candidate news and clicked news, which was further used for personalized candidate newsranking.
例えば，Goossenら[58]は，候補ニュースから抽出したCF-IDF（Concept Frequency-Inverse Document Frequency）特徴とクリックされたニュースとの間のコサイン類似度を計算し，さらにパーソナライズした候補ニュースランキングに利用することを提案している．
Okura et al. [144] used the inner product between news and user embeddings to compute the clickscores, and ranked candidate news based on these scores.
大倉ら[144]はクリックスコアの計算にニュースとユーザ埋め込み間の内積を用い，そのスコアに基づいてニュース候補をランク付けしています．
Gershman et al. [55] proposed to use an SVM model foreach individual user to classify whether this user will click a candidate news based on news and user interestfeatures.
Gershmanら[55]は，個々のユーザに対してSVMモデルを用い，そのユーザがニュース候補をクリックするかどうかを，ニュースとユーザの興味の特徴に基づいて分類することを提案している．
In several recent methods, the relevance between candidate news and user interest is modeled in aine-grained way by matching candidate news with clicked news.
最近のいくつかの手法では，ニュース候補とクリックされたニュースをマッチングすることで，ニュース候補とユーザの関心の関連性をきめ細かくモデル化する．
For example, Wang et al. [196] proposed tomatch candidate news and clicked news with a 3-D convolutional neural network to mine the ine-grainedrelatedness between their content.
例えば，Wangら[196]は，3次元畳み込みニューラルネットワークを用いて候補ニュースとクリックされたニュースをマッチングし，それらのコンテンツの間の粒度の細かい関連性をマイニングすることを提案している．
However, ranking candidate news and user interest merely based on theirrelevance may recommend news that are similar to those previously clicked by users [160], which may cause thełilter bubble” problem.
しかし，ニュース候補とユーザの興味・関心を単に関連性でランク付けすると，ユーザが過去にクリックしたニュースと類似したニュースを推薦する可能性があり[160]，「フィルタバブル」問題を引き起こす可能性がある．

A few methods use reinforcement learning for personalized ranking.
いくつかの方法は、パーソナライズされたランキングのために強化学習を使用しています。
Li et al. [106] irst explore to model thepersonalized news recommendation task as a contextual bandit problem.
Liら[106]は，パーソナライズされたニュース推薦タスクを文脈的バンディット問題としてモデル化することを初めて試みた．
They proposed a LinUCB approach thatcomputes the upper conidence bound (UCB) of each arm eiciently in closed form based on a linear payof model,which can match news with users’ personal interest and meanwhile explore making diverse recommendations.DRN [244] uses a deep reinforcement learning approach to ind the interest matching policy that optimizes thelong-term reward.
彼らは，線形ペイオフモデルに基づいて各アームの上限信頼限界（UCB）を閉形式で効率的に計算するLinUCBアプローチを提案し，ニュースをユーザの個人的な興味にマッチングさせ，一方で多様な推薦を行うことを検討している．
In addition, it uses a Dueling Bandit Gradient Descent (DBGD) method for exploration.
また、探索にはDueling Bandit Gradient Descent (DBGD) 法が用いられる。
Thesemethods usually optimize the long-term reward rather than the current click probability, which has the potentialto alleviate the ilter bubble problem by exploring more diverse user interest.
これらの手法は通常，現在のクリック確率よりも長期的な報酬を最適化し，より多様なユーザの興味を探索することでイルターバブル問題を緩和する可能性を持っている．

## 2.3. 2.4 Model Training 2.4. 2.4 モデルトレーニング

Many personalized news recommendation methods employ machine learning models for news modeling, usermodeling and interest matching.
個人向けニュース推薦手法の多くは，ニュースのモデリング，ユーザモデリング，インタレストマッチに機械学習モデルを用いている．
How to train these models to make accurate recommendations is a criticalproblem.
これらのモデルをどのように学習させ，正確な推薦を行うかは重要な問題である．
A few methods train their models by predicting the ratings on news given by users.
いくつかの手法は，ユーザのニュースに対する評価を予測することによってモデルを学習する．
For example, theGrouplens [168] system is trained by predicting the unknown ratings in the user-news matrix.
例えば、Grouplens [168] システムでは、ユーザ-ニュース行列の未知の評価を予測することによって学習する。
However, explicitfeedback such as ratings is usually sparse on news platforms.
しかし、ニュースプラットフォームでは通常、視聴率のような明示的なフィードバックはまばらである。
Thus, most existing methods use implicit feedbacklike clicks to construct prediction targets for model training.
そこで、既存の手法の多くは、クリックのような暗黙的なフィードバックを用いて、モデル学習のための予測対象を構築する。
For example, Wang et al. [197] formulated the newsclick prediction problem as a binary classiication task, and use crossentropy as the loss function for modeltraining.
例えば、Wangら[197]はニュースクリック予測問題を二値分類タスクとして定式化し、モデル学習のための損失関数としてクロスエントロピーを使用しています。
Wu et al. [204] proposed to employ negative sampling techniques that combine each positive samplewith several negative samples to construct labeled samples for model training.
Wuら[204]は、モデル学習のためにラベル付きサンプルを構築するために、各陽性サンプルと複数の陰性サンプルを結合する陰性サンプリング技術を採用することを提案した。
However, click feedback usuallycontains heavy noise and may not indicate user interest, which poses great challenges to learning accuraterecommendation models.
しかし、クリックフィードバックには通常大きなノイズが含まれており、ユーザの興味を示していない可能性があるため、正確な推薦モデルを学習する上で大きな課題となる。

There are only a few methods that consider user feedback beyond click signals [213,215].
また，クリック信号以外のユーザからのフィードバックを考慮した手法は少ない[213,215]．
For example,Wu et al. [213] proposed to model click preference with click feedback and model reading satisfaction basedon the personalized reading speed of users, and train the recommendation model to predict both clicks anduser satisfaction.
例えば，Wuら[213]は，クリックフィードバックを用いてクリック嗜好をモデル化し，ユーザの個人化された読書速度に基づいて読書満足度をモデル化し，クリック数とユーザ満足度の両方を予測する推薦モデルを学習することを提案している．
By optimizing objectives beyond news clicks, these methods are aware of user engagementinformation and thereby can better understand user interest.
これらの手法は，ニュースのクリック数以外の目的を最適化することで，ユーザのエンゲージメント情報を意識し，ユーザの興味をより理解することができる．
In addition, these methods have the potential torecommend news articles that are not only clicked by users, but also indeed satisfy their information needs.
さらに、これらの手法は、ユーザがクリックするだけでなく、ユーザの情報ニーズを満たすようなニュース記事を推薦する可能性がある。
Thus,designing engagement-aware training objectives is useful for news recommender systems to provide high-qualitynews suggestions.
このように、エンゲージメントを考慮した学習目標を設計することは、ニュース推薦システムが高品質なニュース推薦を行うために有用である。

## 2.4. 2.5 Evaluation 2.5. 2.5 評価

Properly evaluating the performance of personalized news recommendation algorithms is important for devel-oping real-world news recommender systems.
個人向けニュース推薦アルゴリズムの性能を適切に評価することは，実世界のニュース推薦システムを開発する上で重要である．
Most existing methods use click-related metrics to measure theaccuracy of recommendation results.
既存の手法の多くは，推薦結果の精度を測定するためにクリック関連指標を用いている．
Some of them regard the recommendation task as a classiication prob-lem [70,116,197], where the performance is evaluated by classiication metrics such as Area Under Curve (AUC)and F1-score.
また，推薦タスクを分類問題[70,116,197]として捉え，AUC (Area Under Curve) やF1-score などの分類指標によって性能を評価する手法もある．
Many other methods use ranking metrics such as Mean Reciprocal Rank (MRR) and normalized Dis-counted Cummulative Gain (nDCG).
また，MRR（Mean Reciprocal Rank）やnDCG（Normalized Dis-counted Cummulative Gain）といったランキング指標を用いる手法も多くある．
However, click-based metrics may not indicate user experience.
しかし，クリックベースの指標はユーザエクスペリエンスを示さない可能性がある．
Thus, a fewworks explore to use user engagement-based metrics to evaluate the recommendation performance [215], such asdwell time and dislike, which can evaluate the performance of recommendation models more comprehensively.In most works, the performance of recommendation models is oline evaluated.
しかし，クリックベースの指標はユーザエクスペリエンスを示さない可能性がある．そこで，滞留時間や嫌悪度などのユーザエンゲージメントベースの指標を用いて推薦性能を評価する研究がいくつか行われている[215]．
However, the data used foroline evaluation is usually inluenced by the recommendation results generated by the predecessor recommen-dation algorithms, and the real user feedback on recommendation results cannot be obtained.
しかし，オンライン評価に用いるデータは，先行する推薦アルゴリズムが生成した推薦結果に影響されることが多く，推薦結果に対する実際のユーザのフィードバックが得られない．
Only a few worksreported online evaluation results [214], which may better indicate the real performance of the recommendersystems.
また，オンライン評価結果を報告した研究は少なく[214]，これは推薦システムの実際の性能をよりよく表している可能性がある．
To ill the gaps between oline and online experiments, one prior study [107] proposed an unbiasedevaluation method of contextual bandit-based news recommendation methods.
このようなオンライン実験とオンライン実験のギャップを埋めるため，先行研究 [107] では，文脈バンディット型ニュース推薦手法の非バイアス評価法を提案している．
However, there still lacks a generalmethod that can oline evaluate the potentials of various news recommender algorithms in online environments.
しかし，オンライン環境における様々なニュース推薦アルゴリズムの潜在能力をオンライン上で評価できる一般的な方法はまだ存在しない．

## 2.5. 2.6 Dataset and Benchmark 2.6. 2.6 データセットとベンチマーク

Publicly available datasets are important for facilitating researches in the corresponding ields as well as bench-marking their results and indings.
一般に公開されているデータセットは、対応する分野の研究を促進し、その結果や指標をベンチマークするために重要である。
However, in the personalized news recommendation ield most researches areconducted on proprietary datasets collected from diferent news platforms, such as Google News, Microsoft News,Yahoo News, Bing News, etc.
しかし、個人向けニュース推薦の分野では、ほとんどの研究がGoogle News、Microsoft News、Yahoo News、Bing Newsなどの異なるニュースプラットフォームから収集した独自のデータセットで実施されている。
There are only a few datasets that are publicly available for news recommendationresearch.
また，一般に公開されているデータセットは数少ない．
Several representative datasets such as plista [91], Adressa [61] and MIND [223] are widely used byrecent studies.
最近の研究では，plista [91], Adressa [61], MIND [223]などの代表的なデータセットが広く利用されている．
The plista dataset is a German news dataset.
plistaはドイツのニュースデータセットである．
A newer version of this dataset is published by the CLEF 2017 NewsREEL [126] task, and a competition is held based on this data to train and evaluate newsrecommender systems.
このデータセットの新しいバージョンはCLEF 2017 NewsREEL [126]タスクによって公開されており，このデータに基づいてニュースレコメンダーシステムの学習と評価のためのコンペティションが開催されている．
Adressa is a Norwegian dataset that contains not only click information, but also the dwelltime of users and rich context information of users and news.
Adressaはノルウェーのデータセットで，クリック情報だけでなく，ユーザの滞留時間やユーザとニュースのリッチなコンテキスト情報を含んでいる．
MIND is a large-scale English news recommendationdataset with raw textual information of news.
MINDは大規模な英語ニュース推薦データセットであり、ニュースの生テキスト情報を含んでいる。
In addition, MIND is associated with a public leaderboard andan open competition, which can fairly compare the performance of diferent algorithms.
また、MINDは公開のリーダーボードとオープンなコンペティションに関連しており、異なるアルゴリズムの性能を公平に比較することができる。
Thus, many recentresearches are conducted on the MIND dataset [210, 214, 218].
そのため、MINDデータセットを用いた多くの研究が行われている[210, 214, 218]。

## 2.6. 2.7 Responsible News Recommendation 2.7. 2.7 レスポンシブル・ニュースのススメ

Given the overview above, we then present in-depth discussions on each mentioned core problem in thefollowing sections.
以上の概要を踏まえ、以下の章では、それぞれの核心的問題について、より深い議論を展開する。

# 3. 3 NEWS MODELING 3. 3 ニュースモデリング

News modeling is a critical step in personalized news recommendation methods to capture the characteristicsof news articles and understand their content.
ニュースのモデリングは、ニュース記事の特徴を捉え、その内容を理解するためのパーソナライズド・ニュースレコメンデーション手法において重要なステップである。
The techniques for news modeling can be roughly divided intotwo categories, i.e., feature-based and deep learning-based.
ニュースモデリングの手法は、特徴量ベースと深層学習ベースの2つに大別される。
For feature-based methods, news articles are mainlyrepresented by handcrafted features, while deep learning-based methods mainly aim to learn hidden newsrepresentations from the raw inputs.
特徴量ベースの手法では、ニュース記事は主に手作業で作成された特徴量によって表現される。一方、深層学習ベースの手法は、生の入力から隠れたニュース表現を学習することを主な目的としている。
Note that although a few methods may employ some deep learning methodslike multi-layer perceptrons to model interactions between sophisticated handcrafted features, we still categorizethem into feature-based ones because their news representations are not learned from scratch.
ただし、一部の手法では多層パーセプトロンのような深層学習手法を採用し、高度な手作り特徴間の相互作用をモデル化しているが、それらのニュース表現はゼロから学習していないため、我々はそれらを特徴ベースのものに分類していることに注意されたい。
In addition, somedeep learning-based methods may involve some eforts in feature engineering.
また，深層学習ベースの手法の中には，特徴量エンジニアリングの努力を必要とするものがある．
Since their news representationmethods mainly focus on incorporating additional features to enhance deep representations learned from scratch,we still put them into the deep learning-based category.
また、深層学習ベースの手法の中には、特徴量エンジニアリングを行うものもあるが、それらの手法のニュース表現では、ゼロから学習した深層表現を強化するための追加特徴を組み込むことに主眼を置いているため、やはり深層学習ベースのカテゴリーに分類する。
The details of the two types of news modeling methodsare as introduced follows.
2種類のニュースモデリング手法の詳細は以下の通りである。

<img src="https://d3i71xaburhd42.cloudfront.net/a867894db8f9d544a471e86d8844008861f6a2ec/9-Figure3-1.png">

Fig. 3.
図3.
An overview of different types of news features.
様々なタイプのニュース特集の概要。

## 3.1. 3.1 Feature-based News Modeling 3.1. 3.1 特徴に基づくニュースのモデル化

Designing informative features to represent news articles is the key problem in feature-based news modelingmethods.
ニュース記事を表現するための情報量の多い特徴量を設計することは、特徴量ベースのニュースモデリング手法の重要な問題である。
As summarized in Fig. 2, there are mainly four types of features used in news modeling, which areintroduced as follows.
図2に示すように、ニュースモデリングに用いられる特徴量には主に4つの種類があり、以下に紹介する。

In many CF-based methods, news articles are represented by collaborative iltering signals such as newsIDs [29,62,78,141,168,172,225].
多くのCFベースの手法では，ニュース記事はnewsIDのような協調的フィルタリング信号で表現される [29,62,78,141,168,172,225]．
However, on most news websites novel news are published quickly and oldones will soon vanish.
しかし，多くのニュースサイトでは，新しいニュースはすぐに公開され，古いニュースはすぐに消えてしまう．
These methods model news in a content-agnostic manner, which may sufer from theserious cold start problem due to the diiculty in processing newly generated news.
これらの方法は，ニュースの内容に依存しないため，新しく生成されたニュースを処理することが難しく，深刻なコールドスタート問題に悩まされる可能性があります．
Thus, it is not suitable tosimply represent news articles with their IDs [37].
このように，ニュース記事を単純にIDで表現することは適切ではありません[37]．

Due to the drawbacks of ID-based news modeling, many methods incorporate news content into news modeling.For instance, Gershman et al. [55] considered Term Frequency-Inverse Document Frequency (TF-IDF) featuresextracted from news texts.
例えば，Gershman et al. [55]は，ニューステキストから抽出したTF-IDF（Term Frequency-Inverse Document Frequency）素性を検討している．
In news articles, entities
ニュース記事において，エンティティ

Besides semantic features, some works explore to extract other kinds of content features to enhance model-ing [104,109,147].
また，意味的特徴に加え，他の種類のコンテンツ特徴を抽出し，モデリングを強化しようとする研究もある[104,109,147]．
For example, Garcin et al. [52] proposed to use Latent Dirichlet Allocation (LDA) to extracttopics from the concatenation of news title, summary and main content.
例えば，Garcinら[52]はLDA（Latent Dirichlet Allocation）を用いて，ニュースのタイトル，要約，本文を連結してトピックを抽出することを提案した．
Parizi et al. [147] proposed to extractemotion features of sentences in news as complementary information of TF-IDF features.
Pariziら[147]は，TF-IDF特徴の補完情報として，ニュース中の文の感情特徴を抽出することを提案している．
In their method, theemotion is represented by the Ekman model that contains 6 emotion categories.
彼らの手法では，感情は6つの感情カテゴリを含むEkmanモデルによって表現される．
A variant of this method thatuses the sentiment orientation (i.e., positive, neutral and negative) is also developed by Parizi et al. [148].
また，Pariziら[148]は，情動の方向性（肯定，中立，否定）を利用したこの手法の派生版も開発している．
Beyondnews texts, the exploitation of vision-related information such as the videos of news is also studied in [131].These features can provide complementary information to better understand news content.
ニューステキストを越えて、ニュースのビデオなどの視覚関連情報を利用することも、[131]で研究されている。

In addition to content features, many other genres of features are used for news modeling.
ニュースのモデル化には，内容特徴の他に多くの特徴ジャンルが用いられる。
They can be roughlydivided into two categories, i.e., property features and context features.
これらは大きく分けて、特性特徴と文脈特徴の2つに分類される。
Property features such as categories,locations and publishers usually relect intrinsic properties of news.
カテゴリ、場所、出版社などの特性は、通常、ニュースの本質的な特性を反映しています。
The most widely used news property featureis category, since it is an important clue for modeling news content and targeting user interest.
最も広く用いられているのはカテゴリであり，これはニュースの内容をモデル化し，ユーザの関心をターゲットとするための重要な手がかりとなります．
For example,Liu et al. [122] proposed to represent news using their topic categories.
例えば，Liu ら [122] は，トピックカテゴリを使用してニュースを表現することを提案している．
However, since the category labelsof news often need to be manually annotated by editors, in some scenarios news may not have of-the-shelf category labels, Thus, several methods explore to cluster news into categories based on their content.
しかし，ニュースのカテゴリ・ラベルは編集者によって手動でアノテーションされる必要があるため，あるシナリオではニュースには既成のカテゴリ・ラベルがない場合があります．
For instance,in the SCENE [109] recommender system, news articles are clustered in a hierarchical manner based on theirtopic features extracted by LDA.
例えば，SCENE [109] 推薦システムでは，LDA によって抽出されたトピックの特徴に基づき，ニュース記事を階層的にクラスタリングしている．
By incorporating the categories or clusters of news into news modeling, thenews recommender can be aware of news topics and provide more targeted recommendation services.
ニュースのカテゴリやクラスタをニュースのモデリングに組み込むことで、ニュース推薦者はニュースのトピックを認識し、より的を射た推薦サービスを提供することができます。
Anotherrepresentative property feature is news location, which is also widely used to provide users with the news relatedto the locations that they are interested in.
もう一つの代表的な特性は、ニュースの位置情報であり、これもユーザが興味のある場所に関連したニュースを提供するために広く利用されている。
For example, Tavakolifard et al. [187] incorporated the geographicinformation of news to ilter news based on their locations.
例えば，Tavakolifard ら [187] は，ニュースの地理情報を組み込んで，その場所に基づいてニュースを検索しています．
In addition, since news from diferent publishersmay have diferences in their content and topics, the information of news publisher is also considered by severalmethods to enrich the information for news modeling [75, 117].
また，出版社が異なればニュースの内容やトピックも異なるため，出版社の情報もニュースのモデル化のために考慮されます[75, 117]．

Diferent from property features that are usually static after news publishing, context features of news aredynamic.
ニュースの文脈特性は，通常，ニュース発行後に静的な特性であるのに対して，動的な特性である。
Popularity and recency, which relect the attractiveness and freshness of news, are two representativecontext features used by existing methods.
既存の手法では，ニュースの魅力や新鮮さを表す「人気度」や「最新度」が代表的なコンテキスト特徴として利用されている．
For instance, MONERS [104] is a news recommender system thatrepresents news articles by news categories, news importance suggested by providers and the recency of newsarticles.
例えば，MONERS [104]はニュース推薦システムであり，ニュースカテゴリ，プロバイダが提案するニュースの重要度，ニュース記事の新着度によってニュース記事を表現している．
Gershman et al. [55] proposed to use four kinds of features to represent news, i.e., news popularity,news age (recency), TF-IDF features of words and named entities.
Gershmanら[55]は，ニュースの人気度，ニュースエイジ（再放送頻度），単語のTF-IDF特徴，名前付き実体の4種類の特徴を用いて，ニュースを表現することを提案している．
Jonnalagedda et al. [82] proposed to use thetimeline on Twitter to enhance news modeling.
Jonnalageddaら[82]は，Twitter上のタイムラインを利用してニュースのモデリングを行うことを提案している．
They use the popularity and categories of news on Twitter fornews representation.
彼らは，Twitter上のニュースの人気度とカテゴリをニュースの表現に利用している．
News recency only considers the time interval between the publishing and display of news,while time stamp of news display can provide iner-grained information, such as seasons, months, days and thetime in a day.
一方，ニュースのタイムスタンプは，季節，月，日，1日の時間など，より細かい情報を提供することができる．
Thus, several approaches incorporate the time stamp of news impression [25,41,43,75,225].
そのため，ニュースのタイムスタンプを利用するアプローチもある[25,41,43,75,225]．
Forexample, Ilievski et al. [75] proposed to incorporate the weekday and the hour of a news impression in newsmodeling.
例えば，Ilievskiら[75]は，ニュースの印象の曜日と時間をニュースモデリングに取り入れることを提案しています．
In addition to the context features mentioned above, several methods also explore to use weather [229],click-through rate (CTR) [25], and fact
また，上記のコンテキスト機能に加えて，天気 [229]，クリックスルー率 (CTR)[25]，事実[225]を利用する方法も検討されている．

Some hybrid methods consider both news IDs and additional features in news modeling [125].
ハイブリッド手法の中には，ニュースIDと付加的な特徴の両方を考慮し，ニュースモデリングを行うものもあります[125]．
For example,NewsWeeder [99] represents news articles by their IDs and bag-of-word features.
例えば，NewsWeeder [99]は，ニュース記事をIDおよびbag-of-wordの特徴量によって表現している．
Claypool et al. [26] proposedto use news IDs and keywords to model news.
Claypoolら[26]は，ニュースIDとキーワードを用いてニュースをモデル化することを提案している．
Liu et al. [122] proposed to represent news using their IDsand topic categories.
Liuら[122]はニュースのIDとトピックカテゴリを用いてニュースを表現することを提案した。
Saranya et al. [171] proposed to represent news by their IDs, topics, click frequencyand the weights of a news belonging to diferent categories.
Saranyaら[171]は、ニュースのID、トピック、クリック頻度、異なるカテゴリに属するニュースの重みによってニュースを表現することを提案した。
Using the combination of ID-based and content-based news modeling techniques can mitigate the cold-start problem of news to some extent, and have beenwidely explored by integrating other information like news property features [28,202], news sessions [182],ontology [15, 48, 142, 163, 173] and knowledge graphs [236].
IDベースとコンテンツベースの組み合わせによるニュースモデリング技術は，ニュースのコールドスタート問題をある程度軽減することができ，ニュースの特性[28,202]，ニュースセッション[182]，オントロジー[15，48，142，163，173]と知識グラフ[236]など他の情報を統合して広く研究されてきた．

To draw a big picture of feature-based news modeling methods, we summarize the major features they used in Table 2.
特徴量ベースのニュースモデリング手法の全体像を描くために、それらが使用する主な特徴量を表2にまとめた。

<img src="https://d3i71xaburhd42.cloudfront.net/a867894db8f9d544a471e86d8844008861f6a2ec/10-Table2-1.png">

Table 2.
表2.
Main features used for news representation.
ニュース表現に使用した主な特徴量。
\*XF-IDF means TF-IDF and its variants such as CF-IDF and SF-IDF.
\*XF-IDFはTF-IDFとCF-IDFやSF-IDFなどの派生型を意味する。

## 3.2. 3.2 Deep learning-based News Modeling 3.2. 3.2 ディープラーニングによるニュースモデリング

With the development of deep learning techniques, in recent years many methods employ neural networksto automatically learn news representations.
近年，深層学習技術の発展に伴い，ニュース表現を自動的に学習するためにニューラルネットワークを採用する手法が多くなっている．
Instead of using handcrafted features like TF-IDF to representnews content, most of them use neural NLP techniques to learn news representations from news texts.
TF-IDF のような手作りの特徴量を用いてニュースコンテンツを表現するのではなく、それらの多くはニューラル NLP 技術を用いてニューステキストからニュース表現を学習しています。
Forexample, Okura et al. [144] proposed an embedding-based news recommendation (EBNR) method that uses avariant of denoising autoencoders to learn news representations from news texts.
例えば，Okura ら [144] は埋め込み型ニュース推薦法 (EBNR) を提案しており，この方法では，ノイズ除去オートエンコーダの変種を用いて，ニューステキストからニュース表現を学習しています．
RA-DSSM [96] is a neuralnews recommendation approach which incorporates a similar architecture as DSSM [72].
RA-DSSM [96]はDSSM [72]と同様のアーキテクチャを持つニューラルニュース推薦法である．
It irst builds therepresentations of news using the doc2vec [102] tool, then uses a two-layer neural network to learn hidden newsrepresentations.
まず、doc2vec [102]というツールを使ってニュースの表現を構築し、次に2層のニューラルネットワークを使って隠れたニュースの表現を学習する。
This method is also adopted by [97].
この方法は、[97]でも採用されている。
3-D-CNN [98] represents news by the word2vec [139]embeddings of their words, which is further considered by [242].
3-D-CNN [98]では，ニュースの単語をword2vec [139]で埋め込んで表現しており，さらに[242]で検討されている．
However, it is diicult for these methods tomine the semantic information in news texts with traditional neural NLP models.
しかし、これらの方法では、従来のニューラル自然言語処理モデルでは、ニューステキストの意味情報を読み取ることが困難である。

Many later approaches use more advanced neural NLP models for text modeling, such as CNN [196,239] andself-attention [207].
後発の多くのアプローチは、CNN [196,239]や自己注 意[207]など、より高度なニューラルNLPモデルをテキストモデリン グに用いている。
For instance, WE3CN [90] uses 2D CNN models to learn representations of news.
例えば、WE3CN [90]は2次元CNNモデルを用いてニュースの表現を学習している。
NPA [204]uses CNN to generate contextual representations of words in news titles, and use a personalized attentionnetwork to form news representations by selecting important words in a personalized manner.
NPA [204]はCNNを用いてニュースのタイトルに含まれる単語の文脈表現を生成し、パーソナライズされた注意ネットワークを用いて、パーソナライズされた方法で重要な単語を選択することでニュース表現を形成している。
NRMS [207] learnsword representations with a multi-head self-attention network, and uses an additive attention network to formnews representations.
NRMS[207]では、多頭自己注意ネットワークを用いて単語表現を学習し、加法的注意ネットワークを用いてニュース表現を形成している。
Similar news modeling method is also used by many later works [212,213,215,218,221].NRNF [209] uses self-attention to model the contexts of words in news title and body, and it uses an interactiveattention network to model the relatedness between title and body.
NRNF [209]は自己注意を用いてニュースのタイトルと本文の単語の文脈をモデル化し、インタラクティブな注意ネットワークを用いてタイトルと本文の関連性をモデル化するもので、同様のニュースモデル化手法は後の多くの作品でも用いられている [212,213,215,218,221].
A similar co-attention mechanism is usedby [136] to model the interactions between news title and abstract.
同様の共同注意メカニズムは[136]によってニュースのタイトルとアブストラクトの間の相互作用をモデル化するために使用されています。
FedRec [158] learns news representations fromnews titles via a combination of CNN and multi-head self-attention networks.
FedRec [158]はCNNとマルチヘッド自己アテンション・ネットワークを組み合わせてニュースのタイトルからニュース表現を学習する。
These methods usually learn newsrepresentations based on shallow text models and non-contextualized word embeddings such as GloVe [151],which may be insuicient to capture the deep semantic information in news.
これらの手法は通常、GloVe [151]などの浅いテキストモデルや文脈に基づかない単語埋め込みに基づいてニュース表現を学習するが、ニュースの深い意味情報を捉えるには不十分である可能性がある。
WG4Rec [176] introduces a word-graph based news text modeling method.
WG4Rec [176]は単語グラフに基づいたニューステキストをモデリングする手法を導入している。
It constructs a word graph based on semantic similarity, co-occurrenceand news co-click, and learns word embeddings through a GNN model.
この手法は、意味的類似性、共起性、および、ニュースの共クリックに基づいて単語グラフを構築し、GNNモデルを通じて単語の埋め込みを学習する。
These methods can enhance news textunderstanding with various neural architectures.
これらの手法は、様々なニューラルアーキテクチャを用いて、ニューステキストの理解度を向上させることができる。
However, these models are still rather shallow and may not bestrong enough in capturing the deep semantic information in news texts.
しかし、これらのモデルはまだ浅く、ニューステキストに含まれる深い意味情報を捉えるには十分でない可能性がある。

In recent years, big and powerful pre-trained language models (PLMs) such as BERT [34] have been greatlysuccessful in NLP, and a few recent works explore to empower news modeling with PLMs [81,165,214,222,224,231,240,241].
近年、BERT [34]のような大規模で強力な事前学習済み言語モデル（PLM）がNLPにおいて大きな成功を収めており、最近のいくつかの研究はPLMを用いてニュースモデリングを強化することを模索している [81,165,214,222,224,231,240,241]．
For example, PLM-NR [214] uses diferent PLMs to empower English and multilingual newsrecommendation, and the online light results in Microsoft News showed notable performance improvement.UNBERT [241] incorporates the concatenation of news texts as the input of a BERT model.
例えば、PLM-NR [214]は、英語と多言語のニュースを推薦するために異なるPLMを使用しており、Microsoft Newsにおけるオンラインライトの結果は、顕著な性能向上を示している。
The indings in theseworks imply the efectiveness of large PLMs in empowering text understanding in news recommendation.
UNBERT [241]では、BERTモデルの入力としてニューステキストの連結を組み込んでいる。これらの研究結果は、大規模PLMがニュース推薦におけるテキスト理解を強化する上で有効であることを示唆している。

Instead of merely modeling semantic information in news texts, several methods study to use entities orkeywords in news texts to enhance news modeling by introducing complementary knowledge and commonsenseinformation.
ニューステキスト中の意味情報を単にモデル化するのではなく，ニューステキスト中の実体やキーワードを利用して，補完的な知識や常識的な情報を導入し，ニュースのモデル化を強化する方法がいくつか研究されている．
A direct way is regarding entities as texts and combining them with news text modeling [79].
直接的な方法としては，実体をテキストとして捉え，それをニューステキストのモデリングと組み合わせる方法があります[79]．
Forinstance, Gao et al. [49] proposed a knowledge-aware news recommendation approach with hierarchical attentionnetworks.
例えば，Gaoら[49]は，階層的なアテンションネットワークを用いた知識認識型ニュース推薦手法を提案している．
In their method, a word attention network is used to learn word-based news representations by usingthe embeddings of keywords as attention queries, and these representations are concatenated with both entityembeddings and the average embeddings of the entities in their contexts.
彼らの手法では、単語アテンションネットワークを用いて、キーワードの埋め込みをアテンションクエリとして用いて単語ベースのニュース表現を学習し、これらの表現をエンティティ埋め込みとそのコンテキストにおけるエンティティの平均埋め込みと結合する。
An item attention network is usedto aggregate these three kinds of news representations by modeling their informativeness.
この3種類のニュース表現を集約するために、その情報量をモデル化したitem attention networkが用いられる。
DAN [248] learnsnews representations from news titles and entities via two parallel CNN networks with max pooling operations.Saskr [24] builds news representations from news titles and bodies based on the average word embeddings oftheir entities.
Saskr [24]はニュースのタイトルと本文から、その実体の平均的な単語埋め込みを基にニュース表現を構築する。
DNA [235] learns news representations from the news body, news ID and the elements (entitiesand keywords).
DNA [235]はニュースの本文、ニュースID、要素（エンティティやキーワード）からニュース表現を学習する。
More speciically, the sentences in a news body are transformed into their embeddings viadoc2vec [102], and then are aggregated into a uniied one via a sentence-level candidate-aware attention network.Each news element is represented by averaging the embeddings of its words, and elements representations aresynthesized together via an element-level candidate-aware attention network.
具体的には、ニュース本文の文はviadoc2vec [102]によって埋め込みに変換され、文レベルの候補意識アテンションネットワークによって一つにまとめられる。
The embeddings of the ID, texts,and elements of each piece of news are concatenated together into a uniied news representation.
各ニュースのID、テキスト、要素の埋め込みを連結し、1つのニュース表現とする。
HieRec [160]uses text self-attention and entity self-attention to model the contexts in news titles and the relations betweenentities in news texts, respectively.
HieRec [160]では、ニュースのタイトルに含まれる文脈をテキスト自己注目、テキストに含まれるエンティティ間の関係をエンティティ自己注目でモデル化している。
These methods can easily unify the use of texts and knowledge entities, butthey cannot efectively exploit the relatedness between entities.
これらの方法は，テキストと知識実体の利用を容易に統一することができるが，実体間の関連性を効果的に利用することができない．

Another way to exploit entity information is incorporating knowledge graph embeddings [119,175,185,190,197].
実体の情報を利用するもう一つの方法は、知識グラフ埋め込みを取り入れることである[119,175,185,190,197]。
For example, DKN [197] learns news representations from the titles of news and the entities within titlesvia a knowledge-aware CNN.
例えば、DKN[197]は、知識認識型CNNにより、ニュースのタイトルとタイトル内のエンティティからニュース表現を学習する。
The representations of entities are learned from a knowledge graph using theTransD [77] knowledge graph embedding algorithm.
また、実体の表現はTransD [77]の知識グラフ埋め込みアルゴリズムを用いて知識グラフから学習する。
Liu et al. [119] proposed to construct a news-relevantknowledge graph on the basis of the Microsoft Satori knowledge graph by extracting additional knowledgeentities and topic entities from news and connecting entities in the same news, entities clicked by the same userand entities appearing in the same browsing session to enrich the relations between entities in the knowledgegraph.
Liuら[119]は、Microsoft Satoriの知識グラフをベースに、ニュースから知識エンティティとトピックエンティティを追加抽出し、同じニュース中のエンティティ、同じユーザがクリックしたエンティティ、同じ閲覧セッションに現れたエンティティを連結して、知識グラフ中のエンティティ間の関係を豊かにすることにより、ニュース関連知識グラフを構築することを提案している。
They combine the entity embeddings learned by TransE [9] with the news text embeddings learned byLDA and DSSM.
TransE[9]で学習した実体の埋め込みと、LDAとDSSMで学習したニュースのテキスト埋め込みを組み合わせている。
CAGE [174,175] constructs subgraphs of KG by using one-hop neighbors of entities, and uses theTransE embeddings of entities as complements to text embeddings learned by CNN.
CAGE [174,175]は、実体の1ホップ隣接を用いてKGのサブグラフを構築し、TransEによる実体の埋め込みをCNNによるテキスト埋め込みの補完として利用する。
However, these knowledgegraph embeddings mainly condense low-level interactions between entities.
しかし、これらの知識グラフ埋め込みは、主にエンティティ間の低レベルのインタラクションを凝縮したものである。
To enhance the modeling of richentity relatedness, TEKGR [103] enriches the knowledge graph with topical relations between entities.
リッチネス関係のモデリングを強化するために、TEKGR [103] は知識グラフをエンティティ間のトピカルな関係で強化する。
It predictsthe topic of news based on texts and concepts, and uses the predicted topic to enrich the knowledge graph andlearn topic enriched knowledge representations of news with graph neural networks.
TEKGRはテキストと概念に基づいてニュースのトピックを予測し、予測されたトピックを用いて知識グラフを豊かにし、グラフニューラルネットワークを用いてニュースのトピックに富む知識表現が学習される。
KRED [121] irst learnsentity embeddings from knowledge graph with graph attention networks, then incorporates additional entityfeatures such as frequency, category and position, and inally selects entities according to the texts representationsof news.
KRED [121]は、まずグラフアテンションネットワークを用いて知識グラフからエンベディングを学習し、次に頻度、カテゴリ、位置などのエンティティフィーチャーを追加し、最終的にニュースのテキスト表現に従ってエンティティを選択する。
KIM [156] incorporates a knowledge-aware interactive news modeling method that can model therelations between the entities and their neighbors of clicked news and candidate news through graph co-attentionnetworks.
KIM [156]は，クリックされたニュースや候補となるニュースの実体とその近傍との関係をグラフの共注目ネットワークを通してモデル化する知識認識型の対話的ニュースモデリング手法を導入している．
KOPRA [188] only uses the TransE embeddings of knowledge entities to represent news, and it uses arecurrent graph convolution network to learn hidden entity representations.
KOPRA [188]は知識エンティティのTransE embeddingsのみを用いてニュースを表現し、隠れエンティティ表現を学習するためにarecurrent graph convolution networkを用いている。
These methods can encode richerknowledge information of news than pure text-based methods to empower news recommendation.
これらの方法は，純粋なテキストベースの方法よりも豊富なニュースの知識情報をエンコードすることができ，ニュース推薦を強化することができる．

To better model the characteristics of news articles, several methods explore to incorporate other types of newsinformation beyond texts into news modeling.
ニュース記事の特性をより適切にモデル化するために，テキスト以外のニュース情報をニュースモデリングに取り込む方法がいくつか模索されている．
Among them, topic categories and tags are widely consideredby existing methods [63,149,203,205,237].
その中でも、トピックカテゴリとタグは既存の手法で広く考慮されています[63,149,203,205,237]。
For example, DeepJoNN [237] learns news representations fromnews IDs, categories, keywords and entities via a character-level CNN.
例えば，DeepJoNN [237]は，文字レベルのCNNにより，ニュースID，カテゴリ，キーワード，エンティティからニュース表現を学習する．
Park et al. [149] proposed a neural newsrecommendation method based on LSTM.
Parkら[149]はLSTMに基づくニューラルニュース推薦手法を提案した．
They use a proprietary corpus to train a doc2vec [102] model to encodenews articles into their vector representations, and use an LSTM network to generate user representations from the representations of news.
彼らは独自のコーパスを用いてdoc2vec [102]モデルを学習し、ニュース記事をベクトル表現にエンコードし、LSTMネットワークを用いてニュースの表現からユーザ表現を生成する。
In addition, they incorporate the categories of news into news representations, whichare predicted by a CNN [93] model.
さらに、CNN[93]モデルによって予測されたニュースのカテゴリをニュース表現に組み込んでいる。
TANR [205] learns news representation from news titles via a combinationof CNN and attention network, which is also used in [206,230].
TANR[205]はCNNとアテンションネットワークの組み合わせにより、ニュースタイトルからニュース表現を学習するものであり、[206,230]でも利用されている。
Moreover, TANR incorporates an auxiliary newstopic prediction task to learn topic-aware news representations.
さらに、TANRはトピックを考慮したニュース表現を学習するために、補助的なニューストピック予測タスクを組み込んでいる。
NAML [203] is a news recommendation methodwith attentive multi-view learning, which incorporates diferent kinds of news information as diferent viewsof news.
NAML[203]は，異なる種類のニュース情報を異なる視点として取り込む，注意深いマルチビュー学習によるニュース推薦手法である．
In this method, news titles, bodies, categories and subcategories are processed by diferent models,and their embeddings are further aggregated together into a uniied one via a view-level attention network.
この手法では，ニュースのタイトル，本文，カテゴリ，サブカテゴリをそれぞれ異なるモデルで処理し，さらにそれらの埋め込みをビューレベルのアテンションネットワークで1つに集約する．
Asimilar method is also used by [210,243] to model candidate news.
同様の手法は[210,243]でも候補ニュースのモデル化に用いられている。
LSTUR [2] uses a combination of CNN andattention network to process news titles, and incorporates categories and subcategories by applying a non-lineartransformation to their embeddings.
LSTUR [2]はCNNとアテンションネットワークを組み合わせてニュースのタイトルを処理し、その埋め込みに非線形変換を適用することでカテゴリとサブカテゴリを組み込んでいます。
CHAMELEON [31,46] learns news representations from news bodies byusing CNN with diferent kernel sizes, and these textual representations are fused with news metadata featuressuch as topics, categories and tags using a fully connected layer.
CHAMELEON [31,46]では，カーネルサイズの異なるCNNを用いて，ニュース本文からニュース表現を学習し，これらのテキスト表現を完全連結層を用いてトピック，カテゴリ，タグなどのニュースメタデータの特徴と融合させる．
It also predicts the metadata features of news viaauxiliary tasks.
また，補助タスクによりニュースのメタデータの特徴を予測する．

In addition to topical information, several methods consider other types of content information of news.
トピック情報だけでなく，ニュースの他のコンテンツ情報を考慮する手法もあります。
Forexample, SentiRec [212] considers the sentiment orientation of news to learn sentiment-aware news representa-tions.
例えば、SentiRec [212]は、センチメントを考慮したニュース表現を学習するために、ニュースのセンチメント方向性を考慮します。
It uses the VADER [73] algorithm to compute real-valued sentiment scores of news.
VADER [73]アルゴリズムを使用して、ニュースの実数値のセンチメントスコアを計算する。
MM-Rec [217] uses avisiolinguistic model ViLBERT [128] to learn news multi-modal representations from both news texts and images.IMRec [226] models the rich visual impression information of news such as texts, image regions, the arrangementof diferent ields, and spatial positions of diferent words on the impression.
MM-Rec [217]はアビゾル言語モデルViLBERT [128]を用いて、ニュースのテキストと画像からマルチモーダル表現を学習する。IMRec [226]はテキスト、画像領域、異なる画像の配置、印象上の異なる単語の空間位置などニュースの豊富な視覚的印象情報をモデル化する。
These methods can usually learnmore accurate news representations by characterizing their content in multiple aspects.
これらの手法は、通常、ニュースの内容を複数の側面から特徴付けることで、より正確なニュース表現を学習することができる。

Another major group of additional information is context features, such as popularity and positions.
もう一つの主要な追加情報は、人気度やポジションなどのコンテキスト機能である。
Forexample, PP-Rec [157] uses both news title, entities and news popularity information in news modeling.
たとえば，PP-Rec [157] はニュースのモデリングにおいて，ニュースのタイトル，エンティティ，およびニュースの人気度情報の両方を使用します．
It usesgating mechanisms to synthesize the near-real-time CTR, recency and popularity predicted from news title intoa uniied news popularity score.
PP-Recは，ニュースのタイトルから予測されるほぼリアルタイムのCTR，再来時，および人気度を合成して，単一のニュース人気度スコアにするためにゲーティング・メカニズムを使用しています．
TSHGNN [80] incorporates the active time of users on a news page into themodeling of news texts.
TSHGNN [80]は，ニュースページにおけるユーザの活動時間を，ニューステキストのモデリングに取り入れる．
DCAN [138] uses the time from news publishing and near-real-time CTR to modelthe current positions of news articles in their lifecycles.
DCAN [138]はニュースの出版からの時間とほぼリアルタイムのCTRを利用して，ライフサイクルにおけるニュース記事の現在の位置をモデル化する．
CTX [23] studies the exploitation of CTR, Popularity,and Freshness features.
CTX [23]はCTR，人気度，鮮度の特徴を利用することを研究している．
The results show that these context features may even have a stronger impact thanpersonalized interest signals on click prediction.
その結果，これらのコンテキスト機能は，個人的な興味信号よりもクリック予測に強い影響を与える可能性があることが示された．
DebiasRec [230] uses CNN and attention network to learn newscontent representations from news titles, and learns news bias representations from the size and positions of newsdisplayed on websites with a bias model.
DebiasRec [230]はCNNとアテンションネットワークを用いて，ニュースのタイトルからニュース内容表現を学習し，ウェブサイト上に表示されるニュースのサイズと位置からバイアスモデルを用いてニュースバイアス表現を学習している．
These methods can usually better understand users’ interaction patternswith news by incorporating additional context information.
これらの手法は，通常，追加的な文脈情報を取り入れることで，ユーザのニュースとのインタラクションパターンをよりよく理解することができる．
However, some news features (e.g., near-real-timeCTR) may not be available in some real-world news recommender systems, which hinders the exploitation ofthese features.
しかし，現実のニュース推薦システムにおいて，いくつかのニュース特徴（例えば，ニアリアルタイムCTR）は利用できない場合があり，これらの特徴の活用を妨げている．

There are a few methods that learn news representations from graphs.
グラフからニュース表現を学習する手法はいくつかある．
For example, IGNN [161] usesKCNN [197] to learn text-based news representations from news titles, and learn graph-based news representa-tions from the user-news graph.
例えば，IGNN [161]はKCNN [197]を用いて，ニュースのタイトルからテキストベースのニュース表現を学習し，ユーザ-ニュースグラフからグラフベースのニュース表現を学習する．
GERL [53] learns news title representations with a combination of multi-headself-attention and additive attention networks, and combines title representations with the embeddings of newscategories.
GERL [53]はマルチヘッド自己注意ネットワークと加算的注意ネットワークを組み合わせてニュースタイトル表現を学習し、タイトル表現とニュースカテゴリのエンベッディングを組み合わせる。
MVL [170] uses a content view to incorporate news title, body and category, and uses a graph view toenhance news representations with their neighbors on the user-news graph.
MVL [170]では，ニュースのタイトル，本文，カテゴリをコンテンツビューで学習し，ユーザ-ニュースグラフ上の隣接するニュース表現とグラフビューで学習することで，ニュース表現を強化する．
In addition, it uses a graph attentionnetwork to enhance representations of news by incorporating the information of their irst- and second-orderneighbors on the user-news graph.
さらに，グラフアテンションネットワークを用いて，ユーザ・ニュースグラフ上の一次および二次の隣人の情報を取り込み，ニュースの表現力を高める．
GNUD [71] uses the same news encoder as DAN to learn text-based newsrepresentations, and uses a graph convolution network (GCN) with a preference disentanglement regularizationto learn disentangled news representations on user-news graphs.
GNUD [71]は，DANと同じニュースエンコーダを用いてテキストベースのニュース表現を学習し，グラフ畳み込みネットワーク（GCN）と選好異種正則化を用いて，ユーザニューズグラフ上の異種ニュース表現を学習する．
In addition to the user-news graphs used by theabove methods, a few methods incorporate heterogeneous graphs that condense richer collaborative informa-tion [70,133,167].
上記の手法で用いられるユーザニュースグラフに加えて、より豊富な協調情報を凝縮した異種グラフを取り入れる手法もある[70,133,167]。
For example, GNewsRec [70] is a hybrid approach which considers graph information of usersand news as well as news topic categories.
例えば，GNewsRec [70]はユーザとニュースのグラフ情報だけでなく，ニュースのトピックカテゴリも考慮したハイブリッドなアプローチである．
It also uses the same architecture with DAN to learn text-based news representations, and uses a two-layer graph neural network (GNN) to learn graph-based news representationsfrom a heterogeneous user-news-topic graph.
また，DANと同じアーキテクチャを用いてテキストベースのニュース表現を学習し，2層のグラフニューラルネットワーク（GNN）を用いて異種ユーザ-ニュース-トピックグラフからグラフベースのニュース表現を学習する．
These methods can exploit the high-order information on graphsto enhance news modeling.
これらの手法は、グラフの高次情報を利用し、ニュースのモデル化を強化することができる。
However, it is diicult for these methods to handle newly generated news with fewconnections to existing nodes on the old graph used for training.
しかし、これらの手法では、学習に用いた古いグラフ上の既存のノードとの接続が少ない新しく生成されたニュースを扱うことは困難である。

To help better understand the relatedness and diferences between the methods reviewed above, we summarizethe information and models they used for learning news representations in Table 3.
これらの手法の関連性と差異を理解するために，表 3 にニュース表 現の学習に使用した情報とモデルをまとめる．
Next, we provide severaldiscussions on the aforementioned methods for news modeling.
次に，前述したニュースモデル化手法に関するいくつかの考察を行う．

## 3.3. 3.3 Discussions on News Modeling 3.3. 3.3 ニュースモデリングに関する考察

### 3.3.1. 3.3.1 Feature-based News Modeling. 3.3.1. 3.3.1 特徴に基づくニュースモデリング。

In feature-based news modeling methods, mining textual information ofnews is critical for representing news content.
特徴量に基づくニュースモデリング手法では、ニュースのテキスト情報をマイニングすることが、ニュース内容を表現するために重要である。
Many methods incorporate BOW
多くの手法では、BOW

Besides the texts of news, many methods utilize other information of news.
ニュースのテキスト以外に、多くの手法はニュースの他の情報を利用している。
For instance, the categories orclusters of news are popular news features to help model news content.
例えば，ニュースのカテゴリやクラスタは，ニュースの内容をモデル化するのに役立つ人気のあるニュースの特徴である．
In addition, several dynamic features ofnews are also widely employed in feature-based news modeling methods, such as popularity and recency.
さらに，ニュースの動的な特徴である人気度や再来時なども，特徴ベースのニュースモデリング手法に広く採用されています．
Sincemany users may pay more attention to popular events and news usually vanish quickly, incorporating newspopularity and recency can help build more informative news representations.
多くのユーザは人気のあるイベントにより多くの注意を払い、ニュースは通常すぐに消えてしまうため、ニュースの人気度や再現性を取り入れることで、より情報量の多いニュース表現を構築することができます。
Besides, several environmentalfactors, such as locations and time are also utilized by several methods.
また，場所や時間などの環境要因も，いくつかの手法で利用されている．
This is because considering locations ofnews can provide news related to users’ neighbors, and using the timestamps of news may be useful for providingtime-aware news services.
また，ニュースのタイムスタンプを利用することで，時間を考慮したニュースサービスを提供することができる．

A few methods also study incorporating other interesting features.
また、いくつかの手法では、他の興味深い特徴を取り入れることも研究されている。
For example, the sentiment information ofnews is useful for news understanding, because users may have diferent tastes on the sentiment of news.
例えば、ニュースのセンチメント情報は、ニュースの理解に役立ちます。
Thebias of news may also need to be taken into consideration, because recommending news with biased opinions andfacts may hurt user experience and the reputation of news platforms.
また、偏った意見や事実を含むニュースを推薦すると、ユーザー体験やニュースプラットフォームの評判を損なう可能性があるため、ニュースの偏りを考慮する必要がある。
Finally, although several non-personalizednews recommendation methods have used news images to build news representations [127], few personalizedones consider the visual information of news, which is very useful for news modeling.
最後に，いくつかの非個人化ニュース推薦手法は，ニュース画像を用いてニュース表現を構築していますが [127]，ニュースのモデリングに非常に有用なニュースの視覚情報を考慮した個人化手法はほとんどありません．

Although feature-based news modeling methods have comprehensive coverage of various news information,they usually require a large amount of domain knowledge for feature design.
特徴量ベースのニュースモデリング手法は，様々なニュース情報を包括的にカバーしているが，通常，特徴量設計のために大量のドメイン知識が必要となる．
In addition, handcrafted featuresare usually not optimal in representing the textual content of news due to the absence of the contexts and ordersof words.
また，手作業で作成された特徴量は，文脈や語順が分からないため，ニュースのテキスト内容を表現するのに最適なものではありません．

Table 3.
表3.
Comparison of different methods on news modeling.
ニュースのモデル化に関する様々な手法の比較。

### 3.3.2. 3.3.2 Deep Learning-based News Modeling. 3.3.2. 3.3.2 ディープラーニングを用いたニュースのモデリング。

Among all the reviewed methods, only two methods, i.e., DNA [235]and DeepJoNN [237], directly incorporate the embeddings of news IDs.
しかし，DNA [235]とDeepJoNN [237]の2つの手法だけが，ニュースIDの埋め込みを直接的に取り入れている．
This is probably because of the shortlifecycle of news articles and the quick generation of novel news, which make the coverage of news IDs in thetraining set very limited.
これは、ニュース記事のライフサイクルが短く、新しいニュースの生成が早いため、学習セットに含まれるニュースIDの範囲が非常に限られているためと思われます。
Thus, it is very important to understand news from their content.
このように、ニュースを内容から理解することは非常に重要である。

News text modeling is critical for news understanding.
ニューステキストをモデリングすることは，ニュースを理解する上で非常に重要である．
Most methods use news titles to model news sincenews titles, because news titles usually have decisive inluence on users’ click behaviors.
これは，ニュースのタイトルは通常，ユーザのクリック行動に決定的な影響を与えるためです．
Several methods such asEBNR [144], NAML [203] and CPRS [213] use news bodies to enhance news representations, since news bodiesare contain more detailed information of news.
EBNR [144]、NAML [203]、CPRS [213]などのいくつかの手法は、ニュースの本文がより詳細な情報を含んでいるため、ニュース表現を強化するために本文を使用しています。
In existing methods, CNN is the most frequently used architecturefor text modeling.
既存の手法では，CNNがテキストモデリングに最も頻繁に使用されるアーキテクチャである．
This is because local contexts in news articles are important for modeling news content, and CNN is efective and eicient in capturing local contexts.
これは，ニュース記事中の局所的な文脈がニュース内容のモデル化に重要であり，CNNが局所的な文脈を捉えるのに有効かつ効率的であるためである．
In addition, since diferent news informationmay have diferent informativeness in modeling news content and user interest, attention mechanisms are alsowidely used to build news representations by selecting important features.
また、ニュースの内容やユーザの興味をモデル化する上で、異なるニュース情報は異なる情報性を持つ可能性があるため、重要な特徴を選択することでニュース表現を構築するアテンションメカニズムも広く用いられている。
With the success of Transformerin NLP, many methods also use Transformer-like architectures for news modeling, such as NRMS [207] andCPRS [213].
NLPにおけるTransformerの成功により、NRMS [207]やCPRS [213]などの多くの手法もニュースのモデリングにTransformerに似たアーキテクチャを使用しています。
In addition, a few methods use pre-trained language or and visiolinguistic models to empower newsmodeling [214,217].
さらに、いくつかの手法では、事前に学習させた言語モデルや視覚言語モデルを使用して、ニュースモデリングを強化しています[214,217]。
These advanced NLP techniques can greatly improve news content understanding, whichis very important for personalized news recommendation.
これらの高度なNLP技術は，ニュースの内容理解を大幅に向上させることができ，これはパーソナライズされたニュース推薦に非常に重要である．
However, these methods mainly aim to capture thesemantic information of news and may not be aware of the knowledge and commonsense information encodedin news.
しかし，これらの手法は主にニュースの意味情報を捕らえることを目的としており，ニュースにエンコードされた知識や常識的な情報には気づいていない可能性がある．

To address this issue, many methods incorporate news entities into news modeling to learn knowledge-awarenews representations [120].
この問題に対処するため，多くの手法がニュースの実体をニュースモデリングに組み込んで，知識連想ニュース表現を学習している[120]．
Some methods such as DAN [248] directly use entity texts to represent entities,while several other methods like DKN [197] use knowledge graph embeddings to represent entities.
DAN [248]のように実体を表現するために実体のテキストを直接利用する手法もあれば、DKN [197]のように実体の表現に知識グラフ埋め込みを利用する手法もある。
These entityrepresentations are usually combined with representations learned from news texts to better model news content.However, there are many new entities and concepts emerging in news and it may be diicult to accuratelyrepresent them with of-the-shelf knowledge bases.
しかし、ニュースには多くの新しい実体や概念が出現しており、既成の知識ベースではそれらを正確に表現することは困難である。

Several methods incorporate the topic categories of news into news modeling, because news topics are veryuseful for understanding news content and inferring user interest.
ニュースのトピックは，ニュースの内容を理解し，ユーザの興味を推測するのに非常に有用であるため，いくつかの手法はニュースのモデリングにニュースのトピックカテゴリを組み込んでいる．
Considering the scenarios that some newsarticles are not labeled with topic categories, some methods such as TANR [205] and CHAMELEON [46] alsoadopt auxiliary tasks by predicting news topic categories to encode topic information into news representations.In addition, a few methods study using other kinds of news features such as sentiment [212], popularity [23],recency [157], which can help better understand the characteristics of news.
さらに，Sentent[212]，Popular[23]，Recency[157]などの他の種類のニュース特徴を用いる研究も行われており，ニュースの特徴をよりよく理解するのに役立っている．
However, some additional newsfeatures (e.g., category and CTR) may be unavailable in certain scenarios, which limits the application of thesemethods.
しかし，いくつかの追加的なニュース特徴（例えば，カテゴリやCTR）は特定のシナリオで利用できない場合があり，これらの手法の適用を制限している．

There are also a few methods that explore to enhance news modeling with graph information [53,70].These methods can incorporate the high-order information on user-news bipartite graphs [53,71,161,170] ormore complicated heterogeneous graphs [70,167], which can provide useful contexts on understanding thecharacteristics of news for news recommendation.
これらの手法は，ユーザとニュースの二部グラフ[53,71,161,170]やより複雑な異種グラフ[70,167]の高次情報を取り込み，ニュースの特性を理解する上で，ニュース推薦に有用なコンテキストを提供することができる。
However, since the graphs used in these methods are static,they may have some diiculties in accurately representing newly published news.
しかし，これらの手法で用いられるグラフは静的であるため，新しく発表されたニュースを正確に表現することに困難が伴う可能性がある．

In summary, by reviewing news modeling techniques used in existing news recommendation methods, we cansee that news modeling is still a quite challenging problem in news recommendation due to the variety, dynamic,and timeliness of online news information.
以上のように、既存のニュース推薦手法で用いられているニュースモデリング技術を概観すると、オンラインニュース情報の多様性、動的性、適時性から、ニュースモデリングはニュース推薦において依然として非常に困難な問題であることがわかる。

# 4. 4 USER MODELING 4. 4 ユーザーモデリング

<img src="https://d3i71xaburhd42.cloudfront.net/a867894db8f9d544a471e86d8844008861f6a2ec/17-Figure4-1.png">

Fig. 4.
図4.
An example framework of user modeling.
ユーザーモデリングのフレームワークの一例

User modeling is also a critical step in personalized news recommender systems to infer users’ personal interestsin news.
また，個人化されたニュース推薦システムにおいて，ユーザモデリングは，ユーザのニュースに対する個人的な興味を推測するために重要なステップである．
It is usually important for user modeling algorithms to understand users from their behaviors [205].
ユーザーモデリングアルゴリズムでは、通常、ユーザーの行動からユーザーを理解することが重要である[205]。
Anexample user modeling framework in personalized news recommendation is shown in Fig. 4.
図4は、個人向けニュース推薦におけるユーザモデリングのフレームワークの一例である。
We can see thatuser modeling is based on the modeling of news that users have interactions with, and it introduces additionaluser features to achieve better personalized user understanding.
ユーザモデリングは，ユーザが接触したニュースのモデリングに基づいており，よりパーソナライズされたユーザ理解を達成するために，追加のユーザ特徴を導入していることが分かる。
The techniques for user modeling in existingnews recommendation methods can also be classiied into feature-based ones and deep learning-based ones.Feature-based user modeling techniques mainly rely on manually designed user modeling rules or heuristicpatterns to represent user interest.
既存のニュース推薦手法におけるユーザーモデリングの技術は、特徴ベースのものと深層学習ベースのものに分類することもできます。特徴ベースのユーザーモデリング技術は、主にユーザーの関心を表すために、手動で設計したユーザーモデリング規則またはヒューリスティックパターンに依存しています。
By contrast, deep learning-based methods usually focus on automaticallyinding useful patterns from user behaviors to infer user interest.
これに対して、深層学習ベースの手法は、通常、ユーザーの関心事を推論するために、ユーザーの行動から有用なパターンを自動的に見つけ出すことに重点を置いています。
The details of the two kinds of user modelingmethods are introduced in the following sections.
この 2 種類のユーザーモデリング手法の詳細については，以下のセクションで紹介する．

## 4.1. 4.1 Feature-based User Modeling 4.1. 4.1 特徴に基づくユーザモデリング

Feature-based user modeling methods use handcrafted features to represent users.
特徴量ベースのユーザモデリング手法では，ユーザを表現するために手作りの特徴量を使用します．
Similar to news modeling, inCF-based methods users are also represented by their IDs [29, 168].
ニュースモデリングと同様に，CFベースの手法でもユーザはIDによって表現される[29, 168]．
However, ID-based user modeling methodsusually sufer from the data sparsity.
しかし，IDベースのユーザモデリング手法は，通常，データの希少性に悩まされます．
Thus, most methods consider the behaviors of users such as news clicks tomodel their interest.
そこで，多くの手法では，ニュースのクリック数などユーザの行動を考慮し，ユーザの興味をモデル化する．
An intuitive way is to use the features of clicked news to build user features.
直感的な方法は，クリックされたニュースの特徴量を用いてユーザ特徴量を構築することである．
For example,Goossen et al. [58] used the CF-IDF features of clicked news to represent user interest.
例えば，Goossen ら [58] はクリックされたニュースの CF-IDF 特性を用いてユーザの興味関心を表現している．
Capelle et al. [16] proposedto use the SF-IDF features of clicked news for user modeling.
Capelleら[16]はクリックされたニュースのSF-IDF特徴をユーザモデリングに利用することを提案している．
Garcin et al. [52] proposed to model users byaggregating the LDA features of all clicked news into a user vector by averaging.
Garcinら[52]は，クリックされたすべてのニュースのLDA素性を平均化してユーザベクトルに集約し，ユーザをモデル化することを提案している．
However, it is diicult for thesemethods to model users accurately when their news click behaviors are sparse.
しかし，これらの手法では，ニュースのクリック行動がまばらな場合に，ユーザを正確にモデル化することが困難である．

Besides news features, many methods consider other supplementary information of users in user modeling.For instance, in the MONERS [104] recommender system, users are clustered into segments, and the preferencesof user segments on news categories and news articles are used to represent users.
例えば，MONERS [104] 推薦システムでは，ユーザをセグメントに分類し，ニュースカテゴリとニュース記事に関するユーザセグメントの嗜好をユーザ表現に用いている．
In addition, the demographicsof users, such as age, gender and profession, are also useful information for user modeling because users indiferent demographic groups usually have diferent preferences on news.
また，年齢，性別，職業などのユーザの属性も，ユーザモデリングに有用な情報である．なぜなら，異なる属性グループに属するユーザは，通常，ニュースに対する嗜好が異なるからである．
Thus, user demographic features areincorporated by several methods [75, 104, 229].
このように，ユーザの人口統計学的特徴は，いくつかの 方法によって組み込まれている[75, 104, 229]．
For instance, Yeung et al. [229] proposed to use the age, gender,occupation status and social economic grade of users to help identify their diferent preferences on news indiferent categories.
たとえば，Yeung ら [229] は，ユーザの年齢，性 別，職業，社会的経済的等級を利用して，異なるカテゴ リーのニュースに対するユーザの異なる嗜好を識別すること を提案しています．
Chu et al. [25] used the age and gender categories of users to model their characteristics.Besides, the location information of users is also very useful for accurate user modeling, and it has been usedby several location-aware news recommendation methods [43,143].
さらに，ユーザの位置情報も正確なユーザモデリン グに非常に有効であり，いくつかの位置情報対応ニュース推薦 手法で利用されている[43,143]．
However, some kinds of user features suchas locations and demographics are privacy-sensitive, and many users may not provide their accurate personalinformation.
しかし，位置情報や属性情報などのユーザの特徴は，プライバシに敏感であり，多くのユーザが正確な個人情報を提供しない可能性がある．

Since news clicks may not necessarily indicate user interests, several methods also consider other kinds of userbehaviors or feedback.
また，ニュースのクリック数は必ずしもユーザの興味 を示しているとは限らないため，他の種類のユーザ行動やフィー ドバックを考慮する手法もある．
For example, Gershman et al. [55] proposed to represent users by the news they carefullyread (regarded as positive news), rejected, and scrolled (both are regarded as negative news).
たとえば，Gershman ら [55] は，注意深く読んだニュース（ポジ ティブニュース），拒否したニュース，スクロールしたニュース （いずれもネガティブニュース）により，ユーザを表現することを 提案している．
In addition, users’dwell time on clicked news is also an important indication of user interest, and Yi et al. [232] studied to use dwelltime as the weights of clicked news for user modeling.
また，クリックされたニュースの滞在時間もユーザの興味を示す重要な指標であり，Yi ら [232] は，クリックされたニュースの重みとして滞在時間を用いることを研究している．
Besides these user behaviors, several other kinds of user behavior information such as access patterns, are utilized by a few methods [109,171] to capture the users’ habitson news reading.
これらのユーザ行動のほかに，アクセスパターンなど他の種類のユーザ行動情報も，ユーザのニュース閲覧の習慣を把握するために，いくつかの手法で利用されている [109,171]．

Several methods also consider graph information (e.g., news-user graphs) in user modeling [56].
また，ユーザモデリングにおいて，グラフ情報（例 えば，ニュースユーザグラフ）を考慮する手法もある [56]．
For example, Liet al. [108] proposed a news personalization method by using hypergraph to model various high-order interactionsbetween diferent news information, where users are represented by subgraphs of the hypergraph.
例えば，Liet ら [108] は，ユーザを超グラフの部分グラフで表現し，異なるニュース情報間のさまざまな高次相互作用を超グラフでモデル化することによって，ニュースのパーソナライズ手法を提案している．
Garcin etal.
Garcin et al.
[50] proposed to use context trees for user modeling.
[50]は，ユーザモデリングに文脈木を用いることを提案した．
They constructed context trees based on the sequence ofarticles, the sequence of topics and the distribution of topics.
彼らは，記事の順序，トピックの順序，トピックの分布に基づいてコンテクストツリーを構築した．
Trevisiol et al. [192] proposed to build a browsinggraph from the news browsing histories of users on Yahoo News.
Trevisiolら[192]はYahoo Newsにおけるユーザのニュース閲覧履歴からブラウジンググラフを構築することを提案した。
Joseph et al. [84] proposed to represent usersby regarding the clicked news as subgraphs of a knowledge graph, which are constructed via entity linking.These methods can consider the high-order information on graphs to help understand user behaviors, which canimprove user modeling.
Josephら[84]は、クリックされたニュースを知識グラフの部分グラフとして捉え、エンティティリンクによって構築することでユーザを表現することを提案した。これらの手法は、グラフ上の高次情報を考慮してユーザの行動を理解し、ユーザのモデリングを向上させることができる。

A few methods combine user IDs with other user features in user modeling [125].
ユーザモデリングにおいて，ユーザIDを他のユーザ特徴量と組み合わせる手法もいくつかある[125]．
For example, NewsWeeder [99]used user IDs and the bag-of-words features of clicked news to represent users.
例えば，NewsWeeder [99]では，ユーザIDとクリックされたニュースのbag-of-words特徴量を用いてユーザを表現している．
Claypool et al. [26] used user IDsand keywords of clicked news for user modeling Liu et al. [122] proposed to represent users using their IDs anduser interest features predicted by a Bayesian model.
Claypoolら[26]は，ユーザIDとクリックされたニュースのキーワードを用いてユーザをモデル化している Liuら[122]は，ユーザIDとベイズモデルによって予測されるユーザの興味・関心特徴を使ってユーザを表現することを提案している．
These methods can mitigate the drawbacks of ID-baseduser modeling and meanwhile incorporate useful personal information encoded by user IDs.
これらの方法は，IDベースのユーザモデリングの欠点を軽減し，一方でユーザIDによってエンコードされる有用な個人情報を取り込むことができる．

Considering the evolutionary characteristics of user interest, some methods model both long-term and short-term user interests [15,112].
ユーザの興味の進化的特性を考慮し，長期的・短期的な ユーザの興味をモデル化する手法もある [15,112] ．
NewsDude [7] may be one of the earliest methods that consider long short-termuser interests.
NewsDude [7]は長期的・短期的なユーザの興味を考慮した初期の手法の一つであろう．
In this approach, users are represented by a hybrid model, which models short-term interest ofusers based on recently browsed news, and models long-term user interest by sorting words of news in eachcategory with respect to their TF-IDF values and selecting the top ranked words.
この手法では，ユーザは最近閲覧したニュースに基づいてユーザの短期的な関心をモデル化し，各カテゴリのニュースの単語をTF-IDF値に関してソートし，上位の単語を選択することによって長期的なユーザの関心をモデル化するハイブリッドモデルで表現される．
Li et al. [111] proposed LOGO,which is a news recommendation method that models both long-term and short-term user interests.
Liら[111]は，長期的なユーザの関心と短期的なユーザの関心の両方をモデル化するニュース推薦手法であるLOGOを提案した．
LOGO usesa weighted summation of the topic distributions of news clicked by users to indicate long-term user interest, andit uses the topic distribution of the latest clicked news as the short-term user interest.
LOGOは，ユーザがクリックしたニュースのトピック分布の重み付き合計を長期的なユーザの興味として用い，クリックされた最新のニュースのトピック分布を短期的なユーザの興味として用いている．
Viana et al. [193] proposedanother news recommendation method based on long short-term user interest.
Vianaら[193]は，長期的・短期的なユーザの関心に基づくニュース推薦手法をもう一つ提案している．
In their method, the long-terminterest of users is represented by the frequency of a speciic tag being read by this user, and short-term interestis represented by several recently clicked news.
彼らの方法では，ユーザの長期的な興味はそのユーザが特定のタグを読む頻度によって表され，短期的な興味は最近クリックされたいくつかのニュースによって表される．
Diferent from other methods that only consider short-termor long-term user interests, these methods can better model the evolution of user interests by capturing longshort-term user interests.
本手法は，短期的・長期的なユーザの興味のみを考慮する他の手法とは異なり，長期・短期的なユーザの興味を捉えることで，ユーザの興味の進化をより適切にモデル化することができる．

To help readers better understand feature-based user modeling methods in personalized news recommendersystems, we summarize the additional user features (ID and news features are excluded) used in these methods in Table 4.
個人化ニュース推薦システムにおける特徴量ベースのユーザモデリング手法の理解を助けるために、これらの手法で使用される追加的なユーザ特徴量（IDおよびニュース特徴量は除く）を表4にまとめた。

## 4.2. 4.2 Deep Learning-based User Modeling 4.2. 4.2 ディープラーニングに基づくユーザーモデリング

<img src="https://d3i71xaburhd42.cloudfront.net/a867894db8f9d544a471e86d8844008861f6a2ec/19-Table4-1.png">

Table 4.
表4.
Additional features used for user representation.
ユーザー表現に使用する追加特徴量
\*ID
\*ID

In recent years, many personalized news recommendation methods use deep learning techniques for usermodeling to remove the need of manual feature engineering.
近年，多くのパーソナライズドニュースレコメンデーション手法では，ユーザモデリングに深層学習技術を用いることで，人手による特徴抽出の必要性をなくしている．
Most existing methods infer user interests fromhistorical news click behaviors.
既存の手法の多くは，過去のニュースのクリック行動からユーザの興味を推論する．
Several methods focus on aggregating the representations of historical clickednews [63].
いくつかの方法は，過去のクリックされたニュースの表現を集約することに焦点を当てている[63]．
For example, Khattar et al. [97] used the summation of clicked news representations weighted by anexponential discounting function, where more recent clicks gain higher weights.
例えば，Khattar ら [97] はクリックされたニュースの表現を指数割引関数で重み付けした和を用い，最近のクリックほど高い重みを得ている．
NAML [203] and KRED [121]learn user representations from the representations of clicked news using a news-level attention network, andAMM [240] also uses attention network to aggregate diferent information of clicked news and candidate news foruser modeling.
NAML [203]とKRED [121]はニュースレベルのアテンションネットワークを用いてクリックされたニュースの表現からユーザ表現を学習し、AMM [240]もアテンションネットワークを用いてクリックされたニュースと候補ニュースの異なる情報を集約してユーザモデリングを行う。
DKN [197] learns user representations from the representations of clicked news via a candidate-aware attention network, i.e., computing the attention weight of each clicked news according to its relevance tocandidate news.
DKN [197]は候補意識型アテンションネットワークを用いてクリックされたニュースの表現からユーザ表現を学習する。すなわち、候補ニュースとの関連性に応じてクリックされた各ニュースのアテンションウェイトを計算する。
The candidate-aware attention mechanism is also used by TEKGR [103] for user modeling.
また，TEKGR [103]では，この候補考慮型アテンション機構をユーザモデリングに用いている．
Liuet al. [119] use a simple time-decayed averaging of the embeddings of clicked news to build the user embedding.MM-Rec [217] uses a crossmodal candidate-aware attention network that selects clicked news based on theircrossmodal relatedness with candidate news for user modeling.
MM-Rec [217]はクロスモーダルな候補認識ネットワークを用いて、クリックされたニュースの候補ニュースとのクロスモーダルな関連性に基づいてクリックされたニュースを選択し、ユーザモデリングに用いている。
HieRec [160] uses a hierarchical user interestrepresentation method that irst models subtopic-level user interest from the news within the same subtopic, thenaggregates subtopic-level interest representations into coarse-grained topic-level user interest representations,and inally synthesizes topic-level interest representations into an over interest representation.
HieRec [160]は階層的ユーザインタレスト表現法を用いており，まず同じサブトピック内のニュースからサブトピックレベルのユーザインタレストをモデル化し，次にサブトピックレベルのインタレスト表現を粗粒度のトピックレベルのユーザインタレストに集約し，最後にトピックレベルのインタレスト表現を合成してオーバーインタレスト表現としている．
DebiasRec [230]uses a bias-aware user modeling module to learn debiased user interest representations by incorporating theinluence of presentation bias information on click behaviors into attentive behavior aggregation.
DebiasRec [230]は，バイアスを考慮したユーザモデリングモジュールを用いて，クリック行動に対するプレゼンテーションのバイアス情報の影響を注意深い行動集計に取り入れることにより，バイアスされたユーザインタレスト表現を学習している．
These methodscan select important click behaviors for user modeling.
これらの手法は，ユーザモデリングのために重要なクリック行動を選択することができる．
However, the relations among diferent clicked news,which provide rich contexts of behaviors that are useful to user modeling, cannot be modeled by these methods.
しかし，ユーザモデリングに有用な行動の豊富なコンテキストを提供する様々なクリックされたニュース間の関係は，これらの方法ではモデル化することができない．

Therefore, many methods consider the contexts of news click behaviors.
そのため，ニュースのクリック行動のコンテキストを考慮した手法が多く存在する．
Recurrent neural network (RNN)is a popular choice to model the sequential dependency between diferent clicked news [96,144,165,248].
RNN（リカレントニューラルネットワーク）は、クリックされた異なるニュースの間の逐次依存性をモデル化するための一般的な選択肢である[96,144,165,248]。
Forexample, EBNR [144] learns representations of users from the representations of their browsed news via a GRUnetwork.
例えば，EBNR [144] は GRU network を介して，閲覧したニュースの表現からユーザの表現を学習しています．
RA-DSSM [96] uses a bi-directional long short-term memory (Bi-LSTM) network to process the historicalnews click sequence, and then use a news-level attention network to form a user representation.
RA-DSSM [96]は双方向長期短期記憶（Bi-LSTM）ネットワークを用いて過去のニュースのクリック列を処理し、ニュースレベルのアテンションネットワークを用いてユーザー表現を形成するものである。
DAN [248] learnsuser representations from clicked news using a combination of attentive LSTM and candidate-aware attention,which generate user historical sequential embedding and user interest embedding, respectively.
DAN [248]は、アテンションLSTMと候補アテンションを組み合わせて、クリックされたニュースからユーザ表現を学習し、それぞれユーザ履歴順次埋め込みとユーザ興味埋め込みを生成している。
The advantage ofRNN-based user models is their strong ability in modeling user interest dynamics.
RNNベースのユーザモデルの利点は，ユーザの興味・関心のダイナミクスをモデル化する能力が高いことである．
However, they are somewhatweak in capturing the global interest information of users.
しかし、ユーザのグローバルな興味情報を捉えることにはやや弱い。
In addition, as pointed by [216], news recommendationmay not be suitable to be modeled as a conventional sequential recommendation problem because users have astrong preference on the diversity between past and future clicked news.
また，[216]が指摘するように，ニュース推薦では，ユーザは過去と未来のクリックニュースの多様性に強い選好性を持つため，従来の逐次推薦問題としてモデル化することは適切でない可能性がある．

Many other common deep models, such as CNN [239], self-attention [207] and co-attention [138], havealso been applied in user modeling.
また，CNN [239]，自己アテンション [207]，共同アテンション [138] などの一般的な深層モデルもユーザモデリングに適用されている．
For example, WE3CN [90] learns representations of users from the 3Drepresentation tensors of their clicked news using a 3D CNN model.
例えば、WE3CN [90]は3D CNNモデルを用いて、クリックされたニュースの3D表現テンソルからユーザの表現を学習する。
SFI [138] further introduces a hard selectionmechanism to reduce the computational cost in 3D CNN-based user modeling.
また，SFI[138]は3次元CNNを用いたユーザモデリングにおいて，計算コストを削減するためにハードセレクションメカニズムを導入している．
NRMS [207] learns contextual newsrepresentations by using a news-level multi-head self-attention network, and uses an additive attention networkto form the user representation.
NRMS [207]はニュースレベルの多頭自己注意ネットワークを用いて文脈に応じたニュース表現を学習し，付加的注意ネットワークを用いてユーザ表現を形成する．
This method is also adopted by many methods like FairRec [221], IMRec [226] andSentiRec [212], and the variant that uses łCLS” token representation of Transformer is used by [241].
この手法は、FairRec [221], IMRec [226], SentiRec [212]など多くの手法で採用されており、TransformerのłCLSトークン表現を用いた変種は[241]で採用されている。
FIM [196]uses a ine-grained interest modeling method that can capture the word-level relatedness between news witha 3D CNN model.
FIM [196]では、3次元CNNモデルを用いて、ニュース間の単語レベルの関連性を捉えることができる、粒度の細かいインタレストモデリング手法を採用している。
UniRec [218] learns the user embedding for news ranking with the NRMS [207] model, andthen uses this embedding as the attention query to select a set of basis interest embeddings to aggregate theminto a user embedding for news recall.
UniRec [218]は，NRMS [207]モデルを用いてニュースランキングのためのユーザ埋め込みを学習し，この埋め込みを注目クエリとして，基底の興味埋め込みの集合を選択し，それらをニュース想起用のユーザ埋め込みに集約している．
KIM [156] uses a user-news co-encoder that models the interactionsbetween candidate news and clicked news to collaboratively learn a candidate-aware user interest representationand a user-aware candidate news representation.
KIM [156]は、候補ニュースとクリックされたニュースの相互作用をモデル化したユーザ・ニュース協調エンコーダを用いて、候補を考慮したユーザインタレスト表現とユーザを考慮した候補ニュース表現を協調的に学習する。
PP-Rec [157] uses a popularity-aware user modeling method that irst uses self-attention to model the contexts of user behaviors and then uses a content-popularity jointattention network that selects clicked news according to their content and popularity for user interest modeling.RMBERT [81] uses a reasoning memory network [45] to capture the sophisticated interactions between userbehaviors and candidate news in user interest modeling.
RMBERT [81]は推論記憶ネットワーク[45]を用いて、ユーザの行動と候補ニュースの間の高度な相互作用を捉え、ユーザインタレスト・モデリングを行うものである。
These methods can efectively capture the relations ofdiferent user behaviors to enhance user modeling.
これらの手法は，ユーザモデリングを強化するために，異なるユーザ行動の関係を効果的に捕らえることができる．

In recent years, graph neural networks have also been applied to model the contexts of user behaviors bycapturing their high-order relations [136].
近年、グラフ・ニューラル・ネットワークは、ユーザ行動の高次の関係性を捉えることで、ユーザ行動のコンテクストをモデル化することにも応用されています[136]。
For example, CAGE [175] irst uses a GCN model to capture therelations between diferent behaviors within a news session to reine the behavior representations, and thenuses a GRU network to build user representations.
例えば、CAGE[175]では、まずGCNモデルを用いてニュースセッション内の異なる行動間の関係を捉え、行動表現を定義し、次にGRUネットワークを用いてユーザ表現を構築しています。
User-as-Graph [210] is probably the irst work in newsrecommendation that represents each user with a personalized heterogeneous graph constructed from clickbehaviors, where the user modeling task is modeled as a graph pooling problem.
User-as-Graph [210]はおそらく、クリック行動から構築されたパーソナライズされた異種グラフで各ユーザーを表現するニュース推薦の最初の仕事であり、ユーザーモデリングタスクはグラフプーリング問題としてモデル化されている。
It uses a heterogeneous graphpooling method named HG-Pool to iteratively summarize the personalized heterogeneous graph for learning userinterest representations.
また、HG-Poolと呼ばれる異種グラフプーリング法を用いて、ユーザの興味表現を学習するために、パーソナライズされた異種グラフを繰り返し要約する。
EEG [243] models each user as an entity graph.
EEG [243]は、各ユーザをエンティティグラフとしてモデル化する。
It irst uses a graph neural network tolearn hidden entity representations, and then uses an attention network to aggregate them into an entity-baseduser representation.
EEGでは，まずグラフニューラルネットワークを用いて隠れた実体表現を学習し，次にアテンションネットワークを用いてそれらを集約し，実体ベースのユーザ表現にする．
KOPRA [188] also models users as entity graphs and uses recurrent graph convolution toprocess the entity graphs.
KOPRA [188]もユーザをエンティティグラフとしてモデル化し、リカレントグラフコンボリューションを用いてエンティティグラフを処理する。
It models both long-term and short-term user interests with the entire graph and thesubgraph inferred from recently clicked news, respectively.
KOPRAは長期的なユーザインタレストと短期的なユーザインタレストをそれぞれグラフ全体と最近クリックされたニュースから推測される部分グラフでモデル化する．
In addition, it introduces an entity neighbor pruningtechnique to select entity neighbors according to user interests.
さらに，ユーザの興味に応じた近傍エンティティを選択するために，近傍エンティティ刈り込み手法を導入している．
CNE-SUE [136] applies a GCN to diferentsubgraphs of an entire user behavior graph to learn diferent interest representations for diferent behaviorclusters.
CNE-SUE [136] は，ユーザ行動グラフ全体の異なる部分グラフに対してGCNを適用し，異なる行動クラスタに対して異なる興味表現を学習する．
It further employs an intra-cluster attention mechanism to pool node representations and uses anintra-cluster attention mechanism to aggregate cluster representations.
さらに、クラスタ内注目メカニズムを用いてノード表現をプールし、クラスタ内注目メカニズムを用いてクラスタ表現を集約する。
These methods can usually capture therich high-order relatedness between users’ click behaviors to discover latent user interest.
これらの方法は、通常、ユーザのクリック行動間の豊かな高次の関連性を捕らえ、潜在的なユーザの興味を発見することができる。

In addition to click behaviors, a few methods also consider the ID information of users [235,237].
また，クリック行動だけでなく，ユーザのID情報を考慮する手法もある[235,237]．
For exam-ple, NPA [204] uses a news-level personalized attention network to select important news according to usercharacteristics, where the embeddings of user IDs are used to generate the attention queries.
例えば，NPA [204]はニュースレベルのパーソナライズされたアテンションネットワークを用いて，ユーザの特徴に応じた重要なニュースを選択するもので，ユーザIDの埋め込みがアテンションクエリの生成に用いられている．
LSTUR [2] learnsshort-term user interest embeddings by a GRU network, and models long-term user interests by the embeddingsof user IDs.
LSTUR [2]では，短期的なユーザインタレストの埋め込みをGRUネットワークによって学習し，長期的なユーザインタレストをユーザIDの埋め込みによってモデル化する．
To fuse the two kinds of user representations, LSTUR explores two methods, i.e., concatenating twovectors together, or using the long-term user interest embedding to initialize the hidden state of the GRU network.This framework is further used by CUPMAR [190] and KG-LSTUP [185].
このフレームワークはさらにCUPMAR [190]とKG-LSTUP [185]によって使用されている。
These methods can usually better serveactive users with rich behaviors to tune their ID embeddings.
これらの方法は，通常，IDの埋め込みを調整するために，豊富な行動を持つアクティブなユーザーをより良く扱うことができる．
However, they have some diiculties in handlingcold-start users without well-tuned user embeddings.
しかし，これらの方法は，ユーザIDの埋め込みが十分に調整されていない冷やかしのユーザを扱うのにいくつかの困難がある．

All the aforementioned methods mainly rely on the information of users’ click behaviors.
前述したすべての手法は、主にユーザのクリック行動の情報に依存している。
However, clickbehaviors are very noisy and may not necessarily indicate user interest, and it is diicult to comprehensively andaccurately infer user interest from click feedback only.
しかし，クリック行動は非常にノイジーであり，必ずしもユーザの興味を示すとは限らない．また，クリックフィードバックのみからユーザの興味を包括的かつ正確に推測することは困難である．
Thus, a few methods study incorporating other kindsof user information to enhance user interest modeling [238].
このため，ユーザインタレストのモデリングを強化するために，他の種類のユーザ情報を取り入れることを研究する方法がいくつかある[238]．
One major direction is adding context features toenhance user modeling.
このため，ユーザインタフェースのモデリングを強化するために，他の種類のユーザ情報を取り入れることを研究している手法もある[238]．
For example, CHAMELEON [31,46] uses several user context features like time, device,location and referrer.
例えば、CHAMELEON [31,46]は時間、デバイス、位置、リファラなどの ユーザーの文脈の特徴を利用する。
It uses a UGRNN network to learn representations of users in a session, and the click scoreis evaluated by the cosine similarity between user and candidate news representations.
CHAMELEONはUGRNNネットワークを用いてセッション内のユーザの表現を学習し，ユーザとニュース表現候補の間のコサイン類似度によってクリックスコアを評価する．
The context features usedin these methods can provide rich information for inferring users’ current preferences to improve subsequentnews recommendation.
これらの手法で用いられるコンテキスト特徴は，ユーザの現在の嗜好を推測し，その後のニュース推薦を改善するための豊富な情報を提供することができる．

Another main direction is incorporating various kinds of user behaviors [133].
もう一つの主要な方向は、様々な種類のユーザー行動を取り入れることである[133]。
For example, NRHUB [206]considers heterogeneous user behaviors, including news clicks, search queries, and browsed webpages.
例えば，NRHUB[206]は，ニュースのクリック，検索クエリ，閲覧したウェブページなどの異種のユーザ行動を考慮する．
It incor-porates diferent kinds of user behaviors as diferent views of users by learning a user embedding from eachkind of user behaviors separately, where a combination of CNN and attention network is used to learn behaviorrepresentations and a behavior attention network is used to learn a user embedding by selecting important userbehaviors.
NRHUBは、CNNとアテンションネットワークを組み合わせて行動表現を学習し、行動アテンションネットワークを用いて重要なユーザ行動を選択してユーザ埋め込みを学習することにより、異なる種類のユーザ行動を異なるユーザ観として取り込んでいる。
The user embeddings from diferent views are aggregated into a uniied one via a view attention network.
また、異なるビューからのユーザ埋め込みは、ビューアテンションネットワークを介して統一的な埋め込みに集約される。
The efectiveness of webpage browsing behaviors in user modeling for news recommendation is alsostudied by WG4Rec [176].
また，WG4Rec[176]では，ニュース推薦のためのユーザモデリングにおけるウェブページ閲覧行動の有効性が研究されている．
CPRS [213] considers users’ click and reading behaviors in user modeling.
CPRS [213]では，ユーザのクリック行動と読書行動をユーザモデリン グに利用している．
It modelsthe click preference of users from the titles of clicked news, and models their reading satisfaction from thebody of clicked news as well as the personalized reading speed metric derived from dwell time and body length.NRNF [209] uses a dwell time threshold to divide click news into positive ones and negative ones.
NRNF [209]は，クリックされたニュースのタイトルからユーザのクリック嗜好を，クリックされたニュースの本文と滞留時間と本文の長さから得られるパーソナライズされた読書速度指標からユーザの読書満足度をモデル化している．
It uses separateTransformers and attention networks to learn positive and negative user interest representations.
NRNF [209]は、クリックされたニュースをポジティブとネガティブに分けるために、別々のTransformersとアテンションネットワークを用いて、ポジティブとネガティブなユーザインタレストの表現を学習している。
FeedRec [215]uses various kinds of user feedback including click, nonclick, inish, quick close, share and dislike to model userinterest.
FeedRec [215]は、クリック、ノンクリック、イニッシュ、クイッククローズ、シェア、ディスライクなど様々な種類のユーザフィードバックを用いて、ユーザの興味をモデル化する。
It uses a heterogeneous Transformer to model the relatedness between all kinds of feedback and usesdiferent homogeneous Transformers to model the interactions between the same kind of feedback.
フィードバック間の関連性をモデル化するために異種変換器を用い、同じ種類のフィードバック間の相互作用をモデル化するために異なる同種変換器を用いている。
In addition, ituses a strong-to-weak attention network that uses the representations of strong feedback to distill real positiveand negative user interest information from weak feedback.
さらに、強いフィードバックの表現を使って、弱いフィードバックから本当の正と負のユーザインタレスト情報を抽出するstrong-to-weak attention networkを使用する。
These methods can usually infer user interests moreaccurately by mining complementary information encoded in multiple kinds of user behaviors.
これらの手法は、通常、複数の種類のユーザ行動にコード化された補完的な情報をマイニングすることで、より正確にユーザの興味を推測することができる。

There are also several methods that learn user representations on graphs that involve the collaborativeinformation of users and news.
また，ユーザとニュースの協調情報を含むグラフからユーザ表現を学習する手法もいくつか提案されている．
For example, IGNN [161] learns content-based user representations using theaverage embedding of clicked news, and learns graph-based user representations from the user-news graphvia a graph neural network.
例えば，IGNN [161]は，クリックされたニュースの平均埋め込みを利用してコンテンツに基づくユーザ表現を学習し，ユーザとニュースのグラフからグラフに基づくユーザ表現をグラフニューラルネットワークによって学習する．
The content-based user representation is concatenated with graph-based userrepresentation to form a uniied one.
学習したコンテンツベースのユーザ表現は，グラフベースのユーザ表現と連結され，一つのユーザ表現となる．
GNewsRec [70] uses the same architecture with DAN to learn short-term userrepresentations, and uses a two-layer graph neural network (GNN) to learn long-term user representations froma heterogeneous user-news-topic graph.
GNewsRec [70]はDANと同じアーキテクチャを用いて短期的なユーザ表現を学習し、2層のグラフニューラルネットワーク（GNN）を用いて異種のユーザ-ニュース-トピックグラフから長期的なユーザ表現を学習する。
Both short-term and long-term user representations are concatenated tobuild a uniied user representation.
短期ユーザ表現と長期ユーザ表現の両方が連結され、統一的なユーザ表現が構築される。
GERL [53] uses multi-head self-attention and additive attention networks toform content-based user representations from the click history.
GERL [53]はマルチヘッド自己注意ネットワークと加算的注意ネットワークを用いて、クリック履歴からコンテンツに基づくユーザ表現を形成する。
In addition, it uses a graph attention network tolearn graph-based representations of users by capturing high-order information on the user-news graph, whichare further combined with the content-based user representations.
さらに、グラフアテンションネットワークを用いて、ユーザーニューズグラフの高次情報を取得することにより、グラフベースのユーザー表現を学習し、それをコンテンツベースのユーザー表現と組み合わせることで、コンテンツベースのユーザー表現を構築する。
MVL [170] uses attention networks to learnuser interest representations in a content view, and uses a graph attention network to model user interest fromthe user-news graph in a graph view.
MVL [170]では、アテンションネットワークを用いて、コンテンツビューにおけるユーザインタレスト表現を学習し、グラフアテンションネットワークを用いて、グラフビューにおけるユーザ・ニュースのグラフからユーザインタレストをモデル化している。
GNUD [71] uses a disentangled graph convolution network to learn userrepresentations from the user-news graph.
GNUD [71]では、分離グラフ畳み込みネットワークを用いて、ユーザーニューズグラフからユーザー表現を学習する。
These methods can exploit the high-order information on graphsto enhance user modeling.
これらの方法は、グラフの高次情報を利用し、ユーザモデリングを強化することができる。
GBAN [133] combines user embeddings learned by an LSTM and heterogeneousgraph embeddings.
GBAN [133]はLSTMによって学習されたユーザ埋め込みと異種グラフ埋め込みを組み合わせる。
It further introduces subgraph core and coritivity scores that measure the importance of atarget user-news pair in the subgraph to enhance user representations.
さらに、サブグラフにおけるターゲットユーザとニュースのペアの重要度を測定するサブグラフコアと相関性スコアを導入し、ユーザ表現を強化する。
These methods can take the advantage ofhigh-order interaction information between user and news as well as the associated meta features.
これらの手法は、ユーザとニュースの間の高次の相互作用情報や関連するメタ特徴を利用することができる。
However, it ischallenging for them to accurately represent new users that do not participate in the model training.
しかし、モデル学習に参加していない新しいユーザーを正確に表現することは困難である。

We summarize the user information and user modeling techniques used in these deep learning-based methodsin Table 5.
これらの深層学習ベースの手法で用いられているユーザー情報およびユーザーモデリング技術を表5にまとめた。
We then provide several discussions on the user modeling methods introduced in this section.
次に、本節で紹介するユーザモデリング手法に関するいくつかの考察を行う。

## 4.3. 4.3 Discussions on User Modeling 4.3. 4.3 ユーザーモデリングに関する考察

### 4.3.1. 4.3.1 Feature-based User Modeling. 4.3.1. 4.3.1 特徴に基づくユーザーモデリング。

Most feature-based methods construct user proiles based on the collectionsof features extracted from the clicked news.
特徴量ベースの手法の多くは，クリックされたニュースから抽出された特徴量に基づいてユーザプロファイルを構築する．
Besides the news information, some methods leverage additionaluser features to facilitate user modeling.
ニュース情報の他に，ユーザのモデリングを容易にするために，ユーザの特徴を追加で利用する手法もある．
For example, the demographics of users (e.g., age, gender and profession)are used in several methods, since users with diferent demographics usually have diferent preferences onnews.
例えば，ユーザの属性（年齢，性別，職業など）は，通常，異なる属性を持つユーザはニュースに対する嗜好が異なるため，いくつかの手法で利用されています．
The location of users can be used to identify the news related to the user’s neighborhood, and the accesspatterns of users can also help understand the news click behaviors of users.
また，ユーザーの位置情報を利用して，ユーザーの近隣に関連するニュースを特定したり，ユーザーのアクセスパターンを利用して，ユーザーのニュースクリック行動を理解することもできる．
In addition, many methods usethe tags or keywords of users to indicate user interest, and cluster users based on their characteristics.
また、ユーザーのタグやキーワードを利用してユーザーの興味を示し、その特徴に基づいてユーザーをクラスタリングする手法も多く用いられている。
In thisway, the recommender system can more efectively recommend news according to users’ interest in diferenttopics.
このようにすることで，推薦システムは，ユーザの様々なトピックへの興味に応じたニュースをより効果的に推薦することができる．
Moreover, several methods incorporate user behaviors on other platforms, such as social media, searchengines and e-commerce platforms.
さらに、ソーシャルメディア、検索エンジン、電子商取引プラットフォームなど、他のプラットフォームにおけるユーザーの行動を取り入れる手法もある。
These behaviors can not only facilitate user interest modeling, but also has the potential to mitigate the problem of cold-start on the news platform if user data can be successfullyaligned.
これらの行動は、ユーザーの興味・関心のモデリングを容易にするだけでなく、ユーザーデータをうまく整合させることができれば、ニュースプラットフォームのコールドスタートの問題を軽減する可能性もある。
However, feature-based user modeling methods usually require massive expertise for feature design andvalidation, and may not be optimal for representing user interests.
しかし、特徴量ベースのユーザーモデリング手法は、通常、特徴量の設計と検証に膨大な専門知識を必要とし、ユーザーの興味関心を表現するのに最適な手法とは言えない可能性があります。

### 4.3.2. 4.3.2 Deep Learning-based User Modeling. 4.3.2. 4.3.2 深層学習によるユーザーモデリング。

<img src="https://d3i71xaburhd42.cloudfront.net/a867894db8f9d544a471e86d8844008861f6a2ec/23-Table5-1.png">

Table 5.
表 5.
Comparison of different methods on user modeling.
ユーザモデリングに関する各手法の比較。

Deep learning-based user modeling methods usually aim to learnuser representations from user behaviors without feature engineering.
深層学習を用いたユーザモデリング手法は、通常、特徴量エンジニアリングを行わずに、ユーザの行動からユーザ表現を学習することを目的としている。
Many of them infer user interests merelyfrom click behaviors, because click behaviors are implicit indications of users interest in news.
その多くは，クリック行動からユーザの興味を推測する．なぜなら，クリック行動はユーザのニュースへの興味を暗黙的に示すからである．
However, clickbehaviors are usually noisy and they do not necessarily indicate real user interests.
しかし、クリック行動は通常ノイズが多く、必ずしも実際のユーザの興味を示しているとは限らない。
Thus, many methods considerother kinds of information in user modeling.
そのため，多くの手法では，ユーザモデリングにおいて別の種類の情報を考慮している．
For example, some methods such as NPA and LSTUR incorporate theIDs of users to better capture users’ personal interest.
例えば，NPA や LSTUR などの手法は，ユーザの個人的な興味をよりよく捉えるために，ユーザの ID を取り込んでいる．
CHAMELEON and DAINN consider the context features ofusers such as devices and user locations.
CHAMELEON や DAINN はデバイスやユーザーの位置など、ユーザーのコンテクスト特性を考慮する。
CPRS, FeedRec and GBAN incorporate multiple kinds of user feedbackon the news platform to consider user engagement information in user interest modeling.
CPRS, FeedRec, GBANはニュースプラットフォームに対する複数の種類のユーザフィードバックを取り入れ、ユーザインタレストのモデリングにおいてユーザエンゲージメント情報を考慮する。
GERL and GNewsReccan exploit the high-order information on graphs to encode user representations.
GERLとGNewsReccanはグラフの高次情報を利用し、ユーザ表現を符号化する。
However, it is still diicult forthese methods to accurately infer user interests when user behaviors on the news platforms are sparse.
しかし、これらの手法では、ニュースプラットフォーム上でのユーザの行動が疎である場合、ユーザの興味を正確に推測することはまだ困難である。
There areonly two methods, i.e., NRHUB and WG4Rec, that consider users’ behaviors on multiple platforms, which canstill model users accurately even user behaviors on the news platform are sparse.
また，NRHUBとWG4Recの2つの手法では，複数のプラットフォームにおけるユーザの行動を考慮しており，ニュースプラットフォームにおけるユーザの行動が疎であっても，ユーザを正確にモデル化することができる．
However, there may exist somediiculties in linking user data on diferent platforms due to privacy reasons.
しかし，プライバシー保護の観点から，異なるプラットフォーム上のユーザデータを連携させることは困難である．

According to the summarization in Table 3, we can see that the model architectures used for user representationlearning are diverse.
表3にまとめると、ユーザー表現学習に用いられているモデルアーキテクチャは多様であることがわかる。
Some methods utilize recurrent neural networks to capture the relatedness of news clickedby users, such as EBNR, DAN and CHAMELEON.
EBNR、DAN、CHAMELEONのように、ユーザがクリックしたニュースの関連性を捕らえるためにリカレントニューラルネットワークを利用する手法もある。
With the great success of Transformer models, many methodsalso use self-attention or Transformer networks to model the global contexts of user behaviors.
Transformerモデルの大きな成功により、多くの手法は自己アテンションやTransformerネットワークを用いてユーザー行動のグローバルコンテキストをモデル化する。
However, thesesequential models cannot efectively model the high-order relations between user behaviors, which can provideuseful contexts for user interest understanding.
しかし、これらの逐次モデルは、ユーザの興味理解に有用なコンテキストを提供することができるユーザ行動間の高次関係を効果的にモデル化することができません。
Instead of modeling user behaviors as a sequence, several methodslike User-as-Graph model each user as a personalized graph, where the high-order relations between behaviorscan be fully modeled.
ユーザ行動をシーケンスとしてモデル化する代わりに、User-as-Graphのようないくつかの方法は、行動間の高次の関係を完全にモデル化することができるパーソナライズされたグラフとして各ユーザをモデル化している。
In addition, several works such as GERL and GNUD use graph neural networks to capturethe high-order interactions between users and news on the global user-news graphs, which can also help betterunderstand user interest by incorporating collaborative information.
また、GERLやGNUDはユーザーとニュースの高次の相互作用をグラフニューラルネットワークで表現しており、協調的な情報を取り込むことでユーザーの興味関心をよりよく理解することができる。
However, the computational cost of thesegraph-based architectures is usually much heavier than sequential models, and collaborative signals are usuallynot available for cold-start users and news.
しかし、これらのグラフベースのアーキテクチャの計算コストは、通常、逐次モデルよりもはるかに重く、協調信号は通常、コールドスタートのユーザとニュースには利用できません。

To select clicked news that is informative for inferring user interest, attention mechanisms are widely used bymany methods.
クリックされたニュースのうち、ユーザの興味を推測するのに有益なものを選択するために、多くの手法でアテンション機構が広く用いられている。
In some works such as NAML and KRED, the attention query is a global parameter vector, whichis invariant with respect to diferent users.
NAMLやKREDでは、アテンションクエリはグローバルなパラメータベクトルであり、異なるユーザに対して不変である。
In the NPA method, the attention query is generated by the embeddingof user ID, which can achieve personalized news selection.
NPAでは、ユーザIDを埋め込むことでアテンションクエリを生成し、パーソナライズされたニュース選択を実現する。
Both kinds of attention mechanisms are eicient inthe online test phase because user representations can be prepared in advance [204].
両者の注目機構は，ユーザ表現を事前に準備できるため，オンラインテスト段階において有効である[204]．
However, the relatednessbetween candidate news and clicked news cannot be fully modeled, which may not be optimal in modeling userinterests in a speciic candidate news.
しかし，候補ニュースとクリックされたニュースの関連性を完全にモデル化することはできず，特定の候補ニュースに対するユーザの興味をモデル化するには最適でない可能性がある．
Another kind of attention mechanism, i.e., candidate-aware attention, isalso widely used by many methods such as DKN, DAN and KIM.
また、別の種類の注意メカニズム、すなわち、候補を意識した注意も、DKN、DAN、KIMなどの多くの手法で広く利用されている。
In candidate-aware attention networks, therepresentation of candidate news is used as the attention query, and user representations can be dynamicallyconstructed based on candidate news.
候補意識型注目ネットワークでは、候補ニュースのプレゼンテーションが注目クエリとして用いられ、候補ニュースに基づいてユーザ表現を動的に構築することができる。
However, they need to memorize the representations of all clicked news inthe test phase, which may lead to some sacriice in eiciency.
しかし、ユーザはテスト段階でクリックされた全てのニュースの表現を記憶する必要があり、効率性が損なわれる可能性がある。

Some methods study modeling multiple types of user interests.
いくつかの方法は、複数のタイプのユーザーの興味をモデル化することを研究している。
For example, LSTUR, GNewsRec and FedRecconsider both long-term and short-term interests of users to better capture their interest dynamics.
例えば、LSTUR, GNewsRec, FedRec はユーザの長期的興味と短期的興味の両方を考慮し、ユーザの興味のダイナミクスをよりよく捉えることができる。
HieRec modelsthe hierarchical structure of user interests, which can capture the user interests in diferent granularities.
HieRecはユーザの興味の階層構造をモデル化し、様々な粒度でユーザの興味を捉えることができる。
Thesemethods can improve user interest understanding of user interests by taking diferent kinds of user interest intoconsideration.
これらの手法は、様々な種類のユーザの興味を考慮することで、ユーザの興味理解を向上させることができる。
However, user interests are diverse and evolutional, which are still diicult to be comprehensivelyand accurately modeled by these methods.
しかし、ユーザの興味は多様であり、進化的であるため、これらの手法で包括的かつ正確にモデル化することはまだ困難である。

### 4.3.3. 4.3.3 Diferences to User Modeling in General Recommendation. 4.3.3. 4.3.3 一般的なレコメンデーションにおけるユーザーモデリングとの相違点。

The user modeling techniques used for person-alized news recommendation have close relations to the user modeling methods in general recommendationscenarios such as e-commerce [246] and movie recommendation [35].
ニュース推薦に用いられるユーザーモデリング技術は、電子商取引[246]や映画推薦[35]などの一般的な推薦シナリオにおけるユーザーモデリング手法と密接な関係にある。
For example, the core neural architecturessuch as RNN, CNN, self-attention and graph neural networks, are also widely used for sequential recommendation.In addition, several useful user modeling paradigms such as long short-term user interest modeling are alsopopular in other recommendation ields.
例えば、RNN、CNN、自己アテンション、グラフニューラルネットワークなどのコアニューラルアーキテクチャは、逐次推薦にも広く用いられている。さらに、長期短期ユーザー興味モデルなどのいくつかの有用なユーザーモデリングのパラダイムは、他の推薦分野でも一般的である。
However, by scrutinizing recent literature, we ind there are severalunique characteristics of user modeling in personalized news recommendation:
しかし、最近の文献を精査した結果、個人向けニュース推薦におけるユーザモデリングにはいくつかのユニークな特徴があることがわかった。

(1) Short news lifecycles.
(1) 短いニュースライフサイクル。
Diferent from the common e-commerce recommendation scenarios where items canbe actively interacted with for months or even years [247], most news articles have very short lifecycles (i.e., a fewdays).
このため、ニュース記事のライフサイクルは非常に短い（すなわち、数日）。
Thus, in news recommendation it is important to take this unique characteristic into consideration whendesigning user modeling algorithms.
したがって、ニュース推薦では、ユーザーモデリングアルゴリズムを設計する際に、このユニークな特性を考慮することが重要です。
For example, in GNN-based methods for general recommendation, itemnodes can be simply represented by ID embeddings.
例えば、GNNを用いた一般的な推薦手法では、アイテムノードはIDエンベッディングで簡単に表現できる。
However, in GNN-based news recommender, it is better tolearn embeddings of news nodes from news content to handle uncovered news in user modeling [70].
しかし、GNNを用いたニュース推薦においては、ニュースノードの埋め込みをニュースコンテンツから学習した方が、ユーザモデリングにおいて未発見のニュースを扱える[70]。
In addition,the quick vanishment of old news de facto limits the exploitation of collaborative signals in user modeling due tothe large fraction of cold news in the inference stage.
また，古いニュースはすぐに消えてしまうため，推論段階でのコールドニュースの割合が大きく，ユーザモデリングにおける協調信号の利用は事実上制限される．

(2) Fine-grained candidate-aware user modeling.
(2) きめ細かな候補考慮型ユーザモデリング。
In many recommendation tasks, items are mainly representedby their overall embeddings [183], and modeling feature interactions is important for candidate-aware usermodeling [246].
多くの推薦タスクにおいて、項目は主にその全体的な埋め込みによって表現され[183]、特徴の相互作用のモデリングは候補を考慮したユーザモデリングにとって重要である[246]。
By contrast, news articles have rich content and context information, and the interactionsbetween user behaviors and candidate news can be modeled in a more ine-grained way (e.g., word-levelinteractions).
これに対し、ニュース記事は豊富なコンテンツとコンテキスト情報を持っており、ユーザ行動とニュース候補の間の相互作用はよりきめの細かい方法（例えば、単語レベルの相互作用）でモデル化することが可能である。
Capturing the ine-grained relevance between user behaviors and candidate news is very importantfor understanding user interest in a speciic candidate news article.
ユーザ行動とニュース候補の間のきめ細かい関連性を捉えることは、特定のニュース候補に対するユーザの興味を理解する上で非常に重要である。
Thus, ine-grained candidate-aware usermodeling is a core technique used in many recent news recommendation methods.
このように，粒度の異なる候補を考慮したユーザモデリングは，最近の多くのニュース推薦手法で用いられているコア技術である．

(3) User modeling as document modeling.
(3) 文書モデリングとしてのユーザモデリング
Diferent from many recommendation scenarios where user behaviorsare not associated with suicient textual information [245], in news recommendation user behaviors are usuallyclicked news that contain rich texts.
ユーザ行動が十分なテキスト情報と関連しない多くの推薦シナリオとは異なり[245]、ニュース推薦におけるユーザ行動は通常、豊富なテキストを含むニュースがクリックされる。
Thus, the user modeling problem in news recommendation can be formulatedas a document modeling problem, where the texts of clicked news are embedded in user łdocuments”.
したがって，ニュース推薦におけるユーザモデリング問題は，クリックされたニュースのテキストがユーザ文書に埋め込まれる文書モデリング問題として定式化することができる．
Several recentmethods follow this setting and employ strong pre-trained language models to empower user modeling [81,241].The success of these PLM-based user modeling techniques indicates that there may not be a huge barrier betweenNLP and user modeling for news recommendation, which is a unique characteristic of the news recommendationield.
これらのPLMベースのユーザモデリング手法の成功は，ニュース推薦におけるNLPとユーザモデリングの間に大きな障壁がないことを示唆している．

(4) Potential strong temporal diversity preference.
(4) 時間的多様性選好の可能性
Diferent from general recommendation scenarios whereusers may prefer to click very similar items, in news recommendation users tend to click news that are somewhatdiferent from the previously clicked ones [1] (i.e., preference on serendipity).
一般的な推薦では、ユーザーは非常に類似したものをクリックする傾向がありますが、ニュース推薦では、ユーザーは以前にクリックしたものとは異なるニュースをクリックする傾向があります [1]（すなわち、セレンディピティに対する嗜好性）。
As pointed by a recent study [216],it may not be very suitable to model news recommendation as a standard sequential recommendation task, andit is important to consider such temporal diversity preference in user modeling.
最近の研究[216]で指摘されているように，ニュース推薦を標準的な逐次推薦タスクとしてモデル化することはあまり適切ではない可能性があり，ユーザのモデル化においてこのような時間的多様性の選好を考慮することが重要である．
The results show that manysequential models such as RNN [66] and casual self-attention [86] are inferior to standard self-attention thatfocus more on global context rather than sequential dependency.
その結果、RNN[66]やカジュアル自己注意[86]などの多くの逐次モデルは、逐次依存性よりもグローバル文脈に注目する標準自己注意に劣ることが示された。
Further study on this unique phenomenon isneeded to better understand user modeling mechanism in news recommendation.
ニュース推薦におけるユーザモデリングのメカニズムをより良く理解するために、このユニークな現象に関するさらなる研究が必要である。

In summary, by reviewing user modeling techniques used in existing news recommendation methods, weargue that user modeling is also remained challenging due to many reasons, such as the noise and sparsity ofuser behaviors, the diverse and dynamic characteristics of user interests, and the diiculties in modeling userinterests in a speciic candidate news efectively and eiciently.
既存のニュース推薦手法で用いられているユーザモデリング技術を概観すると、ユーザ行動のノイズやスパース性、ユーザの興味の多様性や動的特性、特定の候補ニュースに対するユーザの興味を効果的かつ効率的にモデリングすることの難しさなど、多くの理由により、ユーザモデリングにも課題が残されていることがわかる。

# 5. 5 PERSONALIZED RANKING 5. 5 パーソナライズドランキング

On the basis of news and user modeling, news ranking aims to rank candidate news for personalized displayaccording to users’ personal interest.
ニュースランキングは、ニュースとユーザのモデリングに基づいて、ユーザの個人的な興味に応じてパーソナライズされた表示のために候補のニュースをランク付けすることを目的としています。
Common news ranking techniques can be divided into two categories, i.e.,relevance-based and reinforcement learning-based.
一般的なニュースランキング技術は、関連性ベースと強化学習ベースの2つのカテゴリに分類される。
We introduce them in the following sections.
以下では、これらの手法を紹介する。

## 5.1. 5.1 Relevance-based Personalized Ranking 5.1. 5.1 関連性に基づくパーソナライズドランキング

Relevance-based news ranking methods usually rank candidate news with user interests based on their personal-ized relevance.
関連性に基づくニュースランキング手法では，通常，ユーザの興味に関連するニュースの候補を個人的な関連性に基づいてランク付けします．
In these methods, how to accurately measure the relevance between candidate news and userinterest is a core problem.
これらの手法では，候補ニュースとユーザの興味との関連性をどのように正確に測定するかが中心的な問題である．
Many methods directly evaluate the user-news relevance based on the similarities oftheir inal representations.
多くの手法は，内部表現の類似性に基づいてユーザとニュースの関連性を直接評価する．
For instance, Goossen et al. [58] computed the cosine similarities between the CF-IDFfeature vectors of user and news to measure their relevance.
例えば，Goossen ら [58] はユーザとニュースの CF-IDF 特徴ベクトル間の cosine 類似度を計算し，両者の関連性を測定している．
Garcin et al. [52] used the similarities between thenews topic vectors and the user topic vector to evaluate their relevance.
Garcinら[52]はニュースのトピックベクトルとユーザのトピックベクトル間の類似度を用いて、それらの関連性を評価した。
Okura et al. [144] used the inner productbetween news and user representations to predict the relevance scores.
大倉ら[144]はニュース表現とユーザ表現間の内積を用いて関連性スコアを予測した。
DFM [116] uses an inception module thatcombines neural networks with diferent depths to compute the relevance scores from news and user features.These methods usually employ two-tower architectures, which enable eicient inference by computing newsand user features in advance.
DFM [116]は，深さの異なるニューラルネットワークを組み合わせたインセプションモジュールを用いて，ニュースとユーザの特徴から関連性スコアを計算する．これらの手法は通常2タワーアーキテクチャを採用しており，ニュースとユーザの特徴を事前に計算することで効率的な推論を可能にしている．
However, user interests are usually diverse, and candidate news may only matchthe user interests indicated by a part of the clicked news.
しかし，ユーザの興味は多様であり，クリックされたニュースの一部しかユーザの興味に合致しない可能性がある．
These methods cannot fully consider the relatednessbetween candidate news and clicked news, and the matching between candidate news and user interest may notbe very accurate.
これらの手法では，候補ニュースとクリックされたニュースの関連性を十分に考慮することができず，候補ニュースとユーザインタレストとのマッチングがあまり正確でない可能性がある．

A few methods use ine-grained interest matching techniques to better model the relevance between users’interest and candidate news.
いくつかの手法では，ユーザの興味と候補ニュースの関連性をより適切にモデル化するために，粒度の細かい興味マッチング技術を使用している．
For example, FIM [196] irst multiplies together the word representations of candidatenews and clicked news, and then uses a matching module with 3-D CNN networks to compute relevance scoresby capturing the ine-grained relatedness between candidate news and clicked news.
例えば，FIM [196]では，まず候補ニュースとクリックされたニュースの単語表現を掛け合わせ，次に3次元CNNネットワークによるマッチングモジュールを用いて，候補ニュースとクリックされたニュース間の粒度の細かい関連性を捉えることにより関連性スコアを計算する．
KIM [156] irst uses aknowledge-aware news co-encoder to model the relatedness between words and entities in candidate newsand clicked news, and further uses a user-news co-encoder to further help model the interactions betweenclicked news and candidate news for better relevance modeling.
KIM [156]はまず、知識認識型ニュースコーエンコーダを用いて、候補ニュースとクリックされたニュースの単語と実体の間の関連性をモデル化し、さらにユーザニュースコエンコーダを用いて、クリックされたニュースと候補ニュース間の相互作用をモデル化して、より良い関連性のモデル化を支援します。
HieRec [160] has a hierarchical interest matchingmechanism that matches candidate news with the ine-grained subtopic-level user interest, the coarse-grainedtopic-level user interest and the overall user interest.
HieRec [160]は階層的なインタレストマッチング機構を持ち、サブトピックレベルのユーザのインタレスト、粗いトピックレベルのユーザのインタレスト、全体のユーザのインタレストとニュース候補をマッチングさせる。
AMM [240] uses a multi-ield matching scheme to model theinteractions between each pair of views of a clicked news and a candidate news.
AMM [240]では，クリックされたニュースと候補ニュースの各ビューのペアの間の相互作用をモデル化するために，マルチフィールドマッチングスキームを使用している．
These single-tower methods canmore accurately evaluate the relevance between candidate news and user interest by modeling their ine-grainedand multi-grained relatedness, which can help generate news ranking results that better target user interest.However, these methods usually have much larger computational costs in the inference stage than coarse-grainedinterest matching, which may hinder their application in some low-latency or low-resource scenarios.
しかし，これらの手法は通常，推論段階での計算コストが粗視化インタレストマッチングよりはるかに大きいため，低遅延または低リソースシナリオでの応用の妨げとなる可能性があります．

In most methods, candidate news with higher relevance to user interest will gain higher ranks.
多くの手法では，ユーザの興味と関連性の高いニュース候補が高い順位を獲得する．
However, thesemethods may tend to recommend news that are similar to those previously clicked by users, which is also calledthe łilter bubble” problem.
しかし，これらの手法は，ユーザが過去にクリックしたニュースと類似したニュースを推薦する傾向があり，これは「フィルターバブル」問題とも呼ばれる．
Thus, some news ranking methods explore to recommend news that are somewhatdiferent from previously clicked ones to introduce diversity and serendipity [1].
そこで，いくつかのニュースランキング手法では，多様性とセレンディピティを導入するために，以前にクリックされたニュースとは異なるニュースを推薦することを検討しています[1]．
For example, Newsjunkie [47] isa system that ranks news articles based on their novelty in the context of the news that users previously clicked.SCENE [109] irst ranks news articles based on their relevance to user interests, and then reines the ranking listbased on news popularity and recency to form the inal recommendation list.
例えば，Newsjunkie [47] は，ユーザが過去にクリックしたニュースとの関連性に基づいてニュース記事をランク付けするシステムである．SCENE [109] は，まずユーザの興味との関連性に基づいてニュース記事をランク付けし，そのランキングリストをニュース人気度と最新性に基づいて絞り込み，最終的に推奨リストを作成する．
Diferent from the methods that aresolely based on the relevance between candidate news and user interests, these methods have the potential toprovide more diverse recommendations.
これらの手法は，候補となるニュースとユーザの興味との関連性にのみ基づく手法とは異なり，より多様な推薦を提供する可能性がある．

## 5.2. 5.2 Reinforcement Learning-based Personalized Ranking 5.2. 5.2 強化学習による個人化ランキング

## 5.3. 5.3 Discussions on Personalized Ranking 5.3. 5.3 パーソナライズドランキングに関する考察

In this section we provide some discussions on the news ranking methods in existing personalized news rec-ommender systems.
本節では，既存のパーソナライズドニュースレコメンダーシステムにおけるニュースランキング手法について考察する．
Relevance-based news ranking methods mainly need to accurately evaluate the relevancebetween candidate news and user interest for subsequent news ranking.
関連性に基づくニュースランキング手法では，主に候補ニュースとユーザインタレストとの関連性を正確に評価し，その後のニュースランキングに反映させる必要がある．
Many methods model their overallrelevance by evaluating the relevance between the uniied representations of user interest and candidate news.However, candidate news usually can only match part of user interests, and directly match the overall user interestwith candidate news may be suboptimal.
しかし，候補ニュースは通常ユーザの関心の一部にしか合致せず，ユーザの関心全体と候補ニュースとの直接の合致は最適とは言えない．
A few methods explore to evaluate the relevance between user interestand candidate news in a ine-grained way by modeling the relatedness between candidate news and clicked news,which can improve the accuracy of relevance modeling for news ranking.
しかし，候補ニュースは通常ユーザの興味の一部にしか合致せず，ユーザの興味全体と候補ニュースとの直接の合致は最適とは言えない．そこで，候補ニュースとクリックされたニュースとの関連性をモデル化し，ユーザの興味と候補ニュースとの関連性をきめ細かく評価する方法がいくつか提案されており，ニュースランキングにおける関連性モデル化の精度を向上させることが可能である．
However, these methods are muchmore time-consuming because the representations of users are dependent on candidate news and cannot becomputed in advance.
しかし，これらの方法は，ユーザの表現がニュース候補に依存し，事前に計算できないため，より多くの時間を必要とする．
Moreover, pure relevance-based interest matching methods may tend to recommend newsthat are similar to previously clicked news, which is not beneicial for users to receive diverse news information.Thus, a few works explore to adjust the news ranking strategy by incorporating other factors such as newsnovelty, popularity and recency, which have the potential to make more diverse news recommendations andmitigate the filter bubble problem in news recommender systems.
また，純粋な関連性ベースの興味マッチング手法では，過去にクリックされたニュースと類似したニュースを推薦する傾向があり，ユーザが多様なニュース情報を受け取る上で有益ではない．そこで，ニュースの新規性，人気，再来訪などの他の要素を取り入れることによって，ニュース推薦システムにおいてより多様なニュースを推薦しフィルタバブル問題を軽減できる可能性がある，いくつかの研究結果が示されている．

In relevance-based news ranking methods, candidate news is usually greedily matched with users, i.e., choosingthe news in each impression that mostly satisfy the ranking policy on the current candidate news list.
関連性ベースのニュースランキング手法では，通常，候補となるニュースを貪欲にマッチングさせる．すなわち，現在の候補ニュースリストのランキングポリシーをほぼ満足するニュースを各インプレッションで選択する．
However,it may not be optimal in improving long-term user experience.
しかし，これは長期的なユーザ体験を向上させる上で最適とは言えない．
In reinforcement learning-based methods, theranking algorithm aims to ind the optimal ranking policy to maximize the long-term reward.
強化学習ベースの手法では、ランキングアルゴリズムは、長期的な報酬を最大化するために最適なランキングポリシーを導き出すことを目的としている。
Thus, RL-basednews ranking methods may be more suitable for exploring potential user interest and improving long-term userexperience and engagement, while it may have some sacriice in short-term news CTRs.
このように，RLベースのニュースランキング手法は，短期的なニュースCTRを犠牲にする可能性がある一方で，潜在的なユーザの興味を探り，長期的な利用体験とエンゲージメントを向上させるためにはより適している可能性があります．

In summary, news ranking in news recommendation also faces many challenges, including how to accuratelyand eiciently evaluate the relevance between candidate news and user interest indicated by user behaviors, how to mitigate the łilter bubble” problem in news recommender systems, and how to explore potential user interestswithout hurting user experience.
このように、ニュース推薦におけるランキングは、候補となるニュースとユーザーの興味との関連性をいかに正確かつ効率的に評価するか、ニュース推薦システムにおける「フィルターバブル」問題をいかに軽減するか、ユーザーの体験を損なわずに潜在的なユーザーの興味をいかに探るかなど、多くの課題を抱えている。

# 6. 6 MODEL TRAINING 6. 6 モデルトレーニング

Many personalized news recommendation methods exploit machine learning models for news modeling, user mod-eling and interest matching.
個人向けニュース推薦の多くは，ニュースのモデル化，ユーザのモデル化，インタレストマッチのために機械学習モデルを利用している．
Training these models is a necessary step in building an accurate news recommendersystem.
これらのモデルを学習することは，正確なニュース推薦システムを構築するために必要なステップである．
In this section, we review the techniques used for model training in news recommendation.
本節では、ニュース推薦におけるモデル学習のための技術をレビューする。

## 6.1. 6.1 Training Methods 6.1. 6.1 トレーニング方法

In a few methods based on collaborative iltering, the news recommendation task is formulated as a ratingprediction problem, i.e., predicting the ratings that users give to news [78].
協調フィルタリングに基づくいくつかの手法では，ニュース推薦タスクは評価予測問題，すなわち，ユーザがニュースに与える評価を予測する問題として定式化されている[78]．
To learn their models, they usuallyuse loss functions such as the mean squared error (MSE) computed between the predicted ratings and the goldratings, which are further used to optimize the model [26].
また、モデルを学習するために、予測された評価とgoldratingsの間の平均二乗誤差（MSE）のような損失関数を通常使用し、さらにモデルを最適化するために使用される[26]。
However, explicit user feedback like rating is usuallyvery sparse, which may be insuicient to train an accurate recommendation model.
しかし，評価のような明示的なユーザフィードバックは非常にまばらであり，正確な推薦モデルを学習するのに十分でない可能性がある．

Since implicit feedback such as click is abundant, most methods use the click feedback of users as the predictiontarget.
クリックなどの暗黙のフィードバックが豊富であるため、多くの手法ではユーザのクリックフィードバックを予測対象としている。
They formulate the news recommendation task as a click prediction task.
これらの手法は，ニュース推薦タスクをクリック予測タスクとして定式化する．
Some methods simply classifywhether a candidate news will be clicked by a target user [43,55,197].
いくつかの手法は，候補となるニュースがターゲットユーザにクリックされるかどうかを単純に分類する[43,55,197]．
However, these methods cannot exploitthe relatedness between clicked and nonclicked samples.
しかし，これらの方法では，クリックされたサンプルとクリックされなかったサンプルの間の関連性を利用することができない．
Thus, a few methods use contrastive training techniquesto maximize the margin between the predicted click scores of clicked and nonclicked news.
そこで，いくつかの手法では，クリックされたニュースとされなかったニュースの予測クリックスコア間のマージンを最大化するために，対照的な学習手法を用いる．
For example, PP-Rec [157] uses the Bayesian Personalized Ranking (BPR) loss for model training by comparing each clickedsample with an nonclicked one.
例えば、PP-Rec [157]はベイズパーソナライズドランキング(BPR)ロスを用いて、各クリックされたサンプルとされていないサンプルを比較し、モデルの学習を行なっています。
However, the BPR loss can only exploit a small part of nonclicked samples.NPA [204] uses the InfoNCE [145] loss for model training.
NPA [204]では、モデル学習にInfoNCE [145]ロスを使用している。
For each clicked sample (regarded as a positive sample),it randomly samples a certain number of nonclicked ones (regarded as negative samples) and jointly predictstheir click scores.
各クリックされたサンプル（正のサンプルとみなす）に対して、ある数の非クリックされたサンプル（負のサンプルとみなす）をランダムにサンプリングし、それらのクリックスコアを共同で予測する。
These click scores are further normalized by the softmax function to compute the posteriorclick probabilities, and the model aims to maximize the negative log-likelihood of the posterior click probabilityof positive samples.
これらのクリックスコアをさらにソフトマックス関数で正規化し、事後クリック確率を計算し、モデルは正のサンプルの事後クリック確率の負の対数尤度を最大化することを目的とする。
In this way, the model can exploit the information of more negative samples.
この方法により、モデルはより多くの負のサンプルの情報を利用することができる。

Besides click feedback, a few methods also consider other kinds of feedback to construct training tasks.For example, CPRS [213] trains the recommendation model collaboratively in the click prediction task and anadditional reading satisfaction prediction task, which aims to infer the personalized reading speed based on userinterest and news body.
例えば，CPRS[213]では，クリック予測タスクと，ユーザの興味やニュース本文から個人的な読書速度を推測する読書満足度予測タスクで協調的に推薦モデルを学習させる．
FeedRec [215] trains the model in three tasks, including click prediction, dwell timeprediction and inish prediction.
FeedRec[215]は、クリック予測、滞留時間予測、読了予測の3つのタスクでモデルを学習させる。
GBAN [133] models the recommendation task as a future behavior classiicationproblem to predict the behavior type of a user on a speciic candidate (i.e., click, nonclick, like, follow, comment,and share).2These methods can encourage the model to optimize not only CTR but also user engagement, whichcan help learn engagement-aware news recommendation models.
GBAN [133]は、推薦タスクを将来の行動分類問題としてモデル化し、特定の候補に対するユーザの行動タイプ（すなわち、クリック、ノンクリック、いいね、フォロー、コメント、シェア）を予測する。2 これらの手法は、CTRだけでなくユーザエンゲージメントも最適化するようモデルを促すことができ、これにより、エンゲージメント考慮型のニュース推薦モデルを学習することができる。

There are several methods that use additional news information to design auxiliary training tasks.
このように，ニュース情報を利用して補助的な学習タスクを設計する手法はいくつか存在する．
For exam-ple, EBNR [144] uses autoencoder to learn news representations and it uses another weak supervision task byencouraging the embeddings of news in the same topic to be similar than the embeddings of news in diferenttopics.
例えば，EBNR [144]では，オートエンコーダーを用いてニュース表現を学習し，同じトピックのニュースの埋め込みを異なるトピックのニュースの埋め込みよりも類似させることで，別の弱い監視タスクを用いています．
TANR [205] uses an auxiliary news topic prediction task to help learn topic-aware news representa-tions.
TANR [205]はトピックを考慮したニュース表現を学習するために、補助的なニューストピック予測タスクを用いている。
SentiRec [212] uses a news sentiment orientation score prediction task to learn sentiment-bearing newsrepresentations.
SentiRec [212]はニュースの感情方向スコア予測タスクを用いて、感情を含むニュース表現を学習する。
KRED [121] trains the model in various tasks including item recommendation, item-to-itemrecommendation, category classiication, popularity prediction and local news detection.
KRED [121]はアイテム推薦、アイテム間推薦、カテゴリ分類、人気度予測、ローカルニュース検出など様々なタスクでモデルを学習する。
These methods canalso efectively encode additional information into the recommendation model without taking it as the input.However, it is usually non-trivial to balance the main recommendation task and the auxiliary tasks.
しかし，主推薦タスクと補助タスクのバランスをとることは，通常，容易ではない．

## 6.2. 6.2 Training Environment 6.2. 6.2 トレーニング環境

Existing researches mainly focus on the model training methods while ignoring the implementation environmentof model training, which is in fact important in developing real-world news recommender systems.
既存の研究では，主にモデル学習方法に焦点が当てられており，実際のニュース推薦システムの開発において重要であるモデル学習の実装環境は無視されている．
In manyexisting methods, the news recommendation models are oline trained on centrally stored data with centralizedcomputing resources [223].
しかし，このような環境は，実際のニュース推薦システムの開発において重要である．
This model training paradigm can help quick development of news recommendersystems, but it also has several main drawbacks.
このモデル学習パラダイムは，ニュース推薦システムの迅速な開発に役立つが，いくつかの主要な欠点もある．
First, user behavior data for model training is usually abundantand many recent news recommendation models are in large size [214], which require a large amount of computingresource to train accurate models.
まず，モデル学習のためのユーザ行動データは通常豊富であり，最近のニュース推薦モデルの多くはサイズが大きく[214]，正確なモデルを学習するためには大量の計算機資源が必要となる．
Although some recent works like [214] explore to train models in parallelon multiple GPUs, it is still insuicient to train huge models.
214]のように複数のGPUで並列にモデルを学習する研究もありますが、巨大なモデルを学習するにはまだ不十分です。
Thus, distributed model learning with properacceleration methods like data rearrangement and cache mechanisms may be required in industrial practice [224].Second, the model learned on oline data only may also have some mismatches with the characteristics ofrecommendation scenarios [244].
第二に、オンラインデータのみで学習したモデルは、レコメンデーションシナリオの特性とのミスマッチが発生する可能性がある[244]。
Moreover, the distribution of user interest and news topics may also evolve, andit is shown in previous research that the performance of oline trained models may decline with time [204].
さらに，ユーザの興味やニューストピックの分布は変化する可能性があり，Olineで学習したモデルの性能は時間とともに低下することが先行研究で示されている[204]．
Thus,instead of re-training models periodically, online model training on streaming data is needed.
このため，定期的にモデルを再トレーニングするのではなく，ストリーミングデータを用いたオンラインモデル学習が必要である．
Third, most existingnews recommendation methods are trained on centrally stored user data, which may have some privacy risksbecause user data usually contains private user information.
第三に，既存のニュース推薦手法の多くは，一元的に保存されたユーザデータを用いて学習しており，ユーザデータには通常ユーザの個人情報が含まれているため，プライバシー上のリスクが存在する可能性がある．
Several recent works like [158,159,231] explore totrain news recommendation models based on decentralized data with federated learning techniques, which canbetter protect user privacy in model training.
また，[158,159,231]のような最近の研究は，分散化されたデータに基づくニュース推薦モデルを連携学習技術で学習することを検討しており，モデル学習においてユーザのプライバシーをより良く保護することができる．

## 6.3. 6.3 Discussions on Model Training 6.3. 6.3 モデル学習に関する考察

Next, we provide some discussions on the model training techniques used in news recommendation methods.In some CF-based methods, news recommendation is modeled as a regression task where the ratings given byusers are regarded as prediction targets.
CFベースの手法では、ニュース推薦をユーザの評価を予測対象とした回帰タスクとしてモデル化するものがある。
However, on news platforms explicit user feedback such as rating isusually scarce, which poses great challenges to model training.
しかし、ニュースプラットフォームでは、通常、評価などの明示的なユーザフィードバックが少なく、モデル学習には大きな課題がある。
Therefore, most methods adopt implicit feedbackto construct training tasks.
そのため、多くの手法では暗黙的なフィードバックを用いて学習タスクを構築している。
Click feedback is one of the most widely used signals for model training because itcan implicitly indicate user interests in news and help the model optimize the CTR of recommendation results.However, click signals also have some gaps with the real user interests [232], and increasing CTR only may leadto recommending clickbait news to users, which is actually harmful to user experience.
しかし，クリックシグナルには実際のユーザの興味と異なる点があり[232]，CTRを上げるだけではクリックベイトニュースをユーザに推薦してしまい，ユーザ体験が損なわれてしまう可能性があるため，クリックフィードバックはモデル学習において最も広く用いられているシグナルの1つです．
Thus, a few methodsincorporating other user engagement signals such as dwell time and inish into model training, which can helplearn user engagement-aware recommendation model to improve user experience.
そのため，滞留時間や終了時間などの他のユーザエンゲージメントのシグナルをモデル学習に取り入れる手法もあり，ユーザエンゲージメントを考慮した推薦モデルを学習し，ユーザエクスペリエンスを向上させることができる．
Besides user feedback, somemethods also consider using additional news information as auxiliary prediction objectives.
また，ユーザからのフィードバックだけでなく，付加的なニュース情報を補助的な予測目標として利用する手法もある．
By jointly trainingthe model in both recommendation task and auxiliary tasks, the model can be aware of the additional newsinformation.
推薦タスクと補助タスクの両方でモデルを学習させることにより，モデルは付加的なニュース情報を認識することができる．
Since these methods do not take the additional features as the input, they can handle the scenarioswhere the additional features are unavailable.
これらの手法は付加的な特徴量を入力としないため、付加的な特徴量が利用できないシナリオにも対応することができる。
However, in multi-task learning based methods, it is diicult tochoose the proper coeicients for weighting the loss functions of diferent tasks, and these coeicients may alsobe sensitive to the dataset characteristics.
しかし，マルチタスク学習法では，各タスクの損失関数を重み付けするための適切な係数を選択することが難しく，また，これらの係数はデータセットの特徴に敏感である可能性がある．

Another important problem in model training is designing efective strategies for constructing labeled trainingsamples.
モデル学習におけるもう一つの重要な問題は、ラベル付き学習サンプルを作成するための効果的なストラテジーを設計することである。
In most methods the negative samples are randomly drawn from the entire news set or the impressionlist [218], which are further packed with the positive samples.
多くの手法では，ネガティブサンプルはニュースセット全体もしくはimpressionlist [218]からランダムに抽出され，さらにポジティブサンプルと一緒に詰め込まれます．
However, researchers have found that randomlyselected negative samples may be too easy for the model to distinguish, which is not beneicial for learningdiscriminative recommendation models [105].
しかし，ランダムに抽出されたネガティブサンプルはモデルにとって区別しやすく，識別可能な推薦モデルの学習には適さないことが分かっています[105]．
It is also an interesting problem to study the inluence of thenumber of negative samples on model training [208].
また，ネガティブサンプルの数がモデルの学習に与える影響も興味深い問題である[208]．

Besides, the environment for news recommendation model training is a less studied but important problem.Most researches are oline conducted by learning models on centralized data with centralized computing resources.As discussed in the previous section, this model training environment may pose many potential challenges like the limitation of centralized computing resources, the gaps between oline data and online applications, and theprivacy concerns and risks of centralized model training, which need to be extensively studied in the future.
また，ニュース推薦モデルの学習環境は，あまり研究されていないが重要な問題である．前節で述べたように，このモデル学習環境は，集中管理されたコンピューティングリソースで集中管理されたデータでモデルを学習することにより，オンライン上で行われている．

In summary, model training is critical for news recommendation while it still has much room for improvement,such as designing more efective training tasks, choosing more representative training samples, adaptivelytuning the loss coeicients for multi-task learning, and building more efective, eicient and privacy-preservingenvironment for news recommendation model training.
すなわち、より効果的な学習タスクの設計、より代表的な学習サンプルの選択、マルチタスク学習における損失係数の適応的調整、ニュース推薦モデル学習のためのより効果的、効率的かつプライバシー保護された環境の構築など、多くの改善の余地があることがわかった。

### 6.3.1. 6.3.1 A Bird’s-eye View on Recent Approaches. 6.3.1. 6.3.1 最近のアプローチに関する鳥瞰図。

To help readers better understand the details of recent newsrecommendation methods in terms of their news modeling, user modeling, ranking, and model training techniques,we illustrate a joint table that summarizes their details in these aspects.
最近のニュース推薦手法の詳細を、ニュースモデリング、ユーザモデリング、ランキング、モデル学習技術の観点から理解するために、それらの詳細をまとめた結合表を図示する。
Due to the limitation of page sizes, we do notinclude it in the main content, and readers can refer to it in a public repository (https:
ページ数の制限から本文には含まず、読者は公開リポジトリ（https.org）で参照することができる。

# 7. 7 EVALUATION METRICS 7. 7 評価指標

There are many metrics to quantitatively evaluate the performance of news recommender systems.
ニュース推薦システムの性能を定量的に評価するための指標は数多く存在する．
Most metricsaim to measure the recommendation performance in terms of the ranking relevance.
多くのメトリクスは推薦性能をランキングの関連性という観点で測定することを目的としている．

## 7.1. 推薦を分類問題として捉えるケース

For methods that regard thetask of news recommendation as a classiication problem, the Area Under Curve (AUC) score is a widely usedmetric, which is formulated as follows:
ニュース推薦を分類問題と捉える手法では，AUC (Area Under Curve) スコアが広く用いられており，以下のように定式化されている．

$$
AUC=\frac{
    |{ (i,j)|\text{Rank}(p_i) \geq \text{Rank}(n_j) }|
}{N_p N_n}  \tag{1}
$$

where $N_p$ and $N_n$ the numbers of positive and negative samples, respectively.
ここで、$N_p$と$N_n$はそれぞれ陽性と陰性サンプルの数である。
$p_i$ is the predicted score of the i-th positive sample and $n_j$ is the score of the j-th negative sample.
p_i$はi番目の陽性サンプルの予測スコアで、$n_j$はj番目の陰性サンプルのスコアである。
Another set of popular metrics are precision,recall and F1 scores, which are computed as:
もう一つの一般的な指標は、精度、再現性、F1スコアであり、これらは以下のように計算される。

$$
\text{Precision} = \frac{TP}{TP + FP} \tag*{2}
$$

$$
\text{Recall} = \frac{TP}{TP + FN} \tag*{3}
$$

$$
\text{F1} = \frac{2 * \text{Precision} * \text{Recall}}{\text{Precision} + \text{Recall}} \tag*{4}
$$

where TP, FP and FN respectively denote true positive, false positive and false negative.
ここで、TP、FP、FNはそれぞれ真陽性、偽陽性、偽陰性を表す。

## 7.2. 回帰タスクとしてモデル化する場合

For methods that model news recommendation as a regression task (e.g., predict the ratings of news), severalcommon metrics for regression such as mean absolute error (MAE), mean squared error (MSE), rooted meansquared error (RMSE) and Pearson correlation coeicient (PCC) are used to indicate the recommendationperformance, which are respectively formulated as follows:
ニュース推薦を**回帰タスクとしてモデル化する**手法（例：ニュースの視聴率予測）では、推薦性能を示す指標として、平均絶対誤差（MAE）、平均2乗誤差（MSE）、ルート付き平均2乗誤差（RMSE）、ピアソン相関係数（PCC）など、回帰に関する一般的な指標が用いられ、それぞれ次のように定式化されている。

$$
MAE = hoghoge \tag*{5}
$$

$$
MSE = hogehoge \tag*{6}
$$

$$
RMSE = hoge \tag*{7}
$$

$$
PCC = hoge \tag*{8}
$$

where $r_i$ and $p_i$ are the real and predicted ratings of the i-th sample, ̄r and ̄p respectively denote the arithmeticmean of the real and predicted ratings, and $\sigma$ is the standard deviation.
ここで、$r_i$と$p_i$はi番目のサンプルの実評価と予測評価、̄rと̄pはそれぞれ実評価と予測評価の算術平均、$sigma$は標準偏差を表している。

## 7.3. ニュース推薦をランキングタスクとみなす場合

For methods that regard news recommendation as a ranking task, besides the AUC metric there are also severalother metrics such as Average Precision (AP), Hit Ratio (HR), Mean Reciprocal Rank (MRR) and normalizedDiscounted Cummulative Gain (nDCG).
**ニュース推薦をランキングタスクとみなす手法**では、AUCの他に、平均精度（AP）、ヒット率（HR）、平均逆ランク（MRR）、正規化割引累積利益（nDCG）などの指標もある。
Note that these metrics may be applied to the top K recommendationlists, e.g., HR@K and nDCG@K.
これらの指標は**上位K個の推薦リスト、例えばHR@KやnDCG@Kに適用する**ことができることに注意されたい。
These metrics are respectively formulated as follows:
これらの指標はそれぞれ以下のように定式化される。

$$
AP = hoge \tag*{9}
$$

$$
HR@K = hoge \tag*{10}
$$

$$
MRR = hoge \tag*{11}
$$

$$
nDCG@K = hoge \tag*{12}
$$

where $r_i$ is a relevance score of news with the i-th rank, which is 1 for clicked news and 0 for non-clicked news.There are several other metrics such as Click-Through Rate (CTR) and dwell time, which can be only used tomeasure the performance of online news recommenders.
ここで，$r_i$はi番目のランクのニュースの関連性スコアであり，クリックされたニュースでは1，クリックされていないニュースでは0となる。クリックスルー率（CTR）や滞在時間など，オンラインニュース推薦者の性能を測定するためにのみ使用できる他のいくつかのメトリックが存在する。

## 7.4. 多様性のMetrics

Besides the metrics for measuring ranking accuracy, there are several other objective or subjective metricsto evaluate news recommender systems in other aspects.
ランキングの正確さを測る指標以外にも，ニュース推薦システムを他の側面から評価するための客観的・主観的な指標がいくつかある．
In [47] the recommendation results are evaluated by **novelty**, which is subjectively judged by a group of human subjects by rating the news sets from most novel to leastnovel.
47]では，推薦結果をノベルティで評価している．ノベルティは，人間の被験者によって，最も新しいニュースから最も新しくないニュースまで評価され，主観的に判断されるものである．
In FeedRec [215], the recommendation results are further evaluated by a set of user engagement-relatedmetrics, such as the average dwell time, inish ratio, dislike ratio and share ratio of the top ranked news.
FeedRec [215]では，推薦結果はさらに，上位にランクされたニュースの平均滞在時間，嫌いな人の割合，共有率などのユーザエンゲージメントの指標によって評価される．
Thesemetrics can help comprehensively evaluate the performance of news recommender systems and further improveuser experience.
これらの指標は，ニュース推薦システムのパフォーマンスを総合的に評価し，ユーザ体験をさらに向上させるのに役立つ．
A few methods also measure the diversity of recommendation results in diferent aspects.
また，**推薦結果の多様性**をさまざまな側面から測定する手法もいくつかある．
Forexample, in [244], an Intra-List Similarity (ILS) function is used to measure the diversity of recommendationresults.
例えば，[244]では，**リスト内類似度（Intra-List Similarity: ILS）関数**を用いて推薦結果の多様性を測定している．
More speciically, given a ranking list $L$, its ILS score is calculated as follows:
具体的には，ランキングリスト$L$が与えられたとき，そのILSスコアは次のように計算される．

$$
\text{ILS}(L) = \frac{
    \sum_{b_j \in L} \sum_{b_j \in L, b_j \neq b_i} S(b_i, b_j)
}{
    \sum_{b_j \in L, b_j \neq b_i} 1
}
\tag*{13}
$$

where $S(b_i,b_j)$ represents the cosine similarity between the item $b_i$ and $b_j$.
ここで $S(b_i,b_j)$ はアイテム $b_i$ と $b_j$ の**コサイン類似度**を表す。
A similar diversity metric ILAD is alsoused in [157,160].
類似の多様性指標ILADは[157,160]で言及されている。
SentiRec [212] uses **a set of sentiment diversity metrics** to measure the sentiment diferencebetween historical clicked news and candidate news, which are formulated as follows:
SentiRec [212]では、過去のクリックニュースと候補ニュースとの間の**センチメント(＝感情?)**の相違を測定するために、以下のように定式化された**一連のセンチメント多様性指標**を用いている。

$$
\text{Senti}_{MRR} = \max(0, \bar{s} \sum_{i=1}^N \frac{s_i^c}{i}) \\
\text{Senti}@5 = \max(0, \bar{s} \sum_{i=1}^5 \frac{s_i^c}{i}) \\
\text{Senti}@10 = \max(0, \bar{s} \sum_{i=1}^10 \frac{s_i^c}{i}) \\
\tag*{14}
$$

where N is the number of candidate news in an impression,$s_i^c$ denotes the sentiment score of the i-th ranked candidate news.
ここで、Nは印象の候補ニュースの数、$s_i^c$はi番目のランク付けされた候補ニュースのセンチメントスコアを表す。

### 7.4.1. 公平性のMetrics

Besides diversity, **several fairness metrics** are used to measure whether a news recommender system is fair todiferent groups of users or diferent news publishers.
また，ニュース推薦システムが異なるユーザグループやニュース出版社に対して公平であるかどうかを測定するために，多様性のほかにいくつかの**公平性測定基準**が用いられている．
For example, FairRec [221] uses the accuracy of sensitiveattribute (e.g., gender) prediction based on top recommendation results as the fairness metric, where a higheraccuracy means more serious unfairness because the recommendation results are more heavily inluenced bysensitive attributes.
例えば，FairRec [221]では，推薦結果の上位にある敏感属性（例えば，性別）の予測精度を公平性の指標として用いている．この指標では，推薦結果が敏感属性の影響をより強く受けるため，**精度が高いほど，より深刻な不公平を意味**する．
[57] studies the news recommendation fairness to diferent groups of authors.
また，[57]では，異なる著者グループに対するニュース推薦の公平性を研究している．
It uses anEquity Attention for group fairness (EAGF) measurement and a Supplier Popularity Deviation (SPD) measurementfor evaluating such kind of fairness, which if formulated as follows:
この研究では，このような公平性を評価するために，**EAGF (Equity Attention for Group Fairness) 計測**と **SPD (Supplier Popularity Deviation) 計測**を用いており，以下のように定式化されている．

$$
\text{EAGF} = \sum_{i=1}^{|g|} \sqrt{|L(i)|} \\
\text{SPD} = \frac{
    \sum_{i=1}^{|g|} |\frac{L(i)}{L} - \frac{A(i)}{A}|
}{|g|}
\tag*{15}
$$

where g is the set of author groups and $L(i)$ is the set of recommended news belonging to the i-th group,Lis theset of all recommended items, $A(i)$ is the set of items in the training set belonging to thei-th group, andAis thewhole set of items.
ここで、

- gは著者グループの集合、
- $L(i)$はi番目のグループに属する推薦ニュースの集合。Lは全ての推薦アイテムの集合
- $A(i)$はi番目のグループに属する学習セットのアイテムの集合、Aはアイテムの全体集合を表す。
  A higher EAGF and a lower SPD score indicate better fairness.
  **EAGFが高く、SPDが低いほど公平である**ことを示す。
  These metrics used in the twoworks can be used to measure user-side fairness and provider-side fairness, respectively.
  これらの指標は、**ユーザ側の公平性とプロバイダ側の公平性をそれぞれ測定する**ために用いることができる。

### 7.4.2. プライバシー保護の程度のMetrics

With the development of privacy-preserving news recommendation methods based on federated learning,a few measurements can be used to evaluate **the degree of privacy protection** in news recommendation.
連合学習に基づくプライバシー保護型ニュース推薦手法の開発に伴い，ニュース推薦におけるプライバシー保護の程度を評価するために，いくつかの測定方法を用いることができるようになった．
For example, in FedRec [158] the privacy protection ability of the model can be directly indicated by the privacybudget of model gradients.
例えば、FedRec [158] では、モデルのプライバシー保護能力は、モデルの勾配のプライバシーバジェットによって直接示すことができる。
In addition, privacy protection can also be measured by conducting membershipinference attack on user behavior histories to guess whether a behavior belongs to a target user [159].
また、ユーザの行動履歴に対してメンバーシップインファレンス攻撃を行い、ある行動がターゲットユーザに属するかどうかを推測することによっても、プライバシー保護能力を測定することができる[159]。
Thesemetrics can indicate whether private user information encoded in exchanged models results is well-protected.
これらの指標は、交換されたモデルの結果にエンコードされたプライベートなユーザ情報が適切に保護されているかどうかを示すことができる。

# 8. 8 DATASET, COMPETITION AND BENCHMARK 8. 8 データセット、コンペティション、ベンチマーク

Table 6.
表 6.
Comparisons of the five public datasets for news recommendation.
ニュース推薦のための5つの公開データセットの比較。

Many works in the news recommendation ield are based on proprietary datasets, such as those collected fromGoogle News [29], Yahoo’s news [144], Bing news [116] and MSN news [204].
ニュース推薦の分野では，Google News [29], Yahoo's news [144], Bing news [116], MSN news [204] などの独自のデータセットに基づいて研究が行われている．
There are only a few publiclyavailable datasets for the research on personalized news recommendation, which are respectively introduced asfollows.
個人化されたニュース推薦の研究において，一般に公開されているデータセットは数少なく，それぞれ以下のように紹介されている．

The irst one is the plista [91] dataset.
まず，plista [91] というデータセットがある．
It is constructed by collecting the 70,353 news articles from 13 Germannews portals as well as 1,095,323 news click logs of users.
これは、13のGermannewsポータルから70,353のニュース記事と、ユーザーの1,095,323のニュースクリックログを収集して構築されています。
In the CLEF 2017 NewsREEL task, the organizers publisha new version of the plista dataset, which records users’ interactions with news from eight publishers in February2016.
CLEF 2017 NewsREELタスクにおいて、主催者は2016年2月に8つの出版社からのニュースに対するユーザーのインタラクションを記録したplistaデータセットの新バージョンを公開しています。
This dataset contains 2 million notiications, 58 thousand news updates, and 168 million recommendationrequests.
このデータセットには、200万件の通知、5万8000件のニュース更新、1億6800万件の推薦要求が含まれています。
The language used in the plista datasets is German since it is mainly based on the news websites andusers in German speaking world.
このデータセットでは，主にドイツ語圏のニュースサイトとユーザを対象としているため，ドイツ語が使用されている．
Note that the number of users is not provided.
なお、ユーザー数は提供されていない。

The second one is the Adressa [61] dataset, which was constructed by collecting the news logs of the Adresseav-isen website in three months.
もう一つは，Adressa [61] データセットで，Adresseav-isen というウェブサイトのニュースログを3ヶ月分収集することによって構築されたものである．
It has a full version with logs in 10 weeks and a small version with logs in oneweek.
このデータセットには，10週間分のログを集めたフルバージョンと，1週間分のログを集めたスモールバージョンがある．
The small version contains 561,733 users, 11,207 articles and 2,286,835 clicks, and the full version contains3,083,438 users, 48,486 articles and 27,223,576 clicks.
小バージョンは561,733人、11,207記事、2,286,835クリックで、フルバージョンは3,083,438人、48,486記事、27,223,576クリックで構成されています。
The news articles in Adressa are written in Norwegian.
アドレッサに掲載されているニュース記事は、ノルウェー語で書かれています。

The third one is the Globo [31] dataset, which is retrieved from the Globo news portal in Brazil.
3つ目は，ブラジルのGloboニュースポータルから取得したGloboデータセット[31]である．
This datasetcontains about 314,000 users, 46,000 news articles and 3 million news clicks.
このデータセットには，約314,000人のユーザ，46,000のニュース記事，300万のニュースクリックが含まれる．
This dataset is in Portuguese, andthere is no original news text in this dataset, and it only provides the embeddings of words generated by a neuralmodel that is pre-trained in a news metadata classiication task.
このデータセットはポルトガル語であり，オリジナルのニューステキストは存在せず，ニュースのメタデータ分類タスクで事前に学習したニューラルモデルによって生成された単語の埋め込みのみが提供される．

The fourth one is a Yahoo!3dataset for session-based news recommendation.
4つ目は、セッションベースのニュース推薦のためのYahoo!3datasetである。
It contains 14,180 news articlesand 34,022 click events.
このデータセットには14,180のニュース記事と34,022のクリックイベントが含まれている。
In this dataset, no news text is provided and the number of users is also unknown becausethere is no information about user ID.
このデータセットでは、ニュースのテキストは提供されておらず、ユーザIDの情報もないため、ユーザ数は不明である。

The ifth one is the MIND [223]4dataset, which is a large-scale English dataset for news recommendation.This dataset is recently released by MSN News, which contains the real news logs of 1 million users in 6 weeks(from October 12 to November 22, 2019).
このデータセットはMSN Newsが最近公開したもので、6週間（2019年10月12日から11月22日）の100万ユーザーの実際のニュースログが含まれています。
It involves 161,013 news articles, 15,777,377 impressions and 24,155,470news clicks.
161,013件のニュース記事、15,777,377件のインプレッション、24,155,470件のニュースクリックが含まれています。

We present a comparison of the volume, textual information and leaderboard information of these datasets inTable 6.
表6に、これらのデータセットのボリューム、テキスト情報、リーダーボード情報を比較した結果を示す。
We can see that only the MIND dataset is associated with a public leaderboard.
MINDデータセットのみが、公開されたリーダーボードと関連付けられていることがわかる。
In fact, many researchesconducted on other datasets such as Adressa use diferent dataset preprocessing methods [70,248], making itdiicult to make head-to-head comparisons between the results reported in diferent papers.
実際、Adressaのような他のデータセットで行われた多くの研究は、異なるデータセットの前処理方法を使用しており[70,248]、異なる論文で報告された結果を正面から比較することは困難である。
On the contrary, onthe MIND dataset the training, validation and test samples are given, and the evaluation metrics are consistent.Thus, MIND can serve as a standard testbed for news recommendation research.
一方、MINDデータセットでは学習・検証・テストサンプルが与えられており、評価指標も一貫しているため、MINDはニュース推薦研究の標準的なテストベッドとなり得る。

Based on the datasets introduced above, several competitions and benchmarks on personalized news recom-mendation have been established.
上記で紹介したデータセットに基づき、パーソナライズドニュースレコメンデーションに関するいくつかのコンペティションやベンチマークが確立されている。
One representative one is the NEWSREEL challenge held from 2013 to 2017 (in2013 the challenge is named NRS).5There are usually two tasks in the NEWSREEL challenge.
その代表的なものが、2013年から2017年にかけて開催されたNEWSREELチャレンジ（2013年のチャレンジ名はNRS）5である。
The irst one isnews recommendation in a living lab, which are conducted on an operating news recommendation service.
NEWSREELチャレンジには通常2つのタスクがあり、1つ目はリビングラボにおけるニュース推薦で、これは稼働中のニュース推薦サービス上で実施されます。
Thegoal of recommendation algorithms in this task is achieving high news CTRs.
このタスクでは、推薦アルゴリズムが高いニュースCTRを達成することが目標とされます。
The second one is oline evaluationof news recommendation methods in a simulated environment.
2つ目は、シミュレーション環境におけるニュース推薦手法のオンライン評価である。
This task is performed based on the plista dataset,and the goal is to predict which news articles a visitor would read in the future.
このタスクはplistaデータセットに基づいて行われ、訪問者が将来どのニュース記事を読むかを予測することが目標である。
In the 2017 edition of NewsREEL87 participants are registered [92], and two systems achieved CTRs higher than 2% in the online evaluation task.
2017年版のNewsREELでは87人の参加者が登録されており[92]，オンライン評価タスクでは2つのシステムが2%以上のCTRを達成した．

Another recent competition is the MIND News Recommendation Competition6, which is conducted on theMIND dataset.
また，MIND データセットを用いて行われる MIND News Recommendation Competition6 も最近のコンペティションである．
The goal of this challenge is to predict the click scores of candidate news based on user interestsand rank candidate news in each impression.
このコンペティションの目的は、ユーザの興味に基づいて候補となるニュースのクリックスコアを予測し、各インプレッションにおいて候補となるニュースをランク付けすることである。
This challenge attracted more than 200 registered participantsand the top submission achieved 71.33% in terms of AUC.
このコンペティションでは，200 名以上の参加者が登録し，上位の参加者は AUC で 71.33%を達成した．
The leaderboard of this challenge opens after thechallenge, and researchers can submit their predictions on the test set to obtain the oicial evaluation scores.
このチャレンジのリーダーボードはチャレンジ終了後に公開され、研究者はテストセットで予測した結果を提出し、正式な評価スコアを得ることができます。
Thecurrent top result on this leaderboard is 73.04% in terms of AUC, which is achieved by a recommender namedłUniUM-Fastformer-Pretrain” based on the techniques in [214] and [219].
このリーダーボードでの現在のトップ結果は、AUCで73.04%であり、これは[214]と[219]の技術に基づいた "UniUM-Fastformer-Pretrain "という名前の推薦者によって達成されたものである。
The MIND dataset, challenge and thepublic leaderboard can form a good benchmark to facilitate research and engineering on personalized newsrecommendation.
MINDデータセット、チャレンジ、パブリックリーダーボードは、パーソナライズドニュースレコメンデーションに関する研究とエンジニアリングを促進するための良いベンチマークを形成することができます。

# 9. 9 RESPONSIBLE PERSONALIZED NEWS RECOMMENDATION 9. 9 責任あるパーソナライズド・ニュースレコメンデーション

Although personalized news recommendation techniques have achieved notable success in targeting user interest,they still have several issues that may afect user experience and even lead to potential negative social impacts.There are several critical problems in developing more responsible personalized news recommender systems,including privacy protection, debiasing and fairness, diversity, and content quality, which are discussed in thefollowing sections, respectively.
個人化されたニュース推薦技術は、ユーザの興味をターゲットにすることで顕著な成功を収めているが、ユーザ体験に影響を与え、さらには社会的な悪影響を及ぼす可能性のあるいくつかの問題が残っている。より責任ある個人化ニュース推薦システムの開発には、プライバシー保護、偏向性と公平性、多様性およびコンテンツの品質などのいくつかの重要問題があり、以下のセクションでそれぞれ議論する。

## 9.1. Privacy Protection 9.1. 9.1 プライバシー保護

Most existing personalized news recommender systems rely on centralized storage of users’ behavior data foruser modeling and model training.
既存のパーソナライズドニュースレコメンダーシステムの多くは，ユーザのモデリングやモデル学習のためにユーザの行動データを一元的に保存することに依存している．
However, user behaviors are usually privacy sensitive, and centrally storing them may lead to users’ privacy concerns and further risks on data leakage [115].
しかし，ユーザの行動は通常プライバシーに配慮したものであり，一元的に保存することは，ユーザのプライバシーへの懸念やデータ漏洩のさらなるリスクにつながる可能性がある[115]．
There are only a few works thatstudy the privacy preservation problem in news recommendation [32,158].
ニュース推薦におけるプライバシー保護問題を研究している研究は少ない[32,158]。
For example, FedRec [158] may bethe irst attempt to learning privacy-preserving news recommendation model.
例えば，FedRec[158]はプライバシーを保護したニュース推薦モデルを学習する最初の試みであろう．
Instead of collecting and storinguser behavior data in a central server, in FedRec users’ news click data are locally stored on user devices.
FedRec では，ユーザの行動データを中央サーバに収集・保存する代わりに，ユーザのニュースクリックデータをユーザの端末にローカルに保存する．
FedRecuses a federated learning based framework to collaboratively learn news recommendation model.
FedRecでは、協調学習を行うために、連合学習ベースのフレームワークを用いて、ニュース推薦モデルを学習する。
Each clientkeeps a local copy of the model and locally computes the model updates based on local data.
各クライアントはモデルのローカルコピーを保持し、ローカルデータに基づいてモデルの更新をローカルに計算する。
The local modelupdates are uploaded to a central server that coordinates a number of user clients for model training.
ローカルなモデル更新は中央サーバにアップロードされ、中央サーバは多数のユーザークライアントを連携してモデル学習を行う。
The serveraggregates the local gradients into a global one to update its maintained global model, and distributes the updatedglobal model to user devices for local update.
サーバは、ローカルな勾配をグローバルな勾配に集約し、維持されているグローバルモデルを更新し、更新されたグローバルモデルをユーザ機器に配布してローカルに更新させる。
In addition, to further protect user privacy, FedRec applies localdiferential privacy (LDP) techniques to perturb the local model gradients.
さらに、FedRecはユーザのプライバシーを保護するために、LDP（localdiferential privacy）技術を適用し、ローカルモデルの勾配を変化させる。
Since the protected model gradientsusually contain much less private information, user privacy can be better protected.
保護されたモデルの勾配は通常、個人情報をあまり含まないので、ユーザーのプライバシーをより保護することができます。
However, FedRec is only aframework for privacy-preserving news recommendation model training, and privacy-preserving online servingis still a challenging problem.
しかし、FedRecはプライバシー保護されたニュース推薦モデル学習のためのフレームワークに過ぎず、プライバシー保護されたオンライン配信はまだ挑戦的な問題である。

Uni-FedRec [159] is an improved version of FedRec that considers both privacy-preserving training and serving.It has a recall stage to generate dozens of candidates from the news pool in the server and a ranking stage tolocally rank candidate news.
Uni-FedRec[159]はFedRecの改良版で、プライバシーを保護した学習と配信の両方を考慮したものである。
In the recall stage, Uni-FedRec generates multiple user embeddings to better coveruser interest.
Uni-FedRecは想起段階において、ユーザの興味をよりよくカバーするために、複数のユーザ埋め込みを生成します。
Instead of sending the original user embedding learned by the user model, it decomposes eachuser embedding into a linear combination of several basis user embeddings, and the combination weights areprotected by LDP before sending to the server.
ユーザーモデルで学習したオリジナルのユーザー埋め込みを送信する代わりに、各ユーザー埋め込みを複数の基底ユーザー埋め込みの線形結合に分解し、その結合重みをLDPで保護した上でサーバに送信します。
The server reconstructs user embeddings to retrieve candidatenews and send them to clients for local ranking.
サーバはユーザ埋め込みを再構成して候補となるニュースを取得し、クライアントに送信してローカルランキングを行う。
This framework can be used for both model training andserving in a privacy preserving way.
このフレームワークは、モデルの学習とプライバシー保護された方法でのサービスの両方に使用できる。
However, there are still considerable communication costs in this framework.Eicient-FedRec [231] further studies how to reduce the communication costs of federated news recommendationmodel learning.
Eicient-FedRec [231]はさらに、連合ニュース推薦モデル学習の通信コストを削減する方法を研究している。
It decomposes the whole model into a heavy news model and a light-weight user model, wherethe news model is placed on the server while the user model is kept by clients.
Eicient-FedRec [231]はさらに、連合ニュース推薦モデル学習の通信コストを削減する方法を研究している。これは、モデル全体を、重いニュースモデルと軽いユーザモデルに分解し、ニュースモデルはサーバに置き、ユーザモデルはクライアントが保持するものである。
The hidden news representationsinferred by the news model on the server are distributed to clients in the model training.
このモデルでは，サーバ上のニュースモデルから推論される隠れたニュース表現が，モデル学習においてクライアントに配布される．
This method providesthe potential of incorporating big models such as BERT in federated news recommendation.
この方法は、BERTのような大規模モデルを連携型ニュース推薦に取り込む可能性を提供する。

Although existing works on privacy-preserving news recommendation have made notable progresses, there arestill many challenges in this ield, such as the huge performance sacriice of diferential privacy mechanism, thediiculty of involving some context features (e.g., CTR) and collaborative information in GNN, and the diicultyof real-world deployment of federated news recommender systems.
プライバシー保護型ニュース推薦に関する既存の研究は注目に値する進歩を遂げているが，この分野にはまだ多くの課題がある．例えば，差分プライバシー機構による性能の大きな犠牲，GNNにおける文脈特徴（例えば，CTR）と協調情報の関与の難しさ，連合ニュース推薦システムの実世界への展開の難しさである．

## 9.2. 9.2 Debiasing 9.2. 9.2 デビアス

User behavior data usually encodes various kinds of biases.
ユーザーの行動データには、通常、様々な種類のバイアスが含まれています。
Some kinds of biases are related to news.
この中には，ニュースに関連したバイアスもある．
For example,click behaviors are inluenced by the positions and sizes of news displayed on the webpages (i.e., presentationbias) [230].
たとえば，クリック行動は，ウェブページに表示されるニュースの位置やサイズに影響される（プレゼンテーション・バイアス）[230]．
In addition, popular news may have higher chances to be clicked than unpopular news (i.e., popularitybias) [157].
また，人気のあるニュースは，人気のないニュースよりクリックされる確率が高い（すなわち，人気バイアス）[157]．
These types of bias information may afect the accuracy of user interest modeling and model training.A few works explore to eliminate the inluence of certain kinds of bias information to improve personalized newsrecommendation.
このような偏り情報は，ユーザの興味・関心のモデル化およびモデル学習の精度に影響を与える可能性があります．
For instance, DebiasRec [230] aims to reduce the inluence of position and size biases on newsrecommendation.
例えば，DebiasRec [230]は，位置とサイズのバイアスがニュースレコメンデーションに与える影響を低減することを目的としている．
It uses a bias-aware user modeling method to learn debiased user interest representations,and uses a bias-aware click prediction method that decomposes the overall click score into a bias score and abias-independent user preference score.
DebiasRec [230]は，バイアスを考慮したユーザモデリング手法により，バイアスを考慮したユーザの興味表現を学習し，バイアスを考慮したクリック予測手法により，クリックスコア全体をバイアススコアとバイアス非依存のユーザプレファレンススコアに分解している．
PP-Rec [157] uses a popularity-aware user modeling method to learncalibrated user interest representations, and it separately models the popularity of news and users’ personalpreference on news, which can help better model personalized user interest.
PP-Rec [157]は，人気度考慮ユーザモデリング法を用いて，較正されたユーザインタレスト表現を学習し，ニュースの人気度とユーザのニュースに対する個人的嗜好を別々にモデル化し，個人化されたユーザインタレストをよりよくモデル化するのに役立つとする．
These methods mainly aim toinfer debiased user interest from biased user data.
これらの手法は、主に偏ったユーザデータから偏ったユーザインタレストを推定することを目的としている。
However, without any prior knowledge about unbiased datadistribution, the bias information usually cannot be fully eliminated.
しかし，偏りのないデータ分布に関する予備知識がない場合，通常，偏り情報を完全に除去することはできない．
In addition, many kinds of bias such as exposure and selection biases are rarely studied in the news recommendation ield.
また，ニュース推薦の分野では，暴露バイアスや選択バイアスなどの多くの種類のバイアスがほとんど研究されていない．
Thus, it is important forfuture research to understand how diferent biases afect user behaviors and the recommendation model as wellas how to eliminate their efect in model training and evaluation.
このように，様々なバイアスがユーザの行動や推薦モデルにどのような影響を与えるのか，また，モデルの学習や評価においてどのようにバイアスの影響を排除するのかを理解することは，今後の研究において重要である．

## 9.3. 9.3 Fairness 9.3. 9.3 公平性

Making fair recommendations is an important problem in responsible news recommendation.
公正な推薦を行うことは，責任あるニュース推薦を行う上で重要な問題である．
Researchers havestudied various kinds of fairness problems in recommendation, such as provider-side fairness and consumer-sidefairness [12].
この問題には，提供者サイドの公平性，消費者サイドの公平性など，さまざまな種類がある [12] ．
In personalized news recommendation, a representative kind of unfairness is brought by the biasesrelated to sensitive user attributes, such as genders and professions.
個人化されたニュース推薦において，代表的な不公正性は，性別や職業などの敏感なユーザ属性に関連するバイアスによってもたらされる．
Users with the same sensitive attributesmay have similar patterns in news click behaviors, e.g., fashion news are more preferred by female users.
例えば，ファッション系のニュースは女性ユーザに好まれるなど，同じ属性を持つユーザは，ニュースのクリック行動において類似のパターンを持つ可能性がある．
Themodel may capture these biases and produce biased recommendation results, e.g., tend to only recommendfashion news to female users.
このようなバイアスを考慮したモデルは、例えば、女性ユーザにはファッション系ニュースのみを推薦するような偏った推薦結果を生成する可能性があります。
This will lead to the unfairness problem that some users cannot obtain theirinterested news information, which is harmful to user experience.
これは，一部のユーザが自分の興味あるニュース情報を取得できないという不公平な問題を引き起こし，ユーザエクスペリエンスを損ねることになります．
To address this problem, FairRec [221] uses adecomposed adversarial learning framework with independent user models to learn a bias-aware user embeddingand a bias-free user embedding.
この問題に対処するため，FairRec [221]では，独立したユーザモデルを用いた非構成的な敵対学習の枠組を用いて，偏りを考慮したユーザ埋め込みと偏りのないユーザ埋め込みを学習する．
The bias-aware user embedding mainly aims to capture bias information relatedto sensitive user attributes, and the bias-free user embedding aims to model bias-independent user interest.Both embeddings are regularized to be orthogonal thereby the bias-free user embedding can contain less biasinformation.
両埋め込みは直交するように正則化され，これによりBias-free User Embdingはより少ない偏り情報を含むことができる．
The bias-free user embedding is further used for making fair news recommendations.
さらに、偏りのないユーザ埋め込みは、公正なニュース推薦を行うために用いられる。
By learninguser embeddings that are agnostic to the sensitive user attributes, the unfairness brought by the bias informationrelated to sensitive user attributes can be efectively mitigated.
ユーザ属性に依存しないユーザ埋め込みを学習することで、ユーザ属性に関連するバイアス情報がもたらす不公正性を効果的に緩和することができる。
However, adversarial learning based methods areusually brittle and it is diicult to tune their hyperparameters to fully remove the bias information.
しかし、敵対的学習法は通常脆弱であり、バイアス情報を完全に除去するためにハイパーパラメータを調整することは困難である。
In addition,many other genres of fairness (e.g., provider-side fairness) are less studied in news recommendation.
また、他の多くの公平性のジャンル（例えば、提供者側の公平性）は、ニュース推薦においてあまり研究されていない。
In summary,there are many types of fairness to be improved in news recommendation and it is non-trivial to make both fairand accurate news recommendations.
このように，ニュース推薦において改善すべき公平性は数多く存在し，公平かつ正確なニュース推薦を行うことは自明でない．

## 9.4. 9.4 Diversity 9.4. 9.4 多様性

Diversity is critical for personalized news recommendation [124,155,169].
パーソナライズド・ニュースの推薦には，多様性が重要である [124,155,169]．
Users may not prefer to click news withhomogeneous information and improving the information variety is important for improving user experience andengagement [6].
しかし，既存のニュース推薦手法の多くは，推薦の多様性を無視して推薦精度を最適化することに主眼を置いており，推薦の多様性を向上させることは，ユーザ体験とエンゲージメントを向上させるために重要である[6]．
However, most existing news recommendation methods focus on optimizing recommendationaccuracy while ignoring recommendation diversity, and it is shown in [157,160,212] that many existing newsrecommendation methods cannot make suiciently diverse recommendations.
しかし，既存のニュース推薦手法の多くは，推薦の多様性を無視して推薦精度の最適化に注力しており，既存のニュース推薦手法の多くが十分に多様な推薦を行うことができないことが[157,160,212]で示されている．
There are only a few methods thatconsider the diversity of news recommendation.
また，推薦の多様性を考慮した手法は数少ない．
Some methods aim to recommend news that are diverse frompreviously clicked news [47,212], and several other works explore to diversify the top news recommendationlist [46,109].
また，トップニュースの推薦リストを多様化することを目的とした研究もある[46,109]．
However, there is still no work on promoting both kinds of diversity in news recommendation.In addition, many diversity-aware news recommendation methods rely on reranking strategies to improverecommendation diversity, which may not be optimal for achieving a good tradeof between recommendationaccuracy and diversity.
また，多様性を考慮したニュース推薦手法の多くは，推薦の多様性を向上させるために再ランク付け戦略に依存しており，推薦精度と多様性の良好なトレードオフを達成するためには最適でない可能性がある．
Thus, further research on learning uniied diversity-aware news recommendation modelsis important for improving the quality of online news services.
また，多様性を考慮した推薦手法の多くは，推薦の多様性を向上させるために再ランク付けを行うが，推薦の多様性と推薦の精度を両立させるためには最適な手法ではない可能性がある．

## 9.5. 9.5 Content Moderation 9.5. 9.5 コンテンツの適正化

The moderation of news content in news recommendation is a rarely studied problem.
ニュース推薦におけるニュース内容の適正化については、ほとんど研究されていない問題である。
In fact, some newsarticles published online are clickbaits, fake news or containing misinformation.
実際，オンライン上で公開されているニュースの中には，クリックベイト，フェイクニュース，誤報を含むものがある．
In addition, some news mayencode adversarial clues [33] or contain low-quality or even harmful content (e.g., racialism and hate speech).Recommending these news will damage user experience and the reputation of news platforms, and may evenlead to negative societal impact [101].
さらに，一部のニュースは敵対的な手がかりを含んでいたり[33]，低品質あるいは有害なコンテンツ（例えば，人種差別やヘイトスピーチ）を含んでいる場合があります．これらのニュースを推薦すると，ユーザ体験とニュースプラットフォームの評判が低下し，社会的に悪影響を与える可能性さえあります[101]．
Although online news platforms can perform manual moderation on news content quality, the huge amount of online news information makes it too diicult or even impossible to ilter allnews articles with harmful and useless content.
オンライン・ニュース・プラットフォームは、ニュース・コンテンツの品質について手動でモデレーションを行うことができますが、オンライン・ニュース情報が膨大であるため、有害で役に立たないコンテンツを含むすべてのニュース記事を削除することは困難であり、不可能であるとさえ言えます。
Thus, it is important to design news recommendation algorithmsthat can avoid recommending news with low-quality content.
そのため、低品質のニュースを推薦しないようなニュース推薦アルゴリズムを設計することが重要である。
Researchers have found that news with high ratiosof short reading dwell time (e.g., less than 10 seconds) are probably clickbaits [209].
研究者は，短い読書時間（例えば，10秒未満）の割合が高いニュースは，おそらくクリックベイトであることを発見しています[209]．
In addition, user behaviorssuch as comments and sharing on social media may also provide rich clues for detecting news that containmisinformation and harmful content [4,177].
さらに，ソーシャルメディア上のコメントや共有などのユーザ行動も，誤った情報や有害なコンテンツを含むニュースを検出するための豊富な手がかりを提供する可能性があります[4,177]．
Thus, incorporating the various user feedback has the potential tohelp recommend news with high-quality content, which can improve the responsibility of news recommendationalgorithms.
このように，様々なユーザのフィードバックを取り入れることで，質の高いコンテンツを含むニュースを推薦できる可能性があり，ニュース推薦アルゴリズムの責任を向上させることができる．

# 10. 10 FUTURE DIRECTION AND CONCLUSION 10. 10 今後の方向性と結論

## 10.1. 10.1 Deep News Understanding 10.1. 10.1 ディープニュースの理解

News modeling is at the heart of personalized news recommendation.
ニュースモデリングはパーソナライズドニュースの推薦の中核をなすものである。
It can be improved in the following aspects.First, text understanding is a core problem in news modeling, and existing methods may not be capable ofunderstanding the textual content of news deeply.
まず、テキスト理解はニュースモデリングの核となる問題であり、既存の手法ではニュースのテキスト内容を深く理解することができない可能性がある。
Thus, using more advanced NLP techniques (e.g., knowledge-aware PLMs) may help better understand news texts and improve news modeling.
そのため、より高度な自然言語処理技術（例えば、知識認識型PLM）を用いることで、ニュースのテキストをより深く理解し、ニュースのモデリングを改善することができるかもしれない。
Second, besides textualinformation, news also contain rich multimodal information such as images, videos and slides.
第二に、テキスト情報だけでなく、画像、ビデオ、スライドなどのマルチモーダルな情報も含まれている。
The multimodalnews content can provide complementary information on news understanding.
このようなマルチモーダルなニュースコンテンツは、ニュース理解のための補完的な情報を提供することができる。
Thus, using multimodal contentmodeling techniques has the potential to improve the comprehensiveness of news understanding.
したがって、マルチモーダルコンテンツモデリング技術を使用すると、ニュース理解の包括性を向上させることができる可能性がある。
Third, thereare many useful factors for news modeling that are not covered by news content, such as publisher, popularityand recency.
第三に、ニュースのモデル化には、出版社、人気度、再現性など、ニュース内容ではカバーしきれない多くの有用な要因がある。
A uniied framework is required to incorporate various kinds of news information (e.g., propertyfeatures and context features) and meanwhile efectively model the relatedness between diferent features.
このため、様々な種類のニュース情報（例えば、特性特徴や文脈特徴）を取り込み、異なる特徴間の関連性を効果的にモデル化する統一的な枠組みが必要である。
Furtherresearch on these directions can help understand news more accurately and deeply to empower subsequent usermodeling and news ranking.
このような研究を進めることで、より正確かつ深くニュースを理解し、その後のユーザモデリングやニュースランキングに役立てることができる。

## 10.2. 10.2 Universal User Modeling 10.2. 10.2 ユニバーサルユーザーモデリング

User modeling is critical for understanding users’ interest in news.
ニュースに対するユーザの興味・関心を理解するためには，ユーザのモデリングが重要である．
However, it is diicult to model the dynamic anddiverse user interest accurately and comprehensively for news recommendation.
しかし，ダイナミックで多様なユーザの興味・関心を正確にかつ包括的にモデル化することは，ニュース推薦のためには困難である．
To tackle this problem, a universaluser modeling framework that can model various kinds of user interest is needed.
この問題を解決するためには、多様なユーザインタレストをモデル化できるユニバーサルユーザモデリングフレームワークが必要である。
We argue that this frameworkshould satisfy the following requirements.
このフレームワークは、以下の要件を満たす必要があると考える。
First, the user modeling framework needs to comprehensively inferuser interest from multiple kinds of user behaviors and feedback.
まず、ユーザーモデリングフレームワークは、複数種類のユーザーの行動やフィードバックからユーザーの興味を包括的に推論する必要がある。
This is because click behaviors are very noisyand may be sparse for some users, and it is insuicient to model user interests solely from click behaviors.Fortunately, diferent kinds of user behaviors and feedback (e.g., read and dislike) can provide rich complementaryinformation like user engagement, and incorporating them in a uniied framework can better support usermodeling.
幸いなことに、様々な種類のユーザ行動とフィードバック（例えば、読むと嫌いになる）は、ユーザエンゲージメントのような豊富な補完的情報を提供することができ、それらを統一的なフレームワークに組み込むことにより、ユーザモデリングをより良くサポートすることができる。
Second, the framework needs to model the diverse and multi-grained user interest.
第二に、フレームワークは多様で多粒度のユーザインタレストをモデル化する必要がある。
Since a single userembedding may be insuicient to comprehensively model user interests, it may be a promising way to representuser interest with more sophisticated structures such as embedding sets and graphs to improve the understandingof user interest.
ユーザインタフェースを包括的にモデル化するためには、単一のuserembeddingでは不十分な場合があるため、埋め込みセットやグラフなど、より洗練された構造でユーザインタフェースを表現することが、ユーザインタフェースの理解を深める有力な方法となる可能性がある。
Third, the framework needs to capture the dynamics of user interests.
第三に、フレームワークはユーザの興味のダイナミクスを捉える必要がある。
Since user interest usuallyevolves with time, it is important to understand user interest in diferent periods and further model their inherentrelations.
ユーザーの興味は時間とともに変化するため、異なる時期のユーザーの興味を理解し、さらにその固有の関係をモデル化することが重要である。
To meet this end, using more advanced sequence modeling techniques may help improve user interestmodeling in personalized news recommendation.
このため、より高度なシーケンスモデリング技術を用いることで、パーソナライズドニュースの推薦におけるユーザの興味・関心のモデリングを改善できる可能性がある。

## 10.3. 10.3 Efective and Eficient Personalized Ranking 10.3. 10.3 効果的・効率的なパーソナライズドランキング

News ranking is an essential step to make personalized news recommendations.
ニュースランキングは、パーソナライズされたニュース推薦を行うために不可欠なステップである。
There are mainly three researchdirections to improve news ranking.
ニュースランキングを改善するために、主に3つの研究方向がある。
First, most existing personalized ranking methods are mainly based thecoarse-grained relevance between candidate news and user interest, which may not be optimal for accuratelytargeting user interest.
まず、既存のパーソナライズドランキング手法のほとんどは、主に候補ニュースとユーザーの関心の間の粗い粒度の関連性に基づいており、これはユーザーの関心を正確にターゲットにするために最適ではない可能性があります。
Although a few methods can model the ine-grained relatedness between user and news,they are ineicient and may not be suitable for scenarios with limited computation resources and latency tolerance.Thus, developing both efective and eicient personalized ranking methods is important for improving onlinenews recommendation.
また，ユーザとニュースの細かい関連性をモデル化できる手法もあるが，効率が悪く，計算資源や遅延耐性が限られたシナリオには適さない．したがって，オンラインニュース推薦を改善するには，効果的で効率の良いパーソナライズドランキング手法を開発することが重要である．
Second, ranking news solely based on relevance may lead to the ilter bubble problem.
第二に、関連性のみに基づいてニュースをランク付けすることは、イルターバブルの問題を引き起こす可能性がある。
It isimportant to design more sophisticated news ranking strategies to achieve a good tradeof between accuracy anddiversity.
このため，精度と多様性のトレードオフを実現するために，より洗練されたニュースランキング戦略を設計することが重要である．
Third, most existing news ranking methods are greedy, i.e., only consider the current ranking list in theranking policy.
第三に，既存のニュースランキング手法のほとんどは貪欲であり，ランキング政策において現在のランキングリストのみを考慮する．
However, they may not be optimal for achieving good user engagement in the long-term.
しかし、長期的に良好なユーザーエンゲージメントを達成するためには、最適とは言えないかもしれない。
Thus,designing proper news ranking strategies to optimize long-term rewards may be beneicial for user experience.
したがって、長期的な報酬を最適化するための適切なニュースランキング戦略を設計することは、ユーザー体験にとって有益であると考えられる。

## 10.4. 10.4 Hyperbolic Representation Learning for News Recommendation 10.4. 10.4 ニュース推薦のための双曲線表現学習

In most existing news recommendation methods, news and users representations are learned in Euclidean space.Matching functions such as inner product and cosine similarity are widely used for computing relevance scoresfor news ranking.
既存のニュース推薦手法の多くは，ニュースやユーザの表現をユークリッド空間で学習し，内積や余弦類似度などのマッチング関数がニュースランキングの関連性スコアを計算するために広く利用されている．
However, representation learning in Euclidean space is inefective in capturing the hierarchicalstructure of data, while hyperbolic representation learning is much better at it.
しかし、ユークリッド空間での表現学習は、データの階層的な構造を捉えることができない。
There are many inherent hierarchi-cal data structures in personalized news recommendation, such as diferent levels of user interests, news topics,and commonsense knowledge encoded by knowledge graphs.
個人化されたニュース推薦には、ユーザの興味、ニューストピック、知識グラフでエンコードされた常識的知識など、多くの固有の階層的なデータ構造が存在する。
Thus, news recommendation with hyperbolicrepresentation learning may be a promising solution.
そのため、双曲表現学習によるニュース推薦が有望な解決策となる可能性がある。
There are several existing neural architectures in hyperbolicspace, such as hyperbolic attention [60] and hyperbolic GCN [20], which can serve as the core model componentsin news recommendation.
双曲空間には、双曲型注意[60]や双曲型GCN[20]などの既存の神経アーキテクチャがあり、これらはニュース推薦の中核となるモデルコンポーネントとして機能することが可能である。
In addition, there have been several successful applications of hyperbolic representationlearning to CF-based recommendation [184,194] and knowledge graph embedding [19,198], which can provideuseful guidance of collaborative signal modeling and knowledge exploitation in news recommendation.
さらに、双曲表現学習はCFベース推薦[184,194]や知識グラフ埋め込み[19,198]への応用に成功しており、ニュース推薦における協調信号モデリングと知識抽出の有用な指針を提供することが可能である。
Futureresearch on hyperbolic representation learning may create a new direction to overcome several drawbacks ofcurrent user
また，双曲線表現学習の今後の研究により，現在のユーザ推薦の欠点を克服する新たな方向性を見出すことができる．

## 10.5. Unified Model Training 10.5. ユニファイドモデルトレーニング

Model training techniques are also important for learning efective and robust personalized news recommendationmodels.
また，効果的で頑健な個人向けニュース推薦モデルを学習するためには，モデルの学習技術も重要である．
There are four potential directions for future works to improve model training.
モデル学習を改善するために、将来的に4つの方向性が考えられる。
First, most methods onlyuse click signals for model training, which may be inaccurate because click signals are usually noisy and biased.In addition, the supervision signals in speciic tasks may also be insuicient [220].
まず、ほとんどの手法はクリック信号のみをモデル学習に用いているが、クリック信号は通常ノイズやバイアスが多いため、不正確な場合がある。また、特定のタスクにおける監視信号も不十分な場合がある[220]。
Thus, a uniied frameworkto incorporate various kinds of supervised and self-supervised training signals and objectives for collaborativemodel learning can efectively improve the model quality.
したがって、協調モデル学習のために、様々な種類の教師付きおよび自己教師付き学習信号と目的を組み込むための統一的なフレームワークは、効果的にモデルの品質を向上させることができる。
Second, although several methods explore to usemulti-task learning frameworks to incorporate multiple objectives into model training, they need to manuallytune the loss coeicients of diferent tasks in model training, which usually require much human efort and maybe sensitive to the characteristics of datasets.
第二に、マルチタスク学習のフレームワークを用いて、複数の目的をモデル学習に組み込むことを試みる手法があるが、モデル学習において、異なるタスクの損失係数を手動で調整する必要があり、通常、多くの人間の労力を必要とし、データセットの特徴に影響を受ける可能性がある。
Thus, a self-adaptive multi-task learning framework to automaticallytune hyperparameters like loss coeicients can reduce the developing efort and improve the model generality.Third, many methods use randomly selected negative samples for model training, which may be noisy andless informative.
第三に、多くの手法ではモデル学習にランダムに選択された陰性サンプルを用いるが、これはノイズが多く情報量が少ない可能性がある。
Thus, using more efective negative sampling can help train more robust and accurate newsrecommendation models.
このため，より効果的なネガティブサンプリングを用いることで，より頑健で正確なニュース推薦モデルを学習することができる．
Fourth, oline trained models may have gaps with the online scenarios and may suferfrom the performance decline with time.
第四に、オンライン学習されたモデルは、オンラインシナリオとのギャップがあり、時間の経過とともに性能が低下する可能性がある。
Thus, it is important to incorporate both oline and online learningtechniques to help the model better adapt to the latest online serving requirements.
このため、オンラインとオンラインの両方の学習技術を取り入れ、モデルが最新のオンラインサービス要件にうまく適応できるようにすることが重要である。

## 10.6. News Recommendation in Social Context 10.6. 社会的文脈の中でのニュース推薦

On some news platforms, users may have social interactions with other users in many ways, such as leavingcomments, replies, and sharing to their social media blogs like Twitter.
ニュースプラットフォームでは，ユーザはコメントや返信を残したり，Twitterのようなソーシャルメディアブログで共有するなど，さまざまな方法で他のユーザと社会的な相互作用を行うことができます．
The social interactions among usersconcerning certain news can usually relect their opinions, preferences, and satisfaction on the recommendednews [200], which can provide rich complementary information to user modeling.
このように，あるニュースに関するユーザー間の社会的相互作用は，通常，推奨ニュースに対する彼らの意見，好み，満足度を反映することができ [200]，これはユーザーモデリングに豊富な補完情報を提供することができます．
In addition, users’ discussionsand dissemination behaviors can also help understand the content, quality and authenticity of news [177].
さらに、ユーザーの議論や発信行動は、ニュースの内容、品質、信憑性を理解するのに役立ちます[177]。
Besides,they can help recognize breaking news and adjust recommendation results accordingly [153].
さらに，ユーザはニュース速報を認識し，それに応じて推薦結果を調整することができる[153]．
Therefore, thesocial contexts of news recommendation play an important role.
したがって，ニュース推薦の社会的文脈は重要な役割を果たす．
However, they are usually neglected by newsrecommendation researches in recent years.
しかし，近年のニュース推薦の研究においては，社会的文脈は軽視されがちである．
In future researches, it is an interesting topic to study the impacts ofusers’ online social interactions on the accuracy, timeliness and quality of news personalization.
今後の研究において，ユーザのオンラインでの社会的相互作用がニュースのパーソナライゼーションの精度，適時性，品質に与える影響を研究することは興味深いトピックである．

## 10.7. Privacy-preserving News Recommendation 10.7. プライバシー保護されたニュースの推奨

In recent years, the ethical issues of intelligent systems have attracted much attention from both the academiaand public.
近年、知的システムの倫理的な問題が学界と社会から注目されている。
Developing more responsible news recommender systems can help better serve users of onlinenews services with smaller risks.
このような状況において，より責任あるニュース推薦システムを開発することは，より小さなリスクでオンラインニュースサービスのユーザにより良いサービスを提供することにつながる．
One important direction for improving the responsibility of personalized newsrecommendation is user privacy protection.
このため，個人化されたニュース推薦の責任感を向上させるための重要な方向性として，ユーザのプライバシー保護が挙げられる．
Although a few works like [158] explore to use federated learningtechniques to train news recommendation models in a privacy-preserving way, there are still many challenges indeveloping a privacy-preserving news recommender system.
158]のようないくつかの研究は、プライバシーを保護する方法でニュース推薦モデルを訓練するために連合学習技術を使用することを模索しているが、プライバシーを保護するニュース推薦システムの開発にはまだ多くの課題が残っている。
First, given a model learned in a federated way, it isstill challenging to deploy it online to serve users eiciently.
第一に、連合学習で学習したモデルをオンラインで展開し、ユーザに効率的にサービスを提供することはまだ困難である。
Second, there may also be potential privacy risksduring the training and serving of news recommendation models, and canonical diferential privacy techniquesusually lead to a heavy sacriice on model utility.
第二に、ニュース推薦モデルの学習と配信の間に潜在的なプライバシーリスクが存在する可能性があり、正規の差分プライバシー技術は通常、モデルの有用性を大きく犠牲にすることにつながる。
Third, the data isolation problem in federated learning frameworksettings makes it diicult to exploit some context features like CTR and collaborative information in GNN.
第三に、連合学習フレームワークにおけるデータ分離の問題は、GNNにおけるCTRや協調情報のようないくつかのコンテキスト特徴を利用することを難しくしている。
Thus,further researches on developing more efective, eicient and privacy-preserving news recommendation methodsare needed.
したがって，より効果的で効率的，かつプライバシーを保護したニュース推薦手法の開発に関するさらなる研究が必要である．

## 10.8. Secure and Robust News Recommendation 10.8. セキュアでロバストなニュースのススメ

Existing researches on news recommendation focus on building algorithms in a trusted environment.
ニュース推薦に関する既存の研究は、信頼できる環境下でのアルゴリズム構築に重点を置いている。
However,in real-world scenarios there may be various kinds of threats brought by malicious users and platforms.
しかし、現実の世界では、悪意のあるユーザやプラットフォームがもたらす様々な脅威が存在する可能性があります。
Forexample, existing news recommendation methods are vulnerable to poisoning attacks, which aim to promotecertain items, trigger certain backdoors, or degrade the recommender system performance.
例えば、既存のニュース推薦方式は、特定のアイテムを宣伝したり、特定のバックドアを起動したり、推薦システムの性能を低下させたりすることを目的としたポイズニング攻撃に弱いです。
In addition, newsrecommender systems may be sensitive to adversarial samples.
さらに，ニュース推薦システムは敵対的なサンプルに対して敏感である可能性がある．
When news recommender systems are trainedin the federated learning framework, the threats from the untrusted outside environment become even moreserious.
また、ニュース推薦システムが連合学習フレームワークで学習される場合、信頼されていない外部環境からの脅威はさらに深刻になる。
Unfortunately, although the security and robustness of personalized news recommender systems arecritical, researches on this problem are rather limited.
残念ながら，個人化されたニュース推薦システムの安全性と頑健性は非常に重要であるが，この問題に対する研究はかなり限られている．
Future studies on secure and robust news recommendationare important for the stability and reliability of online news platforms.
今後、オンラインニュースプラットフォームの安定性と信頼性を高めるために、安全で堅牢なニュース推薦に関する研究が重要である。

## 10.9. Diversity-aware News Recommendation 10.9. 多様性を考慮したニュースの推奨

Besides accuracy, diversity in news recommendation also has decisive inluence on user experience.
ニュース推薦の多様性は、正確性だけでなく、ユーザー体験にも決定的な影響を与える。
There arethree main research directions to improve the diversity of news recommendation.
ニュース推薦の多様性を向上させるために、主に3つの研究方向がある。
The irst one is temporal-spatialdiversity-aware news recommendation, which aims to recommend news that are diverse from each other andmeanwhile diverse from historical clicked news.
まず、時間的・空間的多様性を考慮したニュース推薦である。これは、互いに多様性のあるニュースを推薦し、同時に、過去にクリックされたニュースからも多様性のあるニュースを推薦することを目的としている。
This can help the recommendation results better satisfy users’preference on information variety.
これにより、推薦結果は、情報多様性に対するユーザの嗜好をよりよく満たすことができる。
The second one is personalizing the diversity in news recommendation.Diferent users may have diferent preferences on the tradeof between accuracy and diversity, and it maybe better to consider their personalized preference to improve user experience.
第二に、ニュース推薦の多様性をパーソナライズする。ユーザーによって、正確さと多様性のトレードオフに関する好みが異なるため、ユーザー体験を向上させるために、ユーザーの好みを考慮することが望ましい。
The third one is ine-graineddiversity, which aims to not only diversify the content and topic of news, but also many other factors like publishers, locations, opinions and emotions.
3つ目は、ニュースの内容やトピックだけでなく、出版社、場所、意見、感情など、他の多くの要素を多様化することを目的とした「粒状多様性」である。
It has the potential to make higher-quality diversity-aware newsrecommendations.
これは、より質の高い多様性を考慮したニュース推薦を行う可能性を持っている。

## 10.10. Bias-free News Recommendation 10.10. 偏りのないニュースの推奨

Debiasing is another important problem in improving the responsibility of news recommendation.
ニュース推薦の信頼性を向上させるために、偏向補正も重要な課題である。
The biasesencoded by user behavior data will propagate to the recommendation model and may further be ampliied inthe loops of recommendation.
ユーザの行動データから得られるバイアスは推薦モデルに伝わり，推薦のループの中でさらに増幅される可能性がある．
Thus, designing efective methods to eliminate the inluence of the various kindsof biases on recommendation results is important for making high-quality news recommendations.
このため，推薦結果に対する様々な種類のバイアスの影響を排除するための効果的な手法を設計することは，高品質なニュース推薦を行う上で重要である．
There areseveral potential research directions in this ield.
この分野ではいくつかの研究の方向性が考えられる。
First, it is important to understand the inluence of diferentkinds of biases on user behaviors and the recommendation model, which can help the subsequent debiasing.Second, diferent users may be inluenced by the same bias information in diferent ways, and considering thepersonalized preference of users on bias information can help better eliminate the efects of biases.
第一に，様々な種類のバイアスがユーザの行動や推薦モデルに与える影響を理解することが重要であり，その後のデバイアスに役立つ．第二に，同じバイアス情報でもユーザによって影響を受け方が異なるため，バイアス情報に対するユーザの個人的な好みを考慮することでバイアスの影響をより良く除去することができる．
Third, thereare various kinds of biases in news recommendation.
第三に、ニュース推薦には様々な種類のバイアスが存在する。
A uniied debiasing framework that can simultaneouslyreduce the efects of diferent biases can greatly improve the accuracy and robustness of news recommendationalgorithms.
このようなバイアスの影響を同時に低減することができる統一的なデバイシングフレームワークは、ニュース推薦アルゴリズムの精度と頑健性を大きく向上させることができる。

## 10.11. Fairness-aware News Recommendation 10.11. 公平性を考慮したニュース推薦

Fairness is an essential but often ignored factor in personalized news recommendation.
個人向けニュース推薦において，公平性は重要な要素であるが，しばしば無視される．
A fair news recommendersystem is required to provide fair recommendation services to diferent groups of users and give fair chancesto news from diferent providers to be recommended.
このため，公正なニュース推薦システムは，異なるユーザグループに対して公正な推薦サービスを提供し，異なるプロバイダからのニュースが推薦される機会を公平に与えることが要求される．
Future research on fair news recommendation can beconducted in the following three directions.
今後，公正なニュース推薦に関する研究は，次の3つの方向から行うことができる．
First, it is important to reduce the consumer-side unfairness relatedto sensitive user attributes.
第一に、センシティブなユーザ属性に関連する消費者側の不公正性を低減することが重要である。
Although adversarial learning techniques are mature solutions to this problem, theyare usually brittle and diicult to tune.
この問題に対して、敵対的学習技術は成熟した解決策であるが、通常、脆弱で調整が困難である。
Thus, more robust and efective methods are required to remove thebiases introduced by sensitive user attributes.
そのため、敏感なユーザー属性によってもたらされる偏りを取り除くには、より頑健で効果的な方法が必要とされる。
Second, diferent news providers and publishers are diverse intheir characteristics, such as topic preference and reputation.
第二に、異なるニュースプロバイダーや出版社は、トピックの嗜好や評判など、その特性も多様である。
Thus, it is non-trivial to properly balance therecommendation chances of news from diferent providers and publishers to achieve better provider-side fairness.Third, there are diferent types of fairness in the personalized news recommendation scenario, and it is verychallenging to simultaneously achieve multi-side fairness without a heavy sacriice of recommendation accuracy.
第三に，個人化されたニュース推薦のシナリオには様々なタイプの公平性が存在し，推薦精度を大きく犠牲にすることなくマルチサイド公平性を同時に達成することは非常に困難である．

## 10.12. Content Moderation in News Recommendation 10.12. ニュースレコメンデーションにおけるコンテンツモデレーション

The moderation of news content is important for online news platforms to avoid recommending news withlow quality or harmful content to users and mitigate their impact on users and society.
オンラインニュースプラットフォームでは，低品質なニュースや有害なコンテンツをユーザに推薦することを避け，ユーザや社会への影響を軽減するために，ニュースコンテンツのモデレーションが重要である．
However, this issue israrely studied and cannot be resolved by most existing news recommendation methods.
しかし、この問題はほとんど研究されておらず、既存のほとんどのニュース推薦手法では解決できない。
There are three keyresearch directions on this problem.
この問題に対する研究の方向性は以下の3つである。
First, it is essential to understand the generation and spreading mechanism ofharmful news as well as their impact on users, which can help news platforms better defend toxic content.
第一に、有害なニュースの生成と拡散のメカニズム、およびユーザーへの影響を理解することが不可欠であり、これによりニュースプラットフォームが有害なコンテンツをよりよく防御することができる。
Second,it may be useful to incorporate content moderation techniques like fake news detection [177] and clickbaitdetection [211] into news recommendation to adjust the recommendation results according to the quality ofnews content.
第二に、フェイクニュース検出[177]やクリックベイト検出[211]などのコンテンツモデレーション技術をニュース推薦に取り入れ、ニュースコンテンツの質に応じて推薦結果を調整することが有用であると考えられる。
Third, without the assistance of additional tasks and resources, we can learn content quality-awarenews recommendation models with the guidance of certain kinds of user feedback such as comments and dislikes,which is expected to help recommend high-quality news to users.
第三に、追加的なタスクやリソースを必要とせず、コメントや「嫌い」などの特定の種類のユーザーフィードバックを参考に、コンテンツの質に応じたニュース推薦モデルを学習することができ、ユーザーに高品質のニュースを推薦するのに役立つと期待される。

## 10.13. Societal Impact of News Recommendation 10.13. ニュースレコメンデーションの社会的影響

News recommender systems can generate societal impact when they serve a certain number of users.
ニュースレコメンダーシステムは，一定数のユー ザにサービスを提供することで，社会的なインパクトを与える ことができる．
They mayimperceptibly inluence the opinions and views of users when displaying personalized news content [134].
また、パーソナライズされたニュース・コンテンツを表示する際に、ユーザーの意見や見解に影響を与える可能性があります[134]。
Thus, itis valuable for further research to identify and analyze the societal impact of personalized news recommendation algorithms, such as their inluence on political events, economic activities and psychological health.
このように、パーソナライズド・ニュースの推薦アルゴリズムが政治的な出来事や経済活動、心理的な健康に与える影響など、社会的なインパクトを特定し分析することは今後の研究にとって価値がある。
In addition,research on how to reduce the potential negative societal impact of personalized news recommendation methodscan help avoid their risky behaviors and better serve online users.
さらに，パーソナライズド・ニュース推薦手法の潜在的な社会的悪影響を低減する方法に関する研究は，その危険な行動を回避し，オンライン・ユーザによりよいサービスを提供するのに役立つと思われます．

# 11. Conclusion 11. 結論

Finally, we present a conclusion to this survey paper.
最後に、本サーベイ論文の結論を述べる。
In this survey, we conduct a comprehensive overviewof the personalized news recommendation ield, including the technologies involved in diferent core modulesof a personalized news recommender, the dataset and metrics for performance evaluation, the key points fordeveloping responsible personalized news recommender systems, and potential directions to be explored in thefuture.
本サーベイでは，個人向けニュース推薦システムの様々なコアモジュールに関連する技術，性能評価のためのデータセットとメトリック，責任ある個人向けニュース推薦システムを開発するためのキーポイント，および将来的に探求すべき潜在的方向性を含め，個人向けニュース推薦分野の包括的概観を行う．
Diferent from existing survey papers that follow the conventional taxonomy of news recommendationmethods, in this paper we provide a novel perspective to understand personalized news recommendationfrom its key problems and the associated techniques and challenges.
本論文では、従来のニュース推薦手法の分類に従ったサーベイ論文とは異なり、個人化されたニュース推薦を、その主要な問題点と関連する技術や課題から理解する新しい視点を提供するものである。
In addition, this is the irst survey paperthat comprehensively covers both traditional and up-to-date deep learning techniques for personalized newsrecommendation, which can provide rich insights for extending the frontier of this ield.
また、本論文は、パーソナライズドニュースレコメンデーションのための伝統的な深層学習技術と最新の深層学習技術の両方を包括的にカバーする最初のサーベイ論文であり、この分野のフロンティアを拡張するための豊富な洞察を提供することができます。
We hope this paper canfacilitate future research on personalized news recommendation as well as related ields in NLP and data mining.
本論文が、パーソナライズドニュースレコメンデーションや、自然言語処理およびデータマイニングの関連分野における今後の研究の一助となることを期待する。
