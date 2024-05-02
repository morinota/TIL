## 0.1. refs: refs：

- https://arxiv.org/abs/2404.13375 https://arxiv.org/abs/2404.13375

## 0.2. title タイトル

Beyond Collaborative Filtering: A Relook at Task Formulation in Recommender Systems
協調フィルタリングを超えて： 推薦システムにおけるタスクの定式化を再考する

## 0.3. abstruct abstruct

Recommender Systems (RecSys) have become indispensable in numerous applications, profoundly influencing our everyday experiences.
レコメンダーシステム（RecSys）は、多くのアプリケーションにおいて不可欠なものとなっており、私たちの日常体験に大きな影響を与えている。
Despite their practical significance, academic research in RecSys often abstracts the formulation of research tasks from real-world contexts, aiming for a clean problem formulation and more generalizable findings.
実用的な意義があるにもかかわらず、RecSysの学術研究は、しばしば研究課題の定式化を実世界の文脈から抽象化し、クリーンな問題定式化とより一般的な結果を目指している。
However, it is observed that there is a lack of collective understanding in RecSys academic research.
しかし、RecSysの学術研究においては、共通の理解が欠如しているということが観察されている。
The root of this issue may lie in the simplification of research task definitions, and an overemphasis on modeling the decision outcomes rather than the decision-making process.
この問題の根源は、研究課題の定義の単純化と、意思決定の過程よりも意思決定の結果のモデリングに過度に重点を置いていることにあるかもしれない。
That is, we often conceptualize RecSys as the task of predicting missing values in a static user-item interaction matrix, rather than predicting a user's decision on the next interaction within a dynamic, changing, and application-specific context.
つまり、**私たちはRecSysを、静的なユーザとアイテムの相互作用行列の欠損値を予測するタスクとして捉えることが多い**。**次の相互作用におけるユーザの意思決定を、動的で変化するアプリケーション固有のcontetの中で予測する**ということはあまりない。(後者の話って、例えばnext-item prediction的なタスクとして捉えるってこと??)
There exists a mismatch between the inputs accessible to a model and the information available to users during their decision-making process, yet the model is tasked to predict users' decisions.
モデルにアクセス可能な入力と、ユーザの意思決定プロセス中に利用可能な情報との間には、不一致が存在しているが、モデルはユーザの意思決定を予測することが求められている。
While collaborative filtering is effective in learning general preferences from historical records, it is crucial to also consider the dynamic contextual factors in practical settings.
協調フィルタリングは、過去の記録から一般的な嗜好を学習するのに有効であるが、**実用的な設定においては、動的なcontextual factorsも考慮することが重要**である。(文脈によって、ユーザの意思決定の傾向が変わることを考慮すべきって話??:thinking:)
Defining research tasks based on application scenarios using domain-specific datasets may lead to more insightful findings.
ドメイン固有のデータセットを使用し、アプリケーションシナリオに基づいて研究課題を定義することで、より洞察に満ちた知見が得られるかもしれない。
Accordingly, viable solutions and effective evaluations can emerge for different application scenarios.
従って、さまざまな応用シナリオに対して、実行可能な解決策と効果的な評価を導き出すことができる。

<!-- ここまで読んだ! -->

# 1. Introduction はじめに

Recommender System is an attractive research area, evidenced by the increasing number of publications in the past two decades.
レコメンダーシステムは魅力的な研究分野であり、過去20年間に出版された論文の数が増加していることからも明らかである。
Based on a prefix search of “recommend”, about 5000 publications on RecSys were indexed on DBLP within the year 2023 alone.1 As a reference, only 118 papers, or slightly above 100, were indexed in the year 2002.
"recommend"というプレフィックス検索に基づくと、2023年内だけで約5000件のRecSysに関する論文がDBLPに索引付けされたことになる1。参考までに、2002年にはわずか118件、100件をわずかに超える論文しか索引付けされていない。
(そんなに増えてるのか...!)
Given the large and increasing number of publications recently, one might expect the research community to have established a collective understanding of baseline models and evaluation protocols.
最近、多くの論文が発表され、その数も増加していることから、研究コミュニティはベースラインモデルと評価プロトコルについて、集合的な理解を確立していると予想される。
However, such assumptions may not align with reality.
しかし、そのような仮定は現実とは一致しないかもしれない。

Before we discuss the research task formulation, we brief the concerns with baseline models and evaluation protocols.
研究課題の定式化について説明する前に、ベースラインモデルと評価プロトコルに関する懸念を簡単に説明する。
In [Ivanova et al.2023], the authors state that “there are no rigid guidelines that define a comprehensive list of essential baselines”.
[Ivanova et al.2023]では、「必須ベースラインの包括的なリストを定義する厳密なガイドラインは存在しない」と述べている。
The authors then created a dataset which “contains information on 363 baselines used in 903 articles published between 2010 and 2022”.
そして著者らは、「2010年から2022年に発表された903の論文で使用された363のベースラインに関する情報を含む」データセットを作成した。
While most popular baselines can be derived from these papers, it is common to receive review comments on the lack of baselines for RecSys paper submissions.
一般的なベースラインはこれらの論文から導き出すことができるが、**RecSysの論文投稿において、ベースラインが不足しているというレビューコメントを受け取ることが一般的**である。(「このベースラインモデルも比較対象に含めなきゃ!」みたいな指摘ってことか...!:thinking:)
In other words, the authors and the reviewers do not share a common understanding of a list of must-have baselines.
言い換えれば、著者と査読者は、必ず必要なベースラインのリストについて共通の理解をもっていない。
Even if there were a shared understanding of most performing baselines, there are concerns with the quality of third-party implementation [Hidasi and Czapp 2023] and hyperparameter tuning [Shehzad and Jannach 2023].
最も性能の高いベースラインについて共通の理解があったとしても、サードパーティの実装の品質[Hidasi and Czapp 2023]やハイパーパラメータの調整[Shehzad and Jannach 2023]に関する懸念がある。(うんうん、実装方法や調整次第で、性能がばらつくよね...!:thinking:)
Thus, reproducibility becomes a concern, and ACM RecSys conference has a recommended list of implementation and evaluation frameworks.2 Interestingly, a few largescale benchmark evaluations show that simple baselines like nearest-neighbor outperform more advanced models (see Table 3 and Section 3.2 in [Bauer et al.2024] for a summary and insightful discussion).
興味深いことに、**いくつかの大規模なベンチマーク評価では、nearest-neighborなどの単純なベースラインが、より高度なモデルよりも優れた性能を発揮することが示されている**（要約と洞察的な議論については、[Bauer et al.2024]の表3とセクション3.2を参照）。
Probably the most comprehensive evaluation, [McElfresh et al.2022] compares “24 algorithms and 100 sets of hyperparameters across 85 datasets and 315 metrics”.
おそらく最も包括的な評価である[McElfresh et al.2022]は、「85のデータセットと315のメトリックにわたる24のアルゴリズムと100のハイパーパラメータセットを比較している」。
All models in the comparison can be the best on some dataset with some metric.
**比較に含まれる全てのモデルは、いくつかのデータセットといくつかのメトリックで最も優れている可能性がある**。
Authors note that “the algorithms do not generalize – the set of algorithms which perform well changes substantially across datasets and across performance metrics”.
著者は、「**アルゴリズムは一般化されていない - 上手く機能するアルゴリズムの集合は、データセットとperformance metricsにわたって大幅に変化する**」と述べている。(うんうん...!:thinking:)
Nevertheless, the simple Item-KNN model is among best performing models, with the highest average ranking position of 2.3 among 20 models (see Table 1 in [McElfresh et al.2022]).
それにもかかわらず、**単純なItem-KNNモデルは、20のモデルの中で最も高い平均順位2.3位を獲得し、最も良いパフォーマンスを示すモデルの一つである**（[McElfresh et al.2022]の表1を参照）。

