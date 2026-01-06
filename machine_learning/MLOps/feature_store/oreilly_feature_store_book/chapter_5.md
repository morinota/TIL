## CHAPTER 5: Hopsworks Feature Store 第5章: Hopsworksフィーチャーストア

In this chapter, we will look in depth at the Hopsworks feature store. 
この章では、Hopsworksフィーチャーストアについて詳しく見ていきます。

Hopsworks is a platform for the development and operation of batch, real-time, and LLM AI systems at scale. 
Hopsworksは、バッチ、リアルタイム、およびLLM AIシステムの開発と運用のためのプラットフォームです。

It can be installed on as little as one server or as many as hundreds of servers. 
1台のサーバーから数百台のサーバーまでインストールできます。

Hopsworks includes a feature store as well as a complete MLOps and compute platform, but we will focus on the feature store in this chapter. 
Hopsworksにはフィーチャーストアと完全なMLOpsおよびコンピュートプラットフォームが含まれていますが、この章ではフィーチャーストアに焦点を当てます。

We will show how to implement the data model for our credit card fraud model from Chapter 4 in Hopsworks. 
第4章のクレジットカード詐欺モデルのデータモデルをHopsworksで実装する方法を示します。

We will also see how the feature store concepts from the previous chapter are represented in Hopsworks using code snippets in Python. 
前の章のフィーチャーストアの概念が、Pythonのコードスニペットを使用してHopsworksでどのように表現されるかも見ていきます。

We will start with projects in Hopsworks—a secure, collaborative space for storing your feature data, training data, and models. 
Hopsworksのプロジェクトから始めます。これは、フィーチャーデータ、トレーニングデータ、およびモデルを保存するための安全で共同作業ができるスペースです。

###### Hopsworks Projects Hopsworksプロジェクト

A Hopsworks cluster is organized into projects, where each project has a unique name. 
Hopsworksクラスターはプロジェクトに整理されており、各プロジェクトにはユニークな名前があります。

Hopsworks projects are secure spaces for teams to collaborate and manage data and models for AI. 
Hopsworksプロジェクトは、チームがAIのデータとモデルを共同で管理するための安全なスペースです。

Similar to a repository in GitHub, a project has team members (with role-based access control), but instead of storing source code, Hopsworks projects store data for AI. 
GitHubのリポジトリに似て、プロジェクトにはチームメンバー（役割ベースのアクセス制御付き）がいますが、ソースコードを保存する代わりに、HopsworksプロジェクトはAIのデータを保存します。

Each project has its own feature store, a model registry, model deployments, and datasets for general-purpose file storage. 
各プロジェクトには独自のフィーチャーストア、モデルレジストリ、モデルデプロイメント、および一般的なファイルストレージ用のデータセットがあります。

The following code snippet shows how to get a reference to a project object when you log in to Hopsworks. 
以下のコードスニペットは、Hopsworksにログインしたときにプロジェクトオブジェクトへの参照を取得する方法を示しています。

If you do not enter the name of the project, Hopsworks will return a reference to your main project (the project you created when you registered your account on hopsworks.ai). 
プロジェクトの名前を入力しない場合、Hopsworksはメインプロジェクト（hopsworks.aiでアカウントを登録したときに作成したプロジェクト）への参照を返します。

With your project, you can get a reference to its feature store as follows: 
プロジェクトを使用して、次のようにフィーチャーストアへの参照を取得できます。

```  
import hopsworks   
project = hopsworks.login()   
fs = project.get_feature_store()
```

The hopsworks.login() method also has parameters for the hostname (or IP) and port of the Hopsworks cluster, as well as the API key (either as a value or a file containing the API key). 
hopsworks.login()メソッドには、Hopsworksクラスターのホスト名（またはIP）とポート、およびAPIキー（値またはAPIキーを含むファイルのいずれか）のパラメータもあります。

In this book, we will use serverless Hopsworks, which has a hostname of _c.app.hopsworks.ai and a port of 443. 
この本では、ホスト名が_c.app.hopsworks.aiでポートが443のサーバーレスHopsworksを使用します。

In this book, we call hopsworks.login() without parameters, instead setting `HOPSWORKS_API_KEY` as an environment variable in your program. 
この本では、パラメータなしでhopsworks.login()を呼び出し、代わりにプログラム内で`HOPSWORKS_API_KEY`を環境変数として設定します。

If you are not using Hopsworks serverless, you will also need to set `HOPSWORKS_HOST` and `HOPSWORKS_PROJECT` environment variables—set them in an .env file in the root directory of the book’s source code repository. 
Hopsworksサーバーレスを使用していない場合は、`HOPSWORKS_HOST`と`HOPSWORKS_PROJECT`環境変数も設定する必要があります。これらは、本のソースコードリポジトリのルートディレクトリにある.envファイルに設定します。

###### Storing Files in a Project プロジェクト内のファイルの保存

Every project in Hopsworks has directories where you can store data. 
Hopsworksのすべてのプロジェクトには、データを保存できるディレクトリがあります。

From the UI or the Datasets API, you can upload and download files. 
UIまたはDatasets APIから、ファイルをアップロードおよびダウンロードできます。

For example, from the book’s GitHub repo, you can upload the titanic.csv file to a directory called Resources in your project as follows: 
たとえば、本のGitHubリポジトリから、次のようにtitanic.csvファイルをプロジェクト内のResourcesというディレクトリにアップロードできます。

```  
dataset_api = project.get_dataset_api()   
path = dataset_api.upload("data/titanic.csv", "Resources", overwrite=True)
```

Setting overwrite=True makes the upload operation idempotent. 
overwrite=Trueを設定すると、アップロード操作が冪等になります。

You can download a file from Hopsworks by using its path (right-click on the file in the file explorer UI in Hopsworks to get its path): 
Hopsworksからファイルをダウンロードするには、そのパスを使用します（HopsworksのファイルエクスプローラーUIでファイルを右クリックしてパスを取得します）。

```  
dataset_api.download(uploaded_path, overwrite=True)
```

If you navigate to Project Settings → File Browser, you will see the directories listed in Table 5-1 in your project. 
プロジェクト設定 → ファイルブラウザに移動すると、プロジェクト内の表5-1にリストされたディレクトリが表示されます。

_Table 5-1. The names and descriptions of the directories in your Hopsworks project, where <proj> is the name of the project_  
**表5-1. Hopsworksプロジェクト内のディレクトリの名前と説明（<proj>はプロジェクトの名前です）**

**Directory** **Description**  
**ディレクトリ** **説明**  
_Airflow/_ It stores Airflow Python programs for this project (DAG files).  
_Airflow/_ このディレクトリには、このプロジェクトのAirflow Pythonプログラム（DAGファイル）が保存されます。  
This directory is not used in this book.  
このディレクトリはこの本では使用されません。

_Brewer/_ It stores conversation histories and artifacts created with Hopsworks’ LLM assistant, Brewer.  
_Brewer/_ HopsworksのLLMアシスタントBrewerで作成された会話履歴とアーティファクトが保存されます。

_DataValidation/_ When expectations are attached to a feature group, every insertion/deletion creates a validation report that is stored in the <feature_group_name>/<version> subdirectory as a JSON file.  
_DataValidation/_ 期待値がフィーチャーグループに付随する場合、すべての挿入/削除は、<feature_group_name>/<version>サブディレクトリにJSONファイルとして保存される検証レポートを作成します。

_<proj>_featurestore.db/_ This is the offline feature store directory containing the feature store lakehouse table files.  
_<proj>_featurestore.db/_ これは、フィーチャーストアのレイクハウステーブルファイルを含むオフラインフィーチャーストアディレクトリです。

_<proj>_Training_Datasets/ When you save training data as files, by default, they are saved here in the <training_dataset_name>/<version> subdirectory (as Parquet or CSV files).  
_<proj>_Training_Datasets/ トレーニングデータをファイルとして保存すると、デフォルトでは、<training_dataset_name>/<version>サブディレクトリに保存されます（ParquetまたはCSVファイルとして）。

_Jupyter/_ You’ll store Jupyter notebooks run on Hopsworks in here.  
_Jupyter/_ Hopsworksで実行されるJupyterノートブックをここに保存します。  
Typically, you’ll check out Git repositories in this directory.  
通常、このディレクトリでGitリポジトリをチェックアウトします。  
This directory is not used in this book.  
このディレクトリはこの本では使用されません。

_Logs/_ For (Python, Spark, Flink) jobs run in Hopsworks, their output is stored here in a subdirectory:  
_Logs/_ Hopsworksで実行される（Python、Spark、Flink）ジョブの出力は、ここにサブディレクトリに保存されます：  
_[Spark/Python/Flink]/job_name/execution_id. This directory is not used in this book._  
_[Spark/Python/Flink]/job_name/execution_id。このディレクトリはこの本では使用されません。_

_Models/_ Models saved in the Hopsworks model registry are stored in the <model_name>/<version> subdirectory, along with its artifacts.  
_Models/_ Hopsworksモデルレジストリに保存されたモデルは、<model_name>/<version>サブディレクトリに、そのアーティファクトと共に保存されます。

-----
**Directory** **Description**  
**ディレクトリ** **説明**  
_Resources/_ A general-purpose directory for files used in your project.  
_Resources/_ プロジェクトで使用されるファイルのための一般的なディレクトリです。  
_Statistics/_ Statistics computed for feature groups and training datasets are stored in a subdirectory that follows the naming convention <name>_<version>.  
_Statistics/_ フィーチャーグループとトレーニングデータセットのために計算された統計は、<name>_<version>という命名規則に従ったサブディレクトリに保存されます。  

Two of the directories in your project store programs (Jupyter notebooks, Airflow DAGs). 
プロジェクト内の2つのディレクトリはプログラム（Jupyterノートブック、Airflow DAG）を保存します。

We will not use these directories in this book, however, as we will work with serverless Hopsworks—we will run our programs outside of Hopsworks. 
ただし、この本ではこれらのディレクトリを使用しません。サーバーレスHopsworksで作業するため、プログラムはHopsworksの外部で実行します。

If, instead, you have your own Hopsworks cluster, you can use Hopsworks’ Git/Bitbucket support to clone the book’s source code to the Jupyter directory and run Jupyter notebooks and jobs from within Hopsworks. 
代わりに、自分のHopsworksクラスターを持っている場合は、HopsworksのGit/Bitbucketサポートを使用して、本のソースコードをJupyterディレクトリにクローンし、Hopsworks内でJupyterノートブックやジョブを実行できます。

###### Access Control Within Projects プロジェクト内のアクセス制御

Projects support role-based access control (RBAC) inside the project. 
プロジェクトは、プロジェクト内での役割ベースのアクセス制御（RBAC）をサポートしています。

Each active project member has one of two possible roles: the data owner role that has administrator privileges within a project or the data scientist role that is a read-only role for the feature store but can create training data and train models. 
各アクティブなプロジェクトメンバーは、プロジェクト内で管理者権限を持つデータオーナーの役割またはフィーチャーストアに対して読み取り専用の役割を持ち、トレーニングデータを作成しモデルをトレーニングできるデータサイエンティストの役割のいずれかを持っています。

The privileges for the two roles are shown in Table 5-2. 
2つの役割の特権は表5-2に示されています。

_Table 5-2. Privileges of the two roles for operations on Hopsworks services_  
**表5-2. Hopsworksサービスにおける2つの役割の操作に関する特権**  
**Data owner** **Data scientist**  
**データオーナー** **データサイエンティスト**  
Project membership Add/remove/update  
プロジェクトメンバーシップ 追加/削除/更新  

Feature store Read/write/update Read  
フィーチャーストア 読み取り/書き込み/更新 読み取り  

Model registry Add/remove Add/remove  
モデルレジストリ 追加/削除 追加/削除  

Model deployments Create/start/stop  
モデルデプロイメント 作成/開始/停止  

Project directories Read/write/delete Read/write/delete all except read-only for <proj>_featurestore.db/  
プロジェクトディレクトリ 読み取り/書き込み/削除 読み取り/書き込み/削除（<proj>_featurestore.db/は読み取り専用を除く）  

Data sharing across projects Yes No  
プロジェクト間のデータ共有 はい いいえ  



Model deployments Create/start/stop
モデルのデプロイメント 作成/開始/停止

Project directories Read/write/delete Read/write/delete all except read-only for <proj>_featurestore.db/
プロジェクトディレクトリ 読み取り/書き込み/削除 読み取り専用の<proj>_featurestore.db/を除くすべての読み取り/書き込み/削除

Data sharing across projects Yes No
プロジェクト間のデータ共有 はい いいえ

