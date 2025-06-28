## refs:

- [DuckDB-Wasm: Efficient Analytical SQL in the Browser](https://duckdb.org/2021/10/29/duckdb-wasm.html)

## DuckDB-Wasmについて

- DuckDB-Wasmは、**ブラウザ内で動作するインプロセス分析SQLデータベース**。
  - WebAssemblyを基盤とする。


### ブラウザ内での効率的な分析

- Webブラウザは現在、普遍的な計算プラットフォームへと進化してる。


## OPFSって??

- **ブラウザの中のファイルストレージ機能**のひとつ。
  - 正式にはOrigin Private File System（オリジンプライベートファイルシステム）。
  - ざっくり: **ブラウザの中に、ページ専用のローカルファイル保存領域を持てる仕組み**。
- OPFSで何ができる??
  - ブラウザ上に「仮想ディスク」みたいな領域が作れる。
  - 他のドメイン（オリジン）からはアクセスできない → セキュア。
  - DuckDB-Wasm とかで使うと、SQLのテーブルとかParquetファイルを保存して、次回も使えるようになる。
- 通常の仮想ファイルとの比較:
  - 通常の仮想ファイルはブラウザリロードしたら消える。OPFSは永続化される。
  - 通常の仮想ファイルは、メモリ上だけで動く。OPFSはブラウザのストレージに書き込まれる。
  - 通常の仮想ファイルは、小規模データのみ。OPFSは大規模データも扱える。

実装イメージ:


```typescript
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(duckdb_wasm, {
  // OPFSを使うオプション
  path: 'my_database.db', // OPFS上のデータベースファイル名
  useOPFS: true, // OPFSを使用するフラグ
});
```

- 注意点:
  - OFPSサポートしてるブラウザは限定されてる。(Chrome系が安定)
  - 
