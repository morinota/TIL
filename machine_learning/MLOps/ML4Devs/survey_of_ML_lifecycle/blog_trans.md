## link リンク

- https://www.ml4devs.com/articles/mlops-survey-of-machine-learning-life-cycle/ https://www.ml4devs.com/articles/mlops-survey-of-machine-learning-life-cycle/

## title タイトル

Survey of Machine Learning Lifecycle
機械学習ライフサイクルの調査

Evolution of ML lifecycle from resource-constrained batch data mining to MLOps at the cloud scale.
リソースに制約のあるバッチデータマイニングからクラウドスケールのMLOpsへのMLライフサイクルの進化。

# intro イントロ

Everyone has been talking about MLOps for over a year now.
MLOpsについては、もう1年以上も前から誰もが話している。
I looked around for how the lifecycle and processes have evolved.
私は、ライフサイクルとプロセスがどのように進化してきたかを見て回った。

The discipline of seeking insight from data has been around for 25 years.
データから洞察を求めるという学問は、25年前から存在している。
Back then, it was known as data mining.
当時はデータマイニングと呼ばれていた。
In this article, I present a survey of the ML lifecycle process and conclude with my take on machine learning lifecycle for MLOps era.
この記事では、MLのライフサイクル・プロセスのサーベイを紹介し、最後にMLOps時代の機械学習ライフサイクルについて私の考えを述べる。
So if you are in a hurry, jump to the last section for TL;DR.
お急ぎの方は、TL;DRの最後のセクションにジャンプしてください。

The broad steps in data mining/science have remained more or less the same:
データマイニング／サイエンスの大まかなステップは、多かれ少なかれ変わっていない：

Understand domain or business problem
ドメインまたはビジネス上の問題を理解する

Collect the needed data from a variety of sources
さまざまな情報源から必要なデータを収集する

Curate the data, clean and label it
データを整理し、きれいにし、ラベルを付ける

Transform the data, harmonize it, and shape it
データを変換し、調和させ、形にする。

Explore and visualize the data
データの探索と視覚化

Train a model, validate it, and tune hyper-parameters
モデルの訓練、検証、ハイパーパラメータの調整

Use or deploy the models
モデルの使用または展開

But the nature of data, processing, and applications has changed significantly:
しかし、データ、処理、アプリケーションの性質は大きく変わった：

Scale: The amount of data analyzed has increased manifolds.
規模： 分析されるデータ量は何倍にも増えている。

Widespread Use: ML-powered applications are part of our daily lives and we critically depend on them.
広範な利用： MLを利用したアプリケーションは私たちの日常生活の一部であり、私たちはMLに決定的に依存している。

Batch vs.
バッチ対バッチ
Online: The models were used earlier in batch mode to draw insights and guide business decisions.
オンライン モデルは、洞察力を引き出し、ビジネス上の意思決定を導くために、以前にバッチモードで使用された。
Now more models are deployed to serve inference at scale.
現在では、より多くのモデルがスケールの大きな推論を行うために導入されている。

The evolution can be roughly divided into 3 eras (timelines are overlapping):
進化は大きく3つの時代に分けられる（時間軸は重複している）：

Batch Era: ETL pipelines brought data from operational systems to data warehouses and data marts, and data was mined thereafter.
バッチの時代： ETLパイプラインが運用システムからデータウェアハウスやデータマートにデータをもたらし、その後データがマイニングされた。

Big Data Era: Data became too big for warehouses of the time.
ビッグデータ時代： データが大きくなりすぎて、当時の倉庫では対応できなくなった。
Data streamed in data lakes, which often turned into swamps.
データはデータレイクに流れ込み、それはしばしば沼地と化した。
Only a few organizations deploy online models.
オンライン・モデルを導入している組織はごく少数である。

MLOps Era: Making it easy for everyone to deploy online models continuously.
MLOpsの時代： 誰もが簡単にオンラインモデルを継続的に展開できるようにする。

# Batch Era バッチ時代

You can call it ancient times.
古代と言ってもいい。
The internet was still in the nascent stages.
インターネットはまだ黎明期だった。
Most enterprise applications were generating and processing data in batches.
ほとんどのエンタープライズ・アプリケーションは、バッチでデータを生成し処理していた。

