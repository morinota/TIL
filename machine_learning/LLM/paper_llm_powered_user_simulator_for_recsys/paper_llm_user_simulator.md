refs: https://arxiv.org/pdf/2412.16984

# LLM-Powered User Simulator for Recommender System  

## 要約

User simulators can rapidly generate a large volume of timely user behavior data, providing a testing platform for reinforcement learning-based recommender systems, thus accelerating their iteration and optimization. 
**ユーザシミュレーターは、迅速に大量のタイムリーなユーザ行動データを生成でき、強化学習ベースの推薦システムのテストプラットフォームを提供**し、それによってシステムの反復と最適化を加速します。
However, prevalent user simulators generally suffer from significant limitations, including the opacity of user preference modeling and the incapability of evaluating simulation accuracy. 
しかし、一般的なユーザシミュレーターは、ユーザの嗜好モデルの不透明性やシミュレーション精度の評価能力の欠如など、重大な制限に悩まされています。
In this paper, we introduce an LLM-powered user simulator to simulate user engagement with items in an explicit manner, thereby enhancing the efficiency and effectiveness of reinforcement learning-based recommender systems training. 
本論文では、アイテムに対するユーザのエンゲージメントを明示的にシミュレートする**LLM駆動のユーザシミュレーターを紹介し、強化学習ベースの推薦システムのトレーニングの効率と効果を向上させます**。
Specifically, we identify the explicit logic of user preferences, leverage LLMs to analyze item characteristics and distill user sentiments, and design a logical model to imitate real human engagement. 
具体的には、ユーザの嗜好の明示的な論理を特定し、LLMを活用してアイテムの特性を分析し、ユーザの感情を抽出し、実際の人間のエンゲージメントを模倣する論理モデルを設計します。
By integrating a statistical model, we further enhance the reliability of the simulation, proposing an ensemble model that synergizes logical and statistical insights for user interaction simulations. 
統計モデルを統合することで、シミュレーションの信頼性をさらに向上させ、ユーザインタラクションシミュレーションのために論理的および統計的な洞察を相乗的に活用するアンサンブルモデルを提案します。
Capitalizing on the extensive knowledge and semantic generation capabilities of LLMs, our user simulator faithfully emulates user behaviors and preferences, yielding high-fidelity training data that enrich the training of recommendation algorithms. 
LLMの広範な知識と意味生成能力を活用することで、私たちのユーザシミュレーターはユーザの行動と嗜好を忠実に模倣し、**推薦アルゴリズムのトレーニングを豊かにする高忠実度のトレーニングデータを生成**します。
We establish quantifying and qualifying experiments on five datasets to validate the simulator’s effectiveness and stability across various recommendation scenarios. 
私たちは、さまざまな推薦シナリオにおけるシミュレーターの効果と安定性を検証するために、5つのデータセットで定量的および定性的な実験を実施します。


**Code — https://github.com/Applied-Machine-Learning-** Lab/LLM User Simulator  

<!-- ここまで読んだ! -->

## Introduction はじめに

Reinforcement Learning (RL)-based recommender systems have become increasingly important due to their capability to capture user preferences (Zhao et al. 2021a, 2023b; Liu et al. 2023b; Zhang et al. 2020) and long-term engagement (Liu et al. 2023a; Zhao et al. 2018a,b, 2019). 
強化学習（RL）に基づく推薦システムは、ユーザの好みを捉える能力（Zhao et al. 2021a, 2023b; Liu et al. 2023b; Zhang et al. 2020）や長期的なエンゲージメント（Liu et al. 2023a; Zhao et al. 2018a,b, 2019）により、ますます重要になっています。
They require interactive training where agent learns to make decisions by interacting with an environment. 
これらは、**エージェントが環境と相互作用することで意思決定を学ぶインタラクティブなトレーニングを必要**とします。
Online data reflects the real-time user feedback and behavioral patterns, which is critical for continuously refining recommender systems and solving real-world problems (Li et al. 2023; Han et al. 2024; Zhang et al. 2023, 2024c). 
**オンラインデータは、リアルタイムのユーザーフィードバックや行動パターンを反映しており、推薦システムを継続的に洗練し、実世界の問題を解決するために重要**です（Li et al. 2023; Han et al. 2024; Zhang et al. 2023, 2024c）。
However, due to the difficulty in obtaining online user interaction data, high collection costs, and user privacy concerns (Wang et al. 2023a), effectively simulating user interaction behavior has become an urgent problem to be solved. 
しかし、オンラインユーザーインタラクションデータの取得の難しさ、高い収集コスト、ユーザーのプライバシーに関する懸念（Wang et al. 2023a）により、**ユーザーインタラクション行動を効果的にシミュレーションすることは、解決すべき緊急の問題**となっています。
User simulators can quickly generate user behavior data, thus accelerating the evaluation process, and they guarantee user privacy without collection and use of real user data (Zhao et al. 2021b). 
ユーザーシミュレーターは、ユーザー行動データを迅速に生成できるため、評価プロセスを加速し、実際のユーザーデータの収集や使用なしにユーザープライバシーを保証します（Zhao et al. 2021b）。

<!-- ここまで読んだ! -->

Despite the promising progress of user simulators for recommender systems (Wang et al. 2023a; Ie et al. 2019; Corecco et al. 2024; Zhang et al. 2024a; Huang et al. 2024), existing research has two principal deficiencies. 
推薦システムのためのユーザーシミュレーターの有望な進展にもかかわらず（Wang et al. 2023a; Ie et al. 2019; Corecco et al. 2024; Zhang et al. 2024a; Huang et al. 2024）、**既存の研究には2つの主な欠陥**があります。
Firstly, current simulators fail to explicitly model user preferences, which is a critical function for accurately predicting user choices. 
第一に、現在のシミュレーターは**ユーザーの好みを明示的にモデル化することに失敗**しており、これはユーザーの選択を正確に予測するための重要な機能です。
VirtualTaobao (Shi et al. 2019) leverages GAN to simulate user interaction distribution and KuaiSim (Zhao et al. 2023a) employs an offline trained transformer to emulate user’s responses to recommendations. 
VirtualTaobao（Shi et al. 2019）はGANを利用してユーザーインタラクション分布をシミュレートし、KuaiSim（Zhao et al. 2023a）はオフラインで訓練されたトランスフォーマーを使用してユーザーの推薦に対する応答を模倣します。
Secondly, there is an absence of an efficient evaluative framework to assess the fidelity of simulated interactions with real user behavior. 
第二に、**シミュレーションされたインタラクションが実際のユーザー行動とどれだけ忠実であるかを評価するための効率的な評価フレームワークが欠如**しています。
Consequently, there is an urgent need for the advancement of user simulators that can operate with higher degrees of fidelity and transparency in replicating the complex dynamics of user-system interactions. 
その結果、ユーザーシステムインタラクションの複雑なダイナミクスを再現する際に、より高い忠実度と透明性で機能するユーザーシミュレーターの進展が急務となっています。

Recently, Large Language Models (LLMs) have demonstrated remarkable effectiveness in maintaining common knowledge and inferential capabilities across a spectrum of fields (Jia et al. 2023; Fu et al. 2023; Wang et al. 2024a,b; Liu et al. 2024a,b). 
最近、大規模言語モデル（LLMs）は、さまざまな分野で共通の知識と推論能力を維持する上で顕著な効果を示しています（Jia et al. 2023; Fu et al. 2023; Wang et al. 2024a,b; Liu et al. 2024a,b）。
This prowess positions LLMs as a promising avenue for simulating user behavior in recommendation systems. 
この能力により、**LLMsは推薦システムにおけるユーザー行動のシミュレーションにおいて有望な手段**として位置づけられます。
SUBER (Corecco et al. 2024) harnesses the semantic comprehension capabilities of LLMs to directly infer user engagement with items. 
SUBER（Corecco et al. 2024）は、LLMsの意味理解能力を活用して、アイテムに対するユーザーのエンゲージメントを直接推測します。
Agent4Rec (Zhang et al. 2024a) equips user simulation by integrating LLM agents. 
Agent4Rec（Zhang et al. 2024a）は、LLMエージェントを統合することでユーザーシミュレーションを強化します。
It supports a wide range of behaviors, including taste-driven actions, such as viewing and rating items, as well as emotion-driven actions, including exiting the system and feedback through comments. 
これは、アイテムの閲覧や評価などの嗜好に基づく行動や、システムからの退出やコメントを通じたフィードバックなどの感情に基づく行動を含む、幅広い行動をサポートします。
However, the application of LLMs in user simulation is not without drawbacks. 
しかし、ユーザーシミュレーションにおけるLLMsの適用には欠点もあります。
Primarily, the computational and time cost of calling LLM for simulations is substantial, posing a significant barrier to the training of the recommendation system (Corecco et al. 2024; Huang et al. 2024). 
**主に、シミュレーションのためにLLMを呼び出す際の計算コストと時間コストはかなり大きく**、推薦システムのトレーニングに対する重要な障壁となっています（Corecco et al. 2024; Huang et al. 2024）。
What’s more, an overreliance on LLMs also introduces the risk of hallucination, where the model generates factually incorrect or misleading inferences (Ji et al. 2023; Yao et al. 2023). 
さらに、LLMsへの過度の依存は、モデルが事実に基づかないまたは誤解を招く推論を生成するという幻覚のリスクも引き起こします（Ji et al. 2023; Yao et al. 2023）。
These challenges must be navigated carefully to harness LLMs in crafting user simulators that are both efficient and grounded in reality. 
これらの課題は、効率的で現実に基づいたユーザーシミュレーターを作成するためにLLMsを活用するために慎重に対処する必要があります。

<!-- ここまで読んだ! -->

In this paper, we first figure out a fundamental logic governing user interactions with recommended items, as illustrated in Figure 1. 
本論文では、まず、図1に示すように、**推薦アイテムとのユーザーインタラクションを支配する基本的な論理を明らかにします**。
Taking movie recommendations as an example, a user’s engagement with a recommended action movie begins with recognizing what the movie is, i.e., identifying its genre and characteristics that might lead to a liking or disliking sentiment. 
映画推薦を例に取ると、ユーザーが推薦されたアクション映画に関与する際は、まずその映画が何であるかを認識することから始まります。つまり、ジャンルや好まれるか嫌われるかの感情につながる特徴を特定します。
This recognition is followed by a deeper inquiry into how the item aligns with the user’s tastes, i.e., analyzing his past preference to this genre, and considering the general comments to this movie. 
この認識の後、アイテムがユーザーの嗜好とどのように一致するかを深く探求します。つまり、彼の過去のこのジャンルに対する好みを分析し、この映画に対する一般的なコメントを考慮します。
Based on item characteristics and the user’s preference information, our goal is to explicitly utilize the fundamental logic of user interactions and predict their behavior towards an item in a transparent and understandable manner. 
アイテムの特徴とユーザーの好み情報に基づいて、私たちの目標は、**ユーザーインタラクションの基本的な論理を明示的に利用**し、アイテムに対する彼らの行動を透明で理解しやすい方法で予測することです。

It is nontrivial to achieve this goal, and several main challenges must be conquered. 
この目標を達成することは簡単ではなく、いくつかの主要な課題を克服する必要があります。
First, how to depict the user preference explicitly? 
第一に、ユーザーの好みを明示的に描写するにはどうすればよいでしょうか？
Translating user preferences into a clear and understandable model is inherently difficult. 
ユーザーの好みを明確で理解しやすいモデルに翻訳することは本質的に難しいです。(ここは一旦えいやでやってしまってもいいのかも??:thinking:)
Existing deep collaborative filtering models with trainable embedding are hardly explainable, let alone indicating user preference. 
トレーニング可能な埋め込みを持つ既存の深層協調フィルタリングモデルはほとんど説明可能ではなく、ユーザーの好みを示すことはなおさら困難です。
To address this, we propose leveraging LLM to analyze and interpret item characteristics from various angles, including genre, potential likes and dislikes, and user sentiments. 
**これに対処するために、私たちはLLMを活用して、ジャンル、潜在的な好みや嫌い、ユーザーの感情など、さまざまな角度からアイテムの特徴を分析し解釈することを提案**します。
By harnessing the rich analytical capabilities of LLM, we develop a logical model that captures the nuanced decision-making processes underlying user interactions. 
LLMの豊富な分析能力を活用することで、ユーザーインタラクションの背後にある微妙な意思決定プロセスを捉える論理モデルを開発します。

