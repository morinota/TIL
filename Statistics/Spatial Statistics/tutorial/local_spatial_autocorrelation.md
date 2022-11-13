## 0.1. Reference

- https://geographicdata.science/book/notebooks/07_local_autocorrelation.html
- [Contagion, Spillover and Interdependence](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1975.en.pdf)
- [データセット](https://www.data.gov.uk/dataset/be2f2aec-11d8-4bfe-9800-649e5b8ec044/eu-referendum-results)

# 1. Local Spatial Autocorrelation

## 1.1. Intro

前章では、Spatial AutocorrelationのGlobalな測定が、「対象となる現象の全体的な空間分布が**地理的にランダムなプロセスに適合しているかどうか**」を判断するのに役立つことを探った。

**Spatial Autocorrelationの有無**は、その後の統計解析に重要な意味を持つ。

- 1. Spatial Autocorrelationは、**近くの場所のある値の間に関連性を生み出すプロセス**の動作を反映している可能性がある。
  - これは、ある地点での結果が他の地点に影響を与える"**Spillover(波及)**"を表している可能性もあるし、
  - ある地点での結果が他の地点に因果的に影響を与える"**Contagion(伝染)**"を表している可能性もある。
  - 両者の違いがいまいち分からない...??
    - Spilloverの強いVer.がContagion...?
- 2. また後述するように、**単に系統的(Systematic)な空間変動(Spatial Variation)**（あるいは、ここでは「**不均質性(Heterogeneity)**」と呼ぶことにする）の結果である可能性もある。
  - ＝要するに、「SpilloverやContagionの効果はなく、単なる分布の形として偏りがある」みたいな意味？
- 3. また、Spatial Autocorrelationは**データの測定や処理に起因**することもある。
  - この場合、依存性は実質的なプロセスによるものではなく、非ランダムなノイズの一形態である。
  - ## 例えば、地理的データを「ダウンサンプリング」すると、同じ値の大きなパッチができることがある。
  - これは、実質的なAutocorrelationではなく、補間(Interpolation)のアーチファクト(artifacts)に過ぎないかもしれません。

Spatial Autocorrelationが**Substantive(実質的、Spilloverなどがある)なものかNuisance(=厄介なノイズ？)なものかには関係なく、統計解析を複雑にする非ランダム性の一形態である**ことは確かです。

これらの理由から、**地理的に参照されるデータセットにSpatial Autocorrelationが存在するかどうかを判断する能力**は、Geographical Data Scienceのツールボックスの重要な要素である。

## 1.2. Spatial AutocorrelationのGlobalな測定の限界

Spatial AutocorrelationのGlobalな測定は、その重要性にもかかわらず、**「マップ全体」の統計**である。つまり、データセット全体に対する**単一の要約**なのです。

- 例えば、Moran's Iは、データセットを地理的なクラスタリング(=グルーピング)、または負の場合は分散（ばらつき具合）の程度をとらえた単一の値に要約するのに適したツールです。
- しかし、Moran's Iはマップ内の特定のタイプの値（例えば、高い、低い）が集まっているエリアや、明確な分散のインスタンスを示すものではない。
- つまり、Moran's Iは、**マップ内の値が全体的に集まっているか（または分散しているか）**を示すことはできますが、特定のクラスタ（または外れ値）がどこにあるかについては教えてくれません。

## 1.3. そこでSpatial AutocorrelationのLocalな測定

Spatial AutocorrelationのLocalな測定は、地図全体にわたるこれらの関係の**単一の要約を提供するのではなく、各Observationとその周囲の関係に焦点を当てる**。
この意味で、それらはSummary Statisticsではなく、データ中の空間構造についてより多くを学ぶことを可能にするスコアである。

しかし、Metrics(方法論)の背後にある一般的な概念(intuition)は、Globalな測定と同様である。
また、Globalな指標を**Localな指標の集合に分解**することで、数学的なつながりを持つ指標もある。

その例として、"**LISA(Local Indicators of Spatial Association)**"がある。
これを用いてLocal Spatial Autocorrelationの理解を深め、この章の大部分をこれに費やしている。

このような概念が固まったところで、補完的な情報を提供する、あるいはカテゴリーデータに対して同様の洞察を得ることを可能にする2つのAlternative Statistics(代替統計量)を紹介する。
これらの統計量はGeo-Tables(=テーブルデータ＋座標？)で表現されたデータに対して使用されることが非常に多いが，この2つを基本的に結びつけるものはない。
実際、これらの方法を大規模なsurfaces(??)に適用することは、将来有望な分野である。
そのため、本章の最後に、サーフェスとして保存されたデータに対してこれらの統計量をどのように実行できるかを説明する。

# 2. An empirical illustration: the EU Referendum

# 3. Motivating Local Spatial Autocorrelation

Local Spatial Autocorrelationの背景をよりよく理解するために、グラフツールとしてのMoran Plotに戻る。
この文脈では、**空間構造の類型をより簡単に見分ける**ことができるように、標準化された形式でデータを表現することがより直感的である。
まず、我々の関心のある変数のSpatial Lagを計算しよう。

```python
db["w_Pct_Leave"] = weights.spatial_lag.lag_spatial(
    w, db["Pct_Leave"]
)
```

そして、平均値を引き、標準偏差で割ったそれぞれの標準化バージョン。
(標準偏差で割り忘れてない??)

```python
db["Pct_Leave_std"] = db["Pct_Leave"] - db["Pct_Leave"].mean()
db["w_Pct_Leave_std"] = db["w_Pct_Leave"] - db["Pct_Leave"].mean()
```

技術的に言えば、Moran Plotの作成は、他の散布図の作成と非常によく似ています。

```python
# Setup the figure and axis
f, ax = plt.subplots(1, figsize=(6, 6))
# Plot values
seaborn.regplot(
    x="Pct_Leave_std", y="w_Pct_Leave_std", data=db, ci=None
);
```

![](https://geographicdata.science/book/_images/07_local_autocorrelation_19_0.png)

- 標準化値を用いると、各変数（離脱票の割合とそのSpatial Lag）を、正の標準化値を持つ平均以上の離脱票のグループと、負の標準化値を持つ平均以下の離脱票のグループにすぐに分けることができる。
- この考え方を離脱率とSpatial Lagに適用すると、**Moran Plotは4つの象限に分けられる**。
  - それぞれの象限は、元の変数（Pct_Leave）またはそのSpatial Lag（w_Pct_Leave_std）のいずれかにおいて、**与えられたエリアが平均より高い値（high）または低い値（low）を示しているかどうか**に基づいて状況を把握することができます。
  - この用語を使って、4つの象限を次のように名付ける：右上はハイハイ（HH）、左上はローハイ（LH）、左下はローロー（LL）、右下はハイロー（HL）である。
  - グラフにすると、次のように捉えることができる。

```python
# Setup the figure and axis
f, ax = plt.subplots(1, figsize=(6, 6))
# Plot values
seaborn.regplot(
    x="Pct_Leave_std", y="w_Pct_Leave_std", data=db, ci=None
)
# Add vertical and horizontal lines
plt.axvline(0, c="k", alpha=0.5)
plt.axhline(0, c="k", alpha=0.5)
# Add text labels for each quadrant
plt.text(20, 5, "HH", fontsize=25, c="r")
plt.text(12, -11, "HL", fontsize=25, c="r")
plt.text(-20, 8.0, "LH", fontsize=25, c="r")
plt.text(-25, -11.0, "LL", fontsize=25, c="r")
# Display
plt.show()
```

![](https://geographicdata.science/book/_images/07_local_autocorrelation_21_0.png)

# 4. Local Moran's I_i

## 4.1. Moral PlotをLocal Spatial Autocorrelationの観点から見る...

上の図を見る1つの方法は、データセットの各観測値を、その値とその近傍の値によって分類すること(??)である。さらに、この分類は網羅的です：

- すべての点にラベルが割り当てられています。
- しかし、Localな測定は、値の異常な集中の領域を識別するのに役立つことを覚えておいてください。
- クラスターは、Spatial Randomnessの仮定のもとでは現れにくい1つのタイプの値を表します。
  - 各場所がある種の統計的に有意なクラスターに属しているかどうかを知るには、したがって、**データが完全にランダムな方法で空間に割り当てられた場合に予想されるものと比較**する必要があります。
- しかし、私たちが注目するのは、**値が集中する強さが異常に高いかどうか**です。
  - LISAはまさにこれを目指して設計されているのです。
  - LISAの統計的な基礎についての詳しい説明は、この章の範囲外。

LISA統計の1つであるLocal Moran's Iで、それらがどのように機能するかについて直観的に説明する。

## 4.2. Local Moran's I_iの定義と概念

Local Moran's Iの中核となる考え方は、**あるObservationの値とその周囲の平均**が、**純粋な偶然から期待されるより**も、**より類似している**か（上の散布図ではHHまたはLL）、**または非類似**である（HL、LH）ケースを識別することである。

これを行うメカニズムは、GlobalなMoran's Iのものと似ていますが、この場合、**各Observationに適用**されます。
＝＞これは，**オリジナルのObservationと同じ数の統計量**になります。
統計量の形式的表現は，次のように書くことができる：

$$
I_i = \frac{z_i}{m_2}
\sum_{j} w_{ij} z_{j} \\
m_2 = \frac{\sum_{i} z_i^2}{n}
\tag{1}
$$

ここで、

- $m_2$:サンプルデータの値の分布の二次モーメント(=分散)
- $z_i = y_i - \bar{y}$
- $w_{ij}$: Observation $i$と$j$のペアのSpatial Weight
- $n$：Observationの数。

## 4.3. LISAにおけるLocal Moran's Iの位置付け

LISA(Local Indicators of Spatial Association)は、値の地理的なクラスターを特定したり、地理的な外れ値を見つけるために、多くの分野で広く使用されています。

LISAは、値が集中している領域を迅速に返したり、機能している可能性のあるプロセスに関する示唆的な証拠を提供したりすることができる便利なツールである。
このような理由から、LISAはGeographical Data Scienceのツールボックスの中で重要な位置を占めている。

他の多くのApplication(適用事例)の中で、LISAは貧困の地理的クラスターの特定[DSSC18]、民族の飛び地のマップ[JPF10]、特に高い/低い経済活動の領域の定義[TPPGTZ14]、または伝染病のクラスターの特定[ZRW+20]に使用されている。
Local Moran's I統計量は、多くの異なるタイプの空間データに使用できる多種多様なLISAの1つに過ぎない。

## 4.4. esdaモジュールによるLISA統計量の推定

Pythonでは、esdaのおかげで非常に合理的な方法でLISAを計算することができる。Local Moran's I統計量を計算するために、Moran_Local関数を使用します。

```python
lisa = esda.moran.Moran_Local(db["Pct_Leave"], w)
```

関数実行時には、引数として、興味のある変数（この文脈では離脱票の割合）と、データセットを構成する異なるエリア間の近隣関係を記述するSpatial Weight Matrixを渡す必要があります。
この関数はLISAオブジェクト(`lisa`)を作成し、そのオブジェクトにはいくつかの属性があります。Local指標は`Is`属性にあり、seabornを使ってその分布を知ることができる。

```python
# Draw KDE line
ax = seaborn.kdeplot(lisa.Is)
# Add one small bar (rug) for each observation
# along horizontal axis
seaborn.rugplot(lisa.Is, ax=ax)
```

![](https://geographicdata.science/book/_images/07_local_autocorrelation_26_0.png)

## 4.5. Local Moran's Iの分布から分かる事

この図から、Local Moran's I統計量の分布は、かなり歪んでいることがわかる。この結果は、Spatial Association(=Autocorrelationではない？？)の正の形が優勢であるためで、Local Moran's I_i統計量のほとんどが正であることを意味している。
ここで重要なことは、「**高い正の値は空間における値の類似性から生じる**」ということであり、これは**高い値が高い値の隣にあるか、低い値が低い値の隣にあるかのどちらか**である。
Local Moran's Iの値だけでは、この2つのケースを区別することはできない。

密度の左端の値は、負のSpatial Association(=Autocorrelationではない？？)を示す場所を表す。
この場合、**高い値が低い値に囲まれている場合と、低い値が高い値の近隣のオブザベーションに囲まれている場合の2つ**の形態がある。
そして、再び、このLocal Moran's I統計量は2つのケースを区別することができない。

## 4.6. LISAの性質と、Choroplethとの相性

```python
from splot import esda as esdaplot
```

```python
# Set up figure and axes
f, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))
# Make the axes accessible with single indexing
axs = axs.flatten()

# Subplot 1 #
# Choropleth of local statistics
# Grab first axis in the figure
ax = axs[0]
# Assign new column with local statistics on-the-fly
db.assign(
    Is=lisa.Is
    # Plot choropleth of local statistics
).plot(
    column="Is",
    cmap="plasma",
    scheme="quantiles",
    k=5,
    edgecolor="white",
    linewidth=0.1,
    alpha=0.75,
    legend=True,
    ax=ax,
)

# Subplot 2 #
# Quadrant categories
# Grab second axis of local statistics
ax = axs[1]
# Plot Quandrant colors (note to ensure all polygons are assigned a
# quadrant, we "trick" the function by setting significance level to
# 1 so all observations are treated as "significant" and thus assigned
# a quadrant color
esdaplot.lisa_cluster(lisa, db, p=1, ax=ax)

# Subplot 3 #
# Significance map
# Grab third axis of local statistics
ax = axs[2]
#
# Find out significant observations
labels = pandas.Series(
    1 * (lisa.p_sim < 0.05),  # Assign 1 if significant, 0 otherwise
    index=db.index  # Use the index in the original data
    # Recode 1 to "Significant and 0 to "Non-significant"
).map({1: "Significant", 0: "Non-Significant"})
# Assign labels to `db` on the fly
db.assign(
    cl=labels
    # Plot choropleth of (non-)significant areas
).plot(
    column="cl",
    categorical=True,
    k=2,
    cmap="Paired",
    linewidth=0.1,
    edgecolor="white",
    legend=True,
    ax=ax,
)


# Subplot 4 #
# Cluster map
# Grab second axis of local statistics
ax = axs[3]
# Plot Quandrant colors In this case, we use a 5% significance
# level to select polygons as part of statistically significant
# clusters
esdaplot.lisa_cluster(lisa, db, p=0.05, ax=ax)

# Figure styling #
# Set title to each subplot
for i, ax in enumerate(axs.flatten()):
    ax.set_axis_off()
    ax.set_title(
        [
            "Local Statistics",
            "Scatterplot Quadrant",
            "Statistical Significance",
            "Moran Cluster Map",
        ][i],
        y=0,
    )
# Tight layout to minimise in-betwee white space
f.tight_layout()

# Display the figure
plt.show()
```

その性質上、LISAの数値結果を見ることは、LISAが提供できるすべての情報を利用する上で、必ずしも最も有用な方法とは言えない。

**LISAの場合、データ中のすべての観測値に対して統計量を計算している**ので、もし多くの観測値があれば、**意味のあるパターンを抽出することは困難**であることを思い出してください。

**このような場合、Choroplethが役に立ちます**。

- 一見すると、これは値のコレオプスが空間分布を可視化するのに有効な方法であることを示唆しているように見えるかもしれません。
- 下図の**左上のパネル**にそのような地図がありますが、この地図では、**地域の関連性がポジティブ（HH/LL）かネガティブ（HL/LH）かはわかります**。
  - しかし例えば、スコットランドの黄色い地域と東部の黄色い地域の集まりが似ているかどうか(すなわちHHかLLかの違い)は、わからないのです。
  - この2つは空間的な関連性のパターンが似ているのか、それとも一方がHHでもう一方がLLなのでしょうか。
- また、ゼロ付近の値は統計的に有意でないことが分かっている。
  - ＝＞すなわちLocal Moran's I_iが0付近のObservationは、周囲と正or負のSpatial Autocorrelationがあるとはいえない＝Spatial Randomnessの仮定を棄却できない、といえる。
- したがって、どのLocal statisticが有意で、どLocal statisticが統計学的に有意でないのでしょうか？
- 言い換えれば、どれが統計的なクラスターで、どれが単なるノイズと言えるのでしょうか？

![](https://geographicdata.science/book/_images/07_local_autocorrelation_31_0.png)

紫色(負のAutocorrelation)と黄色(正のAutocorrelation)の場所は、Local statisticの絶対値（正と負の値）が最大であることを示している。しかし黄色の場所に関して、これは正のSpatial Autocorrelationを意味し、その値は高くも低くもなりうることを忘れてはならない。このため、この地図ではBrexit投票への支持率が低い地域と高い地域の区別がつかない。

この2つのケースを区別するために、右上の地図は**Moran PlotにおけるLISA統計量の象限内の位置**を示している。これは、正の（または負の）Localな関連が、High-High象限など特定の象限内に存在するかどうかを示しています。この情報は、`lisa`オブジェクトの`q`属性に記録されます。

```python
lisa.q[:10]
=> array([1, 1, 1, 1, 1, 1, 4, 1, 4, 1])
```

`q` 属性の数字と実際の象限との対応は次のとおりである．1はHH象限、2はLH象限、3はLL象限、4はHL象限にある観測値を表す。
上段の2つのマップを比較すると、スコットランドの正の地方連合はBrexitの支持率が低く、南部の正の地方連合はBrexitを強く支持する自治体の間であることがわかる。
全体として、各象限に属する地域のカウントを以下のように求めることができる。

```python
counts = pandas.value_counts(lisa.q)
counts

=>
1    183
3    113
2     50
4     34
dtype: int64
```

## 4.7. Local な統計量の統計的有意性を考慮する必要がある話

上の結果は、high-high(1)とlow-low(3)が優勢であることを示している。

しかし、この**最初の2つのマップの解釈には注意が必要**である。
＝＞なぜなら、Localな値の**基本的な統計的有意性は考慮されていないから**である。
このマップでは、LISAの生の値と局所的な統計値が存在する象限を単純に対応させただけである。

統計的有意性については、左下の地図で、擬似p値(**Pseudo p-value**)がこの文脈で用いる閾値5%以上（「有意でない」）または以下（「有意である」）のポリゴンを区別しています。
このマップを見ると、かなりの数の地方自治体が、純粋な偶然と見なせるほど小さな統計値を有している(=すなわち、Local Spatial Autocorrelationが存在するとはいえない＝Spatial Raodomnessの仮定を棄却できない)ことがわかる。

## 4.8. なので、Cluster Mapを作る！！

＝＞したがって、**最も有望な領域に焦点を当てるために、象限とLocal統計量と一緒に有意性情報を含める必要があります**。

なので一緒に、この "**Cluster Map**"（**右下図**）は、有意なObservation-純粋な偶然から来たとはとても思えない-を抽出し、それらの象限カテゴリーに応じた特定の色でプロットします。
必要な部品はすべて上で作成した `lisa` オブジェクトの中にあり、関連する地理を含む `geo`テーブルと一緒に渡すと、`splot` はCluster Mapを作成します。

このCluster Mapを読むと、他のマップだけでは把握しにくい、データ分析により適した興味深い側面がいくつか見えてくる。

- 第一に、純粋な偶然という考えを否定できるほど強いLocal Spatial Autocorrelationを持つポリゴンが半分以下であること。
  - `(lisa.p_sim < 0.05).sum() * 100 / len(lisa.p_sim)`=>`41.578947368421055`
  - この分析では、41％強の自治体が空間的なクラスター(Spatial Autocorrelationが存在している、と言えそうなグループ)に属していると考えられる。
- 第二に、EU 離脱支持率が低い地域が明確に 3 つあることがわかる。
  - スコットランド、ロンドン、オックスフォード周辺（ロンドン北西部）である。
- 第三に、支持率の高い地域が集中しているように見えるが、イングランド北東部と西部の地域だけが、空間的な集中が強く、純粋な偶然性を合理的に排除している。

## 4.9. 一旦寄り道：Cluster Map作成時のdata engineeringについて。Local Moran's Iの統計的検定の中身とか。

LISA統計から話を進める前に、有意水準やその他の情報を「エクスポート」するために必要なデータ工学について少し触れ、これらの数値が何を表しているのかについてもう少し掘り下げてみましょう。
後者は、より広範なデータパイプラインの一部としてそれらを扱う必要がある場合に有用である。

- これまでのところ、Cluster Mapは`splot`によって処理されてきましたが、フードの下ではかなりのことが起こっています。
- もしそのマップを再作成したり、この情報を別の文脈で使ったりする必要があれば、lisaオブジェクトからそれらを取り出して、元のデータベーステーブルにリンクする必要があります。
- 以下は一つの方法です。(Cluster Map作成時の処理の中身の部分)

(中身はあとで書く！)
このことから、ほとんどの地域別統計は統計的に有意ではないことがわかる。統計的に有意なものでは、ドーナツやダイヤモンド・イン・ザ・ラフよりもホットスポットやコールドスポットの方が多いことがわかる。これは、先ほどの地域別統計の分布に見られた歪みと一致している。

# 5. Getis and Ord’s local statistics

Globalの場合と同様に、Local Moran's I以外にもSpatial Autocorrelationの度合いを表す指標があります。

`esda`には**Getis and Ord's $G_i$-type statistic**が含まれています。これらは異なる種類のLocal statisticであり、一般的に２つの形式で使用される。

- 一つ目：**$G_i$ statistic**. Local Summary(局所的な要約)にサイトでの値(各Observation自身の値？)を省略した統計量。
- ２つ目：**$G_i^*$ statistic**. Local Summaryにサイト自身の値を含む統計量
- また、その計算方法も上記のLocal Moran's I statisticと同様のパターンになる。Brexitの例でどのように見えるか見てみましょう。

```python
# Gi
go_i = esda.getisord.G_Local(db["Pct_Leave"], w)
# Gi*
go_i_star = esda.getisord.G_Local(db["Pct_Leave"], w, star=True)
```

Local統計量なので地図上にプロットして探索するのが一番良い。しかし、LISAとは異なり、**G統計量はPositive Spatial Autocorrelationしか特定できない**。標準化すると、正の値は高い値の集まり(＝つまりHot spot！)を意味し、負の値は低い値の集まり(＝Cold Spot！)を意味する。残念ながら、空間的な外れ値(Outlier)を識別することはできない。

LISA とは異なり、`splot` は現時点では G 統計量の視覚化をサポートしていません。その出力を視覚化するために、代わりに統計量の出力オブジェクトとそれに関連するジオメトリのセットからマップを生成する小さな関数を書くことになります。

```python
def g_map(g, db, ax):
    """
    Create a cluster map
    ...

    Arguments
    ---------
    g      : G_Local
             Object from the computation of the G statistic
    db     : GeoDataFrame
             Table aligned with values in `g` and containing
             the geometries to plot
    ax     : AxesSubplot
             `matplotlib` axis to draw the map on

    Returns
    -------
    ax     : AxesSubplot
             Axis with the map drawn
    """
    ec = "0.8"

    # Break observations into significant or not
    sig = g.p_sim < 0.05

    # Plot non-significant clusters
    ns = db.loc[sig == False, "geometry"]
    ns.plot(ax=ax, color="lightgrey", edgecolor=ec, linewidth=0.1)
    # Plot HH clusters
    hh = db.loc[(g.Zs > 0) & (sig == True), "geometry"]
    hh.plot(ax=ax, color="red", edgecolor=ec, linewidth=0.1)
    # Plot LL clusters
    ll = db.loc[(g.Zs < 0) & (sig == True), "geometry"]
    ll.plot(ax=ax, color="blue", edgecolor=ec, linewidth=0.1)
    # Style and draw
    contextily.add_basemap(
        ax,
        crs=db.crs,
        source=contextily.providers.Stamen.TerrainBackground,
    )
    # Flag to add a star to the title if it's G_i*
    st = ""
    if g.star:
        st = "*"
    # Add title
    ax.set_title(f"G{st} statistic for Pct of Leave votes", size=15)
    # Remove axis for aesthetics
    ax.set_axis_off()
    return ax
```

この関数があれば、G統計量のクラスターマップの生成は、splotを用いたLISA出力と同様に簡単です。

```python
# Setup figure and axes
f, axs = plt.subplots(1, 2, figsize=(12, 6))
# Loop over the two statistics
for g, ax in zip([go_i, go_i_star], axs.flatten()):
    # Generate the statistic's map
    ax = g_map(g, db, ax)
# Tight layout to minimise blank spaces
f.tight_layout()
# Render
plt.show()
```

![](https://geographicdata.science/book/_images/07_local_autocorrelation_52_0.png)

- この場合、G_i と G_i^\* ではほぼ同じ結果になります。
- また，一見すると，これらのマップは上の最終的なLISAマップと視覚的に似ているように見える。
- 当然ながら、これは「**なぜG_iの統計量を全く使わないのか**」という疑問につながります。
  - この疑問に対する答えは、**Local I statisticとLocal G statisticという2つのLocal統計量のセットは、補完的な統計量である**ということです。
  - Local I統計量（それ自体）は、**クラスター／アウトライアの状態**を示しします。
    - ＝Local G統計量では分からない事！
  - LocalG_iは、観測値が**ホットスポット／コールドスポットのどちら側にあるか**を示します。
    - ＝Local I 統計量では分からない事！
- あるいは、LocalなMoran's Iクラスタ・マップは、上記の両方の情報を提供しますが、**一度にすべてを可視化するのはより難しいかも**しれません。
  - （＝前述した４つのコロプレスマップ）
  - したがって、それはあなたの分析の好みと手元の分析のポイントに依存します。

# 6. Bonus: local statistics on surfaces

# Conclusion

- Local Statistics(ここの意味は統計量?)は、Geographical Data ScienceのToolkitの中で最も一般的に使用されているツールの1つです。
- 適切に使用されれば、Local Statistics(統計量)は地理データの構造を分析・視覚化する強力な手段となる。
- Local Moran's I統計量は、Spatial Associationを表すLocal指標として、Observationとその近傍の環境との間の共変動(Co-variation)を要約するものである。
- 一方、Getis-Ord Local G 統計量は、各サイトの周辺領域の値の合計を比較するものである。
- いずれにせよ、Local統計量は多くの分析において最も一般的な「最初の筆」となる地理統計量であるため、効果的な使い方を学ぶことは、Geographical Data Scienceにとって重要である。
