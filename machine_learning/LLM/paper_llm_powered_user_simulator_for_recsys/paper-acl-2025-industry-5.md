refs: https://aclanthology.org/2025.acl-industry.5.pdf


# SimUSER: Simulating User Behavior with Large Language Models for Recommender System Evaluation  
# SimUSER: 大規模言語モデルを用いたユーザ行動のシミュレーションによる推薦システム評価  

Nicolas Bougie[1], Narimasa Watanabe[1]  
ニコラス・ブージー[1], 渡辺成正[1]

{nicolas.bougie,narimasa.watanabe}@woven.toyota  
{nicolas.bougie,narimasa.watanabe}@woven.toyota  

Woven by Toyota

## Abstract 要約

Recommender systems play a central role in numerous real-life applications, yet evaluating their performance remains a significant challenge due to the gap between offline metrics and online behaviors. 
レコメンダーシステムは多くの実生活のアプリケーションで中心的な役割を果たしていますが、**オフラインの指標とオンラインの行動とのギャップのために、そのパフォーマンスを評価することは依然として大きな課題**です。
Given the scarcity and limits (e.g., privacy issues) of real user data, we introduce SimUSER, an agent framework that serves as believable and cost-effective human proxies. 
実際のユーザデータの不足や制限（例：プライバシーの問題）を考慮し、私たちは信頼性が高くコスト効果のある人間の代理として機能するエージェントフレームワークSimUSERを導入します。
SimUSER first identifies selfconsistent personas from historical data, enriching user profiles with unique backgrounds and personalities. 
SimUSERはまず、**歴史的データから自己一貫性のあるペルソナを特定**し、ユニークな背景や個性を持つユーザプロファイルを豊かにします。
Then, central to this evaluation are users equipped with persona, memory, perception, and brain modules, engaging in interactions with the recommender system. 
次に、この評価の中心となるのは、ペルソナ、記憶、知覚、脳モジュールを備えたユーザであり、レコメンダーシステムとのインタラクションに従事します。
SimUSER exhibits closer alignment with genuine humans than prior work, both at micro and macro levels. 
SimUSERは、以前の研究よりもマイクロおよびマクロの両レベルで実際の人間とより密接に一致しています。
Additionally, we conduct insightful experiments to explore the effects of thumbnails on click rates, the exposure effect, and the impact of reviews on user engagement. 
さらに、サムネイルがクリック率に与える影響、露出効果、レビューがユーザエンゲージメントに与える影響を探るための洞察に満ちた実験を行います。
Finally, we refine recommender system parameters based on offline A/B test results, resulting in improved user engagement in the real world. 
**最後に、オフラインA/Bテストの結果に基づいてレコメンダーシステムのパラメータを洗練させ、実世界でのユーザエンゲージメントの向上を実現**します。

<!-- ここまで読んだ! -->

## 1 Introduction はじめに

Recommender systems (RS) have become an indispensable component of our day-to-day lives from e-commerce to social media by offering personalized user experience and improving satisfaction (Li et al., 2024). 
レコメンダーシステム（RS）は、eコマースからソーシャルメディアに至るまで、パーソナライズされたユーザ体験を提供し、満足度を向上させることで、私たちの日常生活に欠かせない要素となっています（Li et al., 2024）。 
Despite their widespread adoption, a key challenge hindering the advancement of the field is evaluation (Yoon et al., 2024). 
**しかし、広く採用されているにもかかわらず、この分野の進展を妨げる重要な課題は評価**です（Yoon et al., 2024）。 
The difficulty arises from the discrepancy between offline metrics (non-interactive), which are typically used during development, and real-life user behaviors, which these systems encounter post-deployment (Zhang et al., 2019). 
**この難しさは、開発中に通常使用されるオフラインメトリック（非対話型）と、これらのシステムが展開後に直面する実際のユーザ行動との間の不一致から生じます**（Zhang et al., 2019）。 
This results in models that perform well in controlled environments but fail to meet expectations in practical use cases.
その結果、制御された環境では良好に機能するモデルが、実際の使用ケースでは期待に応えられないという事態が生じます。 
Such a limitation is further exacerbated by the inherent shortcomings of offline evaluation, notably the inability to measure business values such as user engagement and satisfaction (Jannach and Jugovac, 2019).
このような制限は、オフライン評価の固有の欠点、特にユーザエンゲージメントや満足度といったビジネス価値を測定できないことによってさらに悪化します（Jannach and Jugovac, 2019）。
On the other hand, online A/B testing is costly to scale up, labor-intensive, and encompasses ethical considerations, underscoring the imperative need for reliable and affordable (interactive) evaluation methods. 
一方、**オンラインA/Bテストはスケールアップにコストがかかり、労力を要し、倫理的な考慮も含まれる**ため、信頼性が高く手頃な（**対話型**）評価方法の必要性が強調されています。 

<!-- ここまで読んだ! -->

Recent breakthroughs in Large Language Models (LLMs) have shown promise in human behavior modeling by enabling the creation of autonomous agents. 
最近の大規模言語モデル（LLMs）のブレークスルーは、自律エージェントの作成を可能にすることで、人間の行動モデルにおいて期待が持たれています。
In the realm of recommendation systems, RecMind (Wang et al., 2023b) explores the concept of autonomous recommender agents equipped with self-inspiring planning and external tool utilization. 
レコメンデーションシステムの分野では、RecMind（Wang et al., 2023b）が自己啓発的な計画と外部ツールの利用を備えた自律レコメンダーエージェントの概念を探求しています。
Recently, InteRecAgent (Huang et al., 2023) has extended this idea by proposing memory components, dynamic demonstration-augmented task planning, and reflection. 
最近、InteRecAgent（Huang et al., 2023）は、メモリコンポーネント、動的デモンストレーション強化タスク計画、および反省を提案することでこのアイデアを拡張しました。 
Recently, RecAgent (Wang et al., 2023a) has attempted to introduce more diverse user behaviors, taking into account external social relationships. 
最近、RecAgent（Wang et al., 2023a）は、外部の社会的関係を考慮に入れたより多様なユーザ行動を導入しようと試みました。 
Another work, Agent4Rec (Hou et al., 2024), delves into generating faithful user-RS interactions via agent-based simulations, where agents are equipped with a memory module. 
別の研究であるAgent4Rec（Hou et al., 2024）は、エージェントにメモリモジュールを装備させたエージェントベースのシミュレーションを通じて、信頼できるユーザとRSの相互作用を生成することに取り組んでいます。 
However, a common characteristic of existing studies is their insulated nature — they primarily rely on knowledge embedded within the model’s weights, neglecting the potential benefits of integrating external knowledge and user-item relationships. 
しかし、既存の研究の共通の特徴は、その孤立した性質です — 彼らは主にモデルの重み内に埋め込まれた知識に依存しており、外部知識やユーザ-アイテム関係を統合することの潜在的な利点を無視しています。
Furthermore, prior approaches often disregard user personas and fail to incorporate visual signals, despite their role in shaping user experience and emotion. 
さらに、**以前のアプローチはユーザペルソナを無視**し、ユーザ体験や感情を形成する役割にもかかわらず、視覚的信号を取り入れることに失敗しています。 

<!-- ここまで読んだ! -->

To enable synthetic users, we describe an agent architecture built upon LLMs. 
合成ユーザを可能にするために、私たちはLLMsに基づいたエージェントアーキテクチャを説明します。 
Our methodology consists of two phases: (1) self-consistent persona matching and (2) recommender system evaluation. 
私たちの方法論は、**2つのフェーズ**から成り立っています：（1）自己一貫したペルソナマッチングと（2）レコメンダーシステムの評価。
In Phase 1, we leverage the semantic awareness of LLMs to extract and identify consistent personas from historical data, encompassing unique backgrounds, personalities, and characteristics. 
フェーズ1では、LLMsの意味的認識を活用して、歴史的データから一貫したペルソナを抽出し、特有の背景、性格、特徴を含めて特定します。 
In Phase 2, we impersonate these personas to simulate believable human interactions. 
フェーズ2では、これらのペルソナを模倣して、信じられる人間の相互作用をシミュレートします。 
This involves a retrieval-augmented framework where the agent interacts with the recommender system based on its persona, memory, perception, and brain modules. 
これは、エージェントがそのペルソナ、メモリ、知覚、脳モジュールに基づいてレコメンダーシステムと相互作用する、リトリーバル強化フレームワークを含みます。 
The memory module comprises an episodic memory and a knowledge-graph memory. 
メモリモジュールは、エピソードメモリとナレッジグラフメモリで構成されています。 
Unlike existing studies that solely rely on text, our perception module incorporates visual cues into the agent’s reasoning process. 
既存の研究がテキストのみに依存しているのとは異なり、私たちの知覚モジュールはエージェントの推論プロセスに視覚的手がかりを組み込んでいます。 
Finally, the brain module is responsible for translating retrieved evidences and graph paths into action plans such as [click], or [exit]. 
最後に、脳モジュールは、取得した証拠やグラフパスを[click]や[exit]などのアクションプランに変換する役割を担っています。 
Following action selection, the user engages in self-reflection to synthesize memories into higher-level inferences and draw conclusions. 
アクション選択の後、ユーザは自己反省に従事し、記憶を統合して高次の推論を行い、結論を導き出します。

<!-- ここまで読んだ! -->

## 2 Related Work 関連研究

Conversational RS initially tackled the recommendation problem using bandit models, emphasizing the quick update of traditional systems through item selection and binary feedback from synthetic users (Christakopoulou et al., 2016). 
**会話型推薦システム（Conversational RS）は、最初にバンディットモデルを使用して推薦問題に取り組み**、アイテム選択と合成ユーザからの二項フィードバックを通じて従来のシステムの迅速な更新を強調しました（Christakopoulou et al., 2016）。(合成ユーザって事はオフライン学習的なこと??:thinking:)
Taking this further, (Zhao et al., 2023) created a simulation platform where users not only chat about recommendations. 
さらに進めて、(Zhao et al., 2023)は、**ユーザが推薦についてチャットするだけでなく、さまざまなインタラクションを行うシミュレーションプラットフォーム**を作成しました。
Recent techniques have added more natural language flexibility, but user responses are usually limited to binary or multiple-choice formats (Lei et al., 2020). 
**最近の技術は、より自然な言語の柔軟性を追加しましたが、ユーザの応答は通常、二項または選択肢形式に制限されています**（Lei et al., 2020）。(これってそんなに困る事なのかな...?? 十分に思っちゃうけど...!:thinking:)
In spite of this, these simulations often rely on fixed rules and scripted dialogues, lacking the variability seen in human interactions. 
それにもかかわらず、これらのシミュレーションはしばしば固定されたルールとスクリプト化された対話に依存しており、人間のインタラクションに見られる変動性が欠けています。
To address the above-mentioned limitations, generative simulators using LLMs have been developed, offering more realistic and nuanced conversational abilities (Zhang et al., 2024b; Zhao et al., 2023). 
**上記の制限に対処するために、LLM（大規模言語モデル）を使用した生成シミュレーターが開発**され、より現実的で微妙な会話能力を提供しています（Zhang et al., 2024b; Zhao et al., 2023）。
A few studies have also explored the application of LLMs as recommender systems (Hou et al., 2024; Li et al., 2023; Kang et al., 2023). 
いくつかの研究では、LLMを推薦システムとして応用することも探求されています（Hou et al., 2024; Li et al., 2023; Kang et al., 2023）。(=RecSysの評価じゃなくて、RecSysそのものとしてLLMを使うってパターンか...!:thinking:)
These investigations explore LLMs as recommendation engines, rather than as entities that perceive recommendations, thus providing a perspective complementary to our research (Wang et al., 2024; Zhang et al., 2024a). 
これらの調査は、LLMを推薦エンジンとして探求しており、推薦を認識する存在としてではなく、私たちの研究に補完的な視点を提供しています（Wang et al., 2024; Zhang et al., 2024a）。
RecMind (Wang et al., 2023b) proposes self-inspiring agents for recommendation. 
RecMind（Wang et al., 2023b）は、推薦のための自己啓発エージェントを提案しています。
However, their simulated users are limited to basic actions like rating items, lacking the ability to engage in more complex interactions. 
しかし、彼らのシミュレーションされたユーザはアイテムの評価などの基本的な行動に制限されており、より複雑なインタラクションに関与する能力が欠けています。
Notably, a recent approach (Yoon et al., 2024) examines the effectiveness of LLMs as generative users, specifically for conversational recommendation scenarios. 
**特に、最近のアプローチ（Yoon et al., 2024）は、会話型推薦シナリオに特化して、LLMを生成ユーザとしての効果を検証しています。** (会話型推薦シナリオっていうのは、強化学習的なbanditタスク的なシナリオ、って意味かな??:thinking:)
A closely related work to ours is Agent4Rec (Zhang et al., 2023) that delves into the generative capabilities of LLMs for modeling user interactions.  
私たちの研究に密接に関連するのは、ユーザインタラクションのモデル化のためのLLMの生成能力を掘り下げたAgent4Rec（Zhang et al., 2023）です。
SimUSER differs significantly from these studies as we utilize detailed personas that are systematically inferred from historical and incorporate a perception module to integrate visual reasoning. 
SimUSERは、歴史から体系的に推測された詳細なペルソナを利用し、視覚的推論を統合する知覚モジュールを組み込むことで、これらの研究とは大きく異なります。
Furthermore, SimUSER investigates the potential of graph-based retrieval to represent the rationales underlying user-item interactions. 
さらに、SimUSERは、ユーザとアイテムのインタラクションの背後にある理由を表現するためのグラフベースの検索の可能性を探求しています。
Finally, we introduce multi-round preference elicitation and causal action refinement that leverage retrieved evidences and paths to generate more realistic interactions. 
最後に、取得した証拠と経路を活用して、より現実的なインタラクションを生成するための多段階の嗜好引き出しと因果的行動の洗練を導入します。

<!-- ここまで読んだ! -->

## 3 Methodology 方法論

Simulated USERs provides a framework for systematically assessing recommender systems by engaging in interactions and providing feedback.
Simulated USERsは、相互作用に参加しフィードバックを提供することによって、推薦システムを体系的に評価するためのフレームワークを提供します。(**Simulated USERs = SimUSER**...!:thinking:)
Phase 1 matches historical data with a set of personas to enable nuanced and realistic interactions. 
フェーズ1では、歴史的データを一連のペルソナと照合し、微妙で現実的な相互作用を可能にします。
Phase 2 utilizes the identified personas, historical data, and novel reasoning mechanisms to generate synthetic users with human-like behavior. 
フェーズ2では、特定されたペルソナ、歴史的データ、および新しい推論メカニズムを利用して、人間のような行動を持つ合成ユーザを生成します。

### Problem Formulation. 問題の定式化。

Given a user $u \in U$ and an item $i \in I$, the aggregated rating of the item is denoted by the aggregated rating of the item is denoted by $R_{i} = \frac{1}{\sum_{u \in U} y_{ui}} \sum_{u \in U} y_{ui} r_{ui}$,
ユーザ $u \in U$ とアイテム $i \in I$ が与えられた場合、アイテムの集約評価は $R_{i} = \frac{1}{\sum_{u \in U} y_{ui}} \sum_{u \in U} y_{ui} r_{ui}$ と示されます、
where $y_{ui} = 0$ indicates that the user has not rated the item $i$ and inversely $y_{ui} = 1$ indicates that the user has rated the item with $r_{ui} \in \{1, 2, 3, 4, 5\}$. 
ここで、$y_{ui} = 0$ はユーザがアイテム $i$ を評価していないことを示し、逆に $y_{ui} = 1$ はユーザが $r_{ui} \in \{1, 2, 3, 4, 5\}$ でアイテムを評価したことを示します。
We also introduce $g_i \in G$ as the genre/category of the item. 
また、アイテムのジャンル/カテゴリとして $g_i \in G$ を導入します。
In this study, we seek to discover $y_{ui}$ and $r_{ui}$ for an unseen recommended item $i$. 
本研究では、未知の推薦アイテム $i$ に対する $y_{ui}$ と $r_{ui}$ を発見することを目指します。

<!-- ここまで読んだ! -->

### **3.1 Persona Matching via Consistency Check** 一貫性チェックによるペルソナマッチング

This phase involves assessing the most plausible persona based on historical data. 
このフェーズでは、歴史的データに基づいて最も妥当なペルソナを評価します。
A persona $p$ encompasses a set of features that characterize the user: age, personality, and occupation.
**ペルソナ $p$ は、ユーザを特徴づける一連の特徴（年齢、性格、職業）を含みます。**
Personality traits are defined by the Big Five personality facets: Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism, each measured on a scale from 1 to 3. 
**性格特性はビッグファイブ性格特性（開放性、誠実性、外向性、協調性、神経症傾向）によって定義され、各特性は1から3のスケールで測定**されます。
(へぇ〜こういうのはマーケティング分野の概念なのかな...!:thinking:)
Given the difficulty of obtaining such granular features in real-world settings, our methodology seeks to systematically infer personas from the user’s interaction history. 
**実世界の設定でそのような詳細な特徴を取得することの難しさを考慮し、私たちの方法論はユーザの相互作用履歴からペルソナを体系的に推測することを目指します。**

#### **Persona Extraction. ペルソナ抽出。

For a user $u$ with interactions $\{(i_0, r_{ui_0}), \ldots, (i_n, r_{ui_n})\}$, we query the LLM to produce a short summary $s_u$ of the user’s preferences. 
ユーザ $u$ が相互作用 $\{(i_0, r_{ui_0}), \ldots, (i_n, r_{ui_n})\}$ を持つ場合、LLMにユーザの嗜好の短い要約 $s_u$ を生成するように問い合わせます。
To do so, we randomly select 50 items from the user’s viewing history. 
そのために、ユーザの視聴履歴からランダムに50アイテムを選択します。
Items rated 4 or above are categorized as liked, while those rated below 3 are deemed disliked. 
**評価が4以上のアイテムは「好ましい」と分類され、3未満の評価のアイテムは「好ましくない」と見なされます。** (本論文はexplicit feedbackのシナリオっぽいな...!:thinking:)
We then combine $s_u$ with historical data to prompt the LLM to generate a persona that matches the interaction history for this user.
次に、$s_u$ を歴史的データと組み合わせて、**LLMにこのユーザの相互作用履歴に一致するペルソナを生成するように促します。**
To enhance the diversity, the LLM is provided a list of possible ages, personalities, and occupations. 
多様性を高めるために、**LLMには可能な年齢、性格、職業のリストが提供**されます。
For each user, a set of $m$ ($m = 5$) candidate personas is generated, denoted as $\mathcal{P}$. 
各ユーザに対して、$m$ ($m = 5$) の候補ペルソナのセットが生成され、$\mathcal{P}$ として示されます。

<!-- ここまで読んだ! -->

#### Self-Consistent Persona Evaluation. **自己一貫性ペルソナ評価。

