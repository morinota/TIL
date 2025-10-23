refs: https://bytebytego.com/courses/machine-learning-system-design-interview/personalized-news-feed


# Personalized News Feed パーソナライズされたニュースフィード

### Introduction はじめに

A news feed is a feature of social network platforms that keeps users engaged by showing friends’ recent activities on their timelines. 
ニュースフィードは、ソーシャルネットワークプラットフォームの機能であり、ユーザーのタイムラインに友人の最近の活動を表示することで、ユーザーの関与を維持します。
Most social networks such as Facebook [1], Twitter [2], and LinkedIn [3] personalize news feed to maintain user engagement.
Facebook [1]、Twitter [2]、LinkedIn [3]などのほとんどのソーシャルネットワークは、ユーザーの関与を維持するためにニュースフィードをパーソナライズしています。
In this chapter, we are asked to design a personalized news feed system.
この章では、パーソナライズされたニュースフィードシステムを設計するよう求められています。

### Clarifying Requirements 要件の明確化

Here is a typical interaction between a candidate and an interviewer.
ここでは、候補者と面接官の典型的なやり取りを示します。

Candidate: Can I assume the motivation for a personalized news feed is to keep users engaged with the platform?
候補者: パーソナライズされたニュースフィードの動機は、ユーザーをプラットフォームに引きつけることだと考えてもよいですか？
Interviewer: Yes, we display sponsored ads between posts, and more engagement leads to increased revenue.
面接官: はい、私たちは**投稿の間にスポンサー広告を表示しており、より多くのエンゲージメントが収益の増加につながります**。

Candidate: When a user refreshes their timeline, we display posts with new activities to the user. Can I assume this activity consists of both unseen posts and posts with unseen comments?
候補者: ユーザーがタイムラインを更新すると、新しいアクティビティを含む投稿を表示します。**このアクティビティは、未表示の投稿と未表示のコメントを含む投稿の両方で構成される**と考えてもよいですか？
Interviewer: That is a fair assumption.
面接官: それは妥当な仮定です。

Candidate: Can a post contain textual content, images, video, or any combination?
候補者: **投稿にはテキストコンテンツ、画像、動画、またはその組み合わせ**を含めることができますか？
Interviewer: It can be any combination.
面接官: それはどのような組み合わせでも可能です。

Candidate: To keep users engaged, the system should place the most engaging content at the top of timelines, as people are more likely to interact with the first few posts. Does that sound right?
候補者: **ユーザーを引きつけるために、システムは最もエンゲージングなコンテンツをタイムラインの上部に配置すべきです。人々は最初の数件の投稿とより多くインタラクトする可能性が高いから**です。これで合っていますか？
Interviewer: Yes, that's correct.
面接官: はい、その通りです。

Candidate: Is there a specific type of engagement we are optimizing for? I assume there are different types of engagement, such as clicks, likes, and shares.
候補者: 私たちが最適化している特定のエンゲージメントの種類はありますか？**クリック、いいね、シェアなど、さまざまなエンゲージメントの種類がある**と考えています。
Interviewer: Great question. Different reactions have different values on our platform. For example, liking a post is more valuable than only clicking it. Ideally, our system should consider major reactions when ranking posts. With that, I'll leave you to define "engagement" and choose what your model should optimize for.
面接官: いい質問ですね。異なる反応は私たちのプラットフォームで異なる価値を持っています。例えば、**投稿に「いいね」をすることは、単にクリックするよりも価値があります。理想的には、私たちのシステムは投稿をランク付けする際に主要な反応を考慮すべき**です。**それを踏まえて、「エンゲージメント」を定義**し、モデルが最適化すべきものを選んでください。

Candidate: What are the major reactions available on the platform? I assume users can click, like, share, comment, hide, block another user, and send connection requests. Are there other reactions we should consider?
候補者: **プラットフォームで利用可能な主要な反応は何ですか？**ユーザーはクリック、いいね、シェア、コメント、隠す、他のユーザーをブロックする、接続リクエストを送ることができると考えています。他に考慮すべき反応はありますか？
Interviewer: You mentioned the major ones. Let's keep our focus on those.
面接官: あなたが挙げた主要なものに焦点を当てましょう。

Candidate: How fast is the system supposed to work?
候補者: システムはどれくらいの速さで動作することが期待されていますか？
Interviewer: We expect the system to display the ranked posts quickly after users refresh their timelines or open the application. If it takes too long, users will get bored and leave. Let's assume the system should display the ranked posts in less than 200 milliseconds (ms).
面接官: ユーザーがタイムラインを更新したりアプリケーションを開いた後、システムが迅速にランク付けされた投稿を表示することを期待しています。時間がかかりすぎると、ユーザーは退屈して離れてしまいます。**システムは200ミリ秒（ms）未満でランク付けされた投稿を表示するべき**だと仮定しましょう。

Candidate: How many daily active users do we have? How many timeline updates do we expect each day?
候補者: 私たちには**どれくらいのデイリーアクティブユーザーがいますか？1日にどれくらいのタイムラインの更新を期待していますか？**
Interviewer: We have almost 3 billion users in total. Around 2 billion are daily active users who check their feeds twice a day.
面接官: 私たちは合計で約30億人のユーザーがいます。そのうち**約20億人がデイリーアクティブユーザーで、1日に2回フィードをチェックします**。

Let's summarize the problem statement. 
問題の要約をしましょう。
We are asked to design a personalized news feed system. 
私たちはパーソナライズされたニュースフィードシステムを設計するよう求められています。
The system retrieves unseen posts or posts with unseen comments, and ranks them based on how engaging they are to the user. 
システムは未表示の投稿または未表示のコメントを含む投稿を取得し、ユーザーにとってどれだけエンゲージングであるかに基づいてそれらをランク付けします。
This should take no longer than 200ms.
これには200ミリ秒を超えることはないはずです。
The objective of the system is to increase user engagement.
システムの目的は、ユーザーのエンゲージメントを増加させることです。

<!-- ここまで読んだ!  -->

