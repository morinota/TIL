## link

- https://www.sciencedirect.com/science/article/pii/S1877050921019748 httpsを使用しています。

## title タイトル

How strongly do rank similarity coefficients differ used in decision making problems?
意思決定問題で使われる順位類似度係数はどの程度違うのか？

## Abstract Abstract

It is common practice in the MCDA to use several multi-criteria decision methods and then compares obtained rankings with one or two different rank correlation coefficients.
MCDAでは、複数の多基準決定法を用い、得られた順位を1〜2種類の順位相関係数で比較することが一般的である。
The problem is that different rank correlation coefficient gives different values for the same pair of rankings, and the number of studies which tries to investigate it is small.
しかし、順位相関係数が異なると、同じ順位の組でも異なる値を与えるという問題があり、これを検討しようとする研究は少ない。
Studying the similarity of rankings is a very important challenge in multi-criteria decision support, and the coefficients themselves seem to be the most practical ways of evaluating rankings.
順位の類似性を検討することは、多基準意思決定支援において非常に重要な課題であり、係数そのものが最も実用的な順位評価方法であると思われる。

This paper compares chosen rank correlation coefficients to show how much different they are.
この論文では、選ばれた順位相関係数を比較し、それらがどの程度異なるかを示している。
Spearman’s, Weighted Spearman’s, Kendall Tau and Rank similarity correlation coefficient are compared statistically.
スピアマンの相関係数、加重スピアマンの相関係数、ケンドールタウの相関係数、順位類似性の相関係数を統計的に比較した。
The paper confirms that the coefficients are closely related, and their dependence is graphically represented, which initiates research towards allows for their better selection in the future.
この論文では、これらの係数が密接に関連していることを確認し、それらの依存関係をグラフで表現し、将来、より良い選択を可能にするための研究を開始する。
In conclusions, directions of further development are indicated.
結論として、さらなる発展の方向性を示した。

# Introduction はじめに

People make many decisions every day and often even not pay much attention to them.
人は日々多くの決断を下し、多くの場合、その決断にあまり注意を払うこともない.
Nevertheless, sometimes the one can face complex decision problems, including too many variables and criteria for handling it by human, or a decision that could have severe consequences.
しかし，時には，あまりにも多くの変数とそれを人間が処理するための基準を含む複雑な意思決定問題や，深刻な結果をもたらす可能性のある意思決定に直面することがある.
It is necessary to make a reliable choice by analysing many opposing factors [16].
このような場合、多くの対立する要素を分析し、信頼できる選択をする必要がある[16].
In that case, **multi-criteria decision analysis(MCDA)**should be used, which is a useful branch of operational research.
このような場合、オペレーショナルリサーチの一分野である**multi-criteria decision analysis(MCDA)**を使用する必要がある.
The main MCDA advantages is fact that can help handle complex decision-making problems in everyday life, business [9, 17], medicine [6, 19], and more [23, 27].
MCDAの主な利点は、日常生活、ビジネス [9, 17]、医学 [6, 19]、その他 [23, 27] における複雑な意思決定問題の処理を助けることができるという事実である.
MCDA methods aim to support the decisionmaking process and lead the decision-maker to the right solution [26, 29].
MCDAの手法は、意思決定プロセスを支援し、意思決定者を正しい解決策に導くことを目的としている[26, 29].