We then assess the consistency of the candidate personas to $\mathcal{P}$ to identify the most plausible one. 
次に、候補ペルソナの一貫性を $\mathcal{P}$ に評価し、**最も妥当なものを特定**します。
A self-consistency scoring mechanism measures the alignment of candidate personas with historical data. 
**自己一貫性スコアリングメカニズムは、候補ペルソナと歴史的データの整合性を測定**します。
We define a scoring function $s_{p,u}$ for each candidate persona ($p \in \mathcal{P}$), where $p$ is evaluated against two distinct sets of user-item interactions. 
各候補ペルソナ ($p \in \mathcal{P}$) に対してスコアリング関数 $s_{p,u}$ を定義し、$p$ は2つの異なるユーザ-アイテム相互作用のセットに対して評価されます。
For the targeted user $u$, we sample $j$ subsets of $\rho$ interactions from its history. 
ターゲットユーザ $u$ に対して、履歴から $\rho$ の相互作用の $j$ サブセットをサンプリングします。
These are compared with $\rho$ sampled interactions from other users $\bar{u}$, denoted as $I_{\bar{u}}$: 
これらは、他のユーザ $\bar{u}$ からサンプリングされた $\rho$ の相互作用 ($I_{\bar{u}}$ として示されます) と比較されます：

$$
s(p, u) = \sum_{i \sim I_u} \hat{r}_{i,p} - \sum_{\bar{i} \in I_{\bar{u}}} \hat{r}_{\bar{i},p} 
\tag{1}
$$

where $\hat{r}_{i,p}$ and $\hat{r}_{\bar{i},p}$ are obtained by querying the LLM to rate the two interaction subsets $i$ and $\bar{i}$. 
ここで、$\hat{r}_{i,p}$ と $\hat{r}_{\bar{i},p}$ は、LLMに2つの相互作用サブセット $i$ と $\bar{i}$ を評価するように問い合わせることによって得られます。
Ideally, the LLM agent should assign a higher $\hat{r}_{i,p}$ for interactions from the targeted user and a lower $\hat{r}_{\bar{i},p}$ for samples from other users. 
**理想的には、LLMエージェントはターゲットユーザからの相互作用に対してより高い $\hat{r}_{i,p}$ を割り当て、他のユーザからのサンプルに対してはより低い $\hat{r}_{\bar{i},p}$ を割り当てるべきです。**
The candidate persona $p$ with the highest score $s$ is assigned to the user. 
最高スコア $s$ を持つ候補ペルソナ $p$ がユーザに割り当てられます。

<!-- ここまで読んだ! -->

### **3.2 Engaging in Interactions with RS** レコメンダーシステムとの相互作用への参加

In Phase 2, given a user $u$ and discovered persona $p$, we present a cognitive architecture built upon LLMs comprising four modules: persona, perception, memory, and action. 
フェーズ2では、ユーザ $u$ と発見されたペルソナ $p$ が与えられた場合、私たちは**ペルソナ、知覚、記憶、行動の4つのモジュールからなるLLMに基づいた認知アーキテクチャ**を提示します。

#### **3.2.1 Persona Module** **3.2.1 ペルソナモジュール**

To lay a reliable foundation for the generative agent’s subsequent interactions and evaluations, benchmark datasets are used for initialization of the persona module. 
生成エージェントのその後の相互作用と評価のための信頼できる基盤を築くために、ベンチマークデータセットがペルソナモジュールの初期化に使用されます。
An agent’s profile includes the matched persona $p$ along with attributes extracted from its historical data: $p \cup \{ \text{pickiness, habits, unique tastes} \}$. 
エージェントのプロファイルには、マッチしたペルソナ $p$ と、その歴史的データから抽出された属性が含まれます：$p \cup \{ \text{pickiness, habits, unique tastes} \}$。
Since LLMs are biased towards positive sentiment, unless prompted to behave as picky users (Yoon et al., 2024), each agent is assigned a pickiness level sampled in $\{\text{not picky, moderately picky, extremely picky}\}$ based on the user’s average rating. 
LLMはポジティブな感情に偏っているため、選り好みするユーザとして振る舞うように促されない限り（Yoon et al., 2024）、各エージェントにはユーザの平均評価に基づいて $\{\text{not picky, moderately picky, extremely picky}\}$ からサンプリングされた選り好みレベルが割り当てられます。
Habits account for user tendencies in engagement, conformity, and variety (Zhang et al., 2023), while unique tastes are derived from the viewing history summary $s_u$ generated in Phase 1. 
習慣は、エンゲージメント、順応性、および多様性におけるユーザの傾向を考慮し（Zhang et al., 2023）、ユニークな嗜好はフェーズ1で生成された視聴履歴の要約 $s_u$ から導き出されます。

<!-- ここまで読んだ! -->

#### **3.2.2 Perception Module** **3.2.2 知覚モジュール**

A primary factor in decision-making is visual stimuli due to their significant influence on curiosity and emotion (Liu et al., 2024). 
**意思決定における主要な要因は、好奇心や感情に対する重要な影響を持つ視覚刺激**です（Liu et al., 2024）。
For instance, when scrolling through a movie recommendation platform, human decisions are heavily driven by the thumbnails of items, which can trigger emotional responses and provide quick visual summaries of the content (Koh and Cui, 2022). 
**例えば、映画推薦プラットフォームをスクロールする際、人間の決定はアイテムのサムネイルによって大きく影響され、感情的な反応を引き起こし、コンテンツの迅速な視覚的要約を提供**します（Koh and Cui, 2022）。
(確かに、こう言語化されると、サムネイルって報酬を左右する重要な要素だよなって納得するな...特徴量として考慮できるようにすべきか...!:thinking:)
To graft these visual elements in a cost-efficient manner, we augment action prompts (see Sec A.1) with image-derived captions. 
**これらの視覚要素をコスト効率よく組み込むために、アクションプロンプトを画像由来のキャプションで拡張**します（Sec A.1を参照）。
The caption $i_{\text{caption}}$ of an item $i$ is generated by querying GPT-4 to extract insights that capture emotional tones, visual details, and unique selling points from the item’s thumbnail. 
アイテム $i$ のキャプション $i_{\text{caption}}$ は、GPT-4に問い合わせて、アイテムのサムネイルから感情的なトーン、視覚的な詳細、およびユニークなセールスポイントを捉える洞察を抽出することによって生成されます。
(サムネイル画像を入力して、その特徴を文章で要約したテキストを作らせて、それを後続タスクで特徴量として使う、って感じかな...!:thinking:)

<!-- ここまで読んだ! -->

#### **3.2.3 Memory Module**  **3.2.3 記憶モジュール**

It is critical for an agent to maintain a memory of the knowledge and experience it has of the world and others. 
エージェントが世界や他者に関する知識と経験の記憶を維持することは重要です。
SimUSER uses an episodic memory for interaction history and knowledge-graph memory to capture user-item relationships. 
SimUSERは、相互作用履歴のためのエピソード記憶と、ユーザ-アイテム関係をキャプチャするための知識グラフ記憶を使用します。

##### Episodic Memory. エピソード記憶。

**Episodic Memory** stores the interactions with the RS. The memory is initially populated with the user’s viewing and rating history. 
エピソード記憶はRSとの相互作用を保存します。記憶は、ユーザの視聴および評価履歴で最初に構成されます。
Each time SimUSER executes a new action or rates an item, the corresponding interaction is added to the episodic memory. 
**SimUSERが新しいアクションを実行したりアイテムを評価するたびに、対応する相互作用がエピソード記憶に追加**されます。
Drawing from human psychological processes (Atkinson and Shiffrin, 1968), we use a self-ask retrieval strategy where the LLM generates follow-up questions regarding the query. 
人間の心理的プロセス（Atkinson and Shiffrin, 1968）を参考にして、LLMがクエリに関するフォローアップ質問を生成する自己質問リトリーバル戦略を使用します。
These questions, along with the initial query, then serve as separate queries for vector similarity search, allowing retrieval of more diverse evidences. 
これらの質問は、初期のクエリとともに、ベクトル類似性検索のための別々のクエリとして機能し、より多様な証拠の取得を可能にします。
For a query $q$, we retrieve top-$k_1$ documents using cosine similarity: $s(q, d) = \cos(E(q), E(d))$, where $E$ is an embedding function. 
クエリ $q$ に対して、コサイン類似度を使用してトップ $k_1$ ドキュメントを取得します：$s(q, d) = \cos(E(q), E(d))$、ここで $E$ は埋め込み関数です。(この式はシンプルにベクトル検索・近傍探索の式だった...!:thinking:)

<!-- ここまで読んだ! -->

##### **Knowledge-Graph Memory  知識グラフ記憶**

User behaviors in RS are influenced by both internal factors (personality) and external factors (Zhao et al., 2014). 
**RSにおけるユーザ行動は、内部要因（性格）と外部要因の両方に影響されます**（Zhao et al., 2014）。
External factors include the influence of others and prior beliefs about items. 
外部要因には、他者の影響やアイテムに関する先入観が含まれます。
SimUSER employs a knowledge graph (KG) memory to emulate external influences by retrieving evidences with similar relationships and characteristics. 
SimUSERは、類似の関係と特性を持つ証拠を取得することによって外部の影響を模倣するために、知識グラフ（KG）記憶を使用します。

- メモ: 「RSにおけるユーザ行動は、内部要因（性格）と外部要因の両方に影響される」のニュース推薦の例を考える! :thinking:
  - 内部要因 (そのユーザの中に元々あるもの・積み上がったもの)
    - 経済・スタートアップ系の記事を好む
    - 煽りタイトルはあまり好きじゃない
    - 長文記事への耐性は高い/低い
    - 保守的/リベラル寄りな価値観
    - 専門的な記事でも読む or 初心者向けが好き
  - 外部要因 (その人の外から入ってくる影響)
    - 他の人の影響: SNSで話題になってる。友達がシェアしてた。「みんなが読んでます」ランキング上位。
    - 先入観・文脈: 「このメディアの記事は信頼できる」「この著者の記事は面白い」「過去に似たニュースが炎上してた」
    - 関係性ベース: 「この会社の記事 -> 以前読んだあの企業と関連」「この政策 -> あの政治家・政党と関係あり」

##### **Memory Initialization** **記憶の初期化**

The KG memory is initially populated using real-world datasets. 
KG記憶は、実世界のデータセットを使用して最初に構成されます。
It is structured as a graph $G$, defined as: 
それはグラフ $G$ として構成され、次のように定義されます：

$$
G = \{(h, r, t) \mid h, t \in V, r \in E\}
$$

in which each triple $(h,r,t)$ indicates that a relation $r$ exists from head entity $h$ to tail entity $t$. 
ここで、各三重項 $(h,r,t)$ は、ヘッドエンティティ $h$ からテールエンティティ $t$ への関係 $r$ が存在することを示します。
$V$ is a set of entities and represents relationships between them. 
$V$ はエンティティの集合であり、それらの間の関係を表します。
For $E$, instance nodes may represent entities (e.g., user, item), while edges depict the relationships between these entities (e.g., liked). 
$E$ の場合、インスタンスノードはエンティティ（例：ユーザ、アイテム）を表し、エッジはこれらのエンティティ間の関係（例：好ましい）を描写します。
The memory grows with each interaction, capturing the evolving nature of user preferences: 
**記憶は各相互作用とともに成長し、ユーザの嗜好の進化する性質を捉えます：**

$$
G_{t+1} = G_t \cup \{(v_i, e_{ij}, v_j) \mid (v_i, e_{ij}, v_j) \in V \times E \times V\}
$$

<!-- ここまで読んだ! -->

##### **Graph-Aware Dynamic Item Retrieval ** **グラフ認識型動的アイテム取得**

For a user $u$, the retrieval function takes a query item $x$ as input and returns a set of similar items along with their metadata (e.g., ratings). 
ユーザ $u$ に対して、取得関数はクエリアイテム $x$ を入力として受け取り、類似アイテムのセットとそのメタデータ（例：評価）を返します。
We extend PathSim (Sun et al., 2011) to capture both user-item and item-item relationships through path-based similarity. 
PathSim（Sun et al., 2011）を拡張して、パスベースの類似性を通じてユーザ-アイテム関係とアイテム-アイテム関係の両方をキャプチャします。
A relationship path $p_{x \rightarrow y}$ represents a composite relationship between entities $x$ and $y$ in the form of $x -E_1 \rightarrow z -E_2 \rightarrow \ldots -E_l \rightarrow y$, where $E_1$ denotes the edge between entity $x$ and $z$. 
関係パス $p_{x \rightarrow y}$ は、エンティティ $x$ と $y$ の間の複合関係を $x \rightarrow^{E_1} z \rightarrow^{E_2} \ldots \rightarrow^{E_l} y$ の形式で表し、ここで $E_1$ はエンティティ $x$ と $z$ の間のエッジを示します。
For example, in the MovieLens network, the co-actor relation can be described using the length-2 relationship path 
例えば、MovieLensネットワークでは、共演者の関係は長さ2の関係パスを使用して説明できます。

$$
x \rightarrow^{\text{acts-in}} z \rightarrow^{\text{actor}} y
$$

In order to retrieve relevant items based on the query $x$, SimUSER estimates the item-item similarity as: 
クエリ $x$ に基づいて関連アイテムを取得するために、SimUSERはアイテム-アイテムの類似性を次のように推定します：

$$
s_{x,y} = \frac{2 \times | \{p_{x \rightarrow y} : p_{x \rightarrow y} \in \mathcal{P} \} |}{| \{p_{x \rightarrow x} : p_{x \rightarrow x} \in \mathcal{P} \} | + | \{p_{y \rightarrow y} : p_{y \rightarrow y} \in \mathcal{P} \} |}
\tag{2}
$$

where $\mathcal{P}$ is the set of paths between query item $x$ and candidate item $y$, and $p_{x \rightarrow y}$ is a path instance. 
ここで、$\mathcal{P}$ はクエリアイテム $x$ と候補アイテム $y$ の間のパスの集合であり、$p_{x \rightarrow y}$ はパスインスタンスです。
The score $s_{x,y}$ is determined by two factors: (1) the connectivity level, which is the count of paths that connect $x$ and $y$ through $\mathcal{P}$; and (2) the balance of visibility, defined by the number of times these paths are traversed between the two entities. 
スコア $s_{x,y}$ は2つの要因によって決定されます：（1）接続レベル、これは $\mathcal{P}$ を通じて $x$ と $y$ を接続するパスの数であり；（2）可視性のバランス、これはこれらのパスが2つのエンティティ間で通過する回数によって定義されます。
In addition to item-item similarity $s_{x,y}$, we compute user-item similarity $s_{u,y}$ for the target user $u$ and the candidate item $y$, using the same path-based approach, which is further summed up to 
**アイテム-アイテムの類似性 $s_{x,y}$ に加えて、ターゲットユーザ $u$ と候補アイテム $y$ のためにユーザ-アイテムの類似性 $s_{u,y}$ を同じパスベースのアプローチを使用して計算し、さらに次のように合計**します：

$$
s_{x,y} = \alpha \cdot s_{x,y} + (1 - \alpha) \cdot s_{u,y}
$$

making retrieval sensitive to both past interactions of the user $u$ and communities in the graph. 
これにより、retrieval処理は、ユーザ $u$ の過去の相互作用とグラフ内のコミュニティの両方に敏感になります。

<!-- ここまで読んだ! -->

### **3.3 Brain Module** **3.3 ブレインモジュール**

We endow each agent with a decision-making module that derives subsequent actions. 
**各エージェントに、次のアクションを導出する意思決定モジュールを与えます。**

To replicate human-like sequential reasoning, we employ Chain-of-Thought prompting across five key steps. 
**人間のような逐次的推論を再現するために、5つの重要なステップにわたってChain-of-Thoughtプロンプティングを採用します。**

**Multi-round Preference Elicitation: Agents** 
**マルチラウンド好みの引き出し：エージェントは**

browse items page by page, deciding whether to [WATCH] or [SKIP] based on their preferences and history. 
**アイテムをページごとにブラウズし、好みと履歴に基づいて [WATCH] または [SKIP] するかを決定します。**

To mitigate the inherent positive bias in LLMs, SimUSER incorporates a pickiness modifier (You are {pickiness} about {item_type}). 
**LLMの内在的なポジティブバイアスを軽減するために、SimUSERは選り好み修飾子（あなたは {item_type} に対して {pickiness} です）を組み込みます。**

When available, we enrich item descriptions with thumbnail captions for multimodal reasoning. 
**利用可能な場合、マルチモーダル推論のためにアイテムの説明をサムネイルキャプションで豊かにします。**

A multi-round strategy first forms an initial decision $\delta[0]$ based on persona $p$, pickiness $\rho$, and retrieved evidences $E_{k1}$ and $G_{k2}$ from episodic and KG memory. 
**マルチラウンド戦略は、最初にペルソナ $p$、選り好み $\rho$、およびエピソード記憶とKG記憶から取得した証拠 $E_{k1}$ と $G_{k2}$ に基づいて初期決定 $\delta[0]$ を形成します。**

Then, it identifies contradictions between its choice and persona. 
**次に、それは自らの選択とペルソナとの間の矛盾を特定します。**

If conflicts arise or supporting evidence is insufficient, the agent refines its decision: 
**もし矛盾が生じたり、支持する証拠が不十分な場合、エージェントはその決定を洗練させます：**

$$
\delta[t] = \text{LLM}(P_{\text{watch}}, \delta[t-1], p, E_{k1}, G_{k2})
$$
**$$
\delta[t] = \text{LLM}(P_{\text{watch}}, \delta[t-1], p, E_{k1}, G_{k2})
$$**

To improve decision-making, we expand retrieved documents each round ($k_1 \leftarrow k_1 + \Delta k$ and $k_2 \leftarrow k_2 + \Delta k$) until reaching a final decision $\delta[\text{final}]$. 
**意思決定を改善するために、各ラウンドで取得したドキュメントを拡張します（$k_1 \leftarrow k_1 + \Delta k$ および $k_2 \leftarrow k_2 + \Delta k$）最終決定 $\delta[\text{final}]$ に達するまで。**

**Item Evaluation After selecting items of inter-** 
**アイテム評価 興味のあるアイテムを選択した後、**

est, agents express both explicit ratings (1-5) and subjective feelings about watched items, which update their memory and influence future cognition. 
**エージェントは、明示的な評価（1-5）と視聴したアイテムに対する主観的な感情の両方を表現し、これが彼らの記憶を更新し、将来の認知に影響を与えます。**

Unlike existing approaches (Zhang et al., 2023) that neglect rating rationales, Instead, SimUSER leverages the paths of retrieved evidences from the KG memory, 
**評価の根拠を無視する既存のアプローチ（Zhang et al., 2023）とは異なり、SimUSERはKG記憶から取得した証拠のパスを活用します。**



. . ._ −E→l _i, They are_ formatted as plain text and provided as input to the LLM, which generates ratings while explaining how persona, evidences and paths compare to the shortlisted items and influence their rating.
. . ._ −E→l _i、彼らはプレーンテキストとしてフォーマットされ、LLMへの入力として提供され、LLMは評価を生成し、ペルソナ、証拠、経路がショートリストされたアイテムとどのように比較され、評価にどのように影響するかを説明します。

**Action Selection: Based item evaluation and in-** teraction history, agents decide whether to [EXIT] the system, navigate to [NEXT]/[PREVIOUS] pages, or [CLICK] on items for details. 
**アクション選択：アイテム評価とインタラクション履歴に基づいて、エージェントはシステムを[EXIT]するか、[NEXT]/[PREVIOUS]ページに移動するか、アイテムの詳細を[CLICK]するかを決定します。** 
This decision involves estimating its satisfaction with previous recommendations, fatigue level, and emotional state. 
この決定には、以前の推奨に対する満足度、疲労レベル、および感情状態を推定することが含まれます。 
Upon exiting, a satisfaction interview captures opinions about presented recommendations.
退出時に、満足度インタビューが提示された推奨に関する意見を収集します。

