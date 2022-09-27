## Link

- https://geographicdata.science/book/notebooks/08_point_pattern_analysis.html
- データソース
  - https://hucvl.github.io/visual-storygraphs/

# Pointデータ、Point Patternについて

## Pointデータの２種類の見方

Pointは空間的な実体であり、根本的に異なる2つの方法で理解することができる。

1. 一方は、「**Pointを空間的に固定された物体として捉え、その位置を所与のもの（外生的なもの）**とする」ものである。
   1. この場合、観測されるPointの位置は、そのPointで観測される値にとって二次的なものであると考えられる。
   2. 例えば、ある交差点を通過する車の数を計測するようなもので、**位置は固定されており、その位置で計測されたデータが注目される**。
   3. このようなPointデータの解析は、ポリゴンやラインといった他の空間データの解析と非常に似ている。
2. 一方、Pointでの観測は、地理的に連続したプロセスからの測定の場と考えることができる。
   1. この場合、**測定は理論的にはどこでも可能であるが、ある特定の場所でのみ実施された**、あるいは行われたことになる。
   2. 鳥の翼の長さを測定するようなものだと考えてください。
   3. **鳥が測定される場所は、鳥の移動と採餌という根本的な地理的プロセスを反映**しており、**鳥の翼の長さは、鳥によって異なる根本的な生態学的プロセスを反映しているかもしれない**のです。
   4. このようなアプローチは、**場所と測定の両方が重要**であることを意味する。

この章の残りの部分では、特に2の視点を採用することにする。

## Markedな/UnmarkedなPoint Pattern

- Pointを、複数の場所で起こりうるが、そのうちの数カ所でしか起こらない事象と見なしたとき、そのような事象の集まりをPoint Patternと呼ぶ。
  - この場合、Pointの位置は分析に必要な重要な要素の一つである。
- Point Patternの良い例は、ジオタグが付けられた写真である。
  - 技術的には多くの場所で起こりうるが、通常、写真はそのうちの一握りの場所にのみ集中する傾向があることがわかる。
  - Point Patternは、場所と一緒に多くの属性が提供される場合はマークされ、イベントが発生した場所の座標のみが提供される場合はマークされないことがあります。
  - 写真の例で言えば、撮影場所だけを分析対象とした場合はUnmmarkedなPoint Patternとなり、時間やカメラの機種、「画質スコア」などの他の属性が場所と一緒に提供された場合はMarkedなPoint Patternとなる。

# Point Pattern Analysis

## Introduction

Point Pattern Analysisは、Point Patternの可視化、記述、統計的特徴づけ、モデル化に関するもので、Observationデータを生じさせ、説明する生成過程を理解しようとするものである。この領域でよくある質問には次のようなものがある：

- What does the pattern look like?パターンはどのようなものか？
- What is the nature of the distribution of points?点の分布はどのような性質を持っているか？
- Is there any structure in the way locations are arranged over space? That is, are events clustered? or are they dispersed?空間上の位置の配置に構造はあるか？つまり、事象は集まっているのか、それとも分散しているのか？
- Why do events occur in those places and not in others?なぜその場所でイベントが発生し、他の場所では発生しないのか？

## ProcessとPatternの概念

このとき、ProcessとPatternという重要な区別を思い出すとよいでしょう。

- 「Process」は、私たちが最終的に観察する**結果を生み出すために働いている基本的なメカニズムに関するもの**である。
  - このメカニズムは抽象的であるため、**私たちは目にすることができません**。
  - しかし、多くの場合、「**ある現象を決定する要因は何か**」、そして「**その要因がどのように組み合わさって現象を生み出しているのか**」を知ることが、分析の重要な焦点となる。
  - この文脈では、Processは "方法 "と関連している。
- 一方、「Pattern」は、そのProcessの結果に関するものである。
  - 場合によっては、**PatternがProcessの唯一の痕跡**であり、**Processを再構築するための唯一のインプット**となる。
  - **Patternは直接的に観察可能**であり、間違いなく取り組みやすいものではあるが、**あくまでProcessの反映に過ぎない**。
  - 真の課題は、**Patternを特徴づけることではなく、Processを解明するためにそれ(Pattern)を利用すること**である。

## 本章の構成：

