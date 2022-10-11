## link

- https://geographicdata.science/book/notebooks/11_regression.html

# Spatial Regression

回帰（そしてより一般的な予測）は、空間構造がどのように我々のデータの理解と分析に役立つかを調べるための完璧なケースを提供する。
この章では、特に線形回帰に焦点を当て、予測アルゴリズムの検証と改善のために空間構造をどのように利用できるかを議論する。

# What is spatial regression and why should I care?

- 通常、空間構造は回帰モデルに2つの方法で影響を与えます。

## 空間構造が回帰モデルに与える影響1⃣

- まず（そして最も明確な）空間がデータに影響を与える方法は、**データを生成するプロセス自体が明示的に空間的である場合**です。
  - ここでは、一戸建ての家の値段のようなものを考えてみましょう。
  - 同じ品質の家でも、より良い学区に住むために、個人が家の値段にプレミアムを支払うことはよくあることです。
  - また、排水処理施設やリサイクル施設、広い高速道路など、騒音や化学物質の汚染源に近い住宅は、実は私たちが予想するよりも安いかもしれません。喘息などの場合、職場や娯楽施設など、一日のうちで移動することの多い場所が、住所以上に健康に影響を与えることがある。
  - この場合、ある場所の喘息発症率を予測するために、他の場所のデータを使用する必要がある場合があります。
  - 具体的にどのようなケースであろうと、ここでは、**地理は特徴である。地理的なプロセスから結果が得られるので、結果についての予測をするのに直接役立つ**のである。

## 空間構造が回帰モデルに与える影響

- もう一つの方法（より懐疑的な理解）は、地理学の道具的価値をしぶしぶ認めるものである。
  - 予測手法や分類法の分析では、しばしば、何が間違っているのかを分析することに関心がある。
  - これは計量経済学でよくあることで、分析者はモデルがある種のオブザベーションを系統的に間違って予測することを懸念することがあります。
  - もし我々のモデルが、既知のオブザベーションの集合や入力のタイプに対して、日常的に悪いパフォーマンスをすることがわかっているなら、これを説明できれば、我々はより良いモデルを作ることができるかもしれない。
  - 他の種類の誤差診断の中で、**地理は誤差の構造を評価するのに非常に有用な埋め込みを提供してくれる**。
  - 分類・予測エラーをマッピングすることで、データの中にエラーのクラスターがあるかどうかを示すことができます。
  - もし、**ある地域では他の地域よりも誤差が大きくなる傾向がある**ことがわかれば（あるいは、誤差が観測間で「伝染」することがわかれば）、この構造を利用して、よりよい予測をすることができるかもしれません。

## 空間構造をモデルに含めるモチベーション

- 誤差の空間的な構造は、地理が何らかの属性であるべきなのに、それをどのようにモデルに含めればよいのかがはっきりしない場合に生じるかもしれません。
- また、他の特徴があり、その特徴の欠落がエラーの空間的パターンを引き起こしている場合もあります。
- この追加的な特徴が含まれていれば、その構造は消えるでしょう。
- あるいは、予測因子として選んだ特徴の間の複雑な相互作用や相互依存関係から発生し、結果として予測ミスに本質的な構造をもたらすかもしれない。
- 社会的プロセスのモデルで使用する予測変数のほとんどは、具象化された空間情報を含んでいる：
  - モデルで無料で得られる、その特徴に内在するパターン。
- **意図的であろうとなかろうと、空間的にパターン化された予測因子をモデルで使用すると、空間的にパターン化されたエラーが生じる可能性がある**。
- したがって、**真のプロセスが明示的に地理的であるかどうかにかかわらず、我々の観測の間の空間的関係についての追加情報、あるいは近隣のサイトについてのより多くの情報は、我々の予測をより良くすることができる**のである。

## 本章の内容は...!

この章では、従来の回帰のフレームワークに空間を組み込む。

- まず、地理的な参照を排除した標準的な線形回帰モデルから始める。
- そこから、3つの主要な方法で空間と空間的関係を定式化する。
  - 第一に、外生変数(Exogenous Variables)として埋め込む
    - 単に説明変数として？？
  - 第二に、空間的不均質性(Spatial Heterogeneity)、、すなわち空間横断的な結果の系統的変動(Systematic variation)として。
    - 階層ベイズで、回帰係数に空間的な違いを考慮する？？
  - 第三に、依存性(Dependence)、すなわち空間的隣人(Spatial Neighbors)の特性に関連する効果として。
    - 空間重み行列を使って説明変数に間接効果を加えるやつ？？

全体を通して、我々は技術的な詳細よりも、各アプローチが内包する概念的な違いに焦点を当てる。

```python
from pysal.lib import weights
from pysal.explore import esda
import numpy
import pandas
import geopandas
import matplotlib.pyplot as plt
import seaborn
import contextily
```

# サンプルデータ: San Diego AirBnB

回帰がどのように機能するかをもう少し学ぶために、カリフォルニア州サンディエゴのAirBnB物件に関する情報を調べます。このデータセットは、連続的（bedsのようにベッド数）、カテゴリ的（pg_Xの一連のバイナリ変数のように賃貸のタイプ、AirBnBの専門用語では、プロパティグループ）両方の家の固有特性を含みますが、データセットの位置と空間構成を明確に参照する変数（例えば、バルボアパークへの距離、d2balboaや近隣ID、nighbourhood_cleaned）も含んでいます。

```python
db = geopandas.read_file("../data/airbnb/regression_db.geojson")
```

These are the explanatory variables we will use throughout the chapter.

