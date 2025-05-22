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

title: テーブルメタデータが整備できてないことは、たぶん我々がText2SQLを諦める理由にはならない
subtitle: Context Constructionの仕組みとクエリ実行履歴でベースラインを作ろう!
date: 2025/05/20
author: morinota y-tech-ai 勉強会
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
- どうしたらText2SQLを社内に導入して、それが価値を発揮し、社内のデータ分析業務をより効率化・高速化・標準化・民主化できるのか?? なぜまだ導入できてないのか??

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

# 本論: 我々はどうしたらText2SQLで価値を発揮できるのか??

今の所、ざっくり以下の2点の考えに至ってます...! :thinking:

1. クエリ実行履歴とContext Constructionの仕組みさえあれば、一定品質は担保できる感!
2. より価値を発揮するには、ワークフローを制御してあげる必要はありそう。

# 主張1: クエリ実行履歴とContext Constructionの仕組みさえあれば、一定品質は担保できる感!

- 前提としてContext Constructionの仕組みは必要
- テーブルメタデータは整備されてなくてもクエリ実行履歴さえあればなんとかなる感...!
- 各社のContext Constructionの精度向上の工夫

## 前提としてContext Constructionの仕組みは必要

:::: {.columns}

::: {.column width="60%"}

- LLMが事前学習で得た内部知識には、自社のデータベースの情報は一切含まれていない。なので嘘をつくのは当然。
- よってText2SQL機能には、**各ユーザ質問のために必要な情報を補完できるメカニズム**が必要。
  - このように関連情報を集めることを**Context Construction(文脈構築?)**と呼ぶ。(参考文献1より)
  - Context Constructionの具体的な実装の1つが、かの有名な**RAG(retrieval-Augmented Generation)**。
  - 特に参考文献1では、LLMアプリケーションにおけるContext Constructionは、**従来のMLOpsにおける「継続的訓練(Continual Training)」に近いような役割を果たす**、として重要性が主張されてた。
- なので自社にContext Constructionの仕組みがすでにあれば結構嬉しい。
  - (ちなみに自分の自由研究では、S3 × DuckDB × OpenAI Embedding APIでRAGを実装してた)

:::
::: {.column width="40%"}

