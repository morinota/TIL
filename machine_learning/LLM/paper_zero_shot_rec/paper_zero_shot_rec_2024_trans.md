refs: https://arxiv.org/abs/2305.08845

# Large Language Models are Zero-Shot Rankers for Recommender Systems 大規模言語モデルはレコメンダーシステムのゼロショットランカーである

Recently, large language models(LLMs) (e.g.,GPT-4) have demonstrated impressive general-purpose task-solving abilities, including the potential to approach recommendation tasks.
最近、大規模言語モデル（LLMs）（例：GPT-4）は、推薦タスクにアプローチする可能性を含む、印象的な汎用タスク解決能力を示しています。
Along this line of research, this work aims to investigate the capacity of LLMs that act as the ranking model for recommender systems.
この研究の流れに沿って、本研究はレコメンダーシステムのランキングモデルとして機能するLLMsの能力を調査することを目的としています。
We first formalize the recommendation problem as a conditional ranking task, considering sequential interaction histories as conditions and the items retrieved by other candidate generation models as candidates.
まず、推薦問題を条件付きランキングタスクとして形式化し、逐次的なインタラクション履歴を条件として、他の候補生成モデルによって取得されたアイテムを候補として考慮します。
To solve the ranking task by LLMs, we carefully design the prompting template and conduct extensive experiments on two widely-used datasets.
LLMsによるランキングタスクを解決するために、プロンプトテンプレートを慎重に設計し、広く使用されている2つのデータセットで広範な実験を行います。
We show that LLMs have promising zero-shot ranking abilities but (1) struggle to perceive the order of historical interactions, and (2) can be biased by popularity or item positions in the prompts.
私たちは、LLMsが有望なゼロショットランキング能力を持っていることを示しますが、(1) 歴史的インタラクションの順序を認識するのに苦労し、(2) プロンプト内の人気やアイテムの位置によってバイアスがかかる可能性があることを示します。
We demonstrate that these issues can be alleviated using specially designed prompting and bootstrapping strategies.
これらの問題は、特別に設計されたプロンプトとブートストラッピング戦略を使用することで軽減できることを示します。
Equipped with these insights, zero-shot LLMs can even challenge conventional recommendation models when ranking candidates are retrieved by multiple candidate generators.
これらの洞察を活用することで、ゼロショットLLMsは、複数の候補生成器によって候補が取得される際に、従来の推薦モデルに挑戦することさえ可能です。
The code and processed datasets are available at https://github.com/RUCAIBox/LLMRank.
コードと処理されたデータセットは、https://github.com/RUCAIBox/LLMRank で入手可能です。

<!-- ここまで読んだ! -->

## 1Introduction 1 はじめに

In the literature of recommender systems, most existing models are trained with user behavior data from a specific domain or scenario[49,26,28], suffering from two major issues. 
推薦システムの文献において、既存のモデルのほとんどは特定のドメインまたはシナリオからのユーザ行動データで訓練されており[49,26,28]、2つの主要な問題に悩まされています。
Firstly, it is difficult to capture user preference by solely modeling historical behaviors, e.g., clicked item sequences[28,33,82], limiting the expressive power to model more complicated but explicit user interests (e.g., intentions expressed in natural language). 
第一に、過去の行動、例えばクリックされたアイテムのシーケンス[28,33,82]のみをモデル化することでユーザの好みを捉えることが難しく、より複雑で明示的なユーザの興味（例えば自然言語で表現された意図）をモデル化する表現力が制限されます。
Secondly, these models are essentially “narrow experts”, lacking more comprehensive knowledge in solving complicated recommendation tasks that rely on background or commonsense knowledge[23]. 
第二に、**これらのモデルは本質的に「狭い専門家」**であり、背景知識や常識的知識[23]に依存する複雑な推薦タスクを解決するためのより包括的な知識が欠けています。

<!-- ここまで読んだ! -->

To improve recommendation performance and interactivity, there have been increasing efforts that explore the use of pre-trained language models (PLMs) in recommender systems[21,30,62]. 
推薦性能とインタラクティビティを向上させるために、推薦システムにおける事前学習済み言語モデル（PLMs）の使用を探る努力が増加しています[21,30,62]。
They aim to explicitly capture user preference in natural language[21] or transfer rich world knowledge from text corpora[30,29]. 
これらは、自然言語[21]でユーザの好みを明示的に捉えたり、テキストコーパスから豊富な世界知識を転送したりすることを目的としています[30,29]。
Despite their effectiveness, thoroughly fine-tuning the recommendation models on task-specific data is still a necessity, making it less capable of solving diverse recommendation tasks[30]. 
その効果にもかかわらず、タスク特有のデータに基づいて推薦モデルを徹底的にファインチューニングすることは依然として必要であり、さまざまな推薦タスクを解決する能力が低下します[30]。
More recently, large language models (LLMs) have shown great potential to serve as zero-shot task solvers[64,52]. 
最近では、大規模言語モデル（LLMs）がゼロショットタスクソルバーとしての大きな可能性を示しています[64,52]。
Indeed, there are some preliminary attempts that employ LLMs for solving recommendation tasks[20,59,60,13,40,74]. 
実際、推薦タスクを解決するためにLLMsを利用するいくつかの初期の試みがあります[20,59,60,13,40,74]。
These studies mainly focus on discussing the possibility of building a capable recommender with LLMs. 
これらの研究は主に、LLMsを用いて有能な推薦システムを構築する可能性について議論することに焦点を当てています。
While promising, the insufficient understanding of the new characteristics when making recommendations using LLMs could hinder the development of this new paradigm. 
期待が持てる一方で、LLMsを使用して推薦を行う際の新しい特性に対する理解が不十分であることは、この新しいパラダイムの発展を妨げる可能性があります。

In this paper, we conduct empirical studies to investigate what determines the capacity of LLMs that serve as recommendation models. 
本論文では、推薦モデルとして機能するLLMsの能力を決定する要因を調査するために実証研究を行います。
Typically, recommender systems are developed in a pipeline architecture[10], consisting of candidate generation (retrieving relevant items) and ranking (ranking relevant items at a higher position) procedures. 
通常、推薦システムはパイプラインアーキテクチャ[10]で開発され、候補生成（関連アイテムの取得）とランキング（関連アイテムを高い位置にランク付けする）手順で構成されています。
This work mainly focuses on the ranking stage of recommender systems, since LLMs are more expensive to run on a large-scale candidate set. 
**この研究は主に推薦システムのランキング段階に焦点を当てています。なぜなら、LLMsは大規模な候補セットで実行するのによりコストがかかるからです**。
Further, the ranking performance is sensitive to the retrieved candidate items, which is more suitable to examine the subtle differences in the recommendation abilities of LLMs. 
さらに、ランキング性能は取得された候補アイテムに敏感であり、LLMsの推薦能力の微妙な違いを検証するのにより適しています。

