
# DuckDB-Wasm: Efficient Analytical SQL in the Browser ブラウザにおける効率的な分析SQL

André Kohn and Dominik Moritz
André Kohn と Dominik Moritz

2021-10-29
2021年10月29日

## TL;DR: 

DuckDB-Wasm is an in-process analytical SQL database for the browser. 
DuckDB-Wasmはブラウザ用のインプロセス分析SQLデータベースです。
It is powered by WebAssembly, speaks Arrow fluently, reads Parquet, CSV and JSON files backed by Filesystem APIs or HTTP requests and has been tested with Chrome, Firefox, Safari and Node.js. 
これはWebAssemblyによって動作し、Arrowを流暢に扱い、Filesystem APIやHTTPリクエストに基づくParquet、CSV、JSONファイルを読み込み、Chrome、Firefox、Safari、Node.jsでテストされています。
You can try it in your browser at shell.duckdb.org or on Observable. 
ブラウザでshell.duckdb.orgまたはObservableで試すことができます。

DuckDB-Wasm is fast! 
DuckDB-Wasmは高速です！
If you're here for performance numbers, head over to our benchmarks at shell.duckdb.org/versus. 
パフォーマンスの数値を知りたい方は、shell.duckdb.org/versusのベンチマークをご覧ください。


<!-- ここまで読んだ! -->

## Efficient Analytics in the Browser 効率的なブラウザ内分析

The web browser has evolved to a universal computation platform that even runs in your car.  
**ウェブブラウザは、車の中でも動作する普遍的な計算プラットフォームへと進化しました**。
Its rise has been accompanied by increasing requirements for the browser programming language JavaScript.  
その発展は、ブラウザプログラミング言語JavaScriptに対する要求の増加を伴っています。
JavaScript was, first and foremost, designed to be very flexible which comes at the cost of a reduced processing efficiency compared to native languages like C++.  
JavaScriptは、何よりもまず非常に柔軟であるように設計されており、C++のようなネイティブ言語と比較して処理効率が低下するというコストが伴います。
This becomes particularly apparent when considering the execution times of more complex data analysis tasks that often fall behind the native execution by orders of magnitude.  
これは、より複雑なデータ分析タスクの実行時間を考慮すると特に明らかになり、これらはしばしばネイティブ実行に比べて桁違いに遅れます。
In the past, such analysis tasks have therefore been pushed to servers that tie any client-side processing to additional round-trips over the internet and introduce their own set of scalability problems.  
そのため、過去にはそのような分析タスクはサーバーに押し込まれ、クライアント側の処理がインターネット上での追加の往復に結びつき、独自のスケーラビリティの問題を引き起こしていました。

The processing capabilities of browsers were boosted tremendously 4 years ago with the introduction of WebAssembly:  
**ブラウザの処理能力は、4年前にWebAssemblyの導入により大幅に向上しました**：

WebAssembly (abbreviated Wasm) is a binary instruction format for a stack-based virtual machine.  
WebAssembly（略してWasm）は、スタックベースの仮想マシンのためのバイナリ命令形式です。
Wasm is designed as a portable compilation target for programming languages, enabling deployment on the web for client and server applications.  
Wasmは、プログラミング言語のためのポータブルなコンパイルターゲットとして設計されており、クライアントおよびサーバーアプリケーションのためにウェブ上での展開を可能にします。