###### Access Control at the Cluster Level Using Projects
###### プロジェクトを使用したクラスターレベルのアクセス制御
We can also use projects to implement access control by placing users and data in different projects and selectively sharing access to data across project boundaries. 
私たちは、ユーザとデータを異なるプロジェクトに配置し、プロジェクトの境界を越えてデータへのアクセスを選択的に共有することで、アクセス制御を実装するためにプロジェクトを使用することもできます。
We will examine these capabilities through an example. 
これらの機能を例を通じて検討します。
In Figure 5-1, we can see how the five feature groups from Chapter 4 are organized inside a single project called `credit_card_transactions. 
図5-1では、Chapter 4の5つのフィーチャーグループが`credit_card_transactions`という単一のプロジェクト内にどのように整理されているかを見ることができます。
The project’s members are Denzel (the project owner, who is responsible for the feature pipelines and model deployment) and Jack and Tay (the data scientists, who train the models). 
プロジェクトのメンバーは、フィーチャーパイプラインとモデルデプロイメントを担当するプロジェクトオーナーのDenzelと、モデルをトレーニングするデータサイエンティストのJackとTayです。

-----
_Figure 5-1. This credit_card_transactions project has three members and five feature groups._
_Figure 5-1. このcredit_card_transactionsプロジェクトには3人のメンバーと5つのフィーチャーグループがあります。_

Hopsworks projects are a security boundary; they implement a multitenant security model, where each project is the tenant in the Hopsworks cluster. 
Hopsworksプロジェクトはセキュリティの境界であり、各プロジェクトがHopsworksクラスター内のテナントであるマルチテナントセキュリティモデルを実装しています。
As such, Hopsworks supports project-level multitenancy. 
そのため、Hopsworksはプロジェクトレベルのマルチテナンシーをサポートしています。
You can securely store data in a Hopsworks project on a shared cluster, and, by default, users who are not members of your project will not be able to access the resources in your project. 
共有クラスター上のHopsworksプロジェクトにデータを安全に保存でき、デフォルトでは、プロジェクトのメンバーでないユーザーはプロジェクト内のリソースにアクセスできません。
If you have your own Hopsworks cluster, all jobs you run follow dynamic RBAC. 
独自のHopsworksクラスターを持っている場合、実行するすべてのジョブは動的RBACに従います。
With standard RBAC, being a member of multiple projects would allow you to copy or move data between projects. 
標準のRBACでは、複数のプロジェクトのメンバーであることにより、プロジェクト間でデータをコピーまたは移動することができます。
Dynamic RBAC changes this: user jobs are always run within the context of a specific project and can only access resources inside that project. 
動的RBACはこれを変更します：ユーザージョブは常に特定のプロジェクトのコンテキスト内で実行され、そのプロジェクト内のリソースにのみアクセスできます。
Your job does not inherit all permissions from other projects. 
ジョブは他のプロジェクトからすべての権限を継承しません。
Instead, it runs only with the privileges you have in the project where the job is started. 
代わりに、ジョブが開始されたプロジェクトで持っている権限のみで実行されます。
If you switch to a different project and run a job there, it will have whatever privileges you have in that project. 
別のプロジェクトに切り替えてそこでジョブを実行すると、そのプロジェクトで持っている権限が適用されます。
Hopsworks implements dynamic RBAC by giving each user a unique project-specific identity for every project they belong to. 
Hopsworksは、各ユーザーに所属するすべてのプロジェクトに対してユニークなプロジェクト固有のアイデンティティを与えることで動的RBACを実装しています。
Actions you perform in a project use this project-specific identity, which means your permissions are limited to that project. 
プロジェクト内で実行するアクションはこのプロジェクト固有のアイデンティティを使用し、つまり、あなたの権限はそのプロジェクトに制限されます。

However, what happens if you want to share data from one project to another? 
しかし、あるプロジェクトから別のプロジェクトにデータを共有したい場合はどうなりますか？
Hopsworks supports secure sharing of data with other projects. 
Hopsworksは他のプロジェクトとのデータの安全な共有をサポートしています。
This enables us to refactor our project from Figure 5-1 into smaller projects that share feature groups with one another but have tighter access control on the data. 
これにより、図5-1のプロジェクトを、フィーチャーグループを互いに共有しながらもデータに対してより厳格なアクセス制御を持つ小さなプロジェクトにリファクタリングすることができます。
That is, you can implement the principle of least privilege (giving users the minimal set of privileges they need to get the job done, and no more) through a combination of putting sensitive data in its own project with restricted membership and then sharing that data selectively to only those projects that require access. 
つまり、制限されたメンバーシップを持つ独自のプロジェクトに機密データを配置し、そのデータをアクセスが必要なプロジェクトにのみ選択的に共有することで、最小権限の原則（ユーザーが仕事を完了するために必要な最小限の権限を与え、それ以上は与えない）を実装できます。

In Figure 5-2, we reorganized the feature groups from Figure 5-1 to move `account_fg to a new know_your_customer project and to move the bank_fg and merchant_fg to a new commercial_banking project.`
図5-2では、図5-1のフィーチャーグループを再編成し、`account_fg`を新しい`know_your_customer`プロジェクトに移動し、`bank_fg`と`merchant_fg`を新しい`commercial_banking`プロジェクトに移動しました。

-----
_Figure 5-2. We refactored our project from Figure 5-1 to store our feature groups in three different projects. The new know_your_customer and commercial_banking projects share their feature groups (read-only) with the credit_card_transactions project. Members Jack, Tay, and Denzel of the credit_card_transactions project can now read feature data from all feature groups, but they can only write to the cc_trans_fg and cc_trans_aggs_fg feature groups._
_Figure 5-2. 私たちは図5-1からプロジェクトをリファクタリングし、フィーチャーグループを3つの異なるプロジェクトに保存しました。新しい`know_your_customer`および`commercial_banking`プロジェクトは、`credit_card_transactions`プロジェクトとフィーチャーグループ（読み取り専用）を共有します。`credit_card_transactions`プロジェクトのメンバーであるJack、Tay、Denzelは、すべてのフィーチャーグループからフィーチャーデータを読み取ることができますが、`cc_trans_fg`および`cc_trans_aggs_fg`フィーチャーグループにのみ書き込むことができます。_

Then, we share these feature groups in read-only form with the original `credit_card_transactions project, whose members now have the same read privileges to the data as earlier (when all feature groups were in a single project). 
次に、これらのフィーチャーグループを元の`credit_card_transactions`プロジェクトと読み取り専用の形で共有し、そのメンバーは以前と同じデータへの読み取り権限を持っています（すべてのフィーチャーグループが単一のプロジェクトにあったとき）。
However, the data owner Denzel has lost write privileges to `account_fg,` `bank_fg, and` `merchant_fg. 
しかし、データオーナーのDenzelは`account_fg`、`bank_fg`、および`merchant_fg`への書き込み権限を失いました。
This type of data organization is often known as a data mesh, where instead of a central data team (in one project) managing all data, data ownership is distributed across different business domains (projects). 
この種のデータ組織は、中央のデータチーム（1つのプロジェクト内）がすべてのデータを管理するのではなく、データ所有権が異なるビジネスドメイン（プロジェクト）に分散されるデータメッシュとして知られています。

The best practice for organizing data and users in projects is informed by whether you are doing development, testing in staging, or running in production. 
プロジェクト内でデータとユーザーを整理するためのベストプラクティスは、開発、ステージングでのテスト、または本番環境での実行を行っているかどうかによって異なります。
For less friction in development, you should give each team/developer their own development project (with all users having the data owner role). 
開発での摩擦を減らすために、各チーム/開発者に独自の開発プロジェクトを与えるべきです（すべてのユーザーがデータオーナーの役割を持つ）。
For staging and production, you should follow the principle of least privilege—give the minimal read/write/execution privileges to users such that they can accomplish their tasks. 
ステージングと本番環境では、最小権限の原則に従うべきです—ユーザーがタスクを達成できるように、最小限の読み取り/書き込み/実行権限を与えます。
One practice that I have often seen is to give read-only access to production data to development projects. 
私がよく見かける一つの実践は、開発プロジェクトに本番データへの読み取り専用アクセスを与えることです。
Sometimes this is necessitated by huge data volumes, but in general, this removes the need to metaphorically throw data over the wall to data scientists. 
時には、大量のデータボリュームによって必要とされることもありますが、一般的には、データサイエンティストにデータを比喩的に投げる必要がなくなります。

-----
###### Feature Groups
###### フィーチャーグループ
A feature group in Hopsworks is a table of features, where a feature pipeline updates its feature data and training/inference pipelines read its data via feature views. 
Hopsworksのフィーチャーグループは、フィーチャーのテーブルであり、フィーチャーパイプラインがそのフィーチャーデータを更新し、トレーニング/推論パイプラインがフィーチャービューを介してそのデータを読み取ります。
In Figure 5-3, we can see the offline, online, and vector index stores for feature group data in Hopsworks.
図5-3では、Hopsworksにおけるフィーチャーグループデータのオフライン、オンライン、およびベクトルインデックスストアを見ることができます。

_Figure 5-3. In Hopsworks, a feature pipeline writes to a feature group with the batch or stream API. Hopsworks ensures the consistency of feature data across online/offline stores and the vector index. You query/read feature data using a feature view (that may apply MDTs when reading data). Queries are mapped to one of the backends—the online store, offline store, or vector index._
_Figure 5-3. Hopsworksでは、フィーチャーパイプラインがバッチまたはストリームAPIを使用してフィーチャーグループに書き込みます。Hopsworksは、オンライン/オフラインストアおよびベクトルインデックス全体でフィーチャーデータの整合性を確保します。フィーチャービューを使用してフィーチャーデータをクエリ/読み取ります（データを読み取る際にMDTを適用する場合があります）。クエリは、オンラインストア、オフラインストア、またはベクトルインデックスのいずれかのバックエンドにマッピングされます。_

[Hopsworks’ online store is RonDB, an open source, distributed, highly available, real-time database, developed by Hopsworks and forked from the open source MySQL NDB (network database) Cluster. 
[HopsworksのオンラインストアはRonDBであり、オープンソースの分散型、高可用性のリアルタイムデータベースで、Hopsworksによって開発され、オープンソースのMySQL NDB（ネットワークデータベース）クラスターからフォークされています。
The offline store is a lakehouse table (Apache Hudi, Delta Lake, Apache Iceberg), stored either in an S3 compatible object store or Hopsworks’ native distributed filesystem, HopsFS. 
オフラインストアは、S3互換のオブジェクトストアまたはHopsworksのネイティブ分散ファイルシステムHopsFSに保存されるレイクハウステーブル（Apache Hudi、Delta Lake、Apache Iceberg）です。
It is also possible to create an external feature group where the offline store is an external data warehouse, such as Snowflake, BigQuery, or Redshift. 
オフラインストアがSnowflake、BigQuery、またはRedshiftなどの外部データウェアハウスである外部フィーチャーグループを作成することも可能です。
As such, the offline store can be a mix of external tables and Hopsworks managed lakehouse tables. 
そのため、オフラインストアは外部テーブルとHopsworksが管理するレイクハウステーブルの混合である可能性があります。
You can also store vector embeddings in a vector index for a feature group. 
フィーチャーグループのベクトルインデックスにベクトル埋め込みを保存することもできます。
Clients typically read data from feature groups using feature views. 
クライアントは通常、フィーチャービューを使用してフィーチャーグループからデータを読み取ります。
The feature view provides both offline and online APIs that query data from the offline and online stores, respectively. 
フィーチャービューは、オフラインストアとオンラインストアからそれぞれデータをクエリするオフラインおよびオンラインAPIの両方を提供します。
There is also a similarity search API for feature groups that store vector embeddings, and it enables you to find K rows 
フィーチャーグループにベクトル埋め込みを保存するための類似検索APIもあり、K行を見つけることができます。

-----
that contain embeddings that most closely match your client-provided vector embedding.
クライアントが提供したベクトル埋め込みに最も近い埋め込みを含む行を見つけることができます。
To create a feature group in Hopsworks, you first log in and get a feature store object for your project. 
Hopsworksでフィーチャーグループを作成するには、まずログインし、プロジェクトのフィーチャーストアオブジェクトを取得します。
Then you can use either `create_feature_group(), which returns an error if the feature group already exists, or `get_or_create_feature_group(), which is an idempotent operation that returns the feature group if it already exists. 
次に、`create_feature_group()`を使用することができ、フィーチャーグループが既に存在する場合はエラーを返します。または、`get_or_create_feature_group()`を使用することができ、これは冪等操作であり、フィーチャーグループが既に存在する場合はそのフィーチャーグループを返します。

The following code snippet shows example code for creating an online feature group with a vector embedding and some data validation rules. 
以下のコードスニペットは、ベクトル埋め込みといくつかのデータ検証ルールを持つオンラインフィーチャーグループを作成するための例コードを示しています。
```  
from hopsworks.hsfs import embedding   
fs = hopsworks.login().get_feature_store()   
df = # Read data into (Pandas/Polars/PySpark) DataFrame   
# Use the default Embedding Index   
emb = embedding.EmbeddingIndex()   
# Define the column that contains vector embeddings   
emb.add_embedding(df['col_with_embedding'])   
expectation_suite = … # Define Data Validation Rules for ingestion   
fg_cc_aggs = fs.create_feature_group(     
    name="cc_trans_aggs_fg",     
    version=1,     
    description="Aggregated credit card transaction features",     
    primary_key=['cc_num'],     
    partition_key=['date'],     
    event_time='datetime',     
    online_enabled=True,     
    time_travel_format='DELTA',     
    embedding_index=emb,     
    expectation_suite=expectation_suite,   
)   
fg_cc_aggs.insert(df)
```
フィーチャーグループには名前、バージョン、および主キーが必要です。 
The feature group must have a name, a version, and a primary key. 
You can provide an optional description for the feature group. 
フィーチャーグループに対してオプションの説明を提供することもできます。
It is also possible to set descriptions for individual features using the feature group object. 
フィーチャーグループオブジェクトを使用して、個々のフィーチャーの説明を設定することも可能です。
The feature group can be either offline only (online_enabled=False), which is the default, or online (online_enabled=True), in which case tables are created in both the offline and online stores for the feature group. 
フィーチャーグループは、オフラインのみ（online_enabled=False、デフォルト）またはオンライン（online_enabled=True）であり、その場合、フィーチャーグループのためにオフラインストアとオンラインストアの両方にテーブルが作成されます。
For the offline tables, you can specify the table format for the offline tables. 
オフラインテーブルについては、オフラインテーブルのテーブルフォーマットを指定できます。
Available table formats are Apache Hudi ('HUDI'), Delta Lake ('DELTA'), and Apache Iceberg ('ICEBERG'). 
利用可能なテーブルフォーマットは、Apache Hudi（'HUDI'）、Delta Lake（'DELTA'）、およびApache Iceberg（'ICEBERG'）です。
The index columns included in a feature group definition are:
フィーチャーグループ定義に含まれるインデックス列は：



- A mandatory primary key defined in one or more columns
- An optional event time defined in one column (set for time-series data)
- An optional partition key defined in one or more columns
- Optional foreign keys defined in one or more columns

- 一つ以上の列に定義された必須の主キー
- 一つの列に定義されたオプションのイベント時間（時系列データ用に設定）
- 一つ以上の列に定義されたオプションのパーティションキー
- 一つ以上の列に定義されたオプションの外部キー

The primary key for a feature group uniquely identifies an entity in the feature group.
フィーチャーグループの主キーは、そのフィーチャーグループ内のエンティティを一意に識別します。

If the feature group has an event_time column, then there may be many rows in the feature group for that entity.
フィーチャーグループにevent_time列がある場合、そのエンティティに対してフィーチャーグループ内に多くの行が存在する可能性があります。

Each row for that entity will have a different event_time value and potentially different feature values at each point in time.
そのエンティティの各行は異なるevent_time値を持ち、各時点で異なるフィーチャー値を持つ可能性があります。

The event_time is defined in a feature group, and the unique identifier for each row is the combination of the primary_key and event_time.
event_timeはフィーチャーグループ内で定義されており、各行の一意の識別子は主キーとevent_timeの組み合わせです。

For example, in our cc_trans_fg feature group from Chapter 4, there may be many transactions (rows) with the same `cc_num, but` each row will have a different `event_time indicating when the transaction for the` credit card with that cc_num took place.
例えば、私たちの第4章のcc_trans_fgフィーチャーグループでは、同じ`cc_num`を持つ多くのトランザクション（行）が存在する可能性がありますが、各行はその`cc_num`を持つクレジットカードのトランザクションが行われた時刻を示す異なる`event_time`を持ちます。

The primary key can be defined in one column or over two or more columns (as a _composite primary key).
主キーは一つの列で定義することも、二つ以上の列で定義することもできます（_複合主キーとして）。

For example, in_ ``` bank_fg, we could make the primary key a combination of both the bank_id and the country column, so that the bank_id could refer to a country-specific subsidiary of
``` the bank.
例えば、``` bank_fgでは、主キーをbank_idとcountry列の組み合わせにすることができ、bank_idが国特有の銀行の子会社を指すことができます。

The reason to define a column as a foreign key, indicating that it refers to a primary key in another feature group, is to indicate that it should not be included when you select the feature columns for a feature group (foreign keys are index col‐ umns, not features).
外部キーとして列を定義する理由は、それが別のフィーチャーグループの主キーを参照していることを示すためであり、フィーチャーグループのフィーチャー列を選択する際に含めるべきではないことを示します（外部キーはインデックス列であり、フィーチャーではありません）。

A foreign key is a column in a feature group that is used to join fea‐ tures from another feature group.
外部キーは、別のフィーチャーグループからフィーチャーを結合するために使用されるフィーチャーグループ内の列です。

The join column must point to a primary key in a different feature group.
結合列は、異なるフィーチャーグループの主キーを指す必要があります。

In Hopsworks, foreign keys are not statically bound to a specific feature group.
Hopsworksでは、外部キーは特定のフィーチャーグループに静的にバインドされていません。

Instead, they support late binding.
代わりに、遅延バインディングをサポートします。

That is, when you create a feature view, you specify the join key from one feature group to another.
つまり、フィーチャービューを作成する際に、一つのフィーチャーグループから別のフィーチャーグループへの結合キーを指定します。

Hops‐ works validates that the join key is a foreign key and that it points to a primary key in the joined feature group.
Hopsworksは、結合キーが外部キーであり、結合されたフィーチャーグループの主キーを指していることを検証します。

As foreign keys are not statically bound to a feature group, Hopsworks does not enforce foreign key constraints, such as ON DELETE CASCADE.
外部キーがフィーチャーグループに静的にバインドされていないため、HopsworksはON DELETE CASCADEのような外部キー制約を強制しません。

