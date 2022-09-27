## link

- https://geographicdata.science/book/notebooks/09_spatial_inequality.html

## メモ

- この視点は特に自分の研究でも使えそう！
- 特に地域ごとのMaterial Stock & Flowの重量の推移。"過去から現在"での推移でもいいし、解体&退蔵確率モデルを活用して得られた"現在から将来"での推移でも面白そう！
- これまでは単に重量や割合の空間分布を描いて、ぼんやりと考察を書く事しかできなかったが、きちんと地域ごとに空間統計的な評価指標を算出した上で評価できそう...!

# Spatial Inequality Dynamics

- 本章では、経済的不平等を例にとり、社会的格差の発展に関する研究が、いかに空間的な扱いを明確にすることで利益を得ることができるかを説明する。社会的・経済的不平等は、しばしば政策立案者の課題の最上位に位置づけられる。その研究は、学問の世界でも常に大きな関心を集めてきた。その多くは、個人間の所得格差、つまり、その人が出て行く地域の違いに関係なく、個人間の格差に焦点が当てられてきた。しかし、発展途上国や先進国において、貧 しい地域と豊かな地域の間の格差の拡大が市民動乱 [Ezc19]や政治的分極化 [RP18]の主要因として認識されていることから、地域間の所得不平等の問題にはさらなる注意が必要であるとの認識が広がっている。

## 今回の分析テーマ(経済的不平等)に関するIntroduction

- 不平等に関する研究の多くは、「個人間でどのように結果が異なるのか」という個人レベルに焦点を当てたものである。
  - このアプローチでは、個人を地理的にグループ化することはしない。言い換えれば、こうした差異が、例えば地域レベルでパターンに従っているかどうかには関心がない（例えば、より不利な人口の多くは、地図の特定のセクションに位置しているかどうか）。
  - 実際、この2つの文献（個人的不平等と地域的不平等）は関連しているものの、ほぼ並行して発展してきたため、相互補完は限定的であった。
- 本章では、空間的に明確な焦点を当てることで、不平等とそのダイナミクスの研究にどのような洞察をもたらすことができるかを検討する。
- この図解はそれ自体有用であるが、地域的視点が価値をもたらすことができる他の現象の研究において、これらの方法を使用するきっかけとなることを希望している。
- この章はまた、**追加的な次元として時間を明示的に扱う**唯一の章である。
- この章では、**異なる指標が時間とともにどのように変化するか、空間的なパターンがどの程度変化するかを考慮**し、本質的に時間的な観点から不平等を表現している。
- ここでも、不平等指標を用いた図解が、それ自体で価値を持つだけでなく、より広い文脈で時間や力学に取り組むためのインスピレーションとなることを願っています。

- 我々が用いるデータについて説明した後、まず対人所得格差分析の古典的な手法を紹介し、それらがどのように地域格差の問題に採用されてきたかを説明する。
  - これらの方法には、不平等のよく知られた指標とともに、多くのグラフツールが含まれる。さらに詳しく説明すると、空間的に参照されたデータにおけるこれらの古典的な手法の使用は、空間的不平等のいくつかの側面に関する洞察を提供する上で有用であるが、地理的格差の性質とそのダイナミクスを完全に捉えることはできない。
  - そこで、次に、地域的不平等分析のための空間的に明示的な尺度に移行する。本章は、地域的不平等の動態の空間的次元をより完全に検討するために、いくつかの古典的な尺度を最近拡張したことを紹介し、この章を閉じる。

```python
import seaborn
import pandas
import geopandas
import pysal
import numpy
import mapclassify
import matplotlib.pyplot as plt
from pysal.explore import esda
from pysal.lib import weights
```

# Data: US State Per Capita Income 1969-2017

- 本章では、一人当たりの平均所得を経年変化させたデータを使用する。
  - 具体的には、1969 年から 2017 年までの米国郡を検討する。
  - USカウンティは、州の中に階層的に収まる小さな地域である。
  - この視点により、個々の観測値（郡）、または地理的に一貫した方法でそれらを複数含む地域（州または州の集合体である国勢調査地域）の傾向を調べることができる。
  - **時間的アプローチにより、これらの主体がより豊かになったのか、より貧しくなったのか、また、全体的な所得分布がどのように動き、偏り、広がっていくのか**を明らかにすることができる。

