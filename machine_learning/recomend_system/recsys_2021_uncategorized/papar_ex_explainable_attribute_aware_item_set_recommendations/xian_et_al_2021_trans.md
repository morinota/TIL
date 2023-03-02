## link 

- https://assets.amazon.science/d3/ad/9af131bd49b8a0697c6bd763a1cf/ex3-explainable-attribute-aware-item-set-recommendations.pdf httpsを使用しています。

- https://www.wantedly.com/companies/wantedly/post_articles/350652 httpsを使用しています。

## title タイトル

EX3 : Explainable Attribute-aware Item-set Recommendations
EX3 : 説明可能な属性考慮型アイテムセット勧告

## abstract アブストラクト

Existing recommender systems in the e-commerce domain primarily focus on generating a set of relevant items as recommendations; however, few existing systems utilize underlying item attributes as a key organizing principle in presenting recommendations to users.
電子商取引分野における既存のレコメンダーシステムは、関連するアイテムセットをレコメンデーションとして生成することに主眼を置いている。しかし、既存のシステムでは、ユーザーにレコメンデーションを提示する際の重要な組織原理として、アイテムの基本属性を利用しているものはほとんどない。
Mining important attributes of items from customer perspectives and presenting them along with item sets as recommendations can provide users more explainability and help them make better purchase decision.
しかし、既存のシステムでは、アイテムの属性を重要な組織原理として利用するものはほとんどない。顧客の視点からアイテムの重要な属性を抽出し、アイテムセットとともに推薦として提示することで、ユーザーに説明可能性を提供し、より良い購買決定を支援することができる。
In this work, we generalize the attribute-aware item-set recommendation problem, and develop a new approach to generate sets of items (recommendations) with corresponding important attributes (explanations) that can best justify why the items are recommended to users.
本研究では、属性考慮型アイテムセット推薦問題を一般化し、アイテムセット（推薦）と、そのアイテムをユーザに推薦する理由を最もよく説明できる重要な属性（説明）を対応づけて生成する新しいアプローチを開発する。
In particular, we propose a system that learns important attributes from historical user behavior to derive item set recommendations, so that an organized view of recommendations and their attribute-driven explanations can help users more easily understand how the recommendations relate to their preferences.
特に、過去のユーザー行動から重要な属性を学習し、アイテムセットの推薦を導き出すシステムを提案する。これにより、推薦とその属性に基づいた説明を整理して表示することで、ユーザーは推薦と自分の好みの関連性をより容易に理解することができるようになる。
Our approach is geared towards real world scenarios: we expect a solution to be scalable to billions of items, and be able to learn item and attribute relevance automatically from user behavior without human annotations.
私たちのアプローチは実世界のシナリオを対象としており、何十億ものアイテムに拡張可能で、人間の注釈なしにユーザーの行動からアイテムや属性の関連性を自動的に学習できるソリューションが求められている。
To this end, we propose a multi-step learning-based framework called Extract-Expect-Explain (EX3 ), which is able to adaptively select recommended items and important attributes for users.
このため、我々はExtract-Expect-Explain (EX3) と呼ばれる多段階学習ベースのフレームワークを提案し、ユーザが推奨するアイテムや重要な属性を適応的に選択することができるようにする。
We experiment on a large-scale real-world benchmark and the results show that our model outperforms state-of-the-art baselines by an 11.35% increase on NDCG with adaptive explainability for item set recommendation.
我々は大規模な実世界ベンチマークで実験を行い、その結果、我々のモデルは項目セット推薦のための適応的説明可能性を持つNDCGにおいて、最新技術のベースラインを11.35%上回る性能を持つことを示す。

# Introduction はじめに

Recommender systems have been widely deployed in modern e-commerce websites, helping users overcome overwhelming selection issues in large catalogs and contributing large business impact [9, 20, 32].
レコメンダーシステムは、現代の電子商取引サイトに広く導入されており、大規模なカタログにおける圧倒的な選択の問題を克服し、大きなビジネスインパクトに貢献している [9, 20, 32]。
Many existing recommender systems in industry focus on generating a set of relevant items based on a set of pivot
このようなレコメンダーシステムは，ユーザが膨大なカタログから商品を選択する際の問題を解決し，ビジネスに大きな影響を与える．

Throughout the paper, we study the explainable attribute-aware item-set recommendation problem by learning an item-to-item-set mapping guided by attribute differences.
本論文では、属性の違いによって導かれるアイテムからアイテムへのマッピングを学習することで、説明可能な属性を考慮したアイテムセット推薦問題を研究する。
Formally, given a “pivot” item, our goal is to generate 𝐾 sets of items (recommendations), each of which is associated with an important attribute (explanation) to justify why the items are recommended to users.
形式的には、「ピボット」アイテムが与えられたとき、我々の目標は、各アイテムがユーザに推奨される理由を正当化するための重要な属性（説明）と関連付けられたアイテム（推奨）のᵃセット を生成することである。
We aim to not only generate relevant item recommendations, but also provide corresponding explanations based on those important item attributes whose value changes will affect user purchase decision.
我々は、適切なアイテムの推薦を生成するだけでなく、値の変化がユーザーの購買意思決定に影響を与える重要なアイテムの属性に基づいて、対応する説明を提供することを目指している。
Unlike existing work [3] that focuses primarily on making understandable substitute recommendations, we attempt to help users broaden their consideration set by presenting them with differentiated options by attribute type.
既存の研究[3]が主に理解しやすい代替品の推薦に焦点を当てたのとは異なり、我々は属性タイプによって差別化された選択肢を提示することで、ユーザーの検討範囲を広げる手助けをすることを試みる。
Additionally, different from generating explanations based on user–item and item–attribute interactions [3], we propose to infer important attributes directly from users’ historical behaviors, providing a framework to understand how users reason about recommendations when making decisions.
さらに、ユーザーアイテムやアイテム-属性の相互作用に基づく説明の生成[3]とは異なり、我々はユーザーの過去の行動から直接重要な属性を推測することを提案し、ユーザーが意思決定を行う際にどのように推薦を理由づけるかを理解するための枠組みを提供する。
To the best of our knowledge, we are the first to approach the explainable item-set recommendations via behavior-oriented important attribute identification in e-commerce domain.
我々の知る限り、電子商取引領域において、行動指向の重要属性推定による説明可能なアイテムセット推薦にアプローチしたのは我々が初めてである。

The main idea in solving this problem is to first learn important attributes based on users’ historical behaviors, and then generate corresponding item recommendations.
この問題を解決するための主なアイデアは、まずユーザの過去の行動から重要な属性を学習し、それに対応するアイテム推薦を生成することである。
Note that learning important attributes can benefit many other applications beyond item-set recommendations alone.
重要な属性を学習することは、アイテムセットの推薦だけでなく、他の多くのアプリケーションに利益をもたらすことに注意する必要がある。
Modeling behavior-oriented attribute importance from users’ historical actions rather than manual identification is a critical component to conduct explainable recommendations.
説明可能な推薦を行うためには、手動で識別するのではなく、ユーザーの過去の行動から行動指向の属性重要度をモデル化することが重要な要素である。
It saves time-consuming effort in manual labeling and provides a more robust way to model user preference.
これは、手動でのラベル付けにかかる時間を節約し、ユーザーの嗜好をより強固にモデル化する方法である。
Once important attributes are derived, we can utilize them to build user profiles, e.g., identifying users’ preferred size, color, flavor, etc, which can be used in generating personalized recommendations.
重要な属性が導き出されると、それを利用してユーザープロファイルを構築することができる。例えば、ユーザーの好みのサイズ、色、味などを特定し、パーソナライズされたレコメンデーションの生成に利用することが可能である。
We can also perform brief item summarization based on important attributes, and the proposed method can also be easily extended to involve more contextual information (e.g., users’ sequential actions) to provide customized item summarization [40].
また、重要な属性に基づいて簡単なアイテムの要約を行うことができる。提案手法は、より多くの文脈情報（例えば、ユーザーの連続した行動）を含むように簡単に拡張することができ、カスタマイズされたアイテムの要約を提供することができる[40]。
We can further leverage the behavior-driven important attributes to advance query rewriting techniques in the item search domain, by attending to those terms that are closely related to items’ important attributes.
さらに、行動駆動型の重要属性を活用し、アイテムの重要属性と密接に関連する用語に注目することで、アイテム検索領域におけるクエリ書き換え技術を発展させることができる。