**Causal Action Refinement: To address subop-** timal decision-making (e.g., premature exits), we introduce a causal reasoning step where agents generate questions (Q = LLM (atent, H, p, Pcausal)) to validate tentative actions. 
**因果アクションの洗練：最適でない意思決定（例：早期退出）に対処するために、エージェントが仮のアクションを検証するための質問を生成する因果推論ステップを導入します（Q = LLM (atent, H, p, Pcausal)）。** 
For each counterfactual scenario (e.g., "What would happen if you exited _now?"), the agent estimates outcomes and adjusts_ its final action based on cause-effect consistency.
各反事実的シナリオ（例：「今退出したらどうなるか？」）について、エージェントは結果を推定し、因果関係の一貫性に基づいて最終アクションを調整します。

**Post-interaction Reflection: Post-interaction** reflection lets agents learn from interactions and improve future alignment with their persona. 
**ポストインタラクションの反省：ポストインタラクションの反省により、エージェントはインタラクションから学び、将来のペルソナとの整合性を向上させることができます。** 
After collecting interaction data, the agent first determines what to reflect on, then extracts insights and cites the particular records that served as evidence for the insights. 
インタラクションデータを収集した後、エージェントはまず何を反省するかを決定し、次に洞察を抽出し、洞察の証拠として機能した特定の記録を引用します。 
The post-interaction reflections are fed back into the episodic memory.
ポストインタラクションの反省はエピソード記憶にフィードバックされます。



## 4 Experiments 実験

**Settings. All agents are powered by the GPT-4o-** mini version of ChatGPT, except when specified differently, with the number of agents set to 1,000.  
**設定。すべてのエージェントは、指定がない限り、ChatGPTのGPT-4o-ミニバージョンによって動作し、エージェントの数は1,000に設定されています。**

**Baselines We compare SimUSER against RecA-**  
**ベースライン。SimUSERをRecAと比較します。**  

46  
-----  
**MovieLens** **AmazonBook** **Steam**  
**MovieLens** **AmazonBook** **Steam**  

**Method(1:m)** **Accuracy** **Precision** **Recall** **F1 Score** **Accuracy** **Precision** **Recall** **F1 Score** **Accuracy** **Precision** **Recall** **F1 Score**  
**方法(1:m)** **精度** **適合率** **再現率** **F1スコア** **精度** **適合率** **再現率** **F1スコア** **精度** **適合率** **再現率** **F1スコア**  

RecAgent (1:1) 0.5807 0.6391 0.6035 0.6205 0.6035 0.6539 0.6636 0.6587 0.6267 0.6514 0.6490 0.6499  
RecAgent (1:1) 0.5807 0.6391 0.6035 0.6205 0.6035 0.6539 0.6636 0.6587 0.6267 0.6514 0.6490 0.6499  

RecAgent (1:3) 0.5077 0.7396 0.3987 0.5181 0.6144 0.6676 0.4001 0.5003 0.5873 0.6674 0.3488 0.4576  
RecAgent (1:3) 0.5077 0.7396 0.3987 0.5181 0.6144 0.6676 0.4001 0.5003 0.5873 0.6674 0.3488 0.4576  

RecAgent (1:9) 0.4800 0.7491 0.2168 0.3362 0.6222 0.6641 0.1652 0.2647 0.5995 0.6732 0.1744 0.2772  
RecAgent (1:9) 0.4800 0.7491 0.2168 0.3362 0.6222 0.6641 0.1652 0.2647 0.5995 0.6732 0.1744 0.2772  

Agent4Rec (1:1) 0.6912 0.7460 0.6914 0.6982 0.7190 0.7276 0.7335 0.7002 0.6892 0.7059 0.7031 0.6786  
Agent4Rec (1:1) 0.6912 0.7460 0.6914 0.6982 0.7190 0.7276 0.7335 0.7002 0.6892 0.7059 0.7031 0.6786  

Agent4Rec (1:3) 0.6675 0.7623 0.4210 0.5433 0.6707 0.6909 0.4423 0.5098 0.6505 0.7381 0.4446 0.5194  
Agent4Rec (1:3) 0.6675 0.7623 0.4210 0.5433 0.6707 0.6909 0.4423 0.5098 0.6505 0.7381 0.4446 0.5194  

Agent4Rec (1:9) 0.6175 0.7753 0.2139 0.3232 0.6617 0.6939 0.2369 0.3183 0.6021 0.7213 0.1901 0.2822  
Agent4Rec (1:9) 0.6175 0.7753 0.2139 0.3232 0.6617 0.6939 0.2369 0.3183 0.6021 0.7213 0.1901 0.2822  

SimUSER (1:1) **0.7912** 0.7976 **0.7576** **0.7771** **0.8221** **0.7969** **0.7841** **0.7904** **0.7905** 0.8033 **0.7848** **0.7939**  
SimUSER (1:1) **0.7912** 0.7976 **0.7576** **0.7771** **0.8221** **0.7969** **0.7841** **0.7904** **0.7905** 0.8033 **0.7848** **0.7939**  

SimUSER (1:3) 0.7737 0.8173 0.5223 **0.6373** 0.6629 0.7547 0.5657 **0.6467** 0.7425 **0.8048** 0.5376 **0.6446**  
SimUSER (1:3) 0.7737 0.8173 0.5223 **0.6373** 0.6629 0.7547 0.5657 **0.6467** 0.7425 **0.8048** 0.5376 **0.6446**  

SimUSER (1:9) 0.6791 **0.8382** 0.3534 **0.4972** 0.6497 0.7588 0.3229 **0.4530** 0.7119 0.7823 0.2675 **0.3987**  
SimUSER (1:9) 0.6791 **0.8382** 0.3534 **0.4972** 0.6497 0.7588 0.3229 **0.4530** 0.7119 0.7823 0.2675 **0.3987**  

Table 1: User preference alignment across MovieLens, AmazonBook, and Steam datasets.  
**表1：MovieLens、AmazonBook、Steamデータセットにおけるユーザの嗜好の整合性。**  

**Methods** **MovieLens** **AmazonBook** **Steam** **RMSE** **MAE** **RMSE** **MAE** **RMSE** **MAE**  
**方法** **MovieLens** **AmazonBook** **Steam** **RMSE** **MAE** **RMSE** **MAE** **RMSE** **MAE**  

MF 1.2142 0.9971 1.2928 0.9879 1.3148 1.0066  
MF 1.2142 0.9971 1.2928 0.9879 1.3148 1.0066  

AFM 1.1762 0.8723 1.3006 1.1018 1.2763 0.9724  
AFM 1.1762 0.8723 1.3006 1.1018 1.2763 0.9724  

RecAgent 1.1021 0.7632 1.2587 1.1191 1.0766 0.9598  
RecAgent 1.1021 0.7632 1.2587 1.1191 1.0766 0.9598  

RecMind-SI (few-shot) 1.0651 0.6731 1.2139 0.9434 0.9291 0.6981  
RecMind-SI (few-shot) 1.0651 0.6731 1.2139 0.9434 0.9291 0.6981  

Agent4Rec 0.7612 0.7143 0.8788 0.6712 0.7577 0.6880  
Agent4Rec 0.7612 0.7143 0.8788 0.6712 0.7577 0.6880  

SimUSER(sim ⋅ persona) **0.5020** **0.4460** **0.5676** **0.4210** **0.5866** **0.5323**  
SimUSER(sim ⋅ persona) **0.5020** **0.4460** **0.5676** **0.4210** **0.5866** **0.5323**  

SimUSER(zero ⋅ w/o persona) 0.6663 0.5501 0.6865 0.6329 0.6976 0.6544  
SimUSER(zero ⋅ w/o persona) 0.6663 0.5501 0.6865 0.6329 0.6976 0.6544  

SimUSER(zero ⋅ persona) 0.5813 0.5298 0.6542 0.5116 0.6798 0.6151  
SimUSER(zero ⋅ persona) 0.5813 0.5298 0.6542 0.5116 0.6798 0.6151  

SimUSER(sim ⋅ w/o persona) 0.5844 0.5410 0.6712 0.5441 0.6888 0.6401  
SimUSER(sim ⋅ w/o persona) 0.5844 0.5410 0.6712 0.5441 0.6888 0.6401  

Table 2: Rating prediction performance. Bold: best results; underlined: second-best. SimUSER’s improvements are statistically significant (p < 0.05).  
**表2：評価予測性能。太字：最良の結果；下線：2番目に良い。SimUSERの改善は統計的に有意です（p < 0.05）。**  

gent and Agent4Rec, which represent the closest comparable methods. When possible, we report the results of RecMind, an agent-based RS. Some experiments involve two versions of SimUSER: SimUSER(zero) and SimUSER(sim), where SimUSER(sim) agents first interact with the RS — grounding interactions and filling their memories, before answering the tasks.  
**gentとAgent4Recは、最も近い比較可能な方法を表しています。可能な場合、エージェントベースのRSであるRecMindの結果を報告します。一部の実験では、SimUSERの2つのバージョン、SimUSER(zero)とSimUSER(sim)が関与しており、SimUSER(sim)エージェントは最初にRSと相互作用し、相互作用を基にして記憶を満たした後、タスクに回答します。**  

**4.1** **Believably of Synthetic Users**  
**4.1 合成ユーザの信頼性**  

In order to appropriately respond to recommendations, synthetic users must possess a clear understanding of their own preferences.  
推奨に適切に応答するためには、合成ユーザは自分の嗜好を明確に理解している必要があります。  

Thereby, we query the agents to classify items based on whether their human counterparts have interacted with them or not.  
したがって、エージェントに対して、人間の対応者がアイテムと相互作用したかどうかに基づいてアイテムを分類するように問い合わせます。  

We randomly assigned 20 items to each of 1,000 agents, with varying ratios (1:m where _m ∈_ 1, 3, 9 ) of items users had interacted with { } to non-interacted items (yui = 0).  
1,000人のエージェントそれぞれに20個のアイテムをランダムに割り当て、ユーザが相互作用したアイテムと非相互作用アイテムの比率（1:m、ここで _m ∈_ 1, 3, 9）を変えました。  

We treat this as a binary classification task, taking values between 0 and 1.  
これをバイナリ分類タスクとして扱い、0と1の間の値を取ります。  

Table 1 shows SimUSER agents accurately identified items aligned with their tastes, significantly outperforming RecAgent and Agent4Rec across all distractor levels (paired t-tests, 95% confidence, p < 0.002).  
表1は、SimUSERエージェントが自分の嗜好に合ったアイテムを正確に特定し、すべての気を散らすレベルでRecAgentとAgent4Recを大幅に上回ったことを示しています（対応のt検定、95%の信頼度、p < 0.002）。  

**4.2** **Rating Items**  
**4.2 アイテムの評価**  

A key task when interacting with a RS is rating items.  
RSと相互作用する際の重要なタスクは、アイテムを評価することです。  

We compare several LLM-based baselines,  
いくつかのLLMベースのベースラインを比較します。  

_P view_ _N_ like _P like_ _N_ exit _Ssat_  
_P view_ _N_ like _P like_ _N_ exit _Ssat_  

Random 0.301 3.12 0.252 2.85 2.66  
ランダム 0.301 3.12 0.252 2.85 2.66  

Pop 0.395 4.08 0.372 2.90 3.32  
ポップ 0.395 4.08 0.372 2.90 3.32  

MF 0.461 **5.91** 0.443 3.05 3.65  
MF 0.461 **5.91** 0.443 3.05 3.65  

MultVAE 0.514 5.38 0.455 3.18 3.78  
MultVAE 0.514 5.38 0.455 3.18 3.78  

LightGCN **0.557** 5.45 **0.448** **3.29** **3.92**  
LightGCN **0.557** 5.45 **0.448** **3.29** **3.92**  

Table 3: Evaluation of recommendation strategies on a recommendation task from the MovieLens dataset.  
**表3：MovieLensデータセットからの推薦タスクにおける推薦戦略の評価。**  

along with traditional recommendation baselines: MF (Koren et al., 2009) and AFM (Xiao et al., 2017).  
従来の推薦ベースラインであるMF（Koren et al., 2009）およびAFM（Xiao et al., 2017）とともに。  

Across all tasks (Table 2), SimUSER considerably outperforms other LLM-powered agents, mainly due to its KG memory that encapsulates priors about items and their relationships with user interactions.  
すべてのタスク（表2）において、SimUSERは他のLLM駆動のエージェントを大幅に上回り、主にアイテムとユーザの相互作用との関係に関する事前情報をカプセル化したKGメモリによるものです。  

Agent4Rec shows higher RMSE due to hallucinations with niche items not embedded in its LLM weights.  
Agent4Recは、LLMの重みに埋め込まれていないニッチアイテムに関する幻覚のため、より高いRMSEを示します。  

Notably, incorporating a few steps of simulation always decreases the MAE of the model (SimUSER(sim)).  
特に、いくつかのシミュレーションステップを組み込むことで、常にモデルのMAEが減少します（SimUSER(sim)）。  

This is because the grounded interactions augment the context during the multi-round assessment, demonstrating that agents can refine their own preferences for unrated items through interactions with the simulator.  
これは、基盤となる相互作用がマルチラウンド評価中のコンテキストを増強し、エージェントがシミュレーターとの相互作用を通じて未評価のアイテムに対する自分の嗜好を洗練できることを示しています。  

**4.3** **Recommender System Evaluation**  
**4.3 レコメンダーシステムの評価**  

Understanding the efficacy of various recommendation algorithms is crucial for enhancing user satisfaction.  
さまざまな推薦アルゴリズムの有効性を理解することは、ユーザの満足度を向上させるために重要です。  

By simulating human proxies, we can better predict how users will engage with recommender systems, providing valuable interactive metrics.  
人間の代理をシミュレートすることで、ユーザがレコメンダーシステムとどのように関与するかをよりよく予測でき、貴重なインタラクティブメトリクスを提供します。  

We compare various recommendation strategies, including most popular (Pop), matrix factorization (MF) (Koren et al., 2009), LightGCN (He et al., 2020), and MultVAE (Liang et al., 2018), using the MovieLens dataset.  
MovieLensデータセットを使用して、最も人気のある（Pop）、行列分解（MF）（Koren et al., 2009）、LightGCN（He et al., 2020）、およびMultVAE（Liang et al., 2018）を含むさまざまな推薦戦略を比較します。  

Upon exiting, agents rated their satisfaction on a scale from 1 to 10.  
エージェントは、退出時に1から10のスケールで満足度を評価しました。  

Ratings above 3 were considered indicative of a _like. Metrics include average viewing ratio (P view),_  
3を超える評価は「好む」を示すものと見なされました。メトリクスには、平均視聴比率（P view）が含まれます。  

47  
-----  
**MovieLens** **AmazonBook** **Steam**  
**MovieLens** **AmazonBook** **Steam**  

RecAgent 3.01 ± 0.14 3.14 ± 0.13 2.96 ± 0.17  
RecAgent 3.01 ± 0.14 3.14 ± 0.13 2.96 ± 0.17  

Agent4Rec 3.04 ± 0.12 3.21 ± 0.14 3.09 ± 0.16  
Agent4Rec 3.04 ± 0.12 3.21 ± 0.14 3.09 ± 0.16  

SimUSER(w/o persona) 3.72 ± 0.18* 3.65 ± 0.21* 3.61 ± 0.24*  
SimUSER(w/o persona) 3.72 ± 0.18* 3.65 ± 0.21* 3.61 ± 0.24*  

SimUSER(persona) **4.41±0.16*** **3.99±0.18*** **4.02±0.23***  
SimUSER(persona) **4.41±0.16*** **3.99±0.18*** **4.02±0.23***  

Table 4: Human-likeness score evaluated by GPT-4o across recommendation domains. *Significant improvements over best baseline (p < 0.05).  
**表4：推薦ドメイン全体でGPT-4oによって評価された人間らしさスコア。*最良のベースラインに対する有意な改善（p < 0.05）。**  

average number of likes (N like), average ratio of likes (P like), average exit page number (N exit), and average user satisfaction score (Ssat).  
平均「いいね」の数（N like）、平均「いいね」の比率（P like）、平均退出ページ数（N exit）、および平均ユーザ満足度スコア（Ssat）。  

Table 3 demonstrates that agents exhibit higher satisfaction with advanced recommendations versus random and Pop methods, consistent with real-life trends.  
表3は、エージェントがランダムおよびポップ手法に対して高度な推薦に対してより高い満足度を示すことを示しており、実際の傾向と一致しています。  

**4.4** **LLM Evaluator**  
**4.4 LLM評価者**  

As LLM Evaluators (Chiang and Lee, 2023) achieve comparable performance with human evaluators, we use GPT-4o to assess whether agent interactions appear human or AI-generated using a 5-point Likert scale, with higher scores indicating stronger resemblance to human-like responses.  
LLM評価者（Chiang and Lee, 2023）が人間の評価者と同等のパフォーマンスを達成するため、GPT-4oを使用してエージェントの相互作用が人間のものかAI生成のものかを評価します。5段階のリッカートスケールを使用し、高いスコアは人間らしい応答に似ていることを示します。  

Results in Table 4 show our method significantly outperforms Agent4Rec.  
表4の結果は、私たちの方法がAgent4Recを大幅に上回ることを示しています。  

The memory and persona modules are among the main factors contributing to the faithfulness of our method.  
メモリとペルソナモジュールは、私たちの方法の信頼性に寄与する主な要因の一つです。  

We also noticed that letting the agent estimate its tiredness, feeling and emotion greatly enhances the believability and consistency of its responses.  
また、エージェントに疲労感、感情、感覚を推定させることで、その応答の信頼性と一貫性が大幅に向上することに気付きました。  

On the other hand, Agent4Rec’s tendencies to [EXIT] the recommender system early and provide inconsistent ratings for similar items — ranging from low to high, contribute to suspicions of AI involvement.  
一方、Agent4Recがレコメンダーシステムを早期に[EXIT]し、類似アイテムに対して一貫性のない評価を提供する傾向（低から高まで）は、AIの関与に対する疑念を助長します。  

**4.5** **SimUSER for Offline A/B Testing**  
**4.5 オフラインA/BテストのためのSimUSER**  

We have access a proprietary dataset of 55 online A/B tests, encompassing hundred of thousands of food item recommendations.  
私たちは、数十万の食品アイテム推薦を含む55のオンラインA/Bテストの独自データセットにアクセスできます。  

Each test evaluates variations in recommendation strategies, with the average number of visited pages as the primary business metric.  
各テストは、推薦戦略のバリエーションを評価し、訪問ページの平均数を主要なビジネスメトリクスとしています。  

The results, shown in Fig 1, indicate that SimUSER achieves the highest correlation with ground truth values, significantly outperforming Agent4Rec and RecAgent.  
図1に示す結果は、SimUSERが真の値との相関が最も高く、Agent4RecおよびRecAgentを大幅に上回ることを示しています。  

Statistical tests were conducted to validate the significance of SimUSER’s performance over the baselines, with pvalues below 0.05 for all comparisons.  
SimUSERのパフォーマンスがベースラインを上回ることの有意性を検証するために統計的テストが実施され、すべての比較でp値が0.05未満でした。  

SimUSER effectively captures user engagement, offering a cost-effective alternative to online A/B testing.  
SimUSERはユーザのエンゲージメントを効果的に捉え、オンラインA/Bテストのコスト効果の高い代替手段を提供します。  