In some cases, the researcher or the decision-maker apply several different MCDA methods and sometimes get identical or almost identical rankings.
研究者や意思決定者が複数の異なるMCDA手法を適用し、時には同一またはほぼ同一の順位が得られる場合もある.
However, the problem is that different MCDA methods often give different rankings for the same decision problem [25].
しかし、問題は、**異なるMCDA手法が同じ意思決定問題に対して異なるランキングを与えることが多いこと**である[25].
This fact is rather obvious because these methods using different paradigmatic.
この事実は、これらの方法が異なるパラダイムを使用しているため、むしろ明白である.
However, it is interesting how much similar these rankings are and how to differ these coefficients [31].
しかし，これらの順位がどの程度似ているか，また，これらの係数をどのように異ならせるかは興味深いところである[31].
For this purpose, we can use rank ranking similarity coefficients, which make it possible to determine how similar obtained rankings are.
このため、**ランキングの類似度係数を用いて、得られたランキングがどの程度類似しているかを判断することができる**.
For this purpose, many approaches can be used to determine the similarity of the rankings, e.g., Spearman’s rank correlation coefficient [21], Weighted Spearman’s rank correlation coefficient [5], Kendall Tau [1, 3, 7], Goodman’s and Kruskal’s Gamma [13], and the relatively new weighted similarity coefficient [24, 30].
このために，スピアマンの順位相関係数[21]，加重スピアマンの順位相関係数[5]，Kendall Tau [1，3，7]， Goodmanのガンマ，Kruskalのガンマ [13] や比較的新しい加重類似性係数 [24，30] など多くの手法が利用可能である.

Considering many available coefficients, we observed that a new problem is raised because it is hard to say which one should be used and how these coefficients differ.
しかし、**多くの相関係数がある中で、どの相関係数を使うべきか、どのような違いがあるのかがわかりにくいという新たな問題が生じている**.
Therefore, it is commonly observed that to check rankings similarity, use two or three different correlation coefficients [2, 8, 14, 15, 18, 22].
したがって、順位付けの類似性を確認するために、2つまたは3つの異なる相関係数を使用することが一般的に観察されている[2, 8, 14, 15, 18, 22].
This fact is the main motivation for undertaking work aimed at a practical comparison of selected coefficients measuring the similarity of the rankings.
この事実は、ランキングの類似性を測定するために選択された係数の実用的な比較を目的とした研究を行う主な動機となるものである.
There are few works dedicated to comparing rank correlation coefficients.
順位相関係数の比較に特化した研究はほとんどない.
Fieller et al. proposed tests and show how to compare Kendall’s and Spearman’s rank correlations with them [10, 11].
Fiellerらは検定を提案し、Kendallの順位相関とSpearmanの順位相関を比較する方法を示しています[10, 11].
Similarly to previous works, Chow et al. use a Monte-Carlo approach to compare Kendall’s Tau and Spearman’s Rho rank correlation coefficients [4].
以前の仕事と同様に、Chowらはモンテカルロ法を用いてKendallのTauとSpearmanのRhoの順位相関係数を比較しています[4].
Tarsitano in [28] examine the effectiveness of the several rank correlation measurements, including simple rank correlations, weighted rank correlation and the correlations of scores.
28]のTarsitanoは、単純順位相関、加重順位相関、スコアの相関など、いくつかの順位相関測定の有効性を検証している.

In this paper, we compare three commonly used rank correlation coefficients to examine how similar they are.
本論文では、一般的に使用されている3つの順位相関係数を比較し、それらがどの程度類似しているかを検討する.
Spearman’s, Weighted Spearman’s, Kendall Tau and weighted similarity coefficient are compared statistically.
**スピアマン係数、加重スピアマン係数、ケンドールタウ係数、加重類似度係数**が統計的に比較されている.
The research confirms that the coefficients are closely related, and their dependence is graphically represented and discussed.
この研究により、これらの係数は密接に関連していることが確認され、その依存関係がグラフで表現され、議論されている.
It is initial research towards for better selection of similar coefficients in the future.
これは、将来、類似係数をより良く選択するための初期研究である.
In conclusions, directions of further development are indicated.
結論として、さらなる発展の方向性が示された.

The rest of paper is structured as follows: in the Section 2 four selected correlation coefficients are described, Section 3 describes the run of the experiment, results and discussion are presented in the Section 4, and the Section 5 conclude the paper and shows some possible future directions.
第2節では4つの相関係数について述べ、第3節では実験の実行について、第4節では結果と考察を述べ、第5節では論文の結論と今後の方向性について述べる.

# Preliminaries プレリミナリー

## Spearman’s rank correlation coefficient スピアマンの順位相関係数