To this end, we propose a multi-step framework called Extract-Expect-Explain (EX3 ) to approach the explainable item-set recommendation problem.
そこで、説明可能な項目集合推薦問題にアプローチするために、Extract-Expect-Explain (EX3) と呼ばれる多段階のフレームワークを提案する。
Our EX3 framework takes as input a pivot
このEX3フレームワークでは、入力としてピボット

To guarantee the robustness and scalability in real world environment, EX3 is carefully designed to overcome several inherent challenges.
EX3は、実環境での堅牢性と拡張性を保証するために、いくつかの課題を克服するように慎重に設計されている。
(1) The foremost challenge is how to dynamically recommend items and attributes that provide comprehensive information contributed to users’ purchase decision.
(1) 最も重要な課題は、ユーザの購買意思決定に貢献する包括的な情報を提供するアイテムや属性をどのように動的に推薦するかである。
In this work, we propose to train EX3 with user behavior signals in the distant supervision manner, and leverage attribute value difference and historical purchase signals to capture user-behavior driven important attributes.
本研究では、ユーザの行動信号を遠隔監視方式で学習させ、属性値の差と過去の購買信号を利用して、ユーザ行動主導の重要な属性を捕捉することを提案する。
We believe that the important attributes are those whose value changes will critically affect users’ purchase decision, e.g., size for shoes, roast type for coffee.
重要な属性とは、例えば、靴のサイズやコーヒーの焙煎度など、その値の変化がユーザの購買意思決定に決定的な影響を与えるものであると我々は考えている。
(2) In real-world environment, we are always facing data challenges, especially on the attribute missing
(2)実世界では常にデータの問題に直面し、特に属性の欠落が問題となっている。

- We highlight the importance of jointly considering important attributes and relevant items in achieving the optimal user experience in explainable recommendations. 説明可能なレコメンデーションにおいて最適なユーザー体験を実現するために、重要な属性と関連する項目を共同で考慮することの重要性を強調する。

- We propose a novel three-step framework, EX3 , to approach the explainable attribute-aware item-set recommendation problem along with couples of novel components. The whole framework is carefully designed towards large-scale real-world scenario. 我々は、説明可能な属性考慮型アイテムセット推薦問題にアプローチするための新しい3ステップのフレームワーク、EX3を、新しいコンポーネントのカップリングとともに提案する。 このフレームワークは、大規模な実世界のシナリオを想定して慎重に設計されている。

- We extensively conduct experiments on the real-world benchmark for item-set recommendations. The results show that EX3 achieves 11.35% better NDCG than state-of-the-art baselines, as well as better explainability in terms of important attribute ranking. 我々は、アイテムセット推薦の実世界ベンチマークに対する実験を広範に行った。 その結果、EX3は最新のベースラインと比較して11.35%のNDCGの向上を達成し、重要属性ランキングの説明可能性も向上することがわかった。

# Preliminary 予備

In this section, we start with the introduction of relevant concepts and formulation of the explainable attribute-aware item-set recommendation problem.
本節では、まず、説明可能な属性考慮型項目集合推薦問題の概念と定式化について述べる。
Then, we introduce how to approach this problem via distant supervision.
そして、遠隔監視によるこの問題へのアプローチ方法を紹介する。

## Problem Formulation. Problem Formulation (問題の定式化)

Let P be the universal set of items and A be the set of all available attributes. We define the attribute value to be a function 𝑣 : P × A ↦→ C𝑑𝑣 that maps an item and an attribute to a sequence of characters, where C denotes a set of predefined characters and 𝑑𝑣 is the maximum length of the sequence.1 An item 𝑝 ∈ P is said to have value 𝑣(𝑝, 𝑎) on attribute 𝑎 ∈ A if 𝑣(𝑝, 𝑎) ≠ ∅. Accordingly, the attribute-value pairs of an item 𝑝 on multiple attributes are defined as 𝐴𝑝 = {(𝑎1, 𝑣1), . . . , (𝑎
𝐴𝑝

Definition 1 (Problem Definition).
定義 1 (問題の定義).
Given the pivot item 𝑞 ∈ P with attribute-value pairs 𝐴𝑞, and the number of groups, 𝐾, the goal is to output 𝐾 ordered explainable groups 𝐺𝑎(1) , . . .
属性値の組↪L_1D45↩を持つピボット・アイテム𝑞∈P、およびグループの数ᵃが与えられたとき、目標は、𝑎𝐾の順序付き説明可能グループᵃ（1） , ... ... を出力することである。
,𝐺𝑎(𝐾) such that the user utility (e.g., purchase) of displaying 𝐾 such groups is maximized.
𝐾を表示することによるユーザの効用（例えば、購入）が最大になるようなᵄ(ᵃ)を出力することである。

Intuitively, the goal of the problem is to recommend 𝐾 groups of items with attributes such that the likelihood of these recommended items being clicked or purchased is maximized after users compare them with the pivot item and view the displayed attribute-based justifications.
直感的には、問題の目的は、ユーザーがピボット項目と比較し、表示された属性に基づく正当性を見た後、これらの推奨項目がクリックまたは購入される可能性が最大となるような属性を持つ項目群ᵃを推奨することである。
In other words, it is required to generate important attributes given different pivot and candidate items so that they are useful to users, e.g., “screen resolution” is relatively more important than “height” for a TV item.
つまり、テレビであれば「高さ」よりも「画面解像度」の方が相対的に重要であるなど、異なるピボット項目と候補項目を与えて、ユーザにとって有用な重要属性を生成することが求められる。
Note that the explainable item set recommendation can be considered to be a item-to-item-set recommendation problem in e-commerce shopping scenario, and we assume user context information is not available in this work.
なお、説明可能なアイテムセット推薦とは、電子商取引におけるアイテムからアイテムセットへの推薦問題と考えることができ、本研究ではユーザのコンテキスト情報が利用できないことを想定している。
The challenges of this problem are threefold.
この問題の課題は3つある。

- How to automatically identify important attributes without supervision and aggregate relevant items into the corresponding groups for recommendation? どのようにして、監視なしに自動的に重要な属性を特定し、関連する項目を対応するグループに集約して推薦するのか？

- How to make the model robust to the data issues including missing attributes and noisy and arbitrary values? 欠損属性やノイズの多い恣意的な値などのデータ問題に対して、どのようにモデルをロバスト化するか？

- How to effectively reduce the search space of seeking similar items for item set recommendation and make the model scalable to large real-world dataset? 項目セット推薦のための類似項目探索空間を効率的に縮小し、実世界の大規模データセットに対してスケーラブルなモデルを実現するにはどうすればよいか？

## Distant Supervision. Distant Supervision (遠隔監督)。

In order to capture the comparable relationship among various items, we consider three common user behavior signals to construct datasets to provide distant supervision [11, 20, 30]: co-purchase (Bcp), co-view (Bcv) and purchase-after-view (Bpv) between items, where Bcp, Bcv, Bpv ⊆ P × P denote how items are co-purchased, co-viewed and view-then-purchased together.
ここで、Bcp, Bcv, Bpv ⊆ P × P は、アイテムがどのように共同購入、共同視聴、視聴後購入されたかを表す。
From the above definition, one can notice that Bpv offers an opportunity to simulate users’ shopping behaviors.
上記の定義から、Bpvはユーザーの買い物行動をシミュレートする機会を提供することに気づくことができる。
When users view an item and then purchase another one in a short period of time (e.g., within the same session), it is reasonable to assume that users are making comparison between relevant items.
ユーザーがあるアイテムを閲覧した後、短時間で（例えば、同じセッション内で）別のアイテムを購入する場合、ユーザーは関連するアイテム間の比較を行っていると考えるのが妥当でしょう。
Through empirical analysis on Amazon Mechanical Turk (MTurk), we observe that item pairs within Bpv have more than 80% similarities, which verifies our assumption that users are comparing similar items before purchase.
Amazon Mechanical Turk (MTurk) での実証分析を通じて、Bpv内のアイテムペアは80%以上の類似性を持つことが観察され、これはユーザーが購入前に類似したアイテムを比較しているという我々の仮定を検証しています。
In order to further improve the relevance from raw behavior signals to build up distant supervision with high quality, by further combing Bcp and Bcv, we conduct several annotation experiments via MTurk and observe that B = Bcv ∩ Bpv − Bcp, which contains items pairs in both Bcv and Bpv but not in Bcp, gives us the best relevance signals and mimics users’ shopping actions on Bpv.
BcpとBcvを組み合わせることによって、高品質の遠隔監視を構築するために、生の行動信号からの関連性をさらに改善するために、我々はMTurkを介していくつかのアノテーション実験を行い、B = Bcv∩Bpv - Bcpは、BcvとBpv両方にあるがBcpにはないアイテムペアを含む、最高の関連信号とBpv上のユーザーのショッピングアクションを真似して与えることを確認します。
Throughout the paper, we will use this way to construct datasets for model learning and offline evaluation on multiple item categories.
本論文では、この方法を用いて、複数のアイテムカテゴリに対するモデル学習とオフライン評価のためのデータセットを構築する。

# Proposed Method 提案された方法

In this section, we first formulate an optimization-based method for the explainable attribute-aware item-set recommendation problem and pose several potential issues of this solution in industrial scenario.
本節では、まず、説明可能な属性を考慮した項目集合推薦問題に対する最適化ベースの手法を定式化し、産業シナリオにおけるこのソリューションの潜在的な問題点をいくつか指摘する。
Then, we propose a novel learning-based framework called Extract-Expect-Explain (EX3 ) as a feasible and scalable alternative.
次に、拡張可能で実現可能な代替案として、Extract-Expect-Explain (EX3) と呼ばれる新しい学習ベースの枠組みを提案する。

An Optimization-based Method.
最適化に基づく方法。

Suppose we have a utility function 𝑢(𝑞, 𝑝, 𝑎) that estimates how likely users will click (or purchase) a recommended item 𝑝 ∈ P after comparing it with the pivot item 𝑞 ∈ P on attribute 𝑎 ∈ A, i.e., 𝑢 : P × P × A ↦→ [0, 1].
属性 𝑞 ﹑ である推奨アイテム ᵄ をピボットアイテム 𝑞 と比較した後、ユーザーがどの程度クリック（または購入）するかを推定する効用関数 𝑢（𝑞，↪Ll_21D45E ）、すなわちᵄ : P × P × A⇔→ [0，1] があるとする。
We can formulate an optimization problem for explainable item set recommendation as follows.
説明可能な項目集合推薦の最適化問題を以下のように定式化することができる。
Given a pivot item 𝑞, 𝑚 candidate items {𝑝1, . . .
ピボット項目↪Ll45↩、候補項目ᑝ、 ....
, 𝑝𝑚}
, ᑝᑚ}が与えられる。
⊆ P and 𝑛 attributes {𝑎1, . . .
⊆ P と 𝑛 属性 {ᵄ, ... .
, 𝑎𝑛}
, 𝑎𝑛}である。
⊆ A, we aim to find an assignment 𝑋 ∈ {0, 1} 𝑚×𝑛 that maximizes the overall utilities subject to some constraints:
⊆ A、いくつかの制約条件下で全体の効用を最大化する割り当て𝑋 ∈ {0, 1} 𝑚×𝑛 を見つけることを目的とする。

$$
\tag{1}
$$

where 𝑋𝑖𝑗 = 1 means the item 𝑝𝑖 is assigned to the explainable group 𝐺𝑎𝑗 with attribute 𝑎𝑗 , and otherwise 𝑋𝑖𝑗 = 0.
ここで、𝑋𝑖𝑗 = 1はアイテム𝑝が属性𝐺で説明可能なグループ𝑗に割り当てられることを意味し、それ以外は𝑋_1D44E = 0である。
The group capacity constraint restricts the max number of items assigned in each group with an upperbound 𝐷grp ∈ N, while the item diversity constraint limits the occurrence of each item in overall recommendations with upperbound 𝐷div ∈ N. The problem defined in Eq. 1 can be deemed as the weighted bipartite b-matching problem [22], which can be solved by modern LP solvers.
グループ容量制約は、各グループに割り当てられるアイテムの最大数を上限↪L_1D437↩grp∈Nで制限し、アイテム多様性制約は、全体の推薦における各アイテムの出現を上限↪L_1D437↩div∈Nで制限する。式1で定義した問題は、重み付き二部式bマッチング問題 [22] とみなすことができ、最新のLPソルバによって解くことができる。
Once the 𝑛 sets of item assignments are derived from 𝑋, we can easily select top-𝐾 groups with any heuristic method based on group-level utility, e.g., the average of all item-attribute utilities in the group.
𝑋からアイテム割り当ての𝑛セットが導出されると、グループレベルの効用、例えば、グループ内の全てのアイテム-属性の効用の平均値に基づいて、任意のヒューリスティック手法でトップ-1D43グループを容易に選択することができる。

However, there are two major issues with this method.
しかし、この方法には2つの大きな問題がある。
First, the optimization in Eq. 1 cannot be efficiently solved when 𝑚 is very large and let alone take all items in P as input.
第一に、式 1 の最適化は、↪Ll_145A が非常に大きく、ましてや P の全項目を入力とする場合には、効率的に解くことができない。
Second, the utility 𝑢(𝑞, 𝑝, 𝑎) is not directly available from distant user behavior signal (e.g. view-then-purchase) because users will not explicitly express which attributes are important to them to compare the items.
第二に、ユーザーはアイテムを比較するためにどの属性が重要かを明示的に表現しないため、効用𝑢(ᵅ, 𝑎)は遠くのユーザー行動信号（例：閲覧-購入）から直接利用することはできない。
Meanwhile, attribute frequency is also not a good indicator for 𝑢(𝑞, 𝑝, 𝑎) due to the common data issue of large amount of missing attribute values.
一方、属性頻度も、属性値の欠損が多いという一般的なデータの問題から、𝑢(ᵅ, ᵄ)の良い指標とはならない。

To this end, we propose a learning based multi-step framework called Extract-Expect-Explain (EX3 ).
このため、我々はExtract-Expect-Explain (EX3 ) と呼ばれる学習ベースの多段階フレームワークを提案する。
As illustrated in Fig. 1, the first Extract step aims to reduce the search space of candidate items by learning item embeddings with distant supervision and approximating coarse-grained item similarity.
図1に示すように、最初のExtractステップは、遠隔監視によるアイテム埋め込み学習と粗視化アイテム類似度の近似により、候補アイテムの探索空間を縮小することを目的とする。
Next, the Expect step aims to estimate the utility function 𝑢(𝑞, 𝑝, 𝑎) by decomposing it into two parts: fine-grained item relevance and attribute importance.
次に、Expectステップは効用関数𝑢(↪Ll_1D45E, 𝑎)を細粒度のアイテム関連度と属性重要度の2つに分解して推定することを目的としている。
The last Explain step leverages the outputs from two previous steps to solve the optimization problem and derive the 𝐾 explainable groups for item set recommendations.
最後の説明ステップは、前の2つのステップの出力を活用して最適化問題を解き、アイテムセット推薦のための ᵃ 説明可能なグループを導き出すものである。

## Extract-Step 抽出ステップ

In this step, we aim to learn an item encoder 𝜙 : P ↦→ R 𝑑𝑝 that maps each item in P to 𝑑𝑝 -dimensional space such that the items with relationships in B are closer in the latent space.
このステップでは、P の各アイテムを ᑑ -次元空間に写像するアイテムエンコーダ 𝜙 : P ⇑→ R ᑝ を学習し、B の関係を持つアイテムが潜在空間においてより近くなるようにすることを目的とする。
The latent item vectors generated by 𝜙 can be subsequently used as pretrained item embeddings in downstream steps and extracting coarse-grained similar candidates with respect to pivot items.
↪Ll_1D719 によって生成された潜在的な項目ベクトルは、その後、下流のステップで事前学習された項目埋め込みとして使用でき、ピボット項目に関して粗視化された類似候補を抽出することが可能である。

Specifically, each item 𝑝 ∈ P is initialized with either a one-hot vector or a raw feature vector extracted from metadata such as item title and category. Then, it is fed to the item encoder 𝜙, which is modeled as a multilayer perceptron (MLP) with non-linear activation function. In order to capture relatedness among items, we assume that each item is similar to its related items in B and is distinguishable from other unrelated items. As illustrated in Fig. 1(a), let 𝑁𝑝 = {𝑝𝑖
(𝑝, 𝑝𝑖) ∈ B} be the related items for an item 𝑝 ∈ P. We define a metric function 𝑓 (𝑝, 𝑁𝑝 ) to measure the distance between the item and its related items:

$$
\tag{2}
$$

where 𝜆 is the base distance to distinguish 𝑝 and 𝑁𝑝 , and ℎ(·) denotes an aggregation function over item set 𝑁𝑝 , which encodes 𝑁𝑝 into the same 𝑑𝑝 -dimensional space as 𝜙 (𝑝).
ここで、↪Ll_1D706 は ↪Ll_1D45D と区別するための基底距離、𝑁(-) はアイテム集合𝑝 上の集約関数で、𝑝と同じᵁ -D445D 空間に ᵁ を包含する。
In this work, we define ℎ(·) to be a weighted sum over item embeddings via dot-product attention:
本研究では、ℎ(-) を点積注目による項目埋め込みに対する加重和と定義する。

$$
\tag{3}
$$

We assign a positive label 𝑦 + = 1 for each pair of (𝑝, 𝑁𝑝 ). For non-trivial learning to distinguish item relatedness, for each item 𝑝, we also randomly sample
𝑁𝑝

$$
\tag{4}
$$

where 𝜖 is the margin distance.
ここで、𝜖はマージン距離である。

Once the item encoder 𝜙 is trained, for each pivot item 𝑞 ∈ P, we can retrieve a set of 𝑚 (
𝑁𝑝

##  Expect-Step エクスペクトステップ

The goal of this step is to learn the utility function 𝑢(𝑞, 𝑝, 𝑎) to estimate how likely a candidate item 𝑝 will be clicked or purchased by users after being compared with pivot item 𝑞 on attribute 𝑎.
このステップの目的は、属性 ᵄでピボット・アイテム ᵄと比較された後、候補アイテム ᵆ(ᵅ, ᵅ)がユーザーにクリックまたは購入される確率を推定するための効用関数 𝑢 を学ぶことである。
For simplicity of modeling, we assume that the utility function can be decomposed into two parts:
モデルを簡単にするために、効用関数は2つの部分に分解できると仮定する。

$$
\tag{5}
$$

where 𝑔 : [0, 1] × [0, 1] ↦→ [0, 1] is a binary operation. The first term 𝑢rel(𝑞, 𝑝) reveals the fine-grained item relevance, or equivalently, the likelihood of item 𝑝 being clicked by users after compared with pivot 𝑞 (no matter which attributes are considered). The second term 𝑢att(𝑎
𝑞, 𝑝) indicates the importance of displaying attribute 𝑎 to users when they compare items 𝑞 and 𝑝. It is natural to learn these two functions if well-curated datasets are available. However, practically, even though the item relevance can be simulated from distant user behavior signals, e.g., Bpv view-then-purchased, the groundtruth of important attributes still remain unknown. This is because users will not explicitly express the usefulness of item attributes when they do online shopping, which leads to the challenge of how to infer the attribute importance without supervision. In addition, the data issue of missing attributes and noisy values is quite common since it costs much time and effort to manually align all the attributes of items. That is to say each item may contain arbitrary number of attributes and their values may contain arbitrary content and data types.

To overcome the issues, we propose a novel neural model named Attribute Differentiating Network (ADN) to jointly approximate 𝑢rel and 𝑢att.
この問題を克服するために、我々は𝑢と𝑢を共同で近似する属性微分ネットワーク（ADN）と名付けた新しいニューラルモデルを提案する。
Formally, it takes as input a pivot item𝑞 and a candidate item 𝑝 along with the corresponding attribute-value pairs 𝐴𝑞, 𝐴𝑝 (e.g., 𝐴𝑞 = {(𝑎1, 𝑣(𝑞, 𝑎1)), . . .
形式的には、ピボットアイテムŅと候補アイテムŅを、対応する属性値ペアŅ（例えば、𝐴, ᑝ）、｛（ᑑ,𝑎）, ....
, (𝑎𝑛, 𝑣(𝑞, 𝑎𝑛))}), and simultaneously outputs an item relevance score 𝑌ˆ 𝑝 ∈ [0, 1] and attribute importance scores 𝑦ˆ𝑝,𝑗 ∈ [0, 1] for attribute 𝑎𝑗 (𝑗 = 1, . . . , 𝑛).
, (𝑎, 𝑞)}) と、属性 ᵄ(ᵄˆ 𝑝)に対する項目関連性スコア𝑌∈ [0, 1] と属性重要度スコア𝑗∈ [0, 1] を同時出力する（Ņ＝1, ...,𝑛）。

