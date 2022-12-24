## link 

https:
httpsを使用しています。

https:
httpsを使用しています。

## title タイトル

Revisiting the Performance of iALS on Item Recommendation Benchmarks
項目推薦ベンチマークにおけるiALSの性能の再検討

## abstruct abstruct

Matrix factorization learned by implicit alternating least squares (iALS) is a popular baseline in recommender system research publications. iALS is known to be one of the most computationally efficient and scalable collaborative filtering methods.
iALSは最も計算効率が良くスケーラブルな協調フィルタリング手法の1つとして知られている．
However, recent studies suggest that its prediction quality is not competitive with the current state of the art, in particular autoencoders and other item-based collaborative filtering methods.
しかし、最近の研究では、iALSの予測品質は、特にオートエンコーダや他のアイテムベースの協調フィルタリング手法など、現在の最先端技術と競合しないことが示唆されている。
In this work, we revisit four well-studied benchmarks where iALS was reported to perform poorly and show that with proper tuning, iALS is highly competitive and outperforms any method on at least half of the comparisons.
本研究では、iALSの性能が低いと報告されている4つのよく研究されたベンチマークを再検討し、適切なチューニングによりiALSが高い競争力を持ち、少なくとも比較対象の半分でどの手法よりも優れていることを示す。
We hope that these high quality results together with iALS's known scalability spark new interest in applying and further improving this decade old technique.
我々は、iALSの既知のスケーラビリティとともに、これらの高品質な結果が、この10年来の手法の適用とさらなる改善に対する新たな関心を呼び起こすことを期待している。

# introduction 導入

Research in recommender system algorithms is largely driven by results from empirical studies.
レコメンダーシステムアルゴリズムの研究は、主に経験的研究の結果によって推進されている。
Newly proposed recommender algorithms are typically compared to established baseline algorithms on a set of recommender tasks.
新しく提案されたレコメンダーアルゴリズムは、通常、一連のレコメンダータスクにおいて確立されたベースラインアルゴリズムと比較される。
Findings from such studies influence both the direction of future research and the algorithms for practitioners to adopt, hence it is very important to make sure that the experimental results are reliable.
このような研究から得られた知見は、将来の研究の方向性と実務家が採用するアルゴリズムの両方に影響を与えるため、実験結果の信頼性を確認することが非常に重要である。
Recent work has highlighted issues in recommender system evaluations (e.g., [6, 24]) where newly proposed algorithms often were unable to outperform older baselines hence leading to unreliable claims about the quality of different algorithms.
最近の研究では、レコメンダーシステムの評価における問題点（例えば[6, 24]）が強調されており、新しく提案されたアルゴリズムはしばしば古いベースラインを上回ることができないため、異なるアルゴリズムの品質について信頼できない主張をすることになった。

In this work, we carry out a study of the performance of iALS, a matrix factorization algorithm with quadratic loss, on top-n item recommendation benchmarks.
本研究では，二次損失を用いた行列分解アルゴリズムであるiALSの性能に関する研究を，トップn項目の推薦ベンチマークに対して実施した．
We demonstrate that iALS is able to achieve much better performance than previously reported and is competitive with recently developed and often more complex models.
その結果、iALSは従来の報告よりもはるかに優れた性能を達成することができ、最近開発されたより複雑なモデルに対しても競争力を持つことが実証された。
In addition to reinforcing the importance of tuning baseline models, we provide detailed guidance on tuning iALS, which we hope to help unlock the power of this algorithm in practice.
また、ベースラインモデルのチューニングの重要性を強調するとともに、iALSのチューニングに関する詳細なガイダンスを提供し、このアルゴリズムが実際に力を発揮することを期待する。

iALS 1 [12] is an algorithm for learning a matrix factorization model for the purpose of top-n item recommendation from implicit feedback.
iALS 1 [12]は、暗黙のフィードバックから上位n項目の推薦を行うための行列分解モデルを学習するアルゴリズムである。
An example for such a recommendation task would be to find the best movies (products, songs,...) for a user given the past movies watched (products bought, songs listened,...) by this user. iALS has been proposed over a decade ago and serves as one of the most commonly used baselines in the recommender system literature.
iALSは10年以上前に提案され、推薦システムの文献で最もよく使われるベースラインの一つである。
While iALS is regarded as a simple and computationally efficient algorithm, it is typically no longer considered a top performing method with respect to prediction quality (e.g., [9, 17]).
iALSはシンプルで計算効率の良いアルゴリズムとみなされているが、予測品質に関してはもはやトップパフォーマンスとみなされていない（例えば、[9, 17]）。
In this work, we revisit four well-studied item recommendation benchmarks where poor prediction quality was reported for iALS.
本研究では、iALSの予測品質が低いと報告された、よく研究された4つの項目推薦ベンチマークを再検討する。
The benchmarks that we pick have been proposed and studied by multiple research groups [1, 6, 9, 13, 17] and other researchers have used them for evaluating newly proposed algorithms [14, 18, 25, 26].
これらのベンチマークは複数の研究グループによって提案・研究されており[1, 6, 9, 13, 17]、他の研究者も新しく提案されたアルゴリズムの評価に用いている[14, 18, 25, 26]。
The poor iALS results have been established and reproduced by multiple groups [1, 6, 9, 13, 17] including a paper focused on reproducibility [1].
iALSの結果の悪さは、再現性に焦点を当てた論文[1]を含め、複数のグループによって立証され、再現されてきた。
However, contrary to these results, we show that iALS can in fact generate high quality results on exactly the same benchmarks using exactly the same evaluation method.
しかし、これらの結果とは逆に、我々はiALSが全く同じベンチマークで、全く同じ評価方法を用いて、実際に高品質な結果を生成できることを示す。
Our iALS numbers outperform not only the previously reported numbers for iALS but outperform the reported quality of any other recommender algorithm on at least half of the evaluation metrics.
私たちのiALSの数値は、以前に報告されたiALSの数値だけでなく、少なくとも半分の評価指標において、他のどの推薦アルゴリズムの報告された品質よりも優れている。
We attribute this contradiction to the difficulty of evaluating baselines [24], which can be challenging for many reasons, including improper hyper-parameter tuning.
この矛盾は、不適切なハイパーパラメータのチューニングを含む多くの理由で困難なベースライン評価[24]の難しさに起因すると考えている。
In this work, we give a detailed description of the role of the iALS hyperparameters, and how to tune them.
この研究では、iALSのハイパーパラメータの役割と、その調整方法について詳細に説明する。
We hope that these insights help both researchers and practitioners to obtain better results for this important algorithm in the future.
これらの知見が、今後この重要なアルゴリズムにおいて、研究者と実務家の両方がより良い結果を得るために役立つことを期待している。
As our experiments show, properly tuning an existing algorithm can have as much quality gain as inventing novel modeling techniques.
我々の実験が示すように、既存のアルゴリズムを適切に調整することは、新しいモデリング技術を発明することと同じくらいに品質を向上させることができる。

Our empirical results also call for rethinking the effectiveness of the quadratic loss for ranking problems.
また、我々の実証結果は、ランキング問題に対する2次ロスの有効性を再考することを求めている。
It is striking that iALS achieves competitive or better performance than models learned with ranking losses (LambdaNet, WARP, softmax) which reflect the top-n recommendation task more closely.
iALSは、トップN推薦課題をより忠実に反映するランキング損失で学習したモデル（LambdaNet、WARP、softmax）と同等以上の性能を達成していることが印象的であった。
These observations suggest that further research efforts are needed to deepen our understanding of loss functions for recommender systems.
これらのことから、推薦システムのための損失関数に対する理解を深めるために、さらなる研究努力が必要であることが示唆される。

