refs: https://en.wikipedia.org/wiki/Automatic_taxonomy_construction


Main menu
- Main page
- Contents
- Current events
- Random article
- About Wikipedia
- Contact us
メインメニュー
- メインページ
- 目次
- 現在の出来事
- ランダム記事
- ウィキペディアについて
- お問い合わせ

Main page
Contents
Current events
Random article
About Wikipedia
Contact us
メインページ
目次
現在の出来事
ランダム記事
ウィキペディアについて
お問い合わせ

- Help
- Learn to edit
- Community portal
- Recent changes
- Upload file
- Special pages
- ヘルプ
- 編集を学ぶ
- コミュニティポータル
- 最近の変更
- ファイルをアップロード
- 特別ページ

Help
Learn to edit
Community portal
Recent changes
Upload file
Special pages
ヘルプ
編集を学ぶ
コミュニティポータル
最近の変更
ファイルをアップロード
特別ページ

Search
Appearance
- Donate
- Create account
- Log in
- 検索
- 外観
- 寄付
- アカウントを作成
- ログイン

Donate
Create account
Log in
寄付
アカウントを作成
ログイン

Personal tools
- Donate
- Create account
- Log in
- 個人ツール
- 寄付
- アカウントを作成
- ログイン



## Contents 目次
- (Top) 
- 1ApproachesToggle Approaches subsection1.1Keyword extraction1.2Hyponymy and "is-a" relations
- 1.1Keyword extraction
- 1.2Hyponymy and "is-a" relations
- 2Applications
- 3ATC software
- 4Other names
- 5See also
- 6References
- 7Further reading
- 8External links

## 1 アプローチ
### Toggle Approaches subsection
- 1.1 キーワード抽出
- 1.2 下位語と「is-a」関係

### 1.1 キーワード抽出
### 1.2 下位語と「is-a」関係

## 2 応用
## 3 ATCソフトウェア
## 4 その他の名称
## 5 関連項目
## 6 参考文献
## 7 さらなる読み物
## 8 外部リンク

### Toggle the table of contents
# 自動分類構築
自動分類構築
自動分類構築
Add languages
Add links
- Article
- Talk
Article
Talk
English
- Read
- Edit
- View history
Read
Edit
View history
Tools
- Read
- Edit
- View history
Read
Edit
View history
- What links here
- Related changes
- Upload file
- Permanent link
- Page information
- Cite this page
- Get shortened URL
What links here
Related changes
Upload file
Permanent link
Page information
Cite this page
Get shortened URL
- Download as PDF
- Printable version
Download as PDF
Printable version
- Wikidata item
Wikidata item

自動分類構築（Automatic taxonomy construction, ATC）とは、コーパスと呼ばれるテキストの集合から分類学的分類を生成するためのソフトウェアプログラムの使用です。ATCは自然言語処理の一分野であり、自然言語処理は人工知能の一分野です。

分類学（taxonomy）または分類学的分類とは、特に階層的な分類のスキームであり、物事がグループやタイプに整理されるものです。[1][2][3][4][5][6] 分類学は、文書、記事、動画などの形で知識を整理し、索引を付けるために使用されることがあり、図書館の分類システムや検索エンジンの分類などの形で、ユーザーが探している情報をより簡単に見つけられるようにします。多くの分類学は階層構造を持っており（したがって、固有の木構造を持っています）、すべてがそうであるわけではありません。

手動で分類学を開発し維持することは、時間とリソースを大幅に必要とする労働集約的な作業であり、分類学のドメイン（範囲、主題、または分野）に対する熟知や専門知識が必要です。これがコストを押し上げ、プロジェクトの範囲を制限します。また、ドメインモデル作成者は独自の視点を持っており、意図せずともその視点が分類学に反映されることになります。ATCは、これらの問題を回避し、制限を取り除くために、人工知能技術を使用して特定のドメインの分類を迅速に自動生成します。



## Approaches アプローチ

There are several approaches to ATC. 
ATCにはいくつかのアプローチがあります。

One approach is to use rules to detect patterns in the corpus and use those patterns to infer relations such as hyponymy. 
1つのアプローチは、コーパス内のパターンを検出するためにルールを使用し、それらのパターンを使用してhyponymy（下位関係）などの関係を推測することです。

Other approaches use machine learning techniques such as Bayesian inferencing and Artificial Neural Networks. 
他のアプローチは、ベイズ推論や人工ニューラルネットワークなどの機械学習技術を使用します。

### Keyword extraction キーワード抽出

One approach to building a taxonomy is to automatically gather the keywords from a domain using keyword extraction, then analyze the relationships between them (see Hyponymy, below), and then arrange them as a taxonomy based on those relationships. 
分類体系を構築する1つのアプローチは、キーワード抽出を使用してドメインから自動的にキーワードを収集し、それらの間の関係を分析し（下記のHyponymyを参照）、それらの関係に基づいて分類体系として整理することです。