- 本章では、東京で撮影されたジオタグ付きのFlickr写真を通して、Point Patternを紹介します。
- ここでは、「**東京のどの場所でも撮影可能であるが、特定の場所だけが撮影されている**」というデータで表現される現象をイベントとして扱います。
  - このような東京の写真の捉え方は不変ではありません。
  - それらの場所を所与とし、「イベント」としての側面を無視してそれぞれの性質を見ることに意味がある場合も考えられます。
  - （＝＞これはPointデータの捉え方：その１の考え方！）
- しかし、ここでは、**場所と場所の集合的な形状に関連する質問に焦点**を当てます。
  - これらのツールを使うことで、意味不明なXY座標の長いリストを、特徴的な空間構造を持つ具体的な現象に変換し、Flickrユーザーのために**東京の観光スポットの中心、分散、集積に関する質問**に答えることができるようになります。

# The Tokyo photographs Dataset

## Overview

オンラインサービスにアップロードされたジオタグ付きの写真など、新しい形のデータの台頭は、研究者が都市を研究し理解するための新しい方法を生み出しています。人々はどこで写真を撮っているのか？いつ撮影されたのか？なぜ、ある場所には他の場所よりも多くの写真家が集まるのか？これらの疑問は、例えば、オンラインの写真ホスティングサービスをボランティア地理情報（VGI、[Goo07]）として考えたとき、単なるレトリック以上のものとなる。この章では、Flickrにアップロードされ、[100m Flickrデータセット](https://webscope.sandbox.yahoo.com/catalog.php?datatype=i&did=67)のおかげで抽出された地理参照画像のサンプルからメタデータを調査する。その際、点パターンの分布と特徴をより良く理解するためのアプローチをいくつか紹介する。

# Visualizing Point Patterns

地理的なポイントパターンを視覚化する方法は数多くあり、意図するメッセージによって方法を選択することができます。

## Showing Patterns as Dots on a Map

このデータセットの空間的次元がどのようなものかを知るための最初のステップは、プロットすることです。最も基本的なレベルでは、seabornで散布図を作成することができます。

```python
# Generate scatter plot
seaborn.jointplot(x="longitude", y="latitude", data=db, s=0.5);
```

これは良いスタートです。ドットは、非ランダムなパターンで、カバーエリアの中央に集中する傾向があることがわかります。さらに、この広いパターンの中に、より局所的なクラスターが存在することも確認できます。1つは、地理的なコンテキストがないこと、もう1つは、点の密度が高すぎて、青く塗りつぶされた部分以外が分かりにくいことです。

### Joint Plotにタイルマップを重ねる(これいいなー！)

まずはコンテキストから。追加のコンテキストを提供する最も簡単な方法は、インターネットからタイルマップを重ねることです。そのためにcontextilyを素早く呼び出し、jointplotと統合してみましょう。

```python
# Generate scatter plot
joint_axes = seaborn.jointplot(
    x="longitude", y="latitude", data=db, s=0.5
)
contextily.add_basemap(
    joint_axes.ax_joint,
    crs="EPSG:4326",
    source=contextily.providers.CartoDB.PositronNoLabels,
);
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_13_0.png)

経度と緯度をプロットしているので、CRSをWGS84に指定して、ポイントがプロットされている軸を引き出して、そこにベースマップを追加できることに注意してください。前のプロットと比較して、最初のプロットにベースマップを追加することで、Flickrのデータのパターンがより明確になります。

## Showing Density with Hex-binning

### Cluttering(乱雑さ)とは

2つ目の問題、**Cluttering(乱雑さ)**について考えてみましょう。ある場所に多くの写真が集中している場合、不透明な点を重ねてプロットすると、パターンを見出したり、その性質を探ったりすることが難しくなります。例えば、地図の中央から右側にかけては、最も多くの写真が撮影されているように見えますが、地図上のドットの量が多いため、その地域全体が多くの写真を撮影しているのか、それともその中で特に注目度の高い場所があるのかがわからなくなっています。

### 「Table to surfaces」を用いてClutteringを表現

Clutteringを回避するための1つの解決策は、先に述べた「Table to Cluttering」の移動に関連するものです。

- この方法は、空間ヒストグラムまたは2次元ヒストグラムとして再構築することができます。
- ここでは、通常のグリッド（正方形または六角形）を生成し、各グリッドセル内にあるドットの数をカウントし、他のChoroplethのようにそれを表示します。
- この方法は、シンプルで直感的であり、また、十分な大きさがあれば、正方形の格子によって、地図が引き起こす面積の歪みを取り除くことができるため、魅力的な方法です。
- この例では、**六角形のビンニング（Hex-binning）**を使ってみましょう。
- ヘクスビン2次元ヒストグラムの作成は、Pythonのhexbin関数を使えば簡単にできます。

```python
# Set up figure and axis
f, ax = plt.subplots(1, figsize=(12, 9))
# Generate and add hexbin with 50 hexagons in each
# dimension, no borderlines, half transparency,
# and the reverse viridis colormap
hb = ax.hexbin(
    db["x"],
    db["y"],
    gridsize=50,
    linewidths=0,
    alpha=0.5,
    cmap="viridis_r",
)
# Add basemap
contextily.add_basemap(
    ax, source=contextily.providers.CartoDB.Positron
)
# Add colorbar
plt.colorbar(hb)
# Remove axes
ax.set_axis_off()
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_16_0.png)

