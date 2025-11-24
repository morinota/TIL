refs: https://www.onepeloton.com/press/articles/lessons-learned-from-building-context-aware-recommender-systems

# Lessons Learned from Building out Context-Aware Recommender Systems コンテキスト対応レコメンダーシステムの構築から得た教訓

Written by Shoya Yoshida, Arnab Bhadury, Neel Talukder, Shayak Banerjee, Alexey Zankevich and Vijay Pappu
August 24, 2022

![]()

In our previous post, we described the LSTMNet, the model the Personalization team at Peloton chose as our first foray into building machine learning-based recommender systems for our platforms’ home screens. 
前回の投稿では、Pelotonのパーソナライズチームがプラットフォームのホーム画面向けに機械学習ベースのレコメンダーシステムを構築するための最初の試みとして選んだモデルLSTMNetについて説明しました。
The LSTMNet was an appropriate choice, as data stores were still in their early stages and fragmented, making it hard to use a wide variety of different features. 
LSTMNetは適切な選択でした。なぜなら、データストアはまだ初期段階で断片化しており、さまざまな異なる特徴を使用するのが難しかったからです。
As a result, the LSTMNet that simply learned from sequences of workouts was suitable, in addition to the natural correspondence of the model’s sequential nature and the serial nature of fitness. 
その結果、ワークアウトのシーケンスから単純に学習するLSTMNetは適しており、モデルのシーケンシャルな性質とフィットネスの連続的な性質との自然な対応もありました。
We also detailed the drawbacks of using the LSTMNet, such as the lack of contextual relevance and its inability to handle cold, or new, items and users. 
また、LSTMNetを使用する際の欠点、例えばコンテキストの関連性の欠如や、新しいアイテムやユーザーに対応できないことについても詳述しました。

<!-- ここまで読んだ! -->

In this post, we lay out how we have been building out Context-Aware Recommender Systems (CARS) to iterate on the LSTMNet. 
この投稿では、LSTMNetを反復するために、どのようにコンテキスト対応レコメンダーシステム（CARS）を構築してきたかを説明します。
We will first motivate the need to be context-aware when making recommendations, then dive deep into the lessons we have learned along the way, and finally wrap up with what is planned for ahead. 
まず、**推薦を行う際にコンテキストを意識する必要性**を説明し、その後、私たちが学んできた教訓について詳しく掘り下げ、最後に今後の計画についてまとめます。

<!-- ここまで読んだ! -->

## UNDERSTANDING THE IMPORTANCE OF CONTEXT FOR FITNESS フィットネスにおける文脈の重要性の理解

Fitness is a journey that is unique to each individual with an infinite possibilities of paths. 
フィットネスは、無限の可能性を持つ各個人に特有の旅です。
At Peloton, each class is characterized by different themes, music, fitness disciplines, and teaching styles of our world-class instructors, who range anywhere from soothingly tranquil to inspiringly cheerful. 
Pelotonでは、各クラスは異なるテーマ、音楽、フィットネスの分野、そして穏やかで落ち着いたスタイルから、刺激的で陽気なスタイルまでの世界的なインストラクターの指導スタイルによって特徴付けられています。
Needless to say, user behavior and preferences vary wildly and evolve over time, and it may even change from one context to another even for the same user. 
言うまでもなく、**ユーザーの行動や好みは大きく異なり、時間とともに進化し、同じユーザーであっても文脈によって変わることがあります**。

For example, one user may opt to take our flagship live cycling classes with energetic music on Friday nights on the Peloton Bike, while choosing to take our yoga classes in the morning and meditation classes at night using the mobile app on other days.
例えば、あるユーザーは、金曜日の夜にPeloton Bikeでエネルギッシュな音楽のライブサイクリングクラスを選択する一方で、他の日には朝にヨガクラス、夜にモバイルアプリを使用して瞑想クラスを受講することを選ぶかもしれません。
Another user may not have the Peloton Bike, but instead stream multiple strength classes from their smart TV in the living room and afterwards go outside to follow our guided outdoors run class using the Peloton App. 
別のユーザーはPeloton Bikeを持っていないかもしれませんが、代わりにリビングのスマートTVから複数の筋力トレーニングクラスをストリーミングし、その後外に出てPeloton Appを使用してガイド付きの屋外ランクラスに参加するかもしれません。

With so many types of different workouts available, users must make many small decisions to choose their workouts of the day. 
さまざまな種類のワークアウトが利用可能であるため、ユーザーはその日のワークアウトを選ぶために多くの小さな決定を下さなければなりません。
Peloton’s internal User Research team conducted a study and identified five key decision factors that users face when choosing a class. 
Pelotonの内部ユーザーリサーチチームは調査を行い、ユーザーがクラスを選択する際に直面する5つの重要な決定要因を特定しました。
The factors are time, instructor, class type, mood, and recent state; they are all interrelated with one another as shown in the figure below. 
その要因は、時間、インストラクター、クラスの種類、気分、最近の状態であり、これらはすべて以下の図に示すように相互に関連しています。

