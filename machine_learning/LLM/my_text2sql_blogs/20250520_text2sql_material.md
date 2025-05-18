---
format:
  revealjs:
    # incremental: false
    theme: [default, quarto_custom_style_format.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: 我々はなぜまだText2SQLを社内に展開できてない? なぜまだデータ分析業務を効率化・高速化・標準化・民主化できてない?
subtitle: y-tech-ai 勉強会
date: 2025/05/20
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

# はじめに

## Text2SQLとは?? たぶんText2SQLできた方がみんな嬉しいですよね??

## なぜ今回このトピックを喋りたいんだっけ??

- 社内でもちょくちょくText2SQL的なことを試してる様子がある。
- 自分も半年くらい前から自由研究的にText2SQLについて調べたり試したりしてた (実は社内AIコンテストも応募したが課題解決に至っておらず落選...! :pray:)
- なので、情報共有・交換のために「**こういう事例を調査して、こういう思想で、こういうアプローチを採用してみてて、今ここで困ってるんですよ〜...!**」みたいお喋りがカジュアルにできたらいいな〜と思い...!!
- そして最終的には、価値を発揮するText2SQLアプリケーションが自社に展開され、社内のデータ分析業務の効率化・高速化・標準化・民主化が実現されたらいいな〜と思い...!!

## 先に参考文献達を紹介: これらを参考にしてるよ〜

1. 最初に読んだChip HuyenさんのLLMアプリケーション設計思想の記事: [Building A Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html)
2. 真似しまくってるPinterestさんの事例: [How we built Text-to-SQL at Pinterest](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff)
3. メタデータ作る方法を参考にしたメルカリさんの発表資料: [1日50万件貯まるクエリのログを活かして、SQLの生成に挑戦している話](https://speakerdeck.com/__hiza__/1ri-50mo-jian-zhu-marukuerinorokuwohuo-kasite-sqlnosheng-cheng-nitiao-zhan-siteiruhua)
4. LinkedInさんのText2SQL事例: [Practical text-to-SQL for data analytics](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics)
5. UberさんのText2SQL事例: [QueryGPT – Natural Language to SQL Using Generative AI](https://eng.uber.com/using-llms-to-translate-natural-language-to-sql/)
6. (先週読んだ!) UbieさんのText2SQL事例: [Pydantic AIで作る！実践Text-to-SQLシステム構築ガイド 〜自然言語によるデータ抽出の自動化で分析業務を効率化〜](https://zenn.dev/ubie_dev/articles/64cf285988ebe8)


# 本論: 我々はどうしたら価値のあるText2SQL機能を社内展開して、データ分析業務を効率化・高速化・標準化・民主化できるんだろ??

今の所、ざっくり以下の2点の考えに至ってます...! :thinking:

1. クエリ実行履歴とContext Constructionできる基盤さえあれば、一定品質は担保できる感!
2. より価値を発揮するには、ワークフローを制御してあげる必要はありそう。

# 主張1: クエリ実行履歴とContext Constructionできる基盤さえあれば、一定品質は担保できる感!

- 前提としてText2SQLにはcontext constructionが必要
- テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!
- context constructionの精度向上は iterative & incremental にやれば良さそう

## 前提としてContext Constructionできる仕組みは必要

- LLMが事前学習で得た内部知識には、自社のデータベースの情報は一切含まれていない。なので、**各ユーザ質問のために必要な情報を補完できるメカニズム**が必要。
  - このように関連情報を集めることを**Context Construction(文脈構築?)**と呼ぶ。(参考文献1より引用)
  - Context Constructionの具体的な実装の1つが、かの有名な**RAG(retrieval-Augmented Generation)**。
- なので自社にContext Constructionの仕組みがすでにあれば嬉しい。
  - (ちなみに自分の自由研究では、S3 × DuckDB × OpenAI Embedding APIでRAGを実装してた)

![](https://huyenchip.com/assets/pics/genai-platform/3-rag.png)

## テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!1

Text2SQLタスクにおいて利用される共通のcontextは、テーブルメタデータとクエリ実行履歴の2つ。**ここで壁になりそうなのがテーブルメタデータの整備...!**

- Pinterestさんの事例: データガバナンスの取り組みを通じて過去に作られたテーブルメタデータが全体的なパフォーマンスに重要だった
- LinkedInさんの事例: 関連情報を取得する際に「説明文の頻繁な欠如や不完全さ」が課題だった。なので、数百の重要なテーブルの包括的な説明文を収集するために、ドメインエキスパートと協力してdataset certificationを実施した。ドメインエキスパートは重要なテーブルを特定し、必須のテーブル説明文と任意のフィールド説明文を追加。追加した説明文は、**既存の文書やSlackの議論に基づいて生成AIで補完**した。これにより性能が向上した。

各社、メタデータ整備に一定投資してそう。でも、少なくとも自由研究ではそんなに時間かけたくないなぁ...あれ、**LLMでテーブルメタデータを推定**させられるのでは...?? :thinking:

## テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!2

- メルカリさんの事例: 特定のテーブルを参照したクエリの例をLLMに与えて、メタデータを推定させる。

- 以下は実際にNewsPicksのテーブルメタデータをLLMに推定させてみた例:
  - 結構いい感じなんじゃないか??入力したクエリで使われてないカラムは当然含まれない。使われてるカラムは、そこまで間違ってない気がする...!
  - なので**Text2SQLに必要な生データとしては、クエリ実行履歴さえあればある程度できるんじゃないか...??**:thinking:


```json
{
  ""table_name"": ""dynamodb.news"",
  ""summary"": ""ニュース記事に関する情報を保持するテーブル。各ニュース記事の詳細、発行日、著者、関連情報などが含まれる。"",
  ""columns"": [
    {
      ""column_name"": ""news_id"",
      ""column_type"": ""VARCHAR"",
      ""summary"": ""ニュース記事のユニークID""
    },
    {
      ""column_name"": ""title"",
      ""column_type"": ""VARCHAR"",
      ""summary"": ""ニュース記事のタイトル""
    },
    {
      ""column_name"": ""link"",
      ""column_type"": ""VARCHAR"",
      ""summary"": ""ニュース記事の外部リンク""
    },
    {
      ""column_name"": ""published"",
      ""column_type"": ""TIMESTAMP"",
      ""summary"": ""ニュース記事の発行日""
    },
    {
      ""column_name"": ""publisher"",
      ""column_type"": ""VARCHAR"",
      ""summary"": ""ニュース記事を発行した出版社""
    },
    {
      ""column_name"": ""summary"",
      ""column_type"": ""TEXT"",
      ""summary"": ""ニュース記事の要約""
    },
    {
      ""column_name"": ""expired"",
      ""column_type"": ""TIMESTAMP"",
      ""summary"": ""ニュース記事の掲載終了日。NULLの場合は掲載中を示す。""
    },
    {
      ""column_name"": ""user_id"",
      ""column_type"": ""INT"",
      ""summary"": ""ニュース記事を作成したユーザーのID。外部PICKの場合はNULLとなる。""
    }
  ],
  ""sample"": [
    {
      ""query"": ""with _recent_news as (\n    select\n        n.news_id,\n        n.title,\n        n.published,\n        n.publisher\n    from dynamodb.news n\n    where n.published >= current_date - interval '7 days'\n)\nselect\n    r.news_id,\n    r.title,\n    r.published,\n    r.publisher\nfrom _recent_news r\norder by r.published desc;"",
      ""summary"": ""直近7日間に発行されたニュース記事のリストを取得するクエリ。""
    },
    {
      ""query"": ""select\n    n.news_id,\n    n.title,\n    count(re.uid) as pick_count\nfrom dynamodb.news n\njoin reaction_events re on n.news_id = re.news\nwhere n.published >= current_date - interval '30 days'\ngroup by n.news_id, n.title\norder by pick_count desc;"",
      ""summary"": ""過去30日間に発行されたニュース記事の中で、リアクションイベントに基づくピック数を集計するクエリ。""
    },
    {
      ""query"": ""select\n    n.news_id,\n    n.title,\n    na.link\nfrom dynamodb.news n\nleft join news_attributions na on n.news_id = replace(na.content_id, 'N:', '')\nwhere na.publisher = 'NewsPicks編集部';"",
      ""summary"": ""NewsPicks編集部によって発行されたニュース記事とそのリンクを取得するクエリ。""
    },
    {
      ""query"": ""with _expired_news as (\n    select\n        n.news_id,\n        n.title,\n        n.expired\n    from dynamodb.news n\n    where n.expired < current_date\n)\nselect\n    e.news_id,\n    e.title\nfrom _expired_news e\norder by e.expired;"",
      ""summary"": ""掲載終了したニュース記事のリストを取得するクエリ。""
    }
  ]
}
```

## RAGの精度向上は iterative & incremental にやれば良さそう

RAG(i.e. Context Construction)の精度向上に関しては、各社が色々工夫してた。

- Pinterestさん: 
  - LLMにテーブルとサンプルクエリの要約文を生成させてからベクトル化。
  - ベクトルに基づく検索(EBR)の後で、LLMによるテーブル再選択。
- LinkedInさん: 
  - アクセスの人気度に基づいて検索候補テーブルを絞り込み。
  - ユーザの所属チームに基づいて検索結果にパーソナライズ要素を追加。
  - ベクトルに基づく検索(EBR)の後で、LLM & ナレッジグラフによるテーブル再選択。
- Uberさん:
  - ユーザ質問を意図分類し、事前に用意した意図-テーブル集合のmapを使うことで、検索範囲を狭める。
  - 関連テーブルを検索した後で、ユーザに確認を求めるステップを追加。
  - 大規模スキーマを持つテーブルに対応するために、関連カラムのみに切り落とすステップを追加。

まあこのあたりは、必要に応じて段階的にコンポーネントを追加していけば良さそう。
(ちなみに自分の自由研究では、とりあえずPinterestさんの工夫1つ目のみ真似してます)

## 今の自分の自由研究のText2SQLの設計と振る舞いについて

動画を見せる

# 主張2: より価値を発揮するには、ワークフローを制御してあげる必要はありそう

- 品質向上には、context construction以外でもいくつかコンポーネントが必要そう
- LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう
- Text2SQLタスクの場合はそこまでagentic度合いを高くすべきではなさそう

## 品質向上には、context construction以外でもいくつかコンポーネントが必要そう

- hoge

## LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう

- hoge

## Text2SQLタスクの場合はそこまでagentic度合いを高くすべきではなさそう

- hoge

## 今モタモタしちゃってること: どう社内に展開したらいいんだろ??

- hoge

# おわりに


## まとめ

- hoge
