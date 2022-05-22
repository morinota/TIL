# Link

- https://onlinelibrary.wiley.com/doi/full/10.1111/jiec.13143#:~:text=The%20material%20intensity%20database%20is,see%20Tables%201%20and%202).

## title

Material intensity database for the Dutch building stock Towards Big Data in material stock analysis
オランダの建築ストックの材料強度データベース 材料ストック分析におけるビッグデータに向けて

## Abstract

- Re-use and recycling in the construction sector is essential to keep resource use in check.
  - 建設部門における再利用とリサイクルは、資源の使用を抑制するために不可欠です。
- Data availability about the material contents of buildings is significant challenge for planning future re-use potentials.
  - 建築物の材料含有量に関するデータを入手することは、将来の再利用可能性を計画する上で大きな課題となっています。
- Compiling material intensity (MI) data is time and resource intensive.
  - 材料強度（MI）データの収集は、時間と資源を必要とします。
- Often studies end up with only a handful of datapoints.
  - 多くの場合、調査はほんの一握りのデータポイントに終わります。
- In order to adequately cover the diversity of buildings and materials found in cities, and accurately assess material stocks at detailed spatial scopes, many more MI datapoints are needed.
  - 都市に存在する多様な建物と材料を適切にカバーし、詳細な空間スコープで材料ストックを正確に評価するためには、より多くのMIデータポイントが必要である。
- In this work, we present a database on the material intensity of the Dutch building stock, containing 61 large-scale demolition projects with a total of 781 datapoints, representing more than 306,000 square meters of built floor space.
  - 本研究では、オランダの建物ストックの材料強度に関するデータベースを紹介する。このデータベースは、61の大規模解体プロジェクトを含み、合計781データポイント（306,000平方メートル以上の建築床面積に相当）を有している。
- This dataset is representative of the types of buildings being demolished in the Netherlands.
  - このデータセットは、オランダで取り壊される建物の種類を代表するものです。
- Our data were empirically sourced in collaboration with a demolition company that explicitlyfocuses on re-using and recycling materials and components.
  - このデータは、材料や部品の再利用やリサイクルに積極的に取り組んでいる解体業者と協力して、経験的に収集されたものです。
- The dataset includes both the structural building materials and component materials, and covers a wide range of building types, sizes, and construction years.
  - このデータセットには、構造材料と部品材料の両方が含まれており、建物の種類、サイズ、建設年など、幅広い範囲をカバーしています。
- Compared to the existing literature, this paper adds significantly more datapoints, and more detail to the different types of materials found in demolition streams.
  - 既存の文献と比較すると、この論文ではデータポイントが大幅に増え、解体物の流れに見られるさまざまな種類の材料についてより詳細な情報を得ることができます。
- This increase in data volume is a necessary step toward enabling big data methods, such as data mining and machine learning.
  - このようなデータ量の増加は、データマイニングや機械学習などのビッグデータ手法を可能にするために必要なステップである。
- These methods could be used to uncover previously unrecognized patters in material stocks, or more accurately estimate material stocks in locations that have only sparse data available.
  - これらの手法を用いることで、これまで認識されていなかった材料在庫のパターンを発見したり、データが乏しい場所での材料在庫をより正確に推定したりすることができるようになります。

# Introduction

## 建築材料の重要性

- 現在、世界の材料需要のおよそ半分を建築環境が占めています（IRP, 2019）。
- 都市化と人口増加により、都市環境における材料の需要は増加し続けることが予想されます（Fishman et al.、2016；Wiedenhofer et al.、2019）。
- 材料効率を向上させる様々な戦略（IRP, 2020; Scott et al., 2018）とともに、材料は一次産品ではなく、老朽化した建物の解体から可能な限り調達することが不可欠である。
- どの材料が建築環境に存在し、どの程度の量があるのかを一般的に理解する。
- この種のデータは、現実の材料集約度を正確に表現する現実的なボトムアップモデルを作るために極めて重要

## Data availability about the material contents of buildings

