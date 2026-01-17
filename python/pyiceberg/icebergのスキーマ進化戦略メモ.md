## これは何?

- Apache Icebergのスキーマ進化戦略に関するメモです。

## 参考資料

- [公式ドキュメント](https://iceberg.apache.org/docs/1.7.1/evolution/)
- [How to Achieve Seamless Schema Evolution with Apache Iceberg](https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg)

## ざっくりメモ

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
