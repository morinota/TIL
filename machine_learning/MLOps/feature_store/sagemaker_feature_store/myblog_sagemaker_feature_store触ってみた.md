# タイトル: Feature Storeの肌感を掴むためにSageMaker Feature Storeを触ってみるメモ

## これは何??

- Feature Store周りの肌感をつかむために、SageMaker Feature Storeを触ってみるメモです。具体的には、以下のことをやってみてます。
  - Feature Storeへの特徴量定義の新規作成・更新・削除
  - Feature Storeへの特徴量の書き込み
  - Feature Storeからの特徴量の読み込み
  - Feature Storeからの特徴量の削除
  - point-in-time correct join機能を活用した学習用・バッチ推論用データセットの作成

## 導入: ざっくりFeature Storeってどんなものだっけ? Feature Storeが与える恩恵は??

### ざっくりFeature Storeってどんなものだっけ??

- hoge

### Feature Storeが与える恩恵は??

- [Hopsworksさんの資料では11個ほど列挙されてる](https://www.hopsworks.ai/dictionary/feature-store#problems-solved)が、個人的にこれらの恩恵は大きく以下の3種類に分類できるという認識です...!:thinking:
  - 1つ目: 様々な特徴量を一元管理することによる恩恵
  - 2つ目: FTI Pipelines Architectureに則ったシステムであること(=特徴量生成/学習/推論を分離すること)による恩恵
  - 3つ目: timestamp付きで特徴量を管理することによる恩恵

- ちなみに、以前、Feature Storeが何たるかについて調べた記事はこちら:
  - [The Feature Store Advanced Guide 2025年ver.を読んだメモ](https://qiita.com/morinota/items/2ba8641ab6741c0ba6be)

## いざSageMaker Feature Storeを触ってみる

### Feature Storeへの特徴量定義の新規作成・更新・削除

まずSagemaker Feature Storeの場合は、「**Feature Group**」という概念で特徴量を管理するみたい。

- Feature Groupって何?
  - **「特徴量の集合・テーブル」のようなもので、ひとまとまりの特徴量（カラム）と、その主キー（Identifier）やイベント時刻（EventTime）を持つデータ構造**。
  - 「ユーザ属性特徴量グループ」「商品特徴量グループ」など、用途やドメインごとに分けて管理されるのが一般的みたい。
  - たぶんこのFeature Groupの分け方の設計は、運用しやすさに一定影響しそう...!:thinking:
- Feature Groupの概念って、多くのFeature Storeサービスで共通なのかな。
  - たぶん概念は共通。ただ特徴量の論理的なグループの呼び方は、サービスによって多少異なるっぽい。
  - Sagemaker, Hopsworks, Vertex AIは「Feature Group」
  - 他にもFeature ViewとかFeature Tableとか呼ばれたりするみたい。

Feature Groupを定義するときには、作りたい特徴量名・データ型の他に、主に以下を指定するっぽい。

- entityを識別するカラム (ユーザ特徴量ならuser_idとか)
- timestamp (event_timeと呼ばれてる?) を表すカラム
- そのFeature Groupをオンラインストアに保存するべきか否か...など。

Sagemaker Python SDKを使う場合は、例えば以下のようにFeature Groupを定義できる。
(参考: https://sagemaker.readthedocs.io/en/stable/amazon_sagemaker_featurestore.html)

```python
import boto3
import sagemaker
from sagemaker.feature_store.feature_definition import FeatureDefinition, FeatureTypeEnum
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.feature_store.inputs import FeatureValue

session = boto3.Session(profile_name="my_aws_prifile_name")
sagemaker_session = sagemaker.Session(boto_session=session)

my_feature_group = FeatureGroup(
    name="my-feature-group-name",
    sagemaker_session=sagemaker.Session(),
    # Feature Group内に含める特徴量たちを定義していく
    feature_definitions=[
        # 注意: entityを識別するカラムもfeature_definitionsに含める
        FeatureDefinition(
            feature_name="user_id",
            feature_type=FeatureTypeEnum.STRING,
        ),
        # 注意: 特徴量管理のためのtimestampを表すカラムもfeature_definitionsに含める
        FeatureDefinition(
            feature_name="event_time",
            feature_type=FeatureTypeEnum.STRING,
        ),
        FeatureDefinition(
            feature_name="my_feature_name_1",
            feature_type=FeatureTypeEnum.FRACTIONAL,
        ),
    ],
)
my_feature_group.create(
    # # offline feature store でデータを保存する S3 URIのprefix指定
    s3_uri="s3://my-bucket-name/my-feature-group-name",
    record_identifier_name="user_id",　# entityを識別するカラム名
    event_time_feature_name="event_time", # # timestampを表すカラム名
    enable_online_store=True, # Feature Groupをオンラインストアに保存すべきか否か
    role_arn="Feature Group作成(CreateFeatureGroup)を実行するためのIAM RoleのARN",
    description="Feature Groupの説明文",
    # feature groupに紐づけたいリソースタグ
    tags=[
        {"Key": "my_tag1", "Value": "my_tag_value1"},
        {"Key": "my_tag2", "Value": "my_tag_value2"},
    ],
    # その他、いくつかオプショナルの引数がある
    disable_glue_table_creation=False,
)
```

- 個人的な注意点:
  - feature_definitionsに含める特徴量定義には、entityを識別するカラムと、特徴量の生成時刻を管理するtimestampカラムも含めておく必要がある。
    - ちなみにSagemaker Feature Storeでは、このtimestampのカラムに**event_time**という名前で表すのが一般的みたい。
  - **オンラインストアに保存するか否かは、Feature Group単位で指定する必要がある**。また、**Feature Groupを作成した後で、オンラインストアに保存するか否かを変更することはできない**。
    - 一般にオンラインストアは高コストだと思うので、オンラインストアに保存すべき特徴量とそうでない特徴量を分けてFeature Groupを設計する方が良さそう...!:thinking:
- `disable_glue_table_creation`についてメモ。
  - Sagemaker Feature StoreはFeature Groupを作るときに、オフラインストアのメタデータ管理用に、デフォルトでAWS Glueのテーブルを作成する (なのでこの引数のデフォルト値は`False`)。
  - これにより、**S3に保存したデータのスキーマ情報をGlue Data Catalogで管理できるので**、Athenaや他のSQLクエリエンジンから、S3上のオフラインストアデータをテーブルとしてクエリしやすくなる。
    - 公式ドキュメントより
      - >Feature Store requires data to be registered in a AWS Glue data catalog. By default, Feature Store automatically builds an AWS Glue data catalog when you create a feature group. Feature Storeは、データをAWS Glueデータカタログに登録する必要があります。デフォルトでは、Feature StoreはFeature Groupを作成するときに自動的にAWS Glueデータカタログを構築します。
    - どうやらpoint-in-time correct join機能などの高度な機能を使う場合(=たぶん裏でAthenaのクエリが実行される)は、Glueテーブルの存在が前提になってるみたい。
  - **なので基本はデフォルト(`False`)のままが良さそう!!**
    
またcdkでFeature Groupを作成する場合は、以下のように定義できる。
(参考: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_sagemaker.CfnFeatureGroup.html)

```typescript
export class FeatureStoreStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props: FeatureStoreStackProps) {
        super(scope, id, props);

        const { prefix } = props;

        // オフラインストア用のS3バケットを作成
        const featureStoreBucket = new s3.Bucket(this, `${prefix}FeatureStoreBucket`, {
            bucketName: `${prefix.toLowerCase()}feature-store-bucket`,
            accessControl: s3.BucketAccessControl.PRIVATE,
            removalPolicy: cdk.RemovalPolicy.DESTROY,
            // autoDeleteObjects: true, // お試しなのでバケット削除時にオブジェクトも一緒に削除できるように。
            versioned: false,
            lifecycleRules: [
                {
                    // 万が一リソースを削除しそびれて高額請求が来ないように、七日後に削除するようにする。
                    // 本番運用の際には、適切なライフサイクルポリシーを設定すること。
                    expiration: cdk.Duration.days(7),
                    enabled: true,
                }
            ],
        });

        // Feature Groupを作成・更新・削除するためのIAMロールを作成
        const featureGroupManagementRole = new iam.Role(this, `${prefix}FeatureGroupManagementRole`, {
            assumedBy: new iam.ServicePrincipal("sagemaker.amazonaws.com"),
            path: "/service-role/",
            roleName: `${prefix}feature-group-management-role`,
            managedPolicies: [
                iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonSageMakerFeatureStoreAccess"),
                iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonS3FullAccess"),
            ],
        });

        // 以下で各種Feature Groupを定義していく
        new CfnFeatureGroup(this, `MyFeatureGroup`, {
            featureGroupName: 'user-feature-group',
            recordIdentifierFeatureName: 'user_id',
            eventTimeFeatureName: 'event_time',
            featureDefinitions: [
                {
                    featureName: 'user_id',
                    featureType: 'Integral',
                },
                {
                    featureName: 'event_time',
                    featureType: 'String',
                },
                {
                    featureName: 'user_embedding',
                    featureType: 'String',
                },
                // 他にも特徴量があれば追加
            ],
            // オフラインストアの設定
            offlineStoreConfig: {
                // 注意: ここのpropertyは全部大文字はじまり...!
                S3StorageConfig: {
                    S3Uri: `s3://${featureStoreBucket.bucketName}`
                },
                DisableGlueTableCreation: false,
            },
            // オンラインストアの設定
            onlineStoreConfig: {
                EnableOnlineStore: false,
            },
            // Feature Group管理のためのIAMロール
            roleArn: featureGroupManagementRole.roleArn,
            // CfnFeatureGroupはL1リソースなので、メソッドでRemovalPolicyを設定する必要がある。
        }).applyRemovalPolicy(cdk.RemovalPolicy.DESTROY);
    }
}
```

### Feature Storeへの特徴量の書き込み

- 注意点: オフラインストアへの特徴量書き込み(ingest)の反映には、通常5~15分ほどかかるっぽい。
  - >PutRecord を呼び出すと、データは 15 分以内に Amazon S3 にバッファされ、バッチ処理され、書き込まれます
  - `FeatureGroup.ingest()`メソッドには`wait`オプションがあるが、**これはあくまでPutRecord APIの呼び出しが完了するまで待つだけ。その後実行されるオフラインストアへの非同期の書き込み処理の完了を待つわけではないので注意...!!**
  - なので、オフラインストアへの書き込みが完了したかどうかを確認するには、自前でS3のparquetファイルを確認する実装をする必要があるっぽい...??:thinking:

### Feature Storeからの特徴量の読み込み

- hoge

### point-in-time correct join機能を活用した学習用・バッチ推論用データセットの作成

- hoge
