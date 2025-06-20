https://cloud.google.com/blog/products/ai-machine-learning/glance-gaming-recommendation-at-scale-with-google-cloud-ai?hl=en

# How Glance is collaborating with Google to build a next-level recommendation engine for its gaming platform, Nostra
# GlanceがGoogleと協力して、ゲームプラットフォームNostraの次世代推薦エンジンを構築する方法

##### Paul Duff
Consultant, Data Sciences, Glance, Nostra, InMobi  
##### Gopala Dhar
AI Engineering Lead, Google Cloud Consulting  

Mobile gaming has exploded in popularity in recent years, with billions of people around the world playing games on their smartphones and tablets.  
モバイルゲームは近年、世界中で数十億人がスマートフォンやタブレットでゲームをプレイするようになり、人気が急増しています。  
Glance, a subsidiary of InMobi, is one of the world’s largest lock screen platforms with over 220 million active users.  
GlanceはInMobiの子会社であり、2億2000万人以上のアクティブユーザーを持つ世界最大のロック画面プラットフォームの1つです。
Redefining the way people use their mobile phone lock screen, over 400 million smartphones now come enabled with Glance’s next-generation internet experience.  
人々がモバイルフォンのロック画面を使用する方法を再定義し、4億台以上のスマートフォンがGlanceの次世代インターネット体験に対応しています。  
Glance aims to increase user adoption of Nostra, their mobile gaming platform, by providing personalized game recommendations to users.  
Glanceは、ユーザーにパーソナライズされたゲーム推薦を提供することで、モバイルゲームプラットフォームNostraのユーザー採用を増加させることを目指しています。  
Nostra currently has a few hundred games, with over 75 million monthly active users and a rapidly-growing user base.  
Nostraは現在、数百のゲームを提供しており、7500万人以上の月間アクティブユーザーと急速に成長しているユーザーベースを持っています。  

Glance and Nostra had an urgent need to recommend and personalize the games displayed on the user's lock screen, in order to improve the overall user experience.  
GlanceとNostraは、全体的なユーザー体験を向上させるために、**ユーザーのロック画面に表示されるゲームを推薦し、パーソナライズする緊急のニーズ**がありました。  
They turned to Google Cloud to build recommendation systems to personalize their gaming content according to the user's preferences.  
彼らは、ユーザーの好みに応じてゲームコンテンツをパーソナライズするための推薦システムを構築するためにGoogle Cloudに頼りました。  

Let’s take a deep dive into the recommendation system and the various Google AI technologies that were implemented to build the solution.  
推薦システムと、ソリューションを構築するために実装されたさまざまなGoogle AI技術について詳しく見ていきましょう。  

<!-- ここまで読んだ -->

### The historical dataset 歴史的データセット

Historical interactions on Glance that users had voluntarily provided, compliant with privacy guidelines, produced the following datasets:
ユーザーが自発的に提供したGlance上の歴史的なインタラクションは、プライバシーガイドラインに準拠して、以下のデータセットを生成しました：

- User metadata: Information on the user, such as the unique user ID, the handset details, and the manufacturer details.
ユーザメタデータ：ユニークなユーザーID、ハンドセットの詳細、製造元の詳細など、ユーザーに関する情報。

- Game metadata: Information regarding the games, such as their name, version, description, and unique game ID. The dataset also contained secondary information, such as which regions the game was released in and the game’s category and subcategory.
ゲームメタデータ：ゲームに関する情報、例えばその名前、バージョン、説明、ユニークなゲームIDなど。このデータセットには、ゲームがリリースされた地域やゲームのカテゴリおよびサブカテゴリなどの二次情報も含まれていました。

- User-Game interaction data: Interaction data, i.e. data capturing the unique user ID, the unique game ID, the interaction start time, the duration of interaction, and the game version.
ユーザー-ゲームインタラクションデータ：インタラクションデータ、すなわちユニークなユーザーID、ユニークなゲームID、インタラクション開始時間、インタラクションの持続時間、ゲームバージョンをキャプチャするデータ。

