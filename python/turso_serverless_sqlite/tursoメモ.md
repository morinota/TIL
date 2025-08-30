## refs:

- [SQLite互換サーバーレスDB Turso & FastAPI](https://zenn.dev/ikumasudo/articles/df8ab4fb01038c)

## ざっくりTursoの雰囲気を掴みたい。

- TursoはSQLite互換のサーバーレスデータベース。

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
