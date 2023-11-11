## link リンク

- https://dl.acm.org/doi/10.1145/3604915.3609488 https://dl.acm.org/doi/10.1145/3604915.3609488

## title タイトル

Everyone’s a Winner! On Hyperparameter Tuning of Recommendation Models
誰もが勝者だ 推薦モデルのハイパーパラメータ調整について

## abstruct abstruct

The performance of a recommender system algorithm in terms of common offline accuracy measures often strongly depends on the chosen hyperparameters.
一般的なオフライン精度測定における推薦システムアルゴリズムの性能は、しばしば選択されたハイパーパラメータに強く依存する。
Therefore, when comparing algorithms in offline experiments, we can obtain reliable insights regarding the effectiveness of a newly proposed algorithm only if we compare it to a number of state-of-the-art baselines that are carefully tuned for each of the considered datasets.
したがって、オフライン実験でアルゴリズムを比較する場合、検討したデータセットごとに注意深く調整された数多くの最先端のベースラインと比較した場合にのみ、新しく提案されたアルゴリズムの有効性に関する信頼できる洞察を得ることができる。
While this fundamental principle of any area of applied machine learning is undisputed, we find that the tuning process for the baselines in the current literature is barely documented in much of today’s published research.
応用機械学習のどの分野においても、この基本原則は議論の余地のないものであるが、**現在発表されている研究の多くでは、ベースラインのチューニング過程がほとんど文書化されていない**ことがわかる。
Ultimately, in case the baselines are actually not carefully tuned, progress may remain unclear.
結局のところ、ベースラインが注意深く調整されなければ、進歩は不明瞭なままかもしれない。
In this paper, we exemplify through a computational experiment involving seven recent deep learning models how every method in such an unsound comparison can be reported to be outperforming the state-of-the-art.
本稿では、7つの最近のディープラーニングモデルを用いた計算実験を通じて、このような不健全な比較の中で、どのような方法が最先端の技術を上回っていると報告できるかを例証する。
Finally, we iterate appropriate research practices to avoid unreliable algorithm comparisons in the future.
最後に、将来的に信頼性の低いアルゴリズム比較を避けるために、適切な研究手法を反復する。

# Introduction はじめに

Recommender systems are a highly visible success story of applied machine learning.
レコメンダー・システムは、応用機械学習の成功例として非常に注目されている。
Early reports of the value of such systems date back almost 25 years [27].
このようなシステムの価値に関する初期の報告は、約25年前にさかのぼる[27]。
Today, most major online platforms use such systems to provide personalized item suggestions to their users, nowadays often based on deep learning, see, e.g., [7, 30].
今日、ほとんどの主要なオンライン・プラットフォームは、ユーザーにパーソナライズされたアイテム提案を提供するために、このようなシステムを使用している。
Academic research in this area is flourishing as well, and many new machine learning models or network architectures for the recommendation task are published every year.
この分野の学術研究も盛んで、推薦タスクのための新しい機械学習モデルやネットワーク・アーキテクチャが毎年数多く発表されている。
However, there are indications that the progress that is reported to be achieved in academic papers is not as strong as one could expect, Today’s publication culture more or less mandates that every new published model must significantly improve upon the “state-of-the-art” on various metrics and datasets.
しかし、学術論文で報告される進歩は、期待されるほど強くないという指摘もある。今日の出版文化では、発表される新しいモデルはすべて、さまざまな指標やデータセットで「最先端」を大幅に改善しなければならないことが、多かれ少なかれ義務付けられている。
It was however observed in the related field of information retrieval many years ago that the reported improvements often do not add up [4].
しかし、何年も前に情報検索の関連分野で、報告された改善がしばしば辻褄が合わないことが観察された[4]。
Similar observations were made in the area of recommender systems [9, 23], as well as in other fields of applied machine learning, e.g., in time series forecasting [21].
レコメンダー・システム[9, 23]の分野でも、時系列予測[21]などの応用機械学習の他の分野でも、同様の観察がなされている。
In these and in several other works it turned out that the latest published models are in fact often not outperforming existing models and sometimes conceptually simple or longer-known methods can reach at least similar performance levels, at least in offline evaluations [19, 24].1 There are different factors that contribute to this issue, as discussed in [9, 18, 21].
この問題には、[9, 18, 21]で議論されているように、さまざまな要因がある。
Besides a certain researcher freedom when it comes to the selection of the baselines, the evaluation protocol and the metrics, one major problem seems to be that the hyperparameters of the selected baselines are often not properly tuned [20, 25], whereas significant effort may go into tuning the newly proposed model.
ベースライン、評価プロトコル、メトリクスの選択に関して、研究者がある程度自由にできることに加え、1つの大きな問題は、選択されたベースラインのハイパーパラメータがしばしば適切にチューニングされないことである[20, 25]。
It is clear, however, that it is impossible to derive any insights from experiments in which not all compared models—both the proposed ones and the chosen baselines—are carefully tuned for each dataset considered in the evaluation.
しかし、すべての比較モデル（提案されたモデルと選択されたベースラインの両方）が、評価で考慮された各データセットに対して注意深く調整されていない実験から、いかなる洞察も導き出すことができないことは明らかである。
With the considerable computational complexity of some modern deep learning models, this systematic tuning process can lead to significant demands in terms of times and resources.
最近のディープラーニング・モデルは計算がかなり複雑なため、この体系的なチューニング・プロセスは、時間とリソースの面で大きな要求につながる可能性がある。
It is therefore surprising that the documentation of this process—which may easily take weeks to complete—is often only very briefly covered in many papers or not mentioned at all.
それゆえ、数週間を要することもあるこのプロセスの文書化が、多くの論文でごく簡単にしか取り上げられていないか、まったく触れられていないことが多いのは驚くべきことである。
In some cases, only one set of optimal hyperparameters is reported, even though more than one dataset is used.
場合によっては、複数のデータセットが使用されているにもかかわらず、最適なハイパーパラメータのセットは1つしか報告されていない。
Sometimes, the hyperparameters for the baselines are taken from the original paper, and no discussion is provided if the same datasets (after pre-processing) were actually used in the original paper.
ベースラインのハイパーパラメータは原著論文から引用されていることもあり、同じデータセット（前処理後）が原著論文で実際に使用されたかどうかについての考察はない。
In yet other situations, probably the default parameters of a given public implementation of certain baselines have been used.
さらに別の状況では、おそらくあるベースラインの公開実装のデフォルト・パラメーターが使われている。
Another observation here is that the code of the used baselines and the code that was used to automatically tune the hyperparameters for the experiments is not shared by the authors either.
もう一つの観察は、使用されたベースラインのコードと、実験のためのハイパーパラメータを自動的に調整するために使用されたコードが、著者たちにも共有されていないことである。
With this short essay, we would like to showcase the dangers of what might be common practice in our field.
この短いエッセイで、私たちの分野では常識かもしれないことの危険性を紹介したい。
Next, in Section 2, we report the results of the inspection of a set of recent conference papers published at highly relevant outlets for recommender systems in terms of what is reported in the papers regarding hyperparameter tuning of the baselines.
次に、セクション2において、推薦システムに関連性の高い出版社で最近発表された一連の会議論文を、ベースラインのハイパーパラメータチューニングに関する論文で報告されている内容に関して検査した結果を報告する。
We emphasize that we do not suggest that no proper hyperparameter tuning was actually done in these papers.
我々は、これらの論文で適切なハイパーパラメータのチューニングが実際に行われなかったことを示唆しているのではないことを強調する。
Our observations only refer to the documentation of the process in the papers.
私たちの見解は、各紙に掲載されたプロセスの文書に言及しているに過ぎない。
In Section 3, we then report the outcome of an illustrative experiment, in which we tuned a set of recent models and then compared the results to those obtained when using the random parameters for the same models in a recent evaluation framework.
セクション3では、最近のモデルのチューニングを行い、その結果を最近の評価フレームワークで同じモデルのランダムパラメータを使用した場合の結果と比較した、例示的な実験の結果を報告する。
Not too surprisingly, the results show that every model can be a winner when we compare its optimized version against non-optimized baselines.
驚くことではないが、最適化されたバージョンを最適化されていないベースラインと比較した場合、どのモデルも勝者になりうるという結果が出ている。
The paper ends with a discussion of implications and ways forward in Section 4.
本稿の最後を飾るのは、セクション4での意味合いと今後の展開である。

# A Qulitative Analysis of the State-of-the-Practice 実践の現状に関する定性的分析

To obtain a picture of the state-of-the-practice in terms of what is reported today in research papers, we scanned the 2022 proceedings of five relevant ACM conference series, namely KDD, RecSys, SIGIR, TheWebConf, WSDM, for papers that report algorithmic improvements.
今日、研究論文で報告されている内容という観点から、最先端の実践状況を把握するため、KDD、RecSys、SIGIR、TheWebConf、WSDMという5つの関連するACM会議シリーズの2022年のプロシーディングスをスキャンし、アルゴリズムの改善について報告している論文を探した。
Since our experiment in Section 3 focuses on the top-n recommendation task based mainly on user-item interaction matrices, we only considered such papers in our analysis.
セクション3の実験では、主にユーザーとアイテムの相互作用行列に基づくトップn推薦タスクに焦点を当てているため、分析ではこのような論文のみを考慮した。
We identified 21 relevant papers, which we list in the online material.
その結果、21の関連論文が見つかったので、オンライン資料に掲載した。
To avoid highlighting individual research works here we refrain from providing exact citations here for individual observations.
ここでは、個々の研究成果を強調することを避けるため、個々の観察結果の正確な引用は控える。
We iterate that our goal is to provide evidence regarding what is documented in the context of hyperparameter tuning, and we are not challenging the reported results in any paper.
我々の目的は、ハイパーパラメータチューニングの文脈で文書化されていることに関する証拠を提供することであり、どの論文でも報告されている結果に挑戦しているわけではないことを繰り返す。
We also acknowledge that our analysis is based on a certain selection of conferences series, and things may be different for other publication outlets.
また、私たちの分析は、ある特定の会議シリーズに基づくものであり、他の出版社では状況が異なる可能性があることも承知している。
Still, we believe that our selection of papers is representative for today’s research practices.
それでも、私たちが選んだ論文は、今日の研究慣行を代表するものだと信じている。
Finally, we declare that there are similar patterns of shallow reporting of the hyperparameter tuning process in our own previous works as well.
最後に、ハイパーパラメータのチューニング過程の浅い報告には、我々自身の過去の作品にも同様のパターンがあることを宣言する。
Our observations of what we find in the papers can be summarized as follows.
私たちが論文で見つけたことをまとめると、次のようになる。
Tuning of the proposed model: On the more positive end, one of the examined works reports the searched ranges for “common” hyperparameters for such as learning rate, dropout ratio or the coefficient for L2 regularization.
提案モデルのチューニング： より肯定的な面では、検討された作品の1つが、学習率、ドロップアウト率、L2正則化の係数などの「一般的な」ハイパーパラメータの探索範囲を報告している。
Other parameters are however taken from the original papers or using defaults from the provided codes.
その他のパラメータは、原著論文から引用するか、提供されたコードのデフォルト値を使用している。
Furthermore, the optimal values are not reported in the end, and the pointer to the code leads to an empty GitHub repository.
さらに、最適値は最終的には報告されず、コードへのポインタは空のGitHubリポジトリにつながる。
Another paper reports some of the hyperparameter ranges and some chosen values (also for the baselines), but does not report on how the parameters were found, e.g., by grid search or some other method.
別の論文では、ハイパーパラメータの範囲と選択された値（ベースラインについても）が報告されているが、グリッドサーチや他の方法など、どのようにパラメータを見つけたかについては報告されていない。
In this case, only one set of hyperparameter values is reported, even though evaluations were done on three datasets.
この場合、3つのデータセットで評価が行われたにもかかわらず、ハイパーパラメータ値のセットは1つしか報告されていない。
Yet another paper only reports the fixed learning rate that was used for all models and datasets.
さらに別の論文では、すべてのモデルとデータセットに使用された固定学習率のみが報告されている。
Furthermore, in this case, the embedding size was kept constant across all compared models “for fair comparison”.
さらにこの場合、「公平な比較のため」、すべての比較モデルで埋め込みサイズは一定に保たれた。
In reality, however, embeddings sizes are hyperparameters to tune, and fixing them to one specific value (without much justification) may actually lead to an unfair comparison.
しかし実際には、エンベッディングのサイズは調整すべきハイパーパラメータであり、（あまり正当な理由もなく）特定の値に固定することは、実際には不公平な比較につながる可能性がある。
In the end, we only identified two papers among the 21 ones we considered, which reported all optimal hyperparameter sets (proposed model and baseline) for all examined datasets and which documented the hyperparameter ranges and search procedure in more detail.
最終的に、検討した21の論文のうち、検討したすべてのデータセットについて、すべての最適なハイパーパラメータセット（提案モデルとベースライン）を報告し、ハイパーパラメータの範囲と探索手順をより詳細に文書化している論文を2つだけ同定した。
The code for one of the papers was however not shared publicly.
しかし、ある論文のコードは公開されていない。

Tuning of baseline models: The documentation of how the baselines were tuned and which parameters were finally chosen is even more sparse than for the proposed models.
ベースラインモデルのチューニング： ベースラインがどのようにチューニングされ、最終的にどのパラメータが選ばれたのかについてのドキュメントは、提案モデルよりもさらに少ない。
Four authors refer to default parameters of public code or the values that were used in the original papers (even though we notice from the previous paragraph that the quality of documentation can be improved even for the proposed models).
4人の著者は、公開されているコードのデフォルトのパラメータや、元の論文で使用されている値を参照している（前の段落で、提案されたモデルでもドキュメントの質を改善できることに気づいたにもかかわらず）。
In six papers, no information about the hyperparameters and the tuning process is provided at all.
6つの論文では、ハイパーパラメータとチューニングプロセスに関する情報はまったく提供されていない。
In seven cases, a subset of baseline hyperparameter values is reported, but without listing the ranges or how the values were determined.
7つのケースでは、ベースラインのハイパーパラメータ値のサブセットが報告されているが、その範囲や値の決定方法は記載されていない。
Again, in four cases only one fixed set of hyperparameter values is reported even though various datasets are used in the experiments.
実験ではさまざまなデータセットが使用されているにもかかわらず、4つのケースでは1つの固定されたハイパーパラメータ値のみが報告されている。
Finally, one paper reports that they used hyperparameters from the original papers if available, and applied grid search for the others.
最後に、ある論文では、入手可能であれば原著論文のハイパーパラメータを使用し、それ以外はグリッドサーチを適用したと報告している。
As mentioned, only two papers report detailed hyperparameter ranges and final values for all datasets.
前述のように、すべてのデータセットについて詳細なハイパーパラメータの範囲と最終値を報告している論文は2つしかない。
Shared code: In 12 of the 21 papers, a link to a repository is provided.
共有コード： 21本の論文のうち12本で、リポジトリへのリンクが提供されている。
In two cases, these URLs were pointing to empty or nonexistent places, leaving us with a ratio of 50% in terms of code sharing2 .
2つのケースでは、これらのURLは、空または存在しない場所を指していた。
For the repositories actually containing code, we found that none of them contains the code of the used baselines.
実際にコードが含まれているリポジトリについては、使用したベースラインのコードが含まれているものはないことがわかった。
Also none of them contains code for the hyperparameter search, which would allow other researchers to reconstruct, e.g., the considered hyperparameter ranges.
また、ハイパーパラメータ探索のコードも含まれていないため、他の研究者が検討したハイパーパラメータの範囲などを再構築することができる。
Note however that some papers mentioned that hyperparameter tuning was done in a manual process.
ただし、ハイパーパラメータのチューニングが手作業で行われたと述べている論文もある。
Discussion: Our analysis of a set of papers published at renowned conferences in 2022 clearly shows that the documentation of the hyperparameter tuning process—both for the proposed models and the baselines—is in most cases quite incomplete or even missing.
考察 2022年に有名な学会で発表された論文群を分析したところ、提案されたモデルとベースラインの両方について、ハイパーパラメータのチューニングプロセスに関する文書が、ほとんどの場合、極めて不完全であるか、あるいは欠落していることが明らかになった。
Typically, authors spend about one paragraph in a section typically named “Implementation details”, where this information is packed.
通常、著者はこの情報を詰め込むために、一般的に「実装の詳細」と名付けられたセクションに約1段落を費やす。
In some works, the methodology also seems unclear, e.g., when authors report one single set of hyperparameter values for different datasets or when values from the original works are reused for very different datasets.
例えば、著者が異なるデータセットに対して1セットのハイパーパラメータ値を報告している場合や、原著の値を全く異なるデータセットに再利用している場合などである。
Overall, this lack of documentation makes it unclear if it is mainly a issue of reporting (e.g., because of space limitations) or if we are frequently facing methodological issues of competing against non-tuned baselines, as indicated in the literature.
全体的に、この文書化の欠如は、主に報告の問題なのか（例えば、スペースの制限のため）、それとも文献で指摘されているように、チューニングされていないベースラインとの競合という方法論的な問題に頻繁に直面しているのかを不明確にしている。

