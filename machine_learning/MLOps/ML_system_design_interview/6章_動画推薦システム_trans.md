refs: https://bytebytego.com/courses/machine-learning-system-design-interview/video-recommendation-system


Unlock Full Access with 50% off 50%オフでフルアクセスを解除
Login ログイン



## Machine Learning System Design Interview
## 機械学習システム設計インタビュー

- 01Introduction and Overview
- 01イントロダクションと概要
- 02Visual Search System
- 02ビジュアル検索システム
- 03Google Street View Blurring System
- 03Googleストリートビューぼかしシステム
- 04YouTube Video Search
- 04YouTubeビデオ検索
- 05Harmful Content Detection
- 05有害コンテンツ検出
- 06Video Recommendation System
- 06ビデオ推薦システム
- 07Event Recommendation System
- 07イベント推薦システム
- 08Ad Click Prediction on Social Platforms
- 08ソーシャルプラットフォームにおける広告クリック予測
- 09Similar Listings on Vacation Rental Platforms
- 09バケーションレンタルプラットフォームにおける類似リスティング
- 10Personalized News Feed
- 10パーソナライズされたニュースフィード
- 11People You May Know
- 11あなたが知っているかもしれない人々

# Video Recommendation System 動画推薦システム

Recommendation systems play a key role in video and music streaming services. 
推薦システムは、動画や音楽ストリーミングサービスにおいて重要な役割を果たします。 
For example, YouTube recommends videos a user may like, Netflix recommends movies a user may enjoy watching, and Spotify recommends music to users. 
例えば、YouTubeはユーザーが好む可能性のある動画を推薦し、Netflixはユーザーが楽しむ可能性のある映画を推薦し、Spotifyはユーザーに音楽を推薦します。 

In this chapter, we design a video recommendation system similar to YouTube's [1]. 
この章では、YouTubeのものに似た動画推薦システムを設計します。 
The system recommends videos on the user's homepage based on their profile, previous interactions, etc. 
このシステムは、ユーザーのプロフィールや過去のインタラクションなどに基づいて、ユーザーのホームページに動画を推薦します。 

![]()

Recommendation systems are often very complex in design, and a good amount of engineering effort is required to develop an efficient and scalable system. 
**推薦システムはしばしば非常に複雑な設計を持ち、効率的でスケーラブルなシステムを開発するには相当なエンジニアリングの努力が必要**です。 
Don't worry, though; no one expects you to build the perfect system in a 45-minute interview. 
しかし心配しないでください。誰もが45分の面接で完璧なシステムを構築することを期待しているわけではありません。 
The interviewer is primarily interested in observing your thought process, communication skills, ability to design ML systems, and ability to discuss trade-offs. 
面接官は主にあなたの思考過程、コミュニケーションスキル、MLシステムを設計する能力、そしてトレードオフについて議論する能力を観察することに興味を持っています。 

<!-- ここまで読んだ! -->

### Clarifying Requirements 要件の明確化

Here is a typical interaction between a candidate and an interviewer.
ここでは、候補者と面接官の典型的なやり取りを示します。

Candidate: Can I assume the business objective of building a video recommendation system is to increase user engagement?
候補者: **動画推薦システムを構築するビジネスの目的は、ユーザーのエンゲージメントを高めること**だと仮定してもよいですか？
Interview: That’s correct.
面接官: その通りです。

Candidate: Does the system recommend similar videos to a video a user is watching right now? Or does it show a personalized list of videos on the user’s homepage?
候補者: システムは、ユーザーが現在視聴している動画に類似した動画を推薦しますか？それとも、ユーザーのホームページにパーソナライズされた動画のリストを表示しますか？
Interviewer: This is a homepage video recommendation system, which recommends personalized videos to users when they load the homepage.
面接官: これはホームページ動画推薦システムであり、ユーザーがホームページを読み込むときにパーソナライズされた動画を推薦します。

Candidate: Since YouTube is a global service, can I assume users are located worldwide and videos are in different languages?
候補者: YouTubeはグローバルなサービスなので、ユーザーは世界中にいて、動画は異なる言語であると仮定してもよいですか？
Interviewer: That’s a fair assumption.
面接官: それは妥当な仮定です。

Candidate: Can I assume we can construct the dataset based on user interactions with video content?
候補者: ユーザーの動画コンテンツとのインタラクションに基づいてデータセットを構築できると仮定してもよいですか？
Interviewer: Yes, that sounds good.
面接官: はい、それは良い考えです。

Candidate: Can a user group videos together by creating playlists? Playlists can be informative for the ML model during the learning phase.
候補者: ユーザーはプレイリストを作成することで動画をグループ化できますか？プレイリストは、学習フェーズ中のMLモデルにとって有益です。
Interviewer: For the sake of simplicity, let’s assume the playlist feature does not exist.
面接官: 簡単のために、プレイリスト機能は存在しないと仮定しましょう。

Candidate: How many videos are available on the platform?
候補者: プラットフォーム上にはどれくらいの動画がありますか？
Interviewer: We have about 10 billion videos.
面接官: 約100億本の動画があります。
<!-- 候補アイテム多いな! アイテムidのカーディナリティも多い...! -->

Candidate: How fast should the system recommend videos to a user? Can I assume the recommendation should not take more than 200 milliseconds?
候補者: システムはユーザーにどれくらいの速さで動画を推薦すべきですか？**推薦は200ミリ秒以上かかってはいけない**と仮定してもよいですか？
Interviewer: That sounds good.
面接官: それは良い考えです。

Let’s summarize the problem statement. 
問題の要約をしましょう。
We are asked to design a homepage video recommendation system. 
私たちは、ホームページ動画推薦システムを設計するよう求められています。
The business objective is to increase user engagement. 
ビジネスの目的は、ユーザーのエンゲージメントを高めることです。
Each time a user loads the homepage, the system recommends the most engaging videos. 
ユーザーがホームページを読み込むたびに、システムは最もエンゲージメントの高い動画を推薦します。
Users are located worldwide, and videos can be in different languages. 
ユーザーは世界中におり、動画は異なる言語である可能性があります。
There are approximately 10 billion videos on the platform, and recommendations should be served quickly.
プラットフォーム上には約100億本の動画があり、推薦は迅速に提供されるべきです。

<!-- ここまで読んだ! -->

### Frame the Problem as an ML Task 機械学習タスクとして問題を定義する 

#### Defining the ML objective 機械学習の目的を定義する

The business objective of the system is to increase user engagement.  
システムのビジネス目的は、ユーザのエンゲージメントを高めることです。  
There are several options available for translating business objectives into well-defined ML objectives.  
**ビジネス目的を明確に定義された機械学習の目的に変換**するためのいくつかの選択肢があります。  
We will examine some of them and discuss their trade-offs.  
私たちはそれらのいくつかを検討し、そのトレードオフについて議論します。  

**Maximize the number of user clicks**.  
ユーザのクリック数を最大化する。
A video recommendation system can be designed to maximize user clicks.  
動画推薦システムは、ユーザのクリック数を最大化するように設計できます。  
However, this objective has one major drawback.  
しかし、この目的には大きな欠点があります。  
The model may recommend videos that are so-called "clickbait", meaning the title and thumbnail image look compelling, but the video's content may be boring, irrelevant, or even misleading.  
モデルは、いわゆる「クリックベイト」と呼ばれる動画を推薦する可能性があり、タイトルやサムネイル画像は魅力的に見えますが、動画の内容は退屈であったり、無関係であったり、さらには誤解を招くものである可能性があります。  
Clickbait videos reduce user satisfaction and engagement over time.  
**クリックベイト動画は、時間が経つにつれてユーザの満足度とエンゲージメントを低下させます**。  

**Maximize the number of completed videos.**  
完了した動画の数を最大化する。  
The system could also recommend videos users will likely watch to completion.
システムは、ユーザが最後まで視聴する可能性の高い動画を推薦することもできます。  
A major problem with this objective is that the model may recommend shorter videos that are quicker to watch.  
この目的の大きな問題は、モデルが視聴が早い短い動画を推薦する可能性があることです。  

**Maximize total watch time.**  
総視聴時間を最大化する。  
This objective produces recommendations that users spend more time watching.  
この目的は、ユーザがより多くの時間を視聴する推薦を生み出します。  

