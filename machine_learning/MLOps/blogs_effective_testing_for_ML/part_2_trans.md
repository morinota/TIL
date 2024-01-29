## link リンク

https://ploomber.io/blog/ml-testing-ii/
https://ploomber.io/blog/ml-testing-ii/

# Effective Testing for Machine Learning (Part II) 機械学習のための効果的なテスト（後編）

## Introduction 

In this series’s first part, we started with a simple smoke testing strategy to ensure our code runs on every git push.
このシリーズの最初のパートでは、すべての git プッシュでコードが実行されることを確認するためのシンプルなスモークテスト戦略から始めました。
Then, we built on top of it to ensure that our feature generation pipeline produced data with a minimum level of quality (integration tests) and verified the correctness of our data transformations (unit tests).
そして、その上に機能生成パイプラインが最低限の品質でデータを生成することを確認し（統合テスト）、データ変換の正しさを検証した（単体テスト）。

Now, we’ll add more robust tests: distribution changes, ensure that our training and serving logic is consistent, and check that our pipeline produces high-quality models.
次に、より堅牢なテストを追加する： ディストリビューションの変更、トレーニングとサービングのロジックが一貫していること、パイプラインが高品質なモデルを生成していることを確認します。

If you’d like to know when the third part is out, subscribe to our newsletter, follow us on Twitter or LinkedIn.
第3弾の発売日をお知りになりたい方は、ニュースレターを購読するか、ツイッターかリンクトインでフォローしてください。

## Level 3: Distribution changes and serving pipeline レベル3 配給の変更と配給パイプライン

Sample code available here.
サンプルコードはこちら。

Testing target variable distribution
ターゲット変数分布のテスト

In the previous level, we introduced integration testing to check our assumptions about the data.
前のレベルでは、データに関する仮定をチェックするために統合テストを導入した。
Such tests verify basic data properties such as no NULLs, or numeric ranges.
このようなテストは、NULLがないことや数値範囲などの基本的なデータ特性を検証する。
However, if working on a supervised learning problem, we must take extra care of the target variable and check its distribution to ensure we don’t train on incorrect data.
しかし、教師あり学習問題に取り組む場合は、ターゲット変数に細心の注意を払い、間違ったデータで学習しないようにその分布をチェックしなければならない。
Let’s see an example.
例を見てみよう。

In a previous project, I needed to update my training set with new data.
以前のプロジェクトで、新しいデータでトレーニングセットを更新する必要があった。
After doing so and training a new model, the evaluation metrics improved a lot.
そうして新しいモデルをトレーニングした結果、評価指標は大幅に改善された。
I was skeptical but couldn’t find any issues in recent code changes.
半信半疑だったが、最近のコード変更で問題は見つからなかった。
So I pulled out the evaluation report from the model in production and compared it with the one I had trained.
そこで私は、生産中のモデルの評価レポートを引っ張り出し、私がトレーニングしたモデルと比較した。
The evaluation report included a table with a training data summary: the mean of the target variable had reduced drastically:
評価報告書には、トレーニングデータの要約が表にまとめられていた： 目標変数の平均値が大幅に減少した：

Since the mean of the target variable decreased, the regression problem got easier.
対象変数の平均が減少したので、回帰問題は簡単になった。
Picture the distribution of a numerical variable: a model predicting zero will have an MAE equal to the absolute mean of the distribution; now, imagine you add recently generated data that increases the concentration of your target variable even more (i.e., the mean decreases): if you evaluate the model that always predicts zero, the MAE will decrease, giving the impression that your new model got better!
数値変数の分布を思い浮かべてください： ゼロを予測するモデルは、MAEが分布の絶対平均に等しくなります。今、ターゲット変数の濃度をさらに増加させる（つまり平均が減少する）最近生成されたデータを追加したとします： 常にゼロを予測するモデルを評価すると、MAEは減少し、新しいモデルが良くなったという印象を与えます！

After meeting with business stakeholders, we found out that a recent change in the data source introduced spurious observations.
ビジネス関係者とミーティングを行った結果、最近のデータソースの変更により、偽のオブザベーションが発生していることがわかりました。
After such an incident, I created a new integration test that compared the mean and standard deviation of the target variable to a reference value (obtained from the training set used by the current production model):
このような出来事の後、私はターゲット変数の平均と標準偏差を基準値（現在の生産モデルが使用するトレーニングセットから得られる）と比較する新しい統合テストを作成した：

