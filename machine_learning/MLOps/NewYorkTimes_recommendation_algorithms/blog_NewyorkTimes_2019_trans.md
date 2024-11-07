<!-- これ読む! -->

# How The New York Times is Experimenting with Recommendation Algorithms ニューヨーク・タイムズ紙はどのように推薦アルゴリズムを試しているか

Algorithmic curation at The Times is used in designated parts of our website and apps.
The Timesのアルゴリズム・キュレーションは、ウェブサイトやアプリの指定された部分で使用されています。

The New York Times will publish around 250 articles today, but most readers will only see a fraction of them.
ニューヨーク・タイムズ紙は今日、約250本の記事を掲載するが、ほとんどの読者はそのうちのほんの一部しか目にすることはないだろう。
The majority of our readers access The New York Times online, not on paper, and often using small devices, which means we have a “real estate” problem: we produce more journalism than we have space to surface to readers at any given time.
読者の大半は、紙ではなくオンラインでニューヨーク・タイムズ紙にアクセスし、しばしば小さなデバイスを使用している。これは、**我々がいつでも読者に提供するスペースがある以上に多くのジャーナリズムを生産しているという「real estate(不動産?)」の問題**を意味する。
(i.e. The New York Timesは、限られた画面スペースにどの記事を優先的に表示するかという「スペース（不動産）」の問題に直面している、みたいな...!:thinking:)

To help our readers discover the breadth of our reporting, The Times is experimenting with new ways to deliver more of our journalism to readers.
**読者の皆様にタイムズの報道の幅広さを知っていただくため、タイムズはジャーナリズムをより多く読者の皆様にお届けする新しい方法**を試みています。
We are building real-time feeds, specialized newsletters and customizable parts of our news app.
私たちは、リアルタイムフィード、専門ニュースレター、およびニュースアプリのカスタマイズ可能な部分を構築しています。
We are also using recommendation algorithms to highlight articles that are particularly relevant to our readers.
また、特に読者に関連する記事を強調するために、推薦アルゴリズムを使用しています。

Algorithmic curation at The Times is used in designated parts of our website and apps.
The Timesのアルゴリズム・キュレーションは、ウェブサイトやアプリの指定された部分で使用されています。
We use it to select content where manual curation would be inefficient or difficult, like in the Smarter Living section of the homepage or in Your Weekly Edition, a personalized newsletter.
私たちは、**ホームページの「スマーターリビング」セクションやパーソナライズされたニュースレター「Your Weekly Edition」など、手動キュレーションが非効率的または困難なコンテンツを選択するために使用**しています。(この時点ではNYTも、手動 & アルゴリズムが互いに得意不得意を補い合うような形で使われてそう...!:thinking:)
Personalization algorithms are used to complement the editorial judgment that determines what stories lead our news report.
パーソナライゼーション・アルゴリズムは、ニュースレポートの先頭をリードするストーリーを決定する**編集判断を補完するために使用**されています。(あれ、そうでもない??一緒に一つの出面を構成するユースケースもある??:thinking:)

<!-- ここまで読んだ! -->

## A contextual recommendation approach 文脈に基づく推薦アプローチ

One recommendation approach we have taken uses a class of algorithms called contextual multi-armed bandits.
私たちがとった推薦アプローチのひとつは、コンテクスチュアル・マルチ・アームド・バンディットと呼ばれるアルゴリズムのクラスを使用する。
Contextual bandits learn over time how people engage with particular articles.
**contextual banditsは、時間の経過とともに、人々が特定の記事とどのように関わるかを学習する**。
(contextual banditか通常の教師あり学習モデルかの意味合いの違いって、オンライン学習ができるか否か、みたいなことなのかな:thinking:)
They then recommend articles that they predict will garner higher engagement from readers.
そして、読者のエンゲージメントが高まると予測される記事を推薦する。
The contextual part means that these bandits can use additional information to get a better estimate of how engaging an article might be to a particular reader.
**contextualな部分は、これらのバンディットが、特定の読者にとって記事がどの程度魅力的かをよりよく推定するために追加情報を使用できること**を意味する。
For example, they can take into account a reader’s geographical region (like country or state) or reading history to decide if a particular article would be relevant to that reader.
たとえば、読者の地域（国や州など）や読書歴を考慮して、特定の記事がその読者に関連するかどうかを決定することができる。

