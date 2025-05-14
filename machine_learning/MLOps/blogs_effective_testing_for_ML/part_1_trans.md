<!-- 読む! --> 

## link リンク

https://towardsdatascience.com/effective-testing-for-machine-learning-part-i-e6b5aeb51421
https://towardsdatascience.com/effective-testing-for-machine-learning-part-i-e6b5aeb51421

# Effective Testing for Machine Learning (Part I) A progressive, step-by-step framework for developing robust ML projects Effective Testing for Machine Learning (Part I) ロバストなMLプロジェクト開発のための段階的フレームワーク

This blog post series describes a strategy I’ve developed over the last couple of years to test Machine Learning projects effectively.
このブログ記事シリーズでは、機械学習プロジェクトを効果的にテストするために私がここ数年で開発した戦略について説明する。
Given how uncertain ML projects are, this is an incremental strategy that you can adopt as your project matures; it includes test examples to provide a clear idea of how these tests look in practice, and a complete project implemented with Ploomber is available on GitHub.
MLプロジェクトがいかに不確実であるかを考えると、これはプロジェクトが成熟するにつれて採用できる漸進的な戦略である。これらのテストが実際にどのように見えるかを明確にするためのテスト例が含まれており、Ploomberで実装された完全なプロジェクトがGitHubで利用可能である。
By the end of the post, you’ll be able to develop more robust ML pipelines.
この投稿が終わる頃には、より堅牢なMLパイプラインを開発できるようになっていることだろう。

## Challenges when testing ML projects MLプロジェクトをテストする際の課題

Testing Machine Learning projects is challenging.
機械学習プロジェクトのテストは難しい。
Training a model is a long-running task that may take hours to run and has a non-deterministic output, which is the opposite we need to test software: quick and deterministic procedures.
モデルのトレーニングは、実行に数時間かかることもある長時間のタスクであり、非決定論的な出力を持つ： 迅速で決定論的な手順である。
One year ago, I published a post on testing data-intensive projects to make Continuous Integration feasible.
1年前、私は継続的インテグレーションを実現するためのデータ集約型プロジェクトのテストに関する投稿を発表した。
I later turned that blog post into a talk and presented it at PyData 2020.
その後、そのブログ記事を講演にまとめ、PyData 2020で発表しました。
But such previous work only covered generic aspects of testing data pipelines and left out testing ML models.
しかし、そのような以前の研究は、データパイプラインのテストの一般的な側面をカバーするだけで、MLモデルのテストは除外されていた。

It’s important to clarify that testing and monitoring are two different things.
テストとモニタリングは別物であることを明確にすることが重要だ。
Testing is an offline process that allows us to evaluate whether our code does what it’s supposed to do (i.e., produce a high-quality model).
テストはオフラインのプロセスであり、コードがやるべきことをやっているかどうか（つまり高品質のモデルを生成できるかどうか）を評価することができる。
In contrast, monitoring involves inspecting a deployed model to ensure it works correctly.
対照的に、モニタリングでは、デプロイされたモデルが正しく動作するかどうかを検査する。
Thus, testing happens before deployment; monitoring occurs after deployment.
したがって、テストは配備前に行われ、モニタリングは配備後に行われる。

I use the terms pipeline and task throughout the post.
この記事の中では、パイプラインとタスクという言葉を使っている。
A task is a unit of work (usually a function or a script); for example, one task can be a script that downloads the raw data, and another could clean such data.
たとえば、あるタスクは生データをダウンロードするスクリプトであり、別のタスクはそのようなデータをクリーニングすることができる。
On the other hand, a pipeline is just a series of tasks executed in a pre-defined order.
一方、パイプラインは、あらかじめ定義された順序で実行される一連のタスクに過ぎない。
The motivation for building pipelines made of small tasks is to make our code more maintainable and easier to test; that lines up with the goal of our open-source framework to help data scientists build more maintainable projects using Jupyter.
小さなタスクで構成されるパイプラインを構築する動機は、コードの保守性を高め、テストを容易にすることである。これは、Jupyterを使用してデータ科学者がより保守性の高いプロジェクトを構築できるようにするという、我々のオープンソース・フレームワークの目標に合致している。
In the following sections, you’ll see some sample Python code; we use pytest, pandas, and Ploomber.
以下のセクションでは、Pythonのサンプルコードを紹介する。pytest、pandas、Ploomberを使用する。

If you’d like to know when the second part is out, subscribe to our newsletter, follow us on Twitter or LinkedIn.
後編がいつ出るか知りたい方は、ニュースレターを購読するか、ツイッターかリンクトインでフォローしてください。

## Parts of a Machine Learning pipeline 機械学習パイプラインのパーツ

Before we describe the testing strategy, let’s analyze how a typical ML pipeline looks.
テスト戦略を説明する前に、典型的なMLパイプラインがどのように見えるかを分析してみよう。
By analyzing each part separately, we can clearly state its role in the project and design a testing strategy accordingly.
各パーツを個別に分析することで、プロジェクトにおける役割を明確にし、それに応じてテスト戦略を設計することができる。
A standard ML pipeline has the following components:
標準的なMLパイプラインには、次のような構成要素がある：

Feature generation pipeline.
フィーチャー生成パイプライン。
A series of computations to process raw data and map each data point to a feature vector.
生データを処理し、各データ点を特徴ベクトルにマッピングする一連の計算。
Note that we use this component at training and serving time.
なお、このコンポーネントはトレーニング時とサーブ時に使用する。

Training task.
トレーニングの課題。
Takes a training set and produces a model file.
トレーニングセットを受け取り、モデルファイルを生成する。

Model file.
モデルファイル。
The output from the training task.
トレーニングタスクからの出力。
It’s a single file that contains a model with learned parameters.
これは、学習されたパラメータを持つモデルを含む単一のファイルである。
In addition, it may include pre-processors such as scaling or one-hot encoding.
さらに、スケーリングやワンホットエンコーディングなどのプリプロセッサーが含まれることもある。

Training pipeline.
トレーニングのパイプライン
Encapsulates the training logic: get raw data, generate features, and train models.
学習ロジックをカプセル化します： 生データを取得し、特徴を生成し、モデルを訓練する。

Serving pipeline.
パイプラインを提供する。
(also known as inference pipeline) Encapsulates the serving logic: gets a new observation, generates features, passes features through the model, and returns a prediction.
(推論パイプラインとも呼ばれる）サービングロジックをカプセル化する： 新しいオブザベーションを取得し、特徴を生成し、特徴をモデルに通し、予測を返す。

## What can go wrong? 何が問題なのか？

To motivate our testing strategy, let’s enumerate what could go wrong with each part:
テスト戦略のモチベーションを高めるために、各パーツで何が問題なのかを列挙してみよう：

Feature generation pipeline
フィーチャー生成パイプライン

Cannot run the pipeline (e.g., setup problems, broken code).
パイプラインを実行できない（セットアップの問題、壊れたコードなど）。

Cannot reproduce a previously generated training set.
以前に生成されたトレーニングセットを再現できない。

Pipeline produces low-quality training data.
パイプラインは低品質のトレーニングデータを生成する。

Training task
トレーニング課題

Cannot train a model (e.g., missing dependencies, broken code).
モデルをトレーニングできない（依存関係がない、コードが壊れているなど）。

Running the training task with high-quality data produces low-quality models.
高品質のデータでトレーニングタスクを実行すると、低品質のモデルが生成される。

Model file
モデルファイル

The generated model has a lower quality than our current model in production.
生成されたモデルは、現在生産しているモデルよりも品質が低い。

The model file does not integrate correctly with the serving pipeline.
モデルファイルがサービングパイプラインと正しく統合されない。

Serving pipeline
パイプライン

Cannot serve predictions (e.g., missing dependencies, broken code).
予測を提供できない（依存関係がない、コードが壊れているなど）。

Mismatch between preprocessing at training and serving time (aka training-serving skew).
トレーニング時の前処理とサーブ時の前処理のミスマッチ（別名、トレーニング-サーブスキュー）。

Outputs a prediction when passing invalid raw data.
無効な生データが渡された場合に予測を出力する。

Crashes when passed valid data.
有効なデータを渡されるとクラッシュする。

Note that this isn’t an exhaustive list, but it covers the most common problems.
これは完全なリストではないが、最も一般的な問題をカバーしていることに注意してほしい。
Depending on your use case, you may have other potential issues, and it’s vital to list them to customize your testing strategy accordingly.
あなたのユースケースによっては、他にも潜在的な問題があるかもしれない。

## Testing strategy テスト戦略

When developing ML models, the faster we iterate, the higher the chance of success.
MLモデルを開発する場合、反復が早ければ早いほど、成功する確率は高くなる。
Unlike traditional software engineering projects where it’s clear what we should build (e.g., a sign-up form), ML projects have a lot of uncertainty: Which datasets to use? What features to try? What models to use? Since we don’t know the answer to those questions in advance, we must try a few experiments and evaluate whether they yield better results.
何を作るべきかが明確な従来のソフトウェアエンジニアリングのプロジェクト（例えば、サインアップフォーム）とは異なり、MLプロジェクトは不確定要素が多い： どのデータセットを使うか？どのデータセットを使うか？どんなモデルを使うべきか？どのデータセットを使うか？どの機能を試すか？どのモデルを使うか？これらの質問に対する答えを事前に知ることはできないので、いくつかの実験を試し、より良い結果が得られるかどうかを評価しなければならない。
Because of this uncertainty, we have to balance iteration speed with testing quality.
このような不確実性があるため、反復のスピードとテストの質のバランスを取らなければならない。
If we iterate too fast, we risk writing sloppy code; if we spend too much time thoroughly testing every line of code, we won’t improve our models fast enough.
反復のスピードが速すぎると、杜撰なコードを書いてしまう危険性がある。また、コード1行1行を徹底的にテストすることに時間をかけすぎると、モデルの改良が十分に進まなくなる。

This framework steadily increases the quality of your tests.
このフレームワークは、テストの質を着実に高めてくれる。
The strategy consists of five levels; when reaching the last level, you have robust enough testing that allows you to push new model versions to production confidently.
この戦略は5つのレベルで構成されている。最後のレベルに達したとき、新バージョンのモデルを自信を持って生産に投入できる十分なテストが行われていることになる。

## Testing levels テストレベル

Smoke testing.
スモークテスト。
We ensure our code works by running it on each git push.
gitプッシュのたびにコードを実行することで、私たちのコードが機能することを確認しています。

Integration testing and unit testing.
統合テストと単体テスト。
Test task’s output and data transformations.
タスクの出力とデータ変換をテストする。

Distribution changes and serving pipeline.
配給の変更とパイプラインの提供
Test changes in data distributions and test we can load a model file and predict.
データ分布の変化をテストし、モデルファイルをロードして予測できるかをテストする。

Training-serving skew.
トレーニングに奉仕するスキュー。
Test that the training and serving logic is consistent.
トレーニングとサービングのロジックが一貫していることをテストする。

Model quality.
モデル・クオリティ。
Test model quality.
モデルの品質をテストする。

## Quick introduction to testing in with pytest pytest を使ったテストの簡単な紹介

If you’ve used pytest before, you may skip this section.
以前にpytestを使ったことがある場合は、このセクションは飛ばしてもかまいません。

Tests are short programs that check whether our code is working.
テストは、コードが機能しているかどうかをチェックする短いプログラムである。
For example:
例えば、こうだ：

A test is a function that runs some code, and asserts its output.
テストは、あるコードを実行し、その出力をアサートする関数である。
For example, the previous file has two tests: test_add and test_substract, organized in a file called test_math.py; it's usual to have one file per module (e.g., test_math.py tests all functions in a math.py module).
例えば、前のファイルには2つのテストがあります： test_addとtest_substractの2つのテストがあり、test_math.pyというファイルにまとめられています。
Testing files usually go under a tests/ directory:
テスト・ファイルは通常、tests/ディレクトリの下に置かれる：

Testing frameworks such as pytest allow you to collect all your tests, execute them and report which ones fail and which ones succeed:
pytestのようなテストフレームワークでは、すべてのテストを収集し、実行し、どれが失敗し、どれが成功したかを報告することができます：

A typical project structure looks like this:
典型的なプロジェクト構造は次のようなものだ：

src/ contains your project's pipeline's tasks and other utility functions.
src/には、プロジェクトのパイプラインのタスクやその他のユーティリティ関数が含まれています。
exploratory/ includes exploratory notebooks and your tests go into the tests/ directory.
exploratory/は探索ノートブックを含み、テストはtests/ディレクトリに入ります。
The code in src/ must be importable from the other two directories.
src/にあるコードは、他の2つのディレクトリからインポートできなければならない。
The easiest way to achieve this is to package your project.
これを実現する最も簡単な方法は、プロジェクトをパッケージ化することだ。
Otherwise, you have to fiddle with sys.path or PYTHONPATH.
そうでなければ、sys.pathやPYTHONPATHをいじらなければならない。

## How to navigate the sample code サンプルコードの見方

Sample code is available here.
サンプルコードはこちら。
The repository has five branches, each implementing the testing levels I’ll describe in upcoming sections.
リポジトリには5つのブランチがあり、それぞれがこれから説明するテストレベルを実装している。
Since this is a progressive strategy, you can see the evolution of the project by starting from the first branch and moving up to the following branches.
これは漸進的な戦略なので、最初のブランチから始めて、次のブランチに進むことで、プロジェクトの進化を見ることができる。

The project implements the pipeline using Ploomber, our open-source framework.
このプロジェクトでは、オープンソースのフレームワークであるPloomberを使ってパイプラインを実装している。
Hence, you can see the pipeline specification in the pipeline.yaml file.
したがって、pipeline.yamlファイルでパイプラインの仕様を見ることができる。
To see which commands we're using to test the pipeline, open .github/workflows/ci.yml, this is a GitHub actions configuration file that tells GitHub to run certain commands on each git push.
パイプラインのテストに使っているコマンドを確認するには、.github/workflows/ci.yml を開きましょう。これは GitHub のアクション設定ファイルで、git push のたびに特定のコマンドを実行するように GitHub に指示します。

While not strictly necessary, you may want to check out our Ploomber introductory tutorial to understand the basic concepts.
厳密には必要ではないが、Ploomber入門チュートリアルをチェックして、基本的なコンセプトを理解しておくとよいだろう。

Note that the code snippets displayed in this blog post are generic (they don’t use any specific pipeline framework) because we want to explain the concept in general terms; however, the sample code in the repository uses Ploomber.
一般的な用語でコンセプトを説明したいので、このブログ記事で表示されるコード・スニペットは一般的なもの（特定のパイプライン・フレームワークを使用していない）であることに注意してください。

## Level 1: Smoke testing レベル1 スモークテスト

Sample code available here.
サンプルコードはこちら。

Smoke testing is the most basic level of testing and should be implemented as soon as you start a project.
スモークテストはテストの最も基本的なレベルであり、プロジェクトを開始したらすぐに実施すべきである。
Smoke testing does not check the output of your code but only ensures that it runs.
スモークテストは、コードの出力をチェックするのではなく、コードの実行を確認するだけである。
While it may seem too simplistic, it’s much better than not having tests at all.
単純すぎると思われるかもしれないが、テストをまったくしないよりはずっといい。

Documenting dependencies
依存関係の文書化

Listing external dependencies is step zero when starting any software project, so ensure you document all the dependencies needed to run your project when creating your virtual environment.
外部依存関係をリストアップすることは、どのようなソフトウェア・プロジェクトを開始する際にも必要なステップであるため、仮想環境を作成する際には、プロジェクトの実行に必要な依存関係をすべて文書化しておく必要がある。
For example, if using pip, your requirements.txt file may look like this:
例えば、pipを使用する場合、requirements.txtファイルは次のようになります：

After creating your virtual environment, create another file ( requirements.lock.txt) to register installed versions of all dependencies.
仮想環境を作成したら、別のファイル（requirements.lock.txt）を作成し、すべての依存関係のインストール済みバージョンを登録します。
You can do so with the pip freeze > requirements.lock.txt command (execute it after running pip install -r requirements.txt), which generates something like this:
pip freeze > requirements.lock.txtコマンド（pip install -r requirements.txtを実行した後に実行する）を使えば、次のようなものが生成される：

Recording specific dependency versions ensures that changes from any of those packages do not break your project.
特定の依存バージョンを記録することで、それらのパッケージからの変更がプロジェクトを壊さないようにする。

Another important consideration is to keep your list of dependencies as short as possible.
もうひとつ重要な考慮点は、依存関係のリストをできるだけ短くすることだ。
There’s usually a set of dependencies you need at development time but not in production.
通常、開発時には必要だが生産時には必要ない依存関係がある。
For example, you may use matplotlib for model evaluation plots, but you don't need it to make predictions.
例えば、モデルの評価プロットにはmatplotlibを使うかもしれないが、予測をするのには必要ない。
Splitting your development and deployment dependencies is highly recommended.
開発とデプロイの依存関係を分割することを強く推奨する。
Projects with a lot of dependencies increase the risk of running into version conflicts.
依存関係の多いプロジェクトでは、バージョンの衝突に遭遇するリスクが高まる。

Testing feature generation pipelines
機能生成パイプラインのテスト

One of the first milestones in your project must be to get an end-to-end feature generation pipeline.
プロジェクトの最初のマイルストーンのひとつは、エンド・ツー・エンドのフィーチャー生成パイプラインを手に入れることだ。
Write some code to get the raw data, perform some basic cleaning, and generate some features.
生データを取得し、基本的なクリーニングを行い、いくつかの特徴を生成するコードを書く。
Once you have an end-to-end process working, you must ensure that it is reproducible: delete the raw data and check that you can re-run the process and get the same training data.
エンド・ツー・エンドのプロセスが機能したら、それが再現可能であることを確認しなければならない： 生データを削除し、プロセスを再実行し、同じトレーニングデータが得られることを確認する。

Once you have this, it’s time to implement our first test; run the pipeline with a sample of the raw data (say, 1%).
生データのサンプル（例えば1%）でパイプラインを実行する。
The objective is to make this test run fast (no more than a few minutes).
目的は、このテストを速く（数分以内に）実行することである。
Your test would look like this:
テストは次のようになる：

Note that this is a basic test; we’re not checking the output of the pipeline! However, this simple test allows us to check whether the code runs.
これは基本的なテストであり、パイプラインの出力をチェックしているわけではないことに注意してほしい！しかし、この単純なテストによって、コードが実行されるかどうかをチェックすることができます。
It’s essential to run this test whenever we execute git push.
git pushを実行する際には、必ずこのテストを実行する必要がある。
If you're using GitHub, you can do so with GitHub Actions, other git platforms have similar features.
GitHubを使用している場合は、GitHub Actionsで行うことができます。他のgitプラットフォームにも同様の機能があります。

Testing the training task
トレーニング課題のテスト

After generating features, you train a model.
特徴を生成した後、モデルを訓練する。
The training task takes a training set as an input and outputs a model file.
トレーニング・タスクはトレーニング・セットを入力とし、モデル・ファイルを出力する。
Testing the model training procedure is challenging because we cannot easily define an expected output (model file) given some input (training set) — mainly because our training set changes rapidly (i.e., add, remove features).
というのも、ある入力（トレーニングセット）が与えられたときに、期待される出力（モデルファイル）を簡単に定義することができないからだ。
So, at this stage, our first test only checks whether the task runs.
したがって、この段階では、最初のテストはタスクが実行されるかどうかをチェックするだけである。
Since we disregard the output (for now), we can train a model with a sample of the data; remember that this smoke test must execute on every push.
出力は（今のところ）無視するので、データのサンプルでモデルを訓練することができる。このスモークテストは、プッシュするたびに実行しなければならないことを覚えておいてほしい。
So let’s extend our previous example to cover feature generation and model training:
それでは先ほどの例を拡張して、特徴生成とモデル・トレーニングについて説明しよう：

In the sample repository, we are using Ploomber, so we test the feature pipeline and training task by calling ploomber build, which executes all tasks in our pipeline.
サンプルリポジトリではPloomberを使用しているので、パイプラインのすべてのタスクを実行するploomber buildを呼び出して、特徴パイプラインとトレーニングタスクをテストします。

## Level 2: Integration testing and unit testing レベル 2： 統合テストと単体テスト

Sample code available here.
サンプルコードはこちら。

It’s essential to modularize the pipeline in small tasks to allow us to test outputs separately.
アウトプットを個別にテストできるようにするためには、パイプラインを小さなタスクにモジュール化することが不可欠だ。
After implementing this second testing level, you achieve two things:
この2つ目のテストレベルを実施すると、2つのことが達成される：

Ensure that the data used to train the model meets a minimum quality level.
モデルの訓練に使用するデータが、最低限の品質レベルを満たしていることを確認する。

Separately test the portions of your code that have a precisely defined behavior.
動作が正確に定義されているコード部分は、個別にテストする。

Let’s discuss the first objective.
最初の目的について説明しよう。

Integration testing
統合テスト

Testing data processing code is complicated because its goal is subjective.
データ処理コードのテストは、その目的が主観的であるために複雑である。
For example, imagine I ask you to test a function that takes a data frame and cleans it.
例えば、データフレームを受け取ってそれをクリーニングする関数をテストするように頼んだとしよう。
How would you test it? The idea of data cleaning is to improve data quality.
どのようにテストしますか？データクリーニングの考え方は、データの質を向上させることだ。
However, such a concept depends on the specifics of the data and your project.
しかし、このようなコンセプトは、データとプロジェクトの仕様に依存する。
Hence, it’s up to you to define the clean data concept and translate that into integration tests, although in this case, we can use the term data quality tests to be more precise.
したがって、クリーンデータのコンセプトを定義し、それを統合テストに反映させるのはあなた次第だ。

The idea of integration testing applies to all stages in your pipeline: from downloading data to generating features: it’s up to you to define the expectations at each stage.
統合テストの考え方は、パイプラインのすべての段階に当てはまります： データのダウンロードから機能の生成まで： 各段階で期待されることを定義するのはあなた次第です。
We can see a graphical representation of integration testing in the following diagram:
統合テストを図式化すると以下のようになる：

For example, to add integration tests to a data cleaning function (let’s call it clean), we run a few checks at the end of the function's body to verify its output quality.
例えば、データクリーニング関数（cleanと呼ぶことにする）に統合テストを追加するために、関数本体の最後にいくつかのチェックを実行し、その出力品質を検証する。
Common checks include no empty values, numerical columns within expected ranges or categorical values within a pre-defined set of values:
一般的なチェックには、空の値がないこと、数値列が予想される範囲内にあること、カテゴリ値があらかじめ定義された値の範囲内にあることなどが含まれます：

This form of testing is different than the one we introduced in the first section.
このテスト形式は、最初のセクションで紹介したものとは異なる。
Unit tests exist in the tests/ folder and can run independently, but integration tests run when you execute your training pipeline.
ユニットテストは tests/ フォルダに存在し、独立して実行できますが、統合テストはトレーニングパイプラインを実行するときに実行されます。
Failing tests mean your data assumptions do not hold, and data assumptions must be re-defined (which implies updating your tests accordingly), or your cleaning procedure should change to ensure your tests pass.
テストが不合格になるということは、データの仮定が成立していないということであり、データの仮定を再定義しなければならない（これは、それに応じてテストを更新することを意味する）か、テストが合格するようにクリーニング手順を変更しなければならない。

You can write integration tests without any extra framework by adding assert statements at the end of each task.
各タスクの最後にassert文を追加することで、余計なフレームワークなしで統合テストを書くことができる。
However, some libraries can help.
しかし、図書館の中には助けてくれるところもある。
For example, Ploomber supports running a function when a task finishes.
例えば、Ploomberはタスクの終了時に関数を実行することをサポートしている。

Here’s the implementation of an integration test in our sample repository.
以下は、サンプルリポジトリでの統合テストの実装です。

Unit testing
ユニットテスト

Within each task in your pipeline (e.g., inside clean), you'll likely have smaller routines; such parts of your code should be written as separate functions and unit tested (i.e., add tests in the tests/ directory).
パイプラインの各タスクの中（たとえばcleanの中）には、より小さなルーチンがあるはずだ。コードのそのような部分は、別の関数として書き、ユニットテストを行うべきだ（つまり、tests/ディレクトリにテストを追加する）。

A good candidate for writing unit tests is when applying transformations to individual values in a column.
単体テストを書くのに適しているのは、カラム内の個々の値に変換を適用する場合である。
For example, say that you’re using the heart disease dataset and create a function to map the chest_pain_type categorical column from integers to their corresponding human-readable values.
例えば、心臓病データセットを使って、chest_pain_type カテゴリカル・カラムを整数から対応する人間が読める値にマップする関数を作るとします。
Your clean function may look like this:
クリーン・ファンクションは次のようになる：

Unlike the general clean procedure, transform.chest_pain_type has an explicit, objectively defined behavior: it should map integers to the corresponding human-readable values.
一般的なクリーンプロシージャとは異なり、transform.chest_pain_typeには明示的かつ客観的に定義された動作がある： それは、整数を対応する人間が読める値にマップすることである。
We can translate this into a unit test by specifying the inputs and the expected outputs.
入力と期待される出力を指定することで、これをユニットテストに変換することができる。

Unit testing must be a continuous stream of work on all upcoming testing levels.
単体テストは、今後予定されているすべてのテスト・レベルにおいて、継続的な作業の流れでなければならない。
Therefore, whenever you encounter a piece of logic with a precise objective, abstract it into a function and test it separately.
したがって、正確な目的を持ったロジックに出会ったときは、それを関数に抽象化し、個別にテストする。

Here’s an implementation of a unit test in the sample repository.
サンプルリポジトリにあるユニットテストの実装です。

## References 参考文献

Heart disease dataset retrieved from the UC Irvine Machine Learning repository, distributed under a CC BY 4.0 license.
UC Irvine Machine Learningリポジトリから取得した心臓病データセット。CC BY 4.0ライセンスの下で配布されている。

## Up next 次へ

So far, we’ve implemented a basic strategy that ensures that our feature generation pipeline produces data with a minimum level of quality (integration tests or data quality tests) and verifies the correctness of our data transformations (unit tests).
これまでは、特徴生成パイプラインが最低限の品質を持つデータを生成することを保証し（統合テストまたはデータ品質テスト）、データ変換の正しさを検証する（ユニットテスト）基本戦略を実装してきた。
In the next part of this series, we’ll add more robust tests: test for distribution changes, ensure that our training and serving logic is consistent, and check that our pipeline produces high-quality models.
このシリーズの次のパートでは、より堅牢なテストを追加する： ディストリビューションの変更をテストし、トレーニングとサービングのロジックが一貫していることを確認し、パイプラインが高品質のモデルを生成することをチェックします。

If you’d like to know when the second part is out, subscribe to our newsletter, follow us on Twitter or LinkedIn.
後編がいつ出るか知りたい方は、ニュースレターを購読するか、ツイッターかリンクトインでフォローしてください。

Found an error? Click here to let us know.
エラーが見つかりましたか？ここをクリックしてお知らせください。
