refs: https://careersatdoordash.com/blog/homepage-recommendation-with-exploitation-and-exploration/


# Homepage Recommendation with Exploitation and Exploration ホームページ推薦における活用と探求

October 5, 2022  
2022年10月5日  
Yu Zhang  
ユウ・ジャン  

Building quality recommendations and personalizations requires delicately balancing what is already known about users while recommending new things that they might like.  
質の高い推薦とパーソナライズを構築するには、**ユーザについて既に知られていることと、彼らが好むかもしれない新しいものを推薦することの微妙なバランスを取る必要**があります。  
As one of the largest drivers of DoorDash's business, the homepage contributes a significant portion of our total conversions.  
DoorDashのビジネスの最大の推進力の一つとして、ホームページは私たちの総コンバージョンの重要な部分を占めています。  
Its layout, as shown in Figure 1, is meant to inspire customers to order their favorite food and discover new merchants.  
図1に示すように、そのレイアウトは顧客がお気に入りの食べ物を注文し、新しい商人を発見することを促すことを目的としています。  
Given the homepage’s limited real estate, we wanted to add personalization features to improve the customer experience through increasing the relevance of every item presented there.  
ホームページの限られたスペースを考慮し、そこに表示される各アイテムの関連性を高めることで顧客体験を向上させるために、パーソナライズ機能を追加したいと考えました。 

![]()
Figure 1: DoorDash’s homepage displays local items, stores, and promotions to entice users to make an order.


<!-- ここまで読んだ! -->

Building personalized recommendations is challenging.  
パーソナライズされた推薦を構築することは困難です。
Each person is nuanced in what they like and that varies based on how they feel when ordering.  
各人は自分の好みにおいて微妙な違いがあり、それは注文時の気分によっても変わります。  
Personalized recommendations requires knowing each consumer well enough to surface the most relevant merchants in the space constrained homepage, typically from more than 1,000 merchants available.  
パーソナライズされた推薦は、通常1,000以上の利用可能な商人の中から、限られたスペースのホームページで最も関連性の高い商人を提示するために、**各消費者を十分に理解することを必要とします。** (特徴量をしっかり整備して各消費者の理解度を上げていきてぇ〜...!:thinking:)
Additionally, our recommendation must adapt quickly to changing consumer interests at different times of the day, day of the week, and locations.  
さらに、私たちの推薦は、1日の異なる時間、週の曜日、そして場所による消費者の興味の変化に迅速に適応する必要があります。
Personalized recommendation at DoorDash involves using both what we already know about users (also known as exploitation) and showing users new things to better understand what they like (also known as exploration) to improve consumer experience. 
DoorDashにおけるパーソナライズされた推薦は、**ユーザについて既に知っていること（活用とも呼ばれる）**と、**ユーザが好むものをよりよく理解するために新しいものを示すこと（探求とも呼ばれる）**を組み合わせて、消費者体験を向上させることを含みます。  

<!-- ここまで読んだ! -->

In this post, we will first give a high-level overview of how our homepage rankings work and then zero in on how our model balances exploitation and exploration during ranking to optimize the consumer experience while simultaneously improving fairness for merchants.  
この投稿では、まず私たちのホームページランキングがどのように機能するかの高レベルの概要を示し、その後、ランキング中に私たちのモデルがどのように活用と探求のバランスを取って消費者体験を最適化し、同時に商人に対する公平性を向上させるかに焦点を当てます。
After introducing both the challenges and opportunities in relevance ranking for mixed types of homepage entities, we present our machine learning (ML) solution, a deep-learning-based learn-to-rank (LTR) model — universal ranker (UR).
さまざまなタイプのホームページエンティティにおける関連性ランキングの課題と機会を紹介した後、私たちの機械学習（ML）ソリューションである、深層学習に基づくlearn-to-rank（LTR）モデル — universal ranker（UR）を提示します。  
We discuss the need to go beyond exploitation, sharing our exploration approach based on the concept of upper confidence bound (UCB), a reinforcement learning method known for solving multi-armed bandit (MAB) problems.  
私たちは、活用を超える必要性について議論し、multi-armed bandit（MAB）問題を解決することで知られる強化学習手法であるupper confidence bound（UCB）の概念に基づく探求アプローチを共有します。  
Finally, we illustrate a ranking framework integrating UR and UCB, and discuss how we make intelligent trade-offs between exploitation and exploration in our homepage recommendations.  
最後に、**UR(=ランク学習のDNNモデル)とUCB(=banditの仕組み)を統合したランキングフレームワークを示し**、私たちのホームページ推薦における活用と探求の間でどのようにインテリジェントなトレードオフを行うかについて議論します。

<!-- ここまで読んだ! -->

## What’s behind DoorDash’s homepage recommendation DoorDashのホームページ推薦の背後にあるもの

From retrieving information of thousands of stores to presenting a unique experience for consumers, DoorDash’s homepage recommendation can be divided into three major stages:  
数千の店舗の情報を取得し、消費者にユニークな体験を提供することから、**DoorDashのホームページ推薦は3つの主要な段階**に分けることができます。

