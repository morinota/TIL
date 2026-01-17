refs: https://www.coditation.com/blog/achieve-seamless-schema-evolution-with-apache-iceberg


# How to Achieve Seamless Schema Evolution with Apache Iceberg　Apache Icebergによるシームレスなスキーマ進化の実現方法

Businesses are constantly evolving, and their data infrastructure must keep pace. 
**ビジネスは常に進化しており、そのデータインフラストラクチャもそれに合わせて進化しなければなりません。** 
Apache Iceberg, a powerful open-source framework, offers a flexible approach to data modeling that empowers organizations to adapt to changing data needs. 
Apache Icebergは、強力なオープンソースフレームワークであり、データモデリングに柔軟なアプローチを提供し、組織が変化するデータニーズに適応できるようにします。

In this in-depth exploration, we'll delve into the practical applications of Iceberg's schema evolution capabilities. 
この詳細な探求では、**Icebergのスキーマ進化機能の実用的な応用(practical applications)について**掘り下げます。 
Through real-world case studies, performance benchmarks, and a hands-on tutorial, you'll discover how to leverage Iceberg to build a resilient and scalable data platform. 
実際のケーススタディ、パフォーマンスベンチマーク、ハンズオンチュートリアルを通じて、Icebergを活用して堅牢でスケーラブルなデータプラットフォームを構築する方法を発見します。

To illustrate the challenges of rigid data models, let's revisit a personal experience from my early days as a data engineer. 
堅固なデータモデルの課題を示すために、私のデータエンジニアとしての初期の経験を振り返ってみましょう。 
In 2010, I faced the daunting task of updating a massive customer database to accommodate social media handles. 
2010年、私はソーシャルメディアのハンドルに対応するために、大規模な顧客データベースを更新するという困難な課題に直面しました。 
The limitations of the inflexible schema made this a time-consuming and error-prone process. 
柔軟性のないスキーマの制限により、これは時間がかかり、エラーが発生しやすいプロセスとなりました。 
A tool like Iceberg could have streamlined this effort significantly. 
Icebergのようなツールがあれば、この作業を大幅に効率化できたでしょう。

Today, the data landscape is more complex than ever. 
今日、データの状況はかつてないほど複雑です。 
IDC predicts that the global datasphere will reach a staggering 175 zettabytes by 2025. 
IDCは、2025年までに世界のデータ空間が驚異的な175ゼタバイトに達すると予測しています。 
To effectively manage this exponential growth, organizations need a data solution that can evolve alongside their business. 
この指数関数的な成長を効果的に管理するために、組織はビジネスと共に進化できるデータソリューションを必要としています。

<!-- ここまで読んだ! -->

### What is Apache Iceberg and Schema Evolution Apache Icebergとは何か、スキーマ進化とは

Apache Iceberg, a powerful open-source table format, streamlines the management of massive analytical datasets. 
Apache Icebergは、強力なオープンソースのテーブルフォーマットであり、大規模な分析データセットの管理を効率化します。 
Born at Netflix and now a core Apache project, Iceberg excels in handling large, slow-moving tabular data. 
**Netflixで生まれ、現在はApacheのコアプロジェクトとなっているIcebergは、大規模で動きの遅い表形式データの処理に優れています。** 
A key feature of Iceberg is schema evolution, which allows for dynamic changes to table structures, such as adding, removing, or modifying columns. 
**Icebergの重要な機能はスキーマ進化**であり、列の追加、削除、または変更など、テーブル構造に動的な変更を加えることができます。 
This flexibility is achieved without disruptive table rewrites or intricate ETL processes, ensuring seamless data evolution and backward compatibility. 
この柔軟性は、破壊的なテーブルの書き換えや複雑なETLプロセスなしで実現され、シームレスなデータ進化と後方互換性を確保します。

<!-- ここまで読んだ! -->

#### Key Benefits of Iceberg's Schema Evolution: Icebergのスキーマ進化の主な利点：

1. Flexibility: Adapt to changing business requirements without disrupting existing data or queries.
   1. 柔軟性：既存のデータやクエリを中断することなく、変化するビジネス要件に適応します。
2. Performance: Avoid costly full table rewrites when making schema changes.
   1. パフォーマンス：スキーマ変更時に高額な全テーブルの書き換えを避けます。
