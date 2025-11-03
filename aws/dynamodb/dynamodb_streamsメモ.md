## refs:

- [DynamoDBストリーム活用法｜データ処理を効率化する方法とは？](https://book.st-hakky.com/data-platform/dynamodb-streams-usage)
- [チャネルコーポレーションのアーキテクチャモダナイゼーション：Amazon DynamoDB 活用事例パート 2 ストリーム](https://aws.amazon.com/jp/blogs/news/how-channel-corporation-modernized-their-architecture-with-amazon-dynamodb-part-2-streams/)
- [DynamoDB ストリームとは](https://zenn.dev/mn87/articles/7a0ecbe48659e9)
- [DynamoDB Streams の変更データキャプチャ](https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/Streams.html)

## これは何??

- 特にMLパイプラインにおけるストリーミングパイプラインの構築に役立つ、DynamoDB Streamsの活用について気になったので調べてるメモ。

## 事前に知っておくべきこと

- DynamoDBとは?
  - オンラインDB用途で使われるAWSサービス。
  - フルマネージド型のNoSQLデータベースサービスで、高速で柔軟なスケーラビリティを提供。
- DynamoDB Streamsとは?
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

