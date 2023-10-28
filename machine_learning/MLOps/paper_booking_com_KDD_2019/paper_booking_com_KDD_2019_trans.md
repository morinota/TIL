## 0.1. link リンク

- https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf

## 0.2. title タイトル

150 Successful Machine Learning Models: 6 Lessons Learned at Booking.com
150の成功した機械学習モデル：
ブッキング・ドットコムで学んだ6つの教訓

## 0.3. abstruct abstruct

Booking.com is the world’s largest online travel agent where millions of guests find their accommodation and millions of accommodation providers list their properties including hotels, apartments, bed and breakfasts, guest houses, and more.
Booking.comは、何百万人ものゲストが宿泊施設を見つけ、何百万もの宿泊施設プロバイダーがホテル、アパートメント、ベッド＆ブレックファスト、ゲストハウスなどの物件を掲載している世界最大のオンライン旅行代理店です。
During the last years we have applied Machine Learning to improve the experience of our customers and our business.
ここ数年、私たちは機械学習を応用し、お客様の体験と私たちのビジネスを改善してきました。
While most of the Machine Learning literature focuses on the algorithmic or mathematical aspects of the field, not much has been published about how Machine Learning can deliver meaningful impact in an industrial environment where commercial gains are paramount.
**機械学習に関する文献のほとんどは、この分野のアルゴリズムや数学的な側面に焦点を当てているが、商業的な利益が最優先される産業環境において、機械学習がどのように有意義なインパクトをもたらすことができるかについては、あまり発表されていない。**
We conducted an analysis on about 150 successful customer facing applications of Machine Learning, developed by dozens of teams in Booking.com, exposed to hundreds of millions of users worldwide and validated through rigorous Randomized Controlled Trials.
私たちは、Booking.comの何十ものチームによって開発され、世界中の何億人ものユーザーに公開され、厳密なランダム化比較試験によって検証された、機械学習の顧客向けアプリケーションの成功例約150件の分析を行いました。
Following the phases of a Machine Learning project we describe our approach, the many challenges we found, and the lessons we learned while scaling up such a complex technology across our organization.
機械学習プロジェクトの段階を追って、私たちのアプローチ、私たちが発見した多くの課題、そして組織全体でこのような複雑なテクノロジーをスケールアップする際に学んだ教訓について説明します。
Our main conclusion is that an iterative, hypothesis driven process, integrated with other disciplines was fundamental to build 150 successful products enabled by Machine Learning.
我々の主な結論は、機械学習によって150の成功した製品を構築するためには、他の学問分野と統合された**反復的で仮説主導のプロセス(an iterative, hypothesis driven process)**が基本であったということである。

# 1. Introduction はじめに

Booking.com is the world’s largest online travel agent where millions of guests find their accommodation and millions of accommodation providers list their properties, including hotels, apartments, bed and breakfasts, guest houses, etc.
Booking.comは世界最大のオンライン旅行代理店で、何百万人ものゲストが宿泊施設を見つけ、何百万もの宿泊施設提供者がホテル、アパートメント、ベッド＆ブレックファスト、ゲストハウスなどの物件を掲載しています。
Our platform is developed by many different interdisciplinary teams working on different products, ranging from a large new application like our recent Booking Assistant, or an important page of the website with rich business value like the search results page, to a part of it, like the destinations recommendations displayed at the bottom.
私たちのプラットフォームは、最近の予約アシスタントのような大規模な新しいアプリケーションから、検索結果ページのようなビジネス価値の高いウェブサイトの重要なページ、あるいは下部に表示されるお勧めの目的地のようなその一部まで、さまざまな製品に取り組む多くの異なる学際的なチームによって開発されています。
Teams have their own goals, and use different business metrics to quantify the value the product delivers and to test hypotheses, the core of our learning process.
チームにはそれぞれの目標があり、**さまざまなビジネス指標を使用して、製品が提供する価値を定量化**し、学習プロセスの中核である仮説を検証する。
Several issues make our platform a unique challenge, we briefly describe them below:
私たちのプラットフォームをユニークなものにしているいくつかの問題があるので、以下に簡単に説明する：

**High Stakes**:
高いリスク：
Recommending the wrong movie, song, book, or product has relevant impact in the consumer experience.
間違った映画、歌、本、商品を推薦することは、消費者の体験に影響を与えます。
Nevertheless, in most cases there is a way to “undo” the selection: stop listening to a song or watching a movie, even returning a unsatisfactory product.
とはいえ、ほとんどの場合、選択を「取り消す」方法がある：
曲を聴いたり映画を観たりするのをやめたり、満足のいかない製品を返品したりすることもできる。
But once you arrive to an accommodation that does not meet your expectations, there is no easy undo option, generating frustration and disengagement with the platform.
しかし、一旦期待に沿わない宿泊施設に到着すると、簡単に元に戻すオプションはなく、プラットフォームに対する不満や離脱を生む。

**Infinitesimal Queries**: Users searching for accommodations barely specify their destination, maybe the dates and number of guests.
ごくわずかなクエリー：
宿泊施設を検索するユーザは、目的地、日付、宿泊人数を指定するのがやっとです。
Providing satisfying shopping and accommodation experiences starting from this almost-zero-query scenario is one of the key challenges of our platform.
このほとんどゼロに近いクエリのシナリオから出発して、満足のいくショッピングと宿泊体験を提供することが、私たちのプラットフォームの重要な課題のひとつです。

**Complex Items**: Booking an accommodation requires users to decide on several aspects like destination, dates, accommodation type, number of rooms, room types, refund policies, etc.
複雑な項目：
宿泊施設の予約には、目的地、日程、宿泊施設のタイプ、部屋数、部屋のタイプ、返金ポリシーなど、いくつかの点をユーザが決定する必要があります。
These elements define a multi-dimensional space where bookable options are located, and since not all possible combinations exist, it is not trivial to navigate; users need help to find the best combination.
これらの要素は、予約可能なオプションが配置されている多次元空間を定義しており、すべての可能な組み合わせが存在するわけではないので、ナビゲートするのは簡単ではない。

**Constrained Supply**: Accommodations have limited and dynamic availability.
供給の制約：
宿泊施設の供給は限られており、かつダイナミックである。
Its interaction with prices directly affects guest preferences and the behavior of accommodation providers.
価格との相互作用は、宿泊客の嗜好や宿泊施設提供者の行動に直接影響する。
This aspect cannot be neglected when designing the shopping experience.
ショッピング体験をデザインする上で、この点を無視することはできない。

**Continuous Cold Start**: Guests are in a continuous cold start state [2].
連続コールドスタート：
ゲストは連続コールドスタート状態にある[2]。
Most people only travel once or twice every year.
ほとんどの人は年に1度か2度しか旅行しない。
By the time they come back to our web site their preferences might have changed significantly; long in the past history of users is usually irrelevant.
彼らが私たちのウェブサイトに戻ってくる頃には、彼らの好みは大きく変わっているかもしれません。
Furthermore, new accommodations and new accommodation types are added to the supply every day, their lack of reviews and general content, such as pictures and multilingual descriptions, make it difficult to give them visibility.
さらに、新しい宿泊施設や新しいタイプの宿泊施設が毎日のように追加されるため、写真や多言語説明などのレビューや一般的なコンテンツが不足しており、それらを認知させることが難しくなっている。
Providing a personalized experience regardless of how often a guest interacts with Booking.com and being capable to find an audience for every property from the very beginning of them joining Booking.com are difficult and important problems we face.
お客様がBooking.comとどれくらいの頻度でやりとりしているかにかかわらず、パーソナライズされた体験を提供すること、そして、お客様がBooking.comに入会した当初から、すべての物件の利用者を見つけることができるようにすることは、私たちが直面している困難かつ重要な問題です。

**Content Overload**: Accommodations have very rich content, e.g.descriptions, pictures, reviews and ratings.
コンテンツ過多：
宿泊施設には、説明、写真、レビュー、評価など、非常に豊富なコンテンツがあります。
Destinations themselves also have rich content including visitor authored pictures, free text reviews, visitors endorsements and guides.
目的地自体も、訪問者が執筆した写真、自由なテキストによるレビュー、訪問者の推薦、ガイドなど、豊富なコンテンツを持っている。
This is a powerful advertising tool, but also very complex and difficult to be consumed by guests.
これは強力な広告ツールだが、非常に複雑で、ゲストに消費されにくい。
Successfully exploiting such rich content by presenting it to users in an accessible and relevant way is another key challenge of our platform.
このような豊富なコンテンツを、アクセスしやすく関連性のある方法でユーザーに提示することによってうまく利用することも、私たちのプラットフォームの重要な課題です。

During the last years we have applied Machine Learning techniques to address these and other issues.
ここ数年、私たちは機械学習技術を応用して、こうした問題やその他の問題に取り組んできた。
We found that driving true business impact is amazingly hard, plus it is difficult to isolate and understand the connection between efforts on modeling and the observed impact.
私たちは、真のビジネスインパクトを推進することは驚くほど難しく、さらにモデリングへの取り組みと観察されたインパクトとの関連性を切り分け、理解することは困難であることを発見した。
Similar issues have been highlighted by a few authors in the last years.
同様の問題は、ここ数年、何人かの著者によって強調されてきた。
Wagstaff position paper [13] mentions the lack of studies and lessons on how to exploit Machine Learning and achieve relevant impact in real world problems.
Wagstaffのポジションペーパー[13]は、機械学習をどのように活用し、実世界の問題で適切なインパクトを達成するかについての研究や教訓の不足に言及している。
In an example closer to our industry, Jannach et al.[5] explain how the field of recommender systems provides little guidance to impact metrics relevant to service providers, such as sales diversification, conversion rate or loyalty.
我々の業界に近い例では、Jannachら[5]が、**レコメンダー・システムの分野が、売上の多様化、コンバージョン率、ロイヤリティといったサービス・プロバイダーに関連する指標に影響を与える指針をほとんど提供していない**ことを説明している。
Many other publications have described specific use cases of machine learning and their impact on business metrics (e.g.[10]) but no previous work to our knowledge has studied the overall process of developing and testing products to obtain business and user value through Machine Learning.
他の多くの出版物は、機械学習の特定のユースケースとビジネス・メトリクスへの影響を記述している（例えば[10]）が、我々の知る限り、機械学習を通じてビジネスとユーザの価値を得るための製品開発とテストの全体的なプロセスを研究した先行研究はない。

