## link

- https://recbole.io/docs/user_guide/data_intro.html

# Data Module Introduction

- RecBoleは多くの一般的な推薦モデルを実装しているだけでなく、よく使われる28の公開データセットを収集し、公開している。
  - 各データセットは、[データセットダウンロード](https://recbole.io/docs/user_guide/data/dataset_download.html)のドキュメントに従って自由にダウンロードできる。
  - ダウンロード方法は３つ。
- 拡張性と再利用性のために、Recboleには柔軟で拡張可能な`data`モジュールがある。
  - Recboleの`data`モジュールは、生データをモデル入力に変換するエレガントなデータフローを設計する。
  - データフローとして**様々な推薦タスクが必要とする入力データのほとんどの形式を共通化する**ために、RecBoleは**アトミックファイルと呼ばれる入力データ形式**を設計する。
  - **すべての入力データはアトミックファイル形式に変換されなければならない**。
  - また、異なる推薦アルゴリズムに統一的な内部データ表現を提供するために、 `Interaction` と呼ばれるデータ構造を設計する。
- RecBoleは、explicit feedback(ラベル付きデータ)とimplicit feedback(ラベルなしデータ)の両方をサポートする。
  - explicit feedbackを扱う場合、開発者はconfigで`LABEL_FIELD`を設定することができ、RecBoleはそのラベルに基づいてモデルの訓練とテストを行う。
  - implicit feedbackを扱う場合、RecBoleは観測された全ての相互作用をpositiveサンプルとみなし、観測されていない相互作用から自動的にnegativeサンプルを選択する。
    - (これは負のサンプリングとして知られている。)
    - RecBoleのラベル設定についての詳細は、[Label of data](https://recbole.io/docs/user_guide/data/label_of_data.html)をお読みください。

## Dataset Download

- RecBoleは多くの一般的な推薦モデルを実装しているだけでなく、よく使われる28の公開データセットを収集し、公開している。
  - 各データセットは、[データセットダウンロード](https://recbole.io/docs/user_guide/data/dataset_download.html)のドキュメントに従って自由にダウンロードできる。
  - ダウンロード方法は以下の3つ。

### 方法1: Automatiacally downloading

- RecBoleでは、利便性向上のため、**自動ダウンロードモジュール**を実装し、一般に公開されている28のデータセットのアトミックファイルをダウンロードできるようにした。。
  - データセットを指定してモデルを実行したい場合、データセットを設定するだけで、自動的に対象のアトミックファイルがダウンロードされる。
  - 例えば、ml-1mデータセットでBPRモデルを実行したいが、ml-1mデータセットのAtomic Filesを用意していない場合、自動ダウンロードモジュールを使ってデータをダウンロードすることができる。
    - RecBoleは自動的にデータファイルがあるかどうかをチェックし、なければダウンロードを開始する。

### 方法2: クラウドdeskから手動でダウンロード

- 自動ダウンロードの他に、Google DriveとBaidu Wangpan (Password: e272)に、収集・変換した28データセットのatomicファイルをアップロードしている。
- この2つのリソースから手動でデータをダウンロードできる。

### 方法3: ユーザが用意したraw dataから変換する

- すでに生データをダウンロードしている場合は、自分で原子ファイル形式に変換することもできる。
- すでに[RecDatasets](https://github.com/RUCAIBox/RecDatasets)でいくつかの変換スクリプトを公開している。(自作データセットを使う場合は、この変換スクリプトを参考にすれば良さそう。)

## DataFlow
