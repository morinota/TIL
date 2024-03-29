## link リンク

- https://aws.amazon.com/jp/blogs/machine-learning/how-booking-com-modernized-its-ml-experimentation-framework-with-amazon-sagemaker/ https://aws.amazon.com/jp/blogs/machine-learning/how-booking-com-modernized-its-ml-experimentation-framework-with-amazon-sagemaker/

# How Booking.com modernized its ML experimentation framework with Amazon SageMaker ブッキング・ドットコムがAmazon SageMakerでML実験フレームワークを最新化した方法

This post is co-written with Kostia Kofman and Jenny Tokar from Booking.com.
この投稿は、Booking.comのKostia Kofman氏とJenny Tokar氏との共著です。

As a global leader in the online travel industry, Booking.com is always seeking innovative ways to enhance its services and provide customers with tailored and seamless experiences.
オンライン旅行業界のグローバルリーダーとして、Booking.comは常にサービスを強化し、お客様に合わせたシームレスな体験を提供する革新的な方法を模索しています。
The Ranking team at Booking.com plays a pivotal role in ensuring that the search and recommendation algorithms are optimized to deliver the best results for their users.
Booking.comのRankingチームは、**検索と推薦のアルゴリズムがユーザーに最高の結果をもたらすように最適化されることを保証する上で極めて重要な役割**を果たしています。

Sharing in-house resources with other internal teams, the Ranking team machine learning (ML) scientists often encountered long wait times to access resources for model training and experimentation – challenging their ability to rapidly experiment and innovate.
社内のリソースを他の社内チームと共有するランキングチームの機械学習（ML）サイエンティストは、**モデルのトレーニングや実験のためのリソースにアクセスするのに長い待ち時間がかかることが多く、迅速な実験とイノベーションを行うことが困難だった**。
Recognizing the need for a modernized ML infrastructure, the Ranking team embarked on a journey to use the power of Amazon SageMaker to build, train, and deploy ML models at scale.
**近代化されたMLインフラストラクチャの必要性を認識**したランキング・チームは、Amazon SageMakerのパワーを使ってMLモデルの構築、トレーニング、デプロイを大規模に行う旅に出た。

Booking.com collaborated with AWS Professional Services to build a solution to accelerate the time-to-market for improved ML models through the following improvements:
Booking.comは、AWS Professional Servicesと協力し、以下の改善を通じて**MLモデルの改良の市場投入までの時間を短縮する**ソリューションを構築した：

- Reduced wait times for resources for training and experimentation
  トレーニングや実験に必要なリソースの待ち時間を短縮

- Integration of essential ML capabilities such as hyperparameter tuning
  ハイパーパラメータのチューニングなど、MLに不可欠な機能の統合

- A reduced development cycle for ML models
  MLモデルの開発サイクルの短縮

Reduced wait times would mean that the team could quickly iterate and experiment with models, gaining insights at a much faster pace.
待ち時間が減るということは、チームがモデルを素早く反復(iterate)して実験できることを意味し、より速いペースで洞察を得ることができる。
Using SageMaker on-demand available instances allowed for a tenfold wait time reduction.
オンデマンドで利用可能な SageMaker インスタンスを使用することで、待ち時間を 10 分の 1 に短縮することができました。
(**ここでon-demandとは、事前にリソースを確保する必要がなく、必要に応じてリソースを使用ｄけいる。そして使用した分だけ料金を支払うような柔軟な利用方法、みたいな??**:thinking_face:)
Essential ML capabilities such as hyperparameter tuning and model explainability were lacking on premises.
ハイパーパラメータのチューニングやモデルの説明可能性といったMLに不可欠な機能は、前提条件として欠けていた。
The team’s modernization journey introduced these features through Amazon SageMaker Automatic Model Tuning and Amazon SageMaker Clarify.
チームの近代化の旅は、Amazon SageMaker Automatic Model Tuning と Amazon SageMaker Clarify を通じて、これらの機能を導入しました。(後者はどんなサービスだろう??:thinking_face:)
Finally, the team’s aspiration was to receive immediate feedback on each change made in the code, reducing the feedback loop from minutes to an instant, and thereby reducing the development cycle for ML models.
最後に、チームの願望は、**コードの変更ごとに即座のフィードバックを受け取り**、**フィードバックループを分単位から瞬時に短縮**し、MLモデルの開発サイクルを短縮することでした。
(コードをcommmitする度に自動的にビルドやテストが行われて、エラーやバグを早期に発見できる、みたいなcontinuous integrationの概念の話かな。Sagemakerのサービスで実現できるの??:thinking_face:)

