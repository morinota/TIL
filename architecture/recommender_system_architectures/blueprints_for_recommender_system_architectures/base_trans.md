## link 

- https://amatriain.net/blog/RecsysArchitectures httpsを使用しています。

# Blueprints for recommender system architectures: 10th anniversary edition ♪推薦システムアーキテクチャのための青写真。 10周年記念版

Ten years ago, we published a post in the Netflix tech blog explaining our three-tier architectural approach to building recommender systems (see below).
10年前、私たちはNetflixの技術ブログに、レコメンダーシステム構築のための3層アーキテクチャのアプローチについて説明した記事を掲載しました（下記参照）。
A lot has happened in the last 10 years in the recommender systems space for sure.
この10年間、確かにレコメンダー・システムの分野では多くのことが起こりました。
That’s why, when a few months back I designed a Recsys course for Sphere, I thought it would be a great opportunity to revisit the blueprint.
だからこそ、数ヶ月前に Sphere の Recsys コースをデザインしたとき、この青写真を見直す良い機会になると思ったのです。

In this blog post I summarize 4 existing architectural blueprints, and present a new one that, in my opinion, encompasses all the previous ones.
このブログでは、既存の4つのアーキテクチャーの青写真を要約し、私が考える、これまでのものをすべて包含する新しい青写真を提示します。

At a very high-level, any recommender system has items to score and/or rank, and a machine learned model that does that. This model needs to be trained on some data, which is obtained from the service where the recommender operates in some form of feedback loop. The architectural blueprints that we will see below connect those components (and others) in a general way while incorporating some best practices and guidelines.非常に高いレベルでは、どんなレコメンダーシステムも、スコアやランク付けをする項目と、それを行う機械学習モデルを持っています。このモデルはいくつかのデータで学習される必要があり、それはレコメンダーがある種のフィードバックループで動作しているサービスから取得されます。以下に示すアーキテクチャーの青写真は、いくつかのベストプラクティスやガイドラインを取り入れながら、これらのコンポーネント（およびその他のコンポーネント）を一般的な方法で接続するものです。

## The Netflix three tier architecture ネットフリックスの3層構造

In our post ten years ago, we focused on clearly distinguishing the components that can be executed offline (i.e. not when the recommendations need to be served but rather e.g. once a day), those that need to be computed online (i.e. when the user visits the site and the recommendation is being served) and those somewhere in the middle called nearline (i.e. components that are executed when the user visits the site, but do not need to be served in real-time).
10年前の投稿では、オフラインで実行できるコンポーネント（つまり、レコメンドを提供する必要があるときではなく、例えば1日に1回）、オンラインで計算する必要があるコンポーネント（つまり、ユーザーがサイトを訪問してレコメンドが提供されているとき）、ニアラインという中間のコンポーネント（つまり、ユーザーがサイトを訪れたときに実行するがリアルタイムで提供する必要はない）を明確に区別することに焦点を合わせました。
At that time, and still today in many cases, most of the big data training of the algorithm was performed offline using systems such as Hadoop or Spark.
当時も現在も多くの場合、アルゴリズムのビッグデータ学習は、HadoopやSparkといったシステムを用いてオフラインで行われている。
The nearline layer included things like filtering in response to user events, but also some retraining capabilities such as e.g. folding-in and incremental matrix factorization training (see here for a practical introduction to the topic).
ニアライン層には、ユーザーイベントに対応したフィルタリングのようなものだけでなく、例えばフォールディングインや漸進的行列分解トレーニングのような再トレーニング機能もありました（この話題の実用的な紹介はこちらをご覧ください）。