- First pass ranking, or FPR, is the first part of the retrieval stage and includes: **ファーストパスランキング（FPR）**は、取得段階の最初の部分であり、以下を含みます：

  - Selecting no more than 1,200 candidates from ElasticSearch that are most relevant to the consumer experience among all stores  
  - ElasticSearchから、すべての店舗の中で**消費者体験に最も関連性の高い候補を1,200件以下選択**すること

  - Satisfying a combination of strategies, such as including certain popular stores while guaranteeing diversity across verticals (for example, restaurants, convenience and grocery stores, or retail stores)  
  - 特定の人気店舗を含めつつ、業種間の多様性を保証するなどの戦略の組み合わせを満たすこと（例えば、レストラン、コンビニエンスストア、食料品店、小売店など）

- Second pass ranking, or SPR, filters and pre-ranks those candidates, ultimately:  
- セカンドパスランキング（SPR）は、これらの候補をフィルタリングし、事前にランク付けします。最終的には：

  - Choosing up to 50 for the first page of the store feed  
  - ストアフィードの最初のページに**最大50件を選択**すること

  - Ranking stores/items within horizontally scrollable carousels, each of which offers different subsets of candidates (for example, a “National Favorites” carousel might contain popular chain stores while the “Now on DoorDash” carousel might suggest newly onboarded local stores)  
  - 水平方向にスクロール可能なカルーセル内で店舗/アイテムをランク付けし、それぞれが異なる候補のサブセットを提供します（例えば、「National Favorites」カルーセルには人気のチェーン店舗が含まれ、「Now on DoorDash」カルーセルには新たに参加した地元店舗が提案されるかもしれません）

- Final ranking, or FR, is the concluding stage, resulting in vertical rankings of all available carousels and stores on the first page of the store feed.  
- **最終ランキング（FR）**は、結論的な段階であり、ストアフィードの最初のページにあるすべての利用可能なカルーセルと店舗の縦のランキングを生成します。

Our efforts here focus on the FR stage, which determines the order of contents shown to consumers when they scroll vertically.  
ここでの私たちの努力は、消費者が縦にスクロールしたときに表示されるコンテンツの順序を決定する**FR段階に焦点を当てて**います。

<!-- ここまで読んだ! -->

## Contending with comparing different entities on the DoorDash homepage DoorDashのホームページで異なるエンティティを比較することに関する考察

To better illustrate the complexity at the FR stage, it's helpful to introduce how the DoorDash homepage showcases entities through its organization and layout. 
FRステージの複雑さをよりよく示すために、DoorDashのホームページがその組織とレイアウトを通じてエンティティをどのように表示しているかを紹介することが有益です。
We define an entity as any content module that can be placed into a single slot on the homepage, such as a merchant, an item, or an offer. 
**エンティティとは、商人、アイテム、またはオファーなど、ホームページの単一のスロットに配置できる任意のコンテンツモジュールとして定義**します。
As shown in Figure 2, a single entity could be a store or an item while a nested entity, or carousel, contains ordered individual entities such as the “Now on DoorDash” store carousel or an item carousel such as “Most Ordered Dishes Near You.” 
図2に示すように、単一のエンティティは店舗やアイテムである可能性があり、ネストされたエンティティ、またはカルーセルは、「Now on DoorDash」ストアカルーセルや「Most Ordered Dishes Near You」のようなアイテムカルーセルなど、順序付けられた個々のエンティティを含みます。
(色んな種類・粒度のentityが混在してて、FR段階では、それらをいい感じに並び替えているのか...!:thinking:)

<!-- ここまで読んだ! -->

As discussed, the total candidates for recommendation already have been significantly narrowed in the initial two stages to fewer than 50 carousels — the actual number varies at different locations and time of day — and no more than 50 individual stores for the first page of the store feed. 
前述のように、推薦のための候補は、最初の2つのステージで50未満のカルーセルに大幅に絞り込まれています — 実際の数は異なる場所や時間帯によって異なります — そして、ストアフィードの最初のページには50を超える個々の店舗はありません。
However, these candidates consist of a mixture of different entity types, which creates huge challenges for building ranking models. 
しかし、**これらの候補は異なるエンティティタイプの混合で構成されており、ランキングモデルを構築する上で大きな課題を生み出します。**

<!-- ここまで読んだ! -->

## Difficulties with scalability and calibration スケーラビリティとキャリブレーションの課題

It is not practical or scalable to build a dedicated ranking model for each entity type, both because a new model is required each time a different entity type lands on the homepage and because each model subsequently requires maintenance going forward.
**各エンティティタイプごとに専用のランキングモデルを構築することは実用的でもスケーラブルでもありません。なぜなら、異なるエンティティタイプがホームページに表示されるたびに新しいモデルが必要であり、さらに各モデルは今後メンテナンスが必要になるから**です。
(なるほどなぁ...! でももし特定のentityの表示数を制御する必要があるなら、entityごとにランキングを作って、後からルールベースで混ぜ合わせる方が都合良かったりするのかなと思ってる。あ、でもこれって別にモデルをentityごとに作るべきじゃない、という話とは衝突しないのか...! 同じモデルを使ってentityごとに推論するという話もあるから...!:thinking:)