In this post, we delve into the journey undertaken by the Ranking team at Booking.com as they harnessed the capabilities of SageMaker to modernize their ML experimentation framework.
この投稿では、Booking.comのランキングチームがSageMakerの機能を活用してML実験のフレームワークを近代化するために行った旅について掘り下げます。
By doing so, they not only overcame their existing challenges, but also improved their search experience, ultimately benefiting millions of travelers worldwide.
そうすることで、既存の課題を克服しただけでなく、検索エクスペリエンスを向上させ、**最終的には世界中の何百万人もの旅行者に利益をもたらした**。(開発者も嬉しくて、ユーザも嬉しくて、最高じゃん...!:clap:)

## Approach to modernization 近代化へのアプローチ

The Ranking team consists of several ML scientists who each need to develop and test their own model offline.
ランキングチームは複数のMLサイエンティストで構成され、それぞれがオフラインでモデルを開発し、テストする必要がある。
When a model is deemed successful according to the offline evaluation, it can be moved to production A/B testing.
オフライン評価で成功したと判断されたモデルは、本番のA/Bテストに移行することができる。
If it shows online improvement, it can be deployed to all the users.
オンラインで改善が見られれば、全ユーザーに配備することができる。

The goal of this project was to create a user-friendly environment for ML scientists to easily run customizable Amazon SageMaker Model Building Pipelines to test their hypotheses without the need to code long and complicated modules.
このプロジェクトの目標は、**長く複雑なモジュールをコーディングする必要なく、ML科学者が仮説を検証するためにカスタマイズ可能なAmazon SageMakerモデル構築パイプラインを簡単に実行できる**ユーザーフレンドリーな環境を作ることでした。

One of the several challenges faced was adapting the existing on-premises pipeline solution for use on AWS.
直面したいくつかの**課題の1つは、既存のオンプレミス・パイプライン・ソリューションをAWS上で使用できるようにすること**だった。(かつては、ローカル環境でオフライン実験を走らせてた、みたいな事??:think)
The solution involved two key components:
この解決策には2つの重要な要素があった：

- Modifying and extending existing code – The first part of our solution involved the modification and extension of our existing code to make it compatible with AWS infrastructure.
  既存のコードの修正と拡張 - 私たちのソリューションの最初の部分は、**AWSインフラストラクチャと互換性を持たせるために、既存のコードの修正と拡張**を行いました。
  This was crucial in ensuring a smooth transition from on-premises to cloud-based processing.
  これは、オンプレミスからクラウドベースの処理へのスムーズな移行を保証する上で極めて重要だった。
  (基本的には、外部リソースとのやりとりの箇所だけ修正したら良いはず...??:thinking_face:)

- Client package development – A client package was developed that acts as a wrapper around SageMaker APIs and the previously existing code.
  クライアント・パッケージの開発 - SageMakerのAPIと以前の既存のコードをラップするラッパーとして機能するクライアント・パッケージが開発されました。
  This package combines the two, enabling ML scientists to easily configure and deploy ML pipelines without coding.
  このパッケージは、2つを組み合わせ、**ML科学者がコーディングなしで簡単にMLパイプラインを構成してデプロイできるようにします**。(あ、Sagemaker Python SDKのFacadeみたいなものを用意した、みたいな感じなのかな...??:thinking_face:)

## SageMaker pipeline configuration SageMaker パイプラインの設定

Customizability is key to the model building pipeline, and it was achieved through config.ini, an extensive configuration file.
**カスタマイズ性はモデル構築パイプラインの鍵**であり、広範な設定ファイルである`config.ini`によって実現された。(pipeline DSL以外にもconfigファイルを使う??:thinking_face:)
This file serves as the control center for all inputs and behaviors of the pipeline.
このファイルは、パイプラインのすべての入力と振る舞いのコントロールセンターとして機能します。
(事前に実験用Pipelineの雛形を固定しておき、実験者はその都度configファイルに値を指定してデプロイするだけでいい、みたいな点はいいなと思った...!:thinking_face:)

Available configurations inside config.ini include:
`config.ini`内で利用可能な設定は以下の通り：

- Pipeline details – The practitioner can define the pipeline’s name, specify which steps should run, determine where outputs should be stored in Amazon Simple Storage Service (Amazon S3), and select which datasets to use
  パイプラインの詳細 - プラクティショナー(=実験する人?)は、パイプラインの名前を定義し、どのステップを実行するかを指定し、Amazon Simple Storage Service (Amazon S3) に出力を保存する場所を決定し、使用するデータセットを選択できます。

- AWS account details – You can decide which Region the pipeline should run in and which role should be used
  AWSアカウントの詳細 - パイプラインを実行するリージョンと、使用するロールを決定できます。

- Step-specific configuration – For each step in the pipeline, you can specify details such as the number and type of instances to use, along with relevant parameters
  ステップ固有の設定 - パイプライン内の各ステップについて、使用するインスタンスの数とタイプ、関連するパラメータなどの詳細を指定できます。
  (実験用のpipelineテンプレートが存在していて、たぶんstep数とかは固有な感じかな...!:thinking_face:)

The following code shows an example configuration file:
次のコードは、コンフィギュレーション・ファイルの例を示している：

```ini
[BUILD]
pipeline_name = ranking-pipeline
steps = DATA_TRANFORM, TRAIN, PREDICT, EVALUATE, EXPLAIN, REGISTER, UPLOAD
train_data_s3_path = s3://...
...
[AWS_ACCOUNT]
region = eu-central-1
...
[DATA_TRANSFORM_PARAMS]
input_data_s3_path = s3://...
compression_type = GZIP
....
[TRAIN_PARAMS]
instance_count = 3
instance_type = ml.g5.4xlarge
epochs = 1
enable_sagemaker_debugger = True
...
[PREDICT_PARAMS]
instance_count = 3
instance_type = ml.g5.4xlarge
...
[EVALUATE_PARAMS]
instance_type = ml.m5.8xlarge
batch_size = 2048
...
[EXPLAIN_PARAMS]
check_job_instance_type = ml.c5.xlarge
generate_baseline_with_clarify = False
....
```

config.ini is a version-controlled file managed by Git, representing the minimal configuration required for a successful training pipeline run.
`config.ini`はGitによってバージョン管理されるファイルで、トレーニングパイプラインの実行に必要な最小限の設定を表します。
During development, local configuration files that are not version-controlled can be utilized.
**開発中は、バージョン管理されていないローカル設定ファイルを利用することができる**。(各データサイエンティストがローカルからpipelineをビルドするって事?)
These local configuration files only need to contain settings relevant to a specific run, introducing flexibility without complexity.
これらのローカル・コンフィギュレーション・ファイルには、特定の実行に関連する設定だけが含まれていればよく、複雑さを伴わない柔軟性が導入されている。(指定しないconfigはデフォルト値が指定されるってことか!)
The pipeline creation client is designed to handle multiple configuration files, with the latest one taking precedence over previous settings.
パイプライン作成クライアントは、複数の設定ファイルを扱えるように設計されており、最新の設定ファイルが以前の設定よりも優先されます。(同名のpipelineの話かな...!)

## SageMaker pipeline steps SageMaker パイプラインのステップ

The pipeline is divided into the following steps:
パイプラインは以下のステップに分かれている：
(これが実験用pipelineのstepを定義したテンプレートか...!)

- **Train and test data preparation** – Terabytes of raw data are copied to an S3 bucket, processed using AWS Glue jobs for Spark processing, resulting in data structured and formatted for compatibility.
  訓練データとテストデータの準備 - **テラバイト(やっぱり大きいな...!)の生データ**がS3バケットにコピーされ、Spark処理用のAWS Glueジョブを使用して処理されます。(=ここはProcssingJobじゃなくてGlueを使う??)

- **Train** – The training step uses the TensorFlow estimator for SageMaker training jobs.
  Train - トレーニングステップでは、SageMakerトレーニングジョブ用のTensorFlow Estimatorが使用されます。(=じゃあAWS提供のdocker imageを使ってるんだ...!やっぱり独自imageが必要なケースってそこまで多くない気がするなぁ...!:thinking_face:)
  Training occurs in a distributed manner using Horovod, and the resulting model artifact is stored in Amazon S3.
  トレーニングはHorovodを使用して分散方式で行われ、得られたmodel artifactはAmazon S3に保存されます。
  For hyperparameter tuning, a hyperparameter optimization (HPO) job can be initiated, selecting the best model based on the objective metric.
  ハイパーパラメータのチューニングのために、**hyperparameter optimization (HPO) ジョブ**を開始し、目的指標に基づいて最適なモデルを選択することができる。

- **Predict** – In this step, a SageMaker Processing job uses the stored model artifact to make predictions.
  予測 - このステップでは、SageMaker Processing ジョブは保存されたmodel artifactを使用して予測を行います。(=ここはbatch transformじゃなくてProcessingJobを使うんだ...!batch transformJobの場合は、model artifactを事前にmodel resourceに変換しておく必要があるからかな...!:thinking_face:)
  This process runs in parallel on available machines, and the prediction results are stored in Amazon S3.
  このプロセスは**利用可能なマシン上で並行して実行**され、予測結果はAmazon S3に保存される。

