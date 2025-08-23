refs: https://medium.com/udemy-engineering/building-a-multi-armed-bandit-system-from-the-ground-up-a-recommendations-and-ranking-case-study-b598f1f880e1

# Building a Multi-Armed Bandit System from the Ground Up: A Recommendations and Ranking Case Study, Part I
多腕バンディットシステムをゼロから構築する：推薦とランキングのケーススタディ、パートI

# Introduction はじめに

In recent years, multi-armed bandits (MAB) have been enjoying a surge in popularity as explore-exploit balancing approaches continue to show success in a wide variety of applications. 
近年、マルチアームバンディット（MAB）は、探索と活用のバランスを取るアプローチがさまざまなアプリケーションで成功を収め続けているため、人気が急上昇しています。
One particularly successful application has been the use of multi-armed bandits for recommendations. 
**特に成功した応用の一つは、推薦のためのマルチアームバンディットの使用**です。
Introducing exploration into the recommendation approach helps address common recommendations problems, such as feedback loop bias and the cold-start issue. 
**推薦アプローチに探索を導入することで**(そうそう、これが本質なんだよな...!)、フィードバックループバイアスやコールドスタート問題など、一般的な推薦の問題に対処するのに役立ちます。
While the success of bandit approaches in industry is clearly very attractive, building a fully-working scalable MAB system from scratch presents a number of significant engineering, operational and data science challenges. 
業界におけるバンディットアプローチの成功は明らかに非常に魅力的ですが、完全に機能するスケーラブルなMABシステムをゼロから構築することは、多くの重要なエンジニアリング、運用、データサイエンスの課題を提示します。

In this two-part blog post, we will share our experience in creating a successful scalable, near real-time MAB system for the purpose of ranking in recommendations at our company, Udemy. 
この二部構成のブログ記事では、私たちの会社Udemyにおける推薦のランキングのために、成功したスケーラブルでほぼリアルタイムのMABシステムを作成する経験を共有します。

In this part (Part I), we will discuss what bandits are and why to use them for recommendations, and how to translate the ranking problem into a bandit problem. 
このパート（パートI）では、バンディットとは何か、なぜ推薦に使用するのか、そしてランキング問題をバンディット問題にどのように変換するかについて議論します。
We’ll also walk through the data science challenges that may arise during a practical application of bandits. 
また、バンディットの実際の応用中に発生する可能性のあるデータサイエンスの課題についても説明します。

Then in Part II, we will provide an overview of our production architecture and development environment, and will discuss the engineering challenges teams may face when deploying a similar system. 
次に、パートIIでは、私たちのプロダクションアーキテクチャと開発環境の概要を提供し、同様のシステムを展開する際にチームが直面する可能性のあるエンジニアリングの課題について議論します。

<!-- ここまで読んだ! -->

# What are Multi-Armed Bandits and Why Use Them?  
# マルチアームバンディットとは何か、なぜそれを使用するのか？

## Problem Setting
## 問題設定

Multi-armed bandits are a class of explore-exploit algorithms that are used to make decisions under uncertainty. 
マルチアームバンディットは、不確実性の下で意思決定を行うために使用される探索-活用アルゴリズムの一種です。
To help conceptually understand what we mean by an “explore-exploit algorithm,” it is best to consider the following problem setting, from which multi-armed bandits received their name.
「**探索-活用アルゴリズム(explore-exploit algorithm)**」とは何かを概念的に理解するためには、マルチアームバンディットがその名前を受けた以下の問題設定を考えるのが最適です。

![]()

The problem setting begins in a casino. 
この問題設定はカジノから始まります。
You walk in and are presented with a number of slot machines to choose from. 
あなたはカジノに入り、選択できるいくつかのスロットマシンが提示されます。
Each of these slot machines has an arm (lever) that you can pull, and when you do so, you receive some random reward (payout) sampled from that slot machine’s predetermined reward probability distribution. 
これらのスロットマシンのそれぞれには、引くことができるアーム（レバー）があり、それを引くと、そのスロットマシンの事前に定められた報酬確率分布からサンプリングされたランダムな報酬（支払い）を受け取ります。
Note that each slot machine has a different reward probability distribution, and these distributions are unknown to you when you first begin playing. 
各スロットマシンには異なる報酬確率分布があり、これらの分布は最初にプレイを始めたときにはあなたにはわかりません。

Your goal is to maximize your winnings from playing these slot machines. 
あなたの目標は、これらのスロットマシンをプレイして得られる winnings（勝ち金）を最大化することです。
Being a smart gambler, you came to the casino with a fixed amount of money you were willing to spend, so you only have a limited number of arm pulls to use. 
賢いギャンブラーであるあなたは、使うつもりのある固定の金額を持ってカジノに来たので、使用できるアームを引く回数は限られています。
If you knew the true reward probability distributions for each slot machine, then it would be very clear how to maximize your winnings in the long run: simply continuously play the slot machine’s arm whose reward distribution has the highest expected value. 
**もし各スロットマシンの真の報酬確率分布を知っていれば、長期的に winnings（勝ち金）を最大化する方法は非常に明確**です：単に報酬分布の期待値が最も高いスロットマシンのアームを継続的にプレイするだけです。

However, you do not know anything about these reward distributions at first, so you must use some of your limited arm pulls to explore and learn more about each arm’s expected reward, while also balancing exploitation of the arms you have seen to be best so far. 
しかし、最初はこれらの報酬分布について何も知らないため、限られたアームを引く回数の一部を使って探索し、各アームの期待報酬についてもっと学ぶ必要があります。また、これまでに見た中で最も良いアームの活用とのバランスも取る必要があります。
With only exploration, you would gain high confidence in each of the slot machine’s reward distributions, but would run out of arm pulls before you could profit off knowing the best arm to pull. 
探索だけを行うと、各スロットマシンの報酬分布に対する高い信頼を得ることができますが、最適なアームを引くことを知る前にアームを引く回数が尽きてしまいます。
With only exploitation, you might choose to continuously play a slot machine that is suboptimal, and fail to reap the benefits of the better machines. 
活用だけを行うと、最適でないスロットマシンを継続的にプレイすることになり、より良いマシンの利益を得ることができなくなります。

Clearly, we face the classic explore-exploit dilemma and need to achieve some type of balance between the two. 
明らかに、私たちは古典的な探索-活用のジレンマに直面しており、両者の間で何らかのバランスを達成する必要があります。
Multi-armed bandit algorithms are designed for this purpose: to optimally balance exploration and exploitation and help maximize your cumulative reward. 
マルチアームバンディットアルゴリズムは、この目的のために設計されています：探索と活用の最適なバランスを取り、累積報酬を最大化するのを助けるためです。

<!-- ここまで読んだ! --> 

## Definition 定義

The standard multi-armed bandit problem setup can be defined more formally as follows:
標準的なマルチアームバンディット問題の設定は、以下のようにより正式に定義できます。

- Bandits are a class of explore-exploit algorithms used to make decisions under uncertainty. They can be thought of as a simplified reinforcement learning algorithm. バンディットは、不確実性の下で意思決定を行うために使用される探索-活用アルゴリズムの一種です。これは、**簡略化された強化学習アルゴリズム**と考えることができます。

- Given a set of k arms (options) $A= \{a₁, a₂, …, aₖ\}$, the goal is to determine the best arm(s) to play to maximize the cumulative reward gain from playing these arms. $k$ 本のアーム（選択肢）のセット $A= \{a₁, a₂, …, aₖ\}$ が与えられたとき、目標は、これらのアームをプレイすることで得られる累積報酬を最大化するために、最良のアームを決定することです。

- When an arm $aᵢ$ is played at time $t$, we observe a reward $rₜ$ sampled from that arm’s reward probability distribution — no other rewards are observed for unplayed arms. We record this as an observation, which is an arm-reward pair $(aᵢᵗ, rᵢᵗ)$.
アーム $aᵢ$ が時刻 $t$ にプレイされると、そのアームの報酬確率分布からサンプリングされた報酬 $rₜ$ を観察します。プレイされていないアームに対しては他の報酬は観察されません。これを**観察(observation)**として記録し、アーム-報酬ペア $(aᵢᵗ, rᵢᵗ)$ とします。

- We devise a strategy to optimally decide which arm to select next in order to learn more about the true expected rewards for each arm, without showing a suboptimal arm too often. A strategy takes into account the history of arm-reward observations up until time $t-1$ and uses that history to decide what to pick at time $t$.
私たちは、最適でないアームをあまり頻繁に表示することなく、各アームの真の期待報酬についてより多くを学ぶために、**次にどのアームを選択するかを最適に決定する戦略**を考案します。戦略は、時刻 $t-1$ までのアーム-報酬観察の履歴を考慮し、その履歴を使用して時刻 $t$ に何を選ぶかを決定します。

<!-- ここまで読んだ! -->

There are many different types of multi-armed bandit strategies, each with their own pros and cons in terms of implementation and regret bounds.
マルチアームバンディット戦略には多くの異なるタイプがあり、それぞれ実装や後悔の範囲に関して利点と欠点があります。
For the sake of brevity, in this post we will not go into the mathematical details of the strategies, but simply share some popular strategies at a high conceptual level:
簡潔さのために、この投稿では戦略の数学的詳細には立ち入らず、高い概念レベルでいくつかの人気のある戦略を共有します。

1. Epsilon-Greedy - Choose arm with best empirical reward with probability $1-ε$ - Choose arm uniformly at random with probability $ε$
   1. イプシロン-グリーディ - 確率 $1-ε$ で最良の経験的報酬を持つアームを選択 - 確率 $ε$ でアームを均等にランダムに選択

2. Decayed Epsilon-Greedy - Perform Epsilon-Greedy strategy, but let $ε$ shrink over time to reduce exploration when we are more confident about our expected reward estimates
   2. 減衰イプシロン-グリーディ - イプシロン-グリーディ戦略を実行しますが、期待報酬の推定に自信が持てるようになるにつれて $ε$ を時間とともに縮小させて探索を減らします。

3. Upper Confidence Bound (UCB1) - Construct confidence intervals for each arm’s expected reward - Choose the arm whose upper confidence interval bound is the largest
   3. 上限信頼区間 (UCB1) - 各アームの期待報酬の信頼区間を構築 - 上限信頼区間が最も大きいアームを選択

4. Thompson Sampling - Take a Bayesian approach and set priors for each arm’s reward distribution - With each new reward estimate, update posterior distributions - Sample from each arm’s posterior, and choose arm with the largest sample
   4. トンプソンサンプリング - ベイズ的アプローチを取り、各アームの報酬分布に対して事前分布を設定 - 各新しい報酬推定に対して、事後分布を更新 - 各アームの事後からサンプリングし、最も大きなサンプルを持つアームを選択

As a side note, the applications that we have built at Udemy using our MAB system have primarily utilized the Thompson Sampling strategy.
余談ですが、**私たちがUdemyで構築したアプリケーションは、主にトンプソンサンプリング戦略を利用**しています。

<!-- ここまで読んだ! -->

## Using Multi-Armed Bandits for Recommendations マルチアームバンディットを用いた推薦

The recommendations domain contains perfect applications for multi-armed bandits. 
推薦の領域は、マルチアームバンディットの完璧な応用を含んでいます。
In a general recommendations problem, our goal is to recommend the best items to our users, where “best” is defined according to some type of user feedback. 
**一般的な推薦問題において、私たちの目標はユーザに最適なアイテムを推薦することであり、「最適」とは何らかのユーザフィードバックに基づいて定義されます。**
Then the recommendations problem can be framed as a bandit problem as follows: 
したがって、推薦問題は次のようにバンディット問題として定式化できます。

- The set of candidate items to recommend is the set of arms to play (each item is an arm) 
   推薦する候補アイテムの集合は、プレイするアームの集合です（各アイテムはアームです）。

- Displaying a particular recommended item to a user for a given amount of time is equivalent to “playing that arm” 
   特定の推薦アイテムをユーザに一定の時間表示することは、「そのアームをプレイする」ことに相当します。

- The user’s feedback when shown the recommended item, such as clicks, thumbs up or enrollments (in the case of recommended courses at Udemy), is the observed reward (i.e., the reward that is sampled from the item’s unknown reward distribution) 
   推薦アイテムが表示されたときのユーザのフィードバック（クリック、いいね、またはUdemyの推薦コースの場合の登録など）は、観測された報酬です（すなわち、アイテムの未知の報酬分布からサンプリングされた報酬です）。

- The goal is to determine the items with the highest reward payouts as quickly as possible by dynamically recommending various items to the user in a way that balances exploration with exploitation 
   目標は、探索と活用のバランスを取りながら、ユーザにさまざまなアイテムを動的に推薦することによって、できるだけ早く最高の報酬を得られるアイテムを特定することです。

There are many attractive qualities of multi-armed bandits that make them excellent for recommendations applications. 
マルチアームバンディットには、推薦アプリケーションに優れた特性が多くあります。
Three primary reasons bandits are particularly good for recommendations are: 
**バンディットが特に推薦に適している主な理由は3つ**あります。

### 理由1: Recommendations have opportunity costs. 推薦には機会コストがあります。