### Hyponymy and "is-a" relations ハイポニミーと「is-a」関係

In ATC programs, one of the most important tasks is the discovery of hypernym and hyponym relations among words. 
ATCプログラムにおいて、最も重要なタスクの1つは、単語間のhypernym（上位語）とhyponym（下位語）関係の発見です。

One way to do that from a body of text is to search for certain phrases like "is a" and "such as". 
テキストの中からそれを行う1つの方法は、「is a」や「such as」といった特定のフレーズを検索することです。

In linguistics, is-a relations are called hyponymy. 
言語学において、is-a関係はhyponymy（下位関係）と呼ばれます。

Words that describe categories are called hypernyms and words that are examples of categories are hyponyms. 
カテゴリを説明する単語はhypernyms（上位語）と呼ばれ、カテゴリの例となる単語はhyponyms（下位語）と呼ばれます。

For example, dog is a hypernym and Fido is one of its hyponyms. 
例えば、dog（犬）はhypernym（上位語）であり、Fido（フィド）はそのhyponym（下位語）の1つです。

A word can be both a hyponym and a hypernym. 
単語はhyponym（下位語）でもありhypernym（上位語）でもあり得ます。

So, dog is a hyponym of mammal and also a hypernym of Fido. 
したがって、dog（犬）はmammal（哺乳類）のhyponym（下位語）であり、同時にFido（フィド）のhypernym（上位語）でもあります。

Taxonomies are often represented as is-a hierarchies where each level is more specific than (in mathematical language "a subset of") the level above it. 
分類体系はしばしばis-a階層として表現され、各レベルはその上のレベルよりも具体的です（数学的な言語では「上位集合」）。

For example, a basic biology taxonomy would have concepts such as mammal, which is a subset of animal, and dogs and cats, which are subsets of mammal. 
例えば、基本的な生物学の分類体系には、animal（動物）の部分集合であるmammal（哺乳類）や、mammalの部分集合であるdogs（犬）やcats（猫）などの概念があります。

This kind of taxonomy is called an is-a model because the specific objects are considered instances of a concept. 
この種の分類体系はis-aモデルと呼ばれ、特定のオブジェクトは概念のインスタンスと見なされます。

For example, Fido is-a instance of the concept dog and Fluffy is-a cat. 
例えば、Fido（フィド）は概念dog（犬）のインスタンスであり、Fluffy（フラッフィー）はcat（猫）です。



## Applications 応用

ATC can be used to build taxonomies for search engines, to improve search results.
ATCは、検索エンジンのための分類体系を構築し、検索結果を改善するために使用できます。

ATC systems are a key component of ontology learning (also known as automatic ontology construction), and have been used to automatically generate large ontologies for domains such as insurance and finance.
ATCシステムは、オントロジー学習（自動オントロジー構築とも呼ばれる）の重要な要素であり、保険や金融などの分野の大規模なオントロジーを自動的に生成するために使用されてきました。

They have also been used to enhance existing large networks such as Wordnet to make them more complete and consistent.
また、既存の大規模ネットワーク（Wordnetなど）を強化し、より完全で一貫性のあるものにするためにも使用されています。



## ATC software ATCソフトウェア

[edit] [編集]

[ edit ] [ 編集 ]

(August 2023) (2023年8月)
August 2023 2023年8月



## Other names 他の名称

Please help improve this section by adding citations to reliable sources. 
このセクションを改善するために、信頼できる情報源への引用を追加してください。
Unsourced material may be challenged and removed. 
出典のない資料は異議を唱えられ、削除される可能性があります。
(July 2019) 
（2019年7月）

Other names for automatic taxonomy construction include: 
自動分類体系構築の他の名称には以下が含まれます：

