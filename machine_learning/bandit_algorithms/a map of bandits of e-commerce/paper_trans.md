
# A Map of Bandits for E-commerce Eコマースのためのバンディットの地図  
## Yi Liu[∗]  
## Yi Liu[∗]  
#### yiam@amazon.com Amazon.com Seattle, WA, United States  
#### yiam@amazon.com Amazon.com シアトル, WA, アメリカ合衆国  
### ABSTRACT 要約  
The rich body of Bandit literature not only offers a diverse toolbox of algorithms, but also makes it hard for a practitioner to find the right solution to solve the problem at hand.  
バンディットに関する豊富な文献は、多様なアルゴリズムのツールボックスを提供するだけでなく、実務者が直面している問題を解決するための適切な解決策を見つけるのを難しくします。  
Typical textbooks on Bandits focus on designing and analyzing algorithms, and surveys on applications often present a list of individual applications.  
バンディットに関する典型的な教科書は、アルゴリズムの設計と分析に焦点を当てており、アプリケーションに関する調査はしばしば個々のアプリケーションのリストを提示します。  
While these are valuable resources, there exists a gap in mapping applications to appropriate Bandit algorithms.  
これらは貴重なリソースですが、アプリケーションを適切なバンディットアルゴリズムにマッピングするギャップが存在します。  
In this paper, we aim to reduce this gap with a structured map of Bandits to help practitioners navigate to find relevant and practical Bandit algorithms.  
本論文では、実務者が関連する実用的なバンディットアルゴリズムを見つけるための構造化されたバンディットの地図を用いて、このギャップを縮小することを目指します。  
Instead of providing a comprehensive overview, we focus on a small number of key decision points related to reward, action, and features, which often affect how Bandit algorithms are chosen in practice.  
包括的な概要を提供するのではなく、報酬、アクション、および特徴に関連する少数の重要な意思決定ポイントに焦点を当てます。これらは実際にバンディットアルゴリズムが選択される方法にしばしば影響を与えます。  



### KEYWORDS キーワード
Bandit, reward, action, E-commerce, recommendation
バンディット、報酬、アクション、Eコマース、推薦

**ACM Reference Format:** Yi Liu and Lihong Li. 2021. A Map of Bandits for E-commerce. 
**ACM参照形式:** Yi LiuとLihong Li. 2021. Eコマースのためのバンディットの地図。 

In Proceedings _of Marble-KDD 21. Singapore, 5 pages._
Marble-KDD 21の議事録において。シンガポール、5ページ。



### 1 INTRODUCTION AND MOTIVATION 1. はじめにと動機

Bandit is a framework for sequential decision making, where the decision maker (“agent”) sequentially chooses an action (also known as an “arm”), potentially based on the current contextual information, and observes a reward signal. 
バンディットは、逐次的な意思決定のためのフレームワークであり、意思決定者（「エージェント」）が逐次的にアクション（「アーム」とも呼ばれる）を選択し、現在の文脈情報に基づいて、報酬信号を観察します。 
The typical goal of the agent is to learn an optimal action-selection policy to maximize some function of the observed reward signals. 
エージェントの典型的な目標は、観察された報酬信号のいくつかの関数を最大化するための最適なアクション選択ポリシーを学習することです。 
This problem is a special case of reinforcement learning (RL) [1], and has been a subject of extensive research in AI. 
この問題は強化学習（RL）の特別なケースであり[1]、AIにおける広範な研究の対象となっています。

The main reason for extensive research of Bandit in the literature is its wide applications. 
文献におけるバンディットの広範な研究の主な理由は、その広範な応用です。 
The paper focuses on one of the most important domains, E-commerce, including online recommendation, dynamic pricing, supply chain optimization, among others [2]. 
本論文は、オンライン推薦、動的価格設定、サプライチェーン最適化などを含む、最も重要な領域の1つであるEコマースに焦点を当てています[2]。 
For instance, Bandit has been used for online recommendation across companies such as Amazon, Google, Netflix, and Yahoo! [3]. 
例えば、バンディットはAmazon、Google、Netflix、Yahoo!などの企業でオンライン推薦に使用されています[3]。 
Early applications were on optimizing webpage content suggestion such as news articles, advertisement, and marketing messages [4, 5]. 
初期の応用は、ニュース記事、広告、マーケティングメッセージなどのウェブページコンテンツの提案を最適化することにありました[4, 5]。 
Nowadays, its applications have been extended to dynamic pricing [6], revenue management [7], inventory buying [8], as well as recommendation of various contents such as skills through virtual assistants [9]. 
現在では、その応用は動的価格設定[6]、収益管理[7]、在庫購入[8]、およびバーチャルアシスタントを通じたスキルなどのさまざまなコンテンツの推薦にまで拡張されています[9]。 

