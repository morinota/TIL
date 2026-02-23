## refs:

- [公式docs](https://iceberg.apache.org/docs/nightly/evolution/#sort-order-evolution)
- [Clustering vs Partitioning your Apache Iceberg Tables](https://amdatalakehouse.substack.com/p/clustering-vs-partitioning-your-apache)
- [Apache Iceberg Table Optimization #4: Smarter Data Layout— Sorting and Clustering Iceberg Tables](https://dev.to/alexmercedcoder/apache-iceberg-table-optimization-4-smarter-data-layout-sorting-and-clustering-iceberg-tables-2fml)

## Icebergテーブルにおけるクラスタリング(i.e. ソート)ってどういうニュアンスの話??

- clustering(sorting)とは??
  - hoge
  - partitioningとの共通点:
    - **目的が共通! ともに、クエリパフォーマンスとデータ管理の効率を向上させることを目的とした技術である!**
      - データのlocalityを改善し、クエリ中にスキャンされるデータ量を最小限に抑えることで、クエリパフォーマンスを向上させることができる!
    - 設計時に意識することが共通!
      - 両方の技術ともに、効果的に機能させるためには**データとクエリパターンの理解が必要**! 不適切な設定は、逆にパフォーマンスを悪化させる可能性がある!
      <!-- - 両方の技術は、効果的であるためにデータと**クエリパターンの理解を必要**、不適切な使用は最適でないパフォーマンスにつながる可能性がある! -->
  - Partitioningとの違い
    - 物理的 vs 論理的な分割!
      - Partitioningはデータを異なるファイルに物理的に分割する。
      - Clusteringは同じファイル(partition)内で論理的に整理する。
    - 粗い vs 細かい粒度!
      - Partitioningは粗い粒度で機能し、データセットを大きな塊(chunks)に分割する
      - Clusteringはより細かい粒度で機能し、各塊(chunk)内の行の配置を最適化する。
    - ストレージオーバーヘッドが高い vs 低い!
      - Partitioningはデータファイル数の増加を伴うため、一般的にストレージオーバーヘッドが高い。
      - Clusteringはデータファイル数を増やさないため、一般的にストレージオーバーヘッドが低い。

- ex.) ユーザidでフィルタリングするSQLクエリを実行したい場合:
  - もし**データがランダムに分散してる**と...
    - クエリエンジンは**全てのデータファイルをスキャンする必要**がある!
  - もし**データがソートまたはクラスタリングされてる**と...
    - クエリエンジンは**ファイル全体や行グループをスキップできる**ため、I/Oを削減し、実行を高速化できる!


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
