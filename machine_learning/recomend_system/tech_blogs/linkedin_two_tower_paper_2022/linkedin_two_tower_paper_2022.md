refs: /Users/masato.morita/Downloads/1809.06473v1.pdf


## Towards Deep and Representation Learning for Talent Search at LinkedIn  
LinkedInにおけるタレントサーチのための深層学習と表現学習に向けて  

### Rohan Ramanath [∗], Hakan Inan [∗][,][+], Gungor Polatkan [∗], Bo Hu, Qi Guo, Cagri Ozcaglar Xianren Wu, Krishnaram Kenthapadi, Sahin Cem Geyik [∗]  
Rohan Ramanath [∗], Hakan Inan [∗][,][+], Gungor Polatkan [∗], Bo Hu, Qi Guo, Cagri Ozcaglar Xianren Wu, Krishnaram Kenthapadi, Sahin Cem Geyik [∗]  

##### LinkedIn Corporation, USA  
LinkedIn Corporation, アメリカ合衆国  
i
#### ABSTRACT 要約

Talent search and recommendation systems at LinkedIn strive to match the potential candidates to the hiring needs of a recruiter or a hiring manager expressed in terms of a search query or a job posting. 
LinkedInのタレントサーチおよび推薦システムは、リクルーターや採用マネージャーの検索クエリや求人票の形で表現された採用ニーズに対して、潜在的な候補者をマッチングさせることを目指しています。 
Recent work in this domain has mainly focused on linear models, which do not take complex relationships between features into account, as well as ensemble tree models, which introduce non-linearity but are still insufficient for exploring all the potential feature interactions, and strictly separate feature generation from modeling. 
この分野の最近の研究は、特徴間の複雑な関係を考慮しない線形モデルや、非線形性を導入するがすべての潜在的な特徴の相互作用を探るには不十分なアンサンブルツリーモデルに主に焦点を当てており、特徴生成とモデリングを厳密に分離しています。 
In this paper, we present the results of our application of deep and representation learning models on LinkedIn Recruiter. 
本論文では、**LinkedIn Recruiterにおける深層学習および表現学習モデルの適用結果**を示します。 
Our key contributions include: (i) Learning semantic representations of sparse entities within the talent search domain, such as recruiter ids, candidate ids, and skill entity ids, for which we utilize neural network models that take advantage of LinkedIn Economic Graph, and (ii) Deep models for learning recruiter engagement and candidate response in talent search applications.
私たちの主な貢献は次のとおりです：(i) リクルーターID、候補者ID、スキルエンティティIDなど、タレントサーチドメイン内のスパースエンティティの意味的表現を学習することで、LinkedIn Economic Graphを活用したニューラルネットワークモデルを利用します。 (ii) タレントサーチアプリケーションにおけるリクルーターのエンゲージメントと候補者の応答を学習するための深層モデルです。 
We also explore learning to rank approaches applied to deep models, and show the benefits for the talent search use case. 
また、**深層モデルに適用されたランキング学習アプローチを探求**し、タレントサーチのユースケースにおける利点を示します。 
Finally, we present offline and online evaluation results for LinkedIn talent search and recommendation systems, and discuss potential challenges along the path to a fully deep model architecture. 
最後に、LinkedInのタレントサーチおよび推薦システムに対するオフラインおよびオンライン評価結果を示し、**完全な深層モデルアーキテクチャへの道のりにおける潜在的な課題**について議論します。 
The challenges and approaches discussed generalize to any multi-faceted search engine. 
議論された課題とアプローチは、あらゆる多面的な検索エンジンに一般化されます。

<!-- ここまで読んだ! -->

#### KEYWORDS キーワード

search ranking; faceted search; embedding; learning to rank
検索ランキング; ファセット検索; 埋め込み; ランキング学習

#### 1 INTRODUCTION はじめに

LinkedIn Talent Solutions business contributes to around 65% of LinkedIn’s annual revenue[1], and provides tools for job providers to reach out to potential candidates and for job seekers to find suitable career opportunities. 
LinkedInのタレントソリューションビジネスは、LinkedInの年間収益の約65%を占めており、求人提供者が潜在的な候補者にアプローチし、求職者が適切なキャリア機会を見つけるためのツールを提供します。
LinkedIn’s job ecosystem has been designed as a platform to connect job providers and job seekers, and to serve as a marketplace for efficient matching between potential candidates and job openings. 
LinkedInの求人エコシステムは、求人提供者と求職者をつなぐプラットフォームとして設計されており、潜在的な候補者と求人の効率的なマッチングのためのマーケットプレイスとして機能します。
A key mechanism to help achieve these goals is the LinkedIn Recruiter product, which enables recruiters to search for relevant candidates and obtain candidate recommendations for their job postings. 
**これらの目標を達成するための重要なメカニズムは、LinkedIn Recruiter製品**であり、リクルーターが関連する候補者を検索し、求人掲載のための候補者推薦を得ることを可能にします。

A crucial challenge in talent search and recommendation systems is that the underlying query could be quite complex, combining several structured fields (such as canonical title(s), canonical skill(s), company name) and unstructured fields (such as free-text keywords). 
重要な課題は、基礎となるクエリが非常に複雑であり、いくつかの構造化されたフィールド（正規化されたタイトル、正規化されたスキル、会社名など）と非構造化されたフィールド（自由形式のテキストなど）を組み合わせることです。
Depending on the application, the query could either consist of an explicitly entered query text and selected facets (talent search), or be implicit in the form of a job opening, or ideal candidate(s) for a job (talent recommendations). 
アプリケーションによっては、クエリは明示的に入力されたクエリテキストと選択されたファセット（タレントサーチ）で構成される場合もあれば、求人の形で、または求人の理想的な候補者の形で暗黙的に存在する場合もあります（タレント推薦）。
Our goal is to determine a ranked list of most relevant candidates among hundreds of millions of structured candidate profiles. 
私たちの目標は、数億の構造化された候補者プロフィールの中から最も関連性の高い候補者のランキングリストを決定することです。

The structured fields add sparsity to the feature space when used as a part of a machine learning ranking model. 
構造化されたフィールドは、機械学習ランキングモデルの一部として使用されるときに特徴空間にスパース性を追加します。
This setup lends itself well to a dense representation learning experiment as it not only reduces sparsity but also increases sharing of information in feature space. 
この設定は、スパース性を減少させるだけでなく、**特徴空間での情報の共有を増加させるため、密な表現学習**実験に適しています。
In this work, we present the experiences of applying representation learning techniques for talent search ranking at LinkedIn. 
本研究では、**LinkedInにおけるタレント検索ランキングのための表現学習技術の適用経験**を示します。
Our key contributions include: 
私たちの主な貢献は以下の通りです：

1. Using embeddings as features in a learning to rank application. 
ランキングアプリケーションにおける特徴として埋め込みを使用します。
This typically consists of: 
これは通常、以下を含みます：
– Embedding models for ranking, and evaluating the advantage of a layered (fully-connected) architecture,
**– ランキングのための埋め込みモデルと、層状（全結合）アーキテクチャの利点を評価すること、**
**– Considerations while using point-wise learning and pair-wise losses in the cost function to train models.** 
**– モデルをトレーニングするためのコスト関数におけるポイントワイズ学習とペアワイズ損失を使用する際の考慮事項。**

2. Methods for learning semantic representations of sparse entities (such as recruiter id, candidate id, and skill id) using the structure of the LinkedIn Economic Graph [30]: 
LinkedIn Economic Graphの構造を使用してスパースエンティティ（リクルーターID、候補者ID、スキルIDなど）の意味的表現を学習するための方法：
**– Unsupervised representation learning that uses Economic Graph network data across LinkedIn ecosystem** 
**– LinkedInエコシステム全体のEconomic Graphネットワークデータを使用した教師なし表現学習**
**– Supervised representation learning that utilizes application specific data from talent search domain.** 
**– タレント検索ドメインからのアプリケーション特有のデータを利用した教師あり表現学習。**

3. Extensive offline and online evaluation of above approaches in the context of LinkedIn talent search, and a discussion of challenges and lessons learned in practice. 
LinkedInタレント検索の文脈における上記アプローチの広範なオフラインおよびオンライン評価と、**実践での課題と学んだ教訓**についての議論。

Rest of the paper is organized as follows. 
残りの論文は以下のように構成されています。
We present an overview of talent search at LinkedIn, the constraints, challenges and the optimization problem in §2. 
§2では、LinkedInにおけるタレント検索の概要、制約、課題、および最適化問題を示します。
We then describe the methodology for the application of representation learning models in §3, followed by offline and online experimentation results in §4. 
次に、§3で表現学習モデルの適用方法論を説明し、§4ではオフラインおよびオンラインの実験結果を示します。
Finally, we discuss related work in §5, and conclude the paper in §6. 
最後に、§5で関連研究について議論し、§6で論文を締めくくります。

Although much of the discussion is in the context of search at LinkedIn, it generalizes well to any multi-faceted search engine where there are high dimensional facets, i.e. movie, food / restaurant, product search are a few examples that would help the reader connect to the scale of the problem. 
多くの議論はLinkedInでの検索の文脈にありますが、高次元のファセットが存在する任意の多面的検索エンジンにもうまく一般化されます。つまり、映画、食べ物/レストラン、製品検索は、問題の規模を読者が理解するのに役立ついくつかの例です。

<!-- ここまで読んだ! -->

#### 2 BACKGROUND AND PROBLEM SETTING 背景と問題設定

We next provide a brief overview of the LinkedIn Recruiter product and existing ranking models, and formally present the talent search ranking problem.
次に、LinkedIn Recruiter製品と既存のランキングモデルの簡単な概要を提供し、タレント検索ランキング問題を正式に提示します。

#### 2.1 背景

LinkedIn is the world’s largest professional network with over 500 million members world-wide. 
LinkedInは、全世界で5億人以上のメンバーを持つ世界最大のプロフェッショナルネットワークです。
Each member of LinkedIn has a profile page that serves as a professional record of achievements and qualifications, as shown in Figure 1. 
LinkedInの各メンバーは、Figure 1に示されているように、業績や資格のプロフェッショナルな記録として機能するプロフィールページを持っています。
A typical member profile contains around 5 to 40 structured and unstructured fields including title, company, experience, skills, education, and summary, amongst others. 
典型的なメンバープロフィールには、タイトル、会社、経験、スキル、教育、要約など、**約5から40の構造化されたおよび非構造化されたフィールド**が含まれています。

In the context of talent search, LinkedIn members can be divided into two categories: candidates (job seekers) and recruiters (job providers). 
タレントサーチの文脈において、LinkedInのメンバーは候補者（求職者）とリクルーター（求人提供者）の2つのカテゴリに分けることができます。
Candidates look for suitable job opportunities, while recruiters seek candidates to fill job openings. 
候補者は適切な仕事の機会を探し、リクルーターは求人を埋めるための候補者を探します。
In this work, we address the modeling challenges in the LinkedIn Recruiter product, which helps recruiters find and connect with the right candidates.
本研究では、リクルーターが適切な候補者を見つけて接続するのを助けるLinkedIn Recruiter製品におけるモデリングの課題に取り組みます。

Consider an example of a recruiter looking for a software engineer with machine learning background. 
機械学習のバックグラウンドを持つソフトウェアエンジニアを探しているリクルーターの例を考えてみましょう。
Once the recruiter types keywords software engineer and machine learning as a free text query, the recruiter search engine first standardizes them into the title, software engineer and the skill, machine learning. 
リクルーターがキーワード「ソフトウェアエンジニア」と「機械学習」を自由形式のクエリとして入力すると、リクルーターの検索エンジンはまずそれらをタイトル「ソフトウェアエンジニア」とスキル「機械学習」に標準化します。
Then, it matches these standardized entities with standardized member profiles, and the most relevant candidate results are presented as in Figure 2. 
次に、これらの標準化されたエンティティを標準化されたメンバープロフィールと照合し、最も関連性の高い候補者の結果がFigure 2のように提示されます。
In order to find a desired candidate, the recruiter can further refine their search criteria using facets such as title, location, and industry. 
希望する候補者を見つけるために、リクルーターはタイトル、場所、業界などのファセットを使用して検索条件をさらに絞り込むことができます。
For each result, the recruiter can perform the following actions (shown in the increasing order of recruiter’s interest for the candidate): 
**各結果に対して、リクルーターは以下のアクションを実行できます（候補者に対するリクルーターの関心の高まりの順に示されています）**：
(こんな感じで各アクションを整理するのいいな...!:thinking:)

(1) View a candidate profile, 
    (1) 候補者のプロフィールを表示する、