The rich body of literature not only offers a diverse toolbox of algorithms, but also makes it hard for a practitioner to find the right solution to solve the problem at hand.  
文献の豊富な体は、多様なアルゴリズムのツールボックスを提供するだけでなく、**実務者が直面している問題を解決するための適切な解決策を見つけるのを難しくします**。
A main challenge lies in the many choices when formulating a Bandit problem, and the resulting combinatorial explosion of problem space and algorithms.  
主な課題は、バンディット問題を定式化する際の多くの選択肢と、それに伴う問題空間とアルゴリズムの組み合わせ爆発にあります。  
Typical textbooks on Bandits focus on designing and analyzing algorithms [10, 11], and surveys on applications often present a list of individual applications [e.g., 3].  
バンディットに関する典型的な教科書は、アルゴリズムの設計と分析に焦点を当てており[10, 11]、アプリケーションに関する調査はしばしば個々のアプリケーションのリストを提示します[e.g., 3]。  
While they are valuable resources, there is a gap in mapping applications to algorithms.  
それらは貴重なリソースですが、アプリケーションをアルゴリズムにマッピングする際にギャップがあります。  
This paper aims to reduce this gap, by presenting a structured map for the world of Bandits.  
この論文は、バンディットの世界のための構造化されたマップを提示することで、このギャップを縮小することを目的としています。  
The map consists of a few key decision points, to guide practitioners to navigate in the complex world of Bandits to locate proper algorithms.  
このマップは、実務者がバンディットの複雑な世界をナビゲートし、適切なアルゴリズムを見つけるためのいくつかの重要な意思決定ポイントで構成されています。  
While we use E-commerce as running examples, the map is useful to other applications.  
私たちはEコマースを実例として使用しますが、このマップは他のアプリケーションにも役立ちます。  
Furthermore, it is beyond the scope of the paper to provide a comprehensive map.  
さらに、包括的なマップを提供することはこの論文の範囲を超えています。  
Instead, our map only focuses on a small number of factors that often affect how Bandit algorithms are chosen in practice.  
代わりに、私たちのマップは、実際にバンディットアルゴリズムがどのように選ばれるかにしばしば影響を与える少数の要因にのみ焦点を当てています。  
The map entry is section 2, which assesses whether Bandit is the right formulation.  
マップのエントリはセクション2であり、バンディットが正しい定式化であるかどうかを評価します。  
Sections 3 and 4 describe the navigational details of the map, to help locate appropriate algorithms by inspecting several properties of rewards and actions of the application at hand.  
セクション3と4では、マップのナビゲーションの詳細を説明し、対象のアプリケーションの報酬とアクションのいくつかの特性を検査することで適切なアルゴリズムを見つける手助けをします。  
Section 5 complements the map with a discussion of topics that a practitioner often faces.  
セクション5では、実務者がしばしば直面するトピックについての議論でマップを補完します。  
Section 6 concludes the paper.  
セクション6で論文を締めくくります。  

<!-- ここまで読んだ! -->

### 2 MAP ENTRY: IS BANDIT THE RIGHT FORMULATION? バンドitは適切な定式化か？