Don’t overthink the reference values; take your previous values and add some tolerance.
基準値は考えすぎず、以前の値を参考に、ある程度の許容範囲を加えてください。
Then, if the test fails, investigate if it’s due to a fundamental change in the data generation process (in such a case, you may want to update your reference values) and not due to some data error.
そして、テストが失敗した場合は、それがデータのエラーによるものではなく、データ生成プロセスの根本的な変更によるものであるかどうかを調査する（そのような場合は、基準値を更新するとよい）。
If you’re working on a classification problem instead, you can compare the proportion of each label.
代わりに分類問題に取り組んでいるなら、それぞれのラベルの割合を比較することができる。

We could apply the same logic to all features and test their distributions: since they shouldn’t change drastically from one commit to the next.
すべての機能に同じロジックを適用し、その分布をテストすることができる： コミットごとに大きく変わることはないはずだからだ。
However, manually computing the reference ranges will take a lot of time if you have hundreds of features, so at the very least, test the distribution of your target variable.
しかし、手作業で参照範囲を計算するのは、数百のフィーチャーがある場合、多くの時間がかかるので、最低限、ターゲット変数の分布をテストする。

Note that comparing mean and standard deviation is a simple (but naive) test, it works well if you don’t expect your data to change much from one iteration to the next one, but a more robust and statisically principled way of comparing distributions is the KS test.
平均と標準偏差を比較するのは単純な（しかし素朴な）検定であり、データが反復ごとにあまり変化しないと予想される場合にはうまくいくが、分布を比較するのによりロバストで統計的に原理的な方法はKS検定であることに注意しよう。
Here’s a sample KS test implementation.
これがKSテストの実施例だ。

Testing Inference pipelines
推論パイプラインのテスト

Deploying a model involves a few more steps than loading a .pickle file and calling model.predict(some_input).
モデルをデプロイするには、.pickleファイルをロードしてmodel.predict(some_input)を呼び出すよりもいくつかのステップが必要です。
You most likely have to preprocess input data before passing it to the model.
ほとんどの場合、モデルに渡す前に入力データを前処理しなければならない。
More importantly, you must ensure that such preprocessing steps always happen before calling the model.
さらに重要なことは、このような前処理がモデルを呼び出す前に必ず行われるようにすることである。
To achieve this, encapsulate inference logic in a single call:
これを実現するには、推論ロジックを単一の呼び出しにカプセル化する：

Once you encapsulate inference logic, ensure you throw an error on invalid input data.
推論ロジックをカプセル化したら、無効な入力データに対してエラーを投げるようにする。
Raising an exception protects against ill-defined cases (it’s up to you to define them).
例外を発生させることで、定義されていないケースを防ぐことができる（定義するかどうかはあなた次第だ）。
For example, if you’re expecting a column containing a price quantity, you may raise an error if it has a negative value.
例えば、価格数量を含むカラムを想定している場合、そのカラムに負の値があるとエラーが発生する可能性があります。

There could be other cases where you do not want your model to make a prediction.
モデルに予測をさせたくないケースは他にもあるだろう。
For example, you may raise an error when the model’s input is within a subpopulation where you know the model isn’t accurate.
例えば、モデルの入力が、モデルが正確でないとわかっている部分母集団内にある場合、エラーを発生させることができる。

The following sample code shows how to test exceptions in pytest:
次のサンプルコードはpytestで例外をテストする方法を示しています：

The example above is a new type of unit test; instead of checking that something returns a specific output, we test that it raises an error.
何かが特定の出力を返すかどうかをチェックする代わりに、それがエラーを発生させるかどうかをテストするのだ。
Inside your ServingPipeline.predict method, you may have something like this:
ServingPipeline.predictメソッドの中に、次のようなものがあるでしょう：

To learn more about testing exceptions with pytest, click here.
pytestを使った例外テストの詳細については、ここをクリックしてください。