### Network Overview. ネットワーク概要

As illustrated in Fig. 2, ADN consists of three components: a value-difference module to capture the difference levels of attribute values of two items, an attention-based attribute scorer to implicitly predict the attribute contribution, and a relevance predictor that estimates the fine-grained relevance of two items.
図2に示すように、ADNは2つの項目の属性値の差分レベルを捉える価値差分モジュール、属性寄与度を暗黙的に予測する注目ベース属性スコアラ、2つの項目のきめ細かい関連性を推定する関連性予測器の3つのコンポーネントから構成されています。
Specifically, two input items are first respectively vectorized by the encoder 𝜙 from the Extract step.
具体的には、まず2つの入力項目はExtractステップで得られたエンコーダᵱによってそれぞれベクトル化される。
The derived item embeddings are then mapped into low-dimensional space via linear transformation, i.e. x𝑞𝑝 = 𝑊𝑝 [𝜙 (𝑞);𝜙 (𝑝)], where [;] denotes the concatenation and 𝑊𝑝 is the learnable parameters.
すなわち、xŅ = ↪L_145D↩ [Ņ (↪L_1D44A↩);ᑝ] であり、[;]は連結を、↪L_145D↩は学習可能なパラメータを表す。
Then, each attribute-value tuple (𝑎𝑗 , 𝑣(𝑞, 𝑎𝑗), 𝑣(𝑝, 𝑎𝑗)) is encoded by the value-difference module into a vector denoted by x𝑣𝑗 .
次に、各属性-値タプル(ᵄ 𝑗, 𝑣, 𝑗)は、値差モジュールによってx𝑣𝑗と表されるベクトルにエンコードされる。
All these vectors x𝑣1 , . . .
これらのベクトル x𝑣1 , ... ...
, x𝑣𝑛 together with x𝑞𝑝 will be further fed to the attention-based attribute scorer to produce attribute importance scores 𝑦ˆ𝑝,1, . . .
x𝑣、x𝑝はさらに注意ベースの属性スコアラーに供給され、属性重要度スコア𝑦ˆ𝑝, ... ...が生成される。
,𝑦ˆ𝑝,𝑛 as well as an aggregated vector z𝑣 about value-difference information on all attributes.
𝑦ˆᵅと、すべての属性の価値差情報に関する集約ベクトルz𝑣が生成される。
The relevance predictor finally yields 𝑌ˆ 𝑝 based on the joint of x𝑞𝑝 and z𝑣 .
関連性予測器は最終的に、xŅとzᑣの結合に基づいて、Ņを生成する。

### Value-Difference Module. Value-Difference Moduleの略。