The applications and data were siloed in various departments of an organization.
アプリケーションとデータは、組織のさまざまな部門でサイロ化されていた。
The challenge was to bring it all together so that the whole is greater than the sum of its parts.
課題は、全体が部分の総和よりも大きくなるようにすべてをまとめることだった。

Data modeling “Schema-on-Write” was very important.
データモデリング "スキーマ・オン・ライト "は非常に重要だった。
Batch ETL data pipelines brought the data to a centralized Data Warehouse.
バッチETLデータパイプラインは、集中管理されたデータウェアハウスにデータをもたらした。
It was aggregated and stored in data marts, each for a specific line of business, department, or subject area.
データマートに集約され、それぞれ特定の業務、部署、分野ごとに保存されていた。

Data was not so big.
データはそれほど大きくなかった。
RDBMS with column-oriented indexes were handy and OLAP Cubes ruled the day.
列指向のインデックスを持つRDBMSは便利で、OLAPキューブが一世を風靡した。

Data mining was mostly a backroom operation.
データマイニングはほとんど裏方の仕事だった。
Its role was to extract insights needed for making business decisions.
その役割は、ビジネス上の意思決定に必要な洞察を引き出すことだった。
So the processes of the time reflected this batch mode of data mining.
そのため、当時のプロセスには、このバッチ・モードのデータマイニングが反映されていた。

## KDD: Knowledge Discovery in Database KDD： データベースにおける知識発見

Extracting insights from data predates Big Data.
データからの洞察の抽出は、ビッグデータよりも以前から行われていた。
KDD Process (Knowledge Discovery and Data Mining: Towards a Unifying Framework by Fayyad et.
KDDプロセス（知識発見とデータマイニング： 統一的なフレームワークに向けて by Fayyad et.
al., 1996) was among the first to define a framework for data mining in databases.
al., 1996）は、データベースにおけるデータマイニングのフレームワークを定義した最初の人物の一人である。
KDD process has 5 stages with feedback:
KDDプロセスには、フィードバックを伴う5つの段階がある：

Selection: Selecting a data set, a subset of variables, or data samples
選択： データセット、変数のサブセット、データサンプルの選択

Pre-processing: Clean the data, handle missing values, etc.
前処理： データのクリーンアップ、欠損値の処理など。

Transformation: Feature selection and dimension projection to reduce the effective number of variables.
変換： 有効な変数数を減らすための特徴選択と次元投影。

Data Mining: Apply a particular mining method, e.g., summarization, classification, regression, clustering.
データマイニング： 特定のマイニング手法（要約、分類、回帰、クラスタリングなど）を適用する。

Interpretation & Evaluation: Extract patterns/models, report it along with data visualizations.
解釈と評価： パターン/モデルを抽出し、データの視覚化とともに報告する。

Modern data pipelines have pretty much the same steps.
最近のデータパイプラインは、ほとんど同じステップを踏んでいる。

## CRISP-DM: CRoss-Industry Standard Process for Data Mining CRISP-DM： データマイニングの業界標準プロセス

Then came the CRISP-DM process (The CRISP-DM Model: The New Blueprint for Data Mining by Colin Shearer, 2000), which remains influential even today (CRISP-ML(Q)).
その後、CRISP-DMプロセス（The CRISP-DM Model： Colin Shearer著、データマイニングの新しい設計図、2000年）が登場し、これは現在でも影響力を持ち続けている（CRISP-ML(Q)）。
It describes how “data analysts” should start from business needs, mine the data, and “deploy” the model.
データアナリスト」がどのようにビジネスニーズから出発し、データをマイニングし、モデルを「展開」すべきかが書かれている。
It breaks the data mining process into six major phases:
データマイニングのプロセスを大きく6つのフェーズに分けている：

Business Understanding: Determine business objectives.
ビジネスの理解： ビジネス目標を決定する。
Assess resources, requirements, constraints, risks, and contingencies.
リソース、要件、制約、リスク、不測の事態を評価する。
Define data mining goals and make a project plan.
データマイニングの目標を定め、プロジェクト計画を立てる。

Data Understanding: Collect initial data, explore the data, and verify data quality.
データの理解： 初期データを収集し、データを探索し、データの質を検証する。

Data Preparation: Select and clean the data.
データの準備： データを選択し、クリーニングする。
Add derived attributes and generated records.
派生属性と生成されたレコードを追加する。
Merge the data, and shape it as per the desired schema.
データをマージし、希望するスキーマに沿った形にする。