![](https://amatriain.net/blog/images/NetflixArchitecture.png)

Ten years ago I felt like this architecture was state of the art.
10年前、私はこのアーキテクチャが最先端であると感じていました。
A lot of things have happened since then in the machine learning world, but this three tiered approach is still pretty relevant.
あれから機械学習の世界では様々なことが起こりましたが この3層のアプローチは今でもかなり有効です。
Let’s fast forward.
では、話を先に進めましょう。

## Eugene Yan’s 2 x 2 blueprint ♪ユージン・ヤンの2×2の設計図

Amazon’s Eugene Yan does an amazing job of compiling many industry posts in his june 2021 post.
AmazonのEugene Yanは、2021年6月の投稿で、多くの業界の投稿をまとめた素晴らしい仕事をしています。
He cites and describes systems from Alibaba, Facebook, JD, Doordash, and LinkedIn.
彼は、Alibaba、Facebook、JD、Doordash、LinkedInのシステムを引用し、説明しています。
If you are interested in this space, you should totally read his post (and the rest of his blog btw).
もしあなたがこの領域に興味があるなら、彼の投稿（そして彼のブログの他の部分も）を完全に読むべきです。
After this amazing compilation and distillation work, he presents the following 2x2 blueprint:
この驚くべき編集と蒸留作業の後、彼は以下の2x2の青写真を提示します。

There are a few things worth noting here.
ここで注目すべき点がいくつかあります。
First off, as opposed to our previous blueprint, this one only distinguishes between online and offline.
まず、前回の設計図とは対照的に、今回の設計図ではオンラインとオフラインしか区別していません。
That being said, the “Build Approx. NN index” is close to the boundary, so almost could be considered nearline.
とはいえ、「Build Approx.NN index」は境界線に近いので、ほぼニアラインと考えてよいでしょう。
Second, this blueprint very much focuses on the latest trend of neural network and embedding-based recommender systems, particularly on the retrieval side of things.
第二に、この設計図は、ニューラルネットワークと埋め込みベースの推薦システムの最新トレンド、特に検索サイドに非常に重点を置いています。
While that does exclude “older” approaches, it is a fair assumption since most recommender systems nowadays have replaced the matrix factorization approaches with newer embedding based dimensionality reduction approaches.
これは「古い」アプローチを排除するものですが、最近の推薦システムのほとんどは、行列分解アプローチを新しい埋め込みベースの次元削減アプローチに置き換えているので、これは妥当な仮定です。

Finally, and very importantly, what’s with those “retrieval” components?
最後に、非常に重要なことですが、この「リトリーブ」部品は何なのでしょうか？
Why weren’t they even present in our original blueprint?
なぜ、当初の設計図にはなかったのでしょうか？
I am glad you asked.
というご質問をいただきました。
It turns out that at Netflix the catalog of items was so small that we did not have to select a subset for ranking.
Netflixでは、アイテムのカタログが非常に小さかったので、ランキングのためにサブセットを選択する必要がなかったのです。
We could literally rank the whole catalog for every member.
文字通り、すべてのメンバーについて、カタログ全体をランク付けすることができたのです。
However, in most other situations, as I quickly learned at Quora, you cannot rank all items for all users all the time.
しかし、私がQuoraですぐに学んだように、他のほとんどの状況では、すべてのユーザーに対してすべてのアイテムを常時ランク付けすることはできません。
Therefore, this two phase approach where you first select candidates using some retrieval approach, and then you rank them, is pretty much general purpose.
したがって、**まず何らかの検索アプローチで候補を選び、次にランク付けを行うというこの2段階のアプローチは、かなり汎用的なものだと言える**.

## Nvidia’s 4 stage blueprint Nvidiaの4段階の青写真

A few months later, Even and Karl from NVidia’s Merlin team published a new architectural blueprint that they acknowledge extended Eugene’s.
数カ月後、NVidiaのMerlinチームのEvenとKarlが、Eugeneのアーキテクチャを拡張したと認める新しいアーキテクチャの青写真を発表した。

Indeed, it is clear that this is an extension of the previous blueprint where they added a filtering step, and they decomposed ranking into scoring and ordering.
確かに、これは以前の設計図の延長線上にあり、フィルタリングのステップを追加し、ランキングをスコアリングと順位付けに分解したものであることは明らかです。
While I think those two changes make sense, I do think the way they are named and described is confusing, and not general purpose enough.
この2つの変更は理にかなっていると思いますが、これらの名称や説明の仕方は分かりにくく、汎用性に欠けると思います。
The key aspect to keep in mind is that both before and after the machine learning model is applied (either for scoring or ranking), many systems apply business logic or some other kind of logic for filtering or re-ranking.
留意すべき重要な点は、機械学習モデルが適用される前と後の両方（スコアリングまたはランキングのいずれか）に、多くのシステムはフィルタリングや再ランキングのためのビジネス・ロジックやその他の種類のロジックを適用するという点です。
However, filtering can also be done after scoring or even ranking.
しかし、フィルタリングはスコアリングやランキングの後にも行うことができる。
And, as mentioned, ranking or ordering is not necessarily done following some business logic.
また、前述したように、ランキングや順序付けは必ずしもビジネスロジックに従って行われるとは限らない。
For example, a multi-armed bandit approach can be used at this stage to learn the optimal exploration
例えば、この段階でマルチアームドバンディット法を用いて最適な探索を学習することができる

## Fennel.ai’s 8 stage blueprint Fennel.ai の 8 段階の設計図

Finally, my friends at Fennel.ai recently published a three posts series describing an 8-stage recommender systems architecture.
最後に、Fennel.aiの友人が、8段階の推薦システムアーキテクチャを説明する3つの記事を最近発表しました。

While this might seem simpler than the previous two, there are few things I like.
前の2つよりもシンプルに見えるかもしれませんが、私が気に入った点はいくつかあります。
First off, it is more generic than the other two, which are very much focused on neural network
まず、他の2つに比べてより一般的であり、ニューラルネットワークに非常に重点を置いています。

## My latest proposal 私の最新の提案

Given all the above, and in the context of a course on recommender systems that I recently prepared with Deepak Agarwal, I am proposing the new expanded blueprint below:
以上のことから、最近Deepak Agarwalと準備した推薦システムのコースに関連して、私は以下のように新しく拡張した青写真を提案することにしました。

I am not going to go into the details of all the components in this post, and might do so in a second part if there is enough interest, but I will point out some important aspects and differences when compared to some of the previous ones:
この記事では、すべてのコンポーネントの詳細に触れるつもりはありませんし、十分な関心があれば後編で触れるかもしれませんが、いくつかの重要な側面と、以前のものと比較した場合の違いを指摘します。

1. This blueprint highlights the central role of data, and the feedback loop in recommender systems この青写真は、データの中心的な役割と、レコメンダーシステムにおけるフィードバックループを強調するものです。

2. It includes two potential ML models: one for retrieval (e.g. embeddings) and the other one for scoring or ranking. 1つは検索用（例えば埋め込み），もう1つはスコアリングやランキング用のMLモデルの候補が含まれています．

3. It does not prescribe components having to be offline, online, or nearline but rather introduces the notion that some components are more likely to be online while others are more likely to be offline. This is important given the trend of more and more components transitioning to being more online in modern recommender systems. これは、構成要素がオフライン、オンライン、ニアラインであることを規定するのではなく、ある構成要素はオンラインである可能性が高く、他の構成要素はオフラインである可能性が高いという概念を導入しています。 これは、最近の推薦システムにおいて、より多くのコンポーネントがオンラインに移行している傾向を考えると重要である。

4. It includes several components that are optional (dashed lines). Those include even candidate selection. While that component is extremely important in services with large catalogs it is not necessary in others like Netflix. オプションのコンポーネントがいくつか含まれています（破線）。 それらには、候補の選択までが含まれます。 このコンポーネントは、大規模なカタログを持つサービスでは非常に重要ですが、Netflixのような他のサービスでは必要ありません。

5. Among those optional components, there are two post-processing/filtering components both after scoring and after ranking. To be clear, scoring and ranking are not necessarily two separate components since an ML model can be optimized directly for ranking, and that is why scoring is also optional. But it is important to note that post-processing and/or filtering can be introduced at almost any step (e.g. it could also be included after candidate generation). それらのオプションコンポーネントのうち、2つの後処理

Let me know what you think about this new proposal and whether you would be interested in a more detailed follow up.
この新しい提案についてどう思われるか、また、より詳細なフォローアップにご興味があるかどうかをお聞かせください。