<!-- ここまで読んだ! -->

Second, how to alleviate computational cost and the hallucination issue when using LLM? 
第二に、LLMを使用する際の計算コストと幻覚の問題をどのように軽減するかです。
The computational demands of LLM and the risk of hallucination present substantial hurdles in system reliability (Ji et al. 2023). 
LLMの計算要求と幻覚のリスクは、システムの信頼性において大きな障害をもたらします（Ji et al. 2023）。
Instead of inferring the user interaction directly based on LLM (Zhang et al. 2024a; Corecco et al. 2024), we use LLM to distill the reasons a user might like or dislike an item, condensing and filtering this reasoning into concise keywords that minimize the impact of outliers. 
ユーザーインタラクションをLLMに基づいて直接推測するのではなく（Zhang et al. 2024a; Corecco et al. 2024）、私たちはLLMを使用して、ユーザーがアイテムを好む理由や嫌う理由を抽出し、この推論を簡潔なキーワードに凝縮し、外れ値の影響を最小限に抑えます。
In addition, we complement this with a statistical model, i.e., a trained sequential model, that provides a regularizing effect on the predictions. 
さらに、予測に正則化効果を提供する訓練された逐次モデルなどの統計モデルを補完します。
Our ensemble model integrates the strengths of both logical reasoning and statistical learning, enhancing the reliability and efficiency of user interaction simulations synergistically. 
私たちのアンサンブルモデルは、論理的推論と統計学習の両方の強みを統合し、ユーザーインタラクションシミュレーションの信頼性と効率を相乗的に向上させます。

<!-- ここまで読んだ! -->

Third, how to evaluate the user simulator? 
第三に、ユーザーシミュレーターをどのように評価するかです。
Lacking a standardized metric for evaluation, we face the challenge of assessing the effectiveness of our user simulator. 
標準化された評価指標が欠如しているため、私たちはユーザーシミュレーターの効果を評価するという課題に直面しています。
To tackle this, we establish a series of experiments that span a wide range of applications, i.e., five public datasets encompassing POI, music, movie, game, and anime recommendation, to ensure that our tests are generalizable. 
これに対処するために、私たちは、POI、音楽、映画、ゲーム、アニメ推薦を含む5つの公開データセットを網羅する幅広いアプリケーションにわたる一連の実験を確立し、私たちのテストが一般化可能であることを保証します。
By training reinforcement learning algorithms within these domains and comparing their performance, we aim to validate the simulator’s ability to provide meaningful insights into user behavior within recommendation systems. 
これらの領域内で強化学習アルゴリズムを訓練し、そのパフォーマンスを比較することで、推薦システム内でユーザー行動に関する有意義な洞察を提供するシミュレーターの能力を検証することを目指します。

<!-- ここまで読んだ! -->

The main contributions of this paper are as follows: 
本論文の主な貢献は以下の通りです。

- We identify the intrinsic logic governing user engagement with items in recommendation, and propose a logical model that explicitly infers user interaction. 
- 推薦におけるアイテムとのユーザーエンゲージメントを支配する内在的な論理を特定し、ユーザーインタラクションを明示的に推測する論理モデルを提案します。

- We construct an ensemble model consisting of rule-based logical and data-driven statistical models to imitate human interaction, maintaining consistency and reducing the likelihood of erroneous inferences. 
- ルールベースの論理モデルとデータ駆動型の統計モデルからなるアンサンブルモデルを構築し、人間のインタラクションを模倣し、一貫性を維持し、誤った推論の可能性を減少させます。

- We conduct both qualifying and quantifying experiments on five benchmark datasets that span a variety of application fields to verify the efficacy of the proposed method. 
- 提案手法の有効性を検証するために、さまざまなアプリケーション分野にわたる5つのベンチマークデータセットで、定性的および定量的な実験を実施します。

<!-- ここまで読んだ! -->

## Methodology 方法論  

### Preliminaries 前提条件

#### User Simulator. 

User simulator in recommendation aims_** to infer the engagement as a real human user with candidate item $i_c$ offered by recommender systems. 
推薦におけるユーザシミュレーターの目的は、推薦システムによって提供される候補アイテム$i_c$に対する実際の人間ユーザとしてのエンゲージメントを推測することです。
It can be formulated as $P(y_c|h, i_c)$, where $y_c$ represents the interaction given by the user simulator, such as rating, buy, and dislike. 
これは $P(y_c|h, i_c)$ として定式化でき、ここで$y_c$はユーザシミュレーターによって与えられるインタラクション（評価、購入、嫌悪など）を表します。 
In this paper, we consider like and dislike for clear descriptions. 
本論文では、明確な説明のために「like」と「dislike」を考慮します。
$h = \{(i_1, y_1), \ldots, (i_n, y_n)\}$ is the user’s historical interactions, consisting of his past responses of $n$ items. 
$h = \{(i_1, y_1), \ldots, (i_n, y_n)\}$ はユーザの過去のインタラクションを表し、$n$ 個のアイテムに対する彼の過去の応答で構成されています。
(hはhistory的な意味か...!:thinking:)

<!-- ここまで読んだ! -->

### Framework Overview フレームワークの概要

In this section, we implement the user engagement process with recommended items. 
このセクションでは、推奨アイテムとのユーザーエンゲージメントプロセスを実装します。
The workflow of our system is depicted in Figure 2. 
私たちのシステムのワークフローは、図2に示されています。
The sequence of operations proceeds from left to right, beginning with an analysis of the potential item, followed by a comparison with the user’s past interactions, culminating in a reasoned inference. 
操作のシーケンスは左から右へ進み、潜在的なアイテムの分析から始まり、ユーザーの過去のインタラクションとの比較を経て、理論的な推論に至ります。

![]()

To express the logic of user interactions in a clear way, we use LLM to examine items and produce informative descriptions. 
ユーザーインタラクションの論理を明確に表現するために、**私たちはLLMを使用してアイテムを調査し、情報豊富な説明を生成**します。
We extract keywords that indicate why items might be liked or disliked based on both the item’s features and user reviews. 
アイテムの特徴とユーザーレビューの両方に基づいて、アイテムが好まれる理由や嫌われる理由を示すキーワードを抽出します。
We also create an ensemble model consisting of three base models. 
また、3つのベースモデルからなるアンサンブルモデルを作成します。
This model suite evaluates the user’s past preferences and the current item to produce an inference result. 
このモデルスイートは、ユーザーの過去の好みと現在のアイテムを評価して推論結果を生成します。
By combining these models, we aim to deliver a more precise and dependable assessment. 
これらのモデルを組み合わせることで、より正確で信頼性の高い評価を提供することを目指します。

<!-- ここまで読んだ! -->

### Objective Item Description Collection 目的項目説明の収集

To discern what the item is, we initially leverage the items’ factual descriptions. 
アイテムが何であるかを見極めるために、最初にアイテムの事実に基づく説明を活用します。
Our approach is to pinpoint the category Dcate and delineate objective reasons for liking or disliking the item, i.e., Dpos and Dneg. 
**私たちのアプローチは、カテゴリ $D_{cate}$ を特定し、アイテムを好む理由や嫌う理由を明確にすること、すなわち $D_{pos}$ と $D_{neg}$ を定義すること**です。
This objective item description analysis contributes to a comprehensive understanding of the item’s attributes and potential user reactions.  
この客観的なアイテム説明分析は、アイテムの属性と潜在的なユーザーの反応を包括的に理解することに寄与します。

For item categorization Dcate, we extract textual genre descriptions from the raw data, filtering out the most and least frequent categories. 
アイテムのカテゴリ分けDcateのために、私たちは生データからテキストのジャンル説明を抽出し、最も頻繁なカテゴリと最も少ないカテゴリをフィルタリングします。このプロセスにより、各アイテムには特異性と関連性のバランスを取った最終カテゴリが割り当てられ、過度の一般化やカテゴリ表現の過剰な断片化を避けることができます。

To attain the potential reasons behind user preferences for items Dpos and Dneg, we start with the fundamental details such as the item’s name, category, and attributes. 
アイテムDposおよびDnegに対するユーザの好みの背後にある潜在的な理由を明らかにするために、私たちはアイテムの名前、カテゴリ、属性などの基本的な詳細から始めます。 
Employing an LLM, we generate objective descriptions that encompass the possible factors influencing a user’s affinity or aversion towards the item.
LLMを使用して、私たちはユーザのアイテムに対する親和性や嫌悪感に影響を与える可能性のある要因を含む客観的な説明を生成します。 
Take the movie recommendation as example again, we craft a prompt template Tobj that integrates the available information. 
映画推薦を再度例に挙げると、私たちは利用可能な情報を統合したプロンプトテンプレート $T_{obj}$ を作成する。
Tobj is shown as follows, where NAME, ATTRIBUTES, and CATEGORIES will be filled with item information from raw data, and the response will fill the placeholder in red text:  
$T_{obj}$  は以下のように示され、NAME、ATTRIBUTES、およびCATEGORIESは生データからのアイテム情報で埋められ、応答は赤いテキストのプレースホルダーを埋めます。

```text
hoge
```

Given the LLM’s response according to the form of Tobj, we extract the keywords that represent positive aspects as _Dpos[obj]_ [and those that signify negative aspects as][ D]neg[obj] [. 
LLMの$T_{obj}$ に基づく応答を受けて、ポジティブな側面を表すキーワードを $D_{pos}^{obj}$ と、ネガティブな側面を示すキーワードを $D_{neg}^{obj}$ として抽出します。
Consequently, Dpos[obj] [and][ D]neg[obj] [emerge as curated lists of keywords,] effectively encapsulating the essence of users’ potential attitudes towards items. 
**その結果、$D_{pos}^{obj}$ と $D_{neg}^{obj}$ はキュレーションされたキーワードのリストとして現れ、ユーザのアイテムに対する潜在的な態度の本質を効果的に要約します**。 
These keyword sets serve as concise, informative indicators, reflecting the likely inclinations of user preferences or aversions in a distilled form. 
これらのキーワードセットは、ユーザの好みや嫌悪の傾向を凝縮した形で反映する簡潔で情報豊富な指標として機能します。

<!-- ここまで読んだ! -->

When harnessing the power of LLMs to generate reasons for potential user likes and dislikes, we integrate the Chain of Thoughts (CoT) (Wei et al. 2022; Chu et al. 2023) approach to bolster the precision and reliability of the LLM’s output. 
LLMの力を利用してユーザの好みや嫌悪の理由を生成する際、私たちはChain of Thoughts (CoT) (Wei et al. 2022; Chu et al. 2023)アプローチを統合し、LLMの出力の精度と信頼性を高めます。

In particular, we guide the LLM to first identify the concrete reasons behind the likes and dislikes using the provided keywords and then summarize the reasons into concise keywords. 
特に、私たちはLLMに提供されたキーワードを使用して好みや嫌悪の具体的な理由を特定させ、その後、理由を簡潔なキーワードに要約させます。

Finally, we require LLM to substantiate these reasons with evidence drawn from the information provided. 
最後に、私たちはLLMに提供された情報から得られた証拠でこれらの理由を裏付けるよう要求します。

This process helps circumvent the risk of hallucination inherent in LLMs, ensuring that the generated reasons are well-founded and relevant. 
このプロセスは、LLMに内在する幻覚のリスクを回避するのに役立ち、生成された理由が根拠があり関連性があることを保証します。

This prompt is engineered to inspire a detailed analysis from the LLM regarding the item’s factual characteristics. 
このプロンプトは、アイテムの事実的な特性に関するLLMからの詳細な分析を促すように設計されています。

It encourages the model to consider the full spectrum of attributes from the most appealing features to the possible shortcomings. 
これは、モデルに最も魅力的な特徴から可能性のある欠点まで、属性の全範囲を考慮するよう促します。

By demanding a logical sequence of identification and justification, the LLM’s output is not only informative but also transparent in its reasoning, aligning closely with how human users might evaluate the item. 
識別と正当化の論理的な順序を要求することにより、LLMの出力は情報豊富であるだけでなく、その推論も透明であり、人間のユーザがアイテムを評価する方法に密接に一致します。



#### Subjective Item Description Collection 主観的アイテム説明収集

To comprehend how a user views an item, public opinions can greatly influence the decision-making process. 
ユーザーがアイテムをどのように見ているかを理解するために、公共の意見は意思決定プロセスに大きな影響を与える可能性があります。 
For example, a considerable proportion of users tend to choose mainstream options. 
例えば、かなりの割合のユーザーは主流の選択肢を選ぶ傾向があります。 
Hence, we examine the comments to find keywords that indicate liking or disliking sentiments. 
したがって、私たちはコメントを調査し、好意や嫌悪の感情を示すキーワードを見つけます。

3] Evidence: [evidence of cons 3] 
3] 証拠: [cons 3の証拠] 
Keywords: [keywords of cons 3]  
キーワード: [cons 3のキーワード]  