# Implicit Alternating Least Squares (iALS) 暗黙の交互最小二乗法(iALS)

## Item Recommendation from Implicit Feedback 暗黙のフィードバックからのアイテム推薦

The iALS algorithm targets the problem of learning an item recommender that is trained from implicit feedback [21].
iALSアルゴリズムでは、暗黙のフィードバックから学習されたアイテム推薦器を学習する問題を扱う[21]。
In this problem setting, items from a set I should be recommended to users u ∈ U. For learning such a recommender, a set of positive user-item pairs S⊆U × I is given.
この問題では、ユーザu∈Uに対して集合Iからアイテムを推薦する必要がある。このような推薦器を学習するために、正のユーザ・アイテムペア集合S⊆U × Iが与えられる。
For example, a pair (u, i) ∈ S could express that user u watched movie i, or customer u bought product i. A major difficulty of learning from implicit feedback is that the pairs in S are typically positive only and need to be contrasted with all the unobserved pairs (U × I)∖S.
例えば、ペア(u, i) ∈ Sは、ユーザuが映画iを見たこと、あるいは顧客uが製品iを買ったことを表現することができる。暗黙のフィードバックからの学習の大きな困難は、S中のペアが典型的に正のみで、すべての未観測ペア（U×I）↪Sm16↩Sと対比される必要があることである。
For example, the movies that haven't been watched by a user or the products that haven't been bought by a customer need to be considered when learning the preferences of a user.
例えば、ユーザの嗜好を学習する際には、ユーザが見ていない映画や顧客が買っていない製品を考慮する必要がある。
A recommender algorithm uses S to learn a scoring function $\hat{y} ; U \times I -> \mathbb{R}$ that assigns a score $\hat{y}(u,i)$ to each user-item pair (u, i).
レコメンダーアルゴリズムは、Sを用いて、ユーザとアイテムのペア（u, i）にスコア $hat{y}(u,i)$ を割り当てるスコアリング関数$U \times I -> \mathbb{R}$を学習する。
A common application of the scoring function is to return a ranked list of recommended items for a user u, e.g., sorting all items by $\hat{y}(u,i)$ and recommending the k highest ranked ones to the user.
スコアリング関数の一般的な応用例として、ユーザuに対する推奨アイテムのランク付けリストを返すことが挙げられる。例えば、すべてのアイテムを$hat{y}(u,i)$でソートし、最もランクの高いk個のアイテムをユーザに推奨することが可能である。

## iALS: Model, Loss and Training iALS モデル、損失、トレーニング

iALS uses the matrix factorization model for scoring a user-item pair.
iALSは、ユーザとアイテムのペアをスコアリングするために、行列分解モデルを用いる。
Each user u is embedded into a d dimensional embedding vector Math 4 and every item i into a an embedding vector $w_u \in \mathbb{R}^d$.
各ユーザーuはd次元の埋め込みベクトルMath 4に、各アイテムiは埋め込みベクトル$w_u \in \mathbb{R}^d$に埋め込まれる。
The predicted score of a user-item pair is the dot product between their embedding vectors:
ユーザとアイテムのペアの予測スコアは、それらの埋め込みベクトル間の内積である。
Its scoring function is
そのスコアリング関数は

$$
\hat{y}(u,i) := <w_u, h_i>, W\in \mathbb{R}^{U\times d}, H \in \mathbb{R}^{I \times d} \tag{1}
$$

The model parameters of matrix factorization are the embedding matrices W and H. These model parameters are learned by minimizing the iALS loss, L( W, H), which consists of three components:
行列分解のモデルパラメータは埋め込み行列WとHであり、これらのモデルパラメータは3つの要素からなるiALS損失L( W, H)を最小化することによって学習される。

$$
\begin{align} L(W,H) &= L_S(W,H) + L_I(W,H) + R(W,H) \end{align} \tag*{2}
$$

There exist slightly different definitions for these components in the literature on matrix factorization with ALS.
ALSを用いた行列分解に関する文献では、これらの成分について若干異なる定義が存在する。
We use the formalization that weights all pairs by an unobserved weight [ 2] and allow for frequency-based regularizer as suggested by [ 29] for ALS algorithms for rating prediction.
我々は、すべてのペアを未知の重みで重み付けする形式 [ 2 ] を使用し、格付け予測のためのALSアルゴリズムに [ 29 ] が提案したように、周波数ベースの正則化を可能にします。
The components are defined as:
構成要素は以下のように定義される。

$$
\begin{align} L_S(W,H) &= \sum _{(u,i) \in S} (\hat{y}(u,i) - 1)^2 \end{align}
\tag*{3}
$$

$$
\begin{align} L_I(W,H) &= \alpha _0\sum _{u \in U} \sum _{i\in I} \hat{y}(u,i)^2 \end{align}
\tag*{4}
$$