In this work we analyze 150 successful customer facing applications of Machine Learning techniques (plus many associated failures), and share the challenges we found, how we addressed some of them, lessons that we got along the way, and general recommendations.
この作品では、機械学習技術の顧客向けアプリケーションで成功した150の事例（それに付随する多くの失敗事例）を分析し、我々が発見した課題、そのいくつかにどのように対処したか、その過程で得た教訓、そして一般的な推奨事項を共有する。
Our contributions are:
我々の貢献は以下の通りである：

- A large scale study on the impact of Machine Learning in a commercial product, to our knowledge the first one in the field 商業製品における機械学習の影響に関する大規模な調査。

- A collection of "lessons learned" covering all the phases of a machine learning project 機械学習プロジェクトの全段階を網羅した「教訓集

- A set of techniques to address the challenges we found within each project phase プロジェクトの各段階で見つかった課題に対処するための一連のテクニック

The rest of the paper is organized as a set of lessons associated to a specific phase of the development process of a Machine Learning project, namely Inception, Modeling, Deployment, Monitoring and Evaluation, and a final section where we present our conclusions.
本稿の残りの部分は、機械学習プロジェクトの開発プロセスの特定のフェーズ、すなわち **Inception(開始)、Modeling、Deployment、Monitoring、Evaluation に関連する一連の教訓**として構成されており、最後のセクションでは結論を述べている。

# 2. Inception: Machine Learning as a Swiss Knife for Product Development 開始: 製品開発のためのスイスナイフ(=多機能で色んな用途に使える例え)としての機械学習

During the inception phase of a Machine Learning based project, a product team produces ideas, hypotheses, business cases, etc., where Machine Learning fits as part of the solution.
機械学習ベースのプロジェクトの開始段階では、製品チームは、機械学習がソリューションの一部として適合するアイデア、仮説、ビジネスケースなどを作成する。
One important lesson we have learned is that Machine Learning can be used for many and very different products in widely different contexts.
我々が学んだ重要な教訓のひとつは、機械学習は多くの、そして非常に異なる製品を、大きく異なる文脈で使うことができるということだ。
In practice, our models are tools that help different teams improve their products and learn from their users.
実際には、私たちのモデルは、さまざまなチームが製品を改善し、ユーザから学ぶのを助けるツールです。
At one extreme, we create models which are very specific for a use case.
ある極端な例では、ユースケースに特化したモデルを作成する。
For instance, they optimize the size of an specific element of the user interface, or provide recommendations tailored for one point on the funnel and one specific context.
例えば、ユーザインターフェースの特定の要素のサイズを最適化したり、ファネルのあるポイントや特定のコンテキストに合わせた推薦を提供したりする。
Because of their specificity, we can design and tune them to achieve good performance, hoping to create a strong business impact.
その特異性ゆえに、私たちは優れたパフォーマンスを達成するために設計し、調整することができる。
The counterside is that their breadth of application is limited to a few use cases.
その反面、その応用範囲はいくつかのユースケースに限られる。

At the opposite end of the spectrum we also create models which act as a meaningful semantic layer.
その反対に、意味のあるセマンティック層として機能するモデルも作成する。(=ex. 特徴量を作るモデルとか??)
They model understandable concepts, enabling everyone involved in product development to introduce new features, personalization, persuasion messages, etc., based on the output of the model.
**理解しやすいコンセプトをモデル化すること(定量化できていないユーザの特徴を、MLモデルを使ってモデル化する、みたいな??:thinking:)**で、商品開発に携わるすべての人が、モデルの出力に基づいて新機能やパーソナライゼーション、説得力のあるメッセージなどを導入できるようになる。
They could for instance indicate how flexible a user is with respect to the destination of their trip, giving product teams a concept of destination-flexibility that they can use to improve their products.
例えば、ユーザが旅行の目的地に対してどの程度フレキシブルであるかを示し、プロダクトチームにdestination-flexibilityの概念を与えることで、プロダクトの改善に役立てることができる。
Such models provide an interpretable signal, valid under all the contexts where the product teams would like to use them.
このようなモデルは、製品チームが使用したいすべてのcontextで有効な、解釈可能なシグナル(=出力?)を提供する。(ユーザの特徴量を作るモデル、みたいな??:thinking:)
This requirement limits the coupling between model prediction and specific target business metrics, but this is counteracted by the broad adoption such models have, generating often dozens of use cases all over the platform.
この要件は、モデル予測と特定のターゲットビジネスメトリックスとの間の結合を制限するが、これは、そのようなモデルが広く採用され、多くの場合、プラットフォーム上のすべてのユースケースを生成することによって打ち消される。
Concretely, in our analysis we found that on average each semantic model generated twice as many use cases as the specialized ones.
具体的には、我々の分析では、各**semanticモデル**(=意味モデル?)は平均して、特化されたものよりも2倍のユースケースを生成することがわかった。

## 2.1. Model Families モデルファミリー

The following paragraphs explore different families of models currently deployed in our platform, focusing on how they can be used by product teams to influence our customers.
以下の段落では、当社のプラットフォームで現在展開されているさまざまなモデル・ファミリーを、製品チームが顧客に影響を与えるためにどのように使用できるかに焦点を当てて探ります。
This categorization works as a tool to generate ideas to exploit the capabilities of Machine Learning, forming the backbone of our strategy to address the issues described in the introduction.
この分類は、機械学習の能力を活用するためのアイデアを生み出すツールとして機能し、冒頭で述べた問題に対処するための戦略の骨格を形成する。

### 2.1.1. Traveller Preference Models. 旅行者の嗜好モデル。

Users display different levels of flexibility on different aspects, from no flexibility at all to complete indifference.
まったく融通が利かないものからまったく無関心なものまで、ユーザはさまざまな面で異なるレベルの flexibility(融通性)を示す。
We consider several trip aspects like destination, property price, property location, quality, dates, and facilities among others, and build several Machine Learning models that, in combination, construct a user preference profile assigning a flexibility level to each aspect.
私たちは、目的地、物件の価格、物件の場所、品質、日付、設備など、いくつかの旅行のaspectを考慮し、組み合わせて、各aspectに flexibilityレベルを割り当てる**ユーザの嗜好プロファイルを構築するいくつかの機械学習モデル**を構築します。(なるほど...! この例は、section2の冒頭で紹介されたsemantic modelの話か...!:thinking:)(逆に、二段階推薦の2段階目はsemantic modelに該当しない認識。CTR予測モデルとかだし:thinking:)
Models in this family work as a semantic layer.
**このファミリーのモデルは semantic layer として機能する**。
As an example the Dates Flexibility model gives a measure of how flexible a user is about traveling dates.
例えば、「日付の柔軟性」モデルは、ユーザが旅行の日付に対してどの程度柔軟であるかを示すものである。
If a user is flexible, dates recommendations might be relevant in some situations, but if the user is not flexible, date recommendations might turn out distracting and confusing, and are therefore not displayed.
ユーザが柔軟であれば、日付の推薦は状況によっては適切かもしれないが、ユーザーが柔軟でない場合、日付の推薦は気が散って混乱を招く可能性があるため、表示されない。
Another treatment could focus on inflexible users, re-enforcing the chosen dates with relevant information like price trends or availability
また、融通の利かないユーザに焦点を当て、価格動向や空席状況などの関連情報を使って、選択した日程を再強化することもできる。

### 2.1.2. Traveller Context Models. トラベラーのコンテキストモデル。

Travellers travel as couples, as families, with a group of friends or alone, either for leisure or for business.
旅行者は、カップル、家族、友人同士、あるいは一人で、レジャーやビジネスのために旅行する。
They might go by car to a close by city or by plane to the other side of the world, and visit one single city for a long stay or several cities one after the other for shorter periods.
車で近郊の都市に行くこともあれば、飛行機で地球の裏側に行くこともあり、ひとつの都市に長期滞在することもあれば、複数の都市を次々と短期滞在することもある。
All of these are examples of what we call Traveller Context, which is a theme of the trip that defines constraints and requirements.
これらはすべて、私たちが"Traveller Context"と呼ぶものの一例であり、制約や要件を定義する旅のテーマである。
Most of these contexts are not explicitly stated in our platform, and the ones that can be specified, are usually omitted by most users.
**これらのcontextのほとんどは、私たちのプラットフォームでは明示されておらず**、指定できるものでも、ほとんどのユーザは通常省略している。
Thus, predicting, or guessing the context of the current user, as early in the shopping experience as possible, is highly valuable.
したがって、**ショッピング体験のできるだけ早い段階で、現在のユーザのcontextを予測する、あるいは推測することは、非常に価値がある**。
The Traveller Context Models also work as a semantic layer, in this case, enabling teams to create features for specific contexts.
トラベラーコンテキストモデルは、**semantic layer としても機能する**。(=**あるusecaseに特化したモデルでありながら、且つ汎用的な意味情報を提供するsemantic layerに属するモデルでもあるのか。確かにそんなケースもあるよなぁ**...:thinking:)
As an example consider the Family Traveller Model, that estimates how likely is that a user is shopping for a family trip.
例として、ユーザが家族旅行のために買い物をする可能性を推定する「家族旅行者モデル」を考えてみよう。
Usually, Family Travellers forget to fill in the number of children they travel with (see Figure 1(a)), going through a big part of the shopping process only to find out that the chosen property is out of availability for their children.
通常、家族旅行者は子供の人数を記入するのを忘れ（図1(a)参照）、ショッピング・プロセスの大部分を経た後、選択した宿泊施設が子供の宿泊に空きがないことを知る。
The Family Traveller Model is used to remind the user to fill in the children information as early in the experience as possible, hopefully, removing frustration.
ファミリー・トラベラー・モデル」は、できるだけ早い段階で子どもたちの情報を記入するよう利用者に注意を促し、フラストレーションを取り除くために使用される。

### 2.1.3. Item Space Navigation Models. アイテムスペースナビゲーションモデル。