Modeling: Build the model, and assess its quality.
モデリング： モデルを構築し、その品質を評価する。

Evaluation: Review the model’s construction to ensure that it achieves the stated business objectives.
評価： ビジネス目標を達成するために、モデルの構造を見直す。

Deployment: Generate a report, or implement a repeatable data mining process across the enterprise.
展開 レポートを作成したり、企業全体で反復可能なデータマイニングプロセスを実装します。
Plan monitoring of the data mining results, and maintenance of the data timing process.
データマイニング結果のモニタリング、データタイミングプロセスのメンテナンスを計画する。

“Deployment” is where it was ahead of its time.
"Deployment "は時代を先取りしていたところだ。
There was no way to deploy a model as an inference function.
モデルを推論関数として展開する方法はなかった。
It states (customer here refers to the customer of the analysts, i.e.business org/managers):
と書かれている（ここでいう顧客とは、アナリストの顧客、つまりビジネス・オーガナイザーのことである）：

The knowledge gained must be organized and presented in a way that the customer can use it, which often involves applying “live” models within an organization’s decision-making processes, such as the real-time personalization of Web pages or repeated scoring of marketing databases.
得られた知識は、顧客が利用できるように整理され、提示されなければならない。これはしばしば、ウェブページのリアルタイム・パーソナライゼーションやマーケティング・データベースの繰り返しスコアリングなど、組織の意思決定プロセスの中で「生きた」モデルを適用することを伴う。

Depending on the requirements, the deployment phase can be as simple as generating a report or as complex as implementing a repeatable data mining process across the enterprise.
要件に応じて、展開フェーズは、レポートの生成のような単純なものから、企業全体で反復可能なデータマイニングプロセスの実装のような複雑なものまであります。
Even though it is often the customer, not the data analyst, who carries out the deployment steps, it is important for the customer to understand up front what actions must be taken in order to actually make use of the created models.
デプロイの手順を実行するのはデータアナリストではなく顧客であることが多いとはいえ、作成したモデルを実際に利用するためにどのようなアクションを取らなければならないかを顧客が前もって理解しておくことは重要である。

## SEMMA: Sample, Explore, Modify, Model, and Assess SEMMA サンプル、調査、修正、モデル、評価

SEMMA stands for Sample, Explore, Modify, Model, and Assess.
SEMMAとは、サンプル（Sample）、探究（Explore）、修正（Modify）、モデル（Model）、評価（Assess）の頭文字をとったものだ。
It is a list of sequential steps developed by SAS Institute to guide the implementation of data mining applications.
これは、データマイニングアプリケーションの実装を導くためにSAS Instituteによって開発されたシーケンシャルステップのリストです。

Sample: Sample and select data for modeling.
サンプル サンプリングし、モデリング用のデータを選択する。

Explore: Visualize data to discover anticipated and unanticipated relationships between data variables and identify anomalies.
探求する： データを視覚化し、データ変数間の予期される関係や予期されない関係を発見し、異常を特定する。

Modify: Select and transform data variables to prepare data for modeling.
修正する： データ変数を選択して変換し、モデリング用のデータを準備する。

Model: Apply various modeling techniques to prepare data.
モデルを作る： データを準備するために様々なモデリング技術を適用する。

Assess: Evaluate and compare the effectiveness of the models.
評価する： モデルの有効性を評価し、比較する。

SEMMA stages seem to be somewhere between KDD and CRISP-DM.
SEMMAのステージは、KDDとCRISP-DMの中間のようだ。

# Big Data Era ビッグデータ時代

Data has an uncanny ability to outgrow any storage and processing technology.
データには、どんなストレージや処理技術も凌駕する不思議な能力がある。
Big Data arrived and Data Warehouses were insufficient for processing the piles of data businesses were generating.
ビッグデータが登場し、データウェアハウスは企業が生成するデータの山を処理するには不十分だった。
So, we invented the Data Lake (blobs repository) to store raw data files at any scale.
そこで私たちは、生のデータファイルをどんな規模でも保存できるデータレイク（blobsリポジトリ）を考案した。
This led to the shift from “schema-on-write” to “schema-on-read”.
これが「スキーマ・オン・ライト」から「スキーマ・オン・リード」への移行につながった。

