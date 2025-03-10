## refs

- noteのバッチ推論結果をDynamoDBに保存してる事例: https://note.com/mussso/n/nb662ad4e6d73
- DynamoDBの基礎と設計: https://speakerdeck.com/_kensh/dynamodb-design-practice
- Amazon DynamoDB のベストプラクティスに従うという 2019 年の計を立てる: https://aws.amazon.com/jp/blogs/news/resolve-to-follow-amazon-dynamodb-best-practices-in-2019/
- [DynamoDBでできないこと](https://zenn.dev/hsaki/articles/aws-dynamodb-non-suited)
- [Rustによる並列処理でDynamoDBへのデータ投入を20倍高速化してみた](https://zenn.dev/chiku_dev/articles/b4e068680e2b2e)

## note社のDynamoDB利用事例

- 概要: note記事レコメンド機能のAWSアーキテクチャをリファクタリングした話。
  - アーキテクチャの全体像。ざっくり以下の3種のプロセスを実行してる
    - モデル学習プロセス
    - モデルのバッチ推論プロセス
    - バッチ推論結果のDynamoDB登録プロセス
- 旧アーキテクチャの特徴
  - SQSを責任分界点として、**SQSの左側(consumer)がnoteリポジトリ、SQSの右側(Producer)がMLリポジトリ**、という風にGithubリポジトリが分かれている。
    - noteリポジトリ側のbatchサーバーは、SQSから下記のようなuser_id毎の推薦記事リストデータを受け取って、DynamoDBに登録する処理を実行している。

```
{
    "data":[
        [user_id1, [推薦記事id1, 推薦記事id2, ... 推薦記事id100]], 
        [user_id2, [推薦記事id1, 推薦記事id2, ... 推薦記事id100]],
        [user_id3, [推薦記事id1, 推薦記事id2, ... 推薦記事id100]],
        ...
    ]
}
```

### 旧アーキテクチャの問題点

- 1. noteリポジトリとMLリポジトリの責任分界点
  - 前者はRuby、後者はPythonで実装されている。
  - **パイプライン全体を改善したい場合には、RubyとPythonの両方が書けるエンジニアしか対応できないので、開発がやや難しくなる**。
- 2. スケジュール駆動
  - noteリポジトリ側のbatchサーバは、1時間おきにSQSを見にいくというアーキテクチャになっていた。
    - SQSメッセージがない場合でもメッセージを取得しにいくという**無駄な処理が発生**。
    - また、SQSに最新の推薦データが入ったとしても、noteリポジトリ側のbatchサーバーがSQSメッセージを取りに来るまでに待ち状態が発生。よって**作った推薦結果を即座にユーザーインターフェースに反映できない**。
  - (この観点は重要だ...!:thinking:)
- 3. 処理の失敗があまり想定されていない。
  - 内部的にリトライ処理はしているのですが、失敗したメッセージをどこかにキューイングしておく仕組みではないため、失敗したメッセージは実質無視されている。
- 4. スケールアップ構成
  - noteリポジトリ側はデカいインスタンスで一気にSQSのメッセージを吸い取ってDynamoDBに登録するようなアーキテクチャになっているため、**単一障害点**になっていた。
    - 単一障害点についてメモ!
      - もしこの1台のインスタンスが停止、故障など動作しなくなった場合、全体の処理が完全にストップしてしまう。
      - 

### リファクタリング後のアーキテクチャ

- バッチ推論結果のDynamoDB登録プロセスの処理をリファクタリングした。
  - 責任分界点だったSQSの次にLambdaを置いて、noteリポジトリ側のbatch処理を削除。

リファクタリング後の改善点

- 1. MLチームのみで改善が完結する
  - 以前は、**noteリポジトリとMLリポジトリの責任分解点が微妙だったことで**、パイプライン全体を改善したい場合には、RubyとPythonの両方が書けるエンジニアしか対応できない状態だった。
  - 今回のリファクタリングにより、**MLチーム側の環境で機能改善が完結するので、改善活動がしやすくなった**。
- 2. イベント駆動
  - 以前は、1時間おきにSQSを見にいくというスケジュール駆動なアーキテクチャだった。
    - そのデメリットは前述。
  - 今回のリファクタリングにより、SQS+Lambdaの構成にすることでイベント駆動なアーキテクチャに変更。
    - SQSに届いたメッセージはすぐLabmdaが起動してDynamoDBに登録されるので、**推薦結果をすぐにユーザへ提供できるようになった**。

- 3. 失敗を想定したアーキテクチャ
  - SQS+Lambdaの構成の場合、基本的には処理の失敗を考慮してDLQ(Dead Letter Queue)を設定することが基本なので、失敗したジョブやメッセージはDLQに溜められて、後からDLQの再処理を実行できる。
    - **とりあえず失敗してもやり直せる**、という安心感。
    - 参考: https://dev.classmethod.jp/articles/sqs-dead-letter-queue-metrics-for-alert/
- 4. スケールアウト構成
  - **SQS + Lambdaの構成はスケールアウト構成になっているので、「もう少し同時実行数上げられそうだなぁ」と思ったら、Lambdaの同時実行数を上げれば良い**。
  - また「ちょっと処理が重くてタイムアウトが発生しそうだなぁ」と思ったら、Lambdaのメモリサイズを増加したり、SQSから受け取るメッセージ数を減らす、といった細かいチューニングもしやすい。

実際のLambdaのコードの雰囲気

```python
def lambda_handler(event: Dict[str, str], context: Dict) -> None:
    """
    SQSイベントを受け取り、RDS Proxyからユーザー情報を読み取り、DynamoDBに記事レコメンド結果を格納する
    Args:
        event: SQSイベントから渡されるデータ(メッセージ)
        context: ランタイム情報(ex. timeoutやログストリーム情報)を含む辞書
    """

    # SQSイベントを受け取る
    logger.info(event)
    try:
        recom_items = []

        # 内部でRDS Proxyを使ってRDSに接続のでwithでwrapしてる?
        with pymysql.connect(**mysql_info) as conn:
            # SQSメッセージを1つずつ処理
            for message in event["Records"]:
                body: Dict[str, str] = json.loads(message["body"])
                
                for sqs_message in body["data"]:
                    user_id, note_ids = sqs_message
                    # RDS Proxyからユーザ情報を読み取り、SQSイベントと照合する(あんまりやってること分かってない)
                    recommended_items = select_from_rds(conn, user_id, note_ids)
                    insert_item = {
                        "user_id": user_id,
                        "recommended_note_ids": recommended_items,
                    }
                    recom_items.append(insert_item)
        # DynamoDBに記事レコメンド結果を格納する
        DynamodbRecommendedNotes.bulk_update(recom_items)
    except Exception as e:
        logger.error(str(e) + '\n' + traceback.format_exc())
        raise e
```

### 気づき

#### 責任分界点の決定は重要:
  - 今回は**MLチームが改善活動をしやすくするために**、noteリポジトリとMLリポジトリの責任分界点を変更した。
    - ちなみに...「責任分界点」とは??
      - 複数の主体（組織、チーム、システムなど）の間で、それぞれの責任範囲を明確に区分する境界のこと。
  - このような「どこを責任分界点とするのか」という話はどのようなシステムでもありそう。
    - ex. 
      - APIを作る側が基盤チーム、APIを利用する側がビジネス開発チーム
      - DBを作って登録する側が基盤チーム、DBを利用する側がビジネス開発チーム
    - **どこを責任分界点にすればみんながハッピーになれるのか**というのは早めに計算して決め切るのが重要なポイントかも。
    - **可能であれば、複数開発言語を用いないような環境や、複数リポジトリを跨いだりする手間のないようなシステム構成がやりやすいのでは**。
  - コンウェイの法則とかの観点も関係ありそう。要件やチーム組織次第で最適解は変わってくるはず。
    - ちなみにざっくり「コンウェイの法則」: **システムの構造は、それを設計する組織のコミュニケーション構造に従う。**
    - 参考: https://medium.com/i35-267/%E3%82%B3%E3%83%B3%E3%82%A6%E3%82%A7%E3%82%A4%E3%81%AE%E6%B3%95%E5%89%87%E3%81%A8%E9%80%86%E3%82%B3%E3%83%B3%E3%82%A6%E3%82%A7%E3%82%A4%E3%81%AE%E6%B3%95%E5%89%87%E3%81%8B%E3%82%89%E7%B5%84%E7%B9%94%E6%A7%8B%E9%80%A0%E3%82%92%E8%80%83%E3%81%88%E3%82%8B-bf3f32ebb022
####  スケジュール駆動 vs イベント駆動
  - 前提として、深夜のバッチ処理などはスケジュール駆動なアーキテクチャがふさわしい。
  - しかし、スケジュール駆動のアーキテクチャのシステムが多くなってくるといくつか問題が生じるポイントがあるのかも。
    - ex. 
      - **毎分や毎秒でポーリング（定期的な状態チェック）を行う場合、必要のないタイミングでも処理が実行されることが**あり、リソースが無駄になる。
      - 指定した時間にならないと推論結果がデータベースに反映されないというシステムだとユーザ体験に影響を与える可能性がある。
#### オーケストレーション vs コレオグラフィ
  - マイクロサービスでワークフローを構築する際にいくつかパターンがある。
    - **オーケストレーション**:  Step Functionのような全体ワークフローの指揮者が、LambdaやSageMakerなどの各種サービスを制御するパターン
    - **コレオグラフィ**: SQS/Lambdaのようにイベントのpubsubによってサービス間の結合をして全体ワークフローの指揮者のような存在がいないパターン
  - どのようなアーキテクチャパターンがみんなにとって幸せなのかというのは、全体システムの要件定義やシステム設計段階でちゃんと考えておきたい。
  - 参考: https://theburningmonk.com/2020/08/choreography-vs-orchestration-in-the-land-of-serverless/

#### 単体のデカインスタンス vs 大量のミニインスタンス

- **大量のメッセージをキューイング/処理して、失敗したメッセージがあれば簡単に再処理実行したいという場合**...
  - Lambdaみたいな小さいインスタンスを利用して同時並列性が高くなるような仕組みを使った方が良さそう。
- 画像の加工などの**重たいデータ処理の場合**...
  - SageMaker TrainingJob/EC2のようなデカインスタンスのマシンパワーで殴るみたいにした方が良さそう。
  - また、**大きいタスクでも分割してLambdaで処理できるレベルにブレークダウンする**、という考えもある。
- Lambdaは昔に比べてかなりアップデートされているので、使えるユースケースは増えている。
  - 著者は、**システム設計の初めの段階でLambdaが使えるユースケースかな？**と考える思考回路になってるとのこと。

### 実装のしやすさんい関する感想

#### RDS Proxyはエポックメイキング(=画期的な、歴史的に重要な、という意味らしい!:thinking:)

- 背景
  - **RDS + Lambdaはかつてアンチパターンだった**。
    - Lambdaはサーバーレスで短期間に大量のインスタンスをスケールアウトするが、**RDSはコネクションの上限があるため、Lambdaから直接接続するとコネクションが枯渇する問題が発生**。
    - これが「RDS + Lambda」がかつてアンチパターンとされていた理由。
- RDS Proxyの登場
  - RDS Proxyが解決
    - RDS Proxyは**接続プールを管理**する仕組みを提供し、Lambdaの大量並列実行による接続問題を解消。
    - RDS Proxyを導入すると、**Lambdaから直接RDSに接続する代わりに、RDS Proxyを介して接続する形**になる。 -> (消費するコネクション数は1つになるってこと??:thinking:)
  - 使い方が簡単
    - 既存のRDSエンドポイントを、RDS Proxyが提供するエンドポイントに切り替えるだけで利用可能。
- 感想
  - Lambdaを使ったスケーラブルなアプリケーションの構築が容易になった。

#### 用意されたLambda Layersを使うと楽

- 背景
  - Lambdaの制約
    - Lambda関数には、デプロイ時にライブラリや依存関係を含める必要がありますが、これが煩雑になり得る。
    - 特に、サイズが大きいライブラリ（例:numpy, pandasなど）はアップロードの手間がかかる。
- Lambda Layersとは
  - Lambda関数で共通して使用する依存ライブラリや設定を**独立したレイヤーとして管理し、複数の関数で共有できる仕組み**。
    - (コンテナイメージみたいな感じかな??:thinking:)
  - これにより、ライブラリの準備やアップロードの手間を大幅に削減できる。
  - 参考: https://github.com/keithrozario/Klayers
- メリット: 開発の効率化
  - よく使われるライブラリ（numpy, pandasなど）は、AWSが公式に提供しているLambda Layersを利用することで、独自にパッケージ化する必要がない。
  - コードが軽量化し、アップロードも速くなる。

#### 負荷に関するパラメータチューニングはムズイ

- 背景
  - 本番環境での負荷問題:
    - **サーバーレスアーキテクチャ（Lambda, SQS, DynamoDBなど）では、パラメータチューニングが適切でないと、負荷が集中した場合にシステム全体が不安定になる可能性**がある。
- 具体的な課題
  - 1. Lambdaのスロットリング
    - **Lambdaには同時実行数の上限**があるため、処理が多すぎるとスロットリング（リクエスト抑制）が発生。
    - スロットリングが発生するとリトライが行われますが、リトライ回数を超えるとSQSの**DLQ（デッドレタキュー）**にメッセージが送られる。
  - 2. DynamoDBの書き込みキャパシティ
    - DynamoDBの書き込みキャパシティ（WCU: Write Capacity Unit）が足りないと、書き込みリクエストが失敗する可能性がある。
  - 3. SQSのメッセージバッチ処理
    - SQSのバッチサイズ（1リクエストで処理するメッセージ数）が適切でない場合、効率が悪くなる。
- 解決策
  - 負荷試験の重要性:
    - **本番環境に近い環境で負荷試験を行い、パラメータ（同時実行数、WCU、タイムアウト、バッチサイズなど）を調整**する。
  - 失敗を許容するアーキテクチャ:
    - 完璧な設定を目指すのではなく、失敗を前提とした仕組みを取り入れる（例:DLQで失敗メッセージを一時保存し、後から再処理）
- 感想
  - 本番環境の負荷チューニングは難しいが、DLQなどの仕組みを使えば問題を最小限に抑えられる。
  - メトリクスを定期的に確認し、適切なチューニングを継続的に行う必要がある。


## DynamoDBの基礎と設計のメモ

- Amazon DynamoDBの構成
  - Key-Valueという単純な構造。
    - これにより...
      - テーブルのデータ量に関係なく高速なレスポンス
      - 1日に10兆件以上のリクエスト処理可能
      - 毎秒2,000万件を超えるリクエストをサポート
- 料金体系
  - 設定したReadキャパシティユニット（RCU）, Writeキャパシティユニット（WCU）
  - ストレージ利用料

### DynamoDBの用語

概要

- **Item**: テーブル内の1行に相当
- **Attribute**: Item内の1列に相当
  - **注意: Primary Key以外は、Item間で不揃いであっても問題ない**。
- **Primary Key**: テーブル内の各Itemを一意に識別するためのキー
  - DynamoDBでは2種類のPrimary Keyをサポート
    - **Partition Key**
    - **Partition Key + Sort Key**

### DynamoDBにおけるテーブル設計の概要

#### ざっくりDynamoDBの設計できる項目について

- 1. DynamoDBでは2種類のPrimary Keyをサポートする。
  - **Partition Key**: 同じPartition Keyを持つItemは登録できない。
  - **Partition Key + Sort Key**: Partition KeyとSort Keyがともに同じItemは登録できない。
- 2. DynamoDBでは、2種類の**Secondary Index**を利用することができる。
  - (前提として、Secondary Indexとは、Primary Key以外の属性をキーとして、テーブルのデータを別の方法で検索できるようにする仕組み...!:thinking:)
  - **Local Secondary Index(LSI)**:
    - Sort Key以外に絞り込み検索を行うKeyを持つことができる。
    - Partition Keyはベーステーブルと同じ / Sort Keyが異なる
    - ex.) LSIの例
      - 4種類のカラム(customer_id, order_id, book_name, price)を持つテーブルを想定する。
      - primary keyとして「partition key=customer_id & sort key=order_id」を設定済み。
      - **ここで、Local Secondary Indexとして、「partition key=customer_id & sort key=price」を設定することで、「ある顧客のある注文」以外に、「ある顧客のいくらの注文」も検索可能になる! (なるほど、やっとわかった...!:thinking:)**
  - **Global Secondary Index(GSI)**:
    - Partition Key属性の代わりとなる、Partition Keyをまたいで検索を行うためのインデックス。
- 3. キャパシティユニットの考え方:
  - **Readキャパシティユニット**: 1ユニットにつき、最大4KBのデータを1秒間に1回読み込み可能
    - （強い一貫性を持たない読み込み設定であれば、1秒あたり2回）(? トランザクション分離レベルっぽい話かな...!:thinking:)
  - **Writeキャパシティユニット**: 1ユニットにつき、最大1KBのデータを1秒間に1回書き込み可能
  - 考え方の例:
    - **ピーク時は、1KB以下のデータが秒間80回書き込まれる -> 少し余裕を見て、Writeキャパシティは100にしよう...!**
    
### DynamoDBにおけるデータの操作方法

- HTTPベースのAPIで操作を行う。
- 例:
  - データの作成: PutItem, BatchWriteItem
  - データの更新: UpdateItem(対象ItemのKeyを指定して更新)
  - 単一データの取得: GetItem(対象ItemのKeyを指定して取得)
  - 複数データの取得: Query, Scan


### DynamoDBの設計

- 前提: DynamoDBの知識とベストプラクティス
  - (参考: https://speakerdeck.com/_kensh/dynamodb-design-practice?slide=34)
  - **テーブルの数は最小限に留める**。
    - １箇所にあるデータに、テーブルやインデックスを通じアクセスすることで、望む形のデータが入手しやすいように構成。
    - キャパシティユニットの消費を抑えるためにも重要。
    - テーブルを分けるべき例外はある。
  - DynamoDBは、Primary Key(**Partition Key**(PK)、またはPK + **Sort Key**(SK)の複合)でデータを識別し、アクセスする。
    - ScanまたはQuery等のAPI利用
  - グローバルセカンダリインデックスは、元テーブルから非同期レプリケーションされる別テーブルのような存在。
  - 1テーブルや1インデックスに複数種類のアイテム(=行!)を持たせても良いし、**1属性(=カラム!)に複数種類の値を入れてもよい**。
- DynamoDBの設計プロセス
  - 1. 業務分析とデータのモデリング
    - 対象ドメインのデータをモデリング。RDB設計と同じく、ER図による概念と論理レベルの整理は有効。
  - 2. アクセスパターン設計
    - ビジネス要件から、**アプリケーションで必要な機能とデータ(アクセスパターン)を整理**する。たとえば「**従業員情報をIDで検索する**」など。
  - 3. TableとIndex設計
    - ユースケースを満たせるテーブル及び、インデックスのスキーマを設計する
  - 4. クエリ条件設計
    - クエリの詳細を設計、定義する
    - **ユースケースごとに利用するパラメータ、インデックス、検索条件などを書き出す**。
  - 5. 追加要件が生じたら??
    - サービスに合わせてテーブル・インデックス設計を変更する
    - 他のサービスと連携する、etc.

- DynamoDBのよくある誤解の一つ
  - 「DynamoDBってスキーマレスだから、事前の設計いらないでしょ??」
  - -> No! アクセスパターンに基づいた設計が必要！

## DynamoDBの料金の仕組みメモ

- 参考:
  - https://aws.amazon.com/jp/dynamodb/pricing/on-demand/

- ざっくりDynamoDBでは、テーブル内の**データの保存、読み取り、書き込み**が課金対象になる。
- データの保存
  - **テーブルのクラスによって異なる**。
    - DynamoDB Standard: 1GBあたり、0.285USD/月
    - DynamoDB Standard-IA: 1GBあたり、0.114USD/月
  - 両クラスの比較
    - **通常はStandardクラスを利用することが多い**。
    - 一方で、アクセス頻度の低いデータを大量に保存するようなユースケースでは、Standard-IAを使用するとコストを60%カットできる。
      - >DynamoDB Standard-IA テーブルクラスは、アプリケーションログ、古いソーシャルメディアの投稿、e コマースの注文履歴、過去のゲームの実績など、アクセス頻度の低いデータを長期間保存する必要があるユースケースに最適です。
      - 引用: [Amazon DynamoDB が、DynamoDB コストを最大 60% 削減するのに役立つ新しい Amazon DynamoDB Standard-Infrequent Access テーブルクラスを発表](https://aws.amazon.com/jp/about-aws/whats-new/2021/12/amazon-dynamodb-standard-infrequent-access-table-class/)
    - また、**Standardクラスには無料枠25GB/月**がある。
      - (バッチ推論結果とか、基本的に無料枠を超えることはないかも...!:thinking:)
- データの読み取り/書き込み
  - 現時点では、**大きく2つのキャパシティモード**が用意されており、料金計算が異なる。
    - on-demandキャパシティモード:
      - 実行したデータの**読み取り/書き込みリクエスト**(RRUとWRU)に対して課金。
        - この100万単位あたりの料金が、2024年11月14日から半額になったらしい。
      - 読み取りと書き込みのthroughput予測値を指定する必要がない。
    - provisionedキャパシティモード:
      - 1秒あたりの**読み込みと書き込みの回数**(RCU, WCU)を指定。Auto Scalingも可能。
  - 料金計算における単位についてメモ:
    - 「読み取りリクエスト単位(RRU)」:
      - データを読み込む際は、テーブルに対してAPIコールする必要がある。このとき、**読み込みリクエストという単位で課金が発生**する。
      - **on-demandキャパシティモードでStandardテーブルクラスの場合、100万RRUあたり0.1425USD**
      - 読み込みリクエストには、以下の3種類があり、それぞれ消費するRRUの数が異なる。
        - 「結果整合性のある読み込み(Eventually Consistent Read)」
          - **基本的にはこれを使うらしい！**
          - **一回のリクエストで0.5単位のRRUが消費される(4KBまで)**。
          - ex. 8KBの項目を読み込む場合、1単位のRRUが消費される...!:thinking:
        - 「強い整合性のある読み込み(Strongly Consistent Read)」
        - 「トランザクション読み込み(Transactional Read)」
    - 「読み取りキャパシティユニット(RCU)」
      - hoge
    - 「書き込みリクエスト単位(WRU)」
      - データを書き込む際は、テーブルに対してAPIコールする必要がある。この時、**書き込みリクエストという単位で課金が発生**する
      - **on-demandキャパシティモードでStandardテーブルクラスの場合、100万WRUあたり0.715USD**
      - 書き込みリクエストには、以下の2種類があり、それぞれ消費するWRUの数が異なる。
        - 「標準書き込みリクエスト」
          - 1単位のWRUで、最大1KBまでの項目を書き込むことができる。
        - 「トランザクション書き込みリクエスト」
          - **1単位のWRUで1KBまでのデータを書き込むことができる**。
    - 「書き込みキャパシティユニット(WCU)」

## Partition Keyとsort keyの役割の違い、ホットパーティションの問題

- partition key
  - テーブル内のデータを分散させるために使用される。
  - **データの物理的な配置**を決定するために使用される。
  - 完全一致検索のみが可能。
- sort key
  - オプショナルなキーで、必須ではない。
  - **同じpartition key内のitemをソート**するために使用される。
  - 範囲検索や条件検索が可能。
    - begins_with, between, >, <, >=, <=などの演算子を使って検索が可能。
- ホットパーティション問題。
  - 特定のpartition keyに対して、読み書きが集中する現象。
  - 何が困る??
    - DynamoDBでは、テーブルに割り当てられた読み込み/書き込みcapacity unit(RCU, WCU)が各partitionに均等に分散される。
    - ホットパーティションが発生すると、**そのpartitionのcapacity unitが枯渇し、スロットリング(速度制限)が発生**する可能性がある。
      - DynamoDBには「Adaptive Capacity」機能があり、ホットパーティションが発生した場合でも、他のpartitionの余剰capacity unitを割り当てることで、スロットリングを回避する仕組みらしい。
      - まあでも基本はホットパーティション自体の発生を避けるべきだよね、という話か...!:thinking:
    - (パープレ曰く、on-demandモードでも同様に影響があるみたい、あくまで料金体系がRCU/WCUではなくRRU/WRUになるだけで、裏側の仕組みとしてはこのcapacity unitが使われてるってことなのかな...!:thinking:)
- 

## 実際にテーブルを作って色々やってみる

### cdkでテーブルを定義する

- dynamodb.Tableクラスを使ってテーブルを定義できる。
  - 参考: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_dynamodb.Table.html
  - コンストラクタのpropsには、以下のような設定がある。
    - hoge


```typescript
import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';

export class HelloCdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const table = new dynamodb.Table(this, `TempBatchRecommendations`, {
        // primary key (partition key + sort key)の設定
        partitionKey: { name: "user_id", type: dynamodb.AttributeType.STRING },
        sortKey: { name: "model_unique_name", type: dynamodb.AttributeType.STRING },
        tableName: `TempBatchRecommendations`,
        billingMode: dynamodb.BillingMode.PAY_PER_REQUEST, // on-demandモード
        removalPolicy: cdk.RemovalPolicy.DESTROY, // stack削除時にテーブルも削除する
    });
    // タグを追加(Tableクラスによらず、任意のConstructs)
    cdk.Tags.of(table).add("my_tag_key1", "my_tag_value1")
  }
}
```

### テーブルにデータを書き込んでみる

- まずはAWS CLIで、PutItem APIを使ってデータを書き込んでみる。
  - **Itemがすでに存在する場合は、そのItem全体が置き換えられる**。特定の属性のみを更新する場合は、updateItem APIを使う(バッチ推論結果の文脈では、PutItemやBatchWriteItemで十分そう...!:thinking:)。
    - >putItem メソッドによって、項目をテーブルに格納します。項目が存在する場合、その項目全体が置き換えられます。項目全体を置き換える代わりに固有の属性のみを更新する場合は、updateItem メソッドを使用できます。
    - 参考: https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/JavaDocumentAPIItemCRUD.html#JavaDocumentAPIItemUpdate


```shell
aws dynamodb put-item \
    --table-name TempBatchRecommendations \
    --item '{
        "user_id": {"S": "test_user1"},
        "model_unique_name": {"S": "test_model1"},
        "recommendation": {"S": "item1,item2,item3"}
    }'
```

- 同様にAWS CLIで、 BatchWriteItem APIを使って複数のデータを書き込んでみる。
  - **PutItem APIと同様に、Itemがすでに存在する場合は、そのItem全体が置き換えられる**。

```shell
aws dynamodb batch-write-item --request-items '{
  "TempBatchRecommendations": [
    {
      "PutRequest": {
        "Item": {
          "user_id": { "S": "test_user2" },
          "model_unique_name": { "S": "test_model1" },
          "recommendation": { "S": "item1,item2,item3" }
        }
      }
    },
    {
      "PutRequest": {
        "Item": {
          "user_id": { "S": "test_user1" },
          "model_unique_name": { "S": "test_model2" },
          "recommendation": { "S": "item4,item5,item6" }
        }
      }
    }
  ]
}'
# 以下はレスポンス(書き込めなかったItemはUnprocessedItemsに表示されるっぽい...!:thinking:)
{
    "UnprocessedItems": {}
}
```

- ちなみに、**AWS Python SDKでBatchWriteItemを使いたい場合は、`batch_writer`が便利らしい**...! 
  - 25件の制限を気にせずに裏側でよしなにやってくれるらしい。
  - あと、追加(削除)に失敗したアイテムに対するハンドリングも、裏側でやってくれてる??:thinking:
  - 参考:
    - https://dev.classmethod.jp/articles/lambda-python-dynamodb/
    - https://qiita.com/dokeita/items/2950d0ee8815730973c2

```python
TABLE_NAME = "TempBatchRecommendations"
dynamoDB = boto3.resource("dynamodb")


class BatchRecommendation(TypedDict):
    user_id: str
    model_unique_name: str
    recommendation: str


def batch_write_items(items: list[BatchRecommendation]) -> None:
    try:
        table = dynamoDB.Table(TABLE_NAME)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    except Exception as error:
        logger.error(f"Error: {error}")

df = pl.DataFrame(
        {
            "user_id": ["user1", "user2", "user1"],
            "model_unique_name": ["model1", "model1", "model2"],
            "recommendation": ["[item1, item2]", "[item3, item4]", "[item5, item6]"],
        }
    )
items = df.to_dicts()
batch_write_items(items)
```

### テーブルからデータを取得してみる

まずはAWS CLIで、単一のItemを取得するためのGetItem APIを使ってみる。

```json
% AWS_PROFILE=newspicks-development aws dynamodb get-item \
    --table-name TempBatchRecommendations \
    --key '{"user_id": {"S": "test_user1"}, "model_unique_name": {"S": "test_model1"}}'
// レスポンス
{
    "Item": {
        "recommendation": {
            "S": "item1,item2,item3"
        },
        "user_id": {
            "S": "test_user1"
        },
        "model_unique_name": {
            "S": "test_model1"
        }
    }
}
```

scan APIを使ってデータを取得してみる。
  - 返り値の各keyの意味
    - Items: クエリの結果として返された各Item
    - Count: クエリの結果として返されたItem数
    - ScannedCount: DynamoDBがscanした総アイテム数
    - ConsumedCapacity: 今回の読み取りリクエストで消費されたcapacity unitの情報

```shell
% aws dynamodb scan --table-name TempBatchRecommendations

{
    "Items": [
        {
            "recommendation": {
                "S": "item1,item2,item3"
            },
            "user_id": {
                "S": "test_user1"
            },
            "model_unique_name": {
                "S": "test_model1"
            }
        },
        {
            "recommendation": {
                "S": "item4,item5,item6"
            },
            "user_id": {
                "S": "test_user1"
            },
            "model_unique_name": {
                "S": "test_model2"
            }
        },
        {
            "recommendation": {
                "S": "item1,item2,item3"
            },
            "user_id": {
                "S": "test_user2"
            },
            "model_unique_name": {
                "S": "test_model1"
            }
        }
    ],
    "Count": 3,　# クエリの結果として返されたItem数
    "ScannedCount": 3, # DynamoDBがscanした総アイテム数
    "ConsumedCapacity": null # 今回の読み取りリクエストで消費されたcapacity unitの情報。
}
```

### テーブルのデータを更新してみる

- updateItem APIを使って、テーブル内の単一Itemを更新してみる。
  - 以下の例では、user_id=test_user1, model_unique_name=test_model1のItemについて、recommendation属性を更新している。
  - 補足:
    - 条件付き更新: `ConditionExpression`を使って、特定の条件を満たす場合のみ更新を行うこともできる。
    - 指定した属性が存在しない場合でも、新しく作成される。
    - 複数の属性を更新: `update-expression`に複数の属性を指定することで、複数の属性を一度に更新することもできる。
      - ex. `--update-expression "SET attr1 = :val1, attr2 = :val2" --expression-attribute-values '{":val1": {"S": "value1"}, ":val2": {"S": "value2"}}'`


```shell
aws dynamodb update-item \
    --table-name TempBatchRecommendations \
    --key '{"user_id": {"S": "test_user1"}, "model_unique_name": {"S": "test_model1"}}' \
    --update-expression "SET recommendation = :r" \
    --expression-attribute-values '{":r": {"S": "item7,item8,item9"}}'

# 結果は特に出力されないが、実際にはrecommendation属性が更新される
```

### テーブルからItemを削除してみる。

- AWS CLIから DeleteItem APIを使って、テーブル内の単一Itemを削除してみる。
  - DeleteItem操作でも、書き込みの一種として料金がかかる。
  - ちなみに、**指定されたprimary keyに一致するItemが存在しない場合も、エラーにならずに正常終了してしまう**。
    - なので「DeleteItemするときに対象アイテムがなければ404」という設計にしたい場合は一工夫必要らしい...!:thinking:
      - 参考: https://zenn.dev/hsaki/articles/aws-dynamodb-non-suited#:~:text=DeleteItem%E3%81%99%E3%82%8B%E3%81%A8%E3%81%8D%E3%81%AB%E5%AF%BE%E8%B1%A1%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E3%81%8C%E3%81%AA%E3%81%91%E3%82%8C%E3%81%B0404
  - 

```shell
AWS_PROFILE=newspicks-development aws dynamodb delete-item \
    --table-name TempBatchRecommendations \
    --key '{"user_id": {"S": "test_user1"}, "model_unique_name": {"S": "test_model1"}}'
```

## 大量のItemを一括で高速でかきこむためのメモ

- AWS情報センターによる回答:
  - >複数の PutItem 呼び出しを同時に発行するには、BatchWriteItem API オペレーションを使用します。また、**コード内で並列プロセスまたはスレッドを使用して、複数の並列の BatchWriteItem API 呼び出しを発行**して、データのロードを高速化することもできます。
    - 参考: https://repost.aws/ja/knowledge-center/dynamodb-bulk-upload
  - なのでこれを踏まえると、TrainingJobでバッチ推論した最後に、マルチスレッドでBatchWriteItemを使って一気に書き込む、というのは悪い手段ではないのかも...!:thinking:


- 並列化するスレッド数は、vCPUの数と一致させれば良い??
  - **CPUバウンドな処理の場合と、I/Oバウンドな処理の場合で、スレッド数の最適値は異なるっぽい...!**
  - CPUバウンドな処理の場合:
    - ex. ML推論、数値計算、etc.
    - スレッド数をCPUのコア数に合わせると良さそう。
      - スレッド数をvCPU数よりも多くすると、スレッド間でCPUのコアを共有するため、オーバーヘッドが発生し、処理速度が遅くなる可能性がある。
      - なのでvCPUとスレッド数を一致させるのが基本らしい。
  - I/Oバウンドな処理の場合:
    - I/Oバウンドとは??
      - プログラムの処理速度がCPUではなく、I/O処理(ネットワーク・ディスクなどの外部通信)によって影響を受ける場合。
      - ex. ファイル読み書き、ネットワーク通信、データベースアクセス、etc.
    - スレッド数をCPUのコア数よりも少し多めにすると良いっぽい。
      - CPUはほぼ使わず、I/O待ちがボトルネック
      - **スレッドを増やすと I/O待ち中に他のスレッドが処理を進められるため、隙間時間を有効活用でき、全体の処理速度が向上する**。
      - スレッド数の目安は、vCPU数 * 2~4位らしい。
        - (ex. vCPU数が4の場合、スレッド数は8~16程度)
        - ただしDynamoDBのスロットリング (Throttling) に注意!
          - スループット上限を超えると、`ProvisionedThroughputExceededException`が発生する可能性がある。
    