- Evaluate – A PySpark processing job evaluates the model using a custom Spark script.
  Evaluate - PySparkのprocessingジョブは、カスタムのSparkスクリプトを使用してモデルを評価します。(Spark使ってるのはサイズがデカいから??)
  The evaluation report is then stored in Amazon S3.
  評価レポートはAmazon S3に保存される。

- Condition – After evaluation, a decision is made regarding the model’s quality.
  コンディション - 評価の結果、モデルの品質が決定される。
  This decision is based on a condition metric defined in the configuration file.
  この決定(=condition stepによる条件分岐...!)は、configファイルで定義された条件メトリックに基づいて行われる。
  If the evaluation is positive, the model is registered as approved; otherwise, it’s registered as rejected.
  評価が肯定的であれば、そのモデルは承認されたものとして登録され、そうでなければ拒否されたものとして登録される。(architecture図を見ると、Model Registryを使ってるっぽい...!:thinking_face:)
  In both cases, the evaluation and explainability report, if generated, are recorded in the model registry.
  **どちらの場合も、evaluationとexplainabilityレポートが生成された場合は、モデルレジストリに記録されます**。(ふむふむ良い場合も悪い場合もモデルレジストリに記録するのか...!)

- Package model for inference – Using a processing job, if the evaluation results are positive, the model is packaged, stored in Amazon S3, and made ready for upload to the internal ML portal.
  推論のためにモデルをパッケージ化する - 処理ジョブを使用して、評価結果が肯定的であれば、モデルはパッケージ化され、Amazon S3に保存され、内部のMLポータルにアップロードできるようになる。

- Explain – SageMaker Clarify generates an explainability report.
  説明 - SageMaker Clarify は、説明可能性レポートを生成します。
  (Sagemaker Clarify = データセットやMLモデルのバイアス検出とモデル解釈の機能を提供するサービスっぽい...! 特徴量の寄与度の分析とか...! :thinking_face:)

Two distinct repositories are used.
2つの異なるリポジトリが使用されている。
The first repository contains the definition and build code for the ML pipeline, and the second repository contains the code that runs inside each step, such as processing, training, prediction, and evaluation.
**最初のリポジトリには、MLパイプラインの定義とビルドコードが含まれ、2番目のリポジトリには、処理、トレーニング、予測、評価などの各ステップ内で実行されるコードが含まれます。**(リポジトリを2つに分けているんだ...!)
This dual-repository approach allows for greater modularity, and enables science and engineering teams to iterate independently on ML code and ML pipeline components.
**このdual-repositoryのアプローチは、より良いモジュール性を実現し、データサイエンスチームとエンジニアリングチームがMLコードとMLパイプラインのコンポーネントについて独立してiterationすることを可能にします**。(リポジトリを1つにまとめるか2つに分けるかは、トレードオフだから、開発組織の状況によって良し悪しは異なりそう...!:thinking_face:)
The following diagram illustrates the solution workflow.
次の図は、ソリューションのワークフローを示している。

![]()

<!-- ここまで読んだ! -->

## Automatic model tuning 自動モデルチューニング

Training ML models requires an iterative approach of multiple training experiments to build a robust and performant final model for business use.
MLモデルのトレーニングは、**ビジネスで使用するためのロバストでパフォーマンスの高いfinal modelを構築するため**に、何度もトレーニング実験を繰り返す必要がある。
The ML scientists have to select the appropriate model type, build the correct input datasets, and adjust the set of hyperparameters that control the model learning process during training.
MLの科学者は、適切なモデルタイプを選択し、正しい入力データセットを構築し、学習中にモデルの学習プロセスを制御するハイパーパラメータのセットを調整しなければならない。

The selection of appropriate values for hyperparameters for the model training process can significantly influence the final performance of the model.
**モデル学習プロセスにおけるハイパーパラメータの適切な値の選択**は、モデルの最終的な性能に大きく影響する。
However, there is no unique or defined way to determine which values are appropriate for a specific use case.
しかし、どの値が特定のユースケースにふさわしいかを判断するための、独自の、あるいは定義された方法はない。
Most of the time, ML scientists will need to run multiple training jobs with slightly different sets of hyperparameters, observe the model training metrics, and then try to select more promising values for the next iteration.
ほとんどの場合、ML研究者は、わずかに異なるハイパーパラメータのセットで複数のトレーニングジョブを実行し、モデルのトレーニングメトリクスを観察し、次のiterationの為により有望な値を選択しようとします。(手動でのHPOかー...!)
This process of tuning model performance is also known as hyperparameter optimization (HPO), and can at times require hundreds of experiments.
モデルの性能をチューニングするこのプロセスは、ハイパーパラメータ最適化（HPO）としても知られており、時には数百回もの実験を必要とすることもある。