Every time a recommendation is made to a user, there is an associated opportunity cost; there may have been something better to show. 
ユーザに推薦が行われるたびに、関連する機会コストが発生します。より良いものを表示できたかもしれません。
Bandits shine when there is a cost associated with playing a suboptimal arm. 
バンディットは、最適でないアームをプレイすることに関連するコストがあるときに真価を発揮します。
They are designed to minimize opportunity costs. 
彼らは機会コストを最小化するように設計されています。

### 理由2: Bandits help overcome the recommendations feedback loop bias problem.  バンディットは、推薦フィードバックループバイアス問題を克服するのに役立ちます。

The recommendations feedback loop bias problem arises due to the fact that items which are already recommended have more opportunities for exposure and therefore positive feedback from users. 
推薦フィードバックループバイアス問題は、すでに推薦されたアイテムがより多くの露出の機会を持ち、したがってユーザからのポジティブなフィードバックを得ることに起因します。
Many traditional supervised machine learning algorithms that use this feedback during training are biased toward recommending these items further, continuing the cycle. 
このフィードバックをトレーニング中に使用する多くの従来の教師あり機械学習アルゴリズムは、これらのアイテムをさらに推薦することに偏っており、サイクルを続けます。
Exploration in bandits inherently breaks this cycle— less frequently explored items will need to be tested in the eyes of the bandit, so we are less prone to ending up stuck showing the same items over and over again unless they truly are optimal. 
**バンディットにおける探索は本質的にこのサイクルを断ち切ります**。あまり頻繁に探索されないアイテムは、バンディットの目にはテストされる必要があるため、**真に最適でない限り、同じアイテムを繰り返し表示することに陥る可能性が低くなります**。

### 理由3: Bandits can naturally address the item cold start problem.  バンディットは、アイテムのコールドスタート問題に自然に対処できます。

Highly related to the feedback loop bias problem is the cold start problem: new items that have very little feedback will be less likely to be recommended since they have little to no positive signals associated with them. 
フィードバックループバイアス問題に密接に関連しているのがコールドスタート問題です。フィードバックがほとんどない新しいアイテムは、関連するポジティブなシグナルがほとんどないため、推薦される可能性が低くなります。
Bandits give a fair shot to all candidate arms by naturally exploring a newer item until they are confident enough in the expected reward associated with it, at which point they will either exploit this item if they have deemed it to be successful, or stop showing it if it is deemed a failure. 
バンディットは、期待される報酬に自信を持つまで新しいアイテムを自然に探索することによって、**すべての候補アームに公平な機会を与えます**。その時点で、成功と見なされた場合はこのアイテムを活用し、失敗と見なされた場合は表示を停止します。

<!-- ここまで読んだ! -->

# How to Frame a Ranking Problem as a Bandit Problem ランキング問題をバンディット問題として定式化する方法

There are several resources available online detailing how to set up a traditional bandit problem in industry, where a single arm is presented to the user at a time and the goal is to find the best arm for a single position (e.g., banner optimization, thumbnail optimization, button color optimization and so on.). 
業界での伝統的なバンディット問題の設定方法について詳述したオンラインリソースがいくつかあります。ここでは、**ユーザーに一度に1つのアームが提示され、単一のポジションに対して最良のアームを見つけることが目標**です（例：バナー最適化、サムネイル最適化、ボタンの色の最適化など）。
However, few of these resources provide details on how to frame a recommendations ranking problem as a bandit problem. 
しかし、これらのリソースの中で、推薦ランキング問題をバンディット問題として定式化する方法について詳しく説明しているものはほとんどありません。
The key difference here is that in a ranking problem, there are multiple positions to consider, and therefore we can technically collect rewards for multiple arms at a time. 
**ここでの重要な違いは、ランキング問題では考慮すべき複数のポジションがあり、そのため技術的には複数のアームに対して同時に報酬を収集できるということ**です。
In this section, you’ll read about a case study performed at Udemy, which showcases how you can set up the ranking problem as a bandit problem. 
このセクションでは、Udemyで行われたケーススタディについて説明します。これは、ランキング問題をバンディット問題として設定する方法を示しています。

<!-- ここまで読んだ! -->

One common application of ranking at Udemy is that of recommendation unit ranking. 
**Udemyにおけるランキングの一般的な応用の1つは、推薦ユニットランキング**です。(ページ内での横カルーセルセクション単位のランキングづけ、っぽい...!:thinking:)
A recommendation unit is a horizontal carousel of courses belonging to some type of group (e.g., “Because you Viewed”, “Recommended for You”, “Popular for ____”, etc.). 
推薦ユニットとは、特定のグループに属するコースの横型カルーセルです（例：「あなたが閲覧したため」、「あなたへのおすすめ」、「人気のある____」など）。
The order that these recommendation units appear on a user’s logged-in homepage can be very important from both a user perspective and a business perspective. 
これらの**推薦ユニットがユーザーのログインしたホームページに表示される順序は、ユーザーの視点とビジネスの視点の両方から非常に重要**です。

