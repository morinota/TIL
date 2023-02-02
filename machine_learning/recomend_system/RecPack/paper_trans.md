## 0.1. link 0.1. リンク

- https://dl.acm.org/doi/fullHtml/10.1145/3523227.3551472 httpsを使用しています。

## 0.2. title 0.2. タイトル

RecPack:
RecPack:
An(other) Experimentation Toolkit for Top-N Recommendation using Implicit Feedback Data
暗黙のフィードバックデータを用いたトップNレコメンデーションのための（他の）実験用ツールキット

## 0.3. abstract 0.3. 抽象的

RecPack is an easy-to-use, flexible and extensible toolkit for top-N recommendation with implicit feedback data.
RecPackは、暗黙のフィードバックデータを用いたトップN推薦のための、使いやすく柔軟で拡張可能なツールキットである。
Its goal is to support researchers with the development of their recommendation algorithms, from similarity-based to deep learning algorithms, and allow for correct, reproducible and reusable experimentation.
その目的は、類似性ベースから深層学習アルゴリズムまで、研究者の推薦アルゴリズムの開発を支援し、正しく、再現可能で再利用可能な実験を可能にすることである。
In this demo, we give an overview of the package and show how researchers can use it to their advantage when developing recommendation algorithms.
本デモでは、本パッケージの概要を説明し、研究者が推薦アルゴリズムを開発する際に、どのように本パッケージを利用できるかを紹介します。

# 1. Introduction 1. はじめに

Over the past decade, recommender systems have become a staple of online user experiences across industries, from media to tourism or e-commerce.
過去 10 年間で、レコメンダーシステムは、メディアから観光や電子商取引まで、業界を問わずオンラインユーザ体験の定番となった。
At the same time, the domain of recommender systems’ research has evolved from a focus on rating prediction tasks, e.g. the Netflix 1 Million Dollars Prize [5], to top-N recommendation [26].
同時に、推薦システムの研究領域は、Netflix 100万ドル賞[5]のような視聴率予測タスクに焦点を当てたものから、トップN推薦[26]に発展してきた。
Today, the state-of-the-art in top-N recommendation advances at a very fast pace.
今日、トップN推薦の最先端技術は非常に速いスピードで進歩している。
More and more, researchers are encouraged to share their code to enable reproducibility and increase the transparency of their research process [30].
また、研究者は、再現性を確保し、研究プロセスの透明性を高めるために、コードを共有することが推奨されている[30]。
However, this code is often of low quality and
しかし、このようなコードはしばしば低品質で

RecPack is an experimentation toolkit for top-N recommendation using implicit feedback data written in Python, with a familiar interface and clear documentation.
RecPackは、暗黙のフィードバックデータを用いたトップN推薦のための実験ツールキットで、Pythonで書かれており、親しみやすいインタフェースと明確なドキュメントを備えています。
Its goal is to support researchers who advance the state-of-the-art in top-N recommendation to write reproducible and reusable experiments.
RecPackの目標は、トップNレコメンデーションの最先端を行く研究者が、再現可能で再利用可能な実験を書くことを支援することである。
RecPack comes with a range of different datasets, recommendation scenarios, state-of-the-art baselines and metrics.
RecPackには、様々なデータセット、推薦シナリオ、最先端のベースラインとメトリックが付属しています。
Wherever possible, RecPack sets sensible defaults.
可能な限り、RecPackは賢明なデフォルトを設定する。
For example, the hyperparameters of all recommendation algorithms included in RecPack are initialized to the best performing settings found in the original experiments.
例えば、RecPack に含まれるすべての推薦アルゴリズムのハイパーパラメータは、オリジナルの実験で見つかった最もパフォーマンスの良い設定に初期化されています。
The design of RecPack is heavily inspired by the interface of scikit-learn, a popular Python package for classification, regression, and clustering tasks.
RecPack のデザインは、分類、回帰、クラスタリングタスクのための一般的な Python パッケージである scikit-learn のインターフェースに大きく影響されています。
Data scientists who are familiar with scikit-learn will already have an intuitive understanding of how to work with RecPack.
scikit-learnに慣れているデータサイエンティストは、すでにRecPackの使い方を直感的に理解することができるでしょう。
On top of this, RecPack was developed with a production mindset:
その上、RecPack はプロダクションマインドセットで開発されました。
All contributions are rigorously reviewed and tested.
すべての貢献は厳密にレビューされ、テストされています。
The RecPack maintainers strive to maintain a test coverage of more than ninety percent at all times.
RecPack のメンテナは、常に 90%以上のテストカバレッジを維持するよう努力しています。
Using RecPack, researchers can:
RecPack を使用することで、研究者は以下のことが可能になります。

