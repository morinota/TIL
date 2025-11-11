## refs 審判

- <https://duckdb.org/2024/05/03/vector-similarity-search-vss.html> <https://duckdb.org/2024/05/03/vector-similarity-search-vss.html>

# Vector Similarity Search in DuckDB DuckDBにおけるベクトル類似度検索

TL;DR: This blog post shows a preview of DuckDB's new vss extension, which introduces support for HNSW (Hierarchical Navigable Small Worlds) indexes to accelerate vector similarity search.
TL;DR： このブログポストでは、DuckDBの新しいvss拡張機能のプレビューを紹介します。この拡張機能は、ベクトル類似性検索を高速化するHNSW（Hierarchical Navigable Small Worlds）インデックスのサポートを導入するものです。

In DuckDB v0.10.0, we introduced the ARRAY data type, which stores fixed-sized lists, to complement the existing variable-size LIST data type.
DuckDB v0.10.0では、**既存の可変サイズのLISTデータ型を補完するために、固定サイズのリストを格納するARRAYデータ型を導入**しました。(あ、当たり前かもだけど固定長なのか。サイズの異なる埋め込み表現を一つのカラムで保存することはできない...!:thinking:)

The initial motivation for adding this data type was to provide optimized operations for lists that can utilize the positional semantics of their child elements and avoid branching as all lists have the same length.
このデータ型を追加した最初の動機は、子要素の位置セマンティクスを利用し、すべてのリストが同じ長さであるため分岐を避けることができる、リストに対して最適化された操作を提供することだった。
Think e.g., the sort of array manipulations you'd do in NumPy: stacking, shifting, multiplying – you name it.
例えば、NumPyで行うような配列操作を考えてみよう： 積み重ね、シフト、乗算、何でもできます。
Additionally, we wanted to improve our interoperability with Apache Arrow, as previously Arrow's fixed-size list types would be converted to regular variable-size lists when ingested into DuckDB, losing some type information.
さらに、Apache Arrowとの相互運用性を向上させたかった。以前は、Arrowの固定サイズ・リスト型は、DuckDBに取り込まれる際に通常の可変サイズ・リストに変換され、いくつかの型情報が失われていたからだ。

However, as the hype for vector embeddings and semantic similarity search was growing, we also snuck in a couple of distance metric functions for this new ARRAY type: array_distance, array_inner_product and array_cosine_similarity
しかし、ベクトル埋め込みと意味的類似性検索の宣伝が高まるにつれて、我々はこの新しいARRAY型のための距離測定関数をいくつか忍び込ませた： array_distance、 array_inner_product、 array_cosine_similarity です。

Note
注

If you're one of today's lucky 10,000 and haven't heard of word embeddings or vector search, the short version is that it's a technique used to represent documents, images, entities – data as high-dimensional vectors and then search for similar vectors in a vector space, using some sort of mathematical "distance" expression to measure similarity.
もしあなたが今日の幸運な10,000人のうちの一人で、単語埋め込みやベクトル検索を聞いたことがないのなら、簡単に説明すると、文書、画像、エンティティなどのデータを高次元ベクトルとして表現し、**ある種の数学的な「距離」表現を使って類似性を測定するために、ベクトル空間内で類似したベクトルを検索するために使われるテクニック**だ。
This is used in a wide range of applications, from natural language processing to recommendation systems and image recognition, and has recently seen a surge in popularity due to the advent of generative AI and availability of pre-trained models.
これは、自然言語処理から推薦システムや画像認識まで、幅広いアプリケーションで使用されており、最近では、ジェネレーティブAIの登場と、事前に訓練されたモデルの利用可能性により、人気が急上昇している。

This got the community really excited! While we (DuckDB Labs) initially went on record saying that we would not be adding a vector similarity search index to DuckDB as we deemed it to be too far out of scope, we were very interested in supporting custom indexes through extensions in general.
コミュニティは大いに盛り上がりました！私たち（DuckDB Labs）は当初、**DuckDBにベクトル類似検索インデックスを追加することは範囲外であると判断し、追加しないと公言していました**が、一般的な拡張機能によるカスタムインデックスのサポートには非常に興味がありました。
Shoot, I've been personally nagging on about wanting to plug-in an "R-Tree" index since the inception of DuckDBs spatial extension! So when one of our client projects evolved into creating a proof-of-concept custom "HNSW" index extension, we said that we'd give it a shot.
DuckDBの空間拡張が始まったときから、個人的に 「R-Tree」インデックスをプラグインしたいとずっと思っていました！だから、あるクライアント・プロジェクトが、概念実証のためのカスタム 「HNSW 」インデックス拡張を作成することに発展したとき、私たちはそれを試してみようと言いました。
And… well, one thing led to another.
そして...まあ、あることがきっかけで別のことが始まった。

Fast forward to now and we're happy to announce the availability of the vss vector similarity search extension for DuckDB! While some may say we're late to the vector search party, we'd like to think the party is just getting started!
早速ですが、DuckDBにvssベクトル類似検索エクステンションが登場しました！ベクトル検索パーティに遅れたと言われるかもしれませんが、パーティは始まったばかりです！

Alright, so what's in vss?
さて、ではvssには何があるのか？

## The Vector Similarity Search (VSS) Extension ベクトル類似探索(VSS)拡張

On the surface, vss seems like a comparatively small DuckDB extension.
表面的には、vssは比較的小さなDuckDBの拡張機能のように見える。
It does not provide any new data types, scalar functions or copy functions, but rather a single new index type: HNSW (Hierarchical Navigable Small Worlds), which is a graph-based index structure that is particularly well-suited for high-dimensional vector similarity search.
HNSWは新しいデータ型、スカラー関数、コピー関数を提供しない： HNSW (Hierarchical Navigable Small Worlds)はグラフベースのインデックス構造で、特に高次元のベクトル類似性検索に適している。

```sql
-- Create a table with an array column
CREATE TABLE embeddings (vec FLOAT[3]);

-- Create an HNSW index on the column
CREATE INDEX idx ON embeddings USING HNSW (vec);
```

This index type can't be used to enforce constraints or uniqueness like the built-in ART index, and can't be used to speed up joins or index regular columns either.
このインデックス・タイプは、組み込みのARTインデックスのように制約や一意性を強制するために使用することはできず、結合の高速化や通常のカラムのインデックスにも使用できません。
Instead, the HNSW index is only applicable to columns of the ARRAY type containing FLOAT elements and will only be used to accelerate queries calculating the "distance" between a constant FLOAT ARRAY and the FLOAT ARRAY's in the indexed column, ordered by the resulting distance and returning the top-n results.
その代わりに、**HNSWインデックスはFLOAT要素を含むARRAY型のカラムにのみ適用され、一定のFLOAT ARRAYとインデックスされたカラムのFLOAT ARRAYの間の「距離」を計算するクエリを高速化するためにのみ使用されます**。
That is, queries of the form:
つまり、以下のような形式のクエリである：

```sql
SELECT *
FROM embeddings
ORDER BY array_distance(vec, [1, 2, 3]::FLOAT[3])
LIMIT 3;
```

will have their logical plan optimized to become a projection over a new HNSW index scan operator, removing the limit and sort altogether.
これらのクエリは、論理プランが最適化され、新しいHNSWインデックススキャン演算子に対するプロジェクションになり、LIMITとSORTが完全に削除されます。
We can verify this by checking the EXPLAIN output:
EXPLAINの出力をチェックすることで、これを確認することができる：

You can pass the HNSW index creation statement a metric parameter to decide what kind of distance metric to use.
**HNSWインデックス作成文にメトリックパラメータを渡して、どのような距離メトリックを使うかを決めることができる**。
The supported metrics are l2sq, cosine and inner_product, matching the three built-in distance functions: array_distance, array_cosine_similarity and array_inner_product.
サポートされるメトリクスは l2sq、cosine、 inner_product で、3つの組み込み距離関数に対応しています： array_distance、 array_cosine_similarity、 array_inner_product の3つの組み込み距離関数と一致します。
The default is l2sq, which uses Euclidean distance (array_distance):
デフォルトはl2sqで、ユークリッド距離（array_distance）を使用する：

