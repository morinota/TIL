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
- Centrographyでは、Point Patternが「どこに」あるか、Point Patternがその中心の周りにどれだけ密に集まっているか、あるいはその形状がどれだけ不規則かを示すために、多くの異なるIndices(評価指標)が使用されます。

## Tendency

## Despersion

## Extent

# Randomness & Clustering

## Quadrat statistics

## Ripley’s alphabet of functions

# Identifying clusters

# Conclusion