![]()

### Time 時間

Time can be broken down into two interdependent aspects. 
**時間は、二つの相互依存的な側面に分解することができます。**
One aspect of time is the duration that the user is willing to workout, and the other aspect is the time of the day, week, or year when the user is making this decision. 
時間の一つの側面は、ユーザがトレーニングを行うことに対してどれだけの時間をかける意欲があるかということです。そして、もう一つの側面は、ユーザがこの決定を下す日、週、または年の時間です。
Some users may log in looking to do a 30 minute workout because that may be the only time they have available right then. 
一部のユーザは、その時に利用可能な唯一の時間が30分のトレーニングであるため、そのトレーニングを行うためにログインするかもしれません。
However, the situation could vary on a weekday morning before commuting or the decision may be different if it was on a Saturday afternoon during the holiday season instead. 
しかし、状況は通勤前の平日朝では異なる可能性があり、また、ホリデーシーズンの土曜日の午後であれば決定も異なるかもしれません。
Time can frequently be an unnegotiable decision factor. 
時間はしばしば交渉不可能な決定要因となることがあります。

<!-- ここまで読んだ! -->

### Instructor 講師

As mentioned previously, we have a wide variety of world-class instructors with diverse backgrounds and teaching styles. 
前述のように、私たちは多様なバックグラウンドと教授スタイルを持つ世界クラスの講師を幅広く揃えています。
Most of our users have certain favorite instructors that they will take the bulk of the classes with.
私たちのユーザーのほとんどは、主に特定の好きな講師のクラスを受講します。
Depending on their mood, some users may opt to take classes with Cody Rigsby to get some words of affirmation, or opt to take a class with Olivia Amato, an instructor known to lead very challenging workouts, if in a daring mood. 
気分によっては、Cody Rigsbyのクラスを受けて励ましの言葉をもらったり、挑戦的なワークアウトを指導することで知られるOlivia Amatoのクラスを受けたりするユーザーもいます。

<!-- ここまで読んだ! -->

### Class Type クラスの種類

With diverse instructors comes diverse classes on various platforms. 
多様なインストラクターがいることで、さまざまなプラットフォームで多様なクラスが提供されます。 
To run through the numbers, we have three platforms (Peloton Bike and Bike+, Peloton Tread, and digital, which includes the Peloton App and the recently released Peloton Guide), over 50 instructors, 10+ fitness disciplines, and dozens of different series within each fitness discipline. 
数字を見てみると、私たちは3つのプラットフォーム（Peloton BikeおよびBike+、Peloton Tread、そしてPeloton Appや最近リリースされたPeloton Guideを含むデジタル）を持ち、50人以上のインストラクター、10以上のフィットネス分野、そして各フィットネス分野内に数十の異なるシリーズがあります。 
In addition, each class at Peloton has its own curated music playlist to fit the style of the class. 
さらに、Pelotonの各クラスには、そのクラスのスタイルに合ったキュレーションされた音楽プレイリストがあります。 
Our library of content is diverse enough to fill almost every class type imaginable. 
私たちのコンテンツライブラリは、想像できるほぼすべてのクラスの種類を満たすのに十分な多様性があります。 
From Jess Sim’s “Flash 15” strength workout series that could make you sore in 15 minutes to Dance Cardio to Meditation content with your favorite instructors, our library has something for everyone. 
Jess Simの「Flash 15」筋力トレーニングシリーズ（15分で筋肉痛になる可能性があります）からダンスカーディオ、そしてお気に入りのインストラクターによる瞑想コンテンツまで、私たちのライブラリには誰にでも合うものがあります。

<!-- ここまで読んだ! -->

### Mood 気分

Mood can affect what kind of vibe one may seek out in a class. 
気分は、クラスでどのような雰囲気を求めるかに影響を与える可能性があります。 
Perhaps, it is early Monday morning and one feels the need to reach a sense of calmness and thus opts to take some yoga or stretch classes. 
おそらく、月曜日の早朝で、落ち着きを求める必要があると感じ、そのためにヨガやストレッチのクラスを選ぶでしょう。 
Conversely, one may be in a bright mood on a Friday night and opt to take a Groove cycling class to jam out to your favorite music. 
逆に、金曜日の夜に明るい気分であれば、お気に入りの音楽に合わせて楽しむためにグルーヴサイクリングのクラスを選ぶかもしれません。

<!-- ここまで読んだ! -->

### Recent State 最近の状態

A user’s recent state surrounding last completed workouts is also important. 
**ユーザーの最近の状態、特に最後に完了したワークアウトに関する情報も重要**です。
If one has already taken a lower body strength class and a core exercise class recently, one would likely gravitate towards taking an upper body workout to balance out the muscles used. 
もし誰かが最近、下半身の筋力トレーニングクラスとコアエクササイズクラスを受講していた場合、使用した筋肉のバランスを取るために上半身のワークアウトを受けたくなるでしょう。
Within the same workout session, if one just finished a long cycling class, one would want to take a nice 10 minute lower-body stretch class. 
同じワークアウトセッション内で、もし誰かが長時間のサイクリングクラスを終えたばかりであれば、心地よい10分間の下半身ストレッチクラスを受けたいと思うでしょう。
There are also more external aspects, such as when a user may be injured, and the user must opt to take easier classes than they are normally used to. 
また、ユーザーが怪我をしている場合など、外的な要因もあり、ユーザーは通常受けているクラスよりも簡単なクラスを選択しなければならないこともあります。

All in all, in the realm of fitness, choosing the appropriate class is highly dependent on the real time context of a user. 
要するに、フィットネスの領域において、適切なクラスを選択することは**ユーザーのリアルタイムのコンテキストに大きく依存**しています。
Consequently, an ideal recommender system at Peloton must be context-aware and be able to dynamically adjust to diverse settings a user may be in. 
したがって、Pelotonにおける理想的なレコメンダーシステムはコンテキストを認識し、ユーザーがいる多様な環境に動的に適応できる必要があります。

(こういうコンテキスト的な特徴量って、Feature Storeに保存する、とかではなさそうだよなぁ...:thinking:)
<!-- ここまで読んだ! -->

## THE LIMITATIONS OF LSTMNET LSTMNetの限界

As explained in the previous blog post, the LSTMNet represents each user with the sequence of classes that the user has been taking. 
前回のブログ記事で説明したように、LSTMNetは各ユーザをそのユーザが受講しているクラスのシーケンスで表現します。 
This representation of the user is then compared with the embedding for a specific class to come up with a recommendation score for this user-class pair.
このユーザの表現は、特定のクラスの埋め込みと比較され、このユーザ-クラスペアの推薦スコアが算出されます。

One major limitation of LSTMNet is that it cannot use any contextual information to influence the recommendations. 
**LSTMNetの大きな制限の一つは、推薦に影響を与えるための文脈情報を使用できないこと**です。(つまりid-onlyな手法ってことね...!:thinking:)
For example, regardless of if the user logs in during the early hours of the morning or late in the night, the LSTMNet cannot adapt to these contextual changes because the context is not even an input to the model.
例えば、ユーザが朝早くにログインするか夜遅くにログインするかに関わらず、LSTMNetはこれらの文脈の変化に適応できません。なぜなら、文脈はモデルへの入力ですらないからです。

Another major drawback is the cold start problem for new classes. 
もう一つの大きな欠点は、新しいクラスに対するコールドスタート問題です。(これもid-onlyな手法の宿命的な問題点だよなぁ...!:thinking:)
At Peloton, we release dozens of new classes every day. 
Pelotonでは、毎日数十の新しいクラスをリリースしています。
Since the LSTMNet must learn a separate embedding for each class, this forces us to re-train this model every day with the newest classes in the training data.
LSTMNetは各クラスのために別々の埋め込みを学習しなければならないため、これは私たちに毎日最新のクラスをトレーニングデータに加えてこのモデルを再トレーニングすることを強いることになります。 
The cold start problem for new users is a similar problem; without any workout history, the LSTMNet has no information about the user to compute a recommendation.
新しいユーザに対するコールドスタート問題も同様の問題です。ワークアウト履歴がないため、LSTMNetは推薦を計算するためのユーザに関する情報を持っていません。
(結局のところ行列分解をベースに深層学習モデルで近似してるだけだから、id-onlyな手法はやっぱりこうなるよなぁ...:thinking:)

To address these issues, instead of relying on the model to implicitly capture a black-box representation for each user and class, we would ideally like the model to create representations for each user and class using explicit features and context, as visualized below.
これらの問題に対処するために、私たちはモデルが各ユーザとクラスのために暗黙的にブラックボックス表現をキャプチャすることに依存するのではなく、**理想的にはモデルが明示的な特徴と文脈を使用して各ユーザとクラスの表現を作成することを望んでいます。**以下に示すように。

![]()

<!-- ここまで読んだ! -->

## HOW CONTEXT-AWARE RECOMMENDER MODELS WORK コンテキスト対応推薦モデルの動作

Context-Aware Recommender models are a suite of Click-Through Rate (CTR) models that can flexibly accept any kinds of inputs such as explicit features and user context, no matter if they are continuous or categorical.
コンテキスト対応推薦モデルは、明示的な特徴やユーザコンテキストなど、連続的であろうとカテゴリカルであろうと、あらゆる種類の入力を柔軟に受け入れることができるクリック率（CTR）モデルの一群です。(CTR予測モデル、って言い切っちゃってるのは個人的にどうかと思う...!:thinking:)
Specifically, after experimentation, we decided to use DLRM, a deep learning recommendation model open-sourced by Facebook in 2019. 
具体的には、実験の結果、私たちは2019年に**Facebookによってオープンソース化された深層学習推薦モデルであるDLRM**を使用することに決めました。
As visualized below, DLRM accepts a user-item pair as an input and outputs the probability that the user interacts with the paired item. 
以下に示すように、**DLRMはユーザ-アイテムペアを入力として受け取り、ユーザがペアになったアイテムと相互作用する確率を出力**します。