Very soon, everyone started dumping whatever data they felt like into the data lakes in whatever format/schema they fancied.
すぐに、誰もが好きなデータを好きなフォーマット／スキーマでデータレイクにダンプし始めた。
Data Lakes turned into Data Swamp.
データレイクがデータ沼に変わった
Data abundance coexisted with the scarcity of usable data.
データの豊富さと、使えるデータの少なさが共存している。
Data Cleaning became a thing.
データ・クリーニングが流行した。

You can call it medieval times.
中世と呼んでもいい。
The scale of data analytics and Business Intelligence grew manifolds.
データ分析とビジネス・インテリジェンスの規模は多様化した。
Data Scientist became the sexiest job.
データサイエンティストは最もセクシーな仕事になった。

The data collection and pipelines were automated and ran mostly at a daily cadence.
データ収集とパイプラインは自動化され、ほぼ毎日実行された。
Often, data analytics dashboards were updated in real-time joining batch and streaming data processing.
多くの場合、データ分析ダッシュボードは、バッチ処理やストリーミングデータ処理に参加してリアルタイムで更新されていた。
But most organizations used predictive models in batch mode for guiding their business decisions and products, and only a few deployed ML models in production for online real-time inference.
しかし、ほとんどの組織は、ビジネス上の意思決定や製品を導くためにバッチモードで予測モデルを使用しており、オンライン・リアルタイム推論のために本番環境でMLモデルを導入している組織はわずかであった。

The lifecycle and processes were adapted to include explicit steps for data pipelines, model training, validation, and even (manual) deployment.
ライフサイクルとプロセスは、データパイプライン、モデルのトレーニング、検証、そして（手作業による）デプロイメントのための明確なステップを含むように適応された。

## OSEMN: Obtain, Scrub, Explore, Model, iNterpret OSEMN 取得、スクラブ、探索、モデル、解釈

Hilary Mason and Chris Wiggins described the OSEMN process in “A Taxonomy of Data Science” blog post (dated 25 Sep 2010).
ヒラリー・メイソン（Hilary Mason）とクリス・ウィギンズ（Chris Wiggins）は、ブログ記事「データサイエンスの分類法」（2010年9月25日付）でOSEMNのプロセスについて説明している。
It has 5 steps: Obtain, Scrub, Explore, Model, and INterpret.
それには5つのステップがある： 取得、スクラブ、探索、モデル化、そして解釈。

Obtain: Pointing and clicking do not scale.
入手： ポインティングとクリックは拡大縮小しない。

Crawl or use APIs to automate data collection.
クロールまたはAPIを使用してデータ収集を自動化する。

Scrub: The world is a messy place.
スクラブ 世界は厄介な場所だ。

Your model will be messy too unless you clean and canonicalize the data.
データをクリーンにして正規化しない限り、モデルも乱雑になる。

Explore: You can see a lot by looking.
探検する： 見ることで多くのことが見えてくる。

This is what we do in Exploratory Data Analysis (EDA).
これが探索的データ分析（EDA）である。

Models: Always bad, sometimes ugly.
モデル： 常に悪く、時には醜い。

Optimize the chosen loss function, and pick the best through cross-validation.
選択した損失関数を最適化し、クロスバリデーションによって最適なものを選ぶ。

Interpret: The purpose of computing is insight, not numbers.
解釈する： コンピューティングの目的は洞察であり、数字ではない。

Unlike arithmetics, statistical results require nuanced interpretation.
算数と違って、統計の結果は微妙な解釈を必要とする。

The blog is now defunct, but you can read it on the Web Archive.
ブログは現在閉鎖されているが、ウェブアーカイブで読むことができる。
As you can see, it is still very much like KDD/CRISP-DM but the explanations of the steps reflect web-scale big data reality.
ご覧の通り、KDD/CRISP-DMに非常によく似ているが、ステップの説明はウェブスケールのビッグデータの現実を反映している。

## TDSP: Microsoft’s Team Data Science Process Lifcycle TDSP マイクロソフトのチーム・データ・サイエンス・プロセス・ライフサイクル

Microsoft’s Team Data Science Process (TDSP) Lifecycle has four stages:
マイクロソフトのチーム・データ・サイエンス・プロセス（TDSP）ライフサイクルには4つの段階がある：

Business Understanding
ビジネス理解

Data Acquisition and Understanding
データの取得と理解

Modeling
モデリング

Deployment
配備

