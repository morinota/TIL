refs: https://blog.google/products-and-platforms/products/search/introducing-knowledge-graph-things-not/?utm_source=chatgpt.com

# Introducing the Knowledge Graph: things, not strings 知識グラフの紹介：文字列ではなく物事
May 16, 2012
·
Search is a lot about discovery—the basic human need to learn and broaden your horizons. But searching still requires a lot of hard work by you, the user. So today I’m really excited to launch the Knowledge Graph, which will help you discover new information quickly and easily.
検索は発見に関するものであり、学び、視野を広げるという基本的な人間の欲求です。しかし、**検索には依然としてユーザーであるあなたの多くの努力が必要**です。そこで、今日は知識グラフを発表できることに非常に興奮しています。これにより、あなたは新しい情報を迅速かつ簡単に発見できるようになります。

Take a query like [taj mahal]. 
[taj mahal]のようなクエリを考えてみてください。 
For more than four decades, search has essentially been about matching keywords to queries. 
40年以上にわたり、検索は基本的にキーワードをクエリに一致させることに関するものでした。 
To a search engine the words [taj mahal] have been just that—two words. 
検索エンジンにとって、[taj mahal]という言葉は単に2つの単語に過ぎません。 

But we all know that [taj mahal] has a much richer meaning. 
しかし、私たちは皆、**[taj mahal]がはるかに豊かな意味を持っている**ことを知っています。 
You might think of one of the world’s most beautiful monuments, or a Grammy Award-winning musician, or possibly even a casino in Atlantic City, NJ. 
あなたは、世界で最も美しいモニュメントの1つ、またはグラミー賞を受賞したミュージシャン、あるいはアトランティックシティのカジノを思い浮かべるかもしれません。 
Or, depending on when you last ate, the nearest Indian restaurant. 
あるいは、最後に食事をした時期によっては、最寄りのインド料理店かもしれません。 
It’s why we’ve been working on an intelligent model—in geek-speak, a “graph”—that understands real-world entities and their relationships to one another: things, not strings. 
**それが、私たちが現実のエンティティとそれらの相互関係を理解するインテリジェントなモデル（いわゆる「グラフ」）に取り組んできた理由です：文字列ではなく物事**です。

The Knowledge Graph enables you to search for things, people or places that Google knows about—landmarks, celebrities, cities, sports teams, buildings, geographical features, movies, celestial objects, works of art and more—and instantly get information that’s relevant to your query. 
知識グラフは、Googleが知っている物事、人々、または場所（ランドマーク、著名人、都市、スポーツチーム、建物、地理的特徴、映画、天体、芸術作品など）を検索し、あなたのクエリに関連する情報を瞬時に取得できるようにします。 
This is a critical first step towards building the next generation of search, which taps into the collective intelligence of the web and understands the world a bit more like people do. 
これは、ウェブの集合的知性を活用し、人々のように世界を少し理解する次世代の検索を構築するための重要な第一歩です。 
Google’s Knowledge Graph isn’t just rooted in public sources such as Freebase, Wikipedia and the CIA World Factbook.
Googleの知識グラフは、Freebase、Wikipedia、CIA World Factbookなどの公的な情報源に基づいているだけではありません。 
It’s also augmented at a much larger scale—because we’re focused on comprehensive breadth and depth. 
それは、包括的な広がりと深さに焦点を当てているため、はるかに大規模に拡張されています。 
It currently contains more than 500 million objects, as well as more than 3.5 billion facts about and relationships between these different objects. 
現在、500百万以上のオブジェクトと、これらの異なるオブジェクトに関する35億以上の事実と関係を含んでいます。 
And it’s tuned based on what people search for, and what we find out on the web. 
そして、それは人々が何を検索するか、そして私たちがウェブ上で何を見つけるかに基づいて調整されています。 

The Knowledge Graph enhances Google Search in three main ways to start: 
知識グラフは、Google検索を開始するための3つの主要な方法で強化します：

<!-- ここまで読んだ! -->

## 1. Find the right thing 適切なものを見つける

Language can be ambiguous—do you mean Taj Mahal the monument, or Taj Mahal the musician? 
言語は曖昧であり、あなたはタージ・マハルの記念碑を指しているのか、それともタージ・マハルの音楽家を指しているのか？ 
Now Google understands the difference, and can narrow your search results just to the one you mean—just click on one of the links to see that particular slice of results:
今やGoogleはその違いを理解しており、あなたが意味するものに検索結果を絞り込むことができます—特定の結果のスライスを見るには、リンクの1つをクリックするだけです。

![]()

This is one way the Knowledge Graph makes Google Search more intelligent—your results are more relevant because we understand these entities, and the nuances in their meaning, the way you do.
これは、Knowledge GraphがGoogle検索をよりインテリジェントにする方法の1つです—私たちがこれらのエンティティとその意味のニュアンスを理解することで、あなたの結果はより関連性の高いものになります。

<!-- ここまで読んだ! -->

## 2. Get the best summary 最良の要約を得る

With the Knowledge Graph, Google can better understand your query, so we can summarize relevant content around that topic, including key facts you’re likely to need for that particular thing. 
Knowledge Graphを使用することで、Googleはあなたのクエリをよりよく理解できるため、そのトピックに関連するコンテンツを要約し、特定の事柄に必要と思われる重要な事実を含めることができます。 
For example, if you’re looking for Marie Curie, you’ll see when she was born and died, but you’ll also get details on her education and scientific discoveries: 
例えば、マリー・キュリーを探している場合、彼女が生まれた年と亡くなった年が表示されるだけでなく、彼女の教育や科学的発見に関する詳細も得られます。

![]()

How do we know which facts are most likely to be needed for each item? 
どの事実が各項目に最も必要とされる可能性が高いかをどのように知るのでしょうか？
For that, we go back to our users and study in aggregate what they’ve been asking Google about each item. 
そのために、私たちはユーザーに戻り、彼らが各項目についてGoogleに何を尋ねているのかを集計して研究します。
For example, people are interested in knowing what books Charles Dickens wrote, whereas they’re less interested in what books Frank Lloyd Wright wrote, and more in what buildings he designed. 
例えば、人々はチャールズ・ディケンズが書いた本を知りたがっていますが、フランク・ロイド・ライトが書いた本にはあまり興味がなく、彼が設計した建物にもっと興味を持っています。

The Knowledge Graph also helps us understand the relationships between things. 
**Knowledge Graphは、物事の関係を理解するのにも役立ちます。**
Marie Curie is a person in the Knowledge Graph, and she had two children, one of whom also won a Nobel Prize, as well as a husband, Pierre Curie, who claimed a third Nobel Prize for the family. 
マリー・キュリーはKnowledge Graphの中の人物であり、彼女には二人の子供がいて、そのうちの一人もノーベル賞を受賞しました。また、彼女の夫であるピエール・キュリーは、家族のために三つ目のノーベル賞を受賞しました。
All of these are linked in our graph. 
これらすべては私たちのグラフの中でリンクされています。
It’s not just a catalog of objects; it also models all these inter-relationships. 
これは単なるオブジェクトのカタログではなく、これらの相互関係をすべてモデル化しています。
It’s the intelligence between these different entities that’s the key. 
**異なるエンティティ間の知性こそが鍵**です。

<!-- ここまで読んだ! -->

## 3. Go deeper and broader

Finally, the part that’s the most fun of all—the Knowledge Graph can help you make some unexpected discoveries. 
**最後に、最も楽しい部分、つまりKnowledge Graphはあなたが予期しない発見をする手助け**をしてくれます。
You might learn a new fact or new connection that prompts a whole new line of inquiry. 
新しい事実や新しいつながりを学ぶことで、まったく新しい探求の道が開かれるかもしれません。
Do you know where Matt Groening, the creator of the Simpsons (one of my all-time favorite shows), got the idea for Homer, Marge and Lisa’s names? 
シンプソンズの創作者であるマット・グレイニングが、ホーマー、マージ、リサの名前のアイデアをどこから得たか知っていますか？ 
It’s a bit of a surprise: 
それは少し驚きです：

![]()

We’ve always believed that the perfect search engine should understand exactly what you mean and give you back exactly what you want. 
私たちは常に、完璧な検索エンジンはあなたの意図を正確に理解し、あなたが求めるものを正確に返すべきだと信じてきました。
And we can now sometimes help answer your next question before you’ve asked it, because the facts we show are informed by what other people have searched for. 
そして、私たちは今や、他の人が検索した内容に基づいて表示される事実によって、あなたが質問する前に次の質問に答える手助けをすることができるようになりました。
For example, the information we show for Tom Cruise answers 37 percent of next queries that people ask about him. 
例えば、トム・クルーズに関する情報は、彼について人々が次に尋ねる質問の37パーセントに答えています。
In fact, some of the most serendipitous discoveries I’ve made using the Knowledge Graph are through the magical “People also search for” feature. 
**実際、Knowledge Graphを使用して行った最も偶然の発見のいくつかは、魔法のような「People also search for」機能を通じて得られました。**
One of my favorite books is The White Tiger, the debut novel by Aravind Adiga, which won the prestigious Man Booker Prize. 
私のお気に入りの本の一つは、アラヴィンド・アディガのデビュー小説『ホワイト・タイガー』で、これは権威あるマン・ブッカー賞を受賞しました。
Using the Knowledge Graph, I discovered three other books that had won the same prize and one that won the Pulitzer. 
Knowledge Graphを使用して、同じ賞を受賞した他の3冊の本と、ピューリッツァー賞を受賞した1冊を発見しました。
I can tell you, this suggestion was spot on! 
この提案は的確だったと言えます！

We’ve begun to gradually roll out this view of the Knowledge Graph to U.S. English users. 
私たちは、アメリカ英語のユーザーに対してこのKnowledge Graphのビューを徐々に展開し始めました。
It’s also going to be available on smartphones and tablets—read more about how we’ve tailored this to mobile devices. 
これはスマートフォンやタブレットでも利用可能になる予定です—私たちがこれをモバイルデバイスにどのように調整したかについてもっと読むことができます。
And watch our video (also available on our site about the Knowledge Graph) that gives a deeper dive into the details and technology, in the words of people who've worked on this project: 
そして、このプロジェクトに関わった人々の言葉で、詳細と技術について深く掘り下げた動画（Knowledge Graphに関する私たちのサイトでも利用可能）を見てください：

<!-- ここまで読んだ! -->

#### Introducing the Knowledge Graph

We hope this added intelligence will give you a more complete picture of your interest, provide smarter search results, and pique your curiosity on new topics. 
私たちは、この追加された知性があなたの興味のより完全なイメージを提供し、より賢い検索結果を提供し、新しいトピックへの好奇心を刺激することを願っています。
We’re proud of our first baby step—the Knowledge Graph—which will enable us to make search more intelligent, moving us closer to the "Star Trek computer" that I've always dreamt of building. 
私たちは、検索をより知的にし、私が常に構築したいと夢見てきた「スタートレックのコンピュータ」に近づくことを可能にする最初の一歩であるKnowledge Graphを誇りに思っています。
Enjoy your lifelong journey of discovery, made easier by Google Search, so you can spend less time searching and more time doing what you love. 
Google Searchによって容易にされた発見の生涯にわたる旅を楽しんでください。そうすれば、検索に費やす時間を減らし、あなたが愛することにもっと多くの時間を使うことができます。

<!-- ここまで読んだ! -->
