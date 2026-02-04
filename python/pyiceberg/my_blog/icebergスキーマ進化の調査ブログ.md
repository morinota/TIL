# Feature Store調べてたらレイクハウスアーキテクチャに行き着いてIcebergテーブル形式について調べた! スキーマ進化編!
## これは何??

- Icebergテーブル形式のスキーマ進化(Schema Evolution)やパーティション進化(Partition Evolution)について調査し、試しに実行してみたメモです。

## はじめに: Apache Icebergテーブル形式とは何かをざっくりまとめる

ざっくりApache Icebergとは??

  - オープンソースのテーブル形式(table format)。
  - Netflixが開発し、Apache Software Foundationに寄贈された。
  - モダンなテーブル形式の中で、一番人気があるっぽい。

そもそも「テーブル形式」とは??

> “A table format in the simplest term is a way to organize dataset files to represent them as a single ‘table’.” (テーブル形式とは、簡単に言うと、データセットファイルを1つの「テーブル」として表現する方法のこと。) 
> ([What’s a table format and why do we need one?](https://medium.com/@shreekumar-saparia/whats-a-table-format-and-why-do-we-need-one-51373b94e1c5) より引用)

- lakehouseアーキテクチャにおいて、テーブル形式は**データレイク上のデータを管理・操作するための中間レイヤー**として機能する。
  - Transaction & Metadata Layer (トランザクションとメタデータのレイヤー)。

テーブル形式がなぜ必要になったんだっけ??

- 1980年代に、分析クエリに最適化された専用のDBとして**DWH(データウェアハウス)**が登場!
- 2010年代に入ると、多様なタイプの膨大な量ののデータを低コストで保存する需要が高まり、**データレイク(Data Lake)**が登場!
  - データレイクが提供したこと
    - 1. コスト効率の良いストレージ
    - 2. 任意のデータ形式(parquetとか)を許容できるschema-on-readの柔軟性 (読み取り時にスキーマを適用)
    - 3. 画像、動画、ログファイルなど、多様なデータタイプの保存
    - 4. 特定のクエリエンジンに依存せず、生データに直接アクセスすることもできるので、機械学習システムにも適してる。
- しかしデータレイクの問題点!
  - 1. **適切なガバナンスがないと、「data swamp (データの沼)」になり、時間の経過とともにデータ品質が低下する無秩序なリポジトリ**になってしまう...!!
  - 2. ACIDトランザクションのサポートが欠如しており、データの整合性を確保するのが難しい。
  - 3. SQLクエリのパフォーマンスが、DWHと比べて劣ることが多い。
- そこで登場したのが、**テーブル形式(table format)**! 
  - データレイクストレージの上に位置する、**トランザクションとメタデータを管理する中間レイヤー (Metadata & Transaction Layer)**。
  - この中間レイヤーを追加することで、データレイクの利点を活かしつつ、DWHのようなガバナンスとパフォーマンスを得る。
  - データレイクを「ちゃんとしたテーブル」として扱えるようにするための中間レイヤー。

テーブル形式の例として、以下がある:

- 最初に登場した元祖っぽいテーブル形式
  - Apache Hive 
- 以下3つは、Hiveの限界を克服するために登場したモダンなテーブル形式たち:
  - Apache Iceberg (界隈では一番人気ありそう! 今回のテーマ!)
  - Delta Lake
  - Apache Hudi

その中で今回は、Apache Icebergのスキーマ進化(Schema Evolution)について調査・試行したメモです。

## 本論: Icebergのスキーマ進化 (Schema Evolution)　どんな感じ?

### 公式ドキュメントを読んだメモ!

公式ドキュメントによると、Icebergのスキーマ進化は以下の変更をサポートしてる:

- カラムの追加(Add):
  - カラム or struct型の中のfieldを追加可能。
  - mapのkeyは追加不可。
- カラムの削除(Drop)
  - カラム or struct型の中のfieldを削除可能。
  - mapのkeyは削除不可。
- カラムの名前変更(Rename)
  - カラム or struct型の中のfieldの名前を変更可能。
- カラムの更新(Update)
  - カラムのデータ型のwidening(intをlongに変更するなど)は可能。
  - ↑のwideningは、カラムだけじゃなくてstruct型のfieldや、mapのkey/value、listのelementにも適用可能。
- カラムの順序変更(Reorder)
  - テーブルにおけるカラム達 or sturct型のfield達の順序を変更可能。

上記の変更は全部、**メタデータだけ変える、データファイルは書き直さない**という仕組み。だからパフォーマンス的にも優しい。

- 正しさの保証 (Correctness)
  - スキーマ進化による変更がお互いに独立してて、副作用はないことを保証してる。
  - 具体的には...
    - その1: カラム追加しても、既存の別カラムには影響しない。
    - その2: カラム削除しても、既存の別カラムには影響しない。
    - その3: カラム更新しても、既存の別カラムには影響しない。
    - その4: カラム順序を変更しても、対応する値は変わらない。
  - どうやって正しさを保証してるのか??
    - Icebergは、**テーブル内の各カラムを一意なID(field ID)で管理**してる。
      - よって、**新しいカラムを追加した時は必ず新しいIDが割り当てられる**。既存データが間違って使われることはない。
      - もしカラムを名前で追跡する形式だと、削除時や名前変更時に問題が起きやすい。
      - もしカラムを位置で追跡する形式だと、削除時に既存の他カラムに影響を与えてしまう。

### Icebergテーブル形式はシームレスにスキーマ進化できるからいいぜというブログを読んだメモ

- refs: 
  - [How to Achieve Seamless Schema Evolution with Apache Iceberg　Apache](https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg)

## 実際にS3TablesとPyIcebergで試してみた!

Pyicebergのドキュメントを参考にしつつ、Icebergテーブルを作成し、スキーマ進化を試してみた。

まず、初期スキーマでIcebergテーブルを作成する。

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

# パーティション仕様を定義(今回は本筋ではないので簡単に)
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

### スキーマ進化1としてカラム追加を試す。

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

# 変更後のパーティション仕様を定義
evolved_partition_spec = PartitionSpec(
    PartitionField(source_id=2, field_id=1000, transform=DayTransform(), name="event_time_day"),
    # 新しいパーティションフィールドを追加
    PartitionField(source_id=1, field_id=1001, transform=BucketTransform(16), name="user_id_bucket"),
)
```

### スキーマ差分を検出する

スキーマとパーティションの差分を検出するロジックは以下の通り:

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

@dataclass
class PartitionChange:
    """パーティション変更の種類"""
    change_type: Literal["add_field", "rename_field", "remove_field"]
    partition_name: str
    new_partition_name: str | None = None
    partition_field: PartitionField | None = None
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

def detect_partition_changes(current_spec: PartitionSpec, desired_spec: PartitionSpec) -> list[PartitionChange]:
    """現在のパーティション仕様と期待するパーティション仕様の差分を検出"""
    changes: list[PartitionChange] = []

    current_fields_by_id = {f.field_id: f for f in current_spec.fields}
    desired_fields_by_id = {f.field_id: f for f in desired_spec.fields}

    # 追加・リネームを検出
    for field_id, desired_field in desired_fields_by_id.items():
        if field_id not in current_fields_by_id:
            changes.append(
                PartitionChange(
                    change_type="add_field",
                    partition_name=desired_field.name,
                    partition_field=desired_field,
                    is_destructive=False,
                )
            )
        else:
            current_field = current_fields_by_id[field_id]
            if current_field.name != desired_field.name:
                changes.append(
                    PartitionChange(
                        change_type="rename_field",
                        partition_name=current_field.name,
                        new_partition_name=desired_field.name,
                        is_destructive=False,
                    )
                )

    # 削除を検出
    for field_id, current_field in current_fields_by_id.items():
        if field_id not in desired_fields_by_id:
            changes.append(
                PartitionChange(
                    change_type="remove_field",
                    partition_name=current_field.name,
                    is_destructive=True,
                )
            )

    return changes

# 実際に差分を検出
table = catalog.load_table("public.test_schema_evolution")
schema_changes = detect_schema_changes(table.schema(), evolved_schema)
partition_changes = detect_partition_changes(table.spec(), evolved_partition_spec)

print("Schema changes:", schema_changes)
print("Partition changes:", partition_changes)
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

def apply_partition_changes(table: Table, changes: list[PartitionChange], allow_destructive_changes: bool = False) -> None:
    """検出されたパーティション変更をテーブルに適用"""
    if not changes:
        return

    destructive_changes = [c for c in changes if c.is_destructive]
    if destructive_changes and not allow_destructive_changes:
        print(f"破壊的な変更が検出されました: {destructive_changes}")
        print("破壊的変更を適用するには allow_destructive_changes=True を指定してください")
        return

    with table.update_spec() as update:
        for change in changes:
            if change.change_type == "add_field":
                if change.partition_field:
                    update.add_field(
                        source_column_name=change.partition_field.source_id,
                        transform=change.partition_field.transform,
                        partition_field_name=change.partition_field.name,
                    )
                    print(f"✅ パーティションフィールド追加: {change.partition_field.name}")

            elif change.change_type == "rename_field":
                if change.new_partition_name:
                    update.rename_field(change.partition_name, change.new_partition_name)
                    print(f"✅ パーティションフィールドリネーム: {change.partition_name} → {change.new_partition_name}")

            elif change.change_type == "remove_field":
                update.remove_field(change.partition_name)
                print(f"✅ パーティションフィールド削除: {change.partition_name}")

# 変更を適用
apply_schema_changes(table, schema_changes)
apply_partition_changes(table, partition_changes)
```

### 宣言的スキーマ管理の実装

すべてのテーブルスキーマを一元管理し、宣言的に管理する実装例:

```python
# schema_definitions.py
"""Feature Store用のIcebergテーブルスキーマ定義"""

# テーブル名、スキーマ、パーティション仕様のマッピング
TABLES = {
    "test_schema_evolution": (
        Schema(
            NestedField(field_id=1, name="user_id", field_type=LongType(), required=False),
            NestedField(field_id=2, name="event_time", field_type=TimestamptzType(), required=False),
            NestedField(field_id=3, name="created", field_type=TimestamptzType(), required=False),
            NestedField(field_id=4, name="feature_1", field_type=LongType(), required=False),
            NestedField(field_id=6, name="user_feature_3", field_type=StringType(), required=False),
        ),
        PartitionSpec(
            PartitionField(source_id=2, field_id=1000, transform=DayTransform(), name="event_time_day"),
            PartitionField(source_id=1, field_id=1001, transform=BucketTransform(16), name="user_id_bucket"),
        ),
    ),
}
```

```python
# create_iceberg_tables.py
"""Feature Store用のIcebergテーブルを初期化するCLIツール"""

import typer
from schema_definitions import TABLES
from schema_evolution import detect_schema_changes, detect_partition_changes, apply_schema_changes, apply_partition_changes

def main(mode: str, namespace: str = "public"):
    """Feature Store用のIcebergテーブルを初期化・管理

    mode: "diff"=差分表示のみ, "deploy"=テーブル作成+スキーマ進化
    """
    catalog = load_catalog(...)

    # 全テーブルの差分を検出
    for table_name, (desired_schema, partition_spec) in TABLES.items():
        table_identifier = f"{namespace}.{table_name}"

        try:
            table = catalog.load_table(table_identifier)

            # 既存テーブルのスキーマ変更をチェック
            schema_changes = detect_schema_changes(table.schema(), desired_schema)
            partition_changes = detect_partition_changes(table.spec(), partition_spec)

            if schema_changes or partition_changes:
                print(f"[~] {table_identifier}")
                print("  Schema:", schema_changes)
                print("  Partition:", partition_changes)

                if mode == "deploy":
                    apply_schema_changes(table, schema_changes)
                    apply_partition_changes(table, partition_changes)

        except Exception:
            # テーブルが存在しない場合は新規作成
            print(f"[+] {table_identifier}")
            if mode == "deploy":
                catalog.create_table(
                    identifier=table_identifier,
                    schema=desired_schema,
                    partition_spec=partition_spec,
                )

if __name__ == "__main__":
    typer.run(main)
```

## 終わりに