**Maximize the number of relevant videos.**  
関連する(=i.e. positive feedbackする)動画の数を最大化する。
This objective produces recommendations that are relevant to users.  
この目的は、ユーザに関連する推薦を生み出します。  
Engineers or product managers can define relevance based on some rules.  
エンジニアやプロダクトマネージャーは、いくつかのルールに基づいて関連性を定義できます。  
Such rules can be based on implicit and explicit user reactions.  
そのようなルールは、暗黙的および明示的なユーザの反応に基づくことができます。  
For example, one definition could state a video is relevant if a user explicitly presses the "like" button or watches at least half of it.  
例えば、**ある定義では、ユーザが「いいね」ボタンを明示的に押すか、少なくとも半分以上視聴した場合、その動画は関連性があるとされる**ことがあります。  
Once we define relevance, we can construct a dataset and train a model to predict the relevance score between a user and a video.  
関連性を定義すると、データセットを構築し、ユーザと動画の間の関連性スコアを予測するモデルを訓練できます。

In this system, we choose the final objective as the ML objective because we have more control over what signals to use.  
このシステムでは、使用する信号をより制御できるため、最終的な目的を機械学習の目的として選択します。
In addition, it does not have the shortcomings of the other options described earlier.
さらに、前述の他の選択肢の欠点を持っていません。  

<!-- ここまで読んだ! -->

#### Specifying the system’s input and output システムの入力と出力の指定

As Figure 6.2 shows, a video recommendation system takes a user as input and outputs a ranked list of videos sorted by their relevance scores.
図6.2が示すように、ビデオ推薦システムはユーザを入力として受け取り、関連スコアによってソートされたビデオのランキングリストを出力します。

#### Choosing the right ML category 適切なMLカテゴリの選択

In this section, we examine three common types of personalized recommendation systems. 
このセクションでは、3つの一般的なパーソナライズド推薦システムのタイプを検討します。

- Content-based filtering
- Collaborative filtering
- Hybrid filtering

Let’s examine each type in more detail. 
それぞれのタイプをより詳しく見ていきましょう。



##### Content-based filtering コンテンツベースのフィルタリング

This technique uses video features to recommend new videos similar to those a user found relevant in the past. 
この技術は、ユーザが過去に関連性を見出した動画に似た新しい動画を推薦するために、動画の特徴を使用します。

For example, if a user previously engaged with many ski videos, this method will suggest more ski videos. 
例えば、ユーザが過去に多くのスキー動画に関与していた場合、この方法はさらに多くのスキー動画を提案します。

Figure 6.4 shows an example. 
図6.4は一例を示しています。

Here is an explanation of the diagram. 
以下は図の説明です。

1. User A engaged with videos $X$ and $Y$ in the past 
1. ユーザAは過去に動画$X$と$Y$に関与しました。

2. Video $Z$ is similar to video $X$ and video $Y$ 
2. 動画$Z$は動画$X$と動画$Y$に似ています。

3. The system recommends video $Z$ to user A 
3. システムは動画$Z$をユーザAに推薦します。

Content-based filtering has pros and cons. 
コンテンツベースのフィルタリングには利点と欠点があります。

Pros: 
利点：

- Ability to recommend new videos. 
- 新しい動画を推薦する能力。

With this method, we don't need to wait for interaction data from users to build video profiles for new videos. 
この方法では、新しい動画のためにユーザからのインタラクションデータを待つ必要はありません。

The video profile depends entirely upon its features. 
動画のプロファイルは、その特徴に完全に依存します。

- Ability to capture the unique interests of users. 
- ユーザの独自の興味を捉える能力。

This is because we recommend videos based on users' previous engagements. 
これは、ユーザの過去の関与に基づいて動画を推薦するためです。

Cons: 
欠点：

- Difficult to discover a user's new interests. 
- ユーザの新しい興味を発見するのが難しい。

- The method requires domain knowledge. 
- この方法は専門知識を必要とします。

We often need to engineer video features manually. 
私たちはしばしば動画の特徴を手動で設計する必要があります。



##### Collaborative filtering (CF) 協調フィルタリング (CF)

CF uses user-user similarities (user-based CF) or video-video similarities (item-based CF) to recommend new videos. 
CFは、ユーザー間の類似性（ユーザー基盤CF）または動画間の類似性（アイテム基盤CF）を使用して新しい動画を推薦します。 
CF works with the intuitive idea that similar users are interested in similar videos. 
CFは、類似したユーザーが類似した動画に興味を持つという直感的な考え方に基づいています。 
You can see a user-based CF example in Figure 6.5. 
ユーザー基盤CFの例は図6.5に示されています。 

Let's explain the diagram. 
この図を説明しましょう。 
The goal is to recommend a new video to user A. 
目標は、ユーザーAに新しい動画を推薦することです。 

1. Find a similar user to A based on their previous interactions; say user B 
   1. ユーザーAの過去のインタラクションに基づいて、類似のユーザーを見つけます。例えば、ユーザーBとします。 
2. Find a video that user B engaged with but which user A has not seen yet; say video Z 
   2. ユーザーBが関与したが、ユーザーAがまだ見ていない動画を見つけます。例えば、動画Zとします。 
3. Recommend video Z to user A 
   3. 動画ZをユーザーAに推薦します。 

A  
A  
A  
A  
A  
B  
B  
B  
B  
B  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
Z  
A  
A  
A  
A  
A  

A major difference between content-based filtering and CF filtering is that CF filtering does not use video features and relies exclusively upon users' historical interactions to make recommendations. 
コンテンツベースのフィルタリングとCFフィルタリングの大きな違いは、CFフィルタリングが動画の特徴を使用せず、ユーザーの過去のインタラクションのみに依存して推薦を行うことです。 
Let's see the pros and cons of CF filtering. 
CFフィルタリングの利点と欠点を見てみましょう。 

Pros: 
利点: 
- No domain knowledge needed. 
  - ドメイン知識は不要です。 
  - CF does not rely on video features, which means no domain knowledge is needed to engineer features from videos. 
  - CFは動画の特徴に依存しないため、動画から特徴を設計するためのドメイン知識は必要ありません。 
- Easy to discover users' new areas of interest. 
  - ユーザーの新しい興味の領域を発見しやすいです。 
  - The system can recommend videos about new topics that other similar users engaged with in the past. 
  - システムは、他の類似ユーザーが過去に関与した新しいトピックに関する動画を推薦できます。 
- Efficient. 
  - 効率的です。 
  - Models based on CF are usually faster and less compute-intensive than content-based filtering, as they do not rely on video features. 
  - CFに基づくモデルは、動画の特徴に依存しないため、通常、コンテンツベースのフィルタリングよりも速く、計算負荷が少ないです。 

Cons: 
欠点: 
- Cold-start problem. 
  - コールドスタート問題です。 
  - This refers to a situation when limited data is available for a new video or user, meaning the system cannot make accurate recommendations. 
  - これは、新しい動画やユーザーに対して利用可能なデータが限られている状況を指し、システムが正確な推薦を行えないことを意味します。 
  - CF suffers from a cold-start problem due to the lack of historical interaction data for new users or videos. 
  - CFは、新しいユーザーや動画の過去のインタラクションデータが不足しているため、コールドスタート問題に悩まされます。 
  - This lack of interactions prevents CF from finding similar users or videos. 
  - このインタラクションの欠如は、CFが類似のユーザーや動画を見つけるのを妨げます。 
  - We will discuss later in the serving section how our system handles the cold-start problem. 
  - 後の提供セクションで、私たちのシステムがコールドスタート問題をどのように処理するかについて説明します。 
- Cannot handle niche interests. 
  - ニッチな興味に対応できません。 
  - It's difficult for CF to handle users with specialized or niche interests. 
  - CFは、専門的またはニッチな興味を持つユーザーに対応するのが難しいです。 
  - CF relies upon similar users to make recommendations, and it might be difficult to find similar users with niche interests. 
  - CFは、推薦を行うために類似のユーザーに依存しており、ニッチな興味を持つ類似のユーザーを見つけるのが難しいかもしれません。 

Table 6.1: Comparison between content-based filtering and CF 
表6.1: コンテンツベースのフィルタリングとCFの比較 

A comparison of the two types of filtering is shown in Table 6.1. 
2つのフィルタリング手法の比較が表6.1に示されています。 
As you see, the two methods are complementary. 
ご覧の通り、2つの手法は相補的です。 



##### Hybrid filtering ハイブリッドフィルタリング

Hybrid filtering uses both CF and content-based filtering. 
ハイブリッドフィルタリングは、CF（Collaborative Filtering）とコンテンツベースフィルタリングの両方を使用します。

As Figure 6.6 shows, hybrid filtering combines CF-based and content-based recommenders sequentially, or in parallel. 
図6.6が示すように、ハイブリッドフィルタリングはCFベースのレコメンダーとコンテンツベースのレコメンダーを順次または並行して組み合わせます。

In practice, companies usually use sequential hybrid filtering [2]. 
実際には、企業は通常、順次ハイブリッドフィルタリングを使用します[2]。

This approach leads to better recommendations because it uses two data sources: the user's historical interactions and video features. 
このアプローチは、ユーザの過去のインタラクションとビデオの特徴という2つのデータソースを使用するため、より良い推薦をもたらします。

Video features allow the system to recommend relevant videos based on videos the user engaged with in the past, and CF-based filtering helps users to discover new areas of interest. 
ビデオの特徴により、システムはユーザが過去に関与したビデオに基づいて関連するビデオを推薦でき、CFベースのフィルタリングはユーザが新しい興味の領域を発見するのに役立ちます。



##### Which method should we choose? どの方法を選ぶべきか？

Many companies use hybrid filtering to make better recommendations. 
多くの企業は、より良い推薦を行うためにハイブリッドフィルタリングを使用しています。

For example, a paper published by Google [2] describes how YouTube employs a CF-based model as the first stage (candidate generator), followed by a content-based model as the second stage, to recommend videos. 
例えば、Googleによって発表された論文[2]は、YouTubeがどのようにCFベースのモデルを第一段階（候補生成器）として使用し、次にコンテンツベースのモデルを第二段階として使用して動画を推薦しているかを説明しています。

Due to the advantages of hybrid filtering, we choose this option. 
ハイブリッドフィルタリングの利点により、私たちはこのオプションを選択します。



### Data Preparation データ準備  
#### Data engineering データエンジニアリング
We have the following data available:  
私たちは以下のデータを利用可能です：
- Videos 動画
- Users ユーザ
- User-video interactions ユーザと動画のインタラクション



##### Videos ビデオ

Video data contains raw video files and their associated metadata, such as video ID, video length, video title, etc. 
ビデオデータは、生のビデオファイルと、それに関連するメタデータ（ビデオID、ビデオの長さ、ビデオのタイトルなど）を含みます。
Some of these attributes are provided explicitly by video uploaders, and others can be implicitly determined by the system, such as the video length.
これらの属性のいくつかはビデオアップローダーによって明示的に提供され、他の属性はシステムによって暗黙的に決定されることがあります（例えば、ビデオの長さなど）。

Table 6.2: Video metadata
表6.2: ビデオメタデータ



##### Users ユーザ

The following simple schema represents user data.
以下のシンプルなスキーマはユーザデータを表しています。

Table 6.3: User data schema
表6.3: ユーザデータスキーマ



##### User-video interactions ユーザ-ビデオインタラクション

The user-video interaction data consists of various user interactions with the videos, including likes, clicks, impressions, and past searches. 
ユーザ-ビデオインタラクションデータは、いいね、クリック、インプレッション、過去の検索を含む、ビデオに対するさまざまなユーザのインタラクションで構成されています。

Interactions are recorded along with other contextual information, such as location and timestamp. 
インタラクションは、位置情報やタイムスタンプなどの他の文脈情報とともに記録されます。

The following table shows how user-video interactions are stored. 
以下の表は、ユーザ-ビデオインタラクションがどのように保存されるかを示しています。

Table 6.4: User-video interaction data



#### Feature engineering 特徴量エンジニアリング

The ML system is required to predict videos that are relevant to users. 
MLシステムは、ユーザに関連する動画を予測する必要があります。
Let's engineer features to help the system make informed predictions. 
システムが情報に基づいた予測を行うのを助けるために、特徴量を設計しましょう。



##### Video features 動画の特徴

Some important video features include: 
いくつかの重要な動画の特徴には以下が含まれます：
- Video ID 
- Duration 
- Language 
- Titles and tags 

The IDs are categorical data. 
IDはカテゴリカルデータです。 
To represent them by numerical vectors, we use an embedding layer, and the embedding layer is learned during model training. 
数値ベクトルで表現するために、埋め込み層を使用し、埋め込み層はモデルのトレーニング中に学習されます。 

This defines approximately how long the video lasts from start to finish. 
これは、動画が開始から終了までの大まかな長さを定義します。 
This information is important since some users may prefer shorter videos, while others prefer longer videos. 
この情報は重要です。なぜなら、短い動画を好むユーザーもいれば、長い動画を好むユーザーもいるからです。 

The language used in a video is an important feature. 
動画で使用される言語は重要な特徴です。 
This is because users naturally prefer particular languages. 
これは、ユーザーが自然に特定の言語を好むためです。 
Since language is a categorical variable and takes on a finite set of discrete values, we use an embedding layer to represent it. 
言語はカテゴリカル変数であり、有限の離散値のセットを取るため、埋め込み層を使用して表現します。 

Titles and tags are used to describe a video. 
タイトルとタグは動画を説明するために使用されます。 
They are either provided manually by the uploader or are implicitly predicted by standalone ML models. 
それらはアップローダーによって手動で提供されるか、スタンドアロンの機械学習モデルによって暗黙的に予測されます。 
The titles and tags of a video are valuable predictors. 
動画のタイトルとタグは貴重な予測因子です。 
For example, a video titled "how to make pizza" indicates the video is related to pizza and cooking. 
例えば、「ピザの作り方」というタイトルの動画は、その動画がピザと料理に関連していることを示しています。 

How to prepare it? 
それをどのように準備しますか？ 
For tags, we use a lightweight pre-trained model, such as CBOW [3], to map them into feature vectors. 
タグについては、CBOW [3]のような軽量の事前学習モデルを使用して、それらを特徴ベクトルにマッピングします。 

For the title, we map it into a feature vector using a context-aware word embedding model, such as a pre-trained BERT [4]. 
タイトルについては、事前学習されたBERT [4]のようなコンテキスト対応の単語埋め込みモデルを使用して、特徴ベクトルにマッピングします。 

Figure 6.7 shows an overview of video feature preparation. 
図6.7は動画特徴準備の概要を示しています。



##### User features ユーザ特徴

We categorize user features into the following buckets:
私たちはユーザ特徴を以下のカテゴリに分類します：
- User demographics ユーザの人口統計
- Contextual information コンテキスト情報
- User historical interactions ユーザの過去のインタラクション
An overview of user demographic features is shown in Figure 6.8.
ユーザの人口統計特徴の概要は図6.8に示されています。

Here are a few important features for capturing contextual information:
ここでは、コンテキスト情報を捉えるためのいくつかの重要な特徴を示します：
- Time of day. A user may watch different videos at different times of day. 
- 時間帯。ユーザは異なる時間帯に異なる動画を視聴することがあります。
  For example, a software engineer may watch more educational videos during the evening.
  例えば、ソフトウェアエンジニアは夕方により多くの教育的な動画を視聴するかもしれません。
- Device. On mobile devices, users may prefer shorter videos.
- デバイス。モバイルデバイスでは、ユーザは短い動画を好むかもしれません。
- Day of the week. Depending on the day of the week, users may have different preferences for videos.
- 曜日。曜日によって、ユーザは動画に対する好みが異なるかもしれません。

User historical interactions play an important role in understanding user interests.
ユーザの過去のインタラクションは、ユーザの興味を理解する上で重要な役割を果たします。
A few features related to historical interactions are:
過去のインタラクションに関連するいくつかの特徴は以下の通りです：
- Search history 検索履歴
- Liked videos いいねした動画
- Watched videos and impressions 視聴した動画とインプレッション

Search history Why is it important?
検索履歴 なぜ重要なのか？
Previous searches indicate what the user looked for in the past, and past behavior is often an indicator of future behavior.
過去の検索は、ユーザが過去に何を探していたかを示し、過去の行動はしばしば未来の行動の指標となります。

How to prepare it?
どのように準備するか？
Use a pre-trained word embedding model, such as BERT, to map each search query into an embedding vector.
BERTのような事前学習済みの単語埋め込みモデルを使用して、各検索クエリを埋め込みベクトルにマッピングします。
Note that a user's search history is a variable-sized list of textual queries.
ユーザの検索履歴は可変サイズのテキストクエリのリストであることに注意してください。
To create a fixed-size feature vector summarizing all the search queries, we average the query embeddings.
すべての検索クエリを要約する固定サイズの特徴ベクトルを作成するために、クエリの埋め込みを平均化します。

