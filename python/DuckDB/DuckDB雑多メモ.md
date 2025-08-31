## これは何?

- DuckDBについて雑多に調べたメモです。

## 参考文献

- [DuckDBが思った以上に便利だった話](https://techblog.cartaholdings.co.jp/entry/duckdb-trial)
- [DuckDB Tutorial For Beginners](https://motherduck.com/blog/duckdb-tutorial-for-beginners/)
- [DuckDB で S3 のサーバーアクセスログを集計できた](https://zenn.dev/jigjp_engineer/articles/a9e0bcfa536ad2)

## DuckDBの概要

- DuckDBは、**OLAP用途での利用を想定**された、無料・オープンソースの組み込みRDBMS(リレーショナルデータベース管理システム)。
- S3などのクラウドストレージや、ローカルファイルシステムに保存されたファイルを読み込んで、SQLクエリを実行することができる。
- 強み:
  - SQLが使える。(普通かと思ったが、他のツールだと割と独自言語のケースもあったりするらしい)
  - 移植性が高い。(主要なOS, 主要なCPUアーキテクチャで動作)
  - **csv，json，parquetなどの複数のファイルフォーマットを扱える**。
  - **クラウドストレージへ直接クエリできる点**。
    - **例えば、「RDSにある表とS3上にあるjsonをjoinして調査したい」というような場面でも、DuckDBならローカルで、かつワンストップで対応できる**。(そうなの!?)
  - 拡張性が高い。DuckDBの拡張を入れることで色々対応できるらしい。
  - **アプリケーションのリソースを使ってクエリを実行できる**。
    - これは組み込みのRDBMSゆえの利点...!!
    - PostgreSQLやMySQLなどのサーバ・クライアント型のRDBMSとは異なり、**DuckDBはクエリの実行をアプリケーションのリソースを使って行う**。なので追加のサーバコストなどがかからない!
      - ちなみに「サーバー・クライアント型のRDBMS」とは、
        - ざっくり「サーバー側」にDBエンジンが常に稼働してて、「クライアント側」がSQLクエリを投げて処理してもらう仕組み！
  - 無料!
  - **PythonのAPIも用意されてる!**

## .duckdbファイルについて

- .duckdbファイルは、DuckDBというRDBMS(RDB管理システム)にて、**データを永続化するために使用されるデータファイル形式**。
- **単一ファイル形式**: DuckDBはデータを単一のファイルに保存します。このファイルは.duckdb、.db、.ddbなどの拡張子を持つ。

## langchain_communityのDuckDBクラス

