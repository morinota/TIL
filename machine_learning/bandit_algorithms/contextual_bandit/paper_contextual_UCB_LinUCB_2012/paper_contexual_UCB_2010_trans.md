## link リンク

- <https://elicit.org/search?q=contextual-bandit+approach+to+personalized+news+article+recommendation&token=01H6WSCJKBN9JGVG9CRQNKSJQJ&paper=ec0072bc37f83f1a81459df43289613e04cc61e1&column=title>
- <https://arxiv.org/pdf/1003.0146.pdf>

## title タイトル

A contextual-bandit approach to personalized news article recommendation
パーソナライズされたニュース記事推薦への文脈バンディット・アプローチ

## Abstract

Personalized web services strive to adapt their services (advertisements, news articles, etc.) to individual users by making use of both content and user information.
パーソナライズされたウェブサービスは、コンテンツとユーザー情報の両方を利用することで、サービス（広告、ニュース記事など）を個々のユーザーに適応させようと努めている。
Despite a few recent advances, this problem remains challenging for at least two reasons.
最近のいくつかの進歩にもかかわらず、この問題は少なくとも2つの理由から依然として難題である。
First, web service is featured with dynamically changing pools of content, rendering traditional collaborative filtering methods inapplicable.
**第一に、ウェブサービスには動的に変化するコンテンツプールがあり、従来の協調フィルタリング手法は適用できない。**
Second, the scale of most web services of practical interest calls for solutions that are both fast in learning and computation.
第二に、実用的なほとんどのウェブサービスの規模は、**学習と計算の両方において高速なソリューションを求めている**。

In this work, we model personalized recommendation of news articles as a contextual bandit problem, a principled approach in which a learning algorithm sequentially selects articles to serve users based on contextual information about the users and articles, while simultaneously adapting its article-selection strategy based on user-click feedback to maximize total user clicks.
この問題では、**学習アルゴリズムがユーザと記事に関する文脈情報に基づいてユーザに提供する記事を順次選択し、同時にユーザのクリックフィードバックに基づいて記事選択戦略を適応させ、ユーザの総クリック数を最大化**する。

The contributions of this work are three-fold.
この仕事の貢献は3つある。
First, we propose a new, general contextual bandit algorithm that is computationally efficient and well motivated from learning theory.
まず、計算効率が良く、学習理論に基づいた新しい一般的な文脈バンディットアルゴリズムを提案する。
Second, we argue that any bandit algorithm can be reliably evaluated offline using previously recorded random traffic.
第二に、どのようなバンディット・アルゴリズムも、過去に記録されたランダム・トラフィックを用いてオフラインで確実に評価できることを主張する。
Finally, using this offline evaluation method, we successfully applied our new algorithm to a Yahoo! Front Page Today Module dataset containing over 33 million events.
最後に、このオフライン評価法を用いて、3,300万件以上のイベントを含むYahoo! Front Page Today Moduleデータセットに新しいアルゴリズムを適用することに成功した。
Results showed a 12.5% click lift compared to a standard context-free bandit algorithm, and the advantage becomes even greater when data gets more scarce.
**その結果、標準的なコンテクストフリー・バンディット・アルゴリズムと比較して12.5％のクリックリフトを示し、データがより乏しくなるとその優位性はさらに大きくなる。**

<!-- ここまで読んだ! -->

# 1. INTRODUCTION 1. はじめに

This paper addresses the challenge of identifying the most appropriate web-based content at the best time for individual users.
本稿では、個々のユーザーにとって最適なタイミングで、最適なウェブコンテンツを特定するという課題を取り上げる。
Most service vendors acquire and maintain a large amount of content in their repository, for instance, for filtering news articles [14] or for the display of advertisements [5].
多くのサービスベンダーは、例えばニュース記事のフィルタリング [14]や広告の表示 [5]のために、大量のコンテンツを取得し、リポジトリに保持している。
Moreover, the content of such a web-service repository changes dynamically, undergoing frequent insertions and deletions.
**さらに、このようなウェブサービスリポジトリのコンテンツは動的に変化し、頻繁に挿入や削除が行われる。**
In such a setting, it is crucial to quickly identify interesting content for users.
このような環境では、**ユーザーにとって興味深いコンテンツを素早く見極めること**が重要である。
For instance, a news filter must promptly identify the popularity of breaking news, while also adapting to the fading value of existing, aging news stories.
例えば、ニュースフィルターは、速報ニュースの人気を素早く識別する一方で、既存の古くなったニュースの価値の衰えにも適応しなければならない。

It is generally difficult to model popularity and temporal changes based solely on content information.
一般に、**コンテンツ情報のみに基づいて人気や時間的変化をモデル化することは難しい**。
In practice, we usually explore the unknown by collecting consumers' feedback in real time to evaluate the popularity of new content while monitoring changes in its value [3].
実際には、**消費者のフィードバックをリアルタイムで収集し、新しいコンテンツの人気度を評価しながら、その価値の変化を監視することで、未知の領域を探索するのが一般的**である[3]。
For instance, a small amount of traffic can be designated for such exploration.
例えば、少量のトラフィックをこのような探索のために指定することができる。
Based on the users' response (such as clicks) to randomly selected content on this small slice of traffic, the most popular content can be identified and exploited on the remaining traffic.
**この小さなトラフィックの一部でランダムに選択されたコンテンツに対するユーザーの反応（クリックなど）に基づいて、最も人気のあるコンテンツを特定し、残りのトラフィックで利用することができる**。
This strategy, with random exploration on an $\epsilon$ fraction of the traffic and greedy exploitation on the rest, is known as ǫ-greedy.
この戦略は、トラフィックの $\epsilon$ 分をランダムに探索し、残りを貪欲に利用するもので、$\epsilon$-greedy として知られている。
Advanced exploration approaches such as EXP3 [8] or UCB1 [7] could be applied as well.
EXP3[8]やUCB1[7]のような高度な探査アプローチも適用できるだろう。
Intuitively, we need to distribute more traffic to new content to learn its value more quickly, and fewer users to track temporal changes of existing content.
直感的に言えば、新しいコンテンツにはその価値をより早く知るために多くのトラフィックを配分し、既存のコンテンツの時間的変化を追跡するためには少ないユーザーを配分する必要がある。

<!-- ここまで読んだ! -->

Recently, personalized recommendation has become a desirable feature for websites to improve user satisfaction by tailoring content presentation to suit individual users' needs [10].
近年、パーソナライズド・レコメンデーションは、個々のユーザーのニーズに合わせてコンテンツのプレゼンテーションを調整することで、ユーザーの満足度を向上させるために、ウェブサイトにとって望ましい機能となっている[10]。
Personalization involves a process of gathering and storing user attributes, managing content assets, and, based on an analysis of current and past users' behavior, delivering the individually best content to the present user being served.
パーソナライゼーションとは、ユーザーの属性を収集・蓄積し、コンテンツ資産を管理し、現在および過去のユーザの行動を分析した上で、現在サービスを提供しているユーザに個別に最適なコンテンツを配信するプロセスを指す。

Often, both users and content are represented by sets of features.
**多くの場合、ユーザもコンテンツも特徴量のセットで表される**。
User features may include historical activities at an aggregated level as well as declared demographic information.
ユーザ特徴量には、申告された人口統計情報だけでなく、集約されたレベルでの過去の活動が含まれる場合があります。
Content features may contain descriptive information and categories.
**コンテンツの特徴には、説明的な情報やカテゴリー**が含まれることがある。
In this scenario, exploration and exploitation have to be deployed at an individual level since the views of different users on the same content can vary significantly.
このシナリオでは、同じコンテンツに対する異なるユーザーの見解が大きく異なる可能性があるため、探索と活用を個人レベルで展開する必要がある。
Since there may be a very large number of possible choices or actions available, it becomes critical to recognize commonalities between content items and to transfer that knowledge across the content pool.
可能性のある選択肢や行動が非常に多く存在する可能性があるため、**コンテンツitem間の共通性を認識**(=action embedding的な)し、**その知識をコンテンツプール全体に伝達**することが重要になる。

<!-- ここまで読んだ! -->

Traditional recommender systems, including collaborative filtering, content-based filtering and hybrid approaches, can provide meaningful recommendations at an individual level by leveraging users' interests as demonstrated by their past activity.
協調フィルタリング、コンテンツベースフィルタリング、ハイブリッドアプローチを含む従来のレコメンダーシステムは、過去のアクティビティによって示されるユーザーの興味を活用することで、個人レベルで有意義なレコメンデーションを提供することができる。
Collaborative filtering [25], by recognizing similarities across users based on their consumption history, provides a good recommendation solution to the scenarios where overlap in historical consumption across users is relatively high and the content universe is almost static.
協調フィルタリング[25]は、**消費履歴に基づいてユーザ間の類似性を認識**することで、ユーザ間の消費履歴の重複が比較的高く、コンテンツユニバースがほぼ静的であるシナリオに適した推薦ソリューションを提供する。
Contentbased filtering helps to identify new items which well match an existing user's consumption profile, but the recommended items are always similar to the items previously taken by the user [20].
コンテンツベースのフィルタリングは、**既存のユーザの消費プロファイルによく一致する新しいアイテムを識別するのに役立ちますが、推薦されたアイテムは、常にユーザが以前に摂取したアイテムに似ている**[20]。
Hybrid approaches [11] have been developed by combining two or more recommendation techniques; for example, the inability of collaborative filtering to recommend new items is commonly alleviated by combining it with content-based filtering.
ハイブリッドアプローチ[11]は、2つ以上の推薦テクニックを組み合わせることによって開発されてきた。例えば、**協調フィルタリングが新しいアイテムを推薦できないことは、一般的にコンテンツベースフィルタリングと組み合わせることによって緩和される**。

However, as noted above, in many web-based scenarios, the content universe undergoes frequent changes, with content popularity changing over time as well.
しかし、前述のように、**多くのウェブベースのシナリオでは、コンテンツユニバース(=推薦可能なitem poolの事?? 行動空間的な...!)は頻繁に変更され、コンテンツの人気も時間とともに変化する**。
Furthermore, a significant number of visitors are likely to be entirely new with no historical consumption record whatsoever; this is known as a cold-start situation [21].
さらに、かなりの数の訪問者は、過去の消費記録がまったくない、まったく新しい訪問者である可能性が高い；これはコールドスタート(ユーザ!)状況として知られている[21]。
These issues make traditional recommender-system approaches difficult to apply, as shown by prior empirical studies [12].
これらの問題は、先行する実証的研究[12]が示すように、従来のレコメンダー・システム・アプローチの適用を困難にしている。
It thus becomes indispensable to learn the goodness of match between user interests and content when one or both of them are new.
そのため、ユーザの興味とコンテンツのどちらか、あるいは両方が新しい場合、そのマッチングの良し悪しを学習することが不可欠となる。(ユーザかアイテムのどちらかがcold-start状態じゃなくなるまでログを集める必要があるよね...!って意味?)
However, acquiring such information can be expensive and may reduce user satisfaction in the short term, raising the question of optimally balancing the two competing goals: maximizing user satisfaction in the long run, and gathering information about goodness of match between user interests and content.
しかし、このような情報の取得にはコストがかかり、短期的にはユーザの満足度を低下させる可能性がある。そのため、**長期的にユーザーの満足度を最大化することと、ユーザーの興味とコンテンツの一致度に関する情報を収集することという、相反する2つの目標を最適にバランスさせる必要がある**。(つまり exploration/exploitation のバランスを取る必要がある...! => バンディットアルゴリズムの出番じゃん! :thinking:)

The above problem is indeed known as a feature-based exploration/exploitation problem.
上記の問題は、まさに**feature-based exploration/exploitation problem(特徴に基づく探索/利用問題)**として知られている。
In this paper, we formulate it as a contextual bandit problem, a principled approach in which a learning algorithm sequentially selects articles to serve users based on contextual information of the user and articles, while simultaneously adapting its article-selection strategy based on user-click feedback to maximize total user clicks in the long run.
これは、**学習アルゴリズムが、ユーザと記事の文脈情報に基づいて、ユーザに提供する記事を順次選択し、同時に、長期的にユーザの総クリック数を最大化するために、ユーザクリックフィードバックに基づいて記事選択戦略を適応させる原理的なアプローチ**である。
We define a bandit problem and then review some existing approaches in Section 2.
バンディット問題を定義し、セクション2で既存のアプローチをレビューする。
Then, we propose a new algorithm, LinUCB, in Section 3 which has a similar regret analysis to the best known algorithms for competing with the best linear predictor, with a lower computational overhead.
そして、セクション3では、最良の線形予測器と競合するための最もよく知られたアルゴリズムと同様の**regret analysis(後悔分析?)**を持ち、**より低い計算オーバーヘッドを持つ新しいアルゴリズム、LinUCBを**提案する。
We also address the problem of offline evaluation in Section 4, showing this is possible for any explore/exploit strategy when interactions are independent and identically distributed (i.i.d.), as might be a reasonable assumption for different users.
また、**セクション4でオフライン評価の問題を取り上げ**、異なるユーザーに対して妥当な仮定であるように、相互作用が独立かつ同一分布（i.i.d.）である場合、どのような探索/探索戦略でも可能であることを示す。
We then test our new algorithm and several existing algorithms using this offline evaluation strategy in Section 5.
そしてセクション5で、このオフライン評価戦略を用いて、我々の新しいアルゴリズムといくつかの既存のアルゴリズムをテストする。