The algorithm we used is based on a simple linear model that relates contextual information—like the country or state a reader is in—to some measure of engagement with each article, like click-through rate.
私たちが使用したアルゴリズムは、**読者がいる国や州などのコンテクスト情報と、クリックスルー率などの各記事へのエンゲージメントのいくつかの指標との関係を示す単純な線形モデルに基づいている**。(なるほど...! 開発・運用コスト低いのかも...??:thinking:)
When making new recommendations, it chooses articles more frequently if they have high expected engagement for the given context.
新しいレコメンデーションを行う際、与えられた文脈に対して期待されるエンゲージメントが高い記事をより頻繁に選択する。
("より頻繁に"ってことは、やっぱり探索的な要素も一定あるんだよね...! contextual banditにおける探索戦略:thinking:)
(contextを使っていることに加えて、「オンライン学習ができること」と「探索的な要素があること」があれば、contextual banditとみなせる...???:thinking:)

<!-- ここまで読んだ! -->

## Using contextual bandits for article recommendations 記事推薦に文脈盗賊を使う

One model we implemented is a geo-bandit that tries to optimize the expected click-through rate of a set of articles based on the state in which the reader is located.
私たちが実装したモデルのひとつに、**読者がいる州に基づいて、一連の記事の期待されるクリックスルー率を最適化しようとするジオバンディット**がある。
To illustrate this, let’s say we’ve shown two articles—article A and article B—to readers, capturing data about the states that readers were located in and whether they clicked on the articles.
これを説明するために、読者に記事Aと記事Bの2つを表示し、**読者がどの州にいたかと記事をクリックしたかどうかについてのデータ(同時確率のサンプル...!:thinking:)を収集した**としましょう。

```python
[“recommended”: “article B”; “reader state”: “Texas”, “clicked”: “yes”][“recommended”: “article A”; “reader state”: “New York”, “clicked”: “yes”][“recommended”: “article B”; “reader state”: “New York”, “clicked”: “no”][“recommended”: “article B”; “reader state”: “California”, “clicked”: “no”][“recommended”: “article A”; “reader state”: “New York”, “clicked”: “no”]
```

Once the bandit has been trained on the initial data, it might suggest Article A, Article B or a new article, C, for a new reader from New York.
**いったんバンディットが初期データで訓練**(うんうん、これはバッチ学習...!:thinking:)されると、ニューヨークからの新しい読者のために、記事A、記事B、あるいは新しい記事Cを提案するかもしれない。
The bandit would be most likely to recommend Article A because the article had the highest click-through rate with New York readers in the past.
上記の例では、バンディットは、過去にニューヨークの読者に最も高いクリックスルー率を持つ記事である記事Aを最も推薦する可能性が高い。(うんうん、これは活用...!:thinking:)
With some smaller probability, it might also try showing Article C, because it doesn’t yet know how engaging it is and needs to generate some data to learn about it.
より小さな確率で、記事Cを表示してみるかもしれない。なぜなら、記事Cがどの程度魅力的かまだわからず、それについて学ぶためにデータを生成する必要があるからだ。
(うんうん、これは探索...!:thinking:)

Over time, it will get a really good estimate of every article’s click-through rate given every possible location and then mostly show articles it expects to perform best in a given context.
時間が経つにつれて、すべての可能な場所における各記事のクリックスルー率について非常に良い推定値を得ることになり、その後、与えられた文脈で最もよく機能すると予想される記事をほとんど表示することになる。
(やっぱりオンライン学習前提なんだな...!:thinking:)