```
pci_df = geopandas.read_file(
    "../data/us_county_income/uscountypcincome.gpkg"
)
pci_df.columns

Index(['STATEFP', 'COUNTYFP', 'COUNTYNS', 'GEOID', 'NAME', 'NAMELSAD', 'LSAD',
       'CLASSFP', 'MTFCC', 'CSAFP', 'CBSAFP', 'METDIVFP', 'FUNCSTAT', 'ALAND',
       'AWATER', 'INTPTLAT', 'INTPTLON', 'GeoFIPS', 'GeoName', 'Region',
       'TableName', 'LineCode', 'Descriptio', 'Unit', '1969', '1970', '1971',
       '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980',
       '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989',
       '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
       '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
       '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
       '2017', 'index', 'IndustryCl', 'Descript_1', 'geometry'],
      dtype='object')
```

## dataの中身

- 列の名前を見ると、この表は1つの県に1つの行があり、特定のレコードに関する情報とともに年が列として構成されていることがわかる。
- この形式は、広域縦断データの一例である。
- ワイドフォーマットでは、各列は異なる期間を表し、各行は同じ「主体」について長期間にわたって行われた一連の測定値（およびその主体に関する固有の識別情報）を表していることになる。
- 長尺データは記録の重複が大きく、特に地理的なケースでは一般にデータ保存に不利である。
- しかし、[W+14]が論じているように、データを操作・分析する際には長大な形式のデータの方が有用な場合があります。
- それでも、軌跡、つまり実体が時間の経過とともにたどる道筋を分析する場合には、幅広のデータの方が有用であり、ここではそれを使うことにする。

このデータセットでは、49年間にわたる3076の郡と、各郡を説明する28の余分な列がある。

```python
pci_df.shape

>>(3076, 77)
```

例として、ミシシッピ州ジャクソン郡（州コード28）の最初の10年間を以下に見ることができる。

```python
pci_df.query('NAME == "Jackson" & STATEFP == "28"').loc[
    :, "1969":"1979"
]
```

# Global Inequality

## Intro

まず、所得不平等に関するいくつかのグローバルな指標に注目し、不平等について考察を始める。ここで、「グローバル」とは、その尺度が所得分布内の不平等の全体的な性質に関係していることを意味する。つまり、これらの尺度は、富裕層と貧困層の間の直接的な格差に焦点を当て、富裕層と貧困層がどこに住んでいるかについては何も考慮しない。この目的のために、いくつかの古典的な不平等尺度が利用可能である。

## Inequalityの測定

一般的に、不平等の測定は、**所得分布に存在する分散**に焦点を当てる。地域的・空間的不平等の場合、分布は、郡、国勢調査区、地域といった空間単位での平均または一人当たりの所得を記述している。米国の郡のデータでは、サンプルの最初の年の一人当たり所得の分布を次のように可視化することができる。

```python
seaborn.histplot(x=pci_df["1969"], kde=True);
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_11_0.png)

この分布を見ると、分布の右側が左側よりもずっと長いことに気がつきます。この長い右尾は顕著な特徴で、所得やその他多くの社会現象の研究において一般的です。これは、一つの所得分布の中で、平均と比較して、超富裕層が超貧困層よりはるかに裕福であるという事実を反映しているからです。

ここで注意しなければならないのは、**このデータの測定単位が個人所得の空間的な集計であるということ**である。ここでは、**各県の一人当たり所得**を使用している。これに対して、より広い不平等に関する文献では、**観測単位は通常、世帯または個人**である。**後者の分布では、歪度の程度がより顕著になることが多い**。
この違いは、集計に内在する平滑化に起因する。地域分布は、個人の分布から得られた平均に基づいており、したがって、極めて高所得の個人は、その郡の他の人々と平均化されるのである。地域的アプローチは、地理的な集計から個人の結論が導き出されるという、いわゆる「生態学的誤謬」に陥るのを避けるために、個人（個人）ではなく地域（郡）レベルで結論を出すことを意味する。

## Kernel Density Estimateやヒストグラムの活用＝＞第二の視点コロプレスマップへ

カーネル密度推定値（またはヒストグラム）は、この所得指標に関する特徴的な分布の全体的な形態を捉える強力な視覚化装置である。
同時に、このプロットは県民所得の地理的分布の根底にあるものには触れていない。
この分布の第二の視点は、コレプスマップ（choropleth map）を使って見ることができる。これを作成するには、標準的なジオパンダのプロットツールを使用することができます。

地図作成に入る前に、CRSを地図作成に適したもの、北米のAlbers Equal Area Projectionに変更する。

```python
pci_df = pci_df.to_crs(
    # Albers Equal Area North America
    epsg=5070
)
```

そして、1969年の（分位値）コレプレットは、次のようにして生成できる。

```
ax = pci_df.plot(
    column="1969",
    scheme="Quantiles",
    legend=True,
    edgecolor="none",
    legend_kwds={"loc": "lower left"},
    figsize=(12, 12),
)
ax.set_axis_off()
plt.show()
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_16_0.png)

