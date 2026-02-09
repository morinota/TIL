## refs:

- [公式docs](https://iceberg.apache.org/docs/nightly/evolution/#sort-order-evolution)


## Sort Order機能って ??

### Sort Order Evolution(ソート順進化)

スキーマ進化と同様に、Icebergは**ソート順(sort order)**の進化もサポートする:

- テーブルはpartition内のデータをカラムでソートすることでクエリ性能を向上できる
- ソート順は、ソート順IDとソートフィールドのリストによって定義される
- 各ソートフィールドは以下で定義:
  - ソースカラムのfield ID
  - 変換関数(transform function)
  - ソート方向(ascending/descending)
  - null order(nulls first/nulls last)
- **ソート順を変更しても、以前のソート順で書き込まれた古いデータはそのまま保持される**
  - -> 古いデータファイルに適用するには、optimizeなどのメンテナンスコマンドを実行する。