The “Data Acquisition and Understanding” and “Modeling” stages are further broken down into more detailed steps.
データの取得と理解」と「モデリング」の段階は、さらに詳細なステップに分かれている。
It is envisioned as a waterfall model ending with Customer Acceptance, but it doesn’t require much imagination to extend it to be interactive.
ウォーターフォールモデルとして想定されているのは、カスタマー・アクセプタンスで終わるが、それをインタラクティブに拡張するのにそれほど想像力は必要ない。

It is pretty much what most companies currently follow knowingly or unknowingly.
現在、ほとんどの企業が知ってか知らずか従っていることだ。

In a paper at ICSE-SEIP 2019 conference, Saleema Amershi, et al.from Microsoft Research describe 9 stages of the machine learning workflow that is different from TDSP:
ICSE-SEIP 2019カンファレンスの論文で、マイクロソフト・リサーチのSaleema Amershiらは、TDSPとは異なる機械学習ワークフローの9つのステージについて説明している：

Some stages are data-oriented (e.g., collection, cleaning, and labeling) and others are model-oriented (e.g., model requirements, feature engineering, training, evaluation, deployment, and monitoring).
データ指向のステージ（収集、クリーニング、ラベリングなど）もあれば、モデル指向のステージ（モデル要件、フィーチャーエンジニアリング、トレーニング、評価、デプロイメント、モニタリングなど）もある。
There are many feedback loops in the workflow.
ワークフローには多くのフィードバックループがある。
The larger feedback arrows denote that model evaluation and monitoring may loop back to any of the previous stages.
より大きなフィードバックの矢印は、モデルの評価とモニタリングが、前の段階のいずれかにループバックする可能性があることを示している。
The smaller feedback arrow illustrates that model training may loop back to feature engineering (e.g., in representation learning).
小さい方のフィードバック矢印は、モデルのトレーニングが（例えば表現学習において）特徴工学にループバックする可能性があることを示している。

# MLOps Era MLOpsの時代

The rise of DevOps characterizes the modern era.
DevOpsの台頭は現代を特徴づけている。
When organizations regularly deploy ML models in production as part of their software applications/products, they need a data science process that fits into the DevOps best practices of Continous Integration and Continous Delivery (CI/CD).
組織がソフトウェア・アプリケーション/製品の一部としてMLモデルを本番環境に定期的にデプロイする場合、継続的インテグレーションと継続的デリバリー（CI/CD）というDevOpsのベスト・プラクティスに適合するデータサイエンス・プロセスが必要になる。
That is what is fueling the hype of MLOps.
それがMLOpsの誇大宣伝に拍車をかけている。

Most companies are not yet there and may I dare say need it at present.
ほとんどの企業はまだそこに到達しておらず、あえて言えば、現時点ではそれを必要としている。
Only big corporations like FAANG currently have a business that needs to deploy thousands of models every hour serving millions of end users.
現在、何百万人ものエンドユーザーに毎時間何千ものモデルをデプロイする必要があるビジネスを展開しているのは、FAANGのような大企業だけだ。
But as ML seeps into more applications, companies will begin to adopt a process with continuous training, integration, and delivery of ML models.
しかし、MLがより多くのアプリケーションに浸透するにつれて、企業はMLモデルの継続的なトレーニング、統合、提供のプロセスを採用し始めるだろう。

## ML Meets DevOps: 3 Loops MLとDevOpsの出会い： 3つのループ

An obvious way of blending ML into DevOps is to make the MLOps loop by adding ML to DevOps infinite loop and adapting Dev and Ops to suit data science.
MLをDevOpsに融合させる明らかな方法は、DevOpsの無限ループにMLを加えることでMLOpsループを作り、DevとOpsをデータサイエンスに適合させることだ。

Notice how this loop has the Data and Model as single steps characterizing the data processing and model building.
このループが、データ処理とモデル構築を特徴づける1つのステップとして、データとモデルを持っていることに注目してほしい。
On the other hand, the processes discussed so far dealt precisely with only these two steps.
一方、これまで議論してきたプロセスは、この2つのステップだけを正確に扱ってきた。
IMO, such dominance of Ops in a process is a step backward.
私は、このようなプロセスにおける作戦部の支配は後退だと思う。

There are other attempts at a 3-hoop MLOps loop too.
3フープのMLOPSループの試みは他にもある。
For example, the following captures the 3 broad phases Iterative-Incremental MLOps Process has three broad phases (which are still coarse IMO):
例えば、次のように3つの大まかなフェーズを捉える。 反復的-インクリメンタルMLOpsプロセスには、3つの大まかなフェーズがある（これはまだ粗いIMOである）：

