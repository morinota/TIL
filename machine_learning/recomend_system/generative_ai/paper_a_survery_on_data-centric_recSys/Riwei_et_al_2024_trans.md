## 0.1. refs: refs：

https://arxiv.org/abs/2401.17878
https://arxiv.org/abs/2401.17878

## 0.2. title タイトル

A Survey on Data-Centric Recommender Systems
データ中心の推薦システムに関する調査

## 0.3. abstract 抄録

Recommender systems (RSs) have become an essential tool for mitigating information overload in a range of real-world applications.
レコメンダーシステム（RS）は、実世界の様々なアプリケーションにおいて、情報過多を緩和するための不可欠なツールとなっている。
Recent trends in RSs have revealed a major paradigm shift, moving the spotlight from model-centric innovations to data-centric efforts (e.g., improving data quality and quantity).
RSの最近の動向は、**モデル中心の革新からデータ中心の取り組み（例えば、データの質と量の改善）へとスポットライトを移し**、大きなパラダイムシフトを明らかにしている。
This evolution has given rise to the concept of data-centric recommender systems (Data-Centric RSs), marking a significant development in the field.
この進化は、data-centric recommender systems（Data-Centric RSs, データ中心型推薦システム）という概念を生み出し、この分野における重要な発展を示している。
This survey provides the first systematic overview of Data-Centric RSs, covering 1) the foundational concepts of recommendation data and Data-Centric RSs; 2) three primary issues of recommendation data; 3) recent research developed to address these issues; and 4) several potential future directions of Data-Centric RSs.
本サーベイでは、1）推薦データとデータ中心型RSの基礎概念、2）推薦データの3つの主要な問題、3）これらの問題に対処するために開発された最近の研究、4）データ中心型RSのいくつかの潜在的な将来の方向性を網羅し、**Deata-Centric RSsの初の体系的な概要**を提供する。

# 1. Introduction はじめに

Recommender systems (RSs) have been widely adopted to alleviate information overload in various real-world applications, such as social media, e-commerce, and online advertising.
レコメンダーシステム（RS）は、ソーシャルメディア、電子商取引、オンライン広告などの様々な実世界アプリケーションにおいて、情報過多を緩和するために広く採用されている。
The past few decades have witnessed the rapid development of recommendation models, evolving from traditional collaborative-filtering-based models Rendle et al.(2009) to more advanced deep-learning-based ones Ge et al.(2023), which have markedly improved the accuracy, diversity, and interpretability of recommendation results Li et al.(2020).
過去数十年間、推薦モデルの急速な発展が目覚ましい。従来の協調フィルタリングベースのモデルRendle et al.(2009)から、より高度なディープラーニングベースのモデルGe et al.(2023)へと進化し、推薦結果の精度、多様性、解釈性が著しく向上している Li et al.(2020)。
(Rendle el al. 2009は explicit ALSのやつだっけ! Ge et al. 2023は何の論文だろうか...?)

However, as recommendation models are growing larger and increasingly complex, as exemplified by the P5 recommendation model Geng et al.(2022) that integrates five recommendation-related tasks into a shared language generation framework, the primary constraint impacting recommendation performance gradually transitions towards recommendation data.
しかし、例えば**5つの推薦関連タスクを共有言語生成フレームワークに統合するP5推薦モデル Geng et al.(2022)** のように、推薦モデルが大きく複雑になるにつれて、**推薦性能に影響を与える主要な制約は徐々に推薦データに移行している**。
(P5推薦モデルは、5つのタスクを学習させたモデルってことかな? もしくは5つのusecaseに対応したモデル??)
Instead of focusing solely on developing even more advanced models, an increasing number of researchers have been advocating for the enhancement of recommendation data, leading to the emergence of the novel concept of data-centric recommender systems (Data-Centric RSs) Zha et al.(2023).
より高度なモデルの開発にのみ焦点を当てるのではなく、推薦データの強化を提唱する研究者が増えており、**データ中心型推薦システム（Data-Centric RSs）という新しい概念が登場**している(Zha et al.(2023))。

The fundamental rationale behind Data-Centric RSs is that data ultimately dictates the upper limits of model capabilities.
**Data-Centric RSsの根本的な理論は、データが最終的にモデルの能力の上限を決定するということ**である。(なるほど...!)
Large and high-quality data constitutes the essential prerequisite for breakthroughs in performance.
大量かつ高品質なデータは、パフォーマンスを飛躍的に向上させるための必須条件である。
For instance, the remarkable advancements of GPT models in natural language processing are mainly originated from the use of huge and high-quality datasets Ouyang et al.(2022).
例えば、自然言語処理におけるGPTモデルの目覚ましい進歩は、主に巨大で高品質なデータセットの使用に由来する (Ouyang et al.2022)。(なるほど...!)
Similarly, in computer vision, convolutional neural networks exhibit performance on par with vision transformers when they have access to web-scale datasets Smith et al.(2023).
同様に、コンピュータビジョンにおいても、ウェブスケール(i.e. めちゃめちゃ大量の?)のデータセットにアクセスできると、畳み込みニューラルネットワークはビジョントランスフォーマーと同等のパフォーマンスを発揮する Smith et al.(2023)。(CVでも同じことが言えるのか...!:thinking:)
For RSs, the implication is clear: the greater the quality Wang et al.(2021a) and/or the quantity Liu et al.(2023) of recommendation data, the more proficiently RSs can characterize user preferences, resulting in recommendations that resonate well with users.
RSにおいては、その意味は明確である：**推薦データの質 Wang et al.(2021a) と/または量 Liu et al.(2023) が大きいほど、RSはユーザの嗜好をより効果的に特徴付けることができ、ユーザによく響く推薦を提供することができる**。(うんうん...!:thinking:)

Despite considerable attention from researchers and a great variety of methods that have been put forth in Data-Centric RSs, to the best of our knowledge, there has been no effort to gather and provide a summary of works in this promising and fast-developing research field.
Data-Centric RSsに関する研究者の多大な関心と、この有望で急速に発展している研究分野において提案されてきた多様な手法にもかかわらず、我々の知る限り、この分野における研究の要約をまとめて提供する取り組みはない。
To fulfill this gap, we conduct a systematic review of the literature on Data-Centric RSs and provide insights from the following four aspects.
このギャップを埋めるために、Data-Centric RSsに関する文献の体系的なレビューを行い、以下の**4つの側面から洞察を提供**する。
We first detail the specifics of data that could be used for recommendation and present the formalization of Data-Centric RSs (Section 2).
まず、推薦に使用できるデータの詳細を述べ、データ中心型RSの形式化を示す（セクション2）。
Next, we identify three key issues in recommendation data, i.e., data incompleteness, data noise, and data bias (Section 3), and categorize the existing literature in accordance with these issues (Section 4).
次に、推薦データにおける3つの主要な問題を特定する(セクション3)。すなわち、data imcompleteness(データの不完全性), data noise(データのノイズ) data bias(データのバイアス)である。そして、これらの問題に従って既存の文献を分類する（セクション4）。
Finally, we spotlight a number of encouraging research directions in Data-Centric RSs (Section 5).
最後に、Data-Centric RSsにおけるいくつかの有望な研究方向に焦点を当てる（セクション5）。

<!-- ここまで読んだ！ -->

# 2. Formulation フォーミュレーション

![figure1]()
Figure 1:Three types of recommendation data.

## 2.1. Recommendation Data 推薦データ

The goal of RSs is to help users discover potential items of interest and then generate personalized recommendations.
RSの目的は、ユーザが興味を持つ可能性のあるアイテムを発見し、その後、パーソナライズされた推薦を生成することである。
To achieve this goal, as shown in Figure 1, we summarize three types of data that can be used in RSs:
この目標を達成するために、図1に示すように、**RSで使用できる3種類のデータ**をまとめる：

- User profiles: User profiles refer to a collection of information and characteristics that describe an individual user.
  ユーザプロフィール： ユーザプロフィールは、個々のユーザを記述する情報と特性のコレクションを指す。
  In the context of recommendation, user profiles typically include demographics, preferences, behavior patterns, and other relevant data that helps define and understand a user’s characteristics, needs, and interests.
  推薦の文脈において、ユーザプロフィールには、通常、人口統計、好み、行動パターン、その他の関連データが含まれ、ユーザの特性、ニーズ、興味を定義し理解するのに役立ちます。