# Experiments 実験

In this section, we showcase that adopting a research practice of not carefully tuning the hyperparameters of the baselines can indeed lead to arbitrary “winners” during the hunt for models that outperform the state-of-the-art.
このセクションでは、ベースラインのハイパーパラメータを注意深くチューニングしないという研究慣行を採用すると、最先端技術を凌駕するモデルを探す際に、恣意的な「勝者」を生み出す可能性があることを示す。

## Comparing tuned and non-tuned models チューニング・モデルと非チューニング・モデルの比較

### Methodology. 方法論

We use the recent Elliot framework [2] as a basis for our evaluation.
評価の基礎として、最近のエリオット・フレームワーク[2]を使用する。
This Python-based framework implements a rich variety of recommendation models and it integrates components for automated hyperparameter search and evaluation.
このPythonベースのフレームワークは、豊富な種類の推薦モデルを実装し、自動化されたハイパーパラメータ検索と評価のためのコンポーネントを統合している。
Experiments, including hyperparameter ranges, can be defined through text-based configuration files, which allows for convenient reproducibility.3 Algorithms and Datasets.
ハイパーパラメータの範囲を含む実験は、テキストベースの設定ファイルによって定義することができ、再現性を容易にすることができる。
We focus our experiments on deep learning algorithms, which are the method of choice today.
この実験では、現在主流となっているディープラーニング・アルゴリズムに焦点を当てている。
We initially considered all such methods implemented in Elliot at the time of the experiment.
私たちはまず、実験時点でエリオットに実装されているこのような方法をすべて考慮した。
As some of the model implementations— including those proposed in [6],[12], and[28]—led to much lower performance levels as reported in the original papers (at an order of magnitude), we omitted them from this experiment and reported the issue to the framework authors.
6]、[12]、[28]で提案されたものを含むいくつかのモデル実装は、元の論文で報告されたよりもはるかに低いパフォーマンスレベル（桁違い）になったので、我々はこの実験からそれらを除外し、フレームワークの著者に問題を報告した。
The following models were included in our experiments, all of which were proposed during the last few years, and which might be considered to represent the state-of-the-art in a research paper.
我々の実験には以下のモデルが含まれており、これらはすべてここ数年の間に提案されたもので、研究論文では最先端を代表していると考えられるものである。
• Multinomial Likelihood Denoising Autoencoder (MultDAE) [17] • Multinomial Likelihood Variational Autoencoder (MultVAE) [17] • Convolutional Matrix Factorization (ConvMF) [15] • Generalized Matrix Factorization (GMF) [14] • Neural network based Collaborative Filtering (NeuMF) [14] • Outer product-based Neural Collaborative Filtering (ONCF) [13], (named ConvNeuMF in Elliot) • Neural Graph Collaborative Filtering (NGCF) [31] In addition to these models, we include the non-personalized MostPop method in our experiment, which simply recommends the most popular items in the dataset (in terms of the interaction counts) to every user.

