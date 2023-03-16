## 0.1. link リンク

- https://www.jmlr.org/papers/volume6/shani05a/shani05a.pdf https

## 0.2. title タイトルです。

An MDP-Based Recommender System.
MDPに基づく推薦システム.

## 0.3. abstract abstract.

Typical recommender systems adopt a static view of the recommendation process and treat it as a prediction problem.
一般的なレコメンダーシステムは、**推薦プロセスを静的な視点で捉え**、予測問題として扱っている.
We argue that it is more appropriate to view the problem of generating recommendations as a sequential optimization problem and, consequently, that Markov decision processes (MDPs) provide a more appropriate model for recommender systems.
我々は、推**薦を生成する問題を逐次最適化問題として捉えることがより適切**であり、その結果、マルコフ決定過程（MDP）が推薦システムのモデルとしてより適切であることを主張する.
MDPs introduce two benefits: they take into account the long-term effects of each recommendation and the expected value of each recommendation.
MDPは、各推薦の長期的な効果と各推薦の期待値を考慮するという2つの利点を導入している.
To succeed in practice, an MDP-based recommender system must employ a strong initial model, must be solvable quickly, and should not consume too much memory.
MDPベースの推薦システムが実際に成功するためには、強力な初期モデルを採用し、素早く解けること、そしてメモリをあまり消費しないことが必要.
In this paper, we describe our particular MDP model, its initialization using a predictive model, the solution and update algorithm, and its actual performance on a commercial site.
本論文では、私たちがこだわったMDPモデルについて、予測モデルを用いた初期化、解と更新のアルゴリズム、商用サイトでの実際の性能について説明する.
We also describe the particular predictive model we used which outperforms previous models.
また、私たちが使用した、従来のモデルを凌駕する特定の予測モデルについて説明する.
Our system is one of a small number of commercially deployed recommender systems.
私たちのシステムは、商業的に展開されている数少ないレコメンダーシステムの一つ.
As far as we know, it is the first to report experimental analysis conducted on a real commercial site.
実際の商用サイトで行われた実験的な分析結果を報告したのは、知る限り初めて.
These results validate the commercial value of recommender systems, and in particular, of our MDP-based approach.
これらの結果は、レコメンダーシステム、特にMDPベースのアプローチの商業的価値を検証するもの.
Keywords: recommender systems, Markov decision processes, learning, commercial applications..
キーワード：レコメンダーシステム、マルコフ決定過程、学習、商業応用.

# 1. Introduction

In many markets, consumers are faced with a wealth of products and information from which they can choose.
多くの市場において、消費者は豊富な商品と情報を前にして、その中から選択することができる.
To alleviate this problem, many web sites attempt to help users by incorporating a recommender system (Resnick and Varian, 1997) that provides users with a list of items and/or webpages that are likely to interest them.
この問題を軽減するために、多くのWebサイトでは、ユーザーにアイテムのリストを提供するレコメンダーシステム（Resnick and Varian, 1997）を組み込んで、ユーザーを支援しようと試みている.
Once the user makes her choice, a new list of recommended items is presented.
ユーザが選択すると、新しいおすすめアイテムのリストが表示される.
Thus, the recommendation process is a sequential process.
このように、**推薦プロセスは逐次的なプロセスである**.
Moreover, in many domains, user choices are sequential in nature – for example, we buy a book by the author of a recent book we liked..
さらに、多くのドメインでは、**ユーザの選択は、例えば、最近気に入った本の著者の本を買うというように、連続的な性質を持っている**.

The sequential nature of the recommendation process was noticed in the past (Zimdars et al., 2001).
推薦プロセスの逐次性は過去にも注目されていた（Zimdars et al, 2001）.
Taking this idea one step farther, we suggest that recommendation is not simply a sequential prediction problem, but rather, a sequential decision problem.
この考えを一歩進めて、**推薦とは単なる逐次予測問題(sequential prediction problem)ではなく、逐次決定問題(sequential decision problem)である**ことを提案する.
At each point the Recommender System makes a decision: which recommendation to issue.
各ポイントで、推薦システムは、どの推薦を発行するかという決定を下す.
This decision should take into account the sequential process involved and the optimization criteria suitable for the recommender system, such as the profit generated from selling an item.
この決定には、関連する順序的なプロセスや、アイテムを販売することで得られる利益など、推薦システムに適した最適化基準を考慮する必要がある.
Thus, we suggest the use of Markov decision processes (MDP) (Puterman, 1994), a well known stochastic model of sequential decisions..
そこで、**逐次決定の確率モデルとしてよく知られているマルコフ決定過程（MDP）**（Puterman, 1994）の利用を提案する.

With this view in mind, a more sophisticated approach to recommender systems emerges.
このような考えから、より洗練されたレコメンダーシステムの考え方が生まれている.
First, one can take into account the utility of a particular recommendation – for example, we might want to recommend a product that has a slightly lower probability of being bought, but generates higher profits.
例えば、**購入される確率は少し低いが、より高い利益を生み出す商品を薦めるなど、特定の推薦アイテムの効用を考慮することができる**.
Second, we might suggest an item whose immediate reward is lower, but leads to more likely or more profitable rewards in the future..
次に、「**目先の報酬は低いが、将来、より可能性の高い、あるいはより有益な報酬につながる**アイテム」を提案することがある.(=まさに短期的なクリックではなく、長期的なユーザ体験の改善みたいな...?)

These considerations are taken into account automatically by any good or optimal policy generated for an MDP model of the recommendation process.
これらの考慮は、推薦プロセスのMDPモデルに対して生成される、優れたまたは最適なポリシーによって自動的に考慮される.
In particular, an optimal policy will take into account the likelihood of a recommendation to be accepted by the user, the immediate value to the site of such an acceptance, and the long-term implications of this on the user’s future choices.
特に、**最適なポリシーは、推薦がユーザに受け入れられる可能性、そのような受け入れがサイトにもたらす直接的な価値、そしてそれがユーザの将来の選択に与える長期的な影響を考慮したもの**である.
These considerations are taken with the appropriate balance to ensure the generation of the maximal expected reward stream..
これらの考慮(複数の価値?)を適切なバランスで行うことで、最大限の期待報酬を生み出すことができる.

For instance, consider a site selling electronic appliances faced with the option to suggest a video camera with a success probability of 0.5, or a VCR with a probability of 0.6.
例えば、家電製品の販売サイトで、成功確率0.5のビデオカメラを提案するか、0.6の確率でビデオデッキを提案するかの選択を迫られたとする.
The site may choose the camera, which is less profitable, because the camera has accessories that are likely to be purchased, whereas the VCR does not.
カメラには購入される可能性の高い付属品があるが、ビデオデッキにはないため、サイト側は利益の少ないカメラを選択する可能性がある.
If a video-game console is another option with a smaller success probability, the large profit from the likely future event of selling game cartridges may tip the balance toward this latter choice.
ゲーム機が成功確率の低いもう一つの選択肢であれば、将来起こりうるゲームカートリッジの販売で得られる大きな利益によって、後者の選択肢にバランスが傾くかもしれない.
Similarly, when the products sold are books, by recommending a book for which there is a sequel, we may increase the likelihood that this sequel will be purchased later..
同様に、販売する商品が書籍の場合、続編がある本を勧めることで、その続編を後から購入する可能性を高めることができるかもしれない.

Indeed, in our implemented system, we observed less obvious instances of such sequential behavior: users who purchased novels by the well-known science fiction author, Roger Zelazny, who uses many mythological themes in his writing, often later purchase books on Greek or Hindu mythology.
神話を題材にしたSF作家として知られるロジャー・ゼラズニーの小説を購入したユーザが、その後、ギリシャ神話やヒンドゥー神話に関する本を購入することが多いなど、あまり目立たない例ですが、このような連続的な行動を観察することができた.
On the other hand, users who buy mythology books do not appear to buy Roger Zelazny novels afterwards..
一方、神話の本を買うユーザは、その後、ロジャー・ゼラズニーの小説を買うことはないようだ.

The benefits of an MDP-based recommender system discussed above are offset by the fact that the model parameters are unknown.
上述したMDPベースの推薦システムの利点は、**モデルのパラメータが未知であるという事実**(=最適なpolicyを見つけるのがめちゃめちゃ大変って話?)によって相殺されている.
Standard reinforcement learning techniques that learn optimal behaviors will not do – they take considerable time to converge and their initial behavior is random.
最適な振る舞いを学習する一般的な強化学習では、収束にかなりの時間を要し、初期動作もランダムになってしまうからである.
No commercial site will deploy a system with such behavior.
商業サイトでは、このような動作をするシステムを導入することはない.
Thus, we must find ways for generating good initial estimates for the MDP parameters.
そのため、MDPパラメータの初期推定値をうまく生成する方法を見つけなければならない.
The approach we suggest initializes a predictive model of user behavior using data gathered on the site prior to the implementation of the recommender system.
私たちが提案するアプローチは、推薦システムを導入する前に、サイトで収集したデータを使って、ユーザの行動予測モデルを初期化する.
We then use the predictive model to provide initial parameters for the MDP..
そして、**予測モデルを用いて、MDPの初期パラメータを提供する**.

Our initialization process can be performed using any predictive model.
**私たちの初期化処理は、任意の予測モデルを用いて行うことができる**.
In this paper we suggest a particular model that outperforms previous approaches.
本論文では、これまでのアプローチを凌駕する特定のモデルを提案する.
The predictive model we describe is motivated by our sequential view of the recommendation process, but constitutes an independent contribution.
この予測モデルは、レコメンデーションプロセスの逐次的な見方によって動機づけられたものですが、独立した貢献となる.
The model can be thought of as an n-gram model (Chen and Goodman, 1996) or, equivalently, a (first-order) Markov chain in which states correspond to sequences of events.
このモデルは、n-gramモデル（Chen and Goodman, 1996）、あるいは、状態がイベントのシーケンスに対応する（一次）マルコフ連鎖と考えることができる.
In this paper, we emphasize the latter interpretation due to its natural relationship with an MDP.
本論文では、MDPとの自然な関係から、後者の解釈を重視する.
We note that Su et al.(2000) have described the use of simple n-gram models for predicting web pages.
なお、Su et al.(2000) は、ウェブページを予測するための単純なn-gramモデルの使用について述べている.
Their methods, however, yield poor performance on our data, probably because in our case, due to the relatively limited data set, the use of the enhancement techniques discussed below is needed..
しかし、これらの方法は、私たちのデータでは性能が低く、おそらく、私たちの場合、データセットが比較的限られているため、以下に述べるエンハンスメント技術を使用する必要があるためだと思われる.

Validating recommender system algorithms is not simple.
レコメンダーシステムのアルゴリズムの検証は簡単ではない.
Most recommender systems, such as dependency networks (Heckerman et al., 2000), are tested on historical data for their predictive accuracy.
依存関係ネットワーク（Heckerman et al., 2000）のようなほとんどのレコメンダーシステムは、**その予測精度を過去のデータでテストしている.**
That is, the system is trained using historical data from sites that do not provide recommendations, and tested to see whether the recommendations conform to actual user behavior.
つまり、**レコメンドを行わないサイトの履歴データを使ってシステムを学習させ、レコメンドが実際のユーザの行動に合致しているかどうかをテストする**のである.
We present the results of a similar test with our system showing it to perform better than the previous leading approach..
本システムで同様のテストを行った結果、従来の主要なアプローチよりも優れた性能を発揮することがわかった.

However, predictive accuracy is not an ideal measure, as it does not test how user behavior is influenced by the system’s suggestions or what percentage of recommendations are accepted by users.
しかし、**予測精度は、推薦システムの提案によってユーザの行動がどのように影響されるのか、また、推奨の何パーセントがユーザに受け入れられるのかを検証するものではないので、理想的な指標とは言えない**.
To obtain this data, one must employ the system at a real site with real users, and compare the performance of this site with and without the system (or with this and other systems).
このデータ(=理想的な指標の為のデータ)を得るためには、実際のユーザがいるサイトでシステムを採用し、そのサイトのパフォーマンスを、システムを使った場合と使わない場合（あるいは、このシステムと他のシステムを使った場合）で比較する必要がある.
The extent to which such experiments are possible is limited, as commercial site owners are unlikely to allow experiments which can degrade the performance or the “look-and-feel” of their systems.
商用サイトの所有者は、システムのパフォーマンスや「ルック＆フィール」を低下させるような実験を許可しにくいため、このような実験が可能な範囲は限定的である.
However, we were able to perform a certain set of experiments using our commercial system at the online bookstore Mitos (www.mitos.co.il) by running two models simultaneously on different users: one based on a predictive model and one based on an MDP model.
しかし、オンライン書店ミトス（www.mitos.co.il）では、当社の商用システムを用いて、異なるユーザに対して予測モデルに基づくモデルとMDPモデルに基づくモデルの2つを同時に実行することで、一定の実験を行うことができた.
We were also able, for a short period, to compare user behavior with and without recommendations.
また、短期間ではありますが、レコメンデーションの有無によるユーザー行動の比較も行うことができた.
These results, which to the best of our knowledge are among the first reports of online performance in a commercial site, are reported in Section 6, providing very encouraging validation to recommender systems in general, and to our sequential optimization approach in particular..
これらの結果は、**私たちの知る限り、商業サイトにおけるオンラインパフォーマンスの最初の報告の一つ**であり、一般的な推薦システム、特に私たちの逐次最適化アプローチに非常に有望な検証を提供するものであることを第6節で報告する.

The main contributions of this paper are:
本論文の主な貢献は以下の通りである.

- (1) A novel approach to recommender systems based on an MDP model together with appropriate initialization and solution techniques.
- (1) MDPモデルと適切な初期化・解法に基づく推薦システムに対する新しいアプローチ.
- (2) A novel predictive model that outperforms previous predictive models.
- (2) 従来の予測モデルを凌駕する新規予測モデル.
- (3) One of a small number of commercial applications based on MDPs.
- (3) MDPに基づく少数の商用アプリケーションの1つ.
- (4) The first (to the best of our knowledge) experimental analysis of a commercially deployed recommender system..
- (4) **商業的に展開されているレコメンダーシステムの実験的分析を行ったのは（我々の知る限り）初めて**である.

We note that the use of MDPs for recommender systems was previously suggested by Bohnenberger and Jameson (2001).
なお、推薦システムにMDPを用いることは、Bohnenberger and Jameson (2001)が以前に提案している.
They used an MDP to model the process of a consumer navigating within an airport.
彼らはMDPを使って、消費者が空港内を移動するプロセスをモデル化した.
The state of this MDP was the consumer’s position and rewards were obtained when the consumer entered a store or bought an item.
このMDPの状態(state)は消費者の位置であり、消費者が店に入ったり商品を購入したりすると報酬が得られる.
Recommendations were issued on a palm-top, suggesting routes and stores to visit.
パームトップには、ルートやお店を提案するレコメンドが書かれていた.
However, the MDP model was hand-coded and experiments were conducted with students rather than real users..
しかし、MDPモデルは手作業でコーディングされ、実験も実際のユーザではなく、学生を対象に行われた.

