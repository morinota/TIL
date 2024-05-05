## refs:

- https://zenn.dev/katzumi/scraps/6da7a9605b0753

# Data Source Architectual Patterns

Data Source Architectual Patternsとは、アプリケーションがDBやその他のデータソースとやり取りするための設計パターン。
データアクセスの複雑さを抽象化し、アプリケーションの他の部分とデータソースのやり取りを容易にする事を目的とする。

以下の4種類:

- Table Data Gateway:
  - DBのテーブルに対する操作を提供するオブジェクトのパターン。
  - **DBのテーブル毎にgatewayオブジェクトを作成**し、テーブルに対する全ての操作はtable gatewayオブジェクトを通じて行う。
- Row Data Gateway:
  - DBの各行に対応するオブジェクトのパターン。
- Active Record:
  - DBの各行に対応するオブジェクトで、自分自身を保存や削除するメソッドを持つ。
  - Active Recordオブジェクト自体がDBアクセスのメソッドを含む。
- Data Mapper:
  - **DBの行とdomain objectの間のmapping**を管理する専用オブジェクトを用意するパターン。

## DAO(Data Access Object)との関連

- DAOは、**データアクセスのためのインターフェースを提供する**オブジェクトのパターン。
  - 各テーブルや各レコードを表すオブジェクトに対して、アクセス操作を実行するためのインターフェースを提供する。
  - 特定のテーブルへのクエリ操作など。