<!-- ここまで読んだ! -->

# 2. FORMULATION & RELATED WORK 2. 策定と関連作業

In this section, we define the K-armed contextual bandit problem formally, and as an example, show how it can model the personalized news article recommendation problem.
このセクションでは、K-armed contextual bandit問題を正式に定義し、例として、パーソナライズされたニュース記事の推薦問題をどのようにモデル化できるかを示す。
We then discuss existing methods and their limitations.
次に、既存の方法とその限界について述べる。

## 2.1 A Multi-armed Bandit Formulation 2.1 多腕バンディットの定式化

The problem of personalized news article recommendation can be naturally modeled as a multi-armed bandit problem with context information.
パーソナライズされたニュース記事推薦の問題は、コンテキスト情報を持つ多腕バンディット問題として自然にモデル化することができる.
Following previous work [18], we call it a contextual bandit.1 Formally, a contextual-bandit algorithm A proceeds in discrete trials t = 1, 2, 3, .
以前の研究[18]に従い、我々はこれをコンテクスチュアル・バンディットと呼ぶ。
In trial $t$:
トライアルTで：

- 1. The algorithm observes the current user $u_t$ and a set $A_t$ of arms or actions together with their feature vectors $x_{t,a}$ for $a \in A_{t}$. The vector xt,a summarizes information of both the user ut and arm a, and will be referred to as the context.
- このアルゴリズムは、現在のユーザーutと、アームまたはアクションの集合Atを、その特徴ベクトルxt,aとともに、a∈Atについて観察する。 **ベクトルxt,aは、ユーザーutとアームaの両方の情報を要約しており、コンテキストと呼ばれる**。
- 2. Based on observed payoffs in previous trials, A chooses an arm at ∈ At, and **receives** payoff rt,a t whose expectation depends on both the user ut and the arm at.
- 2.以前の試行で観察されたペイオフ(=報酬?)に基づいて、アルゴリズムはアーム $a_{t} \in A_{t}$ を選択し、期待値がユーザ $u_t$ とアーム $a_t$ の両方に依存するペイオフ(報酬) $r_{t,a_t}$ を受け取る。
- 3. The algorithm then improves its arm-selection strategy with the new observation, (xt,a t , at, rt,a t ). It is important to em-phasize here that no feedback (namely, the payoff rt,a) is observed for unchosen arms a = at. The consequence of this fact is discussed in more details in the next subsection.
- 3. その後アルゴリズムは、新しい観測値 $(x_{t, a_t}, a_t, r_{t, a_t})$ でaction選択戦略を改善する。ここで重要な事は、選ばれてないarms $a \neq a_{t}$ にはfeedback(=報酬 $r_{t, a}$)が観測されない、という事。(=反実仮想的な問題設定...!)

In the process above, the total T -trial payoff of A is defined as T t=1 rt,a t .
上記のプロセスにおいて、Aの総 $T$ 試行ペイオフ(=試行 $T$ までの累積報酬) は $\sum_{t=1}^{T}r_{t,a_t}$ と定義される。
Similarly, we define the optimal expected T -trial payoff as E T t=1 r t,a _t , where a_ t is the arm with maximum expected payoff at trial t.
同様に、T-trialsの総報酬の最適な期待値を $\mathbb{E}[\sum_{t=1}^{T} r_{t, a_{t}^*}]$ として定義する。ここで $a_{t}^*$ は、試行tで最大の期待ペイオフを持つアームである。
Our goal is to design A so that the expected total payoff above is maximized.
我々の目標は、上記の期待総ペイオフが最大になるようにアルゴリズムAを設計することである。
Equivalently, we may find an algorithm so that its regret with respect to the optimal arm-selection strategy is minimized.
同様に、**最適な腕選択戦略に対するregret(後悔)が最小になるようなアルゴリズム**を見つけることもできる。
Here, the T -trial regret $R_{A}(T)$ of algorithm $A$ is defined formally by
ここで、アルゴリズムAのT試行後悔R A (T ) は、形式的に次式で定義される。(理想的なarmを選択し続けた場合の総報酬と、実際の総報酬の差分、の期待値。)

$$
R_{A}(T) := $\mathbb{E}[\sum_{t=1}^{T} r_{t, a_{t}^*}]$ - $\mathbb{E}[\sum_{t=1}^{T} r_{t, a_{t}}]$
$$

An important special case of the general contextual bandit problem is the well-known K-armed bandit in which (i) the arm set At remains unchanged and contains K arms for all t, and (ii) the user ut (or equivalently, the context) is the same for all t.
一般的なコンテクストバンディット問題の重要な特殊ケース(=実運用ではあり得ないケースってこと??:thinking:)は、よく知られたK-armed banditであり、(i)アームセットAtはすべてのtで不変でK個のアームを含み、(ii)ユーザut（または同等にコンテキスト）はすべてのtで同じである。
Since both the arm set and contexts are constant at every trial, they make no difference to a bandit algorithm, and so we will also refer to this type of bandit as a context-free bandit.
**アームセットとコンテキストの両方が各試行で一定**であるため、バンディットアルゴリズムには違いがなく、このタイプのバンディットを**context-free bandit**とも呼ぶ。(あ、そういうことね!:thinking:)

In the context of article recommendation, we may view articles in the pool as arms.
記事推薦の文脈では、**プール内の記事をarmとみなす**ことができる。
When a presented article is clicked, a payoff of 1 is incurred; otherwise, the payoff is 0.
**提示された記事がクリックされた場合、1の報酬が発生し、そうでない場合は0の報酬が発生する**。
With this definition of payoff, the expected payoff of an article is precisely its clickthrough rate (CTR), and choosing an article with maximum CTR is equivalent to maximizing the expected number of clicks from users, which in turn is the same as maximizing the total expected payoff in our bandit formulation.
このペイオフの定義では、**記事の期待報酬は正確にそのクリック率（CTR）**であり、最大のCTRを持つ記事を選択することは、ユーザーからの期待クリック数を最大化することと同じである。

Furthermore, in web services we often have access to user information which can be used to infer a user's interest and to choose news articles that are probably most interesting to her.
さらに、ウェブサービスでは、ユーザの興味を推測し、そのユーザが最も興味を持つであろうニュース記事を選択するために使用できるユーザ情報にアクセスできることが多い。
For example, it is much more likely for a male teenager to be interested in an article about iPod products rather than retirement plans.
たとえば、ティーンエイジャーの男性は、退職金プランよりもiPod製品の記事に興味を持つ可能性が高い。
Therefore, we may "summarize" users and articles by a set of informative features that describe them compactly.
したがって、**ユーザや記事をコンパクトに記述する情報量の多い特徴量によって「要約」することができる**。(i.e. あ、ユーザidや記事idなどのone-hotベクトルを、特徴量を使ってdenseなベクトルに変換するってことね!:thinking:)
By doing so, a bandit algorithm can generalize CTR information from one article/user to another, and learn to choose good articles more quickly, especially for new users and articles.
そうすることで、バンディットアルゴリズムは、**ある記事/ユーザから別の記事/ユーザへのCTR情報を一般化**し、**特に新しいユーザや記事に対して、より迅速に良い記事を選択すること**を学ぶことができる。(記事の特徴量はテキストを使えばOKだけど、新規でも入手できるユーザの特徴量なんかあるかなぁ...オンボーディング回答...!:thinking:)

<!-- ここまで読んだ! -->

## 2.2 Existing Bandit Algorithms 2.2 既存のバンディット・アルゴリズム

The fundamental challenge in bandit problems is the need for balancing exploration and exploitation.
バンディット問題における基本的な課題は、探索と活用のバランスをとる必要性である。
To minimize the regret in Eq.(1), an algorithm A exploits its past experience to select the arm that appears best.
式(1)のregretを最小化する場合、アルゴリズムAは過去の経験を利用し、最適と思われる腕を選択する。
On the other hand, this seemingly optimal arm may in fact be suboptimal, due to imprecision in A's knowledge.
**一方、この一見最適に見える腕は、Aの知識が不正確であるため、実際には最適でない可能性がある**。(うんうん、そりゃそう...!)
In order to avoid this undesired situation, A has to explore by actually choosing seemingly suboptimal arms so as to gather more information about them (c.f., step 3 in the bandit process defined in the previous subsection).
このような望ましくない状況を避けるために、**Aは、より多くの情報を収集するために、一見最適でないように見える武器を実際に選択して探索しなければならない**（前節で定義したバンディット・プロセスのステップ3を参照）。
Exploration can increase short-term regret since some suboptimal arms may be chosen.
探索は、最適でないarmが選択される可能性があるため、短期的なregretを増大させる可能性がある。(うんうん)
However, obtaining information about the arms' average payoffs (i.e., exploration) can refine A's estimate of the arms' payoffs and in turn reduce long-term regret.
しかし、**各armの平均的な報酬に関する情報を得ること（すなわち、探索）**は、**アルゴリズムAの各armの報酬の見積もりを洗練させ**、ひいては長期的なregretを減らすことができる。
Clearly, neither a purely exploring nor a purely exploiting algorithm works best in general, and a good tradeoff is needed.
明らかに、**純粋に探索するアルゴリズムも、純粋に利用するアルゴリズムも、一般的に最もうまく機能するものではなく、適切なトレードオフが必要である**。(purely exploiting algorithm って 要は決定論的なアルゴリズムだよなぁ...:thinking:)

<!-- ここまで読んだ! -->

The context-free K-armed bandit problem has been studied by statisticians for a long time [9,24,26].
**context-freeなK-armdedバンディット問題**は、統計学者によって長い間研究されてきた[9,24,26]。
One of the simplest and most straightforward algorithms is ǫ-greedy.
最も単純で簡単なアルゴリズムのひとつがepsilon-greedyである。
In each trial t, this algorithm first estimates the average payoff μt,a of each arm a.
各試行tにおいて、このアルゴリズムはまず各アームaの報酬期待値 $\hat{\mu_{t,a}}$ を推定する。
Then, with probability 1 − ǫ, it chooses the greedy arm (i.e., the arm with highest payoff estimate); with probability ǫ, it chooses a random arm.
そして、**確率1 - $\epsilon$ で、貪欲なアーム（すなわち、ペイオフの推定値が最も高いアーム）を選択し、確率 $\epsilon$ で、ランダムなアームを選択する。**
In the limit, each arm will be tried infinitely often, and so the payoff estimate μt,a converges to the true value µa with probability 1.
極限では、各 arm は無限に試行されるので、ペイオフ推定値 $\hat{\mu_{t, a}}$ は確率1で**真値 $\mu_{a}$ に収束**する。
Furthermore, by decaying ǫ appropriately (e.g., [24]), the per-step regret, R A (T )/T , converges to 0 with probability 1.
さらに、(例えば[24]のように) **$\epsilon$ を適切に減衰させる**ことで、1ステップあたりのregret、$R_{A}(T)/T$ は確率1で0に収束する。(そっか、減衰させない場合は、報酬の真の値を得たとしても一定確率で最適じゃないarmを選択するのか...!)

In contrast to the unguided exploration strategy adopted by ǫgreedy, another class of algorithms generally known as upper confidence bound algorithms [4,7,17] use a smarter way to balance exploration and exploitation.
$\epsilon$ が採用する**unguided exploration strategy(非誘導探索戦略)**とは対照的に、一般に**upper confidence bound algorithms(上部信頼境界アルゴリズム)**[4,7,17]として知られる別のクラスのアルゴリズムでは、探索と搾取のバランスをとるために、よりスマートな方法を用います。
Specifically, in trial t, these algorithms estimate both the mean payoff μt,a of each arm a as well as a corresponding confidence interval ct,a, so that |μt,a − µa| < ct,a holds with high probability.
具体的には、試行tにおいて、これらのアルゴリズムは、各アーム $a$ の報酬期待値 $\mu_{t,a}$と、それに対応する**信頼区間 $c_{t,a}$ の両方を推定**し、$|\hat{\mu_{t,a}} - \mu_{a}| < c_{t,a}$ が高確率(=90%とか??)で成立するようにする。(期待値と信頼区間、統計学っぽい...!:thinking:)
They then select the arm that achieves a highest upper confidence bound (UCB for short): at = arg maxa (μt,a + ct,a).
そして、**最も高いupper confidence bound(略してUCB)を達成する arm を選択**する: $a_{t} = \argmax_{a}(\hat{\mu_{t,a}} + c_{t,a})$。
With appropriately defined confidence intervals, it can be shown that such algorithms have a small total Ttrial regret that is only logarithmic in the total number of trials T , which turns out to be optimal [17].
適切に定義された信頼区間を用いると、このようなアルゴリズムは、総試行数 $T$ の対数だけ小さい total T trial regret を持つことが示され、これが 最適であることが判明する[17]。