To carry out this study, we first formalize the recommendation process of LLMs as a conditional ranking task. 
この研究を実施するために、まずLLMsの推薦プロセスを条件付きランキングタスクとして形式化します。
Given prompts that include sequential historical interactions as “conditions”, LLMs are instructed to rank a set of “candidates” (e.g., items retrieved by candidate generation models), according to LLM’s intrinsic knowledge. 
**「条件」としてシーケンシャルな過去のインタラクションを含むプロンプトが与えられ、LLMsはLLMの内在的な知識に基づいて「候補」（例えば、候補生成モデルによって取得されたアイテム）のセットをランク付けするよう指示されます**。
Then we conduct control experiments to systematically study the empirical performance of LLMs as rankers by designing specific configurations for “conditions” and “candidates”, respectively. 
次に、「条件」と「候補」に対してそれぞれ特定の構成を設計することにより、LLMsをランカーとしての実証性能を体系的に研究するためのコントロール実験を実施します。
Overall, we attempt to answer the following key questions: 
全体として、以下の重要な質問に答えることを試みます：

- What factors affect the zero-shot ranking performance of LLMs? 
   LLMsのゼロショットランキング性能に影響を与える要因は何ですか？

- What data or knowledge do LLMs rely on for recommendation? 
   LLMsは推薦のためにどのようなデータや知識に依存していますか？

Our empirical experiments are conducted on two public datasets for recommender systems.
私たちの実証実験は、推薦システムのための2つの公開データセットで実施されます。
The results lead to several key findings that potentially shed light on how to develop LLMs as powerful ranking models for recommender systems. 
その結果、LLMsを推薦システムの強力なランキングモデルとして開発する方法に光を当てる可能性のあるいくつかの重要な発見が得られました。
We summarize the key findings as follows: 
私たちは、以下のように重要な発見を要約します：

- LLMs struggle to perceive the order of the given sequential interaction histories. 
   LLMsは与えられたシーケンシャルなインタラクション履歴の順序を認識するのに苦労します。
   By employing specifically designed promptings, LLMs can be triggered to perceive the order, leading to improved ranking performance. 
   特別に設計されたプロンプトを使用することで、LLMsは順序を認識するようにトリガーされ、ランキング性能が向上します。

- LLMs suffer from position bias and popularity bias while ranking, which can be alleviated by bootstrapping or specially designed prompting strategies. 
   LLMsはランキング中に位置バイアスと人気バイアスに悩まされており、ブートストラッピングや特別に設計されたプロンプト戦略によって軽減できます。

- LLMs outperform existing zero-shot recommendation methods, showing promising zero-shot ranking abilities, especially on candidates retrieved by multiple candidate generation models with different practical strategies. 
   LLMsは既存のゼロショット推薦手法を上回り、有望なゼロショットランキング能力を示しています。特に、異なる実用的戦略を持つ複数の候補生成モデルによって取得された候補に対して顕著です。

<!-- ここまで読んだ! -->

## 2General Framework for LLMs as Rankers LLMのランキングモデルとしての一般的なフレームワーク

To investigate the recommendation abilities of LLMs, we first formalize the recommendation process as a conditional ranking task. 
LLMsの推薦能力を調査するために、まず推薦プロセスを条件付きランキングタスクとして形式化します。 
Then, we describe a general framework that adapts LLMs to solve the recommendation task.
次に、LLMsを推薦タスクを解決するために適応させる一般的なフレームワークを説明します。 

<!-- ここまで読んだ! -->

### 2.1 Problem Fromulation 問題の定式化

Given the historical interactions ℋ = {i₁, i₂, …, iₙ} of one user (in chronological order of interaction time) as conditions, the task is to rank the candidate items ℭ = {iⱼ}_{j=1}^{m} such that the items of interest would be ranked at a higher position. 
1人のユーザの過去のインタラクション $H = \{i_{1}, i_{2}, \ldots, i_{n}\}$（インタラクション時間の時系列順）を条件として与えられた場合、タスクは候補アイテム $C = \{i_{j}\}_{j=1}^{m}\$ をランク付けし、関心のあるアイテムがより高い位置にランク付けされるようにすることです。
In practice, the candidate items are usually retrieved by candidate generation models from the whole item set ℐ (m ≪ |ℐ|). 
実際には、候補アイテムは通常、候補生成モデルによって全アイテムセット $I (m << |I|)$ から取得されます。
Further, we assume that each item i is associated with a descriptive text tᵢ. 
さらに、各アイテム $i$ は記述テキスト $t_{i}$ に関連付けられていると仮定します。

<!-- ここまで読んだ! -->

### 2.2　Ranking with LLMs Using Natural Language Instructions　自然言語指示を用いたLLMsによるランキング

We use LLMs as ranking models to solve the above-mentioned task in an instruction-following paradigm[64]. 
私たちは、指示に従うパラダイム[64]で上記のタスクを解決するためにLLMsをランキングモデルとして使用します。
Specifically, for each user, we first construct two natural language patterns that contain sequential interaction histories ℋ (conditions) and retrieved candidate items 𝒞 (candidates), respectively. 
**具体的には、各ユーザについて、まず条件としての逐次的なインタラクション履歴 $H$ と、候補としての取得された候補アイテム $C$ を含む2つの自然言語パターンを構築します**。
Then these patterns are filled into a natural language template T as the final instruction. 
次に、これらのパターンを自然言語テンプレート $T$ に埋め込み、最終的な指示とします。
In this way, LLMs are expected to understand the instructions and output the ranking results as the instruction suggests. 
このようにして、LLMsは指示を理解し、指示が示す通りにランキング結果を出力することが期待されます。
The overall framework of the ranking approach by LLMs is depicted in Figure 1. 
LLMsによるランキングアプローチの全体的なフレームワークは、図1に示されています。
Next, we describe the detailed instruction design in our approach. 
次に、私たちのアプローチにおける詳細な指示設計について説明します。

![]()

#### Sequential historical interactions.  逐次的な歴史的インタラクション。

To investigate whether LLMs can capture user preferences from historical user behaviors, we include sequential historical interactions ℋ into the instructions as inputs of LLMs. 
LLMsが歴史的なユーザ行動からユーザの好みを捉えられるかを調査するために、逐次的な歴史的インタラクション $H$ をLLMsの入力として指示に含めます。
To enable LLMs to be aware of the sequential nature of historical interactions, we propose three ways to construct the instructions: 
LLMsが歴史的インタラクションの逐次的な性質を認識できるように、**指示を構築するための3つの方法**を提案します。

- Sequential prompting: Arrange the historical interactions in chronological order. 
   逐次プロンプティング：歴史的インタラクションを時系列で配置します。
   This way has also been used in prior studies[13]. 
   この方法は以前の研究[13]でも使用されています。
   For example, “I’ve watched the following movies in the past in order: ’0. Multiplicity’, ’1. Jurassic Park’,…normal-…\ldots…”. 
   例えば、「過去に次の映画をこの順番で見ました：’0. Multiplicity’, ’1. Jurassic Park’,…」。