## Data-ML-Dev-Ops Loop データML-デブオプスループ

A blog post by Danny Farah described the 4 loops of the MLOps lifecycle, one each for Data, ML, Dev, and Ops.
ダニー・ファラー（Danny Farah）によるブログ投稿では、MLOpsライフサイクルの4つのループ（データ、ML、開発、運用にそれぞれ1つずつ）について説明されている。
I like it for two reasons:
好きな理由は2つある：

It retains the details of the data and ML steps
データとMLのステップの詳細を保持する。

It feels more familiar w.r.t.
より身近に感じられる。
the DevOps infinite loop.
DevOpsの無限ループ。

Similar to DevOps, but it still feels different.
DevOpsと似ているが、やはり違うと感じる。
It is a missed opportunity to bring developers, data engineers, and data scientists to the same page.
開発者、データ・エンジニア、データ・サイエンティストを同じページに集める機会を逃しているのだ。
My 3 lessons for improving the success rate of ML projects are to consolidate ownership, integrate early, and iterate often.
MLプロジェクトの成功率を向上させるための私の3つの教訓は、オーナーシップを統合し、早期に統合し、頻繁に反復することである。
It is important to have a single lifecycle process that gives flexibility to all 3 to execute at a different cadence.
つのライフサイクル・プロセスを持つことが重要であり、3つすべてに柔軟性を与え、異なるケイデンスで実行できるようにする。
Overall visibility to all stakeholders reduces the surprises and hence improves success.
すべての利害関係者に対する全体的な可視性は、驚きを減らし、したがって成功を向上させる。

## Google Cloud グーグル クラウド

Discussion on MLOps can not be complete without discussing the Big Three cloud providers with massive ML services stack.
MLOpsに関する議論は、大規模なMLサービス・スタックを提供するビッグ3のクラウド・プロバイダーを抜きにしては語れない。

Google is arguable the earliest and the biggest machine learning shop with the Vertex AI MLOps platform.
グーグルは、Vertex AI MLOpsプラットフォームで最も早くから機械学習を行ってきた最大手であることは間違いない。
It published a whitepaper titled Practitioners Guide to MLOps in May 2021.
2021年5月には、『Practitioners Guide to MLOps』と題したホワイトペーパーを発表している。
I am quoting the MLOps Lifecycle section from the whitepaper that describes the following parts:
ホワイトペーパーからMLOpsライフサイクルのセクションを引用する：

ML Development: Experimenting and developing a robust and reproducible model training procedure (training pipeline code), which consists of multiple tasks from data preparation and transformation to model training and evaluation.
ML開発： ロバストで再現可能なモデル学習手順（学習パイプラインコード）の実験と開発。データの準備、変換からモデルの学習、評価まで、複数のタスクから構成される。

Training Operationalization: Automating the process of packaging, testing, and deploying repeatable and reliable training pipelines.
トレーニングの運用化： 反復可能で信頼性の高いトレーニングパイプラインのパッケージ化、テスト、導入プロセスの自動化。

Continuous Training: Repeatedly executing the training pipeline in response to new data, code changes, or on a schedule, potentially with new training settings.
継続的トレーニング： 新しいデータ、コードの変更、またはスケジュールに応じて、潜在的に新しいトレーニング設定でトレーニングパイプラインを繰り返し実行する。

Model Deployment: Packaging, testing, and deploying a model to a serving environment for online experimentation and production serving.
モデルのデプロイメント： モデルをパッケージ化し、テストし、オンライン実験と本番配信のための配信環境にデプロイすること。

Prediction Serving: Serving the model that is deployed in production for inference.
予測サービング： 本番環境に配置されたモデルを推論に供すること。

Continuous Monitoring: Monitoring the effectiveness and efficiency of a deployed model.
継続的なモニタリング： 展開されたモデルの有効性と効率性を監視すること。

Data and Model Management: A central, cross-cutting function for governing ML artifacts to support auditability, traceability, and compliance
データとモデルの管理： MLの成果物を管理し、監査可能性、トレーサビリティ、コンプライアンスをサポートするための中心的かつ横断的な機能。

## Amazon Web Services アマゾン ウェブ サービス