<!-- ここまで読んだ! -->

### Why use geographical information? なぜ地理情報を使うのか？

We chose to use approximate geographical location because it’s one type of contextual information that is readily available in web browsers and apps.
**おおよその地理的位置を使うことにしたのは、ウェブブラウザやアプリですぐに利用できるコンテキスト情報の1つだから**だ。
While location is not always relevant for news consumption, parts of our report are more relevant to readers in certain parts of the United States or the world.
ニュースの消費に所在地が常に関係するとは限らないが、当レポートの一部は、米国や世界の特定の地域の読者にとってより適切なものである。

There are many other types of contextual information, some of which we have implemented.
文脈情報には他にも多くの種類があり、そのうちのいくつかは私たちが実装している。
They include a reader’s device type; the time of day where a reader is located; how many stories a reader has viewed in a particular news section, from which we can gauge interest in a particular topic.
それらには、読者のデバイスタイプ、読者がいる時間帯、読者が特定のニュースセクションでいくつのストーリーを見たかなどが含まれる。これにより、特定のトピックに対する関心を測定することができる。
We have found that depending on the type of articles we’re recommending, different kinds of context variables help the model perform better.
私たちは、**推薦している記事の種類によって、異なる種類のコンテキスト変数(=特徴量)がモデルのパフォーマンスを向上させることを発見**した。

(やっぱりこういう話を聞いてくると、特徴量を使って学習するアプローチが望ましそうと感じてくるな...!:thinking:)
(それを実現しようとすると、feature storeとかの導入を考えた方が良さそう。バッチ学習・バッチ推論だけならDWHやデータレイクに保存するだけでもそこまで困らないかも?? でも結局は特徴量が作られた時間を考慮して学習させる必要があるから、特徴量のバージョン管理的な意図でもfeature storeを利用した方が開発・運用しやすそう...?:thinking:)

<!-- ここまで読んだ! -->

## Choosing the most relevant from Editors’ Picks エディターズ・ピックから最も関連性の高いものを選ぶ

We tested a version of the geo-bandit described above in a recommendation module called Editors’ Picks, which shows up in a right-hand column alongside our articles.
私たちは、上記で説明したジオバンディットのバージョンを、**Editors’ Picks**という推薦モジュールでテストした。このモジュールは、私たちの記事と並んで右側の列に表示される。
As the name suggests, editors choose about 30 noteworthy pieces of journalism for the module.
Editors' Picksモジュールはその名の通り、編集者が約30の注目すべきジャーナリズム作品を選び、モジュールに掲載する。
We then use a geo bandit to select which particular articles to show to readers based on their location (which we broadly defined by state or region).
そして、ジオバンディットを使用して、読者の場所に基づいて（州や地域で広く定義される）どの特定の記事を表示するかを選択する。

Here are some examples of headlines from articles the geo-bandit recommended to readers in different states.
以下は、ジオバンディットが各州の読者に推薦した記事の見出しの例である。

---
New York
ニューヨークの場合

I Know the Struggle’: Why a Pizza Mogul Left Pies at Memorials to 4 Homeless Men
私は苦労を知っている」： ピザの巨匠が4人のホームレス追悼式にパイを置いた理由

Scientists Designed a Drug for Just One Patient.
科学者たちは、たった一人の患者のために薬を設計した。
Her Name Is Mila.
彼女の名前はミラ。

Chasing the Perfect Slice, Bread and Salt in Jersey City Looks to Rome
完璧な一切れを求めて、ジャージーシティのパンと塩はローマを目指す

The Phones Are Alive, With the Sounds of Katie Couric
電話は生きている、ケイティ・クーリックの音とともに

---
Texas
テキサス

When My Louisiana School and Its Football Team Finally Desegregated
ルイジアナ州の学校とフットボールチームがついに人種差別を撤廃したとき

