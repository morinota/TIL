# Feature Store調べてたらレイクハウスアーキテクチャに行き着いてIceberg Table formatについて調べた! スキーマ進化編!

## はじめに: Apache Iceberg Table formatとは何かをざっくりまとめる

### ざっくりApache Icebergとは??

- オープンソースのテーブルフォーマット (Table format)
- Netflixが開発し、Apache Software Foundationに寄贈された
- モダンなテーブルフォーマットの中で、一番人気があるっぽい

### そもそも「テーブルフォーマット (Table format)」とは??

> "A table format in the simplest term is a way to organize dataset files to represent them as a single 'table'." (テーブルフォーマットとは、簡単に言うと、データセットファイルを1つの「テーブル」として表現する方法のこと。)
> ([What's a table format and why do we need one?](https://medium.com/@shreekumar-saparia/whats-a-table-format-and-why-do-we-need-one-51373b94e1c5) より引用)

- レイクハウスアーキテクチャにおいて、テーブルフォーマットは**データレイク上のデータを管理・操作するための中間レイヤー**として機能する
  - Transaction & Metadata Layer (トランザクションとメタデータのレイヤー)!
  - **データレイクを「ちゃんとしたテーブル」として扱えるようにするための中間レイヤー!**

### テーブルフォーマットがなぜ必要になったんだっけ??

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
  - この中間レイヤーを追加することで、データレイクの利点を活かしつつ、DWHのようなガバナンスとパフォーマンスを得る事を目指す。

### テーブルフォーマットの例

- 最初に登場した元祖っぽいテーブルフォーマット
  - Apache Hive
- 以下3つは、Hiveの限界を克服するために登場したモダンなテーブルフォーマットたち:
  - Apache Iceberg (界隈では一番人気ありそう! 今回のテーマ!)
  - Delta Lake
  - Apache Hudi

その中で今回は、Apache Icebergのスキーマ進化(Schema Evolution)について調査・試行したメモです。

## 背景・課題: なぜスキーマ進化が重要なのか?

データレイクの運用において、ビジネス要件の変化に応じてスキーマを進化させる必要性は避けられない。

従来のHiveテーブルなどでは、スキーマ変更時にテーブル全体の書き換えが必要となり、数時間から数日のダウンタイムと高額なコストが発生する。また、柔軟性のないスキーマ管理は、ソーシャルメディアハンドルの追加やマルチ通貨対応といった新機能追加を困難にし、データチームの生産性を低下させてきた。

IDCの予測によれば、2025年までに世界のデータ空間は175ゼタバイトに達すると見られており、こうした指数関数的なデータ成長に対応できる柔軟なデータモデリング手法が求められている。

## 本論: Icebergのスキーマ進化 (Schema Evolution) どんな感じ?

### 公式ドキュメントを読んだメモ!

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

#### 正しさの保証 (Correctness)

スキーマ進化による変更がお互いに独立してて、副作用はないことを保証してる。

具体的には...

- その1: カラム追加しても、既存の別カラムには影響しない
- その2: カラム削除しても、既存の別カラムには影響しない
- その3: カラム更新しても、既存の別カラムには影響しない
- その4: カラム順序を変更しても、対応する値は変わらない

**どうやって正しさを保証してるのか??**

- Icebergは、**テーブル内の各カラムを一意なID(field ID)で管理**してる
  - よって、**新しいカラムを追加した時は必ず新しいIDが割り当てられる**。既存データが間違って使われることはない
  - もしカラムを名前で追跡する形式だと、削除時や名前変更時に問題が起きやすい
  - もしカラムを位置で追跡する形式だと、削除時に既存の他カラムに影響を与えてしまう

### 他のテーブルフォーマットとの比較

主要なテーブルフォーマット間のスキーマ進化機能比較:

| 機能 | Apache Iceberg | Delta Lake | Apache Hudi |
|------|----------------|------------|-------------|
| カラム追加 | ○ | ○ | ○ |
| カラム削除 | ○ | ○ | ○ |
| カラム名変更 | ○ | ○ | × |
| カラム型変更 | ○(限定的) | ○ | × |
| カラム順序変更 | ○ | × | × |
| 書き込み時のスキーマ進化 | ○ | ○ | ○ |

Icebergは**スキーマ進化のための主要なプラットフォーム**として、市場で最も包括的で柔軟な機能を提供している。

### スキーマ進化のパフォーマンス比較

1TBの大規模なテーブルにカラム追加した場合のパフォーマンス比較 (Apache Iceberg vs Apache Hive):

| テーブルフォーマット | カラム追加時間 | 読み取りパフォーマンスへの影響 |
|---------------------|---------------|------------------------------|
| Apache Iceberg | 0秒 | 影響なし |
| Apache Hive | 4.5時間 | 15%低下 |

Icebergは、Hiveが苦しむ長時間のテーブル書き換えや読み取りパフォーマンス低下を回避し、操作をほぼ瞬時に実行する。

### 実際の例: 大規模なEコマースプラットフォームで

最初: 製品カタログのスキーマは以下のような構造だったとする。

```python
# 初期スキーマ
CREATE TABLE products (
    id BIGINT,
    name STRING,
    price DECIMAL(10, 2),
    category STRING
)
```

ビジネスの成長に伴い、以下のようなスキーマ変更が必要になりうる:

```python
# 1. 製品の説明(description)カラムを追加
ALTER TABLE products ADD COLUMN description STRING

# 2. マルチ通貨サポートのためのネスト構造を追加
ALTER TABLE products ADD COLUMN prices STRUCT<
    usd:DECIMAL(10,2),
    eur:DECIMAL(10,2),
    gbp:DECIMAL(10,2)
>

# 3. デフォルト値付きカラムの追加
ALTER TABLE products ADD COLUMN avg_rating FLOAT DEFAULT 0.0

# 4. カラムの名前変更
ALTER TABLE products RENAME COLUMN category TO product_category
```

上記の変更を、テーブル全体を書き直すことなく即座にスキーマ更新できる。**既存のETLプロセスやクエリは影響を受けず、過去のデータには古いスキーマを、新しい情報には新しいスキーマをシームレスにアクセス**できる。

## 実際にS3TablesとPyIcebergで試してみた!

Pyicebergのドキュメントを参考にしつつ、Icebergテーブルを作成し、スキーマ進化を試してみた。

### 初期スキーマでIcebergテーブルを作成

```python
from pyiceberg.schema import Schema
from pyiceberg.types import LongType, NestedField, StringType, TimestamptzType
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.transforms import DayTransform, BucketTransform
from pyiceberg.catalog import load_catalog

# カタログに接続
catalog = load_catalog(...)

# Icebergテーブルのスキーマを定義
initial_schema = Schema(
    NestedField(
        field_id=1,
        name="user_id",
        field_type=LongType(),
        required=False,
        doc="ユーザーID(エンティティの識別子)",
    ),
    NestedField(
        field_id=2,
        name="event_time",
        field_type=TimestamptzType(),
        required=False,
        doc="履歴特徴量のバージョン管理用のカラム",
    ),
    NestedField(
        field_id=4,
        name="feature_1",
        field_type=LongType(),
        required=False,
        doc="テスト用特徴量1",
    ),
)

# パーティション仕様を定義
partition_spec = PartitionSpec(
    PartitionField(source_id=2, field_id=1000, transform=DayTransform(), name="event_time_day"),
)

# テーブルを作成
table = catalog.create_table(
    identifier="public.test_schema_evolution",
    schema=initial_schema,
    partition_spec=partition_spec,
)
```

### スキーマ進化1としてカラム追加を試す

次に、このテーブルに対してスキーマ進化を試す。以下の変更を行う:

- カラム追加: `user_feature_3`という新しいカラムを追加

```python
# 変更後のスキーマを定義
evolved_schema = Schema(
    NestedField(field_id=1, name="user_id", field_type=LongType(), required=False),
    NestedField(field_id=2, name="event_time", field_type=TimestamptzType(), required=False),
    NestedField(field_id=3, name="created", field_type=TimestamptzType(), required=False),
    NestedField(field_id=4, name="feature_1", field_type=LongType(), required=False),
    # 新しいカラムを追加
    NestedField(field_id=6, name="user_feature_3", field_type=StringType(), required=False),
)
```

### スキーマ差分を検出する

スキーマの差分を検出するロジック:

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class SchemaChange:
    """スキーマ変更の種類"""
    change_type: Literal["add_column", "rename_column", "delete_column"]
    field_name: str
    new_field_name: str | None = None
    field: NestedField | None = None
    is_destructive: bool = False

def detect_schema_changes(current_schema: Schema, desired_schema: Schema) -> list[SchemaChange]:
    """現在のスキーマと期待するスキーマの差分を検出"""
    changes: list[SchemaChange] = []

    current_fields_by_id = {f.field_id: f for f in current_schema.fields}
    desired_fields_by_id = {f.field_id: f for f in desired_schema.fields}

    # 追加・リネームを検出
    for field_id, desired_field in desired_fields_by_id.items():
        if field_id not in current_fields_by_id:
            changes.append(
                SchemaChange(
                    change_type="add_column",
                    field_name=desired_field.name,
                    field=desired_field,
                    is_destructive=False,
                )
            )
        else:
            current_field = current_fields_by_id[field_id]
            if current_field.name != desired_field.name:
                changes.append(
                    SchemaChange(
                        change_type="rename_column",
                        field_name=current_field.name,
                        new_field_name=desired_field.name,
                        is_destructive=False,
                    )
                )

    # 削除を検出
    for field_id, current_field in current_fields_by_id.items():
        if field_id not in desired_fields_by_id:
            changes.append(
                SchemaChange(
                    change_type="delete_column",
                    field_name=current_field.name,
                    is_destructive=True,
                )
            )

    return changes

# 実際に差分を検出
table = catalog.load_table("public.test_schema_evolution")
schema_changes = detect_schema_changes(table.schema(), evolved_schema)

print("Schema changes:", schema_changes)
```

### スキーマ変更を適用する

検出した差分を実際にテーブルに適用する:

```python
from pyiceberg.table import Table

def apply_schema_changes(table: Table, changes: list[SchemaChange], allow_destructive_changes: bool = False) -> None:
    """検出されたスキーマ変更をテーブルに適用"""
    if not changes:
        return

    destructive_changes = [c for c in changes if c.is_destructive]
    if destructive_changes and not allow_destructive_changes:
        print(f"破壊的な変更が検出されました: {destructive_changes}")
        print("破壊的変更を適用するには allow_destructive_changes=True を指定してください")
        return

    with table.update_schema(allow_incompatible_changes=allow_destructive_changes) as update:
        for change in changes:
            if change.change_type == "add_column":
                if change.field:
                    update.add_column(
                        path=change.field.name,
                        field_type=change.field.field_type,
                        required=change.field.required,
                        doc=change.field.doc,
                    )
                    print(f"✅ カラム追加: {change.field.name}")

            elif change.change_type == "rename_column":
                if change.new_field_name:
                    update.rename_column(change.field_name, change.new_field_name)
                    print(f"✅ カラムリネーム: {change.field_name} → {change.new_field_name}")

            elif change.change_type == "delete_column":
                update.delete_column(path=change.field_name)
                print(f"✅ カラム削除: {change.field_name}")

# 変更を適用
apply_schema_changes(table, schema_changes)
```

### 宣言的スキーマ管理の実装

すべてのテーブルスキーマを一元管理し、宣言的に管理する実装例:

```python
# schema_definitions.py
"""Feature Store用のIcebergテーブルスキーマ定義"""

# テーブル名とスキーマのマッピング
TABLES = {
    "test_schema_evolution": Schema(
        NestedField(field_id=1, name="user_id", field_type=LongType(), required=False),
        NestedField(field_id=2, name="event_time", field_type=TimestamptzType(), required=False),
        NestedField(field_id=3, name="created", field_type=TimestamptzType(), required=False),
        NestedField(field_id=4, name="feature_1", field_type=LongType(), required=False),
        NestedField(field_id=6, name="user_feature_3", field_type=StringType(), required=False),
    ),
}
```

```python
# create_iceberg_tables.py
"""Feature Store用のIcebergテーブルを初期化するCLIツール"""

import typer
from schema_definitions import TABLES
from schema_evolution import detect_schema_changes, apply_schema_changes

def main(mode: str, namespace: str = "public"):
    """Feature Store用のIcebergテーブルを初期化・管理

    mode: "diff"=差分表示のみ, "deploy"=テーブル作成+スキーマ進化
    """
    catalog = load_catalog(...)

    # 全テーブルの差分を検出
    for table_name, desired_schema in TABLES.items():
        table_identifier = f"{namespace}.{table_name}"

        try:
            table = catalog.load_table(table_identifier)

            # 既存テーブルのスキーマ変更をチェック
            schema_changes = detect_schema_changes(table.schema(), desired_schema)

            if schema_changes:
                print(f"[~] {table_identifier}")
                print("  Schema:", schema_changes)

                if mode == "deploy":
                    apply_schema_changes(table, schema_changes)

        except Exception:
            # テーブルが存在しない場合は新規作成
            print(f"[+] {table_identifier}")
            if mode == "deploy":
                catalog.create_table(
                    identifier=table_identifier,
                    schema=desired_schema,
                )

if __name__ == "__main__":
    typer.run(main)
```

## 学びと考察

### 学んだこと

- Icebergのスキーマ進化は、メタデータのみの変更により高速かつ安全に実行される
- 一意なカラムID管理により、スキーマ変更時の正しさが保証され、副作用がない
- Delta LakeやHudiと比較して、カラムの順序変更や名前変更などの柔軟性が高い
- 柔軟なデータモデリングにより、新データ製品の市場投入時間を最大35%短縮し、データチームの生産性を40%向上できる(2023 Databricks調査)
- スキーマ進化だけでなく、ソート順進化やパーティション進化などもサポートし、データレイク全体の進化を支援

### 自分の考察

#### Feature Storeへの応用可能性

Icebergのスキーマ進化機能は、機械学習のFeature Storeにおいて特に価値が高い:

1. **特徴量の追加・削除の容易性**: 新しい特徴量を追加する際にテーブル全体の書き換えが不要なため、実験サイクルが高速化される
2. **増分処理との相性**: 変更されたデータのみを処理する増分処理により、新しく更新された特徴量レコードだけを効率的に抽出できる
3. **スキーマバージョン管理**: バージョン管理システムでスキーマ変更を追跡することで、特徴量の履歴管理と監査が容易になる

#### 宣言的スキーマ管理のメリット

- **Infrastructure as Code**: スキーマ定義をコードで管理することで、変更履歴の追跡とレビューが容易
- **差分検出の自動化**: 現在のスキーマと期待するスキーマの差分を自動検出し、適用前に確認できる
- **破壊的変更の保護**: `allow_destructive_changes`フラグにより、意図しないカラム削除を防止

#### ガバナンスの重要性

大きな柔軟性には強力なガバナンスが必要:

- スキーマ変更を管理・追跡する堅牢なプロセスの実装
- 意味のあるデフォルト値の使用(列追加時)
- ステージング環境での徹底的なテスト
- すべての利害関係者への変更通知

#### IcebergとDelta Lakeの使い分け

- **Iceberg**: 急速に進化するスキーマ、ベンダーニュートラル、複数処理エンジンの統合が必要な場合
- **Delta Lake**: Databricksエコシステムとの深い統合、厳密なACID準拠が必要な場合

ただし、スキーマ進化の柔軟性の観点では、Icebergが明確な優位性を持つ。

## 参考リンク

- [Apache Iceberg公式ドキュメント - Evolution](https://iceberg.apache.org/docs/1.7.1/evolution/)
- [How to Achieve Seamless Schema Evolution with Apache Iceberg](https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg)
- [Apache Iceberg vs Delta Lake (II): Schema and Partition Evolution](https://www.chaosgenius.io/blog/iceberg-vs-delta-lake-schema-partition/)
- [What's a table format and why do we need one?](https://medium.com/@shreekumar-saparia/whats-a-table-format-and-why-do-we-need-one-51373b94e1c5)
