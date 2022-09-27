## Link

- https://geographicdata.science/book/notebooks/04_spatial_weights.html#introduction

# Spatial Weight

- "Spatial Weight(空間重み付け)"は、Geographical Data ScienceやSpatial Statisticsにおけるグラフの表現方法の一つである。
  - Spatial Weightは、空間的に参照される**データセット内の観測単位間の地理的な関係を表す**ために広く使用されている構成要素です。
  - Spatial Weightは、暗黙のうちに、地理的な表中のオブジェクトを、それらの間の空間的な関係を用いて互いに結びつける。
  - 地理的なProximity(近接性)やConnectedness(連結性)の概念を表現することで、**Spatial Weightは、地理データにおける空間的な関係をその後の分析に生かすための主要なメカニズム**である。

## Introduction

- Spatial Weightは、空間的な関係についての知識を表すことが多い。
  - 例えば、Proximity近接とAdjacency隣接は一般的なSpatial Questionである。
    - どのような地域に囲まれているか？
    - 停車中の車から5マイル以内にいくつのガソリンスタンドがあるか？
  - これらは、特定のターゲット（「近所」、「停車した車」）と地理的に関連するサイト（「隣接する近所」、「近くのガソリンスタンド」）のSpatial Configuration(空間的な構成)に関する特定の情報を対象とするSpatial Questionである。
- この情報を統計解析で利用するためには、多くの場合、**観測値のすべてのペアの間でこれらの関係を計算する必要**があります。
  - つまり、Geographical Data Scienceの多くのアプリケーションでは、データを調査するために使用できるトポロジー（**オブザベーション間の接続性を表現する数学的構造**）を構築していることになります。
- Spatial Weight Matrixは、このトポロジーを表現し、ユニット近くの特徴についての単一の質問と回答ではなく、空間内のすべてのオブザベーションを一緒に埋め込むことができるようにします。

```python
import contextily
import geopandas
import rioxarray
import seaborn
import pandas
import numpy
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from pysal.lib import cg as geometry
```

- このような空間的関係を表現する方法を提供するため、Spatial Weight MatrixはSpatial・Geographical Data Science全体で広く利用されている。
- 本章では、まず、**Spatial Weight Matrixを構築するためのさまざまなアプローチ**を検討し、**隣接(Contiguity)/近接(Adjacency)関係に基づく重み**と、**距離に基づく関係から得られる重み**とを区別する。
- そして、オブザベーション間の近傍関係を導き出す際に、**1つまたは複数の空間演算を組み合わせるHybrid Weights**のケースを議論します。
- ` pysal`の`Spatial Weight`クラスは、Spatial Weight Matrixのための豊富なメソッドと特性のセットを提供し、それは`weights`サブモジュールの下に格納されています。

```python
from pysal.lib import weights
```

また，集合演算の適用により重みを導出できる集合論的な機能についても説明する．この章では，さまざまなタイプの**Spatial Weight Matrixを保存するために使用される一般的なファイル形式**について説明し，Spatial Weight Matrixについて視覚的に説明することで，抽象的な構造をより直感的に理解できるようにした．

# Contiguity Weights (隣接性・連続性の重み)

## Contiguity(隣接性、連続性)の難しさ

- 連続(隣接)する空間オブジェクトのペアとは、「共通の境界を共有するオブジェクト」のことである。
  - これは一見、簡単そうに見える。
  - しかし、実際にはもっと複雑であることが判明している。
  - まず、複雑なのは、**「共通の境界線」の取り方がいろいろあること**である。

難しさを理解する為にまず、3×3のグリッドの例から始めましょう。これはゼロからジオテーブルとして作成することができます。

```python
# Get points in a grid
l = numpy.arange(3)
xs, ys = numpy.meshgrid(l, l)
# Set up store
polys = []
# Generate polygons
for x, y in zip(xs.flatten(), ys.flatten()):
    poly = Polygon([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)])
    polys.append(poly)
# Convert to GeoSeries
polys = geopandas.GeoSeries(polys)
gdf = geopandas.GeoDataFrame(
    {
        "geometry": polys,
        "id": ["P-%s" % str(i).zfill(2) for i in range(len(polys))],
    }
)
```

となり、下図のようなグリッドになります。

# Distance Based Weights

# Block Weights

# Set Operations on Weight

# Visualizing Weight set operations

# Use case: Boundary detection