![]()

Thus, the input features can largely be split into user information and item information, and within each group, it can be split into static and dynamic features. 
したがって、入力特徴は大きくユーザ情報とアイテム情報に分けることができ、各グループ内では**静的特徴と動的特徴**に分けることができます。 
Please see the table below for specific examples. 
具体的な例については、以下の表を参照してください。 

![]()

In this paradigm, we do not learn embeddings for each individual class in our library. 
このパラダイムでは、ライブラリ内の各個別クラスの埋め込みを学習しません。 
Instead, each class is represented by its metadata, so there is no need to retrain the model like in the case of the LSTMNet, as typically all the attributes of newly released classes have already been seen in existing classes. 
代わりに、各クラスはそのメタデータによって表されるため、通常、新しくリリースされたクラスのすべての属性は既存のクラスで既に見られているため、LSTMNetの場合のようにモデルを再訓練する必要はありません。(id-onlyな手法からの卒業ね...!:thinking:)
In addition, even for new users, the cold-start problem is mitigated compared to the LSTMNet, as the model can still infer some information from the static features of the users. 
**さらに、新しいユーザに対しても、モデルがユーザの静的特徴からいくつかの情報を推測できるため、LSTMNetと比較してコールドスタート問題が軽減されます**。 
Similarly, in “chilly” start settings where an existing Peloton Member onboards to a new platform, context-aware models will already have some idea of kinds of content the user prefers. 
同様に、既存のPelotonメンバーが新しいプラットフォームに参加する「寒冷」スタート設定では、コンテキスト対応モデルはユーザが好むコンテンツの種類についてすでにある程度のアイデアを持っています。
By making our recommender systems context-aware, we achieve one central system that will be able to handle all cohorts of users regardless of their current stages in their journey of fitness. 
私たちの推薦システムをコンテキスト対応にすることで、フィットネスの旅の現在の段階に関係なく、すべてのユーザコホートを処理できる中央システムを実現します。 

## SHIFT FROM BATCH PROCESSING TO ONLINE INFERENCE バッチ処理からオンライン推論への移行

One important observation to note about using real-time context, such as hour of the day, as an input to calculate recommendations is that the model must also make the predictions in real-time. 
**リアルタイムコンテキスト（例えば、時間帯）を入力として使用して推薦を計算する際の重要な観察点は、モデルもリアルタイムで予測を行う必要があるということ**です。(もしくは高頻度、例えばhourlyでバッチ推論する手もあるか。いやでも確かにリアルタイム推論にした方が効率的なのかな...!:thinking:)
However, currently our system generates recommendations via daily batch processing jobs, where recommendations for each user are generated and cached to be simply retrieved when a user logs in. 
**しかし、現在私たちのシステムは、各ユーザの推薦が生成され、キャッシュされて、ユーザがログインしたときに単純に取得される日次バッチ処理ジョブを介して推薦を生成**しています。(うんうん分かるよ...!:thinking:)
Therefore, in order to truly utilize context-aware models, we must transition through to online inference.
したがって、コンテキスト対応モデルを真に活用するためには、オンライン推論に移行する必要があります。 

<!-- ここまで読んだ! -->

This paradigm shift is far from trivial, and our team has decided to undertake this journey in two-stages.
**このパラダイムシフトは簡単なものではなく、私たちのチームはこの旅を二段階で進めることに決めました**。
We first develop a pipeline that trains and does batch inference with DLRM that has comparable performance as the LSTMNet. 
**まず、LSTMNetと同等のパフォーマンスを持つDLRMでバッチ推論を行うパイプラインを開発**します。
Then as the second stage, we would move the inference portion to online, where DLRM would then be augmented with real-time context features. 
**次の段階として、推論部分をオンラインに移行し、DLRMにリアルタイムコンテキスト機能を追加**します。
For more details on the tools used to build the system, here is a talk from our team at NVIDIA’s GTC 2020 conference. 
システム構築に使用されるツールの詳細については、NVIDIAのGTC 2020カンファレンスでの私たちのチームの講演をご覧ください。 
At this time, we have completed the first stage of this monumental change, and in doing so, we learned multiple major lessons on iterating on recommender systems. 
**現在、私たちはこの重要な変化の第一段階を完了**しており、その過程で推薦システムの反復に関するいくつかの重要な教訓を学びました。(あ、第二段階はまだ途中なんかい！:thinking:)

<!-- ここまで読んだ! -->

## WHERE THE RUBBER MET THE ROAD: LESSONS LEARNED どこでゴムが道路に接触したか：得られた教訓

- 補足:
  - 「where the rubber meets the road」は英語の慣用句で、「理論や計画が実際の行動や実践に移される瞬間」や「実際の状況で試される瞬間」を指す。