In my understanding, various datasets used in RecSys research reflect diverse application scenarios, each necessitating its own set of most effective solutions.
私の理解では、RecSysの研究で使用されるさまざまなデータセットは、異なるアプリケーションシナリオを反映しており、それぞれが最も効果的な解決策を必要としている。
However, the simplified task definition abstracts away differences in their practical settings, resulting in model comparability on their prediction accuracies across all datasets.
しかし、簡略化されたタスクの定義は、実際の設定の違いを抽象化し、すべてのデータセットにわたって予測精度を比較可能にしている。
Finding a single model capable of excelling in all application scenarios is challenging.
**すべてのアプリケーション・シナリオで優れた性能を発揮できる単一のモデルを見つけるのは困難である**。(そもそも存在しないんじゃない??:thinking:)
Yet, different forms of nearest neighbors appear to be a common theme in RecSys, to be elaborated further in Section 3.
しかし、最近のRecSysでは、異なる形式の最近傍が共通のテーマであるようだが、これについてはセクション3で詳しく説明する。(どういう意味??:thinking:)

If we rely on the results from these large-scale benchmark evaluations, it seems that no much progress has been made in RecSys, which was a question asked in [Dacrema et al.2019; Ferrari Dacrema et al.2021].
これらの大規模ベンチマークの評価結果に頼ると、RecSysにおいてはあまり進歩が見られないようである。 これは[Dacrema et al.2019; Ferrari Dacrema et al.2021]で問われた疑問である。
On the other hand, the results of evaluation also heavily depend on the evaluation protocol, in particular, the datasets and the train/test split of a dataset.
**一方、評価結果は、評価プロトコル、特にデータセットとデータセットの訓練/テスト分割方法に大きく依存している**。(データセットの選択とtrain/testの分割方法の選択によって、評価結果が大きく変わるってことか...!:thinking:)
A very recent survey [Bauer et al.2024] shows that “the same few (and relatively old) datasets (i.e., MovieLens, Amazon review dataset) are used extensively”, and the heavy usage of the MovieLens dataset has also been noted in [Sun et al.2023].
ごく最近の調査[Bauer et al.2024]では、「同じ数少ない（比較的古い）データセット（つまり、MovieLens、Amazonレビューデータセット）が広範囲に使用されている」と述べており、**MovieLensデータセットの大量使用は[Sun et al.2023]でも指摘されている**。
Bauer et al.further comment that “older datasets may not be good proxies of the user behavior and preferences of today’s users”.
バウアーらはさらに、「古いデータセットは、今日のユーザの行動や嗜好の良い代理とはならないかもしれない」とコメントしている。
In particular, movies rated by a user on MovieLens are those he/she has watched before, hence the dataset cannot simulate the situation of recommending new movies to users [Fan et al.2024].
特に、MovieLensでユーザが評価した映画は、彼/彼女が以前に視聴したものであり、したがって、データセットはユーザに新しい映画を推薦する状況をシミュレートすることはできない[Fan et al.2024]。
Further, the majority of RecSys evaluations do not take global timeline into consideration when splitting a dataset into train and test sets [Sun 2023; Ji et al.2023].
さらに、RecSysの評価の大半は、**データセットを訓練セットとテストセットに分割する際に、global timelineを考慮に入れていない**[Sun 2023; Ji et al.2023]。(これは前に読んだ論文達でもちょくちょく主張される話だよね...!:thinking:)
As a result, the model under offline evaluation is given access to data records that happen in the future (e.g., new items, new users, and also useritem interactions) with respect to the time point of the test instance.
その結果、オフライン評価下のモデルは、テストインスタンスの時点に関して未来に発生するデータレコード(ex. 新しいアイテム、新しいユーザ、新しいユーザとアイテムの相互作用)にアクセスできる。
This unrealistic offline evaluation setting may also stem from the simplified formulation of the RecSys task, which overlooks the global timeline.
この非現実的なオフライン評価設定は、RecSysタスクの単純化された定式化に起因する可能性もあり、global timelineを見落としている。

<!-- ここまで読んだ! -->

# 2. The Established RecSys Task Formulation 確立されたRecSysタスクの定式化

In Chapter 1 of the Recommender Systems Handbook, the core recommendation computation is defined as the prediction of the utility (or evaluation) of an item for a user [Ricci et al.2022].
レコメンダー・システム・ハンドブックの第1章では、**core recommendation computation(核となる推薦計算?)が、ユーザにとってのアイテムのutility/evaluation (効用 or 評価)を予測することと定義されている**[Ricci et al.2022]。(うんうん...!)
The degree of utility/evaluation of user u for item i is modeled as a (real-valued) function R(u, i).
アイテム $i$ に対するユーザ $u$ の効用/評価の程度は、(実数値の)関数 $R(u, i)$ としてモデル化される。
Then, “the fundamental task of a recommender system is to predict the value of R(u, i) over pairs of users and items”.
そして、「**レコメンダーシステムの基本的なタスクは、ユーザとアイテムのペアに対してR(u, i)の値を予測すること**」である。(うんうん...!)

We also reference two very recent survey papers at the time of writing.4 In the survey on modern recommender systems using generative models, [Deldjoo et al.2024] consider “a setup where only the user-item interactions (e.g., ‘user A clicks item B’) are available, which is the most general setup studied in RecSys”.
生成モデルを用いた現代のレコメンダーシステムに関するサーベイ論文[Deldjoo et al.2024]では、「ユーザーとアイテムの相互作用のみが利用可能なセットアップ(ex. 'ユーザAがアイテムBをクリック')を考慮しており、これはRecSysで研究されている最も一般的なセットアップである」と述べている。(interactionデータのみを使うタスクってこと?? これが現実的じゃないよねっていう主張かな...!:thinking:)
In the survey on self-supervised learning for recommendation, [Ren et al.2024] formally define the RecSys task with two primary sets: the set of users U and the set of items I.
推薦のための自己教師付き学習に関するサーベイにおいて、[Ren et al.2024]はRecSysタスクを2つの主要な集合で正式に定義している： ユーザの集合 $U$ とアイテムの集合 $I$ 。
Then, an interaction matrix U × I is utilized to represent the recorded interactions between users and items, where a value 1 entry means a user has interacted with an item, and 0 otherwise.
次に、ユーザとアイテムの間の記録された相互作用を表すために、ユーザ $U$ × アイテム $I$ の相互作用行列が利用される。ここで、値1のエントリはユーザがアイテムと相互作用したことを意味し、それ以外は0である。(implicit feedbackの例か...!)
The definition in [Ren et al.2024] also includes a notion of auxiliary observed data denoted as X; an example is “a knowledge graph comprising external item attributes”.
また、[Ren et al.2024]の定義には、$X$ として示される補助的な観測データの概念も含まれており、例として「外部アイテム属性を含む知識グラフ」が挙げられている。(メタデータとか?)
Then a recommendation model aims to estimate the likelihood of a user interacting with an item based on the interaction matrix, and the auxiliary observed data if available.
そして、**推薦モデルは、相互作用行列と、もしあれば補助的な観測データに基づいて、ユーザがアイテムと相互作用する可能性を推定することを目的とする**。(うんうん...!)

The task definitions reviewed above seem to be a common understanding in the RecSys research community.
上記のタスク定義は、RecSysの研究コミュニティでは共通の認識となっているようだ。(うんうん、自分も共通認識もってた)
But there are also papers that mention the issue of simplification or over-simplification in RecSys research.
しかし、**RecSys研究におけるsimplificationやover-simplificationの問題を指摘**する論文もある。
In Section 7 of the review paper on popularity bias in RecSys, [Klimashevskaia et al.2023] summarize a few observations regarding the research on popularity bias, including “no agreed-upon definition of what represents popularity bias” in RecSys.
Klimashevskaiaら[2023]は、RecSysの人気バイアスに関するレビュー論文の第7節で、人気バイアスに関する研究に関するいくつかの観察をまとめており、「**RecSysにおける人気バイアスを表すものの定義について合意がない**」と述べている。
The authors further state that “these observations point to a certain over-simplification of the problem and an overly abstract research operationalization, a phenomenon which can also be observed in today’s research on fairness in recommender systems”.
さらに、著者らは、「これらの観察は、問題の過度な単純化と過度な抽象的な研究の操作化を指摘しており、これは今日のレコメンダーシステムにおける公平性に関する研究でも観察される現象である」と述べている。
In the perspective paper on offline evaluations, [Castells and Moffat 2022] consider the adoption of offline evaluation methodologies from experimental practice in Machine Learning (ML) and Information Retrieval (IR) to RecSys evaluation is a form of simplification.
オフライン評価に関する展望論文[Castells and Moffat 2022]では、**機械学習（ML）や情報検索（IR）の実験的practiceからRecSys評価へのオフライン評価方法論の採用**は、単純化の形態であると考えられている。(nDCGによる評価とかはまさにこれだよね...!:thinking:)
To my understanding, over-simplification commonly exists in research task formulation in RecSys [Sun 2023].
私の理解では、RecSys[Sun 2023]の研究タスクの定式化には、**単純化しすぎ**がよく見られる。
Next, we zoom into the RecSys task formulation from three perspectives: user, model, and item.
次に、**RecSysタスクの定式化を3つの視点から**見ていく：ユーザ、モデル、アイテム。

<!-- ここまで読んだ! -->

# 3. User, Model, and Item ユーザ、モデル、アイテム

The current RecSys task definition mainly involves users, items, and their interactions, in a static view.
現在のRecSysのタスク定義は、**主に静的なビュー**で、ユーザ、アイテム、およびそれらの相互作用を含む。(static view = batch学習的な??:thinking:)
The task of RecSys is viewed as a task of predicting missing values in an incomplete user-item interaction matrix.
RecSysのタスクは、不完全なユーザとアイテムの相互作用行列の欠損値を予測するタスクとして捉えられている。(うんうん)
Then user-item interaction matrix becomes the key focus of RecSys research.
そして、ユーザとアイテムの相互作用行列がRecSys研究の主要な焦点となる。(うんうん...!)
However, if we examine any specific user-item interaction, it occurs at a particular time point and is the outcome of the user’s decision-making.
しかし、特定のユーザとアイテムの相互作用を調べると、それは特定の時点で発生したものであり、ユーザの意思決定の結果である。(うんうん...!)
The decision-making can be influenced by various contextual factors.
意思決定はさまざまなcontextual factors(文脈要因)に影響を受ける可能性がある。

![fig1]()
Fig. 1. Illustration of two rounds of recommendations made to a user: (i) user triggers a recommender with her past interaction history Iu and receives the first set of recommendations R1; and (ii) the user interacts with item i2 after a decision-making process d1, and receives the second set of recommendations R2. The user then interacts with i4 after another decision-making d2. Accordingly, the item collection is updated with the two new interactions. Note that, R1 and R2 are made with different inputs to the model. Best viewed in color.
図1. ユーザに対して行われた**2つのラウンドの推薦**のイラスト：(i) ユーザは過去の相互作用履歴 $I_{u}$ でレコメンダーをトリガーし、最初の推薦 $R_{1}$ を受け取る；および(ii) ユーザは意思決定プロセス $d_{1}$ の後にアイテム $i_{2}$ と相互作用し、2番目の推薦 $R_{2}$ を受け取る。ユーザは別の意思決定 $d_{2}$ の後に $i_{4}$ と相互作用する。したがって、アイテムコレクションは2つの新しい相互作用で更新される。$R_{1}$ と $R_{2}$ は、モデルへの異なる入力で行われる。カラーで表示されるとよい。

We use Figure 1 to illustrate the interactions between a user and a collection of items, through a recommender i.e., a model.
図1を用いて、レコメンダーすなわちモデルを介した、ユーザとアイテムのコレクションとの間の相互作用を説明する。
We assume that the user is familiar with the recommendation service, and the service provider has historical records of the user’s past interactions with the platform.
我々は、ユーザがレコメンデーションサービスに精通しており、サービスプロバイダがユーザの過去のプラットフォームとのインタラクションの履歴記録を持っていると仮定する。(コールドスタートユーザじゃない設定ってことね...!)
We also assume that the model is well-trained and its parameters are fixed, then its output depends solely on its input.
また、モデルは十分に訓練され、そのパラメータは固定されており、その出力は入力のみに依存すると仮定する。