Liked videos Why is it important?
いいねした動画 なぜ重要なのか？
The videos a user liked previously can be helpful in determining which type of content they're interested in.
ユーザが以前にいいねした動画は、どのタイプのコンテンツに興味があるかを判断するのに役立ちます。

How to prepare it?
どのように準備するか？
Video IDs are mapped into embedding vectors using the embedding layer.
動画IDは埋め込み層を使用して埋め込みベクトルにマッピングされます。
Similarly to search history, we average liked embeddings to get a fixed-size vector of liked videos.
検索履歴と同様に、いいねした埋め込みを平均化して、いいねした動画の固定サイズベクトルを取得します。

Watched videos and impressions The feature engineering process for “watched videos" and “impressions" is very similar to what we did for liked videos.
視聴した動画とインプレッション 「視聴した動画」と「インプレッション」の特徴エンジニアリングプロセスは、いいねした動画に対して行ったことと非常に似ています。
So, we won’t repeat it.
したがって、繰り返すことはありません。

Figure 6.10 summarizes features related to user-video interactions.
図6.10は、ユーザと動画のインタラクションに関連する特徴を要約しています。



### Model Development モデル開発

In this section, we examine two embedding-based models that are typically employed in CF-based or content-based recommenders:
このセクションでは、CFベースまたはコンテンツベースのレコメンダーで一般的に使用される2つの埋め込みベースのモデルを検討します：
- Matrix factorization
- Two-tower neural network



#### Matrix factorization 行列分解

To understand the matrix factorization model, it is important to know what a feedback matrix is.
行列分解モデルを理解するためには、フィードバック行列が何であるかを知ることが重要です。



##### Feedback matrix フィードバック行列

Also called a utility matrix, this is a matrix that represents users' opinions about videos. 
ユーティリティ行列とも呼ばれ、これはユーザの動画に対する意見を表す行列です。 
Figure 6.11 shows a binary user-video feedback matrix where each row represents a user, and each column represents a video. 
図6.11は、各行がユーザを、各列が動画を表すバイナリユーザ-動画フィードバック行列を示しています。 
The entries in the matrix specify the user's opinion to 1 as "observed" or "positive." 
行列のエントリは、ユーザの意見を1として「観察された」または「ポジティブ」と指定します。

How can we determine whether a user finds a recommended video relevant? 
どのようにしてユーザが推奨された動画を関連性があると感じているかを判断できますか？ 
We have three options: 
私たちには3つの選択肢があります：
- Explicit feedback 
- Implicit feedback 
- Combination of explicit and implicit feedback 
明示的フィードバック
暗黙的フィードバック
明示的および暗黙的フィードバックの組み合わせ

Explicit feedback. A feedback matrix is built based on interactions that explicitly indicate a user's opinion about a video, such as likes and shares. 
明示的フィードバック。フィードバック行列は、いいねやシェアなど、ユーザの動画に対する意見を明示的に示すインタラクションに基づいて構築されます。 
Explicit feedback reflects a user's opinion accurately as users explicitly expressed their interest in a video. 
明示的フィードバックは、ユーザが動画に対する興味を明示的に表現するため、ユーザの意見を正確に反映します。 
This option, however, has one major drawback: the matrix is sparse since only a small fraction of users provide explicit feedback. 
しかし、この選択肢には1つの大きな欠点があります：行列はスパースであり、少数のユーザしか明示的フィードバックを提供しないためです。 
Sparsity makes ML models difficult to train. 
スパース性は、機械学習モデルのトレーニングを困難にします。

Implicit feedback. This option uses interactions that implicitly indicate a user's opinion about a video, such as "clicks" or "watch time". 
暗黙的フィードバック。この選択肢は、「クリック」や「視聴時間」など、ユーザの動画に対する意見を暗黙的に示すインタラクションを使用します。 
With implicit feedback, more data points are available, resulting in a better model after training. 
暗黙的フィードバックを使用すると、より多くのデータポイントが利用可能になり、トレーニング後により良いモデルが得られます。 
Its main disadvantage is that it does not directly reflect users' opinions and might be noisy. 
その主な欠点は、ユーザの意見を直接反映せず、ノイズが含まれる可能性があることです。

Combination of explicit and implicit feedback. This option combines explicit and implicit feedback using heuristics. 
明示的および暗黙的フィードバックの組み合わせ。この選択肢は、ヒューリスティックを使用して明示的および暗黙的フィードバックを組み合わせます。 
What is the best option for building our feedback matrix? 
フィードバック行列を構築するための最良の選択肢は何ですか？ 
Since the model needs to learn the values of the feedback matrix, it's important to build the matrix that aligns well with the ML objective we chose earlier. 
モデルがフィードバック行列の値を学習する必要があるため、以前に選択した機械学習の目的にうまく合致する行列を構築することが重要です。 
In our case, the ML objective is to maximize relevancy, where relevancy is defined as the combination of explicit and implicit feedback. 
私たちの場合、機械学習の目的は関連性を最大化することであり、関連性は明示的および暗黙的フィードバックの組み合わせとして定義されます。 
As such, the final option of combining explicit and implicit feedback is the best choice. 
したがって、明示的および暗黙的フィードバックを組み合わせる最終的な選択肢が最良の選択です。



##### Matrix factorization model 行列分解モデル

Matrix factorization is a simple embedding model. 
行列分解はシンプルな埋め込みモデルです。

The algorithm decomposes the user-video feedback matrix into the product of two lower-dimensional matrices. 
このアルゴリズムは、ユーザ-ビデオフィードバック行列を2つの低次元行列の積に分解します。

One lower-dimensional matrix represents user embeddings, and the other represents video embeddings. 
1つの低次元行列はユーザの埋め込みを表し、もう1つはビデオの埋め込みを表します。

In other words, the model learns to map each user into an embedding vector and each video into an embedding vector, such that their distance represents their relevance. 
言い換えれば、このモデルは各ユーザを埋め込みベクトルに、各ビデオを埋め込みベクトルにマッピングすることを学習し、その距離が関連性を表すようにします。

Figure6.126.126.12 shows how a feedback matrix is decomposed into user and video embeddings. 
図6.126.126.12は、フィードバック行列がユーザとビデオの埋め込みにどのように分解されるかを示しています。



##### Matrix factorization training 行列分解のトレーニング

As part of training, we aim to produce user and video embedding matrices so that their product is a good approximation of the feedback matrix (Figure 6.13.)  
トレーニングの一環として、ユーザとビデオの埋め込み行列を生成し、その積がフィードバック行列の良い近似となることを目指します（図6.13）。

To learn these embeddings, matrix factorization first randomly initializes two embedding matrices, then iteratively optimizes the embeddings to decrease the loss between the "Predicted scores matrix" and the "Feedback matrix".  
これらの埋め込みを学習するために、行列分解はまず2つの埋め込み行列をランダムに初期化し、その後、"予測スコア行列"と"フィードバック行列"の間の損失を減少させるように埋め込みを反復的に最適化します。

Loss function selection is an important consideration. Let's explore a few options:  
損失関数の選択は重要な考慮事項です。いくつかのオプションを見てみましょう：

- Squared distance over observed⟨\langle⟨user, video⟩\rangle⟩pairs  
- 観測された⟨\langle⟨ユーザ, ビデオ⟩\rangle⟩ペアに対する二乗距離の重み付け組み合わせ  
- A weighted combination of squared distance over observed pairs and unobserved pairs  

Squared distance over observed⟨\langle⟨user, video⟩\rangle⟩pairs  
観測された⟨\langle⟨ユーザ, ビデオ⟩\rangle⟩ペアに対する二乗距離この損失関数は、フィードバック行列のすべての観測された（非ゼロ値の）エントリのペアに対する二乗距離の合計を測定します。これは図6.14に示されています。

$A_{ij}$ refers to the entry with row $i$ and column $j$ in the feedback matrix, $U_i$ is the embedding of user $i$, $V_j$ is the embedding of video $j$, and the summation is over the observed pairs only.  
$A_{ij}$はフィードバック行列の行$i$と列$j$のエントリを指し、$U_i$はユーザ$i$の埋め込み、$V_j$はビデオ$j$の埋め込みであり、合計は観測されたペアのみに対して行われます。

