## refs:

- [公式website](https://recsys.eb.dk/)
- [dataset description](https://recsys.eb.dk/dataset.html)

## これはなに?

- RecSys Challenge 2024のデータセットの概要。

# Ekstra Bladet News Recommendation Dataset(EB-NeRD)の概要:

- ニュース推薦研究の進展を支援するために作成されたデータセット。
- Ekstra Bladetはデンマークの新聞社。
- 2023年4月27日から6月8日までの6週間、アクティブユーザの行動ログを収集したもの。
  - このtimeframeは、非定型的な行動を誘発する可能性がある、祝日や選挙などの大きなイベントを避けるために選ばれた。
  - アクティブユーザの定義: 2023年5月18日から6月8日までの3週間で、ニュースのクリック記録が少なくとも5回、多くとも1000回あったユーザ。

# Dataset Format

- 3種類の大きさのdataset bundleがある:
  - demo
  - small
  - large
- 各bundleには、training setとvalidation setが含まれる。
  - 各data separationには、2つのファイルが含まれる。
    - 1. `behaviors.parquet`: ユーザの7日間のimpressionログ。
    - 2. `history.parquet`: ユーザの28日間のクリック履歴。
      - (behaviorsログの前にクリックされた記事達。historyはbehaviorsログよりも前の期間に固定されている)
      - data separation期間内では更新されない(training setとvalidation set間で同じってこと??)
- 4種類のparquetファイル。(3, 4はdata separation間で共通のファイル)
  - 1. behaviors.parquet: 7日間のユーザのimpressionログ。
  - 2. history.parquet: 28日間のユーザのクリック履歴。
  - 3. articles.parquet: 各記事のメタデータ。
  - 4. artifacts.parquet: 各記事のartifact(成果物??), ex. 記事の埋め込みや画像の埋め込みなど。(要は、独自のモデルによって生成された特徴量...!:thinking:)

# 各データの概要

## behaviors.parquet

-

## history.parquet

## articles.parquet

## artifacts.parquet