At time point t0, user u begins interacting with the recommendation service by opening a mobile app or a website, such as YouTube for video viewing or Amazon for products.
時点 $t_0$ において、ユーザ $u$ は、ビデオ視聴のためのYouTubeや商品のためのAmazonなどのモバイルアプリやウェブサイトを開いて、**レコメンデーションサービスとの相互作用を開始する**。
Based on the set of items that u has interacted with before t0, denoted by Iu, the model makes recommendations R1 = {i1, i2, i3} from a pool of candidate items.
$I_{u}$ で表される時点 $t_0$ 以前に $u$ が相互作用したアイテムのセットに基づいて、モデルは候補アイテムのプールから推薦 $R_{1} = \{i_{1}, i_{2}, i_{3}\}$ を行う。
Upon receiving the recommendations R1 at time t1, u considers these three items and chooses to interact with i2.
時刻 $t_1$ において、$u$ はこれらの3つのアイテムを考慮し、$i_{2}$ と相互作用することを選択する。
Accordingly, right after time t1, the interaction records available to the model would be Iu ∪ {i2}.
したがって、時刻 $t_1$ 直後に、モデルに利用可能な相互作用記録は $I_{u} \cup \{i_{2}\}$ となる。
With the current input of Iu ∪ {i2}, the model makes the next round of recommendation R2 = {i4, i5, i6} at time t2.
現在の $I_{u} \cup \{i_{2}\}$ の入力により、モデルは時刻 $t_2$ に次の推薦 $R_{2} = \{i_{4}, i_{5}, i_{6}\}$ を行う。
Upon further consideration, the user selects i4 for interaction.
さらに検討した結果、ユーザは対話のために $i_{4}$ を選択する。
Consequently, for the subsequent round of recommendations, the model assimilates additional knowledge from Iu ∪ {i2, i4} to make more accurate predictions regarding the user’s current interests within the current interaction session.
その結果、次の推薦ラウンドでは、モデルは $I_{u} \cup \{i_{2}, i_{4}\}$ から**追加の知識を取り込み**、現在の相互作用セッション内でのユーザの現在の興味に関するより正確な予測を行う。
(Twitter上で論文著者とmetaのMLエンジニアの方が議論してたのは、このあたりの{i2, i4}のリアクションの知識への感度が鈍い、みたいな内容だった...!:thinking:)

Here, we assume that the two recommendations, R1 and R2, occur consecutively within a single session of interactions.
ここでは、 $R_{1}$ と $R_{2}$ の2つの推薦が、1つの相互作用セッション内で連続して発生すると仮定する。
It is important to note that in this illustration, we distinguish between the two newly available interactions {i2, i4} and the past historical interactions Iu.
**この図では、新しく利用可能になった2つの相互作用 $\{i_{2}, i_{4}\}$ と過去の相互作用 $I_{u}$ の間に区別をつけることが重要**である。(なるほど...?? 最新のinteractionへの感度を上げろって主張??:thinking:)
This distinction is made because interactions to {i2, i4} just occurred, while Iu may have occurred much earlier, with respect to the current session.
この区別は、$\{i_{2}, i_{4}\}$ への相互作用がたった今発生したのに対して、$I_{u}$ は現在のセッションに関してはるかに過去に発生している可能性があるためである。

From the user’s perspective, at time t0, upon opening the recommendation service, the user expects the recommender to accurately predict her latent needs on information, services, or products.
**ユーザの視点**からは、時刻 $t_0$ において、レコメンデーションサービスを開いた際、**ユーザは、レコメンダーが情報、サービス、または製品に関する彼女の潜在的なニーズを正確に予測することを期待している**。
Upon receiving recommendations R1 at t1, the decision to interact with i2 is the outcome of a decision process, represented by d1 in the figure.
時刻 $t_1$ において、推薦 $R_{1}$ を受け取った後、$i_{2}$ と相互作用する決定は、図に示されている $d_{1}$ によって表される決定プロセスの結果である。
This decision process may consider various factors, such as attributes of the recommended items, the user’s current location, time of day, ongoing activities, and even the user’s mood.
この決定プロセスでは、推薦されたアイテムの属性、ユーザの現在の場所、時間帯、進行中の活動、さらにはユーザの気分など、さまざまな要因が考慮されるかもしれない。
For example, users may choose to watch different types of videos on YouTube depending on whether they are feeling happy or sad.
**例えば、ユーザは楽しい気分か悲しい気分かによって、ユーチューブで異なるタイプのビデオを見ることを選ぶかもしれない**。(その時のcontextによって、ユーザの意思決定の傾向は、dynamicに変わるよねって話か:thinking:)
The interaction with i4 is the outcome of another decision process.
$i_{4}$ との相互作用は、別の決定プロセスの結果である。

From the model’s perspective, the two sets of recommendations are generated by using different user-side inputs: Iu for R1, and Iu ∪ {i2} for R2, respectively.
モデルの観点からは、2つの推薦セットは、異なるユーザ側の入力を使用して生成される：$R_{1}$ には $I_{u}$ 、$R_{2}$ には $I_{u} \cup \{i_{2}\}$ がそれぞれ使われる。
If a subsequent recommendation is to be made, the user-side input will be Iu ∪ {i2, i4}.
その後の推薦を行う場合、ユーザー側の入力は $I_{u} \cup \{i_{2}, i_{4}\}$ となる。
Moreover, the user’s decisions to interact with i2 from R1 and i4 from R2 may strongly suggest that the user, at the current moment, is interested in items similar to or related to i2 and i4, yet confined by the overall preference demonstrated through Iu.
さらに、$R_{1}$ から $i_{2}$ と $R_{2}$ から $i_{4}$ との相互作用を選択するユーザの決定は、**現在の瞬間において、$I_{u}$ を通じて示された全体的な嗜好によって制限されつつ、$i_{2}$ と $i_{4}$ に類似したアイテムに興味を持っていることを強く示唆している**。(長期的な嗜好と短期的な嗜好の両方の観点があるってこと??:thinking:)
Taking videos as example items, similar videos to i2 and i4 include videos in the same genre, uploaded by the same content creator, or featuring the same actors, and yet not too distinct from those viewed in the past.
動画を例にとると、$i_{2}$ と $i_{4}$ に類似した動画には、同じジャンルの動画、同じコンテンツクリエイターがアップロードした動画、または同じ俳優が出演する動画などが含まれるが、過去に視聴したものとあまり異ならない。
The relationships between items may also be established through various means, e.g., by content similarity, by collaborative filtering, or other forms of knowledge.
アイテム間の関係は、コンテンツの類似性、協調フィルタリング、または他の形式の知識によっても確立されるかもしれない。
In many cases, Iu serves as a valuable resource for understanding a user’s general and enduring preferences, gleaned from past interactions.
多くの場合、$I_{u}$ は、**過去の相互作用から得られたユーザのgeneral(一般的)でenduring(持続的)な嗜好**を理解するための貴重なリソースとして機能する。(="一般的で持続的な嗜好"って表現いいな...!:thinking:)
In the ongoing interaction session, the identification of {i2, i4} reveals the user’s current interests, prompting recommendations of similar or related items.
進行中のインタラクション・セッションでは、$\{i_{2}, i_{4}\}$ の特定は、**ユーザの現在の興味**を明らかにし、類似または関連するアイテムの推薦を促す。
This could explain why item-KNN continues to perform well in many evaluations.
これは、item-KNNが多くの評価で良好な結果を出し続けている理由を説明できるだろう。
(ん、なんで??よく分かってない...!:thinking:)