$$
\begin{align} R(W,H) &= \lambda \left(\sum _{u \in U} \#_u^\nu \, \Vert \mathbf {w}_u\Vert ^2 + \sum _{i \in I}\#_i^\nu \, \Vert \mathbf {h}_i\Vert ^2 \right) \end{align}
\tag*{5}
$$

where
どこ

$$
\begin{align*} \#_u = |\lbrace i : (u,i) \in S\rbrace |+\alpha _0 |I|, \quad \#_i = |\lbrace u : (u,i) \in S\rbrace |+\alpha _0 |U|. \end{align*}
$$

The first component LS is defined over the observed pairs S and measures how much the predicted score differs from the observed label, here 1.
第1成分LSは観測されたペアSに対して定義され、予測スコアが観測されたラベル（ここでは1）とどの程度異なるかを測定するものである。
The second component LI is defined over all pairs in U × I and measures how much the predicted score differs from 0. The third component R is an L2 regularizer that encourages small norms of the embedding vectors.
第二成分LIはU×Iにおける全てのペアに対して定義され、予測スコアが0とどれだけ違うかを測る。第三成分RはL2正則化であり、埋め込みベクトルのノルムが小さくなるように促すものである。
In the regularizer, each embedding is weighted by the frequency it appears in LS and LI. ν controls the strength of the frequency regularizer and can switch between traditional ALS regularization ν = 0 and the frequency regularization weighting ν = 1 that an SGD optimizer would apply implicitly.
νは頻度正則化の強さを制御し、従来のALS正則化ν=0とSGD最適化器が暗黙的に適用する頻度正則化重み付けν=1の間で切り替えることができる。

Individually, it is easy to get a loss of 0 for each component LS, LI, R, however, jointly they form a meaningful objective.
個々には、各成分LS, LI, Rの損失は0になりやすいが、合同で意味のある目的を形成する。
The trade-off between the three components is controlled by the unobserved weight α0 and the regularization weight λ.
この3つの成分のトレードオフは、観測されない重みα0と正則化の重みλによって制御される。
Choosing the proper trade-off is crucial for iALS and is explained in detail in Section A.2.
適切なトレードオフを選択することはiALSにとって重要であり、セクションA.2で詳細に説明される。

The iALS loss can be optimized efficiently by T epochs of alternating least squares, where the computational complexity of each epoch is in $O(d^2
S

# Evaluation 評価

We revisit the performance of iALS on four well-studied benchmarks proposed by other authors.
我々は，他の著者によって提案された4つのよく研究されたベンチマークに対して，iALSの性能を再検討した．
Two of them are item recommendation tasks and two are sampled item recommendation tasks.
そのうち2つは項目推薦タスクであり、2つはサンプル項目推薦タスクである。
We use exactly the same evaluation protocol (i.e., same splits, metrics) as in the referenced papers.
評価プロトコルは参考論文と全く同じものを用いた（すなわち、同じ分割、評価基準）。
Table 1 summarizes the benchmarks and the selected iALS hyperparameters.
表1はベンチマークと選択したiALSのハイパーパラメータをまとめたものである。
For all quality results, we repeated the experiment 10 times and report the mean.
すべての品質結果について、実験を10回繰り返し、その平均値を報告しています。
Our source code is available at https:
ソースコードはhttpsで公開されています。

## Item Recommendation Item Recommendation

Table 1: Benchmarks (dataset and evaluation protocol) used in our experiments.
表1：実験に使用したベンチマーク（データセットと評価プロトコル）。
Our iALS hyperparameters were tuned on holdout sets.
iALSのハイパーパラメータはholdoutセットでチューニングした。
All of the experiments share ν = 1 and σ\* = 0.1.
すべての実験でν = 1とσthes* = 0.1を共有。
For ML1M and Pinterest, we set a maximum dimension of d = 192 for a fair comparison to the results from [9, 22].
ML1MとPinterestについては、[9, 22]の結果と公平に比較するために、最大次元をd = 192に設定した。

In their work about variational autoencoders, Liang et al. [17] have established a set of benchmarks for item recommendation that have been followed by other authors [14, 18, 25, 26] since then.
Liangら[17]は変分オートエンコーダに関する研究の中で、項目推薦のベンチマークを確立し、それ以降、他の著者[14, 18, 25, 26]が追随するようになった。
The benchmarks include results for iALS that were produced in [13, 17].
このベンチマークには、[13, 17]で作成されたiALSの結果も含まれている。
We reinvestigate the results on the Movielens 20M (ML20M) and Million Song Data (MSD) benchmarks.
ここでは、Movielens 20M (ML20M) と Million Song Data (MSD) ベンチマークでの結果を再調査する。
We shortly recap the overall evaluation procedure and refer to [17] and their code2 for details:
評価手順について簡単に説明し、詳細については[17]とそのコード2を参照する。
The evaluation protocol removes all interactions from 10,000 users (ML20M) and 50,000 users (MSD) from the training set and puts them into a holdout set.
評価プロトコルは1万人のユーザ（ML20M）と5万人のユーザ（MSD）のインタラクションをトレーニングセットから取り除き、ホールドアウトセットに格納する。
At evaluation time, the recommender is given 80% of the interactions of each of the holdout users and is asked to generate recommendations for each user.
評価時にレコメンダーに80%のインタラクションが与えられ、各ユーザーに対する推薦文を生成するように指示される。
Each ranked list of recommended items is compared to the remaining 20% of the withheld interactions, then ranking metrics are computed.
各推奨アイテムのランク付けされたリストは残りの20%の保留されたインタラクションと比較され、その後ランキングメトリクスが計算される。
The benchmark provides two versions of the holdout data: one for validation and one for testing.
このベンチマークでは、検証用とテスト用の2つのバージョンのホールドアウトデータが提供される。
We use the validation set for hyperparameter tuning and report results for the testing set in Table 2.
我々は検証用セットをハイパーパラメータのチューニングに使用し、テスト用セットの結果を表2に報告する。
The evaluation setup is geared towards algorithms that make recommendations based on a set of items, like autoencoders or item-based CF, because the evaluation users are not available during training time.
この評価セットアップは、オートエンコーダやアイテムベースCFのように、アイテムのセットに基づいて推薦を行うアルゴリズムに向けられたものであり、評価ユーザは学習時間中に利用できないからである。
Matrix factorization with iALS summarizes the user information in a user embedding which is usually learned at training time – this is not possible for the evaluation users in this protocol.
iALSによる行列分解は、通常、学習時に学習されるユーザ埋め込みにユーザ情報をまとめるが、このプロトコルでは評価ユーザが利用できない。
We follow the evaluation protocol strictly and do not train on any part of the evaluation users.
我々は評価プロトコルに厳密に従い、評価用ユーザのいかなる部分に対しても学習を行いません。
Instead, at evaluation time, we create the user embedding using its closed form least squares expression.
その代わり、評価時にはその閉じた形の最小二乗法を用いてユーザ埋め込みを作成します。
As discussed in [15], matrix factorization can be seen as an item-based CF method where the history embedding (=user embedding) is generated at inference time through the closed form projection.
15]で述べたように、行列分解はアイテムベースのCF手法と見ることができ、閉形式の射影により推論時に履歴埋め込み（＝ユーザ埋め込み）が生成されます。
Note that when using a block solver [23], the user embedding does not have a closed form expression; instead, we perform updates for each block and repeat this 8 times.
なお、ブロックソルバー[23]を用いる場合、ユーザエンベッディングは閉形式ではなく、各ブロック毎に更新を行い、これを8回繰り返す。

Table 2:
表2:
Quality results on the ML20M and MSD benchmark sorted by Recall@20 scores.
ML20MおよびMSDベンチマークにおける品質結果をRecall@20スコアでソートしたもの。

### 3.1.1 Quality. 3.1.1 品質

Table 2 summarizes the benchmark results.
表2は、ベンチマーク結果をまとめたものである。
The table highlights the previously reported numbers for iALS and our numbers.
この表は、以前に報告されたiALSの数値と我々の数値を強調しています。
Previously, matrix factorization with iALS was found to perform poorly with a considerable gap to the state of the art.
以前、iALSを用いた行列分解は性能が低く、最新技術との間にかなりのギャップがあることが判明しています。
Both Mult-VAE [17] and the follow-up work RecVAE [25], H+Vamp (Gated) [14], RaCT [18] and EASE [26] outperform the previously reported iALS results on both datasets.
Mult-VAE[17]とその後続のRecVAE[25]、H+Vamp (Gated) [14] 、RaCT [18] 、EASE [26]は、両データセットにおいて、以前に報告されたiALSの結果を上回ります。
However, we obtain considerably better results for iALS matrix factorization than the previously reported iALS numbers.
しかし、iALSの行列分解については、既報のiALSの数値よりもかなり良い結果が得られています。
On the MSD dataset only one method, EASE, outperforms our iALS results.
MSDデータセットでは、1つの手法であるEASEのみが我々のiALSの結果を上回った。
On the ML20M dataset, iALS has comparable performance to Mult-VAE.
ML20Mデータセットでは、iALSはMult-VAEと同程度の性能を示しました。
No method consistently outperforms our iALS results over both datasets and all measures, but iALS consistently outperforms CDAE, Mult-DAE, SLIM, WARP.
両データセット、全測定値においてiALSの結果を一貫して上回る手法はないが、iALSはCDAE、Mult-DAE、SLIM、WARPを一貫して上回っている。
For the remaining methods, iALS is tied with 3 wins out of 6 comparisons.
残りの手法については、iALSは6つの比較のうち3つの勝利で同点である。
It is interesting to note that most high quality results in Table 2 have been obtained by the inventors of the corresponding methods which indicates that knowledge about an algorithm is useful for obtaining good results and that automated hyperparameter search alone might not be sufficient.
これは、アルゴリズムに関する知識が良い結果を得るために有用であり、自動化されたハイパーパラメータ探索だけでは十分でない可能性があることを示しています。

![](https://dl.acm.org/cms/attachment/50001494-5d72-429e-8e5c-455c715845cb/recsys22-140-fig1.jpg)

Figure 1: Our iALS benchmark results with a varying embedding dimension, d. For comparison, the plots contain also the previous iALS results from [17], EASE [26] and Mult-VAE [17].
図1: 埋め込み次元dを変化させたiALSのベンチマーク結果。比較のため、[17]、EASE [26]、Mult-VAE [17]による過去のiALS結果もプロットしています。
The capacity for EASE, Mult-VAE and prev. iALS is not varied in the plot and the numbers represent the best values reported in previous work (see Section 3.1.2 for details).
EASE、Mult-VAE、prev.iALSの容量はプロット上で変化させず、数値は過去の研究で報告された最良の値を表しています（詳細は3.1.2節を参照ください）。

### 3.1.2 Model Capacity 3.1.2 モデル容量

Embedding Dimension.
エンベッディングディメンション。
The ML20M and MSD benchmarks focus mainly on quality and Table 2 reported the best quality without considering model size and capacity.
ML20MとMSDベンチマークは主に品質に重点を置いており、表2はモデルサイズと容量を考慮せずに最高の品質を報告しました。
Now, we discuss the trade-off between quality and model capacity of iALS and compare it to EASE and Mult-VAE as well as the previously reported iALS numbers from [17].
ここで、iALSの品質とモデル容量のトレードオフについて議論し、EASEやMult-VAE、また以前報告された[17]のiALSの数値と比較します。
We measure model capacity by the number of parameters that a model reserves for each item.
モデル容量は、モデルが各項目に対して予約するパラメータ数で測定する。
For iALS and Mult-VAE the item parameters are item embeddings and for EASE the parameters are in the item-to-item weight matrix.
iALSとMult-VAEではアイテムのパラメータはアイテム埋め込みで、EASEではパラメータはアイテム間の重み行列である。
Mult-VAE has two item embeddings: one for the input items and one for the output items.
Mult-VAEは、入力アイテム用と出力アイテム用の2つのアイテム埋め込みを持っています。
Mult-VAE has additional parameters in the hidden units but the number of parameters in these units is small, so we ignore their size in the comparison of this section.
Mult-VAEは隠れユニットに追加のパラメータを持つが、これらのユニットのパラメータ数は少ないので、本節の比較ではその大きさを無視する。
During training, iALS also requires space for user embeddings, however at prediction time, embeddings of test users are computed on the fly from item embeddings.
iALSは学習時にはユーザの埋め込みも必要とするが、予測時にはテストユーザの埋め込みはアイテムの埋め込みからオンザフライで計算される。

Figure 1 breaks down the performance of iALS by embedding dimension and also includes the best results previously reported for iALS, EASE and Mult-VAE.
図1は、iALSの性能を埋め込み次元別に分類したもので、iALS、EASE、Mult-VAEでこれまでに報告された最良の結果も含まれています。
We report the following variations:
以下のバリエーションを報告します。

- iALS (our results)3: We explore embedding dimensions of d ∈ {64, 128, 256, 512, 1024, 2048} for ML20M and d ∈ {128, 256, 512, 1024, 2048, 4096, 8192} for MSD. iALS（我々の結果）3：ML20Mではd∈{64, 128, 256, 512, 1024, 2048}、MSDではd∈{128, 256, 512, 1024, 2048, 4096, 8192}の埋め込み次元を探索した結果。

- Mult-VAE: We use the results from [17] that were generated with 600 dimensional item embeddings for input and output embeddings, so in total Mult-VAE has 1200 free parameters per item. Mult-VAE：入力と出力の埋め込みに600次元の項目埋め込みを行った[17]の結果を用いているので、合計で1項目あたり1200の自由パラメータを持つことになります。

- EASE: This is a dense model with |I|2 model parameters, where each item has |I| many free parameters. That means for ML20M, the EASE model has 20,108 model parameters per item and for MSD it has 41,140 model parameters per item, which is over an order of magnitude more parameters than Mult-VAE. 

- iALS (previous results): These results are from [17] and use item embeddings of d ≤ 200. iALS (以前の結果)。 この結果は[17]のもので、d ≤ 200の項目埋め込みを用いたものである。

Table 3:
表3:
Quality results on the Movielens 1M and Pinterest benchmarks [9] sorted by HR@10 on ML1M.
Movielens 1MとPinterestベンチマーク[9]の品質結果をML1MのHR@10でソートしたもの。
The previously reported numbers for iALS (and its eALS variation), and our iALS numbers are in bold.
iALS（とそのバリエーションであるeALS）の既報の数値と、我々のiALSの数値は太字で表示されています。
The best number is underlined.
ベストな数値には下線が引かれています。

The plots in Figure 1 show that all well performing models on this benchmark have a large capacity.
図1のプロットは、このベンチマークで良好な性能を示したすべてのモデルが、大きな容量を持つことを示している。
For iALS, the gain of large embedding dimensions slowly levels off around d = 1024 (for ML20M) and d = 8192 (for MSD).
iALSの場合、埋め込み次元が大きいことによる利得は、d = 1024（ML20M）およびd = 8192（MSD）のあたりでゆっくりとレベルダウンしています。
When looking at smaller iALS dimensions, d = 1024 outperforms Mult-VAE on the MSD dataset, and a dimension of d = 512 outperforms EASE on ML20M.
iALSの小さい次元を見ると、MSDデータセットではd = 1024がMult-VAEを上回り、ML20Mではd = 512の次元がEASEを上回ります。
The MSD benchmark is interesting because the best performing methods, EASE and iALS (d = 8192) are much simpler than the advanced autoencoder methods that perform the best on ML20M.
MSDベンチマークは、最も性能の良いEASEとiALS（d = 8192）が、ML20Mで最も性能の良い高度なオートエンコーダ手法よりもはるかに単純であるため、興味深いものです。
However, both EASE and iALS (d = 8192) have a very large model capacity in the item representation.
しかし、EASEとiALS (d = 8192)は共に項目表現において非常に大きなモデル容量を持っている。
That might indicate that the MSD dataset has structure that is different from ML20M, for example it might have a very high rank.
これは、MSDデータセットがML20Mとは異なる構造、例えば非常に高いランクを持っている可能性を示しているのかもしれない。

When comparing our iALS results to the previously reported iALS results [17], we can see that on ML20M, they outperform the previous results substantially, even with a smaller embedding dimension.
我々のiALSの結果を既報のiALSの結果[17]と比較すると、ML20M上では、埋め込み次元を小さくしても、既報の結果を大幅に上回っていることがわかる。
This shows the importance of well-tuned hyperparameters.
これは、よく調整されたハイパーパラメータの重要性を示しています。
On MSD, our results are in line with the previous iALS results for a comparable embedding dimension.
MSDでは、埋め込み次元が同程度の場合、我々の結果は以前のiALSの結果と一致します。
However, increasing the embedding dimension results in large improvements.
しかし、埋め込み次元を大きくすることで、大きな改善効果が得られます。
Choosing a comparable capacity as VAE, it outperforms the previously reported iALS quality substantially.
VAEと同等の容量を選択すると、以前に報告されたiALSの品質を大幅に上回ります。

To summarize, the trade-off between quality and model size of iALS is competitive with the state of the art Mult-VAE and EASE models.
要約すると、iALSの品質とモデルサイズのトレードオフは、最先端のMult-VAEモデルやEASEモデルと競合するものです。

### 3.1.3 Runtime. 3.1.3 ランタイム。

Finally, the comparison so far ignored runtime.
最後に、これまでの比較ではランタイムを無視した。
One training epoch of a multithreaded (single-machine) C++ implementation of iALS (using the block solver from [23]) took about 1 minute for d = 2048 on ML20M and 40 minutes for d = 8192 on MSD.
iALSのマルチスレッド（シングルマシン）C++実装（[23]のブロックソルバーを使用）の1つのトレーニングエポックは、ML20Mのd = 2048で約1分、MSDのd = 8192で40分かかりました。
And for smaller dimensions:
また、より小さい次元では
30 seconds for d = 1024 on ML20M and 1 minute 30 seconds for d = 1024 on MSD.
ML20Mではd = 1024で30秒、MSDではd = 1024で1分30秒でした。
While we ran the experiments for 16 epochs, i.e., the total runtime is 16 times higher, the results are almost converged much earlier.
16エポック分の実験を行ったため、総実行時間は16倍になりましたが、結果はかなり早くほぼ収束しました。
For example for MSD and d = 8192 the quality results after four epochs are Recall@20=0.305, Recall@50=0.412, NDCG@100=0.363.
例えば、MSDとd = 8192の場合、4エポック後の品質結果はRecall@20=0.305, Recall@50=0.412, NDCG@100=0.363 です。
It is up to the application if it is worth spending more resources to train longer.
より長く学習するためにより多くのリソースを費やす価値があるかどうかは、アプリケーション次第です。

## Sampled Item Recommendation サンプル品推奨

We also investigate the performance of iALS on the sampled item recommendation benchmarks from [9] which have been used in multiple publications, including [1, 6, 17, 22].
また、[1, 6, 17, 22]を含む複数の論文で使用されている[9]のサンプルアイテム推薦ベンチマークでiALSの性能を調査した。
The benchmark contains two datasets, Pinterest [7] and an implicit version of Movielens 1M (ML1M) [8].
このベンチマークには、Pinterest [7]とMovielens 1M (ML1M) [8]の暗黙的バージョンの2つのデータセットが含まれている。
The evaluation protocol removes one item from each user's history and holds it out for evaluation.
評価プロトコルは，各ユーザの履歴から 1 つの項目を削除し，評価のために保持する．
At evaluation time, the recommender is asked to rank a set of 101 items, where 100 of them are random items and one is the holdout item.
評価時に，レコメンダーは 101 個のアイテム（100 個はランダムなアイテム，1 個は保留されたアイテム）をランク付けするよう要求される．
The evaluation metrics measure at which position the recommender places the withheld items.
評価指標は、レコメンダーが保留項目をどの位置に置くかを測定する。
As discussed in [16], this evaluation task is less focused on the top items than the measured metrics indicate.
16]で議論したように、この評価タスクは測定されたメトリクスが示すよりも上位のアイテムに焦点が当てられていない。
We follow the same procedure as in [22] for hyperparameter tuning by holding out data from training for tuning purposes.
ハイパーパラメータのチューニングについては、[22]と同様の手順で、チューニングのために学習からデータを保留しておく。

Table 3 summarizes the results.
表3はその結果をまとめたものである。
The original comparison in [9] reports results for eALS [10] which is a coordinate descent solver for iALS.
9]では、iALSの座標降下ソルバーであるeALS [10]の結果が報告されている。
Follow up work [6] provided results for iALS which have been reproduced in [1].
フォローアップ研究[6]はiALSの結果を提供し、それは[1]で再現されている。
The previously reported performance of eALS and iALS is poor and not competitive on both measures and both datasets.
以前報告されたeALSとiALSの性能は、両方の指標と両方のデータセットにおいて貧弱であり、競争力がない。
However, with well tuned hyperparameters, we could achieve a high quality on all metrics with iALS.
しかし、ハイパーパラメータをうまく調整することで、iALSでは全ての指標で高い品質を達成することができた。
The results are very close to the ones for a well tuned SGD optimized matrix factorization [22] – which is expected as both are matrix factorization models with a comparable loss.
この結果は、よく調整されたSGD最適化行列分解[22]の結果に非常に近く、これは両者が同等の損失を持つ行列分解モデルであることから予想されることです。
The well-tuned iALS is better than NCF on three metrics and tied on one.
よく調整されたiALSは、3つの指標でNCFより優れており、1つの指標では同点でした。
It is also better than Mult-DAE [17] on three metrics and worse on one.
また、Mult-DAE[17]よりも3つの指標で優れており、1つの指標では劣っています。
Furthermore it outperforms EASE [26] and SLIM [19] on all metrics.
さらに、iALSはすべての指標においてEASE [26]とSLIM [19]を上回る性能を示した。
Note that we limited the embedding dimension for iALS to d = 192 to be comparable to the previously obtained results for NCF and SGD matrix factorization.
なお、iALSの埋め込み次元は、NCFやSGDの行列分解で以前に得られた結果と比較できるように、d = 192に制限しました。
We also produced results for smaller dimensions and d = 64 without further hyperparameter tuning works reasonably well: for ML1M HR@10=0.722 and NDCG@10=0.445 and for Pinterest HR@10=0.892, NDCG@10=0.573.
また、より小さい次元の結果も出しており、更なるハイパーパラメータのチューニングを行わないd = 64は、ML1M HR@10=0.722, NDCG@10=0.445 とPinterest HR@10=0.892, NDCG@10=0.573 に対して、それなりにうまく機能しています。