(2) Bookmark a profile for detailed evaluation later, 
    (2) 後で詳細評価のためにプロフィールをブックマークする、

(3) Save a profile to their current hiring project (as a potential fit), and, 
    (3) 現在の採用プロジェクトにプロフィールを保存する（潜在的な適合として）、

(4) Send an inMail (message) to the candidate. 
    (4) 候補者にinMail（メッセージ）を送信する。

<!-- ここまで読んだ! -->

Unlike traditional search and recommendation systems which solely focus on estimating how relevant an item is for a given query, the talent search domain requires mutual interest between the recruiter and the candidate in the context of the job opportunity. 
従来の検索および推薦システムが特定のクエリに対してアイテムの関連性を推定することにのみ焦点を当てているのに対し、**タレントサーチの領域では、求人の文脈においてリクルーターと候補者の相互の関心が必要**です。
In other words, we simultaneously require that a candidate shown must be relevant to the recruiter’s query, and that the candidate contacted by the recruiter must also show interest in the job opportunity. 
言い換えれば、表示される候補者がリクルーターのクエリに関連している必要があり、リクルーターによって連絡された候補者も求人に興味を示す必要があります。
Therefore, we define a new action event, inMail Accept, which occurs when a candidate replies to an inMail from a recruiter with a positive response.
したがって、**リクルーターからのinMailに候補者が肯定的な返答をしたときに発生する新しいアクションイベント「inMail Accept」を定義**します。(相互推薦的な考慮が必要だよ〜ってことね...!!:thinking:)
Indeed, the key business metric in the Recruiter product is based on inMail Accepts and hence we use the fraction of top k ranked candidates that received and accepted an inMail (viewed as precision@k [2]) as the main evaluation measure for our experiments.
実際、リクルーター製品における主要なビジネスメトリックはinMail Acceptsに基づいており、したがって、inMailを受け取り、受け入れた上位k位の候補者の割合（precision@k [2]として見なされる）を私たちの実験の主要な評価指標として使用します。

<!-- ここまで読んだ! -->

#### 2.2 Current Models 現在のモデル

The current talent search ranking system functions as follows [12, 13]. 
現在のタレントサーチランキングシステムは次のように機能します[12, 13]。
In the first step, the system retrieves a candidate set of a few thousand members from over 500 million LinkedIn members, utilizing hard filters specified in the search query. 
最初のステップでは、システムは検索クエリで指定されたハードフィルターを利用して、5億人以上のLinkedInメンバーから数千人の候補者セットを取得します。
In particular, a query request is created based on the standardized fields extracted from the free form text in the query, as well as the selected facets (such as skill, title, and industry). 
特に、クエリに含まれる自由形式のテキストから抽出された標準化されたフィールドと、選択されたファセット（スキル、職位、業界など）に基づいてクエリリクエストが作成されます。
This query request is then issued to the distributed search service tier, which is built on top of LinkedIn’s _Galene search platform [26]. 
このクエリリクエストは、LinkedInの_Galene検索プラットフォーム[26]の上に構築された分散検索サービス層に送信されます。
A list of candidates is generated based on the matching features (such as title or skill match). 
候補者のリストは、マッチング機能（職位やスキルの一致など）に基づいて生成されます。
In the second step, the search ranker scores the resulting candidates using a ranking model, and returns the top ranked candidate results. 
**次のステップでは、検索ランカーがランキングモデルを使用して結果として得られた候補者にスコアを付け、上位の候補者結果を返します。**
In this paper, we focus on the ranking model used in the second step. 
**本論文では、第二ステップで使用されるランキングモデルに焦点を当てます。**

(下記を読んだ感じ、元々のcontrolモデルはtree ensembleベースのモデルだったっぽいな...!!:thinking:)

Tree ensembles, viewed as non-linear models capable of discovering “interaction features”, have been studied extensively both in academic and industrial settings. 
「相互作用特徴」を発見できる非線形モデルとして見なされるツリーアンサンブルは、学術的および産業的な環境で広く研究されています。
For LinkedIn Talent Search, we have studied the effectiveness of ensemble trees and found that GBDT (Gradient Boosted Decision Trees) models [6, 9] outperform the best logistic regression models on different data sets as measured by area under ROC curve (AUC) and precision@k metrics in offline experiments. 
LinkedInタレントサーチにおいて、私たちはアンサンブルツリーの効果を研究し、GBDT（勾配ブースト決定木）モデル[6, 9]がオフライン実験においてROC曲線下面積（AUC）およびprecision@kメトリックで異なるデータセットに対して最良のロジスティック回帰モデルを上回ることを発見しました。
More importantly, online A/B tests have shown significant improvement across all key metrics based on inMail Accepts (Table 1). 
さらに重要なことに、オンラインA/Bテストは、inMailの受諾に基づいてすべての主要なメトリックでの顕著な改善を示しました（表1）。
Having described the current state of the talent search ranking models, we next formally present the problem setting and the associated challenges. 
現在のタレントサーチランキングモデルの状態を説明した後、次に問題設定と関連する課題を正式に提示します。

2 While metrics like Normalized Discounted Cumulative Gain [16] are more commonly utilized for ranking applications, we have found precision@k to be more suitable as a business metric. 
2 **正規化割引累積ゲイン（Normalized Discounted Cumulative Gain）[16]のような指標はランキングアプリケーションでより一般的に利用されていますが、私たちはprecision@kがビジネス指標としてより適していると考えています**。(自社プロダクトで一番適してるのは何か、はちゃんと考えていきたいよね...!!:thinking:)
Precision@k also aligns well with the way the results are presented in LinkedIn Recruiter application, where each page lists up to 25 candidates by default so that precision@25 is a measure of positive outcome in the first page.  
Precision@kは、LinkedIn Recruiterアプリケーションで結果が表示される方法ともよく一致しており、各ページにはデフォルトで最大25人の候補者がリストされるため、precision@25は最初のページでのポジティブな結果の指標となります。

<!-- ここまで読んだ! -->

#### 2.3 問題設定と課題

Table 1: Results of an online A/B test we performed over** **a period of three weeks in 2017, demonstrating the preci-** **sion improvement for the gradient boosted decision tree** **model compared to the baseline logistic regression model** **for LinkedIn Talent Search. We compute precision as the** **fraction of the top ranked candidate results that received** **and accepted an inMail, within three days of the inMail be-** **ing sent by the recruiter (Prec@k is over the top k candidate** **results), and show the relative lift in precision. We note that** **these improvements are impressive based on our experience** **in the domain.**
**表1: 2017年に3週間にわたって実施したオンラインA/Bテストの結果。** **LinkedIn Talent Searchにおけるベースラインのロジスティック回帰モデルと比較した場合の、勾配ブースト決定木モデルの精度向上を示しています。** **精度は、リクルーターから送信されたinMailの3日以内に受信し、受け入れた上位ランクの候補者結果の割合として計算します（Prec@kは上位k候補者結果に対するものです）。** **また、精度の相対的な向上を示します。これらの改善は、私たちのドメインでの経験に基づいて印象的であることに注意します。**
**Prec@5** **Prec@25** **全体の精度**

_Definition 2.1. Given a search query consisting of search criteria_ such as title, skills, and location, provided by the recruiter or the hiring manager, the goal of Talent Search Ranking is to:
_定義 2.1. リクルーターまたは採用マネージャーによって提供された、タイトル、スキル、場所などの検索基準から構成される検索クエリが与えられたとき、タレントサーチランキングの目標は次のとおりです: 

(1) Determine a set of candidates strictly satisfying the specified search criteria (hard constraints), and,  
    (1) 指定された検索基準（ハード制約）を厳密に満たす候補者のセットを決定します。

(2) Rank the candidates according to their utility for the recruiter, where the utility is the likelihood that the candidate would be a good fit for the position, and would be willing to accept the request (inMail) from the recruiter.
    (2) リクルーターにとっての有用性に基づいて候補者をランク付けします。有用性とは、候補者がそのポジションに適している可能性と、リクルーターからのリクエスト（inMail）を受け入れる意欲を指します。

(↑ うん、検索っぽい目標だ。:thinking:)

As discussed in §2.2, the existing ranking system powering LinkedIn Recruiter product utilizes a GBDT model due to its advantages over linear models.  
§2.2で述べたように、LinkedIn Recruiter製品を支える**既存のランキングシステムは、線形モデルに対する利点からGBDTモデルを利用**しています。
While GBDT provides quite a strong performance, it poses the following challenges:  
GBDTは非常に強力なパフォーマンスを提供しますが、以下の課題があります。

(1) It is quite non-trivial to augment a tree ensemble model with other trainable components such as embeddings for discrete features.  
    (1) 離散特徴の埋め込みなどの他の学習可能なコンポーネントでツリーアンサンブルモデルを拡張することは非常に非自明です。(entity embeddingとかできないよね、みたいな話??:thinking:)
    Such practices typically require joint training of the model with the component/feature, while the tree ensemble model assumes that the features themselves need not be trained.  
    このような手法は通常、コンポーネント/特徴と共にモデルの共同トレーニングを必要としますが、ツリーアンサンブルモデルは特徴自体はトレーニングする必要がないと仮定しています。

(2) Tree models do not work well with sparse id features such as skill ids, company ids, and member ids that we may want to utilize for talent search ranking.  
    (2) ツリーモデルは、タレントサーチランキングに利用したい可能性のあるスキルID、会社ID、メンバーIDなどのスパースID特徴ではうまく機能しません。
    Since a sparse feature is non-zero for a relatively small number of examples, it has a small likelihood to be chosen by the tree generation at each boosting step, especially since the learned trees are shallow in general.  
    スパース特徴は比較的少数の例に対して非ゼロであるため、特に学習された木が一般的に浅いことから、各ブースティングステップでツリー生成によって選ばれる可能性は小さくなります。

(3) Tree models lack flexibility of model engineering.  
    (3) ツリーモデルはモデルエンジニアリングの柔軟性に欠けます。
    It might be desirable to use novel loss functions, or augment the current objective function with other terms.  
    **新しい損失関数を使用したり、現在の目的関数に他の項を追加したり**することが望ましい場合があります。
    Such modifications are not easily achievable with GBDT models, but are relatively straight-forward for deep learning models based on differentiable programming.  
    このような修正はGBDTモデルでは容易に実現できませんが、**微分可能プログラミングに基づく深層学習モデルでは比較的簡単**です。
    A neural network model with a final (generalized) linear layer also makes it easier to adopt approaches such as transfer learning and online learning.  
    **最終的な（一般化された）線形層を持つニューラルネットワークモデルは、転移学習やオンライン学習などのアプローチを採用するのを容易**にします。(確かに、これもtree系モデルだとやりづらいのか...!:thinking:)

In order to overcome these challenges, we explore the usage of neural network based models, which provide sufficient flexibility in the design and model specification.  
これらの課題を克服するために、設計とモデル仕様において十分な柔軟性を提供するニューラルネットワークベースのモデルの使用を探ります。

Another significant challenge pertains to the sheer number of available entities that a recruiter can include as part of their search, and how to utilize them for candidate selection as well as ranking.  
**もう一つの重要な課題は、リクルーターが検索の一部として含めることができる利用可能なエンティティの数が非常に多いこと**であり、それらを候補者の選択やランキングにどのように利用するかです。
For example, the recruiter can choose from tens of thousands of LinkedIn’s standardized skills.  
例えば、リクルーターはLinkedInの標準化されたスキルの中から数万の選択肢から選ぶことができます。
Since different entities could be related to each other (to a varying degree), using syntactic features (e.g., fraction of query skills possessed by a candidate) has its limitations.  
**異なるエンティティが互いに関連している可能性**があるため（その程度はさまざまですが）、構文的特徴（例：候補者が持つクエリスキルの割合）を使用することには限界があります。
Instead, it is more desirable to utilize semantic representations of entities, for example, in the form of low dimensional embeddings.  
代わりに、例えば低次元の埋め込みの形で、エンティティの意味的表現を利用することがより望ましいです。
Such representations allow for numerous sparse entities to be better incorporated as part of a machine learning model.  
このような表現は、多数のスパースエンティティを機械学習モデルの一部としてより良く組み込むことを可能にします。
Therefore, in this work, we also investigate the application of representation learning for entities in the talent search domain.  
したがって、本研究では、タレントサーチドメインにおけるエンティティの表現学習の適用についても調査します。

<!-- ここまで読んだ! -->

#### 3 METHODOLOGY 方法論

In this section, we present our methodology which focuses on two main aspects:  
このセクションでは、私たちの方法論を提示します。これは主に二つの側面に焦点を当てています。

