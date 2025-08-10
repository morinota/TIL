
# Better by Default: Strong Pre-Tuned MLPs and Boosted Trees on Tabular Data デフォルトでより良い: 表形式データにおける強力な事前調整済みMLPとブーステッドツリー

**デビッド・ホルツミュラー[∗]** SIERRAチーム、インリア・パリ・エコール・ノルマル・シュペリウール PSL大学  
**レオ・グリンツタイン** SODAチーム、インリア・サクレー  
**インゴ・シュタインワルト** シュトゥットガルト大学 数学・物理学部 確率論と応用の研究所

## Abstract 要約

For classification and regression on tabular data, the dominance of gradient-boosted decision trees (GBDTs) has recently been challenged by often much slower deep learning methods with extensive hyperparameter tuning. 
表形式データにおける分類と回帰に関して、勾配ブースティング決定木（GBDT）の優位性は、しばしば非常に遅い深層学習手法によって挑戦されていますが、これらの手法は広範なハイパーパラメータの調整を必要とします。
We address this discrepancy by introducing (a) RealMLP, an improved multilayer perceptron (MLP), and (b) strong meta-tuned default parameters for GBDTs and RealMLP. 
私たちは、この不一致に対処するために、(a) **改良された多層パーセプトロン（MLP）であるRealML**Pと、(b) GBDTおよびRealMLPのための**強力なメタ調整済みデフォルトパラメータ**を導入します。
We tune RealMLP and the default parameters on a meta-train benchmark with 118 datasets and compare them to hyperparameter-optimized versions on a disjoint meta-test benchmark with 90 datasets, as well as the GBDT-friendly benchmark by Grinsztajn et al. (2022). 
私たちは、118のデータセットを用いたメタトレインベンチマークでRealMLPとデフォルトパラメータを調整し、90のデータセットを用いた分離されたメタテストベンチマークでハイパーパラメータ最適化されたバージョンと比較し、さらにGrinsztajnら（2022）によるGBDTフレンドリーベンチマークとも比較します。
Our benchmark results on medium-to-large tabular datasets (1K–500K samples) show that RealMLP offers a favorable time-accuracy tradeoff compared to other neural baselines and is competitive with GBDTs in terms of benchmark scores. 
中規模から大規模の表形式データセット（1K–500Kサンプル）における私たちのベンチマーク結果は、RealMLPが他のニューラルベースラインと比較して有利な時間-精度トレードオフを提供し、ベンチマークスコアの点でGBDTと競争力があることを示しています。
Moreover, a combination of RealMLP and GBDTs with improved default parameters can achieve excellent results without hyperparameter tuning. 
さらに、改善されたデフォルトパラメータを持つRealMLPとGBDTの組み合わせは、ハイパーパラメータの調整なしで優れた結果を達成できます。
Finally, we demonstrate that some of RealMLP’s improvements can also considerably improve the performance of TabR with default parameters. 
最後に、RealMLPのいくつかの改善がデフォルトパラメータを持つTabRの性能を大幅に向上させることも示します。

<!-- ここまで読んだ! -->

## 1 Introduction はじめに

Perhaps the most common type of data in practical machine learning (ML) is tabular data, characterized by a fixed number of features (columns) that can take different types such as numerical or categorical, as well as a lack of the spatiotemporal structure found in image or text data.  
おそらく、**実務の機械学習（ML）で最も一般的なデータのタイプはtabular(表形式)データ**であり、固定された数の特徴（列）を持ち、数値やカテゴリカルなどの異なるタイプを取ることができ、画像やテキストデータに見られる時空間構造がないことが特徴です。
The moderate dimension and lack of symmetries make tabular data accessible to a wide variety of machine learning methods.  
中程度の次元と対称性の欠如により、表形式データはさまざまな機械学習手法にアクセス可能です。
Although tabular data is very diverse and no method is dominant on all datasets, gradient-boosted decision trees (GBDTs) exhibit excellent results on benchmarks [18, 43, 58, 69], although their superiority has been challenged by a variety of deep learning methods [3].  
表形式データは非常に多様であり、すべてのデータセットで優位な手法は存在しませんが、勾配ブースティング決定木（GBDT）はベンチマークで優れた結果を示しています[18, 43, 58, 69]が、その優位性はさまざまな深層学習手法によって挑戦されています[3]。 

While many architectures for neural networks (NNs) have been proposed [3], variants of the simple multilayer perceptron (MLP) have repeatedly been shown to be good baselines for tabular NNs [15, 16, 30, 54].  
多くのニューラルネットワーク（NN）のアーキテクチャが提案されています[3]が、単純な多層パーセプトロン（MLP）の変種は、表形式NNの良いベースラインであることが繰り返し示されています[15, 16, 30, 54]。  
Moreover, in terms of training time, MLPs are often slower than GBDTs but still considerably faster than many other architectures [18, 43].  
さらに、**トレーニング時間の観点から、MLPはGBDTよりも遅いことが多いですが、他の多くのアーキテクチャよりはかなり速い**です[18, 43]。  
Therefore, we study how MLPs can be improved in terms of architecture, training, preprocessing, hyperparameters, and initialization.  
したがって、私たちはMLPがアーキテクチャ、トレーニング、前処理、ハイパーパラメータ、および初期化の観点からどのように改善できるかを研究します。 
We also demonstrate that at least some of these improvements can successfully improve TabR [17].  
また、これらの改善の少なくとも一部がTabR [17]を成功裏に改善できることを示します。  

Even with fast and accurate NNs, the cost of extensive hyperparameter optimization can be problematic and hinder the adoption of new methods.  
**高速かつ正確なNNであっても、広範なハイパーパラメータ最適化のコストは問題となり、新しい手法の採用を妨げる可能性**があります。  
To address this issue, we investigate the potential of better dataset-independent default parameters for MLPs and GBDTs.  
この問題に対処するために、MLPとGBDTのためのより良い**データセット非依存のデフォルトパラメータの可能性**を調査します。  
Specifically, we compare the library defaults (D) to our tuned defaults (TD) and (dataset-dependent) hyperparameter optimization (HPO).  
具体的には、ライブラリのデフォルト（D）を私たちの調整されたデフォルト（TD）および（データセット依存の）ハイパーパラメータ最適化（HPO）と比較します。  
Unlike McElfresh et al. [43], who argue in favor HPO on GBDTs over trying NNs, our results show a better time-accuracy trade-off for trying different (tuned) default models, as is done by modern AutoML systems [10, 11]. 
McElfreshら[43]がNNを試すよりもGBDTに対するHPOを支持するのとは異なり、私たちの結果は、現代のAutoMLシステム[10, 11]が行うように、異なる（調整された）デフォルトモデルを試すための時間と精度のトレードオフがより良いことを示しています。  

### 1.1 Contribution** 貢献

The problem of finding better default parameters can be seen as a meta-learning problem [64].  
より良いデフォルトパラメータを見つける問題は、メタ学習の問題[64]として見ることができます。  
We employ a meta-train benchmark consisting of 118 datasets on which the default hyperparameters are optimized, and a disjoint meta-test benchmark consisting of 90 datasets on which they are evaluated.  
私たちは、デフォルトのハイパーパラメータが最適化される118のデータセットからなるメタトレインベンチマークと、それらが評価される90のデータセットからなる分離されたメタテストベンチマークを使用します。  
We consider separate default parameters for classification, optimized for classification error, and for regression, optimized for RMSE.  
分類用のデフォルトパラメータ（分類誤差に最適化）と回帰用のデフォルトパラメータ（RMSEに最適化）を別々に考慮します。  
Our benchmarks do not contain missing numerical values, and we restrict ourselves to sizes between 1K and 500K samples, cf. Section 2.  
私たちのベンチマークには欠損数値が含まれておらず、サンプル数は1Kから500Kの範囲に制限しています（セクション2を参照）。 

In Section 3, we introduce RealMLP, which improves on standard MLPs through a bag of tricks and better default parameters, tuned entirely on the meta-train benchmark.  
セクション3では、メタトレインベンチマークで完全に調整されたトリックのバンドルとより良いデフォルトパラメータを通じて標準MLPを改善するRealMLPを紹介します。  
We introduce many **novel or nonstandard components, such as preprocessing using robust scaling and smooth clipping,** a new numerical embedding variant, a diagonal weight layer, new schedules, different initialization methods, etc.  
**私たちは、ロバストスケーリングとスムーズクリッピングを使用した前処理、新しい数値埋め込みバリアント、対角重み層、新しいスケジュール、異なる初期化方法など、多くの新規または非標準のコンポーネントを導入します。**  
Our benchmark results demonstrate that it often outperforms other comparably fast NNs from the literature and can be competitive with GBDTs.  
私たちのベンチマーク結果は、しばしば文献の他の同等に速いNNを上回り、GBDTと競争できることを示しています。  
To demonstrate that our bag of tricks is useful for other models, we introduce RealTabR-D, a version of TabR [17] including some of our tricks that, despite less extensive tuning, achieves excellent benchmark results.  
私たちのトリックのバンドルが他のモデルにとって有用であることを示すために、私たちはRealTabR-Dを紹介します。これは、私たちのトリックのいくつかを含むTabR [17]のバージョンであり、調整が少ないにもかかわらず優れたベンチマーク結果を達成します。

In Section 4, we provide new default parameters, tuned on the meta-train benchmark, for XGBoost [9], LightGBM [31], and CatBoost [51].  
セクション4では、XGBoost [9]、LightGBM [31]、およびCatBoost [51]のために、メタトレインベンチマークで調整された新しいデフォルトパラメータを提供します。  
While they cannot match HPO on average, they outperform the library defaults on the meta-test benchmark.  
平均してHPOに匹敵することはできませんが、メタテストベンチマークではライブラリのデフォルトを上回ります。  