カーネル密度推計(or ヒストグラム)は、県民所得分布の異なる視覚的描写を提供する。
カーネル密度推定は特徴に基づく表現であり、地図は地理に基づく表現である。
どちらも、より包括的な理解を深めるのに有効である。

## 分布のInequalityに関する評価指標

分布の不平等度に関する洞察を得るために、**統計学や計量経済学の文献で一般的ないくつかの指標について**説明する。

## 20:20 Ratio

分布の不平等の指標としてよく使われるのが、20：20比率と呼ばれるもので、80％台の所得と20％台の所得の比率と定義される。

```python
top20, bottom20 = pci_df["1969"].quantile([0.8, 0.2])
```

top20 (bottom20) オブジェクトには、分布の上位 (下位) 20%とそれ以外との系列を分ける境界値が格納されています。これらを用いて、比率を生成することができます。

```python
top20 / bottom20
>>1.5022494887525562
```

1969年には、最も裕福な20%の郡の所得は、最も貧しい20%の郡の所得の1.5倍であった。
**この20：20の比率は、分布の上位と下位の異常値に対してロバストであるという利点**がある。
この世界的な**不平等指標のダイナミクス**を見るには、ある年のそれを計算する関数を作成し、**時系列のすべての年にそれを適用する**のが一つの方法である。

```python
def ineq_20_20(values):
    top20, bottom20 = values.quantile([0.8, 0.2])
    return top20 / bottom20


# Generate range of strings from 1969 to 2018
years = numpy.arange(1969, 2018).astype(str)
# Compute 20:20 ratio for every year
ratio_2020 = pci_df[years].apply(ineq_20_20, axis=0)
# Plot evolution of 20:20 ratio
ax = plt.plot(years, ratio_2020)

# Grab figure generated in the plot
figure = plt.gcf()
# Replace tick labels with every other year
plt.xticks(years[::2])
# Set vertical label
plt.ylabel("20:20 ratio")
# Set horizontal label
plt.xlabel("Year")
# Rotate year labels
figure.autofmt_xdate(rotation=45)

plt.show()
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_22_0.png)
この比率の推移を見ると、長い間低下していたものが1994年頃に底を打ち、U字型のパターンを示している。しかし，1994年以降，20：20の比率を見ると，2013年までは不平等が拡大しており，県間の所得格差が小さくなる方向に転じている。

20/20比率に加えて、Gini(ジニ)指数とTheil(テイル)指数という、より伝統的な不平等指標を検討する。これらについては、Pysalのinequalityパッケージを使用する

```python
from pysal.explore import inequality
```

## Gini Index

### ローレンツ曲線

ジニ指数は，累積的な富の分布の概念に基づく不平等の長年の尺度である [MM21]。ジニ指数は、**ローレンツ曲線**と呼ばれる別のよく知られた指標と密接に関連している。ローレンツ曲線を構築するために、富の累積的なシェアは、その富を所有している人口の割合に対してプロットされます。

- 例えば、少数の人々がほぼすべての富を所有している極端な不平等社会では、ローレンツ曲線は最初は非常にゆっくりと増加し、その後、最も裕福な人々が含まれるようになると急上昇する。
- これに対して、「完全平等」な社会は、（0,0）と（1,1）を結ぶ直線のようになる。
  - これは完全平等線と呼ばれ、人口のp %が富のp %をちょうど所有している場合を表しています。
  - 例えば、人口の50％がちょうど50％の所得を得ている、あるいは90％の人口が90％の富を所有している、というようなことである。
  - つまり、富や所得の割合は、その富や所得を所有する人口の割合に正確に比例するということであり、これは、全員が同じ所得を持ち、同じ量の富を所有している場合にのみ発生する。

### Gini指標は...

これらの概念を念頭に置くと、**ジニ指数は、「与えられた所得または富の分布の完全平等線とローレンツ曲線との間の面積」を、「完全平等線の下の面積（これは常に1/2である )」で標準化した比率**として定義できる.
したがって、ジニ指数は、**完全平等な社会と、富や所得の各レベルで観察される社会との間のギャップを示す指標**である。

### Gini index 及びローレンツ曲線の算出

1969年のローレンツ曲線は、まず、各観測値より下にある郡の人口の割合を計算することによって作成できる。そのために、累積系列を生成する。

```python
n = len(pci_df)
share_of_population = numpy.arange(1, n + 1) / n
```

次に、所得の累積的な推移を考える。そのためには、総所得のうち、各人口が所有する割合がどの程度かを調べる必要がある。経験的に、これは次のような方法で計算することができる。まず、郡の所得を分類する。

```python
incomes = pci_df["1969"].sort_values()
```

第二に、各データポイントで蓄積された所得の全体的な割合を求める。そのために、各県の所得が全体の何パーセントを占めているかを計算する。

```python
shares = incomes / incomes.sum()
```

これらのシェアの累積和（現在のものまでのすべての所得シェアの合計を反映したもの）を構築する。

$$
CunSum(v, k) = \sum_{i=1}^{k}v_i
$$

これは0から始まり、最後のシェアが含まれると1になる。

```python
cumulative_share = shares.cumsum()
```

これによって、ローレンツ曲線と完全平等線の両方をプロットすることができる。

```python
# Generate figure with one axis
f, ax = plt.subplots()
# Plot Lorenz Curve
ax.plot(share_of_population, cumulative_share, label="Lorenz Curve")
# Plot line of perfect equality
ax.plot((0, 1), (0, 1), color="r", label="Perfect Equality")
# Label horizontal axis
ax.set_xlabel("Share of population")
# Label vertical axis
ax.set_ylabel("Share of income")
# Add legend
ax.legend()