The Wasm stack machine is designed to be encoded in a size- and load-time efficient binary format.  
Wasmスタックマシンは、サイズとロード時間に効率的なバイナリ形式でエンコードされるように設計されています。
WebAssembly aims to execute at native speed by taking advantage of common hardware capabilities available on a wide range of platforms.  
WebAssemblyは、さまざまなプラットフォームで利用可能な一般的なハードウェア機能を活用することで、ネイティブ速度で実行することを目指しています。
(ref:https://webassembly.org/)  
（参照：https://webassembly.org/）

Four years later, the WebAssembly revolution is in full progress with first implementations being shipped in four major browsers.  
4年後、WebAssembly革命は本格的に進行中で、最初の実装が4つの主要なブラウザに出荷されています。
It has already brought us game engines, entire IDEs and even a browser version of Photoshop.  
すでにゲームエンジン、完全なIDE、さらにはPhotoshopのブラウザ版をもたらしています。
Today, we join the ranks with a first release of the npm library @duckdb/duckdb-wasm.  
本日、私たちは**npmライブラリ@duckdb/duckdb-wasm**の初回リリースで仲間入りします。

As an in-process analytical database, DuckDB has the rare opportunity to significantly speed up OLAP workloads in the browser.  
プロセス内分析データベースとして、DuckDBはブラウザ内のOLAPワークロードを大幅に加速する稀な機会を持っています。
We believe that there is a need for a comprehensive and self-contained data analysis library.  
私たちは、**包括的で自己完結型のデータ分析ライブラリの必要性**があると考えています。
DuckDB-wasm automatically offloads your queries to dedicated worker threads and reads Parquet, CSV and JSON files from either your local filesystem or HTTP servers driven by plain SQL input.  
**DuckDB-wasmは、クエリを専用のワーカースレッドに自動的にオフロードし、ローカルファイルシステムまたはプレーンSQL入力によって駆動されるHTTPサーバーからParquet、CSV、JSONファイルを読み取ります**。
In this blog post, we want to introduce the library and present challenges on our journey towards a browser-native OLAP database.  
このブログ投稿では、ライブラリを紹介し、**ブラウザネイティブのOLAPデータベース**への旅での課題を提示したいと思います。

DuckDB-Wasm is not yet stable.  
DuckDB-Wasmはまだ安定していません。
You will find rough edges and bugs in this release.  
このリリースには粗い部分やバグが見つかるでしょう。
Please share your thoughts with us on GitHub.  
GitHubで私たちにあなたの考えを共有してください。

<!-- ここまで読んだ! -->

## How to Get Data In? データの取り込み方法

Let's dive into examples.  
例を見ていきましょう。
DuckDB-Wasm provides a variety of ways to load your data.  
DuckDB-Wasmは、データをロードするためのさまざまな方法を提供します。
First, raw SQL value clauses like `INSERT INTO sometable VALUES (1, 'foo'), (2, 'bar')` are easy to formulate and only depend on plain SQL text.  
まず、`INSERT INTO sometable VALUES (1, 'foo'), (2, 'bar')`のような生のSQL値句は簡単に構成でき、単純なSQLテキストのみに依存します。
Alternatively, SQL statements like `CREATE TABLE foo AS SELECT * FROM 'somefile.parquet'` consult our integrated web filesystem to resolve `somefile.parquet` locally, remotely or from a buffer.  
また、`CREATE TABLE foo AS SELECT * FROM 'somefile.parquet'`のようなSQL文は、統合されたウェブファイルシステムに問い合わせて、`somefile.parquet`をローカル、リモート、またはバッファから解決します。
The methods `insertCSVFromPath` and `insertJSONFromPath` further provide convenient ways to import CSV and JSON files using additional typed settings like column types.  
`insertCSVFromPath`および`insertJSONFromPath`メソッドは、列の型などの追加の型設定を使用してCSVおよびJSONファイルをインポートする便利な方法を提供します。
And finally, the method `insertArrowFromIPCStream` (optionally through `insertArrowTable`, `insertArrowBatches` or `insertArrowVectors`) copies raw IPC stream bytes directly into a WebAssembly stream decoder.  
最後に、`insertArrowFromIPCStream`メソッド（オプションで`insertArrowTable`、`insertArrowBatches`または`insertArrowVectors`を通じて）は、生のIPCストリームバイトをWebAssemblyストリームデコーダに直接コピーします。

The following example presents different options how data can be imported into DuckDB-Wasm:  
以下の例は、DuckDB-Wasmにデータをインポートするさまざまなオプションを示します：

```javascript
// Data can be inserted from an existing arrow.Table 
// データは既存のarrow.Tableから挿入できます
await c.insertArrowTable(existingTable, { name: "arrow_table" });
// ..., from Arrow vectors
// Arrowベクトルから
await c.insertArrowVectors({
  col1: arrow.Int32Vector.from([1, 2]),
  col2: arrow.Utf8Vector.from(["foo", "bar"]),
}, { name: "arrow_vectors" });
// ..., from a raw Arrow IPC stream

const c = await db.connect();
const streamResponse = await fetch(`someapi`);
const streamReader = streamResponse.body.getReader();
const streamInserts = [];
while (true) {
  const { value, done } = await streamReader.read();
  if (done) break;
  streamInserts.push(c.insertArrowFromIPCStream(value, { name: "streamed" }));
}
await Promise.all(streamInserts);
// ..., from CSV files
// (interchangeable: registerFile{Text,Buffer,URL,Handle})
await db.registerFileText(`data.csv`, "1|foo\n2|bar\n");
// ... with typed insert options
await db.importCSVFromPath('data.csv', {
  schema: 'main',
  name: 'foo',
  detect: false,
  header: false,
  delimiter: '|',
  columns: {
    col1: new arrow.Int32(),
    col2: new arrow.Utf8(),
  }
});
// ..., from JSON documents in row-major format
await db.registerFileText("rows.json", `[
  { "col1": 1, "col2": "foo" },
  { "col1": 2, "col2": "bar" },
]`);
// ... or column-major format
await db.registerFileText("columns.json", `{
  "col1": [1, 2],
  "col2": ["foo", "bar"]
}`);
// ... with typed insert options
await db.importJSONFromPath('rows.json', { name: 'rows' });
await db.importJSONFromPath('columns.json', { name: 'columns' });
// ..., from Parquet files
const pickedFile: File = letUserPickFile();
await db.registerFileHandle("local.parquet", pickedFile);
await db.registerFileURL("remote.parquet", "https://origin/remote.parquet");
// ..., by specifying URLs in the SQL text
await c.query(`
  CREATE TABLE direct AS
  SELECT * FROM 'https://origin/remote.parquet'
`);
// ..., or by executing raw insert statements
await c.query(`INSERT INTO existing_table
  VALUES (1, "foo"), (2, "bar")`);
```

## How to Get Data Out? データを取得する方法

Now that we have the data loaded, DuckDB-Wasm can run queries on two different ways that differ in the result materialization. 
データがロードされたので、DuckDB-Wasmは結果のマテリアライゼーションが異なる2つの方法でクエリを実行できます。
First, the method `query` runs a query to completion and returns the results as single `arrow.Table`. 
まず、`query` メソッドはクエリを完了まで実行し、結果を単一の `arrow.Table` として返します。
Second, the method `send` fetches query results lazily through an `arrow.RecordBatchStreamReader`. 
次に、`send` メソッドは `arrow.RecordBatchStreamReader` を介してクエリ結果を遅延的に取得します。
Both methods are generic and allow for typed results in Typescript: 
両方のメソッドはジェネリックであり、Typescriptで型付きの結果を許可します。

```typescript
// Either materialize the query result
await conn.query<{v:arrow.Int32}>(`
SELECT * FROM generate_series(1, 100) t(v)
`);
// ..., or fetch the result chunks lazily
for await (const batch of await conn.send<{v:arrow.Int32}>(`
SELECT * FROM generate_series(1, 100) t(v)
`)) {
// ...
}
```


Alternatively, you can prepare statements for parameterized queries using: 
また、次のようにパラメータ化されたクエリのためのステートメントを準備できます。

```typescript
// Prepare query
const stmt = await conn.prepare<{v:arrow.Int32}>(`SELECT (v + ?) AS v FROM generate_series(0, 10000) t(v);`);
// ... and run the query with materialized results
await stmt.query(234);
// ... or result chunks
for await (const batch of await stmt.send(234)) {
// ...
}
```

## Looks like Arrow to Me 

DuckDB-Wasm uses Arrow as data protocol for the data import and all query results. 
DuckDB-Wasmは、データのインポートとすべてのクエリ結果のデータプロトコルとしてArrowを使用します。
Arrow is a database-friendly columnar format that is organized in chunks of column vectors, called record batches and that support zero-copy reads with only a small overhead. 
**Arrowは、レコードバッチと呼ばれるカラムベクトルのチャンクに整理された、データベースに優しいカラム形式**であり、わずかなオーバーヘッドでゼロコピー読み取りをサポートします。
The npm library apache-arrow implements the Arrow format in the browser and is already used by other data processing frameworks, like Arquero. 
npmライブラリのapache-arrowは、ブラウザでArrow形式を実装しており、Arqueroのような他のデータ処理フレームワークでもすでに使用されています。
Arrow therefore not only spares us the implementation of the SQL type logic in JavaScript, it also makes us compatible to existing tools. 
したがって、ArrowはJavaScriptでのSQL型ロジックの実装を省くだけでなく、既存のツールとの互換性も提供します。

Why not use plain Javascript objects? 
なぜプレーンなJavaScriptオブジェクトを使用しないのでしょうか？

WebAssembly is isolated and memory-safe. 
WebAssemblyは隔離されており、メモリ安全です。
This isolation is part of its DNA and drives fundamental design decisions in DuckDB-Wasm. 
この隔離はそのDNAの一部であり、DuckDB-Wasmの基本的な設計決定を促進します。
For example, WebAssembly introduces a barrier towards the traditional JavaScript heap. 
例えば、WebAssemblyは従来のJavaScriptヒープに対する障壁を導入します。
Crossing this barrier is difficult as JavaScript has to deal with native function calls, memory ownership and serialization performance. 
この障壁を越えることは難しく、JavaScriptはネイティブ関数呼び出し、メモリ所有権、およびシリアル化性能に対処しなければなりません。
Languages like C++ make this worse as they rely on smart pointers that are not available through the FFI. 
C++のような言語は、FFIを通じて利用できないスマートポインタに依存しているため、これをさらに悪化させます。
They leave us with the choice to either pass memory ownership to static singletons within the WebAssembly instance or maintain the memory through C-style APIs in JavaScript, a language that is too dynamic for sound implementations of the RAII idiom. 
これにより、WebAssemblyインスタンス内の静的シングルトンにメモリ所有権を渡すか、RAIIイディオムの健全な実装にはあまりにも動的なJavaScriptのCスタイルAPIを通じてメモリを維持するかの選択を迫られます。
The memory-isolation forces us to serialize data before we can pass it to the WebAssembly instance. 
メモリの隔離により、WebAssemblyインスタンスにデータを渡す前にシリアル化する必要があります。
Browsers can serialize JavaScript objects natively to and from JSON using the functions JSON.stringify and JSON.parse but this is slower compared to, for example, copying raw native arrays. 
ブラウザは、関数JSON.stringifyおよびJSON.parseを使用してJavaScriptオブジェクトをネイティブにJSONにシリアル化できますが、これは例えば生のネイティブ配列をコピーするのに比べて遅くなります。

<!-- ここまで読んだ! -->

## Web Filesystem ウェブファイルシステム

DuckDB-Wasm integrates a dedicated filesystem for WebAssembly. 
**DuckDB-Wasmは、WebAssembly用の専用ファイルシステムを統合**しています。
DuckDB itself is built on top of a virtual filesystem that decouples higher level tasks, such as reading a Parquet file, from low-level filesystem APIs that are specific to the operating system. 
**DuckDB自体は、Parquetファイルを読み取るといった高レベルのタスクを、オペレーティングシステムに特有の低レベルのファイルシステムAPIから切り離す仮想ファイルシステムの上に構築**されています。
We leverage this abstraction in DuckDB-Wasm to tailor filesystem implementations to the different WebAssembly environments. 
私たちは、この抽象化をDuckDB-Wasmで活用し、異なるWebAssembly環境に合わせたファイルシステムの実装を調整します。

The following figure shows our current web filesystem in action. 
以下の図は、現在のウェブファイルシステムの動作を示しています。
The sequence diagram presents a user running a SQL query that scans a single Parquet file. 
シーケンス図は、ユーザが単一のParquetファイルをスキャンするSQLクエリを実行している様子を示しています。
The query is first offloaded to a dedicated web worker through a JavaScript API. 
クエリは最初に、JavaScript APIを介して専用のウェブワーカーにオフロードされます。
There, it is passed to the WebAssembly module that processes the query until the execution hits the parquet_scantable function. 
そこで、クエリを処理するWebAssemblyモジュールに渡され、実行がparquet_scantable関数に達するまで処理されます。
This table function then reads the file using a buffered filesystem which, in turn, issues paged reads on the web filesystem. 
このテーブル関数は、バッファ付きファイルシステムを使用してファイルを読み取り、その結果、ウェブファイルシステムでページ読み取りを発行します。
This web filesystem then uses an environment-specific runtime to read the file from several possible locations. 
このウェブファイルシステムは、環境特有のランタイムを使用して、いくつかの可能な場所からファイルを読み取ります。

![]()

Depending on the context, the Parquet file may either reside on the local device, on a remote server or in a buffer that was registered by the user upfront. 
コンテキストに応じて、Parquetファイルはローカルデバイス上、リモートサーバ上、またはユーザによって事前に登録されたバッファ内に存在する場合があります。
We deliberately treat all three cases equally to unify the retrieval and processing of external data. 
私たちは、外部データの取得と処理を統一するために、これらの3つのケースを意図的に平等に扱います。
This does not only simplify the analysis, it also enables more advanced features like partially consuming structured file formats. 
これにより、分析が簡素化されるだけでなく、構造化ファイル形式を部分的に消費するようなより高度な機能も可能になります。
Parquet files, for example, consist of multiple row groups that store data in a column-major fashion. 
例えば、Parquetファイルは、データを列優先方式で格納する複数の行グループで構成されています。
As a result, we may not need to download the entire file for a query but only required bytes. 
その結果、クエリのためにファイル全体をダウンロードする必要はなく、必要なバイトのみをダウンロードすればよい場合があります。

A query like SELECT count(*) FROM parquet_scan(...), for example, can be evaluated on the file metadata alone and will finish in milliseconds even on remote files that are several terabytes large. 
例えば、**SELECT count(*) FROM parquet_scan(...)のようなクエリは、ファイルメタデータのみに基づいて評価でき、数テラバイトのリモートファイルでもミリ秒で完了**します。
Another more general example are paging scans with LIMIT and OFFSET qualifiers such as SELECT * FROM parquet_scan(...) LIMIT 20 OFFSET 40, or queries with selective filter predicates where entire row groups can be skipped based on metadata statistics. 
もう一つの一般的な例は、LIMITおよびOFFSET修飾子を持つページングスキャンで、SELECT * FROM parquet_scan(...) LIMIT 20 OFFSET 40のようなクエリや、メタデータ統計に基づいて全行グループをスキップできる選択的フィルタ述語を持つクエリです。
These partial file reads are no groundbreaking novelty and could be implemented in JavaScript today, but with DuckDB-Wasm, these optimizations are now driven by the semantics of SQL queries instead of fine-tuned application logic. 
これらの部分的なファイル読み取りは画期的な新しさではなく、今日のJavaScriptで実装可能ですが、DuckDB-Wasmでは、これらの最適化は微調整されたアプリケーションロジックではなく、SQLクエリの意味論によって駆動されるようになりました。

Note: The common denominator among the available File APIs is unfortunately not large. 
注意: 利用可能なファイルAPIの共通の基準は残念ながら大きくありません。
This limits the features that we can provide in the browser. 
これにより、ブラウザで提供できる機能が制限されます。
For example, local persistency of DuckDB databases would be a feature with significant impact but requires a way to either read and write synchronously into user-provided files or IndexedDB. 
例えば、DuckDBデータベースのローカル永続性は、重要な影響を持つ機能ですが、ユーザ提供のファイルまたはIndexedDBに対して同期的に読み書きする方法が必要です。
We might be able to bypass these limitations in the future but this is subject of ongoing research. 
将来的にはこれらの制限を回避できるかもしれませんが、これは現在進行中の研究の対象です。

<!-- ここまで読んだ! -->

## Advanced Features 高度な機能

WebAssembly 1.0 has landed in all major browsers. 
WebAssembly 1.0はすべての主要ブラウザに登場しました。
The WebAssembly Community Group fixed the design of this first version back in November 2017, which is now referred to as WebAssembly MVP. 
WebAssemblyコミュニティグループは、この最初のバージョンの設計を2017年11月に確定し、現在はWebAssembly MVPと呼ばれています。
Since then, the development has been ongoing with eight additional features that have been added to the standard and at least five proposals that are currently in progress. 
それ以来、開発は進行中で、標準に追加された8つの機能と、現在進行中の少なくとも5つの提案があります。

The rapid pace of this development presents challenges and opportunities for library authors. 
この開発の急速な進展は、ライブラリ作成者にとって課題と機会をもたらします。
On the one hand, the different features find their way into the browsers at different speeds which leads to a fractured space of post-MVP functionality. 
一方で、異なる機能が異なる速度でブラウザに導入されるため、ポストMVP機能の断片化された空間が生じます。
On the other hand, features can bring flat performance improvements and are therefore indispensable when aiming for a maximum performance. 
他方で、機能は平坦なパフォーマンスの向上をもたらすことができるため、最大のパフォーマンスを目指す際には不可欠です。

The most promising feature for DuckDB-Wasm is exception handling which is already enabled by default in Chrome 95. 
DuckDB-Wasmにとって最も有望な機能は、Chrome 95でデフォルトで有効になっている例外処理です。
DuckDB and DuckDB-Wasm are written in C++ and use exceptions for faulty situations. 
**DuckDBとDuckDB-WasmはC++で書かれており**、障害のある状況に対して例外を使用します。
DuckDB does not use exceptions for general control flow but to automatically propagate errors upwards to the top-level plan driver. 
DuckDBは一般的な制御フローに対して例外を使用せず、エラーを自動的に上位のプランドライバに伝播させるために使用します。
In native environments, these exceptions are implemented as "zero-cost exceptions" as they induce no overhead until they are thrown. 
ネイティブ環境では、これらの例外は「ゼロコスト例外」として実装されており、投げられるまでオーバーヘッドを引き起こしません。
With the WebAssembly MVP, however, that is no longer possible as the compiler toolchain Emscripten has to emulate exceptions through JavaScript. 
しかし、WebAssembly MVPでは、コンパイラツールチェーンEmscriptenがJavaScriptを通じて例外をエミュレートしなければならないため、それはもはや不可能です。
Without WebAssembly exceptions, DuckDB-Wasm calls throwing functions through a JavaScript hook that can catch exceptions emulated through JavaScript aborts. 
WebAssemblyの例外がない場合、DuckDB-WasmはJavaScriptのフックを介して投げる関数を呼び出し、JavaScriptでエミュレートされた例外をキャッチします。
An example for these hook calls is shown in the following figure. 
これらのフック呼び出しの例は、以下の図に示されています。
Both stack traces originate from a single paged read of a Parquet file in DuckDB-Wasm. 
両方のスタックトレースは、DuckDB-WasmでのParquetファイルの単一ページ読み取りから発生しています。
The left side shows a stack trace with the WebAssembly MVP and requires multiple calls through the functions wasm-to-js-i*. 
左側はWebAssembly MVPのスタックトレースを示しており、関数wasm-to-js-i*を介して複数の呼び出しが必要です。
The right stack trace uses WebAssembly exceptions without any hook calls. 
右側のスタックトレースは、フック呼び出しなしでWebAssemblyの例外を使用しています。

![]()

This fractured feature space is a temporary challenge that will be resolved once high-impact features like exception handling, SIMD and bulk-memory operations are available everywhere. 
この断片化された機能空間は、一時的な課題であり、例外処理、SIMD、バルクメモリ操作などの高影響機能がどこでも利用可能になると解決されます。
In the meantime, we will ship multiple WebAssembly modules that are compiled for different feature sets and adaptively pick the best bundle for you using dynamic browser checks. 
その間、異なる機能セット用にコンパイルされた複数のWebAssemblyモジュールを提供し、動的ブラウザチェックを使用して最適なバンドルを適応的に選択します。
The following example shows how the asynchronous version of DuckDB-Wasm can be instantiated using either manual or JsDelivr bundles: 
以下の例は、DuckDB-Wasmの非同期バージョンを手動またはJsDelivrバンドルを使用してどのようにインスタンス化できるかを示しています：

```javascript
// Import the ESM bundle (supports tree-shaking)
import * as duckdb from '@duckdb/duckdb-wasm/dist/duckdb-esm.js';

// Either bundle them manually, for example as Webpack assets
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb.wasm';
import duckdb_wasm_next from '@duckdb/duckdb-wasm/dist/duckdb-next.wasm';
import duckdb_wasm_next_coi from '@duckdb/duckdb-wasm/dist/duckdb-next-coi.wasm';

const WEBPACK_BUNDLES: duckdb.DuckDBBundles = {
    asyncDefault: {
        mainModule: duckdb_wasm,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-async.worker.js', import.meta.url).toString(),
    },
    asyncNext: {
        mainModule: duckdb_wasm_next,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-async-next.worker.js', import.meta.url).toString(),
    },
    asyncNextCOI: {
        mainModule: duckdb_wasm_next_coi,
        mainWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-async-next-coi.worker.js', import.meta.url).toString(),
        pthreadWorker: new URL('@duckdb/duckdb-wasm/dist/duckdb-browser-async-next-coi.pthread.worker.js', import.meta.url).toString(),
    },
};

// ..., or load the bundles from jsdelivr
const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();

// Select a bundle based on browser checks
const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);

// Instantiate the asynchronus version of DuckDB-Wasm
const worker = new Worker(bundle.mainWorker!);
const logger = new duckdb.ConsoleLogger();
const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainstreModule, bundle.pthreadWorker);
```

You can also test the features and selected bundle in your browser using the web shell command features. 
ブラウザでweb shellコマンドfeaturesを使用して、機能と選択したバンドルをテストすることもできます。

<!-- ここまで読んだ! --> 

## Multithreading マルチスレッド

In 2018, the Spectre and Meltdown vulnerabilities sent crippling shockwaves through the internet. 
2018年、SpectreおよびMeltdownの脆弱性はインターネットに壊滅的な衝撃を与えました。 
Today, we are facing the repercussions of these events, in particular in software that runs arbitrary user code – such as web browsers. 
今日、私たちはこれらの出来事の影響に直面しており、特に任意のユーザーコードを実行するソフトウェア、つまりウェブブラウザにおいてです。 
Shortly after the publications, all major browser vendors restricted the use of SharedArrayBuffers to prevent dangerous timing attacks. 
発表の直後、すべての主要なブラウザベンダーは危険なタイミング攻撃を防ぐためにSharedArrayBuffersの使用を制限しました。 
SharedArrayBuffers are raw buffers that can be shared among web workers for global state and an alternative to the browser-specific message passing. 
SharedArrayBuffersは、グローバルステートのためにウェブワーカー間で共有できる生のバッファであり、ブラウザ固有のメッセージパッシングの代替手段です。 
These restrictions had detrimental effects on WebAssembly modules since SharedArrayBuffers are necessary for the implementation of POSIX threads in WebAssembly. 
これらの制限は、SharedArrayBuffersがWebAssemblyにおけるPOSIXスレッドの実装に必要であるため、WebAssemblyモジュールに悪影響を及ぼしました。 
Without SharedArrayBuffers, WebAssembly modules can run in a dedicated web worker to unblock the main event loop but won't be able to spawn additional workers for parallel computations within the same instance. 
SharedArrayBuffersがない場合、WebAssemblyモジュールは専用のウェブワーカーで実行してメインイベントループをブロック解除できますが、同じインスタンス内で並列計算のために追加のワーカーを生成することはできません。 
By default, we therefore cannot unleash the parallel query execution of DuckDB in the web. 
したがって、デフォルトでは、ウェブ上でDuckDBの並列クエリ実行を解放することはできません。 
However, browser vendors have recently started to reenable SharedArrayBuffers for websites that are cross-origin-isolated. 
しかし、ブラウザベンダーは最近、クロスオリジンアイソレートされたウェブサイトのためにSharedArrayBuffersの再有効化を開始しました。 
A website is cross-origin-isolated if it ships the main document with the following HTTP headers: 
ウェブサイトがクロスオリジンアイソレートされている場合、次のHTTPヘッダーを持つメインドキュメントを配信します： 

```
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
```

These headers will instruct browsers to A) isolate the top-level document from other top-level documents outside its own origin and B) prevent the document from making arbitrary cross-origin requests unless the requested resource explicitly opts in. 
これらのヘッダーは、ブラウザに対してA) トップレベルドキュメントを自分のオリジン外の他のトップレベルドキュメントから隔離し、B) 要求されたリソースが明示的にオプトインしない限り、ドキュメントが任意のクロスオリジンリクエストを行うのを防ぐよう指示します。 
Both restrictions have far reaching implications for a website since many third-party data sources won't yet provide the headers today and the top-level isolation currently hinders the communication with, for example, OAuth pop up's (there are plans to lift that). 
これらの制限は、今日多くのサードパーティデータソースがまだヘッダーを提供していないため、ウェブサイトに広範な影響を及ぼします。また、トップレベルの隔離は、例えばOAuthポップアップとの通信を妨げています（これを解除する計画があります）。 
We therefore assume that DuckDB-Wasm will find the majority of users on non-isolated websites. 
したがって、DuckDB-Wasmは非隔離ウェブサイトの大多数のユーザーを見つけると考えています。 
We are, however, experimenting with dedicated bundles for isolated sites using the suffix-next-coi) and will closely monitor the future need of our users. 
ただし、私たちはsuffix-next-coiを使用して隔離されたサイト向けの専用バンドルを実験しており、ユーザーの将来のニーズを注意深く監視します。



## Web Shell

We further host a web shell powered by DuckDB-Wasm alongside the library release atshell.duckdb.org.
私たちは、ライブラリリリースatshell.duckdb.orgに加えて、DuckDB-Wasmを利用したウェブシェルをホストしています。

Use the following shell commands to query remote TPC-H files at scale factor 0.01.
以下のシェルコマンドを使用して、スケールファクター0.01のリモートTPC-Hファイルをクエリします。

When querying your own, make sure to properly set CORS headers since your browser will otherwise block these requests.
自分のファイルをクエリする際は、CORSヘッダーを適切に設定してください。さもなければ、ブラウザがこれらのリクエストをブロックします。

You can alternatively use the .files command to register files from the local filesystem.
代わりに、.filesコマンドを使用してローカルファイルシステムからファイルを登録することもできます。

```
.timer on SELECT count(*) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/lineitem.parquet'; SELECT count(*) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/customer.parquet'; SELECT avg(c_acctbal) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/customer.parquet'; SELECT * FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/orders.parquet' LIMIT 10; SELECT n_name, avg(c_acctbal) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/customer.parquet', 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/nation.parquet' WHERE c_nationkey = n_nationkey GROUP BY n_name; SELECT * FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/region.parquet', 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/nation.parquet' WHERE r_regionkey = n_regionkey;
```
.timer on
SELECT count(*) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/lineitem.parquet';
SELECT count(*) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/customer.parquet';
SELECT avg(c_acctbal) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/customer.parquet';
SELECT * FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/orders.parquet' LIMIT 10;
SELECT n_name, avg(c_acctbal) FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/customer.parquet', 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/nation.parquet' WHERE c_nationkey = n_nationkey GROUP BY n_name;
SELECT * FROM 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/region.parquet', 'https://blobs.duckdb.org/data/tpch-sf0.01-parquet/nation.parquet' WHERE r_regionkey = n_regionkey;