In Section 5, we evaluate these and other models on the meta-test benchmark and the benchmark by Grinsztajn et al. [18].  
セクション5では、これらおよび他のモデルをメタテストベンチマークおよびGrinsztajnら[18]のベンチマークで評価します。  
We also investigate several possibilities for algorithm selection and ensembling, demonstrating that algorithm selection over default methods provides a better time-performance tradeoff than HPO, thanks to our new improved default parameters and MLP.  
また、アルゴリズム選択とアンサンブルのいくつかの可能性を調査し、デフォルト手法に対するアルゴリズム選択が、私たちの新しい改善されたデフォルトパラメータとMLPのおかげでHPOよりも良い時間とパフォーマンスのトレードオフを提供することを示します。  
The code for our benchmarks, including scikit-learn interfaces for the models, is available at ```          https://github.com/dholzmueller/pytabkit
``` [Our code and data are archived at https://doi.org/10.18419/darus-4555.](https://doi.org/10.18419/darus-4555)  
私たちのベンチマークのコード（モデルのためのscikit-learnインターフェースを含む）は、```          https://github.com/dholzmueller/pytabkit
```で入手可能です。[私たちのコードとデータはhttps://doi.org/10.18419/darus-4555にアーカイブされています。](https://doi.org/10.18419/darus-4555)  
```

### 1.2** **Related Work** 関連研究**

#### **Neural networks** 

Borisov et al. [3] review deep learning on tabular data and identify three main classes of methods: Data transformation methods, specialized architectures, and regularization models.  
Borisovら[3]は表形式データにおける深層学習をレビューし、データ変換手法、専門的なアーキテクチャ、および正則化モデルの3つの主要な手法を特定しています。  
In particular, recent research has mainly focused on specialized architectures based on attention [1, 7, 15, 27], including attention between datapoints [17, 37, 53, 56, 60].  
特に、最近の研究は主にデータポイント間のAttention [1, 7, 15, 27]に基づく専門的なアーキテクチャに焦点を当てています。  
However, these methods are usually significantly slower than MLPs or even GBDTs [17, 18, 43].  
**しかし、これらの手法は通常、MLPやGBDTよりも大幅に遅い**です[17, 18, 43]。
Our research instead expands on improvements to MLPs for tabular data such as the SELU activation function [35], bias initialization methods [61], regularization methods [30], categorical embedding layers [19], and numerical embedding layers [16]. 
私たちの研究は、**SELU活性化関数[35]、バイアス初期化手法[61]、正則化手法[30]、カテゴリカル埋め込み層[19]、および数値埋め込み層[16]など、表形式データのMLPの改善**に拡張します。  

#### Benchmarks

Shwartz-Ziv and Armon [58] benchmarked three deep learning methods and noticed that they performed better on the datasets from their own papers than on other datasets.  
**ベンチマーク** Shwartz-ZivとArmon[58]は3つの深層学習手法をベンチマークし、彼らの論文からのデータセットでより良いパフォーマンスを示したことに気付きました。  
We address this issue by using more datasets and evaluating our methods on datasets that they were not tuned on.  
私たちは、より多くのデータセットを使用し、彼らが調整されていないデータセットで私たちの手法を評価することによってこの問題に対処します。  
Grinsztajn et al. [18], McElfresh et al. [43], and Ye et al. [69] propose larger benchmarks and find that GBDTs still outperform deep learning methods on average, analyzing why and when this is the case.  
Grinsztajnら[18]、McElfreshら[43]、およびYeら[69]はより大きなベンチマークを提案し、GBDTが平均して深層学習手法を上回ることを発見し、なぜそれが起こるのか、いつそれが起こるのかを分析します。  
Kohli et al. [36] also emphasize the need for large benchmarks.  
Kohliら[36]もまた、大規模なベンチマークの必要性を強調しています。  
We evaluate our methods on the benchmark by Grinsztajn et al. [18] as well as datasets from the AutoML benchmark [13] and the OpenML-CTR23 regression benchmark [12].  
私たちは、Grinsztajnら[18]のベンチマークやAutoMLベンチマーク[13]、OpenML-CTR23回帰ベンチマーク[12]のデータセットで私たちの手法を評価します。  

#### **Better defaults** 

Probst et al. [50] study the tunability of ML methods, i.e., the difference in benchmark scores between the best fixed hyperparameters and tuned hyperparameters.  
**より良いデフォルト** Probstら[50]はML手法の調整可能性、すなわち、最良の固定ハイパーパラメータと調整されたハイパーパラメータの間のベンチマークスコアの違いを研究します。  
While their approach involves finding better defaults, they do not evaluate them on a separate meta-test benchmark, only consider classification, and do not provide defaults for LightGBM, CatBoost, and NNs.  
彼らのアプローチはより良いデフォルトを見つけることを含みますが、別のメタテストベンチマークで評価せず、分類のみを考慮し、LightGBM、CatBoost、およびNNのデフォルトを提供していません。  
#### **Meta-learning**

The problem of finding the best fixed hyperparameters is a meta-learning problem [4, 64].  
**メタ学習** 最良の固定ハイパーパラメータを見つける問題はメタ学習の問題です[4, 64]。  
Although we do not introduce or employ a fully automated method to find good defaults, we use a meta-learning benchmark setup to properly evaluate them.  
私たちは良いデフォルトを見つけるための完全自動化された手法を導入または使用しませんが、適切に評価するためのメタ学習ベンチマークセットアップを使用します。  
Wistuba et al. [66] and Pfisterer et al. [49] learn portfolios of configurations and van Rijn et al. [63] learn symbolic defaults, but neither of these papers considers GBDTs or NNs.  
Wistubaら[66]やPfistererら[49]は構成のポートフォリオを学習し、van Rijnら[63]はシンボリックデフォルトを学習しますが、これらの論文のいずれもGBDTやNNを考慮していません。  
Salinas and Erickson [55] learn large portfolios of configurations on an extensive benchmark, without studying the best defaults for individual model families.  
SalinasとErickson[55]は広範なベンチマークで大規模な構成のポートフォリオを学習しますが、個々のモデルファミリーの最良のデフォルトを研究していません。  
Such portfolios are successfully applied in modern AutoML methods [10, 11].  
そのようなポートフォリオは、現代のAutoML手法[10, 11]に成功裏に適用されています。  
At the other end of the meta-learning spectrum, TabPFN [23] meta-learns a (tuning-free) learning method on small synthetic datasets.  
メタ学習のスペクトルの反対側では、TabPFN [23]が小さな合成データセットで（調整不要の）学習手法をメタ学習します。  
Unlike TabPFN, we only meta-learn hyperparameters and can therefore use fewer but larger and more realistic meta-train datasets, resulting in methods that scale to larger datasets.  
TabPFNとは異なり、私たちはハイパーパラメータのみをメタ学習し、したがって、より少ないがより大きく現実的なメタトレインデータセットを使用できるため、より大きなデータセットにスケールする手法を得ることができます。  

## 2 Methodology 方法論

To evaluate a fixed hyperparameter configuration, we need a collection of benchmark _H_ _B[train]_ datasets and a scoring function that computes a benchmark score ( _,_ ) by aggregating the _S_ _B[train]_ _H_ errors attained by the method with hyperparameters on each dataset.  
固定ハイパーパラメータ構成を評価するには、ベンチマーク _H_ _B[train]_ データセットのコレクションと、各データセットでハイパーパラメータを使用して手法が達成した _S_ _B[train]_ _H_ エラーを集約してベンチマークスコア ( _,_ ) を計算するスコアリング関数が必要です。  
However, when optimizing _H_ on, we might overfit to the benchmark and therefore ideally need a second benchmark _H_ _B[train]_ _B[test]_ to get an unbiased score for .  
しかし、_H_ を最適化する際に、ベンチマークに過剰適合する可能性があるため、理想的には、_H_ _B[train]_ _B[test]_ という2つ目のベンチマークが必要です。  
We refer to _,_ as meta-train and meta-test benchmarks and _H_ _B[train]_ _B[test]_ subdivide them into classification and regression benchmarks Bclass[train][,][ B]reg[train][,][ B]class[test] [, and][ B]reg[test][.  
私たちは、_,_ をメタトレインおよびメタテストベンチマークと呼び、_H_ _B[train]_ _B[test]_ を分類および回帰ベンチマーク Bclass[train][,][ B]reg[train][,][ B]class[test][, および][ B]reg[test][に分割します。  
We also use the Grinsztajn et al. [18] benchmark, which allows us to run more expensive _B[Grinsztajn]_ baselines, since it limits training set sizes to 10K samples and contains fewer datasets due to more strict dataset inclusion criteria.  
また、Grinsztajnら[18]のベンチマークを使用します。これは、トレーニングセットのサイズを10Kサンプルに制限し、より厳しいデータセットの包含基準によりデータセットが少なくなるため、より高価な _B[Grinsztajn]_ ベースラインを実行できるようにします。  
Since contains groups of datasets that are variants of the _B[train]_ same dataset, for example by using different columns as targets, we use weighting factors inversely proportional to the group size.  
同じデータセットのバリアントであるデータセットのグループを含むため、たとえば異なる列をターゲットとして使用する場合、グループサイズに反比例する重み付け係数を使用します。  
Table 1 shows some characteristics of the considered benchmarks.  
表1は、考慮されたベンチマークのいくつかの特性を示しています。  
The meta-test benchmark includes datasets that are more extreme in several dimensions, allowing us to test whether our default parameters generalize “out of distribution”.  
メタテストベンチマークには、いくつかの次元でより極端なデータセットが含まれており、私たちのデフォルトパラメータが「分布外」で一般化するかどうかをテストできます。  
For all datasets, we remove rows with missing numerical values and encode missing categorical values as a separate category.  
すべてのデータセットに対して、欠損数値を含む行を削除し、欠損カテゴリカル値を別のカテゴリとしてエンコードします。  
### **2.1** **Benchmark Data Selection**  **ベンチマークデータの選択**  
The meta-train set consists of medium-sized datasets from the UCI Repository [32], adapted from Steinwart [61].  
メタトレインセットは、Steinwart [61]から適応されたUCIリポジトリ[32]の中規模データセットで構成されています。  
The meta-test set consists of the datasets from the AutoML Benchmark [13] as well as the OpenML-CTR23 regression benchmark [12] with a few modifications: we subsample some large datasets and remove datasets that are already contained in the meta-train set, are too small, or have categories with too large cardinality.  
メタテストセットは、AutoMLベンチマーク[13]およびOpenML-CTR23回帰ベンチマーク[12]のデータセットで構成されており、いくつかの修正が加えられています。大規模なデータセットをサブサンプリングし、メタトレインセットにすでに含まれているデータセット、サイズが小さすぎるデータセット、またはカテゴリの基数が大きすぎるデータセットを削除します。  
More details on the datasets and preprocessing can be found in Appendix C.3.  
データセットと前処理の詳細は、付録C.3にあります。  

### **2.2** **Aggregate Benchmark Score**  **集約ベンチマークスコア**  
To optimize the default parameters, we need to define a single benchmark score.  
デフォルトパラメータを最適化するために、単一のベンチマークスコアを定義する必要があります。  
To this end, we evaluate a method on Nsplits = 10 random training-validation-test splits (60%-20%-20%) on each dataset.  
この目的のために、各データセットでNsplits = 10のランダムなトレーニング-バリデーション-テスト分割（60%-20%-20%）で手法を評価します。  
As metrics on individual dataset splits, we use classification error (100% accuracy) or _−_ 1-AUROC(one-vs-rest) for classification and  
個々のデータセット分割のメトリックとして、分類には分類誤差（100%の精度）または _−_ 1-AUROC（one-vs-rest）を使用し、回帰には  
RMSE $nRMSE := \frac{1}{R[2]}$  
を使用します。  
There are various options to aggregate these errors into a single score.  
これらのエラーを単一のスコアに集約するためのさまざまなオプションがあります。  
Some, such as average rank or mean normalized error, depend on which other methods are included in the evaluation, hindering an independent optimization.  
平均ランクや平均正規化誤差などのいくつかは、評価に含まれる他の手法に依存し、独立した最適化を妨げます。  
We would like to use the geometric mean error because arguably, an error reduction from 0.02 to 0.01 is more valuable than an error reduction from 0.42 to 0.41.  
私たちは幾何平均誤差を使用したいと考えています。なぜなら、0.02から0.01への誤差の削減は、0.42から0.41への誤差の削減よりも価値があると考えられるからです。  
However, since the geometric mean error is too sensitive to cases with zero error (especially for classification error), we instead use a shifted geometric mean error, where a small value ε := 0.01 is added to the errors errij before taking the geometric mean:  
しかし、幾何平均誤差はゼロ誤差のケース（特に分類誤差）に対して敏感すぎるため、代わりにシフトされた幾何平均誤差を使用します。ここで、小さな値 ε := 0.01 が誤差 errij に加えられ、幾何平均を取る前に次のようになります：  

$$
SGM_\epsilon := \exp\left(\frac{1}{N_{splits}} \sum_{j=1}^{N_{splits}} \log(err_{ij} + \epsilon)\right)
$$  

Here, we use weights $w_i = \frac{1}{N_{datasets}}$ on the meta-test set and Grinsztajn et al. [18] benchmark.  
ここでは、メタテストセットおよびGrinsztajnら[18]のベンチマークで重み $w_i = \frac{1}{N_{datasets}}$ を使用します。  
On the meta-train set, we make the $w_i$ dependent on the number of related datasets, cf. Appendix C.3.  
メタトレインセットでは、$w_i$ を関連データセットの数に依存させます（付録C.3を参照）。  
In Appendix B.10, we present results for other aggregation strategies.  
付録B.10では、他の集約戦略の結果を示します。

<!-- 2章はあまり興味なかったので飛ばした! -->

## 3 Improving Neural Networks ニューラルネットワークの改善  

The following section presents RealMLP-TD, our improved MLP with tuned defaults, which was designed based on experiments on the meta-train benchmark.  
次のセクションでは、メタトレインベンチマークでの実験に基づいて設計された、調整されたデフォルトを持つ改善されたMLPであるRealMLP-TDを紹介します。  
A simplified version called RealMLP-TD-S is also described.  
RealMLP-TD-Sと呼ばれる簡略化されたバージョンも説明します。  
To demonstrate that our improvements can be useful for other architectures, we introduce RealTabR-D, a version of TabR that includes some of our improvements but has not been tuned as extensively as RealMLP-TD.  
私たちの改善が他のアーキテクチャにとって有用であることを示すために、私たちはRealTabR-Dを紹介します。これは、私たちの改善のいくつかを含むTabRのバージョンですが、RealMLP-TDほど広範に調整されていません。  

### **Data preprocessing** 

In the first step of RealMLP, we apply one-hot encoding to categorical columns with at most eight distinct values (not counting missing values).  
**データ前処理** RealMLPの最初のステップでは、最大8つの異なる値（欠損値を除く）を持つカテゴリカル列にワンホットエンコーディングを適用します。  
Binary categories are encoded to a single feature with values 1, 1.  
バイナリカテゴリは、値1, 1を持つ単一の特徴にエンコードされます。  
Missing values in categorical columns are encoded to zero.  
**カテゴリカル列の欠損値はゼロにエンコード**されます。
<!-- 下記は、one-hotエンコーディングされたカテゴリ特徴量を含む全ての数値カラムについての前処理の説明! -->
After that, all numerical columns, including the one-hot encoded ones, are preprocessed independently as follows: 
**その後、ワンホットエンコードされた列を含むすべての数値列は、次のように独立して前処理されます**： 
Let $x_1, \ldots, x_n \in \mathbb{R}$ be the values in column $i$, and let $q_p$ be the $p$-quantile of $(x_1, \ldots, x_n) \in \mathbb{R}$ for $p \in [0, 1]$.  
ここで $x_1, \ldots, x_n \in \mathbb{R}$ は列$i$の値であり、$q_p$は$(x_1, \ldots, x_n) \in \mathbb{R}$の$p$-分位数です（$p \in [0, 1]$）。
Then,  
その後、

$$
x_{j, processed} := f(s_j(x_j - q_{1/2})), 
\quad f(x) := \frac{x}{ \sqrt{1 + (x/3)^2} }
$$

$$
s_j := \begin{cases}
\frac{1}{q_{3/4} - q_{1/4}} & \text{if } q_{3/4} \neq q_{1/4}
\\
\frac{2}{q_{1} - q_0} & \text{if } q_{3/4} = q_{1/4} \text{ and } q_1 \neq q_0
\\
0 & \text{otherwise.}
\end{cases}
$$

In scikit-learn [48], this corresponds to applying a RobustScaler (first case) or MinMaxScaler (second case), and then the function $f$, which smoothly clips its input to the range (-3, 3).  
scikit-learn [48]では、これは**ロバストスケーラー**（最初のケース）または**MinMaxスケーラー**（2番目のケース）を適用し、その後、入力を範囲（-3, 3）にスムーズにクリップする関数$f$を適用することに相当します。
Smooth clipping functions like $f$ have been used by, e.g., Holzmüller et al. [24] and Hafner et al. [20]. 
$f$のような**スムーズクリッピング関数**は、たとえばHolzmüllerら[24]やHafnerら[20]によって使用されています。  
Intuitively, when features have large outliers, smooth clipping prevents the outliers from affecting the result too strongly, while robust scaling prevents the outliers from affecting the inlier scaling.  
直感的には、特徴に大きな外れ値がある場合、スムーズクリッピングは外れ値が結果に強く影響を与えるのを防ぎ、ロバストスケーリングは外れ値が内挿スケーリングに影響を与えるのを防ぎます。  

<!-- ここまで読んだ! -->

### NN architecture**

Our architecture, visualized in Figure 1 (a), is a multilayer perceptron (MLP) with three hidden layers containing 256 neurons each, except for the following additions and modifications:  
**NNアーキテクチャ** 私たちのアーキテクチャは、図1（a）に示されているように、**256ニューロンを含む3つの隠れ層を持つ多層パーセプトロン（MLP）**です。また、以下の追加と変更を除きます：

#### 工夫1

- RealMLP-TD employs categorical embedding layers [19] to embed the remaining categorical features with cardinality > 8.  
- RealMLP-TDは、**基数が8を超える残りのカテゴリカル特徴を埋め込むためにカテゴリカル埋め込み層[19]を使用**します。

#### 工夫2: 

- For numerical features, excluding the one-hot encoded ones, we introduce PBLD (periodic bias linear DenseNet) embeddings, which concatenate the original value to the PL embeddings proposed by Gorishniy et al. [16] and use a different periodic embedding with biases,  
  - **one-hotエンコードされたものを除く数値特徴量には**、Gorishniyら[16]によって提案されたPL埋め込みに元の値を連結し、バイアスを持つ異なる周期的埋め込みを使用する**PBLD（周期的バイアス線形DenseNet）埋め込み**を導入します。
  - inspired by Huang et al. [26] and Rahimi and Recht [52], respectively.  
  - これはそれぞれHuangら[26]とRahimiとRecht [52]に触発されています。
  - PBLD embeddings apply separate small two-layer MLPs to each feature $x_i$ as 
  - PBLD埋め込みは、各特徴 $x_i$ に対して別々の小さな2層MLPを適用します。

$$
(x_{i}, W^{(2, i)}_{emb} \cdot cos(2 \pi w^{(1, i)}_{emb} x_{i} + b^{(1, i)}_{emb}) + b^{(2, i)}_{emb}) \in \mathbb{R}^{4},
$$

For efficiency reasons, we use 4-dimensional embeddings with $w^{(1)}_{\text{emb},i}, b^{(1)}_{\text{emb},i} \in \mathbb{R}^{16}, b^{(2)}_{\text{emb},i} \in \mathbb{R}^{3}, W^{(2)}_{\text{emb},i} \in \mathbb{R}^{3 \times 16}.$  
効率の理由から、4次元埋め込みを使用します。$w^{(1)}_{\text{emb},i}, b^{(1)}_{\text{emb},i} \in \mathbb{R}^{16}, b^{(2)}_{\text{emb},i} \in \mathbb{R}^{3}, W^{(2)}_{\text{emb},i} \in \mathbb{R}^{3 \times 16}$の4次元埋め込みを使用します。

#### 工夫3:

To encourage (soft) feature selection, we introduce a scaling layer before the first linear layer, which is simply a matrix-vector product with a diagonal weight matrix.  
（ソフト）特徴選択を促進するために、最初の線形層の前に**スケーリング層**を導入します。これは、対角重み行列との行列-ベクトル積に過ぎません。
In other words, it computes $x_{i,out} = s_i x_{i,in}$, with a learnable scaling factor $s_i$ for each feature $i$.  
言い換えれば、各特徴$i$に対して学習可能なスケーリング因子$s_i$を持ち、$x_{i,out} = s_i x_{i,in}$を計算します。  
We found it beneficial to use a larger learning rate for this layer.  
この層には大きな学習率を使用することが有益であることがわかりました。  

#### 工夫4:

Our linear layers use the neural tangent parametrization (NTP) as proposed by Jacot et al. [28], i.e., they compute  
私たちの線形層は、Jacotら[28]が提案した**ニューラル接線パラメータ化（NTP）**を使用します。すなわち、彼らは次のように計算します。

$$
z^{(l+1)} = d_l \frac{1}{2} W^{(l)} x^{(l)} + b^{(l)},
$$  

where $d_l$ is the dimension of the layer input $x^{(l)}$.  
ここで、$d_l$は層入力$x^{(l)}$の次元です。  
The motivation behind the use of the NTP here is that it effectively modifies the learning rate for the weight matrices depending on the input dimension $d_l$, hopefully preventing too large steps whenever the number of columns is large.  
ここでNTPを使用する動機は、入力次元$d_l$に応じて重み行列の学習率を効果的に修正し、列数が多いときに過度に大きなステップを防ぐことを期待しています。  
We did not observe improvements when using the Adam version of the maximal update parametrization [68].  
最大更新パラメータ化[68]のAdamバージョンを使用した際には改善が見られませんでした。  

#### 工夫5:

RealMLP-TD uses parametric activation functions inspired by PReLU [21].  
RealMLP-TDはPReLU[21]に触発された**パラメトリック活性化関数**を使用します。  
In general, for an activation function $\sigma$, we define a parametric version with separate learnable $\alpha_i$ for each neuron $i$:  
一般に、活性化関数$\sigma$に対して、各ニューロン$i$に対して別々の学習可能な$\alpha_i$を持つパラメトリックバージョンを定義します：  

$$
\sigma_{\alpha_i}(x_i) = (1 - \alpha_i)x_i + \alpha_i \sigma(x_i).
$$  

When $\alpha_i = 1$, this recovers $\sigma$, and when $\alpha_i = 0$, the activation function is linear.  
$\alpha_i = 1$のとき、これは$\sigma$を回復し、$\alpha_i = 0$のとき、活性化関数は線形になります。
As activation functions, we use SELU [35] for classification and Mish [45] for regression.  
活性化関数として、分類にはSELU[35]、回帰にはMish[45]を使用します。  

#### 工夫6:

We use dropout after each activation function.  
**各活性化関数の後にドロップアウトを使用**します。 
We do not use the Alpha-dropout variant originally proposed for SELU [35], as we were not able to obtain good results with it.  
SELU[35]のために元々提案されたAlpha-dropoutバリアントは使用しません。なぜなら、良い結果を得ることができなかったからです。  

#### 工夫7:

For regression, at test time, the MLP outputs are clipped to the observed range during training.  
回帰の場合、テスト時にMLPの出力はトレーニング中に観察された範囲にクリップされます。  
(We observed that this is mainly helpful for suboptimal hyperparameters.)  
（これは主に最適でないハイパーパラメータに対して有益であることがわかりました。） 

<!-- ここまで読んだ! -->

### **Initialization** 

The parameters $s_i$ of the scaling layer are initialized to 1, making it an identity function at initialization.  
**初期化** スケーリング層のパラメータ$s_i$は1に初期化され、初期化時に恒等関数になります。  
Similarly, the parameters $\alpha_i$ of the parametric activation functions are initialized to 1, recovering the standard activation functions at initialization.  
同様に、パラメトリック活性化関数のパラメータ$\alpha_i$は1に初期化され、初期化時に標準の活性化関数を回復します。  
We initialize weights and biases in a data-dependent fashion during a forward pass on the (possibly subsampled) training set.  
重みとバイアスは、（おそらくサブサンプリングされた）トレーニングセットでのフォワードパス中にデータ依存的に初期化します。  
We rescale rows of standard-normal-initialized weight matrices to scale the variance of the output pre-activations over the dataset to one.  
標準正規初期化された重み行列の行を再スケーリングして、データセット全体の出力前活性化の分散を1にスケールします。  
For the biases, we use the data-dependent he+5 initialization method [called hull+5 in 61].  
バイアスには、データ依存のhe+5初期化手法[61でhull+5と呼ばれる]を使用します。  

<!-- ここまで読んだ! -->

### **Training** 

Like Gorishniy et al. [15], we use the AdamW optimizer [34, 40].  
**トレーニング** Gorishniyら[15]のように、私たちはAdamWオプティマイザ[34, 40]を使用します。  
We set its momentum hyperparameters to $\beta_1 = 0.9$ and $\beta_2 = 0.95$ instead of the default $\beta_2 = 0.999$.  
そのモーメンタムハイパーパラメータをデフォルトの$\beta_2 = 0.999$の代わりに$\beta_1 = 0.9$および$\beta_2 = 0.95$に設定します。  
The idea to use a smaller value for $\beta_2$ is adopted from the fastai tabular MLP [25].  
$\beta_2$に小さな値を使用するというアイデアは、fastaiのタブラーMLP[25]から採用されています。  
RealMLP is optimized for 256 epochs with a batch size of 256.  
RealMLPは256エポック、バッチサイズ256で最適化されます。  
As a loss function for classification, we use softmax + cross-entropy with label smoothing [62] with parameter $\epsilon = 0.1$.  
分類の損失関数として、ラベルスムージング[62]を用いたsoftmax + クロスエントロピーをパラメータ$\epsilon = 0.1$で使用します。  
For regression, we use the MSE loss and affinely transform the targets to have zero mean and unit variance on the training and validation set.  
回帰にはMSE損失を使用し、ターゲットをアフィン変換してトレーニングおよびバリデーションセットでゼロ平均および単位分散を持たせます。  

<!-- ここまで読んだ! -->

### **Hyperparameters** 

We allow parameter-specific scheduled hyperparameters computed in each iteration using a base value, optional parameter-specific factors, and a schedule, as  
**ハイパーパラメータ** 各イテレーションで基準値、オプションのパラメータ固有の係数、およびスケジュールを使用して計算されたパラメータ固有のスケジュールハイパーパラメータを許可します。  

$$
\text{base_value} \cdot \text{param_factor} \cdot \text{schedule}(\frac{\text{iteration}}{\text{#iterations}})
$$

allowing us, for example, to use a high learning rate factor for scaling layer parameters.  
これにより、たとえばスケーリング層パラメータに高い学習率係数を使用できます。  
Because we do not tune the number of epochs separately on each dataset, we use a multi-cycle learning rate schedule, providing multiple valleys that are usually preferable for stopping the training, while allowing high learning rates in between.  
各データセットでエポック数を個別に調整しないため、マルチサイクル学習率スケジュールを使用し、通常はトレーニングを停止するのに好ましい複数の谷を提供し、その間に高い学習率を許可します。  
Our schedule is similar to Loshchilov and Hutter [39] and Smith [59], but with a simpler analytical expression:  
私たちのスケジュールはLoshchilovとHutter[39]およびSmith[59]に似ていますが、より単純な解析的表現を持っています: 

$$
\text{coslog}_k(t) := \frac{1}{2} \left(1 - \cos\left(2\pi \log_2(1 + (2^k - 1)t)\right)\right).
$$  

We set $k = 4$ to obtain four cycles as shown in Figure 1 (b).  
$k = 4$に設定して、図1（b）に示すように4つのサイクルを取得します。  
To allow stopping at different levels of regularization, we schedule dropout and weight decay using the following schedule, cf. Figure 1 (b):  
異なる正則化レベルで停止できるように、次のスケジュールを使用してドロップアウトと重み減衰をスケジュールします（図1（b）を参照): 

$$
\text{flat\_cos}(t) := \frac{1}{2} \left(1 + \cos\left(\pi \max\{1, 2t\} - 1\right)\right).
$$  

The detailed hyperparameters can be found in Table A.1.  
詳細なハイパーパラメータは表A.1にあります。 

<!-- ここまで読んだ! -->

### **Best-epoch selection** 

Due to the multi-cycle learning rate schedule, we do not perform classical early stopping.  
**最良エポックの選択** マルチサイクル学習率スケジュールのため、古典的な早期停止は行いません。  
Instead, we always train for the full 256 epochs and then revert the model to the epoch with the lowest validation error, which in this paper is based on classification error, or RMSE for regression.  
代わりに、常に256エポックを完全にトレーニングし、その後、モデルを最も低いバリデーションエラーのエポックに戻します。これは、この論文では分類誤差に基づいており、回帰の場合はRMSEです。  
In case of a tie, we found it beneficial to use the last of the tied best epochs.  
同点の場合、最良のエポックの最後のものを使用することが有益であることがわかりました。  

<!-- ここまで読んだ! -->

### **RealMLP-TD-S** 

Since certain aspects of RealMLP-TD are somewhat complex to implement, we introduce a simplified (and faster) variant called RealMLP-TD-S in Appendix A.  
**RealMLP-TD-S** RealMLP-TDの特定の側面が実装するのがやや複雑であるため、付録AにRealMLP-TD-Sと呼ばれる簡略化された（および高速な）バリアントを導入します。  
Among the simplifications are: omitting embedding layers, using non-parametric activations, using a simpler initialization method, and omitting dropout and weight decay.  
簡略化の中には、埋め込み層の省略、非パラメトリック活性化の使用、より単純な初期化手法の使用、ドロップアウトと重み減衰の省略があります。  
2inspired by a similar schedule in `https://github.com/lessw2020/` ``` Ranger-Deep-Learning-Optimizer

### **RealTabR-D**

For RealTabR-D, we adapt TabR-S-D by using our numerical preprocessing, setting Adam’s $\beta_2$ to 0.95, using our scaling layer with a modification to amplify the effective learning rate by a factor of 96, adding PBLD embeddings for numerical features, and adding label smoothing for classification.  
**RealTabR-D** RealTabR-Dでは、数値前処理を使用し、Adamの$\beta_2$を0.95に設定し、効果的な学習率を96倍に増幅するための修正を加えたスケーリング層を使用し、数値特徴のためのPBLD埋め込みを追加し、分類のためのラベルスムージングを追加することによってTabR-S-Dを適応させます。  
More details can be found in Appendix A.3.  
詳細は付録A.3にあります。  

<!-- ここまで雑に読んだ! -->

#### 4 Gradient-Boosted Decision Trees 勾配ブースト決定木

To find better default hyperparameters for GBDTs, we employ a semi-automatic approach: 
GBDTのためのより良いデフォルトハイパーパラメータを見つけるために、半自動アプローチを採用します。

We use hyperparameter optimization libraries like hyperopt [2] and SMAC3 [38] to explore a reasonably large hyperparameter space, 
hyperopt [2]やSMAC3 [38]のようなハイパーパラメータ最適化ライブラリを使用して、適切に大きなハイパーパラメータ空間を探索し、

evaluating the benchmark score of each configuration on the meta-train benchmarks, 
各構成のベンチマークスコアをメタトレインベンチマークで評価し、

and then perform some small manual adjustments like rounding the best obtained hyperparameters. 
その後、得られた最良のハイパーパラメータを四捨五入するなどの小さな手動調整を行います。

To balance efficiency and accuracy, we fix the number of estimators to 1000 and use the hist method for XGBoost. 
効率と精度のバランスを取るために、推定器の数を1000に固定し、XGBoostにはhistメソッドを使用します。

We only consider the libraries’ default tree-building strategies since it is one of their main differences. 
ライブラリのデフォルトの木構築戦略のみを考慮します。これは、それらの主な違いの1つだからです。

The tuned defaults (TD) for LightGBM (LGBM), XGBoost (XGB), and CatBoost can be found in Table C.1, C.2, and C.3, respectively. 
LightGBM (LGBM)、XGBoost (XGB)、およびCatBoostの調整されたデフォルト（TD）は、それぞれ表C.1、C.2、およびC.3に示されています。

While some of the obtained hyperparameter values might be sensitive to the tuning and benchmark setup, 
得られたハイパーパラメータの値のいくつかは、チューニングやベンチマークの設定に敏感である可能性がありますが、

we observe some general trends. 
いくつかの一般的な傾向を観察します。

First, row subsampling is used in all tuned defaults, while column subsampling is rarely applied. 
まず、すべての調整されたデフォルトで行サブサンプリングが使用されているのに対し、列サブサンプリングはほとんど適用されていません。

Second, trees are generally allowed to be deeper for regression than for classification. 
第二に、回帰のためには分類よりも一般的に木が深くなることが許可されています。

Third, the Bernoulli bootstrap in CatBoost is competitive with the Bayesian bootstrap while also being faster. 
第三に、CatBoostのベルヌーイブートストラップは、ベイジアンブートストラップと競争力があり、かつ速いです。



#### 5 Experiments 実験

In the following, we evaluate different methods with library defaults (D), tuned defaults (TD), and hyperparameter optimization (HPO). 
以下では、ライブラリのデフォルト（D）、調整されたデフォルト（TD）、およびハイパーパラメータ最適化（HPO）を用いて異なる手法を評価します。

Recall that TD uses fixed parameters optimized on the meta-train benchmarks, while HPO tunes hyperparameters on each dataset split independently. 
TDはメタトレインベンチマークで最適化された固定パラメータを使用し、HPOは各データセットの分割ごとにハイパーパラメータを独立して調整することを思い出してください。

All methods except random forests select the best iteration/epoch on the validation set of the respective dataset split based on accuracy / RMSE. 
ランダムフォレストを除くすべての手法は、精度/RMSEに基づいて、それぞれのデータセット分割の検証セットで最良のイテレーション/エポックを選択します。

All NN-based regression methods standardize the labels for training. 
すべてのNNベースの回帰手法は、トレーニングのためにラベルを標準化します。

**5.1** **Methods 手法**

We provide methods in the following variants: 
以下のバリエーションで手法を提供します：

- D: Default parameters, taken from the original library if possible (Appendix C.1). 
- D: デフォルトパラメータ（可能であれば元のライブラリから取得、付録C.1）。

- TD: Tuned default parameters from Section 3 and Section 4. 
- TD: セクション3およびセクション4からの調整されたデフォルトパラメータ。

- HPO: Hyperparameters optimized separately for every train-test split on every dataset, using 50 steps of random search. 
- HPO: 各データセットのすべてのトレイン-テスト分割に対して、50ステップのランダムサーチを使用して個別に最適化されたハイパーパラメータ。

Search spaces are specified in Appendix C.2 and are usually adapted from original or popular papers. 
探索空間は付録C.2に指定されており、通常は元の論文や人気のある論文から適応されています。

As tree-based methods, we use XGBoost (XGB), LightGBM (LGBM), and CatBoost from the respective libraries, as well as random forest (RF) from scikit-learn. 
ツリーベースの手法として、私たちはそれぞれのライブラリからXGBoost（XGB）、LightGBM（LGBM）、CatBoostを使用し、scikit-learnからランダムフォレスト（RF）も使用します。

The variant XGB-PBB-D uses meta-learned default parameters from Probst et al. [50]. 
バリアントXGB-PBB-Dは、Probstら[50]からのメタ学習されたデフォルトパラメータを使用します。

For neural methods, we compare to MLP, **ResNet, and FT-Transformer (FTT) from Gorishniy et al. [15], MLP-PLR from Gorishniy et al. [16], as well as TabR and TabR-S (without numerical embeddings) from Gorishniy et al. [17].** 
ニューラル手法については、MLP、**Gorishniyら[15]のResNetおよびFT-Transformer（FTT）、Gorishniyら[16]のMLP-PLR、Gorishniyら[17]のTabRおよびTabR-S（数値埋め込みなし）と比較します。**

We compare these methods to RealMLP and RealTabR from Section 3. 
これらの手法をセクション3のRealMLPおよびRealTabRと比較します。

In addition, we investigate Best, which on each dataset split selects the method with the best validation score out of XGB, LGBM, CatBoost, and MLP-PLR (for Best-D) or RealMLP (for Best-TD and Best-HPO). 
さらに、各データセット分割でXGB、LGBM、CatBoost、およびMLP-PLR（Best-Dの場合）またはRealMLP（Best-TDおよびBest-HPOの場合）の中で最良の検証スコアを持つ手法を選択するBestを調査します。

Ensemble builds a weighted ensemble out of the same methods as Best, using the method of Caruana et al. [5] with 40 greedy selection steps as in Salinas and Erickson [55]. 
アンサンブルは、SalinasとErickson[55]のように、Caruanaら[5]の手法を使用してBestと同じ手法から重み付きアンサンブルを構築します。

We do not run FTT, RF-HPO, and TabR-HPO on all benchmarks since some benchmarks (especially meta-test) are more expensive to run and these methods may run into out-of-memory errors. 
FTT、RF-HPO、およびTabR-HPOは、いくつかのベンチマーク（特にメタテスト）が実行コストが高いため、すべてのベンチマークで実行しません。これらの手法は、メモリ不足エラーに遭遇する可能性があります。

**5.2** **Results 結果**

Figure 2 shows the results of the aforementioned methods on all benchmarks, along with their runtimes on a CPU. 
図2は、前述の手法のすべてのベンチマークにおける結果と、CPU上での実行時間を示しています。

Note that XGB results on some (mainly meta-test) datasets are affected by a bug _in handling rare categories, see Appendix B._  
一部の（主にメタテスト）データセットにおけるXGBの結果は、_稀なカテゴリの処理に関するバグの影響を受けることに注意してください。付録Bを参照してください。_

-----
Figure 2: Benchmark scores on all benchmarks vs. average training time. The y-axis shows the shifted geometric mean (SGMε) classification error (left) or nRMSE (right) as explained in Section 2.2. The x-axis shows average training times per 1000 samples (measured on for _B[train]_ efficiency reasons), see Appendix C.7. The error bars are approximate 95% confidence intervals for the limit #splits, see Appendix C.6. Note that XGB results on some (mainly meta-test) datasets _→∞_ _are affected by a bug in handling rare categories, see Appendix B._  
-----
図2：すべてのベンチマークにおけるベンチマークスコアと平均トレーニング時間の比較。y軸は、セクション2.2で説明されているように、シフトされた幾何平均（SGMε）分類誤差（左）またはnRMSE（右）を示します。x軸は、1000サンプルあたりの平均トレーニング時間（_B[train]_効率の理由で測定）を示し、付録C.7を参照してください。エラーバーは、制限#splitsの95%信頼区間の近似値であり、付録C.6を参照してください。一部の（主にメタテスト）データセットにおけるXGBの結果は、_→∞_ _稀なカテゴリの処理に関するバグの影響を受けることに注意してください。付録Bを参照してください。_

|Col1|Col2|Col3| 
|---|---|---| 
| | | | 
| | | | 
|r| | | 
|b e tte| | | |  
図3：AUCに対するベンチマークスコアと平均トレーニング時間の比較。「no LS」とラベル付けされた手法は、ラベルスムージングを無効にします。停止と最良エポックの選択は精度に基づいて行われ、HPOはAUCに基づいて行われます。交差エントロピーでの停止については、図B.3を参照してください。y軸は、セクション2.2で説明されているように、シフトされた幾何平均（SGMε）1 − AUCを示します。x軸は、効率の理由で測定された1000サンプルあたりの平均トレーニング時間を示し、付録C.7を参照してください。エラーバーは、制限#splitsの95%信頼区間の近似値であり、付録C.6を参照してください。

_→∞_

**How good are tuned defaults on new datasets?** To answer this question, we compare the relative gaps between TD and HPO benchmark scores on the meta-test benchmarks to those on the meta-train benchmarks. 
**新しいデータセットにおける調整されたデフォルトはどれほど良いか？** この質問に答えるために、メタテストベンチマークにおけるTDとHPOのベンチマークスコアの相対的なギャップをメタトレインベンチマークのそれと比較します。

The gap between RealMLP-HPO and RealMLP-TD is not much larger on the meta-test benchmarks, indicating that the tuned defaults transfer very well to the meta-test benchmark. 
RealMLP-HPOとRealMLP-TDのギャップはメタテストベンチマークではそれほど大きくなく、調整されたデフォルトがメタテストベンチマークに非常によく移行することを示しています。

For GBDTs, tuned defaults are competitive with HPO on the meta-train set, but not as good on the meta-test set. 
GBDTに関しては、調整されたデフォルトはメタトレインセットでHPOと競争力がありますが、メタテストセットではそれほど良くありません。

Still, they are considerably better than the untuned defaults on the meta-test set. 
それでも、メタテストセットでは未調整のデフォルトよりもかなり優れています。

Note that we did not limit the TD parameters to the literature search spaces for the HPO models (cf. Appendix C.2); for example, XGB-TD uses a smaller value of min_child_weight for classification and CatBoost-TD uses deeper trees and Bernoulli boosting. 
TDパラメータをHPOモデルの文献検索空間に制限しなかったことに注意してください（付録C.2を参照）。たとえば、XGB-TDは分類のためにmin_child_weightの小さい値を使用し、CatBoost-TDはより深い木とベルヌーイブースティングを使用します。

The XGBoost defaults XGB-PBB-D from Probst et al. [50] outperform XGB-TD on Bclass[test] [, perhaps because their benchmark is more] similar to Bclass[test] [or because XGB-PBB-D uses more estimators (4168) and deeper trees.] 
Probstら[50]からのXGBoostデフォルトXGB-PBB-Dは、Bclass[test]でXGB-TDを上回ります。おそらく、彼らのベンチマークがBclass[test]により類似しているか、XGB-PBB-Dがより多くの推定器（4168）とより深い木を使用しているためです。

**RealMLP and RealTabR perform strongly among NNs.** On most benchmarks, RealMLP-TD and RealTabR-D bring considerable improvements over MLP-PLR-D and TabR-S-D, at slightly larger runtimes, respectively. 
**RealMLPとRealTabRはNNの中で強力に機能します。** ほとんどのベンチマークで、RealMLP-TDとRealTabR-Dは、MLP-PLR-DおよびTabR-S-Dに対してそれぞれわずかに大きな実行時間でかなりの改善をもたらします。

Similarly, RealMLP-HPO improves the results of MLP-PLR-HPO. 
同様に、RealMLP-HPOはMLP-PLR-HPOの結果を改善します。

TabR and FTT are notably slower than MLP-based methods on CPUs, while the difference is less pronounced on GPUs (Figure C.2). 
TabRとFTTは、CPU上ではMLPベースの手法よりも著しく遅いですが、GPU上ではその差はあまり顕著ではありません（図C.2）。

While RealMLP-TD beats TabR-S-D on many benchmarks, RealTabR-D performs even better on four out of six benchmarks, especially all regression benchmarks. 
RealMLP-TDは多くのベンチマークでTabR-S-Dを上回りますが、RealTabR-Dは6つのベンチマークのうち4つでさらに優れた性能を発揮し、特にすべての回帰ベンチマークで優れています。

On the Grinsztajn et al. [18] benchmark where we can afford to run more baselines, TabR-HPO performs best according to many aggregation metrics. 
私たちがより多くのベースラインを実行できるGrinsztajnら[18]のベンチマークでは、TabR-HPOが多くの集約メトリックにおいて最良の性能を発揮します。

It performs especially well on the electricity dataset, where MLPs struggle to learn high-frequency patterns [18]. 
特に、MLPが高周波パターンを学習するのに苦労する電力データセットで優れた性能を発揮します[18]。

**RealMLP and RealTabR are competitive with tree-based models.** On the meta-train and meta-test benchmarks, RealMLP and RealTabR perform better than GBDTs in terms of shifted geometric mean error, while also being comparable or slightly better in terms of other aggregations like mean normalized error (Appendix B.10) or win-rates (Appendix B.12). 
**RealMLPとRealTabRはツリーベースのモデルと競争力があります。** メタトレインおよびメタテストベンチマークにおいて、RealMLPとRealTabRはシフトされた幾何平均誤差の観点でGBDTよりも優れた性能を発揮し、平均正規化誤差（付録B.10）や勝率（付録B.12）などの他の集約においても同等またはわずかに優れています。

On the Grinsztajn et al. [18] benchmark, RealMLP performs worse than CatBoost for classification and comparably for regression, while RealTabR-D performs comparably to CatBoost-TD for classification and better for regression. 
Grinsztajnら[18]のベンチマークでは、RealMLPは分類においてCatBoostよりも劣り、回帰においては同等の性能を発揮しますが、RealTabR-Dは分類においてCatBoost-TDと同等で、回帰においてはより優れた性能を発揮します。

**Among GBDTs, CatBoost defaults are better and slower.** Several papers have found CatBoost to perform favorably among GBDTs while being more computationally expensive to train [8, 33, 43, 51, 69]. 
**GBDTの中では、CatBoostのデフォルトがより優れており、遅いです。** いくつかの論文では、CatBoostがGBDTの中で有利に機能し、トレーニングにおいてより計算コストが高いことが示されています[8, 33, 43, 51, 69]。

We observe the same for our tuned defaults on most benchmarks. 
私たちは、ほとんどのベンチマークにおいて調整されたデフォルトでも同様のことを観察します。

-----
**Simply trying all default algorithms is faster and very often better than (naive) single-algorithm HPO.** 
**すべてのデフォルトアルゴリズムを単純に試すことは、（ナイーブな）単一アルゴリズムHPOよりも速く、非常にしばしば優れています。**

When comparing Best-TD to 50-step HPO on RealMLP or GBDTs, we notice that Best-TD is faster on average, while also being competitive with the best of the HPO models. 
Best-TDをRealMLPまたはGBDTの50ステップHPOと比較すると、Best-TDは平均して速く、HPOモデルの中で最良のものと競争力があることに気付きます。

In comparison, BestD is often outperformed by RealMLP-HPO. 
比較すると、BestDはしばしばRealMLP-HPOに劣ります。

We also note that ensemble selection [5] usually gives 0–3% improvement on the benchmark score compared to selecting the best model, and can potentially be further improved [6]. 
また、アンサンブル選択[5]は通常、最良のモデルを選択するのに比べてベンチマークスコアを0〜3%改善することが多く、さらに改善の余地があります[6]。

Unlike McElfresh et al. [43], who argue in favor of CatBoost-HPO over trying NNs, our results favor model portfolios as used in modern AutoML systems [10]. 
NNを試すよりもCatBoost-HPOを支持するMcElfreshら[43]とは異なり、私たちの結果は現代のAutoMLシステムで使用されるモデルポートフォリオを支持します[10]。

**Analyzing NN improvements** 
**NNの改善を分析する**

Figure 1 (c) shows how adding the proposed RealMLP components to a simple MLP improves the meta-train benchmark performance. 
図1(c)は、提案されたRealMLPコンポーネントをシンプルなMLPに追加することでメタトレインベンチマークの性能が向上する様子を示しています。

However, these results depend on the order in which components are added, which is addressed by a separate ablation study in Appendix B. 
ただし、これらの結果はコンポーネントが追加される順序に依存しており、これは付録Bの別のアブレーション研究で扱われています。

For example, the large weight decay value makes RealMLP-TD sensitive to changes in some other hyperparameters like β2. 
たとえば、大きな重み減衰値はRealMLP-TDをβ2のような他のいくつかのハイパーパラメータの変化に敏感にします。

We also show in Appendix B.8 that our architectural improvements alone are beneficial when applied to MLP-D directly, although non-architectural aspects are at least as important. 
また、付録B.8では、私たちのアーキテクチャの改善がMLP-Dに直接適用された場合に有益であることを示していますが、非アーキテクチャ的な側面も同様に重要です。

In particular, our numerical preprocessing is easy to adopt and often beneficial for other NNs as well (Appendix B.7). 
特に、私たちの数値前処理は採用が容易であり、他のNNにもしばしば有益です（付録B.7）。

The scaling layer and PBLD embeddings are easy to use and turned out to be effective within RealTabR-D as well. 
スケーリング層とPBLD埋め込みは使いやすく、RealTabR-D内でも効果的であることが判明しました。

If affordable, larger stopping patiences and the use of (cyclic) learning rate schedules can be useful, while label smoothing is influential but can be detrimental for metrics like AUROC (Figure 3, Appendix B.5). 
もし可能であれば、より大きな停止耐性と（周期的）学習率スケジュールの使用が有用であり、ラベルスムージングは影響を与えますが、AUROCのようなメトリックには有害である可能性があります（図3、付録B.5）。

**Dependence on benchmark choices** 
**ベンチマーク選択への依存**

We observe that choices in benchmark design can affect the interpretation of the results. 
ベンチマーク設計の選択が結果の解釈に影響を与えることを観察します。

The use of different aggregation metrics than the shifted geometric mean reduces the advantage of TD methods (Appendix B.10). 
シフトされた幾何平均とは異なる集約メトリックの使用は、TD手法の利点を減少させます（付録B.10）。

For classification, using AUROC instead of classification error (Figure 3, Appendix B.5) favors GBDTs. 
分類においては、分類誤差の代わりにAUROCを使用すること（図3、付録B.5）はGBDTに有利です。

Different dataset selection and preprocessing criteria on different benchmarks lead to large differences between benchmarks in the average errors, as indicated by the y-axis scaling in Figure 2. 
異なるベンチマークにおけるデータセット選択と前処理基準の違いは、図2のy軸スケーリングに示されているように、ベンチマーク間の平均誤差に大きな違いをもたらします。

**Further insights** 
**さらなる洞察**

In Appendix B, we present additional experimental results. 
付録Bでは、追加の実験結果を示します。

We compare bagging and refitting for RealMLP-TD and LGBM-TD, finding that refitting multiple models is often better on average. 
RealMLP-TDとLGBM-TDのためにバギングと再フィッティングを比較し、複数のモデルを再フィッティングすることが平均してしばしば優れていることを発見しました。

We demonstrate that GBDTs benefit from high early stopping patiences for classification, especially when using accuracy as the stopping metric. 
GBDTは分類において高い早期停止耐性から利益を得ることを示し、特に停止メトリックとして精度を使用する場合にそうです。

When considering AUROC as a stopping metric, we show that stopping on cross-entropy is preferable to accuracy (Appendix B.5). 
AUROCを停止メトリックとして考慮する場合、交差エントロピーで停止することが精度よりも好ましいことを示します（付録B.5）。

**Limitations** 
**制限**

While our benchmarks cover medium-to-large tabular datasets in standard settings, it is unclear to which extent the obtained defaults can generalize to very small datasets, distribution shifts, datasets with missing numerical values, and other metrics such as log-loss. 
私たちのベンチマークは標準設定の中で中規模から大規模の表形式データセットをカバーしていますが、得られたデフォルトが非常に小さなデータセット、分布のシフト、欠損数値を含むデータセット、およびログ損失のような他のメトリックにどの程度一般化できるかは不明です。

Additionally, runtimes and the resulting tradeoffs may change with different parallelization, hardware, or (time-aware) HPO algorithms. 
さらに、実行時間とその結果としてのトレードオフは、異なる並列化、ハードウェア、または（時間に敏感な）HPOアルゴリズムによって変わる可能性があります。

For computational reasons, we only use a single training-validation split per train-test split. 
計算上の理由から、各トレイン-テスト分割につき1つのトレーニング-検証分割のみを使用します。

This means that HPO can overfit the validation set more easily than in a cross-validation setup. 
これは、HPOがクロスバリデーションのセットアップよりも検証セットに過剰適合しやすいことを意味します。

While we extensively benchmark different NN models from the literature, we do not attempt to equalize non-architectural aspects, and our work should therefore not be seen as a comparison of architectures. 
私たちは文献から異なるNNモデルを広範囲にベンチマークしていますが、非アーキテクチャ的な側面を均等化しようとはしておらず、したがって私たちの作業はアーキテクチャの比較として見なされるべきではありません。

We compared to TabR-S-D as a recent promising method with good default parameters [17, 69]. 
私たちは、良好なデフォルトパラメータを持つ最近の有望な手法としてTabR-S-Dと比較しました[17, 69]。

However, due to a surge of recently published deep tabular models [e.g., 7, 8, 29, 33, 41, 57, 67], it is unclear what the current “best” deep tabular model is. 
しかし、最近発表された深層表形式モデルの急増[例：7, 8, 29, 33, 41, 57, 67]により、現在の「最良の」深層表形式モデルが何であるかは不明です。

In particular, ExcelFormer [7] also promises strong-performing default parameters. 
特に、ExcelFormer[7]も強力なデフォルトパラメータを約束しています。

For GBDTs, due to the cost of running the benchmarks, our limits on the depth and number of trees are on the lower side of the literature. 
GBDTに関しては、ベンチマークを実行するコストのため、木の深さと数に関する制限は文献の下限にあります。



#### 6 Conclusion 結論

In this paper, we studied the potential of improved default parameters for GBDTs and an improved MLP, evaluated on a large separate meta-test benchmark as well as the benchmark by Grinsztajn et al. 
本論文では、GBDTの改善されたデフォルトパラメータと改良されたMLPの可能性を研究し、大規模な別のメタテストベンチマークおよびGrinsztajnらによるベンチマークで評価しました。

[18], and investigated the time-accuracy tradeoffs of various algorithm selection and ensembling scenarios. 
また、さまざまなアルゴリズム選択およびアンサンブルシナリオの時間と精度のトレードオフを調査しました。

Our improved MLP mostly outperforms other NNs from the literature with moderate runtime and is competitive with GBDTs in terms of benchmark scores. 
私たちの改良されたMLPは、適度な実行時間で文献中の他のNNをほとんど上回り、ベンチマークスコアの点でGBDTと競争力があります。

Since many of the proposed improvements to NNs are orthogonal to the improvements in other papers, they offer exciting opportunities for combinations, as we demonstrated with our RealTabR variant. 
NNに対する提案された多くの改善が他の論文の改善と直交しているため、これらは組み合わせのための興味深い機会を提供します。これは、私たちのRealTabRバリアントで示した通りです。

While the “NNs vs GBDTs” debate remains interesting, our results demonstrate that with good default parameters, it is worth trying both algorithm families even with a moderate training time budget. 
「NN対GBDT」の議論は依然として興味深いですが、私たちの結果は、良いデフォルトパラメータを用いることで、適度なトレーニング時間の予算でも両方のアルゴリズムファミリーを試す価値があることを示しています。



#### Acknowledgments and Disclosure of Funding 謝辞および資金の開示

We thank Gaël Varoquaux, Frank Sehnke, Katharina Strecker, Ravid Shwartz-Ziv, Lennart Purucker, and Francis Bach for helpful discussions. 
私たちは、Gaël Varoquaux、Frank Sehnke、Katharina Strecker、Ravid Shwartz-Ziv、Lennart Purucker、Francis Bachに有益な議論をしていただいたことに感謝します。
We thank Katharina Strecker for help with code refactoring. 
また、コードのリファクタリングに関してKatharina Streckerに感謝します。

Funded by Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under Germany’s Excellence Strategy - EXC 2075 – 390740016. 
この研究は、ドイツの卓越性戦略 - EXC 2075 – 390740016の下で、ドイツ研究振興協会（DFG）によって資金提供されています。
The authors thank the International Max Planck Research School for Intelligent Systems (IMPRS-IS) for supporting David Holzmüller. 
著者は、David Holzmüllerを支援している国際マックス・プランク研究学校（IMPRS-IS）に感謝します。
LG acknowledges support in part by the French Agence Nationale de la Recherche under Grant ANR-20CHIA-0026 (LearnI). 
LGは、フランス国立研究機関（Agence Nationale de la Recherche）からの助成金ANR-20CHIA-0026（LearnI）による部分的な支援を認めます。
Part of this work was performed on the computational resource bwUniCluster funded by the Ministry of Science, Research and the Arts Baden-Württemberg and the Universities of the State of Baden-Württemberg, Germany, within the framework program bwHPC. 
この研究の一部は、バーデン＝ヴュルテンベルク州の科学・研究・芸術省およびバーデン＝ヴュルテンベルク州の大学によって資金提供された計算資源bwUniCluster上で実施されました。この枠組みプログラムはbwHPCです。
Part of this work was performed using HPC resources from GENCI–IDRIS (Grant 2023-AD011012804R1 and 2024-AD011012804R2). 
この研究の一部は、GENCI–IDRISからのHPCリソース（助成金2023-AD011012804R1および2024-AD011012804R2）を使用して実施されました。

**Contribution statement** 
**貢献声明**

DH and IS conceived the project. 
DHとISはこのプロジェクトを考案しました。
DH implemented and experimentally validated the newly proposed methods and wrote the initial paper draft. 
DHは新たに提案された方法を実装し、実験的に検証し、初期の論文草稿を書きました。
DH and LG contributed to benchmarking, plotting, and implementing baseline methods. 
DHとLGはベンチマーキング、プロット作成、ベースライン手法の実装に貢献しました。
LG and IS helped revise the draft. 
LGとISは草稿の改訂を手伝いました。
IS supervised the project and contributed dataset downloading code. 
ISはプロジェクトを監督し、データセットのダウンロードコードに貢献しました。



#### References 参考文献

[1] Sercan O. Arik and Tomas Pfister. TabNet: Attentive interpretable tabular learning. In AAAI _Conference on Artificial Intelligence, 2021._  
[1] Sercan O. Arik と Tomas Pfister. TabNet: 注意深く解釈可能な表形式学習. AAAI _人工知能に関する会議, 2021年._

[2] James Bergstra, Daniel Yamins, and David Cox. Making a science of model search: Hyperparameter optimization in hundreds of dimensions for vision architectures. In International _Conference on Machine Learning, 2013._  
[2] James Bergstra, Daniel Yamins, および David Cox. モデル探索の科学を作る: 視覚アーキテクチャのための数百次元でのハイパーパラメータ最適化. 国際 _機械学習会議, 2013年._

[3] Vadim Borisov, Tobias Leemann, Kathrin Seßler, Johannes Haug, Martin Pawelczyk, and Gjergji Kasneci. Deep neural networks and tabular data: A survey. IEEE Transactions on _Neural Networks and Learning Systems, 2022._  
[3] Vadim Borisov, Tobias Leemann, Kathrin Seßler, Johannes Haug, Martin Pawelczyk, および Gjergji Kasneci. 深層ニューラルネットワークと表形式データ: サーベイ. IEEE トランザクションズ _ニューラルネットワークと学習システム, 2022年._

[4] Pavel Brazdil, Christophe Giraud Carrier, Carlos Soares, and Ricardo Vilalta. Metalearning: _Applications to Data Mining. Springer Science & Business Media, 2008._  
[4] Pavel Brazdil, Christophe Giraud Carrier, Carlos Soares, および Ricardo Vilalta. メタラーニング: _データマイニングへの応用. Springer Science & Business Media, 2008年._

[5] Rich Caruana, Alexandru Niculescu-Mizil, Geoff Crew, and Alex Ksikes. Ensemble selection from libraries of models. In International Conference on Machine Learning, 2004.  
[5] Rich Caruana, Alexandru Niculescu-Mizil, Geoff Crew, および Alex Ksikes. モデルライブラリからのアンサンブル選択. 国際機械学習会議, 2004年.

[6] Rich Caruana, Art Munson, and Alexandru Niculescu-Mizil. Getting the most out of ensemble selection. In International Conference on Data Mining, pages 828–833. IEEE, 2006.  
[6] Rich Caruana, Art Munson, および Alexandru Niculescu-Mizil. アンサンブル選択から最大限の効果を得る. 国際データマイニング会議, ページ 828–833. IEEE, 2006年.

[7] Jintai Chen, Jiahuan Yan, Qiyuan Chen, Danny Z. Chen, Jian Wu, and Jimeng Sun. Can a Deep Learning Model be a Sure Bet for Tabular Prediction? In Conference on Knowledge Discovery _and Data Mining. ACM, August 2024._  
[7] Jintai Chen, Jiahuan Yan, Qiyuan Chen, Danny Z. Chen, Jian Wu, および Jimeng Sun. 深層学習モデルは表形式予測の確実な選択肢になり得るか? 知識発見 _およびデータマイニングに関する会議. ACM, 2024年8月._

[8] Kuan-Yu Chen, Ping-Han Chiang, Hsin-Rung Chou, Ting-Wei Chen, and Tien-Hao Chang. Trompt: Towards a better deep neural network for tabular data. In International Conference on _Machine Learning, 2023._  
[8] Kuan-Yu Chen, Ping-Han Chiang, Hsin-Rung Chou, Ting-Wei Chen, および Tien-Hao Chang. Trompt: 表形式データのためのより良い深層ニューラルネットワークに向けて. 国際機械学習会議, 2023年.

[9] Tianqi Chen and Carlos Guestrin. XGBoost: A scalable tree boosting system. In International _Conference on Knowledge Discovery and Data Mining, 2016._  
[9] Tianqi Chen と Carlos Guestrin. XGBoost: スケーラブルなツリーブースティングシステム. 国際 _知識発見とデータマイニング会議, 2016年._

[10] Nick Erickson, Jonas Mueller, Alexander Shirkov, Hang Zhang, Pedro Larroy, Mu Li, and Alexander Smola. AutoGluon-Tabular: Robust and accurate AutoML for structured data. In 7th _ICML Workshop on Automated Machine Learning, 2020._  
[10] Nick Erickson, Jonas Mueller, Alexander Shirkov, Hang Zhang, Pedro Larroy, Mu Li, および Alexander Smola. AutoGluon-Tabular: 構造化データのための堅牢で正確なAutoML. 第7回 _ICML 自動機械学習ワークショップ, 2020年._

[11] Matthias Feurer, Katharina Eggensperger, Stefan Falkner, Marius Lindauer, and Frank Hutter. Auto-sklearn 2.0: Hands-free automl via meta-learning. The Journal of Machine Learning _Research, 23(261), 2022._  
[11] Matthias Feurer, Katharina Eggensperger, Stefan Falkner, Marius Lindauer, および Frank Hutter. Auto-sklearn 2.0: メタラーニングによるハンズフリーのautoml. 機械学習 _研究ジャーナル, 23(261), 2022年._

[12] Sebastian Felix Fischer, Matthias Feurer, and Bernd Bischl. OpenML-CTR23–A curated tabular regression benchmarking suite. In AutoML Conference 2023 (Workshop), 2023.  
[12] Sebastian Felix Fischer, Matthias Feurer, および Bernd Bischl. OpenML-CTR23–キュレーションされた表形式回帰ベンチマークスイート. AutoML会議2023 (ワークショップ), 2023年.

[13] Pieter Gijsbers, Marcos LP Bueno, Stefan Coors, Erin LeDell, Sébastien Poirier, Janek Thomas, Bernd Bischl, and Joaquin Vanschoren. AMLB: an AutoML benchmark. Journal of Machine Learning Research, 25(101):1–65, 2024. URL https://www.jmlr.org/papers/v25/22-0493.html  
[13] Pieter Gijsbers, Marcos LP Bueno, Stefan Coors, Erin LeDell, Sébastien Poirier, Janek Thomas, Bernd Bischl, および Joaquin Vanschoren. AMLB: AutoMLベンチマーク. 機械学習研究ジャーナル, 25(101):1–65, 2024年. URL https://www.jmlr.org/papers/v25/22-0493.html

[14] Tilmann Gneiting and Adrian E Raftery. Strictly proper scoring rules, prediction, and estimation. _Journal of the American Statistical Association, 102(477):359–378, 2007._  
[14] Tilmann Gneiting と Adrian E Raftery. 厳密に適切なスコアリングルール、予測、および推定. _アメリカ統計協会誌, 102(477):359–378, 2007年._

[15] Yury Gorishniy, Ivan Rubachev, Valentin Khrulkov, and Artem Babenko. Revisiting deep learning models for tabular data. Neural Information Processing Systems, 2021.  
[15] Yury Gorishniy, Ivan Rubachev, Valentin Khrulkov, および Artem Babenko. 表形式データのための深層学習モデルの再考. ニューラル情報処理システム, 2021年.

[16] Yury Gorishniy, Ivan Rubachev, and Artem Babenko. On embeddings for numerical features in tabular deep learning. Neural Information Processing Systems, 2022.  
[16] Yury Gorishniy, Ivan Rubachev, および Artem Babenko. 表形式深層学習における数値特徴の埋め込みについて. ニューラル情報処理システム, 2022年.

[17] Yury Gorishniy, Ivan Rubachev, Nikolay Kartashev, Daniil Shlenskii, Akim Kotelnikov, and Artem Babenko. TabR: Tabular deep learning meets nearest neighbors. In International _Conference on Learning Representations, 2024._  
[17] Yury Gorishniy, Ivan Rubachev, Nikolay Kartashev, Daniil Shlenskii, Akim Kotelnikov, および Artem Babenko. TabR: 表形式深層学習と最近傍法の出会い. 国際 _表現学習会議, 2024年._

[18] Léo Grinsztajn, Edouard Oyallon, and Gaël Varoquaux. Why do tree-based models still outperform deep learning on typical tabular data? Neural Information Processing Systems, 2022.  
[18] Léo Grinsztajn, Edouard Oyallon, および Gaël Varoquaux. なぜツリーベースのモデルは依然として典型的な表形式データにおいて深層学習を上回るのか? ニューラル情報処理システム, 2022年.

[19] Cheng Guo and Felix Berkhahn. Entity embeddings of categorical variables. arXiv:1604.06737, 2016.  
[19] Cheng Guo と Felix Berkhahn. カテゴリ変数のエンティティ埋め込み. arXiv:1604.06737, 2016年.

[20] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. arXiv:2301.04104, 2023.  
[20] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, および Timothy Lillicrap. ワールドモデルを通じて多様なドメインをマスターする. arXiv:2301.04104, 2023年.

[21] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Delving deep into rectifiers: Surpassing human-level performance on imagenet classification. In IEEE International Conference _on Computer Vision, pages 1026–1034, 2015._  
[21] Kaiming He, Xiangyu Zhang, Shaoqing Ren, および Jian Sun. レクティファイアの深い探求: imagenet分類における人間レベルのパフォーマンスを超える. IEEE国際会議 _コンピュータビジョン, ページ 1026–1034, 2015年._

[22] Steffen Herbold. Autorank: A Python package for automated ranking of classifiers. Journal _of Open Source Software, 5(48):2173, 2020. doi: 10.21105/joss.02173. URL https://doi.org/10.21105/joss.02173_  
[22] Steffen Herbold. Autorank: 分類器の自動ランク付けのためのPythonパッケージ. オープンソースソフトウェアジャーナル _5(48):2173, 2020年. doi: 10.21105/joss.02173. URL https://doi.org/10.21105/joss.02173

[23] Noah Hollmann, Samuel Müller, Katharina Eggensperger, and Frank Hutter. TabPFN: A transformer that solves small tabular classification problems in a second. In International _Conference on Learning Representations, 2022._  
[23] Noah Hollmann, Samuel Müller, Katharina Eggensperger, および Frank Hutter. TabPFN: 小さな表形式分類問題を1秒で解決するトランスフォーマー. 国際 _表現学習会議, 2022年._

[24] David Holzmüller, Viktor Zaverkin, Johannes Kästner, and Ingo Steinwart. A framework and benchmark for deep batch active learning for regression. Journal of Machine Learning Research, 24(164), 2023.  
[24] David Holzmüller, Viktor Zaverkin, Johannes Kästner, および Ingo Steinwart. 回帰のための深層バッチアクティブラーニングのフレームワークとベンチマーク. 機械学習研究ジャーナル, 24(164), 2023年.

[25] Jeremy Howard and Sylvain Gugger. Fastai: A layered API for deep learning. Information, 11 (2):108, 2020.  
[25] Jeremy Howard と Sylvain Gugger. Fastai: 深層学習のための層状API. 情報, 11 (2):108, 2020年.

[26] Gao Huang, Zhuang Liu, Laurens Van Der Maaten, and Kilian Q. Weinberger. Densely connected convolutional networks. In Computer Vision and Pattern Recognition, pages 4700–4708, 2017.  
[26] Gao Huang, Zhuang Liu, Laurens Van Der Maaten, および Kilian Q. Weinberger. 密に接続された畳み込みネットワーク. コンピュータビジョンとパターン認識, ページ 4700–4708, 2017年.

[27] Xin Huang, Ashish Khetan, Milan Cvitkovic, and Zohar Karnin. TabTransformer: Tabular data modeling using contextual embeddings. arXiv:2012.06678, 2020.  
[27] Xin Huang, Ashish Khetan, Milan Cvitkovic, および Zohar Karnin. TabTransformer: コンテキスト埋め込みを使用した表形式データモデリング. arXiv:2012.06678, 2020年.

[28] Arthur Jacot, Franck Gabriel, and Clément Hongler. Neural tangent kernel: Convergence and generalization in neural networks. Neural Information Processing Systems, 2018.  
[28] Arthur Jacot, Franck Gabriel, および Clément Hongler. ニューラルタンジェントカーネル: ニューラルネットワークにおける収束と一般化. ニューラル情報処理システム, 2018年.

[29] Manu Joseph and Harsh Raj. GANDALF: Gated Adaptive Network for Deep Automated Learning of Features. arXiv:2207.08548, 2024.  
[29] Manu Joseph と Harsh Raj. GANDALF: 特徴の深層自動学習のためのゲート付き適応ネットワーク. arXiv:2207.08548, 2024年.

[30] Arlind Kadra, Marius Lindauer, Frank Hutter, and Josif Grabocka. Well-tuned simple nets excel on tabular datasets. In Neural Information Processing Systems, 2021.  
[30] Arlind Kadra, Marius Lindauer, Frank Hutter, および Josif Grabocka. 適切に調整されたシンプルなネットワークは表形式データセットで優れた性能を発揮する. ニューラル情報処理システム, 2021年.

[31] Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, and Tie-Yan Liu. LightGBM: A highly efficient gradient boosting decision tree. In Neural _Information Processing Systems, 2017._  
[31] Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, および Tie-Yan Liu. LightGBM: 高効率な勾配ブースティング決定木. ニューラル _情報処理システム, 2017年._

[32] Markelle Kelly, Rachel Longjohn, and Kolby Nottingham. The UCI Machine Learning Repository. URL https://archive.ics.uci.edu.  
[32] Markelle Kelly, Rachel Longjohn, および Kolby Nottingham. UCI機械学習リポジトリ. URL https://archive.ics.uci.edu

[33] Myung Jun Kim, Léo Grinsztajn, and Gaël Varoquaux. CARTE: pretraining and transfer for tabular learning. In International Conference on Machine Learning, 2024.  
[33] Myung Jun Kim, Léo Grinsztajn, および Gaël Varoquaux. CARTE: 表形式学習のための事前学習と転送. 国際機械学習会議, 2024年.

[34] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In International _Conference on Learning Representations, 2015._  
[34] Diederik P. Kingma と Jimmy Ba. Adam: 確率的最適化のための手法. 国際 _表現学習会議, 2015年._

[35] Günter Klambauer, Thomas Unterthiner, Andreas Mayr, and Sepp Hochreiter. Self-normalizing neural networks. In Neural Information Processing Systems, 2017.  
[35] Günter Klambauer, Thomas Unterthiner, Andreas Mayr, および Sepp Hochreiter. 自己正規化ニューラルネットワーク. ニューラル情報処理システム, 2017年.

[36] Ravin Kohli, Matthias Feurer, Katharina Eggensperger, Bernd Bischl, and Frank Hutter. Towards Quantifying the Effect of Datasets for Benchmarking: A Look at Tabular Machine Learning. In _ICLR 2024 Data-centric Machine Learning Research Workshop, 2024._  
[36] Ravin Kohli, Matthias Feurer, Katharina Eggensperger, Bernd Bischl, および Frank Hutter. ベンチマークのためのデータセットの効果を定量化することに向けて: 表形式機械学習の考察. _ICLR 2024 データ中心の機械学習研究ワークショップ, 2024年._

[37] Jannik Kossen, Neil Band, Clare Lyle, Aidan N. Gomez, Thomas Rainforth, and Yarin Gal. Self-attention between datapoints: Going beyond individual input-output pairs in deep learning. In Neural Information Processing Systems, 2021.  
[37] Jannik Kossen, Neil Band, Clare Lyle, Aidan N. Gomez, Thomas Rainforth, および Yarin Gal. データポイント間の自己注意: 深層学習における個々の入力-出力ペアを超える. ニューラル情報処理システム, 2021年.

[38] Marius Lindauer, Katharina Eggensperger, Matthias Feurer, André Biedenkapp, Difan Deng, Carolin Benjamins, Tim Ruhkopf, René Sass, and Frank Hutter. SMAC3: A versatile Bayesian optimization package for hyperparameter optimization. Journal of Machine Learning Research, 23(54), 2022.  
[38] Marius Lindauer, Katharina Eggensperger, Matthias Feurer, André Biedenkapp, Difan Deng, Carolin Benjamins, Tim Ruhkopf, René Sass, および Frank Hutter. SMAC3: ハイパーパラメータ最適化のための多目的ベイズ最適化パッケージ. 機械学習研究ジャーナル, 23(54), 2022年.

[39] Ilya Loshchilov and Frank Hutter. SGDR: Stochastic gradient descent with warm restarts. In _International Conference on Learning Representations, 2017._  
[39] Ilya Loshchilov と Frank Hutter. SGDR: ウォームリスタートを伴う確率的勾配降下法. _国際表現学習会議, 2017年._

[40] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In International _Conference on Learning Representations, 2018._  
[40] Ilya Loshchilov と Frank Hutter. 分離型重み減衰正則化. 国際 _表現学習会議, 2018年._

[41] Sascha Marton, Stefan Lüdtke, Christian Bartelt, and Heiner Stuckenschmidt. GRANDE: Gradient-based decision tree ensembles for tabular data. In International Conference on _Learning Representations, 2024._  
[41] Sascha Marton, Stefan Lüdtke, Christian Bartelt, および Heiner Stuckenschmidt. GRANDE: 表形式データのための勾配ベースの決定木アンサンブル. 国際 _表現学習会議, 2024年._

[42] Calvin McCarter. The kernel density integral transformation. Transactions on Machine Learning _Research, 2023._  
[42] Calvin McCarter. カーネル密度積分変換. 機械学習 _研究トランザクション, 2023年._

[43] Duncan McElfresh, Sujay Khandagale, Jonathan Valverde, Vishak Prasad C, Ganesh Ramakrishnan, Micah Goldblum, and Colin White. When do neural nets outperform boosted trees on tabular data? In Neural Information Processing Systems, 2023.  
[43] Duncan McElfresh, Sujay Khandagale, Jonathan Valverde, Vishak Prasad C, Ganesh Ramakrishnan, Micah Goldblum, および Colin White. ニューラルネットは表形式データにおいてブーストツリーを上回るのはいつか? ニューラル情報処理システム, 2023年.

[44] Dmytro Mishkin and Jiri Matas. All you need is a good init. In International Conference on _Learning Representations, 2016._  
[44] Dmytro Mishkin と Jiri Matas. 必要なのは良い初期化だけ. 国際 _表現学習会議, 2016年._

[45] Diganta Misra. Mish: A self regularized non-monotonic activation function. In British Machine _Vision Conference, 2020._  
[45] Diganta Misra. Mish: 自己正則化された非単調活性化関数. 英国機械 _ビジョン会議, 2020年._

[46] Philipp Moritz, Robert Nishihara, Stephanie Wang, Alexey Tumanov, Richard Liaw, Eric Liang, Melih Elibol, Zongheng Yang, William Paul, and Michael I. Jordan. Ray: A distributed framework for emerging AI applications. In USENIX Symposium on Operating Systems Design _and Implementation, 2018._  
[46] Philipp Moritz, Robert Nishihara, Stephanie Wang, Alexey Tumanov, Richard Liaw, Eric Liang, Melih Elibol, Zongheng Yang, William Paul, および Michael I. Jordan. Ray: 新興AIアプリケーションのための分散フレームワーク. USENIXオペレーティングシステム設計 _および実装シンポジウム, 2018年._

[47] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, and Luca Antiga. PyTorch: An imperative style, high-performance deep learning library. Neural Information Processing Systems, 32, 2019.  
[47] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, および Luca Antiga. PyTorch: 命令型スタイルの高性能深層学習ライブラリ. ニューラル情報処理システム, 32, 2019年.

[48] Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, and Vincent Dubourg. Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12(85), 2011.  
[48] Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron Weiss, および Vincent Dubourg. Scikit-learn: Pythonにおける機械学習. 機械学習研究ジャーナル, 12(85), 2011年.

[49] Florian Pfisterer, Jan N. Van Rijn, Philipp Probst, Andreas C. Müller, and Bernd Bischl. Learning multiple defaults for machine learning algorithms. In Genetic and Evolutionary Computation _Conference, July 2021._  
[49] Florian Pfisterer, Jan N. Van Rijn, Philipp Probst, Andreas C. Müller, および Bernd Bischl. 機械学習アルゴリズムのための複数のデフォルトを学習する. 遺伝的および進化的計算 _会議, 2021年7月._

[50] Philipp Probst, Anne-Laure Boulesteix, and Bernd Bischl. Tunability: Importance of hyperparameters of machine learning algorithms. Journal of Machine Learning Research, 20(53), 2019.  
[50] Philipp Probst, Anne-Laure Boulesteix, および Bernd Bischl. 調整可能性: 機械学習アルゴリズムのハイパーパラメータの重要性. 機械学習研究ジャーナル, 20(53), 2019年.

[51] Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush, and Andrey Gulin. CatBoost: Unbiased boosting with categorical features. In Neural Information _Processing Systems, 2018._  
[51] Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush, および Andrey Gulin. CatBoost: カテゴリ特徴を用いたバイアスのないブースティング. ニューラル _情報処理システム, 2018年._

[52] Ali Rahimi and Benjamin Recht. Random features for large-scale kernel machines. In Neural _Information Processing Systems, 2007._  
[52] Ali Rahimi と Benjamin Recht. 大規模カーネルマシンのためのランダム特徴. ニューラル _情報処理システム, 2007年._

[53] Hubert Ramsauer, Bernhard Schäfl, Johannes Lehner, Philipp Seidl, Michael Widrich, Lukas Gruber, Markus Holzleitner, Thomas Adler, David Kreil, and Michael K. Kopp. Hopfield networks is all you need. In International Conference on Learning Representations, 2020.  
[53] Hubert Ramsauer, Bernhard Schäfl, Johannes Lehner, Philipp Seidl, Michael Widrich, Lukas Gruber, Markus Holzleitner, Thomas Adler, David Kreil, および Michael K. Kopp. ホップフィールドネットワークが必要なすべてです. 国際表現学習会議, 2020年.

[54] Ivan Rubachev, Nikolay Kartashev, Yury Gorishniy, and Artem Babenko. TabReD: Analyzing Pitfalls and Filling the Gaps in Tabular Deep Learning Benchmarks. arXiv:2406.19380, 2024.  
[54] Ivan Rubachev, Nikolay Kartashev, Yury Gorishniy, および Artem Babenko. TabReD: 表形式深層学習ベンチマークの落とし穴を分析し、ギャップを埋める. arXiv:2406.19380, 2024年.

[55] David Salinas and Nick Erickson. TabRepo: A large scale repository of tabular model evaluations and its AutoML applications. In AutoML Conference, 2024.  
[55] David Salinas と Nick Erickson. TabRepo: 表形式モデル評価の大規模リポジトリとそのAutoMLアプリケーション. AutoML会議, 2024年.

[56] Bernhard Schäfl, Lukas Gruber, Angela Bitto-Nemling, and Sepp Hochreiter. Modern Hopfield networks as memory for iterative learning on tabular data. In NeurIPS Workshop on Associative _Memory & Hopfield Networks in 2023, 2023._  
[56] Bernhard Schäfl, Lukas Gruber, Angela Bitto-Nemling, および Sepp Hochreiter. 現代のホップフィールドネットワークを表形式データの反復学習のためのメモリとして. NeurIPS ワークショップ _連想記憶とホップフィールドネットワーク, 2023年._

[57] Junhong Shen, Liam Li, Lucio M. Dery, Corey Staten, Mikhail Khodak, Graham Neubig, and Ameet Talwalkar. Cross-modal fine-tuning: Align then refine. In International Conference on _Machine Learning, 2023._  
[57] Junhong Shen, Liam Li, Lucio M. Dery, Corey Staten, Mikhail Khodak, Graham Neubig, および Ameet Talwalkar. クロスモーダルファインチューニング: 整列してから洗練する. 国際機械学習会議, 2023年.

[58] Ravid Shwartz-Ziv and Amitai Armon. Tabular data: Deep learning is not all you need. _Information Fusion, 81:84–90, 2022._  
[58] Ravid Shwartz-Ziv と Amitai Armon. 表形式データ: 深層学習だけでは不十分です. _情報融合, 81:84–90, 2022年._

[59] Leslie N. Smith. Cyclical learning rates for training neural networks. In Winter Conference on _Applications of Computer Vision, 2017._  
[59] Leslie N. Smith. ニューラルネットワークのトレーニングのための周期的学習率. _コンピュータビジョンの応用に関する冬季会議, 2017年._

[60] Gowthami Somepalli, Micah Goldblum, Avi Schwarzschild, C. Bayan Bruss, and Tom Goldstein. SAINT: Improved neural networks for tabular data via row attention and contrastive pre-training. In NeurIPS 2022 Table Representation Learning Workshop, 2022.  
[60] Gowthami Somepalli, Micah Goldblum, Avi Schwarzschild, C. Bayan Bruss, および Tom Goldstein. SAINT: 行注意と対照的事前学習を通じて表形式データのための改善されたニューラルネットワーク. NeurIPS 2022 テーブル表現学習ワークショップ, 2022年.

[61] Ingo Steinwart. A sober look at neural network initializations. arXiv:1903.11482, 2019.  
[61] Ingo Steinwart. ニューラルネットワークの初期化に対する冷静な見方. arXiv:1903.11482, 2019年.

[62] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. In Computer Vision and Pattern Recognition, 2016.  
[62] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jon Shlens, および Zbigniew Wojna. コンピュータビジョンのためのインセプションアーキテクチャの再考. コンピュータビジョンとパターン認識, 2016年.

[63] Jan N. van Rijn, Florian Pfisterer, Janek Thomas, Andreas Muller, Bernd Bischl, and Joaquin Vanschoren. Meta learning for defaults: Symbolic defaults. In NeurIPS 2018 Workshop on _Meta-Learning, 2018._  
[63] Jan N. van Rijn, Florian Pfisterer, Janek Thomas, Andreas Muller, Bernd Bischl, および Joaquin Vanschoren. デフォルトのためのメタラーニング: シンボリックデフォルト. NeurIPS 2018 ワークショップ _メタラーニング, 2018年._

[64] Joaquin Vanschoren. Meta-learning: A survey. arXiv:1810.03548, 2018.  
[64] Joaquin Vanschoren. メタラーニング: サーベイ. arXiv:1810.03548, 2018年.

[65] Joaquin Vanschoren, Jan N. van Rijn, Bernd Bischl, and Luis Torgo. OpenML: Networked science in machine learning. ACM SIGKDD Explorations Newsletter, 15(2):49–60, 2014. Publisher: ACM New York, NY, USA.  
[65] Joaquin Vanschoren, Jan N. van Rijn, Bernd Bischl, および Luis Torgo. OpenML: 機械学習におけるネットワーク化された科学. ACM SIGKDD 探索ニュースレター, 15(2):49–60, 2014年. 出版社: ACM ニューヨーク, NY, USA.

[66] Martin Wistuba, Nicolas Schilling, and Lars Schmidt-Thieme. Learning hyperparameter optimization initializations. In International Conference on Data Science and Advanced _Analytics, pages 1–10, 2015._  
[66] Martin Wistuba, Nicolas Schilling, および Lars Schmidt-Thieme. ハイパーパラメータ最適化初期化の学習. 国際データサイエンスおよび高度な _分析会議, ページ 1–10, 2015年._

[67] Chenwei Xu, Yu-Chao Huang, Jerry Yao-Chieh Hu, Weijian Li, Ammar Gilani, Hsi-Sheng Goan, and Han Liu. BiSHop: Bi-directional cellular learning for tabular data with generalized sparse modern Hopfield model. In International Conference on Machine Learning, 2024.  
[67] Chenwei Xu, Yu-Chao Huang, Jerry Yao-Chieh Hu, Weijian Li, Ammar Gilani, Hsi-Sheng Goan, および Han Liu. BiSHop: 一般化されたスパース現代ホップフィールドモデルを用いた表形式データのための双方向セルラーニング. 国際機械学習会議, 2024年.

[68] Ge Yang, Edward Hu, Igor Babuschkin, Szymon Sidor, Xiaodong Liu, David Farhi, Nick Ryder, Jakub Pachocki, Weizhu Chen, and Jianfeng Gao. Tuning large neural networks via zero-shot hyperparameter transfer. In Neural Information Processing Systems, 2021.  
[68] Ge Yang, Edward Hu, Igor Babuschkin, Szymon Sidor, Xiaodong Liu, David Farhi, Nick Ryder, Jakub Pachocki, Weizhu Chen, および Jianfeng Gao. ゼロショットハイパーパラメータ転送による大規模ニューラルネットワークの調整. ニューラル情報処理システム, 2021年.

[69] Han-Jia Ye, Si-Yang Liu, Hao-Run Cai, Qi-Le Zhou, and De-Chuan Zhan. A closer look at deep learning on tabular data. arXiv:2407.00956, 2024.  
[69] Han-Jia Ye, Si-Yang Liu, Hao-Run Cai, Qi-Le Zhou, および De-Chuan Zhan. 表形式データにおける深層学習の詳細な考察. arXiv:2407.00956, 2024年.



# Appendices 付録  
#### Appendix Contents. 付録の内容
**A Further Details on Neural Networks** **17**  
**A.1 RealMLP-TD Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17**  
**A.1 RealMLP-TDの詳細 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17**  
**A.2 RealMLP-TD-S Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17**  
**A.2 RealMLP-TD-Sの詳細 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17**  
**A.3 RealTabR-D Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17**  
**A.3 RealTabR-Dの詳細 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17**  
**A.4 Details on Cumulative Ablation . . . . . . . . . . . . . . . . . . . . . . . . . . . 19**  
**A.4 蓄積アブレーションの詳細 . . . . . . . . . . . . . . . . . . . . . . . . . . . 19**  
**A.5 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20**  
**A.5 議論 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20**  
**B** **More Experiments** **20**  
**B** **さらなる実験** **20**  
**B.1 MLP Ablations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20**  
**B.1 MLPアブレーション . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20**  
**B.2 MLP Preprocessing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21**  
**B.2 MLP前処理 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21**  
**B.3 Bagging, Refitting, and Ensembling . . . . . . . . . . . . . . . . . . . . . . . . . 22**  
**B.3 バギング、再フィッティング、およびアンサンブル . . . . . . . . . . . . . . . . . . . . 22**  
**B.4 Early stopping for GBDTs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23**  
**B.4 GBDTのための早期停止 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23**  
**B.5 Results for AUROC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24**  
**B.5 AUROCの結果 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24**  
**B.6 Results Without Missing-Value Datasets . . . . . . . . . . . . . . . . . . . . . . . 25**  
**B.6 欠損値データセットなしの結果 . . . . . . . . . . . . . . . . . . . . . . . . . . 25**  
**B.7 Comparing Preprocessing Methods for NNs . . . . . . . . . . . . . . . . . . . . . 25**  
**B.7 ニューラルネットワークの前処理方法の比較 . . . . . . . . . . . . . . . . . . . 25**  
**B.8 Results for Varying Architecture . . . . . . . . . . . . . . . . . . . . . . . . . . . 26**  
**B.8 構造の変化に関する結果 . . . . . . . . . . . . . . . . . . . . . . . . . . . 26**  
**B.9 Comparing HPO Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.9 HPO手法の比較 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.10 More Time-Error Plots . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.10 さらなる時間誤差プロット . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.11 Critical Difference Diagrams . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.11 重要差異図 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.12 Win-rate Plots . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**B.12 勝率プロット . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28**  
**C Benchmark Details** **40**  
**C ベンチマークの詳細** **40**  
**C.1 Default Configurations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40**  
**C.1 デフォルト設定 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40**  
**C.2 Hyperparameter Optimization . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40**  
**C.2 ハイパーパラメータ最適化 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40**  
**C.3 Dataset Selection and Preprocessing . . . . . . . . . . . . . . . . . . . . . . . . . 48**  
**C.3 データセットの選択と前処理 . . . . . . . . . . . . . . . . . . . . . . . . . 48**  
**C.4 Comparison with Standard Grinsztajn et al. [18] Benchmark . . . . . . . . . . . . 54**  
**C.4 標準Grinsztajn et al. [18]ベンチマークとの比較 . . . . . . . . . . . . 54**  
**C.5 Closer-to-original Version of the Grinsztajn et al. [18] Benchmark . . . . . . . . . 54**  
**C.5 Grinsztajn et al. [18]ベンチマークのオリジナルに近いバージョン . . . . . . . . . 54**  
**C.6 Confidence Intervals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.6 信頼区間 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.7 Time Measurements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.7 時間測定 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.8 Compute Resources . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.8 計算リソース . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.9 Used Libraries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**C.9 使用したライブラリ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57**  
**D Results for Individual Datasets** **58**  
**D 個別データセットの結果** **58**  


```md
#### A Further Details on Neural Networks ニューラルネットワークに関する詳細

The detailed hyperparameter settings for RealMLP-TD and RealMLP-TD-S are listed in Table A.1.  
RealMLP-TDおよびRealMLP-TD-Sの詳細なハイパーパラメータ設定は、表A.1に示されています。

**A.1** **RealMLP-TD Details**  
**A.1** **RealMLP-TDの詳細**

**Architecture** To make the binary and multi-class cases more similar, we use two output neurons in the binary case, using the same loss function as in the multi-class case.  
**アーキテクチャ** バイナリケースとマルチクラスケースをより類似させるために、バイナリケースでは2つの出力ニューロンを使用し、マルチクラスケースと同じ損失関数を使用します。

**Initialization** We initialize categorical embedding parameters from N (0, 1). We initialize the components of $w_{emb}[i]$ from $N(0, 0.12)$ and of $b_{emb}[i]$ from $U[-\pi, \pi]$. The other numerical embedding parameters are initialized according to PyTorch’s default initialization, that is, from the uniform $\sqrt{1/16}$ distribution. For weights and biases of the linear layers, we use a data-dependent $U_{-}$ initialization. The initialization is performed on the fly during a first forward pass of the network on the training set (which can be subsampled adaptively not to use more than 1 GB of RAM). We realize this by providing fit_transform() methods similar to a pipeline in scikit-learn. For the weight matrices, we use a custom two-step procedure: First, we initialize all entries from (0, 1). Then, we $N$ rescale each row of the weight matrix such that the outputs $W^{(l)}x^{(j)}$ have variance 1 over the dataset (i.e. when considering the sample index $j = 1, \ldots, n$ as a uniformly distributed random variable). This is somewhat similar to the LSUV initialization method. For the biases, we use the data-dependent he+5 initialization method (called hull+5 in [61]).  
**初期化** カテゴリ埋め込みパラメータは$N(0, 1)$から初期化します。$w_{emb}[i]$の成分は$N(0, 0.12)$から、$b_{emb}[i]$の成分は$U[-\pi, \pi]$から初期化します。他の数値埋め込みパラメータは、PyTorchのデフォルト初期化に従って初期化され、すなわち一様分布$\sqrt{1/16}$から初期化されます。線形層の重みとバイアスには、データ依存の$U_{-}$初期化を使用します。初期化は、トレーニングセット上でのネットワークの最初のフォワードパス中にオンザフライで実行されます（これにより、1GBのRAMを超えないように適応的にサブサンプリングできます）。これは、scikit-learnのパイプラインに似たfit_transform()メソッドを提供することで実現します。重み行列については、カスタムの二段階手順を使用します。まず、すべてのエントリを(0, 1)から初期化します。次に、重み行列の各行を$N$で再スケーリングし、出力$W^{(l)}x^{(j)}$がデータセット全体で分散1を持つようにします（すなわち、サンプルインデックス$j = 1, \ldots, n$を一様分布のランダム変数として考慮します）。これはLSUV初期化法にやや似ています。バイアスについては、データ依存のhe+5初期化法を使用します（[61]でhull+5と呼ばれています）。

**Training** We implement weight decay as in PyTorch using $\theta \leftarrow \theta - lr \cdot wd \cdot \theta$, which includes the learning rate unlike the original version.  
**トレーニング** PyTorchと同様に、重み減衰を$\theta \leftarrow \theta - lr \cdot wd \cdot \theta$として実装します。これは、元のバージョンとは異なり、学習率を含みます。

**A.2** **RealMLP-TD-S Details**  
**A.2** **RealMLP-TD-Sの詳細**

For RealMLP-TD-S, we make the following changes compared to RealMLP-TD:  
RealMLP-TD-Sでは、RealMLP-TDに対して以下の変更を行います：

- We apply one-hot encoding to all categorical variables and do not apply categorical embeddings.  
- すべてのカテゴリ変数に対してワンホットエンコーディングを適用し、カテゴリ埋め込みは適用しません。

- We do not apply numerical embeddings.  
- 数値埋め込みは適用しません。

- We use the standard non-parametric versions of the SELU and Mish activation functions.  
- SELUおよびMish活性化関数の標準的な非パラメトリックバージョンを使用します。

- We do not use dropout and weight decay.  
- ドロップアウトおよび重み減衰は使用しません。

- We use simpler weight and bias initializations: We initialize weights and biases from (0, 1), except in the last layer, where we initialize them to zero.  
- より単純な重みとバイアスの初期化を使用します：重みとバイアスは(0, 1)から初期化しますが、最後の層ではゼロに初期化します。

- We do not clip the outputs, even in the regression case.  
- 回帰の場合でも出力をクリップしません。

- We apply a different base learning rate in the regression case.  
- 回帰の場合には異なる基本学習率を適用します。

**A.3** **RealTabR-D Details**  
**A.3** **RealTabR-Dの詳細**

To obtain RealTabR-D, we modify TabR-S-D in the following ways:  
RealTabR-Dを得るために、TabR-S-Dを以下の方法で修正します：

- We replace the standard numerical preprocessing (a modified quantile transform) with our robust scaling and smooth clipping.  
- 標準的な数値前処理（修正された分位数変換）を、私たちのロバストスケーリングとスムーズクリッピングに置き換えます。

- We set Adam’s $\beta_2$ to 0.95 instead of 0.999.  
- Adamの$\beta_2$を0.999の代わりに0.95に設定します。

- We use our scaling layer, but modify it to obtain a higher effective learning rate. We do this by modifying the forward pass to  
- スケーリング層を使用しますが、より高い効果的学習率を得るために修正します。これは、フォワードパスを次のように修正することで行います：

$$
x_{i,out} = \gamma \cdot s_i \cdot x_{i,in},
$$

while initializing $s_i$ to $1/\gamma$. This will multiply the gradients of $s_i$ by $\gamma$, which will be ignored by Adam’s normalization (when neglecting Adam’s $\epsilon$ parameter). It will also multiply the optimizer updates by $\gamma$, leading to approximately the same effect as multiplying the learning rate by $\gamma. However, a difference is that multiplying the learning rate by $\gamma$ will also lead to stronger weight decay updates in PyTorch’s AdamW implementation, while the introduction of $\gamma$ does not increase the relative magnitude of weight decay updates. We chose the version with $\gamma$ for simplicity of implementation. While RealMLP-TD uses a learning rate factor of 6 for the scaling layer, it uses a higher base learning rate due to the use of the neural tangent parametrization. For all layers except the first one, which have width 256, the neural tangent  
- $s_i$を$1/\gamma$に初期化します。これにより、$s_i$の勾配が$\gamma$で乗算され、Adamの正規化によって無視されます（Adamの$\epsilon$パラメータを無視する場合）。また、オプティマイザの更新も$\gamma$で乗算され、学習率を$\gamma$で乗算するのとほぼ同じ効果をもたらします。ただし、学習率を$\gamma$で乗算すると、PyTorchのAdamW実装において重み減衰の更新が強化されるのに対し、$\gamma$の導入は重み減衰の更新の相対的な大きさを増加させません。実装の簡素化のために、$\gamma$を使用したバージョンを選択しました。RealMLP-TDはスケーリング層に対して6の学習率係数を使用しますが、ニューラル接線パラメータ化の使用により、より高い基本学習率を使用します。幅256の最初の層を除くすべての層について、ニューラル接線

-----
Table A.1: Overview of hyperparameters for RealMLP-TD and RealMLP-TD-S.  
表A.1: RealMLP-TDおよびRealMLP-TD-Sのハイパーパラメータの概要。

RealMLP-TD RealMLP-TD-S Hyperparameter classification regression classification regression  
RealMLP-TD RealMLP-TD-S ハイパーパラメータ 分類 回帰 分類 回帰  
Num. embedding type PBLD PBLD None None  
Num. embedding periodic init std. 0.1 0.1 — —  
Num. embedding hidden dimension 16 16 — —  
Num. embedding dimension 4 4 — —  
Max one-hot size (without missing) 8 8 $\infty$ $\infty$  
Num. preprocessing robust scale + smooth clip Categorical embedding dimension 8 8 — —  
Categorical embedding initialization $N(0, 1)$ $N(0, 1)$ — —  
Use scaling layer yes Scaling layer initialization 1.0 (constant)  
Number of linear layers 4 Hidden layer sizes [256, 256, 256]  
Activation function SELU Mish SELU Mish  
Use parametric activation function yes yes no no  
Parametric activation function initialization 1.0 1.0 — —  
Linear layer parametrization NTP Last linear layer weight initialization data-driven data-driven zero zero  
Other linear layer weight initialization data-driven data-driven std normal std normal  
Last linear layer bias initialization he+5 he+5 zero zero  
Other linear layer bias initialization he+5 he+5 std normal std normal  
Optimizer AdamW Batch size 256 Number of epochs 256  
Adam $\beta_1$ 0.9 Adam $\beta_2$ 0.95 Adam $\epsilon$ 1e-8  
Learning rate (base value) 0.04 0.2 0.04 0.07  
Learning rate schedule coslog4 Learning rate (num. emb. factor) 0.1 0.1 — —  
Learning rate (scaling layer factor) 6 Learning rate (bias factor) 0.1  
Learning rate (param. act. factor) 0.1 0.1 — —  
Dropout probability (base value) 0.15 0.15 0.0 0.0  
Dropout schedule flat_cos flat_cos — —  
Weight decay (base value) 0.02 0.02 0.0 0.0  
Weight decay schedule flat_cos flat_cos — —  
Weight decay (bias factor) 0.0 0.0 — —  
Loss function cross-entropy MSE cross-entropy MSE  
Label smoothing $\epsilon$ 0.1 — 0.1 —  
Standardize targets during training — yes — yes  
Output min-max clipping — yes — no  
Best epoch selection metric class. error MSE class. error MSE  
Best epoch selection method last best validation error  
```