<!-- ここまで読んだ! -->

From the item’s perspective, as depicted in the upper portion of Figure 1, after the two interactions from user u, both i2 and i4 each receive an additional interaction.
アイテムの視点から見ると、図1の上部に描かれているように、ユーザ $u$ からの2つの相互作用の後、$i_{2}$ と $i_{4}$ はそれぞれ追加の相互作用を受ける。
If we consider the number of interactions an item receives as the popularity attribute of the item, then the attributes of both items change.
**アイテムが受ける相互作用の数をアイテムの人気属性と考えると、両方のアイテムの属性が変化する**。(t_0とt_1の間に、i2とi4の人気度属性の値が変動するってことだよね:thinking:)
Given that a typical recommender system serves a substantial number of users concurrently, such attribute changes can significantly impact a large number of items within a short period.
典型的なレコメンダーシステムは、多数のユーザに同時にサービスを提供するため、このような属性の変化は短期間で多数のアイテムに大きな影響を与える可能性がある。
In extreme cases, a popular video can attract thousands or even millions of views within a day or two.
極端な例では、人気のあるビデオは1日か2日のうちに何千、何百万という再生回数を集めることもある。

In short, from three perspectives of user, model, and item, a recommender system should be viewed in a dynamic setting, instead of a prediction of missing values in a static useritem interaction matrix.
つまり、ユーザー、モデル、アイテムの3つの観点から、レコメンダーシステムは、**静的なユーザとアイテムの相互作用マトリックスにおける欠損値の予測ではなく、動的な設定で見られるべき**である。
However, the dynamic nature of RecSys is largely overlooked in academic research, as the time dimension is often omitted from RecSys task definitions.
**しかし、RecSysのダイナミックな性質は、学術研究においてはほとんど見落とされており、RecSysのタスク定義から時間の次元が省かれていることが多い**。(なるほど...!)
The ignorance of the global timeline in the task formulation is also the root of data leakage in offline evaluation.
タスク策定における**グローバルタイムラインの無視も、オフライン評価におけるデータ漏洩の根源**である。(それはそう...!)
More importantly, current task definitions do not sufficiently focus on the decision-making process [Kleinberg et al.2022; Jameson et al.2022].
さらに重要なことは、**現在のタスク定義では、意思決定プロセスに十分に焦点が当てられていないこと**である[Kleinberg et al.2022; Jameson et al.2022]。(これは予測問題として扱ってしまうってこと?? もしくはユーザのcontextの考慮に関すること??:thinking:)

<!-- ここまで読んだ! -->

# 4. Recommenders are Task-specific レコメンダーはtask-specificである

The recommendations generated by a model are influenced by the information it gathers from its inputs.
モデルが生成するレコメンデーションは、インプットから収集した情報に影響される。
These inputs vary significantly depending on the application scenario.
**これらの入力は、アプリケーションのシナリオによって大きく異なる。**(ふむふむ...!)
Let us consider food recommendation as an example application.
食品を推薦するアプリケーションを例に考えてみよう。
When users open a food delivery app, they place their orders and await the arrival of their chosen dishes.
フードデリバリーアプリを開くと、ユーザは注文をし、選んだ料理の到着を待つ。
Effective recommendations streamline the ordering process, potentially reducing browsing time and allowing users to receive their food earlier.
効果的な推薦は、注文プロセスを効率化し、ブラウジング時間を短縮し、ユーザが食事を早く受け取ることを可能にする。

Following the current practice, a typical task formulation is: Given a set of users U, a set of food items I, and a user-item interaction matrix U × I storing the past orders of all users,7 the task is to predict the likelihood of users place orders on the food items.
現在の実践に従い、典型的なタスク定義は、ユーザ $U$ の集合、食品アイテム $I$ の集合、およびすべてのユーザの過去の注文を格納するユーザとアイテムの相互作用行列 $U \times I$ が与えられた場合、ユーザが食品アイテムに注文をする可能性を予測することである。
Again, this is an oversimplified problem definition.
繰り返すが、これは単純化しすぎた問題定義である。
Taking the application scenario into account, it is crucial to recognize the diverse food preferences people have for breakfast, lunch, and dinner.
**このアプリケーションのシナリオを考慮すると、朝食、昼食、夕食における人々の食の嗜好の多様性を認識することが極めて重要**である。
Therefore, considering the time of day in food recommendations becomes essential.
そのため、食事の推薦において時間帯を考慮することが重要となる。
Additionally, since the order is for delivery, the anticipated delivery time significantly impacts user experience.
さらに、注文は配送のため、予想される配送時間はユーザ体験に大きな影響を与える。
There is a notable correlation between delivery time and the distance between the user and the food store fulfilling the order.
配達時間と注文を満たす食品店とユーザとの距離との間には顕著な相関がある。
The ordering time and delivery address are both available to the app and the recommendation model.
注文時間と配達先の住所は、アプリとレコメンデーションモデルの両方で利用可能だ。
As a piece of domain-specific knowledge, there is a strong presence of repeat patterns in food delivery i.e., users often repeatedly place orders from the same store [Li et al.2024].
ドメイン特有の知識として、食品配達においてリピートパターンが強く存在すること、つまり、ユーザは同じ店から何度も注文をすることが多いことがある[Li et al.2024]。

The task formulation shall then be revised.
その後、**タスクの定式化を見直す必要がある**。
We have a set of users U, a collection of food items I, and a collection of past transactions as user-item interactions U × I with auxiliary detailed information such as order timestamps and delivery details.
我々は、ユーザ $U$ の集合、食品アイテム $I$ のコレクション、注文のタイムスタンプや配達の詳細などの補助的な詳細情報を持つ過去のトランザクションのコレクションとしてのユーザとアイテムの相互作用 $U \times I$ を持っている。
When user u triggers a food delivery recommendation request at time t, the application is tasked to provide recommendations by considering the temporal context (t), the delivery address (s), all previous orders (U × I), and the user’s purchase history (Iu).
ユーザ $u$ が時刻 $t$ に食品配達の推薦リクエストをトリガーすると、アプリケーションは、時間的コンテキスト($t$)、配達先($s$)、すべての過去の注文($U \times I$)、およびユーザの購入履歴($I_{u}$)を考慮して推薦を提供することが求められる。

