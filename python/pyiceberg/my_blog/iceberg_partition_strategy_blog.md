<!-- タイトル: Feature Store調べてたらレイクハウスアーキテクチャと繋がったのでIcebergテーブルフォーマットについて調べた! パーティション戦略編! -->


## TL;DR

- Icebergテーブルのパフォーマンスを最大化するための重要な要素の一つに、**パーティショニング(partitioning)戦略**がある。本記事はそれについて調査したもの。
- Feature Storeのオフラインストア文脈では、**大量or大きな特徴量レコード達に対してなるべく高速 & 安価なクエリ**を実現することが、モデルの品質改善やプロジェクトの成功にとって重要な要件の一つ。Icebergのパーティショニング戦略は、これを実現するための重要な設計要素の一つ。
- Icebergは従来のfolder-based (explicit) partitioningとは異なり、**hidden partitioning（メタデータ駆動型）**を採用しており、クエリ性能の向上や運用しやすさ、パーティション進化の柔軟性などのメリットがある。
- パーティショニング戦略のtips
  - パーティションは「**よく使うWhere句（filter条件）とテーブルサイズから逆算**」するのが基本!
  - 時系列イベントテーブルでは day(event_time) や month(event_time) から始めるのが無難。
  - 高カーディナリティカラム（user_idやitem_idなど）をそのままpartition keyにするのは非効率だし危険。 `bucket(id, N)`が推奨されてる文献もあるが、このようなハッシュパーティショニングは、類似値が同じパーティションに配置されるような挙動ではないので、クエリ性能の改善の観点では効果が薄いと思われる。**なので高カーディナリティカラムは、partitioningではなくsort order機能の方でクエリ性能を向上させるのが有効なのかな**と思ってる...!:thinking:
- ただまあIcebergはパーティション進化が得意なので、まずは気負いすぎずpartition無し or 粗い粒度から始めて、データの増加やクエリパターンの変化がある場合などに必要に応じて洗練させていくのが良さそう...!!:thinking:


## はじめに: なんでこの記事を??

本記事は、Icebergテーブルフォーマットのパーティショニングの仕組み、パーティショニング戦略のtipsなどを調査した結果をまとめたものです。