# CONCLUSION 結論

This work reinvestigated matrix factorization with the iALS algorithm and discussed techniques to obtain high quality models.
本研究では、iALSアルゴリズムによる行列分解を再調査し、高品質なモデルを得るための手法について議論した。
On four well-studied item recommendation benchmarks, where iALS was reported to perform poorly, we found that it can actually achieve very competitive results when the hyperparameters are well tuned.
iALSの性能が低いと報告されていた4つのよく研究された項目推薦ベンチマークにおいて，ハイパーパラメータをうまく調整すれば，実際に非常に競争力のある結果を得られることが分かった．
In particular, none of the recently proposed methods consistently outperforms iALS.
特に、最近提案されたどの手法もiALSを一貫して上回らないことがわかった。
On the contrary, iALS outperforms any method on at least half of the metrics and datasets: iALS improves over a neural autoencoder in 6 out of 10 comparisons and over EASE in 7 out of 10.
iALSは10個の比較のうち6個でニューラルオートエンコーダを、7個でEASEを上回った。

These benchmarks focus on prediction quality but ignore other aspects such as training time, scalability to large item catalogs or serving of recommendations. iALS is known to excel in these dimensions: (i) It is a second order method with convergence in a few epochs. (ii) It uses the Gramian trick that solves the issue of
U