これで、より詳細な情報が得られるようになりました。これで、**写真の大半がより局所的なもの**であり、以前の地図ではそれが不明瞭であったことが明らかになった。

## Another Kind of Density: Kernel Density Estimation(KDE)

- グリッドはヒストグラムの空間的等価物であり、**ユーザーはいくつの「バケット」を決め、そしてポイントはその中で離散的にカウント**される。
  - これは高速で効率的であり、（多くのビンが作成された場合）非常に詳細になる可能性があります。
  - しかし、**本質的に連続した現象の離散化であり、そのため、歪みが生じる可能性がある**（例えば、修正可能な面単位の問題[Won04]）。
- 別のアプローチとしては、代わりにカーネル密度推定（KDE）として知られる、確率密度関数の経験的な近似を作成することです。
  - このアプローチは他の場所で詳しく説明されていますが（例えば[Sil86]）、ここではその直観を提供することができます。
  - KDEは、正方形や六角形のグリッドを重ね、それぞれの中にいくつの点が入るかを数えるのではなく、関心空間の上に点のグリッドを置き、その上にカーネル関数を置いて、距離に基づいて異なる重みでその周りの点を数えるのである。
  - これらのカウントを集計し、**確率的に大域的な曲面を生成**する。
  - 最も一般的なカーネル関数はガウシアン関数で、点の重みに正規分布を適用したものである。
  - その結果、各点で評価できる確率関数を持つ連続的な曲面が生成されます。Pythonでガウシアンカーネルを作成するのは簡単です。

```python
# Set up figure and axis
f, ax = plt.subplots(1, figsize=(9, 9))
# Generate and add KDE with a shading of 50 gradients
# coloured contours, 75% of transparency,
# and the reverse viridis colormap
seaborn.kdeplot(
    db["x"],
    db["y"],
    n_levels=50,
    shade=True,
    alpha=0.55,
    cmap="viridis_r",
)
# Add basemap
contextily.add_basemap(
    ax, source=contextily.providers.CartoDB.Positron
)
# Remove axes
ax.set_axis_off()
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_18_0.png)

その結果、Hex-binningの構造はそのままに、異なる領域間の遷移を「緩和」した、より滑らかな出力が得られました。これにより、空間上の理論的な確率分布のより良い一般化が実現されます。技術的には、KDE関数の連続的な性質は、任意の点でのイベントの確率が0であることを意味します。しかし、点の周りの領域が増加すると、その領域内のイベントの確率を得ることができます。これは便利な場合もあるが、主に六角形や四角形の規則正しいグリッドによる制約から逃れるために使われる。

# Centrography

**Centrography**はPoint Patternの**Centrality(中心性)**を分析するものです。

## Centrality(中心性)とは

- Patternの一般的な位置と分散を意味する。
- 上のHex-binningを「空間的なヒストグラム」と見なすと、Centrographyは**平均値などの中心傾向の測定値**に相当するPoint Patternといえる。
  - これらの指標は、**空間分布をより小さな情報の集合（例えば、1点）で要約することができる**ので便利です。
- Centrographyでは、Point Patternが「どこに」あるか、Point Patternがその中心の周りにどれだけ密に集まっているか、あるいはその形状がどれだけ不規則かを示すために、**多くの異なるIndices(評価指標)**が使用されます。

## Tendency

- Point PatternのCentrality傾向の一般的な測定は、その**質量中心**です。
- マークされたPoint Patternでは，質量中心は，そのマークされた属性でより高い値を持つObservationに近い中心点を識別する．
- マークされていないPoint Patternでは，質量中心は平均中心，または座標値の平均に相当する．
- さらに，Median Center(中央値の中心)は，他の場所での中央値と類似しており，データの半分がその点の上または下にあり＆半分がその左または右にある点を表現する．
- Pythonの`pointpats`パッケージを使って、Flickrのポイントパターンで平均中心(mean center)を分析することができます。

```python
from pointpats import centrography
mean_center = centrography.mean_center(db[["x", "y"]])
med_center = centrography.euclidean_median(db[["x", "y"]])
```

Point Patternとその平均中心を並べてプロットすると、最も分かりやすく視覚化できる。

```python
# Generate scatter plot
joint_axes = seaborn.jointplot(
    x="x", y="y", data=db, s=0.75, height=9
)
# Add mean point and marginal lines
joint_axes.ax_joint.scatter(
    *mean_center, color="red", marker="x", s=50, label="Mean Center"
)
joint_axes.ax_marg_x.axvline(mean_center[0], color="red")
joint_axes.ax_marg_y.axhline(mean_center[1], color="red")
# Add median point and marginal lines
joint_axes.ax_joint.scatter(
    *med_center,
    color="limegreen",
    marker="o",
    s=50,
    label="Median Center"
)
joint_axes.ax_marg_x.axvline(med_center[0], color="limegreen")
joint_axes.ax_marg_y.axhline(med_center[1], color="limegreen")
# Legend
joint_axes.ax_joint.legend()
# Add basemap
contextily.add_basemap(
    joint_axes.ax_joint, source=contextily.providers.CartoDB.Positron
)
# Clean axes
joint_axes.ax_joint.set_axis_off()
# Display
plt.show()
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_25_0.png)