Only summing over observed pairs leads to poor embeddings because the loss function doesn't penalize the model for bad predictions on unobserved pairs.  
観測されたペアのみに対して合計することは、損失関数が未観測ペアに対する悪い予測に対してモデルを罰しないため、良くない埋め込みにつながります。

For example, embedding matrices of all ones would have a zero loss on the training data.  
例えば、すべての要素が1の埋め込み行列は、トレーニングデータに対してゼロの損失を持つことになります。

However, those embeddings may not work well for unseen⟨\langle⟨user, video⟩\rangle⟩pairs.  
しかし、これらの埋め込みは未観測の⟨\langle⟨ユーザ, ビデオ⟩\rangle⟩ペアにはうまく機能しないかもしれません。

Squared distance over both observed and unobserved⟨\langle⟨user, video⟩\rangle⟩pairs  
観測された⟨\langle⟨ユーザ, ビデオ⟩\rangle⟩ペアと未観測の⟨\langle⟨ユーザ, ビデオ⟩\rangle⟩ペアに対する二乗距離この損失関数は、未観測のペアを負のデータポイントとして扱い、フィードバック行列においてそれらにゼロを割り当てます。

As Figure 6.15 shows, the loss computes the sum of the squared distances over all entries in the feedback matrix.  
図6.15に示すように、この損失はフィードバック行列のすべてのエントリに対する二乗距離の合計を計算します。

This loss function addresses the previous issue by penalizing bad predictions for unobserved entries.  
この損失関数は、未観測のエントリに対する悪い予測を罰することによって、前の問題に対処します。

However, this loss has a major drawback.  
しかし、この損失には大きな欠点があります。

The feedback matrix is usually sparse (lots of unobserved pairs), so unobserved pairs dominate observed pairs during training.  
フィードバック行列は通常スパース（多くの未観測ペア）であるため、未観測ペアがトレーニング中に観測ペアを支配します。

This results in predictions that are mostly close to zero.  
これにより、予測がほとんどゼロに近くなります。

This is not desirable and leads to poor generalization performance on unseen⟨\langle⟨user, video⟩\rangle⟩pairs.  
これは望ましくなく、未観測の⟨\langle⟨ユーザ, ビデオ⟩\rangle⟩ペアに対する一般化性能が低下します。

A weighted combination of squared distance over observed and unobserved pairs  
観測されたペアと未観測のペアに対する二乗距離の重み付け組み合わせ

To overcome the drawbacks of the loss functions described earlier, we opt for weighted combinations of both.  
前述の損失関数の欠点を克服するために、私たちは両方の重み付け組み合わせを選択します。

The first summation in the loss formula calculates the loss on the observed pairs, and the second summation calculates the loss on unobserved pairs.  
損失式の最初の合計は観測されたペアに対する損失を計算し、2番目の合計は未観測ペアに対する損失を計算します。

$W$ is a hyperparameter that weighs the two summations.  
$W$は2つの合計に重みを付けるハイパーパラメータです。

It ensures one does not dominate the other in the training phase.  
これにより、トレーニングフェーズで一方が他方を支配しないようにします。

This loss function with a properly tuned $W$ works well in practice [5].  
適切に調整された$W$を持つこの損失関数は、実際にうまく機能します[5]。

We choose this loss function for the system.  
私たちはこの損失関数をシステムに選択します。



##### Matrix factorization optimization 行列分解の最適化

To train an ML model, an optimization algorithm is required. 
MLモデルを訓練するためには、最適化アルゴリズムが必要です。

Two commonly used optimization algorithms in matrix factorization are:
行列分解で一般的に使用される2つの最適化アルゴリズムは次のとおりです。

- Stochastic Gradient Descent (SGD): This optimization algorithm is used to minimize losses [6]. 
- 確率的勾配降下法（SGD）：この最適化アルゴリズムは損失を最小化するために使用されます[6]。

- Weighted Alternating Least Squares (WALS): This optimization algorithm is specific to matrix factorization. 
- 重み付き交互最小二乗法（WALS）：この最適化アルゴリズムは行列分解に特化しています。

The process in WALS is:
WALSのプロセスは次のとおりです。

Fix one embedding matrix (U), and optimize the other embedding (V) 
1. 一方の埋め込み行列（U）を固定し、もう一方の埋め込み（V）を最適化します。

Fix the other embedding matrix (V), and optimize the embedding matrix (U) 
2. もう一方の埋め込み行列（V）を固定し、埋め込み行列（U）を最適化します。

Repeat. 
3. 繰り返します。

WALS usually converges faster and is parallelizable. 
WALSは通常、より早く収束し、並列化可能です。

To learn more about WALS, read [7]. 
WALSについて詳しく知りたい場合は、[7]を参照してください。

Here, we use WALS because it converges faster. 
ここでは、WALSを使用します。なぜなら、より早く収束するからです。



##### Matrix factorization inference 行列分解推論

To predict the relevance between an arbitrary user and a candidate video, we calculate the similarity between their embeddings using a similarity measure, such as a dot product. 
任意のユーザと候補動画の関連性を予測するために、私たちはドット積のような類似度測定を使用して、それらの埋め込み間の類似性を計算します。

For example, as shown in Figure 6.17, the relevance score between user 2 and video 5 is 0.32. 
例えば、図6.17に示すように、ユーザ2と動画5の関連性スコアは0.32です。

Figure 6.18 shows the predicted scores for all the ⟨user, video⟩ pairs. 
図6.18は、すべての⟨ユーザ, 動画⟩ペアに対する予測スコアを示しています。

The system returns recommended videos based on relevance scores. 
システムは、関連性スコアに基づいて推奨動画を返します。

Before wrapping up matrix factorization, let’s discuss the pros and cons of this model. 
行列分解をまとめる前に、このモデルの利点と欠点について議論しましょう。

Pros: 利点:
- Training speed: Matrix factorization is efficient during the training phase. 
- トレーニング速度: 行列分解はトレーニングフェーズ中に効率的です。

This is because there are only two embedding matrices to learn. 
これは、学習する埋め込み行列が2つだけだからです。

- Serving speed: Matrix factorization is fast at serving time. 
- サービング速度: 行列分解はサービング時に速いです。

The learned embeddings are static, meaning that once we learn them, we can reuse them without having to transform the input at query time. 
学習された埋め込みは静的であり、一度学習すれば、クエリ時に入力を変換することなく再利用できます。

Cons: 欠点:
- Matrix factorization only relies on user-video interactions. 
- 行列分解はユーザと動画の相互作用のみに依存します。

It does not use other features, such as the user's age or language. 
ユーザの年齢や言語などの他の特徴を使用しません。

This limits the predictive capability of the model because features like language are useful to improve the quality of recommendations. 
これは、言語のような特徴が推薦の質を向上させるのに役立つため、モデルの予測能力を制限します。

- Handling new users is difficult. 
- 新しいユーザを扱うのは難しいです。

For new users, there are not enough interactions for the model to produce meaningful embeddings. 
新しいユーザの場合、モデルが意味のある埋め込みを生成するための相互作用が不十分です。

Therefore, matrix factorization cannot determine whether a video is relevant to a user by computing the dot product between their embeddings. 
したがって、行列分解は、埋め込み間のドット積を計算することによって、動画がユーザに関連しているかどうかを判断できません。

Let's see how two-tower neural networks address the shortcomings of matrix factorization. 
行列分解の欠点に対処するために、2タワーのニューラルネットワークがどのように機能するかを見てみましょう。



#### Two-tower neural network 二塔型ニューラルネットワーク

A two-tower neural network comprises two encoder towers: the user tower and the video tower. 
二塔型ニューラルネットワークは、ユーザタワーとビデオタワーの2つのエンコーダタワーで構成されています。

The user encoder takes user features as input and maps them to an embedding vector (user embedding). 
ユーザエンコーダはユーザの特徴を入力として受け取り、それを埋め込みベクトル（ユーザ埋め込み）にマッピングします。

The video encoder takes video features as input and maps them into an embedding vector (video embedding). 
ビデオエンコーダはビデオの特徴を入力として受け取り、それを埋め込みベクトル（ビデオ埋め込み）にマッピングします。

The distance between their embeddings in the shared embedding space represents their relevance. 
共有埋め込み空間におけるそれらの埋め込みの距離は、関連性を表します。

Figure 6.19 shows the two-tower architecture. 
図6.19は二塔型アーキテクチャを示しています。

In contrast to matrix factorization, two-tower architectures are flexible enough to incorporate all kinds of features to better capture the user's specific interests. 
行列分解とは対照的に、二塔型アーキテクチャは、ユーザの特定の興味をよりよく捉えるために、あらゆる種類の特徴を取り入れる柔軟性があります。



##### Constructing the dataset データセットの構築

We construct the dataset by extracting features from different⟨\langle⟨user, video⟩\rangle⟩pairs and labeling them as positive or negative based on the user's feedback. 
私たちは、異なる⟨\langle⟨ユーザ, 動画⟩\rangle⟩ペアから特徴を抽出し、ユーザのフィードバックに基づいてそれらにポジティブまたはネガティブのラベルを付けることによってデータセットを構築します。

For example, we label a pair as "positive" if the user explicitly liked the video, or watched at least half of it. 
例えば、ユーザが動画を明示的に気に入った場合や、少なくとも半分以上視聴した場合、そのペアを「ポジティブ」とラベル付けします。

To construct negative data points, we can either choose random videos which are not relevant or choose those the user explicitly disliked by pressing the dislike button. 
ネガティブデータポイントを構築するために、関連性のないランダムな動画を選択するか、ユーザが「嫌い」ボタンを押して明示的に嫌った動画を選択することができます。

Figure 6.20 shows an example of the constructed data points. 
図6.20は、構築されたデータポイントの例を示しています。

Note, users usually only find a small fraction of videos relevant. 
注意すべきは、ユーザは通常、動画のごく一部しか関連性があると見なさないことです。

While constructing training data, this leads to an imbalanced dataset where there are many more negative than positive pairs. 
トレーニングデータを構築する際、これはポジティブペアよりもネガティブペアがはるかに多い不均衡なデータセットにつながります。

Training a model on an imbalanced dataset is problematic. 
不均衡なデータセットでモデルをトレーニングすることは問題があります。

We can use the techniques described in Chapter 1 Introduction and Overview, to address the data imbalance issue. 
データの不均衡問題に対処するために、章1の「はじめにと概要」で説明されている技術を使用することができます。



##### Choosing the loss function 損失関数の選択

Since the two-tower neural network is trained to predict binary labels, the problem can be categorized as a classification task. 
二塔型ニューラルネットワークはバイナリラベルを予測するように訓練されるため、この問題は分類タスクとして分類できます。
We use a typical classification loss function, such as cross-entropy, to optimize the encoders during training. 
私たちは、クロスエントロピーのような典型的な分類損失関数を使用して、訓練中にエンコーダを最適化します。
This process is shown in Figure 6.21. 
このプロセスは図6.21に示されています。



##### Two-tower neural network inference 二塔型ニューラルネットワーク推論

At inference time, the system uses the embeddings to find the most relevant videos for a given user. 
推論時に、システムは埋め込みを使用して特定のユーザーに最も関連性の高い動画を見つけます。

This is a classic "nearest neighbor" problem. 
これは古典的な「最近傍」問題です。

We use approximate nearest neighbor methods to find the top $k$ most similar video embeddings efficiently. 
私たちは、近似最近傍法を使用して、最も類似した動画の埋め込みを効率的に上位 $k$ 件見つけます。

Two-tower neural networks are used for both content-based filtering and collaborative filtering. 
二塔型ニューラルネットワークは、コンテンツベースのフィルタリングと協調フィルタリングの両方に使用されます。

When a two-tower architecture is used for collaborative filtering, as shown in Figure 6.22, the video encoder is nothing but an embedding layer that converts the video ID into an embedding vector. 
協調フィルタリングに二塔型アーキテクチャが使用されると、図6.22に示すように、動画エンコーダは動画IDを埋め込みベクトルに変換する埋め込み層に過ぎません。

This way, the model doesn't rely on other video features. 
この方法により、モデルは他の動画の特徴に依存しません。

Let’s see the pros and cons of a two-tower neural network model. 
二塔型ニューラルネットワークモデルの利点と欠点を見てみましょう。

Pros: 利点:
- Utilizes user features. 
- ユーザーの特徴を活用します。

The model accepts user features, such as age and gender, as input. 
モデルは、年齢や性別などのユーザーの特徴を入力として受け入れます。

These predictive features help the model make better recommendations. 
これらの予測特徴は、モデルがより良い推薦を行うのに役立ちます。

- Handles new users. 
- 新しいユーザーを扱います。

The model easily handles new users as it relies on user features (e.g., age, gender, etc.). 
モデルはユーザーの特徴（例：年齢、性別など）に依存するため、新しいユーザーを簡単に扱います。

Cons: 欠点:
- Slower serving. 
- サービングが遅くなります。

The model needs to compute the user embedding at query time. 
モデルはクエリ時にユーザーの埋め込みを計算する必要があります。

This makes the model slower to serve requests. 
これにより、モデルはリクエストに対して遅くなります。

In addition, if we use the model for content-based filtering, the model needs to transform video features into video embedding, which increases the inference time. 
さらに、コンテンツベースのフィルタリングにモデルを使用する場合、モデルは動画の特徴を動画の埋め込みに変換する必要があり、これが推論時間を増加させます。

- Training is more expensive. 
- トレーニングがより高価です。

Two-tower neural networks have more learning parameters than matrix factorization. 
二塔型ニューラルネットワークは、行列分解よりも多くの学習パラメータを持っています。

Therefore, the training is more compute-intensive. 
したがって、トレーニングはより計算集約的です。



#### Matrix factorization vs. two-tower neural network 行列分解と二塔型ニューラルネットワークの比較

Table 6.5 summarizes the differences between matrix factorization and two-tower neural network architecture. 
表6.5は、行列分解と二塔型ニューラルネットワークアーキテクチャの違いを要約しています。

Table 6.5: Matrix factorization vs. two-tower neural networks 
表6.5: 行列分解と二塔型ニューラルネットワークの比較



### Evaluation 評価

The system’s performance can be evaluated with offline and online metrics.
システムのパフォーマンスは、オフラインおよびオンラインのメトリクスで評価できます。



#### Offline metrics オフライン指標

We evaluate the following offline metrics commonly used in recommendation systems.
私たちは、推薦システムで一般的に使用される以下のオフライン指標を評価します。

Precision@k. This metric measures the proportion of relevant videos among the top $k$ recommended videos.
Precision@k。この指標は、上位 $k$ 件の推薦動画の中で関連性のある動画の割合を測定します。

Multiple $k$ values (e.g., 1, 5, 10) can be used.
複数の $k$ 値（例：1, 5, 10）を使用できます。

mAP. This metric measures the ranking quality of recommended videos.
mAP。この指標は、推薦動画のランキング品質を測定します。

It is a good fit because the relevance scores are binary in our system.
私たちのシステムでは関連性スコアが二値であるため、適切です。

Diversity. This metric measures how dissimilar recommended videos are to each other.
Diversity。この指標は、推薦動画がどれだけ異なるかを測定します。

This metric is important to track, as users are more interested in diversified videos.
この指標は重要であり、ユーザは多様な動画により関心を持つため、追跡することが重要です。

To measure diversity, we calculate the average pairwise similarity (e.g., cosine similarity or dot product) between videos in the list.
多様性を測定するために、リスト内の動画間の平均ペアワイズ類似度（例：コサイン類似度または内積）を計算します。

A low average pairwise similarity score indicates the list is diverse.
低い平均ペアワイズ類似度スコアは、リストが多様であることを示します。

Note that using diversity as the sole measure of quality can result in misleading interpretations.
多様性を品質の唯一の指標として使用すると、誤解を招く解釈を生む可能性があることに注意してください。

For example, if the recommended videos are diverse but irrelevant to the user, they may not find the recommendations helpful.
例えば、推薦された動画が多様であってもユーザにとって関連性がない場合、彼らは推薦が役に立たないと感じるかもしれません。

Therefore, we should use diversity with other offline metrics to ensure both relevance and diversity.
したがって、関連性と多様性の両方を確保するために、他のオフライン指標とともに多様性を使用すべきです。



#### Online metrics オンライン指標

In practice, companies track many metrics during online evaluation. 
実際には、企業はオンライン評価中に多くの指標を追跡します。

Let's examine some of the most important ones: 
最も重要な指標のいくつかを見てみましょう：

- Click-through rate (CTR) 
- クリック率 (CTR)
- The number of completed videos 
- 完了した動画の数
- Total watch time 
- 総視聴時間
- Explicit user feedback 
- 明示的なユーザーフィードバック

CTR. The ratio between clicked videos and the total number of recommended videos. 
CTR。クリックされた動画と推奨された動画の総数の比率です。

The formula is: 
式は次のとおりです：

$$
CTR = \frac{\text{number of clicked videos}}{\text{total number of recommended videos}}
$$

CTR is an insightful metric to track user engagement, but the drawback of CTR is that we cannot capture or measure clickbait videos. 
CTRはユーザーエンゲージメントを追跡するための洞察に満ちた指標ですが、CTRの欠点は、クリックベイト動画を捉えたり測定したりできないことです。

The number of completed videos. The total number of recommended videos that users watch until the end. 
完了した動画の数。ユーザーが最後まで視聴した推奨動画の総数です。

By tracking this metric, we can understand how often the system recommends videos that users watch. 
この指標を追跡することで、システムがユーザーが視聴する動画をどのくらいの頻度で推奨しているかを理解できます。

Total watch time. The total time users spent watching the recommended videos. 
総視聴時間。ユーザーが推奨された動画を視聴した合計時間です。

When recommendations interest users, they spend more time watching videos, overall. 
推奨がユーザーの興味を引くと、全体的に動画を視聴する時間が増えます。

Explicit user feedback. The total number of videos that users explicitly liked or disliked. 
明示的なユーザーフィードバック。ユーザーが明示的に「いいね」または「よくない」と評価した動画の総数です。

The metric accurately reflects users' opinions of recommended videos. 
この指標は、推奨された動画に対するユーザーの意見を正確に反映しています。



### Serving サービング

At serving time, the system recommends the most relevant videos to a given user by narrowing the selection down from billions of videos. 
サービング時に、システムは数十億の動画から選択肢を絞り込み、特定のユーザーに最も関連性の高い動画を推薦します。 
In this section, we will propose a prediction pipeline that's both efficient and accurate at serving requests. 
このセクションでは、リクエストに対して効率的かつ正確に応答する予測パイプラインを提案します。

Given we have billions of videos available, the serving speed would be slow if we choose a heavy model which takes lots of features as input. 
数十億の動画が利用可能であるため、多くの特徴を入力として受け取る重いモデルを選択すると、サービング速度が遅くなります。 
On the other hand, if we choose a lightweight model, it may not produce high-quality recommendations. 
一方、軽量モデルを選択すると、高品質な推薦が得られない可能性があります。 
So, what to do? 
では、どうすればよいのでしょうか？ 
A natural decision is to use more than one model in a multi-stage design. 
自然な選択肢は、マルチステージ設計で複数のモデルを使用することです。 
For example, in a two-stage design, a lightweight model quickly narrows down the videos during the first stage, called candidate generation. 
例えば、二段階設計では、軽量モデルが最初の段階（候補生成）で動画を迅速に絞り込みます。 
The second stage uses a heavier model that accurately scores and ranks the videos, called scoring. 
第二段階では、動画を正確にスコアリングしランク付けする重いモデル（スコアリング）を使用します。 
Figure6.236.236.23 shows how candidate generation and scoring work together to produce relevant videos. 
図6.236.236.23は、候補生成とスコアリングがどのように連携して関連する動画を生成するかを示しています。

Let's take a closer look at the components of the prediction pipeline. 
予測パイプラインの構成要素を詳しく見てみましょう。
- Candidate generation
- Scoring
- Re-ranking



#### Candidate generation 候補生成

The goal of candidate generation is to narrow down the videos from potentially billions, to thousands. 
候補生成の目的は、潜在的に数十億の動画から数千に絞り込むことです。

We prioritize efficiency over accuracy at this stage and are not concerned about false positives. 
この段階では、精度よりも効率を優先し、偽陽性については気にしません。

To keep candidate generation fast, we choose a model which doesn't rely on video features. 
候補生成を迅速に保つために、動画の特徴に依存しないモデルを選択します。

In addition, this model should be able to handle new users. 
さらに、このモデルは新しいユーザーにも対応できる必要があります。

A two-tower neural network is a good fit for this stage. 
二塔型ニューラルネットワークは、この段階に適しています。

Figure 6.24 shows the candidate generation workflow. 
図6.24は候補生成のワークフローを示しています。

The candidate generation obtains a user's embedding from the user encoder. 
候補生成は、ユーザーエンコーダからユーザーの埋め込みを取得します。

Once the computation is complete, it retrieves the most similar videos from the approximate nearest neighbor service. 
計算が完了すると、近似最近傍サービスから最も類似した動画を取得します。

These videos are ranked based on similarity in the embedding space and are returned as the output. 
これらの動画は、埋め込み空間での類似性に基づいてランク付けされ、出力として返されます。

In practice, companies may choose to use more than one candidate generation because it could improve the performance of the recommendation. 
実際には、企業は推薦のパフォーマンスを向上させる可能性があるため、複数の候補生成を使用することを選択するかもしれません。

Let's take a look at why. 
その理由を見てみましょう。

Users may be interested in videos for many reasons. 
ユーザーは多くの理由で動画に興味を持つかもしれません。

For example, a user may choose to watch a video because it's popular, trending, or relevant to their location. 
例えば、ユーザーは人気がある、トレンドになっている、または自分の位置に関連しているために動画を視聴することを選ぶかもしれません。

To include those videos in the recommendations, it is common to use more than one candidate generation, as shown in Figure 6.25. 
これらの動画を推薦に含めるために、図6.25に示すように、複数の候補生成を使用することが一般的です。

As soon as we have narrowed down potential videos from billions to thousands, we can use a scoring component to rank these videos before they are displayed. 
数十億の潜在的な動画を数千に絞り込むと、表示される前にこれらの動画をランク付けするためにスコアリングコンポーネントを使用できます。



#### Scoring スコアリング

Also known as ranking, scoring takes the user and candidate videos as input, scores each video, and outputs a ranked list of videos.
スコアリングはランキングとも呼ばれ、ユーザと候補動画を入力として受け取り、各動画にスコアを付け、ランキングされた動画のリストを出力します。
At this stage, we prioritize accuracy over efficiency.
この段階では、効率性よりも正確性を優先します。
To do so, we choose content-based filtering filtering and pick a model which relies on video features.
そのために、コンテンツベースのフィルタリングを選択し、動画の特徴に依存するモデルを選びます。
A two-tower neural network is a common choice for this stage.
この段階では、二塔型ニューラルネットワークが一般的な選択肢です。
Since there are only a handful of videos to rank in the scoring stage, we can employ a heavier model with more parameters.
スコアリング段階ではランク付けする動画がわずかしかないため、より多くのパラメータを持つ重いモデルを使用することができます。
Figure 6.26 shows an overview of the scoring component.
図6.26は、スコアリングコンポーネントの概要を示しています。



#### Re-ranking 再ランキング

This component re-ranks the videos by adding additional criteria or constraints. 
このコンポーネントは、追加の基準や制約を加えることによって動画を再ランキングします。

For example, we may use standalone ML models to determine if a video is clickbait. 
例えば、独立した機械学習モデルを使用して、動画がクリックベイトであるかどうかを判断することがあります。

Here are a few important things to consider when building the re-ranking component: 
再ランキングコンポーネントを構築する際に考慮すべき重要な点をいくつか挙げます：

- Region-restricted videos 
- 地域制限された動画

- Video freshness 
- 動画の新鮮さ

- Videos spreading misinformation 
- 誤情報を広める動画

- Duplicate or near-duplicate videos 
- 重複またはほぼ重複する動画

- Fairness and bias 
- 公平性とバイアス



#### Challenges of video recommendation systems 動画推薦システムの課題

Before wrapping up this chapter, let’s see how our design addresses typical challenges in video recommendation systems. 
この章を締めくくる前に、私たちのデザインが動画推薦システムにおける典型的な課題にどのように対処しているかを見てみましょう。



##### Serving speed 提供速度