Spearman’s rank correlation is defined for the rank values $rg_{X}$ and $rg_{Y}$, as it showed in Equation (1).
スピアマンの順位相関は、式(1)に示すように、順位値 $rg_{X}$ と $rg_{Y}$ に対して定義されている.
To calculate co-variance cov() and standard deviation σ one should use Equations (2) and (3).
共分散 cov() と標準偏差 σ を計算するには、式(2) と式(3)を使用する必要がある.
When both rankings does not contain ties Spearman’s correlation could be calculated with (4) [20].
両者の順位が同値でない場合(ランクの長さの話...??)、スピアマンの相関は(4)で計算できる[20].

$$
r_s = \frac{cov(rg_{X}, rg_{Y})}{\sigma_{rg_{X}}}
\tag{1}
$$

$$
\tag{2}
$$

$$
\tag{3}
$$

$$
r_s = 1 - \frac{6 \cdot \sum_{i=1}^{N}(x_i - \bar{x})(y_i - \bar{y})}{N(N^2 - 1)}
\tag{4}
$$

## Weighted Spearman’s rank correlation coefficient 重み付きスピアマンの順位相関係数

For the sample of size N of the rank values xi and yi Weighted Spearman’s correlation is defined as (5).
順位値$x_i$と$y_i$の大きさNのサンプルに対して、加重スピアマンの相関は(5)のように定義される.
The main difference to the Spearman’s rank correlation is that Weighted Spearman’s coefficient examines whether the differences appeared and at which positions they appeared.
Spearmanの順位相関との主な違いは、Weighted Spearmanの係数は、差が現れたかどうか、どの位置で現れたかを調べることである.
Therefore, differences at the top of both rankings influenced correlation values more [5, 12].
したがって、**両順位の上位にある差は、より相関値に影響を与える**[5, 12].

$$
r_w = 1 - \frac{6 \cdot \sum_{i=1}^{N} (x_i - y_i)^2((N - x_i +1)(N - y_i + 1))}{N^4 + N^3 - N^2 -N}
\tag{5}
$$

## Rank similarity coefficient WS 順位類似度係数 WS

For a samples of size N, the rank values xi and yi is defined as (6) [24].
サイズNのサンプルに対して、ランク値$x_i$と$y_i$は(6)のように定義される[24].
It is an asymmetric measure.
これは非対称な尺度である.
The weight of a given comparison is determined based on the significance of the position in the first ranking, which is used as a reference ranking during the calculation.
与えられた比較の重みは、計算中に参照順位として使用される最初の順位における位置の重要性に基づいて決定される.

$$
WS = 1 -
\tag{6}
$$

## Kendall’s Tau ケンドールのタウ

Kendall’s Tau is a measure of similarity degree between two sets of rankings [1].
ケンドールのタウは、2組の順位間の類似度を表す尺度である[1]。
This correlation coefficient depends on how many pairs of rank positions should be inverted to change one ranking into the other.
この相関係数は、**あるランキングを他のランキングに変更するために、何組のランキングの位置を反転させればよいか**に依存する.
The Kendall’s Tau correlation is defined as (7).
ケンドールのタウの相関は(7)のように定義される.

$$
\tau = 2 \frac{P - Q}{N(N-1)}
\tag{7}
$$

where P is number of concordant pairs and Q is a number of discordant pairs.
ここで、Pは一致するペアの数、Qは不一致のペアの数である.
In other words, P means number of pairs (xi, yi) and (xj, yj), where i < j in both rankings if both xi > xj and yi > yj, and Q means number of pairs with both xi < xj and yi < yj conditions fulfilled.
すなわち、Pは、（xi，yi）と（xj，yj）の組のうち、xi＞xjとyi＞yjの両方の条件を満たす場合に、両方のランキングでi＜jとなる組の数を意味し、Qは、xi＜xjとyi＜yjの両方の条件を満たす組の数を意味している。

# Study case 研究事例

To show how different rank correlation coefficients are, we generate all possible permutations rankings with eight alternatives and calculate four chosen correlation measurements between reference ranking 1, 2,..., 8 and each of 8! = 40320 permutation.
順位相関係数がどのように異なるかを示すために、8つの選択肢を持つすべての可能な順列ランキングを生成し、参照順位1、2、...、8と8！=40320の順列のそれぞれの間の4つの選ばれた相関測定値を計算します。
This number of positions in the ranking was chosen because choosing the larger number of elements in ranking does not bring any significant information in the results.
ランキングの要素の数が多くなると、結果に有意な情報をもたらさないため、この数を選択しました。
As shown in Figure 1, correlations start to overlap, so rankings with only eight elements allow us to approximate results for larger and smaller sets of rankings.
図1に示すように、相関は重なり始めるので、8つの要素だけのランキングで、より大きなランキングのセットとより小さなランキングのセットの結果を近似的に得ることができます。
There should be noted that in this case, the rankings do not contain ties.
なお、この場合、順位に同点が含まれないことに注意する必要がある。

# Results 結果

After calculating Spearman’s, Weighted Spearman’s, Rank similarity and Kendall Tau rank correlation coefficients between reference ranking and 40320 permutations of this ranking, we calculated Pearson correlation between obtained vectors of correlations.
基準順位とこの順列の40320通りの並べ替えとの間のスピアマン相関、加重スピアマン相関、順位類似度、ケンドールタウ順位相関係数を計算した後、得られた相関のベクトル間のピアソン相関を算出した.
Table 1 contains Pearson correlations calculated for each pair of obtained rank correlations.
表1に、得られた順位相関の各組について計算したピアソン相関を示す.
Values of Spearman’s and Weighted Spearman’s coefficients are correlated most (r = 0.9879).
Spearmanの係数とWeighted Spearmanの係数の値が最も相関が高い(r = 0.9879).
It can be seen that values calculated with Spearman’s and Kendall Tau coefficient are slightly less correlated (r = 0.9820) in comparison to the correlation between Spearman’s and Weighted Spearman’s coefficients.
Spearmanの係数とKendall Tauの係数で計算した値は、Spearmanの係数とWeighted Spearmanの係数の相関と比較して、若干相関が低いことがわかる(r = 0.9820).
The two most minor correlated coefficients are Rank similarity coefficient and Kendall Tau.
最も相関の小さい係数は、順位類似度係数とケンドールタウである.
Pearson correlations for them is only r = 0.7912.
これらのピアソン相関は、r = 0.7912に過ぎない.

Figure 2 presented a visual comparison between Spearman’s and Weighted Spearman’s, and Weighted Spearman’s and Rank similarity (right) correlation coefficients.
図2は、スピアマンの相関係数と加重スピアマンの相関係数、加重スピアマンの相関係数と順位類似度（右）の比較を視覚的に示したものである。
Each dot on the plot represents one ranking, and the dot’s position on the axes shows a value of a corresponding correlation coefficient.
プロット上の各ドットは1つのランキングを表し、軸上のドットの位置は対応する相関係数の値を示している。
On the right and top sides of each plot, histograms of correlation coefficients are shown.
各プロットの右側と上側には、相関係数のヒストグラムが表示されている。
Analysing histograms, we could see that there are fewer rankings that get values near the edges of the range (e.g. strongly correlated) than rankings that are uncorrelated and therefore get correlation values in the middle of the range.
ヒストグラムを分析すると、相関がないために相関値が範囲の中央にあるランキングよりも、範囲の端に近い値を得るランキング（例えば、強い相関がある）の方が少ないことがわかります。

On the left plot in Figure 2 we could also see how much presented rank correlation coefficients are different.
図2左のプロットでは、提示された順位相関係数がどの程度異なるかも見ることができた。
In the case of Spearman’s and Weighted Spearman’s correlation coefficient, the ”cloud” of points is dense, which confirms high correlations between these coefficients.
スピアマンの相関係数と加重スピアマンの相関係数の場合、点の「雲」が密集しており、これらの相関係数の相関が高いことが確認された。
Plot on right side of Figure 2 shows the distributions and correlation between Weighted Spearman’s and Rank similarity coefficients.
図2右側のプロットは、重み付きスピアマン相関係数とランク相関係数の分布と相関を示したものである。
The ”cloud” of point has a very interesting shape since Rank similarity coefficient is asymmetric.
ランク類似度係数は非対称であるため、点の「雲」は非常に興味深い形をしている。
We could see that it reaches its minimum value (≈ 0.15) when Weighted Spearman’s correlation is ≈ −0.5.
加重スピアマンの相関が≈-0.5のときに、最小値(≈0.15)に達していることがわかる。
Despite that, on the other side of the points cloud, these two correlation coefficients are more consistent between themselves.
それにもかかわらず、ポイントクラウドの反対側では、これらの2つの相関係数は、それ自身の間でより一貫しています。