- 建物の材料内容に関するデータの入手可能性は、将来の再利用の可能性を計画するための最大の課題の一つである（Augiseau & Barles, 2017; Lanau et al, 2019）。
- 当然ながら、材料とその特性（質量、最終用途、品質など）の定量化は、**建設中か解体中にしか実証的に測定することができない**。
  - 使用中の建物ストックの材料含有量は、推定するしかない。
  - したがって、使用中のストックに焦点を当てた研究では、通常、統計的に推定された材料強度係数（MI、床面積または建物容積あたりの質量）を、理想的には類似の建築タイプ、場所、期間に一致する建物の原型に基づいて使用中のストックに割り当てます。
  - このアプローチは、建築材料ストックに関するいわゆる「ボトムアップ」研究において一般的なものである。

## MIの代表性の限界

- MIデータの収集には時間と資源が必要であり、多くの場合、調査はわずかなデータポイントに終わり、その結果、不明確な点が生じる。
  - さらに、建築は地域特有のスタイル、好み、技術、規制、伝統などに依存し、それらは時には近隣の都市間でも大きく異なる。
  - 個々の建築物の規模では、土地の傾斜、地盤、土壌の種類、水文学などの物理的属性や、建設期間、建設予算、建築デザイン、使用目的などの社会的、経済的要因が、特定の建築物における実際の材料の質量に影響を与える。
  - その結果、MIは事実上、個々の建築物に固有のものとなっています。
  - これは、**数十年前に標準化された生産ラインに移行した他のほぼすべての生産部門と比較すると、かなりユニークな現象**です。
- 従って、原型としての**MIの代表性**は、材料ストックとフロー研究、及び建築物とインフラのライフサイクル評価の両方において認められる**限界**である（Saxe et al.、2020）。

## 更にMIの限界を悪化させるのは...

- その相対的な希少性の問題をさらに悪化させるのは、MIデータが、特定の研究のために、その目的に合わせて、データ編集の制限の範囲内でアドホックに編集されることが多いことである。
  - しかし、材料の種類、最終用途、解像度、さらには測定単位などの対象は研究によって大きく異なる（Heeren & Fishman, 2019)

## MIの限界に対する取り組み

- 最近、ドイツと日本のMI間の移転可能性のテスト（Schillerら、2019）など、いくつかの取り組みが行われている。
- 世界レベルでは、Marinovaら（2020）、Deetmanら（2020）が、異なる地域の材料強度データを組み合わせて、建築関連の材料ストックとダイナミクスを報告している。

## よって本研究では...

- 詳細な空間スケールで材料ストックを正確に評価するためには、都市における建物の多様性と、同じ種類の建物に見られる材料の多様性を適切にカバーするために、より多くのデータポイントが必要である。
- 本研究では、オランダの建物ストックの材料強度に関するデータベースを紹介する。
  - このデータベースは、61の大規模解体プロジェクトを含み、合計781データポイント（306,000 m2以上の建築床面積に相当）を有する。
  - このデータベースでは、**1つのデータポイント（記録または観察とも呼ばれる）は、1つの建物ユニットの材料強度値（単位床面積当たりの質量）と、そのユニットに関する追加情報（築年数や用途など）で構成されています。**
  - このデータは、材料や部品の再利用やリサイクルに力を入れている解体業者と協力して経験的に入手したもので、材料の流れについて比較的詳細な記録を持っています。
  - 建物の構造と部品（窓枠、ドア、ラジエーターなど）の両方についてデータを提供しています。
  - このデータセットは、建物の種類、サイズ、建設年など多岐にわたります。

## 本研究のオリジナリティ??

- 本研究におけるこの多数のデータポイントは、既存のデータセットと比較して有利である。
  - 例えば、Heeren and Fishman（2019）は、その時点までの文献に見られる多くのデータをまとめ、合計301のデータポイントに達したが、そのほとんどは、平均して調査した研究ごとに4～6のMI群として由来するものである。
  - 注目すべき例外は、オーストリア・ウィーンの68のMIデータポイントをまとめたKleemannら（2017）と、46のMIを含むスウェーデンの材料強度データベース（Gontiaら、2018）です。
  - 最近、中国に焦点を当てたデータセットが発表され、813のMIデータポイントを含み（Yang et al., 2020）、今日までのMIの国別コレクションとしては圧倒的に大きく、我々の研究はさらにこれに貢献するものである
- Originality弱くない...???

# methodology

## overview