Figure 1: Spearman correlation between estimated and actual engagement metrics. Higher values indicate better alignment with ground truth metrics.  
**図1：推定されたエンゲージメントメトリクスと実際のエンゲージメントメトリクスとの間のスピアマン相関。高い値は真のメトリクスとのより良い整合性を示します。**  

**Method** _P view_ _N_ like _P like_ _N_ exit _Ssat_  
**方法** _P view_ _N_ like _P like_ _N_ exit _Ssat_  

Baseline 0.521 5.44 0.458 3.21 3.82  
ベースライン 0.521 5.44 0.458 3.21 3.82  

Traditional (nDCG@10) 0.535 5.52 0.462 3.26 3.86  
従来型（nDCG@10） 0.535 5.52 0.462 3.26 3.86  

SimUSER **0.561** **5.80** **0.517** **3.87** **4.09**  
SimUSER **0.561** **5.80** **0.517** **3.87** **4.09**  

Table 5: Performance comparison of parameter selection strategies on various engagement metrics.  
**表5：さまざまなエンゲージメントメトリクスにおけるパラメータ選択戦略のパフォーマンス比較。**  

**4.6** **Optimizing RS with SimUSER**  
**4.6 SimUSERによるRSの最適化**  

We examine whether selecting RS parameters based on SimUSER evaluation or traditional offline metrics (nDCG@10 - TRAD), translates to improved business metrics in the real world.  
SimUSER評価または従来のオフラインメトリクス（nDCG@10 - TRAD）に基づいてRSパラメータを選択することが、実世界のビジネスメトリクスの改善につながるかどうかを検討します。  

We employ the same proprietary dataset.  
同じ独自データセットを使用します。  

The online performance of the baseline system and the two strategies are presented in Table 5.  
ベースラインシステムと2つの戦略のオンラインパフォーマンスは表5に示されています。  

TRAD results in performance on par with the original baseline, demonstrating similar findings as in (Jannach and Jugovac, 2019) — offline metrics do not necessarily translate to business metrics.  
TRADは元のベースラインと同等のパフォーマンスを示し、（Jannach and Jugovac, 2019）と同様の結果を示しています — オフラインメトリクスは必ずしもビジネスメトリクスに変換されるわけではありません。  

SimUSER achieves higher engagement and satisfaction, with improvements in average viewing ratio and satisfaction.  
SimUSERは、平均視聴比率と満足度の改善により、より高いエンゲージメントと満足度を達成します。  



## 5 Conclusion 結論

We present a simulation framework for leveraging LLMs as believable user proxies. 
私たちは、LLMを信頼できるユーザプロキシとして活用するためのシミュレーションフレームワークを提案します。

Our two-phase approach includes persona matching and interactive RS assessment, seeking to align user interactions more closely with real-world user behaviors. 
私たちの二段階アプローチは、ペルソナマッチングとインタラクティブRS評価を含み、ユーザのインタラクションを実世界のユーザ行動により密接に一致させることを目指しています。

We evaluate SimUSER across various recommendation domains, including movies, books, and video games. 
私たちは、映画、書籍、ビデオゲームなど、さまざまな推薦ドメインにわたってSimUSERを評価します。

Results demonstrate closer alignment of our agents with their human counterparts at both micro and macro levels. 
結果は、私たちのエージェントがマイクロおよびマクロの両レベルで人間の対応者とより密接に一致していることを示しています。

We further explore the influence of thumbnails on user engagement and the significance of reviews in user decision-making. 
私たちはさらに、サムネイルがユーザのエンゲージメントに与える影響と、ユーザの意思決定におけるレビューの重要性を探ります。

Experimental findings highlight the potential of LLM-driven simulations in bridging the gap between offline metrics and business metrics. 
実験結果は、LLM駆動のシミュレーションがオフラインメトリクスとビジネスメトリクスのギャップを埋める可能性を強調しています。

As a future direction, we seek to complement our current GPT-4o-based assessments of human-likeness with human evaluation, to further validate the realism of agent behavior. 
将来的な方向性として、私たちは現在のGPT-4oに基づく人間らしさの評価を人間評価で補完し、エージェントの行動のリアリズムをさらに検証することを目指しています。

In addition, we plan to investigate the extent to which LLM-specific biases may influence simulated decisions and explore mitigation strategies. 
さらに、LLM特有のバイアスがシミュレーションされた意思決定にどの程度影響を与えるかを調査し、緩和戦略を探る計画です。



## 6 Ethics Statement 倫理声明

This paper proposes an LLM-empowered agent framework designed to simulate user interactions with recommender systems in a realistic and costeffective manner. 
本論文は、ユーザとレコメンダーシステムとのインタラクションを現実的かつコスト効果の高い方法でシミュレートするために設計されたLLM（大規模言語モデル）を活用したエージェントフレームワークを提案します。

While our approach offers significant benefits in terms of scalability and efficiency, it also raises ethical considerations. 
私たちのアプローチは、スケーラビリティと効率性の面で重要な利点を提供しますが、倫理的な考慮事項も提起します。

The use of such agents could lead to unintended consequences, such as bias amplification, where the synthetic agents might inadvertently reinforce existing stereotypes or present skewed recommendations due to biases in the training data. 
このようなエージェントの使用は、意図しない結果を招く可能性があり、例えばバイアスの増幅が挙げられます。合成エージェントは、トレーニングデータのバイアスにより、既存のステレオタイプを無意識に強化したり、歪んだ推薦を提示したりする可能性があります。

Additionally, there is a risk of manipulation of user preferences, as the synthetic agents could be used to subtly influence user behavior by consistently promoting certain types of content without explicit user consent. 
さらに、合成エージェントは、明示的なユーザの同意なしに特定のタイプのコンテンツを一貫して推進することで、ユーザの好みを巧妙に操作するリスクがあります。

Furthermore, simulating interactions at a broad scale could result in the identification and exploitation of behavioral patterns that might encourage specific user behaviors, potentially leading to negative societal impacts. 
さらに、大規模でのインタラクションのシミュレーションは、特定のユーザ行動を促進する可能性のある行動パターンの特定と悪用を招く可能性があり、社会に対して否定的な影響を及ぼす可能性があります。

Finally, there is a concern that developers or designers might use synthetic users and displace the role of humans and system stakeholders in the design process. 
最後に、開発者やデザイナーが合成ユーザを使用し、設計プロセスにおける人間やシステムの利害関係者の役割を置き換える懸念があります。

We suggest that synthetic uses should not be a substitute for real human input in studies and design processes. 
私たちは、合成ユーザの使用が研究や設計プロセスにおける実際の人間の入力の代替となるべきではないと提案します。

Rather, these agents should be leveraged during the initial design phases to explore concepts, especially in situations where recruiting human participants is impractical or where testing certain theories with real people could be challenging or pose risks. 
むしろ、これらのエージェントは、特に人間の参加者を募集することが非現実的である場合や、実際の人々で特定の理論をテストすることが困難またはリスクを伴う場合に、概念を探求するために初期設計段階で活用されるべきです。

By adhering to these principles, we can ensure that the deployment of synthetic users in the wild is ethical and socially responsible. 
これらの原則を遵守することで、合成ユーザの実社会での展開が倫理的かつ社会的に責任あるものであることを確保できます。



## References 参考文献

Richard C Atkinson and Richard M Shiffrin. 1968. Human memory: A proposed system and its control processes. In Psychology of learning and motivation, volume 2, pages 89–195. Elsevier.  
リチャード・C・アトキンソンとリチャード・M・シフリン。1968年。人間の記憶：提案されたシステムとその制御プロセス。『学習と動機付けの心理学』第2巻、ページ89–195。エルゼビア。

Cheng-Han Chiang and Hung-yi Lee. 2023. Can large language models be an alternative to human evaluations? arXiv preprint arXiv:2305.01937.  
チェン・ハン・チアンとハン・イー・リー。2023年。大規模言語モデルは人間の評価の代替となるか？arXivプレプリントarXiv:2305.01937。

Konstantina Christakopoulou, Filip Radlinski, and Katja Hofmann. 2016. Towards conversational recommender systems. In Proceedings of the 22nd ACM _SIGKDD international conference on knowledge discovery and data mining, pages 815–824._  
コンスタンティナ・クリスタコポウルー、フィリップ・ラドリンスキー、カティア・ホフマン。2016年。対話型レコメンダーシステムに向けて。第22回ACM _SIGKDD国際会議の知識発見とデータマイニングの議事録、ページ815–824_。

Michael Färber, Melissa Coutinho, and Shuzhou Yuan. 2023. Biases in scholarly recommender systems: impact, prevalence, and mitigation. Scientometrics, 128(5):2703–2736.  
マイケル・ファーバー、メリッサ・コウチーニョ、シュズホウ・ユアン。2023年。学術的レコメンダーシステムにおけるバイアス：影響、普及、そして軽減。『サイエンティメトリクス』、128(5):2703–2736。

Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, and Meng Wang. 2020. Lightgcn: Simplifying and powering graph convolution network for recommendation. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval, pages 639–648.  
シャンナン・ハ、クアン・デン、シャン・ワン、ヤン・リー、ヨンドン・ジャン、メン・ワン。2020年。Lightgcn：推薦のためのグラフ畳み込みネットワークの簡素化と強化。第43回国際ACM SIGIR会議の情報検索における研究と開発の議事録、ページ639–648。

Zhankui He, Zhouhang Xie, Rahul Jha, Harald Steck, Dawen Liang, Yesu Feng, Bodhisattwa Prasad Majumder, Nathan Kallus, and Julian McAuley. 2023. Large language models as zero-shot conversational recommenders. In Proceedings of the 32nd ACM _international conference on information and knowledge management, pages 720–730._  
ジャンクイ・ハ、ジョウハン・シエ、ラフル・ジャ、ハラルド・ステック、ダウェン・リャン、イエス・フェン、ボディサットワ・プラサド・マジュムダー、ネイサン・カラス、ジュリアン・マカウリー。2023年。大規模言語モデルをゼロショット対話型レコメンダーとして。第32回ACM _国際情報および知識管理会議の議事録、ページ720–730_。

Yupeng Hou, Junjie Zhang, Zihan Lin, Hongyu Lu, Ruobing Xie, Julian McAuley, and Wayne Xin Zhao. 2024. Large language models are zero-shot rankers for recommender systems. In European Conference _on Information Retrieval, pages 364–381. Springer._  
ユーペン・ホウ、ジュンジエ・ジャン、ズイハン・リン、ホンユ・ルー、ルオビン・シエ、ジュリアン・マカウリー、ウェイン・シン・ジャオ。2024年。大規模言語モデルはレコメンダーシステムのゼロショットランカーである。欧州情報検索会議、ページ364–381。スプリンガー。

Xu Huang, Jianxun Lian, Yuxuan Lei, Jing Yao, Defu Lian, and Xing Xie. 2023. Recommender ai agent: Integrating large language models for interactive recommendations. arXiv preprint arXiv:2308.16505.  
シュー・ファン、ジアンシュン・リアン、ユクシャン・レイ、ジン・ヤオ、デフ・リアン、シン・シエ。2023年。レコメンダーAIエージェント：インタラクティブな推薦のための大規模言語モデルの統合。arXivプレプリントarXiv:2308.16505。

Dietmar Jannach and Michael Jugovac. 2019. Measuring the business value of recommender systems. _ACM Transactions on Management Information Systems (TMIS), 10(4):1–23._  
ディートマール・ヤンナッハとマイケル・ユゴバク。2019年。レコメンダーシステムのビジネス価値の測定。_ACM経営情報システムトランザクション（TMIS）、10(4):1–23_。

Wang-Cheng Kang, Jianmo Ni, Nikhil Mehta, Maheswaran Sathiamoorthy, Lichan Hong, Ed Chi, and Derek Zhiyuan Cheng. 2023. Do llms understand user preferences? evaluating llms on user rating prediction. arXiv preprint arXiv:2305.06474.  
ワン・チェン・カン、ジアンモ・ニ、ニキル・メータ、マヘスワラン・サティアモーティ、リチャン・ホン、エド・チー、デレク・ジーユアン・チェン。2023年。LLMsはユーザの好みを理解しているか？ユーザ評価予測におけるLLMsの評価。arXivプレプリントarXiv:2305.06474。

Byungwan Koh and Fuquan Cui. 2022. An exploration of the relation between the visual attributes of thumbnails and the view-through of videos: The case of branded video content. Decision Support Systems, 160:113820.  
ビョンワン・コーとフークアン・ツイ。2022年。サムネイルの視覚的属性と動画の視聴率との関係の探求：ブランド動画コンテンツのケース。『意思決定支援システム』、160:113820。

Yehuda Koren, Robert Bell, and Chris Volinsky. 2009. Matrix factorization techniques for recommender systems. Computer, 42(8):30–37.  
イェフダ・コレン、ロバート・ベル、クリス・ボリンキー。2009年。レコメンダーシステムのための行列分解技術。『コンピュータ』、42(8):30–37。

Wenqiang Lei, Xiangnan He, Yisong Miao, Qingyun Wu, Richang Hong, Min-Yen Kan, and Tat-Seng Chua. 2020. Estimation-action-reflection: Towards deep interaction between conversational and recommender systems. In Proceedings of the 13th International Conference on Web Search and Data Mining, pages 304–312.  
ウェンチャン・レイ、シャンナン・ハ、イーソン・ミャオ、チンユン・ウー、リチャン・ホン、ミン・イェン・カン、タット・セン・チュア。2020年。推定-行動-反射：対話型システムとレコメンダーシステムの深い相互作用に向けて。第13回国際ウェブ検索とデータマイニング会議の議事録、ページ304–312。

Jinming Li, Wentao Zhang, Tian Wang, Guanglei Xiong, Alan Lu, and Gerard Medioni. 2023. Gpt4rec: A generative framework for personalized recommendation and user interests interpretation. arXiv preprint _arXiv:2304.03879._  
ジンミン・リー、ウェンタオ・ジャン、ティアン・ワン、グアンレイ・シオン、アラン・ルー、ジェラード・メディオニ。2023年。Gpt4rec：パーソナライズされた推薦とユーザの興味の解釈のための生成フレームワーク。arXivプレプリント _arXiv:2304.03879_。

Yang Li, Kangbo Liu, Ranjan Satapathy, Suhang Wang, and Erik Cambria. 2024. Recent developments in recommender systems: A survey. IEEE Computational _Intelligence Magazine, 19(2):78–95._  
ヤン・リー、カンボ・リウ、ランジャン・サタパティ、スーハン・ワン、エリック・カンブリア。2024年。レコメンダーシステムの最近の発展：調査。IEEE計算知能マガジン、19(2):78–95。

Dawen Liang, Rahul G Krishnan, Matthew D Hoffman, and Tony Jebara. 2018. Variational autoencoders for collaborative filtering. In Proceedings of the 2018 _world wide web conference, pages 689–698._  
ダウェン・リャン、ラフル・G・クリシュナン、マシュー・D・ホフマン、トニー・ジェバラ。2018年。協調フィルタリングのための変分オートエンコーダ。2018年 _ワールドワイドウェブ会議の議事録、ページ689–698_。

Yuqing Liu, Yu Wang, Lichao Sun, and Philip S Yu. 2024. Rec-gpt4v: Multimodal recommendation with large vision-language models. arXiv preprint _arXiv:2402.08670._  
ユーチン・リウ、ユー・ワン、リチャオ・スン、フィリップ・S・ユー。2024年。Rec-gpt4v：大規模ビジョン-言語モデルを用いたマルチモーダル推薦。arXivプレプリント _arXiv:2402.08670_。

Andrew Maas, Raymond E Daly, Peter T Pham, Dan Huang, Andrew Y Ng, and Christopher Potts. 2011. Learning word vectors for sentiment analysis. In _Proceedings of the 49th annual meeting of the association for computational linguistics: Human language technologies, pages 142–150._  
アンドリュー・マース、レイモンド・E・デイリー、ピーター・T・ファム、ダン・ファン、アンドリュー・Y・ング、クリストファー・ポッツ。2011年。感情分析のための単語ベクトルの学習。_計算言語学会第49回年次総会の議事録：人間の言語技術、ページ142–150_。

Tien T Nguyen, F Maxwell Harper, Loren Terveen, and Joseph A Konstan. 2018. User personality and user satisfaction with recommender systems. Information _Systems Frontiers, 20:1173–1189._  
ティエン・T・グエン、F・マクスウェル・ハーパー、ローレン・テルビーン、ジョセフ・A・コンスタン。2018年。ユーザの性格とレコメンダーシステムに対するユーザの満足度。情報システムのフロンティア、20:1173–1189。

Yizhou Sun, Jiawei Han, Xifeng Yan, Philip S Yu, and Tianyi Wu. 2011. Pathsim: Meta path-based top-k similarity search in heterogeneous information networks. Proceedings of the VLDB Endowment, 4(11):992–1003.  
イージョウ・スン、ジャウェイ・ハン、シーフェン・ヤン、フィリップ・S・ユー、ティアンイー・ウー。2011年。Pathsim：異種情報ネットワークにおけるメタパスベースのトップk類似性検索。VLDBエンダウメントの議事録、4(11):992–1003。

Lei Wang, Jingsen Zhang, Hao Yang, Zhiyuan Chen, Jiakai Tang, Zeyu Zhang, Xu Chen, Yankai Lin, Ruihua Song, Wayne Xin Zhao, and 1 others. 2023a. User behavior simulation with large language model based agents. arXiv preprint arXiv:2306.02552.  
レイ・ワン、ジンセン・ジャン、ハオ・ヤン、ジーユアン・チェン、ジカイ・タン、ゼユ・ジャン、シュー・チェン、ヤンカイ・リン、ルイファ・ソン、ウェイン・シン・ジャオ、他1名。2023年。大規模言語モデルに基づくエージェントによるユーザ行動シミュレーション。arXivプレプリントarXiv:2306.02552。

Xinyuan Wang, Liang Wu, Liangjie Hong, Hao Liu, and Yanjie Fu. 2024. Llm-enhanced user-item interactions: Leveraging edge information for optimized recommendations. arXiv preprint arXiv:2402.09617.  
シンユアン・ワン、リャン・ウー、リャンジエ・ホン、ハオ・リウ、ヤンジエ・フー。2024年。LLM強化ユーザ-アイテムインタラクション：最適化された推薦のためのエッジ情報の活用。arXivプレプリントarXiv:2402.09617。

Yancheng Wang, Ziyan Jiang, Zheng Chen, Fan Yang, Yingxue Zhou, Eunah Cho, Xing Fan, Xiaojiang Huang, Yanbin Lu, and Yingzhen Yang. 2023b. Recmind: Large language model powered agent for recommendation. arXiv preprint arXiv:2308.14296.  
ヤンチェン・ワン、ズイヤン・ジャン、ジェン・チェン、ファン・ヤン、インシュエ・ジョウ、ユナ・チョ、シン・ファン、シャオジャン・ホアン、ヤンビン・ルー、インジェン・ヤン。2023年。Recmind：大規模言語モデルを活用した推薦エージェント。arXivプレプリントarXiv:2308.14296。

Jun Xiao, Hao Ye, Xiangnan He, Hanwang Zhang, Fei Wu, and Tat-Seng Chua. 2017. Attentional factorization machines: Learning the weight of feature interactions via attention networks. arXiv preprint _arXiv:1708.04617._  
ジュン・シャオ、ハオ・イエ、シャンナン・ハ、ハンワン・ジャン、フェイ・ウー、タット・セン・チュア。2017年。注意機構を用いた因子分解機械：注意ネットワークを介して特徴相互作用の重みを学習する。arXivプレプリント _arXiv:1708.04617_。

