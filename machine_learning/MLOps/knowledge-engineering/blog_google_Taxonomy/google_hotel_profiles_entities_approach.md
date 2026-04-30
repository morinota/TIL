refs: https://streetfightmag.com/2019/04/12/things-not-strings-googles-new-hotel-profiles-exemplify-its-approach-to-entities/?utm_source=chatgpt.com

Back in 2012, Google’s Amit Singhal published a now-famous blog post announcing the Knowledge Graph. 
**2012年に、Googleのアミット・シンガルは、Knowledge Graphを発表する今や有名なブログ投稿を公開**しました。（あれ、有名なんだ...!!:thinking:）
The post, titled “Inside the Knowledge Graph: Things, Not Strings,” introduced a fundamental change in the methodology behind Google’s long-standing mission “to organize the world’s information and make it universally accessible and useful.”
その投稿は「Inside the Knowledge Graph: Things, Not Strings」というタイトルで、**Googleの長年の使命「世界の情報を整理し、普遍的にアクセス可能で有用にする」という方法論に根本的な変化**をもたらしました。

Whereas Google’s original PageRank algorithm, the basis for populating SERPs to this day, makes use of links and other contextual signals to determine the relevancy of a webpage, the Knowledge Graph represents a totally different approach, one that potentially realizes Tim Berners-Lee’s early notion of a semantic web where all content is linked according to its meaning.
Googleの元々のPageRankアルゴリズムは、今日のSERPを構成する基盤であり、リンクやその他の文脈的信号を利用してウェブページの関連性を判断しますが、Knowledge Graphは全く異なるアプローチを示しており、すべてのコンテンツがその意味に従ってリンクされるセマンティックウェブのティム・バーナーズ＝リーの初期の概念を実現する可能性があります。

The Knowledge Graph, as Singhal describes it, shifts Google’s attention from “strings” to “things,” meaning that search is no longer a matter of finding text that matches the text in your query (string matching), but rather a matter of understanding the concepts in a query as well as its probable intent and mining the Google datastore for a response that represents what Google knows about that concept.
シンガルが説明するように、**Knowledge GraphはGoogleの注意を「文字列」から「物事」へと移し**、検索はもはやクエリ内のテキストと一致するテキストを見つけること（文字列マッチング）ではなく、クエリ内の概念とその可能性のある意図を理解し、Googleのデータストアからその概念に関するGoogleの知識を表す応答を探し出すことに関するものです。

<!-- ここまで読んだ! -->

## The Knowledge Graph’s early incarnation 知識グラフの初期の形態

Ask “Who is Charles Dickens?” for example, and the Knowledge Graph “knows” that you are asking about an author from a certain historical period and country of origin who is celebrated for having written certain books. 
例えば「チャールズ・ディケンズとは誰ですか？」と尋ねると、**知識グラフは、あなたが特定の歴史的時代と出身国の著者について尋ねていることを「知っている」**のです。その著者は特定の本を著したことで称賛されています。
The search results Google displays for such a query, with components we’ve come to recognize such as Rich Snippets, Related Questions, and the Knowledge Panel, represent a semantically structured body of knowledge about the entity Charles Dickens. 
そのようなクエリに対してGoogleが表示する検索結果は、リッチスニペット、関連質問、知識パネルなど、私たちが認識するようになった要素を含み、チャールズ・ディケンズというエンティティに関する意味的に構造化された知識の体を表しています。

![]()

We’ve all seen evidence of the Knowledge Graph at work in examples like this one, though for the most part the evidence has pointed out not so much Google’s ability to mine the web for meaning, but rather its ability to regurgitate Wikipedia entries. 
私たちは皆、このような例で知識グラフが機能している証拠を見たことがありますが、ほとんどの場合、その証拠はGoogleが意味をウェブから掘り出す能力ではなく、むしろWikipediaのエントリを反復する能力を指摘しています。
In a Washington Post article in 2016, for example, Caitlin Dewey referred skeptically to Google’s “sketchy quest to control the world’s knowledge,” pointing out that when it came to sensitive topics like the status of Taiwan or Jerusalem, or even the mysteriously contested height of Hillary Clinton, Google relied too heavily on a mechanically redacted version of the facts that tended to flatten crucial nuances and even distort the truth. 
例えば、2016年のワシントンポストの記事で、ケイトリン・デューイはGoogleの「世界の知識を制御しようとする怪しい試み」に懐疑的に言及し、台湾やエルサレムの地位、さらにはヒラリー・クリントンの高さのような敏感なトピックに関して、Googleが重要なニュアンスを平坦化し、真実を歪める傾向のある機械的に修正された事実のバージョンに過度に依存していることを指摘しました。

<!-- ここまで読んだ! -->

## A patent for graphing the world 世界をグラフ化する特許

In the time since, Google has worked to improve its handling of such sensitive information, but it has also been quietly expanding its ambitions.  
その後、Googleはそのような敏感な情報の取り扱いを改善するために取り組んできましたが、同時に静かに野心を広げています。  
That fact is nowhere clearer than in Bill Slawski’s recent analysis of a patent issued to Google in February of this year that explains its methodology behind extracting and classifying information about entities.  
その事実は、今年の2月にGoogleに発行された特許の分析において、Bill Slawskiによって明確に示されています。この特許は、エンティティに関する情報を抽出し分類する方法論を説明しています。

An entity, in Google’s terms, is any place, idea, thing, object, or otherwise classifiable node in a stream of data.  
Googleの用語では、**エンティティとは、データのストリーム内で分類可能なノードである場所、アイデア、物、オブジェクトなど**を指します。 
The patent describes Google’s attempt to record in a massive database not only the more obvious types of entity classifications—famous authors like Charles Dickens, celebrities, historical events, nations, and so on—but also the superclasses to which those classes belong, such as humans, men, women, citizens of certain nations, and so on, and the subclasses they contain, such as lifespan, marital status, or important works.
この特許は、Googleが有名な著者（チャールズ・ディケンズなど）、セレブリティ、歴史的事件、国々などの明らかなエンティティ分類だけでなく、それらのクラスが属するスーパークラス（人間、男性、女性、特定の国の市民など）や、それらが含むサブクラス（寿命、婚姻状況、重要な作品など）を記録しようとする試みを説明しています。
The ambitious aim outlined in the patent would also be able to provide information about the relationships between each node of meaning.
特許に示された野心的な目標は、意味の各ノード間の関係に関する情報を提供できることです。  
To expand on the example we started with, Charles Dickens can be described as an entity belonging to the class “famous authors,” which is part of the class “humans.”  
私たちが最初に始めた例を拡張すると、チャールズ・ディケンズは「有名な著者」というクラスに属するエンティティとして説明できます。これは「人間」というクラスの一部です。  
Dickens, the entity, contains subclasses such as “important works,” which include entities like Great Expectations.  
エンティティであるディケンズは、「重要な作品」などのサブクラスを含み、そこには『大いなる遺産』のようなエンティティが含まれます。  
Relationships between entities may be expressed in forms like, “Dickens was the author of a novel called Great Expectations.”  
エンティティ間の関係は、「ディケンズは『大いなる遺産』という小説の著者であった」という形で表現されることがあります。

The patent doesn’t say, of course, that Google merely intends to map the universe of famous authors.  
もちろん、この特許はGoogleが単に有名な著者の宇宙をマッピングすることを意図しているとは言っていません。  
It implies that Google intends to map—well, everything.  
それは、Googleがすべてをマッピングしようとしていることを示唆しています。  
In Slawski’s analysis, the true scope of the Knowledge Graph comes into view, and that scope is massive.  
Slawskiの分析では、ナレッジグラフの真の範囲が明らかになり、その範囲は非常に広大です。

The trick is for Google to divorce itself from heavy reliance on secondary sources like Wikipedia and to be able instead to classify and cross-reference information as a native, self-sustaining activity on web pages themselves.  
**GoogleがWikipediaのような二次情報源への依存を断ち切り、代わりに情報をウェブページ自体でネイティブで自己持続的な活動として分類し、相互参照できるようにすることが重要**です。  
That’s what makes the patent filing a little different from the evidence of the Knowledge Graph we’ve already seen in the wild.
これが、この特許出願が私たちがすでに目にしたナレッジグラフの証拠とは少し異なる理由です。