(contextual banditの既存研究)

While context-free K-armed bandits are extensively studied and well understood, the more general contextual bandit problem has remained challenging.
context-free な K-armsバンディットは広く研究され、よく理解されているが、より一般的な**contextualバンディット問題は依然として難題**である。
The EXP4 algorithm [8] uses the exponential weighting technique to achieve an Õ( √ T ) regret, 2 but the computational complexity may be exponential in the number of features.
EXP4アルゴリズム[8]は、指数関数的な重み付け技法を使用し、Õ( √ T ) regret を達成する2が、**計算量は特徴量数の指数関数になる可能性**がある。
Another general contextual bandit algorithm is the epochgreedy algorithm [18] that is similar to ǫ-greedy with shrinking ǫ.
もう1つの一般的なコンテキスト・バンディット・アルゴリズムは、$\epsilon$ グリーディに似た epoch-greedy アルゴリズム[18]である.
This algorithm is computationally efficient given an oracle optimizer but has the weaker regret guarantee of Õ(T 2/3 ).
このアルゴリズムは、オラクル・オプティマイザがあれば計算効率は良いが、Õ(T 2/3 )のregret保証は弱い.(計算量は小さいがパフォーマンスが微妙...!)

Algorithms with stronger regret guarantees may be designed under various modeling assumptions about the bandit.
より強いregret保証を持つアルゴリズムは、バンディットに関する様々なモデル化の仮定の下で設計することができる。
Assuming the expected payoff of an arm is linear in its features, Auer [6] describes the LinRel algorithm that is essentially a UCB-type approach and shows that one of its variants has a regret of Õ( √ T ), a significant improvement over earlier algorithms [1].
**ある arm の期待報酬がその特徴量に対して線形であると仮定**すると、Auer [6] は本質的にUCBタイプのアプローチであるLinRelアルゴリズムについて説明し、その変形の1つが $\tilde{O}(\sqrt{T})$ の後悔を持つことを示し、以前のアルゴリズム[1]よりも大幅に改善されている.

Finally, we note that there exist another class of bandit algorithms based on Bayes rule, such as Gittins index methods [15].
最後に、Gittins指数法[15]のような、ベイズルールに基づくバンディットアルゴリズムの別のクラスが存在することに注意する。
With appropriately defined prior distributions, Bayesian approaches may have good performance.
適切に定義された事前分布があれば、ベイズ的アプローチは優れた性能を発揮する可能性がある。
These methods require extensive offline engineering to obtain good prior models, and are often computationally prohibitive without coupling with approximation techniques [2].
これらの方法は、良い事前モデルを得るために大規模なオフラインエンジニアリングを必要とし、近似技術との結合なしでは、しばしば計算量が膨大になる[2]。
(=ベイズ系のbandit algorithmは良い事前分布を用意できれば性能は良いが、事前分布を得るための準備と計算量の大きさがネック。)

# 3. ALGORITHM 3. アルゴリズム

Given asymptotic optimality and the strong regret bound of UCB methods for context-free bandit algorithms, it is tempting to devise similar algorithms for contextual bandit problems.
context-free バンディット・アルゴリズムに対するUCB法の漸近的最適性と強いregret境界(=達成できるregretの最悪値?)を考えると、contexutalバンディット問題に対しても同様のアルゴリズムを考案したくなる。(=UCB法が結構良いので、contextual banditに適用したいよね...!)
Given some parametric form of payoff function, a number of methods exist to estimate from data the confidence interval of the parameters with which we can compute a UCB of the estimated arm payoff.
**報酬関数のパラメトリックな形式(報酬のモデル式?)**が与えられた場合、推定された arm 報酬のUCBを計算することができるパラメータの信頼区間をデータから推定する方法が数多く存在する。
Such an approach, however, is expensive in general.
しかし、このようなアプローチは一般的に高価(=計算量多い?)である。

In this work, we show that a confidence interval can be computed efficiently in closed form when the payoff model is linear, and call this algorithm LinUCB.
本研究では、**報酬モデルが線形である場合に、信頼区間をclosed-formで効率的に計算できること**を示し、このアルゴリズムを**LinUCB**と呼ぶ。
For convenience of exposition, we first describe the simpler form for disjoint linear models, and then consider the general case of hybrid models in Section 3.2.We note LinUCB is a generic contextual bandit algorithms which applies to applications other than personalized news article recommendation.
説明の便宜上、まずdisjoint線形モデルのより単純な形式を説明し、次にセクション3.2でハイブリッドモデルの一般的なケースを考察する。**LinUCBは、パーソナライズされたニュース記事推薦以外のアプリケーションにも適用可能な汎用contextual banditアルゴリズムであること**に注意されたい。

## 3.1 LinUCB with Disjoint Linear Models 3.1 disjoint線形モデルによるLinUCB

Using the notation of Section 2.1, we assume the expected payoff of an arm a is linear in its d-dimensional feature xt,a with some unknown coefficient vector θ θ θ \* a ; namely, for all t,
セクション2.1の表記法を用いて、あるarm $a$ の期待報酬が、その $d$ 次元特徴量 $x_{t,a}$ に、ある未知の係数ベクトル $\mathbf{\theta}_{a}^{*}$ を持つ線形なものであると仮定する。係数ベクトル $\mathbf{\theta}_{a}^{*}$ は即ち、全ての $t$ において、

$$
\mathbb{E}[r_{t,a}|\mathbf{x}_{t,a}] = \mathbf{x}_{t,a}^{T} \mathbf{\theta}_{a}^{*}
$$

を満たす様な係数ベクトルである。

This model is called disjoint since the parameters are not shared among different arms.
**このモデルは、異なるarm間でパラメータが共有されないため、"disjoint"と呼ばれる**。(=arm $a$ 毎にユニークなパラメータを持つ。)
Let Da be a design matrix of dimension m × d at trial t, whose rows correspond to m training inputs (e.g., m contexts that are observed previously for article a), and ba ∈ R m be the corresponding response vector (e.g., the corresponding m click/no-click user feedback).
試行 $t$ における m×d の次元のデザイン行列を $D_a$ とし、その行は $m$ 個のトレーニング入力(例えば、記事 $a$ について以前に観察された $m$ 個のコンテキスト)に対応し、 $\mathbf{c}_{a} \in \mathbb{R}^{m}$ は対応する**レスポンスベクトル(例えば、対応するm個のクリック／クリックなしのユーザーフィードバック)**である。
Applying ridge regression to the training data (Da, ca) gives an estimate of the coefficients:
訓練データ $(D_a, \mathbf{c}_{a})$ にリッジ回帰を適用すると、係数の推定値が得られる:

$$
\hat{\mathbf{\theta}}_{a} = (D_{a}^T D_{a} + I_{d})^{-1} D_a^{T} \mathbf{c}_{a}
\tag{3}
$$

where I d is the d × d identity matrix.
ここで $I_{d}$ はd×dのidentity matrix(単位行列)である。
When components in $\mathbf{c}_{a}$ ar e independent conditioned on corresponding rows in Da, it can be shown [27] that, with probability at least 1 − δ,
$\mathbf{c}_{a}$ の成分が $D_a$ の対応する行を条件として独立(=contextで条件付けると、各feedbackの結果は独立になる?)であるとき、少なくとも $1-\delta$ の確率で、以下のことが示される[27],(=これが期待報酬の推定値のUCBがclosed-formで計算できる話!)

$$
|\mathbf{x}_{t,a}^{T} \hat{\mathbf{\theta}}_{a} - \mathbb{E}[r_{t,a}|\mathbf{x}_{t,a}]|
\leq
\alpha \sqrt{\mathbf{x}_{t,a}^T (D_a^T D_a + I_d)^{-1} \mathbf{x}_{t,a}}
\tag{4}
$$

for any $\delta > 0$ and $x_{t,a} \in \mathbb{R}^{d}$, where $\alpha = 1 + ln(2/\delta)/2$ is a constant.
全ての $\delta > 0$ と $x_{t,a} \in \mathbb{R}^{d}$ で上が満たされる。ここで $\alpha = 1 + ln(2/\delta)/2$ は定数である。
In other words, the inequality above gives a reasonably tight UCB for the expected payoff of arm a, from which a UCBtype arm-selection strategy can be derived: at each trial t, choose
言い換えれば、上記の不等式は、アームaの期待報酬に対する適度にタイトなUCBを与え、そこからUCBタイプのアーム選択戦略を導き出すことができる: 各試行tで、以下を選択する,

$$
a_{t} := \argmax_{a \in A_t} (
  \mathbf{x}_{t,a}^{T} \hat{\mathbf{\theta}}_{a}
  + \alpha \sqrt{\mathbf{x}_{t,a}^T A_{a}^{-1} \mathbf{x}_{t,a}}
  )
  \tag{5}
$$

where $A_{a} := D_a^T D_a + I_d$.

The confidence interval in Eq.(4) may be motivated and derived from other principles.
式(4)の信頼区間は、他の原理から動機づけられ導き出されることもある。
For instance, ridge regression can also be interpreted as a Bayesian point estimate, where the posterior distribution of the coefficient vector, denoted as p(θ θ θa), is Gaussian with mean θ θ θa and covariance A −1 a .
例えば，リッジ回帰は，ベイジアンアプローチによる点推定としても解釈でき，$p(\theta_{a})$ と表記される係数ベクトルの事後分布は，平均 $\theta_{a}$ と共分散 $A_{a}^{-1}$ を持つ多変量ガウス分布である.
Given the current model, the predictive variance of the expected payoff x ⊤ t,a θ θ θ \* a is evaluated as x ⊤ t,a A −1 a xt,a, and then x ⊤ t,a A −1 a xt,a becomes the standard deviation.
現在のモデルが与えられれば、期待報酬 $\mathbf{x}_{t,a}^{T} \hat{\mathbf{\theta}}_{a}$ の予測分散は $\mathbf{x}_{t,a}^T A_{a}^{-1} \mathbf{x}_{t,a}$ と評価され、$\sqrt{\mathbf{x}_{t,a}^T A_{a}^{-1} \mathbf{x}_{t,a}}$ は標準偏差(=予測分布の標準偏差?)となる.
Furthermore, in information theory [19], the differential entropy of p(θ θ θa) is defined as − 1 2 ln((2π) d det Aa).
さらに、情報理論[19]では、$p(\theta_{a})$ の微分エントロピーは、-1 2 ln((2π) d det Aa)と定義される。
The entropy of p(θ θ θa) when updated by the inclusion of the new point xt,a then becomes − 1 2 ln((2π) d det (Aa + xt,ax ⊤ t,a )).
新しい点xt,aを含めて更新したときのp(θ θa)のエントロピーは、-1 2 ln((2π) d det (Aa + xt,ax ⊤ t,a ))となる。
The entropy reduction in the model posterior is 1 2 ln(1 + x ⊤ t,a A −1 a xt,a).
モデル事後値のエントロピー削減は、1 2 ln(1 + x ↪Sm_22A t,a A -1 a xt,a)である。
This quantity is often used to evaluate model improvement contributed from xt,a.
この量は、xt,aから寄与されるモデルの改善を評価するためによく使われる。
Therefore, the criterion for arm selection in Eq.(5) can also be regarded as an additive trade-off between the payoff estimate and model uncertainty reduction.
したがって、**式(5)のアーム選択基準は、報酬推定値とモデルの不確実性低減の間の加算トレードオフとみなすこともできる**。

![algorithm 1]()

Algorithm 1 gives a detailed description of the entire LinUCB algorithm, whose only input parameter is α.
アルゴリズム1は、LinUCBアルゴリズム全体の詳細な説明であり、唯一の入力パラメータ(=ハイパーパラメータ)は $\alpha$ である。
Note the value of α given in Eq.(4) may be conservatively large in some applications, and so optimizing this parameter may result in higher total payoffs in practice.
式(4)で与えられるαの値は、アプリケーションによっては保守的に大きくなる可能性があるため、このパラメータを最適化することで、実際には総ペイオフが高くなる可能性があることに注意。
Like all UCB methods, LinUCB always chooses the arm with highest UCB (as in Eq.(5))
**すべてのUCB手法と同様に、LinUCBは常に最も高いUCBスコアを持つアームを選択する**(式5).

This algorithm has a few nice properties.
このアルゴリズムにはいくつかの優れた特性がある。
First, its computational complexity is linear in the number of arms and at most cubic in the number of features.
**第一に、その計算量はarm数に対して線形**であり、**特徴の数に対して最大でも三乗**である.
To decrease computation further, we may update Aa t in every step (which takes O(d2) time), but compute and cache $Q_a := A_{a}^{-1}$ (for all a) periodically instead of in realtime.
さらに計算量を減らすために、$A_{a_t}$ を毎ステップ更新し（これにはO(d2)時間がかかる）、$Q_a := A_{a}^{-1}$ を（すべてのaについて）リアルタイムではなく定期的に計算し、キャッシュすることもできる。

<!-- ここ大事そう! -->
Second, the algorithm works well for a dynamic arm set, and remains efficient as long as the size of At is not too large.
**第二に、このアルゴリズムは動的なアームセットに対してうまく機能し、Atのサイズが大きすぎない限り効率的であり続ける.**
This case is true in many applications.
このケースは多くの用途で当てはまる.
In news article recommendation, for instance, editors add/remove articles to/from a pool and the pool size remains essentially constant.
例えば、**ニュース記事の推薦では、編集者はプールに記事を追加/削除し、プールのサイズは基本的に一定**である。(=動的なarm setだけど、サイズは一定! コンテンツプールが変化してもモデルパラメータはアイテム間で独立だからいい感じに保持できるってこと??:thinking:)

Third, although it is not the focus of the present paper, we can adapt the analysis from [6] to show the following: if the arm set At is fixed and contains K arms, then the confidence interval (i.e., the right-hand side of Eq.(4)) decreases fast enough with more and more data, and then prove the strong regret bound of Õ( √ KdT ), matching the state-of-the-art result [6] for bandits satisfying Eq.(2).
第三に、本論文の焦点ではないが、我々は[6]の分析を適応して、次のことを示すことができる: **arm集合 $A_t$ が固定され**、K個のアームを含む場合、信頼区間(すなわち、式(4)の右辺)は、より多くのデータとともに十分に速く減少し、そして、式(2)を満たすバンディットのためのstate-of-the-artの結果[6]と一致する、Õ( √ KdT )の強い後悔の境界を証明する。
These theoretical results indicate fundamental soundness and efficiency of the algorithm.
これらの理論結果は、アルゴリズムの基本的な健全性と効率性を示している。

<!-- ここまで読んだ! -->

Finally, we note that, under the assumption that input features xt,a were drawn i.i.d.from a normal distribution (in addition to the modeling assumption in Eq.( 2)), Pavlidis et al.[22] came up with a similar algorithm that uses a least-squares solution θ θ θa instead of our ridge-regression solution ( θ θ θa in Eq.( 3)) to compute the UCB.
最後に、（式(2)のモデリング仮定に加えて）入力特徴量 $x_{t,a}$ が正規分布からi.i.d.描画されたという仮定の下で、Pavlidisら[22]は、UCBを計算するために、我々のリッジ回帰解（式(3)の $\hat{\theta}_{a}$）の代わりに最小二乗解 $\tilde{\theta}_{a}$ を使用する同様のアルゴリズムを考え出したことに注目する。
However, our approach (and theoretical analysis) is more general and remains valid even when input features are nonstationary.
しかし、我々のアプローチ（および理論的分析）はより一般的であり、入力特徴が非定常(=特徴量がi.i.d.正規分布からサンプリングされた仮定が満たせないケース??)であっても有効である。
More importantly, we will discuss in the next section how to extend the basic Algorithm 1 to a much more interesting case not covered by Pavlidis et al.
さらに重要なのは、基本的なアルゴリズム1を、Pavlidisらによってカバーされていない、より興味深いケースに拡張する方法について、次のセクションで議論することである。

<!-- ここまで読んだ! -->

## 3.2 LinUCB with Hybrid Linear Models ハイブリッド線形モデルによるLinUCB

Algorithm 1 (or the similar algorithm in [22]) computes the inverse of the matrix, D ⊤ a Da + I d (or D ⊤ a Da), where Da is again the design matrix with rows corresponding to features in the training data.
アルゴリズム1は、行列($D_{a}^{T} D_{a} + I_{d}$ or $D_{a}^{T} D_{a}$)の逆行列を計算する。(デザイン行列ってやつ??:thinking:)
These matrices of all arms have fixed dimension d × d, and can be updated efficiently and incrementally.
すべてのアームのこれらの行列は、固定された次元d×dを持ち、効率的かつインクリメンタルに更新することができる。
Moreover, their inverses can be computed easily as the parameters in Algorithm 1 are disjoint: the solution θ θ θa in Eq.(3) is not affected by training data of other arms, and so can be computed separately.
さらに、アルゴリズム1のパラメータは不連続であるため、それらの逆数を簡単に計算することができる： **式(3)の解 $\theta_{a}$ は、他のアームのトレーニングデータの影響を受けないため、別々に計算することができる**.
We now consider the more interesting case with hybrid models.
次に、ハイブリッド・モデルを使った、より興味深いケースを考えてみよう。

In many applications including ours, it is helpful to use features that are shared by all arms, in addition to the arm-specific ones.
**私たちを含む多くのアプリケーションでは、アーム固有の特徴量(parameter)に加えて、すべてのアームで共有される特徴量(parameter)を使用することが有用**である。
For example, in news article recommendation, a user may prefer only articles about politics for which this provides a mechanism.
例えば、ニュース記事の推薦において、ユーザーは政治に関する記事だけを好むかもしれない。
Hence, it is helpful to have features that have both shared and non-shared components.
したがって、共有componentと非共有componentの両方を持つ特徴量があると便利だ。
Formally, we adopt the following hybrid model by adding another linear term to the right-hand side of Eq(2):.
形式的には、式(2)の右辺に別の線形項を追加して、以下のハイブリッドモデルを採用する。

$$
\mathbb{E}[r_{t,a}|x_{t,a}]
= \mathbf{z}_{t,a}^T \mathbf{\beta}^*
+ \mathbf{x}_{t,a}^T \mathbf{\theta}_{a}^*
\tag{6}
$$

where zt,a ∈ R k is the feature of the current user/article combination, and β is an unknown coefficient vector common to all arms.
ここで、**$z_{t,a} \in \mathbb{R}^k$ は現在 $t$ のユーザと記事の組み合わせの特徴であり、$\beta^{*}$はすべてのアームに共通する未知の係数ベクトル**である。
This model is hybrid in the sense that some of the coefficients β are shared by all arms, while others θ a are not.
**このモデルは、ある係数 $\beta^{*}$ はすべてのアームに共有され、他の係数 $\theta_{a}^{*}$ は共有されないという意味でハイブリッド**である。

![algorithm 2]()

For hybrid models, we can no longer use Algorithm 1 as the confidence intervals of various arms are not independent due to the shared features.
ハイブリッドモデルの場合、共有された特徴量のため、様々なアームの信頼区間は独立ではないので、アルゴリズム1はもはや使えない。
Fortunately, there is an efficient way to compute an UCB along the same line of reasoning as in the previous section.
幸いなことに、前節と同じ理屈でUCBを計算する効率的な方法がある。
The derivation relies heavily on block matrix inversion techniques.
この導出は、ブロック行列(?)の逆行列テクニックに大きく依存している。
Due to space limitation, we only give the pseudocode in Algorithm 2 (where lines 5 and 12 compute the ridge-regression solution of the coefficients, and line 13 computes the confidence interval), and leave detailed derivations to a full paper.
紙面の都合上、アルゴリズム2の擬似コード(5行目と12行目が係数のリッジ回帰解を計算し、13行目が信頼区間を計算する)のみを示し、詳細な導出は論文に譲る。
Here, we only point out the important fact that the algorithm is computationally efficient since the building blocks in the algorithm (A0, b0, Aa, Ba, and ba) all have fixed dimensions and can be updated incrementally.
ここでは、**アルゴリズムの構成要素 $(A_0, b_0, A_a, B_a, b_a)$ はすべて固定された次元を持ち、インクリメンタルに更新できるため、アルゴリズムが計算効率に優れている**という重要な事実のみを指摘する。(重要だ...!)
Furthermore, quantities associated with arms not existing in At no longer get involved in the computation.
さらに、$A_t$に存在しない arm に関連する量は、もはや計算に関与しない。
Finally, we can also compute and cache the inverses (A −1 0 and A −1 a ) periodically instead of at the end of each trial to reduce the per-trial computational complexity to O(d 2 + k 2 ).
最後に、各トライアル終了時ではなく、定期的に逆数 ($A_{0}^{-1}, A_{a}^{-1}$) を計算しキャッシュすることで、トライアルごとの計算量を $O(d^2+ k^2)$ に減らすこともできる。

# 4. EVALUATION METHODOLOGY 4. 評価方法

Compared to machine learning in the more standard supervised setting, evaluation of methods in a contextual bandit setting is frustratingly difficult.
より標準的な教師あり設定の機械学習と比べると、contextual bandit設定における手法の評価は苛立たしいほど難しい。(OPEの話してる??)
Our goal here is to measure the performance of a bandit algorithm π, that is, a rule for selecting an arm at each time step based on the preceding interactions (such as the algorithms described above).
ここでの目的は、バンディット・アルゴリズム $\pi$, つまり、先行する相互作用に基づいて各時間ステップでアームを選択するルール(上述のアルゴリズムなど)の性能を測定することである。
Because of the interactive nature of the problem, it would seem that the only way to do this is to actually run the algorithm on "live" data.
この問題のインタラクティブな性質から、**$\pi$ の性能を測定する唯一の方法は、"ライブ "データで実際にアルゴリズムを実行すること**だと思われる。(オンラインテスト)
However, in practice, this approach is likely to be infeasible due to the serious logistical challenges that it presents.
しかし実際には、この方法はロジスティクス上の重大な問題(??)があるため、実現不可能である可能性が高い。
Rather, we may only have offline data available that was collected at a previous time using an entirely different logging policy.
むしろ、**まったく別の logging policy を使って以前に収集されたオフライン・データしか利用できない**かもしれない。
Because payoffs are only observed for the arms chosen by the logging policy, which are likely to often differ from those chosen by the algorithm π being evaluated, it is not at all clear how to evaluate π based only on such logged data.
報酬が観測されるのは logging policy によって選択された arm のみであり、評価対象のアルゴリズム $\pi$ によって選択されたアームとは異なることが多いため、このようなロギングデータのみに基づいてπを評価する方法はまったく明確ではない。
This evaluation problem may be viewed as a special case of the so-called "off-policy evaluation problem" in reinforcement learning (see, c.f., [23]).
この評価問題は、**強化学習におけるいわゆる"Off-policy evaluation problem"**の特殊なケースとみなすことができる（例えば、[23]を参照）。

One solution is to build a simulator to model the bandit process from the logged data, and then evaluate π with the simulator.
一つの解決策は、ログデータからバンディットプロセスをモデル化するシミュレータを構築し、そのシミュレータで $\pi$ を評価することである。
However, the modeling step will introduce bias in the simulator and so make it hard to justify the reliability of this simulator-based evalu-ation approach.
しかし、モデリング・ステップはシミュレータにバイアスをもたらすため、このシミュレータ・ベースの評価手法の信頼性を正当化するのは難しい。
In contrast, we propose an approach that is simple to implement, grounded on logged data, and unbiased.
対照的に、我々は、実装が簡単で、記録されたデータに基づき、偏りのないアプローチを提案する。

In this section, we describe a provably reliable technique for carrying out such an evaluation, assuming that the individual events are i.i.d., and that the logging policy that was used to gather the logged data chose each arm at each time step uniformly at random.
このセクションでは、**個々のイベントがi.i.d.であり**、ログデータを収集するために使用された**logging policy が各タイムステップで一様にランダムに各アームを選択したと仮定して**(結構エグい仮定じゃない??)、このような評価を実施するための証明可能な信頼性の高い技術を説明します。
Although we omit the details, this latter assumption can be weakened considerably so that any randomized logging policy is allowed and our solution can be modified accordingly using rejection sampling, but at the cost of decreased efficiency in using data.
詳細は省略するが、**この後者の仮定はかなり弱めることができるため**、どのようなランダム化されたlogging policyも許容され、棄却サンプリングを用いて我々の解をそれに応じて修正することができるが、その代償としてデータの利用効率は低下する。

More precisely, we suppose that there is some unknown distribution D from which tuples are drawn i.i.d. of the form (x1, ..., xK, r1, ..., rK), each consisting of observed feature vectors and hidden payoffs for all arms.
より正確には、$(x_1, \cdots,  x_{K}, r_1, \cdots, r_K)$ という形のタプルがi.i.d.でサンプリングされる未知の分布 $D$ があると仮定する。各タプルは、観測された特徴量ベクトルと、すべてのアームに対する隠れ報酬から構成される。
We also posit access to a large sequence of logged events resulting from the interaction of the logging policy with the world.
我々はまた、ロギングポリシーと世界との相互作用の結果として生じる、ロギングされたイベントの大規模なシーケンスへのアクセスを仮定する。
Each such event consists of the context vectors x1, ..., xK , a selected arm a and the resulting observed payoff ra.
各イベントは、コンテキスト・ベクトル $x1, \cdots, xK$、選択されたアーム$a$、およびその結果観測された報酬 $r_a$ で構成される.
Crucially, only the payoff ra is observed for the single arm a that was chosen uniformly at random.
重要なのは、**一様に無作為に選ばれた単一のアーム $a$ について、報酬 $r_a$ のみが観察されることである**.
For simplicity of presentation, we take this sequence of logged events to be an infinitely long stream; however, we also give explicit bounds on the actual finite number of events required by our evaluation method.
表示を簡単にするため、この一連のログイベントは無限に長いストリームであるとする。しかし、我々の評価方法が必要とする実際の有限イベント数についても、明示的な境界を与える。

Our goal is to use this data to evaluate a bandit algorithm π.
我々の目標は、このデータを使ってバンディット・アルゴリズムπを評価することである。
Formally, π is a (possibly randomized) mapping for selecting the arm at at time t based on the history ht−1 of t−1 preceding events, together with the current context vectors xt1, ..., xtK.
形式的には、πは、現在のコンテキストベクトル $x_{t1},\cdots, x_{tK}$ とともに、 $t-1$ 個前のイベントの履歴 $h_{t-1}$ に基づいて、時刻tにおけるアームを選択するための（おそらくランダム化された）mapping (key=arm, value=報酬推定値のUCB?)である。

![algorithm3]()

Our proposed policy evaluator is shown in Algorithm 3.
我々の提案するポリシー評価器をアルゴリズム3に示す。
The method takes as input a policy π and a desired number of "good" events T on which to base the evaluation.
この方法は、ポリシーπと、評価の基礎となる「良い」イベントの望ましい数 $T$ を入力とする.
We then step through the stream of logged events one by one.
次に、ログに記録されたイベントのストリームをひとつずつ見ていく。
If, given the current history ht−1, it happens that the policy π chooses the same arm a as the one that was selected by the logging policy, then the event is retained, that is, added to the history, and the total payoff Rt updated.
もし、現在の履歴 $h_{t-1}$ が与えられたとき、政策πが logging policy によって選択されたものと同じ腕 $a$ を選択することが起これば、そのイベントは保持され、つまり履歴に追加され、総ペイオフ $R_t$ は更新される.
Otherwise, if the policy π selects a different arm from the one that was taken by the logging policy, then the event is entirely ignored, and the algorithm proceeds to the next event without any other change in its state.
そうでない場合、**ポリシーπが、ロギングポリシーによって取られたものとは異なるアームを選択した場合、そのイベントは完全に無視され**、アルゴリズムは、その状態に他の変更を加えることなく、次のイベントに進みます。
(logging policyのarmの選択傾向に影響を受けた評価結果になるはずだが、今回はlogging policyが一様ランダムにarmを選択する、という仮定なので...!!:thinking:)

Note that, because the logging policy chooses each arm uniformly at random, each event is retained by this algorithm with probability exactly 1/K, independent of everything else.
ロギング・ポリシーは各アームを一様にランダムに選択するため、各イベントはこのアルゴリズムによって、他のすべてから独立して、ちょうど1/Kの確率で保持されることに注意してください。
This means that the events which are retained have the same distribution as if they were selected by D.
つまり、保持されるイベントは、$D$ によって選択された場合と同じ分布を持つ。(??)
As a result, we can prove that two processes are equivalent: the first is evaluating the policy against T real-world events from D, and the second is evaluating the policy using the policy evaluator on a stream of logged events.
その結果、2つのプロセスが等価であることを証明することができる。**1つ目は、DからのT個の実世界イベントに対してポリシーを評価すること**(=オンライン評価??)であり、2つ目は、ログに記録されたイベントのストリームに対してポリシー評価器を使用してポリシーを評価すること(=オフライン評価??)である。

THEOREM 1.
理論1.
For all distributions D of contexts, all policies π, all T , and all sequences of events hT,
コンテキストのすべての分布 $D$、すべてのポリシーπ、すべてのT、およびすべてのイベントのシーケンスhT で 以下が成立する:

$$
Pr_{\text{Policy_Evaluator}(\pi, S)}(h_{T}) = Pr_{\pi, D}(h_{T})
$$

where S is a stream of events drawn i.i.d. from a uniform random logging policy and D.
ここで、$S$ は、一様ランダムロギングポリシーとDによって集められた.i.i.d.のイベントのストリーム(=一様ランダムにarmを選択するlogging policyで集められたログデータ?)である。

Furthermore, the expected number of events obtained from the stream to gather a history hT of length T is KT .
さらに、長さTの履歴 $h_T$ を収集するためにストリームから得られるイベントの期待数は $KT$ である。

This theorem says that every history hT has the identical probability in the real world as in the policy evaluator.
この定理は、すべての履歴hT (=の観測確率??)は、現実世界において、policy evaluator におけるのと同じ確率を持つことを意味している.
Many statistics of these histories, such as the average payoff RT /T returned by Algorithm 3, are therefore unbiased estimates of the value of the algorithm π.
アルゴリズム3が返す平均ペイオフ $R_{T}/T$ のような、これらの履歴の多くの統計は、したがって、アルゴリズムπの値の不偏推定値である。
Further, the theorem states that KT logged events are required, in expectation, to retain a sample of size T .
さらに定理は、KT個の記録されたイベントは、期待値として、サイズTのサンプルを保持するために必要であることを示す。

PROOF.
証明する。
The proof is by induction on $t = 1, \cdots, T$ starting with a base case of the empty history which has probability 1 when t = 0 under both methods of evaluation.
証明は $t = 1, \cdots, T$ の帰納法で、どちらの評価法でもt = 0のときに確率1となる空の履歴の基本ケースから始める。
In the inductive case, assume that we have for all t − 1:
帰納的な場合、すべての $t - 1$ について次のように仮定する:

$$
Pr_{\text{Policy_Evaluator(\pi, S)}}(h_{t-1}) = Pr_{\pi, D}(h_{t-1})
$$

and want to prove the same statement for any history $h_t$.
そして、どのような歴史 $h_t$ でも同じことを証明したい。
Since the data is i.i.d. and any randomization in the policy is independent of randomization in the world, we need only prove that conditioned on the history ht−1 the distribution over the t-th event is the same for each process.
データはi.i.d.であり、policy におけるいかなるランダム化も、世界におけるランダム化とは無関係なので、我々は、履歴 $h_{t-1}$ を条件として、$t$ 番目の事象に対する分布が各プロセスで同じ (=全てのtで独立! マルコフchain的ではない! :thinking:) であることを証明するだけでよい。
In other words, we must show:
つまり、私たちは以下を示さなければならない:

$$
Pr_{\text{Policy_Evaluator(\pi, S)}}
((x_{t,1}, \cdots, x_{t,K}, a, r_{t,a})|h_{t-1})
=
Pr_{D}(x_{t,1}, \cdots, x_{t,K}, a, r_{t,a})
Pr_{\pi (h_{t-1})} (a|x_{t,1}, \cdots, x_{t,K})
$$

Since the arm a is chosen uniformly at random in the logging policy, the probability that the policy evaluator exits the inner loop is identical for any policy, any history, any features, and any arm, implying this happens for the last event with the probability of the last event, PrD(xt,1, ..., xt,K, rt,a).
アーム $a$ はロギングポリシーにおいて一様にランダムに選択されるため、policy evaluator が内部ループを抜ける確率は、どのtarget policy $\pi$、どの履歴 $t$、どの特徴量 $x_{t,a}$、どのアーム $a$ においても同一であり、これは最後のイベントの確率 $Pr_{D}(x_{t,1}, \cdots, x_{t,K}, a, r_{t,a})$ で起こることを意味する。
Similarly, since the policy π's distribution over arms is independent conditioned on the history ht−1 and features (xt,1, ..., xt,K ), the probability of arm a is just Pr π(h t−1 ) (a|xt,1, ..., xt,K ).
同様に、政策 $\pi$ によるarm選択の確率分布は、履歴 $h_{t-1}$ と特徴量(=各armの特徴量) $(x_{t,1}, \cdots, x_{t,K})$ にそれぞれ独立して依存するので、arm $a$ の確率は、$Pr_{\pi (h_{t-1})} (a|x_{t,1}, \cdots, x_{t,K})$ だけである。
Finally, since each event from the stream is retained with probability exactly 1/K, the expected number required to retain T events is exactly KT .
最後に、ストリームからの各イベントはちょうど1/Kの確率で保持される(=$h_t$ と target policyの $a_t$ が一致する確率...??)ので、T個のイベントを保持するのに必要な期待数はちょうどKT個である。

# 5. EXPERIMENTS 5. 実験

In this section, we verify the capacity of the proposed LinUCB algorithm on a real-world application using the offline evaluation method of Section 4.
本節では、セクション4のオフライン評価法(=target policyが一様ランダムを仮定した naive OPE??)を用いて、提案するLinUCBアルゴリズムの能力を実世界のアプリケーションで検証する。
We start with an introduction of the problem setting in Yahoo! Today-Module, and then describe the user/item attributes we used in experiments.
**Yahoo!Today-Module**における問題設定の紹介から始まり、実験に使用したユーザー/アイテム属性について説明する。
Finally, we define performance metrics and report experimental results with comparison to a few standard (contextual) bandit algorithms.
最後に、性能指標を定義し、いくつかの標準的な(contexutal)バンディットアルゴリズムと比較した実験結果を報告する。

## 5.1 Yahoo! Today Module # 5.1 Yahoo

![fig1]()

The Today Module is the most prominent panel on the Yahoo! Front Page, which is also one of the most visited pages on the Internet; see a snapshot in Figure 1 .
Todayモジュールは、ヤフーのフロントページで最も目立つパネルであり、インターネット上で最も訪問者の多いページの一つでもある。
The default "Featured" tab in the Today Module highlights one of four high-quality articles, mainly news, while the four articles are selected from an hourly-refreshed article pool curated by human editors.
Todayモジュールのデフォルトの "Featured "タブは、**ニュースを中心に4つの高品質な記事の中から1つをハイライト**し、**4つの記事は人間の編集者によってキュレートされた1時間ごとに更新される記事プール**から選ばれる。(推薦候補は人間の手でcurateされる)
As illustrated in Figure 1 , there are four articles at footer positions, indexed by F1-F4.
図1に示すように、フッターの位置には4つの記事があり、F1-F4で索引付けされている。
Each article is represented by a small picture and a title.
各記事は小さな写真とタイトルで表されている。
One of the four articles is highlighted at the story position, which is featured by a large picture, a title and a short summary along with related links.
**4つの記事のうち1つが、ストーリ位置でハイライトされ**、大きな写真、タイトル、短い要約、関連リンクで紹介される。
By default, the article at F1 is highlighted at the story position.
デフォルトでは、F1の記事はストーリーの位置でハイライトされる。
A user can click on the highlighted article at the story position to read more details if she is interested in the article.
ユーザーは、記事に興味があれば、ストーリーの位置でハイライトされた記事をクリックして詳細を読むことができる。
The event is recorded as a story click.
イベントはストーリークリックとして記録される。
To draw visitors' attention, we would like to rank available articles according to individual interests, and highlight the most attractive article for each visitor at the story position.
訪問者の注意を引くために、個々の興味に応じて利用可能な記事をランク付けし、**各訪問者にとって最も魅力的な記事をストーリーの位置に強調したい**。

## 5.2 Experiment Setup 5.2 実験セットアップ

This subsection gives a detailed description of our experimental setup, including data collection, feature construction, performance evaluation, and competing algorithms.
このサブセクションでは、データ収集、特徴構築、性能評価、競合アルゴリズムなど、実験セットアップの詳細を説明する。

### 5.2.1 Data Collection 5.2.1 データ収集

We collected events from a random bucket in May 2009.
2009年5月にランダムなバケツからイベントを収集した。
Users were randomly selected to the bucket with a certain probability per visiting view.3 In this bucket, articles were randomly selected from the article pool to serve users.
このバケツでは、**記事が記事プールからランダムに選択され、ユーザーに提供される**。
To avoid exposure bias at footer positions, we only focused on users' interactions with F1 articles at the story position.
フッター位置での露出バイアスを避けるため、**ストーリー位置でのF1記事に対するユーザのインタラクションのみに注目**した。(i.e. 一定期間、ランダムにF1枠に一様ランダムに記事を出すようにした?? 4つの記事の中から??)
Each user interaction event consists of three components: (i) the random article chosen to serve the user, (ii) user/article information, and (iii) whether the user clicks on the article at the story position.
各ユーザインタラクションイベント(=1つのtuple!)は3つの要素から構成される: (i)ユーザにサービスを提供するために選ばれたランダムな記事、(ii)ユーザ/記事情報(=context)、(iii)ストーリーの位置でユーザが記事をクリックしたかどうか。
Section 4 shows these random events can be used to reliably evaluate a bandit algorithm's expected payoff.
セクション4では、バンディットアルゴリズムの期待報酬を確実に評価するために、**これらのランダムイベントを使用できる**ことを示す。(section 4では、一様ランダムなuser interactionイベントを仮定していた!)