3. Compatibility: Maintain backward compatibility with older versions of the schema.
   1. 互換性：スキーマの古いバージョンとの後方互換性を維持します。
4. Simplicity: Make schema changes with simple SQL commands.
   1. シンプルさ：簡単なSQLコマンドでスキーマ変更を行います。

Let's delve into how Iceberg outperforms other data lake formats in terms of schema evolution flexibility. 
Icebergがスキーマ進化の柔軟性において他のデータレイクフォーマットを上回る方法を掘り下げてみましょう。 

![]()

Iceberg stands out as the premier platform for schema evolution, offering the most comprehensive and flexible capabilities in the market. 
Icebergはスキーマ進化のための主要なプラットフォームとして際立っており、市場で最も包括的で柔軟な機能を提供しています。

<!-- ここまで読んだ! -->

### Real-World Use Case: E-commerce Product Catalog 実世界のユースケース：Eコマース製品カタログ

To truly grasp the potential of Iceberg’s schema evolution, let’s delve into a practical example. 
Icebergのスキーマ進化の可能性を真に理解するために、実際の例を掘り下げてみましょう。 
Consider a massive e-commerce platform. 
大規模なEコマースプラットフォームを考えてみましょう。 
Initially, its product catalog schema might resemble the following structure:
最初は、その製品カタログのスキーマは以下の構造に似ているかもしれません：

```sql
CREATE TABLE products (
  id BIGINT,
  name STRING,
  price DECIMAL(10, 2),
  category STRING
)
```

As your business expands, you'll inevitably need to adapt. 
ビジネスが拡大するにつれて、必然的に適応する必要があります。 
Whether it's adding more product details, supporting diverse currencies, or incorporating customer reviews, Iceberg makes scaling your online store effortless. 
**製品の詳細を追加したり、多様な通貨をサポートしたり、顧客レビューを組み込んだりする場合でも、Icebergはオンラインストアのスケーリングを容易にします。**
(ここの"オンラインストア"って、高速なリアルタイムアクセスできるデータストア、というよりは、本番運用されてるデータストア的なニュアンスなのかな...?:thinking:)

1. Adding a new column:
   1. 新しい列を追加する：
   ```sql
   ALTER TABLE products ADD COLUMN description STRING

   ```


2. Adding a nested structure for multi-currency support:
   1. マルチ通貨サポートのためのネスト構造を追加する：
   ```sql
   ALTER TABLE products ADD COLUMN prices STRUCT<usd:DECIMAL(10,2), eur:DECIMAL(10,2), gbp:DECIMAL(10,2)>
   ```

3. Adding a column with a default value for user ratings:
   1. ユーザー評価のデフォルト値を持つ列を追加する：
   ```sql
   ALTER TABLE products ADD COLUMN avg_rating FLOAT DEFAULT 0.0
   ```

Experience instant schema updates without the need for table-wide rewrites. 
テーブル全体の書き換えなしで、即座にスキーマの更新を体験してください。
Your existing ETL processes and queries remain unaffected, seamlessly accessing the old schema for historical data and the new schema for current information. 
**既存のETLプロセスやクエリは影響を受けず、過去のデータには古いスキーマを、新しい情報には新しいスキーマをシームレスにアクセス**できます。

<!-- ここまで読んだ! -->

### Benchmarking Schema Evolution Performance スキーマ進化のパフォーマンスベンチマーク

Let's delve into the performance gains offered by Iceberg's schema evolution. 
Icebergのスキーマ進化が提供するパフォーマンス向上について掘り下げてみましょう。 
By comparing the time required to add a column to a massive 1TB table, we'll illustrate the significant speed advantage over traditional Hive tables. 
**1TBの大規模なテーブルに列を追加するのに必要な時間を比較**することで、従来のHiveテーブルに対する大幅な速度の利点を示します。

![]()

Iceberg's performance advantage is undeniable. 
Icebergのパフォーマンスの利点は否定できません。 
While Hive struggles with significant read performance degradation and lengthy table rewrites for column additions, Iceberg executes these operations nearly instantaneously without impacting read speeds. 
Hiveは列の追加に対して著しい読み取りパフォーマンスの低下や長時間のテーブル書き換えに苦しむ一方で、Icebergは読み取り速度に影響を与えることなく、これらの操作をほぼ瞬時に実行します。

Let's get practical: A step-by-step guide to witness Iceberg's schema evolution in real-time. 
実践的に見てみましょう：Icebergのスキーマ進化をリアルタイムで目撃するためのステップバイステップガイドです。

<!-- ここまで読んだ! -->

### Hands-On Tutorial: Implementing Schema Evolution with Apache Iceberg　ハンズオンチュートリアル：Apache Icebergを使用したスキーマ進化の実装

This tutorial will guide you through the process of interacting with Iceberg tables using PySpark. 
このチュートリアルでは、**PySparkを使用してIcebergテーブルと対話するプロセス**を案内します。 
To begin, ensure that your PySpark environment is configured to support Iceberg by incorporating the required JAR files into your PySpark setup. 
まず、必要なJARファイルをPySparkのセットアップに組み込むことで、PySpark環境がIcebergをサポートするように設定されていることを確認してください。

Step 1: Set up the Spark session
ステップ1：Sparkセッションを設定する

```python
from pyspark.sqlimportSparkSessionspark=SparkSession.builder \
.appName("IcebergSchemaEvolution") \
.config("spark.jars.packages","org.apache.iceberg:iceberg-spark3-runtime:0.13.1,org.apache.hadoop:hadoop-aws:3.2.0") \
.getOrCreate()
```

Step 2: Create an initial Iceberg table
ステップ2：初期のIcebergテーブルを作成する

```python
spark.sql("""
CREATE TABLE IF NOT EXISTS default.products (
id BIGINT,
name STRING,
price DECIMAL(10, 2),
category STRING
) USING iceberg
""")# Insert some sample dataspark.sql("""
INSERT INTO default.products VALUES
(1, 'Laptop', 999.99, 'Electronics'),
(2, 'Desk Chair', 199.99, 'Furniture'),
(3, 'Coffee Maker', 49.99, 'Appliances')
""")
```

Step 3: Add a new column
ステップ3：新しい列を追加する

```python
spark.sql("ALTER TABLE default.products ADD COLUMN description STRING")# Insert data with the new columnspark.sql("""
INSERT INTO default.products VALUES
(4, 'Smartphone', 599.99, 'Electronics', 'Latest model with 5G support')
""")
```


Step 4: Add a nested structure for multi-currency support
ステップ4：マルチ通貨サポートのためのネスト構造を追加する

```python
spark.sql("""
ALTER TABLE default.products ADD COLUMN prices STRUCT<usd:DECIMAL(10,2), eur:DECIMAL(10,2), gbp:DECIMAL(10,2)>
""")# Update existing rows with the new structurespark.sql("""
UPDATE default.products
SET prices = NAMED_STRUCT('usd', price, 'eur', price * 0.84, 'gbp', price * 0.72)
WHERE prices IS NULL
""")
```


Step 5: Rename a column
ステップ5：列の名前を変更する

```python
spark.sql("ALTERTABLEdefault.productsRENAME COLUMN categoryTOproduct_category")
```


Step 6: Query the evolved schema
ステップ6：進化したスキーマをクエリする

```Python
result=spark.sql("SELECT * FROM default.products").show(truncate=False)
```

Streamline Your Data Warehouse: Learn how to effortlessly modify Iceberg table schemas. 
データウェアハウスを効率化する：Icebergテーブルスキーマを簡単に変更する方法を学びましょう。 
Add columns, nest structures, and rename fields without disruptions or data transfers. 
列を追加し、構造をネストし、フィールドの名前を変更しても中断やデータ転送は不要です。

<!-- ここまで読んだ! -->

### Best Practices for Schema Evolution with Iceberg Icebergを使用したスキーマ進化のベストプラクティス

While Iceberg simplifies schema evolution, adhering to best practices ensures smooth transitions and optimal performance. 
Icebergはスキーマ進化を簡素化しますが、ベストプラクティスに従うことでスムーズな移行と最適なパフォーマンスを確保できます。

1. Plan for future growth: Design your initial schema with potential future changes in mind.
   1. 将来の成長を計画する：初期スキーマを将来の変更の可能性を考慮して設計します。
2. Use meaningful default values: When adding columns, consider providing default values that make sense for your data.
   1. **意味のあるデフォルト値を使用する：列を追加する際には、データに適したデフォルト値を提供すること**を検討します。