### Frame the problem as an ML task 機械学習タスクとして問題を定義する 
 
#### Defining the ML objective 機械学習の目的を定義する

Let's examine the following three possible ML objectives:  
以下の3つの可能な機械学習の目的を検討します：

- Maximize the number of specific implicit reactions, such as dwell time or user clicks  
  特定の暗黙的反応の数を最大化する（例：滞在時間やユーザクリック）

- Maximize the number of specific explicit reactions, such as likes or shares  
  特定の明示的反応の数を最大化する（例：いいねやシェア）

- Maximize a weighted score based on both implicit and explicit reactions  
  暗黙的および明示的反応の両方に基づく加重スコアを最大化する

Let's discuss each option in more detail.  
それぞれの選択肢について、より詳細に議論しましょう。

Option 1: Maximize the number of specific implicit reactions, such as dwell time or user clicks  
**選択肢1：特定の暗黙的反応の数を最大化する（例：滞在時間やユーザクリック）**  
In this option, we choose implicit signals as a proxy for user engagement.  
この選択肢では、ユーザのエンゲージメントの代理として暗黙的信号を選択します。  
For example, we optimize the ML system to maximize user clicks.  
例えば、ユーザクリックを最大化するように機械学習システムを最適化します。
The advantage is that we have more data about implicit reactions than explicit ones.  
利点は、明示的な反応よりも暗黙的な反応に関するデータが多いことです。  
More training data usually leads to more accurate models.  
より多くのトレーニングデータは通常、より正確なモデルにつながります。  
The disadvantage is that implicit reactions do not always reflect a user's true opinion about a post.  
欠点は、暗黙的な反応が必ずしもユーザの投稿に対する真の意見を反映するわけではないことです。  
For example, a user may click on a post, but find it is not worth reading.  
例えば、ユーザが投稿をクリックすることはあっても、読む価値がないと感じることがあります。

Option 2: Maximize the number of specific explicit reactions, such as likes, shares, and hides  
**選択肢2：特定の明示的反応の数を最大化する（例：いいね、シェア、非表示）**
With this option, we choose explicit reactions as a proxy for user opinions about a post.
この選択肢では、投稿に対するユーザの意見の代理として明示的反応を選択します。  
The advantage of this approach is that explicit signals usually carry more weight than implicit signals.  
このアプローチの利点は、明示的信号が通常、暗黙的信号よりも重みを持つことです。  
For example, a user liking a post sends a stronger engagement signal than if they simply click it.  
例えば、ユーザが投稿に「いいね」をすることは、単にクリックするよりも強いエンゲージメント信号を送ります。  
The main disadvantage is that very few users actually express their opinions with explicit reactions.  
主な欠点は、実際に明示的反応で意見を表明するユーザが非常に少ないことです。  
For example, a user may find a post engaging but not react to it.  
例えば、ユーザが投稿を魅力的だと感じても、反応しないことがあります。  
In this scenario, it's hard for the model to make an accurate prediction given the limited training data.  
このシナリオでは、限られたトレーニングデータを考慮すると、モデルが正確な予測を行うのは難しいです。

Option 3: Maximize a weighted score based on both implicit and explicit reactions  
**選択肢3：暗黙的および明示的反応の両方に基づく加重スコアを最大化する**  
In this option, we use both implicit and explicit reactions to determine how engaged a user is with a post.  
この選択肢では、暗黙的および明示的反応の両方を使用して、ユーザが投稿にどれだけエンゲージしているかを判断します。  
In particular, we assign a weight to each reaction, based on how valuable the reaction is to us.  
**特に、私たちにとってその反応がどれだけ価値があるかに基づいて、各反応に重みを割り当てます。**  
We then optimize the ML system to maximize the weighted score of reactions.  
その後、反応の加重スコアを最大化するように機械学習システムを最適化します。  
Table 10.1 shows the mapping between different reactions and weights.  
表10.1は、異なる反応と重みの対応を示しています。
As you can see, pressing the "like" button has more weight than a click, while a share is more valuable than a like.  
ご覧のように、「いいね」ボタンを押すことはクリックよりも重みがあり、シェアは「いいね」よりも価値があります。 
In addition, negative reactions such as hide and block have a negative weight.  
さらに、非表示やブロックなどの否定的な反応には負の重みがあります。  
Note that these weights can be chosen based on business needs.  
**これらの重みは、ビジネスのニーズに基づいて選択できる**ことに注意してください。

![]()

Table 10.1: Weights of different reactions  
表10.1：異なる反応の重み  

Which option to choose?  
どの選択肢を選ぶべきか？  
We choose the final blended option because it allows us to assign different weights to different reactions.  
私たちは、異なる反応に異なる重みを割り当てることができるため、最終的なブレンドオプションを選択します。  
This is important because we can optimize the system based on what’s important to the business.  
これは、**ビジネスにとって重要なことに基づいてシステムを最適化できる**ため、重要です。

<!-- ここまで読んだ!  -->

#### Specifying the system’s input and output システムの入力と出力の指定

As Figure 10.2 shows, the personalized news feed system takes a user as input and outputs a ranked list of unseen posts or posts with unseen comments sorted by engagement score.
図10.2が示すように、パーソナライズされたニュースフィードシステムは、**ユーザを入力として受け取り、エンゲージメントスコアでソートされた未表示の投稿または未表示のコメントを持つ投稿のランク付けされたリストを出力**します。

![]()

#### Choosing the right ML category 適切なMLカテゴリの選択

A personalized news feed system produces a ranked list of posts based on how engaging the posts are to a user. 
パーソナライズされたニュースフィードシステムは、投稿がユーザにとってどれだけ魅力的であるかに基づいて、投稿のランク付けされたリストを生成します。
Pointwise Learning to Rank (LTR) is a simple yet effective approach that personalizes news feeds by ranking posts based on engagement scores. 
**Pointwise Learning to Rank (LTR)**は、エンゲージメントスコアに基づいて投稿をランク付けすることでニュースフィードをパーソナライズするシンプルでありながら効果的なアプローチです。(point-wiseだから、単に各投稿のスコアを予測して降順に並べるだけって話か...!:thinking:)
To understand how to compute engagement scores between users and posts, let's examine a concrete example. 
ユーザと投稿の間のエンゲージメントスコアを計算する方法を理解するために、具体的な例を見てみましょう。

As Figure 10.3 shows, we employ several binary classifiers to predict the probabilities of various implicit and explicit reactions for a ⟨user, post⟩ pair. 
図10.3に示すように、**私たちはいくつかのバイナリ分類器を使用して、⟨user, post⟩ペアに対するさまざまな暗黙的および明示的な反応の確率を予測**します。

![]()
Figure 10.3: Predicted probabilities of various reactions

Once these probabilities are predicted, we compute the engagement score. 
これらの確率が予測されると、エンゲージメントスコアを計算します。
Figure 10.4 shows an example of how the engagement score is calculated. 
図10.4は、エンゲージメントスコアがどのように計算されるかの例を示しています。

![]()
Figure 10.4: Calculate the engagement score 
図10.4: エンゲージメントスコアの計算

<!-- ここまで読んだ!  -->

### Data Preparation データ準備

#### Data engineering データエンジニアリング

It is generally helpful to understand what raw data is available before going on to engineer predictive features. 
**予測特徴量を設計する前に、どのような生データが利用可能であるかを理解することは一般的に有益**です。(うんうん...!:thinking:)
Here, we assume the following types of raw data are available: 
ここでは、以下の種類の生データが利用可能であると仮定します：

- Users ユーザ
- Posts 投稿
- User-post interactions ユーザ-投稿インタラクション
- Friendship 友情 (=あ、これはuser-userの関係性データか...)

##### Users ユーザ

The user data schema is shown below. 
ユーザデータスキーマは以下に示されています。

- id, username, Age, Gender, City, Country, Language, Timezone

![]()

Table 10.2: User data schema 
表10.2: ユーザデータスキーマ

##### Posts 投稿

Table 10.3 shows post data.
表10.3は投稿データを示しています。

- Author_id, Texual_content, Hashtags, Mentions, Images_or_videos, Timestamp

![Table 10.3: Post data]()
表10.3: 投稿データ

##### User-post interactions ユーザ-投稿インタラクション

Table 10.4 shows user-post interaction data. 
表10.4はユーザ-投稿インタラクションデータを示しています。

- User_id, Post_id, Interaction_type, Interaction_value, Location, Timestamp

![Table 10.4: User-post interaction data ]()
表10.4: ユーザ-投稿インタラクションデータ

##### Friendship 友情

The friendship table stores data of connections between users. 
友情テーブルは、ユーザ間の接続データを保存します。
We assume users can specify their close friends and family members. 
私たちは、ユーザが親しい友人や家族を指定できると仮定します。
Table 10.5 shows examples of friendship data. 
表10.5は友情データの例を示しています。

- user_id1, user_id2, time_when_friendship_was_formed, close_friend, family_member

![Table 10.5: Friendship data]()
表10.5: 友情データ

<!-- ここまで読んだ!  -->

#### Feature engineering 特徴量エンジニアリング

In this section, we engineer predictive features and prepare them for the model. 
このセクションでは、予測特徴量をエンジニアリングし、モデルのために準備します。
In particular, we engineer features from each of the following categories: 
特に、以下の各カテゴリから特徴量をエンジニアリングします：

- Post features
- User features
- User-author affinities

##### Post features 投稿の特徴

In practice, each post has many attributes. 
実際には、各投稿には多くの属性があります。
We cannot cover everything, so only discuss the most important ones. 
すべてをカバーすることはできないので、最も重要なものについてのみ議論します。

- Textual content
  - テキストコンテンツ
- Images or videos
  - 画像または動画
- Reactions
  - 反応
- Hashtags
  - ハッシュタグ
- Post's age
  - 投稿の年齢

###### Textual content

What is it? This is the textual content - the main body - of a post. 
これは何ですか？これは投稿のテキストコンテンツ - 本文 - です。
Why is it important? Textual content helps determine what the post is about. 
なぜ重要なのですか？テキストコンテンツは、投稿が何についてであるかを判断するのに役立ちます。
How to prepare it? We preprocess textual content and use a pre-trained language model to convert the text into a numerical vector. 
どのように準備しますか？私たちは**テキストコンテンツを前処理し、事前に学習した言語モデルを使用してテキストを数値ベクトルに変換**します。
Since the textual content is usually in the form of sentences and not a single word, we use a context-aware language model such as BERT [4]. 
テキストコンテンツは通常、単一の単語ではなく文の形であるため、BERT [4]のような文脈を考慮した言語モデルを使用します。

###### Images or videos

What is it? A post may contain images or videos. 
これは何ですか？投稿には画像や動画が含まれる場合があります。
Why is it important? We can extract important signals from images. 
なぜ重要なのですか？画像から重要な信号を抽出できます。
For example, an image of a gun may indicate that a post is unsafe for children. 
例えば、銃の画像は、その投稿が子供にとって安全でないことを示す可能性があります。
How to prepare it? First, preprocess the images or videos. 
どのように準備しますか？まず、画像や動画を前処理します。
Next, use a pre-trained model to convert the unstructured image/video data into an embedding vector. 
次に、**事前に学習したモデルを使用して、非構造化された画像/動画データを埋め込みベクトルに変換**します。(テキストや画像などの非構造化データは、やっぱり事前学習済みモデルを使うよなぁ...:thinking:)
For example, we can use ResNet, [5] or the recently introduced CLIP model [6] as the pre-trained model. 
例えば、ResNet [5]や最近導入されたCLIPモデル [6]を事前学習モデルとして使用できます。

###### Reactions