There were about 4.7 million events in the random bucket on May 01.
5月1日のランダムバケットには約470万件のイベントがあった。
We used this day's events (called "tuning data") for model validation to decide the optimal parameter for each competing bandit algorithm.
この日の出来事(tuning dataと呼ばれる)をモデル検証に使用し、競合する各バンディット・アルゴリズムの最適なパラメータを決定した。(i.e. 5月1日のデータをモデルパラメータの学習に使用した!)
Then we ran these algorithms with tuned parameters on a one-week event set (called "evaluation data") in the random bucket from May 03-09, which contained about 36 million events.
次に、パラメータを調整したこれらのアルゴリズムを、5月03日～09日のランダムバケットに含まれる1週間のイベントセット(evaluation dataと呼ばれる)に対して実行した。

<!-- ここまで読んだ! -->

### 5.2.2 Feature Construction 5.2.2 フィーチャー構築

We now describe the user/article features constructed for our experiments.
次に、実験のために構築されたユーザ/記事の特徴について説明する。
Two sets of features for the disjoint and hybrid models, respectively, were used to test the two forms of LinUCB in Section 3 and to verify our conjecture that hybrid models can improve learning speed.
セクション3でLinUCBの2つの形式をテストし、ハイブリッドモデルが学習速度を向上させるという我々の推測を検証するために、disjointモデルとハイブリッドモデルにそれぞれ2つの特徴セットを使用した。

We start with raw user features that were selected by "support".
まずは、"サポート"によって選ばれた生のユーザの特徴から。(supportってなんだっけ? 特徴量選択の話? アソシエーションルールにそんな評価指標あった気もする...)
The support of a feature is the fraction of users having that feature.
ある特徴量の"support"は、その特徴を持つユーザの割合である。(欠損値の割合??)
To reduce noise in the data, we only selected features with high support.
データのノイズを減らすため、**支持率の高い特徴のみを選択**した。
Specifically, we used a feature when its support is at least 0.1.
**具体的には、支持率が少なくとも0.1以上である場合に、その特徴量を使用**した。(i.e. 欠損値が全ユーザの90%以上を占める場合、その特徴量は捨てるって意味か...! :thinking:)
Then, each user was originally represented by a raw feature vector of over 1000 categorical components, which include: (i) demographic information: gender (2 classes) and age discretized into 10 segments; (ii) geographic features: about 200 metropolitan locations worldwide and U.S.states; and (iii) behavioral categories: about 1000 binary categories that summarize the user's consumption history within Yahoo! properties.
次に、各ユーザは、元々、1000以上のカテゴリコンポーネントからなる生の特徴ベクトルで表現されていた:(i)人口統計学的情報：**性別（2クラス）と10セグメントに離散化された年齢**、(ii)地理的特徴：世界中の約200の大都市所在地と米国の州、(iii)行動カテゴリ：**ヤフーのプロパティ内でのユーザの消費履歴を要約する約1000のバイナリカテゴリ**。(=たぶんembeddingというよりは、tf-idfみたいなsparseベクトル??, token空間)
Other than these features, no other information was used to identify a user.
これらの特徴量以外には、ユーザを特定するための情報は使われていない。

Similarly, each article was represented by a raw feature vector of about 100 categorical features constructed in the same way.
同様に、各記事は同じ方法で構築された**約100のカテゴリー特徴量**からなる生の特徴ベクトルで表された。
These features include: (i) URL categories: tens of classes inferred from the URL of the article resource; and (ii) editor categories: tens of topics tagged by human editors to summarize the article content.
これらの特徴には以下が含まれる：(i) URLカテゴリ：記事リソースのURLから推測される数十のクラス、(ii) エディタカテゴリ: 記事コンテンツを要約するために人間の編集者によってタグ付けされた数十のトピック.(線形な報酬モデルなので全て、binary変数にしてると思う:thinking:)

We followed a previous procedure [12] to encode categorical user/article features as binary vectors and then normalize each feature vector to unit length.
我々は、**カテゴリー化されたユーザ/記事の特徴をバイナリベクトルとして符号化**し、**各特徴ベクトルを単位長に正規化する**既存の手順[12]に従った。
We also augmented each feature vector with a constant feature of value 1.
また、各特徴ベクトルを値1の定数特徴量で補強した。(=constant項=bias項!)
Now each article and user was represented by a feature vector of 83 and 1193 entries, respectively.
ここで、各記事とユーザーは、それぞれ83と1193エントリーの特徴ベクトルで表現された。

To further reduce dimensionality and capture nonlinearity in these raw features, we carried out conjoint analysis based on random exploration data collected in September 2008.
**さらに次元を減らし、これらの生特徴の非線形性を捉えるために**、2008年9月に収集されたランダム探索データ(=tuning data?)に基づいてconjoint分析(共起分析的な??)を行った。
Following a previous approach to dimensionality reduction [13], we projected user features onto article categories and then clustered users with similar preferences into groups.
次元削減のための以前のアプローチ[13]に従って、ユーザーの特徴を記事のカテゴリーに投影し、類似した嗜好を持つユーザをグループにクラスタリングした。
More specifically:
もっと具体的に言えば

- We first used logistic regression (LR) to fit a bilinear model for click probability given raw user/article features so that $\phi_{u}^{T} W \phi_{a}$ approximated the probability that the user u clicks on article a, where φ φ φu and φ φ φa were the corresponding feature vectors, and W was a weight matrix optimized by LR.
- 最初にロジスティック回帰(LR)を使って、$\phi_{u}^{T} W \phi_{a}$ がユーザ $u$ が記事 $a$ をクリックする確率を近似するように、未加工のユーザ/記事特徴を与えられたクリック確率の bi-linear モデルを当てはめた。

- Raw user features were then projected onto an induced space by computing $\psi_{u} := \phi_{u}^T W$. Here, the i th component in ψ ψ ψu for user u may be interpreted as the degree to which the user likes the i th category of articles. K-means was applied to group users in the induced ψ ψ ψu space into 5 clusters.
- そして、生のユーザー特徴は、$\psi_{u} := \phi_{u}^T W$ を計算することによって誘導空間に投影された。ここで、ユーザuに対する $\psi_{u}$ のi番目の成分は、ユーザが記事のi番目のカテゴリを好む度合いとして解釈される。K-meansは、誘導された $\psi_{u}$ 空間内のユーザを**5つのクラスターにグループ化**するために適用された。
(two-towerのuser-embeddingを使うイメージでもいいのかな??:thinking:)

- The final user feature was a six-vector: five entries corresponded to membership of that user in these 5 clusters (computed with a Gaussian kernel and then normalized so that they sum up to unity), and the sixth was a constant feature 1.
- **最終的なユーザ 特徴量は6ベクトル**であった: そのうち5つのエントリは、これらの5つのクラスターにおけるそのユーザーのメンバーシップに対応し(ガウスカーネルで計算され、それらの合計が1になるように正規化される)、6番目は定数特徴1であった。(5つの要素はone-hot encoding的なbinaryかと思ったけどそうでもない?)

At trial t, each article a has a separate six-dimensional feature xt,a that is exactly the six-dimensional feature constructed as above for user ut.
試行 $t$ において、各記事aは、ユーザ $u_t$ について上記のように構築された6次元特徴量 $x_{t,a}$ を持つ。
Since these article features do not overlap, they are for disjoint linear models defined in Section 3.
これらの記事の特徴量は重ならないので、セクション3で定義されたdisjointな線形モデルのためのものである。

<!-- 上記はユーザ特徴量の前処理の話 -->

For each article a, we performed the same dimensionality reduction to obtain a six-dimensional article feature (including a constant 1 feature).
各記事aについて、同じように次元削減を行い、**6次元の記事特徴(定数1の特徴を含む)**を得た。
Its outer product with a user feature gave 6 × 6 = 36 features, denoted $z_{t,a} \in \mathbb{R}^{36}$, that corresponded to the shared features in Eq.(6), and thus (zt,a, xt,a) could be used in the hybrid linear model.
そのユーザ特徴量との外積は6×6＝36個の特徴量を与え、$z_{t,a} \in \mathbb{R}^{36}$ と表される。これは、式(6)のshared特徴量に対応するため、$(z_{t,a}, x_{t,a})$ をハイブリッド線形モデルに用いることができる。
Note the features zt,a contains user-article interaction information, while xt,a contains user information only.
特徴量 $z_{t,a}$ はユーザと記事の相互作用情報を含み、$x_{t,a}$ はユーザ情報のみを含むことに注意。

Here, we intentionally used five users (and articles) groups, which has been shown to be representative in segmentation analysis [13].
**ここでは、セグメンテーション分析において代表的であることが示されている5つのユーザ(および記事)グループを意図的に使用した**[13]。(なにそれ??)
Another reason for using a relatively small feature space is that, in online services, storing and retrieving large amounts of user/article information will be too expensive to be practical.
**比較的小さな特徴量空間を使用するもう一つの理由は、オンラインサービスでは、大量のユーザ／記事情報を保存したり検索したりすることは、コストがかかりすぎて実用的ではないからである。**

## 5.3 Compared Algorithms

The algorithms empirically evaluated in our experiments can be categorized into three groups: I.
我々の実験で経験的に評価されたアルゴリズムは、**3つのグループ**に分類できる：

### I. Algorithms that make no use of features

特徴を利用しないアルゴリズム。
These correspond to the context-free K-armed bandit algorithms that ignore all contexts (i.e., user/article information).
これらは、すべてのコンテキスト（すなわち、ユーザー/記事情報）を無視するコンテキストフリーのKアームドバンディットアルゴリズムに対応する。

• random: A random policy always chooses one of the candidate articles from the pool with equal probability.

- ランダム： ランダムポリシーは、常に同じ確率でプールから候補の記事の一つを選ぶ。
  This algorithm requires no parameters and does not "learn" over time.
  このアルゴリズムはパラメーターを必要とせず、時間とともに「学習」することもない。
  • ǫ-greedy: As described in Section 2.2, it estimates each article's CTR; then it chooses a random article with probability ǫ, and chooses the article of the highest CTR estimate with probability 1 − ǫ.
- ↪L_1-greedy： セクション2.2で説明したように、各記事のCTRを推定する。次に、確率↪LlEBでランダムな記事を選択し、確率1 - ↪Ll_1EB で最も高いCTR推定値の記事を選択する。
  The only parameter of this policy is ǫ.
  この政策の唯一のパラメータは↪LlEB↩である。
  • ucb: As described in Section 2.2, this policy estimates each article's CTR as well as a confidence interval of the estimate, and always chooses the article with the highest UCB.
- ucbとする： セクション2.2で説明したように、このポリシーは各記事のCTRと推定値の信頼区間を推定し、常に最も高いUCBを持つ記事を選択する。
  Specifically, following UCB1 [7], we computed an article a's confidence interval by ct,a = α √ nt,a , where nt,a is the number of times a was chosen prior to trial t, and α > 0 is a parameter.
  具体的には、UCB1[7]に従って、我々は記事 a の信頼区間を、ct,a = α √ nt,a 、ここで nt,a は試行 t の前に a が選択された回数で、α > 0 はパラメータである。

• omniscient: Such a policy achieves the best empirical context-free CTR from hindsight.

- 全知全能： このような方針は、後知恵で最高の経験的文脈自由CTRを達成する。
  It first computes each article's empirical CTR from logged events, and then always chooses the article with highest empircal CTR when it is evaluated using the same logged events.
  まず、ログに記録されたイベントから各記事の経験的CTRを計算し、次に同じログに記録されたイベントを使って評価したときに、常に経験的CTRが最も高い記事を選択する。
  This algorithm requires no parameters and does not "learn" over time.
  このアルゴリズムはパラメーターを必要とせず、時間とともに「学習」することもない。

### II. Algorithms with "warm start" "warm start"によるアルゴリズム