西東京市と南東京市では、遠く離れた場所に写真の「クラスタ」が多く存在し、北東東京市では、密集しているが、すぐに途切れてしまうため、**2つの中心間(mean center とmedian center)の不一致は、傾きによって生じている**。このように、遠く離れた場所にある写真のクラスタが、中央の中心に対して、西と南に平均の中心を引っ張っているのです。

## Despersion

Centrographyで一般的な分散の指標は、Standard Distance(標準距離)です。この指標は、**点群の中心からの平均距離**（重心によって測定されるような）を提供します。これも、`std_distance`関数を使って、`pointpats`で簡単に計算できる。

```python
centrography.std_distance(db[["x", "y"]])
>>>8778.218564382098
```

つまり、平均すると、mean centerから約8800m離れて撮影されていることになる。

もう一つの有用な視覚化として、Standard Deviational Ellipse(標準偏差楕円)、またはStandard Ellipse(標準楕円)があります。これは、データから中心(center)、分散(dispersion)、方向(orientation)を反映した楕円を描いたものである。これを視覚化するために、まず`pointpats`の`ellipse`関数を使って軸と回転を計算する。

```python
major, minor, rotation = centrography.ellipse(db[["x", "y"]])

from matplotlib.patches import Ellipse

# Set up figure and axis
f, ax = plt.subplots(1, figsize=(9, 9))
# Plot photograph points
ax.scatter(db["x"], db["y"], s=0.75)
ax.scatter(*mean_center, color="red", marker="x", label="Mean Center")
ax.scatter(
    *med_center, color="limegreen", marker="o", label="Median Center"
)

# Construct the standard ellipse using matplotlib
ellipse = Ellipse(
    xy=mean_center,  # center the ellipse on our mean center
    width=major * 2,  # centrography.ellipse only gives half the axis
    height=minor * 2,
    angle=numpy.rad2deg(
        rotation
    ),  # Angles for this are in degrees, not radians
    facecolor="none",
    edgecolor="red",
    linestyle="--",
    label="Std. Ellipse",
)
ax.add_patch(ellipse)

ax.legend()
# Display
# Add basemap
contextily.add_basemap(
    ax, source=contextily.providers.CartoDB.Positron
)
plt.show()
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_31_0.png)

## Extent

Centrographyの最後の指標は、**点群の範囲(Extent)を特徴づけるもの**である。4つの形状が有用であり、パターンをどれだけ「きつく」縛るかの様々なレベルを反映する。

以下では、それぞれの例の作成方法を説明し、最後にそれらを可視化します。より明確にするために、データセットの中で最も多くのユーザーを持つFlickrの写真（ID: 95795770）を使って、これらの結果がどのように異なるかを示します。

```python
user = db.query('user_id == "95795770@N00"')
coordinates = user[["x", "y"]].values
```

### Convex hull

第一に、ユーザーの写真を囲むConvex Shape(凸形状)のうち、最もきついものを**Convex hull**として計算します。Convex hullとは、その形状が決して「二重反転」しないこと、つまり、**くぼみ、谷、勾配、穴がないこと**を意味します。また、すべての内角が180度より小さくなっています。これは `centrography.hull` メソッドで計算されます。

```python
convex_hull_vertices = centrography.hull(coordinates)
```

### Alpha Shape

第二に、**Alpha Shape**を計算する。Alpha Shapeは、Convex hullの「きつい」バージョンと理解することができる。Convex hullは、大きな球や円を転がしたときにできる余白のようなものです。ボールは形状に対して非常に大きいので、その半径は実際には無限であり、Convex hullを形成する線は実際には単なる直線なのです。

これに対してAlpha Shapeは、小さなボールを転がすことでできる空間と考えることができます。ボールは小さいので、点と点の間にできる凹みや谷に転がり込みます。そのボールが大きくなると、Alpha ShapeはConvex hullになる。しかし、小さなボールの場合、形状は実に窮屈になる。実際、αが小さくなりすぎると、点を「滑って」しまい、複数の船型が出来てしまうのです。そのため、`pysal`パッケージには `alpha_shape_auto `関数があり、ボールの大きさを推測することなく、最小のAlpha Shapeを見つけることができます。

```python
import libpysal