It is vital to recommend videos fast. 
動画を迅速に推薦することは非常に重要です。
However, as we have billions of videos in this system, recommending them efficiently and accurately is challenging. 
しかし、このシステムには数十億の動画があるため、それらを効率的かつ正確に推薦することは困難です。
To address this issue, we used a two-stage design. 
この問題に対処するために、私たちは二段階の設計を使用しました。
Specifically, we use a lightweight model in the first stage to quickly narrow down candidate videos from billions to thousands. 
具体的には、最初の段階で軽量モデルを使用して、数十億の動画から数千の候補動画に迅速に絞り込みます。
YouTube uses a similar approach [2], and Instagram adopts a multi-stage design [8]. 
YouTubeは同様のアプローチを使用しており[2]、Instagramはマルチステージ設計を採用しています[8]。



##### Precision 精度

To ensure precision, we employ a scoring component that ranks videos using a powerful model, which relies on more features, including video features. 
精度を確保するために、私たちは強力なモデルを使用して動画をランク付けするスコアリングコンポーネントを採用しており、これは動画の特徴を含むより多くの特徴に依存しています。
Using a more powerful model doesn't affect serving speed because only a small subset of videos is selected after the candidate generation phase.
より強力なモデルを使用しても、候補生成フェーズの後に選択される動画のサブセットが小さいため、提供速度には影響しません。



##### Diversity 多様性

Most users prefer to see a diverse selection of videos in their recommendations. 
ほとんどのユーザーは、推薦される動画の多様な選択肢を見たいと好みます。
To ensure our system produces a diverse set of videos, we adopt multiple candidate generators, as explained in the candidate generation section.
私たちのシステムが多様な動画セットを生成することを保証するために、候補生成セクションで説明されているように、複数の候補生成器を採用します。



##### Cold-start problem コールドスタート問題

How does our system handle the cold-start problem?  
私たちのシステムはコールドスタート問題をどのように扱っていますか？

For new users: We don't have any interaction data about new users when they begin using our platform.  
新しいユーザについて: 新しいユーザが私たちのプラットフォームを使用し始めるとき、彼らに関するインタラクションデータはありません。

In this case, predictions are made using two-tower neural networks based on features such as age, gender, language, location, etc.  
この場合、年齢、性別、言語、場所などの特徴に基づいて、2タワーニューラルネットワークを使用して予測が行われます。

The recommended videos are personalized to some extent, even for new users.  
推奨される動画は、新しいユーザに対してもある程度パーソナライズされています。

As the user interacts with more videos, we are able to make better predictions based on new interactions.  
ユーザがより多くの動画とインタラクションを持つにつれて、新しいインタラクションに基づいてより良い予測を行うことができるようになります。

For new videos: When a new video is added to the system, the video metadata and content are available, but no interactions are present.  
新しい動画について: 新しい動画がシステムに追加されると、動画のメタデータとコンテンツは利用可能ですが、インタラクションは存在しません。

One way to handle this is to use heuristics.  
これを扱う一つの方法は、ヒューリスティクスを使用することです。

We can display videos to random users and collect interaction data.  
私たちは動画をランダムなユーザに表示し、インタラクションデータを収集することができます。

Once we gather enough interactions, we fine-tune the two-tower neural network using the new interactions.  
十分なインタラクションを収集したら、新しいインタラクションを使用して2タワーニューラルネットワークをファインチューニングします。



##### Training scalability トレーニングのスケーラビリティ

It's challenging to train models on large datasets in a cost-effective manner. 
大規模データセットでモデルをコスト効率よくトレーニングすることは困難です。

In recommendation systems, new interactions are continuously added, and the models need to quickly adapt to make accurate recommendations. 
推薦システムでは、新しいインタラクションが継続的に追加され、モデルは正確な推薦を行うために迅速に適応する必要があります。

To quickly adapt to new data, the models should be able to be fine-tuned. 
新しいデータに迅速に適応するために、モデルはファインチューニングできる必要があります。

In our case, the models are based on neural networks and designed to be easily fine-tuned. 
私たちのケースでは、モデルはニューラルネットワークに基づいており、簡単にファインチューニングできるように設計されています。



### Other Talking Points その他の話題

If there is time left at the end of the interview, here are some additional talking points:
インタビューの最後に時間が残っている場合、以下の追加の話題があります：

- The exploration-exploitation trade-off in recommendation systems [9].
推薦システムにおける探索と活用のトレードオフ [9]。
- Different types of biases may be present in recommendation systems [10].
推薦システムにはさまざまなタイプのバイアスが存在する可能性があります [10]。
- Important considerations related to ethics when building recommendation systems [11].
推薦システムを構築する際の倫理に関連する重要な考慮事項 [11]。
- Consider the effect of seasonality - changes in users' behaviors during different seasons - in a recommendation system [12].
推薦システムにおける季節性の影響 - 異なる季節におけるユーザの行動の変化 - を考慮する [12]。
- Optimize the system for multiple objectives, instead of a single objective [13].
単一の目的ではなく、複数の目的のためにシステムを最適化する [13]。
- How to benefit from negative feedback such as dislikes [14].
嫌いなどのネガティブフィードバックからどのように利益を得るか [14]。
- Leverage the sequence of videos in a user's search history or watch history [2].
ユーザの検索履歴や視聴履歴における動画のシーケンスを活用する [2]。



### References 参考文献

1. YouTube recommendation system. https://blog.youtube/inside-youtube/on-youtubes-recommendation-system.
   YouTubeの推薦システム。 https://blog.youtube/inside-youtube/on-youtubes-recommendation-system.
   
2. DNN for YouTube recommendation. https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf.
   YouTube推薦のためのDNN。 https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf.
   
3. CBOW paper. https://arxiv.org/pdf/1301.3781.pdf.
   CBOWに関する論文。 https://arxiv.org/pdf/1301.3781.pdf.
   
4. BERT paper. https://arxiv.org/pdf/1810.04805.pdf.
   BERTに関する論文。 https://arxiv.org/pdf/1810.04805.pdf.
   
5. Matrix factorization. https://developers.google.com/machine-learning/recommendation/collaborative/matrix.
   行列分解。 https://developers.google.com/machine-learning/recommendation/collaborative/matrix.
   
6. Stochastic gradient descent. https://en.wikipedia.org/wiki/Stochastic_gradient_descent.
   確率的勾配降下法。 https://en.wikipedia.org/wiki/Stochastic_gradient_descent.
   
7. WALS optimization. https://fairyonice.github.io/Learn-about-collaborative-filtering-and-weighted-alternating-least-square-with-tensorflow.html.
   WALS最適化。 https://fairyonice.github.io/Learn-about-collaborative-filtering-and-weighted-alternating-least-square-with-tensorflow.html.
   
8. Instagram multi-stage recommendation system. https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/.
   Instagramのマルチステージ推薦システム。 https://ai.facebook.com/blog/powered-by-ai-instagrams-explore-recommender-system/.
   
9. Exploration and exploitation trade-offs. https://en.wikipedia.org/wiki/Multi-armed_bandit.
   探索と活用のトレードオフ。 https://en.wikipedia.org/wiki/Multi-armed_bandit.
   
10. Bias in AI and recommendation systems. https://www.searchenginejournal.com/biases-search-recommender-systems/339319/#close.
    AIと推薦システムにおけるバイアス。 https://www.searchenginejournal.com/biases-search-recommender-systems/339319/#close.
    
11. Ethical concerns in recommendation systems. https://link.springer.com/article/10.1007/s00146-020-00950-y.
    推薦システムにおける倫理的懸念。 https://link.springer.com/article/10.1007/s00146-020-00950-y.
    
12. Seasonality in recommendation systems. https://www.computer.org/csdl/proceedings-article/big-data/2019/09005954/1hJsfgT0qL6.
    推薦システムにおける季節性。 https://www.computer.org/csdl/proceedings-article/big-data/2019/09005954/1hJsfgT0qL6.
    
13. A multitask ranking system. https://daiwk.github.io/assets/youtube-multitask.pdf.
    マルチタスクランキングシステム。 https://daiwk.github.io/assets/youtube-multitask.pdf.
    
14. Benefit from a negative feedback. https://arxiv.org/abs/1607.04228?context=cs.
    ネガティブフィードバックからの利益。 https://arxiv.org/abs/1607.04228?context=cs.



### Partner With Us パートナーシップのご案内



### Company & Legal 会社と法務



### Support サポート



### Careers キャリア

Copyright ©2025 ByteByteGo Inc. All rights reserved.
著作権 ©2025 ByteByteGo Inc. 無断転載を禁じます。