These were the primary data sources used further for analysis, experimentation, and ultimately modeling. 
これらは、さらなる分析、実験、そして最終的なモデル化に使用された主要なデータソースでした。
These datasets were partitioned by time, and in the spirit of experimentation, we considered a data chunk of 30 days for the solution approach.
これらのデータセットは時間によって分割され、実験の精神に則り、解決策アプローチのために30日間のデータチャンクを考慮しました。

<!-- ここまで読んだ -->

### Identifying data trends データトレンドの特定

We observed the plots of session duration vs. the number of events. 
私たちは、セッションの持続時間とイベントの数のプロットを観察しました。 
From those, we decided to remove user interaction events that were less than two seconds long, as these events were likely unintentional or accidental. 
**そこから、2秒未満のユーザーインタラクションイベントを削除することに決めました。これらのイベントは意図しないものであるか、偶発的である可能性が高いため**です。

Another interesting trend we observed was that the majority of the sessions occurred at night, followed by events that occurred after midnight. 
私たちが観察したもう一つの興味深いトレンドは、セッションの大多数が夜に発生し、その後に真夜中以降のイベントが続いたことです。 

We also observed that some games had a relatively higher median session interaction duration compared to other games, which was expected. 
また、いくつかのゲームは他のゲームと比較して相対的に高い中央値のセッションインタラクション持続時間を持っていることが観察されましたが、これは予想されていたことです。

<!-- ここまで読んだ -->

### Dealing with the outliers 外れ値の処理

For the given interaction dataset, the observed value of the session duration varied across the board. 
与えられたインタラクションデータセットでは、セッションの持続時間の観測値が全体にわたって異なりました。
Consequently, we observed outliers on both ends of the session duration spectrum. 
その結果、**セッションの持続時間のスペクトルの両端に外れ値が観察されました**。

As mentioned earlier, the minimum possible session duration was capped at two seconds, and any lower values were discarded. 
前述のように、最小のセッション持続時間は2秒に制限され、それより低い値は破棄されました。
Through mathematical analysis, we also affixed a certain maximum session duration to be the representative value for a single session interaction; any value higher than this was considered spurious. 
**数学的分析を通じて、単一のセッションインタラクションの代表値として特定の最大セッション持続時間を設定**しました。この値を超えるものはすべて虚偽と見なされました。

<!-- ここまで読んだ -->

### Splitting the data データの分割

We used 30 days' worth of data, but to fairly and accurately access the recommendation system, we needed to fix the data split methodology.  
私たちは30日分のデータを使用しましたが、推薦システムに公平かつ正確にアクセスするためには、データ分割の方法論を固定する必要がありました。

We considered several approaches, including the following:  
いくつかのアプローチを検討しました。以下の通りです。

1. Random split in 80/10/10 fashion. This might lead the model to preemptively learn trends from the future and ultimately cause data leakage.  
   1. 80/10/10の方法でのランダム分割。これはモデルが未来のトレンドを事前に学習し、最終的にデータ漏洩を引き起こす可能性があります。

2. Split stratified based on unique games/users. This would lead to the cold-start problem with a collaborative filtering approach.  
   2. ユニークなゲーム/ユーザーに基づいて層別分割。これは協調フィルタリングアプローチにおいてコールドスタート問題を引き起こすことになります。

3. Split based on a “last one out” strategy, which would imply we consider only (N-1) games with which the user interacted, keeping the last game for the test set. This would cause data leakage across the temporal dimension.  
   3. 「最後の一つを残す」戦略に基づく分割。これは、ユーザーが相互作用した(N-1)のゲームのみを考慮し、最後のゲームをテストセットに保持することを意味します。これにより、時間的次元でのデータ漏洩が発生します。