Note that Iu is part of U × I, yet it is necessary to separately consider Iu due to the recurrent pattern; users frequently reorder food they have previously tried.
$I_{u}$ は $U \times I$ の一部であるが、recurrent(繰り返し)パターンがあるため、別々に考慮する必要がある; ユーザは以前に試した食品を頻繁に再注文する。(sequential data的な考慮ってことか...!:thinking:)
The primary distinction lies in the item search space: for repeat orders, we recommend items from within Iu, whereas, for first-time or exploration orders, the search space is I − Iu; and |I − Iu| ≫ |Iu| in terms of cardinality.
**主な違いは、アイテムの検索空間にある**: リピートオーダーの場合、$I_{u}$ の中からアイテムを推薦し、一方、初めてのオーダーや探索オーダーの場合、検索空間は $I - I_{u}$ であり、濃度に関して $|I - I_{u}| \gg |I_{u}|$ である。(推薦アイテム候補の違い？？:thinking:)f
Due to the significant difference in the search space, separate recommendation models can be designed for repeat and exploration orders respectively [Li et al.2024].
**探索空間が大きく異なるため、推薦モデルはリピート・オーダーと探索オーダーのそれぞれに設計することができる**[Li et al.2024]。

In this case study, the task formulation has evolved beyond simply predicting missing values in a basic and static user-item interaction matrix, now incorporating additional spatial and temporal dimensions.
このケーススタディでは、タスクの定式化は、基本的で静的なユーザとアイテムの相互作用マトリックスにおける欠損値を予測するだけでなく、追加の空間的および時間的次元を取り入れて進化している。
The strong presence of domain-specific knowledge on repeated consumption significantly influences the design of recommendation models, as this knowledge directly affects the item search space.
**リピート消費に関するドメイン特有の知識の強い存在は、推薦モデルの設計に大きな影響を与える。なぜなら、この知識はアイテムの検索空間に直接影響を与えるからだ**。
Such additional information in the input may or may not affect the recommendation modeling, but these factors may heavily affect the user’s decision-making from the user’s perspective.
入力に含まれるこのような追加情報は、推薦モデリングに影響を与える場合もあれば、与えない場合もあるが、**ユーザの視点から見ると、これらの要因はユーザの意思決定に大きな影響を与える可能性がある**。(動画で言えば、出演者とか??)
Similar recommendation scenarios include hotel recommendations and restaurant recommendations.
同様の推薦シナリオには、ホテルの推薦やレストランの推薦などがある。
In both cases, recommendations are more meaningful when a user plans to visit an unfamiliar place.
どちらの場合も、**ユーザが見知らぬ場所を訪れる予定がある場合、レコメンデーションはより有意義なものとなる**。
The destination to be visited should be considered as a known input to the recommendation model, e.g., booking a hotel for attending a conference two months later in a different city.
例えば、2ヶ月後に別の都市で開催される会議に出席するためにホテルを予約するといったように、訪問先は推薦モデルへの既知の入力として考慮されるべきである。
Similarly, if a user explicitly expects songs from a specific singer or movies featuring a particular actor/actress or genre, these preferences become part of the input.
同様に、ユーザが特定の歌手の曲や、特定の俳優・女優の出演する映画やジャンルを明示的に期待している場合、これらの嗜好は入力の一部となる。
It is important to note that while related, these additional inputs differ from the side information widely studied in recommendation systems [Sun et al.2019].
関連はあるが、**これらの追加入力は推薦システムで広く研究されているside informationとは異なることに注意**することが重要である[Sun et al.2019]。(side informationって何??:thinking:)
Side information, such as knowledge graphs about items, may only be available to the RecSys model and remain transparent to users.
アイテムに関する知識グラフなどの**side informationは、RecSysモデルにのみ利用可能であり、ユーザにはtransparent(透明)のまま**である。(ユーザには認知されない情報ってことか??:thinking:)
Furthermore, the exploration of side information has primarily focused on enhancing model accuracy or addressing issues like cold start or cross-domain settings, which users are typically unaware of, and are not factors in users’ decision-making.
さらに、side informationの探索は、主にモデルの精度向上やcold startやcross-domain設定などの問題に対処することに焦点を当てており、**これらは通常ユーザが認識していない要因であり、ユーザの意思決定には影響を与えない**。(なるほど...!:thinking:)

<!-- ここまでよんだ! なるほど side information と ユーザの意思決定に影響を与えるcontext...! -->

Based on the above discussion, we may consider a recommender taking the following inputs: ⟨X, u, Iu, Ic, I, U × I⟩.
上記の議論に基づき、以下の入力を持つレコメンダーを考えることができる： X, u, Iu, Ic, I, U × I⟩。
Among them, X represents task-specific contextual inputs such as time and location.
このうち、Xは時間や場所といったタスク固有の文脈入力を表す。
Note that, the X here refers to those contextual factors that are available to and/or accessible by the users or even the explicit input from users e.g., movie genre.
なお、ここでいうXとは、ユーザーが利用可能な、あるいはアクセス可能な文脈的要素、あるいはユーザーからの明示的な入力、たとえば映画のジャンルなどを指す。
These factors are part of the user’s decision-making consideration and are not auxiliary knowledge only known to the model but not to users.
これらの要因は、ユーザーの意思決定の考慮事項の一部であり、モデルだけが知っていてユーザーが知らない補助的な知識ではない。
Among the remaining inputs, u denotes the user who initiates the recommendation service, Iu consists of the user’s past interacted items, and Ic comprises the newly interacted items in the current session (e.g., {i2, i4} in Figure 1).
残りの入力のうち、uは推薦サービスを開始したユーザ、Iuはユーザの過去の対話項目、Icは現在のセッションで新たに対話された項目（例えば、図1の{i2, i4}）を示す。
Ic is empty at the start of the current session, and changes along with the increasing availability of new interactions.
Icは現在のセッションの開始時点では空であり、新しい相互作用の利用可能性が高まるにつれて変化する。
I refers to all candidate items available for recommendation.
推薦可能なすべての候補を指す。
With the increasing available interactions, some of the interaction-related attributes of items in I are dynamically updated e.g., the number of interactions an item receives.
利用可能なインタラクションが増えるにつれて、Iのアイテムのインタラクション関連属性のいくつかは動的に更新される。
U × I represents historical user-item interactions before the current session.8 The task of a recommender is to generate recommendations for user u under the current decision-making context.
U×Iは現在のセッション以前の過去のユーザーとアイテムのやりとりを表す。
For comparison, the inputs considered in common RecSys task formulations are ⟨u, I, U × I⟩.
比較のために、一般的なRecSysタスクの定式化で考慮される入力は⟨u, I, U × I⟩である。

# 5. The Mismaching Datasets ♪ミスマッチング・データセット

We have outlined the inputs that a recommender system should consider, primarily to highlight the dynamic nature of RecSys by emphasizing the context of decision-making.
レコメンダーシステムが考慮すべきインプットを概説したが、これは主に意思決定の文脈を強調することでRecSysのダイナミックな性質を強調するためである。
Note that, the consideration of both user’s general preferences and the current contexts is not new at all.
なお、ユーザーの一般的な好みと現在のコンテキストの両方を考慮することは、まったく新しいことではない。
[Cheng et al.2016] consider not only user (static) features like country, language, and age, but also contextual features like device, hour of the day, day of the week for app recommendation.
[Cheng et al.2016]は、アプリ推薦のために、国、言語、年齢といったユーザー（静的）特徴だけでなく、デバイス、時間帯、曜日といったコンテキスト特徴も考慮する。
[Zhou et al.2018] also consider context features for click-through rate prediction.
また、[Zhou et al.2018]もクリックスルー率予測のためにコンテキスト特徴を考慮している。
A “User Instant Interest” modeling layer is part of the solution proposed in [Xiao et al.2024] to model the user’s current interest following the user’s behavior i.e., clicking an item that is referred to as a trigger item.
ユーザー瞬間関心 "モデリングレイヤーは、[Xiao et al.2024]で提案されたソリューションの一部であり、ユーザーの行動、すなわちトリガーアイテムと呼ばれるアイテムをクリックした後のユーザーの現在の関心をモデル化する。
The assumption is that “the clicked trigger item explicitly represents the user’s instant interests”.
その前提は、「クリックされたトリガーアイテムが、ユーザーの瞬間的な興味を明示的に表している」ということである。
Note that, all aforementioned papers are from industry.
なお、前述の論文はすべて産業界のものである。
Eventually, in a practical setting, the recommendation is a ranking problem with at least two forms of latent needs of information/service/product, learned from (i) the relatively static user/item features and historical interactions, and (ii) the current and dynamic interaction process, respectively.
結局、実用的な設定では、推薦とは、(i)比較的静的なユーザー／アイテムの特徴と過去のインタラクション、および(ii)現在のインタラクションプロセスと動的なインタラクションプロセスからそれぞれ学習された、情報／サービス／製品に関する少なくとも2つの潜在的ニーズを持つランキング問題である。
The learned preferences then serve as implicit queries for item ranking or re-ranking [Liu et al.2022].
学習された嗜好は、アイテムのランク付けや再ランク付けのための暗黙のクエリーとして機能する[Liu et al.2022]。
However, in academic research, accessing an online recommendation platform is not feasible in most cases.
しかし、学術研究においては、オンライン推薦プラットフォームにアクセスすることは、ほとんどの場合不可能である。
The comprehension of the current context relies on two factors.
現在の状況を理解するには、2つの要素が必要だ。
The first factor is the information available in an offline dataset.
第一の要因は、オフラインデータセットで利用可能な情報である。
The widely used datasets like MovieLens and Amazon reviews only record the outcomes of the decision-making process, but not the context of decision-making e.g., under what consideration and/or among which options, a user decides to watch a movie or buy a product.
MovieLensやAmazonレビューのような広く使われているデータセットは、意思決定プロセスの結果のみを記録しているが、意思決定のコンテキストは記録していない。
The second factor is the way a dataset is used, e.g., whether the user-item interactions are arranged in chronological order following the global timeline, and how a model is trained and evaluated on the dataset.
第二の要因は、データセットの使われ方である。例えば、ユーザーとアイテムのインタラクションが、グローバルなタイムラインに従って時系列に並んでいるかどうか、そして、データセットに対してモデルがどのようにトレーニングされ評価されるか、などである。
We further elaborate on the second factor through Figure 2.
図2を通して、2つ目の要因についてさらに詳しく説明する。
The figure shows an illustration of train/test instances using leave-one-out data split with interactions by three example users.
図は、3人のユーザーによるインタラクションで分割されたリーブワンアウトデータを使用した訓練/テストインスタンスの説明図である。
Here, all interactions are arranged in chronological order following the global timeline.
ここでは、すべての交流がグローバルタイムラインに従って時系列に並べられている。
The last interaction of each user is the test instance, represented by a squared octagonal star, and the circles represent training instances.
各ユーザーの最後のインタラクションがテスト・インスタンスで、四角い八角形の星で表され、丸はトレーニング・インスタンスを表す。
Following a typical offline evaluation, illustrated in the lower half of the figure, a model is trained by using all training instances, and then evaluated on all test instances.
図の下半分に示される典型的なオフライン評価に従って、モデルはすべてのトレーニングインスタンスを使ってトレーニングされ、次にすべてのテストインスタンスで評価される。
Take user u1 as an example.
ユーザーu1を例にとろう。
Many training interactions in the dataset occurred after u1’s test instance i.e., time tx1.
データセット中の多くのトレーニング相互作用は、u1のテストインスタンス、すなわち時間tx1の後に発生した。
Then the model predicts u1’s test instance, with future training data that occurred after tx1.
そしてモデルは、tx1の後に発生した未来のトレーニングデータを使って、u1のテスト・インスタンスを予測する。
This is a data leakage issue discussed and evaluated in our earlier work [Ji et al.2023; Sun 2023].
これは、我々の以前の研究[Ji et al.2023; Sun 2023]で議論され、評価されたデータ漏洩の問題である。
The upper half of the figure illustrates an ideal online simulation using the same offline dataset.
図の上半分は、同じオフラインデータセットを使った理想的なオンラインシミュレーションを示している。
In this simulation, the model is trained/retrained periodically or is a retrieval model.
このシミュレーションでは、モデルは定期的に学習/再学習されるか、検索モデルである。
We assume that the model is lastly updated at time tm, which learns from all the interactions U × I that occurred before tm.
時刻tmにモデルが最後に更新され、tm以前に発生したすべての相互作用U×Iから学習されると仮定する。
We also assume that the test instance of u1 occurred right after the two preceding interactions, which form the Ic of u1.
また、u1のテスト・インスタンスは、u1のIcを形成する先行する2つの相互作用の直後に発生したと仮定する。
Then predicting u1’s test instance is through a model trained at tm, and tm < tx1 .
そして、u1のテスト・インスタンスの予測は、tmで学習されたモデルを通して行われ、tm < tx1 となる。
The model utilizes u1’s historical interactions Iu and her current session Ic to make the prediction.
モデルはu1の過去のインタラクションIuと彼女の現在のセッションIcを利用して予測を行う。
However, it is computationally expensive to strictly follow this online simulation to have a model retrained at every time point of every test instance.
しかし、このオンライン・シミュレーションを厳密に実行し、すべてのテスト・インスタンスのすべての時点でモデルを再学習させるには、計算コストがかかる。
A periodical model retraining with the timeline evaluation scheme could be a possible solution [Ji et al.2023; Sun 2023].
タイムライン評価スキームによる定期的なモデル再トレーニングは、可能な解決策である [Ji et al.2023; Sun 2023]。
Certainly, more research is required to discover the most effective evaluation schemes that best simulate the online setting for RecSys using offline datasets.
確かに、オフラインデータセットを用いてRecSysのオンライン設定を最もよくシミュレートする最も効果的な評価スキームを発見するためには、さらなる研究が必要である。