Most users who browse our inventory navigate through several supplementary and complementary options and items, such as dates, properties, policies, locations, etc.
当社のインベントリーを閲覧するほとんどのユーザは、日付、物件、ポリシー、ロケーションなど、いくつかの補足的、補完的なオプションや項目をナビゲートします。
In order to make a choice, they need to keep track of the options they have seen, while exploring neighbouring ones and trying to make a purchase decision.
選択するためには、自分が見た選択肢を追跡し、隣の選択肢を探しつつ、購入の決断を下す必要がある。
Our item space navigation models both feed from this process and try to guide it.
私たちのアイテムスペース・ナビゲーション・モデルは、このプロセスから情報を得て、それを導こうとする。
They treat different actions, like scrolling, clicking, sorting, filtering etc., as implicit feedback about the user preferences.
**スクロール、クリック、ソート、フィルタリングなどのさまざまなアクションを、ユーザの好みに関する暗黙のフィードバックとして扱う**。
These signals can then be used to facilitate access to the most relevant items in the user history, as well as to surface other relevant items in our inventory.
これらのシグナルは、ユーザ履歴の中で最も関連性の高いアイテムへのアクセスを容易にしたり、インベントリの中で他の関連性の高いアイテムを表示したりするために使用される。

### 2.1.4. User Interface Optimization Models. ユーザーインターフェースの最適化モデル。

Font sizes, number of items in a list, background colors or images, the presence or absence of a visual element, etc., all have big impact in user behaviour as measured by business metrics.
フォントサイズ、リスト内の項目数、背景色や画像、ビジュアル要素の有無など、すべてがビジネス指標で測定されるユーザ行動に大きな影響を与えます。
Models in this family directly optimize these parameters with respect to a specific target business metric.
このファミリーのモデルは、特定の目標ビジネス指標に関して、これらのパラメータを直接最適化する。
We found that it is hardly the case that one specific value is optimal across the board, so our models consider context and user information to decide the best user interface.
そのため、私たちのモデルは、コンテキストとユーザ情報を考慮して、最適なユーザーインターフェースを決定します。

### 2.1.5. Content Curation. コンテンツ・キュレーション。

Content describing destinations, landmarks, accommodations, etc., comes in different formats like free text, structured surveys and photos; and from different sources like accommodation managers, guests, and public databases.
目的地、ランドマーク、宿泊施設などを説明するコンテンツは、フリーテキスト、構造化された調査、写真などさまざまな形式で提供され、宿泊施設の管理者、宿泊客、公的データベースなどさまざまな情報源から提供される。
It has huge potential since it can be used to attract and advertise guests to specific cities, dates or even properties, but it is also very complex, noisy and vast, making it hard to be consumed by users.
特定の都市、日付、あるいは物件にゲストを誘致し、宣伝するために使用できるため、大きな可能性を秘めているが、非常に複雑で騒々しく、膨大であるため、ユーザに消費されにくいという欠点もある。
Content Curation is the process of making content accessible to humans.
**Content Curationとは、コンテンツを人間がアクセスできるようにするプロセス**である。
For example, we have collected over 171M reviews in more than 1.5M properties, which contain highly valuable information about the service a particular accommodation provides and a very rich source of selling points.
例えば、私たちは150万件以上の宿泊施設の1億7100万件以上のレビューを収集しており、**これらのレビューには特定の宿泊施設が提供するサービスに関する非常に価値の高い情報が含まれており**、セールスポイントの非常に豊富な情報源となっています。
A Machine Learning model "curates" reviews, constructing brief and representative summaries of the outstanding aspects of an accommodation (Figure 1(b)).
**機械学習モデルがレビューを「キュレーション」し、宿泊施設の優れた点を簡潔かつ代表的に要約する**(図1(b))。(コメントのキュレーション的な...!コメントって、ニュースに対するレビューとも言えるのかな)

### 2.1.6. Content Augmentation. コンテンツの補強。

The whole process of users browsing, selecting, booking, and reviewing accommodations, puts to our disposal implicit signals that allow us to construct deeper understanding of the services and the quality a particular property or destination can offer.
ユーザが宿泊施設をブラウズし、選択し、予約し、レビューするプロセス全体は、特定の施設や目的地が提供できるサービスや品質をより深く理解することを可能にする、暗黙のシグナル(implicit feedback?)を私たちが自由に使えるようにする。
Models in this family derive attributes of a property, destination or even specific dates, augmenting the explicit service offer.
このファミリーのモデルは、物件、目的地、あるいは特定の日付の属性を導き出し、明示的なサービス提供を補強する。
Content Augmentation differs from Content Curation in that curation is about making already existing content easily accessible by users whereas augmentation is about enriching an existing entity using data from many others.
**Content Augmentation が Content Curation と異なる点は、キュレーションが既存のコンテンツにユーザが簡単にアクセスできるようにすることであるのに対し、オーグメンテーションは既存のエンティティを他の多くのデータを使って充実させることである**。
To illustrate this idea, we give two examples:
この考えを説明するために、2つの例を挙げる：

- Great Value: Booking.com provides a wide selection of properties, offering different levels of value in the form of amenities, location, quality of the service and facilities, policies, and many other dimensions. Users need to assess how the price asked for a room relates to the value they would obtain. "Great Value Today" icons simplify this process by highlighting properties offering an outstanding value for the price they are asking, as compared to other available options. A machine learning model analyses the value proposition of millions of properties and the transactions and ratings of millions of users and selects the subset of properties with a "Great Value" offer.
- お得：Booking.comは、アメニティ、立地、サービスや施設の質、ポリシーなど、さまざまな観点からさまざまなレベルの価値を提供する、幅広い選択肢を提供しています。 利用者は、部屋に対する要求価格と得られる価値との関係を見極める必要がある。 「Great Value Today "のアイコンは、他の選択肢と比較して、提示価格に対して優れた価値を提供する物件を強調することで、このプロセスを簡素化します。 機械学習モデルは、数百万件の物件の価値提案と数百万人のユーザの取引と評価を分析し、「お得な」オファーを提供する物件のサブセットを選択する。

- Price Trends: Depending on the anticipation of the reservation, the specific travelling dates and the destination, among other aspects, prices display different dynamics. Since we have access to thousands of reservations in each city every day, we can build an accurate model of the price trend of a city for a given time and travelling dates. When the model finds a specific trend, we inform the users to help them make a better decision, either by encouraging them to choose a destination and dates that look like an opportunity, or discouraging particular options in favor of others. Note that in this case, the augmented item is not an accommodation but a destination (see Figure 1(c)).
- 価格動向:予約の時期、旅行日、目的地などによって、価格は異なる動きを見せる。 各都市の何千件もの予約に毎日アクセスしているため、指定された時間と旅行日程におけるその都市の価格動向の正確なモデルを構築することができます。 モデルが特定の傾向を見つけると、私たちはユーザに情報を提供し、チャンスがありそうな目的地や日程を選ぶように促したり、特定の選択肢を控えて他の選択肢を優先させたりすることで、より良い決断ができるように支援する。 この場合、拡張されたアイテムは宿泊施設ではなく、目的地であることに注意（図1(c)参照）。

## 2.2. All model families can provide value すべてのモデル・ファミリーが価値を提供できる

![fig2]()

Each family of Machine Learned Models provides business value.
機械学習モデルの各ファミリーは、ビジネス上の価値を提供する。
This is reflected in Figure 2 where each bar represents the relation between the median improvement on one of our core metrics by a model family and a baseline computed as the median improvement on the same metric for of all the successful projects (machine learning based or not), on a comparable period.
これは図2に反映されており、各バーは、各model familyによるコアメトリクスの1つに関する改善の**中央値**と、比較可能な期間において成功したすべてのプロジェクト(機械学習ベースかどうかにかかわらず)の同じメトリクスに関する改善の**中央値**として計算されたベースライン(1.0)との関係を表している。
Most of the families contribution are above the benchmark, one is below, but all of them make a significant contribution, and the collective effect is clearly positive.
ほとんどの model family の貢献度はベンチマークを上回っており、1つのmodel family は下回っているが、どのmodel familyも大きな貢献をしており、総合的な効果は明らかにプラスである。

The graph mentioned above shows the direct impact of Machine Learning based projects, measured at their introduction or when improving the model behind them.
上述したグラフは、機械学習ベースのプロジェクトがもたらす直接的な影響を、その**導入時またはその背後にあるモデルの改善時に測定したもの**である。
We have also observed models becoming the foundation of a new product, enabling value generation through other product development disciplines.
また、機械学習モデルが新製品の基礎となり、他の製品開発分野を通じて価値創造を可能にすることも観察されている。(semantic modelの話だと思う)
Such indirect impact is hard to quantify, but the multiplying effect is clear and it is a concept that product teams exploit.
このような間接的な影響を定量化するのは難しいが、乗数効果は明らかであり、製品チームが利用する概念である。
As an example, Figure 3 illustrates the iterative process of the development of a destinations recommendations system.
一例として、図3は観光地推薦システムの開発における反復プロセスを示している。
Each bar represents a successful iteration starting from the top and focusing on one aspect of the product: User Interface, Target Audience, Copy (captions, descriptions, messages, etc.), or the Algorithm itself.
各バーは、製品の1つの側面に焦点を当て、上から始めて成功した反復を表しています：
ユーザインターフェース、ターゲットオーディエンス、コピー（キャプション、説明文、メッセージなど）、またはアルゴリズムそのものです。
The length of the bar indicates the relative (all statistical significant) impact relative to the first iteration.
棒の長さは、最初のiterationに対する相対的な（すべて統計的に有意な）影響を示す。
All these improvements were enabled by the first algorithm, illustrating the indirect impact of Machine Learning projects through other disciplines.
これらの改善はすべて最初のアルゴリズムによって可能になったものであり、機械学習プロジェクトが他の分野を通じて間接的に影響を及ぼしていることを示している。

![fig3]()