an intermediate step towards personalized services.
パーソナライズド・サービスへの中間ステップ。
The idea is to provide an offline-estimated user-specific adjustment on articles' context-free CTRs over the whole traffic.
このアイデアは、トラフィック全体にわたる記事のcontext-free CTRについて、オフラインで推定されたユーザ固有の調整を提供することである。
The offset serves as an initialization on CTR estimate for new content, a.k.a."warm start".
このオフセットは、新しいコンテンツのCTR推定値の初期化、つまり「ウォームスタート」の役割を果たす。
We re-trained the bilinear logistic regression model studied in [12] on Sept 2008 random traffic data, using features zt,a constructed above.
我々は，[12]で研究されたバイリニア・ロジスティック回帰モデルを，上記で構築した特徴量zt,aを用いて，2008年9月のランダム・トラフィック・データで再トレーニングした．
The selection criterion then becomes the sum of the context-free CTR estimate and a bilinear term for a user-specific CTR adjustment.
**選択基準は、文脈のないCTR推定値と、ユーザー固有のCTR調整のためのバイリニア項の合計**となる。
In training, CTR was estimated using the context-free ǫ-greedy with ǫ = 1.
訓練では、↪Ll_1EB = 1の文脈自由(context-free ↪L_1EB↩-greedy)を用いてCTRを推定した。
(つまり、「全体傾向（context-free CTR）＋ユーザー補正（warm start）」でCTRを初期化するイメージ...!!:thinking:)

• ǫ-greedy (warm): This algorithm is the same as ǫ-greedy except it adds the user-specific CTR correction to the article's context-free CTR estimate.

- ↪L_1-greedy (warm)： このアルゴリズムは↪Ll_1-reedy と同じですが、**ユーザー固有の CTR 補正を記事のcontext-fee CTR 推定値に加えます。**
  • ucb (warm): This algorithm is the same as the previous one but replaces ǫ-greedy with ucb.
- ucb (warm)： このアルゴリズムは前のものと同じだが、 ↪L_1-greedy を ucb に置き換えたものである。

### Algorithms that learn user-specific CTRs online オンラインでユーザー固有のCTRを学習するアルゴリズム

• ǫ-greedy (seg): Each user is assigned to the closest user cluster among the five constructed in Section 5.2.2, and so all users are partitioned into five groups (a.k.a.

- ↪L_1-greedy (seg)： 各ユーザーはセクション5.2.2で構築された5つのユーザークラスタのうち、最も近いユーザークラスタに割り当てられるため、全ユーザーは5つのグループ（a.k.a.
  user segments), in each of which a separate copy of ǫ-greedy was run.
  ユーザー・セグメント)のそれぞれで、↪Ll_1-greedy の別個のコピーが実行された。

• ucb (seg): This algorithm is similar to ǫ-greedy (seg) except it ran a copy of ucb in each of the five user segments.

- ucb (seg)： このアルゴリズムは ucb のコピーを5つのユーザーセグメントのそれぞれで実行したことを除けば、 ↪L_1-greedy (seg) と似ている。
  • ǫ-greedy (disjoint): This is ǫ-greedy with disjoint models, and may be viewed as a close variant of epoch-greedy [18].
- ↪L_1-greedy (disjoint)： これはモデルが不連続な↪L_1EB↩ greedyであり、epoch-greedy [18]に近い変形とみなすことができる。
  • linucb (disjoint): This is Algorithm 1 with disjoint models.
- linucb (disjoint)： これは不連続モデルを用いたアルゴリズム1である。

• ǫ-greedy (hybrid): This is ǫ-greedy with hybrid models, and may be viewed as a close variant of epoch-greedy.

- ↪L_1-greedy (ハイブリッド)： これはハイブリッドモデルによる↪L_1- greedyであり、エポックグリーディに近い変種とみなすことができる。
  • linucb (hybrid): This is Algorithm 2 with hybrid models.
- linucb（ハイブリッド）： これはハイブリッドモデルを使ったアルゴリズム2である。

## 5.4 Performance Metric 5.4 パフォーマンス指標

An algorithm's CTR is defined as the ratio of the number of clicks it receives and the number of steps it is run.
**アルゴリズムのCTRは、クリック数と実行ステップ数の比率**として定義される。
We used all algorithms' CTRs on the random logged events for performance comparison.
パフォーマンス比較のために、ランダムに記録されたイベントに対する全アルゴリズムのCTRを使用した。
To protect business-sensitive information, we report an algorithm's relative CTR, which is the algorithm's CTR divided by the random policy's.
**ビジネス上の機密情報を保護するため、アルゴリズムのCTRを random policy のCTRで割った相対CTRを報告する**。(なるほど...!確かに。)
Therefore, we will not report a random policy's relative CTR as it is always 1 by definition.
したがって、random policy の**relative CTRは定義上常に1**であるため、報告しない。
For convenience, we will use the term "CTR" from now on instead of "relative CTR".
**便宜上、今後は「相対CTR」ではなく「CTR」という用語を使用する**。(ふむふむ)

For each algorithm, we are interested in two CTRs motivated by our application, which may be useful for other similar applications.
各アルゴリズムについて、我々は、**我々のアプリケーションによって動機づけられた2つのCTR**に興味がある。
When deploying the methods to Yahoo!'s front page, one reasonable way is to randomly split all traffic to this page into two buckets [3].
ヤフー!のトップページにメソッドを展開する場合、1つの合理的な方法は、このページへのすべてのトラフィックをランダムに**2つのバケツに分割すること**である[3]。(要するにA/Bテストか!:thinking:)
The first, called "learning bucket", usually consists of a small fraction of traffic on which various bandit algorithms are run to learn/estimate article CTRs.
"learning bucket"と呼ばれる最初のバケツは、通常、記事のCTRを学習/推定するために様々なバンディットアルゴリズムが実行されるトラフィックのごく一部で構成されています。
The other, called "deployment bucket", is where Yahoo! Front Page greedily serves users using CTR estimates obained from the learning bucket.
もうひとつは"deployment bucket"と呼ばれるもので、ヤフー・フロントページが学習バケットから得たCTR推定値を用いてユーザに貪欲に(??)サービスを提供する場所である。
Note that "learning" and "deployment" are interleaved in this problem, and so in every view falling into the deployment bucket, the article with the highest current (user-specific) CTR estimate is chosen; this estimate may change later if the learning bucket gets more data.
"learning"と "deployment"は、この問題ではインターリーブ(=混ざっている??)されているので、deploymentバケツに入るすべてのビューで、現在の(ユーザー固有の)CTR推定値が最も高い記事が選ばれる。
CTRs in both buckets were estimated with Algorithm 3.
両方のバケツにおけるCTRはアルゴリズム3で推定された。
Since the deployment bucket is often larger than the learning bucket, CTR in the deployment bucket is more important.
deploymentバケットは学習バケットより大きいことが多いので、deploymentバケットでのCTRはより重要である。
However, a higher CTR in the learning bucket suggests a faster learning rate (or equivalently, smaller regret) for a bandit algorithm.
しかし、learningバケツにおけるCTRが高いほど、バンディット・アルゴリズムの学習速度が速い(or 同等の意味で、regretが小さい)ことを示唆している。
Therefore, we chose to report algorithm CTRs in both buckets.
したがって、両方のバケツでアルゴリズムCTRを報告することにした。
(learning bubket と deployment bucket, まだ良くわかってない。hold-out法的な意味なんだろうか??)

## Experimental Results

### 5.5.1 Results for Tuning Data 5.5.1 チューニング・データの結果

Each of the competing algorithms (except random and omniscient) in Section 5.3 requires a single parameter: ǫ for ǫ-greedy algorithms and α for UCB ones.
セクション5.3で競合するアルゴリズム(ランダムと全知全能を除く)は、それぞれ1つのパラメータを必要とする：↪Ll_1-greedy アルゴリズムは、UCB アルゴリズムはαである。
We used tuning data to optimize these parameters.
これらのパラメーターを最適化するためにチューニングデータを使用した。
Figure 2 shows how the CTR of each algorithm changes with respective parameters.
**図2は、各アルゴリズムのCTRがそれぞれのハイパーパラメータによってどのように変化するかを示している。**
All results were obtained by a single run, but given the size of our dataset and the unbiasedness result in Theorem 1, the reported numbers are statistically reliable.
すべての結果は1回の実行で得られたものであるが、我々のデータセットのサイズと定理1の不偏性の結果を考えれば、報告された数字は統計的に信頼できるものである。

![fig2]()

First, as seen from Figure 2 , the CTR curves in the learning buckets often possess the inverted U-shape.
まず、図2からわかるように、**学習バケットのCTR曲線はしばしば逆U字型**をしている。
When the parameter (ǫ or α) is too small, there was insufficient exploration, the algorithms failed to identify good articles, and had a smaller number of clicks.
パラメータ($\epsilon$ または α)が小さすぎる場合、探索が不十分で、アルゴリズムは良い記事を識別できず、クリック数も少ない。
On the other hand, when the parameter is too large, the algorithms appeared to and thus wasted some of the opportunities to increase the number of clicks.
一方、パラメータが大きすぎる(=活用よりも探索しまくる!)場合、アルゴリズムはクリック数を増加させる機会を無駄にしたように見える。
Based on these plots on tuning data, we chose appropriate parameters for each algorithm and ran it once on the evaluation data in the next subsection.
チューニングデータに対するこれらのプロットに基づいて、各アルゴリズムに適切なパラメータを選択し、次のサブセクションで評価データに対して1回実行した。

Second, it can be concluded from the plots that warm-start information is indeed helpful for finding a better match between user interest and article content, compared to the no-feature versions of ǫ-greedy and UCB.
第二に、**warm-startの情報は、epsilon-greedy と UCB の特徴なしバージョンと比較して、ユーザの興味と記事内容のより良い一致を見つけるのに役立つ**とプロットから結論づけることができる。
Specifically, both ǫ-greedy (warm) and ucb (warm) were able to beat omniscient, the highest CTRs achievable by context-free policies in hindsight.
具体的には、epsilon-greedy (warm)とucb (warm)の両方が、後知恵で**context-free policy が達成可能な最高のCTRであるomiscientに勝つことができた**。
However, performance of the two algorithms using warm-start information is not as stable as algorithms that learn the weights online.
しかし、warm-start情報を使用する2つのアルゴリズムの性能は、オンラインで重みを学習するアルゴリズム(=cotextual-bandit)ほど安定していない。
Since the offline model for "warm start" was trained with article CTRs estimated on all random traffic [12], ǫ-greedy (warm) gets more stable performance in the deployment bucket when ǫ is close to 1.
warm-startのオフライン・モデルは、すべてのランダムなトラフィックで推定された記事 CTR を使ってトレーニングされたので [12]、epsilon-greedy (warm)は、epsilon が 1 に近いとき(=全部探索するケース!)、デプロイメント・バケットでより安定したパフォーマンスを得る。
The warm start part also helps ucb (warm) in the learning bucket by selecting more attractive articles to users from scratch, but did not help ucb (warm) in determining the best online for deployment.
warm-startの部分は、ユーザにとってより魅力的な記事をゼロから選択することによって、ucb (warm)の学習バケットでの性能にも役立つが、ucb (warm)がdeploymentバケットに最適なオンラインを決定するのには役立たなかった。
Since ucb relies on the a confidence interval for exploration, it is hard to correct the initialization bias introduced by "warm start".
**ucbは信頼区間を用いて探索を行うため、"warm-start"によって生じる初期化バイアスを修正することは難しい**。
In contrast, all online-learning algorithms were able to consistently beat the omniscient policy.
**対照的に、すべてのオンライン学習アルゴリズムは、常に全知全能のpolicyを打ち負かすことができた**。
Therefore, we did not try the warm-start algorithms on the evaluation data.
したがって、ウォームスタートアルゴリズムを評価データで試すことはしなかった。

Third, ǫ-greedy algorithms (on the left of Figure 2 ) achieved similar CTR as upper confidence bound ones (on the right of Figure 2 ) in the deployment bucket when appropriate parameters were used.
第三に、**epsilon-greedy アルゴリズム達（図2の左）は、適切なパラメータ(epsilon)を使用した場合、deploymentバケットにおいてUCBアルゴリズム達（図2の右）と同様のCTRを達成した**。
Thus, both types of algorithms appeared to learn comparable policies.
したがって、どちらのタイプのアルゴリズムも、同等のpolicyを学習しているように見えた。
However, they seemed to have lower CTR in the learning bucket, which is consistent with the empirical findings of contextfree algorithms [2] in real bucket tests.
しかし、学習バケツではCTRが低いようで、これは実際のバケツテストにおけるcontext-free アルゴリズム[2]の経験的知見と一致する。(??)

Finally, to compare algorithms when data are sparse, we repeated the same parameter tuning process for each algorithm with fewer data, at the level of 30%, 20%, 10%, 5%, and 1%.
最後に、データがまばらな場合のアルゴリズムを比較するため、各アルゴリズムについて、30％、20％、10％、5％、1％のレベルで、少ないデータで同じパラメータチューニングプロセスを繰り返した。
Note that we still used all data to evaluate an algorithm's CTR as done in Algorithm 3, but then only a fraction of available data were randomly chosen to be used by the algorithm to improve its policy.
アルゴリズム3で行われたように、**アルゴリズムのCTRを評価するためにすべてのデータを使用することに変わりはない**が、その後、利用可能なデータの一部のみが、アルゴリズムがそのpolicyを改善するために使用するためにランダムに選択されたことに注意してください。(=学習には少量のデータを使用したよ)