4. Data split stratified over N weeks, as we did explore some weekly trends. Hence, the first N weeks can be considered as a training set, and subsequent sets can be for testing and validation. This split type is also known as global-temporal-split.  
   4. N週間にわたって層別されたデータ分割。私たちはいくつかの週次トレンドを探求しました。したがって、最初のN週間はトレーニングセットと見なすことができ、その後のセットはテストと検証に使用できます。この分割タイプはグローバル・テンポラル・スプリットとしても知られています。

Since the number of games was less than the number of users, we considered all the games across sets, i.e., all N games should be considered that have at least *one* user interaction per each set train/test/validation (or at least three user interactions in total).  
ゲームの数がユーザーの数よりも少なかったため、私たちはすべてのセットにわたるすべてのゲームを考慮しました。つまり、各セットのトレーニング/テスト/検証に対して少なくとも*1*回のユーザーの相互作用があるすべてのNゲームを考慮する必要があります（または合計で少なくとも3回のユーザーの相互作用）。

We chose the fourth approach, global temporal split, where we first ordered the data chronologically, then defined the split interval and created the train, test, and evaluation splits. This way, we could avoid temporal data leakage and ensure that the trends were being captured properly across all users.  
私たちは4番目のアプローチ、グローバル・テンポラル・スプリットを選択しました。まずデータを時系列で順序付け、その後分割間隔を定義し、トレーニング、テスト、評価の分割を作成しました。この方法により、時間的データ漏洩を回避し、すべてのユーザーにわたってトレンドが適切に捉えられることを保証できました。

<!-- ここまで読んだ -->

### Preprocessing the data データの前処理

The next logical step was to scale the values. 
次の論理的なステップは、値をスケーリングすることでした。
However, due to the non-normal nature of the distribution, we could not perform any normalization, so we thus went with the approach of median centering over the aggregated duration. 
しかし、分布の非正規性のため、正規化を行うことができなかったため、**集約された期間に対する中央値中心化のアプローチを採用**しました。

The aggregated duration was calculated by summing the total interaction time between a unique user-game pair across all sessions, per split set, so each set had train, test, and evaluation. 
集約された期間は、すべてのセッションにわたるユニークなユーザ-ゲームペア間の総インタラクション時間を合計することによって計算され、各分割セットにはトレーニング、テスト、および評価が含まれていました。

In this approach, we selected the median sum of the duration of the training distribution and used it within a formula to scale the values down. 
このアプローチでは、トレーニング分布の期間の中央値の合計を選択し、それを使用して値をスケーリングダウンするための式に組み込みました。
Scaling the values ensured that the model we trained would be able to converge swiftly; it also ensured that all values that were lesser than the median were transformed as negative numbers and that all values above the median were transformed as positive numbers. 
**値をスケーリングすることで、私たちが訓練したモデルが迅速に収束できることが保証されました**。また、中央値より小さいすべての値が負の数に変換され、中央値より大きいすべての値が正の数に変換されることも保証されました。

<!-- ここまで読んだ -->

### Experimentation and modeling approaches 実験とモデリングアプローチ

We experimented deep and wide to find the best-fit solution for this use case. 
私たちは、このユースケースに最適なソリューションを見つけるために、深く広く実験を行いました。 
The experiments that we conducted included methods such as matrix factorization, two tower modeling through Vertex AI and TFRS implementation, and reinforcement learning. 
私たちが実施した実験には、行列分解、Vertex AIを通じた二塔モデル化、TFRSの実装、強化学習などの方法が含まれています。

#### Matrix factorization through BQML BQMLを通じた行列分解

Matrix factorization is a class of collaborative filtering algorithms used in recommender systems. 
行列分解は、推薦システムで使用される協調フィルタリングアルゴリズムの一種です。 
Matrix factorization algorithms work by decomposing the user-item interaction matrix into the product of two lower-dimensionality rectangular matrices. 
行列分解アルゴリズムは、ユーザー-アイテム相互作用行列を2つの低次元の長方形行列の積に分解することによって機能します。 
BQML offers matrix factorization out of the box. 
BQMLは、すぐに使用できる行列分解を提供します。 
This model only requires us to write SQL scripts to create a model and start training the same. 
このモデルは、モデルを作成し、トレーニングを開始するためにSQLスクリプトを書く必要があるだけです。 
BQML implements the WALS algorithm to decompose the user-item interaction matrix. 
BQMLは、ユーザー-アイテム相互作用行列を分解するためにWALSアルゴリズムを実装しています。 

