## 0.1. refs:

- https://www.elastic.co/jp/elasticsearch
- [Vertex AI Feature Store に 機械学習エンジニアが涙した 理由](https://speakerdeck.com/asei/vertex-ai-feature-store-ni-ji-jie-xue-xi-enziniagalei-sita-li-you?slide=23)
- [ZOZOTOWNの検索基盤におけるElasticsearch移行で得た知見](https://techblog.zozo.com/entry/migrating-zozotown-search-platform)
- [データベースとしてのElasticsearch](https://qiita.com/rjkuro/items/95f71ad522226dc381c8#:~:text=%E3%81%A8%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82-,%E5%9F%BA%E6%9C%AC%E7%9A%84%E3%81%AA%E9%81%95%E3%81%84,%E3%83%91%E3%83%95%E3%82%A9%E3%83%BC%E3%83%9E%E3%83%B3%E3%82%B9%E3%81%A8%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%A9%E3%83%93%E3%83%AA%E3%83%86%E3%82%A3%E3%81%8C%E5%BC%B7%E3%81%84%E3%80%82)
- [AWS はお客様のベクトルデータベース要件をどのようにサポートできるか?](https://aws.amazon.com/jp/what-is/vector-databases/#:~:text=AWS%20%E3%81%AF%E3%81%8A%E5%AE%A2%E6%A7%98%E3%81%AE%E3%83%99%E3%82%AF%E3%83%88%E3%83%AB%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E8%A6%81%E4%BB%B6%E3%82%92%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E3%81%A7%E3%81%8D%E3%82%8B%E3%81%8B%3F)
- [NineOCRの改善を⽀えるFeature Store / Feature Store Supporting NineOCR Improvements](https://speakerdeck.com/sansan_randd/feature-store-supporting-nineocr-improvements)

# 1. ElasticSearchとは

## 1.1. 何それ??

- Elasitic社が開発している、様々なユースケースを解決する分散型RESTful検索/分析エンジン
  - 検索だけじゃないんだ...!:thinking:
- OpenSearchとは同じ様なサービス??
  - **OpenSearchはElasticSearchのフォークとして開発された**。AWS手動で、ElasticSearch 7.10.2をベースにしてる。
    - (ともにオープンソースだが、それぞれ異なる方向性で開発がすすむ)
  - OpenSearchをfeature storeとして活用する事例もある(https://speakerdeck.com/sansan_randd/feature-store-supporting-nineocr-improvements?slide=10)

# 2. RDBとの違い:

ともにデータを保存するデータベースとして機能するが色々違いがある。

## 2.1. データの操作方法:

- RDBはSQLを使う。
- ElasticsearchはRESTful APIを使う。

## 2.2. . 機能の多様性:

- RDBは汎用的。
- elastic searchは全文検索に特化している。

## 2.3. . パフォーマンスやスケーラビリティ:

- RDBはデータの整合性を保つために、データの書き込み時にロックをかける。
- Elasticsearchはデータの書き込み時にロックをかけないため、パフォーマンスやスケーラビリティが高い。

## 2.4. 用語の違い:

- RDBではデータベース内に複数のテーブルがあり、テーブル内に行と列がある。
- Elasticsearchでは、**データベース=インデックス、テーブル=マッピングタイプ、行=文書(ドキュメント)、列=フィールド**と呼ぶ。
  - (左側の概念から右側の概念にかけて、入れ子型のイメージ??:thinking:)
  - Elasticsearchにデータを送って格納することを「indexする」や「ingestする」と呼ぶ。(ingestはfeature storeの文脈で使われていたな...!:thinking:)

## 2.5. データベース(i.e. インデックス)の扱いの違い:

- 複数に分割するか否か:
  - RDBではデータベースを複数に分けるケースは少ない。
  - 一方で**Elasticsearchではインデックスを分けるケースが多い**。(ユーザ毎、時系列のデータを時間間隔で区切ったり)
    - search APIも複数インデックスをまたいで実行可能になっている。
- 積極的に削除するか否か:
  - **RDBはマスターデータを半永久的に保管するユーザシナリオが多い**ので、データベースを削除するケースは少ない。
  - **elastic searchは分析や検索用のデータを保管するユーザシナリオが多い**ので、不要になったインデックスを削除するケースは多い。

## 2.6. テキスト処理:

- elastic searchは豊富。tokenizeとか。

## 2.7. 値の持ち方の違い:

- RDBのカラムは基本的にsingle-valuedな挙動。
- 一方で、**elasticsearchのフィールドはmulti-valuedな挙動(暗黙的に配列型)**。
  - 同じデータ型の複数の値を持てる。1個の値は要素数1の配列として扱われる。

## 2.8. デフォルト値の指定方法の違い:

- RDBはカラムに対してデフォルト値を指定できる。(デフォルト値の指定もない場合はNULL)
- 一方、elasticsearchにはデフォルト値がない。
  - その代わり、マッピングタイプ定義でnull_valueというオプションを指定すると、デフォルト値っぽいことができる。

## 2.9. INSERT処理:

## 2.10. UPDATE処理:

## 2.11. DELETE処理:

## 2.12. LOAD処理:

## 2.13. SELECT処理:

## 2.14. GROUPBY処理:

## 2.15. ORDER BY処理:

## 2.16. JOIN、副問合わせ処理:
