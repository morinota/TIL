refs: https://aihub.hkuspace.hku.hk/2024/02/14/amazon-sagemaker-feature-store-now-supports-cross-account-sharing-discovery-and-access/

# Amazon SageMaker Feature Store now supports cross-account sharing, discovery, and access
# Amazon SageMaker Feature Storeがクロスアカウント共有、発見、アクセスをサポートするようになりました

14 February, 2024  
2024年2月14日

Amazon SageMaker Feature Store is a fully managed, purpose-built repository to store, share, and manage features for machine learning (ML) models.  
Amazon SageMaker Feature Storeは、機械学習（ML）モデルのための特徴を保存、共有、管理するために特別に設計された完全管理型リポジトリです。
Features are inputs to ML models used during training and inference.  
特徴は、トレーニングと推論中に使用されるMLモデルへの入力です。
For example, in an application that recommends a music playlist, features could include song ratings, listening duration, and listener demographics. 
例えば、音楽プレイリストを推薦するアプリケーションでは、特徴には曲の評価、リスニング時間、リスナーの人口統計が含まれる可能性があります。
Features are used repeatedly by multiple teams, and feature quality is critical to ensure a highly accurate model.  
特徴は複数のチームによって繰り返し使用され、特徴の品質は高精度なモデルを確保するために重要です。
Also, when features used to train models offline in batch are made available for real-time inference, it’s hard to keep the two feature stores synchronized.  
**また、バッチでオフラインにモデルをトレーニングするために使用される特徴がリアルタイム推論のために利用可能になると、2つの特徴ストアを同期させるのが難しくなります**。

SageMaker Feature Store provides a secured and unified store to process, standardize, and use features at scale across the ML lifecycle.  
SageMaker Feature Storeは、MLライフサイクル全体で特徴を処理、標準化、使用するための安全で統一されたストアを提供します。
SageMaker Feature Store now makes it effortless to share, discover, and access feature groups across AWS accounts.  
**SageMaker Feature Storeは、AWSアカウント間で特徴グループを共有、発見、アクセスすることを容易にします**。
This new capability promotes collaboration and minimizes duplicate work for teams involved in ML model and application development, particularly in enterprise environments with multiple accounts spanning different business units or functions.  
この新機能は、MLモデルとアプリケーション開発に関与するチーム間のコラボレーションを促進し、特に異なるビジネスユニットや機能にまたがる複数のアカウントを持つ企業環境において、重複作業を最小限に抑えます。

With this launch, account owners can grant access to select feature groups by other accounts using AWS Resource Access Manager (AWS RAM).  
このリリースにより、**アカウント所有者はAWSリソースアクセスマネージャー（AWS RAM）を使用して、他のアカウントによる特定のfeature groupへのアクセスを許可できます**。
After they’re granted access, users of those accounts can conveniently view all of their feature groups, including the shared ones, through Amazon SageMaker Studio or SDKs.  
アクセスが許可されると、これらのアカウントのユーザーは、Amazon SageMaker Studioや**SDKを通じて**、共有されたものを含むすべての特徴グループを便利に表示できます。
This enables teams to discover and utilize features developed by other teams, fostering knowledge sharing and efficiency.  
これにより、チームは他のチームが開発した特徴を発見し、利用できるようになり、知識の共有と効率性が促進されます。
Additionally, usage details of shared resources can be monitored with Amazon CloudWatch and AWS CloudTrail.  
さらに、共有リソースの使用状況の詳細は、Amazon CloudWatchおよびAWS CloudTrailで監視できます。
For a deep dive, refer to Cross account feature group discoverability and access.  
詳細については、[クロスアカウント特徴グループの発見可能性とアクセス](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-cross-account.html)を参照してください。

In this post, we discuss the why and how of a centralized feature store with cross-account access.  
この記事では、**クロスアカウントアクセスを持つ中央集権的な特徴ストア**の理由と方法について説明します。
We show how to set it up and run a sample demonstration, as well as the benefits you can get by using this new capability in your organization.  
私たちは、これを設定し、サンプルデモを実行する方法、そしてこの新機能を組織で使用することによって得られる利点を示します。

<!-- ここまで読んだ! -->

## Who needs a cross-account feature store 誰がクロスアカウントフィーチャーストアを必要とするのか