What is it? This refers to the number of likes, shares, replies, etc., of a post. 
これは何ですか？これは投稿の「いいね」や「シェア」、「返信」などの数を指します。
Why is it important? The number of likes, shares, hides, etc., indicates how engaging users find a post to be. 
**なぜ重要なのですか？「いいね」や「シェア」、「隠す」などの数は、ユーザ達がその投稿をどれだけ魅力的だと感じているかを示します。**
A user is more likely to engage with a post with thousands of likes than a post with ten likes. 
**ユーザーは、10の「いいね」が付いた投稿よりも、数千の「いいね」が付いた投稿に関与する可能性が高い**です。
How to prepare it? These values are represented by numerical values. 
どのように準備しますか？これらの値は数値で表されます。
We scale these numerical values to bring them into a similar range. 
これらの数値をスケーリングして、同様の範囲に持っていきます。(やっぱり数値特徴量は、この手順が必要なのか...!:thinking:)

###### Hashtags

Why is it important? Users use hashtags to group content around a certain topic. 
なぜ重要なのですか？ユーザーはハッシュタグを使用して、**特定のトピックに関連するコンテンツをグループ化**します。
These hashtags represent the topics to which a post relates. 
これらのハッシュタグは、投稿が関連するトピックを表します。
For example, a post with the hashtag "#women_in_tech" indicates the content relates to technology and females, so the model may decide to rank it higher for people who are interested in technology. 
例えば、ハッシュタグ「#women_in_tech」が付いた投稿は、その内容が技術と女性に関連していることを示しているため、モデルは技術に興味のある人々に対してそれをより高くランク付けすることを決定するかもしれません。
How to prepare it? The detailed steps to preprocess text are already explained in Chapter 4, YouTube Video Search, so we will only focus on the unique steps for preparing hashtags. 
どのように準備しますか？テキストの前処理に関する詳細な手順は第4章「YouTubeビデオ検索」で既に説明されているため、ハッシュタグの準備に特有の手順にのみ焦点を当てます。
(あ、ここでのハッシュタグはユーザ自身が自由に設定できる値のためカーディナリティが無限に増え得る。なのでentity embeddingではなくてsemanticなベクトル化が必要ってことね...!:thinking:)

- Tokenization: Hashtags like "lifeisgood" or "programmer_lifestyle" contain multiple words. 
- トークン化： "lifeisgood"や"programmer_lifestyle"のようなハッシュタグは複数の単語を含んでいます。
We use algorithms such as Viterbi [7] to tokenize the hashtags. 
私たちは、ハッシュタグをトークン化するためにViterbi [7]のようなアルゴリズムを使用します。
For instance, "lifeisgood" becomes 3 words: "life" "is" "good". 
例えば、"lifeisgood"は3つの単語に分かれます："life" "is" "good"。

- Tokens to IDs: Hashtags evolve quickly on social media platforms and change as trends come and go. 
- トークンからIDへ：ハッシュタグはソーシャルメディアプラットフォームで急速に進化し、トレンドが移り変わるにつれて変化します。
A feature hashing technique is a good fit because it is capable of assigning indexes to unseen hashtags. 
**特徴ハッシュ技術(feature hashing technique)**は、見たことのないハッシュタグにインデックスを割り当てることができるため、適しています。(??:thinking:)

- Vectorization: We use simple text representation methods such as TF-IDF [8] or word2vec [9], instead of Transformer-based models, to vectorize hashtags. 
- ベクトル化：私たちは、ハッシュタグをベクトル化するために、Transformerベースのモデルの代わりにTF-IDF [8]やword2vec [9]のようなシンプルなテキスト表現方法を使用します。
Let's take a look at why. 
なぜか見てみましょう。
Transformer-based models are useful when the context of the data is essential. 
Transformerベースのモデルは、データの文脈が重要な場合に役立ちます。
In the case of hashtags, each one is usually a single word or a phrase, and often no context is necessary to understand what the hashtag means. 
**ハッシュタグの場合、各ハッシュタグは通常単一の単語またはフレーズであり、ハッシュタグの意味を理解するために文脈はしばしば必要ありません**。
Therefore, faster and lighter text representation methods are preferred. 
**したがって、より速く軽量なテキスト表現方法が好まれます。**(なるほど...!:thinking:)

<!-- ここまで読んだ!  -->

###### Post's age

What is it? This feature shows how much time has passed since the author posted the content. 
これは何ですか？この特徴は、**著者がコンテンツを投稿してからどれだけの時間が経過したか**を示します。
Why is it important? Users tend to engage with newer content. 
なぜ重要なのですか？ユーザーは新しいコンテンツに関与する傾向があります。
How to prepare it? We bucketize the post's age into a few categories and use one-hot encoding to represent it. 
どのように準備しますか？**私たちは投稿の年齢をいくつかのカテゴリに分け、one-hotエンコーディングを使用して表現**します。
For example, we use the following buckets: 
例えば、次のバケットを使用します: 

- 0: less than 1 hour
- 0: 1時間未満
- 1: between 1 to 5 hours
- 1: 1〜5時間の間
- 2: between 5 to 24 hours
- 2: 5〜24時間の間
- 3: between 1-7 days
- 3: 1〜7日の間
- 4: between 7-30 days
- 4: 7〜30日の間
- 5: more than a month
- 5: 1ヶ月以上

- 思ったことメモ
  - ふーん。そのまま数値特徴量として扱うよりも、バケット化した方が良かったりするのかも...??:thinking:
  - バケット化してカテゴリ特徴量扱いしちゃった方が、モデルが「区切り」を意識しやすくなって良いっぽい。特に必ずしも線形に影響しない場合とか。
    - Tree系モデルとかは特に顕著らしい。
    - NN系モデルのそもそも“連続値”の特徴量をうまく学習できるらしいので、全ての場合でバケット化する必要があるわけではないっぽい。

![Figure 10.5: Post-related feature preparation]()

<!-- ここまで読んだ!  -->

##### User features ユーザ特徴

Some of the most important user-related features are:
ユーザに関連する最も重要な特徴のいくつかは次のとおりです：

- Demographics: age, gender, country, etc
  - 人口統計：年齢、性別、国など
- Contextual information: device, time of the day, etc
  - コンテキスト情報：デバイス、時間帯など