Figure 3: A sequence of experiments on a Recommendations Product. Each experiment tests a new version focusing on the indicated discipline or ML Problem Setup. The length of the bar is the observed impact relative to the first version (all statistically significant)
図3：レコメンデーション製品に関する一連の実験。各実験は、指定された分野やML問題設定に焦点を当てた新しいバージョンをテストする。棒の長さは、最初のバージョンと比較して観察されたインパクトである（すべて統計的に有意）。

# 3. Modeling: Offline Model Performance Is Just A Health Check モデリング: オフラインでのモデルのパフォーマンスは健康診断に過ぎない

![fig4]()

A common approach to quantify the quality of a model is to estimate or predict the performance the model will have when exposed to data it has never seen before.
モデルの品質を定量化するための一般的なアプローチは、モデルが見たことのないデータにさらされたときの性能を推定または予測することである。
Different flavors of cross-validation are used to estimate the value of a specific metric that depends on the task (classification, regression, ranking).
タスク（分類、回帰、ランキング）に依存する特定のメトリックの値を推定するために、さまざまなクロスバリデーションが使用される。
In Booking.com we are very much concerned with the value a model brings to our customers and our business.
Booking.comでは、**あるモデルがお客様と私たちのビジネスにもたらす価値を非常に重視**しています。
Such value is estimated through Randomized Controlled Trials (RCTs) and specific business metrics like conversion, customer service tickets or cancellations.
このような価値は、**ランダム化比較試験(RCT)と**、コンバージョン、カスタマー・サービス・チケット、キャンセルなどの**特定のビジネス指標を通じて推定される**。
A very interesting finding is that increasing the performance of a model, does not necessarily translates to a gain in value.
非常に興味深い発見は、モデルの性能を上げても、必ずしも価値が上がるとは限らないということだ。
Figure 4 illustrates this learning.
図4は、この学習を示している。
Each point represents the comparison of a successful model that proved its value through a previous RCT, versus a new model.
各ポイントは、以前のRCTによってその価値が証明された成功モデルと、新しいモデルの比較を表している。
The horizontal coordinate is given by the relative difference between the new model and the current baseline according to an offline estimation of the performance of the models.
水平座標は、モデルの性能のオフライン推定による、新しいモデルと現在のベースラインとの相対的な差で与えられる。
This data is only about classifiers and rankers, evaluated by ROC AUC and Mean Reciprocal Rank respectively.
このデータはclassifiers(分類モデル)とrankers(ランキングモデル)に関するもので、それぞれROC AUCと Mean Reciprocal Rank(平均逆順位)で評価される。
The vertical coordinate is given by the relative difference in a business metric of interest as observed in a RCT where both models are compared (all models aim for the same business metric).
縦座標は、両モデルを比較したRCTで観察された、関心のあるビジネス指標の相対的な差で与えられる(すべてのモデルは同じビジネス指標を目指している)。
We include a total of 23 comparisons (46 models).
合計23の比較（46モデル）を含む。
Visual inspection already shows a lack of correlation, deeper analysis shows that the Pearson correlation is -0.1 with 90% confidence interval (-0.45, 0.27), and Spearman correlation is -0.18 with 90% confidence interval (-0.5, 0.19).
目視ではすでに相関がないことがわかるが、より深く分析すると、**ピアソン相関は-0.1**、90％信頼区間（-0.45、0.27）、**スピアマン相関は-0.18**、90％信頼区間（-0.5、0.19）である。
We stress that this lack of correlation is not between offline and online performance, but between offline performance gain and business value gain.
この相関性の欠如は、**オフラインとオンラインのパフォーマンス(=自主練は上手だけど本番は下手くそ、みたいな話)ではなく、オフラインでのパフォーマンス向上とビジネス価値向上の間にあることを強調する**。
At the same time we do not want to overstate the generality of this result, the external validity can be easily challenged by noting that these models work in a specific context, for a specific system, they are built in specific ways, they all target the same business metric, and furthermore they are all trying to improve it after a previous model already did it.
同時に、**我々はこの結果の一般性を誇張したくはない**。これらのモデルは特定の文脈、特定のシステムで動作し、特定の方法で構築され、すべて同じビジネス指標をターゲットにしており、さらに、それらはすべて以前のモデルがすでにそれを行った後にそれを改善しようとしていることに注目することで、外的妥当性は容易に異議を唱えることができる。
Nevertheless we still find the lack of correlation a remarkable finding.
とはいえ、相関がないことは注目に値する。
In fact, such finding led us to investigate other areas of Booking.com and consistently found the same pattern.
実際、このような発見をきっかけに、Booking.comの他のエリアも調査したところ、一貫して同じパターンが見つかりました。
For example [8] highlights that the standard performance metric for Machine Translation (BLEU) exhibits a “rather tenuous” correlation with human metrics.
例えば、[8]は、機械翻訳の標準的なパフォーマンス指標(BLEU)は、人間のメトリックと "むしろ微妙な "相関性を示すことを強調している。
Only where the offline metric is almost exactly the business metric, a correlation can be observed.
**オフライン指標がビジネス指標とほぼ一致する場合のみ、相関関係が観察される**。

This phenomenon can be explained by different factors, we list the ones we found most relevant to share:
この現象は、さまざまな要因によって説明することができる：

- Value Performance Saturation: It is clear that there are business problems for which it is not possible to drive value from model performance gains indefinitely, at some point the value vs performance curve saturates, and gains in performance produce no value gain, or too small gains, impossible to detect in an RCT in reasonable time. バリュー・パフォーマンスの飽和: ある時点で、価値対パフォーマンス曲線(x軸=オフライン性能、y軸=ビジネス価値)は飽和し、パフォーマンスの向上は価値の向上をもたらさないか、あるいは小さすぎる向上しかもたらさないため、妥当な時間内にRCTで検出することは不可能である。

- Segment Saturation: when testing a new model against a baseline we apply triggered analysis to make sure we only consider the users exposed to a change, that is, users for which the models disagree. As models improve on each other, this disagreement rate goes down, reducing the population of users that are actually exposed to a treatment, and with that, the power to detect gains in value. More details about how we test competing models can be found in Section 7.4. セグメントの飽和:ベースラインに対して新しいモデルをテストする場合、トリガー分析を適用して、変化にさらされたユーザ、つまりモデルが不一致のユーザーのみを考慮するようにする。 モデルが改良されるにつれて、この不一致率は低下し、実際に治療にさらされるユーザーの母集団が減少し、それに伴って**価値の向上を検出する力も低下する**。 競合モデルのテスト方法についての詳細は、セクション7.4にある。

- Uncanny Valley effect: as models become better and better, they seem to know more and more about our users, or can predict very well what the user is about to do. This can be unsettling for some of our customers (see Figure 5 and [10]), which likely translates to a negative effect on value. 不気味の谷効果: モデルがだんだん良くなるにつれて、ユーザのことがだんだんわかるようになったり、ユーザが何をしようとしているのかよく予測できるようになったりする。 これは、一部のユーザにとっては不安なこと(=予測があたりすぎて怖い、って話...!)であり（図5と[10]を参照）、価値に悪影響を及ぼす可能性が高い。

- Proxy Over-optimization: Usually, our Machine Learned models are supervised models that maximize certain observed variable, but not necessarily the specific objective business metric. For example, we might build a recommender system based on Click Through Rate because we know that CTR has a strong correlation or even causation with Conversion Rate, the business metric we really care about in this case. But as models get better and better, they might end up “just driving clicks”, without any actual effect on conversion. An example of this is a model that learned to recommend very similar hotels to the one a user is looking at, encouraging the user to click (presumably to compare all the very similar hotels), eventually drowning them into the paradox of choice and hurting conversion. In general, over-optimizing proxies leads to distracting the user away from their goal. プロキシの過剰最適化: 通常、**機械学習モデルは特定の観測変数を最大化する教師ありモデルであるが、必ずしも特定の目的ビジネス指標を最大化するものではない**。 例えば、クリック率（Click Through Rate）に基づいてレコメンダー・システムを構築するかもしれません。なぜなら、CTRはコンバージョン率（Conversion Rate）と強い相関関係、あるいは因果関係があることがわかっているからです。 しかし、モデルがどんどん良くなるにつれて、コンバージョンに実際の効果がないまま、「クリックを促すだけ」で終わってしまうかもしれない。 この例としては、ユーザが見ているホテルと非常によく似たホテルを推薦することを学習したモデルがあり、ユーザにクリックを促し（おそらく非常によく似たホテルをすべて比較するため）、最終的には選択のパラドックスに溺れさせ、コンバージョンを阻害する。 一般的に、プロキシを過剰に最適化することは、ユーザを目的から遠ざけることにつながる。(CTRを上げることに特化したモデルだったら、ビジネス指標が上がるとは限らない。)

It is challenging to address each of this issues on its own.
それぞれの問題に単独で取り組むのは難しい。
Our approach relies on a fast cycle of developing hypotheses, building minimum models to test them in experiments, and using the results to keep iterating.
**私たちのアプローチは、仮説を立て、それを実験で検証するための最小限のモデルを構築し、その結果を使って反復を続けるという高速サイクルに依存している。**
Offline model performance metrics are only a health check, to make sure the algorithm does what we want to.
**オフラインモデルのパフォーマンス測定基準は、アルゴリズムが私たちの望むことを行っているかどうかを確認するための、健康チェックに過ぎない**。(まあでも健康チェックも大事だよなぁ...。品質保証というか。)
This cycle drives us to focus on many aspects of the product development process besides the offline model performance, multiplying the iterative process along many dimensions.
このサイクルによって、私たちはオフラインモデルの性能以外にも、製品開発プロセスの多くの側面に焦点を当てるようになり、反復プロセスが多次元に及ぶことになる。
These include the Problem Construction Process described in the following section, qualitative aspects of a model (like diversity, transparency, adaptability, etc.), experiment design and latency.
これには、次のセクションで説明する問題構築プロセス、モデルの質的側面(多様性、透明性、適応性など)、実験デザイン、レイテンシーなどが含まれる。
As an example consider a recommender system that predicts the rating a user would give to an accommodation.
例として、ユーザが宿泊施設に与えるであろう評価を予測する推薦システムを考えてみよう。
Minimizing RMSE looks like a reasonable approach.
RMSEを最小化するのは合理的なアプローチに見える。
After a few successful iterations we hypothesize that the model is lacking diversity, so we create a challenger model that although still minimizes RMSE, somehow produces higher diversity.
数回の反復に成功した後、このモデルには多様性が欠けているという仮説を立て、RMSEを最小化しつつも、より高い多様性を生み出すチャレンジャー・モデルを作成する。
It is likely that this new model has a higher RMSE, but as long as it succeeds at increasing diversity and gives a reasonable RMSE, it will be used to test the hypothesis “diversity matters”.
この新しいモデルはRMSEが高い可能性が高いが、多様性を高めることに成功し、妥当なRMSEを与える限り、「多様性が重要である」という仮説を検証するために使用される。
Inconclusive results might point to adjustments of the model or experiment design, to make sure we give the hypothesis a fair chance.
結論の出ない結果は、仮説に公平なチャンスを与えるために、モデルや実験デザインの調整を指摘するかもしれない。
Negative results will likely reject the concept.
否定的な結果は、コンセプトを否定する可能性が高い。
Positive results on the other hand, will encourage diversity related changes, not only in the model but also in the User Interface, and even the product as a whole.
一方、ポジティブな結果は、モデルだけでなく、ユーザー・インターフェース、さらには製品全体にも、多様性に関連した変化を促すことになる。

