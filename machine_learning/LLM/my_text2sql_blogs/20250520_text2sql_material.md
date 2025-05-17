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

## なぜ今回このトピックを喋りたいんだっけ??

- 社内でもちょくちょくText2SQL的なことを試してる様子がある。
- 自分も半年くらい前から自由研究的にText2SQLについて調べたり試したりしてた(実は社内AIコンテストもText2SQLで応募したが実力不足で落選...!)。
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

1. Context Constructionできる基盤さえあれば、一定品質は担保できる感!
2. より価値を発揮するには、ワークフローを制御してあげる必要はありそう。

# 主張1: Context Constructionできる基盤さえあれば、一定品質は担保できる感!

- hoge

## 前提としてcontext constructionは必要

- hoge

## テーブルメタデータ整備はとりあえず頑張りすぎなくて良さそう

- hoge

## context constructionの精度向上は iterative & incremental にやれば良さそう

- hoge

# 主張2: より価値を発揮するには、ワークフローを制御してあげる必要はありそう

- hoge  

## 品質向上には、context constructionの前後で色んなコンポーネントが必要そう

- hoge

## context constructionの前の追加コンポーネント例

- hoge

## context constructionの後の追加コンポーネント例

- hoge

## LLMにSQL実行権限を与えたい場合は特に、ワークフローを制御してしっかり検証させてあげたほうが良さそう

- hoge

## Text2SQLタスクの場合はそこまでagentic度合いを高くすべきではなさそう

- hoge

# 今モタモタしちゃってること: どう社内に展開したらいいんだろ??

- hoge

# おわりに


## まとめ

- hoge