In Figure 3 next two plots are presented.
図3では、次の2つのプロットを示している。
It shows a visual comparison between Weighted Spearman’s and Kendall Tau on the left side of the figure and Rank similarity and Kendall Tau on the right side of the figure.
これは、図の左側がWeighted SpearmanとKendall Tau、右側がRank similarityとKendall Tauを視覚的に比較したものである。
We decide to omit the visual comparison between Spearman’s and Rank similarity and Kendall Tau correlation because it turned out that the results are very similar to Weighted Spearman’s results.
SpearmanとRankの類似度とKendall Tauの相関の視覚的比較は、Weighted Spearmanの結果と非常に似ていることが判明したため、省略することにした。

Analysing plots in the Figure 3 it could be noticed that values of Kendall Tau correlation are discrete, and there are empty lines in the points cloud.
図3のプロットを分析すると、Kendall Tau相関の値が不連続であり、点群に空白の線があることに気づくだろう。
This is due to how this correlation is calculated.
これは、この相関の計算方法によるものである。
As it is shown in Equation (7), Kendall Tau correlation is based on a count of concordant and discordant pairs, which is discrete and not continuous values for a given size of the ranking.
式(7)に示すように、Kendall Tau相関は、一致するペアと不一致するペアのカウントに基づいており、これは、ランキングのサイズが与えられた場合に連続値ではなく、離散的な値です。
The further analysis of plots shows that Weighted Spearman’s and Kendall Tau correlations have similar values.
プロットをさらに分析すると、重み付きスピアマンの相関とケンドールタウの相関は似たような値を持っていることがわかる。
However, the cloud of dots is not so dense as it was when Spearman’s and Weighted Spearman’s correlations were compared.
しかし、Spearmanの相関とWeighted Spearmanの相関を比較したときのように、点の雲はそれほど密ではありません。
The plot on the right side of the figure shows the comparison of Rank similarity and Kendall Tau correlation coefficients.
図の右側のプロットは、ランク類似度とケンドールタウ相関係数を比較したものである。
The shape of the dot’s cloud is quite similar to the comparing Rank similarity and Weighted Spearman’s correlations.
点群の形状は、Rank類似度相関とWeighted Spearman相関の比較とよく似ている。
It noticeable that Rank similarity coefficient reaches its minimum value (≈ 0.15) when Kendall Tau is only (≈ −0.25), which is due to the asymmetric nature of this coefficient.
Kendall Tauが(≈-0.25)のとき、Rank類似度係数は最小値(≈0.15)になっていることがわかるが、これはこの係数の非対称性によるものである。

The next interesting visualisation that could be done for these data is a graph showing the dependence of the range of one correlation coefficient’s values on other correlation coefficient values.
これらのデータに対して、次に興味深い視覚化を行うことができるのは、ある相関係数の値の範囲の他の相関係数の値への依存性を示すグラフである。
The plots presented in Figures 4 - 9 are provide this type of visualisation.
Figure 4 - 9に示したプロットは、このタイプの視覚化です。
It is expected that most pairs of compared correlation coefficient would be more consistent on the edges of their respected ranges (near −1 and 1, 0 and 1).
比較された相関係数のほとんどのペアは、その尊重された範囲の端（-1と1、0と1付近）でより一貫していることが予想されます。
This assumption turns wrong for Rank correlation coefficients since it is asymmetric and deviates strongly from other correlations when rankings are not perfectly correlated.
しかし、順位相関係数は非対称であり、順位が完全に相関していない場合、他の相関関係から強く逸脱するため、この仮定は間違いであることがわかります。