Here’s a sample implementation that checks that our pipeline throws a meaningful error when passed incorrect input data.
不正な入力データが渡されたときに、パイプラインが意味のあるエラーを投げることをチェックするサンプル実装を示します。

## Level 4: Training-serving skew レベル4 トレーニングに奉仕するスキュー

Sample code available here.
サンプルコードはこちら。

At this level, we test that our inference pipeline is correct.
このレベルでは、推論パイプラインが正しいかどうかをテストする。
We must verify two aspects to assess the correctness of our inference pipeline:
推論パイプラインの正しさを評価するためには、2つの側面を検証しなければならない：

Preprocessing is consistent at training and serving time.
前処理はトレーニング時とサーブ時に一貫して行われる。

Feature generation part of the inference pipeline correctly integrates with the model file.
推論パイプラインのフィーチャー生成部分がモデルファイルと正しく統合される。

Training-serving skew
トレーニング・サービス・スキュー

Training-serving skew is one of the most common problems in ML projects.
トレーニング・サービス・スキューは、MLプロジェクトで最も一般的な問題の1つである。
It happens when the input data is preprocessed differently at serving time (compared to training time).
これは、（トレーニング時と比べて）サービング時に入力データの前処理が異なる場合に起こる。
Ideally, we should share the same preprocessing code at serving and training time; however, even if that’s the case, it’s still essential to check that our training and serving code preprocess the data in the same manner.
しかし、たとえそうであったとしても、トレーニングコードとトレーニングコードが同じ方法でデータを前処理していることを確認することは不可欠である。

The test is as follows: sample some observations from your raw data and pass them through your data processing pipeline to obtain a set of (raw_input, feature_vector) pairs.
テストは以下のようになる： 生データからいくつかのオブザベーションをサンプリングし、それをデータ処理パイプラインに通して、(raw_input, feature_vector)のペアの集合を得る。
Now, take the same inputs, pass them through your inference pipeline, and ensure that both feature vectors match precisely.
同じ入力を推論パイプラインに通し、両方の特徴ベクトルが正確に一致することを確認する。

Here’s a sample implementation of a test from our sample repository that checks there is no training-serving skew.
以下は、私たちのサンプルリポジトリにあるテストの実装例で、訓練に役立つスキューがないことをチェックします。

To simplify maintaining a training and serving pipeline, check out Ploomber, one of our features is to transform batch-based training pipeline into an in-memory one without code changes.
トレーニング・パイプラインとサービング・パイプラインの保守を簡素化するために、Ploomberをチェックしてください。Ploomberの特徴の1つは、バッチ・ベースのトレーニング・パイプラインを、コードを変更することなくインメモリ・パイプラインに変換することです。

Features and model file integration
機能とモデルファイルの統合

Imagine I deployed a model that used ten features a month ago.
ヶ月前に10個の機能を使ったモデルをデプロイしたとしよう。
Now, I’m working on a new one, so I add the corresponding code to the training pipeline and deploy: production breaks.
今、新しいものに取り組んでいるので、トレーニングパイプラインに対応するコードを追加し、デプロイする： プロダクションが壊れる。
What happened? I forgot to update my inference pipeline to include the recently added feature.
何が起こったのか？最近追加された機能を含むように推論パイプラインを更新するのを忘れていた。
So, it’s essential to add another test to ensure your inference code correctly integrates with the model file produced by the training pipeline: the inference pipeline should generate the same features that the model was trained on.
そのため、推論コードがトレーニングパイプラインによって生成されたモデルファイルと正しく統合されていることを確認するために、別のテストを追加することが不可欠です： 推論パイプラインは、モデルがトレーニングされたのと同じ特徴を生成する必要があります。

In our sample project, we first train a model with a sample of the data, then we ensure that we can use the trained model to generate predictions.
サンプル・プロジェクトでは、まずデータのサンプルを使ってモデルを訓練し、次に訓練されたモデルを使って予測を生成できることを確認する。
Such a test is implemented in the ci.yml file, and it executes on each git push.
このようなテストはci.ymlファイルに実装されており、git pushのたびに実行される。

## Level 5: Model quality レベル5： モデルの品質

Sample code available here.
サンプルコードはこちら。

Before deploying a model, it’s essential to evaluate it offline to ensure that it has at least the same performance as a benchmark model.
モデルを配備する前に、少なくともベンチマークモデルと同じパフォーマンスを持っていることを確認するために、オフラインで評価することが不可欠です。
A benchmark model is often the current model in production.
ベンチマークモデルとは、多くの場合、生産中の現行モデルのことである。
This model quality test helps you quickly ensure that releasing some candidate model to production is acceptable.
このモデル品質テストは、ある候補モデルをプロダクションにリリースしても問題ないことを迅速に確認するのに役立ちます。

For example, if you’re working on a regression problem and use Mean Absolute Error (MAE) as your metric, you may compute MAE across the validation set and for some sub-populations of interest.
たとえば、回帰問題に取り組んでいて、平均絶対誤差（Mean Absolute Error：MAE）を指標として使用する場合、検証集合全体と関心のあるいくつかの部分集団についてMAEを計算することができます。
Say you deployed a model and calculated your MAE metrics; after some work, you added a new feature to improve model metrics.
モデルをデプロイし、MAEメトリクスを計算したとします。いくつかの作業の後、モデルのメトリクスを改善するために新しい機能を追加したとします。
Finally, you train a new model and generate metrics:
最後に、新しいモデルをトレーニングし、メトリクスを生成します：

How do you compare these results? At first glance, it looks like your model is working because it reduced MAE for the first two metrics, although it increased them in the third group.
これらの結果をどのように比較しますか？一見したところ、最初の2つのメトリクスでMAEを減少させたので、あなたのモデルは機能しているように見えますが、3番目のグループでは増加しています。
Is this model better?
このモデルの方がいいのか？

It’s hard to judge based on a single set of reference values.
一つの基準値で判断するのは難しい。
So instead of having a single set of reference values, create a distribution by training the production model with the same parameters multiple times.
そのため、単一の基準値セットを持つ代わりに、同じパラメータで生産モデルを複数回トレーニングすることで分布を作成します。
Say we repeat our training procedure three times for the benchmark model and the candidate model, and we get three data points this time:
ベンチマークモデルと候補モデルについて学習手順を3回繰り返し、今回は3つのデータ点を得たとする：

We now have an empirical distribution.
これで経験的分布が得られた。
Then you can compare that the metrics in your candidate model are within the observed range:
そして、候補モデルのメトリクスが観測された範囲内にあることを比較することができます：

Here’s a test implementation in our sample repository.
サンプルリポジトリにあるテスト実装です。

Note that we’re evaluating current on both sides; this is essential because we want the tests to alert us when our model drops in performance and increases steeply.
両側の電流を評価していることに注意してほしい。これは、モデルの性能が落ちたり、急上昇したりしたときに、テストが警告を発してくれるようにしたいからだ。
While performance increases are great news, we should make sure that such increase is due to some specific improvement (e.g., training on more data, adding new features) and not due to a methodological error such as information leakage.
性能の向上は素晴らしいニュースだが、そのような向上が、情報漏洩のような方法論上の誤りによるものではなく、何らかの具体的な改善（例えば、より多くのデータでトレーニングする、新しい特徴を追加する）によるものであることを確認する必要がある。

Note: Evaluating model performance with minimum and maximum metric values is a simple way to get started, however, at some point you may want to implement more statistically principled approaches, this article reviews a few methods for doing so.
注意 しかし、ある時点で、より統計的に原理的なアプローチを実装したくなるかもしれません。この記事では、そのためのいくつかの方法をレビューします。

