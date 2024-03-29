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
さらに、**ほとんどのstate、つまりほとんどのitem逐次配列が非常に起こりにくいという事実を利用した近似**を導入する（詳細な説明は第3節に続く）.

MDPs extend the simpler Markov chain (MC) model – a well known model of dynamic systems.
MDPは、動的システムのモデルとしてよく知られている、より単純なマルコフ連鎖(MC)モデルを拡張したものである.
A Markov chain is simply an MDP without actions.
**マルコフ連鎖とは、単純にactionを含まないMDPのこと**である.
It contains a set of states and a stochastic transition function between states.
これは、**stateの集合とstate間の確率的遷移関数(stochastic transition function)を含んでいる**.
In both models the next state does not depend on any states other than the current state..
**どちらのモデルでも、次のstateは現在のstate以外のstateには依存しない**.(なるほど! 次のstateは直近のstateのみに依存するんだ!)

In the context of recommender systems, if we equate actions with recommendations, then an MDP can be used to model user behavior with recommendations – as we show below – whereas an MC can be used to model user behavior without recommendations.
推薦システムの文脈では、**actionと推薦を同一視すると**、以下に示すように、**MDPは推薦を伴うユーザのactionをモデル化するのに使用**でき、**MCは推薦を伴わないユーザの行動をモデル化するのに使用できる**ことになる.
Markov chains are also closely related to n-gram models.
マルコフ連鎖は、n-gramモデルとも密接な関係がある.
In a bi-gram model, the choice of the next word depends probabilistically on the previous word only.
bi-gramモデル(n=binaryのケース?)では、**次の単語の選択は、前の単語のみに確率的に依存する**.
Thus, a bi-gram is simply a first-order Markov chain whose states correspond to words.
したがって、**bi-gramは、単に、stateが単語に対応する一次マルコフ連鎖**である。
An n-gram is a n−1-order Markovian model in which the next state depends on the previous n − 1 states.
**n-gramは、次の状態が前のn - 1個の状態に依存するn-1次マルコフモデル**である.
Such variants of MDP-models are well known.
このようなMDPモデルの変種はよく知られている.
A non-first-order Markovian model can be converted into a first-order model by making each state include information related to the previous n−1 states.
非一次マルコフモデルは、**各stateが前のn-1個のstateに関連する情報を含むようにすることで、一次モデルに変換**することができる.($s_{t-1}$から$s_{t-n+1}$までの情報を含んだ一つのstate $s'_{t-1}$ とみなすイメージ??)
More general transformation techniques that attempt to reduce the size of the state space have been investigated in the literature (for example, see Bacchus et al.
state空間のサイズを小さくしようとする、より一般的な変換技術が文献で研究されている（例えば、Bacchus et al.(1996); Thiebaux et al.(2002);

# 3. The Predictive Model 予測モデル

Our first step is to construct a predictive model of user purchases, that is, a model that can predict what item the user will buy next.
まず、ユーザの購買予測モデル、つまり、ユーザが次にどのようなアイテムを購入するかを予測できるモデルを構築する.
This model does not take into account its influence on the user, as it does not model the recommendation process and its effects.
このモデルでは、推薦のプロセスやその効果をモデル化していないため、ユーザへの影響を考慮していない.
Nonetheless, we shall use a Markov chain, with an appropriate formulation of the state space, as our model.
それでも、**状態空間(state space)を適切に定式化したマルコフ連鎖をモデルとして使用することにする**.
In Section 4 we shall show that our predictive model outperforms previous models, and in Section 5 we shall intialize our MDP-based recommender system using this predictive model..
第4節では、本予測モデルが従来のモデルを凌駕することを示し、第5節では、**本予測モデルを用いたMDPベースのレコメンダーシステムの初期化**について述べる.

## 3.1. The Basic Model 基本モデル

A Markov chain is a model of system dynamics – in our case, user “dynamics.” To use it, we need to formulate an appropriate notion of a user state and to estimate the state-transition function..
マルコフ連鎖は、システムのダイナミクス（ここではユーザの "ダイナミクス"）をモデル化したものである. マルコフ連鎖を利用するためには、**ユーザのstateに関する適切な概念を定式化**し、 **state-transition function を推定することが必要**である.

### States.

The states in our MC model represent the relevant information that we have about the user.
MCモデルの state は、ユーザについて我々が持っている関連情報を表している.
This information corresponds to previous choices made by users in the form of a set of ordered sequences of selections.
この情報は、**ユーザが過去に行った選択に対応するもの(="どのアイテムを買った"みたいなログ...?)で、順序付けられた選択順序(sequences)の集合**の形をしている.
We ignore data such as age or gender, although it could be beneficial.3 Thus, the set of states contains all possible sequences of user selections.
**年齢や性別のようなデータは、有益である可能性があるが、無視する**. したがって、state のセットは、ユーザの選択のすべての可能な sequences を含む.
Of course, this formulation leads to an unmanageable state space with the usual associated problems—data sparsity and MDP solution complexity.
もちろん、この定式化は、 データスパース性 と MDP解の複雑さ という、通常の関連問題を伴う扱いにくい state space をもたらす.
To reduce the size of the state space, we consider only sequences of at most k items, for some relatively small value of k.
state space のサイズを小さくするために、 $k$ の値が比較的小さい場合、最大で $k$ 個のアイテムの sequences のみを考慮する.
We note that this approach is consistent with the intuition that the near history (for example, the current user session) often is more relevant than selections made less recently (for example, past user sessions).
このアプローチは、近い履歴(ex. 現在のユーザセッション)は、より最近(ex. 過去のユーザセッション)に選択されたものよりも関連性が高いことが多いという直観と一致することに留意されたい.
These sequences are represented as vectors of size k.
**これらの配列(sequences)は、サイズ$k$のベクトルとして表現される**.
In particular, we use $<x_1, \cdots,x_k>$ to denote the state in which the user’s last k selected items were $x_1, \cdots x_k$.
特に、**ユーザの直近のk個の選択アイテムが $x_1, \cdots, x_k$ であった状態を $<x_1, \cdots, x_k>$ と表現する**.
Selection sequences with l < k items are transformed into a vector in which x1 through xk−l have the value missing.
$l＜k$ 個の選択配列(=直近の選択アイテム数がk個に満たない場合!)は、$x_1$ ~ $x_{k-l}$の値がmissingとなるベクトルに変換される.
The initial state in the Markov chain is the state in which every entry has the value missing.
**マルコフ連鎖の初期状態は、すべてのエントリーがvalue missingを持つ状態**である.
In our experiments, we used values of k ranging from 1 to 5..
実験では、kの値を1～5まで使用した.

### The state-Transition Function.

The transition function for our Markov chain describes the probability that a user whose k recent selections were x1,...,xk will select the item x 0 next, denoted trMC(hx1, x2,...,xki,hx2,...,xk, x 0 i).
**マルコフ連鎖の transition function は、直近 k 回選択したアイテムが $x_1,\cdots, x_k$ であるユーザが、次に $x'$ を選択する確率を記述**し、$tr_{MC}(<x_1, x_2, \cdots, x_k>, <x_2,\cdots, x_k, x'>)$と表記される.
Initially, this transition function is unknown to us; and we would like to estimate it based on user data.
この transition function は、当初は未知であり、ユーザデータに基づいて推定したい.
As mentioned, a maximum-likelihood estimate can be used:.
前述したように、最尤推定を使用することができる：

$$
tr_{MC}(<x_1, x_2, x_3>, <x_2,x_3, x_4>) = \frac{const(<x_1, x_2, x_3, x_4>)}{const(<x_1, x_2, x_3>)}
\tag{5}
$$

where $const(<x_1, x_2, x_3, x_4>)$ is the number of times the sequence x1, x2,...,xk was observed in the data set.
ここで、$const(<x_1, x_2, \cdots, x_k>)$ は、**シーケンス $x_1, x_2,...,x_k$ がデータセットで観察された回数**である.
This model, however, still suffers from the problem of data sparsity (for example, see Sarwar et al.(2000a)) and performs poorly in practice.
**しかし、このモデルは、依然としてデータの疎密の問題に悩まされており(ex. Sarwar et al.(2000a))、実際の性能は低い**.
In the next section, we describe several techniques for improving the estimate..
次節では、推定値を改善するためのいくつかの技法について説明する.

## 3.2. Some Improvements いくつかの改善点.

We experimented with several enhancements to the maximum-likelihood n-gram model on data different from that used in our formal evaluation.
最尤N-gramモデルについては、正式な評価で使用したデータとは異なるデータで、いくつかの機能拡張の実験を行った.
The improvements described and used here are those that were found to work well..
ここで説明され、使用されている改良は、うまく機能することが確認されたもの.

One enhancement is a form of skipping (Chen and Goodman, 1996), and is based on the observation that the occurrence of the sequence $x_1, x_2, x_3$ lends some likelihood to the sequence $x_1, x_3$.
1つの強化はスキップの一種で（Chen and Goodman, 1996）、シーケンス$x_1, x_2, x_3$ の発生がシーケンス $x_1, x_3$ にある程度の可能性を与えるという観察に基づいている.(?? 次の例を見たらわかりやすかった!)
That is, if a person bought x1, x2, x3, then it is likely that someone will buy x3 after x1.
**つまり、$x_1, x_2, x_3$ を買った人がいた場合、$x1$の次に$x3$を買う人がいる可能性が高い.**
The particular skipping model that we found to work well is a simple additive model.
私たちがうまく機能することを発見した特定のスキップモデルは、**単純な加法モデル**である.
First, the count for each state transition is initialized to the number of observed transitions in the data.
まず、各 state transition のカウントは、データで観測されたtransitionsの数に初期化される.
Then, given a user sequence $x_1, x_2, \cdots, x_n$, we add the fractional count $1/2^{(j−(i+3))}$ to the transition from $<x_i, x_{i+1}, x_{i+2}$ to $<x_{i+1}, x_{i+2}, x_{j}>$, for all $i+3 < j <= n$.
次に、ユーザ列 $x_1, x_2, \cdots, x_n$ が与えられたとき、すべての $i+3 < j <= n$ について、$<x_i, x_{i+1}, x_{i+2}>$ から $<x_{i+1}, x_{i+2}, x_{j}>$ への遷移(transition)に分数 $1/2^{(j−(i+3))}$ を追加する.(->分数を追加する意味って...?)
This fractional count corresponds to a diminishing probability of skipping a large number of transactions in the sequence.
この端数カウントは、シーケンス内の多数のトランザクションをスキップする確率が減少することに対応している.(??)
We then normalize the counts to obtain the transition probabilities:.
次に、カウントを正規化し、遷移確率(transition probabilities)(=state sのユーザがs'にtransitionする確率質量?)を求める.

$$
tr_{MC}(s, s') = \frac{const(s, s')}{\sum_{s'} const(s,s')}
\tag{6}
$$

where $const(s, s')$ is the (fractional) count associated with the transition from s to s 0 ..
ここで、$const(s, s')$ は、**sからs'へのtransitionに関連する(分数)カウント(??)**である.

A second enhancement is a form of clustering that we have not found in the literature.
**2つ目の強化点**は、文献にはないクラスタリングという形式を採用したことである.
Motivated by properties of our domain, the approach exploits similarity of sequences.
このアプローチは、我々のドメインの特性から動機づけられ、シーケンスの類似性を利用するものである.
For example, the state hx, y,zi and the state hw, y,zi are similar because some of the items appearing in the former appear in the latter as well.
例えば、state $<x,y,z>$ とstate $<w,y,z>$ は、**前者に出現するアイテムの一部が後者にも出現するため、類似している**.
The essence of our approach is that the likelihood of transition from s to s 0 can be predicted by occurrences from t to s 0 , where s and t are similar.
**このアプローチの本質は、$s$ と $t$ が類似している場合、$s$ から $s'$ への遷移(transition)の尤度を、$t$から$s'$への発生によって予測できること**である.
In particular, we define the similarity of states si and sj to be.
特に、state $s_i$ と $s_j$ の類似性を次のように定義する.

$$
sim(s_i,s_j) = \sum_{m=1}^{k} \delta(s_{i}^{m}, s_{j}^{m})\cdot (m + 1)
\tag{7}
$$

where $\delta(\cdot ,\cdot)$ is the Kronecker delta function and s m i is the mth item in state si .
ここで、$\delta(\cdot ,\cdot)$ は**クロネッカーデルタ関数**、$s^{m}_{i}$ はstate $s_i$ における m 番目のアイテムである.
This similarity is arbitrary up to a constant.
この類似性は一定まで任意である.
In addition, we define the similarity count from state s to s 0 to be.
また、state $s$ から $s'$ への類似度カウント(カウント??)を次のように定義する.

$$
simcount(s, s') = \sum_{s_i} sim(s,s_{i})\cdot tr_{MC}^{old}(s_i, s')
\tag{8}
$$

where $tr_{MC}^{old}(s_i, s')$ is the original transition function, with or without skipping (we shall compare the models created with and without the benefit of skipping).
ここで、$tr_{MC}^{old}(s_i, s')$ は、スキップの有無にかかわらず、**元のtransition function** である(スキップの恩恵の有無で作成したモデルを比較することにする).
The new transition probability from s 0 to s is then given by5.
そして、$s'$ から$s$への新しい遷移確率は、次式で与えられる:

$$
tr_{MC}(s, s') = \frac{1}{2} tr_{MC}^{old}(s, s')
+ \frac{1}{2} \frac{simcount(s, s')}{\sum_{s''} simcount(s,s'')}
\tag{9}
$$

A third enhancement is the use of finite mixture modeling.6 Similar methods are used in n-gram models, where—for example—a trigram, a bigram, and a unigram are combined into a single model.
同様の手法は、例えば、trigram(n=3)、bigram(n=2?)、unigram(n=1)を1つのモデルに統合する、n-gramモデルでも使用されている.
Our mixture model is motivated by the fact that larger values of k lead to states that are more informative whereas smaller values of k lead to states on which we have more statistics.
**この混合モデルは、kの値が大きいほど情報量の多い状態になり、kの値が小さいほど統計量の多い状態になるという事実に基づいている**.(情報量と統計量の値定義を調べた方がよさそう...!)
To balance these conflicting properties, we mix k models, where the ith model looks at the last i transactions.
これらの相反する特性のバランスをとるために、k個のモデルを混合し、i番目のモデルは直近のi個のトランザクションを見るようにする.
Thus, for k = 3, we mix three models that predict the next transaction based on the last transaction, the last two transactions, and the last three transactions.
したがって、**k = 3の場合**、最後のtransaction、最後の2つのtransactions、最後の3つのtransactionsに基づいて次の取引を予測する、**3つのモデルを混合する**.
In general, we can learn mixture weights from data.
一般的には、データから混合物の重みを学習することができる.
We can even allow the mixture weights to depend on the given case (and informal experiments on our data suggest that such context-specificity would improve predictive accuracy).
また、混合比の重みが与えられたケースに依存するようにすることもできる(私たちのデータに対する非公式な実験では、このような文脈特異性が予測精度を向上させることが示唆されている)
Nonetheless, for simplicity, we use π1 = ··· = πk = 1/k in our experiments.
ただ我々の実験では、簡単のために、$\pi_1 = \cdots = \pi_k = \frac{1}{k}$ とする.
Because our primary model is based on the k last items, the generation of the models for smaller values entails little computational overhead..
我々の主要なモデルは直近のk個のアイテムに基づいているため、より小さな値のモデルの生成はほとんど計算オーバーヘッドを必要としない(=混合するか否かは計算量に影響を与えない、みたいな意味??).

# 4. Evaluation of the Predictive Model 予測モデルの評価

Before incorporating our predictive model into an MDP-based recommender system, we evaluated the accuracy of the predictive model.
MDPベースのレコメンダーシステムに予測モデルを組み込む前に、予測モデルの精度を評価した.
Our evaluation used data corresponding to user behavior on a web site (without recommendation) and employed the evaluation metrics commonly used in the collaborative filtering literature.
**評価には、Webサイト上でのユーザの行動(推薦なし)に相当するデータを使用**し、協調フィルタリングの文献で一般的に使用されている評価指標を採用した.
In Section 6 we evaluate the MDP-based approach using an experimental approach in which recommendations on an e-commerce site are manipulated by our algorithms..
セクション6では、電子商取引サイトのレコメンデーションが我々のアルゴリズムによって操作される実験的アプローチを用いて、MDPベースのアプローチを評価する.

## 4.1. Data Sets データセット

We base our evaluations on real user transactions from the Israeli online bookstore Mitos(www.mitos.co.il).
イスラエルのオンライン書店Mitos(www.mitos.co.il)の実際のユーザ取引に基づく評価を行っている.
Two data sets were used: one containing user transactions (purchases) and one containing user browsing paths obtained from web logs.
ユーザのトランザクション(購入)を含むデータセットと、ウェブログから取得したユーザのブラウジングパスを含むデータセットの2つを使用した.
We filtered out items that were bought/visited less than 100 times and users who bought/browsed no more than one item as is commonly done when evaluating predictive models (for example, Zimdars et al.(2001)).
**予測モデルを評価する際によく行われるように、購入・閲覧回数が100回以下のアイテムや、購入・閲覧回数が1回以下のユーザをフィルタリングした**（例えば、Zimdars et al(2001))。
We were left with 116 items and 10820 users in the transactions data set, and 65 items and 6678 users in the browsing data set.7 In our browsing data, no cookies were used by the site.
その結果，トランザクションデータセットとして116アイテム，10820ユーザー，ブラウジングデータセットとして65アイテム，6678ユーザーが残された7。ブラウジングデータでは，サイトがクッキーを使用していない.
If the same user visited the site with a new IP address, then we would treat her as a new user.
同じユーザが新しいIPアドレスでサイトを訪れた場合、新しいユーザーとして扱われる.
Also, activity on the same IP address was attributed to a new user whenever there were no requests for two hours.
また、同じIPアドレスでのアクティビティは、2時間リクエストがない場合、新しいユーザーに帰属していた.
These data sets were randomly split into a training set (90% of the users) and a test set (10% of the users)..
これらのデータセットは、ランダムにトレーニングセット（ユーザーの90％）とテストセット（ユーザーの10％）に分割された.

The rational for removing items that were rarely bought is that they cannot be reliably predicted.
ほとんど買われなかったアイテムを削除した(フィルタリングした)根拠は、確実な予測ができないからである.
This is a conservative approach which implies, in practice, that a rarely visited item will not be recommended by the system, at least initially.
これは保守的なアプローチであり、実際には、めったに訪れないアイテムは、少なくとも最初はシステムによって推薦されないことを意味する.

We evaluated predictions as follows.
予測値の評価は以下のように行った.
For every user sequence $t_1,t_2,\cdots,t_n$ in the test set, we generated the following test cases:.
テストセット内の各ユーザ sequence $t_1,t_2,\cdots,t_n$ に対して、以下のテストケースを生成した.

$$
<t_1>, <t_1, t_2>, \cdots, <t_{n-k}, t_{n-k + 1}, \cdots, t_{n-1}>
\tag{10}
$$

closely following tests done by Zimdars et al.(2001).
Zimdarsらによって行われたテストに密着している(2001).
For each case, we then used our various models to determine the probability distribution for ti given ti−k,ti−k+1,...,ti−1 and ordered the items by this distribution.
そして、それぞれのケースについて、様々なモデルを用いて、$t_{i-k},t_{i-k+1},\cdots, t_{i-1}$ が与えられたときの $t_{i}$ の確率分布(=**次にどのアイテムをinteractionするかって話だっけ...??**)を求め、この分布によってアイテムをソートした.
Finally, we used the ti actually observed in conjunction with the list of recommended items to compute a score for the list..
最後に、実際に観察された$t_i(=t_i番目にinteractionしたアイテム?)$と推薦アイテムのリスト(=$t_i$の予測値の順に降順ソートしたアイテムリスト??)を合わせて、リストのスコアを算出した.

## 4.2. Evaluation Metrics 評価指標

We used two scores: Recommendation Score (RC) (Microsoft, 2002) and Exponential Decay Score (ED) (Breese et al., 1998) with slight modifications to fit into our sequential domain..
我々は2つのスコアを使用した. Recommendation Score (RC) (Microsoft, 2002) と Exponential Decay Score (ED) (Breese et al., 1998) の2つのスコアを使用し、我々のシーケンシャルドメインに適合するように若干の修正を加えている.

### 4.2.1. Recommendation Score レコメンドスコア

For this measure of accuracy, a recommendation is deemed successful if the observed item ti is among the top m recommended items (m is varied in the experiments).
この精度の指標では、**観測されたアイテム $t_i$ が上位$m$個の推薦アイテムの中にあれば、推薦は成功したとみなされる**(実験では$m$は変化させる).
The score RC is the percentage of cases in which the prediction is successful.
**スコアRCは、予測が成功したケースの割合**.
A score of 100 means that the recommendation was successful in all cases.
100点満点は、すべてのケースで推薦が成功したことを意味する.
This score is meaningful for commerce sites that require a short list of recommendations and therefore care little about the ordering of the items in the list..
このスコアは、短い推薦リストを必要とし、したがって**リスト内のアイテムの順序をあまり気にしないコマースサイトに有意義**である.

### 4.2.2. Exponential Decay Score 指数関数的減衰スコア

This measure of accuracy is based on the position of the observed ti on the recommendation list, thus evaluating not only the content of the list but also the order of items in it.
この精度の指標は、**推薦リストにおける観測された $t_i$ の位置に基づいている**ため、リストの内容だけでなく、**リスト内のアイテムの順序も評価される**.
The underlying assumption is that users are more likely to select a recommendation near the top of the list.
ユーザがリストのトップに近いレコメンドを選択する可能性が高いというのが根本的な前提.
In particular, it is assumed that a user will actually see the mth item in the list with probability.
特に、ユーザがリストの$m$番目のアイテムを実際に見ることは確率的に想定されている.

$$
p(m) = 2^{-\frac{(m-1)}{(\alpha - 1)}}, (m \geq 1)
\tag{11}
$$

where α is the half-life parameter—the index of the item in the list with probability 0.5 of being seen.
ここで、$\alpha$ は**半減期パラメータ(half-life parameter)**=リストの中で0.5%の確率で見られるアイテムのインデックスである.
The score is given by.
スコアは、次のように与えられる.

$$
100 \cdot \frac{\sum_{c \in C} p(m = pos(t_i|c))}{|C|}
\tag{12}
$$

where $C$ is the set of all cases, $c = t_{i−k},t_{i−k+1}, \cdots,t_{i−1}$ is a case, and $pos(t_i|c)$ is the position of the observed item $t_i$ in the list of recommended items for $c$.
ここで、$C$は全ケースの集合、$c = t_{i-k},t_{i-k+1},\cdots,t_{i-1}$ はケース、$pos(t_i |c)$ は$c$のアイテムアイテムリストにおける観測アイテム$t_i$の位置である.
We used α = 5 in our experiments in order to be consistent with the experiments of Breese et al.(1998) and Zimdars et al.(2001).
Breese et al.(1998) and Zimdars et al.(2001)の実験と整合性を取るため、実験ではα＝5を使用した.
The relative performance of the models was not sensitive to α..
モデルの相対的な性能は、αに敏感ではなかった.(=$\alpha$の影響をそんなに受けなかった.)

## 4.3. Comparison Models 比較モデル.

### 4.3.1. Commerce Server 2000 Predictor Commerce Server 2000 Predictor.

A model to which we compared our results is the Predictor tool developed by Microsoft as a part of Microsoft Commerce Server 2000, based on the models of Heckerman et al.(2000).
今回の結果を比較したモデルとして、HeckermanらのモデルをベースにMicrosoft Commerce Server 2000の一部としてMicrosoft社が開発したPredictorツールがある.
This tool builds dependency-network models in which the local distributions are probabilistic decision trees.
局所分布が確率的な決定木である依存関係ネットワークモデルを構築するツールである.
We used these models in both a non-sequential and sequential form.
これらのモデルを、非連続型と連続型の両方で使用した.
These two approaches are described in Heckerman et al.(2000) and Zimdars et al.(2001), respectively.
これら2つのアプローチについては、Heckerman et al.(2000)やZimdars et al.(2001)に記載されている.

In the non-sequential approach, for every item, a decision tree is built that predicts whether the item will be selected based on whether the remaining items were or were not selected.
**non-sequential approachでは、すべてのアイテムに対して、残りのアイテムが選ばれたか選ばれなかったかで、そのアイテムが選ばれるかどうかを予測する決定木が構築**される.
In the sequential approach, for every item, a decision tree is built that predicts whether the item will be selected next, based on the previous k items that were selected.
sequential approachでは、すべてのアイテムに対して、過去に選択されたk個のアイテムに基づいて、次にそのアイテムが選択されるかどうかを予測する決定木が構築される.
The predictions are normalized to account for the fact that only one item can be predicted next.
予測値は、次に予測できるアイテムが1つだけであることを考慮して正規化されている.
Zimdars et al.(2001) also use a “cache” variable, but preliminary experiments showed it to decrease predictive accuracy.
Zimdars et al.(2001)も“cache” variableを用いているが、予備実験では予測精度を低下させることがわかった.
Consequently, we did not use the cache variable in our formal evaluation..
そのため、正式な評価では、キャッシュ変数を使用しなかった.

These algorithms appear to be the most competitive among published work.
これらのアルゴリズムは、公開されている作品の中で最も競争力があると思われる.
The combined results of Breese et al.(1998) and Heckerman et al.(2000) show that (non-sequential) dependency networks are no less accurate than Bayesian-network or clustering models, and about as accurate as Correlation, the most accurate (but computationally expensive) memory-based method.
Breese et alらとeckerman et al.の結果を総合すると、(non-sequential)依存性ネットワークは、ベイジアンネットワークやクラスタリングモデルに劣らず、最も正確な(しかし計算コストのかかる)メモリベースの方法であるCorrelationとほぼ同じ精度であることを示している.
Sarwar et al.(2000b) apply dimensionality reduction techniques to the user rating matrix, but their approach fails to be consistently more accurate than Correlation.
Sarwarら(2000b)は、ユーザ評価行列に次元削減技術を適用したが、彼らのアプローチは、Correlationより一貫して正確であることを失敗した.
Only the sequential algorithm of Zimdars et al.(2001) is more accurate than the non-sequential dependency network to our knowledge..
Zimdarsらのsequentialアルゴリズム(2001)のみは、我々の知る限り、non-sequential従属ネットワークより正確である.

We built five sequential models 1 ≤ k ≤ 5 for each of the data sets.
各データセットについて、1≦k≦5の5つの逐次モデルを構築した.
We refer to the non-sequential Predictor models as Predictor-NS, and to the Predictor models built using the data expansion methods with a history of length k as Predictor-k..
**non-sequentialなPredictorモデルをPredictor-NS**、**長さkの履歴を持つデータ拡張法を用いて構築したPredictorモデルをPredictor-k**と呼ぶことにする.

### 4.3.2. Unordered MCs

We also evaluated a non-sequential version of our predictive model, where sequences such as hx, y,zi and hy,z, xi are mapped to the same state.
また、$x,y,z$や$y,z,x$などのシーケンスが**同じ状態にマッピングされる、予測モデルのnon-sequential version**も評価した.
If our assumption about the sequential nature of recommendations is incorrect, then we should expect this model to perform better than our MC model, as it learns the probabilities using more training data for each state, gathering all the ordered data into one unordered set.
もし、**レコメンデーションの順次性(sequential nature)についての仮定が正しくない場合**、このモデルは、各stateについてより多くのトレーニングデータを用いて確率を学習し、すべての順序付きデータを1つの順序なしセットに集めるので、MCモデルよりも良いパフォーマンスを示すと予想される.
Skipping, clustering, and mixture modeling were included as described in section 2.
スキップ、クラスタリング、混合モデリングは、セクション 2 で説明したように含まれている.
We call this model UMC (Unordered Markov chain).
このモデルをUMC(Unordered Markov chain)と呼ぶ.

## 4.4. Variations of the MC Model MCモデルのバリエーション

In order to measure how each n-gram enhancement influenced predictive accuracy, we also evaluated models that excluded some of the enhancements.
また、各n-gramの強化が予測精度に与える影響を測定するために、一部の強化を除いたモデルも評価した.
In reporting our results, we refer to a model that uses skipping and similarity clustering with the terms SK and SM, respectively.
結果を報告する際、**飛び飛び(skipping)のクラスタリングと類似(similarity)のクラスタリングを使用するモデルをそれぞれSKとSMと呼ぶ**ことにする.
In addition, we use numbers to denote which mixture components are used.
また、どの混合成分が使用されているかを数字で表している.
Thus, for example, we use MC 123 SK to denote a Markov chain model learned with three mixture components—a bigram, trigram, and quadgram—where each component employs skipping but not clustering..
例えば、MC123 SKは、bigram, trigram, quadgram の3つの混合成分で学習したマルコフ連鎖モデルであり、各成分はクラスタリングを行わず、スキップすることを表す.(n=1,2,3 ではなく n=2, 3, 4になるのか...?)

## 4.5. Experimental Results 実験結果

Figure 1(a) and figure 1(b) show the exponential decay score for the best models of each type (Markov chain, Unordered Markov chain, Non-Sequential Predictor model, and Sequential Predictor Model).
図1（a）、図1（b）は、各タイプの最良モデル(Markov chain、Unordered Markov chain、Non-Sequential Predictor model、Sequential Predictor Model)の指数関数的減衰スコアを示している.
It is important to note that all the MC models using skipping, clustering, and mixture modelling yielded better results than every one of the Predictor-k models and the non-sequential Predictor model.
スキップ、クラスタリング、混合モデリングを用いた**すべてのMCモデルが、Predictor-kモデルや非連続Predictorモデルのどれよりも良い結果をもたらしたことは重要なポイント**.
We see that the sequence-sensitive models are better predictors than those that ignore sequence information.
**sequence情報を無視したモデルよりも、sequence-sensitiveなモデルの方が予測精度が高いことがわかる**.
Furthermore, the Markov chain predicts best for both data sets..
さらに、**マルコフ連鎖は、どちらのデータセットに対しても最適な予測**をしている.

Figure 2(a) and Figure 2(b) show the recommendation score as a function of list length (m).
図2（a）と図2（b）は、リスト長 $m$ の関数として推薦スコアを示したものである.
Once again, sequential models are superior to non-sequential models, and the Markov chain models are superior to the Predictor models..
今回も sequential モデルは non-sequential モデルより優れており、マルコフ連鎖モデルはpredictorモデルより優れている.

Figure 3(a) and Figure 3(b) show how different versions of the Markov chain performed under the exponential decay score in both data sets.
図3(a)と図3(b)は、両方のデータセットにおいて、指数関数的減衰スコアの下で**マルコフ連鎖の異なるバージョンがどのように機能するか**を示している.
We see that multi-component models out-perform single-component models, and that similarity clustering is beneficial.
**多成分モデルが単成分モデルより優れていること、similarity clusteringが有効であること**がわかる.
In contrast, we find that skipping is only beneficial for the transactions data set.
**一方、スキップが有効なのは、トランザクションデータセットのみ**であることがわかる.
Perhaps users tend to follow the same paths in a rather conservative manner, or site structure does not allow users to “jump ahead”.
おそらく、ユーザはどちらかというと保守的に同じ道をたどる傾向があるのか、サイト構造上、ユーザが "先に進む "ことができないのだろう.(??)
In either case, once recommendations are available in the site (thus changing the site structure), skipping may prove beneficial..
いずれにせよ、**サイト内でレコメンデーションが利用できるようになると(サイト構造が変わる)、スキップが有効になる可能性がある**.

# 5. An MDP-Based Recommender Model MDP ベースの推薦者モデル

The predictive model we described above does not attempt to capture the short and long-term effect of recommendations on the user, nor does it try to optimize its behavior by taking into account such effects.
先に述べた予測モデルは、レコメンデーションがユーザに与える短期的・長期的な影響を捉えようとするものではなく、また、そうした影響を考慮して行動を最適化しようというものでもない.
We now move to an MDP model that explicitly models the recommendation process and attempts to optimize it.
**ここで、推薦プロセスを明示的にモデル化し、その最適化を試みるMDPモデルに移行**する.
The predictive model plays an important role in the construction of this model..
このモデルの構築には、**予測モデルが重要な役割を果たす**.

We assume that we are given a set of cases describing user behavior within a site that does not provide recommendations, as well as a probabilistic predictive model of a user acting without recommendations generated from this data.
ここでは、レコメンデーションを提供しないサイト内でのユーザの行動を記述したケースと、このデータから生成されたレコメンデーションなしで行動するユーザの確率的予測モデル(前の章のやつ.)が与えられると仮定する.
The set of cases is needed to support some of the approximations we make, and in particular, the lazy initialization approach we take.
このケースは、私たちが行う近似の一部、特に私たちが取る遅延初期化(lazy initialization)アプローチをサポートするために必要.(?)
The predictive model provides the probability the user will purchase a particular item x given that her sequence of past purchases is x1,...,xk.
**予測モデルは、ユーザが過去の購入履歴が$x1,...,xk$である場合に、特定のアイテムxを購入する確率を提供**する.(うんうん！)
We denote this value by Prpred(x|x1,...,xk), where k = 3 in our case.
x1,...,xk), where k = 3 in our case.
It is important to stress that the approach presented here is independent of the particular technique by which the above predictive value is approximated.
ここで強調したいのは、**ここで紹介するアプローチは、上記の予測値を近似する特定の技術に依存しないということ**である.
Naturally, in our implementation we used the predictive model developed in Section 3, but there are other ways of constructing such a model (for example, Zimdars et al.
当然ながら、我々の実装では、セクション3で開発した予測モデルを使用したが、このようなモデルを構築する方法は他にもある（例えば、Zimdars et al.
(2001); Kadie et al.
(2001); Kadie et al.
(2002))..
(2002))..

## 5.1. Defining the MDP MDPを定義する

Recall that to define an MDP, we need to provide a set of states, actions, transition function, and a reward function.
MDPを定義するためには、**状態(state)、行動(action)、遷移関数(transition function)、報酬関数(reward function)のセットを提供する必要がある**ことを思い出してください.
We now describe each of these elements.
次に、これらの要素についてそれぞれ説明する.
The states of the MDP for our recommender system are k-tuples of items (for example, books, CDs), some prefix of which may contain null values corresponding to missing items.
推薦システムのMDPの **状態(state) は、アイテム（例えば、本、CD）の k-tuples(interaction履歴)** であり、そのうちのいくつかの接頭辞は、アイテムの欠落に対応するNULL値を含むことができる.(ユーザのinteractionがk個に満たないケース)
This allows us to model shorter sequences of purchases..
これにより、より短い購入の連続をモデル化することができる.

The actions of the MDP correspond to a recommendation of an item.
MDPの **action は、アイテムの推薦に対応**している.
One can consider multiple recommendations but, to keep our presentation simple, we start by discussing single recommendations..
複数の推奨事項を検討することも可能ですが、ここではシンプルに、一つの推奨事項を検討することから始める.

Rewards in our MDP encode the utility of selling an item (or showing a web page) as defined by the site.
MDPの報酬は、サイトが定義する interaction (ex. 商品を売る, ウェブページを見せる, etc.)の効用を符号化したものである.
Because the state encodes the list of items purchased, the reward depends on the last item defining the current state only.
状態は購入したアイテムのリストを符号化するため、報酬は現在の状態を定義する最後のアイテムにのみ依存する.
For example, the reward for state hx1, x2, x3i is the reward generated by the site from the sale of item x3.
例えば、状態hx1, x2, x3iの報酬は、アイテムx3の販売からサイトが生み出す報酬である.
In this paper, we use net profit for reward..
本論文では、報酬のために純利益を使用する.

The state following each recommendation is determined by the user’s response to that recommendation.
**各レコメンドに続く state は、そのレコメンドに対するユーザの反応によって決まる.**
When we recommend an item x 0 , the user has three options:.
アイテム $x'$ を推薦するとき、ユーザには次の**3つの選択肢**がある.

- Accept this recommendation, thus transferring from state hx1, x2, x3i into hx2, x3, x 0 i この勧告を受け入れることで、状態hx1, x2, x3iからhx2, x3, x 0 iに移行する.
- Select some non-recommended item x 00, thus transferring the state hx1, x2, x3i into hx2, x3, x 00i. ある非推薦アイテム$x''$を選択することで、状態hx1, x2, x3iをhx2, x3, x 00iに移行する.
- Select nothing (for example, when the user terminates the session), in which case the system remains in the same state. 何もしない(ユーザーがセッションを終了した場合など)を選択すると、システムはそのままのstate を維持する.

Thus, the stochastic element in our model is the user’s actual choice.
したがって、このモデルにおける確率的要素は、ユーザの実際の選択である.
The transition function for the MDP model:.
MDPモデルの遷移関数は以下:

$$
tr^{1}_{MDP} (<x_1, x_2, x_3>, x', <x_2, x_3, x''>)
\tag{13}
$$

is the probability that the user will select item x 00 given that item x 0 is recommended in state hx1, x2, x3i.
は、状態hx1, x2, x3iでアイテムx0が推奨されている場合に、ユーザがアイテムx00を選択する確率.
We write tr1 MDP to denote that only single item recommendations are used..
単品推薦のみを行うことを表すためにtr1 MDPと表記する.

### 5.1.1. Initializing $tr_{MMDP}$ $tr_{MMDP}$ を初期化する。

Proper initialization of the transition function is an important implementation issue in our system.
**transition functionの適切な初期化は、本システムにおける重要な実装課題**である.
Unlike traditional model-based reinforcement learning algorithms that learn the proper values for the transition function and hence an optimal policy online, our system needs to be fairly accurate when it is first deployed.
**従来のモデルベースの強化学習アルゴリズムが、遷移関数の適切な値、つまり最適な方策をオンラインで学習するのとは異なり、私たちのシステムは、最初に展開するときにかなり正確である必要がある.**
A for-profit e-commerce8 site is unlikely to use a recommender system that generates irrelevant recommendations for a long period, while waiting for it to converge to an optimal policy.
営利目的のEコマース8サイトでは、**最適なポリシーに収束するのを待つ間、無関係なレコメンドを生成するレコメンダーシステムを長期間使用することは考えにくい**.
We therefore need to initialize the transition function carefully.
そのため、遷移関数を慎重に初期化する必要がある.
We can do so based on any good predictive model, making the following assumptions:.
あらゆる優れた予測モデルに基づいて、以下の**2つの仮定**を立てて行うことができる.

- A recommendation increases the probability that a user will buy an item. This probability is proportional to the probability that the user will buy this item in the absence of recommendations. This assumption is made by most collaborative filtering models dealing with e-commerce sites.9 We denote the proportionality constant for recommendation r in state s by αs,r , where αs,r > 1. レコメンデーションは、ユーザが商品を購入する確率を高めるもの. **この確率は、レコメンドがない場合にユーザがこのアイテムを購入する確率に比例する**. この仮定は、電子商取引サイトを扱う協調フィルタリングモデルの多くでなされている9。状態$s$における推薦$r$の比例定数を$\alpha_{s,r}$とし、$\alpha_{s,r}>1$ とする.

- The probability that a user will buy an item that was not recommended is lower than the probability that she will buy when the system issues no recommendations at all, but still proportional to it. We denote the proportionality constant for recommendation r in state s by βs,r , where βs,r < 1. 推薦されなかった商品を購入する確率は、システムが全く推薦をしない場合に購入する確率より低いが、それでも比例しているのである. 状態 $s$ における推薦 $r$ の比例定数を$\beta_{s,r}$とする（$\beta_{s,r} < 1$）.

To allow for a simpler representation of the equations, for a state s = hx1,...,xki and a recommendation r let us use s·r to denote the state s 0 = hx2,...,xk,ri.
方程式をより簡単に表現するために、state $s = <x1,...,xk>$と推薦rに対して、state $s' = <x2,...,xk,r>$ を表すために $s \cdot r$ を使用することにする.
We use trpredict(s,s·r) to denote the probability that the user will choose r next, given that its current state is s according to the predictive model in which recommendations are not considered, that is, Prpred(r|s).
推薦を考慮しない予測モデルにより、ユーザの現在の状態が$s$である場合に、次に$r$を選択する確率、すなわち$P_{r_{pred}}(r|s)$を表すために、$tr_{predict}(s,s \cdot r)$とする.
Thus, with αs,r and βs,r constant over s and r and equal to α and β, respectively, we have.
したがって、$\alpha_{s,r}$ と $\beta_{s,r}$ がsとrにわたって(任意のsとrの組み合わせにおいて)一定で、それぞれαとβに等しいとすると、次のようになる.

$$
tr^{1}_{MDP}(s,r, s \cdot r) = \alpha \cdot $tr_{predict}(s,s \cdot r)
\tag{14}
$$

the probability that a user will buy r next if it was recommended;.
推薦された場合、ユーザーが次にrを購入する確率；↑

$$
tr^{1}_{MDP}(s,r', s \cdot r) = \beta \cdot $tr_{predict}(s,s \cdot r), r' \neq r,

\tag{15}
$$

the probability that a user will buy r if something else was recommended; and.
他のアイテム$r'$を推薦された場合に、ユーザーがrを購入する確率↑

$$
tr^{1}_{MDP}(s,r, s) = 1 - tr^{1}_{MDP}(s,r, s \cdot r) - \sum_{r' \neq r} tr^{1}_{MDP}(s,r, s \cdot r')

\tag{16}
$$

the probability that a user will not buy any new item after r was recommended.
↑は推薦された後、そのユーザが新たなアイテムを購入しない確率を示す.
We do not see a reason to stipulate a particular relationship between α and β, although we must have.
しなければならないが、αとβの関係を特に規定する理由は見いだせない.

$$
tr^{1}_{MDP}(s,r, s \cdot r) +  \sum_{r' \neq r} tr^{1}_{MDP}(s,r, s \cdot r') < 1
\tag{17}
$$

The exact values of αs,r and βs,r should be chosen carefully.
$α_{s,r}$と$β_{s,r}$の正確な値は慎重に選択する必要がある.
Choosing αs,r and βs,r to be constants over all states and recommendations (say α = 2, β = 0.5) might cause the sum of transition probabilities in the MDP to exceed 1.
$α_{s,r}$と$β_{s,r}$ をすべての state $s$ と 推薦action $r$ で定数にすると（α＝2、β＝0.5）、**MDPの遷移確率の合計が1を超えてしまう可能性がある**.
The approach we took was motivated by Kitts et al.
私たちがとったアプローチは、Kittsらによって動機づけられたもの.
(2000), who showed that the increase in the probability of following a recommendation is large when one recommends items having high lift, defined to be $pr(x|h) / pr(x)$.
$pr(x|h) / pr(x)$を"Lift"と定義し、"Lift"が高いアイテムを推薦した場合に、推薦に従う確率の増加が大きくなる.
Thus, it is not unreasonable to assume that this increase in probability is proportional to lift:.
したがって、**この確率(?)の上昇は、"Lift"値に比例する**と考えても無理はないだろう:

$$
pr(r|s, r) - pr(r|s, r') \sim \gamma \frac{p(r|s)}{p(r)}
\tag{18}
$$

where p(r) is the prior probability of buying r.
ここで、**$p(r)$はrを購入する事前確率**である.
Fixing αs,r to be a little larger than 1 as follows:.
次のように$α_{s,r}$が1より少し大きくなるように固定する:

$$
\alpha_{s, r} = \frac{\gamma + p(r)}{p(r)}
\tag{19}
$$

where γ is a very small constant (we use γ = 1 1000 ), and solving for βs,r , we obtain.
ここで、$\gamma$ は非常に小さな定数（ここではγ＝1/1000としている）であり、$β_{s,r}$について解くと、次のようになる:

$$
\beta_{s,r} = \frac{1 - \sum_{r'} \alpha_{s,r'} p(s \cdot r'|s)}{(n-1)p(s \cdot r|s)} + \alpha_{s,r}
\tag{20}
$$

If βs,r is negative, we set it to a very small positive value and normalize the probabilities afterwards..
$β_{s,r}$が負の値であれば、非常に小さな正の値に設定し、その後の確率を正規化する.

There are a few things to note about tr1 MDP(s,r 0 ,s·r), the probability that a user will buy r if something else was recommended, and its representation.
$tr^{1}_{MDP}(s,r', s\cdot r)$、即ち**ユーザが他のアイテムを勧められた場合にrを購入する確率とその表現**について、いくつか注意すべき点がある.
First, since tr1 MDP(s,r 0 ,s·r) = βs,r ·tr(s,s· r), the MDP’s initial transition probability does not depend on r 0 because our initialization is based on data that was collected without the benefit of recommendations.
まず、$tr^{1}_{MDP}(s,r', s\cdot r) = \beta_{s,r} \cdot tr(s,s\cdot r)$ であるため、**推薦の恩恵を受けずに収集したデータに基づいて初期化を行う**ため、MDPの初期遷移確率が$r'$に依存しない.
Of course, if one has access to data that reflects the effect of recommendations (prpredict(s·r|s,r)), one can use it to provide a more accurate initial model.
もちろん、**推薦の効果を反映したデータ**($pr_{predict}(s \cdot r|s,r)$)**にアクセスできれば**、それを使ってより正確な初期モデルを提供することができる.
Next, note that we can represent this transition function concisely using at most two values for every state-item pair: the probability that an item will be selected in a state when it is recommended (that is, pr(s·r|s,r)) and the probability that an item will be selected when it is not recommended (that is, pr(s·r|s,r 0 )).
次に、**この transition function は、各state-itemペアに対して最大2つの値を用いて簡潔に表現できること**に注目する：
すなわち、ある state において、**あるアイテムが推薦されたときに選択(interaction)される確率**(= $pr(s \cdot r|s,r)$)と、あるアイテムが推薦されていないときに選択(interaction)される確率(= $pr(s \cdot r|s,r')$)である.
Because the number of items is much smaller than the number of states, we obtain significant reduction in the space requirements of the model..
アイテム数がstate数よりはるかに少ないため(これは分かる. state数はnum_item^mくらい?)、モデルの空間要件が大幅に削減される.(?)

### 5.1.2. Generating Multple Recommendations 複数の推薦を生成する。

When moving to multiple recommendations, we make the assumption that recommendations are independent.
複数の推薦に移行する場合、**推薦アイテム達が独立していること**(i.e. 推薦アイテムリストの組み合わせによって、ユーザのinteraction確率が変化しない事...!)を前提にしている.
Namely we assume that for every pair of sets of recommended items, R,R 0 , we have that.
すなわち、推奨アイテムの集合であるR,R'の各ペアについて、次のように仮定する.

$$
(r \in R \cup r \in R') \cap (r \notin R \cup r \notin R') \rightarrow tr_{MDP}(s,R,s\cdot r) = tr_{MDP}(s,R',s\cdot r)
\tag{21}
$$

This assumption might prove to be false.
この仮定は誤りであることが証明されるかもしれない.
It seems reasonable that, as the list of recommendations grows, the probability of selecting any item decreases.
推薦リストが大きくなるにつれて、どの項目も選択される確率が低くなるのは、合理的なことだと思う.
Another more subtle example is the case where the system “thinks” that the user is interested in an inexpensive cooking book.
また、もっと微妙な例として、ユーザが安価な料理本に興味を持っているとシステムが "考える "ケースもある.
It can then recommend a few very expensive cooking books and one is reasonably priced (but in no way cheap) cooking book.
そして、**非常に高価な料理本を数冊と、手頃な価格の（しかし決して安くはない）料理本を1冊を推薦することができる**.(=推薦アイテム達が独立でないケース!)
The reasonably priced book will seem like a bargain compared to the expensive ones, thus making the user more likely to buy it..
リーズナブルな価格の本は、高価な本と比べてお買い得に感じられるため、ユーザーは購入しやすくなる.

Nevertheless, we make this assumption so as not to be forced to create a larger action space where actions are ordered combinations of recommendations.
しかし、この仮定は、アクションがレコメンデーションの順序付けられた組み合わせである、より大きなアクション空間を作ることを余儀なくされないようにするためである.
Taking the simple approach for representing the transition function we defined above, we still keep only two values for every state–item pair:.
先に定義した遷移関数をシンプルに表現すると、各状態-項目のペアに対して、次の2つの値しか保持しない:

$$
tr_{MDP}(s,r \in R, s\cdot r) = tr_{MDP}^{1}(s,r, s\cdot r)
\tag{22}
$$

the probability that r will be bought if it appeared in the list of recommendations; and.
↑は推薦リスト$R$に登場した場合に$r$が購入される確率、である.
(複数アイテムを推薦しようが一つだけ推薦しようが、ユーザのinteractionしやすさは変わらないという仮定.)

$$
tr_{MDP}(s,r \notin R, s\cdot r) = tr_{MDP}^{1}(s,r', s\cdot r)
,\forall r' \notin r
\tag{23}
$$

the probability that r will be bought if it did not appear in the list..
↑はリストに掲載されなかった場合にrが購入される確率である.

As before, trMDP(s,r ∈/ R,s·r) does not depend on r, and will not depend on R in the discussion that follows.
前回同様、trMDP(s,r∈/ R,s-r)はrに依存せず、以降の議論でもRに依存することはないだろう.
We note again, that these values are merely reasonable initial values and are adjusted by our system based on actual user behavior, as we shall discuss..
なお、**これらの値はあくまで妥当な初期値であり、実際のユーザの行動に基づいてシステムで調整される**ことは、後述するとおり.

## 5.2. Solving the MDP MDPを解く

Having defined the MDP, we now consider how to solve it in order to obtain an optimal policy.
MDPを定義した上で、**最適な方策を得るためにどのように解くか**を考える.
Such a policy will, in effect, tell us what item to recommend given any sequence of user purchases.
このような方策は、事実上、ユーザが購入した商品の中から、どの商品を推薦するかを教えてくれるもの.
For the domains we studied, we found policy iteration (Howard, 1960)—with a few approximations to be described—to be a tractable solution method.
私たちが研究した領域では、**policy iteration（Howard, 1960）—with a few approximations to be described—が扱いやすい解法であることがわかった**.
In fact, on tests using real data, we found that policy iteration terminates after a few iterations.
実際、実データを使ったテストでは、ポリシーの反復が数回で終了してしまうことがわかった.
This stems from the special nature of our state space and the approximations we make, as we now explain..
これは、これから説明するように、**state spaceとその近似の特殊性**に起因している.

Our state space enjoys a number of features that lead to fast convergence of the policy iteration algorithm:.
**この状態空間は、政策反復アルゴリズムの高速収束につながる以下のような特徴を備えている**:

### Directionality. 指向性

Transitions in our state space seem to have inherent directionality: First, a state representing a short sequence cannot follow a state representing a longer sequence.
**状態空間における遷移には、固有の方向性があるようだ**. まず、短い配列を表す状態が、長い配列を表す状態に続くことはない.(それはそう.)
Second, the success of the sequential prediction model indicates that typically, if x is likely to follow y, y is less likely to follow x – otherwise, the sequence x, y and y, x would have similar probabilities, and we could simply use sets.
第二に、**sequential prediction modelの成功は、典型的には、xがyに続く可能性が高い場合、yはxに続く可能性が低いことを示している** - そうでなければ、順序x、yとy、xは同様の確率を持ち、単にセットを使用することができる.(=そうでなければnon-sequential モデルの性能が低下しないはず...!)
Thus, loops, which in principle could occur in our MDP model because we maintain only a limited amount of history, are not very likely.
このように、MDPモデルでは限られた量の履歴しか保持しないため、原理的に起こりうるループ(**feedback loopの事ではなく、policy iterationの事!**)はあまり起こらない.
Indeed, an examination of the loops in our state space graph reveals them to be small and scarce.
実際、状態空間グラフのループを調べると、ループは小さく希少であることがわかる.
Moreover, in the web site implementation, it is easy enough to filter out items that were already bought by the user from our list of recommendations.
さらに、**Webサイトの実装では、ユーザがすでに購入したアイテムをおすすめリストからフィルタリングすることも簡単**である.
It is well-known that directionality can be used to reduce the running time of MDP solution algorithm (for example, Bonet and Geffner (2003))..
MDP解法アルゴリズムの実行時間を短縮するために**方向性を利用できること**はよく知られている（例えば、Bonet and Geffner (2003) など）.

### Insensitivity to k. kに対する不感性

We have also found that the computation of an optimal policy is not heavily sensitive to variations in k—the number of past transactions we encapsulate in a state.
また、**最適なポリシーの計算は、1つの state にカプセル化された過去のトランザクションの数であるkの変動に大きく影響されないこと**も分かっている.
As k increases, so does the number of states, but the number of positive entries in our transition matrix remains similar.
kが大きくなると state の数(種類)も増えますが、遷移行列の正のエントリーの数は変わらない.(そうなんだ?)
Note that, at most, a state can have as many successors as there are items.
なお、1つのstateは、せいぜいアイテムの数だけ後継者(=次のstateの最後尾に追加されるアイテム履歴)を持つことができる.
When k is small, the number of observed successors for a state can be large.
kが小さいと、あるstateに対して観測される後継者の数が多くなることがある.(??)
When k grows, however, the number of successors decreases considerably.
しかし、kが大きくなると、後継者の数が大幅に減少する.
Table 2 demonstrates this relation in our implemented model..
表2は、この関係を我々の実装モデルで示したものである:

Despite these properties of the state space, policy evaluation still requires much effort given the large state and action space we have to deal with.
このような状態空間の特性にもかかわらず、扱うべきstate spaceとaction space が大きいため、方策評価には多くの労力が必要.
To alleviate this problem we resort to a number of approximations..
この問題を解決するために、いくつかの近似に頼ることになる.

### Ignoring Unobserved States.観察されない状態を無視する.

The vast majority of states in our models do not correspond to sequences that were observed in our training set because most combinations of items are extremely unlikely.
ほとんどのアイテムの組み合わせは極めてあり得ないため、モデルの状態の大部分は、トレーニングセットで観察されたシーケンスに対応しない.
For example, it is unlikely to find adjacent purchases of a science-fiction and a gardening book.
例えば、SFとガーデニングの本が隣接して購入されることはまずないでしょう.
We leverage this fact to save both space and computation time.
この事実を利用して、スペースと計算時間の両方を節約している.
First, we maintain transition probabilities only for states for which a transition occurred in our training data.
まず、**学習データで遷移が発生したstateのみ遷移確率を保持するようにした.**
These transitions correspond to pairs of states of the form s and s·r.
これらの**遷移は、sとs-rという形の状態のペアに対応**している.
Thus, the number of transitions required per state is bounded by the number of items rather than by an amount exponential in k in the worst case.
したがって、**1つの状態に必要な遷移の数は、最悪の場合、kの指数関数的な量ではなく、アイテムの数によって制限される**のである.(i.e.過去に観測された遷移のパターンのみを遷移確率に考慮する...!!)
The non-zero transitions are stored explicitly, and as can be inferred from Table 2, their number is much smaller than the total number of entries in the explicit transition matrix.
**非ゼロ遷移は明示的に保存され、表2から推測できるように、その数は明示的遷移行列の総エントリ数よりはるかに少ない**.
And while much memory is still required, in Section 6.2, we show that these requirements are not too large for modern computers to handle..
また、多くのメモリが必要であるが、6.2節では、これらの要件は現代のコンピュータが扱うには大きすぎないことを示す.

Moreover, we do not compute a policy choice for a state that was not encountered in our training data.
また、**訓練データで遭遇しなかったstateに対する方策選択を計算することはない**.
When the value of such a state is needed for the computation of an optimal policy of some observed state, we simply use its immediate reward.
このような状態の値が、ある観測された状態の最適なポリシーの計算に必要な場合、単にその即時報酬を使用する.
That is, if the sequence hx, y,zi did not appear in the training data, we do not calculate a policy for it and assume its value to be R(z)—the reward for the last item in the sequence.
つまり、**$<x,y,z>$というシーケンスが学習データに現れなかった場合、そのポリシーは計算せず、その値をR(z)(シーケンスの最後のアイテムの報酬)と仮定する**のである.
Note that given the skipping and clustering methods we use, the probability of making a transition from some (observed) sequence hw, x, yi to hw, x, yi is not zero even though hx, y,zi was never observed.
なお、スキップやクラスタリングの手法を用いると、ある（観測された）シーケンス$<w, x, y>$から$<x, y,z>$へ遷移する確率は、$x, y,z$ が一度も観測されていなくてもゼロにはならない.
This approximation, although risky in general MDPs, is motivated by the fact that in our initial model, for each state there is a relatively small number of items that are likely to be selected; and the probability of making a transition into an un-encountered state is very low.
この近似は、一般的なMDPでは危険だが、今回の初期モデルでは、**各stateで選択されそうなアイテムが比較的少なく、未遭遇のstateに遷移する確率が非常に低いという事実に動機づけられている**.
Moreover, the reward (that is, profit) does not change significantly across different states, so, there are no “hidden treasures” in the future that we could miss..
しかも、異なるstateによって報酬(つまり利益)が大きく変わるわけではないので、将来を見逃してしまうような「隠し玉」は存在しないのである.

When a recommendation must be generated for a state that was not encountered in the past, we compute the value of the policy for this state online.
**過去に遭遇していないstateに対して推薦を生成する必要がある場合**、このstateに対するポリシーの値をオンラインで計算する.
This requires us to estimate the transition probabilities for a state that did not appear in our training data.
そのため、学習データに現れていないstateの遷移確率を推定する必要がある.
We handle such new states in the same manner that we handled states for which we had sparse data in the initial predictive model – that is, using the techniques of skipping, clustering, and finite mixture of unigram, bigram, and trigrams described in Section 3.2..
このような新しいstateは、最初の予測モデルでデータが疎な状態を扱ったのと同じ方法で、つまり、セクション3.2で説明したスキップ、クラスタリング、ユニグラム、ビッググラム、トリグラムの有限混合という手法で扱われる.

### Using the Independence of Recommendations. レコメンデーションの独立性を利用する。

One of the basic steps in policy iteration is policy determination.
policy iteration の基本的なステップのひとつに、方策決定がある.
At each iteration, we compute the best action for each state s – that is, the action satisfying:.
各反復において、各state $s$ に対する最適なアクションを計算する、つまり、以下を満たすアクションを計算する:

$$
\argmax_{R}[Rwd(s) + \gamma \sum_{s'\in S}tr(s, R, s')V_{i}(s')]
= \argmax_{R}
[Rwd(s) + \gamma (\sum_{r\in R}tr_{MDP}(s, r \in R, s\cdot r)V_{i}(s \cdot r) + \sum_{r \notin R}tr_{MDP}(s, r \notin R, s \cdot r))]
\tag{24}
$$

where tr(s,r ∈ R,s·r) and tr(s,r ∈/ R,s·r) follow the definitions above..
ここで、$tr_{MDP}(s, r \in R, s\cdot r)$ および $tr_{MDP}(s, r \notin R, s \cdot r)$ は全セクションで定義したものである.

The above equation requires maximization over the set of possible recommendations for each state.
上記の式は、各stateに対して可能な推薦アイテムのセットに対する最大化を要求している.
The number of possible recommendations is n κ , where n is the number of items and κ is the number of items we recommend each time.
推薦可能なアイテム数は$n^k$ 、ここでnはアイテムの数、κは毎回推薦するアイテムの数である.
To handle this large action space, we make use of our independence assumption.
**この大きな行動空間を扱うために、私たちは独立性の仮定を利用する**.
Recall that we assumed that the probability that a user buys a particular item depends on her current state, the item, and whether or not this item is recommended.
**ユーザが特定の商品を購入する確率は、ユーザの現在の状態、その商品、そしてその商品が推薦されているか否かに依存すると仮定したこと**を思い出してください.
It does not depend on the identity of the other recommended items.
他の推薦アイテムの同一性には依存しない.
The following method uses this fact to quickly generate an optimal set of recommendations for each state..
次の方法は、この事実を利用して、各 state に最適な推薦のセットを素早く生成するものである.

Let us define $\Delta(s,r)$ – the additional value of recommending r in state s:.
ここで、$\Delta(s,r)$を、**状態sにおいてrを推薦することの付加価値**-と定義する:

$$
\Delta(s,r) = (tr(s,r \in R, s \cdot r) - tr(s, r \notin R, s \cdot r))V(s \cdot r).
\tag{25}
$$

Now define
では、付加価値を最大にするような推薦アイテムリストを以下のように定義します:

$$
R^{s, k}_{max \Delta} = {r_1, \cdots, r_k| \Delta(s, r_1) \geq \cdots \geq \Delta(s, r_k)
\\
\And \forall r \neq r_i(i = 1, \cdots,k), \Delta(s, r_k) \geq \Delta(s,r)
}
\tag{26}
$$

R s,κ max∆ is the set of κ items that have the maximal ∆(s,r) values..
$R^{s, k}_{max \Delta}$ は、$\Delta(s,r)$の値が最大となるk個のアイテムの集合である.

#### Theorem 1 定理1

R s,κ max∆ is the set that maximizes Vi+1(s) – that is,.
$R^{s, k}_{max \Delta}$ は、$V_{i+1}(s)$を最大化する集合である、つまり...

$$
V_{i+1}(s) = Rwd(s) +
\gamma(\sum_{r \in R^{s, k}_{max \Delta}}tr(s,r \in R, s\cdot r)V_i(s \cdot r) +
\sum_{r \notin R^{s, k}_{max \Delta}} tr(s, r \notin R, s \cdot r)V_i(s \cdot r)).
\tag{27}
$$

#### Proof.

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
本仮定の下で、**各ステージで複数のアイテムを推薦する場合の最適なポリシーを見つける複雑さは、単一のアイテムを推薦する場合の最適なポリシーを計算する複雑さと変わらない**.

By construction, our MDP optimizes site profits.
このように、私たちのMDPは、サイトの利益を最適化する.
In particular, the system does not recommend items that are likely to be bought whether recommended or not, but rather recommends items whose likelihood of being purchased is increased when they are recommended.
特に、**推薦してもしなくても買われる可能性が高いものを推薦するのではなく、推薦すると買われる可能性が高くなるものを推薦するようにした**.
Nonetheless, when recommendations are based solely on lift, it is possible that many recommendations will be made for which the absolute probability of a purchase (or click) is small.
**しかし、リフトだけでレコメンドすると、購入(クリック)される絶対確率が低いレコメンドが多くなる可能性がある**.
In this case, if recommendations are seldom followed, users might start ignoring them altogether, making the overall benefit zero.
この場合、推奨事項がほとんど守られないと(?)、ユーザはそれを完全に無視するようになり、全体の利益はゼロになってしまうかもしれない.
Our model does not capture such effects.
私たちのモデルは、そのような効果を捉えていない.
One way to remedy this possible problem is to alter the reward function so as to provide a certain immediate reward for the acceptance of a recommendation.
このような問題を解決する一つの方法として、推薦を受けるとすぐに一定の報酬が得られるように報酬機能を変更することが考えられる.
Another way to handle this problem is to recommend a book with a large MDP score only if the probability of buying it passes some threshold.
この問題を扱う別の方法として、MDPスコアが大きい本を購入する**確率がある閾値を超えた場合にのみ推薦する**方法がある.
We did not find it necessary to introduce these modifications in our current system..
現在のシステムでは、このような改良を加える必要はないと考えている.

## 5.3. Updating the Model Online オンラインでモデルを更新する。

Once the recommender system is deployed with its initial model, we need to update the model according to actual observations.
レコメンダーシステムが初期モデルで展開された後は、**実際の観測結果に応じてモデルを更新する必要がある**.
One approach is to use some form of reinforcement learning— methods that improve the model after each recommendation is made.
強化学習と呼ばれる、推薦が行われるたびにモデルを改良していく方法を用いるのも一つの方法である.
Although such models need little administration to improve, the implementation requires many calls and computations by the recommender system online, which will lead to slower responses—an undesirable result.
このようなモデルは、改良のための管理はほとんど必要ないが、その実装には、推**薦システムがオンラインで多くの呼び出しと計算を行う必要があり、レスポンスが遅くなるという好ましくない結果を招く**.
A simpler approach is to perform off-line updates at fixed time intervals.
**よりシンプルな方法として、一定の時間間隔でオフラインの更新を行う方法がある**.
The site need only keep track of the recommendations and the user selections and, say, once a week use those statistics to build a new model and replace it with the old one.
サイトでは、**推薦内容とユーザの選択を記録し、例えば週に一度、それらの統計情報を使って新しいモデルを構築し、古いモデルと置き換えるだけでいい**のである.
This is the approach we used..
このようなアプローチで臨んだ.

In order to re-estimate the transition function the following counts are obtained from the recently collected statistics:.
**遷移関数を再推定するため**に、最近収集した統計から以下のカウントを取得した.

- $c_{in}(s,r,s·r)$—the number of times the r recommendation was accepted in state s. $c_{in}(s,r,s·r)$-状態sでrの推薦が受け入れられた回数.

- $c_{out}(s,r,s·r)$—the number of times the user took item r in state s even though it was not recommended, $c_{out}(s,r,s·r)$-状態sにおいて、推薦されていないにもかかわらず、ユーザがアイテムrを取った回数.

- $c_{total}(s,s·r)$—the number of times a user took item r while being in state s, regardless of whether it was recommended or not. $c_{total}(s,s·r)$-ユーザが状態sの時にアイテムrを摂取した回数(推薦されたか否かに関わらず).

We compute the new counts and the new approximation for the transition function at time t +1 based on the counts and probabilities at time t as follows:.
時刻tにおけるカウントと確率に基づいて、時刻t+1の新しいカウントと遷移関数の新しい近似を次のように計算する.

$$
c^{t+1}_{in}(s,r,s·r) = c^t_{in}(s, r, s \cdot r) + count(s, r, s\cdot r)
\tag{29}
$$

$$
c^{t+1}_{total}(s,s·r) = c^t_{total}(s, s \cdot r) + count(s, s\cdot r)
\tag{30}
$$

$$
c^{t+1}_{out}(s,r,s·r) = c^t_{out}(s, r, s \cdot r) + count(s, s\cdot r) - count(s, r, s\cdot r)
\tag{31}
$$

$$
tr(s, r \in R, s\cdot r) = \frac{c^{t+1}_{in}(s,r,s·r)}{c^{t+1}_{total}(s,s·r) }
\tag{32}
$$

$$
tr(s, r \notin R, s\cdot r) = \frac{c^{t+1}_{out}(s,r,s·r)}{c^{t+1}_{total}(s,s·r) }
\tag{33}
$$

Note that at this stage the constants αs,r and βs,r no longer play a role—they were used only to generate the initial model.
この段階では、**定数$\alpha_{s,r}$と$\beta_{s,r}$はもはや役割を果たさず、初期モデルの生成にのみ使用されたことに注意してください**.
We still need to define how the counts at time t = 0 are initialized.
時刻t = 0のカウントがどのように初期化されるかを定義する必要がある.
We showed in section 5.1.1 how the transition function tr is initialized, and now we define:.
5.1.1節で遷移関数$tr$の初期化方法を示したが、ここでは次のように定義する:

$$
c^{0}_{in}(s,r,s·r) = \xi_s \cdot tr(s, r, s\cdot r)
\tag{34}
$$

$$
c^{0}_{out}(s,r,s·r) = \xi_s \cdot tr(s, r, s\cdot r)
\tag{35}
$$

$$
c^{0}_{total}(s,s·r) = \xi_s
\tag{36}
$$

where ξs is proportional to the number of times the state s was observed in the training data (in our implementation we used 10 · count(s)).
ここで、$\xi_s$ は**学習データでstate sが観測された回数に比例する**(定数)(我々の実装では、$10 \cdot count(s)$ を使用).
This initialization causes states that were observed infrequently to be updated faster than states that were observed frequently and in whose estimated transition probabilities we have more confidence.10.
この初期化により、観測頻度の低いstateは、観測頻度が高く推定遷移確率に信頼性があるstateよりも速く(??)更新される.

To ensure convergence to an optimal solution, the system must obtain accurate estimates of the transition probabilities.
最適解に収束させるためには、システムは遷移確率の正確な推定値を得る必要がある.
This, in turn, requires that for each state s and for every recommendation r, we observe the response of users to a recommendation of r in state s sufficiently many times.
そのためには、各state $s$ と各推薦 $r$ について、state $s$ におけるrの推薦に対するユーザの反応を十分な回数観察する必要がある.
If at each state the system always returns the best recommendations only, then most values for count(s,r,s·r) would be 0, because most items will not appear among the best recommendations.
もし、各stateで常に ベストレコメンデーションのみを返すシステムであれば、ほとんどのアイテムがベストレコメンデーションに含まれないため、$count(s,r, s \cdot r)$ の値は0となる.
Thus, the system needs to recommend non-optimal items occasionally in order to get counts for those items.
そのため、最適でないアイテムを推薦することで、そのアイテムのカウントを獲得する必要があるである.(探索の要素!!)
This problem is widely known in computational learning as the exploration versus exploitation tradeoff (for some discussion of learning rate decay and exploration vs.
この問題は、計算機学習において、**探索と利用のトレードオフ**として広く知られている(学習率の減衰と探索と利用のトレードオフに関するいくつかの議論については、こちら)
exploitation in reinforcement learning, see, for example Kaelbling et al.
強化学習での活用は、例えばKaelbling et al.
(1996) and Sutton and Barto (1998)).
(1996)、Sutton and Barto(1998))がある.
The system balances the need to explore unobserved options in order to improve its model and the desire to exploit the data it has gathered so far in order to get rewards..
このシステムは、**モデルを改良するために未観測のオプションを探索(explore)する必要性**と、報酬を得るためにこれまでに収集したデータを活用(exploit)する必要性のバランスをとっている.

One possible solution is to select some constant ε, such that recommendations whose expected value is ε-close to optimal will be allowed—for example, by following a Boltzmann distribution:.
一つの可能な解決策は、ある定数$\epsilon$を選択することで、期待値が$\epsilon$に近いレコメンデーションは、例えば、ボルツマン分布に従うことで、最適になるようにすることである：

$$
\tag{37}
$$

with an ε cutoff—meaning that only items whose value is within ε of the optimal value will be allowed.
↑を設定し、その値が最適値からε以内にあるアイテムのみを許可することを意味する.
The exact value of ε can be determined by the site operators.
εの正確な値は、サイト運営者が決定することができる.
The price of such a conservative exploration policy is that we are not guaranteed convergence to an optimal policy.
**このような保守的な探索方針の代償**として、最適な方針への収束が保証されないことが挙げられる.
Another possible solution is to show the best recommendation on the top of the list, but show items less likely to be purchased as the second and third items on the list.
また、**一番お勧めの商品をリストの一番上に表示し、購入の可能性が低いものをリストの2番目、3番目に表示する方法**も考えられる.(=これは推薦システム \* 強化学習で特有かも!)
In our implementation we use a list of three recommendations where the first one is always the optimal one, but the second and third items are selected using the Boltzman distribution without a cutoff..
我々の実装では、3つの推薦リストを使用し、最初のものは常に最適なものであるが、2番目と3番目のアイテムは、カットオフなしでボルツマン分布を用いて選択されるものである.

We also had to equip our system to change with frequent changes (for example, addition and removal of items).
また、頻繁な変更(例えば、アイテムの追加や削除など)に対応できるような装備にする必要があった.
When new items are added, users will start buying them and positive counts for them will appear.
新しいアイテムが追加されると、ユーザはそれを買い始め、そのアイテムのプラスカウントが表示されるようになる.
At this stage, our system adds new states for these new items, and the transition function is expanded to express the transitions for these new states.
この段階で、私たちのシステムは、これらの新しいアイテムのための新しい state を追加し、これらの新しい state のための遷移を表現するために遷移関数を拡張する.
Of course, prior to updating the model, the system is not able to recommend those new items (the well-known “cold start” problem (Good et al., 1999) in recommender systems).
もちろん、モデルを更新する前は、システムはそれらの新しいアイテムを推薦することができない(推薦システムにおけるよく知られた「コールドスタート」問題(Good et al.，1999)).
In our implementation, when the first transition to a state s·r is observed, its probability is initialized to 0.9 the probability of the most likely next item in state s with ξs = 10.
本実装では、状態 $s\cdot r$ への最初の遷移が観測されたとき、その確率は、状態sで最も可能性の高い次のアイテムの確率を$\xi_s = 10$として、0.9に初期化される.
This approach causes the new items to be recommended quite frequently..
**この方法だと、新しいアイテムが推薦される頻度が高くなりますね**.

One possible approach to handling removed items is to do nothing to our system, in which case the transition probabilities slowly decay to zero.
**削除されたアイテムを処理する方法**として考えられるのは、システムに何もしないことであり、その場合、遷移確率はゆっくりとゼロに減衰する.
Using this approach, however, we may still insert deleted items into the list of recommended items – an undesirable feature.
しかし、この方法では、**削除されたアイテムが推奨アイテムに挿入される可能性があり**、好ましくない機能.
Consequently, in our Mitos implementation, items are programmatically removed from the model during offline updates.
そのため、Mitosの実装では、オフラインアップデート時にアイテムをプログラムから削除している.
Another solution that we have implemented but not evaluated is to use weighted data and to exponentially decay the weights in time, thus placing more weight on more recently observed transitions..
もう一つの解決策は、**重み付けされたデータを使用し、時間的に指数関数的に減衰させることで、より最近観測された遷移に重きを置く**というもの.（評価はしていません）.

# 6. Evaluation of the MDP Recommender Model MDPレコメンダーモデルを評価する

The main thesis of this work is that (1) recommendation should be viewed as a sequential optimization problem, and (2) MDPs provide an adequate model for this view.
本研究の主要なテーゼは、**（1）推薦を逐次最適化問題として捉えるべきであり、（2）MDPはこの見解に適したモデルを提供する**、というものである.
This is to be contrasted with previous systems which used predictive models for generating recommendations.
これは、従来のシステムが予測モデルを用いてレコメンデーションを生成していたのと対照的である.
In this section, we present an empirical validation of our thesis.
本節では、本論文の実証的な検証を紹介する.
We compare the performance of our MDP-based recommender system (denoted MDP) with the performance of a recommender system based on our predictive model (denoted MC) as well as other variants..
**MDPに基づく推薦システム（MDPと表記）と、予測モデルに基づく推薦システム(MCと表記)、および他の変種との性能を比較した**.

Our studies were performed on the online book store Mitos (www.mitos.co.il) from August, 2002 till April, 2004.
2002年8月から2004年4月まで、オンライン書店「ミトス」（www.mitos.co.il）で調査を行った.
During our evaluations, approximately 5000 − 6000 different users visited the Mitos site daily.
私たちの評価では、毎日約5000〜6000人のユーザがミトスのサイトを訪れていた.
Of those, around 900 users inserted items into their basket, thus entering our data-set.11 On average, each customer inserted 1.97 items into the shopping basket.
このうち、約900人のユーザが買い物かごに商品を入れ、データセットに登録された. 平均して、1人当たり1.97個の商品を買い物かごに入れた.
Over 15,000 items were available for purchase on the site..
サイトでは15,000点以上のアイテムが販売されていた.

Users received recommendations when adding items to the shopping cart.12 The recommendations were based on the last k items added to the cart ordered by the time they were added.
ショッピングカートに商品を追加する際に、ユーザにおすすめの商品を紹介した. **このおすすめ商品は、カートに追加された商品のうち、追加された時間順に並んだ直近のk個の商品に基づいている**.
An example is shown in Figure 4 where the three book covers at the bottom are the recommended items.
例として、図4に示すように、下部の3つのブックカバーがおすすめアイテムであることを示す.
Every time a user was presented with a list of recommendations on either page, the system stored the recommendations that were presented and recorded whether the user purchased a recommended item.
どちらのページでも、ユーザにおすすめ商品のリストが提示されるたびに、提示されたおすすめ商品を記憶し、**ユーザがおすすめ商品を購入したかどうかを記録した.**
Cart deletions were rare and ignored.
カートの削除は稀であり、無視された.
Once every two or three weeks, a process was run to update the model given the data that was collected over the latest time period.13.
**2～3週間に一度、最新の期間に収集されたデータをもとに、モデルを更新するプロセスが実行された**.

We compared the MDP and MC models both in terms of their value or utility to the site as well as their computational costs..
MDPモデルとMCモデルを、**現場での価値や有用性、計算コストの両面から比較検討**した.

## 6.1. Utility Performance ユーティリティの性能

Our first set of results is based on the assumption that the transition function we learn for our MDP using data collected with recommendations, provides the the best available model of user behavior under recommendation.
最初の結果は、レコメンデーションで収集されたデータを用いてMDPに学習させた遷移関数が、レコメンデーション下のユーザ行動の最良のモデルを提供するという仮定に基づいている.
Under this assumption, we can measure the effect of different recommendation policies.
この前提のもと、さまざまな推薦ポリシーの効果を測定することができる.
An important caveat is that the states in our MDP correspond to truncated (that is, last k) user sequences.
**重要な注意点は、MDPの state は切り捨てられた(つまり最後のk個の)ユーザーシーケンスに対応すること**である.
Thus, the model does not exclude repeated purchases of the same item.
したがって、**このモデルでは、同じ商品の繰り返し購入は除外されない**.
Despite this shortcoming, we proceeded with the evaluation..
このような欠点があるにもかかわらず、我々は評価を進めた.

As discussed above, a predictive model can answer queries in the form Pr(x|h)—the probability that item x will be purchased given user history h.
上述したように、予測モデルは、$Pr(x|h)$-**ユーザー履歴hが与えられた場合にアイテムxが購入される確率**-という形式のクエリに答えることができる.
Recommender systems may employ different strategies when generating recommendations using such a predictive model.
推薦システムは、このような予測モデルを用いて推薦を生成する際に、異なる戦略を採用することができる.
Assuming that an MDP formalizes the recommendation problem well, we may use the learned MDP model to evaluate these strategies.
MDPが推薦問題をうまく定式化していると仮定すると、**学習したMDPモデルを用いて、これらの戦略を評価することができる.**(??)
The evaluation of the quality of different possible policies for the MDP, each corresponding to a popular approach to recommending, may shed light on the preferred recommendation strategy..
MDPで考えられる様々な方策(それぞれ一般的な推薦のアプローチに対応する)の質を評価することで、好ましい推薦戦略を明らかにすることができるかもしれない.

The MDP model was built using data gathered while the model was running in the site with incremental updates (as described above) for almost a year.
MDPモデルは、約1年間、サイト内でインクリメンタルアップデート(上記のようなアップデート)を行いながら、収集したデータを使って構築した.
We compared four policies, where the first policy uses information about the effect of recommendations, and the remaining policies are based on the predictive model solely:.
最初のポリシーはレコメンドの効果に関する情報を使用し、残りのポリシーは予測モデルのみに基づいている：**4つのポリシーを比較**した.

- Optimal – recommends items based on optimal policy for the MDP. Optimal - MDPに最適なポリシーに基づいたアイテムを推薦する.

- Greedy – recommends items that maximize Pr(x|h)· R(x) (where Pr(x|h) is the probability of buying item x given user history h, and R(x) is the value of x to the site – for example, net profit). - $Pr(x|h)\cdot R(x)$ を最大化するアイテムを推薦する(ここで、$Pr(x|h)$はユーザーの履歴hが与えられた場合にアイテムxを購入する確率、$R(x)$ はサイトにとってのxの価値（例えば純利益）である).

- Most likely – recommends items that maximize Pr(x|h).最も可能性が高い - Pr(x|h)を最大化するアイテムを推薦する.

- Lift – recommends items that maximize $Pr(x|h)/Pr(x)$ , where Pr(x) is the prior probability of buying item x.Pr(x|h)/Pr(x)$を最大化するアイテムを推薦する. ここで、Pr(x)はアイテムxを購入する事前確率である.

To evaluate the different policies we ran a simulation of the interaction of a user with the system.
異なるポリシーを評価するために、ユーザとシステムとのInteractionのシミュレーションを実行した.
During the simulation the system generated a list of recommended items R, from which the simulated user selected the next item, using the distribution tr(s,R,s· x)—the probability that the next selected item is x given the current state s and the recommendation list R, simulating the purchase of x by the user.
シミュレーション中、システムは推薦アイテムのリストRを生成し、そこから模擬ユーザが次のアイテムを選択する。(遷移確率質量の)分布$tr(s,R,s \cdot x)$-**現在のstate sと推薦リストRが与えられたときに、次の選択アイテムがxである確率**-を用いて、ユーザによるx購入のシミュレーションをした.
The length of user session was taken from the learned distribution of user session length in the actual site.
ユーザセッションの長さは、実際のサイトにおけるユーザセッションの長さの学習済み分布から取得した.(?)
We ran the simulation for 10,000 iterations for each policy, and calculated the average accumulated reward for user session..
各ポリシーについて10,000回の反復シミュレーションを行い、ユーザセッションの平均累積報酬を算出した.

The results are presented in Table 3.
その結果を表3に示す.
The calculated value for each policy is the sum of discounted profit in (New Israeli Shekels) averaged over all states.
各方策の計算値は、全state で平均した（新イスラエル・シェケル）割引利益の合計である.
We used a weighted average, where the weight of each state was the probability of observing it.
各state の重みを観測する確率とした加重平均を使用した.
Obviously, an optimal policy results in the highest value.
当然ながら、optimal policyは最も高い値をもたらす.
However, the differences are small, and it appears that one can use the predictive model alone with very good results..
しかし、**その差は小さく、予測モデルだけでも非常に良い結果が得られると思われる**.

Next, we performed an experiment to compare the performance of the MDP-based system with that of the MC-based system.
次に、MDPベースのシステムとMCベースのシステムの性能を比較する実験を行った.
In this experiment, each user entering the site was assigned a randomly generated cart-id.
この実験では、サイトに入る各ユーザに、ランダムに生成されたカートIDが割り当てられた.
Based on the last bit of this cart-id, the user was provided with recommendations by the MDP or MC.
このcart-idの最終ビットに基づき、MDPまたはMCからユーザにレコメンドが提供された.(要するにA/Bテスト!!)
Reported mean profits were calculated for each user session (a single visit to the site).
報告された平均利益は、ユーザセッション(サイトへの1回の訪問)ごとに計算された.
Data gathered in both cases was used to update both models.14.
この2つのケースで収集されたデータは、両モデルのアップデートに使用された.

The deployed system was built using three mixture components, with history length ranging from one to three for both the MDP model and the MC model.
展開されたシステムは、MDPモデル、MCモデルともに履歴長が1～3までの3つの混合コンポーネントを用いて構築された.
Recommendations from the different mixture components were combined using an equal (0.33) weight.
異なる混合成分からの勧告は、等しい(0.33)重み付けを使用して結合された.
We used the policy-iteration procedure and approximations described in Section 5 to compute an optimal policy for the MDP.
セクション5で説明したpolicy-iteration手順と近似を用いて、MDPの最適方策を計算した.
Our model encoded approximately 25,000 states in the two top mixture components (k = 2, k = 3).
我々のモデルでは、上位2つの混合成分（k = 2, k = 3）に約25,000のstate を符号化した.
The reported results were gathered after the model was running in the site with incremental updates (as described above) for almost a year..
今回発表された結果は、**サイト内で約1年間、段階的なアップデート(上記のような方策=遷移関数の更新)を行いながらモデルを稼働させた後に得られたもの**である.

During the testing period, 50.7% of the users who made at least one purchase were shown MDP-based recommendations and the other 49.3% of these users were shown MC-based recommendations.
テスト期間中、少なくとも1回購入したユーザの50.7%にMDPベースのレコメンデーションが表示され、残りの49.3%にMCベースのレコメンデーションが表示されました.
For each user, we computed the average site profit per session for that user, leaving out of consideration the first purchase made in each session.
各ユーザについて、各セッションで最初に購入されたものは考慮せず、そのユーザのセッションごとの平均サイト利益を計算した.
The first item was excluded as it was bought without the benefit of recommendations, and is therefore irrelevant to the comparison between the recommender systems.15.
最初の商品は、レコメンデーションの恩恵を受けずに購入したため、レコメンダーシステム間の比較には無関係であるとして除外した.

The average site profit generated by the users was 28% higher for the MDP group.16 We used a permutation test (see, for example, Yeh (2000)) to see how likely it would be for a difference this large to emerge if there were in fact no systematic difference in the effectiveness of the two recommendation methods.17 We randomly generated 10000 permutations of the assignments of session profits to users, for each permutation computing the ratio of average session profits between the MDP and the MC groups.
2つの推薦手法の有効性に系統的な差がない場合、これほど大きな差が生じる可能性があるのか、順列検定（例えば、Yeh (2000)を参照）を用いて検討した. セッション利益の割り当てをランダムに10000通り生成し、それぞれの順列について、MDPグループとMCグループの平均セッション利益の比率を計算した.
With only 8% of these random assignments was the ratio as large as (or larger than) 1.282.
このうち、1.282と同程度（またはそれ以上）の比率となったのは、わずか8％であった.
Therefore, the better performance of the MDP recommender is statistically significant with p = 0.08 by a one-tailed permutation test..
したがって、**MDPレコメンダーの性能向上は**、片側並べ替え検定でp = 0.08と**統計的に有意であった**ことがわかる.

There are two possible sources for the observed improvement—the MDP may be generating more sales or sales of more expensive items.
これは、**MDPがより多くのアイテム購入を生み出しているか、より高価な商品の売上を生み出しているかの2つの可能性がある**.
In our experiment, the average number of items bought per user session was 6.8% in favor of the MDP-based recommender (p = 0.15), whereas the average price of items was 4% higher in favor of the MDP-based recommender (p = 0.04).
実験では、ユーザセッションあたりの平均購入アイテム数は、MDPベースのレコメンダーが6.8%有利であったのに対し（p = 0.15）、アイテムの平均価格はMDPベースのレコメンダーが4%有利であった（p = 0.04）．
Thus, both effects may have played a role..
したがって、両方の効果が作用している可能性がある.

In our second and last experiment, we compared site performance with and without a recommender system.
最後の2つ目の実験では、レコメンダーシステムを導入した場合と導入しない場合のサイトパフォーマンスを比較した.
Ideally, we would have liked to assign users randomly to an experience with and without recommendations.
理想を言えば、レコメンデーションのある体験とない体験にランダムにユーザを割り当てることができればよかったが.
This option was ruled-out by the site owner because it would have led to a non-uniform user experience.
この選択肢は、ユーザエクスペリエンスが統一されないという理由で、サイトオーナーによって除外された.
Fortunately, the site owner was willing to remove the recommender system from the site for one week.
幸い、サイトオーナーが1週間だけレコメンドシステムをサイトから外してくれることになった.(=なるほど...! A/Bテストではない!)
Thus, we were able to compare average profits per user session during two consecutive weeks – one with recommendations and one without recommendations.18 We found that, when the recommender system was not in use, average site profit dropped 17% (p = 0.0).
その結果、レコメンダーシステムを使用しない場合、サイトの平均利益は17%減少することがわかりました（p=0.0）.
Although, we cannot rule out the possibility that this difference is due to other factors (for example, seasonal effects or special events), these result are quite encouraging..
**この差が他の要因（例えば、季節的な影響や特別なイベントなど）によるものである可能性は否定できませんが、この結果は非常に有望である**.

Overall, our experiments support the claims concerning the added value of using recommendations in commercial web sites and the validity of the MDP-based model for recommender systems..
本実験は、商用サイトにおけるレコメンデーションの付加価値と、レコメンデーションシステムのためのMDPベースのモデルの有効性に関する主張を支持するものであった.

## 6.2. Computational Analysis Computational Analysis（計算解析）。

In this section, we compare computational costs of the MDP-based and the Predictor recommender system..
ここでは、**MDPベースとPredictorレコメンダーシステムの計算コスト**を比較する。

Our comparison uses the transaction data set and corresponding models described in Section 4.
この比較では、セクション4で説明したトランザクションデータセットと対応するモデルを使用する.
In addition to using the full data set, we measured costs associated with smaller versions of the data in which transactions among only the the top N items were considered, in order to demonstrate the effect of the size of the data-set on performance..
また、データセットの規模がパフォーマンスに与える影響を示すため、フルセットに加えて、上位Nアイテムのみの取引を考慮した小規模なデータセットに関連するコストを測定した.

First, let us consider the time it takes to make a recommendation.
まず、**推薦にかかる時間**について考えてみましょう.
Recommendation time is typically the most critical of computational costs.
**レコメンデーション時間は、一般的に計算コストの中で最も重要なもの**である.
If recommendation latency is noticeable, no reasonable site administrator will use the recommender system.
レコメンデーションの遅延が目立つようでは、合理的なサイト管理者はそのレコメンダーシステムを利用しないだろう.
Table 5 shows the number of recommendations generated per second by the recommender system.
表5は、レコメンダーシステムが1秒間に生成するレコメンド数を示している.
The results show that the MDP model is faster.
その結果、MDPモデルの方が高速であることがわかった.
This result is due to the fact that, with the MDP model, we do almost no computations online.
この結果は、**MDPモデルで、オンラインでほとんど計算をしないこと**に起因している.
While predicting, the model simply finds the proper state and returns the state’s pre-calculated list of recommendations..
予測中は、モデルは単に適切な state を見つけ、その state に対応する、**事前に計算された推薦リストを返す**.

The price paid for faster recommendation is a larger memory footprint.
**より高速な推薦のために支払われる代償は、より大きなmemory footprintである**.
Table 6 shows the amount of memory needed to build and store a model in megabytes.
表6に、モデルの構築と保存に必要なメモリ量をメガバイトで示す.
The MDP model requires more memory to store than the Predictor model, due to the structured representation of the Predictor model using a collection of decision trees..
**MDPモデルはPredictorモデルより多くのメモリを必要とする**が、これはPredictorモデルが決定木の集合体を用いて構造的に表現されているからである.

Finally, we consider the time needed to build a new model.
最後に、新しいモデルを構築するのに必要な時間を考慮する.
This computational cost is perhaps the least important parameter when selecting a recommender system, as model building is an offline task executed at long time intervals (say once a week at most) on a machine that does not affect the performance of the site.
モデル構築は、サイトのパフォーマンスに影響を与えないマシンで、長い時間間隔(せいぜい週に1回程度)で実行されるオフラインタスクであるため、この計算コストは、レコメンダーシステムを選択する際に最も重要ではないパラメータと言えるかもしれない.
That being said, as we see in Table 4, the MDP model has the smallest build times..
とはいえ、表4にあるように、**MDPモデルは構築時間が最も短い**.(=MDPはオンライン更新的な事だから??)

Overall the MDP-based model is quite competitive with the Predictor model.
全体的にMDPベースのモデルは、Predictorモデルとかなり競合している.
It provides the fastest recommendations at the price of more memory use, and builds models more quickly.
**より多くのメモリを使用する代償として最速のレコメンデーションを提供し、より速くモデルを構築する**.

# 7. Discussion ディスカッション

This paper describes a new model for recommender systems based on an MDP.
本論文では、MDPに基づくレコメンダーシステムの新しいモデルについて説明する.
Our work presents one of a few examples of commercial systems that use MDPs, and one of the first reports of the performance of commercially deployed recommender system.
私たちの研究は、MDPを用いた商用システムの数少ない例の一つであり、商用に展開されたレコメンダーシステムの性能に関する最初の報告の一つでもある.
Our experimental results validate both the utility of recommender systems and the utility of the MDP-based approach to recommender systems..
この実験結果は、推薦システムの有用性と推薦システムに対するMDPベースのアプローチの有用性の両方を検証するものである.

To provide the kind of performance required by an online commercial site, we used various approximations and, in particular, made heavy use of the special properties of our state space and its sequential origin.
オンライン商業サイトに求められる性能を実現するために、さまざまな近似式を用い、**特に state space の特殊な性質とそのsequentialな起源を大いに利用した**.
Whereas the applicability of these techniques beyond recommender systems is not clear, it represents an interesting case study of a successful real system.
これらの技術のレコメンダーシステム以外への適用性は明確ではありませんが、実際のシステムの成功例として興味深い事例である.
Moreover, the sequential nature of our system stems from the fact that we need to maintain history of past purchases in order to obtain a Markovian state space.
また、**本システムの逐次性(sequential nature)は、マルコフのstate spaceを得るために、過去の購入履歴を保持する必要があることに起因**している.
The need to record facts about the past in the current state arises in various domains, and has been discussed in a number of papers on handling non-first-order Markov reward functions (see, for example, Bacchus et al.(1996) or Thiebaux et al.(2002))..
**過去に関する事実を現在の state に記録する必要性**は様々なドメインで生じ、非一次マルコフ報酬関数の取り扱いに関する多くの論文で議論されてきた(例えば、Bacchus et al.(1996)やThiebaux et al.(2002))..

Another interesting technique is our use of off-line data to initialize a model that can provide adequate initial performance..
また、**オフラインのデータを使ってモデルを初期化することで、十分な初期性能を発揮させるという手法も興味深い.**

In the future, we hope to improve our transition function on those states that are seldom encountered using generalization techniques, such as skipping and clustering, that are similar to the ones we employed in the predictive Markov chain model.
今後は、予測MCモデルで採用したようなスキップやクラスタリングなどの汎化手法を用いて、**めったに遭遇しないような state の遷移関数を改善したい**と考えています。
Other potential improvements are the use of a partially observable MDP to model the user.
その他の改善点として、ユーザをモデル化するために部分観測可能なMDPを使用することが考えられる.(??)
As a model, this is more appropriate than an MDP, as it allows us to explicitly model our uncertainty about the true state of the user (Boutilier, 2002)..
モデルとしては、ユーザの真の state に関する不確実性を明示的にモデル化できるため、MDPよりも適切である（Boutilier, 2002）.

In fact, our current model can be viewed as approximating a particular POMDP by using a finite – rather than an unbounded – window of past history to define the current state.
実際、現在のモデルは、**現在の state を定義するために過去の履歴のウィンドウを無制限ではなく、有限のウィンドウを使用する**ことで、特定のPOMDP(POって何??)を近似していると見なすことができる.
Of course, the computational and representational overhead of POMDPs are significant, and appropriate techniques for overcoming these problems must be developed..
もちろん、POMDPの計算量や表現力のオーバーヘッドは大きく、これらの問題を克服するための適切な技術の開発が必要である.

Weaknesses of our predictive (Markov chain) model include the use of ad hoc weighting functions for skipping and similarity functions and the use of fixed mixture weights.
予測(マルコフ連鎖)モデルの弱点として、スキップや類似関数にアドホックな重み付け関数を使用していること、混合物の重みが固定であることが挙げられる.
Although the recommendations that result from our current model are (empirically) useful for ranking items, we have noticed that the model probability distributions are not calibrated.
現在のモデルから得られるレコメンデーションは、（経験的に）アイテムのランキングに有用ですが、モデルの確率分布が較正されていないことに気づいた.
Learning the weighting functions and mixture weights from data should improve calibration.
データから重み付け関数や混合重みを学習することで、キャリブレーションを向上させることができるはずである.
In addition, in informal experiments, we have seen evidence that learning case-dependent mixture weights should improve predictive accuracy..
また、非公式な実験では、ケースに依存した混合重みを学習することで、予測精度が向上することが確認されている.

Our predictive model should also make use of relations between items that can be explicitly specified.
予測モデルは、明示的に指定できるアイテム間の関係も利用する必要がある.
For example, most sites that sell items have a large catalogue with hierarchical structure such as categories or subjects, a carefully constructed web structure, and item properties such as author name.
例えば、物品を販売するサイトの多くは、カテゴリーやテーマなどの階層構造、綿密に構築されたウェブ構造、著者名などのアイテムプロパティを持つ大規模なカタログを用意している.
Finally, our models should incorporate information about users such as age and gender..
最後に、年齢や性別など、ユーザーに関する情報をモデルに取り込む必要がある.