iALS also has some challenges: (i) Its loss is less aligned with ranking metrics but surprisingly, it achieves high ranking metrics on benchmarks, on par with models that optimize ranking losses such as lambdarank and softmax.
iALSにも課題はある。(i)iALSの損失はランキング指標とあまり整合していないが、驚くべきことに、lambdarankやsoftmaxなどのランキング損失を最適化するモデルと同等に、ベンチマークで高いランキング指標を達成した。
Also EASE and SLIM that share the quadratic loss with iALS do not suffer from the quadratic loss on these benchmarks.
また、iALSと二次損失を共有するEASEやSLIMも、これらのベンチマークでは二次損失に悩まされることがない。
(ii) In its simplest form discussed in this paper, iALS learns a matrix factorization model, making it less flexible for richer problems with extra features.
(ii) 本論文で議論した最も単純な形式では、iALSは行列分解モデルを学習するため、余分な特徴を持つリッチな問題に対する柔軟性に欠ける。
However, iALS has been extended for more complex models as well [2, 11, 21].
しかし、iALSはより複雑なモデルに対しても拡張されている[2, 11, 21]。
(iii) Finally, matrix factorization requires recomputing the user embedding whenever a user provides new feedback.
(iii) 最後に、行列分解は、ユーザが新しいフィードバックを提供するたびに、ユーザ埋め込みを再計算する必要がある。
Bag of item models like SLIM, EASE or autoencoders do not require retraining but can just make inference using the modified input.
SLIM、EASE、オートエンコーダのようなBag of itemモデルは再トレーニングを必要とせず、変更された入力を使って推論を行うことができる。
Nevertheless, the user embedding of iALS has a closed form expression and this can be seen as the inference step of iALS.
しかし、iALSのユーザー埋め込みは閉じた形の式を持ち、これはiALSの推論ステップと見なすことができる。
Instead of passing the history through an encoder, in iALS a different computation (the solve step) is performed.
iALSでは、履歴をエンコーダーに通す代わりに、別の計算（解決ステップ）が実行される。

