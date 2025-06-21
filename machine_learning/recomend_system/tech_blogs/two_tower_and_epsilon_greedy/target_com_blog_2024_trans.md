https://tech.target.com/blog/contextual-offer-recommendation-engine

# Contextual Offer Recommendations Engine at Target ターゲットにおける文脈に基づくオファー推薦エンジン

July 11, 2024  
2024年7月11日

Lead Data Scientist - DS Guest and Digital  
リードデータサイエンティスト - DSゲストおよびデジタル

Privacy Note:  
プライバシーに関する注意:

While providing personalized experiences, Target also prioritizes guest privacy by honoring applicable guest privacy choices, following legal requirements, and adhering to Target’s.  
パーソナライズされた体験を提供する一方で、ターゲットは適用可能なゲストのプライバシー選択を尊重し、法的要件に従い、ターゲットのプライバシー基準を遵守することを優先しています。

## introduction 

Imagine walking into a Target store or browsing, and the offers that you see seem like they were picked just for you.  
ターゲットの店舗に入ったり、オンラインで閲覧したりすると、目にするオファーがまるであなたのために選ばれたかのように感じることを想像してください。
This isn't just a happy coincidence; it's the result of a fine blend of machine learning and retail strategy.  
これは単なる幸運な偶然ではなく、機械学習と小売戦略の巧妙な融合の結果です。

Target developed a new system called Contextual Offer Recommendation Engine (CORE), used to recommend personalized offers to each Target Circle guest.  
ターゲットは、各ターゲットサークルのゲストにパーソナライズされたオファーを推奨するために、文脈に基づくオファー推薦エンジン（contextual offer recommendation engine、CORE）という新しいシステムを開発しました。
Under the hood, CORE is powered by a contextual built on top of a rich custom feature set including transactions, promotions, and guest behavior that optimizes for guest engagement including offer adds and redemption.  
COREは、**トランザクション、プロモーション、ゲストの行動を含む豊富なカスタム特徴量セットの上に構築された文脈に基づいて動作**し、オファーの追加や引き換えを含むゲストのエンゲージメントを最適化します。

At the heart of this joyful shopping experience is our team, Offer Personalization.  
この楽しいショッピング体験の中心には、私たちのチームであるオファーパソナライズがあります。
We are an Artificial Intelligence/Machine Learning (AI/ML) team within Target Tech responsible for creating segmented offers for Target Circle members.  
私たちは、ターゲットテック内の人工知能/機械学習（AI/ML）チームで、ターゲットサークルのメンバー向けにセグメント化されたオファーを作成する責任を担っています。
In 2022, our team's scope increased, and we were tasked to improve offer performance in both offer engagement and incremental revenue.  
2022年には、私たちのチームの範囲が拡大し、**オファーのエンゲージメントと増分収益の両方においてオファーのパフォーマンスを向上させる任務が与えられました**。

In this blog, we will dive into how our recommendation system addresses interaction sparsity and utilizes a deep neural agent to deliver highly relevant offers to our guests.  
このブログでは、私たちの推薦システムがどのようにインタラクションの希薄性に対処し、深層ニューラルエージェントを利用してゲストに非常に関連性の高いオファーを提供するかについて掘り下げます。

## What is Target Circle?   ターゲットサークルとは何ですか？

In Target Circle, Target's loyalty program, members receive personalized spend-based offers called (TCB).  
ターゲットサークルは、ターゲットのロイヤルティプログラムで、メンバーは（TCB）と呼ばれるパーソナライズされた支出ベースのオファーを受け取ります。
CORE recommends customized TCB offers with specific spend and reward dollar amounts for Target Circle members.  
COREは、ターゲットサークルのメンバーに特定の支出および報酬金額を持つカスタマイズされたTCBオファーを推奨します。
Multi-trip-based spend threshold offers involve a series of shopping experiences where each trip's spending must exceed a certain dollar threshold to earn a reward of a specified value.  
マルチトリップベースの支出閾値オファーは、各トリップの支出が特定のドル閾値を超える必要がある一連のショッピング体験を含み、指定された価値の報酬を得ることができます。
For example, the first image above illustrates an offer: "Make 2 qualifying purchases of $80 or more to earn a $15 reward in Target Circle earnings."  
例えば、上の最初の画像は、「$80以上の2回の適格購入を行うと、ターゲットサークルの収益で$15の報酬を得る」というオファーを示しています。
These offers are designed to encourage frequent engagement with Target, rewarding consistent shopping behavior.  
これらのオファーは、ターゲットとの頻繁なエンゲージメントを促進し、一貫したショッピング行動を報いるように設計されています。

## Our Goal  

Our goal is to increase guest engagement and drive trips to Target by determining the most effective offers for our guests.  
私たちの目標は、ゲストにとって最も効果的なオファーを特定することによって、ゲストのエンゲージメントを高め、ターゲットへの訪問を促進することです。

## Our Solution 私たちの解決策

To address the need for personalization at a guest level, our team developed an advanced AI-driven contextual offer recommendation engine.  
ゲストレベルでのパーソナライズの必要性に対処するために、私たちのチームは高度なAI駆動の文脈に基づくオファー推薦エンジンを開発しました。

## How CORE Works COREの仕組み

Our contextual multi-arm bandit (CMAB) algorithm includes the state of the environment in the decision-making process, allowing context-specific decisions.
私たちのcontextual multi-arm bandit (CMAB)アルゴリズムは、環境の状態を意思決定プロセスに含め、文脈に応じた決定を可能にします。
CORE employs a combination of matrix factorization techniques and CMAB to generate pertinent offers.  
COREは、**行列分解技術とCMABの組み合わせを使用して、関連するオファーを生成します。**
We start by pulling historic guest offer interactions to construct an interaction matrix.  
私たちは、歴史的なゲストオファーのインタラクションを引き出してインタラクション行列を構築することから始めます。
This matrix is highly sparse as individual guests might have only a few interactions with Target Circle offers.  
この行列は非常に希薄であり、個々のゲストはターゲットサークルのオファーとのインタラクションがわずかしかない可能性があります。
In the image below, you can see that the rows show individual guests, and the columns reflect offer indices.  
下の画像では、行が個々のゲストを示し、列がオファーのインデックスを反映していることがわかります。


![Interaction matrix showing guest interactions with Target Circle offers]()
ターゲットサークルオファーとのゲストインタラクションを示すインタラクション行列

### a) Non-Negative Matrix Factorization (NNMF)

**Non-Negative Matrix Factorization (NNMF)** is used to reduce sparsity in interactions.  
非負値行列分解（NNMF）は、インタラクションの希薄性を減少させるために使用されます。
This is used because of its proficiency in uncovering latent features that represent underlying guest preferences and offer attributes.  
これは、基礎となるゲストの好みやオファーの属性を表す潜在的な特徴を明らかにする能力があるためです。
This method is particularly beneficial as it can capture the nonlinear relations in the data, thereby providing a deeper insight into user-offer interactions.  
この方法は、データ内の非線形関係を捉えることができるため、ユーザーとオファーのインタラクションに対するより深い洞察を提供します。

We apply NNMF to factorize the guest-offer matrix into matrices W (user matrix) and H (offer matrix).  
私たちは、guest-offer行列にNNMFを適用して、行列W（ユーザ行列）とH（オファー行列）に分解します。

The factorization can be represented as follows:  
分解は次のように表すことができます：

$$
V \approx W \times H^T
$$

where $V$ is the original interaction matrix, $W$ is the user matrix, $H$ is the offer matrix, and $H^T$ is the transpose of the offer matrix.  
ここで、$V$は元のインタラクション行列、$W$はユーザ行列、$H$はオファー行列、$H^T$はオファー行列の転置です。

In the next steps, the offer latent features (H) will be extensively leveraged as bandit's per-arm features in the CMAB approach, aiding in the fine-tuning of personalized offer recommendations.  
次のステップでは、オファーの潜在的特徴（H）がCMABアプローチにおけるバンディットの各アームの特徴として広く活用され、パーソナライズされたオファー推薦の微調整を助けます。

The reverse computation can be carried out to find an approximate interaction matrix $I'$ using the factorized matrices as:  
逆計算を行い、分解された行列を使用して近似インタラクション行列$I'$を見つけることができます：

$$
I' = W \times H^T
$$

