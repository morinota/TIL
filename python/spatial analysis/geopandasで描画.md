# 参考

- https://geopandas.org/en/stable/index.html
- 無償で使える GIS データ/マップ
  - https://www.esrij.com/gis-guide/other-dataformat/free-gis-data/
  - https://fgd.gsi.go.jp/download/menu.php
- ポリゴンの重心測定
  - https://qiita.com/c60evaporator/items/ac6a6d66a20520f129e6#%E5%87%A6%E7%90%868%E3%83%9D%E3%83%AA%E3%82%B4%E3%83%B3%E3%81%AE%E9%87%8D%E5%BF%83%E6%B8%AC%E5%AE%9A
# はじめに

私は大学院の研究活動で、地理情報データを扱っています。これまでは、各フィーチャの属性情報や隣接するフィーチャとの位置関係をテーブルデータとして扱い、機械学習なり空間統計モデルなりしてきました。
それで今度は、地理情報データ(ベクトルデータ)を画像として扱い、画像認識なり物体検出なりの手法を活用する事で、これまでテーブルデータとして表現できなかったフィーチャの特徴を捉える事ができないかと思いました。

したがって今回の記事では、「地理情報データの各フィーチャに対して、周囲のフィーチャとの位置関係を画像として保存する」処理を実装しました。

今回はPythonのライブラリであるGeoPandasを使用して、上述した目的を達成する為の処理を実装します。ArcGISやQGIS等のGISソフトウェアを使っても可能だとは思うのですが、個人的にPandasに慣れている事とできる限りGUIを使わずにコーディングで処理を実装したいという矜持から、GeoPandasを選択しました。

実装に向けて調べた印象では、GeoPandasを含めた地理情報データ系のPythonパッケージ・ライブラリは日本語のDocumentや記事が少なそうでした。本記事を通して、私と同じように地理情報データを扱う方と情報共有できれば幸いです。

# GeoPandasとは?

以下、公式Documentからの引用です。

> GeoPandas is an open source project to make working with geospatial data in python easier. GeoPandas extends the datatypes used by pandas to allow spatial operations on geometric types. Geometric operations are performed by shapely. Geopandas further depends on fiona for file access and matplotlib for plotting.

使用してみた印象では、地理情報(ベクターデータ)をPandasのDataFrameのように扱う事ができて、心地良いです：）
(GeoPandasでは、GeoDataFrameというクラスを使用します。)

# 準備

## 準備1:地理情報データの用意

```python
import geopandas as gpd
from geopandas.datasets import get_path

world = gpd.read_file(get_path('naturalearth_lowres'))
cities = gpd.read_file(get_path('naturalearch_cities'))
```

## 準備2:GeoDataFrameオブジェクトの生成

## 準備3:座標参照系(CRS)を統一する。

座標参照系(Coodinate Reference System, CRS)というのは、地物(フィーチャ)の座標(緯度経度)から、その地物がどの位置にあるかを正確に表す為の設定、みたいな感じだと認識しています。
世界地図の種類(メルカトル図法、正距方位図法, etc.)の違い、がわかりやすいような気がしますね。例えば、一つの世界地図には川が描かれていて、もう一方の世界地図には山が描かれていて、２つの地図を重ねて川と山の位置関係を比較しようとした時に、両者の世界地図の図法(座標参照系)が異なっていたら、位置関係を正しく検討できない、みたいな...。

```

```
## 準備4：フィーチャの重心の算出方法を確認

## 準備5: 描画の仕方を確認

# いざ実装。描画用の関数を定義。

# イテレータで各フィーチャ毎に周囲のフィーチャとの位置関係を画像として保存