Organizations need to securely share features across teams to build accurate ML models, while preventing unauthorized access to sensitive data. 
組織は、正確な機械学習（ML）モデルを構築するために、チーム間でフィーチャーを安全に共有する必要があり、同時に機密データへの不正アクセスを防ぐ必要があります。 
SageMaker Feature Store now allows granular sharing of features across accounts via AWS RAM, enabling collaborative model development with governance. 
SageMaker Feature Storeは、**AWS RAMを介してアカウント間でフィーチャーの詳細な共有**を可能にし、ガバナンスを伴う共同モデル開発を実現します。

- メモ: AWS RAMって?
  - AWS RAM(Resource Access Manager)は、AWSリソースを複数のアカウントで、簡単に&安全に共有するためのサービス。

SageMaker Feature Store provides purpose-built storage and management for ML features used during training and inferencing. 
SageMaker Feature Storeは、トレーニングおよび推論中に使用されるMLフィーチャーのために特別に設計されたストレージと管理を提供します。
With cross-account support, you can now selectively share features stored in one AWS account with other accounts in your organization. 
**クロスアカウントサポートにより、1つのAWSアカウントに保存されたフィーチャーを組織内の他のアカウントと選択的に共有できる**ようになりました。

For example, the analytics team may curate features like customer profile, transaction history, and product catalogs in a central management account. 
例えば、分析チームは、顧客プロファイル、取引履歴、製品カタログなどのフィーチャーを中央管理アカウントでキュレーションすることがあります。
These need to be securely accessed by ML developers in other departments like marketing, fraud detection, and so on to build models. 
これらは、マーケティング、詐欺検出などの他の部門のML開発者によって安全にアクセスされ、モデルを構築する必要があります。

The following are key benefits of sharing ML features across accounts: 
以下は、アカウント間でMLフィーチャーを共有することの主な利点です：

**Consistent and reusable features**– Centralized sharing of curated features improves model accuracy by providing consistent input data to train on. 
一貫性があり再利用可能なフィーチャー – キュレーションされたフィーチャーの中央集約的な共有は、一貫した入力データを提供することによりモデルの精度を向上させます。
Teams can discover and directly consume features created by others instead of duplicating them in each account. 
**チームは、各アカウントでフィーチャーを複製するのではなく、他の人が作成したフィーチャーを発見し、直接利用することができます**。

**Feature group access control**– You can grant access to only the specific feature groups required for an account’s use case. 
フィーチャーグループアクセス制御 – アカウントのユースケースに必要な特定のフィーチャーグループへのアクセスのみを付与できます。
For example, the marketing team may only get access to the customer profile feature group needed for recommendation models. 
例えば、マーケティングチームは、推薦モデルに必要な顧客プロファイルフィーチャーグループへのアクセスのみを得ることができます。

**Collaboration across teams**– Shared features allow disparate teams like fraud, marketing, and sales to collaborate on building ML models using the same reliable data instead of creating siloed features. 
チーム間のコラボレーション – 共有されたフィーチャーにより、詐欺、マーケティング、営業などの異なるチームが、孤立したフィーチャーを作成するのではなく、同じ信頼できるデータを使用してMLモデルを構築するために協力できます。

**Audit trail for compliance**– Administrators can monitor feature usage by all accounts centrally using CloudTrail event logs. 
コンプライアンスのための監査証跡 – 管理者は、CloudTrailイベントログを使用して**すべてのアカウントによるフィーチャーの使用状況を中央で監視**できます。
This provides an audit trail required for governance and compliance. 
これにより、ガバナンスとコンプライアンスに必要な監査証跡が提供されます。

## Delineating producers from consumers in cross-account feature stores　クロスアカウントフィーチャーストアにおける生産者と消費者の区別

In the realm of machine learning, the feature store acts as a crucial bridge, connecting those who supply data with those who harness it. 
機械学習の領域において、フィーチャーストアはデータを供給する者とそれを活用する者をつなぐ重要な架け橋として機能します。
This dichotomy can be effectively managed using a cross-account setup for the feature store. 
この二分法は、フィーチャーストアのクロスアカウント設定を使用することで効果的に管理できます。
Let’s demystify this using the following personas and a real-world analogy: 
以下のペルソナと実世界のアナロジーを用いて、これを明らかにしましょう：

- Data and ML engineers (owners and producers)– They lay the groundwork by feeding data into the feature store. データおよびMLエンジニア（所有者および生産者）– 彼らはデータをフィーチャーストアに供給することによって基盤を築きます。
- Data scientists (consumers)– They extract and utilize this data to craft their models. データサイエンティスト（消費者）– 彼らはこのデータを抽出し、モデルを作成するために利用します。