- Recency-focused prompting: In addition to the sequential interaction records, we can add an additional sentence to emphasize the most recent interaction. 
   最近重視のプロンプティング：逐次的なインタラクション記録に加えて、**最も最近のインタラクションを強調するための追加の文を加える**ことができます。
   For example, “I’ve watched the following movies in the past in order: ’0. Multiplicity’, ’1. Jurassic Park’,…normal-…\ldots….Note that my most recently watched movie is Dead Presidents.…normal-…\ldots…”. 
   例えば、「過去に次の映画をこの順番で見ました：’0. Multiplicity’, ’1. Jurassic Park’,…normal-…\ldots…。最近見た映画はDead Presidentsです…normal-…\ldots…」。

- In-context learning (ICL): ICL is a prominent prompting approach for LLMs to solve various tasks[79], where it includes demonstration examples in the prompt. 
  インコンテキスト学習（ICL）：ICLは、LLMsがさまざまなタスクを解決するための重要なプロンプティングアプローチ[79]であり、プロンプトにデモンストレーション例を含みます。
   For the personalized recommendation task, simply introducing examples of other users may introduce noises because users usually have different preferences. 
   パーソナライズされた推薦タスクでは、他のユーザの例を単に導入することは、ユーザが通常異なる好みを持つため、ノイズを引き起こす可能性があります。
   Instead, we introduce demonstration examples by augmenting the input interaction sequence itself. 
   その代わりに、入力インタラクションシーケンス自体を拡張することによってデモンストレーション例を導入します。
   We pair the prefix of the input interaction sequence and the corresponding successor as examples. 
   **入力インタラクションシーケンスの接頭辞と対応する後続を例としてペアにします**。(これは要するにfew-shot learningってことか...!:thinking:)
   For instance, “If I’ve watched the following movies in the past in order: ’0. Multiplicity’, ’1. Jurassic Park’,…normal-…\ldots…, then you should recommend Dead Presidents to me and now that I’ve watched Dead Presidents, then…normal-…\ldots…”.  
   例えば、「もし私が過去に次の映画をこの順番で見たなら：’0. Multiplicity’, ’1. Jurassic Park’,...、あなたはDead Presidentsを私に推薦すべきで、今私がDead Presidentsを見たなら...」。

<!-- ここまで読んだ! -->

#### Retrieved candidate items. 取得された候補アイテム。

Typically, candidate items to be ranked are first retrieved by candidate generation models[10]. 
通常、ランキングされる候補アイテムは、最初に候補生成モデル[10]によって取得されます。
In this work, we consider a relatively small pool for the candidates, and keep 20 candidate items (i.e., $m=20$) for ranking. 
本研究では、候補のために比較的小さなプールを考慮し、**ランキングのために20の候補アイテム（すなわち、$m=20$）を保持**します。
To rank these candidates with LLMs, we arrange the candidate items 𝒞 in a sequential manner. 
これらの候補をLLMsでランキングするために、候補アイテム $C$ を逐次的に配置します。
For example, “Now there are 20 candidate movies that I can watch next: ’0. Sister Act’, ’1. Sunset Blvd’,…normal-…\ldots…”. 
例えば、「**今、私が次に見ることができる20の候補映画があります：’0. Sister Act’, ’1. Sunset Blvd’,...**」。
Note that, following the classic candidate generation approach[10], there is no specific order for candidate items. 
古典的な候補生成アプローチ[10]に従って、**候補アイテムには特定の順序はないことに注意**してください。
As a result, 
その結果、
We generate different orders for the candidate items in the prompts, which enables us to further examine whether the ranking results of LLMs are affected by the arrangement order of candidates, i.e., position bias, and how to alleviate position bias via bootstrapping. 
プロンプト内の候補アイテムの異なる順序を生成することで、LLMsのランキング結果が候補の配置順序、すなわち位置バイアスの影響を受けるかどうか、またブートストラップを通じて位置バイアスを軽減する方法をさらに検討することができます。

#### Ranking with large language models. 大規模言語モデルによるランキング。

Existing studies show that LLMs can follow natural language instructions to solve diverse tasks in a zero-shot setting[64,79]. 
既存の研究は、LLMsがゼロショット設定[64,79]で多様なタスクを解決するために自然言語の指示に従うことができることを示しています。
To rank using LLMs, we infill the patterns above into the instruction template T. 
LLMsを使用してランキングするために、上記のパターンを指示テンプレート $T$ に埋め込みます。
An example instruction template can be given as: “[pattern that contains sequential historical interactions ℋ][pattern that contains retrieved candidate items 𝒞]Please rank these movies by measuring the possibilities that I would like to watch next most, according to my watching history.”. 
例として、指示テンプレートは次のようになります：「[逐次的な歴史的インタラクション $H$ を含むパターン][取得された候補アイテム $C$ を含むパターン]私の視聴履歴に基づいて、次に最も見たい映画の可能性を測定して、これらの映画をランキングしてください。」。

#### Parsing the output of LLMs. LLMsの出力の解析。

Note that the output of LLMs is still in natural language text, and we parse the output with heuristic text-matching methods and ground the recommendation results on the specified item set. 
LLMsの出力は依然として自然言語テキストであることに注意し、ヒューリスティックなテキストマッチング手法を用いて出力を解析し、指定されたアイテムセットに基づいて推薦結果を確定します。
In detail, we can directly perform efficient substring matching algorithms like KMP[35] between the LLM outputs and the text of candidate items. 
具体的には、LLMの出力と候補アイテムのテキストの間で、KMP[35]のような効率的な部分文字列マッチングアルゴリズムを直接実行できます。
We also found that LLMs occasionally generate items that are not present in the candidate set. 
**また、LLMsは時折、候補セットに存在しないアイテムを生成することがあることもわかりました。**
For GPT-3.5, such deviations occur in a mere 3% of cases. 
GPT-3.5の場合、そのような逸脱はわずか3%のケースで発生します。
One can either reprocess the illegal cases or simply treat the out-of-candidate items as incorrect recommendations. 
不正なケースを再処理するか、単に候補外のアイテムを不正確な推薦として扱うことができます。

![table1]()

<!-- ここまで読んだ! -->

## 3 Empirical Studies 実証研究

#### Datasets.

The experiments are conducted on two widely-used public datasets for recommender systems: (1) the movie rating dataset MovieLens-1M [24] (in short, ML-1M) where user ratings are regarded as interactions, and (2) one category from the Amazon Review dataset [46] named Games where reviews are regarded as interactions. 
実験は、推薦システムのための2つの広く使用されている公開データセットで実施されます：(1) ユーザの評価がインタラクションと見なされる映画評価データセット MovieLens-1M [24]（略して ML-1M）、および (2) レビューがインタラクションと見なされる Amazon Review データセット [46] の「Games」というカテゴリです。
We filter out users and items with fewer than five interactions. 
5回未満のインタラクションを持つユーザとアイテムは除外します。
Then we sort the interactions of each user by timestamp, with the oldest interactions first, to construct the corresponding historical interaction sequences. 
次に、各ユーザのインタラクションをタイムスタンプでソートし、最も古いインタラクションを最初にして、対応する歴史的インタラクションシーケンスを構築します。
The movie/product titles are used as the descriptive text of an item. 
**映画/製品のタイトルは、アイテムの説明テキストとして使用**されます。
We use item titles in this study for two reasons: (1) to determine if LLMs can make recommendations based on their intrinsic world knowledge with minimal information provided, and (2) to conserve computational resources. 
この研究では、アイテムタイトルを使用する理由は2つあります：(1) LLMが最小限の情報提供で内在的な世界知識に基づいて推薦を行えるかどうかを判断するため、(2) 計算リソースを節約するためです。
Exploring how LLMs use more extensive textual features for recommendations will be the focus of our future work. 
LLMが推薦のためにより広範なテキスト特徴をどのように使用するかを探ることが、私たちの今後の研究の焦点となります。

