## refs:

- [SQLite互換サーバーレスDB Turso & FastAPI](https://zenn.dev/ikumasudo/articles/df8ab4fb01038c)
- [みんな、libSQLとTursoについてどう思う？](https://www.reddit.com/r/sqlite/comments/1doizwk/what_do_yall_think_of_libsql_and_turso/?tl=ja)
- [Tursoを軽く触ってみた](https://zenn.dev/ryohei0509/articles/62b80b47483425)
- [Turso Quickstart (Python)](https://docs.turso.tech/sdk/python/quickstart)
- [Embedded Replicas](https://docs.turso.tech/features/embedded-replicas/introduction)

## ざっくりTursoの雰囲気を掴みたい。

- Tursoは、軽量で高速なSQLiteデータベースを元にしたクラウド分散DBサービス。
- Tursoの**Embedded Replicas**という仕組み:
  - ざっくり!: 
    - ローカルにレプリカ(SQLiteのファイル)を持ちつつ、クラウド上のメインDBと同期できるハイブリッドな仕組み。これにより「**爆速ローカル読み込み + クラウド同期**」の両方が実現される!
    - もう少し詳細:
      - ローカルのSQLiteファイルが、「TursoクラウドのlibSQL本体」と自動でデータ同期される（ネットが繋がってる時はバックグラウンドでsync）
      - **クラウドDBのデータをローカルSQLiteファイルにレプリケート**して、**SELECT等の読み込みは完全にローカル動作 → 通信待ちゼロでクエリ爆速！**
      - INSERTやUPDATEは基本クラウド側で処理され、ローカルに反映される形。オフライン書き込みや一部β機能も拡張中っぽい。
    - **Embedded ReplicasはAPIサーバーやローカルPCだけでなく、モバイル端末やエッジデバイスでも使える**。

### Turso CLIについて

- Tursoにはデータベースを管理するためのダッシュボードがある。しかし、ダッシュボード上でできる操作は結構限りがあるらしい。どうやら**主にCLIを使って操作していくことを想定してる**っぽい...!!
- Turso CLIの基本コマンドを軽くメモ:
  - install
    - `brew install tursodatabase/tap/turso`
  - sign up
    - `turso auth signup`
  - login
    - `turso auth login`
  - create a database
    - `turso db create <db-name>`
  - show a information of a database
    - `turso db show <db-name>`
    - get the database URL
      - `turso db show --url <db-name>`
      - 認証情報は `TURSO_DATABASE_URL` という環境変数に入れておくと良い。
  - get the database authentication token
    - `turso db token create <db-name>`
    - 認証情報は `TURSO_AUTH_TOKEN` という環境変数に入れておくと良い。
  - connect to database shell
    - `turso db shell <db-name>`
    - → これで**SQLiteのCLIが立ち上がる**。
    - ex.
      - 新規テーブル作成
        - `CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);`
      - テーブルへのデータ挿入
        - `INSERT INTO users (name, age) VALUES (1, 'Alice', 30);`
      - select文でデータ取得
        - `SELECT * FROM users;`
      - テーブル一覧
        - `.tables`
      - テーブルのスキーマ確認
        - `.schema users`
      - shellから抜ける
        - `.exit`　もしくは `Ctrl + C`

### Python連携

- PythonからTursoに接続するには、libSQL SDKのlibSQL clientを使えるらしい。
  - libSQLとは??
    - SQLiteのフォーク(派生プロジェクト)。普通のSQLiteと互換性を保ちつつ、**クラウドや分散環境でも使えるように機能追加**されたDBエンジン。
    - libSQLとTursoの関係性は?
      - **Tursoは、libSQLを基盤としたクラウド分散データベースサービス**。
    - `poetry add libsql` でlibSQL Python SDKをインストール
    - `import libsql`

サンプルコード:

```python
import libsql
import os

url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")

# Embedded Replicas
conn = libsql.connect("hello.db", sync_url=url, auth_token=auth_token)
conn.sync()