- Quickly develop algorithms by using one of RecPack’s abstract algorithm base classes, which represent popular recommendation paradigms such as factorization and item-to-item similarity. 因子分解やアイテム間の類似性など、一般的なレコメンデーションパラダイムを表すRecPackの抽象的なアルゴリズムベースクラスのいずれかを使用して、アルゴリズムを迅速に開発することができます。

- Compare their algorithms against state-of-the-art baselines in several different recommendation scenarios using a variety of performance metrics. 様々な性能指標を用いて、いくつかの異なる推薦シナリオで、最先端のベースラインとアルゴリズムを比較します。

- Tune hyperparameters of both baselines and their own implementations with minimal data leakage. ベースラインと独自の実装の両方のハイパーパラメータを最小限のデータリークでチューニングします。

In recent years, many other Python packages for top-N recommendation have been released [e.g. 3, 29, 35].
近年、top-N 推薦のための Python パッケージが多数リリースされています [e.g. 3, 29, 35]。
However, these focus more on the purpose of ‘benchmarking’, i.e., quick and accurate comparisons of state-of-the-art recommendation algorithms.
しかし、これらは「ベンチマーク」、すなわち、最新の推薦アルゴリズムの迅速かつ正確な比較の目的に重点を置いています。
Consequently, they provide access through the use of a configuration language or command-line interface.
そのため、設定言語やコマンドラインインタフェースを用いてアクセスを提供している。
RecPack on the other hand wishes to support researchers with the development of their own algorithms through repeated refinement, experimentation and bug-fixing in e.g., a Notebook environment.
一方、RecPackは、研究者がNotebook環境などで改良、実験、バグフィックスを繰り返しながら、独自のアルゴリズムを開発することを支援したいとしている。

In this demo, we will give you an overview of the different components of RecPack and how to use them to run your experiments and speed up the development of your own recommendation algorithms.
このデモでは、RecPackの様々なコンポーネントの概要と、それらを使って実験を行い、独自の推薦アルゴリズムの開発を加速させる方法について説明します。

# 2. RecPack Library 2. RecPackライブラリ

A typical experimentation pipeline for top-N recommendation is shown in Figure 1 1.
トップNレコメンデーションの典型的な実験パイプラインを図1 1に示す。
RecPack provides a dedicated module to support you with each step.
RecPack では、各ステップをサポートするための専用モジュールが用意されている。
In this Section, we will discuss the functionality of each of these modules.
本節では、これらのモジュールの各機能を説明する。