This Is an Indian House, According to One Architect
ある建築家が語るインドの家

No One Needs a Superyacht, but They Keep Selling Them
誰もスーパーヨットを必要としていないのに、売られ続けている

The Phones Are Alive, With the Sounds of Katie Couric
電話は生きている、ケイティ・クーリックの音とともに

---
Wisconsin
ウィスコンシン州

When My Louisiana School and Its Football Team Finally Desegregated
ルイジアナ州の学校とフットボールチームがついに人種差別を撤廃したとき

The Phones Are Alive, With the Sounds of Katie Couric
電話は生きている、ケイティ・クーリックの音とともに

36 Hours in Milwaukee
ミルウォーキーで36時間

No One Needs a Superyacht, but They Keep Selling Them
誰もスーパーヨットを必要としていないのに、売られ続けている

---

Note how the recommendations include articles that are popular across all of the regions (“The Phones Are Alive, With the Sounds of Katie Couric”), while also capturing different regional interests (“36 Hours in Milwaukee”).
おすすめ記事には、全地域で人気のある記事（「電話は生きている、ケイティ・クーリックの音とともに」）が含まれていることに注目してください。また、異なる地域の関心も捉えている（「ミルウォーキーで36時間」）。
By making regionally relevant recommendations, we were able to increase the click-through rate on the Editors’ Picks module by 55 percent, compared to randomly choosing from the pool of articles selected by editors.
**地域に関連する推薦を行うことで、編集者が選んだ記事のプールからランダムに選ぶよりも、Editors’ Picksモジュールのクリックスルー率を55%向上させることができた**。

<!-- ここまで読んだ! -->

## How we implemented contextual bandits How we implemented contextual bandits

Although the underlying algorithm is relatively simple, contextual bandits can be challenging to implement.
**基本的なアルゴリズムは比較的単純だが、contextual banditsを実装することは難しくなりうる**。(オンライン学習とオンライン推論が難しそう...!:thinking:)
Bandits must be continuously re-trained with new data on reader engagement with articles on the Times homepage or apps.
バンディットは、タイムズのホームページやアプリの記事に対する読者のエンゲージメントに関する**新しいデータで継続的に再トレーニング**されなければならない。(オンライン学習と言っても、1時間に一回、とかでもいいのかな:thinking:)
This means that not only do we need accurate data on which articles readers read (click data), we need accurate data on what articles were shown to readers (impression data).
つまり、**読者がどの記事を読んだかという正確なデータ（クリックデータ）だけでなく、どの記事が読者に表示されたかという正確なデータ（インプレッションデータ）が必要**なのだ。

Further complicating bandit implementation is the need to do these calculations quickly.
**バンディットの実装をさらに複雑にしているのは、これらの計算を素早く行う必要があること**だ。
As readers visit our page, recommendations need to be made in real-time to avoid blank sections of the page.
読者がページを訪れると、ページの空白部分を避けるためにリアルタイムで推薦を行わなければならない。
This real-time requirement also means that any contextual information about the reader has to be made available for our algorithm along with the recommendation request.
このリアルタイムの要件はまた、読者に関するあらゆるcontext情報が、推薦リクエストとともにアルゴリズムに利用可能である必要があることを意味する。
(特徴量へのリアルタイムアクセスが必要って話...! まあこれも、頻度高めのバッチ推論とかでも運用はできそうな気がする:thinking:)

Keeping these requirements in mind, we re-train on the most recent data generated by readers interacting with content on our site, and we re-deploy bandit models every 15 minutes.
これらの要件を念頭に置きながら、私たちはサイト上の**コンテンツに接触する読者によって生成された最新のデータに基づいて再トレーニングを行い、15分ごとにバンディット・モデルを再展開**している。
The models are deployed via Kubernetes and training runs are orchestrated using Kubernetes cron jobs.
モデルはKubernetes経由でデプロイされ、トレーニングの実行はKubernetesのcronジョブを使用してオーケストレーションされる。
The training data comes from our main event tracking store in BigQuery.
**トレーニングデータは、BigQueryのメインイベントトラッキングストアから取得**した。
(やっぱりDWHから取得するよね。このデータストアは高頻度で更新されるやつなのかな...!:thinking:)