# 4. Modeling:Before Solving A Problem, Design It モデリング：問題を解決する前に、それをデザインする

The Modeling phase involves building a Machine Learning model that can contribute in solving the business case at hand.
モデリング・フェーズでは、目の前のビジネス・ケースの解決に貢献できる機械学習モデルを構築する。
A basic first step is to “set up” a Machine Learning Problem, and we learned that focusing on this step is key.
**基本的な最初のステップは、機械学習問題を「設定」すること**であり、このステップに集中することが重要であることを学んだ。
The Problem Construction Process takes as input a business case or concept and outputs a well defined modeling problem (usually a supervised machine learning problem), such that a good solution effectively models the given business case or concept.
問題構築プロセスは、ビジネスケースやコンセプトを入力とし、優れたソリューションが与えられたビジネスケースやコンセプトを効果的にモデル化するような、明確に定義されたモデリング問題(通常は教師あり機械学習問題)を出力する。
The point(s) at which the prediction needs to be made are often given, which fixes the feature space universe, yet the target variable and the observation space are not always given and they need to be carefully constructed.
予測が必要とされるポイントはしばしば与えられ、特徴空間ユニバースが固定されるが、ターゲット変数と観測空間は常に与えられるわけではないので、注意深く構築する必要がある。(??場合によっては最適化したい値が観測できず、代理学習問題を設計する必要がある、みたいな??:thinking:)
As an example, consider the Dates Flexibility model mentioned before, where we want to know the dates flexibility of the users every time a search request is submitted.
例として、前述の「日付の柔軟性」モデルを考えてみましょう。ここでは、検索リクエストが送信されるたびに、ユーザの日付の柔軟性を知りたいのです。
It is not obvious what flexibility means: does it mean that a user is considering more alternative dates than a typical user? or that the dates they will end up booking are different to the ones they are looking at right now?; or maybe it means that a visitor is willing to change dates but only for a much better deal, etc.
柔軟性が何を意味するかは明らかではない: ユーザが一般的なユーザよりも多くの代替日を検討していることを意味するのか、最終的に予約する日程が今見ている日程と異なることを意味するのか、あるいは、訪問者が日程を変更することを望んでいるが、より良い条件のためにのみ変更することを意味するのか、などである。
For each of these definitions of flexibility a different learning setup can be used.
これらの柔軟性の定義それぞれについて、**異なる学習設定を用いることができる**。(あるusecaseに対して)
For example, we could learn to predict how many different dates the user will consider applying regression to a specific dataset composed by users as observations, or to estimate the probability of changing dates by solving a classification problem, where the observations are searches, and so on.
例えば、ユーザをオブザベーションとして構成された特定のデータセットに回帰を適用して、ユーザがいくつの異なる日付を考慮するかを予測する学習や、オブザベーションが検索である分類問題を解くことによって日付を変更する確率を推定する学習などができる。
These are all constructed machine learning problems, that, when solved, output a model of the Dates Flexibility of a user.
これらはすべて機械学習の問題で、それを解くと、ユーザのDates Flexibilityのモデルが出力される。

To compare alternative problems we follow simple heuristics, that consider among others, the following aspects:
alternative problemsを比較する(=複数の機械学習問題の設定の良し悪しを判断する事??)ために、特に以下の点を考慮した単純なヒューリスティックに従う:

- **Learning Difficulty**: when modeling these very subjective concepts, target variables are not given as ground truth, they are constructed. Therefore, some setups are harder than others from a learning perspective. Quantifying learnability is not straightforward. For classification problems the Bayes Error is a good estimate since it only depends on the data set, we apply methods from the work of Tumer & Ghosh [12]. Another popular approach that works well for ranking problems is to compare the performance of simple models against trivial baselines like random and popularity. Setups where simple models can do significantly better than trivial models are preferred. 学習の難しさ: このような**非常に主観的な概念(flexibilityとか? semantic modelの1例)をモデル化する場合、ターゲット変数はground-truthとして与えられるのではなく、構築される**。 そのため、セットアップによっては、学習の観点から他のものより難しいものもある。 学習可能性を定量化するのは簡単ではない。 分類問題では、ベイズ誤差はデータセットに依存するだけなので、良い推定値である。 ランキング問題で有効なもうひとつのよく使われるアプローチは、ランダムや人気のようなtrivialなベースラインとシンプルなモデルの性能を比較することである。 **シンプルなモデルの方がtrivialなモデルよりもはるかに良い結果を出せるようなセットアップ(=代理問題の設定)が好まれる**。

- **Data to Concept Match**: some setups use data that is closer to the concept we want to model. For example, for the Dates Flexibility case we could create a data set asking users themselves if they know the dates they want to travel on, and then build a model to predict the answer. This would give a very straightforward classification problem, that, compared to the other options, sits much closer to the idea of Dates Flexibility. On the other hand, the data would suffer from severe selection Bias since labels are only available for respondents. データとコンセプトの一致：モデル化したい概念に近いデータを使うセットアップ(=代理問題の設定)もある。 例えば、「日程の柔軟性」のケースでは、ユーザ自身に旅行したい日程を知っているかどうかを尋ねるデータセットを作成し、その答えを予測するモデルを構築することができる。 これは、他の選択肢に比べ、デイトスの柔軟性の考えに非常に近い、非常に単純な分類問題を与えるだろう。 一方、ラベルは回答者のみしか入手できないため、データは深刻な選択バイアスに苦しむことになる。

- **Selection Bias**: As just described, constructing label and observation spaces can easily introduce selection bias. An unbiased problem would be based on observations that map 1 to 1 to predictions made when serving, but this is not always possible or optimal. Diagnosing selection bias is straightforward: consider a sample of the natural observation space (users or sessions in the dates flexibility case), we can then construct a classification problem that classifies each observation into the class of the observations for which a target variable can be computed and the class of the observations for which a target variable cannot be computed. If this classification problem is easy (in the sense that a simple algorithm performs significantly better than random) then the bias is severe and must be addressed. Correcting for this type of bias is not obvious. Techniques like Inverse Propensity Weighting [11] and Doubly Robust [4] are helpful in some cases, but they require at least one extra model to build (the propensity model). Other approaches that have been applied successfully but not systematically are methods from the PU-Learning [9] and Semi Supervised Learning fields. 選択バイアス: 先ほど説明したように、ラベル空間と観測空間を構築する(??)と、選択バイアスが発生しやすい。 不偏不党の問題は、サーブ時の予測と1対1に対応するオブザベーションに基づくだろうが、これは常に可能であるわけでも、最適であるわけでもない。 選択バイアスの診断は簡単です: 自然なオブザベーション空間(日付の柔軟性のケースでは、ユーザまたはセッション)のサンプルを考え、そして、**各オブザベーションを、ターゲット変数が計算できるオブザベーションのクラスと、ターゲット変数が計算できないオブザベーションのクラスに分類する分類問題**を構築できます(こうやって学習データとテストデータ間のbiasを評価する方法って名前なんだっけ...??:thinking:)。 もしこの分類問題が簡単であるならば(単純なアルゴリズムがランダムよりも有意に良い結果を出すという意味で)、バイアスは深刻であり、対処しなければならない。 この種のバイアスを補正することは自明ではない。 Inverse Propensity Weighting [11]やDoubly Robust [4]のような技法は、場合によっては有用ですが、少なくとも1つの追加モデル（傾向モデル）を構築する必要があります。 その他のアプローチとして、PU-Learning [9]やSemi Supervised Learning（半教師付き学習）の分野からの手法が、体系的ではないがうまく適用されている。

The Problem Construction process opens an iteration dimension.
問題構築プロセスは、反復の次元を開く。
For a given business case and a chosen problem setup, improving the model is the most obvious way of generating value, but we can also change the setup itself.
与えられたビジネスケースと選択された問題設定の場合、モデルを改善することが価値を生み出す最も明白な方法だが、**設定(=代理問題)そのものを変えることもできる**。
A simple example is a regression predicting the length of a stay, turned in to a multiclass classification problem; and a more involved example is a user preferences model based on click data switched to a Natural Language Processing problem on guest review data.
単純な例としては、滞在時間の長さを予測する回帰が、多クラス分類問題に変化したものであり、より複雑な例としては、クリックデータに基づくユーザ嗜好モデルが、宿泊客のレビューデータに関する自然言語処理問題に変化したものである。(=これってCF -> CBの変化??)
Figure 3 shows a more concrete example.
図3は、より具体的な例を示している。
There are 6 successful algorithm iterations and 4 different setups: Pr(Last Minute) classifies users into Last Minute or not, Pr(Booking) is a conversion model, Pr(Overlap) models the probability of a user making 2 reservations with overlapping stay dates and Unsupervised Similarity models the similarity of destinations.
6つの成功したアルゴリズムiteracionと4つの異なるセットアップ(代理問題)がある:
Pr(Last Minute)はユーザをLast Minuteか否かに分類(=分類問題として解く。last minute="ギリギリ", "土壇場"などの意味)し、Pr(Booking)はコンバージョンモデル(=予約するか否かを予測するタスク)であり、Pr(Overlap)はユーザが宿泊日が重なる2つの予約をする確率をモデル化(=よくわからないが別の代理問題)し、Unsupervised Similarityは目的地の類似性をモデル化(CB filtering的な問題設定)する。(それぞれ代理問題の設定が異なる.)