```sql
CREATE INDEX l2sq_idx ON embeddings USING HNSW (vec)
WITH (metric = 'l2sq');
```

To use cosine distance (array_cosine_similarity):
余弦距離（array_cosine_similarity）を使う：

```sql
CREATE INDEX cos_idx ON embeddings USING HNSW (vec)
WITH (metric = 'cosine');
```

To use inner product (array_inner_product):
内積 (array_inner_product) を使用する：

```sql
CREATE INDEX ip_idx ON embeddings USING HNSW (vec)
WITH (metric = 'ip');
```

## Implementation インプリメンテーション

The vss extension is based on the usearch library, which provides a flexible C++ implementation of the HNSW index data structure boasting very impressive performance benchmarks.
vss拡張はusearchライブラリに基づいており、非常に優れた性能ベンチマークを誇るHNSWインデックスデータ構造の柔軟なC++実装を提供する。
While we currently only use a subset of all the functionality and tuning options provided by usearch, we're excited to explore how we can leverage more of its features in the future.
現在、私たちはusearchが提供するすべての機能とチューニングオプションのサブセットしか使用していませんが、将来的にはより多くの機能を活用する方法を模索していきたいと思っています。
So far we're mostly happy that it aligns so nicely with DuckDB's development ethos.
今のところ、DuckDBの開発理念とうまく合致しているので、ほとんど満足しています。
Much like DuckDB itself, usearch is written in portable C++11 with no external dependencies and released under a permissive license, making it super smooth to integrate into our extension build and distribution pipeline.
DuckDBそのものと同様、usearchはポータブルなC++11で書かれており、外部依存はなく、寛容なライセンスでリリースされている。

## Limitations 制限事項

The big limitation as of now is that the HNSW index can only be created in in-memory databases, unless the SET hnsw_enable_experimental_persistence = ⟨bool⟩ configuration parameter is set to true.
現時点での大きな制限は、`SET hnsw_enable_experimental_persistence = ⟨bool⟩`のconfigパラメータがtrueに設定されている場合を除いて、HNSWインデックスはインメモリデータベースでのみ作成できるということです。
If this parameter is not set, any attempt to create an HNSW index in a disk-backed database will result in an error message, but if the parameter is set, the index will not only be created in memory, but also persisted to disk as part of the DuckDB database file during checkpointing.
このパラメータが設定されていない場合、ディスクバックアップデータベースにHNSWインデックスを作成しようとするとエラーメッセージが表示されます。しかし、このパラメータが設定されている場合、インデックスはメモリ上に作成されるだけでなく、チェックポイント時にDuckDBデータベースファイルの一部としてディスクに永続化されます。
After restarting or loading a database file with a persisted HNSW index, the index will be lazily loaded back into memory whenever the associated table is first accessed, which is significantly faster than having to re-create the index from scratch.
永続化されたHNSWインデックスを持つデータベースファイルを再起動またはロードした後、関連するテーブルに最初にアクセスするたびに、インデックスはメモリに遅延ロードされます。

The reasoning for locking this feature behind an experimental flag is that we still have some known issues related to persistence of custom indexes that we want to address before enabling it by default.
この機能を実験的フラグにロックする理由は、カスタムインデックスの永続性に関する既知の問題がまだ残っており、デフォルトで有効にする前に対処したいからです。
In particular, WAL recovery is not yet properly implemented for custom indexes, meaning that if a crash occurs or the database is shut down unexpectedly while there are uncommited changes to a HNSW-indexed table, you can end up with data loss or corruption of the index.
特に、WALリカバリはカスタムインデックスに対してまだ適切に実装されていないため、HNSWでインデックスされたテーブルにコミットされていない変更がある間にクラッシュが発生したり、データベースが予期せずシャットダウンされたりすると、データが失われたり、インデックスが破損したりする可能性があります。
While it is technically possible to recover from a unexpected shutdown manually by first starting DuckDB separately, loading the vss extension and then ATTACHing the database file, which ensures that the HNSW index functionality is available during WAL-playback, you should not rely on this for production workloads.
技術的には、まずDuckDBを個別に起動し、vss拡張をロードし、データベースファイルをアタッチすることで、予期せぬシャットダウンから手動で回復することは可能ですが、WAL再生中にHNSWインデックス機能が利用可能であることを保証します。