Objective Description Prompt Template Tobj 
目的の説明プロンプトテンプレート Tobj 
Given a Movie named NAME and its characteristics, I need you to provide pros and cons, corresponding evidence and keywords from a customer perspective. 
NAMEという映画とその特徴が与えられた場合、顧客の視点から利点と欠点、対応する証拠とキーワードを提供する必要があります。 
Movie has the following attributes: ATTRIBUTES. 
映画には次の属性があります: ATTRIBUTES。 
Categories of the movie include CATEGORIES. 
映画のカテゴリにはCATEGORIESが含まれます。 
Reasons, keywords, and evidence should be concise and reasonable. 
理由、キーワード、および証拠は簡潔で合理的であるべきです。 
Keywords should appear positive or negative. 
キーワードは肯定的または否定的であるべきです。 
Evidence should refer to the information given. 
証拠は与えられた情報を参照するべきです。 
Strictly follow the reply format, fill [], do not say anything else: 
厳密に返信フォーマットに従い、[]を埋めて、他のことは言わないでください: 
Pros 1: [pros 1] 
利点 1: [pros 1] 
Evidence: [evidence of pros 1] 
証拠: [pros 1の証拠] 
Keywords: [keywords of pros 1] 
キーワード: [pros 1のキーワード] 
Pros 2: [pros 2] 
利点 2: [pros 2] 
Evidence: [evidence of pros 2] 
証拠: [pros 2の証拠] 
Keywords: [keywords of pros 2] 
キーワード: [pros 2のキーワード] 
Pros 3: [pros 3] 
利点 3: [pros 3] 
Evidence: [evidence of pros 3] 
証拠: [pros 3の証拠] 
Keywords: [keywords of pros 3] 
キーワード: [pros 3のキーワード] 
Cons 1: [cons 1] 
欠点 1: [cons 1] 
Evidence: [evidence of cons 1] 
証拠: [cons 1の証拠] 
Keywords: [keywords of cons 1] 
キーワード: [cons 1のキーワード] 
Cons 2: [cons 2] 
欠点 2: [cons 2] 
Evidence: [evidence of cons 2] 
証拠: [cons 2の証拠] 
Keywords: [keywords of cons 2] 
キーワード: [cons 2のキーワード] 
Cons 3: [cons 3] 
欠点 3: [cons 3] 
Evidence: [evidence of cons 3] 
証拠: [cons 3の証拠] 
Keywords: [keywords of cons 3] 
キーワード: [cons 3のキーワード]  

To accomplish this, we devise a prompt template Tsub that encompasses the item’s descriptions and the user’s feedback. 
これを達成するために、アイテムの説明とユーザーのフィードバックを包含するプロンプトテンプレート Tsubを考案します。 
We ensure that the LLM is instructed to generate reasons for a positive rating when the user provides one, and vice versa for negative ratings. 
ユーザーがポジティブな評価を提供した場合にはその理由を生成し、ネガティブな評価の場合にはその逆を生成するようにLLMに指示します。 
For instance, when presenting a prompt for a positive rating, we use “Pros”; we use “Cons” for a negative rating. 
例えば、ポジティブな評価のプロンプトを提示する際には「Pros」を使用し、ネガティブな評価には「Cons」を使用します。 
The template Tsub with positive rating is illustrated as follows, with placeholders for RATING, COMMENTS, NAME, ATTRIBUTES, and CATEGORIES to be filled with actual data. 
ポジティブな評価のテンプレート Tsubは以下のように示され、RATING、COMMENTS、NAME、ATTRIBUTES、およびCATEGORIESのプレースホルダーが実際のデータで埋められます。 
The LLM’s response will answer the query indicated by the placeholder in red text. 
LLMの応答は、赤いテキストで示されたプレースホルダーのクエリに答えます。 

Subjective Description Prompt Template Tsub 
主観的説明プロンプトテンプレート Tsub 
A customer rates RATING to the movie with comments: COMMENTS 
顧客が映画にRATINGを付け、コメントを残します: COMMENTS 
The information of this movie is: name: NAME, attributes: ATTRIBUTES, categories: CATEGORIES. 
この映画の情報は次のとおりです: 名前: NAME、属性: ATTRIBUTES、カテゴリ: CATEGORIES。 
I need you to provide Pros, corresponding evidence and keywords of the rating based on given information. 
与えられた情報に基づいて、利点、対応する証拠、および評価のキーワードを提供する必要があります。 
Evidence should refer to the information given. 
証拠は与えられた情報を参照するべきです。 
Strictly follow the reply format, fill [], do not say anything else: 
厳密に返信フォーマットに従い、[]を埋めて、他のことは言わないでください: 
Pros 1: [pros 1] 
利点 1: [pros 1] 
Keywords: [keywords of pros 1] 
キーワード: [pros 1のキーワード] 
Evidence: [evidence of pros 1] 
証拠: [pros 1の証拠] 
Pros 2: [pros 2] 
利点 2: [pros 2] 
Keywords: [keywords of pros 2] 
キーワード: [pros 2のキーワード] 
Evidence: [evidence of pros 2] 
証拠: [pros 2の証拠] 
Pros 3: [pros 3] 
利点 3: [pros 3] 
Keywords: [keywords of pros 3] 
キーワード: [pros 3のキーワード] 
Evidence: [evidence of pros 3] 
証拠: [pros 3の証拠] 