The paper is structured as follows.
本稿は以下のような構成になっている.
In Section 2 we review the necessary background on recommender systems, MDPs, and reinforcement learning.
第2節では、レコメンダーシステム、MDP、強化学習について必要な背景を概説する.
In Section 3 we describe the predictive model we constructed whose goal is to accurately predict user behavior in an environment without recommendations.
セクション3では、**推薦のない環境におけるユーザの行動を正確に予測することを目的として構築した予測モデル**について説明する.(この予測モデルをRLの初期値に用いる)
In Section 4 we present our empirical evaluation of the predictive model.
セクション4では、予測モデルの実証評価を紹介する.
In Section 5 we explain how we use this predictive model as a basis for a more sophisticated MDP-based model for the recommender system.
セクション5では、この予測モデルを、より洗練された推薦システムのMDPベースのモデルの基礎として使用する方法を説明する.
In Section 6 we provide an empirical evaluation of the actual recommender system based on data gathered from our deployed system.
第6節では、実際に導入したシステムから収集したデータに基づき、実際のレコメンダーシステムの実証評価を行う.
We conclude the paper in Section 7 discussing our current and future work..
最後に、第7節で、現在と将来の仕事について述べる.

# 2. Background バックグラウンド

In this section we provide the necessary background on recommender systems, N-gram models, and MDPs..
ここでは、レコメンダーシステム、N-gramモデル、MDPについて必要な背景を説明する.

## 2.1. Recommender Systems Recommender Systems.

Early in the 1990s, when the Internet became widely used as a source of information, information explosion became an issue that needed addressing.
インターネットが情報源として広く普及した1990年代初頭、情報爆発が問題視されるようになった.
Many web sites presenting a wide variety of content (such as articles, news stories, or items to purchase) discovered that users had difficulties finding the items that interested them out of the total selection.
多くのWebサイトでは、記事、ニュース、商品など様々なコンテンツが用意されており、その中から自分の興味のあるものを探し出すことが困難であることがわかった.
Recommender Systems (Resnick and Varian, 1997) help users limit their search by supplying a list of items that might interest a specific user.
リコメンダーシステム（Resnick and Varian, 1997）は、特定のユーザーが興味を持ちそうなアイテムのリストを提供することで、ユーザーが検索を制限することを支援する.
Different approaches were suggested for supplying meaningful recommendations to users and some were implemented in modern sites (Schafer et al., 2001).
ユーザに意味のあるレコメンデーションを提供するために様々なアプローチが提案され、いくつかは現代のサイトに実装されている（Schafer et al, 2001）.
Traditional data mining techniques such as association rules were tried at the early stages of the development of recommender systems.
レコメンダーシステムの開発初期には、アソシエーションルールのような**伝統的なデータマイニング技術が試みられた**.
Initially, they proved to be insufficient for the task, but more recent attempts have yielded some successful systems (Kitts et al., 2000)..
当初、これらのシステムはタスクに対して不十分であることが証明されたが、より最近の試みにより、いくつかの成功したシステムが得られた（Kitts et al.、2000）.

Approaches originating from the field of information retrieval (IR) rely on the content of the items (such as description, category, title, author) and therefore are known as content-based recommendations (Mooney and Roy, 2000).
**情報検索（IR）の分野から生まれたアプローチ**は、アイテムの内容（説明、カテゴリー、タイトル、著者など）に依存するため、**コンテンツベースの推薦**として知られている（Mooney and Roy, 2000）.
These methods use some similarity score to match items based on their content.
これらの方法は、何らかの類似性スコアを用いて、その内容に基づいてアイテムをマッチングさせる.
Based on this score, a list of items similar to the ones the user previously selected can be supplied.
このスコアに基づいて、ユーザが以前に選択したものと類似したアイテムのリストを提供することができる.
Knowledge-based recommender systems (Burke, 2000) go one step farther by using deeper knowledge about the user and the domain.
**知識ベース(Knowledge-based )推薦システム**（Burke, 2000）は、ユーザやドメインに関するより深い知識を利用することで、さらに一歩進んだシステムである.
In particular, the user is able to introduce explicit information about her preferences.
特に、ユーザが自分の好みに関する情報を明示的に導入することができるのが特徴.
Thus, for instance, the user could specify interest in Thai cuisine, and the system might suggest a restaurant serving some other south-Asian cuisine..
例えば、ユーザがタイ料理に興味があることを伝えると、システムは他の南アジア料理のレストランを提案することができる. (=なるほど...! knowledge-basedの推薦システムは、推薦と検索の間に位置するようなアプローチっぽい...!)

Another possibility is to avoid using information about the content, but rather use historical data gathered from other users in order to make a recommendation.
また、**コンテンツに関する情報を使わず、他のユーザから集めた過去のデータを使って推薦**することも考えられる.
These methods are widely known as collaborative filtering (CF) (Resnick et al., 1994), and we discuss them in more depth below.
これらの手法は協調フィルタリング（CF）（Resnick et al, 1994）として広く知られており、以下、より深く議論する.
Finally, some systems try to create hybrid models that combine collaborative filtering and content-based recommendations (Balabanovic and Shoham, 1997; Burke, 2002)..
最後に、協調フィルタリングとコンテンツベースの推薦を組み合わせたハイブリッドモデルを作ろうとするシステムもある（Balabanovic and Shoham, 1997; Burke, 2002）.

## 2.2. Collaborative Filtering Collaborative Filtering（コラボレイティブ・フィルタリング）。

The collaborative filtering approach originates in human behavior: people searching for an interesting item they know little of, such as a movie to rent at the video store, tend to rely on friends to recommend items they tried and liked.
例えば、**ビデオ屋さんで借りる映画など、自分があまり知らない面白いものを探している人は、自分が試してみて気に入ったものを友達に勧める傾向がある**.
The person asking for advice is using a (small) community of friends that know her taste and can therefore make good predictions as to whether she will like a certain item.
アドバイスを求める人は、自分の好みを知っている友人たちの（小さな）コミュニティを使っているので、あるアイテムを気に入るかどうか、うまく予測することができます。
Over the net however, a larger community that can recommend items to our user is available, but the persons in this large community know little or nothing about each other.
しかし、ネット上では、ユーザに対してアイテムを推薦してくれる大きなコミュニティが用意されていますが、この大きなコミュニティの中の人たちは、お互いのことをほとんど知らないのである.
Conceptually, the goal of a collaborative filtering engine is to identify those users whose taste in items is predictive of the taste of a certain person (usually called a neighborhood), and use their recommendations to construct a list of items interesting for her..
協調フィルタリングエンジンの目的は、ある人（通常、neighborhoodと呼ばれる）の好みを予測できるようなアイテムを持つユーザを特定し、そのユーザの推薦をもとに、その人にとって興味深いアイテムのリストを作成することである、という概念.

To build a user’s neighborhood, these methods rely on a database of past users interactions with the system.
ユーザの周辺環境を構築するために、これらの方法は、過去のユーザとシステムとのインタラクションのデータベースに依存している.
Early systems used explicit ratings.
初期のシステムでは、明示的なレーティングが使われていた.
In such systems, users grade items (e.g., 5 stars to a great movie, 1 star to a horrible one) and then receive recommendations.1 Later systems shifted toward implicit ratings.
このようなシステムでは、ユーザはアイテムに点数を付け（例えば、素晴らしい映画には5つ星、ひどい映画には1つ星）、推薦を受けることができる. その後、システムは implicit rating にシフトしました.
A common approach assumes that people like what they buy.
一般的なアプローチでは、人々は自分が買ったものが好きだと仮定する.
A binary grading method is used when a value of 1 is given to items the user has bought and 0 to other items.
ユーザが購入したアイテムに1を、それ以外のアイテムに0を付与する場合、二値採点方式が採用される.
Many modern recommender systems successfully implement this approach.
最近のレコメンダーシステムの多くは、このアプローチの実装に成功している.
Claypool et al.(2001) have suggested the use of other implicit grading methods through a special web browser that keeps track of user behavior such as the time spent looking at the web page, the scrolling of the page by the user, and movements of the mouse over the page.
Claypoolら(2001)は、ウェブページを見ている時間、ユーザによるページのスクロール、ページ上でのマウスの動きなどのユーザの行動を記録する特別なウェブブラウザを通して、他のimplicitな採点方法を使用することを提案している.
Their evaluation, however, failed to establish a method of rating that gave results consistently better than the binary method mentioned above..
しかし、彼らの評価では、上記の2値法よりも安定した結果を得られる評価方法を確立することはできなかった.

As described in Breese et al.(1998), collaborative filtering systems are either memory based or model based.
Breeseらに記載されているように(1998)、協調フィルタリングシステムには、メモリベースとモデルベースの2種類があるとしている.
Memory-based systems work directly with user data.
メモリベースのシステムは、ユーザのデータを直接扱う.
Given the selections of a given user, a memory-based system identifies similar users and makes recommendations based on the items selected by these users.
あるユーザの選択したアイテムがあれば、記憶に基づいて類似のユーザを特定し、そのユーザが選択したアイテムに基づいて推薦を行うものである.
Model-based systems compress such user data into a predictive model.
モデルベースシステムは、このようなユーザデータを圧縮して予測モデルにする.
Examples of model-based collaborative filtering systems are Bayesian networks (Breese et al., 1998) and dependency networks (Heckerman et al., 2000).
モデルベースの協調フィルタリングシステムの例としては、ベイジアンネットワーク（Breese et al., 1998）や依存性ネットワーク（Heckerman et al., 2000）がある.
In this paper, we consider modelbased systems..
本論文では、モデルベースシステムを検討する.

## 2.3. The Sequential Nature of the Recommendation Process レコメンデーションプロセスの逐次性

Most recommender systems work in a sequential manner: they suggest items to the user who can then accept one of the recommendations.
ほとんどのレコメンダーシステムは、ユーザにアイテムを提案し、ユーザはその中から1つを選択する、という順序で動作する.
At the next stage a new list of recommended items is calculated and presented to the user.
次のステージでは、新しいおすすめアイテムのリストが計算され、ユーザに提示される.
This sequential nature of the recommendation process, where at each stage a new list is calculated based on the user’s past ratings, will lead us naturally to our reformulation of the recommendation process as a sequential optimization process..
このように、**ユーザの過去の評価をもとに、各段階で新しいリストを算出するという推薦プロセスの逐次性**は、推薦プロセスを逐次最適化プロセスとして再定義することに自然につながっていくだろう.

There is yet another sequential aspect to the recommendation process.
推薦のプロセスには、**さらにもう一つの逐次性がある.**
Namely, optimal recommendations may depend not only on previous items pruchased, but also on the order in which those items are purchased.
すなわち、**最適なレコメンデーションは、過去に購入したアイテムだけでなく、それらのアイテムを購入した順番にも依存する**可能性がある.
Zimdars et al.(2001) recognized this possible dependency and suggested the use of an auto-regressive model (a k-order Markov chain) to represent it.
Zimdars et al.(2001)は、この可能性のある依存関係を認識し、自己回帰モデル（k次マルコフ連鎖）を使って表現することを提案した.
They divided a sequence of transactions X1,...,XT (for example, product purchases, web-page views) into cases (Xt−k,...,Xt−1,Xt) for t = 1,...,T as shown in Table 1.
彼らは、一連のトランザクション$X_1,...,X_T$（例えば、商品購入やウェブページ閲覧）を、表1のように$t＝1,...,T$のケース$(X_{t-k},...,X_{t-1}, X_t)$ に分割している.
They then built a model (in particular, a dependency network) to predict the last column given the other columns, under the assumption that the cases were exchangeable.
そして、事例が交換可能であるという仮定のもと、**他の列から最後の列を予測するモデル**(特に依存関係ネットワーク)を構築したのである.
Our model will also incorporate this sequential view..
私たちのモデルは、この逐次表示も取り入れる予定.

## 2.4. N-gram Models N-gram Models（エヌグラムモデル）。

N-gram models originate in the field of language modeling.
N-gramモデルは、言語モデリングの分野で生まれたモデル.
They are used to predict the next word in a sentence given the last n − 1 words.
**直近のn - 1個の単語から、文中の次の単語を予測する**ために使用される.
In the simplest form of the model, probabilities for the next word are estimated via maximum likelihood; and many methods exist for improving this simple approach including skipping, clustering, and smoothing.
最も単純なモデルでは、次の単語の確率を最尤法で推定する. この単純なアプローチを改善するために、スキップ、クラスタリング、スムージングなど多くの方法が存在する.
Skipping assumes that the probability of the next word xi depends on words other than just the previous n − 1.
スキップは、次の単語$x_i$の確率が、前のn - 1以外の単語にも依存することを想定している.
A separate model is built using skipping and then combined with the standard n-gram model.
スキップを使って別モデルを構築し、標準的なn-gramモデルと組み合わせている.
Clustering is an approach that groups some states together for purposes of predicting next states.
クラスタリングは、次の状態を予測するために、いくつかの状態をグループ化するアプローチ.
For example, we can group items such a basketball, football, and volleyball into a “sports ball” class.
例えば、バスケットボール、サッカー、バレーボールなどのアイテムを「スポーツボール」というクラスにまとめることができる.
Such grouping helps to address the problem of data sparsity.
このようなグループ分けは、データの疎密の問題を解決するのに役立つ.
Smoothing is a general name for methods that modify the estimates of probabilities to achieve higher accuracy by adjusting zero or low probabilities upward.
**Smoothing(平滑化)**とは、確率の推定値を修正する方法の総称で、ゼロまたは低い確率を上方修正することで、より高い精度を実現するものである.(=要するに、確率分布の裾野を広くするようなイメージ?)
One type of smoothing is finite mixture modeling, which combines multiple models via a convex combination.
平滑化の一種に、複数のモデルを凸組み合わせで結合する有限混合モデリングがある.
In particular, given k component models for xi given a prior sequence X — $p_{M_1}(x_i|X),\cdots, p_{M_k}(x_i|X)$ —we can define the k-component mixture model $p(x_i|X)= \pi_{1}\cdot p_{M_1}(x_i|X) + \cdots \pi_{k} \cdot p_{M_k}(x_i|X)$, where $\sum_{i=1}^{k}\pi_{i} = 1$ are its mixture weights.
特に、事前シーケンス$X$を与えられた$x_i$の $k$ 成分モデル $p_{M_1}(x_i|X),\cdots, p_{M_k}(x_i|X)$ が与えられた場合、$k$ 成分混合モデル$p(x_i|X)= \pi_{1}\cdot p_{M_1}(x_i|X) + \cdots \pi_{k} \cdot p_{M_k}(x_i|X)$を定義できる. ここで $\sum_{i=1}^{k}\pi_{i} = 1$ はその混合重み.
Details of these and other methods are given in Chen and Goodman (1996)..
これらの方法と他の方法の詳細は、Chen and Goodman (1996)に記載されている.

## 2.5. MDPs

An MDP is a model for sequential stochastic decision problems.
MDPとは、**逐次確率的決定問題(sequential stochastic decision problems)のモデル**である.
As such, it is widely used in applications where an autonomous agent is influencing its surrounding environment through actions (for example, a navigating robot).
そのため、**自律的なエージェントが行動(action)によって周囲の環境(environment)に影響を与えるようなアプリケーション**(例えば、ナビゲーションロボットなど)に広く利用されている.
MDPs (Bellman, 1962) have been known in the literature for quite some time, but due to some fundamental problems discussed below, few commercial applications have been implemented..
MDP（Bellman、1962）は、かなり以前から文献で知られていましたが、後述するいくつかの基本的な問題のため、**商用アプリケーションはほとんど実装されていなかった**.

An MDP is by definition a four-tuple: hS,A,Rwd,tri, where S is a set of states, A is a set of actions, Rwd is a reward function that assigns a real value to each state/action pair, and tr is the state-transition function, which provides the probability of a transition between every pair of states given each action..
**MDP(マルコフ決定過程)の定義**は four-tuple(４つ組)：$\langle S, S, Rwd, tr \rangle$で、$S$ はstateの集合、Aはactionの集合、$Rwd$は各stateに実数値を割り当てる報酬関数である.
($tr$ は状態遷移関数?)