Data engineers serve as architects sketching the initial blueprint. 
データエンジニアは初期の設計図を描く建築家として機能します。
Their task is to construct and oversee efficient data pipelines. 
彼らの仕事は、効率的なデータパイプラインを構築し、監視することです。
Drawing data from source systems, they mold raw data attributes into discernable features. 
ソースシステムからデータを引き出し、生データ属性を認識可能な特徴に成形します。
Take “age” for instance. 
「年齢」を例にとりましょう。
Although it merely represents the span between now and one’s birthdate, its interpretation might vary across an organization. 
それは単に現在と誕生日の間の期間を表すだけですが、その解釈は組織によって異なる場合があります。
Ensuring quality, uniformity, and consistency is paramount here. 
ここで重要なのは、品質、一貫性、そして整合性を確保することです。
Their aim is to feed data into a centralized feature store, establishing it as the undisputed reference point. 
彼らの目標は、**データを中央のフィーチャーストアに供給し、それを疑いの余地のない参照点として確立すること**です。

ML engineers refine these foundational features, tailoring them for mature ML workflows. 
MLエンジニアはこれらの基盤となる特徴を洗練させ、成熟したMLワークフローに合わせて調整します。
In the context of banking, they might deduce statistical insights from account balances, identifying trends and flow patterns. 
銀行の文脈では、彼らは口座残高から統計的な洞察を導き出し、トレンドやフローパターンを特定するかもしれません。
The hurdle they often face is redundancy. 
彼らがしばしば直面する障害は冗長性です。
It’s common to see repetitive feature creation pipelines across diverse ML initiatives. 
さまざまなMLイニシアティブにおいて、繰り返しのフィーチャー作成パイプラインが見られるのは一般的です。

Imagine data scientists as gourmet chefs scouting a well-stocked pantry, seeking the best ingredients for their next culinary masterpiece. 
データサイエンティストを、次の料理の傑作のために最高の食材を探すグルメシェフとして想像してみてください。
Their time should be invested in crafting innovative data recipes, not in reassembling the pantry. 
彼らの時間は、パントリーを再構成するのではなく、革新的なデータレシピを作成することに投資されるべきです。
The hurdle at this juncture is discovering the right data. 
この時点での障害は、適切なデータを見つけることです。
A user-friendly interface, equipped with efficient search tools and comprehensive feature descriptions, is indispensable. 
**効率的な検索ツールと包括的なフィーチャー説明を備えたユーザーフレンドリーなインターフェース**は不可欠です。

In essence, a cross-account feature store setup meticulously segments the roles of data producers and consumers, ensuring efficiency, clarity, and innovation. 
本質的に、クロスアカウントフィーチャーストアの設定はデータ生産者と消費者の役割を綿密に分け、効率性、明確性、そして革新を確保します。
Whether you’re laying the foundation or building atop it, knowing your role and tools is pivotal. 
基盤を築くにせよ、その上に構築するにせよ、自分の役割とツールを知ることは重要です。

The following diagram shows two different data scientist teams, from two different AWS accounts, who share and use the same central feature store to select the best features needed to build their ML models. 
以下の図は、異なる2つのAWSアカウントからの異なるデータサイエンティストチームが、**同じ中央フィーチャーストアを共有し、MLモデルを構築するために必要な最良の特徴を選択する様子**を示しています。
The central feature store is located in a different account managed by data engineers and ML engineers, where the data governance layer and data lake are usually situated. 
中央フィーチャーストアは、データエンジニアとMLエンジニアによって管理される別のアカウントに位置しており、データガバナンス層とデータレイクが通常存在します。

<!-- ここまで読んだ! -->

## Cross-account feature group controls クロスアカウントフィーチャグループ制御

With SageMaker Feature Store, you can share feature group resources across accounts. 
SageMaker Feature Storeを使用すると、アカウント間でフィーチャグループリソースを共有できます。
The resource owner account shares resources with the resource consumer accounts. 
**リソースオーナーアカウントは、リソース消費者アカウントとリソースを共有**します。
(prodアカウントとdevアカウントの場合は、prodアカウントがリソースオーナーアカウント、devアカウントがリソース消費者アカウントにすれば良いかな...!:thinking:)
There are two distinct categories of permissions associated with sharing resources: 
**リソースを共有する際に関連する権限には、2つの異なるカテゴリ**があります。

