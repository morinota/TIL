## refs 審判

- https://arxiv.org/pdf/2103.01696.pdf https://arxiv.org/pdf/2103.01696.pdf

## title タイトル

Cross-Domain Recommendation: Challenges, Progress, and Prospects
クロスドメイン推薦： 課題、進展、展望

## abstract 抄録

To address the long-standing data sparsity problem in recommender systems (RSs), cross-domain recommendation (CDR) has been proposed to leverage the relatively richer information from a richer domain to improve the recommendation performance in a sparser domain.
推奨システム(RS)における長年のデータスパースティ問題に対処するために、領域横断推奨(CDR)が提案されている。CDRは、より豊かな領域からの相対的に豊かな情報を活用して、よりスパースな領域における推奨性能を向上させる。
Although CDR has been extensively studied in recent years, there is a lack of a systematic review of the existing CDR approaches.
CDRは近年盛んに研究されているが、既存のCDRアプローチに関する体系的なレビューはない。
To fill this gap, in this paper, we provide a comprehensive review of existing CDR approaches, including challenges, research progress, and prospects.
このギャップを埋めるため、本稿では、課題、研究の進展、展望を含め、既存のCDRアプローチを包括的にレビューする。
Specifically, we first summarize existing CDR approaches into four types, including single-target CDR, multi-domain recommendation, dual-target CDR, and multi-target CDR.
具体的には、まず既存のCDRアプローチを、シングルターゲットCDR、マルチドメイン推薦、デュアルターゲットCDR、マルチターゲットCDRの4つのタイプに要約する。
We then present the definitions and challenges of these CDR approaches.
そして、これらのCDRアプローチの定義と課題を提示する。
Next, we propose a full-view categorization and new taxonomies on these approaches and report their research progress in detail.
次に、これらのアプローチに関するフルビューの分類と新しい分類法を提案し、その研究経過を詳細に報告する。
In the end, we share several promising prospects in CDR.
最後に、我々はCDRにおけるいくつかの有望な展望を共有している。

# Introduction はじめに

In the past couple of decades, recommender systems (RSs) have become a popular technique in many web applications, e.g., Youtube (video sharing), Amazon (e-commerce), and Facebook (social networking), as they provide suggestions of items to users so that they can avoid facing the information overload problem [Ricci et al., 2015].
過去数十年間で、レコメンダー・システム（RS）は、多くのウェブ・アプリケーション、例えばYoutube（動画共有）、Amazon（電子商取引）、Facebook（ソーシャル・ネットワーキング）において一般的な技術となっている。
In the existing RSs, collaborative filtering (CF) has been proven to be the most promising technique [Chen et al., 2018].
既存のRSでは、協調フィルタリング（CF）が最も有望な手法であることが証明されている[Chen et al, 2018]。
The general idea of CF techniques is to recommend items to a user based on the observed preferences of other users whose historical preferences are similar to those of the target user.
CF技術の一般的な考え方は、過去の嗜好がターゲットユーザーの嗜好と類似している他のユーザーの嗜好の観察に基づいて、ユーザーにアイテムを推薦することである。
Motivation of Cross-Domain Recommendations.
クロスドメイン推薦の動機。
In most real-world application scenarios, few users can provide ratings or reviews for many items [Ricci et al., 2015] (i.e., data sparsity), which reduces the recommendation accuracy of CF-based models.
ほとんどの実世界のアプリケーションシナリオでは、多くのアイテムに対して評価やレビューを提供できるユーザは少なく[Ricci et al, 2015]（すなわち、データの疎ら性）、CFベースのモデルの推薦精度を低下させる。
Almost all existing CF-based recommender systems suffer from this long-standing data sparsity problem to some extent, especially for new items or users (the cold-start problem).
既存のCFベースのレコメンダーシステムのほとんどは、特に新しいアイテムやユーザー（コールドスタート問題）に対して、ある程度この長年のデータスパースティ問題に悩まされている。
This problem may lead to over-fitting when training a CF-based model, which significantly reduces recommendation accuracy.
この問題は、CFベースのモデルをトレーニングする際にオーバーフィッティングを引き起こす可能性があり、推薦精度を著しく低下させる。
To address the data sparsity problem, cross-domain recommendation (CDR) [Berkovsky et al., 2007] has emerged to utilise the relatively richer information, e.g., user/item information [Chung et al., 2007], thumbs-up [Shapira et al., 2013], tags [Fernandez-Tob ´ ´ıas and Cantador, 2014], reviews [Tan et al., 2014], and observed ratings [Zhu et al., 2018], from the richer (source) domain to improve the recommendation accuracy in the sparser (target) domain.
データスパースティ問題に対処するために、比較的リッチな情報、例えば、ユーザー/アイテム情報[Chung et al., 2007]、サムズアップ[Shapira et al、 2013]、タグ[Fernandez-Tob´´ıas and Cantador, 2014]、レビュー[Tan et al., 2014]、観察された評価[Zhu et al., 2018]など、よりリッチな（ソース）ドメインから、よりスパースな（ターゲット）ドメインにおける推薦精度を向上させる。
For example, the Douban’s1 RS can recommend books to users according to their movie reviews (i.e., CDR), since a common user in different domains is likely to have similar tastes.
例えば、Douban's1のRSは、異なるドメインにいる共通のユーザーは同じような嗜好を持っている可能性が高いので、映画のレビュー（すなわちCDR）に応じてユーザーに本を推薦することができる。
Notion of Domain.
ドメインの概念。
In the literature, researchers have attempted to define the notion of domain.
文献の中で、研究者たちはドメインという概念を定義しようと試みてきた。
However, the concept of domain is still very confusing.
しかし、ドメインの概念はまだ非常に混乱している。
For example, some of them treated items (e.g., movies and books) as different domains [Hu et al., 2013], while others considered items in different sub-categories, e.g., such as textbooks and novels, as different domains [Cao et al., 2010].
例えば、アイテム（映画と本など）を異なるドメインとして扱うものもあれば [Hu et al., 2013]、教科書と小説など異なるサブカテゴリのアイテムを異なるドメインとみなすものもある [Cao et al., 2010]。
These definitions mainly focus on the difference of items but the difference of users is ignored.
これらの定義は主にアイテムの違いに焦点を当てているが、ユーザーの違いは無視されている。
In this survey paper, we define domain from the following three perspectives, i.e., content-level relevance, user-level relevance, and item-level relevance.
本サーベイでは、コンテンツレベルの関連性、ユーザーレベルの関連性、アイテムレベルの関連性という3つの観点からドメインを定義する。

Content-level relevance.
コンテンツレベルの関連性。
In the dual/multiple domains, there are the same content or metadata features, e.g., keywords and tags, from user preferences and item details.
デュアル/マルチドメインでは、ユーザー設定やアイテムの詳細から、同じコンテンツやメタデータの特徴、例えばキーワードやタグが存在する。
However, there are not common users/items in these domains, e.g., Amazon music2 and Netflix.
しかし、例えばAmazon music2やNetflixのように、これらのドメインに共通のユーザーやアイテムがあるわけではない。
User-level relevance.
ユーザーレベルの関連性。
In the dual/multiple domains, there are common users and different levels of items – such as attribute-level (i.e., items in the same type (e.g., book) with different attribute values, e.g., textbooks and novels) and textbftype-level (i.e., items in different types, e.g., movies and books).
デュアル/マルチドメインでは、共通のユーザーと異なるレベルのアイテムが存在する。例えば、属性レベル（つまり、同じタイプ（例：本）のアイテムで属性値が異なるもの（例：教科書と小説））、textbftypeレベル（つまり、異なるタイプのアイテム（例：映画と本））などがある。
• Item-level relevance.
- 項目レベルの関連性。
In the dual/multiple domains, there are common items (e.g., movies) and different users, e.g., the users in MovieLens4 and Netflix systems.
デュアル/マルチドメインでは、共通のアイテム（例：映画）と異なるユーザー（例：MovieLens4とNetflixシステムのユーザー）が存在する。
These users are totally different or it is difficult to distinguish the overlapped users among different recommender systems.
これらのユーザは全く異なるものであったり、異なる推薦システム間で重複したユーザを区別することは困難である。
In the literature [Zhu et al., 2018; Zhu et al., 2020], this type of cross-domain recommendation is also referred to as ‘crosssystem recommendation’.
文献[Zhu et al, 2018; Zhu et al, 2020]では、この種のクロスドメイン・レコメンデーションは「クロスシステム・レコメンデーション」とも呼ばれている。
Classification of CDR.
CDRの分類。
Conventional CDR approaches can be generally classified into three groups: (1) contentbased transfer approaches, (2) embedding-based transfer approaches, and (3) rating pattern-based transfer.
従来のCDRアプローチは、一般的に3つのグループに分類することができる： (1)内容ベースの転送アプローチ、(2)埋め込みベースの転送アプローチ、(3)評価パターンベースの転送アプローチである。
Contentbased transfer mainly handles the CDR problems with content-level relevance and tends to link different domains by identifying similar content information, such as item details [Winoto and Tang, 2008], user-generated reviews [Tan et al., 2014], and social tags [Fernandez-Tob ´ ´ıas and Cantador, 2014].
コンテンツベースの転送は、主にコンテンツレベルの関連性でCDRの問題を処理し、アイテムの詳細[Winoto and Tang, 2008]、ユーザーが作成したレビュー[Tan et al, 2014]、ソーシャルタグ[Fernandez-Tob´ıas and Cantador, 2014]などの類似したコンテンツ情報を識別することによって、異なるドメインをリンクする傾向がある。
In contrast, embedding-based transfer [Zhu et al., 2020] mainly handles the CDR problems with user-level relevance and item-level relevance.
対照的に、埋め込みベースの転送[Zhu et al., 2020]は、主にユーザーレベルの関連性とアイテムレベルの関連性を持つCDR問題を扱う。
This class involves first training different CF-based models (such as singular value decomposition [Deerwester et al., 1990], maximum-margin matrix factorisation [Srebro et al., 2005], probabilistic matrix factorisation [Mnih and Salakhutdinov, 2007], bayesian personalised ranking [Rendle et al., 2009], neural collaborative filtering [He et al., 2017] and deep matrix factorisation [Xue et al., 2017]) and graphic models [Zhu et al., 2020; Liu et al., 2020b]) to obtain user/item embeddings, and then transferring these embeddings through common or similar users/items across domains.
このクラスでは、まず異なるCFベースのモデル（特異値分解[Deerwester et al., 1990]、最大マージン行列分解[Srebro et al., 2005]、確率的行列分解[Mnih and Salakhutdinov, 2007]、ベイジアンパーソナライズドランキング[Rendle et al、 2009]、ニューラル協調フィルタリング[He et al.,2017]、ディープ行列分解[Xue et al.,2017]）やグラフィックモデル[Zhu et al.,2020;Liu et al.,2020b]）を使ってユーザー／アイテムの埋め込みを取得し、ドメイン間で共通または類似のユーザー／アイテムを通してこれらの埋め込みを転送する。
Different from embeddingbased transfer, rating pattern-based transfer tends to transfer an independent knowledge, i.e., rating pattern s, across domains.
レーティングパターンに基づく移譲は、埋め込みに基づく移譲とは異なり、独立した知識、すなわちレーティングパターンsをドメイン間で移譲する傾向がある。
In contrast to the content-based transfer approaches, embedding-based and rating pattern-based transfer approaches typically employ machine learning techniques, such as multi-task learning [Singh and Gordon, 2008], transfer learning [Zhang et al., 2016], clustering [Farseev et al., 2017], and neural networks [Zhu et al., 2018], to transfer knowledge across domains.
コンテンツベースの移転アプローチとは対照的に、埋め込みベースや評価パターンベースの移転アプローチは、通常、マルチタスク学習[Singh and Gordon, 2008]、移転学習[Zhang et al., 2016]、クラスタリング[Farseev et al., 2017]、ニューラルネットワーク[Zhu et al., 2018]などの機械学習技術を採用し、ドメイン間で知識を移転する。
The above conventional CDR approaches are single-target approaches that can only leverage the auxiliary information from a richer domain to help a sparser domain.
上記のような従来のCDRアプローチは、単一対象へのアプローチであり、より豊かな領域からの補助的な情報を活用して、より疎な領域を支援することしかできない。
However, each of the domains may be relatively richer in certain types of information (e.g., ratings, reviews, user profiles, item details, and tags); if such information can be leveraged well, it is possible to improve the recommendation performance in all domains simultaneously rather than in a single target domain only.
しかし、それぞれのドメインは、ある種の情報（例えば、評価、レビュー、ユーザープロフィール、アイテムの詳細、タグなど）が比較的豊富である可能性があり、そのような情報をうまく活用できれば、単一の対象ドメインのみではなく、すべてのドメインで同時に推薦性能を向上させることが可能である。
To this end, dual-target CDR [Zhu et al., 2019; Li and Tuzhilin, 2020; Zhu et al., 2020; Liu et al., 2020b] and multi-target CDR [Cui et al., 2020] have been proposed recently to improve the recommendation performance in dual/multiple domains.
このため、デュアル/マルチドメインにおける推薦性能を向上させるために、デュアルターゲットCDR [Zhu et al., 2019; Li and Tuzhilin, 2020; Zhu et al.
The Motivation of This Survey.
この調査の動機
CDR is not a new research area, and in the literature, there are two survey papers [Fernandez-Tob ´ ´ıas et al., 2012; Cantador and Cremonesi, 2014] and a systematical handbook [Ricci et al., 2015] which have carefully introduced and analyzed this area.
CDRは新しい研究分野ではなく、文献では2つのサーベイ論文[Fernandez-Tob´´ıas et al., 2012; Cantador and Cremonesi, 2014]と体系的なハンドブック[Ricci et al.
However, after these tutorials, there are many new challenges, e.g., feature mapping, embedding optimization, and negative transfer, and new directions, e.g., dual-target CDR and multi-target CDR.
しかし、これらのチュートリアルの後にも、特徴マッピング、埋め込み最適化、ネガティブトランスファーなどの新たな課題や、デュアルターゲットCDRやマルチターゲットCDRなどの新たな方向性が数多く存在する。
These new research trends motivate us to analyze the challenges in CDR and summarize the research progress.
このような新しい研究動向は、CDRにおける課題を分析し、研究の進展をまとめる動機となっている。
Our Contributions.
我々の貢献
The main contributions of this survey paper are summarized as follows: • We provide a detailed overview of the challenges in CDR and classify them from a developing perspective, which provides a whole view of the development in CDR area.
本サーベイ・ペーパーの主な貢献は以下の通りである： - CDRにおける課題を詳細に概観し、発展途上の視点からそれらを分類することで、CDR分野における発展の全体像を提供する。
• We present a comprehensive review of current research progress in CDR.
- 我々は、CDRにおける現在の研究進展を包括的にレビューする。
Specifically, we analyze the contributions of existing approaches and the similarities and differences between them.
具体的には、既存のアプローチの貢献度と、それらの類似点と相違点を分析する。
• We outline some promising future research directions in CDR, which would shed light on the development of the research community.
- 我々は、CDRにおける将来有望な研究の方向性を概説し、研究コミュニティの発展に光を当てる。

# Problems and Challenges 問題点と課題

Cross-domain recommendation problem has been formulated in different recommendation scenarios, i.e., single-target CDR, multi-domain recommendation, dual-target CDR, and multi-target CDR.
クロスドメイン推薦問題は、シングルターゲットCDR、マルチドメイン推薦、デュアルターゲットCDR、マルチターゲットCDRといった異なる推薦シナリオで定式化されている。
The main differences among these scenarios are the scales of domains, overlaps, and improvement targets.
これらのシナリオの主な違いは、ドメインの規模、重複、改善目標である。
In this section, we introduce these particular CDR scenarios and their corresponding challenges.2.1 Single-Target CDR Single-target CDR is a conventional recommendation scenario in CDR area and most of the existing CDR approaches focus on this scenario.
2.1 シングル・ターゲットCDR シングル・ターゲットCDRは、CDR分野における従来の推薦シナリオであり、既存のCDRアプローチのほとんどはこのシナリオに焦点を当てている。
We define this recommendation problem as follows.
この推薦問題を以下のように定義する。
Definition 1 Single-Target Cross-Domain Recommendation: Given the source domain s (including a user set U s and an item set V s ) with richer data — such as explicit feedback (e.g., ratings and comments), implicit feedback (e.g., purchase and browsing histories), and side information (e.g., user profiles and item details) — and the target domain t (including a user set U t and an item set V t ) with sparser data, single-target CDR is to improve the recommendation accuracy in t by leveraging the auxiliary information in s.
定義1 単一ターゲット・クロスドメイン推薦： ソースドメインs（ユーザ集合U sとアイテム集合V sを含む）とターゲットドメインt（ユーザ集合U tとアイテム集合V tを含む）が、明示的フィードバック（評価やコメントなど）、暗黙的フィードバック（購入履歴や閲覧履歴など）、サイド情報（ユーザプロファイルやアイテムの詳細など）などの豊富なデータを持つ場合、シングルターゲットCDRは、sの補助情報を活用することで、tの推薦精度を向上させる。
As introduced in Section 1, we define the notion of domain from three perspectives, i.e., content-level relevance, user-level relevance, and item-level relevance.
セクション1で紹介したように、コンテンツレベルの関連性、ユーザーレベルの関連性、アイテムレベルの関連性という3つの観点からドメインの概念を定義する。
Thus, singletarget CDR scenario is divided into three corresponding subscenarios as well (see Figure 1).
このように、シングルターゲットCDRシナリオは、3つの対応するサブシナリオに分けられる（図1参照）。
We summarize three main challenges for the single-target CDR scenarios.
シングル・ターゲットCDRシナリオにおける3つの主要な課題を要約する。
Building content-based relations (CH1).
コンテンツ・ベースの関係構築（CH1）。
In Figure 1(a), to improve the recommendation accuracy in the target domain, one should first build content-based relations, then choose similar users/items according to their common features, and finally, transfer/share other features between similar users/items across domains.
図1(a)において、対象ドメインにおける推薦精度を向上させるためには、まずコンテンツベースの関係性を構築し、次に共通する特徴によって類似ユーザ／アイテムを選択し、最後にドメインを越えて類似ユーザ／アイテム間で他の特徴を転送／共有する必要がある。
Therefore, how to build a suitable content-based relation in single-target CDR (contentlevel relevance) scenario is very important and challenging.
したがって、単一ターゲットCDR（コンテンツレベルの関連性）シナリオにおいて、どのように適切なコンテンツベースの関連性を構築するかは、非常に重要かつ挑戦的である。
Generating accurate user/item embeddings or rating patterns (CH2).
正確なユーザー/アイテムの埋め込みまたは評価パターンを生成する（CH2）。
In Figures 1(b) and 1(c), to improve the recommendation accuracy in the target domain, one should first generate accurate user/item embeddings or rating patterns, and then transfer/share the embeddings of common users/items or rating patterns of common users across domains.
図1(b)および図1(c)において、対象ドメインにおける推薦精度を向上させるためには、まず、正確なユーザ／項目の埋め込み、または、評価パターンを生成し、次に、ドメイン間で共通のユーザ／項目の埋め込み、または、共通のユーザの評価パターンを転送／共有する必要がある。
Therefore, how to generate accurate embeddings or rating patterns is a fundamental and crucial challenge.
したがって、いかにして正確な埋め込みや評価パターンを生成するかは、基本的かつ重要な課題である。
Learning accurate mapping relations (CH3).
正確なマッピング関係を学ぶ（CH3）。
For the three scenarios of single-target CDR in Figure 1, a naive transfer strategy is to directly replace the features/embeddings of users/items in the target domain with those of their similar users/items in the source domain [Zhao et al., 2017].
図1の単一ターゲットCDRの3つのシナリオでは、素朴な転送戦略は、ターゲットドメインのユーザー／アイテムの特徴／埋め込みを、ソースドメインの類似ユーザー／アイテムの特徴／埋め込みに直接置き換えることである［Zhao et al.］
This strategy is simple but not intelligent.
この戦略は単純だが、知的ではない。
An elegant way is to first learn accurate mapping relations between two domains, and then transfer the knowledge (e.g., user/item embeddings and rating patterns) learned from a source domain to a target domain according to the learned mapping relations.
エレガントな方法は、まず2つのドメイン間の正確なマッピング関係を学習し、学習したマッピング関係に従って、ソースドメインで学習した知識（ユーザー／アイテムの埋め込みや評価パターンなど）をターゲットドメインに転送することである。
Following such an intuition, how to learn accurate mapping relations becomes a crucial challenge.2.2 Multi-Domain Recommendation Multi-Domain Recommendation (MDR) is another direction in single-target CDR.
このような直観に従って、どのように正確なマッピング関係を学習するかが重要な課題となる。
It leverages the auxiliary information from multiple domains to recommend a set of items from multiple domains to a certain set of users (single-target) in the multiple domains.
複数ドメインの補助情報を活用し、複数ドメイン内の特定のユーザー（シングルターゲット）に対して、複数ドメインのアイテムセットを推薦する。
We define multiple-domain recommendation as follows.
複数ドメイン推薦を以下のように定義する。
Definition 2 Multi-Domain Recommendation (MDR): Given the multiple domains 1 to n, including user sets {U1 , ..., U n} and item sets {V1 , ..., V n}, multi-target CDR is to recommend a set of items V x (V x ∈ V1 ∪ ...∪ Vn) to a certain set of users U x (U x ∈ U1 ∪ ...∪ U n) and improve the corresponding recommendation accuracy.
定義2 マルチドメイン推薦（MDR）： ユーザ集合｛U1 ，...，U n｝とアイテム集合｛V1 ，...，V n｝を含む複数のドメイン1〜nが与えられたとき、マルチターゲットCDRは、あるユーザ集合U x (U x ∈ U1 ∪ ...∪ U n)にアイテム集合V x (V x ∈ V1 ∪ ...∪ Vn)を推薦し、対応する推薦精度を向上させることである。
MDR faces the same challenges as single-target CDR.2.3 Dual-Target CDR Dual-target CDR is a new recommendation scenario in CDR area and it has attracted increasing attention in recent years.
2.3 デュアル・ターゲットCDR デュアル・ターゲットCDRは、CDR分野での新しい推奨シナリオであり、近年注目されている。
We define this recommendation problem as follows.
この推薦問題を以下のように定義する。
Definition 3 Dual-Target Cross-Domain Recommendation: Given the two domains 1 and 2, including user sets U 1 , U 2 and item sets V 1 , V 2 respectively, dual-target CDR is to improve the recommendation accuracy in both domains 1 and 2 simultaneously by leveraging their observed information.
定義3 デュアルターゲットクロスドメイン推薦： ユーザ集合U 1 , U 2とアイテム集合V 1 , V 2をそれぞれ含む2つのドメイン1, 2が与えられたとき、デュアルターゲットCDRは、ドメイン1, 2の観測情報を活用することで、同時にドメイン1, 2の推薦精度を向上させることである。
Similar to the problem of single-target CDR, dual-target CDR scenario can be divided into three sub-scenarios according to the notion of domain.
シングルターゲットCDRの問題と同様に、デュアルターゲットCDRのシナリオは、ドメインの概念に従って3つのサブシナリオに分けることができる。
This means that dual-target CDR scenarios can also use common features (content-level relevance), common users (user-level relevance), and common items (item-level relevance), to link the two domains and share/transfer knowledge across domains based on these common entities.
つまり、デュアルターゲットCDRシナリオは、共通の特徴（コンテンツレベルの関連性）、共通のユーザー（ユーザーレベルの関連性）、共通のアイテム（アイテムレベルの関連性）を使用して、2つのドメインをリンクし、これらの共通のエンティティに基づいてドメイン間で知識を共有/転送することもできる。
However, different from single-target CDR, dual-target CDR is to improve the recommendation accuracy in both target domains simultaneously (see Figure 4).
しかし、シングルターゲットCDRとは異なり、デュアルターゲットCDRは、両方のターゲットドメインにおいて同時に推薦精度を向上させるものである（図4参照）。
To achieve dual-target CDR, there are two challenges.
デュアルターゲットCDRを達成するためには、2つの課題がある。
Designing a feasible dual-target CDR framework (CH4).
実現可能なデュアルターゲットCDRフレームワークの設計（CH4）。
Unlike conventional single-target CDR, dual-target CDR should enhance the recommendation performance in the two domains, i.e., the source domain and the target domain.
従来のシングルターゲットCDRとは異なり、デュアルターゲットCDRは、ソースドメインとターゲットドメインの2つのドメインにおける推薦性能を向上させる必要がある。
Therefore, how to design an effective framework for a dualtarget CDR scenario is still very challenging because the auxiliary information from the target domain may negatively affect the performance in the source domain.
したがって、デュアルターゲットCDRシナリオのための効果的なフレームワークを設計する方法は、ターゲットドメインからの補助情報がソースドメインでのパフォーマンスに悪影響を与える可能性があるため、依然として非常に困難である。
Optimizing the embedding of users and items (CH5).
ユーザーとアイテムの埋め込みを最適化する（CH5）。
In a dual-target CDR scenario, to improve the recommendation accuracy in each domain, the researchers tend to share the common embeddings of common users/items for the two domains or enhance the embedding quality of users/items in each domain by leveraging the auxiliary information from another domain.
デュアルターゲットCDRシナリオでは、各ドメインの推薦精度を向上させるために、研究者は2つのドメインに共通するユーザ／アイテムの埋め込みを共有したり、別のドメインの補助情報を活用して各ドメインのユーザ／アイテムの埋め込み品質を向上させたりする傾向がある。
Therefore, embedding optimization for dualtarget CDR scenarios is particularly important.2.4 Multi-Target CDR Inspired by dual-target CDR, in a multi-target CDR scenario, the researchers aim to improve the recommendation accuracy in multiple domains simultaneously.
したがって、デュアルターゲットCDRシナリオにおける埋め込み最適化は特に重要である。
The core idea of multitarget CDR is to leverage more auxiliary information from more domains to achieve a further improvement of recommendation performance.
マルチターゲットCDRの核となる考え方は、より多くのドメインからの補助情報を活用することで、推薦性能のさらなる向上を達成することである。
The problem of multi-target CDR can be defined as follows.
マルチターゲットCDRの問題は次のように定義できる。
Definition 4 Multi-Target Cross-Domain Recommendation: Given the multiple domains 1 to n, including user sets {U1 , ..., U n} and item sets {V1 , ..., V n}, multi-target CDR is to improve the recommendation accuracy in all domains simultaneously by leveraging their observed information.
定義4 マルチターゲットクロスドメイン推薦： ユーザ集合｛U1 ，...，U n｝とアイテム集合｛V1 ，...，V n｝を含む複数のドメイン1〜nが与えられたとき、それらの観測情報を活用することで、すべてのドメインにおける推薦精度を同時に向上させるのがマルチターゲットCDRである。
To achieve multi-target CDR, in addition to the challenges in single-target CDR and dual-target CDR scenarios, there is a new challenge as follows.
マルチターゲットCDRを実現するためには、シングルターゲットCDRとデュアルターゲットCDRのシナリオにおける課題に加えて、以下のような新たな課題がある。
Avoiding negative transfer (CH6).
マイナスの移籍を避ける（CH6）。
In a multi-target CDR scenario, the recommendation performance in some domains may decline as more domains, especially sparser domains, join in.
マルチターゲットCDRシナリオでは、より多くのドメイン、特にスパースなドメインが参加するにつれて、いくつかのドメインにおける推薦性能が低下する可能性がある。
This is the negative transfer problem that the transferred data/knowledge may negatively affect the recommendation performance in the target domain.
これは、転送されたデータ／知識が、ターゲット・ドメインにおける推薦性能に悪影響を及ぼす可能性があるという負の転送問題である。
In fact, in singletarget CDR, MDR, and dual-target CDR scenarios, the researchers may also face the negative transfer problem.
実際、シングルターゲットCDR、MDR、デュアルターゲットCDRのシナリオにおいても、研究者はネガティブトランスファーの問題に直面する可能性がある。
However, this problem in multi-target CDR scenarios is more serious because the auxiliary information/knowledge in each domain should be transferred to other domains more than once.
しかし、マルチターゲットCDRシナリオでは、各ドメインの補助情報／知識を他のドメインに複数回転送する必要があるため、この問題はより深刻になる。
Therefore, avoiding negative transfer is an important prerequisite in multi-target CDR scenarios.
したがって、負の転移を避けることは、マルチターゲットCDRシナリオにおける重要な前提条件である。

# Research Progress 研究の進展

To correspond with the recommendation scenarios and challenges mentioned in Section 2, in this section, we summarize the existing CDR approaches according to their target scenarios, target challenges, data categories, and technical perspectives.
セクション2で述べた推薦シナリオと課題に対応するため、このセクションでは、既存のCDRアプローチを、ターゲットシナリオ、ターゲット課題、データカテゴリ、および技術的観点に従って要約する。
We also summarize the popular datasets in CDRs.3.1 Single-Target CDR Most of existing single-target CDR approaches tend to leverage useful information from the source domain to the target domain.
3.1 シングル・ターゲットCDR 既存のシングル・ターゲットCDRアプローチのほとんどは、ソース・ドメインからターゲット・ドメインへの有用な情報を活用する傾向がある。
According to transfer strategies, these single-target CDR approaches are divided in three categories: contentbased transfer, embedding-based transfer, and rating patternbased transfer.
転送戦略によって、これらの単一ターゲットCDRアプローチは3つのカテゴリーに分けられる： コンテントベース、エンベッディングベース、レーティングパターンベースである。
Content-Based Transfer.
コンテント・ベース・トランスファー。
To target CH1, the existing content-based transfer approaches first create links based on the common contents, e.g., user/item attributes, social tags, semantic properties, thumbs-up, text information, metadata, and browsing or watching history.
CH1をターゲットとするために、既存のコンテンツベースの転送アプローチは、まず、共通のコンテンツ、例えば、ユーザー／アイテムの属性、ソーシャルタグ、セマンティックプロパティ、サムズアップ、テキスト情報、メタデータ、閲覧または視聴履歴に基づいてリンクを作成する。
Then, they transfer user/item data or knowledge across domains.
そして、ユーザーやアイテムのデータや知識をドメインを越えて転送する。
We clearly compare the difference of these approaches in Table 1.
表1では、これらのアプローチの違いを明確に比較している。
Embedding-Based Transfer.
エンベディングベースの移籍。
To target CH2 and CH3, the existing embedding-based transfer approaches employ some classical machine learning models, e.g., multi-task learning, transfer learning, clustering, deep neural networks, relational learning, and semi-supervised learning, to map or share embeddings, e.g., user/item latent factors, learned by CF-based models across domains.
CH2とCH3をターゲットとするために、既存の埋め込みベースの転送アプローチは、いくつかの古典的な機械学習モデル、例えば、マルチタスク学習、転送学習、クラスタリング、ディープニューラルネットワーク、関係学習、半教師付き学習を採用し、CFベースのモデルによって学習された埋め込み、例えば、ユーザー／アイテムの潜在的要因をドメイン間でマッピングまたは共有する。
In addition to these frequentlyused learning techniques, other embedding-based transfer approaches tend to employ different techniques or ideas, e.g., Bayesian latent factor models & interest drift, triadic relation (user-item-domain), reinforcement learning, sequential recommendations, and data privacy.
これらのよく使われる学習技術に加えて、他の埋め込みベースの転送アプローチは、例えば、ベイズ潜在因子モデル＆インタレストドリフト、三項関係（ユーザー-アイテム-ドメイン）、強化学習、逐次レコメンデーション、データプライバシーなど、異なる技術やアイデアを採用する傾向がある。
We clearly compare the differences among these approaches in Table 2.
表2では、これらのアプローチの違いを明確に比較している。
Rating Pattern-Based Transfer.
格付けパターンに基づく移籍。
To target CH2, the existing rating pattern-based transfer approaches tend to first learn an independent rating pattern of users from the source domain and then transfer the rating pattern for the target domain to improve the corresponding recommendation accuracy.
CH2をターゲットとするために、既存の評価パターンベースの転送アプローチは、まずソースドメインからユーザーの独立した評価パターンを学習し、次にターゲットドメインの評価パターンを転送して、対応する推薦精度を向上させる傾向がある。
The representative work of this type of approach includes [Gao et al., 2013; He et al., 2018b; Yuan et al., 2019].
この種のアプローチの代表的な研究には、[Gao et al., 2013; He et al., 2018b; Yuan et al., 2019]がある。
We list the difference of these approaches in Table 2.3.2 Multi-Domain Recommendation
これらのアプローチの違いを表2.3.2に示す。

Multi-Domain Recommendation (MDR) is another direction in single-target CDR, but it achieves a different goal: it makes recommendations for different domains.
マルチドメイン・レコメンデーション（MDR）は、シングルターゲットCDRのもう一つの方向性だが、異なるゴールを達成する： 異なるドメインに対して推薦を行う。
Some of these multidomain approaches can be applied in CDR scenarios, but they tend to make recommendations either for specific or common users who are selected from domains, or for the users in the target domain only.
これらのマルチドメインアプローチのいくつかは、CDRシナリオに適用することができるが、ドメインから選択された特定または共通のユーザー、またはターゲットドメインのユーザーのみに推奨を行う傾向がある。
MDR also faces the conventional challenges, e.g., CH1 and CH2, in STCDR.
MDRもまた、STDRにおける従来の課題、例えばCH1とCH2に直面している。
To address these challenges, in [Zhang et al., 2012], Zhang et al.proposed a multi-domain collaborative filtering (MCF) framework for solving the data sparsity problem in multiple domains.
これらの課題に対処するため、[Zhang et al., 2012]において、Zhang et al.は複数ドメインにおけるデータスパースティ問題を解決するための複数ドメイン協調フィルタリング（MCF）フレームワークを提案した。
After this, the MDR models proposed in [Cao et al., 2010; Moreno et al., 2012; Pan and Yang, 2013; Zhang et al., 2016] employ different techniques, i.e., feature combination, transfer learning, and active learning to transfer the knowledge of similar/common users among multiple domains.3.3 Dual-Target CDR Dual-target CDR is still a novel but very attractive concept for improving the recommendation accuracies in both domains simultaneously.
この後、[Cao et al., 2010; Moreno et al., 2012; Pan and Yang, 2013; Zhang et al., 2016]で提案されたMDRモデルは、複数のドメイン間で類似/共通ユーザーの知識を転送するために、特徴組み合わせ、転送学習、能動学習などの異なる技術を採用している。
Therefore, existing solutions are limited but the researchers are paying more and more attention to this direction.
そのため、既存の解決策は限られているが、研究者たちはこの方向にますます注目している。
To target CH4 and CH5, the existing dual-target CDR approaches mainly focus on either applying fixed or flexible combination strategies [Zhu et al., 2019; Zhu et al., 2020; Liu et al., 2020b], or simply changing the existing single-target transfer learning to become dual-transfer learning [Li and Tuzhilin, 2020].
CH4とCH5をターゲットにするために、既存のデュアルターゲットCDRアプローチは、主に固定または柔軟な組み合わせ戦略を適用するか[Zhu et al., 2019; Zhu et al., 2020; Liu et al., 2020b]、または単に既存の単一ターゲット転移学習をデュアル転移学習に変更することに焦点を当てている[Li and Tuzhilin, 2020]。
In [Zhu et al., 2019], Zhu et al.first proposed the DTCDR, a dual-target CDR framework that uses multi-source information such as ratings, reviews, user profiles, item details, and tags to generate more representative embeddings of users and items.
Zhu et al., 2019]において、Zhuらはまず、評価、レビュー、ユーザープロファイル、アイテムの詳細、タグなどのマルチソース情報を使用して、ユーザーとアイテムのより代表的な埋め込みを生成するデュアルターゲットCDRフレームワークであるDTCDRを提案した。
Then, based on multi-task learning, the DTCDR framework uses three different combination strategies to combine and share the embedding of common users across domains.
次に、マルチタスク学習に基づいて、DTCDRフレームワークは、3つの異なる組み合わせ戦略を使用して、ドメイン間で共通のユーザーのエンベッディングを組み合わせて共有する。
Similarly, in [Liu et al., 2020b], Liu et al.also use a fixed combination strategy, i.e., hyper-parameters and data sparsity degrees of common users, to combine the embedding of common users.
同様に、[Liu et al., 2020b]では、Liu et al.も固定的な組み合わせ戦略、すなわち、共通ユーザのハイパーパラメータとデータ疎分散度を用いて、共通ユーザの埋め込みを組み合わせている。
Additionally, a new dual-target CDR model (DDTCDR) was proposed in [Li and Tuzhilin, 2020], which considers the bi-directional latent relations between users and items and applies a latent orthogonal mapping to extract user preferences.
さらに、新しいデュアルターゲットCDRモデル（DDTCDR）が[Li and Tuzhilin, 2020]で提案され、これはユーザとアイテムの間の双方向の潜在的関係を考慮し、ユーザの嗜好を抽出するために潜在的直交マッピングを適用する。
Based on the orthogonal mapping, DDTCDR can transfer users’ embeddings in a bidirectional way (i.e., Source → Target and Target → Source).
直交マッピングに基づき、DDTCDRはユーザのエンベッディングを双方向（ソース→ターゲット、ターゲット→ソース）に転送することができる。
Recently, Zhu et al.proposed another dual-target CDR framework in [Zhu et al., 2020], which employs graph embedding to generate more informative embeddings of users and items, and employs element-wise attention to combine the embeddings of common users/items across domains.3.4 Multi-Target CDR Although multi-target CDR is inspired by dual-target CDR and multi-domain recommendation, it aims to achieve a bigger goal, i.e., providing a complete solution for data sparsity.
Zhu et al., 2020]では、グラフ埋め込みを用いて、より情報量の多いユーザとアイテムの埋め込みを生成し、ドメイン間で共通のユーザ／アイテムの埋め込みを結合するために、要素ごとの注意を用いている。3.4 マルチターゲットCDR マルチターゲットCDRは、デュアルターゲットCDRとマルチドメイン推薦に触発されているが、より大きな目標、すなわち、データスパース性の完全な解決策を提供することを目指している。
In principle, if the multi-target CDR models can find enough related domains and utilize the auxiliary information from these multiple domains well, the long-standing data sparsity problem in recommender systems can be greatly alleviated and even solved.
原理的には、マルチターゲットCDRモデルが十分な関連ドメインを見つけ、これらの複数のドメインからの補助情報をうまく利用することができれば、推薦システムにおける長年のデータスパースティ問題を大幅に緩和し、解決することさえできる。
However, as introduced in Section 2.4, apart from the challenges in single-target CDR and dualtarget CDR scenarios, a new challenge, i.e., negative transfer (CH6), is inevitable in real multi-target CDR scenarios.
しかし、セクション2.4で紹介したように、シングル・ターゲットCDRやデュアル・ターゲットCDRシナリオにおける課題とは別に、実際のマルチ・ターゲットCDRシナリオでは、ネガティブ・トランスファー（CH6）という新たな課題が避けられない。
Multi-target CDR is a challenging recommendation scenario, and thus, by now, there are few solutions [Cui et al., 2020; Krishnan et al., 2020] on achieving this goal.
マルチターゲットCDRは困難な推薦シナリオであるため、現在までにこの目標を達成するための解決策はほとんどない[Cui et al, 2020; Krishnan et al, 2020]。
In [Cui et al., 2020], the authors use a shared heterogeneous graph to generate more informative embeddings of users and items among multiple domains.
Cui et al., 2020]では、著者らは共有された異種グラフを用いて、複数のドメイン間でユーザーとアイテムのより有益な埋め込みを生成している。
Also, the MDCDR approach proposed in [Krishnan et al., 2020] leverages the auxiliary information from a source domain to improve the recommendation accuracy of multiple domains.
また、[Krishnan et al., 2020]で提案されているMDCDRアプローチは、ソースドメインからの補助情報を活用し、複数ドメインの推薦精度を向上させる。
However, these approaches do not consider the negative transfer problem.
しかし、これらのアプローチは負の移籍問題を考慮していない。
Therefore, multitarget CDR is still a challenging task in CDR.3.5 Summary of Datasets In this section, we summarize several popularly used datasets for CDR tasks in Table 3.
3.5 データセットのまとめ 本節では、CDRタスクによく使われるデータセットを表3にまとめる。
This will guide the researchers to obtain these CDR datasets conveniently.
これにより、研究者はこれらのCDRデータセットを便利に入手できるようになる。
Anyone who wishes to use these datasets can refer to the corresponding citations and websites for more details.
これらのデータセットの利用を希望する人は、対応する引用文献やウェブサイトを参照して詳細を確認することができる。

# Research Prospects 研究展望

Although many efforts have been put to tackle the challenges of CDR, there remain some promising prospects, and we summarize three of them as follows.
CDRの課題に取り組むために多くの努力が払われてきたが、いくつかの有望な展望も残されている。
Heterogeneous CDR.
ヘテロジニアスCDR。
Most existing CDR approaches assume information across domains is homogeneous, which is not consistent with reality.
既存のCDRアプローチのほとんどは、ドメイン間の情報が均質であることを前提としているが、これは現実と一致していない。
For example, some researchers assume both domains have rating and content information [Winoto and Tang, 2008], while other studies assume the existence of rating data across both domains [Zhao et al., 2017].
例えば、両ドメインにレーティングとコンテンツ情報があると仮定する研究者もいれば[Winoto and Tang, 2008]、両ドメインにまたがるレーティングデータが存在すると仮定する研究もある[Zhao et al, 2017]。
However, in practice, different domains are rich in different kinds of information.
しかし実際には、異なるドメインには異なる種類の情報が豊富にある。
For instance, an e-commerce domain (e.g., Amazon) is rich in user-item interaction data while a social domain (e.g., Facebook) has plenty of user-user social data.
例えば、電子商取引のドメイン（アマゾンなど）には、ユーザーとアイテムの相互作用データが豊富にあり、ソーシャル・ドメイン（フェイスブックなど）には、ユーザーとユーザーのソーシャル・データが豊富にある。
Under such situations, new techniques should be proposed to identify the ‘bridges’ across domains so as to transfer information and improve the performance of CDR.
このような状況下では、情報を伝達しCDRのパフォーマンスを向上させるために、ドメイン間の「橋」を特定する新しい技術が提案されるべきである。
How to leverage these heterogeneous data across domains, to further improve the recommendation performance, becomes the first promising prospect in CDR.
このようなドメイン間の異種データをどのように活用し、推薦性能をさらに向上させるかが、CDRにおける最初の有望な展望となる。
Sequential CDR.
シーケンシャルCDR。
Sequential recommendation has gained much attention since it can suggest items to users by modeling the sequential dependencies over the user-item interactions [Wang et al., 2019a].
シーケンシャル・レコメンデーションは、ユーザーとアイテムの相互作用にわたるシーケンシャルな依存関係をモデル化することで、ユーザーにアイテムを提案することができるため、注目を集めている[Wang et al, 2019a]。
Naturally, CDR also faces the problem of sequentially modeling of users and items, the same as conventional recommender systems.
当然ながら、CDRも従来のレコメンダーシステムと同様に、ユーザーとアイテムの逐次的なモデル化という問題を抱えている。
Prior work on sequential recommendation mainly focuses on learning the high-order, long-term, and noisy user-item interactions in sequence.
逐次レコメンデーションに関する先行研究は、主に高次で長期的、かつノイズの多いユーザーとアイテムの相互作用を逐次学習することに焦点を当てている。
It becomes more challenging for sequential CDR since one not only needs to model sequential user-item interactions, but also transfer information across domains [Ma et al., 2019].
逐次的なCDRでは、ユーザーとアイテムの逐次的な相互作用をモデル化するだけでなく、ドメインをまたいだ情報の転送も必要となるため、より困難となる[Ma et al, 2019]。
Therefore, sequential CDR becomes the second promising research prospect.
したがって、逐次CDRは2番目の有望な研究展望となる。
Privacy-Preserving CDR.
プライバシーを保護するCDR。
Most existing approaches in CDR assume that data across domains are available in plaintext, which ignores the data isolation problem in practice.
CDRにおける既存のアプローチのほとんどは、ドメイン間のデータが平文で利用可能であることを前提としているが、これは実際にはデータの分離問題を無視している。
Apparently, most recommender systems are built using users’ sensitive data, e.g., check-in data, user profile, and browse history.
どうやら、ほとんどのレコメンダー・システムは、チェックイン・データ、ユーザー・プロフィール、閲覧履歴など、ユーザーの機密データを使って構築されているようだ。
And in CDR, these data are usually held by different domains, e.g., Amazon and eBay.
そしてCDRでは、これらのデータは通常、アマゾンとeBayのように異なるドメインによって保持されている。
In some cases, these data across domain cannot share with other directly since they contain sensitive information.
場合によっては、これらのデータは機密情報を含んでいるため、ドメイン間で直接共有することはできない。
Thus, it is urgent to build CDR meanwhile protect data privacy [Gao et al., 2019].
したがって、データのプライバシーを保護しながらCDRを構築することが急務である[Gao et al, 2019]。
A recent study on privacy-preserving CDR can only handle the simple social matrix factorization model [Chen et al., 2020], and there is a long way to go for complex privacy-preserving CDR.
プライバシー保護CDRに関する最近の研究では、単純な社会的行列分解モデルしか扱うことができず[Chen et al.
Therefore, privacy-preserving CDR is the third pressing and promising research prospect.
したがって、プライバシーを保護するCDRは、3番目の緊急かつ有望な研究展望である。

# Conclusion 結論

Cross-domain recommendations (CDRs) have attracted increasing research attention, with the development of deep neural network and graph learning techniques.
クロスドメイン・レコメンデーション（CDR）は、ディープニューラルネットワークやグラフ学習技術の発展に伴い、研究上の注目が高まっている。
This paper conducted a comprehensive survey on the following four scopes, i.e., single-target CDR, multi-domain recommendation, dual-target CDR, and multi-target CDR.
本稿では、シングルターゲットCDR、マルチドメイン推薦、デュアルターゲットCDR、マルチターゲットCDRの4つのスコープについて包括的な調査を行った。
We first have presented the definitions and challenges of these scopes, then proposed a full-view categorization and new taxonomies on these scopes, and finally listed several promising prospects in CDR.
私たちはまず、これらのスコープの定義と課題を提示し、次にこれらのスコープに関する全体像の分類と新しい分類法を提案し、最後にCDRにおけるいくつかの有望な展望を挙げた。
This survey summarizes current representative research efforts and trends and we expect it can facilitate future research in the community.
この調査は、現在の代表的な研究の取り組みと傾向をまとめたものであり、コミュニティにおける今後の研究を促進することを期待している。