Heng Yang, Chen Zhang, and Ke Li. 2023. Pyabsa: A modularized framework for reproducible aspect-based sentiment analysis. pages 5117–5122.  
ヘン・ヤン、チェン・ジャン、ケ・リー。2023年。Pyabsa：再現可能なアスペクトベースの感情分析のためのモジュール化フレームワーク。ページ5117–5122。

Yuan Yao, Tianyu Yu, Ao Zhang, Chongyi Wang, Junbo Cui, Hongji Zhu, Tianchi Cai, Haoyu Li, Weilin Zhao, Zhihui He, Qianyu Chen, Huarong Zhou, Zhensheng Zou, Haoye Zhang, Shengding Hu, Zhi Zheng, Jie Zhou, Jie Cai, Xu Han, and 4 others. 2024. Minicpmv: A gpt-4v level mllm on your phone. arXiv preprint _2408.01800._  
ユアン・ヤオ、ティアンユ・ユー、アオ・ジャン、チョンイー・ワン、ジュンボ・ツイ、ホンジ・ジュ、ティアンチ・ツァイ、ハオユ・リー、ウェイリン・ジャオ、ジーフイ・ハ、チャンユ・チェン、フアロン・ジョウ、ジェンシェン・ゾウ、ハオイ・ジャン、シェンディン・フー、ジ・ジェン、ジエ・ジョウ、ジエ・ツァイ、シュー・ハン、他4名。2024年。Minicpmv：あなたの電話でのgpt-4vレベルのmllm。arXivプレプリント _2408.01800_。

Se-eun Yoon, Zhankui He, Jessica Maria Echterhoff, and Julian McAuley. 2024. Evaluating large language models as generative user simulators for conversational recommendation. _arXiv preprint arXiv:2403.09738._  
セウン・ユン、ジャンクイ・ハ、ジェシカ・マリア・エヒターホフ、ジュリアン・マカウリー。2024年。対話型推薦のための生成ユーザシミュレーターとしての大規模言語モデルの評価。_arXivプレプリントarXiv:2403.09738_。

Guanghu Yuan, Fajie Yuan, Yudong Li, Beibei Kong, Shujie Li, Lei Chen, Min Yang, Chenyun Yu, Bo Hu, Zang Li, Yu Xu, and Xiaohu Qie. 2022. Tenrec: A large-scale multipurpose benchmark dataset for recommender systems. In Thirty-sixth Conference _on Neural Information Processing Systems Datasets and Benchmarks Track._  
グアンフー・ユアン、ファジエ・ユアン、ユードン・リー、ベイベイ・コン、シュージエ・リー、レイ・チェン、ミン・ヤン、チェンユン・ユー、ボー・フー、ザン・リー、ユー・シュー、シャオフー・チエ。2022年。Tenrec：レコメンダーシステムのための大規模な多目的ベンチマークデータセット。第36回 _神経情報処理システムデータセットとベンチマークトラックに関する会議_。

An Zhang, Leheng Sheng, Yuxin Chen, Hao Li, Yang Deng, Xiang Wang, and Tat-Seng Chua. 2023. On generative agents in recommendation. arXiv preprint _arXiv:2310.10108._  
アン・ジャン、レヘン・シェン、ユシン・チェン、ハオ・リ、ヤン・デン、シャン・ワン、タット・セン・チュア。2023年。推薦における生成エージェントについて。arXivプレプリント _arXiv:2310.10108_。

Jizhi Zhang, Keqin Bao, Wenjie Wang, Yang Zhang, Wentao Shi, Wanhong Xu, Fuli Feng, and Tat-Seng Chua. 2024a. Prospect personalized recommendation on large language model-based agent platform. arXiv _preprint arXiv:2402.18240._  
ジジ・ジャン、ケキン・バオ、ウェンジエ・ワン、ヤン・ジャン、ウェンタオ・シー、ワンホン・シュー、フーリ・フェン、タット・セン・チュア。2024年。大規模言語モデルベースのエージェントプラットフォームにおける見込みパーソナライズド推薦。arXiv _プレプリントarXiv:2402.18240_。

Junjie Zhang, Yupeng Hou, Ruobing Xie, Wenqi Sun, Julian McAuley, Wayne Xin Zhao, Leyu Lin, and JiRong Wen. 2024b. Agentcf: Collaborative learning with autonomous language agents for recommender systems. In Proceedings of the ACM on Web Conference 2024, pages 3679–3689.  
ジュンジエ・ジャン、ユーペン・ホウ、ルオビン・シエ、ウェンチャン・スン、ジュリアン・マカウリー、ウェイン・シン・ジャオ、レイユ・リン、ジロン・ウェン。2024年。Agentcf：レコメンダーシステムのための自律言語エージェントとの協調学習。ACMウェブ会議2024の議事録、ページ3679–3689。

Shuai Zhang, Lina Yao, Aixin Sun, and Yi Tay. 2019. Deep learning based recommender system: A survey and new perspectives. ACM computing surveys _(CSUR), 52(1):1–38._  
シュアイ・ジャン、リナ・ヤオ、アイシン・サン、イー・テイ。2019年。深層学習に基づくレコメンダーシステム：調査と新しい視点。ACMコンピューティングサーベイ _(CSUR)、52(1):1–38_。

Kesen Zhao, Shuchang Liu, Qingpeng Cai, Xiangyu Zhao, Ziru Liu, Dong Zheng, Peng Jiang, and Kun Gai. 2023. Kuaisim: A comprehensive simulator for recommender systems. Advances in Neural Information Processing Systems, 36:44880–44897.  
ケセン・ジャオ、シューチャン・リウ、チンペン・ツァイ、シャンユ・ジャオ、ジル・リウ、ドン・ジェン、ペン・ジャン、クン・ガイ。2023年。Kuaisim：レコメンダーシステムのための包括的なシミュレーター。神経情報処理システムの進展、36:44880–44897。

Tong Zhao, Julian McAuley, and Irwin King. 2014. Leveraging social connections to improve personalized ranking for collaborative filtering. In Proceedings of the 23rd ACM international conference on conference on information and knowledge management, pages 261–270.  
トン・ジャオ、ジュリアン・マカウリー、アーウィン・キング。2014年。ソーシャルコネクションを活用して協調フィルタリングのためのパーソナライズドランキングを改善する。第23回ACM国際会議の情報と知識管理に関する議事録、ページ261–270。



## A Experimental Setup 実験設定

**Experimental Settings. We separate the dataset** into training, validation, and test sets (80/10/10%), using a time-based split. 
**実験設定。データセットを** トレーニング、バリデーション、テストセット（80/10/10%）に分割し、時間ベースの分割を使用します。

This ensures to reflect temporal distribution shift that may be observed in the real-world. 
これにより、実世界で観察される可能性のある時間的分布のシフトを反映することが保証されます。

Relationships between users and items from the training/validation and test sets were excluded from the knowledge graph memory to prevent data leakage. 
トレーニング/バリデーションおよびテストセットのユーザとアイテムの関係は、データ漏洩を防ぐために知識グラフメモリから除外されました。

These datasets are employed for the initialization of each agent — persona and memory modules, as well as self-consistent persona matching. 
これらのデータセットは、各エージェントの初期化（ペルソナおよびメモリモジュール、自己一貫性のあるペルソナマッチング）に使用されます。

In order to address privacy concerns, the name and gender are omitted. 
プライバシーの懸念に対処するために、名前と性別は省略されています。

Moreover, for the sake of generality, we do not utilize userspecific information available in these datasets, relying instead on the personas identified in Phase 1 of SimUSER. 
さらに、一般性のために、これらのデータセットで利用可能なユーザ固有の情報は使用せず、SimUSERのフェーズ1で特定されたペルソナに依存します。

In this paper, we report results for SimUSER with simulation SimUSER(sim), and without simulation SimUSER(zero). 
本論文では、シミュレーションSimUSER(sim)を用いたSimUSERの結果と、シミュレーションなしのSimUSER(zero)の結果を報告します。

In SimUSER(zero), the agent’s memory module is initialized from the history of its human counterpart. 
SimUSER(zero)では、エージェントのメモリモジュールは、その人間の対応者の履歴から初期化されます。

When the review score for an item is greater than 4, the agent stores a memory entry in the form I liked {item_name} based on my review score of {score}. 
アイテムのレビュースコアが4を超えると、エージェントは「I liked {item_name} based on my review score of {score}」という形式でメモリエントリを保存します。

For a score of 2 or below, the following format is utilized I disliked {item_name} based on my review score of {score}. 
スコアが2以下の場合、次の形式が使用されます。「I disliked {item_name} based on my review score of {score}」。

Neutral scores result in the entry I felt neutral about {item_name} based on my review score of {score}. 
中立的なスコアは、「I felt neutral about {item_name} based on my review score of {score}」というエントリになります。

In SimUSER(sim), agents can also interact with the recommender systems (training set) for up to 20 pages or exit the system at any time. 
SimUSER(sim)では、エージェントは推薦システム（トレーニングセット）と最大20ページまで対話することができ、いつでもシステムを終了できます。

The corresponding interactions are used to enhance the memory module. 
対応するインタラクションは、メモリモジュールを強化するために使用されます。

In all the experiments, items rated ≥ 4 are considered as liked by the user, while items ≤ 2 are considered as disliked. 
すべての実験において、評価が≥ 4のアイテムはユーザに好まれたと見なされ、評価が≤ 2のアイテムは嫌われたと見なされます。

These interactions are stored both as plain text in the episodic memory and as relationships in the knowledge graph memory. 
これらのインタラクションは、エピソードメモリのプレーンテキストとして、また知識グラフメモリの関係として保存されます。

These simulated interactions with the RS are stored in the episodic memory with the following format: 
RSとのこれらのシミュレートされたインタラクションは、次の形式でエピソードメモリに保存されます：

The recommender system recommended the following {item_type} to me on page {page_number}: {name_all_items}, among them, I selected {watched_items} and rate them {ratings} respectively. 
推薦システムは、ページ{page_number}で私に次の{item_type}を推薦しました：{name_all_items}の中から、私は{watched_items}を選択し、それぞれ{ratings}と評価しました。

I dislike the rest {item_type} items: {dislike_items}. 
残りの{item_type}アイテムは嫌いです：{dislike_items}。

In some sets of experiments, we report performance without persona matching SimUSER(w/o persona), and with persona matching SimUSER(persona). 
いくつかの実験セットでは、ペルソナマッチングなしのSimUSER(w/o persona)とペルソナマッチングありのSimUSER(persona)のパフォーマンスを報告します。

In where P1 corresponds to not picky, P2 corresponds to moderately picky, and P3 corresponds to extremely picky. 
ここで、P1は「好みがない」、P2は「やや好みがある」、P3は「非常に好みがある」に対応します。

The persona attributes are estimated as follows: 
ペルソナ属性は次のように推定されます：

- Engagement quantifies the frequency and breadth of a user’s interactions with recommended items, distinguishing between users who extensively watch and rate many of items and those who confine themselves to a minimal set. 
- エンゲージメントは、ユーザが推薦されたアイテムとどれだけ頻繁に広範囲に対話するかを定量化し、多くのアイテムを広く視聴し評価するユーザと、最小限のセットに制限するユーザを区別します。

The engagement trait for user u 
ユーザuのエンゲージメント特性は

the absence of persona matching, personality traits, age, occupation and taste summary are omitted from the prompts. 
ペルソナマッチングがない場合、性格特性、年齢、職業、嗜好の要約はプロンプトから省略されます。

Matrix factorization (MF) is utilized as the recommender model unless specified otherwise. 
行列分解（MF）は、特に指定がない限り、推薦モデルとして使用されます。

In our simulator, agents are presented with four items n = 4 per page and allowed to interact by viewing and rating items based on their preferences. 
私たちのシミュレーターでは、エージェントはページごとに4つのアイテム（n = 4）を提示され、好みに基づいてアイテムを視聴し評価することが許可されます。

When the output of the LLM deviated from the desired format, resulting in errors, the LLM was re-prompted with the following instruction: 
LLMの出力が望ましい形式から逸脱し、エラーが発生した場合、LLMは次の指示で再プロンプトされました：

You have one more chance to provide the correct answer. 
「正しい答えを提供するためのチャンスがもう一度あります。」

The path-score used during the retrieval of evidences from the KG memory, we further combine this score with user-item similarity ($s_{x,y} = \alpha \cdot s_{x,y} + (1 - \alpha) \cdot s_{u,y}$) and enhance it with semantic similarity using embeddings from OpenAI’s text-embedding-3-small model. 
KGメモリから証拠を取得する際に使用されるパススコアは、ユーザアイテムの類似性と組み合わせられ（$s_{x,y} = \alpha \cdot s_{x,y} + (1 - \alpha) \cdot s_{u,y}$）、OpenAIのtext-embedding-3-smallモデルからの埋め込みを使用して意味的類似性で強化されます。

The top-k2 items, their attributes, and paths are returned to condition the brain module. 
トップk2アイテム、その属性、およびパスが脳モジュールの条件付けに返されます。

As mentioned above, we leverage GPT-4o-mini as the LLM backbone in all the experiments unless stated differently. 
上記のように、異なると明記されていない限り、すべての実験でLLMのバックボーンとしてGPT-4o-miniを活用します。

We use $\alpha = 0.8$ to balance item-item similarity with user-item similarity. 
アイテム間の類似性とユーザアイテムの類似性をバランスさせるために、$\alpha = 0.8$を使用します。

We set $k_2 = 3$ when retrieving similar items from the knowledge graph-memory, and $k_1 = 5$ for the episodic memory. 
知識グラフメモリから類似アイテムを取得する際に$k_2 = 3$を設定し、エピソードメモリには$k_1 = 5$を設定します。

The titles and ratings of retrieved items from the knowledge graph are concatenated to condition decision-making prompts. 
知識グラフから取得したアイテムのタイトルと評価は、意思決定プロンプトの条件付けのために連結されます。

Empirically, we set the weight of node embeddings to 0.25 when computing top-k2 scores. 
経験的に、トップk2スコアを計算する際にノード埋め込みの重みを0.25に設定します。

Documents and embedding of text (E) were obtained using text-embedding-3-small. 
文書とテキストの埋め込み（E）は、text-embedding-3-smallを使用して取得されました。

Given the average rating $\bar{R}$ of a user: $\bar{R} = \frac{1}{N} \sum_{i=1}^{N} r_{ui}$, the pickiness level $P_{\bar{R}}$ of a user was determined based on the following thresholds: 
ユーザの平均評価$\bar{R}$が与えられた場合：$\bar{R} = \frac{1}{N} \sum_{i=1}^{N} r_{ui}$、ユーザの好みのレベル$P_{\bar{R}}$は次の閾値に基づいて決定されました：

$P_1$ if $\bar{R} \geq 4.5$ 
$P_2$ if $3.5 \leq \bar{R} < 4.5$ 
$P_3$ if $\bar{R} < 3.5$ 
$P_{\bar{R}} = \begin{cases} 
P_1 & \text{if } \bar{R} \geq 4.5 \\ 
P_2 & \text{if } 3.5 \leq \bar{R} < 4.5 \\ 
P_3 & \text{if } \bar{R} < 3.5 
\end{cases}$

Figure 2: The SimUSER framework for evaluating a movie recommender system. 
図2：映画推薦システムを評価するためのSimUSERフレームワーク。

can be mathematically expressed as: $T_{act}[u] = \sum_{i \in I} y_{ui}$. 
数学的には次のように表現できます：$T_{act}[u] = \sum_{i \in I} y_{ui}$。

confidence scores. 
信頼スコア。

In Appendix C.7, we compare the results of SimUSER taking as input: 1) the original movie poster, 2) a random screenshot from the movie trailer on YouTube, 3) the original movie poster distorted with a blue color filter (hue=30, lightness=30, saturation=30). 
付録C.7では、SimUSERの結果を次の入力で比較します：1）元の映画ポスター、2）YouTubeの映画トレーラーからのランダムなスクリーンショット、3）青色フィルター（hue=30、lightness=30、saturation=30）で歪められた元の映画ポスター。

An illustration of the method is provided in Figure 2, detailing the interaction between its components and their roles within the proposed framework. 
この方法の説明は図2に示されており、そのコンポーネント間の相互作用と提案されたフレームワーク内での役割が詳述されています。

**A.1** **Brain Module Details**
**A.1** **脳モジュールの詳細**

We now provide a comprehensive explanation of the Brain Module, detailing the implementation and technical details. 
ここでは、脳モジュールの包括的な説明を提供し、実装と技術的詳細を詳述します。

To replicate human-like sequential reasoning, we employ Chain-of-Thought prompting, repeatedly performing the five steps. 
人間のような逐次的推論を再現するために、Chain-of-Thoughtプロンプティングを使用し、5つのステップを繰り返し実行します。

**A.2** **Multi-round Preference Elicitation**
**A.2** **マルチラウンドの嗜好引き出し**

We employ a multi-round preference elicitation strategy to refine the user’s choice. 
ユーザの選択を洗練させるために、マルチラウンドの嗜好引き出し戦略を採用します。

First, an initial decision $\delta[0]$ is formed based on the agent’s persona $p$, pickiness level $\rho$, and retrieved evidences $E_{k1}$ $G_{k2}$ from the episodic and KG memory respectively. 
まず、エージェントのペルソナ$p$、好みのレベル$\rho$、およびエピソードメモリとKGメモリから取得した証拠$E_{k1}$ $G_{k2}$に基づいて初期決定$\delta[0]$が形成されます。

Along with this decision, the agent provides a reason for its choice and cites the supporting evidence, if any. 
この決定に加えて、エージェントはその選択の理由を提供し、支持する証拠があれば引用します。

Next, the agent checks for contradictions, such as deciding to watch a pure horror film while the persona indicates strong aversion to horror. 
次に、エージェントは矛盾をチェックします。たとえば、ペルソナがホラーに対して強い嫌悪感を示しているのに、純粋なホラー映画を観ることを決定する場合です。

If a conflict arises or cannot find enough supporting evidences, the agent is prompted to confirm or modify the initial decision, resulting in an updated decision $\delta[t] = \text{LLM}(P_{watch}, \delta[t-1], p, E_{k1}, G_{k2})$, where $P_{watch}$ is the task prompt, and $G_t$ and $E(t)$ are retrieved evidences. 
もし矛盾が生じるか、十分な支持証拠が見つからない場合、エージェントは初期決定を確認または修正するよう促され、更新された決定$\delta[t] = \text{LLM}(P_{watch}, \delta[t-1], p, E_{k1}, G_{k2})$が得られます。ここで、$P_{watch}$はタスクプロンプトであり、$G_t$と$E(t)$は取得された証拠です。

To assist the agent’s decision-making, we expand the retrieved documents at each round: $k_1 \leftarrow k_1 + \Delta k$ and $k_2 \leftarrow k_2 + \Delta k$, exposing 
エージェントの意思決定を支援するために、各ラウンドで取得した文書を拡張します：$k_1 \leftarrow k_1 + \Delta k$および$k_2 \leftarrow k_2 + \Delta k$、露出させます。