#### Evaluation and implementation details. 

Following existing works [33,30], we apply the leave-one-out strategy for evaluation. 
評価と実装の詳細。既存の研究 [33,30] に従い、**(オフライン)評価のために leave-one-out 戦略を適用**します。
For each historical interaction sequence, the last item is used as the ground-truth item in test set. 
各歴史的インタラクションシーケンスに対して、最後のアイテムがテストセットの真のアイテムとして使用されます。
The item before the last one is used in the validation set (used for training baseline methods). 
最後のアイテムの前のアイテムは、検証セット（ベースライン手法のトレーニングに使用）で使用されます。
We adopt the widely used metric NDCG@K (in short, N@K) to evaluate the ranking results over the given $m$ candidates, where $K \leq m$. 
私たちは、与えられた $m$ の候補に対するランキング結果を評価するために、広く使用されている指標 NDCG@K（略して N@K）を採用します。ここで、$K \leq m$ です。
To ease the reproduction of this work, our experiments are conducted using a popular open-source recommendation library RecBole [78]. 
この研究の再現を容易にするために、私たちの実験は人気のあるオープンソース推薦ライブラリ RecBole [78] を使用して実施されます。
The historical interaction sequences are truncated within a length of 50. 
歴史的インタラクションシーケンスは、長さ50以内に切り詰められます。
We evaluate LLM-based methods on all users in ML-1M dataset and randomly sampled 6,000 users for Games dataset by default. 
私たちは、ML-1M データセットのすべてのユーザに対して LLM ベースの手法を評価し、Games データセットのためにデフォルトで 6,000 ユーザをランダムにサンプリングします。
Unless specified, the evaluated LLM is accessed by calling OpenAI’s API gpt-3.5-turbo. 
特に指定がない限り、評価された LLM は OpenAI の API gpt-3.5-turbo を呼び出すことでアクセスされます。
The hyperparameter temperature of calling LLMs is set to 0.2. 
LLM を呼び出す際のハイパーパラメータ温度は 0.2 に設定されています。
All the reported results are the average of at least three repeat runs to reduce the effect of randomness. 
報告されたすべての結果は、ランダム性の影響を減らすために、少なくとも 3 回の繰り返し実行の平均です。

<!-- ここまで読んだ! -->

### 3.1 LLMは連続した歴史的ユーザ行動を含むプロンプトを理解できるか？

In LLM-based methods, historical interactions are naturally arranged in an ordered sequence.  
LLMベースの手法では、歴史的な相互作用は自然に順序付けられたシーケンスに配置されます。
By designing different configurations of ℋ, we aim to examine whether LLMs can leverage these historical user behaviors and perceive the sequential nature for making accurate recommendations.  
$H$ の異なる構成(前述されてた3パターンだっけ?)を設計することで、LLMがこれらの歴史的ユーザ行動を活用し、正確な推薦を行うためにその順序性を認識できるかどうかを検証することを目指します。
LLMs struggle to perceive the order of given historical user behaviors.  
**LLMは与えられた歴史的ユーザ行動の順序を認識するのに苦労**しています。
In this section, we examine whether LLMs can understand prompts with ordered historical interactions and give personalized recommendations.  
このセクションでは、LLMが順序付けられた歴史的相互作用を含むプロンプトを理解し、個別化された推薦を行うことができるかどうかを検討します。
The task is to rank a candidate set of 20 items, containing one ground-truth item and 19 randomly sampled negatives.  
**タスクは、1つの真のアイテムと19のランダムにサンプリングされたネガティブを含む20アイテムの候補セットをランク付けすること**です。
By analyzing historical behaviors, items of interest should be ranked at a higher position.  
歴史的行動を分析することで、関心のあるアイテムはより高い位置にランク付けされるべきです。
We compare the ranking results of three LLM-based methods: 
私たちは、3つのLLMベースの手法のランク付け結果を比較します：
(a) Ours, which ranks as we have described in Section 2.2.  Historical user behaviors are encoded into prompts using the “sequential prompting” strategy.  
(a) 私たちの手法で、これはセクション2.2で説明したようにランク付けされます。歴史的ユーザ行動は「シーケンシャルプロンプティング」戦略を使用してプロンプトにエンコードされます。
(b) Random Order, where the historical user behaviors will be randomly shuffled before being fed to the model, and  
(b) ランダムオーダーでは、歴史的ユーザ行動がモデルに供給される前にランダムにシャッフルされます。
(c) Fake History, where we replace all the items in original historical behaviors with randomly sampled items as fake historical behaviors.  
(c) フェイクヒストリーでは、元の歴史的行動のすべてのアイテムをランダムにサンプリングされたアイテムで置き換え、フェイクの歴史的行動とします。
From Figure 2(a), we can see that Ours has better performance than variants with fake historical behaviors.  
図2(a)から、私たちの手法はフェイクの歴史的行動を持つバリアントよりも優れたパフォーマンスを示していることがわかります。
However, the performance of Ours and Random Order is similar, indicating that LLMs are not sensitive to the order of the given historical user interactions.  
しかし、私たちの手法とランダムオーダーのパフォーマンスは似ており、LLMが与えられた歴史的ユーザ相互作用の順序に敏感でないことを示しています。

![figure2]()

Moreover, in Figure 2(b), we vary the number of latest historical user behaviors (|ℋ|) used for constructing the prompt from 5 to 50.  
さらに、図2(b)では、**プロンプトを構築するために使用される最新の歴史的ユーザ行動の数（|ℋ|）を5から50に変化**させます。
The results show that increasing the number of historical user behaviors does not improve, but rather negatively impacts the ranking performance.  
**結果は、歴史的ユーザ行動の数を増やすことが改善にはつながらず、むしろランク付けパフォーマンスに悪影響を与えることを示しています**。
We speculate that this phenomenon is caused by the fact that LLMs have difficulty understanding the order, but consider all the historical behaviors equally.  
私たちは、この現象がLLMが順序を理解するのに苦労し、すべての歴史的行動を同等に考慮するために起こると推測しています。
Therefore too many historical user behaviors (e.g., |ℋ| = 50) may overwhelm LLMs and lead to a performance drop.  
したがって、あまりにも多くの歴史的ユーザ行動（例：|H| = 50）はLLMを圧倒し、パフォーマンスの低下を引き起こす可能性があります。
In contrast, a relatively small |ℋ| enables LLMs to concentrate on the most recently interacted items, resulting in better recommendation performance.  
**対照的に、比較的小さな|H|はLLMが最も最近相互作用したアイテムに集中できるようにし、より良い推薦パフォーマンスをもたらします**。