Discoverability permissions–Discoverability means being able to see feature group names and metadata. 
発見可能性の権限 - 発見可能性とは、**フィーチャグループの名前やメタデータを見ることができること**を意味します。
When you grant discoverability permission, all feature group entities in the account that you share from (resource owner account) become discoverable by the accounts that you are sharing with (resource consumer accounts). 
発見可能性の権限を付与すると、共有元のアカウント（リソースオーナーアカウント）内のすべてのフィーチャグループエンティティが、共有先のアカウント（リソース消費者アカウント）によって発見可能になります。
For example, if you make the resource owner account discoverable by the resource consumer account, then principals of the resource consumer account can see all feature groups contained in the resource owner account. 
例えば、**リソースオーナーアカウントをリソース消費者アカウントから発見可能にすると、リソース消費者アカウントのプリンシパルはリソースオーナーアカウントに含まれるすべてのフィーチャグループを見ることができます**。(じゃあfeature group粒度ではなく、アカウント粒度で付与される権限なのかな...!)
This permission is granted to resource consumer accounts by using the SageMaker catalog resource type. 
この権限は、SageMakerカタログリソースタイプを使用してリソース消費者アカウントに付与されます。

Access permissions– When you grant an access permission, you do so at the feature group resource level (not the account level). 
アクセス権限 - アクセス権限を付与する場合、アカウントレベルではなくフィーチャグループリソースレベルで行います。
This gives you more granular control over granting access to data. 
これにより、データへのアクセスを付与する際に、より細かい制御が可能になります。
The type of access permissions that can be granted are read-only, read/write, and admin. 
**付与できるアクセス権限の種類には、読み取り専用、読み書き、管理者があります**。
For example, you can select only certain feature groups from the resource owner account to be accessible by principals of the resource consumer account, depending on your business needs. 
例えば、ビジネスニーズに応じて、リソースオーナーアカウントから特定のフィーチャグループのみをリソース消費者アカウントのプリンシパルがアクセスできるように選択できます。
This permission is granted to resource consumer accounts by using the feature group resource type and specifying feature group entities. 
この権限は、**フィーチャグループリソースタイプを使用し、フィーチャグループエンティティを指定する**ことでリソース消費者アカウントに付与されます。

The following example diagram visualizes sharing the SageMaker catalog resource type granting the discoverability permission vs. sharing a feature group resource type entity with access permissions. 
以下の例の図は、発見可能性の権限を付与するSageMakerカタログリソースタイプの共有と、アクセス権限を持つフィーチャグループリソースタイプエンティティの共有を視覚化しています。
The SageMaker catalog contains all of your feature group entities. 
SageMakerカタログには、すべてのフィーチャグループエンティティが含まれています。
When granted a discoverability permission, the resource consumer account can search and discover all feature group entities within the resource owner account. 
発見可能性の権限が付与されると、リソース消費者アカウントはリソースオーナーアカウント内のすべてのフィーチャグループエンティティを検索して発見できます。
A feature group entity contains your ML data. 
フィーチャグループエンティティには、あなたのMLデータが含まれています。
When granted an access permission, the resource consumer account can access the feature group data, with access determined by the relevant access permission. 
アクセス権限が付与されると、リソース消費者アカウントはフィーチャグループデータにアクセスでき、そのアクセスは関連するアクセス権限によって決定されます。

<!-- ここまで読んだ! -->

## Solution overview ソリューションの概要

Complete the following steps to securely share features between accounts using SageMaker Feature Store:
SageMaker Feature Storeを使用してアカウント間で機能を安全に共有するために、以下の手順を完了します。

In the source (owner) account, ingest datasets and prepare normalized features.
ソース（オーナー）アカウントで、データセットを取り込み、正規化された特徴量を準備します。
Organize related features into logical groups called feature groups.
関連する特徴量をfeature groupsと呼ばれる論理グループに整理します。
Create a resource share to grant cross-account access to specific feature groups.
特定のfeature groupsへのクロスアカウントアクセスを付与するために、**リソース共有**を作成します。
Define allowed actions like get and put, and restrict access only to authorized accounts.
getやputなどの許可されたアクションを定義し、アクセスを認可されたアカウントのみに制限します。
In the target (consumer) accounts, accept the AWS RAM invitation to access shared features.
**ターゲット（消費者）アカウントで、共有された特徴量にアクセスするためのAWS RAMの招待を受け入れます。**
Review the access policy to understand permissions granted.
付与された権限を理解するために、アクセスポリシーを確認します。

Developers in target accounts can now retrieve shared features using the SageMaker SDK, join with additional data, and use them to train ML models.
**ターゲットアカウントの開発者は、SageMaker SDKを使用して共有された特徴量を取得し**、追加データと結合し、それらを使用してMLモデルをトレーニングできます。
The source account can monitor access to shared features by all accounts using CloudTrail event logs.
ソースアカウントは、CloudTrailイベントログを使用して、すべてのアカウントによる共有機能へのアクセスを監視できます。
Audit logs provide centralized visibility into feature usage.
監査ログは、機能の使用状況に対する集中管理された可視性を提供します。

