## refs: refs：

https://neptune.ai/blog/building-ml-systems-with-feature-store
https://neptune.ai/blog/building-ml-systems-with-feature-store

# How to Build Machine Learning Systems With a Feature Store フィーチャーストアを使った機械学習システムの構築方法

Training and evaluating models is just the first step toward machine-learning success.
モデルの訓練と評価は、機械学習の成功への第一歩に過ぎない。
To generate value from your model, it should make many predictions, and these predictions should improve a product or lead to better decisions.
モデルから価値を生み出すためには、モデルは多くの予測を行う必要があり、これらの予測は製品を改善したり、より良い意思決定につながったりするはずだ。
For this, we have to build an entire machine-learning system around our models that manages their lifecycle, feeds properly prepared data into them, and sends their output to downstream systems.
そのためには、モデルのライフサイクルを管理し、適切に準備されたデータをモデルに送り込み、その出力を下流のシステムに送る、機械学習システム全体を構築しなければならない。

This can seem daunting.
これは大変なことに思えるかもしれない。
Luckily, we have tried and trusted tools and architectural patterns that provide a blueprint for reliable ML systems.
幸運なことに、我々には信頼できるMLシステムの青写真を提供する、試行錯誤されたツールやアーキテクチャ・パターンがある。
In this article, I’ll introduce you to a unified architecture for ML systems built around the idea of FTI pipelines and a feature store as the central component.
この記事では、FTIパイプラインとフィーチャーストアを中心に構築されたMLシステムの統一アーキテクチャを紹介する。
We’ll see how this architecture applies to different classes of ML systems, discuss MLOps and testing aspects, and look at some example implementations.
このアーキテクチャがMLシステムの様々なクラスにどのように適用されるかを見て、MLOpsとテストの側面について議論し、いくつかの実装例を見ていく。

## Understanding machine learning pipelines 機械学習パイプラインを理解する

Machine learning (ML) pipelines are a key component of ML systems.
機械学習（ML）パイプラインは、MLシステムの重要な構成要素である。
But what is an ML pipeline? Ask four ML engineers, and you will likely get four different answers.
しかし、MLパイプラインとは何だろうか？4人のMLエンジニアに聞けば、4つの異なる答えが返ってくるだろう。
Some will say that an ML pipeline trains models, another says it makes predictions, and another says it does both in a single run.
ある人はMLパイプラインがモデルを訓練すると言い、別の人は予測をすると言い、また別の人は1回の実行で両方を行うと言う。
None of them are wrong, but you can already tell that just saying “ML pipeline” can easily lead to miscommunication.
どれも間違いではないが、「MLパイプライン」と言うだけで、誤解を招きやすいことはすでにお分かりだろう。
We’ll have to be more precise.
もっと正確でなければならない。

An ML system needs to transform the data into features, train models, and make predictions.
MLシステムは、データを特徴量に変換し、モデルを訓練し、予測を行う必要がある。
Each of these tasks can be performed by a pipeline: A program that runs on some schedule with well-defined inputs and outputs.
これらの各タスクは、パイプラインによって実行することができる： 入力と出力が明確に定義されたスケジュールで実行されるプログラム。

In this article, we define a machine learning system as consisting of three ML pipelines:
本稿では、機械学習システムを3つのMLパイプラインから構成されると定義する：

A feature pipeline that transforms its input data into features/labels as output,
入力データを出力として特徴/ラベルに変換する特徴パイプライン、

a training pipeline that transforms its input features/labels into trained models as output,
入力された特徴/ラベルを出力として学習済みモデルに変換する学習パイプライン、

and an inference pipeline that uses these trained models to transform its input features into predictions as output.
そして、これらの学習済みモデルを使用して、入力特徴を出力として予測に変換する推論パイプライン。

Collectively, these three ML pipelines are known as the FTI pipelines: feature, training, and inference.
これら3つのMLパイプラインを総称してFTIパイプラインと呼ぶ： feature、training、inferenceです。

## Machine learning systems with feature stores 特徴ストアによる機械学習システム