In an MDP, the decision-maker’s goal is to behave so that some function of its reward stream is maximized – typically the average reward or the sum of discounted reward.
MDPでは、意思決定者の目標は、reward stream関数(=streamってどういう意味? 短期的でimmidiateなrewardではなく、長期的なrewardって意味?)が最大になるように行動することである(通常は平均報酬、または割引報酬の合計).
An optimal solution to the MDP is such a maximizing behavior.
MDPの最適解とは、このようなmaximizing behaviorのことである.
Formally, a stationary policy for an MDP π is a mapping from states to actions, specifying which action to perform in each state.
形式的には、MDP $\pi$ の**stationary policy(定常方策?)は、stateからaction へのmapping**であり、**各stateでどのactionを実行するかを指定するもの**である.(=**stateが決まれば、常に同じactionが決定するって意味**??)
Given such an optimal policy π, at each stage of the decision process, the agent need only establish what state s it is in and execute the action a = π(s)..
このような最適な方策 $\pi$ が与えられた場合、エージェントは意思決定プロセスの各段階において、どのような state $s$ にあるかを確定し、action $a = \pi(s)$ を実行すればよい.

Various exact and approximate algorithms exist for computing an optimal policy.
最適なポリシーを計算するために、様々な厳密および近似アルゴリズムが存在する.
Below we briefly review the algorithm known as policy-iteration (Howard, 1960), which we use in our implementation.
以下では、我々の実装で使用しているpolicy-iteration (Howard, 1960)として知られるアルゴリズムについて簡単に説明する.
A basic concept in all approaches is that of the value function.
すべてのアプローチにおいて基本的な概念は、**価値関数(value function)**である.
The value function of a policy $\pi$, denoted $V^{\pi}$, assigns to each state $s$ a value which corresponds to the expected infinitehorizon discounted sum of rewards obtained when using $\pi$ starting from $s$.
方策 $\pi$ の価値関数 $V^{\pi}$ は、各state $s$ を入力に受け取り、**あるstate $s$ (initial state)から方策 $\pi$ を使用した(スタートした)**場合に得られる**報酬のexpected infinitehorizon discounted sumに相当する値** を出力するものである.

This function satisfies the following recursive equation:.
value functionは、以下の再帰的方程式を満たします:
(reward function と value functionの違い: reward functionは、agentが state $s$で action $a$ を取った時に得られる即時報酬を定義する関数.
一方で value functionは、**あるstate $s$ を initial stateとして、ある方策 $\pi$ を取った場合に得られる将来の累積報酬の期待値**を定義する.よって**価値関数は報酬関数とは異なり、agentが採用する方策に依存する.**)

$$
V^{\pi}(s) = Rwd(s, \pi(s)) + \gamma \sum_{s_j \in S} tr(s, \pi(s), s_j) V^{\pi}(s_j)
\tag{1}
$$

(右辺第一項は、initial stateにおいて方策に基づいてactionした場合のt=1の即時報酬? 右辺第二項は、t=2, ...の期待累積報酬?)

where 0 < γ < 1 is the discount factor.2 An optimal value function, denoted V ∗ , assigns to each state s its value according to an optimal policy π ∗ and satisfies.
ここで、$0 < \gamma < 1$ は割引係数である. 最適な価値関数( $V*$ とする)は、最適な方策 $\pi*$ に従って各state $s$ にその価値を割り当て、以下を満たすものである.

$$
V^{*} = \max_{a \in A}[Rwd(s, a) + \gamma \sum_{s_j \in S} tr(s, a, s_j) V^{*}(s_j)]
\tag{2}
$$

To find a π ∗ and V ∗ using the policy-iteration algorithm, we search the space of possible policies.
ポリシー反復アルゴリズムを用いて $\pi^*$ と $V^*$ を見つけるために、可能なポリシーの空間を探索する.
We start with an initial policy π0(s) = argmax a∈A Rwd(s,a).
初期方策 $\pi_{0}(s) = \argmax_{a \in A} Rwd(s,a)$ でスタートする.
At each step we compute the value function based on the former policy and update the policy given the new value function:.
各ステップでは、以前の方策に基づいて価値関数を計算し、新しい価値関数を与えてポリシーを更新する.：

$$
V_{i}(s) = Rwd(s, \pi_{i}(s)) + \gamma \sum_{s_j \in S} tr(s, \pi_{i}(s), s_j) V_i(s_j)
\tag{3}
$$

$$
\pi_{i+1}(s) = \argmax_{a \in A}[Rwd(s, a) + \gamma \sum_{s_j \in S} tr(s, a, s_j) V_{i}(s_j)]
\tag{4}
$$

These iterations will converge to an optimal policy (Howard, 1960)..
これらの繰り返しにより、最適な方策に収束する(Howard, 1960).

Solving MDPs is known to be a polynomial problem in the number of states (via a reduction to linear programming (Puterman, 1994)).
MDPの解法は、state数の多項式問題であることが知られている(線形計画法への還元により（Puterman, 1994）).
It is usually more natural to represent the problem in terms of states variables, where each state is a possible assignment to these variables and the number of states is hence exponential in the number of state variables.
通常、問題をstate変数で表現する方が自然であり、各stateはこれらの変数への可能な割り当てであり、したがってstateの数は状態変数の数の指数関数となる.
This well known “curse of dimensionality” makes algorithms based on an explicit representation of the state-space impractical.
このよく知られた"次元の呪い"によって、状態空間の明示的な表現に基づくアルゴリズムは非現実的なものとなっている.
Thus, a major research effort in the area of MDPs during the last decade has been on computing an optimal policy in a tractable manner using factored representations of the state space and other techniques (for example Boutilier et al.(2000); Koller and Parr (2000)).
そのため、この10年間、MDPの分野では、状態空間のファクタリング表現などを用いて、**扱いやすい方法で最適な方策を計算すること**が大きな研究課題となっていた（例えば、Boutilier et al.(2000); Koller and Parr (2000))。
Unfortunately, these recent methods do not seem applicable in our domain in which the structure of the state space is quite different – that is, each state can be viewed as an assignment to a very small number of variables (three in the typical case) each with very large domains.
つまり、各stateは、非常に大きな領域を持つ非常に少数の変数（典型的なケースでは3つ）への割り当てとみなすことができる.
Moreover, the values of the variables (describing items bought recently) are correlated.
さらに、変数（最近買ったものを表す）の値には相関がある.
However, we were able to exploit the special structure of our state and action spaces using different techniques.
しかし、私たちは別の手法で、状態空間(state space)と行動空間(action space)の特殊な構造を利用することができた.
In addition, we introduce approximations that exploit the fact that most states – that is, most item sequences – are highly unlikely to occur (a detailed explanation will follow in Section 3)..
さらに、ほとんどの状態、つまりほとんどの項目配列が非常に起こりにくいという事実を利用した近似を導入する（詳細な説明は第3節に続く）。

MDPs extend the simpler Markov chain (MC) model – a well known model of dynamic systems.
MDPは、動的システムのモデルとしてよく知られている、より単純なマルコフ連鎖(MC)モデルを拡張したものです。
A Markov chain is simply an MDP without actions.
マルコフ連鎖とは、単純にアクションのないMDPのことである。
It contains a set of states and a stochastic transition function between states.
これは、状態のセットと状態間の確率的遷移関数を含んでいます。
In both models the next state does not depend on any states other than the current state..
どちらのモデルでも、次の状態は現在の状態以外の状態には依存しない。

In the context of recommender systems, if we equate actions with recommendations, then an MDP can be used to model user behavior with recommendations – as we show below – whereas an MC can be used to model user behavior without recommendations.
レコメンダーシステムの文脈では、行動と推奨を同一視すると、以下に示すように、MDPは推奨を伴うユーザーの行動をモデル化するのに使用でき、MCは推奨を伴わないユーザーの行動をモデル化するのに使用できることになります。
Markov chains are also closely related to n-gram models.
マルコフ連鎖は、n-gramモデルとも密接な関係がある。
In a bi-gram model, the choice of the next word depends probabilistically on the previous word only.
バイグラムモデルでは、次の単語の選択は、前の単語のみに確率的に依存する。
Thus, a bi-gram is simply a first-order Markov chain whose states correspond to words.
したがって、バイグラムは、単に、状態が単語に対応する一次マルコフ連鎖である。
An n-gram is a n−1-order Markovian model in which the next state depends on the previous n − 1 states.
n-gramは、次の状態が前のn - 1個の状態に依存するn-1次マルコフモデルである。
Such variants of MDP-models are well known.
このようなMDPモデルの変種はよく知られている。
A non-first-order Markovian model can be converted into a first-order model by making each state include information related to the previous n−1 states.
非一次マルコフモデルは、各状態が前のn-1個の状態に関連する情報を含むようにすることで、一次モデルに変換することができます。
More general transformation techniques that attempt to reduce the size of the state space have been investigated in the literature (for example, see Bacchus et al.
状態空間のサイズを小さくしようとする、より一般的な変換技術が文献で研究されている（例えば、Bacchus et al.
(1996); Thiebaux et al.
(1996); Thiebaux et al.
(2002))..
(2002))..

# 3. The Predictive Model 予測モデル

Our first step is to construct a predictive model of user purchases, that is, a model that can predict what item the user will buy next.
まず、ユーザーの購買予測モデル、つまり、ユーザーが次にどのようなアイテムを購入するかを予測できるモデルを構築します。
This model does not take into account its influence on the user, as it does not model the recommendation process and its effects.
このモデルでは、推薦のプロセスやその効果をモデル化していないため、ユーザーへの影響を考慮していない。
Nonetheless, we shall use a Markov chain, with an appropriate formulation of the state space, as our model.
それでも、状態空間を適切に定式化したマルコフ連鎖をモデルとして使用することにする。
In Section 4 we shall show that our predictive model outperforms previous models, and in Section 5 we shall intialize our MDP-based recommender system using this predictive model..
第4節では、本予測モデルが従来のモデルを凌駕することを示し、第5節では、本予測モデルを用いたMDPベースのレコメンダーシステムの初期化について述べる。

## 3.1. The Basic Model 基本モデルです。

A Markov chain is a model of system dynamics – in our case, user “dynamics.” To use it, we need to formulate an appropriate notion of a user state and to estimate the state-transition function..
マルコフ連鎖は、システムのダイナミクス（ここではユーザーの "ダイナミクス"）をモデル化したものです。マルコフ連鎖を利用するためには、ユーザーの状態に関する適切な概念を定式化し、状態遷移関数を推定することが必要である。

States.
状態です。
The states in our MC model represent the relevant information that we have about the user.
MCモデルの状態は、ユーザーについて我々が持っている関連情報を表しています。
This information corresponds to previous choices made by users in the form of a set of ordered sequences of selections.
この情報は、ユーザーが過去に行った選択に対応するもので、順序付けられた選択順序の集合の形をしています。
We ignore data such as age or gender, although it could be beneficial.3 Thus, the set of states contains all possible sequences of user selections.
年齢や性別のようなデータは、有益である可能性があるが、無視する。3 したがって、状態のセットは、ユーザーの選択のすべての可能なシーケンスを含む。
Of course, this formulation leads to an unmanageable state space with the usual associated problems—data sparsity and MDP solution complexity.
もちろん、この定式化は、データスパース性とMDP解の複雑さという、通常の関連問題を伴う扱いにくい状態空間をもたらす。
To reduce the size of the state space, we consider only sequences of at most k items, for some relatively small value of k.
状態空間のサイズを小さくするために、kの値が比較的小さい場合、最大でk個のアイテムのシーケンスのみを考慮する。
We note that this approach is consistent with the intuition that the near history (for example, the current user session) often is more relevant than selections made less recently (for example, past user sessions).
このアプローチは、近い履歴（例えば、現在のユーザーセッション）は、より最近（例えば、過去のユーザーセッション）に選択されたものよりも関連性が高いことが多いという直観と一致することに留意されたい。
These sequences are represented as vectors of size k.
これらの配列は、サイズkのベクトルとして表現される。
In particular, we use hx1,...,xki to denote the state in which the user’s last k selected items were x1, .
特に、hx1,...,xkiを使用して、ユーザーの直近のk個の選択項目がx1, .
.
.
.
.
, xk.
を、xk。
Selection sequences with l < k items are transformed into a vector in which x1 through xk−l have the value missing.
l＜k個の選択配列は、x1〜xk-lの値がmissingとなるベクトルに変換される。
The initial state in the Markov chain is the state in which every entry has the value missing.
マルコフ連鎖の初期状態は、すべてのエントリーが値missingを持つ状態である。
4 In our experiments, we used values of k ranging from 1 to 5..
4 実験では、kの値を1～5まで使用した。

The Transition Function.
トランジション機能です。
The transition function for our Markov chain describes the probability that a user whose k recent selections were x1,...,xk will select the item x 0 next, denoted trMC(hx1, x2,...,xki,hx2,...,xk, x 0 i).
マルコフ連鎖の遷移関数は、最近k回選択したアイテムがx1,...,xkであったユーザが次にx0を選択する確率を記述し、trMC（hx1, x2,...,xki,hx2,...,xk, x 0 i）と表記されます。
Initially, this transition function is unknown to us; and we would like to estimate it based on user data.
この遷移関数は、当初は未知であり、ユーザーデータに基づいて推定したい。
As mentioned, a maximum-likelihood estimate can be used:.
前述したように、最尤推定を使用することができます：。

$$
\tag{5}
$$

where count(hx1, x2,...,xki) is the number of times the sequence x1, x2,...,xk was observed in the data set.
ここで、count(hx1, x2,...,xki) は、シーケンス x1, x2,...,xk がデータセットで観察された回数である。
This model, however, still suffers from the problem of data sparsity (for example, see Sarwar et al.
しかし、このモデルは、依然としてデータの疎密の問題に悩まされている（例えば、Sarwar et al.
(2000a)) and performs poorly in practice.
(2000a)）で、実際の性能は低い。
In the next section, we describe several techniques for improving the estimate..
次節では、推定値を改善するためのいくつかの技法について説明する。

## 3.2. Some Improvements いくつかの改善点。

We experimented with several enhancements to the maximum-likelihood n-gram model on data different from that used in our formal evaluation.
最尤N-gramモデルについては、正式な評価で使用したデータとは異なるデータで、いくつかの機能拡張の実験を行いました。
The improvements described and used here are those that were found to work well..
ここで説明され、使用されている改良は、うまく機能することが確認されたものです。

One enhancement is a form of skipping (Chen and Goodman, 1996), and is based on the observation that the occurrence of the sequence x1, x2, x3 lends some likelihood to the sequence x1, x3.
1つの強化はスキップの一種で（Chen and Goodman, 1996）、シーケンスx1, x2, x3の発生がシーケンスx1, x3にある程度の可能性を与えるという観察に基づいている。
That is, if a person bought x1, x2, x3, then it is likely that someone will buy x3 after x1.
つまり、x1、x2、x3を買った人がいた場合、x1の次にx3を買う人がいる可能性が高い。
The particular skipping model that we found to work well is a simple additive model.
私たちがうまく機能することを発見した特定のスキップモデルは、単純な加法モデルです。
First, the count for each state transition is initialized to the number of observed transitions in the data.
まず、各状態遷移のカウントは、データで観測された遷移の数に初期化される。
Then, given a user sequence x1, x2,...,xn, we add the fractional count 1/2 (j−(i+3)) to the transition from hxi , xi+1, xi+2i to hxi+1, xi+2, xji, for all i+3 < j ≤ n.
次に、ユーザー列x1,x2,...,xnが与えられたとき、分数カウント1
This fractional count corresponds to a diminishing probability of skipping a large number of transactions in the sequence.
この端数カウントは、シーケンス内の多数のトランザクションをスキップする確率が減少することに対応しています。
We then normalize the counts to obtain the transition probabilities:.
次に、カウントを正規化し、遷移確率を求める。