We're actively working on addressing this and other issues related to index persistence, which will hopefully make it into DuckDB v0.10.3, but for now we recommend using the HNSW index in in-memory databases only.
この問題やインデックスの永続性に関するその他の問題については、DuckDB v0.10.3に反映させるべく積極的に取り組んでいますが、**現時点ではインメモリデータベースでのみHNSWインデックスを使用することをお勧めします**。

At runtime however, much like the ART the HNSW index must be able to fit into RAM in its entirety, and the memory allocated by the HNSW at runtime is allocated "outside" of the DuckDB memory management system, meaning that it wont respect DuckDB's memory_limit configuration parameter.
実行時にHNSWが割り当てるメモリは、DuckDBのメモリ管理システムの「外部」で割り当てられるため、DuckDBのmemory_limit設定パラメータは無視されます。

Another current limitation with the HNSW index so far are that it only supports the FLOAT (a 32-bit, single-precision floating point) type for the array elements and only distance metrics corresponding to the three built in distance functions, array_distance, array_inner_product and array_cosine_similarity.
HNSW インデックスの現在のもう一つの限界は、**配列要素に FLOAT（32ビットの単精度浮動小数点）型しかサポートしていない**ことと、組み込みの3つの距離関数、array_distance、array_inner_product、array_cosine_similarity に対応する距離メトリクスしかサポートしていないことである。
But this is also something we're looking to expand upon in the near future as it is much less of a technical limitation and more of a "we haven't gotten around to it yet" limitation.
**しかし、これは技術的な制限というより、「まだ手をつけていない」という制限なので、近い将来、拡張したい**と考えています。

## Conclusion 結論

The vss extension for DuckDB is a new extension that adds support for creating HNSW indexes on fixed-size list columns in DuckDB, accelerating vector similarity search queries.
DuckDBのvss拡張は、DuckDBの固定サイズのリストカラムにHNSWインデックスを作成するサポートを追加し、ベクトル類似検索クエリを高速化する新しい拡張です。
The extension can currently be installed on DuckDB v0.10.2 on all supported platforms (including WASM!) by running INSTALL vss; LOAD vss.
この拡張機能は現在、DuckDB v0.10.2、すべてのサポート対象プラットフォーム（WASMを含む！）で、INSTALL vss; LOAD vssを実行することでインストールできます。
The vss extension treads new ground for DuckDB extensions by providing a custom index type and we're excited to refine and expand on this functionality going forward.
vssエクステンションは、カスタムインデックスタイプを提供することで、DuckDBエクステンションの新たな地平を切り開きました。

While we're still working on addressing some of the limitations above, particularly those related to persistence (and performance), we still really want to share this early version the vss extension as we believe this will open up a lot of cool opportunities for the community.
上記の制限事項、特に永続性（とパフォーマンス）に関する制限事項のいくつかにまだ対処している最中ではあるが、vssエクステンションのこの初期バージョンを共有することで、コミュニティにとって多くの素晴らしい機会が開かれると信じている。
So make sure to check out the vss extension documentation for more information on how to work with this extension!
そのため、この拡張機能を使用する方法については、必ずvss拡張機能のドキュメントをチェックしてほしい！

This work was made possible by the sponsorship of a DuckDB Labs customer! If you are interested in similar work for specific capabilities, please reach out to DuckDB Labs.
この作業はDuckDB Labsのお客様のスポンサーシップにより実現しました！DuckDB Labsのお客様からのご協賛により実現したものです。
Alternatively, we're happy to welcome contributors! Please reach out to the DuckDB Labs team over on Discord or on the vss extension GitHub repository to keep up with the latest developments.
また、コントリビューターの方も大歓迎です！Discordまたはvss拡張機能のGitHubリポジトリでDuckDB Labsチームにご連絡ください。

<!-- ここまで読んだ! -->
