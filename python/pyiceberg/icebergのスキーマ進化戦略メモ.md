## これは何?

- Apache Icebergのスキーマ進化戦略に関するメモです。

## 参考資料

- [公式ドキュメント](https://iceberg.apache.org/docs/1.7.1/evolution/)
- [How to Achieve Seamless Schema Evolution with Apache Iceberg](https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg)


## 公式ドキュメントを読んだメモ:

- Icebergのスキーマ進化(Schema Evolution)は、以下の変更をサポートしてる:
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
  - 上記の変更は全部**メタデータだけ変える、データファイルは書き直さない**という仕組み。
    - だからパフォーマンス的にも優しい。
- 正しさの保証 (Correctness)
  - スキーマ進化による変更がお互いに独立してて、副作用はないことを保証してる。
  - 具体的には...
    - その1: カラム追加しても、既存の別カラムには影響しない。
    - その2: カラム削除しても、既存の別カラムには影響しない。
    - その3: カラム更新しても、既存の別カラムには影響しない。
    - その4: カラム順序を変更しても、対応する値は変わらない。
  - Icebergは、**テーブル内の各カラムを一意なIDで管理**してる。
    - よって、**新しいカラムを追加した時は必ず新しいIDが割り当てられる**。既存データが間違って使われることはない。
    - もしカラムを名前で追跡する形式だと、削除時や名前変更時に問題が起きやすい。
    - もしカラムを位置で追跡する形式だと、削除時に既存の他カラムに影響を与えてしまう。

## Sort order evolution (ソート順進化)

- sorting機能
  - Icebergテーブルは、partition内のデータをカラムでソートすることで、クエリ性能を向上できる.
  - **ソート順（sort order）**として、データファイルまたは delete ファイルごとに宣言できる。
- ソート順(sort order)の定義:
  - **ソート順ID（sort order id）**と、**ソートフィールド**のリストによって定義される。
  - ソートフィールドのリスト内での順序が、**データに対してソートが適用される順番**を表す。
- 各ソートフィールドは以下で定義される:
  - テーブルスキーマ内のソースカラム(単一or複数)のfield ID。
  - ソースカラムからソート対象の値を生成するための 変換関数(transform function)。
  - ソート方向(ascending or descending)。
  - nullの扱いを表すnull order
    - nulls first (nullを最初に)
    - nulls last (nullを最後に)
  - partition specと同様に、クエリのスキャン計画の最適化に使われる!
- スキーマやpartition仕様と同様に、既存Icebergテーブルのsort orderも後から変更できる。
  - sort orderをevolveしても、以前のソート順で書き込まれた古いデータはそのまま変更されない。

