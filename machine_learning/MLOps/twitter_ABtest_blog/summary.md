# Bayesian Personalized Ranking from Implicit Feedback

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf
(勉強会発表者: morinota)

---

n週連続推薦システム系論文読んだシリーズ 36 週目の記事になります。
ちなみに35週目は [タイトル](url) でした!

## どんなもの?

- 読んだきっかけ:
  - Work In ProgressさんのPodcast配信 -> NetflixさんのABテストに関するブログ連載 -> X(旧Twitter)さんのABテストのサンプルサイズ設計に関するブログを読んで、もう少しABテストの設計周りの雰囲気を掴みたいと思い、参考文献に記載されてた本論文を読むに至りました:)_
- 概要:
  - Webサービスにおける制御実験のpracticeやguidelineについてまとめた論文。
- 本記事では、以下の3つの資料を参考にしながら理解したことをまとめつつ、特に推薦システムのABテストに関して思いを馳せる。

## ABテストってどんなものだっけ?

- hoge

## controlled experimentsに関する用語の定義

### Overall Evaluation Criterion (OEC, 総合評価基準):
- 実験を経て改善させたい目的となる定量的な指標 (i.e. netflixさんの資料における primary decision metric?:thinking:)
- 実験によっては複数の目的がある場合もある。その場合は、複数の指標を重み付けして組み合わせた単一のOECを用意することが推奨される。

### Factor

- OECに影響を与えると考えられる、制御可能な実験変数 ()
- factorには値(levelやversionとも呼ばれる)が割り当てられる。
  - (例えばpush通知のパーソナライスするか否かのABテストの場合、factor = is_personalized, value = true or false、みたいな?:thinking:)
- 単純なA/Bテストでは、2つの値(=AとB)を持つ単一のfactorを持つ。

### Variant

- factorにlevel(=値)を割り当てることで、ユーザ体験がテストされる。
  - 既存のバージョンを指定する特別なvariantであるcontrolと、新しいversionを試すvariantであるtreatmentがある。
  - ex) 施策にバグがあった場合、実験は中止され、すべてのユーザがコントロールの variant を割り当てられる。

### Experimental unit (実験単位)

### Null Hypothesis (帰無仮説)

### Confidence level (信頼度)

### Power (検出力)

### A/A test

## 意思決定のためのツールとしての統計的仮説検定