3. Communicate changes: Ensure all stakeholders are aware of schema changes to prevent unexpected behavior in downstream processes.
   1. 変更を伝える：すべての利害関係者がスキーマの変更を認識していることを確認し、下流プロセスでの予期しない動作を防ぎます。
4. Version control your schemas: Keep track of schema changes in your version control system for easy rollback and auditing.
   1. **スキーマのバージョン管理：スキーマの変更をバージョン管理システムで追跡し、簡単にロールバックや監査ができるようにします。** (そう、これしたいんだよなぁ:thinking:)
5. Test thoroughly: Always test schema changes in a staging environment before applying them to production.
   1. **徹底的にテストする：スキーマ変更を本番環境に適用する前に、常にステージング環境でテスト**します。

### The Impact of Flexible Data Modeling on Business Agility 柔軟なデータモデリングがビジネスの機敏性に与える影響

Accelerate your data journey with agile data modeling. 
アジャイルデータモデリングでデータの旅を加速させましょう。 
By adopting flexible data modeling techniques, like those powered by Iceberg, organizations can slash time-to-market for new data products by up to 35% and supercharge data team productivity by 40%, as revealed in a 2023 Databricks survey. 
**Icebergによって強化された柔軟なデータモデリング技術を採用することで、組織は新しいデータ製品の市場投入までの時間を最大35％短縮し、データチームの生産性を40％向上させることができる**と、2023年のDatabricksの調査で明らかになりました。

Let's break down some of the key business benefits:
いくつかの主要なビジネスの利点を分解してみましょう：

1. Faster Innovation: With the ability to quickly adapt data models, businesses can rapidly prototype and launch new features or products.
   1. より迅速なイノベーション：データモデルを迅速に適応させる能力により、ビジネスは新しい機能や製品を迅速にプロトタイプし、立ち上げることができます。
2. Reduced Operational Costs: By eliminating the need for costly data migrations and downtime, companies can significantly reduce their operational expenses.
   1. 運用コストの削減：高額なデータ移行やダウンタイムの必要性を排除することで、企業は運用費用を大幅に削減できます。
3. Improved Data Quality: Flexible schemas allow for more accurate representation of real-world entities, leading to better data quality and more insightful analytics.
   1. データ品質の向上：柔軟なスキーマにより、現実のエンティティをより正確に表現できるため、データ品質が向上し、より洞察に満ちた分析が可能になります。
4. Enhanced Collaboration: When data scientists and analysts can easily add or modify columns, it fosters a culture of experimentation and collaboration.
   1. **コラボレーションの強化：データサイエンティストやアナリストが簡単に列を追加または変更できると、実験とコラボレーションの文化**が育まれます。

<!-- ここまで読んだ! -->

### Challenges and Considerations 課題と考慮事項

While Iceberg offers robust schema evolution, it's not without its hurdles. 
Icebergは堅牢なスキーマ進化を提供しますが、課題がないわけではありません。

1. Governance: With great flexibility comes the need for strong governance. 
   1. ガバナンス：**大きな柔軟性には強力なガバナンスが必要**です。 
   Implement robust processes to manage and track schema changes.
   **スキーマ変更を管理し追跡するための堅牢なプロセスを実装すべき**です。
2. Training: Teams need to be trained on best practices for schema evolution to avoid potential pitfalls.
   1. トレーニング：チームはスキーマ進化のベストプラクティスについてトレーニングを受け、潜在的な落とし穴を避ける必要があります。
3. Tool Compatibility: Ensure that all your data tools and pipelines are compatible with Iceberg's format and can handle schema changes gracefully.
   1. ツールの互換性：すべてのデータツールとパイプラインがIcebergのフォーマットと互換性があり、スキーマ変更をスムーズに処理できることを確認します。

<!-- ここ   まで読んだ! -->

### Future Trends in Data Modeling　データモデリングの未来のトレンド

The future of data modeling is flexible and adaptable. 
データモデリングの未来は柔軟で適応可能です。 
As we move forward, we're witnessing a surge in the adoption of:
私たちが前進するにつれて、次のような採用の急増を目撃しています。

1. Self-describing data formats: Like Iceberg, these formats carry their schema information with them, enabling more dynamic data interactions.
   1. 自己記述型データフォーマット：Icebergのように、これらのフォーマットはスキーマ情報を持ち運び、より動的なデータインタラクションを可能にします。