In typical sequential decision making modeled by Bandit, the agent repeats the following in every step: observe contextual information _𝑥𝑡_, take an action 𝑎𝑡 from an action set 𝐴𝑡, and receive reward 𝑟𝑡, where 𝑡 denotes the step. 
バンドitによってモデル化された典型的な逐次意思決定では、エージェントは各ステップで以下のことを繰り返します：文脈情報 _𝑥𝑡_ を観察し、アクションセット 𝐴𝑡 からアクション 𝑎𝑡 を選択し、報酬 𝑟𝑡 を受け取ります。ここで、𝑡 はステップを示します。
The reward depends on 𝑥𝑡 and 𝑎𝑡. 
報酬は 𝑥𝑡 と 𝑎𝑡 に依存します。
The objective of a Bandit algorithm is to recommend actions for each step to maximize the expected cumulative reward over time: $R[T] = \sum_{t=1}^{T} E[r_t]$ where 𝑇 is the total number of steps. 
バンドitアルゴリズムの目的は、各ステップでアクションを推奨し、時間を通じて期待される累積報酬を最大化することです：$R[T] = \sum_{t=1}^{T} E[r_t]$ ここで、𝑇 はステップの総数です。
Suppose we want to recommend a video (𝑎𝑡) from recently released ones (𝐴𝑡) to customers, an application seen with Amazon Prime video, Netflix, HBO, etc. 
最近リリースされた動画（𝑎𝑡）を顧客に推奨したいとします。これは、Amazon Prime Video、Netflix、HBOなどで見られるアプリケーションです。
We want to consider customer features to improve the recommendation relevance: film genre (drama, romance, etc.) preference of the customer (𝑥𝑡). 
推奨の関連性を向上させるために、顧客の特徴を考慮したいと思います：顧客の映画ジャンル（ドラマ、ロマンスなど）の好み（𝑥𝑡）。
The business metric of interest is total video viewers. 
関心のあるビジネスメトリックは、総視聴者数です。
The observed reward (𝑟𝑡) can then be defined as 1 if the customer watches the recommended video and 0 otherwise. 
観察された報酬（𝑟𝑡）は、顧客が推奨された動画を視聴した場合は1、そうでない場合は0と定義できます。
Assume stationarity and linear structure, we may model the reward as $E[r_t(x_t, a_t)] = g(w_0 + w_1 \cdot a_t + w_2 \cdot x_t - a_t)$ where $w_i$’s are weights parameters and $g$ is a link function to map a linear predictor to the mean of the reward. 
定常性と線形構造を仮定すると、報酬を次のようにモデル化できます：$E[r_t(x_t, a_t)] = g(w_0 + w_1 \cdot a_t + w_2 \cdot x_t - a_t)$ ここで、$w_i$ は重みパラメータであり、$g$ は線形予測子を報酬の平均にマッピングするリンク関数です。
Logit and Probit are common link functions in Bandit applications. 
Logit と Probit は、バンドitアプリケーションで一般的なリンク関数です。

The term “Bandit” refers to the fact that only the reward of the chosen action is observed. 
「バンドit」という用語は、選択されたアクションの報酬のみが観察されるという事実を指します。
If rewards of all actions are observed, the setting is called “full-information” [12]. 
すべてのアクションの報酬が観察される場合、その設定は「フルインフォメーション」と呼ばれます[12]。
For example, consider typical multi-class classification, where predicting the label for an instance can be viewed as choosing an action. 
例えば、典型的な多クラス分類を考えてみましょう。ここでは、インスタンスのラベルを予測することはアクションを選択することと見なすことができます。
It is full-information, because once we know an instance’s correct label, the rewards of all predictions are known (1 for the correct prediction and 0 otherwise). 
これはフルインフォメーションです。なぜなら、インスタンスの正しいラベルがわかれば、すべての予測の報酬がわかるからです（正しい予測には1、そうでない場合は0）。
One should follow a different algorithmic path of supervised learning [13, 14] if the application is in the full-information setting. 
**アプリケーションがフルインフォメーション設定にある場合、異なるアルゴリズムの道をたどるべきです**[13, 14]。

On the other hand, in the more general RL setting, the next context (“state”) may depend on previous contexts and taken actions, so the agent needs to reason with long-term rewards using more complex algorithms like Q-learning [1]. 
一方、より一般的な強化学習（RL）設定では、次の文脈（「状態」）は以前の文脈や取られたアクションに依存する可能性があるため、エージェントはQ-learning [1]のようなより複雑なアルゴリズムを使用して長期的な報酬を考慮する必要があります。
For example, suppose we want to maximize sales from an online shopping website, which has search, (product) detail, add-to-cart, and checkout pages. 
例えば、検索、（商品）詳細、カートに追加、チェックアウトページを持つオンラインショッピングウェブサイトからの売上を最大化したいとします。
The shopper’s state on the detail page is affected by results shown earlier on the search page. 
詳細ページでの買い物客の状態は、検索ページで以前に表示された結果に影響されます。
The revenue at the end of each shopping session depends on information on all pages in the session. 
各ショッピングセッションの最後の収益は、セッション内のすべてのページの情報に依存します。
When long-term impacts are significant, Bandits may not be the best formulation, but can still be a good baseline or starting point [15]. 
長期的な影響が重要な場合、バンドitは最適な定式化ではないかもしれませんが、依然として良いベースラインまたは出発点となる可能性があります[15]。