```python
variable_names = [
    "accommodates",  # Number of people it accommodates
    "bathrooms",  # Number of bathrooms
    "bedrooms",  # Number of bedrooms
    "beds",  # Number of beds
    # Below are binary variables, 1 True, 0 False
    "rt_Private_room",  # Room type: private room
    "rt_Shared_room",  # Room type: shared room
    "pg_Condominium",  # Property group: condo
    "pg_House",  # Property group: house
    "pg_Other",  # Property group: other
    "pg_Townhouse",  # Property group: townhouse
]
```

# Non-Spatial Regression, a (very) quick refresh

線形回帰のフレームワークに明示的に空間を含める方法を議論する前に、Pythonで基本的な回帰を実行する方法と、結果を解釈する方法を紹介します。
これは決して回帰の正式で完全な入門書ではありませんので、もしお探しのものがあれば、[GH06]の特に3章と4章が素晴らしい、非空間的な入門書を提供していますので、そちらをお勧めします。

線形回帰の核となる考え方は、与えられた（従属）変数の変動を、**他の（説明）変数の集まりの線形関数**として説明することです。例えば、我々の事例では、家の価格をベッドルームの数とマンションかどうかの関数として表現したいかもしれません。

個人レベルでは、次のように表すことができます：

$$
P_i = \alpha + \sum_{k} X_{ik} \beta_k + \epsilon_i
$$

where

- $P_i$ is the AirBnB price of house $i$,
- $X$ is a set of covariates that we use to explain such price (e.g. No. of bedrooms and condominium binary variable).
- $\beta$ is a vector of parameters that give us information about in which way and to what extent each variable is related to the price,
- $\alpha$, the constant term, is the average house price when all the other variables are zero.
- The term $\epsilon_i$ is usually referred to as “error” and captures elements that influence the price of a house but are not included in $X$.

We can also express this relation in matrix form(行列形式), excluding (includingの逆) subindices for $i$, which yields:

$$
P = \alpha + X \beta + \epsilon
$$

A regression can be seen as a multivariate extension (多変量拡張) of bivariate correlations (二変量相関).
Indeed (実際), one way to interpret the $\beta_k$ coefficients in the equation above (上の式) is as the degree of correlation (相関の度合い. 相関係数ではない笑) between the explanatory variable $k$ and the dependent variable (従属変数), keeping all the other explanatory variables constant.

### 二変数相関と比較したRegressionのメリット

When one calculates bivariate correlations (二変数の相関を計算する時), the coefficient of a variable is picking up (拾う) the correlation between the variables, but it is also subsuming (含んでいる) into it variation (変動) associated with other correlated variables – also called confounding factors.
Regression allows us to isolate (分離する) the distinct (明確な) effect that a single variable has on the dependent one, once (～する事で...) we control for those other variables.

### Regressionの実装

実用的には、Pythonの線形回帰は合理的で簡単に扱えます。また、それらを実行するパッケージもいくつかあります（例：statsmodels, scikit-learn, pysal）。ここでは、Pysal の spreg モジュールをインポートする。

```python
from pysal.model import spreg
```

In the context of this chapter, it makes sense to start with `spreg` as that is the only library that will allow us to move into explicitly spatial econometric models. To fit the model specified in the equation above with $X$ as the list defined, we only need the following line of code:

```python
# Fit OLS model
m1 = spreg.OLS(
    # Dependent variable
    db[["log_price"]].values,
    # Independent variables
    db[variable_names].values,
    # Dependent variable name
    name_y="log_price",
    # Independent variable name
    name_x=variable_names,
)
```

We use the command `OLS`, part of the `spreg` sub-package, and specify the dependent variable (the log of the price, so we can interpret results in terms of percentage change) and the explanatory ones. Note that both objects need to be arrays, so we extract them from the `pandas.DataFrame` object using `.values`.

In order to inspect the results of the model, we can print the `summary` attribute:

```python
print(m1.summary)
```

```
REGRESSION
----------
SUMMARY OF OUTPUT: ORDINARY LEAST SQUARES
-----------------------------------------
Data set            :     unknown
Weights matrix      :        None
Dependent Variable  :   log_price                Number of Observations:        6110
Mean dependent var  :      4.9958                Number of Variables   :          11
S.D. dependent var  :      0.8072                Degrees of Freedom    :        6099
R-squared           :      0.6683
Adjusted R-squared  :      0.6678
Sum squared residual:    1320.148                F-statistic           :   1229.0564
Sigma-square        :       0.216                Prob(F-statistic)     :           0
S.E. of regression  :       0.465                Log likelihood        :   -3988.895
Sigma-square ML     :       0.216                Akaike info criterion :    7999.790
S.E of regression ML:      0.4648                Schwarz criterion     :    8073.685

------------------------------------------------------------------------------------
            Variable     Coefficient       Std.Error     t-Statistic     Probability
------------------------------------------------------------------------------------
            CONSTANT       4.3883830       0.0161147     272.3217773       0.0000000
        accommodates       0.0834523       0.0050781      16.4336318       0.0000000
           bathrooms       0.1923790       0.0109668      17.5419773       0.0000000
            bedrooms       0.1525221       0.0111323      13.7009195       0.0000000
                beds      -0.0417231       0.0069383      -6.0134430       0.0000000
     rt_Private_room      -0.5506868       0.0159046     -34.6244758       0.0000000
      rt_Shared_room      -1.2383055       0.0384329     -32.2198992       0.0000000
      pg_Condominium       0.1436347       0.0221499       6.4846529       0.0000000
            pg_House      -0.0104894       0.0145315      -0.7218393       0.4704209
            pg_Other       0.1411546       0.0228016       6.1905633       0.0000000
        pg_Townhouse      -0.0416702       0.0342758      -1.2157316       0.2241342
------------------------------------------------------------------------------------

REGRESSION DIAGNOSTICS
MULTICOLLINEARITY CONDITION NUMBER           11.964

TEST ON NORMALITY OF ERRORS
TEST                             DF        VALUE           PROB
Jarque-Bera                       2        2671.611           0.0000

DIAGNOSTICS FOR HETEROSKEDASTICITY
RANDOM COEFFICIENTS
TEST                             DF        VALUE           PROB
Breusch-Pagan test               10         322.532           0.0000
Koenker-Bassett test             10         135.581           0.0000
================================ END OF REPORT =====================================
```