- Automated outline building 
- 自動アウトライン構築
- Automated outline construction 
- 自動アウトライン作成
- Automated outline creation 
- 自動アウトライン生成
- Automated outline extraction 
- 自動アウトライン抽出
- Automated outline generation 
- 自動アウトライン生成
- Automated outline induction 
- 自動アウトライン誘導
- Automated outline learning 
- 自動アウトライン学習
- Automated outlining 
- 自動アウトライン作成
- Automated taxonomy building 
- 自動分類体系構築
- Automated taxonomy construction 
- 自動分類体系構築
- Automated taxonomy creation 
- 自動分類体系作成
- Automated taxonomy extraction 
- 自動分類体系抽出
- Automated taxonomy generation 
- 自動分類体系生成
- Automated taxonomy induction 
- 自動分類体系誘導
- Automated taxonomy learning 
- 自動分類体系学習
- Automatic outline building 
- 自動アウトライン構築
- Automatic outline construction 
- 自動アウトライン作成
- Automatic outline creation 
- 自動アウトライン生成
- Automatic outline extraction 
- 自動アウトライン抽出
- Automatic outline generation 
- 自動アウトライン生成
- Automatic outline induction 
- 自動アウトライン誘導
- Automatic outline learning 
- 自動アウトライン学習
- Automatic taxonomy building 
- 自動分類体系構築
- Automatic taxonomy creation 
- 自動分類体系作成
- Automatic taxonomy extraction 
- 自動分類体系抽出
- Automatic taxonomy generation 
- 自動分類体系生成
- Automatic taxonomy induction 
- 自動分類体系誘導
- Automatic taxonomy learning 
- 自動分類体系学習
- Outline automation 
- アウトライン自動化
- Outline building 
- アウトライン構築
- Outline construction 
- アウトライン作成
- Outline creation 
- アウトライン生成
- Outline extraction 
- アウトライン抽出
- Outline generation 
- アウトライン生成
- Outline induction 
- アウトライン誘導
- Outline learning 
- アウトライン学習
- Semantic taxonomy building 
- セマンティック分類体系構築
- Semantic taxonomy construction 
- セマンティック分類体系構築
- Semantic taxonomy creation 
- セマンティック分類体系作成
- Semantic taxonomy extraction 
- セマンティック分類体系抽出
- Semantic taxonomy generation 
- セマンティック分類体系生成
- Semantic taxonomy induction 
- セマンティック分類体系誘導
- Semantic taxonomy learning 
- セマンティック分類体系学習
- Taxonomy automation 
- 分類体系自動化
- Taxonomy building 
- 分類体系構築
- Taxonomy construction 
- 分類体系作成
- Taxonomy creation 
- 分類体系生成
- Taxonomy extraction 
- 分類体系抽出
- Taxonomy generation 
- 分類体系生成
- Taxonomy induction 
- 分類体系誘導
- Taxonomy learning 
- 分類体系学習



## See also 参照

[edit] 
[編集] 
- Document classification (文書分類)
- Information extraction (情報抽出)



## References 参考文献

1. ^"Taxonomy". 10 October 2021.
1. ^「分類法」。2021年10月10日。

2. ^"Taxonomy Definition & Meaning". Dictionary.com. Retrieved 2022-05-13.
2. ^「分類法の定義と意味」。Dictionary.com。2022年5月13日取得。

3. ^"What is Taxonomy?". 14 August 2017.
3. ^「分類法とは何か？」。2017年8月14日。

4. ^"TAXONOMY | Meaning & Definition for UK English". Lexico.com. Archived from the original on March 2, 2021. Retrieved 2022-05-13.
4. ^「分類法 | 英国英語の意味と定義」。Lexico.com。2021年3月2日に原本からアーカイブ。2022年5月13日取得。

5. ^"What is Taxonomy?". 20 August 2003.
5. ^「分類法とは何か？」。2003年8月20日。

6. ^"TAXONOMY (Noun) definition and synonyms | Macmillan Dictionary".
6. ^「分類法（名詞）の定義と同義語 | マクミラン辞典」。

