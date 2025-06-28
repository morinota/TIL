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
- 最近DuckDB-WasmがOPFS対応がマージされた。
  - [Add OPFS (Origin Private File System) Support by e1arikawa · Pull Request #1856 · duckdb/duckdb-wasm](https://github.com/duckdb/duckdb-wasm/pull/1856)
  - DuckDB-Wasmのデータベース保存先をOPFSにするという仕組み。
  - 利用方法はシンプルで db.instantiate した後に db.open で path に `opfs://` から始める。
    - 書き込みと読み込みをするので、アクセスモードは `READ_WRITE` を指定する。
- 注意点:
  - OFPSサポートしてるブラウザは限定されてる。(Chrome系が安定)

実装イメージ:

```typescript
import * as duckdb from '@duckdb/duckdb-wasm'
import duckdb_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?worker'
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url'

const worker = new duckdb_worker()
const logger = new duckdb.ConsoleLogger()
const db = new duckdb.AsyncDuckDB(logger, worker)

// instantiate DuckDB with the worker and wasm module
await db.instantiate(duckdb_wasm)
// open a database in OPFS
await db.open({
    path: 'opfs://duckdb-wasm-opfs.db',
    accessMode: duckdb.DuckDBAccessMode.READ_WRITE,
})

// 書き込む場合は、
```