<!-- ここまで読んだ! -->

What’s more, even if we built these dedicated models, it is difficult to calibrate and compare the scores they produce for different entities.
さらに、**これらの専用モデルを構築したとしても、異なるエンティティに対して生成されるスコアをキャリブレーションし、比較することは困難**です。(なるほどね...!:thinking:)
For example, say we want to recommend highly relevant and good-quality Japanese restaurants and dishes to consumers who often order sushi or ramen.
例えば、寿司やラーメンをよく注文する消費者に対して、高い関連性と良質な日本料理やレストランを推薦したいとします。
While it might be straightforward to compare relevance between two restaurants, comparing a Japanese restaurant with a store carousel consisting of more than 10 popular Asian restaurants and their dishes is a nontrivial task.
2つのレストラン間の関連性を比較することは簡単かもしれませんが、10以上の人気アジアレストランとその料理からなるストアキャロセルと日本のレストランを比較することは簡単ではありません。
That challenge demands comparing apples and oranges.
その課題は、リンゴとオレンジを比較することを要求します。

<!-- ここまで読んだ! -->

## Enhancing relevance and efficiency opens opportunities 関連性と効率の向上は機会を開く

The ability to rank mixed entity types helps unlock the potential for more relevant homepage recommendations.  
異なるエンティティタイプをランク付けする能力は、より関連性の高いホームページの推薦の可能性を引き出すのに役立ちます。
On our existing homepage, we have a fixed order for entities:  
**私たちの既存のホームページでは、エンティティの固定順序があります**：
(わかる...!:thinking:)

- nested carousel entities come first  
  - ネストされたカルーセルエンティティが最初に来ます
- single-store entities come second  
  - シングルストアエンティティが次に来ます

This worked well initially in 2020 when there were only half a dozen carousels; consumers could either scroll horizontally to engage with a favorite carousel or vertically to move quickly to individual stores for more options.
**これは、2020年にカルーセルがわずか6つしかなかったときにはうまく機能しました。**消費者は、お気に入りのカルーセルに横にスクロールするか、個々のストアに縦にスクロールしてより多くのオプションに素早く移動することができました。
But the number of carousels has exploded to more than 30 as of the third quarter of 2022, making it hard for consumers to see any individual stories below the carousels.  
しかし、**2022年第3四半期までにカルーセルの数は30を超え、消費者がカルーセルの下にある個々のストーリーを見るのが難しくなっています。**
The old homepage organization makes for a suboptimal consumer experience today.  
古いホームページの構成は、今日の消費者体験にとって最適ではありません。
While we could place highly relevant stores just below the carousels, the distance from the beginning of the consumer journey sharply lowers their visibility.  
非常に関連性の高いストアをカルーセルのすぐ下に配置することはできますが、消費者の旅の始まりからの距離が彼らの視認性を大きく低下させます。
Switching positions of stores and carousels could result in low-relevance stores getting top billing, wasting precious impression opportunities.  
ストアとカルーセルの位置を入れ替えると、関連性の低いストアが優先され、貴重なインプレッションの機会を無駄にする可能性があります。

To address the issue, we launched a new UI framework.  
この問題に対処するために、私たちは新しいUIフレームワークを立ち上げました。
It allows intermixing experiences on the homepage to unlock the potential for more optimal homepage recommendations;  
これにより、ホームページ上での体験を混合させ、より最適なホームページの推薦の可能性を引き出すことができます。
for instance, a more relevant store could be ranked higher than a less relevant carousel overall, as shown by the “New” UX in Figure 3.  
例えば、より関連性の高いストアが、全体として関連性の低いカルーセルよりも高くランク付けされる可能性があります。これは、図3の「新しい」UXに示されています。
However, this new experience also has created challenges for the ML ranking model.  
しかし、この新しい体験は、MLランク付けモデルにとっても課題を生み出しました。
Our solution has been to develop a single model that essentially can compare apples and oranges to showcase the best products to consumers.  
**私たちの解決策は、基本的にリンゴとオレンジを比較して消費者に最良の製品を示す単一のモデルを開発すること**でした。


![]()
Figure 3: Homepage ranking with mixed entity types 

<!-- ここまで読んだ! -->

## Building a universal ranker to empower exploitation 普遍的なランカーを構築して活用を促進する

