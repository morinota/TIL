## refs:

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-replication-tables.html

## AWS 公式のS3 Tables replication機能のメモ

### 概要: 

>Amazon S3 Tables support automatic replication of Apache Iceberg tables stored in Amazon S3 table buckets. Replication destinations can be within the same AWS Region, across multiple AWS Regions, the same account, or to other AWS accounts.

- Amazon S3 Tables は、テーブルバケットに保存された Apache Iceberg テーブルを **自動でレプリケーション（複製）**する機能をサポートしてる。
  - **レプリケーションの宛先 (replica destination) は、同じリージョン内でも複数リージョンでも、同じAWSアカウントでも他のアカウントでもOK!**

>🔹By configuring replication for your tables, you can maintain read-only replicas of your data across multiple locations. 
> 🔹You can use replicas to enhance data availability, meet compliance requirements and increase access performance for distributed applications.
> 🔹S3 Tables replication maintains data consistency by committing all table updates…

- レプリケーションを設定すると、いろんな場所に読み取り専用のレプリカ(コピー)を維持できるようになる。
  - これによって、データの可用性(data availability)を高めたり、コンプライアンス要件を満たしたり、分散アプリケーションのアクセスパフォーマンスを向上させたりできる。
  - S3 Tablesのレプリケーションは、すべてのテーブル更新をコミットすることでデータの一貫性を維持する。
    - (つまり本番に書き込む時に、dev環境へのcommitも同時に行うイメージかな...!:thinking:)

### S3 Tables　レプリケーションを使うタイミング

- レイテンシ（待ち時間）を下げたい時 → 地理的に離れたユーザーに近い場所にレプリカ置いたら早くアクセスできる！
- 規制対応が必要な時 → 特定リージョンやアカウントにデータを置きたい場合にも使える！
- 分析の集中管理 → 複数リージョンのデータを中央リージョンでまとめてクエリしたい場合に便利！
- **テスト/開発に本番データ使いたい時 → 本番テーブルの読み取り専用コピーを別環境に作れる！**

### S3 Tables レプリケーションの設定方法

- ソーステーブルに対して、**最大5つのレプリケーション宛先(destination)**を設定できる。
- 設定は、バケット全体単位(=中の全テーブルに適用)と、特定テーブル単位(=個別に設定)の両方で可能。
- 設定方法は、公式ドキュメントではAWSコンソール / AWS CLI でどう設定するかが書かれてる。

- 必要なもの:
  - ソース側のテーブルバケット。
  - destination側のテーブルバケット(s)。
  - ソーステーブル。
  - IAMロール (S3がレプリケーションを実行できる権限を持つIAMロール)。
- バケットレベルのレプリケーション:
  - そのバケットの 既存テーブルも、新しく作られるテーブルも、全て自動でレプリケーションされる。
- テーブルレベルのレプリケーション:
  - 個別テーブル単位で設定する場合は、バケット単位の設定よりも優先される。
- **クロスアカウントでのレプリケーションの追加要件**:
  - 送信先バケットポリシーで、ソース側アカウントにレプリケートの権限を付与。
  - **宛先アカウントの ID／テーブルバケット ARN**を指定する必要がある。

### S3 Tables レプリケーションの仕組み

- Apatch Icebergテーブルの読み取り専用レプリカを、異なるAWSリージョンや異なるAWSアカウントに自動で作成する仕組み。
- 仕組み:
  - destination bucket(s)に対して、ソースと同じ名前・名前空間で読み取り専用のIcebergテーブルを作成する。
  - ソーステーブルの最新状態でレプリカをbackfillする(初回コピー)。
  - その後も、ソーステーブルの更新を監視。
  - 更新があったら、元と同じ順序でレプリカにcommitして整合性をキープ。

## 関連して、AthenaのCTAS(Create Table As Select)操作について!

- refs:
  - https://docs.aws.amazon.com/athena/latest/ug/ctas.html?utm_source=chatgpt.com

- CREATE TABLE AS SELECT（略して CTAS）クエリは、**別のクエリのselectの結果から新しいテーブルをAthena上に作成**する。
- CTASクエリは何のために使えるか??
  - その1: rawデータを繰り返しクエリせずに、1ステップでテーブルを作成する。
  - その2: クエリ結果を加工して、icebergテーブル形式とかに変換・移行する。
  - その3: クエリ結果を、ParquetやORCなどの列指向ストレージ形式に変換することで、後続クエリの性能・コストを最適化する。
  - **その4: 必要なデータだけが入った、既存テーブルのコピーを作る。**