As shown in Fig. 2(b), we represent each attribute 𝑎𝑗 as a one-hot vector and then embed it into 𝑑𝑎-dimensional space via linear transformation, i.e., a𝑗 = 𝑊𝑎𝑎𝑗 , with learnable parameters 𝑊𝑎.
図 2(b)に示すように、各属性ᵄをワンホットベクトルとして表現し、線形変換、すなわち、a𝑑 = ↪L_1D44E↩、学習可能パラメータᵄを用いて𝑎次元空間へ埋め込む。
Since the value 𝑣(𝑝, 𝑎𝑗) of item 𝑝 and attribute 𝑎𝑗 can be of arbitrary type, inspired by character-level CNN, we treat it as a sequence of characters and each character is embedded into a 𝑑𝑐 -dimensional vector via linear transformation with parameters 𝑊𝑐 .
項目 ᵅ と属性 ᵄ の値 𝑣 は任意の型が可能なので、文字レベルCNNにヒントを得て、これを文字列として扱い、各文字をパラメータ ᵄ の線形変換により𝑐次元ベクトルに埋め込むことにした。
Suppose the length of character sequence is at most 𝑛𝑐 .
文字列の長さが最大でも𝑛𝑐であるとする。
We can represent the value 𝑣(𝑝, 𝑎𝑗) as a matrix v𝑝 𝑗 ∈ R 𝑛𝑐×𝑑𝑐 .
値 𝑣(𝑝, 𝑗)は行列 v𝑝∈ R 𝑛𝑐×𝑑として表すことができる．
Then, we adopt convolutional layers to encode the character sequence as follows:
そして、文字列の符号化に畳み込み層を採用し、以下のようにする。

$$
\tag{6}
$$

where conv(·) denotes the 1D convolution layer and maxpool(·) is the 1D max pooling layer.
ここでconv(-)は1次元畳み込み層、maxpool(-)は1次元最大プーリング層であることを示す。
The output x𝑖𝑗 ∈ R 𝑑𝑐 is the latent representation of arbitrary value 𝑣𝑖𝑗 .
出力 x𝑖ᑗ∈ R ᑑ は任意の値ᑣ𝑖ᑗの潜在的表現である。
To capture value difference on attribute 𝑎𝑗 between items 𝑞, 𝑝, we further encode the attribute vector a𝑗 and the value vectors x𝑞𝑗 and x𝑝 𝑗 via an MLP:
項目 ᑎ, Ņ 間の属性 ↪Ll_1457 の価値差を捉えるために、さらに属性ベクトル a↪Ll_1457 と価値ベクトル xᑞ, xŅ をMLPで符号化したものである。

$$
\tag{7}
$$

where x𝑣𝑗 is supposed to encode the value-difference information between values 𝑣(𝑞, 𝑎𝑗) and 𝑣(𝑝, 𝑎𝑗) on attribute 𝑎𝑗 .
ここで、xᑣは属性ᑗの値ᑣ(ᵅ, 𝑓)と𝑎ᑗの値差情報をコード化するものとされる。

### Attention-based Attribute Scorer. アテンションベースのアトリビュートスコアラー。

Since our goal is to detect important attributes with respect to the pair of items, we further entangle each value-difference vector x𝑣𝑗 of attribute 𝑎𝑗 conditioned on item vector x𝑞𝑝 as follows:
我々の目的は項目のペアに関して重要な属性を検出することなので、項目ベクトルxᑞを条件とする属性ᑗの各値差ベクトルxᑓをさらに以下のように絡める。

$$
\tag{8}
$$

where another MLP𝑝 is employed to generate the item-conditioned value-difference vector w𝑝 𝑗 .
ここで，別のMLPᵅが項目条件付き価値差ベクトルw𝑗を生成するために採用される．

Natually, we can use attention mechanism to aggregate 𝑛 item-conditioned attribute vectors w𝑝1, . . .
通常、注目メカニズムを用いて、𝑛個の項目条件付き属性ベクトルwl_1D, ... ...を集約することができる。
, w𝑝𝑛 for better representation and automatic detection of important attributes.
, wl_145D↩𝑛をより良い表現と重要な属性の自動検出のために使用することができる。
However, directly applying existing attention mechanism here will encounter several issues.
しかし、ここで既存の注目メカニズムを直接適用すると、いくつかの問題が発生する。
First, the learned attention weights may have bias on frequent attributes.
まず、学習された注意の重みは頻度の高い属性に偏りがある可能性がある。
That is higher weights may not necessarily indicate attribute importance, but only because they are easily to acquire and hence occur frequently in datasets.
つまり、高い重みは必ずしも属性の重要性を示しているわけではなく、取得が容易であるためデータセットに頻繁に現れるというだけの理由である可能性がある。
Second, attribute cardinality varies from items to items due to the issue of missing attribute values, so model performance is not supposed to only rely on a single attribute, i.e. distributing large weight on one attribute.
第二に、属性値の欠落の問題から、属性のカーディナリティは項目ごとに異なるため、モデルの性能は一つの属性にのみ依存する、つまり、一つの属性に大きな重みを割り当てることは想定されない。
To this end, we propose the Random-masking Attention Block (RAB) to alleviate the issues.
そこで、この問題を緩和するために、Random-masking Attention Block (RAB)を提案する。
Specifically, given item vector x𝑞𝑝 and 𝑛 item-conditioned value-difference vectors w𝑝1, . . .
具体的には、項目ベクトルxᑞと𝑛個の項目条件付き値差ベクトルwᑝ1, ... ...が与えられたとき、RABは項目条件付き値差ベクトルwᑝ1, ... ...に重みを与える。
, w𝑝𝑛, the RAB block is defined as follows.
, wl_1D45𝑛 が与えられた場合、RAB ブロックは以下のように定義される。

$$
\tag{9}
$$

$$
\tag{10}
$$

$$
\tag{11}
$$

where 𝜂𝑗 is a random mask that has value 𝛾 with probability 𝑓 𝑟𝑒𝑞𝑗 (frequency of attribute 𝑎𝑗 ) in training and value 1 otherwise. It is used to alleviate the influence by imbalanced attribute frequencies. 𝜏𝑗 is known as the temperature in softmax and is set as (1 + 𝑓 𝑟𝑒𝑞𝑗) by default, which is used to shrink the attention on the attribute assigned with large weight. The RAB block can be regarded as a variant of the scaled dot-product attention by incorporating randomness of attribute frequencies and item-conditioned information. The attention weights {𝑦ˆ𝑝,𝑗 }𝑗 ∈ [𝑛] are used to approximate attribute importance 𝑢att(𝑎𝑗
𝑞, 𝑝). The output z𝑣 encodes the aggregated information contributed by all attributes.

### Relevance Predictor. 関連性予測装置。

We adopt a linear classifier model to predict the relevance of two items based on the item vector as well as encoded attribute-value vector:
項目ベクトルと符号化された属性値ベクトルをもとに、2つの項目の関連性を予測する線形分類器モデルを採用した。

$$
\tag{12}
$$

We treat the problem as a binary classification with the objective function defined as follows:
この問題を、目的関数を以下のように定義した2値分類として扱う。

$$
\tag{13}
$$

Note that pairwise ranking loss can also easily be extended here and the choice of a better ranking loss function is beyond the scope of this paper.
なお、ここではペアワイズランキングロスも簡単に拡張でき、より良いランキングロス関数の選択は本論文の範囲外である。

Once the model is trained, we can obtain the relevance score 𝑢rel(𝑞, 𝑝) ≈ 𝑌ˆ 𝑝 that implies whether candidate item 𝑝 is relevant to query item 𝑞, and the attribute importance score 𝑢att(𝑎𝑗
𝑞, 𝑝) ≈ 𝑦ˆ𝑝,𝑗 (𝑗 = 1, . . . , 𝑛) indicating how important each attribute 𝑎𝑗 is to users when they compare items 𝑞 and 𝑝. We adopt a simple binary operation 𝑔(𝑢rel(𝑞, 𝑝), 𝑢att(𝑎𝑗

## Explain-Step Explain-Step

In this step, the goal is to present 𝐾 explainable groups 𝐺𝑎(1) , . . .
このステップでは、全体の効用を最大化するような説明可能なグループ ᵃ(1) , ... .
,𝐺𝑎(𝐾) such that the whole utility is maximized.
ᵃ(ᵃ)は全体の効用を最大化するようなものである。
The complete inference algorithm is described in Alg.
完全な推論アルゴリズムはAlg.1に記述されている。
1.
1.
Specifically, it first extracts a small subset of similar candidate items 𝐶𝑞 with respect to the pivot item 𝑞.
具体的には、まずピボット項目↪Ll_1D45E に対して類似の候補項目𝐶の小さな部分集合を抽出する。
For each pair of 𝑞 and 𝑝𝑖 ∈ C𝑞, it computes the relevance score of two items as well as the importance scores of attributes.
Ņとᑝの各組∈CŅに対して、2つのアイテムの関連性スコアと属性の重要度スコアを計算する。
Then, the LP problem defined in Eq. 1 is solved to obtain the assignments of candidate items on attribute-based groups.
次に、式1で定義されるLP問題を解いて、属性ベースのグループへの候補アイテムの割り当てを得る。
For each group, the algorithm takes the score from the most significant item as the heuristic score for group-level ranking.
各グループに対して、アルゴリズムは最も重要な項目のスコアをグループレベルのランキングのためのヒューリスティックスコアとして用いる。
Finally, the top 𝐾 groups are generated as the recommendation with attribute-based explanations.
最後に、上位 оグループが属性に基づく説明付きの推薦文として生成される。
Note that we adopt template-based generation approach to generate the natural language explanation based on attributes, which is not the focus in this paper.
なお、属性に基づく自然言語説明の生成にはテンプレートベースの生成アプローチを採用しているが、これは本論文の焦点ではない。

## Implementation Detail 実施内容

In the Extract-step, the raw features of each item consist in n-gram features extracted from items’ titles, key words and categories.
抽出ステップでは、各アイテムの生の特徴は、アイテムのタイトル、キーワード、カテゴリから抽出されたn-gram特徴で構成される。
The feature extractor 𝜙 consists of 3 fully-connected layers of sizes 1024, 1024, 128 with ReLU [24] as nonlinear activation function.
特徴抽出器 𝜙 はサイズ 1024, 1024, 128 の 3 つの完全連結層からなり、非線形活性化関数として ReLU [24] を用いている。
Margin parameters 𝜆 = 1.0 and 𝜖 = 1.0.
マージンパラメータはᜆ = 1.0 と 𝜖 = 1.0である。
The model is trained with Adam optimizer with learning rate 0.001 and batch size 128.
このモデルは、学習率0.001、バッチサイズ128のAdam optimizerで学習される。

In the Expect-step, the network parameters are as follows. 𝑊𝑝 ∈ R 256×64 , 𝑊𝑎 ∈ R
A

In the Explain-step, we set both 𝐷grp and 𝐷att to be 5 by default. Candidate set size
𝐶𝑞

# Experiments 実験

In this section, we comprehensively evaluate the performance of the proposed method EX3 in terms of both recommendation and attribute ranking on a real-world benchmark.
本節では、提案手法EX3の推薦性能と属性ランク付け性能を実世界のベンチマークで総合的に評価する。

## Experimental Setup Experimental Setup

### Dataset. データセット

We take experiments on a real-world industrial dataset collected from Amazon.com including 7 subcategories:
Amazon.comから収集した、7つのサブカテゴリを含む実世界の産業用データセットで実験を行う。
Battery, Coffee, Incontinence Protector, Laundry Detergent, Shampoo, Toilet Paper and Vitamin.
電池、コーヒー、失禁防止剤、洗濯洗剤、シャンプー、トイレットペーパー、ビタミンである。
Following distant supervision manner mentioned in Section 2, each subset can be regarded as an individual benchmark.
セクション2で述べた遠隔監視の方法に従い、各サブセットは個々のベンチマークとみなすことができる。
To enable fast experiments, we randomly sample products from each product category and select their corresponding attributes to construct the datasets.
高速な実験を可能にするため、各製品カテゴリから製品をランダムに抽出し、対応する属性を選択してデータセットを構築する。
The statistics of these datasets are summarized in Table 1.
これらのデータセットの統計量は表1にまとめられている。
Similar metadata can also be found in [20, 21].
同様のメタデータは[20, 21]にも記載されている。
Due to the large-scale product pool, we generate candidate products for each query product via the proposed Extract-Step, which leads to around 30 similar candidate products per query.
大規模な商品プールのため、提案するExtract-Stepにより各クエリ商品に対して候補商品を生成し、1クエリあたり約30の類似候補商品を生成する。
Our model and all the baselines are trained and evaluated based on the extracted candidates.
我々のモデルと全てのベースラインは、抽出された候補に基づいて学習・評価される。
We randomly split the dataset into training set (80%), validation set (10%) and test set (10%).
データセットを学習セット(80%)、検証セット(10%)、テストセット(10%)にランダムに分割し、学習と評価を行う。

### Baselines & Metrics. ベースライン＆メトリックス

We compare our method with following baselines.
本手法を以下のベースラインと比較する。

- Relevance is the method that computes item similarity based on item embeddings learned in Extract step. 関連性とは、Extractステップで学習した項目埋め込みを元に、項目の類似性を計算する方法である。

- BPR [26] is the Bayesian personalized ranking method for making recommendations, which is modified to item-to-item prediction in this work. BPR [26]は、推薦を行うためのベイズ型パーソナライズドランキング手法であり、本研究では項目間予測に修正したものである。

- ACCM [27] is a CF-based and CB-based recommendation approach that leverages attribute to enrich the representation of items. We adapt this method to our item-to-item recommendation. ACCM [27]は、CFベースおよびCBベースの推薦手法であり、項目の表現を豊かにするために属性を利用するものである。 我々はこの手法をアイテム間推薦に適用する。

- A2CF [3] is the state-of-the-art attribute-based recommendation model that outputs substitutes for pivot items. A2CF [3]は、ピボットアイテムの代替品を出力する、最先端の属性ベース推薦モデルである。

- EX3 is our approach proposed in Expect step. EX3は、Expect stepで提案したアプローチです。

For fair comparison, we generate the a candidate set of 30 items for each pivot from the Extract step.
比較のため、Extract の段階で各ピボットに対応する 30 個のアイテムからなる候補セットを生成する。
All the baselines are evaluated based on the candidate set and also leverage the pretrained item embeddings as input if necessary.
ベースラインはすべてこの候補セットに基づいて評価され、必要に応じて事前に学習されたアイテム埋め込みも入力として利用される。

We adopt NDCG@10, Recall@10, Precision@10 as the metrics to evaluate the top-N recommendation performance.
TOP-Nの推薦性能を評価する指標として、NDCG@10、Recall@10、Precision@10を採用した。

## Top-N Recommendation Performance (Expect-Step) トップNレコメンデーション性能(Expect-Step)

In this experiment, we first evaluate the recommendation performance output by the Expect step, which produces the same results as traditional recommendations.
本実験では、まずExpectステップで出力される推薦性能を評価する。Expectステップでは、従来の推薦と同じ結果が得られる。
Specifically, given a pivot item, both our method and all other baselines outputs top 10 recommendations from 30 candidates generated by Extract step.
具体的には、ピボットアイテムが与えられた場合、本手法と他のベースラインは共にExtractステップで生成された30個の候補の中から上位10個の推薦を出力する。
The goal of this experiment is to verify if our model can output more relevant items than others.
この実験の目的は、我々のモデルが他のモデルよりも関連性の高いアイテムを出力できるかどうかを検証することである。

The results are reported in Table 2.
その結果を表 2 に示す。
We observe that our model EX3 consistently outperforms all baselines across all datasets on all metrics.
我々のモデルEX3は、全てのデータセットにおいて、全ての指標で一貫してベースラインより優れていることが分かる。
For instance, our model achieves NDCG of 0.8177, Recall of 0.9667 and Precision of 0.1953, which are higher than the results produced by the best baseline A2CF by a large margin.
例えば、我々のモデルはNDCG 0.8177、Recall 0.9667、Precision 0.1953を達成し、最良のベースラインA2CFの結果よりも大きな差をつけて高い値を示している。
It is interesting to see that our model shows significant improvements on the item ranking performance, resulting at least 11.35% improvement in NDCG in Overall dataset and 10.36%–56.06% improvements across 7 subdomains.
興味深いことに、我々のモデルはアイテムランキングの性能に著しい改善を示し、Overall datasetでは少なくとも11.35%のNDCGの改善、7つのサブドメインでは10.36%-56.06%の改善を示しています。
In addition, we notice that for datasets Coffee and Incontinence Protector, the recommendation performance of all models are better than the overall (average) performance.
また，データセットCoffeeとIncontinence Protectorでは，すべてのモデルの推薦性能が全体（平均）性能よりも優れていることが分かる．
For example, our model achieves NDCG of 0.8716 and 0.8660 respectively, which are higher than Overall NDCG of 0.8177.
例えば、我々のモデルはそれぞれ0.8716と0.8660のNDCGを達成し、全体のNDCGである0.8177より高い値を示しています。
Other models share similar trends.
他のモデルも同様の傾向を示している。
This indicates that the cases in these two datasets are easier to learn to capture user behavior.
これは、この2つのデータセットのケースは、ユーザーの行動を捉えるための学習が容易であることを示しています。

##  Model Robustness to Missing Attributes 属性欠落に対するモデルの頑健性

We further show our model is robust to missing attributes in inference data with the proposed masking attention.
さらに、提案するマスキングアテンションを用いて、我々のモデルが推論データにおける属性の欠落に対してロバストであることを示す。
Specifically, we randomly drop 10%, 20%, 30%, 40% and 50% attributes in the test set and evaluate the top-N recommendation performance of our model with and without the proposed attention mechanism.
具体的には、テストセット中の10%、20%、30%、40%、50%の属性をランダムに削除し、提案する注目機構を用いた場合と用いない場合の我々のモデルのトップN推薦性能を評価する。
All other settings remain the same.
他の設定は全て同じである。
As shown in Fig. 3, our model w
図3に示すように、我々のモデルw

## Attribute Ranking Performance (Explain-Step) 属性ランキング性能（Explain-Step）

### Effectiveness of Attribute Ranking. 属性ランキングの効果

In this experiment, we evaluate the performance of the proposed Explain-Step in identifying important attributes.
本実験では、提案するExplain-Stepが重要な属性を特定する際の性能を評価する。
We specifically consider following three baselines.
具体的には、以下の3つのベースラインを検討する。

- Random is a simple grouping algorithm by randomly assigning items into attribute-based groups as long as the corresponding value exists. Then the groups are ordered in the way same as Alg. 1 (line 13–14). ランダムは、対応する値が存在する限り、属性に基づいたグループにランダムに項目を割り当てることで、単純なグループ化を行うアルゴリズムである。 そして、各グループはAlg.1と同じ方法で順序付けされる。 1と同じ方法で順序付けされる（13-14行目）。

- Greedy is an iterative algorithm by always picking the pair of item and attribute with larger utility value 貪欲とは、常に効用値の大きい項目と属性の組を選ぶ反復アルゴリズムである

- EX3 is our proposed method of the Explain-Step. EX3は、私たちが提案するExplain-Stepの方法です。

Note that all compared methods differ in the grouping ways but take the same utility function as input, which is generated by the Expect-step for fair comparison.
なお、比較した手法はすべてグループ化の方法が異なるが、公正な比較のためにExpectステップで生成された同じ効用関数を入力としている。
To quantify the attribute ranking performance, we randomly sample around 1000 cases and ask human evaluators to manually score each attribute in a 5-point scale given a pivot item and a set of candidate items.
属性ランキングの性能を定量化するために、約1000ケースをランダムにサンプリングし、人間の評価者に、ピボット項目と候補項目のセットを与えて各属性を5点満点で手動で採点してもらう。
Then we can calculate the average and the normalized score of the predicted important attributes by each model.
そして、各モデルによって予測された重要な属性の平均値と正規化されたスコアを計算することができる。
The results are reported in Table 3.
その結果を表3に報告する。

We observe that our method EX3 gives the better performance in important attribute ranking compared with two baselines.
その結果、我々の手法EX3は、2つのベースラインと比較して、重要属性ランキングでより良い性能を示すことがわかった。
One interesting fact is that the Greedy algorithm is actually an approximation algorithm for the optimization problem Eq. 1, which interprets that its performance is slightly worse than ours.
興味深いことに、Greedyアルゴリズムは式1の最適化問題の近似アルゴリズムであり、我々の手法より若干性能が悪いと解釈される。

### Adaptive attribute ranking. 適応的な属性ランキング。

In addition, we show that for the same pivot item, our model will rank attributes differently if the candidates are different.
また、同じピボット項目であっても、候補が異なれば属性のランク付けも異なることを示す。
We showcase an example in Table 4 to demonstrate this characteristics of our model.
このモデルの特徴を示すために、表 4 に例を示す。
Given a shampoo product with ID “B000YG1INI” as pivot item 3 , whose attributes are listed in the second column, we feed two sets of candidate items to our model that is able to generate two different attribute rankings as shown in the upper and lower parts of the table.
IDが "B000YG1INI "のシャンプー商品をピボットアイテム3とし、その属性を2列目に記載した場合、2セットの候補アイテムを我々のモデルに供給すると、表の上下に示すように、2種類の属性ランキングを生成することができる。
It is interesting to see that the model is able to rank attributes based on value differences and diversity.
興味深いのは、このモデルが価値の差と多様性に基づいて属性をランク付けすることができることである。
Take “brand” attribute as example.
例えば、「ブランド」属性を例にとります。
In the first case (upper table), “brand” is ranked in the second place and considered as a relatively important attributes when users compare different shampoo products.
最初のケース（上表）では、「ブランド」は2位にランクされており、ユーザーが様々なシャンプー製品を比較する際に比較的重要な属性であると考えられている。
In contrast, in the second case (lower table), “brand” is ranked lower because all the candidates have the same brand “Desert Essence” and it is less informative for users to enhance their shopping experience.
一方、2番目のケース（下表）では、すべての候補が同じブランド「Desert Essence」を持っており、ユーザーにとってショッピング体験を高めるための情報量が少ないため、「ブランド」の順位は低くなっています。

## Ablation Study アブレーション研究

We first show the recommendation performance under different masking ratios (𝜂) in the proposed attention mechanism.
まず、提案する注意メカニズムにおいて、異なるマスキング比率(ᴥ)の下での推薦性能を示す。
Specifically, we adopt different values of 𝜂 to train the model of Expect step, e.g. 𝜂 = 0, 0.1, . . .
具体的には、Expectステップのモデルを学習するために、異なる値のᜂを採用する、例えば、ᜂ = 0, 0.1, . .
, 0.9, 1.0.
, 0.9, 1.0.
Note that 𝜂 = 0 means the attribute is completely dropped while 𝜂 = 1 means there is no attribute dropping.
ᜂ = 0は属性が完全に削除されることを意味し、ᜂ = 1は属性が削除されないことを意味することに注意されたい。
We report the top-N recommendation performance under various 𝜂’s in Fig. 4 (a, b).
図 4 (a, b) は、様々な ᜂ の下でトップ N の推薦性能を報告したものである。
We observe that the masking ratios influence on ranking performance (NDCG) and the model achieves the best performance when 𝜂 = 0.3.
マスキング比率はランキング性能（NDCG）に影響を与え、モデルは𝜂=0.3のときに最良の性能を達成することがわかる。
For precision, we find that the performance does not vary a lot, but still show similar trends as the NDCG, i.e. 𝜂 = 0.4 leads to the relatively better performance.
精度に関しては、性能はあまり変化しないが、NDCGと同様の傾向を示し、すなわち、ᜂ = 0.4が比較的良い性能につながることが分かる。

Next, we evaluate the influence of different values of temperatures (𝜏) in the attention mechanism.
次に、注意メカニズムにおける温度（）の値の違いの影響を評価する。
Specifically, we experiment with two ways of imposing temperatures over softmax function.
具体的には、ソフトマックス関数に温度を課す2つの方法を実験する。
The first one relies on the predefined attribute frequencies, i.e. 𝜏 = (1 + 𝑓 𝑟𝑒𝑞𝑖) 𝑛 with 𝑛 = 1, 2.
1つ目は事前に定義された属性頻度、すなわち𝜏 = (1 + 𝑓) 𝑛で𝑟 = 1, 2に依存するものである。
The other one uses the fixed value of 𝜏 = 1, 1.5, 2, 10.
もう1つは固定値𝜏 = 1, 1.5, 2, 10を用いるものである。
All other training settings remain the same.
他の学習設定は全て同じである。
The results of top N recommendation are reported in Fig. 4 (c, d).
トップN推薦の結果を図4 (c, d)に報告する。
We can see that the default choice of 𝜏 = 1 + 𝑓 𝑟𝑒𝑞𝑖 leads to the best performance in both NDCG and precision.
𝜏 = 1 + 𝑓 𝑒𝑞𝑖のデフォルトの選択はNDCGと精度の両方で最高のパフォーマンスをもたらすことが分かる。
Besides, note that when 𝜏 = 1, it is equivalent to the original softmax function.
その上、↪Ll_1F = 1の時、元のソフトマックス関数と等価であることに注意。
Our model with the default 𝜏 shows superior performance over such setup, which indicates the effectiveness of the proposed attention mechanism.
デフォルトのを用いた我々のモデルは、このような設定よりも優れた性能を示し、提案する注意メカニズムの有効性を示している。

## Online Simulation and Experiments 

In this experiment, we evaluate the overall performance of the group-form explainable item set recommendation.
本実験では、グループ形式の説明可能な項目セット推薦の総合的な性能を評価する。
Before serving the proposed method to real users, we generate a batch of explainable item set recommendations in an offline mode and leverage human annotators to help us evaluate the recommendation quality.
提案手法を実際のユーザに提供する前に、オフラインモードで説明可能なアイテムセット推薦のバッチを生成し、人間のアノテーターに推薦品質の評価を依頼する。
For each of 7 product categories, we sample top 50 most popular pivot products from our recommendation dataset and ask the annotators to evaluate whether the attribute-based explainable recommendations can help users make better purchase decision.
7つの商品カテゴリごとに、推薦データセットから上位50の人気商品を抽出し、属性に基づく説明可能な推薦がユーザのより良い購買意思決定に役立つかどうかをアノテーターに評価してもらっている。
Note that the evaluation metric contains two-fold interactive measurement on both product relevance and attribute importance, as the ranked important attribute list should depend on what products are recommended to users.
この評価指標は、商品の関連性と属性の重要性の2重の評価から構成されています。
Through human evaluation, we obtain over 80% acceptance rate on high-quality item set recommendations with over 86% accuracy on comparable product recommendation performance, which is 2x higher than using raw Bpv data for recommendation.
人間による評価では、80%以上の高品質なアイテムセット推薦を得ることができ、86%以上の精度で同等の商品推薦を行うことができました。これは、推薦に生のBpvデータを使用するよりも2倍高い精度です。
We also conduct online A
また、オンラインA

# Related Work 関連作品

In this section, we discuss the related work regarding explainable recommendation and item relationship mining.
本節では、説明可能な推薦と項目関係マイニングに関する関連研究について述べる。

## Explainable Recommendation. Explainable Recommendation (説明可能な推奨事項)

In the era of e-commerce, recommender systems have been widely used to provide users with relevant item suggestions.
電子商取引の時代において，ユーザに関連する商品を提案するために，推薦システムが広く利用されている．
Most of existing methods are based on collaborative filtering [16], matrix factorization [17] and neural recommendation model [34].
既存の手法の多くは、協調フィルタリング [16]、行列分解 [17]、ニューラル推薦モデル [34] に基づいている。
Recently, to further improve user experience of recommender systems [18], great research efforts have been promoted to explainable recommendation problems [6, 7, 35].
近年，推薦システムのユーザエクスペリエンスをさらに向上させるために[18]，説明可能な推薦問題に対する大きな研究努力が進められている[6, 7, 35]．
One common way to generate explanation for recommendation is to leverage knowledge graphs [5, 15, 31, 33, 39].
推薦のための説明を生成する一般的な方法として、知識グラフを活用する方法がある[5, 15, 31, 33, 39]。
For example, Xian et al. [32] propose to leverage reinforcement learning on knowledge graph to provide behavior-based explanation for product recommendations, while Zhao et al. [37] also employs reinforcement learning but propose a different demonstration-based knowledge graph reasoning framework for explainable recommendation.
例えば、Xianら[32]は知識グラフの強化学習を利用して、商品推薦のための行動ベースの説明を提供することを提案し、Zhaoら[37]も強化学習を利用しているが、説明可能な推薦のための異なるデモベースの知識グラフ推論フレームワークを提案している。
Besides knowledge graph, sentiment
知識グラフの他に、感情

## Item Relationship Mining. アイテム関係 マイニング

As our work is around item-to-item-set recommendation, we will also discuss existing work on item relationship mining.
本論文では、項目間推薦を対象としているため、項目間関係マイニングに関する既存の研究についても言及する。
Identifying relationships among items is a fundamental component of many realworld recommender systems [20, 30].
アイテム間の関係を特定することは、多くの現実世界の推薦システムの基本要素である [20, 30]。
Linden et al. [19] designs an item-to-item collaborative filtering to generate similar item recommendation for Amazon.com.
Linden ら[19]は Amazon.com の類似品推薦を生成するためにアイテム間協調フィルタリングを設計している。
Zhang et al. [38] discuss the impact of substitute and complement relationship between items on recommendations.
Zhang ら[38]は、アイテム間の代替・補完関係が推薦に与える影響について議論している。
Similar efforts [1, 12] have been put to target at explicitly modeling relationship between items for recommendations.
また，レコメンデーションにおけるアイテム間の関係を明示的にモデル化することも，同様の取り組み[1,12]によって目標とされている．
Representative examples include Sceptre [20], which proposes a topic modeling method to infer networks of products, and PMSC [30], which incorporates path constraints in item pairwise relational modeling.
代表的な例として、商品のネットワークを推定するトピックモデリング手法を提案したSceptre [20]や、項目のペアワイズリレーショナルモデリングにパス制約を組み込んだPMSC [30]がある。
He et al. [13] design a framework to use visual features to identify compatibility relationship between clothes and jewelry.
Heら[13]は、衣服と宝飾品の互換性関係を識別するために視覚的特徴を利用するフレームワークを設計している。
These methods seek to distinguish substitutes, complements and compatibilities, but fail to provide any clear explanation on why these items are substitutable and comparable.
これらの方法は、代替品、補完品、互換品を区別しようとするものであるが、なぜこれらの品目が代替可能であり、比較可能であるのかについて明確な説明を提供することができない。

# Conclusion 結論

In this work, we study the important problem of explainable attribute-aware item-set recommendation.
本研究では、説明可能な属性を考慮した項目集合推薦という重要な問題を研究する。
We propose a multi-step learning-based framework called Extract-Expect-Explain (EX3 ) to approach the problem by first extracting coarse-grained candidate sets of items with respect to the pivot to reduce the search space of similar items (Extract-step), followed by a joint prediction of pairwise item relevance and attribute importance (Expect-step), which are subsequently fed to a constrained optimization solver to generate the group-form recommendations with explanations (Explain-step).
まず、類似項目の探索空間を縮小するために、ピボットに関する粗視化された候補項目群を抽出し（Extract-step）、次に、ペアワイズ項目関連性と属性重要度の共同予測（Expect-step）を行い、その後、説明付きグループ形式推薦を生成する（Explain-step）制約付き最適解法に供給して問題にアプローチする、EX3 （Exract-Expect-Explain) と呼ぶマルチステップ学習ベースの枠組みを提案する。
The experiments are conducted on a real-world large-scale dataset and the results demonstrate that our proposed model achieves over 10% higher NDCG than state-of-the-art baselines in the explainable recommendation domain.
実世界の大規模データセットを用いて実験を行った結果、提案手法は説明可能な推薦領域において、最新のベースラインと比較して10%以上高いNDCGを達成することが示された。
Moreover, our proposed method can adaptively generate attribute-based explanations for various products, and the resulting explainable item-set recommendations are also shown to be effective in large-scale online experiments.
さらに、提案手法は様々な商品に対して属性に基づいた説明を適応的に生成することができ、その結果得られた説明可能なアイテムセット推薦が大規模オンライン実験においても有効であることが示された。
There are several promising areas that we consider for future work, such as leveraging the learnt important attributes for query rewriting and product categorization.
また、学習した重要な属性をクエリ書き換えや商品分類に利用するなど、今後の課題として有望な領域がいくつか考えられる。