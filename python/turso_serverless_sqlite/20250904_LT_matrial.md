---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Noto Sans JP', sans-serif;
  }
  h1 {
    color: #00d4aa;
    border-bottom: 3px solid #00d4aa;
    padding-bottom: 10px;
  }
  h2 {
    color: #00a688;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  code {
    background-color: #f4f4f4;
    padding: 2px 4px;
    border-radius: 3px;
  }
  pre code {
    background-color: transparent;
    padding: 0;
  }
  blockquote {
    border-left: 4px solid #00d4aa;
    padding-left: 10px;
    color: #666;
  }
  .highlight {
    background-color: #fffacd;
    padding: 2px 4px;
    border-radius: 3px;
  }
---

# Turso + SQLite で実現する
# エッジ分散データベース

2025.09.04 LT

---

# 今日話すこと

1. **SQLiteってそもそも何がすごいの？**
2. **なぜSQLiteを書き直す必要があったのか？**
3. **Tursoって何？その革新性**
4. **Embedded Replicasによる爆速DB体験**
5. **Python連携とVector Searchの実装**

---

# SQLiteの意外な実力 🚀

## 世界で一番使われているRDBMS

- **利用者数: 数十億人** 😲
  - なぜSQLiteの利用者は数十億人もいるのか?? 
  - → **Android や iOS、つまりスマホに組み込まれているから**！(なるほどエッジデバイス上で動作してるからか:thinking:)
- **組み込み型データベース**
  - サーバー不要、設定不要
  - パッケージ管理システム上でインストールするだけ！
- **20年以上の実績**
  - エッジデバイスで問題なく動作してきた歴史

---

# SQLiteが選ばれる理由

<div class="columns">

<div>

## 🎯 パフォーマンス
- OSのAPIをネイティブで呼び出せるC言語で作られてるから高速
- **ファイルシステムへの直接アクセスよりも速い！**
- ほとんどフル機能のSQL実装

</div>

<div>

## 🔒 信頼性
- **オープンソースであってもオープンコントリビュートではない**
- 「互換性がない方法で変更しない」と明言してるらしい
- どんな環境でも動作するように設計されている

</div>

</div>

---

# SQLiteの現実的な課題 ⚠️

## 現代のアプリケーションが求めるもの vs SQLite

- **同時書き込みができない**
  - 低スループットでも書き込み失敗のリスクがある
- **リアルタイムアプリケーションに不向き**
  - 変更ストリームをキャプチャする仕組みがない
- **同期APIのみ**
  - ブラウザなどの環境で使いにくいっぽい
- **スキーマ進化の困難さ**
  - カラム削除・型変更時はテーブル作り直しが必要

---

# Tursoの解決アプローチ 🚀

## SQLiteを**Rustで完全書き直し**してlibSQLを作った

- **🔄 非同期API**: ブラウザでもシームレスに動作
- **⚡ 同時書き込み対応**: 高スループットを実現
- **🤖 Native Vector Search**: 外部依存なしでAI/ML対応
- **🌐 クラウドネイティブ設計**: エッジ分散を前提

> 💡 **「地球上で最高のソフトウェア」SQLiteを現代に適応させた！**

---

# Tursoの信頼性への取り組み 🛡️

## SQLiteを超える信頼性を目指してるらしい

<div class="columns">

<div>

### 🔬 最先端テスト手法
- **Deterministic Simulation Testing (DST)**
- **Antithesis との提携**
- 数千の障害シナリオを体系的にテストしてる

</div>

<div>

### 💰 品質への自信
- **$1,000 バグバウンティ**
- データ破損バグを発見で報酬がもらえる！
- SQLiteの伝説的信頼性を継承・超越を目指す

</div>

</div>

---

# Tursoとは？ 🌍

## SQLiteをクラウド・エッジで使えるようにした分散DB

- **SQLiteベースのエッジ向け分散データベースプラットフォーム**
- libSQL（SQLiteのフォーク）を基盤としてる
- グローバルに分散したデータベースレプリカにより、**ユーザーの近くでデータを読み書きでき、低遅延を実現**
- **115人以上の貢献者**による活発な開発中！

> 💡 **libSQL** = SQLite + クラウド/分散環境向け機能
> 💡 **Turso** = libSQLを基盤としたクラウド分散データベースサービス

---

# Embedded Replicas の魔法 ✨

## ローカル爆速 + クラウド同期のハイブリッドな仕組み

```
┌─────────────┐        自動同期        ┌──────────────┐
│  ローカル    │ ◀──────────────────▶ │ Turso Cloud  │
│  SQLite     │                      │   (libSQL)   │
└─────────────┘                      └──────────────┘
     ↑
     │ 読み込み: 0ms（ローカル完結）
     │ 書き込み: クラウド経由で同期
     ↓
アプリケーション
```

> 💡 ローカルにレプリカ(SQLiteのファイル)を持ちつつ、クラウド上のメインDBと同期できる仕組み！

---

# Embedded Replicasのメリット

## **SELECT等の読み込みは完全ローカル動作**

- 🚀 **通信待ちゼロでクエリ爆速！**
- 📱 **APIサーバーやローカルPCだけでなく、モバイル端末やエッジデバイスでも使える**
- 🔄 バックグラウンドで自動同期（ネットが繋がってる時）
- 💾 オフライン時も読み込み可能

---

# Turso CLIで簡単セットアップ

```bash
# インストール
brew install tursodatabase/tap/turso

# サインアップ & ログイン
turso auth signup
turso auth login

# データベース作成
turso db create my-edge-db

# SQLite CLIでデータベースに接続
turso db shell my-edge-db
# → これで**SQLiteのCLIが立ち上がる**
```

> 💡 Tursoにはダッシュボードもあるけど、どうやら**主にCLIを使って操作していくことを想定してる**っぽい！

---

# PythonからTursoを使う 🐍

```python
import libsql
import os

# Embedded Replicas（ローカル + クラウド同期）
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")

conn = libsql.connect("hello.db", 
                     sync_url=url, 
                     auth_token=auth_token)
# 初回同期
conn.sync()

# ローカルで高速読み込み
conn.execute("SELECT * FROM users").fetchall()

# 書き込み後の同期
conn.execute("INSERT INTO users(id) VALUES (1);")
conn.commit()
conn.sync() # sync your local database with the primary database(cloud)
```

> 💡 PythonからTursoに接続するには、libSQL SDKのlibSQL clientを使えばOK！

---

# Native Vector Search対応 🔍

## 2024年6月からベクトル検索をネイティブサポート！

**AI/MLアプリケーションが外部依存なしで実現可能**  
**基本的にはただデータ型を指定するだけっぽい！**

```sql
-- ベクトルカラムを定義（拡張機能不要！）
CREATE TABLE movies (
  title TEXT,
  year INT,
  embedding F32_BLOB(3)  -- float32の3次元array
);

-- ベクトルデータの挿入
-- vector()関数: 文字列表現をベクトルに変換する関数
INSERT INTO movies VALUES 
  ('Gladiator', 2000, vector('[7,8,9]'));

-- コサイン類似度で検索
SELECT title, vector_extract(embedding),
       vector_distance_cos(embedding, vector('[5,6,7]'))
FROM movies
ORDER BY vector_distance_cos(embedding, '[5,6,7]')
LIMIT 3;
```

---

# 高速化のためのANNインデックス

```sql
-- ANNインデックスの作成（DiskANNアルゴリズム）
-- index作成時...libsql_vector_idx()関数でベクトルカラムをwrapするだけでいいっぽい!
CREATE INDEX movies_idx ON movies(
  libsql_vector_idx(embedding)
);

-- 高速ベクトル検索
-- vector_top_k()関数を使ってANNインデックスを指定して、元テーブルとjoinする必要がある
SELECT title, year FROM 
  vector_top_k('movies_idx', '[4,5,6]', 3)
JOIN movies ON movies.rowid = id
WHERE year >= 2020;
```

> 💡 より大きなデータセットで高速に検索したい場合、Tursoは**ANN(Approximate Nearest Neighbor)をサポート**している

---

# 既存SQLiteからの移行も簡単

```bash
# SQLiteファイルの準備
sqlite3 my-database.db
> PRAGMA journal_mode=WAL;  # WAL journalモードを設定
> PRAGMA wal_checkpoint(truncate);  # checkpointを実行
> PRAGMA journal_mode;  # 返り値が`wal`であることを確認
> .exit

# Tursoにインポート（一発！）
turso db import ~/path/to/my-database.db
# データベース名はSQLiteファイル名から自動的に決定される

# 既存グループにインポートする場合
turso db import --group production ~/path/to/my-database.db
```

> 💡 全てのテーブル、データ、スキーマがimportされる

---

# 実用事例: Spice.ai 🌟

## AIデータ推論エンジンでの採用

- **Spice.ai**: SQLite/DuckDBをアクセラレーターとして使用してる
- **Turso採用の理由**:
  - 一部クエリでSQLiteより高性能らしい
  - 同時書き込み対応でさらなる性能向上を期待
- **エッジでのAI推論**が現実的になってきた

> 💡 軽量DBへのワークロードシフトが加速中っぽい

---

# まとめ

## Tursoで実現できること

- ✅ **SQLiteの課題を解決**
  - 同時書き込み・非同期API・リアルタイム対応
- ✅ **エッジでの爆速データベース**
  - ローカル読み込みで遅延ゼロ！
- ✅ **グローバル分散とローカル性能の両立**
  - Embedded Replicasによる「**爆速ローカル読み込み + クラウド同期**」
- ✅ **モダンな機能をSQLiteで**
  - Native Vector Search対応（外部依存なし！）
- ✅ **活発なオープンソースコミュニティ**
  - 115人以上の貢献者が参加中

---

# 参考資料 📚

- [Turso公式ドキュメント](https://docs.turso.tech/)
- [libSQL GitHub](https://github.com/libsql/libsql)
- [Embedded Replicas解説](https://docs.turso.tech/features/embedded-replicas/introduction)
- [Native Vector Search](https://turso.tech/blog/turso-brings-native-vector-search-to-sqlite)
- [SQLAlchemy + Turso連携](https://docs.turso.tech/sdk/python/orm/sqlalchemy)

---

# ご清聴ありがとうございました！ 🎉

## Questions?

**Turso + SQLite**で
エッジコンピューティング時代の
データベースを体験しよう！

GitHub: [@your-github]
Twitter: [@your-twitter]