**Triggering LLMs to perceive the interaction order.**
相互作用の順序を認識するようにLLMをトリガーする。
Based on the above observations, we find it difficult for LLMs to perceive the order in interaction histories by a default prompting strategy.  
上記の観察に基づいて、私たちはLLMがデフォルトのプロンプティング戦略によって相互作用の歴史における順序を認識するのが難しいことを発見しました。
As a result, we aim to elicit the order-perceiving abilities of LLMs, by proposing two alternative prompting strategies and emphasizing the recently interacted items.  
その結果、私たちはLLMの順序認識能力を引き出すことを目指し、2つの代替プロンプティング戦略を提案し、最近相互作用したアイテムを強調します。
Detailed descriptions of the proposed strategies have been given in Section 2.2.  
提案された戦略の詳細な説明はセクション2.2に記載されています。
In Table 2, we can see that both recency-focused prompting and in-context learning can generally improve the ranking performance of LLMs, though the best strategy may vary on different datasets.  
表2から、最近重視のプロンプティングとインコンテキスト学習の両方が一般的にLLMのランク付けパフォーマンスを改善できることがわかりますが、最良の戦略は異なるデータセットで異なる場合があります。
The above results can be summarized as the following key observation:  
上記の結果は、以下の重要な観察として要約できます：

---

**Observation 1**. LLMs struggle to perceive the order of the given sequential interaction histories.  
観察1. LLMは与えられた連続的な相互作用の歴史の順序を認識するのに苦労しています。
By employing specifically designed promptings, LLMs can be triggered to perceive the order of historical user behaviors, leading to improved ranking performance.  
特別に設計されたプロンプティングを使用することで、LLMは歴史的ユーザ行動の順序を認識するように促され、ランク付けパフォーマンスが向上します。

![table2]()

<!-- ここまで読んだ! -->

### 3.2 LLMはランキング中にバイアスの影響を受けるか？

The biases and debiasing methods in conventional recommender systems have been widely studied[5].  
従来の推薦システムにおけるバイアスとデバイアス手法は広く研究されています[5]。
For LLM-based recommendation models, both the input and output are natural language texts and will inevitably introduce new biases.  
**LLMベースの推薦モデルでは、入力と出力の両方が自然言語テキストであり、必然的に新たなバイアスを導入します**。
In this section, we discuss two kinds of biases that LLM-based recommendation models suffer from.  
このセクションでは、**LLMベースの推薦モデルが直面する2種類のバイアス**について議論します。
We also make discussions on how to alleviate these biases.  
また、これらのバイアスを軽減する方法についても議論します。

#### The order of candidates affects the ranking results of LLMs. 候補の順序は、LLMのランキング結果に影響を与えます。

For conventional ranking methods, the order of retrieved candidates usually will not affect the ranking results[33,28].  
従来のランキング手法では、取得された候補の順序は通常、ランキング結果に影響を与えません[33,28]。
However, for the LLM-based approach that is described in Section 2.2, the candidates are arranged in a sequential manner and infilled into a prompt.  
しかし、セクション2.2で説明されているLLMベースのアプローチでは、候補が順次配置され、プロンプトに埋め込まれます。
It has been shown that LLMs are generally sensitive to the order of examples in the prompts for NLP tasks[80,44].  
**LLMは、NLPタスクのプロンプト内の例の順序に一般的に敏感であること**が示されています[80,44]。
As a result, we also conduct experiments to examine whether the order of candidates affects the ranking performance of LLMs.  
その結果、候補の順序がLLMのランキング性能に影響を与えるかどうかを調べる実験も行います。
We follow the experimental settings adopted in Section 3.1.  
私たちは、セクション3.1で採用された実験設定に従います。
The only difference is that we control the order of these candidates in the prompts, by making the ground-truth items appear at a certain position.  
**唯一の違いは、グラウンドトゥルースアイテムが特定の位置に現れるように、プロンプト内のこれらの候補の順序を制御すること**です。(これはあくまで実験としてってことか...! 実運用ではground-truthは未知なのでこの手法は取れない:thinking:)
We vary the position of ground-truth items at {0,5,10,15,19} and present the results in Figure 3(a).  
グラウンドトゥルースアイテムの位置を{0,5,10,15,19}で変化させ、結果を図3(a)に示します。
We can see that the performance varies when the ground-truth items appear at different positions.  
グラウンドトゥルースアイテムが異なる位置に現れると、パフォーマンスが変化することがわかります。
Especially, the ranking performance drops significantly when the ground-truth items appear at the last few positions.  
**特に、グラウンドトゥルースアイテムが最後の数位置に現れると、ランキング性能が大幅に低下します。**
The results indicate that LLM-based rankers are affected by the order of candidates, i.e., position bias, which may not affect conventional recommendation models.  
結果は、LLMベースのランカーが候補の順序、すなわち位置バイアスの影響を受けることを示しており、これは従来の推薦モデルには影響しない可能性があります。
The order of candidates affects the ranking results of LLMs.  
候補の順序は、LLMのランキング結果に影響を与えます。

#### Alleviating position bias by bootstrapping.  ブートストラップによる位置バイアスの軽減。

A simple strategy to alleviate position bias is to bootstrap the ranking process.  
位置バイアスを軽減するための簡単な戦略は、ランキングプロセスをブートストラップすることです。
We may rank the candidate set repeatedly for $B$ times, with candidates randomly shuffled at each round.  
候補セットを$B$回繰り返しランク付けし、各ラウンドで候補をランダムにシャッフルすることができます。
In this way, one candidate may appear in different positions.  
この方法では、1つの候補が異なる位置に現れる可能性があります。
We then merge the results of each round to derive the final ranking.  
次に、各ラウンドの結果を統合して最終的なランキングを導き出します。
From Figure 3(b), we follow the setting in Section 3.1 and apply the bootstrapping strategy to Ours.  
図3(b)から、私たちはセクション3.1の設定に従い、ブートストラップ戦略を私たちのモデルに適用します。
Each candidate set will be ranked for 3 times.  
各候補セットは3回ランク付けされます。
We can see that bootstrapping improves the ranking performance on both datasets.  
ブートストラッピングが両方のデータセットでランキング性能を向上させることがわかります。

<!-- ここまで読んだ! -->

#### Popularity degrees of candidates affect ranking results of LLMs. 候補の人気度は、LLMのランキング結果に影響を与えます。

For popular items, the associated text may also appear frequently in the pre-training corpora of LLMs.
**人気のあるアイテムの場合、関連するテキストはLLMの事前学習コーパスに頻繁に現れる可能性**があります。
For example, a best-selling book would be widely discussed on the Web.  
例えば、ベストセラーの本はWeb上で広く議論されるでしょう。
Thus, we aim to examine whether the ranking results are affected by the popularity of candidates.  
したがって、ランキング結果が候補の人気によって影響を受けるかどうかを調べることを目指します。
However, it is difficult to directly measure the popularity of item text.  
しかし、アイテムテキストの人気を直接測定することは難しいです。
Here, we hypothesize that the text popularity can be indirectly measured by item frequency in one recommendation dataset.  
ここでは、テキストの人気は1つの推薦データセットにおけるアイテムの頻度によって間接的に測定できると仮定します。
In Figure 3(c), we report the item popularity score (measured by the normalized item frequency of appearance in the training set) at each position of the ranked item lists.  
図3(c)では、ランキングされたアイテムリストの各位置におけるアイテムの人気スコア（トレーニングセットにおける出現頻度の正規化によって測定）を報告します。
We can see that popular items tend to be ranked at higher positions.  
**人気のあるアイテムは、より高い位置にランク付けされる傾向があることがわかります**。

