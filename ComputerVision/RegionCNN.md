# 物体検出とは

## 画像認識と物体検出

![](https://camo.qiitausercontent.com/4e348fd976008cdf0decc504146f4d0d5031f58b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f65353562323539372d386436352d323436372d383539662d3739386264303832636236342e706e67)
有名なMNISTデータセットで行っているのは"画像認識(Image Classification)"というタスク。
これは一枚の画像が与えられ、機械学習モデルが0~9のどの数字か当てる。
（例えば左上は5の画像が与えられ、"5"とモデルが返せたら正解）
これは**画像全体に対して推論を行い、結果は一つ**という点に注目したい。

![](https://camo.qiitausercontent.com/4e348fd976008cdf0decc504146f4d0d5031f58b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f65353562323539372d386436352d323436372d383539662d3739386264303832636236342e706e67)
これに対して、"物体検出(Object Detection)"では更にタスクが複雑になる。これは画像をPASCAL VOC 2007という物体検知タスクのMNIST的なデータセットから拝借している。
ここでは画像に複数の物体（車＊２＋バス）が写り込んでおり、モデルは**その物体が画像中のどこの座標に存在しているか**当てる必要がある。

例えばモデルの出力値は`bus xmin=300, ymin=150, xmax=450, ymax=200`のように、**「物体が何であるか(bus)」と「その座標(xmin=300, ymin=150, xmax=450, ymax=200)」を回答**し、その結果として**生成される物体を囲む箱をBoundingBox（BBox）**などと表現する。
平たく言うと、物体検出タスクは画像中の物体全てを箱で囲み、それが何であるかを当てれればよい。

## 物体検出モデルの2種類のタスク

物体検出モデルでは、大きく2種のタスクを実施している。

1. ある画像領域が背景か物体か？(物体検出タスク)
2. もし物体ならば何の物体か？(画像認識タスク)

それゆえ、単純に画像認識だけを行うモデルと比較して、タスク難易度は数段高い。

# 物体検出モデルの遍歴

## Windowベース検出器(ex. Alexnet)

**じゃあ画像を細かく(数1000～)分割して、片っ端から画像分類のCNNに突っ込めばいいじゃん！**という力技のアプローチが元祖Window-CNN。
CNNは高品質な特徴量抽出ができる為、CNN出力から**画像の一部分が背景または物体かを当てる**のは難しくない。

ここで実際のWindow-CNN動作を見てみる。
![](https://camo.qiitausercontent.com/34fc572e0a190e6adf26f1d80fb8504ae8e1bf99/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f64663638333661642d616632622d616331332d653264392d6434616461633864323164322e706e67)
ネットワーク図では、細かく分割した画像をwarped imageとし、CNNに入力する。
CNNは画像の特徴量を抽出し、4096値の特徴量ベクトルを出力する。
抽出した特徴量を分類器に突っ込み、推論結果を得る。
（各"細かく分割した画像の一部分"は、背景、自転車、人、車いずれかであったかわかる）。

### Window-CNNのデメリット：処理時間(演算量)

一方でWindow-CNNのデメリットは処理時間（または演算量）であった。

画像一枚につきCNNを数千回、数万回回さなくてはならないため、検出が非常に遅い（リアルタイム性が低い）というのが欠点。
以下のコードのイメージ

```python
for window in windows
    patch = get_patch(image, window)
    results = CNNdetector(patch)
```

それではR-CNN,Faster-R-CNNが技術の進化でこの速度ギャップを埋める様を見ていく。
端的に言うと、**如何にCNN detectorを回す回数を減らすか**というのが研究の主眼となっている。

## R-CNN(Regional CNN, 領域ベースCNN)

これも従来の物体検出モデルをCNNに置き換えたものであるが、考え方は重要。

画像内に隈なくdetector(=画像を細かく分割して各々CNNに突っ込む)を走らせると計算コストが大きすぎるので、**最初に物体があるっぽい領域を提案させよう！**というアプローチ。

detectorは物体があるっぽい領域のみ計算すればいいのでWindowベースモデルよりは高速化が期待できる。
また物体があるっぽい領域を**region-of-interest(ROI)**などと呼ぶ。また、ROIを提案するモデルを**region proposal**と呼ぶ。

### R-CNN系のDNNモデルの基本構造

R-CNN系のDNNモデルは、以下の2-stage構成になっている点に注目したい。(ネットワーク図後半のFC layerは全結合層の意味！)

1. 物体があるっぽい領域を提案するモデル(region poroposal)
2. 画像認識をするモデル(CNN detector)

![](https://camo.qiitausercontent.com/e768a19e415dabb904e39876742a0f693d9fe229/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f62373930346636612d633834662d383130612d633937652d3466656532393631663336312e706e67)

### R-CNNのメリット・デメリット

R-CNNの挙動は、以下のコードの様なイメージ。

```python
ROIs = region_proposal(image)
for ROI in ROIs
    patch = get_patch(image, ROI)
    results = CNNdetector(patch)
```

R-CNNはregion proposalによって提案された画像部分(=物体があるっぽい領域)ROIに対してのみ、CNNdetectorを回す。そのためCNNを回す回数は、window-baseに対しては大幅に削減可能！

region proposalで使われるのは非DNNの従来技術の為「精度がまだ低い」という欠点はあるものの、考え方そのものは汎用的で、**現在のtwo-staged detectorの基本**となっている。

しかし当然、**regional proposal自体の精度も非常に重要**で、物体のない領域を提案してしまうといくら2段目のCNN detectorの認識精度がどれほど高くても検出を間違えてしまう。
また、この**regional proposal自体の演算量も大きい**、という欠点もあった。

## Fast R-CNN

直球的な名前が示す通り、R-CNNの高速化を達成した研究。
以下のネットワーク図が分かりやすいので、そちらに注目する。

構造としてはR-CNNに似ている：RegionProposal(RP)があり、CNNがある。

では**どこがFastなのか**？
RegionProposalは、CNNの出力する特徴量領域を指している(?)のに注目したい。
どうやら、**RP出力とCNN出力を繋ぐ、ROI(Region-of-interest) pooling layer**がFast-R-CNNで提案されている事らしい！

### Fast-R-CNNのブレイクスルー

Fast-RCNNでは画像認識を行う時には**毎回CNNを走らせる必要はなく**、**RegionProposalの抽出した特徴領域を切り出し、全結合層に与えるだけ**でよい。
従来のR-CNNが、画像認識毎にCNN層も走らせていたのに比べると大幅な高速化を達成できる。

RegionProposalが1000回あったとすると演算量は：

- 従来R-CNN：$CNN \times 1000+FC \times 1000$
- Fast-R-CNN:$CNN \times 1+FC \times 1000$

と、**CNNの演算回数を1/1000にできる**！
(また全結合相は遅いため画像認識層を全てConvolution層に置き換えるFully convolutional Fast R-CNNも提案された。）

擬似コードで書くと、Fast R-CNNは以下の様になる。

```python
ROIs = region_proposal_by_selective_search(image)
Fmaps = CNN(image)
for ROI in ROIs
    patch = ROI_pooling(Fmaps, ROI)
    results = FCdetector(patch)
```

特徴量マップ（Fmaps)を一度取得し、それをfor loopの中で使い回す。
CNNを回す回数は一度に削減できた。

## Faster R-CNN

実はFast R-CNNは、Region Proposalの実行時間が支配的になってしまっている。一枚の画像に2.3秒かかるが、そのうち**2秒(86%!)がRegionProposal**に費やされていた。

というのもFast R-CNNではRegion Proposalに従来技術であるSelective Search(**非DNN**?)を使用しており、そこが速度ボトルネックとなっていた。

**Faster R-CNNはRegionProposalもCNN化することで物体検出モデルを全てDNN化し、高速化するのがモチベーションとなっている**。

またFaster-RCNNは**Multi-task loss**という学習技術を使っており、RegionProposalモデルも込でモデル全体をend-to-endで学習させることに成功している。

- end-to-endな学習とは:
  - 入力データが与えられてから結果を出力するまで多段の処理を必要としていた機械学習システムを，様々な処理を行う複数の層・モジュールを備えた一つの大きなニューラルネットワークに置き換えて学習を行うもの。
  - 自動運転を例に取ると，非エンドツーエンドのアプローチでは，物体認識，レーン検出，経路プランニング，ステアリング制御など，人間が設定した**複数個のサブタスクを解く必要があった**ところ，エンドツーエンド学習では**車載カメラから取得した画像から直接ハンドル操作を学習**する。

ネットワーク図は以下。
![](https://camo.qiitausercontent.com/09445813f0b4ba2e129064b011f4e0a205729bfd/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f36623032393438332d623832312d353632642d366564382d6165633861366139376532632e706e67)
Faster-RCNNは、**CNN出力（特徴マップ）を元にregion proposal(物体があるっぽい領域を抽出）するCNNモデル**を構築している。実際のregion proposalは3~4層ほどのCNNで構成可能で小さい。

**CNNが生成した特徴マップをできる限り使い倒す！**という流れがR-CNN系の発展に見て取れる。
実際にこのアプローチは精度向上・計算効率向上に寄与しており、興味深い。

Faster R-CNNを擬似コードで書くと以下のようになる。

```python
Fmaps = CNN(image)
ROIs = regionproposalCNN(Fmaps)
for ROI in ROIs
    patch = ROIpooling(Fmaps, ROI)
    results = FCdetector(patch)
```

### Fast R-CNNからの変更点

Region Proposalモデルの軽量化(CNN化)。
結果として、一枚の画像の推論時間は、

- Fast R-CNN:2.3秒
- Faster R-CNN:0.2秒

RegionProposalにかかる時間をほぼゼロに近づけたことにより、大幅な高速化を達成。ほぼ全てのモデルがDNNに！

またこれはTitanXpでFaster R-CNNのバックボーンに**Resnet101**を用いたときの実動作速度である。
検出タスクによってはバックボーンに**Resnet18**などを用いることで検出速度は20~40msまで短縮することができる。

### Region ProposalとAnchorについて

Faster-R-CNNにおいて、Region Propsal Network(RPN)はCNNの特徴マップ（つまりResnet等のCNN層出力）を入力情報とする。

そして「ある領域が物体か背景か(objectness)」、および「アンカーの位置の補正データ=(corrdinates)」を出力する。
Objectnessは0～１の値で、１に近いほど物体である確証が高い。CorrdinatesはBoundingBoxの四角の座標について、補正する量を出力する。

![](https://camo.qiitausercontent.com/bc1839c4c56095cdb9ccfdedb02f419a7cd3af67/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f34646538303631372d313462372d653937302d663130382d6531383366306231646133342e706e67)

RPNモデルは1箇所につき、**k個のBoundingBoxを提案**する。
これは1つの物体について重複する事が多く、最も確度の高いBoundingBoxのみ残したい(**Refining**)。大体k=128などが使われる事がある通り、refineなしでは大量のPredictionが生成されてしまい実用的ではない。

そこで、Refineに使われるが概念がAnchorである。
物体検出において、物体は3×3のような正方形である事は少ない。
例えば、人間は大体縦長であったり、車は横長である事が多い。
**このような図形情報を扱う為に提案された概念がAnchor**である。
(**たぶん検出されるべき物体はこんな形、みたいな事前情報を設定してる？？**)

![](https://camo.qiitausercontent.com/0014c632e332304018fdf24768ee09463829bca0/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e616d617a6f6e6177732e636f6d2f302f3137313931352f34666663313336312d646561322d646561372d353535312d3661623762353765393666332e706e67)

ある１座標(=Objectnessが1に近い座標の事?)につき提案されるBoundingBoxに対し、Anchor情報とどれくらい異なるかを導出し、一番Anchorに近いBoundingBoxをMain Predictionとして出力する。
このプロセスによって、**物体1つにつきBoundingBoxを1つに絞り込み、かつ一番高精度なものを残す事ができる**。

例えばF-RCNNでは(Faster-R-CNNだけでAnchorが使われてる訳じゃないっぽい！)、正方形、縦長、横長の3種類とそれをそれぞれスケールした計9種類が使われている。
これはCOCOなど一般物体検知は様々な形の物体を検出するためで、**もし使うデータセットが車のみならば横長のアンカーだけを使うなどカスタマイズすれば、高精度化が可能になるだろう**。

# 参考

- https://qiita.com/arutema47/items/8ff629a1516f7fd485f9
- https://jonathan-hui.medium.com/what-do-we-learn-from-region-based-object-detectors-faster-r-cnn-r-fcn-fpn-7e354377a7c9
