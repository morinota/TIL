## refs:

- [AWS CDK でのTypeScript の使用](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/work-with-cdk-typescript.html)
- [CDKv2 で AssumeRole を使い安全に CD する方法](https://qiita.com/munepi0713/items/fa74c35755f02a1007b0)
- [cdk bootstrap(CDKToolkit)を使いこなす](https://zenn.dev/rrrraaaaa6/articles/61319c356dc964)
- cdk bootstrapでECRリポジトリが作られないバグ [CDK bootstrap: does not create ECR repository #28876](https://github.com/aws/aws-cdk/issues/28876)

## CDK v2 で、Continuou Deliveryする

- CDしてくれるサービスに対して、AWSアカウントの操作権を委ねる(AssumeRoleする)必要があるが、できるだけリスクを下げて安全に行いたい。

## cdkコマンド達:

### cdk bootstrap

- 公式ドキュメントの記述:
  - Bootstrapping is the process of provisioning resources for the AWS CDK before you can deploy AWS CDK apps into an AWS environment. (An AWS environment is a combination of an AWS account and Region).
- つまり、CDKアプリケーションをデプロイするにあたって、必要なリソースを作る呪文が `cdk bootstrap` である。
  - この呪文を実行すると、`CDKToolkit`という名前のCloudFormation stackが作成される。
- 呪文で作られるリソース一覧は以下:
  - DeploymentActionRole (ざっくりデプロイに関わる挙動)
  - LookupRole (cdk diffなどで使われる)
  - CloudFormationExecutionRole (CloudFormationのstackにpassRoleされる)
  - ImagePublishingRole
  - FilePublishingRole
  - ContainerAssetsRepository
  - StagingBucket