The Ranking team used to perform HPO manually in their on-premises environment because they could only launch a very limited number of training jobs in parallel.
**ランキング・チームはオンプレミス環境でHPOを手作業で行っていたが**、それは並行して起動できるトレーニング・ジョブの数が非常に限られていたからだ。(booking.comさんでもこれってことは安心するなぁ...!:thinking_face:)
Therefore, they had to run HPO sequentially, test and select different combinations of hyperparameter values manually, and regularly monitor progress.
そのため、HPOを順次実行し、ハイパーパラメータ値のさまざまな組み合わせを手動でテストして選択し、進捗状況を定期的に監視する必要があった。
This prolonged the model development and tuning process and limited the overall number of HPO experiments that could run in a feasible amount of time.
このため、モデル開発とチューニングのプロセスが長引き、実行可能な時間内に実施できるHPO実験の全体数が制限された。

With the move to AWS, the Ranking team was able to use the automatic model tuning (AMT) feature of SageMaker.
AWSへの移行に伴い、ランキングチームはSageMakerの**automatic model tuning（AMT）機能**を利用できるようになった。
AMT enables Ranking ML scientists to automatically launch hundreds of training jobs within hyperparameter ranges of interest to find the best performing version of the final model according to the chosen metric.
AMTにより、ランキングMLの科学者は、関心のあるハイパーパラメータの範囲内で何百ものトレーニングジョブを自動的に起動し、選択されたメトリックに従って最終モデルの最高のパフォーマンスバージョンを見つけることができる。
The Ranking team is now able choose between four different automatic tuning strategies for their hyperparameter selection:
ランキングチームは、ハイパーパラメータの選択について、**4つの異なる自動チューニング戦略**から選択できるようになった:

- **Grid search** – AMT will expect all hyperparameters to be categorical values, and it will launch training jobs for each distinct categorical combination, exploring the entire hyperparameter space.
  グリッド探索 - AMTはすべてのハイパーパラメータがカテゴリー値であることを想定し、各カテゴリーの組み合わせに対してトレーニングジョブを起動し、ハイパーパラメータ空間全体を探索する。

- **Random search** – AMT will randomly select hyperparameter values combinations within provided ranges.
  ランダム検索 - AMTは、指定された範囲内のハイパーパラメータ値の組み合わせをランダムに選択します。
  Because there is no dependency between different training jobs and parameter value selection, multiple parallel training jobs can be launched with this method, speeding up the optimal parameter selection process.
  異なるトレーニングジョブとパラメータ値選択の間に依存関係がないため、**この方法では複数の並列トレーニングジョブを起動することができ、最適なパラメータ選択プロセスを高速化**できる。

- **Bayesian optimization** – AMT uses Bayesian optimization implementation to guess the best set of hyperparameter values, treating it as a regression problem.
  ベイズ最適化 - AMTは、ベイズ最適化実装を使用して、回帰問題として扱い、最適なハイパーパラメータ値のセットを推測します。
  It will consider previously tested hyperparameter combinations and its impact on the model training jobs with the new parameter selection, optimizing for smarter parameter selection with fewer experiments, but it will also launch training jobs only sequentially to always be able to learn from previous trainings.
  これは、以前にテストされたハイパーパラメータの組み合わせと、新しいパラメータ選択によるモデル訓練ジョブへの影響を考慮し、より少ない実験でよりスマートなパラメータ選択を最適化する。

- **Hyperband** – AMT will use intermediate and final results of the training jobs it’s running to dynamically reallocate resources towards training jobs with hyperparameter configurations that show more promising results while automatically stopping those that underperform.
  ハイパーバンド - AMTは、実行中のトレーニングジョブの中間結果と最終結果を使用して、より有望な結果を示すハイパーパラメータ設定のトレーニングジョブに動的にリソースを再配分し、パフォーマンスが低下したトレーニングジョブは自動的に停止します。
  (中間成績が悪かったハイパーパラメータ候補は、早期でジョブを終了させる事で、探索を効率化するような戦略...??:thinking_face:)

AMT on SageMaker enabled the Ranking team to reduce the time spent on the hyperparameter tuning process for their model development by enabling them for the first time to run multiple parallel experiments, use automatic tuning strategies, and perform double-digit training job runs within days, something that wasn’t feasible on premises.
SageMaker 上の AMT により、Ranking チームは、複数の並列実験の実行、自動チューニング戦略の使用、**2桁のトレーニングジョブの実行を初めて数日以内に行うことができるようになり**、モデル開発のためのハイパーパラメータチューニングプロセスに費やす時間を短縮することができました。

