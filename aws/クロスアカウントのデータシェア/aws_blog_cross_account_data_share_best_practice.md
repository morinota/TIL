refs: https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account-notes.html

# Cross-account data sharing best practices and considerations
# クロスアカウントデータ共有のベストプラクティスと考慮事項

Lake Formation cross-account capabilities allow users to securely share distributed data lakes across multiple AWS accounts, AWS organizations or directly with IAM principals in another account providing fine-grained access to the Data Catalog metadata and underlying data.
**Lake Formationのクロスアカウント機能**により、ユーザーは複数のAWSアカウント、AWS組織間、または別のアカウントのIAMプリンシパルと直接、安全に分散データレイクを共有し、Data Catalogメタデータおよび基盤データへの細かいアクセスを提供します。

Consider the following best practices when using Lake Formation cross-account data sharing:
Lake Formationのクロスアカウントデータ共有を使用する際は、以下のベストプラクティスを考慮してください：

- There is no limit to the number of Lake Formation permission grants that you can make to principals in your own AWS account. 
- 自分のAWSアカウント内のプリンシパルに対して行えるLake Formationの権限付与の数に制限はありません。
    However, Lake Formation uses AWS Resource Access Manager (AWS RAM) capacity for cross-account grants that your account can make with the named resource method. 
    しかし、Lake Formationは、指定されたリソースメソッドを使用して、アカウントが行うクロスアカウントの権限付与にAWSリソースアクセスマネージャー（AWS RAM）の容量を使用します。
    To maximize the AWS RAM capacity, follow these best practices for the named resource method:
    AWS RAMの容量を最大化するために、指定されたリソースメソッドに関する以下のベストプラクティスに従ってください：

    - Use the new cross-account grant mode (Version 3 and above under Cross account version settings) to share a resource with an external AWS account. 
    新しいクロスアカウント権限付与モード（バージョン3以上、クロスアカウントバージョン設定の下）を使用して、外部AWSアカウントとリソースを共有します。
    For more information, see Updating cross-account data sharing version settings.
    詳細については、クロスアカウントデータ共有バージョン設定の更新を参照してください。

    - Arrange AWS accounts into organizations, and grant permissions to organizations or organizational units. 
    AWSアカウントを組織に整理し、組織または組織単位に権限を付与します。
    A grant to an organization or organizational unit counts as one grant.
    組織または組織単位への権限付与は1つの権限付与としてカウントされます。
    Granting to organizations or organizational units also eliminates the need to accept an AWS Resource Access Manager (AWS RAM) resource share invitation for the grant.
    組織または組織単位への権限付与は、権限付与のためにAWSリソースアクセスマネージャー（AWS RAM）のリソース共有招待を受け入れる必要を排除します。
    For more information, see Accessing and viewing shared Data Catalog tables and databases.
    詳細については、共有されたData Catalogテーブルおよびデータベースへのアクセスと表示を参照してください。

- Instead of granting permissions on many individual tables in a database, use the special All tables wildcard to grant permissions on all tables in the database. 
- データベース内の多くの個別テーブルに権限を付与するのではなく、特別なAll tablesワイルドカードを使用してデータベース内のすべてのテーブルに権限を付与します。

Granting on All tables counts as a single grant.
All tablesに対する権限付与は1つの権限付与としてカウントされます。

For more information, see Granting permissions on Data Catalog resources.
詳細については、Data Catalogリソースへの権限付与を参照してください。

Note For more information about requesting a higher limit for the number of resource shares in AWS RAM, see AWS service quotas in the AWS General Reference.
注：AWS RAMにおけるリソース共有の数の上限を引き上げるリクエストに関する詳細は、AWS一般リファレンスのAWSサービスクォータを参照してください。

- You must create a resource link to a shared database for that database to appear in the Amazon Athena and Amazon Redshift Spectrum query editors. 
- 共有データベースがAmazon AthenaおよびAmazon Redshift Spectrumのクエリエディタに表示されるようにするには、リソースリンクを作成する必要があります。

Similarly, to be able to query shared tables using Athena and Redshift Spectrum, you must create resource links to the tables.
同様に、AthenaおよびRedshift Spectrumを使用して共有テーブルをクエリするには、テーブルへのリソースリンクを作成する必要があります。

The resource links then appear in the tables list of the query editors.
リソースリンクは、その後、クエリエディタのテーブルリストに表示されます。

Instead of creating resource links for many individual tables for querying, you can use the All tables wildcard to grant permissions on all tables in a database.
多くの個別テーブルのクエリ用にリソースリンクを作成するのではなく、All tablesワイルドカードを使用してデータベース内のすべてのテーブルに権限を付与できます。

Then, when you create a resource link for that database and select that database resource link in the query editor, you'll have access to all tables in that database for your query.
その後、そのデータベースのリソースリンクを作成し、クエリエディタでそのデータベースリソースリンクを選択すると、そのデータベース内のすべてのテーブルに対してクエリを実行できます。

For more information, see Creating resource links.
詳細については、リソースリンクの作成を参照してください。

- When you share resources directly with principals in another account, the IAM principal in the recipient account may not have permission to create resource links to be able to query the shared tables using Athena and Amazon Redshift Spectrum. 
- 別のアカウントのプリンシパルとリソースを直接共有する場合、受取アカウントのIAMプリンシパルは、AthenaおよびAmazon Redshift Spectrumを使用して共有テーブルをクエリするためのリソースリンクを作成する権限を持っていない可能性があります。

