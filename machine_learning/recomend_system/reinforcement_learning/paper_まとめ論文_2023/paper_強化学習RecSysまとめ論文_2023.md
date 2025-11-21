refs: https://arxiv.org/pdf/2308.11336


## On the Opportunities and Challenges of Offline Reinforcement Learning for Recommender Systems  
オフライン強化学習の推薦システムにおける機会と課題  

### XIAOCONG CHEN, Data61, CSIRO, Australia  
シアオコン・チェン、Data61、CSIRO、オーストラリア  
SIYU WANG, UNSW Sydney, Australia  
シユ・ワン、UNSWシドニー、オーストラリア  
JULIAN MCAULEY, UCSD, USA  
ジュリアン・マカウリー、UCSD、アメリカ  
DIETMAR JANNACH, University of Klagenfurt, Austria  
ディートマール・ヤンナッハ、クラゲンフルト大学、オーストリア  
LINA YAO, Data61, CSIRO & UNSW Sydney, Australia  
リナ・ヤオ、Data61、CSIRO & UNSWシドニー、オーストラリア  

Reinforcement learning serves as a potent tool for modeling dynamic user interests within recommender systems, garnering increasing research attention of late.  
強化学習は、推薦システム内で動的なユーザの興味をモデル化するための強力なツールとして機能し、最近では研究の注目を集めています。  
However, a significant drawback persists: its poor data efficiency, stemming from its interactive nature.  
しかし、重要な欠点が残っています。それは、**インタラクティブな性質から生じるデータ効率の悪さ**です。  
The training of reinforcement learning-based recommender systems demands expensive online interactions to amass adequate trajectories, essential for agents to learn user preferences.  
強化学習に基づく推薦システムのトレーニングは、エージェントがユーザの好みを学ぶために必要な十分な軌跡を集めるために、高価なオンラインインタラクションを必要とします。  
This inefficiency renders reinforcement learning-based recommender systems a formidable undertaking, necessitating the exploration of potential solutions.  
この非効率性は、強化学習に基づく推薦システムを困難な取り組みとし、潜在的な解決策の探求を必要とします。  
Recent strides in offline reinforcement learning present a new perspective.  
最近のオフライン強化学習の進展は、新たな視点を提供します。  
Offline reinforcement learning empowers agents to glean insights from offline datasets and deploy learned policies in online settings.  
オフライン強化学習は、エージェントがオフラインデータセットから洞察を得て、オンライン環境で学習したポリシーを展開することを可能にします。  
Given that recommender systems possess extensive offline datasets, the framework of offline reinforcement learning aligns seamlessly.  
推薦システムは広範なオフラインデータセットを持っているため、オフライン強化学習のフレームワークはシームレスに適合します。  
Despite being a burgeoning field, works centered on recommender systems utilizing offline reinforcement learning remain limited.  
急成長している分野であるにもかかわらず、オフライン強化学習を利用した推薦システムに焦点を当てた研究は限られています。  
This survey aims to introduce and delve into offline reinforcement learning within recommender systems, offering an inclusive review of existing literature in this domain.  
この調査は、推薦システムにおけるオフライン強化学習を紹介し、掘り下げることを目的としており、この分野の既存文献の包括的なレビューを提供します。  
Furthermore, we strive to underscore prevalent challenges, opportunities, and future pathways, poised to propel research in this evolving field.  
さらに、私たちは、進化するこの分野の研究を推進するための一般的な課題、機会、将来の道筋を強調することに努めます。  

<!-- ここまで読んだ! -->

## 1 INTRODUCTION はじめに

In recent years, notable advancements have materialized in the realm of recommendation techniques, transcending the scope of traditional approaches (such as collaborative filtering, content-based recommendation, and matrix factorization [32]). 
近年、推薦技術の分野で顕著な進展が見られ、従来のアプローチ（協調フィルタリング、コンテンツベースの推薦、行列因子分解など [32]）の範囲を超えています。
This evolution has led to the emergence of deep learning-based methods in the field of recommender systems (RS). 
この進化は、レコメンダーシステム（RS）の分野における深層学習ベースの手法の出現をもたらしました。
The appeal of deep learning stems from its ability to comprehend intricate non-linear relationships between users and items, making it adept at accommodating diverse data sources like images and text. 
**深層学習の魅力は、ユーザとアイテム間の複雑な非線形関係を理解する能力にあり、画像やテキストなどの多様なデータソースに対応するのに優れています**。
The adoption of deep learning in RS has proven beneficial in tackling multifaceted challenges. 
RSにおける深層学習の採用は、多面的な課題に対処するのに有益であることが証明されています。
Its strength lies in addressing intricate tasks and managing complex data structures [61]. 
その強みは、複雑なタスクに対処し、複雑なデータ構造を管理することにあります[61]。

<!-- ここまで読んだ -->

Traditional recommendation systems (RS) have limitations in capturing interest dynamics, a challenge that emphasizes the distinction between users’ long-term and short-term interests [7, 61]. 
従来の推薦システム（RS）は、興味のダイナミクスを捉える上で限界があり、これはユーザーの長期的および短期的な興味の違いを強調する課題です[7, 61]。
Specifically, while these traditional methods are adept at recognizing and modeling long-term interests based on historical data and patterns, they often fall short in accounting for the rapidly changing and more nuanced short-term interests. 
具体的には、これらの従来の手法は、歴史的データやパターンに基づいて長期的な興味を認識しモデル化するのに優れていますが、急速に変化するより微妙な短期的な興味を考慮するのにはしばしば不十分です。
This gap in responsiveness to short-term shifts can lead to recommendations that are out-of-sync with a user’s current preferences or situational needs. 
短期的な変化に対する反応のギャップは、ユーザーの現在の好みや状況に合わない推薦をもたらす可能性があります。
In contrast, deep reinforcement learning (RL) aims to train an agent with the capacity to learn from interaction trajectories provided by the environment, achieved through the integration of deep learning and RL techniques as expounded in [11]. 
対照的に、深層強化学習（RL）は、環境から提供される相互作用の軌跡から学ぶ能力を持つエージェントを訓練することを目指しており、これは[11]で詳述されている深層学習とRL技術の統合を通じて達成されます。
Notably, this approach empowers the agent to proactively glean insights from real-time user feedback, thereby enabling the discernment of evolving user preferences within the dynamic context of reinforcement learning. 
特に、このアプローチはエージェントにリアルタイムのユーザーフィードバックから積極的に洞察を得る能力を与え、強化学習の動的な文脈の中で進化するユーザーの好みを識別できるようにします。

<!-- ここまで読んだ -->

RL provides a structured mathematical framework for acquiring learning-based control strategies. 
RLは、学習に基づく制御戦略を取得するための構造化された数学的枠組みを提供します。
By employing RL, we can systematically attain highly effective behavioral policies, which encapsulate action strategies. 
**RLを利用することで、行動戦略を包含する非常に効果的な行動ポリシーを体系的に達成できます。**
These policies are engineered to optimize predefined objectives referred to as reward functions. 
これらのポリシーは、報酬関数と呼ばれる事前に定義された目的を最適化するように設計されています。
In essence, the reward function serves as a directive, guiding the RL algorithm towards desired actions, while the algorithm itself devises the means to enact these actions. 
**本質的に、報酬関数は指針として機能し、RLアルゴリズムを望ましい行動に導き、アルゴリズム自体がこれらの行動を実行する手段を考案します。**
Throughout its history, the field of RL has been a subject of intensive research. 
RLの分野は、その歴史を通じて集中的な研究の対象となってきました。
More recently, the integration of robust tools like deep neural networks into RL methodologies has yielded substantial advancements. 
最近では、深層ニューラルネットワークのような強力なツールをRLの方法論に統合することで、実質的な進展が得られています。
These neural networks act as versatile approximators, empowering RL techniques to exhibit exceptional performance across a diverse array of problem domains. 
**これらのニューラルネットワークは多用途の近似器として機能し、RL技術が多様な問題領域で卓越したパフォーマンスを発揮できるようにします。**

<!-- ここまで読んだ -->

Nevertheless, a pertinent challenge to the widespread implementation of RL techniques emerges. 
それにもかかわらず、RL技術の広範な実装に対する重要な課題が浮上します。
RL methods fundamentally follow an incremental learning approach, wherein they gather knowledge by iteratively engaging with their environment. 
RL手法は基本的に漸進的な学習アプローチに従い、環境と反復的に関与することで知識を集めます。
Subsequent refinements are informed by previous experiences. 
その後の改良は、以前の経験に基づいて行われます。
While this iterative learning approach is effective in numerous scenarios, its practicality is not universal. 
**この反復学習アプローチは多くのシナリオで効果的ですが、その実用性は普遍的ではありません。**
Consider cases such as real-world robotics, educational software pedagogy, or healthcare interventions; these situations entail potential risks and resource expenses that cannot be disregarded. 
実世界のロボティクス、教育ソフトウェアの教育法、または医療介入などのケースを考えてみてください。これらの状況は、無視できない潜在的なリスクとリソースの費用を伴います。
Moreover, even within scenarios conducive to online learning, such as in the context of RS, a preference for historical data often arises. 
さらに、RSの文脈のようにオンライン学習に適したシナリオ内でも、歴史的データへの好みがしばしば生じます。
This preference is particularly pronounced in intricate domains where sound decision-making hinges upon substantial data inputs. 
この好みは、健全な意思決定が substantial data inputs に依存する複雑な領域では特に顕著です。
The rationale is that leveraging previously amassed data enables informed decisions without necessitating continuous real-world experimentation. 
その理由は、**以前に蓄積されたデータを活用することで、継続的な実世界の実験を必要とせずに情報に基づいた意思決定が可能になるから**です。

<!-- ここまで読んだ -->

The success of machine learning methods in solving real-world problems in the past decade is largely thanks to new ways of learning from large amounts of data. 
過去10年間における機械学習手法の実世界の問題解決における成功は、大量のデータから学ぶ新しい方法のおかげです。
These methods get better as they’re trained with more data. 
これらの手法は、より多くのデータで訓練されることで改善されます。
However, applying this approach to online Reinforcement Learning (RL) doesn’t fit well. 
**しかし、このアプローチをオンライン強化学習（RL）に適用することはうまくいきません。**
While this wasn’t a big problem when RL methods were simpler and used small datasets for easy problems, adding complex neural networks to RL makes us wonder if we can use the same data-driven approach for RL goals. 
RL手法がより単純で簡単な問題に小さなデータセットを使用していたときには大きな問題ではありませんでしたが、複雑なニューラルネットワークをRLに追加すると、RLの目標に対して同じデータ駆動型アプローチを使用できるかどうか疑問に思います。
This would mean creating a system where RL learns from existing data without needing more data collected in real-time [27]. 
これは、RLがリアルタイムで収集されたデータを必要とせずに既存のデータから学ぶシステムを作成することを意味します[27]。

However, this idea of using existing data for RL brings its own challenges. 
しかし、RLに既存のデータを使用するというこのアイデアは独自の課題をもたらします。
As we discuss in this article, many common RL methods can learn from data collected differently from how the policy behaves. 
**この記事で議論するように、多くの一般的なRL手法は、ポリシーの振る舞いとは異なる方法で収集されたデータから学ぶことができます。** (データ収集方策と学習方策ね...!:thinking:)
But these methods often struggle when trying to learn effectively from a whole set of data collected in advance, without more data being collected as the policy improves. 
しかし、これらの手法は、ポリシーが改善されるにつれて新たなデータが収集されることなく、事前に収集されたデータ全体から効果的に学ぼうとするとしばしば苦労します。
Making things more complicated with high-dimensional neural networks can make this problem worse. 
高次元のニューラルネットワークで事態を複雑にすることは、この問題を悪化させる可能性があります。
A big issue with using pre-existing data for RL is that the data’s distribution may not match real-world conditions [27]. 
RLに既存のデータを使用する際の大きな問題は、データの分布が実世界の条件と一致しない可能性があることです[27]。
Still, the potential of a fully offline RL system is exciting. 
それでも、完全なオフラインRLシステムの可能性は魅力的です。
Just like how machine learning can turn data into useful tools like image recognition or speech understanding, an offline RL system, using strong function approximators, might turn data into smart decision-makers. 
機械学習がデータを画像認識や音声理解のような有用なツールに変えるのと同様に、強力な関数近似器を使用したオフラインRLシステムは、データをスマートな意思決定者に変える可能性があります。
This could mean that people with lots of data could make policies that help them make better choices for what they want to achieve [35]. 
これは、多くのデータを持つ人々が、達成したい目標に対してより良い選択をするのに役立つポリシーを作成できることを意味します[35]。

<!-- ここまで読んだ -->

RS and advertising are particularly well-suited areas for applying offline RL. 
**RSと広告は、オフラインRLを適用するのに特に適した分野**です。
This is because collecting data is straightforward and efficient, often done by recording user actions. 
これは、**データの収集が簡単で効率的であり、ユーザーの行動を記録することで行われることが多いため**です。
Moreover, the existing RS literature provides sufficient datasets which can be used for training offline RL. 
さらに、既存のRS文献は、オフラインRLの訓練に使用できる十分なデータセットを提供しています。
However, these domains are also critical in terms of safety. 
しかし、これらの領域は安全性の観点からも重要です。
Making a very poor decision could lead to significant financial losses. 
**非常に悪い決定を下すことは、重大な財務損失につながる可能性があります**。(うんうん。だからRSではオフライン学習ゼロから始めることはできない...!:thinking:)
Therefore, traditional online exploration methods are not practical here. 
したがって、従来のオンライン探索手法はここでは実用的ではありません。
This is why offline RL methods have a history of being used in these fields. 
これが、オフラインRL手法がこれらの分野で使用されてきた理由です。

<!-- ここまで読んだ -->

One technique commonly employed is called off-policy evaluation. 
一般的に使用される手法の1つは、オフポリシー評価と呼ばれます。
This approach is useful for running A/B tests and estimating the effectiveness of advertising and RS methods without needing to interact with the environment further. 
このアプローチは、A/Bテストを実行し、広告やRS手法の効果を推定するのに役立ち、さらに環境と相互作用する必要がありません。

In the case of RS, things are a bit different compared to other applications. 
RSの場合、他のアプリケーションと比較して状況は少し異なります。
RS policy evaluation is often set up as a contextual bandit problem. 
**RSのポリシー評価は、しばしばコンテキストバンディット問題として設定されます**。
Here, "states" might represent a user’s past behavior, and "actions" are the recommendations made to them. 
ここで、「状態」はユーザーの過去の行動を表し、「行動」は彼らに対して行われた推薦です。
This simplification avoids the complexity of sequential decision making, which is useful. 
この単純化は、連続的な意思決定の複雑さを回避し、有用です。
However, it can lead to inaccuracies if actions are connected over time, like in robotics or healthcare scenarios. 
しかし、ロボティクスや医療シナリオのように、行動が時間的に関連している場合、誤差を引き起こす可能性があります。

Using offline RL for RS has practical applications such as optimizing recommendations presented together on a page, improving entire web pages, and estimating website visits with the help of doubly robust estimation. 
RSにオフラインRLを使用することには、ページ上で一緒に提示される推薦の最適化、全体のウェブページの改善、ダブリーロバスト推定を用いたウェブサイト訪問の推定などの実用的な応用があります。
Another use is A/B testing to fine-tune click rates for optimization. 
別の用途は、最適化のためにクリック率を微調整するA/Bテストです。
Researchers have also used offline data to learn policies. 
研究者たちは、オフラインデータを使用してポリシーを学習することもあります。
This includes efforts like improving clickthrough rates for newspaper articles, ranking advertisements on search pages, and tailoring ad recommendations for digital marketing. 
これには、新聞記事のクリック率を改善すること、検索ページでの広告のランキング、デジタルマーケティングのための広告推薦を調整することなどの取り組みが含まれます。

In this survey, our main focus will be on offline RL in RS (offline RL4RS). 
この調査では、私たちの主な焦点はRSにおけるオフラインRL（offline RL4RS）になります。
We aim to provide a comprehensive overview of existing works, along with discussing open challenges and future directions. 
私たちは、既存の研究の包括的な概要を提供し、オープンな課題と将来の方向性について議論することを目指しています。

<!-- ここまで読んだ! -->

**1.1** **Relations to existing surveys** **1.1 既存の調査との関係**

Two existing surveys have centered on the topic of RL in RS [1, 11]. 
既存の2つの調査は、RSにおけるRLのトピックに焦点を当てています[1, 11]。
While Afsar et al. [1] provides an overview of RL in RS, it does not comprehensively explore the expanding realm of deep RL. 
Afsar et al. [1]はRSにおけるRLの概要を提供していますが、深層RLの拡大する領域を包括的に探求していません。
In contrast, [11] delves more deeply into the analysis and discussion of RL in RS, but predominantly focuses on online RL and its RS applications. 
対照的に、[11]はRSにおけるRLの分析と議論により深く掘り下げていますが、主にオンラインRLとそのRSアプリケーションに焦点を当てています。
It’s noteworthy that [11] identifies offline RL in RS as a potential future direction but does not offer an all-encompassing review of this area. 
[11]はRSにおけるオフラインRLを潜在的な将来の方向性として特定していますが、この分野の包括的なレビューを提供していません。
The limited coverage of offline RL in RS can be attributed to its emergence around the same time as these two surveys. 
RSにおけるオフラインRLの限られたカバレッジは、これらの2つの調査とほぼ同時に出現したことに起因しています。
Furthermore, due to the recent establishment of the offline RL concept, certain works examined in these two existing surveys are classified as special cases of policy-based methods. 
さらに、オフラインRLの概念が最近確立されたため、これらの2つの既存の調査で検討された特定の研究は、ポリシーベースの手法の特別なケースとして分類されています。
Differently, this survey endeavors to refine these categorizations by reclassifying prior works into the domain of offline RL in RS. 
異なり、この調査は、以前の研究をRSにおけるオフラインRLの領域に再分類することで、これらの分類を洗練させることを目指しています。
Additionally, we extend the literature to encompass the most recent developments in offline RL for RS, thereby augmenting our understanding of recent progress in this field. 
さらに、RSのためのオフラインRLにおける最近の発展を含むように文献を拡張し、この分野の最近の進展に対する理解を深めます。

