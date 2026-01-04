## これは何??

- 特徴量エンジニアリングの一種であるHashing Trick(Feature Hashing)について調べたメモ。

## refs:

- 日本語記事: [ロジスティック回帰に対するFeature Hashingの影響](https://qiita.com/tyoshitake/items/0b18f02a85db45b455cf)
  - **one-hotエンコーディングした137次元の特徴量ベクトルを、Hashing Trickで40~130次元に圧縮しても精度低下は(0.835 - (0.82~0.83)) = 0.005程度に抑えられる**、という実験結果。同記事では、「次元を1/3程度に圧縮しても精度がそこまで落ちないなら、計算コスト次第では有効な手段になり得る」と明言しており、カテゴリ数が数百~数千になると有効性が更に高まるとコメントしてる。
- Booking.com データサイエンス組織のテックブログ: [Don’t be tricked by the Hashing Trick](https://booking.ai/dont-be-tricked-by-the-hashing-trick-192a6aae3087)
- [機械学習処理におけるカテゴリ変数の扱い方(Feature hashingについて)](https://developers.microad.co.jp/entry/2018/12/07/184133#Feature-hashing%E3%81%A8%E3%81%AF)

## Hashing Trick(Feature Hashing)とは? 最初にざっくりメモ:

- **巨大なカテゴリ特徴量を、さくっと低次元ベクトルに押し込むための手法**。
  - 目的が共通する手法として、one-hotエンコーディング, multi-hotエンコーディング, entity embeddingなどがある。
- 特徴量をハッシュ関数に通して、その値をベクトルのインデックスとして使う。

## Hashing Trickの仕組み

例えば、以下のようなカテゴリ特徴量があったとする。

```
特徴量名 | 職種 | 趣味
社員A | 営業 | 釣り
社員B | デザイナー | サッカー
社員C | エンジニア | 盆栽
```

one-hotエンコーディングを使うと、以下のように変換される。

```
# 右から順に、"職種__営業", "職種__デザイナー", "職種__エンジニア", "趣味__釣り", "趣味__サッカー", "趣味__盆栽"の順番
社員A = [1, 0, 0, 1, 0, 0] 
社員B = [0, 1, 0, 0, 1, 0]
社員C = [0, 0, 1, 0, 0, 1]
```

Feature Hashingの場合は、ハッシュ関数を用いてカテゴリ変数データを指定した次元のベクトルに圧縮する。
例えば、社員Aのデータを `{"職種": "営業", "趣味": "釣り"}`と表現する。

## feature hashingのバリエーション

- 全てのカテゴリ特徴量たちで共通の空間を利用するか否かで、以下の2種類に分類できる。
  - global hashing space
  - per-field hashing space