- Conformity measures how closely a user’s ratings align with average item ratings, drawing a distinction between users with unique perspectives and those whose opinions closely mirror popular sentiments. 
- 一致性は、ユーザの評価が平均アイテム評価とどれだけ一致しているかを測定し、独自の視点を持つユーザと、一般的な感情に近い意見を持つユーザを区別します。

For user $u$, the conformity trait is defined as: $T_{conf}[u] = \sum_{i \in I_1} y_{ui} \cdot \left| r_{ui} - R_i \right|^2$. 
ユーザ$u$の一致性特性は次のように定義されます：$T_{conf}[u] = \sum_{i \in I_1} y_{ui} \cdot \left| r_{ui} - R_i \right|^2$。

- Variety reflects the user’s proclivity toward a diverse range of item genres or their inclination toward specific genres. 
- バラエティは、ユーザが多様なアイテムジャンルに対して持つ傾向や特定のジャンルに対する傾向を反映します。

The variety trait for user $u$ is formulated as: $T_{div}[u] = |U_i \in \{y_{ui}=1\} g_i|$. 
ユーザ$u$のバラエティ特性は次のように定式化されます：$T_{div}[u] = |U_i \in \{y_{ui}=1\} g_i|$。

To encode users’ unique tastes in natural language, we utilize the summary $s_u$ obtained in Phase 1, which describes long-term preferences. 
ユーザの独自の嗜好を自然言語でエンコードするために、フェーズ1で得られた要約$s_u$を利用し、長期的な嗜好を説明します。

To generate captions, for each item $i$, we first generate an initial caption draft $i^{*}$ by querying: $i^{*} = \text{LLM}(P_{caption}, i)$, where $P_{caption}$ is the task prompt. 
キャプションを生成するために、各アイテム$i$について、最初に初期キャプションドラフト$i^{*}$を生成します：$i^{*} = \text{LLM}(P_{caption}, i)$、ここで$P_{caption}$はタスクプロンプトです。

To reduce hallucination, we then decompose $i^{*}$ into atomic claims $\{ a_1, \ldots, a_m \}$, each describing a specific, factual statement (e.g., “The movie is scary”), rather than subjective opinions. 
ハルシネーションを減らすために、次に$i^{*}$を原子的な主張$\{ a_1, \ldots, a_m \}$に分解します。各主張は特定の事実に基づく声明（例：「その映画は怖い」）を説明します。

Next, each claim $a_k$ is formed into a polar (yes/no) query, and an open-source MLLM (Yao et al., 2024) is queried to generate the confidence of agreement and disagreement as the claim score $s_a = (p_{yes}, p_{no})$, where $p_{yes}$ is the probability of answering with “yes” and $p_{no}$ is the probability of answering with “no”. 
次に、各主張$a_k$は極性（はい/いいえ）クエリに形成され、オープンソースのMLLM（Yao et al., 2024）に問い合わせて、合意と不合意の信頼度を主張スコア$s_a = (p_{yes}, p_{no})$として生成します。ここで、$p_{yes}$は「はい」と答える確率であり、$p_{no}$は「いいえ」と答える確率です。

Finally, the original caption is refined in order to obtain the item’s caption $i_{caption} = \text{LLM}(i^{*}, P_{combine}, (a, s_a), \ldots)$. 
最後に、元のキャプションは洗練され、アイテムのキャプション$i_{caption} = \text{LLM}(i^{*}, P_{combine}, (a, s_a), \ldots)$が得られます。

This minimizes the risk of agents selecting items based on inaccurate captions by ensuring the generated descriptions are fact-based and supported by 
これにより、生成された説明が事実に基づいており、追加の関連アイテムや過去のインタラクションによってサポートされることを保証することで、エージェントが不正確なキャプションに基づいてアイテムを選択するリスクが最小限に抑えられます。

additional relevant items or past interactions. This continues until a final decision $\delta[final]$ is reached. 
追加の関連アイテムや過去のインタラクション。このプロセスは、最終決定$\delta[final]$が達成されるまで続きます。

**A.3** **Providing Feelings and Rating Items**
**A.3** **感情の提供とアイテムの評価**

Once the user identifies the items of interest $\delta[final] = \{i_1, \ldots\}$, they express their reactions through both explicit ratings and subjective feelings. 
ユーザが興味のあるアイテム$\delta[final] = \{i_1, \ldots\}$を特定すると、彼らは明示的な評価と主観的な感情の両方を通じて反応を表現します。

Intuitively, a real user may produce much feelings after watching an item, which will be stored in their memory and influence their future cognition and behaviors. 
直感的に、実際のユーザはアイテムを視聴した後に多くの感情を生み出す可能性があり、これが彼らの記憶に保存され、将来の認知や行動に影響を与えます。

Along with the item rating $\in \{1, 2, 3, 4, 5\}$, we query the user’s feelings $\{ \}$ about the watched items and leverage such information to update the memory module. 
アイテム評価$\in \{1, 2, 3, 4, 5\}$に加えて、視聴したアイテムに対するユーザの感情$\{ \}$を問い合わせ、その情報を利用してメモリモジュールを更新します。

Newly liked and disliked items are fed back into the memory module. 
新たに好まれたアイテムと嫌われたアイテムはメモリモジュールにフィードバックされます。

Existing approaches (Zhang et al., 2023) neglect the underlying rationale behind user ratings. 
既存のアプローチ（Zhang et al., 2023）は、ユーザ評価の背後にある根本的な理由を無視しています。

Instead, SimUSER leverages the paths of each retrieved evidences $i$ from the KG memory, 
代わりに、SimUSERはKGメモリから取得された各証拠$i$のパスを活用します、

$u \xrightarrow{E} 1 \xrightarrow{E} 2 \ldots \xrightarrow{E} l \ x$. 
$u \xrightarrow{E} 1 \xrightarrow{E} 2 \ldots \xrightarrow{E} l \ x$。

These paths are formatted as plain text and provided as input to the LLM, which generates ratings while explaining how persona, evidences and paths compare to the shortlisted items and influence their rating. 
これらのパスはプレーンテキストとしてフォーマットされ、LLMへの入力として提供され、ペルソナ、証拠、パスが短縮リストのアイテムとどのように比較され、評価に影響を与えるかを説明しながら評価を生成します。

**A.4** **Emotion-driven Action Selection**
**A.4** **感情駆動のアクション選択**

The agent decides ($a_{tent}$) whether to [EXIT] the system, go to [NEXT] page, return to a [PREVIOUS] page, or [CLICK] on an item to access more details. 
エージェントは、システムを[EXIT]するか、[NEXT]ページに進むか、[PREVIOUS]ページに戻るか、またはアイテムを[CLICK]して詳細にアクセスするかを決定します。

If the agent decides to click on an item, the item is displayed with an extended description that replaces the short $item_{description}$, which is $\{ \}$ then used to determine whether it wishes to engage further with the item. 
エージェントがアイテムをクリックすることを決定した場合、そのアイテムは短い$item_{description}$を置き換える拡張された説明と共に表示され、$\{ \}$はそのアイテムにさらに関与したいかどうかを判断するために使用されます。

Finally, if [EXIT] is selected, a satisfaction interview is conducted to gather granular opinions and ratings on the presented recommendations. 
最後に、[EXIT]が選択されると、提示された推薦に関する詳細な意見と評価を収集するための満足度インタビューが実施されます。

To this end, the agent sequentially: 
この目的のために、エージェントは順次：

1) estimates its satisfaction level with preceding recommendations, 
1) 前の推薦に対する満足度を推定します。

2) generates its current fatigue level (Zhang et al., 2023), 
2) 現在の疲労レベルを生成します（Zhang et al., 2023）。

3) infers its current emotion, such as EXCITED, and 
3) 現在の感情を推測します（例：興奮している）。

4) selects the most suitable action. 
4) 最も適切なアクションを選択します。



. Satisfaction level, fatigue, and emotion are dynamic elements that the agent employs to adapt its actionable plan with the recommender system.
満足度、疲労、感情は、エージェントが推薦システムにおける行動計画を適応させるために利用する動的要素です。

**A.5** **Causal Action Refinement**
**A.5** **因果的行動の洗練**
Suboptimal decision-making (e.g., premature exits or misaligned clicks) can arise as the agent struggles to understand the impact of its decision, necessitating iterative adjustments to align with implicit preferences.
最適でない意思決定（例：早期の退出や不適切なクリック）は、エージェントが自らの決定の影響を理解しようと苦労することで生じる可能性があり、暗黙の好みに合わせるための反復的な調整が必要です。

In light of this, we introduce a causal reasoning step which encourages the assistant to actively seek to understand the causal relationships between its decisions and latent user-state dynamics.
この点を踏まえ、私たちは因果推論のステップを導入し、アシスタントが自らの決定と潜在的なユーザステートの動態との因果関係を積極的に理解することを促します。

Assuming the tentative action atent and context H, the LLM generates causal questions Q to validate the rationale behind atent, Q = LLM (atent, H, p, Pcausal), where _Pcausal refers to a predetermined prompt.
仮の行動atentと文脈Hを仮定すると、LLMはatentの背後にある理由を検証するための因果的質問Qを生成します。Q = LLM (atent, H, p, Pcausal)であり、ここで_Pcausalは事前に定められたプロンプトを指します。

Causal_ questions may for example be: Does tiredness re_duce the appeal of this action?, What would happen_ _if you exited the system now?.
因果的質問の例としては、次のようなものがあります：疲労はこの行動の魅力を減少させますか？今システムを退出したらどうなりますか？

For each counter-_ factual, the LLM estimates outcomes such as satisfaction, alignment with persona, and fatigue.
各反事実に対して、LLMは満足度、ペルソナとの整合性、疲労などの結果を推定します。

This includes a scalar sq and textual verdict vq reflecting how cause-effect relationships support or contradict atent.
これには、因果関係がatentを支持または矛盾させる方法を反映するスカラー値sqとテキストの判決vqが含まれます。

Finally, the LLM is queried to adjust the action if the consistency score is low, afinal = _LLM_ (atent, H, p, Paction, Πq∈Q{q, sq, vq}).
最後に、一貫性スコアが低い場合、LLMに行動を調整するように問い合わせます。afinal = _LLM_ (atent, H, p, Paction, Πq∈Q{q, sq, vq})。



## B Pseudo-Code 擬似コード

We present the pseudo-code for SimUSER agent.
SimUSERエージェントの擬似コードを示します。

**Algorithm 1 SimUSER Algorithm**
**アルゴリズム 1 SimUSER アルゴリズム**

1: Input: Historical data Hu for user u  
1: 入力: ユーザuのための履歴データHu  
2: Output: Simulated interactions and feedback  
2: 出力: シミュレーションされたインタラクションとフィードバック  
3: Phase 1: Persona Matching  
3: フェーズ 1: ペルソナマッチング  
4: P ← Generate persona from Hu  
4: P ← Huからペルソナを生成する  
5: p ← Identify best persona ∈ _P using self-_ consistency score  
5: p ← 自己整合性スコアを使用して_Pの中から最適なペルソナを特定する  
6: Phase 2: Simulate Interactions  
6: フェーズ 2: インタラクションのシミュレーション  
7: Initialize memory module from Hu  
7: Huからメモリモジュールを初期化する  
8: repeat  
8: 繰り返す  
9: Perceive the page and items - Generate captions  
9: ページとアイテムを認識する - キャプションを生成する  
10: Retrieve similar items from the KG memory  
10: KGメモリから類似アイテムを取得する  
11: Decide what items to watch  
11: どのアイテムを見るかを決定する  
12: Rate the items and provide feelings  
12: アイテムに評価を付け、感情を提供する  
13: Decide next action a based on satisfaction, fatigue, and emotion  
13: 満足度、疲労、感情に基づいて次のアクションaを決定する  
14: Perform post-interaction reflection  
14: インタラクション後の反省を行う  
15: Update memory module  
15: メモリモジュールを更新する  
16: **if a = [EXIT] then**  
16: **もし a = [EXIT] なら**  
17: **break**  
17: **中断する**  
18: **else**  
18: **さもなければ**  
19: Perform action a  
19: アクションaを実行する  
20: until Maximum number of pages reached  
20: 最大ページ数に達するまで  
21: Return Simulated interactions, metrics, and feedback  
21: シミュレーションされたインタラクション、メトリクス、およびフィードバックを返す  

-----
Figure 3: Comparison of rating distributions between ground-truth and human proxies.  
図3: グラウンドトゥルースと人間の代理の間の評価分布の比較。

Figure 4: Ratings vs feelings on IMDB dataset. Comparison between human (top left) and LLM-empowered agents.  
図4: IMDBデータセットにおける評価と感情の比較。人間（左上）とLLMを活用したエージェントの比較。



## C Additional Experiments C 追加実験

**C.1** **Rating Distribution 評価分布**  
Beyond individual rating alignment, human proxies must replicate real-world behavior at the macro level.  
個々の評価の整合性を超えて、人間の代理者はマクロレベルでの現実の行動を再現する必要があります。  
This implies ensuring that the distribution of ratings generated by the agents aligns closely with the distributions observed in the original dataset.  
これは、エージェントによって生成された評価の分布が、元のデータセットで観察された分布と密接に一致することを保証することを意味します。  
Figure 3 presents the rating distribution from the MovieLens-1M dataset and the ratings generated by the agents.  
図3は、MovieLens-1Mデータセットからの評価分布とエージェントによって生成された評価を示しています。  
These results reveal a high degree of alignment between the simulated and actual rating distributions, with a predominant number of ratings at 4 and a small number of low ratings (1-2).  
これらの結果は、シミュレーションされた評価分布と実際の評価分布の間に高い整合性があることを示しており、評価の大部分が4であり、低評価（1-2）は少数です。  
While Agent4Rec assigns fewer 1-2 ratings than real users, our approach, by retrieving past interactions from the episodic memory, allows agents to contextualize their ratings based on a broader and more consistent understanding of their own preferences.  
Agent4Recは実際のユーザよりも1-2の評価を少なく割り当てますが、私たちのアプローチはエピソード記憶から過去のインタラクションを取得することにより、エージェントが自分の好みをより広範で一貫した理解に基づいて評価を文脈化できるようにします。  

Figure 5: Preference coherence (accept/reject task). ’I’ stands for incoherent; ’C’ stands for coherent (Reddit dataset).  
図5: 好みの整合性（受け入れ/拒否タスク）。 'I'は不整合を、'C'は整合性を示します（Redditデータセット）。  

**C.2** **Alignment: Rating vs Feeling 整合性：評価と感情**  
Expressing aligned reviews and ratings is of primary importance to simulate realistic human proxies.  
整合したレビューと評価を表現することは、現実的な人間の代理者をシミュレートするために非常に重要です。  
Thus, in this section we delve into the alignment between ratings and sentiments.  
したがって、このセクションでは、評価と感情の整合性について掘り下げます。  
In detail, we prompt the agent to assume one has interacted with a certain item, and ask about its rating and feelings on it.  
具体的には、エージェントに特定のアイテムとインタラクションを持ったと仮定させ、その評価と感情について尋ねます。  
Reviews and ratings from IMDB (Maas et al., 2011) are used as ground truth since MovieLens does not contain reviews.  
MovieLensにはレビューが含まれていないため、IMDB（Maas et al., 2011）からのレビューと評価が真実の基準として使用されます。  
After getting a collection of responses, we conduct sentiment-based analysis with PyABSA (Yang et al., 2023).  
回答のコレクションを得た後、PyABSA（Yang et al., 2023）を使用して感情ベースの分析を行います。  
We compare the rating and sentiment distributions of: humans, RecAgent, Agent4Rec, and SimUSER.  
私たちは、人間、RecAgent、Agent4Rec、およびSimUSERの評価と感情の分布を比較します。  
As depicted in Figure 4, our agents generate ratings aligned with their opinions.  
図4に示されているように、私たちのエージェントは自分の意見に沿った評価を生成します。  
For instance, ratings ≥ 4 are typically associated with positive sentiments.  
例えば、評価が≥ 4の場合、通常はポジティブな感情に関連付けられます。  
In contrast, Agent4Rec exhibits a bias towards positive opinions, resulting in more positive feelings about the items, including when generating low ratings.  
対照的に、Agent4Recはポジティブな意見に偏りがあり、低評価を生成する際にもアイテムに対するポジティブな感情が増加します。  
It is noteworthy that SimUSER agents and genuine humans express similar sentiments at a macro level.  
SimUSERエージェントと実際の人間は、マクロレベルで類似の感情を表現することが注目されます。  

**C.3** **Preference Coherence 好みの整合性**  
Under this scenario, we aim to evaluate whether agents prefer positive recommendations based on a query.  
このシナリオでは、エージェントがクエリに基づいてポジティブな推薦を好むかどうかを評価することを目指します。  
Namely, for each request in the Reddit dataset (He et al., 2023), we sample: (1) a comment from this request (positive recommendation) (2) a random comment (negative recommendation).  
具体的には、Redditデータセット（He et al., 2023）の各リクエストについて、(1) このリクエストからのコメント（ポジティブな推薦）と (2) ランダムなコメント（ネガティブな推薦）をサンプリングします。  
The agent is then prompted to decide which items to watch.  
その後、エージェントはどのアイテムを視聴するかを決定するよう促されます。  
Ideally, synthetic users should watch only positive recommendations and decline negative ones.  
理想的には、合成ユーザはポジティブな推薦のみを視聴し、ネガティブなものは拒否すべきです。  
Behavior is incoherent when the simulator accepts a negative recommendation.  
シミュレーターがネガティブな推薦を受け入れると、行動は不整合になります。  
We clearly see in Figure 5 that our agents are overall coherent, but sometimes prefer negative recommendations, its proportion being around 4%.  
図5に示されているように、私たちのエージェントは全体的に整合していますが、時折ネガティブな推薦を好むことがあり、その割合は約4%です。  
Particularly, Agent4Rec agents often accept recommendations that are not aligned with their age and personality.  
特に、Agent4Recエージェントは、自分の年齢や性格に合わない推薦を受け入れることがよくあります。  
To further assess the robustness of our agents  
私たちのエージェントの堅牢性をさらに評価するために  

Figure 6: Preference coherence (accept/reject task). ’I’ stands for incoherent; ’C’ stands for coherent. Results are reported on Tenrec dataset with hard negative items.  
図6: 好みの整合性（受け入れ/拒否タスク）。 'I'は不整合を、'C'は整合性を示します。結果は、ハードネガティブアイテムを含むTenrecデータセットで報告されています。  
Figure 7: Distribution of interaction numbers (top) and average ratings (bottom) for 3 groups of personas. The left column does not use persona module while the right employs a persona module.  
図7: 3つのペルソナグループのインタラクション数（上）と平均評価（下）の分布。左の列はペルソナモジュールを使用せず、右の列はペルソナモジュールを使用しています。  
under more realistic recommendation conditions, we conduct an additional experiment using the Tenrec dataset (Yuan et al., 2022).  
より現実的な推薦条件の下で、Tenrecデータセット（Yuan et al., 2022）を使用して追加の実験を行います。  
Unlike the Reddit dataset, which relies on random negative sampling, Tenrec provides true negative feedback—items that were shown to users but explicitly ignored.  
ランダムなネガティブサンプリングに依存するRedditデータセットとは異なり、Tenrecは真のネガティブフィードバックを提供します—ユーザに表示されたが明示的に無視されたアイテムです。  
This allows us to create harder negative samples, as these unclicked items are likely to be more relevant but still rejected by real users.  
これにより、クリックされなかったアイテムはより関連性が高い可能性があるため、より難しいネガティブサンプルを作成できますが、実際のユーザによって拒否されます。  
Under this setting, hard negatives are items that were exposed to the user but ignored.  
この設定では、ハードネガティブはユーザに表示されたが無視されたアイテムです。  
As expected, the increased difficulty results in a slight drop in coherence across all agents (Figure 6).  
予想通り、難易度の上昇はすべてのエージェントで整合性のわずかな低下をもたらします（図6）。  
SimUSER remains the most consistent but sees a 5% decrease in coherence, while Agent4Rec and RecAgent show larger declines.  
SimUSERは最も一貫性がありますが、整合性が5%低下し、Agent4RecとRecAgentはより大きな低下を示します。  
Notably, Agent4Rec exhibits a stronger bias toward selecting hard negatives, suggesting sensitivity to misleading but plausible recommendations.  
特に、Agent4Recはハードネガティブを選択する傾向が強く、誤解を招くがもっともらしい推薦に対する感受性を示唆しています。  

