## link リンク

- https://www.ml4devs.com/articles/mlops-machine-learning-life-cycle/ https://www.ml4devs.com/articles/mlops-machine-learning-life-cycle/

# MLOps: Machine Learning Life Cycle MLOps 機械学習のライフサイクル

MLOps Lifecycle strings model and software development together in an unified machine learning life cycle.
MLOpsライフサイクルは、統一された機械学習ライフサイクルで、モデルとソフトウェア開発を一緒に紐付けます。

Building machine learning products or ML-assisted product features involve two distinct disciplines:
機械学習製品またはML-assistedな製品機能の構築には、2つの異なる分野が含まれる：

- **Model Development**: Data Scientists — highly skilled in statistics, linear algebra, and calculus — train, evaluate, and select the best-performing statistical or neural network model. モデル開発： 統計学、線形代数、微積分学に精通したデータサイエンティストが、最適な統計モデルまたはニューラルネットワークモデルをトレーニング、評価、選択します。(scientistの仕事)

- **Model Deployment**: Developers — highly skilled in software design and engineering — build a robust software system, deploy it on the cloud, and scale it to serve a huge number of concurrent model inference requests. モデルの展開： ソフトウェア設計とエンジニアリングに熟練した開発者が、堅牢なソフトウェアシステムを構築し、クラウド上にデプロイし、膨大な数の同時モデル推論リクエストに対応できるように拡張する。(ML engineerの仕事)

Of course, that is a gross over-simplification.
もちろん、それは単純化しすぎだ。
It takes several other vital expertise in building useful and successful ML-assisted products:
有用で成功するML支援製品の構築には、他にもいくつかの重要な専門知識が必要だ:

- **Data Engineering**: Build data pipelines to collect data from disparate sources, curate and transform it, and turn it into homogenous, clean data that can be safely used for training models. データエンジニアリング： 異種ソースからデータを収集し、キュレーションと変換を行い、モデルのトレーニングに安全に使用できる均質でクリーンなデータに変換するためのデータパイプラインを構築する。

- **Product Design**: Understand business needs, identify impactful objectives and relevant business matrices; define product features or user stories for those objectives, recognize the underlying problems that ML is better suitable to solve; design user experience to not only utilize ML model prediction seamlessly with rest of the product features but also collect user (re)action as implicit evaluation of the model results, and use it to improve the models. 製品設計： ビジネスニーズを理解し、インパクトのある目的と関連するビジネスマトリクスを特定する。これらの目的に対して製品の特徴やユーザーストーリーを定義し、MLが解決するのに適している根本的な問題を認識する。MLモデルの予測を製品の他の機能とシームレスに利用するだけでなく、モデル結果の暗黙の評価としてユーザの（再）行動を収集し、モデルの改善に役立てるためにユーザーエクスペリエンスを設計する。

- **Security Analysis**: Ensure that the software system, data, and model are secure, and no Personally Identifiable Information (PII) is revealed by combining model results and other publicly available information or data. セキュリティ分析： ソフトウェアシステム、データ、モデルの安全性を確保し、モデル結果と他の一般に入手可能な情報またはデータを組み合わせることによって、個人を特定できる情報（PII）が明らかにならないようにする。

- **AI Ethics**: Ensure adherence to all applicable laws, and add measures to protect against any kind of bias (e.g.limit the scope of the model, add human oversight, etc.)AIの倫理： 適用されるすべての法律の遵守を保証し、あらゆる種類のバイアスから保護する手段を追加する（モデルの範囲を制限する、人間の監視を追加するなど）。

As more models are being deployed in production, the importance of MLOps has naturally grown.
より多くのモデルがプロダクションに導入されるにつれて、MLOpsの重要性は当然高まっている。
There is an increasing focus on the seamless design and functioning of ML models within the overall product.
製品全体におけるMLモデルのシームレスな(=隙間がない??:thinking:)設計と機能にますます注目が集まっている。
Model Development can’t be done in a silo given the consequences it may have on the product and business.
モデル開発は、製品やビジネスへの影響を考えると、サイロで行うことはできない。