### Make Each End-to-End Iteration Quick as Possible 各エンドツーエンドの反復をできるだけ迅速に行う

Building machine learning models is all about trying out as many ideas as possible, as quickly as possible.  
**機械学習モデルの構築は、できるだけ多くのアイデアをできるだけ早く試すことに関するもの**です。
This is especially true when developing a context-aware model, since there are suddenly infinitely more knobs to tune.  
これは、コンテキスト対応モデルを開発する際に特に当てはまります。なぜなら、**調整すべきノブが無限に増えるから**です。 (確かに、id-onlyな手法に比べて自由度が格段に上がるから...!:thinking:)
We didn’t quite have this problem in the LSTMNet, since the only input is the workout history of users for that model.  
LSTMNetではこの問題はあまりありませんでした。なぜなら、そのモデルの唯一の入力はユーザのトレーニング履歴だからです。 
With context-aware models, we have the gift and the curse to explore infinitely more combinations of different features, feature preprocessing methods, as well as methods of generating positive and negative samples.  
**コンテキスト対応モデルでは、異なる特徴、特徴の前処理方法、ポジティブおよびネガティブサンプルを生成する方法の無限の組み合わせを探求するという贈り物と呪いがあります**。  
This project was one of the first major iterations on our machine learning pipeline, and we learned that it is absolutely crucial to make each end-to-end experimentation of an idea as quick as possible.  
このプロジェクトは、私たちの機械学習パイプラインにおける最初の主要な反復の一つであり、**アイデアの各エンドツーエンドの実験をできるだけ迅速に行うことが絶対に重要であること**を学びました。  

In the early days of the project, it took hours to go through the whole offline experimentation cycle of preparing the training data, preprocessing the data, training the model, and evaluating the model.  
プロジェクトの初期段階では、トレーニングデータの準備、データの前処理、モデルのトレーニング、モデルの評価という**オフライン実験サイクル全体を通過するのに数時間かかりました**。(うぇ〜い、かかってるね〜:thinking:) 
Quickly, we realized that we needed to make two changes: enable parallel experimentation and make each experiment quicker by downsampling the data.  
私たちはすぐに、2つの変更を行う必要があることに気付きました：**並列実験を可能にし、データをダウンサンプリングすることで各実験を迅速にすること**です。(並列実験は最初から可能にしてたな!:thinking:)

By enabling parallel experimentation, we could kick off multiple experiments concurrently with different setups and compare them side by side.
並列実験を可能にすることで、異なる設定で複数の実験を同時に開始し、それらを並べて比較することができました。 
On the downsampling front, one could downsample the number of users used for evaluation and the training data itself.  
ダウンサンプリングの観点からは、評価に使用するユーザの数とトレーニングデータ自体をダウンサンプリングすることができます。
One may be wary of downsampling both of these data, as evaluating on a subset of users may not give an accurate picture of the whole population, and training on a smaller dataset may hinder models, especially collaborative filtering models, from truly understanding user behaviors.  
これらのデータの両方をダウンサンプリングすることには注意が必要です。なぜなら、ユーザのサブセットで評価することは全体の人口の正確なイメージを与えない可能性があり、より小さなデータセットでトレーニングすることは、特に協調フィルタリングモデルがユーザの行動を真に理解するのを妨げる可能性があるからです。

However, after conducting some experiments, we found out that the evaluation metrics calculated using all the relevant users actually resulted in virtually the same numbers as when we only utilized 5% of randomly chosen users.  
しかし、いくつかの実験を行った結果、**関連するすべてのユーザを使用して計算した評価指標は、実際にはランダムに選ばれたユーザの5%のみを利用した場合とほぼ同じ数値になった**ことがわかりました。  
In addition, models trained on 10% of the data compared to the full dataset only suffered a small drop in offline evaluation metrics.  
**さらに、全データセットと比較して10%のデータでトレーニングされたモデルは、オフライン評価指標でわずかな低下しか見られませんでした**。(なるほど...!:thinking:)
Context-aware models are technically hybrid models, combining elements of both content and collaborative filtering, so that likely enabled the model to still perform decently well even with data from less users.  
**コンテキスト対応モデルは技術的にはハイブリッドモデルであり、コンテンツと協調フィルタリングの要素を組み合わせているため、ユーザが少ないデータでもモデルがそれなりに良いパフォーマンスを発揮できる可能性があります**。
With these changes, we were able to make the entire offline experimentation shorter by an order of magnitude.  
これらの変更により、私たちは全体のオフライン実験を桁違いに短縮することができました。  
We did, however, still run experiments on the full dataset from time to time during development to check scalability of new changes.  
**ただし、開発中は新しい変更のスケーラビリティを確認するために、時折フルデータセットで実験を行いました**。(そうだよね...!:thinking:)

<!-- ここまで読んだ! -->

### Invest in Evaluation 評価への投資