$$
\tag{6}
$$

where count(s,s 0 ) is the (fractional) count associated with the transition from s to s 0 ..
ここで、count(s,s 0 )は、sからs 0への遷移に関連する（分数）カウントである。

A second enhancement is a form of clustering that we have not found in the literature.
2つ目の強化点は、文献にはないクラスタリングという形式を採用したことです。
Motivated by properties of our domain, the approach exploits similarity of sequences.
このアプローチは、我々のドメインの特性から動機づけられ、シーケンスの類似性を利用するものである。
For example, the state hx, y,zi and the state hw, y,zi are similar because some of the items appearing in the former appear in the latter as well.
例えば、状態hx,y,ziと状態hw,y,ziは、前者に出現する項目の一部が後者にも出現するため、類似しています。
The essence of our approach is that the likelihood of transition from s to s 0 can be predicted by occurrences from t to s 0 , where s and t are similar.
このアプローチの本質は、sとtが類似している場合、sからs 0への移行の尤度を、tからs 0への発生によって予測できることである。
In particular, we define the similarity of states si and sj to be.
特に、状態siとsjの類似性を次のように定義する。

$$
\tag{7}
$$

where δ(·,·) is the Kronecker delta function and s m i is the mth item in state si .
ここで、δ(-,-)はクロネッカーデルタ関数、s m i は状態 si における m 番目のアイテムである。
This similarity is arbitrary up to a constant.
この類似性は一定まで任意である。
In addition, we define the similarity count from state s to s 0 to be.
また、状態sからs 0への類似度カウントを次のように定義する。

$$
\tag{8}
$$

where trold MC(si ,s 0 ) is the original transition function, with or without skipping (we shall compare the models created with and without the benefit of skipping).
ここで、trold MC(si ,s 0 )は、スキップの有無にかかわらず、元の遷移関数である（スキップの恩恵の有無で作成したモデルを比較することにする）。
The new transition probability from s 0 to s is then given by5.
そして、s 0からsへの新しい遷移確率は、次式で与えられる5。

$$
\tag{9}
$$

A third enhancement is the use of finite mixture modeling.6 Similar methods are used in ngram models, where—for example—a trigram, a bigram, and a unigram are combined into a single model.
同様の手法は、例えば、トリグラム、ビッグラム、ユニグラムを1つのモデルに統合する、ヌグラムモデルでも使用されています6。
Our mixture model is motivated by the fact that larger values of k lead to states that are more informative whereas smaller values of k lead to states on which we have more statistics.
この混合モデルは、kの値が大きいほど情報量の多い状態になり、kの値が小さいほど統計量の多い状態になるという事実に基づいています。
To balance these conflicting properties, we mix k models, where the ith model looks at the last i transactions.
これらの相反する特性のバランスをとるために、k個のモデルを混合し、i番目のモデルは直近のi個のトランザクションを見るようにする。
Thus, for k = 3, we mix three models that predict the next transaction based on the last transaction, the last two transactions, and the last three transactions.
したがって、k = 3の場合、最後の取引、最後の2つの取引、最後の3つの取引に基づいて次の取引を予測する3つのモデルを混合する。
In general, we can learn mixture weights from data.
一般的には、データから混合物の重みを学習することができます。
We can even allow the mixture weights to depend on the given case (and informal experiments on our data suggest that such context-specificity would improve predictive accuracy).
また、混合比の重みが与えられたケースに依存するようにすることもできます（私たちのデータに対する非公式な実験では、このような文脈特異性が予測精度を向上させることが示唆されています）。
Nonetheless, for simplicity, we use π1 = ··· = πk = 1/k in our experiments.
それにもかかわらず、簡単のために、π1＝---＝πk＝1とする。
Because our primary model is based on the k last items, the generation of the models for smaller values entails little computational overhead..
我々の主要なモデルは最後のk個のアイテムに基づいているため、より小さな値のモデルの生成はほとんど計算オーバーヘッドを必要としない。

# 4. Evaluation of the Predictive Model 予測モデルの評価

Before incorporating our predictive model into an MDP-based recommender system, we evaluated the accuracy of the predictive model.
MDPベースのレコメンダーシステムに予測モデルを組み込む前に、予測モデルの精度を評価しました。
Our evaluation used data corresponding to user behavior on a web site (without recommendation) and employed the evaluation metrics commonly used in the collaborative filtering literature.
評価には、Webサイト上でのユーザーの行動（推薦なし）に相当するデータを使用し、協調フィルタリングの文献で一般的に使用されている評価指標を採用しました。
In Section 6 we evaluate the MDP-based approach using an experimental approach in which recommendations on an e-commerce site are manipulated by our algorithms..
セクション6では、電子商取引サイトのレコメンデーションが我々のアルゴリズムによって操作される実験的アプローチを用いて、MDPベースのアプローチを評価する。

## 4.1. Data Sets データセット

We base our evaluations on real user transactions from the Israeli online bookstore Mitos(www.mitos.co.il).
イスラエルのオンライン書店Mitos(www.mitos.co.il)の実際のユーザー取引に基づく評価を行っています。
Two data sets were used: one containing user transactions (purchases) and one containing user browsing paths obtained from web logs.
ユーザーのトランザクション（購入）を含むデータセットと、ウェブログから取得したユーザーのブラウジングパスを含むデータセットの2つを使用しました。
We filtered out items that were bought/visited less than 100 times and users who bought/browsed no more than one item as is commonly done when evaluating predictive models (for example, Zimdars et al.
購入された商品をフィルタリングしました
(2001)).
(2001)).
We were left with 116 items and 10820 users in the transactions data set, and 65 items and 6678 users in the browsing data set.7 In our browsing data, no cookies were used by the site.
その結果，トランザクションデータセットとして116アイテム，10820ユーザー，ブラウジングデータセットとして65アイテム，6678ユーザーが残された7。ブラウジングデータでは，サイトがクッキーを使用していない。
If the same user visited the site with a new IP address, then we would treat her as a new user.
同じユーザーが新しいIPアドレスでサイトを訪れた場合、新しいユーザーとして扱われます。
Also, activity on the same IP address was attributed to a new user whenever there were no requests for two hours.
また、同じIPアドレスでのアクティビティは、2時間リクエストがない場合、新しいユーザーに帰属していました。
These data sets were randomly split into a training set (90% of the users) and a test set (10% of the users)..
これらのデータセットは、ランダムにトレーニングセット（ユーザーの90％）とテストセット（ユーザーの10％）に分割されました。

The rational for removing items that were rarely bought is that they cannot be reliably predicted.
ほとんど買われなかったものを削除する根拠は、確実な予測ができないからです。
This is a conservative approach which implies, in practice, that a rarely visited item will not be recommended by the system, at least initially..
これは保守的なアプローチであり、実際には、めったに訪れないアイテムは、少なくとも最初はシステムによって推奨されないことを意味します。

We evaluated predictions as follows.
予測値の評価は以下のように行いました。
For every user sequence t1,t2,..,tn in the test set, we generated the following test cases:.
テストセット内の各ユーザーシーケンスt1,t2,...,tnに対して、以下のテストケースを生成した。

$$
\tag{10}
$$

closely following tests done by Zimdars et al.
Zimdarsらによって行われたテストに密着しています。
(2001).
(2001).
For each case, we then used our various models to determine the probability distribution for ti given ti−k,ti−k+1,...,ti−1 and ordered the items by this distribution.
そして、それぞれのケースについて、様々なモデルを用いて、ti-k,ti-k+1,...,ti-1が与えられたときのtiの確率分布を求め、この分布によって項目を並べました。
Finally, we used the ti actually observed in conjunction with the list of recommended items to compute a score for the list..
最後に、実際に観察されたtiと推奨アイテムのリストを合わせて、リストのスコアを算出しました。

## 4.2. Evaluation Metrics 評価指標

We used two scores: Recommendation Score (RC) (Microsoft, 2002) and Exponential Decay Score (ED) (Breese et al., 1998) with slight modifications to fit into our sequential domain..
我々は2つのスコアを使用した。Recommendation Score (RC) (Microsoft, 2002) と Exponential Decay Score (ED) (Breese et al., 1998) の2つのスコアを使用し、我々のシーケンシャルドメインに適合するように若干の修正を加えている．

### 4.2.1. Recommendation Score レコメンドスコア

For this measure of accuracy, a recommendation is deemed successful if the observed item ti is among the top m recommended items (m is varied in the experiments).
この精度の指標では、観測されたアイテムtiが上位m個の推奨アイテムの中にあれば、推奨は成功したとみなされる（実験ではmは変化させる）。
The score RC is the percentage of cases in which the prediction is successful.
スコアRCは、予測が成功したケースの割合である。
A score of 100 means that the recommendation was successful in all cases.
100点満点は、すべてのケースで推薦が成功したことを意味します。
This score is meaningful for commerce sites that require a short list of recommendations and therefore care little about the ordering of the items in the list..
このスコアは、短い推奨リストを必要とし、したがってリスト内のアイテムの順序をあまり気にしないコマースサイトに有意義である。

### 4.2.2. Exponential Decay Score 指数関数的減衰スコア。

This measure of accuracy is based on the position of the observed ti on the recommendation list, thus evaluating not only the content of the list but also the order of items in it.
この精度の指標は、推薦リストにおける観測されたtiの位置に基づいているため、リストの内容だけでなく、リスト内のアイテムの順序も評価されます。
The underlying assumption is that users are more likely to select a recommendation near the top of the list.
ユーザーがリストのトップに近いレコメンドを選択する可能性が高いというのが根本的な前提です。
In particular, it is assumed that a user will actually see the mth item in the list with probability.
特に、ユーザがリストのm番目の項目を実際に見ることは確率的に想定されている。

$$
\tag{11}
$$

where α is the half-life parameter—the index of the item in the list with probability 0.5 of being seen.
ここで、αは半減期パラメータ-リストの中で0.5%の確率で見られるアイテムのインデックス-である。
The score is given by.
スコアは、次のように与えられます。

$$
\tag{12}
$$

where C is the set of all cases, c = ti−k,ti−k+1,...,ti−1 is a case, and pos(ti |c) is the position of the observed item ti in the list of recommended items for c.
c) is the position of the observed item ti in the list of recommended items for c.
We used α = 5 in our experiments in order to be consistent with the experiments of Breese et al.
Breeseらの実験と整合性を取るため、実験ではα＝5を使用した。
(1998) and Zimdars et al.
(1998)、Zimdars et al.
(2001).
(2001).
The relative performance of the models was not sensitive to α..
モデルの相対的な性能は、αに敏感ではなかった。

## 4.3. Comparison Models 比較モデルです。

### 4.3.1. Commerce Server 2000 Predictor Commerce Server 2000 Predictor.

A model to which we compared our results is the Predictor tool developed by Microsoft as a part of Microsoft Commerce Server 2000, based on the models of Heckerman et al.
今回の結果を比較したモデルとして、HeckermanらのモデルをベースにMicrosoft Commerce Server 2000の一部としてMicrosoft社が開発したPredictorツールがあります。
(2000).
(2000).
This tool builds dependency-network models in which the local distributions are probabilistic decision trees.
局所分布が確率的な決定木である依存関係ネットワークモデルを構築するツールです。
We used these models in both a non-sequential and sequential form.
これらのモデルを、非連続型と連続型の両方で使用しました。
These two approaches are described in Heckerman et al.
これら2つのアプローチについては、Heckerman et al.に記載されています。
(2000) and Zimdars et al.
(2000)、Zimdars et al.
(2001), respectively.
(2001)をそれぞれ参照してください。
In the non-sequential approach, for every item, a decision tree is built that predicts whether the item will be selected based on whether the remaining items were or were not selected.
非連続型では、すべての項目に対して、残りの項目が選ばれたか選ばれなかったかで、その項目が選ばれるかどうかを予測する決定木が構築されます。
In the sequential approach, for every item, a decision tree is built that predicts whether the item will be selected next, based on the previous k items that were selected.
逐次方式では、すべての項目に対して、過去に選択されたk個の項目に基づいて、次にその項目が選択されるかどうかを予測する決定木が構築されます。
The predictions are normalized to account for the fact that only one item can be predicted next.
予測値は、次に予測できる項目が1つだけであることを考慮して正規化されています。
Zimdars et al.
Zimdars et al.
(2001) also use a “cache” variable, but preliminary experiments showed it to decrease predictive accuracy.
(2001)も「キャッシュ」変数を用いているが、予備実験では予測精度を低下させることがわかった。
Consequently, we did not use the cache variable in our formal evaluation..
そのため、正式な評価では、キャッシュ変数を使用しませんでした。

These algorithms appear to be the most competitive among published work.
これらのアルゴリズムは、公開されている作品の中で最も競争力があると思われます。
The combined results of Breese et al.
Breeseらの結果を総合すると
(1998) and Heckerman et al.
(1998)、Heckerman et al.
(2000) show that (non-sequential) dependency networks are no less accurate than Bayesian-network or clustering models, and about as accurate as Correlation, the most accurate (but computationally expensive) memory-based method.
(2000)は、（非連続）依存性ネットワークは、ベイジアンネットワークやクラスタリングモデルに劣らず、最も正確な（しかし計算コストのかかる）メモリベースの方法であるCorrelationとほぼ同じ精度であることを示しています。
Sarwar et al.
Sarwarら。
(2000b) apply dimensionality reduction techniques to the user rating matrix, but their approach fails to be consistently more accurate than Correlation.
(2000b)は、ユーザー評価行列に次元削減技術を適用したが、彼らのアプローチは、Correlationより一貫して正確であることを失敗した。
Only the sequential algorithm of Zimdars et al.
Zimdarsらの逐次アルゴリズムのみ。
(2001) is more accurate than the non-sequential dependency network to our knowledge..
(2001)は、我々の知る限り、非連続従属ネットワークより正確である。

We built five sequential models 1 ≤ k ≤ 5 for each of the data sets.
各データセットについて、1≦k≦5の5つの逐次モデルを構築しました。
We refer to the non-sequential Predictor models as Predictor-NS, and to the Predictor models built using the data expansion methods with a history of length k as Predictor-k..
非連続的なPredictorモデルをPredictor-NS、長さkの履歴を持つデータ拡張法を用いて構築したPredictorモデルをPredictor-kと呼ぶことにする。

### 4.3.2. Unordered MCs アンオーダーメイドのMC

We also evaluated a non-sequential version of our predictive model, where sequences such as hx, y,zi and hy,z, xi are mapped to the same state.
また、hx,y,ziやhy,z,xiなどのシーケンスが同じ状態にマッピングされる、予測モデルの非シーケンシャル版も評価しました。
If our assumption about the sequential nature of recommendations is incorrect, then we should expect this model to perform better than our MC model, as it learns the probabilities using more training data for each state, gathering all the ordered data into one unordered set.
もし、レコメンデーションの順次性についての仮定が正しくない場合、このモデルは、各状態についてより多くのトレーニングデータを用いて確率を学習し、すべての順序付きデータを1つの順序なしセットに集めるので、MCモデルよりも良いパフォーマンスを示すと予想されます。
Skipping, clustering, and mixture modeling were included as described in section 2.
スキップ、クラスタリング、混合モデリングは、セクション 2 で説明したように含まれています。
We call this model UMC (Unordered Markov chain)..
このモデルをUMC(Unordered Markov chain)と呼ぶ。

## 4.4. Variations of the MC Model MCモデルのバリエーション