With these steps, you can enable teams across your organization to securely use shared ML features for collaborative model development.
これらの手順を実行することで、組織全体のチームが共同モデル開発のために安全に共有ML機能を使用できるようになります。

<!-- ここまで読んだ! -->

## Prerequisites 前提条件

We assume that you have already created feature groups and ingested the corresponding features inside your owner account. 
私たちは、あなたがすでにフィーチャーグループを作成し、対応するフィーチャーを所有者アカウント内に取り込んでいると仮定します。
For more information about getting started, refer to Get started with Amazon SageMaker Feature Store.
始めるための詳細については、「[Amazon SageMaker Feature Storeの使い始め](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-getting-started.html)」を参照してください。

<!-- ここまで読んだ! -->

## Grant discoverability permissions 発見可能性の権限を付与する

First, we demonstrate how to share our SageMaker Feature Store catalog in the owner account. 
まず、オーナーアカウントでSageMaker Feature Storeカタログを共有する方法を示します。
Complete the following steps: 
次の手順を完了してください：

In the owner account of the SageMaker Feature Store catalog, open the AWS RAM console. 
SageMaker Feature Storeカタログのオーナーアカウントで、AWS RAMコンソールを開きます。
Under Shared by me in the navigation pane, choose Resource shares. 
ナビゲーションペインの「私が共有した」セクションで、「リソース共有」を選択します。
Choose Create resource share. 
「リソース共有の作成」を選択します。
Enter a resource share name and choose SageMaker Resource Catalogs as the resource type. 
リソース共有名を入力し、リソースタイプとして「SageMakerリソースカタログ」を選択します。

Choose Next. 
「次へ」を選択します。
For discoverability-only access, enter AWS RAM Permission SageMaker Catalog Resource Search for Managed permissions. 
発見可能性のみのアクセスのために、管理された権限として「AWS RAM Permission SageMaker Catalog Resource Search」を入力します。

Choose Next. 
「次へ」を選択します。
Enter your consumer account ID and choose Add. 
消費者アカウントIDを入力し、「追加」を選択します。
You may add several consumer accounts. 
複数の消費者アカウントを追加できます。

Choose Next and complete your resource share. 
「次へ」を選択し、リソース共有を完了します。

Now the shared SageMaker Feature Store catalog should show up on the Resource shares page. 
これで、共有されたSageMaker Feature Storeカタログが「リソース共有」ページに表示されるはずです。

You can achieve the same result by using the AWS Command Line Interface (AWS CLI) with the following command (provide your AWS Region, owner account ID, and consumer account ID): 
同じ結果を得るには、次のコマンドを使用してAWSコマンドラインインターフェース（AWS CLI）を利用できます（AWSリージョン、オーナーアカウントID、および消費者アカウントIDを指定してください）：

```shell
aws ram create-resource-share
–name MyCatalogFG
–resource-arns arn:aws:sagemaker:REGION:OWNERACCOUNTID:sagemaker-catalog/DefaultFeatureGroupCatalog
–principals CONSACCOUNTID
–permission-arns arn:aws:ram::aws:permission/AWSRAMPermissionSageMakerCatalogResourceSearch
```

<!-- ここまで読んだ! -->

## Accept the resource share invite リソース共有招待の受け入れ

To accept the resource share invite, complete the following steps:
リソース共有招待を受け入れるには、以下の手順を完了してください。

In the target (consumer) account, open the AWS RAM console.
ターゲット（消費者）アカウントで、AWS RAMコンソールを開きます。
Under Shared with me in the navigation pane, choose Resource shares.
ナビゲーションペインの「私と共有された」セクションで、「リソース共有」を選択します。

Choose the new pending resource share.
新しい保留中のリソース共有を選択します。

Choose Accept resource share.
「リソース共有を受け入れる」を選択します。

You can achieve the same result using the AWS CLI with the following command:
次のコマンドを使用して、同じ結果をAWS CLIで達成できます。

```shell
aws ram get-resource-share-invitations
```

From the output of preceding command, retrieve the value of resourceShareInvitationArn and then accept the invitation with the following command:
前のコマンドの出力から、resourceShareInvitationArnの値を取得し、次のコマンドで招待を受け入れます。

