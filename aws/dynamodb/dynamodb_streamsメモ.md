## refs:

- [DynamoDBストリーム活用法｜データ処理を効率化する方法とは？](https://book.st-hakky.com/data-platform/dynamodb-streams-usage)
- [チャネルコーポレーションのアーキテクチャモダナイゼーション：Amazon DynamoDB 活用事例パート 2 ストリーム](https://aws.amazon.com/jp/blogs/news/how-channel-corporation-modernized-their-architecture-with-amazon-dynamodb-part-2-streams/)
- [DynamoDB ストリームとは](https://zenn.dev/mn87/articles/7a0ecbe48659e9)
- [DynamoDB Streams の変更データキャプチャ](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/Streams.html)

## これは何??

- 特にMLパイプラインにおけるストリーミングパイプラインの構築に役立つ、DynamoDB Streamsの活用について気になったので調べてるメモ。

## 事前に知っておくべきこと

### DynamoDBとは?
  - オンラインDB用途で使われるAWSサービス。
  - フルマネージド型のNoSQLデータベースサービスで、高速で柔軟なスケーラビリティを提供。

### DynamoDB Streamsとは?
- **DynamoDBのテーブルで発生したデータの変更（追加・更新・削除）をリアルタイムでキャプチャして、最大24時間ストリームとして保持してくれる機能**。
- メリット:
  - 各ストリームレコードは、ストリームに 1 回だけ出現。
  - DynamoDB テーブルで変更された各項目について、ストリームレコードは項目に対する実際の変更と同じ順序で出現。
  - DynamoDB ストリーム は、ストリームレコードをほぼリアルタイムで書き込むため、これらのストリームを使用し、内容に基づいてアクションを実行するアプリケーションを構築できる。
  - ストリームとLambdaを関連づけることによって、ストリームにデータが書き込まれるとLambdaが起動されてイベントを処理することができるようになる。
- DynamoDB Streamsに関する用語:
  - ストリームレコード: DynamoDBテーブル内の1アイテムのデータ変更を表すレコード。
  - シャード: ストリームレコードの集合。
  - ストリーム: ストリームレコードとシャードを含む全体。
- DynamoDB Streamsの有効化について:
  - 新しいDynamoDBテーブル作成時に有効化可能。
  - また、既存のDynamoDBテーブルに対しても後から有効化/無効化可能。
  - DynamoDB Streamsは非同期的に動作するので、DynamoDBテーブルのパフォーマンスに影響はない。
- DynamoDB Streams APIが提供してること:
  - `ListStreams`: 現在のストリーミング記述子のリストを返す。必要に応じて、特定のテーブル名でフィルタリング可能。
  - `DescribeStream`: 指定されたストリームの詳細情報を返す。

## ざっくりDynamoDB Streams × Lambdaの連携について

- refs:
  - [https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/with-ddb.html](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/with-ddb.html)
- DynamoDB Streamsでは、Lambda関数を使用して、DynamoDBテーブルが更新されるたびに追加の作業を実行できる。
  - **event source mapping**を使用して、DynamoDB StreamsとLambda関数を関連付ける必要がある。
    - 複数のevent source mappingを使用して、複数のlambda関数で同じストリーミングデータを処理したり、1つの関数で複数のストリームを処理したりできる。
- Lamdbaは2種類の方法でDynamoDB Streamsからデータを取得できる: **ポーリングストリーム**と**バッチストリーム**。
  - デフォルトではポーリングストリームを使用する。
    - この場合、Lambdaは新しいストリームレコードが利用可能になると同時に関数を呼び出す。
  - 前者で効率悪くなる場合、バッチストリームを使用する。
    - 具体的には、「バッチ処理ウィンドウ」を設定して、最大5分間bufferしてから一括処理することが可能。
- 注意点: **パイプライン内の実装は冪等であるべき!**
  - Lambda event source mappingは、各イベント(=ストリームレコード)を**少なくとも1回処理する(=at-least-once delivery)ことを保証**する。
  - 逆に言えば、同じイベントを重複して処理してしまう可能性がある。
  - なので、Lambda関数の実装は冪等にすることが強く推奨されてる。

## DynamoDB Streamsの活用事例: チャネルコーポレーション(海外企業)の場合

- 時系列に並んだ一連のイベントを"ストリーム"と呼ぶ。
  - **DynamoDBは、Streamとして変更データキャプチャ(CDC)を実行する2つの方法を提供**されてる。
    - Amazon DynamoDB Streams
      - DynamoDB テーブル内のアイテムレベルの変更の時系列順のシーケンスをキャプチャし、この情報を最大 24 時間ログに保存する。
    - Amazon Kinesis Data Streams
      - Amazon Kinesis Data Streams は、DynamoDB テーブル内のアイテムレベルの変更をキャプチャし、それらを Kinesis データストリームに複製する。


チャネルコーポレーション は、これらのサービスを使用して、**DynamoDB の変更データをストリームを介して検索性能の高いサービス(OpenSearch Service)に連携**してるらしい。


以下はDynamoDB Streamsを使用したワークフロー:

```
Amazon DynamoDB
    | (1) DynamoDB Streams captures item-level changes
    v
DynamoDB Streams
    | (2) AWS Lambda processes stream records
    v
AWS Lambda
    | (3) Upsert Data or delete data
    v
Amazon OpenSearch Service
```

- 特性:
  - **DynamoDB Streamsからの読み取りは、AWS Lambdaベースのconsumerにとって無料**。
  - **重複が削除された、時系列順のアイテムレベルの変更sequence**を提供する。

## DynamoDB StreamsのデータをS3に永続化する例:

- そもそも?
  - ストリーミングデータをS3に永続化する必要があるかは迷いどころかも。
  - ストリーミング処理でMLパイプラインを実現するとしたら、DynamoDB Streamsから直接Lambdaを起動して特徴量生成/学習/推論しちゃっていいかもしれない。
- DynamoDB StreamsのデータをS3に連携するメリット:
  - 永続化: 24時間の制約がなくなる。
  - 再処理可能: S3に残ってるため、失敗時の再処理が容易。
  - コスト効率: 一旦S3に集約してからバッチ処理する方が、Lambda連続実行より安い場合がある。

このパターンのアーキテクチャ例:

```
DynamoDB Table (Streams有効化)
    | 
    v
DynamoDB Streams (最大24時間保持)
    | 
    v
Kinesis Data Firehose (ストリーミング配信サービス)
    | Buffer and batch data
    v
S3 (永続化・長期保存)
    |
    v
ex. 後続のバッチ処理達??
```

- Kinesis Data Firehoseざっくりメモ:
  - フルマネージド型のストリーミングデータ配信サービス。
    - **リアルタイムデータを自動的に様々な送信先（S3、Redshift、OpenSearchなど）に配信してくれる**。
    - 従量課金(GB単位)
  - 特徴:
    - フルマネージド型。
      - サーバー管理不要。自動スケーリング。インフラの構築・運用が不要。
    - buffering機能。
      - ストリーミングデータを一時的にバッファリングし、指定した条件（サイズや時間）でまとめて送信可能。
        - size buffering: ex. 1MBに達したら送信
        - time buffering: ex. 60秒経ったら送信
  - よくある使われ方:
    - パターン1: DynamoDB Streams → Firehose → S3
    - パターン2: アプリケーション → Firehose → S3 (アプリケーションログの保存など)

```typescript
// firehoseの定義の例
new firehose.DeliveryStream(this, "DeliveryStream", {
    deliveryStreamName: `${envName}-dynamodb-streams-to-s3`,
    // あれ? srcの情報はどこで指定するんだっけ?
    // ここで配信先やbuffering設定を指定
    destination: new destinations.S3Bucket(bucket, {
        bufferingInterval: cdk.Duration.seconds(60),
        bufferingSize: cdk.Size.mebibytes(5),
        compression: destinations.Compression.GZIP,
        dataOutputPrefix: "my-data/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/",
    }),
});
```

