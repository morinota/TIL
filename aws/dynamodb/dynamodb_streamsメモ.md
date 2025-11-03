## refs:

- [DynamoDBストリーム活用法｜データ処理を効率化する方法とは？](https://book.st-hakky.com/data-platform/dynamodb-streams-usage)
- [チャネルコーポレーションのアーキテクチャモダナイゼーション：Amazon DynamoDB 活用事例パート 2 ストリーム](https://aws.amazon.com/jp/blogs/news/how-channel-corporation-modernized-their-architecture-with-amazon-dynamodb-part-2-streams/)

## これは何??

- 特にMLパイプラインにおけるストリーミングパイプラインの構築に役立つ、DynamoDB Streamsの活用について気になったので調べてるメモ。

## 事前に知っておくべきこと

- DynamoDBとは?
  - オンラインDB用途で使われるAWSサービス。
  - フルマネージド型のNoSQLデータベースサービスで、高速で柔軟なスケーラビリティを提供。
- DynamoDB Streamsとは?
  - DynamoDBテーブルのアイテムに対する変更（追加、更新、削除）をリアルタイムでキャプチャする機能。
  - ストリームを使用することで、データの変更をトリガーにして他のAWSサービスやアプリケーションと連携することが可能。

## DynamoDB Streamsの活用事例: チャネルコーポレーション(海外企業)の場合

- 時系列に並んだ一連のイベントを"ストリーム"と呼ぶ。
  - **DynamoDBは、Streamとして変更データキャプチャ(CDC)を実行する2つの方法を提供**されてる。
    - Amazon DynamoDB Streams
      - DynamoDB テーブル内のアイテムレベルの変更の時系列順のシーケンスをキャプチャし、この情報を最大 24 時間ログに保存する。
    - Amazon Kinesis Data Streams
      - Amazon Kinesis Data Streams は、DynamoDB テーブル内のアイテムレベルの変更をキャプチャし、それらを Kinesis データストリームに複製する。


チャネルコーポレーション は、これらのサービスを使用して、**DynamoDB の変更データをストリームを介して検索性能の高いサービス(OpenSearch Service)に連携**してるらしい。

```
