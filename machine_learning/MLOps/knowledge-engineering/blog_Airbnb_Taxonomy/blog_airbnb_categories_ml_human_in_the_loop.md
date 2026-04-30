refs: https://medium.com/airbnb-engineering/building-airbnb-categories-with-ml-and-human-in-the-loop-e97988e70ebb


# Building Airbnb Categories with ML and human-in-the-loop
AirbnbのカテゴリをMLと人間の介入を用いて構築する

## Airbnb Categories blog series — Part I Airbnbカテゴリブログシリーズ — パートI

By: Mihajlo Grbovic, Ying Xiao, Pratiksha Kadam, Aaron Yin, Pei Xiong, Dillon Davis, Aditya Mukherji, Kedar Bellare, Haowei Zhang, Shukun Yang, Chen Qian, Sebastien Dubois, Nate Ney, James Furnary, Mark Giangreco, Nate Rosenthal, Cole Baker, Bill Ulammandakh, Sid Reddy, Egor Pakhomov
著者: Mihajlo Grbovic, Ying Xiao, Pratiksha Kadam, Aaron Yin, Pei Xiong, Dillon Davis, Aditya Mukherji, Kedar Bellare, Haowei Zhang, Shukun Yang, Chen Qian, Sebastien Dubois, Nate Ney, James Furnary, Mark Giangreco, Nate Rosenthal, Cole Baker, Bill Ulammandakh, Sid Reddy, Egor Pakhomov

Nov 22, 2022
2022年11月22日

## 25 years of online travel search 25年間のオンライン旅行検索

Online travel search hasn’t changed much in the last 25 years. 
オンライン旅行検索は、過去25年間あまり変わっていません。
The traveler enters her destination, dates, and the number of guests into a search interface, which dutifully returns a list of options that best meet the criteria. 
旅行者は、目的地、日付、ゲストの人数を検索インターフェースに入力し、それに基づいて最も適したオプションのリストが返されます。
Eventually, Airbnb and other travel sites made improvements to allow for better filtering, ranking, personalization and, more recently, to display results slightly outside of the specified search parameters–for example, by accommodating flexible dates or by suggesting nearby locations. 
最終的に、Airbnbや他の旅行サイトは、より良いフィルタリング、ランキング、パーソナライズを可能にする改善を行い、最近では、指定された検索パラメータの少し外側の結果を表示するようになりました。例えば、柔軟な日付に対応したり、近隣の場所を提案したりします。
Taking a page from the travel agency model, these websites also built more “inspirational” browsing experiences that recommend popular destinations, showcasing these destinations with captivating imagery and inventory (think digital “catalog”). 
旅行代理店モデルを参考にして、これらのウェブサイトは人気のある目的地を推薦する「インスピレーショナル」なブラウジング体験を構築し、魅力的な画像や在庫を使ってこれらの目的地を紹介しています（デジタル「カタログ」を考えてみてください）。

The biggest shortcoming of these approaches is that the traveler must have a specific destination in mind. 
**これらのアプローチの最大の欠点は、旅行者が特定の目的地を考えている必要があること**です。
(=> 要するに、従来の検索って「場所ありき」だよねって話。目的地を先に決めないと検索できない。ex. 「沖縄行きたい」「パリ行きたい」みたいな感じ...!!:thinking:)
Even travelers who are flexible get funneled to a similar set of well-known destinations, reinforcing the cycle of mass tourism. 
**例え予定(=場所など!)が柔軟な旅行者であっても、結局は似たような有名な観光地への誘導されてしまい、結果としてマスツーリズム(大衆観光)の循環がさらに強まってしまう。**

<!-- ここまで読んだ! -->

## Introducing Airbnb Categories Airbnbカテゴリの紹介

In our recent release, we flipped the travel search experience on its head by having the inventory dictate the destinations, not the other way around. 
私たちの最近のリリースでは、**在庫が目的地を決定することで旅行検索体験を一新**しました。逆ではありません。
In this way, we sought to inspire the traveler to book unique stays in places they might not think to search for. 
このようにして、私たちは**旅行者が検索しようと思わないようなユニークな宿泊先を予約するように促しました**。
By leading with our unique places to stay, grouped together into cohesive “categories”, we inspired our guests to find some incredible places to stay off the beaten path. 
**ユニークな宿泊先を「カテゴリ」としてまとめて提示することで、私たちはゲストに人里離れた素晴らしい宿泊先を見つけるように促しました。** (いいね! まさにユーザのガイドだ...!!:thinking:)

Though our goal was an intuitive browsing experience, it required considerable work behind the scenes to pull this off. 
私たちの目標は直感的なブラウジング体験でしたが、これを実現するためには裏でかなりの作業が必要でした。
In this three-part series, we will pull back the curtain on the technical aspects of the Airbnb 2022 Summer Launch. 
この三部構成のシリーズでは、Airbnb 2022年夏のローンチの技術的側面を明らかにします。

- Part I(this post) is designed to be a high-level introductory post about how we applied machine learning to build out the listing collections and to solve different tasks related to the browsing experience–specifically, quality estimation, photo selection and ranking. 
  - パートI（この投稿）は、機械学習をどのように適用してリスティングコレクションを構築し、ブラウジング体験に関連するさまざまなタスク、具体的には品質評価、写真選択、ランキングを解決したかについての高レベルの紹介投稿です。

- Part II of the series focuses on ML Categorization of listings into categories. 
  - シリーズのパートIIは、リスティングをカテゴリに分類するML（機械学習）分類に焦点を当てています。
    It explains the approach in more detail, including signals and labels that we used, tradeoffs we made, and how we set up a human-in-the-loop feedback system. 
    それは、私たちが使用した信号やラベル、私たちが行ったトレードオフ、そして人間のフィードバックシステムをどのように設定したかについて、より詳細に説明します。

- Part III focuses on ML Ranking of Categories depending on the search query. 
  - パートIIIは、検索クエリに応じたカテゴリのML（機械学習）ランキングに焦点を当てています。
    For example, we taught the model to show the Skiing category first for an Aspen, Colorado query versus Beach/Surfing for a Los Angeles query. 
    例えば、コロラド州アスペンのクエリに対してスキーカテゴリを最初に表示し、ロサンゼルスのクエリに対してはビーチ/サーフィンを表示するようにモデルに教えました。
    That post will also cover our approach for ML Ranking of listings within each category. 
    その投稿では、各カテゴリ内のリスティングのMLランキングに対する私たちのアプローチについても説明します。

<!-- ここまで読んだ! -->

## Grouping listings into Categories カテゴリへのリスティングのグループ化

(listing = Airbnb上に掲載されてる個々の宿泊先のこと。要するにアイテム的なイメージ...!:thinking:)

Airbnb has thousands of very unique, high quality listings, many of which received design and architecture awards or have been featured in travel magazines or movies. 
Airbnbには非常にユニークで高品質なリスティングが数千件あり、その多くはデザインや建築の賞を受賞したり、旅行雑誌や映画に取り上げられたりしています。**しかし、これらのリスティングは、あまり知られていない町にあるためや、予約を最適化する検索アルゴリズムによって十分に高く評価されていないため、発見が難しいことがあります。** 
While these unique listings may not always be as bookable as others due to lower availability or higher price, they are great for inspiration and for helping guests discover hidden destinations where they may end up booking a stay influenced by the category.
これらのユニークなリスティングは、利用可能性が低かったり価格が高かったりするために他のリスティングほど予約可能でないこともありますが、インスピレーションを得るためや、ゲストがカテゴリに影響されて予約をするかもしれない隠れた目的地を発見するのに役立ちます。

To showcase these special listings we decided to group them into collections of homes organized by what makes them unique. 
これらの特別なリスティングを紹介するために、私たちは**それらをユニークな特徴に基づいて整理されたホームのコレクションにグループ化する**ことに決めました。 
The result was Airbnb Categories, collections of homes revolving around some common themes including the following: 
その結果、Airbnb Categoriesが生まれ、以下のような共通のテーマに基づくホームのコレクションが作成されました：

- Categories that revolve around a location or a place of interest (POI) such as Coastal, Lake, National Parks, Countryside, Tropical, Arctic, Desert, Islands, etc. 
  - **場所や観光名所（POI）に関連するカテゴリ**、例えば海岸、湖、国立公園、田舎、熱帯、北極、砂漠、島など。
- Categories that revolve around an activity such as Skiing, Surfing, Golfing, Camping, Wine tasting, Scuba, etc. 
  - スキー、サーフィン、ゴルフ、キャンプ、ワインテイスティング、スキューバなどの**アクティビティに関連するカテゴリ。**
- Categories that revolve around a home type such as Barns, Castles, Windmills, Houseboats, Cabins, Caves, Historical, etc. 
  - 納屋、城、風車、ハウスボート、キャビン、洞窟、歴史的なものなどの**ホームタイプに関連するカテゴリ**。
- Categories that revolve around a home amenity such as Amazing Pools, Chef’s Kitchen, Grand Pianos, Creative Spaces, etc. 
  - 驚くべきプール、シェフのキッチン、グランドピアノ、**クリエイティブスペースなどのホームアメニティに関連するカテゴリ**。

(まさに直交する複数のtaxonomy達があるイメージ...!!:thinking:)

We defined 56 categories and outlined the definition for each category. 
私たちは56のカテゴリを定義し、それぞれのカテゴリの定義を概説しました。 
Now all that was left to do was to assign our entire catalog of listings to categories. 
今残っているのは、私たちの**全リスティングカタログをカテゴリに割り当てることだけ**でした。

<!-- ここまで読んだ! -->

With the Summer launch just a few months away, we knew that we could not manually curate all the categories, as it would be very time consuming and costly. 
夏のローンチまであと数ヶ月ということで、すべてのカテゴリを手動でキュレーションすることは非常に時間がかかり、コストがかかることを私たちは知っていました。 
We also knew that we could not generate all the categories in a rule-based manner, as this approach would not be accurate enough. 
また、ルールベースの方法でカテゴリをすべて生成することもできないことも知っていました。なぜなら、このアプローチは十分に正確ではないからです。
Finally, we knew we could not produce an accurate ML categorization model without a training set of human-generated labels. 
最後に、人間が生成したラベルのトレーニングセットなしでは、正確なMLカテゴリモデルを作成できないことも知っていました。 
Given all of these limitations, we decided to combine the accuracy of human review with the scale of ML models to create a human-in-the-loop system for listing categorization and display. 
**これらすべての制約を考慮し、私たちは人間のレビューの精度とMLモデルのスケールを組み合わせて、リスティングのカテゴリ化と表示のためのヒューマン・イン・ザ・ループシステムを作成することに決めました。**
(素晴らしい言語化! 素晴らしい仕事の説明! :thinking:)

<!-- ここまで読んだ! -->

### Rule-based candidate generation ルールベースの候補生成

Before we could build a trained ML model for assigning listings to categories, we had to rely on various listing- and geo-based signals to generate the initial set of candidates. 
リスティングをカテゴリに割り当てるためのトレーニングされたMLモデルを構築する前に、私たちは初期の候補セットを生成するために、さまざまなリスティングおよび地理的信号に依存する必要がありました。
We named this technique weighted sum of indicators. 
この技術を「**weighted sum of indicators（指標の加重和）**」と名付けました。 
It consists of building out a set of signals (indicators) that associate a listing with a specific category. 
これは、**リスティングを特定のカテゴリに関連付ける一連の信号（指標）を構築すること**から成ります。 
The more indicators the listing has, the better the chances of it belonging to that category. 
リスティングが持つ指標が多いほど、そのカテゴリに属する可能性が高くなります。
(たぶん"hogehoge度合いスコア"みたいな感じかな??:thinking:)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*l8v0iDnqsyguo85jgk75Lw.png)

For example, let’s consider a listing that is within 100 meters of a Lake POI, with keyword “lakefront” mentioned in listing title and guest reviews, lake views appearing in listing photos and several kayaking activities nearby. 
例えば、湖のPOIから100メートル以内にあるリスティングを考えてみましょう。リスティングのタイトルやゲストレビューに「lakefront」というキーワードが含まれ、リスティングの写真に湖の景色が写っており、近くにいくつかのカヤックアクティビティがある場合です。
All this information together strongly indicates that the listing belongs to the Lakefront category. 
これらの情報はすべて、リスティングがLakefrontカテゴリに属することを強く示しています。 
The weighted sum of these indicators totals to a high score, which means that this listing-category pair would be a strong candidate for human review. 
これらの指標の加重和は高いスコアに達し、このリスティング-カテゴリのペアが人間のレビューの強力な候補となることを意味します。 
If a rule-based candidate generation created a large set of candidates we would use this score to prioritize listings for human review to maximize the initial yield. 
**ルールベースの候補生成が大規模な候補セットを作成した場合、このスコアを使用して人間のレビューのためにリスティングの優先順位を付け、初期の収益を最大化します。**

<!-- ここまで読んだ! -->

### Human review 人間のレビュー