To ensure we have an accurate measurement of what articles were shown to readers, along with data about which articles were read in full, we implemented impression tracking.
読者にどのような記事が表示されたかを正確に測定し、どの記事が全文読まれたかというデータを確実に得るために、インプレッション・トラッキングを導入しました。
We found it particularly useful to store a unique ID for every article impression and carry that ID forward whenever a reader clicks on an article.
私たちは、**記事のインプレッションごとに一意のIDを保存し、読者が記事をクリックするたびにそのIDを引き継ぐことが特に有用であることを発見**した。
This allows us to join impressions and clicks easily during training.
**これにより、トレーニング中にインプレッションとクリックを簡単に結びつけることができる**。

Using BigTable, we maintain a low-latency store that allows us to quickly access a reader’s recent reading history; We use the articles a reader has read in the past 30 days to build some of the contextual features.
BigTableを使用して、読者の最近の読書履歴に素早くアクセスできる低レイテンシーのストアを維持している。というのも、過去30日間に読んだ記事を使用して、いくつかのコンテクスト特徴を構築している。

We wrote our contextual bandits in Python, but to ensure they can respond fast enough to meet our latency requirements, we rewrote some of the functionality in Cython, a compiler that translates Python to equivalent C code.
私たちはPythonでコンテキスト・バンディットを書いたが、**レイテンシの要件を満たすのに十分な速さで応答できるようにするため、Pythonを同等のCコードに変換するコンパイラであるCythonで機能の一部を書き直した**。

<!-- ここまで読んだ! -->

## A recommendation toolbox that helps readers find more stories 読者がより多くのストーリーを見つけるためのレコメンデーション・ツールボックス

Using contextual bandits got us pretty far in terms of increasing reader engagement.
**読者のエンゲージメントを高めるという点では、コンテクスチュアル・バンディットを使うことで、かなり遠くまで行くことができた**。(強い...!:thinking:)
But like any algorithm, contextual bandits have strengths and weaknesses.
しかし、他のアルゴリズムと同様、contextual banditsには長所と短所がある。
Bandit algorithms are great at quickly adapting to changing preferences and efficiently it exploring new options.
バンディット・アルゴリズムは、変化する嗜好に素早く適応し、新しい選択肢を効率的に探索することに長けている。
A downside is that they are not primarily designed to make recommendations that feel personalized.
欠点は、パーソナライズされた感じの推薦を行うことを主な目的としてデザインされていないことだ。

Next, we want to combine contextual multi-armed bandits with other models in our recommendation toolbox—like collaborative filtering or content-based recommenders—that include a more fine-grained representation of readers and their interests.
次に私たちは、**協調フィルタリングやコンテンツベースのレコメンダーなど、レコメンデーションツールボックスにある他のモデルとコンテクスチュアル・マルチ・アームド・バンディットを組み合わせたい**と考えている。
By adding outputs of these models as context features to a contextual bandit, we hope to leverage the strength of each approach and get another step closer to our goal of helping our readers discover the coverage most relevant to them.
**これらのモデルの出力をcontexual特徴量としてcontextual banditに追加する**ことで、各アプローチの強みを活用し、読者が最も関連性の高いカバレッジを発見するという目標にさらに近づけることを期待している。

Anna Coenen is a Senior Data Scientist at The New York Times.
Anna Coenenはニューヨーク・タイムズのシニア・データ・サイエンティスト。
She also enjoys plants, cats and cognitive science.
趣味は植物、猫、認知科学。

<!-- ここまで読んだ! -->