- Item attributes: Item attributes involve the specific details or characteristics that describe an item.
  アイテムの属性： アイテムの属性には、アイテムを記述する特定の詳細や特性が含まれます。
  These details can include color, material, brand, price, and other relevant information that helps identify or categorize the item.
  これらの詳細には、色、素材、ブランド、価格、その他の関連情報が含まれ、アイテムを識別または分類するのに役立ちます。

- User-item interactions: User-item interactions represent users’ actions or involvements with items.
  ユーザとアイテムの相互作用: ユーザとアイテムのインタラクションは、ユーザのアイテムに対するアクションや関与を表す。
  Additional contextual information such as ratings, behaviors, timestamps, and reviews can also be utilized to provide a more comprehensive picture of the interactions between users and items.
  評価、行動(の種類)、タイムスタンプ、レビューなどの追加の文脈情報も利用され、ユーザとアイテムの相互作用のより包括的なイメージを提供するのに役立ちます。

## 2.2. Data-Centric RSs データ中心RS

![figure2]()
Figure 2:Model-Centric RSs v.s. Data-Centric RSs.

As shown in Figure 2, different from Model-Centric RSs which improve recommendation performance by refining models, Data-Centric RSs shift the focus from model to data and emphasize the importance of data enhancement.
図2に示すように、**モデルを改良することで推薦性能を向上させるModel-Centric RSsとは異なり、Data-Centric RSsはモデルからデータに焦点を移し、データの強化の重要性を強調している**。
More specifically, given the recommendation data 𝒟 (e.g., user-item interactions), Data-Centric RSs aim to determine a strategy � , which takes the original data 𝒟 as input and outputs the enhanced data 𝒟 ′ :
より具体的には、データ中心型RSは、推薦データ(例えば、ユーザーとアイテムの相互作用)が与えられると、元のデータ($D$)を入力として受け取り、強化されたデータ($D'$)を出力する戦略を決定することを目指している。

$$
D'= f(D)
\tag{1}
$$

The enhanced data 𝒟 ′ could be used by different recommendation models to further improve their performance.
強化されたデータ $D'$ は、異なる推薦モデルによって使用され、その性能をさらに向上させることができる。
We also attempt to answer the following questions to clarify the definition of Data-Centric RSs:
我々はまた、Data-Centric RSsの定義を明確にするために、以下の質問に答えようと試みる:

### Q1: Are Data-Centric RSs the same as Data-Driven RSs? Q1: データ中心RSはデータ駆動RSと同じですか？

Data-Centric RSs and Data-Driven RSs are fundamentally different, as the latter only emphasize the use of recommendation data to guide the design of recommendation models without modifying the data, which are essentially still Model-Centric RSs Zha et al.(2023).
データ中心RSとデータ駆動RSは基本的に異なる。後者は、データを変更せずに推薦データを使用して推薦モデルの設計をガイドすることを強調するだけであり、本質的にはモデル中心RSである(Zha et al.(2023))。

### Q2: Why Data-Centric RSs are necessary? Q2: なぜデータ中心RSが必要なのか？

The objective of a recommendation model is to fit the recommendation data.
推薦モデルの目的は、推薦データに適合させることである。(なるほど、モデルはそのためのツールといえばそうか...! 推薦システムの目的は違うけど...!)
Without changing the data, Model-Centric RSs may generalize or even amplify errors (e.g., noise or bias) in the data, resulting in suboptimal recommendations Zhang et al.(2023a).
データを変更せずに、モデル中心RSは、データのエラー(ex. ノイズやバイアス)を一般化したり、拡大したりする可能性があり、最適でない推薦をもたらすことがある(Zhang et al.(2023a))。
Therefore, Data-Centric RSs are necessary.
したがって、データ中心のRSが必要となる。

### Q3: Will Data-Centric RSs substitute Model-Centric RSs? Q3: データ中心RSはモデル中心RSの代わりになるのか？

Data-Centric RSs do not diminish the value of Model-Centric RSs.
データ中心RSがモデル中心RSの価値を下げることはありません。
Instead, these two paradigms complement each other to build more effective recommender systems.
むしろ、**これら2つのparadigms(=パラダイム、ものの見方や考え方・認識の枠組み、フレームワーク?)は、より効果的な推薦システムを構築するために互い補完し合う**。(うんうん)
Interestingly, model-centric methods can be used to achieve data-centric goals.
興味深いことに、model-centricな手法は、data-centricな目標を達成するために使用することができる。
For example, diffusion models Liu et al.(2023) can be an effective tool for data augmentation.
例えば、拡散モデルLiu et al.(2023)は、データ補強のための効果的なツールとなり得る。
Data-centric methods can facilitate the improvement of model-centric outcomes.
Data-Centric RSsは、model-centricな成果を向上させるのに役立つことができる。
For instance, high-quality synthesized data could inspire further advancements in model design Sachdeva et al.(2022).
例えば、高品質に合成されたデータは、モデル設計のさらなる進歩を促す可能性がある。(Sacdeva et al. 2022)

# 3. Data Issues データの問題

![figure3]()
Figure 3:Overview of data issues in RSs.

As illustrated in Figure 3, we identify three key issues from which recommendation data may suffer, including data incompleteness, data noise, and data bias.
図3に示すように、推薦データが被る可能性のある問題として、**data incompleteness(データの不完全性)**、**data noise(データのノイズ)**、**data bias(データのバイアス)**の3つの主要な問題を特定する。

## 3.1. Data Incompleteness データの不完全性

The data incompleteness issue refers to the scenarios where data used for making recommendations is inadequate, consequently resulting in information gaps or missing details regarding users or items.
data incompletenessの問題は、推薦を行うために使用されるデータが不十分である場合を指し、その結果、ユーザやアイテムに関する情報の欠如や詳細の不足が生じる。
Specifically, the forms and reasons in which recommendation data can be incomplete include:
具体的には、推薦データが不完全である理由や形態は以下の通り：

- **Missing user profiles**: During the registration or setup process, users may fail to fully complete their profiles.
  ユーザープロファイルの欠落： 登録やセットアップの過程で、ユーザがプロファイルを完全に入力できない場合があります。
  Key information may be omitted as they might bypass certain fields or provide inadequate information Wei et al.(2023).
  特定のフィールドを迂回(=わかる、入力を飛ばすよね!:thinking:)したり、不十分な情報を提供したりすることで、重要な情報が省略される可能性がありますWei et al.(2023)。
  For example, a user may neglect to add age or gender, resulting in a profile that is less informative than it could be.
  たとえば、ユーザが年齢や性別を追加しなかったために、プロフィールの情報量が少なくなってしまうことがあります。

- **Limited item attributes**: Similarly, data regarding item attributes may also be lacking.
  限られたアイテム属性： 同様に、アイテムの属性に関するデータも不足している可能性がある。
  This incompleteness hinders the ability to precisely portray items and capture their distinct characteristics Wu et al.(2020).
  この不完全さが、アイテムを正確に描写し、その独自の特性を捉える能力を妨げることがありますWu et al.(2020)。
  For instance, an online bookshop may only provide basic data about a book such as the title and author, neglecting additional details like genre or publication year that can enhance the recommendation accuracy.
  例えば、オンライン書店は、タイトルや著者などの基本的な書籍データのみを提供し、ジャンルや出版年などの追加情報を無視することがあり、これらの情報は推薦の精度を向上させることができます。

- **Sparse user-item interactions**: RSs can encounter the “cold start” problem when new users join.
  ユーザとアイテムの疎な相互作用： RSは、新しいユーザが参加すると「コールドスタート」問題に遭遇する可能性がある。
  With limited or no historical interactions for these users, providing accurate recommendations becomes challenging Wang et al.(2019).
  このようなユーザの過去のinteractionが限られているか存在しない場合、正確な推薦を提供することは困難になります。Wang et al.(2019)。
  Additionally, users usually do not engage with every item.
  さらに、ユーザは通常、すべてのアイテムと関わるわけではありません。
  For example, in a movie recommender system, a user may only rate a handful of thousands of movies available, leading to an incomplete picture of true preferences.
  例えば、映画推薦システムにおいて、ユーザは利用可能な何千もの映画のうちわずか数本しか評価しないかもしれず、真の嗜好の不完全なイメージをもたらす。

- **Inadequate contextual information**: Contextual information like timestamps, ratings, locations, or user reviews significantly contributes to generating effective recommendations.
  不適切な文脈情報： タイムスタンプ、評価、場所、ユーザレビューなどのコンテキスト情報は、効果的なレコメンデーションの生成に大きく貢献する。(=interactionのsequence的なデータもcontextに含まれるのかな...!:thinking:)
  However, due to privacy issues or constraints in user feedback, the available contextual information may be incomplete or lack details Chae et al.(2019).
  しかし、プライバシーの問題やユーザーフィードバックにおける制約のために、利用可能なコンテキスト情報は不完全であったり、詳細が欠けていたりする場合がある (Chae et al.2019)。(まあratingは中々得られないよね。locationもユーザが位置情報の開示を有効にしてないといけないし...!:thinking:)
  For instance, a user might give a high rating for a hotel visit but does not provide a review that could offer useful insights about his/her preferences for future recommendations.
  例えば、ユーザがホテル訪問に高い評価をつけるかもしれませんが、将来の推薦に役立つ洞察を提供するレビューを提供しないかもしれません。

<!-- ここまで読んだ! -->

## 3.2. Data Noise データ・ノイズ

Data noise arises when a portion of the recommendation data is irrelevant or erroneous, which negatively impacts the quality of recommendations provided.
データノイズは、推薦データの一部に無関係なものや誤りがある場合に発生し、提供される推薦の品質に悪影響を与える。
Noisy recommendation data can appear in several forms:
ノイジーな推薦データは、いくつかの形で現れる:

- **Redundant data**: An abundance of identical data is often the consequence of errors during the data collection process.
  冗長なデータ： 同一データが大量に存在するのは、データ収集過程におけるエラーの結果であることが多い。
  RSs might incorrectly identify and log certain identical item attributes multiple times, such as the same item category appearing repeatedly.
  RSは、同じアイテムカテゴリが繰り返し表示されるなど、特定の同一のアイテム属性を誤って複数回識別して記録するかもしれない。
  Alternatively, it might record a user interacting with the same item multiple times – a shop page refresh mistake, for example.
  あるいは、ショップページの更新ミスなど、ユーザが同じアイテムを何度も操作したことを記録する場合もある。

- Inconsistent data: Inconsistencies in data occur mainly due to human errors, such as users unintentionally clicking or providing incorrect ratings to an item Lin et al.(2023b).
  データの矛盾： データの不整合は主に、ユーザが意図せずにアイテムをクリックしたり、誤った評価を提供したりするなどの人為的なエラーによって発生することが多い(Lin et al.(2023b))。
  Additionally, different data sources, like explicit ratings, implicit signals, and textual reviews, can present conflicting information about a user’s current preferences.
  さらに、明示的な評価、暗黙的なシグナル、テキストレビューなど、**異なるデータソース(=多種のfeedbackデータたち...!)は、ユーザの現在の嗜好について相反する情報を提示する可能性がある**。
  For example, a user might provide a low rating for a product, but the text in his/her review might be generally positive, which creates confusion.
  例えば、あるユーザがある製品に低い評価を付けるかもしれませんが、そのレビューのテキストが一般的に肯定的である場合、混乱が生じるかもしれません。(確かに、これはratingを誤って操作してそう...!:thinking:)

- Spam or fake data: At a more malicious level, RSs can be susceptible to spam or fake data generated by either malicious users or automated bots trying to harm the system.
  スパムまたは偽データ： **より悪質なレベルでは、RSは悪意のあるユーザやシステムを害するために生成された自動化されたボットによるスパムや偽データに対して脆弱である可能性がある**。(なるほど確かに...! 基本的にCFとかだと、自動化されたbotのinteractionデータは除外したほうが良いよな...!:thinking:)
  This undesired data can significantly contaminate the pool of authentic user data and can drastically impact the quality of recommendations, leading to decreased user satisfaction Wu et al.(2023).
  このような望ましくないデータは、**本物のユーザデータのプールを著しく汚染し**、推薦の品質に大きな影響を与え、ユーザの満足度を低下させる可能性がある(Wu et al.(2023))。
  A typical example is “review bombing”, where orchestrated attempts by certain users or bots fill a product’s review section with negative feedback to harm its overall rating, even though the product may be generally well-received by the majority.
  典型的な例が **"review bombing"(レビュー爆撃)**で、特定のユーザやボットによる組織的な試みにより、製品のレビューセクションがnegative feedbackで埋め尽くされ、その製品が一般的に好評であるにもかかわらず、その総合評価を損なうことがある。
  (なるほど...!:thinking:)

## 3.3. Data Bias データの偏り

![figure4]()
Figure 4:An illustration of data bias in RSs.

A significant data bias issue arises when there is a significant distribution shift between the data collected and the real-world data.
重要なデータバイアスの問題は、収集されたデータと実世界のデータとの間に著しい分布シフトがある場合に発生する。
This problem mainly originates from:
この問題は主に以下の点から発生する:

- **Shifts in user preferences**: As illustrated in Figure 4, users’ preferences can change due to shifts in wider environmental factors or their personal circumstances like pregnancy.
  ユーザの嗜好の変化： 図4に示すように、ユーザの嗜好は、より広い環境要因の変化や、妊娠などの個人的な状況の変化によって変化する可能性がある。
  In these scenarios, data collected in the past may no longer provide an accurate representation of the user’s current preferences Wang et al.(2023a).
  **このようなシナリオでは、過去に収集されたデータは、もはやユーザの現在の嗜好を正確に表現していないかもしれない**(Wang et al.(2023a))。(うんうん...!:thinking:)

- **Changes in item popularity**: Similarly, the popularity of certain items or categories is not static and can significantly vary over time.
  アイテム人気の変化： 同様に、特定のアイテムやカテゴリの人気は固定的なものではなく、時間の経過とともに大きく変化する可能性がある。
  Items or trends that were once prevalent may lose their charm and relevance as time passes.
  かつて流行したアイテムやトレンドは、時が経つにつれてその魅力や関連性を失うかもしれない。
  For example, as shown in Figure 4, a certain genre of products like the watch that was the rage a few years ago may not hold the same appeal to the audience in the present day as tastes evolve and new genres emerge Zhang et al.(2023a).
  例えば、図4に示すように、数年前に流行した時計のような特定の製品ジャンルは、味覚が変化し、新しいジャンルが登場するにつれて、現在の観客に同じ魅力を持たないかもしれない(Zhang et al.(2023a))。
  (ニュース推薦で言うところの、例えば今はAI関連のニュースが人気で流行ってるけど、数年後には必ずしもそうではない。その時に今の観測データでユーザの嗜好を捉えようとすると時代遅れな感じになっちゃうよね....!:thinking:)

<!-- ここまで読んだ! -->

# 4. Research Progress 研究の進展

![table1]()
Table 1:Representative works and key techniques used in handling different data issues
データ課題

We organize the existing literature according to the data issues in RSs outlined before.
既存の文献を、先に概説したRSにおけるデータの問題点に従って整理する。
Specific categorization as well as representative works and techniques are shown in Table 1.
具体的な分類と代表的な作品・技術を表1に示す。

## 4.1. Handling Incomplete Data 不完全なデータの処理

The key to handling incomplete data is to fill in the missing information.
不完全なデータを処理するための鍵は、**欠落している情報を補完すること**である。(data augmentation的な?:thinking:)
According to the different forms of incomplete data introduced in Section 3.1, we divide existing methods into two categories: attribute completion and interaction augmentation.
セクション3.1で紹介した不完全なデータの異なる形態に基づいて、既存の方法を**attribute completion(属性の補完)とinteraction augmentation(相互作用の拡張)の2つのカテゴリ**に分ける。

### 4.1.1. Attribute Completion 属性の完成

Let 𝒱 be the set of users and items.
ユーザとアイテムの集合を$V$とする。
In practice, the profiles or attributes of some users or items may not be available.
実際には、一部のユーザやアイテムのプロフィールや属性が利用できない場合があります。
Therefore, the set 𝒱 can be divided into two subsets, i.e., 𝒱 + and 𝒱 − , which denote the attributed set and the no-attribute set, respectively.
したがって、**集合 $V$ は、それぞれ属性付きセット $V^{+}$ と無属性セット $V^{-}$ を示す2つのサブセットに分割できる**。
Let $A = \{a_{v}|v \in V^{+}\}$ denote the input attribute set.
$A = \{a_{v}|v \in V^{+}\}$ として、入力属性セットを示す。
Attribute completion aims to complete the attribute for each no-attribute user or item � ∈ 𝒱 − :
**Attribute completionは、各無属性ユーザorアイテム $v \in V^{-}$ の属性を補完することを目的とする**。

$$
A^{c} = \{a^{c}_{v}|v \in V^{-}\} = f_{ac}(A)
\tag{2}
$$

where � � � denotes the completed attribute of � .
ここで $a^{c}_{v}$ は $v$ の補完された属性を示す。
The enhanced input attribute set 𝒜 ′ is formulated as:
強化された入力属性セット $A'$ は以下のように定式化される:

$$
A' = A \cup A^{c} = \{a_{v}|v \in V^{+}\} \cup \{a^{c}_{v}|v \in V^{-}\}
$$

Existing works on attribute completion mainly rely on utilizing the topological structure of given graphs (e.g., user-item interaction, knowledge graphs, and social networks) Wu et al.(2020); You et al.(2020); Jin et al.(2021); Tu et al.(2022); Zhu et al.(2023); Guo et al.(2023).
**属性補完に関する既存の研究は、主に与えられたグラフ(例: ユーザーとアイテムの相互作用、知識グラフ、ソーシャルネットワーク)のトポロジカル構造を利用**している(Wu et al.(2020); You et al.(2020); Jin et al.(2021); Tu et al.(2022); Zhu et al.(2023); Guo et al.(2023)
For instance, by modeling user-item interactions with respective user or item attributes into an attributed user-item bipartite graph, AGCN Wu et al.(2020) proposes an adaptive graph convolutional network for joint item recommendation and attribute completion, which iteratively performs two steps: graph embedding learning with previously learned attribute values, and attribute update procedure to update the input of graph embedding learning.
例えば、ユーザとアイテムの属性をそれぞれのユーザまたはアイテムの属性とともに属性付きユーザ・アイテム二部グラフにモデル化することで、AGCN Wu et al.(2020)は、属性補完とアイテム推薦を同時に行うための適応的グラフ畳み込みネットワークを提案しており、以前に学習した属性値を用いたグラフ埋め込み学習と、グラフ埋め込み学習の入力を更新する属性更新手順を反復的に実行する。
Moreover, given a knowledge graph, HGNN-AC Jin et al.(2021) leverages the topological relationship between nodes as guidance and completes attributes of no-attribute nodes by weighted aggregation of the attributes of linked attributed nodes.
さらに、HGNN-AC Jin et al.(2021)は、知識グラフが与えられると、ノード間の位相的関係をガイダンスとして活用し、リンクされた属性ノードの属性の重み付き集約によって、無属性ノードの属性を補完する。
AutoAC Zhu et al.(2023) identifies that different attribute completion operations should be taken for different no-attribute nodes and models the attribute completion problem as an automated search problem for the optimal completion operation of each no-attribute node.
AutoAC Zhuら(2023)は、異なる無属性ノードに対して異なる属性補完操作を取るべきであることを特定し、属性補完問題を各無属性ノードの最適補完操作の自動探索問題としてモデル化する。
Instead of focusing on attribute completion accuracy, FairAC Guo et al.(2023) pays attention to the unfairness issue caused by attributes and completes missing attributes fairly.
FairAC Guoら(2023)は、属性の補完精度に注目する代わりに、属性に起因する不公平問題に注目し、欠落した属性を公平に補完する。

Given the extensive knowledge base and powerful reasoning capabilities of large language models (LLMs) Zhao et al.(2023), some recent works have focused on leveraging LLMs to complete missing attributes.
大規模言語モデル（LLM）の広範な知識ベースと強力な推論能力を考慮すると、**Zhaoら(2023)は、いくつかの最近の研究は、欠落した属性を補完するためにLLMを活用することに焦点を当てている**。(なるほど??)
For example, LLMRec Wei et al.(2023) carefully designs some prompts as the inputs of ChatGPT Ouyang et al.(2022) to generate user profiles or item attributes that were not originally part of the dataset.
例えば、LLMRec Weiら(2023)は、元々データセットの一部ではなかったユーザプロファイルやアイテム属性を生成するために、ChatGPT(Ouyangら(2022))の入力としていくつかのプロンプトを慎重に設計している。
An example of designed prompts is as follows:
デザインされたプロンプトの例を以下に示す:

> Provide the inquired information of the given movie.
> 指定された映画の情報を提供する。
> Heart and Souls (1993), Comedy/Fantasy The inquired information is: director, country, language.
> Heart and Souls (1993), コメディ／ファンタジー お問い合わせのあった情報です： 監督, 国, 言語.
> Please output them in form of: director, country, language
> 形式で出力してください： 監督、国、言語

(確かに、LLMで既知のアイテム属性は補完できそう...!:thinking:)

Similar to FairAC, some works [Xu et al., 2023] are exploring the ability of LLMs in generating sensitive user profiles or item attributes and considering the risks it may bring to privacy leakage and unfairness issues.
FairACと同様に、一部の研究[Xu et al., 2023]は、LLMが機密性漏洩や不公平問題にもたらすリスクを考慮し、sensitiveなユーザプロファイルやアイテム属性を生成する能力を探っている。

### 4.1.2. Interaction Augmentation

Let 𝒪 = { ( � , � ) ∣ � , � ∈ 𝒱 } be the set of user-item pair ( � , � ) with observed interactions.
$O = \{(u, i)|u,i \in V\}$ を、観測された相互作用を持つユーザ-アイテムペアの集合とする。
We denote ℛ = { � � , � ∣ ( � , � ) ∈ 𝒪 } as the input interaction set.
$R = \{r_{u,i}|(u,i) \in O\}$ を、入力interaction集合とする。
For inactive users and unpopular items, insufficient observed interactions can lead to inaccurate characterization of user preferences and item features.
非活動的なユーザや人気のないアイテムの場合、観測されたinteractionが不十分であると、ユーザの嗜好やアイテムの特徴が正確に特徴付けされない可能性がある。
Therefore, interaction augmentation aims to augment the interaction information of some specific unobserved user-item pairs ( � , � ) ∉ 𝒪 :
したがって、**interaction augmentationは、特定の観測されていないユーザ-アイテムペア $(u,i) \notin O$ のinteraction情報を拡張することを目的としている**:

$$
R^{A} = \{r^{a}_{u,i}|(u,i) \notin O\} = f_{ia}(R)
\tag{3}
$$

where � � , � � denotes the augmented interaction information of ( � , � ) .
ここで、$r^{a}_{u,i}$ は $(u,i)$ の拡張されたinteraction情報を示す。
The enhanced input interaction set ℛ ′ is:
強化された入力interaction集合 $R'$ は以下のようになる:

$$
R' = R \cup R^{A} = \{r_{u,i}|(u,i) \in O\} \cup \{r^{a}_{u,i}|(u,i) \notin O\}
$$

![figure5]()
Figure 5:Categorization of data denoising methods in RSs.
推薦システムにおけるデータノイズ除去方法の分類。

For implicit information such as like/dislike, the critical focus of interaction augmentation lies in how to choose an interaction.
好き嫌いのような暗黙的な情報の場合、interaction augmentationの重要な焦点は、**どのinteractionを選択するか**にある。(正確には、like/dislikeだとexplicit feedbackだよね。implicit feedbackの場合はdislikeかunknownかが判別できないわけなので...!)
Negative sampling pays attention to how to choose an interaction as dislike Rendle et al.(2009); Zhang et al.(2013); Chen et al.(2017); Ding et al.(2020); Huang et al.(2021); Lai et al.(2023); Shi et al.(2023); Lai et al.(2024).
negative samplingは、dislikeとしてinteractionを選択する方法に注目する (Rendle et al.(2009); Zhang et al.(2013); Chen et al.(2017); Ding et al.(2020); Huang et al.(2021); Lai et al.(2023); Shi et al.(2023); Lai et al.(2024)。)
(=ここでnegative samplingの意味は、negative exampleのサンプリング方法...!:thinking:)
Specifically, negative sampling aims to identify uninteracted items of a user as negative items.
具体的には、ネガティブサンプリングは、ユーザの未インタラクションアイテムをネガティブアイテムとして特定することを目指している。
The simplest and most prevalent idea is to randomly select uninteracted items, BPR Rendle et al.(2009) is a well-known instantiation of this idea.
**最も単純で一般的なアイデアは、ランダムに未インタラクションのアイテムを選択すること**であり、BPR(Rendle et al.(2009))は、このアイデアのよく知られた具体例である。
Inspired by the word-frequency-based negative sampling distribution for network embedding Mikolov et al.(2013), NNCF Chen et al.(2017) adopts an item-popularity-based sampling distribution to select more popular items as negative.
ネットワーク埋め込みのための単語頻度ベースのネガティブサンプリング分布に触発されて(Mikolov et al.(2013))、NNCF Chen et al.(2017)は、**アイテムの人気度に基づいたサンプリング分布を採用し、より人気のあるアイテムをネガティブとして選択する**。(うんうん、一般的)
DNS Zhang et al.(2013) proposes to select uninteracted items with higher prediction scores (e.g., the inner product of a user embedding and an item embedding).
DNS Zhang et al.(2013)は、より高い予測スコア（例えば、ユーザ埋め込みとアイテム埋め込みの内積）を持つ未インタラクションのアイテムを選択することを提案している。(うんうん、想像できる...!)
Such hard negative items can provide more informative training signals so that user interests can be better characterized.
このようなハードネガティブなアイテムは、より情報量の多いトレーニングシグナルを提供し、ユーザの興味をよりよく特徴付けることができる。(hard negativeは、確か予測が難しいnegative exampleのことだっけ...!:thinking:)
SRNS Ding et al.(2020) oversamples items with both high predicted scores and high variances during training to tackle the false negative problem.
SRNS Ding et al.(2020)は、偽陰性の問題に対処するために、学習中に予測得点と分散の両方が高いアイテムをオーバーサンプリングする。
DENS Lai et al.(2023) points out the importance of disentangling item factors in negative sampling and designs a factor-aware sampling strategy to identify the best negative item.
DENS Lai et al.(2023)は、ネガティブサンプリングにおけるアイテムfactorの分離の重要性を指摘し、最適なネガティブアイテムを特定するための**factor-awareサンプリング戦略**を設計している。(ここでfactorって、アイテムの特徴量のこと??:thinking:)
MixGCF Huang et al.(2021) synthesizes harder negative items by mixing information from positive items while AHNS Lai et al.(2024) proposes to adaptively select negative items with different hardness levels.
MixGCF Huangら(2021)は、ポジティブアイテムから情報を混ぜ合わせてより難しいネガティブアイテムを合成し、AHNS Laiら(2024)は、異なる難易度レベルのネガティブアイテムを適応的に選択することを提案している。

Different from negative sampling, positive augmentation focuses on how to choose an interaction as like Wang et al.(2019, 2021b); Yang et al.(2021); Zhang et al.(2021a); Lai et al.(2022); Liu et al.(2023); Wei et al.(2023).
**negative samplingとは異なり、positive augmentationは、likeとしてinteractionを選択する方法に焦点を当てている**(Wang et al.(2019, 2021b); Yang et al.(2021); Zhang et al.(2021a); Lai et al.(2022); Liu et al.(2023); Wei et al.(2023))。
(positiveデータを拡張する必要あるの??それってもはや嗜好の予測そのものでは??)
For example, EGLN Yang et al.(2021) selects uninteracted items with higher prediction scores and labels them as positive to enrich users’ interactions.
例えば、EGLN Yangら(2021)は、ユーザのインタラクションを豊かにするために、より高い予測スコアを持つ未インタラクションのアイテムを選択し、それらを正としてラベル付けする。
CASR Wang et al.(2021b) leverages counterfactual reasoning to generate user interaction sequences in the counterfactual world.
CASR Wangら(2021b)は、反実仮想的推論を活用して、反実仮想的世界におけるユーザとのインタラクションシーケンスを生成する。
MNR-GCF Lai et al.(2022) constructs heterogeneous information networks and fully exploits the contextual information therein to identify potential user-item interactions.
MNR-GCF Lai et al.(2022)は、異種情報ネットワークを構築し、そこに含まれるコンテキスト情報を完全に利用して、潜在的なユーザーとアイテムの相互作用を特定する。
Based on generative adversarial nets (GANs), AugCF Wang et al.(2019) generates high-quality augmented interactions that mimic the distribution of original interactions.
生成的敵対ネット（GAN）に基づくAugCF Wangら(2019)は、元の相互作用の分布を模倣した高品質の増強相互作用を生成する。
Inspired by the superior performance of diffusion models in image generation, DiffuASR Liu et al.(2023) adapts diffusion models to user interaction sequence generation, and a sequential U-Net is designed to capture the sequence information and predict the added noise of generated interactions.
画像生成における拡散モデルの優れた性能に触発され、DiffuASR Liuら(2023)は拡散モデルをユーザーインタラクションシーケンス生成に適応させ、シーケンス情報を捕捉し、生成されたインタラクションの付加ノイズを予測するために逐次U-Netを設計した。
Leveraging the capabilities of LLMs, LLMRec Wei et al.(2023) also seeks to identify both positive and negative interactions from a candidate set using well-designed prompts.
LLMRec Wei et al.(2023)は、LLMの能力を活用し、適切に設計されたプロンプトを使用して、候補セットから肯定的なインタラクションと否定的なインタラクションの両方を識別しようとしている。

<!-- positive augumentationのセクションはあんまり読んでない...! -->

For contextual information like rating, the critical focus of interaction augmentation shifts to how to infer the missing value Ren et al.(2012, 2013); Yoon et al.(2018); Chae et al.(2019); Li et al.(2019); Chae et al.(2020); Hwang and Chae (2022).
**ratingのような文脈情報の場合、interaction augmentationの重要な焦点は、欠落している値をどのように推測するか**に移る(Ren et al.(2012, 2013); Yoon et al.(2018); Chae et al.(2019); Li et al.(2019); Chae et al.(2020); Hwang and Chae (2022))。
(これももはや嗜好の予測そのものじゃない...??)
For instance, AutAI Ren et al.(2012) and AdaM Ren et al.(2013) calculate missing ratings according to heuristic similarity-based metrics, such as Pearson correlation coefficient or cosine similarity.
例えば、AutAI Renら(2012)やAdaM Renら(2013)は、ピアソン相関係数やコサイン類似度のような発見的類似度ベースのメトリクスに従って、欠落した評価を計算している。
RAGAN Chae et al.(2019) and UA-MI Hwang and Chae (2022) leverage GANs for rating augmentation.
RAGAN Chae et al.(2019)とUA-MI Hwang and Chae(2022)は、視聴率補強のためにGANを活用している。
Instead of augmenting ratings of interactions between real users and items, AR-CF Chae et al.(2020) proposes to generate virtual users and items and then adopts GANs to predict ratings between them.
AR-CF Chae et al.(2020)は、現実のユーザーとアイテム間の相互作用の評価を補強する代わりに、**仮想のユーザとアイテムを生成し**(??)、それらの間の評価を予測するためにGANを採用することを提案している。

<!-- ここまで雑に読んだ! -->

### 4.1.3. Discussion ディスカッション

While a variety of methods exist for addressing the incomplete data issue, the fact remains that no single method is capable of comprehensively addressing all scenarios involving missing data.
不完全データ問題に対処するための様々な方法が存在する一方で、データの欠落を含むすべてのシナリオに包括的に対処できる単一の方法は存在しないという事実に変わりはない。
Consequently, a considerable amount of time and effort must be devoted to identifying missing information and selecting enhancement strategies.
その結果、不足している情報を特定し、強化戦略を選択するために、かなりの時間と労力を割かなければならない。
Furthermore, evaluating the quality of enhanced data is not straightforward – improvements in RSs might be misleadingly attributed to the simple expansion of data volume, which can cloud the actual effects of refinements in data quality.
**さらに、強化されたデータの質を評価するのは簡単ではない**(うんうん...!)。RSの改善は、単純なデータ量の拡大によるものと誤解される可能性があり、データの質の向上による実際の効果を曇らせる可能性がある。

<!-- ここまで読んだ! -->

## 4.2. Handling Noisy Data ノイズデータの処理

The key to handling the data noise issue is to filter out the noisy information.
データのノイズ問題に対処する鍵は、ノイズとなる情報をフィルタリングすることだ。
According to the varying severity of noisy data presented in Section 3.2, we divide existing denoising methods into three categories: reweighting-based methods, selection-based methods, and dataset distillation/condensation, which are illustrated in Figure 5.
セクション3.2で示したノイズの多いデータの深刻度の違いにより、既存のノイズ除去法を3つのカテゴリーに分類する： 重み付けに基づく方法、選択に基づく方法、データセットの蒸留／凝縮である。

### 4.2.1. Reweighting-Based Denoising リワイティングに基づくノイズ除去

The reweighting-based method aims to assign lower weights to the noisy data (or assign higher weights to the noiseless data) Wang et al.(2021a); Gao et al.(2022); Zhou et al.(2022); Zhang et al.(2023d); Ge et al.(2023); Wang et al.(2023c).
再重み付けに基づく方法は、ノイズのあるデータにより低い重みを割り当てる（またはノイズのないデータにより高い重みを割り当てる）ことを目的としている。
Wang et al.Wang et al.(2021a) experimentally observe that noisy interactions are harder to fit in the early training stages, and, based on this observation, they regard the interactions with large loss values as noise and propose an adaptive denoising training strategy called R-CE, which assigns different weights to noisy interactions according to their loss values during training.
Wang et al.Wangら(2021a)は、ノイズの多い相互作用は学習初期に適合しにくいことを実験的に観察し、この観察に基づいて、損失値の大きい相互作用をノイズとみなし、学習中に損失値に応じてノイズの多い相互作用に異なる重みを割り当てるR-CEと呼ばれる適応的ノイズ除去学習戦略を提案している。
SLED Zhang et al.(2023d) identifies and determines the reliability of interactions based on their related structural patterns learned on multiple large-scale recommendation datasets.
SLED Zhang et al.(2023d)は、複数の大規模推薦データセットで学習された関連構造パターンに基づき、相互作用の信頼性を識別・判定する。
FMLP-Rec Zhou et al.(2022) adopts learnable filters for denoising in sequential recommendation.
FMLP-Rec Zhouら(2022)は、逐次推薦におけるノイズ除去に学習可能なフィルタを採用している。
The learnable filters perform a fast Fourier transform (FFT) to convert the input sequence into the frequency domain and filter out noise through an inverse FFT procedure.
学習可能なフィルターは、高速フーリエ変換（FFT）を実行して入力シーケンスを周波数領域に変換し、逆FFT手順によってノイズを除去する。
SGDL Gao et al.(2022) leverages the self-labeled memorized data as guidance to offer denoising signals without requiring any auxiliary information or defining any weighting functions.
SGDL Gaoら(2022)は、自己ラベル付けされた記憶データをガイダンスとして活用し、補助情報を必要とせず、重み付け関数を定義することなく、ノイズ除去信号を提供する。
AutoDenoise Ge et al.(2023) adopts reinforcement learning to automatically and adaptively learn the most appropriate weight for each interaction.
AutoDenoise Geら(2023)は強化学習を採用し、各インタラクションに最適な重みを自動的に適応的に学習する。

### 4.2.2. Selection-Based Denoising 選択ベースのノイズ除去

Instead of assigning lower weights, the selection-based method directly removes the noisy data Tong et al.(2021); Wang et al.(2021a); Yuan et al.(2021); Zhang et al.(2022b); Lin et al.(2023a); Zhang et al.(2023c); Quan et al.(2023); Wang et al.(2023b); Lin et al.(2023b).
より低い重みを割り当てる代わりに、選択ベースの方法はノイズの多いデータを直接除去する Tong et al.(2021); Wang et al.(2021a); Yuan et al.(2021); Zhang et al.(2022b); Lin et al.(2023a); Zhang et al.(2023c); Quan et al.
For instance, different from R-CE, Wang et al.Wang et al.(2021a) propose another adaptive denoising training strategy called T-CE, which discards the interactions with large loss values.
例えば、R-CEとは異なり、Wangら(2021a)はT-CEと呼ばれる別の適応的ノイズ除去学習戦略を提案している。
RAP Tong et al.(2021) formulates the denoising process as a Markov decision process and proposes to learn a policy network to select the appropriate action (i.e., removing or keeping an interaction) to maximize long-term rewards.
RAP Tongら(2021)は、ノイズ除去プロセスをマルコフ決定過程として定式化し、長期的な報酬を最大化するために適切な行動（すなわち、相互作用を除去するか維持するか）を選択するためのポリシーネットワークを学習することを提案している。
DSAN Yuan et al.(2021) suggests using the entmax function to automatically eliminate the weights of irrelevant interactions.
DSAN Yuanら(2021)は、無関係な相互作用の重みを自動的に除去するためにentmax関数を使うことを提案している。
HSD Zhang et al.(2022b) learns both user-level and sequence-level inconsistency signals to further identify inherent noisy interactions.
HSD Zhangら(2022b)は、ユーザーレベルとシーケンスレベルの不整合シグナルの両方を学習し、固有のノイズの多い相互作用をさらに識別する。
DeCA Wang et al.(2023b) finds that different models tend to make more consistent agreement predictions for noise-free interactions, and utilizes predictions from different models as the denoising signal.
DeCA Wangら(2023b)は、異なるモデルがノイズのない相互作用についてより一貫した一致予測をする傾向があることを発見し、異なるモデルからの予測をノイズ除去信号として利用している。
GDMSR Quan et al.(2023) designs a self-correcting curriculum learning mechanism and an adaptive denoising strategy to alleviate noise in social networks.
GDMSR Quanら(2023)は、ソーシャルネットワークのノイズを緩和するために、自己修正カリキュラム学習メカニズムと適応的ノイズ除去戦略を設計している。
STEAM Lin et al.(2023b) further designs a corrector that can adaptively apply “keep”, “delete”, and “insert” operations to correct an interaction sequence.
STEAM Linら(2023b)はさらに、相互作用シーケンスを修正するために「keep」、「delete」、「insert」操作を適応的に適用できるコレクタを設計している。

Some studies integrate the reweighting-based method with the selection-based method for better denoising Tian et al.(2022); Ye et al.(2023).
より良いノイズ除去のために、再重み付けベースの手法と選択ベースの手法を統合した研究もある。
For instance, RGCF Tian et al.(2022) and RocSE Ye et al.(2023) estimate the reliability of user-item interactions using normalized cosine similarity between their respective embeddings.
例えば、RGCF Tian et al.(2022)やRocSE Ye et al.(2023)は、それぞれの埋め込み間の正規化コサイン類似度を用いて、ユーザとアイテムのインタラクションの信頼性を推定している。
Subsequently, they filter out interactions and only retain those whose weights exceed a pre-defined threshold value.
その後、相互作用をフィルタリングし、重みが事前に定義されたしきい値を超えるものだけを保持する。

### 4.2.3. Dataset Distillation/Condensation データセット 蒸留／凝縮

Dataset distillation or dataset condensation techniques Yu et al.(2023) aim to synthesize data points with the goal of condensing the comprehensive knowledge from the entire dataset into a small, synthetic data summary.
データセット蒸留またはデータセット凝縮技術 Yuら(2023)は、データセット全体からの包括的な知識を小さな合成データ要約に凝縮することを目標に、データ点を合成することを目的としている。
This process retains the essence of the data, enabling models to be trained more efficiently.
このプロセスはデータの本質を保持し、モデルをより効率的に学習させることができる。
Recently, some works Sachdeva et al.(2022); Wu et al.(2023) observe that dataset distillation has a strong data denoising effect in recommendation.
最近、Sachdevaら(2022); Wuら(2023)は、データセット蒸留が推薦において強いデータノイズ除去効果を持つことを観察している。
For example, DISTILL-CF Sachdeva et al.(2022) applies dataset meta-learning to synthetic user-item interactions.
例えば、DISTILL-CF Sachdeva et al.(2022)は、データセットのメタ学習を合成ユーザーとアイテムのインタラクションに適用している。
Remarkably, models trained on the condensed dataset synthesized by DISTILL-CF have demonstrated improved performance compared to those trained on the full, original dataset.
驚くべきことに、DISTILL-CFによって合成された凝縮データセットで訓練されたモデルは、完全なオリジナルデータセットで訓練されたモデルよりも性能が向上している。

### 4.2.4. Discussion ディスカッション

Normally, data collected from real-world scenarios are frequently contaminated with noise stemming from system bugs or user mistakes.
通常、実世界のシナリオから収集されたデータは、システムのバグやユーザーのミスに起因するノイズで汚染されていることが多い。
However, obtaining labels for this noise is often impractical or even impossible, due to the lack of expert knowledge required for identifying noise, the high costs associated with manual labeling, or the dynamic nature of some noise which makes it hard to give fixed labels.
しかし、ノイズの識別に必要な専門知識が不足していたり、手作業によるラベル付けに高いコストがかかったり、あるいはノイズの動的な性質によって固定的なラベル付けが困難であったりするため、このようなノイズのラベルを得ることは現実的でなかったり、不可能であったりすることが多い。
In the absence of the ground truth, it is difficult to determine whether the denoising method achieves the optimal situation – no over-denoising or under-denoising.
グランド・トゥルースがない場合、ノイズ除去法が最適な状況（オーバーデノイズやアンダーデノイズ）を達成しているかどうかを判断するのは難しい。
Taking into account this limitation, it may be preferable to synthesize a noise-free dataset via dataset distillation/condensation rather than attempting to adjust or filter the existing dataset through reweighting-based or selection-based methods.
この制限を考慮すると、重み付けに基づく方法や選択に基づく方法で既存のデータセットの調整やフィルタリングを試みるよりも、データセットの蒸留／凝縮によってノイズのないデータセットを合成する方が望ましいかもしれない。

## 4.3. Handling Biased Data バイアスのかかったデータを扱う

The key to handling biased data is to align the biased training distribution with the unbiased test distribution.
偏ったデータを扱う鍵は、偏った訓練分布と不偏のテスト分布を一致させることである。
According to the causes of biased data explained in Section 3.2, we divide existing debiasing methods into two categories: user preference alignment and item popularity alignment.
セクション3.2で説明した偏ったデータの原因に従って、既存のデビアス方法を2つのカテゴリーに分類する： ユーザ嗜好アライメントと項目人気アライメントである。

### 4.3.1. User Preference Alignment ユーザー嗜好の調整

User preferences may shift due to a variety of reasons, such as temporal changes Zafari et al.(2019); Wangwatcharakul and Wongthanavasu (2021); Ding et al.(2022), locational moves Yin et al.(2016), or alterations in personal and environmental conditions Zheng et al.(2021); He et al.(2022); Wang et al.(2023a).
ユーザーの嗜好は、時間的な変化Zafariら(2019); Wangwatcharakul and Wongthanavasu(2021);Dingら(2022)、場所的な移動Yinら(2016)、または個人的な条件や環境条件の変化Zhengら(2021); Heら(2022); Wangら(2023a)など、さまざまな理由で変化する可能性がある。
Existing methods are designed to track and adjust to these changes, thereby maintaining alignment with the ever-evolving user preferences.
既存の方法は、このような変化を追跡し、調整するように設計されているため、常に進化するユーザーの嗜好との整合性を維持することができる。
For example, Aspect-MF Zafari et al.(2019) analyzes and models temporal preference drifts using a component-based factorized latent approach.
例えば、Aspect-MF Zafari et al.(2019)は、成分ベースの因数分解潜在アプローチを用いて、時間的嗜好ドリフトを分析しモデル化している。
MTUPD Wangwatcharakul and Wongthanavasu (2021) adopts a forgetting curve function to calculate the correlations of user preferences across time.
MTUPD Wangwatcharakul and Wongthanavasu (2021)は、忘却曲線関数を採用し、ユーザーの嗜好の時間的相関を計算している。
ST-LDA Yin et al.(2016) learns region-dependent personal interests and crowd preferences to align locational preference drifts.
ST-LDA Yin et al.(2016)は、地域に依存した個人の興味と群衆の嗜好を学習し、場所的嗜好のドリフトを調整する。
Wang et al.Wang et al.(2023a) review user preference shifts across environments from a causal perspective and inspect the underlying causal relations through causal graphs.
Wangら.Wangら(2023a)は、因果的な観点から環境間のユーザーの嗜好の変化をレビューし、因果関係グラフを通してその根底にある因果関係を検証している。
Based on the causal relations, they further propose the CDR framework, which adopts a temporal variational autoencoder to capture preference shifts.
さらに、因果関係に基づき、嗜好の変化を捉えるために時間変分オートエンコーダを採用したCDRフレームワークを提案している。

### 4.3.2. Item Popularity Alignment アイテム人気アライメント

Existing methods for item popularity alignment roughly fall into five groups Zhang et al.(2023a).
項目人気アライメントのための既存の方法は、大まかに5つのグループに分類される。
Inverse propensity scoring Schnabel et al.(2016); Saito et al.(2020) utilizes the inverse of item popularity as a propensity score to rebalance the loss for each user-item interaction.
逆傾向スコアリング Schnabel et al.(2016); Saito et al.(2020) は，項目人気の逆数を傾向スコアとして利用し，各ユーザー-項目相互作用の損失をリバランスする．
Domain adaptation Bonner and Vasile (2018); Chen et al.(2020) leverages a small sample of unbiased data as the target domain to guide the training process on the larger but biased data in the source domain.
Domain adaptation Bonner and Vasile (2018); Chen et al. (2020)は、ターゲット・ドメインとしてバイアスのかかっていないデータの小さなサンプルを活用し、ソース・ドメインのより大きな、しかしバイアスのかかったデータに対する学習プロセスを導く。
Causal estimation Wei et al.(2021); Zhang et al.(2021b); Wang et al.(2022) identifies the effect of popularity bias through assumed causal graphs and mitigates its impact on predictions.
因果推定 Wei et al.(2021); Zhang et al.(2021b); Wang et al.(2022) は、仮定された因果グラフを通じて人気バイアスの影響を特定し、予測への影響を緩和する。
Regularization-based methods Boratto et al.(2021) explore regularization strategies to adjust recommendation results, aligning them more closely with the actual popularity distribution.
正則化に基づく方法 Boratto et al.(2021) は、推薦結果を調整し、実際の人気分布により近づけるための正則化戦略を探求している。
Generalization methods Zhang et al.(2022a, 2023b, 2023a) aim to learn invariant features that counteract popularity bias, thereby enhancing the stability and generalization capabilities of recommendation models.
汎化手法 Zhangら(2022a, 2023b, 2023a)は、人気バイアスを打ち消す不変特徴を学習することで、推薦モデルの安定性と汎化能力を高めることを目指している。

### 4.3.3. Discussion ディスカッション

Traditional evaluation settings in RSs may not be appropriate for assessing debiasing methods because they typically entail that the distribution of a test set is representative of the distribution in the training set (independent and identically distributed evaluation settings).
RSにおける従来の評価設定は、テスト集合の分布が訓練集合の分布を代表することが一般的であるため（独立同分布の評価設定）、デビアス手法の評価には適切ではないかもしれない。
Therefore, in this part, we discuss two out-of-distribution evaluation settings to assess debiasing methods:
そこでこのパートでは、デビアス法を評価するための2つの分布外評価設定について議論する：

• Temporal split setting: Temporal split setting slices the historical interactions into the training, validation, and test sets according to the timestamps Zhang et al.(2022a, 2023b).

- 時間分割設定： 時間的分割設定：時間的分割設定は、タイムスタンプに従って、過去の相互作用をトレーニングセット、検証セット、テストセットにスライスする。
  In this case, any shift in user preferences or item popularity over time is appropriately represented and accounted for during the evaluation.
  この場合、時間の経過に伴うユーザーの嗜好やアイテムの人気の変化は、評価中に適切に表現され、説明される。

• Popularity split setting: Popularity split setting constructs the training, validation, and test sets based on various popularity distributions Wei et al.(2021); Zheng et al.(2021).

- 人気度分割設定： 人気度分割設定は、様々な人気度分布に基づいて訓練、検証、テストセットを構築する。
  For example, the training interactions are sampled to be a long-tail distribution over items while the validation and test interactions are sampled with equal probability in terms of items (uniform popularity distribution).
  例えば、トレーニングの相互作用は項目に関するロングテール分布になるようにサンプリングされ、一方、検証およびテストの相互作用は項目に関して等確率でサンプリングされる（一様な人気分布）。
  However, such a split setting has an inherent drawback: it may inadvertently lead to information leakage.
  しかし、このような分割設定には固有の欠点がある： それは、不注意によって情報が漏れてしまう可能性があるということだ。
  By explicitly tailoring the test set to a known distribution of item popularity, the debiasing methods might be unduly influenced by this information.
  アイテムの人気度の既知の分布に合わせてテスト・セットを明示的に調整することで、デバイアシング手法がこの情報に不当に影響される可能性がある。

# 5. Future Directions 今後の方向性

## 5.1. Data-Centric RSs with Multimodal Data マルチモーダルデータによるデータ中心RS

Multimodal data refers to data that consists of multiple modalities or types of information, such as text, images, audio, video, or any combination thereof.
マルチモーダルデータとは、テキスト、画像、音声、映像、またはそれらの組み合わせなど、複数のモダリティやタイプの情報から構成されるデータのことである。
Traditionally, RSs have primarily relied on user-item interaction data, such as ratings or click-through data, to generate recommendations.
従来、RSはレコメンデーションを生成するために、主に評価やクリックスルーデータなどのユーザーアイテムインタラクションデータに依存してきた。
By incorporating multimodal data, RSs can capture richer and more diverse user preferences and item characteristics, leading to more personalized and relevant recommendations Truong and Lauw (2019).
マルチモーダルデータを取り入れることで、RSはより豊かで多様なユーザーの嗜好やアイテムの特徴を捉えることができ、よりパーソナライズされた適切なレコメンデーションにつながる Truong and Lauw (2019).
However, the data issues mentioned before (i.e., incomplete data, noisy data, and biased data) also exist in multimodal data, and they can pose additional challenges in the context of multimodal RSs:
しかし、先に述べたようなデータの問題（不完全なデータ、ノイズの多いデータ、偏ったデータなど）はマルチモーダルデータにも存在し、マルチモーダルRSの文脈ではさらなる課題となりうる：

• Heterogeneity: Multimodal data can be highly heterogeneous, with different modalities having distinct data formats, scales, and distributions.

- 異質性： マルチモーダルデータは、異なるモダリティが異なるデータ形式、スケール、分布を持ち、非常に異質である可能性がある。
  For example, text data may require natural language processing techniques, while image data may need computer vision algorithms.
  例えば、テキストデータには自然言語処理技術が必要かもしれないし、画像データにはコンピュータ・ビジョン・アルゴリズムが必要かもしれない。

• Imbalance: Multimodal datasets may exhibit imbalances in the distributions of different modalities.

- 不均衡： マルチモーダルデータセットは、異なるモダリティの分布に不均衡を示すことがある。
  For example, there may be a larger number of text samples compared to images or audio samples.
  例えば、画像や音声サンプルに比べ、テキストサンプルの数が多い場合があります。
  Modality imbalance can affect the performance and generalization of recommendation models trained on such data.
  モダリティの不均衡は、そのようなデータで学習された推薦モデルの性能と一般化に影響を与える可能性がある。

• Scalability: Multimodal data, especially when it includes high-dimensional modalities like images or videos, can be computationally expensive to process and analyze.

- スケーラビリティ： マルチモーダルデータは、特に画像や動画のような高次元のモダリティを含む場合、処理や分析に計算コストがかかる。
  Therefore, handling large-scale multimodal data may require efficient algorithms or distributed computing frameworks to ensure scalability.
  したがって、大規模なマルチモーダルデータを扱うには、スケーラビリティを確保するための効率的なアルゴリズムや分散コンピューティングフレームワークが必要になるかもしれない。

## 5.2. Data-Centric RSs with LLMs LLMによるデータ中心RS

With the emergence of large language models (LLMs) in natural language processing, there has been a growing interest in harnessing the power of these models to enhance recommender systems.
自然言語処理における大規模言語モデル（LLM）の出現に伴い、レコメンダーシステムを強化するためにこれらのモデルの力を活用することへの関心が高まっている。
In Data-Centric RSs, LLMs can serve as:
データ中心のRSでは、LLMは次のような役割を果たす：

• Recommendation models: Pre-trained LLMs can take as input a sequence that includes user profiles, item attributes, user-item interactions, and task instructions.

- 推薦モデル： 事前に訓練されたLLMは、ユーザープロファイル、アイテムの属性、ユーザーとアイテムの相互作用、タスクの指示を含むシーケンスを入力として受け取ることができる。
  Then LLMs analyze this information to understand the context and the user’s preferences.
  そしてLLMはこの情報を分析し、文脈とユーザーの好みを理解する。
  Based on this understanding, LLMs can generate a sequence that directly represents the recommendation results, which could be a list of items, a ranking of items, or even detailed descriptions or reasons for the recommendations.
  この理解に基づいて、LLMは、アイテムのリスト、アイテムのランキング、あるいは詳細な説明や推薦理由など、推薦結果を直接表すシーケンスを生成することができる。
  However, using LLMs as recommendation models also raises some challenges such as limited token length or latency, especially for users with a large amount of interactions.
  しかし、LLMを推薦モデルとして使用すると、トークンの長さや待ち時間が制限されるなどの課題も生じる。
  With data denoising techniques to improve the design of input sequences, the ability of LLMs as recommendation models can be further explored.
  入力シーケンスの設計を改善するデータノイズ除去技術により、推薦モデルとしてのLLMの能力をさらに探求することができる。

• Data processors: As mentioned before, given the extensive knowledge base and powerful reasoning capabilities of LLMs, some recent work has attempted to augment data with LLMs, for example, through carefully designed prompts, LLMRec Wei et al.(2023) employs three simple yet effective LLM-based data augmentation strategies to augment implicit feedback, user profiles, and item attributes, respectively.

- データプロセッサ： 例えば、LLMRec Wei et al.(2023)は、暗黙のフィードバック、ユーザープロファイル、アイテム属性をそれぞれ拡張するために、3つのシンプルかつ効果的なLLMベースのデータ拡張戦略を採用している。
  Moving forward, it’s crucial to investigate the capability of LLMs in managing tasks such as data denoising and data debiasing.
  今後、LLMがデータノイズ除去やデータデビアスのようなタスクを管理する能力を調査することは極めて重要である。
  This could pave the way for LLMs to harmonize Data-Centric RSs effectively.
  これは、LLMがデータ中心RSを効果的に調和させる道を開く可能性がある。

## 5.3. Automatic Data-Centric RSs 自動データ中心RS

Automatic machine learning (AutoML) He et al.(2021) refers to the process of automating the end-to-end process of applying machine learning to real-world problems, which typically involves automating a variety of tasks that are part of the machine learning workflow.
自動機械学習（AutoML）He et al.(2021)は、実世界の問題に機械学習を適用するエンド・ツー・エンドのプロセスを自動化するプロセスを指し、通常、機械学習ワークフローの一部である様々なタスクの自動化を伴う。
In the context of Data-Centric RSs, these tasks encompass data augmentation, data denoising, and data debiasing.
データ中心RSの文脈では、これらのタスクは、データの増強、データのノイズ除去、データのデバイアシングを含む。
Consequently, AutoML can automatically streamline and enhance the efficiency of these tasks, enabling more accurate recommendations, which is of great significance in practice.
その結果、AutoMLはこれらの作業を自動的に合理化し、効率化することができ、より正確な推薦を可能にする。

## 5.4. Transparent Data-Centric RSs 透明データ中心RS

Transparent Data-Centric RSs refer to Data-Centric RSs that not only offer enhanced data for model training but also provide insights into how and why particular enhancements are made, thereby allowing users and developers to understand the underlying decision-making processes.
透明なデータ中心RSとは、モデルトレーニングのために強化されたデータを提供するだけでなく、特定の強化がどのように行われ、なぜ行われたのかについての洞察も提供するデータ中心RSのことで、これによりユーザーや開発者は基本的な意思決定プロセスを理解することができる。
Research in transparent Data-Centric RSs is tackling complex challenges, such as the trade-off between transparency and complexity, ensuring user privacy while providing explanations, and developing standards for explainability and interpretability.
透明性の高いデータ中心型RSの研究は、透明性と複雑性のトレードオフ、説明を提供しながらユーザーのプライバシーを確保すること、説明可能性と解釈可能性の基準を開発することなど、複雑な課題に取り組んでいる。

# 6. Conclusion 結論

In this survey, we presented a comprehensive literature review of Data-Centric RSs.
本サーベイでは、データ中心型RSに関する包括的な文献レビューを行った。
We systematically analyzed three critical issues inherent in recommendation data and subsequently categorized existing works in accordance with their focus on these issues.
我々は、レコメンデーションデータに内在する3つの重要な問題を体系的に分析し、その後、これらの問題への焦点に従って既存の研究を分類した。
Additionally, we point out a range of prospective research directions to advance Data-Centric RSs.
さらに、データ中心型RSを発展させるための様々な研究の方向性を指摘する。
We expect that this survey can help readers easily grasp the big picture of this emerging field and equip them with the basic techniques and valuable future research ideas.
このサーベイが、読者がこの新興分野の全体像を容易に把握し、基本的なテクニックと貴重な将来の研究アイデアを身につける一助となることを期待している。
