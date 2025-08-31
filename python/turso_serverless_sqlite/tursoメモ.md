## refs:

- [SQLite互換サーバーレスDB Turso & FastAPI](https://zenn.dev/ikumasudo/articles/df8ab4fb01038c)
- [みんな、libSQLとTursoについてどう思う？](https://www.reddit.com/r/sqlite/comments/1doizwk/what_do_yall_think_of_libsql_and_turso/?tl=ja)
- [Tursoを軽く触ってみた](https://zenn.dev/ryohei0509/articles/62b80b47483425)
- [Turso Quickstart (Python)](https://docs.turso.tech/sdk/python/quickstart)
- [Embedded Replicas](https://docs.turso.tech/features/embedded-replicas/introduction)
- [Turso brings Native Vector Search to SQLite](https://turso.tech/blog/turso-brings-native-vector-search-to-sqlite)
- Turso + ORMについて: [SQLAlchemy + Turso](https://docs.turso.tech/sdk/python/orm/sqlalchemy)
- sqlite -> tursoのmigrate: [Migrate to Turso](https://docs.turso.tech/cloud/migrate-to-turso)
- [利用者は数十億人！？ SQLiteはどこが凄いデータベース管理システムなのか調べてみた](https://qiita.com/ko1nksm/items/87d27a287e1b6005d11c)

## ざっくりTursoの雰囲気を掴みたい。

- Tursoは、軽量で高速なSQLiteデータベースを元にしたクラウド分散DBサービス。
  - SQLiteをベースにした、エッジ向けの分散データベースプラットフォーム。グローバルに分散したデータベースレプリカにより、**ユーザーの近くでデータを読み書きでき、低遅延を実現**。
- まずSQLiteってなんだっけ??
  - DBMSの中での位置付け:
    - まず組み込み型！ RDSやサーバー・クライアント型ではない。
      - 組み込み型の中では、OLTP(オンライントランザクション処理)向け！OLAP(オンライン分析処理)向けではない。
  - 世界で一番多く使われてるRDBMSらしい。
    - なぜSQLiteの利用者は数十億人もいるのか?? 
      - -> **Android や iOS、つまりスマホに組み込まれているから。** (なるほどエッジデバイス上で動作してるからか:thinking:)
      - 多くのRDBMSとは異なり組み込み型なので。
  - SQLiteの信頼性が高いって言われるのはなぜ??
    - 1. 歴史が長く、20年以上エッジデバイスで問題なく使用されてきた。
    - 2. どんな環境でも動作するように設計されている(らしい)。
    - 3. オープンソースでも危険なコードの混入はない。
      - -> **オープンソースであってもオープンコントリビュートではない**。
    - 4. 互換性が高く、SQLiteをアップデートしてもアプリケーション側の修正は不要。
      - 「互換性がない方法で変更しない」と名言してるらしい。
  - SQLiteはRDBMSとして何がすごいの??
    - 利用するための設定作業が全く不要! パッケージ管理システム上でインストールするだけ。
    - ほとんどフル機能のSQL実装。
    - OSのAPIをネイティブで呼び出せるC言語で作られてるから高速。パフォーマンスが良い。
      - ファイルシステムへの直接アクセスよりも速い!
    - NoSQLとしても使える(JSON形式・半構造化データへの対応)
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


# クラウド上のTurso DBにアクセスする場合(Embedded Replicas)
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")

conn = libsql.connect("hello.db", sync_url=url, auth_token=auth_token)
conn.sync()

# Local Onlyなsqliteファイルにアクセスする場合
# conn = libsql.connect("hello.db")
# cur = conn.cursor()

# SQLクエリの実行
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER);")
conn.execute("INSERT INTO users(id) VALUES (10);")

print(conn.execute("select * from users").fetchall())

# Sync (Embedded Replicasを使ってる場合のみ)
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER);")
conn.execute("INSERT INTO users(id) VALUES (1);")
conn.commit()

conn.sync() # sync your local database with the primary database(cloud)

print(conn.execute("select * from users").fetchall())
```

### Native Vector Searchのサポート

- 2024年6月に、Tursoがnativeな**Vector Similarity Search**をサポートしたらしい。
- 具体的な使い方:　基本的には**ただデータ型を指定するだけっぽい!**
  - 拡張機能は不要。
  - TursoクラウドDBでも、ローカルのインメモリDBでも、同様に動作する。
  - 

例:

```sql
-- テーブル作成時に、embeddingカラムをF32_BLOB(3)型(=float32の3次元array)で定義
CREATE TABLE movies (
  title TEXT,
  year INT,
  embedding F32_BLOB(3)
);

-- Insert時には、vector('[1,2,3]')のようにvector()関数で指定すればOKっぽい。
-- vector()関数: 文字列表現をベクトルに変換する関数
INSERT INTO movies (title, year, embedding)
VALUES
  (
    'Napoleon',
    2023,
    vector('[1,2,3]')
  ),
  (
    'Black Hawk Down',
    2001,
    vector('[10,11,12]')
  ),
  (
    'Gladiator',
    2000,
    vector('[7,8,9]')
  ),
  (
    'Blade Runner',
    1982,
    vector('[4,5,6]')
  );

  -- 検索時には、vector_distance_cos()関数でコサイン類似度を計算できる。
  -- vector_extract()関数: vector()関数の逆。つまり、ベクトルを文字列表現に変換する関数
  SELECT title,
       vector_extract(embedding),
       vector_distance_cos(embedding, vector('[5,6,7]'))
  FROM movies;

  -- 例えば、2020年以降の映画で、embeddingが[3,1,2]に最も近い上位3件を取得するクエリは以下の通り:
  SELECT *
  FROM
    movies
  WHERE
    year >= 2020
  ORDER BY
    vector_distance_cos(embedding, '[3,1,2]')
  LIMIT 3;
```

- Indexingについて
  - より大きなデータセットで高速に検索したい場合、Tursoは**ANN(Approximate Nearest Neighbor)をサポート**している(具体的にはDiskANNというアルゴリズムを使用してるらしい)。
  - 方法:
    - index作成時...`libsql_vector_idx()`関数でベクトルカラムをwrapするだけでいいっぽい!
    - ANN検索時...
      - インデックスは内部的には別テーブルとして表現されるので、前述のクエリのままでは自動ではANNにならない。
      - 以下のように `vector_top_k()`関数を使ってANNインデックスを指定して、元テーブルとjoinしてあげる必要があるみたい!

例:

```sql
-- embeddingカラムに対してANNインデックスを作成
CREATE INDEX movies_idx ON movies ( libsql_vector_idx(embedding) );

-- 上述のクエリの、ANNを使ったver.
SELECT
  title,
  year
FROM
  vector_top_k('movies_idx', '[4,5,6]', 3)
JOIN
  movies
ON
  movies.rowid = id
WHERE
  year >= 2020;
```

### TursoのAuthenticationについて!

- SDKを使ってTursoのDBにアクセスする際には、**Database URL + Auth Token(認証トークン)**を必要とする。
  - Database URL
    - URLの確認はTurso CLIもしくはPlatform APIを使ってできる。
    - `libsql://`プロトコルもしくは`https://`プロトコルのどちらでもOK。
      - `libsql://[DB-NAME]-[ORG-NAME].turso.io`
      - `https://[DB-NAME]-[ORG-NAME].turso.io`
      - それぞれパフォーマンスに得手不得手がある。
  - Auth Token
    - クラウド上のDBにアクセスする際、SDKはauth tokeを必要とする。
    - DB(もしくは複数のDBのグループ)のための新しいトークンは、Turso CLIもしくはPlatform APIを使って作成できる。
    - `full-access`と`read-only`の2種類の権限レベルがある。
    - tokeの有効期限も設定できる。
    - 必要に応じて全てのトークンを無効化することも可能。

### 既存SQLite DBからTursoへのimport

- 準備:
  - 対象のSQLite databaseを開く
    - `sqlite3 path/to/your/database.db`
  - WAL journalモードを設定する。
    - `PRAGMA journal_mode=WAL;`
  - checkpointを実行する。
    - checkpointを実行して、全ての変更がmainデータベースに書き込まれて、WALファイルがtruncate(削除)されるようにする。
    - `PRAGMA wal_checkpoint(truncate);`
  - journalモードを確認する。
    - `PRAGMA journal_mode;`
    - 返り値が`wal`であることを確認する。
  - SQLiteデータベースを閉じる。
    - `.exit`
  - これでTursoへのimport準備は完了!
- Turso CLIを使ってimport
  - `turso db import ~/path/to/your/database.db`
  - データベース名はSQLiteファイル名から自動的に決定される。
  - 全てのテーブル、データ、スキーマがimportされる。
  - もし既存のグループに、SQLiteデータベースをimportしたい場合は、`--group`フラグを使う。
    - `turso db import --group <group_name> ~/path/to/my-database.db`