- 多項尤度ノイズ除去オートエンコーダ(Multinomial Likelihood Denoising Autoencoder: MultDAE) [17] - 多項尤度変分オートエンコーダ(Multinomial Likelihood Variational Autoencoder: MultVAE) [17] - 畳み込み行列分解(Convolutional Matrix Factorization: ConvMF) [15] - 一般化行列分解(Generalized Matrix Factorization: GMF) [14] - ニューラルネットワークベースの協調フィルタリング(Neural network based Collaborative Filtering: NeuMF) [14] - 外積ベースのニューラル協調フィルタリング(Outer product-based Neural Collaborative Filtering: ONCF) [13]、 (ElliotではConvNeuMFと命名) - ニューラルグラフ協調フィルタリング(NGCF) [31] これらのモデルに加えて、非パーソナライズされたMostPop法を実験に含め、これは単にデータセットで最も人気のあるアイテム(インタラクションカウントの観点から)をすべてのユーザーに推奨する。
  We also used the implementation from the Elliot framework.
  エリオット・フレームワークの実装も使用した。
  Researchers have a lot of freedom to select datasets and metrics for their experiments, which represents another reason why it is difficult to impossible to determine what actually represents the state-of-the-art.
  研究者は、実験に使うデータセットや測定基準を自由に選ぶことができるが、これは、実際に何が最先端であるかを判断するのが難しい、あるいは不可能であるもう1つの理由を示している。
  To avoid any bias in our setup, we strictly followed the experimental setup described in [3], which was also based on the Elliot framework.
  我々のセットアップの偏りを避けるため、エリオットフレームワークに基づく[3]の実験セットアップに厳密に従った。
  Regarding the dataset, we therefore used the exact same datasets and p-core pre-processing procedures.
  従って、データセットに関しては、全く同じデータセットとp-coreの前処理手順を使用した。
  Specifically, the datasets include (i) MovieLens-1M (ML-1m), a dataset with movie ratings, (ii) Amazon Digital Music (AMZm), a dataset containing ratings for musical tracks, and (iii) Epinions, a dataset containing binary trust relationships between users of a social network.
  具体的には、(i)MovieLens-1M（ML-1m）は映画のレーティングを含むデータセット、(ii)Amazon Digital Music（AMZm）は音楽曲のレーティングを含むデータセット、(iii)Epinionsはソーシャルネットワークのユーザー間のバイナリ信頼関係を含むデータセットである。
  For the ML-1M and AMZm datasets, the rating data were transformed in a way that ratings with a value greater than 3 were encoded as positive signals.4 Hyperparameter Tuning Process.
  ML-1MとAMZmのデータセットでは、3以上の評価を正のシグナルとしてエンコードするように、評価データを変換した。
  We used the Tree Parzen Estimators for hyperparameter tuning, a method that is embedded in Elliot.
  ハイパーパラメータのチューニングには、Elliotに組み込まれているTree Parzen Estimatorsを使用した。
  In terms of finding suitable ranges for the different hyperparameters, we adopted different strategies to inform our choices.
  さまざまなハイパーパラメータの適切な範囲を見つけるという点で、私たちはさまざまな戦略を採用して選択を行った。
  First, we looked up the original papers to see if the authors reported ranges that they explored.
  まず、原著論文を調べ、著者が調査した範囲を報告しているかどうかを確認した。
  If this was not the case, we selected ranges that are frequently observed in the literature, e.g., for the learning rate, a common range could be from 0.0001 to 0.01, and typical embedding dimensions in the literature are 64, 128 and 256.
  そうでない場合は、文献で頻繁に観察される範囲を選択した。例えば、学習率については、一般的な範囲は0.0001から0.01であり、文献における典型的な埋め込み次元は64、128、256である。
  We set the number of iterations depending on the computational complexity of the tested algorithms.
  繰り返しの回数は、テストしたアルゴリズムの計算量に応じて設定した。
  The number of iterations ranged from 10 to 50.
  反復回数は10～50回。
  The exact ranges and finally chosen values are documented in the online repository.
  正確な範囲と最終的に選択された値は、オンライン・リポジトリに文書化されている。
  Importantly, we note here that we selected ranges in a way that they are good enough for the purpose of our experiment.
  重要なのは、私たちの実験の目的には十分な範囲を選んだということだ。
  This means that we need to find a set of hyperparameter values for each model that is outperforming any other model when using random values.
  つまり、ランダムな値を使用した場合に、他のどのモデルよりも優れた性能を発揮する各モデルのハイパーパラメータ値のセットを見つける必要がある。
  We therefore do not rule out that better hyperparameters can be found for each model and dataset; and that the ranking of the tuned algorithms may change with other values.
  したがって、各モデルとデータセットに対して、より良いハイパーパラメータが見つかる可能性を排除するものではない。
  For the sake of our experiment, we first executed all models with the non-tuned (random) values for the hyperparameters.
  実験のために、まずハイパーパラメータをチューニングしていない（ランダムな）値ですべてのモデルを実行した。
  The random procedure consisted of arbitrarily picking values manually from the given ranges for each hyperparameter.
  ランダムな手順は、各ハイパーパラメータについて与えられた範囲から手動で任意に値を選ぶことから成っている。
  We chose this procedure because we argue that there is a certain randomness in terms of how hyperparameters for the baselines are chosen in many papers.
  我々は、多くの論文でベースラインのハイパーパラメータがどのように選択されているかという点で、ある種のランダム性があると主張しているため、この手順を選択した。
  It can, for example, depend on what worked well for the datasets used in the original paper; or it can be simply based on the hard-coded default values that were left in the published source code by the authors.
  例えば、元の論文で使用されたデータセットでうまく機能したものに依存することもあれば、著者によって公開されたソースコードに残されたハードコードされたデフォルト値に単純に基づくこともある。
  After having obtained the results when using non-tuned hyperparameters, we systematically tuned the hyperparameters for all models on all datasets to obtain the best accuracy values.
  チューニングされていないハイパーパラメータを使用した場合の結果を得た後、最高の精度値を得るために、すべてのデータセットですべてのモデルのハイパーパラメータを系統的にチューニングした。
  We used the Normalized Discounted Cumulative Gain (NDCG) as the target metric during hyperparameter optimization.3.1.2 Results.
  3.1.2結果 ハイパーパラメータ最適化の際、正規化割引累積利得（NDCG）を目標指標とした。
  Table 1 shows the results for all models on the three datasets in terms of the NDCG@10.
  表1は、3つのデータセットにおける全モデルの結果をNDCG@10で示したものである。
  The ranking of the algorithms when using other metrics such as NDCG or MAP are as usual roughly aligned and can be found in the online repository.
  NDCGやMAPといった他の指標を用いた場合のアルゴリズムのランキングは、例によってほぼ一致しており、オンライン・リポジトリで見ることができる。
  The upper part of the table shows the results after systematic hyperparameter tuning, and the lower parts shows the outcomes when running all models with the non-tuned hyperparameters.
  表の上部は、系統的なハイパーパラメータ・チューニング後の結果を示し、下部は、チューニングされていないハイパーパラメータですべてのモデルを実行した場合の結果を示す。
  The numbers in the table correspond to the averages obtained through a five-fold cross-validation procedure.5 The most important observation is that for each dataset, even the worst-performing tuned model is better than the best model with non-tuned hyperparameters.
  表中の数値は、5重のクロス・バリデーション手順によって得られた平均値に対応する。5 最も重要な観察点は、各データセットについて、最も成績の悪いチューニング・モデルでさえ、チューニングされていないハイパーパラメータを持つ最良のモデルよりも優れていることである。
  Now this might not sound particularly surprising, given that it is well known that the performance of machine learning models can highly depend on the chosen hyperparameters.
  機械学習モデルの性能が選択されたハイパーパラメータに大きく依存することはよく知られている。
  Looking at our results, we in fact find that the difference between tuned and non-tuned models can be of an order of magnitude and more.
  我々の結果を見ると、実際、チューニングされたモデルとチューニングされていないモデルの間には、1桁以上の差があることがわかる。
  However, the important point is that even the worst-performing models for each dataset, which have NDCG values that are actually substantially lower than the best performing tuned models, can be reported as being a winner in a comparison in which the hyperparameters of the competitors are not tuned.
  しかし、重要な点は、各データセットで最も成績の悪いモデルでさえ、NDCGの値がチューニングされた最も成績の良いモデルよりも実際には大幅に低く、競合のハイパーパラメータがチューニングされていない比較では勝者であると報告できることである。
  In other words, it can be sufficient to outperform an existing method that is actually quite weak to report an improvement over the state-of-the-art that includes as many as seven recent neural methods on three datasets.
  言い換えれば、3つのデータセットで7つもの最新のニューラル手法を含む最先端技術に対する改善を報告するには、実際にはかなり弱い既存の手法を上回るだけで十分なのである。
  Considering however how little is documented about hyperparameter tuning of baselines in the current literature (see Section 2), there can be major concerns regarding the reliability of the reported rankings and improvements over the state-of-the-art.
  しかし、ベースラインのハイパーパラメータチューニングについて、現在の文献（セクション2参照）ではほとんど記述されていないことを考えると、報告されているランキングの信頼性や、最先端技術に対する改善について、大きな懸念がある。
  In fact, previous reproducibility analyses as reported, e.g., in [9], confirm that methodological issues of various kinds can hamper progress in recommender systems research.
  実際、例えば[9]で報告されているような過去の再現性分析は、様々な種類の方法論的問題が推薦システム研究の進歩を妨げる可能性があることを確認している。
  Another striking observation here is that the popularity-based MostPop method is performing better than some of the tuned models.
  ここでのもう一つの顕著な観察は、人気に基づくMostPop法が、いくつかの調整されたモデルよりも良いパフォーマンスをしていることである。
  A similar phenomenon was also reported in [9].
  同様の現象は[9]でも報告されている。
  The poor performance of some of the models—also compared to the MostPop method—may to some extent lie in the particular types of modestsized datasets in our experiment.
  MostPop法と比較した場合、いくつかのモデルの性能が低いのは、実験に使用したデータセットの種類が特殊であったためである可能性がある。
  Or it may be the result of the somewhat restricted hyperparameter tuning process, which was only executed to the extent that was necessary for experiment.
  あるいは、実験に必要な範囲でのみ実行された、やや制限されたハイパーパラメータ・チューニングの結果かもしれない。
  We iterate here that the ranking of the tuned models in Table 4 is not important, because we limited our search for hyperparameter ranges to typical values, and we limited the number of tuning iterations for the computationally complex models.
  ハイパーパラメータの範囲を典型的な値に限定し、計算が複雑なモデルについてはチューニングの反復回数を制限したためである。
  Exploring alternative or more unusual ranges, as done recently in [24], may help to further improve the performance of the individual models.
  最近[24]で行われたように、代替的な、またはより珍しい範囲を探ることは、個々のモデルの性能をさらに向上させるのに役立つかもしれない。

