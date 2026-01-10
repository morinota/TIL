## CHAPTER 1: Building Machine Learning Systems 第1章: 機械学習システムの構築

Imagine you have been tasked with producing a financial forecast for the upcoming financial year. 
あなたは、来るべき会計年度の財務予測を作成する任務を与えられたと想像してください。
You decide to use machine learning (ML), as there is a lot of available data, but, not unexpectedly, the data is spread across many different places—in spreadsheets and many different tables in the data warehouse. 
利用可能なデータがたくさんあるため、機械学習（ML）を使用することに決めましたが、予想通り、**データはスプレッドシートやデータウェアハウスのさまざまなテーブルに分散**しています。
You have been working for several years at the same organization, and this is not the first time you have been given this task. 
あなたは同じ組織で数年間働いており、このタスクを与えられるのはこれが初めてではありません。
Every year to date, the final output of your model has been a Power‐ Point presentation showing the financial projections. 
これまでの毎年、あなたのモデルの最終出力は財務予測を示すPowerPointプレゼンテーションでした。
Each year, you trained a new model, your model made only one prediction, and you were finished with it. 
毎年、新しいモデルを訓練し、モデルは1つの予測を行い、それで終わりでした。
Each year, you started effectively from scratch. 
毎年、実質的にゼロから始めていました。
You had to find the data sources (again), rerequest access to the data to create the features for your model, and then dig out the Jupyter notebook from last year and update it with new data and improvements to your model. 
データソースを（再度）見つけ、モデルの特徴を作成するためにデータへのアクセスを再リクエストし、昨年のJupyterノートブックを掘り出して新しいデータとモデルの改善で更新する必要がありました。

This year, however, you realize that it may be worth investing the time in building the scaffolding for this project so that you have less work to do next year. 
**しかし、今年はこのプロジェクトのための足場を構築するために時間を投資する価値があることに気づきます。そうすれば、来年の作業が少なくて済みます。**
So instead of delivering a PowerPoint, you decide to build a dashboard. 
したがって、PowerPointを提供する代わりに、ダッシュボードを構築することに決めました。
Instead of requesting one-off access to the data, you build feature pipelines that extract the historical data from its source(s) and compute the features (and labels) used in your model. 
一時的なデータアクセスをリクエストする代わりに、データのソースから履歴データを抽出し、モデルで使用される特徴（およびラベル）を計算する特徴パイプラインを構築します。
You have an insight that the feature pipelines can be used to do two things: compute both the historical features used to train your model and the features that will be used as inputs into your trained model, which outputs the predictions. 
**特徴パイプラインは2つのことに使用できるという洞察があります。モデルを訓練するために使用される履歴的特徴と、訓練されたモデルに入力として使用される特徴の両方を計算すること**です。
Now, after training your model, you can connect it to the feature pipelines to make predictions that power your dashboard. 
今、モデルを訓練した後、特徴パイプラインに接続してダッシュボードを動かす予測を行うことができます。
You thank yourself when you only have to tweak this ML system by adding/updating/removing features and training a new model. 
特徴を追加/更新/削除し、新しいモデルを訓練することで、このMLシステムを調整するだけで済むと自分に感謝します。
You update the frequency of your financial forecasts to quarterly with no extra work. 
追加の作業なしで、財務予測の頻度を四半期ごとに更新します。
You use the time you saved in grunt data sourcing, cleaning, and feature engineering to investigate new ML frameworks and model architectures, resulting in a much-improved financial model, much to the delight of your boss.  
データソーシング、クリーニング、特徴エンジニアリングで節約した時間を使って、新しいMLフレームワークやモデルアーキテクチャを調査し、結果として大幅に改善された財務モデルを作成し、上司を喜ばせます。

<!-- ここまで読んだ! -->

This example shows the difference between training a model to make a one-off prediction on a static dataset and building a batch ML system—a system that automates reading from data sources, transforming data into features, training models, performing inference on new data with the model, and updating a dashboard with the model’s predictions. 
**この例は、静的データセットに対して一度きりの予測を行うためにモデルを訓練することと、データソースからの読み取りを自動化し、データを特徴に変換し、モデルを訓練し、新しいデータに対してモデルで推論を行い、モデルの予測でダッシュボードを更新するバッチMLシステムを構築することの違いを示しています。**
The dashboard is the value delivered by the model to stakeholders. 
**ダッシュボードは、モデルがステークホルダーに提供する価値**です。

If you want a model to generate repeated value, the model should make predictions more than once. 
モデルに繰り返し価値を生成させたい場合、モデルは1回以上予測を行う必要があります。
That means you are not finished when you have evaluated the model’s performance on a test set drawn from your static dataset. 
つまり、静的データセットから抽出したテストセットでモデルのパフォーマンスを評価したときに、あなたは終わりではありません。
Instead, you will have to build _ML pipelines, which are programs that transform raw data into features, feed_ features to your model for easy retraining, and feed new features to your model so that it can make predictions, generating value with every new prediction it makes. 
代わりに、生のデータを特徴に変換し、モデルに特徴を供給して簡単に再訓練できるようにし、新しい特徴をモデルに供給して予測を行わせる_ MLパイプラインを構築する必要があります。これにより、モデルが行う新しい予測ごとに価値を生成します。

With this book, you will embark on the same journey from training models on static datasets to building _ML systems—from decision trees to deep learning to LLM-_ powered (large language model) agents. 
この本を通じて、静的データセットでモデルを訓練することから_ MLシステムを構築する同じ旅に出ることになります。決定木から深層学習、LLM（大規模言語モデル）を活用したエージェントまで。
The most important part of that journey is working with dynamic data. 
**その旅の最も重要な部分は、動的データを扱うこと**です。
This means moving from static data (such as the hand-curated datasets used in ML competitions found on Kaggle.com and crafting prompts for LLMs), to batch data that’s updated at some interval (hourly, daily, weekly, yearly), to the real-time data that’s needed to build intelligent interactive applications. 
これは、静的データ（Kaggle.comで見つかるMLコンペティションで使用される手作りのデータセットやLLMのためのプロンプト作成など）から、ある間隔（毎時、毎日、毎週、毎年）で更新されるバッチデータ、そしてインテリジェントなインタラクティブアプリケーションを構築するために必要なリアルタイムデータに移行することを意味します。

<!-- ここまで読んだ! -->

### The Anatomy of a Machine Learning System 機械学習システムの構造

One of the main challenges you will face in building ML systems is managing the data that is used to train models and the data that models make predictions with. 
MLシステムを構築する際に直面する主な課題の1つは、モデルを訓練するために使用されるデータと、モデルが予測を行うために使用するデータを管理することです。
We can categorize ML systems by how they process the new data that is used to make predictions. 
MLシステムは、予測を行うために使用される新しいデータを処理する方法によって分類できます。
Does the ML system make predictions on a schedule (for example, once per day), or does it run 24/7, making predictions in response to user requests? 
MLシステムは、スケジュールに従って予測を行いますか（たとえば、1日1回）、それとも24時間365日稼働し、ユーザーのリクエストに応じて予測を行いますか？

<!-- ここまで読んだ! -->

Spotify’s Discovery Weekly is an example of a batch ML system, which is a recommendation engine that, once per week, predicts which songs you might want to listen to and adds them to your playlist. 
**SpotifyのDiscovery WeeklyはバッチMLシステムの一例で、週に1回、あなたが聴きたい曲を予測し、それをプレイリストに追加するレコメンデーションエンジンです。**
In a batch ML system, the ML system reads a batch of data (from all 575M+ users in the case of Spotify) and makes predictions using the trained recommender ML model for all rows in the batch of data.
バッチMLシステムでは、MLシステムはデータのバッチ（Spotifyの場合、575M以上のユーザーから）を読み取り、バッチ内のすべての行に対して訓練されたレコメンダーMLモデルを使用して予測を行います。
The model takes all of the input features (such as how often you listen to music and the genres of music you listen to) and makes a prediction of the 30 “best” songs for you for the upcoming week. 
モデルはすべての入力特徴（音楽を聴く頻度や聴く音楽のジャンルなど）を取り込み、次の週にあなたにとっての「ベスト」な30曲を予測します。
The predictions are then stored in a database (Cassandra), and when you log on, the Spotify weekly recommendation list is downloaded from the database and shown as recommendations in the user interface. 
予測はデータベース（Cassandra）に保存され、ログインするとSpotifyの週間レコメンデーションリストがデータベースからダウンロードされ、ユーザーインターフェースにレコメンデーションとして表示されます。

<!-- ここまで読んだ! -->

TikTok’s recommendation engine, on the other hand, is famous for adapting its recommendations in near real time as you click and watch its short-form videos. 
**一方、TikTokのレコメンデーションエンジンは、あなたが短い動画をクリックして視聴する際に、ほぼリアルタイムでレコメンデーションを適応させることで有名**です。
TikTok’s recommendation service is a _real-time ML system. It predicts which videos to_ show you as you scroll and watch videos. 
TikTokのレコメンデーションサービスは_リアルタイムMLシステムです。スクロールして動画を視聴する際に、どの動画を_表示するかを予測します。
Andrej Karpathy, ex-head of AI at Tesla, said TikTok’s recommendation engine “is scary good. It’s digital crack.” 
テスラの元AI責任者であるAndrej Karpathyは、TikTokのレコメンデーションエンジンについて「恐ろしいほど優れている。デジタルクラックだ」と述べました。
TikTok was the first online video platform to include real-time recommendations, which gave it a competitive advantage over incumbents that enabled it to build the world’s second most popular online video platform. 
**TikTokはリアルタイムレコメンデーションを含む最初のオンライン動画プラットフォーム**であり、これにより既存のプラットフォームに対して競争優位性を持ち、世界で2番目に人気のあるオンライン動画プラットフォームを構築することができました。

<!-- ここまで読んだ! -->

Lovable is a coding assistant for building web applications from a chat window on its website. 
Lovableは、ウェブサイトのチャットウィンドウからウェブアプリケーションを構築するためのコーディングアシスタントです。
It is the fastest-growing software company to reach $100 million in revenue, which took it just eight months. 
これは、わずか8ヶ月で1億ドルの収益に達した最も急成長しているソフトウェア会社です。
Lovable is an _agentic AI system that takes your_ instructions and uses an LLM to create and run your web application as TypeScript code along with CSS styling and an optional integrated database. 
Lovableは、あなたの指示を受け取り、LLMを使用してウェブアプリケーションをTypeScriptコードとして作成し、CSSスタイリングとオプションの統合データベースを使用して実行する_エージェンティックAIシステムです。
Agentic systems have natural language interfaces. 
エージェンティックシステムは自然言語インターフェースを持っています。
You give them a high-level goal or task to execute, and they work with a high degree of autonomy to achieve your goal or task. 
あなたは彼らに高レベルの目標やタスクを実行するように指示し、彼らはその目標やタスクを達成するために高い自律性で作業します。
Agentic systems are more often interactive systems than batch systems, but both are possible. 
エージェンティックシステムはバッチシステムよりもインタラクティブシステムであることが多いですが、**両方とも可能**です。(??)

This book provides a unified architecture, based around ML pipelines, for building these three types of ML systems: batch, real-time, and LLM applications. 
この本は、バッチ、リアルタイム、LLMアプリケーションの3種類のMLシステムを構築するためのMLパイプラインを基にした統一アーキテクチャを提供します。
In particular, this book addresses the data challenges in building ML systems. 
特に、**この本はMLシステムを構築する際のデータの課題に対処**します。
Most ML systems need to process different types of data from different data sources, both for training models and for making predictions (inferences). 
ほとんどのMLシステムは、モデルを訓練するためと予測（推論）を行うために、異なるデータソースから異なる種類のデータを処理する必要があります。
For example, when TikTok recommends videos to you, it uses your recent viewing behavior (clicks, swipes, likes), your historical viewing behavior and preferences, and aggregated information such as what videos are trending right now for users like you, near you. 
たとえば、TikTokがあなたに動画を推薦する際、最近の視聴行動（クリック、スワイプ、いいね）、過去の視聴行動や好み、そしてあなたのようなユーザーに近い場所で現在トレンドになっている動画などの集約情報を使用します。
Processing all of this data in ML pipelines at scale is a significant engineering challenge that we cover in this book. 
**これらすべてのデータを大規模にMLパイプラインで処理することは、この本で取り上げる重要なエンジニアリングの課題**です。

<!-- ここまで読んだ! -->

#### Types of Machine Learning 機械学習の種類

The main types of machine learning used in ML systems are supervised learning, unsupervised learning, self-supervised learning, reinforcement learning, and in-context learning: 
MLシステムで使用される主な機械学習の種類は、教師あり学習、教師なし学習、自己教師あり学習、強化学習、インコンテキスト学習です。

_Supervised learning_ In supervised learning, you train a model with data containing features and labels. 
_教師あり学習_ 教師あり学習では、特徴とラベルを含むデータでモデルを訓練します。
Each row in a training dataset contains a set of input feature values and a label (the outcome, given the input feature values). 
訓練データセットの各行には、入力特徴値のセットとラベル（入力特徴値に基づく結果）が含まれています。
Supervised ML algorithms learn relationships between the labels (also called the target variables) and the input feature values. 
教師ありMLアルゴリズムは、ラベル（ターゲット変数とも呼ばれる）と入力特徴値との関係を学習します。
Supervised ML is used to solve classification problems, in which the ML system will answer yes-or-no questions (Is there a hot dog in this photo?) or make a multi-class classification (What type of hot dog is this?). 
教師ありMLは、MLシステムがイエスまたはノーの質問に答える（この写真にホットドッグはありますか？）か、マルチクラス分類を行う（これはどのタイプのホットドッグですか？）ために使用されます。
Supervised ML is also used to solve regression problems, in which the model predicts a numeric value using the input feature values (e.g., by estimating the price of an apartment, given input features such as its area, condition, and location). 
教師ありMLは、モデルが入力特徴値を使用して数値を予測する回帰問題を解決するためにも使用されます（たとえば、面積、状態、場所などの入力特徴に基づいてアパートの価格を推定することによって）。
Finally, supervised ML is also used to fine-tune chatbots using open source LLMs. 
最後に、教師ありMLはオープンソースのLLMを使用してチャットボットを微調整するためにも使用されます。
For example, if you train a chatbot with questions (features) and answers (labels) from the legal profession, your chatbot can be fine-tuned so that it talks like a lawyer.  
たとえば、法律業界からの質問（特徴）と回答（ラベル）でチャットボットを訓練すると、チャットボットは弁護士のように話すように微調整できます。

<!-- ここまで読んだ! -->
_Unsupervised learning_ In contrast, unsupervised learning algorithms learn from input features without any labels. 
_教師なし学習_ 対照的に、教師なし学習アルゴリズムはラベルなしの入力特徴から学習します。
For example, you could train an anomaly detection system with credit card transactions, and if an anomalous credit card transaction arrives, you could flag it as suspicious and potentially fraudulent. 
たとえば、クレジットカード取引で異常検知システムを訓練し、異常なクレジットカード取引が発生した場合、それを疑わしいものとしてフラグを立て、潜在的に詐欺的であると見なすことができます。

_Self-supervised learning_ Self-supervised learning involves generating a labeled dataset from a fully unlabeled one. 
_自己教師あり学習_ 自己教師あり学習は、**完全にラベルのないデータセットからラベル付きデータセットを生成することを含み**ます。
The main method of generating the labeled dataset is _masking. 
ラベル付きデータセットを生成する主な方法は_マスキングです。
For natural language processing (NLP), you can provide a piece of text and mask out individual words (via masked language modeling) and train a model to predict the missing word. 
自然言語処理（NLP）では、テキストの一部を提供し、個々の単語をマスクアウト（マスクされた言語モデリングを介して）し、欠落している単語を予測するモデルを訓練できます。
Here, you know the label (the missing word), so you can train the model using any supervised learning algorithm. 
ここでは、ラベル（欠落している単語）を知っているので、任意の教師あり学習アルゴリズムを使用してモデルを訓練できます。
In NLP, you can also mask out entire sentences with next-sentence prediction that can teach a model to understand longer-term dependencies across sentences. 
NLPでは、次の文の予測を使用して、モデルが文間の長期的な依存関係を理解できるように、全体の文をマスクアウトすることもできます。
The language model BERT uses both masked language modeling and next-sentence prediction for training. 
言語モデルBERTは、訓練のためにマスクされた言語モデリングと次の文の予測の両方を使用します。
Similarly, with image classification, you can mask out a (randomly chosen) small part of each image and then train a model to reproduce the original image with as high fidelity as possible. 
同様に、画像分類では、各画像の（ランダムに選ばれた）小さな部分をマスクアウトし、元の画像をできるだけ高い忠実度で再現するモデルを訓練できます。

<!-- ここまで読んだ! -->

_Reinforcement learning_ Reinforcement learning (RL) is another type of ML algorithm (not covered in this book). 
_強化学習_ 強化学習（RL）は、別のタイプのMLアルゴリズムです（この本では扱っていません）。
RL is concerned with learning how to make optimal decisions. 
RLは、最適な意思決定を行う方法を学ぶことに関係しています。

<!-- ここまで読んだ! -->

_In-context learning_ Supervised ML, unsupervised ML, and RL can only learn with the data they are trained on. 
_インコンテキスト学習_ 教師ありML、教師なしML、RLは、訓練されたデータでのみ学習できます。
However, LLMs that are large enough exhibit a different type of ML: in-context learning, which is the ability to learn to solve new tasks by providing context (examples) in the prompt to the LLM. 
しかし、十分に大きなLLMは異なるタイプの機械学習を示します：**インコンテキスト学習です。これは、LLMへのプロンプトにコンテキスト（例）を提供することによって新しいタスクを解決する方法を学ぶ能力**です。
LLMs exhibit in-context learning even though they are trained only with the objective of next-token prediction.
LLMsは、次のトークン予測の目的でのみ訓練されているにもかかわらず、インコンテキスト学習を示します。
Agents build on in-context learning, but they require context engineering to get the relevant data into the LLM’s prompt. 
エージェントはインコンテキスト学習に基づいて構築されますが、関連データをLLMのプロンプトに取り込むためにはコンテキストエンジニアリングが必要です。
With in-context learning, the newly learned skill is forgotten directly after the LLM’s context window is emptied—no model weights are updated as they are during model training.
**インコンテキスト学習では、新しく学習したスキルはLLMのコンテキストウィンドウが空になるとすぐに忘れられます**—モデルの重みはモデル訓練中のように更新されません。

<!-- ここまで読んだ! -->

ChatGPT is a good example of an AI system that uses a combination of different types of ML. 
ChatGPTは、異なるタイプの機械学習の組み合わせを使用するAIシステムの良い例です。
ChatGPT includes an LLM pretrained with self-supervised learning, supervised learning to fine-tune the foundation model to create a task-specific model (such as a chatbot), and RL (with human feedback) to align the task-specific model with human values (e.g., to remove bias and vulgarity in a chatbot).
**ChatGPTは、自己教師あり学習で事前訓練されたLLM、基盤モデルを微調整してタスク特化型モデル（チャットボットなど）を作成するための教師あり学習、およびタスク特化型モデルを人間の価値観に合わせるための強化学習（人間のフィードバックを伴う）を含んでいます**（例：チャットボットのバイアスや下品さを取り除くため）。
Finally, LLMs can learn from the data in the input prompt by using in-context learning.
最後に、LLMsはインコンテキスト学習を使用して入力プロンプトのデータから学ぶことができます。

<!-- ここまで読んだ! -->

#### Data Sources　データソース

Data for ML systems can, in principle, come from any available data source. 
MLシステムのデータは、原則として、利用可能な任意のデータソースから取得できます。
That said, some data sources and data formats are more popular as input into ML systems.
とはいえ、いくつかのデータソースやデータフォーマットは、MLシステムへの入力としてより一般的です。
In this section, we introduce the data sources most commonly encountered in enterprise computing.[1]
このセクションでは、**エンタープライズコンピューティングで最も一般的に遭遇するデータソース**を紹介します。[1]

<!-- ここまで読んだ! -->

##### Tabular data　表形式データ

_Tabular data is data stored as tables containing columns and rows, typically in a data‐_ base. 
_表形式データは、通常データベース内の列と行を含むテーブルとして保存されるデータです。_
There are two main types of databases that are sources of data for ML:
**MLのデータソースとなるデータベースには、主に2つのタイプ**があります: 

_Row-oriented stores_ These include relational databases and NoSQL databases. 
_行指向ストア_ これには、リレーショナルデータベースとNoSQLデータベースが含まれます。
They have a storage layout that is optimized for reading and writing rows of data.
これらは、データの行を読み書きするために最適化されたストレージレイアウトを持っています。

_Column-oriented stores_ These include _data warehouses and_ _data lakehouses. 
_列指向ストア_ これには、_データウェアハウス_ と_データレイクハウス_ が含まれます。
They have a storage layout_ that is optimized for reading and processing columns of data (such as computing the min/max/average/sum for a column).
これらは、データの列を読み取り処理するために最適化されたストレージレイアウトを持っています（例えば、列の最小/最大/平均/合計を計算するなど）。

As a developer, you need to familiarize yourself with the APIs and query languages for both row-oriented and column-oriented stores. 
開発者として、行指向ストアと列指向ストアの両方のAPIとクエリ言語に慣れる必要があります。
For example, SQL and objectrelational mappers (ORM) are used by relational databases (MySQL, Postgres), keyvalue APIs (Cassandra, RocksDB), and JSON store APIs (MongoDB).
例えば、SQLやオブジェクトリレーショナルマッパー（ORM）は、リレーショナルデータベース（MySQL、Postgres）、キー値API（Cassandra、RocksDB）、およびJSONストアAPI（MongoDB）で使用されます。
Columnar stores typically support reading and writing data with SQL and DataFrame APIs (Spark, Pandas, Polars).
列指向ストアは通常、SQLおよびDataFrame API（Spark、Pandas、Polars）を使用してデータの読み書きをサポートします。

In enterprises, much of the data generated by applications is stored in row-oriented stores. 
**企業では、アプリケーションによって生成されたデータの多くが行指向ストアに保存されます。**
Most enterprises have a large number of such databases, and instead of analyz‐ ing the data directly in place, they typically employ data pipelines that transfer some or all of the operational data to a centralized, scalable columnar store. 
**ほとんどの企業はそのようなデータベースを多数持っており、データを直接分析するのではなく、通常はデータパイプラインを使用して、運用データの一部またはすべてを中央集権的でスケーラブルな列指向ストアに転送します。**
This enables analysts to process all historical data for the whole company in a platform. 
これにより、アナリストはプラットフォーム上で会社全体のすべての履歴データを処理できます。
This ana‐ lytical data is also the most common data source for AI systems in enterprises.
この分析データは、企業のAIシステムにとって最も一般的なデータソースでもあります。

<!-- ここまで読んだ! -->

##### Event data　イベントデータ