**C.4** **Impact of Persona on User Behaviors ペルソナがユーザ行動に与える影響**  
In real life, user behaviors are driven by factors beyond mere individual tastes, including personality traits and demographic attributes such as age, and occupation.  
現実の生活では、ユーザの行動は単なる個々の嗜好を超え、性格特性や年齢、職業などの人口統計的属性によっても影響を受けます。  
To account for these factors, we developed a persona module that incorporates these characteristics.  
これらの要因を考慮するために、私たちはこれらの特性を組み込んだペルソナモジュールを開発しました。  
Using the MovieLens dataset, agents were categorized based on their age, occupation (student, office worker, other), and personality traits — categorical features were encoded using one-hot representation, via k-means (k=3).  
MovieLensデータセットを使用して、エージェントは年齢、職業（学生、オフィスワーカー、その他）、および性格特性に基づいて分類されました—カテゴリカル特徴は、k-means（k=3）を介してワンホット表現を使用してエンコードされました。  
We hypothesize that agents with similar preferences may still exhibit distinct behavior patterns due to their unique persona.  
私たちは、類似の嗜好を持つエージェントでも、独自のペルソナにより異なる行動パターンを示す可能性があると仮定します。  
Figure 7 depicts the distribution of interaction numbers and average ratings among agents with different personas.  
図7は、異なるペルソナを持つエージェント間のインタラクション数と平均評価の分布を示しています。  
As shown in the figure, it is evident that agents from different groups demonstrate distinct behaviors, with higher average ratings in groups 2 and 3 than group 1.  
図に示されているように、異なるグループのエージェントは明確に異なる行動を示し、グループ2および3の平均評価はグループ1よりも高いことが明らかです。  
Synthetic users without personas display more homogeneous behaviors.  
ペルソナのない合成ユーザは、より均質な行動を示します。  
Younger users (group 3, avg age=19.6) engage more frequently with the system compared to older users (group 1, avg age=40.2), likely due to higher adaptability and interest in exploring new recommendations, while older users exhibit fewer interactions, possibly from ingrained preferences and less willingness to engage with new content.  
若いユーザ（グループ3、平均年齢=19.6）は、より高い適応性と新しい推薦を探求する興味から、年配のユーザ（グループ1、平均年齢=40.2）と比較してシステムとより頻繁に関与しますが、年配のユーザは、根付いた嗜好や新しいコンテンツに関与する意欲の低さから、インタラクションが少なくなる可能性があります。  

**C.5** **Post-Interaction Interviews インタビュー後の感想**  
A central advantage of LLM-based evaluation is their capacity to generate human-comprehensible explanations.  
LLMベースの評価の中心的な利点は、人間が理解できる説明を生成する能力です。  
Such explanations provide valuable insights that can be employed to refine the recommender system.  
このような説明は、推薦システムを洗練させるために利用できる貴重な洞察を提供します。  
Figure 8 illustrates a postinteraction interview scenario, where the agent rates its experience with the recommender and returns an explanation based on its personal tastes, habits, emotional memory, and interaction history.  
図8は、エージェントが推薦システムとの体験を評価し、自身の嗜好、習慣、感情的記憶、インタラクション履歴に基づいて説明を返すインタビュー後のシナリオを示しています。  
The agent noticed that the recommender system generally aligned well with its tastes, particularly recommending movies suitable for its age and personality.  
エージェントは、推薦システムが一般的に自分の嗜好にうまく合致していることに気づき、特に自分の年齢や性格に適した映画を推薦してくれました。  
However, some factors reduce the overall satisfaction.  
しかし、いくつかの要因が全体的な満足度を低下させます。  
For instance, despite the agent’s preference for sub-genres like neo-noir and psychological thrillers such as “The Sixth Sense” and “Apt Pupil”, the system frequently recommended mainstream blockbusters like “Star Wars: Episode I”, “The Phantom Menace”.  
例えば、エージェントが「シックスセンス」や「アプト・ピューピル」などのネオノワールや心理スリラーのサブジャンルを好むにもかかわらず、システムは頻繁に「スター・ウォーズ エピソード1」や「ファントム・メナス」などのメインストリームの大ヒット作を推薦しました。  
These findings underscore the importance of understanding the nuanced behavior of different recommendation algorithms and their suitability for each group of users.  
これらの発見は、異なる推薦アルゴリズムの微妙な行動を理解し、それぞれのユーザグループに対する適合性を把握することの重要性を強調しています。  

Case Study of Satisfaction Interview 満足度インタビューのケーススタディ  
**Question: How satisfied are you with the recommender system? Please rate your satisfaction on a scale from 1 to 10 and provide an explanation for your rating.**  
**Rating: 7** **Reason: As a 35-year-old film enthusiast with a preference for independent films and documentaries, I found the recommender system fairly effective in suggesting thought-provoking content. It recommended several documentaries and indie films that I enjoyed.**  
**評価: 7** **理由: 35歳の映画愛好家として、独立系映画やドキュメンタリーを好む私は、推薦システムが考えさせられるコンテンツを提案するのにかなり効果的であると感じました。いくつかのドキュメンタリーやインディ映画を推薦してくれました。**  
However, the system often leaned towards mainstream and popular films rather than exploring unique and lesser-known titles.  
しかし、システムはしばしば主流で人気のある映画に偏り、ユニークであまり知られていないタイトルを探求することがありませんでした。  
This tendency occasionally led to less satisfying recommendations, as I value discovering independent, high-quality films.  
この傾向は時折、満足度の低い推薦につながりました。なぜなら、私は独立系の高品質な映画を発見することを重視しているからです。  
Additionally, while the system recognized my interest in dramas and thrillers, it missed specific sub-genres like neo-noir and psychological thrillers that I particularly enjoy.  
さらに、システムは私のドラマやスリラーへの興味を認識していましたが、特に楽しむネオノワールや心理スリラーのような特定のサブジャンルを見逃しました。  
Improving the system’s ability to identify these nuanced preferences could enhance its effectiveness.  
これらの微妙な嗜好を特定するシステムの能力を向上させることで、その効果を高めることができるでしょう。  
Overall, the system shows strengths in general recommendations but would benefit from a better balance between popular and niche films.  
全体として、システムは一般的な推薦において強みを示していますが、人気のある映画とニッチな映画の間でより良いバランスを取ることが求められます。  

Figure 8: One case study of post-exit feeling interview.  
図8: 退出後の感想インタビューのケーススタディ。  
The blue color highlights the user’s satisfaction score.  
青色はユーザの満足度スコアを強調しています。  

**C.6** **Rating Items under Hallucination 幻覚下でのアイテム評価**  
In this section, we specifically target items that are unfamiliar to the LLM, seeking to evaluate the ability of SimUSER to mitigate hallucination through its memory module.  
このセクションでは、LLMにとって不明なアイテムを特定し、SimUSERがそのメモリモジュールを通じて幻覚を軽減する能力を評価します。  
Similarly to Section 4.2, users are asked to rate movies (MovieLens).  
セクション4.2と同様に、ユーザは映画（MovieLens）を評価するよう求められます。  
Nevertheless, we exclusively include items that are detected as unknown to the LLM.  
それでも、LLMにとって未知と見なされるアイテムのみを含めます。  
These items are identified by querying the LLM to classify each movie into one of 18 genres.  
これらのアイテムは、LLMに各映画を18のジャンルのいずれかに分類するように問い合わせることによって特定されます。  
If the LLM’s genre classification matches the actual category $g_i$, it indicates that the LLM is familiar with the item, and such movies are excluded from the experiment.  
LLMのジャンル分類が実際のカテゴリ $g_i$ と一致する場合、LLMがそのアイテムに精通していることを示し、そのような映画は実験から除外されます。  
From Figure 9, it is evident that while the RMSE values for all methods increase under hallucination, the performance degradation of SimUSER is less severe compared to the baselines.  
図9から、すべての手法のRMSE値が幻覚の下で増加する一方で、SimUSERの性能低下はベースラインと比較してそれほど深刻ではないことが明らかです。  
This relative robustness of SimUSER can be attributed to its KG memory, which effectively mitigates the impact of hallucination by leveraging relationships between users/movies/ratings from previous interactions.  
SimUSERのこの相対的な堅牢性は、以前のインタラクションからのユーザ/映画/評価の関係を活用することによって、幻覚の影響を効果的に軽減するKGメモリに起因しています。  
By comparing the unfamiliar movie with these similar, well-known ones, the LLM can anchor its predictions in familiar contexts, reducing the likelihood of hallucinations and leading to more accurate ratings.  
未知の映画をこれらの類似のよく知られた映画と比較することにより、LLMはその予測を馴染みのある文脈に固定し、幻覚の可能性を減少させ、より正確な評価につながります。  

Figure 9: Comparison of RMSE values for original (dark colors) and hallucination-affected (light colors) models for the rating task (MovieLens).  
図9: 評価タスク（MovieLens）における元の（暗い色）および幻覚の影響を受けた（明るい色）モデルのRMSE値の比較。  
Figure 10: Effect on visual cues on rating distribution for different thumbnail types.  
図10: 異なるサムネイルタイプの評価分布に対する視覚的手がかりの影響。  

**C.7** **Thumbnail Quality Effect サムネイル品質の影響**  
Emotions largely shape decision-making in the recommendation domain.  
感情は推薦領域における意思決定を大きく形成します。  
At the center of emotion, images are powerful stimuli that motivate our choices.  
感情の中心において、画像は私たちの選択を促す強力な刺激です。  
In light of this, a question arises: Can SimUSER be useful in assessing the quality of items’ thumbnails?  
これを踏まえて、次の疑問が生じます：SimUSERはアイテムのサムネイルの品質を評価するのに役立つでしょうか？  
To understand the factors influencing ratings, we randomly selected 100 movies from the MovieLens dataset and ask 100 agents whether they want to watch it.  
評価に影響を与える要因を理解するために、MovieLensデータセットからランダムに100本の映画を選び、100人のエージェントに視聴したいかどうかを尋ねます。  



. For each movie, we collected three versions of the thumbnails: 1) the original movie poster, 2) a random screenshot from the movie trailer on YouTube, and 3) the original movie poster distorted with a blue color filter. 
各映画について、3つのバージョンのサムネイルを収集しました：1）オリジナルの映画ポスター、2）YouTubeの映画トレーラーからのランダムなスクリーンショット、3）青色フィルターで歪められたオリジナルの映画ポスターです。

Based on the click rates shown in Figure 10, we notice that high-quality thumbnails — original posters, significantly influence users’ inclination to watch a movie. 
図10に示されているクリック率に基づくと、高品質のサムネイル（オリジナルポスター）が、ユーザの映画視聴の傾向に大きな影響を与えることがわかります。

Specifically, original posters lead to higher engagement compared to random screenshots and color-distorted posters. 
具体的には、オリジナルポスターはランダムなスクリーンショットや色歪みポスターと比較して、より高いエンゲージメントをもたらします。

This result highlights SimUSER’s capability to reflect the quality of item images in decision-making processes,  
この結果は、SimUSERが意思決定プロセスにおいてアイテム画像の品質を反映する能力を持っていることを強調しています。

-----

Figure 11: Heatmap showing the impact of biased recommendations on genre ratings over time — exposure effect. 
図11：時間の経過に伴うバイアスのかかった推薦がジャンル評価に与える影響を示すヒートマップ — エクスポージャー効果。

The genres and their ratings are displayed after 5, 20, and 50 pages scrolled. 
ジャンルとその評価は、5、20、50ページスクロール後に表示されます。

**C.8** **Exposure Effect in Recommendation** 
**C.8** **推薦におけるエクスポージャー効果**

To assess how biased recommendations shape user preferences over time, we introduce a scenario where the RS only recommends two movie categories: action and horror. 
バイアスのかかった推薦が時間の経過とともにユーザの好みをどのように形成するかを評価するために、RSがアクションとホラーの2つの映画カテゴリのみを推薦するシナリオを導入します。

It emulates an exposure effect (Färber et al., 2023), where repeated exposures to a particular stimulus increase an individual’s preference for that stimulus. 
これは、特定の刺激に繰り返しさらされることで、その刺激に対する個人の好みが増加するエクスポージャー効果（Färber et al., 2023）を模倣しています。

In the context of recommender systems, repeated exposure to specific genres could amplify user preferences for those genres. 
レコメンダーシステムの文脈では、特定のジャンルに繰り返しさらされることで、ユーザのそのジャンルに対する好みが強化される可能性があります。

Under this scenario, we record the average movie ratings for each category after 5, 20, and 50 pages scrolled by the agents. 
このシナリオの下で、エージェントが5、20、50ページスクロールした後の各カテゴリの平均映画評価を記録します。

Namely, the 50 agents are prompted to rate 500 randomly selected movies. 
つまり、50人のエージェントが500本のランダムに選ばれた映画を評価するよう促されます。

Figure 11 illustrates a tendency of the agents to rate items of categories that are overrepresented higher during the interactions with the recommender system, particularly after more than 20 pages. 
図11は、エージェントがレコメンダーシステムとのインタラクション中に、過剰に表現されたカテゴリのアイテムを高く評価する傾向を示しています。特に20ページ以上の後に顕著です。

Conversely, categories that differ significantly from action and horror genres generally tend to receive lower average ratings. 
逆に、アクションやホラージャンルとは大きく異なるカテゴリは、一般的に低い平均評価を受ける傾向があります。

Experimental results validate SimUSER’s capability to replicate the exposure effect, although further research and validation are required with alternative datasets. 
実験結果は、SimUSERがエクスポージャー効果を再現する能力を検証しますが、他のデータセットでのさらなる研究と検証が必要です。

**C.9** **User Review Influence** 
**C.9** **ユーザレビューの影響**

User proxies may help researchers in identifying the psychological effect of reviews on human interactions. 
ユーザプロキシは、レビューが人間の相互作用に与える心理的影響を特定するのに役立つかもしれません。

To investigate this effect, we modified the recommendation simulator to display a) the number of reviews, b) one random negative comment, or c) one random positive comment for each item on  
この効果を調査するために、推薦シミュレーターを修正して、各アイテムに対してa）レビューの数、b）ランダムなネガティブコメント1件、またはc）ランダムなポジティブコメント1件を表示するようにしました。

**MF** **MultVAE** **LightGCN** 
**MF** **MultVAE** **LightGCN**

**Condition** _P view_ _P like_ _P view_ _P like_ _P view_ _P like_ 
**条件** _P view_ _P like_ _P view_ _P like_ _P view_ _P like_ 

Origin 0.461 0.443 0.514 0.455 0.557 0.448 
Origin 0.461 0.443 0.514 0.455 0.557 0.448 

+ With # Reviews 0.485 0.491 0.535 0.492 0.570 0.505 
+ レビュー数あり 0.485 0.491 0.535 0.492 0.570 0.505 

+ With Negative 0.413 0.408 0.450 0.435 0.507 0.409 
+ ネガティブあり 0.413 0.408 0.450 0.435 0.507 0.409 

+ With Positive 0.469 0.495 0.549 0.510 0.573 0.444 
+ ポジティブあり 0.469 0.495 0.549 0.510 0.573 0.444 

Table 6: Impact of user reviews on recommender System performance. 
表6：ユーザレビューがレコメンダーシステムのパフォーマンスに与える影響。

nDCG@10 F1-score@10 
nDCG@10 F1スコア@10 

Method Offline SimUSER Offline SimUSER 
手法 オフライン SimUSER オフライン SimUSER 

MF 0.226 0.213 0.165 0.144 
MF 0.226 0.213 0.165 0.144 

MultVAE 0.288 0.278 0.180 0.189 
MultVAE 0.288 0.278 0.180 0.189 

LightGCN **0.423** **0.465** **0.227** **0.255** 
LightGCN **0.423** **0.465** **0.227** **0.255** 

Table 7: nDCG@k (k=10) and F1-score@k (k=10) for three recommender systems, using either offline or SimUSER-generated interactions. 
表7：オフラインまたはSimUSER生成のインタラクションを使用した3つのレコメンダーシステムのnDCG@k（k=10）およびF1スコア@k（k=10）。

the recommendation page. 
推薦ページで。

We report in Table 6 the average viewing ratio P view and ratio of likes P like. 
表6に、平均視聴比率P viewといいねの比率P likeを報告します。

We can see that displaying the number of reviews slightly improves the viewing ratio, especially for items having enough reviews (i.e., more than 20 reviews). 
レビューの数を表示することで、特に十分なレビュー（すなわち20件以上のレビュー）があるアイテムに対して、視聴比率がわずかに改善されることがわかります。

This aligns with humans’ inclination to select popular items in real-life scenarios. 
これは、現実のシナリオにおいて人気のあるアイテムを選択する人間の傾向と一致しています。

On the other, there is no significant difference in P like (t-test p > 0.05). 
一方で、P likeには有意な差はありません（t検定p > 0.05）。

Another observation is that displaying negative reviews has a stronger impact on user behavior than showing positive reviews, with a decrease in both the average viewing ratio and number of likes. 
もう一つの観察は、ネガティブレビューを表示することがポジティブレビューを表示することよりもユーザの行動に強い影響を与え、平均視聴比率といいねの数の両方が減少することです。

One possible explanation is that negative reviews discourage users from watching an item, while positive reviews primarily encourage users who are already inclined to watch it to proceed with their choice. 
一つの可能な説明は、ネガティブレビューがユーザにアイテムを視聴することを思いとどまらせる一方で、ポジティブレビューはすでに視聴する傾向のあるユーザにその選択を進めるように促すということです。

**C.10** **SimUSER vs. Offline Metrics** 
**C.10** **SimUSERとオフラインメトリクスの比較**

We aim to investigate whether SimUSER can reliably estimate traditional metrics such as nDCG@k (k=10) and F1-score@k (k=10) by comparing the results from traditional offline evaluation with those from SimUSER-generated interactions. 
私たちは、SimUSERが伝統的なメトリクス（nDCG@k（k=10）やF1スコア@k（k=10））を信頼性高く推定できるかどうかを、伝統的なオフライン評価の結果とSimUSER生成のインタラクションの結果を比較することで調査することを目指しています。

For this purpose, we evaluate three recommender systems using the MovieLens dataset under identical conditions for both offline and SimUSER-based evaluations. 
この目的のために、MovieLensデータセットを使用して、オフライン評価とSimUSERベースの評価の両方で同一の条件下で3つのレコメンダーシステムを評価します。

Table 7 reports the nDCG@k and F1score@k (k=10) for both evaluation strategies. 
表7は、両方の評価戦略に対するnDCG@kおよびF1スコア@k（k=10）を報告します。