This was the baseline model that was created and trained, and the feature we considered was the aggregate session duration for each user-game interaction. 
これは作成され、トレーニングされたベースラインモデルであり、私たちが考慮した特徴は、各ユーザー-ゲーム相互作用の合計セッション時間でした。 
This model performed quite well, and after hyper-parameter tuning, it was the model with the best scores for test and evaluation sets. 
このモデルは非常に良好なパフォーマンスを示し、ハイパーパラメータの調整後、テストおよび評価セットで最高のスコアを持つモデルとなりました。 
The following diagram describes the flow of data in the BigQuery pipeline: 
以下の図は、BigQueryパイプラインにおけるデータの流れを示しています。

#### Two Tower Embedding Algorithm with Vertex AI matching engine Vertex AIマッチングエンジンを使用した二塔埋め込みアルゴリズム
This is an embedding-based approach to build the recommendation system. 
これは、推薦システムを構築するための埋め込みベースのアプローチです。 
The two-tower approach is a ranking model that uses a query tower and a candidate tower to generate embeddings of the query and its related candidate passed on to their respective towers. 
二塔アプローチは、クエリタワーと候補タワーを使用して、クエリとその関連候補の埋め込みを生成するランキングモデルです。 
The generated embeddings are then represented in a vector embedding space. 
生成された埋め込みは、ベクトル埋め込み空間で表現されます。 

Embedding-based models use the user and the item context to create a well-informed embedding in a shared vector space. 
埋め込みベースのモデルは、ユーザーとアイテムのコンテキストを使用して、共有ベクトル空間で十分に情報を得た埋め込みを作成します。 
In our experimentation approach, we considered numerous combinations of user features and game features to construct the embeddings. 
私たちの実験アプローチでは、埋め込みを構築するためにユーザー特徴とゲーム特徴の多数の組み合わせを考慮しました。 
The best results were observed when the game embeddings included the category and the user embeddings included the temporal features, such as the day of the week and the time of the day. 
**ゲームの埋め込みにカテゴリが含まれ、ユーザーの埋め込みに曜日や時間などの時間的特徴が含まれているときに、最良の結果が観察されました**。 

After these embeddings were created, we created a Vertex AI Matching Engine Index. 
これらの埋め込みが作成された後、私たちはVertex AIマッチングエンジンインデックスを作成しました。 
Vertex AI Matching Engine provides the industry's leading high-scale low latency vector database (a.k.a, vector similarity-matching or approximate nearest neighbor service).
Vertex AIマッチングエンジンは、業界で最も優れた高スケール低遅延ベクトルデータベース（別名、ベクトル類似性マッチングまたは近似最近傍サービス）を提供します。 
More specifically, given the query item, Matching Engine finds the most semantically similar items from a large corpus of candidate items. 
より具体的には、クエリアイテムが与えられると、マッチングエンジンは大量の候補アイテムから最も意味的に類似したアイテムを見つけます。 

Utilizing this, we created indexes for Bruteforce search and Approximate Nearest Neighbour Search. 
これを利用して、私たちはブルートフォース検索と近似最近傍検索のためのインデックスを作成しました。 
Then, we performed a series of experimentations with various distance metrics, including dot product, cosine similarity, etc. 
次に、ドット積、コサイン類似度など、さまざまな距離メトリックを使用して一連の実験を行いました。 
The results from these experimentations concluded that we may require additional modeling and additional contextual data to make the embedding model perform better. 
これらの実験の結果、埋め込みモデルのパフォーマンスを向上させるためには、追加のモデリングと追加のコンテキストデータが必要である可能性があることが結論付けられました。