Amazon was the first to offer an end-to-end MLOps platform: SageMaker.
アマゾンはエンド・ツー・エンドのMLOpsプラットフォームを最初に提供した： SageMakerである。
It published a Whitepaper “MLOps: Emerging Trends in Data, Code,
ホワイトペーパー「MLOps」を発表した： データ、コードにおける新たなトレンド、

and Infrastructure, AWS Whitepaper” in June 2022, which defines a much simpler lifecycle.
とインフラ、AWSホワイトペーパー」（2022年6月）は、よりシンプルなライフサイクルを定義している。
It is so simple that it is self-explanatory.
とてもシンプルなので、自明のことだ。
It appears more like KDD and CRISP-DM than the DevOps loop.
DevOpsのループというよりは、KDDやCRISP-DMのように見える。

## Microsoft Azure マイクロソフト アジュール

Microsoft also published an MLOps whitepaper “MLOps with Azure Machine Learning” in Aug 2021, defining the ML lifecycle and MLOps workflow.
また、マイクロソフトは2021年8月にMLOpsのホワイトペーパー「MLOps with Azure Machine Learning」を発表し、MLのライフサイクルとMLOpsのワークフローを定義した。
It is similar to AWS: simple and self-explanatory.
AWSに似ている： シンプルでわかりやすい。

# My take on ML Lifecycle MLライフサイクルについての私の考え

This article turned out to be much longer than I imagined.
この記事は想像以上に長くなってしまった。
So thank you for your patience in reading it.
だから、辛抱強く読んでくれてありがとう。
If jumped here for TL;DR, then also thank you for caring to read my take.
もし、TL;DRのためにここにジャンプしたのなら、私の考えを読んでくれてありがとう。

First, what are the key characteristics of the ML lifecycle in the MLOps era?
まず、MLOps時代におけるMLのライフサイクルの主な特徴は何か？

Evolutionary, and not revolutionary.
革命的ではなく進化的だ。
It should feel familiar to data scientists who are following CRISP-DM, OSEMN, or TDSP so far.
これまでCRISP-DM、OSEMN、TDSPを追ってきたデータサイエンティストには馴染み深いものに感じられるはずだ。
It should also feel familiar to engineers following the DevOps infinite loop.
また、DevOpsの無限ループに従うエンジニアにとっても、馴染み深いものに感じられるはずだ。

Optimized for recall, instead of precision.
精度ではなく、想起に最適化されている。
An easy-to-remember process is more likely to be followed and become part of a team’s vocabulary.
覚えやすいプロセスは、守られやすく、チームの語彙の一部になりやすい。
For example, the DevOps infinite loop is not precise.
例えば、DevOpsの無限ループは正確ではない。
Each step has several implicit back arrows to previous steps.
各ステップには、前のステップに戻るための暗黙の矢印がいくつかある。
Not everything after the Test leads to the Release.
テスト後のすべてがリリースにつながるわけではない。
Failures go back to the Code or even Plan step.
失敗はコード、あるいはプランの段階まで遡る。

Facilitates taking ML model to production.
MLモデルを本番稼動しやすくする。
It should improve visibility and collaboration across a team of developers, data scientists, and data engineers, especially my philosophy of consolidating ownership, integrating early, and iterating often.
開発者、データサイエンティスト、データエンジニアで構成されるチーム全体の可視性とコラボレーションを向上させ、特に所有権を集約し、早期に統合し、頻繁に反復するという私の哲学を改善する必要がある。

Flexible.
柔軟性がある。
It should allow parts of a team to choose their cadence.
チームの各パートが自分のケイデンスを選択できるようにすべきだ。
Data Science and software development are inherently different.
データサイエンスとソフトウェア開発は本質的に異なる。
Data Scientists can not produce incremental results daily.
データサイエンティストは、毎日少しずつ成果を上げることはできない。
The goal of a lifecycle and process is visibility and cohesion, not a three-legged race.
ライフサイクルとプロセスの目標は可視化と結束であり、二人三脚ではない。

## Model Development Loop モデル開発ループ

If you ignore the deployment, the Model Development has its infinite loop just like the DevOps loop.
デプロイメントを無視すれば、モデル開発にもDevOpsのループと同じように無限ループがある。

Think of CRISP-DM molded into an infinite loop.
CRISP-DMを無限ループに成型したと考えればいい。
The steps in the Model Development loop are:
モデル開発ループのステップは以下の通り：

Formulate a business problem in ML terms.
ビジネス上の問題をML用語で定式化する。

Collect the necessary data from internal applications as well as external sources.
社内のアプリケーションや外部ソースから必要なデータを収集する。

Curate the data.
データをキュレートする。
Clean it, remove duplicates, fill missing values, label it, etc., and finally catalog and store it.
それをクリーニングし、重複を取り除き、欠落値を埋め、ラベルを付けるなどして、最終的にカタログ化して保管する。

Transform the data.
データを変換する。
Compute additional features, change the structure, etc.
追加機能の計算、構造の変更など。

Validate the data.
データを検証する。
Implement quality checks, log data distribution, etc.
品質チェック、ログデータ配信などの実施

Explore the data.
データを探る。
Exploratory data analysis, feature engineering, etc.
探索的データ分析、フィーチャーエンジニアリングなど
Most likely will lead to adding more transformations and data validation checks.
多くの場合、変換とデータ検証チェックを追加することになるだろう。

Train a model.
モデルを訓練する。
Run experiments, compare model performance, tune hyper-parameters, etc.
実験の実行、モデル性能の比較、ハイパーパラメータの調整など。

Evaluate the model characteristics against business objectives.
ビジネス目標に照らしてモデルの特性を評価する。
Any feedback may result in tweaking and formulating the ML problem differently.
どのようなフィードバックも、MLの問題を微調整し、別の形で定式化する結果になるかもしれない。

## Putting it All Together ♪すべてをまとめる

Both data science and software development are meant to serve business goals.
データサイエンスもソフトウェア開発も、ビジネスゴールに貢献するためのものだ。
In ML-assisted applications, model design has to be mindful of how it will impact user experience and the constraints of the production environment.
ML支援アプリケーションでは、モデル設計は、ユーザーエクスペリエンスと生産環境の制約にどのような影響を与えるかを念頭に置かなければならない。
Similarly, the software design must include inconspicuously collecting user feedback vital for model improvement.
同様に、ソフトウェアの設計には、モデルの改良に不可欠なユーザーからのフィードバックを目立たないように収集することが含まれていなければならない。

In ML-assisted products, model design and software design has a symbiotic relationship.
ML支援製品では、モデル設計とソフトウェア設計は共生関係にある。
The product design, the Plan step, has to consider both of these holistically, and that is the unifying step to join these two loops.
プランのステップである製品デザインは、この2つを総合的に考慮しなければならない。

A unified MLOps Lifecycle gives visibility to all constituents rather than developers thinking of models as a black box that data scientists somehow train and toss over, and data scientists developing models that don’t serve the intended business objectives in production.
統一されたMLOpsライフサイクルは、開発者がモデルをブラックボックスとして考え、データサイエンティストがなんとなく訓練して、その上に放り投げたり、データサイエンティストが本番で意図されたビジネス目的に役立たないモデルを開発したりするのではなく、すべての構成員に可視性を与える。

Data, ML, Data-ML, and DevOps loops can run in different cadences.
データ、ML、Data-ML、DevOpsのループは、それぞれ異なるケイデンスで実行することができる。
I always try to first build an end-to-end application with a rule-based or dummy model, cutting off the Data-ML loop entirely.
私はいつも、最初にルールベースまたはダミーモデルでエンド・ツー・エンドのアプリケーションを構築し、データ・MLのループを完全に断ち切るようにしている。
It works as a baseline, helps collect data, and also gives a context for data scientists to know how their model will be used.
これはベースラインとして機能し、データ収集に役立ち、またデータサイエンティストが自分のモデルがどのように使われるかを知るためのコンテキストを与える。

# Summary 要約

This article described the evolution of the ML lifecycle across the Data Warehouse, Big Data Lakes, and MLOps eras.
この記事では、データウェアハウス、ビッグデータレイク、MLOpsの各時代におけるMLのライフサイクルの進化について説明した。
It also explained how it can be modified by joining model development and DevOps loops, and the advantages of doing so.
また、モデル開発とDevOpsのループを結合することでどのように変更できるのか、その利点についても説明した。

# Refs: 参考文献

https://www.ml4devs.com/articles/mlops-survey-of-machine-learning-life-cycle/#references
https://www.ml4devs.com/articles/mlops-survey-of-machine-learning-life-cycle/#references