- 材料強度データベースは、オランダで実際に行われた相当数の解体プロジェクトからの経験的データに基づいています。
  - 建物は7つのサブタイプに分類
    - Single house
    - Row house
    - Apartment
    - High rise
    - Commercial
    - Office
    - Other
  - このデータはGISデータ（Kadaster, 2018）で補強され、解体された物の正確な表面積、建設年、体積が提供された。
  - この組み合わせにより、1平方メートルあたりの材料強度データベースを構築することができる。
- 建物の構造に関する材料（例：基礎、壁、屋根）と建物の構成要素に関する材料（例：ドア、天井、ランプ、窓枠）の2つのクラスに細分化されました。
  - このように分けるのは、構造材と構成材では解体時の処理が異なるためです。

## On-site data collection

## Data processing

- 解体現場から得られた生データを処理した後、政府から提供された建築環境を記述するGISデータセットからいくつかの建物属性を抽出した。

  - これらの属性は、解体業者によって収集された情報以外に、解体プロジェクトで発見された建物の特徴をさらに明らかにするために使用されました。
  - これらは、建設年、機能的床面積、建物タイプ、建物ごとの住居数などを含み、BAG3D（Kadaster、2018）から抽出されたものであった。
  - これらの情報を用いて、各建物タイプの材料強度（kg/m2）を算出した。