#### Making LLMs focus on historical interactions helps reduce popularity bias. LLMが歴史的なインタラクションに焦点を当てることで、人気バイアスを軽減するのに役立ちます。

We assume that if LLMs focus on historical interactions, they may give more personalized recommendations but not more popular ones.  
LLMが歴史的なインタラクションに焦点を当てる場合、よりパーソナライズされた推薦を行うが、より人気のあるものではないと仮定します。
From Figure 2(b), we know that LLMs make better use of historical interactions when using less historical interactions.  
図2(b)から、LLMは少ない歴史的インタラクションを使用する際に、歴史的インタラクションをより良く活用することがわかります。
From Figure 3(d), we compare the popularity scores of the best-ranked items varying the number of historical interactions.  
図3(d)から、歴史的インタラクションの数を変化させた最も高くランク付けされたアイテムの人気スコアを比較します。
It can be observed that as $|H|$ decreases, the popularity score decreases as well.  
$|H|$が減少するにつれて、人気スコアも減少することが観察できます。
This suggests that one can reduce the effects of popularity bias when LLMs focus more on historical interactions.  
**これは、LLMが歴史的インタラクションにより焦点を当てると、人気バイアスの影響を軽減できることを示唆しています。**
From the above experiments, we can conclude the following:  
上記の実験から、次のことを結論できます：

---

**Observation 2.** LLMs suffer from position bias and popularity bias while ranking, which can be alleviated by bootstrapping or specially designed prompting strategies.  
観察2. LLMはランキング中に位置バイアスと人気バイアスの影響を受け、これはブートストラッピングや特別に設計されたプロンプト戦略によって軽減できます。

<!-- ここまで読んだ! -->

### 3.3 LLMはゼロショット設定で候補をどれだけうまくランク付けできるか？

We further evaluate LLM-based methods on candidates with hard negatives that are retrieved by different strategies to further investigate what the ranking of LLMs depends on.
私たちは、LLMベースの手法を、異なる戦略で取得されたハードネガティブを持つ候補に対してさらに評価し、LLMのランキングが何に依存しているのかを調査します。
Then, we present the ranking performance of different methods on candidates retrieved by multiple candidate generation models to simulate a more practical and difficult setting.
次に、より実践的で困難な設定をシミュレートするために、複数の候補生成モデルによって取得された候補に対する異なる手法のランキング性能を示します。


#### LLMs have promising zero-shot ranking abilities.LLMは有望なゼロショットランキング能力を持っています。

In Table 2, we conduct experiments to compare the ranking abilities of LLM-based methods with existing methods.
表2では、LLMベースの手法のランキング能力を既存の手法と比較する実験を行います。
We follow the same setting in Section 3.1 where $|\mathcal{C}|=20$ and candidate items are randomly retrieved.
私たちは、セクション3.1と同じ設定に従い、$|\mathcal{C}|=20$で候補アイテムがランダムに取得されます。
We include three conventional models that are trained on the training set, i.e., Pop (recommending according to item popularity), BPRMF[49], and SASRec[33].
私たちは、トレーニングセットで訓練された3つの従来のモデル、すなわち、アイテムの人気に基づいて推薦するPop、BPRMF[49]、およびSASRec[33]を含めます。
We also evaluate three zero-shot recommendation methods that are not trained on the target datasets, including BM25[50] (rank according to the textual similarity between candidates and historical interactions), UniSRec[30], and VQ-Rec[29].
また、ターゲットデータセットで訓練されていない3つのゼロショット推薦手法、すなわち、BM25[50]（候補と歴史的インタラクション間のテキスト類似性に基づいてランク付け）、UniSRec[30]、およびVQ-Rec[29]を評価します。
For UniSRec and VQ-Rec, we use their publicly available pre-trained models.
UniSRecとVQ-Recについては、公開されている事前訓練モデルを使用します。
We do not include ZESRec[15] because there is no pre-trained model released.
ZESRec[15]は、リリースされた事前訓練モデルがないため、含めません。
In addition, we compare the zero-shot ranking performance of different LLMs in Table 3.
さらに、表3では、異なるLLMのゼロショットランキング性能を比較します。
“Recency-Focused” prompting strategy is used for LLM-based rankers.
LLMベースのランカーには「最近重視」プロンプティング戦略が使用されます。

From Table 2 and 3, we can see that LLMs with more parameters generally perform better.
**表2と3から、パラメータが多いLLMは一般的により良い性能を発揮することがわかります。**
The best LLM-based methods outperform existing zero-shot recommendation methods by a large margin, showing promising zero-shot ranking abilities.
最良のLLMベースの手法は、既存のゼロショット推薦手法を大きく上回り、有望なゼロショットランキング能力を示しています。
We would highlight that it is difficult to conduct zero-shot recommendations on the ML-1M dataset, due to the difficulty in measuring the similarity between movies merely by the similarity of their titles.
**ML-1Mデータセットでゼロショット推薦を行うことは、映画のタイトルの類似性だけで映画間の類似性を測定することが難しいため、困難であることを強調したいと思います。**
However, LLMs can use their intrinsic knowledge to measure the similarity between movies and make recommendations.
**しかし、LLMはその内在的な知識を使用して映画間の類似性を測定し、推薦を行うことができます。**
We would emphasize that the goal of evaluating zero-shot recommendation methods is not to surpass conventional models.
ゼロショット推薦手法を評価する目的は、従来のモデルを上回ることではないことを強調したいと思います。
The goal is to demonstrate the strong recommendation capabilities of pre-trained base models, which can be further adapted and transferred to downstream scenarios.
目標は、事前訓練されたベースモデルの強力な推薦能力を示すことであり、これらはさらに適応され、下流のシナリオに転送されることができます。

#### LLMs rank candidates based on item popularity, text features as well as user behaviors. LLMはアイテムの人気、テキスト特徴、ユーザーの行動に基づいて候補をランク付けします。

To further investigate how LLMs rank the given candidates, we evaluate LLMs on candidates that are retrieved by different candidate generation methods.
LLMが与えられた候補をどのようにランク付けするかをさらに調査するために、異なる候補生成手法で取得された候補に対してLLMを評価します。
These candidates can be viewed as hard negatives for ground-truth items, which can be used to measure the ranking ability of LLMs for specific categories of items.
これらの候補は、真のアイテムに対するハードネガティブと見なすことができ、特定のカテゴリのアイテムに対するLLMのランキング能力を測定するために使用できます。
We consider two categories of strategies to retrieve the candidates:
**候補を取得するための2つの戦略カテゴリ**を考慮します：