- なぜIcebergテーブルフォーマットを??
  - 要約すると、自分はMLOpsに関心があってFeature Storeの本を読んでたら、オフラインストアの実装にレイクハウスアーキテクチャが採用されることが多いと書いてあったので、その中核技術であるIcebergテーブルフォーマットについて調べている、という感じ。
    - より詳細は、前回の記事([Feature Store調べてたらレイクハウスアーキテクチャと繋がったのでIcebergテーブルフォーマットについて調べた! スキーマ進化編!](https://qiita.com/morinota/items/a670abb84cf5aca480b2))へ!
- なぜIcebergのパーティショニング戦略を??
  - Feature Store (のオフラインストア) がビジネスで価値を発揮するための要件として、**大量or大きな特徴量レコード達に対してなるべく高速 & 安価なクエリ**を実現することが重要。
    - (注意点として、リアルタイムで低レイテンシアクセスできるほど高速、という意味ではないです!その役割はオフラインストアではなくオンラインストアが担うので。ここでは寧ろ、学習用/バッチ推論用に大きなデータセットを作成する際のクエリ性能の話をしてます!)
  - もし学習データセット作成時の**クエリが遅い or 高コストになってしまうと**、データサイエンティストが特徴量の探索やモデルのトレーニングを行う際のフィードバックループが遅くなってしまい、**結果的にモデルの品質向上やプロジェクトの成功に悪影響を与えてしまう可能性も高い**はず。
    - 特にMLプロジェクトの種類によっては、**データサイズの大きい埋め込み表現などのベクトル型の特徴量**を扱うことも多いので、何も気にしてないとクエリ性能が大幅に低下 or コスト爆増の可能性は十分に高いと思われる。
  - そして、**Icebergテーブルのクエリ性能を最大化するための重要な要素の一つに、パーティショニング(partitioning)戦略がある。**

## Icebergのパーティショニングの仕組み (Hidden Partitioning) の話

Icebergのパーティショニングは、**hidden partitioning**と呼ばれるアプローチを採用してる。どうやらこれが結構いい感じらしいです...!:thinking:

### そもそもpartitioningってどういう概念だっけという話。
- partitioning = 巨大なデータセットを**小さな複数のデータセットに分割**し、**キー属性に基づいて複数のパーティション(区画, 仕切り)に分配**するプロセス。
  - 全てのレコードは必ずどれか1つのパーティションに属する。
  - 各パーティションは、read / write を独立に実行でき、論理的には小さなデータベースのように振る舞う。
- なぜ分割したいのか??
  - 大規模データでは、テーブル全体スキャンは高コスト(I/Oの量, 時間, クラウド料金)
  - partitioningにより、クエリスコープを限定でき、不要なデータ塊をスキップできる(**partition pruning**と呼ばれる機能)
    - ex. `select ... where month(order_ts) = 10` みたいなクエリがあったときに、10月のパーティションだけを対象とすれば良いので、他の全ての関連しないファイル達をスキップできるようになる
- ちなみに...partitioningの分類: 水平 vs 垂直
  - 水平パーティショニング(Horizontal Partitioning, splitting rows): 
    - データセットを行単位で分割する方法。
  - 垂直パーティショニング(Vertical Partitioning, splitting columns):
    - データセットを列単位で分割する方法。
  - 大規模テーブルの場合は水平パーティショニングが一般的。
- ちなみに...一般的なpartitioning戦略
  - **範囲パーティショニング(Range Partitioning)**: 
    - 連続した値の範囲に基づいて行を分割する方法(ex. year/month/day)。時系列データと相性が良い。
  - **リストパーティショニング(List Partitioning)**: 
    - 明示的な値の集合に基づいて分割(ex. country=US/EU/JP)
  - **ハッシュパーティショニング(Hash Partitioning)**: 
    - ハッシュ関数を使用して行を分割(ex. user_idを16個のbucketに分割するみたいな)。
    - 注意点: **類似値を同じパーティションに配置するような挙動じゃないので、クエリ最適化の観点では効果は薄いらしい。**
  - **複合パーティショニング(Composite Partitioning)**: 
    - 複数戦略を組み合わせる方法(ex. 日付で範囲パーティショニングして、その中でさらにregionでリストパーティショニングするみたいな)。
- Partitioningがもたらすシステム的なメリット達:
  - Reducing query scope (クエリのスコープを限定できる)
  - Parallel processing (異なるパーティションに対して並列に読み書きできる)
  - High throughput (I/Oの効率化により高スループットを実現できる)
  - Scalability (複数マシンに異なるパーティションを分散できる)
  - Maintenance (古いパーティションをアーカイブしたり削除したりするのが簡単)
  - Availability (一部のパーティションが障害を起こしても、他のパーティションは利用可能なままにできる)

### 従来 (Iceberg以前) のpartitioningの方法と問題点

- Icebergより前の従来のテーブルフォーマット(Hiveなど)のpartitioningの仕組みは **Folder-based(Explicit) Partitioning**と呼ばれるアプローチを採用。
  - ざっくり「**パーティション = ディレクトリ構造**」という仕組み!
- このFolder-based Partitioningの何がつらいのか??
  - 1. 手動管理つらい:
    - パーティション追加・修復の運用が大変。
  - 2. 柔軟性が低くてつらい:
    - パーティションスキームの変更が困難。既存データを再書き込みする必要があることも多い。
  - 3. クラウドでの大量のlist操作がつらい:
    - S3のようなオブジェクトストレージで、ディレクトリを大量に辿るのがクエリのボトルネックになりやすい。
  - 4. クエリがパーティションを意識する必要があってつらい:
    - クエリを書く人が、どのようにパーティションが切られているかを明確に理解し、適切にwhere句でパーティションキーを参照する必要がある。
      - ex. `select ... where month(order_ts) = 10` みたいなクエリを書けばpruningが効く。しかし、`select ... where order_ts >= '2023-10-01' and order_ts < '2023-11-01'` みたいなクエリを書いてしまうと、pruningが効かずに全てのパーティションをスキャンしてしまう。
  - 5. メタストアが肥大化してつらい:
    - パーティションが増えるほど、Glue catalogのようなメタストアが肥大化し、そこがクエリ性能のボトルネックになりやすい。

### Icebergなどのモダンなpartitioningの方法と特徴

- Icebergは、伝統的なfolder-based partitioningから脱却して、**hidden partitioning (i.e. メタデータ駆動型アプローチ)**を採用。
  - 核となる思想は「Decouple partitioning from physical storage layout」。
    - つまりPartitioningを物理的なストレージレイアウトから切り離し、メタデータで管理するアプローチ。
  - パーティション情報はIcebergのメタデータファイル(manifestファイル)に保持される。
    - 具体的には、**各データファイルがどのパーティションに属するかの情報**が、メタデータファイルに保存される。
    - よってクエリ時の動作としては以下。
      - まず Query predicate (クエリのwhere句の条件) を解析。
      - 次に **メタデータファイルを参照して、条件を満たすパーティションに所属するデータファイル一覧を特定する。ここで高価なディレクトリのlist操作は発生しない!**
      - 最後に、特定されたデータファイルだけをスキャンする。
    - ↑はDirectory-based pruningに対してmetadata-driven file pruningと呼ばれるらしい。
- このhidden partitioningの重要な利点たち:
  - 1. パーティションカラムの詳細を意識しなくていい!
    - パーティション情報がテーブルメタデータに入ってるので、エンドユーザがクエリ内で物理的なディレクトリ構造を意識する必要がない。
  - 2. パーティション進化が楽。
    - パーティションスキームの変更が柔軟で、既存データを再書き込みする必要もない。
  - 3. list操作が不要でクエリ性能が向上。
    - S3のようなオブジェクトストレージでディレクトリを大量に辿る必要がないので、クエリ性能が大幅に向上する。

- Icebergのpartitioningの設定の流れ
  - 1. テーブル作成時
    - `PARTITIONED BY`句でパーティションの定義を宣言的(declarative)に指定する。
    - この際 Iceberg が提供する**組み込みの変換関数(transform functions)を使用**して定義する。以下が変換関数の一覧。
      - `identity(col)` - カラムの値をそのままパーティションキーにする。
      - `years(ts), month(ts), day(ts), hour(ts)` - タイムスタンプを年/月/日/時間粒度に変換してパーティションキーにする。
      - `bucket(N, col)` - カラムの値をN個のバケットにハッシュ分割してパーティションキーにする。
      - `truncate(L, col)` - カラムの値を先頭L文字・桁で切り捨ててパーティションキーにする。
  - 2. データ書き込み時
    - Iceberg が partition spec に基づいて変換関数を噛ませて**partition values を自動計算**。
    - データファイルを作成するとともに、各データファイルのpartition valueをメタデータファイルに登録する。
  - 3. データ読み込み(クエリ)時
    - クエリのwhere句の条件を解析。
    - メタデータファイルを参照して、条件を満たすパーティションに所属するデータファイル一覧を特定し、スキャンする。
  - 4. 必要に応じてパーティションスキームを変更する(Partition Evolution)
    - データ量や頻出のクエリパターンが変化してきたら、パーティションスキームを変更することも有効。
    - Icebergはパーティション進化が容易 (既存データを再書き込みする必要なし) なので。

- パーティション進化の挙動
  - 古いデータは古いパーティションスキームのまま、新しいデータは新しいパーティションスキームで書き込まれる。
  - クエリは自動的に両方のスキームを活用
  - データの書き換えは不要（Zero-Copy Evolution）

## Icebergのパーティショニング戦略のtips

「**どのカラムをどう変換して分割すべきか**」を**クエリパターンから逆算**して設計するのが基本!

- 基本的には、「**よく使うWhere句(i.e. filter条件)**」と「**テーブルサイズ**」から決める感じ!
- (1) そもそもpartitionすべきかの判断!
  - 全体で1TB未満くらいのテーブルだったら、無理にpartition切らない方がシンプルで良いことも多いらしい。
    - **過剰に小さくパーティションが切られていると逆にクエリ性能が悪化する事もある**らしい。
      - (たぶんここで悪化するのはクエリ時間。スキャンする量は下がるはずなので、例えばAthenaの場合はコストが下がるはず...!:thinking:)
  - まあ**パーティション進化が容易なので、まずは粗い粒度から始めて、データの増加やクエリパターンの変化がある場合などに必要に応じて洗練させていく**のが良さそう...!!:thinking:
- (2) 時系列イベントテーブルなら...
  - まずは`day(event_time)`や`hour(event_time)`でpartition切るのが無難。
  - 1日にどれくらいデータ入るか見て、日次で多すぎるなら時間単位に、少なすぎるなら月単位を検討する感じ。
- (3) ユーザ/テナント単位のアクセスが多いなら...
  - 日付 + `bucket(user_id, 16)`みたいな、複合partitionを検討。
  - Nは「1partitionあたりの数百MB〜数GB」くらいに落ち着くように試す。
  - ただ個人的に、この `bucket()` という変換関数はあんまり意味ない気がしてる...!!:thinking:
    - **結局ハッシュに基づいて分割するだけなので、あんまりpartitioning pruningでクエリ性能を向上させるという効果は薄い**っぽい。
- (4) カラムのcardinalityを意識する
  - row cardinalityなカラム (ex. countryが数十種類) → `identity(country)`は全然あり。
  - high cardinalityなカラム (ex. user_idが数百万 ~ 数千万以上) → `bucket(16, user_id)`とか`truncate(3, user_id)`みたいに変換をかける。
    - ただ上述した理由で`bucket()`はあまり効果的じゃない気がしてる。**なのでhigh cardinalityなカラム、特にuser_idやitem_idなどの連番っぽいカラムは、partitioningではなくsort order機能の方でクエリ性能を向上させる、のが有効なのかな〜**と思ってる...!:thinking:
  - 基本的には、**低カーディナリティで比較的一様な分布を持つkey**がpartition keyに適してる。
    - 推奨されるkeyの例:
      - 時系列データ: `days(timestamp)`, `hours(timestamp)`
      - カテゴリカルデータ: `region`, `product_category`, `customer_segment`
      - 高カーディナリティ列の場合: `bucket(user_id, N)` (でもこれはハッシュパーティショニングなので個人的に微妙そう...!:thinking:)
    - 避けるべきkeyの例:
      - `user_id`, `transaction_id` などの高カーディナリティ列（バケット化を使わない場合）

## おわりに

## 参考資料

- [What is Hidden Partitioning in Apache Iceberg?](https://www.stackgazer.com/p/what-is-hidden-partitioning-in-apache-iceberg)
- [Iceberg Partitioning and Performance Optimization (Conduktor)](https://conduktor.io/glossary/iceberg-partitioning-and-performance-optimization)
- [Best Practices for Optimizing Apache Iceberg Performance (Starburst)](https://www.starburst.io/blog/best-practices-for-optimizing-apache-iceberg-performance/)
- [Iceberg Partitioning vs. Hive Partitioning](https://olake.io/iceberg/hive-partitioning-vs-iceberg-partitioning/)