<!-- ここまで読んだ! -->

## Model explainability with SageMaker Clarify SageMaker Clarifyによるモデル説明可能性

Model explainability enables ML practitioners to understand the nature and behavior of their ML models by providing valuable insights for feature engineering and selection decisions, which in turn improves the quality of the model predictions.
モデルの説明可能性は、ML実務者が**特徴エンジニアリングと選択決定のための貴重な洞察を提供**することによって、**MLモデルの性質と挙動を理解**することを可能にし、その結果、**モデル予測の品質が向上**します。
The Ranking team wanted to evaluate their explainability insights in two ways: understand how feature inputs affect model outputs across their entire dataset (global interpretability), and also be able to discover input feature influence for a specific model prediction on a data point of interest (local interpretability).
ランキングチームは、説明可能性の洞察を**2つの方法**で評価したいと考えていた: 特徴入力がデータセット全体にわたってモデル出力にどのように影響するかを理解する(**global interpretablity**)、そして特定のデータポイントに対するモデル予測の入力特徴量の影響を発見することができる(**local interpretability**)。
With this data, Ranking ML scientists can make informed decisions on how to further improve their model performance and account for the challenging prediction results that the model would occasionally provide.
このデータがあれば、ランキングMLの科学者は、モデルの性能をさらに向上させる方法や、モデルが時折出す困難な予測結果を考慮する方法について、情報に基づいた決定を下すことができる。

SageMaker Clarify enables you to generate model explainability reports using Shapley Additive exPlanations (SHAP) when training your models on SageMaker, supporting both global and local model interpretability.
SageMaker Clarify を使用すると、SageMaker でモデルをトレーニングする際に、Shapley Additive exPlanations (SHAP) を使用してモデルの説明可能性レポートを生成することができ、グローバルおよびローカルの両方のモデルの解釈可能性をサポートします。
In addition to model explainability reports, SageMaker Clarify supports running analyses for pre-training bias metrics, post-training bias metrics, and partial dependence plots.
モデルの説明可能性レポートに加え、SageMaker Clarifyは、トレーニング前のバイアスメトリクス、トレーニング後のバイアスメトリクス、およびpartial dependence plotsの分析を実行することをサポートしています。(PDPなつかしい...!:thinking_face:)
The job will be run as a SageMaker Processing job within the AWS account and it integrates directly with the SageMaker pipelines.
**ジョブは AWS アカウント内で SageMaker Processing ジョブとして実行され、SageMaker パイプラインと直接統合されます**。(Sagemaker ClarifyのジョブはProcessingJobとして実行されるんだ...!)

The global interpretability report will be automatically generated in the job output and displayed in the Amazon SageMaker Studio environment as part of the training experiment run.
グローバルインタープリタビリティレポートは、ジョブの出力に自動的に生成され、トレーニング実験の実行の一部として Amazon SageMaker Studio 環境に表示されます。
If this model is then registered in SageMaker model registry, the report will be additionally linked to the model artifact.
**このモデルが SageMaker モデルレジストリに登録されると、レポートはmodel artifactに追加でリンクされます**。(MLflowみたい! Tracking情報を紐付けてくれるのはいいね...!:thinking_face:)
Using both of these options, the Ranking team was able to easily track back different model versions and their behavioral changes.
この2つのオプションを使用することで、ランキングチームは異なるモデルのバージョンとその動作の変化を簡単にtrack back(追跡)することができました。

To explore input feature impact on a single prediction (local interpretability values), the Ranking team enabled the parameter save_local_shap_values in the SageMaker Clarify jobs and was able to load them from the S3 bucket for further analyses in the Jupyter notebooks in SageMaker Studio.
1つの予測値(local interpretability values)に対する入力特徴量の影響を探るために、ランキングチームはSageMaker Clarifyジョブでパラメータsave_local_shap_valuesを有効にし、SageMaker StudioのJupyterノートブックでさらなる分析のためにそれらをS3バケットからロードすることができました。

![]()

The preceding images show an example of how a model explainability would look like for an arbitrary ML model.
先の画像は、任意のMLモデルに対するモデルの説明可能性の例を示している。

<!-- ここまで読んだ! -->

## Training optimization トレーニングの最適化