![]()

(この定式化方法、参考になりそう...!:thinking:)
We frame the recommendation unit ranking problem as follows: 
私たちは、推薦ユニットランキング問題を次のように定式化します。
(定式化大事すぎる...!:thinking:)

1. Each recommendation unit type is a candidate arm 
   各推薦ユニットのタイプは候補アームです。

2. Playing an arm means to display a recommendation unit to a user in a given position for a fixed amount of time (15 minutes in our case) - Each user will generate an observation (reward) based on the feedback provided on the shown unit. Note that an observation only begins once a unit impression is made 
   アームをプレイすることは、特定のポジションにおいてユーザに推薦ユニットを固定時間（私たちの場合は15分）表示することを意味します - 各ユーザーは、表示されたユニットに対して提供されたフィードバックに基づいて観察（報酬）を生成します。ユニットのインプレッションが行われた時点でのみ観察が始まることに注意してください。

3. The reward is the metric we wish to use to compare various units’ performance in a given position - We use a combination of user clicks and enrollments for courses in the unit, in the fixed amount of time 
   報酬は、特定のポジションにおけるさまざまなユニットのパフォーマンスを比較するために使用したい指標です - 私たちは、固定時間内にユニット内のコースに対するユーザのクリックと登録の組み合わせを使用します。

All of this seems simple enough. 
これらすべては十分にシンプルに思えます。
However, we have yet to elaborate on how to treat feedback in the multiple positions of the ranking. 
しかし、**ランキングの複数のポジションにおけるフィードバックの扱い**についてはまだ詳しく説明していません。
In the traditional bandit setup, only a single arm is shown. 
伝統的なバンディット設定では、単一のアームのみが表示されます。
To take advantage of the fact that multiple arms can be pulled at once, we need to modify the traditional bandit setting. 
**複数のアームを同時に引くことができるという利点を活かすために、伝統的なバンディット設定を修正**する必要があります。(なるほど、利点と見做せるのか...!:thinking:)
For this, we consider two possible frameworks: the per position framework and the slate bandit framework. 
これに対して、私たちは2つの可能なフレームワークを考慮します：**per position framework（ポジションごとのフレームワーク）**と**slate bandit framework（スレートバンディットフレームワーク）**です。

<!-- ここまで読んだ! -->

## Per Position Framework

![]()

In the per position framework, we consider using a separate bandit instance for each position of the ranking. 
各位置フレームワークでは、**ランキングの各位置に対して別々のバンディットインスタンスを使用すること**を考慮します。
(ポジションの数だけバンディットインスタンスを立てて、各バンディットインスタンスは、シンプルなSingle-play MABを解くってことか...!:thinking:)
The goal of each bandit is to find the optimal arm to play in its assigned position (e.g., Bandit₂ only considers an arm “played” if a unit is shown to a user in position 2, and only considers rewards generated by clicks and enrollments in position 2). 
各バンディットの目標は、割り当てられた位置でプレイする最適なアームを見つけることです（例えば、Bandit₂は、位置2でユーザにユニットが表示された場合にのみアームを「プレイされた」と見なし、位置2でのクリックや登録によって生成された報酬のみを考慮します）。

There are both advantages and disadvantages to this approach. 
このアプローチには利点と欠点の両方があります。
On the advantages side, we are able to achieve a much more granular, specific ranking optimization because the bandits are learning the best units to display at an exact location. 
利点としては、バンディットが正確な位置に表示する最適なユニットを学習するため、はるかに詳細で特定的なランキング最適化を達成できることです。
This is more in line with what we think of when tasked with finding an optimal overall ranking. 
これは、最適な全体ランキングを見つけるという課題に取り組む際に私たちが考えるものにより一致しています。

However, there are some practical challenges that arise when using the per position framework: 
しかし、各位置フレームワークを使用する際にはいくつかの**実際的な課題(practical challenges)**が発生します：

