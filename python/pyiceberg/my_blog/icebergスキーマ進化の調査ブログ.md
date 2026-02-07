タイトル: Feature Store調べてたらレイクハウスアーキテクチャに行き着いてIceberg Table formatについて調べた! スキーマ進化編!

## なんでこの記事を書いたの??

自分はMLOps分野に興味があって普段から色々調べているのですが、Feature Storeに関する書籍を読んでいたら、以下のような記述がありました。

> The offline stores for existing feature stores are lakehouses. (既存のフィーチャーストアの**オフラインストアはレイクハウス**である)

> In contrast to a data warehouse, a lakehouse is an open platform that separates the storage of columnar data from the query engines that use it. (データウェアハウスとは対照的に、レイクハウスは、**列指向データのストレージをそれを使用するクエリエンジンから分離**するオープンプラットフォームである)

> The main open source standards for a lakehouse are the open table formats (OTFs) for data storage (Apache Iceberg, Delta Lake, Apache Hudi). (レイクハウスの主なオープンソース標準は、データストレージのためのオープンテーブルフォーマット（OTF）（**Apache Iceberg**、Delta Lake、Apache Hudi）である)

元々業務関連でS3 TablesやIcebergテーブルフォーマットについてなんとな〜く調べていたので、MLOpsとIcebergが繋がった感じがしました。嬉しくなったので調べた内容を記事に残します:)
（ちなみに「レイクハウス」という言葉は初知りでした。なるほど、じゃあS3 TablesにIcebergテーブルで特徴量レコードを保存して、AthenaやSnowflakeやPyIcebergなどの任意のクエリエンジンでクエリできるようにする設計は、レイクハウスアーキテクチャの一例と言えるのか...!:thinking:）

## 前提: Apache Iceberg Table formatってなんだっけ??

### ざっくりApache Icebergとは??

- オープンソースのテーブルフォーマット (Table format)
- Netflixが開発し、Apache Software Foundationに寄贈された
- モダンなテーブルフォーマットの中で、一番人気があるっぽい

### そもそも「テーブルフォーマット (Table format)」とは??