![](https://huyenchip.com/assets/pics/genai-platform/2.png)

![](https://huyenchip.com/assets/pics/genai-platform/3-rag.png)

:::
::::

## でもcontextとしてテーブルメタデータが整備されてないと...

Text2SQLタスクにおいて利用される共通のcontextは、テーブルメタデータとクエリ実行履歴の2つ。**ここで壁になりそうなのがテーブルメタデータの整備...!**

- Pinterestさんの事例: **データガバナンスの取り組みを通じて過去に作られたテーブルメタデータ**が全体的なパフォーマンスに重要だった
- LinkedInさんの事例: 関連情報を取得する際に **「説明文の頻繁な欠如や不完全さ」が課題**だった。なので、数百の重要なテーブルの包括的な説明文を収集するために、ドメインエキスパートと協力してdataset certificationを実施した。ドメインエキスパートは重要なテーブルを特定し、必須のテーブル説明文と任意のフィールド説明文を追加。追加した説明文は、既存の文書やSlackの議論に基づいて生成AIで補完した。これにより性能が向上した。

上記の通り、各社メタデータ整備に一定投資してるっぽい。
以前Snowflakeの人とText2SQL周りで喋った時も、結局はセマンティックレイヤーの整備が重要だと言ってた。

なのでどうしても「**うちの会社はまだテーブルメタデータが整備されてないから、Text2SQLは早いかな...**」って思ってしまう:thinking:

## クエリ実行履歴さえあればベースラインは作れそう!

でも**LLMでテーブルメタデータを推定**させられるのでは...?? :thinking:

:::: {.columns}

::: {.column width="50%"}

- 参考文献3のメルカリさんの事例: 特定のテーブルを参照したクエリの例をLLMに入力として与えて、テーブルメタデータを推定させてた。

- 実際にLLMに推定させてみると...
  - 結構いい感じなんじゃないか??
  - 入力したクエリで使われてないカラムは当然含まれない。
  - 使われてるカラムは、そこまで間違ってない気がする...!

:::
::: {.column width="50%"}

![](image.png)

:::
::::

なのでText2SQLに必要な生データとして、**クエリ実行履歴さえあればベースラインを作れるのでは..!!**:thinking:

(PinterestさんでもLinkedInさんでも、**テーブルメタデータ整備が完了してからText2SQLを導入したわけではない**...!)

## それらを踏まえて自由研究ではこんなアーキテクチャで実装してみてました!

- Context Constructionの実装として埋め込みベースのRAG(EBR)を採用。
- RAGの検索対象は、テーブルメタデータとクエリ実行履歴(サンプルクエリ)。
- テーブルメタデータは、過去のクエリ実行履歴からLLMに推定させて作成。

:::: {.columns}
::: {.column width="55%"}

![](image-1.png){width=100%}

:::
::: {.column width="45%"}

![](image-2.png){width=100%}

:::
::::

## 余談: 各社のContext Constructionの精度向上の工夫

まあこのあたりは、**必要に応じて incremental & iterative にコンポーネントを追加して試していけば良さそうかな**と思ってます! (ちなみに自分の自由研究では、とりあえずPinterestさんの工夫1つ目のみ真似してます:hand:)

- Pinterestさん: 
  - **LLMにテーブルとサンプルクエリの要約文を生成させてからベクトル化して検索インデックス登録**。
  - ベクトルに基づく検索(EBR)の後で、LLMによるテーブル再選択ステップを追加。
- LinkedInさん: 
  - アクセスの人気度に基づいて検索候補テーブルを絞り込み。
  - ユーザの所属チームに基づいて検索結果にパーソナライズ要素を追加。
  - ベクトルに基づく検索(EBR)の後で、LLM & ナレッジグラフによるテーブル再選択。
- Uberさん:
  - ユーザ質問を意図分類し、事前に用意した意図-テーブル集合のmapを使うことで、検索範囲を狭める。
  - 関連テーブルを検索した後で、ユーザに確認を求めるステップを追加。
  - 大規模スキーマを持つテーブルに対応するために、関連カラムのみに切り落とすステップを追加。

# 主張2: より価値を発揮するには、ワークフローを制御してあげる必要はありそう

- 品質向上には、context constructionに加えていくつかコンポーネントが必要そう
- LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう
- Text2SQLタスクの場合は、そこまでagentic度合いを高くすべきではなさそう...!

## 品質向上には、context constructionに加えていくつかコンポーネントが必要そう

各社の事例では、context constructionに加えて、いくつかのコンポーネントを追加して精度向上を図っている様子があった。

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

## 品質向上には、context constructionに加えていくつかコンポーネントが必要そう


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


## 品質向上には、context constructionに加えていくつかコンポーネントが必要そう


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

## 品質向上には、context constructionに加えていくつかコンポーネントが必要そう

- Ubieさん:
  - 生成されたSQLを評価するコンポーネントで、**LLM-as-a-judge的に反復的なSQL生成プロセス**を採用。
  - 評価後に、**生成されたSQLを実際に実行して結果を取得**し、回答を整形してユーザに返す。

![](image-7.png)

## LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう

データ分析の民主化の観点では、LLMにSQL生成だけじゃなく、**SQL実行させて分析結果をまとめて返してくれた方がきっと便利**。

- AgenticなLLMシステムにどれくらいのアクション権限を与えるかの話(参考文献1より)
  - AIのAgentic、Agentらしさの定義: 「LangGraph」のドキュメントによると...”**LLMがアプリケーションの制御フローを決定すること**”
  - AgenticなLLMシステムにおいて、モデルが呼び出すツール(i.e. アクション)は**read-only actions**と**write actions**に分類できる。
    - read-only actions: 外部ソースから情報を取得するが、状態を変更しないアクション
    - write actions: 状態を変更するアクション。
  - **LLMにwrite actionsを許可することは、LLMアプリケーションをはるかに強力にするが、より多くのリスクも伴う**。
    - インターンに本番データベースを削除する権限を与えてはいけないように、信頼性のないAIに銀行振込を開始させてはいけない。
    - prompt injection対策を行い、有害なアクションを実行させようとする悪質なユーザからシステムを守る必要がある。
  
LLMにSQL実行権限を与えることも同様に、**Text2SQLアプリケーションをはるかに強力にするが、より多くのリスクも伴う**はず...!:thinking: 

## LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう

じゃあText2SQLアプリにSQL実行権限を与える場合は、どんなリスクを考慮すべきだろ?? :thinking:

- delete文やupdate文などを生成して実行しちゃうリスク
- 計算がめちゃ重いselect文を生成して実行して、お金が溶ける or DB負荷が上がるリスク
- (prompt injectionは社内アプリだからあんまり気にしなくて大丈夫そう)

LLMにSQL実行権限を与えるなら上記のリスクを対策すべき。生成したSQLをきちんと評価・検証してから実行するようなワークフロー制御はあった方が良さそう...!:thinking:

- 各事例でもワークフロー制御してる感 (LLM自身がAgenticに判断する部分は、LinkedInさんの意図分類コンポーネントくらいかも)
- 例えば、RAG用(retrieve用)MCPサーバーと、DWHにアクセスできるMCPサーバーを用意して、両ツールをgithub copilotが自由に呼べるようにする。これだけだとリスクが大きい...!:thinking:

## 余談: UberさんのText2SQLの継続的改善のための評価方法がしっかりしてて参考になる感...!

- Text2SQLのパフォーマンスの漸進的な改善を追跡するために、**標準化された評価手順が必要**。
- 評価用セット(典型的なユーザ質問-ゴールデンSQLのペア)を用意。
- 採用してるパフォーマンスmetricsたち:
  - Intent (意図分類の予測精度)
  - Table Overlap (関連テーブルのretrieve精度)
  - Successful Run (生成されたクエリの実行は成功するか否か)
  - Run Has Output (クエリの実行は0件を超えるレコードを返すか否か)
  - Qualitative Query Similarity (ゴールデンSQLとの定性的なクエリ類似性)
    - **LLMを使用して0から1の間の類似性スコアを割り当てる**。
    - このmetricsにより、構文エラーで失敗している生成クエリが、**使用される列、結合、適用される関数などの観点から正しい方向に進んでいるかどうか**を迅速に確認できる。
- 監視方法: 定期的に評価用セットに対するパフォーマンスmetricsを計算・追跡。
- Text2SQL評価における制限事項:
  - LLMの推論は確率論的 (i.e. 非決定論的) な性質を持つ。Uberでは**metricsの5%の変動では一喜一憂しない**。
  - 評価用セットが自社の全ての分析業務のドメインをカバーするのは無理なので、新しいバグの発見されるにつれて評価用セットを更新していく。
  - 常に正しい答えが一つだけあるわけではない。ある程度はQualitative Query Similarityでカバーできる。

## 余談: Uberさん事例の学び: LLMは優れた分類器である

- Uberさんの事例では、最初のバージョン (シンプルなRAG) に、様々な中間エージェント(=分類タスクを解くLLM) を追加することでText2SQLの精度を向上させていったとのこと。
  - 意図分類, テーブル再選択, カラム切り落とし
  - それらはすべてLLMに分類タスクを解かせることで実現してた。
- 上手く機能した理由は、**それぞれが広範な一般化されたタスクではなく、単一の作業単位に取り組むように求められたから**。

<!-- ## 余談: 今モタモタしちゃってること: どう社内に展開したらいいんだろ??

現在は簡単のため、Context Construction部分をMCPサーバーとして実装して、VSCodeのCopilotから呼べるようにしてる (今日PRリリースしました!:hand:)

::::{ .columns}
:::{ .column width="55%"}

![](image-8.png){width=100%}

:::
:::{ .column width="45%"}


- ただ今後、さらに価値を発揮できるように**RAG以外のコンポーネントも連結していくとしたら、この提供方法でいいのかな?** 一連のワークフローを1つのツールに梱包して提供する?? 
- **更に、エンジニア以外のメンバーにはどう提供したらいいんだろ??**
  - webアプリケーションとして提供する?? Slackボットとして提供する?? 社内のLLM schatbotが呼び出せるMCPサーバーとして提供する??

まだ自分のソフトウェアエンジニアリング力が不足してるので、社内への展開方法に苦戦中...!:crying_cat_face:
 
::: 
:::: -->

## まとめ

- LLMは一定普及したが、社内のデータ分析業務は依然としてアナリスト & エンジニアの手作業に依存してるし、データ分析の知識は属人化している。なぜText2SQLはまだ導入できないのか??
- 多くの場合、**自社のテーブルメタデータが整備されてないことが壁になってる**。そこで諦めがち。
- でも、**クエリ実行履歴とContext Constructionの仕組みさえあれば**、一定品質は担保できる感! 
- そこをベースラインとして社内展開した後、FBをもらいながら徐々に、コンポーネントを追加したりテーブルメタデータを整備していけば良いのでは...!!

テーブルメタデータが整備できてないことは、たぶん我々がText2SQLを諦める理由にはならないはずだ...!!:thinking:

## (再掲) 参考文献

1. 最初に読んだChip HuyenさんのLLMアプリケーション設計思想の記事: [Building A Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html)
2. 真似しまくってるPinterestさんの事例: [How we built Text-to-SQL at Pinterest](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff)
3. メタデータ作る方法を参考にしたメルカリさんの発表資料: [1日50万件貯まるクエリのログを活かして、SQLの生成に挑戦している話](https://speakerdeck.com/__hiza__/1ri-50mo-jian-zhu-marukuerinorokuwohuo-kasite-sqlnosheng-cheng-nitiao-zhan-siteiruhua)
4. LinkedInさんのText2SQL事例: [Practical text-to-SQL for data analytics](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics)
5. UberさんのText2SQL事例: [QueryGPT – Natural Language to SQL Using Generative AI](https://www.uber.com/en-JP/blog/query-gpt/)
6. (先週読んだ!) UbieさんのText2SQL事例: [Pydantic AIで作る！実践Text-to-SQLシステム構築ガイド 〜自然言語によるデータ抽出の自動化で分析業務を効率化〜](https://zenn.dev/ubie_dev/articles/64cf285988ebe8)