- There are inherent interdependencies between each of the bandit instances in each position. 
   **各位置のバンディットインスタンス間には固有の相互依存関係があります**。(ポジション間の相互作用ね...!:thinking:)
   For example, Bandit₂ might wish to show the “Because you Viewed” unit at a particular time, but if Bandit₁ has already chosen that same unit, then Bandit₂ must choose something else to avoid duplication on the user side. 
   例えば、Bandit₂は特定の時間に「Because you Viewed」ユニットを表示したいかもしれませんが、Bandit₁がすでにそのユニットを選択している場合、Bandit₂はユーザー側の重複を避けるために別のものを選択しなければなりません。
   You can imagine that these interdependencies become more and more complicated as we continue down the ranking and extend this to a greater number of positions. 
   ランキングを進め、より多くの位置に拡張するにつれて、これらの相互依存関係はますます複雑になることが想像できます。

- You must maintain several different bandit instances at a time. 
   **同時にいくつかの異なるバンディットインスタンスを維持する必要があります**。
   These are streaming applications with dependencies on each other; failure of one bandit instance could cause issues for the other bandit instances. 
   これらは相互に依存するストリーミングアプリケーションです；1つのバンディットインスタンスの障害は、他のバンディットインスタンスに問題を引き起こす可能性があります。

- Reward feedback cannot be shared between bandits easily. 
   報酬フィードバックはバンディット間で簡単に共有できません。(各インスタンスが個別で頑張って学習する必要がある...:thinking:)
   Because the definition of a reward for the “Because you Viewed” unit in the eyes of Bandit₂ is clicks and enrollments that occur when that unit is shown in position 2, user clicks and enrollments that occur on the “Because you Viewed” unit in position 3 cannot be shared with Bandit₂. 
   Bandit₂の視点で「Because you Viewed」ユニットの報酬の定義は、位置2でそのユニットが表示されたときに発生するクリックと登録であるため、位置3で「Because you Viewed」ユニットに発生したユーザーのクリックと登録はBandit₂と共有できません。
   This increases the time for the bandit to learn and for the ranking to converge (we will talk more about convergence later!). 
   これにより、バンディットが学習する時間とランキングが収束する時間が増加します（収束については後で詳しく説明します！）。

Because of the multiple practical challenges that arise when using the per position framework, we instead chose to use the slate bandit framework. 
各位置フレームワークを使用する際に発生する複数の実際的な課題のため、私たちは代わりにスレートバンディットフレームワークを使用することを選びました。

<!-- ここまで読んだ! -->

## Slate Bandit Framework スレートバンディットフレームワーク

![]()

In the slate bandit framework, we forgo using a separate bandit instance per position and instead use a single bandit that tests multiple arms at one time.  
スレートバンディットフレームワークでは、各位置ごとに別々のバンディットインスタンスを使用するのをやめ、**代わりに複数のアームを同時にテストする単一のバンディットを使用**します。
In this setup, we define “playing an arm” to be displaying a unit in any of the top k positions.  
この設定では、**「アームをプレイする」とは、上位 k 位置のいずれかにユニットを表示すること**と定義します。
The selection of the value for k is important; feedback for arms shown in one of the top k positions is all treated equally, so a click or enrollment in the first position is no different than a click or enrollment in the kᵗʰ position in the eyes of the bandit.  
**k の値の選択は重要**です。上位 k 位置のいずれかに表示されたアームに対するフィードバックはすべて同等に扱われるため、最初の位置でのクリックや登録は、バンディットの目には k 位置目でのクリックや登録と何ら変わりません。
Generally speaking, the value chosen for k is a design decision, and will vary depending on the use case and page layout.  
一般的に、k の値として選ばれるものは設計上の決定であり、使用ケースやページレイアウトによって異なります。
For our particular use case, we chose k = 3 because a user’s logged-in homepage usually shows three full units in the window when the screen is maximized, so an argument can be made that feedback for units in these positions is generally comparable.  
私たちの特定の使用ケースでは、k = 3 を選択しました。なぜなら、**ユーザのログインしたホームページは通常、画面が最大化されるとウィンドウ内に3つの完全なユニットを表示するため、これらの位置にあるユニットに対するフィードバックは一般的に比較可能であると主張できます**。
(ここでのk=3って、以前他のスレートバンディットの論文でいう $L_{init}$ と同じだな...!:thinking:)

Note that under this framework, the bandit is no longer trying to find the exact best units in each position for the ranking, but is now answering the less specific question, “What are the best units to show towards the top of the page?” 
このフレームワークの下では、バンディットはもはや各位置における正確な最適ユニットを見つけようとはせず、**「ページの上部に表示するのに最適なユニットは何か？」という、より具体性の低い質問に答えています**。(最も良さげなユニットたちを上位k個選ぶ、的な問題になる...!:thinking:)