One might think we’ve seen this before with Schema markup.  
Schemaマークアップでこれを以前に見たと思うかもしれません。  
After all, the Schema.org standard, created by Google in collaboration with other search engines, provides a standard tagging language that helps to reveal the content of text, at least as it applies to certain classes of information, such as local businesses or consumer reviews.  
結局のところ、Googleが他の検索エンジンと協力して作成したSchema.org標準は、少なくとも地元のビジネスや消費者レビューなどの特定の情報クラスに適用されるテキストの内容を明らかにするのに役立つ標準的なタグ付け言語を提供します。  
The entities Schema markup is designed to identify, and the relationships between those entities which the standard helps to describe, are structurally very similar to the entities described in the new patent.  
Schemaマークアップが識別するように設計されたエンティティと、そのエンティティ間の関係は、新しい特許で説明されているエンティティと構造的に非常に似ています。

But Schema markup is more like a crutch than a comprehensive solution.  
しかし、Schemaマークアップは包括的な解決策というよりも、むしろ杖のようなものです。  
The requirement it imposes—that human beings apply semantic tags to text on web pages—will never scale.  
それが課す要件（人間がウェブページのテキストにセマンティックタグを適用すること）は、決してスケールしません。  
That’s essentially why Tim Berners-Lee gave up on the semantic web in the first place and defaulted to the simple display language of HTML.  
これが、ティム・バーナーズ＝リーが最初にセマンティックウェブを諦め、HTMLのシンプルな表示言語に戻った理由です。  
Schema will never serve the ultimate purpose the Knowledge Graph takes as its aim because the vast majority of content classifications cannot be captured with prescriptive markup.  
**Schemaは、ナレッジグラフが目指す最終目的を決して果たすことはありません。なぜなら、ほとんどのコンテンツ分類は、規定されたマークアップで捉えることができないから**です。  
Google needs to train its technology to impose semantic structure on raw unstructured text, just as our brains do.  
Googleは、私たちの脳が行うように、生の非構造化テキストにセマンティック構造を適用するために技術を訓練する必要があります。

It’s only when the Knowledge Graph is able to apply what it knows to any new content it encounters, learning as it goes about entities it hasn’t seen before, that its larger intent will be realized.  
**ナレッジグラフが新しいコンテンツに出会ったときに、自分が知っていることを適用し、見たことのないエンティティについて学ぶことができるときに、その大きな意図が実現されます。**

<!-- ここまで読んだ! -->

In the patent, there’s a lot of language about this learning process.  
特許には、この学習プロセスに関する多くの言葉があります。  
From the abstract:  
要約から：

“Computer-implemented systems and methods are provided for extracting and storing information regarding entities from documents, such as webpages.  
「コンピュータ実装されたシステムと方法は、ウェブページなどの文書からエンティティに関する情報を抽出し、保存するために提供されます。  
In one implementation, a system is provided that detects an entity candidate in a document and determines that the detected candidate is a new entity.  
1つの実装では、文書内のエンティティ候補を検出し、検出された候補が新しいエンティティであると判断するシステムが提供されます。  
The system also detects a known entity proximate to the known entity based on the one or more entity models.  
システムは、1つ以上のエンティティモデルに基づいて、既知のエンティティに近接する既知のエンティティを検出します。  
The system also detects a context proximate to the new and known entities having a lexical relationship to the known entity.  
システムは、既知のエンティティに対して語彙的関係を持つ新しいエンティティと既知のエンティティに近接するコンテキストも検出します。  
The system also determines a second entity class associated with the known entity and a context class associated with the context.  
システムは、既知のエンティティに関連する第2のエンティティクラスと、コンテキストに関連するコンテキストクラスを決定します。  
The system also generates a first entity class based on the second entity class and the context class.  
システムは、第2のエンティティクラスとコンテキストクラスに基づいて第1のエンティティクラスを生成します。  
The system also generates an entry in the one or more entity models reflecting an association between the new entity and the first entity class.”  
システムは、新しいエンティティと第1のエンティティクラスとの関連を反映する1つ以上のエンティティモデルにエントリを生成します。」

In other words, the Knowledge Graph learns about new entities by inference, setting aside what it already knows in order to isolate what it doesn’t.  
言い換えれば、**ナレッジグラフは推論によって新しいエンティティについて学び、既に知っていることを脇に置いて、知らないことを特定**します。  
If successful, this process could eventually run itself, becoming ever more effective at learning new things the more new things it learns.  
成功すれば、このプロセスは最終的に自動的に実行されるようになり、新しいことを学べば学ぶほど、ますます新しいことを学ぶのに効果的になります。

<!-- ここまで読んだ! -->

Take for example a web page that discusses Bill and Hillary Clinton.  
例えば、ビルとヒラリー・クリントンについて議論するウェブページを考えてみましょう。  
Imagine that the Knowledge Graph has already collected and organized a significant amount of information about Bill but has never heard of Hillary.  
**ナレッジグラフがビルに関するかなりの量の情報をすでに収集し整理しているが、ヒラリーについては聞いたことがない状況**を想像してみてください。  
The patent describes an entity extraction process whereby Google draws a circle around what it already knows, leaving the rest as new information to be associated with a new entity called Hillary Clinton.  
この特許は、Googleが既に知っていることの周りに円を描き、残りをヒラリー・クリントンという新しいエンティティに関連付ける新しい情報として残すエンティティ抽出プロセスを説明しています。

Of course, no document contains only two entities. 
もちろん、どの文書にも2つのエンティティだけが含まれているわけではありません。
Indeed, an entity like “Bill Clinton” is a member of a superclass called “humans” and another called “politicians” and another called “Caucasian men,” each superclass containing subclasses like age, height, time in office, ancestry, and so on. 
実際、「ビル・クリントン」のようなエンティティは、「人間」と呼ばれるスーパークラスや「政治家」と呼ばれるスーパークラス、さらには「白人男性」と呼ばれるスーパークラスのメンバーであり、各スーパークラスには年齢、身長、在職期間、祖先などのサブクラスが含まれています。
In short, this type of analysis is incredibly complex, but its issued patent suggests Google is probably attempting it. 
要するに、この種の分析は非常に複雑ですが、発行された特許はGoogleがそれを試みている可能性があることを示唆しています。

So far, one doesn’t see this more fully realized version of the Knowledge Graph much in actual search results—though this may partly be due to the fact that, when successful, the results could be hard to distinguish from data mined in a cruder fashion. 
これまでのところ、実際の検索結果ではこのより完全に実現された知識グラフのバージョンはあまり見られません—これは、成功した場合、結果が粗い方法でデータをマイニングしたものと区別がつきにくい可能性があるためです。

<!-- ここまで読んだ! -->

## Google now treats hotels as entities Googleは今やホテルをエンティティとして扱う

- 個人メモ:
  - このセクションでは、Googleが特許として構想してた「生のテキストからentitiesを抽出し結びつける」という野心的なアプローチが、「Google Hotels」というじつサービスでどのように体現されてるかを解説してる。
  - 重要なポイントは以下の3点:
    - 1. 機械学習の2つの異なる使われ方:
      - 価格やトレンドの分析(従来型のML):
        - 「Deals(お得な情報)フィルター」機能は、過去の価格トレンドを分析し、通常より安い料金を提供するホテルを強調するために使われる。これは広告配信やRecSysで見られる、典型的なパターン学習の例。
      - entityへのデータ紐付け(次世代のML):
        - 一方で、写真やレビューを動的にキュレーションして提示する機能は、無数の情報源からもっとも有用な情報を抽出し、それを特定のホテルというentityに紐づけるためのML。これが知識グラフ関連。
    - 2. 「ホテル」というentityに紐づけられる膨大なデータ:
      - Googleでは特定のホテル施設を独立したentityとして扱い、そこに自社データやサードパーティデータからの情報を構造化して紐づけている。具体的には以下: (attributeって感じ??:thinking:)
        - ホテルクラスの評価
        - レビューと要約。
        - 写真や動画
        - 周辺の地理情報
    - 3. Wikipedia依存からの脱却と「自給自足のナレッジグラフ」へ:
      - これまでの一般的な検索で見られる「ナレッジパネル(検索結果の右側に出る情報ボックス)」機能は、Wikipediaなどの二次情報源に大きく依存していた。
      - しかし、Google Hotelsにおける膨大なデータ群は、より複雑で多様な情報源がミックスされたもの。
        - 著者はこれを、Googleが外部の辞書的ソースに頼る段階から一歩踏み出し、ナレッジグラフ自体が自律的に様々なウェブ上の情報を収集し、関係性を構築していく「自給自足」の段階に到達した証拠であると高く評価してる。

While this more ambitious way of surfacing information about entities is not yet standard, in researching Google’s new interface for hotels, I think I’m seeing evidence of a real-world example. 
このようなエンティティに関する情報を表示するより野心的な方法はまだ標準ではありませんが、Googleのホテルの新しいインターフェースを調査する中で、私は現実世界の例の証拠を見ていると思います。
The Google Hotels interface contains structured information about each listed hotel culled from a variety of internal and third-party sources. 
Google Hotelsインターフェースには、さまざまな内部および第三者のソースから収集された、各リストされたホテルに関する構造化情報が含まれています。

You can visit the new interface, which Google quietly announced in March, at google.com/hotels. 
Googleが3月に静かに発表した新しいインターフェースには、google.com/hotelsでアクセスできます。

In the blog post announcing the new interface, Google’s Richard Holden mentions machine learning in a couple of key sentences. 
新しいインターフェースを発表するブログ記事の中で、Googleのリチャード・ホールデンは、いくつかの重要な文で機械学習に言及しています。

The first relates to the search experience, with Holden introducing Google’s new Deals filter by explaining, “This filter uses machine learning to highlight hotels where one or more of our partners offer rates that are significantly lower than the usual price for that hotel or similar hotels nearby.” 
最初の文は検索体験に関連しており、ホールデンはGoogleの新しいDealsフィルターを紹介し、「このフィルターは、私たちのパートナーの1つ以上がそのホテルや近くの類似ホテルの通常価格よりも大幅に低い料金を提供しているホテルを強調するために機械学習を使用します」と説明しています。

The second mention of machine learning hints that Holden is talking about the Knowledge Graph: “You can also view a hotel’s highlights—like a fancy pool, if it’s a luxury hotel, or if it’s popular with families—with expanded pages for photos and reviews curated with machine learning.” 
機械学習の2回目の言及は、ホールデンがKnowledge Graphについて話していることを示唆しています。「また、豪華なホテルであれば素敵なプールのようなホテルのハイライトや、家族に人気があるかどうかを、機械学習でキュレーションされた写真やレビューの拡張ページで見ることができます。」

It would be easy to elide these two references to machine learning and make the false assumption that Holden is talking about the same thing in both cases, but he’s not. 
これら2つの機械学習への言及を省略し、ホールデンが両方のケースで同じことを話しているという誤った仮定をするのは簡単ですが、彼はそうではありません。

In the first case, historical trend analysis of hotel prices helps Google highlight deals that are lower than the usual price. 
最初のケースでは、ホテル価格の歴史的トレンド分析がGoogleに通常の価格よりも低い取引を強調するのを助けます。

The Deals filter incorporates machine learning, we can assume, in the sense that it continually takes in new information about hotel prices and adjusts its recommendations accordingly. 
Dealsフィルターは、ホテル価格に関する新しい情報を継続的に取り入れ、それに応じて推奨を調整するという意味で、機械学習を取り入れていると考えられます。

As such, this is a classic example, not unlike the type of machine learning one sees in programmatic advertising or Netflix movie recommendations. 
したがって、これはプログラマティック広告やNetflixの映画推薦で見られるタイプの機械学習とあまり変わらない古典的な例です。

On the other hand, curation of content like photos and reviews sounds a lot more like the process of linking data to entities. 
一方で、写真やレビューのようなコンテンツのキュレーションは、データをエンティティにリンクするプロセスにもっと似ているように聞こえます。

In this case, machine learning likely comes into play from the point of view of constructing a dynamic user interface that presents the most engaging, useful, or popular reviews and photos from various sources. 
この場合、機械学習は、さまざまなソースから最も魅力的で有用、または人気のあるレビューや写真を表示する動的ユーザーインターフェースを構築する観点から関与している可能性があります。

The major entity at play, of course, is the hotel property itself, to which other entities are linked such as: 
もちろん、主要なエンティティはホテルの物件そのものであり、他のエンティティは以下のようにリンクされています：

- Contact information sourced from the hotel, Google’s local data, Google users, and third-party sources 
- ホテル、Googleのローカルデータ、Googleユーザー、および第三者のソースから取得された連絡先情報

- Hotel class ratings assigned by Google based on data from “third-party partners, direct research, feedback from hoteliers, and machine learning inference that examines and evaluates hotel attributes, such as price, location, room size, and amenities” 
- 「第三者パートナー、直接調査、ホテル業者からのフィードバック、および価格、場所、部屋のサイズ、アメニティなどのホテル属性を調査・評価する機械学習推論」に基づいてGoogleによって割り当てられたホテルクラス評価

- Booking rates from Google’s Hotel Ads marketplace 
- Googleのホテル広告マーケットプレイスからの予約料金

- Reviews from Google users, third-party reviews from booking sites like Expedia and travel sites like TripAdvisor, and first-party reviews (if available) sourced by the hotel itself 
- Googleユーザーからのレビュー、Expediaのような予約サイトやTripAdvisorのような旅行サイトからの第三者レビュー、そしてホテル自体から取得されたファーストパーティレビュー（利用可能な場合）

- Review summaries created by Google partner TrustYou 
- GoogleパートナーのTrustYouによって作成されたレビューの要約

- Amenity data sourced from the hotel and from Google users 
- ホテルおよびGoogleユーザーから取得されたアメニティデータ

- Photos, videos, and 360 degree images sourced from the hotel, Google users, and third-party sites like Oyster 
- ホテル、Googleユーザー、およびOysterのような第三者サイトから取得された写真、動画、360度画像

- Descriptive text sourced from Google’s editorial team, partially powered by web mining 
- Googleの編集チームから取得された記述テキスト（部分的にウェブマイニングによって強化）

- Neighborhood data including descriptive text and Google’s own location ratings 
- 記述テキストとGoogle自身のロケーション評価を含む近隣データ

- Neighborhood maps with points of interest identified 
- 特徴的な地点が特定された近隣地図

- Nearby attractions pulled in from Google Maps 
- Googleマップから引き出された近くの観光名所

- Links to transportation and directions also from Google Maps 
- Googleマップからの交通機関や道順へのリンク

It’s an impressive compendium of data. 
これは印象的なデータの集大成です。

For a while now, it has been assumed that Knowledge Panels represented the best showcase of Google entity data, and this remains true for many other businesses, celebrities, and historical figures. 
しばらくの間、Knowledge PanelsがGoogleエンティティデータの最良のショーケースを表していると考えられており、これは他の多くのビジネス、著名人、歴史的人物にも当てはまります。

But Knowledge Panels generally work from a smaller set of data sources, such as Google Maps itself for businesses or Wikipedia for historical figures. 
しかし、Knowledge Panelsは一般的に、ビジネスの場合はGoogleマップ自体や歴史的人物の場合はWikipediaなど、より小さなデータソースのセットから機能します。

Google Hotels represents a significantly expanded dataset with a more complex mix of sources, one that represents a step away from dependence on a pre-existing body of knowledge, and a step toward self-sufficient population of the Knowledge Graph. 
Google Hotelsは、より複雑なソースのミックスを持つ大幅に拡張されたデータセットを表しており、既存の知識体系への依存からの一歩を示し、Knowledge Graphの自給自足的な人口に向けた一歩を示しています。

To be sure, there are reasons why hotels would be an obvious choice for this evolutionary step. 
確かに、ホテルがこの進化的ステップの明白な選択肢である理由はいくつかあります。

They are, after all, discrete entities in the world about which it is relatively straightforward to accumulate reliable, verifiable information. 
結局のところ、彼らは信頼できる検証可能な情報を比較的簡単に蓄積できる世界の中の離散的なエンティティです。

It’s a big leap from hotels to more controversial entities like Taiwan, Jerusalem, and Hillary Clinton. 
ホテルから台湾、エルサレム、ヒラリー・クリントンのようなより物議を醸すエンティティへの大きな飛躍です。

Wikipedia has been able to maintain a neutral position when dealing with controversy, in part due to the fact that well-managed crowdsourcing does an excellent job of evening out bias, and in part due to its old-school insistence on authoritative primary sources. 
Wikipediaは、物議を醸す問題に対処する際に中立的な立場を維持できていますが、これは部分的には、適切に管理されたクラウドソーシングがバイアスを均等にするのに優れた仕事をしているためであり、部分的には権威ある一次情報源に対する古典的な主張によるものです。

It remains to be seen how Google will ensure that the Knowledge Graph doesn’t place undue reliance on sources that shouldn’t be trusted but happen to contain readily parseable information. 
GoogleがKnowledge Graphが信頼されるべきでないソースに過度に依存しないようにするかは、今後の課題です。
That’s just one of the many challenges inherent in the project. 
それは、このプロジェクトに内在する多くの課題の1つに過ぎません。
But the progress represented by Google Hotels suggests that Google is making a serious attempt at turning its patented technology into a reality, one that may augur a fundamental transformation in search. 
しかし、Google Hotelsが示す進展は、Googleがその特許技術を現実に変える真剣な試みを行っていることを示唆しており、これは検索における根本的な変革を予告するかもしれません。