Instead of creating a resource link for each table that is shared, the data lake administrator can create a placeholder database and grant CREATE_TABLE permission to the ALL IAM Principal group.
共有される各テーブルのリソースリンクを作成する代わりに、データレイク管理者はプレースホルダーデータベースを作成し、ALL IAM PrincipalグループにCREATE_TABLE権限を付与できます。

Then, all IAM principals in the recipient account can create resource links in the placeholder database and start querying the shared tables.
その後、受取アカウント内のすべてのIAMプリンシパルはプレースホルダーデータベース内にリソースリンクを作成し、共有テーブルをクエリし始めることができます。

See the example CLI command for granting permissions to ALL IAM Principals in Granting database permissions using the named resource method.
指定されたリソースメソッドを使用してデータベース権限を付与する際のALL IAM Principalsへの権限付与の例CLIコマンドを参照してください。

- When cross-account permissions are granted directly to a principal, only the recipient of the grant can view these permissions. 
- クロスアカウント権限がプリンシパルに直接付与されると、権限の受取人のみがこれらの権限を表示できます。

The data lake administrator in the recipient's AWS account cannot view these direct grants.
受取人のAWSアカウント内のデータレイク管理者は、これらの直接的な権限付与を表示できません。

- Athena and Redshift Spectrum support column-level access control, but only for inclusion, not exclusion. 
- AthenaおよびRedshift Spectrumは列レベルのアクセス制御をサポートしていますが、含めることのみで、除外はサポートしていません。

Column-level access control is not supported in AWS Glue ETL jobs.
列レベルのアクセス制御は、AWS Glue ETLジョブではサポートされていません。

- When a resource is shared with your AWS account, you can grant permissions on the resource only to users in your account. 
- リソースがあなたのAWSアカウントと共有されると、そのリソースに対する権限をあなたのアカウント内のユーザーにのみ付与できます。

You can't grant permissions on the resource to other AWS accounts, to organizations (not even your own organization), or to the IAM Allowed Principals group.
他のAWSアカウント、組織（自分の組織でさえも）、またはIAM Allowed Principalsグループに対してリソースの権限を付与することはできません。

- You can't grant DROP or Super on a database to an external account.
- 外部アカウントに対してデータベースのDROPまたはSuperを付与することはできません。

- Revoke cross-account permissions before you delete a database or table. 
- データベースまたはテーブルを削除する前に、クロスアカウント権限を取り消してください。

Otherwise, you must delete orphaned resource shares in AWS Resource Access Manager.
そうしないと、AWSリソースアクセスマネージャーで孤立したリソース共有を削除する必要があります。

- Lake Formation tag-based access control best practices and considerations
- Lake Formationのタグベースのアクセス制御のベストプラクティスと考慮事項

- CREATE_TABLE in the Lake Formation permissions reference for more cross-account access rules and limitations.
- クロスアカウントアクセスルールおよび制限に関する詳細は、Lake Formation権限リファレンスのCREATE_TABLEを参照してください。

Javascript is disabled or is unavailable in your browser.
Javascriptが無効になっているか、ブラウザで利用できません。

To use the Amazon Web Services Documentation, Javascript must be enabled. 
Amazon Web Servicesのドキュメントを使用するには、Javascriptを有効にする必要があります。

Please refer to your browser's Help pages for instructions.
ブラウザのヘルプページを参照して、手順を確認してください。

Thanks for letting us know we're doing a good job!
私たちが良い仕事をしていることを知らせていただきありがとうございます！

If you've got a moment, please tell us what we did right so we can do more of it.
もしお時間があれば、私たちが何をうまくやったのか教えていただければ、さらにそれを続けることができます。

Thanks for letting us know this page needs work. 
このページに改善が必要であることを知らせていただきありがとうございます。

We're sorry we let you down.
ご期待に添えなかったことをお詫び申し上げます。

If you've got a moment, please tell us how we can make the documentation better.
もしお時間があれば、ドキュメントをどのように改善できるか教えていただければ幸いです。

- Related resources AWS Lake Formation API Reference AWS CLI commands for AWS Lake Formation SDKs & Tools
- 関連リソース AWS Lake Formation APIリファレンス AWS Lake FormationのAWS CLIコマンド SDKおよびツール

- Did this page help you? Yes No Provide feedback
- このページは役に立ちましたか？ はい いいえ フィードバックを提供



### Related resources 関連リソース

Related resources
関連リソース

AWS Lake Formation API Reference
AWS Lake Formation API リファレンス

AWS CLI commands for AWS Lake Formation
AWS Lake Formation のための AWS CLI コマンド

SDKs & Tools
SDK とツール



#### Did this page help you? このページは役に立ちましたか？

Yes はい
No いいえ
Provide feedback フィードバックを提供する



#### Next topic: 次のトピック

Service-linked role limitations
サービスに関連する役割の制限



#### Previous topic: 前のトピック

Lake Formation best practices, considerations, and limitations
Lake Formationのベストプラクティス、考慮事項、および制限



#### Need help? 助けが必要ですか？

- Try AWS re:Post 
- Connect with an AWS IQ expert 
- AWS re:Postを試してみてください
- AWS IQの専門家に接続してください