The rise of deep learning (DL) has led to ML becoming increasingly reliant on computational power and vast amounts of data.
ディープラーニング（DL）の台頭により、MLは計算能力と膨大なデータへの依存度を高めている。
ML practitioners commonly face the hurdle of efficiently using resources when training these complex models.
MLの実務者は、このような複雑な(=time complexityの大きい!)モデルをトレーニングする際に、**リソースを効率的に使用するというハードルに直面するのが一般的**だ。
When you run training on large compute clusters, various challenges arise in optimizing resource utilization, including issues like I/O bottlenecks, kernel launch delays, memory constraints, and underutilized resources.
大規模な計算クラスタでトレーニングを実行すると、**I/Oのボトルネック、カーネルの起動の遅延、メモリの制約、リソースの未使用など、リソースの利用を最適化するためのさまざまな課題が発生**します。
If the configuration of the training job is not fine-tuned for efficiency, these obstacles can result in suboptimal hardware usage, prolonged training durations, or even incomplete training runs.
トレーニングジョブの構成が効率化のために微調整されていない場合、これらの障害により、**ハードウェアの使用率が最適でなくなったり、トレーニング時間が長くなったり、トレーニングの実行が不完全になったりする可能性**がある。
These factors increase project costs and delay timelines.
これらの要因は、プロジェクト・コストを増加させ、スケジュールを遅らせる。

Profiling of CPU and GPU usage helps understand these inefficiencies, determine the hardware resource consumption (time and memory) of the various TensorFlow operations in your model, resolve performance bottlenecks, and, ultimately, make the model run faster.
**CPUとGPUの使用状況のプロファイリング**は、これらの非効率性を理解し、モデル内のさまざまなTensorFlow操作のハードウェアリソース消費(時間とメモリ)を決定し、パフォーマンスのボトルネックを解決し、最終的にモデルを高速化するのに役立ちます。

Ranking team used the framework profiling feature of Amazon SageMaker Debugger (now deprecated in favor of Amazon SageMaker Profiler) to optimize these training jobs.
ランキングチームは、**Amazon SageMaker Debuggerのframework profiling機能** (現在は**Amazon SageMaker Profiler**に置き換えられています) を使用して、これらのトレーニングジョブを最適化しました。(インスタンス最適化のためのサービスがあるっぽい...!?これ自体はインスタンスを必要としないので利用料金は無料...!:thinking_face:)
This allows you to track all activities on CPUs and GPUs, such as CPU and GPU utilizations, kernel runs on GPUs, kernel launches on CPUs, sync operations, memory operations across GPUs, latencies between kernel launches and corresponding runs, and data transfer between CPUs and GPUs.
これにより、**CPUとGPU上のすべてのアクティビティを追跡**できます。CPUとGPUの利用、GPU上でのカーネルの実行、CPU上でのカーネルの起動、同期操作、GPU間のメモリ操作、カーネルの起動と対応する実行の間の遅延、CPUとGPU間のデータ転送などです。

Ranking team also used the TensorFlow Profiler feature of TensorBoard, which further helped profile the TensorFlow model training.
ランキングチームは、TensorBoardのTensorFlow Profiler機能も使用し、TensorFlowモデルのトレーニングのプロファイリングをさらに支援した。
SageMaker is now further integrated with TensorBoard and brings the visualization tools of TensorBoard to SageMaker, integrated with SageMaker training and domains.
SageMakerは、TensorBoardとさらに統合され、SageMakerトレーニングとドメインに統合されたTensorBoardの可視化ツールを提供します。
TensorBoard allows you to perform model debugging tasks using the TensorBoard visualization plugins.
TensorBoardでは、TensorBoard可視化プラグインを使用してモデルのデバッグタスクを実行できます。(TensorBoard = TensorFlow専用の視覚化ツール?)

With the help of these two tools, Ranking team optimized the their TensorFlow model and were able to identify bottlenecks and reduce the average training step time from 350 milliseconds to 140 milliseconds on CPU and from 170 milliseconds to 70 milliseconds on GPU, speedups of 60% and 59%, respectively.
これら2つのツールの助けを借りて、ランキングチームはTensorFlowモデルを最適化し、CPU上の平均トレーニングステップ時間を350ミリ秒から140ミリ秒、GPU上の平均トレーニングステップ時間を170ミリ秒から70ミリ秒に短縮し、それぞれ**60%と59%の高速化を実現**しました。

<!-- ここまで読んだ! -->

## Business outcomes ビジネスの成果

The migration efforts centered around enhancing availability, scalability, and elasticity, which collectively brought the ML environment towards a new level of operational excellence, exemplified by the increased model training frequency and decreased failures, optimized training times, and advanced ML capabilities.
**この移行(migration)の取り組みは、availability(可用性)、scalability(スケーラビリティ)、elasticity(弾力性)の向上を中心に据えています**。(=アーキテクチャ品質の改善?)
これらが集合的に(作用したことで?)、モデルトレーニングの頻度の増加、失敗の減少、トレーニング時間の最適化、高度なML能力(=精度改善?)など、新しいレベルの運用の優れた環境にML環境をもたらしました。

