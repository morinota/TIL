## link

- https://www.sciencedirect.com/science/article/pii/S1877050921019748

## title

How strongly do rank similarity coefficients differ used in decision making problems?

## Abstract

It is common practice in the MCDA to use several multi-criteria decision methods and then compares obtained rankings with one or two different rank correlation coefficients. The problem is that different rank correlation coefficient gives different values for the same pair of rankings, and the number of studies which tries to investigate it is small. Studying the similarity of rankings is a very important challenge in multi-criteria decision support, and the coefficients themselves seem to be the most practical ways of evaluating rankings.

This paper compares chosen rank correlation coefficients to show how much different they are. Spearman’s, Weighted Spearman’s, Kendall Tau and Rank similarity correlation coefficient are compared statistically. The paper confirms that the coefficients are closely related, and their dependence is graphically represented, which initiates research towards allows for their better selection in the future. In conclusions, directions of further development are indicated.

# Introduction

People make many decisions every day and often even not pay much attention to them. Nevertheless, sometimes the one can face complex decision problems, including too many variables and criteria for handling it by human, or a decision that could have severe consequences. It is necessary to make a reliable choice by analysing many opposing factors [16]. In that case, multi-criteria decision analysis (MCDA) should be used, which is a useful branch of operational research. The main MCDA advantages is fact that can help handle complex decision-making problems in everyday life, business [9, 17], medicine [6, 19], and more [23, 27]. MCDA methods aim to support the decisionmaking process and lead the decision-maker to the right solution [26, 29].

In some cases, the researcher or the decision-maker apply several different MCDA methods and sometimes get identical or almost identical rankings. However, the problem is that different MCDA methods often give different rankings for the same decision problem [25]. This fact is rather obvious because these methods using different paradigmatic. However, it is interesting how much similar these rankings are and how to differ these coefficients [31]. For this purpose, we can use rank ranking similarity coefficients, which make it possible to determine how similar obtained rankings are. For this purpose, many approaches can be used to determine the similarity of the rankings, e.g., Spearman’s rank correlation coefficient [21], Weighted Spearman’s rank correlation coefficient [5], Kendall Tau [1, 3, 7], Goodman’s and Kruskal’s Gamma [13], and the relatively new weighted similarity coefficient [24, 30].

Considering many available coefficients, we observed that a new problem is raised because it is hard to say which one should be used and how these coefficients differ. Therefore, it is commonly observed that to check rankings similarity, use two or three different correlation coefficients [2, 8, 14, 15, 18, 22]. This fact is the main motivation for undertaking work aimed at a practical comparison of selected coefficients measuring the similarity of the rankings. There are few works dedicated to comparing rank correlation coefficients. Fieller et al. proposed tests and show how to compare Kendall’s and Spearman’s rank correlations with them [10, 11]. Similarly to previous works, Chow et al. use a Monte-Carlo approach to compare Kendall’s Tau and Spearman’s Rho rank correlation coefficients [4]. Tarsitano in [28] examine the effectiveness of the several rank correlation measurements, including simple rank correlations, weighted rank correlation and the correlations of scores.

In this paper, we compare three commonly used rank correlation coefficients to examine how similar they are. Spearman’s, Weighted Spearman’s, Kendall Tau and weighted similarity coefficient are compared statistically. The research confirms that the coefficients are closely related, and their dependence is graphically represented and discussed. It is initial research towards for better selection of similar coefficients in the future. In conclusions, directions of further development are indicated.

The rest of paper is structured as follows: in the Section 2 four selected correlation coefficients are described, Section 3 describes the run of the experiment, results and discussion are presented in the Section 4, and the Section 5 conclude the paper and shows some possible future directions.

# Preliminaries

## Spearman’s rank correlation coefficient

Spearman’s rank correlation is defined for the rank values rgX and rgY , as it showed in Equation (1). To calculate co-variance cov() and standard deviation σ one should use Equations (2) and (3). When both rankings does not contain ties Spearman’s correlation could be calculated with (4) [20].

$$
\tag{1}
$$

$$
\tag{2}
$$

$$
\tag{3}
$$

$$
\tag{4}
$$

## Weighted Spearman’s rank correlation coefficient

For the sample of size N of the rank values xi and yi Weighted Spearman’s correlation is defined as (5). The main difference to the Spearman’s rank correlation is that Weighted Spearman’s coefficient examines whether the differences appeared and at which positions they appeared. Therefore, differences at the top of both rankings influenced correlation values more [5, 12].

$$
\tag{5}
$$

## Rank similarity coefficient WS

For a samples of size N, the rank values xi and yi is defined as (6) [24]. It is an asymmetric measure. The weight of a given comparison is determined based on the significance of the position in the first ranking, which is used as a reference ranking during the calculation.

$$
\tag{6}
$$

## Kendall’s Tau

Kendall’s Tau is a measure of similarity degree between two sets of rankings [1]. This correlation coefficient depends on how many pairs of rank positions should be inverted to change one ranking into the other. The Kendall’s Tau correlation is defined as (7).

$$
\tag{7}
$$

where P is number of concordant pairs and Q is a number of discordant pairs. In other words, P means number of pairs (xi, yi) and (xj, yj), where i < j in both rankings if both xi > xj and yi > yj, and Q means number of pairs with both xi < xj and yi < yj conditions fulfilled.

# Study case

To show how different rank correlation coefficients are, we generate all possible permutations rankings with eight alternatives and calculate four chosen correlation measurements between reference ranking 1, 2,..., 8 and each of 8! = 40320 permutation. This number of positions in the ranking was chosen because choosing the larger number of elements in ranking does not bring any significant information in the results. As shown in Figure 1, correlations start to overlap, so rankings with only eight elements allow us to approximate results for larger and smaller sets of rankings. There should be noted that in this case, the rankings do not contain ties.

# Results

After calculating Spearman’s, Weighted Spearman’s, Rank similarity and Kendall Tau rank correlation coefficients between reference ranking and 40320 permutations of this ranking, we calculated Pearson correlation between obtained vectors of correlations. Table 1 contains Pearson correlations calculated for each pair of obtained rank correlations. Values of Spearman’s and Weighted Spearman’s coefficients are correlated most (r = 0.9879). It can be seen that values calculated with Spearman’s and Kendall Tau coefficient are slightly less correlated (r = 0.9820) in comparison to the correlation between Spearman’s and Weighted Spearman’s coefficients. The two most minor correlated coefficients are Rank similarity coefficient and Kendall Tau. Pearson correlations for them is only r = 0.7912.

Figure 2 presented a visual comparison between Spearman’s and Weighted Spearman’s, and Weighted Spearman’s and Rank similarity (right) correlation coefficients. Each dot on the plot represents one ranking, and the dot’s position on the axes shows a value of a corresponding correlation coefficient. On the right and top sides of each plot, histograms of correlation coefficients are shown. Analysing histograms, we could see that there are fewer rankings that get values near the edges of the range (e.g. strongly correlated) than rankings that are uncorrelated and therefore get correlation values in the middle of the range.

On the left plot in Figure 2 we could also see how much presented rank correlation coefficients are different. In the case of Spearman’s and Weighted Spearman’s correlation coefficient, the ”cloud” of points is dense, which confirms high correlations between these coefficients. Plot on right side of Figure 2 shows the distributions and correlation between Weighted Spearman’s and Rank similarity coefficients. The ”cloud” of point has a very interesting shape since Rank similarity coefficient is asymmetric. We could see that it reaches its minimum value (≈ 0.15) when Weighted Spearman’s correlation is ≈ −0.5. Despite that, on the other side of the points cloud, these two correlation coefficients are more consistent between themselves.

In Figure 3 next two plots are presented. It shows a visual comparison between Weighted Spearman’s and Kendall Tau on the left side of the figure and Rank similarity and Kendall Tau on the right side of the figure. We decide to omit the visual comparison between Spearman’s and Rank similarity and Kendall Tau correlation because it turned out that the results are very similar to Weighted Spearman’s results.

Analysing plots in the Figure 3 it could be noticed that values of Kendall Tau correlation are discrete, and there are empty lines in the points cloud. This is due to how this correlation is calculated. As it is shown in Equation (7), Kendall Tau correlation is based on a count of concordant and discordant pairs, which is discrete and not continuous values for a given size of the ranking. The further analysis of plots shows that Weighted Spearman’s and Kendall Tau correlations have similar values. However, the cloud of dots is not so dense as it was when Spearman’s and Weighted Spearman’s correlations were compared. The plot on the right side of the figure shows the comparison of Rank similarity and Kendall Tau correlation coefficients. The shape of the dot’s cloud is quite similar to the comparing Rank similarity and Weighted Spearman’s correlations. It noticeable that Rank similarity coefficient reaches its minimum value (≈ 0.15) when Kendall Tau is only (≈ −0.25), which is due to the asymmetric nature of this coefficient.

The next interesting visualisation that could be done for these data is a graph showing the dependence of the range of one correlation coefficient’s values on other correlation coefficient values. The plots presented in Figures 4 - 9 are provide this type of visualisation. It is expected that most pairs of compared correlation coefficient would be more consistent on the edges of their respected ranges (near −1 and 1, 0 and 1). This assumption turns wrong for Rank correlation coefficients since it is asymmetric and deviates strongly from other correlations when rankings are not perfectly correlated.

Some pairs of compared correlation coefficients result in a pretty interesting graph’s shape. For example, comparing Kendall Tau ranges with Spearman’s and Weighted Spearman’s correlations makes steps of Kendall’s Tau discrete values clearly visible. It is also interesting that when comparing ranges of other correlation coefficients to Rank similarity coefficients, the plot turns out to be filled. It means that for some values of Rank similarity coefficient, there are no corresponding values of other correlations coefficients. Therefore, the range of these values is zero, which makes the graph look filled inside.

We also calculate some statistic metrics, which could help compare correlation coefficients at some point. Table 2 contains mean value, standard deviation and variance for four examined correlation coefficients. Due to the symmetric distribution of Spearman’s, Weighted Spearman’s and Kendall Tau coefficients, it is expected that the mean value would lay in the centre of range for these coefficients. On the other hand, the mean value for Rank similarity coefficient is 0.5197. It could be explained with the asymmetric nature of this correlation coefficient and that it takes values from (0, 1] range. Therefore, it could be expected that mean values lie near the centre of the range but slightly shifted to 1. It is also interesting that Rank similarity coefficient has a smaller standard deviation and variance across other correlation coefficients. According to [28] it makes it performs better than coefficients with higher variance and standard deviation.

# Conclusions

In this paper, we present some comparisons which could be helpful when deciding which correlation coefficients should be used. It turns out that a Rank correlation coefficient differs significantly from other popular rank correlation coefficients due to its unusual range and asymmetric nature. Another interesting observation is that Rank correlation coefficient values are denser in the range, which may be due to half less range than other correlation coefficients. Other tested correlation coefficients perform very similarly, except Kendall Tau correlation coefficients which values are discrete since it based on counting pair in rankings. There is no unambiguous answer which correlation coefficients is better and which one should be used.

Therefore, there are some directions which could be investigated in the future studies:

- applying tests from [10, 11] to Rank similarity and other rank correlation coefficients;
- extending number of compared correlation coefficients;
- examining correlations coefficients from a statistical point of view.