> "A table format in the simplest term is a way to organize dataset files to represent them as a single 'table'." (テーブルフォーマットとは、簡単に言うと、データセットファイルを1つの「テーブル」として表現する方法のこと。)
> ([What's a table format and why do we need one?](https://medium.com/@shreekumar-saparia/whats-a-table-format-and-why-do-we-need-one-51373b94e1c5) より引用)

- レイクハウスアーキテクチャにおいて、テーブルフォーマットは**データレイク上のデータを管理・操作するための中間レイヤー**として機能する
  - Transaction & Metadata Layer (トランザクションとメタデータのレイヤー)!
- かなりラフな言い方をすると、**データレイクを「ちゃんとしたテーブル」として扱えるようにするための中間レイヤー**...!!:thinking:

### テーブルフォーマットがなぜ必要になったんだっけ??

データウェアハウス → データレイク → レイクハウス(with テーブルフォーマット)みたいな流れみたい。

- 1980年代に、意思決定支援のために分析クエリに最適化された専用のDBが必要に...**DWH(データウェアハウス)**が登場!
  - データウェアハウスが提供したこと:
    - 1. 事前定義されたスキーマを持つ、構造化されたデータストレージ。
    - 2. データの整合性を保証するACIDトランザクション。
    - 3. BIのための大量データに対する高性能なSQLクエリ。
    - 4. スキーマ検証を通じたデータ品質の向上。
  - しかしデータウェアハウスの問題点!
    - 1. スケールアップが高コスト。
    - 2. 非構造化データ(画像, 動画, ログファイルなど)の保存が困難。
    - 3. データをロードするために高額なETLプロセスが必要。
- 2010年代に入ると、多様なタイプの膨大な量ののデータを低コストで保存する需要が高まった...**データレイク(Data Lake)**が登場!
  - データレイクが提供したこと:
    - 1. コスト効率の良いストレージ
    - 2. 任意のデータ形式(parquetとか)を許容できるschema-on-readの柔軟性 (読み取り時にスキーマを適用)
    - 3. 画像、動画、ログファイルなど、多様なデータタイプの保存
    - 4. 特定のクエリエンジンに依存せず、生データに直接アクセスすることもできるので、機械学習システムにも適してる
  - しかしデータレイクの問題点!
    - 1. **適切なガバナンスがないと、「data swamp (データの沼)」になり、時間の経過とともにデータ品質が低下する無秩序なリポジトリ**になってしまう...!!
    - 2. ACIDトランザクションのサポートが欠如しており、データの整合性を確保するのが難しい
    - 3. **SQLクエリのパフォーマンスが、DWHと比べてしばしば劣る...!**
- そこで2020年台に登場したのが、テーブルフォーマット! (を用いたレイクハウスアーキテクチャ!)
  - データレイクストレージの上に、トランザクションとメタデータを管理する中間レイヤー (Metadata & Transaction Layer)としてテーブルフォーマットを配置して、クエリエンジンを分離した構造。
  - この中間レイヤーを追加することで、データレイクの利点を活かしつつ、DWHのようなガバナンスとパフォーマンスを得る事を目指す!

### テーブルフォーマット達

- 最初に登場した元祖っぽいテーブルフォーマット
  - Apache Hive
- 以下3つは、Apache Hiveの限界を克服するために登場したモダンなテーブルフォーマットたち:
  - Apache Iceberg (界隈では一番人気ありそう 今回のテーマ!)
  - Delta Lake
  - Apache Hudi

その中で今回は、モダンなテーブルフォーマットの中で一番人気があるっぽいApache Icebergについて、スキーマ進化(Schema Evolution)について調査・試行してみました!

## 背景: スキーマ進化のしやすさって重要だよね!!

- データレイクの運用において、**ビジネス要件の変化に応じてスキーマを進化させる必要性は避けられない**。
  - (実際にMLOps文脈でFeature Storeストアとして運用する上でも、**少なくともMLモデル改善の試行錯誤の中で新しい特徴量の追加はガンガン発生**するよね...!!:thinking:)
- 従来のHiveテーブルフォーマットなどでは、スキーマ変更時にテーブル全体の書き換えが必要となり、数時間から数日のダウンタイムと高額なコストが発生するらしい。
- IDCの予測によれば、2025年までに世界のデータ空間は175ゼタバイトに達すると見られており、こうした指数関数的なデータ成長に対応できる柔軟なデータモデリング手法が求められている。

## 本論: Icebergのスキーマ進化 (Schema Evolution) どんな感じ?

公式ドキュメントによると、Icebergのスキーマ進化は以下の変更をサポートしてる:

- **カラムの追加(Add)**:
  - カラム or struct型の中のfieldを追加可能
  - mapのkeyは追加不可
- **カラムの削除(Drop)**
  - カラム or struct型の中のfieldを削除可能
  - mapのkeyは削除不可
- **カラムの名前変更(Rename)**
  - カラム or struct型の中のfieldの名前を変更可能
- **カラムの更新(Update)**
  - カラムのデータ型のwidening(intをlongに変更するなど)は可能
  - ↑のwideningは、カラムだけじゃなくてstruct型のfieldや、mapのkey/value、listのelementにも適用可能
- **カラムの順序変更(Reorder)**
  - テーブルにおけるカラム達 or sturct型のfield達の順序を変更可能

**上記の変更は全部、メタデータだけ変える、データファイルは書き直さない**という仕組み。だからパフォーマンス的にも優しい。

またスキーマ進化による変更がお互いに独立してて、副作用はないことを保証してる。

具体的には...

- その1: カラム追加しても、既存の別カラムには影響しない
- その2: カラム削除しても、既存の別カラムには影響しない
- その3: カラム更新しても、既存の別カラムには影響しない
- その4: カラム順序を変更しても、対応する値は変わらない

どうやって正しさを保証してるのか??

- Icebergは、**テーブル内の各カラムを一意なID(field ID)で管理**してる
  - よって、**新しいカラムを追加した時は必ず新しいIDが割り当てられる**。既存データが間違って使われることはない
- もしもID管理ではなかったら...
  - 名前で追跡する形式だと...削除時や名前変更時に問題が起きやすい
  - 位置で追跡する形式だと...削除時に既存の他カラムに影響を与えてしまう

現代風の他のテーブルフォーマットと比べても、もっとも柔軟で包括的なスキーマ進化機能を持つらしい。([How to Achieve Seamless Schema Evolution with Apache Iceberg](https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg) より)

## 実際にS3TablesとPyIcebergで試してみた!

Pyicebergのドキュメントを参考にしつつ、Icebergテーブルを作成し、スキーマ進化を試してみた。

### 初期スキーマでIcebergテーブルを作成

まず動作確認用のIcebergテーブルを新規作成する。
なおFeature Storeを意識して、テーブルスキーマは、エンティティ識別子として`user_id`カラム、ダミーの特徴量として`feature_1`カラムを持つようにした。

```python
from pyiceberg.schema import Schema
from pyiceberg.types import LongType, NestedField, StringType, TimestamptzType
from pyiceberg.catalog import load_catalog
import polars as pl

# 1. カタログに接続(S3Tablesとか)
catalog = load_catalog(...)

# 2. Icebergテーブルのスキーマを定義
initial_schema = Schema(
    NestedField(
        field_id=1,
        name="user_id",
        field_type=LongType(),
        required=False,
        doc="ユーザーID",
    ),
    NestedField(
        field_id=2,
        name="feature_1",
        field_type=LongType(),
        required=False,
        doc="テスト用特徴量1",
    ),
)

# 3. テーブルを作成
table = catalog.create_table(
    identifier="public.test_schema_evolution",
    schema=initial_schema,
)

# 4. 初期データを書き込み
initial_data = pl.DataFrame({
    "user_id": [1, 2, 3],
    "feature_1": [100, 200, 300],
})
table.append(initial_data)

# 5. データを読み込んで確認
df = table.scan().to_polars()
print(df)
# 出力:
# shape: (3, 2)
# ┌─────────┬───────────┐
# │ user_id ┆ feature_1 │
# │ ---     ┆ ---       │
# │ i64     ┆ i64       │
# ╞═════════╪═══════════╡
# │ 1       ┆ 100       │
# │ 2       ┆ 200       │
# │ 3       ┆ 300       │
# └─────────┴───────────┘
```

OK! 無事にIcebergテーブルが作成され、初期データも書き込めた!

### スキーマ進化のパターン1つ目: カラム追加

次に、このテーブルに対してスキーマ進化1種類目としてカラム追加を試す。
具体的には、`feature_2`という新しいカラムを追加する。
Pyicebergでは以下のように `update_schema` コンテキストマネージャを使ってスキーマ変更を行えるみたい。
カラム追加の場合は `update.add_column` メソッドを使う。

```python
# カラムを追加
with table.update_schema() as update:
    update.add_column(
        path="feature_2",
        field_type=StringType(),
        required=False,
        doc="テスト用特徴量2",
    )

# スキーマ更新の反映を確認
table = table.refresh()
print(f"更新後のスキーマ:\n{table.schema()}")
# 出力:
# 更新後のスキーマ:
# table {
#   1: user_id: optional long (ユーザーID)
#   2: feature_1: optional long (テスト用特徴量1)
#   3: feature_2: optional string (テスト用特徴量2)
# }

# 既存レコードがどうなってるか確認
df_after_add = table.scan().to_polars()
print(f"カラム追加後の既存データ:\n{df_after_add}")
# 出力:
# shape: (3, 3)
# ┌─────────┬───────────┬───────────┐
# │ user_id ┆ feature_1 ┆ feature_2 │
# │ ---     ┆ ---       ┆ ---       │
# │ i64     ┆ i64       ┆ str       │
# ╞═════════╪═══════════╪═══════════╡
# │ 1       ┆ 100       ┆ null      │
# │ 2       ┆ 200       ┆ null      │
# │ 3       ┆ 300       ┆ null      │
# └─────────┴───────────┴───────────┘


```

既存レコードは保持され、新しいカラムはnullで初期化されていることが確認できた!

### スキーマ進化のパターン2: カラムの名前変更

PyIcebergでは、`update.rename_column` メソッドを使えばいいっぽい。

```python
# 1. スキーマ進化操作 (カラム名変更) を実行
with table.update_schema() as update:
    update.rename_column("feature_1", "feature_1_renamed")

# 2. スキーマを確認
table = table.refresh()
print(table.schema())
# 出力:
# table {
#   1: user_id: optional long (ユーザーID)
#   2: feature_1_renamed: optional long (テスト用特徴量1)
#   3: feature_2: optional string (テスト用特徴量2)
# }

# 3. スキーマ進化後のデータを確認
df_after_rename = table.scan().to_polars()
print(df_after_rename)

# 出力例:
# ┌─────────┬──────────────────┬───────────┐
# │ user_id │ feature_1_renamed│ feature_2 │
# │ ---     │ ---              │ ---       │
# │ i64     │ i64              │ str       │
# ╞═════════╪══════════════════╪═══════════╡
# │ 1       │ 100              │ null      │
# │ 2       │ 200              │ null      │
# │ 3       │ 300              │ null      │
# └─────────┴──────────────────┴───────────┘
```

スキーマ進化の操作が成功し、データはそのまま保持されていることが確認できた!

### スキーマ進化のパターン3: カラム削除

PyIcebergでは、`update.delete_column` メソッドを使う。
また、Pyicebergではデフォルトでは破壊的なスキーマ変更 (カラム削除など) をブロックするようになっているので、`update_schema` コンテキストマネージャの引数に `allow_incompatible_changes=True` を指定する必要がある。

```python
# 1. スキーマ進化操作 (カラム削除) を実行
with table.update_schema(allow_incompatible_changes=True) as update:
    
    update.delete_column("feature_2")

# 2. スキーマを確認
table = table.refresh()
print(table.schema())
# 出力:
# table {
#   1: user_id: optional long (ユーザーID)
#   2: feature_1_renamed: optional long (テスト用特徴量1)
# }

# 3. スキーマ進化後のデータを確認
df_after_delete = table.scan().to_polars()
print(df_after_delete)
# 出力例:
# ┌─────────┬──────────────────┐
# │ user_id │ feature_1_renamed│
# │ ---     │ ---              │
# │ i64     │ i64              │
# ╞═════════╪══════════════════╡
# │ 1       │ 100              │
# │ 2       │ 200              │
# │ 3       │ 300              │
# └─────────┴──────────────────┘
```

スキーマ進化の操作が成功し、データはそのまま保持されていることが確認できた!

## 終わりに

本記事ではざっくり以下の内容についてまとめた!

- テーブルフォーマットってなんだっけ??
- Apach Icebergってなんだっけ??
- Icebergのスキーマ進化ってどんな感じ??
- PyIcebergで実際にスキーマ進化を試してみた!

Icebergテーブルフォーマットのスキーマ進化に関するポイントは以下の通り:

- **メタデータのみの変更**: スキーマ進化はメタデータの更新のみで完結し、既存のデータファイルを書き換えない
- **Field IDベースの管理**: カラムを一意なIDで追跡することで、名前変更や順序変更の際も既存データとの対応関係を正しく保てる
- **既存データの保護**: 新規カラム追加時は既存レコードでnullが入り、削除したカラムのデータは保持される(メタデータ上で非表示になるだけ)

最後に実運用の観点では以下の点を意識したいなと思った。

- **宣言的なスキーマ管理**できるようにしたい! :thinking:
  - 例えばAWS CDKの`cdk diff`/`cdk deploy`のように、期待するテーブルスキーマをgithub上でコードとして管理し、差分検出→適用という流れを自動化しておきたい。
  - ↑ができれば、テーブルが今どんな状態かが分かりやすいし、スキーマ進化の承認フローも簡単だし、変更履歴を追跡しやすいし...!
- またスキーマ進化をデプロイする際には、**先にテスト環境で事前に試せるように**したい。
  - 既存のクエリや読み書きするデータパイプライン達への影響を確認したいので。
  - まあFeature Storeとして運用するなら、特にカラム追加 (i.e. 新しい特徴量の追加)は気軽にできるような気がする。特徴量パイプラインさえ更新すればいいので...!!


また、本記事ではスキーマ進化のみを扱ったが、Icebergにはパーティション進化やソート順進化といった機能もある。これらについては別途調査・検証していきたい。

## 参考資料

- [Apache Iceberg公式ドキュメント - Evolution](https://iceberg.apache.org/docs/1.7.1/evolution/)
- [How to Achieve Seamless Schema Evolution with Apache Iceberg](https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg)
- [Apache Iceberg vs Delta Lake (II): Schema and Partition Evolution](https://www.chaosgenius.io/blog/iceberg-vs-delta-lake-schema-partition/)
- [What's a table format and why do we need one?](https://medium.com/@shreekumar-saparia/whats-a-table-format-and-why-do-we-need-one-51373b94e1c5)