![fig3]()

In general we found that often the best problem is not the one that comes to mind immediately and that changing the set up is a very effective way to unlock value.
一般的に、**最良の問題はすぐに思い浮かぶものではなく、セットアップを変えることが価値を引き出す非常に効果的な方法であることがわかった**。

# 5. Deployment: Time Is Money 配備: 時は金なり!

![fig6]()

In the context of Information Retrieval and Recommender Systems, it is well known that high latency has a negative impact on user behavior [1].
情報検索やレコメンダーシステムの文脈では、遅延が大きいとユーザの行動に悪影響を与えることがよく知られている[1]。
We quantified the business impact that latency has in our platform by running a multiple-armed RCT where users assigned to each arm were exposed to synthetic latency.
私たちは、各群に割り当てられたユーザがsynthetic latency(=実験用の疑似的な応答時間??)にさらされる多群RCTを実行することによって、**私たちのプラットフォームでレイテンシが持つビジネス上の影響を定量化した**。
Results are depicted in Figure 6 (bottom right quadrant).
結果は図6（右下）に示されている。
Each point is one arm of the experiment, the horizontal coordinate is the relative difference in observed (mean) latency between the arm and the control group, and the vertical coordinate is the relative difference in conversion rate.
各ポイントは実験の1群であり、横座標はその群とcontroll群との間で観察された（平均）latencyの相対差、縦座標はconversion rateの相対差である。
Crosses correspond to arms that did not show statistical significance and circles to arms that did.
十字は統計的有意性を示さなかった群、丸は統計的有意性を示した群に対応する。
This is a single experiment with 4 arms (plus a control group), so we use Šidák correction to account for multiple testing.
これは4群（＋対照群）の単一実験なので、多重検定を考慮するためにŠidák補正を用いている。
Visual inspection shows a clear trend, in which an increase of about 30% in latency costs more than 0.5% in conversion rate (a relevant cost for our business).
目視検査では、**遅延が約30％増加すると、コンバージョン率が0.5％以上低下するという明確な傾向が見られます**。
This finding led us to hypothesize that decreasing latency can produce a gain in conversion.
この発見から、**latencyを短くすることでコンバージョンを向上させることができるという仮説が導かれた**。
On the top left quadrant of Figure 6 we can see the effect of decreasing the latency, in 4 individual experiments in different devices and different pages of the site.
図6の左上の象限では、異なるデバイスとサイトの異なるページにおける4つの個別の実験において、レイテンシを減少させる効果を見ることができる。
All results are statistically significant, supporting the hypothesis.
すべての結果は統計的に有意であり、仮説を裏付けている。

This is particularly relevant for machine learned models since they require significant computational resources when making predictions.
**機械学習モデルは予測を行う際に多大な計算資源を必要とするため、これ(=time is money問題!)は特に機械学習モデルに関連する**。
Even mathematically simple models have the potential of introducing relevant latency.
数学的に単純なモデルでさえ、関連する待ち時間をもたらす可能性がある。
A linear model, for example, might require to compute many (hundreds of thousands), and complicated features, or require to be evaluated on thousands of accommodations.
例えば線形モデルは、多くの(何十万もの)複雑な特徴を計算する必要があったり、何千もの宿泊施設で評価する必要があるかもしれない。
Many pages in our site contain several Machine Learned models, some of them computed at the user level, others at the item level (destination, accommodation, attraction, etc.) or even at UI widget level.
私たちのサイトの多くのページには、ユーザレベルで計算されたもの、アイテムレベル(目的地、宿泊施設、アトラクションなど)で計算されたもの、あるいはUIウィジェットレベルで計算されたものなど、複数の機械学習モデルが含まれています。
Even if each model is fast enough, the overall effect must be considered carefully.
各モデルが十分に速いとしても、全体的な効果は注意深く考慮しなければならない。

To minimize the latency introduced by our models we use several techniques:
**モデルによってもたらされる待ち時間を最小化するために、私たちはいくつかのテクニックを使っている**：

- **Model Redundancy**: Copies of our models are distributed across a cluster to make sure we can respond to as many predictions as requested, scale horizontally and deal with large traffic. モデルの冗長性：私たちのモデルのコピーはクラスタに分散され、要求された多くの予測に対応し、水平方向に拡張し、大規模なトラフィックに対処できるようにしています。(=分散処理)

  - 分散処理(Distributed Processing): 複数のシステム(コンピュータ)によるタスクの同時実行。
  - 並列処理(Parallel Processing): 一つのシステム内でのタスクの同時実行。

- In-house developed Linear Prediction engine: We developed our own implementation of linear predictions, highly tuned to minimize prediction time. It can serve all models reducible to inner products, such as Naive Bayes, Generalized Linear Models, k-NN with cosine or euclidean distance, Matrix Factorization models and more. **自社開発の線形予測エンジン**: 予測時間を最小化するために高度に調整された線形予測の実装を独自に開発しました。 ナイーブ・ベイズ、一般化線形モデル、コサインまたはユークリッド距離によるk-NN、行列因数分解モデルなど、**内積に還元可能なすべてのモデル**に対応できる。(どんな方法なんだろう。気になる...!:thinking:)

- Sparse models: The less parameters a model has, the less computation is needed at prediction time. 疎なモデル: モデルのパラメータが少ないほど、予測時の計算量が少なくて済む。

- Precomputation and caching: When the feature space is small we can simply store all predictions in a distributed key-value store. When the feature space is too big we can still cache frequent requests in memory. **事前計算とキャッシュ**:特徴空間が小さい場合、すべての予測を分散キーバリューストアに格納することができる。 特徴空間が大きすぎる場合でも、頻繁にリクエストされるものをメモリにキャッシュすることができる。

- Bulking: Some products require many requests per prediction. To minimize network load, we bulk them together in one single request. バルク化: 商品によっては、1回の予測に多くのリクエストを必要とするものもある。 ネットワーク負荷を最小限にするため、1つのリクエストにまとめている。

- Minimum Feature Transformations: Sometimes features require transformations that introduce more computation, for example, we might cluster destinations geographically, and then learn parameters of a linear model for each cluster. At prediction time one could compute the cluster given the destination, and then invoke the model. We save one step by just expressing the model in terms of the destination, mapping the weight of a cluster to all the cities in it. 最小限の特徴量変換(=推論時の前処理を減らす工夫??:thinking:): 例えば、目的地を地理的にクラスタリングし、各クラスタに対して線形モデルのパラメータを学習する。 予測時には、目的地からクラスターを計算し、モデルを呼び出すことができる。 クラスターの重みをそのクラスターに含まれるすべての都市にマッピングし、目的地の観点からモデルを表現するだけで、1ステップを節約できる。

Most of these techniques are implemented by our Machine Learning Production service, which provides a simple interface to deploy and consume models in a variety of formats.
これらのテクニックのほとんどは、私たちの機械学習プロダクション・サービスによって実装されており、様々な形式でモデルをデプロイし、利用するためのシンプルなインターフェースを提供しています。
This service abstracts away many challenging aspects of model deployment, including prediction latency, but also high availability, fault tolerance, monitoring, etc.
このサービスは、予測レイテンシーだけでなく、高いavailability(可用性)、フォールトトレランス、モニタリングなど、モデル展開の多くの困難な側面を抽象化する。
Although these techniques are usually very successful at achieving low latency on an individual model level, there could always be the case where adding a fast model is “the last straw” that breaks our system.
これらのテクニックは通常、個々のモデルレベルで低遅延を達成することに非常に成功しているが、高速モデルを追加することが、システムを壊す「最後の藁」(最後のきっかけみたいな??:thinking:)になるケースは常にあり得る。(ex. sparceなモデルに変更して、latencyは下がったけど予測性能も下がって、conversionが下がる、みたいな...?)
To detect this situation we use a method described in detail in section 7.3.The idea is to disentangle the effects of latency and the model itself on the business metric, so that we can decide whether there is a need to improve the latency or the model itself in one single RCT.
この状況を検出するために、7.3節で詳述する方法を用いる(RCTのデザインの工夫)。このアイデアは、ビジネス指標に対するレイテンシーとモデル自体(の予測性能)の影響を切り離すことで、1回のRCTでレイテンシーを改善する必要があるか、モデル自体を改善する必要があるかを判断できるようにすることである。

# 6. Monitoring: Unsupervised Red Flags モニタリング: 監視されないレッドフラッグ

When models are serving requests, it is crucial to monitor the quality of their output but this poses at least two challenges:
モデルがリクエストに応えるとき、**その出力の質をモニターすることは極めて重要**だが、これには少なくとも**2つの課題**がある:

**Incomplete feedback**: In many situations true labels cannot be observed.
不完全なフィードバック: 多くの状況では、真のラベルを観察することはできない。
For example, consider a model that predicts whether a customer will ask for a “special request”.
例えば、顧客が「特別なリクエスト」を求めるかどうかを予測するモデルを考えてみよう。
Its predictions are used while the user shops (search results page and hotel page), but we can only assign a true label to predictions that were made for users that actually booked, since it is at booking time when the special request can be filled in.
その予測は、ユーザが買い物をする間（検索結果ページとホテルページ）使用されるが、特別なリクエストを記入できるのは予約時であるため、実際に予約したユーザに対して行われた予測にのみ真のラベルを割り当てることができる。
Predictions that were made for users that did not book, will not have an associated true label.
予約しなかったユーザに対して行われた予測は、関連する真のラベルを持たない。

**Delayed feedback**: In other cases the true label is only observed many days or even weeks after the prediction is made.
フィードバックの遅れ:**予測が行われてから何日も、あるいは何週間も経ってから、真のラベルが観測される場合もある**。
Consider a model that predicts whether a user will submit a review or not.
ユーザがレビューを投稿するかどうかを予測するモデルを考えてみよう。
We might make use of this model at shopping time, but the true label will be only observed after the guest completes the stay, which can be months later.
買い物時にこのモデルを利用することもあるが、本当のラベルが表示されるのは、ゲストが滞在を終えてからで、数ヶ月後になることもある。