In order to measure how each n-gram enhancement influenced predictive accuracy, we also evaluated models that excluded some of the enhancements.
また、各n-gramの強化が予測精度に与える影響を測定するために、一部の強化を除いたモデルも評価しました。
In reporting our results, we refer to a model that uses skipping and similarity clustering with the terms SK and SM, respectively.
結果を報告する際、飛び飛びのクラスタリングと類似のクラスタリングを使用するモデルをそれぞれSKとSMと呼ぶことにする。
In addition, we use numbers to denote which mixture components are used.
また、どの混合成分が使用されているかを数字で表しています。
Thus, for example, we use MC 123 SK to denote a Markov chain model learned with three mixture components—a bigram, trigram, and quadgram—where each component employs skipping but not clustering..
例えば、MC123 SKは、bigram, trigram, quadgramの3つの混合成分で学習したマルコフ連鎖モデルであり、各成分はクラスタリングを行わず、スキップすることを表す。

## 4.5. Experimental Results 実験結果です。

Figure 1(a) and figure 1(b) show the exponential decay score for the best models of each type (Markov chain, Unordered Markov chain, Non-Sequential Predictor model, and Sequential Predictor Model).
図1（a）、図1（b）は、各タイプの最良モデル（マルコフ連鎖、非順序マルコフ連鎖、非順序予測モデル、順序予測モデル）の指数関数的減衰スコアを示しています。
It is important to note that all the MC models using skipping, clustering, and mixture modelling yielded better results than every one of the Predictor-k models and the non-sequential Predictor model.
スキップ、クラスタリング、混合モデリングを用いたすべてのMCモデルが、Predictor-kモデルや非連続Predictorモデルのどれよりも良い結果をもたらしたことは重要なポイントです。
We see that the sequence-sensitive models are better predictors than those that ignore sequence information.
配列情報を無視したモデルよりも、配列に敏感なモデルの方が予測精度が高いことがわかる。
Furthermore, the Markov chain predicts best for both data sets..
さらに、マルコフ連鎖は、どちらのデータセットに対しても最適な予測をしている。

Figure 2(a) and Figure 2(b) show the recommendation score as a function of list length (m).
図2（a）と図2（b）は、リスト長（m）の関数として推薦スコアを示したものである。
Once again, sequential models are superior to non-sequential models, and the Markov chain models are superior to the Predictor models..
今回もシーケンシャルモデルはノンシーケンシャルモデルより優れており、マルコフ連鎖モデルはプレディクターモデルより優れています。

Figure 3(a) and Figure 3(b) show how different versions of the Markov chain performed under the exponential decay score in both data sets.
図3(a)と図3(b)は、両方のデータセットにおいて、指数関数的減衰スコアの下でマルコフ連鎖の異なるバージョンがどのように機能するかを示している。
We see that multi-component models out-perform single-component models, and that similarity clustering is beneficial.
多成分モデルが単成分モデルより優れていること、類似性クラスタリングが有効であることがわかります。
In contrast, we find that skipping is only beneficial for the transactions data set.
一方、スキップが有効なのは、トランザクションデータセットのみであることがわかります。
Perhaps users tend to follow the same paths in a rather conservative manner, or site structure does not allow users to “jump ahead”.
おそらく、ユーザーはどちらかというと保守的に同じ道をたどる傾向があるのか、サイト構造上、ユーザーが "先に進む "ことができないのでしょう。
In either case, once recommendations are available in the site (thus changing the site structure), skipping may prove beneficial..
いずれにせよ、サイト内でレコメンデーションが利用できるようになると（サイト構造が変わる）、スキップが有効になる可能性があります。

# 5. An MDP-Based Recommender Model MDP ベースの推薦者モデル

The predictive model we described above does not attempt to capture the short and long-term effect of recommendations on the user, nor does it try to optimize its behavior by taking into account such effects.
先に述べた予測モデルは、レコメンデーションがユーザーに与える短期的・長期的な影響を捉えようとするものではなく、また、そうした影響を考慮して行動を最適化しようというものでもない。
We now move to an MDP model that explicitly models the recommendation process and attempts to optimize it.
ここで、推薦プロセスを明示的にモデル化し、その最適化を試みるMDPモデルに移行する。
The predictive model plays an important role in the construction of this model..
このモデルの構築には、予測モデルが重要な役割を果たします。

We assume that we are given a set of cases describing user behavior within a site that does not provide recommendations, as well as a probabilistic predictive model of a user acting without recommendations generated from this data.
ここでは、レコメンデーションを提供しないサイト内でのユーザーの行動を記述したケースと、このデータから生成されたレコメンデーションなしで行動するユーザーの確率的予測モデルが与えられると仮定する。
The set of cases is needed to support some of the approximations we make, and in particular, the lazy initialization approach we take.
このケースは、私たちが行う近似の一部、特に私たちが取る遅延初期化アプローチをサポートするために必要です。
The predictive model provides the probability the user will purchase a particular item x given that her sequence of past purchases is x1,...,xk.
予測モデルは、ユーザーが過去の購入履歴がx1,...,xkである場合に、特定のアイテムxを購入する確率を提供します。
We denote this value by Prpred(x|x1,...,xk), where k = 3 in our case.
x1,...,xk), where k = 3 in our case.
It is important to stress that the approach presented here is independent of the particular technique by which the above predictive value is approximated.
ここで強調したいのは、ここで紹介するアプローチは、上記の予測値を近似する特定の技術に依存しないということである。
Naturally, in our implementation we used the predictive model developed in Section 3, but there are other ways of constructing such a model (for example, Zimdars et al.
当然ながら、我々の実装では、セクション3で開発した予測モデルを使用したが、このようなモデルを構築する方法は他にもある（例えば、Zimdars et al.
(2001); Kadie et al.
(2001); Kadie et al.
(2002))..
(2002))..

## 5.1. Defining the MDP MDPを定義する。

Recall that to define an MDP, we need to provide a set of states, actions, transition function, and a reward function.
MDPを定義するためには、状態、行動、遷移関数、報酬関数のセットを提供する必要があることを思い出してください。
We now describe each of these elements.
次に、これらの要素についてそれぞれ説明します。
The states of the MDP for our recommender system are k-tuples of items (for example, books, CDs), some prefix of which may contain null values corresponding to missing items.
推薦システムのMDPの状態は、アイテム（例えば、本、CD）のkタプルであり、そのうちのいくつかの接頭辞は、アイテムの欠落に対応するNULL値を含むことができる。
This allows us to model shorter sequences of purchases..
これにより、より短い購入の連続をモデル化することができます。

The actions of the MDP correspond to a recommendation of an item.
MDPのアクションは、アイテムの推薦に対応しています。
One can consider multiple recommendations but, to keep our presentation simple, we start by discussing single recommendations..
複数の推奨事項を検討することも可能ですが、ここではシンプルに、一つの推奨事項を検討することから始めます。

Rewards in our MDP encode the utility of selling an item (or showing a web page) as defined by the site.
MDPの報酬は、サイトが定義する商品を売る（あるいはウェブページを見せる）ことの効用を符号化したものである。
Because the state encodes the list of items purchased, the reward depends on the last item defining the current state only.
状態は購入したアイテムのリストを符号化するため、報酬は現在の状態を定義する最後のアイテムにのみ依存する。
For example, the reward for state hx1, x2, x3i is the reward generated by the site from the sale of item x3.
例えば、状態hx1, x2, x3iの報酬は、アイテムx3の販売からサイトが生み出す報酬である。
In this paper, we use net profit for reward..
本論文では、報酬のために純利益を使用します。

The state following each recommendation is determined by the user’s response to that recommendation.
各レコメンドに続く状態は、そのレコメンドに対するユーザーの反応によって決まります。
When we recommend an item x 0 , the user has three options:.
アイテムx 0を勧めるとき、ユーザーには次の3つの選択肢がある。

- Accept this recommendation, thus transferring from state hx1, x2, x3i into hx2, x3, x 0 i この勧告を受け入れることで、状態hx1, x2, x3iからhx2, x3, x 0 iに移行する。

- Select some non-recommended item x 00, thus transferring the state hx1, x2, x3i into hx2, x3, x 00i. ある非推奨アイテムx 00を選択することで、状態hx1, x2, x3iをhx2, x3, x 00iに移行させる。

- Select nothing (for example, when the user terminates the session), in which case the system remains in the same state. 何もしない（ユーザーがセッションを終了した場合など）を選択すると、システムはそのままの状態を維持します。

Thus, the stochastic element in our model is the user’s actual choice.
したがって、このモデルにおける確率的要素は、ユーザーの実際の選択である。
The transition function for the MDP model:.
MDPモデルの遷移関数：。

$$
\tag{13}
$$

is the probability that the user will select item x 00 given that item x 0 is recommended in state hx1, x2, x3i.
は、状態hx1, x2, x3iでアイテムx0が推奨されている場合に、ユーザがアイテムx00を選択する確率である。
We write tr1 MDP to denote that only single item recommendations are used..
単品推薦のみを行うことを表すためにtr1 MDPと表記する。

### 5.1.1. Initializing $tr_{MMDP}$ $tr_{MMDP}$ を初期化する。

Proper initialization of the transition function is an important implementation issue in our system.
遷移関数の適切な初期化は、本システムにおける重要な実装課題である。
Unlike traditional model-based reinforcement learning algorithms that learn the proper values for the transition function and hence an optimal policy online, our system needs to be fairly accurate when it is first deployed.
従来のモデルベースの強化学習アルゴリズムが、遷移関数の適切な値、つまり最適なポリシーをオンラインで学習するのとは異なり、私たちのシステムは、最初に展開するときにかなり正確である必要があります。
A for-profit e-commerce8 site is unlikely to use a recommender system that generates irrelevant recommendations for a long period, while waiting for it to converge to an optimal policy.
営利目的のEコマース8サイトでは、最適なポリシーに収束するのを待つ間、無関係なレコメンドを生成するレコメンダーシステムを長期間使用することは考えにくいです。
We therefore need to initialize the transition function carefully.
そのため、遷移関数を慎重に初期化する必要があります。
We can do so based on any good predictive model, making the following assumptions:.
あらゆる優れた予測モデルに基づいて、次のような仮定を立てて行うことができます。

- A recommendation increases the probability that a user will buy an item. This probability is proportional to the probability that the user will buy this item in the absence of recommendations. This assumption is made by most collaborative filtering models dealing with e-commerce sites.9 We denote the proportionality constant for recommendation r in state s by αs,r , where αs,r > 1. レコメンデーションは、ユーザーが商品を購入する確率を高めるものです。 この確率は、レコメンドがない場合にユーザーがこのアイテムを購入する確率に比例する。 この仮定は、電子商取引サイトを扱う協調フィルタリングモデルの多くでなされている9。状態sにおける推薦rの比例定数をαs,rとし、αs,r > 1とする。

- The probability that a user will buy an item that was not recommended is lower than the probability that she will buy when the system issues no recommendations at all, but still proportional to it. We denote the proportionality constant for recommendation r in state s by βs,r , where βs,r < 1. 推薦されなかった商品を購入する確率は、システムが全く推薦をしない場合に購入する確率より低いが、それでも比例しているのである。 状態sにおける推薦者rの比例定数をβs,rとする（βs,r＜1）。

To allow for a simpler representation of the equations, for a state s = hx1,...,xki and a recommendation r let us use s·r to denote the state s 0 = hx2,...,xk,ri.
方程式をより簡単に表現するために、状態s = hx1,...,xkiと推薦rに対して、状態s 0 = hx2,...,xk,ri を表すためにs-rを使用することにする。
We use trpredict(s,s·r) to denote the probability that the user will choose r next, given that its current state is s according to the predictive model in which recommendations are not considered, that is, Prpred(r|s).
s).
Thus, with αs,r and βs,r constant over s and r and equal to α and β, respectively, we have.
したがって、αs,rとβs,rがsとrにわたって一定で、それぞれαとβに等しいとすると、次のようになる。

$$
\tag{14}
$$

the probability that a user will buy r next if it was recommended;.
推奨された場合、ユーザーが次にrを購入する確率；。

$$
\tag{15}
$$

the probability that a user will buy r if something else was recommended; and.
他のものを勧められた場合に、ユーザーがrを購入する確率。

$$
\tag{16}
$$

the probability that a user will not buy any new item after r was recommended.
が推奨された後、そのユーザーが新たなアイテムを購入しない確率を示す。
We do not see a reason to stipulate a particular relationship between α and β, although we must have.
なければならないが、αとβの関係を特に規定する理由は見いだせない。

$$
\tag{17}
$$

The exact values of αs,r and βs,r should be chosen carefully.
αs,rとβs,rの正確な値は慎重に選択する必要があります。
Choosing αs,r and βs,r to be constants over all states and recommendations (say α = 2, β = 0.5) might cause the sum of transition probabilities in the MDP to exceed 1.
αs,rとβs,rをすべての状態とレコメンデーションで定数にすると（α＝2、β＝0.5）、MDPの遷移確率の合計が1を超えてしまう可能性があります。
The approach we took was motivated by Kitts et al.
私たちがとったアプローチは、Kittsらによって動機づけられたものです。
(2000), who showed that the increase in the probability of following a recommendation is large when one recommends items having high lift, defined to be pr(x|h) pr(x) .
h) pr(x) .
Thus, it is not unreasonable to assume that this increase in probability is proportional to lift:.
したがって、この確率の上昇は、リフト：に比例すると考えても無理はないでしょう。

$$
\tag{18}
$$

where p(r) is the prior probability of buying r.
ここで、p(r)はrを購入する事前確率である。
Fixing αs,r to be a little larger than 1 as follows:.
次のようにαs,rが1より少し大きくなるように固定する。

$$
\tag{19}
$$

where γ is a very small constant (we use γ = 1 1000 ), and solving for βs,r , we obtain.
ここで、γは非常に小さな定数（ここではγ＝1 1000としている）であり、βs,r について解くと、次のようになる。

$$
\tag{20}
$$

If βs,r is negative, we set it to a very small positive value and normalize the probabilities afterwards..
βs,rが負の値であれば、非常に小さな正の値に設定し、その後の確率を正規化します。