- Learning of deep models to estimate likelihood of the two way interest (inMail accept) between the candidate and the recruiter,  
候補者とリクルーターの間の二方向の関心（inMail受諾）の可能性を推定するための深層モデルの学習、

- Learning of supervised and unsupervised embeddings of the entities in the talent search domain.  
タレント検索ドメインにおける**エンティティの教師ありおよび教師なしの埋め込みの学習**です。

In Table 2, we present the notation used in the rest of the section.  
表2では、残りのセクションで使用される表記法を示します。
Note that the term example refers to a candidate that is presented to the recruiter.  
「例」という用語は、リクルーターに提示される候補者を指します。

**Table 2: Notations**  
**表2: 表記法**  

- $n$ : size of training set
- $x_{i}$ : feature vector for the $i$[th] training example 特徴量ベクトル
- $y_{i}$ : binary responsefor the $i$[th] training example (1 if inMail accepted, 0 otherwise) binaryの応答アクション。
- $s_{i}$ : the search session to which the $i$[th] training example belongs $i$[番目]のトレーニング例が属する検索セッション
- $tuple(x_i, y_i, s_i)$ : the $i$[th] example in the training set トレーニングセット内の$i$[番目]の例
- $w$ : weight vector 重みベクトル
- $<·,·>$ : dot product ドット積
- $\psi(·)$ : neural network function ニューラルネットワーク関数
- $u_{j} \in \mathbb{R}^{d}$: $d$ dimensional vector representation (embedding) of entity $j$ エンティティ$j$の$d$次元ベクトル表現（埋め込み）

<!-- ここまで読んだ! -->

#### 3.1 Embedding Models for Ranking

(ランキングもembedddingモデルというか、表現学習的なモデルなんだな! じゃあきっとtwo-towerモデルだな...!:thinking:)

As mentioned before, we would like to have a flexible ranking model that allows for easy adaptation to novel features and training schemes. 
前述のように、私たちは**新しい特徴やトレーニングスキームに容易に適応できる柔軟なランキングモデル**を持ちたいと考えています。
Neural networks, especially in the light of recent advances that have made them the state of the art for many statistical learning tasks including learning to rank [4, 19], are the ideal choice owing to their modular structure and their ability to be trained end-to-end using straightforward gradient based optimization. 
**ニューラルネットワークは、特にランキング学習を含む多くの統計学習タスクにおいてstate of the artを実現した最近の進歩**に照らして、**モジュラー構造と単純な勾配ベースの最適化を使用してエンドツーエンドでトレーニングできる能力により、理想的な選択肢**です。
Hence we would like to use neural network rankers as part of our ranking models for Talent Search at LinkedIn. 
したがって、私たちはLinkedInのTalent Searchのランキングモデルの一部としてニューラルネットワークランカーを使用したいと考えています。
Specifically, we propose to utilize multilayer perceptron (MLP) with custom unit activations for the ranking task. 
具体的には、ランキングタスクのためにカスタムユニット活性化を持つ多層パーセプトロン（MLP）を利用することを提案します。
Our model supports a mix of model regularization methods including L2 norm penalty and dropout [27]. 
私たちのモデルは、L2ノルムペナルティやドロップアウト[27]を含むモデル正則化手法の混合をサポートしています。

<!-- ここまで読んだ! -->

For the training objective of the neural network, we consider two prevalent methodologies used in learning to rank: 
ニューラルネットワークのトレーニング目的として、ランキング学習で使用される2つの一般的な方法論を考慮します：

##### _3.1.1_ _Pointwise Learning.  _3.1.1_ _ポイントワイズ学習。_

Also called ranking by binary classification, this method involves training a binary classifier utilizing each example in the training set with their labels, and then grouping the examples from the same search session together and ranking them based on their scores. 
バイナリ分類によるランキングとも呼ばれるこの方法は、**トレーニングセット内の各例をそのラベルを用いてバイナリ分類器でトレーニング**し、同じ検索セッションからの例をグループ化してスコアに基づいてランキングします。
For this purpose, we apply logistic regression on top of the neural network as follows. 
この目的のために、次のようにニューラルネットワークの上にロジスティック回帰を適用します。
We include a classification layer which sums the output activations from the neural network, passes the sum through the logistic function, and then trains against the labels using the cross entropy cost function: 
出力活性化を合計する分類層を含め、その合計をロジスティック関数に通し、次にクロスエントロピーコスト関数を使用してラベルに対してトレーニングします：

$$
\sigma_i = \frac{1}{1 + \exp(- w \cdot \psi(x_i))}, 
i \in {1, 2, ..., n}
\tag{1}
$$

$$
L = -\sum_{i=1}^{n} y_i \log(\sigma_i) + (1 - y_i) \log(1 - \sigma_i).
\tag{2}
$$

In above equations, $\psi(·)$ refers to the neural network function, and $\sigma_i$ is the value of the logistic function applied to the score for the $i$[th] training example. 
上記の式において、$\psi(·)$はニューラルネットワーク関数を指し、$\sigma_i$は$i$[番目]のトレーニング例のスコアに適用されるロジスティック関数の値です。

<!-- ここまで読んだ! -->

##### _3.1.2_ _Pairwise Learning. _3.1.2_ _ペアワイズ学習。_

Although pointwise learning is simple to implement and works reasonably well, the main goal for talent search ranking is to provide a ranking of candidates which is guided by the information inherent in available session-based data. 
**ポイントワイズ学習は実装が簡単で合理的に機能しますが**、タレントサーチランキングの主な目標は、利用可能なセッションベースのデータに内在する情報に基づいて候補者のランキングを提供することです。
Since it is desirable to compare candidates within the same session depending on how they differ with respect to the mutual interest between the recruiter and the candidate (inMail accept), we form pairs of examples with positive and negative labels respectively from the same session and train the network to maximize the difference of scores between the paired positive and negative examples: 
リクルーターと候補者（inMail受諾）との相互関心に関してどのように異なるかに基づいて、**同じセッション内で候補者を比較することが望ましい**ため、**同じセッションからそれぞれ正と負のラベルを持つ例のペアを形成し、ペアの正と負の例のスコアの差を最大化するように**ネットワークをトレーニングします：
(contrastive learningはどっちかっていうとpairwiseやlistwise学習に近い考え方だよな〜...!!:thinking:)

$$
d_{i+, i-} = w \cdot ( \psi(x_{i+}) - \psi(x_{i-}) ),
\tag{3}
$$

$$
L = \sum_{(i+, i-) : s_{i+} = s_{i-}, y_{i+} = 1, y_{i-} = 0} f(d_{i+, i-}),
\tag{4}
$$

The score difference between a positive and a negative example is denoted by $d_{i+},i-$, with $i[+]$ and $i[-]$ indicating the indices for a positive and a negative example, respectively. 
正の例と負の例のスコアの差は $d_{i+, i-}$で表され、$i[+]$ と $i[-]$ はそれぞれ正の例と負の例のインデックスを示します。
The function $f(·)$ determines the loss, and (4) becomes equivalent to the objective of RankNet [4] when $f$ is the logistic loss: 
関数 $f(·)$ は損失を決定し、(4)は $f$ がロジスティック損失であるときにRankNet [4]の目的に等しくなります：

$$
f(d_{i+},i-) = \log \left( \frac{1}{1 + \exp(-d_{i+, i-})} \right).
$$

whereas (4) becomes equivalent to ranking SVM objective [17] when $f$ is the hinge loss: 
一方、(4)は$f$がヒンジ損失であるときにランキングSVMの目的[17]に等しくなります：

$$
f(d_{i+},i-) = \max(0, 1 - d_{i+, i-}).
$$

We implemented both pointwise and pairwise learning objectives. 
私たちはポイントワイズとペアワイズの両方の学習目的を実装しました。
For the latter, we chose hinge loss over logistic loss due to faster training times, and our observation that the precision values did not differ significantly (we present the evaluation results for point-wise and hinge loss based pairwise learning in §4). 
**後者については、トレーニング時間が短縮されるためロジスティック損失よりもヒンジ損失を選択し、精度値に大きな差がないことを観察**しました（ポイントワイズとヒンジ損失に基づくペアワイズ学習の評価結果は§4で示します）。
(hinge lossってのがあるのか...! 距離指標が逆になってたら0にするってことか...!:thinking:)

<!-- ここまで読んだ! -->

#### 3.2 Talent Searchにおけるスパースエンティティのセマンティック表現の学習



Next, we would like to focus on the problem of sparse entity representation, which allows for the translation of the various entities (skills, titles, etc.) into a low-dimensional vector form. 
次に、**さまざまなエンティティ（スキル、職位など）を低次元のベクトル形式に変換することを可能にするスパースエンティティ表現の問題**に焦点を当てたいと思います。 
Such a translation makes it possible for various types of models to directly utilize the entities as part of the feature vector, e.g., §3.1. 
このような変換により、さまざまなタイプのモデルがエンティティを特徴ベクトルの一部として直接利用できるようになります（例：§3.1）。
To achieve this task of generating vector representations, we re-formulate the talent search problem as follows: given a query q by a recruiter _ri_, rank a list of LinkedIn members m1, _m2, ...,_ _md in the order of_ decreasing relevance.
**ベクトル表現を生成するこのタスクを達成するために、タレントサーチの問題を次のように再定義します：リクルーター $r_i$によるクエリ $q$ が与えられた場合、LinkedInメンバー $m_1, m_2, ..., m_d$ のリストを関連性の低い順にランク付けします。**
In other words, we want to learn a function that assigns a score for each potential candidate, corresponding to the query issued by the recruiter. 
言い換えれば、リクルーターによって発行されたクエリに対応する各潜在的候補者にスコアを割り当てる関数を学習したいと考えています。 
Such a function can learn a representation for query and member pair, and perform final scoring afterwards. 
このような関数は、クエリとメンバーのペアの表現を学習し、その後最終的なスコアリングを行うことができます。 
We consider two broad approaches for learning these representations. 
これらの表現を学習するための**2つの大まかなアプローチ**を考慮します。 

- The unsupervised approach learns a shared representation space for the entities, thereby constructing a query representation and a member representation. 
  - 教師なしアプローチは、エンティティのための共有表現空間を学習し、クエリ表現とメンバー表現を構築します。 
    We do not use talent search specific interactions to supervise the learning of representations. 
    タレントサーチ特有のインタラクションを使用して表現の学習を監視することはありません。 

- The supervised approach utilizes the interactions between recruiters and candidates in historical search results while learning both representation space as well as the final scoring. 
  - 教師ありアプローチは、過去の検索結果におけるリクルーターと候補者のインタラクションを利用し、表現空間と最終スコアリングの両方を学習します。 

The architecture for learning these representations and the associated models is guided by the need to scale for deployment to production systems that serve over 500M members. 
これらの表現を学習するためのアーキテクチャと関連するモデルは、5億人以上のメンバーにサービスを提供するプロダクションシステムへの展開のためにスケールする必要性に基づいています。 
For this reason, we split the network scoring of query-member pair into three semantic pieces, namely query network, member network, and cross network, such that each piece is run on one of the production systems as given in Figure 3. 
このため、クエリ-メンバーペアのネットワークスコアリングを**3つのセマンティックな部分、すなわちクエリネットワーク、メンバーネットワーク、クロスネットワークに分割**し、各部分が図3に示すプロダクションシステムの1つで実行されるようにします。 
(これって結局two-towerモデルアーキテクチャにおける、query encoder, item encoder, score prediction moduleと同一で良さそう...! 図3を見た感じ、cross networkは単純なdot productっぽいし...!:thinking:)

![]()
**Figure 3: The two arm architecture with a shallow query arm** **and a deep member arm**  
**図3：浅いクエリアームと深いメンバーアームを持つ二腕アーキテクチャ**

<!-- ここまで読んだ! -->

##### _3.2.1_ _Unsupervised Embeddings. _3.2.1_ _教師なし埋め込み。

Most features used in_ LinkedIn talent search and recommendation models are categorical in nature, representing entities such as skill, title, school, company, and other attributes of a member’s profile. 
LinkedInのタレントサーチおよび推薦モデルで使用されるほとんどの特徴は、スキル、職位、学校、会社、メンバーのプロフィールの他の属性などのエンティティを表すカテゴリカルな性質を持っています。 
In fact, to achieve personalization, even the member herself could be represented as a categorical feature via her LinkedIn member Id. 
実際、パーソナライズを達成するために、**メンバー自身もLinkedInメンバーIDを介してカテゴリカルな特徴として表現される可能性**があります。(うんうん...!:thinking:)
Such categorical features often suffer from sparsity issues because of the large search space, and learning a dense representation to represent these entities has the potential to improve model performance. 
このようなカテゴリカルな特徴は、大きな検索空間のためにスパース性の問題に悩まされることが多く、**これらのエンティティを表現するための密な表現を学習することは、モデルのパフォーマンスを向上させる可能性があります**。 
While commonly used algorithms such as word2vec [20] work well on text data when there is information encoded in the sequence of entities, they cannot be directly applied to our use case. 
一般的に使用されるアルゴリズムであるword2vec [20]は、エンティティのシーケンスに情報がエンコードされている場合、テキストデータでうまく機能しますが、私たちのユースケースには直接適用できません。 
Instead, we make use of LinkedIn Economic Graph [30] to learn the dense entity representations. 
代わりに、**LinkedIn Economic Graph [30]を利用して密なエンティティ表現を学習**します。(graph embeddingを使うって話か...!:thinking:)