- User-post historical interactions
  - ユーザと投稿の過去の相互作用
- Being mentioned in the post
  - 投稿で言及されること

Since we have already discussed user demographic and contextual information in previous chapters, here we only examine the remaining two features.
前の章でユーザの人口統計とコンテキスト情報についてすでに議論したので、ここでは残りの2つの特徴のみを検討します。

###### User-post historical interactions ユーザと投稿の過去の相互作用

All posts liked by a user are represented by a list of post IDs. The same logic applies to shares and comments.
**ユーザが「いいね」したすべての投稿は、投稿IDのリストで表されます**。同じ論理がシェアやコメントにも適用されます。
Why is it important? Users' previous engagements are usually helpful in determining their future engagements.
なぜ重要なのか？**ユーザの過去の関与は、通常、将来の関与を決定するのに役立ちます。**
How to prepare it? Extract features from each post that the user interacted with.
どのように準備するのか？ユーザが相互作用した各投稿から特徴を抽出します。

###### Being mentioned in a post

What is it? This means whether or not the user is mentioned in a post.
それは何か？これは、ユーザが投稿で言及されているかどうかを意味します。
Why is it important? Users usually pay more attention to posts that mention them.
なぜ重要なのか？ユーザは通常、自分が言及されている投稿により多くの注意を払います。
How to prepare it? This feature is represented by a binary value. If a user is mentioned in the post, this feature is 1, otherwise 0.
どのように準備するのか？この特徴はバイナリ値で表されます。ユーザが投稿で言及されている場合、この特徴は1、そうでない場合は0です。
Figure 10.6 summarizes feature preparation for users.
図10.6は、ユーザのための特徴準備を要約しています。

![Figure 10.6: Feature preparation for user-related data]()

<!-- ここまで読んだ!  -->

##### User-author affinities ユーザと著者の親和性

According to studies, affinity features, such as the connection between the user and the author, are among the most important factors in predicting a user's engagement on Facebook [10]. 
研究によると、**ユーザと著者の関係などの親和性特徴量は、Facebookにおけるユーザのエンゲージメントを予測する上で最も重要な要素の一つです**[10]。 
Let's engineer some features to capture user-author affinities. 
ユーザと著者の親和性を捉えるための特徴を設計しましょう。

###### Like/click/comment/share rate

This is the rate at which a user reacted to previous posts by an author. 
これは、**ユーザが著者の以前の投稿に反応した割合**です。
For example, a like rate of 0.95 indicates that a user liked the posts from that author 95 percent of the time. 
例えば、いいね率が0.95であれば、ユーザはその著者の投稿を95％の確率で好んだことを示します。

###### Length of friendship

The number of days the user and the author have been friends on the platform. 
ユーザと著者がプラットフォーム上で友達であった日数です。 
This feature can be obtained from the friendship data. 
この特徴は、友達データから取得できます。
Why is it important? 
なぜ重要なのでしょうか？ 
Users tend to engage more with their friends. 
ユーザは友達とのエンゲージメントが高くなる傾向があります。

###### Close friends and family

A binary value representing whether the user and the author have included each other in their close friends and family list. 
ユーザと著者が互いに親しい友人や家族リストに含めているかどうかを示す二値の値です。 
Why is it important? 
なぜ重要なのでしょうか？ 
Users pay more attention to posts by close friends and family members. 
ユーザは親しい友人や家族の投稿により多くの注意を払います。 
Figure10.710.710.7summarizes features related to user-author affinities. 
図10.710.710.7は、ユーザと著者の親和性に関連する特徴を要約しています。

![Figure 10.7: User-author affinity features]()

### Model Development モデル開発  

#### Model selection モデル選択

We choose neural networks for the following reasons:  
私たちは以下の理由からニューラルネットワークを選択します：

- Neural networks work well with unstructured data, such as text and images.  
  - ニューラルネットワークは、テキストや画像などの非構造化データに対してうまく機能します。
- Neural networks allow us to use embedding layers to represent categorical features.  
  - **ニューラルネットワークは、カテゴリカル特徴を表現するために埋め込み層を使用することを可能にします**。
- With a neural network architecture, we can fine-tune pre-trained models employed during feature engineering. This is not possible with other models.  
  - **ニューラルネットワークアーキテクチャを使用することで、特徴エンジニアリング中に使用される事前学習モデルをファインチューニングできます。これは他のモデルでは不可能です**。(なるほどね...!:thinking:)

Before training a neural network, we need to choose its architecture.  
ニューラルネットワークをトレーニングする前に、そのアーキテクチャを選択する必要があります。  
There are two architectural options for building and training our neural networks:  
私たちのニューラルネットワークを構築しトレーニングするための2つのアーキテクチャオプションがあります：

- N independent DNNs  
  - N個の独立したDNN
- A multi-task DNN  
  - マルチタスクDNN

Let’s explore each one.  
それぞれを見ていきましょう。


##### Option 1: N independent DNNs   オプション1：N個の独立したDNN  

In this option, we use N independent deep neural networks (DNN), one for each reaction. This is shown in Figure 10.8.  
このオプションでは、各反応に対して1つのN個の独立した深層ニューラルネットワーク（DNN）を使用します。これは図10.8に示されています。

![Figure 10.8: Using independent DNNs]()

This option has two drawbacks:  
このオプションには2つの欠点があります：

- Expensive to train. Training several independent DNNs is compute-intensive and time-consuming.  
  - トレーニングに高コストがかかります。複数の独立したDNNをトレーニングすることは計算集約的で時間がかかります。
- For less frequent reactions, there might not be enough training data. This means our system is not able to predict the probabilities of infrequent reactions accurately.  
  - 発生頻度の低い反応に対しては、十分なトレーニングデータがない可能性があります。これは、私たちのシステムが稀な反応の確率を正確に予測できないことを意味します。

<!-- ここまで読んだ!  -->

##### Option 2: Multi-task DNN オプション2：マルチタスクDNN

