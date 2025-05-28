# タイトル: Feature Storeの具体的な機能の肌感をつかむために、SageMaker Feature Storeを触ってみたメモ

## これは何??

- 
- この記事は、Feature Storeの具体的な機能を知りたいので、その肌感をつかむために、SageMaker Feature Storeを触ってみたメモです。
  - (どのFeature Storeサービスも基本的にはほぼほぼ同じような機能を持ってるだろうから、1個触っておけば肌感掴めるだろうという認識...!:thinking:)
- 具体的には、以下のことをやってみてます。
  - Feature Storeへの特徴量定義(feature group)の新規作成
  - Feature Storeへの特徴量の書き込み
  - Feature Storeからの特徴量の読み込み
  - point-in-time correct join機能を活用した学習用・バッチ推論用データセットの作成
  - Feature Storeからの特徴量の削除
- ちなみに、Feature Storeについて調べた過去の記事はこちら
  - [The Feature Store Advanced Guide 2025年ver.を読んだメモ](https://qiita.com/morinota/items/2ba8641ab6741c0ba6be)
  - [Operational(=本番システム上で実際に価値を発揮する?)なFeature Storeに必要な5つの最低条件を読んだメモ](https://qiita.com/morinota/items/9e5eb673be3abfc24296)

## 導入: ざっくりFeature Storeってどんなものだっけ? Feature Storeが与える恩恵は??

- ざっくりFeature Storeってどんなものだっけ??
  - > A feature store is a data platform that supports the development and operation of machine learning systems by managing the storage and efficient querying of feature data. Feature Storeは、特徴量データの保存と効率的なクエリを管理することにより、機械学習システムの開発と運用をサポートするデータプラットフォームである。
    - 引用: [Feature Store: The Definitive Guide](https://www.hopsworks.ai/dictionary/feature-store#training-data)
  - ざっくりFeature Storeの自分の理解! 
    - **特徴量を一元管理する場所！ timestamp付きで特徴量をバージョン管理するよ! 特徴量生成/学習/推論という3種のMLパイプラインを結びつける接着剤として機能するよ!**
- Feature Storeが与える恩恵は??
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

Sagemaker Python SDKを使う場合は、例えば以下のようにFeature Groupを定義できるようです。
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
    enable_online_store=False, # Feature Groupをオンラインストアに保存すべきか否か
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

### Feature Storeへの特徴量レコードの書き込み

前セクションにて、特徴量を管理するためのfeature groupを定義できました。
なので次は、feature groupに対して特徴量レコードを実際に書き込んでみます。

- 特徴量レコードのfeature groupへの書き込み方法はいくつかあるようですが、今回はバッチで一気に複数レコードをオフラインストアに書き込む方法として`FeatureGroup.ingest()`メソッドを使ってみます。
  - オンラインストアに少量レコードを書き込む場合は別のAPIを使うことになりそうです。

以下が実装例です。

```python
import abc
import json
from datetime import datetime

import polars as pl
import sagemaker
from sagemaker.feature_store.feature_group import FeatureGroup
from sagemaker.feature_store.feature_store import FeatureStore

class SagemakerFeatureStoreRepository:
    def __init__(
        self,
        sagemaker_session: sagemaker.Session,
        bucket_for_temp_file: str = "my-bucket-for-temp-file",
    ) -> None:
        self._sagemaker_session = sagemaker_session

        self._feature_store = FeatureStore(sagemaker_session=self._sagemaker_session)
        self._bucket_for_temp_file = bucket_for_temp_file

    def ingest_features(
        self,
        feature_group_name: str,
        feature_df: pl.DataFrame,
    ) -> None:
        feature_group = FeatureGroup(feature_group_name, self._sagemaker_session)

        feature_group.ingest(data_frame=feature_df.to_pandas(), max_workers=1, wait=True)

        # TODO: オフラインストアへの結果反映まで5~15分くらいかかるっぽいので、待機処理を追加する。
```

上記の`ingest_features`メソッドを実際に呼び出してみます。

```python
import json

import boto3
import polars as pl
import sagemaker

from feature_store_repository import SagemakerFeatureStoreRepository

# awsとの接続設定
sagemaker_session = sagemaker.Session()

# Feature Storeのリポジトリを作成
repository = SagemakerFeatureStoreRepository(sagemaker_session)

# 特徴量をfeature groupに登録
feature_df = pl.DataFrame(
    {
        "user_id": [1, 1, 1, 2, 2, 2, 3, 3, 3],
        "event_time": ["2025-01-01T00:00:00Z", "2025-01-02T00:00:00Z", "2025-01-03T00:00:00Z"] * 3,
        "user_embedding": [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]] * 3,
    }
).with_columns(
    # ベクトル型がないので、embeddingを文字列にencodeして保存してる
    pl.col("user_embedding").map_elements(lambda record: json.dumps(list(record)))
)
print(f"{feature_df=}")
repository.ingest_features(
    feature_group_name="user-feature-group",
    feature_df=feature_df,
)
```

今回は以下のような特徴量レコード達を書き込んでみました。
想定としては、3人のユーザについて、3つのバージョンの特徴量を追加しています。
(実運用では、例えば1日一回、ユーザ埋め込みを作るfeature pipelineが稼働して、1つ(i.e.ある日)のバージョンの特徴量をfeature groupに追加していくのがイメージしやすそう:thinking:)

```
┌─────────┬──────────────────────┬────────────────┐
│ user_id ┆ event_time           ┆ user_embedding │
│ ---     ┆ ---                  ┆ ---            │
│ i64     ┆ str                  ┆ str            │
╞═════════╪══════════════════════╪════════════════╡
│ 1       ┆ 2025-01-01T00:00:00Z ┆ [0.1, 0.2]     │
│ 1       ┆ 2025-01-02T00:00:00Z ┆ [0.3, 0.4]     │
│ 1       ┆ 2025-01-03T00:00:00Z ┆ [0.5, 0.6]     │
│ 2       ┆ 2025-01-01T00:00:00Z ┆ [0.1, 0.2]     │
│ 2       ┆ 2025-01-02T00:00:00Z ┆ [0.3, 0.4]     │
│ 2       ┆ 2025-01-03T00:00:00Z ┆ [0.5, 0.6]     │
│ 3       ┆ 2025-01-01T00:00:00Z ┆ [0.1, 0.2]     │
│ 3       ┆ 2025-01-02T00:00:00Z ┆ [0.3, 0.4]     │
│ 3       ┆ 2025-01-03T00:00:00Z ┆ [0.5, 0.6]     │
└─────────┴──────────────────────┴────────────────┘
```

エラーなく処理が成功しました。なのでS3上のオフラインストアにparquetファイルが書き込まれたか見てみたのですが、すぐにはS3上にparquetファイルが生成されていません。
ここで注意点なのですが、どうやらオフラインストアへの特徴量書き込み(ingest)の反映には、通常5~15分ほどかかるっぽい。

- >PutRecord を呼び出すと、データは 15 分以内に Amazon S3 にバッファされ、バッチ処理され、書き込まれます
- `FeatureGroup.ingest()`メソッドには`wait`オプションがあるが、**これはあくまでPutRecord APIの呼び出しが完了するまで待つだけ。その後実行されるオフラインストアへの非同期の書き込み処理の完了を待つわけではないので注意...!!**
- なので、オフラインストアへの書き込みが完了したかどうかを確認するには、自前でS3のparquetファイルを確認する実装をする必要があるっぽい...??:thinking:

<!-- - 訃報: Sagemaker Feature Storeのオフラインストアは、vector型の特徴量をサポートしていない...:cry:
  - なので埋め込み表現などの特徴量は、文字列にencodeしてFeature Storeに保存しておき、使うときにdecodeする必要がありそう...:cry: -->

### Feature Storeからの特徴量の読み込み

- オンラインストアから取得するか、オフラインストアから取得するかでAPIが異なる。
  - オンラインストアから取得する場合:
    - `get_record`メソッド。entityカラムの値と取得したい特徴量名を指定する。
    - 今回はオフラインストアのみに保存するfeature groupを作成したので、これは試さない。
  - オフラインストアから取得する場合
    - **3パターンくらい方法がありそう**。
    - 方法1: `FeatureGroup.athena_query().run(query)`メソッドを使う方法。
      - Amazon Athena用のSQLクエリを直接書いて、run()メソッドの引数に渡して実行する。
      - 自由にSQLクエリをかけるので、柔軟性は高い。
    - **方法2: `FeatureStore.create_dataset()`メソッドを使う**。
      - **基本的に本番システムにおいて、学習用データセットやバッチ推論用データセットを作る時はこの方法で十分そう...!**:thinking:
      - point-in-time correct join機能なども抽象化されてる。
    - 方法3: S3上のparquetファイルを直接読み込む。
      - あまり使わなさそう。

以下は、方法1によるオフラインストアからの特徴量の読み込み実装例です。
今回はとりあえず、feature group内の全ての特徴量レコードを取得するようなSQLクエリを書いて実行させてます。

```python
    def fetch_features(
        self,
        feature_group_name: str,
    ) -> pl.DataFrame:
        feature_group = FeatureGroup(feature_group_name, self._sagemaker_session)
        feature_store_query = feature_group.athena_query()
        feature_store_table = feature_store_query.table_name
        
        query_string = f"""
        select * 
        from "{feature_store_table}"
        """

        feature_store_query.run(
            query_string=query_string,
            output_location=f"s3://{self._bucket_for_temp_file}/athena_query_results/{feature_group_name}/",
        )
        feature_store_query.wait()
        feature_pd_df = feature_store_query.as_dataframe()
        return pl.from_pandas(feature_pd_df)
```

試しに呼び出してみる。

```python
# Feature Groupから全ての特徴量レコードを取得する例
fetched_feature_df = repository.fetch_features("user-feature-group")
print(f"{fetched_feature_df=}")
```

無事に、指定したfeature groupの全て特徴量レコードがDataFrameとして返ってくることを確認できました!

```
fetched_feature_df=shape: (9, 6)
┌─────────┬─────────────────────┬────────────────┬──────────────┬─────────────────────┬────────────┐
│ user_id ┆ event_time          ┆ user_embedding ┆ write_time   ┆ api_invocation_time ┆ is_deleted │
│ ---     ┆ ---                 ┆ ---            ┆ ---          ┆ ---                 ┆ ---        │
│ i64     ┆ str                 ┆ str            ┆ str          ┆ str                 ┆ bool       │
╞═════════╪═════════════════════╪════════════════╪══════════════╪═════════════════════╪════════════╡
│ 1       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.463 ┆ 11:22:23.000        ┆            │
│ 1       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.454 ┆ 11:22:22.000        ┆            │
│ 3       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.833 ┆ 11:22:24.000        ┆            │
│ 3       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.834 ┆ 11:22:24.000        ┆            │
│ 2       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 3       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.829 ┆ 11:22:24.000        ┆            │
│ 2       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 2       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 1       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.458 ┆ 11:22:23.000        ┆            │
└─────────┴─────────────────────┴────────────────┴──────────────┴─────────────────────┴────────────┘
```

- 注意点: Sagemaker Feature Store側が勝手に追加してくれるカラム達について。
  - Athenaクエリで普通に`select *`で取得すると、feature groupで定義した3つのカラム(user_id, event_time, user_embedding)に加えて、以下の3つのカラムも自動付与されていることがわかる。
    - write_time: データがFeature Storeに書き込まれた時間
    - api_invocation_time: データを書き込むAPIリクエストを受けた時間
    - is_deleted: データが削除済かどうか。
      - しかしオフラインストアの場合はS3にappend-only保存だから、deleteリクエストがきても物理的にはレコードが消えない。
      - その代わりにis_deletedがTrueになり、レコードが無効化される。

### point-in-time correct join機能を活用した学習用・バッチ推論用データセットの作成

おそらくMLの学習 & バッチ推論時など、実運用でよく使うと思われるやつです。
point-in-time correct join機能を活用して、学習用・バッチ推論用のデータセットを作成する方法について。

以下のように実装してみました。

```python
    def fetch_dataset_with_point_in_time_join(
            self,
            base_entity_df: pl.DataFrame,
            base_record_identifier_name: str,
            base_event_time_name: str,
            feature_groups: list[tuple[str, str]],
        ) -> pl.DataFrame:
        """point-in-time join によるデータ取得を行うメソッド
            Args:
                base_entity_df: ベースとなるデータフレーム
                base_record_identifier_name: ベースのレコード識別子のカラム名
                base_event_time_name: ベースのイベント時間のカラム名
                feature_groups: ターゲットのフィーチャグループ名と結合キーのタプルのリスト
                    feature_group_name: フィーチャグループ名
                    join_key: フィーチャグループとのjoinに使いたいbase_entity_dfのカラム名
            Returns:
                各種特徴量がbase_entity_dfに結合されたデータフレーム
        """
        dataset_builder = (
            self._feature_store.create_dataset(
                base=base_entity_df.to_pandas(),
                event_time_identifier_feature_name=base_event_time_name,
                record_identifier_feature_name=base_record_identifier_name,
                output_path=f"s3://{self._bucket_for_temp_file}/point_in_time_join/",
            )
            # 時点整合性を保証するための設定
            .point_in_time_accurate_join()
            # かつ最も新しいtimestampのレコードのみを取得する設定
            .with_number_of_recent_records_by_record_identifier(1)
        )

        for feature_group_name, join_key in feature_groups:
            dataset_builder = dataset_builder.with_feature_group(
                feature_group=FeatureGroup(
                    feature_group_name,
                    self._sagemaker_session,
                ),
                target_feature_name_in_base=join_key,
            )

        dataset_pandas_df, _ = dataset_builder.to_dataframe()
        return pl.from_pandas(dataset_pandas_df)
```

上記の`fetch_dataset_with_point_in_time_join`メソッドを、まずは学習用データセットを作る想定で呼び出してみます。

```python
# point-in-time correct join機能を使って、学習用データセットを作る例

# 擬似的なinteractionデータを用意(このrewardに基づく目的関数でMLモデルを学習するイメージ)
interaction_df = pl.DataFrame(
    {
        "interaction_id": [1, 2, 3],
        "user_id": [1, 2, 3],
        "item_id": [101, 102, 103],
        "reward": [0.5, 1.0, 0.75],
        "event_time": ["2025-01-01T12:00:00Z", "2025-01-02T12:00:00Z", "2025-01-03T12:00:00Z"],
    }
)
print(f"{interaction_df=}")

## 必要な特徴量をpoint-in-time correct joinで結合
train_df = repository.fetch_dataset_with_point_in_time_join(
    base_entity_df=interaction_df,
    base_record_identifier_name="interaction_id",
    base_event_time_name="event_time",
    feature_groups=[("user-feature-group", "user_id")],
)
print(f"{train_df=}")

# 学習ステップへ...!
```

出力結果は以下です。

```
interaction_df=shape: (3, 5)
┌────────────────┬─────────┬─────────┬────────┬──────────────────────┐
│ interaction_id ┆ user_id ┆ item_id ┆ reward ┆ event_time           │
│ ---            ┆ ---     ┆ ---     ┆ ---    ┆ ---                  │
│ i64            ┆ i64     ┆ i64     ┆ f64    ┆ str                  │
╞════════════════╪═════════╪═════════╪════════╪══════════════════════╡
│ 1              ┆ 1       ┆ 101     ┆ 0.5    ┆ 2025-01-01T12:00:00Z │
│ 2              ┆ 2       ┆ 102     ┆ 1.0    ┆ 2025-01-02T12:00:00Z │
│ 3              ┆ 3       ┆ 103     ┆ 0.75   ┆ 2025-01-03T12:00:00Z │
└────────────────┴─────────┴─────────┴────────┴──────────────────────┘

train_df=shape: (3, 8)
┌──────────────┬─────────┬─────────┬────────┬──────────────┬───────────┬─────────────┬─────────────┐
│ interaction_ ┆ user_id ┆ item_id ┆ reward ┆ event_time   ┆ user_id.1 ┆ event_time. ┆ user_embedd │
│ id           ┆ ---     ┆ ---     ┆ ---    ┆ ---          ┆ ---       ┆ 1           ┆ ing.1       │
│ ---          ┆ i64     ┆ i64     ┆ f64    ┆ str          ┆ i64       ┆ ---         ┆ ---         │
│ i64          ┆         ┆         ┆        ┆              ┆           ┆ str         ┆ str         │
╞══════════════╪═════════╪═════════╪════════╪══════════════╪═══════════╪═════════════╪═════════════╡
│ 2            ┆ 2       ┆ 102     ┆ 1.0    ┆ 2025-01-02T1 ┆ 2         ┆ 2025-01-02T ┆ [0.3, 0.4]  │
│              ┆         ┆         ┆        ┆ 2:00:00Z     ┆           ┆ 00:00:00Z   ┆             │
│ 1            ┆ 1       ┆ 101     ┆ 0.5    ┆ 2025-01-01T1 ┆ 1         ┆ 2025-01-01T ┆ [0.1, 0.2]  │
│              ┆         ┆         ┆        ┆ 2:00:00Z     ┆           ┆ 00:00:00Z   ┆             │
│ 3            ┆ 3       ┆ 103     ┆ 0.75   ┆ 2025-01-03T1 ┆ 3         ┆ 2025-01-03T ┆ [0.5, 0.6]  │
│              ┆         ┆         ┆        ┆ 2:00:00Z     ┆           ┆ 00:00:00Z   ┆             │
└──────────────┴─────────┴─────────┴────────┴──────────────┴───────────┴─────────────┴─────────────┘
```

出力された`train_df`を見てみると、interactionデータに加えて、user-feature-groupからの特徴量が結合されていることがわかります。
そして重要なのは、point-in-time correct join機能により、各interactionレコードの`event_time`の値に基づいて、**feature data leakしない範囲での最新の特徴量レコードが結合されていること**です。
うんうん、これぞpoint-in-time correct joinって感じがして良さげですね...!:thinking:

同様に、バッチ推論用のデータセットを作る場合も想定して、`fetch_dataset_with_point_in_time_join`メソッドを呼び出してみます。

```python
# point-in-time correct join機能を使って、バッチ推論用データセットを作る例
# 基本的には全ユーザについて、バッチ推論を実行する際のtimestampを指定すれば良いはず
execution_timestamp = "2025-01-04T00:00:00Z"
target_user_df = pl.DataFrame(
    {
        "user_id": [1, 2, 3],
        "event_time": [execution_timestamp] * 3,
    }
)

# 学習と同様に、point-in-time correct joinで必要な特徴量を結合
inference_input_df = repository.fetch_dataset_with_point_in_time_join(
    base_entity_df=target_user_df,
    base_record_identifier_name="user_id",
    base_event_time_name="event_time",
    feature_groups=[("user-feature-group", "user_id")],
)
print(f"{inference_input_df=}")

# バッチ推論ステップへ...!
```

出力結果は以下です。

```
inference_input_df=shape: (3, 5)
┌─────────┬──────────────────────┬───────────┬──────────────────────┬──────────────────┐
│ user_id ┆ event_time           ┆ user_id.1 ┆ event_time.1         ┆ user_embedding.1 │
│ ---     ┆ ---                  ┆ ---       ┆ ---                  ┆ ---              │
│ i64     ┆ str                  ┆ i64       ┆ str                  ┆ str              │
╞═════════╪══════════════════════╪═══════════╪══════════════════════╪══════════════════╡
│ 1       ┆ 2025-01-04T00:00:00Z ┆ 1         ┆ 2025-01-03T00:00:00Z ┆ [0.5, 0.6]       │
│ 2       ┆ 2025-01-04T00:00:00Z ┆ 2         ┆ 2025-01-03T00:00:00Z ┆ [0.5, 0.6]       │
│ 3       ┆ 2025-01-04T00:00:00Z ┆ 3         ┆ 2025-01-03T00:00:00Z ┆ [0.5, 0.6]       │
└─────────┴──────────────────────┴───────────┴──────────────────────┴──────────────────┘
```

作られた`inference_input_df`を見てみると、学習用データセットと同様に、`base_entity_df`の各レコードの`event_time`に基づいて、feature data leakしない範囲での最新の特徴量レコードが結合されています。
今回の場合は推論なので、基本的には推論時点での最も新しい特徴量レコードを使えば良いですよね。

### Feature Storeからの特徴量の削除

最後に、今回追加した特徴量レコードをfeature groupから削除しておきます。

- **注意点: オフラインストアの場合はあくまで論理削除のみ! 物理削除する場合はS3のライフサイクルルールなどを使うと良さそう!**
  - 特にオフラインストアの場合、Feature Storeのデータは基本append-only (オンラインストアの場合は物理削除できるけど、オフラインストアはできない)
  - **よって「削除」という動作は、`is_deleted`フラグを立てる(論理削除)という動作になる!**
    - 言い換えると、レコードを消すのではなく「無効です!」とマークすることになる。
  - **なので、オフラインストアにあるデータを物理削除するには、S3側の機能を使う必要があるみたい...! ライフサイクルルールとか!**
- 唯一提供されてる削除API: `FeatureGroup.delete_record()`メソッド
  - 引数は3つ (=削除したいレコードを一意に識別するための情報のみ...!シンプル!:thinking:)
    - `record_identifier_value_as_string`: 削除したいレコードのentity id
    - `event_time`: 削除したいレコードのevent time (i.e. レコードのversion)
    - `deletion_mode`(オプショナル): 削除モードをソフトかハードか指定する。あ、物理削除できるじゃん、と思いがちだが、これで物理削除できるのはあくまでオンラインストア上にあるレコードのみ...! **どちらのモードを指定してもオフラインストアのレコードは論理削除になる**。

#### オフラインストアからの論理削除

以下のように、`FeatureGroup.delete_record()`メソッドを使って実装してみました。

```python
    def delete_features(
        self,
        feature_group_name: str,
        delete_target_entity_df: pl.DataFrame,
        base_record_identifier_name: str,
        base_event_time_name: str,
    ) -> None:
        feature_group = FeatureGroup(feature_group_name, self._sagemaker_session)

        # 一括削除のAPIが存在しないので、個別に削除する
        for record in delete_target_entity_df.iter_rows(named=True):
            feature_group.delete_record(
                record_identifier_value_as_string=str(record[base_record_identifier_name]),
                event_time=str(record[base_event_time_name]),
            )
```

- 注意点: 公式APIには「一括の論理削除」は存在しなさそう。
  - よってforループで順番にdeleteするしかない。
- 注意点: もし自前でAthenaクエリを書いて特徴量レコードを取得するときは、論理削除ずみか否か(`is_deleted`)を考慮すべき!
  - `FeatureStore.create_dataset()`メソッドを使う場合は、デフォルトで論理削除済みのレコードは除外されるので、たぶん特に考慮しなく大丈夫なはず。
  - 自前でSQLクエリを書いてAthenaに投げる場合は`where is_deleted = 0`みたいな条件を追加する必要がある!

実際に`delete_features`メソッドを呼び出して、今回用意した特徴量レコード達を削除してみます。

```python
# 一旦feature group上の全てのレコードを取得
user_feature_df = repository.fetch_features("user-feature-group")
print(f"{user_feature_df=}")

# 論理削除されてないレコード一覧を取得
delete_target_entity_df = user_feature_df.filter(pl.col("is_deleted") == False).select(
    pl.col("user_id"),
    pl.col("event_time"),
)
print(f"{delete_target_entity_df=}")

# 論理削除を実行
repository.delete_features(
    feature_group_name="user-feature-group",
    delete_target_entity_df=delete_target_entity_df,
    base_record_identifier_name="user_id",
    base_event_time_name="event_time",
)

# 改めてfeature group上の全てのレコードを取得して確認してみる
user_feature_df_after_delete = repository.fetch_features("user-feature-group")
print(f"{user_feature_df_after_delete=}")
```

出力結果は以下です。あれ?? `is_deleted`カラムがFalseのままだぞ...??:thinking:

```
user_feature_df=shape: (9, 6)
┌─────────┬─────────────────────┬────────────────┬──────────────┬─────────────────────┬────────────┐
│ user_id ┆ event_time          ┆ user_embedding ┆ write_time   ┆ api_invocation_time ┆ is_deleted │
│ ---     ┆ ---                 ┆ ---            ┆ ---          ┆ ---                 ┆ ---        │
│ i64     ┆ str                 ┆ str            ┆ str          ┆ str                 ┆ bool       │
╞═════════╪═════════════════════╪════════════════╪══════════════╪═════════════════════╪════════════╡
│ 1       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.463 ┆ 11:22:23.000        ┆            │
│ 1       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.454 ┆ 11:22:22.000        ┆            │
│ 3       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.833 ┆ 11:22:24.000        ┆            │
│ 3       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.834 ┆ 11:22:24.000        ┆            │
│ 2       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 3       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.829 ┆ 11:22:24.000        ┆            │
│ 2       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 2       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 1       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.458 ┆ 11:22:23.000        ┆            │
└─────────┴─────────────────────┴────────────────┴──────────────┴─────────────────────┴────────────┘


delete_target_entity_df=shape: (9, 2)
┌─────────┬──────────────────────┐
│ user_id ┆ event_time           │
│ ---     ┆ ---                  │
│ i64     ┆ str                  │
╞═════════╪══════════════════════╡
│ 1       ┆ 2025-01-03T00:00:00Z │
│ 1       ┆ 2025-01-01T00:00:00Z │
│ 3       ┆ 2025-01-03T00:00:00Z │
│ 3       ┆ 2025-01-02T00:00:00Z │
│ 2       ┆ 2025-01-01T00:00:00Z │
│ 3       ┆ 2025-01-01T00:00:00Z │
│ 2       ┆ 2025-01-03T00:00:00Z │
│ 2       ┆ 2025-01-02T00:00:00Z │
│ 1       ┆ 2025-01-02T00:00:00Z │
└─────────┴──────────────────────┘

user_feature_df_after_delete=shape: (9, 6)
┌─────────┬─────────────────────┬────────────────┬──────────────┬─────────────────────┬────────────┐
│ user_id ┆ event_time          ┆ user_embedding ┆ write_time   ┆ api_invocation_time ┆ is_deleted │
│ ---     ┆ ---                 ┆ ---            ┆ ---          ┆ ---                 ┆ ---        │
│ i64     ┆ str                 ┆ str            ┆ str          ┆ str                 ┆ bool       │
╞═════════╪═════════════════════╪════════════════╪══════════════╪═════════════════════╪════════════╡
│ 1       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.463 ┆ 11:22:23.000        ┆            │
│ 1       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.454 ┆ 11:22:22.000        ┆            │
│ 3       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.833 ┆ 11:22:24.000        ┆            │
│ 3       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.834 ┆ 11:22:24.000        ┆            │
│ 2       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 3       ┆ 2025-01-01T00:00:00 ┆ [0.1, 0.2]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.829 ┆ 11:22:24.000        ┆            │
│ 2       ┆ 2025-01-03T00:00:00 ┆ [0.5, 0.6]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 2       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:21.858 ┆ 11:22:23.000        ┆            │
│ 1       ┆ 2025-01-02T00:00:00 ┆ [0.3, 0.4]     ┆ 2025-05-25   ┆ 2025-05-25          ┆ false      │
│         ┆ Z                   ┆                ┆ 11:27:22.458 ┆ 11:22:23.000        ┆            │
└─────────┴─────────────────────┴────────────────┴──────────────┴─────────────────────┴────────────┘
```

たぶんdelete record APIも非同期で動作するので、5分くらい待たないとオフラインストアに論理削除が反映されないのかもしれないですね...!:thinking:
数分待ってから再度`fetch_features`メソッドを呼び出してみると、`is_deleted`カラムがTrueになっていることが確認できました! 

#### オフラインストアからの物理削除

最後に、オフラインストアから特徴量レコードを物理削除しておきましょうか!
前述した通り、Sagemaker Feature StoreのAPIからはオフラインストアのレコードは物理削除できないようになってるので、S3のparqeutファイルを直接削除することで対応します。

```python
# S3上のparquetファイルを削除後、改めてfeature groupから特徴量を取得してみる
fetched_feature_df = repository.fetch_features("user-feature-group")
print(f"{fetched_feature_df=}")

fetched_feature_df=shape: (0, 6)
┌─────────┬────────────┬────────────────┬────────────┬─────────────────────┬────────────┐
│ user_id ┆ event_time ┆ user_embedding ┆ write_time ┆ api_invocation_time ┆ is_deleted │
│ ---     ┆ ---        ┆ ---            ┆ ---        ┆ ---                 ┆ ---        │
│ str     ┆ str        ┆ str            ┆ str        ┆ str                 ┆ str        │
╞═════════╪════════════╪════════════════╪════════════╪═════════════════════╪════════════╡
└─────────┴────────────┴────────────────┴────────────┴─────────────────────┴────────────┘
```

うん、無事に全ての特徴量レコードを物理削除できましたね!

ちなみに、とりあえず今回はAWSコンソールから手動でparquetファイル達を削除しますが、**実運用ではS3のライフサイクルルールを使って定期的に古いparquetファイルを削除する**感じになるのかなと思います。
推論時には最新バージョンの特徴量レコードを使えば良いですし、継続的学習(i.e. オンライン学習)を行う場合も新しめの特徴量レコードさえあれば十分そうです。

一方で、オフライン学習の際には古いバージョンの特徴量レコードも必要になると思うので、そこはオフライン学習の頻度やコストと合わせて相談なのかなぁ...。基本的には「よし、新しいモデルをオフライン学習するぞ!」ってなった時に、**on-demandでfeature pipelineをbackfillしてその場で古いバージョンの特徴量レコードを作ればいい気もしてます**。
ただまあSagemaker Feature Storeの場合はオフラインストアがS3なので、大量に古いバージョンの特徴量レコードを1年くらい保存しててもそこまでコスト的に問題にはならないのかな?? まあここは検討ポイントですね...!:thinking:

