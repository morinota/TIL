refs: https://aws.amazon.com/jp/blogs/aws/new-improve-apache-iceberg-query-performance-in-amazon-s3-with-sort-and-z-order-compaction/?utm_source=chatgpt.com

# New: Improve Apache Iceberg query performance in Amazon S3 with sort and z-order compaction
新しい機能: ソートとZオーダー圧縮を使用してAmazon S3におけるApache Icebergのクエリ性能を向上

by Sébastien Stormacq  
著者: セバスチャン・ストルマク  
on 24 JUN 2025  
2025年6月24日  

in Amazon S3 Tables, Amazon Simple Storage Service (S3), Announcements, AWS Glue, Launch, News  
Amazon S3テーブル、Amazon Simple Storage Service (S3)、お知らせ、AWS Glue、発表、ニュース  

<!-- ここまで読んだ! -->

You can now use sort and z-order compaction to improve Apache Iceberg query performance in Amazon S3 Tables and general purpose S3 buckets.  
**Amazon S3テーブルと一般的なS3バケットで、ソートとZオーダー圧縮を使用してApache Icebergのクエリ性能を向上させることができます。**

You typically use Iceberg to manage large-scale analytical datasets in Amazon Simple Storage Service (Amazon S3) with AWS Glue Data Catalog or with S3 Tables.  
通常、Icebergは、AWS Glue Data CatalogまたはS3テーブルを使用して、Amazon Simple Storage Service (Amazon S3)内の大規模な分析データセットを管理するために使用されます。  
Iceberg tables support use cases such as concurrent streaming and batch ingestion, schema evolution, and time travel.  
Icebergテーブルは、同時ストリーミングやバッチ取り込み、スキーマの進化、タイムトラベルなどのユースケースをサポートしています。  
When working with high-ingest or frequently updated datasets, data lakes can accumulate many small files that impact the cost and performance of your queries.  
高い取り込みや頻繁に更新されるデータセットを扱う際、データレイクは多くの小さなファイルを蓄積し、クエリのコストと性能に影響を与える可能性があります。  
You’ve shared that optimizing Iceberg data layout is operationally complex and often requires developing and maintaining custom pipelines.  
Icebergデータレイアウトの最適化は運用上複雑であり、しばしばカスタムパイプラインの開発と維持が必要であると共有されています。  
Although the default binpack strategy with managed compaction provides notable performance improvements, introducing sort and z-order compaction options for both S3 and S3 Tables delivers even greater gains for queries filtering across one or more dimensions.  
**管理された圧縮を伴うデフォルトのbinpack戦略は顕著な性能向上を提供しますが、S3およびS3テーブルの両方に対してソートおよびZオーダー圧縮オプションを導入することで、1つ以上の次元にわたるフィルタリングを行うクエリに対してさらに大きな利点をもたらします。**  (ありがてぇ...!:thinking:)

<!-- ここまで読んだ! -->

## Two new compaction strategies: Sort and z-order 2つの新しい圧縮戦略: ソートとZオーダー  

To help organize your data more efficiently, Amazon S3 now supports two new compaction strategies: sort and z-order, in addition to the default binpack compaction.  
データをより効率的に整理するために、Amazon S3はデフォルトのbinpack圧縮に加えて、ソートとZオーダーという2つの新しい圧縮戦略をサポートしています。  
These advanced strategies are available for both fully managed S3 Tables and Iceberg tables in general purpose S3 buckets through AWS Glue Data Catalog optimizations.  
これらの高度な戦略は、完全に管理されたS3テーブルと一般的なS3バケット内のIcebergテーブルの両方に対して、AWS Glue Data Catalogの最適化を通じて利用可能です。  

Sort compaction organizes files based on a user-defined column order.  
ソート圧縮は、ユーザー定義の列順に基づいてファイルを整理します。  
When your tables have a defined sort order, S3 Tables compaction will now use it to cluster similar values together during the compaction process.  
**テーブルに定義されたソート順がある場合、S3テーブルの圧縮は、圧縮プロセス中に類似の値を一緒にクラスタリングするためにそれを使用します。**  
This improves the efficiency of query execution by reducing the number of files scanned.  
これにより、スキャンされるファイルの数が減少し、クエリ実行の効率が向上します。  
For example, if your table is organized by sort compaction along state and zip_code, queries that filter on those columns will scan fewer files, improving latency and reducing query engine cost.  
たとえば、テーブルが州と郵便番号に沿ってソート圧縮されている場合、これらの列でフィルタリングするクエリは、スキャンするファイルが少なくなり、レイテンシが改善され、クエリエンジンのコストが削減されます。  

