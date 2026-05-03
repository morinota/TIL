refs: /tmp/defining_data_products_original.md


# Defining Data Products: A Community Effort データプロダクトの定義：コミュニティの取り組み  
**Source:** https://medium.com/data-mesh-learning/defining-data-products-a-community-effort-77363611e5c5  
**Author:** Jean-Georges Perrin  
**Published:** Jan 28, 2025  
**Publication:** Data Mesh Learning  

---  

Redefining data products through community insights, bridging product thinking and engineering principles for the future of data.  
コミュニティの洞察を通じてデータプロダクトを再定義し、製品思考とエンジニアリング原則を結びつけてデータの未来を見据えます。  

> Besides the fire, this was pretty much what happened at Data Days Texas: 40 people in a room.  
> 火事を除けば、これがテキサスデータデイズで起こったことのほとんどです：40人が一つの部屋にいました。  

At Data Days Texas, I had the privilege of moderating a discussion around a deceptively simple yet critical question: What is a data product?  
テキサスデータデイズでは、一見単純でありながら重要な質問「データプロダクトとは何か？」についての議論を進行する特権を得ました。
Spoiler alert — it didn't go as I expected.  
ネタバレですが、私の予想とは異なる展開になりました。  
What unfolded was a dynamic exchange of ideas, perspectives, and insights from some of the brightest minds in the field.  
展開されたのは、この分野で最も優れた頭脳たちからのアイデア、視点、洞察の活発な交換でした。  

With the room packed with thought leaders like Malcolm Hawker, Bethany Lyons, Ryan Dolley, Lisa N. Cao, Yoann Benoit, Joe Reis, Juan Sequeda, and others,  
マルコム・ホーカー、ベサニー・ライオンズ、ライアン・ドリー、リサ・N・カオ、ヨアン・ブノワ、ジョー・レイス、フアン・セケダなどの思想的リーダーたちで満員の部屋で、  
I quickly realized this wasn't a question with a one-size-fits-all answer.  
私はすぐに、この質問には一律の答えがないことに気づきました。  
However, I took extensive notes and will attempt to distill them into something actionable and (hopefully) insightful.  
しかし、私は詳細なメモを取り、それを実行可能で（願わくば）洞察に満ちたものにまとめようと試みます。  

<!-- ここまで読んだ! -->

## Why Data Products Matter なぜデータプロダクトが重要なのか

Interest in data products has surged, especially following Zhamak Dehghani's influential work on Data Mesh (Data Mesh: Delivering Data-Driven Value at Scale, O'Reilly, 2022) and Gartner's recent focus on data products in their data management hype cycle. 
データプロダクトへの関心は高まっており、特にZhamak Dehghaniのデータメッシュに関する影響力のある研究（Data Mesh: Delivering Data-Driven Value at Scale, O'Reilly, 2022）や、Gartnerのデータ管理ハイプサイクルにおけるデータプロダクトへの最近の注目に続いています。 
Data products represent a paradigm shift — treating data with the same principles as software products. 
データプロダクトはパラダイムシフトを表しており、**データをソフトウェアプロダクトと同じ原則で扱います。** 
However, confusion persists about what exactly constitutes a data product. 
しかし、データプロダクトが正確に何を構成するのかについては混乱が続いています。

<!-- ここまで読んだ! -->

## Diverging Perspectives 視点の相違  

### The Product Management View プロダクトマネジメントの視点  

From a product management standpoint, a data product is, first and foremost, a product.  
プロダクトマネジメントの観点から見ると、データプロダクトはまず第一に製品です。  
Customers — whether internal or external — consume the product.  
顧客は、内部であれ外部であれ、その製品を消費します。  
It relies on regular scaled consumption.  
それは定期的なスケール消費に依存しています。  
It must have a value proposition, a clear use case, and a design that aligns with an ideal customer profile (ICP, Framework for Ideal Customer Profile Development, 2019).  
それは価値提案、明確なユースケース、理想的な顧客プロファイル（ICP、理想的な顧客プロファイル開発のためのフレームワーク、2019）に沿ったデザインを持たなければなりません。  
High-quality data products incorporate history, data quality rules, and reusability while applying product thinking methodologies to ensure alignment and success.  
**高品質のデータプロダクトは、履歴、データ品質ルール、再利用性を取り入れ、整合性と成功を確保するためにプロダクト思考の方法論を適用**します。  