## Evaluation 評価

The following table teases the execution times of some TPC-H queries at scale factor 0.5 using the libraries DuckDB-Wasm, sql.js, Arquero and Lovefield. 
以下の表は、ライブラリDuckDB-Wasm、sql.js、Arquero、Lovefieldを使用したスケールファクター0.5でのいくつかのTPC-Hクエリの実行時間を示しています。
You can find a more in-depth discussion with all TPC-H queries, additional scale factors and microbenchmarks on the “DuckDB-Wasm versus X” page.
より詳細な議論は、すべてのTPC-Hクエリ、追加のスケールファクター、およびマイクロベンチマークについて「DuckDB-Wasm versus X」ページで見つけることができます。



## Future Research 将来の研究

We believe that WebAssembly unveils hitherto dormant potential for shared query processing between clients and servers. 
私たちは、WebAssemblyがクライアントとサーバー間の共有クエリ処理のためのこれまで眠っていた潜在能力を明らかにすると信じています。
Pushing computation closer to the client can eliminate costly round-trips to the server and thus increase interactivity and scalability of in-browser analytics. 
計算をクライアントに近づけることで、サーバーへの高コストな往復を排除し、ブラウザ内分析のインタラクティビティとスケーラビリティを向上させることができます。
We further believe that the release of DuckDB-Wasm could be the first step towards a more universal data plane spanning across multiple layers including traditional database servers, clients, CDN workers and computational storage. 
さらに、DuckDB-Wasmのリリースが、従来のデータベースサーバー、クライアント、CDNワーカー、計算ストレージを含む複数のレイヤーにまたがるより普遍的なデータプレーンへの第一歩になると信じています。
As an in-process analytical database, DuckDB might be the ideal driver for distributed query plans that increase the scalability and interactivity of SQL databases at low costs. 
プロセス内分析データベースとして、DuckDBは低コストでSQLデータベースのスケーラビリティとインタラクティビティを向上させる分散クエリプランの理想的なドライバーかもしれません。

##### In this article この記事の内容
- Efficient Analytics in the Browser ブラウザ内の効率的な分析
- How to Get Data In? データの取り込み方法
- How to Get Data Out? データの取り出し方法
- Looks like Arrow to Me 私にはArrowのように見える
- Web Filesystem ウェブファイルシステム
- Advanced Features 高度な機能
- Multithreading マルチスレッド
- Web Shell ウェブシェル
- Evaluation 評価
- Future Research 将来の研究



# Recent Posts 最近の投稿

using DuckDB
DuckDBを使用しています



### Discovering DuckDB Use Cases via GitHub DuckDBの使用事例の発見

using DuckDB DuckDBを使用して



### Lightweight Text Analytics Workflows with DuckDB
### DuckDBを用いた軽量テキスト分析ワークフロー