alpha_shape, alpha, circs = libpysal.cg.alpha_shape_auto(
    coordinates, return_circles=True
)
```

下図は、最もタイトな単一のAlpha Shapeを緑で、元のソースポイントを黒で示したものです。図中の「境界」円はすべて半径8652mである。この円は、点群内の2つまたは3つの点に「境界」ディスクが接触しているところにプロットされています。円は2点（または3点）に接するまで、青い破線で示したConvex hullに「食い込んで」いることがわかる。これ以上きつくすると、Alpha Shapeの境界で円が点の一つを切断してしまう。

```python
from descartes import PolygonPatch  # to plot the alpha shape easily

f, ax = plt.subplots(1, 1, figsize=(9, 9))

# Plot a green alpha shape
ax.add_patch(
    PolygonPatch(
        alpha_shape,
        edgecolor="green",
        facecolor="green",
        alpha=0.2,
        label="Tighest single alpha shape",
    )
)

# Include the points for our prolific user in black
ax.scatter(
    *coordinates.T, color="k", marker=".", label="Source Points"
)

# plot the circles forming the boundary of the alpha shape
for i, circle in enumerate(circs):
    # only label the first circle of its kind
    if i == 0:
        label = "Bounding Circles"
    else:
        label = None
    ax.add_patch(
        plt.Circle(
            circle,
            radius=alpha,
            facecolor="none",
            edgecolor="r",
            label=label,
        )
    )

# add a blue convex hull
ax.add_patch(
    plt.Polygon(
        convex_hull_vertices,
        closed=True,
        edgecolor="blue",
        facecolor="none",
        linestyle=":",
        linewidth=2,
        label="Convex Hull",
    )
)

# Add basemap
contextily.add_basemap(
    ax, source=contextily.providers.CartoDB.Positron
)

plt.legend();
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_39_0.png)

### 三種のBoundary shapes

ここでは、**さらに3つのBoundary shapes**を取り上げるが、いずれも矩形または円である。

### minimum bounding rectangles と Minumum Rotated Rectangle

まず、2種類のminimum bounding rectangles(最小外接矩形)である。

- どちらも、すべての点を含むデータの周りに描くことができる最も狭い矩形として構成されます。
- 1種類のminimum bounding rectanglesは、縦線と横線を考えるだけで描くことができる。
- しかし、対角線を引くとより小さな面積の矩形を構成できることが多い。つまり、最小回転矩形は、点パターンをより厳密に矩形で拘束するが、矩形が斜めになったり、回転したりするのである。=>2種類目：Minumum Rotated Rectangle

Minumum Rotated Rectangleは、`pygeos`モジュールの`minimum_rotated_rectangle`関数を使用し、入力の多点オブジェクトに対して最小の回転矩形を構築します。つまり、点を1つの多点オブジェクトに集め、そのオブジェクトの回転矩形を計算する必要があります。

```python
import pygeos

point_array = geopandas.points_from_xy(x=user.x, y=user.y)
multipoint = pygeos.from_shapely(point_array.unary_union())

min_rot_rect = pygeos.to_shapely(
    pygeos.minimum_rotated_rectangle(multipoint)
)
```