The manual review of candidates consists of several tasks. 
候補の手動レビューは、いくつかのタスクで構成されています。 
Given a listing candidate for a particular category or several categories, an agent would: 
特定のカテゴリまたは複数のカテゴリのリスティング候補が与えられた場合、エージェントは以下のことを行います：

- Confirm/reject the category or categories assigned to the listing by comparing it to the category definition. 
  - カテゴリ定義と比較して、リスティングに割り当てられたカテゴリを確認または拒否します。
- Pick the photo that best represents the category. 
  - カテゴリを最もよく表す写真を選びます。 
    Listings can belong to multiple categories, so it is sometimes appropriate to pick a different photo to serve as the cover image for different categories. 
    **リスティングは複数のカテゴリに属することができる**ため、異なるカテゴリのカバー画像として異なる写真を選ぶことが適切な場合もあります。
- Determine the quality tier of the selected photo. 
  - 選択した写真の品質レベルを決定します。 
    Specifically, we defined four quality tiers: Most Inspiring, High Quality, Acceptable Quality, and Low Quality. 
    具体的には、私たちは4つの品質レベルを定義しました：最もインスパイアリング、高品質、許容可能な品質、低品質。 
    We use this information to rank the higher quality listings near the top of the results to achieve the “wow” effect with prospective guests. 
    この情報を使用して、より高品質なリスティングを結果の上位にランク付けし、見込み客に「ワオ」と思わせる効果を得ます。
- Some of the categories rely on signals related to Places of Interest (POIs) data such as the locations of lakes or national parks, so the reviewers could add a POI that we were missing in our database. 
  - **一部のカテゴリは、湖や国立公園の位置などの観光名所（POI）データに関連する信号に依存しているため、レビュアーは私たちのデータベースに欠けているPOIを追加することができます。** (まあこれはあった方がいいよね〜!!:thinking:)

<!-- ここまで読んだ! -->

### Candidate expansion 候補の拡張

Although the rule-based approach can generate many candidates for some categories, for others (e.g., Creative Spaces, Amazing Views) it may produce only a limited set of listings. 
ルールベースのアプローチは一部のカテゴリに対して多くの候補を生成できますが、他のカテゴリ（例：クリエイティブスペース、驚くべき景色）では限られたリスティングしか生成できない場合があります。
In those cases, we turn to candidate expansion. 
そのような場合、私たちは**候補の拡張**に頼ります。 
One such technique leverages pre-trained listing embeddings. 
その一つの技術は、**事前にトレーニングされたリスティング埋め込みを活用**します。 
Once a human reviewer confirms that a listing belongs to a particular category, we can find similar listings via cosine similarity. 
**人間のレビュアーがリスティングが特定のカテゴリに属することを確認すると、コサイン類似度を通じて類似のリスティングを見つけることができます。** (なるほどね! :thinking:)
Very often the 10 nearest neighbors are good candidates for the same category and can be sent for human review. 
非常に多くの場合、10の最近傍が同じカテゴリの良い候補となり、人間のレビューに送ることができます。 
We detailed one of the embedding approaches in our previous blog post and have developed new ones since then. 
私たちは以前のブログ投稿で埋め込みアプローチの一つを詳述し、それ以来新しいものを開発してきました。

Other expansion techniques include keyword expansion, location-based expansion (i.e. considering neighboring homes for same POI category), etc. 
他の拡張技術には、キーワード拡張、場所に基づく拡張（つまり、同じPOIカテゴリの近隣のホームを考慮すること）などが含まれます。

<!-- ここまで読んだ! -->

### Training ML models MLモデルのトレーニング

Once we collected enough human-generated labels, we trained a binary classification model that predicts whether or not a listing belongs to a specific category. 
**十分な人間生成ラベルを収集した後、特定のカテゴリにリスティングが属するかどうかを予測するバイナリ分類モデルをトレーニング**しました。 
We then used a holdout set to evaluate performance of the model using a precision-recall (PR) curve.
次に、ホールドアウトセットを使用して、精度-再現率（PR）曲線を使用してモデルのパフォーマンスを評価しました。 
Our goal here was to evaluate if the model was good enough to send highly confident listings directly to production. 
ここでの目標は、モデルが高い信頼性のあるリスティングを直接プロダクションに送るのに十分良いかどうかを評価することでした。