We need an ML lifecycle that is attuned to the realities of ML-assisted products and MLOps.
ML-assisted商品とMLOpsの現実に適応したMLライフサイクルが必要だ。
It should facilitate visibility for all stakeholders, without causing too many changes in the existing workflows of data scientists and engineers.
データサイエンティストやエンジニアの既存のワークフローに大きな変更を加えることなく、すべての利害関係者の可視化を促進する必要がある。

In the rest of the article, I first give an overview of the typical Model Development and Software Development workflows, and then how to bring the two together for adapting to the needs of building ML-assisted products in the MLOps era.
記事の続きでは、**まず典型的なモデル開発とソフトウェア開発のワークフロー**の概要を説明し、次にMLOps時代のML-assited製品構築のニーズに適応するために、**この2つをどのように結びつけるか**を説明する。

# Machine Learning Life Cycle 機械学習のライフサイクル

Let’s set aside deploying ML models online into production for a moment.
MLモデルをオンラインで本番環境にデプロイすることは少し脇に置いておこう。(i.e. Model Developmentだけに焦点を当てて考えるってことか:thinking:)
Data Scientists have been building statistical and neural-net models for over a decade.
データサイエンティストは、10年以上にわたって統計モデルやニューラルネットモデルを構築してきた。
Often, these models were used offline (i.e.executed manually) for predictive analytics.
多くの場合、**これらのモデルはオフラインで（つまり手作業で）予測分析に使用されていた**。(なるほど...!)

Model development consists of two sets of activities: data preparation and model training.
モデル開発には**2つの作業**がある: データの準備とモデルのトレーニングである。
Traditional machine learning life cycle starts with formulating an ML problem and ends with model evaluations.
従来の機械学習のライフサイクルは、MLの問題を定式化することから始まり、モデルの評価で終わる。