To overcome these issues, we use a multi-task learning approach (Figure 10.9).  
これらの問題を克服するために、私たちはマルチタスク学習アプローチを使用します（図10.9）。  
(ちゃんとわかってないけど、図を見るに、中間層をshareしてる感じ!:thinking:)

![Figure 10.9: Multi-task DNN]()

We explained multi-task learning in Chapter 5, Harmful Content Detection, so we only briefly discuss it here.  
私たちは第5章「有害コンテンツ検出」でマルチタスク学習について説明したので、ここでは簡単に触れるだけにします。 
In summary, multi-task learning refers to the process of learning multiple tasks simultaneously.  
要約すると、マルチタスク学習は複数のタスクを同時に学習するプロセスを指します。  
This allows the model to learn the similarities between tasks and avoid unnecessary computations.  
これにより、モデルはタスク間の類似性を学習し、不必要な計算を回避できます。  
For a multi-task neural network model, it's essential to choose an appropriate architecture.  
マルチタスクニューラルネットワークモデルでは、適切なアーキテクチャを選択することが重要です。 
The choice of architecture and the associated hyperparameters are usually determined by running experiments.
**アーキテクチャの選択と関連するハイパーパラメータは、通常、実験を実施することによって決定されます**。  
That means training and evaluating the model on different architectures and choosing the one which leads to the best result.  
つまり、異なるアーキテクチャでモデルをトレーニングおよび評価し、最良の結果をもたらすものを選択することを意味します。

<!-- ここまで読んだ!  -->

##### Improving the DNN architecture for passive users 受動的なユーザーのためのDNNアーキテクチャの改善

So far, we have employed a DNN to predict reactions such as shares, likes, clicks, and comments. 
これまで、私たちはDNNを使用して、シェア、いいね、クリック、コメントなどの反応を予測してきました。しかし、Many users use the platform passively, meaning they do not interact much with the content on their timelines. 
**多くのユーザーはプラットフォームを受動的に使用しており、タイムライン上のコンテンツとあまり相互作用しません。**そのため、For such users, the current DNN model will predict very low probabilities for all reactions, since they rarely react to posts. 
そのようなユーザーに対して、現在のDNNモデルはすべての反応に対して非常に低い確率を予測します。なぜなら、彼らは投稿に対してほとんど反応しないからです。Therefore, we need to change the DNN architecture to consider passive users. 
したがって、受動的なユーザーを考慮するためにDNNアーキテクチャを変更する必要があります。

For this to work, we add two implicit reactions to the list of tasks:
これを実現するために、**タスクのリストに2つの暗黙的な反応を追加**します：
(implicit feedkbackを追加する感じか...!:thinking:)

- Dwell-time: the time a user spends on a post.
  - Dwell-time（滞在時間）：ユーザーが投稿に費やす時間。
- Skip: if a user spends less than t seconds (e.g.,0.50.50.5seconds) on a post, then that post can be assumed to have been skipped by the user.
  - Skip（スキップ）：ユーザーが投稿にt秒未満（例：0.5秒）を費やした場合、その投稿はユーザーによってスキップされたと見なすことができます。

Figure 10.10 shows the multi-task DNN model with the additional tasks.
図10.10は、追加のタスクを持つマルチタスクDNNモデルを示しています。

![Figure 10.10: Multi-task DNN model with two new tasks]()

#### Model training モデル訓練  

##### Constructing the dataset データセットの構築

In this step, we construct the dataset from raw data. 
このステップでは、生データからデータセットを構築します。 
Since the DNN model needs to learn multiple tasks, positive and negative data points are created for each (e g., click, like, etc.) 
DNNモデルは複数のタスクを学習する必要があるため、各タスク（例：クリック、いいねなど）に対して正のデータポイントと負のデータポイントが作成されます。
(正例と負例を用意する必要があるってことね!:thinking:)

We will use the reaction type of "like" as an example to explain how to create positive/negative data points. 
「いいね」という反応タイプを例にして、**正のデータポイントと負のデータポイントの作成方法**を説明します。
Each time a user likes a post, we add a data point to our dataset, compute $\langle\langle user, post \rangle\rangle$ features, and then label it as positive. 
ユーザーが投稿に「いいね」をするたびに、データセットにデータポイントを追加し、$\langle\langle user, post \rangle\rangle$特徴を計算し、それを正のラベルとして付けます。
To create negative data points, we chose impressions that didn't lead to a "like" reaction. 
**負のデータポイントを作成するために、「いいね」反応につながらなかったインプレッションを選びます**。
Note that the number of negative data points is usually much higher than positive data points. 
**負のデータポイントの数は通常、正のデータポイントよりもはるかに多いことに注意**してください。
To avoid having an imbalanced dataset, we create negative data points to equal the number of positive data points. 
不均衡なデータセットを避けるために、**正のデータポイントの数と等しくなるように負のデータポイントを作成**します。
Figure 10.11 shows positive and negative data points for the "like" reaction. 
図10.11は、「いいね」反応に対する正のデータポイントと負のデータポイントを示しています。

![Figure 10.11: Training data for like classification task]()

This same process can be used to create positive and negative labels for other reactions. 
このプロセスは、他の反応に対して正のラベルと負のラベルを作成するためにも使用できます。
However, because dwell-time is a regression task, we construct it differently. 
**ただし、滞在時間は回帰タスクであるため、異なる方法で構築します**。(なるほど確かに...!:thinking:)
As shown in Figure 10.12, the ground truth label is the dwell-time of the impression. 
図10.12に示すように、グラウンドトゥルースラベルはインプレッションの滞在時間です。

![Figure 10.12: Training data for dwell-time task]()

<!-- ここまで読んだ!  -->

##### Choosing the loss function 損失関数の選択

