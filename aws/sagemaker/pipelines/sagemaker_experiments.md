## refs

- https://qiita.com/mariohcat/items/9fde1b04c0ecf439d427
- コネヒト柏木さんのブログ [SageMaker Experimentsを使った機械学習モデルの実験管理](https://tech.connehito.com/entry/2021/12/15/181332)
- マネーフォワードさんのブログ [SageMaker Experimentsによる実験管理とQuickSightを使ったその可視化](https://moneyforward-dev.jp/entry/2021/08/20/sagemaker-experiments/)

# Sagemaker Experimentsって?

何度も無駄な実験を繰り返さないため、また振り返ったときにわかるように、実験管理はきちんとしようね、という気持ち...!

> Amazon SageMaker Experiments is a capability of Amazon SageMaker that lets you organize, track, compare, and evaluate your machine learning experiments.

- 機械学習モデルの再現性を担保するために必要な情報 (versioningや学習のtracking, 比較, 評価など) を収集して管理できる機能。記録をGUI上から確認できる。
  - (Sagemaker Experimentsは、Sagemaker Studioと連携してるので、Studio上の画面から確認できる)
  - MLはiterativeな実験が必要になるが、何度もモデル学習を行っていると、どのモデルが性能が良くて、その時のハイパーパラメータや評価指標の値が何で、設定はどうだったかなど、きちんと管理しておかないとわからなくなる。

## なぜSagaMaker Experimentsを使うのか?

- 他のOSS製品の実験管理ツールもあるよね、MLflowとか。
- なぜSagemaker Experimentsを使うのか?

  - 1. AWSの各種サービスをMLプロジェクトで使用しており、それらと相性が良い。
  - 2. 再現性に必要なメタデータを管理できて、それを簡単にチームで共有できること。
    - 前半部分は、他のOSS製品でもできる。
    - 後半部分は、例えばMLflowはトラッキング用サーバを立てる必要があったりする、それを別途管理・運用する必要が出てくる。

- 若干物足りない or 使いづらい部分:

  - 1. 実験後の結果に対して，どうゆう実験内容だったかなどのコメントを入れることができない。
    - (そうなの?? 2024年現在は改善されてたりするかな...:thinking:)
  - 2. 実装方法がSageMakerのフレームワークに則る必要があり，その理解に時間がかかる。
    - (これはどのフレームワークでもそうだよね。お作法は存在するし。)

## Sagemaker Experimentsの概念

上から順番に上位の概念になっている。

- 1. **Experiment**:
  - 最上位の概念。1つのプロジェクトに相当する。
  - 一度作成すると、同一名称では作成できないっぽい。
    - UIから削除できないので注意が必要。(コマンド実行で削除できるが、下の階層にあるデータを削除してからでないとExperimentを削除できないらしい...!)
- 2. **Trial**:
  - Experiment内での実験の試行を表す。
  - (実験実行時のtimestamp毎につくってるイメージ)
- 3. **TrialComponent**:
  - Trialの中に複数のTrialComponentが存在する。
  - (実験タスク内のフェーズ毎に分けるイメージ。前処理/学習/評価など)

## Experimentsを使った実験管理

- Sagemaker Experiments SDKをインストールする必要がある。
  - `pip install sagemaker-experiments`
  - でも2024年現在では、Sagemaker Python SDKを使えばいいのかも...! どうやら今は統合されてるっぽい...!:thinking:

# ちなみに情報たち

## (ちなみに) Sagemaker ProcessingJobと比較したTrainingJobの利点??

コネヒト柏木さんのブログより:

> 現在，毎日レコメンドエンジンの学習が回っており，それをStep Functionsのパイプラインで実行しています．その際に**SageMaker CreateProcessingJobを使っているのですが，これだと実験管理が十分にできないため，それをTraining Jobに置き換えて実行するというもの**です．これによりExperimentsに情報を蓄積できるため学習のログを簡単に可視化したり，オンラインのビジネス指標と比較したりすることもできます．

- これって、2024年現在でもそうなのかな。Sagemaker ProcessingJobとExperimentsの連携が弱い状況って...!

## (ちなみに) Experiement Analyticsクラスを使うと、tracking情報をpd.DataFrameとして取得できる。

- なのでこれを活用すると、Sagemaer Experimentsでtrackingした情報を、Sagemaker Studio以外の任意の環境で使えたりする。
  - 参考: マネーフォワードさんのブログ [SageMaker Experimentsによる実験管理とQuickSightを使ったその可視化](https://moneyforward-dev.jp/entry/2021/08/20/sagemaker-experiments/)