### 3 NAVIGATION BY REWARD 報酬によるナビゲーション

The nature of reward signals in an application plays a major role in deciding the right Bandit algorithms.  
アプリケーションにおける報酬信号の性質は、適切なバンディットアルゴリズムを決定する上で重要な役割を果たします。  
Figure 1 identifies six key properties of rewards that lead to 10 typical use cases in practice.  
図1は、実際の10の典型的な使用例に至る報酬の6つの重要な特性を特定しています。  
The highlighted two paths are perhaps the most common.  
強調された2つの経路は、おそらく最も一般的なものです。  
The key reward properties are:  
報酬の主要な特性は次のとおりです：

**Dimension The reward can be one-dimension (scalar) or multi-** dimension (vector).  
**次元 報酬は1次元（スカラー）または多次元（ベクトル）である可能性があります。**  
In the latter case, the task can be optimizing the vector reward (node 3), or maximizing one reward dimension subject to constraints on remaining dimensions (node 4).  
後者の場合、タスクはベクトル報酬（ノード3）を最適化するか、残りの次元に対する制約の下で1つの報酬次元を最大化することができます（ノード4）。  

**Distributional assumption In stochastic Bandits, the reward is** drawn from an unknown distribution.  
**分布の仮定 確率的バンディットでは、報酬は未知の分布から引き出されます。**  
When the reward distribution may change slowly over time, as in many real-world applications, one can still treat it as a stochastic Bandit by constantly retraining the policy with new data.  
報酬分布が多くの実世界のアプリケーションのように時間とともにゆっくりと変化する場合でも、新しいデータでポリシーを常に再訓練することで、依然として確率的バンディットとして扱うことができます。  
In adversarial Bandits, there is no probabilistic assumption on the reward (node 7).  
敵対的バンディットでは、報酬に関する確率的な仮定はありません（ノード7）。  

**Relativity While a reward usually measures how good an action** is, in some problems like ranking one can also work with relative rewards that compare actions, as in dueling Bandits (node 8).  
**相対性 報酬は通常、アクションの良さを測定しますが、ランキングのような一部の問題では、デュエリングバンディット（ノード8）のようにアクションを比較する相対的な報酬を扱うこともできます。**  

**Granularity When actions are combinatorial (see section 4), the** reward can be for the entire action (node 9), or can provide signal for subactions that comprise the action (node 10).  
**粒度 アクションが組み合わせ的である場合（セクション4を参照）、報酬は全体のアクション（ノード9）に対してであるか、アクションを構成するサブアクションに対する信号を提供することができます（ノード10）。**  
The latter setting is also known as semi-bandits.  
後者の設定はセミバンディットとしても知られています。  

**Delay Practical limitations like software constraints may prevent** rewards from being observed before the next actions have to be taken.  
**遅延 ソフトウェアの制約のような実用的な制限により、次のアクションを取る前に報酬が観察されるのを妨げることがあります。**  
There are two types of reward delays: bounded (node 5) and indefinite (node 6), depending on whether we have a reasonably small upper bound for the delay.  
報酬の遅延には2種類あり、制約されたもの（ノード5）と無期限のもの（ノード6）があります。これは、遅延に対して合理的に小さな上限があるかどうかによります。  

**Value type Reward can be binary (node 1) or numerical (node 2).**  
**値のタイプ 報酬はバイナリ（ノード1）または数値（ノード2）である可能性があります。**  
These two leaf nodes are unique as value type must be defined for the other seven nodes to complete the reward formulation.  
これらの2つのリーフノードは、報酬の定義を完成させるために他の7つのノードに対して値のタイプを定義する必要があるため、ユニークです。  
We take this into consideration for algorithm recommendation in Table 1.  
私たちは、表1のアルゴリズム推奨にこれを考慮します。  