There are a few things to note about tr1 MDP(s,r 0 ,s·r), the probability that a user will buy r if something else was recommended, and its representation.
tr1 MDP(s,r 0 ,s-r)、ユーザーが他のものを勧められた場合にrを購入する確率とその表現について、いくつか注意すべき点があります。
First, since tr1 MDP(s,r 0 ,s·r) = βs,r ·tr(s,s· r), the MDP’s initial transition probability does not depend on r 0 because our initialization is based on data that was collected without the benefit of recommendations.
まず、tr1 MDP(s,r 0 ,s-r) = βs,r -tr(s,s- r)であるため、推薦の恩恵を受けずに収集したデータに基づいて初期化を行うため、MDPの初期遷移確率がr 0に依存しない。
Of course, if one has access to data that reflects the effect of recommendations (prpredict(s·r|s,r)), one can use it to provide a more accurate initial model.
s,r)), one can use it to provide a more accurate initial model.
Next, note that we can represent this transition function concisely using at most two values for every state-item pair: the probability that an item will be selected in a state when it is recommended (that is, pr(s·r|s,r)) and the probability that an item will be selected when it is not recommended (that is, pr(s·r|s,r 0 )).
s,r)) and the probability that an item will be selected when it is not recommended (that is, pr(s·r
Because the number of items is much smaller than the number of states, we obtain significant reduction in the space requirements of the model..
アイテム数が状態数よりはるかに少ないため、モデルの空間要件が大幅に削減されます。

### 5.1.2. Generating Multple Recommendations 複数の推薦文を生成する。

When moving to multiple recommendations, we make the assumption that recommendations are independent.
複数のレコメンデーションに移行する場合、レコメンデーションが独立していることを前提にしています。
Namely we assume that for every pair of sets of recommended items, R,R 0 , we have that.
すなわち、推奨アイテムの集合であるR,R 0の各ペアについて、次のように仮定する。

$$
\tag{21}
$$

This assumption might prove to be false.
この仮定は誤りであることが証明されるかもしれません。
It seems reasonable that, as the list of recommendations grows, the probability of selecting any item decreases.
推薦リストが大きくなるにつれて、どの項目も選択される確率が低くなるのは、合理的なことだと思います。
Another more subtle example is the case where the system “thinks” that the user is interested in an inexpensive cooking book.
また、もっと微妙な例として、ユーザーが安価な料理本に興味を持っているとシステムが "考える "ケースもあります。
It can then recommend a few very expensive cooking books and one is reasonably priced (but in no way cheap) cooking book.
そして、非常に高価な料理本を数冊と、手頃な価格の（しかし決して安くはない）料理本を1冊を推薦することができます。
The reasonably priced book will seem like a bargain compared to the expensive ones, thus making the user more likely to buy it..
リーズナブルな価格の本は、高価な本と比べてお買い得に感じられるため、ユーザーは購入しやすくなります。

Nevertheless, we make this assumption so as not to be forced to create a larger action space where actions are ordered combinations of recommendations.
しかし、この仮定は、アクションがレコメンデーションの順序付けられた組み合わせである、より大きなアクション空間を作ることを余儀なくされないようにするためである。
Taking the simple approach for representing the transition function we defined above, we still keep only two values for every state–item pair:.
先に定義した遷移関数をシンプルに表現すると、各状態-項目のペアに対して、次の2つの値しか保持しない。

$$
\tag{22}
$$

the probability that r will be bought if it appeared in the list of recommendations; and.
推奨リストに登場した場合にrが購入される確率、である。

$$
\tag{23}
$$

the probability that r will be bought if it did not appear in the list..
リストに掲載されなかった場合、rが購入される確率が高い。

As before, trMDP(s,r ∈/ R,s·r) does not depend on r, and will not depend on R in the discussion that follows.
先ほどと同様に、trMDP(s,r∈)
We note again, that these values are merely reasonable initial values and are adjusted by our system based on actual user behavior, as we shall discuss..
なお、これらの値はあくまで妥当な初期値であり、実際のユーザーの行動に基づいてシステムで調整されることは、後述するとおりです。

## 5.2. Solving the MDP MDPを解く。

Having defined the MDP, we now consider how to solve it in order to obtain an optimal policy.
MDPを定義した上で、最適な政策を得るためにどのように解くかを考える。
Such a policy will, in effect, tell us what item to recommend given any sequence of user purchases.
このようなポリシーは、事実上、ユーザーが購入した商品の中から、どの商品を推奨するかを教えてくれるものです。
For the domains we studied, we found policy iteration (Howard, 1960)—with a few approximations to be described—to be a tractable solution method.
私たちが研究した領域では、政策的反復（Howard, 1960）-いくつかの近似を説明する-が扱いやすい解法であることがわかった。
In fact, on tests using real data, we found that policy iteration terminates after a few iterations.
実際、実データを使ったテストでは、ポリシーの反復が数回で終了してしまうことがわかりました。
This stems from the special nature of our state space and the approximations we make, as we now explain..
これは、これから説明するように、状態空間とその近似の特殊性に起因しています。

Our state space enjoys a number of features that lead to fast convergence of the policy iteration algorithm:.
この状態空間は、政策反復アルゴリズムの高速収束につながる以下のような特徴を備えています。

Directionality.
指向性です。
Transitions in our state space seem to have inherent directionality: First, a state representing a short sequence cannot follow a state representing a longer sequence.
状態空間における遷移には、固有の方向性があるようです。まず、短い配列を表す状態が、長い配列を表す状態に続くことはない。
Second, the success of the sequential prediction model indicates that typically, if x is likely to follow y, y is less likely to follow x – otherwise, the sequence x, y and y, x would have similar probabilities, and we could simply use sets.
第二に、順序予測モデルの成功は、典型的には、xがyに続く可能性が高い場合、yはxに続く可能性が低いことを示している - そうでなければ、順序x、yとy、xは同様の確率を持ち、単にセットを使用することができるだろう。
Thus, loops, which in principle could occur in our MDP model because we maintain only a limited amount of history, are not very likely.
このように、MDPモデルでは限られた量の履歴しか保持しないため、原理的に起こりうるループはあまり起こりません。
Indeed, an examination of the loops in our state space graph reveals them to be small and scarce.
実際、状態空間グラフのループを調べると、ループは小さく希少であることがわかります。
Moreover, in the web site implementation, it is easy enough to filter out items that were already bought by the user from our list of recommendations.
さらに、Webサイトの実装では、ユーザーがすでに購入したアイテムをおすすめリストからフィルタリングすることも簡単です。
It is well-known that directionality can be used to reduce the running time of MDP solution algorithm (for example, Bonet and Geffner (2003))..
MDP解法アルゴリズムの実行時間を短縮するために方向性を利用できることはよく知られている（例えば、Bonet and Geffner (2003) など）。

Insensitivity to k.
kに対する不感症。
We have also found that the computation of an optimal policy is not heavily sensitive to variations in k—the number of past transactions we encapsulate in a state.
また、最適なポリシーの計算は、1つの状態にカプセル化された過去のトランザクションの数であるkの変動に大きく影響されないことも分かっています。
As k increases, so does the number of states, but the number of positive entries in our transition matrix remains similar.
kが大きくなると状態の数も増えますが、遷移行列の正のエントリーの数は変わりません。
Note that, at most, a state can have as many successors as there are items.
なお、1つの状態は、せいぜいアイテムの数だけ後継者を持つことができる。
When k is small, the number of observed successors for a state can be large.
kが小さいと、ある状態に対して観測される後継者の数が多くなることがある。
When k grows, however, the number of successors decreases considerably.
しかし、kが大きくなると、後継者の数が大幅に減少する。
Table 2 demonstrates this relation in our implemented model..
表2は、この関係を我々の実装モデルで示したものである。

Despite these properties of the state space, policy evaluation still requires much effort given the large state and action space we have to deal with.
このような状態空間の特性にもかかわらず、扱うべき状態空間と行動空間が大きいため、政策評価には多くの労力が必要です。
To alleviate this problem we resort to a number of approximations..
この問題を解決するために、いくつかの近似に頼ることになる。

Ignoring Unobserved States.
観察されない状態を無視する。
The vast majority of states in our models do not correspond to sequences that were observed in our training set because most combinations of items are extremely unlikely.
ほとんどのアイテムの組み合わせは極めてあり得ないため、モデルの状態の大部分は、トレーニングセットで観察されたシーケンスに対応しない。
For example, it is unlikely to find adjacent purchases of a science-fiction and a gardening book.
例えば、SFとガーデニングの本が隣接して購入されることはまずないでしょう。
We leverage this fact to save both space and computation time.
この事実を利用して、スペースと計算時間の両方を節約しています。
First, we maintain transition probabilities only for states for which a transition occurred in our training data.
まず、学習データで遷移が発生した状態のみ遷移確率を保持するようにしました。
These transitions correspond to pairs of states of the form s and s·r.
これらの遷移は、sとs-rという形の状態のペアに対応しています。
Thus, the number of transitions required per state is bounded by the number of items rather than by an amount exponential in k in the worst case.
したがって、1つの状態に必要な遷移の数は、最悪の場合、kの指数関数的な量ではなく、アイテムの数によって制限されるのである。
The non-zero transitions are stored explicitly, and as can be inferred from Table 2, their number is much smaller than the total number of entries in the explicit transition matrix.
非ゼロ遷移は明示的に保存され、表2から推測できるように、その数は明示的遷移行列の総エントリ数よりはるかに少ない。
And while much memory is still required, in Section 6.2, we show that these requirements are not too large for modern computers to handle..
また、多くのメモリが必要であるが、6.2節では、これらの要件は現代のコンピュータが扱うには大きすぎないことを示す。

Moreover, we do not compute a policy choice for a state that was not encountered in our training data.
また、訓練データで遭遇しなかった状態に対する政策選択を計算することはない。
When the value of such a state is needed for the computation of an optimal policy of some observed state, we simply use its immediate reward.
このような状態の値が、ある観測された状態の最適なポリシーの計算に必要な場合、単にその即時報酬を使用します。
That is, if the sequence hx, y,zi did not appear in the training data, we do not calculate a policy for it and assume its value to be R(z)—the reward for the last item in the sequence.
つまり、hx,y,ziというシーケンスが学習データに現れなかった場合、そのポリシーは計算せず、その値をR(z)（シーケンスの最後のアイテムの報酬）と仮定するのである。
Note that given the skipping and clustering methods we use, the probability of making a transition from some (observed) sequence hw, x, yi to hw, x, yi is not zero even though hx, y,zi was never observed.
なお、スキップやクラスタリングの手法を用いると、ある（観測された）シーケンスhw, x, yiからhw, x, yiへ遷移する確率は、hx, y,zi が一度も観測されていなくてもゼロにはならない。
This approximation, although risky in general MDPs, is motivated by the fact that in our initial model, for each state there is a relatively small number of items that are likely to be selected; and the probability of making a transition into an un-encountered state is very low.
この近似は、一般的なMDPでは危険だが、今回の初期モデルでは、各状態で選択されそうな項目が比較的少なく、未遭遇の状態に遷移する確率が非常に低いという事実に動機づけられている。
Moreover, the reward (that is, profit) does not change significantly across different states, so, there are no “hidden treasures” in the future that we could miss..
しかも、州によって報酬（つまり利益）が大きく変わるわけではないので、将来を見逃してしまうような「隠し玉」は存在しないのです。

When a recommendation must be generated for a state that was not encountered in the past, we compute the value of the policy for this state online.
過去に遭遇していない状態に対して推薦文を生成する必要がある場合、この状態に対するポリシーの値をオンラインで計算する。
This requires us to estimate the transition probabilities for a state that did not appear in our training data.
そのため、学習データに現れていない状態の遷移確率を推定する必要がある。
We handle such new states in the same manner that we handled states for which we had sparse data in the initial predictive model – that is, using the techniques of skipping, clustering, and finite mixture of unigram, bigram, and trigrams described in Section 3.2..
このような新しい状態は、最初の予測モデルでデータが疎な状態を扱ったのと同じ方法で、つまり、セクション3.2で説明したスキップ、クラスタリング、ユニグラム、ビッググラム、トリグラムの有限混合という手法で扱われるのです。

Using the Independence of Recommendations.
レコメンデーションの独立性を利用する。
One of the basic steps in policy iteration is policy determination.
政策反復の基本的なステップのひとつに、政策決定がある。
At each iteration, we compute the best action for each state s – that is, the action satisfying:.
各反復において、各状態sに対する最適なアクションを計算する、つまり、以下を満たすアクションを計算する。

$$
\tag{24}
$$

where tr(s,r ∈ R,s·r) and tr(s,r ∈/ R,s·r) follow the definitions above..
ここで、tr（s，r∈R，s-r）およびtr（s，r∈R，s-r）である。

The above equation requires maximization over the set of possible recommendations for each state.
上記の式は、各状態に対して可能な推奨事項のセットに対する最大化を要求している。
The number of possible recommendations is n κ , where n is the number of items and κ is the number of items we recommend each time.
推薦可能な数はn κ 、ここでnはアイテムの数、κは毎回推薦するアイテムの数である。
To handle this large action space, we make use of our independence assumption.
この大きな行動空間を扱うために、私たちは独立性の仮定を利用する。
Recall that we assumed that the probability that a user buys a particular item depends on her current state, the item, and whether or not this item is recommended.
ユーザーが特定の商品を購入する確率は、ユーザーの現在の状態、その商品、そしてその商品が推奨されているか否かに依存すると仮定したことを思い出してください。
It does not depend on the identity of the other recommended items.
他の推奨アイテムの同一性には依存しません。
The following method uses this fact to quickly generate an optimal set of recommendations for each state..
次の方法は、この事実を利用して、各状態に最適な推薦文のセットを素早く生成するものです。

Let us define ∆(s,r) – the additional value of recommending r in state s:.
ここで、△（s,r）-状態sにおいてrを推奨することの付加価値-と定義する：。

$$
\tag{25}
$$

Now define.
では、定義します。

$$
\tag{26}
$$

R s,κ max∆ is the set of κ items that have the maximal ∆(s,r) values..
R s,κ max△は、△(s,r)の値が最大となるκ個のアイテムの集合である。

Theorem 1 R s,κ max∆ is the set that maximizes Vi+1(s) – that is,.
定理1 R s,κ max△は、Vi+1(s)を最大化する集合である、つまり。

$$
\tag{27}
$$

Proof.
証明する。

Let us assume that there exists some other set of κ recommendations R 6= R s,κ max∆ that maximizes Vi+1(s).
ここで、Vi+1(s)を最大化するκ推奨R 6= R s,κ max△の他の集合が存在すると仮定する。
For simplicity, we shall assume that all ∆ values are different.
簡単のため、△の値はすべて異なると仮定する。
If that is not the case, then R should be a set of recommendations not equivalent to R s,κ max∆ .
そうでない場合、R は R s,κ max∆ と等価でない推薦文の集合であるべきです。
Let r be an item in R but not in R s,κ max∆ , and r 0 be an item in R s,κ max∆ but not in R.
rをRに含まれるがR s,κ max△に含まれない項目、r 0をR s,κ max△に含まれるがRに含まれない項目とする。
Let R 0 be the set we get when we replace r with r 0 in R.
Rのrをr 0に置き換えたときに得られる集合をR 0とする。
We need only show that Vi+1(s,R) < Vi+1(s,R 0 ):.
Vi+1(s,R) < Vi+1(s,R 0 ): を示せばよい。

$$
\tag{28}
$$

To compute Vi+1(s) we therefore need to compute all ∆(s,r) and find R s,κ max∆ , making the computation of Vi+1(s) independent of the number of subsets (or even worse—ordered subsets) of κ items.
したがって、Vi+1(s)を計算するためには、すべての△(s,r)を計算し、R s,κ max△を求める必要があり、Vi+1(s)の計算はκ項目の部分集合（あるいはさらに悪い順の部分集合）の数とは無関係となる。
The complexity of finding an optimal policy when recommending multiple items at each stage under our assumptions remains the same as the complexity of computing an optimal policy for single item recommendations..
本仮定の下で、各ステージで複数のアイテムを推奨する場合の最適なポリシーを見つける複雑さは、単一のアイテムを推奨する場合の最適なポリシーを計算する複雑さと変わりません。

By construction, our MDP optimizes site profits.
このように、私たちのMDPは、サイトの利益を最適化します。
In particular, the system does not recommend items that are likely to be bought whether recommended or not, but rather recommends items whose likelihood of being purchased is increased when they are recommended.
特に、推薦してもしなくても買われる可能性が高いものを推薦するのではなく、推薦すると買われる可能性が高くなるものを推薦するようにしました。
Nonetheless, when recommendations are based solely on lift, it is possible that many recommendations will be made for which the absolute probability of a purchase (or click) is small.
しかし、リフトだけでレコメンドすると、購入（クリック）される絶対確率が低いレコメンドが多くなる可能性があります。
In this case, if recommendations are seldom followed, users might start ignoring them altogether, making the overall benefit zero.
この場合、推奨事項がほとんど守られないと、ユーザーはそれを完全に無視するようになり、全体の利益はゼロになってしまうかもしれません。
Our model does not capture such effects.
私たちのモデルは、そのような効果を捉えていません。
One way to remedy this possible problem is to alter the reward function so as to provide a certain immediate reward for the acceptance of a recommendation.
このような問題を解決する一つの方法として、推薦を受けるとすぐに一定の報酬が得られるように報酬機能を変更することが考えられる。
Another way to handle this problem is to recommend a book with a large MDP score only if the probability of buying it passes some threshold.
この問題を扱う別の方法として、MDPスコアが大きい本を購入する確率がある閾値を超えた場合にのみ推薦する方法があります。
We did not find it necessary to introduce these modifications in our current system..
現在のシステムでは、このような改良を加える必要はないと考えています。

## 5.3. Updating the Model Online オンラインでモデルを更新する。

Once the recommender system is deployed with its initial model, we need to update the model according to actual observations.
レコメンダーシステムが初期モデルで展開された後は、実際の観測結果に応じてモデルを更新する必要があります。
One approach is to use some form of reinforcement learning— methods that improve the model after each recommendation is made.
強化学習と呼ばれる、推薦が行われるたびにモデルを改良していく方法を用いるのも一つの方法です。
Although such models need little administration to improve, the implementation requires many calls and computations by the recommender system online, which will lead to slower responses—an undesirable result.
このようなモデルは、改良のための管理はほとんど必要ありませんが、その実装には、レコメンダーシステムがオンラインで多くの呼び出しと計算を行う必要があり、レスポンスが遅くなるという好ましくない結果を招きます。
A simpler approach is to perform off-line updates at fixed time intervals.
よりシンプルな方法として、一定の時間間隔でオフラインの更新を行う方法があります。
The site need only keep track of the recommendations and the user selections and, say, once a week use those statistics to build a new model and replace it with the old one.
サイトでは、レコメンデーションとユーザーの選択を記録し、例えば週に一度、それらの統計情報を使って新しいモデルを構築し、古いモデルと置き換えるだけでいいのです。
This is the approach we used..
このようなアプローチで臨みました。

In order to re-estimate the transition function the following counts are obtained from the recently collected statistics:.
遷移関数を再推定するために、最近収集した統計から以下のカウントを取得した。

- cin(s,r,s·r)—the number of times the r recommendation was accepted in state s. cin(s,r,s-r)-状態sでrの推薦が受け入れられた回数です。

- cout(s,r,s·r)—the number of times the user took item r in state s even though it was not recommended, cout(s,r,s-r)-状態sにおいて、推奨されていないにもかかわらず、ユーザーがアイテムrを取った回数、。

- ctotal(s,s·r)—the number of times a user took item r while being in state s, regardless of whether it was recommended or not. ctotal(s,s-r)-ユーザーが状態sの時にアイテムrを摂取した回数（推奨されたか否かに関わらず）。

We compute the new counts and the new approximation for the transition function at time t +1 based on the counts and probabilities at time t as follows:.
時刻tのカウントと確率に基づいて、時刻t +1の新しいカウントと遷移関数の新しい近似を次のように計算する。

$$
\tag{29}
$$

Note that at this stage the constants αs,r and βs,r no longer play a role—they were used only to generate the initial model.
この段階では、定数αs,rとβs,rはもはや役割を果たさず、初期モデルの生成にのみ使用されたことに注意してください。
We still need to define how the counts at time t = 0 are initialized.
時刻t = 0のカウントがどのように初期化されるかを定義する必要があります。
We showed in section 5.1.1 how the transition function tr is initialized, and now we define:.
5.1.1節で遷移関数trの初期化方法を示したが、ここでは次のように定義する。

$$
\tag{34}
$$

where ξs is proportional to the number of times the state s was observed in the training data (in our implementation we used 10 · count(s)).
ここで、ξsは学習データで状態sが観測された回数に比例する（我々の実装では、10 - count(s)を使用）。
This initialization causes states that were observed infrequently to be updated faster than states that were observed frequently and in whose estimated transition probabilities we have more confidence.10.
この初期化により、観測頻度の低い状態は、観測頻度が高く、推定遷移確率に信頼性がある状態よりも速く更新される。

To ensure convergence to an optimal solution, the system must obtain accurate estimates of the transition probabilities.
最適解に収束させるためには、システムは遷移確率の正確な推定値を得る必要があります。
This, in turn, requires that for each state s and for every recommendation r, we observe the response of users to a recommendation of r in state s sufficiently many times.
そのためには、各状態sと各推薦rについて、状態sにおけるrの推奨に対するユーザの反応を十分な回数観察する必要がある。
If at each state the system always returns the best recommendations only, then most values for count(s,r,s·r) would be 0, because most items will not appear among the best recommendations.
もし、各状態で常にベストレコメンデーションのみを返すシステムであれば、ほとんどのアイテムがベストレコメンデーションに含まれないため、count(s,r,s-r)の値は0となります。
Thus, the system needs to recommend non-optimal items occasionally in order to get counts for those items.
そのため、最適でないアイテムを推奨することで、そのアイテムのカウントを獲得する必要があるのです。
This problem is widely known in computational learning as the exploration versus exploitation tradeoff (for some discussion of learning rate decay and exploration vs.
この問題は、計算機学習において、探索と利用のトレードオフとして広く知られている（学習率の減衰と探索と利用のトレードオフに関するいくつかの議論については、こちら）。
exploitation in reinforcement learning, see, for example Kaelbling et al.
強化学習での活用は、例えばKaelbling et al.
(1996) and Sutton and Barto (1998)).
(1996)、Sutton and Barto(1998))がある。
The system balances the need to explore unobserved options in order to improve its model and the desire to exploit the data it has gathered so far in order to get rewards..
このシステムは、モデルを改良するために未観測のオプションを探索する必要性と、報酬を得るためにこれまでに収集したデータを利用する必要性のバランスをとっています。

One possible solution is to select some constant ε, such that recommendations whose expected value is ε-close to optimal will be allowed—for example, by following a Boltzmann distribution:.
一つの可能な解決策は、ある定数εを選択することで、期待値がεに近いレコメンデーションは、例えば、ボルツマン分布に従うことで、最適になるようにすることである：。

$$
\tag{37}
$$

with an ε cutoff—meaning that only items whose value is within ε of the optimal value will be allowed.
を設定し、その値が最適値からε以内にある項目のみを許可することを意味する。
The exact value of ε can be determined by the site operators.
εの正確な値は、サイト運営者が決定することができます。
The price of such a conservative exploration policy is that we are not guaranteed convergence to an optimal policy.
このような保守的な探査方針の代償として、最適な方針への収束が保証されないことが挙げられます。
Another possible solution is to show the best recommendation on the top of the list, but show items less likely to be purchased as the second and third items on the list.
また、一番お勧めの商品をリストの一番上に表示し、購入の可能性が低いものをリストの2番目、3番目に表示する方法も考えられます。
In our implementation we use a list of three recommendations where the first one is always the optimal one, but the second and third items are selected using the Boltzman distribution without a cutoff..
我々の実装では、3つの推薦リストを使用し、最初のものは常に最適なものであるが、2番目と3番目の項目は、カットオフなしでボルツマン分布を用いて選択されるものである。

We also had to equip our system to change with frequent changes (for example, addition and removal of items).
また、頻繁な変更（例えば、項目の追加や削除など）に対応できるような装備にする必要がありました。
When new items are added, users will start buying them and positive counts for them will appear.
新しいアイテムが追加されると、ユーザーはそれを買い始め、そのアイテムのプラスカウントが表示されるようになります。
At this stage, our system adds new states for these new items, and the transition function is expanded to express the transitions for these new states.
この段階で、私たちのシステムは、これらの新しいアイテムのための新しい状態を追加し、これらの新しい状態のための遷移を表現するために遷移関数を拡張する。
Of course, prior to updating the model, the system is not able to recommend those new items (the well-known “cold start” problem (Good et al., 1999) in recommender systems).
もちろん、モデルを更新する前は、システムはそれらの新しいアイテムを推薦することができない（推薦システムにおけるよく知られた「コールドスタート」問題（Good et al.，1999））。
In our implementation, when the first transition to a state s·r is observed, its probability is initialized to 0.9 the probability of the most likely next item in state s with ξs = 10.
本実装では、状態s-rへの最初の遷移が観測されたとき、その確率は、状態sで最も可能性の高い次の項目の確率をξs = 10として、0.9に初期化される。
This approach causes the new items to be recommended quite frequently..
この方法だと、新しいアイテムが推奨される頻度が高くなりますね。

One possible approach to handling removed items is to do nothing to our system, in which case the transition probabilities slowly decay to zero.
削除されたアイテムを処理する方法として考えられるのは、システムに何もしないことであり、その場合、遷移確率はゆっくりとゼロに減衰する。
Using this approach, however, we may still insert deleted items into the list of recommended items – an undesirable feature.
しかし、この方法では、削除されたアイテムが推奨アイテムに挿入される可能性があり、好ましくない機能です。
Consequently, in our Mitos implementation, items are programmatically removed from the model during offline updates.
そのため、Mitosの実装では、オフラインアップデート時にアイテムをプログラムから削除しています。
Another solution that we have implemented but not evaluated is to use weighted data and to exponentially decay the weights in time, thus placing more weight on more recently observed transitions..
もう一つの解決策は、重み付けされたデータを使用し、時間的に指数関数的に減衰させることで、より最近観測された遷移に重きを置くというものです（評価はしていません）。

# 6. Evaluation of the MDP Recommender Model MDPレコメンダーモデルを評価する。

The main thesis of this work is that (1) recommendation should be viewed as a sequential optimization problem, and (2) MDPs provide an adequate model for this view.
本研究の主要なテーゼは、（1）推薦を逐次最適化問題として捉えるべきであり、（2）MDPはこの見解に適したモデルを提供する、というものである。
This is to be contrasted with previous systems which used predictive models for generating recommendations.
これは、従来のシステムが予測モデルを用いてレコメンデーションを生成していたのと対照的である。
In this section, we present an empirical validation of our thesis.
本節では、本論文の実証的な検証を紹介する。
We compare the performance of our MDP-based recommender system (denoted MDP) with the performance of a recommender system based on our predictive model (denoted MC) as well as other variants..
MDPに基づくレコメンダーシステム（MDPと表記）と、予測モデルに基づくレコメンダーシステム（MCと表記）、および他の変種との性能を比較しました。

Our studies were performed on the online book store Mitos (www.mitos.co.il) from August, 2002 till April, 2004.
2002年8月から2004年4月まで、オンライン書店「ミトス」（www.mitos.co.il）で調査を行いました。
During our evaluations, approximately 5000 − 6000 different users visited the Mitos site daily.
私たちの評価では、毎日約5000〜6000人のユーザーがミトスのサイトを訪れていました。
Of those, around 900 users inserted items into their basket, thus entering our data-set.11 On average, each customer inserted 1.97 items into the shopping basket.
このうち、約900人のユーザーが買い物かごに商品を入れ、データセットに登録されました。11 平均して、1人当たり1.97個の商品を買い物かごに入れました。
Over 15,000 items were available for purchase on the site..
サイトでは15,000点以上のアイテムが販売されていました。

Users received recommendations when adding items to the shopping cart.12 The recommendations were based on the last k items added to the cart ordered by the time they were added.
ショッピングカートに商品を追加する際に、ユーザーにおすすめの商品を紹介しました12。このおすすめ商品は、カートに追加された商品のうち、追加された時間順に並んだ直近のk個の商品に基づいています。
An example is shown in Figure 4 where the three book covers at the bottom are the recommended items.
例として、図4に示すように、下部の3つのブックカバーがおすすめアイテムであることを示します。
Every time a user was presented with a list of recommendations on either page, the system stored the recommendations that were presented and recorded whether the user purchased a recommended item.
どちらのページでも、ユーザーにおすすめ商品のリストが提示されるたびに、提示されたおすすめ商品を記憶し、ユーザーがおすすめ商品を購入したかどうかを記録しました。
Cart deletions were rare and ignored.
カートの削除は稀であり、無視された。
Once every two or three weeks, a process was run to update the model given the data that was collected over the latest time period.13.
2～3週間に一度、最新の期間に収集されたデータをもとに、モデルを更新するプロセスが実行された13。

We compared the MDP and MC models both in terms of their value or utility to the site as well as their computational costs..
MDPモデルとMCモデルを、現場での価値や有用性、計算コストの両面から比較検討しました。

## 6.1. Utility Performance ユーティリティの性能

Our first set of results is based on the assumption that the transition function we learn for our MDP using data collected with recommendations, provides the the best available model of user behavior under recommendation.
最初の結果は、レコメンデーションで収集されたデータを用いてMDPに学習させた遷移関数が、レコメンデーション下のユーザー行動の最良のモデルを提供するという仮定に基づいています。
Under this assumption, we can measure the effect of different recommendation policies.
この前提のもと、さまざまな推薦ポリシーの効果を測定することができます。
An important caveat is that the states in our MDP correspond to truncated (that is, last k) user sequences.
重要な注意点は、MDPの状態は切り捨てられた（つまり最後のk個の）ユーザーシーケンスに対応することである。
Thus, the model does not exclude repeated purchases of the same item.
したがって、このモデルでは、同じ商品の繰り返し購入は除外されない。
Despite this shortcoming, we proceeded with the evaluation..
このような欠点があるにもかかわらず、我々は評価を進めたのです。

As discussed above, a predictive model can answer queries in the form Pr(x|h)—the probability that item x will be purchased given user history h.
h)—the probability that item x will be purchased given user history h.
Recommender systems may employ different strategies when generating recommendations using such a predictive model.
リコメンダーシステムは、このような予測モデルを用いて推薦を生成する際に、異なる戦略を採用することができる。
Assuming that an MDP formalizes the recommendation problem well, we may use the learned MDP model to evaluate these strategies.
MDPが推薦問題をうまく定式化していると仮定すると、学習したMDPモデルを用いて、これらの戦略を評価することができる。
The evaluation of the quality of different possible policies for the MDP, each corresponding to a popular approach to recommending, may shed light on the preferred recommendation strategy..
MDPで考えられる様々な政策（それぞれ一般的な推薦のアプローチに対応する）の質を評価することで、好ましい推薦戦略を明らかにすることができるかもしれません。