```shell
aws ram accept-resource-share-invitation
–resource-share-invitation-arn RESOURCESHAREINVITATIONARN
```

The workflow is the same for sharing feature groups with another account via AWS RAM.
AWS RAMを介して別のアカウントとフィーチャーグループを共有する場合も、ワークフローは同じです。

After you share some feature groups with the target account, you can inspect the SageMaker Feature Store, where you can observe that the new catalog is available.
ターゲットアカウントといくつかのフィーチャーグループを共有した後、SageMaker Feature Storeを確認すると、新しいカタログが利用可能であることがわかります。

<!-- ここまで読んだ! -->

## Grant access permissions アクセス権限の付与

With access permissions, we can grant permissions at the feature group resource level. 
アクセス権限を使用することで、フィーチャーグループリソースレベルで権限を付与できます。
Complete the following steps: 
次の手順を完了してください：

In the owner account of the SageMaker Feature Store catalog, open the AWS RAM console. 
SageMaker Feature Storeカタログのオーナーアカウントで、AWS RAMコンソールを開きます。
Under Shared by me in the navigation pane, choose Resource shares. 
ナビゲーションペインの「私が共有した」セクションで、「リソース共有」を選択します。
Choose Create resource share. 
「リソース共有の作成」を選択します。
Enter a resource share name and choose SageMaker Feature Groups as the resource type. 
リソース共有名を入力し、リソースタイプとして「SageMaker Feature Groups」を選択します。
Select one or more feature groups to share. 
**共有するフィーチャーグループを1つ以上選択**します。

Choose Next. 
「次へ」を選択します。
For read/write access, enter AWSRAMPermissionSageMakerFeatureGroupReadWrite for Managed permissions. 
読み書きアクセスのために、**Managed permissionsとして「AWSRAMPermissionSageMakerFeatureGroupReadWrite」を入力**します。

Choose Next. 
「次へ」を選択します。
Enter your consumer account ID and choose Add. 
消費者アカウントIDを入力し、「追加」を選択します。
You may add several consumer accounts. 
**複数の消費者アカウントを追加できます。**

Choose Next and complete your resource share. 
「次へ」を選択し、リソース共有を完了します。

Now the shared catalog should show up on the Resource shares page. 
これで、共有カタログが「リソース共有」ページに表示されるはずです。

You can achieve the same result by using the AWS CLI with the following command (provide your Region, owner account ID, consumer account ID, and feature group name): 
次のコマンドを使用してAWS CLIで同じ結果を得ることができます（リージョン、オーナーアカウントID、消費者アカウントID、およびフィーチャーグループ名を指定してください）：

```shell
aws ram create-resource-share
–name MyCatalogFG
–resource-arns arn:aws:sagemaker:REGION:OWNERACCOUNTID:feature-group/FEATUREGROUPNAME
–principals CONSACCOUNTID
–permission-arns arn:aws:ram::aws:permission/AWSRAMPermissionSageMakerFeatureGroupReadWrite
```

There are three types of access that you can grant to feature groups: 
フィーチャーグループに付与できるアクセス権の種類は3つあります：

- AWSRAMPermissionSageMakerFeatureGroupReadOnly – The read-only privilege allows resource consumer accounts to read records in the shared feature groups and view details and metadata 
`AWSRAMPermissionSageMakerFeatureGroupReadOnly` – 読み取り専用の特権により、リソース消費者アカウントは共有フィーチャーグループ内のレコードを読み取り、詳細およびメタデータを表示できます。

- AWSRAMPermissionSageMakerFeatureGroupReadWrite – The read/write privilege allows resource consumer accounts to write records to, and delete records from, the shared feature groups, in addition to read permissions 
`AWSRAMPermissionSageMakerFeatureGroupReadWrite` – 読み書きの特権により、リソース消費者アカウントは共有フィーチャーグループにレコードを書き込み、レコードを削除することができ、読み取り権限に加えて利用できます。

AWSRAMPermissionSagemakerFeatureGroupAdmin – The admin privilege allows the resource consumer accounts to update the description and parameters of features within the shared feature groups and update the configuration of the shared feature groups, in addition to read/write permissions 
`AWSRAMPermissionSagemakerFeatureGroupAdmin` – 管理者の特権により、リソース消費者アカウントは共有フィーチャーグループ内のフィーチャーの説明やパラメータを更新し、共有フィーチャーグループの構成を更新することができ、読み書き権限に加えて利用できます。

<!-- ここまで読んだ! -->

## Accept the resource share invite リソース共有招待の受け入れ

To accept the resource share invite, complete the following steps:
リソース共有招待を受け入れるには、以下の手順を完了してください。