We design the structure in Figure 1 so that it covers common use cases in E-commerce.  
私たちは、図1の構造を設計し、Eコマースにおける一般的な使用例をカバーしています。  
Leaf nodes 3–10 are not exhaustive as the splits are not mutually exclusive.  
リーフノード3〜10は、分割が相互に排他的でないため、網羅的ではありません。  
For instance, adversarial Bandits can also be a dueling one [30] and there can be delay in reward [22].  
例えば、敵対的バンディットはデュエリングバンディットである可能性もあり[30]、報酬に遅延がある場合もあります[22]。  
In practice, however, such combinations appear uncommon.  
しかし、実際にはそのような組み合わせは一般的ではありません。  

In Table 1, for each leaf note we list example business problems with suggested algorithms.  
表1では、各リーフノードに対して、提案されたアルゴリズムを持つビジネス問題の例をリストします。  
Given this paper’s focus, we recommend algorithms that are empirically validated, especially those that find wide applications in practice.  
本論文の焦点を考慮し、経験的に検証されたアルゴリズム、特に実際に広く応用されているものを推奨します。  
For leaf nodes 3–10, we may have two suggested benchmark papers when binary and numerical reward are both common.  
リーフノード3〜10については、バイナリ報酬と数値報酬の両方が一般的な場合に、2つの提案されたベンチマーク論文があるかもしれません。  

To find Bandit solutions for a given business problem, one can use Figure 1 as a guide to land in the most relevant node, then refer to Table 1 for similar applications and algorithmic suggestions.  
特定のビジネス問題に対するバンディットソリューションを見つけるために、図1をガイドとして使用して最も関連性の高いノードに到達し、その後、表1を参照して類似のアプリケーションとアルゴリズムの提案を確認できます。  
We emphasize that there are no universally best algorithms, but expect the suggested references offer a good starting point for algorithm development and experimentation.  
私たちは、普遍的に最良のアルゴリズムは存在しないことを強調しますが、提案された参考文献がアルゴリズムの開発と実験の良い出発点を提供することを期待しています。  



### 4 NAVIGATION BY ACTION

**Figure 2: Illustration of three action types**  
**図2: 3つのアクションタイプの図解**  

The action set 𝐴 also plays an important role in determining the right bandit algorithm.  
アクションセット𝐴は、適切なバンディットアルゴリズムを決定する上で重要な役割を果たします。 
Here, we identify two properties: action type and action set size.  
**ここでは、2つの特性を特定します：アクションタイプとアクションセットのサイズ。**
The cases based on these properties are not exclusive to those identified in the previous section, but are orthogonal in many scenarios.  
これらの特性に基づくケースは、前のセクションで特定されたものに限定されるわけではなく、多くのシナリオで直交しています。  

Figure 2 shows three common action types: single, slate and combinatorial.  
図2は、3つの一般的なアクションタイプを示しています：シングル、スレート、そしてコンビナトリアル。  
In the first, the action set is a set of items.  
最初のタイプでは、アクションセットはアイテムの集合です。  

The set is often small and finite, but can also be large or even infinite.  
このセットはしばしば小さく有限ですが、大きい場合や無限の場合もあります。  

In the second, the action is a slate consisting of a ranked list of items.  
2番目のタイプでは、アクションはアイテムのランク付けされたリストからなるスレートです。  
The challenge is the exponentially many possible permutations that require more efficient algorithms.  
課題は、より効率的なアルゴリズムを必要とする指数関数的に多くの可能な順列です。  
Furthermore, we need to consider two effects: position bias for actions shown at different slots and item diversity in the overall slate.  
さらに、異なるスロットで表示されるアクションの位置バイアスと、全体のスレートにおけるアイテムの多様性という2つの効果を考慮する必要があります。  

In the third, the action is a combinatorial object (such as content layout on a web page), consisting of sub-actions coming from different sets.  
3番目のタイプでは、アクションは異なるセットからのサブアクションで構成される組み合わせオブジェクト（ウェブページ上のコンテンツレイアウトなど）です。  
The algorithmic challenge is often in dealing with combinatorial explosions of actions, and with interaction effects between sub-actions.  
アルゴリズムの課題は、しばしばアクションの組み合わせ爆発やサブアクション間の相互作用効果に対処することにあります。 
In the literature, slate bandits are sometimes referred to as combinatorial.  
文献では、スレートバンディットは時折コンビナトリアルと呼ばれます。  
Table 2 lists business problems and recommended work by these two types.  
表2は、これら2つのタイプによるビジネス問題と推奨される作業を示しています。  

Another action property is the size of the action set.  
別のアクションの特性は、アクションセットのサイズです。  
In Figure 3, we list representative business applications with increasing size.  
図3では、サイズが増加する代表的なビジネスアプリケーションを示します。  
Many Bandit use cases have discrete actions.  
多くのバンディットのユースケースには離散的なアクションがあります。  
When the action space is small, actions ID can be considered as a categorical value and encoded as a set of binary variables in the reward formulation.  
アクション空間が小さい場合、アクションIDはカテゴリカル値と見なされ、報酬の定式化においてバイナリ変数のセットとしてエンコードできます。
When the action space becomes large, we use features to represent actions.  
アクション空間が大きくなると、アクションを表現するために特徴を使用します。  
Such action featurization not only reduces the dimension of variables but also enables generalization across actions which mitigates action cold-start problem.  
このようなアクションの特徴化は、変数の次元を削減するだけでなく、アクション間の一般化を可能にし、アクションのコールドスタート問題を軽減します。 
While action and contextual features contain different meanings, they can be handled in a similar manner.  
アクションとコンテキストの特徴は異なる意味を持ちますが、同様の方法で扱うことができます。  

More discussions are found in section 5.  
詳細な議論はセクション5にあります。  

It is also common to see continuous actions in practice.  
実際には連続的なアクションを見ることも一般的です。  

In this case, the continuous action set often has a natural distance metric, so that one can use tools like Gaussian process to solve the Bandit problem.  
この場合、連続アクションセットはしばしば自然な距離メトリックを持ち、ガウス過程のようなツールを使用してバンディット問題を解決できます。  



### 5 OTHER TOPICS その他のトピック

This section discusses feature engineering, offline policy evaluation, and best-arm identification, three important topics in Bandit applications to complement the previous sections.
このセクションでは、特徴量エンジニアリング、オフラインポリシー評価、およびベストアームの特定という、バンディットアプリケーションにおける重要な3つのトピックについて議論します。

<!-- ここまで読んだ! -->

### 5.1 特徴量エンジニアリング

In many applications, we use features to deal with large context or action sets more efficiently. 
多くのアプリケーションでは、大きなコンテキストやアクションセットをより効率的に扱うために特徴量を使用します。 
The expected reward 𝑟 can be written as a function of action features 𝝓𝒂 and contextual features 𝝓𝒙 : 𝐸 [𝑟 ] = 𝑓(𝝓𝒂, 𝝓𝒙). 
期待報酬 $r$ は、アクション特徴量 $\phi_a$ とコンテキスト特徴量 $\phi_x$ の関数として書くことができます: $E[r] = f(\phi_a, \phi_x)$。
Feature engineering in Bandit involves selection/preprocessing of 𝝓𝒂 and 𝝓𝒙 and their interaction terms. 
バンディットにおける特徴量エンジニアリングは、$\phi_a$ と $\phi_x$ の選択/前処理およびそれらの相互作用項を含みます。
Linear Bandits are the most studied in the literature where 𝐸 [𝑟 ] is assumed to be linear in the features. 
線形バンディットは、文献で最も研究されているもので、$E[r]$ は特徴量に対して線形であると仮定されています。
To model non-linearity especially when the size(s) of 𝝓𝒂 or/and 𝝓𝒙 is large, we can learn lower-dimension embeddings from the raw features (𝝓𝒂 or/and 𝝓𝒙) and put the embeddings in the reward function instead [38, 39]. 
特に $\phi_a$ または/および $\phi_x$ のサイズが大きい場合に非線形性をモデル化するために、生の特徴量（$\phi_a$ または/および $\phi_x$）から低次元の埋め込みを学習し、埋め込みを報酬関数に代わりに入れることができます [38, 39]。
Embedding generation techniques for supervised learning generally apply to Bandits [40]. 
教師あり学習のための埋め込み生成技術は一般的にバンディットに適用されます [40]。
Another way to relax the linear-reward assumption is to use non-linear Bandits where reward function becomes nonlinear in feature vectors [e.g., 31]. 
線形報酬の仮定を緩和する別の方法は、報酬関数が特徴ベクトルに対して非線形になる非線形バンディットを使用することです [e.g., 31]。