#### Custom modeling with TFRS TFRSを使用したカスタムモデリング

TensorFlow Recommenders (TFRS) is a library for building recommender system models. 
TensorFlow Recommenders（TFRS）は、推薦システムモデルを構築するためのライブラリです。 
It is built on top of TensorFlow and streamlines the process of building, training, and deploying recommender systems. 
これはTensorFlowの上に構築されており、推薦システムの構築、トレーニング、および展開のプロセスを簡素化します。 

The TFRS retrieval model built for this approach was composed of two sub-models viz, a query model (UserModel) computing the query representation using query features, and a candidate model (GameModel) computing the candidate representation using the candidate features. 
このアプローチのために構築されたTFRSリトリーバルモデルは、クエリ特徴を使用してクエリ表現を計算するクエリモデル（UserModel）と、候補特徴を使用して候補表現を計算する候補モデル（GameModel）の2つのサブモデルで構成されていました。 
The outputs of the two models were used to give a query-candidate affinity score, with higher scores expressing a better match between the candidate and the query. 
2つのモデルの出力は、クエリ-候補親和度スコアを提供するために使用され、高いスコアは候補とクエリの間のより良い一致を表します。 
Similar to the Vertex AI Two Tower approach, we conducted multiple experiments defining various user features and game features to create the embeddings, and created Indexes on Vertex AI Matching Engine. 
Vertex AIの二塔アプローチと同様に、私たちは埋め込みを作成するためにさまざまなユーザー特徴とゲーム特徴を定義する複数の実験を行い、Vertex AIマッチングエンジンにインデックスを作成しました。 

Best results and generalization was observed when only the user features were considered and the no game feature was considered, so only the unique game ID was used as a reference to embed the unique games in the vector space. 
**ユーザー特徴のみが考慮され、ゲーム特徴が考慮されなかった場合に、最良の結果と一般化が観察されました。そのため、ユニークなゲームIDのみが、ベクトル空間にユニークなゲームを埋め込むための参照として使用されました**。(ん?? それだとコールドスタートアイテム問題に対応できなくない?? オフライン評価で過剰評価されてるのではって思っちゃうな...!:thinking:) 
The index used for the analysis was a Brute Force one to recommend top K games. 
分析に使用されたインデックスは、トップKゲームを推奨するためのブルートフォースのものでした。 
We used Brute Force as the search space was limited. 
検索空間が限られていたため、ブルートフォースを使用しました。

#### Reinforcement learning through contextual bandits コンテキストバンディットを通じた強化学習

We implemented a multi-armed contextual bandit algorithm implemented through tf-agents. 
私たちは、tf-agentsを通じて実装されたマルチアームコンテキストバンディットアルゴリズムを実装しました。
Multi-Armed Bandit (MAB) is a machine learning framework in which an agent has to select actions (arms) to maximize its cumulative reward in the long term. 
マルチアームバンディット（MAB）は、エージェントが長期的に累積報酬を最大化するためにアクション（アーム）を選択しなければならない機械学習フレームワークです。 
In each round, the agent receives some information about the current state (context), and then it chooses an action based on this information and the experience gathered in previous rounds. 
各ラウンドで、エージェントは現在の状態（コンテキスト）に関する情報を受け取り、その情報と前のラウンドで得た経験に基づいてアクションを選択します。 
At the end of each round, the agent receives the reward associated with the chosen action. 
各ラウンドの終わりに、エージェントは選択したアクションに関連する報酬を受け取ります。 

In this approach, we utilize the Multi-Armed Contextual Bandit (MACB) modeling, with per-arm features, i.e. the learning agent has the option to choose games from one of the "arms" having their respective features. 
このアプローチでは、**各アームの特徴を持つ**マルチアームコンテキストバンディット（MACB）モデリングを利用します。つまり、学習エージェントはそれぞれの特徴を持つ「アーム」の1つからゲームを選択するオプションがあります。 
This helps in generalization as the user and the game context are embedded through a neural network. 
これにより、ユーザーとゲームのコンテキストがニューラルネットワークを通じて埋め込まれるため、一般化が助けられます。