In the target (consumer) account, open the AWS RAM console.
ターゲット（コンシューマ）アカウントで、AWS RAMコンソールを開きます。
Under Shared with me in the navigation pane, choose Resource shares.
ナビゲーションペインの「Shared with me」から「Resource shares」を選択します。
Choose the new pending resource share.
新しい保留中のリソース共有を選択します。

Choose Accept resource share.
「Accept resource share」を選択します。

The process of accepting the resource share using the AWS CLI is the same as for the previous discoverability section, with the get-resource-share-invitations and accept-resource-share-invitation commands.
AWS CLIを使用してリソース共有を受け入れるプロセスは、前の発見可能性セクションと同様で、get-resource-share-invitationsおよびaccept-resource-share-invitationコマンドを使用します。

<!-- ここまで読んだ! -->

## Sample notebooks showcasing this new capability 新機能を示すサンプルノートブック

Two notebooks were added to the SageMaker Feature Store Workshop GitHub repository in the folder 09-module-security/09-03-cross-account-access:
2つのノートブックがSageMaker Feature Store WorkshopのGitHubリポジトリのフォルダ09-module-security/09-03-cross-account-accessに追加されました：

m9_03_nb1_cross-account-admin.ipynb– This needs to be launched on your admin or owner AWS account
m9_03_nb1_cross-account-admin.ipynb – これはあなたの管理者またはオーナーのAWSアカウントで起動する必要があります。

m9_03_nb2_cross-account-consumer.ipynb– This needs to be launched on your consumer AWS account
m9_03_nb2_cross-account-consumer.ipynb – これはあなたの消費者AWSアカウントで起動する必要があります。

The first script shows how to create the discoverability resource share for existing feature groups at the admin or owner account and share it with another consumer account programmatically using the AWS RAM API create_resource_share().
最初のスクリプトは、管理者またはオーナーアカウントの既存のフィーチャーグループの発見可能性リソース共有を作成し、AWS RAM APIのcreate_resource_share()を使用して別の消費者アカウントとプログラム的に共有する方法を示しています。
It also shows how to grant access permissions to existing feature groups at the owner account and share these with another consumer account using AWS RAM.
また、オーナーアカウントの既存のフィーチャーグループにアクセス権限を付与し、これをAWS RAMを使用して別の消費者アカウントと共有する方法も示しています。
You need to provide your consumer AWS account ID before running the notebook.
ノートブックを実行する前に、あなたの消費者AWSアカウントIDを提供する必要があります。

The second script accepts the AWS RAM invitations to discover and access cross-account feature groups from the owner level.
2番目のスクリプトは、オーナーレベルからクロスアカウントフィーチャーグループを発見しアクセスするためのAWS RAMの招待を受け入れます。
Then it shows how to discover cross-account feature groups that are on the owner account and list these on the consumer account.
次に、オーナーアカウントにあるクロスアカウントフィーチャーグループを発見し、これを消費者アカウントにリストする方法を示します。
You can also see how to access in read/write cross-account feature groups that are on the owner account and perform the following operations from the consumer account: describe(), get_record(), ingest(), and delete_record().
**また、オーナーアカウントにある読み書き可能なクロスアカウントフィーチャーグループにアクセスし、消費者アカウントから次の操作を実行する方法も確認できます**：describe()、get_record()、ingest()、およびdelete_record()。
(Athenaによるpoint-in-time correct joinもたぶんできるってことだよね??:thinking:)

<!-- ここまで読んだ! -->

## Conclusion 結論

The SageMaker Feature Store cross-account capability offers several compelling benefits. 
SageMaker Feature Storeのクロスアカウント機能は、いくつかの魅力的な利点を提供します。
Firstly, it facilitates seamless collaboration by enabling sharing of feature groups across multiple AWS accounts. 
まず、複数のAWSアカウント間でフィーチャーグループを共有できることで、シームレスなコラボレーションを促進します。
This enhances data accessibility and utilization, allowing teams in different accounts to use shared features for their ML workflows. 
これによりデータのアクセス性と利用が向上し、異なるアカウントのチームが共有されたフィーチャーをMLワークフローで使用できるようになります。

Additionally, the cross-account capability enhances data governance and security. 
さらに、クロスアカウント機能はデータガバナンスとセキュリティを強化します。
With controlled access and permissions through AWS RAM, organizations can maintain a centralized feature store while ensuring that each account has tailored access levels. 
**AWS RAMを通じて制御されたアクセスと権限を持つことで、組織は中央集権的なフィーチャーストアを維持しつつ、各アカウントに合わせたアクセスレベルを確保できます**。
This not only streamlines data management, but also strengthens security measures by limiting access to authorized users. 
これはデータ管理を効率化するだけでなく、認可されたユーザーへのアクセスを制限することでセキュリティ対策を強化します。