Evaluation is undoubtedly the most important aspect of any experiment. 
**評価は、間違いなくあらゆる実験において最も重要な側面**です。
Especially in earlier phases of development, it was very meaningful to actually qualitatively assess the output of the model for some real users – typically our teammates so we know their tastes – to sanity check. 
特に開発の初期段階では、実際のユーザ、通常は私たちのチームメイトのモデル出力を定性的に評価することが非常に意義深いものでした。彼らの好みを知っているため、妥当性を確認するためです。

In fact, qualitative evaluation has helped us uncover problems with our outputs that we wouldn’t have been able to observe with pure quantitative metrics. 
**実際、定性的評価は、純粋な定量的指標では観察できなかった出力の問題を明らかにするのに役立ちました**。
For example, our system generates different recommendations for each user for different platforms (i.e. Peloton Bike and Bike+, Peloton Tread, Peloton App, and more) because user behavior changes drastically across different platforms, even for the same user. 
例えば、私たちのシステムは、異なるプラットフォーム（すなわち、Peloton BikeとBike+、Peloton Tread、Peloton Appなど）に対して各ユーザに異なる推薦を生成します。これは、同じユーザであっても、異なるプラットフォーム間でユーザの行動が大きく変わるためです。
However, we saw that model output for one of our teammates on the Bike platform put too much weight on an instructor this person has taken non-cycling classes with on the Peloton App but usually avoids on the bike. 
しかし、Bikeプラットフォームでの私たちのチームメイトのモデル出力は、その人がPeloton Appで受講したことのあるインストラクターに過度に重みを置いていることがわかりましたが、通常は自転車では避けているものでした。
By detecting insights like this, we were able to more carefully craft some features to improve the recommendations. 
このような洞察を検出することで、私たちは推薦を改善するためにいくつかの特徴量をより慎重に設計することができました。

However, qualitative evaluation can be cumbersome and is not suitable for every iteration we were making. 
しかし、**定性的評価は手間がかかり、私たちが行っていたすべての反復に適しているわけではありま**せん。
So we did mainly rely on offline evaluation metrics, such as Mean Average Precision at K (MAP@K), especially after the initial phases of development. 
そのため、**私たちは主にオフライン評価指標、例えばKにおける平均適合率（MAP@K）に依存しました。特に開発の初期段階を過ぎてからはそうでした**。