<!-- ここまで読んだ! -->

Z-order compaction goes a step further by enabling efficient file pruning across multiple dimensions.  
Zオーダー圧縮は、複数の次元にわたる効率的なファイルのプルーニングを可能にすることで、一歩進んでいます。  
It interleaves the binary representation of values from multiple columns into a single scalar that can be sorted, making this strategy particularly useful for spatial or multidimensional queries.  
複数の列からの値のバイナリ表現を単一のスカラーに交互に配置し、ソート可能にすることで、この戦略は特に空間的または多次元クエリに役立ちます。  
For example, if your workloads include queries that simultaneously filter by pickup_location, dropoff_location, and fare_amount, z-order compaction can reduce the total number of files scanned compared to traditional sort-based layouts.  
たとえば、ワークロードにピックアップ場所、ドロップオフ場所、運賃額で同時にフィルタリングするクエリが含まれている場合、Zオーダー圧縮は従来のソートベースのレイアウトと比較してスキャンされるファイルの総数を減少させることができます。  

<!-- ここまで読んだ! -->

S3 Tables use your Iceberg table metadata to determine the current sort order.  
**S3テーブルは、Icebergテーブルのメタデータを使用して現在のソート順を決定**します。  
If a table has a defined sort order, no additional configuration is needed to activate sort compaction—it’s automatically applied during ongoing maintenance.  
**テーブルに定義されたソート順がある場合、ソート圧縮を有効にするために追加の設定は必要ありません。**これは、継続的なメンテナンス中に自動的に適用されます。  
To use z-order, you need to update the table maintenance configuration using the S3 Tables API and set the strategy to z-order.  
**Zオーダーを使用するには、S3テーブルAPIを使用してテーブルメンテナンス設定を更新し、戦略をZオーダーに設定する必要**があります。
For Iceberg tables in general purpose S3 buckets, you can configure AWS Glue Data Catalog to use sort or z-order compaction during optimization by updating the compaction settings.  
一般的なS3バケット内のIcebergテーブルに対しては、圧縮設定を更新することで、最適化中にAWS Glue Data CatalogをソートまたはZオーダー圧縮を使用するように設定できます。  
Only new data written after enabling sort or z-order will be affected.  
**ソートまたはZオーダーを有効にした後に書き込まれた新しいデータのみが影響を受けます。**  
Existing compacted files will remain unchanged unless you explicitly rewrite them by increasing the target file size in table maintenance settings or rewriting data using standard Iceberg tools.  
**既存の圧縮ファイルは、テーブルメンテナンス設定でターゲットファイルサイズを増加させるか、標準のIcebergツールを使用してデータを書き換えない限り、変更されません。**
This behavior is designed to give you control over when and how much data is reorganized, balancing cost and performance.  
この動作は、データを再編成するタイミングと量を制御できるように設計されており、コストと性能のバランスを取ります。  

<!-- ここまで読んだ! -->

## Let’s see it in action  実際に見てみましょう  

I’ll walk you through a simplified example using Apache Spark and the AWS Command Line Interface (AWS CLI).  
Apache SparkとAWSコマンドラインインターフェース（AWS CLI）を使用した簡略化された例を紹介します。  
I have a Spark cluster installed and an S3 table bucket.  
Sparkクラスターがインストールされており、S3テーブルバケットがあります。  
I have a table named testtable in a testnamespace.  
testnamespaceにtesttableという名前のテーブルがあります。  
I temporarily disabled compaction, the time for me to add data into the table.  
テーブルにデータを追加するための時間として、一時的に圧縮を無効にしました。  
Let’s see it in action  
実際に見てみましょう  

After adding data, I check the file structure of the table.  
データを追加した後、テーブルのファイル構造を確認します。  

```sql
spark.sql("""
  SELECT 
    substring_index(file_path, '/', -1) as file_name,
    record_count,
    file_size_in_bytes,
    CAST(UNHEX(hex(lower_bounds[2])) AS STRING) as lower_bound_name,
    CAST(UNHEX(hex(upper_bounds[2])) AS STRING) as upper_bound_name
  FROM ice_catalog.testnamespace.testtable.files
  ORDER BY file_name
""").show(20, false)
```

I observe the table is made of multiple small files and that the upper and lower bounds for the new files have overlap–the data is certainly unsorted.
テーブルは複数の小さなファイルで構成されており、新しいファイルの上限と下限が重なっていることがわかります。データは確かにソートされていません。

I set the table sort order.
テーブルのソート順を設定します。

I enable table compaction (it’s enabled by default; I disabled it at the start of this demo)
テーブルの圧縮を有効にします（デフォルトで有効になっています。デモの開始時に無効にしました）

Then, I wait for the next compaction job to trigger. These run throughout the day, when there are enough small files. I can check the compaction status with the following command.
その後、次の圧縮ジョブがトリガーされるのを待ちます。これらは、十分な小さなファイルがあるときに一日中実行されます。次のコマンドで圧縮の状態を確認できます。

When the compaction is done, I inspect the files that make up my table one more time. I see that the data was compacted to two files, and the upper and lower bounds show that the data was sorted across these two files.
圧縮が完了したら、テーブルを構成するファイルをもう一度確認します。データが2つのファイルに圧縮され、上限と下限がこれら2つのファイルにわたってデータがソートされていることがわかります。


```sql
spark.sql("""
SELECT
substring_index(file_path,'/', -1)as file_name,
record_count,
file_size_in_bytes,
CAST(UNHEX(hex(lower_bounds[2]))AS STRING)as lower_bound_name,
CAST(UNHEX(hex(upper_bounds[2]))AS STRING)as upper_bound_name
FROM ice_catalog.testnamespace.testtable.files
ORDER BY file_name""").show(20,false)
```

There are fewer files, they have larger sizes, and there is a better clustering across the specified sort column.
ファイルの数が少なくなり、サイズが大きくなり、指定されたソート列に沿ったクラスタリングが改善されました。

To use z-order, I follow the same steps, but I set strategy=z-order in the maintenance configuration.
z-orderを使用するには、同じ手順に従いますが、メンテナンス設定でstrategy=z-orderを設定します。

## Regional availability 

Sort and z-order compaction are now available in all AWS Regions where Amazon S3 Tables are supported and for general purpose S3 buckets where optimization with AWS Glue Data Catalog is available.
地域の可用性として、**Sortおよびz-order圧縮は、Amazon S3 TablesがサポートされているすべてのAWSリージョンおよびAWS Glue Data Catalogによる最適化が可能な一般的なS3バケットで利用可能**です。
There is no additional charge for S3 Tables beyond existing usage and maintenance fees.
S3 Tablesに関しては、既存の使用料およびメンテナンス料金を超える追加料金はありません。
For Data Catalog optimizations, compute charges apply during compaction.
データカタログの最適化については、圧縮中に計算料金が適用されます。

With these changes, queries that filter on the sort or z-order columns benefit from faster scan times and reduced engine costs.
これらの変更により、ソートまたはz-order列でフィルタリングするクエリは、スキャン時間の短縮とエンジンコストの削減の恩恵を受けます。
In my experience, depending on my data layout and query patterns, I observed performance improvements of threefold or more when switching from binpack to sort or z-order.
**私の経験では、データのレイアウトやクエリパターンに応じて、binpackからsortまたはz-orderに切り替えた際に、3倍以上のパフォーマンス向上を観察しました。**
Tell us how much your gains are on your actual data.
実際のデータでの利益がどれくらいか教えてください。

<!-- ここまで読んだ! -->

To learn more, visit the Amazon S3 Tables product page or review the S3 Tables maintenance documentation.
詳細を学ぶには、[Amazon S3 Tablesの製品ページ](https://aws.amazon.com/s3/features/tables/)を訪れるか、[S3 Tablesのメンテナンスドキュメント](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html)を確認してください。
You can also start testing the new strategies on your own tables today using the S3 Tables API or AWS Glue optimizations.
また、S3 Tables APIや[AWS Glueの最適化](https://docs.aws.amazon.com/glue/latest/dg/table-optimizers.html)を使用して、今日から自分のテーブルで新しい戦略をテストすることもできます。

<!-- ここまで読んだ! -->