Disadvantages of this reduced granularity include the following:  
この粒度の低下による欠点は以下の通りです。

- The ranking within the top k positions is not optimized—the bandit treats the best arms as an unordered set since feedback among the top k is indistinguishable  
  - **上位 k 位置内のランキングは最適化されていません**。バンディットは、上位 k のフィードバックが区別できないため、最良のアームを無秩序なセットとして扱います。
  (ex. このユニットは2番目に出すと良い、みたいな事を見つけられない...??:thinking:)

- The ranking outside the top k positions is induced and not directly learned—the unit that ends up in position k+1 is placed there because it is what the bandit believes is the next best unit to show somewhere in the top k positions if it could, not because the bandit believes position k+1 specifically is optimal  
  - **上位 k 位置外のランキングは誘導されており、直接学習されていません**。位置 k+1 に配置されるユニットは、バンディットが上位 k 位置のどこかに表示する次に良いユニットだと考えるからであり、バンディットが特に位置 k+1 が最適だと考えているわけではありません。
  (なるほど。ここでの学習方法的には、$L_{init}$ までのサンプルのみを学習に使って、$L - L_{init}$ 番目以降の位置は学習には使われず、$L_{init}$ までの学習結果から誘導されて推論される、ということか...! カスケード報酬モデル使っても良さそう:thinking:)

However, the slate bandit framework comes with numerous advantages as well:  
しかし、スレートバンディットフレームワークには多くの利点もあります。

- Easier implementation and maintenance—just a single bandit with no complications stemming from interdependencies between multiple bandits  
  - **実装とメンテナンスが容易です**。複数のバンディット間の相互依存から生じる複雑さがない単一のバンディットだけです。

- More reward feedback per bandit instance—rewards for all of the arms shown in the top k positions are used by the bandit, so we receive more feedback per user for the bandit than in the per position framework. This enables the bandit to learn and converge much more quickly  
  - **各バンディットインスタンスあたりの報酬フィードバックが増えます**。上位 k 位置に表示されたすべてのアームに対する報酬がバンディットによって使用されるため、位置ごとのフレームワークよりもユーザーあたりのフィードバックが多く得られます。これにより、バンディットはより迅速に学習し、収束することができます。

We implemented the slate bandit framework for our unit ranking application, and observed strong revenue and engagement lifts during our A/B test against our existing non-bandit unit ranking algorithm.  
私たちは**ユニットランキングアプリケーションのためにスレートバンディットフレームワークを実装し、既存の非バンディットユニットランキングアルゴリズムに対するA/Bテスト中に強い収益とエンゲージメントの向上を観察**しました。
This suggests that the simpler slate bandit framework can still be highly effective, while simultaneously reducing complexity.  
これは、**よりシンプルなスレートバンディットフレームワークが依然として非常に効果的であり、同時に複雑さを軽減できること**を示唆しています。

<!-- ここまで読んだ! -->

# Data Science Challenges データサイエンスの課題

## Achieving / Measuring Convergence 収束の達成 / 測定

One common data science challenge when running a multi-armed bandit system is that of achieving convergence.
マルチアームバンディットシステムを運用する際の一般的なデータサイエンスの課題の一つは、収束を達成することです。
In the stationary bandit setting (where the true reward distributions per arm do not change drastically over time), we expect our bandit system to converge onto the optimal arm(s) (i.e., reduce exploration and mostly perform exploitation). 
**定常バンディット設定（各アームの真の報酬分布が時間とともに大きく変化しない場合）では、私たちはバンディットシステムが最適なアームに収束することを期待**しています（すなわち、探索を減らし、主に活用を行う）。
In general, the speed at which a multi-armed bandit algorithm can converge is dependent on several factors.  
一般的に、**マルチアームバンディットアルゴリズムが収束する速度は、いくつかの要因に依存**します。  
These are summarized in the table below.  
これらは以下の表にまとめられています。  

![]()

- Convergence Factors
<!-- - TODO: 後でメモする -->

Defining and measuring convergence can be done in many different ways.  
収束を定義し、測定する方法はいくつかあります。  
For our slate bandit ranking system, we developed a metric that looks at the consecutive rankings outputted by the bandit and tracks the average proportion of arm set changes in the top k positions for a window of time.
私たちのスレートバンディットランキングシステムでは、**バンディットが出力する連続したランキングを見て、一定の時間ウィンドウ内で上位k位置におけるアームセットの変更の平均割合を追跡するメトリック**を開発しました。  
Conceptually, this metric can be thought of as a “rate of change” metric.  
概念的には、このメトリックは「変化率」メトリックと考えることができます。  

