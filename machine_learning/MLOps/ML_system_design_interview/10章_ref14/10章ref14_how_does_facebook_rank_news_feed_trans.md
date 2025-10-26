refs: https://liuzhenglaichn.gitbook.io/system-design/news-feed/how-does-facebook-rank-news-feed



# How does facebook rank news feed? Facebookはニュースフィードをどのようにランク付けするのか？

## Key moments of Facebook Algorithm Facebookアルゴリズムの重要な瞬間



## EdgeRank

Stopped since 2011, replaced by Machine Learning with 100K factors.
2011年以降は停止され、100Kのfactor(=特徴量?)を持つ機械学習に置き換えられました。
https://mashable.com/2013/05/07/facebook-edgerank-infographic/

## How the New Facebook Algorithm Works 新しいFacebookアルゴリズムの仕組み

The new Facebook algorithm works by ranking all available posts that can display on a user’s News Feed based on how likely that user will have a positive reaction.
新しいFacebookアルゴリズムは、**ユーザーがポジティブな反応を示す可能性に基づいて、ユーザーのニュースフィードに表示できるすべての投稿をランク付けすること**によって機能します。

Facebook’s algorithm for ranking and displaying content on your News Feed is based on four factors:
Facebookのニュースフィード上のコンテンツをランク付けし表示するためのアルゴリズムは、4つの要因に基づいています。

1. The Inventory of all posts available to display.
   1. 表示可能なすべての投稿のインベントリ。(=つまり候補アイテムプール...!:thinking:)
2. Signals that tell Facebook what each post is.
   1. 各投稿が何であるかをFacebookに伝える信号。(=つまり特徴量...!:thinking:)
3. Predictions on how you will react to each post.
   1. 各投稿に対するあなたの反応を予測すること。(=つまりモデルの推論...!:thinking:)
4. A Final Score assigned to the content based on all factors considered.
   1. 考慮されたすべての要因に基づいてコンテンツに割り当てられる最終スコア。(=つまりモデルが出力するスコア...!:thinking:)