To improve homepage engagement, we built the UR to provide consistent ranking across a variety of entities, prioritize better relevancy, and shorten the consumer’s shopping journey. 
ホームページのエンゲージメントを向上させるために、私たちはURを構築し、さまざまなエンティティにわたって一貫したランキングを提供し、関連性を優先し、消費者のショッピングジャーニーを短縮します。
As noted earlier, this LTR model uses a deep neural network to leverage the learnings from the deep learning recommendation model and “Wide & Deep” learning, which deploys jointly trained wide linear models and deep neural networks. 
前述のように、このLTRモデルは、深層学習推薦モデルと「Wide & Deep」学習からの学びを活用するための深層ニューラルネットワークを使用します。**「Wide & Deep」学習は、共同で訓練された広い線形モデルと深いニューラルネットワークを展開**します。
The UR jointly ranks vertical positions for mixed types of entities by order of their pConv — probability of conversion, which is how we measure the relevance of a recommendation. 
**URは、異なるタイプのエンティティの垂直位置をpConv（コンバージョンの確率）の順に共同でランク付けし、これが推薦の関連性を測定する方法**です。

<!-- ここまで読んだ! -->

The most complex and universal aspect of developing our UR was figuring out how to compare different entities in different places. 
URを開発する上で最も複雑で普遍的な側面は、異なる場所にある異なるエンティティをどのように比較するかを考えることでした。
Ultimately, we accomplished this by creating a consistent relationship across all types of entities. 
最終的に、私たちはすべてのタイプのエンティティ間に一貫した関係を作ることでこれを達成しました。
From high to low, we define three hierarchical levels of entities: 1) a store carousel, 2) an individual store/item carousel, and 3) an individual item, where a higher-level entity can be represented by an ordered sequence of lower-level ones. 
高いものから低いものまで、私たちは**3つの階層レベルのエンティティを定義**します：1）ストアカルーセル、2）個々のストア/アイテムカルーセル、3）個々のアイテムであり、**高レベルのエンティティは低レベルのエンティティの順序付けられたシーケンスで表すことができます。**
For example, a store carousel could be viewed as an ordered list of stores, each of which also could be viewed as an ordered list of items. 
例えば、ストアカルーセルはストアの順序付けられたリストとして見ることができ、それぞれのストアもアイテムの順序付けられたリストとして見ることができます。
With the bridge through individual stores, a store carousel can then be viewed as an ordered, nested list of items. 
個々のストアを通じての橋渡しで、ストアカルーセルはアイテムの順序付けられたネストされたリストとして見ることができます。
The model ranks a store as a carousel with only one store and an item within that store as a carousel with only one store and one item. 
**モデルは、ストアを1つのストアだけのカルーセルとして、そしてそのストア内のアイテムを1つのストアと1つのアイテムだけのカルーセルとしてランク付けします。** 
(3段階のentity達を、モデルは全て一番上のentityであるストアカルーセルとして扱う、って意味かな...??:thinking:)
With this sequential relationship, we can then construct the features of a high-level entity from the low-level ones it contains. 
この順次的な関係を持つことで、私たちは高レベルのエンティティの特徴をそれが含む低レベルのエンティティから構築することができます。
Using a feature “f” as an example, we build the feature for an individual store and a store carousel as follows: 
特徴「f」を例として、私たちは個々のストアとストアカルーセルの特徴を次のように構築します：

- individual store 1: [f_1, padding, padding]
- carousel with 3 stores: [f_1, f_2, f_3]

In addition to the padding/clipping approach, where we need to define a pre-fixed sequence length, we can also incorporate a layer such as LSTM to transform the sequential features into the same dimensions as individual ones, which the model then can easily use. 
事前に固定されたシーケンス長を定義する必要があるpadding/clippingアプローチに加えて、LSTMのような層を組み込むことで、**順次的な特徴を個々の特徴と同じ次元に変換**し、モデルが簡単に使用できるようにすることもできます。

<!-- ここまで読んだ! -->

The UR’s features can be divided into four major categories: 
URの特徴は4つの主要なカテゴリに分けることができます：

- Entity-related features such as cuisine type, price range, popularity, quality, and rating
  - エンティティ関連の特徴（料理の種類、価格帯、人気、品質、評価など）
- Consumer-related features such as cuisine/taste preference, vegan status, and affordability
  - 消費者関連の特徴（料理/味の好み、ビーガンのステータス、手頃さなど）
- Consumer-entity engagement features such as view/click/order history, rating, and reorder rate
  - 消費者-エンティティエンゲージメントの特徴（閲覧/クリック/注文履歴、評価、再注文率など）
- Context-related features such as delivery ETA/distance/fee, promotion, day part, week part, holiday, and weather conditions
  - コンテキスト関連の特徴（配達のETA/距離/料金、プロモーション、日中の時間帯、週の時間帯、祝日、天候条件など）

In addition to traditional numerical and categorical feature types, we heavily used embeddings across all the feature categories, including both pre-trained embeddings from existing ML models and embedding layers trained as part of the model itself. 
**従来の数値およびカテゴリ型の特徴に加えて、私たちはすべての特徴カテゴリにわたって埋め込みを多く使用しました。これは事前学習済み埋め込みモデルとモデル自身の一部として学習される埋め込み層の両方を含みます。**
The ETL for the batch features was developed and maintained through our internal tool Fabricator and the LTR UR model was implemented in PyTorch. 
バッチ特徴のETLは、私たちの内部ツールFabricatorを通じて開発および維持され、LTR URモデルはPyTorchで実装されました。