However, it is a frequent problem in the industry that the offline evaluation metrics don’t always correlate to online performance, as confirmed by companies like Pinterest. 
しかし、オフライン評価指標がオンラインパフォーマンスと常に相関しないというのは、[Pinterest](https://medium.com/pinterest-engineering/experiment-without-the-wait-speeding-up-the-iteration-cycle-with-offline-replay-experimentation-7a4a95fa674b)のような企業によって確認されている業界の一般的な問題です。
To confirm if offline evaluation actually helps, we ran a couple multivariate tests where each variant purposefully had varying levels of MAP@K to compare what kind of offline performance each would achieve. 
オフライン評価が実際に役立つかどうかを確認するために、私たちはいくつかの**multivariateテスト**を実施しました。各バリアントは意図的に異なるMAP@Kのレベルを持ち、各々がどのようなオフラインパフォーマンスを達成するかを比較しました。
(これって結局variant分けてオンラインテストした、って話??:thinking:)
The idea is that if we could observe that models with higher offline metrics result in higher online metrics, we can confidently optimize for higher offline metrics during development. 
その考えは、オフライン指標が高いモデルがオンライン指標も高くなることを観察できれば、開発中にオフライン指標を高めるために自信を持って最適化できるというものです。
Specifically, by using this result, we were able to establish an offline-online metrics correlation chart, illustrated below, where each variant’s performance is plotted on a graph with the X-axis being the offline metric and Y-axis being the online metric. 
具体的には、この結果を使用することで、以下に示すオフライン-オンライン指標相関チャートを確立することができました。ここでは、各バリアントのパフォーマンスがグラフにプロットされており、X軸がオフライン指標、Y軸がオンライン指標です。

![]()

With this chart, we first gained some confidence that a higher offline metric does result in a higher online metric, and we also started to see the actual mathematical relationship between the two. 
このチャートを使って、私たちはまず、**より高いオフライン指標がより高いオンライン指標につながるという自信を得ました**。また、両者の実際の数学的関係も見え始めました。
Theoretically, if we had a perfectly fit offline-online correlation chart, then the life of best fit could approximate the expected lift in online metrics from the lift in the offline metrics. 
**理論的には、完璧にフィットしたオフライン-オンライン相関チャートがあれば、最適なフィットのライフはオフライン指標の向上からオンライン指標の期待される向上を近似できる**でしょう。
This means that we don’t always have to run an A/B test to confirm if we would get an uplift in online metrics, which would be beneficial as A/B tests take time. 
これは、オンライン指標の向上が得られるかどうかを確認するために常にA/Bテストを実施する必要がないことを意味します。A/Bテストには時間がかかるため、これは有益です。
While a perfect offline-online correlation chart never exists in practice, this chart effectively dictates how much confidence we could bestow to our offline metrics. 
**完璧なオフライン-オンライン相関チャートは実際には存在しません**が、このチャートは私たちがオフライン指標にどれだけの信頼を置けるかを効果的に示しています。

<!-- ここまで読んだ! -->

However, this technique had a couple of quirks. 
しかし、この手法にはいくつかの特異点がありました。
First, we found that our online metrics are not always stable, even if we have not made any changes from our side. 
まず、私たちは、こちら側で何も変更を加えていなくても、**オンライン指標が常に安定しているわけではないこと**を発見しました。
(まあvarianceだよね。オンライン評価が完全にground truthって訳じゃなくて、結局はこれも観測されたデータに基づいて真の値を推定してるだけなので。biasは0でもvarianceはある、って話...!:thinking:)
Our main online metric such as conversion on our recommended classes on the homescreen can vary depending on what else may be happening that week on our platforms. 
私たちの主なオンライン指標である、ホーム画面での推薦クラスのコンバージョンは、その週にプラットフォームで何が起こっているかによって変動する可能性があります。
For example, if there is a new type of workout class being released or some sort of a special event ongoing, it could sway users away from their usual habit of taking their recommended classes. 
例えば、新しいタイプのワークアウトクラスがリリースされたり、特別なイベントが進行中であったりすると、ユーザが推薦クラスを受講する通常の習慣から逸れる可能性があります。
At Peloton, running different multivariate tests to keep accumulating more data points for the offline-online correlation chart proved to be very unreliable due to the forever evolving landscape of our content. 
Pelotonでは、**オフライン-オンライン相関チャートのためにデータポイントを蓄積し続けるために異なる多変量テストを実施することは、コンテンツの常に進化する状況のために非常に信頼性が低いこと**が証明されました。(オンライン指標も当然ばらつきがあるから...!:thinking:)

Therefore, an offline-online correlation chart is a tool that can help you locate metrics to loosely trust, but it is still far from perfect. 
したがって、**オフライン-オンライン相関チャートは、信頼できる指標を見つけるのに役立つツールですが、まだ完璧には程遠いもの**です。(「完璧ではないが役に立つ」、ってことか...!:thinking:)
Consequently, our team is looking to develop more sophisticated offline evaluation techniques involving page simulation and replay to add to our arsenal of evaluation approaches. 
その結果、私たちのチームは、評価アプローチの武器を増やすために、[ページシミュレーションやリプレイ](https://netflixtechblog.com/page-simulator-fa02069fb269)を含むより洗練されたオフライン評価技術の開発を目指しています。

<!-- ここまで読んだ! -->

### Invest in Experiment Tracking Tools 実験追跡ツールへの投資

We log and store all the metrics as well as model artifacts from every step of the training and evaluation pipelines in MLFLow. 
私たちは、MLFLowのトレーニングおよび評価パイプラインの各ステップから、すべてのメトリックとモデルアーティファクトを記録し、保存します。
This includes metrics like size of training data, the ratio of positive to negative examples, used features, various evaluation metrics, as well as of course the trained model files.
これには、トレーニングデータのサイズ、正例と負例の比率、使用された特徴、さまざまな評価メトリック、そしてもちろんトレーニングされたモデルファイルが含まれます。
However, with so many experiments running in parallel, it could quickly get messy and you could lose track of which run corresponds to the intended changes. 
しかし、並行して多くの実験が行われると、すぐに混乱し、どの実行が意図した変更に対応しているのかを見失う可能性があります。
As a result, we plan on investing further into our infrastructure around MLFlow and experiment tracking in general to ease some of the manual experiment tracking that one has to do. 
その結果、私たちはMLFlowおよび一般的な実験追跡に関するインフラにさらに投資し、手動で行わなければならない実験追跡の一部を軽減することを計画しています。

<!-- ここまで読んだ! -->

### Better Infrastructure Reliability for Better DevEx より良いインフラストラクチャの信頼性がより良い開発者体験をもたらす

(まあAttentionとか使ってないならGPUはそこまでなくても良いのかもしれんけど...:thinking:)

We rely on AWS to spin up GPU pods with Kubernetes to run our model training and evaluation jobs. 
私たちは、モデルのトレーニングと評価ジョブを実行するために、Kubernetesを使用してAWSでGPUポッドを立ち上げることに依存しています。
However, due to the ongoing global chip shortage, there were some periods when our jobs could not even be spun up. 
しかし、進行中の世界的なチップ不足のため、私たちのジョブを立ち上げることができない期間がありました。
This hindered developer experience, and we temporarily improved the situation by purchasing reserved instances from AWS. 
これにより開発者体験が妨げられ、私たちは一時的にAWSからリザーブドインスタンスを購入することで状況を改善しました。
Furthermore, by downsampling the data, we were able to reduce the number of GPUs our jobs needed to iterate during development, which also ameliorated the issue. 
さらに、**データをダウンサンプリングすることで、開発中に私たちのジョブが必要とするGPUの数を減らすことができ**、これも問題を改善しました。
Our team continues to work closely with other teams to make the developer experience better from an infrastructure standpoint. 
私たちのチームは、インフラの観点から開発者体験を向上させるために、他のチームと密接に協力し続けています。

## BRINGING CARS FULL THROTTLE: WHAT’S PLANNED FOR AHEAD 車をフルスロットルに: 今後の計画

As we shift gears into the next stage of building out our fully context-aware recommender systems by moving inference to online, there are also other exciting things that we plan on doing with CARs.
私たちが推論をオンラインに移行することによって、完全にコンテキストを意識したレコメンダーシステムの構築の次の段階に移行する中で、CARsに関して計画している他のエキサイティングなこともあります。

### Generating Contextual Rows of Content コンテキストに基づくコンテンツの行の生成

(Rows of content = 特定のテーマに基づくコンテンツのリスト、例えば横カルーセルで表示されるようなやつ...!:thinking:)

CARS can be used to expand the variety of rows of content we show on our homescreen.
CARSは、私たちのホームスクリーンに表示するコンテンツの行の多様性を拡大するために使用できます。
By leveraging the time context, we could create new rows such as “Start your Morning With…” or “End your Day With…” that are filled with content the user may particularly like at those specific times of the day. 
**時間のコンテキストを活用することで、「朝を始めるには…」や「一日を終えるには…」のような新しい行を作成でき、これらは特定の時間にユーザが特に好むコンテンツで満たされます**。(時間のcontext特徴量を元に、コンテンツ編成を作れるのか...!:thinking:)
Other types of possible rows of content may include rows like “To Recover from Yesterday’s 60 Minute Workout…” or “If you are in a Bubbly Mood.” 
他の可能なコンテンツの行のタイプには、「昨日の60分のワークアウトから回復するために…」や「気分が高揚している場合は…」のような行が含まれるかもしれません。

<!-- ここまで読んだ! -->

### Multi-headed Predictions マルチヘッド予測

Earlier, we explained that the inputs to the context-aware models are very flexible. 
以前、私たちはコンテキスト対応モデルへの入力が非常に柔軟であることを説明しました。
The same thing can be said about the outputs of these types of models as well. 
これらのタイプのモデルの出力についても同じことが言えます。
Traditional CTR models only have one “head,” which predicts if the user will click on the item or not. 
従来のCTRモデルは、ユーザーがアイテムをクリックするかどうかを予測する「ヘッド」が1つだけです。
However, we can modify these models to have multiple heads, where each head predicts something different, thereby making our model learn multiple tasks at once. 
**しかし、これらのモデルを修正して複数のヘッドを持たせることができ、各ヘッドが異なるものを予測することで、モデルが同時に複数のタスクを学習できるようにします**。
(分かるんだけど、これはTwo-tower型のアーキテクチャだと不可能ではないけどやや扱いづらいかなぁ...タスクの数だけ埋め込みが作られるってことだと思うので...!:thinking:)
(あ、いや、でもそれでもいいのかも?? 用途ごとに使う埋め込みを使い分ければよいし、効果的な知識共有・伝搬ができると思えば...! 上流モデル&下流モデルって分ける必要もないのか:thinking:)
At Peloton, most of our classes play multiple songs, which the user can explicitly like during the workout.
Pelotonでは、ほとんどのクラスで複数の曲が再生され、ユーザはワークアウト中に明示的にその曲を気に入ることができます。
By using this data, we can add a head to predict if a user will like the music in the class or not, which would let us make music-based recommendations.
このデータを使用することで、ユーザーがクラスの音楽を気に入るかどうかを予測するヘッドを追加でき、音楽に基づく推薦を行うことができます。
We will also explore the possibilities of adding other heads to predict other actions, such as bookmarking or sharing to others. 
**また、ブックマークや他者への共有など、他のアクションを予測するための他のヘッドを追加する可能性も探ります。**
With multi-headed predictions, we will be able to create different shelves of content to add to our home screen and beyond. 
マルチヘッド予測を使用することで、ホーム画面やそれ以外の場所に追加するための異なるコンテンツの棚を作成できるようになります。

<!-- ここまで読んだ! --> 

### CONCLUSION 結論

We hope that the learnings shared in this blog could help inform any other teams looking to build out context-aware recommender systems. 
私たちは、このブログで共有された学びが、コンテキスト対応のレコメンダーシステムを構築しようとしている他のチームに役立つことを願っています。
We have an exciting roadmap ahead as we keep tackling the very rewarding and unique challenges we face at the intersection of recommender systems and fitness.
私たちは、レコメンダーシステムとフィットネスの交差点で直面する非常にやりがいのあるユニークな課題に取り組み続ける中で、エキサイティングなロードマップを持っています。
If you or anyone you know are interested in working with us, please visit our careers page and join the ride! 
もしあなたやあなたの知り合いが私たちと一緒に働くことに興味があるなら、ぜひ私たちのキャリアページを訪れて、共に旅を始めましょう！

<!-- ここまで読んだ! -->