plt.show()
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_35_0.png)

青い線は1969年の郡の所得に関するローレンツ曲線である。
ジニ指数は、これと赤で示した45度の平等線との間の面積を、すべて平等線の下の面積で標準化したものである。

### ローレンツ曲線を時系列で算出していく

**不平等がどのように変化してきたか**を調べる最初のアプローチは、各年度のローレンツ曲線をプロットすることである。Pythonでこれを行う1つの方法は、任意の所得のセットに対してローレンツ曲線を計算する関数を作成することです。以下の関数は、上記のステップを一発でカプセル化したものです。

```python
def lorenz(y):
    y = numpy.asarray(y)
    incomes = numpy.sort(y)
    income_shares = (incomes / incomes.sum()).cumsum()
    N = y.shape[0]
    pop_shares = numpy.arange(1, N + 1) / N
    return pop_shares, income_shares
```

例えば1969年という単一の年について、この関数はローレンツ曲線プロットの各軸に対応する2つの配列からなるタプルを返すだろう。

```python
lorenz(pci_df["1969"])

>>(array([3.25097529e-04, 6.50195059e-04, 9.75292588e-04, ...,
        9.99349805e-01, 9.99674902e-01, 1.00000000e+00]),
 array([1.22486441e-04, 2.52956561e-04, 3.83636778e-04, ...,
        9.98429316e-01, 9.99176315e-01, 1.00000000e+00]))
```

ここで、上記と同じ方法で、データセットに含まれるすべての年のローレンツ曲線を計算することができる。

```python
lorenz_curves = pci_df[years].apply(lorenz, axis=0)
```

実際には、各年度の列を持つデータフレームとなる。行には人口シェア（または所得シェア）がリストとして格納される。そして、このデータフレームの列（年）に対して反復処理を行い、各年のローレンツ曲線のプロットを作成することができる。

```python
# Set up figure with one axis
f, ax = plt.subplots()
# Plot line of perfect equality
ax.plot((0, 1), (0, 1), color="r")
# Loop over every year in the series
for year in lorenz_curves.columns:
    # Extract the two arrays or each dimension
    year_pop_shares, year_inc_shares = lorenz_curves[year].values
    # Plot Lorenz curve for a given year
    ax.plot(year_pop_shares, year_inc_shares, color="k", alpha=0.05)
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_43_0.png)

**ローレンツ曲線を比較するだけでは不平等の時間的なパターンを確認することは困難**である。
ジニ係数に明確に注目することで、不平等の時間的な進化をより明らかにすることができるだろう。

### Gini Indexを時系列で算出していく

ジニ係数は、ローレンツ曲線と完全平等の曲線との間の面積を表していることを思い出してください。この指標は、`inequality`モジュールにおける`Gini`クラスを通して直接計算することができる。1969年の場合、これは次のことを意味する。

```python
g69 = inequality.gini.Gini(pci_df["1969"].values)
```

係数を抽出するために、g69の`g`プロパティを取得する。

```python
g69.g
>>0.13556175504269904
```

ここで、1969年のジニ係数は0.13である。これをすべての年について計算するためには、これまでと同様のパターンを用いることができる。まず、関心のある量を計算する関数を定義し、次に、その関数をすべての年の表全体に適用する。

```python
def gini_by_col(column):
    return inequality.gini.Gini(column.values).g