Machine learning (ML) systems manage the data transformations, model training, and predictions made on ML models.
機械学習（ML）システムは、データの変換、モデルのトレーニング、MLモデルによる予測を管理する。
They transform data into features, train ML models using features and labels, and use trained models to make predictions.
データを特徴量に変換し、特徴量とラベルを使ってMLモデルを学習し、学習したモデルを使って予測を行う。

As you’re building an ML system, you’ll find that matching the outputs of your feature pipeline with the inputs of the training and inference pipelines becomes a challenge.
MLシステムを構築していると、特徴パイプラインの出力と学習パイプラインや推論パイプラインの入力を一致させることが課題になることに気づくだろう。
Keeping track of how exactly the incoming data (the feature pipeline’s input) has to be transformed and ensuring that each model receives the features precisely how it saw them during training is one of the hardest parts of architecting ML systems.
入力データ（特徴パイプラインの入力）がどのように変換されなければならないかを正確に把握し、各モデルがトレーニング中に見た通りの特徴を正確に受け取れるようにすることは、MLシステムをアーキテクトする上で最も難しい部分の1つである。

This is where feature stores come in.
そこでフィーチャーストアの出番となる。
A feature store is a data platform that supports the creation and use of feature data throughout the lifecycle of an ML model, from creating features that can be reused across many models to model training to model inference (making predictions).
フィーチャーストアは、多くのモデルで再利用できるフィーチャーの作成から、モデルのトレーニング、モデルの推論（予測）まで、MLモデルのライフサイクル全体を通してフィーチャーデータの作成と利用をサポートするデータプラットフォームである。

A feature store typically comprises a feature repository, a feature serving layer, and a metadata store.
特徴ストアは通常、特徴リポジトリ、特徴サービングレイヤー、メタデータストアから構成される。
The feature repository is essentially a database storing pre-computed and versioned features.
機能リポジトリは基本的に、事前に計算され、バージョン管理された機能を保存するデータベースである。
The serving layer facilitates real-time access to these features during model training and inference.
サービングレイヤーは、モデルのトレーニングや推論中に、これらの特徴にリアルタイムでアクセスすることを容易にする。
It can also transform incoming data on the fly.
また、入力されたデータをその場で変換することもできる。
The metadata store manages the metadata associated with each feature, such as its origin and transformations.
メタデータストアは、各フィーチャに関連するメタデータ（オリジンや変換など）を管理する。
Together, these components form a specialized infrastructure to streamline feature data management in ML workflows.
これらのコンポーネントを組み合わせることで、MLワークフローにおける特徴データ管理を合理化するための専用インフラストラクチャが形成される。

Many ML systems benefit from having the feature store as their data platform, including:
多くのMLシステムは、フィーチャーストアをデータ・プラットフォームとすることで恩恵を受ける：

Interactive ML systems receive a user request and respond with a prediction.
対話型MLシステムは、ユーザーのリクエストを受け、予測で応答する。
An interactive ML system either downloads a model and calls it directly or calls a model hosted in a model-serving infrastructure.
対話型MLシステムは、モデルをダウンロードして直接呼び出すか、モデル提供インフラにホストされているモデルを呼び出す。
The inputs to the model – the features – can be computed on-demand from request parameters or be precomputed and read at runtime.
モデルへの入力（特徴量）は、リクエストパラメータからオンデマンドで計算することもできるし、あらかじめ計算しておいて実行時に読み込むこともできる。
Both scenarios are supported by feature stores.
どちらのシナリオもフィーチャーストアがサポートしている。

Batch ML systems run on a schedule or are triggered when a new batch of data arrives.
バッチMLシステムは、スケジュールに従って実行されるか、新しいバッチデータが到着したときにトリガーされる。
They download a model from a model registry, compute predictions, and store the results to be later consumed by AI-enabled applications.
モデルレジストリからモデルをダウンロードし、予測を計算し、結果を保存して、後でAI対応アプリケーションで利用できるようにする。
Batch ML systems can retrieve a new batch of inference data from a feature store as a batch of precomputed features created by the feature pipelines.
バッチMLシステムは、特徴パイプラインによって事前に計算された特徴のバッチとして、特徴ストアから新しい推論データのバッチを取り出すことができる。