<!-- ここまで読んだ -->

**1.2** **Structure of this Survey**
**1.2 この調査の構成**

This survey is structured into four distinct sections. 
この調査は4つの異なるセクションに構成されています。
Firstly, we offer an introduction to RL basics, providing readers with a foundational understanding of various RL algorithms, including Q-Learning, Policy-based Methods, Actor-Critic Methods, and Model-based RL. 
まず、RLの基本についての紹介を提供し、Q-Learning、ポリシーベースの手法、アクター-クリティック手法、モデルベースのRLなど、さまざまなRLアルゴリズムの基礎的な理解を読者に提供します。
Subsequently, we delve into the concept of offline RL and present a problem formulation that explores how to integrate recommender systems (RS) into the offline RL framework. 
次に、オフラインRLの概念に深く入り込み、**推薦システム（RS）をオフラインRLフレームワークに統合する方法を探る問題の定式化**を提示します。
Continuing, we conduct a comprehensive review of existing works from two main perspectives: off-policy evaluation using logged data and the realm of offline RL in RS. 
続いて、ログデータを使用したオフポリシー評価とRSにおけるオフラインRLの領域という2つの主要な視点から、既存の研究の包括的なレビューを行います。
This examination highlights current research trends and insights. 
この調査は、現在の研究動向と洞察を強調します。
Following the review, we outline the open challenges and promising opportunities that warrant in-depth exploration. 
レビューの後、私たちは詳細な探求に値するオープンな課題と有望な機会を概説します。
Finally, building upon the identified challenges and opportunities, we propose potential future directions that could serve as solutions to these challenges. 
最後に、特定された課題と機会に基づいて、これらの課題に対する解決策となる可能性のある将来の方向性を提案します。
This forward-looking section aims to guide future research endeavors in the field, by suggesting pathways to address the outstanding issues and capitalize on the untapped opportunities. 
この将来を見据えたセクションは、未解決の問題に対処し、未開拓の機会を活用するための道筋を提案することで、この分野の将来の研究努力を導くことを目指しています。

<!-- ここまで読んだ! -->

## 2 OFFLINE RL OVERVIEW AND PROBLEM STATEMENT
## 2 オフラインRLの概要と問題定義

In this section, we delve into fundamental concepts essential to understanding the field of RL. 
このセクションでは、強化学習（RL）分野を理解するために不可欠な基本概念について掘り下げます。
We initiate with RL preliminaries, encompassing Markov Decision Processes, On-Policy and Off-Policy Learning, and Typical RL algorithms. 
まず、マルコフ決定過程、オンポリシー学習とオフポリシー学習、典型的なRLアルゴリズムを含むRLの前提知識から始めます。
In doing so, we establish the foundational understanding by clarifying key principles and terminologies employed throughout this survey. 
その過程で、**本調査全体で使用される主要な原則と用語を明確にする**ことにより、基礎的な理解を確立します。
Subsequently, we shift our focus toward the concept of offline RL and how it can be used to formulate RS. 
その後、オフラインRLの概念と、それが推薦システム（RS）を形成するためにどのように使用できるかに焦点を移します。
For the sake of clarity, we have summarized the common notations used in this survey in Table 1. 
明確さのために、本調査で使用される一般的な表記を表1にまとめました。

- 表1: 本調査で使用される一般的な表記
  - $M$: マルコフ決定過程
  - $\pi_{\beta}$: behavior policy(データ収集方策)
  - $\gamma$: 割引因子(discount factor)
  - $E$: 期待値(expected value)
  - $\theta$: 方策のパラメータ(policy parameter)
  - $s$: 状態(state) - ユーザ関連情報
  - $a$: 行動(action) - 推薦アイテム
  - $\pi$: 方策(policy) - 推薦方策, target policy
  - $R(\cdot, \cdot)$: 報酬関数(reward function) - 例えばユーザのクリック行動
  - $D$: オフラインデータセット(offline dataset) - $\{(s_t, a_t, s_{t+1}, r_t)\}$ の集合

**2.1** **Markov Decision Process**  
**2.1** **マルコフ決定過程**

In this section, we shall expound upon fundamental concepts within the realm of RL, adhering closely to established standard definitions as outlined in[44]. 
このセクションでは、RLの領域内の基本概念について詳述し、[44]で概説された確立された標準定義に密接に従います。
RL deals with the challenge of learning how to control dynamic systems in a broad context. 
RLは、広い文脈で動的システムを制御する方法を学ぶという課題に取り組みます。
RL4RS are typically described by fully observed Markov decision processes (MDP) or partially observed ones known as Partially Observable Markov Decision Processes (POMDP). 
**RL4RSは通常、完全に観測されたマルコフ決定過程（MDP）または部分的に観測されたマルコフ決定過程（POMDP）として説明されます。**
Moreover, we will also provide  
さらに、私たちは以下の定義を提供します。

---

Definition 1 (Markov decision process). The Markov decision process is formalized as the tuple M = {S, A, P, R,𝛾 }. 
定義1（マルコフ決定過程）。マルコフ決定過程は、タプル $M = {S, A, P, R, \gamma}$ として形式化されます。
Within this structure, each component serves a distinct purpose: S encompasses the set of states 𝑠_ ∈S, capable of adopting discrete or continuous values, potentially even multi-dimensional vectors. 
この構造内で、各コンポーネントは異なる目的を果たします。Sは状態の集合 $s \in S$ を包含し、離散または連続の値を採用でき、場合によっては多次元ベクトルでさえあります。
A characterizes the set of actions 𝑎_ ∈A, which may be discrete or continuous in _nature. 
$A$ は、性質上離散または連続である可能性のあるアクションの集合 $a \in A$ を特徴付けます。
P defines a conditional probability distribution, P(𝑠𝑡_ +1|𝑠𝑡,𝑎𝑡 ), delineating the progression of _the system’s dynamics over time. 
$P$ は条件付き確率分布 $P(s_{t+1} | s_t, a_t)$ を定義し、システムの動態が時間とともに進行する様子を示します。(状態遷移の確率分布だよね...!:thinking:)
R : S × A →_ R serves as the reward function, linking states and _actions to real-valued rewards. 
$R : S × A → \mathbb{R}$ は報酬関数として機能し、状態とアクションを実数値の報酬に結び付けます。
𝛾_ ∈[0, 1] assumes the role of a scalar discount factor, influencing the _extent to which future rewards are taken into consideration._ 
$\gamma \in [0, 1]$ はスカラーの割引因子の役割を果たし、将来の報酬が考慮される程度に影響を与えます。

---

Throughout most of this article, we will primarily employ fully-observed formalism. 
この記事のほとんどの部分では、主に完全観測形式を使用します。
However, we also include the definition of the partially observed Markov decision process (POMDP) to ensure comprehensiveness. 
ただし、包括性を確保するために、**部分的に観測されたマルコフ決定過程（POMDP, Partially Observed Markov Decision Process）**の定義も含めます。
The MDP definition can be extended to the partially observed setting in the following manner:  
MDPの定義は、以下のように部分的に観測された設定に拡張できます。

---

Definition 2 (Partially observed Markov decision process). The partially observed Markov _decision process is defined as a tuple M = {S, A, O, P, R,𝛾_ }, where S, A, P, R,𝛾 _are defined as_ _before, O is a set of observations, where each observation is given by 𝑜_ ∈O.  
定義2（部分的に観測されたマルコフ決定過程）。部分的に観測されたマルコフ決定過程は、タプル $M = {S, A, O, P, R, \gamma}$ として定義されます。ここで、$S, A, P, R, \gamma$ は前述のように定義され、$O$ は観測の集合であり、各観測は $o \in O$ によって与えられます。

---

The ultimate objective within a RL problem is to acquire a policy, denoted as 𝜋, which establishes a probability distribution over actions conditioned upon states, 𝜋 (𝑎𝑡 |𝑠𝑡 ), or alternatively conditioned upon observations within the context of partially observed scenarios, 𝜋 (𝑎𝑡 |𝑜𝑡 ).  
RL問題における最終的な目的は、ポリシー $\pi$ を取得することであり、これは状態に条件付けられたアクションに関する確率分布 $\pi (a_t | s_t)$ または部分的に観測されたシナリオの文脈で観測に条件付けられた $\pi (a_t | o_t)$ を確立します。
From these definitions, we can derive the trajectory distribution. 
これらの定義から、軌道分布を導出できます。
A trajectory in this context refers to a sequence encompassing both states and actions, spanning a length of _𝑇_, represented as 𝜏 = {𝑠0,𝑎0, · · ·,𝑠𝑇 _,𝑎𝑇_ }.  
この文脈における軌道は、状態とアクションの両方を含むシーケンスを指し、長さ $T$ にわたり、$\tau = {s_0, a_0, \cdots, s_T, a_T}$ と表されます。
It is noteworthy that the parameter 𝑇 can be an infinite value, implying the consideration of scenarios with an indefinite time horizon, as seen in infinite horizon MDP [44].  
パラメータ $T$ は無限の値である可能性があり、無限ホライズンMDP [44] に見られるように、無期限の時間ホライズンを持つシナリオを考慮することを意味します。
The trajectory distribution 𝑝𝜋 for a given MDP tuple M and policy 𝜋 is given by  
与えられたMDPタプルMとポリシー $\pi$ の軌道分布 $p_{\pi}$ は次のように与えられます。

$$
p_\pi(\tau) = d_0(s_0) \prod_{t=0}^{T} \pi(a_t | s_t) P(s_{t+1} | s_t, a_t),
\tag{1}
$$  

(メモ: $p(\tau)$ は2*T個の確率変数の同時分布みたいなイメージ...!! なので 積の形で表されてる...!!:thinking:)

where 𝑑_0(𝑠_0) represents the initial state distribution. 
ここで、 $d_0(s_0)$ は初期状態分布を表します。
This definition can easily be extended into the partially observed setting by including the observations 𝑜𝑡 . 
この定義は、観測 $o_t$ を含めることで、部分的に観測された設定に簡単に拡張できます。
The RL objective 𝐽 (𝜋), can then be written as an expectation under this trajectory distribution:  
RLの目的 $J(\pi)$ は、この軌道分布の下での期待値として次のように書くことができます。

$$
J(\pi) = E_{\tau \sim p_\pi(\tau)} \left[ \sum_{t=0}^{T} \gamma^t R(s_t, a_t) \right].
\tag{2}
$$

(メモ: 期待値の中身は、割引報酬の和! $R(s_t, a_t)$ は即時報酬...!!:thinking:)

<!-- ここまで読んだ -->

**2.2** **On-Policy and Off-Policy Learning**  
**2.2** **オンポリシーとオフポリシー学習**

While the process of interaction unfolds, gathering additional episodes enhances the precision of the function estimates. 
**インタラクションのプロセスが進行する間、追加のエピソードを収集することで関数推定の精度が向上し**ます。
Nevertheless, a challenge arises. 
しかし、課題が生じます。
If the policy improvement algorithm consistently adjusts the policy in a greedy manner—prioritizing actions with immediate rewards— then actions and states lying outside this advantageous route might not be adequately sampled. 
ポリシー改善アルゴリズムが常に貪欲な方法でポリシーを調整し、即時報酬のあるアクションを優先する場合、この有利なルートの外にあるアクションや状態は十分にサンプリングされない可能性があります。(活用ばっかりだと困るねって話ね!!:thinking:)
Consequently, superior rewards that could exist in these unexplored areas remain concealed from the learning process. 
その結果、これらの未探索の領域に存在する可能性のある優れた報酬は、学習プロセスから隠されたままになります。
Fundamentally, we confront a decision between opting for the optimal choice based on existing data or delving deeper into exploration to collect more data. 
基本的に、既存のデータに基づいて最適な選択をするか、より多くのデータを収集するために探索を深めるかの決定に直面します。
This predicament is commonly recognized as the Exploration vs. Exploitation Dilemma. 
このジレンマは、**探索と活用のジレンマ**として一般的に認識されています。

What we need is a middle ground between these two extremes. 
私たちが必要とするのは、これら二つの極端の間の中間点です。
Pure exploration would require a significant amount of time to collect the necessary information, while pure exploitation could trap the agent in a local reward maximum. 
純粋な探索は、必要な情報を収集するために多くの時間を要し、純粋な活用はエージェントを局所的な報酬の最大値に閉じ込める可能性があります。
To address this, there are two approaches that ensure all actions are adequately sampled, known as on-policy and off-policy methods. 
これに対処するために、**すべてのアクションが適切にサンプリングされることを保証する二つのアプローチ、すなわちオンポリシーとオフポリシー手法**があります。

<!-- ここまで読んだ -->

On-policy methods resolve the exploration vs. exploitation dilemma by incorporating randomness_ through a soft policy. 
オンポリシー手法は、ソフトポリシーを通じてランダム性を取り入れることにより、探索と活用のジレンマを解決します。(soft policy ってのは、探索要素を取り入れた確率的方策って意味なのかな??初めて聞いた。次の行でまさにそうって書いてた:thinking:)
This means that non-greedy actions are chosen with some probability. 
これは、**非貪欲なアクションが一定の確率で選択されること**を意味します。
These policies are referred to as 𝜖-greedy policies because they select random actions with a probability of 𝜖 and follow the optimal action with a probability of 1-𝜖. 
これらのポリシーは、確率𝜖でランダムなアクションを選択し、確率1-𝜖で最適なアクションに従うため、𝜖-貪欲ポリシーと呼ばれます。

<!-- ここまで読んだ -->

Since the probability of randomly selecting an action from the action space is 𝜖, the probability of choosing any specific non-optimal action is 𝜖/|A(𝑠)|. 
アクション空間からランダムにアクションを選択する確率が𝜖であるため、特定の非最適アクションを選択する確率は $\epsilon / |A(s)|$ です。
On the other hand, the probability of following the optimal action will always be slightly higher due to the 1 - 𝜖 probability of selecting it outright and the 𝜖/|A(𝑠)| probability of choosing it through sampling the action space:  
一方で、最適なアクションに従う確率は、直接選択する確率1 - 𝜖とアクション空間をサンプリングすることによって選択する確率𝜖/|A(𝑠)|のため、常にわずかに高くなります。

<!-- ここまで読んだ -->

_Off-policy methods offer a different solution to the exploration vs. exploitation problem. 
オフポリシー手法は、探索と活用の問題に対する異なる解決策を提供します。
While_ on-policy algorithms attempt to improve the same 𝜖-greedy policy used for exploration, off-policy approaches utilize two distinct policies: a behavior policy and a target policy. 
オンポリシーアルゴリズムが探索に使用される同じ𝜖-貪欲ポリシーを改善しようとする一方で、オフポリシーアプローチは、**行動ポリシーとターゲットポリシーという二つの異なるポリシーを利用**します。
The behavioral policy (denoted as 𝜋𝛽 ) is employed for exploration and episode generation, while the target or goal policy (denoted as 𝜋) is used for function estimation and improvement. 
行動ポリシー（𝜋𝛽と表記）は探索とエピソード生成に使用され、ターゲットまたは目標ポリシー（𝜋と表記）は関数推定と改善に使用されます。

The efficacy of this approach lies in the capacity of the target policy 𝜋 to attain a balanced perspective of the environment, enabling it to assimilate insights from the behavioral policy _𝑏, while_ concurrently capturing advantageous actions and seeking further improvements. 
このアプローチの有効性は、ターゲットポリシー $\pi$ が環境のバランスの取れた視点を得る能力にあり、行動ポリシー $\pi_{\beta}$ からの洞察を取り入れつつ、有利なアクションを捉え、さらなる改善を追求します。
Nevertheless, it is imperative to acknowledge that in off-policy learning, a distributional discrepancy arises between the target policy estimation and the sampled policy. 
しかし、**オフポリシー学習においては、ターゲットポリシーの推定とサンプリングされたポリシーの間に分布の不一致が生じることを認識することが重要**です。(うんうん:thinking:)
Consequently, a widely employed technique known as importance sampling is applied to address this disparity [28]. 
その結果、この不一致に対処するために、重要度サンプリングと呼ばれる広く使用される手法が適用されます[28]。

<!-- ここまで読んだ! -->

**2.3** **Typical RL algorithms**  
**2.3** **典型的なRLアルゴリズム**