![](https://www.ml4devs.com/images/illustrations/ml-lifecycle-model-development.webp)

Machine Learning Life Cycle: Data-ML loop for model development

## Formulate 定式化

Data Scientists translate a business objective into a machine learning problem.
データサイエンティストは、ビジネスの目的を機械学習の問題に変換する。
There are several factors that you may need to consider:
考慮すべきいくつかの要素がある:

### Business Objective:

Narrow down to a small set of ML problems that can serve the business objective. ビジネスの目的 ビジネス目的に役立つMLの問題を絞り込む。

### Cost of Mistakes:

No ML model can be 100% accurate.
ミスのコスト： 100％正確なMLモデルは存在しない。
What are the cost of false positives and false negatives? For example, if an image classification model wrongly predicts breast cancer in a healthy person, further tests will rectify it.
偽陽性と偽陰性のコストは？例えば、画像分類モデルが健康な人の乳がんを誤って予測した場合、さらなる検査で修正される。
But if the model fails to diagnose cancer in a patient, then it can turn out to be fatal due to late detection.
しかし、もしこのモデルが患者の癌を診断できなければ、発見が遅れたために致命的な結果を招くことになる。
(予測が外れた場合にどの程度リスクがあるか? どの程度の誤りを許容できるか??の話かな:thinking:)

### Data Availability:

It may come as a surprise, but you may start with no data and bootstrap your data collection.
データの入手可能性： 意外に思われるかもしれないが、データがないところから始めて、データ収集をブートストラップすることもできる。
As the data becomes richer, it may make more types of models viable.
データがリッチになれば、より多くの種類のモデルが実行可能になるかもしれない。
For example, if you were to do anomaly detection with no labeled data, you may start with various kinds of unsupervised clustering algorithms and mark points that are not in any cluster as anomalies.
例えば、ラベル付けされたデータがない状態で異常検知を行う場合、様々な教師なしクラスタリングアルゴリズムから始めて、どのクラスタにも属さないポイントを異常としてマークすることができる。
But as you collect user reactions to your model, you will have a labeled dataset.
しかし、あなたのモデルに対するユーザーの反応を集めれば、ラベル付きデータセットができる。
Then you may want to try if a supervised classification model will perform better.
それなら、教師あり分類モデルの方がうまくいくかどうか試してみるのもいいだろう。

### Evaluation Metrics:

Depending upon problem formulation, you also should specify a model performance metric to optimize for, which should align with the business metric for your business objective.
評価指標： 問題の定式化に応じて、最適化するモデルのパフォーマンス指標を指定する必要があります。これは、**ビジネス目標のビジネス指標と一致させる**(=まあ相関させる??:thinking:)必要があります。

## Collect コレクト

Collect the necessary data from internal applications as well as external sources.
社内のアプリケーションや外部ソースから必要なデータを収集する。
It may be by scrapping the web, capturing event streams from your mobile app or web service, Change Data Capture (CDC) streams from operational (OLTP) databases, application logs, etc.
ウェブのスクラップ、モバイル・アプリやウェブ・サービスからのイベント・ストリームのキャプチャ、運用（OLTP）データベースからの変更データ・キャプチャ（CDC）ストリーム、アプリケーション・ログなどである。
You may ingest all of the needed data into your data pipeline, which is designed and maintained by Data Engineers.
データエンジニアが設計・管理するデータパイプラインに、必要なデータをすべて取り込むことができます。
Store the data in “raw / landing / bronze” zone in the data lake or warehouse.
データは、データレイクまたはウェアハウス内の「生／ランディング／ブロンズ」ゾーンに保存する。

## Curate キュレート

Collected data is almost never pristine.
収集されたデータは、ほとんど原始的なものではない。
You need clean it, remove duplicates, fill in missing values, and store it in “cleaned / augmented / silver” zone of a data lake or warehouse.
それを**クリーニングし、重複を削除し、欠損値を埋め**、データレイクやウェアハウスの「クリーニング／補強／シルバー」ゾーンに保存する必要がある。(こういうプロセスをcurateって呼ぶんだ??:thinking:)
If it is for training a supervised ML model, then you will also have to label it.
教師ありMLモデルのトレーニング用であれば、ラベル付けも必要だ。
Also, you must catalog it so that it can be easily discovered and correctly understood.
また、簡単に発見でき、正しく理解できるようにカタログ化しなければならない。
Try to automate as much as you can, but there will be parts to be done manually (labeling particularly).
できる限り自動化を試みるが、手作業で行う部分（特にラベリング）もあるだろう。

## Transform ♪ トランスフォーム

Once data has been cleaned, you can transform it to suit the analytics and ML modeling.
データがクリーニングされたら、アナリティクスやMLモデリングに適した形に変換することができる。
It may require changing the structure, joining with other tables, aggregating or summarizing along important dimensions, computing additional features, etc.
構造の変更、他のテーブルとの結合、重要な次元に沿った集計や要約、追加featureの計算などが必要になるかもしれない。
Store the results in “transformed / aggregated / gold” zone of data lake or warehouse.
**結果をデータレイクやウェアハウスの「transformed / aggregated / gold」ゾーンに保存する**。(うんうん、保存しておきたいよなぁ...:thinking:)
Data Engineers should automate all of it in the data pipeline.
データエンジニアは、**データパイプラインでそのすべてを自動化すべき**である。(digdagとかでやってもいいのかな。)

## Validate Validate

Implement quality checks, maintain logs of statistical distributions over time, and create triggers to alert when any of the checks fail or the distribution sways beyond expected limits.
品質チェックを実施し、経時的な統計分布のログを管理し、チェックに失敗したり、**予想される限界を超えて分布が揺れたりした場合に警告を発するトリガー**を作成する。(学習データの品質モニタリング、的な事か...!:thinking:)
Data Engineers in consultation with Data Scientists implement these validations in the data pipeline.
データエンジニアはデータサイエンティストと相談しながら、データパイプラインでこれらの検証を実施する。

## Explore 探索

Data Scientists perform Exploratory Data Analysis (EDA) to understand the relationships between various features and the target value they want the model to predict.
データサイエンティストは、様々な特徴とモデルが予測したい目標値との関係を理解するために、探索的データ分析（EDA）を行う。
They also do Feature Engineering, which is likely to lead to adding more transformation and validation checks (the previous two stages).
また、フィーチャー・エンジニアリングも行っており、これは（前の2つの段階である）変換と検証チェックをさらに追加することにつながるだろう。

## Train 学習

Data Scientists train multiple modes, run experiments, compare model performance, tune hyper-parameters, and select a couple of best-performing models.
データサイエンティストは、複数のモードを訓練し、実験を行い、モデルのパフォーマンスを比較し、ハイパーパラメータを調整し、最もパフォーマンスの高いモデルをいくつか選択する。

## Evaluate 評価する

Evaluate the model characteristics against business objectives and metrics.
ビジネス目標や指標に照らしてモデルの特性を評価する。
Some feedback may result in even tweaking and formulating the ML problem differently, and repeating the whole process all over again.
フィードバックによっては、MLの問題をさらに微調整し、別の形で定式化し、すべてのプロセスを繰り返すことになるかもしれない。

This Data-ML infinite loop is not linear.
このData-MLの無限ループはリニアではない。(後ろの文脈的に、一方通行ではないってこと??:thinking:)
At every stage, you don’t always move forward to the next stage.
どの段階でも、常に次の段階に進めるわけではない。
Upon discovering problems, you go back to the relevant previous stage to fit them.
**問題を発見したら、関連する前の段階に戻って問題を解決する**。
So there are implicit edges from each stage to previous stages.
つまり、各ステージから前のステージへの暗黙のエッジが存在する。

It is similar to the DevOps loop that developers follow.
これは、**開発者が従うDevOpsのループに似ている**。
Not every code that goes to the Test stage progresses to Release.
テスト段階に進んだすべてのコードがリリースに進むわけではない。
If the tests fail, it goes back to the Code (sometimes even to Plan) stage for problems to be rectified.
もしテストが失敗すれば、問題を修正するためにコード（場合によってはプラン）の段階に戻る。

# Software Development Life Cycle ソフトウェア開発ライフサイクル

The DevOps infinite loop is the de-facto standard for the software development lifecycle to rapidly build and deploy software applications and services on the cloud.
**DevOpsの無限ループ**は、クラウド上でソフトウェア・アプリケーションやサービスを迅速に構築・展開するためのソフトウェア開発ライフサイクルのデファクトスタンダードである。

It consists of two sets of activities: designing and developing a software system, and deploying and monitoring software services and applications.
これは**2つの活動**からなる: ソフトウェア・システムの設計(designing)と開発(development)、ソフトウェア・サービスとアプリケーションのデプロイ(deploying)とモニタリング(monitoring)。

## Plan プラン

This is the first stage for any product or product feature.
これは、どんな製品や製品機能にとっても最初の段階である。
You discuss the business objectives and key business metrics, and what product features can help achieve them.
ビジネス目標と主要なビジネス指標、そしてどのような製品機能がその達成に役立つかを議論します。
You drill down into the end-user problems and debate about user journeys to address those problems and collect required data to assess how an ML model is performing in the real world.
エンドユーザーの問題を掘り下げ、その問題に対処するためのユーザー・ジャーニーについて議論し、MLモデルが現実世界でどのように機能しているかを評価するために必要なデータを収集する。

## Code コード

Design and develop the software, the end-to-end product or application, and not just ML models.
MLモデルだけでなく、エンドツーエンドの製品やアプリケーションであるソフトウェアを**設計・開発**する。(設計も開発もここに含まれるんだ...!)
Establish contracts and APIs the application code uses to invoke the model inference and consume its results, and also what user reactions and feedback will be collected.
アプリケーションコードがモデル推論を呼び出し、その結果を利用するために使用するコントラクトとAPIを確立する。

It is very important to get developers, data engineers, and data scientists to get here on the same page.
開発者、データ・エンジニア、データ・サイエンティストが同じページに立つことは非常に重要だ。
That will reduce nasty surprises later.
そうすることで、後で嫌な驚きを減らすことができる。

## Build ビルド

This stage fuels the Continuous Integration of various parts as they evolve and package into a form that will be released.
この段階は、様々なパーツが進化し、リリースされる形にパッケージ化される際の継続的インテグレーション(Continuous Integration)を促進する。
It can be a library or SDK, a docker image, or an application binary (e.g.apk for Android apps).
ライブラリやSDK、Dockerイメージ、アプリケーション・バイナリ（Androidアプリの.apkなど）である。

## Test テスト

Unit tests, integration tests, coverage tests, performance tests, load tests, privacy tests, security tests, and bias tests.
ユニットテスト、統合テスト、カバレッジテスト、パフォーマンステスト、負荷テスト、プライバシーテスト、セキュリティテスト、バイアステスト。
Think of all kinds of software and ML model tests that are applicable here and automate them as much as feasible.
ここで適用できるあらゆる種類のソフトウェアと[MLモデルのテスト](https://www.ml4devs.com/newsletter/002-model-evaluation-vs-model-testing-vs-model-explainability/)を考え、**可能な限り自動化する**。

Testing is done on a staging environment that is similar to the targeted production environment but not designed for a similar scale.
テストは、対象とする本番環境に似ているが、同じような規模には設計されていないステージング環境で行われる。
It may have dummy, artificial, or anonymized data to test the software system end-to-end.
ソフトウェア・システムをエンド・ツー・エンドでテストするために、**ダミー、人工、あるいは匿名化されたデータを持つこともある**。

## Release

Once all automated tests pass and, in some cases, test results are manually inspected, the software code or models are approved for release.
すべての自動テストが合格し、場合によってはテスト結果が手作業で検査されると、ソフトウェア・コードやモデルのリリースが承認される。
Just like code, models should also be versioned and necessary metadata automatically captured.
コードと同様に、モデルもバージョン管理され、必要なメタデータが自動的に取り込まれるべきである。
Just as the docker images are versioned in a docker repo, the model should also be persisted in a model repo.
ドッカーイメージがドッカーリポジトリでバージョン管理されているように、**モデルもモデルリポジトリで永続化されるべき**です。

If models are packaged along with the code for the microservice that serves the model, then the docker image has the model image too.
モデルが、モデルを提供するマイクロサービスのコードと一緒にパッケージ化されている場合、Dockerイメージにはモデルイメージも含まれます。
This is where Continuous Integration ends and Continuous Deployment takes over.
ここで継続的インテグレーションは終了し、継続的デプロイが引き継がれる。

## Deploy デプロイ

Picking the released artifacts from the docker repo or model store and deploying it on production infrastructure.
リリースされた成果物をドッカーリポジトリまたはモデルストアから選び、本番インフラにデプロイする。(じゃあ成果物をDockerリポジトリやモデルストアにuploadする事をreleaseと呼んでる??:thinking:)
Depending upon your need, you may choose Infrastructure as a Service (IaaS), Container as a Service (CaaS), or Platform as a Service (PaaS).
ニーズに応じて、IaaS（Infrastructure as a Service）、CaaS（Container as a Service）、PaaS（Platform as a Service）を選択することができる。

You may also use TensorFlow Serve, PyTorch Serve, or services like SageMaker and Vertex AI to deploy your model services.
また、TensorFlow ServeやPyTorch Serve、あるいはSageMakerやVertex AIなどのサービスを利用して、モデル・サービスをデプロイすることもできる。

## Operate ♪ オペレート

Once the services are deployed, you may decide to send a small percentage of the traffic first.
サービスが展開されたら、まずトラフィックのごく一部を送信することにしてもよい。(A/Bテスト的な)
Canary Deployment is common tactic to update in phases (e.g.2%, 5%, 10%, 25%, 75%, 100%).
**カナリアデプロイ(Canary Deployment)**は、段階的（例えば2％、5％、10％、25％、75％、100％）に更新する一般的な戦術である。(blue greed deploymentと同様の、デプロイ方法の種類かな?)
In case of a problem, unexpected behavior, or a drop in metrics, you can roll back the deployment.
問題が発生した場合、予期しない動作が発生した場合、またはメトリクスが低下した場合は、**デプロイメントをロールバック**できます。

Once the gate is opened to 100% traffic, your deployment infra should gracefully bring down the old service.
ゲートが100％トラフィックに開放されれば、デプロイメント・インフラは**古いサービスを潔く停止させる**はずだ。
It should also scale as the load peaks and falls.
また、負荷のピークや下降に合わせてスケーリングする必要がある。
Kubernetes and KubeFlow are common tools for this purpose.
KubernetesとKubeFlowは、この目的のための一般的なツールである。

## Monitor モニター

In this final phase, you constantly monitor the health of services, errors, latencies, model predictions, outliers and distribution of input model features, etc.
この最終段階では、サービスの健全性、エラー、遅延、モデル予測、外れ値、入力モデルの特徴の分布などを常に監視する。
In case a problem arises, depending upon the severity and diagnosis, you may roll back the system to an older version, release a hotfix, trigger model re-training, or do whatever else is needed.
問題が発生した場合、深刻度と診断に応じて、システムを古いバージョンにロールバックしたり、hotfixをリリースしたり、モデルの再トレーニングを実施したり、その他必要なことを行うことができる。
(hotfix = ソフトウェアの特定の問題やバグを迅速に修正するためにリリースされる小規模な更新)

# MLOps Lifecycle MLOpsのライフサイクル

At the moment, it is quite common for data scientists to develop a model and then [“throw it over the wall”](https://wiki.c2.com/?ThrownOverTheWall) to developers and ML engineers to integrate with the rest of the system and deploy it in production.
現時点では、**データサイエンティストがモデルを開発し、それを開発者やMLエンジニアに「壁越しに投げて」他のシステムと統合し、本番稼動させるのが一般的**だ。

The ML and Dev silos and fragmented ownership are one of the most common reasons why many ML Projects fail.
**多くのMLプロジェクトが失敗する最も一般的な理由の1つは、MLとDev部門のサイロ化と所有権の分断**である。(なるほど...!)
Unifying the model and software development into one machine learning life cycle provides much-needed visibility to all stakeholders.
モデルとソフトウェア開発を**1つの機械学習ライフサイクルに統合する**ことで、すべての利害関係者に必要な可視性が提供される。

![](https://www.ml4devs.com/images/illustrations/ml-lifecycle-fusing-model-and-software-development.webp)

MLOps Lifecycle: Model Development and Software Development need to stitch together into unified Machine Learning Life Cycle.
MLOpsのライフサイクル： モデル開発とソフトウェア開発は、統一された機械学習ライフサイクルに統合する必要がある。

## Plan Step is the Starting Point プラン・ステップは出発点

Product planning comes before everything else.
商品企画は何よりも優先される。
Defining business objectives and designing user experiences should include not just product functionality, but also how model results and capturing user reactions will be blended into the production design.
ビジネス目標を定義し、ユーザー・エクスペリエンスをデザインするには、製品の機能性だけでなく、モデルの結果やユーザの反応をどのようにプロダクション・デザインに融合させるかを含める必要がある。

Unlike traditional software, when more data is collected with time, the user experience of the ML aspects of a product may need an update to benefit from it, even though there is no “new functionality.”
従来のソフトウェアとは異なり、**時間の経過とともにより多くのデータが収集されるようになると、"新しい機能"がないにもかかわらず、製品のML面でのユーザー・エクスペリエンスに、その恩恵を受けるためのアップデートが必要になる**ことがある。(機能を追加しない場合でも、時間の経過によって想定されるUXが変化しうるってことか。)

## First Build the Product Without ML First Build the Product Without ML

I often first build an end-to-end application with a rule-based heuristics or dummy model, cutting off the Data-ML loop entirely.
ルールベースのヒューリスティックスやダミーモデルを使ってエンド・ツー・エンドのアプリケーションを構築し、データ・MLのループを完全に遮断することがよくある。
That works as a baseline model and is useful in collecting data.
これは**ベースラインモデルとして機能し、データ収集に役立つ**。
It also gives context to the data scientists by showing how the model will be used in the product.
また、モデルが製品でどのように使用されるかを示すことで、データサイエンティストにcontextを与える。

## Different Cadence for Model and Software Development モデル開発とソフトウェア開発におけるケイデンスの違い

Developing an ML model is quite different from developing software.
MLモデルの開発は、ソフトウェアの開発とは全く異なる。
Software systems can be developed incrementally (with some parts not working).
ソフトウェア・システムは、(機能しない部分があっても)インクリメンタルに開発することができる。(feedbackをもらえる最小のタスクに分解できるってこと??)
Unlike software pieces, ML models can’t be broken into fine granularity.
**ソフトウェアの断片とは異なり、MLモデルは細かい粒度に分割することができない**。

A single lifecycle does not preclude Data, ML, Dev, and Ops wheels spinning at different speeds.
単一のライフサイクルは、**Data、ML、Dev、Opsの車輪が異なる速度で回転すること**を妨げるものではない。
In fact, it already happens in DevOps.
実際、DevOpsではすでにそうなっている。
At some teams, not every Dev sprint results in a new version being deployed.
チームによっては、すべての開発スプリントで新バージョンがデプロイされるわけではない。
On the other hand, some teams deploy new versions every hour, i.e.hundreds of times in a single sprint.
その一方で、1時間ごとに新しいバージョンをデプロイするチームもある。
Let every wheel spin at its own optimal speed.
各ホイールをそれぞれの最適なスピードで回転させる。

## Consolidated Ownership, Integrate Early, Iterate Often

These are my 3 percepts for improving the success rate in developing and deploying ML-assisted products:
以下が、ML-assited製品のdevelopmentとdeployingの成功率を向上させるための私の3つの認識である：

- **Consolidate Ownership**: Cross-functional team responsible for the end-to-end project 所有権の統合： エンド・ツー・エンドのプロジェクトに責任を持つ部門横断チーム。

- **Integrate Early**: Implement a simple (rule-based or dummy) model and develop a product feature end-to-end first. 早期に統合する： 単純な（ルールベースまたはダミーの）モデルを実装し、**最初に製品の機能をエンドツーエンドで開発**する。(まず動く一連の仕組みを作る。その後でモデルのcomponentだけを置き換える、みたいな事か:thinking:)

- Iterate Often: Build better models and replace the simple model, monitor, and repeat. 頻繁に反復する: より良いモデルを作り、単純なモデルを置き換え、監視し、繰り返す。

# Summary 要約

Machine Learning Life Cycle for MLOps era brings model development and software development together into one eternal knot.
MLOps時代の機械学習ライフサイクルは、モデル開発とソフトウェア開発を一つの無限の結び目にまとめる。
It facilitates visibility to all stakeholders in building ML-assisted products and features.
MLを活用した製品や機能の構築において、すべてのステークホルダーが可視化されやすくなる。

You may also enjoy reading about the survey of ML lifecycle from resource-constrained batch data mining to MLOps at the cloud scale.
リソースに制約のあるbatchデータマイニングからクラウドスケールでのMLOpsまで、[MLのライフサイクルに関する調査](https://www.ml4devs.com/articles/mlops-survey-of-machine-learning-life-cycle/)についての記事もお楽しみください。