Stream-processing ML systems typically use a model downloaded from a model registry to make predictions on streaming data.
ストリーム処理MLシステムは通常、ストリーミング・データに対して予測を行うために、モデル・レジストリからダウンロードしたモデルを使用する。
Features are typically computed on-demand but may also be enriched with precomputed features retrieved from a feature store.
特徴量は通常オンデマンドで計算されるが、特徴量ストアから取得した事前計算された特徴量でエンリッチされることもある。
(It is also possible for stream-processing systems to use an externally hosted model, although less common due to the higher latency it introduces).
(ストリーム処理システムが外部ホストモデルを使用することも可能だが、レイテンシーが高くなるため、あまり一般的ではない）。

There are ML systems, such as embedded systems in self-driving cars, that do not use feature stores as they require real-time safety-critical decisions and cannot wait for a response from an external database.
自動運転車の組み込みシステムのように、リアルタイムで安全上重要な判断を必要とし、外部データベースからの応答を待つことができないため、フィーチャストアを使用しないMLシステムがある。

## A unified architecture for ML systems MLシステムの統一アーキテクチャ

One of the challenges in building machine-learning systems is architecting the system.
機械学習システムの構築における課題のひとつは、システムのアーキテクチャーである。
As you’ll likely have experienced yourself, there is no one right way that fits every situation.
あなた自身も経験したことがあるだろうが、どんな状況にも合う正しい方法というものはない。
But there are some common patterns and best practices, which we’ll explore in this section.
しかし、共通のパターンやベストプラクティスがいくつかあるので、このセクションで紹介する。

Figure 1.
図1.
Overview of the high-level architecture of an ML system centered around a feature store.
特徴ストアを中心としたMLシステムの高レベルアーキテクチャの概要。
The feature pipeline retrieves data from outside sources, transforms them, and loads them into the feature store.
フィーチャー・パイプラインは、外部ソースからデータを取得し、変換し、フィーチャー・ストアにロードする。
The training pipeline fetches data from the feature store for model training, sends training metadata to an experiment tracker for later analysis, and places the resulting model in the model registry.
トレーニングパイプラインは、モデルトレーニングのためにフィーチャーストアからデータをフェッチし、後の分析のためにトレーニングメタデータを実験トラッカーに送信し、結果として得られたモデルをモデルレジストリに配置する。
The inference pipeline loads a model from the model registry.
推論パイプラインはモデルレジストリからモデルをロードします。
It uses the feature store to retrieve properly transformed features, which it feeds to the model to make predictions that it exposes to downstream applications.
特徴ストアを使用して適切に変換された特徴を取得し、それをモデルに与えて予測を行い、下流のアプリケーションに公開する。
In most ML systems, the feature and inference pipeline are always active, while the training pipeline is only invoked occasionally.
ほとんどのMLシステムでは、特徴量パイプラインと推論パイプラインは常にアクティブで、トレーニングパイプラインはたまにしか起動されない。

The feature pipeline ingests data.
フィーチャー・パイプラインはデータを取り込む。
In the most straightforward case, you’ll load complete datasets at once, reading them from CSV or Parquet files.
最も簡単なケースでは、CSVファイルやParquetファイルからデータセット全体を一度に読み込む。
But often, you’ll want to load data incrementally, adding new samples to datasets that already exist in the system.
しかし、データを少しずつロードし、すでにシステムに存在するデータセットに新しいサンプルを追加したい場合も多い。
When you have to comply with GDPR or similar regulations, you’ll also need the ability to delete samples.
GDPRや同様の規制に準拠しなければならない場合、サンプルを削除する機能も必要になります。

The feature store is the stateful layer to manage your features (and training labels) for your ML system.
特徴ストアは、MLシステムの特徴（とトレーニング・ラベル）を管理するステートフルなレイヤーである。
It stores the features created in feature pipelines and provides APIs to retrieve them.
フィーチャー・パイプラインで作成されたフィーチャーを保存し、それらを取得するためのAPIを提供する。

For model training, it’s paramount that the training pipeline can easily load snapshots of training data from tables of features (feature groups).
モデルのトレーニングでは、トレーニング・パイプラインが、特徴のテーブル（特徴グループ）からトレーニング・データのスナップショットを簡単にロードできることが最も重要である。
In particular, a feature store should provide point-in-time consistent snapshots of feature data so that your models do not suffer from future data leakage.
特に、フィーチャーストアは、フィーチャーデータのポイント・イン・タイムの一貫したスナップショットを提供する必要があります。

For batch and interactive ML systems where features are pre-computed, the feature store provides batch and point APIs enabling the inference pipeline to retrieve a batch of precomputed features in a DataFrame or a row of precomputed features in a feature vector.
特徴量が事前に計算されるバッチ型および対話型MLシステムのために、特徴量ストアは、推論パイプラインがDataFrame内の事前計算された特徴量のバッチまたは特徴ベクトル内の事前計算された特徴量の行を取得することを可能にするバッチおよびポイントAPIを提供します。

In real-time ML systems, some features may be based on information that only becomes available right when a prediction is requested.
リアルタイムMLシステムでは、いくつかの特徴は、予測が要求されたときに初めて利用可能になる情報に基づいているかもしれない。
These features are computed on-demand using feature functions.
これらの特徴は、特徴関数を使ってオンデマンドで計算される。
A feature store helps ensure that the features calculated online match those used in the training pipeline.
特徴ストアは、オンラインで計算された特徴がトレーニングパイプラインで使用された特徴と一致することを保証するのに役立ちます。

The model registry connects your training and inference pipeline.
モデルレジストリは、学習パイプラインと推論パイプラインを接続します。
It stores the trained models created by training pipelines and provides an API for inference pipelines to download the trained models.
学習パイプラインによって作成された学習済みモデルを保存し、推論パイプラインが学習済みモデルをダウンロードするためのAPIを提供する。

This high-level design around a feature store and a model registry as central components provides a unified architecture for batch, interactive, and streaming ML systems.
フィーチャーストアとモデルレジストリを中心としたこのハイレベルな設計は、バッチ、インタラクティブ、ストリーミングのMLシステムに統一されたアーキテクチャを提供する。
It also enables developers to concentrate on building the ML pipelines rather than the ML infrastructure.
また、開発者はMLインフラよりもMLパイプラインの構築に集中することができる。

The following table shows the different technologies that can be used to build the FTI pipelines, depending on the type of machine-learning system you want to develop:
次の表は、開発したい機械学習システムのタイプに応じて、FTIパイプラインの構築に使用できるさまざまなテクノロジーを示している：

Table 1.
表1.
Reference table for which technologies to use for your FTI pipelines for each ML system.
MLシステムごとに、FTIパイプラインにどのテクノロジーを使用するかの参考表。

## MLOps and FTI pipelines testing MLOps と FTI パイプラインのテスト

Once you have built an ML system, you have to operate, maintain, and update it.
いったんMLシステムを構築したら、それを運用し、維持し、更新しなければならない。
Typically, these activities are collectively called “MLOps.”
通常、これらの活動は "MLOps "と総称される。

One of the core principles of MLOps is automation.
MLOpsの基本原則のひとつは自動化である。
Many ML engineers dream of having a big green button and a big red button.
多くのMLエンジニアは、大きな緑のボタンと大きな赤いボタンを持つことを夢見ている。
Press the green button to upgrade and the red button to roll back an upgrade.
アップグレードするには緑のボタンを、アップグレードをロールバックするには赤いボタンを押します。
Achieving this dream requires versioning of artifacts – model versions are connected to specific feature versions – and comprehensive testing to increase the user’s confidence that the new model will work well.
この夢を達成するためには、成果物のバージョン管理（モデルのバージョンは特定の機能のバージョンに関連づけられる）と、新しいモデルがうまく機能するというユーザーの確信を高めるための包括的なテストが必要である。

Figure 2.
図2.
Testing machine learning systems is a hierarchical process spanning data, features, models, and ML-enabled applications.
機械学習システムのテストは、データ、特徴、モデル、ML対応アプリケーションにまたがる階層的プロセスである。
The testing pyramid shows that a reliable ML app requires reliable models, which in turn require reliable features derived from the raw data.
テスト・ピラミッドは、信頼できるMLアプリには信頼できるモデルが必要であり、そのモデルには生データから得られる信頼できる特徴が必要であることを示している。

Aside from testing a pipeline’s implementation prior to its deployment, testing has to happen while operating the ML system:
配備前のパイプラインの実装テストとは別に、MLシステムの運用中にもテストが必要だ：

In feature pipelines, we validate the incoming data and the data written to the feature store.
フィーチャー・パイプラインでは、入力されたデータとフィーチャー・ストアに書き込まれたデータを検証する。

In training pipelines, we validate the model performance and validate that the model is free from bias and other undesirable behavior.
トレーニングパイプラインでは、モデルの性能を検証し、モデルにバイアスやその他の望ましくない挙動がないことを検証する。

In inference pipelines, we can use A/B testing to validate the models.
推論パイプラインでは、A/Bテストを使ってモデルを検証することができる。
Instead of deploying a new model directly, we can deploy it in “shadow mode,” evaluating its performance compared to the old model.
新モデルを直接配備する代わりに、「シャドーモード」で配備し、旧モデルと比較してそのパフォーマンスを評価することができる。
When we’re happy enough with the new version, we can replace the previous version with the new version.
新しいバージョンに十分満足したら、前のバージョンを新しいバージョンに置き換えることができる。

Versioning of features and models enables the online upgrade of ML systems.
機能とモデルのバージョン管理は、MLシステムのオンラインアップグレードを可能にする。
A specific model version is linked to a particular feature version.
特定のモデル・バージョンは、特定の機能バージョンとリンクしている。
Thus, during operation, the inference pipeline can retrieve precisely the kind of features it was trained on.
このように、推論パイプラインは、動作中に、それが訓練された特徴の種類を正確に取り出すことができる。

When the model is upgraded to a new version, the inference pipeline will simultaneously start requesting the associated new feature versions.
モデルが新しいバージョンにアップグレードされると、推論パイプラインは同時に関連する新しい機能バージョンの要求を開始する。
If there is a problem after upgrading, you can immediately go back to using the previous model and feature versions.
アップグレード後に問題が発生しても、すぐに以前のモデルや機能のバージョンに戻すことができます。
(This is the “big red button” I mentioned above).
(これが先ほどの "大きな赤いボタン "だ）。

Figure 3 shows an example of how all of this comes together.
図3は、これらすべてがどのように組み合わされているかを示す一例である。

Figure 3.
図3.
Example of an ML system that uses model and feature versioning to facilitate seamless and reliable upgrades.
シームレスで信頼性の高いアップグレードを促進するために、モデルと機能のバージョニングを使用するMLシステムの例。
An air quality model has been upgraded from version 1 to version 2.
大気質モデルがバージョン1からバージョン2にアップグレードされた。
The airquality model uses weather and airquality features from the feature store.
大気質モデルは、フィーチャーストアの天気と大気質のフィーチャーを使用する。
As part of the upgrade from version 1 to version 2, we needed a new version of the air quality features (air_quality_v2).
バージョン1からバージョン2へのアップグレードの一環として、大気品質機能の新しいバージョン（air_quality_v2）が必要になった。
Upgrading a model involves synchronizing the upgrade of both the model and the features.
モデルのアップグレードには、モデルと機能の両方のアップグレードの同期が含まれます。

## Examples of ML systems with feature stores and FTI pipelines 特徴ストアとFTIパイプラインを持つMLシステムの例

To truly understand an abstract concept, I always find it best to look at some concrete examples.
抽象的な概念を本当に理解するためには、私はいつも具体的な例を見るのが一番だと思う。

In Table 1 below, I’ve compiled a list of different ML systems that follow the unified architecture.
以下の表1は、統一されたアーキテクチャに従ったさまざまなMLシステムのリストである。
Most of them were built by people who took my free online serverless machine learning course or my Scalable Machine Learning and Deep Learning course at KTH Royal Institute of Technology in Stockholm.
そのほとんどは、私の無料オンラインサーバーレス機械学習コースや、ストックホルムにあるKTH王立工科大学のスケーラブル機械学習とディープラーニングコースを受講した人たちによって作られたものだ。

The ML systems mostly follow the same structure.
MLシステムのほとんどは、同じ構造に従っている。
They have a non-static data source (new data will arrive at some cadence), train an ML model to solve a prediction problem, and have a user interface that allows users to consume the predictions.
非定常的なデータソース（新しいデータはある程度の周期で到着する）を持ち、予測問題を解決するためにMLモデルを訓練し、ユーザーが予測を利用できるユーザーインターフェースを持つ。
Some ML systems use deep learning, while others utilize more classical models like decision trees or XGBoost.
MLシステムにはディープラーニングを使うものもあれば、決定木やXGBoostのような古典的なモデルを使うものもある。

They are all serverless systems, i.e., they don’t require any computational resources when no pipeline is actively running.
これらはすべてサーバーレスシステムである。つまり、パイプラインがアクティブに実行されていないときは、計算リソースを必要としない。
All of them are written in Python.
これらはすべてPythonで書かれている。
The systems run their pipelines on GitHub Actions or with Cloud Composer, the managed Apache Airflow offering on the Google Cloud Platform.
これらのシステムは、GitHub Actions、またはGoogle Cloud Platform上でマネージドApache Airflowを提供するCloud Composerでパイプラインを実行する。
They store their feature data in Hopsworks’ free serverless platform, app.hopsworks.ai.
彼らは機能データをホップワークスの無料サーバーレスプラットフォーム、app.hopsworks.aiに保存している。

## How to get started with FTI pipelines and feature stores FTIパイプラインとフィーチャーストアの始め方

To learn more about designing ML systems using FTI pipelines and feature stores, check out my free open-source course at serverless-ml.org.
FTIパイプラインとフィーチャーストアを使ったMLシステムの設計についてもっと学びたい方は、serverless-ml.orgにある私の無料のオープンソースコースをチェックしてほしい。
It covers the principles and practices of creating an ML system (both batch and interactive) in Python using free serverless services.
Pythonで無料のサーバーレスサービスを使ってMLシステム（バッチとインタラクティブの両方）を作成する原則と実践をカバーしています。
Python is the only prerequisite for the course, and your first ML system will consist of just three different Python scripts.
Pythonはこのコースの唯一の前提条件であり、あなたの最初のMLシステムはたった3種類のPythonスクリプトで構成されます。
We also have a discord channel dedicated to serverless machine learning with over 2,500 members where you can ask questions and discuss what you learned with fellow participants.
また、2,500人以上のメンバーが参加するサーバーレス機械学習専用のdiscordチャンネルでは、参加者同士で質問したり、学んだことを話し合ったりすることができます。

The course uses Hopsworks as the serverless feature store, GitHub Actions to schedule batch Python programs, and HuggingFace Spaces to host a UI for your machine-learning systems.
このコースでは、サーバーレス機能ストアとしてHopsworks、バッチPythonプログラムをスケジュールするGitHub Actions、機械学習システムのUIをホストするHuggingFace Spacesを使用します。
You can use Neptune as your experiment tracking system and model registry for the course, just like in the NBA Score Predictions example I shared above.
上で紹介したNBAのスコア予測の例のように、Neptuneを実験追跡システムやコースのモデル登録として使うことができる。

I’m also working on a book about building machine-learning systems with a feature store.
また、フィーチャーストアを使った機械学習システムの構築に関する本も執筆中だ。
It will be published by O’Reilly in the summer of 2025.
2025年夏にオライリー社から出版される予定だ。
You can already read the first few chapters on our website.
最初の数章はすでにウェブサイトで読むことができる。

If you make the leap from training models, to building ML systems, please do share what you’ve built on the discord channel with all the other builders – when we learn together, we learn faster and better.
もしあなたがモデルのトレーニングからMLシステムの構築へと飛躍したなら、あなたが構築したものを他の構築者たちとディスコードチャンネルで共有してください。