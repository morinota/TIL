## refs:

- [【MLOps】「いつか使いたい！」と思っていた人のためのMLflowまとめ](https://qiita.com/c60evaporator/items/e0eb1a0c521d1310d95d)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)

# MLflowの概要

## 機能:

以下の4つの機能からなる。

- MLflow Tracking:実験管理
- MLflow Projects:コード管理
- MLflow Models:デプロイ支援
- MLflow Model Registry:モデルのバージョン管理

- ちなみに、**MLflowは一般的な意味でのオーケストレーションツールとは言えない**っぽい...!
  - バッチ処理や定期実行のスケジューリング機能は持たないので。
    - MLflowは、依存関係を持つタスク集合のスケジューリングや実行のオーケストレーション（自動調整と管理）は扱わない。
  - 一般的なオーケストレーションツール(Orchestrator)が持つ機能:
    - 1. 複数のタスクやプロセス間の依存関係の管理: 依存関係のあるプロセス間の実行順序を保証する。
    - 2. スケジューリング: プロセスの実行時刻や条件を管理する。
    - 3. リソース管理: プロセスの実行に必要なリソースの割当やスケーリングを自動的に行う。
    - 4. 失敗の回復: プロセスの失敗時にリトライやエラー処理を行う機能を提供。
    - (これらを踏まえると、やっぱりdigdagはorcherstratorなんだな～)

# MLflow Trackingについて

## 実験管理の使用手順:

- 1. 管理したい情報の洗い出し
- 2. トラッキングサーバの構築:
- 3. Experimentの作成
- 4. 実験結果のlogging
- 5. 結果表示UIの立ち上げ

## 手順1: 管理したい情報の洗い出し

公式documentによると、記録したい情報を以下のように分類してる:

- 1. code version(コードバージョン)
- 2. Start & End time(記録を開始&終了した時刻)
- 3. Source(MLflow Project情報)
- 4. Tags(モデルの種類名やバージョン情報などのkey-value)
- 5. Parameters(性能に寄与するハイパーパラメータなどの実験条件)
- 6. Metrics(性能を測定するための指標)
  - ex. 精度スコア、処理時間
  - 確かに処理時間大事...!:thinking_face:
- 7. Artifacts(上記以外に保持したい任意のファイル情報)
  - ex. CSVファイル、画像、MLモデルのpickleファイルなど。
  - (定性評価の推薦記事リストなどは、Artifactsとして管理すると良いかも...! :thinking_face:)

実験管理という目的であれば、最重要はParametersとMetricsの情報だが、その他の情報も合わせて管理すると後追いがしやすい...!

## 手順2: トラッキングサーバの構築

MLflowによる実験管理を実現する為には、以下の4種類の機構を整備する必要がある。

- 1. Tracking Server:
  - ex. EC2やECSなどのクラウド上のサーバ。
- 2. Backend Store:
  - ParametersやMetricsの情報を保存。
  - ex. ファイルストレージ、S3、DBなど。
  - 詳細は[link](https://qiita.com/c60evaporator/items/e1fd57a0263a19b629d1#%E3%83%90%E3%83%83%E3%82%AF%E3%82%A8%E3%83%B3%E3%83%89)
- 3. Artifact Storage:
  - Artifactsを保存。
  - ex. ファイルストレージ、S3、DBなど。
- 4. Registry server:
  - モデルとバージョン情報を保持。(MLflow Model Registryの設定が必要)
  - ex. ファイルストレージ、S3、DBなど。
  - (レジストリサーバはトラッキングサーバと同一とする事が多いので、残りの3種類が特に重要らしい)

公式documentによると、以下の4種類のシナリオが紹介:

1. MLflow on localhost:
   - tracking server = ローカルに自動生成
   - backend store = ローカルストレージ
   - artifact store = ローカルストレージ
2. MLflow on localhost with SQLite:
   - tracking server = ローカルに自動生成
   - backend store = SQLite(ローカルDB)
   - artifact store = ローカルストレージ
3. MLflow on localhost with Tracking Server:
   - tracking server = ローカルに手動ホスティング
   - backend store = SQLite(ローカルDB) or ローカルストレージ
   - artifact store = ローカルストレージ
4. MLflow with remote Tracking Server, backend and artifact stores:
   - tracking server = リモートサーバ
   - backend store = リモートDB
   - artifact store = リモートストレージ

おすすめは、個人開発ならシナリオ2, チーム開発ならシナリオ4らしい。
何もしないとシナリオ1がデフォルトで選択されるらしい。

## 手順3: Experimentの作成

- MLflowでは実験をグルーピングして管理できる。-> このグルーピング単位 = Experimentと呼ぶ。
  - ex. プロジェクト毎にExperimentを分ける。
- Tracking serverの構築方法によって、Experiment作成時に関連するArtifact storeやbackend storeの設定が必要か否かが異なる。

## 手順4: 実験結果のlogging

手順1で決めた情報を実際に記録する。
この操作がTrackingを実行する部分。

- MLflowにおいて、記録したい1回の実験の事を **Run** と呼ぶ。

  - (Experimentの中に複数の Runがあるようなイメージ:thinking_face:)

- 手順1: Runを開始する
  - `mlflow.start_run(experiment_id=experiment_id)`
  - with構文を使うと便利らしい。
- 手順2: loggingを実施する
  - 記録したい情報の種類毎(手順1で示した7種類の情報)に異なるメソッドが用意されている。
    - ちなみに、同じMetricsを複数回連続で記録する事もできる。この機能は学習時のEpchなど、スコアの推移を見たい場合を想定してるみたい。
- 手順3: Runを終了する
  - `mlflow.end_run()`
  - with構文を使う場合は明示的にend_run()を呼ぶ必要はないらしい。

## 手順5: 結果表示UIの立ち上げ

- MLflow には、記録(tracking)した結果をブラウザ上で表示する機能がある。
- 内部的にはWebサーバを起動することになるが、以下のコマンドで立ち上げることができる。
- 手順2で選択した各シナリオによって方法が異なる。
  - シナリオ1,2については、コンソールからコマンドを実行する。
  - シナリオ3,4については、Dockerfileに`mlflow server`コマンドが記述済みなので、コンソール側からなにか操作する必要はない。
  - ブラウザから`http://[リモートサーバのIP]:500`にアクセスすると、結果表示UIが立ち上がる。

# MLflow Projectsについて

# MLflow Modelsについて

# MLflow Model Registryについて