It is critical to test model quality on every code change.
コード変更のたびにモデルの品質をテストすることは非常に重要である。
For example, imagine you haven’t run your tests in a while; since the last time you ran them, you increased the training set size, added more features, and optimized the performance of some data transformations.
例えば、しばらくテストを実行していなかったとします。前回テストを実行したときから、トレーニングセットのサイズを大きくし、より多くの特徴を追加し、いくつかのデータ変換のパフォーマンスを最適化したとします。
You then train a model, and the test breaks because the pipeline produced a model with higher performance.
そしてモデルを訓練し、パイプラインがより高い性能を持つモデルを生成したため、テストが中断される。
In such a case, you may need to train models from previous commits to know what action caused the model’s performance to fall out of the expected range.
このような場合、モデルのパフォーマンスが期待範囲から外れた原因を知るために、過去のコミットからモデルをトレーニングする必要があるかもしれない。
Compare that to the scenario where you test on each change: if your model increases performance when adding more training data, that’s great news! But if you improved the performance (i.e., to use less memory) of some data transformation and your model is better all of a sudden, there’s reason to be skeptical.
変更ごとにテストするシナリオと比較してください： 学習データを増やしたときにモデルの性能が向上したなら、それは素晴らしいニュースだ！しかし、あるデータ変換のパフォーマンス（つまり、より少ないメモリ使用量）を向上させ、モデルが突然良くなったとしたら、懐疑的になる理由がある。

From a statistical perspective, the more metrics to compare, the higher the chance of your test to fail.
統計的な観点からは、比較するメトリクスが多ければ多いほど、テストが失敗する確率は高くなります。
A test that fails with no apparent reason isn’t great.
明らかな理由もなく失敗するテストは素晴らしいものではない。
To increase the reliability of such a test, you have two options:
このようなテストの信頼性を高めるには、2つの選択肢がある：

Generate a more accurate empirical distribution (e.g., train the benchmark model 50 times instead of 10).
より正確な経験分布を生成する（例えば、ベンチマークモデルを10回ではなく50回訓練する）。

Reduce the number of metrics to compare.
比較する指標の数を減らす。

For critical models, it’s a good idea to complement the previous model quality testing with some manual quality assessment.
クリティカルなモデルについては、これまでのモデルの品質テストを、手作業による品質評価で補完するのがよい。
Manual assessment helps because some model properties are more difficult to test automatically but show up quickly by visual human inspection; once you detect any critical metrics to track, you can include them in the automated test.
モデルの特性の中には、自動テストは難しいが、人間が目視することですぐにわかるものがあるため、手動評価が役立ちます。追跡すべき重要なメトリクスを検出したら、それを自動テストに含めることができます。

One way to quickly generate model evaluation reports is to run your training code as a notebook; for example, say your train.py script looks like this:
モデルの評価レポートを素早く作成する1つの方法は、トレーニングコードをノートブックとして実行することです。例えば、train.pyスクリプトが以下のようなものだとします：

Instead of writing extra code to save the chart and the table in a .html file, you can use Ploomber, which automatically converts your .py to .ipynb (or .html) files at runtime, so you easily get a model evaluation report each time you train a new model.
チャートと表を.htmlファイルに保存するために余分なコードを書く代わりに、Ploomberを使うことができます。Ploomberは実行時に.pyを.ipynb（または.html）ファイルに自動的に変換するので、新しいモデルをトレーニングするたびに、簡単にモデルの評価レポートを得ることができます。
You can also use sklearn-evaluation which can compare multiple .ipynb files (see this example).
また、複数の.ipynbファイルを比較できるsklearn-evaluationを使用することもできます（この例を参照してください）。

## Up Next 次へ

In this second part, we increase the robustness of our tests: we check for distribution changes in our target variable, ensure that our training and serving logic is consistent, and check that our pipeline produces high-quality models, concluding our 5-level framework.
この第2部では、テストの頑健性を高める： ターゲット変数の分布の変化をチェックし、トレーニングとサービングのロジックが一貫していることを確認し、パイプラインが高品質なモデルを生成することをチェックし、5レベルのフレームワークを完成させる。

In the following (and last) part of the series, we’ll provide extra advice to set up a streamlined workflow that allows us to repeat the develop -> test -> improve loop: we modify our pipeline, ensure that it works correctly, and continue improving.
このシリーズの次の（そして最後の）パートでは、開発→テスト→改善のループを繰り返すことができる合理的なワークフローを設定するための特別なアドバイスを提供する： 私たちはパイプラインを修正し、それが正しく機能することを確認し、改善を続けます。

If you’d like to know when the third part is out, subscribe to our newsletter, follow us on Twitter or LinkedIn.
第3弾の発売日をお知りになりたい方は、ニュースレターを購読するか、ツイッターかリンクトインでフォローしてください。