## Comparison with Other Baselines 他のベースラインとの比較

Besides comparisons with baselines that are not well tuned, another potential methodological issue observed in [9] can lie in the choice of the baselines and the propagation of weak baselines.
十分に調整されていないベースラインとの比較に加えて、[9]で観察されたもう1つの潜在的な方法論的問題は、ベースラインの選択と弱いベースラインの伝播にある可能性がある。
Remember that we limited our comparison to recent deep learning models, and reviewers might probably not complain, given the large set of recent baselines.
比較対象を最近のディープラーニング・モデルに限定したことを思い出してほしい。最近のベースラインの大規模なセットを考えれば、レビュアーはおそらく文句を言わないだろう。
However, there are several indications, also reported in [9] and other works, that simple methods can be competitive as well.
しかし、[9]などでも報告されているように、単純な方法でも競争力を発揮できることがいくつか示唆されている。
The propagation of weak baseline may happen, if we only consider models from one family, e.g., neural models.
弱いベースラインの伝播は、例えばニューラル・モデルのような、ある系列に属するモデルだけを考慮した場合に起こる可能性がある。
In the analysis in [3], the linear and “shallow” EASE𝑅 model [29] was the strongest performing method on the datasets used in our experiments.
3]の分析では、線形で "浅い "EASEǔモデル[29]が、我々の実験に使用したデータセットで最も強力な性能を発揮する手法であった。
Also the traditional user-based nearest-neighbor method (userKNN), which was proposed in the context of the GroupLens system [26] from 1994 can lead to competitive results when tuned properly [3].
また、1994年にGroupLensシステム[26]のコンテキストで提案された伝統的なユーザーベースの最近傍法（userKNN）は、適切に調整された場合、競争力のある結果を導くことができます[3]。
In fact, had we included EASE𝑅 in our comparison, it would have been on top of the ranking list of the tuned models for all datasets, with NDCG@10 = 0.343 for ML-1M, NDCG@10 = 0.086 for AMZm, and NDCG@10 = 0.164 for the Epinions dataset.
実際、EASE↪Lu_1 を比較に含めていれば、ML-1MではNDCG@10 = 0.343、AMZmではNDCG@10 = 0.086、EpinionsデータセットではNDCG@10 = 0.164となり、すべてのデータセットで調整済みモデルのランキングリストのトップになっただろう。
In that context it is also worth noting that EASE𝑅 has only one relevant hyperparameter to tune (L2-norm).
その意味で、EASE_445が調整するハイパーパラメータは1つだけ（L2-norm）であることも注目に値する。
The performance of EASE𝑅 was also quite good in case we selected this hyperparameter randomly, and a randomly tuned EASE𝑅 model would be ranked about in the middle of the tuned models for all three datasets.
EASE_445の性能は、このハイパーパラメータをランダムに選択した場合にも非常に優れており、ランダムにチューニングされたEASE_445モデルは、3つのデータセットすべてにおいて、チューニングされたモデルのほぼ中央に位置する。
It remains therefore important to consider simpler, e.g., linear, models, even though they might not be able to learn non-linear, higher-order dependencies in the data that neural models are often claimed to do in the literature.
従って、より単純な、例えば線形モデルを検討することは重要である。たとえ線形モデルであっても、ニューラル・モデルがしばしば文献で主張されるような、データ中の非線形で高次の依存関係を学習することはできないかもしれない。