If our bandit is successfully converging, then the rate of change should gradually decrease towards zero (with some natural fluctuations that occur due to the inherent exploration that is almost always possible with most bandit strategies).  
**もし私たちのバンディットが成功裏に収束しているなら、変化率は徐々にゼロに向かって減少するはず**です（ほとんどのバンディット戦略で常に可能な固有の探索による自然な変動があることを考慮して）。
Having graphs to measure convergence is vital for ensuring that the bandit system is working as expected.  
収束を測定するためのグラフを持つことは、バンディットシステムが期待通りに機能していることを確認するために重要です。
An example of this can be seen below:  
その例は以下に示されています：

![]()

We have generally seen that successful A/B test results with our bandit system correlate highly with successful, quick convergence.  
私たちは一般的に、**バンディットシステムによる成功したA/Bテストの結果が、成功した迅速な収束と高い相関関係があることを確認**しています。  
When choosing your application and deciding whether bandits are a good fit, keep in mind all of the factors that can affect convergence.  
アプリケーションを選択し、バンディットが適しているかどうかを決定する際には、収束に影響を与える可能性のあるすべての要因を考慮してください。

<!-- ここまで読んだ! -->

## Offline Evaluation オフライン評価

<!-- TODO: ここも面白そうだが、一定肌感はあるので後で読む --> 

Another data science challenge that arises when dealing with bandit systems is performing offline evaluation. 
バンディットシステムを扱う際に生じる別のデータサイエンスの課題は、オフライン評価を行うことです。
Offline evaluation is useful for determining which explore-exploit strategy to test online in an A/B test, and to shorten the time needed to iterate and improve. 
オフライン評価は、A/Bテストでオンラインでテストするための探索-活用戦略を決定し、反復と改善に必要な時間を短縮するのに役立ちます。

Multi-armed bandits are notoriously difficult to evaluate offline because they are inherently online, interactive algorithms. 
マルチアームバンディットは、本質的にオンラインでインタラクティブなアルゴリズムであるため、オフラインで評価するのが非常に難しいです。

The sequence of decisions selected by the bandit that we wish to evaluate is dependent on the real user reward feedback obtained. 
私たちが評価したいバンディットによって選択された決定のシーケンスは、得られた実際のユーザー報酬フィードバックに依存しています。

Using previously collected historical data is often not sufficient, as the arms shown in the past might not match up with what the bandit strategy selected. 
以前に収集された歴史的データを使用することはしばしば不十分であり、過去に示されたアームがバンディット戦略が選択したものと一致しない可能性があります。

To address this problem, one can use the replay method. 
この問題に対処するために、リプレイ法を使用することができます。

In the replay method, we perform a short random data collection phase, where candidate arms are shown to the user at random and the associated rewards are collected. 
リプレイ法では、候補アームがランダムにユーザーに表示され、関連する報酬が収集される短いランダムデータ収集フェーズを実行します。

This creates a stream of unbiased historical arm-reward pairs. 
これにより、偏りのない歴史的アーム-報酬ペアのストリームが生成されます。

Then, to evaluate a given bandit strategy, we simply sequentially step through the stream of historical arm-reward pairs and keep the pairs that match up with what the bandit wanted to select at that time. 
次に、特定のバンディット戦略を評価するために、歴史的アーム-報酬ペアのストリームを順次進み、その時点でバンディットが選択したいと思っていたペアを保持します。

The cumulative reward from these matched pairs gives us a measure of how successful a particular bandit strategy is. 
これらの一致したペアからの累積報酬は、特定のバンディット戦略がどれだけ成功しているかの指標を提供します。

Please see the figure below for a visualization of how this is performed. 
このプロセスがどのように行われるかの視覚化については、以下の図を参照してください。



# Conclusion 結論

In this part, we discussed what bandits are, how to use them in a recommendations ranking application and the types of common data science challenges that arise when successfully using bandits in industry.
この部分では、バンディットとは何か、推薦ランキングアプリケーションでの使用方法、そして業界でバンディットを成功裏に使用する際に発生する一般的なデータサイエンスの課題について議論しました。

In the next part, we will dive into our system architecture that makes this all possible in near real-time with millions of users!
次の部分では、数百万のユーザーとともに、これをほぼリアルタイムで可能にするシステムアーキテクチャについて詳しく説明します！
