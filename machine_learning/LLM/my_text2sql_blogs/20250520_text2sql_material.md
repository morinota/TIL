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

title: テーブルメタデータが整備できてないことは、我々がText2SQLを社内展開しない理由にはならない
subtitle: y-tech-ai 勉強会
date: 2025/05/20
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

# はじめに

## Text2SQLって? たぶんText2SQLできた方がみんな嬉しいですよね??

- Text2SQL: 自然言語で書かれた質問をSQLクエリに変換する技術。
- 望ましい状況:
  - 社内のデータ分析業務が効率化・標準化・民主化されている。
  - より具体的には、アナリスト&エンジニアの分析業務が効率化・高速化されること。また、普段分析業務に関わらない人でもより簡単に分析ができるようになること(民主化、標準化)。
- 課題感: 
  - LLMは一定普及したが、社内のデータ分析業務は依然としてアナリスト & エンジニアの手作業に依存している。データ分析の知識は属人化している。
  - 「あれ、このデータってどこにあるっけ?」「あの人に聞けばわかるけど、また聞くの気まずいな〜」「なんか最近、同じようなSQL書く時間ばっか増えてる気がする...」「A/Bテストの事後分析ってこれでいいんだっけ?」
- どうしたらText2SQLを社内に導入して、それが価値を発揮し、社内のデータ分析業務を効率化・高速化・標準化・民主化できるのか?? なぜまだ導入できてないのか??

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
5. UberさんのText2SQL事例: [QueryGPT – Natural Language to SQL Using Generative AI](https://www.uber.com/en-JP/blog/query-gpt/)
6. (先週読んだ!) UbieさんのText2SQL事例: [Pydantic AIで作る！実践Text-to-SQLシステム構築ガイド 〜自然言語によるデータ抽出の自動化で分析業務を効率化〜](https://zenn.dev/ubie_dev/articles/64cf285988ebe8)

# 本論: 我々はどうしたら価値のあるText2SQL機能を社内展開して、データ分析業務を効率化・高速化・標準化・民主化できるんだろ??

今の所、ざっくり以下の2点の考えに至ってます...! :thinking:

1. クエリ実行履歴とContext Constructionできる基盤さえあれば、一定品質は担保できる感!
2. より価値を発揮するには、ワークフローを制御してあげる必要はありそう。

# 主張1: クエリ実行履歴とContext Constructionできる基盤さえあれば、一定品質は担保できる感!

- 前提としてContext Constructionできる仕組みは必要
- テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!
- 各社のContext Constructionの精度向上の工夫

## 前提としてContext Constructionできる仕組みは必要

:::: {.columns}

::: {.column width="60%"}

- LLMが事前学習で得た内部知識には、自社のデータベースの情報は一切含まれていない。なので嘘をつくのは当然。
- よってText2SQL機能には、**各ユーザ質問のために必要な情報を補完できるメカニズム**が必要。
  - このように関連情報を集めることを**Context Construction(文脈構築?)**と呼ぶ。(参考文献1より)
  - Context Constructionの具体的な実装の1つが、かの有名な**RAG(retrieval-Augmented Generation)**。
  - 特に参考文献1では、LLMアプリケーションにおけるContext Constructionは、**従来のMLOpsにおける「継続的訓練(Continual Training)」に近いような役割を果たす**、として重要性が主張されてた。
- なので自社にContext Constructionの仕組みがすでにあれば嬉しい。
  - (ちなみに自分の自由研究では、S3 × DuckDB × OpenAI Embedding APIでRAGを実装してた)

:::
::: {.column width="40%"}

![](https://huyenchip.com/assets/pics/genai-platform/2.png)

![](https://huyenchip.com/assets/pics/genai-platform/3-rag.png)

:::
::::

## テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!

Text2SQLタスクにおいて利用される共通のcontextは、テーブルメタデータとクエリ実行履歴の2つ。**ここで壁になりそうなのがテーブルメタデータの整備...!**

- Pinterestさんの事例: **データガバナンスの取り組みを通じて過去に作られたテーブルメタデータ**が全体的なパフォーマンスに重要だった
- LinkedInさんの事例: 関連情報を取得する際に **「説明文の頻繁な欠如や不完全さ」が課題**だった。なので、数百の重要なテーブルの包括的な説明文を収集するために、ドメインエキスパートと協力してdataset certificationを実施した。ドメインエキスパートは重要なテーブルを特定し、必須のテーブル説明文と任意のフィールド説明文を追加。追加した説明文は、既存の文書やSlackの議論に基づいて生成AIで補完した。これにより性能が向上した。

各社、メタデータ整備に一定投資してそう。
以前Snowflakeの人とText2SQL周りで喋った時も、結局はセマンティックレイヤーの整備が重要だと言ってた。
なのでどうしても「うちの会社はまだテーブルメタデータが整備されてないから、Text2SQLはまだ早いかな...」って思ってしまう:thinking:

## テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!

でも**LLMでテーブルメタデータを推定**させられるのでは...?? :thinking:

:::: {.columns}

::: {.column width="50%"}

- 参考文献3のメルカリさんの事例: 特定のテーブルを参照したクエリの例をLLMに与えて、メタデータを推定させてた。

- 実際にLLMに推定させてみると:
  - 結構いい感じなんじゃないか??入力したクエリで使われてないカラムは当然含まれない。使われてるカラムは、そこまで間違ってない気がする...!

:::
::: {.column width="50%"}

![](image.png)

:::
::::

なので**Text2SQLに必要な生データとしては、クエリ実行履歴さえあれば**ある程度できるんじゃないか...??:thinking:

--- 

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

## それらを踏まえて自由研究ではこんなアーキテクチャで実装してみてました!

- Context Constructionの実装として埋め込みベースのRAG(EBR)を採用。
- contextとして、テーブルメタデータとクエリ実行履歴を使用。
- テーブルメタデータは、過去のクエリ実行履歴からLLMに推定させて作成。

:::: {.columns}
::: {.column width="55%"}

![](image-1.png){width=100%}

:::
::: {.column width="45%"}

![](image-2.png){width=100%}

:::
::::

## 各社のContext Constructionの精度向上の工夫

まあこのあたりは、必要に応じて incremental & iterative にコンポーネントを追加して試していけば良さそうかなと思ってます! (ちなみに自分の自由研究では、とりあえずPinterestさんの工夫1つ目のみ真似してます:hand:)

- Pinterestさん: 
  - LLMにテーブルとサンプルクエリの要約文を生成させてからベクトル化して検索インデックス登録。
  - ベクトルに基づく検索(EBR)の後で、LLMによるテーブル再選択ステップを追加。
- LinkedInさん: 
  - アクセスの人気度に基づいて検索候補テーブルを絞り込み。
  - ユーザの所属チームに基づいて検索結果にパーソナライズ要素を追加。
  - ベクトルに基づく検索(EBR)の後で、LLM & ナレッジグラフによるテーブル再選択。
- Uberさん:
  - ユーザ質問を意図分類し、事前に用意した意図-テーブル集合のmapを使うことで、検索範囲を狭める。
  - 関連テーブルを検索した後で、ユーザに確認を求めるステップを追加。
  - 大規模スキーマを持つテーブルに対応するために、関連カラムのみに切り落とすステップを追加。

## 今の自分の自由研究のText2SQLの設計と振る舞いについて

動画を見せる

# 主張2: より価値を発揮するには、ワークフローを制御してあげる必要はありそう

- 品質向上には、context construction以外にもいくつかコンポーネントが必要そう
- LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう
- Text2SQLタスクの場合は、そこまでagentic度合いを高くすべきではなさそう...!

## 品質向上には、context construction以外にもいくつかコンポーネントが必要そう

各社の事例では、context construction以外にもいくつかコンポーネントを追加してる

::::{ .columns}
:::{ .column width="40%"}


- Pinterestさん: 
  - こちらは1年以上前の事例だからか、**RAGで一度生成したSQLをそのままユーザに返してた**。
  - なのでそんなに追加コンポーネントはない!
  - 今後の課題として、LLM-as-a-judge的に反復的なSQL生成プロセスを検討してるとのこと。

:::
:::{ .column width="60%"}

![](image-3.png){width=100%}

:::
::::

## 品質向上には、context construction以外でもいくつかコンポーネントが必要そう


:::: { .columns}
:::{ .column width="40%"}

- LinkedInさん: 
  - RAGの手前で、**ユーザ質問を意図分類するコンポーネント** (ex. テーブル検索なのか、参考クエリが欲しいのか、SQLを書いてほしいのか, etc.)
  - 生成されたSQLを評価するコンポーネントで、**LLM-as-a-judge的に反復的なSQL生成プロセス**を採用してる (DWHから実行計画などを取得し、問題があればSQL生成コンポーネントにフィードバックを送る)。

:::

:::{ .column width="60%"}

![alt text](image-4.png)

:::
::::


## 品質向上には、context construction以外でもいくつかコンポーネントが必要そう


:::: { .columns}
:::{ .column width="40%"}


- Uberさん:
  - 初期バージョンはPinterestさんと(i.e. 自由研究と)ほぼ同様の構成!(かなりシンプルなRAG!)
  - 対応テーブルの増加 & 大規模スキーマを持つ(カラム数が多い)テーブルに対応するために、だんだんと追加コンポーネントを増やしていったとのこと。
    - Intent Agent (LLMによる意図分類)
    - Table Agent (ユーザ自身によるretrieve結果の補正)
    - Column Prune Agent (LLMによる不要なカラムの切り落とし)
  - SQL生成後のvalidationやLLM-as-a-judge的な反復的なSQL生成プロセスは採用してない。
  - Text2SQLの継続的改善のための評価方法が参考になった。

:::
:::{ .column width="60%"}

![](image-5.png)

:::
::::

## 品質向上には、context construction以外でもいくつかコンポーネントが必要そう

- Ubieさん:
  - 生成されたSQLを評価するコンポーネント。
  - 生成されたSQLを実行し、最終的な分析結果を整形するコンポーネント。

![](image-7.png)

## LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう1

- 最終的な回答はSQLクエリ? それともSQLクエリを実行して得た分析結果??
  - 前者: Pinterestさん, LinkedInさん, Uberさん
  - 後者: Ubieさん
- AgenticなLLMシステムにどれくらいのアクション権限を与えるかの話:
  - AgenticなLLMシステムにおいて、モデルが呼び出すツール(i.e. アクション)は**read-only actions**と**write actions**に分類できる(参考文献1より引用)。
    - read-only actions: 外部ソースから情報を取得するが、状態を変更しないアクション
    - write actions: 状態を変更するアクション。
  - **LLMにwrite actionsを許可することは、LLMアプリケーションをはるかに強力にするが、より多くのリスクも伴う**。
    - インターンに本番データベースを削除する権限を与えてはいけないように、信頼性のないAIに銀行振込を開始させてはいけない。
    - model jailbreakやprompt injection対策を行い、有害なアクションを実行させようとする悪質なユーザからシステムを守る必要がある。

## LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう2

- LLMにSQL実行権限を与える場合は、どんなリスクを考慮すべきだろ?? :thinking:
  - delete文やupdate文などを生成して実行しちゃうリスク
  - 計算がめっちゃ重いselect文を生成して実行しちゃって、お金が溶ける or DB負荷が上がるリスク
  - prompt injectionは社内アプリだからあんまり気にしなくて大丈夫かな。
- LLMにSQL実行権限を与えるなら、あんまりLLMのAgentic度合いは高くない方がいいかも。生成したSQLをきちんと評価・検証してから実行するようなワークフロー制御はあった方が良さそう...!:thinking:
  - 少なくとも、これまで述べてきた各種コンポーネントをそれぞれツール化して、LLMがそれらを自由な順番に呼び出せるようにする、というのは
  - 例えば、関連テーブル・サンプルクエリを取得するRAG用(retrieve用)MCPサーバーと、DWHにアクセスできるMCPサーバーを用意して、それをgithub copilotが自由に呼べるようにする。これだけだとリスクが大きいよね...!:thinking:
  - 各事例でもワークフロー制御してる感 (LLM自身がAgenticに判断する部分は、LinkedInさんの意図分類コンポーネントくらいかも)

## Text2SQLタスクの場合はそこまでagentic度合いを高くすべきではなさそう

- hoge

## 今モタモタしちゃってること: どう社内に展開したらいいんだろ??

- 現在は簡単のため、Context Construction部分をMCPサーバーとして実装して、VSCodeのCopilotから呼べるようにしてる。

# おわりに


## まとめ

- hoge