In our earlier work [Yu and Sun 2023], we argue that it is not merely the problem definition in its formal form, but the dataset and training, define the task that a model aims to solve.
我々の先行研究[Yu and Sun 2023]では、単に形式的な問題定義だけでなく、データセットとトレーニングによって、モデルが解決しようとするタスクが定義されると論じている。
Put simply, the way a dataset is used defines what information is made available to a model under training.
簡単に言えば、データセットの使われ方によって、学習中のモデルがどのような情報を利用できるかが決まる。
To my understanding, with the common practice in RecSys academic research, a model’s prediction relies on the general preferences it has learned from a user, while the user’s decision-making process takes into account both her general preferences and her current interests during the current interaction session.
私の理解では、RecSysの学術研究における一般的な慣行では、モデルの予測はユーザーから学習した一般的な嗜好に依存し、ユーザーの意思決定プロセスでは、現在の対話セッション中の一般的な嗜好と現在の興味の両方が考慮される。
Yet, the impact of contextual factors varies across recommendation scenarios.
しかし、文脈的要因の影響は推薦シナリオによって異なる。
Without providing the relevant contextual information, the model learned from these datasets will face a completely different setting when deployed online.
関連するコンテキスト情報を提供しなければ、これらのデータセットから学習したモデルは、オンラインで展開されたときにまったく異なる設定に直面することになる。
Due to the inadequacy of many existing datasets to capture the essential input for users’ decision-making processes, the application of collaborative filtering in predicting users’ general and enduring preferences appears to be the main focus of academic research.
既存の多くのデータセットでは、ユーザーの意思決定プロセスに不可欠なインプットを捉えることができないため、ユーザーの一般的かつ永続的な嗜好を予測するための協調フィルタリングの応用が、学術研究の主な焦点となっているようだ。
This could be a possible reason for the significant diverge between RecSys in academic research and RecSys in industry.
これは、学術研究におけるRecSysと産業界におけるRecSysが大きく乖離している理由である可能性がある。
On the positive side, there is a promising trend in the availability of RecSys datasets containing more information e.g., impressions, than simply user-item interactions [Wu et al.2020; Perez Maurera et al.2022].
肯定的な面では、RecSysのデータセットには、単にユーザーとアイテムのインタラクションだけでなく、インプレッションなど、より多くの情報が含まれているため、有望な傾向がある[Wu et al.2020; Perez Maurera et al.2022]。

# 6. Conclusion 結論

In this paper, we revisit RecSys task formulation from a user perspective, highlighting two main messages.
本稿では、ユーザーの視点からRecSysタスクの定式化を再検討し、2つの主要なメッセージを強調する。
Firstly, we emphasize that RecSys tasks are inherently applicationspecific, as factors influencing user decision-making vary across different scenarios.
まず、ユーザーの意思決定に影響を与える要因はシナリオによって異なるため、RecSysタスクは本質的にアプリケーションに特化したものであることを強調する。
Thus, it is imperative to study application-specific recommendation tasks rather than treating all recommendation tasks as simple missing value prediction problems in user-item interaction matrices.
したがって、すべての推薦タスクをユーザーとアイテムの相互作用行列における単純な欠損値予測問題として扱うのではなく、アプリケーションに特化した推薦タスクを研究することが不可欠である。
Secondly, we view recommender systems in a dynamic setting.
第二に、我々はレコメンダーシステムをダイナミックな設定で捉えている。
While collaborative filtering effectively learns general user preferences, it fails to capture dynamics in the decision-making process.
協調フィルタリングは、一般的なユーザーの嗜好を効果的に学習する一方で、意思決定プロセスにおけるダイナミクスを捉えることができない。
Therefore, a balanced approach considering both aspects leads us to conceptualize RecSys as a ranking problem.
したがって、両方の側面を考慮したバランスの取れたアプローチにより、RecSysをランキング問題として概念化することになる。
With a clearer understanding of the RecSys problem, it is hopeful that more datasets containing necessary details will become available for various recommendation scenarios.
RecSysの問題をより明確に理解することで、様々な推薦シナリオに必要な詳細を含むデータセットがより多く利用可能になることが期待される。
Furthermore, a more refined task formulation will directly impact the design of effective evaluations.
さらに、より洗練されたタスクの定式化は、効果的な評価の設計に直接影響する。
Again, all points discussed in this opinion paper are not new.
繰り返しになるが、この意見書で論じられている点はすべて目新しいものではない。
These points should have already been well considered in practical RecSys applications for long, and some points extensively discussed in earlier literature [Castells and Moffat 2022] .
これらの点は、実用的なRecSysのアプリケーションでは以前からよく考慮されていたはずであり、以前の文献[Castells and Moffat 2022]で広く議論されている点もある。
However, due to the relatively large number of publications from academia, researchers who are new to RecSys may not have well considered these contexts and simply follow the common practice.
しかし、アカデミアからの出版物が比較的多いため、RecSysを始めたばかりの研究者は、これらの文脈をよく考慮せず、単に一般的な慣例に従っている可能性がある。
As a research field closely tied to real-world applications, it is imperative for us to clearly define research tasks tailored to specific recommendation scenarios, rather than relying on generic and oversimplified settings.
実世界での応用と密接に結びついた研究分野である以上、一般的で単純化されすぎた設定に頼るのではなく、特定の推薦シナリオに合わせた研究課題を明確に定義することが不可欠である。
This is particularly important when considering new RecSys settings like convostational recommendation, and sequential recommendation, as well as when we bring in new technologies to RecSys like large language models.
これは、対話型推薦や逐次推薦のような新しいRecSysの設定を検討するときや、大規模言語モデルのような新しい技術をRecSysに導入するときに特に重要である。
Formulating tasks specific to scenarios would also significantly aid in selecting compatible baselines and establishing evaluation settings that best simulate practical conditions.
シナリオに特化したタスクを策定することは、適合するベースラインを選択し、実用的な条件を最もよくシミュレートする評価設定を確立する上でも、大きな助けとなるだろう。
Lastly, the definition of scenario-specific tasks heavily depends on the availability of high-quality datasets from real-world platforms.
最後に、シナリオ固有のタスクの定義は、実世界のプラットフォームから高品質のデータセットを入手できるかどうかに大きく依存する。