The process is based on the Vickrey-Clarke-Groves algorithm, which “operates as a closed auction,” in which advertisers’ bids are kept hidden from one another, prompting them to bid their real value.
このプロセスは、[Vickrey-Clarke-Grovesアルゴリズム](https://en.wikipedia.org/wiki/Vickrey%E2%80%93Clarke%E2%80%93Groves_auction)に基づいており、「閉じたオークション」として機能します。このオークションでは、広告主の入札が互いに隠されており、彼らが実際の価値を入札するよう促されます。

- VCG(Vickrey-Clarke-Groves)アルゴリズムのメモ:
  - 経済学におけるオークションメカニズムの一つ。
    - 参加者が自分の真の価値を正直に報告することを促す。
    - ざっくり「みんなが正直に言ったほうが全体として最適(=皆の価値の合計が最大)になるよね」という考え方に基づく。
      - perplexityが言うには「「複数エージェント（＝広告主や投稿者）」の**社会的効用（utility sum）**を最大化するためのアルゴリズム」らしい。
  - このVCGが、ニュースフィードの投稿ランク付けとどう関係するの??
    - ニュースフィードの投稿ランク付けは「ユーザーにとっての価値」を競わせる“オークション的”構造になってる。
  - (VCGがまだ良くわかってないが、**たぶん各投稿のpoint-wiseなスコア達を出した後で、それらを組み合わせてlist-wiseなランキングを作る時にVCGアルゴリズムが使われてるっぽい??**:thinking:)
    - たぶん読み手だけじゃなくて、全ての投稿者 (=広告主) の効用の総和を最大化するようにランク付けを行う、みたいな...!:thinking:

## The New Facebook Algorithm 新しいFacebookアルゴリズム

The new Facebook algorithm works by prioritizing content posted from friends over publishers, with a focus on “meaningful interactions.”  
新しいFacebookアルゴリズムは、出版社よりも友人から投稿されたコンテンツを優先し、「意味のある相互作用」に焦点を当てて機能します。

Since the data controversy erupted around the social network in late 2017, Facebook has worked to improve transparency around how it ranks content on the News Feed.  
2017年末にソーシャルネットワークを巡るデータの論争が勃発して以来、**Facebookはニュースフィード上でコンテンツをどのようにランク付けするかについての透明性を向上**させるために取り組んできました。(=つまりアルゴリズムの説明責任を果たすために頑張ってる、みたいな意味合い??:thinking:)

![]()

Between Facebook’s F8 conferences, News Feed webinars, and algorithm presentations— we can now say that Facebook’s new algorithm is no longer a complete black box.  
FacebookのF8カンファレンス、ニュースフィードウェビナー、アルゴリズムプレゼンテーションの間に、私たちは**今やFacebookの新しいアルゴリズムがもはや完全なブラックボックスではない**と言えるようになりました。

Facebook went public with changes to the algorithm in their post “Meaningful Interactions” update back in January 2018.  
Facebookは2018年1月に「意味のある相互作用」という投稿でアルゴリズムの変更を公表しました。

<!-- ここまで読んだ!-->

## The 4 Facebook Algorithm Factors 4つのFacebookアルゴリズム要因

The goal of Facebook’s algorithm is to “show stories that matter to users,” according to Adam Mosseri, VP of Facebook’s News Feed Management. 
Facebookのアルゴリズムの目的は「**ユーザーにとって重要なストーリーを表示すること**」であると、Facebookのニュースフィード管理のVPであるアダム・モッセリは述べています。
With that in mind, you should know how Facebook’s different algorithm factors work together to determine which stories “matter” to a user.
そのことを念頭に置いて、Facebookの異なるアルゴリズム要因がどのように連携して、ユーザーにとって「重要な」ストーリーを決定するかを理解する必要があります。

<!-- ここまで読んだ!-->

### Inventory 在庫

Inventory represents the stock of all content that can display to a user on Facebook’s News Feed. 
在庫は、Facebookのニュースフィードにユーザーに表示できるすべてのコンテンツのストックを表します。
This includes everything posted from friends and publishers. 
これには、**友人や出版社から投稿されたすべてのもの**が含まれます。

### Signals 信号

Signals represent the information that Facebook can gather about a piece of content. 
信号は、Facebookがコンテンツの情報を収集できることを表します。

Signals are the single factor that advertisers have control over. 
**信号は、広告主が制御できる唯一の要素**です。(ん？？:thinking:)
These are your inputs that Facebook interprets; type of content, the publisher, its age, purpose, and more. 
これらは、Facebookが解釈するあなたの入力です。コンテンツの種類、発行者、その年齢、目的などです。(=あ〜やっぱりアイテム側の特徴量のことか...!:thinking:)

You want your content to signal to Facebook that it’s meaningful and relevant to your target audience. 
あなたは、あなたのコンテンツがFacebookに対して、ターゲットオーディエンスにとって意味があり関連性があることを示すことを望んでいます。

<!-- ここまで読んだ!-->

### Predictions 予測

Predictions represent the behavior of a user and how likely they are predicted to have a positive interaction with a content piece.
予測は、ユーザの行動と、コンテンツに対してポジティブなインタラクションを持つ可能性がどれくらいあるかを表します。

### Score スコア

Score is the final number assigned to a piece of content based on the likelihood the user will respond positively to it.
スコアは、ユーザーがそのコンテンツに対して肯定的に反応する可能性に基づいて、コンテンツに割り当てられる最終的な数値です。

<!-- ここまで読んだ!-->

### Meaningful Interactions Are Valued Most 意義のあるインタラクションが最も重視される

(ん? 前述のシグナルはアイテム特徴量の話だと思ったけど、ここではimplicit/explicitなユーザFBっぽい話になってる...?:thinking:)

As advertisers, the only part of the process that we have control over are the signals of our content. 
広告主として、私たちがプロセスの中で制御できる唯一の部分は、私たちのコンテンツのシグナルです。

These signals can be divided into two categories: passive and active. 
これらのシグナルは、受動的シグナルと能動的シグナルの2つのカテゴリに分けることができます。

Passive signals include view time, story type, time posted, and other metrics non-active metrics. 
受動的シグナルには、視聴時間、ストーリーの種類、投稿時間、その他の非能動的な指標が含まれます。

Active signals include likes, shares, comments, and other active events that prompt engagement. 
能動的シグナルには、いいね、シェア、コメント、そしてエンゲージメントを促すその他の能動的なイベントが含まれます。

You should tailor your content to promote positive engagement, or what Facebook has defined as “meaningful interactions.” 
あなたは、ポジティブなエンゲージメント、つまりFacebookが「意義のあるインタラクション」と定義しているものを促進するようにコンテンツを調整すべきです。

<!-- ここまで読んだ!-->

### Why Should Advertisers Care? なぜ広告主は気にするべきか？

- 4.75 billion pieces of content shares – daily
  - 4.75億件のコンテンツシェア - 毎日
- 300+ million photo uploads – daily
  - 3億件以上の写真アップロード - 毎日
- 510,000 comments – every 60 seconds
  - 51万件のコメント - 60秒ごと
- 293,000 statuses – every 60 seconds
  - 29万3千件のステータス - 60秒ごと

## Reference 参考文献

1. https://tinuiti.com/blog/paid-social/facebook-algorithm/
2. https://blog.hootsuite.com/facebook-algorithm/
https://tinuiti.com/blog/paid-social/facebook-algorithm/
https://blog.hootsuite.com/facebook-algorithm/

<!-- ここまで読んだ!-->