### `summary`属性の解釈

A full detailed explanation of the output is beyond the scope of this chapter, so we will focus on the relevant bits for our main purpose. This is concentrated on the Coefficients section, which gives us the estimates for $\beta_k$ in our model. In other words, these numbers express the relationship between each explanatory variable and the dependent one, once the effect of confounding factors has been accounted for. Keep in mind however that regression is no magic; we are only discounting the effect of confounding factors that we include in the model, not of all potentially confounding factors.
出力の詳細な説明はこの章の範囲外なので、我々の主な目的に関連するビットに焦点を当てます。これは、係数セクションに集中しており、我々のモデルにおける$beta_k$の推定値が得られます。言い換えると、これらの数値は、交絡因子の効果が説明された後の、各説明変数と従属変数の間の関係を表しています。しかし、**回帰は魔法ではない**ことに注意してください。我々は、モデルに含まれる交絡因子の効果を割り引いているだけで、**すべての交絡因子の可能性を割り引いているわけではありません**。

Results are largely as expected:

- houses tend to be significantly more expensive if they accommodate more people (`accommodates`), if they have more bathrooms and bedrooms, and if they are a condominium or part of the “other” category of house type.
  - 収容人数が多い場合（accommodates）、バスルームやベッドルームが多い場合、マンションや「その他」のカテゴリーに属する住宅は、著しく高くなる傾向があることがわかった。
- Conversely, given a number of rooms, houses with more beds (i.e.. listings that are more “crowded”) tend to go for cheaper, as it is the case for properties where one does not rent the entire house but only a room (`rt_Private_room`) or even shares it (`rt_Shared_room`).
  - 逆に、部屋数が多ければ、ベッド数が多い家（つまり、より「混んでいる」物件）は安くなる傾向があります。これは、家全体を借りるのではなく、部屋だけを借りる物件（rt_Private_room）、あるいは共有する物件（rt_Shared_room）のケースと同様です。
- Of course, you might conceptually doubt the assumption that it is possible to arbitrarily change the number of beds within an AirBnB without eventually changing the number of people it accommodates, but methods to address these concerns using interaction effects won’t be discussed here.
  - もちろん、AirBnB内のベッド数を任意に変更しても、最終的に収容人数は変わらないという仮定には概念的に疑問があるかもしれないが、交互作用効果を用いてその懸念を払拭する方法はここでは触れないことにする。

## Hidden Structures

- In general, our model performs well, being able to predict slightly about two-thirds ($R^2 = 0.67$) of the variation in the mean nightly price using the covariates (共変量) we’ve discussed above.
- But, our model might display some clustering in the errors, which may be a problem as that violates the **i.i.d. assumption** (**独立同分布**＝**誤差項の均一分散性&共分散0**) linear models usually come built-in with.
- To interrogate this(調べるには), we can do a few things.
- **One simple concept** might be to look at (を調べる) **the correlation between the error in predicting an AirBnB (予測誤差) and the error in predicting its nearest neighbor (近傍の予測誤差)**.
  - To examine this(調べるには),
    - we first might want to split our data up by regions
    - and see if we’ve got some spatial structure in our residuals (残差).
  - One reasonable theory might be that our model does not include any information about beaches, a critical aspect of why people live and vacation in San Diego.
  - Therefore, we might want to see **whether or not our errors are higher or lower (誤差が大きくなるか小さくなるか) depending on whether or not an AirBnB is in a “beach” neighborhood, a neighborhood near the ocean(AirBnBが「ビーチ」地域、つまり海に近い地域にあるかどうか)**:

```python
# Create a Boolean (True/False) with whether a
# property is coastal or not
is_coastal = db.coastal.astype(bool)
# Split residuals (m1.u) between coastal and not
coastal = m1.u[is_coastal]
not_coastal = m1.u[~is_coastal]
# Create histogram of the distribution of coastal residuals
plt.hist(coastal, density=True, label="Coastal")
# Create histogram of the distribution of non-coastal residuals
plt.hist(
    not_coastal,
    histtype="step",
    density=True,
    linewidth=4,
    label="Not Coastal",
)
# Add Line on 0
plt.vlines(0, 0, 1, linestyle=":", color="k", linewidth=4)
# Add legend
plt.legend()
# Display
plt.show()
```