# Implications and Conclusions 意味合いと結論

Our study showcases that almost arbitrary performance rankings for a given set of algorithms can be obtained depending on the level of fine-tuning of the hyperparameters.
我々の研究は、ハイパーパラメータの微調整のレベルに応じて、与えられたアルゴリズムのセットに対してほぼ任意の性能ランキングが得られることを示す。
While this is certainly not a huge surprise, the fact that in many published papers insufficient information about the hyperparameter tuning process is provided may raise major concerns regarding the true progress that is achieved.
確かにこれは大きな驚きではないが、多くの発表論文において、ハイパーパラメータのチューニング過程に関する情報が不十分であるという事実は、達成された真の進歩に関して大きな懸念を抱かせるかもしれない。
A number of previous research efforts both in the area of recommender systems and related fields like information retrieval confirm this issue, e.g., [9, 18, 23].
レコメンダーシステムと情報検索のような関連分野の両方で、多くの先行研究の努力がこの問題を裏付けている、例えば[9, 18, 23]。
The additional degrees of freedom that researchers usually have, e.g., in terms of the selection of baselines, metrics, datasets, and pre-processing steps, can further aggravate the problem.
ベースライン、測定基準、データセット、前処理ステップの選択など、研究者が通常持っている自由度がさらに増えることは、問題をさらに悪化させる可能性がある。
Various measures may help to better address these fundamental methodological problems.
このような方法論上の根本的な問題によりよく対処するために、さまざまな方策が役立つだろう。
First, despite increased awareness in the community, reproducibility is still a major obstacle to achieving progress.
第一に、コミュニティーの意識が高まっているにもかかわらず、再現性が進歩達成の大きな障害となっている。
We may observe that researchers share the code for their newly proposed models more often nowadays, and more attention is also paid to reproducibility in the peer-reviewing process, e.g., through explicit items on review forms.
最近では、研究者が新しく提案したモデルのコードを共有することが多くなり、査読プロセスにおいても、査読フォームに明示的な項目を設けるなど、再現性に注目が集まっている。
However, the reproducibility packages are often incomplete—in particular in terms of missing code for the baselines or the tuning process—which makes true reproducibility challenging.
しかし、再現性パッケージは不完全であることが多く、特にベースラインやチューニングプロセスのコードが欠けているため、真の再現性は困難である。
Various earlier works discuss this issue and propose guidelines and checklists for reproducible research both for general AI, for machine learning, and for recommender systems [8, 11, 22].
様々な先行研究がこの問題を議論し、一般的なAI、機械学習、レコメンダーシステムの両方について、再現可能な研究のためのガイドラインやチェックリストを提案している[8, 11, 22]。
However, it seems that the research community is only making very slow progress towards a systematic and strict adoption of such checklists and guidelines.
しかし、このようなチェックリストやガイドラインの体系的かつ厳格な採用に向けて、研究コミュニティが前進するのは非常に遅いようだ。
In the context of our present work, an important next step would be to make the provision of more detailed information about the hyperparameter tuning process and the sharing of the related software artifacts a mandatory requirement for paper submissions.
我々の研究の文脈では、次のステップとして、ハイパーパラメータのチューニングプロセスに関するより詳細な情報の提供と、関連するソフトウェアの成果物の共有を、論文投稿の必須要件とすることが重要であろう。
The increased use of validated evaluation frameworks such as Elliot is another measure that may help to address the problem.
エリオットのような有効な評価フレームワークの利用を増やすことも、問題解決に役立つかもしれない。
Various alternative frameworks exist, which often not only feature a rich number of baseline algorithms, but also include pre-implemented and validated procedures for systematic hyperparameter tuning and model evaluation.
様々な代替フレームワークが存在し、それらは多くのベースラインアルゴリズムを備えているだけでなく、系統的なハイパーパラメータチューニングとモデル評価のための、あらかじめ実装され検証された手順を含んでいることが多い。
While custom evaluation procedures may be required for specific application scenarios, many of today’s libraries can be used almost off-the-shelf for the most predominant evaluation scenarios, e.g., for traditional matrix-completion problems and top-n recommendation, as well as for alternative scenarios such as session-based recommendation.
特定のアプリケーションシナリオでは、カスタム評価手順が必要になるかもしれないが、今日のライブラリの多くは、従来の行列補完問題やトップN推薦などの最も一般的な評価シナリオや、セッションベースの推薦などの代替シナリオに対して、ほとんどそのまま使用することができる。
However, in the majority of works that we reviewed in the context of this work (see Section 2), researchers did not rely on existing frameworks, which also leads to the risk of unsound evaluation procedures.
しかし、本研究の文脈でレビューした大半の研究（セクション2参照）では、研究者は既存のフレームワークに依存しておらず、これはまた、不健全な評価手順のリスクにつながる。
These problems may both stem from a lack of knowledge about proper evaluation methodology, or they may simply be the result of programming errors.
これらの問題は、いずれも適切な評価方法についての知識不足に起因するものかもしれないし、単にプログラミング・エラーの結果かもしれない。
The use of existing frameworks should therefore be strongly encouraged, both to avoid such mistakes and to increase reproducibility.
従って、このような失敗を避け、再現性を高めるためにも、既存のフレームワークの利用を強く推奨すべきである。
Generally, it seems that increased awareness of this fundamental issue is needed in the community, both on the side of researchers who develop and evaluate new models and on the side of reviewers and journal editors.
一般的に、新しいモデルを開発・評価する研究者側にも、査読者やジャーナル編集者側にも、この基本的な問題に対する認識を高めることが必要であると思われる。
One main instrument in this area may lie in improved education of scholars who are entering the field [5].
この分野の主要な手段のひとつは、この分野に参入する研究者の教育を改善することにあるのかもしれない[5]。
For example, today’s textbooks on recommender systems, e.g., [1, 10], provide in-depth coverage of how to perform offline evaluation and which metrics may be used.
例えば、今日のレコメンダーシステムに関する教科書、例えば[1, 10]は、オフライン評価をどのように行うか、そしてどのメトリクスを使用するかについて深くカバーしている。
Methodological questions of proper hyperparameter tuning for reliable experimental research results are however not discussed in much detail.
しかし、信頼できる実験的研究結果を得るための適切なハイパーパラメータのチューニングに関する方法論的な問題は、あまり詳しく議論されていない。
Thus, it is important that in the future these topics are communicated more frequently through various educational channels, including books, lecture materials, or tutorials.
したがって、今後は書籍、講義資料、チュートリアルなど、さまざまな教育チャンネルを通じて、これらのトピックをより頻繁に伝えることが重要である。
Moreover, explicitly asking researchers to include more information about the hyperparameter tuning in their submitted works and considering this aspect in review forms may certainly increase the awareness of the problem.
さらに、ハイパーパラメータのチューニングに関するより多くの情報を投稿作品に含めるよう研究者に明示的に求めたり、レビューフォームでこの点を考慮したりすることで、この問題に対する認識が確実に高まる可能性がある。
Ultimately, one may speculate to what extent our currently acceptable practice of not reporting in depth about the tuning of the baselines and publication pressure—tuning many models on various datasets can be computationally highly demanding—contribute to the apparent problems in our field.
結局のところ、ベースラインのチューニングや公表圧力について深く報告しないという、現在受け入れられている慣行が、どの程度、この分野の明らかな問題を引き起こしているのかを推測することができる。
Confirmation bias, where researchers have a predisposition to expect that their own model works better than previous ones, may also play a role.
確証バイアスは、研究者が自分のモデルが以前のモデルよりもうまく機能すると期待する素因を持つもので、これも一役買っている可能性がある。
In general, we do not expect to see a radical change of the research practices in our field in the near future, also because many issues, e.g., related to reproducibility, are known for many years now.
一般的に、近い将来、私たちの分野における研究慣行が根本的に変わることはないだろう。なぜなら、再現性など多くの問題は、もう何年も前から知られているからである。
Through constant educational measures and increased awareness—also in the form of the showcase study in this present work–we however believe that we will observe more reliable results in recommender systems research in the future.
しかし、今回のショーケース研究のような不断の啓蒙と意識改革によって、推薦システム研究において、今後、より確かな成果が得られると信じている。