In the methodology, the context was derived from the BQML matrix factorization model. 
この方法論では、コンテキストはBQML行列分解モデルから導出されました。 
We used an epsilon Greedy agent with a prespecified exploration factor, which ensured that the model is capable of learning trends as well as exploring beyond. 
私たちは、**事前に指定された探索係数を持つイプシロングリーディエージェントを使用し、モデルがトレンドを学習し、さらに探索する能力を持つことを保証しました**。 
This model gave surprisingly good results, considering that it was only trained on a subset of 1 million unique users. 
**このモデルは、100万人のユニークユーザーのサブセットでのみトレーニングされたことを考慮すると、驚くほど良い結果を出しました。**(お〜いいね。探索と継続的学習の成果って感じだ...!:smile:)

The model gained exceptional generalizability from the limited training samples and was able to understand and map out the context space for a total of 19 million unique users. 
このモデルは、**限られたトレーニングサンプルから優れた一般化能力を得て**、1900万人のユニークユーザーのコンテキスト空間を理解し、マッピングすることができました。
(ここで限られたトレーニングサンプルって、オフライン学習なのかな?? もしくは、ロールアウトやA/Bテスト的に、アクティブユーザのサブセットに対して稼働させてオンライン学習させた可能性もあるかも...!:thinking:)
(なるほどな〜。toC向けのアプリだったら、もしオフライン学習が精度悪かったとしても、**社内ユーザにだけ先に展開して報酬を観測して、オンライン学習しながら精度向上を図ることもできるかも...!** 社内ユーザが相当他のアクティブユーザと行動パターンが異なってない限りは、全体適用前にモデルの学習を進められるのでは...!!:thinking:)

This model was one of the top performers throughout this engagement, wherein it aimed at optimizing model metrics like the Sub-Optimal Arms Metrics and the Regret Metric.
このモデルは、この取り組み全体で最高のパフォーマンスを発揮し、サブオプティマルアームメトリックや後悔メトリックなどのモデルメトリックの最適化を目指しました。 
For experimentation of MACB we followed the following approach: 
MACBの実験のために、私たちは以下のアプローチに従いました：

![]()

(たぶん図を見た感じだと、ユーザ側のcontext feature + アイテム側のarm featureを使ったMLモデル + epsilon greedyなアクション選択をしてる感じっぽい??:thinking:)

<!-- ここまで読んだ -->

### Experimentation metrics 実験指標

In all of these experimentations we calculated four metrics:
これらの実験では、4つの指標を計算しました：

- Mean Average Precision at K (MAP)
- Normalized Discounted Cumulative Gain at K (NDCG)
- Average Rank
- Mean Squared Error

The "K" here represents the number of results to be recommended.
ここでの「K」は、推奨される結果の数を表します。 
We experimented with values of K being 5, 10 and All.
Kの値として5、10、Allを使用して実験を行いました。

These metrics were used to rank models across different modeling methodologies.
これらの指標は、異なるモデリング手法におけるモデルの順位付けに使用されました。
However, out of these four metrics, we mainly focused on comparing the MAP and NDCG values, as they do a better job of representing the problem statement at hand.
しかし、これらの4つの指標の中で、主にMAPとNDCGの値を比較することに焦点を当てました。これらは、現在の問題ステートメントをより適切に表現するからです。

<!-- ここまで読んだ -->

### Results and observations 結果と観察