![](https://geographicdata.science/book/_images/11_regression_14_0.png)

海岸沿いの地域は平均誤差がわずかに大きい（予測誤差の分散が小さい）ように見えるが、古典的なt検定で比較すると、この2つの分布は互いに有意に異なることがわかる。

```python
from scipy.stats import ttest_ind

ttest_ind(coastal, not_coastal)

>>Ttest_indResult(statistic=array([13.98193858]), pvalue=array([9.442438e-44]))
```

しかし、このデータに適用できる、より洗練された（そして騙すのが難しい）テストがあります。それらについては、「挑戦」のセクションで取り上げます。

さらに、モデル化されていない潜在的な嗜好やマーケティングによって、ある地域が他の地域よりも望ましいというケースもあり得る。例えば、海に近いにもかかわらず、市の北部にある海兵隊基地Camp Pendletonの近くに住むと、騒音や公害のために地域の望ましさに大きなペナルティーが課されるかもしれない。このような疑問には、領域知識とデータ分析が役立ちます。これが事実かどうかを判断するために、我々は各近隣地域におけるモデル残差の全分布に興味を持つかもしれません。

これをより明確にするために、まずその近傍の残差の中央値でデータをソートし、各近傍の残差の分布を示す箱ひげ図を作成することにします。

```python
# Create column with residual values from m1
db["residual"] = m1.u
# Obtain the median value of residuals in each neighbourhood
medians = (
    db.groupby("neighborhood")
    .residual.median()
    .to_frame("hood_residual")
)

# Increase fontsize
seaborn.set(font_scale=1.25)
# Set up figure
f = plt.figure(figsize=(15, 3))
# Grab figure's axis
ax = plt.gca()
# Generate bloxplot of values by neighbourhood
# Note the data includes the median values merged on-the-fly
seaborn.boxplot(
    "neighborhood",
    "residual",
    ax=ax,
    data=db.merge(
        medians, how="left", left_on="neighborhood", right_index=True
    ).sort_values("hood_residual"),
    palette="bwr",
)
# Auto-format of the X labels
f.autofmt_xdate()
# Display
plt.show()
```

![](https://geographicdata.science/book/_images/11_regression_19_0.png)

しかし、ガスランプ・クオーター、リトル・イタリー、ザ・コアといったダウンタウンの有名な観光地など、他の地域より高い値を示している地域もある。このように、このモデルでは、無形の近隣のファッション性が重要な影響を及ぼしている可能性があります。

また、最も過大予測された地域と過小予測された地域が市内で互いに近接していることに注目すると、夜間賃料価格に何らかの伝染や空間的波及が起きている可能性も考えられる。これは、個人がAirBnBのリスティングの価格を近隣の類似のリスティングと競合するようにしようとするときにしばしば明らかになる。我々のモデルはこのような挙動を認識していないので、その誤差はクラスター化する傾向があるかもしれません。この構造を見ることができる非常に簡単な方法の1つは、ある観測の残差とその周囲の残差の間の関係を調べることです。

To do this, we will use spatial weights to represent the geographic relationships between observations. We cover spatial weights in detail in Chapter 4, so we will not repeat ourselves here. For this example, we’ll start off with a KNN matrix where k=1, meaning we’re focusing only on the linkages of each AirBnB to their closest other listing.

これを行うために、オブザベーション間の地理的関係を表現するために空間的重みを使用します。空間重みについては、第4章で詳しく説明するので、ここでは繰り返さない。この例では、まず k=1 の KNN 行列から始めます。つまり、各 AirBnB の最も近い他のリスティングへのリンクのみに焦点を当てます。

```python
knn = weights.KNN.from_dataframe(db, k=1)
```

つまり、そのKNN WeightによるSpatial Lagと残差を計算すると、各オブザベーションに最も近いAirBnBリスティングの残差が得られるということです。

```python
lag_residual = weights.spatial_lag.lag_spatial(knn, m1.u)
ax = seaborn.regplot(
    m1.u.flatten(),
    lag_residual.flatten(),
    line_kws=dict(color="orangered"),
    ci=None,
)
ax.set_xlabel("Model Residuals - $u$")
ax.set_ylabel("Spatial Lag of Model Residuals - $W u$");
```

このプロットでは、予測誤差が密集する傾向があることがわかります。上図は、各サイトの予測誤差と、そのサイトに最も近いサイトの予測誤差の関係を示しています。ここでは、この最寄りのサイトを、そのAirBnBの周辺に置き換えています。つまり、あるAirBnBの1泊のログ価格が過剰に予測される傾向がある場合、そのAirBnBの周辺サイトも過剰に予測される可能性が高くなるのです。この関係の興味深い特性は、各AirBnBの周辺を構築するために使用される最近傍の数が増加すると安定する傾向があることです。この性質については、チャレンジのセクションを参照してください。

この挙動を踏まえて、安定したk=20の隣人数について見てみましょう。この安定した周辺平均と焦点となるAirBnBの関係を調べると、モデル誤差にクラスタを見出すこともできます。第7章のローカルモラン統計量を参照すると、一晩のAirBnB価格（対数）の予測が大きく外れる傾向がある地域を特定することができます。

```python
# Re-weight W to 20 nearest neighbors
knn.reweight(k=20, inplace=True)
# Row standardise weights
knn.transform = "R"
# Run LISA on residuals
outliers = esda.moran.Moran_Local(m1.u, knn, permutations=9999)
# Select only LISA cluster cores
error_clusters = outliers.q % 2 == 1
# Filter out non-significant clusters
error_clusters &= outliers.p_sim <= 0.001
# Add `error_clusters` and `local_I` columns
ax = (
    db.assign(
        error_clusters=error_clusters,
        local_I=outliers.Is
        # Retain error clusters only
    )
    .query(
        "error_clusters"
        # Sort by I value to largest plot on top
    )
    .sort_values(
        "local_I"
        # Plot I values
    )
    .plot("local_I", cmap="bwr", marker=".")
)
# Add basemap
contextily.add_basemap(ax, crs=db.crs)
# Remove axes
ax.set_axis_off();
```

したがって、これらのエリアは、我々のモデルがその特定のオブザベーションとその近辺のオブザベーションの両方でAirBnBの夜間価格を著しく低く予測する場所である傾向があります。もし、これらのエリアがどのように構成されているかを識別できれば、つまり、モデル化できる一貫した地理があれば、我々の予測をさらに良くすることができ、少なくとも、あるエリアでの価格を体系的に間違って予測し、他のエリアでの価格を正しく予測することはなくなるかもしれないので、これは重要です。予測不足と予測過多が高度に構造化されているように見えるので、より優れたモデルを用いて、モデル誤差の地理的特性を修正することができるかもしれません。

# Bringing space into the regression framework

空間構造については、特に研究しようと思っていなくても、モデルや予測、データの中に様々な形で現れることがあります。幸いなことに、このような種類の構造を扱うための**空間回帰法と呼ばれるテクニック**が、同じくらいたくさんあります。空間回帰は、回帰の統計的な枠組みに空間や地理的な文脈を明示的に導入することです。
概念的には、我々は以下の条件の時、いつでもモデルに空間(space)を導入したいのである。

- 空間(space)が我々が興味を持っているプロセスで重要な役割を果たしていると思うとき
  - 前者の例として、海辺の家は眺めが良いので、2列目の家より高いだろうことが想像できる。
- あるいは空間(space)が、我々がモデルに含めることはできないが含めるべき他の要因の妥当な代理として働くことができるとき。
  - 後者の例としては，近隣の地域の特性が住宅の価格を決定する上でいかに重要であるかを考えることができる。しかし，「特性」それ自体を特定して定量化することは非常に難しいが，その空間的変化を把握することは容易であろうから，空間を代理とするケースもある。

空間回帰は、計量経済学や統計学の文献の中で大きな発展を遂げている分野である。この簡単な紹介では、空間効果を生み出す、関連はあるが全く異なる2つのプロセス、空間的不均質性と空間的依存性について考えてみることにする。その前に、回帰モデルに空間を導入するアプローチとして、モデル自体を修正するのではなく、空間的に明示的な独立変数を作成する方法から始める。ここで紹介するトピックのより厳密な処理については、[Ans03, AR14, GH06]を参照されたい。

# 空間情報を埋め込む方法1:Spatial Feature Engineering: Proximity Variables(近接変数)

**地理情報を使って新しいデータを「構築」するこ**とは、データ分析に空間情報を持ち込むための一般的なアプローチである。多くの場合、これは、分析対象地図のどこでも同じプロセスがあるわけではないこと、あるいは、地理的情報が我々の関心のある結果を予測するのに有用であることを反映したものである。このセクションでは、**標準的な線形モデルに空間特徴、または地理的な関係から構築されるX変数を挿入する方法**を簡単に紹介します。
しかし、**Spatial Feature Engineering**については、第12章で広範囲に説明しており、Spatial Feature Engineeringの深さと広さは言い尽くせないほどです。このセクションでは、詳細というよりも、エンジニアリングした空間的な明示的な変数をどのようにモデルに「プラグイン」して、そのパフォーマンスを向上させたり、関心のある根本的なプロセスをより正確に説明するのに役立てたりするかを紹介します。

当社のサンディエゴモデルに影響を与える可能性のある近接駆動型変数の1つは、バルボアパークへのリスティングの近接性に基づいています。一般的な観光地であるBalboa公園は、多くの博物館やサンディエゴ動物園を含む、サンディエゴの街の中心的なレクリエーション拠点です。したがって、サンディエゴでAirBnBを検索する人は、公園に近いところに住むために割増料金を支払うことを望んでいる、ということが考えられます。もしこれが本当で、モデルからこれを省略した場合、確かにこの距離減衰効果による有意な空間パターンを見ることができるかもしれない。

したがって、これはSpatially-Patterned Omitted Covariate(空間的にパターン化された省略された共変量)と呼ばれることがあります：モデルが良い予測をするために必要な地理的情報ですが、モデルから除外されています。
したがって、このBalboa Parkまでの距離を共変量として含む新しいモデルを構築してみましょう。しかし、まず、この距離の共変量自体の構造を可視化するのに役立ちます。

```python
ax = db.plot("d2balboa", marker=".", s=5)
contextily.add_basemap(ax, crs=db.crs)
ax.set_axis_off();
```

公園までの距離という追加変数を含む線形モデルを実行するために、元々含んでいた変数のリストに名前を追加します。

```python
balboa_names = variable_names + ["d2balboa"]
```

そして、PysalのspregのOLSクラスを使ってモデルを当てはめます。

```python
m2 = spreg.OLS(
    db[["log_price"]].values,
    db[balboa_names].values,
    name_y="log_price",
    name_x=balboa_names,
)
```

回帰診断と出力を見てみると、この共変量は我々が予想したほどには役に立っていないことがわかります。

```python
pandas.DataFrame(
    [[m1.r2, m1.ar2], [m2.r2, m2.ar2]],
    index=["M1", "M2"],
    columns=["R2", "Adj. R2"],
)
```

従来の有意水準では統計的に有意ではなく、モデルの適合度は実質的に変化していない。

```python
# Set up table of regression coefficients
pandas.DataFrame(
    {
        # Pull out regression coefficients and
        # flatten as they are returned as Nx1 array
        "Coeff.": m2.betas.flatten(),
        # Pull out and flatten standard errors
        "Std. Error": m2.std_err.flatten(),
        # Pull out P-values from t-stat object
        "P-Value": [i[1] for i in m2.t_stat],
    },
    index=m2.name_x,
)
```

そして、このモデルの誤差には、やはり空間的な構造があるようだ。(誤差が大きいObservationの近傍のObservationsの誤差も大きい傾向にある)

```python
lag_residual = weights.spatial_lag.lag_spatial(knn, m2.u)
ax = seaborn.regplot(
    m2.u.flatten(),
    lag_residual.flatten(),
    line_kws=dict(color="orangered"),
    ci=None,
)
ax.set_xlabel("Residuals ($u$)")
ax.set_ylabel("Spatial lag of residuals ($Wu$)");
```

最後に、バルボアパークへの距離の変数は、アメニティへの距離がAirBnBの価格にどのように影響するかについての我々の理論に適合していません：係数の推定値は正で、人々は公園から遠いことにプレミアムを払っていることを意味します。この結果については、後ほど空間的不均質性を考慮した上で再検討し、明らかにする予定である。さらに、次の章では空間固定効果について幅広く扱い、より多くのSpatial Feature Engineeringの手法を提示します。ここでは、**標準的な線形モデリングの枠組みの中で、これらの工学的特徴を含む方法を示したに過ぎない**。

# 空間情報を埋め込む方法2:Spatial Heterogeneity(空間的異質性)

これまで我々は、近接変数が、レクリエーションゾーン（この場合、公園）に近いときに個人が支払う測定しにくいプレミアムを代用する可能性があると仮定してきました。その場合の我々のアプローチは、非常に特殊なチャネル、つまり、最終的な価格に影響を与えると考えられるアメニティへの距離を通じて空間を組み込むことでした。

**しかし、すべての地域の住宅価格が同じとは限りません**。ある地域は、バルボア公園への近さに関係なく、他の地域よりも体系的に高いかもしれません。

このような場合、それぞれの地域がこのようなゲシュタルト的でユニークな効果を経験Spatial Heterogeneityを捉えることです。

最も基本的なことですが、Spatial Heterogeneityとは、モデルの一部が地理的な要因によって系統的に変化し、異なる場所で変化する可能性があることを意味します。

- 例えば、切片、$alpha$の変化は、異なる地域が与えられたプロセスに対する異なるベースライン露出を持つという事実を反映することができる。
- 回帰係数$\beta$の変化は、独立変数と従属変数の関係を空間的に変化させる何らかの地理的な媒介因子を示すかもしれない、例えば、政府の政策が管轄区域間で一貫して適用されていない場合などである。
- 最後に、一般に$sigma^2$と呼ばれる残差の分散の変化は、空間的異種分散性をもたらす可能性がある。

このセクションでは、最初の二つを扱う。

## Spatial Fixed Effects 空間固定効果

- この文献では、一般に$alpha$の地理的な変動を「**Spatial Fixed Effects(空間固定効果)**」と呼んでいる。
- それを説明するために、前節の住宅価格の例で考えてみよう。
  - 空間固定効果は、結果が空間的に変化することを知っていて、それがどのようなパターン（我々の場合、近隣によって）であるかを知っていて、それに応じて$αla$を変化させることによって、その知識をモデルに取り入れることができるという意味で、「**space as a proxy(代理としての空間)**」を捉えると言われることがある。
  - その根拠は次のようなものである。
    - 我々がモデルにいくつかの説明変数しか含めていないことを考えると、家が売られる価格を決定する際に役割を果たすいくつかの重要な要因を見逃している可能性がある。
    - しかし、それらのいくつかは、**空間的に系統的に変化する**可能性が高い（例えば、異なる近隣特性）。
    - もしそうであれば、我々は、伝統的なバイナリ変数を使用し、その作成を空間的なルールに基づくことによって、それらの観察されない要因をコントロールすることができます。
    - たとえば、すべての近隣に対して、与えられた家がその地域内にあるかどうか（1）、または（0）を示すバイナリ変数を含めるとします。数学的には、我々は今、次の方程式に適合している。

$$
\log P_i =\alpha_r + \sum_{k}{X_{ik} \beta_{k}} + \epsilon_i
$$

ここで、主な違いは、定数項である$alpha$を近傍$r$で変化させること、$alpha_r$であることです。

プログラム的には、statsmodelsを使う方法と、spregを使う方法の2種類を紹介します。まず、Pythonの計量経済学ツールボックスであるstatsmodelsを使用します。

```python
import statsmodels.formula.api as sm
```

このパッケージは数式に似たAPIを提供し、推定したい方程式を直接表現することができる。

```python
f = (
    "log_price ~ "
    + " + ".join(variable_names)
    + " + neighborhood - 1"
)
print(f)
>>>log_price ~ accommodates + bathrooms + bedrooms + beds + rt_Private_room + rt_Shared_room + pg_Condominium + pg_House + pg_Other + pg_Townhouse + neighborhood - 1
```

この文の**チルダ演算子**は、通常「log_price is a function of ...」と読みます。これは、log_priceと共変量リストの間の関数関係に従って、多くの異なるモデル仕様を適合させることができるという事実を説明するためです。
重要なのは、末尾の-1項が、切片項なしでこのモデルをフィットさせることを意味していることです。これは必要なことです。
なぜなら、すべての近隣地域に対して一意な平均と一緒に切片項を含めると、基礎となる方程式系が十分に規定されなくなるからです。

この式を用いて、statsmodelsでモデルをあてはめながら、各近隣の固有の効果を推定することができる（モデルの指定、式、データが、あてはめのステップと分離されていることに注意）。

```python
m3 = sm.ols(f, data=db).fit()
```

回帰から同様の要約レポートを出力するために `summary2()` メソッドに頼ることもできますが、今回は長いので、Spatial Fixed Effectsを表示するために表に抽出する方法を説明します。

```python
# Store variable names for all the spatial fixed effects
sfe_names = [i for i in m3.params.index if "neighborhood[" in i]
# Create table
pandas.DataFrame(
    {
        "Coef.": m3.params[sfe_names],
        "Std. Error": m3.bse[sfe_names],
        "P-Value": m3.pvalues[sfe_names],
    }
)
```

## Spatial Regimes

- Spatial Fixed Effectの推定の核心は、**従属変数が空間的に一様な振る舞いをすると仮定するのではなく、その振る舞いに影響を与える地理的パターンに従った系統的効果が存在するという考え方**である。
  - 言い換えれば、Spatial FEはSpatial Heterogeneityという概念を経済学的に導入する。
  - これは、定数項を地理的に変化させるという、最も単純な形で行われる。
  - 回帰の他の要素はそのままで、それゆえ空間的に一様に適用される。
- 空間レジーム（SR）の考え方は、空間FEアプローチを一般化して、**定数項だけでなく、他の説明変数も変化させる**ことができるようにすることです。
- これは、これから推定する方程式を意味する。

$$
\log P_i = \alpha_r + \sum_{k}{X_{ki}\beta_{k-r}} + \epsilon_i
$$

ここで、定数項($\alpha_r$)だけでなく、他のすべてのパラメータも地域によって変化するようにする($\beta_{kr}$)。

このアプローチを説明するために、**家が沿岸地域にあるかどうか**という「Spatial Differentiator(空間的差別化要因)」（`coreast_neig`）を使って、レジームを定義することにする。
この選択の根拠は、海の近くに家を借りることは、人々が家の特性ごとに異なるレートで支払うことを望むほど強い引力であるかもしれないということである。

# 空間情報を埋め込む方法3:Spatial Dependence

## Exogenous Effects: The SLX Model

$$
\log (P_i) = \alpha + \sum_{k=1}^{p}{X_{ij}\beta_{j}}
+ \sum_{k=1}^{p}(\sum_{j=1}^{N} w_{ij} x_{jk})\gamma_{k} + \epsilon_i
$$

$$
\log (P_i) = \alpha + X\beta + WX\gamma + \epsilon
$$

As an illustration, let’s look at some of the direct/indirect effects. The direct effect of the pg*Condominium variable means that condominiums are typically 11% more expensive ($\beta*{pg*Condominium} = 0.1063$) than the benchmark property type, apartments. More relevant to this section, any given house surrounded by condominiums also receives a price premium. But, since $pg*{Condominium}$ is a dummy variable, the spatial lag at site represents the percentage of properties near that are condominiums, which is between $0$ and $1$. So, a unit change in this variable means that you would increase the condominium percentage by 100%. Thus, a .1 increase in w*pg_Condominium (a change of ten percentage points) would result in a 5.92% increase in the property house price ($\betas*{w_pg_condominium}=0.6$). Similar interpretations can be derived for all other spatially lagged variables to derive the indirect effect of a change in the spatial lag.

To compute the indirect change for a given site $i$, you may need to examine the predicted values for its price. In this example, since we are using a row-standardized weights matrix with twenty nearest neighbors, the impact of changing $x_i$ is the same for all of its neighbors and for any site . Thus, the effect is always $\gamma / 20$, or about $0.0296$. However, it is interesting to consider this would not be the case for many other kinds of weights (like Kernel, Queen, Rook, DistanceBand, or Voronoi), where each observation has potentially a different number of neighbors. To illustrate this, we will construct the indirect effect for a specific $i$ in the condominium group.

First, predicted values for $y_i$ are stored in the predy attribute of any spreg model:

## Spatial Error

The spatial error model includes a spatial lag in the error term of the equation:空間誤差モデルは、方程式の誤差項に空間ラグを含んでいる。

$$
\log P_i = \alpha + \sum_{k} \beta_{k} X_{ki} + u_{i} \\
u_{i} = \lambda u _{lag, i} + \epsilon_{i}
$$

where $u_{lag, i} = \sum_{j} w_{ij} u_{j}$. Although it appears similar, this specification violates the assumptions about the error term in a classical OLS model. Hence, alternative estimation methods are required. Pysal incorporates functionality to estimate several of the most advanced techniques developed by the literature on spatial econometrics. For example, we can use a general method of moments that account for heteroskedasticity [ADKP10]:

ここで、$u_{lag, i} = \sum_{j} w_{ij} u_{j}$ である。一見似ているが、この仕様は古典的なOLSモデルの誤差項に関する仮定に違反している。したがって、別の推定方法が必要である。Pysalは空間経済学の文献で開発された最も高度な手法のいくつかを推定する機能を組み込んでいる。例えば、ヘテロスケダスティックスを考慮した一般的なモーメント法[ADKP10]が利用可能である。

Similarly as before, the summary attribute will return a full-featured table of results. For the most part, it may be interpreted in similar ways to those above. The main difference is that, in this case, we can also recover an estimate and inference for the $\lambda$ parameter in the error term:

以前と同様に、summary属性は結果の全機能のテーブルを返します。ほとんどの場合、上記と同様の方法で解釈することができます。主な違いは、この場合、誤差項の$lambda$パラメータの推定と推論も回復できることである。

## Spatial Lag

The spatial lag model introduces a spatial lag of the dependent variable. In the example we have covered, this would translate into:

$$
\log P_i = \alpha + \rho \log P_{lag, i} + \sum_{k} \beta_{k} X_{ki} + \epsilon_{i}
$$

Although it might not seem very different from the previous equation, this model violates the exogeneity assumption, crucial for OLS to work. Put simply, this occurs when $P_i$ exists on both “sides” of the equals sign. In theory, since $P_i$ is included in computing $P_{lag, i}$, exogeneity is violated. Similarly to the case of the spatial error, several techniques have been proposed to overcome this limitation, and Pysal implements several of them. In the example below, we use a two-stage least squares estimation [Ans88], where the spatial lag of all the explanatory variables is used as instrument for the endogenous lag:

Similarly to the effects in the SLX regression, changes in the spatial lag regression need to be interpreted with care. Here, W_log_price applies consistently over all observations, and actually changes the effective strength of each of the $\beta$ coefficients. Thus, it is useful to use predictions and scenario-building to predict $y$ when changing $X$, which allows you to analyze the direct and indirect components.
## Other ways of bringing space into regression

We have covered here only a few ways to formally introduce space in a regression framework. There are however many other advanced spatial regression methods routinely used in statistics, data science, and applied analysis. For example, Generalized Additive Models [GOP15, Woo06] haven been used to apply spatial kernel smoothing directly within a regression function. Other similar smoothing methods, such as spatial Gaussian process models [BFC10] or Kriging, conceptualize the dependence between locations as smooth as well. Other methods in spatial regression that consider graph-based geographies (rather than distance/kernel effects) include variations on conditional autoregressive model, which examines spatial relationships at locations conditional on their surroundings, rather than as jointly co-emergent with them. Full coverage of these topics is beyond the scope of this book, however, though [BGFS08] provides a detailed and comprehensive discussion. We have not covered these (and other existing ones) not because we do not think are important or useful, far from it, but because we consider them a bit more advanced than the level at which we wanted to pitch the chapter.

ここでは、回帰のフレームワークで空間を正式に導入するいくつかの方法のみを取り上げました。しかし、統計学、データサイエンス、応用分析で日常的に使用されている高度な空間回帰手法は他にもたくさんあります。例えば，Generalized Additive Models [GOP15, Woo06]は，回帰関数の中で直接空間カーネルスムージングを適用するのに使われています．空間ガウス過程モデル[BFC10]やKrigingなどの他の類似の平滑化手法は，同様に場所間の依存性を平滑化として概念化する．グラフベースの地理を考慮した空間回帰の他の方法（距離/カーネル効果ではなく）には、条件付き自己回帰モデルのバリエーションがあり、これは、場所での空間関係を、それらと共同で発生するものとしてではなく、それらの周囲に条件付きで検討するものです。しかし、これらのトピックを完全にカバーすることは本書の範囲外であり、[BGFS08]が詳細かつ包括的な議論を提供している。私たちがこれら（および他の既存のもの）を取り上げなかったのは、重要でない、あるいは有用でないと考えたからではなく、それどころか、私たちがこの章を投げかけたいと思ったレベルよりも少し高度であると考えたからである。

# Questions

## Challenge Questions

The following discussions are a bit challenging, but reflect extra enhancements to the discussions in the chapter that may solidify or enhance an advanced understanding of the material.以下の議論は少し難しいですが、その章の議論をさらに強化することで、材料の高度な理解を強固にしたり、強化したりすることができます。

### the random coast

In the section analyzing our naive model residuals, we ran a classic two-sample t-test to identify whether or not our coastal and not-coastal residential districts tended to have the same prediction errors. Often, though, it’s better to use straightforward, data-driven testing and simulation methods than assuming that the mathematical assumptions of the -statistic are met. 素朴なモデルの残差の分析では、沿岸部とそうでない住宅地の予測誤差が同じ傾向にあるかどうかを確認するために、古典的な2標本のt検定を行っています。しかし、多くの場合、-統計量の数学的仮定が満たされていると仮定するよりも、データに基づいたテストやシミュレーションの方法を使用した方が良い場合が多いのです。

## Next steps

For additional reading on the topics covered in this chapter, please consult the following resources:

For a more in-depth discussion of the fundamentals of spatial econometrics and applications in both GUI and command-line software, consult

Anselin, Luc and Sergio Rey. 2014. Modern Spatial Econometrics in Practice: A Guide to GeoDa, GeoDaSpace, and Pysal. GeoDa Press.

For additional mathematical detail and more extensive treatment of space-time models, consult:

Cressie, Noel and Christopher N. Wikle. 2011. Statistics for Spatio-Temporal Data. Singapore: Wiley Press.

For an alternative perspective on regression and critique of the spatial econometric perspective, consider:

Gibbons, Stephen and Henry G. Overman. 2012. “Mostly Pointless Spatial Econometrics.” Journal of Regional Science 52: 172-191.

And for a useful overview of the discussions around multilevel modelling, with references therein to further resources, consider:

Owen, Gwilym, Richard Harris, and Kelvyn Jones. “Under Examination: Multilevel models, geography and health research.” Progress in Human Geography 40(3): 394-412.

本章で取り上げたトピックについてさらに詳しく知りたい場合は、以下の資料を参照してください。

空間計量学の基礎とGUIおよびコマンドラインソフトウェアのアプリケーションについてのより詳細な議論については、以下を参照してください。

Anselin, Luc and Sergio Rey. 2014. Modern Spatial Econometrics in Practice: GeoDa、GeoDaSpace、およびPysalへのガイド。GeoDa Press.

数学的な詳細と時空間モデルのより広範な取り扱いについては、以下を参照。

Cressie, Noel and Christopher N. Wikle. 2011. 時空間データのための統計学. シンガポール．Wiley Press.

回帰の別の視点と空間経済学の視点に対する批判については、以下のように考えている。

Gibbons, Stephen and Henry G. Overman. 2012. "Mostly Pointless Spatial Econometrics". ジャーナル・オブ・リージョナル・サイエンス 52: 172-191.

また、マルチレベル・モデリングをめぐる議論の有用な概要については、そこにさらなるリソースを参照することで、検討することができます。

Owen, Gwilym, Richard Harris, and Kelvyn Jones. "Under Examination: マルチレベル・モデル、地理学、健康研究". Progress in Human Geography 40(3): 394-412.
