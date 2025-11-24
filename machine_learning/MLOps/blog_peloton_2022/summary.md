# context-awareなrecsysを構築した教訓ブログを読んだメモ

## これは何??

- Peloton社さん(フィットネスに関するプロダクトを提供する企業)のブログ記事 を読んで感想などをメモしたもの。
  - [Lessons Learned from Building out Context-Aware Recommender Systems](https://www.onepeloton.com/press/articles/lessons-learned-from-building-context-aware-recommender-systems)
- 元々は協調フィルタリングベースの推薦モデル(LSTMNet)を運用してたが、今回新たに**コンテキスト情報を活用した推薦システム(Context-Aware Recommender Systems: CARS)**に移行した際の教訓をまとめて下さってるブログ記事。
  - 共感できる点も多く、かなり参考になりました...!! 圧倒的感謝...!:pray:
  
## 背景: プロダクトの推薦システムにおけるコンテキスト考慮の重要性の話

- hoge

## 現行モデルの制限: 協調フィルタリングベースの推薦モデル(LSTMNet)

- hoge

## Context-Awareな推薦システムがどのように動作するか

- hoge

## Context-Awareな推薦システムの真価を発揮するために: バッチ推論からオンライン推論への移行

- hoge

## 得られた教訓

### 教訓1: end-to-endのiterationをできるだけ迅速に行う

- hoge

### 教訓2: 評価への投資(Invest in Evaluation)

- hoge

### 教訓3: 実験トラッキングツールへの投資(Invest in Experiment Tracking Tools)

- hoge

### 教訓4:　より良いインフラの信頼性がより良い開発者体験をもたらす

- hoge

## 今後の改善計画

- context-awareな推薦モデルを、コンテンツリスト(rows of content)の生成に活用する。
  - hoge
- マルチタスク的な学習設定で、複数の目的を同時に最適化する。
  - hoge