```

`inequality`のGiniは、`pandas.Series`オブジェクトではなく、`numpy.ndarray`を必要とし、`values`属性を通して取り出すことができます。これは`Gini`クラスに渡され、我々は`DataFrame`オブジェクトとして係数の値のみを返します。

```python
inequalities = (
    pci_df[years].apply(gini_by_col, axis=0).to_frame("gini")
)
```

この結果、各年度のジニ値のシリーズが出来上がる。
これは、標準的なパンダのプロットにより、グラフにすることができます。結果のパターンは、上記の20:20の比率のものと似ています。

```python
inequalities.plot(figsize=(10, 3));
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_55_0.png)

## Theil's Index

3番目によく使われる不等式の尺度は、次のように与えられるTheilのT [MM21]である。

$$
T = \sum_{i}^{m}(
  \frac{y_i}{\sum_{i=1}^{m}y_i}
  \ln{(m\frac{y_i}{\sum_{i=1}^{m}y_i})}
  )
$$

ここで、$y_i$ は m 地域中の i 地域における一人当たり所得である。
概念的には、この指標は所得分布のエントロピーに関連しており、所得が人口全体にどれだけ均等に分布しているかを測定する。

Theil指数はPysalの`inequality`モジュールでも利用できるので、上記と同様のアプローチで各年について計算することができる。

```python
def theil(column):
    return inequality.theil.Theil(column.values).T

inequalities["theil"] = pci_df[years].apply(theil, axis=0)
```

そして、その経年変化を視覚的に比較生成する。

```python
inequalities["theil"].plot(color="orange", figsize=(10, 3));
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_59_0.png)

## Gini Index と Theil's Indexの比較

ジニ係数とテイル係数の時間推移を見ると、非常によく似ているように見える。
このことは、一見すると、両指標が互いに代替関係にあることを示唆している。
しかし、両者をプロットしてみると、完全には相関がないことがわかる。

```python
_ = seaborn.regplot(x="theil", y="gini", data=inequalities)
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_61_0.png)

実際、後述するように、**各インデックスは、補完的に機能する特定の空間拡張に適した特性を持っている**。
**全体像を把握するためには、両方（そしてそれ以上）が必要**なのです。

# Personal Versus Regional Income

個人所得不平等と地域所得不平等の研究には、微妙な、しかし重要な違いがある。これを見るためには、まず、2つのタイプの不平等の関係を表現する必要がある。

N人の個人が$m$個の地域に分布している国を考えてみよう。
個人$l$の所得を$Y_l$とすると、地域全体の個人所得は$Y_i=\sum_{l \in i}Y_l$、地域iの一人当たり所得は$y_i= \frac{Y_i}{N_i}$となる。
ここで、$N_i$ は地域の個人数である。

国民レベルでは、所得の変動係数を対人所得格差の指標とすることができる。これは、次のようになる。

# Spatial Inequality

地域別所得格差の分析は、空間的な単位に着目する点で、全国的な対人所得格差の分析とは異なっている。
**地域所得は明示的に地理的空間に埋め込まれている**ので、その空間的構成を利用することで、不平等の本質をより深く知ることができる。
地域的不平等に関する文献では、これは多くの方法でアプローチされてきた。
本章では、6章と7章の空間的自己相関の議論とリンクさせたもの、グローバルな指標を地域的に分解したものに基づくもの、そして従来のグローバルな指標に空間を埋め込んだものの**3つ**を検討した。

## Spatial Autocorrelation

このアプローチは、地域所得データの空間的パターンの特性を明らかにするのに役立つ。ここで、本書の冒頭で紹介した空間的自己相関のグローバルな測定に戻る。このアプローチの本質は、所得の空間分布がどの程度空間的に集中しているかを調べることである。このために、Queen Spatial Weight Matrixを用い、サンプル中の各年についてMoranのIを計算する。

```python
wq = weights.Queen.from_dataframe(pci_df)
```

関数を「ブロードキャスト」するのと同じパターンで、各統計値から必要な結果を返す関数を作成します。ここでは、第6章で見たように、所得が地理的にランダムに分布しているという帰無仮説のもとで、指数が統計的に有意であるかどうかを識別するのに役立つモラン統計量の擬似p値も残しておく。

