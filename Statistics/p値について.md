# 参考

- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4877414/

# Abstract

- Misinterpretation and abuse of statistical tests, confidence intervals, and statistical power have been decried for decades, yet remain rampant.
  - 統計的検定、信頼区間、検出力の誤った解釈や乱用は何十年も前から指摘されていますが、いまだに後を絶ちません。
- A key problem is that there are no interpretations of these concepts that are at once simple, intuitive, correct, and foolproof.
  - 重要な問題は、これらの概念について、単純で、直感的で、正しく、間違いのない解釈が存在しないことである。
- Instead, correct use and interpretation of these statistics requires an attention to detail which seems to tax the patience of working scientists.
  - むしろ、これらの統計を正しく利用し、解釈するためには、細部にまで注意を払う必要があり、現役の科学者の忍耐力を奪っているように思われる。
- This high cognitive demand has led to an epidemic of shortcut definitions and interpretations that are simply wrong, sometimes disastrously so—and yet these misinterpretations dominate much of the scientific literature.
  - このように認知的な要求が高いため、近道となる定義や解釈は単に間違っており、時には悲惨なほど間違っているにもかかわらず、これらの間違った解釈が科学文献の多くを占めているのである。
- In light of this problem, we provide definitions and a discussion of basic statistics that are more general and critical than typically found in traditional introductory expositions.
- このような問題を踏まえ、本書では、従来の入門書よりも一般的かつ批判的に基礎統計学の定義と考察を提供する。
- Our goal is to provide a resource for instructors, researchers, and consumers of statistics whose knowledge of statistical theory and technique may be limited but who wish to avoid and spot misinterpretations.
  - 本書の目的は、統計学の理論や技法に関する知識が乏しいが、誤解を避けたい、見抜きたいと考えている教員、研究者、統計学の利用者にリソースを提供することである。
- We emphasize how violation of often unstated analysis protocols (such as selecting analyses for presentation based on the P values they produce) can lead to small P values even if the declared test hypothesis is correct, and can lead to large P values even if that hypothesis is incorrect.
  - 私たちは、しばしば明文化されていない解析プロトコルの違反（例えば、生成されるP値に基づいて解析結果を選択すること）が、宣言された検定仮説が正しくてもP値が小さくなり、その仮説が間違っていてもP値が大きくなる可能性があることを強調します。
- We then provide an explanatory list of 25 misinterpretations of P values, confidence intervals, and power.
  - 次に、P値、信頼区間、検出力に関する25の誤った解釈について説明します。
- We conclude with guidelines for improving statistical interpretation and reporting.
  - 最後に、統計的解釈と報告を改善するためのガイドラインを示す。

# Introduction

## 統計的検定の禁止令

- 統計的検定の誤った解釈や乱用は何十年も前から批判されてきましたが、いまだに横行しているため、一部の科学雑誌では「統計的有意性」（P値に基づいて結果を「有意」かどうかに分類すること）の使用を控えています[1]。
- ある雑誌では、統計的検定や信頼区間のような数学的に関連する手続きをすべて禁止しており [2]、そのような禁止のメリットについてかなりの議論と討論が行われています [3、4]。

## しかし禁止令にも関わらず...なので本研究では...

- しかし、このような禁止令が出されているにもかかわらず、今回問題となった統計手法は今後何年にもわたって使用されることが予想される。
- そのため、これらの統計手法の基本的な教え方と一般的な理解を深めることが急務であると考える。
  - そのために、**有意性検定、信頼区間、統計的検出力の意味を従来よりも一般的かつ批判的に**説明し、**よくある25の誤解**を我々の説明に照らし合わせて検討することを試みる。
  - また、より微妙ではあるが、それでも蔓延しているいくつかの問題について、**個々の結果に注目するのではなく、科学的な疑問に関連するすべての結果を検討し、統合することが重要である**理由を説明する。
  - さらに、**統計的検定が、関連性や効果に関する推論や判断の唯一の材料となるべきでない**理由も説明する。