また、回転を伴わないminimum bounding rectanglesについては、`pointpats` パッケージの `minimum_bounding_rectangle` 関数を使用します。

```python
min_rect_vertices = centrography.minimum_bounding_rectangle(
    coordinates
)
```

#### Minumum Bounding Circle

最後に、Minumum Bounding Circleは、データセット全体を囲むように描ける最小の円である。多くの場合、この円はMinimum Bounding Rectangleより大きい。これは`pointpats`の`minimum_bounding_circl`e関数で実装されている。

```python
(center_x, center_y), radius = centrography.minimum_bounding_circle(
    coordinates
)
```

さて、これらを可視化するために、点群の範囲(Extent)を特徴づける各手法で得られた頂点の座標を、matplotlibのパッチに変換します。

```python
from matplotlib.patches import Polygon, Circle, Rectangle
from descartes import PolygonPatch

# Make a purple alpha shape
alpha_shape_patch = PolygonPatch(
    alpha_shape,
    edgecolor="purple",
    facecolor="none",
    linewidth=2,
    label="Alpha Shape",
)

# a blue convex hull
convex_hull_patch = Polygon(
    convex_hull_vertices,
    closed=True,
    edgecolor="blue",
    facecolor="none",
    linestyle=":",
    linewidth=2,
    label="Convex Hull",
)

# a green minimum rotated rectangle

min_rot_rect_patch = PolygonPatch(
    min_rot_rect,
    edgecolor="green",
    facecolor="none",
    linestyle="--",
    label="Min Rotated Rectangle",
    linewidth=2,
)


# compute the width and height of the
min_rect_width = min_rect_vertices[2] - min_rect_vertices[0]
min_rect_height = min_rect_vertices[2] - min_rect_vertices[0]

# a goldenrod minimum bounding rectangle
min_rect_patch = Rectangle(
    min_rect_vertices[0:2],
    width=min_rect_width,
    height=min_rect_height,
    edgecolor="goldenrod",
    facecolor="none",
    linestyle="dashed",
    linewidth=2,
    label="Min Bounding Rectangle",
)

# and a red minimum bounding circle
circ_patch = Circle(
    (center_x, center_y),
    radius=radius,
    edgecolor="red",
    facecolor="none",
    linewidth=2,
    label="Min Bounding Circle",
)
```

最後に、パッチを写真の位置と一緒に下にプロットしておきます。

```python
f, ax = plt.subplots(1, figsize=(10, 10))

ax.add_patch(alpha_shape_patch)
ax.add_patch(convex_hull_patch)
ax.add_patch(min_rot_rect_patch)
ax.add_patch(min_rect_patch)
ax.add_patch(circ_patch)

ax.scatter(db.x, db.y, s=0.75, color="grey")
ax.scatter(user.x, user.y, s=100, color="r", marker="x")
ax.legend(ncol=1, loc="center left")

# Add basemap
contextily.add_basemap(
    ax, source=contextily.providers.CartoDB.Positron
)
plt.show()
```

![](https://geographicdata.science/book/_images/08_point_pattern_analysis_49_0.png)

それぞれ、ユーザーの撮影範囲を囲む領域の印象が異なる。この図では、Alpha Shapeが他の形状よりずっとタイトであることがわかります。Minimum Bounding RectangleとMinumum Bounding Circleは、ユーザーの典型的な領域の外側に最も多くの領域を含むという意味で、「最も緩い」シェイプです。しかし、描くのも理解するのも最も簡単なシェイプでもあります。

# Randomness & Clustering

## Introduction

Point Patternの空間統計では、Centrality(中心性)やExtent(範囲)だけでなく、「点の分布がどの程度均一であるか」が問題になることが多い。
これは、**点が互いに近くに集まる傾向があるのか**、**それとも問題領域全体に均等に分散しているのか**を意味する。
このような質問は、Point Pattern全体の密度(Intensity)や分散(Dispersion)を意味する。前2章の専門用語で言えば、この焦点は、Global Spatial Autocorrelationを導入したときに検討した目標に似ている：パターンに見られる全体的なClustering(グルーピング、つまりPositive Spatial Autocorrelation？？)の程度は何か？

空間統計学はこのようなクラスタリングを理解するために多くの努力を払ってきた。このセクションでは**、Point Patternにおけるクラスタリングを特定するのに有効な方法**を紹介する。

## Quadrat statistics

## Ripley’s alphabet of functions

# Identifying clusters

# Conclusion