2. Graph-based data models: These offer even more flexibility for complex, interconnected data.
   1. グラフベースのデータモデル：これらは、複雑で相互接続されたデータに対してさらに柔軟性を提供します。
3. AI-assisted schema design: Machine learning models that can suggest optimal schema designs based on data patterns and usage.
   1. AI支援スキーマ設計：データパターンと使用に基づいて最適なスキーマ設計を提案できる機械学習モデルです。

### Conclusion 結論

#### Navigate Evolving Data Lakes with Agile Schema Management in Apache Iceberg Apache Icebergにおけるアジャイルスキーマ管理で進化するデータレイクをナビゲートする

The ever-shifting tides of business demands can leave your data lake feeling like a tangled mess.
ビジネスの要求の絶え間ない変化は、あなたのデータレイクを絡まった混乱のように感じさせることがあります。
Traditional data management struggles to adapt, leading to costly migrations and downtime.
従来のデータ管理は適応に苦労し、**高額な移行やダウンタイム**を引き起こします。
Enter Apache Iceberg, a revolutionary force in data lake management.
Apache Icebergが登場します。これはデータレイク管理における革命的な力です。
It empowers organizations with unparalleled schema evolution capabilities.
それは、比類のないスキーマ進化の能力を持つ組織を力づけます。
Imagine a data model that bends and adjusts, seamlessly integrating new information requirements without disrupting existing workflows.
既存のワークフローを妨げることなく、新しい情報要件をシームレスに統合する、曲がりくねったデータモデルを想像してみてください。
Iceberg achieves this through its flexible data modeling approach.
Icebergは、その柔軟なデータモデリングアプローチを通じてこれを実現します。
Update times plummet, queries run smoother, and business agility skyrockets.
更新時間は急減し、クエリはスムーズに実行され、ビジネスの機敏性は急上昇します。
Forget the rigid structures of the past – Iceberg lets your data model evolve organically, like a majestic iceberg carving its path through the ocean of information.
過去の硬直した構造を忘れてください。Icebergは、あなたのデータモデルが情報の海を切り開く壮大な氷山のように有機的に進化することを可能にします。

#### Embrace Change, Conquer Big Data 変化を受け入れ、大規模データを征服する

The one constant in big data? Change itself.
大規模データにおける唯一の不変のもの？それ自体が変化です。
 Schemas evolve, data formats shift, and new requirements emerge.
With Iceberg, you're no longer caught off guard.
Icebergを使えば、もはや不意を突かれることはありません。
Proactive planning and adaptable schema management ensure your data lake thrives amidst constant evolution.
積極的な計画と適応可能なスキーマ管理により、あなたのデータレイクは絶え間ない進化の中で繁栄します。

#### Key Takeaways: 重要なポイント

- Flexible Data Modeling: Iceberg empowers you to effortlessly adapt your data model as business needs evolve.
  - 柔軟なデータモデリング：Icebergは、ビジネスニーズの進化に応じてデータモデルを容易に適応させる力を与えます。
- Reduced Downtime: Schema updates are lightning-fast, minimizing disruptions to your operations.
  - ダウンタイムの削減：スキーマの更新は非常に迅速で、運用への影響を最小限に抑えます。
- Enhanced Query Performance: Queries run smoother, leveraging the power of your data lake more effectively.
  - クエリパフォーマンスの向上：クエリはスムーズに実行され、データレイクの力をより効果的に活用します。
- Increased Business Agility: Respond to changing market demands with ease, thanks to your adaptable data model.
  - ビジネスの機敏性の向上：適応可能なデータモデルのおかげで、変化する市場の要求に容易に対応できます。

#### Stay Ahead of the Curve with Iceberg Icebergで先を行きましょう

Don't let your data lake become a stagnant swamp.
あなたのデータレイクが停滞した沼にならないようにしましょう。
Embrace the dynamic nature of big data with Apache Iceberg.
Apache Icebergで大規模データの動的な性質を受け入れましょう。
Take control, ride the wave of data evolution, and remain agile, efficient, and ahead of the competition.
コントロールを取り、データの進化の波に乗り、機敏で効率的、そして競争の先を行きましょう。

<!-- ここまで読んだ! -->