### Model training frequency and failures モデルトレーニングの頻度と失敗

The number of monthly model training jobs increased fivefold, leading to significantly more frequent model optimizations.
**毎月のモデルトレーニングジョブの数(実行数?)は5倍に増え**、モデルの最適化の頻度が大幅に増えた。
Furthermore, the new ML environment led to a reduction in the failure rate of pipeline runs, dropping from approximately 50% to 20%.
さらに、新しいML環境は、**パイプラインの失敗率を約50％から20％へと減少させた**。
The failed job processing time decreased drastically, from over an hour on average to a negligible 5 seconds.
失敗したジョブの処理時間は、平均で1時間以上から無視できる5秒に大幅に減少した。(復旧速度が向上したって事?)
This has strongly increased operational efficiency and decreased resource wastage.
これによって業務効率が大幅に向上し、**リソースの無駄を減らすことができた**。

### Optimized training time トレーニング時間の最適化

The migration brought with it efficiency increases through SageMaker-based GPU training.
この移行は、SageMakerベースの**GPUトレーニングによる効率化**をもたらした。
This shift decreased model training time to a fifth of its previous duration.
このシフトにより、**モデルのトレーニング時間は以前の5分の1に短縮**された。
Previously, the training processes for deep learning models consumed around 60 hours on CPU; this was streamlined to approximately 12 hours on GPU.
従来、ディープラーニングモデルの学習プロセスにはCPUで約60時間かかっていたが、GPUでは約12時間にまで効率化された。
This improvement not only saves time but also expedites the development cycle, enabling faster iterations and model improvements.
この改良は、時間を節約するだけでなく、開発サイクルを迅速化し、より迅速なiterationとモデルの改善を可能にしました。
(めちゃいいじゃん...!:thinking_face:)

### Advanced ML capabilities 高度なML機能

Central to the migration’s success is the use of the SageMaker feature set, encompassing hyperparameter tuning and model explainability.
移行の成功の中心は、ハイパーパラメータのチューニングとモデルの説明可能性を包含するSageMaker機能セットの使用です。
Furthermore, the migration allowed for seamless experiment tracking using Amazon SageMaker Experiments, enabling more insightful and productive experimentation.
さらに、この移行により、**Amazon SageMaker Experimentsを使用したシームレスな実験trackingが可能になり**、より洞察に富んだ生産的な実験が可能になりました。

Most importantly, the new ML experimentation environment supported the successful development of a new model that is now in production.
最も重要なことは、新しいML実験環境が、現在生産中の新モデルの開発を成功に導いたことである。
This model is deep learning rather than tree-based and has introduced noticeable improvements in online model performance.
このモデルはツリーベースではなくディープラーニングであり、オンラインモデルのパフォーマンスに顕著な改善をもたらした。

<!-- ここまで読んだ! -->

## Conclusion 結論

This post provided an overview of the AWS Professional Services and Booking.com collaboration that resulted in the implementation of a scalable ML framework and successfully reduced the time-to-market of ML models of their Ranking team.
この投稿では、スケーラブルなMLフレームワークを実装し、**ランキングチームのMLモデルの市場投入までの時間を短縮することに成功した**、AWSプロフェッショナルサービスとBooking.comの協力の概要を提供しました。

The Ranking team at Booking.com learned that migrating to the cloud and SageMaker has proved beneficial, and that adapting machine learning operations (MLOps) practices allows their ML engineers and scientists to focus on their craft and increase development velocity.
Booking.comのRankingチームは、**クラウドとSageMakerへの移行が有益であることを学び**、機械学習オペレーション（MLOps）の実践を適応することで、MLエンジニアと科学者が自分たちの技術に集中し、開発速度を向上させることができるということです。
The team is sharing the learnings and work done with the entire ML community at Booking.com, through talks and dedicated sessions with ML practitioners where they share the code and capabilities.
チームは、トークやML実務者との専用セッションを通じて、**Booking.comのMLコミュニティ全体と学んだことや行ったことを共有し**、コードと機能(capability=能力?)を共有しています。
We hope this post can serve as another way to share the knowledge.
この投稿が、知識を共有するもうひとつの方法として役立つことを願っている。

AWS Professional Services is ready to help your team develop scalable and production-ready ML in AWS.
AWSプロフェッショナルサービスは、お客様のチームがAWSでスケーラブルかつプロダクションレディなMLを開発するお手伝いをいたします。
For more information, see AWS Professional Services or reach out through your account manager to get in touch.
詳細については、AWSプロフェッショナルサービスを参照するか、アカウントマネージャーを通じてお問い合わせください。

<!-- ここまで読んだ! -->
