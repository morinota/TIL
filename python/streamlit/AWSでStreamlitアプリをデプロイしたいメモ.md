## これは何?

- AWS上でStreamlitアプリをホストするためのメモ

## refs

- [【AWSコンテナ入門】簡単なPythonアプリをECSにデプロイしてみよう！](https://qiita.com/minorun365/items/84bef6f06e450a310a6a)
- [AWS上にStreamlitの動作環境を作ってみた](https://qiita.com/tommy_aka_jps/items/5db7bd157aa5d424712e)
- AWS Fargateで社内限定公開してる事例: https://zenn.dev/any_dev/articles/rag-streamlit-and-langsmith
- [社内向けStreamlitのデプロイの現実解](https://zenn.dev/dataheroes/articles/2eae5a5ad92534)

# メモ

- 基本的には ALB + ECS みたいな構成で対応できるっぽい...??
  - ざっくり:
    - Streamlitアプリを実装してDockerイメージとしてビルド。
    - ECRにプッシュ。
    - ECSタスク定義を作成し、Fargateで実行。
    - ALBを設定して外部からアクセス可能にする。
- 注意: どうやらALB(Application Load Balancer)が必須っぽい!
  - 理由は、StreamlitはWebSocketでページに表示するコンテンツを取得するため。
  - そしてWebSocket対応のロードバランサーがALBのみらしい。
    - https://uorat.hatenablog.com/entry/2016/09/26/070000
    - CLB(Classic Load Balancer)っていうのもあるらしく、そっちはWebSocket非対応なのでStreamlitのページを表示できないみたい...!
  - **StreamlitはWebSocketを前提とした技術であるため**、2024.12時点でもAWS App Runnerで構築できないらしい。
- 注意: **フロントエンドとバックエンドが共存する形になるため、対外的なアプリケーションとして構築するとセキュリティリスクを伴う!**
  - あくまでも社内アプリかつ本番データを取り扱わないこと!

ざっくりcdkの実装イメージ

```typescript
export class StreamlitAppStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPC作成（デフォルト設定）
    const vpc = new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 3
    });

    // ECSクラスター作成
    const cluster = new ecs.Cluster(this, 'EcsCluster', {
      vpc,
      clusterName: 'my-cluster'
    });

    // Fargateタスク定義
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'TaskDef', {
      memoryLimitMiB: 512,
      cpu: 256
    });
    // コンテナ定義
    taskDefinition.addContainer('WebContainer', {
      image: ecs.ContainerImage.fromRegistry('amazon/amazon-ecs-sample'),
      portMappings: [{ containerPort: 80 }]
    });

    // セキュリティグループを追加して、社内限定公開に。
    const albSg = new ec2.SecurityGroup(this, 'AlbSg', {
    vpc,
    description: 'Restrict ALB access'
    });
    albSg.addIngressRule(
    ec2.Peer.ipv4('10.0.0.0/16'), // 社内IP範囲
    ec2.Port.tcp(80)
    );

    // 改善されたサービス定義
    new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'SecureService', {
    cluster,
    taskDefinition,
    securityGroups: [albSg],
    publicLoadBalancer: false, // 内部ALB
    vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }
    });
```

- なるほどなぁ...。SiS(Streamlit in Snowflake)だと、ALBとか社内限定公開のための設定とかをかなりすっ飛ばせるのか〜...! :thinking:
  - メリット:
    - **Snowflakeのアクセス管理機能がマネージドで提供される。-> 安全なデプロイとホストが容易に実現できる** (AWSだとここを自分で一定頑張らなきゃいけないのか...!:thinking:)
    - データの位置とコンピューティングの位置が近い -> アプリケーションの実行速度を向上できる (まあこれはSnowflakeのDWHとやり取りする前提かな)
    - Snowflakeからデータが出ないのでより安全。
  - 制限事項
    - Snowflakeアカウントが必要。
    - 一部のPythonライブラリの利用が制限されている。
