## CHAPTER 13: Testing AI Systems 第13章：AIシステムのテスト
MLOps is a set of best practices for the automated testing, versioning, and monitoring of the ML pipelines and ML assets that power our AI systems. 
MLOpsは、私たちのAIシステムを支えるMLパイプラインとML資産の自動テスト、バージョン管理、および監視のためのベストプラクティスのセットです。 
We introduced MLOps in Chapter 1, data validation tests in Chapter 6, and unit testing for transformation functions in Chapter 7. 
第1章でMLOpsを紹介し、第6章でデータ検証テスト、第7章で変換関数の単体テストを紹介しました。 
But there is still much more ground to cover. 
しかし、まだ多くの課題があります。 
If you are to build a reliable, governed, maintainable AI system, you need integration tests for each of your ML pipelines, run both during development and before deployment. 
信頼性が高く、管理され、保守可能なAIシステムを構築するには、各MLパイプラインの統合テストが必要であり、開発中およびデプロイ前に実行する必要があります。 

We will look at how to write feature pipeline tests and model validation tests and how to test model deployments. 
機能パイプラインテストとモデル検証テストの書き方、モデルデプロイメントのテスト方法を見ていきます。 
We will look at how to reliably package our ML pipelines with automatic containerization in development, staging, and production environments. 
開発、ステージング、および本番環境で自動コンテナ化を使用してMLパイプラインを信頼性高くパッケージ化する方法を見ていきます。 
We will also present offline testing of agents and LLM workflows with evals. 
また、エージェントとLLMワークフローのオフラインテストをevalsを使用して紹介します。 

Testing is key to building a high-quality AI system. 
テストは高品質なAIシステムを構築するための鍵です。 
Your testing should be at a level where you are so confident in your tests that you will deploy to production on a Friday. 
テストに自信を持てるレベルで、金曜日に本番環境にデプロイできるようにするべきです。 
And even if an upgrade fails, you will be easily able to roll back your changes. 
アップグレードが失敗しても、変更を簡単に元に戻すことができるでしょう。 
In the next chapter we will focus on operational concerns of MLOps, but in this chapter, we will look at tests run during development and how to automate offline testing for AI systems. 
次の章ではMLOpsの運用上の懸念に焦点を当てますが、この章では開発中に実行されるテストとAIシステムのオフラインテストを自動化する方法を見ていきます。 

###### Offline Testing オフラインテスト
The starting point for building reliable AI systems is testing. 
信頼性の高いAIシステムを構築するための出発点はテストです。 
AI systems require more levels of testing than traditional software systems. 
AIシステムは、従来のソフトウェアシステムよりも多くのテストレベルを必要とします。 
Small bugs in data or code can easily cause an ML model to silently make incorrect predictions. 
データやコードの小さなバグは、MLモデルが静かに不正確な予測を行う原因となることがあります。 
AI systems require significant engineering effort to test and validate to make sure they produce high-quality predictions that are free from bias. 
AIシステムは、バイアスのない高品質な予測を生成することを確認するために、テストと検証にかなりのエンジニアリング努力を必要とします。 
When AI systems are deployed, they also need to be monitored for bad data, drift, and violation of SLOs or degradation of KPIs. 
AIシステムが展開されると、悪いデータ、ドリフト、SLOの違反、またはKPIの劣化を監視する必要があります。 
The testing pyramids in Figure 13-1 show that both offline tests and online (operational) checks are needed throughout the AI system lifecycle.
図13-1のテストピラミッドは、AIシステムライフサイクル全体でオフラインテストとオンライン（運用）チェックの両方が必要であることを示しています。

-----
_Figure 13-1. The offline and online testing pyramids for AI systems are higher than for traditional software systems, as both code and data need to be tested, not just code._
図13-1. AIシステムのオフラインおよびオンラインテストピラミッドは、従来のソフトウェアシステムよりも高く、コードだけでなくデータもテストする必要があります。 
They are testing pyramids because most of the tests are at the bottom (unit tests for feature functions and data validation tests for feature groups) and there are fewer tests at the top layers (blue/green model deployment tests and SLOs and KPIs for model deployments). 
テストピラミッドは、ほとんどのテストが下部（機能関数の単体テストと機能グループのデータ検証テスト）にあり、上部層（青/緑モデルデプロイメントテストおよびモデルデプロイメントのSLOとKPI）にはテストが少ないため、テストピラミッドと呼ばれています。 
We already covered the bottom layers of both pyramids in Chapters 6 and 7, and in this chapter, we will cover the rest of the offline tests pyramid. 
第6章と第7章で両方のピラミッドの下層をすでにカバーしており、この章ではオフラインテストピラミッドの残りをカバーします。 

These testing pyramids can be intimidating, particularly if you do not have a software engineering background. 
これらのテストピラミッドは、特にソフトウェアエンジニアリングのバックグラウンドがない場合、威圧的に感じることがあります。 
An important point is that support for automated testing with CI/CD is not a prerequisite for starting to build AI systems. 
重要な点は、CI/CDによる自動テストのサポートは、AIシステムの構築を開始するための前提条件ではないということです。 
Support for automated testing can come after you have built your first MVPS to validate that what you built is worth maintaining. 
自動テストのサポートは、構築したものが維持する価値があることを検証するために最初のMVPSを構築した後に来ることがあります。 
It is OK to incrementally add testing to the AI systems you build. 
構築するAIシステムにテストを段階的に追加することは問題ありません。 
You can start with unit tests for feature functions and transformations, then add integration tests for both feature pipelines and training pipelines (including model performance and model bias tests). 
機能関数と変換の単体テストから始め、次に機能パイプラインとトレーニングパイプラインの統合テスト（モデルのパフォーマンスとモデルのバイアステストを含む）を追加できます。 
You can then look at automating your tests by adding CI support to run your tests whenever you push code to your source code repository. 
その後、ソースコードリポジトリにコードをプッシュするたびにテストを実行するCIサポートを追加して、テストの自動化を検討できます。 

-----
###### From Dev to Prod 開発から本番へ
The code for your ML pipelines should go on a journey from development (your laptop) to staging (central automated tests) to production (deployment). 
MLパイプラインのコードは、開発（あなたのラップトップ）からステージング（中央自動テスト）を経て本番（デプロイメント）へと移動する必要があります。 
For this, you need infrastructure support and different environments for development, staging, and production. 
これには、開発、ステージング、および本番用のインフラストラクチャサポートと異なる環境が必要です。 
The infrastructure services needed for developing and testing ML pipelines are:
MLパイプラインの開発とテストに必要なインフラストラクチャサービスは次のとおりです：
- Version control (a source code repository) for the source code for your ML pipelines
- MLパイプラインのソースコード用のバージョン管理（ソースコードリポジトリ）
- A CI/CD service that can check out code from version control, run tests, and deploy artifacts
- バージョン管理からコードをチェックアウトし、テストを実行し、アーティファクトをデプロイできるCI/CDサービス
- An artifact repository, such as a PyPI server for Python or a Maven repository for Java, to store and serve libraries used to build containers
- コンテナを構築するために使用されるライブラリを保存および提供するためのPyPIサーバー（Python用）やMavenリポジトリ（Java用）などのアーティファクトリポジトリ
- A container registry to store the containers for your ML pipelines
- MLパイプラインのコンテナを保存するためのコンテナレジストリ
- A feature store and model registry to act as sources and sinks for pipeline integration tests
- パイプライン統合テストのソースとシンクとして機能するフィーチャーストアとモデルレジストリ
- Model-serving infrastructure to run model deployment tests
- モデルデプロイメントテストを実行するためのモデル提供インフラストラクチャ
- Agent deployment infrastructure to run evals against agent deployments
- エージェントデプロイメントに対してevalsを実行するためのエージェントデプロイメントインフラストラクチャ

Hopsworks provides the last four of these infrastructure services, but you need to provide your own source code repository, CI/CD service, and artifact repository. 
Hopsworksはこれらのインフラストラクチャサービスの最後の4つを提供しますが、独自のソースコードリポジトリ、CI/CDサービス、およびアーティファクトリポジトリを提供する必要があります。 
For our example AI systems, we used the free and public versions of GitHub, GitHub Actions, and PyPI services. 
私たちの例のAIシステムでは、GitHub、GitHub Actions、およびPyPIサービスの無料および公開バージョンを使用しました。 
Some other widely used platforms are Jenkins, GitLab, Azure DevOps, JFrog, and Sonatype Nexus. 
他にも広く使用されているプラットフォームには、Jenkins、GitLab、Azure DevOps、JFrog、Sonatype Nexusがあります。 
You can also replace Hopsworks’ infrastructural services if needed. 
必要に応じてHopsworksのインフラストラクチャサービスを置き換えることもできます。 
For example, you may want to use an existing centralized container registry, such as AWS Elastic Container Registry, for your enterprise. 
たとえば、企業向けにAWS Elastic Container Registryなどの既存の中央集権的なコンテナレジストリを使用したい場合があります。 

In Figure 13-2, you can see a CI/CD architecture for Hopsworks, where source code moves from development to staging to production using branches in version control.
図13-2では、ソースコードがバージョン管理のブランチを使用して開発からステージング、そして本番に移動するHopsworksのCI/CDアーキテクチャを見ることができます。

-----
_Figure 13-2. CI/CD architecture and services for moving source code from development to staging and production with Hopsworks._
図13-2. Hopsworksを使用してソースコードを開発からステージングおよび本番に移動するためのCI/CDアーキテクチャとサービス。 
In Hopsworks, each environment has its own project, with production often using a separate Hopsworks cluster from the one used by development/staging. 
Hopsworksでは、各環境には独自のプロジェクトがあり、本番環境は開発/ステージングで使用されるものとは異なるHopsworksクラスターを使用することがよくあります。 
Projects have their own feature store, model registry, and model serving so that you can build and test artifacts locally within a project. 
プロジェクトには独自のフィーチャーストア、モデルレジストリ、およびモデル提供があり、プロジェクト内でアーティファクトをローカルに構築およびテストできます。 

By default, the artifacts do not migrate from one environment to another. 
デフォルトでは、アーティファクトはある環境から別の環境に移行しません。 
Often, features and models are created with nonproduction data in development/staging environments, in which case migrating features/models makes no sense. 
多くの場合、機能とモデルは開発/ステージング環境で非本番データを使用して作成されるため、機能/モデルを移行することは意味がありません。 
Instead, the ML pipeline code migrates from development to staging via a pull request (PR). 
代わりに、MLパイプラインのコードはプルリクエスト（PR）を介して開発からステージングに移行します。 
The PR triggers the execution of all automated tests by the CI/CD service. 
PRはCI/CDサービスによってすべての自動テストの実行をトリガーします。 
Tests and test-launching code are often parameterized by an environment variable indicating whether they are run in a development, staging, or production environment. 
テストとテスト起動コードは、開発、ステージング、または本番環境で実行されるかどうかを示す環境変数によってパラメータ化されることがよくあります。 
This helps ensure your testing code is DRY and able to run in development, staging, and production. 
これにより、テストコードがDRY（Don't Repeat Yourself）であり、開発、ステージング、および本番で実行できることが保証されます。 
If all tests pass in staging, the code can be flagged as ready for deployment to production. 
すべてのテストがステージングで合格した場合、コードは本番環境へのデプロイメントの準備が整ったとマークされます。 
A human reviewer often signs off on deploying an ML artifact to production. 
人間のレビュアーがMLアーティファクトを本番環境にデプロイすることを承認することがよくあります。 

The Hopsworks approach is both open source and open-platform friendly, as you can run the ML pipelines and tests either inside Hopsworks as jobs or outside Hopsworks in any container runtime. 
Hopsworksのアプローチはオープンソースであり、オープンプラットフォームにも優しいもので、MLパイプラインとテストをHopsworks内でジョブとして実行することも、Hopsworksの外部の任意のコンテナランタイムで実行することもできます。 
This makes it easier to integrate your ML pipelines with your existing testing infrastructure or choose the best-in-class testing infrastructure.
これにより、既存のテストインフラストラクチャとMLパイプラインを統合したり、最高のテストインフラストラクチャを選択したりすることが容易になります。



_Pre-commit hooks are commands that run automatically right_ before a commit is made to version control. 
プレコミットフックは、バージョン管理にコミットされる直前に自動的に実行されるコマンドです。

They can help keep code quality standards high by ensuring the new code follows code formatting rules (using `black); identifying syntax errors, unused` imports, and style issues with a linter (using flake8); and detecting security vulnerabilities (using `bandit). 
これにより、新しいコードがコードフォーマットルール（`black`を使用）に従っていることを確認し、構文エラー、未使用のインポート、リンター（flake8を使用）によるスタイルの問題を特定し、セキュリティの脆弱性（`bandit`を使用）を検出することで、コード品質基準を高く保つのに役立ちます。

They can even help when` committing changes in Jupyter Notebooks (nbstripout) by remov‐ ing unnecessary outputs or metadata from cells, making reviewing the differences between two notebook versions easier. 
Jupyterノートブック（nbstripout）での変更をコミットする際に、セルから不要な出力やメタデータを削除することで、2つのノートブックバージョン間の違いをレビューしやすくすることもできます。

To run our ML pipeline programs, we will look at how to containerize them and package them in jobs and give the jobs the resources (CPU, memory, GPUs) that they need to run. 
私たちのMLパイプラインプログラムを実行するために、それらをコンテナ化し、ジョブにパッケージ化し、実行に必要なリソース（CPU、メモリ、GPU）をジョブに与える方法を見ていきます。

The next section will look at building containers and creating and run‐ ning jobs in Hopsworks. 
次のセクションでは、コンテナの構築とHopsworksでのジョブの作成と実行について見ていきます。

###### Automatic Containerization and Jobs
###### 自動コンテナ化とジョブ

To date, we have defined our ML pipelines as source code, but to run them in produc‐ tion, we also need to define and install their dependencies and the resources they need to run, such as the amount of memory, number of CPU cores, number of GPUs, and number of instances. 
これまで、私たちはMLパイプラインをソースコードとして定義してきましたが、実際に運用するためには、依存関係や実行に必要なリソース（メモリの量、CPUコアの数、GPUの数、インスタンスの数）を定義してインストールする必要があります。

Our ML pipelines may need to run on a schedule or run 24/7. 
私たちのMLパイプラインは、スケジュールに従って実行する必要がある場合や、24時間365日実行する必要がある場合があります。

We will start by looking at how to containerize the program(s) that make up your ML pipeline. 
まず、MLパイプラインを構成するプログラムをコンテナ化する方法を見ていきます。

Many MLOps courses begin with how to develop, compile, register, pull (download), and run Docker images. 
多くのMLOpsコースは、Dockerイメージを開発、コンパイル、登録、プル（ダウンロード）、実行する方法から始まります。

The idea is that you can package your ML pipe‐ line code, along with its dependencies, in a container. 
このアイデアは、MLパイプラインコードとその依存関係をコンテナにパッケージ化できるというものです。

You can then run the con‐ tainer(s) on a container runtime—start with Docker, then move on to production container runtimes, such as Kubernetes or AWS Fargate. 
その後、コンテナをコンテナランタイム上で実行できます。最初はDockerから始め、次にKubernetesやAWS Fargateなどの本番用コンテナランタイムに移行します。

This approach involves learning how to: 
このアプローチでは、以下のことを学ぶ必要があります。

- Write a Dockerfile that includes your program’s source code, dependencies, and how to run it. Parameterize it with environment variables. 
  - プログラムのソースコード、依存関係、および実行方法を含むDockerfileを書くこと。環境変数でパラメータ化します。

- Compile a container image from the Dockerfile. 
  - Dockerfileからコンテナイメージをコンパイルします。

- Test your container on your local environment with Docker. 
  - Dockerを使用してローカル環境でコンテナをテストします。

- Register the container image with a container registry. 
  - コンテナイメージをコンテナレジストリに登録します。

- Write a program for an orchestrator to schedule the execution of your container on a container runtime like Kubernetes. 
  - オーケストレーター用のプログラムを書いて、Kubernetesのようなコンテナランタイム上でコンテナの実行をスケジュールします。

While working with containers is a useful skill, it is not a requirement for building AI systems. 
コンテナを扱うことは有用なスキルですが、AIシステムを構築するための必須条件ではありません。

An easier approach that we use is automatic containerization. 
私たちが使用するより簡単なアプローチは、自動コンテナ化です。

_Automatic_ _containerization is an umbrella term for methods that transparently build containers_ 
自動コンテナ化は、透明にコンテナを構築する方法の総称です。

for programs that include library dependencies and operating system dependencies. 
ライブラリ依存関係やオペレーティングシステム依存関係を含むプログラムのためのものです。

Automatic containerization requires a platform that compiles and registers the con‐ tainers from your source code. 
自動コンテナ化には、ソースコードからコンテナをコンパイルして登録するプラットフォームが必要です。

Automatic containerization platforms also provide an orchestrator to download and run/schedule the container as jobs. 
自動コンテナ化プラットフォームは、コンテナをジョブとしてダウンロードし、実行/スケジュールするためのオーケストレーターも提供します。

That means that the only abstractions developers need to be concerned with are their programs and jobs. 
つまり、開発者が関心を持つ必要があるのは、プログラムとジョブだけです。

Automatic containerization platforms build container images starting from a: 
自動コンテナ化プラットフォームは、以下からコンテナイメージを構築します。

- Base Docker image in which you can install operating system packages 
  - オペレーティングシステムパッケージをインストールできるベースDockerイメージ

- Base Python environment in which you can install Python dependencies 
  - Python依存関係をインストールできるベースPython環境

Some platforms have many base images and/or Python environments to choose from. 
いくつかのプラットフォームには、多くのベースイメージやPython環境が用意されています。

In Figure 13-3, you can see the continuum from writing, compiling, and managing your own containers to automatic containerization solutions that (1) customize con‐ tainers that can be reused by many programs and (2) build a container for every job. 
図13-3では、自分のコンテナを作成、コンパイル、管理することから、(1) 多くのプログラムで再利用できるコンテナをカスタマイズする自動コンテナ化ソリューションや、(2) 各ジョブのためにコンテナを構築する自動コンテナ化ソリューションまでの連続性を見ることができます。

_Figure 13-3. Developers can containerize their pipeline code by writing Dockerfiles and_ _working with a Docker registry. Managed environments and managed jobs containerize_ _code automatically for developers, allowing them to focus solely on writing Python code._ 
図13-3. 開発者はDockerfileを書き、Dockerレジストリで作業することでパイプラインコードをコンテナ化できます。管理された環境と管理されたジョブは、開発者のためにコードを自動的にコンテナ化し、Pythonコードの記述に専念できるようにします。

Now, we will look at two approaches to automatic containerization: Hopsworks and Modal. 
さて、私たちは自動コンテナ化の2つのアプローチ、HopsworksとModalを見ていきます。

###### Environments and Jobs in Hopsworks
###### Hopsworksにおける環境とジョブ

In Hopsworks, you select the most appropriate base container for your ML pipeline or deployment. 
Hopsworksでは、MLパイプラインまたはデプロイメントに最も適切なベースコンテナを選択します。

There are different base containers for feature pipelines (Pandas/Polars, PySpark), training pipelines (XGBoost, Transformers, PyTorch), batch inference (Pan‐ das, PySpark), online inference (KServe/XGBoost, Transformers/vLLM), and agents (LlamaIndex). 
特徴パイプライン（Pandas/Polars、PySpark）、トレーニングパイプライン（XGBoost、Transformers、PyTorch）、バッチ推論（Pandas、PySpark）、オンライン推論（KServe/XGBoost、Transformers/vLLM）、およびエージェント（LlamaIndex）用の異なるベースコンテナがあります。

You can clone and customize the base environments in the UI by: 
UIでベース環境をクローンしてカスタマイズできます。

- Running command-line operations to install operating system packages 
  - オペレーティングシステムパッケージをインストールするためのコマンドライン操作を実行すること

- Installing Python libraries from an artifact repository (PyPI, GitHub, Conda, etc.). 
  - アーティファクトリポジトリ（PyPI、GitHub、Condaなど）からPythonライブラリをインストールすること。

While the UI is useful, for MLOps, we prefer to write code to configure environments and create jobs or model/agent deployments that run in those environments. 
UIは便利ですが、MLOpsでは、環境を構成し、それらの環境で実行されるジョブやモデル/エージェントのデプロイメントを作成するためにコードを書くことを好みます。

In the following code snippet that should be run on Hopsworks, we create an environment and a Spark job to run in that environment: 
以下のコードスニペットはHopsworksで実行されるべきもので、環境とその環境で実行されるSparkジョブを作成します。

```   
proj = hopsworks.login()   
# This code normally goes in the Program itself, not in the Job Creation   
# Assume the book’s repo is already cloned into the Jupyter dir in your project   
repo = git_api.get_repo("mlfs-book",f"/Projects/{proj.name}/Jupyter/mlfs-book" )   
repo.checkout_branch("v1") # Run v1 of job   
repo.checkout("v1") # Run v1 of job   
repo.pull("v1")   
env_api = proj.get_environment_api()   
env = env_api.get_environment("spark-feature-pipeline-v1")   
env.install_requirements("/Jupyter/mlfs-book/spark-requirements.txt")   
# Create a Spark Job to run in the env pyspark_feature_pipeline   
job_api = proj.get_job_api()   
spark_config = job_api.get_configuration("PYSPARK")   
spark_config.update({     
    "spark.driver.memory" : 2048,     
    "spark.driver.cores" : 1,     
    "spark.executor.memory" : 8192,     
    "spark.executor.cores" : 2,     
    "spark.executor.instances" : 20,     
    "environmentName" : "spark-feature-pipeline-v1",     
    "appPath" : "/Resources/my_feature_pipeline.py"   
})   
job = job_api.create_job("my_spark_feature_pipeline", spark_config)   
# Run the Spark job now   
execution = job.run()   
out_log_path, err_log_path = execution.download_logs()   
# Run the Spark job on a schedule every day at 5:00 AM   
job.schedule(     
    cron_expression="0 0 5 * * ?", # quartz cron syntax     
    start_time=datetime.datetime.now(tz=timezone.utc)   
)
```

In the preceding code, we installed Python dependencies from a requirements.txt in a base `spark-feature-pipeline-v1 environment. 
前述のコードでは、ベースの`spark-feature-pipeline-v1`環境のrequirements.txtからPython依存関係をインストールしました。

Then, we defined a PySpark job,` including the program to run (my_feature_pipeline.py), the amount of memory and CPU cores for the Spark driver and workers, and the number of workers. 
次に、実行するプログラム（my_feature_pipeline.py）、SparkドライバーとワーカーのためのメモリとCPUコアの量、ワーカーの数を含むPySparkジョブを定義しました。

Jobs can be run eagerly or scheduled to run at time intervals defined using a cron expression. 
ジョブは即時に実行することも、cron式を使用して定義された時間間隔で実行するようにスケジュールすることもできます。

In Hopsworks, the Python dependencies can be downloaded from a PyPI server, a Conda server, or a Git repository, or they can be provided in a wheel file. 
Hopsworksでは、Python依存関係はPyPIサーバー、Condaサーバー、またはGitリポジトリからダウンロードすることができ、またはwheelファイルで提供されることもあります。

Figure 13-4 shows how you can select and configure a container for use by a job. 
図13-4は、ジョブで使用するためにコンテナを選択して構成する方法を示しています。

Hopsworks uses _Papermill to run Jupyter notebooks as jobs. 
Hopsworksは、Jupyterノートブックをジョブとして実行するために_Papermill_を使用します。

Typically, the source code for your pro‐ grams/jobs is checked out from a source code repository and put into a directory in Hopsworks. 
通常、プログラム/ジョブのソースコードはソースコードリポジトリからチェックアウトされ、Hopsworksのディレクトリに配置されます。

_Figure 13-4. Jobs and deployments are created using a program (Pandas, Polars, Spark,_ _PyTorch, etc.) and a container in Hopsworks. Jobs can be scheduled or orchestrated by_ _Airflow._  
図13-4. ジョブとデプロイメントは、Hopsworks内のプログラム（Pandas、Polars、Spark、PyTorchなど）とコンテナを使用して作成されます。ジョブはスケジュールまたはAirflowによってオーケストレーションできます。

Hopsworks also includes Airflow to define and run larger ML pipelines as DAGs of jobs. 
Hopsworksには、より大きなMLパイプラインをジョブのDAGとして定義し実行するためのAirflowも含まれています。

For example, you might have five different feature pipelines that should all be scheduled to run once per day at nighttime. 
たとえば、夜間に1日1回実行されるべき5つの異なる特徴パイプラインがあるかもしれません。

They could be separate jobs scheduled by Hopsworks, but what if there is a relationship between them? 
それらはHopsworksによってスケジュールされた別々のジョブである可能性がありますが、彼らの間に関係がある場合はどうでしょうか？

Job B should only start if job A has completed, for example. 
たとえば、ジョブAが完了した場合にのみジョブBが開始されるべきです。

You can define a DAG in Airflow that runs those feature pipelines with derived features computed after their upstream parent features have successfully completed. 
AirflowでDAGを定義し、上流の親特徴が正常に完了した後に計算された派生特徴を持つ特徴パイプラインを実行できます。

This simplifies your operational burden, as you now have one DAG program to monitor, rather than five separate jobs. 
これにより、5つの別々のジョブではなく、1つのDAGプログラムを監視するだけで済むため、運用の負担が軽減されます。

Airflow schedules and monitors the DAGs. 
AirflowはDAGをスケジュールし、監視します。

###### Modal Jobs
###### Modalジョブ

We saw an example of a Modal program in Chapter 8. 
第8章でModalプログラムの例を見ました。

Modal supports program-level automatic containerization. 
Modalはプログラムレベルの自動コンテナ化をサポートしています。

In the following code snippet, we show how to define a container for the Python code that uses `ffmpeg and` `hopsworks. 
以下のコードスニペットでは、`ffmpeg`と`hopsworks`を使用するPythonコードのためのコンテナを定義する方法を示します。

First, we define a` Debian container image with a Python version, then define any OS dependencies with `apt, and then install any Python dependencies with` `pip. 
まず、Pythonバージョンを持つDebianコンテナイメージを定義し、次に`apt`でOS依存関係を定義し、最後に`pip`でPython依存関係をインストールします。

We then attach the` image to a function, `my_function, that will be run as a container in the Modal` runtime: 
次に、`image`を関数`my_function`に添付し、Modalランタイムでコンテナとして実行されます。

```   
image = (     
    modal.Image.debian_slim(python_version="3.12")     
    .apt_install("ffmpeg")     
    .pip_install(["hopsworks", "ffmpeg-python"])   
)   
@app.function(image=image, ...)   
def my_function():     
    ...
```

Note that as this code is run outside Hopsworks, we also need to inject environment variables (the Hopsworks API key and possibly the domain name and project for your Hopsworks cluster). 
このコードはHopsworksの外部で実行されるため、環境変数（Hopsworks APIキーや、場合によってはHopsworksクラスターのドメイン名とプロジェクト）を注入する必要があります。

We didn’t need to add this information to the Hopsworks job earlier, as it is run inside a project and the environment variables are transpar‐ ently injected into the job’s containers. 
この情報を以前のHopsworksジョブに追加する必要はありませんでした。なぜなら、それはプロジェクト内で実行され、環境変数がジョブのコンテナに透明に注入されるからです。

###### CI/CD Tests for AI Systems
###### AIシステムのためのCI/CDテスト

Figure 13-5 visualizes the different suite of tests that cover the AI lifecycle, catego‐ rized by development tests that are executed offline when building your ML pipelines and operational tests that are run as part of system operation. 
図13-5は、AIライフサイクルをカバーするさまざまなテストスイートを視覚化しており、MLパイプラインを構築する際にオフラインで実行される開発テストと、システム運用の一部として実行される運用テストに分類されています。

_Figure 13-5. Testing AI systems requires testing all the ML pipelines and the artifacts_ _they produce, as well as the final models and their interactions with client applications._ 
図13-5. AIシステムのテストには、すべてのMLパイプラインとそれらが生成するアーティファクト、最終モデル、およびクライアントアプリケーションとの相互作用をテストする必要があります。

Some of the open source technologies that we will introduce to help with testing are: 
テストを支援するために紹介するオープンソース技術のいくつかは次のとおりです。

[• pytest to run unit tests for feature functions and transformation functions (Chap‐](https://oreil.ly/iy6hF) ter 7) 
[• Great Expectations to run data validation tests in feature pipelines (Chapter 6)](https://oreil.ly/7ZS3u) 
[• KServe to test model deployments (Chapter 11)](https://oreil.ly/MbMQO) 
[• NannyML for model/feature monitoring (Chapter 14)](https://oreil.ly/ipvH0) 



We will now dive into the tests we haven’t covered yet, including feature pipeline tests, model validation tests, model deployment tests, and batch inference pipeline tests, concluding testing with evals for agents.
これから、まだ取り上げていないテスト、すなわちフィーチャーパイプラインテスト、モデル検証テスト、モデルデプロイメントテスト、バッチ推論パイプラインテストに dive し、エージェントの evals でテストを締めくくります。

You will need very different types of integration tests for FTI pipelines. 
FTI パイプラインには、非常に異なるタイプの統合テストが必要です。

Feature pipelines validate data output and invariants in transformations, while training pipelines validate properties of a trained model (free from bias, performance, etc.). 
フィーチャーパイプラインはデータ出力と変換の不変性を検証し、トレーニングパイプラインはトレーニングされたモデルの特性（バイアスがないこと、パフォーマンスなど）を検証します。

Inference pipelines should validate that predictions are of high quality and meet SLOs.
推論パイプラインは、予測が高品質であり、SLO（サービスレベル目標）を満たしていることを検証する必要があります。

###### Feature Pipeline Tests
###### フィーチャーパイプラインテスト

Feature pipelines write featurized DataFrames to one or more feature groups. 
フィーチャーパイプラインは、特徴化された DataFrame を 1 つ以上のフィーチャーグループに書き込みます。

To test a feature pipeline, you will need to refactor it into separate functions, so that you can mock the source data and any data validation tests. 
フィーチャーパイプラインをテストするには、それを別々の関数にリファクタリングする必要があります。そうすることで、ソースデータやデータ検証テストをモックできます。

The feature pipeline itself will also need to be encapsulated in a function. 
フィーチャーパイプライン自体も関数にカプセル化する必要があります。

You will use some sample source data that you commit to version control, to remove any dependency on an external data source.
外部データソースへの依存を排除するために、バージョン管理にコミットするサンプルソースデータを使用します。

The feature pipeline will write to a development feature store, the connection to which you can configure with environment variables or explicit parameters. 
フィーチャーパイプラインは、開発フィーチャーストアに書き込みます。その接続は、環境変数または明示的なパラメータで構成できます。

The following code snippet shows the production feature pipeline that contains a data source function, a function that creates data validation rules as _expectations, a function for_ the actual feature pipeline, and an entry point (main) when you run the feature pipe‐ line. 
以下のコードスニペットは、データソース関数、データ検証ルールを _expectations として作成する関数、実際のフィーチャーパイプラインの関数、およびフィーチャーパイプラインを実行する際のエントリポイント（main）を含むプロダクションフィーチャーパイプラインを示しています。

This pipeline could be scheduled to run daily by Airflow, which would provide `start_ts` and `end_ts` as parameters for each run.
このパイプラインは、Airflow によって毎日実行されるようにスケジュールでき、各実行のパラメータとして `start_ts` と `end_ts` を提供します。

```python
def read_data_source(fs, start_ts, end_ts):     
    fg = fs.get_feature_group("transactions", version=1)     
    return fg.filter((fg.ts > start_ts) & (fg.ts <= end_ts)).read()   

def fg2_expectations():     
    expectation_suite = ge.core.ExpectationSuite(expectation_suite_name="ge_fg")     
    expectation_suite.add_expectation(       
        ge.core.ExpectationConfiguration(       
            expectation_type="expect_column_values_to_be_between",       
            kwargs={"column":"amount", "min_value": 0, "max_value": 1000000})     
    )     
    return expectation_suite   

def create_feature_group(fs):     
    suite = fg2_expectations()     
    fg = fs.create_feature_group("cc_aggs_trans", version=1,       
        primary_key=["cc_num"], expectation_suite=suite     
    )     
    return fg   

# This function is run by the pipeline test   
def pipeline(fs, df):     
    fg2 = fs.get_feature_group("cc_aggs_trans", version=1)     
    if not fg2:
        fg2 = create_feature_group(fs)     
    return fg2.insert(df)
```

Our feature pipeline test can be run as a program; it requires the development feature store to be available but doesn’t require the data source to be available. 
私たちのフィーチャーパイプラインテストはプログラムとして実行でき、開発フィーチャーストアが利用可能である必要がありますが、データソースが利用可能である必要はありません。

Instead, the source data comes from `sample_transactions.csv`, a file you can create by asking an LLM to create synthetic data. 
代わりに、ソースデータは `sample_transactions.csv` から取得されます。このファイルは、LLM に合成データを作成するように依頼することで作成できます。

Synthetic data avoids compliance problems that may arise from using samples of production data. 
合成データは、プロダクションデータのサンプルを使用することから生じる可能性のあるコンプライアンスの問題を回避します。

In our pipeline test, you can ensure that our target feature group(s), `cc_aggs_trans`, is empty by dropping and re-creating it. 
パイプラインテストでは、ターゲットフィーチャーグループ（`cc_aggs_trans`）が空であることを確認するために、それを削除して再作成できます。

You need to create the expectation suite in a separate function, as this enables our test to attach it to `fg` with the `always ingestion policy—otherwise ingestion would fail` and our test would not complete. 
期待値スイートは別の関数で作成する必要があります。これにより、テストが `fg` に `always ingestion policy` を付けることができ、そうでなければインジェストが失敗し、テストが完了しなくなります。

When you insert the sample data into `fg`, you’ll use the ingestion `job` and `validation_report` to wait for ingestion to complete and ensure the validation tests work as expected on the sample data. 
サンプルデータを `fg` に挿入するとき、インジェスト `job` と `validation_report` を使用してインジェストの完了を待ち、サンプルデータに対して検証テストが期待通りに機能することを確認します。

After inserting data, you can assert that the number of rows of features added to `fg2` should equal the number of rows in our sample data: 
データを挿入した後、`fg2` に追加された特徴の行数がサンプルデータの行数と等しいことを主張できます。

```python
def test_pipeline():     
    fs = hopsworks.login().get_feature_store()     
    # Make sure the target feature group is empty for this test     
    fg2 = fs.get_feature_group("cc_aggs_trans", version=1)     
    if fg2:       
        fg2.delete()       
    # Run the pipeline with simulated data for testing     
    df = pd.read_csv("sample_transactions.csv")     
    job, validation_report = pipeline(fs, df)     
    # Fetch the feature group created and perform required validation     
    fg2 = fs.get_feature_group("cc_aggs_trans", version=1)     
    # Sample data should fail one data validation rule,     
    assert validation_report.statistics["unsuccessful_expectations"] == 1     
    job._wait_for_job()     
    df2 = fg2.read()     
    # Test that the data read is the same as the data written     
    assert len(df) == len(df2)
```

Your CI/CD server will run the unit test, and you can configure the following environment variables to point to your staging feature store: `HOPSWORKS_HOST, HOPSWORKS_PROJECT, and HOPSWORKS_API_KEY.`
CI/CD サーバーはユニットテストを実行し、次の環境変数を構成してステージングフィーチャーストアを指すことができます：`HOPSWORKS_HOST, HOPSWORKS_PROJECT, and HOPSWORKS_API_KEY.`

If you only want to test the pipeline logic and not test writing/reading from the feature store, you can mock all external connections in the pipeline function and then run the pipeline test as a unit test. 
パイプラインのロジックのみをテストし、フィーチャーストアへの書き込み/読み取りをテストしたくない場合は、パイプライン関数内のすべての外部接続をモックし、その後パイプラインテストをユニットテストとして実行できます。

The unit test runtime is much shorter, but you will not be testing the feature pipeline end to end.
ユニットテストの実行時間ははるかに短いですが、フィーチャーパイプラインをエンドツーエンドでテストすることはありません。

In Figure 13-6, you can see how pytest runs the unit tests. 
図 13-6 では、pytest がユニットテストをどのように実行するかを見ることができます。

This architecture is quite flexible, and it is even possible to run the pipeline unit test with different source data in the staging environment by checking whether a `DEV environment variable exists,` then reading a DataFrame from a staging data source or otherwise reading the sample data in `sample_transactions.csv`. 
このアーキテクチャは非常に柔軟で、`DEV` 環境変数が存在するかどうかを確認することで、ステージング環境で異なるソースデータを使用してパイプラインユニットテストを実行することも可能です。その後、ステージングデータソースから DataFrame を読み込むか、そうでなければ `sample_transactions.csv` のサンプルデータを読み込みます。

It is good practice to store sampled data, checked into the source code repository, to remove any dependency on an external data source when running the integration test.
統合テストを実行する際に外部データソースへの依存を排除するために、サンプルデータをソースコードリポジトリにチェックインして保存することは良いプラクティスです。

_Figure 13-6. End-to-end feature pipeline tests._
_図 13-6. エンドツーエンドのフィーチャーパイプラインテスト。_

When a developer has finished implementing their feature pipeline, they run their unit tests (a feature function and pipeline tests) in their development environment.
開発者がフィーチャーパイプラインの実装を終えたら、開発環境でユニットテスト（フィーチャー関数とパイプラインテスト）を実行します。

These can be run on their laptop, in a Hopsworks job, or in an external cluster. 
これらは、彼らのラップトップ、Hopsworks ジョブ、または外部クラスターで実行できます。

If the tests pass, the developer can then create a PR to the staging branch. 
テストが成功した場合、開発者はステージングブランチに PR を作成できます。

A CI/CD service will then check out the code in the PR and run the tests (with the staging environment variables set). 
CI/CD サービスは、PR のコードをチェックアウトし、テストを実行します（ステージング環境変数が設定されている状態で）。

If they pass, a data owner should perform a manual code review before the PR is merged to main.
テストが成功した場合、データオーナーは PR がメインにマージされる前に手動コードレビューを行うべきです。

###### Training Pipeline Tests for Model Performance and Bias
###### モデルのパフォーマンスとバイアスのためのトレーニングパイプラインテスト

Testing training pipelines is radically different from testing feature pipelines. 
トレーニングパイプラインのテストは、フィーチャーパイプラインのテストとは根本的に異なります。

First, the output of a training pipeline is typically one or more trained models. 
まず、トレーニングパイプラインの出力は通常、1 つ以上のトレーニング済みモデルです。

Second, model training can be time-consuming, and development involves hyperparameter tuning and training of smaller models with less data than in a production training run. 
第二に、モデルのトレーニングは時間がかかる場合があり、開発にはハイパーパラメータの調整や、プロダクショントレーニング実行よりも少ないデータでの小さなモデルのトレーニングが含まれます。

The types of model validation steps include checking that model performance falls within an expected range and that the model is free from bias. 
モデル検証ステップの種類には、モデルのパフォーマンスが期待される範囲内に収まっていることを確認し、モデルがバイアスから解放されていることを確認することが含まれます。

In contrast with our feature function tests and feature pipeline tests, model validation tests are always run after a model training run has completed: 
フィーチャー関数テストやフィーチャーパイプラインテストとは対照的に、モデル検証テストは常にモデルのトレーニング実行が完了した後に実行されます。

```python
fv = fs.get_feature_view('cc_fraud', version=1)   
X_train, X_test, y_train, y_test = fv.train_test_split(test_size=0.2, seed=42)   
model.fit(X_train, y_train)   
y_pred = pd.DataFrame(     
    model.predict(X_test),     
    columns=y_test.columns,     
    index=X_test.index   
)   

# calculate y_pred for online and offline merchants   
pred_df = pd.concat([X_test, y_pred], axis=1)   
y_pred_online = pred_df[pred_df['card_present']].loc[:, y_test.columns]   
y_pred_offline = pred_df[~pred_df['card_present']].loc[:, y_test.columns]   

# calculate y_test for online and offline merchants   
test_df = pd.concat([X_test, y_test], axis=1)   
y_test_online = test_df[test_df['card_present']].loc[:, y_test.columns]   
y_test_offline = test_df[~test_df['card_present']].loc[:, y_test.columns]   

f1_online = f1_score(y_test_online, y_pred_online)   
f1_offline = f1_score(y_test_offline, y_pred_offline)
```

You can also use filters when reading training data, using feature views to read your evaluation test data directly from the feature store as follows: 
トレーニングデータを読み込む際にフィルターを使用することもでき、フィーチャービューを使用して評価テストデータをフィーチャーストアから直接読み込むことができます。

```python
_, X_test_offline, _, y_test_offline = fv.filter(Feature("card_present") == True).train_test_split(test_size=0.2, seed=42)   
_, X_test_online, _, y_test_online = fv.filter(Feature("card_present") == False).train_test_split(test_size=0.2, seed=42)
```

In Figure 13-7, you can see how a successful training run on the development branch can lead to a full training run on production data. 
図 13-7 では、開発ブランチでの成功したトレーニング実行が、プロダクションデータでの完全なトレーニング実行につながる様子を見ることができます。

Training pipeline integration tests need access to sample data to run, and it is common that they are connected directly to the feature store. 
トレーニングパイプラインの統合テストは実行するためにサンプルデータへのアクセスが必要であり、フィーチャーストアに直接接続されていることが一般的です。

You can use environment variables to select the appropriate feature store, depending on whether the test is run in development or production.
テストが開発環境で実行されるかプロダクション環境で実行されるかに応じて、環境変数を使用して適切なフィーチャーストアを選択できます。

_Figure 13-7. End-to-end training pipeline tests._
_図 13-7. エンドツーエンドのトレーニングパイプラインテスト。_

The production training run can be triggered manually or using CI/CD. 
プロダクショントレーニング実行は手動または CI/CD を使用してトリガーできます。

If the production training run succeeds, the model deployment owner approves the deployment of the model by running a separate model deployment pipeline, typically a blue/green test of the new version of the model.
プロダクショントレーニング実行が成功した場合、モデルデプロイメントオーナーは、別のモデルデプロイメントパイプラインを実行することでモデルのデプロイメントを承認します。通常は新しいバージョンのモデルのブルー/グリーンテストです。

###### Testing Model Deployments
###### モデルデプロイメントのテスト

Before you deploy a new model version, you should test it with production traffic. 
新しいモデルバージョンをデプロイする前に、プロダクショントラフィックでテストする必要があります。

You can do this by using either A/B tests or blue/green tests. 
これを行うには、A/B テストまたはブルー/グリーンテストを使用できます。

A/B tests split the prediction requests into X% that go to the production model and Y% that go to the challenger model. 
A/B テストは、予測リクエストを X% をプロダクションモデルに、Y% をチャレンジャーモデルに分割します。

For example, 99% can go to production and 1% can go to the challenger. 
例えば、99% をプロダクションに、1% をチャレンジャーに送ることができます。

A/B tests are not for testing the model deployment. 
A/B テストはモデルデプロイメントをテストするためのものではありません。

They are for testing the model’s effect on the application that uses the new version of the model. 
それらは、新しいバージョンのモデルを使用するアプリケーションに対するモデルの効果をテストするためのものです。

The A/B test will be connected to an application-level KPI that can also be split into X% and Y% of clients. 
A/B テストは、クライアントの X% と Y% に分割できるアプリケーションレベルの KPI に接続されます。

Examples of KPIs include click-through rate, engagement, revenue lift, conversion rate, and
KPI の例には、クリック率、エンゲージメント、収益の向上、コンバージョン率などがあります。



task/session success/failure rates. A/B tests let you see whether the new model version improves the KPI for the Y% of clients or not, before you replace the production model with the challenger model.
タスク/セッションの成功/失敗率。A/Bテストは、新しいモデルバージョンがY%のクライアントに対するKPIを改善するかどうかを確認することを可能にし、その後に生産モデルを挑戦者モデルに置き換えます。

Blue/green tests test the correctness and performance of the model directly. You send 100% of requests to the production (blue) model and Y% of requests to the challenger (green) model. 
ブルー/グリーンテストは、モデルの正確性とパフォーマンスを直接テストします。100%のリクエストを生産（青）モデルに送り、Y%のリクエストを挑戦者（緑）モデルに送ります。

Y% can be anything from 1% to 100% of prediction requests. Blue/ green testing is risk-free testing for the clients that use it. 
Y%は、予測リクエストの1%から100%の範囲の任意の値にすることができます。ブルー/グリーンテストは、それを使用するクライアントにとってリスクのないテストです。

You can detect problems before exposing clients to the new model. 
新しいモデルにクライアントをさらす前に問題を検出することができます。

You can run both A/B tests and blue/green tests on KServe. 
KServeでは、A/Bテストとブルー/グリーンテストの両方を実行できます。

In Figure 13-8, you can see how to deploy a challenger model alongside the production version of the model, in a blue/green deployment. 
図13-8では、ブルー/グリーンデプロイメントにおいて、挑戦者モデルを生産モデルのバージョンと並行してデプロイする方法を見ることができます。

_Figure 13-8. Blue/green testing of a model deployment._ 
_Figure 13-8. モデルデプロイメントのブルー/グリーンテスト。_

You can compare the performance of the two models for a period of time by parsing the prediction logs. 
予測ログを解析することで、一定期間にわたって2つのモデルのパフォーマンスを比較できます。

If there is a large amount of traffic on the production model, you can start by sending only a small percentage of production traffic to the challenger model and slowly increasing the percentage. 
生産モデルに大量のトラフィックがある場合は、最初に生産トラフィックのごく一部を挑戦者モデルに送信し、徐々にその割合を増やすことができます。

If, after a period of time, you observe that the challenger model outperforms the production model, you can replace the production model with the challenger model. 
一定期間後に、挑戦者モデルが生産モデルを上回ることを観察した場合は、生産モデルを挑戦者モデルに置き換えることができます。

Alternatively, you can then start with an A/B test and slowly increase traffic on the new model if the application KPIs are improved for the new model.
あるいは、アプリケーションのKPIが新しいモデルで改善された場合は、A/Bテストから始めて新しいモデルへのトラフィックを徐々に増やすこともできます。



###### A/B Tests for Batch Inference
Batch inference AI systems should also be A/B tested before you upgrade a model version.
バッチ推論AIシステムは、モデルバージョンをアップグレードする前にA/Bテストを実施する必要があります。

Rather than performing a live A/B test on batch inference runs, you typically perform an A/B test by backtesting a model with historical data and comparing the challenger model’s performance with the current production model.
バッチ推論の実行に対してライブA/Bテストを行うのではなく、通常は過去のデータを用いてモデルをバックテストし、挑戦モデルのパフォーマンスを現在の本番モデルと比較することでA/Bテストを実施します。

You can do this in the training pipeline after the model has been trained.
これは、モデルがトレーニングされた後のトレーニングパイプラインで行うことができます。

You should measure a model’s performance as a single scalar value so that you can easily compare the model’s performance with the currently deployed model.
モデルのパフォーマンスは単一のスカラー値として測定するべきであり、これにより現在デプロイされているモデルとのパフォーマンスを簡単に比較できます。

Then your batch inference pipeline can just retrieve the “best” model: 
その後、バッチ推論パイプラインは「最良の」モデルを取得することができます：
```   
model = mr.get_best_model(name='model', metric='performance', direction='max')
```

###### Evals for Agents
LLM applications and agents are more complex to test than model deployments, as they do much more than just invoke an LLM.
LLMアプリケーションとエージェントは、モデルデプロイメントよりもテストが複雑であり、単にLLMを呼び出す以上のことを行います。

They take a number of steps before they respond to client queries.
彼らはクライアントのクエリに応答する前にいくつかのステップを踏みます。

Changes in any of the following can affect the quality of responses:
以下のいずれかの変更が応答の質に影響を与える可能性があります：
- The LLM(s) used.
- 使用されるLLM。
- The system prompt.
- システムプロンプト。
- RAG queries.
- RAGクエリ。
- RAG data source updates.
- RAGデータソースの更新。

For example, if new data is added to your vector index, your RAG queries might return different context (examples), positively or negatively affecting the quality of the agent responses.
例えば、新しいデータがベクトルインデックスに追加されると、RAGクエリは異なるコンテキスト（例）を返す可能性があり、エージェントの応答の質に良い影響を与えたり悪い影響を与えたりします。

Instead of developing individual tests for each step taken by an agent, we will look at end-to-end tests that evaluate whether any changes at any step improved the agent performance or not.
エージェントが踏む各ステップに対して個別のテストを開発するのではなく、任意のステップでの変更がエージェントのパフォーマンスを改善したかどうかを評価するエンドツーエンドテストを見ていきます。

That is, we will evaluate the agent’s responses to a curated set of prompts.
つまり、キュレーションされたプロンプトのセットに対するエージェントの応答を評価します。

We call this dataset of prompts and expected outputs evals (short for evaluations).
このプロンプトと期待される出力のデータセットをevals（評価の略）と呼びます。

We use the evals to score the agent responses with the expected responses.
私たちはevalsを使用して、エージェントの応答を期待される応答とスコアリングします。

If the total score improves, then we can say that the changes passed the evals.
総スコアが改善された場合、変更がevalsを通過したと言えます。

If the agent’s total score decreases, we can say that the agent failed the evals.
エージェントの総スコアが減少した場合、エージェントがevalsに失敗したと言えます。

An example eval architecture for storing and scoring responses is shown in Figure 13-9.  
応答を保存しスコアリングするためのevalアーキテクチャの例は、図13-9に示されています。

_Figure 13-9. Automate the evaluation of changes in LLM agents using evals (prompts and expected responses) and an evaluator that scores the performance of the agent on the evals._
図13-9. evals（プロンプトと期待される応答）を使用してLLMエージェントの変更の評価を自動化し、エージェントのevalsにおけるパフォーマンスをスコアリングする評価者。

Evals are tabular datasets, with columns for the `eval_id,` `task to perform,` `prompt,` and `expected_response. 
Evalsは、`eval_id`、`task to perform`、`prompt`、および`expected_response`の列を持つ表形式のデータセットです。

You can leverage the feature store to store evals and the `responses to running the evals (eval_runs).
フィーチャーストアを活用してevalsと`evalsを実行した結果（eval_runs）を保存できます。

Evals are run against an agent deployment in a staging environment, where the agent is connected to the same LLM and tools that it uses in production.
Evalsは、エージェントが本番で使用するのと同じLLMおよびツールに接続されたステージング環境のエージェントデプロイメントに対して実行されます。

The agent (or LLM workflow) outputs traces—logs for all the steps the agent takes, including RAG request/responses, LLM request/responses, prompt templates used, and the final response to the original request.
エージェント（またはLLMワークフロー）は、RAGリクエスト/応答、LLMリクエスト/応答、使用されたプロンプトテンプレート、および元のリクエストに対する最終応答を含む、エージェントが踏むすべてのステップのログであるトレースを出力します。

You can store the traces as logging feature groups in Hopsworks.  
トレースはHopsworksのロギングフィーチャーグループとして保存できます。

Running evals for an LLM agent is similar to backfilling a feature pipeline.
LLMエージェントのevalsを実行することは、フィーチャーパイプラインのバックフィリングに似ています。

In both cases, you have the same production program, and you run it with historical data as input.
どちらの場合も、同じ本番プログラムがあり、過去のデータを入力として実行します。

For evals, your LLM agent reads from the evals dataset and its output is eval runs that are then scored by an evaluator.
evalsの場合、LLMエージェントはevalsデータセットから読み取り、その出力はeval_runsであり、評価者によってスコアリングされます。

An evaluator is a program you write that processes the traces and expected responses from the evals dataset to score the responses and store them as eval runs.
評価者は、トレースとevalsデータセットからの期待される応答を処理して応答にスコアを付け、それらをeval_runsとして保存するプログラムです。

If your eval responses are subjective, you can use an LLM-as-a-judge as the evaluator.
eval応答が主観的な場合、LLMを評価者として使用できます。

If your eval describes an objective task, the results of which can be measured or inspected, you can write a task-specific program to evaluate whether the agent correctly executes the expected task in response to the prompt.
evalが測定または検査可能な客観的なタスクを説明する場合、エージェントがプロンプトに応じて期待されるタスクを正しく実行するかどうかを評価するためのタスク特化型プログラムを書くことができます。

There are many classes of response that you should look for when scoring your objective evals, including:
客観的なevalをスコアリングする際に探すべき応答の多くのクラスがあります：
_Hallucinations_ Context adherence, correctness, and uncertainty
_幻覚_ コンテキストの遵守、正確性、および不確実性

_Safety_ Toxicity, bias, PII, tone, and prompt injection
_安全性_ 有害性、バイアス、PII、トーン、およびプロンプトインジェクション

What scoring system should you use? 
どのスコアリングシステムを使用すべきですか？

The two most popular approaches are _binary classification and the Likert scale (1 to 5).
最も人気のある2つのアプローチは、_バイナリ分類とリッカートスケール（1から5）です。

If you have a small number of responses to score and you are confident in the quality of the scorers, the Likert scale contains more information and enables you to track gradual improvements.
スコアを付ける応答の数が少なく、スコアラーの質に自信がある場合、リッカートスケールはより多くの情報を含み、徐々に改善を追跡することができます。

However, binary classification enables faster scoring by humans and commits them to making a decision—there’s no hiding behind a score of 2 or 3.
しかし、バイナリ分類は人間によるスコアリングを迅速にし、彼らに決定を下すことを求めます—スコア2や3の後ろに隠れることはできません。

As well as a score, the evaluator can update each entry in `eval_runs with` `feedback, a human-readable explanation for the score` given to an eval.
スコアに加えて、評価者は`eval_runs`の各エントリを`フィードバック`で更新でき、これはevalに与えられたスコアの人間が読める説明です。

The best evals are application specific.
最良のevalはアプリケーション特有のものです。

They test both edge cases and common cases for user inputs.
それらはユーザー入力のエッジケースと一般的なケースの両方をテストします。

For agents that retrieve context with RAG, it is also possible to write separate evals for your RAG queries, with measurements of the quality of RAG responses, including chunk attribution, chunk utilization, context relevance, and completeness.
RAGを使用してコンテキストを取得するエージェントの場合、RAGクエリに対して別々のevalを作成し、チャンクの帰属、チャンクの利用、コンテキストの関連性、および完全性を含むRAG応答の質を測定することも可能です。

An example of a prompt used by the open source Opik framework for an LLM-as-a-judge is the following:
オープンソースのOpikフレームワークでLLMを評価者として使用するためのプロンプトの例は以下の通りです：

User
You are an impartial AI judge. Evaluate if the assistant’s output effectively addresses the user’s input. Consider: accuracy, completeness, and relevance. Provide a score (1-5) and explain your reasoning in one clear sentence.
ユーザー
あなたは公平なAI評価者です。アシスタントの出力がユーザーの入力に効果的に対処しているかどうかを評価してください。考慮すべき点：正確性、完全性、関連性。スコア（1-5）を提供し、あなたの理由を1つの明確な文で説明してください。

INPUT:
{{input}}
OUTPUT:
{{output}}  
-----
For example, imagine you are building a customer support agent for a food delivery app.
例えば、食料品配達アプリのカスタマーサポートエージェントを構築していると想像してください。

The user might say, “I need a refund.”
ユーザーは「返金が必要です」と言うかもしれません。

The agent needs to know contextual information—order details, delivery-tracking details, and so on.
エージェントはコンテキスト情報—注文の詳細、配達追跡の詳細など—を知る必要があります。

Now you have written a prompt template that needs to be rendered with contextual information.
今、あなたはコンテキスト情報でレンダリングする必要があるプロンプトテンプレートを書きました。

This rendered prompt is what the model will use to decide whether or not to issue a refund.
このレンダリングされたプロンプトは、モデルが返金を発行するかどうかを決定するために使用されます。

Before you deploy this prompt to production, you will want to evaluate its performance—instances where it correctly decided to issue or decline a refund.
このプロンプトを本番環境にデプロイする前に、そのパフォーマンス—返金を発行するか拒否するかを正しく決定したインスタンス—を評価したいでしょう。

To evaluate, you can “replay” historical refund requests.
評価するために、過去の返金リクエストを「再生」することができます。

The issue is that the information in the context changes with time.
問題は、コンテキスト内の情報が時間とともに変化することです。

You will want to instead simulate the value of the context at a historical point in time—or time-travel.
代わりに、過去の特定の時点でのコンテキストの値をシミュレートしたいでしょう—つまり、タイムトラベルです。

For example, in Hopsworks, we built an LLM assistant that helps you perform many different tasks, such as building FTI pipelines.
例えば、Hopsworksでは、FTIパイプラインの構築など、さまざまなタスクを実行するのを助けるLLMアシスタントを構築しました。

One eval we designed is a prompt that generates a feature pipeline for a given data source.
私たちが設計した1つのevalは、特定のデータソースのためのフィーチャーパイプラインを生成するプロンプトです。

When we make changes in the Hopsworks assistant, we rerun the evals.
Hopsworksアシスタントに変更を加えると、evalを再実行します。

The eval tests run the feature pipeline created by the eval prompt and then provide a score for that particular eval, indicating whether or not it successfully created the expected features.
evalテストはevalプロンプトによって作成されたフィーチャーパイプラインを実行し、その特定のevalに対してスコアを提供し、期待されるフィーチャーを成功裏に作成したかどうかを示します。

But how do you design a library of evals for your LLM agent?
しかし、LLMエージェントのためのevalのライブラリをどのように設計しますか？

We will look in detail at generating evals from production traces in Chapter 14, but for bootstrapping your evals without any production traces, you can start by using a powerful trainer LLM to generate synthetic prompts and expected responses.
私たちは第14章で本番トレースからevalを生成する方法を詳しく見ていきますが、本番トレースなしでevalをブートストラップするためには、強力なトレーナーLLMを使用して合成プロンプトと期待される応答を生成することから始めることができます。

We will then look at the challenge of running evals with RAG data sources that do not support point-in-time correct data.
次に、時点において正しいデータをサポートしないRAGデータソースでevalを実行する際の課題を見ていきます。

###### LLM-assisted synthetic eval generation
LLM-assisted synthetic eval generation
LLM支援の合成eval生成

When generating synthetic evals, follow these key principles to ensure it’s effective:
合成evalを生成する際は、効果的であることを保証するために以下の重要な原則に従ってください：

_Diversify your dataset_ Create examples that cover a wide range of features, scenarios, and personas.
_データセットを多様化する_ 幅広い特徴、シナリオ、ペルソナをカバーする例を作成します。

This diversity helps you identify edge cases and failure modes you might not anticipate otherwise.
この多様性は、他では予測できないエッジケースや失敗モードを特定するのに役立ちます。

_Generate user inputs, not outputs_ Use LLMs to generate realistic user queries or inputs, not the expected AI responses.
_ユーザー入力を生成する、出力ではなく_ LLMを使用して、期待されるAI応答ではなく、現実的なユーザークエリや入力を生成します。

This prevents your synthetic data from inheriting the biases or limitations of the generating model.
これにより、合成データが生成モデルのバイアスや制限を引き継ぐのを防ぎます。

This principle is hard to keep, though.
ただし、この原則を守るのは難しいです。

Sometimes you will just create the expected responses with the same LLM and manually clean them up.
時には、同じLLMで期待される応答を作成し、それを手動でクリーンアップすることになります。

_Incorporate real system constraints_ Ground your synthetic data in actual system limitations and data sources that will be available when you are running the evals.
_実際のシステム制約を組み込む_ 合成データを、evalを実行する際に利用可能な実際のシステム制約やデータソースに基づいて構築します。

_Verify scenario coverage_ Ensure your generated data actually triggers the scenarios you want to test.
_シナリオカバレッジを確認する_ 生成したデータが実際にテストしたいシナリオを引き起こすことを確認します。

_Use a powerful (frontier) LLM_ Frontier models are currently superior to smaller models for generating synthetic evals.
_強力な（フロンティア）LLMを使用する_ フロンティアモデルは、合成evalを生成するために現在小型モデルよりも優れています。

To make some of this advice concrete, you can use the example of the Hopsworks coding assistant, Brewer.
このアドバイスを具体的にするために、HopsworksコーディングアシスタントBrewerの例を使用できます。

You can ask the following:
次のことを尋ねることができます：
- What tasks does your coding assistant support?
- あなたのコーディングアシスタントはどのようなタスクをサポートしていますか？
- What type of situations will it encounter?
- どのような状況に直面しますか？
- Which user personas will be using it and how?
- どのユーザーペルソナがそれを使用し、どのように使用しますか？

We then ask an LLM to generate a prompt that, in turn, could generate evals for us:
次に、LLMにプロンプトを生成するように依頼し、それが私たちのためにevalを生成できるようにします：
Can you help create a prompt that can be used to generate the evals for my agent? 
私のエージェントのevalを生成するために使用できるプロンプトを作成するのを手伝ってくれますか？

The evals should be tabular data with these columns: 
evalは、次の列を持つ表形式のデータであるべきです：
```     
columns_for_evals = [       
eval_id, event_ts, task, prompt, expected_response     
]
```

Here is a guide for the type of evals I want to create: 
私が作成したいevalのタイプに関するガイドは次のとおりです：
```     
tasks = [       
"create-feature-pipeline"     
]     
scenarios = [       
"data source reading", #Help with data sources (external feature groups)       
"data transformations",#Help with creating features to create       
"data cleaning",    #Help with removing duplicates, formatting dates       
"data validation"   #Help identifying data validation rules     
]     
personas = [       
"data_engineer",    #Needs help with data science concepts       
"data_scientist",   #Needs help with data engineering concepts       
"ml_engineer",     #Needs help with advanced data science       
"novice"        #Needs help with everything     
]
```

While this advice for creating synthetic evals may not stand the test of time, one thing you need to consider when running your evals is that they may use RAG data sources.
合成evalを作成するためのこのアドバイスは時の試練に耐えないかもしれませんが、evalを実行する際に考慮すべきことの1つは、RAGデータソースを使用する可能性があるということです。

You don’t want an update to a RAG data source to break your evals.
RAGデータソースの更新があなたのevalを壊すことは望ましくありません。



###### Historical evals require point-in-time correct RAG data
###### 歴史的評価には、時点において正しいRAGデータが必要です

When an agent retrieves data from an external source via RAG, there is no guarantee that rerunning the same query on the external source will return the same data. 
エージェントがRAGを介して外部ソースからデータを取得する際、同じクエリを外部ソースで再実行しても同じデータが返される保証はありません。

If the vector index or MCP server queries data from a mutable data source, executing the same query at a different point in time may return a different response. 
ベクターインデックスまたはMCPサーバーが可変データソースからデータをクエリする場合、異なる時点で同じクエリを実行すると異なる応答が返される可能性があります。

To make the retrieval operations idempotent, all the data sources need to support time travel, and the queries need to include a timestamp to retrieve the response as of that point in time. 
取得操作を冪等にするためには、すべてのデータソースがタイムトラベルをサポートし、クエリにはその時点での応答を取得するためのタイムスタンプを含める必要があります。

Our current vector index and online feature stores do not have that capability, although lakehouse tables could. 
現在の私たちのベクターインデックスとオンラインフィーチャーストアにはその機能がありませんが、レイクハウステーブルには可能性があります。

There are many different ways in which you can handle this problem. 
この問題に対処する方法はいくつかあります。

You could double down on synthetic evals and create immutable RAG data sources in your development environment, so that RAG queries are predictable. 
合成評価に注力し、開発環境で不変のRAGデータソースを作成することで、RAGクエリを予測可能にすることができます。

Alternatively, a better approach, in my opinion, is to continually update your evals dataset. 
あるいは、私の意見では、評価データセットを継続的に更新する方が良いアプローチです。

You can log each request/response for your production agent as an eval along with a TTL. 
本番エージェントの各リクエスト/レスポンスを評価としてTTLと共にログに記録できます。

The TTL should be set to expire just before the RAG data it queries expires. 
TTLは、クエリするRAGデータが期限切れになる直前に期限切れになるように設定する必要があります。

That way, you can run your evals against production RAG data sources. 
そうすれば、本番のRAGデータソースに対して評価を実行できます。

###### Governance
###### ガバナンス

_Governance is an oft-used, little understood term in data platforms. It refers to the_ policies, processes, and controls that ensure that an organization is compliant with regulations and internal policies. 
ガバナンスは、データプラットフォームでよく使われるがあまり理解されていない用語です。これは、組織が規制や内部ポリシーに準拠していることを保証するためのポリシー、プロセス、およびコントロールを指します。

AI data governance is the exercise of authority and control (planning, monitoring, and enforcement) over the management of AI data assets (features, training data, models, deployments). 
AIデータガバナンスは、AIデータ資産（特徴、トレーニングデータ、モデル、デプロイメント）の管理に対する権限とコントロール（計画、監視、施行）を行使することです。

In practice, this means that your training datasets should be free of bias; there should be traceability for decisions made by AI systems; AI systems should be accurate, robust, and secure; and they should support human oversight. 
実際には、トレーニングデータセットはバイアスがないべきであり、AIシステムによって行われた決定のトレーサビリティが必要です。AIシステムは正確で堅牢かつ安全であるべきであり、人間の監視をサポートする必要があります。

Governance is more than just being compliant; it should also ensure that data is accurate, secure, and used responsibly across an organization. 
ガバナンスは単に準拠しているだけではなく、データが正確で安全であり、組織全体で責任を持って使用されることを保証する必要があります。

Governance also covers data quality, access control, lineage, and auditing. 
ガバナンスはデータの品質、アクセス制御、系譜、および監査もカバーします。

We will look first at schematized tags to define governance policies for AI assets, lineage to capture dependencies between ML pipelines and AI assets, versioning to control the lifecycle of AI assets, and audit logs to identify violations of policies. 
まず、AI資産のガバナンスポリシーを定義するためのスキーマ化されたタグ、MLパイプラインとAI資産間の依存関係をキャプチャするための系譜、AI資産のライフサイクルを制御するためのバージョン管理、ポリシー違反を特定するための監査ログを見ていきます。

###### Schematized Tags
###### スキーマ化されたタグ

_Custom metadata is a general-purpose tool you can use to describe and discover AI_ assets and to define governance policies. 
カスタムメタデータは、AI資産を記述し発見するために使用できる汎用ツールであり、ガバナンスポリシーを定義するためにも使用されます。

You can design custom metadata to describe an AI asset and how to use it, whether it has passed compliance and CI/CD tests, what its permitted scope of use and estimated cost is, and so on. 
AI資産を記述し、その使用方法、コンプライアンスおよびCI/CDテストに合格したかどうか、許可された使用範囲や推定コストなどを記述するためにカスタムメタデータを設計できます。

You can index an AI asset for search using its custom metadata, helping promote discoverability and reuse. 
カスタムメタデータを使用してAI資産を検索用にインデックス化することで、発見性と再利用を促進します。

In practice, you can create an unlimited amount of custom metadata for AI assets. 
実際には、AI資産のために無限のカスタムメタデータを作成できます。

We will look at schematized tags as a generic mechanism for designing searchable metadata in Hopsworks. 
Hopsworksにおける検索可能なメタデータを設計するための一般的なメカニズムとして、スキーマ化されたタグを見ていきます。

Tags (without a schema) are widely used as metadata labels or keywords to enhance the discoverability, organization, and management of data and AI assets. 
タグ（スキーマなし）は、データおよびAI資産の発見性、組織化、管理を強化するためのメタデータラベルやキーワードとして広く使用されています。

Hopsworks calls them _keywords. You probably have experience using tags to search_ and filter for things on the internet. 
Hopsworksではこれをキーワードと呼びます。おそらく、インターネット上で物を検索したりフィルタリングしたりするためにタグを使用した経験があるでしょう。

For example, I have tagged LinkedIn posts with #featurestoresummit. 
例えば、私はLinkedInの投稿に#featurestoresummitというタグを付けました。

Some systems only support exact tag matches when searching, while others support free-text search, in which a partial match on a tag returns relevant results. 
一部のシステムは検索時に正確なタグの一致のみをサポートし、他のシステムは部分一致のタグに対して関連する結果を返す自由形式の検索をサポートしています。

Many data catalog platforms, such as the Apache Ranger and Apache Atlas projects, support tags for organizing and searching for data assets. 
Apache RangerやApache Atlasプロジェクトなど、多くのデータカタログプラットフォームは、データ資産を整理し検索するためのタグをサポートしています。

Hopsworks supports both schematized tags and keywords for AI assets. 
HopsworksはAI資産のためにスキーマ化されたタグとキーワードの両方をサポートしています。

A schematized tag conforms to a predefined schema. 
スキーマ化されたタグは、事前に定義されたスキーマに準拠しています。

Just like the schema for a table or feature group, a schematized tag has expected fields and possibly a hierarchy or controlled vocabulary. 
テーブルやフィーチャーグループのスキーマと同様に、スキーマ化されたタグには期待されるフィールドがあり、階層や制御された語彙がある可能性があります。

Unlike free-form tags, schematized tags provide standardization, enabling consistent tagging across assets and supporting richer use cases like governance, automation, and advanced search. 
自由形式のタグとは異なり、スキーマ化されたタグは標準化を提供し、資産全体で一貫したタグ付けを可能にし、ガバナンス、オートメーション、先進的な検索などのより豊かなユースケースをサポートします。

For example, I used an LLM to help design the schematized tag in Table 13-1 that helps ensure AI assets are not in breach of the EU AI Act. 
例えば、私はLLMを使用して、AI資産がEU AI法に違反しないことを確保するためのスキーマ化されたタグをTable 13-1で設計しました。

All of the rows are required. 
すべての行は必須です。

LLMs have good knowledge of the EU AI Act and can help you get started with a schema and find errors in a schema. 
LLMはEU AI法についての知識が豊富で、スキーマの作成を始めたり、スキーマ内のエラーを見つけたりするのに役立ちます。

_Table 13-1. A schematized tag describing requirements for the EU AI Act_
_Table 13-1. EU AI法の要件を説明するスキーマ化されたタグ_

**Field** **Type** **Description**
**フィールド** **タイプ** **説明**

`risk_level` enum Minimal, limited, high, and unacceptable
`risk_level` enum 最小、制限、高、受け入れられない

`conformity_passed_date` date Date when latest conformity check passed (NULL if not conformant)
`conformity_passed_date` date 最新の適合チェックが合格した日付（適合していない場合はNULL）

`notified_body` string ID of the EU-notified conformity body
`notified_body` string EU通知適合機関のID

`technical_documentation_url` string Required under the act
`technical_documentation_url` string 法律に基づいて必要

`data_governance_validated_by` string ID of person who ensured dataset quality and representativeness
`data_governance_validated_by` string データセットの品質と代表性を確保した人のID

`explainability_documentation` string Required transparency obligation
`explainability_documentation` string 必要な透明性義務

`human_oversight` string For example, enabled or manual_review_required
`human_oversight` string 例えば、有効または手動レビューが必要

`bias_testing_results` string URL for bias and discrimination tests
`bias_testing_results` string バイアスおよび差別テストのURL

`provider` string Organization responsible for the asset
`provider` string 資産に対する責任を持つ組織

`intended_use` string Required under Annex III of the act
`intended_use` string 法律の附則IIIに基づいて必要

A schematized tag is often part of a taxonomy or ontology and typically has:
スキーマ化されたタグは、しばしば分類法やオントロジーの一部であり、通常は次のような特徴があります：

- A defined structure (like key-value pairs)
- 定義された構造（キーと値のペアのような）

- Controlled values or types
- 制御された値またはタイプ

- Validation rules
- 検証ルール

In Hopsworks, you can define a schematized tag in the UI or by using JSON. 
Hopsworksでは、UIまたはJSONを使用してスキーマ化されたタグを定義できます。

JSON supports both types and constraints on valid values. 
JSONは、型と有効な値に対する制約の両方をサポートしています。

I asked my LLM to translate Table 13-1 into a Hopsworks schematized tag, and it managed that, including correctly specifying the required key-value pairs. 
私はLLMにTable 13-1をHopsworksのスキーマ化されたタグに翻訳するように依頼し、必要なキーと値のペアを正しく指定することを含めてそれを実現しました。

In Hopsworks, a key-value pair is optional, unless you specify it explicitly as “required.” 
Hopsworksでは、キーと値のペアはオプションですが、「必須」と明示的に指定しない限りはそうです。

This is an abbreviated version of the JSON the LLM returned: 
これはLLMが返したJSONの省略版です：

```  
{  
  "type": "object",  
  "properties": {  
    "risk_level": {  
      "type": "string",  
      "enum": ["minimal", "limited", "high", "unacceptable"]  
    },  
    "conformity_passed_date": {  
      "type": "string",  
      "format": "date"  
    },  
    ...
    "intended_use": {  
      "type": "string"  
    }  
  },  
  "required": [  
    "risk_level",  
    ...  
  ]  
}
```  

You can attach an instance of this schematized tag to an AI asset. 
このスキーマ化されたタグのインスタンスをAI資産に添付できます。

Here is an example of one such schematized tag attached to a model: 
以下は、モデルに添付されたそのようなスキーマ化されたタグの例です：

```  
eu_ai_act_tag = {  
  "risk_level": "high",  
  "conformity_passed_date": "2025-03-15",  
  ...  
  "intended_use": "Credit card fraud scoring"  
}  
my_model.add_tag("eu_ai_act", eu_ai_act_tag)  
```  

In Hopsworks, you can now free-text search for my_model using any of the tag values, the model name, or the model description. 
Hopsworksでは、タグの値、モデル名、またはモデルの説明を使用してmy_modelを自由形式で検索できます。

AI assets can also have multiple tags associated with them. 
AI資産には、複数のタグを関連付けることもできます。

Schematized tags enable you to implement organization-wide standards for categorizing and describing ML assets. 
スキーマ化されたタグは、ML資産を分類し記述するための組織全体の標準を実装することを可能にします。

Each entry in the schema has:
スキーマ内の各エントリには次のものがあります：

- A name
- 名前

- A type (string, boolean, list, etc.)
- タイプ（文字列、ブール値、リストなど）

- A flag indicating whether the entry is required or optional
- エントリが必須かオプションかを示すフラグ

- An optional range of valid values (a validation constraint in the JSON schema)
- 有効な値のオプションの範囲（JSONスキーマ内の検証制約）

When users attach tags to an artifact, the tag values will be validated against the tag schema. 
ユーザーがアーティファクトにタグを添付すると、タグの値はタグスキーマに対して検証されます。

This ensures tags are consistent, no matter the project or the team generating them. 
これにより、プロジェクトや生成するチームに関係なく、タグが一貫性を持つことが保証されます。

You can also prevent the creation of AI assets if a specific schematized tag is not attached to it. 
特定のスキーマ化されたタグが添付されていない場合、AI資産の作成を防ぐこともできます。

For example, you could specify that models cannot be created in the production model registry if the EU AI Act tag is not filled in correctly for the model. 
例えば、モデルに対してEU AI法のタグが正しく記入されていない場合、本番モデルレジストリにモデルを作成できないように指定することができます。

You can attach tags to feature groups, feature views, or models in Hopsworks. 
Hopsworksでは、フィーチャーグループ、フィーチャービュー、またはモデルにタグを添付できます。

Some other useful examples of schematized tags for governance are:
ガバナンスのためのスキーマ化されたタグの他の有用な例には次のようなものがあります：

- A GDPR schema that includes a data retention date for training data or feature data and a governance tool that searches for AI assets that will soon need to be deleted due to the data retention period expiring.
- トレーニングデータまたはフィーチャーデータのデータ保持日を含むGDPRスキーマと、データ保持期間が満了するためにすぐに削除する必要があるAI資産を検索するガバナンツール。

- A compliance schema that defines the conditions under which an ML asset can be used for a particular task. 
- 特定のタスクに対してML資産を使用できる条件を定義するコンプライアンススキーマ。

For example, it can define whether a feature group can be used in a particular geographic region or not or whether it contains PII data. 
例えば、フィーチャーグループが特定の地理的地域で使用できるかどうか、またはPIIデータを含むかどうかを定義できます。

- A checklist schema that defines tasks that must be completed before a feature group is approved for production. 
- フィーチャーグループが本番用に承認される前に完了しなければならないタスクを定義するチェックリストスキーマ。

Who is the owner? 
所有者は誰ですか？

Who is consuming the output of this pipeline, and what problem does it solve? 
このパイプラインの出力を消費しているのは誰で、どのような問題を解決しますか？

What is the potential harm if this feature group is not updated in time (and breaks its SLA)? 
このフィーチャーグループが適時に更新されない場合の潜在的な害（およびSLAを破ること）は何ですか？

###### Lineage
###### 系譜

How can you find out which models use features from a PII-tagged feature group when the model itself does not have a PII tag? 
モデル自体にPIIタグがない場合、どのようにしてPIIタグ付きフィーチャーグループの特徴を使用しているモデルを見つけることができますか？

How can you see whether a feature group can be safely deleted because it is not used by any models or deployments? 
フィーチャーグループがどのモデルやデプロイメントにも使用されていないため、安全に削除できるかどうかをどのように確認できますか？

Say you have a production model that users are flagging for bias. 
ユーザーがバイアスを指摘している本番モデルがあるとします。

How can you find out which feature groups are used by the model (remember, bias comes from data, not from the ML algorithms)? 
モデルによって使用されているフィーチャーグループをどのようにして見つけることができますか（バイアスはデータから生じることを忘れないでください、MLアルゴリズムからではありません）？

The answer to these questions is lineage. 
これらの質問への答えは系譜です。

Lineage (or provenance) in AI systems tracks the origin, transformations, movement, and historical connections of data and models throughout their lifecycle. 
AIシステムにおける系譜（または起源）は、データとモデルの起源、変換、移動、および歴史的な接続をそのライフサイクル全体にわたって追跡します。

Hopsworks builds a lineage graph from data sources to deployments:
Hopsworksはデータソースからデプロイメントまでの系譜グラフを構築します：



Data Source → Feature Group → Feature View → Training Data → Model → Deployment
データソース → フィーチャーグループ → フィーチャービュー → トレーニングデータ → モデル → デプロイメント

Hopsworks provides graph APIs to query the provenance of AI assets, such as what models use this feature group or what feature groups are used in this feature view.
Hopsworksは、AI資産の出所を照会するためのグラフAPIを提供しており、どのモデルがこのフィーチャーグループを使用しているか、またはこのフィーチャービューでどのフィーチャーグループが使用されているかを確認できます。

The following edges are defined in Hopsworks’ provenance graph, traversing down from the data source(s) to model deployments:
以下のエッジは、データソースからモデルデプロイメントに向かって下方向に移動するHopsworksの出所グラフで定義されています。

- Data source → external feature groups
- データソース → 外部フィーチャーグループ

- Feature group → derived feature groups
- フィーチャーグループ → 派生フィーチャーグループ

- Feature group → feature views
- フィーチャーグループ → フィーチャービュー

- Feature view → training datasets
- フィーチャービュー → トレーニングデータセット

- Training dataset → models
- トレーニングデータセット → モデル

- Model → deployment
- モデル → デプロイメント

The following edges are defined in the provenance graph, traversing up from model deployments back to the data source(s):
以下のエッジは、モデルデプロイメントからデータソースに向かって上方向に移動する出所グラフで定義されています。

- Deployment → model
- デプロイメント → モデル

- Model → training dataset
- モデル → トレーニングデータセット

- Model → feature view (skip a layer)
- モデル → フィーチャービュー（1層スキップ）

- Training dataset → feature view
- トレーニングデータセット → フィーチャービュー

- Feature view → feature groups
- フィーチャービュー → フィーチャーグループ

- Feature group → source feature groups
- フィーチャーグループ → ソースフィーチャーグループ

- External feature group → data source
- 外部フィーチャーグループ → データソース

With provenance APIs and tags, you can build custom governance checks. 
出所APIとタグを使用することで、カスタムガバナンスチェックを構築できます。

For example, you can check whether a model’s usage scope is consistent with its feature groups’ usage scope.
例えば、モデルの使用範囲がそのフィーチャーグループの使用範囲と一致しているかどうかを確認できます。

In combination, tags and provenance APIs enable you to write and schedule governance enforcement jobs for your organization.
タグと出所APIを組み合わせることで、組織のためのガバナンス強制ジョブを作成し、スケジュールすることができます。

###### Versioning
###### バージョニング

Versioning of AI assets is important in governance to track the usage of AI assets over time.
AI資産のバージョニングは、ガバナンスにおいてAI資産の使用状況を時間の経過とともに追跡するために重要です。

Table 13-2 shows the support for versioning of the AI assets in Hopsworks introduced in the book.
表13-2は、本書で紹介されたHopsworksにおけるAI資産のバージョニングのサポートを示しています。

-----
_Table 13-2. Versioning overview for AI assets in Hopsworks_
表13-2. HopsworksにおけるAI資産のバージョニング概要

**AI asset** **Versioned?** **Upgrade considerations**
**AI資産** **バージョン管理されているか？** **アップグレードの考慮事項**

Feature group Yes Mutable with data versioning for lakehouse tables. New version needed for changed/removed features.
フィーチャーグループ はい データバージョニングが可能なレイクハウステーブルに対して可変です。変更または削除されたフィーチャーには新しいバージョンが必要です。

New versions of feature groups need to be backfilled.
フィーチャーグループの新しいバージョンは、バックフィルが必要です。

Feature view Yes Immutable. Cheap to create.
フィーチャービュー はい 不変です。作成コストは安いです。

New version needed for new/changed/removed features.
新しい/変更された/削除されたフィーチャーには新しいバージョンが必要です。

Training data Yes Immutable. Can be expensive to create.
トレーニングデータ はい 不変です。作成コストが高くなる可能性があります。

New version needed for new/changed/removed features.
新しい/変更された/削除されたフィーチャーには新しいバージョンが必要です。

Model Yes Immutable. New version created after each successful training run.
モデル はい 不変です。各成功したトレーニング実行後に新しいバージョンが作成されます。

Deployment No Mutable. Blue/green and A/B testing for a new model version. Semantic versioning—new name for new deployment. Clients depend on the Deployment API.
デプロイメント いいえ 可変です。新しいモデルバージョンのためのブルー/グリーンおよびA/Bテスト。セマンティックバージョニング—新しいデプロイメントのための新しい名前。クライアントはデプロイメントAPIに依存します。

Training datasets are immutable in Hopsworks to enable reproducibility.
トレーニングデータセットは、再現性を確保するためにHopsworksでは不変です。

However, as training datasets grow in size, they could be considered materialized views, and they could grow as new data arrives in feature groups.
しかし、トレーニングデータセットが大きくなるにつれて、マテリアライズドビューと見なされる可能性があり、フィーチャーグループに新しいデータが到着するにつれて成長する可能性があります。

But then they would also need to support time-travel for reproducibility.
しかし、その場合、再現性のためにタイムトラベルをサポートする必要があります。

In Chapter 3, our air quality model used pm25 as a measure of air quality.
第3章では、私たちの空気質モデルはpm25を空気質の指標として使用しました。

What if you want to update your air quality model to also predict `pm10? 
もしあなたが空気質モデルを更新して`pm10`も予測したい場合はどうしますか？

For this, you will also need to update the air quality feature group and the feature view (see also Figure 5-7).
そのためには、空気質フィーチャーグループとフィーチャービューも更新する必要があります（図5-7も参照）。

The code for adding the pm10 column could look as follows: 
pm10列を追加するためのコードは次のようになります：

```   
features = [ Feature(name="pm10",type="float") ]   
fg = fs.get_or_create_feature_group("airquality", version=1)   
fg.append_features(features)
```

We do not have to upgrade the fg version, as we are not making a schema-breaking change.
スキーマを破る変更を行っていないため、fgバージョンをアップグレードする必要はありません。

However, if we follow this approach, all existing rows will have a default value of “0.0” for pm10, and when we create training data, we will need to know how to filter out training data only created after the date when the new pm10 column was added.
しかし、このアプローチに従うと、すべての既存の行はpm10のデフォルト値として「0.0」を持ち、新しいpm10列が追加された日以降に作成されたトレーニングデータをフィルタリングする方法を知る必要があります。

Instead, we can just add a new version for airquality: 
代わりに、空気質の新しいバージョンを追加することができます：

```   
airquality_fg = fs.create_feature_group("airquality", version=2)
```

We can now backfill version 2 of airquality with historical weather data.
これで、空気質のバージョン2を過去の気象データでバックフィルできます。

We want to train a new model to predict pm10, and for this we will require a new version of our feature view: 
pm10を予測する新しいモデルをトレーニングしたいので、そのためにはフィーチャービューの新しいバージョンが必要です：

```   
selected_features = airquality_fg.select(["pm10"]).join(weather_fg.select_all())   
fv = fs.create_feature_view("aq_fv", version=2,       
       query=selected_features,       
       labels=["pm10"]   
)
```

Versioning models is more straightforward than versioning feature groups, as models are immutable while feature groups store mutable data.
モデルのバージョニングはフィーチャーグループのバージョニングよりも簡単です。モデルは不変であり、フィーチャーグループは可変データを保存します。

-----
_Schema-breaking changes require a new version of a feature group_ or feature view.
スキーマを破る変更には、フィーチャーグループまたはフィーチャービューの新しいバージョンが必要です。

Examples of schema-breaking changes are changing how a feature is computed (you should not mix the old feature data with the new feature data in the same feature group version), deleting a feature, and changing a feature type.
スキーマを破る変更の例には、フィーチャーの計算方法を変更すること（同じフィーチャーグループバージョン内で古いフィーチャーデータと新しいフィーチャーデータを混合してはいけません）、フィーチャーを削除すること、フィーチャータイプを変更することが含まれます。

Finally, there is support for data versioning in one lakehouse table, Apache Iceberg.
最後に、1つのレイクハウステーブルでのデータバージョニングのサポートがあります。Apache Icebergです。

If offline feature groups become very large (PBs or larger), storing copies of the data becomes increasingly impractical.
オフラインフィーチャーグループが非常に大きくなる（PB以上）と、データのコピーを保存することがますます非現実的になります。

With Iceberg tables, you can create a branch of production tables to test new features or algorithms on a subset of data without interfering with the production table.
Icebergテーブルを使用すると、プロダクションテーブルに干渉することなく、データのサブセットで新しいフィーチャーやアルゴリズムをテストするためのプロダクションテーブルのブランチを作成できます。

If the new features are a success, you can merge your branch back to main.
新しいフィーチャーが成功した場合、ブランチをメインにマージできます。

If they aren’t a success, the branch can be discarded with no impact.
成功しなかった場合、ブランチは影響を与えずに破棄できます。

Iceberg also allows you to create tags for branches.
Icebergは、ブランチにタグを作成することも可能です。

```   
# Create a branch   
spark.sql(    
    "ALTER TABLE local.default.sample_table CREATE BRANCH IF NOT EXISTS dev_branch"   
)   

# Make changes in the dev_branch   
spark.sql("INSERT INTO local.default.sample_table.branch_dev_branch \         
         VALUES (3, 'Charlie', 35)")   

# Create a tag for the main branch   
spark.sql("ALTER TABLE local.default.sample_table \         
         CREATE TAG IF NOT EXISTS v1_0")   

# Query the original table   
spark.sql("SELECT * FROM local.default.sample_table").show()   

# Query the dev_branch   
spark.sql("SELECT * FROM local.default.sample_table.branch_dev_branch").show()   

# Query using the tag   
spark.sql("SELECT * FROM local.default.sample_table.tag_v1_0").show()
```

###### Audit Logs
###### 監査ログ

``` 
Hopsworks capabilities are exposed via a REST API, and it stores an audit log of who executed what action at what time.
Hopsworksの機能はREST APIを介して公開されており、誰が何のアクションをいつ実行したかの監査ログを保存します。

For governance in an AI system, audit logs should provide a complete, tamperproof record of key events across the AI lifecycle.
AIシステムにおけるガバナンスのために、監査ログはAIライフサイクル全体の重要なイベントの完全で改ざん不可能な記録を提供する必要があります。

This includes:
これには以下が含まれます：

- Feature store events when feature groups are created, modified, accessed, or deleted
- フィーチャーストアイベント（フィーチャーグループが作成、変更、アクセス、または削除されたとき）

- Model lifecycle events, such as registrations, deployments, and updates
- モデルライフサイクルイベント（登録、デプロイメント、更新など）

-----
- Access control events, such as who updated an ML asset or approved a production deployment
- アクセス制御イベント（誰がML資産を更新したか、またはプロダクションデプロイメントを承認したか）

- Model deployment activity, such as who sent a given prediction request
- モデルデプロイメント活動（誰が特定の予測リクエストを送信したか）

There are also developer-created audits that are often needed, such as model validation reports, including results of bias testing.
モデル検証レポートなど、開発者が作成した監査もよく必要とされます。これにはバイアステストの結果が含まれます。

Model cards form an important part of the audit trail for models.
モデルカードは、モデルの監査トレイルの重要な部分を形成します。

Dashboards auditing platform usage are also important for stakeholders.
プラットフォームの使用状況を監査するダッシュボードも、利害関係者にとって重要です。

These include dashboards that show ML asset activity, including model request traffic patterns, and feature usage charts showing feature usage in different models.
これには、モデルリクエストのトラフィックパターンを含むML資産の活動を示すダッシュボードや、異なるモデルにおけるフィーチャー使用状況を示すフィーチャー使用チャートが含まれます。

###### Summary and Exercises
###### まとめと演習

In this chapter, we looked at offline testing as part of MLOps.
この章では、MLOpsの一環としてオフラインテストを見てきました。

We described an approach to moving from development to production with FTI pipelines using version control, CI/CD, and test/staging/development infrastructure (feature store, model registry, and model serving).
バージョン管理、CI/CD、およびテスト/ステージング/開発インフラストラクチャ（フィーチャーストア、モデルレジストリ、モデルサービング）を使用して、開発からプロダクションへの移行アプローチを説明しました。

We looked at the diverse set of offline tests you can write to validate changes in AI systems.
AIシステムの変更を検証するために書くことができる多様なオフラインテストのセットを見てきました。

We also introduced blue/green testing as a method for evaluating model deployments before they are rolled out to production.
また、モデルデプロイメントをプロダクションに展開する前に評価する方法として、ブルー/グリーンテストを紹介しました。

Then, we looked at how to design your own governance rules, how to enforce them, and how lineage and versioning are crucial to safely debugging and upgrading your AI systems, respectively.
次に、自分自身のガバナンスルールを設計する方法、それを強制する方法、そして系譜とバージョニングがそれぞれAIシステムの安全なデバッグとアップグレードにどれほど重要であるかを見てきました。

We concluded by explaining how you can evaluate the performance of changes to your LLM inference using evals.
最後に、evalsを使用してLLM推論の変更のパフォーマンスを評価する方法を説明しました。

The following exercises will help you learn how to govern your AI assets programmatically:
以下の演習は、AI資産をプログラム的に管理する方法を学ぶのに役立ちます：

- Write a program that takes a tag value and a feature group as a parameter and returns the list of deployments that use that feature group. Assume the tag is “PII”—find the deployments using the PII features.
- タグ値とフィーチャーグループをパラメータとして受け取り、そのフィーチャーグループを使用するデプロイメントのリストを返すプログラムを書いてください。タグは「PII」と仮定し、PIIフィーチャーを使用するデプロイメントを見つけてください。

- Design a schematized tag for Know Your Customer (KYC) feature data that is typically found in a bank. Leverage an LLM if you don’t know what KYC data is—the LLM knows.
- 銀行に通常見られるKnow Your Customer（KYC）フィーチャーデータのためのスキーマ化されたタグを設計してください。KYCデータが何か分からない場合はLLMを活用してください—LLMは知っています。

-----
-----