Figure 6 shows a trained ML model for the Lakefront category.  
図6は、Lakefrontカテゴリのために訓練されたMLモデルを示しています。  
On the left we can see the feature importance graph, indicating which signals contribute most to the decision of whether or not a listing belongs to the Lakefront category.  
**左側には特徴重要度グラフが表示されており、どの信号がリスティングがLakefrontカテゴリに属するかどうかの決定に最も寄与しているか**を示しています。  
On the right we can see the hold out set PR curve of different model versions.  
右側には、異なるモデルバージョンのホールドアウトセットPR曲線が表示されています。

![]()

Sending confident listings to production: using a PR curve we can set a threshold that achieves 90% precision on a downsampled hold out set that mimics the true listing distribution.  
自信のあるリスティングをプロダクションに送信する：PR曲線を使用して、真のリスティング分布を模倣したダウンサンプルされたホールドアウトセットで90%の精度を達成するしきい値を設定できます。 
Then we can score all unlabeled listings and send ones above that threshold to production, with the expectation of 90% accuracy.  
次に、すべてのラベルのないリスティングにスコアを付け、そのしきい値を超えるものをプロダクションに送信し、90%の精度を期待します。  
In this particular case, we can achieve 76% recall at 90% precision, meaning that with this technique we can expect to capture 76% of the true Lakefront listings in production.  
**この特定のケースでは、90%の精度で76%の再現率を達成できるため、この技術を使用することで、プロダクションで真のLakefrontリスティングの76%をキャッチできると期待**できます。(偽陽性を10%だけ許容して、真のLakefrontリスティングの76%をキャッチできるって見積もりってことかな...! :thinking:)

![]()

Selecting listings for human review: given the expectation of 76% recall, to cover the rest of the Lakefront listings we also need to send listings below the threshold for human evaluation.  
人間によるレビューのためのリスティングの選択：76%の再現率の期待を考慮して、**Lakefrontリスティングの残りをカバーするために、しきい値未満のリスティングも人間の評価のために送信する必要**があります。  
When prioritizing the below-threshold listings, we considered the photo quality score for the listing and the current coverage of the category to which the listing was tagged, among other factors.  
しきい値未満のリスティングを優先する際には、リスティングの写真品質スコアや、リスティングがタグ付けされたカテゴリの現在のカバレッジなど、他の要因を考慮しました。  
Once a human reviewer confirmed a listing’s category assignment, that tag would be made available to production.  
**人間のレビュアーがリスティングのカテゴリ割り当てを確認すると、そのタグはプロダクションに利用可能に**なります。  
Concurrently, we send the tags back to our ML models for retraining, so that the models improve over time.  
**同時に、タグをMLモデルに戻して再訓練を行い、モデルが時間とともに改善されるように**します。

<!-- ここまで読んだ! -->

ML models for quality estimation and photo selection.  
品質推定と写真選択のためのMLモデル。
In addition to the ML Categorization models described above, we also trained a Quality ML model that assigns one of the four quality tiers to the listing, as well as a Vision Transformer Cover Image ML model that chooses the listing photo that best represents the category.  
上記で説明したMLカテゴリモデルに加えて、リスティングに4つの品質ティアのいずれかを割り当てる品質MLモデルと、カテゴリを最もよく表すリスティング写真を選択するVision Transformer Cover Image MLモデルも訓練しました。  
In the current implementation the Cover Image ML model takes the category information as the input signal, while the Quality ML model is a global model for all categories.  
現在の実装では、Cover Image MLモデルはカテゴリ情報を入力信号として受け取り、Quality MLモデルはすべてのカテゴリに対するグローバルモデルです。  
The three ML models work together to assign category, quality and cover photo.  
これら3つのMLモデルは協力してカテゴリ、品質、カバー写真を割り当てます。  
Listings with these assigned attributes are sent directly into production under certain circumstances and also queued for review.  
これらの割り当てられた属性を持つリスティングは、特定の状況下で直接プロダクションに送信され、レビューのためにキューに入れられます。

![]()

<!-- ここまで読んだ! -->

### Two new ranking algorithms

The Airbnb Summer release introduced categories both to homepage (Figure 9 left), where we show categories that are popular near you, and to location searches (Figure 9 right), where we show categories that are related to the searched destination.  
Airbnbの夏のリリースでは、ホームページ（図9左）に近くで人気のあるカテゴリを表示し、検索した目的地に関連するカテゴリを表示するロケーション検索（図9右）にカテゴリが導入されました。  
For example, in the case of a Lake Tahoe location search we show Skiing, Cabins, Lakefront, Lake House, etc., and Skiing should be shown first if searching in winter.  
たとえば、Lake Tahoeのロケーション検索の場合、Skiing、Cabins、Lakefront、Lake Houseなどを表示し、冬に検索する場合はSkiingが最初に表示されるべきです。