Multi-task models are trained to learn multiple tasks simultaneously. 
**マルチタスクモデルは、複数のタスクを同時に学習するように訓練**されます。 
This means we need to compute the loss for each task separately and then combine them to get an overall loss. 
これは、**各タスクの損失を個別に計算し、それらを組み合わせて全体の損失を得る必要があること**を意味します。
(なるほどかなりシンプルでわかりやすい...!:thinking:)
Typically, we define a loss function for each task depending on the ML category of the task. 
通常、**タスクの機械学習（ML）カテゴリに応じて、各タスクのための損失関数を定義**します。 
In our case, we use a binary cross-entropy loss for each binary classification task, and a regression loss such as MAE [11], MSE [12], or Huber loss [13] for the regression task (dwell-time prediction). 
**私たちの場合、各バイナリ分類タスクにはバイナリ交差エントロピー損失を使用し、回帰タスク（滞在時間予測）にはMAE [11]、MSE [12]、またはHuber損失 [13]などの回帰損失を使用します。**
The overall loss is computed by combining task-specific losses, as shown in Figure 10.13. 
全体の損失は、図10.13に示すように、タスク固有の損失を組み合わせることによって計算されます。

$$
Loss = \lambda L_{dwell} + L_{skip} + L_{like} + \ldots + L_{share}
$$

(あ、ここでの$\lambda$は、dwell-timeの予測タスクだけ回帰タスクだから、他の分類タスクとスケールを合わせるための重み付けパラメータってことね...!:thinking:)

<!-- ここまで読んだ!  -->

### Evaluation 評価

#### Offline metrics オフライン指標

During the offline evaluation, we measure the performance of our model in predicting different reactions.  
**オフライン評価中に、私たちは異なる反応を予測する際のモデルの性能を測定**します。  
To evaluate the performance of an individual type of reaction, we can use binary classification metrics, such as precision and recall.  
特定の反応タイプの性能を評価するために、精度や再現率などの二項分類指標を使用できます。  
However, these metrics alone may not be sufficient to understand the overall performance of a binary classification model.  
しかし、これらの指標だけでは、二項分類モデルの全体的な性能を理解するには不十分な場合があります。
So, we use the ROC curve to understand the trade-off between the true positive rate and false positive rate.
そのため、真陽性率と偽陽性率のトレードオフを理解するためにROC曲線を使用します。  
In addition, we compute the area under the ROC curve (ROC-AUC) to summarize the performance of the binary classification with a numerical value.
さらに、ROC曲線の下の面積（ROC-AUC）を計算して、二項分類の性能を数値で要約します。

<!-- ここまで読んだ!  -->

#### Online metrics オンライン指標

We use the following metrics to measure user engagement from various angles:  
私たちは、さまざまな角度からユーザーエンゲージメントを測定するために、以下の指標を使用します:

- Click-through rate (CTR)  
  - クリック率 (CTR)  
- Reaction rate  
  - 反応率  
- Total time spent  
  - 合計滞在時間  
- User satisfaction rate found in a user survey  
  - ユーザー調査で得られたユーザー満足度  

##### CTR. 

The ratio between the number of clicks and impressions.  
CTR. クリック数とインプレッション数の比率です。 

$$
CTR = \frac{\text{number of clicked posts}}{\text{number of impressions}} 
$$  

A high CTR does not always indicate more user engagement.  
**高いCTRは必ずしもユーザーエンゲージメントが高いことを示すわけではありません。**
For example, users may click on a low-value clickbait post, and quickly realize it is not worth reading.  
例えば、ユーザーは低価値のクリックベイト投稿をクリックし、すぐに読む価値がないことに気づくかもしれません。  
Despite this limitation, it is an important metric to track.
この制限にもかかわらず、これは追跡すべき重要な指標です。(なんで??:thinking:)

##### Reaction rates. 

These are a set of metrics that reflect user reactions.  
反応率。これはユーザーの反応を反映する一連の指標です。  
For example, a like rate measures the ratio between posts liked and the total number of posts displayed in users' feeds.  
例えば、いいね率は、いいねされた投稿の数とユーザーのフィードに表示された投稿の総数の比率を測定します。

$$
\text{Like rate} = \frac{\text{number of liked posts}}{\text{number of impressions}} 
$$  

Similarly, we track other reactions such as "share rate", "comment rate", "hide rate", "block rate", and "skip rate".  
同様に、「シェア率」、「コメント率」、「非表示率」、「ブロック率」、「スキップ率」などの他の反応も追跡します。
These are stronger signals than CTR, as users have explicitly expressed a preference.  
これらは、ユーザーが明示的に好みを表現しているため、CTRよりも強い信号です。  

<!-- ここまで読んだ!  -->

The metrics we discussed so far are based on user reactions.  
これまでに議論した指標は、ユーザーの反応に基づいています。  
But what about passive users?
しかし、受動的なユーザーはどうでしょうか？
These are users who tend not to react at all to the majority of posts.  
これらは、ほとんどの投稿に対してまったく反応しない傾向のあるユーザーです。  
To capture the effectiveness of our personalized news feed system for passive users, we add the following two metrics.  
受動的なユーザーに対する私たちのパーソナライズされたニュースフィードシステムの効果を捉えるために、次の2つの指標を追加します。  

- Total time spent. This is the total time users spend on the timeline during a fixed period, such as 1 week.  
**合計滞在時間。これは、ユーザーが1週間などの固定期間中にタイムラインで過ごす合計時間**です。  
This metric measures the overall engagement of both passive and active users.  
この指標は、受動的および能動的なユーザーの全体的なエンゲージメントを測定します。  

- User satisfaction rate found in a user survey.  
ユーザー調査で得られたユーザー満足度。  
Another way to measure the effectiveness of our personalized news feed system is to explicitly ask users for their opinion about the feed, or how engaging they find the posts.  
私たちのパーソナライズされたニュースフィードシステムの効果を測定する別の方法は、フィードについてのユーザーの意見や、投稿がどれだけ魅力的であると感じているかを明示的に尋ねることです。  
Since we seek explicit feedback, this is an accurate way to measure the system’s effectiveness.  
明示的なフィードバックを求めているため、これはシステムの効果を測定する正確な方法です。  (なるほどね〜ユーザインタビュー的な...!:thinking:)

<!-- ここまで読んだ!  -->