(1) content-based methods like BM25[50] and BERT[14] retrieve candidates based on the text feature similarities, and
**(1) BM25[50]やBERT[14]のようなコンテンツベースの手法は、テキスト特徴の類似性に基づいて候補を取得します**。(今の俺たちじゃん! :thinking:)
(2) interaction-based methods, including Pop, BPRMF[49], GRU4Rec[28], and SASRec[33], retrieve items using neural networks trained on user-item interactions.
(2) Pop、BPRMF[49]、GRU4Rec[28]、およびSASRec[33]を含むインタラクションベースの手法は、ユーザー-アイテムインタラクションで訓練されたニューラルネットワークを使用してアイテムを取得します。(こっちはCFっていうかid-onlyの手法か...!:thinking:)
Given candidates, we compare the ranking performance of the LLM-based model (Ours) and representative methods.
与えられた候補に対して、LLMベースのモデル（私たちのモデル）と代表的な手法のランキング性能を比較します。

From Figure 4, we can see that the ranking performance of the LLM-based method varies on different candidate sets and different datasets.
図4から、LLMベースの手法のランキング性能は、異なる候補セットや異なるデータセットで異なることがわかります。
(1) On ML-1M, LLM-based method cannot rank well on candidate sets that contain popular items (e.g., Pop and BPRMF), indicating the LLM-based method recommend items largely depend on item popularity on ML-1M dataset.
(1) ML-1Mでは、LLMベースの手法は人気アイテムを含む候補セットでうまくランク付けできず（例：PopやBPRMF）、**LLMベースの手法がML-1Mデータセットでアイテムの人気に大きく依存していることを示しています。**
(2) On Games, we can observe that Ours has similar performance both on popular candidates and textual similar candidates, showing that item popularity and text features contribute similarly to the ranking of LLMs.
(2) Gamesでは、私たちのモデルが人気のある候補とテキスト的に類似した候補の両方で同様の性能を示しており、アイテムの人気とテキスト特徴がLLMのランキングに同様に寄与していることがわかります。
(3) On both two datasets, the performance of Ours is affected by hard negatives retrieved by interaction-based candidate generation models, but not as severe as those interaction-based rankers like SASRec.
(3) 両方のデータセットで、私たちのモデルの性能はインタラクションベースの候補生成モデルによって取得されたハードネガティブの影響を受けますが、SASRecのようなインタラクションベースのランカーほど深刻ではありません。
The above results demonstrate that LLM-based methods not only consider one single aspect for ranking, but make use of item popularity, text features, and even user behaviors.
**上記の結果は、LLMベースの手法がランキングのために単一の側面だけでなく、アイテムの人気、テキスト特徴、さらにはユーザーの行動を利用していることを示しています。**
On different datasets, the weights of these three aspects to affect the ranking performance may also vary.
異なるデータセットでは、ランキング性能に影響を与えるこれら3つの側面の重みも異なる場合があります。

#### LLMs can effectively rank candidates retrieved by multiple candidate generation models. LLMは複数の候補生成モデルによって取得された候補を効果的にランク付けできます。

For real-world recommender systems, the items to be ranked are usually retrieved by multiple candidate generation models.
実世界のレコメンダーシステムでは、ランク付けされるアイテムは通常、複数の候補生成モデルによって取得されます。
As a result, we also conduct experiments in a more practical and difficult setting.
そのため、私たちはより実践的で困難な設定で実験を行います。
We use the above-mentioned seven candidate generation models to retrieve items.
上記の7つの候補生成モデルを使用してアイテムを取得します。
The top-3333 best items retrieved by each candidate generation model will be merged into a candidate set containing a total of 21212121 items.
**各候補生成モデルによって取得された上位3のアイテムは、合計21アイテムを含む候補セットに統合されます**。
As a more practical setting, we do not complement the ground-truth item to each candidate set.
より実践的な設定として、各候補セットに真のアイテムを補完しません。
Note that the experiments here were conducted under the implicit preference setup, indicating that implicit positive instances (not explicitly labeled) may exist among the retrieved items.
ここでの実験は、暗黙の好み設定の下で行われたことに注意してください。これは、取得されたアイテムの中に暗黙の正のインスタンス（明示的にラベル付けされていない）が存在する可能性があることを示しています。
A more faithful evaluation might require a human study, which we intend to explore in our future work.
より信頼性の高い評価には人間の研究が必要になるかもしれませんが、これは私たちの今後の研究で探求する予定です。
For Ours, we summarize the experiences gained from Section 3.1 and 3.2.
私たちのモデルについては、セクション3.1と3.2から得られた経験を要約します。
We use the recency-focused prompting strategy to encode $|\mathcal{H}|=5$ sequential historical interactions into prompts and use a bootstrapping strategy to repeatedly rank for 3333 rounds.
私たちは、最近重視のプロンプティング戦略を使用して、$|\mathcal{H}|=5$ の連続した歴史的インタラクションをプロンプトにエンコードし、ブートストラップ戦略を使用して3333ラウンドで繰り返しランク付けします。

![table4]()

From Table 4, we can see that the LLM-based model (Ours) yields the second-best performance over the compared recommendation models on most metrics.
表4から、LLMベースのモデル（私たちのモデル）がほとんどの指標で比較した推薦モデルの中で2番目に良い性能を発揮していることがわかります。
The results show that LLM-based zero-shot ranker even beats the conventional recommendation model Pop and BPRMF that has been trained on the target datasets, further demonstrating the strong zero-shot ranking ability of LLMs.
結果は、LLMベースのゼロショットランカーがターゲットデータセットで訓練された従来の推薦モデルであるPopやBPRMFを上回っており、LLMの強力なゼロショットランキング能力をさらに示しています。
We assume that LLMs can make use of their intrinsic world knowledge to rank the candidates comprehensively considering popularity, text features, and user behaviors.
私たちは、LLMがその内在的な世界知識を利用して、人気、テキスト特徴、ユーザーの行動を考慮しながら候補を包括的にランク付けできると仮定します。
In comparison, existing models (as narrow experts) may lack the ability to rank items in a complicated setting.
比較すると、既存のモデル（狭い専門家として）は、複雑な設定でアイテムをランク付けする能力が欠けている可能性があります。
The above findings can be summarized as:
上記の発見は次のように要約できます：

---

Observation 3. LLMs have promising zero-shot ranking abilities, especially on candidates retrieved by multiple candidate generation models with different practical strategies.
観察3. LLMは有望なゼロショットランキング能力を持っており、特に異なる実践的戦略を持つ複数の候補生成モデルによって取得された候補に対してです。

<!-- ここまで読んだ! -->

## 4Related Work 関連研究

#### Transfer learning for recommender systems. レコメンダーシステムのための転移学習。

