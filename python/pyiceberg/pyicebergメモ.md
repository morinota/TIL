## これは何?


## ざっくりメモ

- まずApache Icebergテーブル形式について。
  - ビッグデータ向けに設計されたオープンテーブルフォーマット。
  - ACID トランザクション、スキーマ進化、隠蔽されたパーティションなどの機能を備えており、大量データを扱う分析ワークロードに適している。
- そしてPyIcebergについて。
  - Pythonから軽くIcebergテーブルを操作できるライブラリ。
    - **Apach Icebergの公式Pythonクライアント**。
  - **従来Icebergを操作するには、Apache SparkやTrino、Flinkなどの分散処理エンジンが必要だった。**
    - しかしPyIcebergを使うことで、Pythonから直接Icebergテーブルを操作できるようになる。
  - 具体的には、以下の操作がPythonだけで可能になる。
    - Icebergテーブルの作成・削除
    - スキーマやパーティションの管理
    - データの追加・読み取り
    - SparkやTrinoを使わずにIcebergを操作
  - PyIcebergはIcebergのメタデータを直接扱うので、軽量で、Pythonネイティブなワークフローに統合しやすいのが特徴!

- PyIcebergの利点(Advantages of PyIceberg)
  - その1: 軽量であること
    - Apache SparkやApache Flinkなどの重い分散処理エンジンを必要とせず、Python環境で直接Icebergテーブルを操作できる。
  - その2: PythonネイティブなAPIを提供してること
    - この特徴により、既存のPythonワークフローやETLパイプラインに簡単にくみ込める
  - その3: Icebergのメタデータを直接操作できること
    - この特徴により、テーブル作成、スキーマ進化、スナップショット管理といったIcebergのコア機能をフルに活用できる。
  - その4: PyArrowやDuckDBなどのPythonデータツールと相性が良いこと。
    - IcebergテーブルをArrow形式で読み込み、そのままpolarsやPandasで分析したり、DuckDBでクエリを実行したりできる。
  - その5: クラウドやローカル環境のどちらでも利用可能であること
    - S3やGCSなどのオブジェクトストレージと組み合わせることで、本番環境でもスケーラブルに利用できる!

### PyIcebergでIcebergテーブルをクエリする (Querying Iceberg Tables with PyIceberg)

基本的なテーブル全体のスキャンは以下のように行う。

```python
# 1. まずscan()メソッドを使ってテーブルスキャンを作成
scan = table.scan()
# このスキャンは、Icebergテーブルの最新スナップショットを対象とする

# 2. データをArrowテーブルとして読み込む
arrow_table = scan.to_arrow()
# Arrowテーブルは、Pythonのデータ処理エコシステムと高い互換性を持つので、効率的にデータを扱える

# この後pandasなりpolarsなりのDataFrameに変換しても良い!
pl_df = pl.from_arrow(arrow_table)
```

PyIcebergはIcebergテーブルの強力なクエリ機能を提供してる。
具体的には、**predicate filtering (述語フィルタリング) 機能**や、**column selectio (カラム選択)機能**によって、柔軟なデータ抽出が可能になる。

その1: Query By Name (String Matching)

```python
from pyiceberg.expressions import StartsWith

# nameカラムの値が"metric"で始まるすべての行を検索
result = iceberg_table \
    .scan(row_filter=StartsWith("name", "metric")) \
    .to_arrow()
print(result.to_string(preview_cols=10))

# Output:
# pyarrow.Table
# id: int32 not null
# name: large_string not null
# value: int32 not null
# ----
# id: [[1, 2, 3]]
# name: [["metric_1", "metric_2", "metric_3"]]
# value: [[5, 12, 18]]
```

その2: Query Latest Entries (Filtering by Timestamp)

```python
from pyiceberg.expressions import GreaterThan
import datetime

# 直近7日以内に作成されたすべての行を検索
seven_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()

# created_atカラムがあるテーブルを想定
result = iceberg_table \
    .scan(row_filter=GreaterThan("created_at", seven_days_ago)) \
    .to_arrow()
print(result.to_string(preview_cols=10))
```

その3: Query with Multiple Conditions (Category & Value Filtering)

```python
from pyiceberg.expressions import And, EqualTo, GreaterThan

# categoryカラムが"A"で、valueカラムが10より大きいすべての行を検索
result = iceberg_table \
    .scan(
        row_filter=And(
            EqualTo("category", "A"),
            GreaterThan("value", 10)
        )
    ) \
    .to_arrow()
print(result.to_string(preview_cols=10))
```

その4: Retrieving Specific Columns for Performance Optimization