7. ^Neshati, Mahmood; Alijamaat, Ali; Abolhassani, Hassan; Rahimi, Afshin; Hoseini, Mehdi (2007). "Taxonomy Learning Using Compound Similarity Measure". IEEE/WIC/ACM International Conference on Web Intelligence (WI'07). pp.487–490. doi:10.1109/WI.2007.135. ISBN 978-0-7695-3026-0. S2CID 14206314.
7. ^Neshati, Mahmood; Alijamaat, Ali; Abolhassani, Hassan; Rahimi, Afshin; Hoseini, Mehdi (2007)。 「複合類似度測定を用いた分類法学習」。IEEE/WIC/ACM国際会議「Web Intelligence」（WI'07）。pp.487–490。doi:10.1109/WI.2007.135。ISBN 978-0-7695-3026-0。S2CID 14206314。

8. ^Brachman, Ronald (October 1983). "What IS-A is and isn't. An Analysis of Taxonomic Links in Semantic Networks". IEEE Computer. 16(10):30–36. doi:10.1109/MC.1983.1654194. OSTI 5363562. S2CID 16650410.
8. ^Brachman, Ronald (1983年10月)。 「IS-Aとは何か、そして何でないのか。意味ネットワークにおける分類的リンクの分析」。IEEE Computer。16(10):30–36。doi:10.1109/MC.1983.1654194。OSTI 5363562。S2CID 16650410。

9. ^Velardi, Paola; Faralli, Stefano; Navigli, Roberto (10 October 2012). "OntoLearn Reloaded: A Graph-based Algorithm for Taxonomy Induction". Computational Linguistics. Association for Computational Linguistics. CiteSeerX 10.1.1.278.5674.
9. ^Velardi, Paola; Faralli, Stefano; Navigli, Roberto (2012年10月10日)。 「OntoLearn Reloaded: 分類法誘導のためのグラフベースのアルゴリズム」。計算言語学。計算言語学会。CiteSeerX 10.1.1.278.5674。

10. ^Liu, Xueqing; Song, Yangqiu; Liu, Shixia; Wang, Haixun (12–16 August 2012). "Automatic taxonomy construction from keywords". Proceedings of the 18th ACM SIGKDD international conference on Knowledge discovery and data mining (PDF). ACM. p.1433. doi:10.1145/2339530.2339754. ISBN 9781450314626. S2CID 9100603. Retrieved 7 March 2017.
10. ^Liu, Xueqing; Song, Yangqiu; Liu, Shixia; Wang, Haixun (2012年8月12–16日)。 「キーワードからの自動分類法構築」。第18回ACM SIGKDD国際会議「知識発見とデータマイニング」の議事録（PDF）。ACM。p.1433。doi:10.1145/2339530.2339754。ISBN 9781450314626。S2CID 9100603。2017年3月7日取得。

11. ^Snow, Rion; Jurafsky, Daniel; Ng, Andrew. "Semantic Taxonomy Induction from Heterogenous Evidence" (PDF). Stanford University. Retrieved 8 March 2017.
11. ^Snow, Rion; Jurafsky, Daniel; Ng, Andrew。「異種証拠からの意味的分類法誘導」（PDF）。スタンフォード大学。2017年3月8日取得。



## Further reading さらなる参考文献
[edit]
[
edit
]
- Automatic Taxonomy Construction from Keywords(2012) 
- Domain taxonomy learning from text: The subsumption method versus hierarchical clustering from Data & Knowledge Engineering, Volume 83, January 2013, Pages 54–69 
- Learning taxonomic relations from a set of text documents 
- Learning Taxonomic Relations from Heterogeneous Sources of Evidence 
- A Metric-based Framework for Automatic Taxonomy Induction 
- A New Method for Evaluating Automatically Learned Terminological Taxonomies 
- Problematizing and Addressing the Article-as-Concept Assumption in Wikipedia 
- Structured Learning for Taxonomy Induction with Belief Propagation 
- Taxonomy Learning Using Word Sense Induction 



## External links 外部リンク
[edit]
[
edit
]
- Taxonomy 101: The Basics and Getting Started with Taxonomies– shows where ATC fits in to the general activity of managing taxonomies for a business enterprise in need of knowledge management.
- タクソノミー101: 基礎とタクソノミーの始め方 - ATCが知識管理を必要とするビジネス企業のタクソノミー管理の一般的な活動にどのように適合するかを示します。
- Natural language processing
- 自然言語処理
- Taxonomy
- タクソノミー
- CS1 errors: missing periodical
- CS1エラー: 欠落している定期刊行物
- Articles with short description
- 短い説明のある記事
- Short description matches Wikidata
- 短い説明がWikidataと一致
- Articles to be expanded from August 2023
- 2023年8月から拡張されるべき記事
- All articles to be expanded
- すべての拡張されるべき記事
- Articles with empty sections from August 2023
- 2023年8月から空のセクションを持つ記事
- All articles with empty sections
- すべての空のセクションを持つ記事
- Articles needing additional references from July 2019
- 2019年7月から追加の参考文献を必要とする記事
- All articles needing additional references
- すべての追加の参考文献を必要とする記事
- This page was last edited on 5 December 2023, at 22:50(UTC).
- このページは2023年12月5日22:50（UTC）に最終編集されました。
- Text is available under the Creative Commons Attribution-ShareAlike 4.0 License; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.
- テキストはクリエイティブ・コモンズ 表示-継承 4.0 ライセンスの下で利用可能です; 追加の条件が適用される場合があります。このサイトを使用することにより、利用規約およびプライバシーポリシーに同意したことになります。Wikipedia®は、非営利団体であるウィキメディア財団の登録商標です。
(UTC)
- Privacy policy
- プライバシーポリシー
- About Wikipedia
- Wikipediaについて
- Disclaimers
- 免責事項
- Contact Wikipedia
- Wikipediaへの連絡
- Legal & safety contacts
- 法的および安全に関する連絡先
- Code of Conduct
- 行動規範
- Developers
- 開発者
- Statistics
- 統計
- Cookie statement
- クッキーステートメント
- Mobile view
- モバイルビュー
-
-
Search
- 検索
Toggle the table of contents
- 目次を切り替える
Automatic taxonomy construction
- 自動タクソノミー構築
Automatic taxonomy construction
- 自動タクソノミー構築
Add languages
- 言語を追加
Add topic
- トピックを追加