As recommender systems are mostly trained on data collected from a single source, people have sought to transfer knowledge from other domains[71,85,45,86,76,83], markets[3,51], or platforms[4,19].  
レコメンダーシステムは主に単一のソースから収集されたデータで訓練されるため、人々は他のドメイン[71,85,45,86,76,83]、市場[3,51]、またはプラットフォーム[4,19]から知識を転送しようとしています。
Typical transfer learning methods for recommender systems rely on anchors, including shared users/items[45,84,69,70,7,8]or representations from a shared space[11,18,38].  
レコメンダーシステムの典型的な転移学習手法は、共有ユーザー/アイテム[45,84,69,70,7,8]や共有空間からの表現[11,18,38]を含むアンカーに依存しています。
However, these anchors are usually sparse among different scenarios, making transferring difficult for recommendations[85].  
しかし、これらのアンカーは通常、異なるシナリオ間でまばらであり、推薦のための転送を困難にします[85]。
More recently, there are studies aiming to transfer knowledge stored in language models by adapting them to recommendation tasks via tuning[1,21,12,53]or prompting[37,75,39].  
最近では、チューニング[1,21,12,53]やプロンプティング[37,75,39]を通じて、言語モデルに保存された知識を推薦タスクに適応させることを目指した研究があります。
In this paper, we conduct zero-shot recommendation experiments to examine the potential to transfer knowledge from LLMs.  
本論文では、**LLMから知識を転送する可能性を検討するために、ゼロショット推薦実験**を実施します。

#### Large language models for recommender systems. レコメンダーシステムのための大規模言語モデル。

The design of recommendation models, especially sequential recommendation models, has been long inspired by the design of language models, from word2vec[2,22,25]to recent neural networks[28,33,82,54].  
推薦モデル、特に逐次推薦モデルの設計は、word2vec[2,22,25]から最近のニューラルネットワーク[28,33,82,54]に至るまで、長い間言語モデルの設計に触発されてきました。
In recent years, with the development of pre-trained language models (PLMs)[14], people have tried to transfer knowledge stored in PLMs to recommendation models, by either representing items using their text features or representing behavior sequences in the format of natural language[21,58,42,16,68].  
**近年、事前学習された言語モデル（PLMs）の発展[14]に伴い、人々はPLMsに保存された知識を推薦モデルに転送しようと試みており、アイテムをテキスト特徴を使用して表現するか、行動シーケンスを自然言語の形式で表現**しています[21,58,42,16,68]。
(なるほど。semanticなアイテム埋め込みを使うことも、言語モデルの知識を推薦モデルに転送する方法の1つと見做せるのか...!:thinking:)
Very recently, large language models (LLMs) have been shown superior language understanding and generation abilities[79,56,47,66,17,6,67].  
ごく最近、大規模言語モデル（LLMs）が優れた言語理解と生成能力を示しています[79,56,47,66,17,6,67]。
Studies have been made to make recommender systems more interactive by integrating LLMs along with conventional recommendation models[20,36,43,59,27,61,65,48]or fine-tuned with specially designed instructions[12,21,1,31,81].  
LLMsを従来の推薦モデルと統合することによって、レコメンダーシステムをよりインタラクティブにするための研究が行われています[20,36,43,59,27,61,65,48]または特別に設計された指示でファインチューニングされています[12,21,1,31,81]。
There are also early explorations showing LLMs have zero-shot recommendation abilities[59,41,13,34,72,60,63,73].  
LLMsがゼロショット推薦能力を持つことを示す初期の探求もあります[59,41,13,34,72,60,63,73]。
Despite being effective to some extent, few works have explored what determines the recommendation performance of LLMs.  
ある程度効果的であるにもかかわらず、LLMsの推薦性能を決定する要因を探求した研究はほとんどありません。

<!-- ここまで読んだ! -->

## 5Conclusion 結論

In this work, we investigated the capacities of LLMs that act as the zero-shot ranking model for recommender systems. 
本研究では、推薦システムのゼロショットランキングモデルとして機能するLLMの能力を調査しました。
To rank with LLMs, we constructed natural language prompts that contain historical interactions, candidates, and instruction templates. 
LLMを使用してランキングを行うために、歴史的なインタラクション、候補、および指示テンプレートを含む自然言語プロンプトを構築しました。
We then propose several specially designed prompting strategies to trigger the ability of LLMs to perceive orders of sequential behaviors. 
次に、LLMが順次行動の順序を認識する能力を引き出すために、特別に設計されたプロンプト戦略をいくつか提案します。
We also introduce bootstrapping and prompting strategies to alleviate the position bias and popularity bias issues that LLM-based ranking models may suffer. 
また、LLMベースのランキングモデルが直面する可能性のある位置バイアスと人気バイアスの問題を軽減するために、ブートストラッピングおよびプロンプト戦略を導入します。
Extensive empirical studies indicate that LLMs have promising zero-shot ranking abilities. 
広範な実証研究は、LLMが有望なゼロショットランキング能力を持っていることを示しています。
The empirical studies demonstrate the strong potential of transferring knowledge from LLMs as powerful recommendation models. 
実証研究は、LLMから強力な推薦モデルとして知識を転送する強い可能性を示しています。
We aim at shedding light on several promising directions to further improve the ranking abilities of LLMs, including 
私たちは、LLMのランキング能力をさらに向上させるためのいくつかの有望な方向性を明らかにすることを目指しています。

(1) better perceiving the order of sequential historical interactions 
（1）順次の歴史的インタラクションの順序をより良く認識すること

and (2) alleviating the position bias and popularity bias. 
（2）位置バイアスと人気バイアスを軽減すること。

For future work, we consider developing technical approaches to solve the above-mentioned key challenges when deploying LLMs as recommendation models. 
今後の研究では、LLMを推薦モデルとして展開する際に、上記の重要な課題を解決するための技術的アプローチを開発することを検討しています。
We also would like to develop LLM-based recommendation models that can be efficiently tuned on downstream user behaviors for effective personalized recommendations. 
また、効果的なパーソナライズされた推薦のために、下流のユーザ行動に対して効率的に調整できるLLMベースの推薦モデルを開発したいと考えています。

<!-- ここまで読んだ! -->

## 6 Limitations 制限事項

In most experiments in this paper, ChatGPT is used as the primary target LLM for evaluation. 
本論文のほとんどの実験では、ChatGPTが評価のための主要なターゲットLLMとして使用されています。
However, being a closed-source commercial service, ChatGPT might integrate additional techniques with its core large language model to improve performance. 
しかし、ChatGPTはクローズドソースの商用サービスであるため、パフォーマンスを向上させるためにコアの大規模言語モデルに追加の技術を統合している可能性があります。
While there are open-source LLMs available, such as LLaMA 2[57] and Mistral[32], they exhibit a notable performance disparity compared to ChatGPT (e.g., LLaMA-2-70B-Chat vs. ChatGPT in Table 3). 
LLaMA 2[57]やMistral[32]などのオープンソースのLLMが利用可能である一方で、これらはChatGPTと比較して顕著なパフォーマンスの差を示しています（例：表3のLLaMA-2-70B-ChatとChatGPT）。
This gap makes it difficult to evaluate the emergent abilities of LLMs on the recommendation tasks using purely open-source models. 
このギャップは、純粋にオープンソースモデルを使用して推薦タスクにおけるLLMの新たな能力を評価することを困難にします。
In addition, we should note that the observations might be biased by specific prompts and datasets. 
さらに、観察結果は特定のプロンプトやデータセットによってバイアスがかかる可能性があることに注意すべきです。

<!-- ここまで読んだ! -->