Some pairs of compared correlation coefficients result in a pretty interesting graph’s shape.
相関係数を比較すると、かなり面白いグラフの形になる組もあります。
For example, comparing Kendall Tau ranges with Spearman’s and Weighted Spearman’s correlations makes steps of Kendall’s Tau discrete values clearly visible.
例えば、Kendall Tauの範囲をSpearmanの相関とWeighted Spearmanの相関と比較すると、KendallのTauの離散値のステップがはっきりと見えるようになります。
It is also interesting that when comparing ranges of other correlation coefficients to Rank similarity coefficients, the plot turns out to be filled.
また、他の相関係数の範囲をRankの類似性係数と比較すると、プロットが塗りつぶされることが判明するのも興味深い点です。
It means that for some values of Rank similarity coefficient, there are no corresponding values of other correlations coefficients.
これは、あるRank類似度係数の値に対して、対応する他の相関係数の値が存在しないことを意味します。
Therefore, the range of these values is zero, which makes the graph look filled inside.
したがって、これらの値の範囲はゼロとなり、グラフは内側が塗りつぶされたようになります。

We also calculate some statistic metrics, which could help compare correlation coefficients at some point.
また、相関係数の比較に役立つような統計的な指標をいくつか計算した。
Table 2 contains mean value, standard deviation and variance for four examined correlation coefficients.
表2は、調査した4つの相関係数の平均値、標準偏差、分散を含んでいる。
Due to the symmetric distribution of Spearman’s, Weighted Spearman’s and Kendall Tau coefficients, it is expected that the mean value would lay in the centre of range for these coefficients.
Spearmanの係数、Weighted Spearmanの係数、Kendall Tauの係数は対称的な分布をしているので、これらの係数の平均値は範囲の中央に位置することが予想されます。
On the other hand, the mean value for Rank similarity coefficient is 0.5197.
一方、ランク類似度係数の平均値は0.5197であった。
It could be explained with the asymmetric nature of this correlation coefficient and that it takes values from (0, 1] range.
これは、この相関係数が非対称的な性質を持ち、(0, 1)の範囲から値を取ることから説明できる。
Therefore, it could be expected that mean values lie near the centre of the range but slightly shifted to 1. It is also interesting that Rank similarity coefficient has a smaller standard deviation and variance across other correlation coefficients.
また、Rank類似度係数は、他の相関係数に比べて標準偏差と分散が小さいことも興味深い点である.
According to [28] it makes it performs better than coefficients with higher variance and standard deviation.
28]によれば、分散や標準偏差が大きい係数よりも性能が良いということになる.

# Conclusions 結論

In this paper, we present some comparisons which could be helpful when deciding which correlation coefficients should be used.
この論文では、どの相関係数を使用すべきかを決定する際に有用と思われるいくつかの比較を示す.
It turns out that a Rank correlation coefficient differs significantly from other popular rank correlation coefficients due to its unusual range and asymmetric nature.
ランク相関係数は、その特異な範囲と非対称性により、他の一般的なランク相関係数と大きく異なることがわかった.
Another interesting observation is that Rank correlation coefficient values are denser in the range, which may be due to half less range than other correlation coefficients.
また、Rank相関係数の値が範囲内で密になっているのも興味深い観察結果で、これは他の相関係数に比べて範囲が半分ほど狭いことが原因かもしれない.
Other tested correlation coefficients perform very similarly, except Kendall Tau correlation coefficients which values are discrete since it based on counting pair in rankings.
他の相関係数もほぼ同じような結果が得られていますが、Kendall Tau相関係数はランキングのペアをカウントしているため、値が不連続になっている.
There is no unambiguous answer which correlation coefficients is better and which one should be used.
どの相関係数が優れていて、どの相関係数を使うべきかという明確な答えはありません。

Therefore, there are some directions which could be investigated in the future studies:
したがって、今後の研究で検討されるべき方向性がいくつかある。

- applying tests from [10, 11] to Rank similarity and other rank correlation coefficients; ランク類似度や他のランク相関係数に[10, 11]のテストを適用。

- extending number of compared correlation coefficients; 比較した相関係数の数を拡張する。

- examining correlations coefficients from a statistical point of view. 統計的な観点から相関係数の検証を行う。