Data is the product for data(set) vendors like D&B, Sequentum, and others.  
データは、D&BやSequentumなどのデータ（セット）ベンダーにとっての製品です。  
It's a product, not a service, as it is manufactured for reselling (Oxford Languages, OUP).  
それは製品であり、サービスではありません。なぜなら、再販のために製造されるからです（Oxford Languages, OUP）。  
While technically accurate, this category — 'products composed of data' — shouldn't be confused with the broader concept of data products in engineering and product management.  
技術的には正確ですが、このカテゴリ—「データで構成された製品」—は、エンジニアリングやプロダクトマネジメントにおけるデータプロダクトのより広い概念と混同すべきではありません。 

<!-- ここまで読んだ! -->

### The Engineering View エンジニアリングの視点  

From an engineering perspective, a data product is a data asset that contains other artifacts (e.g., tables, pipelines, models).  
エンジニアリングの観点から見ると、データプロダクトは他のアーティファクト（例：テーブル、パイプライン、モデル）を含むデータ資産です。  
It includes data contracts to ensure the consistency and quality of inputs and outputs, metadata for governance, and a Software Bill of Materials (SBOM) to document dependencies and transformations.  
それは、入力と出力の一貫性と品質を確保するためのデータ契約、ガバナンスのためのメタデータ、依存関係と変換を文書化するためのソフトウェア部品表（SBOM）を含みます。  

I dodged the question of whether a report was a data product or not, we only had an hour… and had to shut down, in the crib, the attempt to link Data Products to DevOps (although it is a great idea, once more, only one hour).  
私は、レポートがデータプロダクトであるかどうかという質問を避けました。私たちは1時間しかなく…データプロダクトをDevOpsに結びつける試みを、早々に中止しなければなりませんでした（素晴らしいアイデアですが、再度言うと、1時間しかありませんでした）。  
We could not address questions about marketplaces and lifecycle.  
私たちは、市場やライフサイクルに関する質問に対処することができませんでした。  
Room for Data Days Texas 2026!  
2026年のデータデイズテキサスの余地があります！  

At some point, the 2012 DJ Patil's definition of a data product came back: it is a product that facilitates an end goal through the use of data (Data Jujitsu: The Art of Turning Data into Product, O'Reilly, 2012).  
ある時点で、2012年のDJ Patilによるデータプロダクトの定義が戻ってきました：それは**データを使用して最終目標を促進する製品**です（Data Jujitsu: The Art of Turning Data into Product, O'Reilly, 2012）。  
As much as this definition is true, it is a little too generic.  
この定義が真実であるとしても、少し一般的すぎます。  
The world is a bit more complicated in 2025 than 2012, right?  
2025年の世界は2012年よりも少し複雑です、そうですよね？

<!-- ここまで読んだ! -->

## Proposed Definition 提案された定義

My goal of creating a combined definition for both product management and engineering is nearing completion. 
私のプロダクトマネジメントとエンジニアリングの両方に対する統合定義の作成の目標は、完成に近づいています。 
Based on those discussions, here is the definition I am proposing today. 
これらの議論に基づいて、私が今日提案する定義は以下の通りです。

> A data product is a reusable, active, and standardized data asset designed to deliver measurable value to its users — whether internal or external — by applying the rigorous principles of product thinking and management. 
> **データプロダクトとは、内部または外部のユーザーに測定可能な価値を提供するために、製品思考と管理の厳格な原則を適用して設計された再利用可能でアクティブな標準化データ資産**です。

(taxonomyとかknowledge graphとかは上記の定義を満たしてそう...!!:thinking:)