![](https://dl.acm.org/cms/attachment/0b77448a-4224-4264-a434-aef7e6883db2/recsys22-147-fig1.jpg)

Figure 1: Top-N Recommendation Pipeline:
図1: Top-Nレコメンデーションパイプライン。
First, a dataset is preprocessed and transformed into a user-item interaction matrix.
まず、データセットが前処理され、ユーザーとアイテムの相互作用行列に変換される。
Next, this matrix is split into a training, validation and test dataset.
次に、この行列をトレーニング、検証、テストデータセットに分割する。
These datasets are then used to first train algorithms and later make recommendations.
これらのデータセットを用いて、まずアルゴリズムを学習し、その後レコメンデーションを行う。
Finally recommendations are postprocessed, after which performance metrics are computed.
最後にレコメンデーションは後処理され、その後パフォーマンスメトリクスが計算される。

Datasets.
データセット
RecPack’s datasets provide easy access to many of the most popular collaborative filtering datasets [4, 13, 14, 18, 21, 24, 33].
RecPackのデータセットは、最も一般的な協調フィルタリングデータセット[4, 13, 14, 18, 21, 24, 33]の多くに簡単にアクセスすることができます。
To use one, simply instantiate a Dataset object, e.g., d = MovieLens25M().
データセットを使うには、d = MovieLens25M()のようにDatasetオブジェクトをインスタンス化するだけです。
Using RecPack’s datasets saves you time in two ways.
RecPack のデータセットを使用すると、2つの点で時間を節約できます。
First, if the dataset is publicly available RecPack will download it for you.
まず、データセットが一般に公開されている場合、RecPack がそれをダウンロードしてくれる。
If you already have a copy of the dataset or access to the dataset is restricted, you can specify a path and filename to tell RecPack where to find it.
既にデータセットのコピーを持っている場合や、データセットへのアクセスが制限されている場合は、パスとファイル名を指定して、RecPack にデータセットの場所を伝えることができます。
Second, for each dataset a set of default preprocessing filters is defined.
次に、各データセットに対して、デフォルトの前処理フィルタのセットが定義されています。
Using these default preprocessing filters increases the comparability between your experiments and those of other researchers.
これらのデフォルトの前処理フィルタを使用することで、他の研究者の実験との比較可能性が高まります。
Of course, this default filtering can be turned off when creating the Dataset, after which you can add your own preprocessing filters, as detailed in the next paragraph.
もちろん、データセットを作成する際にこのデフォルトのフィルタリングをオフにすることができ、その後、次の段落で説明するように、独自の前処理フィルタを追加することができます。
If your dataset of choice is not included in RecPack we recommend you load it as a pandas DataFrame [34].
RecPackに含まれていないデータセットは、pandas DataFrame [34]として読み込むことをお勧めします。

Preprocessing.
前処理。
In collaborative filtering, it is customary to first apply preprocessing filters to the raw dataset and then transform it into a user-item interaction matrix [2, 8, 29].
協調フィルタリングでは、まず生のデータセットに前処理フィルタを適用し、ユーザーとアイテムの相互作用行列に変換するのが通例です [2, 8, 29]。
If you use one of RecPack’s built-in datasets with the default preprocessing filters, this is done for you.
RecPackの組み込みデータセットとデフォルトの前処理フィルタを使用する場合、この処理は自動的に行われます。
If you are using your own dataset or wish to override the default preprocessing filters, the first step is to create the filters of your choice.
独自のデータセットを使う場合や、デフォルトの前処理フィルタを上書きしたい場合は、まず最初に好みのフィルタを作成します。

RecPack currently supports a choice of seven popular preprocessing filters.
RecPackは現在、7つの一般的な前処理フィルタをサポートしています。
MinUsersPerItem, MinItemsPerUser and MaxItemsPerUser are used to remove outliers that can negatively impact recommendation performance.
MinUsersPerItem、MinItemsPerUser、MaxItemsPerUserは、レコメンデーションパフォーマンスに悪影響を与える異常値を除去するために使用されます。
NMostPopular an NMostRecent can be used to limit the size of the item catalogue.
NMostPopularとNMostRecentは、アイテムカタログのサイズを制限するために使用される。
Deduplicate eliminates repeat interactions by retaining only the first occurrence of every user-item pair.
Deduplicateは、すべてのユーザーとアイテムのペアの最初の出現だけを保持することで、繰り返しのインタラクションを排除する。
Finally, MinRating selects ratings equal to or higher than a minimum rating value.
最後に、MinRatingは最小のレーティング値と同じかそれ以上のレーティングを選択する。
It is used to transform rating data into implicit feedback data.
これは、レーティングデータを暗黙のフィードバックデータに変換するために使用される。

To apply these filters to your own DataFrame, create a DataFramePreprocessor.
これらのフィルタを自分のDataFrameに適用するには、DataFramePreprocessorを作成します。
This DataFramePreprocessor will apply the filters and transform the user and item identifiers into consecutive matrix indices.
この DataFramePreprocessor は、フィルタを適用して、ユーザー識別子とアイテム識別子を連続した行列インデックスに変換します。
To add filters to either a Dataset or a DataFramePreprocessor, use their add_filter method.
Dataset または DataFramePreprocessor にフィルタを追加するには、それらの add_filter メソッドを使用します。

Matrix.
マトリクスです。
In RecPack, a user-item interaction matrix, optionally with timestamps, is represented by an InteractionMatrix object.
RecPack では、ユーザとアイテムのインタラクションマトリックス（オプションでタイムスタンプ付き）は InteractionMatrix オブジェクトで表現されます。
To create one, call the load method of your Dataset or pass your pandas DataFrame to the DataFramePreprocessor’s process
これを作成するには、Dataset の load メソッドを呼び出すか、pandas の DataFrame を DataFramePreprocessor の処理に渡します。

method.
メソッドを使用します。
You can also create an InteractionMatrix directly from your own preprocessed pandas DataFrame or a SciPy [32] Sparse csr_matrix.
また、前処理されたpandas DataFrameやSciPy [32] Sparse csr_matrixから直接InteractionMatrixを作成することも可能です。
The InteractionMatrix provides different views of your data.
InteractionMatrix は、データの様々なビューを提供します。
For example, you can extract your data as a csr_matrix with user-item interaction counts, the same user-item interactions binarized, or a list of items interacted with for every user, sorted from first to last interaction.
例えば、ユーザーとアイテムのインタラクション数、同じユーザーとアイテムのインタラクションを2値化したcsr_matrix、または各ユーザーがインタラクションしたアイテムのリスト（最初のインタラクションから最後のインタラクションまでソートされたもの）としてデータを抽出することが可能です。
The best thing about the InteractionMatrix is that for most experiments you do not have to worry about it.
InteractionMatrixについて最も良いことは、ほとんどの実験ではそれを気にする必要がないことです。
The Scenarios, Algorithms and Pipeline, discussed in the following paragraphs, know exactly what to do with it.
次の段落で説明するシナリオ、アルゴリズム、パイプラインは、それを使って何をすべきかを正確に知っています。

Scenarios.
シナリオ
Avoiding data leakage, yet evaluating a recommendation algorithm on a representative task is a difficult challenge.
データ漏洩を避けつつ、代表的なタスクで推薦アルゴリズムを評価することは難しい課題である。
Recommendations are used in many different contexts.
レコメンデーションは様々な文脈で使用される。
In one, it may be most important to make reasonable recommendations for previously unseen users.
あるときは、以前に見たことのないユーザーに対して合理的な推薦を行うことが最も重要かもしれません。
In another, it is important to get the user's next move exactly right.
また、あるときは、ユーザーの次の行動を正確に把握することが重要です。
RecPack comes with an elaborate set of recommendation scenarios, covering virtually all train-validation-test splits encountered in the scientific literature on recommender systems [2, 6, 8, 25, 29].
RecPack には、推薦システムに関する科学的文献 [2, 6, 8, 25, 29] で見られる、事実上すべての訓練-検証-テスト分割をカバーする、精巧な推薦シナリオのセットが付属しています。
When you do not need to tune any hyperparameters, pass validation=False to the constructor of your Scenario to split your InteractionMatrix into a training and test set.
ハイパーパラメータを調整する必要がない場合は、シナリオのコンストラクタに validation=False を渡して、 InteractionMatrix をトレーニングセットとテストセットに分割します。
When you do wish to tune your hyperparameters, pass validation=True instead to obtain a training, validation, and test set.
ハイパーパラメータを調整する場合は、validation=Trueを指定し、トレーニングセット、バリデーションセット、テストセットを作成します。
For a complete overview of all supported scenarios, see the documentation.
サポートされている全てのシナリオの概要については、ドキュメントをご覧ください。

Algorithms.
アルゴリズム
RecPack currently includes over twenty state-of-the-art recommendation algorithms that cover some of the most popular recommendation paradigms:
RecPack は現在、最も一般的な推薦パラダイムをカバーする 20 以上の最先端推薦アルゴリズムを搭載しています。
Item-to-item similarity [7, 12, 22, 31], factorization [2, 17, 23], auto-encoders [19, 27, 28], session-based [10, 16] and time-aware recommendation algorithms [20].
アイテム間の類似性 [7, 12, 22, 31]、因子分解 [2, 17, 23]、オートエンコーダー [19, 27, 28]、セッションベース [10, 16]、時間を考慮した推薦アルゴリズム [20] など、最も一般的な推薦パラダイムをカバーしています。
Additionally, it provides three abstract base classes that you can use to accelerate the development of your own algorithm:
さらに、独自のアルゴリズムの開発を加速するために利用できる3つの抽象的な基底クラスを提供する。
ItemSimilarityMatrixAlgorithm, FactorizationAlgorithm, and
ItemSimilarityMatrixAlgorithm, FactorizationAlgorithm, および FactorizationAlgorithm。

TorchMLAlgorithm.
TorchMLAlgorithm です。
These base classes implement a significant portion of the shared recommendation logic so that you can focus your efforts on the things that make your recommendation algorithm unique.
これらの基本クラスは共有される推薦ロジックの大部分を実装しており、あなたの推薦アルゴリズムをユニークなものにするために努力を傾けることができます。
All of RecPack’s algorithms implement scikit-learn’s BaseEstimator interface:
RecPack のアルゴリズムはすべて scikit-learn の BaseEstimator インタフェースを実装しています。
They have fit and predict methods and expect hyperparameters to be passed when the object is created.
これらは fit と predict メソッドを持ち、オブジェクトの作成時にハイパーパラメータが渡されることを想定しています。

Postprocessing.
後処理。
Real world recommender systems often apply postprocessing, in the form of business rules, to the predictions made by the recommendation algorithm.
現実のレコメンダーシステムでは、レコメンデーションアルゴリズムによる予測に対して、ビジネスルールという形で後処理を行うことが多い。
In an e-commerce context, for example, it is customary to exclude sensitive or age-restricted items.
例えば、電子商取引においては、機密事項や年齢制限のある商品を除外することが通例となっている。
In a news context, the recommendations are limited to articles published in the last two days.
ニュースの文脈では、レコメンデーションは過去2日間に公開された記事に限定される。
RecPack currently allows you to either select a subset of items through the use of SelectItems or exclude unwanted items via the ExcludeItems PostFilter.
RecPackでは現在、SelectItemsを使用してアイテムのサブセットを選択するか、ExcludeItems PostFilterを使用して不要なアイテムを除外することができます。

Metrics.
メトリックス
Of course, the ultimate goal of a recommendation experiment is to evaluate the performance of a recommendation algorithm.
もちろん、推薦実験の究極の目的は、推薦アルゴリズムの性能を評価することである。
RecPack comes with a selection of the most commonly used metrics in Top-N ranking [2, 25].
RecPack には Top-N ランキングで最もよく使われるメトリックスが付属しています [2、25]。
For example, to obtain the NDCG@20 of your algorithm, first create the metric ndcg = NDCGK(20).
例えば、アルゴリズムの NDCG@20 を得るには、まず ndcg = NDCGK(20) というメトリックを作成します。
Next, pass the targets and predictions to the metric's calculate method.
次に、ターゲットと予測値をメトリックの計算メソッドに渡します。
To obtain the average NDCG@20 over users, use ndcg.value.
ユーザー全体の平均NDCG@20を取得するには、ndcg.valueを使用します。
However, RecPack’s metrics also allow for a more fine-grained analysis of the performance of your algorithms.
しかし、RecPackのメトリックでは、アルゴリズムのパフォーマンスをより細かく分析することも可能です。
To inspect detailed performance results, e.g., the NDCG@20 of individual users, use ndcg.results.
詳細なパフォーマンス結果、例えば個々のユーザーのNDCG@20を調べるには、ndcg.resultsを使用します。
For a complete overview of all metrics, see the documentation.
すべてのメトリクスの完全な概要については、ドキュメントを参照してください。

Pipelines.
パイプライン
RecPack’s Pipeline helps you to determine the optimal hyperparameters for a given algorithm and dataset, apply postprocessing, and evaluate the performance of your algorithm (and baselines) on a selection of performance metrics.
RecPackのPipelineは、与えられたアルゴリズムとデータセットに最適なハイパーパラメータを決定し、ポストプロセスを適用し、アルゴリズム（およびベースライン）の性能を性能指標のセレクションで評価することを支援します。
To use it, first create a pb = PipelineBuilder().
使用するには、まずpb = PipelineBuilder()を作成します。
Then, pass your Scenario to its set_data_from_scenario method to initialize the training, validation and test set.
そして、Scenarioをset_data_from_scenarioメソッドに渡して、トレーニング、バリデーション、テストセットを初期化します。
Use the add_algorithm method to add any algorithms you want to evaluate and add_metric to add performance metrics.
評価したいアルゴリズムがあればadd_algorithmメソッドで追加し、パフォーマンスメトリクスを追加するにはadd_metricメソッドを使用します。
To obtain a Pipeline, call p = pb.build() and then use p.run() to run your pipeline.
Pipelineを取得するには、p = pb.build()を呼び出し、p.run()を使ってパイプラインを実行します。
For more advanced use, see the documentation.
より高度な使い方は、ドキュメントを参照してください。

# 3. SETUP 3. セットアップ

RecPack is available for download from PyPI.
RecPack は PyPI からダウンロードすることができます。
In the documentation, you will find Getting Started Guides as well as detailed documentation of each of RecPack’s modules.
ドキュメントには、RecPackの各モジュールの詳細なドキュメントだけでなく、Getting Started Guidesもあります。
The code is open-source and available on GitLab.
コードはオープンソースで、GitLab で公開されています。
RecPack is licensed under AGPL [9].
RecPack は AGPL [9] の下でライセンスされています。
To raise issues or ask questions about the use of RecPack, check out the source code and contribution guidelines on GitLab.
RecPack の使用に関する問題提起や質問は、GitLab 上のソースコードと貢献のガイドラインをチェックしてください。

# 4. DEMO 4. デモ

In the demo, we first implement MLP, a neural matrix factorization algorithm proposed in He et al. [15], to showcase how RecPack’s TorchMLAlgorithm’s base class assists you in the development of your own recommendation algorithms.
デモでは、まずHeら[15]で提案されたニューラル行列因子法MLPを実装し、RecPackのTorchMLAlgorithmの基底クラスが独自の推薦アルゴリズムの開発を支援することを紹介します。
We then carry out a recommendation experiment.
次に、推薦実験を行う。
First, we select the MovieLens25M Dataset and transform it into an InteractionMatrix.
まず、MovieLens25M Datasetを選択し、InteractionMatrixに変換する。
Next, we split this InteractionMatrix into a training, validation and test dataset using the WeakGeneralization Scenario.
次に、このInteractionMatrixをWeakGeneralizationシナリオを用いて、トレーニングデータセット、検証用データセット、テストデータセットに分割します。
Subsequently, we create a PipelineBuilder and start building a Pipeline in which we compare the performance of MLP to WMF and BPRMF, two baselines included in RecPack.
その後、PipelineBuilderを作成し、RecPackに含まれる2つのベースラインであるWMF、BPRMFとMLPの性能を比較するPipelineの構築を開始します。
We define a parameter grid for hyperparameter tuning, an optimization metric, and evaluation metrics.
ハイパーパラメータチューニングのためのパラメータグリッド、最適化メトリック、評価メトリックを定義します。
Finally, we build and run our pipeline and evaluate the performance of each of the algorithms.
最後に，我々のパイプラインを構築・実行し，各アルゴリズムの性能を評価する．

# 5. FUTURE WORK 5. 将来の仕事

RecPack is being actively maintained and developed.
RecPack は積極的に保守・開発されている。
In the near future, its maintainers plan to add beyond-accuracy metrics [11] and hybrid and content-based recommendation algorithms [2].
近い将来には、精度を超える指標 [11]、ハイブリッドおよびコンテンツベースの推薦アルゴリズム [2] を追加する予定です。