LinkedIn Economic Graph is a digital representation of the global economy based on data generated from over 500 million members, tens of thousands of standardized skills, millions of employers and open jobs, as well as tens of thousands of educational institutions, along with the relationships between these entities. 
LinkedIn Economic Graphは、5億人以上のメンバー、数万の標準化されたスキル、数百万の雇用主とオープンジョブ、さらに数万の教育機関から生成されたデータに基づく、グローバル経済のデジタル表現です。
It is a compact representation of all the data on LinkedIn. 
これは、LinkedIn上のすべてのデータのコンパクトな表現です。
To obtain a representation for the entities using the Economic Graph, we could use a variety of graph embedding algorithms (see §5). 
Economic Graphを使用してエンティティの表現を取得するために、さまざまなグラフ埋め込みアルゴリズムを使用できます（§5を参照）。 
For the purposes of this work, we adopted Large-Scale Information Network Embeddings approach [28], by changing how we construct the graph. 
この作業の目的のために、グラフの構築方法を変更することにより、Large-Scale Information Network Embeddingsアプローチ [28]を採用しました。 
In [28], the authors construct the graph of a social network by defining the members of the network as vertices, and use some form of interaction (clicks, connections, or social actions) between members to compute the weight of the edge between any two members. 
[28]では、著者はネットワークのメンバーを頂点として定義し、メンバー間のインタラクション（クリック、接続、またはソーシャルアクション）のいずれかの形式を使用して、任意の2つのメンバー間のエッジの重みを計算することで、ソーシャルネットワークのグラフを構築します。 
In our case, this would create a large sparse graph resulting in intractable training and a noisy model. 
私たちのケースでは、これにより大きなスパースグラフが生成され、扱いきれないトレーニングとノイズの多いモデルが生じます。 
Instead, we define a weighted graph, _G = (V_, E, _w..) over the entities whose representations need to be_ learned (e.g., skill, title, company), and use the number of members sharing the same entity on their profile to induce an edge weight (w..) between the vertices. 
代わりに、学習する必要のあるエンティティ（例：スキル、職位、会社）に対して、重み付きグラフ $G = (V, E, w..)$ を定義し、プロフィールで同じエンティティを共有するメンバーの数を使用して、頂点間のエッジの重み（w..）を誘導します。
Thus we reduce the size of the problem by a few orders of magnitude by constructing a smaller and denser graph. 
このようにして、より小さく密なグラフを構築することにより、問題のサイズを数桁減少させます。 

<!-- ここまで読んだ! -->

An illustrative sub-network of the graph used to construct company embeddings is presented in Figure 4. 
会社の埋め込みを構築するために使用されるグラフの説明的なサブネットワークが図4に示されています。 
Each vertex in the graph represents a company, and the edge weight (denoted by the edge thickness) represents the number of LinkedIn members that have worked at both companies (similar graphs can be constructed for other entity types such as skills and schools). 
グラフの各頂点は会社を表し、エッジの重み（エッジの太さで示される）は、両方の会社で働いたLinkedInメンバーの数を表します（スキルや学校などの他のエンティティタイプに対しても同様のグラフを構築できます）。 
In the example, our aim would be to embed each company (i.e., each vertex in the graph) into a fixed dimensional latent space. 
この例では、**各会社（すなわち、グラフの各頂点）を固定次元の潜在空間に埋め込むことを目指します**。(ニュース推薦でも、ノード=ユーザ, エッジの重み=共通ニュース閲覧数みたいなグラフを作ったら、graph embeddingでユーザ埋め込みが作れそうだな...! ユーザとニュース逆の方がいいのかな??:thinking:)
We propose to learn first or_der and second order embeddings from this graph.
このグラフから第一および第二のオーダーの埋め込みを学習することを提案します。 
Our approach,_ presented below, is similar to the one proposed in [28]. 
以下に示す私たちのアプローチは、[28]で提案されたものに似ています。 

**First order embeddings Corresponding to each undirected** edge between vertices vi and vj, we define the joint probability between vertices vi and vj as: 
**第一オーダー埋め込み：頂点 vi と vj の間の各無向エッジに対応して、頂点 vi と vj の間の結合確率を次のように定義します：**

$$
p1(vi, vj) = \frac{1}{Z} \cdot \frac{1}{1 + exp(- (u_i · u_j))},
\tag{5}
$$ 

where $u_i in \mathbb{R}^d$ is the d-dimensional vector representation of vertex $v_i$, and $Z = \sum_{(vi,vj) \in E} \frac{1}{1 + exp(- (u_i · u_j))}$ is the normalization factor.
ここで、$u_i in \mathbb{R}^d$ は頂点 $v_i$ のd次元ベクトル表現であり、$Z = \sum_{(vi,vj) \in E} \frac{1}{1 + exp(- (u_i · u_j))}$ は正規化因子です。
The emprical probability, $\hat{p1}(·, ·)$ over the space $V × V$ can be calculated using:
空間 $V × V$ における経験的確率 $\hat{p1}(vi, vj)$ は次のように計算できます：

$$
\hat{p1}(vi, vj) = \frac{w_{ij}}{W}
\tag{6}
$$

where $w_{ij}$ is the edge weight in the company graph, and $W = \sum_{(vi,vj) \in E} w_{ij}$.
ここで、$w_{ij}$ は会社グラフにおけるエッジの重みであり、$W = \sum_{(vi,vj) \in E} w_{ij}$です。
Wh minimize the following objective function in order to preserve the first-order proximity:

$$
O_{1} = d(\hat{p1}(·, ·), p1(·, ·))
\tag{7}
$$

where $d(·, ·)$ is a measure of dissimilarity between two probability distributions.
ここで、$d(·, ·)$ は2つの確率分布間の非類似性の尺度(=距離指標的な...!:thinking:)です。
We chose to minimize KL-divergence of $\hat{p1}(·, ·)$ with respect to $p1(·, ·)$:

$$
O_{1} = - \sum_{(vi,vj) \in E} \hat{p1}(vi, vj) \log{\frac{p1(vi, vj)}{\hat{p1}(vi, vj)}}
\tag{8}
$$

<!-- ここまで読んだ! -->

**Second order embeddings Second order embeddings are gen-** erated based on the observation that vertices with shared neighbors are similar. 
**第二オーダー埋め込み：第二オーダー埋め込みは、共有の隣接点を持つ頂点が類似しているという観察に基づいて生成されます。** 
In this case, each vertex plays two roles: the vertex itself, and a specific context of other vertices. 
この場合、各頂点は2つの役割を果たします：頂点自体と他の頂点の特定のコンテキストです。 
Let _ui and_ _ui_ [′] be two vectors, where ui is the representation of vi when it is treated as a vertex, while ui [′] is the representation of vi when it is used as a specific context. 
$u_{i}$ と $u_i^{′}$ を2つのベクトルとし、$u_i$ は頂点として扱われるときの $v_i$ の表現であり、$u_i^{′}$ は特定のコンテキストとして使用されるときの $v_i$ の表現です。
For each directed edge (i, j), we define the probability of context vj to be generated by vertex vi as follows: 
各有向エッジ $(i, j)$ に対して、頂点 $v_i$ によって生成されるコンテキスト $v_j$ の確率を次のように定義します：

$$
p2(v_j | vi) = \frac{ \exp{(u_j^{′} \cdot u_i)} }{ \sum_{k=1}^{|V|} \exp{(u_k^{′} · u_i)} }
\tag{9}
$$ 

The corresponding empirical probability can be obtained as: 
対応する経験的確率は次のように得られます: 
(こっちが観測済みデータによって計算済みのやつ。経験平均...!:thinking:)

$$
\hat{p2}(vj | vi) = \frac{w_{ij}}{W_i}
\tag{10}
$$ 

where Wi = _wij_. In order to preserve the second order proximity, we aim to make conditional probability distribution of contexts, p2(·|vi), to be close to empirical probability distribution _pˆ2(·|vi), by minimizing the following objective function: 
ここで、$W_i = \sum_{j : (vi, vj) ∈ E} w_{ij}$ です。第二オーダーの近接性を保持するために、次の目的関数を最小化することにより、コンテキストの条件付き確率分布 $p2(·|vi)$ を経験的確率分布 $\hat{p2}(·|vi)$ に近づけることを目指します：

$$
O_{2} = \sum_{v_i ∈ V} \lambda_i · d(\hat{p2}(· | vi), p2(· | vi))
\tag{11}
$$ 

where d(·, ·) is a measure of dissimilarity between two probability distributions, and $\lambda_i$ represents the importance of vertex $v_i$ (e.g., computed using PageRank algorithm). 
ここで、d(·, ·) は2つの確率分布間の非類似性の尺度であり、$\lambda_i$ は頂点 $v_i$ の重要性を表します（例：PageRankアルゴリズムを使用して計算されます）。
In this work, for simplicity, we set λi to be the degree of vertex vi. 
この作業では、単純さのために、$\lambda_i$ を頂点 $v_i$ の次数に設定します。
(メモ: ノードの次数 = そのノードに接続しているエッジの数らしい...!:thinking:)
Using KL-divergence as before, the objective function for the second order embeddings can be rewritten as: 
以前と同様にKLダイバージェンスを使用して、第二オーダー埋め込みの目的関数は次のように書き換えることができます： 

$$
O_{2} = \sum_{v_i \in V} \lambda_i · \sum_{ v_j: (vi,vj) \in E } \hat{p2}(vj | vi) \log{\frac{p2(vj | vi)}{\hat{p2}(vj | vi)}}
\tag{12}
$$ 

<!-- ここまで読んだ! -->

Using Figure 4, we can now explain how the feature is constructed for each member. 
**図4を使用して、各メンバーの特徴量がどのように構築されるかを説明できます**。 
After optimizing for $O1$ and $O2$ individually using gradient descent, we now have two vectors for each vertex of the graph (i.e. in this case the company). 
勾配降下法を使用して $O_1$ と $O_2$ を個別に最適化した後、グラフの各頂点（この場合は会社）に対して2つのベクトルを持つことになります。
A company can now be represented as a single vector by concatenating the first and second order embeddings. 
**会社は、第一および第二のオーダーの埋め込みを連結することによって、単一のベクトルとして表現できます**。
(うん、2種類の方法で埋め込みを作って、それを連結して1つのベクトルにする感じか...!:thinking:)
This represents each company on a single vector space. 
これにより、各会社が単一のベクトル空間で表現されます。 
Each query and member can be represented by a bag of companies, i.e. a query can contain multiple companies referenced in the search terms and a member could have worked at multiple companies which is manifested on the profile. 
**各クエリとメンバーは、会社のバッグによって表現**できます。つまり、クエリは検索用語で参照される複数の会社を含むことができ、メンバーはプロフィールに現れる複数の会社で働いていた可能性があります。 
Thus, with a simple pooling operation (max-pooling or mean-pooling) over the bag of companies, we can represent each query and member as a point on the vector space. 
したがって、**会社のバッグに対する単純なプーリング操作（最大プーリングまたは平均プーリング）を使用することで、各クエリとメンバーをベクトル空間の点として表現**できます。 
A similarity function between the two vector representations can be used as a feature in ranking. 
**2つのベクトル表現間の類似性関数は、ランキングの特徴として使用**できます。 
(あれ、じゃあランキングモデルは別にTwo-towerではないのかな?? もしくは使おうと思えば、的な話かな...!:thinking:)

##### _3.2.2_ _Supervised Embeddings. _3.2.2_ _教師あり埋め込み。