This $I'$ is the approximation of the original interaction matrix, which retains most of the significant information from the original matrix.  
この$I'$は元のインタラクション行列の近似であり、元の行列からの重要な情報のほとんどを保持しています。
Each offer becomes a single arm bandit and guest features become context.  
**各オファーは単一のアームバンディットになり、ゲストの特徴は文脈になります**。
(あ〜、コールドスタートアイテムに対応しづらいタイプのやり方だ...!:thinking:)

Aided by the dense interaction data $I'$, the neural networks foster a stable environment where the loss function aptly gauges the divergence between predicted and actual values.  
密なインタラクションデータ $I'$ (=ユーザ特徴量?)によって支援され、ニューラルネットワークは、損失関数が予測値と実際の値の乖離を適切に測定する安定した環境を育みます。
This not only guards against overfitting but also improves the model's accuracy over successive iterations.  
これは過学習を防ぐだけでなく、モデルの精度を繰り返しのイテレーションで向上させます。

<!-- ここまで読んだ! -->

### b) The CORE’s CMAB Workflow: COREのCMABワークフロー：

CMAB excels in environments where the reward distributions of actions are not known a priori and must be estimated from observed outcomes.  
CMABは、各行動の報酬分布が事前に知られておらず、観察された結果から推定されなければならない環境で優れています。(CMABっていうか、MABが得意なことかな...!:thinking:)
The algorithm iteratively refines these estimates, maximizing the expected reward.
アルゴリズムはこれらの推定を反復的に洗練し、期待される報酬を最大化します。
CMAB leverages contextual guest information compared to standard multi-arm bandits to ultimately provide more accurate recommendations.  
CMABは、標準的なマルチアームバンディットと比較して**文脈に基づくゲスト情報を活用**し、最終的により正確な推薦を提供します。

Additionally, CMAB is adept at handling scenarios with inherent uncertainties, where outcomes of actions are unknown.  
さらに、**CMABは、行動の結果が不明な固有の不確実性を伴うシナリオを扱うのに優れています**。
Due to the sparse nature of guest-offer interaction data, the algorithm employs risk-reward balancing techniques, enhancing decision accuracy as it gathers more data.  
ゲストオファーインタラクションデータの希薄な性質のため、アルゴリズムはリスクと報酬のバランス技術を採用し、データを収集するにつれて意思決定の精度を向上させます。

![Guest offer CMAB workflow]()

- Environment: The environment provides contextual guest information and offers metadata which includes latent offer features (H), allowing the algorithm to make informed decisions.  
環境: 環境は文脈に基づくゲスト情報とオファーメタデータを提供し、潜在的なオファー特徴（H）を含み、アルゴリズムが情報に基づいた意思決定を行えるようにします。

- Reward Estimation: The agent learns from observed rewards generated by the environment. Rewards are computed based on approximate Interaction in matrix $I'$.  
報酬推定: エージェントは環境によって生成された観察された報酬から学習します。報酬は近似インタラクション行列$I'$に基づいて計算されます。