- 多くの理由の中で、ほとんどの科学的環境において、**結果を「有意」と「非有意」に任意に分類すること**は、
  - **データの有効な解釈にとって不必要**であり、
  - **しばしば有害**である。
- そして効果の大きさと推定値の不確実性を推定することは、そのような分類(=有意 or 非有意)よりも科学的推測と健全な判断にとってはるかに重要であることを説明する。

# Statistical tests, P values, and confidence intervals: a caustic primer

## Statistical models, hypotheses, and tests

### 仮定(前提)を満たす事が困難な話
- 統計的推測のあらゆる手法は、データの収集と分析の方法、分析結果の提示のための選択方法に関する複雑な前提の網に依存している。
  - この仮定は、その手法を支える統計モデルとして具現化されます。

### モデルの範囲を定義する事の問題点

### 仮定を理解し評価することの難しさ

### 

## Uncertainty, probability, and statistical significance

## Moving from tests to estimates

# What P values, confidence intervals, and power calculations don’t tell us

## Common misinterpretations of single P values

- ThePvalue is the probability that the test hypothesis is true; for example, if a test of the null hypothesis gaveP = 0.01, the null hypothesis has only a 1 % chance of being true; if instead it gaveP = 0.40, the null hypothesis has a 40 % chance of being true.

- ThePvalue for the null hypothesis is the probability that chance alone produced the observed association; for example, if thePvalue for the null hypothesis is 0.08, there is an 8 % probability that chance alone produced the association.

- A significant test result (P ≤ 0.05) means that the test hypothesis is false or should be rejected.

- A nonsignificant test result (P > 0.05) means that the test hypothesis is true or should be accepted.

- A largePvalue is evidence in favor of the test hypothesis.

- A null-hypothesisPvalue greater than 0.05 means that no effect was observed, or that absence of an effect was shown or demonstrated.

- Statistical significance indicates a scientifically or substantively important relation has been detected.

- Lack of statistical significance indicates that the effect size is small.

- ThePvalue is the chance of our data occurring if the test hypothesis is true; for example,P = 0.05 means that the observed association would occur only 5 % of the time under the test hypothesis.

- If you reject the test hypothesis becauseP ≤ 0.05, the chance you are in error (the chance your “significant finding” is a false positive) is 5 %.

- P = 0.05 andP ≤ 0.05 mean the same thing.

- Pvalues are properly reported as inequalities (e.g., report “P < 0.02” whenP = 0.015 or report “P > 0.05” whenP = 0.06 orP = 0.70).

- Statistical significance is a property of the phenomenon being studied, and thus statistical tests detect significance.

- One should always use two-sidedPvalues.

## Common misinterpretations of P value comparisons and predictions

- When the same hypothesis is tested in different studies and none or a minority of the tests are statistically significant (allP > 0.05), the overall evidence supports the hypothesis.

- When the same hypothesis is tested in two different populations and the resultingPvalues are on opposite sides of 0.05, the results are conflicting.

- When the same hypothesis is tested in two different populations and the samePvalues are obtained, the results are in agreement.

- If one observes a smallPvalue, there is a good chance that the next study will produce aPvalue at least as small for the same hypothesis.

- The specific 95 % confidence interval presented by a study has a 95 % chance of containing the true effect size.

- An effect size outside the 95 % confidence interval has been refuted (or excluded) by the data.

- If two confidence intervals overlap, the difference between two estimates or studies is not significant.
-
- An observed 95 % confidence interval predicts that 95 % of the estimates from future studies will fall inside the observed interval.
- If one 95 % confidence interval includes the null value and another excludes that value, the interval excluding the null is the more precise one.

## Common misinterpretations of power

- If you accept the null hypothesis because the nullPvalue exceeds 0.05 and the power of your test is 90 %, the chance you are in error (the chance that your finding is a false negative) is 10 %.
- If the nullPvalue exceeds 0.05 and the power of this test is 90 % at an alternative, the results support the null over the alternative.

# A statistical model is much more than an equation with Greek letters

# Conclusions