We hope that the encouraging benchmark results for iALS spark new interest in this old technique.
私たちは、iALSのベンチマーク結果が、この古い手法に新たな関心を呼び起こすことを期待しています。
Other models, such as autoencoders or SLIM, benefited from a growing interest in item-based collaborative filtering that resulted in improved versions such as Mult-VAE, RecVAE or EASE.
オートエンコーダやSLIMのような他のモデルは、アイテムベースの協調フィルタリングへの関心が高まり、Mult-VAE、RecVAE、EASEなどの改良型が生まれたことで利益を得ました。
The basic iALS model might have similar potential for improvements.
iALSの基本モデルにも、同様の改良の可能性があると思われます。
Besides academia, iALS should be considered as a strong option for practical applications. iALS has very appealing properties in terms of runtime, scalability and low top-n querying costs, and as this study argues, it also performs well on benchmarks in terms of quality.
iALSは、実行時間、スケーラビリティ、低いトップNクエリコストの点で非常に魅力的な特性を持ち、本研究が主張するように、品質の点でもベンチマークで良い結果を出している。

Finally, this paper is another example for the difficulty of tuning machine learning models [24].
最後に、本論文は機械学習モデルのチューニングの難しさを示すもう一つの例である[24]。
Converging to reliable numbers is a process that takes time and needs a community effort.
信頼できる数値に収束させるのは時間がかかるプロセスであり、コミュニティの努力が必要である。
Over the long term, shared benchmarks like the ones established in the VAE paper [17] and adopted by other researchers [14, 18, 25, 26] are a way to make progress towards reliable numbers.
長期的には、VAE論文[17]で確立され、他の研究者[14, 18, 25, 26]によって採用されたような共有ベンチマークが、信頼できる数値に向けた前進の方法である。
Until then, it should be understood that both the benchmark results that we achieve with iALS and the ones from the other methods might be further improved in the future.
それまでは、iALSで達成したベンチマーク結果も、他の手法による結果も、将来的にはさらに改善される可能性があることを理解しておく必要があります。

# Hyperparameter Search for iALS iALSのハイパーパラメータ探索

In this section, we give guidelines on how to choose hyperparameter values for iALS.
本節では、iALSのハイパーパラメータ値の選び方について指針を示す。
The six hyperparameters4 of iALS are summarized in Table 4.
iALSの6つのハイパーパラメータ4は表4のようにまとめられている。

As our experiments in Section 3 indicate, good hyperparameter values are crucial for obtaining a high quality model.
セクション3での実験が示すように、優れたハイパーパラメータ値は高品質なモデルを得るために極めて重要である。
To obtain good hyperparameter values, it is important to focus the search on the important hyperparameters and spent only little time on the unimportant ones.
良いハイパーパラメータ値を得るためには、重要なハイパーパラメータに探索を集中させ、重要でないものにはわずかな時間しかかけないことが重要である。
Any reduction of the search space is very important when dealing with exponential complexity.
指数関数的な複雑さを扱う場合、探索空間の縮小は非常に重要である。
In this section, we will describe the meaning of the iALS hyperparameters in detail.
このセクションでは、iALSのハイパーパラメータの意味について詳しく説明する。
A detailed understanding of the hyperparameters will allow us to eliminate most hyperparameters from a time consuming grid-search and focus on the important regularization value λ and unobserved weight α0.
ハイパーパラメータを詳細に理解することで、時間のかかるグリッドサーチからほとんどのハイパーパラメータを排除し、重要な正則化値λと非観測重みα0に焦点を当てることができる。

## Metrics メトリクス

While exploring hyperparameters, it is useful to look at several metrics.
ハイパーパラメータを探索する際に、いくつかのメトリクスを見ることは有用である。
Obviously, measuring the validation metric (e.g., Recall or NDCG on a holdout set) is useful and will drive the overall exploration.
明らかに、検証メトリック（例えば、ホールドアウト集合でのリコールやNDCG）を測定することは有用であり、全体的な探索を推進することになります。
However, the validation metrics are often only loosely connected with the training process and might not reveal why a particular hyperparameter choice does not work.
しかし、検証メトリックは、しばしば学習プロセスと緩やかな関係しかなく、特定のハイパーパラメータの選択がなぜうまくいかないかを明らかにしないかもしれません。
To spot some issues with learning related hyperparameters, we found it useful to plot the training loss L and its components LS, LI, R as well.
学習関連のハイパーパラメータの問題を発見するために、学習損失Lとその成分LS、LI、Rもプロットすることが有用であることがわかりました。
These training losses can reveal if the hyperparameters are in the wrong region and can be useful in the beginning of the hyperparameter search.
これらの学習損失は、ハイパーパラメータが間違った領域にあるかどうかを明らかにすることができ、ハイパーパラメータ探索の初期に有用となることがあります。

Table 4: Hyperparameters of iALS.
表4：iALSのハイパーパラメータ。