Let’s briefly outline various types of RL algorithms and present their definitions. 
さまざまなタイプのRLアルゴリズムを簡単に概説し、それらの定義を示します。
At a high level, all standard RL algorithms follow a common learning loop: the agent engages with the MDP using M a behavior policy 𝜋𝛽 . 
**高いレベルでは、すべての標準RLアルゴリズムは共通の学習ループに従います**：エージェントは行動ポリシー $\pi_{\beta}$ を使用してMDPと関与します。
This behavior policy, which could or could not align with 𝜋 (𝑎|𝑠), leads the agent to observe the current state 𝑠𝑡, choose an action 𝑎𝑡, and then witness the subsequent state _𝑠𝑡_ +1 and the reward value 𝑟𝑡 = R(𝑠𝑡,𝑎𝑡 ). 
この行動ポリシーは、$\pi (a|s)$ と一致する場合もあればしない場合もあり、エージェントは現在の状態 $s_t$ を観察し、アクション $a_t$ を選択し、その後の状態 $s_{t+1}$ と報酬値 $r_t = R(s_t, a_t)$ を目撃します。
This sequence can repeat over multiple steps, allowing the agent to gather transitions {𝑠𝑡,𝑎𝑡,𝑠𝑡 +1,𝑟𝑡 }. 
このシーケンスは複数のステップで繰り返すことができ、エージェントは遷移 { $s_t, a_t, s_{t+1}, r_t$ } を収集できます。
These observed transitions are then used by the agent to adjust its policy, and this update process might incorporate earlier observed transitions as well. 
これらの観察された遷移は、**エージェントによってポリシーを調整するために使用され**、この更新プロセスには以前に観察された遷移も含まれる可能性があります。
We’ll denote the set of available transitions for policy updating as D = {(𝑠𝑡,𝑎𝑡,𝑠𝑡 +1,𝑟𝑡 )}. 
ポリシー更新のための利用可能な遷移の集合を $D = {(s_t, a_t, s_{t+1}, r_t)}$ と表します。

<!-- ここまで読んだ -->

**Q-learning [51] is an off-policy value-based learning scheme aimed at finding a target policy** that selects the best action:  
Q-learning [51]は、最適なアクションを選択するターゲットポリシーを見つけることを目的としたオフポリシーのvalue-basedな学習スキームです。
(value-basedってなんだろ??:thinking:)

$$
\pi(s) = \arg \max_a Q_\pi(s, a)
\tag{3}
$$  


Here, 𝑄𝑢 (𝑠,𝑎) represents the Q-value and applies to a discrete action space. 
ここで、 $Q_{u}(s, a)$ はQ-valueを表し、離散アクション空間に適用されます。
For deterministic policies, the Q-value can be computed as:  
決定論的ポリシーの場合、Q値は次のように計算できます。

$$
Q(s_t, a_t) = E_{\tau \sim \pi} \left[ r(s_t, a_t) + \gamma Q(s_{t+1}, a_{t+1}) \right].
\tag{4}
$$  

Deep Q learning (DQN) [38] employs deep learning to approximate a nonlinear Q function parameterized by 𝜃𝑞: 𝑄𝜃𝑞 (𝑠,𝑎). 
**Deep Q学習（DQN）[38]は、深層学習を用いて、パラメータ $\theta_q$ によってパラメータ化された非線形Q関数 $Q_{\theta_q} (s, a)$ を近似**します。
(policy-value期待値の予測値が一番高くなるようなアクションを選ぶ = Q学習?? :thinking:)
DQN involves a network 𝑄𝜃𝑞 that’s updated asynchronously by minimizing the Mean Squared Error (MSE) as defined by:  
DQNは、平均二乗誤差（MSE）を最小化することによって非同期に更新されるネットワーク $Q_{\theta_q}$ を含みます。

$$
L(\theta_q) = E_{\tau \sim \pi} \left[ Q_{\theta_q}(s_t, a_t) - (r(s_t, a_t) + \gamma Q_{\theta_q}(s_{t+1}, a_{t+1})) \right]^2.
\tag{5}
$$

In this equation, 𝜏 signifies a sampled trajectory including (𝑠,𝑎,𝑠[′],𝑟 (𝑠,𝑎)). 
この方程式では、 $\tau$ は ( $s, a, s', r(s, a)$ ) を含むサンプリングされた軌道を示します。
Notably, 𝑠𝑡[′] [and][ 𝑎]𝑡[′] originate from the behavior policy 𝜋𝑏, while 𝑠,𝑎 come from the target policy 𝜋. 
特に、 $s_{t}'$ と $a_{t}'$ は行動ポリシー $\pi_{b}$ から派生し、 $s, a$ はターゲットポリシー $\pi$ から来ます。

<!-- ここまで読んだ -->

Furthermore, the concept of **value functions** plays a role. 
さらに、価値関数の概念が役割を果たします。
(value function = 方策性能の予測関数 = Q関数、みたいなイメージ??:thinking:)
These assess states and actions. 
これらは状態とアクションを評価します。
The value function 𝑉𝜋 (𝑠) evaluates states, and 𝑄𝜋 (𝑠𝑡,𝑎𝑡 ) evaluates actions. 
価値関数 $V_{\pi} (s)$ は状態を評価し、 $Q_{\pi} (s_t, a_t)$ はアクションを評価します。
The relationship between them is given by:  
それらの関係は次のように示されます。

$$
V_\pi(s) = E_{a \sim \pi} [Q_\pi(s, a)].
\tag{6}
$$  

The value function gets updated via the Temporal Difference (TD) method:  
価値関数は時間差（TD）法によって更新されます。

$$
V_\pi(s_t) \leftarrow V_\pi(s_t) + \alpha \left[ r(s_{t+1}, a_{t+1}) + \gamma V_\pi(s_{t+1}) - V_\pi(s_t) \right].
\tag{7}
$$  

where 𝛼 represents the learning rate.  
ここで、𝛼は学習率を表します。

<!-- ここまで読んだ -->

**Policy gradient [52] is a technique used in reinforcement learning that tackles scenarios** where actions are high-dimensional or continuous—something not easily managed by Q-learning.  
ポリシー勾配[52]は、**アクションが高次元または連続であるシナリオに対処するために強化学習で使用される手法**です。これはQ学習では簡単に管理できないものです。(アクションが高次元って、ベクトルっぽいアクションってこと??:thinking:)
Unlike Q-learning, which focuses on finding optimal actions, policy gradient aims to find optimal parameters 𝜃 for a policy 𝜋𝜃 in order to maximize the total reward.  
最適なアクションを見つけることに焦点を当てるQ学習とは異なり、ポリシー勾配は、**総報酬を最大化するためにポリシー $\pi_{\theta}$ の最適なパラメータ $\theta$ を見つけることを目的**としています。(うんうん...!:thinking:)
The central goal of policy gradient is to maximize the expected return, or accumulated reward, starting from the initial state.  
ポリシー勾配の中心的な目標は、初期状態から始まる期待リターンまたは累積報酬を最大化することです。
This is captured by the equation:  
これは次の方程式で表されます。

$$
J(\pi_{\theta}) = E_{\tau \sim \pi_{\theta}} [r(\tau)]
= \inf \pi_{\theta}(\tau) r(\tau) d\tau.
\tag{8}
$$

Here, 𝜋𝜃 (𝜏) signifies the probability of observing trajectory 𝜏.  
ここで、 $\pi_{\theta} (\tau)$ は軌道 $\tau$ を観察する確率を意味します。(=軌跡つまりアクション配列の選択確率分布みたいなイメージ...!:thinking:)
The technique learns the optimal parameter 𝜃 by computing the gradient ∇𝜃 _𝐽_ (𝜋𝜃 ) as follows:  
この手法は、次のように勾配 $\nabla_\theta J(\pi_\theta)$ を計算することによって最適なパラメータ $\theta$ を学習します。

$$
\nabla_\theta J(\pi_\theta) = E_{\tau \sim d_\pi} [\sum_{t=1}^{T} r(s_t, a_t) \sum_{t=1}^{T} \nabla_\theta \log \pi_\theta(s_t, a_t)].
\tag{9}
$$

In the above equation, 𝑑𝜋𝜃 is the distribution of trajectories generated by policy 𝜋𝜃.  
上記の方程式では、 $d_{\pi_\theta}$ はポリシー $\pi_\theta$ によって生成された軌道の分布です。

The derivation involves the substitution:  
導出には次の置換が含まれます。

$$
\pi_\theta(\tau) = p(s_1) \prod_{t=1}^{T} \pi_\theta(s_t, a_t) p(s_{t+1}|s_t, a_t).
$$
(軌跡 $tau$ は状態sと選ばれるアクションaの同時確率だから、prod記号を用いた確率質量の積で表される!:thinking:)

Here, 𝑝 (·) is independent of the policy parameter 𝜃, and for simplicity, it’s not explicitly included in the derivation.  
ここで、$p(·)$ はポリシーパラメータ $\theta$ とは独立した確率分布であり、簡単のために導出には明示的に含まれていません。

Prior policy gradient algorithms, like REINFORCE, have often used Monte-Carlo sampling to estimate 𝜏 from 𝑑𝜋𝜃.  
以前のポリシー勾配アルゴリズム、例えばREINFORCEは、モンテカルロサンプリングを使用して $d_{\pi_\theta}$ から $\tau$ を推定することがよくありました。(REINFORCEは勾配ベースアプローチなのか...!:thinking:)

<!-- ここまで読んだ -->

**Actor-critic networks bring together the strengths of both Q-learning and policy gradient** techniques.  
**アクター-クリティックネットワーク**は、Q学習とポリシー勾配の両方の強みを組み合わせます。(actor-criticネットワーク初めて聞いた...!:thinking:)
They can function as either on-policy methods [26] or off-policy methods [12].  
これらは、オンポリシー手法[26]またはオフポリシー手法[12]として機能できます。
An actor-critic network is composed of two key components:  
アクター-クリティックネットワークは、**二つの主要なコンポーネント**で構成されています。

- The actor: This component optimizes the policy 𝜋𝜃 based on the guidance provided by ∇𝜃 _𝐽_ (𝜋𝜃 ).  
  - アクター：このコンポーネントは、$\nabla_\theta J(\pi_\theta)$ によって提供されるガイダンスに基づいてポリシー $\pi_\theta$ を最適化します。
- The critic: The critic evaluates the learned policy 𝜋𝜃 using the Q-value function 𝑄𝜃𝑞 (𝑠,𝑎).  
  - クリティック：クリティックは、Q値関数 $Q_{\theta_q} (s, a)$ を使用して学習されたポリシー $\pi_\theta$ を評価します。

The overall gradient expression for an actor-critic network is as follows:  
アクター-クリティックネットワークの全体的な勾配表現は次のようになります。

$$
E_{s \sim d_\pi_{\theta}} [Q_{\theta_q}(s, a) \nabla_\theta \log \pi_\theta(s, a)].
$$  

In the case of off-policy learning, the value function for 𝜋𝜃 (𝑎|𝑠) can be further defined using deterministic policy gradient (DPG):  
オフポリシー学習の場合、 $\pi_\theta (a|s)$ の価値関数は、決定論的ポリシー勾配（DPG）を使用してさらに定義できます。

$$
E_{s \sim d_\pi_{\theta}} [\nabla_{a} Q_{\theta_q}(s, a) | a= \pi \theta(s) \nabla_\theta \pi_\theta(s, a)].
\tag{12}
$$

It’s worth noting that while traditional policy gradient calculations involve integrating over both the state space and the action space, DPG only requires integrating over the state space.  
伝統的なポリシー勾配計算が状態空間とアクション空間の両方にわたって積分するのに対し、DPGは状態空間にわたってのみ積分することが必要であることに注意する価値があります。
In S A S DPG, given a state 𝑠 ∈S, there corresponds only one action 𝑎 ∈A such that 𝜇𝜃 (𝑠) = 𝑎.  
S A S DPGにおいて、状態𝑠 ∈Sが与えられると、対応するアクション𝑎 ∈Aはただ一つであり、𝜇𝜃 (𝑠) = 𝑎となります。

<!-- ここまで読んだ! よくわかってない -->

**Model-based RL is a broad term encompassing methods that rely on explicit estimates of the** transition or dynamics function.  
**モデルベースのRL**は、遷移または動的関数の明示的な推定に依存する手法を含む広範な用語です。
The distinguishing feature of model-based RL is that it assumes P the dynamics model is known and can be learned.  
モデルベースのRLの特徴は、動的モデルPが知られており、学習可能であると仮定することです。
This is in contrast to other forms of RL where P such a dynamics model is neither known nor learnable.  
これは、他の形式のRLにおいて、Pのような動的モデルが知られておらず、学習可能でないことと対照的です。
強化学習
**2.4** **Offline RL**  
**2.4** **オフラインRL**

The offline RL problem can be defined as a data-driven formulation of the RL problem [27].  
オフラインRLの問題は、RL問題のデータ駆動型定式化として定義できます[27]。

The ultimate objective remains centered on optimizing the goal presented in Equation (2).  
最終的な目的は、方程式（2）で示された目標を最適化することにあります。

Notably, the agent’s capacity to engage with the environment and amass supplementary transitions using the behavior policy is nullified.  
特に、エージェントが環境と関わり、行動ポリシーを使用して追加の遷移を蓄積する能力は無効化されます。

Instead, the learning algorithm receives a fixed collection of transitions denoted as D = {𝑠𝑡[𝑖][,𝑎][𝑖]𝑡[,𝑠]𝑡[𝑖] +1[,𝑟]𝑡[𝑖] [}][, and its task is to acquire the most optimal policy using this provided] dataset.  
代わりに、学習アルゴリズムはD = {𝑠𝑡[𝑖][,𝑎][𝑖]𝑡[,𝑠]𝑡[𝑖] +1[,𝑟]𝑡[𝑖]}として示される固定された遷移のコレクションを受け取り、この提供されたデータセットを使用して最適なポリシーを取得することがそのタスクです。

This approach aligns more closely with the supervised learning paradigm, and we can view as the training dataset for the policy.  
このアプローチは、監視学習のパラダイムにより密接に一致し、ポリシーのトレーニングデータセットとして見ることができます。

Fundamentally, offline RL necessitates that the learning algorithm comprehends the underlying dynamics of the MDP M solely from a fixed dataset.  
基本的に、オフラインRLは、学習アルゴリズムが固定されたデータセットからのみMDP Mの基礎となる動的を理解することを必要とします。

Subsequently, it must create a policy 𝜋 (𝑎|𝑠) that achieves the highest cumulative reward during the interaction with the MDP.  
その後、MDPとのインタラクション中に最高の累積報酬を達成するポリシー𝜋 (𝑎|𝑠)を作成しなければなりません。

We will denote the distribution over states and actions in D as 𝜋𝛽 (also referred to as the behavior policy).  
Dにおける状態とアクションの分布を𝜋𝛽（行動ポリシーとも呼ばれます）として表記します。

Here, we assume that state-action pairs (𝑠,𝑎) ∈D are drawn from 𝑠 ∼ _𝑑[𝜋][𝛽]_ (𝑠), and actions are sampled according to the behavior policy, i.e., 𝑎 ∼ _𝜋𝛽_ (𝑎|𝑠).  
ここでは、状態-アクションペア(𝑠,𝑎) ∈Dが𝑠 ∼ _𝑑[𝜋][𝛽]_ (𝑠)から引き出され、アクションは行動ポリシーに従ってサンプリングされると仮定します。すなわち、𝑎 ∼ _𝜋𝛽_ (𝑎|𝑠)です。

This problem formulation has been expressed using a range of terminologies.  
この問題定式化は、さまざまな用語を使用して表現されています。

Within the field of RS, the term that frequently induces confusion is “off-policy RL”.  
RSの分野において、しばしば混乱を引き起こす用語は「オフポリシーRL」です。

This phrase is commonly employed as a broad label encompassing all RL algorithms that can leverage datasets of transitions, wherein the actions in each transition were acquired using policies distinct from the current D policy 𝜋 (𝑎|𝑠).  
このフレーズは、遷移のデータセットを活用できるすべてのRLアルゴリズムを包括する広範なラベルとして一般的に使用され、各遷移のアクションは現在のDポリシー𝜋 (𝑎|𝑠)とは異なるポリシーを使用して取得されました。

However, it’s important to note that the term “off-policy” typically signifies an RL algorithm where the behavior policy 𝜋𝛽 differs from the target policy 𝜋, as discussed earlier.  
ただし、「オフポリシー」という用語は、通常、行動ポリシー𝜋𝛽がターゲットポリシー𝜋と異なるRLアルゴリズムを意味することに注意することが重要です。

This distinction can sometimes cause confusion.  
この区別は時に混乱を引き起こすことがあります。

Hence, the terms “fully off-policy RL” or “offline RL” are recently introduced to indicate situations where no additional online data collection takes place.  
したがって、「完全オフポリシーRL」または「オフラインRL」という用語が最近導入され、追加のオンラインデータ収集が行われない状況を示します。

We have presented various illustrations of distinct RL approaches to emphasize the disparities between them in Figure 2.  
私たちは、図2においてそれらの間の違いを強調するために、異なるRLアプローチのさまざまな例を示しました。

rollout data {(st, at, st+1, rt )}  
ロールアウトデータ {(st, at, st+1, rt )}

Buffer  
バッファ

_πt+1_  
_πt+1_

**(a) on-policy RL4RS**  
**(a) オンポリシーRL4RS**

**(b) off-policy RL4RS**  
**(b) オフポリシーRL4RS**

rollout data {(st, at, st+1, rt )}  
ロールアウトデータ {(st, at, st+1, rt )}

_πt+1_  
_πt+1_

|Col1|Col2|Col3|  
|---|---|---|  
|Reward r t … State s t Policy πt … Reward implies User u Action a t|  
|Update Policy πt+1|  
|Offline Dataset|  
|Reward implies User u Action at|  
|Data Collection: data collected once with any policy|  

|Col2|Col3|  
|---|---|  
|Offline Dataset Learn Policy π|  
|Reward r t … State s t Policy π … Reward implies User u Action a t|  
|Reward r t … State s t Policy π … Reward implies User u Action a t|  

Training phase  
トレーニングフェーズ

**(c) offline RL4RS**  
**(c) オフラインRL4RS**

User u Action at  
ユーザーu アクションat

Deployment/Fine-tune  
デプロイ/ファインチューニング

Fig. 2. Illustration of classic on-policy RL (a), classic off-policy RL (b), and offline RL (c).  
図2. 古典的なオンポリシーRL (a)、古典的なオフポリシーRL (b)、およびオフラインRL (c)の図示。

The challenge of offline RL can be tackled through algorithms belonging to any of the four main categories in RL: Q-learning, policy gradient, actor-critic, and model-based RL.  
オフラインRLの課題は、RLの四つの主要カテゴリのいずれかに属するアルゴリズムを通じて対処できます：Q学習、ポリシー勾配、アクター-クリティック、モデルベースのRL。

In principle, any off-policy RL algorithm could function as an offline RL approach when the online interaction process is excluded.  
原則として、オンラインインタラクションプロセスが除外されると、任意のオフポリシーRLアルゴリズムはオフラインRLアプローチとして機能する可能性があります。

For instance, a straightforward offline RL technique can be created by employing Q-learning without requiring supplementary online exploration.  
例えば、追加のオンライン探索を必要とせずにQ学習を使用することで、簡単なオフラインRL手法を作成できます。

This method utilizes the dataset D to pre-fill the data buffer.  
この手法は、データセットDを使用してデータバッファを事前に埋めます。

**2.5** **Offline RL4RS - Problem Formulation**  
**2.5** **オフラインRL4RS - 問題定式化**

In this section, we establish a problem formulation for Offline RL4RS.  
このセクションでは、オフラインRL4RSの問題定式化を確立します。

We begin with a standard MDP framework, commonly used in RS.  
RSで一般的に使用される標準MDPフレームワークから始めます。

The setup involves a set of users denoted as U = 𝑢,𝑢1,𝑢2,𝑢3, ...  
この設定には、ユーザーの集合U = 𝑢,𝑢1,𝑢2,𝑢3, ...が含まれます。

and a set of items denoted as I = 𝑖,𝑖1,𝑖2,𝑖3, ....  
アイテムの集合I = 𝑖,𝑖1,𝑖2,𝑖3, ...が含まれます。

The process begins with the system recommending item 𝑖 to user 𝑢 and receiving feedback 𝑓𝑖[𝑢][.  
プロセスは、システムがユーザー𝑢にアイテム𝑖を推薦し、フィードバック𝑓𝑖[𝑢]を受け取ることから始まります。

This feedback is then utilized to enhance future recommendations, leading to the identification of an optimal policy 𝜋 [∗] that guides the selection of items to recommend in order to achieve positive feedback.  
このフィードバックは、将来の推薦を向上させるために利用され、ポジティブなフィードバックを得るために推薦するアイテムの選択を導く最適ポリシー𝜋 [∗]の特定につながります。

The MDP framework treats the user as the environment while the system acts as the agent.  
MDPフレームワークは、ユーザーを環境として扱い、システムをエージェントとして機能させます。

The fundamental components within the MDP context, especially in Deep Reinforcement Learning (DRL)-based RS, include:  
MDPの文脈内の基本的なコンポーネント、特に深層強化学習（DRL）ベースのRSには以下が含まれます。

- State S: At a given time 𝑡, the state 𝑠𝑡 ∈S is defined by a combination of the user’s characteristics and the recent 𝑙 items that the user has shown interest in prior to time 𝑡.  
- 状態S：ある時点𝑡において、状態𝑠𝑡 ∈Sは、ユーザーの特性と、ユーザーが時点𝑡の前に興味を示した最近の𝑙アイテムの組み合わせによって定義されます。

This may also include demographic information if relevant.  
これには、関連する場合、人口統計情報も含まれる可能性があります。

- Action A: The action 𝑎𝑡 ∈A represents the agent’s prediction of the user’s evolving preferences at time 𝑡.  
- アクションA：アクション𝑎𝑡 ∈Aは、エージェントが時点𝑡におけるユーザーの進化する好みを予測することを表します。

Here, A encompasses the entire set of potential candidate items, which could be vast, potentially numbering in the millions.  
ここで、Aは、数百万に及ぶ可能性のあるすべての候補アイテムの集合を含みます。

- Transition Probability P: The transition probability 𝑝 (𝑠𝑡 +1|𝑠𝑡,𝑎𝑡 ) quantifies the likelihood of transitioning from state 𝑠𝑡 to 𝑠𝑡 +1 when the agent performs action 𝑎𝑡 .  
- 遷移確率P：遷移確率𝑝 (𝑠𝑡 +1|𝑠𝑡,𝑎𝑡)は、エージェントがアクション𝑎𝑡を実行したときに状態𝑠𝑡から𝑠𝑡 +1に遷移する可能性を定量化します。

In the context of a recommender system, this probability corresponds to the likelihood of user behavior changes.  
推薦システムの文脈において、この確率はユーザーの行動変化の可能性に対応します。

- Reward function R: After the agent selects an appropriate action 𝑎𝑡 based on the current state 𝑠𝑡 at time 𝑡, the user receives the item recommended by the agent.  
- 報酬関数R：エージェントが時点𝑡における現在の状態𝑠𝑡に基づいて適切なアクション𝑎𝑡を選択した後、ユーザーはエージェントによって推薦されたアイテムを受け取ります。

The feedback from the user regarding the recommended item contributes to the reward 𝑟𝑡 = R(𝑠𝑡,𝑎𝑡 ).  
推薦されたアイテムに関するユーザーからのフィードバックは、報酬𝑟𝑡 = R(𝑠𝑡,𝑎𝑡)に寄与します。

This reward reflects the user’s response and guides the enhancement of the learned policy 𝜋 by the recommendation agent.  
この報酬はユーザーの反応を反映し、推薦エージェントによる学習したポリシー𝜋の向上を導きます。

- Discount Factor 𝛾: The discount factor 𝛾 ∈[0, 1] is employed to balance the consideration of future and immediate rewards.  
- 割引因子𝛾：割引因子𝛾 ∈[0, 1]は、将来の報酬と即時の報酬の考慮をバランスさせるために使用されます。

A value of 𝛾 = 0 indicates the agent prioritizes immediate rewards, while a non-zero value implies a blend of both immediate and future rewards.  
𝛾 = 0の値は、エージェントが即時の報酬を優先することを示し、非ゼロの値は即時の報酬と将来の報酬の両方のブレンドを示唆します。

- Offline Dataset D: The offline dataset D is amassed by an unknown behavior policy 𝜋𝛽 .  
- オフラインデータセットD：オフラインデータセットDは、未知の行動ポリシー𝜋𝛽によって収集されます。

This dataset serves as the historical records of user interactions and is utilized to improve the recommendation policy.  
このデータセットは、ユーザーインタラクションの履歴記録として機能し、推薦ポリシーの改善に利用されます。

This MDP-based framework lays the groundwork for Offline RL4RS, where the aim is to devise effective recommendation policies using historical interaction data, even when the data is collected under an unknown or different behavior policy.  
このMDPベースのフレームワークは、オフラインRL4RSの基盤を築き、目標は、未知または異なる行動ポリシーの下で収集されたデータであっても、歴史的インタラクションデータを使用して効果的な推薦ポリシーを考案することです。

If a POMDP is used, we just need to add the observation O which is the partial information from users and 𝑙 items in which the user was interested before time 𝑡.  
POMDPが使用される場合、ユーザーからの部分的な情報と、ユーザーが時点𝑡の前に興味を持っていた𝑙アイテムに関する観測Oを追加するだけです。

Definition 3. Given an offline dataset D, which contains the trajectories when user 𝑢 ∈U _interacts with the system for a certain period with an unknown behavior policy 𝜋𝛽_ _, the RL agent aims_ _to learn a policy 𝜋_ _from the offline dataset D.  
定義3. オフラインデータセットDが与えられた場合、これはユーザー𝑢 ∈Uが未知の行動ポリシー𝜋𝛽でシステムと一定期間相互作用する際の軌道を含み、RLエージェントはオフラインデータセットDからポリシー𝜋を学習することを目指します。

After that, the trained policy 𝜋_ _will be deployed/tested_ _on a production or evaluation environment with a similar scenario with the collected dataset D._  
その後、学習したポリシー𝜋は、収集されたデータセットDを用いた類似のシナリオで本番または評価環境にデプロイ/テストされます。



## 3 CURRENT PROGRESS IN OFFLINE RL4RS
## 3 現在のオフラインRL4RSの進展

In this section, we survey offline RL-based RS. 
このセクションでは、オフラインRLに基づく推薦システム（RS）を調査します。

Generally speaking, it can be divided into two categories: off-policy with logged data (i.e., “full” off-policy) and offline RL. 
一般的に、オフラインRLは、ログデータを用いたオフポリシー（すなわち「完全」オフポリシー）とオフラインRLの2つのカテゴリに分けることができます。

These two concepts are generally the same except for some specific settings in off-policy methods such as assuming bandit conditions. 
これら2つの概念は、バンディット条件を仮定するなど、オフポリシー手法の特定の設定を除いて、一般的には同じです。

Due to the recent introduction of offline RL, we have opted to distinguish and separate these for clarity and to prevent potential confusion. 
最近のオフラインRLの導入により、明確さを保ち、潜在的な混乱を防ぐために、これらを区別して分けることにしました。

**3.1 Off-policy with Logged Data**
**3.1 ログデータを用いたオフポリシー**

_3.1.1 Off-policy Evaluation. The typical method in this domain is known as off-policy evaluation._ 
_3.1.1 オフポリシー評価。この分野の典型的な手法は、オフポリシー評価として知られています。_

Off-policy evaluation methods are rooted in the direct estimation of policy returns. 
オフポリシー評価手法は、ポリシーリターンの直接的な推定に基づいています。

These methods often utilize a technique known as importance sampling, which involves estimating the return of a given policy or approximating the corresponding policy gradient. 
これらの手法は、特定のポリシーのリターンを推定するか、対応するポリシー勾配を近似する重要度サンプリングと呼ばれる手法を利用することがよくあります。

A straightforward application of importance sampling involves using trajectories sampled from 𝜋𝛽 (𝜏) to derive an unbiased estimator of 𝐽 (𝜋):  
重要度サンプリングの簡単な適用は、𝜋𝛽 (𝜏) からサンプリングされた軌跡を使用して、𝐽 (𝜋) の無偏推定量を導出することを含みます：

$$
\hat{J}(\pi) = \sum_{t=0}^{T} \gamma[t] R(s, a) = E_{\tau \sim \pi_\beta} \left[ \sum_{t=0}^{T} \frac{\pi_\theta(a_t | s_t)}{\pi_\beta(s_t | a_t)} R(s, a) \right]
$$

However, this estimator often exhibits high variance, particularly if _𝑇_ (the time horizon) is large, due to the product of importance weights. 
しかし、この推定量は、重要度重みの積のために、特に _𝑇_（時間の地平線）が大きい場合に高い分散を示すことがよくあります。

To address this, a weighted importance sampling estimator can be used. 
これに対処するために、重み付き重要度サンプリング推定量を使用することができます。

This involves dividing the weights by $n$ to normalize them, resulting in a biased estimator with significantly lower variance, while still maintaining strong consistency. 
これは、重みを $n$ で割って正規化することを含み、バイアスのある推定量を生成しますが、分散は大幅に低く、強い一貫性を維持します。

When considering the estimation of Q-values for each state-action pair (𝑠𝑡,𝑎𝑡 ), denoted as _𝑄ˆ_ _[𝜋]_ (𝑠𝑡,𝑎𝑡 ), an approximate model comes into play. 
各状態-行動ペア (𝑠𝑡,𝑎𝑡) のQ値の推定を考慮する際、_𝑄ˆ_ _[𝜋]_ (𝑠𝑡,𝑎𝑡) として示される近似モデルが登場します。

This model could be derived from estimating the transition probability P(𝑠𝑡 +1|𝑠𝑡,𝑎𝑡 ) of the Markov Decision Process (MDP) and subsequently solving for the corresponding Q-function. 
このモデルは、マルコフ決定過程（MDP）の遷移確率 P(𝑠𝑡 +1|𝑠𝑡,𝑎𝑡) を推定し、その後、対応するQ関数を解くことから導出される可能性があります。

Alternatively, other methods for approximating Q-values could be employed. 
あるいは、Q値を近似するための他の手法を使用することもできます。

The integration of these approximated Q-values as control variates within the importance sampled estimator leads to an enhanced approach:  
これらの近似Q値を重要度サンプリング推定量内の制御変数として統合することで、強化されたアプローチが得られます：

$$
\hat{J}(\pi_\theta) = \sum_{t=0}^{T} \gamma[t] \left[ r_t[i] - \hat{Q}[\pi](s_t, a_t) \right] - w_t[i]^{-1} E_a \sim \pi_\theta \left[ \hat{Q}[\pi](s_t, a_t) \right]
$$

This method, referred to as a doubly robust estimator, exhibits unbiasedness either when _𝜋𝛽_ is known or when the model is accurate. 
この手法は、ダブリーロバスト推定量と呼ばれ、_𝜋𝛽_ が知られている場合やモデルが正確な場合に無偏性を示します。

In essence, it leverages both the unbiasedness of the importance sampling method and the approximated Q-values to produce an estimator with lower variance and strong consistency. 
本質的には、重要度サンプリング手法の無偏性と近似Q値の両方を活用して、分散が低く、一貫性の強い推定量を生成します。

_3.1.2 Recent works. The recent advancements in off-policy using logged data method can be_ broadly categorized into three distinct domains: estimator improvement (focus on the discrepancy between the offline data and online data), algorithmic improvement (focus on the recommendation algorithm itself), and miscellaneous application domains. 
_3.1.2 最近の研究。ログデータを使用したオフポリシーの最近の進展は、_推定量の改善（オフラインデータとオンラインデータの不一致に焦点を当てる）、アルゴリズムの改善（推薦アルゴリズム自体に焦点を当てる）、およびその他の応用分野_ の3つの異なる領域に大別できます。

We have compiled a summary of these works in Figure 3. 
これらの研究の概要を図3にまとめました。

**Estimator Improvement Hoiles and Schaar [18] focus on the problem of student course scheduling and curriculum design.** 
**推定量の改善 HoilesとSchaar [18] は、学生のコーススケジューリングとカリキュラム設計の問題に焦点を当てています。**

It proposes an algorithm for personalized course recommendation and curriculum design based on logged student data. 
これは、ログされた学生データに基づいて、パーソナライズされたコース推薦とカリキュラム設計のためのアルゴリズムを提案します。

The algorithm uses a regression estimator for contextual multi-armed bandits and provides guarantees on their predictive performance. 
このアルゴリズムは、文脈的マルチアームバンディットのための回帰推定量を使用し、その予測性能に関する保証を提供します。

The paper also addresses the issue of missing data and provides guidelines for including expert domain knowledge in the recommendations. 
この論文は、欠損データの問題にも対処し、推薦に専門家のドメイン知識を含めるためのガイドラインを提供します。

The algorithms can be used to identify curriculum gaps and provide recommendations for course schedules. 
これらのアルゴリズムは、カリキュラムのギャップを特定し、コーススケジュールの推奨を提供するために使用できます。

The paper also discusses off-policy evaluation techniques and the use of the regression estimator for estimating the expected reward of a new policy. 
この論文では、オフポリシー評価手法と新しいポリシーの期待報酬を推定するための回帰推定量の使用についても論じています。

One drawback is that the proposed approach assumes a fixed set of courses and does not consider the dynamic nature of course offerings and student preferences. 
1つの欠点は、提案されたアプローチが固定されたコースセットを仮定しており、コースの提供や学生の好みの動的な性質を考慮していないことです。

Swaminathan et al. [45] address the problem of off-policy evaluation and optimization in combinatorial contextual bandits. 
Swaminathanら [45] は、組合せ文脈バンディットにおけるオフポリシー評価と最適化の問題に取り組んでいます。

The motivation behind this research is the need to estimate the reward of a new target policy using data collected by a different logging policy. 
この研究の動機は、異なるログポリシーによって収集されたデータを使用して、新しいターゲットポリシーの報酬を推定する必要性です。

The authors propose a pseudoinverse (PI) estimator that makes a linearity assumption about the evaluated metric, allowing for more efficient estimation compared to importance sampling. 
著者らは、評価されたメトリックに関して線形性の仮定を行う擬似逆（PI）推定量を提案し、重要度サンプリングと比較してより効率的な推定を可能にします。

The PI estimator requires exponentially fewer samples to achieve a given error bound and can be used for off-policy optimization as well. 
PI推定量は、所定の誤差境界を達成するために指数的に少ないサンプルを必要とし、オフポリシー最適化にも使用できます。

The methodology involves using the PI estimator to impute action-level rewards for each context, enabling direct optimization of whole-page metrics through pointwise learning to rank algorithms. 
この方法論は、PI推定量を使用して各コンテキストのアクションレベルの報酬を補完し、ポイントワイズ学習を通じて全ページメトリックの直接最適化を可能にします。

The authors demonstrate the effectiveness of their approach on real-world search ranking datasets, showing that the PI estimator outperforms prior baselines in terms of off-policy evaluation of whole-page metrics. 
著者らは、実世界の検索ランキングデータセットにおけるアプローチの有効性を示し、PI推定量が全ページメトリックのオフポリシー評価において以前のベースラインを上回ることを示しています。

This method has several limitations. 
この方法にはいくつかの制限があります。

One drawback of this method is that it relies on the linearity assumption, which may not always hold in practice. 
この方法の1つの欠点は、実際には常に成り立たない可能性のある線形性の仮定に依存していることです。

Moreover, there is a bias-variance tradeoff between the weighted pseudoinverse (wPI) method and the direct method, with wPI showing bias for the Expected Reciprocal Rank metric. 
さらに、重み付き擬似逆（wPI）法と直接法の間にはバイアス-分散のトレードオフがあり、wPIは期待逆順位メトリックに対してバイアスを示します。

The wPI method also deteriorates for larger slate spaces and is sensitive to linearity assumptions. 
wPI法は、より大きなスレート空間に対しても劣化し、線形性の仮定に敏感です。

These drawbacks highlight areas where further refinement and research are needed to enhance the robustness and effectiveness of the approach. 
これらの欠点は、アプローチの堅牢性と効果を高めるためにさらなる洗練と研究が必要な領域を浮き彫りにしています。

Jeunen and Goethals [21, 22] focus on improving the recommendation performance of policies that rely on value-based models (i.e., Q-learning) of expected reward. 
JeunenとGoethals [21, 22] は、期待報酬の価値ベースモデル（すなわちQ学習）に依存するポリシーの推薦性能を改善することに焦点を当てています。

The authors propose a pessimistic reward modeling framework that incorporates Bayesian uncertainty estimates to express skepticism about the reward model. 
著者らは、報酬モデルに対する懐疑心を表現するためにベイズ的不確実性推定を組み込んだ悲観的報酬モデリングフレームワークを提案します。

This allows for the generation of conservative decision rules based on lower-confidence-bound estimates, rather than the usual maximum likelihood or maximum PI estimates. 
これにより、通常の最尤推定や最大PI推定ではなく、下限信頼区間推定に基づく保守的な意思決定ルールを生成することが可能になります。

The approach is agnostic to the logging policy and does not require propensity scores, making it more flexible and avoiding the limitations of inverse propensity score weighting. 
このアプローチは、ログポリシーに依存せず、傾向スコアを必要としないため、より柔軟であり、逆傾向スコア重み付けの制限を回避します。

The methodology involves training reward models using a range of datasets generated under different environmental conditions. 
この方法論は、異なる環境条件下で生成されたさまざまなデータセットを使用して報酬モデルを訓練することを含みます。

The authors compare the performance of policies that act based on reward models using maximum likelihood or maximum PI estimates, with policies that use lower confidence bounds based on tuned parameters. 
著者らは、最大尤度または最大PI推定を使用して報酬モデルに基づいて行動するポリシーの性能を、調整されたパラメータに基づく下限信頼区間を使用するポリシーと比較します。

The evaluation is done through simulated A/B tests, with the resulting click-through-rate (CTR) estimates compared to the logging policy and an unattainable skyline policy. 
評価はシミュレーションされたA/Bテストを通じて行われ、得られたクリック率（CTR）推定はログポリシーおよび達成不可能なスカイラインポリシーと比較されます。

The experiments show that the pessimistic decision-making approach consistently decreases post-decision disappointment and can significantly increase the policy’s attained CTR. 
実験は、悲観的な意思決定アプローチが一貫して決定後の失望を減少させ、ポリシーの達成したCTRを大幅に増加させることを示しています。

One drawback of this approach is that it relies on the assumption that the reward estimates are conditionally unbiased, which may not always hold in practice. 
このアプローチの1つの欠点は、報酬推定が条件付きで無偏であるという仮定に依存していることであり、これは実際には常に成り立たない可能性があります。

The authors acknowledge that underfitting and model misspecification can make this assumption unrealistic. 
著者らは、アンダーフィッティングやモデルの誤指定がこの仮定を非現実的にする可能性があることを認めています。

Additionally, the approach requires tuning the hyperparameter alpha, which determines the lower confidence bound, and finding the optimal value may not always be straightforward. 
さらに、このアプローチは、下限信頼区間を決定するハイパーパラメータαの調整を必要とし、最適な値を見つけることは常に簡単ではないかもしれません。

Narita et al. [39] proposes a new off-policy evaluation method for RL4RS. 
Naritaら [39] は、RL4RSのための新しいオフポリシー評価手法を提案します。

The motivation behind this work is to address the limitations of existing estimators, such as inverse propensity weighting and doubly robust estimators, which suffer from bias and overfitting issues. 
この研究の動機は、逆傾向重み付けやダブリーロバスト推定量などの既存の推定量の限界に対処することであり、これらはバイアスや過剰適合の問題に悩まされています。

The authors introduce a new estimator that combines the doubly robust estimator with double/debiased machine learning techniques. 
著者らは、ダブリーロバスト推定量とダブル/デバイアス機械学習技術を組み合わせた新しい推定量を導入します。

The key features of this estimator are its robustness to bias in behavior policy and state-action value function estimates, as well as the use of a sample-splitting procedure called cross-fitting to remove overfitting bias. 
この推定量の主な特徴は、行動ポリシーと状態-行動価値関数推定におけるバイアスに対する堅牢性、および過剰適合バイアスを除去するためのクロスフィッティングと呼ばれるサンプル分割手法の使用です。

However, the experiments are limited to specific domains, such as the CartPole-v0 environment and online ads, and it is unclear how the estimator would perform in other tasks in RS. 
しかし、実験はCartPole-v0環境やオンライン広告などの特定のドメインに制限されており、推定量がRSの他のタスクでどのように機能するかは不明です。

Jagerman et al. [20] address the problem of off-policy evaluation in non-stationary environments, where user preferences change over time. 
Jagermanら [20] は、ユーザーの好みが時間とともに変化する非定常環境におけるオフポリシー評価の問題に取り組んでいます。

Existing off-policy evaluation techniques fail to work in such environments. 
既存のオフポリシー評価手法は、そのような環境では機能しません。

It proposes several off-policy estimators that operate well in non-stationary environments. 
この研究は、非定常環境でうまく機能するいくつかのオフポリシー推定量を提案します。

These estimators rely more on recent bandit feedback and accurately capture changes in user preferences. 
これらの推定量は、最近のバンディットフィードバックにより依存し、ユーザーの好みの変化を正確に捉えます。

They provide a rigorous analysis of the proposed estimators’ bias and show that the bias does not grow over time, unlike the standard Inverse Propensity Scoring (IPS) estimator. 
彼らは、提案された推定量のバイアスに関する厳密な分析を提供し、バイアスが時間とともに増加しないことを示します。これは、標準の逆傾向スコアリング（IPS）推定量とは異なります。

They also create adaptive variants of the estimators that change their parameters in real-time to improve estimation performance. 
彼らはまた、推定性能を向上させるために、リアルタイムでパラメータを変更する推定量の適応型バリアントを作成します。

Extensive empirical evaluation on recommendation datasets shows that the proposed estimators significantly outperform the regular IPS estimator and provide a more accurate estimation of a policy’s true performance. 
推薦データセットに対する広範な実証評価は、提案された推定量が通常のIPS推定量を大幅に上回り、ポリシーの真の性能のより正確な推定を提供することを示しています。

One drawback of the work is the trade-off between bias and variance. 
この研究の1つの欠点は、バイアスと分散のトレードオフです。

While the estimators avoid a bias term that grows with time, they introduce variance that scales with the window size or decay factor. 
推定量は、時間とともに増加するバイアス項を回避しますが、ウィンドウサイズや減衰係数に応じてスケールする分散を導入します。

Choosing a smaller window size or larger decay factor reduces bias but increases variance, and vice versa. 
小さなウィンドウサイズや大きな減衰係数を選択するとバイアスが減少しますが、分散が増加し、その逆もまた然りです。

Finding the optimal balance between bias and variance is a challenge. 
バイアスと分散の最適なバランスを見つけることは課題です。

**Algorithmic Improvement Wang et al. [46] address the problem of designing a stable off-policy RL method for RS.** 
**アルゴリズムの改善 Wangら [46] は、RSのための安定したオフポリシーRL手法の設計の問題に取り組んでいます。**

Moreover, the exploration error is also highlighted, which arises from the mismatch between the recommendation policy and the distribution of customers’ feedback in the training data. 
さらに、探索エラーも強調されており、これは推薦ポリシーとトレーニングデータにおける顧客のフィードバックの分布との不一致から生じます。

This exploration error can lead to unstable training processes and potentially diverging results. 
この探索エラーは、不安定なトレーニングプロセスや潜在的に発散する結果を引き起こす可能性があります。

To mitigate this problem, the authors propose an off-policy logged data method called Generator Constrained deep Q-learning (GCQ). 
この問題を軽減するために、著者らはGenerator Constrained deep Q-learning（GCQ）と呼ばれるオフポリシーのログデータ手法を提案します。

GCQ combines a neural generator that simulates customers’ possible feedback with a Q-network that selects the highest valued action to form the recommendation policy. 
GCQは、顧客の可能なフィードバックをシミュレートするニューラルジェネレーターと、推薦ポリシーを形成するために最も価値のあるアクションを選択するQネットワークを組み合わせています。

The authors also design the generator’s architecture based on Huffman Trees to reduce decision time. 
著者らは、決定時間を短縮するために、Huffman Treesに基づいてジェネレーターのアーキテクチャを設計しています。

One drawback of this work is the limited capability to handle long sequences of user behavior. 
この研究の1つの欠点は、ユーザーの行動の長いシーケンスを処理する能力が限られていることです。

Chen et al. [5] address the problem of data biases that arise when applying policy gradient methods in a recommendation system. 
Chenら [5] は、推薦システムにおけるポリシー勾配法を適用する際に生じるデータバイアスの問題に取り組んでいます。

The primary goal is to address the distribution mismatch from the behavior policy 𝜋𝛽 and the learned policy 𝜋. 
主な目標は、行動ポリシー 𝜋𝛽 と学習されたポリシー 𝜋 からの分布の不一致に対処することです。

As a result, an off-policy-corrected gradient estimator is introduced to reduce the variance of each gradient term while still correcting for the bias of a non-corrected policy gradient. 
その結果、オフポリシー修正勾配推定量が導入され、各勾配項の分散を減少させつつ、修正されていないポリシー勾配のバイアスを修正します。

A recurrent neural network (RNN) is adopted to model the user state at each time step. 
再帰神経ネットワーク（RNN）が、各時間ステップでのユーザー状態をモデル化するために採用されます。

To estimate the behavior policy 𝜋𝛽, which is a mixture of the policies of multiple agents in the system, the authors use a context-dependent neural estimator which is a contextual bandit based method. 
システム内の複数のエージェントのポリシーの混合である行動ポリシー 𝜋𝛽 を推定するために、著者らは文脈依存のニューラル推定量を使用します。これは文脈的バンディットに基づく手法です。

One drawback of the proposed method is the variance of the estimator, which can be large when there are very low or high values of the importance weights. 
提案された方法の1つの欠点は、推定量の分散であり、重要度重みの値が非常に低いまたは高い場合に大きくなる可能性があります。

To reduce this variance, the authors take a first-order approximation and ignore the state visitation differences under the two policies. 
この分散を減少させるために、著者らは一次近似を行い、2つのポリシーの下での状態訪問の違いを無視します。

This results in a slightly biased estimator with a lower variance. 
これにより、分散が低いがわずかにバイアスのある推定量が得られます。

Another drawback is the difficulty in estimating the behavior policy 𝜋𝑏𝑒𝑡𝑎, especially when there are multiple agents in the system and the collected trajectories are generated by a mixture of deterministic policies and stochastic policies. 
もう1つの欠点は、行動ポリシー 𝜋𝑏𝑒𝑡𝑎 を推定することの難しさであり、特にシステム内に複数のエージェントが存在し、収集された軌跡が決定論的ポリシーと確率的ポリシーの混合によって生成される場合です。

Jeunen et al. [23] propose a new approach called the Dual Bandit, which combines value-based and policy-based methods to improve performance in recommendation settings. 
Jeunenら [23] は、推薦設定における性能を向上させるために、価値ベースとポリシーベースの手法を組み合わせたDual Banditと呼ばれる新しいアプローチを提案します。

It highlights that existing offline evaluation results are often even contradictory over different runs and datasets, or extremely hard to reproduce in a robust manner. 
既存のオフライン評価結果は、異なる実行やデータセット間で矛盾していることが多く、堅牢な方法で再現することが非常に難しいことを強調しています。

Hence, they introduce simulation environments as an alternative and reproducible evaluation approach. 
したがって、彼らは代替の再現可能な評価アプローチとしてシミュレーション環境を導入します。

**Others Sakhi et al. [41] introduce a probabilistic model known as BLOB (Bayesian Latent Organic Bandit) designed for bandit-based RS.** 
**その他 Sakhiら [41] は、バンディットベースのRSのために設計されたBLOB（ベイズ潜在有機バンディット）と呼ばれる確率モデルを導入します。**

BLOB aims to enhance recommendation quality by combining organic user behavior (items viewed without intervention) with bandit signals (recommendations and their outcomes). 
BLOBは、介入なしで表示されたアイテム（有機ユーザー行動）とバンディット信号（推薦とその結果）を組み合わせることで、推薦の質を向上させることを目指しています。

Traditional recommendation algorithms often focus on either organic-based or bandit-based approaches, but the authors recognize the potential to enhance recommendation quality by integrating both aspects. 
従来の推薦アルゴリズムは、有機ベースまたはバンディットベースのアプローチのいずれかに焦点を当てることが多いですが、著者らは両方の側面を統合することで推薦の質を向上させる可能性を認識しています。

The goal is to create a model that leverages the relationship between organic and bandit behaviors to provide more accurate and personalized recommendations. 
目標は、有機的行動とバンディット行動の関係を活用して、より正確でパーソナライズされた推薦を提供するモデルを作成することです。

The proposed model uses a matrix variate prior distribution to relate these two types of behaviors, and variational autoencoders are employed for training. 
提案されたモデルは、これら2つの行動タイプを関連付けるために行列変量事前分布を使用し、トレーニングには変分オートエンコーダーが使用されます。

However, the proposed model requires a two-state training process which needs to train the model for organic behavior and bandit signals separately instead of training simultaneously. 
しかし、提案されたモデルは、同時にトレーニングするのではなく、有機的行動とバンディット信号のためにモデルを別々にトレーニングする必要がある2状態のトレーニングプロセスを必要とします。

Xiao and Wang [55] present a value ranking algorithm that combines RL and ranking metrics to improve the effectiveness of ranking algorithms. 
XiaoとWang [55] は、RLとランキングメトリックを組み合わせてランキングアルゴリズムの効果を向上させる価値ランキングアルゴリズムを提案します。

The proposed method uses the concept of extrapolation and regularization to address the challenges of partial and sparse rewards. 
提案された方法は、部分的およびスパースな報酬の課題に対処するために、外挿と正則化の概念を使用します。

Extrapolation is used to estimate rewards from logged feedback, while regularization is used to incorporate ranking signals into the RL policy. 
外挿はログされたフィードバックから報酬を推定するために使用され、正則化はランキング信号をRLポリシーに組み込むために使用されます。

The authors propose a sequential Expectation-Maximization (EM) framework that alternates between the E-step, which estimates rewards and ranking signals, and the M-step, which optimizes the RL policy. 
著者らは、報酬とランキング信号を推定するEステップと、RLポリシーを最適化するMステップの間で交互に進む逐次的期待最大化（EM）フレームワークを提案します。

They show that this framework can effectively learn from rewards and ranking signals. 
彼らは、このフレームワークが報酬とランキング信号から効果的に学習できることを示しています。

This proposed algorithm’s drawback lies in the bandit setting, as it doesn’t account for future rewards. 
この提案されたアルゴリズムの欠点は、バンディット設定にあり、将来の報酬を考慮していないことです。

Additionally, in the full RL setting, it might suffer from the curse of dimensionality. 
さらに、完全なRL設定では、次元の呪いに悩まされる可能性があります。

Hong et al. [19] address the complex issue of multi-task off-policy learning from bandit feedback, a challenge that has significant implications for various applications, including RS. 
Hongら [19] は、バンディットフィードバックからのマルチタスクオフポリシー学習の複雑な問題に取り組んでおり、これはRSを含むさまざまなアプリケーションに重要な影響を与える課題です。

It is motivated to develop a solution that can efficiently handle multiple tasks simultaneously, leveraging the relationships between tasks to enhance performance. 
これは、タスク間の関係を活用してパフォーマンスを向上させるために、複数のタスクを同時に効率的に処理できるソリューションを開発することを目的としています。

It proposes a hierarchical off-policy optimization algorithm (HierOPO) to tackle this problem. 
この問題に対処するために、階層的オフポリシー最適化アルゴリズム（HierOPO）を提案します。

The problem is formulated as a contextual off-policy optimization within a hierarchical graphical model, specifically focusing on linear Gaussian models. 
この問題は、階層的グラフィカルモデル内の文脈的オフポリシー最適化として定式化され、特に線形ガウスモデルに焦点を当てています。

The authors provide an efficient implementation and analysis, proving per-task bounds on the sub-optimality of the learned policies. 
著者らは、効率的な実装と分析を提供し、学習されたポリシーのサブ最適性に関するタスクごとの境界を証明します。

They demonstrate that using the hierarchy improves performance compared to solving each task independently. 
彼らは、階層を使用することで、各タスクを独立に解決するよりもパフォーマンスが向上することを示しています。

The algorithm is evaluated on synthetic problems and applied to a multi-user recommendation system. 
このアルゴリズムは、合成問題で評価され、マルチユーザー推薦システムに適用されます。

However, the proposed method is a model-based off-policy approach, the model-based approaches tend to be biased, due to using a potentially misspecified model. 
しかし、提案された方法はモデルベースのオフポリシーアプローチであり、モデルベースのアプローチは、潜在的に誤指定されたモデルを使用するため、バイアスがかかる傾向があります。

**3.2 Offline RL4RS**
**3.2 オフラインRL4RS**

In this section, we will provide reviews of existing offline RL4RS methods. 
このセクションでは、既存のオフラインRL4RS手法のレビューを提供します。

Different from off-policy evaluation, offline RL4RS does not limit the setting to bandit-based methods. 
オフポリシー評価とは異なり、オフラインRL4RSは設定をバンディットベースの手法に制限しません。

Moreover, in this part, we have included the off-policy learning based methods as offline RL. 
さらに、この部分では、オフポリシー学習に基づく手法をオフラインRLとして含めています。

However, the existing works in this field lack organization, with no apparent interconnection among the various works that often emphasize different aspects. 
しかし、この分野の既存の研究は組織化されておらず、さまざまな研究の間に明らかな相互接続がなく、しばしば異なる側面を強調しています。

Currently, we lack a systematic approach to review these works, resorting to a sequential examination of each one individually. 
現在、これらの研究をレビューするための体系的なアプローチが欠けており、各研究を個別に順次検討することに頼っています。

Ma et al. [33] discuss off-policy learning in two-stage RS. 
Maら [33] は、2段階のRSにおけるオフポリシー学習について論じています。

The proposed method consists of a candidate generation model in the first stage and a ranking model in the second stage. 
提案された方法は、第一段階で候補生成モデル、第二段階でランキングモデルから構成されています。

The authors propose a two-stage off-policy policy gradient method that takes into account the ranking model when training the candidate generation model. 
著者らは、候補生成モデルを訓練する際にランキングモデルを考慮に入れた2段階のオフポリシーポリシー勾配法を提案します。

The proposed method employs IPS to correct the bias and design variance reduction tricks to reduce the variance. 
提案された方法は、バイアスを修正するためにIPSを使用し、分散を減少させるための分散削減トリックを設計します。

However, the proposed method does not provide a comprehensive experiment about how the ranking model and the candidate generation model affect the final performance. 
しかし、提案された方法は、ランキングモデルと候補生成モデルが最終的なパフォーマンスにどのように影響するかについての包括的な実験を提供していません。

Chen et al. [6] focus on scaling an off-policy actor-critic algorithm for industrial recommendation systems. 
Chenら [6] は、産業用推薦システムのためのオフポリシーアクター-クリティックアルゴリズムのスケーリングに焦点を当てています。

The motivation behind their research is to address the challenges of offline evaluation and learning in RS, where only partial feedback is available. 
彼らの研究の動機は、オフライン評価とRSにおける学習の課題に対処することであり、ここでは部分的なフィードバックしか利用できません。

The authors propose an approach that combines off-policy learning with importance weighting to estimate the value of state-action pairs under the target policy. 
著者らは、オフポリシー学習と重要度重み付けを組み合わせて、ターゲットポリシーの下での状態-行動ペアの価値を推定するアプローチを提案します。

They use a critic network to estimate the value function and update the policy network accordingly. 
彼らは、価値関数を推定するためにクリティックネットワークを使用し、それに応じてポリシーネットワークを更新します。

The methodology involves minimizing the temporal difference loss and using a Huber loss to handle outliers. 
この方法論は、時間差損失を最小化し、外れ値を処理するためにハイバーロスを使用することを含みます。

The authors also investigate the impact of different estimation methods for the target value function. 
著者らは、ターゲット価値関数の異なる推定手法の影響も調査します。

However, the proposed methods have several limitations. 
しかし、提案された方法にはいくつかの制限があります。

One drawback is the potential bias introduced by using the cumulative future return on the behavior trajectory while ignoring the importance weighting on future trajectories. 
1つの欠点は、将来の軌跡に対する重要度重み付けを無視しながら、行動軌跡の累積未来リターンを使用することによって導入される可能性のあるバイアスです。

Another drawback is the conservative nature of the learned policy when using sampling from the learned policy. 
もう1つの欠点は、学習されたポリシーからのサンプリングを使用する際の学習されたポリシーの保守的な性質です。

The softmax policy parameterization used in the approach leads to a more myopic policy, recommending more popular and longer content and less novel content. 
このアプローチで使用されるソフトマックスポリシーのパラメータ化は、より人気のある長いコンテンツを推奨し、より新しいコンテンツを少なくするより近視的なポリシーをもたらします。

Gao et al. [15] centre around the problem of the Matthew effect in offline RL based RS. 
Gaoら [15] は、オフラインRLに基づくRSにおけるマシュー効果の問題に焦点を当てています。

The Matthew effect describes a phenomenon where popular items or categories are recommended more frequently, leading to the neglect of less popular ones. 
マシュー効果は、人気のあるアイテムやカテゴリがより頻繁に推薦される現象を説明し、結果として人気のないアイテムが無視されることにつながります。

This bias towards popular items can reduce the diversity in recommendations and decrease user satisfaction. 
人気のあるアイテムに対するこのバイアスは、推薦の多様性を減少させ、ユーザーの満足度を低下させる可能性があります。

To address the Matthew effect, the authors propose a Debiased model-based Offline RL (DORL) method. 
マシュー効果に対処するために、著者らはデバイアスされたモデルベースのオフラインRL（DORL）手法を提案します。

DORL introduces a penalty term to the RL algorithm, encouraging exploration and diversity in recommendations. 
DORLは、RLアルゴリズムにペナルティ項を導入し、推薦における探索と多様性を促進します。

By adding this penalty, the method aims to reduce the bias towards popular items and promote a more varied selection. 
このペナルティを追加することで、方法は人気のあるアイテムに対するバイアスを減少させ、より多様な選択を促進することを目指します。

Wang et al. [47] address the challenges inherent in designing reward functions and handling large-scale datasets within RL4RS. 
Wangら [47] は、RL4RS内で報酬関数を設計し、大規模データセットを扱う際の固有の課題に取り組んでいます。

Traditional RL4RS approaches may fall short in accurately estimating rewards only based on limited observations. 
従来のRL4RSアプローチは、限られた観察に基づいて報酬を正確に推定することに失敗する可能性があります。

To address this problem, a Causal Decision Transformer for RS (CDT4Rec) is proposed, a novel model that integrates offline RL and transformer architecture. 
この問題に対処するために、オフラインRLとトランスフォーマーアーキテクチャを統合した新しいモデルであるRSのための因果決定トランスフォーマー（CDT4Rec）が提案されます。

CDT4Rec employs a causal mechanism to estimate rewards based on user behavior, allowing for a more accurate understanding of user preferences. 
CDT4Recは、ユーザーの行動に基づいて報酬を推定する因果メカニズムを採用し、ユーザーの好みをより正確に理解できるようにします。

The transformer architecture is used to process large datasets and capture dependencies, enabling the model to handle complex data structures. 
トランスフォーマーアーキテクチャは、大規模データセットを処理し、依存関係を捉えるために使用され、モデルが複雑なデータ構造を扱えるようにします。

Yuan et al. [57] is motivated by the challenges associated with optimizing mobile notification systems. 
Yuanら [57] は、モバイル通知システムの最適化に関連する課題に動機づけられています。

Traditional response-prediction models often struggle to accurately attribute the impact to a single notification, leading to inefficiencies in managing and delivering notifications. 
従来の応答予測モデルは、単一の通知に影響を正確に帰属させることに苦労し、通知の管理と配信における非効率を引き起こします。

Recognizing this limitation, the authors aim to explore the application of RL to enhance the decision-making process for sequential notifications, seeking to provide a more effective and targeted approach to mobile notification systems. 
この制限を認識し、著者らは、連続通知の意思決定プロセスを強化するためにRLの適用を探求し、モバイル通知システムに対してより効果的でターゲットを絞ったアプローチを提供することを目指しています。

Hence, an offline RL framework specifically designed for sequential notification decisions is proposed. 
したがって、連続通知決定のために特別に設計されたオフラインRLフレームワークが提案されます。

They introduce a state-marginalized importance sampling policy evaluation approach, which is a novel method to assess the effectiveness of different notification strategies. 
彼らは、異なる通知戦略の効果を評価するための新しい方法である状態周辺化重要度サンプリングポリシー評価アプローチを導入します。

Through simulations, the authors demonstrate the performance of the approach, and they also present a real-world application of the framework, detailing the practical considerations and results. 
シミュレーションを通じて、著者らはアプローチの性能を示し、フレームワークの実世界での適用を提示し、実際の考慮事項と結果を詳述します。

Wang et al. [50] are motivated by the challenge of adapting to new users in recommendation systems, particularly when there are limited interactions to understand user preferences. 
Wangら [50] は、推薦システムにおける新しいユーザーへの適応の課題に動機づけられており、特にユーザーの好みを理解するための相互作用が限られている場合です。

This situation, often referred to as the “cold-start” problem, can hinder the ability to provide personalized recommendations that align with long-term user interests. 
この状況は、しばしば「コールドスタート」問題と呼ばれ、長期的なユーザーの興味に沿ったパーソナライズされた推薦を提供する能力を妨げる可能性があります。

The proposed approach introduces a user context variable to represent user preferences, employing a meta-level model-based RL method for rapid user adaptation. 
提案されたアプローチは、ユーザーの好みを表すためのユーザーコンテキスト変数を導入し、迅速なユーザー適応のためのメタレベルのモデルベースRL手法を採用します。

The user model and recommendation agent interact alternately, with the interaction relationship modeled from an information-theoretic perspective. 
ユーザーモデルと推薦エージェントは交互に相互作用し、相互作用関係は情報理論的な視点からモデル化されます。

Zhang et al. [59] discuss the problem of interactive recommendation with natural-language feedback and proposes an offline RL framework to address the challenges of collecting experience through user interaction. 
Zhangら [59] は、自然言語フィードバックを伴うインタラクティブ推薦の問題について論じ、ユーザーの相互作用を通じて経験を収集する課題に対処するためのオフラインRLフレームワークを提案します。

The authors develop a behavior-agnostic off-policy correction framework that leverages the conservative Q-function for off-policy evaluation. 
著者らは、オフポリシー評価のために保守的Q関数を活用する行動無関係なオフポリシー修正フレームワークを開発します。

This allows for learning effective policies from fixed datasets without further interactions. 
これにより、さらなる相互作用なしに固定データセットから効果的なポリシーを学習することが可能になります。

Xiao and Wang [54] propose a general offline RL framework for the interactive recommendation. 
XiaoとWang [54] は、インタラクティブ推薦のための一般的なオフラインRLフレームワークを提案します。

The proposed method introduces different techniques such as support constraints, supervised regularization, policy constraints, dual constraints, and reward extrapolation. 
提案された方法は、サポート制約、監視正則化、ポリシー制約、二重制約、報酬外挿などのさまざまな技術を導入します。

These methods aim to minimize the mismatch between the recommendation policy and logging policy and to balance the supervised signal and task reward. 
これらの方法は、推薦ポリシーとログポリシーの不一致を最小限に抑え、監視信号とタスク報酬のバランスを取ることを目指しています。



## 4 CHALLENGES AND OPPORTUNITIES 課題と機会

Offline RL4RS is an emerging domain that introduces multiple challenges demanding comprehensive exploration. 
オフラインRL4RSは、包括的な探索を要求する複数の課題を導入する新興分野です。
In this section, we aim to outline the open challenges in offline RL4RS. 
このセクションでは、オフラインRL4RSにおける未解決の課題を概説します。
Given that RS fall under the application scope of offline RL, several shared challenges naturally arise. 
RSはオフラインRLの応用範囲に含まれるため、いくつかの共通の課題が自然に生じます。
We will begin by addressing some common challenges before delving into the specific challenges unique to RS when utilizing offline RL techniques. 
一般的な課題に取り組んだ後、オフラインRL技術を利用する際のRS特有の課題に深く掘り下げていきます。

**4.1** **High-quality Offline Data and Cold-Start Problems 高品質なオフラインデータとコールドスタート問題** 
One of the most prominent challenges in offline Reinforcement Learning (RL) lies in the fact that the learning process hinges solely on the provided static dataset. 
オフライン強化学習（RL）における最も顕著な課題の一つは、学習プロセスが提供された静的データセットのみに依存しているという事実です。
This limitation results in a significant obstacle to enhancing exploration, as exploration falls outside the algorithm’s purview. 
この制限は、探索がアルゴリズムの範囲外にあるため、探索を強化する上での重要な障害となります。
Consequently, if the dataset lacks transitions that demonstrate regions of the state space yielding high rewards, the algorithm may be fundamentally incapable of uncovering these rewarding regions. 
したがって、データセットに高い報酬を生み出す状態空間の領域を示す遷移が欠けている場合、アルゴリズムはこれらの報酬を得られる領域を発見することが根本的に不可能になる可能性があります。
In contrast to control tasks, which are common in offline RL applications and often face challenges in gathering comprehensive data to facilitate effective learning from high-reward scenarios, the landscape changes when it comes to RS. 
オフラインRLアプリケーションで一般的な制御タスクとは対照的に、高報酬シナリオから効果的に学習するための包括的なデータを収集することに課題がある場合が多いですが、RSに関しては状況が変わります。
In this domain, a plethora of offline datasets, such as those from MovieLens, GoodReads, and Amazon, are publicly available. 
この分野では、MovieLens、GoodReads、Amazonなどのオフラインデータセットが多数公開されています。
These datasets stem from real-world interactions and adeptly capture users’ preferences. 
これらのデータセットは、実世界の相互作用から派生し、ユーザーの好みを巧みに捉えています。
However, RS diverge from traditional offline RL application domains due to their distinct characteristics. 
しかし、RSはその独自の特性により、従来のオフラインRL応用分野から逸脱しています。
To illustrate, let’s consider implicit feedback, particularly review data. 
例を挙げると、暗黙のフィードバック、特にレビューデータを考えてみましょう。
This kind of data poses a challenge when attempting to embed it within the state space due to its reliance on text. 
この種のデータは、テキストに依存しているため、状態空間に埋め込む際に課題を引き起こします。
Although techniques like word2vec exist to transform textual data into vectors that might potentially be integrated into the state space, the question of how to effectively guide the agent in utilizing such data in RS remains unexplored. 
word2vecのような技術が存在し、テキストデータを状態空間に統合できるベクトルに変換することが可能ですが、RSにおいてそのようなデータを効果的に利用するためにエージェントをどのように導くかという問題は未解決のままです。
Another intriguing aspect is the presence of graph data, extensively used in RS to represent social connections, item relationships, and more. 
もう一つの興味深い側面は、RSで広く使用されているグラフデータの存在で、社会的なつながりやアイテムの関係などを表現します。
The prevalent form of representation is a knowledge graph, which can be transformed into embeddings through the application of Graph Neural Networks (GNN). 
一般的な表現形式は知識グラフであり、Graph Neural Networks (GNN)を適用することで埋め込みに変換できます。
Nonetheless, it faces a similar challenge as textual data: how to empower the agent to effectively utilize this information. 
それでも、テキストデータと同様の課題に直面しています：エージェントがこの情報を効果的に利用できるようにする方法です。
There are some works investigating graph RL which may be able to provide some directions to offline RL4RS. 
グラフRLを調査しているいくつかの研究があり、オフラインRL4RSに対するいくつかの方向性を提供できるかもしれません。
However, a challenge surfaces due to what’s known as the “data sparsity problem”. 
しかし、「データスパース性問題」として知られる課題が浮上します。
This means that despite having ample data, there’s no assurance that the collected user interactions or behaviors cover all the situations where users have expressed positive feedback, like giving high ratings. 
これは、十分なデータがあっても、収集されたユーザーの相互作用や行動が、ユーザーが高評価を与えるなどのポジティブなフィードバックを示したすべての状況をカバーしている保証がないことを意味します。
In other words, there might be important scenarios where users found something valuable, but the data doesn’t reflect those instances well. 
言い換えれば、ユーザーが何か価値のあるものを見つけた重要なシナリオがあるかもしれませんが、データはそれらの事例をうまく反映していない可能性があります。
On the other hand, there is another widely recognized hurdle in RS that also applies to Offline RL4RS: the cold-start problem. 
一方で、RSにおいて広く認識されているもう一つの障害があり、オフラインRL4RSにも適用されます：コールドスタート問題です。
Unlike data sparsity, cold-start challenges emerge when the agent aims to provide recommendations to a new user. 
データスパース性とは異なり、コールドスタートの課題は、エージェントが新しいユーザーに推奨を提供しようとする際に発生します。
This issue arises due to the absence of adequate historical data or interactions, which in turn hampers the understanding of preferences and traits related to these new users or items. 
この問題は、十分な履歴データや相互作用が欠如しているために発生し、これにより新しいユーザーやアイテムに関連する好みや特性の理解が妨げられます。
While addressing the cold-start problem is an ongoing research avenue in conventional RS tasks, it hasn’t received sufficient attention in the context of RL4RS. 
コールドスタート問題に対処することは、従来のRSタスクにおける継続的な研究の道筋ですが、RL4RSの文脈では十分な注意を払われていません。
Considering the interactive procedure of the RL4RS, new users have limited contextual information that they can use to formulate the state representation; this contributes to the difficulty of making recommendations. 
RL4RSのインタラクティブな手続きを考慮すると、新しいユーザーは状態表現を形成するために使用できる限られた文脈情報しか持っておらず、これが推奨を行う上での難しさに寄与しています。
This predicament continues to remain an unsolved puzzle within the realm of offline RL4RS. 
この困難は、オフラインRL4RSの領域において未解決のパズルとして残り続けています。

**4.2** **Distribution Shift 分布のシフト**
A challenge of significant intricacy within the context of offline RL pertains to the effective formulation and addressing of counterfactual queries—a task that might not be readily apparent but is of great importance. 
オフラインRLの文脈における重要な複雑さのある課題は、反事実的クエリの効果的な定式化と対処に関するものであり、これは明白ではないかもしれませんが、非常に重要です。
Counterfactual queries, in essence, are defined as hypothetical “what if” scenarios. 
反事実的クエリは、本質的に仮想的な「もしも」のシナリオとして定義されます。
These queries involve creating educated guesses about potential outcomes if the agent were to undertake actions different from those observed in the data. 
これらのクエリは、エージェントがデータで観察された行動とは異なる行動を取った場合の潜在的な結果についての推測を作成することを含みます。
It is the core behind offline RL, as our objective is to learn a policy that can perform better than the behavior recorded in the dataset. 
これはオフラインRLの核心であり、私たちの目的はデータセットに記録された行動よりも優れたパフォーマンスを発揮できるポリシーを学ぶことです。
Hence, the agent must execute an action that is different from the learned policy. 
したがって、エージェントは学習したポリシーとは異なる行動を実行しなければなりません。
This situation, unfortunately, places a substantial strain on the capabilities of several prevailing deep-learning methods. 
残念ながら、この状況は、いくつかの既存の深層学習手法の能力に大きな負担をかけます。
Existing methods have been methodically fashioned under the assumption that the data is independence and identical distribution (i.i.d.). 
既存の手法は、データが独立同一分布（i.i.d.）であるという仮定の下で体系的に構築されています。
In traditional supervised learning based RS, the goal is to train a model to achieve superior performance, such as higher accuracy, recall or precision. 
従来の教師あり学習に基づくRSでは、目標はモデルを訓練して、より高い精度、再現率、または適合率を達成することです。
The evaluation dataset follows the same distribution as the training dataset. 
評価データセットは、トレーニングデータセットと同じ分布に従います。
Hence, in offline RL4RS, the key point is to learn a policy that can recommend different items (ideally with better feedback) from the behavior recorded in the dataset. 
したがって、オフラインRL4RSにおいて重要な点は、データセットに記録された行動から異なるアイテム（理想的にはより良いフィードバックを伴う）を推奨できるポリシーを学ぶことです。
The challenge behind counterfactual queries is that of distribution shift. 
反事実的クエリの背後にある課題は、分布のシフトです。
The policy is trained under one distribution, but it will be evaluated on a different distribution. 
ポリシーはある分布の下で訓練されますが、異なる分布で評価されます。
Given that such a problem is not widely discussed in the RS literature, we will provide some algorithmic insights from the offline RL perspective to help address this in offline RL4RS. 
このような問題がRS文献で広く議論されていないため、オフラインRLの観点からいくつかのアルゴリズム的な洞察を提供し、オフラインRL4RSでの解決に役立てます。
Distribution shift issues can be addressed in several ways, with the simplest one being to constrain something about the learning process such that the distribution shift is bounded. 
分布のシフトの問題は、いくつかの方法で対処でき、最も簡単な方法は、学習プロセスに関して何かを制約し、分布のシフトを制限することです。
For example, we can constrain how much the learned policy $\pi(a|s)$ differs from behavior policy $\pi_\beta(a|s)$ by using some techniques like Trust Region Policy Optimization (TRPO). 
例えば、Trust Region Policy Optimization (TRPO)のような技術を使用して、学習したポリシー $\pi(a|s)$ が行動ポリシー $\pi_\beta(a|s)$ からどれだけ異なるかを制約することができます。
However, if there is a significant disparity between the distribution of the training dataset and that of the evaluation environment, it might lead to the emergence of out-of-distribution (OOD) behavior. 
しかし、トレーニングデータセットの分布と評価環境の分布の間に大きな不一致がある場合、分布外（OOD）行動の出現につながる可能性があります。
Several recent studies have delved into OOD recommendation, taking into account shifts in user features. 
最近のいくつかの研究は、ユーザーの特徴のシフトを考慮したOOD推薦に取り組んでいます。
These efforts can be categorized into two main groups: OOD generalization and OOD adaptation. 
これらの取り組みは、主に2つのグループに分類できます：OOD一般化とOOD適応。
The underlying notion here is to acquire a causal representation of users’ preferences by leveraging their most recent behaviors. 
ここでの基本的な考え方は、ユーザーの最近の行動を活用して、ユーザーの好みの因果表現を取得することです。
This representation is then utilized within a causal graph framework to comprehend how shifts in features could impact users’ preferences. 
この表現は、因果グラフフレームワーク内で利用され、特徴のシフトがユーザーの好みにどのように影響を与えるかを理解するために使用されます。
Furthermore, the current methodologies primarily target sequential recommendation systems, which share certain properties with MDPs, rendering them relevant to offline RL4RS. 
さらに、現在の方法論は主に、MDPと共通の特性を持つ逐次推薦システムを対象としており、これによりオフラインRL4RSに関連性を持たせています。
However, this domain is still in its exploratory phase, and it has not garnered substantial attention. 
しかし、この分野はまだ探索段階にあり、十分な注目を集めていません。
As a result, this presents an open challenge with significant potential for further exploration. 
その結果、これはさらなる探求のための重要な可能性を持つ未解決の課題を提示します。

**4.3** **Bias and Variance Trade-off バイアスと分散のトレードオフ**
Another prevalent issue within offline RL4RS pertains to the bias inherited from RS, a topic that has recently gained increasing research attention. 
オフラインRL4RSにおけるもう一つの一般的な問題は、RSから引き継がれるバイアスに関するもので、これは最近ますます研究の注目を集めています。
This bias stems from the nature of offline data, with recent studies revealing that user behavior data are not experimental but rather observational, introducing bias-related challenges. 
このバイアスはオフラインデータの性質に起因し、最近の研究ではユーザー行動データが実験的ではなく観察的であることが明らかになり、バイアスに関連する課題を引き起こしています。
The prevalence of bias can be attributed to two primary factors. 
バイアスの蔓延は、主に2つの要因に起因します。
Firstly, the inherent character of user behavior data is observational rather than experimental. 
第一に、ユーザー行動データの本質的な性質は、実験的ではなく観察的です。
In simpler terms, the data fed into RS are susceptible to selection bias. 
簡単に言えば、RSに供給されるデータは選択バイアスに影響されやすいです。
For instance, in a video recommendation system, users tend to engage with, rate, and comment on movies that align with their personal interests. 
例えば、ビデオ推薦システムでは、ユーザーは自分の興味に合った映画に対して関与し、評価し、コメントする傾向があります。
Secondly, a discrepancy in distribution exists, signifying that the distributions of users and items within the recommender system are uneven. 
第二に、分布の不一致が存在し、推薦システム内のユーザーとアイテムの分布が不均一であることを示しています。
This imbalance can lead to a “popularity bias”, where popular items receive disproportionately frequent recommendations compared to others. 
この不均衡は「人気バイアス」を引き起こし、人気のあるアイテムが他のアイテムに比べて不均衡に頻繁に推薦されることになります。
Nonetheless, disregarding products within the "long tail" of less popular items can have adverse effects on businesses, given that these items are equally essential, albeit less likely to be discovered by chance. 
それでも、あまり人気のないアイテムの「ロングテール」にある製品を無視することは、これらのアイテムが同様に重要であるにもかかわらず、偶然に発見される可能性が低いため、ビジネスに悪影響を及ぼす可能性があります。
As mentioned earlier, a substantial portion of existing offline off-policy with logged data methods primarily focus on off-policy evaluation. 
前述のように、既存のオフラインオフポリシーのログデータを使用した手法の大部分は、主にオフポリシー評価に焦点を当てています。
This approach employs importance sampling to tackle the bias issue. 
このアプローチは、バイアスの問題に対処するために重要度サンプリングを使用します。
However, the importance sampling gives rise to another hurdle—high variance. 
しかし、重要度サンプリングは別の障害、高い分散を引き起こします。
While importance sampling already contends with high variance, this issue is further exacerbated in the context of sequential scenarios. 
重要度サンプリングはすでに高い分散に対処していますが、この問題は逐次シナリオの文脈でさらに悪化します。
In this setting, the importance weights at consecutive time steps are multiplied together, leading to an exponential amplification of variance. 
この設定では、連続する時間ステップでの重要度重みが掛け合わされ、分散が指数的に増幅されます。
Approximate and marginalized importance sampling methods mitigate this concern to some extent by circumventing the multiplication of importance weights across multiple time steps. 
近似的および周辺的な重要度サンプリング手法は、複数の時間ステップにわたる重要度重みの掛け算を回避することによって、この懸念をある程度軽減します。
Yet, the fundamental challenge persists: when the behavior policy $\pi_\beta$ substantially diverges from the current learned policy $\pi_\theta$, the importance weights degenerate. 
それでも、根本的な課題は残ります：行動ポリシー $\pi_\beta$ が現在の学習ポリシー $\pi_\theta$ から大きく逸脱すると、重要度重みが劣化します。
Consequently, any estimations of the return or gradient encounter excessive variance, particularly in scenarios characterized by high-dimensional state and action spaces or extended time horizons. 
その結果、リターンや勾配の推定は過剰な分散に直面し、特に高次元の状態および行動空間や長い時間のホライズンを特徴とするシナリオでは顕著です。
For this reason, importance-sampled estimators are most effective when the policy’s deviation from the behavior policy remains within a reasonable limit. 
この理由から、重要度サンプリングされた推定量は、ポリシーの行動ポリシーからの逸脱が合理的な範囲内にあるときに最も効果的です。
In the general off-policy setting, this condition generally holds true, as new trajectories are frequently amassed and integrated into the dataset using the latest policy. 
一般的なオフポリシー設定では、この条件は一般的に真であり、新しい軌道が頻繁に集められ、最新のポリシーを使用してデータセットに統合されます。
However, in the offline context, this is not typically the case. 
しかし、オフラインの文脈では、通常はそうではありません。
Consequently, the extent of enhancement achievable through importance sampling is confined by several factors: (i) the relative suboptimality of the behavior policy; (ii) the dimensionality of the state and action space; (iii) the effective task horizon. 
その結果、重要度サンプリングを通じて達成可能な改善の程度は、いくつかの要因によって制限されます：（i）行動ポリシーの相対的な最適性の低さ；（ii）状態および行動空間の次元；（iii）効果的なタスクのホライズン。
Hence, the tradeoff between bias and variance in offline RL4RS presents an intriguing potential avenue for advancement. 
したがって、オフラインRL4RSにおけるバイアスと分散のトレードオフは、進展のための興味深い可能性のある道を提示します。

**4.4** **Explainability 説明可能性**
While deep learning-based models can significantly enhance the performance of RS, they often lack interpretability. 
深層学習ベースのモデルはRSのパフォーマンスを大幅に向上させることができますが、しばしば解釈可能性に欠けます。
Consequently, the task of rendering recommender outputs understandable becomes vital, all while maintaining high-quality recommendations. 
その結果、推薦出力を理解可能にする作業が重要になり、高品質な推奨を維持する必要があります。
Elevating explainability in RS carries benefits beyond aiding end-users in comprehending suggested items. 
RSにおける説明可能性を高めることは、提案されたアイテムを理解するのを助けるだけでなく、システム設計者がRSの内部動作を精査することを可能にします。
Additionally, the realm of explainability in RL has been garnering attention, although the current focus primarily revolves around visualizing learned representations. 
さらに、RLにおける説明可能性の領域は注目を集めていますが、現在の焦点は主に学習された表現の視覚化にあります。
What remains is an explanation of how the learned policy translates into actionable decisions. 
残るのは、学習されたポリシーがどのように実行可能な決定に変換されるかの説明です。
In the transition to RL4RS, the emphasis on explainability will shift towards elucidating how the agent justifies its recommended items. 
RL4RSへの移行において、説明可能性に対する重点は、エージェントがどのように推奨アイテムを正当化するかを明らかにすることに移ります。
Hence, explainability becomes a relatively easy task compared with interpreting the learning process or decision process. 
したがって、説明可能性は、学習プロセスや意思決定プロセスを解釈することと比較して、比較的容易な作業となります。
Attention models have emerged as powerful tools that not only bolster predictive performance but also enhance explainability. 
アテンションモデルは、予測性能を高めるだけでなく、説明可能性を向上させる強力なツールとして登場しました。
For instance, Wang et al. introduce an RL framework coupled with an attention model for explainable recommendations. 
例えば、Wangらは、説明可能な推薦のためのアテンションモデルと組み合わせたRLフレームワークを紹介しています。
This approach ensures model-agnostic by segregating the recommendation model from the explanation generator. 
このアプローチは、推薦モデルを説明生成器から分離することによって、モデルに依存しないことを保証します。
Agents instantiated through attention-based neural networks facilitate the generation of sentence-level explanations. 
アテンションベースのニューラルネットワークを通じてインスタンス化されたエージェントは、文レベルの説明を生成することを容易にします。
This approach could prove promising given the close connection between offline RL4RS and online RL4RS. 
このアプローチは、オフラインRL4RSとオンラインRL4RSの密接な関係を考えると、有望である可能性があります。
Moreover, with access to offline datasets in offline RL4RS, more solutions become feasible. 
さらに、オフラインRL4RSにおいてオフラインデータセットにアクセスできることで、より多くの解決策が実現可能になります。
Knowledge graphs, for instance, contain abundant user and item information, enabling the creation of more personalized, intuitive explanations for recommendation systems. 
例えば、知識グラフは豊富なユーザーおよびアイテム情報を含んでおり、推薦システムのためのよりパーソナライズされた直感的な説明の作成を可能にします。
However, the processing of graph data presents challenges. 
しかし、グラフデータの処理には課題があります。
One potential strategy involves embedding a prelearned knowledge graph from the offline dataset into the environment. 
1つの潜在的な戦略は、オフラインデータセットから事前学習された知識グラフを環境に埋め込むことです。
The final objective then shifts from recommending items to navigating the knowledge graph. 
最終的な目標は、アイテムを推薦することから知識グラフをナビゲートすることに移ります。
As an example, Zhao et al. extract informative path demonstrations with minimal labeling effort. 
例として、Zhaoらは最小限のラベリング作業で情報豊富なパスのデモを抽出します。
Then an adversarial actor-critic model for demonstration-guided pathfinding is proposed. 
次に、デモンストレーションに基づくパスファインディングのための敵対的なアクター-クリティックモデルが提案されます。
This approach enhances recommendation accuracy and explainability through RL and knowledge graph reasoning and can be further expanded by integrating offline RL features. 
このアプローチは、RLと知識グラフ推論を通じて推薦の精度と説明可能性を向上させ、オフラインRL機能を統合することでさらに拡張できます。



## 5 FUTURE DIRECTIONS 今後の方向性

In offline RL4RS, several key areas emerge as promising avenues. 
オフラインRL4RSにおいて、いくつかの重要な分野が有望な道筋として浮かび上がっています。

Cross-domain recommendation systems offer the potential in transferring insights between diverse domains, enhancing recommendation effectiveness. 
クロスドメイン推薦システムは、異なるドメイン間での知見の移転を可能にし、推薦の効果を高める可能性を提供します。

The integration of large language models holds the prospect of enriching contextual understanding and refining user-item interactions. 
大規模言語モデルの統合は、文脈理解を豊かにし、ユーザーとアイテムの相互作用を洗練させる可能性を秘めています。

Incorporating causality into offline RL4RS can deepen comprehension of user behaviors, leading to more accurate and interpretable recommendations. 
オフラインRL4RSに因果関係を組み込むことで、ユーザーの行動の理解が深まり、より正確で解釈可能な推薦が可能になります。

The exploration of self-supervised learning and graph-based techniques presents innovative possibilities for capturing intricate user-item relationships. 
自己教師あり学習やグラフベースの技術の探求は、複雑なユーザーとアイテムの関係を捉えるための革新的な可能性を提示します。

Moreover, addressing uncertainty and fortifying the robustness of RL4RS against noise and adversarial inputs stand out as essential directions for ensuring dependable and consistent recommendation outcomes. 
さらに、不確実性に対処し、ノイズや敵対的入力に対するRL4RSの堅牢性を強化することは、信頼性が高く一貫した推薦結果を確保するための重要な方向性として際立っています。

**5.1** **Cross-Domain Recommendation クロスドメイン推薦**

Cross-domain recommendation refers to the task of providing recommendations to users by leveraging data and knowledge from multiple distinct domains. 
クロスドメイン推薦とは、複数の異なるドメインからのデータと知識を活用して、ユーザーに推薦を提供するタスクを指します。

Cross-domain recommendation systems can be particularly useful in scenarios where user data is sparse within a single domain but might be enriched when multiple domains are combined. 
クロスドメイン推薦システムは、単一のドメイン内でユーザーデータが希薄なシナリオで特に有用ですが、複数のドメインを組み合わせることで豊かになる可能性があります。

Additionally, they enable more comprehensive and diverse recommendations by tapping into different aspects of users’ interests. 
さらに、異なるユーザーの興味の側面にアクセスすることで、より包括的で多様な推薦を可能にします。

From this viewpoint, we may be able to treat offline RL4RS as a type of cross-domain recommendation in certain situations. 
この観点から、特定の状況においてオフラインRL4RSを一種のクロスドメイン推薦として扱うことができるかもしれません。

For example, when the evaluation environment is significantly different from the offline dataset, we may treat the evaluation platform as a new domain and we would like to transfer D those learned knowledge from into such a platform. 
例えば、評価環境がオフラインデータセットと大きく異なる場合、評価プラットフォームを新しいドメインとして扱い、そこに学習した知識を移転したいと考えます。

The challenge in cross-domain recommendation lies in effectively transferring knowledge and patterns across domains while accounting for variations in user behaviors and item characteristics. 
クロスドメイン推薦の課題は、ユーザーの行動やアイテムの特性の変動を考慮しながら、ドメイン間で知識やパターンを効果的に移転することにあります。

Techniques such as domain adaptation, transfer learning, and hybrid models are often employed to bridge the gaps between different domains and optimize recommendation performance. 
ドメイン適応、転移学習、ハイブリッドモデルなどの技術が、異なるドメイン間のギャップを埋め、推薦性能を最適化するためにしばしば使用されます。

Moreover, recent work in cross-domain offline RL would be beneficial. 
さらに、クロスドメインオフラインRLにおける最近の研究は有益です。

Liu et al. [31] present BOSA (Beyond OOD State Actions), a method for cross-domain offline RL (RL). 
Liuらは、クロスドメインオフラインRL（RL）のための手法BOSA（Beyond OOD State Actions）を提案しています。

BOSA tackles the challenges of out-of-distribution (OOD) state actions and data inefficiency by incorporating additional source domain data. 
BOSAは、追加のソースドメインデータを取り入れることで、分布外（OOD）状態アクションとデータの非効率性の課題に取り組みます。

The authors propose specific objectives to address OOD transition dynamics and demonstrate that BOSA improves data efficiency and outperforms existing methods. 
著者たちは、OOD遷移ダイナミクスに対処するための具体的な目標を提案し、BOSAがデータ効率を改善し、既存の手法を上回ることを示しています。

The method is also applicable to model-based RL and data augmentation techniques. 
この手法は、モデルベースのRLやデータ拡張技術にも適用可能です。

However, in offline RL4RS, this problem is still open for investigation as the techniques mentioned have not yet been explored in offline RL4RS. 
しかし、オフラインRL4RSにおいては、これらの技術がまだオフラインRL4RSで探求されていないため、この問題は依然として調査の余地があります。

**5.2** **Implicit Feedback and Large Language Models 暗黙的フィードバックと大規模言語モデル**

Implicit feedback serves as a commonly employed feedback mechanism for learning recommendation policies in RS. 
暗黙的フィードバックは、推薦システム（RS）における推薦ポリシーを学習するための一般的に使用されるフィードバックメカニズムです。

Implicit feedback encompasses user actions like clicks, views, purchases, time spent, and dwell time during interactions with platforms or systems, signifying user preferences and interests. 
暗黙的フィードバックは、クリック、ビュー、購入、費やした時間、プラットフォームやシステムとのインタラクション中の滞在時間などのユーザーアクションを含み、ユーザーの好みや興味を示します。

Although not as explicit as ratings or reviews, these behaviors offer valuable insights. 
評価やレビューほど明示的ではありませんが、これらの行動は貴重な洞察を提供します。

In the context of RL4RS, the reward mechanism evaluates recommended items. 
RL4RSの文脈において、報酬メカニズムは推薦されたアイテムを評価します。

Typically, this involves binary rewards based on click behavior, with some efforts, like Zheng et al. [66], incorporating dwell times for a more comprehensive reward signal. 
通常、これはクリック行動に基づくバイナリ報酬を含み、Zhengら[66]のように、より包括的な報酬信号のために滞在時間を組み込む努力もあります。

However, accommodating multiple implicit feedback sources concurrently in RL4RS poses challenges due to limited relevant datasets or simulations. 
しかし、RL4RSにおいて複数の暗黙的フィードバックソースを同時に取り入れることは、関連するデータセットやシミュレーションが限られているため、課題を呈します。

Additionally, harnessing review comments, a common type of implicit feedback in RS, within RL4RS remains a subject of exploration. 
さらに、RSにおける一般的な暗黙的フィードバックの一種であるレビューコメントをRL4RS内で活用することは、探求の対象となっています。

Zhang et al. [60] propose a text encoder solution, albeit relying on a manually gathered generator to produce review texts, which primarily validate feature learning rather than directly influencing the final reward. 
Zhangら[60]は、テキストエンコーダーソリューションを提案していますが、これは手動で収集されたジェネレーターに依存してレビューテキストを生成し、主に特徴学習を検証するもので、最終的な報酬に直接影響を与えるものではありません。

Transitioning this approach to offline RL4RS presents difficulties. 
このアプローチをオフラインRL4RSに移行することは困難です。

Firstly, integrating review comments into the reward function requires careful study. 
まず、レビューコメントを報酬関数に統合するには慎重な研究が必要です。

Secondly, textual data introduces high-dimensional state representations, potentially necessitating novel algorithms tailored to this scenario. 
第二に、テキストデータは高次元の状態表現を導入し、このシナリオに特化した新しいアルゴリズムが必要になる可能性があります。

Recently, Large Language Models (LLMs) have received increasing research interest in RS. 
最近、大規模言語モデル（LLMs）がRSにおいてますます研究の関心を集めています。

LLM demonstrates a superior capability in handling textual data from multiple tasks such as natural language understanding, contextual understanding and sentiment analysis [65]. 
LLMは、自然言語理解、文脈理解、感情分析などの複数のタスクからのテキストデータを処理する優れた能力を示します[65]。

Existing RS works provides some insights about how LLMs can be adopted in RS such as prompt engineering to instruct the LLM to make recommendations [58], utilizing the Generative Pre-trained Transformer (GPT) as the backbone to process features [43] etc. 
既存のRSの研究は、LLMをRSにどのように採用できるかについてのいくつかの洞察を提供しています。例えば、LLMに推薦を行うよう指示するためのプロンプトエンジニアリング[58]や、特徴を処理するためのバックボーンとしてGenerative Pre-trained Transformer（GPT）を利用すること[43]などです。

Moreover, some attempts have been undertaken about how LLM can be used in RL. 
さらに、LLMをRLでどのように使用できるかについてのいくつかの試みが行われています。

Du et al. [14] introduce a method called ELLM (Exploring with Large Language Models) that aims to enhance pretraining in RL by using LLM. 
Duら[14]は、LLMを使用してRLの事前学習を強化することを目的とした手法ELLM（Exploring with Large Language Models）を紹介しています。

ELLM works by prompting an LLM with a description of the agent’s current state and then rewarding the agent for achieving goals suggested by the LLM. 
ELLMは、エージェントの現在の状態の説明を用いてLLMにプロンプトを与え、その後LLMが提案した目標を達成することでエージェントに報酬を与えます。

This method biases exploration towards behaviors that are meaningful and potentially useful from a human perspective, without needing human intervention. 
この手法は、人間の視点から意味があり、潜在的に有用な行動への探索を偏らせ、人間の介入を必要としません。

Meanwhile, Carta et al. [3] explore the use of LLM in interactive environments through an approach called GLAM (Grounding Language Models). 
一方、Cartaら[3]は、GLAM（Grounding Language Models）と呼ばれるアプローチを通じて、インタラクティブな環境におけるLLMの使用を探求しています。

This method aligns the knowledge of LLMs with the environment, focusing on aspects like sample efficiency, generalization to new tasks, and the impact of online RL. 
この手法は、LLMの知識を環境と整合させ、サンプル効率、新しいタスクへの一般化、オンラインRLの影響などの側面に焦点を当てています。

**5.3** **Causality 因果関係**

In the previous section, we mentioned that offline RL can be formulated as answering counterfactual queries. 
前のセクションで、オフラインRLは反実仮想クエリに答える形で定式化できることに言及しました。

It is an intuitive choice to integrate the causality into offline RL from this perspective. 
この観点から、因果関係をオフラインRLに統合することは直感的な選択です。

Moreover, causality is widely used in RS and receiving increasing interest in offline RL. 
さらに、因果関係はRSで広く使用されており、オフラインRLにおいても関心が高まっています。

We believe it would be a promising topic in offline RL4RS. 
私たちは、これはオフラインRL4RSにおける有望なトピックになると考えています。

In the work by Zhu et al. [67], an exploration is undertaken regarding the integration of causal world models into the domain of model-based offline RL. 
Zhuら[67]の研究では、因果世界モデルをモデルベースのオフラインRLの領域に統合する探求が行われています。

The theoretical underpinning of their study accentuates the superiority of causal world models over ordinary world models in the context of offline RL. 
彼らの研究の理論的基盤は、オフラインRLの文脈において因果世界モデルが通常の世界モデルよりも優れていることを強調しています。

This advantage is attributed to the incorporation of causal structure within the generalization error bound. 
この利点は、一般化誤差境界内に因果構造を組み込むことに起因しています。

The authors introduce an operational algorithm termed FOCUS (Offline Model-based RL with Causal Structure) to exemplify the potential value derived from comprehending and effectively utilizing causal structure in the domain of offline RL. 
著者たちは、オフラインRLの領域における因果構造を理解し、効果的に活用することから得られる潜在的な価値を示すために、FOCUS（因果構造を持つオフラインモデルベースRL）という操作アルゴリズムを紹介しています。

Additionally, Liao et al. [29] introduce the notion of instrumental variable value iteration for causal offline RL. 
さらに、Liaoら[29]は、因果オフラインRLのための計量経済学的変数価値反復の概念を導入しています。

The presentation of their work introduces IV-aided Value Iteration (IVVI), an algorithm designed with efficiency in mind, aimed at extracting optimal policies from observational data in the presence of unobserved variables. 
彼らの研究の発表では、観察データから最適なポリシーを抽出することを目的とした効率性を考慮したアルゴリズムIV支援価値反復（IVVI）が紹介されています。

The utilization of instrumental variables (IVs) forms the foundation, with the authors devising a framework named Confounded Markov Decision Process with Instrumental Variables (CMDP-IV) to contextualize the problem. 
計量経済学的変数（IV）の利用が基盤を形成し、著者たちは問題を文脈化するためにIVを持つ混乱したマルコフ決定過程（CMDP-IV）というフレームワークを考案しています。

Notably, the IVVI algorithm, established upon a primal-dual reformulation of a conditional moment restriction, emerges as the first demonstrably efficient solution for instrument-aided offline RL. 
特に、条件付きモーメント制約のプライマル-双対再定式化に基づいて確立されたIVVIアルゴリズムは、計量経済学的支援を受けたオフラインRLに対する初の実証的に効率的な解決策として浮上します。

One of the most common applications of integrating causality into the RL4RS is counterfactual augmentation. 
因果関係をRL4RSに統合する最も一般的な応用の一つは、反実仮想拡張です。

Chen et al. [8, 9] develop a data augmentation technique that employs counterfactual reasoning to produce more informative interaction trajectories for RL4RS. 
Chenら[8, 9]は、反実仮想推論を用いてRL4RSのためにより情報量の多いインタラクショントラジェクトリを生成するデータ拡張技術を開発しています。

Wang et al. [48] introduces the Causal Decision Transformer for RS (CDT4Rec), a model that merges offline RL with the transformer architecture. 
Wangら[48]は、オフラインRLとトランスフォーマーアーキテクチャを統合したモデルであるRSのための因果決定トランスフォーマー（CDT4Rec）を紹介しています。

CDT4Rec is designed to tackle the challenges of crafting reward functions and leveraging large-scale datasets in RS. 
CDT4Recは、RSにおける報酬関数の作成と大規模データセットの活用に関する課題に対処するように設計されています。

It employs a causal mechanism to deduce rewards from user behavior and uses the transformer architecture to handle vast datasets and identify dependencies. 
それは、ユーザーの行動から報酬を推定するために因果メカニズムを採用し、トランスフォーマーアーキテクチャを使用して膨大なデータセットを処理し、依存関係を特定します。

Drawing inspiration from the works mentioned above, exploring causality in offline RL4RS emerges as a promising avenue for future research. 
上記の研究からインスピレーションを得て、オフラインRL4RSにおける因果関係の探求は、今後の研究の有望な道筋として浮上します。

Particularly, as causal offline RL4RS advances, its primary emphasis on counterfactual augmentation highlights an exciting direction. 
特に、因果オフラインRL4RSが進展するにつれて、反実仮想拡張に対する主な強調は、刺激的な方向性を浮き彫りにします。

However, it is important to recognize the need for additional endeavors in different domains, including but not limited to distribution shifts and the presence of biases. 
しかし、分布の変化やバイアスの存在を含むがそれに限定されない異なるドメインにおける追加の取り組みの必要性を認識することが重要です。

**5.4** **Robustness 堅牢性**

The vulnerability of deep learning-based methods is evident through adversarial samples, underscoring the pressing concern of robustness in both RS and RL. 
深層学習ベースの手法の脆弱性は、敵対的サンプルを通じて明らかであり、RSとRLの両方における堅牢性の重要な懸念を強調しています。

Particularly, the exploration of adversarial attacks and defense strategies within the domain of RS has garnered significant attention in recent times, as emphasized by the comprehensive survey conducted by [13]. 
特に、RSの領域における敵対的攻撃と防御戦略の探求は、最近大きな注目を集めており、[13]によって実施された包括的な調査によって強調されています。

This attention is fueled by the critical importance of security within the realm of RS operations. 
この注目は、RSの運用におけるセキュリティの重要性によって促進されています。

Furthermore, the vulnerability of RL policies to adversarial perturbations in agents’ observations has been established by [30]. 
さらに、エージェントの観察における敵対的摂動に対するRLポリシーの脆弱性は[30]によって確立されています。

In the context of RL4RS, Cao et al. [2] introduce an adversarial attack detection approach. 
RL4RSの文脈において、Caoら[2]は敵対的攻撃検出アプローチを紹介しています。

This method leverages the utilization of a Gated Recurrent Unit (GRU) to encode the action space into a lower-dimensional representation, alongside the design of decoders to identify potential attacks. 
この手法は、Gated Recurrent Unit（GRU）を利用してアクション空間を低次元の表現にエンコードし、潜在的な攻撃を特定するためのデコーダーの設計を行います。

However, it’s important to note that this method exclusively addresses attacks rooted in the Fast Gradient Sign Method (FGSM) and strategically-timed maneuvers. 
しかし、この手法は、Fast Gradient Sign Method（FGSM）および戦略的にタイミングを合わせた操作に基づく攻撃にのみ対処していることに注意することが重要です。

As a result, its ability to detect other forms of attacks is limited. 
その結果、他の形式の攻撃を検出する能力は限られています。

Within the arena of offline RL, recent advancements provide a promising direction. 
オフラインRLの領域において、最近の進展は有望な方向性を提供します。

Panaganti et al. [40] address the challenge of robust offline RL, centering on the learning of policies that can withstand uncertainties in model parameters. 
Panagantiら[40]は、モデルパラメータの不確実性に耐えるポリシーの学習に焦点を当て、堅牢なオフラインRLの課題に取り組んでいます。

The authors introduce the Robust Fitted Q-Iteration (RFQI) algorithm, which relies solely on offline data to determine the optimal robust policy. 
著者たちは、最適な堅牢ポリシーを決定するためにオフラインデータのみに依存する堅牢なフィッティングQ反復（RFQI）アルゴリズムを紹介しています。

This algorithm adeptly tackles concerns such as offline data collection, model optimization, and unbiased estimation. 
このアルゴリズムは、オフラインデータ収集、モデル最適化、バイアスのない推定などの懸念に巧みに対処します。

Additionally, Zhang et al. [62] concentrate on a scenario involving a batch dataset of state-action-reward-next state tuples, susceptible to potential corruption by adversaries. 
さらに、Zhangら[62]は、敵による潜在的な破損の影響を受けやすい状態-アクション-報酬-次状態のタプルのバッチデータセットを含むシナリオに焦点を当てています。

Their objective is to extract a near-optimal policy from this compromised dataset. 
彼らの目的は、この損なわれたデータセットから近似最適ポリシーを抽出することです。



## 6 CONCLUSION 結論

The recent advancements in RL4RS pave the way for efficiently capturing users’ dynamic interests. 
最近のRL4RSの進展は、ユーザーの動的な興味を効率的に捉える道を開きます。

However, the nature of online interactions necessitates costly trajectory collection procedures, posing a significant hurdle for researchers interested in this field. 
しかし、オンラインインタラクションの性質は、高価な軌道収集手続きを必要とし、この分野に興味を持つ研究者にとって大きな障害となっています。

In this survey, our goal is to provide a comprehensive overview of offline RL4RS, a novel paradigm that eliminates the need for an expensive data collection process. 
この調査の目的は、高価なデータ収集プロセスを排除する新しいパラダイムであるオフラインRL4RSの包括的な概要を提供することです。

Alongside reviewing recent works, we also offer insights into potential future opportunities. 
最近の研究をレビューするだけでなく、将来の可能性についての洞察も提供します。

Specifically, we’ve compiled and analyzed recent progress in offline RL4RS, organized into two distinct categories: off-policy learning utilizing logged data and offline RL4RS techniques. 
具体的には、オフポリシー学習（ログデータを利用）とオフラインRL4RS技術という2つの異なるカテゴリに整理されたオフラインRL4RSの最近の進展をまとめ、分析しました。

Furthermore, we address several prevailing challenges in this domain: offline data quality, distribution shift, bias and variance, and explainability. 
さらに、この分野におけるいくつかの一般的な課題、すなわちオフラインデータの質、分布の変化、バイアスと分散、説明可能性についても取り上げます。

Additionally, we present potential avenues for future exploration in this rapidly evolving field, such as cross-domain recommendation, LLMs, causality, and robustness. 
加えて、クロスドメイン推薦、LLMs、因果関係、ロバスト性など、この急速に進化する分野における将来の探求のための潜在的な道筋を提示します。

Being an emerging topic, offline RL4RS introduces fresh possibilities for integrating pre-existing offline datasets into the realm of RL4RS. 
新たに登場したトピックであるオフラインRL4RSは、既存のオフラインデータセットをRL4RSの領域に統合するための新しい可能性をもたらします。

This survey can also be perceived as a visionary paper, offering potential benefits to researchers who are newcomers to this field. 
この調査は、また、この分野に新たに参入する研究者に潜在的な利益を提供するビジョナリーな論文と見なすこともできます。