In the SimUSER scenario, interactions are generated by our synthetic users, where liked and disliked items replace the ground-truth interactions from the offline dataset. 
SimUSERシナリオでは、インタラクションは私たちの合成ユーザによって生成され、好まれたアイテムと嫌われたアイテムがオフラインデータセットの真のインタラクションを置き換えます。

Results indicate minimal differences between SimUSER-generated and real-world data, with consistent model rankings across systems. 
結果は、SimUSER生成データと実世界データの間に最小限の差異があることを示しており、システム全体で一貫したモデルランキングが得られています。

These slight differences reflect real-world users being unconstrained by page numbers and interaction frequency. 
これらのわずかな違いは、実世界のユーザがページ数やインタラクション頻度に制約されていないことを反映しています。

These findings demonstrate that SimUSER reliably measures traditional metrics while enabling exploration of system performance across user demographics, website settings (items per page), and recommender system configurations. 
これらの発見は、SimUSERが伝統的なメトリクスを信頼性高く測定し、ユーザの人口統計、ウェブサイト設定（ページあたりのアイテム数）、およびレコメンダーシステムの構成にわたるシステムパフォーマンスの探求を可能にすることを示しています。

**C.11** **Impact of Number of Interactions on** **Rating Performance** 
**C.11** **インタラクション数が評価パフォーマンスに与える影響**

In this experiment, we measure rating prediction performance as a function of interaction history length ∈(5, 10, 20, and 50 interactions). 
この実験では、インタラクション履歴の長さに応じた評価予測パフォーマンスを測定します ∈(5, 10, 20, 50インタラクション)。

While most methods generally benefit from increased context (Figure 12), small fluctuations occur (e.g., AFM on AmazonBook shows a slight rise from 1.28 at 20 interactions to 1.3006 at 50). 
ほとんどの手法は一般的にコンテキストの増加から利益を得ますが（図12）、小さな変動が発生します（例：AmazonBookのAFMは20インタラクションで1.28から50で1.3006にわずかに上昇します）。

SimUSER consistently outperforms all baselines, achieving RMSEs of 0.5020 (MovieLens), 0.5676 (AmazonBook), and 0.5866 (Steam) at 50 interactions. 
SimUSERはすべてのベースラインを一貫して上回り、50インタラクションで0.5020（MovieLens）、0.5676（AmazonBook）、および0.5866（Steam）のRMSEを達成します。

These results confirm that leveraging personabased context yields robust performance improvements, even with limited historical data, and aligns with our main results. 
これらの結果は、パーソナライズされたコンテキストを活用することで、限られた履歴データでも堅牢なパフォーマンス向上が得られることを確認し、私たちの主要な結果と一致しています。

This highlights SimUSER’s ability to utilize past interactions for realistic simulations while remaining believable when modeling _cold-start or few-shot users._ 
これは、SimUSERが過去のインタラクションを利用して現実的なシミュレーションを行う能力を強調し、_コールドスタートや少数ショットユーザ_をモデル化する際に信頼性を保つことを示しています。

**C.12** **Ablation Studies** 
**C.12** **アブレーションスタディ**

**C.12.1** **Impact of the Knowledge-Graph** **Memory on SimUSER** 
**C.12.1** **SimUSERにおける知識グラフメモリの影響**

Here, our focus is on evaluating the impact of incorporating a knowledge-graph memory on the performance. 
ここでは、パフォーマンスに対する知識グラフメモリの組み込みの影響を評価することに焦点を当てています。

Specifically, the goal is to determine whether employing the KG memory, which simulates external influences such as reviews, enhances believability in human proxies. 
具体的には、レビューなどの外部影響をシミュレートするKGメモリを使用することが、人間のプロキシにおける信頼性を高めるかどうかを判断することが目標です。

All models follow the same settings as in Sec 4.2. 
すべてのモデルは、セクション4.2と同じ設定に従います。

Table 8, highlights that leveraging the KG structure significantly reduces both RMSE and MAE across  
表8は、KG構造を活用することで、RMSEとMAEの両方が大幅に減少することを強調しています。

different datasets. 
異なるデータセットで。

This module mirrors how our prior expectations of an item can shape and bias our assessment of it. 
このモジュールは、アイテムに対する私たちの事前の期待が、どのようにその評価を形成し、バイアスをかけるかを反映しています。

**C.12.2** **Persona Matching: Age, Occupation** 
**C.12.2** **ペルソナマッチング：年齢、職業**

We postulate that personas are crucial for capturing the heterogeneity and diversity present in realworld recommender networks. 
私たちは、ペルソナが実世界のレコメンダーネットワークに存在する異質性と多様性を捉えるために重要であると仮定します。

These attributes significantly shape individual behaviors and preferences, which subsequently influence the overall dynamics of the system. 
これらの属性は、個々の行動や好みに大きな影響を与え、その後システム全体のダイナミクスに影響を与えます。

To evaluate the effectiveness of our self-consistent persona-matching technique, we conducted an experiment using the MovieLens1M dataset. 
私たちの自己一貫したペルソナマッチング技術の効果を評価するために、MovieLens1Mデータセットを使用して実験を行いました。

The goal was to predict the age and occupation of users based on their historical data. 
目標は、ユーザの履歴データに基づいて年齢と職業を予測することでした。

This task was formulated as a classification problem. 
このタスクは分類問題として定式化されました。

Our results are summarized in table 9. 
私たちの結果は表9に要約されています。

We observe a high degree of alignment between the predicted and actual user personas, highlighting the effectiveness of Phase 1 in SimUSER. 
予測されたユーザペルソナと実際のユーザペルソナの間に高い一致度が見られ、SimUSERのフェーズ1の効果が強調されます。

Overall, persona matching turns out to be reasonably robust for enriching simulated agents with detailed backgrounds, including domains where explicit demographic data is not readily provided. 
全体として、ペルソナマッチングは、明示的な人口統計データが容易に提供されない領域を含む詳細な背景でシミュレーションエージェントを豊かにするために、かなり堅牢であることがわかります。

**C.12.3** **Persona Matching: Personality** 
**C.12.3** **ペルソナマッチング：性格**

In order to assess the quality of persona matching in predicting personality traits from historical interaction data, we conduct an additional experiment using the Personality 2018 dataset (Nguyen et al., 2018). 
歴史的インタラクションデータから性格特性を予測する際のペルソナマッチングの質を評価するために、Personality 2018データセット（Nguyen et al., 2018）を使用して追加の実験を行います。

The primary objective is to evaluate whether our model could accurately infer users’ Big Five personality traits based solely on users’ watching history. 
主な目的は、私たちのモデルがユーザの視聴履歴のみに基づいて、ユーザのビッグファイブ性格特性を正確に推測できるかどうかを評価することです。

For a fair comparison, the personality traits within the dataset, as well as the predictions, are normalized to a scale ranging from 0 to 1. 
公正な比較のために、データセット内の性格特性と予測は、0から1の範囲に正規化されます。

We report the results for various lengths of movie history ϱ ∈ 10, 20, 50 . 
映画の履歴のさまざまな長さに対する結果を報告します ϱ ∈ 10, 20, 50。

This task is formulated as { } a regression problem. 
このタスクは回帰問題として定式化されます。

Figure 13 summarizes the results, showing that our model achieved an average MAE of 0.155 across all traits. 
図13は結果を要約しており、私たちのモデルがすべての特性に対して平均MAE 0.155を達成したことを示しています。

Besides, the results reveal that using a history length of 50 items reduces the average MAE from 0.279 (10 items) to 0.155, demonstrating that self-consistent persona matching can reasonably predict personality traits of users from their past interactions. 
さらに、結果は、50アイテムの履歴長を使用することで、平均MAEが0.279（10アイテム）から0.155に減少することを示しており、自己一貫したペルソナマッチングがユーザの過去のインタラクションから性格特性を合理的に予測できることを示しています。

**C.12.4** **Choice of Foundation Model** 
**C.12.4** **基盤モデルの選択**

We seek to evaluate the performance of our methodology using various foundation models on the movie rating task. 
私たちは、映画評価タスクにおいてさまざまな基盤モデルを使用して、私たちの方法論のパフォーマンスを評価しようとしています。

Specifically, we compare the results obtained by employing GPT-4o-mini, GPT4o, Mistral-7b Instruct, Llama-3 Instruct, and Phi3-mini as the underlying LLMs 
具体的には、GPT-4o-mini、GPT4o、Mistral-7b Instruct、Llama-3 Instruct、およびPhi3-miniを基盤LLMとして使用して得られた結果を比較します。



. Specifically, we compare the results obtained by employing GPT-4o-mini, GPT4o, Mistral-7b Instruct, Llama-3 Instruct, and Phi3-mini as the underlying LLMs. 
具体的には、GPT-4o-mini、GPT4o、Mistral-7b Instruct、Llama-3 Instruct、およびPhi3-miniを基盤となるLLMとして使用した結果を比較します。
The results, presented in Table 10, demonstrate that the performance of SimUSER is generally robust across different foundation models. 
表10に示す結果は、SimUSERの性能が異なる基盤モデル全体で一般的に堅牢であることを示しています。
While GPT-4o exhibits significantly lower mean RMSE and MAE (t-test _p < 0.05), GPT-4o-mini achieves similar performance but with a lower inference time. 
GPT-4oは平均RMSEおよびMAEが有意に低い（t検定 _p < 0.05）一方で、GPT-4o-miniは同様の性能を達成しますが、推論時間は短くなります。
Mistral7b Instruct also performs reasonably well on the MovieLens dataset. 
Mistral7b InstructもMovieLensデータセットで合理的に良い性能を発揮します。
On the other hand, Llama-3 Instruct and Phi-3-mini, while competitive, show higher errors. 
一方、Llama-3 InstructとPhi-3-miniは競争力がありますが、より高い誤差を示します。

**C.12.5** **Impact of Perception Module**
**C.12.5** **知覚モジュールの影響**
We now investigate the perception module’s impact on agent believability. 
ここでは、知覚モジュールがエージェントの信頼性に与える影響を調査します。
Table 11 shows agents consistently exhibit more realistic behavior with the perception module (♠), likely due to the inclusion of visual details and unique selling points. 
表11は、エージェントが知覚モジュール（♠）を使用することで一貫してより現実的な行動を示すことを示しており、これは視覚的な詳細やユニークなセールスポイントの含有によるものと考えられます。
The believability gain is lower on AmazonBook than other datasets, possibly because users judge books less by covers and more by descriptions. 
信頼性の向上は他のデータセットに比べてAmazonBookでは低く、これはユーザが本を表紙ではなく説明で判断するためかもしれません。
Examining interactions reveals agents with different personas are significantly influenced by emotional tones. 
インタラクションを調査すると、異なるペルソナを持つエージェントが感情的なトーンに大きく影響されることが明らかになります。
For instance, an agent with high openness may be more inclined to select movies with captions that use positive language like “exciting” or “inspiring”. 
例えば、高いオープンネスを持つエージェントは、「エキサイティング」や「インスパイアリング」といったポジティブな言葉を使ったキャプションの映画を選ぶ傾向が強いかもしれません。
While SimUSER (♦) may inherit biases from the LLM’s interpretation of item descriptions, these can be partially mitigated through factual caption information. 
SimUSER（♦）はアイテムの説明に対するLLMの解釈からバイアスを受ける可能性がありますが、これらは事実に基づくキャプション情報によって部分的に軽減されることがあります。
This suggests the perception module contributes to more visually and emotionally driven engagement. 
これは、知覚モジュールがより視覚的かつ感情的に駆動されるエンゲージメントに寄与していることを示唆しています。



## D Discussion 議論

We acknowledge that our method has certain limitations. 
私たちは、私たちの方法にはいくつかの制限があることを認めます。

Observed behaviors are well-aligned with existing theories and common behaviors in the recommendation domain. 
観察された行動は、既存の理論や推薦ドメインにおける一般的な行動とよく一致しています。

Phenomena at micro-level (rating, watching) are manifestations of agent endogenous behaviors. 
マイクロレベル（評価、視聴）での現象は、エージェントの内因的行動の現れです。

But why agents possess these behaviors are unexplored due to the black-box nature of the large language models we adopted. 
しかし、エージェントがなぜこれらの行動を持つのかは、私たちが採用した大規模言語モデルのブラックボックス性のために未探求です。

A potential reason could be that LLMs are trained on a massive corpus that includes texts from various domains. 
潜在的な理由は、LLMがさまざまなドメインのテキストを含む大規模なコーパスで訓練されていることです。

A potential limitation of our approach lies in its reliance on sufficient interaction data to construct detailed user personas. 
私たちのアプローチの潜在的な制限は、詳細なユーザペルソナを構築するために十分なインタラクションデータに依存していることです。

In some scenarios, many users exhibit limited engagement, particularly in cold-start settings where new users have few or no recorded interactions. 
いくつかのシナリオでは、多くのユーザが限られた関与を示し、特に新しいユーザが記録されたインタラクションをほとんど持たないコールドスタート設定ではそうです。

This constraint reduces the effectiveness of our persona module,  
この制約は、私たちのペルソナモジュールの効果を減少させます。

59  
-----

**Methods** **MovieLens** **AmazonBook** **Steam** **RMSE** **MAE** **RMSE** **MAE** **RMSE** **MAE**  
**方法** **MovieLens** **AmazonBook** **Steam** **RMSE** **MAE** **RMSE** **MAE** **RMSE** **MAE**  
GPT-4o-mini 0.5020 0.4465 0.5676 0.4210 0.5866 0.5325  
GPT-4o **0.4739** **0.4167** **0.5532** **0.3998** **0.5549** **0.4823**  
Mistral-7b Instruct 0.5486 0.4874 0.6435 0.4909 0.6407 0.6275  
Llama-3 Instruct 0.5901 0.5812 0.6346 0.4715 0.6453 0.6321  
Phi-3-mini 0.6358 0.5964 0.6789 0.5763 0.7175 0.6935  
Table 10: Performance comparison in rating prediction on MovieLens with different types of foundation LLMs.  
表10: 異なるタイプの基盤LLMを用いたMovieLensにおける評価予測の性能比較。  

**MovieLens** **AmazonBook** **Steam**  
**MovieLens** **AmazonBook** **Steam**  
RecAgent 3.01 ± 0.14 3.14 ± 0.13 2.96 ± 0.17  
RecAgent 3.01 ± 0.14 3.14 ± 0.13 2.96 ± 0.17  
Agent4Rec 3.04 ± 0.12 3.21 ± 0.14 3.09 ± 0.16  
Agent4Rec 3.04 ± 0.12 3.21 ± 0.14 3.09 ± 0.16  
SimUSER (♦) 4.27±0.18 3.94±0.16 3.89±0.20  
SimUSER (♦) 4.27±0.18 3.94±0.16 3.89±0.20  
SimUSER (♠) **4.41±0.16*** **3.99±0.18*** **4.02±0.23***  
SimUSER (♠) **4.41±0.16*** **3.99±0.18*** **4.02±0.23***  
Table 11: Human-likeness score evaluated by GPT-4o for SimUSER without (♦) and with (♠) perception module. Asterisks (*) denote statistically significant improvements when the perception module is activated.  
表11: SimUSERの人間らしさスコアを、知覚モジュールなし（♦）およびあり（♠）でGPT-4oによって評価したもの。アスタリスク（*）は、知覚モジュールが有効なときの統計的に有意な改善を示します。  

as it derives user preferences primarily from past interactions. 
これは、主に過去のインタラクションからユーザの好みを導き出すためです。

To address this issue, a potential alternative is initializing the persona module using predefined user features, such as categorical tags (e.g., "tech-savvy," "frequent traveler"). 
この問題に対処するための潜在的な代替手段は、カテゴリタグ（例: "技術に詳しい"、"頻繁に旅行する"）などの事前定義されたユーザ機能を使用してペルソナモジュールを初期化することです。

LLMs may replicate biases prevalent in social spaces, such as some groups of individuals being underrepresented. 
LLMは、社会的空間で一般的なバイアスを再現する可能性があり、特定のグループの個人が過小評価されることがあります。

This is problematic if it causes designers to then underlook these peoples’ needs when designing a recommender system. 
これは、設計者が推薦システムを設計する際にこれらの人々のニーズを見落とす原因となる場合、問題となります。

In our experiments, we mitigated this risk by ensuring a broad range of personas via diverse potential occupations, age, and personalities. 
私たちの実験では、多様な職業、年齢、性格を通じて広範なペルソナを確保することで、このリスクを軽減しました。

We also measured the discrepancy between identified and real personas. 
私たちは、特定されたペルソナと実際のペルソナとの間の不一致も測定しました。

Our future investigation will focus on analyzing underrepresented user groups, as well as evaluating persona matching on a wider range of domains (e.g., food). 
私たちの今後の調査は、過小評価されたユーザグループの分析や、より広範なドメイン（例: 食品）でのペルソナマッチングの評価に焦点を当てます。

Finally, UX and UI drive our choices and actions in real-world applications. 
最後に、UXとUIは、実世界のアプリケーションにおける私たちの選択と行動を促進します。

Our simulation, on the other hand, does not fully replicate all those intricate factors, which introduces a gap between real life and simulation. 
一方、私たちのシミュレーションは、これらの複雑な要因を完全には再現しておらず、実生活とシミュレーションの間にギャップを生じさせています。

An important future direction is developing an image-based simulator to better capture the complex nature of user experience. 
重要な今後の方向性は、ユーザ体験の複雑な性質をよりよく捉えるための画像ベースのシミュレーターを開発することです。



## E Cost Analysis コスト分析

We report the cost of running SimUSER per 1000 users. 
私たちは、1000ユーザあたりのSimUSERの運用コストを報告します。

Costs may vary slightly due to differences in interaction numbers and LLM outputs, but scale approximately linearly with user count. 
コストは、インタラクション数やLLM出力の違いにより若干の変動があるかもしれませんが、ユーザ数に対してほぼ線形にスケールします。

Our implementation uses OpenAI’s GPT4o-mini. 
私たちの実装は、OpenAIのGPT4o-miniを使用しています。

SimUSER costs approximately $13 ($0.0013/User), while Agent4Rec costs approximately $10 ($0.0010/User). 
SimUSERのコストは約$13（$0.0013/ユーザ）であり、Agent4Recのコストは約$10（$0.0010/ユーザ）です。

The cost difference mainly stems from the integration of images to enable visual-driven reasoning. 
コストの違いは主に、視覚駆動の推論を可能にするための画像の統合に起因しています。



## F Running Time Analysis 実行時間分析

We compare the running time of SimUSER and Agent4Rec for 1,000 user interactions with GPT4o. 
私たちは、1,000のユーザインタラクションに対するSimUSERとAgent4Recの実行時間をGPT4oで比較します。
Without parallelization (♥), Agent4Rec and SimUSER require 9.3h and 10.1h, respectively. 
並列化なし（♥）では、Agent4RecとSimUSERはそれぞれ9.3時間と10.1時間を要します。
With parallelization (♣, max 500 workers), these times drop to 0.53h and 0.59h. 
並列化（♣、最大500ワーカー）を行うと、これらの時間は0.53時間と0.59時間に短縮されます。
This demonstrates that parallelizing LLM calls significantly reduces inference time, allowing the system to scale efficiently.  
これは、LLM呼び出しの並列化が推論時間を大幅に短縮し、システムが効率的にスケールすることを可能にすることを示しています。