```python
from pyiceberg.expressions import EqualTo

# 全カラムをスキャンする代わりに、パフォーマンス向上のために必要なカラムのみをselectすることもできる!
result = iceberg_table \
    .scan(
        row_filter=EqualTo("id", 3),
        selected_fields=["id", "value"]
    ) \
    .to_arrow()
print(result.to_string(preview_cols=10))
```

その5: Find Null or Missing Values (欠損値の検索)

```python
from pyiceberg.expressions import IsNull

# もしデータセットが欠損値やNULL値を含んでいる場合、それらを簡単に見つけることができる
result = iceberg_table \
    .scan(row_filter=IsNull("value")) \
    .to_arrow()
print(result.to_string(preview_cols=10))
```

その6: Query Using a List of IDs (IDリストを使ったクエリ) IN Clause Alternative

```python
from pyiceberg.expressions import In

# 複数IDのリストにマッチする行を一括でクエリしたい場合、Inが使える。
result = iceberg_table \
    .scan(row_filter=In("id", [1, 3, 5, 7, 9])) \
    .to_arrow()
print(result.to_string(preview_cols=10))
```

### PyIcebergでデータを更新または削除する (Updating and Deleteing Data with PyIceberg)

Icebergテーブルのデータを更新するには、以下のように行う。

```python
import pyarrow as pa
from pyiceberg.expressions import EqualTo
import datetime

# 'updated_at'カラムの

# 1. まず更新したい行を検索
filtered_table = iceberg_table \
  .scan(row_filter=EqualTo('id', 4)) \
  .to_arrow()

# 2. 'updated_at'カラムのindexとフィールドを取得
updated_at_col_index = filtered_table.column_names.index('updated_at')
updated_at_col_field = filtered_table.field(updated_at_col_index)

# 3. 現在のUTCタイムスタンプをISOフォーマットで取得
current_utc_timestamp = datetime.datetime.utcnow().isoformat()

# 4. 'updated_at'カラムを現在のタイムスタンプでreplace
updated_table = filtered_table.set_column(
  updated_at_col_index, 
  updated_at_col_field, 
  # もしupdated_atカラムがstring型ならこうする。
  pa.array([current_utc_timestamp], type=pa.string())
  # もしupdated_atカラムがtimestamp型なら例えばこうなる
  # pa.array([datetime.datetime.utcnow()], type=pa.timestamp('us')
)

# 5. Icebergテーブルの既存の行を上書き
iceberg_table.overwrite(
  df=updated_table,
  overwrite_filter=EqualTo('id', 4)
)
```

同様に、Icebergテーブルのデータを削除するには以下のように行う。

```python
from pyiceberg.expressions import EqualTo

# idカラムが1の行をすべて削除
iceberg_table.delete(
 delete_filter=EqualTo('id', 1)
)
```

### PyIcebergでIcebergテーブルのスキーマ進化を管理する (Schema Evolution with PyIceberg)

参考: [Schema evolution](https://py.iceberg.apache.org/api/#schema-evolution)

- スキーマ変更は共通の必須要件であり、Icebergテーブル形式は安全なスキーマ進化をサポートしている。
- **PyIceberg は Python API を通じて完全なスキーマ進化をサポート。**
  - これにより、Iceberg テーブルのスキーマを変更する作業が簡単にできる。
- field-ID の管理は PyIceberg が自動的に行い、**破壊的でない変更のみが行われるようにする。**(必要に応じてオーバーライドも可能)

スキーマ進化の実行例:

```python
# Tableオブジェクトの`update_schema()`コンテキストマネージャを使ってスキーマ進化を制御できる
with table.update_schema() as update_schema:
    # これは新しいカラムを追加する例
    update_schema.add_column("some_field", IntegerType(), "doc")

# スキーマ進化以外の変更もまとめて行いたい場合には、トランザクションコンテキストマネージャで更にラップできる
with table.transaction() as transaction:
    with transaction.update_schema() as update _schema:
        update_schema.add_column("another_field", StringType(), "doc")
    # ... Update properties etc. (スキーマ進化以外の変更)
```

- 注意点: `table.update_schema()`コンテキストマネージャと破壊的変更について!
  - スキーマ進化の操作の種類によっては、incompatible(=破壊的)な変更となる場合がある。
    - ex. 既存カラムをoptionalから必須に変更する, 既存カラムを削除するなど。
  - **デフォルトでは、PyIcebergの本コンテキストマネージャは、破壊的な変更の実行を防止する**。
    - もし破壊的な変更を試みた場合、`IncompatibleSchemaChangeError`例外が発生する。
    - ただし`allow_incompatible_changes=True`パラメータを指定することで、破壊的な変更も明示的に許可できる。

### PyIcebergでIcebergテーブルのパーティション進化を管理する (Partition Evolution with PyIceberg)

参考: [Partition evolution](https://py.iceberg.apache.org/api/#partition-evolution)
