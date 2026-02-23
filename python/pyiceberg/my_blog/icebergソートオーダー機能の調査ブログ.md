## refs:

- [公式docs](https://iceberg.apache.org/docs/nightly/evolution/#sort-order-evolution)
- [Clustering vs Partitioning your Apache Iceberg Tables](https://amdatalakehouse.substack.com/p/clustering-vs-partitioning-your-apache)
- [Apache Iceberg Table Optimization #4: Smarter Data Layout— Sorting and Clustering Iceberg Tables](https://dev.to/alexmercedcoder/apache-iceberg-table-optimization-4-smarter-data-layout-sorting-and-clustering-iceberg-tables-2fml)

## Icebergテーブルにおけるクラスタリング(i.e. ソート)ってどういうニュアンスの話??

- clustering(sorting)とは??
  - Partitioningと同様、**データの配置を整理することでテーブルのパフォーマンスが高い状態を維持**するための技術。
  - Partitioningとの違い = 物理的なデータ分割をするのがPartitioning、データの配置を整理するのがClustering(ソート)。

- ex.) ユーザidでフィルタリングするSQLクエリを実行したい場合:
  - もし**データがランダムに分散してる**と...
    - クエリエンジンは**全てのデータファイルをスキャンする必要**がある!
  - もし**データがソートまたはクラスタリングされてる**と...
    - クエリエンジンは**ファイル全体や行グループをスキップできる**ため、I/Oを削減し、実行を高速化できる!
- クラスタリング(i.e. ソート)の利点:
  - スキャンされるファイルと行が少なくなる
  - より良い圧縮率
  - より高速な結合と集約
  - パーティションと行グループのより効率的なプルーニング


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