### Serving サービング

At serving time, the system serves requests by outputting a ranked list of posts. 
サービング時に、システムはリクエストに応じて投稿のランク付けされたリストを出力します。
Figure 10.14 shows the architectural diagram of the personalized news feed system. 
図10.14は、パーソナライズされたニュースフィードシステムのアーキテクチャ図を示しています。

The system comprises the following pipelines: 
システムは以下のパイプラインで構成されています：

- Data preparation pipeline 
  - データ準備パイプライン(=つまりFeature Pipeline!:thinking:)
- Prediction pipeline 
  - 予測パイプライン

We do not go into detail about the data preparation pipeline because it is very similar to that described in Chapter 8, Ad Click Prediction in Social Platforms. 
データ準備パイプラインについては、Chapter 8の「Social Platformsにおける広告クリック予測」で説明されているものと非常に似ているため、詳細には触れません。
Let’s examine the prediction pipeline. 
予測パイプラインを見てみましょう。

<!-- ここまで読んだ!  -->

#### Prediction pipeline 予測パイプライン

The prediction pipeline consists of the following components: retrieval service, ranking service, and re-ranking service.
予測パイプラインは、以下のコンポーネントで構成されています：retrieval service（取得サービス）、ranking service（ランキングサービス）、およびre-ranking service（再ランキングサービス）。

##### Retrieval service 取得サービス

This component retrieves posts that a user has not seen, or which have comments also unseen by them. 
このコンポーネントは、ユーザがまだ見ていない投稿や、ユーザがまだ見ていないコメントがある投稿を取得します。
To learn more about efficiently fetching unseen posts, read [14]. 
未見の投稿を効率的に取得する方法については、[14]を参照してください。
(ref14 = [Design a News Feed System](https://liuzhenglaichn.gitbook.io/system-design/news-feed/design-a-news-feed-system))

##### Ranking service ランキングサービス

This component ranks the retrieved posts by assigning an engagement score to each one.
このコンポーネントは、取得した投稿にエンゲージメントスコアを割り当てることによって、それらをランク付けします。

##### Re-ranking service 再ランキングサービス

This service modifies the list of posts by incorporating additional logic and user filters. 
このサービスは、追加のロジックとユーザーフィルターを組み込むことによって、投稿のリストを修正します。
For example, if a user has explicitly expressed interest in a certain topic, such as soccer, this service assigns a higher rank to the post.
例えば、ユーザーがサッカーのような特定のトピックに明示的に興味を示した場合、このサービスはその投稿により高いランクを割り当てます。

<!-- ここまで読んだ!  -->

### Other Talking Points その他の話題

If there is time left at the end of the interview, here are some additional talking points:
インタビューの最後に時間が残っている場合、以下の追加の話題があります：

- How to handle posts that are going viral [15].
  - バイラルな投稿をどのように扱うか [15]。
- How to personalize the news feed for new users [16].
  - 新しいユーザーのためにニュースフィードをどのようにパーソナライズするか [16]。
  - (一応デモグラがあるからOKじゃない?? 履歴のlist[news id]は空っぽになるだけで推論はできるし...!:thinking:)
- How to mitigate the positional bias present in the system [17].
  - システムに存在する位置バイアスをどのように軽減するか [17]。
  - (これは確かに言及されてないね! まあシンプルなのは、カスケードモデルの仮定を置いたりすることかなぁ...:thinking:)
- How to determine a proper retraining frequency [18].
  - 適切な再学習の頻度をどのように決定するか [18]。
    - (まあ再学習のコスト次第かな...。基本的には継続的学習した方が成果は出ると思うし...!:thinking:)

### References 参考文献

1. News Feed ranking in Facebook. https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/.  
   Facebookにおけるニュースフィードのランキング。

2. Twitter’s news feed system. https://blog.twitter.com/engineering/en_us/topics/insights/2017/using-deep-learning-at-scale-in-twitters-timelines.  
   Twitterのニュースフィードシステム。

3. LinkedIn’s News Feed system LinkedIn. https://engineering.linkedin.com/blog/2020/understanding-feed-dwell-time.  
   LinkedInのニュースフィードシステム。

4. BERT paper. https://arxiv.org/pdf/1810.04805.pdf.  
   BERTに関する論文。

5. ResNet model. https://arxiv.org/pdf/1512.03385.pdf.  
   ResNetモデル。

6. CLIP model. https://openai.com/blog/clip/.  
   CLIPモデル。

7. Viterbi algorithm. https://en.wikipedia.org/wiki/Viterbi_algorithm.  
   Viterbiアルゴリズム。

8. TF-IDF. https://en.wikipedia.org/wiki/Tf%E2%80%93idf.  
   TF-IDF。

9. Word2vec. https://en.wikipedia.org/wiki/Word2vec.  
   Word2vec。

10. Serving a billion personalized news feed. https://www.youtube.com/watch?v=Xpx5RYNTQvg.  
    10億のパーソナライズされたニュースフィードの提供。

11. Mean absolute error loss. https://en.wikipedia.org/wiki/Mean_absolute_error.  
    平均絶対誤差損失。

12. Means squared error loss. https://en.wikipedia.org/wiki/Mean_squared_error.  
    平均二乗誤差損失。

13. Huber loss. https://en.wikipedia.org/wiki/Huber_loss.  
    Huber損失。

14. A news feed system design. https://liuzhenglaichn.gitbook.io/system-design/news-feed/design-a-news-feed-system.  
    ニュースフィードシステムの設計。

15. Predict viral tweets. https://towardsdatascience.com/using-data-science-to-predict-viral-tweets-615b0acc2e1e.  
    バイラルツイートを予測する。

16. Cold start problem in recommendation systems. https://en.wikipedia.org/wiki/Cold_start_(recommender_systems).  
    推薦システムにおけるコールドスタート問題。

17. Positional bias. https://eugeneyan.com/writing/position-bias/.  
    位置バイアス。

18. Determine retraining frequency. https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html#towards-continual-learning.  
    再訓練の頻度を決定する。