- Agent: The agent interacts with the environment, selecting offers based on state information and predicted rewards. It employs a Neural Epsilon-Agent approach to balance exploration and exploitation.  
エージェント: エージェントは環境と相互作用し、状態情報と予測された報酬に基づいてオファーを選択します。**探索と活用のバランスを取るために、[Neural Epsilon-Agentアプローチ](https://proceedings.mlr.press/v162/dann22a/dann22a.pdf)を採用**します。
Here, a deep network is developed to approximate the expected reward for each offer.  
ここでは、各オファーの期待報酬を近似するために深層ネットワークが開発されます。

<!-- ここまで読んだ! -->

### c) Neural Epsilon Agent with two towers + common tower 2つのタワーと共通タワーを持つニューラルEpsilonエージェント：

A neural Epsilon-Greedy agent is a type of reinforcement learning agent that combines the Epsilon-Greedy algorithm with a deep neural network.  
ニューラルEpsilon-Greedyエージェントは、**Epsilon-Greedyアルゴリズムと深層ニューラルネットワークを組み合わせた強化学習エージェントの一種**です。
The neural network is used to approximate the expected reward for each action, based on the current context.  
ニューラルネットワークは、**現在の文脈に基づいて各アクションの期待報酬を近似(=推定??)**するために使用されます。
One of the benefits of the Epsilon-Greedy algorithm is that it is simple to implement and easy to tune.
**Epsilon-Greedyアルゴリズムの利点の1つは、実装が簡単で調整が容易であること**です。
CORE's deep learning agent has 3 main components:  
**COREの深層学習エージェントには3つの主要なコンポーネント**があります：

- Guest Network: This network handles the processing of the guest or context features. The output of this network is fed into the Common Network. 
**ゲストネットワーク**: このネットワークは、ゲストまたは文脈の特徴の処理を担当します。このネットワークの出力は共通ネットワークに送られます。
(user tower, context towerとか呼ばれる方ね...!:thinking:)

- Offer Network: This network processes the features specific to each offer. The output of this network is also fed into the Common Network.  
**オファーネットワーク**: このネットワークは、各オファーに特有の特徴を処理します。このネットワークの出力も共通ネットワークに送られます。
(item towerとかaction towerとか呼ばれる方ね...!:thinking:)

- Common Tower Network: This network combines the information from both the Guest Network and the Offer Network and processes it through three more layers. The final output layer gives the action predictions or estimated rewards, which are used by the agent to make action selections.  
**共通タワーネットワーク**: このネットワークは、ゲストネットワークとオファーネットワークの両方からの情報を組み合わせ、**さらに3層を通して処理**します。最終出力層は、エージェントがアクション選択を行うために使用するアクション予測または推定報酬を提供します。

```
Agent Network 
 
 
Guest network                             Offer network 
 
     | (256 units)                           | (256 units) 
 
     |                                       | 
 
     V (512 units)                           V (512 units) 
 
     |                                       | 
 
     V (256 units)                           V (256 units) 
 
     |                                       | 
 
     +------------------+     +--------------+ 
 
                        |     | 
 
                        V     V 
 
                       Common Network 
 
                           | (256 units) 
 
                           | 
 
                           V (1024 units) 
 
                           | 
 
                           V (512 units) 
 
                           | 
 
                           V (estimated reward) 
```

<!-- ここまで読んだ! -->

### d) Maximizing Efficacy in Recommendations: 推薦の効果を最大化する：

The E-Greedy algorithm works by selecting actions in one of two ways:  
E-Greedyアルゴリズムは、アクションを次の2つの方法のいずれかで選択することによって機能します：

- With a probability epsilon, the agent will select a random action (exploration).
確率epsilonで、エージェントはランダムなアクションを選択します（探索）。

- With a probability 1-epsilon, the agent will select the action that has the highest expected reward (exploitation).  
確率1-epsilonで、エージェントは期待報酬(の推定値!)が最も高いアクションを選択します（活用）。

![Diagram of E-Greedy Algorithm]()


Epsilon is a hyper-parameter that determines the balance between exploration and exploitation.  
Epsilonは、探索と活用のバランスを決定するハイパーパラメータです。
A high value for epsilon will result in more exploration, while a low value will result in more exploitation.  
Epsilonの高い値はより多くの探索をもたらし、低い値はより多くの活用をもたらします。

In uncertain environments, it's crucial to explore different options to gain more information.  
不確実な環境では、さまざまなオプションを探索してより多くの情報を得ることが重要です。
CMAB incorporates an exploration mechanism, which helps in discovering the effectiveness of various offers despite limited information.  
CMABは探索メカニズムを組み込み、限られた情報にもかかわらずさまざまなオファーの効果を発見するのに役立ちます。

- Explore Vs Exploit: Exploration delves into testing different offers to uncover what truly resonates with guests for long-term gain.  
**探索と活用**: 探索は、異なるオファーをテストして、ゲストに本当に響くものを明らかにし、長期的な利益を得ることに焦点を当てます。
In contrast, exploitation focuses on presenting guests with offers that are most likely to engage them in the short term.  
対照的に、活用はゲストが短期的に関与する可能性が最も高いオファーを提示することに焦点を当てます。
The feedback gained from exploration is crucial in refining the future offer recommendations.  
**探索から得られたフィードバックは、将来のオファー推薦を洗練する上で重要**です。

- Balancing the Trade-off: The right balance between exploration and exploitation is critical as the model learns from dynamic guest preferences, ensuring its effectiveness aligns with evolving market trends.  
トレードオフのバランス: 探索と活用の適切なバランスは、モデルが動的なゲストの好みから学習するために重要であり、その効果が進化する市場のトレンドに合致することを保証します。

Balancing the explore and exploit tradeoff is similar to balancing a bias vs. variance tradeoff.  
**探索と活用のトレードオフのバランスを取ることは、バイアスと分散のトレードオフのバランスを取ることに似ています**。
High levels of exploration might result in less-than-optimal offers in the short term, whereas a low exploration rate can create an echo effect, where the recommendation model becomes restricted to its previous predictions for future learning.
高い探索レベルは短期的に最適でないオファーをもたらす可能性がある一方で、低い探索率はエコー効果を生み出し、推薦モデルが将来の学習のために以前の予測に制限されることがあります。

<!-- ここまで読んだ! -->

## A/B Testing - Results A/Bテスト - 結果

For testing the model, we used a robust A/B experimentation framework built on a multi-variate stratified sampling method.  
モデルのテストには、**多変量層化サンプリング法に基づいた堅牢なA/B実験フレームワーク**(こういう手法があるのか...!:thinking:)を使用しました。
We split the initial audience list into two groups:  
初期のオーディエンスリストを2つのグループに分けました：

- Variant (This group receives offers from CORE model)  
バリアント（このグループはCOREモデルからのオファーを受け取ります）
(treatment群のことだと思うんだけど、variantっていうのか...!:thinking:)

- Control (This group receives offers from the production baseline method)  
コントロール（このグループは生産ベースライン手法からのオファーを受け取ります）

A holdout group is kept separate from both Variant and Control for incremental sales measurement.  
**ホールドアウトグループは、増分売上測定のためにバリアントとコントロールの両方から分離**されます。(これなんだろ??:thinking:)
The primary metric of interest here is the opt-in rate, i.e. the percentage of guests who opted in or added the offer divided by the total number of guests who received the offer.  
ここでの**primary metric**は、オプトイン率、すなわちオファーにオプトインまたは追加したゲストの割合を、オファーを受け取ったゲストの総数で割ったものです。
The secondary metric here is the Completion Rate, defined as the percentage of guests who completed the offer from the initial pool of guests who opted in.  
ここでのsecondary metricは、オファーを完了したゲストの割合を、オプトインした初期のゲストプールから定義した完了率です。
(ちゃんとprimary decision metricとsecondary  metricsを分けて考えられてるのが流石だな...!:thinking:)

![A/B Testing Audience with Test and Decision Metrics A/Bテストオーディエンスとテストおよび決定指標]()

We performed seven tests with CORE and observed a statistically significant positive lift in both of our engagement metrics in each test.  
私たちはCOREを使用して7回のテストを行い、各テストで両方のエンゲージメント指標において統計的に有意なプラスの向上を観察しました。
The variant in the testing, CORE, enabled more guests to engage with, on the Target app, and in our sped a streamlined data preparation and model deployment process, using PySpark for efficient data handling and TensorFlow for machine learning, with model training and scoring orchestration on Kubeflow.  
テストのバリアントであるCOREは、ターゲットアプリでより多くのゲストが関与できるようにし、データ準備とモデル展開プロセスを効率化しました。データ処理にはPySparkを、機械学習にはTensorFlowを使用し、モデルのトレーニングとスコアリングのオーケストレーションにはKubeflowを使用しました。
CORE powered millions of recommended offers in 2023.  
COREは2023年に数百万の推奨オファーを提供しました。

## Next Steps   次のステップ

The Offer Personalization team's goal is to make shopping with Target more engaging and fun by presenting offers that guests are excited about, turning every trip into a uniquely tailored experience.  
オファーパソナライズチームの目標は、ゲストが興奮するオファーを提示することによって、ターゲットでのショッピングをより魅力的で楽しいものにし、すべての訪問をユニークにカスタマイズされた体験に変えることです。
This work has taken the mantel from personalization at a cohort level to a state of hyper-personalization at a guest level.  
この作業は、コホートレベルでのパーソナライズからゲストレベルでのハイパーパーソナライズの状態に移行しました。
The current implementation also allows for enhancements to bring multi-objective models, where many metrics can be optimized at once.  
現在の実装は、**複数の指標を同時に最適化できるマルチオブジェクティブモデルを導入**するための強化も可能にします。

<!-- ここまで読んだ! -->