<!-- ここまで読んだ! -->

With this model, we can show consumers items they might like despite the varying entity challenges. 
このモデルを使用することで、私たちは消費者に異なるエンティティの課題にもかかわらず、彼らが好むかもしれないアイテムを示すことができます。
The next step would be to expand our model beyond what we think they like so we can broaden our understanding of customer preferences. 
次のステップは、私たちが彼らが好むと思うものを超えてモデルを拡張し、顧客の好みの理解を広げることです。

<!-- ここまで読んだ! -->

## Exploring beyond exploitation 利用の枠を超えて

Only focusing on exploitation can lead consumers into the so-called filter bubble/ideological frame problem. 
**利用にのみ焦点を当てることは、消費者をいわゆるフィルターバブル/イデオロギー的枠組みの問題に導く可能性があります。**
This occurs when existing consumers begin to perceive only a small subset of merchants with whom they are already familiar, creating a self-fulfilling prophecy in which consumers buy primarily similar items. 
これは、既存の消費者がすでに知っている小さな商人のサブセットのみを認識し始め、消費者が主に類似のアイテムを購入する自己実現的予言を生み出すときに発生します。 
Recommendations for new consumers might be biased toward their initial engagement rather than their true preferences; their homepage may be flooded with very similar options, reducing the amount of time left to explore. 
**新しい消費者への推薦は、彼らの真の好みではなく、初期の関与に偏る可能性があります。**その結果、彼らのホームページは非常に似たオプションであふれ、探索に残される時間が減少します。 

This exploitation also may delay response to consumer preference changes over time because exploitation models have strong momentum for previous behaviors and are slow to adapt to new information. 
この利用は、消費者の好みの変化に対する反応を時間とともに遅らせる可能性があります。なぜなら、利用モデルは以前の行動に対して強い慣性を持ち、新しい情報に適応するのが遅いからです。 
Consumers also could become bored with what they perceive as a stale homepage; the lack of inspiration could depress order rates. 
消費者は、古くなったホームページと認識するものに飽きてしまう可能性があります。インスピレーションの欠如は、注文率を低下させる可能性があります。 
On the merchant side, over-exploitation could cause fairness issues over time as popular merchants become ever more dominant while new merchants recede into the platform’s background. 
**商人側では、過剰な利用が時間とともに公平性の問題を引き起こす可能性があります。人気のある商人がますます支配的になる一方で、新しい商人はプラットフォームの背景に退いていくから**です。

<!-- ここまで読んだ! -->

## Enabling exploration using upper confidence bound 上限信頼区間を用いた探索の促進

To overcome these problems, we introduced a reinforcement learning approach based on aUCB algorithm to enable consumers to explore. 
これらの問題を克服するために、私たちは消費者が探索できるようにするために、UCBアルゴリズムに基づいた強化学習アプローチを導入しました。
In a greedy manner, the UCB algorithm favors exploration actions with the strongest potential to maximize rewards, where potential is quantified in terms of uncertainty. 
貪欲な方法で、UCBアルゴリズムは報酬を最大化するための最も強い潜在能力を持つ探索アクションを優先します。この潜在能力は不確実性の観点から定量化されます。
While there are various UCB variants with different assumptions and complexities, the core concept involves the expected reward and its associated uncertainty for a given action: 
さまざまな仮定や複雑さを持つUCBのバリアントが存在しますが、コアの概念は特定のアクションに対する期待報酬とその関連する不確実性を含みます：

<!-- ここまで読んだ! -->

$$
e^{*}_{t, c} = \argmax_{e} [\hat{Q}_t(c, e) + \hat{U}_t(c, e)]
$$

where t is the total times of all the previous trials of recommending an entity e to a consumer c.
ここで、$t$ は、消費者 $c$ にエンティティ $e$ を推薦するすべての以前の試行の合計回数です。
$e^*_t, c$ is the optimal entity we want to recommend to a consumer $c$ at a time $t$; 
$e^*_{t, c}$ は、時間 $t$ に消費者 $c$ に推薦したい最適なエンティティです。
$e_{t, c} \in E_{t, c}$ are an individual entity and the entire entity set available to consumer c at time t, respectively;
$e_{t, c} \in E_{t, c}$ は、時間 $t$ に消費者 $c$ が利用できる個々のエンティティとエンティティセット全体です。
$\hat{Q}_t(c, e)$ is the expected reward for consumer $c$ on an entity $e$; 
$\hat{Q}_t(c, e)$ は、消費者 $c$ に対するエンティティ $e$ の期待報酬です。
$\hat{U}_t(c, e)$ is the uncertainty of the reward for a consumer $c$ on an entity $e$;
$\hat{U}_t(c, e)$ は、消費者 $c$ に対するエンティティ $e$ の報酬の不確実性です。