It comprises one or more data artifacts (e.g., datasets, models, pipelines) and is enriched with metadata, including governance policies, data quality rules, data contracts, and, where applicable, a Software Bill of Materials (SBOM) to document its dependencies and components. 
それは、1つ以上のデータアーティファクト（例：データセット、モデル、パイプライン）で構成され、ガバナンスポリシー、データ品質ルール、データ契約、そして該当する場合には依存関係とコンポーネントを文書化するためのソフトウェア部品表（SBOM）を含むメタデータで強化されています。
Ownership of a data product is aligned to a specific domain or use case, ensuring accountability, stewardship, and its continuous evolution throughout its lifecycle. 
**データプロダクトの所有権は特定のドメインまたはユースケースに関連付けられ、責任、管理、そしてライフサイクル全体にわたる継続的な進化を保証**します。
Adhering to the FAIR principles — Findable, Accessible, Interoperable, and Reusable — a data product is designed to be discoverable, scalable, reusable, and aligned with both business and regulatory standards, driving innovation and efficiency in modern data ecosystems. 
**FAIR原則（Findable, Accessible, Interoperable, and Reusable）に従い、データプロダクトは発見可能で、スケーラブルで、再利用可能であり、ビジネスおよび規制基準に整合するように設計**されており、現代のデータエコシステムにおける革新と効率を促進します。

Note: this definition is in the public domain as Community Definition of Data Product by Jean-Georges Perrin et al. is marked with CC0 1.0 Universal. 
注：この定義は、Jean-Georges Perrinらによるデータプロダクトのコミュニティ定義がCC0 1.0 Universalでマークされているため、パブリックドメインにあります。

<!-- ここまで読んだ! -->

A shorter version of the definition, which I like less, could be: 
私があまり好まない短いバージョンの定義は次のようになります：

> A data product is a reusable, active, and standardized data asset designed to deliver measurable value by applying product thinking principles. 
> データプロダクトとは、製品思考の原則を適用して測定可能な価値を提供するために設計された再利用可能でアクティブな標準化データ資産です。
It includes one or more artifacts enriched with metadata like governance policies, data contracts, and optionally a SBOM. 
それは、ガバナンスポリシー、データ契約、そしてオプションでSBOMのようなメタデータで強化された1つ以上のアーティファクトを含みます。
Aligned to a specific domain or use case, it ensures accountability, continuous evolution, and adheres to the FAIR principles enabling scalability, reusability, and compliance with business and regulatory standards. 
特定のドメインまたはユースケースに整合し、責任、継続的な進化を保証し、スケーラビリティ、再利用性、ビジネスおよび規制基準への準拠を可能にするFAIR原則に従います。

<!-- ここまで読んだ! -->

## Looking Ahead 先を見据えて

Data products are at the heart of the future of data engineering and management. 
データプロダクトは、データエンジニアリングと管理の未来の中心にあります。
As we move toward treating data more like software, incorporating agile principles, and aligning around frameworks like Data Mesh and Data Product thinking, reaching a shared definition becomes essential. 
私たちがデータをソフトウェアのように扱い、アジャイルの原則を取り入れ、Data MeshやData Product思考のようなフレームワークに沿って進むにつれて、共通の定義に到達することが不可欠になります。
I hope this resonates with you, and I'd love to hear your thoughts. 
これがあなたに響くことを願っており、あなたの考えを聞きたいと思っています。
Together, as a community, we can define and shape the next chapter of the data revolution. 
私たちがコミュニティとして一緒に、データ革命の次の章を定義し、形作ることができます。

<!-- ここまで読んだ! -->

## More interesting resources on the topic トピックに関する興味深いリソース

- The ABC(DE) framework from Juan Sequeda.
- Juan SequedaによるABC(DE)フレームワーク。
- Normalizing efforts by the Linux Foundation and the Bitol project.
- Linux FoundationとBitolプロジェクトによる正規化の取り組み。
- The Bitol GitHub.
- BitolのGitHub。

<!-- ここまで読んだ! -->