### 5.2 オフラインポリシー評価

Testing a Bandit policy in real user traffic is often expensive, and poses risks on user experiences. 
バンディットポリシーを実際のユーザートラフィックでテストすることはしばしば高価であり、ユーザー体験にリスクをもたらします。
It is common to evaluate a new policy offline before deploying it. 
新しいポリシーを展開する前にオフラインで評価することは一般的です。
A key challenge in offline policy evaluation is that we do not know how users would have reacted to actions different from the one in the log data, since the data only have rewards for selected actions. 
**オフラインポリシー評価の重要な課題は、ログデータにある行動とは異なる行動に対してユーザーがどのように反応したかを知ることができないこと**です。なぜなら、データには選択された行動に対する報酬しか含まれていないからです。
This counterfactual nature makes Bandit offline evaluation similar to causal inference where we want to infer the average reward $E_\pi [r]$ (the causal effect) if policy $\pi$ is used to choose actions. 
この反実仮想的な性質により、バンディットのオフライン評価は因果推論に似ており、ポリシー $\pi$ が行動を選択する場合の平均報酬 $E_\pi [r]$（因果効果）を推測したいと考えます。
There exist effective approaches to evaluating a stationary policy, including simulation [41], inverse propensity scoring [42, 43], doubly robust evaluation [44], and selfnormalized inverse propensity estimators [45]. 
定常ポリシーを評価するための効果的なアプローチには、シミュレーション [41]、逆傾向スコアリング [42, 43]、二重ロバスト評価 [44]、および自己正規化逆傾向推定器 [45] が含まれます。
Typically, offline evaluation becomes more challenging with a larger action set. 
**一般的に、オフライン評価はアクションセットが大きくなるほど難しくなります。**
For a slate Bandit, pseudoinverse estimator is available to account for position bias [46]. 
スレートバンディットの場合、位置バイアスを考慮するための擬似逆推定器が利用可能です [46]。
Offline evaluation for non-stationary Bandits remains challenging [47, 48], with opportunities for further research. 
非定常バンディットのオフライン評価は依然として難しく [47, 48]、さらなる研究の機会があります。

### 5.3 Best-arm Identification 最良アームの特定

In some bandit applications, our goal is not to maximize reward during an experiment, but to identify the best action (e.g., best marketing campaign strategy) at the end of the experiment. 
いくつかのバンディットアプリケーションでは、私たちの目標は実験中に報酬を最大化することではなく、実験の終了時に最良のアクション（例：最良のマーケティングキャンペーン戦略）を特定することです。 
This problem, known as best-arm identification [49–51], shares the same goal as conventional A/B/N testing [52], but can be statistically more efficient by adaptively selecting actions during an experiment.
この問題は最良アームの特定（best-arm identification）として知られ、従来のA/B/Nテストと同じ目標を共有していますが、実験中にアクションを適応的に選択することで統計的により効率的である可能性があります。



### 6 CONCLUSIONS 結論

We presented a structured map for the world of Bandits, with the hope to guide practitioners to navigate to practical Bandit algorithms. 
私たちは、Banditsの世界のための構造化されたマップを提示し、実務者が実用的なBanditアルゴリズムにナビゲートできることを期待しています。
The work is not attempted to provide a comprehensive map. 
この作業は、包括的なマップを提供することを目的としていません。
Instead, it focuses on a few key decision points that often affect how Bandit algorithms are chosen. 
代わりに、Banditアルゴリズムの選択にしばしば影響を与えるいくつかの重要な意思決定ポイントに焦点を当てています。
We hope it reduces the gap in connecting applications to appropriate algorithms. 
私たちは、アプリケーションと適切なアルゴリズムを結びつけるギャップを減少させることを期待しています。