Therefore, in these situations, label-dependent metrics like precision, recall, etc, are inappropriate, which led us to the following question: what can we say about the quality of a model by just looking at the predictions it makes when serving? To answer this question for the case of binary classifiers we apply what we call Response Distribution Analysis, which is a set of heuristics that point to potential pathologies in the model.
したがって、**このような状況(=推論してから真のラベルの観測までに期間があくケース)では、精度やリコールなどのラベルに依存した指標は不適切**である:
このことから、我々は次のような問いを持つことになりました：**モデルの品質について、それがサービスを提供するときに行う予測を見るだけで、何が言えるのだろうか**？バイナリ分類器のケースでこの質問に答えるために、**我々は応答分布分析(=Response Distribution Analysis)**と呼ぶものを適用します。
The method is based on the Response Distribution Chart (RDC), which is simply a histogram of the output of the model.
この方法は、**応答分布図(Response Distribution Chart, RDC)に基づいており、これは単にモデルの出力のヒストグラム**である。
The simple observation that the RDC of an ideal model should have one peak at 0 and one peak at 1 (with heights given by the class proportion) allows us to characterize typical patterns that signal potential issues in the model, a few examples are:
理想的なモデルのRDCは、0に1つのピークがあり、1に1つのピークがあるはずだという単純な観察（高さはクラスの割合で与えられる）により、モデルの潜在的な問題を知らせる典型的なパターンを特徴付けることができる(**RDCはかくあるべき、という仮定を用意しておく必要がある**:thinking:):

- A smooth unimodal distribution with a central mode might indicate high bias in the model or high Bayes error in the data 中央モードがある滑らかな単峰分布は、モデルの偏りが大きいか、データのベイズ誤差が大きいことを示すかもしれない。

- An extreme, high frequency mode might indicate defects in the feature layer like wrong scaling or false outliers in the training data 極端な高頻度モードは、間違ったスケーリングやトレーニングデータの偽の外れ値など、特徴層の欠陥を示すかもしれない。

- Non-smooth, very noisy distributions point to too excessively sparse models 非平滑で非常にノイジーな分布は、モデルが過度にスパースであることを示している。

- Difference in distributions between training and serving data may indicate concept drift, feature drift, bias in the training set, or other forms of training-serving skew. 訓練データと使用データの間の分布の違いは、コンセプトドリフト、特徴ドリフト、訓練セットの偏り、または他の形態の訓練と使用のスキューを示す可能性があります。

- Smooth bimodal distributions with one clear stable point are signs of a model that successfully distinguishes two classes 1つの明確な安定点を持つ滑らかな二峰性分布は、2つのクラスをうまく区別するモデルの兆候である。

![fig7]()

Figure 7: Examples of Response Distribution Charts

Figure 7 illustrate these heuristics.
図7はこれらのヒューリスティック(??)を示している。
The rationale behind these heuristic is that if a model cannot assign different scores to different classes then it is most likely failing at discriminating one from another, small changes in the score should not change the predicted class.
これらのヒューリスティックの根拠は、モデルが異なるクラスに異なるスコアを割り当てることができない場合、そのモデルはクラスと別のクラスの識別に失敗している可能性が高く、スコアのわずかな変化では予測されるクラスは変わらないはずだからである。(ラベル1の確率=45%, ラベル2の確率=55%みたいな感じじゃ自信無さそうだしダメだよね、みたいな仮定:thinking:)
It is not important where the stable point is (which could indicate calibration problems), it only matters that there is one, since the goal is to clearly separate two classes, one that will receive a treatment and one that will not.
安定点がどこにあるかは重要ではなく（キャリブレーションに問題があることを示す可能性がある）、2つのクラス（治療を受けるクラスとそうでないクラス）を明確に分けることが目的なのだから、安定点があることだけが重要なのだ。
These are the advantages this method offers:
これがこの方法がもたらす利点である：

- It can be applied to any scoring classifier どのような得点分類器にも適用できる

- It is robust to class distribution. In extreme cases, the logarithm of the frequency in the RDC is used to make the cues more obvious. クラス分布にロバストである。 極端な場合は、RDCの周波数の対数を使用して、キューをより明確にする。

- It addresses the Incomplete Feedback issue providing Global Feedback since the RDC is computed considering all predictions RDCはすべての予測を考慮して計算されるため、grobal feedbackを提供し、incompete feedback の問題に対処する。

- It addresses the Delayed Feedback issue providing Immediate Feedback, since the RDC can be constructed as soon as a few predictions are made RDCは、いくつかの推論がなされるとすぐに構築することができるため、即時フィードバックを提供し、 delayed feedback の問題に対処する。

- It is sensitive to both class distribution and feature space changes, since it requires very few data points to be constructed 構築するデータポイントが非常に少ないので、クラス分布と特徴空間の変化の両方に敏感です。

- It can be used for multi-class classification when the number of classes is small by just constructing one binary classifier per class that discriminates between one class and the others (one vs all or one vs rest) クラス数が少ない場合、クラスごとに1つの2値分類器を構成し、1つのクラスと他のクラス(1対すべて、または1対その他)を識別するだけで、多クラス分類に使用できます。

- It offers a label-free criterion to choose a threshold for turning a score into a binary output. The criterion is to simply use a minimum of the RDC in between the 2 class-representative modes. If the region is large, then one can choose to maximize recall or precision using the lower and upper bound of that region respectively. This is very useful when the same model is used in various points of the system like hotel page or search results page, since they have different populations with different class distributions. **スコアを2値出力に変換するための閾値を選択するラベルフリーの基準を提供する**(最適な閾値を探せる??:thinking:)。 その基準は、2つのクラスを代表するモードの中間のRDCの最小値を単純に使用することである。 もしその領域が大きければ、その領域の下限と上限を使って、それぞれ再現率(recall)か精度(precision)を最大化することを選択できる。 これは、ホテルのページや検索結果のページなど、システムのさまざまな場所で同じモデルが使用される場合に非常に便利です。

The main drawbacks are:
主な欠点は以下の通りだ：

- It is a heuristic method, it cannot prove or disprove a model has high quality これは**発見的な(=heuristic)方法**であり、モデルが高品質であることを証明することも反証することもできない。

- It does not work for estimators or rankers 推定モデルやrankingモデルには使えない

In practice, Response Distribution Analysis has proven to be a very useful tool that allows us to detect defects in the models very early.
実際、**応答分布分析は、モデルの欠陥を早期に発見できる非常に有用なツールである**ことが証明されている。

# 7. Evaluation: Experiment Design Sophistication Pays Off 評価:洗練された実験計画が功を奏す

Experimentation through Randomized Controlled Trials is ingrained into Booking.com culture.
**無作為化比較試験(RCT)による実験は、Booking.comの文化に根付いている**。
We have built our own experimentation platform which democratizes experimentation, enabling everybody to run experiments to test hypotheses and assess the impact of our ideas [6].
**私たちは、実験を民主化する独自の実験プラットフォームを構築し、誰もが実験を実行して仮説を検証し、私たちのアイデアの影響を評価できるようにした**[6]。(ABテストの話だよね。これのオフライン実験ver.を作りたい。2実験を民主化する"って表現いいなぁ...:thinking:)
Machine Learning products are also tested through experiments.
機械学習製品も実験を通じてテストされる。
The large majority of the successful use cases of machine learning studied in this work have been enabled by sophisticated experiment designs, either to guide the development process or in order to detect their impact.
この研究で研究された機械学習の成功したユースケースの大部分は、開発プロセスを導くため、あるいはその影響を検出するために、洗練された実験デザインによって実現されている。
In this section we show examples of how we use a combination of triggered analysis with treatments design to isolate the causal effect of specific modeling and implementation choices on business metrics.
このセクションでは、特定のモデル(ex. 推論結果の違い)と実装の選択(ex. レイテンシーの違い)がビジネス指標に及ぼす因果効果を分離するために、trigger分析(triggered analysis)とtreatments designの組み合わせを使用する方法の例を示します。

## 7.1. Selective triggering 選択的トリガー

In a standard RCT, the population is divided into control and treatment groups, all subjects in the treatment group are exposed to the change, and all subjects in the control group are exposed to no change.
標準的なRCTでは、集団をcotrol群とtreatment群に分け、treatment群の被験者全員が変化(ex. 新モデル)にさらされ、controll群の被験者全員が変化なし(ex. 旧モデル)にさらされる。(うんうん...!)
However, in many cases, not all subjects are eligible to be treated, and the eligibility criteria are unknown at assignment time.
しかし、多くの場合、すべての被験者がtreatmentを受けられるわけではなく、割り付け時点では適格基準は不明である。
In the case of machine learning models, this is often the case since models may require specific features to be available.
機械学習モデルの場合、モデルが特定の特徴量を必要とすることがあるため、このようなケースはよくある。
The subjects assigned to a group but not treated add noise to the sample, diluting the observed effect, reducing statistical power and inflating the False Discovery Rate.
あるグループに割り付けられたがtreatmentを受けなかった被験者は、サンプルにノイズを加え、観察された効果を希釈し、統計的検出力を低下させ、偽発見率を上昇させる。
To deal with this situation, we apply Triggered Analysis [3], where only the treatable (or triggered) subjects in both groups are analyzed.
この状況に対処するため、**トリガー分析[3]**を適用し、**両グループのtreatment可能な(またはtriggerされた)被験者だけを分析**する。(triggered = model availableって事っぽい! 要はtreatment群のうち、実際にtreatmentを受けたユーザのみをちゃんと分析するってことかな:thinking:)
(参考文献: https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf)
Figure 8 illustrates this setup.
図8はこの設定を示している。(ex. 推薦機能の新旧モデルを比較するRCTの場合、treatment群/controll群にユーザを分けるが、実際に推薦機能を利用した=triggerされたユーザのビジネス指標を使って評価しようってことかな。)

![fig8]()

## 7.2. Model-output dependent triggering モデル出力に依存するトリガー

![fig9]()

Even when all the model requirements are met, the treatment criteria might depend on the model output.
モデル要件がすべて満たされている場合でも、treatment基準はモデル出力に依存する可能性がある。
This happens for instance when we show a block with alternative destinations only to users identified as destination-flexible by the model.
これは例えば、モデルによって「目的地の柔軟性がある」と識別されたユーザにのみ、代替の目的地があるブロックを表示する場合に起こる。(=要するに、特定の推論結果の場合にのみ、ユーザにtreatmentイベントが発生して、正解ラベルが得られる、みたいなケース??)
(ex. 「ユーザの目的地の柔軟性を定量化するMLモデル」の改善のRCT。MLモデルが「柔軟性がある」と判定したユーザにのみ、代替の目的地が推薦される。)
It may also be the case that subsequent steps fail or succeed depending on the model output, like fetching relevant items which may not be available.
また、利用できないかもしれない関連アイテムをフェッチするなど、モデル出力によって後続ステップが失敗したり成功したりする場合もある。
In such cases, some users are not exposed to any treatment, once more diluting the observed effect.
このような場合、何人かのユーザはtreatmentを受けず、観察された効果がさらに薄れてしまう。
Nevertheless, the setup of Figure 8 cannot be used since in the control group the output of the model is not known and therefore cannot condition the triggering.
とはいえ、controllグループでは、モデルの出力が不明(=新モデルの出力が不明)であるため、Triggerを条件付けることができないため、図8の設定は使用できない。(図8は、新旧モデルが推論する前の情報を元にTriggerを条件づけていたのでOKだった。)
Modifying the control group to call the model is not advised, since we also use this group as a safety net to detect problems with the experiment setup, and in such cases all the traffic can be directed to the control group while studying the issue.
モデルを呼び出すためにコントロール・グループを変更することは推奨されない。なぜなら、実験セットアップの問題を検出するためのセーフティネットとしてこのグループも使用しており、そのような場合、問題を研究している間、すべてのトラフィックをコントロール・グループに向けることができるからである。
The setup for model output dependent triggering requires an experiment with 3 groups as shown on Figure 9.
**モデル出力に依存するtriggerのセットアップ(=treatmentされるかがモデル出力値に依存するケース)には、図9に示すような3つのグループによる実験が必要である**。
The control group C is exposed to no change at all, the two treatment groups T 1 and T 2 invoke the model and check the triggering criteria (e.g.output > 0) but only in T 1 triggered users are exposed to a change.
controll群Cは全く変化にさらされず、2つのtreatment群 $T_1$ と $T_2$ はモデル(=新モデル)を起動し、トリガー基準 (例えば出力 >0 )をチェックするが、トリガーされた $T_1$ のユーザだけが変化にさらされる。
In T 2 users are not exposed to any change regardless of the model output.
$T_2$ では、モデルの出力に関係なく、ユーザはいかなる変化にもさらされない。(=新モデルでtrigger基準を満たしているか否かは判定されるが、旧モデルが適用される。)
The statistical analysis is conducted using only triggered subjects from both T 1 and T 2.
統計分析は、$T_1$ と $T_2$ の両方からtriggerされた(=新モデルのtrigger基準を満たした) 被験者だけを用いて行われた。

## 7.3. Controlling performance impact パフォーマンスへの影響をコントロールする

The setup described in the previous section serves also as a way to disentangle the causal effect of the functionality on the user experience - for instance, new recommendations - from that of any slow down due to model computation.
前節で説明したセットアップは、**ユーザエクスペリエンスに対する機能の因果関係(例えば、新しいレコメンデーション)を、モデル計算による速度低下から切り離す**方法としても役立つ。(ex. UX悪化が、推論結果によるものか、推論速度低下によるものか、を切り離せる??)
A comparison of metrics betweenC andT 1 measures the overall effect of the new functionality, including any performance degradation.
Cと $T_1$ のメトリクスの比較は、パフォーマンス低下を含む**新機能の全体的な効果**(ex. 推論結果 & 推論速度を含めて総合的なUX!)を測定する。
A positive result endorses the current implementation.
肯定的な結果は、現在の実施を支持するものである。(positiveな結果だったらこれだけでGOサインを出せる。)
Otherwise, we can still learn from two more comparisons.
そうでなければ、あと2つの比較から学ぶことができる。
With C and T 2 we can isolate and measure both the slowdown and its impact on the metrics of interest, since there is no change on the functionality between these variants.
Cと $T_2$ では、これらのvariant間で機能に変化がないため、**速度低下と、関心のある測定基準への影響の両方を分離して測定することができる**。
Conversely, T 1 and T 2 share the same computational load due to model invocation and are only different on the exposure to the new functionality, allowing to measure its effect regardless of the computational cost associated to the model.
逆に、$T_1$ と $T_2$ は、**モデル呼び出しによる計算負荷を共有**(=推論時間の条件は同じはず)し、新機能への露出度だけが異なるため、モデルに関連する計算コストに関係なく、その効果を測定することができる。
A positive result in this last comparison supports the new functionality, independently of the effect of the model on latency.
この最後の比較で肯定的な結果が出たことは、遅延に対するモデルの効果とは無関係に、新機能を裏付けている。
More details on this topic can be found in [7].
このトピックの詳細は[7]にある。

## 7.4. Comparing Models モデルの比較

![fig10]()

Figure 10: Experiment design for comparing models.

When comparing treatments based on models which improve on one another, there are often high correlations.
互いに改善し合うモデルに基づいてtreatmentを比較すると、高い相関が見られることが多い。
As a toy example, consider a binary classification problem and consider model x, a successful solution with 80% accuracy.
おもちゃの例として、2値分類問題を考え、80％の精度で成功した解であるモデルxを考える。
Model y improves on this result by correcting half of the mistakes of model x, while introducing only 5% new mistakes.
モデルyは、モデルxのミスの半分を修正し、新しいミスを5％だけ導入することで、この結果を改善した。
These two models disagree only on at most 15% of the cases.
この2つのモデルが一致しないのは、せいぜい15％程度である。
For the other (at least) 85% of the cases, being on control or treatment does not result on a different experience, differences in metrics cannot be caused by difference in the model outputs, and therefore this traffic only adds noise.
残りの（少なくとも）85％のケースについては、controll群とtreatment群のどちらを選んでも、異なる経験は得られず、測定基準の違いはモデル出力の違いによって引き起こされることはない。
Figure 10 shows the setup for this situation, which is very similar to the previous one.
図10は、この状況でのセットアップを示しており、前回と非常によく似ている。
In this case the triggering condition is models disagree, which means that the outputs from both models are required in T 1 and T 2.
この場合、トリガー条件はモデルの不一致であり、T1とT2で両方のモデルからの出力が必要となる。
The control group invokes and uses the output from model 1, the current baseline, and also works as a safety net.
コントロール・グループは、現在のベースラインであるモデル1のアウトプットを呼び出して使用し、セーフティネットとしても機能する。
As an additional gain, both T 1 and T 2 perform the same model associated computations, removing any difference due to performance between the models, isolating the causal effect of the difference between the model outputs on the target metric.
追加的な利益として、T1とT2の両方が同じモデルに関連する計算を実行し、モデル間の性能による差を取り除き、ターゲットメトリックに対するモデル出力の差の因果効果を分離する。

# 8. Conclusion 結論

In this work we shared 6 lessons we have learned while developing 150 successful applications of Machine Learning in a large scale ecommerce.
この仕事では、大規模なeコマースで機械学習の150の成功したアプリケーションを開発する間に学んだ6つの教訓を共有した。
We covered all the phases of a Machine Learning project from the perspective of commercial impact delivery.
商業的インパクトの提供という観点から、機械学習プロジェクトの全フェーズをカバーした。
All our lessons are about improving the hypothesis-model-experiment cycle:
すべての教訓は、**仮説-モデル-実験のサイクルを改善すること**です：
the semantic layer and model families help us to initiate as many cycles as possible;
セマンティックレイヤーとモデルファミリーは、可能な限り多くのサイクルを開始するのに役立ちます。
the finding that offline metrics are poorly correlated to business gains led us to focus on other aspects, like for example, Problem Construction, which adds a very rich iteration dimension;
オフラインのメトリクスはビジネス上の利益との相関性が低いという発見により、例えば、非常に豊かな反復の次元を追加する問題構築(??)のような、他の側面に焦点を当てるようになりました；
the finding that latency has commercial value led us to implement methods to keep it low giving each model the best chance to be impactful, and led to experiment design techniques to isolate its effects on business metrics;
レイテンシーに商業的価値があることを発見したことで、各モデルにインパクトを与える最高のチャンスを与えるために、レイテンシーを低く抑える方法を導入することになり、また、ビジネス・メトリクスへの影響を切り分けるための実験デザイン手法につながった(section7のやつ!)；
Response Distribution Analysis improved our ability to detect model issues right after deployed;
レスポンス分布分析により、導入直後のモデルの問題を検出する能力が向上しました。
and finally, experiment sophistication improved the iteration cycle by giving fast, reliable and fine-grained estimations of the effect of our choices and the validity of our hypotheses.
そして最後に、実験の高度化により、我々の選択の効果や仮説の妥当性を、迅速かつ信頼性の高い、きめ細かな推定を行うことで、反復サイクルが改善されました。
In order to turn these lessons into actions we integrated ideas from various disciplines like Product Development, User Experience, Computer Science, Software Engineering, Causal Inference among others.
これらの教訓を行動に移すために、私たちは製品開発、ユーザ・エクスペリエンス、コンピューター・サイエンス、ソフトウェア工学、因果推論など、さまざまな分野のアイデアを統合した。
Hypothesis driven iteration and interdisciplinary integration are the core of our approach to deliver value with Machine Learning, and we wish this work can serve as a guidance to other Machine Learning practitioners and sparkle further investigations on the topic.
**仮説に基づいた反復と学際的な統合は、機械学習で価値を提供するための私たちのアプローチの中核**であり、この研究が他の機械学習実践者のガイダンスとなり、このトピックに関するさらなる調査に火をつけることができればと願っている。