### 5.5.2 Results for Evaluation Data

![table1]()

With parameters optimized on the tuning data (c.f., Figure 2 ), we ran the algorithms on the evaluation data and summarized the CTRs in Table 1 .
チューニング・データで最適化されたパラメータ(図2参照)を用いて、評価データでアルゴリズムを実行し、CTR(relative CTR)を表1にまとめた。
The table also reports the CTR lift compared to the baseline of ǫ-greedy.
この表は、$\epsilon$-greedy のベースラインと比較した CTR lift(比率)も示している。
The CTR of omniscient was 1.615, and so a significantly larger CTR of an algorithm indicates its effective use of user/article features for personalization.
全知全能のCTRは1.615であり(table1にはない?)、アルゴリズムのCTRが著しく大きいことは、パーソナライゼーションのためにユーザ/記事の特徴を効果的に利用していることを示す。
Recall that the reported CTRs were normalized by the random policy's CTR.
報告されたCTRはランダムポリシーのCTRで正規化されたことを思い出してほしい。(relative CTRだよ!)
We examine the results more closely in the following subsections.
以下のサブセクションで、その結果をさらに詳しく検証する。

#### On the Use of Features

機能の使用について。

We first investigate whether it helps to use features in article recommendation.
まず、記事の推薦に特徴量を使うことが役に立つかどうかを調査する。
It is clear from Table 1 that, by considering user features, both ǫ-greedy (seg/disjoint/hybrid) and UCB methods (ucb (seg) and linucb (disjoint/hybrid)) were able to achieve a CTR lift of around 10%, compared to the baseline ǫ-greedy.
表1から明らかなように、**ユーザの特徴を考慮することで**、$\epsilon$-greedy (seg/disjoint/hybrid)とUCBメソッド(ucb (seg)とlinucb (disjoint/hybrid))の両方が、**ベースラインの$\epsilon$-greedyと比較して、約10%のCTR lift を達成することができました**。

![fig3]()

To better visualize the effect of features, Figure 3 shows how an article's CTR (when chosen by an algorithm) was lifted compared to its base CTR (namely, the context-free CTR).4 Here, an article's base CTR measures how interesting it is to a random user, and was estimated from logged events.
特徴量の効果をよりよく視覚化するために、**図3は、記事のCTR（アルゴリズムによって選択されたとき）がその基本CTR（すなわち、context-free CTR）と比較してどのように持ち上げられたか(=CTR lift)を示している**。ここで、記事の基本CTRは、それがランダムなユーザにとってどの程度興味深いかを測定し、logged イベントから推定された。
Therefore, a high ratio of the lifted and base CTRs of an article is a strong indicator that an algorithm does recommend this article to potentially interested users.
したがって、**ある記事(各plot点は記事か!)のリフトされたCTRとベースのCTRの比率が高い事(=plot点の原点からのx軸, y軸方向の距離が正方向に遠い事!:thinking:)は、アルゴリズムが潜在的に関心のあるユーザにこの記事を推薦しているという強い指標となる**。
the other three plots show clear benefits by considering personalized recommendation.
他の3つのプロットでは、**パーソナライズされた推薦を考慮することで、明確な利点があることを示している**。(3(a)では両方とも context-freeなアルゴリズムなので、ほぼ同程度の結果になっている事を示している.)
In an extreme case (Figure 3 (c)), one of the article's CTR was lifted from 1.31 to 3.03-a 132% improvement.
極端な例では（図3 (c)）、ある記事のCTRが1.31から3.03に上がり、これは132%の改善である。
Furthermore, it is consistent with our previous results on tuning data that, compared to ǫ-greedy algorithms, UCB methods achieved higher CTRs in the deployment bucket, and the advantage was even greater in the learning bucket.
さらに、**$\epsilon$-greedy アルゴリズムと比較して、UCB 手法はdevelopmentバケツでより高い CTR を達成**し、学習バケツではその優位性がさらに高まるという、チューニングデータに関する我々の以前の結果とも一致する.
As mentioned in Section 2.2, ǫgreedy approaches are unguided because they choose articles uniformly at random for exploration.
セクション2.2で述べたように、$\epsilon$greedy アプローチは、探索のために記事を一様にランダムに選択するため、unguided(=誘導されない=ずっとそのまま?)である。
In contrast, exploration in upper confidence bound methods are effectively guided by confidence intervals-a measure of uncertainty in an algorithm's CTR estimate.
対照的に、UCBの探索は、アルゴリズムのCTR推定値の不確実性の尺度である信頼区間によって効果的に導かれる。
Our experimental results imply the effectiveness of upper confidence bound methods and we believe they have similar benefits in many other applications as well.
我々の実験結果は、UCBの有効性を示唆しており、他の多くのアプリケーションにおいても同様の利点があると信じている。

#### On the Size of Data　データのサイズについて

<!-- このセクションは実運用で重要そう -->

One of the challenges in personalized web services is the scale of the applications.
**パーソナライズされたウェブサービスにおける課題の1つは、アプリケーションの規模**である。
In our problem, for example, a small pool of news articles were hand-picked by human editors.
例えば、私たちの問題では、ニュース記事の小さなプールは人間の編集者によって手作業で選ばれた。
But if we wish to allow more choices or use automated article selection methods to determine the article pool, the number of articles can be too large even for the high volume of Yahoo! traffic.
しかし、より多くの選択肢を許容したり、記事プールを決定するために自動化された記事選択方法を使用したい場合、記事の数はヤフーのトラフィック量が多いにもかかわらず多すぎる可能性があります。
Therefore, it becomes critical for an algorithm to quickly identify a good match between user interests and article contents when data are sparse.
**したがって、データがまばらな場合、ユーザーの興味と記事の内容の間の良い一致を素早く識別するアルゴリズムが重要になる。**
In our experiments, we artificially reduced data size (to the levels of 30%, 20%, 10%, 5%, and 1%, respectively) to mimic the situation where we have a large article pool but a fixed volume of traffic.
実験では、データサイズを人為的に縮小し（それぞれ30％、20％、10％、5％、1％）、記事プールは大きいがトラフィック量は一定という状況を模倣した。

To better visualize the comparison results, we use bar graphs in Figure 4 to plot all algorithms' CTRs with various data sparsity levels.
比較結果をよりよく視覚化するために、図4では棒グラフを用いて、様々なデータスパースティレベルでの全アルゴリズムのCTRをプロットしている。
A few observations are in order.
いくつかの見解を述べておこう。
First, at all data sparsity levels, features were still useful.
**まず、どのようなデータ疎密レベルにおいても、特徴量は依然として有用**であった。
At the level of 1%, for instance, we observed a 10.3% improvement of linucb (hybrid)'s CTR in the deployment bucket (1.493) over ucb's (1.354).
例えば、1％のレベルでは、デプロイメントバケットにおけるlinucb（ハイブリッド）のCTR（1.493）は、ucbのCTR（1.354）よりも10.3％向上している。

Second, UCB methods consistently outperformed ǫ-greedy ones in the deployment bucket.5 The advantage over ǫ-greedy was even more apparent when data size was smaller.
第二に、UCB法はデプロイメント・バケットにおいて常に↪Ll_1- greedy法を上回った5。↪Ll_1- greedy法に対する優位性は、データサイズが小さいほど顕著であった。

Third, compared to ucb (seg) and linucb (disjoint), linucb (hybrid) showed significant benefits when data size was small.
第三に、ucb（seg）とlinucb（disjoint）に比べて、linucb（hybrid）はデータサイズが小さいときに大きな利点を示した。
Recall that in hybrid models, some features are shared by all articles, making it possible for CTR information of one article to be "transferred" to others.
ハイブリッドモデルでは、いくつかの特徴はすべての記事で共有され、ある記事のCTR情報を他の記事に「転送」することが可能である。
This advantage is particularly useful when the article pool is large.
この利点は、記事プールが大きい場合に特に有効である。
In contrast, in disjoint models, feedback of one article may not be utilized by other articles; the same is true for ucb (seg).
対照的に、不連続モデルでは、ある記事のフィードバックが他の記事で利用されることはない。
Figure 4 (a) shows transfer learning is indeed helpful when data are sparse.
図4(a)は、データが疎な場合に転移学習が実際に役立つことを示している。

#### Comparing ucb (seg) and linucb (disjoint)

ucb（seg）とlinucb（disjoint）の比較。

![fig4]()

From Figure 4 (a), it can be seen that ucb (seg) and linucb (disjoint) had similar performance.
図4 (a)から、ucb (seg)とlinucb (disjoint)は同じようなパフォーマンスであることがわかる。
We believe it was no coincidence.
偶然ではないと信じている。
Recall that features in our disjoint model are actually normalized membership measures of a user in the five clusters described in Section 5.2.2.
我々のdisjointモデルにおける特徴量は、実際にはセクション5.2.2で説明した5つのクラスターにおけるユーザの正規化されたメンバーシップ測定値であることを思い出してください。
Hence, these features may be viewed as a "soft" version of the user assignment process adopted by ucb (seg).
**したがって、これらの特徴量は、ucb(seg)が採用したユーザー割り当てプロセスの「ソフト」バージョンとみなすことができる**。

![fig5]()

Figure 5 plots the histogram of a user's relative membership measure to the closest cluster, namely, the largest component of the user's five, non-constant features.
図5は、**最も近いクラスター**、すなわちユーザーの5つの特徴量のうち最も大きい成分(一定でない特徴量)に対するユーザーの相対的なメンバーシップ尺度のヒストグラムをプロットしたものである。
It is clear that most users were quite close to one of the five cluster centers: the maximum membership of about 85% users were higher than 0.5, and about 40% of them were higher than 0.8.Therefore, many of these features have a highly dominating component, making the feature vector similar to the "hard" version of user group assignment.
約85％のユーザの最大メンバーシップは0.5より高く、約40％のユーザーは0.8より高かった。**したがって、これらの特徴量の多くは非常に支配的な成分を持ち、特徴量ベクトルはユーザーグループ割り当ての「ハード」バージョンに似ている**。(ユーザがあるクラスターに強く属している場合、特徴量ベクトルはそのクラスターにほぼ一致するから。なのでユーザセグメント毎のcontect-free banditと同じような結果になる...!:thinking:)

We believe that adding more features with diverse components, such as those found by principal component analysis, would be necessary to further distinguish linucb (disjoint) from ucb (seg).
我々は、**linucb（disjoint）とucb（seg）をさらに区別するためには、主成分分析によって見出されるような多様な成分を持つ特徴量をさらに加えることが必要**だと考えている。

# 6. CONCLUSIONS 6. 結論

This paper takes a contextual-bandit approach to personalized web-based services such as news article recommendation.
本稿では、ニュース記事の推薦のようなパーソナライズされたウェブベースのサービスに対して、コンテクスチュアル・バンディット・アプローチを採用する。
We proposed a simple and reliable method for evaluating bandit algorithms directly from logged events, so that the often problematic simulator-building step could be avoided.
**記録されたイベントから直接バンディット・アルゴリズムを評価するためのシンプルで信頼性の高い方法を提案**し、しばしば問題となるシミュレータ構築のステップを回避できるようにした。
Based on real Yahoo! Front Page traffic, we found that upper confidence bound methods generally outperform the simpler yet unguided ǫ-greedy methods.
実際のYahoo! Front Pageのトラフィックに基づき、我々は、UCBが、一般的に、より単純であるがガイドのないepsilon-greedy法を上回ることを発見した。
Furthermore, our new algorithm LinUCB shows advantages when data are sparse, suggesting its effectiveness to personalized web services when the number of contents in the pool is large.
さらに、我々の新しいアルゴリズムLinUCBは、**データが疎な場合に優位性を示し、これはプール内のコンテンツ数が多い場合にパーソナライズされたウェブサービスに有効である**ことを示唆している。

In the future, we plan to investigate bandit approaches to other similar web-based serviced such as online advertising, and compare our algorithms to related methods such as Banditron [16].
将来的には、バンディット・アプローチをオンライン広告のような他の類似したウェブベースのサービスに対して調査し、我々のアルゴリズムをバンディトロン[16]のような関連する手法と比較する予定である。
A second direction is to extend the bandit formulation and algorithms in which an "arm" may refer to a complex object rather than an item (like an article).
第二の方向性は、バンディットの定式化とアルゴリズムを拡張し、「腕」が（物品のような）アイテムではなく、複雑な物体を指すようにすることである。
An example is ranking, where an arm corresponds to a permutation of retrieved webpages.
例えば、アームが検索されたウェブページの並べ替えに対応するランキングである。
Finally, user interests change over time, and so it is interesting to consider temporal information in bandit algorithms.
最後に、ユーザの興味は時間とともに変化するため、バンディット・アルゴリズムにおいて時間情報を考慮することは興味深い。