- 図 1 は、解体データの処理を可視化したものである。
  - ![](https://onlinelibrary.wiley.com/cms/asset/c32a520f-6ed6-4d6e-bdc3-56214c4d592d/jiec13143-fig-0001-m.png)
- 図2については、均一なMIを提示するために、すべての材料をkg/m2床面積で計算した。

  - ![](https://onlinelibrary.wiley.com/cms/asset/cb70d9ca-8df2-491f-96ea-3a49e24b55a3/jiec13143-fig-0002-m.png)


# Results

## figure2. オランダの建築物ストックの平均的な材料強度

- オランダの建築物ストックの平均的な材料強度を提示する。次に、我々のデータセットにおけるばらつきを探る。
- As we can see in Figure 2, the average material intensity ranges from 612 to 1,909 kg/m2.
  - 図2に見られるように、平均材料強度は612から1,909 kg/m2の範囲にあります。
  - Residential buildings can be found on both ends of the intensity scale, with utility buildings being relatively consistent around 1 metric ton/m2.
    - 住宅は原単位の両端に位置し、公共施設は1トン/m2前後で比較的安定しています。
- Of note is the disparity between apartment buildings and residential high rises, where an apartment building has almost 50% more material intensity of a high-rise building.
  - 注目すべきは、集合住宅と高層住宅の間の格差で、集合住宅は高層ビルより50%近くも材料原単位が高い。
  - これは、このデータセットに含まれるアパートと高層ビルでは、コンクリート基礎の大きさは同等ですが、高層ビルの方が床面積が広いため、1m2あたりの材料強度が低くなっているためです。
  - 逆に、「住宅-一軒家」のユニットは、基礎と屋根が比較的小さな床面積で分けられているため、MIが比較的高くなります。

## figure3 ばらつき

- Figure 3 shows the variability of the datapoints per building type in a boxplot, except for the building types with too few datapoints to construct a boxplot (n < 4).
  - 図3は、建物タイプごとのばらつきをボックスプロットで示したものである。
  - データポイントが少なすぎてボックスプロットを構成できない建物タイプ（n＜4）の場合は、平均値のみを表示する。
  - ![](https://onlinelibrary.wiley.com/cms/asset/2a3b28d7-e293-40b1-b79a-78584774a6fd/jiec13143-fig-0003-m.png)
- **The non-office utility buildings have a particularly high variability. オフィス以外の公共施設は、特に変動が大きい**。
  - これは、その機能が大きく変化するため、建物の設計がすべての建物タイプの中で最も均一でないためである。
  - 非常に高いデータポイントは、いくつかのビルが駐車場を含んでおり、これらの駐車場が建物の構造の一部である場合、結果として生じるコンクリートの流れも "建物の構造" と一緒になることで説明できる。

## figure 4
- The distribution demolition projects per age cohort and building type is shown in Figure 4. 図4は、解体工事の年代別、建物タイプ別の分布を示したもの.
  - 縦軸の単位はデータポイント(観測値)の数？？
  - ![](https://onlinelibrary.wiley.com/cms/asset/7b0f0112-5ccf-4099-b3de-0bd89058bc7f/jiec13143-fig-0004-m.png)
  - この図には、比較のためにオランダの全建築物ストックの分布も示されている。
  - 解体された住宅は1945年から1970年の間に建てられたものが多く、オフィスビルは1971年から2000年のものが多い。
  - 比較的最近に建てられた公共施設（2000年より新しい建物）も取り壊されているが、住宅用建物はない。
  - これは、オフィスビルが建てられすぎた一方で、住宅ビルの需要が近年急激に高まっていることを反映しており、現在は可能な限り住宅ビルに転換している（Meeste Oppervlakteleegstand Bij Kantoren En Winkels, 2019）。
  - 空いた公共施設やオフィスビルを住宅に改装できない場合は、取り壊して建て替えることになります。

# Discussion
## Summary
- 既存の文献と比較して、本論文はデータポイントを大幅に増やし、解体物の流れに見られる様々な種類の材料についてより詳細に説明しています。
- 我々のMIデータベースのデータポイントの数は、これまでのMIデータセットの大部分よりも1桁か2桁多く、同様の規模の他のデータベース（Yang et al.、2020）と比べても1つだけである。
- このようにデータが豊富になったことは、データマイニングや機械学習などのビッグデータ手法を産業エコロジー研究に適用するための一歩となる。
  - 例えば、決定木やランダムフォレストなどの分類手法やクラスタリングアプローチを用いて、データに内在する特性を探ることができる。
  - このような手法と組み合わせることで、現在ごく少数の観測データの単純平均に基づいて行われている典型的なMI範囲の評価も向上させることができます。
- 全体として、1平方メートルあたりの物質強度は他の研究の結果と一致しており（表4参照）、別々の物質に細かく分類した場合の精度に対する信頼が高まっています。

- In conclusion, the combination of real-world demolition data obtained from and processed in close cooperation with a demolition company, combined with GIS data is a novel data acquisition method compared to existing work. 
  - 結論として、解体業者と密接に協力して取得・処理した実際の解体データをGISデータと組み合わせることは、既存の手法と比較して新しいデータ取得方法であると言えます。
- This approach yields material intensities for the building stock, and—we believe—improves upon the accuracy of these data.
  - この手法により、建物ストックの材料強度が得られ、これらのデータの精度を向上させることができると考えています。

## Limitations
- いくつかの小さな材料の流れは、一般的なC&DWの流れと一緒に建築現場から取り除かれるため、データベースから除外されており、そのため文書化も十分ではありません。
- また、銅はデータベースの部品として報告されていますが、この金属が建物内で使用されるすべての用途を完全に網羅しているわけではありません。
- さらに、ここで報告されているデータは、建物が取り壊される前の専門家の推定に基づくものです
  - 精度は高いものの、実際に計量されたマテリアルフローが報告されれば、なお改善されるはず
  - これが不可能だった理由は、異なる材料が異なる下請け業者によって異なる時期に回収されるから
  - これらのデータを一貫して収集することは、組織的な観点から不可能であることが判明しました。

## Recommendations for future research
- 次の論文では、このデータベースをオランダのいくつかの都市のダイナミックモデルに適用する予定である。
  - 他のいくつかの同規模のデータセットとともに、建築環境のストックとフローの分析にビッグデータの手法を適用するための最初のステップを踏み出すことができるだろう。
- もう一つの論理的なステップは、Reschら（2020）が行ったように、材料に関連する環境影響を追加することである。

- モデリング演習でデータベースを使用する以外にも、我々はデータを改善するためのいくつかの機会を特定した。成分セクションをさらに「内部」と「外部」のサブセットに細分化することが可能である。
  - 建物の大きさと建物周辺に見られる部品数の関係は非常に不規則であるため（特に公共施設の建物）、将来的には建物周辺を個別にモデル化することで、外挿の精度を高めることができるだろう。
- 最後に、地下室と基礎は、特に大規模な地下駐車場を持つ建物に関して、顕著な不確実性の要因となっている。

# Reference