The MDP model was built using data gathered while the model was running in the site with incremental updates (as described above) for almost a year.
MDPモデルは、約1年間、サイト内でインクリメンタルアップデート（上記のようなアップデート）を行いながら、収集したデータを使って構築しました。
We compared four policies, where the first policy uses information about the effect of recommendations, and the remaining policies are based on the predictive model solely:.
最初のポリシーはレコメンドの効果に関する情報を使用し、残りのポリシーは予測モデルのみに基づいている：4つのポリシーを比較しました。

- Optimal – recommends items based on optimal policy for the MDP. Optimal - MDPに最適なポリシーに基づいたアイテムを推奨します。

- Greedy – recommends items that maximize Pr(x|h)· R(x) (where Pr(x|h) is the probability of buying item x given user history h, and R(x) is the value of x to the site – for example, net profit). R(x) (where Pr(x

- Most likely – recommends items that maximize Pr(x|h).

- Lift – recommends items that maximize Pr(x|h) Pr(x) , where Pr(x) is the prior probability of buying item x. Pr(x) , where Pr(x) is the prior probability of buying item x..

To evaluate the different policies we ran a simulation of the interaction of a user with the system.
異なるポリシーを評価するために、ユーザーとシステムとのインタラクションのシミュレーションを実行しました。
During the simulation the system generated a list of recommended items R, from which the simulated user selected the next item, using the distribution tr(s,R,s· x)—the probability that the next selected item is x given the current state s and the recommendation list R, simulating the purchase of x by the user.
シミュレーション中、システムは推奨アイテムのリストRを生成し、そこから模擬ユーザーが次のアイテムを選択する。分布tr（s,R,s-x）-現在の状態sと推奨リストRが与えられたときに、次の選択アイテムがxである確率-を用いて、ユーザーによるx購入のシミュレーションをした。
The length of user session was taken from the learned distribution of user session length in the actual site.
ユーザーセッションの長さは、実際のサイトにおけるユーザーセッションの長さの学習済み分布から取得しました。
We ran the simulation for 10,000 iterations for each policy, and calculated the average accumulated reward for user session..
各ポリシーについて10,000回の反復シミュレーションを行い、ユーザーセッションの平均累積報酬を算出しました。

The results are presented in Table 3.
その結果を表3に示します。
The calculated value for each policy is the sum of discounted profit in (New Israeli Shekels) averaged over all states.
各保険の計算値は、全州で平均した（新イスラエル・シェケル）割引利益の合計です。
We used a weighted average, where the weight of each state was the probability of observing it.
各状態の重みを観測する確率とした加重平均を使用しました。
Obviously, an optimal policy results in the highest value.
当然ながら、最適なポリシーは最も高い値をもたらします。
However, the differences are small, and it appears that one can use the predictive model alone with very good results..
しかし、その差は小さく、予測モデルだけでも非常に良い結果が得られると思われます。

Next, we performed an experiment to compare the performance of the MDP-based system with that of the MC-based system.
次に、MDPベースのシステムとMCベースのシステムの性能を比較する実験を行いました。
In this experiment, each user entering the site was assigned a randomly generated cart-id.
この実験では、サイトに入る各ユーザーに、ランダムに生成されたカートIDが割り当てられました。
Based on the last bit of this cart-id, the user was provided with recommendations by the MDP or MC.
このcart-idの最終ビットに基づき、MDPまたはMCからユーザーにレコメンドが提供された。
Reported mean profits were calculated for each user session (a single visit to the site).
報告された平均利益は、ユーザーセッション（サイトへの1回の訪問）ごとに計算されました。
Data gathered in both cases was used to update both models.14.
この2つのケースで収集されたデータは、両モデルのアップデートに使用されました14。

The deployed system was built using three mixture components, with history length ranging from one to three for both the MDP model and the MC model.
展開されたシステムは、MDPモデル、MCモデルともに履歴長が1～3までの3つの混合コンポーネントを用いて構築された。
Recommendations from the different mixture components were combined using an equal (0.33) weight.
異なる混合成分からの勧告は、等しい（0.33）重量を使用して結合された。
We used the policy-iteration procedure and approximations described in Section 5 to compute an optimal policy for the MDP.
セクション5で説明した政策反復手順と近似を用いて、MDPの最適政策を計算した。
Our model encoded approximately 25,000 states in the two top mixture components (k = 2, k = 3).
我々のモデルでは、上位2つの混合成分（k = 2, k = 3）に約25,000の状態を符号化した。
The reported results were gathered after the model was running in the site with incremental updates (as described above) for almost a year..
今回発表された結果は、サイト内で約1年間、段階的なアップデート（上記のような）を行いながらモデルを稼働させた後に得られたものです。

During the testing period, 50.7% of the users who made at least one purchase were shown MDP-based recommendations and the other 49.3% of these users were shown MC-based recommendations.
テスト期間中、少なくとも1回購入したユーザーの50.7%にMDPベースのレコメンデーションが表示され、残りの49.3%にMCベースのレコメンデーションが表示されました。
For each user, we computed the average site profit per session for that user, leaving out of consideration the first purchase made in each session.
各ユーザーについて、各セッションで最初に購入されたものは考慮せず、そのユーザーのセッションごとの平均サイト利益を計算しました。
The first item was excluded as it was bought without the benefit of recommendations, and is therefore irrelevant to the comparison between the recommender systems.15.
最初の商品は、レコメンデーションの恩恵を受けずに購入したため、レコメンダーシステム間の比較には無関係であるとして除外した15。

The average site profit generated by the users was 28% higher for the MDP group.16 We used a permutation test (see, for example, Yeh (2000)) to see how likely it would be for a difference this large to emerge if there were in fact no systematic difference in the effectiveness of the two recommendation methods.17 We randomly generated 10000 permutations of the assignments of session profits to users, for each permutation computing the ratio of average session profits between the MDP and the MC groups.
セッション利益の割り当てをランダムに 10000 通り作成し，それぞれの順列について，MDP 群と MC 群の平均セッション利益の比率を計算した．
With only 8% of these random assignments was the ratio as large as (or larger than) 1.282.
このうち、1.282と同程度（またはそれ以上）の比率となったのは、わずか8％であった。
Therefore, the better performance of the MDP recommender is statistically significant with p = 0.08 by a one-tailed permutation test..
したがって、MDPレコメンダーの性能向上は、片側並べ替え検定でp = 0.08と統計的に有意であったことがわかる。

There are two possible sources for the observed improvement—the MDP may be generating more sales or sales of more expensive items.
MDPがより多くの売上を生み出しているか、より高価な商品の売上を生み出しているかの2つの可能性があるのです。
In our experiment, the average number of items bought per user session was 6.8% in favor of the MDP-based recommender (p = 0.15), whereas the average price of items was 4% higher in favor of the MDP-based recommender (p = 0.04).
実験では、ユーザーセッションあたりの平均購入アイテム数は、MDPベースのレコメンダーが6.8%有利であったのに対し（p = 0.15）、アイテムの平均価格はMDPベースのレコメンダーが4%有利であった（p = 0.04）．
Thus, both effects may have played a role..
したがって、両方の効果が作用している可能性があります。

In our second and last experiment, we compared site performance with and without a recommender system.
最後の2つ目の実験では、レコメンダーシステムを導入した場合と導入しない場合のサイトパフォーマンスを比較しました。
Ideally, we would have liked to assign users randomly to an experience with and without recommendations.
理想を言えば、レコメンデーションのある体験とない体験にランダムにユーザーを割り当てることができればよかったのですが。
This option was ruled-out by the site owner because it would have led to a non-uniform user experience.
この選択肢は、ユーザーエクスペリエンスが統一されないという理由で、サイトオーナーによって除外されました。
Fortunately, the site owner was willing to remove the recommender system from the site for one week.
幸い、サイトオーナーが1週間だけレコメンドシステムをサイトから外してくれることになった。
Thus, we were able to compare average profits per user session during two consecutive weeks – one with recommendations and one without recommendations.18 We found that, when the recommender system was not in use, average site profit dropped 17% (p = 0.0).
その結果、レコメンダーシステムを使用しない場合、サイトの平均利益は17%減少することがわかりました（p=0.0）。
Although, we cannot rule out the possibility that this difference is due to other factors (for example, seasonal effects or special events), these result are quite encouraging..
この差が他の要因（例えば、季節的な影響や特別なイベントなど）によるものである可能性は否定できませんが、この結果は非常に有望です。

Overall, our experiments support the claims concerning the added value of using recommendations in commercial web sites and the validity of the MDP-based model for recommender systems..
本実験は、商用サイトにおけるレコメンデーションの付加価値と、レコメンデーションシステムのためのMDPベースのモデルの有効性に関する主張を支持するものであった。

## 6.2. Computational Analysis Computational Analysis（計算解析）。

In this section, we compare computational costs of the MDP-based and the Predictor recommender system..
ここでは、MDPベースとPredictorレコメンダーシステムの計算コストを比較する。

Our comparison uses the transaction data set and corresponding models described in Section 4.
この比較では、セクション4で説明したトランザクションデータセットと対応するモデルを使用する。
In addition to using the full data set, we measured costs associated with smaller versions of the data in which transactions among only the the top N items were considered, in order to demonstrate the effect of the size of the data-set on performance..
また、データセットの規模がパフォーマンスに与える影響を示すため、フルセットに加えて、上位N項目のみの取引を考慮した小規模なデータセットに関連するコストを測定しました。

First, let us consider the time it takes to make a recommendation.
まず、推薦にかかる時間について考えてみましょう。
Recommendation time is typically the most critical of computational costs.
レコメンデーション時間は、一般的に計算コストの中で最も重要なものです。
If recommendation latency is noticeable, no reasonable site administrator will use the recommender system.
レコメンデーションの遅延が目立つようでは、合理的なサイト管理者はレコメンダーシステムを利用しないでしょう。
Table 5 shows the number of recommendations generated per second by the recommender system.
表5は、レコメンダーシステムが1秒間に生成するレコメンド数を示しています。
The results show that the MDP model is faster.
その結果、MDPモデルの方が高速であることがわかりました。
This result is due to the fact that, with the MDP model, we do almost no computations online.
この結果は、MDPモデルで、オンラインでほとんど計算をしないことに起因しています。
While predicting, the model simply finds the proper state and returns the state’s pre-calculated list of recommendations..
予測中は、モデルは単に適切な状態を見つけ、その状態の事前に計算された推奨リストを返します。

The price paid for faster recommendation is a larger memory footprint.
より高速な推薦のために支払われる代償は、より大きなメモリフットプリントです。
Table 6 shows the amount of memory needed to build and store a model in megabytes.
表6に、モデルの構築と保存に必要なメモリ量をメガバイトで示します。
The MDP model requires more memory to store than the Predictor model, due to the structured representation of the Predictor model using a collection of decision trees..
MDPモデルはPredictorモデルより多くのメモリを必要としますが、これはPredictorモデルが決定木の集合体を用いて構造的に表現されているためです。

Finally, we consider the time needed to build a new model.
最後に、新しいモデルを構築するのに必要な時間を考慮します。
This computational cost is perhaps the least important parameter when selecting a recommender system, as model building is an offline task executed at long time intervals (say once a week at most) on a machine that does not affect the performance of the site.
モデル構築は、サイトのパフォーマンスに影響を与えないマシンで、長い時間間隔（せいぜい週に1回程度）で実行されるオフラインタスクであるため、この計算コストは、レコメンダーシステムを選択する際に最も重要ではないパラメータと言えるかもしれません。
That being said, as we see in Table 4, the MDP model has the smallest build times..
とはいえ、表4にあるように、MDPモデルは構築時間が最も短い。

Overall the MDP-based model is quite competitive with the Predictor model.
全体的にMDPベースのモデルは、Predictorモデルとかなり競合しています。
It provides the fastest recommendations at the price of more memory use, and builds models more quickly.
より多くのメモリを使用する代償として最速のレコメンデーションを提供し、より速くモデルを構築します。

# 7. Discussion ディスカッション

This paper describes a new model for recommender systems based on an MDP.
本論文では、MDPに基づくレコメンダーシステムの新しいモデルについて説明する。
Our work presents one of a few examples of commercial systems that use MDPs, and one of the first reports of the performance of commercially deployed recommender system.
私たちの研究は、MDPを用いた商用システムの数少ない例の一つであり、商用に展開されたレコメンダーシステムの性能に関する最初の報告の一つでもあります。
Our experimental results validate both the utility of recommender systems and the utility of the MDP-based approach to recommender systems..
この実験結果は、推薦システムの有用性と推薦システムに対するMDPベースのアプローチの有用性の両方を検証するものである。

To provide the kind of performance required by an online commercial site, we used various approximations and, in particular, made heavy use of the special properties of our state space and its sequential origin.
オンライン商業サイトに求められる性能を実現するために、さまざまな近似式を用い、特に状態空間の特殊な性質とその逐次的な起源を大いに利用しました。
Whereas the applicability of these techniques beyond recommender systems is not clear, it represents an interesting case study of a successful real system.
これらの技術のレコメンダーシステム以外への適用性は明確ではありませんが、実際のシステムの成功例として興味深い事例です。
Moreover, the sequential nature of our system stems from the fact that we need to maintain history of past purchases in order to obtain a Markovian state space.
また、本システムの逐次性は、マルコフの状態空間を得るために、過去の購入履歴を保持する必要があることに起因しています。
The need to record facts about the past in the current state arises in various domains, and has been discussed in a number of papers on handling non-first-order Markov reward functions (see, for example, Bacchus et al.
過去に関する事実を現在の状態に記録する必要性は様々なドメインで生じ、非一次マルコフ報酬関数の取り扱いに関する多くの論文で議論されてきた（例えば、Bacchus et al.
(1996) or Thiebaux et al.
(1996)やThiebaux et al.
(2002))..
(2002))..

Another interesting technique is our use of off-line data to initialize a model that can provide adequate initial performance..
また、オフラインのデータを使ってモデルを初期化することで、十分な初期性能を発揮させるという手法も興味深い。

In the future, we hope to improve our transition function on those states that are seldom encountered using generalization techniques, such as skipping and clustering, that are similar to the ones we employed in the predictive Markov chain model.
今後は、予測マルコフ連鎖モデルで採用したようなスキップやクラスタリングなどの汎化手法を用いて、めったに遭遇しないような状態の遷移関数を改善したいと考えています。
Other potential improvements are the use of a partially observable MDP to model the user.
その他の改善点として、ユーザーをモデル化するために部分観測可能なMDPを使用することが考えられます。
As a model, this is more appropriate than an MDP, as it allows us to explicitly model our uncertainty about the true state of the user (Boutilier, 2002)..
モデルとしては、ユーザーの真の状態に関する不確実性を明示的にモデル化できるため、MDPよりも適切である（Boutilier, 2002）。

In fact, our current model can be viewed as approximating a particular POMDP by using a finite – rather than an unbounded – window of past history to define the current state.
実際、現在のモデルは、現在の状態を定義するために過去の履歴のウィンドウを無制限ではなく、有限のウィンドウを使用することで、特定のPOMDPを近似していると見なすことができます。
Of course, the computational and representational overhead of POMDPs are significant, and appropriate techniques for overcoming these problems must be developed..
もちろん、POMDPの計算量や表現力のオーバーヘッドは大きく、これらの問題を克服するための適切な技術の開発が必要である。

Weaknesses of our predictive (Markov chain) model include the use of ad hoc weighting functions for skipping and similarity functions and the use of fixed mixture weights.
予測（マルコフ連鎖）モデルの弱点として、スキップや類似関数にアドホックな重み付け関数を使用していること、混合物の重みが固定であることが挙げられます。
Although the recommendations that result from our current model are (empirically) useful for ranking items, we have noticed that the model probability distributions are not calibrated.
現在のモデルから得られるレコメンデーションは、（経験的に）アイテムのランキングに有用ですが、モデルの確率分布が較正されていないことに気づきました。
Learning the weighting functions and mixture weights from data should improve calibration.
データから重み付け関数や混合重みを学習することで、キャリブレーションを向上させることができるはずです。
In addition, in informal experiments, we have seen evidence that learning case-dependent mixture weights should improve predictive accuracy..
また、非公式な実験では、ケースに依存した混合重みを学習することで、予測精度が向上することが確認されています。

Our predictive model should also make use of relations between items that can be explicitly specified.
予測モデルは、明示的に指定できる項目間の関係も利用する必要があります。
For example, most sites that sell items have a large catalogue with hierarchical structure such as categories or subjects, a carefully constructed web structure, and item properties such as author name.
例えば、物品を販売するサイトの多くは、カテゴリーやテーマなどの階層構造、綿密に構築されたウェブ構造、著者名などのアイテムプロパティを持つ大規模なカタログを用意しています。
Finally, our models should incorporate information about users such as age and gender..
最後に、年齢や性別など、ユーザーに関する情報をモデルに取り込む必要があります。