```python
def moran_by_col(y, w=wq):
    mo = esda.Moran(y, w=w)
    mo_s = pandas.Series(
        {"I": mo.I, "I-P value": mo.p_sim},
    )
    return mo_s
```

今回、この関数はSeriesオブジェクトを返すので、それをapplyに渡すと、うまくフォーマットされた表が得られます。

```python
moran_stats = pci_df[years].apply(moran_by_col, axis=0).T

moran_stats.head()
```

さらに比較のため、上で作成していた`inequalities`変数に結果を添付した。

```python
inequalities = inequalities.join(moran_stats)
```

```python
inequalities[["I", "I-P value"]].plot(subplots=True, figsize=(10, 6))
plt.show()
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_76_0.png)

その詳細を見る前に，ジニ指数とTheil指数が同様の経路を辿っているのに対して，**MoranのIは明確な軌跡を描いている**ことに注目したい。

- これは、**一人当たりの所得が近隣の県との間であまり変わらなくなっていること**、また、格差が大きいか小さいかにかかわらず、一貫して減少していることを示唆している。
- 第二に、このように低下しているにもかかわらず、**空間的自己相関が統計的に有意でない年はない**。
  - =>つまり、**地域所得の分布には強い地理的構造があり**、不平等の問題に注目する際には、それを説明する必要がある。

## Regional Decomposition of Inequality

- 総体としての不平等の分析に対する一般的な反論の一つは、不平等が最も重要である規模についての詳細の欠如に関連している。
- **不平等は、同じような個人間の所得の差ではなく、グループ間の差によって引き起こされる可能性があります**。
- つまり、観察された不平等が、年齢、性別、教育などの交絡変数によって「説明」される可能性が常に存在するのである。

  - 例えば、高齢者と若年者の所得差は、社会的な富の不平等の大部分を「説明」できる。
  - 高齢者は経験を積むのにはるかに時間がかかるため、一般にその経験に対してより多くの報酬が支払われる。
  - 年配者は経験を積むのに時間がかかるため、その分給料も高くなる。若い人は経験が少ないため、（平均して）年配者よりも所得が低くなる。

- この問題に取り組むためには、不平等指標を構成するグループに分解することがしばしば有効である。
  - これにより、不平等がどの程度、集団の総体的な差異によってもたらされ、どの程度、観測レベルの不平等によってもたらされているかを理解することができます。
  - また、各グループがどの程度不平等であるかを個別に把握することができます。
  - 地理的なアプリケーションでは，これらのグループは，通常，空間的に定義され，地域はオブザベーションの連続した地理的グループである [SW05]．
  - このセクションでは，不平等の研究に地理を導入する方法として，地域の不平等分解を議論する．

これらのアイデアを所得データセットで説明しよう。この表では、Region変数に郡が属するUnited States Census Bureauの地域が記録されている。これらは国土を8つの地域に分割し、それぞれに以下に示すような名前に関連する番号を割り当てている。

```python
region_names = {
    1: "New England",
    2: "Mideast",
    3: "Great Lakes",
    4: "Plains",
    5: "Southeast",
    6: "Southwest",
    7: "Rocky Mountain",
    8: "Far West",
}
```

まず地域名と地域番号を対応させ、質的なチョロプレスをレンダリングすることで、凡例の地域名を視覚化することができる。

```**python**
ax = pci_df.assign(Region_Name=pci_df.Region.map(region_names)).plot(
    "Region_Name",
    linewidth=0,
    legend=True,
    categorical=True,
    legend_kwds=dict(bbox_to_anchor=(1.2, 0.5)),
)
ax.set_axis_off();
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_80_0.png)

地域ごとの所得の変化をピークに見てみよう。そのためには、県を地域ごとにグループ化し、その平均を計算し、表にまとめるという分割-適用-結合のパターンを適用すればよい。

```python
rmeans = (
    pci_df.assign(
        # Create column with region name for each county
        Region_Name=pci_df.Region.map(region_names)
    )
    .groupby(
        # Group counties by region name
        by="Region_Name"
        # Calculate mean by region and save only year columns
    )
    .mean()[years]
)
```

この表は、地域ごとに1行、年ごとに1列で構成されている。これらの平均値を視覚化することで、その時間的な軌跡を知ることができる。

```python
rmeans.T.plot.line(figsize=(10, 5));
```

![](https://geographicdata.science/book/_images/09_spatial_inequality_84_0.png)

## Spatializing Classic Measures

# Conclusion