In this section, we explain how to_ train the entity embeddings in a supervised manner. 
このセクションでは、**エンティティ埋め込みを教師ありの方法でトレーニングする方法**を説明します。 
We first collect the training data from candidates recommended to the recruiters (with the inMail accept events as the positive labels) within the LinkedIn Recruiter product, and then learn the feature representations for the entities guided by the labeled data. 
まず、LinkedIn Recruiter製品内でリクルーターに推奨された候補者からトレーニングデータを収集し（**inMail受諾イベントを正のラベルとして**）、ラベル付きデータに基づいてエンティティの特徴表現を学習します。 
For this purpose, we adopted and extended Deep Semantic Structured Models (DSSM) based learning architecture [15]. 
この目的のために、Deep Semantic Structured Models (DSSM) ベースの学習アーキテクチャ [15] を採用し、拡張しました。(どんなアーキテクチャだろう??:thinking:)
In this scheme, document and query text are modeled through separate neural layers and crossed before final scoring, optimizing for the search engagement as a positive label. 
このスキームでは、**ドキュメントとクエリテキストは別々のニューラル層を通じてモデル化され、最終スコアリングの前に交差**し、検索エンゲージメントを正のラベルとして最適化します。(あ! two-towerモデルアーキテクチャだ...!:thinking:)
Regarding features, the DSSM model uses the query and document text and converts them to character trigrams, then utilizes these as inputs to the model. 
**特徴に関して、DSSMモデルはクエリとドキュメントテキストを使用し、それらを文字トライグラムに変換し、次にこれらをモデルへの入力として利用します**。(テキスト特徴だけなのかな...!:thinking:) 
An example character trigram of the word java is given as {#ja, jav, ava, va#}. 
単語「java」の例として、文字トライグラムは {#ja, jav, ava, va#} です。 
This transformation is also called word-hashing and instead of learning a vector representation (i.e. embedding) for the entire word, this technique provides representations for each character trigram. 
この変換はワードハッシングとも呼ばれ、単語全体のベクトル表現（すなわち埋め込み）を学習するのではなく、この技術は各文字トライグラムの表現を提供します。 
In this section we extend this scheme and add categorical representations of each type of entity as inputs to the DSSM model. 
このセクションでは、このスキームを拡張し、**DSSMモデルへの入力として各タイプのエンティティのカテゴリカルな表現を追加**します。(あ、じゃあLinkedInの実際のユースケースでは、テキスト特徴に加えて、カテゴリカル特徴も使ってる感じか...!:thinking:)

<!-- ここまで読んだ! -->

We illustrate our usage of word-hashing through an example. 
ワードハッシングの使用例を示します。 
Suppose that a query has the title id ti selected as a facet, and contains the search box keyword, java. 
クエリがファセットとして選択されたタイトルID ti を持ち、検索ボックスのキーワード「java」を含むとします。 
We process the text to generate the following trigrams: {#ja, jav, ava, va#}. 
テキストを処理して次のトライグラムを生成します：{#ja, jav, ava, va#}。 
Next, we add the static standardized ids corresponding to the selected entities (ti, in this example) as inputs to the model. 
次に、選択されたエンティティに対応する静的標準化ID（この例ではti）をモデルへの入力として追加します。 
We add entities from the facets to the existing model, since text alone is not powerful enough to encode the semantics. 
テキストだけではセマンティクスをエンコードするには不十分なため、ファセットからのエンティティを既存のモデルに追加します。 
After word hashing, a multi-layer non-linear projection (consisting of multiple fully connected layers) is performed to map the query and the documents to a common semantic representation. 
ワードハッシングの後、クエリとドキュメントを共通のセマンティック表現にマッピングするために、複数の全結合層からなる多層非線形射影が行われます。 
Finally, the similarity of the document to the query is calculated using a vector similarity measure (e.g., cosine similarity) between their vectors in the new learned semantic space. 
最後に、ドキュメントとクエリの類似性は、新しく学習されたセマンティック空間におけるベクトル間のベクトル類似性測定（例：コサイン類似度）を使用して計算されます。 
We use stochastic gradient descent with back propagation to infer the network coefficients. 
ネットワーク係数を推測するために、逆伝播を伴う確率的勾配降下法を使用します。 

Output of the model is a set of representations (i.e. dictionary) for each entity type (e.g. title, skill) and network architecture that we re-use during the inference. 
モデルの出力は、各エンティティタイプ（例：職位、スキル）および推論中に再利用するネットワークアーキテクチャの表現のセット（すなわち辞書）です。(=embedding lookup tableってことかな...!:thinking:)
Each query and member can be represented by a bag of entities, i.e. a query can contain multiple titles and skills referenced in the search terms and a member could have multiple titles and skills which are manifested on the profile. 
各クエリとメンバーは、エンティティのバッグによって表現できます。つまり、クエリは検索用語で参照される複数の職位やスキルを含むことができ、メンバーはプロフィールに現れる複数の職位やスキルを持っている可能性があります。 
The lookup tables learned during training and network coefficients are used to construct query and document embeddings. 
**トレーニング中に学習されたルックアップテーブルとネットワーク係数**は、クエリとドキュメントの埋め込みを構築するために使用されます。(=実際のランキングを行うtwo-towerモデルのentity embedding層とかに使われる感じかな...!:thinking:)
The two arms of DSSM corresponds to the supervised embeddings of the query and the document respectively. 
DSSMの2つのアームは、それぞれクエリとドキュメントの教師あり埋め込みに対応します。 
We then use the similarity measured by the distance of these two vectors (e.g. cosine) as a feature in the learning to rank model. 
次に、これら2つのベクトル間の距離（例：コサイン）によって測定された類似性を、ランキングモデルの特徴として使用します。

We used DSSM models over other deep learning models and nonlinear models for the following reasons.
**私たちは、以下の理由から他の深層学習モデルや非線形モデルよりもDSSMモデルを使用しました**。(教師ありのentity埋め込みモデルに、って話かな...!:thinking:)
First, DSSM enables projection of recruiter queries (query) and member profiles (document) into a common low-dimensional space, where relevance of the query and the document can be computed as the distance between them. 
第一に、DSSMはリクルーターのクエリ（クエリ）とメンバープロフィール（ドキュメント）を共通の低次元空間に投影することを可能にし、クエリとドキュメントの関連性をそれらの間の距離として計算できます。
This is important for talent search models, as the main goal is to find the match between recruiter queries and member profiles. 
これはタレントサーチモデルにとって重要であり、主な目標はリクルーターのクエリとメンバープロフィールの間のマッチを見つけることだからです。 
Secondly, DSSM uses word hashing, which enables handling large vocabularies, and results in a scalable semantic model. 
第二に、DSSMはワードハッシングを使用しており、大規模な語彙を扱うことができ、スケーラブルなセマンティックモデルを実現します。
(DSSM = Two-towerモデルアーキテクチャの一種 + テキスト特徴に強い構造、って感じかな...!:thinking:)

<!-- ここまで読んだ! -->

#### 3.3 オンラインシステムアーキテクチャ

![]()
**Figure 5: Online System Architecture for Search Ranking** 
**図5: 検索ランキングのためのオンラインシステムアーキテクチャ**

Figure 5 presents the online architecture of the proposed talent search ranking system, which also includes the embedding step (§3.2). 
図5は、提案されたタレント検索ランキングシステムのオンラインアーキテクチャを示しており、埋め込みステップ（§3.2）も含まれています。
We designed our architecture such that the member embeddings are computed offline, but the query embeddings are computed at run time. 
私たちは、**メンバーの埋め込みをオフラインで計算し、クエリの埋め込みを実行時に計算するようにアーキテクチャを設計**しました。(うんうん、検索におけるtwo-towerモデルの典型的な設計パターンだな...!:thinking:)
We made these choices for the following reasons:
これらの選択をした理由は以下の通りです：

(1) since a large number of members may match a query, computing the embeddings for these members at run time would be computationally expensive, 
多くのメンバーがクエリに一致する可能性があるため、これらのメンバーの埋め込みを実行時に計算することは計算コストが高くなり、
and, (2) the queries are typically not known ahead of time, and hence the embeddings need to be generated online. 
クエリは通常事前に知られていないため、埋め込みはオンラインで生成する必要があります。
(逆にメンバーは事前に知られてるのでオフラインで事前計算できるよね、って話:thinking:)
(推薦タスクの場合は、スーパー新規ユーザ以外は、ユーザもアイテムも事前に知られてるのでオフラインで計算できる...!:thinking:)
Consequently, we chose to include member embeddings as part of the forward index containing member features, which is generated periodically by an offline workflow (not shown in the figure). 
その結果、メンバーの特徴を含むフォワードインデックスの一部としてメンバーの埋め込みを含めることにしました。このインデックスはオフラインのワークフローによって定期的に生成されます（図には示されていません）。(ん? あ、これは多分クエリタワー側の入力として、ってことかな...!:thinking:)
We incorporated the component for generating query embeddings as part of the online system. 
**クエリの埋め込みを生成するコンポーネントをオンラインシステムの一部として組み込みました**。
Our online recommendation system consists of two services: 
私たちのオンライン推薦システムは2つのサービスで構成されています：

(1) Retrieval Service: This service receives a user query, generates the candidate set of members that match the criteria specified in the query, and computes an initial scoring of the retrieved candidates using a simple, first-pass model. 
(1) 取得サービス：このサービスはユーザのクエリを受け取り、クエリで指定された基準に一致するメンバーの候補セットを生成し、単純なファーストパスモデルを使用して取得した候補の初期スコアを計算します。
These candidates, along with their features, are retrieved from a distributed index and returned to the scoring/ranking service. 
**これらの候補は、その特徴量と共に分散インデックスから取得**され、スコアリング/ランキングサービスに返されます。
The features associated with each member can be grouped into two categories: 
各メンバーに関連付けられた特徴は2つのカテゴリに分類できます：
(あれ? でもメンバーの埋め込みは事前計算しておくって話だったよね。じゃあメンバーに関するそれ以外の特徴量ってランキングで必要なのかな??:thinking:)

- Explicit Features: These features correspond to fields that are present in a member profile, e.g., current and past work positions, education, skills, etc. 
  - **明示的特徴**：これらの特徴は、メンバープロフィールに存在するフィールドに対応します。例えば、現在および過去の職務、教育、スキルなどです。
- Derived Features: These features could either be derived from a member’s profile (e.g., implied skills), or generated by an external algorithm (e.g., embedding for a member (§3.2)). 
  - **派生特徴**：これらの特徴は、メンバーのプロフィールから派生したものであるか（例：暗黙のスキル）、外部アルゴリズムによって生成されたものである可能性があります（例：メンバーの埋め込み（§3.2））。

The retrieval service is built on top of LinkedIn’s Galene search platform [26], which handles the selection of candidates matching the query, and the initial scoring/pruning of these candidates, in a distributed fashion. 
取得サービスは、LinkedInのGalene検索プラットフォーム[26]の上に構築されており、クエリに一致する候補の選択と、これらの候補の初期スコアリング/プルーニングを分散方式で処理します。

---

(2) Scoring/Ranking Service: This component is responsible for the second-pass ranking of candidates corresponding to each query, and returning the ranked list of candidates to the front-end system for displaying in the product. 
(2) スコアリング/ランキングサービス：このコンポーネントは、各クエリに対応する候補のセカンドパスランキングを担当し、製品に表示するためにフロントエンドシステムに候補のランキングリストを返します。
Given a query, this service fetches the matching candidates, along with their features, from the retrieval service, and in parallel, computes the vector embedding for the query. 
クエリが与えられると、このサービスは取得サービスから一致する候補とその特徴を取得し、並行してクエリのベクトル埋め込みを計算します。
Then, it performs the second-pass scoring of the candidates (which includes generation of similarity features based on query and member embeddings (§3.2)) and returns the top ranked results. 
次に、候補のセカンドパススコアリングを実行し（これはクエリとメンバーの埋め込みに基づく類似性特徴の生成を含みます（§3.2））、上位のランキング結果を返します。
The second-pass scoring can be performed either by a deep learning based model (§3.1), or any other machine learned model (e.g., a GBDT model, as discussed in §2.2), periodically trained and updated as part of an offline workflow (not shown in the figure). 
**セカンドパススコアリングは、深層学習ベースのモデル（§3.1）または他の機械学習モデル（例：GBDTモデル（§2.2で議論））によって実行**され、オフラインのワークフローの一部として定期的にトレーニングおよび更新されます（図には示されていません）。
(あ、ランキングはTwo-towerじゃないのか...!:thinking:)

<!-- ここまで読んだ! -->

#### 4 EXPERIMENTS 実験

We next present the results from our offline experiments for the proposed models, and then discuss the trade-offs and design decisions to pick a model for online experimentation. 
次に、提案したモデルに対するオフライン実験の結果を示し、**オンライン実験のためのモデルを選択する際のトレードオフと設計上の決定について議論**します。
We finally present the results of our online A/B test of the chosen model on LinkedIn _Recruiter product, which is based on unsupervised embeddings._ 
最後に、選択したモデルのLinkedIn _Recruiter_ プロダクトにおけるオンラインA/Bテストの結果を示します。このプロダクトは、教師なし埋め込みに基づいています。

<!-- ここまで読んだ! -->

#### 4.1 オフライン実験

To evaluate the proposed methodologies, we utilized LinkedIn Recruiter usage data collected over a two month period within 2017.
提案された方法論を評価するために、**2017年の2か月間に収集されたLinkedIn Recruiterの使用データを利用**しました。
This dataset consists of the impressions (recommended candidates) with tracked features from the candidates and recruiters, as well as the labels for each impression (positive/1 for impressions which resulted in the recruiter sending an inMail and the inMail being accepted, negative/0 otherwise).
このデータセットは、**候補者とリクルーターからの追跡された特徴を持つインプレッション（推薦された候補者）と、各インプレッションのラベル（リクルーターがinMailを送信し、inMailが受け入れられた場合はpositive/1、そうでない場合はnegative/0）で構成**されています。
Furthermore, we filter the impression set for both training and testing sets to come from a random bucket, i.e., a subset of the traffic where the top 100 returned search results are randomly shuffled and shown to the recruiters.
さらに、トレーニングセットとテストセットの両方のインプレッションセットを**ランダムバケット**から取得するようにフィルタリングします。つまり、上位100件の検索結果がランダムにシャッフルされ、リクルーターに表示されるトラフィックのサブセットです。
The random bucket helps reduce positional bias [18].
ランダムバケットは、位置バイアスを軽減するのに役立ちます[18]。
(random bucketよくわかってないな...!:thinking:)

- メモ: random bucket:
  - hoge

We split training data and test data by time, which forms a roughly 70% 30% split.
**トレーニングデータとテストデータは時間で分割し、約70%対30%の比率を形成**します。
The dataset covers tens of thousands of recruiters, and millions of candidates recommended.
このデータセットは、数万のリクルーターと数百万の推薦候補者をカバーしています。

<!-- ここまで読んだ! -->

To evaluate the performance of the ranking models, we use offline replay, which re-ranks the recommended candidates based on the new model being tested, and evaluates the new ranked list.
ランキングモデルのパフォーマンスを評価するために、**オフラインリプレイ**を使用します。これは、テスト中の新しいモデルに基づいて推薦された候補者を再ランク付けし、新しいランクリストを評価します。
(replayメソッドによるオフライン評価ってこと...??:thinking:)
- 補足: replayメソッドってどんなだっけ?
  - データ収集方策で取得したログデータを用いて、別の新しい方策性能を推定するnaiveな手法の一つ。
  - 手法のコンセプトとしては、データ収集方策と同じ行動を新しい方策がとった場合のログだけを使って評価を行う。

As explained previously, the main metric we report is precision at k (Prec@k) due to its stability and the suitability with the way LinkedIn Recruiter product presents candidates.
前述のように、私たちが報告する主な指標は、安定性とLinkedIn Recruiter製品が候補者を提示する方法に適しているため、kにおける精度（Prec@k）です。
Prec@k lift represents the % gain in the inMail Accept precision for top _k impressions._
Prec@kリフトは、上位_kインプレッション_に対するinMail Accept精度の%向上を表します。
Prec@k is computed as the fraction of positive responses (inMail accepts, within three days of the inMail being sent by the recruiter) in a given search session, averaged over all the sessions in the dataset.
**Prec@kは、特定の検索セッションにおけるポジティブな応答（リクルーターによって送信されたinMailの3日以内に受け入れられたinMail）をデータセット内のすべてのセッションで平均した割合として計算**されます。
For training of the deep models, we utilized TensorFlow [1], an open-source software package for creating and training custom neural network models.
深層モデルのトレーニングには、カスタムニューラルネットワークモデルを作成およびトレーニングするためのオープンソースソフトウェアパッケージであるTensorFlow [1]を利用しました。

##### _4.1.1_ _深層モデル。_ 

We first evaluated the effect of utilizing the end-to-end deep model, proposed in §3.1, with up to three layers on the dataset described above.
まず、上記のデータセットに対して、§3.1で提案されたエンドツーエンドの深層モデルを最大3層まで利用する効果を評価しました。(=ランキング用のtwo-towerモデル!)
The baseline model is a gradient boosted decision tree (§2.2, trained using the XGBoost [6] package) which consists of 30 trees, each having a maximum depth of 4 and trained in a point-wise manner, and we compare it to the neural network approach.
**ベースラインモデルは、30本の木から構成され、各木の最大深さは4で、ポイントワイズ方式でトレーニングされた勾配ブースト決定木**（§2.2、XGBoost [6]パッケージを使用してトレーニング）であり、これをニューラルネットワークアプローチと比較します。
The model family is a k layer multi-layer perceptron (MLP) with 100 units in each layer and rectified linear units (ReLU) for activations.
モデルファミリーは、**各層に100ユニットを持つk層の多層パーセプトロン（MLP）であり、活性化には整流線形ユニット（ReLU）を使用**します。
We did not regularize the network because the size of the network was small enough, but rather used early stopping to achieve a similar effect.
ネットワークのサイズが十分に小さかったため、正則化は行わず、むしろ早期停止を使用して同様の効果を達成しました。
Also, as explained in §3.1, we chose hinge loss to train the pairwise training (the final metrics produced from logistic or hinge loss did not differ significantly).
また、§3.1で説明したように、**ペアワイズトレーニングをトレーニングするためにヒンジ損失を選択**しました（ロジスティックまたはヒンジ損失から生成された最終的なメトリックは、著しく異なりませんでした）。

<!-- ここまで読んだ! -->

The results are shown in Table 3.
結果は表3に示されています。
Interestingly, while single layer neural network trained with pointwise loss has poor ranking performance, additional layers of nonlinearity bring the neural network performance almost on par with XGBoost (further layers and units per layer did not improve the results, and are omitted here for brevity).
興味深いことに、ポイントワイズ損失でトレーニングされた**単層ニューラルネットワークはランキング性能が低いですが、非線形性のために層を追加するとニューラルネットワークの性能をXGBoostとほぼ同等に引き上げます**（さらなる層や層ごとのユニットは結果を改善せず、簡潔さのためにここでは省略されています）。
On the other hand, neural network models trained using pairwise loss outperformed those trained with pointwise loss and XGBoost baseline as more layers are introduced (similar to the pointwise case, we did not see additional gains using more layers or units for pairwise loss).
一方、**ペアワイズ損失を使用してトレーニングされたニューラルネットワークモデルは、より多くの層が導入されるにつれて、ポイントワイズ損失およびXGBoostベースラインでトレーニングされたモデルを上回りました**（ポイントワイズの場合と同様に、ペアワイズ損失に対してより多くの層やユニットを使用しても追加の利得は見られませんでした）。
A possible explanation is the following:
考えられる説明は次のとおりです。

(1) Pairwise loss approach explicitly compares positive examples to negative examples within a search session rather than simply separate positive examples from negative examples in a broad sense, and,
    (1) ペアワイズ損失アプローチは、広い意味でポジティブな例をネガティブな例から単に分離するのではなく、**検索セッション内でポジティブな例をネガティブな例と明示的に比較**します。
(2) It automatically deals with imbalanced classes since it could be mathematically shown that pairwise ranking loss is closely related to AUC [10], which is immune to class imbalance.
    (2) ペアワイズランキング損失がAUCに密接に関連していることが数学的に示されるため[10]、**クラスの不均衡に自動的に対処**します。

##### _4.1.2_ _Shallow Models._  _4.1.2_ _浅層モデル。_ 

In this family of models, we use representation learning methods to construct dense vectors to represent certain categorical features.
このモデルファミリーでは、特定のカテゴリカル特徴を表すために密なベクトルを構築するための表現学習方法を使用します。
Although deep networks are used to train the embeddings, once trained, they are used as features in the baseline gradient boosted decision tree model, which is shallow.
深層ネットワークは埋め込みをトレーニングするために使用されますが、一度トレーニングされると、**浅いベースライン勾配ブースト決定木モデルの特徴量として使用**されます。(あれ? 4.1.1でベースラインよりも性能高いのに、実運用ではtreeモデルを続けて使うってこと?? それとも4.1.2の実験では、ってことかな??:thinking:)

Our first set of experiments utilizes unsupervised network embeddings, as proposed in §3.2 to learn representations for categorical variables like skills and titles from member profiles.
最初の実験セットでは、§3.2で提案されたように、メンバープロファイルからスキルやタイトルのようなカテゴリ変数の表現を学習するために、教師なしネットワーク埋め込みを利用します。
The title/skill representations are learned for both the query and the document (member) and a measure of similarity between the two is used as a new feature in the ranking model (baseline GBDT with additional feature).
タイトル/スキルの表現は、クエリとドキュメント（メンバー）の両方に対して学習され、両者の類似度の測定がランキングモデルの新しい特徴（追加機能を持つベースラインGBDT）として使用されます。
As shown in Table 4, converting the categorical interaction feature to a dense similarity measure results in large gains in the precision metric.
**表4に示すように、カテゴリカルインタラクション特徴を密な類似度測定に変換することで、精度メトリックに大きな向上が得られます**。
The employed embedding was a concatenated version of order 1 and order 2 representations.
使用された埋め込みは、順序1と順序2の表現の連結バージョンでした。
For each member or query, the aggregation strategy used was mean pooling (although max pooling resulted in similar results), i.e., if a member or query has multiple skills, we do a mean pool of all the individual skill vectors to represent them on the vector space.
**各メンバーまたはクエリに対して、使用された集約戦略は平均プーリング**でした（最大プーリングでも同様の結果が得られました）。つまり、メンバーまたはクエリが複数のスキルを持つ場合、すべての個々のスキルベクトルの平均プールを行い、ベクトル空間でそれらを表現します。
Denote the mean pooled member vector by m, and the mean pooled query vector by _q.
平均プールされたメンバーベクトルを $m$、平均プールされたクエリベクトルを $q$ とします。
We experimented with three similarity measures between the two vector representations:
私たちは、2つのベクトル表現間の3つの類似度測定を実験しました: 

(1) Dot Product ドット積: 

$$
m \cdot q = \sum_{i} m_i q_i
$$

(2) Cosine Similarity: 

$$
\frac{m \cdot q}{||m||_2 ||q||_2} = \frac{\sum_{i} m_i q_i}{\sqrt{\sum_{i} m_i^2} \sqrt{\sum_{i} q_i^2}}
$$

(3) Hadamard Product: ハダマード積（要素ごとの積とも呼ばれます）

$$
m \circ q = [m_1 q_1, m_2 q_2, ..., m_d q_d]
$$

We note that both dot product and cosine similarity measures result in a single new feature added to the ranking model, whereas Hadamard product measure contributes to as many features as the dimensionality of the embedding vector representation.
**ドット積とコサイン類似度の両方の測定は、ランキングモデルに追加される単一の新しい特徴をもたらしますが、ハダマード積の測定は埋め込みベクトル表現の次元数と同じ数の特徴に寄与します**。(あ、ハダマード積ってベクトルなのか...!:thinking:)
From Table 4, we can observe that using dot product outperformed using Hadamard product based set of features.
表4から、**ドット積を使用する方がハダマード積に基づく特徴セットを使用するよりも優れている**ことがわかります。

---

<!-- ここまで読んだ! -->

In our second set of experiments, we retain the same strategy of introducing feature(s) based on the similarity between the member/query embeddings into the ranking model.
2回目の実験セットでは、メンバー/クエリ埋め込み間の類似性に基づいて特徴をランキングモデルに導入する同じ戦略を保持します。
The only difference is that we now utilize a supervised algorithm (DSSM) to train the embeddings, which uses the same dataset as the offline experiments [3].
唯一の違いは、今度は教師ありアルゴリズム（DSSM）を使用して埋め込みをトレーニングすることであり、これはオフライン実験と同じデータセットを使用します[3]。
As shown in Table 5, we observed comparatively modest lift values in the Prec@k metric.
表5に示すように、Prec@kメトリックで比較的控えめなリフト値を観察しました。
In all experiments, we fixed the size of the embedding to 50.
すべての実験で、埋め込みのサイズを50に固定しました。
We used tanh as the activation function and experimented with dot product and cosine similarity for the similarity computation between the two arms of DSSM.
活性化関数としてtanhを使用し、DSSMの2つのアーム間の類似度計算にドット積とコサイン類似度を使用しました。
We used a minimum of 1 layer and a maximum of 3 layers in our experiments with DSSM models.
DSSMモデルの実験では、最小1層、最大3層を使用しました。
The first hidden layer is used for word hashing, and the next two hidden layers are used to reduce the dimensionality of query/document vector representation.
最初の隠れ層は単語ハッシングに使用され、次の2つの隠れ層はクエリ/ドキュメントベクトル表現の次元を削減するために使用されます。
In our experiments, we did not observe better performance by using more than 3 layers.
私たちの実験では、3層以上を使用してもより良いパフォーマンスは観察されませんでした。
We conducted extensive offline experiments and tried over 75 models.
私たちは広範なオフライン実験を行い、75以上のモデルを試しました。
We only report the best configuration (network architecture) for each model.
各モデルの最良の構成（ネットワークアーキテクチャ）だけを報告します。

![]()

**Table 5: 教師あり埋め込みを使用したオフライン実験。** **ネットワークアーキテクチャは角括弧で表されます。各評価の次元（類似度測定、テキスト対ファセット）に対して最も良いパフォーマンスのアーキテクチャタイプのみが示されています。**
**Model** **Similarity** **Prec@1** **Prec@5** **Prec@25**
XGBoost    - 0% 0% 0%
Text [200, 100] Dot 3.62% -0.13% 0.15%
Text [200, 100] Cosine 0.44% 0.55% -0.10%
Text [500, 500, 128] Dot 0.55% -0.01% 0.38%
Title [500] Dot 2.42% -0.13% -0.02%

<!-- ここまで読んだ! -->

#### 4.2 オンライン実験

Based on the offline results, we have currently put off the online deployment of the end-to-end deep learning models in LinkedIn Recruiter due to the following reasons:
**オフラインの結果に基づき、現在、LinkedIn Recruiterにおけるエンドツーエンドの深層学習モデルのオンライン展開を以下の理由により見送っています**。(見送ったんかい!:thinking:)

(理由1)
There is a significant engineering cost to implementing end-to-end deep learning solutions in search systems since the number of items (candidates) that need to be scored can be quite large.
スコアリングが必要なアイテム（候補者）の数が非常に多くなる可能性があるため、**検索システムにエンドツーエンドの深層学習ソリューションを実装するには、かなりのエンジニアリングコストがかかります**。
Further, the relatively large amount of computation needed to evaluate deep neural networks could cause the search latency to be prohibitively large, especially when there are many candidates to be scored, thereby not meeting the real-time requirements of search systems such as LinkedIn Recruiter.
さらに、深層ニューラルネットワークを評価するために必要な比較的大きな計算量は、特にスコアリングする候補者が多い場合、検索のレイテンシを過度に大きくする可能性があり、その結果、LinkedIn Recruiterのような検索システムのリアルタイム要件を満たさなくなります。

(理由2)
The offline evaluation for the end-to-end deep models (§4.1.1) showed an improvement of 1.72% in Prec@25 for the 3-layer case, which, although impressive per our experience, does not currently justify the engineering costs discussed above.
エンドツーエンドの深層モデルのオフライン評価（§4.1.1）は、3層の場合においてPrec@25で1.72%の改善を示しましたが、**私たちの経験からすると印象的ではあるものの、上記のエンジニアリングコストを正当化するものではありません**。

<!-- ここまで読んだ! -->

Instead, we performed online A/B tests incorporating the unsupervised network embeddings (§3.2.1) as a feature in the gradient boosted decision tree model.
その代わりに、**無監督ネットワーク埋め込み（§3.2.1）を勾配ブースト決定木モデルの特徴として組み込んだオンラインA/Bテストを実施**しました。
As in the case of the offline experiments, in the online setting, we first concatenate both the first and the second order embeddings for the search query, and for each potential candidate to be shown, then take the cosine similarity between the two concatenated embeddings, and use that as a single additional feature (to the baseline) in the gradient boosted decision tree (for both offline training and online model evaluation).
オフライン実験の場合と同様に、オンライン設定では、まず検索クエリのために一次および二次の埋め込みを連結し、表示される各候補者に対して、**連結された2つの埋め込み間のコサイン類似度を計算し、それを勾配ブースト決定木の基準モデルに対する単一の追加特徴（オフライントレーニングおよびオンラインモデル評価の両方に使用）として利用**します。
Although the offline gain as evaluated in §4.1.2 is smaller compared to that of an end-to-end deep learning model, the engineering cost and computational complexity is much less demanding, since the embeddings can be precomputed offline, and the online dot product computation is relatively inexpensive compared to a neural network evaluation.
§4.1.2で評価されたオフラインの利得はエンドツーエンドの深層学習モデルと比較して小さいものの、**埋め込みはオフラインで事前に計算でき、オンラインのドット積計算はニューラルネットワークの評価と比較して比較的安価であるため、エンジニアリングコストと計算の複雑さははるかに要求が少ない**です。(うんうん...!! two-tower型アーキテクチャのメリットだよね...!:thinking:)
An additional benefit of testing the embedding features with a tree model instead of an end-to-end deep model is that we can measure the impact of the new feature(s) in an apple-to-apple comparison, i.e., under similar latency conditions as the baseline model which is a tree model as well, with the embedding based feature as the only difference.
エンドツーエンドの深層モデルの代わりにツリーモデルで埋め込み特徴をテストする追加の利点は、新しい特徴の影響を同じ条件で測定できることです。つまり、埋め込みに基づく特徴が唯一の違いであるツリーモデルと同様のレイテンシ条件下での比較です。
Finally, we decided against deploying the supervised embeddings (§3.2.2) due to relatively weaker offline experimental results (§4.1.2).
最後に、比較的弱いオフライン実験結果（§4.1.2）により、監視された埋め込み（§3.2.2）の展開は見送ることにしました。

The A/B test as explained above was performed on LinkedIn Recruiter users during the last quarter of 2017, with the control group being served results from the baseline model (gradient boosted decision tree model trained using XGBoost [6]) and the treatment group, consisting of a random subset of tens of thousands of users, being served results from the model that includes the unsupervised network embedding based feature.
上記で説明したA/Bテストは、2017年の最後の四半期にLinkedIn Recruiterのユーザーに対して実施され、コントロールグループには基準モデル（XGBoost [6]を使用してトレーニングされた勾配ブースト決定木モデル）からの結果が提供され、治療グループには無監督ネットワーク埋め込みに基づく特徴を含むモデルからの結果が提供されました。
We present the results of the experiment in Table 6.
実験の結果を表6に示します。
Although the p-values are high for the experiments (as a result of relatively small sample sizes), we note that an increase of 3% in the overall precision is an impressive lift, considering that precision is a hard metric to move, based on our domain experience.
実験のp値は高いですが（比較的小さなサンプルサイズの結果として）、**全体の精度が3%向上したことは、精度が動かしにくい指標であることを考慮すると、印象的な向上**です。

**Table 6: Online A/B testing results. Comparing XGBoost model with vs. without network embedding based semantic similarity feature.**
**表6: オンラインA/Bテスト結果。ネットワーク埋め込みに基づくセマンティック類似度特徴の有無によるXGBoostモデルの比較。**
**Prec@5** **Prec@25** **Overall precision**
**Prec@5** **Prec@25** **全体の精度**
Improvement 2% 1.8% 3%
改善 2% 1.8% 3%
p-value 0.2 0.25 0.11
p値 0.2 0.25 0.11

<!-- ここまで読んだ! -->

#### 4.3 実践で得られた教訓

We next present the challenges encountered and the lessons learned as part of our offline and online empirical investigations. 
次に、私たちのオフラインおよびオンラインの実証調査の一環として直面した課題と得られた教訓を示します。 
As stated in §4.2, we had to weigh the potential benefits vs. the engineering cost associated with implementing end-to-end deep learning models as part of LinkedIn Recruiter search system. 
§4.2で述べたように、**LinkedIn Recruiter検索システムの一部としてエンドツーエンドの深層学習モデルを実装することに関連する潜在的な利点とエンジニアリングコストを天秤にかける必要がありました**。 
Considering the potential latency increase of introducing deep learning models into ranking, we decided against deploying end-to-end deep learning models in our system. 
**深層学習モデルをランキングに導入することによる潜在的なレイテンシの増加を考慮し、私たちはシステムにエンドツーエンドの深層学習モデルを展開しないことに決めました**。(まあね〜:thinking:)
Our experience suggests that hybrid approaches that combine offline computed embeddings (including potentially deep learning based embeddings trained offline) with simpler online model choices could be adopted in other large-scale latency-sensitive search and recommender systems. 
私たちの経験は、**オフラインで計算された埋め込み（オフラインで訓練された深層学習ベースの埋め込みを含む）と、よりシンプルなオンラインモデルの選択肢を組み合わせたハイブリッドアプローチが、他の大規模なレイテンシに敏感な検索および推薦システムに採用される可能性があること**を示唆しています。 
Such hybrid approaches have the following key benefits: 
このようなハイブリッドアプローチには、以下の主要な利点があります：

(1) the engineering cost and complexity associated with computing embeddings offline is much lower than that of an online deep learning based system, especially since the existing online infrastructure can be reused with minimal modifications; 
(1) オフラインで埋め込みを計算することに関連するエンジニアリングコストと複雑さは、オンラインの深層学習ベースのシステムよりもはるかに低く、特に既存のオンラインインフラストラクチャを最小限の変更で再利用できるためです。

(2) the latency associated with computing dot product of two embedding vectors is much lower than that of evaluating a deep neural network with several layers. 
(2) **2つの埋め込みベクトルのドット積を計算することに関連するレイテンシは、数層の深層ニューラルネットワークを評価する際のそれよりもはるかに低い**です。(うんうん...!:thinking:)

<!-- ここまで読んだ! -->

#### 5 RELATED WORK 関連研究

Use of neural networks on top of curated features for ranking is an established idea which dates back at least to [5], wherein simple 2-layer neural networks are used for ranking the risk of mortality in a medical application. 
キュレーションされた特徴の上にニューラルネットワークを使用してランキングを行うことは、少なくとも[5]に遡る確立されたアイデアであり、そこで単純な2層のニューラルネットワークが医療アプリケーションにおける死亡リスクのランキングに使用されています。
In [4], the authors use neural networks together with the logistic pairwise ranking loss, and demonstrate that neural networks outperform linear models that use the same loss function. 
[4]では、著者たちはニューラルネットワークをロジスティックペアワイズランキング損失と組み合わせて使用し、ニューラルネットワークが同じ損失関数を使用する線形モデルよりも優れていることを示しています。
More recently, the authors of [7] introduced a model that jointly trains a neural network and a linear classifier, where the neural network takes dense features, and the linear layer incorporates cross-product features and sparse features. 
最近では、[7]の著者たちが、ニューラルネットワークと線形分類器を共同で訓練するモデルを導入しました。このモデルでは、ニューラルネットワークが密な特徴を取り込み、線形層がクロスプロダクト特徴とスパース特徴を組み込んでいます。

Research in deep learning algorithms for search ranking has gained momentum especially since the work on Deep Structured Semantic Models (DSSM) [15]. 
**検索ランキングのための深層学習アルゴリズムに関する研究は、特にDeep Structured Semantic Models (DSSM) [15]に関する研究以降、勢いを増しています**。
DSSM involves learning the semantic similarity between a pair of text strings, where a sparse representation called tri-letter grams is used. 
DSSMは、テキスト文字列のペア間の意味的類似性を学習することを含み、ここではtri-letter gramsと呼ばれるスパース表現が使用されます。
The C-DSSM model [25] extends DSSM by introducing convolution and max-pooling after word hashing layer to capture local contextual features of words. 
C-DSSMモデル[25]は、単語ハッシング層の後に畳み込みとマックスプーリングを導入することで、単語の局所的な文脈特徴を捉えるためにDSSMを拡張します。
The Deep Crossing model [24] focuses on sponsored search (ranking ads corresponding to a query), where there is more contextual information about the ads. 
Deep Crossingモデル[24]は、スポンサー検索（クエリに対応する広告のランキング）に焦点を当てており、広告に関するより多くの文脈情報があります。
Finally, two other popular deep ranking models that have been used for search ranking are the ARC-I [14] (a combination of C-DSSM and Deep Crossing) and Deep Relevance Matching Model [11] (which introduces similarity histogram and query gating concepts). 
最後に、検索ランキングに使用される他の2つの人気のある深層ランキングモデルは、ARC-I [14]（C-DSSMとDeep Crossingの組み合わせ）とDeep Relevance Matching Model [11]（類似性ヒストグラムとクエリゲーティングの概念を導入）です。

There is extensive work on generating unsupervised embeddings. 
**教師なし埋め込み生成**に関する広範な研究があります。
The notion of word embeddings (word2vec) was proposed in [20], inspiring several subsequent *2vec algorithms. 
単語埋め込み（word2vec）の概念は[20]で提案され、その後のいくつかの*2vecアルゴリズムにインスピレーションを与えました。
Several techniques have been proposed for graph embeddings, including classical approaches such as multidimensional scaling (MDS) [8], IsoMap [29], LLE [23], and Laplacian Eigenmap [3], and recent approaches such as graph factorization [2] and DeepWalk [21]. 
グラフ埋め込みのために、古典的アプローチ（多次元尺度法（MDS）[8]、IsoMap [29]、LLE [23]、ラプラシアン固有写像 [3]）や、最近のアプローチ（グラフ因子分解 [2]、DeepWalk [21]）を含むいくつかの技術が提案されています。
To generate embedding representation for the entities using the LinkedIn Economic Graph, we adopt Large-Scale Information Network Embeddings approach [28], by changing how we construct the graph. 
LinkedIn Economic Graphを使用してエンティティの埋め込み表現を生成するために、グラフの構築方法を変更することでLarge-Scale Information Network Embeddingsアプローチ[28]を採用します。
While the graph used in [28] considers the members of the social network as vertices, we instead define a weighted graph over the entities (e.g., skill, title, company), and use the number of members sharing the same entity on their profile to induce an edge weight between the vertices. 
[28]で使用されるグラフはソーシャルネットワークのメンバーを頂点として考慮しますが、私たちは代わりにエンティティ（例：スキル、職位、会社）に対して重み付きグラフを定義し、同じエンティティをプロフィールに共有するメンバーの数を使用して頂点間のエッジの重みを誘導します。
Thus, we were able to reduce the size of the problem by a few orders of magnitude, thereby allowing us to scale the learning to all entities in the Economic Graph. 
このようにして、問題のサイズを数桁減少させることができ、経済グラフ内のすべてのエンティティに対して学習をスケールさせることが可能になりました。
Finally, a recent study presents a unified view of different network embedding methods like LINE and node2vec as essentially performing implicit matrix factorizations, and proposes NetMF, a general framework to explicitly factorize the closed-form matrices that network embeddings methods including LINE and word2vec aim to approximate [22]. 
最後に、最近の研究では、LINEやnode2vecのような異なるネットワーク埋め込み手法の統一的な見解を提示し、実質的に暗黙の行列因子分解を行っているとし、LINEやword2vecを含むネットワーク埋め込み手法が近似しようとする閉形式行列を明示的に因子分解するための一般的なフレームワークNetMFを提案しています[22]。

<!-- ここまで読んだ! -->

#### 6 CONCLUSIONS AND FUTURE WORK 結論と今後の課題

In this paper, we presented our experiences of applying deep learning models as well as representation learning approaches for talent search systems at LinkedIn. 
本論文では、LinkedInのタレントサーチシステムにおける深層学習モデルおよび表現学習アプローチの適用に関する私たちの経験を紹介しました。
We provided an overview of LinkedIn Recruiter search architecture, described our methodology for learning representations of sparse entities and deep models in the talent search domain, and evaluated multiple approaches in both offline and online settings. 
LinkedIn Recruiterの検索アーキテクチャの概要を提供し、タレントサーチ領域におけるスパースエンティティと深層モデルの表現を学習するための方法論を説明し、オフラインおよびオンラインの両方の設定で複数のアプローチを評価しました。
We also discussed challenges and lessons learned in applying these approaches in a large-scale latency-sensitive search system such as ours. 
また、私たちのような**大規模でレイテンシに敏感な検索システムにおいて、これらのアプローチを適用する際の課題と得られた教訓**についても議論しました。
Our design choices for learning semantic representations of entities at scale, and the deployment considerations in terms of weighing the potential benefits vs. the engineering cost associated with implementing end-to-end deep learning models should be of broad interest to academicians and practitioners working on large-scale search and recommendation systems. 
**エンティティのセマンティック表現を大規模に学習するための設計選択や、エンドツーエンドの深層学習モデルを実装する際の潜在的な利益とエンジニアリングコストを天秤にかけるデプロイメントの考慮事項**は、大規模な検索および推薦システムに取り組む学者や実務者にとって広く関心を持たれるべきです。

<!-- ここまで読んだ! -->

#### REFERENCES 参考文献

[1] M. Abadi et al. TensorFlow: A system for large-scale machine learning. In OSDI, 2016.  
[1] M. Abadiら. TensorFlow: 大規模機械学習のためのシステム. OSDIにおいて, 2016年.

[2] A. Ahmed, N. Shervashidze, S. Narayanamurthy, V. Josifovski, and A. J. Smola.  
Distributed large-scale natural graph factorization. In WWW, 2013.  
[2] A. Ahmed, N. Shervashidze, S. Narayanamurthy, V. Josifovski, および A. J. Smola.  
分散大規模自然グラフ因子分解. WWWにおいて, 2013年.

[3] M. Belkin and P. Niyogi. Laplacian eigenmaps and spectral techniques for embedding and clustering. In NIPS, 2002.  
[3] M. Belkin および P. Niyogi. ラプラシアン固有写像と埋め込みおよびクラスタリングのためのスペクトル技術. NIPSにおいて, 2002年.

[4] C. Burges et al. Learning to rank using gradient descent. In ICML, 2005.  
[4] C. Burgesら. 勾配降下法を用いたランキング学習. ICMLにおいて, 2005年.

[5] R. Caruana, S. Baluja, and T. Mitchell. Using the future to “sort out” the present: Rankprop and multitask learning for medical risk evaluation. In NIPS, 1996.  
[5] R. Caruana, S. Baluja, および T. Mitchell. 未来を利用して現在を「整理」する: 医療リスク評価のためのRankpropとマルチタスク学習. NIPSにおいて, 1996年.

[6] T. Chen and C. Guestrin. XGBoost: A scalable tree boosting system. In KDD, 2016.  
[6] T. Chen および C. Guestrin. XGBoost: スケーラブルなツリーブースティングシステム. KDDにおいて, 2016年.

[7] H.-T. Cheng et al. Wide & deep learning for recommender systems. In Workshop _on Deep Learning for Recommender Systems, 2016._  
[7] H.-T. Chengら. 推薦システムのためのWide & Deep Learning. _推薦システムのための深層学習に関するワークショップ, 2016年._

[8] T. F. Cox and M. A. Cox. Multidimensional scaling. CRC press, 2000.  
[8] T. F. Cox および M. A. Cox. 多次元尺度法. CRCプレス, 2000年.

[9] J. H. Friedman. Greedy function approximation: a gradient boosting machine.  
_Annals of Statistics, 2001._  
[9] J. H. Friedman. 貪欲な関数近似: 勾配ブースティングマシン.  
_統計学の年報, 2001年._

[10] W. Gao and Z.-H. Zhou. On the consistency of auc pairwise optimization. Int.  
_Conf. on Artifical Intelligence, 2015._  
[10] W. Gao および Z.-H. Zhou. AUCペアワイズ最適化の一貫性について.  
_人工知能に関する国際会議, 2015年._

[11] J. Guo, Y. Fan, Q. Ai, and W. B. Croft. A deep relevance matching model for ad-hoc retrieval. In CIKM, 2016.  
[11] J. Guo, Y. Fan, Q. Ai, および W. B. Croft. アドホック検索のための深い関連性マッチングモデル. CIKMにおいて, 2016年.

[12] V. Ha-Thuc et al. Personalized expertise search at LinkedIn. In Big Data, 2015.  
[12] V. Ha-Thucら. LinkedInにおけるパーソナライズされた専門知識検索. Big Dataにおいて, 2015年.

[13] V. Ha-Thuc et al. Search by ideal candidates: Next generation of talent search at LinkedIn. In WWW Companion, 2016.  
[13] V. Ha-Thucら. 理想的な候補者による検索: LinkedInにおける次世代のタレント検索. WWWコンパニオンにおいて, 2016年.

[14] B. Hu, Z. Lu, H. Li, and Q. Chen. Convolutional neural network architectures for matching natural language sentences. In NIPS, 2014.  
[14] B. Hu, Z. Lu, H. Li, および Q. Chen. 自然言語文をマッチングするための畳み込みニューラルネットワークアーキテクチャ. NIPSにおいて, 2014年.

[15] P.-S. Huang et al. Learning deep structured semantic models for web search using clickthrough data. In CIKM, 2013.  
[15] P.-S. Huangら. クリックデータを用いたウェブ検索のための深層構造的意味モデルの学習. CIKMにおいて, 2013年.

[16] K. Jarvelin and J. Kekalainen. Cumulated gain-based evaluation of IR techniques.  
_ACM TOIS, 20(4), 2002._  
[16] K. Jarvelin および J. Kekalainen. IR技術の累積ゲインに基づく評価.  
_ACM TOIS, 20(4), 2002年._

[17] T. Joachims. Optimizing search engines using clickthrough data. In KDD, 2002.  
[17] T. Joachims. クリックデータを用いた検索エンジンの最適化. KDDにおいて, 2002年.

[18] T. Joachims, L. Granka, B. Pan, H. Hembrooke, and G. Gay. Accurately interpreting clickthrough data as implicit feedback. In SIGIR, 2005.  
[18] T. Joachims, L. Granka, B. Pan, H. Hembrooke, および G. Gay. クリックデータを暗黙のフィードバックとして正確に解釈する. SIGIRにおいて, 2005年.

[19] T. Y. Liu. Learning to rank for information retrieval. Foundations and Trends in _Information Retrieval, 3(3), 2009._  
[19] T. Y. Liu. 情報検索のためのランキング学習. _情報検索の基礎とトレンド, 3(3), 2009年._

[20] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and J. Dean. Distributed representations of words and phrases and their compositionality. In NIPS, 2013.  
[20] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, および J. Dean. 単語とフレーズの分散表現とその合成性. NIPSにおいて, 2013年.

[21] B. Perozzi, R. Al-Rfou, and S. Skiena. DeepWalk: Online learning of social representations. In KDD, 2014.  
[21] B. Perozzi, R. Al-Rfou, および S. Skiena. DeepWalk: 社会的表現のオンライン学習. KDDにおいて, 2014年.

[22] J. Qiu et al. Network embedding as matrix factorization: Unifying DeepWalk, LINE, PTE, and node2vec. In WSDM, 2018.  
[22] J. Qiuら. 行列因子分解としてのネットワーク埋め込み: DeepWalk, LINE, PTE, および node2vecの統一. WSDMにおいて, 2018年.

[23] S. T. Roweis and L. K. Saul. Nonlinear dimensionality reduction by locally linear embedding. Science, 290(5500), 2000.  
[23] S. T. Roweis および L. K. Saul. 局所的線形埋め込みによる非線形次元削減. Science, 290(5500), 2000年.

[24] Y. Shan et al. Deep Crossing: Web-scale modeling without manually crafted combinatorial features. In CIKM, 2016.  
[24] Y. Shanら. Deep Crossing: 手動で作成された組み合わせ特徴なしのウェブスケールモデリング. CIKMにおいて, 2016年.

[25] Y. Shen, X. He, J. Gao, L. Deng, and G. Mesnil. Learning semantic representations using convolutional neural networks for web search. In WWW, 2014.  
[25] Y. Shen, X. He, J. Gao, L. Deng, および G. Mesnil. ウェブ検索のための畳み込みニューラルネットワークを用いた意味表現の学習. WWWにおいて, 2014年.

[26] S. Sriram and A. Makhani. LinkedIn’s Galene search engine, https://engineering.linkedin.com/search/did-you-mean-galene. 2014.  
[26] S. Sriram および A. Makhani. LinkedInのGalene検索エンジン, https://engineering.linkedin.com/search/did-you-mean-galene. 2014年.

[27] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov.  
Dropout: A simple way to prevent neural networks from overfitting. JMLR, 15(1), 2014.  
[27] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, および R. Salakhutdinov.  
ドロップアウト: ニューラルネットワークの過学習を防ぐためのシンプルな方法. JMLR, 15(1), 2014年.

[28] J. Tang et al. LINE: Large-scale information network embedding. In WWW, 2015.  
[28] J. Tangら. LINE: 大規模情報ネットワーク埋め込み. WWWにおいて, 2015年.

[29] J. B. Tenenbaum, V. De Silva, and J. C. Langford. A global geometric framework for nonlinear dimensionality reduction. Science, 290(5500), 2000.  
[29] J. B. Tenenbaum, V. De Silva, および J. C. Langford. 非線形次元削減のためのグローバル幾何学的フレームワーク. Science, 290(5500), 2000年.

[30] J. Weiner. The future of LinkedIn and the Economic Graph. LinkedIn Pulse, 2012.  
[30] J. Weiner. LinkedInと経済グラフの未来. LinkedIn Pulse, 2012年.  

<!-- ここまで読んだ! -->