_Event data contains a record of discrete occurrences or actions that happen at specific_ points in time, such as clicks on a website or a reading from a sensor. 
_イベントデータは、特定の_ 時点で発生する離散的な出来事やアクションの記録を含みます。例えば、ウェブサイトのクリックやセンサーからの読み取りなどです。
An _event-_ _streaming platform, such as Apache Kafka, is a data platform for collecting and tem‐_ porarily storing event data for downstream consumers of the event data. 
_イベントストリーミングプラットフォーム_（Apache Kafkaなど）は、イベントデータの下流の消費者のためにイベントデータを収集し、一時的に保存するためのデータプラットフォームです。
Examples of consumers are columnar data stores that store raw event data for subsequent analysis as well as stream processing programs that enable you to build real-time ML systems that react within a second of your click or swipe on their website.
**消費者の例としては、後続の分析のために生のイベントデータを保存する列指向データストアや、ウェブサイトでのクリックやスワイプに対して1秒以内に反応するリアルタイムMLシステムを構築できるストリーム処理プログラム**があります。

<!-- ここまで読んだ! -->

##### Graph data　グラフデータ

_Graph data is represented as nodes (entities) and edges (relationships). 
_グラフデータは、ノード（エンティティ）とエッジ（関係）として表現されます。_
Graph data‐_ bases support the efficient storage and retrieval of complex, interconnected graph data. 
グラフデータベースは、複雑で相互接続されたグラフデータの効率的な保存と取得をサポートします。
The rich connectivity and attributes inherent in the graph enable ML models for link prediction and fraud detection. 
グラフに固有の豊富な接続性と属性は、リンク予測や詐欺検出のためのMLモデルを可能にします。
LLMs can also use graph databases as structured knowledge sources for improved reasoning and question answering.
LLMsは、改善された推論や質問応答のための構造化された知識ソースとしてグラフデータベースを使用することもできます。

<!-- ここまで読んだ! -->

##### Unstructured data　 非構造化データ

Data that has a schema (a SQL table, a JSON object, or graph data) is called structured _data. 
**スキーマ（SQLテーブル、JSONオブジェクト、またはグラフデータ）を持つデータは、構造化データと呼ばれます。**
All other types of data are grouped into the antonymous category of unstructured_ _data. 
その他のすべてのデータタイプは、非構造化データという対義語のカテゴリに分類されます。
This includes text (PDFs, docs, HTML, markdown), image, video, and audio data. 
これには、テキスト（PDF、ドキュメント、HTML、マークダウン）、画像、動画、音声データが含まれます。
Unstructured data is typically stored in files, sometimes very large files of GBs of data or more, and stored in filesystems or object stores, like Amazon S3. 
非構造化データは通常、ファイルに保存され、時には数GB以上の非常に大きなファイルとして保存され、ファイルシステムやオブジェクトストア（Amazon S3など）に保存されます。
Deep learning has made huge strides in solving prediction problems with unstructured data. 
**深層学習は、非構造化データを用いた予測問題の解決において大きな進展を遂げました。**
Image tag‐ ging services, self-driving cars, voice transcription systems, and many other AI systems are all trained with vast amounts of manually labeled unstructured data.
画像タグ付けサービス、自動運転車、音声転写システム、そして多くの他のAIシステムは、すべて膨大な量の手動でラベル付けされた非構造化データで訓練されています。

##### API-scraped data　APIスクレイピングデータ

More and more data is being stored and processed in software-as-a-service (SaaS) systems, and it is, therefore, becoming more important to be able to retrieve or scrape data from such services using their public APIs. 
**ますます多くのデータがソフトウェア・アズ・ア・サービス（SaaS）システムに保存され、処理されており、そのため、これらのサービスから公開APIを使用してデータを取得またはスクレイピングできることがますます重要**になっています。
Similarly, as society is becoming increasingly digitized, more data is becoming available on websites that can be scra‐ ped and used as data sources for AI systems. 
同様に、**社会がますますデジタル化されるにつれて、ウェブサイト上でスクレイピング可能なデータが増え、AIシステムのデータソースとして使用できるようになっています**。(なるほど確かに...自社データソースだけにこだわる理由はそこまでないんだよなぁ...:thinking:)
There are low-code software systems that know about the APIs to popular SaaS platforms (like Salesforce and HubSpot) and can pull data from those platforms into data warehouses, such as Airbyte. 
SalesforceやHubSpotなどの人気のSaaSプラットフォームのAPIを知っているローコードソフトウェアシステムがあり、これらのプラットフォームからデータをデータウェアハウス（Airbyteなど）に引き込むことができます。
But sometimes, external APIs or websites will not have data integration support, and you will need to scrape the data. 
しかし、時には外部APIやウェブサイトがデータ統合サポートを持っていないことがあり、その場合はデータをスクレイピングする必要があります。
In Chapter 3, you will build an air quality prediction ML system that scrapes data from the closest public air quality sensor data source to where you live (there are tens of thousands of these available on the internet today— and one is probably closer to you than you imagine).
第3章では、あなたが住んでいる場所に最も近い公共の空気質センサーのデータソースからデータをスクレイピングする空気質予測MLシステムを構築します（今日、インターネット上にはこれらが数万件あり、あなたが想像するよりも近くにあるかもしれません）。

<!-- ここまで読んだ! -->

#### Mutable Data　 可変データ

Even though working with data is often seen as the majority of the work in building and operating ML systems, existing ML courses typically only use the simplest form of data: immutable datasets. 
**データを扱うことは、MLシステムの構築と運用における作業の大部分と見なされることが多い**ですが、既存のMLコースは通常、最も単純なデータ形式である**不変データセット(immutable datasets)**のみを使用します。
Smaller datasets (a few GBs at most) are typically stored in comma-separated values (CSV) files, while larger datasets (GBs to TBs) are usually available in a more compressible file format, such as Apache Parquet.[2]
小規模なデータセット（最大数GB）は通常、カンマ区切り値（CSV）ファイルに保存されますが、大規模なデータセット（GBからTB）は通常、Apache Parquetのようなより圧縮可能なファイル形式で利用可能です。[2]

[For example, the well-known Titanic passenger dataset consists of the following files:[3]](https://oreil.ly/3m9E8)
[例えば、よく知られたタイタニックの乗客データセットは、以下のファイルで構成されています：[3]](https://oreil.ly/3m9E8)

_train.csv_ The training set you should use to train your model
_train.csv_ モデルを訓練するために使用すべきトレーニングセット

_test.csv_ The test set you should use to evaluate the performance of your trained model
_test.csv_ 訓練したモデルの性能を評価するために使用すべきテストセット

The data is static, and your job is to train an ML model to predict whether a given passenger survives the sinking of the Titanic or not. 
**データは静的**であり、あなたの仕事は、特定の乗客がタイタニックの沈没から生き残るかどうかを予測するMLモデルを訓練することです。
Your first task is to perform basic feature engineering on the data. 
最初のタスクは、データに対して基本的な特徴エンジニアリングを行うことです。
For example, there are some missing values that you need to fill in (or impute), and you need to remove columns that have no power to predict whether a given passenger survives the sinking of the _Titanic or not. 
例えば、埋める必要のある欠損値がいくつかあり、特定の乗客がタイタニックの沈没から生き残るかどうかを予測する力を持たない列を削除する必要があります。
The_ _Titanic dataset is popular, as you can learn the basics of data cleaning, transforming_ data into features, and fitting a model to the data.
_タイタニックデータセットは人気があり、データクリーニングの基本、データを特徴に変換すること、そしてデータにモデルを適合させることを学ぶことができます。

Immutable files are not suitable as the data layer of record in an enterprise where the EU’s General Data Protection Regulation (GDPR) or the California Consumer Privacy Act (CCPA) requires that users are allowed to have their data deleted and updated and its usage and provenance tracked.
不変ファイルは、EUの一般データ保護規則（GDPR）やカリフォルニア州消費者プライバシー法（CCPA）が、ユーザーにデータの削除や更新を許可し、その使用と出所を追跡することを要求する企業の記録データ層としては適していません。

There are, however, no new passengers arriving for the Titanic. 
**ただし、タイタニックには新しい乗客が到着することはありません。**
So you don’t have to worry about adding new passengers to the dataset as they arrive, removing a passen‐ ger from the dataset because of a GDPR request from a close relative, or selecting a subset of the available passengers as training data because you can’t or don’t want to train your model on all available data. 
したがって、到着する新しい乗客をデータセットに追加したり、近親者からのGDPRリクエストに基づいてデータセットから乗客を削除したり、すべての利用可能なデータでモデルを訓練できない、または訓練したくないために利用可能な乗客のサブセットをトレーニングデータとして選択したりすることを心配する必要はありません。
You will also need to re-create the training and test sets from whatever rows you select as your training data.
また、トレーニングデータとして選択した行からトレーニングセットとテストセットを再作成する必要があります。

<!-- ここまで読んだ! -->

Production ML systems typically work with _mutable data. 
**プロダクションMLシステムは通常、mutable dataを扱います。**
Mutable data is typically_ stored in a row-oriented or column-oriented store and supports efficient inserts, appends, updates, and deletions. 
可変データは通常、行指向または列指向ストアに保存され、効率的な挿入、追加、更新、および削除をサポートします。
This introduces challenges for data scientists who have only used Python to read and write feature data. 
これにより、特徴データを読み書きするためにPythonのみを使用してきたデータサイエンティストにとっての課題が生じます。
In the past, they had to learn SQL and work directly with the database, but now, they can also read/write mutable data using Python and DataFrame APIs, which is the main focus of this book.
過去には、SQLを学び、データベースと直接作業する必要がありましたが、現在ではPythonとDataFrame APIを使用して可変データを読み書きすることもでき、これが本書の主な焦点です。

---

補足: 
2 Parquet files store tabular data in a columnar format—the values for each column are stored together, ena‐ bling faster aggregate operations at the column level (such as the average value for a numerical column) and [better compression, with both dictionary and run-length encoding.](https://oreil.ly/bEjOI)
2 Parquetファイルは、表形式データを列指向形式で保存します—各列の値は一緒に保存され、列レベルでの集約操作（数値列の平均値など）を高速化し、[辞書とランレングスエンコーディングの両方でより良い圧縮を実現します。](https://oreil.ly/bEjOI)

3 The Titanic dataset is a well-known example of a binary classification problem in ML, where you have to train a model to predict whether a given passenger will survive or not.  
3 タイタニックデータセットは、特定の乗客が生き残るかどうかを予測するモデルを訓練する必要があるMLのバイナリ分類問題のよく知られた例です。

---

Mutable data introduces challenges for feature engineering.
**可変データは、特徴エンジニアリングに課題をもたらします。**
There are many data transformations—such as aggregations, binning, and dimensionality reduction, and traditionally called “data preparation steps”—that can be performed before storing feature data in databases (or feature stores). 
多くのデータ変換—集約、ビニング、次元削減など、伝統的に「データ準備ステップ」と呼ばれるもの—は、特徴データをデータベース（または特徴ストア）に保存する前に実行できます。
However, there are also data transforma‐ tions, such as encoding (categorical) strings into a numerical representation and nor‐ malizing numerical variables, that are parameterized by the training data. 
しかし、（カテゴリカル）文字列を数値表現にエンコードしたり、数値変数を正規化したりするなど、トレーニングデータによってパラメータ化されるデータ変換もあります。
As you don’t know what the training data is until you select it and read from your data store, these data transformations happen after reading from the data store. 
データストアから選択して読み取るまでトレーニングデータが何であるかはわからないため、これらのデータ変換はデータストアから読み取った後に発生します。
In Chapter 2, we introduce a taxonomy of data transformations for ML that helps you identify whether you should perform data transformations before saving feature data or after reading data from the feature store. 
第2章では、MLのためのデータ変換の分類法を紹介し、**特徴データを保存する前にデータ変換を実行するか、特徴ストアからデータを読み取った後に実行するかを特定**するのに役立てます。
In Chapters 6 and 7, we dive into the details of data transformations to create features for batch, real-time, and LLM ML systems.
第6章と第7章では、バッチ、リアルタイム、およびLLM MLシステムのための特徴を作成するためのデータ変換の詳細に深く掘り下げます。

<!-- ここまで読んだ! -->

### A Brief History of Machine Learning Systems　機械学習システムの簡単な歴史

In the mid-2010s, revolutionary ML systems started appearing in consumer internet applications, such as image tagging in Facebook and Google Translate. 
**2010年代中頃、革命的なMLシステムがFacebookの画像タグ付けやGoogle翻訳などの消費者向けインターネットアプリケーションに登場し始めました。** (それくらいの時期なんだ...! :thinking:)
The first generation of ML systems were either batch ML systems that made predictions on a schedule (see Figure 1-1) or interactive online ML systems that made predictions in response to user actions.
最初の世代のMLシステムは、スケジュールに基づいて予測を行うバッチMLシステム（図1-1を参照）またはユーザーのアクションに応じて予測を行うインタラクティブなオンラインMLシステムのいずれかでした。

![]()
_Figure 1-1. A monolithic batch ML system that can run in either training mode or inference mode._
_図1-1. トレーニングモードまたは推論モードのいずれかで実行できるモノリシックなバッチMLシステム。_

A challenge in building batch ML systems is to ensure that the features created for training data and the features created for batch inference are consistent. 
**バッチMLシステムを構築する際の課題は、トレーニングデータのために作成された特徴とバッチ推論のために作成された特徴が一貫していることを保証すること**です。
This can be achieved by building a batch program (or pipeline) that is run in either training mode or inference mode. 
これは、トレーニングモードまたは推論モードのいずれかで実行されるバッチプログラム（またはパイプライン）を構築することで達成できます。
The monolithic architecture ensures the same “Create Features” code is run to create training data (from historical data) and inference data (from new data).  
モノリシックアーキテクチャは、トレーニングデータ（履歴データから）と推論データ（新しいデータから）を作成するために同じ「特徴を作成する」コードが実行されることを保証します。

<!-- ここまで読んだ! -->

In Figure 1-2, you can see an interactive ML system that receives requests from clients and responds with predictions in real time. 
図1-2では、クライアントからのリクエストを受け取り、リアルタイムで予測に応答するインタラクティブなMLシステムを見ることができます。
In this architecture, you need two separate systems—an offline training pipeline and an online model-serving service.
このアーキテクチャでは、オフラインのトレーニングパイプラインとオンラインのモデル提供サービスという2つの別々のシステムが必要です。
You can no longer ensure consistent features between training and inference by having a single monolithic program. 
**単一のモノリシックプログラムを持つことで、トレーニングと推論の間で一貫した特徴を保証することはできなくなります。**
Early solutions to this problem involved versioning the feature creation source code and ensuring that both training and serving use the same version.
この問題に対する初期の解決策は、特徴作成のソースコードのバージョン管理を行い、トレーニングと提供の両方が同じバージョンを使用することを保証することでした。

![]()
_Figure 1-2. A (real-time) interactive ML system requires a separate offline training system from the online inference systems. Notice that the online inference pipeline is stateless. We will see later that stateful online inference pipelines require adding a feature store to this architecture._
_図1-2. （リアルタイム）インタラクティブMLシステムは、オンライン推論システムとは別のオフライントレーニングシステムを必要とします。オンライン推論パイプラインはステートレスであることに注意してください。後で、ステートフルなオンライン推論パイプラインには、このアーキテクチャにフィーチャーストアを追加する必要があることを見ていきます。_

Stateless online ML systems were, and still are, useful in some cases. 
**ステートレスオンラインMLシステム**は、いくつかのケースで有用でしたし、今でも有用です。
For example, an image tagging program can take a photo as input, and an image classification model predicts the bounding boxes and labels for objects identified in the image. 
例えば、画像タグ付けプログラムは写真を入力として受け取り、画像内で識別されたオブジェクトのバウンディングボックスとラベルを予測する画像分類モデルがあります。
The first chatbots that used LLMs were stateless online ML systems. 
**LLMを使用した最初のチャットボットは、ステートレスオンラインMLシステムでした。**
The chatbot server received user input as a prediction request and appended the user input to a system prompt. 
チャットボットサーバーは、ユーザー入力を予測リクエストとして受け取り、ユーザー入力をシステムプロンプトに追加しました。
The system prompt was the text, added by the chatbot developer, that typically instructed the LLM to be helpful, not abusive, and not to reveal sensitive information. 
システムプロンプトは、チャットボット開発者によって追加されたテキストで、通常はLLMに対して役立つように、攻撃的でないように、そして機密情報を明らかにしないように指示しました。
The combined prompt was then sent to an LLM that returned a response. 
その後、結合されたプロンプトがLLMに送信され、応答が返されました。
LLM responses were simply predictions of the most probable sequence of characters that follow the combined prompt.
LLMの応答は、結合されたプロンプトに続く最も可能性の高い文字のシーケンスの予測に過ぎませんでした。

Stateless online ML systems are, however, limited by their training data. 
**しかし、ステートレスオンラインMLシステムは、そのトレーニングデータによって制限されています。**
The image classifier can only identify objects from the fixed number of labels in its training data. 
画像分類器は、トレーニングデータにある固定された数のラベルからのみオブジェクトを識別できます。
The chatbot cannot answer questions about events that happened after the creation of its training data. 
**チャットボットは、トレーニングデータの作成後に発生したイベントに関する質問に答えることができません。**
You can overcome this limitation by providing history and context information as input into a model. 
**この制限を克服するためには、履歴とコンテキスト情報をモデルへの入力として提供することができます。**
For example, an online recommender model could take as input recent products you viewed or liked in order to predict products to recommend to you. 
例えば、オンラインレコメンダーモデルは、最近あなたが閲覧したり好んだ製品を入力として受け取り、あなたに推奨する製品を予測することができます。
That is, passing your recent history as input features is sufficient for the model to make predictions with recent data—you don’t need to retrain the model with information about your recent orders. 
**つまり、最近の履歴を入力特徴量として渡すことは、モデルが最近のデータで予測を行うのに十分です—最近の注文に関する情報でモデルを再トレーニングする必要はありません。**
Similarly, we will see that you can also retrieve and add context information to an LLM’s prompt so that it can answer questions about events that happened after its training cutoff time. 
同様に、LLMのプロンプトにコンテキスト情報を取得して追加することで、トレーニングのカットオフ時間以降に発生したイベントに関する質問に答えることができることも見ていきます。
For example, an LLM trained in 2024 could tell you who won the 2025 NBA finals if you include in the prompt the Wikipedia article about the 2025 NBA finals.
例えば、2024年にトレーニングされたLLMは、2025年NBAファイナルに関するWikipedia記事をプロンプトに含めれば、2025年NBAファイナルの勝者を教えてくれるでしょう。

<!-- ここまで読んだ! -->

But where does this context and history come from? 
**しかし、このコンテキストと履歴はどこから来るのでしょうか？**
The client requesting the prediction can pass it as parameters, but more often than not, the client is an application whose state is stored in a database. 
予測をリクエストするクライアントは、それをパラメータとして渡すことができますが、クライアントはデータベースに状態が保存されているアプリケーションであることが多いです。
For example, our recommender model may need input features created from a user’s recent activity and historical orders. 
**例えば、私たちのレコメンダーモデルは、ユーザーの最近の活動や履歴注文から作成された入力特徴を必要とするかもしれません。**
But the source data for the features can’t be sent by the client, as it is stored in the client’s database. 
しかし、特徴のためのソースデータはクライアントのデータベースに保存されているため、クライアントによって送信することはできません。
What if, instead, the features were created and stored by a separate stateful system and the online model could just read those features when a prediction request arrived?
**代わりに、特徴量が別のステートフルシステムによって作成され保存され、オンラインモデルが予測リクエストが到着したときにそれらの特徴を読み取ることができたらどうでしょうか？**

<!-- ここまで読んだ! -->

The general problem of building stateful online ML systems was first addressed by feature stores, which were introduced as a new category of platform by Uber in 2017, [with their article on their internal Michelangelo platform. Feature stores manage the](https://oreil.ly/k5_DV) transformation and storage of context and history as features that can be easily used by online models (see Figure 1-3).
ステートフルなオンラインMLシステムを構築するという一般的な問題は、2017年にUberによって新しいプラットフォームカテゴリとして導入されたフィーチャーストアによって最初に対処されました。[彼らの内部Michelangeloプラットフォームに関する記事で。フィーチャーストアは、オンラインモデルで簡単に使用できる特徴として、コンテキストと履歴の変換と保存を管理します（図1-3を参照）。](https://oreil.ly/k5_DV) (図1-3参照)
(ウーバーさんのFeature Storeのブログって、こういうステートフルなリアルタイムMLシステムの文脈だったのか...!!:thinking:)

![]()
_Figure 1-3. Many (real-time) interactive ML systems also require history and context to make personalized predictions. The feature store enables personalized history and context to be retrieved at low latency as precomputed features for online models._
_図1-3. 多くの（リアルタイム）インタラクティブMLシステムは、パーソナライズされた予測を行うために履歴とコンテキストを必要とします。フィーチャーストアは、オンラインモデルのための事前計算された特徴としてパーソナライズされた履歴とコンテキストを低遅延で取得できるようにします。_

<!-- ここまで読んだ! -->

A feature pipeline reads historical or new data from one or more data sources, transforms it into features, and stores the feature data in the feature store. 
**フィーチャーパイプラインは、1つまたは複数のデータソースから履歴データまたは新しいデータを読み取り、それを特徴に変換し、フィーチャーストアに特徴データを保存します。**
Online inference programs use API calls to retrieve the precomputed feature data that is then passed to models for online predictions. 
オンライン推論プログラムは、API呼び出しを使用して事前計算された特徴データを取得し、それをモデルに渡してオンライン予測を行います。
As the feature store collects feature data over time, it is also used to create training data for training models. 
フィーチャーストアは時間の経過とともに特徴データを収集するため、モデルのトレーニングのためのトレーニングデータを作成するためにも使用されます。
Feature pipelines can be batch programs that run on a schedule, but feature data can then only be as fresh as the most recent run. 
**フィーチャーパイプラインは、スケジュールに基づいて実行されるバッチプログラムであることがありますが、フィーチャーデータは最も最近の実行の新鮮さに制限されます**。(うんうん...ストリーミングプログラムじゃない限り...!:thinking:)
If you need to make very recent events (such as user activity in the last 10 minutes) available as features, you can write a feature pipeline as a stream processing program. 
**非常に最近のイベント（例えば、過去10分間のユーザー活動）を特徴として利用可能にする必要がある場合、フィーチャーパイプラインをストリーム処理プログラムとして記述することができます。** (うんうん...!:thinking:)
Batch and streaming feature pipelines are covered in Chapters 8 and 9, while feature stores and data transformations are explored in Chapters 4 to 7.
バッチおよびストリーミングフィーチャーパイプラインは第8章と第9章で扱われ、フィーチャーストアとデータ変換は第4章から第7章で探求されます。
The term ML pipeline is a collective term that refers to any of the feature pipelines, training pipelines, and inference pipelines that make up the ML system.
**MLパイプラインという用語は、MLシステムを構成するフィーチャーパイプライン、トレーニングパイプライン、および推論パイプラインのいずれかを指す総称です。** (あ、これ今後のブログで引用できる文言だ...!!:thinking:)

<!-- ここまで読んだ! -->

Stateless LLM applications, such as the first chatbots, faced a challenge similar to that faced by stateless ML systems—they needed to incorporate relevant and timely context as input, not just for events that happened after the training data cutoff time but also for private data not scraped by LLMs for training. 
**最初のチャットボットのようなステートレスLLMアプリケーションは、ステートレスMLシステムが直面したのと同様の課題に直面しました—彼らは、トレーニングデータのカットオフ時間以降に発生したイベントだけでなく、トレーニングのためにLLMによってスクレイピングされなかったプライベートデータに対しても、関連性がありタイムリーなコンテキストを入力として組み込む必要がありました。**(なるほど確かに...!! :thinking:)
The solution was to include context data, retrieved at request time, in system prompts. 
解決策は、リクエスト時に取得されたコンテキストデータをシステムプロンプトに含めることでした。(chipさんが言うところの「context-construction」ってやつか...!!:thinking:)
The first such approach to gain widespread adoption was RAG using a vector database (see Figure 1-4).
広く採用された最初のアプローチは、ベクターデータベースを使用したRAGでした（図1-4を参照）。(うんうん...!:thinking:)

_Figure 1-4. LLM systems can retrieve relevant context data at request time and add the context data to the prompt in a process known as retrieval-augmented generation (RAG)._
_図1-4. LLMシステムは、リクエスト時に関連するコンテキストデータを取得し、リトリーバル拡張生成（RAG）として知られるプロセスでプロンプトにコンテキストデータを追加できます。_

<!-- ここまで読んだ! -->

The first RAG-powered LLM applications took the user input as a string and queried a vector database with the input string, returning chunks of text similar to the input using approximate nearest neighbor (ANN) search. 
最初のRAG駆動のLLMアプリケーションは、ユーザ入力を文字列として受け取り、入力文字列でベクターデータベースにクエリを実行し、近似最近傍（ANN）検索を使用して入力に類似したテキストのチャンクを返しました。(うんうんまさに...!:thinking:)
Any context information you wanted to include in the system prompt must first have been written to the vector database, and you needed a vector embedding pipeline to keep that data up to date.
**システムプロンプトに含めたいコンテキスト情報は、最初にベクターデータベースに書き込まれている必要があり、そのデータを最新の状態に保つためにはベクター埋め込みパイプラインが必要でした。**
The pipeline transformed the source data into chunks of text that were then transformed into vector embeddings using an embedding model. 
パイプラインは、ソースデータをテキストのチャンクに変換し、それを埋め込みモデルを使用してベクター埋め込みに変換しました。
The vector embeddings were then written to a vector index so they could later be used for ANN search. 
その後、ベクター埋め込みはベクターインデックスに書き込まれ、後でANN検索に使用できるようにされました。
The system prompt was then no longer static, as it was a prompt template with both instructions and empty slots that were filled in with text retrieved from the vector index. 
**システムプロンプトはもはや静的ではなく、指示とベクターインデックスから取得されたテキストで埋められた空のスロットを持つプロンプトテンプレートになりました。**(うんうん確かに...!:thinking:)
The prompt was also finite in size and defined by the LLM’s context window.
プロンプトはサイズが有限であり、LLMのコンテキストウィンドウによって定義されていました。
The context window stores both the input and output of the LLM, and recent LLMs have a context window of anything from a few KBs to a few MBs in size. 
コンテキストウィンドウはLLMの入力と出力の両方を保存し、最近のLLMは数KBから数MBのサイズのコンテキストウィンドウを持っています。
The challenge of preparing and retrieving context data for LLMs is known as context engineering. 
**LLMのためのコンテキストデータを準備し取得する課題は、コンテキストエンジニアリングとして知られています。**
The goal of context engineering is to construct a prompt from user input and context data that maximizes the performance of the LLM’s output for a given input.
**コンテキストエンジニアリングの目標は、ユーザ入力とコンテキストデータからプロンプトを構築し、特定の入力に対するLLMの出力のパフォーマンスを最大化することです。** (なるほど...!:thinking:)

<!-- ここまで読んだ! -->

The first LLM applications were tightly focused assistants that helped in coding, answering medical questions, and even creating cooking recipes. 
最初のLLMアプリケーションは、コーディング、医療質問への回答、さらには料理レシピの作成を支援することに特化したアシスタントでした。
As LLM applications took on increasingly complex tasks, they required more autonomy in what data to query and what tasks to execute. 
**LLMアプリケーションがますます複雑なタスクを引き受けるようになると、どのデータをクエリし、どのタスクを実行するかについてより多くの自律性が必要になりました。**
Agents are a class of LLM application that have a level of autonomy in how to query diverse data sources (vector indexes, search engines, feature stores, etc.) to retrieve relevant context data and how to plan and execute tasks to achieve goals. 
エージェントは、関連するコンテキストデータを取得するために多様なデータソース（ベクターインデックス、検索エンジン、フィーチャーストアなど）をクエリする方法や、目標を達成するためにタスクを計画し実行する方法において自律性を持つLLMアプリケーションのクラスです。
Anthropic defines agents as “systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.” 
**Anthropicはエージェントを「LLMが自らのプロセスとツールの使用を動的に指揮し、タスクを達成する方法を制御するシステム」と定義**しています。(これもブログ記事書く時に引用できそう...!:thinking:)
Agents represent a paradigm shift from human-machine interaction to primarily machine-machine interaction. 
エージェントは、**人間と機械の相互作用から主に機械と機械の相互作用へのパラダイムシフト**を表しています。
Users set high-level goals, and developers provide agents with the tools and context required to achieve those goals.
ユーザーは高レベルの目標を設定し、開発者はエージェントがそれらの目標を達成するために必要なツールとコンテキストを提供します。

<!-- ここまで読んだ! -->

Figure 1-5 shows how LLM RAG applications evolved to agentic AI systems where online inference programs have become agent programs. 
図1-5は、LLM RAGアプリケーションがエージェントAIシステムに進化し、オンライン推論プログラムがエージェントプログラムになった様子を示しています。
Agents have a unified standard, called Model Context Protocol (MCP), for retrieving RAG data from a variety of data sources and using internal and external APIs as tools.
エージェントは、さまざまなデータソースからRAGデータを取得し、内部および外部APIをツールとして使用するための統一された標準であるモデルコンテキストプロトコル（MCP）を持っています。

![]()
_Figure 1-5. Agents require the same data processing pipelines to prepare context data for use in LLMs, but they have more autonomy in deciding on what actions to take to execute tasks._
_図1-5. エージェントは、LLMで使用するためのコンテキストデータを準備するために同じデータ処理パイプラインを必要としますが、タスクを実行するためにどのアクションを取るかを決定する際により多くの自律性を持っています。_

In both LLM application and agent architectures, the training of LLMs is optional, but it can be added by fine-tuning a foundation LLM using instruction data from a feature store; see Chapter 10. 
**LLMアプリケーションとエージェントアーキテクチャの両方において、LLMのトレーニングはオプション**ですが、フィーチャーストアからの指示データを使用して基盤となるLLMをファインチューニングすることで追加できます；第10章を参照してください。
You’ll encounter the same engineering challenges with agents as with ML systems, such as how to precompute context data and vector embeddings and make them queryable.
**エージェントにおいても、MLシステムと同様のエンジニアリングの課題に直面します。例えば、コンテキストデータとベクター埋め込みを事前計算し、それらをクエリ可能にする方法**などです
We cover vector embedding pipelines in Chapters 5 and 6 and RAG and context engineering in Chapter 12. 
ベクトル埋め込みパイプラインについては第5章と第6章で、RAGとコンテキストエンジニアリングについては第12章で説明します。 

<!-- ここまで読んだ! -->

---
(補足)
Is it an ML system or an AI system? 
これはMLシステムですか、それともAIシステムですか？ 
An ML system is a type of AI system that learns from data through ML algorithms and statistical models. 
**MLシステムは、MLアルゴリズムと統計モデルを通じてデータから学習するAIシステムの一種**です。 
AI is a broader term that also covers search, memory, and many of the techniques used to build agents. 
AIはより広い用語で、検索、メモリ、エージェントを構築するために使用される多くの技術も含まれます。 
As such, we often use the terms batch ML system, real-time ML system, and agentic AI system to describe different AIs. 
**そのため、バッチMLシステム、リアルタイムMLシステム、エージェントAIシステムという用語を使って異なるAIを説明することがよくあります。 **
We will use the most general term, AI system, except in cases where we refer to a specific class of ML system. 
特定のMLシステムのクラスを指す場合を除いて、最も一般的な用語であるAIシステムを使用します。 

<!-- ここまで読んだ! -->

### MLOps and LLMOps

The evolution of ML system architectures described here, from stateless to stateful systems, did not happen in a vacuum. 
ここで説明するMLシステムアーキテクチャの進化は、ステートレスからステートフルシステムへのものであり、真空の中で起こったわけではありません。
It happened within a new field of ML engineering called machine learning operations (MLOps) that can be dated back to 2015, [when authors at Google published a canonical paper entitled “Hidden Technical Debt](https://oreil.ly/oeHjv) in Machine Learning Systems”. 
それはMLエンジニアリングの新しい分野
(MLOpsって2015年からなんだ...!もう10年、まだ10年??:thinking:)
The paper cemented in ML developers’ minds the](https://oreil.ly/oeHjv) adage that only a small percentage of the work in building ML systems is training models. 
この論文は、MLシステムを構築する作業の中で、モデルのトレーニングはほんの一部であるという格言をML開発者の心に定着させました。(有名な図のやつね! :thinking:)
Most of the work is in data management and building and operating the ML system infrastructure. 
**ほとんどの作業はデータ管理やMLシステムインフラの構築と運用にあります。** 

Inspired by the DevOps movement in software engineering, 
ソフトウェアエンジニアリングにおけるDevOps運動に触発され、 
MLOps is a set of practices and processes for building reliable and scalable ML systems that can be quickly and incrementally developed, tested, and rolled out to production using automation where possible. 
MLOpsは、信頼性が高くスケーラブルなMLシステムを構築するための一連の実践とプロセスであり、可能な限り自動化を使用して迅速かつ段階的に開発、テスト、運用に展開できます。 
MLOps practices should help you tighten the development loop and shorten the time that it takes you to make changes to software or data, test your changes, and then deploy those changes to production. 
MLOpsの実践は、開発ループを短縮し、ソフトウェアやデータの変更を行い、その変更をテストし、運用に展開するまでの時間を短縮するのに役立つはずです。 
Many developers with a data science background are intimidated by the systems focus of MLOps on automation, testing, and operations. 
データサイエンスのバックグラウンドを持つ多くの開発者は、MLOpsの自動化、テスト、運用に対するシステムの焦点に圧倒されます。 
In contrast, DevOps’ North Star is to get to a minimum viable product (MVP) as fast as possible and then iteratively improve that MVP. 
**対照的に、DevOpsの北極星は、できるだけ早く最小限の実用的製品（MVP）に到達し、その後そのMVPを反復的に改善することです。**
In Chapter 2, we will introduce our process for building an MVP. 
第2章では、MVPを構築するためのプロセスを紹介します。 

<!-- ここまで読んだ! -->

---
(補足)
4 Wikipedia states that DevOps integrates and automates the work of software development (Dev) and IT operations (Ops) as a means for improving and shortening the systems development life cycle.  
4 Wikipediaによれば、DevOpsはソフトウェア開発（Dev）とIT運用（Ops）の作業を統合し自動化することで、システム開発ライフサイクルを改善し短縮する手段です。 

-----

The journey from building an MVP to having a reliable ML system involves more levels of testing than those for a traditional software system. 
MVPを構築することから信頼性のあるMLシステムを持つことへの旅は、従来のソフトウェアシステムのテストよりも多くのレベルのテストを含みます。 
Small bugs in either input data or code can easily cause an ML model to make incorrect predictions. 
**入力データやコードの小さなバグが、MLモデルが不正確な予測をする原因となることがあります。** 
ML systems require significant engineering effort to test and ensure that they produce high-quality predictions that are free from bias. 
MLシステムは、高品質でバイアスのない予測を生成することを確認するために、重要なエンジニアリング作業を必要とします。
Testing occurs at all stages in ML system development, from feature engineering to model training to model deployment. 
テストは、特徴エンジニアリングからモデルのトレーニング、モデルのデプロイメントまで、MLシステム開発のすべての段階で行われます。 
In traditional software systems, you have to test the code and integrations. 
**従来のソフトウェアシステムでは、コードと統合(integration)をテストする必要**があります。 
In ML systems, you also need tests and monitoring for both input data and models. 
**MLシステムでは、入力データとモデルの両方に対してもテストと監視が必要**です。

<!-- ここまで読んだ! -->

Tests that are run at development time include: 
**開発時に実行されるテスト**には以下が含まれます: 

- _Unit tests_ These validate feature logic (changes to feature logic can pollute training data). 
  - _単体テスト_ これらは特徴ロジックを検証します（特徴ロジックの変更はトレーニングデータを汚染する可能性があります）。 
- _Integration tests_ These validate ML pipelines, helping catch errors in your Python code. 
  - _統合テスト_ これらはMLパイプラインを検証し、Pythonコードのエラーをキャッチするのに役立ちます。 
- _Model validation tests_ These check for good performance and bias. 
  - _モデル検証テスト_ これらは良好なパフォーマンスとバイアスをチェックします。 
- _Evals_ These are for safety, reliability, and performance of LLM applications and agents. 
  - _評価_ これらはLLMアプリケーションとエージェントの安全性、信頼性、パフォーマンスのためのものです。 

<!-- ここまで読んだ! -->

Monitoring and tests run in production ML include: 
**ML運用で実行される監視とテスト**には以下が含まれます:

- _Data validation tests_ These prevent bad data from entering your system. 
  - _データ検証テスト_ これらは悪いデータがシステムに入るのを防ぎます。 
- _Model performance monitoring_ Most models degrade in performance over time. 
  - _モデルパフォーマンス監視_ ほとんどのモデルは時間とともにパフォーマンスが低下します。 
- _Feature drift detection_ This checks whether the input data at inference time is statistically significantly different from the model’s training data. 
  - _特徴ドリフト検出_ これは、推論時の入力データがモデルのトレーニングデータと統計的に有意に異なるかどうかをチェックします。 
- _A/B tests_ These are run for new versions of models before rolling them out to production. 
  - _A/Bテスト_ これらは新しいモデルのバージョンを運用に展開する前に実行されます。 
- _Guardrails_ These are run for LLM inputs and outputs to prevent harmful responses. 
  - _ガードレール_ これらはLLMの入力と出力に対して有害な応答を防ぐために実行されます。 

This list of tests and checks for ML systems has grown in parallel with the formation of MLOps communities that are aligning around a shared set of values and beliefs. 
MLシステムのためのテストとチェックのリストは、共通の価値観と信念に基づいて整列するMLOpsコミュニティの形成と並行して成長しています。 
What are their MLOps principles?  
彼らのMLOpsの原則は何ですか？ 

<!-- ここまで読んだ! -->

MLOps folks believe that testing should have minimal friction on your development speed. 
MLOpsの人々は、テストが開発速度に最小限の摩擦を持つべきだと信じています。 
Automating the execution of your tests helps improve your productivity. 
テストの実行を自動化することで、生産性が向上します。 
There are many continuous integration (CI) platforms for the automated execution of development tests. 
開発テストの自動実行のための多くの継続的インテグレーション（CI）プラットフォームがあります。 
Popular platforms for CI are GitHub Actions, Jenkins, and Azure DevOps. 
CIの人気プラットフォームには、GitHub Actions、Jenkins、Azure DevOpsがあります。 
CI is not a prerequisite for starting to build ML systems. 
CIはMLシステムの構築を開始するための前提条件ではありません。 
If you have a data science background, comprehensive testing is something you may not have experience with, and it is OK to take time to incrementally add testing to both your arsenal and the ML systems you build. 
データサイエンスのバックグラウンドがある場合、包括的なテストは経験がないかもしれませんが、**あなたの武器と構築するMLシステムの両方にテストを段階的に追加するために時間をかけることは問題ありません。**
You can start with unit tests for functions, model performance and bias testing in your training pipelines, and integration tests for all of your ML pipelines. 
関数の単体テスト、トレーニングパイプラインでのモデルパフォーマンスとバイアスのテスト、すべてのMLパイプラインの統合テストから始めることができます。 
You can automate your tests by adding CI support to run your tests whenever you push code to your source code repository. 
コードをソースコードリポジトリにプッシュするたびにテストを実行するCIサポートを追加することで、テストを自動化できます。
You can add automated tests after you have validated that your MVP is worth maintaining. 
**MVPが維持する価値があると確認した後に、自動テストを追加できます。**

<!-- ここまで読んだ! -->

MLOps folks love that feeling when you push changes in your source code and your ML artifact or system is automatically deployed. 
**MLOpsの人々は、ソースコードに変更をプッシュし、MLアーティファクトやシステムが自動的にデプロイされる感覚が大好きです。**
Deployments are often associated with the concept of development (dev), preproduction (preprod), and production (prod) environments. 
デプロイメントは、開発（dev）、プレプロダクション（preprod）、およびプロダクション（prod）環境の概念に関連付けられることがよくあります。 
ML assets are developed in the dev environment, tested in preprod, and tested again before deployment in the prod environment. 
ML資産はdev環境で開発され、preprodでテストされ、prod環境でデプロイメント前に再度テストされます。 
Although a human may ultimately have to sign off on deploying an ML artifact to production, the steps should be automated in a process known as continuous deployment (CD). 
最終的には人間がMLアーティファクトをプロダクションにデプロイすることを承認する必要があるかもしれませんが、その手順は継続的デプロイメント（CD）として知られるプロセスで自動化されるべきです。 
In this book, we work with the philosophy that you can build, test, and run your whole ML system in dev, preprod, or prod environments. 
この本では、dev、preprod、またはprod環境で全体のMLシステムを構築、テスト、実行できるという哲学で作業します。 
The data your ML system can access may be dependent on which environment you deploy in (dev may not have access to production data). 
MLシステムがアクセスできるデータは、デプロイする環境によって異なる場合があります（devはプロダクションデータにアクセスできないかもしれません）。 
We will look at CD in detail in Chapter 13. 
第13章ではCDについて詳しく見ていきます。

<!-- ここまで読んだ! -->

MLOps folks generally live by the well-known database community maxim of “garbage in, garbage out.” 
MLOpsの人々は一般的に「**ゴミが入ればゴミが出る(garbage in, garbage out)**」というデータベースコミュニティの格言に従っています。 
Many ML systems use data that has few or no guarantees on its quality, and blindly ingesting garbage data can lead to very well-trained models that still predict garbage. 
**多くのMLシステムは、その品質に対する保証がほとんどないか全くないデータを使用しており、盲目的にゴミデータを取り込むことは、非常に良く訓練されたモデルが依然としてゴミを予測する原因となります。**
In Chapter 6, we will design and write data validation tests for feature pipelines. 
第6章では、特徴パイプラインのためのデータ検証テストを設計し、記述します。 
We will detail the mitigating actions you can take if you identify data as incorrect, missing, or corrupt. 
データが不正確、欠落、または破損していると特定した場合に取ることができる緩和策について詳しく説明します。 

<!-- ここまで読んだ! -->

MLOps folks dream of a big green button for upgrading the system and a big red button for rolling back a problematic upgrade. 
MLOpsの人々は、システムをアップグレードするための大きな緑のボタンと、問題のあるアップグレードを元に戻すための大きな赤のボタンを夢見ています。 
Versioning of both features and models is a necessary prerequisite for both A/B testing and upgrading/downgrading an ML system without downtime. 
**特徴量とモデルのバージョン管理は、A/BテストとダウンタイムなしでMLシステムをアップグレード/ダウングレードするための必要な前提条件**です。 
Versioning enables you to quickly roll back your changes to a working earlier version of the model and the versioned features that feed it. 
バージョン管理により、変更をモデルの動作する以前のバージョンと、それに供給するバージョン管理された特徴量に迅速にロールバックできます。 

<!-- ここまで読んだ! -->

MLOps folks don’t like the surprises that arise when a new version of their LLM or [agent (like a version of Amazon Q, a coding agent, that could wipe users’ filesystems](https://oreil.ly/qO2z3) [clean!) introduces unexpected behavior. 
MLOpsの人々は、新しいバージョンのLLMや[エージェント（ユーザーのファイルシステムを消去する可能性のあるAmazon Qのバージョンのような）が予期しない動作を引き起こすときに生じる驚きを好みません。
In Chapter 13, we will look at designing and](https://oreil.ly/qO2z3) running evals to evaluate changes to your LLM applications and agents before they go into production.  
第13章では、LLMアプリケーションとエージェントの変更を運用に入れる前に評価するための評価を設計し、実行する方法を見ていきます。

<!--  ここまで読んだ! -->

MLOps folks love to know how their systems are performing. 
**MLOpsの人々は、自分たちのシステムがどのように機能しているかを知ることが大好き**です。 
A production AI system should collect metrics to build dashboards and alerts for:
本番AIシステムは、ダッシュボードとアラートを構築するためのメトリクスを収集する必要があります：

- Monitoring the quality of your models’ predictions with respect to some business key performance indicator (KPI) 
  - いくつかのビジネスの主要業績評価指標（KPI）に関するモデルの予測の質を監視すること 
- Monitoring newly arriving data for drift 
  - 新しく到着するデータのドリフトを監視すること 
- Measuring the performance (throughput and latency) of your ML platform (model serving, feature store, vector index, LLMs, and ML pipelines) 
  - MLプラットフォーム（モデル提供、特徴ストア、ベクトルインデックス、LLM、MLパイプライン）のパフォーマンス（スループットとレイテンシ）を測定すること

<!-- ここまで読んだ! -->
 
MLOps folks need logs from operational services to debug and improve AI systems. 
MLOpsの人々は、**AIシステムをデバッグし改善するために運用サービスからのログが必要**です。 
Eyeballing model logs is a powerful technique for error analysis in LLMs, as described in Chapter 14. 
モデルログを目視で確認することは、LLMにおけるエラー分析のための強力な手法です（第14章で説明します）。 
They also need logs to debug errors and understand model performance in classical ML systems. 
彼らはまた、エラーをデバッグし、従来のMLシステムにおけるモデルのパフォーマンスを理解するためのログが必要です。 

<!-- ここまで読んだ! -->

Be warned. 
警告します。 
This book takes a nontraditional approach to MLOps.
**この本はMLOpsに対して非伝統的なアプローチを取ります。**
You will not learn Terraform to program infrastructure as code, how to write Dockerfiles and containerize pipelines, or how to become a Kubernetes whiz.
インフラをコードとしてプログラムするためのTerraformの使い方、Dockerfileの書き方やパイプラインのコンテナ化、Kubernetesの達人になる方法を学ぶことはありません。 
Instead, you’ll learn to test, version, operate, and monitor the ML pipelines that power your AI systems. 
代わりに、AIシステムを支えるMLパイプラインをテストし、バージョン管理し、運用し、監視する方法を学びます。(これらがめちゃめちゃ非伝統的か、っていうと別に全然そうでもない気もする...!!:thinking:)

<!-- ここまで読んだ! -->

### A Unified Architecture for AI Systems: Feature, Training, and Inference Pipelines

_Modularity in software is the capacity to decompose a system into smaller, more manageable modules that can be independently developed and composed into a complete software system. 
_ソフトウェアにおけるモジュラリティ(=モジュラー性...!:thinking:)は、システムをより小さく、管理しやすいモジュールに分解し、それらを独立して開発し、完全なソフトウェアシステムに組み合わせる能力です。 
Modularity helps us build better-quality, more reliable software systems, as it allows modules to be independently tested. 
**モジュラリティは、モジュールを独立してテストできるため、より高品質で信頼性の高いソフトウェアシステムを構築するのに役立ちます。**
AI systems can also benefit from modularity because it enables teams to build higher-quality AI systems faster. 
AIシステムもモジュラリティの恩恵を受けることができ、チームがより高品質なAIシステムをより迅速に構築できるようになります。 

<!-- ここまで読んだ! -->

Implementing modularity involves structuring your AI system so that its functionality is separated into independent components that can be independently developed, run, and tested. 
モジュラリティを実装することは、AIシステムの機能を独立したコンポーネントに分離し、それらを独立して開発、実行、テストできるように構造化することを含みます。 
Modules should be kept small and easy to understand and document. 
**モジュールは小さく、理解しやすく、文書化しやすいものであるべき**です。 
Modules should enable reuse of functionality in AI systems, clear separation of work between teams, and better communication between those teams through shared understanding of the concepts and interfaces in the AI system.
**モジュールは、AIシステムにおける機能の再利用、チーム間の作業の明確な分離、AIシステム内の概念とインターフェースに関する共通理解を通じたチーム間のより良いコミュニケーションを可能にするべきです。**

<!-- ここまで読んだ! -->

Earlier in this chapter, we presented five different AI system architectures for batch, stateless real-time, stateful real-time, RAG LLM, and agentic AI systems.
この章の前半では、バッチ、ステートレスリアルタイム、ステートフルリアルタイム、RAG LLM、エージェントAIシステムのための5つの異なるAIシステムアーキテクチャを提示しました。 
These are useful architectural patterns that you can employ when developing a new AI system.
これらは、新しいAIシステムを開発する際に利用できる有用なアーキテクチャパターンです。 
However, the architectures are very different, and it is challenging for developers to jump from one to another or transfer learnings from one architecture to another.
しかし、アーキテクチャは非常に異なり、開発者が一つから別のものに飛び移ったり、一つのアーキテクチャから別のアーキテクチャに学びを移転するのは難しいです。 

-----
Luckily, we can do better
幸運なことに、私たちはより良いことができます。



Luckily, we can do better. 
幸運なことに、私たちはより良いことができます。

There is a unified architecture for developing all AI systems that follows a natural decomposition of any AI system into feature creation, model training, and inference pipelines. 
すべてのAIシステムを開発するための統一されたアーキテクチャがあり、これは任意のAIシステムを特徴の作成、モデルのトレーニング、および推論パイプラインに自然に分解します。

At KTH, my students built AI systems in teams as project work, and despite the fact that they built all different AI systems, they could easily divide the work in building their systems and communicate their system architecture with this feature/training/inference (FTI) decomposition. 
KTHでは、私の学生たちがプロジェクト作業としてチームでAIシステムを構築しました。彼らは異なるAIシステムを構築しましたが、システムの構築において作業を簡単に分担し、この特徴/トレーニング/推論（FTI）分解を用いてシステムアーキテクチャを伝えることができました。

In enterprises, different teams can take responsibility for the different parts: feature creation can require help from data engineers, model training is the realm of data scientists, and inference can involve folks from IT operations. 
企業では、異なるチームが異なる部分の責任を負うことができます。特徴の作成にはデータエンジニアの助けが必要な場合があり、モデルのトレーニングはデータサイエンティストの領域であり、推論にはIT運用の人々が関与することがあります。

ML engineers are expected to contribute to all three classes of pipeline. 
MLエンジニアは、すべての3つのパイプラインクラスに貢献することが期待されています。

The three different ML pipelines have clear inputs and outputs and can be developed, tested, and operated independently: 
3つの異なるMLパイプラインは明確な入力と出力を持ち、独立して開発、テスト、運用することができます。

_Feature pipelines_ These take data as input and produce reusable feature data as output. 
_特徴パイプライン_ これらはデータを入力として受け取り、再利用可能な特徴データを出力します。

_Training pipelines_ These take feature data as input, train a model, and output the trained model. 
_トレーニングパイプライン_ これらは特徴データを入力として受け取り、モデルをトレーニングし、トレーニングされたモデルを出力します。

_Inference pipelines_ These take feature data and a model as inputs, and they output predictions and prediction logs. 
_推論パイプライン_ これらは特徴データとモデルを入力として受け取り、予測と予測ログを出力します。

Modularity only helps if the modules can be easily composed into functioning systems. 
モジュール性は、モジュールが機能するシステムに簡単に構成できる場合にのみ役立ちます。

Good examples of this are web applications that are still being built 30 years later with separate presentation, business logic, and database modules. 
良い例としては、30年後も別々のプレゼンテーション、ビジネスロジック、およびデータベースモジュールを持つウェブアプリケーションがあります。

Microservice architectures, on the other hand, can suffer when there are too many microservices, as that increases operational complexity when they are composed into a single system. 
一方、マイクロサービスアーキテクチャは、マイクロサービスが多すぎると、単一のシステムに構成される際に運用の複雑さが増すため、問題が生じることがあります。

For our AI system decomposition, we can naturally compose our AI system from the three types of ML pipeline by making them independent programs that are connected with a shared data layer that consists of a feature store and model registry. 
私たちのAIシステムの分解において、特徴ストアとモデルレジストリで構成される共有データレイヤーで接続された独立したプログラムとして、3種類のMLパイプラインから自然にAIシステムを構成することができます。

The feature store stores real-time data in a row-oriented store for low latency access from online inference pipelines and agents, historical data in a columnar data store for training models and batch inference, and vector embeddings in a vector index for inference pipelines and agents. 
特徴ストアは、オンライン推論パイプラインとエージェントからの低遅延アクセスのために行指向ストアにリアルタイムデータを保存し、モデルのトレーニングとバッチ推論のために列指向データストアに履歴データを保存し、推論パイプラインとエージェントのためにベクトルインデックスにベクトル埋め込みを保存します。

We can now define an AI system as a set of independent feature pipelines, training pipelines, and inference pipelines that are connected via a feature store and model registry (see Figure 1-6). 
これで、AIシステムを特徴ストアとモデルレジストリを介して接続された独立した特徴パイプライン、トレーニングパイプライン、および推論パイプラインのセットとして定義できます（図1-6を参照）。

_Figure 1-6. An AI system with a feature pipeline, a training pipeline, and an inference pipeline, operationally connected through a feature store. Inference pipelines can be anything from batch programs to model serving programs to agents. Operational logs need to be collected for monitoring and debugging AI systems._ 
_図1-6. 特徴パイプライン、トレーニングパイプライン、および推論パイプラインを持つAIシステムで、特徴ストアを介して運用的に接続されています。推論パイプラインは、バッチプログラムからモデル提供プログラム、エージェントまで何でも可能です。運用ログは、AIシステムの監視とデバッグのために収集する必要があります。_

Feature pipelines ingest both backfill and production data and compute feature data that is stored as tabular data in the feature store. 
特徴パイプラインは、バックフィルデータと生産データの両方を取り込み、特徴データを計算して特徴ストアに表形式データとして保存します。

Feature pipelines can be either batch programs or stream processing programs. 
特徴パイプラインは、バッチプログラムまたはストリーム処理プログラムのいずれかです。

Training pipelines read training data from the feature store and store any trained models they produce in the model registry. 
トレーニングパイプラインは、特徴ストアからトレーニングデータを読み取り、生成したトレーニング済みモデルをモデルレジストリに保存します。

Inference pipelines output predictions using a model (either downloaded from the model registry or via an API) and new feature data (precomputed from the feature store and/or computed from data available at prediction request time). 
推論パイプラインは、モデル（モデルレジストリからダウンロードしたものまたはAPI経由のもの）と新しい特徴データ（特徴ストアから事前計算されたものおよび/または予測リクエスト時に利用可能なデータから計算されたもの）を使用して予測を出力します。

The ML pipelines can be run on potentially any compute engine. 
MLパイプラインは、潜在的に任意のコンピュートエンジンで実行できます。

Popular batch compute engines include SQL in data warehouses, Spark, Pandas, Polars, and DuckDB. 
一般的なバッチコンピュートエンジンには、データウェアハウスのSQL、Spark、Pandas、Polars、およびDuckDBが含まれます。

Popular stream processing engines include Flink, Spark Structured Streaming, and Feldera. 
一般的なストリーム処理エンジンには、Flink、Spark Structured Streaming、およびFelderが含まれます。

Training pipelines are most commonly implemented in Python, as are online inference pipelines and agents. 
トレーニングパイプラインは最も一般的にPythonで実装されており、オンライン推論パイプラインやエージェントも同様です。

Batch inference pipelines are often written with PySpark, Pandas, and Polars. 
バッチ推論パイプラインは、PySpark、Pandas、およびPolarsで書かれることが多いです。

###### Classes of AI Systems with a Feature Store
###### 特徴ストアを持つAIシステムのクラス

An AI system is defined by how it computes its predictions, not by the type of application that consumes the predictions. 
AIシステムは、予測をどのように計算するかによって定義され、予測を消費するアプリケーションの種類によって定義されるわけではありません。

AI systems with a feature store can be categorized as: 
特徴ストアを持つAIシステムは次のように分類できます。

_Real-time (interactive) ML systems_ These make predictions in response to user requests. 
_リアルタイム（インタラクティブ）MLシステム_ これらはユーザーのリクエストに応じて予測を行います。

They can compute features on demand from prediction request parameters and/or read precomputed features from the feature store or other external systems. 
これらは、予測リクエストパラメータからオンデマンドで特徴を計算したり、特徴ストアや他の外部システムから事前計算された特徴を読み取ったりできます。

Stream processing is often used to precompute features that are fresh, enabling interactive ML systems to react faster to user actions compared with batch feature pipelines. 
ストリーム処理は、フレッシュな特徴を事前計算するためにしばしば使用され、インタラクティブMLシステムがバッチ特徴パイプラインと比較してユーザーのアクションにより迅速に反応できるようにします。

_Agentic workflows_ These are user-guided AI systems that, with some level of autonomy, achieve goals by using LLMs and tools (i.e., execute actions on external systems and acquire context information by using data sources such as a vector index, a row-oriented data store, a column-oriented data store, and external APIs). 
_エージェンティックワークフロー_ これらはユーザーがガイドするAIシステムで、ある程度の自律性を持ち、LLMやツールを使用して目標を達成します（つまり、外部システムでアクションを実行し、ベクトルインデックス、行指向データストア、列指向データストア、外部APIなどのデータソースを使用してコンテキスト情報を取得します）。

Feature pipelines, vector-embedding pipelines, and real-time feature engineering create context data for use by agents. 
特徴パイプライン、ベクトル埋め込みパイプライン、およびリアルタイム特徴エンジニアリングは、エージェントが使用するためのコンテキストデータを作成します。

_Batch ML systems_ These run batch inference programs on a schedule. 
_バッチMLシステム_ これらはスケジュールに従ってバッチ推論プログラムを実行します。

They take new feature data and a model and output predictions that are typically stored in some downstream database (called an inference store), to be consumed later by some ML-enabled application. 
これらは新しい特徴データとモデルを取り込み、予測を出力します。これらの予測は通常、下流のデータベース（推論ストアと呼ばれる）に保存され、後でML対応アプリケーションによって消費されます。

_Stream processing ML systems_ These use an embedded model to make predictions on streaming data without user input. 
_ストリーム処理MLシステム_ これらは埋め込まれたモデルを使用して、ユーザー入力なしでストリーミングデータに対して予測を行います。

They are often machine-to-machine ML systems. 
これらはしばしば機械間MLシステムです。

For example, a network intrusion detection ML system could use stream processing to extract features from network traffic and a model to predict network intrusion. 
例えば、ネットワーク侵入検知MLシステムは、ストリーム処理を使用してネットワークトラフィックから特徴を抽出し、ネットワーク侵入を予測するモデルを使用することができます。

Real-time ML systems and agentic workflows are both interactive systems that provide a prediction request API, handle concurrent prediction requests, and use a model to make predictions. 
リアルタイムMLシステムとエージェンティックワークフローはどちらも、予測リクエストAPIを提供し、同時予測リクエストを処理し、モデルを使用して予測を行うインタラクティブシステムです。

The distinction we use is that real-time ML systems have a custom-trained model (not an LLM, but perhaps a decision tree or deep learning model) hosted internally on model-serving infrastructure and a relatively simple online inference pipeline. 
私たちが使用する区別は、リアルタイムMLシステムがカスタムトレーニングされたモデル（LLMではなく、決定木や深層学習モデルの可能性があります）をモデル提供インフラストラクチャに内部的にホストし、比較的単純なオンライン推論パイプラインを持つということです。

In contrast, agentic workflows have a more complex online inference pipeline program, an agent program, that uses both tools and an LLM typically accessed via an external API. 
対照的に、エージェンティックワークフローは、ツールと通常外部APIを介してアクセスされるLLMの両方を使用する、より複雑なオンライン推論パイプラインプログラム、エージェントプログラムを持っています。

The following are AI systems that we will build in this book: 
以下は、この本で構築するAIシステムです。

_Batch ML systems_ In Chapter 3, you will build an air quality prediction dashboard that shows air quality forecasts for a location near you. 
_バッチMLシステム_ 第3章では、あなたの近くの場所の空気質予測を表示する空気質予測ダッシュボードを構築します。

It will use observations of air quality from a public sensor and weather data as features. 
これは、公共センサーからの空気質の観測と天候データを特徴として使用します。

You will train a model to predict air quality using weather forecast data. 
あなたは、天気予報データを使用して空気質を予測するモデルをトレーニングします。

_Real-time ML systems_ From Chapter 4 onward, we will develop a credit card fraud detection ML system. 
_リアルタイムMLシステム_ 第4章以降、クレジットカード詐欺検出MLシステムを開発します。

It will take a credit card transaction, retrieve precomputed features about recent use of the credit card from a feature store, and then build a feature vector that’s sent to a decision tree model you train to predict whether the transaction is suspected of fraud or not. 
これは、クレジットカード取引を受け取り、特徴ストアからクレジットカードの最近の使用に関する事前計算された特徴を取得し、次に、取引が詐欺の疑いがあるかどうかを予測するためにトレーニングした決定木モデルに送信される特徴ベクトルを構築します。

In Chapter 15, we will build a video recommender system, similar to TikTok’s, based on the retrieval-and-ranking architecture. 
第15章では、TikTokに似た動画推薦システムを、取得とランキングのアーキテクチャに基づいて構築します。

It will use stream processing to create features from user actions, such as clicks and swipes, a two-tower embedding model for retrieval, and a faster eXtreme Gradient Boosting (XGBoost) model for ranking. 
これは、ユーザーのアクション（クリックやスワイプなど）から特徴を作成するためにストリーム処理を使用し、取得のための2タワー埋め込みモデルと、ランキングのためのより高速なeXtreme Gradient Boosting（XGBoost）モデルを使用します。

_Agentic AI systems_ We will add LLM capabilities to our air quality prediction system and our TikTok recommender systems, with examples of agents in LlamaIndex. 
_エージェンティックAIシステム_ 私たちは、空気質予測システムとTikTok推薦システムにLLM機能を追加し、LlamaIndexにおけるエージェントの例を示します。

###### ML Frameworks and ML Infrastructure Used in This Book
###### この本で使用されるMLフレームワークとMLインフラストラクチャ

In this book, we will build AI systems using programs written in Python. 
この本では、Pythonで書かれたプログラムを使用してAIシステムを構築します。

Given that we aim to build AI systems, not the ML infrastructure underpinning them, we have to make decisions about what platforms to cover in this book. 
私たちがAIシステムを構築することを目指しているため、それを支えるMLインフラストラクチャではなく、この本でどのプラットフォームをカバーするかについて決定を下す必要があります。

Given space restrictions, we have to restrict ourselves to a set of well-motivated choices. 
スペースの制約を考慮して、私たちは十分に根拠のある選択肢のセットに制限する必要があります。

For programming, we chose Python as it is accessible to developers, the dominant language of data science, and increasingly important in data engineering. 
プログラミングには、開発者にとってアクセスしやすく、データサイエンスの主要な言語であり、データエンジニアリングにおいてますます重要になっているPythonを選びました。

We will use open source frameworks in Python, including Pandas and Polars for feature engineering, Scikit-Learn and PyTorch for ML, and KServe for model serving. 
私たちは、特徴エンジニアリングのためのPandasとPolars、MLのためのScikit-LearnとPyTorch、モデル提供のためのKServeを含むPythonのオープンソースフレームワークを使用します。

Python can be used for everything from creating features from raw data, to model training, to developing user interfaces for our AI systems. 
Pythonは、生データから特徴を作成することから、モデルのトレーニング、AIシステムのユーザーインターフェースの開発まで、すべてに使用できます。

We will also use pretrained LLMs—open source foundation models. 
私たちはまた、事前トレーニングされたLLM（オープンソースの基盤モデル）を使用します。

When appropriate, we will also provide examples using other programming frameworks or languages widely used in the enterprise, such as Spark and dbt/SQL for scalable data processing, and stream processing frameworks for real-time ML systems. 
適切な場合には、スケーラブルなデータ処理のためのSparkやdbt/SQL、リアルタイムMLシステムのためのストリーム処理フレームワークなど、企業で広く使用されている他のプログラミングフレームワークや言語を使用した例も提供します。

That said, the example AI systems presented in this book were developed so that only knowledge of Python is a prerequisite. 
とはいえ、この本で提示される例のAIシステムは、Pythonの知識のみが前提条件となるように開発されています。

To run our Python programs as pipelines in the cloud, we’ll use serverless platforms like Modal and GitHub Actions. 
私たちのPythonプログラムをクラウドでパイプラインとして実行するために、ModalやGitHub Actionsのようなサーバーレスプラットフォームを使用します。

Both GitHub and Modal offer a free tier (although Modal requires credit card registration) that will enable you to run the ML pipelines introduced in this book. 
GitHubとModalの両方は、（Modalはクレジットカード登録が必要ですが）この本で紹介されているMLパイプラインを実行できる無料プランを提供しています。

If you have a dedicated Hopsworks cluster, you can also run your ML pipelines there. 
専用のHopsworksクラスターがある場合、そこでもMLパイプラインを実行できます。

If you have any other platform for running Python jobs, the ML pipeline examples here should also work. 
Pythonジョブを実行するための他のプラットフォームがある場合、ここでのMLパイプラインの例も機能するはずです。

For exploratory data analysis, model training, and other nonoperational services, we will use open source Jupyter Notebooks. 
探索的データ分析、モデルのトレーニング、およびその他の非運用サービスには、オープンソースのJupyter Notebooksを使用します。

Finally, for (serverless) user interfaces hosted in the cloud, we will use Streamlit, which also provides a free cloud tier. 
最後に、クラウドでホストされる（サーバーレス）ユーザーインターフェースには、無料のクラウドプランも提供しているStreamlitを使用します。

Alternatives would be Hugging Face Spaces and Gradio. 
代替案としては、Hugging Face SpacesやGradioがあります。

We will use Hopsworks as serverless ML infrastructure, using its feature store, model registry, and model-serving platform to manage features and models. 
私たちは、HopsworksをサーバーレスMLインフラストラクチャとして使用し、その特徴ストア、モデルレジストリ、およびモデル提供プラットフォームを使用して特徴とモデルを管理します。

Hopsworks is open source, was the first open source and enterprise feature store, and has a free tier for its serverless platform. 
Hopsworksはオープンソースであり、最初のオープンソースおよびエンタープライズ特徴ストアであり、サーバーレスプラットフォームのための無料プランがあります。

The other reason for using Hopsworks is that I am one of its developers, so I can provide deeper insights into its inner workings as a representative ML infrastructure platform. 
Hopsworksを使用するもう一つの理由は、私がその開発者の一人であるため、代表的なMLインフラストラクチャプラットフォームとしての内部動作についてより深い洞察を提供できることです。



. The other reason for using Hopsworks is that I am one of its developers, so I can provide deeper insights into its inner workings as a representative ML infrastructure platform. 
Hopsworksを使用するもう一つの理由は、私がその開発者の一人であるため、代表的なMLインフラストラクチャプラットフォームとしての内部動作についてより深い洞察を提供できることです。

With Hopsworks’ free serverless tier, you can deploy and operate your AI systems without cost or the need to install or operate ML infrastructure platforms. 
Hopsworksの無料サーバーレスティアを使用すると、コストをかけずにAIシステムを展開および運用でき、MLインフラストラクチャプラットフォームをインストールまたは運用する必要もありません。

That said, given that all of the examples are in common open source Python frameworks, you can easily modify the provided examples to replace Hopsworks with any combination of an existing feature store (such as Feast), a model registry, and a model serving platform (such as MLflow). 
とはいえ、すべての例が一般的なオープンソースのPythonフレームワークであるため、提供された例を簡単に修正して、Hopsworksを既存のフィーチャーストア（Feastなど）、モデルレジストリ、およびモデルサービングプラットフォーム（MLflowなど）の任意の組み合わせに置き換えることができます。

Alternatively, you could use Databricks, Google Cloud Platform (GCP) Vertex, or Amazon Web Services (AWS) SageMaker. 
あるいは、Databricks、Google Cloud Platform（GCP）Vertex、またはAmazon Web Services（AWS）SageMakerを使用することもできます。

###### Summary 要約
In this chapter, we introduced batch, real-time, and LLM AI systems with a feature store. 
この章では、バッチ、リアルタイム、およびLLM AIシステムとフィーチャーストアを紹介しました。

We introduced the main properties of AI systems, their architecture, and the ML pipelines that power them. 
AIシステムの主な特性、そのアーキテクチャ、およびそれらを支えるMLパイプラインを紹介しました。

We introduced MLOps and its historical evolution as a set of best practices for developing and evolving AI systems, and we presented a new architecture for AI systems as FTI pipelines connected with a feature store. 
MLOpsとその歴史的進化をAIシステムを開発および進化させるためのベストプラクティスのセットとして紹介し、フィーチャーストアに接続されたFTIパイプラインとしてのAIシステムの新しいアーキテクチャを提示しました。

In the next chapter, we will look closer at this new FTI architecture for building AI systems and how you can build AI systems faster and more reliably as connected FTI pipelines. 
次の章では、AIシステムを構築するためのこの新しいFTIアーキテクチャを詳しく見ていき、接続されたFTIパイプラインとしてAIシステムをより速く、より信頼性高く構築する方法について説明します。