Hopsworks also supports data layout optimizations for the offline (lakehouse) tables, which can help speed up your queries.
Hopsworksは、オフライン（レイクハウス）テーブルのデータレイアウト最適化もサポートしており、これによりクエリの速度を向上させることができます。

You can define a `partition_key on one or` more columns to partition data in the offline store (it has no effect on the online store, as RonDB [automatically partitions data).
一つ以上の列に`partition_key`を定義してオフラインストア内のデータをパーティション分割できます（RonDBがデータを自動的にパーティション分割するため、オンラインストアには影響しません）。

The `partition_key deter‐` mines the subdirectory (or nested subdirectories for multipart partition keys) to which the data (Parquet) files are written in the offline store.
`partition_key`は、オフラインストア内でデータ（Parquet）ファイルが書き込まれるサブディレクトリ（またはマルチパートパーティションキーのためのネストされたサブディレクトリ）を決定します。

That is, all rows in your feature group with the same partition key value(s) store their Parquet files in the same subdirectory of the feature group.
つまり、同じパーティションキー値を持つフィーチャーグループ内のすべての行は、そのフィーチャーグループの同じサブディレクトリにParquetファイルを保存します。

In the preceding feature group creation code snippet, the date column is set as the partition key, so when you insert a DataFrame, all of its rows with the same date value will end up in the same subdirectory (in the feature group’s directory).
前述のフィーチャーグループ作成コードスニペットでは、日付列がパーティションキーとして設定されているため、DataFrameを挿入すると、同じ日付値を持つすべての行が同じサブディレクトリ（フィーチャーグループのディレクトリ内）に格納されます。

Then, when you query data from that feature group (for example, with date="2024-11-11"), only the Parquet files in the “2024-11-11” subdi‐ rectory will be read—skipping the data files for all the other subdirectories for all other dates containing feature data.
その後、そのフィーチャーグループからデータをクエリすると（例えば、date="2024-11-11"の場合）、"2024-11-11"サブディレクトリ内のParquetファイルのみが読み込まれ、フィーチャーデータを含む他の日付のすべての他のサブディレクトリのデータファイルはスキップされます。

This is known as _Hive-style partitioning, and_ when a query can skip reading many of the data files, it is known as _data skipping._
これは_Hiveスタイルのパーティショニング_として知られており、クエリが多くのデータファイルの読み込みをスキップできる場合、_データスキッピング_として知られています。

Hive-style partitioning works well if you have one or more columns with relatively low cardinality.
Hiveスタイルのパーティショニングは、相対的に低いカーディナリティを持つ一つ以上の列がある場合にうまく機能します。

If, however, you pick a partition_key with high cardinality, you will have a new directory for every unique value of your `partition_key.
しかし、カーディナリティが高いpartition_keyを選択すると、`partition_key`の各ユニークな値に対して新しいディレクトリが作成されます。

So do not, for example, make the partition_key the same as the primary key!
したがって、例えば、partition_keyを主キーと同じにしないでください！

The most common use case for partitioning is where you have a feature pipeline that runs once per hour/day/week and creates GBs/TBs of data, then you create a new ``` date column (by extracting the date from your event_time column) and make it the partition_key.
パーティショニングの最も一般的な使用例は、1時間/日/週ごとに実行され、GB/TBのデータを生成するフィーチャーパイプラインがある場合であり、その後、``` event_time列から日付を抽出して新しい日付列を作成し、それをpartition_keyにします。

Every time your feature pipeline runs, a new directory will be created and store the data for that date in the feature group.
フィーチャーパイプラインが実行されるたびに、新しいディレクトリが作成され、その日付のデータがフィーチャーグループに保存されます。

Then, when you query the data and set a _filter on the_ `date for a given time period, only the data for the requested` time period will be read from the offline store, speeding up queries.
その後、データをクエリし、特定の期間の`date`にフィルターを設定すると、要求された期間のデータのみがオフラインストアから読み込まれ、クエリが高速化されます。

Make sure you set the date as a single partition key in ISO 8601 format (YYYY-MM-DD) to store dates in alphabetical order, so your range queries will work correctly.
日付をISO 8601形式（YYYY-MM-DD）で単一のパーティションキーとして設定し、日付をアルファベット順に保存するようにしてください。そうすれば、範囲クエリが正しく機能します。

This means range queries such as (date >= '2025-01-31' AND date <= '2025-02-28') will be partition pruned.
これは、(date >= '2025-01-31' AND date <= '2025-02-28')のような範囲クエリがパーティションプルーニングされることを意味します。

If, in contrast, you decided to create a multipart partition key from three columns—year, month, and day—your nested range queries would be extremely difficult to write.
対照的に、3つの列（年、月、日）からマルチパートパーティションキーを作成することにした場合、ネストされた範囲クエリを書くのは非常に難しくなります。

###### Versioning
###### バージョニング

Hopsworks supports creating multiple versions of feature groups, where each version contains its own offline/online tables and vector indexes.
Hopsworksは、各バージョンが独自のオフライン/オンラインテーブルとベクトルインデックスを含むフィーチャーグループの複数のバージョンを作成することをサポートしています。

Hopsworks also supports _data versioning within a given version of a feature group.
Hopsworksは、特定のフィーチャーグループのバージョン内での_データバージョニング_もサポートしています。

That is, every time data is_ added/updated/deleted to/from a feature group, Hopsworks stores the changes, ena‐ bling Git-like operations on feature groups.
つまり、フィーチャーグループにデータが追加/更新/削除されるたびに、Hopsworksは変更を保存し、フィーチャーグループに対してGitのような操作を可能にします。

Data versioning is based on time-travel capabilities found in lakehouse tables.
データバージョニングは、レイクハウステーブルに見られるタイムトラベル機能に基づいています。

###### Data versioning in feature groups and time travel
###### フィーチャーグループにおけるデータバージョニングとタイムトラベル

Hopsworks tracks mutations (appends, updates, deletions) to feature groups as com‐ mits.
Hopsworksは、フィーチャーグループへの変更（追加、更新、削除）をコミットとして追跡します。

When data is either upserted (inserted or updated) to or deleted from a feature group, each group of changes to the rows in a feature group is called a commit.
データがフィーチャーグループに対してアップサート（挿入または更新）されるか、削除されると、フィーチャーグループ内の行に対する変更の各グループはコミットと呼ばれます。

Every commit has a unique ID and a timestamp (see Figure 5-4).
各コミットには一意のIDとタイムスタンプがあります（図5-4を参照）。

_Figure 5-4. Every time you update data in a feature group, a new commit is performed_ _on the feature group. A history of commits is stored in the feature group, enabling you to_ _read changes made by a commit or read the state of a feature group at a given commit_ _(point in time)._
_図5-4. フィーチャーグループ内のデータを更新するたびに、フィーチャーグループに対して新しいコミットが行われます。コミットの履歴がフィーチャーグループに保存され、コミットによって行われた変更を読み取ったり、特定のコミット時点でのフィーチャーグループの状態を読み取ったりすることができます。_

A commit contains a set of updates/deletes/appends to rows in the feature group.
コミットには、フィーチャーグループ内の行に対する一連の更新/削除/追加が含まれます。

Each commit has an associated timestamp, and as long as a commit has not been compacted, you can time-travel on a feature group to read its state “as of” a given timestamp.
各コミットには関連するタイムスタンプがあり、コミットが圧縮されていない限り、フィーチャーグループの状態を特定のタイムスタンプの「時点」で読み取るためにタイムトラベルできます。

In Figure 5-4, you can also see how rows in feature groups are removed by providing a DataFrame `df containing the primary key values for the rows to be` deleted and then calling fg.delete_records(df).
図5-4では、行を削除するための主キー値を含むDataFrame `df`を提供し、その後fg.delete_records(df)を呼び出すことで、フィーチャーグループ内の行がどのように削除されるかも見ることができます。

Feature groups support both _time-travel and_ _incremental queries (note: this is only_ supported by Spark clients for Hopsworks 4.x):
フィーチャーグループは、_タイムトラベル_と_インクリメンタルクエリ_の両方をサポートしています（注：これはHopsworks 4.xのSparkクライアントのみでサポートされています）：

- Time-travel queries read data in the feature group ASOF a provided timestamp or commit ID.
- タイムトラベルクエリは、提供されたタイムスタンプまたはコミットIDの時点でフィーチャーグループ内のデータを読み取ります。

The timestamp here does not refer to the `event_time column in a` feature group, but rather to the ingestion time for the commit.
ここでのタイムスタンプはフィーチャーグループ内の`event_time`列を指すのではなく、コミットの取り込み時間を指します。

- Incremental queries read the data changed in commits to a feature group during a specified time range—that is, the row-level upserts (inserts or updates).
- インクリメンタルクエリは、指定された時間範囲内でフィーチャーグループへのコミットで変更されたデータを読み取ります。つまり、行レベルのアップサート（挿入または更新）です。

You can provide the ingestion time as a parameter to the `as_of() method to read` the state of the feature group ASOF that point in time (see Figure 5-5).
取り込み時間を`as_of()`メソッドのパラメータとして提供して、その時点でのフィーチャーグループの状態を読み取ることができます（図5-5を参照）。

You can also read changes to records upserted within a specified time interval.
指定された時間間隔内でアップサートされたレコードの変更を読み取ることもできます。

The time range is specified with a starting timestamp (asof) and an optional ending timestamp (exclude_until).
時間範囲は、開始タイムスタンプ（asof）とオプションの終了タイムスタンプ（exclude_until）で指定されます。

If no ending timestamp is set, the range returned will include all records since the starting timestamp.
終了タイムスタンプが設定されていない場合、返される範囲には開始タイムスタンプ以降のすべてのレコードが含まれます。

_Figure 5-5. For version 2 of the bank_fg feature group, we read the changes in the_ _provided date interval as df1, containing the rows updated/appended in the time range_ _provided. We then read the state of the feature group into df2 as of the provided_ _timestamp. If you omit the timestamp, read() returns the latest data._
_図5-5. bank_fgフィーチャーグループのバージョン2では、提供された日付範囲内の変更をdf1として読み取り、その範囲内で更新/追加された行を含みます。その後、提供されたタイムスタンプの時点でフィーチャーグループの状態をdf2に読み取ります。タイムスタンプを省略すると、read()は最新のデータを返します。_

Note that the ingestion time refers to the physical (actual) time at which that commit was ingested into Hopsworks.
取り込み時間は、そのコミットがHopsworksに取り込まれた物理的（実際の）時間を指します。

The ingestion time can be confusing because your fea‐ ture group may also have an event_time column indicating the value of a feature as of a point in time.
取り込み時間は混乱を招く可能性があります。なぜなら、フィーチャーグループには、ある時点でのフィーチャーの値を示すevent_time列があるかもしれないからです。

Ingestion time and event time are different concepts.
取り込み時間とイベント時間は異なる概念です。

For example, imagine that in our air quality project from Chapter 3, a sensor went offline from days 4 to 9, as shown in Figure 5-6.
例えば、第3章の私たちの空気質プロジェクトで、センサーが4日目から9日目までオフラインになったと想像してみてください（図5-6に示されています）。

_Figure 5-6. In this diagram, we see air quality measurements from days 4 to 9 arrive late_ _on day 10. They arrived just after Training Dataset v1 was created. If we want to_ _reproduce Training Dataset v1 at a later point in time, we should not include the late-_ _arriving data in it._
_図5-6. この図では、4日目から9日目までの空気質測定値が10日目に遅れて到着する様子が示されています。これらは、Training Dataset v1が作成された直後に到着しました。後でTraining Dataset v1を再現したい場合、遅れて到着したデータは含めるべきではありません。_



The weather updates came for every day, but on day 10, we received the missing six days of air quality measurements. 
天気の更新は毎日ありましたが、10日目に、欠けていた6日間の空気質測定値が届きました。

They arrived late. 
それらは遅れて到着しました。

The event_time values for these six late arrivals correspond to days 4 to 9, which makes sense as the event_time refers to the day the air quality measurement was taken. 
これらの6つの遅れた到着のevent_timeの値は、4日から9日までに対応しており、event_timeは空気質測定が行われた日を指すため、理にかなっています。

However, the ingestion time for the late arrivals is day 10—so the event time doesn’t match ingestion time. 
しかし、遅れた到着の摂取時間は10日目であるため、event timeは摂取時間と一致しません。

In real-world systems, late-arriving data is a fact of life, and systems need to be designed to account for it. 
実世界のシステムでは、遅れて到着するデータは現実の一部であり、システムはそれに対応できるように設計される必要があります。

If you read the feature group on day 9, it will not include any of the air quality measurements from days 4 to 9, but if you read it on day 10, it will include the measurements from days 4 to 10. 
9日目にフィーチャーグループを読むと、4日から9日までの空気質測定値は含まれませんが、10日目に読むと、4日から10日までの測定値が含まれます。

The Training Dataset v1 was created on day 9, however, and it does not include days 4 to 9. 
ただし、Training Dataset v1は9日目に作成されており、4日から9日までのデータは含まれていません。

If I later delete Training Dataset v1 but have to reproduce it, I would like it to be exactly the same as the original (compliance will demand this). 
後でTraining Dataset v1を削除して再現する必要がある場合、元のものと全く同じであることを望みます（コンプライアンスがこれを要求します）。

I do not want it to include the air quality data for days 4 to 9. 
4日から9日までの空気質データを含めたくありません。

However, if I only used a query based on the _event time to reproduce the training dataset, it would_ include the data from days 4 to 9. 
しかし、_event timeに基づくクエリのみを使用してトレーニングデータセットを再現した場合、4日から9日までのデータが含まれてしまいます。_

The solution is to use ingestion time to re-create Training Dataset v1 exactly as it was created on day 9. 
解決策は、摂取時間を使用してTraining Dataset v1を9日目に作成されたとおりに正確に再作成することです。

Luckily, Hopsworks does this transparently for you when you call any of its feature view methods to re-create training data using its version number, such as: 
幸運なことに、Hopsworksは、バージョン番号を使用してトレーニングデータを再作成するためにそのフィーチャービューのメソッドのいずれかを呼び出すと、これを透明に行います。

```  
X, y = feature_view.get_train_test_split(training_dataset_version=1)
```

We have seen the term _ASOF twice now in different contexts._ 
私たちは、異なる文脈で_ ASOFという用語を2回見てきました。_

When you re-create a training dataset, you want to include the feature data `ASOF its ingestion time (the feature data that existed at` that time). 
トレーニングデータセットを再作成する際には、特徴データを`摂取時間のASOF（その時点で存在した特徴データ）`として含めたいです。

But when you create point-in-time correct training data, you want the value of the features ASOF the event time, as you want to include the correct value for that feature at that point in time. 
しかし、時点に正しいトレーニングデータを作成する場合、event timeのASOFで特徴の値を取得したいです。その時点でその特徴の正しい値を含めたいからです。

###### Versioning feature groups
###### フィーチャーグループのバージョン管理

Data versioning is only concerned with changes to the rows in feature groups. 
データのバージョン管理は、フィーチャーグループ内の行の変更にのみ関係しています。

But what if you want to add, remove, or update the features in a feature group? 
しかし、フィーチャーグループに特徴を追加、削除、または更新したい場合はどうなりますか？

You can add a new feature to a feature group as follows, and existing clients of the feature group will work as before: 
次のようにフィーチャーグループに新しい特徴を追加できます。フィーチャーグループの既存のクライアントは以前と同様に機能します。

```  
features = [     
    Feature(name="limit", type="int", default_value=1000)   
]   
fg = fs.get_feature_group(name=”cc_trans_fg”, version=1)   
fg.append_features(features)
```

However, if you want to change the data type for a feature or delete a feature from a feature group, then you are making a breaking schema change. 
ただし、特徴のデータ型を変更したり、フィーチャーグループから特徴を削除したりする場合は、破壊的なスキーマ変更を行っていることになります。

Existing clients of the feature group will not work because one or more of the features they expect will either have the wrong data type or not exist. 
フィーチャーグループの既存のクライアントは機能しません。なぜなら、彼らが期待する1つ以上の特徴が、間違ったデータ型を持っているか、存在しないからです。

Another less obvious breaking change is changing how a feature is computed. 
もう一つの明白でない破壊的変更は、特徴の計算方法を変更することです。

You shouldn’t mix the old feature values and new feature values in the same feature in a feature group. 
フィーチャーグループ内の同じ特徴に古い特徴値と新しい特徴値を混ぜるべきではありません。

This will not break clients, but any models you train on the mixed feature data will probably not perform well. 
これによりクライアントは壊れませんが、混合された特徴データでトレーニングしたモデルはおそらくうまく機能しません。

The solution to breaking (schema) changes is to create a new version of the feature group with new feature(s). 
破壊的（スキーマ）変更の解決策は、新しい特徴を持つフィーチャーグループの新しいバージョンを作成することです。

For example, in Figure 5-7, the `cc_fraud_v1 model is` upgraded to cc_fraud_v2, which uses a new version v2 of the account feature group. 
例えば、図5-7では、`cc_fraud_v1モデルが`cc_fraud_v2にアップグレードされ、アカウントフィーチャーグループの新しいバージョンv2を使用します。

When a model depends on a feature group for precomputed features, the model and feature versions are tightly coupled, requiring synchronized upgrades and down‐ grades of model/feature versions. 
モデルが事前計算された特徴のためにフィーチャーグループに依存している場合、モデルとフィーチャーのバージョンは密接に結びついており、モデル/フィーチャーのバージョンの同期されたアップグレードとダウングレードが必要です。

_Figure 5-7. Here, v2 of the cc_fraud model uses new features only available in v2 of the_ _account feature group. 
_図5-7。ここでは、cc_fraudモデルのv2が、アカウントフィーチャーグループのv2でのみ利用可能な新しい特徴を使用しています。_

To be able to downgrade (in case of error), you need to maintain_ _the older v1 of the account feature group._ 
（エラーが発生した場合に）ダウングレードできるようにするには、アカウントフィーチャーグループの古いv1を維持する必要があります。_

When you create a new feature group version, new offline/online tables will be cre‐ ated, so you will need to backfill the new feature group version with data from the old feature group version. 
新しいフィーチャーグループのバージョンを作成すると、新しいオフライン/オンラインテーブルが作成されるため、新しいフィーチャーグループのバージョンを古いフィーチャーグループのバージョンのデータでバックフィルする必要があります。

The backing table name in the offline/online stores is ``` <feature_group_name>__<version>. 
オフライン/オンラインストアのバックテーブル名は``` <feature_group_name>__<version>です。 

When a feature group has a large amount of data, you may want to avoid creating a new version of a feature group due to the cost of backfilling. 
フィーチャーグループに大量のデータがある場合、バックフィルのコストのためにフィーチャーグループの新しいバージョンを作成することを避けたい場合があります。

Sometimes, you can just keep appending new features, leaving the old feature versions in the feature group. 
時には、新しい特徴を追加し続け、古いフィーチャーバージョンをフィーチャーグループに残すことができます。

That can also be expensive, as appending a new feature requires updating all existing rows in the table with a `default_value. 
それも高くつく可能性があります。新しい特徴を追加するには、テーブル内のすべての既存の行を`default_value`で更新する必要があるからです。

For example, assume you have a feature group with hundreds of columns that stores 10s of TBs of data but you only want to change how one column is computed. 
例えば、数百の列を持ち、10TB以上のデータを保存するフィーチャーグループがあると仮定しますが、1つの列の計算方法だけを変更したいとします。

You don’t want to create a new version of the feature group and backfill the whole feature group. 
フィーチャーグループの新しいバージョンを作成し、フィーチャーグループ全体をバックフィルしたくありません。

You don’t want to append a new feature, either, as that will require updating all rows in the feature group with the new column and its default value—in lakehouse tables, that will probably require rewrit‐ ing all of the data files. 
新しい特徴を追加したくもありません。なぜなら、それはフィーチャーグループ内のすべての行を新しい列とそのデフォルト値で更新する必要があるからです。レイクハウステーブルでは、おそらくすべてのデータファイルを再書き込みする必要があります。

Instead, you can create a new feature group with a different name but with the same primary key and event time as the original feature group (see Figure 5-8). 
その代わりに、異なる名前の新しいフィーチャーグループを作成できますが、元のフィーチャーグループと同じ主キーとevent timeを持っています（図5-8を参照）。

You will need to backfill the new column for this feature group, but it will be a much less expensive operation than backfilling hundreds of columns. 
このフィーチャーグループの新しい列をバックフィルする必要がありますが、それは数百の列をバックフィルするよりもはるかに安価な操作になります。

_Figure 5-8. The new feature group stores a categorical version of the limit feature—the_ _original is a numerical feature. 
_図5-8。新しいフィーチャーグループは、制限特徴のカテゴリカルバージョンを保存します。元のものは数値的な特徴です。_

Feature view v2 replaces the old limit feature with the new one but keeps the other features unchanged from v1. 
フィーチャービューv2は、古い制限特徴を新しいものに置き換えますが、他の特徴はv1から変更されません。

Model v1 continues to use the_ _old limit feature, while model v2 uses the new limit feature. 
モデルv1は古い制限特徴を使用し続け、モデルv2は新しい制限特徴を使用します。_

The new feature, from Figure 5-8, is a categorical `limit feature in our new feature` group that we will compute from the sparse limit feature. 
図5-8の新しい特徴は、スパース制限特徴から計算する新しいフィーチャーグループのカテゴリカル`limit featureです。`

You need to write a trans‐ formation function that converts the numerical `limit value to categorical value` (high, med, or low). 
数値的な`limit valueをカテゴリカル値`（高、中、または低）に変換する変換関数を書く必要があります。

That transformation function can be used to backfill the new feature group with all of the values from the original feature group, and it should also be included in a feature pipeline that will update the new feature group. 
その変換関数は、元のフィーチャーグループからのすべての値で新しいフィーチャーグループをバックフィルするために使用でき、また新しいフィーチャーグループを更新するフィーチャーパイプラインにも含めるべきです。

Now, assume we have a model v1 that we want to update to v2 to use the new catego‐ rical `limit feature instead of the numerical` `limit. 
さて、モデルv1をv2に更新して新しいカテゴリカル`limit featureを数値的な`limitの代わりに使用したいと仮定します。

What we can do is create a new`  
何ができるかというと、新しい`  

_feature view v2 that replaces the old numerical limit with the new categorical limit_ but keeps all the other features from feature view v1. 
古い数値的な制限を新しいカテゴリカル制限に置き換えるフィーチャービューv2を作成しますが、フィーチャービューv1からの他のすべての特徴はそのままにします。

Creating feature views is a metadata-only operation, so it is cheap. 
フィーチャービューを作成することはメタデータのみの操作であるため、コストは低いです。

The new feature view can now create new training data and train model v2. 
新しいフィーチャービューは、現在新しいトレーニングデータを作成し、モデルv2をトレーニングできます。

Now assume that you have a production model that uses the old feature and you want to deploy a new version of the model that uses a new version of the feature. 
さて、古い特徴を使用するプロダクションモデルがあり、そのモデルの新しいバージョンを新しいバージョンの特徴を使用して展開したいと仮定します。

For the new model, you create a new feature view that uses all the features from the feature view of the previous model, replacing the old feature with the new one. 
新しいモデルのために、前のモデルのフィーチャービューからすべての特徴を使用し、古い特徴を新しいものに置き換える新しいフィーチャービューを作成します。

When you read train‐ ing/inference data from the new feature view, it will join the original features (not including the feature you are replacing) with the new version of your feature. 
新しいフィーチャービューからトレーニング/推論データを読むと、元の特徴（置き換える特徴を含まない）と新しいバージョンの特徴が結合されます。

###### Online Store
###### オンラインストア

When you create a feature group, you have to decide whether the feature data will be stored in the online store or not. 
フィーチャーグループを作成する際には、フィーチャーデータをオンラインストアに保存するかどうかを決定する必要があります。

By default, a table is not created in the online store. 
デフォルトでは、オンラインストアにテーブルは作成されません。

To enable the online store, you have to specify online_enabled=True when you cre‐ ate the feature group. 
オンラインストアを有効にするには、フィーチャーグループを作成する際にonline_enabled=Trueを指定する必要があります。

In contrast, a table is always created in the offline store. 
対照的に、オフラインストアには常にテーブルが作成されます。

You should make a feature group online_enabled if its feature data will be read by inter‐ active or real-time ML systems. 
フィーチャーデータがインタラクティブまたはリアルタイムのMLシステムによって読み取られる場合、フィーチャーグループをonline_enabledにするべきです。

If the feature data will only be used by batch ML systems, then do not make it `online_enabled, as it will add cost in data storage and` updates. 
フィーチャーデータがバッチMLシステムでのみ使用される場合は、`online_enabledにしないでください。データストレージと`更新のコストが追加されるためです。

If you want an online-only feature group, with no data in the offline store, then you specify that writes should not be materialized to the offline store: 
オフラインストアにデータがないオンライン専用のフィーチャーグループが必要な場合は、書き込みがオフラインストアに具現化されないように指定します。

```  
fg.insert(df,     
    write_options={"start_offline_materialization":False}   
)
```

Hopsworks stores online feature data either in memory or in on-disk columns. 
Hopsworksは、オンラインフィーチャーデータをメモリまたはディスク上の列に保存します。

By default, it uses _in-memory tables, which have lower latency and higher throughput_ compared with on-disk columns. 
デフォルトでは、ディスク上の列と比較して、_レイテンシが低くスループットが高い_インメモリテーブルを使用します。

However, in-memory tables require enough RAM to store the data, and when you have feature groups that will store many TBs of online data, it may be more cost-efficient to use on-disk tables. 
ただし、インメモリテーブルはデータを保存するために十分なRAMを必要とし、オンラインデータを多く保存するフィーチャーグループがある場合、ディスク上のテーブルを使用する方がコスト効率が良い場合があります。

You can specify that the online feature data will be stored on disk (online_disk=True) when you create the feature group as follows: 
フィーチャーグループを作成する際に、オンラインフィーチャーデータをディスクに保存するように指定できます（online_disk=True）。

```  
fs.create_feature_group(     
    ... 
    online_enabled=True,     
    online_disk=True   
)
```

The code also shows how you can configure the table_space for the on-disk table in RonDB—you allocate storage space for on-disk data in table spaces in RonDB. 
このコードは、RonDBのディスク上のテーブルのtable_spaceを構成する方法も示しています。RonDBのテーブルスペースにディスク上のデータのストレージスペースを割り当てます。



###### Time to live 有効期限

By default, the event_time column is not included in the online table, and the online table only stores the latest feature values for each entity. 
デフォルトでは、event_time列はオンラインテーブルに含まれておらず、オンラインテーブルは各エンティティの最新の特徴値のみを保存します。

When you write new feature data for an entity, the row containing the feature data for that entity is overwritten. 
エンティティの新しい特徴データを書き込むと、そのエンティティの特徴データを含む行が上書きされます。

This ties the size of your online table to the number of entities in your table. 
これにより、オンラインテーブルのサイズはテーブル内のエンティティの数に依存します。

However, what if you have hundreds of millions of entities and the feature data becomes stale for an entity after a period of time? 
しかし、数億のエンティティがあり、エンティティの特徴データが一定の期間後に古くなった場合はどうでしょうか？

Or what if you want to perform online aggregations for an entity? 
また、エンティティに対してオンライン集計を行いたい場合はどうでしょうか？

Then you will need to include the event_time column in the online table to be able to store many rows for each entity. 
その場合、各エンティティのために多くの行を保存できるように、オンラインテーブルにevent_time列を含める必要があります。

In both of these cases, you should specify a _time-to-live (TTL) value for rows, whereby rows are_ removed from the database when they exceed the specified TTL defined on the feature group. 
これらの両方のケースでは、行のために有効期限（TTL）値を指定する必要があります。これにより、行は特徴グループで定義された指定されたTTLを超えたときにデータベースから削除されます。

For example, if the TTL is one hour, then one hour after the event_time for a row has passed, the row will be scheduled for deletion. 
例えば、TTLが1時間の場合、行のevent_timeが経過してから1時間後に、その行は削除のスケジュールに入ります。

You can define the TTL, at minute-level granularity, when you create an online_enabled feature group: 
オンライン対応の特徴グループを作成する際に、分単位の粒度でTTLを定義できます：

```  
ttl=timedelta(days=7)   
fs.create_feature_group( …     
ttl=ttl   
)
```

When you set a value for ttl, ttl_enabled is set to True for the feature group, and the primary key constraint for the entity ID is dropped. 
ttlの値を設定すると、ttl_enabledが特徴グループに対してTrueに設定され、エンティティIDの主キー制約が削除されます。

That is, like the offline store, each row is uniquely identified by the combination of the primary key (entity ID) and `event_time. 
つまり、オフラインストアと同様に、各行は主キー（エンティティID）と`event_time`の組み合わせによって一意に識別されます。

TTL expiration is a background process, and expired rows are typically deleted within 15 minutes of expiration, although in situations with high database load, it may take a bit longer. 
TTLの期限切れはバックグラウンドプロセスであり、期限切れの行は通常、期限切れから15分以内に削除されますが、高いデータベース負荷の状況では、もう少し時間がかかることがあります。

It is important to handle potential data leakage caused by the TTL. 
TTLによって引き起こされる可能性のあるデータ漏洩を処理することが重要です。

When you are creating training data, what should happen if the `label.event_time is 01:00 and a` 
トレーニングデータを作成しているとき、`label.event_time`が01:00で、`feature.event_time`が00:15でTTLが30分の場合、何が起こるべきでしょうか？

``` feature.event_time for that label is 00:15 but the TTL is 30 minutes? 
その特徴値を含めるべきではありません。そうでなければ、漏洩が発生します。

You shouldn’t include that feature value; otherwise, there will be leakage. 
その特徴値を含めるべきではありません。そうでなければ、漏洩が発生します。

The reason why is that the online store would have removed the feature’s row at 00:45, when its TTL expired. 
その理由は、オンラインストアが00:45にその特徴の行を削除したためです。TTLが期限切れになったときです。

When the label event arrived at 01:00, there would be no feature value to retrieve. 
ラベルイベントが01:00に到着したとき、取得する特徴値はありません。

This is a subtle yet pernicious form of data leakage that Hopsworks prevents by adding a lookback window to queries. 
これは微妙でありながら悪質なデータ漏洩の形であり、Hopsworksはクエリにルックバックウィンドウを追加することでこれを防ぎます。

The general rule here is that when you create training data using features from a feature group with a TTL, the feature value will be null if the following holds: 
ここでの一般的なルールは、TTLを持つ特徴グループの特徴を使用してトレーニングデータを作成する場合、次の条件が満たされると特徴値はnullになります：

```  
label.event_time - feature.event_time > TTL
```

###### Vector index ベクトルインデックス

Vector embeddings enable approximate nearest neighbor (ANN) search (also known as similarity search) for rows in online_enabled feature groups. 
ベクトル埋め込みは、オンライン対応の特徴グループ内の行に対して近似最近傍（ANN）検索（類似性検索とも呼ばれる）を可能にします。

You create a vector embedding by taking high-dimensional data (such as text, images, or a mix of data) and passing it to an _embedding model that then compresses the input data into a_ fixed-size array of floating-point numbers. 
高次元データ（テキスト、画像、またはデータの混合など）を取り、それを_埋め込みモデル_に渡すことでベクトル埋め込みを作成し、入力データを_固定サイズの浮動小数点数の配列_に圧縮します。

The vector embedding is the output array of floating-point numbers, and what is astonishing about it is that, even after compression, it retains semantic information about the original input data. 
ベクトル埋め込みは浮動小数点数の出力配列であり、圧縮後も元の入力データに関する意味情報を保持していることが驚くべき点です。

You can take millions of images or books of text (split into paragraphs), compute vector embeddings from them, and then pass in a new image or piece of text, and ANN search will find the closest images or paragraphs of text to the new data. 
数百万の画像やテキストの本（段落に分割）を取り、それらからベクトル埋め込みを計算し、新しい画像やテキストを渡すと、ANN検索は新しいデータに最も近い画像や段落を見つけます。

And they work really well, even though it is a probabilistic matching. 
確率的なマッチングであるにもかかわらず、非常にうまく機能します。

To add vector embeddings to a feature group, you specify which columns in your DataFrame contain the vector embeddings. 
特徴グループにベクトル埋め込みを追加するには、DataFrame内のどの列がベクトル埋め込みを含むかを指定します。

The column values are then inserted into a vector index so that you can call `find_neighbors() on the feature group to find` rows with similar values. 
列の値はベクトルインデックスに挿入され、特徴グループの`find_neighbors()`を呼び出して類似の値を持つ行を見つけることができます。

However, before inserting rows into an _embedding feature_ _group, you need to first compute the vector embeddings for the columns using an_ _embedding model. 
ただし、_埋め込み特徴_グループに行を挿入する前に、_埋め込みモデル_を使用して列のベクトル埋め込みを最初に計算する必要があります。

There are many off-the-shelf embedding models that you can use, such as the sentence transformers model in the following example. 
使用できるオフ・ザ・シェルフの埋め込みモデルが多数あり、以下の例のように文の変換器モデルがあります。

You can also train your own embedding model. 
独自の埋め込みモデルをトレーニングすることもできます。

We will now look at our example credit card transaction fraud system and how we add support for vector embeddings. 
次に、クレジットカード取引詐欺システムの例と、ベクトル埋め込みのサポートを追加する方法を見ていきます。

Suppose you are doing some EDA on fraudulent transactions and would like to find the rows that are most similar to a row marked as fraud. 
詐欺取引に関するEDAを行っていて、詐欺としてマークされた行に最も類似した行を見つけたいとします。

That’s hard, as there may be tens of thousands of rows of fraudulent transactions or more. 
それは難しいです。なぜなら、詐欺取引の行が数万行以上あるかもしれないからです。

The cc_fraud table (in Postgres) that contains the fraud labels also has a string column called explanation. 
詐欺ラベルを含むcc_fraudテーブル（Postgres内）には、explanationという文字列列もあります。

This column contains a human-written description of the reason the transaction was marked as fraudulent. 
この列には、取引が詐欺としてマークされた理由の人間が書いた説明が含まれています。

You can add the data from the `cc_fraud table as a new feature group (cc_fraud_fg) to enable similarity` search for fraudulent transactions using the explanation. 
`cc_fraud`テーブルのデータを新しい特徴グループ（cc_fraud_fg）として追加し、説明を使用して詐欺取引の類似性検索を有効にできます。

You can then run the following code that reads the source data from an external feature group (for cc_fraud) and creates a vector embedding using an open source sentence-transformers (embedding) model that maps the `explanation to a 384-dimensional array. 
次に、外部特徴グループ（cc_fraud）からソースデータを読み込み、`explanation`を384次元の配列にマッピングするオープンソースの文変換器（埋め込み）モデルを使用してベクトル埋め込みを作成する以下のコードを実行できます。

The vector embedding is stored as a column in the cc_fraud_fg: 
ベクトル埋め込みはcc_fraud_fgの列として保存されます：

```  
from sentence_transformers import SentenceTransformer   
model = SentenceTransformer('all-MiniLM-L6-v2')   
df = cc_fraud.read()   
embedding_body = model.encode(df['explanation'])   
df['embed_explanation'] = pd.Series(embedding_body.tolist())   
emb = embedding.EmbeddingIndex()   
emb.add_embedding('explanation', model.get_sentence_embedding_dimension())   
cc_fraud_fg = fs.create_feature_group(     
name="cc_fraud_fg",     
version=1,     
description="Credit Card Fraud Data",     
primary_key=['tid'],     
event_time='datetime',     
embedding=emb   
)   
cc_fraud_fg.insert(df)
```

You can then perform similarity search on cc_fraud_fg, passing a vector embedding to the feature group’s find_neighbor() method: 
その後、cc_fraud_fgで類似性検索を実行し、ベクトル埋め込みを特徴グループのfind_neighbor()メソッドに渡すことができます：

```  
model = SentenceTransformer('all-MiniLM-L6-v2')   
search_query = "Geographic attack in South Carolina"   
cc_fraud_fg.find_neighbors(model.encode(search_query), k=3)
```

The preceding code will return the three rows in the feature group that had an 
``` explanation column value that is most similar to the search string “Geographic 
```
attack in South Carolina.” 
前述のコードは、特徴グループ内で検索文字列「Geographic attack in South Carolina」に最も類似した`explanation`列の値を持つ3行を返します。



###### Offline Store (Lakehouse Tables) オフラインストア（レイクハウステーブル）

Hopsworks’ offline store is lakehouse tables. 
Hopsworksのオフラインストアはレイクハウステーブルです。

Hopsworks supports three different types of lakehouse table, each of which has its own strengths: Apache Iceberg, Apache Hudi, and Delta Lake. 
Hopsworksは、Apache Iceberg、Apache Hudi、Delta Lakeの3種類のレイクハウステーブルをサポートしており、それぞれに独自の強みがあります。

All three formats support time travel, but there are other properties leveraged by Hopsworks: 
これら3つのフォーマットはすべてタイムトラベルをサポートしていますが、Hopsworksによって活用される他の特性もあります。

_Primary key uniqueness_ This is enforced by Hudi but not by Iceberg or Delta. 
_主キーの一意性_ はHudiによって強制されますが、IcebergやDeltaでは強制されません。

_Data skipping_ Hive-style partitioning is supported across all three file formats, but additionally, there is Z-ordering (Hudi, Delta), liquid clustering (Delta), and Hilbert spacefilling curves (Hudi). 
_データスキップ_ は、すべてのファイルフォーマットでHiveスタイルのパーティショニングをサポートしていますが、さらにZ-ordering（Hudi、Delta）、液体クラスタリング（Delta）、およびヒルベルト空間充填曲線（Hudi）があります。

``` Read_changes
```
``` Read_changes
```
File formats support _CDC queries, although full support will only come in Ice‐_ berg v3. 
ファイルフォーマットは_CDCクエリをサポートしていますが、完全なサポートはIceberg v3でのみ提供されます。

Delta and Iceberg do not enforce the uniqueness constraint for primary keys, and this means you have duplicate rows when you create training data. 
DeltaとIcebergは主キーの一意性制約を強制しないため、トレーニングデータを作成するときに重複行が発生します。

The ASOF LEFT JOIN (which is used to create training data from Chapter 4) joins features to labels, and if there are multiple matching rows in a joined feature group, you will get multiple output rows for each row in your label feature group. 
ASOF LEFT JOIN（第4章からトレーニングデータを作成するために使用される）は、特徴をラベルに結合し、結合された特徴グループに複数の一致する行がある場合、ラベル特徴グループの各行に対して複数の出力行が得られます。

That is not desired behavior, as a feature should have only one value for a given label. 
これは望ましくない動作であり、特徴は特定のラベルに対して1つの値のみを持つべきです。

###### External feature groups 外部特徴グループ

If you already have existing tables with feature data in a data warehouse or object store, you can create an external feature group from those tables. 
データウェアハウスやオブジェクトストアに特徴データを持つ既存のテーブルがある場合、それらのテーブルから外部特徴グループを作成できます。

In external feature groups, the offline table is the external data store or data warehouse (such as S3, Snowflake, BigQuery, Redshift, or any database that is compatible with Java Database Connectivity [JDBC]). 
外部特徴グループでは、オフラインテーブルは外部データストアまたはデータウェアハウス（S3、Snowflake、BigQuery、Redshift、またはJava Database Connectivity [JDBC]と互換性のある任意のデータベースなど）です。

No offline data will be stored in Hopsworks; only metadata will be stored there. 
Hopsworksにはオフラインデータは保存されず、メタデータのみが保存されます。

For example, all of the tables in our credit card data mart (credit_card_transactions, `card_details,` `merchant_details,` `account_details,` ``` bank_details) can be created as external feature groups, making it easy to use them as data sources for feature pipelines. 
たとえば、私たちのクレジットカードデータマートのすべてのテーブル（credit_card_transactions、`card_details、` `merchant_details、` `account_details、` ``` bank_details）は外部特徴グループとして作成でき、特徴パイプラインのデータソースとして簡単に使用できます。

An external feature group first needs a data source for your external store. 
外部特徴グループは、まず外部ストアのデータソースが必要です。

External feature groups are interchangeable with normal feature groups—you can read feature data for them, use them in feature views, and so on. 
外部特徴グループは通常の特徴グループと互換性があり、それらの特徴データを読み取ったり、特徴ビューで使用したりできます。

Typically, you create external feature groups in the Hopsworks UI, where you can enter the connection details for a data source, and then, with LLM assistance, select the external tables you want included. 
通常、Hopsworks UIで外部特徴グループを作成し、データソースの接続詳細を入力し、その後LLMの支援を受けて含めたい外部テーブルを選択します。

You can also create external feature groups with API calls. 
API呼び出しを使用して外部特徴グループを作成することもできます。

Here, we show you how to define `account_fg as an external feature group, assuming you already have created the Snowflake data source object: 
ここでは、Snowflakeデータソースオブジェクトをすでに作成していると仮定して、`account_fg`を外部特徴グループとして定義する方法を示します。

```   
data_source = fs.get_data_source("my_snowflake")   
external_fg = fs.create_external_feature_group(         
    name="sales",         
    version=1,         
    description="Physical shop sales features",         
    primary_key=['account_id'],         
    event_time='event_time',         
    data_source=data_source         
).save()
```
```   
data_source = fs.get_data_source("my_snowflake")   
external_fg = fs.create_external_feature_group(         
    name="sales",         
    version=1,         
    description="物理店舗の販売特徴",         
    primary_key=['account_id'],         
    event_time='event_time',         
    data_source=data_source         
).save()
```
If your external feature group is online_enabled, you need to schedule a job to syn‐ chronize the data from the offline store to the online store. 
外部特徴グループがonline_enabledの場合、オフラインストアからオンラインストアにデータを同期するジョブをスケジュールする必要があります。

###### Data statistics データ統計

When you write data to the offline feature group, by default, Hopsworks computes and saves descriptive statistics for features. 
オフライン特徴グループにデータを書き込むと、デフォルトでHopsworksは特徴の記述統計を計算して保存します。

Statistics are used for both EDA and mon‐ itoring for feature drift (see Chapter 14). 
統計は、EDAおよび特徴ドリフトの監視（第14章を参照）に使用されます。

Hopsworks can compute histograms for cat‐ egorical variables (counts for each of the categories), a _correlation matrix for the_ features (to help identify redundant features that can be removed), descriptive statis‐ _tics for numerical features (min, max, mean, standard deviation), and the sparsity of a_ feature through exact_uniqueness (values closer to 1 indicate more unique values). 
Hopsworksは、カテゴリ変数のヒストグラム（各カテゴリのカウント）、特徴の_相関行列_（削除可能な冗長な特徴を特定するのに役立つ）、数値特徴の記述統計（最小値、最大値、平均、標準偏差）、およびexact_uniquenessを通じて特徴のスパース性（値が1に近いほどよりユニークな値を示します）を計算できます。

You provide the list of features that you want to compute features for in the columns parameter of the statistics_config dictionary: 
計算したい特徴のリストをstatistics_config辞書のcolumnsパラメータに提供します。

```   
fg_cc = feature_store.create_feature_group(name="cc_trans_fg",     
    statistics_config={       
        "enabled": True,       
        "histograms": True,       
        "correlations": True,       
        "exact_uniqueness": False,       
        "columns": ["feature1"]     
    }   
)   
fg_cc.compute_statistics()
```
```   
fg_cc = feature_store.create_feature_group(name="cc_trans_fg",     
    statistics_config={       
        "enabled": True,       
        "histograms": True,       
        "correlations": True,       
        "exact_uniqueness": False,       
        "columns": ["feature1"]     
    }   
)   
fg_cc.compute_statistics()
```
Note that computing statistics is expensive, particularly if they are computed on large volumes of data. 
統計を計算することは高コストであることに注意してください。特に、大量のデータに対して計算される場合はそうです。

###### Change Data Capture for Feature Groups 特徴グループの変更データキャプチャ

Sometimes, it is useful to build event-driven ML systems by executing actions when rows in a feature group have changed. 
時には、特徴グループの行が変更されたときにアクションを実行することで、イベント駆動型のMLシステムを構築することが有用です。

One example use case is when you have a large number of entities and you want to make predictions for entities after changes in their feature values. 
1つの使用例は、多数のエンティティがあり、それらの特徴値の変更後にエンティティの予測を行いたい場合です。

You can do this by enabling a change data capture (CDC) API for a feature group by providing a Kafka topic for the feature group:  
これを行うには、特徴グループのためにKafkaトピックを提供することで、特徴グループの変更データキャプチャ（CDC）APIを有効にします。

```   
kafka_api = project.get_kafka_api()   
my_schema = kafka_api.create_schema(SCHEMA_NAME, schema)   
my_topic = kafka_api.create_topic(     
    TOPIC_NAME, SCHEMA_NAME, 1, replicas=3, partitions=8   
)   
fg_cc_ags = feature_store.create_feature_group(name="cc_trans_fg",     
    notification_topic_name=TOPIC_NAME,   
)
```
```   
kafka_api = project.get_kafka_api()   
my_schema = kafka_api.create_schema(SCHEMA_NAME, schema)   
my_topic = kafka_api.create_topic(     
    TOPIC_NAME, SCHEMA_NAME, 1, replicas=3, partitions=8   
)   
fg_cc_ags = feature_store.create_feature_group(name="cc_trans_fg",     
    notification_topic_name=TOPIC_NAME,   
)
```
Rows that are updated in the cc_trans_fg feature group are published to the Kafka topic (TOPIC_NAME), and consumers of the changes can subscribe to the Kafka topic to consume the rows that were updated. 
cc_trans_fg特徴グループで更新された行はKafkaトピック（TOPIC_NAME）に公開され、変更の消費者はKafkaトピックにサブスクライブして更新された行を取得できます。

###### Feature Views 特徴ビュー

As introduced in Chapter 4, feature views bridge the gap between feature groups and models by defining the model’s interface as a list of input features and output labels/ targets. 
第4章で紹介したように、特徴ビューは、モデルのインターフェースを入力特徴と出力ラベル/ターゲットのリストとして定義することによって、特徴グループとモデルのギャップを埋めます。

The main steps in creating and using feature views are: 
特徴ビューを作成し使用する主なステップは次のとおりです。

1. Selecting the features and labels/targets that will be used by your model 
1. モデルで使用される特徴とラベル/ターゲットを選択すること

2. Defining any MDTs you want to perform on your features 
2. 特徴に対して実行したいMDTを定義すること

3. Creating the feature view from your feature selection and MDTs 
3. 特徴選択とMDTから特徴ビューを作成すること

The main use cases for feature views are: 
特徴ビューの主な使用例は次のとおりです。

- Creating training data for your model 
- モデルのトレーニングデータを作成すること

- Creating batch inference data for your model 
- モデルのバッチ推論データを作成すること

- Creating online inference data for your model 
- モデルのオンライン推論データを作成すること

We will work with the credit card fraud example and use the feature view to create training and inference data for our model. 
私たちはクレジットカード詐欺の例を使い、特徴ビューを使用してモデルのトレーニングデータと推論データを作成します。

###### Feature Selection 特徴選択

When you want to create a model, you will need to select columns from feature groups that will be used by your model and also columns needed by the AI system— for example, for logging or for interacting with external systems. 
モデルを作成したい場合、モデルで使用される特徴グループから列を選択し、AIシステムに必要な列（たとえば、ログ記録や外部システムとの相互作用のため）を選択する必要があります。

Many of these selected columns will be features and labels/targets of your model, but you may also need helper columns for training and inference pipelines. 
これらの選択された列の多くは、モデルの特徴やラベル/ターゲットになりますが、トレーニングおよび推論パイプラインのための補助列も必要になる場合があります。

You create feature views by selecting and joining columns from feature groups, irrespective of whether the fea‐ ture groups are organized in a star schema or snowflake schema data model.  
特徴グループから列を選択して結合することで特徴ビューを作成します。特徴グループがスタースキーマまたはスノーフレークスキーマのデータモデルで整理されているかどうかに関係ありません。

When creating a feature view, you start by identifying the label feature group for your feature view. 
特徴ビューを作成する際は、まず特徴ビューのラベル特徴グループを特定します。

Each feature view has at most one label feature group containing the labels. 
各特徴ビューには、ラベルを含むラベル特徴グループが最大1つあります。

If you want to join features with your label feature group, your label feature group needs to have a foreign key to the feature group that contains those features. 
特徴をラベル特徴グループと結合したい場合、ラベル特徴グループはそれらの特徴を含む特徴グループへの外部キーを持つ必要があります。

In Chapter 10, we will look at how to add foreign keys to label feature groups, but for now, we will assume those foreign keys exist. 
第10章では、ラベル特徴グループに外部キーを追加する方法を見ていきますが、今のところはその外部キーが存在すると仮定します。

Any feature group that’s joined to the label feature group can, in turn, have foreign keys to other feature groups that can also be included in the feature selection. 
ラベル特徴グループに結合された特徴グループは、さらに他の特徴グループへの外部キーを持つことができ、それらも特徴選択に含めることができます。

You can also create a feature view without labels, for unsupervised learning, in which case the label feature group is just the root _feature group in a feature selection statement._ 
ラベルなしの特徴ビューを作成することもでき、これは教師なし学習の場合であり、その場合、ラベル特徴グループは特徴選択ステートメントのルート_特徴グループ_に過ぎません。

In our credit card fraud snowflake data model, `cc_num in` `cc_trans_fg is a foreign` key to cc_trans_aggs_fg. 
私たちのクレジットカード詐欺のスノーフレークデータモデルでは、`cc_num in` `cc_trans_fg`はcc_trans_aggs_fgへの外部キーです。

Similarly, merchant_id in cc_trans_fg is a foreign key to ``` merchant_fg. 
同様に、cc_trans_fgのmerchant_idは``` merchant_fgへの外部キーです。

We can also transitively include features from bank_fg and account_fg, as their primary keys are foreign keys in cc_trans_aggs_fg. 
また、bank_fgとaccount_fgからの特徴も推移的に含めることができ、これらの主キーはcc_trans_aggs_fgの外部キーです。

We start by getting references to those feature groups: 
私たちは、これらの特徴グループへの参照を取得することから始めます。

```   
labels = fs.get_feature_group("cc_trans_fg", version=1)   
aggs = fs.get_feature_group("cc_trans_aggs_fg", version=1)   
merchant = fs.get_feature_group("merchant_fg", version=1)   
bank = fs.get_feature_group("bank_fg", version=1)   
account = fs.get_feature_group("account_fg", version=1)
```
```   
labels = fs.get_feature_group("cc_trans_fg", version=1)   
aggs = fs.get_feature_group("cc_trans_aggs_fg", version=1)   
merchant = fs.get_feature_group("merchant_fg", version=1)   
bank = fs.get_feature_group("bank_fg", version=1)   
account = fs.get_feature_group("account_fg", version=1)
```
You specify which features to join by calling one of the select methods on a feature group: 
どの特徴を結合するかは、特徴グループのselectメソッドの1つを呼び出すことで指定します。

``` 
select_features()
```
``` 
select_features()
```
Selects all the feature columns (not index columns and foreign keys) 
すべての特徴列を選択します（インデックス列や外部キーは含まれません）。

``` 
select_all()
```
``` 
select_all()
```
Selects all the columns (including index columns and foreign keys) 
すべての列を選択します（インデックス列や外部キーを含む）。

``` 
select_except(['f1', 'f2', …])
```
``` 
select_except(['f1', 'f2', …])
```
Selects all the columns except those in the provided list 
提供されたリストに含まれないすべての列を選択します。

``` 
select(['f1', 'f2', …])
```
``` 
select(['f1', 'f2', …])
```
Selects only those columns in the provided list 
提供されたリストに含まれる列のみを選択します。

The `select methods return a` `Query object that represents the selection of features.` 
`select`メソッドは、特徴の選択を表す`Query`オブジェクトを返します。

You can read feature data with a Query object, add a filter to read a subset of feature data, inspect the query string used to read the feature data, and, most importantly, call `join() on it to join with other` `Query objects (that represent features selected` from other feature groups). 
`Query`オブジェクトを使用して特徴データを読み取り、特徴データのサブセットを読み取るためのフィルターを追加し、特徴データを読み取るために使用されるクエリ文字列を検査し、最も重要なこととして、他の特徴グループから選択された特徴を表す他の`Query`オブジェクトと結合するために`join()`を呼び出すことができます。

Here are the select and join methods that are used to create the selection of features (and the label) used in our credit card fraud model: 
以下は、私たちのクレジットカード詐欺モデルで使用される特徴（およびラベル）の選択を作成するために使用されるselectおよびjoinメソッドです。

```   
aggs_subtree = aggs.select_features()   
.join(bank.select_features())   
.join(account.select_features())
```
```   
aggs_subtree = aggs.select_features()   
.join(bank.select_features())   
.join(account.select_features())
```
```   
selection = labels.select_features()   
.join(merchant.select_features())   
.join(aggs_subtree)
```
```   
selection = labels.select_features()   
.join(merchant.select_features())   
.join(aggs_subtree)
```
In the preceding code, we do not specify any join key explicitly. 
前述のコードでは、明示的に結合キーを指定していません。

Hopsworks looks for the column(s) in the left-hand feature group with the same name and type as the pri‐ mary key in the right-hand (joined) feature group. 
Hopsworksは、左側の特徴グループにおいて、右側（結合された）特徴グループの主キーと同じ名前と型の列を探します。

If there is no match, you have to explicitly define the join key. 
一致がない場合は、結合キーを明示的に定義する必要があります。



. If there is no match, you have to explicitly define the join key. 
一致するものがない場合、結合キーを明示的に定義する必要があります。

For example, if the primary key of account_fg were id (instead of account_id), you would have to construct the join as follows: 
例えば、account_fgの主キーがid（account_idの代わりに）であった場合、結合は次のように構築する必要があります：

```   
aggs.select_features().join(bank.select_features(),   
left_on=["account_id"], right_on=["id"]) 
```
If there is a clash between feature names from the left and right feature groups (that is, if both feature groups have a feature with the same name), then in the `join` method, you can use the `prefix="abc_" parameter to add a prefix to the feature` names from the right-hand feature group. 
左側と右側の特徴グループからの特徴名が衝突する場合（つまり、両方の特徴グループに同じ名前の特徴がある場合）、`join`メソッドでは、`prefix="abc_"`パラメータを使用して右側の特徴グループからの特徴名にプレフィックスを追加できます。

###### Model-Dependent Transformations
###### モデル依存の変換

In Hopsworks, you can declaratively attach a transformation function to any of the selected features in your feature view. 
Hopsworksでは、フィーチャービュー内の選択された特徴のいずれかに変換関数を宣言的に添付できます。

The transformation functions are executed in the client after data has been read from the feature store with a feature view. 
変換関数は、フィーチャービューを使用してフィーチャーストアからデータが読み込まれた後、クライアントで実行されます。

As feature views are only used in training and inference pipelines, these transformation functions are MDTs. 
フィーチャービューはトレーニングおよび推論パイプラインでのみ使用されるため、これらの変換関数はMDTです。

You can either use built-in transformations (such as ``` min_max_scaler) or define your own custom transformation function, such as here: 
組み込みの変換（例えば、``` min_max_scaler）を使用するか、次のように独自のカスタム変換関数を定義できます：

```   
from hopsworks.transformation_statistics import TransformationStatistics   
@hopsworks.udf(float)   
def f1(amount, days_until_expired, stats: TransformationStatistics):     
return (amount * days_until_expired) / stats.amount.mean 
```
In this example, we can see that the transformation function is parameterized by the ``` TransformationStatistics object that contains statistics that were computed over features in a training dataset. 
この例では、変換関数がトレーニングデータセット内の特徴に対して計算された統計を含む``` TransformationStatisticsオブジェクトによってパラメータ化されていることがわかります。

The `TransformationStatistics object comes from a` training dataset object owned by the feature view—either it is a training dataset created by the feature view in a training pipeline or the feature view was initialized with the training dataset object in an inference pipeline. 
`TransformationStatisticsオブジェクトは、フィーチャービューが所有するトレーニングデータセットオブジェクトから来ます。これは、トレーニングパイプライン内でフィーチャービューによって作成されたトレーニングデータセットであるか、推論パイプライン内でトレーニングデータセットオブジェクトで初期化されたフィーチャービューです。

In this custom transformation, we use the mean of amount from the training dataset. 
このカスタム変換では、トレーニングデータセットからのamountの平均を使用します。

Transformation functions can be defined either as Python user-defined functions (UDFs) or Pandas UDFs. 
変換関数は、Pythonのユーザー定義関数（UDF）またはPandas UDFとして定義できます。

Pandas UDFs scale to process large data volumes (for example, in PySpark training dataset pipelines), but they add a small amount of latency in online inference pipelines. 
Pandas UDFは、大規模なデータボリュームを処理するためにスケールします（例えば、PySparkトレーニングデータセットパイプラインで）が、オンライン推論パイプラインではわずかな遅延を追加します。

Python UDFs, in contrast, scale poorly when data volumes increase, but they have lower latency in online inference pipelines. 
対照的に、Python UDFはデータボリュームが増加するとスケールが悪くなりますが、オンライン推論パイプラインでは遅延が少なくなります。



###### Creating Feature Views 特徴ビューの作成

Once you have selected your features and defined your MDTs, you can create a feature view as follows: 
特徴を選択し、MDTを定義したら、次のように特徴ビューを作成できます：

```  
feature_view = fs.create_feature_view(     
    name='cc_fraud',     
    query=selection,     
    labels=["is_fraud"],     
    transformation_functions = [ min_max_scaler("amount") ],     
    inference_helper_columns=['cc_expiry_date','prev_loc_transaction', 'prev_ts_transaction']   
)
```

You typically create a feature view for one model or a family of related models. 
通常、1つのモデルまたは関連するモデルのファミリーのために特徴ビューを作成します。

For example, if you have models for customers in different geographic regions, you could use the same feature view to represent the models for all of your customers and then apply filters when creating training data or batch inference data to only return the data for the model’s geographic region: 
たとえば、異なる地理的地域の顧客のためのモデルがある場合、同じ特徴ビューを使用してすべての顧客のモデルを表現し、トレーニングデータやバッチ推論データを作成する際にフィルターを適用して、モデルの地理的地域のデータのみを返すことができます：

```  
feature_view.training_data(extra_filter = account.region=="Europe")
```

When you use one or more filters to create training data, the filter or filters are stored as metadata in the training dataset object. 
トレーニングデータを作成するために1つ以上のフィルターを使用すると、フィルターはトレーニングデータセットオブジェクトのメタデータとして保存されます。

The model will apply the same filter(s) when you read batch inference data from a feature view that has been initialized with the same training dataset object. 
モデルは、同じトレーニングデータセットオブジェクトで初期化された特徴ビューからバッチ推論データを読み取るときに、同じフィルターを適用します。

Also, if you reproduce the training data using only metadata and the feature view, the filter(s) will be reapplied. 
また、メタデータと特徴ビューのみを使用してトレーニングデータを再現する場合、フィルターは再適用されます。

A feature view does not have a primary key; instead, it has _serving keys. 
特徴ビューには主キーはなく、_serving keys（サービングキー）があります。

When you use a feature view to retrieve one or more rows of features (which are called feature _vectors) via the online API, you have to provide values for the serving keys. 
特徴ビューを使用してオンラインAPI経由で1つ以上の特徴（特徴ベクトルと呼ばれる）を取得する場合、サービングキーの値を提供する必要があります。

The serving keys are the foreign keys in the label feature group for the feature view. 
サービングキーは、特徴ビューのラベル特徴グループの外部キーです。

In our credit card fraud example, the serving keys from `cc_trans_fg are` `cc_num and` 
私たちのクレジットカード詐欺の例では、`cc_trans_fg`からのサービングキーは`cc_num`と`merchant_id`です。

```  
merchant_id, as both of these foreign keys were used to create our feature view. 
これらの外部キーの両方が私たちの特徴ビューを作成するために使用されました。
```

You can inspect a feature view’s serving keys as follows: 
特徴ビューのサービングキーを次のように確認できます：

```  
print(feature_view.serving_keys)
```

Other parameters that can be provided when creating a feature view are 
特徴ビューを作成する際に提供できる他のパラメータは、

```  
training_helper_columns and inference_helper_columns. 
training_helper_columnsとinference_helper_columnsです。
```

Sometimes, during training or inference, you need helper columns that will not be used as features. 
時には、トレーニングや推論中に、特徴として使用されないヘルパーカラムが必要です。

For example, helper columns could be used as inputs to transformation functions, but they will not themselves be features. 
たとえば、ヘルパーカラムは変換関数への入力として使用される可能性がありますが、それ自体は特徴にはなりません。

In our credit card fraud system, we define three columns as inference_helper_columns, as they are all used as parameters in transformation functions used to compute on-demand features: 
私たちのクレジットカード詐欺システムでは、3つのカラムをinference_helper_columnsとして定義します。これらはすべて、オンデマンド機能を計算するために使用される変換関数のパラメータとして使用されます：

`haversine_distance,` 
`haversine_distance、`

```  
time_since_last_trans, and days_to_card_expiry. 
time_since_last_trans、days_to_card_expiryです。
```

When you read online inference data with the feature view, you will receive these columns and then use them to compute the on-demand features (they are parameters to the transformation functions).  
特徴ビューを使用してオンライン推論データを読み取ると、これらのカラムを受け取り、それを使用してオンデマンド機能を計算します（それらは変換関数のパラメータです）。

However, you will not include them as input parameters when calling `model.pre` 
ただし、`model.pre`を呼び出すときにそれらを入力パラメータとして含めることはありません。

```  
dict(). 
dict()です。
```

When you use the same feature view to read training data, fv.training_data(), it will not return the inference_helper_columns, as they are only needed 
同じ特徴ビューを使用してトレーニングデータを読み取ると、`fv.training_data()`はinference_helper_columnsを返しません。なぜなら、それらは推論時にのみ必要だからです（トレーニングパイプラインにはODT関数がありません）。

Similarly, training_helper_columns are returned when you create training data, but they are not 
同様に、トレーニングデータを作成するときにtraining_helper_columnsは返されますが、それらは返されません。

```  
returned when you read (batch or online) inference data. 
（バッチまたはオンラインの）推論データを読み取るときには返されません。
```

###### Training Data as Either DataFrames or Files トレーニングデータをDataFrameまたはファイルとして

With your feature view, you can read training data as Pandas DataFrames or create training data as files (see Table 5-3). 
特徴ビューを使用すると、トレーニングデータをPandas DataFramesとして読み取るか、ファイルとしてトレーニングデータを作成できます（表5-3を参照）。

_Table 5-3. Read training data as Pandas DataFrames or create training data as files_ 
**Feature view methods** **Output** **When to use** 
```  
fv.train_test_split(...) fv.training_data(...)
```

Pandas DataFrames using Arrow Flight Tabular data < 1-10 GB 
Arrow Flightを使用したPandas DataFrames タブularデータ < 1-10 GB 

Scikit-Learn or XGBoost 
Scikit-LearnまたはXGBoost

Tabular data > 1-10 GB 
タブularデータ > 1-10 GB 

PyTorch or TensorFlow 
PyTorchまたはTensorFlow
```  
fv.create_train_test_split(...) fv.create_training_data(...)
```

Training data as Parquet or CSV files in S3 or HopsFS 
S3またはHopsFSのParquetまたはCSVファイルとしてのトレーニングデータ



Assuming that there is enough available memory in your Python program and that your training data is under 10 GB in size, you can read training data directly into Pandas DataFrames. 
Pythonプログラムに十分なメモリがあり、トレーニングデータのサイズが10GB未満であると仮定すると、トレーニングデータを直接Pandas DataFramesに読み込むことができます。

If, however, your training data is larger (TBs or even PBs), you can run a training dataset pipeline program that creates training data and saves it as files in an output filesystem, like S3 or HopsFS on Hopsworks. 
しかし、トレーニングデータがより大きい（TBまたはPB）場合は、トレーニングデータを作成し、S3やHopsworksのHopsFSのような出力ファイルシステムにファイルとして保存するトレーニングデータセットパイプラインプログラムを実行できます。

The code to read, join, and save the training dataset files runs in PySpark. 
トレーニングデータセットファイルを読み込み、結合し、保存するコードはPySparkで実行されます。

You can run it directly in a PySpark program, but if you create training data as files from a Python program, it will launch a Spark job on Hopsworks on your behalf. 
PySparkプログラムで直接実行できますが、Pythonプログラムからファイルとしてトレーニングデータを作成すると、Hopsworks上であなたの代わりにSparkジョブが起動します。

The methods for creating training data as DataFrames or files have two versions: a `training_data() version` that outputs features and labels and a train_test_split() version that splits training data into a training set and a test set using a random or time-series split. 
DataFramesまたはファイルとしてトレーニングデータを作成するためのメソッドには2つのバージョンがあります：特徴とラベルを出力する`training_data()`バージョンと、トレーニングデータをランダムまたは時系列分割を使用してトレーニングセットとテストセットに分割するtrain_test_split()バージョンです。

###### Random, time-series, and stratified splits
###### ランダム、時系列、および層化分割

You can read your training data, split using a random split into training and test sets of features (X_) and labels (y_), as follows: 
トレーニングデータを読み込み、ランダム分割を使用して特徴（X_）とラベル（y_）のトレーニングセットとテストセットに分割できます。次のように：

```  
X_train, X_test, y_train, y_test = fv.train_test_split(test_size=0.2)
``` 

The preceding example gives you 80% of the data in the training set (X_train, y_train) and 20% in the test set (X_test, y_test). 
前の例では、トレーニングセット（X_train, y_train）にデータの80％、テストセット（X_test, y_test）に20％が与えられます。

Sometimes, you also need a validation set in addition to the training and test sets. 
時には、トレーニングセットとテストセットに加えて検証セットも必要です。

For example, if you want to perform hyperparameter tuning, you should not evaluate model performance using the test set (otherwise the test set can leak into model training). 
たとえば、ハイパーパラメータの調整を行いたい場合、テストセットを使用してモデルのパフォーマンスを評価すべきではありません（そうしないと、テストセットがモデルのトレーニングに漏れ込む可能性があります）。

Instead, you can create an additional validation set, on which you evaluate training runs with different hyperparameters:  
代わりに、異なるハイパーパラメータでトレーニングを評価するための追加の検証セットを作成できます：

```  
X_train, X_validation, X_test, y_train, y_validation, y_test = \     
fv.train_validation_test_split(validation_size=0.15, test_size=0.15)
``` 

In this case, the test set is the holdout set used to evaluate final model performance, after hyperparameter tuning is finished. 
この場合、テストセットはハイパーパラメータの調整が終了した後に最終モデルのパフォーマンスを評価するために使用されるホールドアウトセットです。

The same train_test_split and train_validation_test_split functions can also return a time-series split of your training data. 
同じtrain_test_splitおよびtrain_validation_test_split関数は、トレーニングデータの時系列分割も返すことができます。

As a rule, you should never create a random split of time-series data—as temporal patterns and trends get lost in randomization. 
一般的に、時系列データのランダム分割を作成すべきではありません。なぜなら、時間的パターンやトレンドがランダム化によって失われるからです。

Instead, specify a time range for each of your training, validation, and test sets. 
代わりに、トレーニング、検証、およびテストセットのそれぞれに対して時間範囲を指定します。

In the sample code that follows, the training set time window is from January 1 to 31, 2024, and the test data is the data that arrived between February 1 and 7, 2024: 
以下のサンプルコードでは、トレーニングセットの時間ウィンドウは2024年1月1日から31日までで、テストデータは2024年2月1日から7日までに到着したデータです：

```  
X_train, X_test, y_train, y_test = \     
fv.train_test_split(start_train_time="20240101", end_train_time="20240131",\       
start_test_time="20240201", end_test_time="20240207")
``` 

If you omit the `start_test_time`, the test set will start after the `end_train_time.` 
`start_test_time`を省略すると、テストセットは`end_train_time`の後から始まります。

Also, if you omit the end_test_time, the test set will include all data that arrived after February 1, 2024. 
また、`end_test_time`を省略すると、テストセットには2024年2月1日以降に到着したすべてのデータが含まれます。

Sometimes, you need a more sophisticated way to split your training data than a random or time-series split. 
時には、ランダムまたは時系列分割よりもトレーニングデータを分割するためのより洗練された方法が必要です。

For example, when predicting credit card fraud, you can train a binary classifier, but the positive class (fraud) is massively underrepresented compared with the negative class (no-fraud). 
たとえば、クレジットカードの不正を予測する場合、バイナリ分類器をトレーニングできますが、正のクラス（不正）は負のクラス（非不正）と比較して大幅に過小評価されています。

The imbalance ratio could be thousands to one or higher. 
不均衡比は千対一以上になる可能性があります。

There is a high risk when you split your data into training and test sets that the ratio of positive and negative classes will not be the same, which would result in poor evaluation of model performance, as the distribution of labels would not be the same in training and test sets. 
トレーニングセットとテストセットにデータを分割する際、正のクラスと負のクラスの比率が同じでないリスクが高く、これによりモデルのパフォーマンス評価が不十分になる可能性があります。なぜなら、ラベルの分布がトレーニングセットとテストセットで同じではないからです。

In this case, and in general if you have an imbalanced dataset, you should use a stratified split. 
この場合、また一般的に不均衡なデータセットを持っている場合は、層化分割を使用すべきです。

For this, you should read your training data as a single DataFrame and then implement the stratified split yourself using an appropriate library, such as scikit-learn, if needed: 
そのためには、トレーニングデータを単一のDataFrameとして読み込み、必要に応じてscikit-learnなどの適切なライブラリを使用して層化分割を自分で実装する必要があります：

```  
training_data = fv.training_data()   
# apply custom splits into training and test/validation sets
``` 

Supervised learning does not work well when the class distribution is skewed. 
教師あり学習は、クラス分布が偏っている場合にはうまく機能しません。

For binary classifiers, you should upsample or downsample one of the classes to improve balance between the classes. 
バイナリ分類器の場合、クラス間のバランスを改善するために、クラスの一方をアップサンプリングまたはダウンサンプリングする必要があります。

In Python, the imbalance library is widely used for up-/downsampling. 
Pythonでは、アップサンプリングおよびダウンサンプリングに不均衡ライブラリが広く使用されています。

If imbalance is too high, you may need to consider an alternative technique, such as anomaly detection with unsupervised learning instead of a binary classifier.  
不均衡があまりにも高い場合は、バイナリ分類器の代わりに教師なし学習による異常検出などの代替技術を検討する必要があるかもしれません。

###### Reproducible training data
###### 再現可能なトレーニングデータ

When you read training data as DataFrames or create training data as files, Hopsworks stores metadata about the training data created, including the feature view used, any filters used when creating training data, the training dataset ID, any random number seed, and the commit IDs for the feature groups that the training data was read from. 
トレーニングデータをDataFramesとして読み込むか、ファイルとしてトレーニングデータを作成すると、Hopsworksは作成されたトレーニングデータに関するメタデータを保存します。これには、使用された特徴ビュー、トレーニングデータを作成する際に使用されたフィルター、トレーニングデータセットID、任意の乱数シード、およびトレーニングデータが読み込まれた特徴グループのコミットIDが含まれます。

This way, you can delete the training data and Hopsworks can still reproduce that training data exactly, using only the training dataset ID: 
このようにして、トレーニングデータを削除しても、HopsworksはトレーニングデータセットIDのみを使用してそのトレーニングデータを正確に再現できます：

```  
X_train, X_test, y_train, y_test = fv.get_train_test_split(training_data_id=111)
``` 

Sometimes, you will need to delete training datasets due to storage costs or for compliance reasons (like your company’s data retention policies). 
時には、ストレージコストやコンプライアンスの理由（会社のデータ保持ポリシーなど）からトレーニングデータセットを削除する必要があります。

In these cases, the ability to accurately re-create training data is important. 
これらのケースでは、トレーニングデータを正確に再作成する能力が重要です。

###### Experiment Tracking and Reproducible Training Data
###### 実験追跡と再現可能なトレーニングデータ

Data science has aspired to be more science than engineering, with an emphasis on reproducibility and replicability as they are cornerstones of the scientific method. 
データサイエンスは、科学的手法の礎として再現性と複製性を重視し、工学よりも科学であることを目指してきました。

This has led to the growth in popularity of experiment tracking platforms that store hyperparameters from training runs and therefore enable models to be reproduced using experiment tracking metadata. 
これにより、トレーニング実行からのハイパーパラメータを保存し、実験追跡メタデータを使用してモデルを再現できる実験追跡プラットフォームの人気が高まっています。

Reproducible training data has received comparatively less attention, but it is now possible with feature stores and should grow in importance with the coming regulation of AI. 
再現可能なトレーニングデータは比較的少ない注目を受けていますが、特徴ストアを使用することで可能になり、AIの規制が進むにつれて重要性が増すべきです。

###### Batch Inference Data
###### バッチ推論データ

You can read batches of inference data from the offline store with a feature view. 
特徴ビューを使用して、オフラインストアから推論データのバッチを読み込むことができます。

A popular use case in batch inference pipelines is to read all new data that has arrived since the last time the batch inference pipeline ran: 
バッチ推論パイプラインでの一般的なユースケースは、バッチ推論パイプラインが最後に実行されて以来に到着したすべての新しいデータを読み込むことです：

```  
last_run_timestamp = "2024-05-10 00:01"   
fv = fs.get_feature_view(...)   
fv.init_batch_scoring(training_data_version=1)   
df = fv.get_batch_data(start_time=last_run_timestamp)   
df["prediction"] = model.predict(df)   
fv.log(df)
``` 

Here, we call init_batch_scoring on the feature view to tell it which training dataset version to use if it has to compute MDTs. 
ここでは、MDTを計算する必要がある場合に使用するトレーニングデータセットのバージョンを指定するために、特徴ビューでinit_batch_scoringを呼び出します。

In Chapter 11, we will see that you typically skip retrieving a pre-initialized feature view object from the model registry along with the model. 
第11章では、通常、モデルとともにモデルレジストリから事前初期化された特徴ビューオブジェクトを取得するのをスキップすることを示します。

This avoids potential skew between the training data version used to train the model and the version used here in the batch inference pipeline. 
これにより、モデルをトレーニングするために使用されたトレーニングデータのバージョンと、ここでバッチ推論パイプラインで使用されるバージョンとの間の潜在的な偏りを回避できます。

After we have a correctly initialized feature view, we read from the feature store a Pandas DataFrame, `df`, containing the transformed input feature data that arrived after `last_run_timestamp.` 
正しく初期化された特徴ビューを取得した後、特徴ストアからPandas DataFrame `df`を読み込み、`last_run_timestamp`以降に到着した変換された入力特徴データを含みます。

Finally, we make our predictions with the model on df  
最後に、df上のモデルで予測を行います。

(assuming the model can take a Pandas DataFrame as its input, which is possible for XGBoost and Scikit-Learn models). 
（モデルがPandas DataFrameを入力として受け取ることができると仮定します。これはXGBoostおよびScikit-Learnモデルで可能です）。

You can also log predictions and the feature values using fv.log(df). 
fv.log(df)を使用して予測と特徴値をログに記録することもできます。

Sometimes, you need more flexibility when reading batch inference data. 
時には、バッチ推論データを読み込む際により柔軟性が必要です。

For example, imagine you want to read the latest feature data for all entities (such as the latest transactions and fraud features for all credit cards) with your feature view. 
たとえば、特徴ビューを使用してすべてのエンティティ（すべてのクレジットカードの最新の取引や不正特徴など）の最新の特徴データを読み込みたいとします。

For this, you can use a Spine Group. 
そのためには、スパイングループを使用できます。

A Spine Group contains rows of serving keys for reading your features for your feature view, along with a timestamp value for every serving key. 
スパイングループは、特徴ビューの特徴を読み込むためのサービングキーの行と、各サービングキーのタイムスタンプ値を含みます。

It is called a spine because it is the structure around which the training data or batch inference data is built. 
スパインと呼ばれるのは、トレーニングデータやバッチ推論データが構築される構造だからです。

Spine Groups are only used in batch inference—they are not used in online inference. 
スパイングループはバッチ推論でのみ使用され、オンライン推論では使用されません。

A Spine Group can only be the label (or root) feature group in a feature view. 
スパイングループは、特徴ビュー内のラベル（またはルート）特徴グループである必要があります。

You can define a Spine Group as follows: 
スパイングループは次のように定義できます：

```  
trans_spine = fs.get_or_create_spine_group(     
name="cc_trans_spine_fg",     
…     
dataframe=trans_df   
)
``` 

Notice that you have to include a DataFrame, `trans_df`, to provide the schema for the feature group. 
特徴グループのスキーマを提供するために、DataFrame `trans_df`を含める必要があることに注意してください。

A Spine Group does not materialize any data to the feature store itself, and its data always needs to be provided when retrieving features for training or batch inference. 
スパイングループは、特徴ストア自体にデータを具現化せず、トレーニングやバッチ推論のために特徴を取得する際には常にそのデータを提供する必要があります。

You can think of it as a temporary feature group, to be replaced by a DataFrame when data is read from it. 
データがそこから読み込まれるときにDataFrameに置き換えられる一時的な特徴グループと考えることができます。

When you want to create training data with a feature view that contains a Spine Group as its label feature group, you can do so as follows: 
スパイングループをラベル特徴グループとして含む特徴ビューでトレーニングデータを作成したい場合は、次のようにできます：

```  
df = # (serving keys, timestamp for label values)   
X_train, X_test, y_train, y_test =   
feature_view.train_test_split(0.2, spine=df)
``` 

Similarly, for batch inference, you can read inference data as follows: 
同様に、バッチ推論の場合、推論データを次のように読み込むことができます：

```  
input_df = # (serving keys, timestamp for feature values)   
output_df = feature_view.get_batch_data(spine=input_df)   
predictions = model.predict(output_df)
``` 

If you can avoid Spine Groups, you should, as they add complexity and externalize much of the work for building training datasets and batch inference data to clients. 
スパイングループを避けることができる場合は、避けるべきです。なぜなら、スパイングループは複雑さを加え、トレーニングデータセットやバッチ推論データを構築するための多くの作業をクライアントに外部化するからです。

###### Online Inference Data
###### オンライン推論データ

Feature views are also used to retrieve rows of features from the online store at low latency. 
特徴ビューは、オンラインストアから低遅延で特徴の行を取得するためにも使用されます。

In our fraud example, the get_feature_vector() method call retrieves a row of precomputed features for a given credit card number (the serving key): 
私たちの不正の例では、get_feature_vector()メソッド呼び出しは、特定のクレジットカード番号（サービングキー）に対する事前計算された特徴の行を取得します：

```  
feature_vector = feature_view.get_feature_vector(entry={"cc_num":   "1234", "merchant_id": 4321}, return_type = "pandas")
```

The result, the feature vector, is returned as a Pandas DataFrame, but you can also read a NumPy array or list type (which is the default). 
結果である特徴ベクトルはPandas DataFrameとして返されますが、NumPy配列やリスト型（デフォルト）としても読み込むことができます。

There is also a version of this method call that retrieves many rows called get_feature_vectors, where the entry parameter is a list of serving keys. 
このメソッド呼び出しには、エントリパラメータがサービングキーのリストである多くの行を取得するget_feature_vectorsというバージョンもあります。

The transformation functions, introduced earlier, can also be used to define ODT functions 
以前に紹介した変換関数は、ODT関数を定義するためにも使用できます。



. For example, the on-demand days_to_card_expiry feature can be computed as follows: 
例えば、オンデマンドのdays_to_card_expiry機能は、次のように計算できます：

```   
@hopsworks.udf(int, mode="python", drop=["expiry_date"])   
def days_to_card_expiry(expiry_date):     
    return (datetime.today().date() - expiry_date.date()).days
``` 

この関数は、次のようにオンライン推論パイプラインで呼び出す必要があります：
You need to register ODTs with feature groups (see Chapter 7). 

```   
feature_vector = feature_view.get_feature_vector(     
    entry={"cc_num": "1234", "merchant_id": 4321}, return_type = "pandas")   
cc_expiry = days_to_card_expiry(feature_vector["expiry_date"])   
feature_vector = feature_vector.drop(columns=["expiry_date"])   
prediction = model.predict(feature_vector)
``` 

`expiry_date`は、推論ヘルパーカラムであるため、`feature_view.get_feature_vector()`を呼び出すと取得されません。
Note that `expiry_date will not be retrieved when you call` `feature_view.get_feature_vector(), as it is an inference helper column. 

推論ヘルパーカラムは、同じサービングキーを使用して`feature_view.inference_helpers()`を呼び出すことで取得できます。
Inference helper columns can be retrieved by calling feature_view.inference_helpers() with the same serving keys.

第11章では、MDTs、予測/特徴値のログ記録、特徴/モデルの監視を含むすべてのオンライン推論ステップをまとめます。
In Chapter 11, we will bring all online inference steps together, including MDTs, logging the prediction/feature values, and monitoring the features/models.

###### Faster Queries for Feature Data
特徴データの高速クエリ

We finish this chapter by looking at how to read feature data using filters. 
この章の最後では、フィルターを使用して特徴データを読み取る方法を見ていきます。

Applying filters can lead to huge performance improvements when reading a subset of feature data. 
フィルターを適用することで、特徴データのサブセットを読み取る際に大幅なパフォーマンス向上が得られます。

For example, in the offline store, when data volumes are large, if you first read large amounts of data into (Pandas or PySpark) DataFrames and then drop the columns and rows you do not need, you will incur huge overhead. 
例えば、オフラインストアでは、データ量が大きい場合、最初に大量のデータを（PandasまたはPySpark）DataFrameに読み込み、その後不要な列や行を削除すると、大きなオーバーヘッドが発生します。

It will either be very slow or may not work due to out-of-memory errors. 
非常に遅くなるか、メモリ不足エラーにより動作しない可能性があります。

The two main techniques for _data skipping (reducing the amount of data read in a query) are:_ 
データスキッピング（クエリで読み取るデータ量を減らす）に関する2つの主な技術は次のとおりです：

_Projection pushdown_ 
読み取る列のみをリクエストします。

_Pushdown filters_ 
提供するフィルタ値のデータのみを読み取ります。これには、パーティションのプルーニングと述語プッシュダウンの両方が含まれます。

When you read a subset of the features in a feature group and only the data for those features is returned to the client, it is known as _projection pushdown. 
特徴グループ内の特徴のサブセットを読み取り、その特徴のデータのみがクライアントに返される場合、これをプロジェクションプッシュダウンと呼びます。

Hopsworks



supports projection pushdown out of the box. 
プロジェクションプッシュダウンを標準でサポートしています。

When you define a feature view that only uses a subset of the features in a feature group, reads using that feature view will read with projection pushdown. 
フィーチャーグループ内の特徴のサブセットのみを使用するフィーチャービューを定義すると、そのフィーチャービューを使用した読み取りはプロジェクションプッシュダウンで行われます。

Both Hopsworks’ online feature store (RonDB) and its offline store (lakehouse tables) support projection pushdown. 
Hopsworksのオンラインフィーチャーストア（RonDB）とオフラインストア（レイクハウステーブル）は、プロジェクションプッシュダウンをサポートしています。

Online stores without projection pushdown—for example, Redis—require the client to read all of the columns in feature groups, and only in the client will it filter out the data it doesn’t need. 
プロジェクションプッシュダウンを持たないオンラインストア（例えば、Redis）は、クライアントがフィーチャーグループ内のすべての列を読み取る必要があり、クライアント内でのみ不要なデータをフィルタリングします。

Projection pushdown is particularly needed in cases such as when you have a wide feature group with many columns and a subset of those columns are used in many different models. 
プロジェクションプッシュダウンは、幅広いフィーチャーグループに多くの列があり、その列のサブセットが多くの異なるモデルで使用される場合に特に必要です。

When you read data with a feature view for training or batch inference, you can provide a filter such as: 
トレーニングやバッチ推論のためにフィーチャービューでデータを読み取るときは、次のようなフィルターを提供できます：

```   
X_features, y_labels = fv.training_data(extra_filter=fg.date=="2024-01-10")
``` 
```   
X_features, y_labels = fv.training_data(extra_filter=fg.date=="2024-01-10")
```

You can also read data directly from feature groups using filters: 
フィーチャーグループからフィルターを使用してデータを直接読み取ることもできます：

```   
df = fg.filter(fg.date > "2024-01-10").read()
``` 
```   
df = fg.filter(fg.date > "2024-01-10").read()
```

In the case where you have a feature view that contains features from multiple feature groups, you can chain filters that can all potentially be pushed down to the backing feature groups. 
複数のフィーチャーグループからの特徴を含むフィーチャービューがある場合、すべてのフィルターをチェーンして、バックフィーチャーグループにプッシュダウンできる可能性があります。

For example, assume we have a feature view that contains features from two feature groups. 
例えば、2つのフィーチャーグループからの特徴を含むフィーチャービューがあると仮定します。

The first feature group is partitioned by the date column, and the second one is partitioned by the country column. 
最初のフィーチャーグループは日付列でパーティション分けされ、2番目のフィーチャーグループは国列でパーティション分けされています。

In this case, we chain filter function calls. 
この場合、フィルタ関数呼び出しをチェーンします。

In the following feature view query, we use a Feature object to identify the features to filter on: 
次のフィーチャービュークエリでは、フィルタリングする特徴を特定するためにFeatureオブジェクトを使用します：

```   
df = fv.training_data( 
    extra_filter =     
    ( Feature("date")=="2024-01-10" and Feature("country") == "Ireland")   
)
``` 
```   
df = fv.training_data( 
    extra_filter =     
    ( Feature("date")=="2024-01-10" and Feature("country") == "Ireland")   
)
```

We already covered partitioning earlier, but we didn’t cover how to write filtered queries for multicolumn partition keys. 
私たちはすでにパーティショニングについて説明しましたが、マルチカラムパーティションキーのフィルタリングされたクエリの書き方については説明していませんでした。

For example, if you define two columns as your partition key, the order of the columns is important. 
例えば、2つの列をパーティションキーとして定義する場合、列の順序は重要です。

If you have `['date', 'country']` as the partition key, a query that filters for a given date (in the leftmost column), it will skip reading the files for rows that do not contain that date value. 
`['date', 'country']`をパーティションキーとして持っている場合、特定の日付（最も左の列）でフィルタリングするクエリは、その日付値を含まない行のファイルを読み取るのをスキップします。

It will, however, return data for all the countries for that date. 
ただし、その日付に対してすべての国のデータを返します。

If, however, you only filter by country and not by date, partition pruning won’t work. 
ただし、国でのみフィルタリングし、日付でフィルタリングしない場合、パーティションプルーニングは機能しません。

That’s because partition pruning follows the order of your partition keys: it can only prune based on the first key (date), not the second (country), unless the first is also specified. 
これは、パーティションプルーニングがパーティションキーの順序に従うためです：最初のキー（date）に基づいてのみプルーニングでき、2番目のキー（country）に基づいてはプルーニングできません。

The other type of _pushdown predicate that can reduce the amount of data read_ requires indexes on the underlying tables. 
データの読み取り量を減らすことができる別のタイプの_プッシュダウン述語_は、基盤となるテーブルにインデックスを必要とします。

In Hopsworks’ online store, RonDB supports user-defined indexes on columns. 
Hopsworksのオンラインストアでは、RonDBが列に対するユーザー定義インデックスをサポートしています。

These are B-tree-like indexes, optimized for in-memory layouts. 
これらはBツリーのようなインデックスで、メモリ内レイアウトに最適化されています。

In Hopsworks’ offline store, Apache Hudi tables support Z-ordered indexes and Delta Lake supports liquid clustering indexes. 
Hopsworksのオフラインストアでは、Apache HudiテーブルがZ順インデックスをサポートし、Delta Lakeが液体クラスタリングインデックスをサポートしています。

For offline queries, the Hopsworks Feature Query Service can leverage lakehouse table indexes to perform data skipping at both the Parquet file level and the row group level. 
オフラインクエリの場合、Hopsworksフィーチャークエリサービスはレイクハウステーブルインデックスを活用して、Parquetファイルレベルと行グループレベルの両方でデータスキップを実行できます。

These indexes use column-level statistics collected by the backing lakehouse table (for example, min/max column values for a Parquet file) to skip files when reading data and _zone maps in the Parquet file’s metadata to enable the reader to only fetch row_ groups with parameter values provided in the query. 
これらのインデックスは、データを読み取る際にファイルをスキップするために、バックのレイクハウステーブルによって収集された列レベルの統計（例えば、Parquetファイルの最小/最大列値）を使用し、_クエリで提供されたパラメータ値を持つ行_グループのみを取得できるようにするために、Parquetファイルのメタデータ内のゾーンマップを使用します。

Lakehouse tables store their data as Parquet files. 
レイクハウステーブルはデータをParquetファイルとして保存します。

Lakehouse tables can consist of thousands of Parquet files. 
レイクハウステーブルは数千のParquetファイルで構成されることがあります。

A well-designed feature pipeline will ensure that Parquet file sizes are uniform and of reasonable size (tens of MBs to a few GBs). 
適切に設計されたフィーチャーパイプラインは、Parquetファイルのサイズが均一で合理的なサイズ（数十MBから数GB）であることを保証します。

Having too many small files hurts query performance, as there are too many files to process. 
小さすぎるファイルが多すぎると、処理するファイルが多すぎるため、クエリパフォーマンスが低下します。

Having too few files or skewed file sizes results in inefficient data skipping during query execution. 
ファイルが少なすぎたり、ファイルサイズが偏っていると、クエリ実行中のデータスキップが非効率になります。

Hopsworks has table services that can run periodically to dynamically adjust file sizes and garbage-collect unused files. 
Hopsworksには、定期的に実行されてファイルサイズを動的に調整し、未使用のファイルをガーベジコレクトするテーブルサービスがあります。

###### Summary and Exercises 要約と演習

This chapter explores the Hopsworks Feature Store, emphasizing API calls to create and use both feature groups and feature views. 
この章では、Hopsworksフィーチャーストアを探求し、フィーチャーグループとフィーチャービューの両方を作成および使用するためのAPI呼び出しを強調します。

We started by looking at how to implement access control for feature data using Hopsworks projects and RBAC. 
私たちは、HopsworksプロジェクトとRBACを使用してフィーチャーデータのアクセス制御を実装する方法を見始めました。

We looked at the internals of the feature groups: the offline store (a lakehouse), online store (RonDB), and vector index(es). 
フィーチャーグループの内部（オフラインストア（レイクハウス）、オンラインストア（RonDB）、およびベクトルインデックス）を見ました。

We looked at how to create feature views and use them to create both training data and inference data. 
フィーチャービューを作成し、それを使用してトレーニングデータと推論データの両方を作成する方法を見ました。

Finally, we gave some advice on how to improve the performance of feature store queries using filters. 
最後に、フィルターを使用してフィーチャーストアクエリのパフォーマンスを向上させる方法についていくつかのアドバイスをしました。

The following exercises will help you learn how to get started on Hopsworks: 
次の演習は、Hopsworksの使い始め方を学ぶのに役立ちます：

- Create some synthetic data for two CSV files with an LLM (like ChatGPT), where the primary key for the second CSV file is also a column in the first CSV file. 
- LLM（ChatGPTのような）を使用して、2つのCSVファイルのための合成データを作成します。ここで、2番目のCSVファイルの主キーは、最初のCSVファイルの列でもあります。

Create two feature groups, one from each CSV file. 
各CSVファイルから1つずつ、2つのフィーチャーグループを作成します。

- Create a feature view that selects features from both feature groups you created. 
- あなたが作成した両方のフィーチャーグループから特徴を選択するフィーチャービューを作成します。

- Create training data with a random split. 
- ランダムスプリットでトレーニングデータを作成します。

- Add an event_time column to your original CSV files and make sure there are rows in both CSV files with the same join key values. 
- 元のCSVファイルにevent_time列を追加し、両方のCSVファイルに同じ結合キー値を持つ行があることを確認します。

Create two new feature groups and a feature view that uses features from both of them. 
2つの新しいフィーチャーグループと、それらの両方の特徴を使用するフィーチャービューを作成します。

Create training data with the feature view using a time-series split. 
時系列スプリットを使用してフィーチャービューでトレーニングデータを作成します。

###### PART III #### Data Transformations

###### PART III #### データ変換