In both cases, this created a need for two new ranking algorithms:  
どちらの場合も、2つの新しいランキングアルゴリズムの必要性が生まれました：

- Category ranking (green arrow in Figure 9 left): How to rank categories from left to right, by taking into account user origin, season, category popularity, inventory, bookings and user interests  
  - **カテゴリランキング（図9左の緑の矢印）**：ユーザーの出身地、季節、カテゴリの人気、在庫、予約、ユーザーの興味を考慮して、カテゴリを左から右にランク付けする方法
  - (いいね...!!:thinking:)
- Listing ranking (blue arrow in Figure 9 left): given all the listings assigned to the category, rank them from top to bottom by taking into account assigned listing quality tier and whether a given listing was sent to production by humans or by ML models.  
  - リスティングランキング（図9左の青の矢印）：カテゴリに割り当てられたすべてのリスティングを考慮し、割り当てられたリスティング品質ティアと、特定のリスティングが人間またはMLモデルによってプロダクションに送信されたかどうかを考慮して、上から下にランク付けします。
- (つまり、**特定カテゴリ内のリスティングのランキング**ね...!:thinking:)

<!-- ここまで読んだ! -->

## Putting it all together まとめ

To summarize, we presented how we create categories from scratch, first using rules that rely on listing signals and POIs and then with ML with humans in the loop to constantly improve the category. 
要約すると、私たちは、**リスティングシグナルとPOIに依存するルールを使用してゼロからカテゴリを作成する方法を示し、その後、ML（機械学習）を用いて人間をループに組み込み、カテゴリを常に改善する方法**を示しました。 
Figure 10 describes the end-to-end flow as it exists today.
図10は、現在のエンドツーエンドのフローを示しています。

![]()

Our approach was to define an acceptable delivery; prototype several categories to acceptable level; scale the rest of the categories to the same level; revisit the acceptable delivery and improve the product over time.
私たちのアプローチは、受け入れ可能なデリバリーを定義し、いくつかのカテゴリを受け入れ可能なレベルにプロトタイプし、残りのカテゴリを同じレベルにスケールし、受け入れ可能なデリバリーを再訪し、時間をかけて製品を改善することでした。

- 合格ラインの定義(defining an acceptable delivery):
  - 大量のリスティングの全てを手作業で割り当てるのは無理。プログラム的な割り当てだけでは精度が低い。
  - なので、最終的な機能として「どこまでの品質(精度や写真の魅力など)ならリリースできるか」という基準と、それを満たすための「人間のレビューと機械学習(ML)を組み合わせたシステム(human-in-the-loop system)」を定義した。
- プロトタイプによる検証(prototyping several categories to acceptable level):
  - **いきなり56種類のカテゴリ全てを同時に作るのではなく、まずは「Lakefront」と「Skiing」という2つのカテゴリに絞って試作**した。例えば「適合率90%で本番環境に送る」といった基準を満たせるかtestを行った。
- 全体への横展開(scaling the rest of the categories to the same level):
  - プロトタイプで上手くいった手法を残りのカテゴリにも横展開し、システム全体を同じ品質レベルに引き上げた。
- 継続的な改善(revisiting the acceptable delivery and improving the product over time):
  - リリースして終わりではない。人間がレビューしたカテゴリや写真を継続的にMLモデルに戻して再学習させることで、時間の経過とともにモデルの分類精度や写真選定のクオリティを向上させる仕組みを作った。

In Part II, we’ll explain in greater detail the models that categorize listings into categories.
第II部では、リスティングをカテゴリに分類するモデルについて、より詳細に説明します。

<!-- ここまで読んだ! -->

## Acknowledgments 謝辞

We would like to thank everyone involved in the project. 
プロジェクトに関わったすべての人々に感謝したいと思います。

Building Airbnb Categories holds a special place in our careers as one of those rare projects where people with different backgrounds and roles came together to work jointly to build something unique. 
Airbnbカテゴリの構築は、異なるバックグラウンドと役割を持つ人々が集まり、共同でユニークなものを作り上げるという稀なプロジェクトの一つとして、私たちのキャリアの中で特別な位置を占めています。

<!-- ここまで読んだ! -->
