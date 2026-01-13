## これは何??

- Icebergテーブル形式を運用する上での、partition戦略について調査したメモ。

## 参考:

- [Iceberg Partitioning vs. Hive Partitioning](https://olake.io/iceberg/hive-partitioning-vs-iceberg-partitioning/)
- [Apache Iceberg Table Optimization #8: Hidden Pitfalls — Compaction and Partition Evolution in Apache Iceberg](https://dev.to/alexmercedcoder/apache-iceberg-table-optimization-8-hidden-pitfalls-compaction-and-partition-evolution-in-13f1)
- [What is Hidden Partitioning in Apache Iceberg?](https://www.stackgazer.com/p/what-is-hidden-partitioning-in-apache-iceberg)
- [Best Practices for Optimizing Apache Iceberg Performance](https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/)
- [Iceberg Partitioning and Performance Optimization](https://conduktor.io/glossary/iceberg-partitioning-and-performance-optimization)

##　Icebergのpartition戦略についてメモ:

- 「**どのカラムをどう変換して分割すべきか**」を**クエリパターンから逆算**して設計するのが基本!
- Icebergのpartitionの特徴:
  - Icebergでは**hidden partition**。
    - hidden partition = 後で!
    - クエリ描く人がpartition keyを意識しなくて良いっぽい...!:thinking:
  - day(timestamp)やbucket(id, 16)などの「transform」を定義しておくと、クエリ時にwhere句のfilterが自動でpartition filterに変換されてスキャン量を減らしてくれる。
  - 途中から `day(ts)` → `month(ts)` 等のように**partition specを変更する「partition evolution」も可能。なので最初の設計をミスっても詰みにならないのがかなりありがたい。**

- Icebergでよく使われるpartition transformたち:
  - `idendity(col)`
    - そのままpartition keyにする。`country`とか`tenant_id`みたいに、カーディナリティがそこそこなカラム向け。
  - `yeas(ts), month(ts), day(ts), hour(ts)`
    - 時系列テーブルのど定番。`day(ts)`か`hour(ts)`あたりがよく使われる印象。
  - `bucket(N, col)`
    - user_idやdevice_idみたいにカーディナリティが高すぎて直接partition keyにしづらいけど、よくfilter条件に使われるカラム向け。
    - ex. `bucket(16, user_id)`なら、user_idを16個のbucketに分割してpartition keyにする。
  - `truncate(width, col)`
    - 長い文字列やでかい数値を、先頭N文字・桁でグルーピングするときに使う。
    - ex. `truncate(3, country_code)`など。

- partition戦略を決める時の考え方:
  - 基本的には、「よく使うWhere句(i.e. filter条件)」と「テーブルサイズ」から決める感じ!
  - (1) そもそもpartitionすべきか?
    - 全体で1TB未満くらいのテーブルだったら、無理にpartition切らない方がシンプルで良いことも多い。
  - (2) 時系列イベントテーブルなら
    - まずは`day(event_time)`や`hour(event_time)`でpartition切るのが無難。
    - 1日にどれくらいデータ入るか見て、日次で多すぎるなら時間単位に、少なすぎるなら月単位を検討する感じ。
  - (3) ユーザ/テナント単位のアクセスが多いなら
    - 日付 + `bucket(user_id, 16)`みたいな、複合partitionを検討。
    - Nは「1partitionあたりの数百MB〜数GB」くらいに落ち着くように試す。
  - (4) カラムのcardinalityを意識する
    - row cardinalityなカラム (ex. countryが数十種類) → `identity(country)`は全然あり。
    - high cardinalityなカラム (ex. user_idが数百万 ~ 数千万以上) → `bucket(16, user_id)`とか`truncate(3, user_id)`みたいに変換をかける。
