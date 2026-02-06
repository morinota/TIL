## Metadata
name: 技術記事をブログdraftに変換
description: 技術論文や技術ブログ記事を読み、個人ブログのdraftを作成する

## Overview

技術論文や技術ブログ記事を読み、個人ブログのdraftを作成するスキル。

## 使用方法

記事のURLまたはローカルファイルパスを指定してください:

```
/tech-blog-to-draft https://example.com/article
```

または

```
/tech-blog-to-draft path/to/article.md
```

## draft作成の方針

- 記事の要点を日本語で整理
- 構造:
  - タイトル(日本語訳または要約)
  - 元記事情報(著者、日付、URL)
  - 内容の要約と重要なポイント
  - 技術的な詳細
  - 学びや考察
- マークダウン形式で出力
- コードブロックや図表は適宜引用