Similar to our approach with Tobj, we prompt the LLM to list the pros, their associated keywords, and supporting evidence, aiming for an output that is both reliable and wellsubstantiated. 
Tobjでのアプローチと同様に、LLMに利点、その関連キーワード、および支持する証拠をリストするように促し、信頼性が高く十分に裏付けられた出力を目指します。 
From the LLM’s response, we extract the keywords that indicate positive aspects as Dpos[sub] [and those indi-] cating negative aspects as Dneg[sub] [. 
LLMの応答から、ポジティブな側面を示すキーワードをDpos[sub]として抽出し、ネガティブな側面を示すキーワードをDneg[sub]として抽出します。 
Upon obtaining the lists of keywords that represent likes and dislikes from both the objective and subjective standpoints, we combine these lists to form comprehensive sets: 
客観的および主観的な観点からの好みと嫌悪を表すキーワードのリストを取得した後、これらのリストを結合して包括的なセットを形成します: 
_Dpos = Dpos[obj]_ _[∪][D]pos[sub]_ [and][ D][neg] [=][ D]neg[obj] _[∪][D]neg[sub]_ [. 
_Dpos = Dpos[obj]_ _[∪][D]pos[sub]_ [および][ D][neg] [=][ D]neg[obj] _[∪][D]neg[sub]_ [。 
By merging these keyword lists, we develop a holistic view of the potential inclinations users may have towards items. 
これらのキーワードリストを統合することで、ユーザーがアイテムに対して持つ可能性のある傾向の全体像を構築します。 
This synthesis allows us to better anticipate and understand the diverse motivations that drive user preferences and behaviors in the context of recommendations. 
この統合により、推薦の文脈におけるユーザーの好みや行動を駆動する多様な動機をよりよく予測し理解することができます。 

We then apply a filtering process to refine these keywords, excluding those that are either too common or too rare. 
次に、これらのキーワードを洗練させるためのフィルタリングプロセスを適用し、あまりにも一般的またはあまりにも珍しいものを除外します。 
This ensures that the keywords we retain are both informative and concise, effectively capturing the essence of item factual information and real users’ subjective opinions. 
これにより、保持するキーワードが情報的かつ簡潔であり、アイテムの事実情報と実際のユーザーの主観的意見の本質を効果的に捉えることができます。 

In summary, we have attained informative textual descriptions for each item, including category Dcate, a set of keywords reflecting reasons for liking Dpos, and disliking keywords Dneg. 
要約すると、私たちは各アイテムに対して情報的なテキスト記述を取得し、カテゴリDcate、好意の理由を反映するキーワードのセットDpos、および嫌悪のキーワードDnegを含んでいます。 
This comprehensive characterization equips our user simulation with a deeper understanding of the items’ attributes and the potential reactions from users. 
この包括的な特徴付けにより、私たちのユーザーシミュレーションはアイテムの属性とユーザーからの潜在的な反応をより深く理解することができます。



#### Logical Model 論理モデル

Following the explicit user interaction logic, we design a logical model to simulate user engagement with the recommended candidate item.  
明示的なユーザーインタラクションの論理に従い、推奨された候補アイテムに対するユーザーのエンゲージメントをシミュレートするための論理モデルを設計します。  
To decide whether to like or dislike a candidate item, users consider the characteristics of historical liking items and the potential reasons for liking candidate items and compare them with the characteristics of historical disliking items and the potential reasons for disliking candidate items.  
候補アイテムを好むか嫌うかを決定するために、ユーザーは過去に好まれたアイテムの特性と候補アイテムを好む可能性のある理由を考慮し、それを過去に嫌われたアイテムの特性や候補アイテムを嫌う可能性のある理由と比較します。  
In this subsection, we devise two types of logical models leveraging the distilled information of items, i.e., keywords matching model and similarity calculation model.  
この小節では、アイテムの抽出された情報を活用した2種類の論理モデル、すなわちキーワードマッチングモデルと類似度計算モデルを考案します。  

**Keywords Matching Model キーワードマッチングモデル**  
Given user’s historical interacted item list $h = \{(i_k, y_k)\}_{k=1}^{n}$ [containing indicative features,]  
ユーザーの過去にインタラクションしたアイテムリスト $h = \{(i_k, y_k)\}_{k=1}^{n}$ [は、指標となる特徴を含んでいます。]  
we design a keywords matching model, which concentrates on the direct matching of textual keywords.  
私たちは、テキストキーワードの直接的なマッチングに集中するキーワードマッチングモデルを設計します。  
Firstly, to retrieve user’s preference explicitly, we extract historical interacted items with the same category of $i_c$, noted as $h_C := \{(i_k, y_k)\}_{k=1}^{C}$ [with]  
まず、ユーザーの好みを明示的に取得するために、$i_c$と同じカテゴリの過去にインタラクションしたアイテムを抽出し、$h_C := \{(i_k, y_k)\}_{k=1}^{C}$ [と記載します。]  
items. When there are no historical items with the same category, we set $h_C = h$.  
同じカテゴリの過去のアイテムがない場合、$h_C = h$と設定します。  
Then, we extract item set from $h_C$ with positive rating $y_k = 1$ as historical liking items $I_{pos} := \{i_k\}_{k=1}^{C_{pos}}$ [and item set]  
次に、$h_C$から正の評価 $y_k = 1$ を持つアイテムセットを過去に好まれたアイテム $I_{pos} := \{i_k\}_{k=1}^{C_{pos}}$ [として抽出します。]  
with negative rating $y_k = 0$ as historical disliking items $I_{neg} := \{i_k\}_{k=1}^{C_{neg}}$, [where]  
負の評価 $y_k = 0$ を持つアイテムセットを過去に嫌われたアイテム $I_{neg} := \{i_k\}_{k=1}^{C_{neg}}$ [として抽出します。]  
where $C = C_{pos} + C_{neg}$.  
ここで、$C = C_{pos} + C_{neg}$です。  
Given the user historical preference $I_{pos}$ and $I_{neg}$, we design a keywords matching model $f_{mat}(I_{pos}, I_{neg}, i_c)$ to infer the user’s inclination towards liking or disliking candidate item $i_c$.  
ユーザーの過去の好み $I_{pos}$ と $I_{neg}$ を考慮して、候補アイテム $i_c$ を好むか嫌うかのユーザーの傾向を推測するためのキーワードマッチングモデル $f_{mat}(I_{pos}, I_{neg}, i_c)$ を設計します。  
To implement this, we calculate the number of matched keywords of historical liking reasons, i.e., $D_{pos}$ of items in $I_{pos}$, and potential liking reasons for the candidate item, i.e., $D_{pos}$ of $i_c$.  
これを実装するために、過去に好まれた理由のマッチしたキーワードの数、すなわち $I_{pos}$ のアイテムの $D_{pos}$ と、候補アイテムの潜在的な好まれる理由、すなわち $i_c$ の $D_{pos}$ を計算します。  
Similarly, we calculate the alignment of historical disliking reasons, i.e., $D_{neg}$ of items in $I_{neg}$ and potential disliking reasons of candidate item, i.e., $D_{neg}$ of $i_c$.  
同様に、過去に嫌われた理由の整合性、すなわち $I_{neg}$ のアイテムの $D_{neg}$ と候補アイテムの潜在的な嫌われる理由、すなわち $i_c$ の $D_{neg}$ を計算します。  
Denote the keywords for positive and negative reasons of item $i$ with $D_{pos}[i]$ [and] $D_{neg}[i]$, [respectively. The number of]  
アイテム $i$ の好まれる理由と嫌われる理由のキーワードをそれぞれ $D_{pos}[i]$ [および] $D_{neg}[i]$ [とします。マッチしたキーワードの数は]  
matched keywords for positive and negative attitudes $\alpha_{pos}$ and $\alpha_{neg}$ can be formulated as:  
好まれる態度と嫌われる態度のマッチしたキーワードの数 $\alpha_{pos}$ と $\alpha_{neg}$ は次のように定式化できます。  

$$
\alpha_{pos} = \left| D_{pos}[i_c] \cap D_{pos}[i] \right| \quad (1)  
_{i \in I_{pos}}  
$$  

**Similarity Calculation Model 類似度計算モデル**  
To enhance the underlying interaction logic simulation process beyond mere keyword matching, we introduce similarity calculation model $f_{sim}(I_{pos}, I_{neg}, I_c)$ that leverages embedding representations for a nuanced understanding of user preferences.  
単なるキーワードマッチングを超えて、基盤となるインタラクションロジックのシミュレーションプロセスを強化するために、ユーザーの好みをより深く理解するために埋め込み表現を活用する類似度計算モデル $f_{sim}(I_{pos}, I_{neg}, I_c)$ を導入します。  
Akin to the keywords matching model, this model focuses on the relationship among items within the same category $h_C$ and its respective positive and negative subsets, i.e., $I_{pos}$ and $I_{neg}$.  
キーワードマッチングモデルと同様に、このモデルは同じカテゴリ $h_C$ 内のアイテム間の関係と、それぞれの正のサブセット $I_{pos}$ と負のサブセット $I_{neg}$ に焦点を当てます。  

$$
\alpha_{neg} = \left| D_{neg}[i_c] \cap D_{neg}[i] \right| \quad (2)  
_{i \in I_{neg}}  
$$  

$\alpha_{pos}$ と $\alpha_{neg}$ は、候補アイテムの好まれる/嫌われる理由とユーザーの過去の好みとの重なりの度合いを捉え、アイテムに対するユーザーの潜在的な傾向を定量化します。  
The keywords matching model can be represented by Eq. 3:  
キーワードマッチングモデルは次のように表現できます。  

$$
f_{mat}(I_{pos}, I_{neg}, i_c) =  
\begin{cases}  
1 & \text{if } \alpha_{pos} > \alpha_{neg} \\  
\text{rand}\{0, 1\} & \text{if } \alpha_{pos} = \alpha_{neg} \\  
0 & \text{if } \alpha_{pos} < \alpha_{neg}  
\end{cases} \quad (3)  
$$  

-----
Table 1: Dataset statistics.  
表1: データセットの統計。  
**Dataset** #Users #Items #Instances Sparsity  
**Yelp** 15,081 10,186 228,000 99.85%  
**Amazon Music** 125,627 65,019 162,261 99.99%  
**Amazon Games** 30,195 23,096 165,571 99.98%  
**Amazon Movie** 24,191 49,154 972,536 99.92%  
**Anime** 24,859 11,188 6,111,860 97.80%  

$I_{neg}$ このカテゴリ分析により、特定のカテゴリに固有のパターンや好みを識別でき、ユーザーの傾向推測の精度が向上します。  
Initially, we employ a representative backbone model to transform keywords into embeddings in the semantic space.  
最初に、キーワードを意味空間の埋め込みに変換するための代表的なバックボーンモデルを使用します。  
Specifically, we harness the capabilities of BERT (Devlin 2018) to produce embeddings that capture the semantic richness of each keyword set, calculating $E_{pos}$ as the average pooling of the embeddings of the elements in $D_{pos}$, and similarly, $E_{neg}$ as the average pooling of the embeddings in $D_{neg}$, as shown in Eqs. 4 and 5:  
具体的には、BERT (Devlin 2018) の能力を活用して、各キーワードセットの意味的な豊かさを捉える埋め込みを生成し、$D_{pos}$ の要素の埋め込みの平均プーリングとして $E_{pos}$ を計算し、同様に $D_{neg}$ の埋め込みの平均プーリングとして $E_{neg}$ を計算します。  

$$
E_{pos} = \text{AvePool}\{Bert(d) | d \in D_{pos}\} \quad (4)  
$$  

$$
E_{neg} = \text{AvePool}\{Bert(d) | d \in D_{neg}\} \quad (5)  
$$  

We then proceed to assess the closeness of the candidate item’s pros and cons to those of historically liked or disliked items.  
次に、候補アイテムの利点と欠点が過去に好まれたアイテムや嫌われたアイテムにどれだけ近いかを評価します。  
We calculate similarities between the keywords embedding of the user’s positively rated items, i.e., $E_{pos}$ of items in $I_{pos}$, and embedding of pros from candidate item, i.e., $E_{pos}$ of $i_c$.  
ユーザーの正の評価を受けたアイテムのキーワード埋め込み、すなわち $I_{pos}$ のアイテムの $E_{pos}$ と、候補アイテムの利点の埋め込み、すなわち $i_c$ の $E_{pos}$ の間の類似度を計算します。  
Meanwhile, we calculate similarities between the keywords embedding of the user’s negatively rated items, i.e., $E_{neg}$ of items in $I_{neg}$, and the cons from candidate item, i.e., $E_{neg}$ of $i_c$.  
同時に、ユーザーの負の評価を受けたアイテムのキーワード埋め込み、すなわち $I_{neg}$ のアイテムの $E_{neg}$ と、候補アイテムの欠点の埋め込み、すなわち $i_c$ の $E_{neg}$ の間の類似度を計算します。  
The similarity between keywords for positive and negative attitudes $\beta_{pos}$ and $\beta_{neg}$ can be mathematically presented as follows, where $\phi$ represents similarity metric, and we use cosine similarity.  
好まれる態度と嫌われる態度のキーワード間の類似度 $\beta_{pos}$ と $\beta_{neg}$ は次のように数学的に表現できます。ここで、$\phi$ は類似度指標を表し、コサイン類似度を使用します。  

$$
\beta_{pos} = \max\{\phi(E_{pos}[i_c], E_{pos}[i]) | i \in I_{pos}\} \quad (6)  
$$  

$$
\beta_{neg} = \max\{\phi(E_{neg}[i_c], E_{neg}[i]) | i \in I_{neg}\} \quad (7)  
$$  

This comparison with the cosine similarity metric provides a quantifiable and interpretable measure of how the candidate item aligns with the user’s historical preferences.  
このコサイン類似度指標との比較は、候補アイテムがユーザーの過去の好みにどれだけ一致しているかを定量化可能で解釈可能な尺度を提供します。  
The similarity calculation model can be formulated as Eq. 8:  
類似度計算モデルは次のように定式化できます。  

This approach introduces the power of traditional statistical model, trained on user historical interaction data, to predict the user’s inclination towards a candidate item.  
このアプローチは、ユーザーの過去のインタラクションデータで訓練された従来の統計モデルの力を導入し、候補アイテムに対するユーザーの傾向を予測します。  
It enhances the reliability of the user simulator by integrating statistical learning with logical reasoning.  
統計学習と論理的推論を統合することで、ユーザーシミュレーターの信頼性を向上させます。  



#### Ensemble User Simulator アンサンブルユーザシミュレーター

Given the established two logical models, i.e., keywords matching model fmat and similarity calculation model fsim, and statistic model fsta, we construct an ensemble model to synergize the user interaction simulation performance.
確立された2つの論理モデル、すなわちキーワードマッチングモデルfmatと類似度計算モデルfsim、そして統計モデルfstaを考慮して、ユーザインタラクションシミュレーションのパフォーマンスを強化するためのアンサンブルモデルを構築します。

By integrating the strengths of both logical reasoning and statistical learning, our ensemble model offers a comprehensive and robust framework for simulating user preferences and behaviors in recommendation scenarios.
論理的推論と統計的学習の両方の強みを統合することにより、私たちのアンサンブルモデルは、推薦シナリオにおけるユーザの好みや行動をシミュレートするための包括的で堅牢なフレームワークを提供します。

Next we introduce the training pipeline with reinforcement learning-based recommender system in this subsection.
次に、この小節では強化学習に基づくレコメンダーシステムのトレーニングパイプラインを紹介します。



#### MDP Formulation MDPの定式化

In reinforcement learning-based recommender system training, the sequential item interactions can be formulated by a Markov Decision Process (MDP) (Puterman 1990). 
強化学習に基づく推薦システムのトレーニングでは、逐次的なアイテムの相互作用をマルコフ決定過程（MDP）として定式化できます（Puterman 1990）。 
In this pipeline, recommender system serves as an agent, user interaction and preference are the environments, recommendation of item is action, user’s response towards recommendation is the reward signal.
このパイプラインでは、推薦システムがエージェントとして機能し、ユーザーの相互作用と嗜好が環境となり、アイテムの推薦が行動、推薦に対するユーザーの反応が報酬信号となります。

- State (s ∈S): the set of all possible states of the environment, including user profile, historical interactions h, and current context including Ipos and Ineg.
- 状態 (s ∈S): ユーザープロファイル、過去の相互作用 h、現在のコンテキスト（IposおよびInegを含む）を含む環境のすべての可能な状態の集合。
- Action (ic ∈A): the set of all possible actions the recommender system can take, where an action represents one recommended item ic.
- 行動 (ic ∈A): 推薦システムが取ることのできるすべての可能な行動の集合であり、行動は1つの推薦アイテム ic を表します。
- Transition Probabilities (P(s[′]|s, ic)): the probabilities of transitioning to a new state s[′] given the current state s and action ic from recommender system.
- 遷移確率 (P(s[′]|s, ic)): 現在の状態 s と推薦システムからの行動 ic に基づいて新しい状態 s[′] に遷移する確率。
- Reward Function (R(s, ic, s[′])): assigns a numerical reward to each transition from state s to s[′] by action ic.
- 報酬関数 (R(s, ic, s[′])): 行動 ic によって状態 s から s[′] への各遷移に数値的な報酬を割り当てます。

We craft an ensemble model to serve as the user simulator, and the reward function is determined by the consensus reached among three constituent base models, which could be formulated as Eq. 9:
ユーザーシミュレーターとして機能するアンサンブルモデルを作成し、報酬関数は3つの構成ベースモデル間で達成された合意によって決定されます。これは式 (9) のように定式化できます：
$$
R(s, ic, s[′]) = 
\begin{cases} 
1 & \text{if } fmat + fsim + fsta \geq 2, \\ 
0 & \text{if } fmat + fsim + fsta < 2. 
\end{cases}
$$

- Discount Factor γ: A number between 0 and 1 used to discount future rewards.
- 割引因子 γ: 将来の報酬を割引くために使用される0と1の間の数値。



### Experiments 実験

#### Experimental Setup 実験設定

To verify the efficacy of the proposed ensemble user simulator, we incorporate datasets from diverse fields: Yelp[1] (the state of Missouri), Amazon[2] (Digital Music, Video Games, 
提案されたアンサンブルユーザシミュレーターの有効性を検証するために、私たちは多様な分野からのデータセットを取り入れます：Yelp[1]（ミズーリ州）、Amazon[2]（デジタル音楽、ビデオゲーム、

1 https://www.yelp.com/dataset/documentation/main  
2 https://nijianmo.github.io/amazon/index.html  

1 _if_ _βpos > βneg,_ _rand{0, 1}_ _if_ _βpos = βneg,_ 0 _if_ _βpos < βneg._ (8)  
1 _もし_ _βpos > βneg_ の場合、_rand{0, 1}_ _もし_ _βpos = βneg_ の場合、0 _もし_ _βpos < βneg_ の場合。 (8)  

_fsim(Ipos, Ineg, ic) =_  
_fsim(Ipos, Ineg, ic) =_  



#### Statistic Model 統計モデル

Beyond the two logical models, we augment our user simulator with a statistical model to enhance the reliability of the generated user inferences. 
2つの論理モデルを超えて、私たちは生成されたユーザー推論の信頼性を高めるために、ユーザーシミュレーターに統計モデルを追加します。

To achieve this, we employ a deep model, SASRec (Kang and McAuley 2018), and train on the user’s historical interaction data. 
これを実現するために、私たちは深層モデルであるSASRec（Kang and McAuley 2018）を使用し、ユーザーの過去のインタラクションデータでトレーニングします。

Specifically, we pretrain the statistical model fsta(h, ic) with the dataset. 
具体的には、データセットを用いて統計モデルfsta(h, ic)を事前トレーニングします。

Subsequently, we load the pretrained model parameter to infer the engagement with the candidate item.  
その後、事前トレーニングされたモデルパラメータをロードして、候補アイテムとのエンゲージメントを推測します。

-----
Table 2: Overall performance. A. Rwd and T. Rwd represent average and total rewards, respectively. Liking% is the liking items ratio in the top-10 recommendations.
表2: 全体のパフォーマンス。A. RwdとT. Rwdはそれぞれ平均報酬と総報酬を表します。Liking%はトップ10の推薦アイテムにおける好まれるアイテムの比率です。

**Dataset** **Metric** PPO TRPO A2C DQN  
**A. Rwd↑** 9.97 13.45 24.15 **27.56**  
**Yelp** **T. Rwd↑** 141.57 157.42 267.60 **330.98**  
**Liking%↑** 34.59 40.07 48.35 **49.43**  
**Amazon** **A. Rwd↑** 10.49 11.31 13.45 **16.70**  
**Music** **T. Rwd↑** 129.03 140.15 141.03 **181.42**  
**Liking%↑** 29.30 32.46 29.54 **33.18**  
**Amazon** **A. Rwd↑** 18.72 21.35 **27.56** 26.43  
**Games** **T. Rwd↑** 208.43 242.26 **317.56** 269.02  
**Liking%↑** 33.15 37.64 **43.52** 40.73  
**Amazon** **A. Rwd↑** 29.42 27.47 31.72 **38.60**  
**Movie** **T. Rwd↑** 310.69 301.40 354.34 **416.18**  
**Liking%↑** 38.59 36.70 42.37 **44.50**  
**A. Rwd↑** 14.12 14.58 **21.50** 18.03  
**Anime** **T. Rwd↑** 155.74 163.44 **242.95** 201.94  
**Liking%↑** 25.46 24.27 **31.52** 30.67  

and Movies), and Anime[3]. Dataset statistics are shown in Table 1. 
および映画、アニメ[3]。データセットの統計は表1に示されています。

We convert ratings into a binary format, where a rating is marked as ’1’ if it is 3 or higher and ’0’ for ratings below 3. 
私たちは評価をバイナリ形式に変換します。評価が3以上の場合は「1」とし、3未満の場合は「0」とします。

We use ChatGLM-6B[4] as our LLM. 
私たちはChatGLM-6B[4]をLLMとして使用します。

We employ several representative reinforcement learning algorithms: A2C (Mnih et al. 2016), DQN (Mnih et al. 2013), PPO (Schulman et al. 2017), and TRPO (Schulman et al. 2015). 
私たちは、いくつかの代表的な強化学習アルゴリズムを採用します：A2C（Mnih et al. 2016）、DQN（Mnih et al. 2013）、PPO（Schulman et al. 2017）、およびTRPO（Schulman et al. 2015）。



#### Benchmark Results ベンチマーク結果

We provide the results of reinforcement learning algorithms on our user simulator and report the average reward, total reward, and liking ratio. 
私たちは、ユーザシミュレーター上での強化学習アルゴリズムの結果を提供し、平均報酬、総報酬、および好意比率を報告します。

Experimental results are shown in Table 2. 
実験結果は表2に示されています。

The results indicate that DQN consistently outperforms other algorithms, a result that can be attributed to its superior capacity for handling tasks with discrete action spaces. 
結果は、DQNが他のアルゴリズムを一貫して上回っていることを示しており、これは離散的なアクション空間を持つタスクを処理する優れた能力に起因しています。

DQN combines Q-learning with deep learning and excels at estimating the expected return for each action. 
DQNはQ学習と深層学習を組み合わせており、各アクションの期待リターンを推定するのに優れています。

The robust performance of DQN in the simulator is likely bolstered by its use of experience replay and target networks. 
シミュレーターにおけるDQNの堅牢なパフォーマンスは、経験再生とターゲットネットワークの使用によって強化されている可能性があります。

Besides, all algorithms exhibit good liking ratio of recommendation, which suggests that the user simulator provides a consistent environment where different algorithms can perform their interactions with the recommended items over a similar timescale. 
さらに、すべてのアルゴリズムは推薦の好意比率が良好であり、これはユーザシミュレーターが異なるアルゴリズムが推薦アイテムとの相互作用を類似のタイムスケールで行うことができる一貫した環境を提供していることを示唆しています。

The user simulator can produce consistent and reliable interaction patterns across different algorithms, showcasing the simulator’s reliability in mimicking real user behavior. 
ユーザシミュレーターは、異なるアルゴリズム間で一貫した信頼性のある相互作用パターンを生成でき、実際のユーザ行動を模倣するシミュレーターの信頼性を示しています。

It highlights the simulator’s strength in replicating genuine user behaviors, which is crucial for accurately assessing algorithmic performance. 
これは、アルゴリズムのパフォーマンスを正確に評価するために重要な、真のユーザ行動を再現するシミュレーターの強みを強調しています。

3https://www.kaggle.com/datasets/CooperUnion/animerecommendations-database 
4https://huggingface.co/THUDM/chatglm-6b



#### Case Study ケーススタディ

In this subsection, we delve into case studies to further demonstrate the effectiveness of our user simulator. 
この小節では、ユーザシミュレーターの効果をさらに示すためにケーススタディに深く掘り下げます。

We first illustrate the recommendations by the DQN on Yelp in Table 3. 
まず、Table 3におけるYelpでのDQNによる推薦を示します。

Due to space limitation, we showcase a selection of 3 historical items (i[t][−][3], i[t][−][2], and i[t][−][1]) and 3 RL recommended items (i[t]c[,][ i][t]c[+1], and i[t]c[+2]) highlighting their notable pros and cons. 
スペースの制約により、3つの歴史的アイテム（i[t][−][3], i[t][−][2], i[t][−][1]）と3つのRL推薦アイテム（i[t]c[,][ i][t]c[+1], and i[t]c[+2]）を選択し、それらの顕著な利点と欠点を強調します。

We omit cons for positive historical items and pros for negative ones. 
ポジティブな歴史的アイテムの欠点とネガティブなアイテムの利点は省略します。

The user simulator’s detailed inference process on the RL recommendations is presented in Table 4. 
ユーザシミュレーターのRL推薦に関する詳細な推論プロセスはTable 4に示されています。

For instance, for i[t]c[, the matching cons with][ i][t][−][1][ results in] a fmat output of 0. 
例えば、i[t]c[の欠点がi[t][−][1]と一致する場合、fmatの出力は0になります。

Similarly, fmat for i[t]c[+2] is 1, as its pros align with those of it−2. 
同様に、i[t]c[+2]のfmatは1であり、その利点はi[t][−][2]の利点と一致します。

The fmat for i[t]c[+1] being 1 is incidental, given the lack of matching pros or cons. 
i[t]c[+1]のfmatが1であるのは、利点や欠点の一致がないため、偶然の結果です。

When faced with items featuring new genres, such as i[t]c[+1], the logical model assesses both the matching of pros and cons and the overall similarity to the historical item set, which may somewhat reduce precision. 
i[t]c[+1]のような新しいジャンルのアイテムに直面したとき、論理モデルは利点と欠点の一致と歴史的アイテムセットとの全体的な類似性の両方を評価し、これが精度を若干低下させる可能性があります。

Nonetheless, our statistical model fsta serves as a crucial fallback. 
それでも、私たちの統計モデルfstaは重要なバックアップとして機能します。

Its collaborative filtering capabilities ensure that the inference remains accurate and well-informed. 
その協調フィルタリング機能により、推論が正確で十分な情報に基づいていることが保証されます。

In conclusion, our ensemble user simulator harnesses the advantages of both logical and statistical models to explicitly generate user interactions that reflect user preferences. 
結論として、私たちのアンサンブルユーザシミュレーターは、論理モデルと統計モデルの両方の利点を活用して、ユーザの好みを反映したユーザインタラクションを明示的に生成します。

The logical model ensures transparency and consistency in user engagement, while the statistical model captures the subtleties of user behavior, enhancing the simulator’s fidelity and effectiveness in emulating real-world user interactions. 
論理モデルはユーザのエンゲージメントにおける透明性と一貫性を保証し、統計モデルはユーザ行動の微妙なニュアンスを捉え、シミュレーターの忠実度と実世界のユーザインタラクションを模倣する効果を高めます。



#### User Simulator Comparison ユーザシミュレーターの比較

To clearly position our user simulator with existing user simulators, we present the main features in Table 5. 
既存のユーザシミュレーターと私たちのユーザシミュレーターを明確に位置付けるために、主な特徴を表5に示します。

For RL-based recommender systems, traditional user simulators typically rely on statistical models to generate user inferences. 
RLベースのレコメンダーシステムにおいて、従来のユーザシミュレーターは通常、統計モデルに依存してユーザの推論を生成します。

our simulator provides a transparent and logical method for inferring user engagement, enhancing transparency and realism. 
私たちのシミュレーターは、ユーザのエンゲージメントを推測するための透明で論理的な方法を提供し、透明性とリアリズムを向上させます。

The reliance on LLMs for inference will inevitably introduce implementation complexity and computational cost, particularly when dealing with large datasets or high-frequency user interactions. 
推論にLLMs（大規模言語モデル）を依存することは、特に大規模データセットや高頻度のユーザインタラクションを扱う際に、実装の複雑さと計算コストを必然的に引き起こします。

Moreover, the hallucination in LLMs can impede performance, which is an issue that still lacks an effective solution. 
さらに、LLMsにおける幻覚（hallucination）はパフォーマンスを妨げる可能性があり、これは依然として効果的な解決策が欠如している問題です。

Unlike other LLM-based simulators that face issues like computational cost and hallucination during training, our approach utilizes the LLM for offline analysis, avoiding direct calls during the training phase and thus mitigating related challenges. 
計算コストやトレーニング中の幻覚といった問題に直面している他のLLMベースのシミュレーターとは異なり、私たちのアプローチはLLMをオフライン分析に利用し、トレーニングフェーズ中の直接呼び出しを避けることで、関連する課題を軽減します。

According to the performance comparison in Table 6, our simulator consistently outperforms the state-of-the-art simulators, which proves its precise approximation to user preference. 
表6のパフォーマンス比較によると、私たちのシミュレーターは常に最先端のシミュレーターを上回っており、ユーザの好みに対する正確な近似を証明しています。

It also achieves competitive efficiency against both LLM- and non-LLM-based simulators. 
また、LLMベースおよび非LLMベースのシミュレーターに対しても競争力のある効率を達成しています。



### Related Works 関連研究

**Traditional User Simulator**  
**従来のユーザシミュレーター**  
To bridge the performance gap between offline metrics and online performance of recommender systems, RecoGym (Rohde et al. 2018) simulates user behavior in e-commerce and their responses  
オフライン指標とレコメンダーシステムのオンラインパフォーマンスの間のパフォーマンスギャップを埋めるために、RecoGym (Rohde et al. 2018) はeコマースにおけるユーザの行動とその反応をシミュレートします。

|Dataset|Metric|PPO TRPO A2C DQN|  
|---|---|---|  
|Yelp|A. Rwd↑ T. Rwd↑ Liking%↑|9.97 13.45 24.15 27.56 141.57 157.42 267.60 330.98 34.59 40.07 48.35 49.43|  
|Amazon Music|A. Rwd↑ T. Rwd↑ Liking%↑|10.49 11.31 13.45 16.70 129.03 140.15 141.03 181.42 29.30 32.46 29.54 33.18|  
|Amazon Games|A. Rwd↑ T. Rwd↑ Liking%↑|18.72 21.35 27.56 26.43 208.43 242.26 317.56 269.02 33.15 37.64 43.52 40.73|  
|Amazon Movie|A. Rwd↑ T. Rwd↑ Liking%↑|29.42 27.47 31.72 38.60 310.69 301.40 354.34 416.18 38.59 36.70 42.37 44.50|  
|Anime|A. Rwd↑ T. Rwd↑ Liking%↑|14.12 14.58 21.50 18.03 155.74 163.44 242.95 201.94 25.46 24.27 31.52 30.67|  

-----

Table 3: RL algorithm recommendation on Yelp. Green grids denote the positive aspects of historical items, and orange ones represent the negative aspects, aligning with the framework in Figure 2.  
表3: YelpにおけるRLアルゴリズムの推薦。緑のグリッドは歴史的アイテムのポジティブな側面を示し、オレンジのグリッドはネガティブな側面を示し、図2のフレームワークに沿っています。

historical items h RL recommendations  
歴史的アイテム h RL 推薦  
|_i[t][−][3]_ |_i[t][−][2]_ |_i[t][−][1]_ |_i[t]c_ |_i[t]c[+1]_ |_i[t]c[+2]_|  
|---|---|---|---|---|---|  
|Name|City|Diner|EI|Maguey|Popeyes|  
|名前|都市|ダイナー|EI|マゲイ|ポパイ|  
|Kitchen|IHOP|Gooey Cakes|Crusoe’s Original|Category|  
|キッチン|IHOP|グーイケーキ|クルーソーのオリジナル|カテゴリ|  
|Restaurants|Restaurants|Restaurants|Restaurants|Bakeries|Restaurants|  
|レストラン|レストラン|レストラン|レストラン|ベーカリー|レストラン|  
|Pros|family gathering|child-friendly|   -|casual|variety|child-friendly|  
|利点|家族の集まり|子供に優しい|   -|カジュアル|多様性|子供に優しい|  
|Cons|   -|   -|loud, crowded|loud|no in-store dining|no reservations|  
|欠点|   -|   -|うるさい、混雑|うるさい|店内飲食なし|予約不可|  
|Rating|1|1|0|   -|   -|  
|評価|1|1|0|   -|   -|  

Table 4: User simulator inference on recommendation.  
表4: 推薦に関するユーザシミュレーターの推論。

Recommendation _fmat_ _fsim_ _fsta_ _R_  
推薦 _fmat_ _fsim_ _fsta_ _R_  
|_i[t]c_|0|0|1|0|  
|_i[t]c[+1]_ |1|0|1|1|  
|_i[t]c[+2]_ |1|1|1|1|  

Table 5: User simulator qualified comparison.  
表5: ユーザシミュレーターの定量的比較。

**Simulators** **Real dataset** **Simulation engine** **Evaluation**  
**シミュレーター** **実データセット** **シミュレーションエンジン** **評価**  
RecoGym ✕ Statistical model case study (Rohde et al. 2018)  
RecSim ✕ Statistical model case study (Ie et al. 2019)  
VirtualTaobao ✓ GAN online (Shi et al. 2019)  
Adversarial ✓ GAN offline (Chen et al. 2019)  
KuaiSim ✓ Transformer offline (Zhao et al. 2023a)  
SUBER ✓ LLM offline & case study (Corecco et al. 2024)  
Agent4Rec ✓ LLM offline & case study (Zhang et al. 2024a)  
LLM-based logical Ours ✓ offline & case study & statistical model  
LLMベースの論理的な我々のもの ✓ オフライン & ケーススタディ & 統計モデル  

to recommendations. Both organic user interactions on ecommerce sites and bandit sessions are incorporated.  
推薦に対して。eコマースサイトでのオーガニックなユーザインタラクションとバンディットセッションの両方が組み込まれています。  
RecSim (Ie et al. 2019) provides a customizable environment for testing user interaction hypotheses, allowing for tailored user preferences, latent states, dynamics, and choice models.  
RecSim (Ie et al. 2019) は、ユーザインタラクションの仮説をテストするためのカスタマイズ可能な環境を提供し、特定のユーザの好み、潜在状態、ダイナミクス、および選択モデルを調整可能にします。  
Virtual-Taobao (Shi et al. 2019) uses GANs for realistic customer feature simulation and multi-agent adversarial imitation learning for generalized customer action generation.  
Virtual-Taobao (Shi et al. 2019) は、現実的な顧客特徴のシミュレーションにGANを使用し、一般化された顧客行動生成のためのマルチエージェント敵対的模倣学習を行います。  
Similarly, Chen et al. (Chen et al. 2019) uses GANs to model online interaction rewards, introducing a model-based RL technique that enhances sample efficiency in policy learning.  
同様に、Chen et al. (Chen et al. 2019) は、オンラインインタラクション報酬をモデル化するためにGANを使用し、ポリシー学習におけるサンプル効率を向上させるモデルベースのRL技術を導入します。  
Kuaisim (Zhao et al. 2023a) integrates a transformer model for user responses and sets benchmarks at the request, session, and cross-session levels for comprehensive recommender system evaluation.  
KuaiSim (Zhao et al. 2023a) は、ユーザの反応のためにトランスフォーマーモデルを統合し、包括的なレコメンダーシステム評価のためにリクエスト、セッション、およびクロスセッションレベルでベンチマークを設定します。  

**LLM-based User Simulator**  
**LLMベースのユーザシミュレーター**  
Given the successful precedents in related areas (Bubeck et al. 2023; Bommasani et al. 2021), there emerge LLM-based user inference simulations leveraging LLM’s outstanding semantic understanding  
関連分野における成功した前例 (Bubeck et al. 2023; Bommasani et al. 2021) を考慮すると、LLMの優れた意味理解を活用したLLMベースのユーザ推論シミュレーションが登場します。

Table 6: User simulator quantified comparison.  
表6: ユーザシミュレーターの定量的比較。

**Metric** **A. Rwd↑** **T. Rwd↑** **AUC↑** **Infer Time(s)**  
**指標** **A. Rwd↑** **T. Rwd↑** **AUC↑** **推論時間(s)**  
SUBER 23.74 297.48 0.643 2.42  
KuaiSim 25.35 316.46 0.658 0.53  
Ours **27.56** **330.98** **0.674** 0.76  

and inferring capability. With an empirical study on ChatGPT’s performance in conversational recommendation using benchmark datasets, Wang et al. (Wang et al. 2023b) advocate to consider two types of interaction: attribute-based question answering and free-form chit-chat.  
および推論能力。ベンチマークデータセットを使用した会話型推薦におけるChatGPTのパフォーマンスに関する実証研究を通じて、Wang et al. (Wang et al. 2023b) は、属性ベースの質問応答と自由形式の雑談という2種類のインタラクションを考慮することを提唱しています。  
Aiming at simulating search users, USimAgent (Zhang et al. 2024b) devises LLM agent to fabricate complete search sessions, including querying, clicking, and stopping behaviors, based on specific search tasks.  
検索ユーザをシミュレートすることを目指して、USimAgent (Zhang et al. 2024b) は、特定の検索タスクに基づいて、クエリ、クリック、および停止行動を含む完全な検索セッションを作成するLLMエージェントを考案します。  
SUBER (Corecco et al. 2024) utilizes LLMs as synthetic users within a gym environment, marking progress towards more realistic training environments for recommender systems.  
SUBER (Corecco et al. 2024) は、ジム環境内で合成ユーザとしてLLMを利用し、レコメンダーシステムのより現実的なトレーニング環境に向けた進展を示しています。  
Agent4Rec (Zhang et al. 2024a) focuses on developing a simulator that accurately reflects user preferences and social traits.  
Agent4Rec (Zhang et al. 2024a) は、ユーザの好みや社会的特性を正確に反映するシミュレーターの開発に焦点を当てています。  
It leverages LLMs to create agents, each initialized with a unique user profile that includes tastes and social traits, ensuring agents’ behaviors mirror those of real human users.  
それはLLMを活用してエージェントを作成し、それぞれが好みや社会的特性を含むユニークなユーザプロファイルで初期化され、エージェントの行動が実際の人間ユーザの行動を反映することを保証します。



### Conclusion 結論

This paper presents a novel user simulator for RL-based recommender systems. 
本論文では、RLベースの推薦システムのための新しいユーザシミュレータを提案します。

To address the prevalent issues of opacity and simulation evaluation in current systems in existing user simulators, we introduce an LLM-powered user simulator designed to explicitly model user preferences and engagement. 
既存のユーザシミュレータにおける現在のシステムの不透明性とシミュレーション評価の一般的な問題に対処するために、ユーザの好みとエンゲージメントを明示的にモデル化するように設計されたLLM駆動のユーザシミュレータを導入します。

Our method identifies explicit logic of user preferences, utilizing LLMs to analyze item characteristics and distill user sentiments. 
私たちの手法は、アイテムの特性を分析し、ユーザの感情を抽出するためにLLMを利用して、ユーザの好みの明示的な論理を特定します。

We propose a novel ensemble model that integrates both logical and statistical insights, enhancing the reliability and fidelity of user interaction simulations. 
論理的および統計的な洞察を統合した新しいアンサンブルモデルを提案し、ユーザインタラクションシミュレーションの信頼性と忠実性を向上させます。

We conduct comprehensive experiments across five datasets, demonstrating the simulator’s effectiveness and stability in various recommendation scenarios. 
私たちは5つのデータセットにわたる包括的な実験を行い、さまざまな推薦シナリオにおけるシミュレータの効果と安定性を示します。

Currently, this simulator only infers binary interactions of ‘like’ or ‘dislike’. 
現在、このシミュレータは「好き」または「嫌い」の二項インタラクションのみを推測します。

Future work will focus on integrating additional interaction signals, such as duration, rating, and retention, to enrich the application of the simulator. 
今後の研究では、シミュレータの適用を豊かにするために、持続時間、評価、保持などの追加のインタラクション信号を統合することに焦点を当てます。



### Acknowledgment 謝辞

This research was partially supported by Research Impact Fund (No.R1015-23), APRC - CityU New Research Initiatives (No.9610565, Start-up Grant for New Faculty of CityU), CityU - HKIDS Early Career Research Grant (No.9360163), Hong Kong ITC Innovation and Technology Fund Midstream Research Programme for Universities Project (No.ITS/034/22MS), Hong Kong Environmental and Conservation Fund (No. 88/2022), and SIRG - CityU Strategic Interdisciplinary Research Grant (No.7020046), the Fundamental Research Funds for the Central Universities, JLU, and Kuaishou.
この研究は、Research Impact Fund（No.R1015-23）、APRC - CityU New Research Initiatives（No.9610565、CityUの新任教員のためのスタートアップ助成金）、CityU - HKIDS Early Career Research Grant（No.9360163）、香港ITCイノベーションおよび技術基金大学向け中流研究プログラムプロジェクト（No.ITS/034/22MS）、香港環境保護基金（No. 88/2022）、およびSIRG - CityU戦略的学際研究助成金（No.7020046）、中央大学の基礎研究資金、JLU、およびKuaishouによって部分的に支援されました。



### References 参考文献

Bommasani, R.; Hudson, D. A.; Adeli, E.; Altman, R.; Arora, S.; von Arx, S.; Bernstein, M. S.; Bohg, J.; Bosselut, A.; Brunskill, E.; et al. 2021. On the opportunities and risks of foundation models. arXiv preprint arXiv:2108.07258.  
Bommasani, R.; Hudson, D. A.; Adeli, E.; Altman, R.; Arora, S.; von Arx, S.; Bernstein, M. S.; Bohg, J.; Bosselut, A.; Brunskill, E.; 他. 2021. 基盤モデルの機会とリスクについて。arXivプレプリント arXiv:2108.07258。

Bubeck, S.; Chandrasekaran, V.; Eldan, R.; Gehrke, J.; Horvitz, E.; Kamar, E.; Lee, P.; Lee, Y. T.; Li, Y.; Lundberg, S.; et al. 2023. Sparks of artificial general intelligence: Early experiments with gpt-4. arXiv preprint arXiv:2303.12712.  
Bubeck, S.; Chandrasekaran, V.; Eldan, R.; Gehrke, J.; Horvitz, E.; Kamar, E.; Lee, P.; Lee, Y. T.; Li, Y.; Lundberg, S.; 他. 2023. 人工一般知能の火花：gpt-4を用いた初期実験。arXivプレプリント arXiv:2303.12712。

Chen, X.; Li, S.; Li, H.; Jiang, S.; Qi, Y.; and Song, L. 2019. Generative adversarial user model for reinforcement learning based recommendation system. In International Conference on Machine Learning, 1052–1061. PMLR.  
Chen, X.; Li, S.; Li, H.; Jiang, S.; Qi, Y.; および Song, L. 2019. 強化学習に基づく推薦システムのための生成的敵対的ユーザーモデル。国際機械学習会議において、1052–1061。PMLR。

Chu, Z.; Chen, J.; Chen, Q.; Yu, W.; He, T.; Wang, H.; Peng, W.; Liu, M.; Qin, B.; and Liu, T. 2023. A survey of chain of thought reasoning: Advances, frontiers and future. arXiv preprint arXiv:2309.15402.  
Chu, Z.; Chen, J.; Chen, Q.; Yu, W.; He, T.; Wang, H.; Peng, W.; Liu, M.; Qin, B.; および Liu, T. 2023. 思考の連鎖推論に関する調査：進展、最前線、未来。arXivプレプリント arXiv:2309.15402。

Corecco, N.; Piatti, G.; Lanzendörfer, L. A.; Fan, F. X.; and Wattenhofer, R. 2024. SUBER: An RL Environment with Simulated Human Behavior for Recommender Systems.  
Corecco, N.; Piatti, G.; Lanzendörfer, L. A.; Fan, F. X.; および Wattenhofer, R. 2024. SUBER：推薦システムのための人間行動をシミュレートしたRL環境。

Devlin, J. 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805.  
Devlin, J. 2018. Bert：言語理解のための深層双方向トランスフォーマーの事前学習。arXivプレプリント arXiv:1810.04805。

Fu, Z.; Li, X.; Wu, C.; Wang, Y.; Dong, K.; Zhao, X.; Zhao, M.; Guo, H.; and Tang, R. 2023. A unified framework for multi-domain ctr prediction via large language models.  
Fu, Z.; Li, X.; Wu, C.; Wang, Y.; Dong, K.; Zhao, X.; Zhao, M.; Guo, H.; および Tang, R. 2023. 大規模言語モデルを用いたマルチドメインCTR予測のための統一フレームワーク。

_ACM Transactions on Information Systems._  
_ACM情報システムトランザクション。_

Han, X.; Zhu, C.; Hu, X.; Qin, C.; Zhao, X.; and Zhu, H. 2024. Adapting Job Recommendations to User Preference Drift with Behavioral-Semantic Fusion Learning. In Baeza-Yates, R.; and Bonchi, F., eds., Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD 2024, Barcelona, Spain, August 25-29, 2024, 1004–1015. ACM.  
Han, X.; Zhu, C.; Hu, X.; Qin, C.; Zhao, X.; および Zhu, H. 2024. 行動-意味融合学習を用いたユーザープリファレンスの変化に適応したジョブ推薦。Baeza-Yates, R.; および Bonchi, F. 編、30回ACM SIGKDD知識発見とデータマイニング会議の議事録、KDD 2024、バルセロナ、スペイン、2024年8月25-29日、1004–1015。ACM。

Huang, F.; Yang, Z.; Jiang, J.; Bei, Y.; Zhang, Y.; and Chen, H. 2024. Large Language Model Interaction Simulator for Cold-Start Item Recommendation. arXiv preprint arXiv:2402.09176.  
Huang, F.; Yang, Z.; Jiang, J.; Bei, Y.; Zhang, Y.; および Chen, H. 2024. コールドスタートアイテム推薦のための大規模言語モデルインタラクションシミュレーター。arXivプレプリント arXiv:2402.09176。

Ie, E.; Hsu, C.-w.; Mladenov, M.; Jain, V.; Narvekar, S.; Wang, J.; Wu, R.; and Boutilier, C. 2019. Recsim: A configurable simulation platform for recommender systems. arXiv preprint arXiv:1909.04847.  
Ie, E.; Hsu, C.-w.; Mladenov, M.; Jain, V.; Narvekar, S.; Wang, J.; Wu, R.; および Boutilier, C. 2019. Recsim：推薦システムのための構成可能なシミュレーションプラットフォーム。arXivプレプリント arXiv:1909.04847。

Ji, Z.; Yu, T.; Xu, Y.; Lee, N.; Ishii, E.; and Fung, P. 2023. Towards mitigating LLM hallucination via self reflection. In Findings of the Association for Computational Linguistics: EMNLP 2023, 1827–1843.  
Ji, Z.; Yu, T.; Xu, Y.; Lee, N.; Ishii, E.; および Fung, P. 2023. 自己反省を通じてLLMの幻覚を軽減することを目指して。計算言語学会の成果：EMNLP 2023において、1827–1843。

Jia, P.; Liu, Y.; Zhao, X.; Li, X.; Hao, C.; Wang, S.; and Yin, D. 2023. MILL: Mutual Verification with Large Language Models for Zero-Shot Query Expansion. arXiv preprint arXiv:2310.19056.  
Jia, P.; Liu, Y.; Zhao, X.; Li, X.; Hao, C.; Wang, S.; および Yin, D. 2023. MILL：ゼロショットクエリ拡張のための大規模言語モデルによる相互検証。arXivプレプリント arXiv:2310.19056。

Kang, W.-C.; and McAuley, J. 2018. Self-attentive sequential recommendation. In 2018 IEEE international conference on data mining (ICDM), 197–206. IEEE.  
Kang, W.-C.; および McAuley, J. 2018. 自己注意型逐次推薦。2018年IEEE国際データマイニング会議（ICDM）において、197–206。IEEE。

Li, M.; Zhang, Z.; Zhao, X.; Wang, W.; Zhao, M.; Wu, R.; and Guo, R. 2023. Automlp: Automated mlp for sequential recommendations. In Proceedings of the ACM Web Conference 2023, 1190–1198.  
Li, M.; Zhang, Z.; Zhao, X.; Wang, W.; Zhao, M.; Wu, R.; および Guo, R. 2023. Automlp：逐次推薦のための自動化されたMLP。ACM Web Conference 2023の議事録において、1190–1198。

Liu, L.; Cai, L.; Zhang, C.; Zhao, X.; Gao, J.; Wang, W.; Lv, Y.; Fan, W.; Wang, Y.; He, M.; et al. 2023a. Linrec: Linear attention mechanism for long-term sequential recommender systems. In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval, 289–299.  
Liu, L.; Cai, L.; Zhang, C.; Zhao, X.; Gao, J.; Wang, W.; Lv, Y.; Fan, W.; Wang, Y.; He, M.; 他. 2023a. Linrec：長期逐次推薦システムのための線形注意メカニズム。第46回国際ACM SIGIR情報検索に関する研究開発会議の議事録において、289–299。

Liu, Q.; Wu, X.; Zhao, X.; Zhu, Y.; Zhang, Z.; Tian, F.; and Zheng, Y. 2024a. Large language model distilling medication recommendation model. arXiv preprint arXiv:2402.02803.  
Liu, Q.; Wu, X.; Zhao, X.; Zhu, Y.; Zhang, Z.; Tian, F.; および Zheng, Y. 2024a. 大規模言語モデルによる医薬品推薦モデルの蒸留。arXivプレプリント arXiv:2402.02803。

Liu, Q.; Zhao, X.; Wang, Y.; Wang, Y.; Zhang, Z.; Sun, Y.; Li, X.; Wang, M.; Jia, P.; Chen, C.; Huang, W.; and Tian, F. 2024b. Large Language Model Enhanced Recommender Systems: Taxonomy, Trend, Application and Future. arXiv:2412.13432.  
Liu, Q.; Zhao, X.; Wang, Y.; Wang, Y.; Zhang, Z.; Sun, Y.; Li, X.; Wang, M.; Jia, P.; Chen, C.; Huang, W.; および Tian, F. 2024b. 大規模言語モデル強化推薦システム：分類、トレンド、応用と未来。arXiv:2412.13432。

Liu, Z.; Tian, J.; Cai, Q.; Zhao, X.; Gao, J.; Liu, S.; Chen, D.; He, T.; Zheng, D.; Jiang, P.; et al. 2023b. Multi-task recommendations with reinforcement learning. In Proceedings of the ACM Web Conference 2023, 1273–1282.  
Liu, Z.; Tian, J.; Cai, Q.; Zhao, X.; Gao, J.; Liu, S.; Chen, D.; He, T.; Zheng, D.; Jiang, P.; 他. 2023b. 強化学習によるマルチタスク推薦。ACM Web Conference 2023の議事録において、1273–1282。

Mnih, V.; Badia, A. P.; Mirza, M.; Graves, A.; Lillicrap, T.; Harley, T.; Silver, D.; and Kavukcuoglu, K. 2016. Asynchronous methods for deep reinforcement learning. In International conference on machine learning, 1928–1937. PMLR.  
Mnih, V.; Badia, A. P.; Mirza, M.; Graves, A.; Lillicrap, T.; Harley, T.; Silver, D.; および Kavukcuoglu, K. 2016. 深層強化学習のための非同期手法。国際機械学習会議において、1928–1937。PMLR。

Mnih, V.; Kavukcuoglu, K.; Silver, D.; Graves, A.; Antonoglou, I.; Wierstra, D.; and Riedmiller, M. 2013. Playing atari with deep reinforcement learning. arXiv preprint arXiv:1312.5602.  
Mnih, V.; Kavukcuoglu, K.; Silver, D.; Graves, A.; Antonoglou, I.; Wierstra, D.; および Riedmiller, M. 2013. 深層強化学習を用いたアタリのプレイ。arXivプレプリント arXiv:1312.5602。

Puterman, M. L. 1990. Markov decision processes. Handbooks in operations research and management science, 2: 331–434.  
Puterman, M. L. 1990. マルコフ決定過程。オペレーションズリサーチとマネジメントサイエンスのハンドブック、2: 331–434。

Rohde, D.; Bonner, S.; Dunlop, T.; Vasile, F.; and Karatzoglou, A. 2018. Recogym: A reinforcement learning environment for the problem of product recommendation in online advertising. arXiv preprint arXiv:1808.00720.  
Rohde, D.; Bonner, S.; Dunlop, T.; Vasile, F.; および Karatzoglou, A. 2018. Recogym：オンライン広告における製品推薦の問題のための強化学習環境。arXivプレプリント arXiv:1808.00720。

Schulman, J.; Levine, S.; Abbeel, P.; Jordan, M.; and Moritz, P. 2015. Trust region policy optimization. In International conference on machine learning, 1889–1897. PMLR.  
Schulman, J.; Levine, S.; Abbeel, P.; Jordan, M.; および Moritz, P. 2015. 信頼領域ポリシー最適化。国際機械学習会議において、1889–1897。PMLR。

Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; and Klimov, O. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347.  
Schulman, J.; Wolski, F.; Dhariwal, P.; Radford, A.; および Klimov, O. 2017. 近接ポリシー最適化アルゴリズム。arXivプレプリント arXiv:1707.06347。

Shi, J.-C.; Yu, Y.; Da, Q.; Chen, S.-Y.; and Zeng, A.-X. 2019. Virtual-taobao: Virtualizing real-world online retail environment for reinforcement learning. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, 4902–4909.  
Shi, J.-C.; Yu, Y.; Da, Q.; Chen, S.-Y.; および Zeng, A.-X. 2019. Virtual-taobao：強化学習のための現実世界のオンライン小売環境の仮想化。AAAI人工知能会議の議事録において、ボリューム33、4902–4909。

Wang, H.; Liu, X.; Fan, W.; Zhao, X.; Kini, V.; Yadav, D.; Wang, F.; Wen, Z.; Tang, J.; and Liu, H. 2024a. Rethinking large language model architectures for sequential recommendations. arXiv preprint arXiv:2402.09543.  
Wang, H.; Liu, X.; Fan, W.; Zhao, X.; Kini, V.; Yadav, D.; Wang, F.; Wen, Z.; Tang, J.; および Liu, H. 2024a. 逐次推薦のための大規模言語モデルアーキテクチャの再考。arXivプレプリント arXiv:2402.09543。

Wang, K.; Zou, Z.; Zhao, M.; Deng, Q.; Shang, Y.; Liang, Y.; Wu, R.; Shen, X.; Lyu, T.; and Fan, C. 2023a. RL4RS: A real-world dataset for reinforcement learning based recommender system. In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2935–2944.  
Wang, K.; Zou, Z.; Zhao, M.; Deng, Q.; Shang, Y.; Liang, Y.; Wu, R.; Shen, X.; Lyu, T.; および Fan, C. 2023a. RL4RS：強化学習に基づく推薦システムのための実世界データセット。第46回国際ACM SIGIR情報検索に関する研究開発会議の議事録において、2935–2944。

Wang, M.; Zhao, Y.; Liu, J.; Chen, J.; Zhuang, C.; Gu, J.; Guo, R.; and Zhao, X. 2024b. Large Multimodal Model Compression via Iterative Efficient Pruning and Distillation. In Companion Proceedings of the ACM on Web Conference 2024, 235–244.  
Wang, M.; Zhao, Y.; Liu, J.; Chen, J.; Zhuang, C.; Gu, J.; Guo, R.; および Zhao, X. 2024b. 反復的効率的プルーニングと蒸留による大規模マルチモーダルモデル圧縮。ACM Web Conference 2024の補助議事録において、235–244。

Wang, X.; Tang, X.; Zhao, W. X.; Wang, J.; and Wen, J.R. 2023b. Rethinking the evaluation for conversational recommendation in the era of large language models. arXiv preprint arXiv:2305.13112.  
Wang, X.; Tang, X.; Zhao, W. X.; Wang, J.; および Wen, J.R. 2023b. 大規模言語モデルの時代における会話型推薦の評価の再考。arXivプレプリント arXiv:2305.13112。

Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35: 24824–24837.  
Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; 他. 2022. 思考の連鎖を促すプロンプトが大規模言語モデルにおける推論を引き出す。神経情報処理システムの進展、35: 24824–24837。

Yao, J.-Y.; Ning, K.-P.; Liu, Z.-H.; Ning, M.-N.; and Yuan, L. 2023. Llm lies: Hallucinations are not bugs, but features as adversarial examples. arXiv preprint arXiv:2310.01469.  
Yao, J.-Y.; Ning, K.-P.; Liu, Z.-H.; Ning, M.-N.; および Yuan, L. 2023. LLMの嘘：幻覚はバグではなく、敵対的例としての特徴である。arXivプレプリント arXiv:2310.01469。

Zhang, A.; Chen, Y.; Sheng, L.; Wang, X.; and Chua, T.S. 2024a. On generative agents in recommendation. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 1807–1817.  
Zhang, A.; Chen, Y.; Sheng, L.; Wang, X.; および Chua, T.S. 2024a. 推薦における生成エージェントについて。第47回国際ACM SIGIR情報検索に関する研究開発会議の議事録において、1807–1817。

Zhang, E.; Wang, X.; Gong, P.; Lin, Y.; and Mao, J. 2024b. Usimagent: Large language models for simulating search users. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2687–2692.  
Zhang, E.; Wang, X.; Gong, P.; Lin, Y.; および Mao, J. 2024b. Usimagent：検索ユーザーをシミュレートするための大規模言語モデル。第47回国際ACM SIGIR情報検索に関する研究開発会議の議事録において、2687–2692。

Zhang, W.; Zhao, X.; Zhao, L.; Yin, D.; Yang, G. H.; and Beutel, A. 2020. Deep reinforcement learning for information retrieval: Fundamentals and advances. In Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval, 2468–2471.  
Zhang, W.; Zhao, X.; Zhao, L.; Yin, D.; Yang, G. H.; および Beutel, A. 2020. 情報検索のための深層強化学習：基礎と進展。第43回国際ACM SIGIR情報検索に関する研究開発会議の議事録において、2468–2471。

Zhang, Y.; Shen, G.; Han, X.; Wang, W.; and Kong, X. 2023. Spatio-Temporal Digraph Convolutional Network-Based Taxi Pickup Location Recommendation. IEEE Trans. Ind. Informatics, 19(1): 394–403.  
Zhang, Y.; Shen, G.; Han, X.; Wang, W.; および Kong, X. 2023. 空間-時間ダイグラフ畳み込みネットワークに基づくタクシー乗車場所推薦。IEEEトランザクションズ インダストリアル インフォマティクス、19(1): 394–403。

Zhang, Z.; Liu, S.; Yu, J.; Cai, Q.; Zhao, X.; Zhang, C.; Liu, Z.; Liu, Q.; Zhao, H.; Hu, L.; et al. 2024c. M3oe: Multi-domain multi-task mixture-of experts recommendation framework. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 893–902.  
Zhang, Z.; Liu, S.; Yu, J.; Cai, Q.; Zhao, X.; Zhang, C.; Liu, Z.; Liu, Q.; Zhao, H.; Hu, L.; 他. 2024c. M3oe：マルチドメインマルチタスクエキスパート混合推薦フレームワーク。第47回国際ACM SIGIR情報検索に関する研究開発会議の議事録において、893–902。

Zhao, K.; Liu, S.; Cai, Q.; Zhao, X.; Liu, Z.; Zheng, D.; Jiang, P.; and Gai, K. 2023a. KuaiSim: A comprehensive simulator for recommender systems. Advances in Neural Information Processing Systems, 36: 44880–44897.  
Zhao, K.; Liu, S.; Cai, Q.; Zhao, X.; Liu, Z.; Zheng, D.; Jiang, P.; および Gai, K. 2023a. KuaiSim：推薦システムのための包括的シミュレーター。神経情報処理システムの進展、36: 44880–44897。

Zhao, K.; Zou, L.; Zhao, X.; Wang, M.; and Yin, D. 2023b. User retention-oriented recommendation with decision transformer. In Proceedings of the ACM Web Conference 2023, 1141–1149.  
Zhao, K.; Zou, L.; Zhao, X.; Wang, M.; および Yin, D. 2023b. ユーザー保持を重視した推薦を意思決定トランスフォーマーで実現。ACM Web Conference 2023の議事録において、1141–1149。

Zhao, X.; Gu, C.; Zhang, H.; Yang, X.; Liu, X.; Tang, J.; and Liu, H. 2021a. Dear: Deep reinforcement learning for online advertising impression in recommender systems. In Proceedings of the AAAI conference on artificial intelligence, volume 35, 750–758.  
Zhao, X.; Gu, C.; Zhang, H.; Yang, X.; Liu, X.; Tang, J.; および Liu, H. 2021a. Dear：推薦システムにおけるオンライン広告インプレッションのための深層強化学習。AAAI人工知能会議の議事録において、ボリューム35、750–758。

Zhao, X.; Xia, L.; Tang, J.; and Yin, D. 2019. Deep reinforcement learning for search, recommendation, and online advertising: a survey. ACM sigweb newsletter, 2019(Spring): 1–15.  
Zhao, X.; Xia, L.; Tang, J.; および Yin, D. 2019. 検索、推薦、オンライン広告のための深層強化学習：調査。ACM sigwebニュースレター、2019年春号：1–15。

Zhao, X.; Xia, L.; Zhang, L.; Ding, Z.; Yin, D.; and Tang, J. 2018a. Deep reinforcement learning for page-wise recommendations. In Proceedings of the 12th ACM conference on recommender systems, 95–103.  
Zhao, X.; Xia, L.; Zhang, L.; Ding, Z.; Yin, D.; および Tang, J. 2018a. ページ単位の推薦のための深層強化学習。第12回ACM推薦システム会議の議事録において、95–103。

Zhao, X.; Xia, L.; Zou, L.; Liu, H.; Yin, D.; and Tang, J. 2021b. Usersim: User simulation via supervised generative adversarial network. In Proceedings of the Web Conference 2021, 3582–3589.  
Zhao, X.; Xia, L.; Zou, L.; Liu, H.; Yin, D.; および Tang, J. 2021b. Usersim：教師あり生成的敵対的ネットワークによるユーザーシミュレーション。Web Conference 2021の議事録において、3582–3589。

Zhao, X.; Zhang, L.; Ding, Z.; Xia, L.; Tang, J.; and Yin, D. 2018b. Recommendations with negative feedback via pairwise deep reinforcement learning. In Proceedings of the 24th ACM SIGKDD international conference on knowledge discovery & data mining, 1040–1048.  
Zhao, X.; Zhang, L.; Ding, Z.; Xia, L.; Tang, J.; および Yin, D. 2018b. ペアワイズ深層強化学習によるネガティブフィードバックを伴う推薦。第24回ACM SIGKDD国際会議における知識発見とデータマイニングの議事録において、1040–1048。