With our best model, we observed a significant performance improvement compared to the baseline model used previously. 
私たちの最良のモデルを使用した結果、以前に使用されたベースラインモデルと比較して、パフォーマンスが大幅に改善されたことを観察しました。
The BQML Matrix Factorization model was the best performer, followed by the Contextual Bandits model, VertexAI Two Tower, and finally the TFRS approach. 
**BQML行列分解モデルが最も優れたパフォーマンスを示し、その後にコンテキストバンディットモデル、VertexAI Two Tower、最後にTFRSアプローチが続きました**。(どうしてもオフライン評価でCFの手法が過剰評価されてそうに感じてしまう...??:thinking:)
The embedding-based models suffered because of the lack of certain user demographic features in the given dataset. 
埋め込みベースのモデルは、与えられたデータセットに特定のユーザの人口統計的特徴が欠けていたため、苦しみました。
We also observed that as the K value increased, the model performance also increased, which is expected behavior. 
また、K値が増加するにつれてモデルのパフォーマンスも向上することが観察され、これは予想される挙動です。

Explaining the productionization and scaling approach of these models, the Nostra team initially deployed new models on a small percentage of traffic, comparing engagement metrics with control traffic in an A/B testing fashion. 
これらのモデルの生産化とスケーリングアプローチを説明すると、Nostraチームは**最初に新しいモデルをトラフィックの小さな割合で展開し、A/Bテスト方式でコントロールトラフィックとエンゲージメントメトリクスを比較しました**。(ロールアウト戦略ってやつか...!:thinking:)
This deployment was tuned to ensure low latency output and to gain a deeper understanding of the key drivers behind user engagement. 
この展開は、低遅延出力を確保し、ユーザエンゲージメントの背後にある主要な要因をより深く理解するために調整されました。
Once the model showed good performance, Nostra was positioned for further cost optimisations if required, and to scale the model to a larger percentage of traffic.
モデルが良好なパフォーマンスを示すと、Nostraは必要に応じてさらなるコスト最適化を行い、モデルをより大きな割合のトラフィックにスケールする準備が整いました。

After this engagement, the Nostra team decided to implement the BQML Matrix Factorization model in production, after which they observed a preliminary increase in the time spent by the users interacting with the games on their platform. 
このエンゲージメントの後、**NostraチームはBQML行列分解モデルを本番環境に実装することを決定し**、その後、ユーザがプラットフォーム上のゲームと対話する際に費やす時間が初期的に増加したことを観察しました。(あれ?? CFモデルを?? 後でepsilon-greedyを採用したってことかな??)

### Fast track end-to-end deployment with Google Cloud AI Services (AIS) 

The partnership between Google Cloud and Glance is just one of the latest examples of how we’re providing AI-powered solutions to solve complex problems to help organizations drive the desired outcomes. 
Google CloudとGlanceのパートナーシップは、私たちが複雑な問題を解決するためにAI駆動のソリューションを提供し、組織が望ましい成果を達成する手助けをしている最新の例の一つです。 
To learn more about Google Cloud’s AI services, visit our AI & ML Products page. 
Google CloudのAIサービスについて詳しく知りたい方は、私たちのAI & ML製品ページをご覧ください。

Paul Duff, Consultant - Data Sciences with Nostra emphasized how happy he is with Cloud AIS and out-of-the-box products like BQML that helped get to productionable models in just a few weeks, stating, “The Google team was able to exceed our agreed objective to develop an offline recommendation system for Nostra, completing all milestones on or before time and delivering four fully documented working models. 
NostraのデータサイエンスコンサルタントであるPaul Duffは、Cloud AISやBQMLのような既製品に非常に満足していることを強調し、数週間で生産可能なモデルに到達するのを助けたと述べています。「Googleチームは、Nostraのオフライン推薦システムを開発するという合意された目標を超えることができ、すべてのマイルストーンを時間通りまたはそれ以前に完了し、4つの完全に文書化された作業モデルを提供しました。 
We were able to deploy the first of these in production (beyond the agreed project scope) and saw an uplift in our key metrics before the project end date. 
私たちは、これらのうちの最初のモデルを（合意されたプロジェクトの範囲を超えて）生産に展開することができ、プロジェクトの終了日より前に主要な指標の向上を見ました。 
The organization of the team was exemplary with excellent communication throughout.” 
チームの組織は模範的で、全体を通して優れたコミュニケーションがありました。」

<!-- ここまで読んだ -->