![](https://d3i71xaburhd42.cloudfront.net/2cc27e89b6b174eb356dd33d00d70fda65b3f7e6/6-Table1-1.png)

## Hyperparameters ハイパーパラメータ

The metrics help to guide the hyperparameter search.
メトリクスは、ハイパーパラメータの探索をガイドするのに役立つ。
It is important to understand the hyperparameters and reduce the search space early and then focus on the important hyperparameters.
ハイパーパラメータを理解し、早期に探索空間を縮小し、重要なハイパーパラメータに集中することが重要である。
We also don't recommend tuning a large set of hyperparameters jointly but to explore them iteratively.
また、大規模なハイパーパラメータのセットを合同でチューニングすることは推奨しませんが、繰り返し探索することは可能です。

Number of Training Iterations.
トレーニングの反復回数。
It is advisable to measure the metrics during training after each iteration.
各反復の後、トレーニング中のメトリクスを測定することが望ましい。
This removes the number of iterations T from the search space – provided that T is large enough.
Tが十分に大きければ、反復回数Tを探索空間から取り除くことができます。
A too large value of T is not a concern with respect to quality, but only with respect to runtime. iALS converges usually within a few iterations and a reasonable initial choice could be 16 iterations.
iALSは通常数回の反復で収束するため、初期値として16回の反復を選択するのが妥当である。
Depending on the observed convergence curve, this value can be increased or decreased later.
観測された収束曲線に応じて、この値は後で増減させることができます。
For speeding up exploration, we also found it useful to use a smaller value during initial exploration of the hyperparameter space, and then increase it for the final search.
また、探索を高速化するために、ハイパーパラメータ空間の初期探索時に小さい値を使用し、最終探索時にそれを大きくすることも有用であることがわかりました。
For example, using 8 instead of 16 iterations during a broad search will cut the runtime in half.
例えば、広範な探索の際に16回ではなく8回の反復を使用すると、実行時間が半分になります。

Standard Deviation for Initialization.
初期化のための標準偏差。
Usually, the standard deviation for iALS is easy to set and we haven't observed much sensitivity within a broad range.
通常、iALSの標準偏差は簡単に設定でき、広い範囲での感度はあまり観測されていない。
Instead of setting the hyperparameter σ, it helps to rescale it by the embedding dimension
ハイパーパラメータσを設定する代わりに、埋め込み次元で再スケールすることが有効です

$$
\sigma = \frac{1}{\sqrt{d}} \sigma^*
\tag*{6}
$$

where σ * is a small constant, such as 0.1.
ここで、σ * は0.1などの小さな定数である。
This makes the initialization less sensitive to large changes in the embedding dimension.
これにより、埋め込み次元の大きな変化に対して、初期化の影響を受けにくくなります。
The intuition is that this keeps the variance of a random dot product constant, i.e., the variance of predictions at initialization is independent of d.
直感的には、これによりランダムドット積の分散が一定に保たれる、すなわち、初期化時の予測値の分散がdに依存しなくなる、ということである。

We only observe some sensitivity if the value for the standard deviation is chosen orders of magnitude too small or too large.
標準偏差の値が小さすぎたり大きすぎたりした場合にのみ、いくつかの感度を観察することができます。
In this case, it takes a few extra steps for iALS to readjust the norms of the user and item embeddings.
この場合、iALSはユーザーとアイテムの包埋の規範を再調整するために、いくつかの余分なステップを必要とします。
This can be spotted easily by plotting L, LS, LI and R where LS will not drop immediately.
これはL、LS、LI、Rをプロットすることで容易に発見することができ、LSはすぐに低下することはありません。

Embedding Dimension.
エンベッディングディメンション。
The embedding dimension controls the capacity of the model.
埋め込み次元は、モデルの容量をコントロールします。
From our experience, a common reason for suboptimal results with iALS is that the embedding dimension is chosen too small.
我々の経験では、iALSで最適な結果が得られない共通の理由は、埋め込み次元が小さく選ばれすぎていることです。
We usually observe that, with proper regularization, the larger the embedding dimension the better the quality.
我々は通常、適切な正則化を行えば、埋め込み次元を大きくすればするほど、品質が向上することを確認しています。
For example, for the Movielens 20M dataset, we found that 2000 dimensions provide the best results.
例えば、Movielens 20Mのデータセットでは、2000次元が最も良い結果をもたらすことがわかりました。
It may seem that a 2000 dimensional embedding is too expressive for a dataset that has 73 ratings per user on average.
一人当たり平均73件の評価を持つデータセットに対して、2000次元の埋め込みは表現力が豊かすぎると思われるかもしれません。
And even worse it might lead to overfitting.
また、さらに悪いことに、オーバーフィッティングを引き起こすかもしれません。
However, empirically, larger dimensions are better and L2 regularization is very effective at preventing overfitting.
しかし、経験的に、次元は大きい方がよく、L2正則化はオーバーフィッティングを防ぐのに非常に効果的です。
Moreover, other successful models such as VAE are also trained with large embedding dimensions and full rank models such as EASE are also effective.
さらに、VAEなどの他の成功モデルも大きな埋め込み次元で学習していますし、EASEなどのフルランクモデルも有効です。
The effectiveness of large embedding dimensions for matrix factorization is also well studied in the rating prediction literature [15, 20, 29].
行列分解における大きな埋め込み次元の有効性は、視聴率予測に関する文献でもよく研究されています[15, 20, 29]。

![](https://dl.acm.org/cms/attachment/4e7097e6-fce8-4b0e-9f90-26605004a8c2/recsys22-140-fig2.jpg)

Figure 2: When using frequency-scaled regularization, ν, good regularization values λ are in different regions for different choices of ν (left).
図2：周波数スケールの正則化νを用いた場合、正則化の良い値λはνの選択によって異なる領域に存在する（左）。
A shifted regularization scale λ* brings good values on the same scale as a reference scale ν*.
正則化スケールλ*をシフトさせると、基準スケールν*と同じスケールで良好な値が得られる。
The middle plot shows scaling to the reference ν* = 0, the right to the reference ν* = 1.
中央のプロットは基準スケールν* = 0へのスケーリング、右は基準スケールν* = 1へのスケーリングを示す。

Computational resources are an important factor when choosing the embedding dimension.
埋め込み次元を選択する際には、計算機資源が重要な要素となる。
A good strategy is to first get a rough estimate of good hyperparameter values using a mid-sized embedding dimension, such as d = 128, and then to perform a more refined search using larger embedding dimensions, e.g., doubling the dimension during each refinement of the other hyperparameters until the improvement plateaus.
良い方法は、まずd = 128のような中間のサイズの埋め込み次元を使って、良いハイパーパラメータ値の大まかな推定値を得て、次に大きな埋め込み次元を使ってより洗練された探索を行うことです。
This way, the first pass is sufficiently fast and more time can be spent for the detailed search of the most important parameters: unobserved weight and regularization.
この方法では、最初のパスが十分に速く、より多くの時間を最も重要なパラメータである非観測重みと正則化の詳細な探索に費やすことができます。

### Unobserved Weight and Regularization. 非観測重みと正則化。

Both unobserved weight α0 and the regularization λ are crucial for iALS 5 and it is important to choose them carefully.
iALS 5では、観測されない重みα0と正則化λの両方が重要であり、これらを慎重に選択することが重要である。
It is advisable to search the unobserved weight together with the regularization because both of them control the trade-off between the three loss components, LS, LI and R. Intuitively, we know that for item recommendation we need both LS and LI – otherwise the solution degenerates to always predicting 1 (if α0 = 0) or always predicting 0 (if α0 → ∞).
直感的には、項目推薦にはLSとLIの両方が必要であり、さもなければ、常に1を予測する（α0 = 0の場合）か、常に0を予測する（α0 → ∞の場合）ことに退化することが分かっている。
So, the observed error values of LS and LI shouldn't differ by several orders of magnitude.
そのため、LSとLIの誤差は数桁も違わないはずです。
Similarly, with large embedding dimensions, we need some regularization, so again the values of R, LS and LI should have comparable orders of magnitude.
同様に、埋め込み次元が大きいと、ある程度の正則化が必要なので、やはりR、LS、LIの値は同程度のオーダーになるはずです。

The scale of regularization values depends on ν (Eq. (5)) which sets the strength of frequency regularization – see Figure 2 left side for an example. Without frequency regularization, ν = 0, good regularization values are typically larger than 1, for frequency regularization ν = 1, good regularization values are usually smaller than 1. This is because the regularization value λ is scaled by (I(u) + α0
I

$$
\begin{align} \lambda &= \lambda ^* \frac{\sum _{i \in I} (|U(i)| + \alpha _0 |U|)^{\nu ^*} + \sum _{u \in U} (|I(u)| + \alpha _0 |I|)^{\nu ^*}}{\sum _{i \in I} (|U(i)| + \alpha _0 |U|)^{\nu } + \sum _{u \in U} (|I(u)| + \alpha _0 |I|)^{\nu }}, \end{align}
$$

where ν * is the reference scale.
ここで、ν *は基準スケールである。
For example, if we want the regularization values for all ν to be in the same region as ν = 0, we would choose ν * = 0. See Figure  2 middle, where good regularization values λ * are in the same region for ν = 1 as for ν = 0. The right plot in Figure  2 shows a case where ν * = 1 is chosen as the reference and good regularization values for ν = 0 are shifted to the region of the frequency regularized version ν = 1.
例えば、すべてのνの正則化値をν = 0と同じ領域にしたい場合は、ν * = 0を選びます。図2中、ν = 1の正則化値λ *はν = 0と同じ領域にあります。図2右は、ν * = 1を基準として、ν = 0の良い正則化値は周波数正則化の領域ν = 1へシフトしている場合を示しています。
Which reference ν * to pick depends on the practitioner and the application.
どの基準ν * を選ぶかは、実務者や用途によって異なる。
For example, if there is a comparison to SGD algorithms, choosing the reference as ν * = 1 might be useful.
例えば、SGDアルゴリズムとの比較がある場合、ν * = 1を基準に選ぶと便利かもしれません。
Or if a practitioner is more familiar with common ALS algorithms, ν * = 0 might be better.
また、一般的なALSアルゴリズムに精通している場合は、ν * = 0の方がよいかもしれません。
Note that the discussed rescaling of λ does not introduce any new hyperparameters and is for convenience only.
λの再スケーリングは、新しいハイパーパラメータを導入するものではなく、便宜上そうしているだけであることに注意してください。
Also ν * is an arbitrary choice of a reference, it does not need any tuning and (unlike ν) has no effects on the solution; it just simplifies the hyperparameter search for regularization values, λ. Unless stated otherwise, in the following we discuss λ * with a reference point of ν * = 1.
また、ν *は任意の基準選択であり、チューニングの必要はなく、（νとは異なり）解に影響を与えず、正則化値λのハイパーパラメータ探索を簡略化するだけです。

After the relationship of the parameters has been described, we want to give some practical advice on the search.
パラメータの関係を説明した後、探索に関する実用的なアドバイスをしたいと思います。
When setting the unobserved weight one should consider the degree of matrix sparseness.
観測されない重みを設定する場合、行列の疎密の度合いを考慮する必要があります。
It is advised that the overall magnitude of the unobserved loss term (LI(W, H) eq. (4)) does not dominate that of the observed loss term (LS(W, H) eq. (3)).
観測されない損失項（LI（W，H）式（4））の全体の大きさが、観測された損失項（LS（W，H）式（3））のそれを支配しないようにすることが望ましいです。
Thus, usually, the unobserved weight is smaller than 1.0 and is decreasing for sparser matrices6.
したがって、通常、観測されない重みは1.0より小さく、より疎な行列に対して減少している6。
A good starting point is an exponential grid, for example α0 ∈ {1, 0.3, 0.1, 0.03, 0.01, 0.003}.
良い出発点は指数グリッドで、例えばα0∈{1, 0.3, 0.1, 0.03, 0.01, 0.003}のようなものです。
For the regularization, a good starting point is λ* ∈ {0.1, 0.03, 0.01, 0.003, 0.001, 0.0003}.
正則化については、λ*∈{0.1, 0.03, 0.01, 0.003, 0.001, 0.0003}が良いスタートポイントになります。
The regularization becomes especially important for larger embedding dimensions.
正則化は埋め込み次元が大きくなると特に重要になります。
If the hyperparameter search is performed on too small an embedding dimension, the regularization value found on the small dimension might not be a good one for larger dimensions.
埋め込み次元が小さすぎる場合にハイパーパラメータ探索を行うと、小さい次元で見つけた正則化値が大きい次元では良い値でない可能性があります。
A large enough dimension (e.g., d = 128) can be used to get a rough estimate on which area a finer search with a higher dimension should focus on.
十分に大きな次元（例えば、d = 128）は、より高い次元でのより細かい探索がどの領域に焦点を当てるべきかのおおまかな見積もりを得るために使用することができます。
The suggested parameters are a starting point and need to be refined based on the results.
提案されたパラメータは出発点であり、結果に基づいて改良される必要がある。

Some additional notes:
補足説明

- The training errors L for different hyperparameter settings are not comparable and should not be used for selecting a model. ハイパーパラメータの設定が異なる場合の学習誤差Lは比較できないので、モデルの選択には使用しないでください。

- Plotting curves for validation quality vs. log unobserved weight and validation quality vs. log regularization can help to get an idea which parts can be abandoned and where to refine. In general, we would expect to see some  ∪ -shaped curve (for error) or  ∩ -shaped curve (for quality) for the parameters – if not, then the boundaries of the search may need to be expanded (see Figure 2 for an example). Also the change in quality between two neighboring hyperparameter values shouldn't be too abrupt, otherwise more exploration is needed. 検証品質とlog unobserved weight、検証品質とlog regularizationの曲線をプロットすると、どの部分を捨てて、どこを改良すればいいのかがわかります。 一般的には、パラメータに対して∪字型の曲線（誤差の場合）または∩字型の曲線（品質の場合）が見られると思われますが、もしそうでなければ、探索の境界を広げる必要があるかもしれません（例として図2参照）。 また、2つの隣接するハイパーパラメータ値間の品質の変化はあまり急激であってはならず、そうでなければより多くの探索が必要です。

- It also helps not to refine exclusively around the best results, but to look at the overall behavior of the curves to get a better understanding of how hyperparameters interact on a particular data set. また、最良の結果を中心に絞り込むのではなく、曲線の全体的な挙動を見て、特定のデータセットでハイパーパラメータがどのように作用するかをよりよく理解することができます。

- Measuring the noise in the validation metrics (i.e., if the same experiment is repeated twice, how much do the numbers differ) is also useful to avoid reading too much into a single experiment. 検証指標のノイズを測定する（同じ実験を2回繰り返した場合、どの程度数値が異なるか）ことも、1回の実験に深読みしないために有効である。

- At some point, large embedding dimensions should be considered. Doubling the embedding dimensions until no improvement is observed is a good strategy. If no improvement is observed, a refined search of regularization and unobserved weight might be needed. Then one can double the embedding dimension again. ある時点で、大きな埋め込み次元を考慮する必要があります。 改善が見られないまで埋め込み次元を2倍にするのは良い戦略です。 もし、改善が見られない場合は、正則化と未観測の重みの精緻な探索が必要かもしれません。 そして、再び埋め込み次元を2倍にすればよい。

Frequency Scaled Regularization.
周波数スケールの正則化
In the experiments of Section 3, frequency scaled regularization was useful and ν = 1 worked the best.
セクション3の実験では、周波数スケールの正則化が有効であり、ν=1が最も効果的であった。
Interestingly, it becomes more important with larger embedding dimensions.
興味深いことに、埋め込み次元が大きくなると、より重要になる。
For example, even though the quality plateaued with ν = 0, with ν = 1 further increasing the embedding dimension gave additional improvements.
例えば、ν=0では品質が頭打ちになっても、ν=1では埋め込み次元をさらに大きくすることで、さらに向上する。

# References リファレンス

https:
httpsを使用しています。