Furthermore, the ability to share feature groups across accounts simplifies the process of building and deploying ML models in a collaborative environment. 
さらに、アカウント間でフィーチャーグループを共有できることで、コラボレーティブな環境でのMLモデルの構築と展開のプロセスが簡素化されます。
It fosters a more integrated and efficient workflow, reducing redundancy in data storage and facilitating the creation of robust models with shared, high-quality features. 
これにより、より統合された効率的なワークフローが促進され、データストレージの冗長性が減少し、共有された高品質のフィーチャーを用いた堅牢なモデルの作成が容易になります。
Overall, the Feature Store’s cross-account capability optimizes collaboration, governance, and efficiency in ML development across diverse AWS accounts. 
全体として、Feature Storeのクロスアカウント機能は、さまざまなAWSアカウントにおけるML開発のコラボレーション、ガバナンス、効率を最適化します。
Give it a try, and let us know what you think in the comments. 
ぜひお試しください。コメントでご意見をお聞かせください。

<!-- ここまで読んだ! -->

### About the Authors 著者について

Ioan Catanais a Senior Artificial Intelligence and Machine Learning Specialist Solutions Architect at AWS. 
Ioan Catanaisは、AWSのシニア人工知能および機械学習スペシャリストソリューションアーキテクトです。
He helps customers develop and scale their ML solutions in the AWS Cloud. 
彼は顧客がAWSクラウドでMLソリューションを開発し、スケールさせるのを支援しています。
Ioan has over 20 years of experience, mostly in software architecture design and cloud engineering. 
Ioanは20年以上の経験があり、主にソフトウェアアーキテクチャ設計とクラウドエンジニアリングに従事しています。

Philipp Kaindlis a Senior Artificial Intelligence and Machine Learning Solutions Architect at AWS. 
Philipp Kaindlは、AWSのシニア人工知能および機械学習ソリューションアーキテクトです。
With a background in data science and mechanical engineering, his focus is on empowering customers to create lasting business impact with the help of AI. 
データサイエンスと機械工学のバックグラウンドを持つ彼の焦点は、顧客がAIの助けを借りて持続的なビジネスインパクトを生み出すことを支援することです。
Outside of work, Philipp enjoys tinkering with 3D printers, sailing, and hiking. 
仕事の外では、Philippは3Dプリンターでの作業、セーリング、ハイキングを楽しんでいます。

Dhaval Shahis a Senior Solutions Architect at AWS, specializing in machine learning. 
Dhaval Shahは、AWSのシニアソリューションアーキテクトで、機械学習を専門としています。
With a strong focus on digital native businesses, he empowers customers to use AWS and drive their business growth. 
デジタルネイティブビジネスに強く焦点を当て、彼は顧客がAWSを利用してビジネスの成長を促進するのを支援しています。
As an ML enthusiast, Dhaval is driven by his passion for creating impactful solutions that bring positive change. 
ML愛好者として、Dhavalはポジティブな変化をもたらす影響力のあるソリューションを創造する情熱に駆り立てられています。
In his leisure time, he indulges in his love for travel and cherishes quality moments with his family. 
余暇の時間には、旅行を楽しみ、家族との質の高い瞬間を大切にしています。

Mizanur Rahmanis a Senior Software Engineer for Amazon SageMaker Feature Store with over 10 years of hands-on experience specializing in AI and ML. 
Mizanur Rahmanは、AIとMLを専門とするAmazon SageMaker Feature Storeのシニアソフトウェアエンジニアで、10年以上の実務経験を持っています。
With a strong foundation in both theory and practical applications, he holds a Ph.D. in Fraud Detection using Machine Learning, reflecting his dedication to advancing the field. 
理論と実践の両方に強固な基盤を持ち、彼は機械学習を用いた不正検出に関する博士号を取得しており、分野の進展に対する彼の献身を反映しています。
His expertise spans a broad spectrum, encompassing scalable architectures, distributed computing, big data analytics, micro services and cloud infrastructures for organizations. 
彼の専門知識は、スケーラブルなアーキテクチャ、分散コンピューティング、ビッグデータ分析、マイクロサービス、組織のためのクラウドインフラストラクチャにわたります。

<!-- ここまで読んだ! -->