<!-- ここまで読んだ! -->

Based on Hoeffding’s inequality for any bounded distribution, this approach guarantees that with only a probability of $e^{-2t\hat{U}_t(c, e)^2}$ could the actual reward $Q_t(c, e)$ be higher than the estimated UCB of $Q_t(c, e) + \hat{U}_t(c, e)$. 
任意の有界分布に対するホフディングの不等式に基づいて、このアプローチは、実際の報酬 $Q_t(c, e)$ が推定されたUCB $Q_t(c, e) + \hat{U}_t(c, e)$ よりも高くなる確率が $e^{-2t\hat{U}_t(c, e)^2}$ であることを保証します。
If we choose a very small constant $p$ for $e^{-2t\hat{U}_t(c, e)^2$, then we have: 
もし $e^{-2t\hat{U}_t(c, e)^2}$ のために非常に小さな定数 $p$ を選ぶと、次のようになります：

$$
hoge
$$

To have higher confidence in our UCB estimation as we continue to collect more reward (conversion) data from our recommendations, we can reduce the threshold by setting $p = T^{-4}$ following the UCB1 algorithm: 
私たちの推薦からの報酬（コンバージョン）データを収集し続けることでUCB推定に対する信頼を高めるために、UCB1アルゴリズムに従って $p = T^{-4}$ を設定することでしきい値を減少させることができます：

$$
hoge
$$

where T is the total times of consumer $c$’s trials on all the recommended entities and t is the total times of consumer $c$’s trials on an entity $e$.
ここで$T$ は、すべての推奨エンティティに対する消費者 $c$ の総試行回数であり、$t$ はエンティティ $e$ に対する消費者 $c$ の総試行回数です。

<!-- ここまで読んだ! -->

## How we combined exploitation and exploration どのようにして利用と探索を組み合わせたか

It is neither feasible nor optimal to directly implement the UCB in its original form because:
**UCBをそのままの形で直接実装することは、実現可能でも最適でもありません**。なぜなら：

- Each consumer can choose from thousands of stores and hundreds of thousands of items at a certain location and time, making it impossible to try each of them and hampering collection of cumulative conversion data to estimate the pConv.
  - 各消費者は特定の場所と時間で数千の店舗と数十万のアイテムから選択できるため、それぞれを試すことは不可能であり、pConvを推定するための累積コンバージョンデータの収集を妨げます。

- Estimating the expected pConv for entities with mixed types adds further complexity
  - 異なるタイプのエンティティに対する期待されるpConvを推定することは、さらなる複雑さを加えます。

- The recommendation engine produces a ranked list of entities for each consumer. But because a single app window can only show a few entities and because each consumer can choose how deep they wish to browse/scroll, there’s uncertainty around how many of the recommended entities will receive effective consumer feedback.
  - レコメンデーションエンジンは各消費者に対してエンティティのランク付けされたリストを生成します。しかし、単一のアプリウィンドウは数個のエンティティしか表示できず、各消費者はどれだけ深くブラウズ/スクロールするかを選択できるため、推奨されたエンティティのうちどれが効果的な消費者フィードバックを受けるかについての不確実性があります。

- When introducing fresh options for a consumer, we need to control uncertainty carefully so that they do not add confusion or interrupt the consumer experience.
  - 消費者に新しい選択肢を提供する際には、混乱を招いたり消費者体験を中断させたりしないように、不確実性を慎重に管理する必要があります。

<!-- ここまで読んだ! -->

Given these considerations, our final solution was to integrate the UR into the UCB algorithm. 
これらの考慮事項を踏まえ、私たちの最終的な解決策は、URをUCBアルゴリズムに統合することでした。
This allows us to make scalable and smart trade-offs between exploitation and exploration, allowing fresh choices for consumers without disturbing their routing experience.
これにより、利用と探索の間でスケーラブルで賢いトレードオフを行うことができ、消費者のルーティング体験を妨げることなく新しい選択肢を提供することが可能になります。

<!-- ここまで読んだ! -->

## Defining the composite model 複合モデルの定義

We define the reward from any recommendation as the consumer conversion within a certain time period; hence, the expected reward essentially is evaluated by the expected pConv for any consumer-entity pair. 
私たちは、任意の推薦からの報酬を特定の時間枠内での消費者のコンバージョンとして定義します。したがって、期待される報酬は本質的に任意の消費者-エンティティペアに対する期待pConvによって評価されます。
The consumer-entity impression is used to track the effective recommendation trial and estimate the uncertainty of the corresponding pConv. 
消費者-エンティティのインプレッションは、効果的な推薦試行を追跡し、対応するpConvの不確実性を推定するために使用されます。
The final UCB score is then obtained by blending the UR score (pConv) with the uncertainty. 
最終的なUCBスコアは、URスコア（pConv）と不確実性を組み合わせることによって得られます。
Data driving the UR and uncertainty is refreshed daily; the entire process could be viewed from a Bayesian perspective. 
URと不確実性を駆動するデータは毎日更新されます。この全プロセスはベイズ的な視点から見ることができます。
Each day, we assume the prior distribution for the pConv variable has the mean and standard deviation of the current UR score and uncertainty. 
毎日、pConv変数の事前分布は現在のURスコアと不確実性の平均と標準偏差を持つと仮定します。
We then compute the posterior distribution with another day’s consumer-entity engagement data: 
次に、別の日の消費者-エンティティのエンゲージメントデータを用いて事後分布を計算します：

$$
score^{c,e}_{Comp} = Score^{c,e}_{UR} + C \sqrt{\frac{log{N_{c}}}{N_{c,m}}}
$$

where $N_c$ is the total impressions for the consumer $c$ on all recommended entities within a certain time period 
ここで、$N_c$は特定の時間枠内で消費者$c$がすべての推薦エンティティに対して持つ総インプレッションです。
$N_{c,m}$ is the impressions between consumer $c$ and entity $e$ within a certain time period 
$N_{c,m}$は特定の時間枠内で消費者$c$とエンティティ$e$の間のインプレッションです。
$C$ is the exploration coefficient. 
$C$は探索係数です。

<!-- ここまで読んだ! -->

The uncertainty increases slowly and logarithmically as a consumer’s total impression goes up but decays rapidly with the linear relationship as the specific impression for a certain entity increases. 
**不確実性は、消費者の総インプレッションが増加するにつれてゆっくりと対数的に増加しますが、特定のエンティティのインプレッションが増加するにつれて線形関係で急速に減少**します。
This relative relationship benefits the ranking system in two ways: 
この**相対的な関係は、ランキングシステムに2つの方法で利益**をもたらします：

- It improves freshness when a consumer mostly engages with a few entities (for example, the top 10 on the homepage). 
**消費者が主に少数のエンティティ（例えば、ホームページのトップ10）に関与する場合**、新鮮さが向上します。
Although the UR scores for these entities remain high, their uncertainties will continue to drop rapidly. 
これらのエンティティのURスコアは高いままですが、それらの不確実性は急速に低下し続けます。
On the other hand, those entities without impressions would have their uncertainties continue to increase until they are large enough to force their way into the top 10. 
一方、インプレッションのないエンティティは、不確実性が増加し続け、トップ10に入るのに十分な大きさになるまで続きます。

- It aids quick homepage personalization when a consumer enjoys broad exploration. 
**消費者が広範な探索を楽しむ場合**、迅速なホームページのパーソナライズを助けます。
With multiple impressions for various entities, there is a consistent uncertainty drop for each of them such that the composite score converges to its UR score, which is sensitive to positive engagement signals such as clicks, orders, and good ratings. 
さまざまなエンティティに対する複数のインプレッションがある場合、それぞれの不確実性は一貫して低下し、合成スコアはクリック、注文、良い評価などのポジティブなエンゲージメント信号に敏感なURスコアに収束します。

<!-- ここまで読んだ! -->

We also add the exploration coefficient $C$ for the uncertainty because we are less interested in its accuracy but more in its scale, which directly determines how much disturbance will be introduced to the existing ranking (for example, how many new entities are surfaced higher and how different their positions are historically). 
私たちは、不確実性のために探索係数$C$も追加します。なぜなら、**私たちはその精度にはあまり関心がなく、そのスケールにもっと関心があるからです。これは、既存のランキングにどれだけの混乱がもたらされるか（例えば、どれだけの新しいエンティティがより高く表示され、歴史的にどれだけ異なる位置にあるか）を直接決定**します。
The optimal $C$ is then determined later through online experiments. 
最適な$C$は、その後オンライン実験を通じて決定されます。

<!-- ここまで読んだ! -->

## Integrating all models into a ranking framework モデルをランキングフレームワークに統合する

The DoorDash homepage ranking framework with all these pieces put together is shown in Figure 4. 
これらの要素をすべて統合したDoorDashのホームページランキングフレームワークは、図4に示されています。
The exploitation component includes the FPR, SPR, and UR, while the exploration component introduces uncertainty to the expected pConv predicted by the UR. 
利用部分はFPR、SPR、URを含み、探索部分はURによって予測される期待pConvに不確実性を導入します。
By continuing to collect and update the engagement data through daily refreshed features, we can generate a more accurate mean of the pConv while building more confidence in our uncertainty estimation. 
日々更新される特徴を通じてエンゲージメントデータを収集し更新し続けることで、pConvのより正確な平均を生成し、私たちの不確実性推定に対する信頼を高めることができます。

![]()

<!-- ここまで読んだ! -->

## Enabling a better homepage experience ホームページ体験の向上

With the newly developed framework, we give consumers an improved dynamic experience, including:
新たに開発されたフレームワークにより、**私たちは消費者に改善された動的体験を提供します。これには以下が含まれます**:

- Keeping the most relevant entities at the top (high UR scores)
最も関連性の高いエンティティを上位に保持する（高いURスコア）

- Downranking the entities that are somehow relevant (median UR scores) but have way too many impressions (low uncertainties)
関連性はあるが、インプレッションが多すぎる（低い不確実性）エンティティのランクを下げる（中央値URスコア）

- Trying new entities from lower positions (low UR scores) that have little chance to be shown to the consumers (high uncertainties)
消費者に表示される可能性がほとんどない（高い不確実性）低い位置から新しいエンティティを試す（低いURスコア）

- Prioritizing the newly tried entities if they receive positive feedback from consumers as measured by orders or good ratings, which also represents improved UR scores with dropped uncertainties
消費者からの注文や良い評価などのポジティブなフィードバックを受けた場合、優先的に新しく試したエンティティを表示します。これは、不確実性が低下したURスコアの改善も表しています。

- Deemphasizing newly tried entities if there is no positive feedback from consumers — for instance, only views but no further actions. This represents low UR scores with dropped uncertainties
消費者からのポジティブなフィードバックがない場合、優先度を下げる新たに試したエンティティ。例えば、ビューのみでそれ以上のアクションがない場合などです。これは、不確実性が低下した低いURスコアを表しています。

<!-- ここまで読んだ! -->

As can be seen in Figure 5, the change primarily impacts existing consumers who previously have browsed entities on our platform. 
図5に示すように、**この変更は主に以前に私たちのプラットフォームでエンティティを閲覧した既存の消費者に影響を与えます。**
There is little impact on new consumers for whom we have no engagement data. 
**エンゲージメントデータがない新しい消費者にはほとんど影響がありません。**
We show the example experience using carousel and store feeds separately because the homepage experience with mixed entities remains a work in progress.
私たちは、カルーセルとストアフィードを別々に使用した体験の例を示します。なぜなら、混合エンティティを用いたホームページ体験はまだ進行中だからです。

![]()

With the developed framework, we observe consistent improvements in our online experiments. 
開発されたフレームワークにより、**私たちはオンライン実験において一貫した改善**を観察しています。
The new experience drives more consumers to engage with our recommendations and convert on the homepage. 
**新しい体験は、より多くの消費者が私たちの推薦に関与し、ホームページでコンバージョンすることを促進します。**
More consumers are interested in trying new merchants and items they never ordered before, which not only enriches their experience but also creates more opportunities for our local or new merchants rather than our enterprise ones.
より多くの消費者が、これまで注文したことのない新しい商人やアイテムを試すことに興味を持っており、これは彼らの体験を豊かにするだけでなく、私たちの大手商人ではなく、地元の商人や新しい商人にとっての機会を増やします。

<!-- ここまで読んだ! -->

## Conclusion 結論

We have demonstrated here the challenges, opportunities, and goals for homepage recommendations at DoorDash. 
私たちはここで、DoorDashにおけるホームページ推薦の課題、機会、目標を示しました。
Two machine learning approaches — including a deep-learning LTR UR model and a reinforcement learning algorithm UCB — have been integrated into our existing ranking framework. 
深層学習LTR URモデルと強化学習アルゴリズムUCBを含む2つの機械学習アプローチが、私たちの既存のランキングフレームワークに統合されました。
Through online experiments, we have proven that the ranking framework can efficiently rank various entities with a smart trade-off between exploitation and exploration to optimize consumer experience, improve marketplace diversity and fairness, and drive DoorDash’s long-term growth. 
オンライン実験を通じて、私たちはランキングフレームワークが、**消費者体験を最適化し、市場の多様性と公平性を改善し、DoorDashの長期的成長を促進するために、利用と探索の間で賢いトレードオフを持ってさまざまなエンティティを効率的にランク付けできること**を証明しました。

<!-- ここまで読んだ! -->

Our work to date shows positive results, but there are still potential improvements we can make. 
これまでの私たちの作業は良好な結果を示していますが、まだ改善の余地があります。
So far, we have only introduced exploration to vertical rankings. 
これまで、私たちは**垂直ランキング**にのみ探索を導入しました。
But it could be promising for horizontal ranking within high-level entities such as store and item carousels at the SPR stage and possibly for candidate retrieval during the FPR stage. 
しかし、SPR段階における店舗やアイテムカルーセルなどの**高レベルエンティティ内での水平ランキング**や、FPR段階での候補取得に対しても有望である可能性があります。
Note, too, that the current exploration coefficient is uniform for all consumers; 
また、現在の探索係数はすべての消費者に対して均一であることにも注意してください。
we could personalize it for different consumers based on their shopping behavior and exploration sensitivity. 
私たちは、消費者の購買行動や探索感度に基づいて、異なる消費者に対してそれをパーソナライズすることができます。
Ultimately, Thompson sampling could be an alternative to test against the current UCB approach. 
最終的には、Thompson samplingが現在のUCBアプローチに対抗するための代替手段となる可能性があります。

<!-- ここまで読んだ! -->
